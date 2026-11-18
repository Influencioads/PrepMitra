"""Writes batches/parts/BATCH_001_CHE_p2.json: package CHE_001_p2 of BATCH_001 (Chemistry, 119 questions).

Topics: d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of Organic Compounds,
Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen,
Biomolecules (Chemistry), Principles Related to Practical Chemistry. IDs NEET_CHE_000132..NEET_CHE_000250.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_001/CHE_001_p2.py
"""

import itertools
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
OUT = ROOT / "batches" / "parts" / "BATCH_001_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
# ai:self-recheck = a second, separate solve of every question by the author after the file was written.
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
# Questions the coordinator answered blind (separate solve) and matched; it added ai:independent-check to them.
# NEET_CHE_000142 was replaced on 2026-11-16 after a syllabus-scope audit and awaits a new blind check.
BLIND_CHECKED = {f"NEET_CHE_{n:06d}" for n in range(132, 251)} - {"NEET_CHE_000142"}

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
    assert answer in LETTERS and len(options) == 4
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
                         "verified_by": list(verified_by) + (["ai:independent-check"] if qid in BLIND_CHECKED else []),
                         "verified_at": TODAY},
    }


_NEXT = iter(range(132, 251))


def Q(topic, subtopic, difficulty, fmt, text, options, answer, *rest, **kw):
    """q() with the next ID of this package (questions are written in ID order)."""
    return q(f"NEET_CHE_{next(_NEXT):06d}", CHE, topic, subtopic, difficulty, fmt, text, options, answer, *rest, **kw)


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


# ---------------------------------------------------------------- shared chemistry helpers
def spin_only(n):
    """Spin-only magnetic moment in BM for n unpaired electrons, rounded to 2 decimals."""
    return round(math.sqrt(n * (n + 2)), 2)


def unpaired_oct(d, low_spin):
    """Unpaired electrons for an octahedral d^n ion (t2g holds 6, eg holds 4)."""
    if low_spin:
        t2g, eg = min(d, 6), max(0, d - 6)
    else:
        t2g = min(d, 3) + max(0, min(d - 5, 3)) if d > 5 else min(d, 3)
        eg = min(max(d - 3, 0), 2) + (max(0, d - 8) if d > 8 else 0)
    up = lambda n, cap: n if n <= cap // 2 else cap - n
    return up(t2g, 6) + up(eg, 4)


def cfse_oct(d, low_spin):
    """CFSE in units of Delta_o (pairing energy ignored): t2g -0.4 each, eg +0.6 each."""
    if low_spin:
        t2g, eg = min(d, 6), max(0, d - 6)
    else:
        t2g = min(d, 3) + max(0, min(d - 5, 3))
        eg = min(max(d - 3, 0), 2) + max(0, d - 8)
    return F(-4, 10) * t2g + F(6, 10) * eg


assert [unpaired_oct(d, False) for d in range(11)] == [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
assert [unpaired_oct(d, True) for d in range(11)] == [0, 1, 2, 3, 2, 1, 0, 1, 2, 1, 0]
assert spin_only(1) == 1.73 and spin_only(3) == 3.87 and spin_only(4) == 4.9 and spin_only(5) == 5.92

# Octahedral stereoisomer counter: positions 0/1 = +x/-x, 2/3 = +y/-y, 4/5 = +z/-z.
OPP = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}


def _rotations():
    rx = (0, 1, 4, 5, 3, 2)  # 90 deg about x: +y -> +z, +z -> -y
    ry = (5, 4, 2, 3, 0, 1)  # 90 deg about y: +z -> +x, +x -> -z
    group = {tuple(range(6))}
    frontier = list(group)
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
INV = (1, 0, 3, 2, 5, 4)
ALL_OPS = ROT | {tuple(INV[g[i]] for i in range(6)) for g in ROT}
assert len(ALL_OPS) == 48


def octahedral_isomers(mono, n_bidentate):
    """(stereoisomers, geometrical isomers) of an octahedral complex with symmetric AA chelates."""
    configs = set()
    cis_edges = [frozenset((a, b)) for a in range(6) for b in range(a + 1, 6) if OPP[a] != b]
    for edges in itertools.combinations(cis_edges, n_bidentate):
        used = set().union(*edges) if edges else set()
        if len(used) != 2 * n_bidentate:
            continue
        free = [p for p in range(6) if p not in used]
        for perm in set(itertools.permutations(mono)):
            configs.add((frozenset(edges), tuple(sorted(zip(free, perm)))))

    def canon(cfg, ops):
        edges, mono_pos = cfg
        forms = []
        for g in ops:
            e = frozenset(frozenset(g[p] for p in edge) for edge in edges)
            m = tuple(sorted((g[p], lab) for p, lab in mono_pos))
            forms.append((sorted(sorted(x) for x in e), m))
        return min(forms)

    stereo = {repr(canon(c, ROT)) for c in configs}
    geom = {repr(canon(c, ALL_OPS)) for c in configs}
    return len(stereo), len(geom)


assert octahedral_isomers(["a", "a", "a", "a", "b", "b"], 0) == (2, 2)  # [MA4B2]: cis, trans
assert octahedral_isomers(["a", "a", "a", "b", "b", "b"], 0) == (2, 2)  # [MA3B3]: fac, mer
assert octahedral_isomers([], 3) == (2, 1)  # [M(AA)3]: one pair of enantiomers

# Constants used in several stems
M_AG, M_AGCL, M_CL = 108, F(1435, 10), F(355, 10)


# ================================================================ d- and f-Block Elements (132-143)
# 133: Fe3+ (aq) is 3d5 high spin
assert spin_only(unpaired_oct(5, False)) == 5.92 and spin_only(4) == 4.9 and spin_only(3) == 3.87
# 136: Cr2O7(2-) + 14H+ + 6e- -> 2Cr3+ ; Fe2+ -> Fe3+ + e-
mol_fe = F(1, 10) * 6
assert mol_fe == F(6, 10) and F(1, 10) * 3 == F(3, 10) and F(1, 10) * 5 == F(5, 10)
# 138: d-counts of M2+: Ti 2, Mn 5, Fe 6, Co 7 (aqua ions are high spin)
moments = {ion: spin_only(unpaired_oct(d, False)) for ion, d in {"Ti": 2, "Mn": 5, "Fe": 6, "Co": 7}.items()}
assert [k for k, v in moments.items() if v == 3.87] == ["Co"]
# 141: FeC2O4 gives 3 e- per formula unit (Fe2+ -> Fe3+: 1, C2O4(2-) -> 2CO2: 2); MnO4- takes 5 e-
mmol_e = 1 * 3
vol_kmno4 = F(mmol_e, 5) / F(2, 100)
assert vol_kmno4 == 30 and F(1, 5) / F(2, 100) == 10 and F(2, 5) / F(2, 100) == 20 and 1 / F(2, 100) == 50
# 143: Mn(VI) in MnO4(2-) is 3d1, Mn(VII) in MnO4- is 3d0
assert (spin_only(7 - 6), spin_only(7 - 7)) == (1.73, 0.0)

QUESTIONS = []
QUESTIONS += [
    Q(T_DF, "Transition element trends", "Basic", "direct",
      "Which element of the first transition series (3d series) shows every oxidation state from +2 to +7?",
      ["Scandium", "Manganese", "Zinc", "Copper"], "B",
      "Variable oxidation states of 3d elements",
      "The number of oxidation states is greatest in or near the middle of the series, where both 4s and 3d "
      "electrons can take part in bonding. Manganese (3d⁵4s²) can use all seven of these electrons.",
      ["Mn: [Ar] 3d⁵ 4s² → maximum oxidation state = 2 + 5 = +7",
       "Mn shows +2 (MnSO₄), +3, +4 (MnO₂), +6 (K₂MnO₄) and +7 (KMnO₄)",
       "Sc shows mainly +3, Zn only +2, Cu mainly +1 and +2"],
      why_others_wrong="Sc and Zn sit at the ends of the series and show essentially one oxidation state; Cu shows "
                       "only +1 and +2.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxidation states", seconds=25),

    Q(T_DF, "Magnetic and colour properties", "Basic", "numerical",
      "The spin-only magnetic moment of the Fe³⁺ ion in aqueous solution (Z of Fe = 26) is about:",
      ["4.90 BM", "3.87 BM", "5.92 BM", "1.73 BM"], "C",
      "Spin-only formula μ = √[n(n + 2)] BM",
      "Fe³⁺ is 3d⁵. Water is a weak-field ligand, so the five electrons stay unpaired.",
      ["Fe: [Ar] 3d⁶ 4s² → Fe³⁺: [Ar] 3d⁵", "n = 5 unpaired electrons",
       "μ = √(5 × 7) = √35 ≈ 5.92 BM"],
      why_others_wrong="4.90 BM is for Fe²⁺ (3d⁶, n = 4). 3.87 BM is for n = 3. 1.73 BM assumes the electrons pair "
                       "up, leaving one unpaired, which does not happen with water.",
      seconds=35, verified_by=RECOMPUTED),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "direct",
      "Because of the lanthanoid contraction, which pair of elements has almost the same atomic radius?",
      ["Ti and Zr", "Sc and Y", "V and Nb", "Zr and Hf"], "D",
      "Lanthanoid contraction",
      "The 4f electrons shield the nuclear charge poorly, so radii shrink steadily across the lanthanoids. This "
      "cancels the expected increase from the 4d to the 5d series, so Zr (160 pm) and Hf (159 pm) are almost the "
      "same size.",
      ["Going from period 5 to period 6 adds a shell, which should increase the radius",
       "The 14 lanthanoids in between contract the radius by about the same amount",
       "Result: 4d and 5d elements of the same group (Zr/Hf, Nb/Ta, Mo/W) have nearly equal radii"],
      why_others_wrong="Ti/Zr, Sc/Y and V/Nb are 3d/4d pairs: no lanthanoids lie between them, so the heavier "
                       "element is clearly larger.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', lanthanoid contraction", seconds=30),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Basic", "statement_pair",
      *sp("In acidic solution, the permanganate ion is reduced to Mn²⁺ by gaining five electrons per ion.", True,
          "Orange dichromate solution turns yellow when its pH is raised, because dichromate changes into "
          "chromate.", True),
      "Oxidising action of KMnO₄ and the chromate–dichromate equilibrium",
      "In acid, MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O (Mn goes from +7 to +2). Chromate (yellow) and dichromate (orange) "
      "interconvert with pH: 2CrO₄²⁻ + 2H⁺ ⇌ Cr₂O₇²⁻ + H₂O. Adding alkali removes H⁺ and shifts the equilibrium "
      "to chromate.",
      ["Statement I: oxidation state of Mn changes from +7 to +2 → 5 electrons → true",
       "Statement II: raising pH (adding OH⁻) shifts the equilibrium to yellow CrO₄²⁻ → true"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate", seconds=40),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Intermediate", "numerical",
      "How many moles of Fe²⁺ ions are oxidised to Fe³⁺ by 0.1 mol of K₂Cr₂O₇ in acidic solution?",
      ["0.6 mol", "0.3 mol", "0.5 mol", "0.1 mol"], "A",
      "Electron balance in a dichromate titration",
      "Each Cr goes from +6 to +3, so one Cr₂O₇²⁻ accepts 6 electrons. Each Fe²⁺ gives one electron.",
      ["Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O", "Fe²⁺ → Fe³⁺ + e⁻",
       "So 1 mol Cr₂O₇²⁻ oxidises 6 mol Fe²⁺", "0.1 mol × 6 = 0.6 mol Fe²⁺"],
      why_others_wrong="0.3 mol counts the change of only one Cr atom (3 electrons). 0.5 mol uses the 5 electrons of "
                       "permanganate. 0.1 mol assumes a 1 : 1 mole ratio.",
      seconds=45, verified_by=RECOMPUTED),

    Q(T_DF, "Transition element trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the 3d series are correct?",
          [("Sc³⁺ ions are coloured in aqueous solution.", False),
           ("Transition metals have high enthalpies of atomisation because many unpaired d electrons take part in "
            "metallic bonding.", True),
           ("Manganese shows a maximum oxidation state of +8.", False),
           ("Zn, Cd and Hg are not regarded as transition metals because their d orbitals are completely filled in "
            "the ground state and in their common oxidation state.", True),
           ("Copper is the only 3d metal with a positive standard electrode potential E°(M²⁺/M).", True)],
          [["a", "b", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
      "General properties of the 3d series",
      "Check each statement against the electronic configurations and the trends in the d-block chapter.",
      ["(a) Sc³⁺ is 3d⁰: no d–d transition is possible, so it is colourless → false",
       "(b) Unpaired d electrons strengthen metallic bonding → high atomisation enthalpies → true",
       "(c) The highest oxidation state of Mn is +7 (in MnO₄⁻) → false",
       "(d) Zn²⁺, Cd²⁺, Hg²⁺ are d¹⁰, so these metals are not counted as transition metals → true",
       "(e) E°(Cu²⁺/Cu) = +0.34 V; all other 3d metals have negative values → true"],
      why_others_wrong="Any option containing (a) or (c) is wrong; (a) is the usual trap because Sc is in the 3d "
                       "series but its only ion has no d electrons.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', general properties of the transition elements", seconds=75),

    Q(T_DF, "Magnetic and colour properties", "Intermediate", "numerical",
      "An aqueous M²⁺ ion of the 3d series has a spin-only magnetic moment of about 3.87 BM. M can be "
      "(atomic numbers: Ti 22, Mn 25, Fe 26, Co 27):",
      ["Ti", "Mn", "Co", "Fe"], "C",
      "Working back from μ to the number of unpaired electrons",
      "μ = √[n(n + 2)] = 3.87 BM gives n = 3. Aqua complexes of M²⁺ ions are high spin, so the d count must be d³ "
      "or d⁷.",
      ["√15 ≈ 3.87 → n(n + 2) = 15 → n = 3",
       "Ti²⁺ 3d² → 2 unpaired (2.83 BM); Mn²⁺ 3d⁵ → 5 (5.92 BM)",
       "Fe²⁺ 3d⁶ → 4 (4.90 BM); Co²⁺ 3d⁷ → 3 (3.87 BM)"],
      why_others_wrong="Mn²⁺ and Fe²⁺ have 5 and 4 unpaired electrons. Ti²⁺ has only 2.",
      seconds=60, verified_by=RECOMPUTED),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Intermediate", "assertion_reason",
      *ar("Titrations with potassium permanganate are not carried out in the presence of hydrochloric acid.", True,
          "Permanganate oxidises hydrochloric acid to chlorine, so part of the titrant is used up by the acid.",
          True, explains=True),
      "Choice of acid in permanganate titrations",
      "KMnO₄ is a strong enough oxidant to oxidise Cl⁻ to Cl₂. In HCl, some permanganate would react with the acid "
      "instead of the substance being estimated, giving a wrong (high) titre. Dilute H₂SO₄ is used instead.",
      ["A is true: permanganate titrations are done in dilute H₂SO₄",
       "R is true: 2MnO₄⁻ + 16H⁺ + 10Cl⁻ → 2Mn²⁺ + 5Cl₂ + 8H₂O",
       "R is exactly why HCl is avoided → R explains A"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate", seconds=40),

    Q(T_DF, "Magnetic and colour properties", "Intermediate", "match_list",
      *ml("Match the aquated ion in List-I with its colour in List-II.",
          ["Ti³⁺", "Cu²⁺", "Zn²⁺", "Mn²⁺"], ["Colourless", "Pink", "Purple", "Blue"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}], "B"),
      "Colour of transition metal ions from d–d transitions",
      "A transition metal ion is coloured when it has partly filled d orbitals: light of a particular wavelength "
      "excites an electron from a lower to a higher d level, and we see the complementary colour. A d¹⁰ ion "
      "has no d–d transition.",
      ["Ti³⁺ (3d¹) → purple → III", "Cu²⁺ (3d⁹) → blue → IV", "Zn²⁺ (3d¹⁰) → no d–d transition → colourless → I",
       "Mn²⁺ (3d⁵) → pale pink → II"],
      why_others_wrong="A-IV, B-III swaps purple Ti³⁺ and blue Cu²⁺. C-II, D-I makes d¹⁰ Zn²⁺ coloured. A-II, "
                       "D-III swaps Ti³⁺ and Mn²⁺.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', formation of coloured ions", seconds=45),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Advanced", "numerical",
      "A sample containing 1.0 mmol of ferrous oxalate (FeC₂O₄) is dissolved in dilute H₂SO₄ and titrated with "
      "0.02 M KMnO₄ until both Fe²⁺ and oxalate are completely oxidised. The volume of KMnO₄ used is:",
      ["10 mL", "20 mL", "50 mL", "30 mL"], "D",
      "Equivalents when one compound contains two reducing parts",
      "Permanganate oxidises Fe²⁺ to Fe³⁺ (1 electron) and C₂O₄²⁻ to 2CO₂ (2 electrons). So each FeC₂O₄ gives 3 "
      "electrons, and each MnO₄⁻ takes 5.",
      ["Electrons given: 1.0 mmol × 3 = 3.0 mmol",
       "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O → mmol MnO₄⁻ = 3.0/5 = 0.60 mmol",
       "Volume = 0.60 mmol / 0.02 mmol mL⁻¹ = 30 mL"],
      shortcut="mmol × electrons must match: 0.02 × V × 5 = 1.0 × 3 → V = 30 mL.",
      why_others_wrong="10 mL counts only Fe²⁺ (1 electron). 20 mL counts only oxalate (2 electrons). 50 mL assumes "
                       "a 1 : 1 mole ratio of KMnO₄ to FeC₂O₄.",
      seconds=110, verified_by=RECOMPUTED),

    Q(T_DF, "Lanthanoids and actinoids", "Advanced", "multi_statement",
      *ms("Consider the following statements about the f-block elements.",
          [("Yb²⁺, with a 4f¹⁴ configuration, acts as a reducing agent, changing to the common +3 state.", True),
           ("Actinoids show a smaller range of oxidation states than lanthanoids.", False),
           ("The most common oxidation state of the lanthanoids is +3.", True),
           ("Eu²⁺ is a strong oxidising agent.", False),
           ("Ce⁴⁺ is a strong oxidising agent, changing to the common +3 state.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["b", "c", "e"]], "B"),
      "Oxidation states of lanthanoids and actinoids",
      "Lanthanoids mainly show +3; a +2 ion tends to lose an electron and a +4 ion to gain one, returning to +3. The "
      "5f, 6d and 7s levels of actinoids are close in energy, so actinoids show many more oxidation states.",
      ["(a) Yb²⁺ (4f¹⁴) readily loses an electron to become Yb³⁺ → reductant → true",
       "(b) Actinoids show a wider range of oxidation states (uranium, for example, reaches +6) → false",
       "(c) +3 is the characteristic oxidation state of lanthanoids → true",
       "(d) Eu²⁺ (4f⁷) readily changes to Eu³⁺, losing an electron → it is a strong reducing agent → false",
       "(e) Ce⁴⁺ (4f⁰) readily gains an electron to become Ce³⁺ → strong oxidant → true"],
      why_others_wrong="Swapping the roles of Eu²⁺ (reductant) and Ce⁴⁺ (oxidant) is the trap behind options that "
                       "include (d).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids and the actinoids", seconds=90),

    Q(T_DF, "Magnetic and colour properties", "Advanced", "numerical",
      "The spin-only magnetic moments (in BM) of the manganese species in K₂MnO₄ and in KMnO₄ are, respectively "
      "(Z of Mn = 25):",
      ["0 and 1.73", "1.73 and 2.83", "1.73 and 0", "2.83 and 1.73"], "C",
      "Oxidation state → d-electron count → magnetic moment",
      "In K₂MnO₄ manganese is +6; in KMnO₄ it is +7. Mn has seven valence electrons (3d⁵4s²).",
      ["K₂MnO₄: 2(+1) + x + 4(−2) = 0 → x = +6 → 3d¹ → n = 1 → μ = √3 = 1.73 BM (green, paramagnetic)",
       "KMnO₄: +1 + x − 8 = 0 → x = +7 → 3d⁰ → n = 0 → μ = 0 (diamagnetic)"],
      why_others_wrong="'0 and 1.73' swaps the two compounds. Values with 2.83 BM (n = 2) treat Mn(VI) as 3d², as if "
                       "Mn had eight valence electrons.",
      seconds=75, verified_by=RECOMPUTED),
]


# ================================================================ Coordination Compounds (144-157)
# 146: CoCl3.4NH3 with CN 6 = [Co(NH3)4Cl2]Cl -> 1 ionisable Cl- per formula unit
mass_agcl = F(1, 100) * 1 * M_AGCL
assert mass_agcl == F(1435, 1000) and F(1, 100) * 2 * M_AGCL == F(287, 100) and F(1, 100) * 3 * M_AGCL == F(4305, 1000)
# 148: [Fe(CN)6]4-: Fe2+ d6 low spin
assert cfse_oct(6, True) == F(-12, 5) and cfse_oct(6, False) == F(-2, 5)
assert cfse_oct(5, True) == F(-2) and cfse_oct(4, True) == F(-8, 5)
# 149: [Co(en)2Cl2]+ -> 3 stereoisomers (trans + cis pair), 2 geometrical
assert octahedral_isomers(["Cl", "Cl"], 2) == (3, 2)
# 154: Delta_o = N_A h c / lambda for [Ti(H2O)6]3+ absorbing at 498 nm
h, c, NA = 6.626e-34, 3.0e8, 6.022e23
delta_o = NA * h * c / 498e-9 / 1000
assert round(delta_o) == 240 and round(delta_o / 0.6) == 401 and round(delta_o / 2) == 120
# 155: Fe3+ d5: CN- low spin (1 unpaired), F- high spin (5 unpaired)
assert (spin_only(unpaired_oct(5, True)), spin_only(unpaired_oct(5, False))) == (1.73, 5.92)
# 156: [Co(en)(NH3)2Cl2]+ -> 4 stereoisomers, 3 geometrical
assert octahedral_isomers(["N", "N", "Cl", "Cl"], 1) == (4, 3)

QUESTIONS += [
    Q(T_CC, "Werner's theory and ligands", "Basic", "direct",
      "Which of the following is an ambidentate ligand?",
      ["NO₂⁻", "Ethane-1,2-diamine (en)", "NH₃", "C₂O₄²⁻"], "A",
      "Types of ligands",
      "An ambidentate ligand can bind to the metal through either of two different donor atoms, but only one at a "
      "time. The nitrite ion can bind through N (nitrito-N) or through O (nitrito-O).",
      ["NO₂⁻: donor atom N or O → ambidentate",
       "en and C₂O₄²⁻ bind through two atoms at the same time → bidentate (chelating), not ambidentate",
       "NH₃ has a single donor atom → unidentate"],
      why_others_wrong="Bidentate ligands use two donor atoms together; ambidentate ligands use one of two possible "
                       "donor atoms.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms (ligands)", seconds=25),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of K₃[Fe(CN)₆] is:",
      ["Potassium hexacyanidoferrate(II)", "Potassium hexacyanidoiron(III)", "Potassium hexacyanidoferrate(III)",
       "Hexacyanidoferrate(III) potassium"], "C",
      "Naming an anionic complex",
      "The cation is named first. In an anionic complex the metal name ends in -ate (iron → ferrate) and its "
      "oxidation state follows in Roman numerals. CN⁻ as a ligand is 'cyanido'.",
      ["Charge of the complex ion: 3 K⁺ → [Fe(CN)₆]³⁻",
       "x + 6(−1) = −3 → x = +3",
       "Name: potassium hexacyanidoferrate(III)"],
      why_others_wrong="(II) gets the oxidation state wrong. 'iron' is used only for a cationic or neutral complex. "
                       "The cation must come first.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=30),

    Q(T_CC, "Werner's theory and ligands", "Basic", "numerical",
      "An octahedral complex has the composition CoCl₃·4NH₃, and cobalt has a coordination number of 6 in it. When "
      "0.01 mol of the complex is treated with excess AgNO₃ solution, the mass of AgCl precipitated is "
      "(molar mass of AgCl = 143.5 g mol⁻¹):",
      ["2.870 g", "1.435 g", "4.305 g", "0.718 g"], "B",
      "Werner's theory: primary (ionisable) and secondary valences",
      "Coordination number 6 needs six ligands: four NH₃ and two Cl⁻. Only the remaining Cl⁻ lies outside the "
      "coordination sphere and is precipitated by Ag⁺.",
      ["Formula: [Co(NH₃)₄Cl₂]Cl → one ionisable Cl⁻",
       "mol AgCl = 0.01 × 1 = 0.01 mol",
       "Mass = 0.01 × 143.5 = 1.435 g"],
      why_others_wrong="2.870 g counts two ionisable chlorides and 4.305 g counts all three, ignoring the chloride "
                       "ligands bound to Co. 0.718 g halves the correct amount.",
      seconds=45, verified_by=RECOMPUTED),

    Q(T_CC, "Applications", "Basic", "statement_pair",
      *sp("Hardness of water is estimated by simple titration with Na₂EDTA, as Ca²⁺ and Mg²⁺ form stable complexes "
          "with EDTA.", True,
          "Chlorophyll, the pigment responsible for photosynthesis, is a coordination compound of iron.", False),
      "Importance of coordination compounds",
      "EDTA titrations are the standard way to estimate Ca²⁺ and Mg²⁺. Chlorophyll is a magnesium complex; "
      "haemoglobin is the iron complex.",
      ["Statement I: EDTA forms stable complexes with Ca²⁺ and Mg²⁺ → true",
       "Statement II: chlorophyll contains Mg, not Fe → false"],
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications of coordination compounds", seconds=30),

    Q(T_CC, "Crystal field theory", "Intermediate", "numerical",
      "Ignoring the pairing energy, the crystal field stabilisation energy (CFSE) of [Fe(CN)₆]⁴⁻ is:",
      ["−0.4 Δo", "−2.0 Δo", "−1.6 Δo", "−2.4 Δo"], "D",
      "CFSE in an octahedral field",
      "In an octahedral field each t₂g electron is stabilised by 0.4 Δo and each eg electron destabilised by "
      "0.6 Δo. CN⁻ is a strong-field ligand, so Fe²⁺ (3d⁶) is low spin.",
      ["Fe²⁺: 3d⁶; strong field (Δo > P) → t₂g⁶ eg⁰",
       "CFSE = 6 × (−0.4 Δo) + 0 × (0.6 Δo) = −2.4 Δo"],
      why_others_wrong="−0.4 Δo is the high-spin value (t₂g⁴ eg²), as if CN⁻ were a weak-field ligand. −2.0 Δo uses "
                       "Fe³⁺ (t₂g⁵). −1.6 Δo is for t₂g⁴ (a d⁴ low-spin ion).",
      seconds=50, verified_by=RECOMPUTED),

    Q(T_CC, "Isomerism", "Intermediate", "numerical",
      "The total number of stereoisomers (geometrical and optical) possible for [Co(en)₂Cl₂]⁺ is:",
      ["2", "4", "6", "3"], "D",
      "Geometrical and optical isomerism in octahedral [M(AA)₂B₂] complexes",
      "The two Cl ligands can be trans or cis. The trans form has a mirror plane, so it is optically inactive. The "
      "cis form has no mirror plane, so it exists as a pair of enantiomers.",
      ["trans-[Co(en)₂Cl₂]⁺: 1 isomer (achiral)",
       "cis-[Co(en)₂Cl₂]⁺: 2 isomers (d and l)",
       "Total = 1 + 2 = 3"],
      why_others_wrong="2 counts only cis and trans and misses the optical pair. 4 wrongly gives the trans form an "
                       "enantiomer too.",
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=50,
      verified_by=RECOMPUTED),

    Q(T_CC, "Crystal field theory", "Intermediate", "assertion_reason",
      *ar("[CoF₆]³⁻ is paramagnetic, whereas [Co(NH₃)₆]³⁺ is diamagnetic.", True,
          "NH₃ is a weaker field ligand than F⁻.", False),
      "Spectrochemical series and spin state",
      "Co³⁺ is 3d⁶. F⁻ is a weak-field ligand (Δo < P), so the electrons go into eg before pairing: t₂g⁴eg², four "
      "unpaired electrons. NH₃ is a stronger field ligand (Δo > P), so all six electrons pair in t₂g: diamagnetic.",
      ["A: [CoF₆]³⁻ has 4 unpaired electrons, [Co(NH₃)₆]³⁺ has none → true",
       "R: in the spectrochemical series F⁻ < H₂O < NH₃, so NH₃ is the stronger field ligand → false"],
      why_others_wrong="R reverses the spectrochemical order; the true reason is that NH₃ is the stronger field "
                       "ligand.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory", seconds=45),

    Q(T_CC, "Valence bond theory", "Intermediate", "match_list",
      *ml("Match the complex in List-I with the hybridisation of the metal in List-II.",
          ["[Ni(CO)₄]", "[CoF₆]³⁻", "[PtCl₄]²⁻", "[Fe(CN)₆]³⁻"], ["dsp²", "sp³", "d²sp³", "sp³d²"],
          {"A": "II", "B": "IV", "C": "I", "D": "III"},
          [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
           {"A": "II", "B": "IV", "C": "III", "D": "I"}], "A"),
      "Valence bond theory: hybridisation and geometry",
      "Decide the d count of the metal and whether the ligand pairs the d electrons. Strong-field ligands (CO, CN⁻) "
      "free inner d orbitals; F⁻ does not, so outer 4d orbitals are used.",
      ["[Ni(CO)₄]: Ni(0), CO pairs electrons into 3d¹⁰ → 4s4p³ → sp³, tetrahedral → II",
       "[CoF₆]³⁻: Co³⁺ 3d⁶, F⁻ weak → outer orbital sp³d², 4 unpaired → IV",
       "[PtCl₄]²⁻: Pt²⁺ 5d⁸ → one 5d orbital emptied → dsp², square planar → I",
       "[Fe(CN)₆]³⁻: Fe³⁺ 3d⁵, CN⁻ strong → inner orbital d²sp³, 1 unpaired → III"],
      why_others_wrong="Codes giving [CoF₆]³⁻ d²sp³ treat F⁻ as a strong-field ligand; codes giving [Ni(CO)₄] dsp² "
                       "confuse it with square planar d⁸ complexes.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=60),

    Q(T_CC, "Isomerism", "Intermediate", "multi_statement",
      *ms("Which of the following statements about isomerism in coordination compounds are correct?",
          [("[Co(NH₃)₅(NO₂)]Cl₂ and [Co(NH₃)₅(ONO)]Cl₂ are linkage isomers.", True),
           ("[Co(NH₃)₆][Cr(CN)₆] and [Cr(NH₃)₆][Co(CN)₆] are ionisation isomers.", False),
           ("[Co(NH₃)₅(SO₄)]Br and [Co(NH₃)₅Br]SO₄ are ionisation isomers.", True),
           ("A square planar complex of the type [MABCD] shows optical isomerism.", False),
           ("[Cr(H₂O)₆]Cl₃ and [Cr(H₂O)₅Cl]Cl₂·H₂O are solvate (hydrate) isomers.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "e"]], "C"),
      "Structural and stereoisomerism in complexes",
      "Name each pair by what differs between the two formulas: the donor atom of one ligand, the ligands shared "
      "between a complex cation and anion, the ion inside versus outside the sphere, or water inside versus outside.",
      ["(a) NO₂⁻ bound through N in one and through O in the other → linkage → true",
       "(b) Ligands are exchanged between the cationic and anionic complexes → coordination isomers, not "
       "ionisation isomers → false",
       "(c) SO₄²⁻ and Br⁻ swap between the coordination sphere and the counter-ion → ionisation → true",
       "(d) A square planar complex lies in a plane, which is a mirror plane → never optically active → false",
       "(e) Water inside versus outside the sphere → solvate (hydrate) isomers → true"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=80),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "direct",
      "Equimolar aqueous solutions of the following are compared. Which one has the lowest molar conductivity?",
      ["[Co(NH₃)₆]Cl₃", "[Co(NH₃)₃Cl₃]", "[Co(NH₃)₅Cl]Cl₂", "[Co(NH₃)₄Cl₂]Cl"], "B",
      "Ionisation of complexes and conductivity",
      "Molar conductivity rises with the number of ions a complex gives in solution. Ligands inside the square "
      "brackets do not ionise.",
      ["[Co(NH₃)₆]Cl₃ → 4 ions", "[Co(NH₃)₅Cl]Cl₂ → 3 ions", "[Co(NH₃)₄Cl₂]Cl → 2 ions",
       "[Co(NH₃)₃Cl₃] → non-electrolyte (no ions) → lowest conductivity"],
      seconds=35),

    Q(T_CC, "Crystal field theory", "Advanced", "numerical",
      "[Ti(H₂O)₆]³⁺ absorbs light most strongly at 498 nm, owing to a t₂g → eg transition of its single d "
      "electron. The crystal field splitting energy Δo in kJ mol⁻¹ is about "
      "(h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, N_A = 6.022 × 10²³ mol⁻¹):",
      ["240", "120", "24.0", "401"], "A",
      "Δo from the absorption wavelength of a d¹ ion",
      "For a d¹ ion, the energy of the absorbed photon equals Δo (the gap between t₂g and eg). Convert the energy per "
      "ion into energy per mole.",
      ["E per ion = hc/λ = (6.626 × 10⁻³⁴ × 3.0 × 10⁸)/(498 × 10⁻⁹) = 3.99 × 10⁻¹⁹ J",
       "Per mole: 3.99 × 10⁻¹⁹ × 6.022 × 10²³ = 2.40 × 10⁵ J mol⁻¹",
       "Δo ≈ 240 kJ mol⁻¹"],
      why_others_wrong="120 halves the photon energy. 24.0 comes from a power-of-ten slip in converting nm to m. 401 "
                       "divides by 0.6, wrongly treating the photon energy as only the eg rise (0.6 Δo).",
      seconds=100, verified_by=RECOMPUTED),

    Q(T_CC, "Valence bond theory", "Advanced", "numerical",
      "The spin-only magnetic moments (in BM) of [Fe(CN)₆]³⁻ and [FeF₆]³⁻ are, respectively:",
      ["5.92 and 1.73", "1.73 and 5.92", "0 and 4.90", "3.87 and 5.92"], "B",
      "Ligand strength decides the number of unpaired electrons",
      "Both contain Fe³⁺ (3d⁵). CN⁻ pairs the d electrons (inner orbital d²sp³ complex); F⁻ does not (outer orbital "
      "sp³d² complex).",
      ["[Fe(CN)₆]³⁻: 3d⁵ paired as far as possible in three orbitals → 1 unpaired → √3 = 1.73 BM",
       "[FeF₆]³⁻: 5 unpaired → √35 = 5.92 BM"],
      why_others_wrong="'5.92 and 1.73' swaps strong and weak field. '0 and 4.90' treats iron as Fe²⁺. 3.87 BM "
                       "(3 unpaired) has no basis for a d⁵ ion.",
      seconds=60, verified_by=RECOMPUTED),

    Q(T_CC, "Isomerism", "Advanced", "numerical",
      "The total number of stereoisomers (geometrical and optical together) of the octahedral ion "
      "[Co(en)(NH₃)₂Cl₂]⁺ is:",
      ["3", "2", "5", "4"], "D",
      "Stereoisomers of an [M(AA)a₂b₂] complex",
      "The en ligand must span two cis positions. Then place the two NH₃ and the two Cl ligands in the four "
      "remaining positions and look for mirror symmetry.",
      ["Isomer 1: two Cl trans to each other (NH₃ cis) → has a mirror plane → 1 isomer",
       "Isomer 2: two NH₃ trans to each other (Cl cis) → has a mirror plane → 1 isomer",
       "Isomer 3: both Cl cis and both NH₃ cis (each trans to an en N) → no mirror plane → a pair of enantiomers",
       "Total = 1 + 1 + 2 = 4 (3 geometrical isomers, one of them chiral)"],
      why_others_wrong="3 counts only the geometrical isomers. 2 treats the ion like [MA₄B₂] (cis/trans only). 5 "
                       "wrongly makes a second geometrical isomer chiral.",
      seconds=120, verified_by=RECOMPUTED),

    Q(T_CC, "Crystal field theory", "Advanced", "statement_pair",
      *sp("In a tetrahedral crystal field, the e orbitals lie higher in energy than the t₂ orbitals.", False,
          "Since Δt is only about (4/9)Δo, low-spin tetrahedral complexes are common.", False),
      "Crystal field splitting in tetrahedral complexes",
      "In a tetrahedral field the splitting is inverted relative to the octahedral case: the t₂ set is higher and "
      "the e set lower. Δt ≈ (4/9)Δo is too small to force pairing, so low-spin tetrahedral complexes are rarely "
      "observed.",
      ["Statement I: in a tetrahedral field t₂ is above e → false",
       "Statement II: Δt ≈ (4/9)Δo is true, but the conclusion is the opposite: tetrahedral complexes are almost "
       "always high spin → false"],
      why_others_wrong="Statement II starts with a true fact and draws a false conclusion; reading only its first "
                       "half leads to option D.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in tetrahedral coordination entities",
      seconds=50),
]


# ================================================================ Purification and Characterisation (158-163)
# 159: Carius: 0.287 g AgCl from 0.20 g compound
pct_cl = F(287, 1000) * M_CL / M_AGCL / F(2, 10) * 100
assert pct_cl == F(355, 10) and 2 * pct_cl == 71
assert round(float(F(287, 1000) * M_CL / M_AG / F(2, 10) * 100), 1) == 47.2 and round(float(pct_cl / 2), 1) == 17.8
# 160: Dumas: 44.8 mL N2 at STP from 0.28 g
pct_n = F(448, 10) / 22400 * 28 / F(28, 100) * 100
assert pct_n == 20 and F(448, 10) / 22400 * 14 / F(28, 100) * 100 == 10
assert F(448, 10) / 224000 * 28 / F(28, 100) * 100 == 2
# 162: Kjeldahl: 1.0 g; 50 mL 0.5 M H2SO4 (50 mmol H+); back titre 60 mL 0.5 M NaOH (30 mmol)
mmol_nh3 = 50 * F(1, 2) * 2 - 60 * F(1, 2)
pct_kj = mmol_nh3 * 14 / 1000 / 1 * 100
assert mmol_nh3 == 20 and pct_kj == 28
assert [F(n * 14, 1000) * 100 for n in (50, 30, 10)] == [70, 42, 14]  # distractors

QUESTIONS += [
    Q(T_PU, "Purification methods", "Basic", "direct",
      "Glycerol decomposes at or below its normal boiling point. In industry it is recovered from spent-lye by:",
      ["Steam distillation", "Sublimation", "Distillation under reduced pressure", "Fractional crystallisation"],
      "C",
      "Distillation under reduced pressure",
      "A liquid boils when its vapour pressure equals the external pressure. Lowering the pressure lowers the "
      "boiling point, so a liquid that decomposes at its normal boiling point can be distilled without "
      "decomposing.",
      ["Glycerol has a high boiling point and decomposes near it",
       "Reducing the pressure lets it boil at a much lower temperature",
       "This is how glycerol is separated from spent-lye in the soap industry"],
      why_others_wrong="Steam distillation needs a steam-volatile liquid immiscible with water (glycerol mixes with "
                       "water). Sublimation and crystallisation are for solids.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', methods of purification", seconds=30),

    Q(T_PU, "Quantitative analysis and formulae", "Basic", "numerical",
      "In a Carius determination, 0.20 g of an organic compound gave 0.287 g of AgCl. The percentage of chlorine "
      "in the compound is (Ag = 108, Cl = 35.5):",
      ["71.0%", "47.2%", "17.8%", "35.5%"], "D",
      "Carius method for halogens",
      "All the chlorine of the compound ends up in AgCl. The fraction of chlorine in AgCl is 35.5/143.5.",
      ["Mass of Cl = 0.287 × 35.5/143.5 = 0.071 g",
       "% Cl = 0.071/0.20 × 100 = 35.5%"],
      why_others_wrong="71.0% uses 71 (Cl₂) per mole of AgCl. 47.2% divides by the atomic mass of Ag (108) instead "
                       "of the molar mass of AgCl. 17.8% halves the correct value.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis (halogens)",
      seconds=45, verified_by=RECOMPUTED),

    Q(T_PU, "Quantitative analysis and formulae", "Intermediate", "numerical",
      "In Dumas' method, 0.28 g of an organic compound gave 44.8 mL of nitrogen, measured at STP. The percentage of "
      "nitrogen in the compound is (molar volume at STP = 22400 mL):",
      ["20%", "10%", "40%", "2.0%"], "A",
      "Dumas method for nitrogen",
      "Nitrogen of the compound is collected as N₂ gas. Convert its volume at STP to mass using 28 g of N₂ per "
      "22400 mL.",
      ["Mass of N₂ = 28 × 44.8/22400 = 0.056 g",
       "% N = 0.056/0.28 × 100 = 20%"],
      shortcut="% N = (28 × V × 100)/(22400 × m) = (28 × 44.8 × 100)/(22400 × 0.28) = 20.",
      why_others_wrong="10% uses 14 instead of 28 for a mole of N₂. 40% counts each mole of N₂ twice. 2.0% uses "
                       "224000 mL for the molar volume (a power-of-ten slip).",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis (nitrogen)",
      seconds=60, verified_by=RECOMPUTED),

    Q(T_PU, "Qualitative analysis", "Intermediate", "multi_statement",
      *ms("Which of the following statements about Lassaigne's test (sodium fusion extract) are correct?",
          [("Nitrogen is indicated by a Prussian blue colour when the extract is boiled with FeSO₄ and then "
            "acidified with concentrated H₂SO₄.", True),
           ("When both nitrogen and sulphur are present, sodium thiocyanate forms and gives a blood-red colour with "
            "Fe³⁺ ions.", True),
           ("During sodium fusion, the nitrogen of the compound is converted into sodium nitrite.", False),
           ("Before the AgNO₃ test for halogens, the extract is boiled with dilute HNO₃ to convert halide ions into "
            "free halogens.", False),
           ("Sulphur is indicated by a violet colour with sodium nitroprusside.", True)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
      "Detection of N, S and halogens by sodium fusion",
      "Fusion with sodium converts covalent N, S and X into NaCN, Na₂S and NaX, which are then tested as ions.",
      ["(a) NaCN + FeSO₄ → ferrocyanide; with Fe³⁺ in acid → Prussian blue → true",
       "(b) N and S together → NaSCN → [Fe(SCN)]²⁺ blood red → true",
       "(c) Nitrogen becomes NaCN, not NaNO₂ → false",
       "(d) HNO₃ is used to decompose NaCN and Na₂S (which would interfere with AgNO₃), not to make free halogen → "
       "false",
       "(e) S²⁻ + sodium nitroprusside → violet colour → true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis", seconds=80),

    Q(T_PU, "Quantitative analysis and formulae", "Advanced", "numerical",
      "In a Kjeldahl estimation, the ammonia evolved from 1.0 g of an organic compound was absorbed in 50 mL of "
      "0.5 M H₂SO₄. The remaining acid needed 60 mL of 0.5 M NaOH for neutralisation. The percentage of nitrogen in "
      "the compound is:",
      ["70%", "28%", "42%", "14%"], "B",
      "Kjeldahl method with back titration",
      "The ammonia uses up part of the acid; the rest is found by titration with NaOH. H₂SO₄ is dibasic, so count "
      "millimoles of H⁺.",
      ["H⁺ taken = 50 × 0.5 × 2 = 50 mmol",
       "H⁺ left (= NaOH used) = 60 × 0.5 = 30 mmol",
       "H⁺ used by NH₃ = 50 − 30 = 20 mmol → NH₃ = 20 mmol → N = 20 mmol = 0.28 g",
       "% N = 0.28/1.0 × 100 = 28%"],
      why_others_wrong="70% assumes all the acid reacted with NH₃ (ignores the back titration). 42% takes the NaOH "
                       "used as the NH₃. 14% treats H₂SO₄ as monobasic when finding the acid used.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', Kjeldahl's method", seconds=120,
      verified_by=RECOMPUTED),

    Q(T_PU, "Purification methods", "Advanced", "assertion_reason",
      *ar("In thin layer chromatography, the component that is adsorbed more strongly on the stationary phase has "
          "the higher Rf value.", False,
          "Rf = (distance moved by the substance from the base line) / (distance moved by the solvent from the base "
          "line).", True),
      "Retardation factor in adsorption chromatography",
      "A strongly adsorbed component is held back by the stationary phase and moves a shorter distance, so its Rf is "
      "smaller. R correctly defines Rf.",
      ["Strong adsorption → short distance moved → low Rf → A is false",
       "R is the definition of Rf → true"],
      why_others_wrong="Option A or B would need A to be true; the trap is reversing the link between adsorption and "
                       "distance moved.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', chromatography", seconds=45),
]

# ================================================================ Some Basic Principles of Organic Chemistry (164-180)
# 165: buta-1,3-diene CH2=CH-CH=CH2: 6 C-H, one C-C, two C=C (each 1 sigma + 1 pi)
bonds = {"C-H": 6, "C-C": 1, "C=C": 2}
sigma, pi = bonds["C-H"] + bonds["C-C"] + bonds["C=C"], bonds["C=C"]
assert (sigma, pi) == (9, 2)
# 169: C4H10O structural isomers
C4H10O = ["butan-1-ol", "butan-2-ol", "2-methylpropan-1-ol", "2-methylpropan-2-ol",
          "1-methoxypropane", "2-methoxypropane", "ethoxyethane"]
assert len(set(C4H10O)) == 7 and sum(n.endswith("ol") for n in C4H10O) == 4
# 174: alpha-H of 2-methylbut-2-ene (CH3)2C=CH-CH3: sp3 carbons on the double bond and their H
alpha = {"C1 (CH3 on C2)": 3, "CH3 branch on C2": 3, "C4 (CH3 on C3)": 3}
assert sum(alpha.values()) == 9 and sum(alpha.values()) + 1 == 10
# 176: butane-2,3-diol: two like stereocentres; the molecule reads the same from either end
diol = {min(cfg, cfg[::-1]) for cfg in itertools.product("RS", repeat=2)}
assert len(diol) == 3 and 2 ** 2 == 4

QUESTIONS += [
    Q(T_GO, "Hybridisation and functional groups", "Basic", "direct",
      "The hybridisation of the three carbon atoms in acrylonitrile, CH₂=CH–C≡N, taken from left to right, is:",
      ["sp², sp, sp", "sp³, sp², sp", "sp², sp², sp", "sp², sp², sp²"], "C",
      "Hybridisation from the type of bonds at each carbon",
      "A carbon with one double bond is sp²; a carbon with a triple bond is sp; a carbon with only single bonds is "
      "sp³.",
      ["CH₂= : double bond → sp²", "=CH– : double bond → sp²", "–C≡N : triple bond → sp"],
      seconds=25),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "numerical",
      "The numbers of σ and π bonds in buta-1,3-diene, CH₂=CH–CH=CH₂, are:",
      ["9σ, 2π", "6σ, 2π", "11σ, 2π", "9σ, 4π"], "A",
      "Counting σ and π bonds",
      "Every single bond is one σ bond; a double bond is one σ plus one π bond.",
      ["C–H bonds: 2 + 1 + 1 + 2 = 6 σ", "C–C single bond: 1 σ", "Two C=C: 2 σ + 2 π",
       "Total: 9 σ and 2 π"],
      why_others_wrong="6σ counts only C–H bonds. 11σ counts each double bond as two σ bonds. 4π counts each double "
                       "bond as two π bonds.",
      seconds=30, verified_by=RECOMPUTED),

    Q(T_GO, "IUPAC nomenclature", "Basic", "match_list",
      *ml("Match the compound in List-I with its IUPAC name in List-II.",
          ["(CH₃)₂CH–CH₂–CH(OH)–CH₃", "CH₃CH₂C(CH₃)₂CHO", "CH₂=CH–CH(CH₃)₂", "(CH₃)₂CH–CH₂–CO–CH₃"],
          ["3-Methylbut-1-ene", "4-Methylpentan-2-one", "2,2-Dimethylbutanal", "4-Methylpentan-2-ol"],
          {"A": "IV", "B": "III", "C": "I", "D": "II"},
          [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
           {"A": "IV", "B": "III", "C": "II", "D": "I"}], "D"),
      "IUPAC names: longest chain containing the principal group, lowest locants",
      "Choose the longest chain that contains the principal functional group (or the double bond), number it to give "
      "that group the lowest locant, then name the substituents.",
      ["A: 5-carbon chain, OH on C2, CH₃ on C4 → 4-methylpentan-2-ol → IV",
       "B: CHO carbon is C1, two CH₃ on C2, chain of 4 → 2,2-dimethylbutanal → III",
       "C: double bond from C1, CH₃ on C3, chain of 4 → 3-methylbut-1-ene → I",
       "D: C=O on C2, CH₃ on C4, chain of 5 → 4-methylpentan-2-one → II"],
      why_others_wrong="A-II with D-IV swaps the alcohol and the ketone; the -ol and -one suffixes settle these two.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of organic compounds",
      seconds=60),

    Q(T_GO, "Types of organic reactions", "Basic", "direct",
      "Which of the following can act as a nucleophile?",
      ["NO₂⁺", "(CH₃)₃C⁺", "(C₂H₅)₂NH", "AlCl₃"], "C",
      "Nucleophiles and electrophiles",
      "A nucleophile has an electron pair to donate. Neutral molecules with a lone pair on N or O, such as amines "
      "and water, are nucleophiles. Cations such as NO₂⁺ and carbocations, and electron-deficient molecules such as "
      "AlCl₃, accept electron pairs.",
      ["(C₂H₅)₂NH has a lone pair on N → nucleophile",
       "NO₂⁺ and (CH₃)₃C⁺ are electron deficient → electrophiles",
       "AlCl₃ has an incomplete octet on Al → electron-pair acceptor"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=25),

    Q(T_GO, "Types of organic reactions", "Basic", "statement_pair",
      *sp("Homolytic cleavage of a covalent bond gives carbocations.", False,
          "In heterolytic cleavage of a C–X bond, if the carbon keeps the shared pair of electrons, a carbanion is "
          "formed.", True),
      "Homolytic and heterolytic bond cleavage",
      "In homolytic cleavage each atom takes one electron of the bond, giving free radicals. In heterolytic cleavage "
      "one atom takes both electrons: carbon becomes a carbocation if it loses the pair and a carbanion if it keeps "
      "it.",
      ["Statement I: homolysis gives free radicals, not carbocations → false",
       "Statement II: carbon with the pair → negative charge → carbanion → true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fission of a covalent bond",
      seconds=30),

    Q(T_GO, "Isomerism", "Intermediate", "numerical",
      "How many structural isomers (alcohols and ethers together) have the molecular formula C₄H₁₀O?",
      ["4", "7", "6", "8"], "B",
      "Chain, position and functional isomerism",
      "C₄H₁₀O is saturated and acyclic, so it is either an alcohol or an ether. Count each class separately.",
      ["Alcohols (4): butan-1-ol, butan-2-ol, 2-methylpropan-1-ol, 2-methylpropan-2-ol",
       "Ethers (3): 1-methoxypropane, 2-methoxypropane, ethoxyethane",
       "Total = 7"],
      why_others_wrong="4 counts only the alcohols. 8 adds the two enantiomers of butan-2-ol, which are "
                       "stereoisomers, not structural isomers. 6 misses one isomer, usually 2-methoxypropane.",
      seconds=70, verified_by=RECOMPUTED),

    Q(T_GO, "Electronic effects", "Intermediate", "direct",
      "Which of the following is the strongest acid?",
      ["FCH₂COOH", "ClCH₂COOH", "BrCH₂COOH", "CH₃COOH"], "A",
      "−I effect of halogens and acid strength",
      "An electron-withdrawing group near the –COOH group spreads out the negative charge of the carboxylate ion and "
      "stabilises it. The more electronegative the halogen, the stronger its −I effect.",
      ["−I effect: F > Cl > Br; CH₃ shows +I",
       "Acid strength: FCH₂COOH > ClCH₂COOH > BrCH₂COOH > CH₃COOH"],
      why_others_wrong="CH₃ is electron-releasing and makes acetic acid the weakest. Cl and Br are less "
                       "electronegative than F.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect", seconds=30),

    Q(T_GO, "Electronic effects", "Intermediate", "assertion_reason",
      *ar("The electromeric effect is a temporary effect.", True,
          "The inductive effect is transmitted through σ bonds and dies down quickly as the number of intervening "
          "bonds increases.", True, explains=False),
      "Electromeric versus inductive effect",
      "The electromeric effect is the complete transfer of a π-electron pair of a multiple bond to one atom, which "
      "happens only when an attacking reagent is present and is undone when it is removed. R is a correct statement "
      "about a different effect (the inductive effect), so it cannot explain A.",
      ["A: the electromeric effect operates only in the presence of a reagent → temporary → true",
       "R: the inductive effect weakens rapidly along a chain → true",
       "R describes the inductive effect, not why the electromeric effect is temporary → B"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', electronic displacements",
      seconds=45),

    Q(T_GO, "Isomerism", "Intermediate", "match_list",
      *ml("Match the pair of compounds in List-I with the type of isomerism they show in List-II.",
          ["Butan-1-ol and butan-2-ol", "Ethoxyethane and 1-methoxypropane", "Propanal and propanone",
           "Pentane and 2,2-dimethylpropane"],
          ["Chain isomerism", "Position isomerism", "Functional group isomerism", "Metamerism"],
          {"A": "II", "B": "IV", "C": "III", "D": "I"},
          [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
           {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
      "Types of structural isomerism",
      "Ask what differs: the skeleton (chain), the position of a group on the same skeleton (position), the "
      "functional group (functional), or the alkyl groups on either side of the same functional group (metamerism).",
      ["A: OH on C1 versus C2 of the same chain → position → II",
       "B: both ethers; C₂H₅/C₂H₅ versus CH₃/C₃H₇ around O → metamerism → IV",
       "C: aldehyde versus ketone → functional group → III",
       "D: straight versus branched chain → chain → I"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=50),

    Q(T_GO, "Reactive intermediates", "Intermediate", "multi_statement",
      *ms("Which of the following statements about reactive intermediates are correct?",
          [("A carbanion is an electron-deficient species.", False),
           ("The positively charged carbon of a carbocation is sp² hybridised and has a vacant p orbital.", True),
           ("Carbocations act as nucleophiles.", False),
           ("Carbocation stability follows the order 3° > 2° > 1° > CH₃⁺.", True),
           ("In a carbanion such as CH₃⁻, the carbon is sp³ hybridised and the ion is pyramidal.", True)],
          [["b", "c", "d"], ["a", "b", "e"], ["c", "d", "e"]], "A"),
      "Structure and stability of carbocations and carbanions",
      "A carbocation has six electrons around the charged carbon (electron deficient, planar, sp²). A carbanion has "
      "eight electrons including a lone pair (electron rich, sp³, pyramidal).",
      ["(a) A carbanion carries an extra electron pair → electron rich → false",
       "(b) Carbocation: three σ bonds in a plane, empty p orbital → true",
       "(c) Carbocations accept electron pairs → electrophiles → false",
       "(d) Alkyl groups stabilise the positive charge by +I effect and hyperconjugation → true",
       "(e) CH₃⁻: three bond pairs + one lone pair on sp³ carbon → pyramidal → true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', reactive intermediates",
      seconds=70),

    Q(T_GO, "Electronic effects", "Intermediate", "numerical",
      "How many hydrogen atoms in 2-methylbut-2-ene, (CH₃)₂C=CH–CH₃, can take part in hyperconjugation with the "
      "double bond?",
      ["10", "6", "9", "3"], "C",
      "Hyperconjugation needs C–H bonds on the carbon next to the double bond (α-hydrogens)",
      "Only C–H bonds on sp³ carbons directly attached to the C=C can overlap with its π system. The H on the "
      "double-bond carbon itself (vinylic H) does not count.",
      ["sp³ carbons attached to C=C: two CH₃ groups on C2 and one CH₃ on C3",
       "α-H = 3 + 3 + 3 = 9",
       "The vinylic H on C3 is excluded"],
      why_others_wrong="10 includes the vinylic hydrogen. 6 counts only the two methyl groups on C2. 3 counts only "
                       "one methyl group.",
      seconds=50, verified_by=RECOMPUTED),

    Q(T_GO, "Types of organic reactions", "Intermediate", "direct",
      "In which of the following reactions does a carbon atom that is sp² hybridised in the organic reactant "
      "become sp³ hybridised in the product?",
      ["Reaction of CH₃Br with aqueous KOH to give CH₃OH",
       "Addition of HCN to CH₃CHO to give a cyanohydrin",
       "Reaction of CH₃CH₂Br with alcoholic KOH to give CH₂=CH₂",
       "Nitration of benzene to give nitrobenzene"], "B",
      "Change of hybridisation in addition, substitution and elimination",
      "Addition to a C=O or C=C bond turns an sp² carbon into an sp³ carbon. Substitution keeps the hybridisation; "
      "elimination turns sp³ into sp².",
      ["CH₃CHO + HCN → CH₃CH(OH)CN: carbonyl carbon sp² → sp³ ✓",
       "CH₃Br → CH₃OH: sp³ → sp³ (substitution)",
       "CH₃CH₂Br → CH₂=CH₂: sp³ → sp² (elimination)",
       "C₆H₆ → C₆H₅NO₂: ring carbons are sp² before and after (substitution)"],
      why_others_wrong="Elimination is the reverse change (sp³ → sp²); nitration passes through an sp³ intermediate "
                       "but the product carbon is sp² again.",
      seconds=50),

    Q(T_GO, "Isomerism", "Advanced", "numerical",
      "The total number of stereoisomers of butane-2,3-diol, CH₃–CH(OH)–CH(OH)–CH₃, is:",
      ["4", "2", "1", "3"], "D",
      "Stereoisomers when two chiral centres are identically substituted",
      "With n chiral centres the maximum is 2ⁿ. When the two centres carry the same four groups, the (R,S) form has "
      "a plane of symmetry and is identical to its mirror image (meso), so one isomer is lost.",
      ["C2 and C3 are both chiral (H, OH, CH₃, CH(OH)CH₃)",
       "Combinations: (R,R), (S,S), (R,S), (S,R)",
       "(R,R) and (S,S) are enantiomers; (R,S) = (S,R) is the meso form",
       "Total = 3"],
      why_others_wrong="4 applies 2ⁿ without checking for a meso form. 2 counts only the optically active pair.",
      seconds=75, verified_by=RECOMPUTED),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₂=CH–CH(CH₃)–CH₂–COOH is:",
      ["3-Methylpent-1-en-5-oic acid", "3-Methylpent-4-enoic acid", "2-Methylpent-4-enoic acid",
       "3-Methylhex-5-enoic acid"], "B",
      "Numbering from the principal functional group",
      "–COOH has priority over C=C, so its carbon is C1 even though this gives the double bond a higher locant.",
      ["Principal chain: 5 carbons including the COOH carbon → pentenoic acid",
       "C1 = COOH, C2 = CH₂, C3 = CH(CH₃), C4=C5 double bond",
       "Name: 3-methylpent-4-enoic acid"],
      why_others_wrong="'pent-1-en-5-oic acid' numbers from the double bond, giving the principal group a higher "
                       "locant. '2-methyl' puts the methyl on the wrong carbon. 'hex' counts six chain carbons.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of compounds with "
            "functional groups", seconds=50),

    Q(T_GO, "Electronic effects", "Advanced", "assertion_reason",
      *ar("The –NO₂ group withdraws electron density from the benzene ring, and the ortho and para positions become "
          "the most electron-deficient.", True,
          "The –NO₂ group shows a +I effect.", False),
      "−R (−M) effect of the nitro group",
      "The nitro group withdraws electrons by the −I effect and, more strongly, by the −R effect. The resonance "
      "structures place positive charge at the ortho and para positions, so these are the most electron-deficient.",
      ["A: resonance structures of nitrobenzene show δ+ at ortho and para → true",
       "R: –NO₂ is electron-withdrawing, i.e. −I, not +I → false"],
      why_others_wrong="A student who remembers only that −NO₂ affects ortho/para may accept R; a +I group would "
                       "release electrons, the opposite of A.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', resonance effect", seconds=50),

    Q(T_GO, "Electronic effects", "Advanced", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("The canonical (resonance) structures of a molecule can be isolated separately.", False),
           ("Resonance structures differ only in the positions of electrons, not in the positions of atomic "
            "nuclei.", True),
           ("The –OH group attached to a benzene ring shows a +R effect.", True),
           ("The resonance hybrid has a lower energy than any of the contributing structures.", True),
           ("Hyperconjugation involves delocalisation of σ electrons of a C–H bond of an alkyl group attached to an "
            "unsaturated system or to an atom with an unshared p orbital.", True)],
          [["a", "b", "c", "d"], ["b", "c", "d"], ["a", "c", "d", "e"]], "C"),
      "Resonance and hyperconjugation",
      "Canonical structures are imaginary limiting forms; only the hybrid exists. Lone pairs on O, N or a halogen "
      "attached to a ring are donated into it (+R).",
      ["(a) Only the hybrid exists; canonical structures cannot be isolated → false",
       "(b) Nuclei stay fixed; only electrons are moved → true",
       "(c) A lone pair of O is delocalised into the ring → +R → true",
       "(d) The hybrid is more stable (lower in energy) than any one structure → true",
       "(e) This is the definition of hyperconjugation (σ–π conjugation) → true"],
      seconds=90),

    Q(T_GO, "Hybridisation and functional groups", "Advanced", "statement_pair",
      *sp("Pent-1-en-4-yne, HC≡C–CH₂–CH=CH₂, contains three sp²-hybridised carbon atoms.", False,
          "An sp hybrid orbital has 50% s character, so an sp-hybridised carbon is more electronegative than an sp² "
          "or sp³ carbon.", True),
      "Hybridisation and s character",
      "Assign each carbon from its bonds, then use the link between s character and electronegativity.",
      ["HC≡ (C5) and ≡C– (C4): sp, sp", "–CH₂– (C3): sp³", "–CH= (C2) and =CH₂ (C1): sp², sp²",
       "Only two sp² carbons → Statement I false",
       "s character: sp 50% > sp² 33% > sp³ 25%; greater s character → greater electronegativity → Statement II "
       "true"],
      why_others_wrong="Counting the CH₂ carbon next to the double bond as sp² gives three, the error Statement I "
                       "invites.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation", seconds=50),
]


# ================================================================ Hydrocarbons (181-194)
# 183: C3H8 + 5O2 -> 3CO2 + 4H2O; volumes in the mole ratio at the same T and P
o2_per_l = 3 + F(8, 4)
assert o2_per_l == 5 and 2 * o2_per_l == 10 and 2 * F(7, 2) == 7 and 2 * 3 == 6
# 186: open-chain C5H10 alkenes; True = shows cis/trans isomerism
C5H10 = {"pent-1-ene": False, "pent-2-ene": True, "2-methylbut-1-ene": False, "3-methylbut-1-ene": False,
         "2-methylbut-2-ene": False}
assert len(C5H10) == 5 and len(C5H10) + sum(C5H10.values()) == 6
# 191: C6H12 alkene giving a single ozonolysis product: (CH3)2C=C(CH3)2 -> 2 acetone, or hex-3-ene -> 2 propanal
M_C6H12, M_C3H6O = 84, 58
mass_191 = F(84, 10) / M_C6H12 * 2 * M_C3H6O
assert mass_191 == F(116, 10) and F(84, 10) / M_C6H12 * M_C3H6O == F(58, 10) and F(2, 10) * 44 == F(88, 10)
# 192: monochlorination of 2-methylbutane CH3-CH(CH3)-CH2-CH3: sets of equivalent H
h_sets = ["C1 and branch CH3 (6 H)", "C2 (1 H)", "C3 (2 H)", "C4 (3 H)"]
assert len(h_sets) == 4

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "Which statement about the conformations of ethane is correct?",
      ["The staggered conformation has the least repulsion between C–H bond pairs and is more stable than the "
       "eclipsed form.",
       "The eclipsed conformation is more stable because its C–H bonds are closest together.",
       "The staggered and eclipsed forms can be separated and stored at room temperature.",
       "In the staggered conformation, the dihedral angle between C–H bonds on adjacent carbons is 0°."], "A",
      "Conformations of ethane and torsional strain",
      "Rotation about the C–C σ bond gives conformations. In the eclipsed form the C–H bonds of the two carbons "
      "are directly behind each other and repel most; in the staggered form they are farthest apart.",
      ["Staggered: dihedral angle 60°, minimum repulsion → most stable",
       "Eclipsed: dihedral angle 0°, maximum repulsion (torsional strain)",
       "The energy barrier is only about 12.5 kJ mol⁻¹, so the forms interconvert rapidly and cannot be "
       "isolated"],
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane", seconds=30),

    Q(T_HC, "Benzene and aromaticity", "Basic", "direct",
      "Which of the following is NOT a condition for a compound to be aromatic according to Hückel's rule?",
      ["Planarity of the ring", "Complete delocalisation of the π electrons in the ring",
       "Presence of (4n + 2) π electrons in the ring", "Presence of at least one heteroatom in the ring"], "D",
      "Hückel's rule for aromaticity",
      "A compound is aromatic if it is planar, its π electrons are completely delocalised round the ring, and the "
      "ring holds (4n + 2) π electrons (n = 0, 1, 2 …). Nothing requires a heteroatom; benzene has none.",
      ["Benzene: planar, 6 π electrons (n = 1) delocalised, no heteroatom → aromatic",
       "So a heteroatom is not a requirement"],
      ncert=f"{NC11}, 'Hydrocarbons', aromaticity", seconds=25),

    Q(T_HC, "Alkanes and conformations", "Basic", "numerical",
      "The volume of oxygen needed for the complete combustion of 2 L of propane, both gases measured at the same "
      "temperature and pressure, is:",
      ["10 L", "5 L", "7 L", "6 L"], "A",
      "Combustion of alkanes and Gay-Lussac's law of gaseous volumes",
      "Balance the combustion equation; at the same T and P, volumes of gases are in the ratio of their moles.",
      ["C₃H₈ + 5O₂ → 3CO₂ + 4H₂O", "1 L propane needs 5 L O₂", "2 L propane needs 10 L O₂"],
      why_others_wrong="5 L is for 1 L of propane. 7 L uses the ratio for ethane (3.5 per litre). 6 L burns only "
                       "the carbon to CO₂ and forgets the hydrogen.",
      seconds=35, verified_by=RECOMPUTED),

    Q(T_HC, "Alkynes", "Basic", "statement_pair",
      *sp("Ethyne reacts with sodium metal to form sodium acetylide and hydrogen gas.", True,
          "The hydrogen atoms of ethene are more acidic than those of ethyne.", False),
      "Acidic character of alkynes",
      "A hydrogen on a triply bonded carbon is attached to an sp carbon (50% s character). That carbon holds the "
      "bonding pair closer, so the H is released as H⁺ more easily than from sp² (ethene) or sp³ (ethane) carbons.",
      ["Statement I: HC≡CH + Na → HC≡C⁻Na⁺ + ½H₂ → true",
       "Statement II: acidity order is ethyne > ethene > ethane → false"],
      ncert=f"{NC11}, 'Hydrocarbons', acidic character of alkynes", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "direct",
      "Ozonolysis of 2-methylbut-2-ene followed by treatment with zinc and water gives:",
      ["Butanone and methanal", "Propanone and ethanal", "Two molecules of propanal", "2-Methylpropanal and methanal"],
      "B",
      "Ozonolysis cleaves the C=C bond into two C=O groups",
      "Cut the double bond and put =O on each carbon that was part of it.",
      ["(CH₃)₂C=CH–CH₃", "(CH₃)₂C= → (CH₃)₂C=O, propanone", "=CH–CH₃ → CH₃CHO, ethanal"],
      why_others_wrong="Butanone + methanal comes from 2-methylbut-1-ene. Two propanal come from hex-3-ene. "
                       "2-Methylpropanal + methanal comes from 3-methylbut-1-ene.",
      ncert=f"{NC11}, 'Hydrocarbons', ozonolysis of alkenes", seconds=45),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "numerical",
      "How many open-chain alkenes have the molecular formula C₅H₁₀, counting geometrical (cis/trans) isomers "
      "separately?",
      ["6", "5", "4", "7"], "A",
      "Structural and geometrical isomerism in alkenes",
      "List the structural isomers first; then check which have two different groups on each double-bond carbon.",
      ["Straight chain: pent-1-ene, pent-2-ene",
       "Branched: 2-methylbut-1-ene, 3-methylbut-1-ene, 2-methylbut-2-ene → 5 structural isomers",
       "Only pent-2-ene has two different groups on both sp² carbons → cis and trans",
       "Total = 5 + 1 = 6"],
      why_others_wrong="5 ignores geometrical isomerism. 7 wrongly gives 2-methylbut-2-ene cis/trans forms, but one "
                       "of its double-bond carbons carries two CH₃ groups.",
      seconds=75, verified_by=RECOMPUTED),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "assertion_reason",
      *ar("Benzene readily undergoes addition reactions like alkenes.", False,
          "Benzene is stabilised by the delocalisation of its six π electrons (resonance).", True),
      "Stability of benzene",
      "Because the π electrons are delocalised, benzene is unusually stable. It prefers electrophilic substitution, "
      "which keeps the aromatic ring, to addition, which would destroy it. Addition happens only under drastic "
      "conditions.",
      ["A: benzene does not decolourise bromine water or react like an alkene → false",
       "R: resonance (delocalisation) stabilises benzene → true"],
      ncert=f"{NC11}, 'Hydrocarbons', structure of benzene and resonance", seconds=35),

    Q(T_HC, "Alkynes", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with its main organic product in List-II.",
          ["Propyne + H₂O (Hg²⁺, dilute H₂SO₄, 333 K)",
           "Ethyne + H₂ (Pd on charcoal partly deactivated with quinoline)",
           "Ethene + Br₂ (in CCl₄)", "Ethyne passed through a red-hot iron tube at 873 K"],
          ["Benzene", "Propanone", "1,2-Dibromoethane", "Ethene"],
          {"A": "II", "B": "IV", "C": "III", "D": "I"},
          [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "I", "B": "IV", "C": "III", "D": "II"},
           {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
      "Reactions of alkenes and alkynes",
      "Identify each reaction: hydration of an alkyne (Markovnikov), partial hydrogenation, halogen addition and "
      "cyclic polymerisation.",
      ["A: CH₃C≡CH + H₂O → enol → CH₃COCH₃ (propanone) → II",
       "B: Lindlar-type catalyst stops reduction at the alkene → CH₂=CH₂ → IV",
       "C: Br₂ adds across C=C → BrCH₂CH₂Br → III",
       "D: three ethyne molecules cyclise → benzene → I"],
      why_others_wrong="A gives propanone, not propanal, because H₂O adds by Markovnikov's rule; full hydrogenation "
                       "to ethane would need an active catalyst.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: chemical properties", seconds=60),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the preparation and properties of alkanes are correct?",
          [("Heating sodium propanoate with soda lime gives ethane.", True),
           ("Alkenes add hydrogen in the presence of finely divided Pt, Pd or Ni to give alkanes.", True),
           ("2,2-Dimethylpropane (neopentane) has a higher boiling point than n-pentane.", False),
           ("Alkyl halides (other than fluorides) are reduced by zinc and dilute HCl to alkanes.", True),
           ("Chlorination of methane in diffused sunlight gives only chloromethane.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
      "Preparation and properties of alkanes",
      "Recall the standard methods (decarboxylation, hydrogenation, reduction of alkyl halides) and the effect of "
      "branching on boiling point.",
      ["(a) Decarboxylation removes one carbon: C₂H₅COONa + NaOH → C₂H₆ + Na₂CO₃ → true",
       "(b) Catalytic hydrogenation of alkenes → alkanes → true",
       "(c) Branching makes the molecule more compact (smaller surface area), lowering the boiling point → false",
       "(d) R–X + H₂ (Zn, H⁺) → R–H → true",
       "(e) Free-radical chlorination continues to CH₂Cl₂, CHCl₃ and CCl₄ → mixture → false"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: preparation and properties", seconds=80),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "direct",
      "Which substituent on a benzene ring deactivates the ring towards electrophilic substitution and yet directs "
      "the incoming group to the ortho and para positions?",
      ["–Cl", "–CH₃", "–NO₂", "–OCH₃"], "A",
      "Directive influence of substituents",
      "Halogens withdraw electrons strongly by the −I effect, which deactivates the ring. Their lone pairs donate "
      "by the +R effect, which builds up electron density at the ortho and para positions, so attack goes there.",
      ["–Cl: −I > +R → deactivating; +R decides orientation → o/p directing",
       "–CH₃ and –OCH₃: activating, o/p directing",
       "–NO₂: deactivating, meta directing"],
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=35),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "numerical",
      "An open-chain alkene of formula C₆H₁₂ gives only one carbonyl compound on ozonolysis (O₃, then Zn/H₂O). The "
      "mass of this carbonyl compound obtained from 8.4 g of the alkene, assuming complete reaction, is "
      "(C = 12, H = 1, O = 16):",
      ["5.8 g", "11.6 g", "8.8 g", "8.4 g"], "B",
      "Ozonolysis of a symmetrical alkene",
      "A single product means the double bond sits in the middle of a symmetrical molecule, so each molecule of "
      "alkene gives two identical C₃ carbonyl molecules. The two possible alkenes, 2,3-dimethylbut-2-ene "
      "(→ propanone) and hex-3-ene (→ propanal), both give a product of molar mass 58 g mol⁻¹.",
      ["Moles of alkene = 8.4/84 = 0.1 mol",
       "Each mole gives 2 mol of C₃H₆O (M = 58)",
       "Mass = 0.2 × 58 = 11.6 g"],
      why_others_wrong="5.8 g forgets that each alkene gives two carbonyl molecules. 8.8 g takes the product to be "
                       "ethanal (M = 44). 8.4 g assumes the mass stays the same.",
      seconds=110, verified_by=RECOMPUTED),

    Q(T_HC, "Alkanes and conformations", "Advanced", "numerical",
      "How many structurally different monochloro products can be formed by free-radical chlorination of "
      "2-methylbutane?",
      ["3", "5", "4", "6"], "C",
      "Equivalent hydrogens decide the number of monosubstitution products",
      "Each set of equivalent hydrogens gives one monochloro product. In CH₃–CH(CH₃)–CH₂–CH₃, the two methyl "
      "groups on C2 are equivalent.",
      ["C1 and the methyl branch (equivalent) → 1-chloro-2-methylbutane",
       "C2 → 2-chloro-2-methylbutane", "C3 → 2-chloro-3-methylbutane", "C4 → 1-chloro-3-methylbutane",
       "Total = 4 structural isomers"],
      why_others_wrong="5 treats the two methyls on C2 as different. 6 also counts the enantiomers of the two chiral "
                       "products, which the question excludes. 3 misses one set of hydrogens.",
      seconds=80, verified_by=RECOMPUTED),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "assertion_reason",
      *ar("Addition of HBr to propene in the presence of benzoyl peroxide gives 1-bromopropane as the main "
          "product.", True,
          "The peroxide effect is observed equally in the addition of HCl and HI to alkenes.", False),
      "Peroxide (Kharasch) effect",
      "With peroxide, HBr adds by a free-radical chain, giving the anti-Markovnikov product. With HCl the H–Cl bond "
      "is too strong to be split by the radicals, and with HI the iodine radicals combine to I₂ instead of adding, "
      "so no peroxide effect is seen.",
      ["A: anti-Markovnikov addition → CH₃CH₂CH₂Br → true",
       "R: the peroxide effect is seen only with HBr → false"],
      ncert=f"{NC11}, 'Hydrocarbons', anti-Markovnikov addition (peroxide effect)", seconds=45),

    Q(T_HC, "Electrophilic substitution", "Advanced", "multi_statement",
      *ms("Which of the following statements about benzene and its reactions are correct?",
          [("Nitrobenzene undergoes Friedel–Crafts alkylation easily.", False),
           ("All six C–C bonds in benzene have the same length, 139 pm.", True),
           ("Benzene reacts with Cl₂ in the presence of UV light to give chlorobenzene.", False),
           ("Friedel–Crafts alkylation of benzene with CH₃Cl needs anhydrous AlCl₃.", True),
           ("Toluene undergoes nitration faster than benzene.", True)],
          [["a", "b", "d"], ["b", "c", "e"], ["c", "d", "e"]], "A"),
      "Structure and electrophilic substitution of benzene",
      "Delocalisation makes the C–C bonds equal. Electron-withdrawing groups deactivate the ring; electron-releasing "
      "groups activate it. In UV light benzene adds chlorine instead of being substituted.",
      ["(a) –NO₂ strongly deactivates the ring; nitrobenzene does not undergo Friedel–Crafts reactions → false",
       "(b) Bond length 139 pm lies between C–C (154 pm) and C=C (133 pm) → true",
       "(c) UV light → addition → C₆H₆Cl₆ (benzene hexachloride) → false",
       "(d) AlCl₃ generates the electrophile CH₃⁺ → true",
       "(e) –CH₃ is activating (+I, hyperconjugation) → faster nitration → true"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons", seconds=85),
]

# ================================================================ Organic Compounds Containing Halogens (195-204)
# 199: C2H5Br (109) -> C2H5MgBr -> C2H6 (1:1)
vol_ethane = F(109, 10) / 109 * F(224, 10)
assert vol_ethane == F(224, 100) and vol_ethane / 2 == F(112, 100)
# 202: dehydrobromination of 2-bromobutane
alkenes_202 = ["but-1-ene", "cis-but-2-ene", "trans-but-2-ene"]
assert len(alkenes_202) == 3

QUESTIONS += [
    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "Which of the following has the longest carbon–halogen bond?",
      ["CH₃F", "CH₃I", "CH₃Cl", "CH₃Br"], "B",
      "Size of the halogen and C–X bond length",
      "Bond length increases with the size of the halogen atom: F < Cl < Br < I.",
      ["C–F < C–Cl < C–Br < C–I", "Iodine is the largest atom → C–I is the longest bond (about 214 pm)"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nature of the C–X bond", seconds=20),

    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "The reaction R–Cl + NaI → R–I + NaCl, carried out in dry acetone, is called:",
      ["Finkelstein reaction", "Swarts reaction", "Sandmeyer reaction", "Wurtz reaction"], "A",
      "Halogen exchange",
      "Alkyl iodides are made from alkyl chlorides or bromides with NaI in dry acetone. NaCl (or NaBr) is insoluble "
      "in dry acetone and precipitates, which drives the reaction forward.",
      ["Exchange of Cl/Br for I using NaI in dry acetone → Finkelstein reaction",
       "Swarts reaction makes alkyl fluorides (AgF, Hg₂F₂)"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', halogen exchange", seconds=20),

    Q(T_HX, "Polyhalogen compounds", "Basic", "statement_pair",
      *sp("DDT is readily metabolised by animals, so it does not accumulate in their fatty tissues.", False,
          "Chloroform is slowly oxidised by air in the presence of light to phosgene, so it is stored in closed, "
          "dark coloured bottles filled to the top.", True),
      "Environmental and storage aspects of polyhalogen compounds",
      "DDT is not metabolised rapidly; it is stored in fatty tissues and its concentration builds up along food "
      "chains. Chloroform forms the poisonous gas phosgene (COCl₂) in air and light, so air and light are kept out.",
      ["Statement I: DDT accumulates in fatty tissue → false",
       "Statement II: 2CHCl₃ + O₂ → 2COCl₂ + 2HCl (light) → storage in full, dark bottles → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=30),

    Q(T_HX, "SN1 and SN2", "Intermediate", "direct",
      "Which of the following alkyl bromides undergoes SN1 hydrolysis fastest?",
      ["CH₃Br", "CH₃CH₂Br", "(CH₃)₂CHBr", "(CH₃)₃CBr"], "D",
      "Carbocation stability controls the SN1 rate",
      "The slow step of SN1 is ionisation to a carbocation. The more stable the carbocation, the faster the "
      "reaction.",
      ["Carbocation stability: 3° > 2° > 1° > CH₃⁺",
       "(CH₃)₃CBr gives the tertiary (CH₃)₃C⁺ → fastest SN1"],
      why_others_wrong="CH₃Br reacts fastest by SN2, which is the opposite order; the question asks about SN1.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=30),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "numerical",
      "10.9 g of bromoethane (molar mass 109 g mol⁻¹) is converted completely into ethylmagnesium bromide, which is "
      "then treated with excess water. The volume of gas formed at STP is (molar volume = 22.4 L mol⁻¹):",
      ["2.24 L", "1.12 L", "4.48 L", "22.4 L"], "A",
      "Grignard reagents react with water to give alkanes",
      "C₂H₅Br + Mg → C₂H₅MgBr; C₂H₅MgBr + H₂O → C₂H₆ + Mg(OH)Br. One mole of bromoethane gives one mole of ethane.",
      ["Moles of C₂H₅Br = 10.9/109 = 0.1 mol", "Ethane formed = 0.1 mol",
       "Volume = 0.1 × 22.4 = 2.24 L"],
      why_others_wrong="1.12 L assumes two ethyl groups join (as in the Wurtz reaction). 4.48 L doubles the moles. "
                       "22.4 L takes one whole mole.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reaction with metals (Grignard reagents)", seconds=45,
      verified_by=RECOMPUTED),

    Q(T_HX, "SN1 and SN2", "Intermediate", "assertion_reason",
      *ar("Hydrolysis of optically active 2-bromobutane by the SN1 mechanism gives a racemic mixture.", True,
          "The carbocation intermediate is planar, so the nucleophile attacks it from either face with equal "
          "probability.", True, explains=True),
      "Stereochemistry of SN1 reactions",
      "In SN1 the C–Br bond breaks first, giving a planar sp² carbocation. Attack from the two faces gives the two "
      "enantiomers in equal amounts.",
      ["A: SN1 → racemisation → true", "R: planar carbocation, attack from both sides → true",
       "R is the reason for A"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', stereochemical aspects of nucleophilic substitution",
      seconds=40),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with its name in List-II.",
          ["2CH₃CH₂Br + 2Na (dry ether) → CH₃CH₂CH₂CH₃ + 2NaBr",
           "2C₆H₅Cl + 2Na (dry ether) → C₆H₅–C₆H₅ + 2NaCl",
           "C₆H₅Cl + CH₃Cl + 2Na (dry ether) → C₆H₅CH₃ + 2NaCl",
           "CH₃Br + AgF → CH₃F + AgBr"],
          ["Swarts reaction", "Fittig reaction", "Wurtz–Fittig reaction", "Wurtz reaction"],
          {"A": "IV", "B": "II", "C": "III", "D": "I"},
          [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
           {"A": "II", "B": "IV", "C": "III", "D": "I"}], "B"),
      "Named reactions of alkyl and aryl halides",
      "With sodium in dry ether: two alkyl halides → Wurtz; two aryl halides → Fittig; one of each → Wurtz–Fittig. "
      "Exchange with a metallic fluoride → Swarts.",
      ["A: alkyl + alkyl → Wurtz → IV", "B: aryl + aryl → Fittig → II", "C: aryl + alkyl → Wurtz–Fittig → III",
       "D: AgF → alkyl fluoride → Swarts → I"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloalkanes and haloarenes", seconds=45),

    Q(T_HX, "SN1 and SN2", "Advanced", "numerical",
      "2-Bromobutane is heated with alcoholic KOH. Counting geometrical isomers separately, how many different "
      "alkenes can be formed?",
      ["2", "1", "3", "4"], "C",
      "Dehydrohalogenation (β-elimination) and Saytzeff's rule",
      "A β-hydrogen can be removed from C1 or from C3. Removing it from C3 gives but-2-ene, which exists as cis and "
      "trans isomers.",
      ["β-H on C1 → but-1-ene", "β-H on C3 → but-2-ene → cis and trans",
       "Total = 3 alkenes (but-2-ene is the main product, by Saytzeff's rule)"],
      why_others_wrong="2 ignores cis/trans isomerism of but-2-ene. 1 gives only the Saytzeff product.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions", seconds=60, verified_by=RECOMPUTED),

    Q(T_HX, "SN1 and SN2", "Advanced", "multi_statement",
      *ms("Which of the following statements about nucleophilic substitution are correct?",
          [("An SN2 reaction proceeds with inversion of configuration.", True),
           ("The rate of an SN1 reaction depends on the concentrations of both the alkyl halide and the "
            "nucleophile.", False),
           ("Haloarenes are less reactive than haloalkanes towards nucleophilic substitution, partly because "
            "resonance gives the C–X bond partial double bond character.", True),
           ("An –NO₂ group at the ortho or para position to the halogen increases the reactivity of a haloarene "
            "towards nucleophilic substitution.", True),
           ("Allylic and benzylic halides are highly reactive towards SN1 because their carbocations are "
            "stabilised by resonance.", True)],
          [["a", "b", "c", "d"], ["c", "d", "e"], ["a", "b", "d", "e"]], "C"),
      "SN1, SN2 and the reactivity of haloarenes",
      "SN2 is one step with backside attack; SN1 has a slow ionisation step that involves only the substrate.",
      ["(a) Backside attack → Walden inversion → true",
       "(b) SN1 is first order: rate = k[R–X] → false",
       "(c) Lone pair of X delocalised into the ring → stronger, shorter C–X bond → true",
       "(d) –NO₂ at o/p stabilises the negatively charged intermediate by resonance → true",
       "(e) Allyl and benzyl cations are resonance-stabilised → fast SN1 → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution", seconds=90),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "The major organic product formed when 2-bromo-2-methylpropane is heated with sodium ethoxide in ethanol is:",
      ["2-Methylpropene", "tert-Butyl ethyl ether", "2-Methylpropan-2-ol", "2-Methylpropane"], "A",
      "Elimination versus substitution",
      "A tertiary alkyl halide is too crowded for SN2 attack. Ethoxide is a strong base, so it removes a "
      "β-hydrogen and elimination dominates.",
      ["(CH₃)₃C–Br + C₂H₅O⁻ → (CH₃)₂C=CH₂ + C₂H₅OH + Br⁻",
       "Tertiary substrate + strong base → elimination is the main pathway"],
      why_others_wrong="The ether would form by substitution, which is minor for a tertiary halide with a strong base "
                       "(Williamson synthesis uses a primary halide for this reason). The alcohol needs water as the "
                       "nucleophile. 2-Methylpropane would need reduction.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination versus substitution", seconds=45),
]


# ================================================================ Organic Compounds Containing Oxygen (205-221)
# 208: 0.6 g CH3COOH (60) with 0.1 M NaOH, 1:1
vol_208 = F(6, 10) / 60 / F(1, 10) * 1000
assert vol_208 == 100
# 210: HOCH2CH2OH (62) + 2Na -> NaOCH2CH2ONa + H2 (1 mol H2 per mol diol)
mol_diol = F(31, 10) / 62
assert mol_diol * F(224, 10) == F(112, 100) and mol_diol / 2 * F(224, 10) == F(56, 100)
assert mol_diol * 2 * F(224, 10) == F(224, 100)
# 216: RCHO + 2[Ag(NH3)2]+ -> 2Ag; 0.88 g CH3CHO (44)
mass_ag = F(88, 100) / 44 * 2 * M_AG
assert mass_ag == F(432, 100) and mass_ag / 2 == F(216, 100) and mass_ag * 2 == F(864, 100)
# 217: 0.1 mol acid + 0.1 mol ethanol -> theoretical 0.1 mol ethyl ethanoate (88)
theo = F(6, 1) / 60 * 88
yld = F(528, 100) / theo * 100
assert theo == F(88, 10) and yld == 60 and 100 - yld == 40 and F(528, 100) / (2 * theo) * 100 == 30
assert round(float(F(528, 100) / F(106, 10) * 100), 1) == 49.8
# 221: ester CnH2nO2 + NaOH (1:1); 4.4 g needs 0.05 mol NaOH
M_ester = F(44, 10) / (F(50, 1000) * 1)
n_c = (M_ester - 32) / 14
assert M_ester == 88 and n_c == 4

QUESTIONS += [
    Q(T_OX, "Alcohols", "Basic", "direct",
      "Which of the following alcohols gives turbidity immediately with Lucas reagent (concentrated HCl + anhydrous "
      "ZnCl₂) at room temperature?",
      ["Butan-1-ol", "Butan-2-ol", "2-Methylpropan-1-ol", "2-Methylpropan-2-ol"], "D",
      "Lucas test for 1°, 2° and 3° alcohols",
      "The alkyl chloride formed is insoluble and makes the solution turbid. Tertiary alcohols react at once "
      "because they form a stable tertiary carbocation; primary alcohols do not react at room temperature.",
      ["2-Methylpropan-2-ol, (CH₃)₃C–OH, is tertiary → immediate turbidity",
       "Butan-2-ol is secondary → turbidity after some minutes",
       "Butan-1-ol and 2-methylpropan-1-ol are primary → no turbidity at room temperature"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reaction with hydrogen halides", seconds=25),

    Q(T_OX, "Phenols", "Basic", "direct",
      "Phenol is heated with chloroform and aqueous NaOH, and the product is acidified. The main product is:",
      ["Salicylic acid", "Salicylaldehyde", "Benzaldehyde", "p-Hydroxybenzoic acid"], "B",
      "Reimer–Tiemann reaction",
      "With CHCl₃ and alkali, a –CHO group is introduced at the ortho position of phenol (via a –CHCl₂ "
      "intermediate). Acidification gives 2-hydroxybenzaldehyde.",
      ["C₆H₅OH + CHCl₃ + NaOH → o-substituted –CHCl₂ intermediate → hydrolysed to –CHO",
       "Acidification → salicylaldehyde (2-hydroxybenzaldehyde)"],
      why_others_wrong="Salicylic acid comes from Kolbe's reaction (sodium phenoxide + CO₂), not from chloroform.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Reimer–Tiemann reaction", seconds=25),

    Q(T_OX, "Ethers", "Basic", "direct",
      "Williamson's synthesis of ethers is the reaction of:",
      ["two molecules of an alcohol with concentrated H₂SO₄",
       "an alkene with water in the presence of acid",
       "an aldehyde with an alcohol in the presence of dry HCl",
       "an alkyl halide with a sodium alkoxide"], "D",
      "Williamson synthesis",
      "An alkoxide ion is a strong nucleophile; it displaces the halide from an alkyl halide by SN2: "
      "R–X + R′–O⁻Na⁺ → R–O–R′ + NaX. Both symmetrical and unsymmetrical ethers can be made.",
      ["Example: CH₃Br + C₂H₅ONa → CH₃–O–C₂H₅ + NaBr"],
      why_others_wrong="Heating an alcohol with concentrated H₂SO₄ is dehydration (another ether method, not "
                       "Williamson's). Alkene + water gives an alcohol; aldehyde + alcohol gives an acetal.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of ethers", seconds=20),

    Q(T_OX, "Carboxylic acids", "Basic", "numerical",
      "The volume of 0.1 M NaOH needed to neutralise 0.6 g of ethanoic acid (molar mass 60 g mol⁻¹) is:",
      ["10 mL", "100 mL", "50 mL", "200 mL"], "B",
      "Neutralisation of a monobasic acid",
      "CH₃COOH + NaOH → CH₃COONa + H₂O, a 1 : 1 reaction.",
      ["Moles of acid = 0.6/60 = 0.01 mol", "Moles of NaOH = 0.01 mol",
       "Volume = 0.01/0.1 = 0.1 L = 100 mL"],
      why_others_wrong="10 mL slips a factor of ten. 50 mL and 200 mL treat ethanoic acid as needing half or twice "
                       "the NaOH (it has only one acidic H).",
      seconds=30, verified_by=RECOMPUTED),

    Q(T_OX, "Aldehydes and ketones", "Basic", "statement_pair",
      *sp("Ketones reduce Tollens' reagent and give a silver mirror.", False,
          "In Fehling's test, the aldehyde is reduced to a primary alcohol.", False),
      "Tollens' and Fehling's tests",
      "Both tests depend on the easy oxidation of aldehydes. The aldehyde is oxidised to the carboxylate anion; "
      "Ag⁺ is reduced to silver (Tollens'), and Cu²⁺ to red-brown Cu₂O (Fehling's). Ketones are not oxidised by "
      "these mild reagents.",
      ["Statement I: ketones generally do not respond to Tollens' reagent → false",
       "Statement II: the aldehyde is oxidised (not reduced); Cu²⁺ is the species reduced → false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', oxidation (Tollens' and Fehling's tests)",
      seconds=35),

    Q(T_OX, "Alcohols", "Intermediate", "numerical",
      "3.1 g of ethane-1,2-diol (molar mass 62 g mol⁻¹) reacts completely with excess sodium. The volume of hydrogen "
      "evolved at STP is (molar volume = 22.4 L mol⁻¹):",
      ["0.56 L", "2.24 L", "1.12 L", "0.28 L"], "C",
      "Reaction of alcohols with active metals",
      "Each –OH group gives ½ H₂ with sodium. Ethane-1,2-diol has two –OH groups, so one mole of the diol gives one "
      "mole of H₂.",
      ["HOCH₂CH₂OH + 2Na → NaOCH₂CH₂ONa + H₂",
       "Moles of diol = 3.1/62 = 0.05 mol → H₂ = 0.05 mol",
       "Volume = 0.05 × 22.4 = 1.12 L"],
      why_others_wrong="0.56 L counts only one –OH group. 2.24 L gives a whole H₂ per –OH group. 0.28 L does both "
                       "halvings.",
      seconds=50, verified_by=RECOMPUTED),

    Q(T_OX, "Phenols", "Intermediate", "direct",
      "Which of the following is the strongest acid?",
      ["Ethanol", "Phenol", "p-Cresol (4-methylphenol)", "p-Nitrophenol"], "D",
      "Acidity of phenols and substituent effects",
      "Phenoxide is stabilised by resonance, so phenol is far more acidic than ethanol. An electron-withdrawing "
      "–NO₂ group at the para position delocalises the negative charge further and increases acidity; an "
      "electron-releasing –CH₃ group decreases it.",
      ["pKa: ethanol 15.9 > p-cresol 10.2 > phenol 10.0 > p-nitrophenol 7.1",
       "Lowest pKa → strongest acid → p-nitrophenol"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols", seconds=30),

    Q(T_OX, "Ethers", "Intermediate", "assertion_reason",
      *ar("Anisole (methoxybenzene) reacts with HI to give phenol and methyl iodide, not iodobenzene and methanol.",
          True,
          "The O–C(aryl) bond has partial double bond character because the aryl carbon is sp² hybridised and the "
          "oxygen lone pair is delocalised into the ring, so this bond is not cleaved.", True, explains=True),
      "Cleavage of alkyl aryl ethers by HI",
      "HI protonates the ether oxygen; I⁻ then attacks the methyl carbon (SN2). The aryl–oxygen bond is stronger, "
      "so it stays intact and phenol is formed.",
      ["A: C₆H₅OCH₃ + HI → C₆H₅OH + CH₃I → true",
       "R: the C₆H₅–O bond is stronger (sp² carbon, partial double bond) → true",
       "R is the reason the methyl–oxygen bond breaks instead → R explains A"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', cleavage of the C–O bond in ethers", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "match_list",
      *ml("Match the named reaction in List-I with its reagent in List-II.",
          ["Rosenmund reduction", "Stephen reaction", "Etard reaction", "Clemmensen reduction"],
          ["CrO₂Cl₂ in CS₂, then H₃O⁺", "Zn–Hg / concentrated HCl", "H₂, Pd–BaSO₄",
           "SnCl₂ + HCl, then H₃O⁺"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}], "A"),
      "Preparation and reduction of carbonyl compounds",
      "Three of these make aldehydes (from an acyl chloride, a nitrile and toluene); Clemmensen reduction turns a "
      "C=O group into CH₂.",
      ["Rosenmund: RCOCl + H₂ over Pd–BaSO₄ → RCHO → III",
       "Stephen: RCN + SnCl₂/HCl → imine → hydrolysis → RCHO → IV",
       "Etard: toluene + chromyl chloride → chromium complex → benzaldehyde → I",
       "Clemmensen: >C=O → >CH₂ with zinc amalgam and conc. HCl → II"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes and ketones", seconds=50),

    Q(T_OX, "Carboxylic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about carboxylic acids are correct?",
          [("Methanoic acid is a stronger acid than ethanoic acid.", True),
           ("Carboxylic acids are weaker acids than phenol.", False),
           ("Carboxylic acids boil at higher temperatures than aldehydes, ketones and even alcohols of comparable "
            "molecular mass, because of extensive hydrogen bonding.", True),
           ("The C=O group of carboxylic acids shows the usual nucleophilic addition reactions of aldehydes and "
            "ketones.", False),
           ("Carboxylic acids liberate CO₂ from sodium hydrogencarbonate solution.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["c", "d", "e"]], "C"),
      "Physical and chemical properties of carboxylic acids",
      "The carboxylate ion is stabilised by two equivalent resonance structures, which makes carboxylic acids "
      "stronger than phenol and stronger than carbonic acid. The same resonance reduces the electrophilic character "
      "of the carbonyl carbon.",
      ["(a) CH₃ (+I) destabilises the anion; HCOOH (pKa 3.75) > CH₃COOH (pKa 4.76) → true",
       "(b) Carboxylic acids (pKa about 4–5) are stronger than phenol (pKa 10) → false",
       "(c) Hydrogen-bonded dimers persist even in the vapour → high boiling points → true",
       "(d) Resonance in –COOH removes the typical aldehyde/ketone reactions of C=O → false",
       "(e) RCOOH + NaHCO₃ → RCOONa + H₂O + CO₂ (effervescence) → true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', carboxylic acids", seconds=80),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "direct",
      "Which of the following undergoes the Cannizzaro reaction with concentrated NaOH?",
      ["CH₃CHO", "CH₃CH₂CHO", "C₆H₅CHO", "CH₃COCH₃"], "C",
      "Cannizzaro reaction needs an aldehyde without α-hydrogen",
      "Aldehydes with no α-hydrogen undergo self oxidation–reduction with concentrated alkali: one molecule is "
      "reduced to an alcohol and another oxidised to a carboxylate salt. Those with α-hydrogen undergo aldol "
      "condensation instead.",
      ["C₆H₅CHO: the CHO is attached to a ring carbon with no H → no α-H → Cannizzaro",
       "2C₆H₅CHO + conc. NaOH → C₆H₅CH₂OH + C₆H₅COONa",
       "CH₃CHO, CH₃CH₂CHO and CH₃COCH₃ have α-H → aldol reactions"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Cannizzaro reaction", seconds=30),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "numerical",
      "0.88 g of ethanal (molar mass 44 g mol⁻¹) is completely oxidised by Tollens' reagent. The mass of silver "
      "deposited is (Ag = 108):",
      ["2.16 g", "8.64 g", "4.32 g", "1.08 g"], "C",
      "Stoichiometry of the silver mirror test",
      "RCHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → RCOO⁻ + 2Ag + 2H₂O + 4NH₃. Each aldehyde group gives two electrons, so it "
      "reduces two Ag⁺ ions.",
      ["Moles of ethanal = 0.88/44 = 0.02 mol", "Moles of Ag = 2 × 0.02 = 0.04 mol",
       "Mass of Ag = 0.04 × 108 = 4.32 g"],
      why_others_wrong="2.16 g assumes one Ag per aldehyde. 8.64 g assumes four. 1.08 g uses 0.01 mol of Ag.",
      seconds=45, verified_by=RECOMPUTED),

    Q(T_OX, "Carboxylic acids", "Advanced", "numerical",
      "6.0 g of ethanoic acid is heated with 4.6 g of ethanol in the presence of a little concentrated H₂SO₄, and "
      "5.28 g of ethyl ethanoate is obtained. The percentage yield of the ester is (C = 12, H = 1, O = 16):",
      ["60%", "49.8%", "40%", "30%"], "A",
      "Esterification and percentage yield",
      "CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O. Find the limiting reagent, then the theoretical mass of ester.",
      ["Ethanoic acid: 6.0/60 = 0.1 mol; ethanol: 4.6/46 = 0.1 mol (1 : 1, neither in excess)",
       "Theoretical ester = 0.1 mol × 88 g mol⁻¹ = 8.8 g",
       "Yield = 5.28/8.8 × 100 = 60%"],
      why_others_wrong="49.8% divides by the total mass of the reactants (10.6 g), forgetting the water lost. 40% is "
                       "the fraction that did not react. 30% takes 0.2 mol of ester as the theoretical amount.",
      seconds=90, verified_by=RECOMPUTED),

    Q(T_OX, "Alcohols", "Advanced", "direct",
      "The main product of heating 3-methylbutan-2-ol, (CH₃)₂CH–CH(OH)–CH₃, with concentrated H₂SO₄ is:",
      ["3-Methylbut-1-ene", "2-Methylbut-2-ene", "2-Methylbut-1-ene", "Pent-2-ene"], "B",
      "Acid-catalysed dehydration of alcohols and Saytzeff's rule",
      "Protonation and loss of water gives a secondary carbocation at C2. Loss of H⁺ from C3 gives the most "
      "substituted (most stable) alkene. A hydride shift from C3 gives a tertiary carbocation, which leads to the "
      "same alkene, so both routes agree.",
      ["(CH₃)₂CH–CH(OH)–CH₃ → (CH₃)₂CH–C⁺H–CH₃ + H₂O",
       "Loss of H⁺ from C3 → (CH₃)₂C=CH–CH₃ (trisubstituted, most stable)",
       "Loss of H⁺ from C1 → 3-methylbut-1-ene (monosubstituted, minor)"],
      why_others_wrong="3-Methylbut-1-ene is the less substituted (minor) alkene. 2-Methylbut-1-ene is disubstituted "
                       "and less stable. Pent-2-ene would need the carbon skeleton itself to change.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', dehydration of alcohols", seconds=60),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "assertion_reason",
      *ar("Benzaldehyde is less reactive than propanal towards nucleophilic addition.", True,
          "Benzaldehyde has no α-hydrogen atom.", True, explains=False),
      "Reactivity of aromatic aldehydes",
      "In benzaldehyde, the C=O group is conjugated with the ring; resonance releases electrons to the carbonyl "
      "carbon and makes it less electrophilic, so nucleophilic addition is slower. The absence of α-hydrogen is "
      "true, but it explains why benzaldehyde gives the Cannizzaro reaction and not aldol condensation, not its "
      "lower reactivity.",
      ["A: resonance with the ring lowers the δ+ on the carbonyl carbon → true",
       "R: the CHO group is attached directly to the ring → no α-H → true",
       "R does not explain A → option B"],
      why_others_wrong="Option A is the trap: R is a true fact about benzaldehyde, but not the cause of its lower "
                       "reactivity.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition reactions", seconds=50),

    Q(T_OX, "Phenols", "Advanced", "multi_statement",
      *ms("Which of the following statements about phenols are correct?",
          [("Phenol is a weaker acid than ethanol.", False),
           ("Phenol reacts with bromine water to give a white precipitate of 2,4,6-tribromophenol.", True),
           ("Sodium phenoxide heated with CO₂ under pressure, followed by acidification, gives salicylic acid.", True),
           ("p-Nitrophenol is steam volatile because of intramolecular hydrogen bonding.", False),
           ("The o- and p-nitrophenols formed by nitration of phenol with dilute HNO₃ can be separated by steam "
            "distillation.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["c", "d", "e"]], "D"),
      "Reactions and properties of phenol",
      "The –OH group strongly activates the ring. Intramolecular hydrogen bonding in o-nitrophenol makes it steam "
      "volatile; p-nitrophenol forms intermolecular hydrogen bonds and is not.",
      ["(a) Phenoxide is resonance-stabilised; phenol (pKa 10.0) is more acidic than ethanol (pKa 15.9) → false",
       "(b) Br₂(aq) → 2,4,6-tribromophenol (white ppt) → true",
       "(c) Kolbe's reaction → salicylic acid → true",
       "(d) It is o-nitrophenol that has intramolecular H-bonding and is steam volatile → false",
       "(e) o-Nitrophenol distils with steam and p-nitrophenol stays behind → true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of phenols", seconds=85),

    Q(T_OX, "Carboxylic acids", "Advanced", "numerical",
      "4.4 g of an ester of formula CₙH₂ₙO₂ needs exactly 50 mL of 1.0 M NaOH for complete saponification. The "
      "molecular formula of the ester is (C = 12, H = 1, O = 16):",
      ["C₃H₆O₂", "C₂H₄O₂", "C₅H₁₀O₂", "C₄H₈O₂"], "D",
      "Saponification equivalent of an ester",
      "One ester group reacts with one NaOH: RCOOR′ + NaOH → RCOONa + R′OH. So moles of ester = moles of NaOH.",
      ["Moles of NaOH = 0.050 L × 1.0 M = 0.05 mol = moles of ester",
       "Molar mass = 4.4/0.05 = 88 g mol⁻¹",
       "14n + 32 = 88 → n = 4 → C₄H₈O₂"],
      why_others_wrong="C₃H₆O₂ (74) and C₅H₁₀O₂ (102) are one CH₂ off; C₂H₄O₂ (60) is the formula of methyl "
                       "methanoate or ethanoic acid. None has molar mass 88.",
      seconds=75, verified_by=RECOMPUTED),
]


# ================================================================ Organic Compounds Containing Nitrogen (222-231)
# 226: Hofmann bromamide: C6H5CONH2 (121) -> C6H5NH2 (93), 1:1
mol_amide = F(242, 100) / 121
assert mol_amide * 93 == F(186, 100) and mol_amide * 107 == F(214, 100)
# 229: C6H5NH2 (93) -> C6H5N2+Cl- -> C6H5OH (94) + N2 (22400 mL per mol at STP)
mol_an = F(186, 100) / 93
assert mol_an * 94 == F(188, 100) and mol_an * 22400 == 448

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Which of the following gives a foul-smelling isocyanide when heated with chloroform and ethanolic KOH?",
      ["CH₃NH₂", "(CH₃)₂NH", "(CH₃)₃N", "C₆H₅N(CH₃)₂"], "A",
      "Carbylamine test for primary amines",
      "Only primary amines (aliphatic or aromatic) have the –NH₂ group needed to form R–N≡C. Secondary and tertiary "
      "amines do not give this test.",
      ["CH₃NH₂ + CHCl₃ + 3KOH → CH₃NC + 3KCl + 3H₂O", "(CH₃)₂NH, (CH₃)₃N and C₆H₅N(CH₃)₂ are 2° or 3° → no reaction"],
      ncert=f"{NC12}, 'Amines', carbylamine reaction", seconds=25),

    Q(T_NI, "Diazonium salts", "Basic", "direct",
      "Aniline is treated with NaNO₂ and dilute HCl at 273–278 K. The product is:",
      ["Nitrobenzene", "Phenol", "Benzenediazonium chloride", "Chlorobenzene"], "C",
      "Diazotisation",
      "Nitrous acid, formed in situ from NaNO₂ and HCl, converts a primary aromatic amine into a diazonium salt. The "
      "low temperature keeps the unstable salt from decomposing.",
      ["C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O (273–278 K)"],
      why_others_wrong="Phenol forms only if the diazonium salt solution is warmed with water.",
      ncert=f"{NC12}, 'Amines', preparation of diazonium salts", seconds=20),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("Aniline is a weaker base than ammonia.", True,
          "In aniline, the lone pair on nitrogen is delocalised into the benzene ring, so it is less available for "
          "protonation.", True),
      "Basicity of aryl amines",
      "In aniline the –NH₂ group is attached directly to the ring; its lone pair takes part in resonance with the "
      "ring. Ammonia has no such delocalisation.",
      ["pKb: aniline 9.38, ammonia 4.75 → aniline is the weaker base → Statement I true",
       "Resonance delocalises the N lone pair → Statement II true"],
      ncert=f"{NC12}, 'Amines', basic character of amines", seconds=30),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "direct",
      "The correct order of basic strength of the methyl-substituted amines and ammonia in aqueous solution is:",
      ["(CH₃)₃N > (CH₃)₂NH > CH₃NH₂ > NH₃", "(CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃",
       "CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N > NH₃", "NH₃ > CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N"], "B",
      "Basicity of amines in water: inductive effect, solvation and steric factors",
      "In water, basicity depends on the +I effect of alkyl groups and on how well the protonated amine is "
      "stabilised by hydrogen bonding with water. The tertiary ammonium ion has only one N–H for hydrogen bonding, "
      "and the three methyl groups also crowd the nitrogen.",
      ["+I effect alone would give 3° > 2° > 1°", "Solvation (hydrogen bonding) alone would give 1° > 2° > 3°",
       "Combined effect for methyl amines: (CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃"],
      why_others_wrong="3° > 2° > 1° is the gas-phase order, where solvation plays no part.",
      ncert=f"{NC12}, 'Amines', basic character of amines", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "numerical",
      "2.42 g of benzamide (molar mass 121 g mol⁻¹) is converted completely into an amine by Hofmann's bromamide "
      "degradation (Br₂ and NaOH). The mass of amine formed is (C = 12, H = 1, N = 14):",
      ["2.14 g", "0.93 g", "3.72 g", "1.86 g"], "D",
      "Hofmann bromamide degradation removes one carbon",
      "RCONH₂ + Br₂ + 4NaOH → RNH₂ + Na₂CO₃ + 2NaBr + 2H₂O. The carbonyl carbon is lost, so benzamide gives aniline, "
      "not benzylamine.",
      ["Moles of benzamide = 2.42/121 = 0.02 mol", "Product: C₆H₅NH₂ (M = 93), 1 : 1",
       "Mass = 0.02 × 93 = 1.86 g"],
      why_others_wrong="2.14 g assumes benzylamine (C₆H₅CH₂NH₂, M = 107), keeping the carbon. 0.93 g and 3.72 g "
                       "halve or double the moles.",
      ncert=f"{NC12}, 'Amines', Hofmann bromamide degradation", seconds=50, verified_by=RECOMPUTED),

    Q(T_NI, "Diazonium salts", "Intermediate", "assertion_reason",
      *ar("Arenediazonium salts are more stable than alkyldiazonium salts.", True,
          "The positive charge of the arenediazonium ion is dispersed over the benzene ring by resonance.", True,
          explains=True),
      "Stability of diazonium salts",
      "In C₆H₅–N₂⁺ the –N≡N group is conjugated with the ring, so the positive charge is delocalised. Alkyl "
      "diazonium ions have no such stabilisation and lose N₂ at once.",
      ["A: benzenediazonium chloride can be kept in cold solution; alkyldiazonium salts cannot → true",
       "R: resonance with the ring spreads the charge → true",
       "R is the reason for A"],
      ncert=f"{NC12}, 'Amines', diazonium salts", seconds=35),

    Q(T_NI, "Diazonium salts", "Intermediate", "match_list",
      *ml("Match the reagent in List-I, used with benzenediazonium chloride, with the main product in List-II.",
          ["CuCN / KCN", "KI (aqueous)", "H₂O (warm)", "HBF₄, then heat"],
          ["Iodobenzene", "Benzonitrile", "Fluorobenzene", "Phenol"],
          {"A": "II", "B": "I", "C": "IV", "D": "III"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
           {"A": "II", "B": "III", "C": "IV", "D": "I"}], "D"),
      "Replacement of the diazonium group",
      "The –N₂⁺ group leaves as N₂ gas and is replaced by the group the reagent supplies.",
      ["A: CuCN/KCN → C₆H₅CN (Sandmeyer) → II", "B: KI → C₆H₅I → I", "C: warm water → C₆H₅OH → IV",
       "D: HBF₄ → C₆H₅N₂⁺BF₄⁻, which on heating gives C₆H₅F → III"],
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts", seconds=45),

    Q(T_NI, "Diazonium salts", "Advanced", "numerical",
      "1.86 g of aniline is diazotised completely, and the diazonium salt solution is then warmed with water until "
      "the reaction is complete. The mass of phenol formed and the volume of N₂ released at STP are "
      "(C = 12, H = 1, N = 14, O = 16; molar volume at STP = 22400 mL):",
      ["0.94 g and 224 mL", "1.88 g and 224 mL", "1.88 g and 448 mL", "1.86 g and 448 mL"], "C",
      "Stoichiometry across two steps: diazotisation and hydrolysis",
      "Each mole of aniline gives one mole of diazonium salt, which gives one mole of phenol and one mole of N₂.",
      ["Moles of aniline = 1.86/93 = 0.02 mol",
       "C₆H₅N₂⁺Cl⁻ + H₂O → C₆H₅OH + N₂ + HCl",
       "Phenol = 0.02 × 94 = 1.88 g; N₂ = 0.02 × 22400 = 448 mL"],
      why_others_wrong="0.94 g and 224 mL halve both amounts. '1.88 g and 224 mL' wrongly takes one N₂ for every two "
                       "aniline molecules. '1.86 g and 448 mL' uses the molar mass of aniline for phenol.",
      seconds=80, verified_by=RECOMPUTED),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "multi_statement",
      *ms("Which of the following statements about amines are correct?",
          [("In Hinsberg's test, the product from a secondary amine dissolves in aqueous alkali.", False),
           ("Gabriel phthalimide synthesis gives primary aliphatic amines but cannot be used to prepare aromatic "
            "primary amines.", True),
           ("Tertiary amines react with benzenesulphonyl chloride to give sulphonamides.", False),
           ("Aniline does not undergo Friedel–Crafts reactions because it forms a salt with AlCl₃.", True),
           ("Direct nitration of aniline with a mixture of conc. HNO₃ and conc. H₂SO₄ gives a substantial amount of "
            "m-nitroaniline.", True)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
      "Preparation, identification and reactions of amines",
      "Hinsberg's test separates amines by whether the sulphonamide has an acidic N–H. In strong acid, aniline is "
      "protonated to the anilinium ion, which is meta directing.",
      ["(a) A secondary amine gives C₆H₅SO₂NR₂, which has no H on N → insoluble in alkali → false",
       "(b) Aryl halides do not undergo nucleophilic substitution with the phthalimide anion → true",
       "(c) Tertiary amines have no H on N → no reaction → false",
       "(d) The lone pair of N bonds to the Lewis acid AlCl₃, deactivating the ring → true",
       "(e) C₆H₅NH₃⁺ forms in the acid and directs meta → about 47% m-nitroaniline → true"],
      ncert=f"{NC12}, 'Amines', preparation and chemical reactions of amines", seconds=90),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "Which of the following is the strongest base?",
      ["Aniline", "p-Nitroaniline", "p-Toluidine (4-methylaniline)", "Benzylamine"], "D",
      "Aryl versus aralkyl amines",
      "In benzylamine, C₆H₅CH₂NH₂, the –NH₂ group is on a CH₂ carbon, not on the ring, so its lone pair is not "
      "delocalised into the ring. It behaves like an alkylamine. In all the anilines the lone pair is partly "
      "delocalised.",
      ["pKb: benzylamine 4.70 < p-toluidine 8.92 < aniline 9.38 < p-nitroaniline (about 13)",
       "Lowest pKb → strongest base → benzylamine"],
      why_others_wrong="p-Toluidine is the strongest of the anilines (the CH₃ group releases electrons), which is "
                       "the trap; benzylamine is not an aniline at all.",
      ncert=f"{NC12}, 'Amines', basic character of amines (pKb values)", seconds=45),
]

# ================================================================ Biomolecules (232-241)
# 235: tripeptides with Gly, Ala, Val each used once = 3!
assert math.factorial(3) == 6 and 3 ** 3 == 27
# 239: open-chain aldohexose CH2OH-(CHOH)4-CHO: C2-C5 are chiral
chiral_c = 4
assert 2 ** chiral_c == 16 and 2 ** 3 == 8 and 2 ** 5 == 32 and 2 ** 6 == 64

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "Which of the following is a non-reducing sugar?",
      ["Maltose", "Sucrose", "Lactose", "Glucose"], "B",
      "Reducing and non-reducing sugars",
      "A sugar reduces Fehling's or Tollens' reagent if it has a free (hemiacetal) aldehyde or ketone group. In "
      "sucrose, the glycosidic bond joins C1 of glucose to C2 of fructose, so both reducing groups are tied up.",
      ["Sucrose: α-D-glucose C1 – β-D-fructose C2 linkage → no free reducing group → non-reducing",
       "Maltose and lactose keep one free hemiacetal group → reducing", "Glucose is a reducing sugar"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "direct",
      "Which of the following vitamins is water soluble?",
      ["Vitamin A", "Vitamin D", "Vitamin C", "Vitamin K"], "C",
      "Classification of vitamins by solubility",
      "Vitamins A, D, E and K are fat soluble and are stored in the liver and adipose tissue. Vitamins of the "
      "B group and vitamin C are water soluble and must be supplied regularly in the diet.",
      ["Fat soluble: A, D, E, K", "Water soluble: B group and C → vitamin C"],
      ncert=f"{NC12}, 'Biomolecules', classification of vitamins", seconds=20),

    Q(T_BM, "Amino acids and proteins", "Basic", "statement_pair",
      *sp("In aqueous solution, an amino acid exists as a dipolar ion (zwitterion), with –COO⁻ and –NH₃⁺ groups.",
          True,
          "Except glycine, all naturally occurring α-amino acids are optically active.", True),
      "Properties of amino acids",
      "The acidic carboxyl group gives a proton to the basic amino group of the same molecule, forming a zwitterion. "
      "Glycine (R = H) has two H atoms on the α-carbon, so it has no chiral centre; all other α-amino acids do.",
      ["Statement I: H₃N⁺–CHR–COO⁻ → true", "Statement II: only glycine lacks a chiral α-carbon → true"],
      ncert=f"{NC12}, 'Biomolecules', amino acids", seconds=30),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "numerical",
      "How many different tripeptides can be formed using one molecule each of glycine, alanine and valine, so that "
      "every tripeptide contains all three amino acids?",
      ["3", "9", "27", "6"], "D",
      "Sequence of amino acids in a peptide",
      "A peptide has a direction (N-terminal to C-terminal end), so Gly-Ala-Val and Val-Ala-Gly are different "
      "tripeptides. Each different order is a different compound.",
      ["Number of orders of three different amino acids = 3! = 3 × 2 × 1 = 6",
       "Gly-Ala-Val, Gly-Val-Ala, Ala-Gly-Val, Ala-Val-Gly, Val-Gly-Ala, Val-Ala-Gly"],
      why_others_wrong="27 = 3³ allows an amino acid to be repeated, which the question excludes. 3 ignores that the "
                       "two ends of a peptide are different.",
      seconds=40, verified_by=RECOMPUTED),

    Q(T_BM, "Vitamins", "Intermediate", "match_list",
      *ml("Match the vitamin in List-I with the disease caused by its deficiency in List-II.",
          ["Vitamin A", "Vitamin B₁ (thiamine)", "Vitamin C (ascorbic acid)", "Vitamin D"],
          ["Scurvy", "Rickets", "Beriberi", "Xerophthalmia"],
          {"A": "IV", "B": "III", "C": "I", "D": "II"},
          [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
           {"A": "II", "B": "III", "C": "I", "D": "IV"}], "B"),
      "Deficiency diseases of vitamins",
      "Recall the deficiency disease of each vitamin from the table of vitamins.",
      ["Vitamin A → xerophthalmia (hardening of the cornea) and night blindness → IV",
       "Vitamin B₁ → beriberi → III", "Vitamin C → scurvy (bleeding gums) → I",
       "Vitamin D → rickets in children (osteomalacia in adults) → II"],
      ncert=f"{NC12}, 'Biomolecules', vitamins (sources and deficiency diseases)", seconds=35),

    Q(T_BM, "Carbohydrates", "Intermediate", "assertion_reason",
      *ar("Glucose gives Schiff's test and forms a hydrogensulphite addition product with NaHSO₃.", False,
          "Glucose exists mainly in a cyclic hemiacetal form, which has no free –CHO group.", True),
      "Cyclic structure of glucose",
      "The open-chain formula of glucose cannot explain why it fails some typical aldehyde tests. The C5–OH adds to "
      "the –CHO group to form a six-membered ring (a hemiacetal), and only a tiny amount of the open-chain form is "
      "present.",
      ["A: despite having an aldehyde group, glucose does not give Schiff's test or the NaHSO₃ adduct → false",
       "R: the cyclic (pyranose) hemiacetal form dominates → true"],
      ncert=f"{NC12}, 'Biomolecules', cyclic structure of glucose", seconds=40),

    Q(T_BM, "Nucleic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about nucleic acids are correct?",
          [("Thymine is one of the bases present in RNA.", False),
           ("In DNA, adenine pairs with thymine and guanine pairs with cytosine.", True),
           ("The sugar in DNA is 2-deoxy-D-ribose, while the sugar in RNA is D-ribose.", True),
           ("RNA molecules are usually double-stranded helices.", False),
           ("A nucleoside is a base joined to a sugar; a nucleotide is a nucleoside joined to a phosphate group.",
            True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "A"),
      "Composition and structure of DNA and RNA",
      "DNA contains A, G, C and T with deoxyribose and is a double helix; RNA contains A, G, C and U with ribose and "
      "is usually a single strand.",
      ["(a) RNA has uracil in place of thymine → false", "(b) Base pairing A=T and G≡C → true",
       "(c) Deoxyribose (DNA) versus ribose (RNA) → true", "(d) RNA is usually single-stranded → false",
       "(e) Base + sugar = nucleoside; nucleoside + phosphate = nucleotide → true"],
      ncert=f"{NC12}, 'Biomolecules', nucleic acids", seconds=60),

    Q(T_BM, "Carbohydrates", "Advanced", "numerical",
      "How many stereoisomers are possible for the open-chain structure of an aldohexose, "
      "CH₂OH–(CHOH)₄–CHO?",
      ["8", "32", "16", "64"], "C",
      "Chiral centres and the 2ⁿ rule",
      "A carbon is chiral if it carries four different groups. In the open-chain aldohexose, C1 (CHO) and C6 (CH₂OH) "
      "are not chiral; C2, C3, C4 and C5 are. No meso form is possible because the two ends differ.",
      ["Chiral carbons: C2, C3, C4, C5 → n = 4",
       "Number of stereoisomers = 2⁴ = 16 (8 pairs of enantiomers; D-glucose is one of them)"],
      why_others_wrong="8 uses three chiral centres, as in a 2-ketohexose such as fructose. 32 counts C1 or C6 as "
                       "chiral. 64 counts all six carbons.",
      seconds=60, verified_by=RECOMPUTED),

    Q(T_BM, "Amino acids and proteins", "Advanced", "direct",
      "When egg white is boiled, its protein coagulates. Which statement correctly describes this change?",
      ["The protein is broken down into its amino acids.",
       "The secondary and tertiary structures are destroyed, but the primary structure remains intact.",
       "Only the peptide bonds near the ends of the chain are hydrolysed.",
       "The protein becomes more soluble and biologically more active."], "B",
      "Denaturation of proteins",
      "Heat (or a change in pH) breaks the hydrogen bonds and other weak interactions that hold the helices, "
      "sheets and folds. The chain unfolds and the protein loses its biological activity, but the covalent peptide "
      "bonds, and so the sequence of amino acids, are not broken.",
      ["Denaturation disturbs 2° and 3° structure", "Peptide bonds (1° structure) remain → amino acid sequence intact",
       "The denatured protein loses its biological activity and often becomes insoluble (coagulates)"],
      why_others_wrong="Breaking peptide bonds is hydrolysis, which needs acid, alkali or enzymes, not boiling alone.",
      ncert=f"{NC12}, 'Biomolecules', denaturation of proteins", seconds=35),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about carbohydrates are correct?",
          [("Maltose is made of two α-D-glucose units joined by a C1–C4 glycosidic linkage.", True),
           ("Amylose is a branched polymer, whereas amylopectin is an unbranched chain.", False),
           ("Sucrose is dextrorotatory, but the mixture obtained on its hydrolysis is laevorotatory.", True),
           ("Lactose is made of β-D-galactose and β-D-glucose, with C1 of galactose linked to C4 of glucose.", True),
           ("Cellulose is a straight-chain polymer of α-D-glucose units.", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "d", "e"]], "D"),
      "Disaccharides and polysaccharides",
      "Check each sugar for its units and the type of linkage, and remember that hydrolysis of sucrose changes the "
      "sign of rotation.",
      ["(a) Maltose: α-D-glucose (C1) – α-D-glucose (C4) → true",
       "(b) Reversed: amylose is the unbranched, water-soluble part; amylopectin is branched → false",
       "(c) Fructose (−92.4°) outweighs glucose (+52.5°), so the product (invert sugar) is laevorotatory → true",
       "(d) Lactose: β-D-galactose C1 – β-D-glucose C4 → true",
       "(e) Cellulose is made of β-D-glucose units → false"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides and polysaccharides", seconds=85),
]


# ================================================================ Principles Related to Practical Chemistry (242-250)
# 243: 2MnO4- + 5C2O4(2-) + 16H+ -> 2Mn2+ + 10CO2 + 8H2O; 20 mL of 0.05 M oxalic acid vs 0.02 M KMnO4
mmol_ox = 20 * F(5, 100)
vol_243 = mmol_ox * F(2, 5) / F(2, 100)
assert vol_243 == 20 and mmol_ox / F(2, 100) == 50 and mmol_ox * F(5, 2) / F(2, 100) == 125
# 245: 3.92 g Mohr's salt (392) in 250 mL; 25.0 mL needs 20.0 mL KMnO4; MnO4- : Fe2+ = 1 : 5
conc_fe = F(392, 100) / 392 / F(250, 1000)
mmol_fe = conc_fe * 25
m_kmno4 = mmol_fe / 5 / 20
assert conc_fe == F(4, 100) and mmol_fe == 1 and m_kmno4 == F(1, 100)
assert mmol_fe / 20 == F(5, 100) and mmol_fe * 2 / 5 / 20 == F(2, 100)
assert round(float(F(392, 100) / 152 / F(250, 1000) * 25 / 5 / 20), 3) == 0.026
# 248: enthalpy of neutralisation: 200 g solution, s = 4.2 J/g/K, dT = 3.4 K, 0.05 mol water formed
q_j = 200 * F(42, 10) * F(34, 10)
dh = -q_j / F(5, 100) / 1000
assert q_j == F(28560, 10) and round(float(dh), 1) == -57.1
assert round(float(-q_j / 2 / F(5, 100) / 1000), 1) == -28.6 and round(float(-q_j / F(25, 1000) / 1000), 1) == -114.2
# 249: initial rate proportional to 1/t and first order in thiosulphate: t2 = t1 x c1/c2
t2 = 40 * F(1, 10) / F(5, 100)
assert t2 == 80 and 40 * (F(1, 10) / F(5, 100)) ** 2 == 160

QUESTIONS += [
    Q(T_PR, "Detection of elements and functional groups", "Basic", "direct",
      "Which of the following gives a violet colour with neutral iron(III) chloride solution?",
      ["Phenol", "Ethanol", "Acetone", "Acetic acid"], "A",
      "Ferric chloride test for the phenolic group",
      "Phenols form coloured complexes with Fe³⁺. Phenol itself gives a violet colour with neutral FeCl₃; alcohols, "
      "ketones and acetic acid do not give this colour.",
      ["6C₆H₅OH + Fe³⁺ → coloured iron(III) phenoxide complex (violet)"],
      ncert=f"{LAB}, tests for functional groups (phenolic group)", seconds=20),

    Q(T_PR, "Titrimetric analysis", "Basic", "numerical",
      "20.0 mL of 0.05 M oxalic acid is titrated against 0.02 M KMnO₄ in the presence of dilute H₂SO₄. The volume of "
      "KMnO₄ needed is:",
      ["50 mL", "125 mL", "10 mL", "20 mL"], "D",
      "Mole ratio in the permanganate–oxalic acid titration",
      "2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O. Two moles of permanganate react with five moles of oxalic "
      "acid.",
      ["mmol oxalic acid = 20.0 × 0.05 = 1.0 mmol",
       "mmol KMnO₄ = 1.0 × 2/5 = 0.40 mmol",
       "Volume = 0.40/0.02 = 20 mL"],
      why_others_wrong="50 mL assumes a 1 : 1 ratio. 125 mL inverts the ratio (5/2 instead of 2/5). 10 mL halves the "
                       "correct volume.",
      ncert=f"{LAB}, titrimetric analysis (redox titrations)", seconds=45, verified_by=RECOMPUTED),

    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In salt analysis, the brown ring test (fresh FeSO₄ solution and concentrated H₂SO₄ poured down the side of "
      "the test tube) confirms the presence of:",
      ["Sulphate ion", "Chloride ion", "Nitrate ion", "Carbonate ion"], "C",
      "Confirmatory test for nitrate",
      "Nitrate is reduced by Fe²⁺ to NO, which combines with excess Fe²⁺ to form the brown complex "
      "[Fe(H₂O)₅(NO)]²⁺ at the junction of the two liquids.",
      ["NO₃⁻ + 3Fe²⁺ + 4H⁺ → NO + 3Fe³⁺ + 2H₂O",
       "[Fe(H₂O)₆]²⁺ + NO → [Fe(H₂O)₅(NO)]²⁺ + H₂O (brown ring)"],
      ncert=f"{LAB}, qualitative analysis (tests for anions)", seconds=25),

    Q(T_PR, "Titrimetric analysis", "Intermediate", "numerical",
      "3.92 g of Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O (molar mass 392 g mol⁻¹), is dissolved in water and made up to "
      "250 mL. 25.0 mL of this solution needs 20.0 mL of a KMnO₄ solution for complete oxidation in acidic medium. "
      "The molarity of the KMnO₄ solution is:",
      ["0.010 M", "0.050 M", "0.020 M", "0.026 M"], "A",
      "Standardising KMnO₄ with Mohr's salt",
      "Find the molarity of the Mohr's salt solution, then use MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O.",
      ["Moles of Mohr's salt = 3.92/392 = 0.01 mol in 250 mL → 0.04 M",
       "mmol Fe²⁺ in 25.0 mL = 25.0 × 0.04 = 1.0 mmol",
       "mmol MnO₄⁻ = 1.0/5 = 0.20 mmol",
       "Molarity = 0.20/20.0 = 0.010 M"],
      why_others_wrong="0.050 M assumes a 1 : 1 ratio. 0.020 M takes two electrons per Fe²⁺. 0.026 M uses the molar "
                       "mass of anhydrous FeSO₄ (152) instead of Mohr's salt.",
      ncert=f"{LAB}, titrimetric analysis (Mohr's salt against KMnO₄)", seconds=90, verified_by=RECOMPUTED),

    Q(T_PR, "Titrimetric analysis", "Intermediate", "assertion_reason",
      *ar("In the titration of oxalic acid with KMnO₄, the oxalic acid solution is warmed to about 50–60 °C before "
          "titrating.", True,
          "KMnO₄ acts as a self-indicator in this titration.", True, explains=False),
      "Conditions for the permanganate–oxalic acid titration",
      "The reaction between permanganate and oxalate is slow at room temperature, so the solution is warmed to make "
      "it fast enough for a sharp end point. Separately, the first permanent pink colour of excess MnO₄⁻ marks the "
      "end point, so no indicator is added.",
      ["A: warming speeds up the slow reaction → true",
       "R: excess MnO₄⁻ gives a pink colour at the end point → true",
       "Being a self-indicator has nothing to do with warming → R does not explain A"],
      why_others_wrong="Option A is the trap: both facts belong to the same titration, but R is not the reason for "
                       "warming.",
      ncert=f"{LAB}, titrimetric analysis (oxalic acid against KMnO₄)", seconds=45),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the cation in List-I with the group reagent that precipitates it in systematic salt analysis "
          "(List-II).",
          ["Cu²⁺", "Al³⁺", "Zn²⁺", "Ba²⁺"],
          ["(NH₄)₂CO₃ in the presence of NH₄OH", "H₂S in the presence of dilute HCl", "H₂S in the presence of NH₄OH",
           "NH₄OH in the presence of NH₄Cl"],
          {"A": "II", "B": "IV", "C": "III", "D": "I"},
          [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}], "C"),
      "Group reagents in cation analysis",
      "Group II sulphides (such as CuS) have very low solubility products and precipitate even in acid. Group IV "
      "sulphides (such as ZnS) need the higher S²⁻ concentration of ammoniacal solution. Group III hydroxides "
      "precipitate with NH₄OH, with NH₄Cl keeping the OH⁻ concentration low. Group V carbonates come next.",
      ["Cu²⁺: Group II → H₂S in dilute HCl → II", "Al³⁺: Group III → NH₄OH with NH₄Cl → IV",
       "Zn²⁺: Group IV → H₂S in NH₄OH → III", "Ba²⁺: Group V → (NH₄)₂CO₃ → I"],
      why_others_wrong="Swapping Cu²⁺ and Zn²⁺ is the common slip: ZnS is too soluble to precipitate in acid.",
      ncert=f"{LAB}, systematic qualitative analysis of cations", seconds=50),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "numerical",
      "100 mL of 0.5 M HCl is mixed with 100 mL of 0.5 M NaOH in a calorimeter, and the temperature rises by 3.4 K. "
      "Taking the density of the solution as 1 g mL⁻¹, its specific heat as 4.2 J g⁻¹ K⁻¹, and ignoring the heat "
      "absorbed by the calorimeter, the enthalpy of neutralisation is:",
      ["−28.6 kJ mol⁻¹", "−114.2 kJ mol⁻¹", "+57.1 kJ mol⁻¹", "−57.1 kJ mol⁻¹"], "D",
      "Enthalpy of neutralisation from a calorimetry experiment",
      "Heat released = mass of the whole mixture × specific heat × rise in temperature. Divide by the moles of "
      "water formed. Heat is given out, so ΔH is negative.",
      ["Mass of solution = 200 mL × 1 g mL⁻¹ = 200 g",
       "q = 200 × 4.2 × 3.4 = 2856 J",
       "Moles of H₂O formed = 0.100 L × 0.5 M = 0.05 mol",
       "ΔH = −2856/0.05 = −57 120 J mol⁻¹ ≈ −57.1 kJ mol⁻¹"],
      why_others_wrong="−28.6 kJ mol⁻¹ uses only 100 g of solution. −114.2 kJ mol⁻¹ divides by 0.025 mol. "
                       "+57.1 kJ mol⁻¹ has the wrong sign for an exothermic change.",
      ncert=f"{LAB}, thermochemistry (enthalpy of neutralisation)", seconds=100, verified_by=RECOMPUTED),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "numerical",
      "In a study of the reaction Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S + H₂O, the time taken for the precipitated "
      "sulphur to hide a cross marked under the flask is 40 s when the thiosulphate concentration is 0.10 M. The "
      "experiment is repeated with 0.05 M thiosulphate, all else unchanged. If the reaction is first order in "
      "thiosulphate and the initial rate is taken as proportional to 1/time, the new time is:",
      ["80 s", "20 s", "40 s", "160 s"], "A",
      "Effect of concentration on rate (sulphur-clock experiment)",
      "The cross disappears when a fixed amount of sulphur has formed, so the time taken is inversely proportional "
      "to the rate. For first order, rate ∝ [S₂O₃²⁻].",
      ["Rate ∝ 1/t and rate ∝ [S₂O₃²⁻] → t ∝ 1/[S₂O₃²⁻]",
       "Concentration halved → rate halved → time doubled",
       "t = 40 × (0.10/0.05) = 80 s"],
      why_others_wrong="20 s takes time as proportional to concentration. 40 s ignores the change. 160 s treats the "
                       "reaction as second order in thiosulphate.",
      ncert=f"{LAB}, chemical kinetics (effect of concentration on the rate of reaction)", seconds=75,
      verified_by=RECOMPUTED),

    Q(T_PR, "Detection of elements and functional groups", "Advanced", "multi_statement",
      *ms("Which of the following laboratory tests are correctly described?",
          [("Biuret test: a protein gives a violet colour with an alkaline solution of copper sulphate.", True),
           ("Schiff's test: acetone restores the pink colour of Schiff's reagent.", False),
           ("2,4-Dinitrophenylhydrazine gives a yellow-orange precipitate with both aldehydes and ketones.", True),
           ("Azo dye test: a primary aromatic amine, diazotised and then added to alkaline β-naphthol, gives an "
            "orange-red dye.", True),
           ("Fehling's test: sucrose gives a red precipitate of Cu₂O.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["c", "d", "e"]], "B"),
      "Tests for functional groups and biomolecules",
      "Match each test with the group it detects: biuret for peptide bonds, 2,4-DNP for the carbonyl group, the "
      "azo dye test for –NH₂ on a ring, and Schiff's/Fehling's for aldehyde (reducing) groups.",
      ["(a) Peptide bonds + Cu²⁺ in alkali → violet → true",
       "(b) Schiff's reagent is restored to pink by aldehydes, not by ketones such as acetone → false",
       "(c) Any >C=O of an aldehyde or ketone forms a 2,4-dinitrophenylhydrazone → true",
       "(d) ArN₂⁺ couples with β-naphthol → coloured azo dye → true",
       "(e) Sucrose has no free reducing group → no Cu₂O → false"],
      ncert=f"{LAB}, tests for functional groups and for carbohydrates and proteins", seconds=75),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_DF: (4, 5, 3), T_CC: (4, 6, 4), T_PU: (2, 2, 2), T_GO: (5, 7, 5), T_HC: (4, 6, 4), T_HX: (3, 4, 3),
        T_OX: (5, 7, 5), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (3, 3, 3)}

if __name__ == "__main__":
    assert len(QUESTIONS) == 119
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(132, 251)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert all(27 <= keys[k] <= 33 for k in LETTERS), keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    assert 0.27 <= fmts["numerical"] / 119 <= 0.33, fmts
    assert all(fmts[f] / 119 >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "Package CHE_001_p2: 119 original Chemistry questions (d/f block, coordination compounds, "
                    "organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_001/CHE_001_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
