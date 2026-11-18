"""Writes batches/parts/BATCH_002_CHE_p2.json: package CHE_002_p2 of BATCH_002 (Chemistry, 122 questions).

Topics: d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of Organic Compounds,
Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen,
Biomolecules (Chemistry), Principles Related to Practical Chemistry. IDs NEET_CHE_000379..NEET_CHE_000500.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_002/CHE_002_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_002_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 379, 500
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


def r2(x):
    """Round a Fraction or float to 2 decimals (as a float)."""
    return round(float(x), 2)


# ---------------------------------------------------------------- shared chemistry helpers
# Atomic masses used in the stems
C_, H_, O_, N_, S_, P_, BR, I_, NA, MG, CL = 12, 1, 16, 14, 32, 31, 80, 127, 23, 24, F(355, 10)


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    table = {"C": C_, "H": H_, "O": O_, "N": N_, "S": S_, "P": P_, "Br": BR, "I": I_, "Na": NA, "Mg": MG, "Cl": CL}
    return sum(table[k] * v for k, v in atoms.items())


def unpaired_oct(d, low_spin):
    """Unpaired electrons for an octahedral d^n ion (t2g holds 6, eg holds 4)."""
    if low_spin:
        t2g, eg = min(d, 6), max(0, d - 6)
    else:
        t2g = min(d, 3) + max(0, min(d - 5, 3))
        eg = min(max(d - 3, 0), 2) + max(0, d - 8)
    up = lambda n, cap: n if n <= cap // 2 else cap - n
    return up(t2g, 6) + up(eg, 4)


assert [unpaired_oct(d, False) for d in range(11)] == [0, 1, 2, 3, 4, 5, 4, 3, 2, 1, 0]
assert [unpaired_oct(d, True) for d in range(11)] == [0, 1, 2, 3, 2, 1, 0, 1, 2, 1, 0]

# Octahedral stereoisomer counter: positions 0/1 = +x/-x, 2/3 = +y/-y, 4/5 = +z/-z.
OPP = {0: 1, 1: 0, 2: 3, 3: 2, 4: 5, 5: 4}


def _rotations():
    rx = (0, 1, 4, 5, 3, 2)
    ry = (5, 4, 2, 3, 0, 1)
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


assert octahedral_isomers(["a", "a", "a", "a", "b", "b"], 0) == (2, 2)
assert octahedral_isomers([], 3) == (2, 1)


def square_planar_isomers(ligands):
    """Distinct arrangements of 4 monodentate ligands at the corners of a square (D4h symmetry)."""
    sym = [tuple((i + r) % 4 for i in range(4)) for r in range(4)]
    sym += [tuple((r - i) % 4 for i in range(4)) for r in range(4)]
    seen = set()
    for perm in set(itertools.permutations(ligands)):
        seen.add(min(tuple(perm[g[i]] for i in range(4)) for g in sym))
    return len(seen)


assert square_planar_isomers("aabb") == 2 and square_planar_isomers("aaab") == 1


QUESTIONS = []

# ================================================================ d- and f-Block Elements (379-390)
# 380: 2MnO4- + 10I- + 16H+ -> 2Mn2+ + 5I2 + 8H2O (Mn +7 -> +2: 5 e-; each I2 needs 2 e-)
mol_i2 = F(2) * 5 / 2
assert mol_i2 == 5 and F(2) * 5 == 10
# 382: neutral medium MnO4- -> MnO2 (3 e-); S2O3(2-) -> 2SO4(2-): S average +2 -> +6, 2 S atoms -> 8 e-
e_per_thio = 2 * (6 - 2)
mol_mno4 = F(3) * e_per_thio / 3
assert e_per_thio == 8 and mol_mno4 == 8 and F(3) * e_per_thio / 5 == F(24, 5) and 3 * e_per_thio == 24
# 387: Cr2O7(2-) takes 6 e-; H2S -> S gives 2 e- -> 3 S per dichromate
mass_s = F(5, 100) * 6 / 2 * S_
assert mass_s == F(48, 10) and F(5, 100) * S_ == F(16, 10) and F(5, 100) * 6 * S_ == F(96, 10) and F(5, 100) * 2 * S_ == F(32, 10)
# 389: MnO4- (5 e-) and NO2- -> NO3- (2 e-); NaNO2 = 69
m_nano2 = mm(Na=1, N=1, O=2)
mmol_mno4 = 20 * F(2, 100)
mg_nitrite = mmol_mno4 * 5 / 2 * m_nano2
assert m_nano2 == 69 and mg_nitrite == 69
assert r2(mmol_mno4 * m_nano2) == 27.6 and r2(mmol_mno4 * 2 / 5 * m_nano2) == 11.04 and r2(mmol_mno4 * 3 / 2 * m_nano2) == 41.4

QUESTIONS += [
    Q(T_DF, "Transition element trends", "Basic", "direct",
      "Which oxide of chromium is amphoteric?",
      ["CrO", "Cr₂O₃", "CrO₃", "None of the chromium oxides"], "B",
      "Acid–base character of transition metal oxides",
      "As the oxidation state of a metal rises, its oxide becomes more covalent and more acidic. Chromium(II) oxide "
      "is basic, chromium(III) oxide is amphoteric and chromium(VI) oxide is acidic.",
      ["CrO: Cr +2 → basic", "Cr₂O₃: Cr +3 → amphoteric (dissolves in both acids and alkalis)",
       "CrO₃: Cr +6 → acidic (gives chromic acid with water)"],
      why_others_wrong="CrO is basic and CrO₃ is acidic; Cr₂O₃ is the amphoteric one, so 'none' is also wrong.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxides and oxoanions of metals", seconds=25),

    N(T_DF, "K2Cr2O7 and KMnO4", "Basic",
      "Acidified potassium permanganate oxidises iodide ions to iodine. How many moles of I₂ are liberated by 2 mol "
      "of MnO₄⁻ ions?",
      ["2 mol", "10 mol", "2.5 mol", "5 mol"], "D", "5 mol",
      "Electron balance for permanganate in acid",
      "In acid, each MnO₄⁻ gains 5 electrons (Mn +7 → +2). Each I₂ formed needs 2 electrons to be removed from two "
      "I⁻ ions.",
      ["2MnO₄⁻ + 10I⁻ + 16H⁺ → 2Mn²⁺ + 5I₂ + 8H₂O",
       "Electrons accepted by 2 mol MnO₄⁻ = 2 × 5 = 10 mol",
       "Moles of I₂ = 10/2 = 5 mol"],
      why_others_wrong="10 mol is the number of I⁻ ions (or electrons), not I₂ molecules. 2 mol assumes a 1 : 1 "
                       "ratio. 2.5 mol halves the correct value.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (oxidising action in acid)", seconds=40),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "statement_pair",
      *sp("The general electronic configuration of the lanthanoids can be written as [Xe] 4f¹⁻¹⁴ 5d⁰⁻¹ 6s².", True,
          "Gadolinium has the configuration [Xe] 4f⁷ 5d¹ 6s², so the Gd³⁺ ion has a half-filled 4f⁷ subshell.", True),
      "Electronic configurations of the lanthanoids",
      "The lanthanoids fill the 4f subshell; some of them (La, Ce, Gd, Lu) keep one electron in 5d. Gd keeps the "
      "half-filled 4f⁷ arrangement and places the extra electron in 5d. Removing the 5d and two 6s electrons leaves "
      "Gd³⁺ as 4f⁷.",
      ["Statement I: matches the general configuration given in NCERT → true",
       "Statement II: Gd (Z = 64) = [Xe] 4f⁷ 5d¹ 6s² → Gd³⁺ = [Xe] 4f⁷ → true"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids (electronic configurations)", seconds=40),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "In neutral or faintly alkaline solution, permanganate oxidises thiosulphate to sulphate and is itself reduced "
      "to MnO₂. How many moles of MnO₄⁻ are needed to oxidise 3 mol of S₂O₃²⁻ ions completely?",
      ["3 mol", "8 mol", "4.8 mol", "24 mol"], "B", "8 mol",
      "Electron balance when the medium changes the product of permanganate",
      "In neutral medium MnO₄⁻ → MnO₂ (Mn +7 → +4), a gain of 3 electrons. In S₂O₃²⁻ the average oxidation state of "
      "S is +2; in SO₄²⁻ it is +6, so each thiosulphate ion loses 2 × 4 = 8 electrons.",
      ["Electrons lost by 3 mol S₂O₃²⁻ = 3 × 8 = 24 mol",
       "Moles of MnO₄⁻ = 24/3 = 8 mol",
       "Balanced: 8MnO₄⁻ + 3S₂O₃²⁻ + H₂O → 8MnO₂ + 6SO₄²⁻ + 2OH⁻"],
      why_others_wrong="4.8 mol uses the 5-electron change of acidic medium. 24 mol is the number of electrons, not "
                       "of MnO₄⁻ ions. 3 mol assumes a 1 : 1 ratio.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (neutral or faintly alkaline medium)",
      seconds=75),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Intermediate", "multi_statement",
      *ms("Which of the following statements about potassium dichromate and potassium permanganate are correct?",
          [("In the dichromate ion, two CrO₄ tetrahedra share one corner, giving a Cr–O–Cr linkage.", True),
           ("Fusion of MnO₂ with KOH and an oxidising agent such as KNO₃ gives dark green K₂MnO₄, a step in making "
            "KMnO₄.", True),
           ("The chromate ion is tetrahedral.", True),
           ("The dichromate ion contains a direct Cr–Cr bond.", False),
           ("Acidified KMnO₄ oxidises H₂S, and sulphur is precipitated.", True)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "c", "d", "e"]], "C"),
      "Structures and reactions of dichromate and permanganate",
      "Both oxoanions are built from tetrahedral MO₄ units. Dichromate is two tetrahedra joined through one shared "
      "oxygen atom; there is no metal–metal bond.",
      ["(a) Cr₂O₇²⁻: two tetrahedra sharing a corner, Cr–O–Cr angle about 126° → true",
       "(b) 2MnO₂ + 4KOH + O₂ → 2K₂MnO₄ + 2H₂O (KNO₃ can supply the oxygen); K₂MnO₄ is green → true",
       "(c) CrO₄²⁻ is tetrahedral → true",
       "(d) The two Cr atoms are joined only through a bridging O atom → false",
       "(e) H₂S → 2H⁺ + S, with MnO₄⁻ reduced to Mn²⁺ → true"],
      why_others_wrong="Every option containing (d) is wrong; leaving out (e) is also wrong because acidified "
                       "permanganate does oxidise H₂S to sulphur.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate", seconds=75),

    Q(T_DF, "Transition element trends", "Intermediate", "assertion_reason",
      *ar("The Cu⁺ ion is unstable in aqueous solution and disproportionates into Cu²⁺ and Cu.", True,
          "The hydration enthalpy of Cu²⁺(aq) is much more negative than that of Cu⁺, which more than compensates "
          "for the second ionisation enthalpy of copper.", True, explains=True),
      "Stability of oxidation states in aqueous solution",
      "Whether an ion is stable in water depends on ionisation enthalpies and hydration enthalpies together. Cu²⁺ "
      "is small and doubly charged, so it is hydrated far more strongly than Cu⁺.",
      ["A: 2Cu⁺(aq) → Cu²⁺(aq) + Cu(s) → true",
       "R: the large negative ΔhydH of Cu²⁺ outweighs the second ionisation enthalpy → true",
       "R is exactly why Cu²⁺(aq) is more stable than Cu⁺(aq) → R explains A"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', trends in stability of oxidation states", seconds=45),

    Q(T_DF, "Magnetic and colour properties", "Intermediate", "match_list",
      *ml("Match the property of transition metals in List-I with its cause in List-II.",
          ["Paramagnetism", "Colour of their ions", "Catalytic activity", "Ready formation of alloys"],
          ["Presence of unpaired electrons", "Similar atomic radii of the metals",
           "Ability to adopt multiple oxidation states and to form complexes", "d–d transitions of electrons"],
          {"A": "I", "B": "IV", "C": "III", "D": "II"},
          [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "I", "B": "IV", "C": "II", "D": "III"},
           {"A": "I", "B": "III", "C": "IV", "D": "II"}], "D"),
      "Origin of characteristic properties of transition elements",
      "Each typical property of the d-block has a specific cause in NCERT: magnetism from unpaired electrons, colour "
      "from d–d transitions, catalysis from variable oxidation states and complex formation, and alloy formation "
      "from similar atomic sizes.",
      ["Paramagnetism → unpaired electrons → I", "Colour → d–d transitions → IV",
       "Catalytic activity → multiple oxidation states and complex formation → III",
       "Alloys → atoms of similar radii replace one another in the lattice → II"],
      why_others_wrong="A-IV, B-I swaps magnetism and colour. C-II, D-III swaps the causes of catalysis and alloy "
                       "formation. B-III, C-IV gives colour to oxidation states.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', general properties of the transition elements", seconds=45),

    Q(T_DF, "Transition element trends", "Intermediate", "direct",
      "Interstitial compounds are formed when small atoms such as H, C or N are trapped inside the crystal lattices "
      "of transition metals. Which of the following is NOT a property of these compounds?",
      ["They have higher melting points than the pure metals.", "They are very hard.",
       "They are chemically very reactive.", "They retain metallic conductivity."], "C",
      "Interstitial compounds",
      "Compounds such as TiC, Mn₄N, Fe₃H and VH₀.₅₆ are usually non-stoichiometric. NCERT lists their properties: "
      "high melting points (higher than the pure metals), very hard, metallic conductivity retained, and "
      "chemically inert.",
      ["High melting point → true property", "Very hard (some borides approach diamond) → true property",
       "Metallic conductivity is retained → true property", "They are chemically inert, not reactive → the exception"],
      why_others_wrong="The other three are properties NCERT lists for interstitial compounds.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', interstitial compounds", seconds=35),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "H₂S gas is passed into an acidified solution containing 0.05 mol of K₂Cr₂O₇ until all the dichromate is "
      "reduced to Cr³⁺. The mass of sulphur precipitated is (S = 32):",
      ["1.6 g", "4.8 g", "9.6 g", "3.2 g"], "B", "4.8 g",
      "Electron balance between dichromate and H₂S",
      "Each Cr₂O₇²⁻ gains 6 electrons (2 Cr: +6 → +3). Each H₂S loses 2 electrons when it is oxidised to S "
      "(S: −2 → 0).",
      ["Cr₂O₇²⁻ + 3H₂S + 8H⁺ → 2Cr³⁺ + 3S + 7H₂O",
       "Moles of S = 0.05 × 3 = 0.15 mol",
       "Mass = 0.15 × 32 = 4.8 g"],
      shortcut="Electrons: 0.05 × 6 = 0.30 mol; S formed = 0.30/2 = 0.15 mol.",
      why_others_wrong="1.6 g assumes 1 mol S per mol dichromate. 3.2 g uses one S per Cr atom. 9.6 g treats H₂S as "
                       "a one-electron reductant (6 S per dichromate).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate (oxidising action)", seconds=90),

    Q(T_DF, "Transition element trends", "Advanced", "multi_statement",
      *ms("Consider the following statements about the 3d series.",
          [("E°(Mn³⁺/Mn²⁺) is strongly positive because Mn²⁺ (3d⁵) is particularly stable.", True),
           ("Cr²⁺ is a reducing agent, because changing from d⁴ to d³ gives a half-filled t₂g level.", True),
           ("Cr²⁺ and Mn³⁺ are both d⁴; Cr²⁺ is oxidising while Mn³⁺ is reducing.", False),
           ("Oxygen stabilises high oxidation states better than fluorine for manganese: the highest fluoride is MnF₄ "
            "whereas the highest oxide is Mn₂O₇.", True),
           ("Copper(II) iodide, CuI₂, is a stable compound.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "D"),
      "Electrode potentials and stability of oxidation states",
      "Stable configurations (d⁵, half-filled t₂g) decide which ions oxidise or reduce. Oxygen can form multiple "
      "bonds to the metal, so oxides reach higher oxidation states than fluorides.",
      ["(a) Mn³⁺ readily takes an electron to reach d⁵ Mn²⁺ → large positive E° → true",
       "(b) Cr²⁺ → Cr³⁺ (d³, t₂g³) easily → reducing agent → true",
       "(c) The roles are swapped: Cr²⁺ is reducing, Mn³⁺ is oxidising → false",
       "(d) MnF₄ vs Mn₂O₇ (Mn +7) → true",
       "(e) Cu²⁺ oxidises I⁻: 2Cu²⁺ + 4I⁻ → Cu₂I₂ + I₂, so CuI₂ does not exist → false"],
      why_others_wrong="Options with (c) swap the reducing and oxidising d⁴ ions; options with (e) forget that Cu²⁺ "
                       "oxidises iodide.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', standard electrode potentials and oxidation states", seconds=100),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "20.0 mL of 0.02 M KMnO₄ is exactly used up in oxidising a solution of sodium nitrite in dilute H₂SO₄ "
      "(nitrite → nitrate). The mass of NaNO₂ in the solution is (Na = 23, N = 14, O = 16):",
      ["27.6 mg", "41.4 mg", "69.0 mg", "11.0 mg"], "C", "69.0 mg",
      "Mole ratio in the permanganate–nitrite reaction",
      "In acid, MnO₄⁻ takes 5 electrons. Nitrite goes from N +3 to N +5 in nitrate, giving 2 electrons.",
      ["2MnO₄⁻ + 5NO₂⁻ + 6H⁺ → 2Mn²⁺ + 5NO₃⁻ + 3H₂O",
       "mmol MnO₄⁻ = 20.0 × 0.02 = 0.40 mmol",
       "mmol NO₂⁻ = 0.40 × 5/2 = 1.0 mmol",
       "Mass = 1.0 mmol × 69 mg mmol⁻¹ = 69.0 mg"],
      why_others_wrong="27.6 mg assumes a 1 : 1 ratio. 11.0 mg inverts the ratio (2/5 instead of 5/2). 41.4 mg uses "
                       "the 3-electron change of neutral medium.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (oxidising action in acid)", seconds=100),

    Q(T_DF, "Lanthanoids and actinoids", "Advanced", "assertion_reason",
      *ar("Tb⁴⁺ acts as an oxidising agent, readily changing to the common +3 state.", True,
          "In Tb⁴⁺ the 4f subshell is completely filled (4f¹⁴).", False),
      "Oxidation states of the lanthanoids and the stability of 4f configurations",
      "The common oxidation state of the lanthanoids is +3. A +4 ion that reverts to +3 is an oxidant. Terbium "
      "(Z = 65) is [Xe] 4f⁹ 6s². Losing four electrons leaves Tb⁴⁺ as 4f⁷, a half-filled subshell, which is why "
      "the +4 state forms at all.",
      ["A: Tb⁴⁺ + e⁻ → Tb³⁺, so Tb⁴⁺ is an oxidant → true",
       "R: Tb (Z = 65) = [Xe] 4f⁹ 6s² → Tb⁴⁺ = [Xe] 4f⁷ → half-filled, not completely filled → false"],
      why_others_wrong="R mixes up the half-filled 4f⁷ of Tb⁴⁺ with the completely filled 4f¹⁴ of ions such as "
                       "Yb²⁺. Because R is false, options A, B and D are wrong.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids (oxidation states)", seconds=55),
]


# ================================================================ Coordination Compounds (391-406)
# 393: [Co(en)2(C2O4)]Cl: complex ion charge +1; en neutral, oxalate -2
ox_co = 1 - (2 * 0 + (-2))
cn_co = 2 * 2 + 1 * 2
assert (ox_co, cn_co) == (3, 6)
# 396: [Pt(NH3)(Br)(Cl)(py)] square planar MABCD -> 3 geometrical isomers
assert square_planar_isomers("abcd") == 3 and math.factorial(4) // 4 == 6
# 397: [Co(NH3)5Cl]Cl2 -> [Co(NH3)5Cl]2+ + 2Cl-  : i = 3
dtf = 3 * F(1, 100) * F(186, 100)
assert dtf == F(558, 10000) and F(1, 100) * F(186, 100) == F(186, 10000)
assert 2 * F(1, 100) * F(186, 100) == F(372, 10000) and 4 * F(1, 100) * F(186, 100) == F(744, 10000)
# 402: [Pt(NH3)2Cl2(py)2]2+ = [MA2B2C2] -> 6 stereoisomers (5 geometrical, one of them chiral)
assert octahedral_isomers(["a", "a", "b", "b", "c", "c"], 0) == (6, 5)
# 403: d counts: Zn2+ 10, Cr3+ 3, Fe2+ 6 (aqua, high spin), Sc3+ 0, Cu+ 10, Mn2+ 5 (aqua, high spin)
d_counts = {"[Zn(NH3)4]2+": 10, "[Cr(NH3)6]3+": 3, "[Fe(H2O)6]2+": 6, "[Sc(H2O)6]3+": 0, "[Cu(CN)4]3-": 10,
            "[Mn(H2O)6]2+": 5}
# d10 and d0 have no unpaired electrons in any geometry; the others are octahedral high-spin or d3
n_dia = sum(1 for d in d_counts.values() if unpaired_oct(d, False) == 0)
assert n_dia == 3
# 406: [M(AA)3] is chiral (two stereoisomers, one geometrical form); trans-[M(AA)2B2] is not
assert octahedral_isomers([], 3) == (2, 1) and octahedral_isomers(["b", "b"], 2) == (3, 2)

QUESTIONS += [
    Q(T_CC, "Werner's theory and ligands", "Basic", "direct",
      "Which of the following is a hexadentate ligand?",
      ["Ethane-1,2-diamine (en)", "Oxalate ion", "Ammonia", "Ethylenediaminetetraacetate ion (EDTA⁴⁻)"], "D",
      "Denticity of ligands",
      "EDTA⁴⁻ binds a metal ion through two nitrogen atoms and four carboxylate oxygen atoms, so it is hexadentate.",
      ["en: two N donors → didentate", "C₂O₄²⁻: two O donors → didentate", "NH₃: one N donor → unidentate",
       "EDTA⁴⁻: 2 N + 4 O donors → hexadentate"],
      ncert=f"{NC12}, 'Coordination Compounds', definitions (ligands)", seconds=20),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of [Co(NH₃)₅Cl]Cl₂ is:",
      ["Pentaamminechloridocobalt(III) chloride", "Chloridopentaamminecobalt(III) chloride",
       "Pentaamminechloridocobalt(II) chloride", "Pentaamminechloridocobaltate(III) chloride"], "A",
      "Naming a complex cation",
      "Ligands are named in alphabetical order (ammine before chlorido), the metal keeps its plain name in a cation, "
      "and its oxidation state is shown in Roman numerals.",
      ["Oxidation state: x + 5(0) + (−1) = +2 (charge of the complex ion) → x = +3",
       "Ligands alphabetically: ammine (a) before chlorido (c) → pentaamminechlorido",
       "Cation → 'cobalt' (not 'cobaltate') → pentaamminechloridocobalt(III) chloride"],
      why_others_wrong="'Chloridopentaammine' ignores alphabetical order. Cobalt(II) misreads the oxidation state. "
                       "'-ate' is used only for anionic complexes.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=35),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "The oxidation state and the coordination number of cobalt in [Co(en)₂(C₂O₄)]Cl are, respectively "
      "(en = ethane-1,2-diamine):",
      ["+1 and 6", "+3 and 6", "+3 and 3", "+2 and 6"], "B", "+3 and 6",
      "Oxidation state and coordination number",
      "en is a neutral didentate ligand and oxalate is a didentate ligand with charge −2. One Cl⁻ outside the "
      "bracket means the complex ion carries +1.",
      ["Charge: x + 2(0) + (−2) = +1 → x = +3",
       "Donor atoms: 2 en × 2 + 1 C₂O₄²⁻ × 2 = 6 → coordination number 6"],
      why_others_wrong="+1 ignores the charge of oxalate. A coordination number of 3 counts ligands instead of donor "
                       "atoms. +2 takes oxalate as −1.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions (coordination number, oxidation number)", seconds=35),

    Q(T_CC, "Werner's theory and ligands", "Basic", "statement_pair",
      *sp("In Werner's theory, the secondary valences of the metal are ionisable and are satisfied by negative ions "
          "only.", False,
          "In Werner's theory, the primary valences are normally ionisable and are satisfied by negative ions.", True),
      "Primary and secondary valences",
      "Werner proposed two kinds of linkage. Primary valences are ionisable and satisfied by negative ions "
      "(they correspond to the oxidation state). Secondary valences are non-ionisable, equal the coordination "
      "number, and are satisfied by neutral molecules or negative ions.",
      ["Statement I: secondary valences are non-ionisable and can be satisfied by neutral molecules too → false",
       "Statement II: matches Werner's postulate → true"],
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory of coordination compounds", seconds=35),

    Q(T_CC, "Applications", "Basic", "match_list",
      *ml("Match the substance in List-I with the metal it contains in List-II.",
          ["Haemoglobin", "Vitamin B₁₂ (cyanocobalamin)", "cis-Platin (anticancer drug)",
           "Wilkinson's catalyst (used to hydrogenate alkenes)"],
          ["Platinum", "Rhodium", "Cobalt", "Iron"],
          {"A": "IV", "B": "III", "C": "I", "D": "II"},
          [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
           {"A": "IV", "B": "II", "C": "I", "D": "III"}], "C"),
      "Coordination compounds in biology, medicine and industry",
      "Several important substances are coordination compounds of a single metal: the oxygen carrier of blood, the "
      "anti-pernicious anaemia vitamin, an anticancer drug and a homogeneous hydrogenation catalyst.",
      ["Haemoglobin → iron → IV", "Vitamin B₁₂ → cobalt → III", "cis-[PtCl₂(NH₃)₂] → platinum → I",
       "Wilkinson's catalyst [(Ph₃P)₃RhCl] → rhodium → II"],
      why_others_wrong="A-III, B-IV swaps Fe and Co. C-II, D-I swaps Pt and Rh. B-II, D-III puts rhodium in the "
                       "vitamin.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications of coordination compounds", seconds=40),

    N(T_CC, "Isomerism", "Intermediate",
      "How many geometrical isomers are possible for the square planar complex [Pt(NH₃)(Br)(Cl)(py)] "
      "(py = pyridine)?",
      ["2", "3", "4", "6"], "B", "3",
      "Geometrical isomerism in square planar [MABCD]",
      "Fix one ligand, say NH₃. Any one of the other three can sit trans to it; the remaining two are then fixed. "
      "So there are three arrangements.",
      ["trans to NH₃: Br, Cl or py → 3 choices",
       "Once the trans partner of NH₃ is chosen, the other two ligands occupy the remaining trans pair",
       "Number of geometrical isomers = 3"],
      why_others_wrong="2 counts only cis and trans as for [MA₂B₂]. 6 = 4!/4 counts rotations but not reflections "
                       "of the square. 4 has no basis.",
      ncert=f"{NC12}, 'Coordination Compounds', geometrical isomerism", seconds=50),

    N(T_CC, "Werner's theory and ligands", "Intermediate",
      "A 0.01 mol kg⁻¹ aqueous solution of [Co(NH₃)₅Cl]Cl₂ is prepared. Assuming complete dissociation of the "
      "compound into its ions, the depression in freezing point is (Kf of water = 1.86 K kg mol⁻¹):",
      ["0.0186 K", "0.0372 K", "0.0744 K", "0.0558 K"], "D", "0.0558 K",
      "Ionisable counter ions and colligative properties",
      "Only the chloride ions outside the coordination sphere ionise. The Cl bound to cobalt stays in the complex "
      "cation.",
      ["[Co(NH₃)₅Cl]Cl₂ → [Co(NH₃)₅Cl]²⁺ + 2Cl⁻ → i = 3",
       "ΔTf = i Kf m = 3 × 1.86 × 0.01 = 0.0558 K"],
      why_others_wrong="0.0186 K ignores dissociation. 0.0372 K takes i = 2. 0.0744 K treats all three chlorines as "
                       "ionisable (i = 4).",
      seconds=60),

    Q(T_CC, "Crystal field theory", "Intermediate", "assertion_reason",
      *ar("Anhydrous copper(II) sulphate is white, whereas CuSO₄·5H₂O is blue.", True,
          "In the absence of ligands, crystal field splitting of the d orbitals does not occur.", True, explains=True),
      "Role of ligands in the colour of complexes",
      "Colour in a d-block compound comes from d–d transitions, which need the d orbitals to be split by ligands. "
      "When the water ligands are removed, there is no splitting and no visible absorption.",
      ["A: anhydrous CuSO₄ is white; the pentahydrate (with water ligands around Cu²⁺) is blue → true",
       "R: no ligands → d orbitals stay degenerate → no d–d transition → true",
       "R directly explains why removing water removes the colour → R explains A"],
      ncert=f"{NC12}, 'Coordination Compounds', colour in coordination compounds", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Match the complex in List-I with the coordination number of its metal in List-II.",
          ["[Ag(NH₃)₂]⁺", "[Ni(CO)₄]", "[Fe(CO)₅]", "[Co(en)₃]³⁺"], ["2", "4", "5", "6"],
          {"A": "I", "B": "II", "C": "III", "D": "IV"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
           {"A": "I", "B": "III", "C": "II", "D": "IV"}], "A"),
      "Coordination number counts donor atoms",
      "The coordination number is the number of ligand donor atoms bonded to the metal, not the number of ligands. "
      "Each en uses two N atoms.",
      ["[Ag(NH₃)₂]⁺: 2 N → 2 → I", "[Ni(CO)₄]: 4 C → 4 → II", "[Fe(CO)₅]: 5 C → 5 (trigonal bipyramidal) → III",
       "[Co(en)₃]³⁺: 3 × 2 N → 6 → IV"],
      why_others_wrong="C-IV, D-III counts the three en ligands as 3 (or 5). The other codes mix up the carbonyls.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions (coordination number, coordination polyhedron)",
      seconds=35),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("[Co(NH₃)₆]³⁺ is a homoleptic complex, because the metal is bound to only one kind of donor group.", True),
           ("[Co(NH₃)₄Cl₂]⁺ is a heteroleptic complex.", True),
           ("A chelating ligand is a unidentate ligand that can bind through either of two different donor atoms.",
            False),
           ("The coordination polyhedron of [Co(NH₃)₆]³⁺ is an octahedron.", True),
           ("In a coordination entity, the ligands act as Lewis acids.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "B"),
      "Terms used in coordination chemistry",
      "Ligands donate electron pairs (Lewis bases) to the metal (Lewis acid). A chelating ligand is a di- or "
      "polydentate ligand that binds through two or more donor atoms at once; a ligand that can bind through either "
      "of two atoms is ambidentate.",
      ["(a) Only NH₃ ligands → homoleptic → true", "(b) NH₃ and Cl⁻ ligands → heteroleptic → true",
       "(c) This describes an ambidentate ligand, not a chelating one → false",
       "(d) Six donor atoms around Co³⁺ → octahedral → true",
       "(e) Ligands are electron-pair donors (Lewis bases) → false"],
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=70),

    Q(T_CC, "Crystal field theory", "Intermediate", "direct",
      "Which of the following arrangements of ligands is in the correct order of increasing crystal field "
      "splitting (spectrochemical series)?",
      ["F⁻ < Cl⁻ < H₂O < en < CO", "Cl⁻ < F⁻ < en < H₂O < CO", "Cl⁻ < H₂O < F⁻ < en < CO",
       "Cl⁻ < F⁻ < H₂O < en < CO"], "D",
      "Spectrochemical series",
      "The experimentally determined order is I⁻ < Br⁻ < SCN⁻ < Cl⁻ < S²⁻ < F⁻ < OH⁻ < C₂O₄²⁻ < H₂O < NCS⁻ < "
      "edta⁴⁻ < NH₃ < en < CN⁻ < CO.",
      ["Halides are weak: Cl⁻ < F⁻", "F⁻ is below H₂O", "H₂O < en (en is above NH₃)", "CO is the strongest"],
      why_others_wrong="The first option swaps Cl⁻ and F⁻. The second places en below H₂O. The third places F⁻ above "
                       "H₂O.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory (spectrochemical series)", seconds=40),

    N(T_CC, "Isomerism", "Advanced",
      "The total number of stereoisomers (geometrical and optical together) of the octahedral ion "
      "[Pt(NH₃)₂Cl₂(py)₂]²⁺ (py = pyridine, a unidentate ligand) is:",
      ["5", "8", "6", "4"], "C", "6",
      "Stereoisomers of an octahedral [MA₂B₂C₂] complex",
      "List the arrangements by which pairs are trans. Either all three pairs are trans, or exactly one pair is "
      "trans, or none is. Then check each arrangement for a mirror image that cannot be superimposed.",
      ["All three pairs trans (A/A, B/B, C/C) → 1 isomer",
       "Only A/A trans, only B/B trans or only C/C trans → 3 isomers",
       "No pair trans (all cis) → 1 arrangement, which is chiral → a pair of enantiomers",
       "Geometrical isomers = 1 + 3 + 1 = 5; stereoisomers = 5 + 1 = 6"],
      why_others_wrong="5 counts only geometrical isomers and misses the enantiomer of the all-cis form. 4 and 8 come "
                       "from counting the trans/cis cases incorrectly.",
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=120),

    N(T_CC, "Crystal field theory", "Advanced",
      "How many of the following are diamagnetic?\n[Zn(NH₃)₄]²⁺, [Cr(NH₃)₆]³⁺, [Fe(H₂O)₆]²⁺, [Sc(H₂O)₆]³⁺, "
      "[Cu(CN)₄]³⁻, [Mn(H₂O)₆]²⁺\n(Atomic numbers: Sc 21, Cr 24, Mn 25, Fe 26, Cu 29, Zn 30)",
      ["2", "4", "1", "3"], "D", "3",
      "Unpaired electrons from oxidation state and d count",
      "Find each metal's oxidation state and d count. d⁰ and d¹⁰ ions have no unpaired electrons whatever the "
      "ligand. Water is a weak-field ligand, so the aqua ions are high spin.",
      ["Zn²⁺ 3d¹⁰ → diamagnetic", "Cr³⁺ 3d³ → 3 unpaired → paramagnetic",
       "Fe²⁺ 3d⁶ with H₂O (high spin) → 4 unpaired → paramagnetic", "Sc³⁺ 3d⁰ → diamagnetic",
       "Cu⁺ (in [Cu(CN)₄]³⁻: x − 4 = −3 → +1) 3d¹⁰ → diamagnetic",
       "Mn²⁺ 3d⁵ with H₂O → 5 unpaired → paramagnetic", "Diamagnetic: 3"],
      why_others_wrong="2 usually comes from taking copper as Cu²⁺ (d⁹). 4 treats [Fe(H₂O)₆]²⁺ as low spin. 1 counts "
                       "only the zinc complex.",
      seconds=110),

    Q(T_CC, "Crystal field theory", "Advanced", "statement_pair",
      *sp("For a d⁴ ion in an octahedral field, if Δo < P (pairing energy), the fourth electron enters an eg "
          "orbital, giving the configuration t₂g³ eg¹.", True,
          "Ligands for which Δo > P are called weak field ligands and form high spin complexes.", False),
      "Strong and weak field ligands",
      "The fourth electron either pairs in t₂g (cost P) or goes up to eg (cost Δo). It takes the cheaper path. "
      "Ligands giving Δo < P are weak field (high spin); those giving Δo > P are strong field (low spin).",
      ["Statement I: Δo < P → occupying eg is cheaper → t₂g³ eg¹ → true",
       "Statement II: Δo > P describes strong field ligands, which form low spin complexes → false"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=50),

    Q(T_CC, "Valence bond theory", "Advanced", "multi_statement",
      *ms("Which of the following statements about the theories of bonding in coordination compounds are correct?",
          [("Valence bond theory does not explain the colour of coordination compounds.", True),
           ("Valence bond theory gives a quantitative interpretation of magnetic data.", False),
           ("Crystal field theory treats the metal–ligand bond as ionic, arising purely from electrostatic "
            "interaction between the metal ion and the ligands.", True),
           ("In crystal field theory, anionic ligands are treated as point charges and neutral ligands as point "
            "dipoles.", True),
           ("Valence bond theory distinguishes clearly between weak and strong field ligands.", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "d", "e"]], "B"),
      "Limitations of VBT and assumptions of CFT",
      "NCERT lists the shortcomings of valence bond theory: it rests on several assumptions, gives no quantitative "
      "interpretation of magnetic data, does not explain colour, and does not distinguish weak from strong ligands. "
      "Crystal field theory is an electrostatic model.",
      ["(a) Colour is not explained by VBT → true",
       "(b) VBT gives no quantitative interpretation of magnetic data → false",
       "(c) CFT: purely electrostatic, ionic bond → true",
       "(d) Point charges (anions) and point dipoles (neutral molecules) → true",
       "(e) VBT does not distinguish weak and strong ligands → false"],
      ncert=f"{NC12}, 'Coordination Compounds', bonding in coordination compounds (VBT limitations, CFT)",
      seconds=80),

    Q(T_CC, "Isomerism", "Advanced", "direct",
      "Which of the following complexes is optically active?",
      ["trans-[Co(en)₂Cl₂]⁺", "cis-[Pt(NH₃)₂Cl₂]", "[Cr(C₂O₄)₃]³⁻", "[Co(NH₃)₆]³⁺"], "C",
      "Chirality of octahedral chelate complexes",
      "A complex is optically active when it has no plane or centre of symmetry. Three didentate chelates wrapped "
      "around an octahedron form a propeller that is not superimposable on its mirror image.",
      ["trans-[Co(en)₂Cl₂]⁺: the two en rings lie in one plane, which is a mirror plane → inactive",
       "cis-[Pt(NH₃)₂Cl₂]: square planar, the molecular plane is a mirror plane → inactive",
       "[Cr(C₂O₄)₃]³⁻: [M(AA)₃] type → exists as d and l forms → optically active",
       "[Co(NH₃)₆]³⁺: highly symmetric → inactive"],
      why_others_wrong="It is the cis (not the trans) isomer of [Co(en)₂Cl₂]⁺ that is chiral. Square planar complexes "
                       "of this kind are never optically active.",
      ncert=f"{NC12}, 'Coordination Compounds', optical isomerism", seconds=50),
]


# ================================================================ Purification and Characterisation (407-412)
# 408: %C = (12/44) x m(CO2) / m(sample) x 100
pc = F(12, 44) * F(44, 100) / F(30, 100) * 100
assert pc == 40 and r2(F(12, 28) * F(44, 100) / F(30, 100) * 100) == 62.86 and r2(F(12, 44) * 100) == 27.27
# 409: %P = (62/222) x m(Mg2P2O7) / m(sample) x 100 ; Mg2P2O7 = 222
m_mg2p2o7 = mm(Mg=2, P=2, O=7)
pp = F(2 * P_, m_mg2p2o7) * F(444, 1000) / F(248, 1000) * 100
assert m_mg2p2o7 == 222 and pp == 50
assert F(P_, 222) * F(444, 1000) / F(248, 1000) * 100 == 25
assert r2(F(62, 142) * F(444, 1000) / F(248, 1000) * 100) == 78.17 and r2(F(62, 222) * 100) == 27.93
# 411: 0.45 g gives 0.66 g CO2 and 0.27 g H2O; M = 90
mc, mh = F(66, 100) * 12 / 44, F(27, 100) * 2 / 18
mo = F(45, 100) - mc - mh
nc, nh, no = mc / 12, mh / 1, mo / 16
assert (mc, mh, mo) == (F(18, 100), F(3, 100), F(24, 100)) and nh / nc == 2 and no / nc == 1
efm = mm(C=1, H=2, O=1)
assert efm == 30 and 90 // efm == 3 and mm(C=3, H=6, O=3) == 90

QUESTIONS += [
    Q(T_PU, "Purification methods", "Basic", "direct",
      "A sample of naphthalene contains a small amount of sodium chloride as an impurity. Which method is the most "
      "suitable for purifying the naphthalene?",
      ["Sublimation", "Fractional distillation", "Distillation under reduced pressure", "Simple distillation"], "A",
      "Sublimation",
      "Some solids change directly into vapour on heating, and the vapour condenses back to the solid on cooling. "
      "Naphthalene sublimes, while sodium chloride does not, so heating separates the two.",
      ["Naphthalene: sublimable", "NaCl: non-sublimable ionic solid",
       "Heat the mixture; pure naphthalene collects on a cool surface → sublimation"],
      why_others_wrong="The three distillation methods are for liquids; neither component here is a liquid to be "
                       "boiled off.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', methods of purification "
            f"(sublimation)", seconds=25),

    N(T_PU, "Quantitative analysis and formulae", "Basic",
      "On complete combustion, 0.30 g of an organic compound gives 0.44 g of CO₂. The percentage of carbon in the "
      "compound is (C = 12, O = 16):",
      ["27.3%", "12.0%", "40.0%", "62.9%"], "C", "40.0%",
      "Estimation of carbon",
      "All the carbon of the compound ends up in CO₂, and 12 g of every 44 g of CO₂ is carbon.",
      ["Mass of C = (12/44) × 0.44 = 0.12 g", "% C = (0.12/0.30) × 100 = 40.0%"],
      why_others_wrong="27.3% is just the fraction of carbon in CO₂. 12.0% forgets to divide by the 0.30 g sample. "
                       "62.9% uses 12/28, the factor for CO.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis (carbon and "
            f"hydrogen)", seconds=40),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "In the estimation of phosphorus, 0.248 g of an organic compound is oxidised and the phosphoric acid formed is "
      "finally weighed as 0.444 g of Mg₂P₂O₇. The percentage of phosphorus in the compound is (Mg = 24, P = 31, "
      "O = 16):",
      ["25.0%", "78.2%", "27.9%", "50.0%"], "D", "50.0%",
      "Estimation of phosphorus as magnesium pyrophosphate",
      "Each Mg₂P₂O₇ (molar mass 222 g mol⁻¹) contains two P atoms (62 g).",
      ["Mass of P = (62/222) × 0.444 = 0.124 g", "% P = (0.124/0.248) × 100 = 50.0%"],
      why_others_wrong="25.0% counts only one P atom per Mg₂P₂O₇. 78.2% uses the factor for P₂O₅ (62/142). 27.9% "
                       "is the fraction of P in Mg₂P₂O₇, without using the sample mass.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis "
            f"(phosphorus)", seconds=60),

    Q(T_PU, "Purification methods", "Intermediate", "assertion_reason",
      *ar("Aniline is separated from an aniline–water mixture by steam distillation.", True,
          "Aniline is volatile in steam and is immiscible with water.", True, explains=True),
      "Steam distillation",
      "Steam distillation is used for substances that are steam volatile and immiscible with water. The mixture "
      "boils when the sum of the vapour pressures of the substance and water equals atmospheric pressure, so the "
      "substance distils below its own boiling point.",
      ["A: NCERT gives aniline as the example of steam distillation → true",
       "R: these are exactly the two conditions for steam distillation → true",
       "R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', methods of purification "
            f"(steam distillation)", seconds=35),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "0.45 g of an organic compound containing only C, H and O gives 0.66 g of CO₂ and 0.27 g of H₂O on complete "
      "combustion. Its molar mass is 90 g mol⁻¹. The molecular formula of the compound is (C = 12, H = 1, O = 16):",
      ["C₂H₄O₂", "C₃H₆O₃", "C₃H₈O₃", "C₆H₁₂O₆"], "B", "C₃H₆O₃",
      "Empirical and molecular formula from combustion data",
      "Find the masses of C and H from CO₂ and H₂O, get O by difference, convert to moles, and scale the empirical "
      "formula to the molar mass.",
      ["C = (12/44) × 0.66 = 0.18 g; H = (2/18) × 0.27 = 0.03 g; O = 0.45 − 0.21 = 0.24 g",
       "Moles: C 0.015, H 0.030, O 0.015 → ratio 1 : 2 : 1 → empirical formula CH₂O (30 g mol⁻¹)",
       "n = 90/30 = 3 → C₃H₆O₃"],
      why_others_wrong="C₂H₄O₂ has the right empirical formula but a molar mass of 60. C₃H₈O₃ (92) has the wrong H : C "
                       "ratio. C₆H₁₂O₆ (180) doubles the molar mass.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis",
      seconds=120),

    Q(T_PU, "Purification methods", "Advanced", "multi_statement",
      *ms("Which of the following statements about methods of purification are correct?",
          [("In column chromatography, the component that is adsorbed less strongly on the adsorbent moves down the "
            "column faster and is eluted first.", True),
           ("Simple distillation can separate two liquids whose boiling points differ only slightly.", False),
           ("Crystallisation depends on the difference in solubilities of the compound and its impurities in a "
            "suitable solvent.", True),
           ("In differential extraction, the organic compound should be more soluble in water than in the organic "
            "solvent.", False),
           ("Paper chromatography is a type of partition chromatography.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "e"]], "C"),
      "Principles behind purification techniques",
      "Each method exploits one difference between the compound and its impurities: adsorption, boiling point, "
      "solubility or distribution between two phases.",
      ["(a) Strongly adsorbed components stay near the top; weakly adsorbed ones come down first → true",
       "(b) Close boiling points need fractional distillation → false",
       "(c) Crystallisation exploits solubility differences → true",
       "(d) The compound must be more soluble in the organic solvent, so it can be extracted from water → false",
       "(e) Paper chromatography: water held in the paper is the stationary phase → partition → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', methods of purification",
      seconds=80),
]


# ================================================================ Some Basic Principles of Organic Chemistry (413-429)
# 415: 2,2,4-trimethylpentane carbon skeleton; primary carbon = bonded to one other carbon
bonds = [(1, 2), (2, 3), (3, 4), (4, 5), (2, 6), (2, 7), (4, 8)]
deg = Counter(x for b in bonds for x in b)
assert len(deg) == 8 and sum(1 for c in deg if deg[c] == 1) == 5
# 418: chiral when the candidate carbon carries four different groups
cand = {"butan-2-ol": ("H", "OH", "CH3", "C2H5"), "propan-2-ol": ("H", "OH", "CH3", "CH3"),
        "2-chlorobutane": ("H", "Cl", "CH3", "C2H5"), "3-chloropentane": ("H", "Cl", "C2H5", "C2H5"),
        "2-bromopropanoic acid": ("H", "Br", "CH3", "COOH"), "1-chlorobutane": ("H", "H", "Cl", "C3H7")}
assert sum(1 for g in cand.values() if len(set(g)) == 4) == 3
# 419: fourth member of the aldehydes HCHO, CH3CHO, C2H5CHO, C3H7CHO -> C4H8O
alde = [mm(C=n, H=2 * n, O=1) for n in range(1, 6)]
assert alde == [30, 44, 58, 72, 86]
# 425: hepta-2,5-diene CH3CH=CHCH2CH=CHCH3: E/Z at each double bond, molecule symmetric end to end
forms = {min((a, b), (b, a)) for a in "EZ" for b in "EZ"}
assert len(forms) == 3
# 426: penta-1,2-diene CH2=C=CH-CH2-CH3: pi bonds per carbon -> 0 sp3, 1 sp2, 2 sp
pi = {1: 1, 2: 2, 3: 1, 4: 0, 5: 0}
hyb = Counter({0: "sp3", 1: "sp2", 2: "sp"}[v] for v in pi.values())
assert (hyb["sp2"], hyb["sp"], hyb["sp3"]) == (2, 1, 2)

QUESTIONS += [
    Q(T_GO, "Types of organic reactions", "Basic", "direct",
      "Which of the following species is an electrophile?",
      ["NH₃", "CN⁻", "BF₃", "CH₃OH"], "C",
      "Electrophiles and nucleophiles",
      "An electrophile is an electron-seeking (electron-pair accepting) species. BF₃ has only six electrons around "
      "boron and readily accepts an electron pair.",
      ["NH₃: lone pair on N → nucleophile", "CN⁻: negative ion with lone pairs → nucleophile",
       "BF₃: electron-deficient B → electrophile", "CH₃OH: lone pairs on O → nucleophile"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=20),

    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of (CH₃)₃C–CH₂–Br is:",
      ["2,2-Dimethyl-1-bromopropane", "3-Bromo-2,2-dimethylpropane", "1-Bromopentane",
       "1-Bromo-2,2-dimethylpropane"], "D",
      "Naming a haloalkane with branching",
      "The longest chain has three carbons. Numbering from the end that gives the lowest locants puts Br on C-1 "
      "and both methyls on C-2. Prefixes are written in alphabetical order (bromo before methyl).",
      ["Parent chain: CH₂Br–C(CH₃)₂–CH₃ → propane",
       "Locants: Br at 1, methyls at 2,2 → set {1,2,2} is lower than {2,2,3}",
       "Alphabetical order: bromo, then dimethyl → 1-bromo-2,2-dimethylpropane"],
      why_others_wrong="'2,2-Dimethyl-1-bromo' breaks alphabetical order. '3-Bromo' numbers from the wrong end. "
                       "1-Bromopentane is a different (unbranched) isomer.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=35),

    N(T_GO, "Hybridisation and functional groups", "Basic",
      "How many primary (1°) carbon atoms are present in 2,2,4-trimethylpentane, (CH₃)₃C–CH₂–CH(CH₃)–CH₃?",
      ["3", "5", "4", "8"], "B", "5",
      "Classifying carbon atoms",
      "A primary carbon is bonded to only one other carbon atom. Here every CH₃ group is primary.",
      ["(CH₃)₃C–: three CH₃ groups → 3 primary", "–CH(CH₃)–CH₃ at the other end: two CH₃ groups → 2 primary",
       "CH₂ is secondary, CH is tertiary, the C bearing three methyls is quaternary",
       "Primary carbons = 3 + 2 = 5"],
      why_others_wrong="8 is the total number of carbon atoms. 3 counts only the tert-butyl methyls. 4 misses one "
                       "of the methyls at C-4.",
      seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "statement_pair",
      *sp("The functional group of an ester is –COOR.", True,
          "Aldehydes and ketones both contain the carbonyl group; in a ketone the carbonyl carbon is bonded to two "
          "carbon atoms.", True),
      "Functional groups",
      "Esters are RCOOR′. In aldehydes the carbonyl carbon carries at least one hydrogen; in ketones it is bonded to "
      "two carbon groups.",
      ["Statement I: e.g. CH₃COOC₂H₅ → –COOR → true",
       "Statement II: e.g. CH₃COCH₃ → >C=O between two carbons → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', functional groups", seconds=25),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "match_list",
      *ml("Match the compound in List-I with the class of compound in List-II.",
          ["CH₃CONH₂", "CH₃CN", "(CH₃CO)₂O", "CH₃COCl"],
          ["Acid chloride", "Acid anhydride", "Nitrile", "Amide"],
          {"A": "IV", "B": "III", "C": "II", "D": "I"},
          [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
           {"A": "II", "B": "III", "C": "IV", "D": "I"}], "D"),
      "Functional groups derived from carboxylic acids",
      "Replace the –OH of CH₃COOH by –NH₂ (amide), –Cl (acid chloride) or –OCOCH₃ (anhydride). A nitrile carries "
      "the –C≡N group.",
      ["CH₃CONH₂ → amide → IV", "CH₃C≡N → nitrile → III", "CH₃CO–O–COCH₃ → anhydride → II",
       "CH₃COCl → acid chloride → I"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', functional groups", seconds=30),

    N(T_GO, "Isomerism", "Intermediate",
      "How many of the following compounds are chiral (contain a carbon atom bonded to four different groups)?\n"
      "Butan-2-ol, propan-2-ol, 2-chlorobutane, 3-chloropentane, 2-bromopropanoic acid, 1-chlorobutane",
      ["2", "4", "3", "5"], "C", "3",
      "Asymmetric carbon atoms",
      "Look at the carbon carrying the substituent in each molecule and list its four groups.",
      ["Butan-2-ol: H, OH, CH₃, C₂H₅ → chiral", "Propan-2-ol: two CH₃ groups → not chiral",
       "2-Chlorobutane: H, Cl, CH₃, C₂H₅ → chiral", "3-Chloropentane: two C₂H₅ groups → not chiral",
       "2-Bromopropanoic acid: H, Br, CH₃, COOH → chiral", "1-Chlorobutane: CH₂Cl has two H → not chiral",
       "Chiral: 3"],
      why_others_wrong="4 usually counts 3-chloropentane, forgetting its two identical ethyl groups. 2 misses the "
                       "chiral carbon of 2-bromopropanoic acid.",
      seconds=60),

    N(T_GO, "Hybridisation and functional groups", "Intermediate",
      "The members of a homologous series differ by a –CH₂– unit. The first member of the aliphatic aldehydes is "
      "methanal, HCHO. The molar mass of the fourth member of this series is (C = 12, H = 1, O = 16):",
      ["58 g mol⁻¹", "72 g mol⁻¹", "86 g mol⁻¹", "44 g mol⁻¹"], "B", "72 g mol⁻¹",
      "Homologous series",
      "Each next member adds CH₂ (14 g mol⁻¹). The aldehydes are HCHO, CH₃CHO, CH₃CH₂CHO, CH₃CH₂CH₂CHO, ...",
      ["Fourth member: butanal, C₄H₈O", "Molar mass = 4(12) + 8(1) + 16 = 72 g mol⁻¹",
       "Check: 30 + 3 × 14 = 72"],
      why_others_wrong="58 is the third member (propanal), 86 the fifth (pentanal) and 44 the second (ethanal).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', homologous series", seconds=35),

    Q(T_GO, "Electronic effects", "Intermediate", "direct",
      "Which of the following groups, attached to a benzene ring, shows a −R (electron-withdrawing resonance) "
      "effect?",
      ["–OH", "–NH₂", "–OCH₃", "–CHO"], "D",
      "Resonance (mesomeric) effect",
      "A group with a lone pair on the atom next to the ring pushes electrons into the ring (+R). A group with a "
      "multiple bond to a more electronegative atom, such as C=O, pulls π electrons out of the ring (−R).",
      ["–OH, –NH₂, –OCH₃: lone pair on O or N → +R",
       "–CHO: C=O conjugated with the ring draws π electrons towards O → −R"],
      why_others_wrong="–OH, –NH₂ and –OCH₃ all donate electrons by resonance.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance effect", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "assertion_reason",
      *ar("The carbon–carbon bond length in ethene is greater than that in ethane.", False,
          "The carbon–carbon bond in ethene consists of one σ bond and one π bond.", True),
      "Bond length and bond order",
      "A double bond (σ + π) holds the two carbon atoms closer than a single σ bond. The C=C bond in ethene is "
      "134 pm, shorter than the C–C bond in ethane (154 pm).",
      ["A: ethene C=C (134 pm) < ethane C–C (154 pm) → A is false",
       "R: C=C = one σ (sp²–sp²) + one π (2p–2p) → true"],
      why_others_wrong="R is true, but it implies the opposite of A: the extra π bond shortens the bond.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', shapes of carbon compounds",
      seconds=35),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "statement_pair",
      *sp("The IUPAC name of (CH₃)₂CH–CH₂–OH is 2-methylpropan-2-ol.", False,
          "The IUPAC name of CH₃–CO–CH₂–CH₃ is butan-3-one.", False),
      "Locants in IUPAC names",
      "Number the chain from the end that gives the principal functional group the lowest locant.",
      ["(CH₃)₂CH–CH₂OH: OH on C-1, methyl on C-2 → 2-methylpropan-1-ol, so Statement I is false "
       "(2-methylpropan-2-ol is (CH₃)₃COH)",
       "CH₃COCH₂CH₃: numbering from the left gives C=O at C-2 → butan-2-one, so Statement II is false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=40),

    Q(T_GO, "Electronic effects", "Intermediate", "multi_statement",
      *ms("Which of the following statements about electronic effects are correct?",
          [("–NO₂, –CN and –COOH groups show a −I effect.", True),
           ("The –CH₃ group shows a −I effect.", False),
           ("The inductive effect is a permanent effect.", True),
           ("Halogens attached to a carbon chain show a −I effect.", True),
           ("Electron-withdrawing groups attached to the positive carbon stabilise a carbocation.", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "d", "e"]], "B"),
      "Inductive effect and carbocation stability",
      "Groups more electronegative than carbon pull σ electrons (−I); alkyl groups release them (+I). A carbocation "
      "is electron-deficient, so electron-releasing groups stabilise it and electron-withdrawing groups destabilise "
      "it.",
      ["(a) –NO₂, –CN, –COOH withdraw electrons → −I → true", "(b) Alkyl groups are electron-releasing (+I) → false",
       "(c) The inductive effect is a permanent polarisation of σ bonds → true",
       "(d) Halogens are more electronegative than C → −I → true",
       "(e) Withdrawing electron density increases the positive charge → destabilises → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', electron displacement effects",
      seconds=60),

    Q(T_GO, "Types of organic reactions", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with its type in List-II.",
          ["CH₃Br + OH⁻ → CH₃OH + Br⁻", "CH₂=CH₂ + HBr → CH₃CH₂Br",
           "CH₃CH₂Br + alcoholic KOH → CH₂=CH₂ + KBr + H₂O",
           "n-Hexane heated with anhydrous AlCl₃ and HCl → 2-methylpentane + 3-methylpentane"],
          ["Elimination", "Rearrangement", "Substitution", "Addition"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
      "Types of organic reactions",
      "Substitution replaces one group by another; addition joins two parts across a multiple bond; elimination "
      "removes atoms to form a multiple bond; rearrangement changes the carbon skeleton without changing the "
      "molecular formula.",
      ["A: Br replaced by OH → substitution → III", "B: H and Br add across C=C → addition → IV",
       "C: H and Br removed to form C=C → elimination → I",
       "D: straight chain → branched isomers (same formula) → rearrangement (isomerisation) → II"],
      why_others_wrong="A-IV, B-III swaps substitution and addition. C-II, D-I calls the isomerisation an "
                       "elimination. A-I, C-III swaps substitution and elimination.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', types of organic reactions",
      seconds=40),

    N(T_GO, "Isomerism", "Advanced",
      "How many geometrical isomers are possible for hepta-2,5-diene, CH₃–CH=CH–CH₂–CH=CH–CH₃?",
      ["4", "2", "6", "3"], "D", "3",
      "Geometrical isomerism with two double bonds in a symmetric molecule",
      "Each double bond can be cis or trans, giving 2 × 2 = 4 combinations. Because the molecule is the same read "
      "from either end, cis,trans and trans,cis are the same compound.",
      ["Combinations: cis,cis; trans,trans; cis,trans; trans,cis",
       "cis,trans = trans,cis (turn the molecule end to end)",
       "Distinct geometrical isomers = 3"],
      why_others_wrong="4 ignores the symmetry of the molecule. 2 counts only the all-cis and all-trans forms. 6 has "
                       "no basis.",
      seconds=75),

    N(T_GO, "Hybridisation and functional groups", "Advanced",
      "In penta-1,2-diene, CH₂=C=CH–CH₂–CH₃, the numbers of sp², sp and sp³ hybridised carbon atoms are, "
      "respectively:",
      ["3, 0 and 2", "2, 1 and 2", "2, 0 and 3", "1, 2 and 2"], "B", "2, 1 and 2",
      "Hybridisation from the number of π bonds",
      "A carbon with no π bond is sp³, one π bond sp², and two π bonds (two double bonds or one triple bond) sp. The "
      "central carbon of a C=C=C unit forms two π bonds.",
      ["C-1 (=CH₂): one π bond → sp²", "C-2 (=C=): two π bonds → sp", "C-3 (=CH–): one π bond → sp²",
       "C-4 and C-5: single bonds only → sp³", "sp² : sp : sp³ = 2 : 1 : 2"],
      why_others_wrong="'3, 0 and 2' treats the central carbon as sp², as if it formed only one double bond. The other "
                       "options misread the chain.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation", seconds=60),

    Q(T_GO, "Electronic effects", "Advanced", "assertion_reason",
      *ar("The two nitrogen–oxygen bonds in nitromethane, CH₃NO₂, have the same length.", True,
          "Nitromethane, CH₃–NO₂, and methyl nitrite, CH₃–O–N=O, have the same molecular formula.", True,
          explains=False),
      "Resonance versus isomerism",
      "Nitromethane is a resonance hybrid of two equivalent structures in which the N=O double bond and the N–O⁻ "
      "single bond exchange places; each N–O bond is therefore intermediate between a single and a double bond, and both are equal. "
      "That two different compounds share the formula CH₃NO₂ is a separate fact about isomerism.",
      ["A: two equivalent canonical structures → equal N–O bond lengths → true",
       "R: CH₃NO₂ and CH₃ONO are isomers (both CH₃NO₂) → true",
       "R says nothing about the bonding inside nitromethane → R does not explain A"],
      why_others_wrong="Option A is the trap: R is true, but the equal bond lengths are explained by resonance, not by "
                       "the existence of an isomer.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance structure", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "multi_statement",
      *ms("Which of the following IUPAC names are correct?",
          [("(CH₃)₂CH–CH₂–CH₂–OH: 3-methylbutan-1-ol", True),
           ("CH₃–CO–CH₂–COOH: 3-oxobutanoic acid", True),
           ("CH₃–CH(CH₃)–CH₂–CH₃: 3-methylbutane", False),
           ("CH₃–CH=CH–COOH: but-3-enoic acid", False),
           ("CH₃–CH(OH)–CH₂–CHO: 3-hydroxybutanal", True)],
          [["a", "c", "e"], ["b", "d", "e"], ["a", "b", "c"]], "D"),
      "IUPAC names of polyfunctional and branched compounds",
      "Choose the principal functional group (acid > aldehyde > ketone > alcohol), give it the lowest locant, and "
      "name the others as prefixes (oxo, hydroxy).",
      ["(a) OH on C-1, methyl on C-3 → 3-methylbutan-1-ol → true",
       "(b) COOH carbon is C-1; C=O at C-3 → 3-oxobutanoic acid → true",
       "(c) Lowest locants give 2-methylbutane → false",
       "(d) C-1 = COOH, double bond between C-2 and C-3 → but-2-enoic acid → false",
       "(e) CHO carbon is C-1; OH at C-3 → 3-hydroxybutanal → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=90),

    Q(T_GO, "Reactive intermediates", "Advanced", "direct",
      "In which of the following carbocations is the positive charge delocalised by resonance with a π bond?",
      ["CH₂=CH–CH₂–CH₂⁺", "CH₂=CH⁺", "CH₂=CH–CH₂⁺", "(CH₃)₃C⁺"], "C",
      "Resonance stabilisation of carbocations",
      "For resonance, the vacant p orbital of the positive carbon must be next to (conjugated with) a π bond. In the "
      "allyl cation the charge is shared by C-1 and C-3: CH₂=CH–CH₂⁺ ↔ ⁺CH₂–CH=CH₂.",
      ["CH₂=CH–CH₂–CH₂⁺: a CH₂ separates C⁺ from the π bond → no conjugation",
       "CH₂=CH⁺: the charge sits on a doubly bonded carbon; its empty orbital is not part of the π system",
       "CH₂=CH–CH₂⁺: allylic → two equivalent resonance structures",
       "(CH₃)₃C⁺: stabilised by hyperconjugation and +I, not by resonance with a π bond"],
      why_others_wrong="(CH₃)₃C⁺ is stable, but through hyperconjugation; the homoallyl and vinyl cations have no "
                       "conjugation of the empty p orbital with a π bond.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', carbocations and resonance",
      seconds=60),
]


# ================================================================ Hydrocarbons (430-443)
# 432: C2H2 + 2H2 -> C2H6 ; 2.6 g ethyne
m_c2h2 = mm(C=2, H=2)
vol_h2 = F(26, 10) / m_c2h2 * 2 * F(224, 10)
assert m_c2h2 == 26 and vol_h2 == F(448, 100) and F(26, 10) / 26 * F(224, 10) == F(224, 100)
# 434: Wurtz 2C2H5Br + 2Na -> C4H10 ; 21.8 g bromoethane (109)
m_etbr, m_but = mm(C=2, H=5, Br=1), mm(C=4, H=10)
mass_but = F(218, 10) / m_etbr / 2 * m_but
assert m_etbr == 109 and m_but == 58 and mass_but == F(58, 10)
assert F(218, 10) / m_etbr * m_but == F(116, 10) and F(218, 10) / m_etbr / 2 * mm(C=2, H=6) == 3
# 435: buta-1,3-diene has two C=C -> 2 Br2 per molecule
mass_br2 = F(1, 10) * 2 * (2 * BR)
assert mass_br2 == 32 and F(1, 10) * 160 == 16
# 440: CxHy + (x + y/4) O2 -> x CO2 + y/2 H2O ; 10 mL hydrocarbon, 55 mL O2, 40 mL CO2
x = F(40, 10)
y = (F(55, 10) - x) * 4
assert (x, y) == (4, 6)
assert [4 + F(h, 4) for h in (8, 10, 4)] == [6, F(13, 2), 5]  # O2 per volume for C4H8, C4H10, C4H4
# 441: Hueckel: planar, cyclic, fully conjugated, (4n + 2) pi electrons
species = {"benzene": (True, 6), "cyclopentadienyl anion": (True, 6), "cyclopentadiene": (False, 4),
           "tropylium cation": (True, 6), "cyclooctatetraene": (False, 8), "cyclobutadiene": (True, 4)}
huckel = lambda n: n >= 2 and (n - 2) % 4 == 0
assert sum(1 for conj, n in species.values() if conj and huckel(n)) == 3

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "An aqueous solution of sodium ethanoate (sodium acetate) is electrolysed (Kolbe's electrolytic method). The "
      "hydrocarbon formed at the anode is:",
      ["Methane", "Ethane", "Ethene", "Butane"], "B",
      "Kolbe's electrolytic method",
      "At the anode the carboxylate ion loses an electron and then CO₂, giving a methyl free radical. Two methyl "
      "radicals join to form ethane.",
      ["2CH₃COO⁻ → 2CH₃COO• + 2e⁻", "2CH₃COO• → 2CH₃• + 2CO₂", "CH₃• + CH₃• → CH₃–CH₃ (ethane)"],
      why_others_wrong="Methane comes from heating sodium ethanoate with soda lime, not electrolysis. Butane would "
                       "need sodium propanoate.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes (Kolbe's electrolytic method)", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "direct",
      "Ethene is shaken with a cold, dilute, alkaline solution of KMnO₄ (Baeyer's reagent). The organic product is:",
      ["Ethanal", "Ethanoic acid", "Ethanol", "Ethane-1,2-diol"], "D",
      "Oxidation of alkenes with cold dilute KMnO₄",
      "Cold, dilute, alkaline permanganate adds two –OH groups across the double bond, forming a vicinal glycol, and "
      "its pink colour disappears. This is a test for unsaturation.",
      ["CH₂=CH₂ + H₂O + [O] → HOCH₂–CH₂OH (ethane-1,2-diol)"],
      why_others_wrong="Ethanal and ethanoic acid would need cleavage or stronger oxidation; ethanol needs addition "
                       "of water, not oxidation.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkenes (oxidation)", seconds=25),

    N(T_HC, "Alkynes", "Basic",
      "The volume of hydrogen, measured at STP, needed to convert 2.6 g of ethyne completely into ethane is "
      "(C = 12, H = 1; molar volume at STP = 22.4 L mol⁻¹):",
      ["4.48 L", "2.24 L", "8.96 L", "1.12 L"], "A", "4.48 L",
      "Stoichiometry of complete hydrogenation",
      "A triple bond takes up two molecules of H₂ to become a single bond.",
      ["HC≡CH + 2H₂ → CH₃–CH₃ (Ni, Pt or Pd)", "Moles of ethyne = 2.6/26 = 0.1 mol → H₂ = 0.2 mol",
       "Volume = 0.2 × 22.4 = 4.48 L"],
      why_others_wrong="2.24 L stops at ethene (one H₂). 8.96 L and 1.12 L double and halve the moles by mistake.",
      seconds=35),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "statement_pair",
      *sp("But-2-ene exists as cis and trans isomers.", True,
          "trans-But-2-ene is more polar than cis-but-2-ene.", False),
      "Geometrical isomers of alkenes and their polarity",
      "Each doubly bonded carbon of but-2-ene carries two different groups (H and CH₃), so cis and trans forms exist. "
      "In the trans form the two C–CH₃ bond dipoles cancel, so it is almost non-polar; the cis form has a net dipole.",
      ["Statement I: CH₃CH=CHCH₃ → cis and trans → true",
       "Statement II: the cis isomer is the polar one; trans is (nearly) non-polar → false"],
      ncert=f"{NC11}, 'Hydrocarbons', isomerism in alkenes", seconds=35),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "21.8 g of bromoethane is treated with sodium in dry ether (Wurtz reaction). Assuming complete conversion to "
      "the coupling product, the mass of alkane formed is (C = 12, H = 1, Br = 80):",
      ["11.6 g", "2.9 g", "5.8 g", "3.0 g"], "C", "5.8 g",
      "Wurtz reaction stoichiometry",
      "Two molecules of alkyl halide join to give one molecule of an alkane with twice as many carbon atoms.",
      ["2CH₃CH₂Br + 2Na → CH₃CH₂CH₂CH₃ + 2NaBr",
       "Moles of C₂H₅Br = 21.8/109 = 0.2 mol → butane = 0.1 mol",
       "Mass = 0.1 × 58 = 5.8 g"],
      why_others_wrong="11.6 g takes one butane per bromoethane. 2.9 g halves the moles twice. 3.0 g assumes ethane "
                       "is formed.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes (Wurtz reaction)", seconds=50),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "The mass of bromine that adds to 0.1 mol of buta-1,3-diene, CH₂=CH–CH=CH₂, until the compound is fully "
      "saturated is (Br = 80):",
      ["16 g", "32 g", "8 g", "64 g"], "B", "32 g",
      "Addition of bromine to each double bond",
      "Each C=C adds one molecule of Br₂. Buta-1,3-diene has two C=C bonds.",
      ["CH₂=CH–CH=CH₂ + 2Br₂ → CH₂Br–CHBr–CHBr–CH₂Br", "Moles of Br₂ = 0.1 × 2 = 0.2 mol",
       "Mass = 0.2 × 160 = 32 g"],
      why_others_wrong="16 g saturates only one double bond. 8 g uses 80 g mol⁻¹ (atomic Br) for one bond. 64 g "
                       "counts four double bonds.",
      seconds=40),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "direct",
      "HBr is added to 2-methylpropene in the absence of peroxide. The major product is:",
      ["2-Bromo-2-methylpropane", "1-Bromo-2-methylpropane", "2-Bromobutane", "1-Bromobutane"], "A",
      "Markovnikov's rule",
      "H⁺ adds first to give the more stable carbocation. Adding H to the CH₂ end of (CH₃)₂C=CH₂ gives the tertiary "
      "carbocation (CH₃)₃C⁺, which then takes up Br⁻.",
      ["(CH₃)₂C=CH₂ + H⁺ → (CH₃)₃C⁺ (3°, more stable than the 1° alternative)",
       "(CH₃)₃C⁺ + Br⁻ → (CH₃)₃CBr = 2-bromo-2-methylpropane"],
      why_others_wrong="1-Bromo-2-methylpropane is the anti-Markovnikov product (needs peroxide). The butane "
                       "derivatives have a different carbon skeleton.",
      ncert=f"{NC11}, 'Hydrocarbons', addition of hydrogen halides (Markovnikov's rule)", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "assertion_reason",
      *ar("Nitration of benzene is carried out with a mixture of concentrated nitric acid and concentrated sulphuric "
          "acid.", True,
          "In this mixture, sulphuric acid itself is the electrophile that attacks the benzene ring.", False),
      "Generation of the electrophile in nitration",
      "Sulphuric acid protonates nitric acid, which then loses water to give the nitronium ion NO₂⁺. NO₂⁺ is the "
      "electrophile; H₂SO₄ only helps to produce it.",
      ["A: the nitrating mixture is conc. HNO₃ + conc. H₂SO₄ → true",
       "HNO₃ + 2H₂SO₄ ⇌ NO₂⁺ + H₃O⁺ + 2HSO₄⁻",
       "R: the electrophile is NO₂⁺, not H₂SO₄ → false"],
      ncert=f"{NC11}, 'Hydrocarbons', mechanism of electrophilic substitution", seconds=35),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "match_list",
      *ml("Match the reaction of benzene in List-I with its main product in List-II.",
          ["Cl₂, anhydrous FeCl₃, dark", "CH₃COCl, anhydrous AlCl₃", "Fuming sulphuric acid (oleum)",
           "H₂, Ni, heat and pressure"],
          ["Benzenesulphonic acid", "Cyclohexane", "Chlorobenzene", "Acetophenone"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "III", "B": "I", "C": "IV", "D": "II"}], "B"),
      "Substitution and addition reactions of benzene",
      "Halogenation, Friedel–Crafts acylation and sulphonation are electrophilic substitutions. Benzene adds hydrogen "
      "only under forcing conditions.",
      ["Cl₂/FeCl₃ → chlorobenzene → III", "CH₃COCl/AlCl₃ → acetophenone (C₆H₅COCH₃) → IV",
       "Oleum → C₆H₅SO₃H → I", "H₂/Ni → C₆H₁₂ → II"],
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of benzene", seconds=40),

    Q(T_HC, "Alkynes", "Intermediate", "multi_statement",
      *ms("Which of the following statements about ethyne and the alkynes are correct?",
          [("Ethyne is a linear molecule with an H–C–C bond angle of 180°.", True),
           ("The C≡C bond length in ethyne is 154 pm.", False),
           ("Ethyne is prepared by the action of water on calcium carbide.", True),
           ("Vicinal dihalides on treatment with alcoholic KOH, followed by sodamide, give alkynes.", True),
           ("Each carbon of ethyne has two unhybridised p orbitals, which form two π bonds perpendicular to each "
            "other.", True)],
          [["a", "b", "c"], ["a", "c", "d"], ["b", "d", "e"]], "D"),
      "Structure and preparation of alkynes",
      "Each carbon of ethyne is sp hybridised. The C≡C bond (one σ, two π) is 120 pm long, much shorter than a C–C "
      "single bond (154 pm).",
      ["(a) sp carbons → linear, 180° → true", "(b) C≡C is 120 pm; 154 pm is the C–C single bond → false",
       "(c) CaC₂ + 2H₂O → Ca(OH)₂ + C₂H₂ → true",
       "(d) Two successive dehydrohalogenations form the triple bond → true",
       "(e) Two π bonds from two pairs of p orbitals at right angles → true"],
      ncert=f"{NC11}, 'Hydrocarbons', alkynes (structure and preparation)", seconds=70),

    N(T_HC, "Alkanes and conformations", "Advanced",
      "10 mL of a gaseous hydrocarbon needs exactly 55 mL of oxygen for complete combustion and gives 40 mL of CO₂, "
      "all volumes measured at the same temperature and pressure. The formula of the hydrocarbon is:",
      ["C₄H₈", "C₄H₁₀", "C₄H₆", "C₄H₄"], "C", "C₄H₆",
      "Finding a formula from combustion volumes",
      "For CₓHᵧ + (x + y/4) O₂ → x CO₂ + (y/2) H₂O, gas volumes at the same T and P are in the mole ratio.",
      ["CO₂: 10x = 40 → x = 4", "O₂: 10(x + y/4) = 55 → x + y/4 = 5.5 → y/4 = 1.5 → y = 6",
       "Formula C₄H₆ (for example buta-1,3-diene or a butyne)"],
      why_others_wrong="C₄H₈ would need 60 mL of O₂, C₄H₁₀ 65 mL and C₄H₄ 50 mL.",
      seconds=100),

    N(T_HC, "Benzene and aromaticity", "Advanced",
      "How many of the following species are aromatic according to Hückel's rule?\n"
      "Benzene, cyclopentadienyl anion, cyclopenta-1,3-diene, tropylium (cycloheptatrienyl) cation, "
      "cyclooctatetraene, cyclobutadiene",
      ["3", "4", "2", "5"], "A", "3",
      "Hückel's rule",
      "An aromatic species is planar and cyclic, has a closed ring of conjugated p orbitals, and holds (4n + 2) π "
      "electrons.",
      ["Benzene: 6 π, fully conjugated → aromatic",
       "Cyclopentadienyl anion: 6 π (two C=C + lone pair), fully conjugated → aromatic",
       "Cyclopenta-1,3-diene: one sp³ CH₂ breaks the conjugation → not aromatic",
       "Tropylium cation: 6 π over 7 carbons → aromatic",
       "Cyclooctatetraene: 8 π, and the ring is not planar → not aromatic",
       "Cyclobutadiene: 4 π (4n) → not aromatic", "Aromatic: 3"],
      why_others_wrong="4 usually counts cyclooctatetraene or cyclopentadiene. 2 misses one of the ionic species.",
      ncert=f"{NC11}, 'Hydrocarbons', aromaticity (Hückel rule)", seconds=90),

    Q(T_HC, "Alkanes and conformations", "Advanced", "multi_statement",
      *ms("Which of the following statements about the conformations of ethane are correct?",
          [("Rotation about the C–C single bond in ethane is completely free, with no energy barrier.", False),
           ("The energy difference between the staggered and eclipsed conformations is about 12.5 kJ mol⁻¹.", True),
           ("The staggered and eclipsed conformations of ethane can be separated and isolated at room temperature.",
            False),
           ("In a Newman projection, the front carbon is shown as a point and the rear carbon as a circle.", True),
           ("Torsional strain is greatest in the eclipsed conformation.", True)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
      "Conformations of ethane",
      "Rotation about the C–C bond is hindered by a small energy barrier (torsional strain from the repulsion of "
      "bond pairs). The barrier is so small that the conformations interconvert rapidly and cannot be isolated.",
      ["(a) There is a barrier of about 12.5 kJ mol⁻¹ → false", "(b) Staggered is lower by about 12.5 kJ mol⁻¹ → true",
       "(c) They interconvert rapidly at room temperature → false",
       "(d) Newman projection: front C = point, rear C = circle → true",
       "(e) Eclipsed C–H bond pairs repel most → maximum torsional strain → true"],
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane", seconds=75),

    Q(T_HC, "Alkynes", "Advanced", "direct",
      "Propyne reacts with an excess of HBr (no peroxide). The final product is:",
      ["1,2-Dibromopropane", "1,1-Dibromopropane", "1,3-Dibromopropane", "2,2-Dibromopropane"], "D",
      "Two successive Markovnikov additions to an alkyne",
      "The first HBr adds by Markovnikov's rule to give 2-bromopropene. In the second addition, H goes to the CH₂ "
      "end and Br to C-2, where the carbocation is stabilised by the bromine already present. Both Br atoms end on "
      "the same carbon (a gem-dihalide).",
      ["CH₃–C≡CH + HBr → CH₃–CBr=CH₂", "CH₃–CBr=CH₂ + HBr → CH₃–CBr₂–CH₃ (2,2-dibromopropane)"],
      why_others_wrong="1,2-Dibromopropane forms from propene and Br₂, not from propyne and HBr. 1,1-Dibromopropane "
                       "is the anti-Markovnikov product. 1,3-Dibromopropane cannot form by addition.",
      ncert=f"{NC11}, 'Hydrocarbons', addition of hydrogen halides to alkynes", seconds=50),
]


# ================================================================ Organic Compounds Containing Halogens (444-453)
# 446: 2-bromobutane 2deg, 2-chloro-2-methylpropane 3deg, 1-bromopropane 1deg, bromocyclohexane 2deg, 2-iodopropane 2deg
cls = {"2-bromobutane": 2, "2-chloro-2-methylpropane": 3, "1-bromopropane": 1, "bromocyclohexane": 2,
       "2-iodopropane": 2}
assert sum(1 for v in cls.values() if v == 2) == 3
# 447: C2H5Br + KCN -> C2H5CN (propanenitrile, 55)
m_etcn = mm(C=3, H=5, N=1)
assert m_etcn == 55 and F(109, 10) / 109 * m_etcn == F(55, 10) and mm(C=2, H=3, N=1) == 41
# 451: SN2 rate = k[RX][OH-]
assert 3 * 2 == 6 and 3 ** 2 == 9 and 3 + 2 == 5

QUESTIONS += [
    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "Which reagent is preferred for converting an alcohol into an alkyl chloride, because both by-products are "
      "gases that escape and leave a fairly pure product?",
      ["Concentrated HCl with anhydrous ZnCl₂", "PCl₅", "SOCl₂", "PCl₃"], "C",
      "Preparation of alkyl chlorides from alcohols",
      "R–OH + SOCl₂ → R–Cl + SO₂↑ + HCl↑. Both SO₂ and HCl are gases, so the alkyl chloride is easy to obtain pure.",
      ["SOCl₂: by-products SO₂ and HCl (gases)", "PCl₅: by-product POCl₃ (liquid)", "PCl₃: by-product H₃PO₃",
       "HCl/ZnCl₂: water is formed and the mixture must be separated"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=25),

    Q(T_HX, "Polyhalogen compounds", "Basic", "direct",
      "Iodoform was used earlier as an antiseptic. Its antiseptic action is due to:",
      ["The liberation of free iodine", "Its sweet smell", "The CHI₃ molecule itself acting on microbes",
       "The liberation of phosgene"], "A",
      "Uses of iodoform",
      "NCERT states that the antiseptic property of iodoform is due to the iodine it liberates, not to iodoform "
      "itself. Because of its objectionable smell it has been replaced by other iodine-containing preparations.",
      ["Iodoform releases free I₂ when it is applied to a wound → antiseptic action"],
      why_others_wrong="Iodoform has an unpleasant smell, and phosgene is formed by the oxidation of chloroform, not "
                       "iodoform.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (iodoform)", seconds=25),

    N(T_HX, "C-X bond and preparation", "Basic",
      "How many of the following are secondary (2°) alkyl halides?\n"
      "2-Bromobutane, 2-chloro-2-methylpropane, 1-bromopropane, bromocyclohexane, 2-iodopropane",
      ["2", "3", "4", "1"], "B", "3",
      "Classification of alkyl halides",
      "The halide is 1°, 2° or 3° according to the number of carbon atoms bonded to the carbon that carries the "
      "halogen.",
      ["2-Bromobutane: C-2 bonded to 2 C → 2°", "2-Chloro-2-methylpropane: C-2 bonded to 3 C → 3°",
       "1-Bromopropane: C-1 bonded to 1 C → 1°", "Bromocyclohexane: ring CH bonded to 2 C → 2°",
       "2-Iodopropane: C-2 bonded to 2 C → 2°", "Secondary: 3"],
      why_others_wrong="4 counts 2-chloro-2-methylpropane, which is tertiary. 2 usually misses the cyclic halide.",
      seconds=35),

    N(T_HX, "SN1 and SN2", "Intermediate",
      "10.9 g of bromoethane is heated with an excess of ethanolic KCN. If the alkyl cyanide is the only organic "
      "product and the conversion is complete, its mass is (C = 12, H = 1, N = 14, Br = 80):",
      ["4.1 g", "2.75 g", "11.0 g", "5.5 g"], "D", "5.5 g",
      "Nucleophilic substitution by cyanide",
      "CN⁻ replaces Br⁻, and the product keeps the ethyl group: the nitrile has one more carbon than the halide.",
      ["CH₃CH₂Br + KCN → CH₃CH₂CN + KBr", "Moles = 10.9/109 = 0.1 mol",
       "Molar mass of CH₃CH₂CN = 36 + 5 + 14 = 55 g mol⁻¹ → mass = 5.5 g"],
      why_others_wrong="4.1 g is the mass of 0.1 mol of CH₃CN, which forgets that the ethyl group is kept. 2.75 g and "
                       "11.0 g halve and double the moles.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions", seconds=45),

    Q(T_HX, "SN1 and SN2", "Intermediate", "assertion_reason",
      *ar("Haloalkanes react with KCN to give alkyl cyanides as the main product, but with AgCN they give "
          "isocyanides as the main product.", True,
          "KCN is predominantly ionic and the cyanide ion attacks mainly through carbon, whereas AgCN is mainly "
          "covalent, so only the nitrogen atom is free to donate its electron pair.", True, explains=True),
      "Ambident nucleophile: cyanide",
      "CN⁻ can bond through C or N. Free CN⁻ from ionic KCN attacks through carbon, because the C–C bond formed is "
      "stronger than a C–N bond. In covalent AgCN the carbon is tied up with silver, so nitrogen attacks.",
      ["A: R–X + KCN → R–CN; R–X + AgCN → R–NC → true",
       "R: ionic KCN gives free CN⁻; covalent Ag–CN leaves only N free → true",
       "R is the reason given for the different products → R explains A"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution (ambident nucleophiles)", seconds=50),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "statement_pair",
      *sp("Haloalkanes are highly soluble in water because they form strong hydrogen bonds with water molecules.",
          False,
          "The density of chloro derivatives of methane increases with the number of chlorine atoms, so CCl₄ is "
          "denser than CH₂Cl₂.", True),
      "Physical properties of haloalkanes",
      "Haloalkanes are only very slightly soluble in water: the energy released by their weak attractions to water "
      "is less than the energy needed to break the hydrogen bonds between water molecules. Density rises with the "
      "number and mass of halogen atoms.",
      ["Statement I: haloalkanes cannot form strong hydrogen bonds with water and are only slightly soluble → false",
       "Statement II: density order CH₂Cl₂ < CHCl₃ < CCl₄ → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties", seconds=40),

    Q(T_HX, "SN1 and SN2", "Intermediate", "match_list",
      *ml("Match the reagent in List-I, reacting with a haloalkane R–X, with the main product in List-II.",
          ["Aqueous NaOH", "Sodium alkoxide, R′ONa", "Ammonia", "AgNO₂"],
          ["Ether", "Nitroalkane", "Alcohol", "Amine"],
          {"A": "III", "B": "I", "C": "IV", "D": "II"},
          [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
           {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C"),
      "Nucleophilic substitution products of haloalkanes",
      "The nucleophile replaces the halogen. NO₂⁻ is ambident: covalent AgNO₂ bonds through N and gives a "
      "nitroalkane, while KNO₂ gives an alkyl nitrite.",
      ["OH⁻ → R–OH (alcohol) → III", "R′O⁻ → R–O–R′ (ether) → I", "NH₃ → R–NH₂ (amine) → IV",
       "AgNO₂ → R–NO₂ (nitroalkane) → II"],
      why_others_wrong="A-I, B-III swaps alcohol and ether. C-II, D-IV makes ammonia give a nitro compound. B-IV, "
                       "C-I mixes up alkoxide and ammonia.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions", seconds=40),

    N(T_HX, "SN1 and SN2", "Advanced",
      "CH₃Br reacts with OH⁻ by the SN2 mechanism. If the concentration of CH₃Br is tripled and that of OH⁻ is "
      "doubled at the same temperature, the rate of the reaction increases by a factor of:",
      ["3", "6", "9", "5"], "B", "6",
      "Rate law of an SN2 reaction",
      "SN2 is a one-step bimolecular reaction, so the rate depends on the concentrations of both the alkyl halide "
      "and the nucleophile: rate = k[CH₃Br][OH⁻].",
      ["New rate / old rate = (3)(2) = 6"],
      why_others_wrong="3 treats the reaction as SN1 (rate independent of OH⁻). 9 squares the factor 3. 5 adds the "
                       "factors instead of multiplying them.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', mechanism of nucleophilic substitution (SN2)", seconds=45),

    Q(T_HX, "SN1 and SN2", "Advanced", "multi_statement",
      *ms("Which of the following statements about nucleophilic substitution of alkyl halides are correct?",
          [("The order of reactivity towards SN2 is CH₃Br > CH₃CH₂Br > (CH₃)₂CHBr > (CH₃)₃CBr.", True),
           ("For a given alkyl group, the reactivity of the halides is R–I > R–Br > R–Cl.", True),
           ("In an SN2 reaction, the bond to the incoming nucleophile forms as the bond to the leaving group breaks, "
            "in a single step.", True),
           ("In an SN1 reaction, the rate-determining step is the attack of the nucleophile on the carbocation.",
            False),
           ("Tertiary alkyl halides react fastest by the SN2 mechanism.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
      "Comparing SN1 and SN2",
      "SN2 needs backside attack, so bulky groups slow it down: methyl reacts fastest and tertiary slowest. In SN1 "
      "the slow step is the ionisation of R–X to the carbocation; the nucleophile then attacks quickly.",
      ["(a) Steric hindrance increases from CH₃ to 3° → SN2 rate falls → true",
       "(b) The C–X bond weakens from Cl to I → true",
       "(c) SN2 is concerted: one step, with a transition state → true",
       "(d) The slow step of SN1 is the loss of X⁻ to form the carbocation → false",
       "(e) Tertiary halides are the slowest by SN2 (they react by SN1) → false"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', mechanism of nucleophilic substitution", seconds=80),

    Q(T_HX, "C-X bond and preparation", "Advanced", "assertion_reason",
      *ar("Aryl halides cannot be prepared by treating phenols with HCl.", True,
          "The C–O bond in phenol has partial double bond character and is difficult to break.", True, explains=True),
      "Why phenols do not give aryl halides with HX",
      "In phenol, a lone pair of the oxygen is delocalised into the ring, so the C–O bond is stronger than a single "
      "bond. Replacing –OH by –X needs this bond to break, which does not happen with HX.",
      ["A: C₆H₅OH + HCl does not give C₆H₅Cl → true",
       "R: resonance gives the C(aryl)–O bond partial double bond character → true",
       "R is the reason NCERT gives for A → R explains A"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloarenes", seconds=40),
]


# ================================================================ Organic Compounds Containing Oxygen (454-470)
# 457: C6H5COONa + NaOH (CaO) -> C6H6 + Na2CO3 ; sodium benzoate 144
m_benzoate, m_benzene = mm(C=7, H=5, O=2, Na=1), mm(C=6, H=6)
assert m_benzoate == 144 and m_benzene == 78 and F(144, 10) / m_benzoate * m_benzene == F(78, 10)
assert F(144, 10) / m_benzoate * mm(C=7, H=8) == F(92, 10)
# 459: toluene (92) -> benzoic acid (122)
assert mm(C=7, H=8) == 92 and mm(C=7, H=6, O=2) == 122 and F(92, 10) / 92 * 122 == F(122, 10)
assert mm(C=7, H=6, O=1) == 106
# 460: 2HCHO + NaOH -> HCOONa + CH3OH ; 6.0 g HCHO
m_hcho, m_hcoona = mm(C=1, H=2, O=1), mm(C=1, H=1, O=2, Na=1)
mass_formate = F(6) / m_hcho / 2 * m_hcoona
assert m_hcho == 30 and m_hcoona == 68 and mass_formate == F(68, 10)
assert F(6) / m_hcho * m_hcoona == F(136, 10) and F(6) / m_hcho / 2 * mm(C=1, H=4, O=1) == F(32, 10)
assert F(6) / m_hcho / 2 * mm(C=1, H=2, O=2) == F(46, 10)
# 466: CH3COCH3 + 3I2 + 4NaOH -> CHI3 + CH3COONa + 3NaI + 3H2O ; 5.8 g propanone
m_acetone, m_chi3, m_i2 = mm(C=3, H=6, O=1), mm(C=1, H=1, I=3), 2 * I_
n_ac = F(58, 10) / m_acetone
assert m_acetone == 58 and m_chi3 == 394 and m_i2 == 254
assert (n_ac * m_chi3, n_ac * 3 * m_i2) == (F(394, 10), F(762, 10)) and n_ac * m_i2 == F(254, 10)
# 467: (CH3)2C(OH)CH2CH3 from CH3MgBr needs CH3COCH2CH3 (butanone, 72)
assert mm(C=4, H=8, O=1) == 72 and F(1, 10) * 72 == F(72, 10) and mm(C=5, H=12, O=1) == 88 and mm(C=5, H=10, O=1) == 86

QUESTIONS += [
    Q(T_OX, "Alcohols", "Basic", "direct",
      "Propene is treated with diborane, and the product is oxidised with H₂O₂ in aqueous NaOH "
      "(hydroboration–oxidation). The alcohol formed is:",
      ["Propan-2-ol", "Propanal", "Propan-1-ol", "Propane-1,2-diol"], "C",
      "Hydroboration–oxidation",
      "Boron adds to the less substituted carbon of the double bond, and is then replaced by –OH. The net result is "
      "addition of water opposite to Markovnikov's rule.",
      ["CH₃CH=CH₂ + (H–BH₂)₂ → (CH₃CH₂CH₂)₃B", "(CH₃CH₂CH₂)₃B + 3H₂O₂ (OH⁻) → 3CH₃CH₂CH₂OH + B(OH)₃"],
      why_others_wrong="Propan-2-ol is the Markovnikov product of acid-catalysed hydration. Propanal and the diol are "
                       "not formed in this reaction.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols (hydroboration–oxidation)", seconds=30),

    Q(T_OX, "Alcohols", "Basic", "direct",
      "Which reagent oxidises a primary alcohol to an aldehyde without further oxidation to the carboxylic acid?",
      ["Acidified KMnO₄", "Pyridinium chlorochromate (PCC)", "Excess acidified K₂Cr₂O₇ on heating", "LiAlH₄"], "B",
      "Controlled oxidation of primary alcohols",
      "PCC, a complex of chromium trioxide with pyridine and HCl, is a mild oxidising agent that stops at the "
      "aldehyde stage.",
      ["RCH₂OH + PCC → RCHO", "Strong oxidants (acidified KMnO₄, excess hot dichromate) carry the oxidation on to RCOOH"],
      why_others_wrong="LiAlH₄ is a reducing agent. The two strong oxidising agents give carboxylic acids.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols (oxidation)", seconds=25),

    Q(T_OX, "Phenols", "Basic", "direct",
      "Phenol is converted into benzene by heating it with:",
      ["Sodium", "Concentrated H₂SO₄", "Bromine water", "Zinc dust"], "D",
      "Reaction of phenol with zinc dust",
      "Zinc dust removes the oxygen of phenol: C₆H₅OH + Zn → C₆H₆ + ZnO.",
      ["C₆H₅OH + Zn → C₆H₆ + ZnO"],
      why_others_wrong="Sodium gives sodium phenoxide and H₂, conc. H₂SO₄ sulphonates the ring, and bromine water "
                       "gives 2,4,6-tribromophenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of phenol with zinc dust", seconds=20),

    N(T_OX, "Carboxylic acids", "Basic",
      "14.4 g of sodium benzoate is heated with soda lime until decarboxylation is complete. The mass of benzene "
      "formed is (C = 12, H = 1, O = 16, Na = 23):",
      ["9.2 g", "3.9 g", "7.8 g", "14.4 g"], "C", "7.8 g",
      "Decarboxylation of sodium salts of carboxylic acids",
      "Heating the sodium salt with soda lime (NaOH + CaO) removes CO₂ and gives a hydrocarbon with one carbon "
      "fewer than the acid.",
      ["C₆H₅COONa + NaOH → C₆H₆ + Na₂CO₃ (CaO, heat)", "Moles = 14.4/144 = 0.1 mol",
       "Mass of benzene = 0.1 × 78 = 7.8 g"],
      why_others_wrong="9.2 g is 0.1 mol of toluene, assuming no carbon is lost. 3.9 g halves the moles. 14.4 g "
                       "assumes the mass is unchanged.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', decarboxylation", seconds=40),

    Q(T_OX, "Ethers", "Basic", "statement_pair",
      *sp("In ethers, the C–O–C bond angle is slightly greater than the tetrahedral angle, because of repulsion "
          "between the two bulky alkyl groups.", True,
          "Lower ethers such as methoxymethane are completely immiscible with water.", False),
      "Structure and solubility of ethers",
      "In methoxymethane the C–O–C angle is about 111.7°. Ether oxygen can accept hydrogen bonds from water, so "
      "the miscibility of lower ethers with water is similar to that of alcohols of about the same mass.",
      ["Statement I: bond angle about 111.7° > 109.5° → true",
       "Statement II: lower ethers form hydrogen bonds with water and are miscible to a similar extent as "
       "alcohols → false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', structure and physical properties of ethers", seconds=35),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "9.2 g of toluene is oxidised completely with alkaline KMnO₄, and the mixture is then acidified. The mass of "
      "the aromatic acid formed is (C = 12, H = 1, O = 16):",
      ["10.6 g", "9.2 g", "24.4 g", "12.2 g"], "D", "12.2 g",
      "Side-chain oxidation of alkylbenzenes",
      "Vigorous oxidation converts the whole alkyl side chain into –COOH, so toluene gives benzoic acid, mole for "
      "mole.",
      ["C₆H₅CH₃ → C₆H₅COOH (KMnO₄–KOH, then H₃O⁺)", "Moles of toluene = 9.2/92 = 0.1 mol",
       "Mass of benzoic acid = 0.1 × 122 = 12.2 g"],
      why_others_wrong="10.6 g is 0.1 mol of benzaldehyde, which is not the end product of vigorous oxidation. 9.2 g "
                       "ignores the change in molar mass. 24.4 g doubles the moles.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of carboxylic acids from alkylbenzenes",
      seconds=45),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "6.0 g of methanal undergoes the Cannizzaro reaction completely with concentrated NaOH. The mass of sodium "
      "methanoate formed is (C = 12, H = 1, O = 16, Na = 23):",
      ["6.8 g", "13.6 g", "3.2 g", "4.6 g"], "A", "6.8 g",
      "Cannizzaro reaction stoichiometry",
      "Two molecules of an aldehyde with no α-hydrogen react: one is oxidised to the carboxylate salt, the other is "
      "reduced to the alcohol.",
      ["2HCHO + NaOH (conc.) → HCOONa + CH₃OH", "Moles of HCHO = 6.0/30 = 0.2 mol → HCOONa = 0.1 mol",
       "Mass = 0.1 × 68 = 6.8 g"],
      why_others_wrong="13.6 g assumes every HCHO becomes HCOONa. 3.2 g is the mass of methanol formed. 4.6 g is the "
                       "mass of free methanoic acid.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Cannizzaro reaction", seconds=50),

    Q(T_OX, "Phenols", "Intermediate", "direct",
      "In the industrial preparation of phenol from cumene, cumene is oxidised in air to cumene hydroperoxide, which "
      "is then treated with dilute acid. The products are:",
      ["Benzene and ethanol", "Phenol and propanone", "Benzoic acid and methanol", "Phenol and propan-2-ol"], "B",
      "Cumene process",
      "Cumene (isopropylbenzene) hydroperoxide splits in dilute acid into phenol and acetone; acetone is a valuable "
      "by-product.",
      ["C₆H₅CH(CH₃)₂ + O₂ → C₆H₅C(CH₃)₂OOH", "C₆H₅C(CH₃)₂OOH → (H⁺, H₂O) → C₆H₅OH + CH₃COCH₃"],
      why_others_wrong="The three-carbon fragment leaves as propanone, not propan-2-ol, and the ring keeps the "
                       "oxygen as phenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of phenols (from cumene)", seconds=30),

    Q(T_OX, "Alcohols", "Intermediate", "assertion_reason",
      *ar("When the vapour of 2-methylpropan-2-ol is passed over heated copper at 573 K, 2-methylpropene is formed "
          "instead of a carbonyl compound.", True,
          "In a tertiary alcohol, the carbon carrying the –OH group has no hydrogen atom, so dehydrogenation to a "
          "carbonyl compound is not possible.", True, explains=True),
      "Dehydrogenation of alcohols over copper",
      "Over hot copper, primary and secondary alcohols lose H₂ (one H from O and one from the carbinol carbon) to "
      "give aldehydes and ketones. A tertiary alcohol has no H on the carbinol carbon, so it loses water instead.",
      ["Primary → aldehyde; secondary → ketone (dehydrogenation)",
       "(CH₃)₃C–OH has no C–H on the carbinol carbon → dehydration → (CH₃)₂C=CH₂",
       "A and R are both true, and R explains A"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', dehydrogenation of alcohols", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Benzaldehyde does not give a red precipitate with Fehling's solution.", True,
          "Ketones are oxidised only by strong oxidising agents at elevated temperatures, with cleavage of "
          "carbon–carbon bonds.", True),
      "Oxidation of aldehydes and ketones",
      "Aliphatic aldehydes reduce Fehling's solution, but aromatic aldehydes do not respond to this test. Ketones "
      "resist mild oxidants; vigorous oxidation breaks a C–C bond next to the carbonyl group and gives a mixture of "
      "carboxylic acids with fewer carbon atoms.",
      ["Statement I: aromatic aldehydes do not respond to Fehling's test → true",
       "Statement II: vigorous oxidation of ketones cleaves C–C bonds → true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', oxidation of aldehydes and ketones", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with the main organic product in List-II.",
          ["Propanone + NH₂OH (weakly acidic)", "Propanone + NH₂NH₂, then KOH in ethylene glycol, heat",
           "Ethanal + excess CH₃OH, dry HCl gas", "Ethanoic acid + NH₃, then strong heating"],
          ["Propane", "Ethanamide", "Propanone oxime", "1,1-Dimethoxyethane (an acetal)"],
          {"A": "III", "B": "I", "C": "IV", "D": "II"},
          [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
           {"A": "III", "B": "IV", "C": "I", "D": "II"}], "D"),
      "Reactions of carbonyl compounds and carboxylic acids",
      "Ammonia derivatives condense with C=O. The hydrazone heated with KOH loses N₂ (Wolff–Kishner), reducing C=O "
      "to CH₂. Excess alcohol with dry HCl converts an aldehyde into an acetal. Ammonium ethanoate loses water on "
      "strong heating to give the amide.",
      ["A: (CH₃)₂C=N–OH → III", "B: (CH₃)₂C=O → CH₃CH₂CH₃ (Wolff–Kishner) → I",
       "C: CH₃CH(OCH₃)₂ → IV", "D: CH₃COONH₄ → CH₃CONH₂ + H₂O → II"],
      why_others_wrong="A-I, B-III swaps the oxime and the fully reduced product. C-II, D-IV gives the amide from the "
                       "aldehyde. B-IV, C-I makes the acetal reaction a reduction.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions", seconds=50),

    Q(T_OX, "Phenols", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Oxidation of phenol with chromic acid gives benzoquinone.", True),
           ("Phenol reacts with aqueous NaOH to form sodium phenoxide.", True),
           ("Phenol liberates CO₂ from aqueous sodium hydrogencarbonate.", False),
           ("Ethanol reacts with aqueous NaOH to form sodium ethoxide.", False),
           ("Acidified KMnO₄ oxidises a primary alcohol directly to a carboxylic acid.", True)],
          [["a", "c", "e"], ["b", "c", "d"], ["a", "b", "d"]], "B"),
      "Acidity and oxidation of alcohols and phenols",
      "Phenol is acidic enough to react with NaOH but is a weaker acid than carbonic acid, so it does not "
      "decompose NaHCO₃. Alcohols are weaker acids than water and do not form alkoxides with aqueous NaOH.",
      ["(a) C₆H₅OH + Na₂Cr₂O₇/H₂SO₄ → p-benzoquinone → true",
       "(b) C₆H₅OH + NaOH → C₆H₅ONa + H₂O → true",
       "(c) Phenol is too weak an acid to release CO₂ from NaHCO₃ → false",
       "(d) Ethanol does not form ethoxide with aqueous NaOH (it needs Na metal) → false",
       "(e) Strong oxidising agents give carboxylic acids directly → true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols and phenols", seconds=70),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "5.8 g of propanone is warmed with iodine and aqueous NaOH until the iodoform reaction is complete:\n"
      "CH₃COCH₃ + 3I₂ + 4NaOH → CHI₃ + CH₃COONa + 3NaI + 3H₂O\n"
      "The mass of iodoform formed and the mass of iodine consumed are, respectively (C = 12, H = 1, O = 16, "
      "I = 127):",
      ["39.4 g and 25.4 g", "19.7 g and 76.2 g", "39.4 g and 76.2 g", "39.4 g and 50.8 g"], "C",
      "39.4 g and 76.2 g",
      "Stoichiometry of the haloform reaction",
      "One mole of propanone gives one mole of CHI₃ and uses three moles of I₂, because all three H atoms of the "
      "methyl group are replaced by iodine.",
      ["Moles of propanone = 5.8/58 = 0.1 mol",
       "CHI₃ = 0.1 mol × 394 = 39.4 g",
       "I₂ = 0.3 mol × 254 = 76.2 g"],
      why_others_wrong="25.4 g uses one I₂ per propanone. 50.8 g uses two. 19.7 g halves the iodoform.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', haloform reaction", seconds=100),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "A ketone reacts with CH₃MgBr, and the adduct is hydrolysed, giving 2-methylbutan-2-ol, (CH₃)₂C(OH)CH₂CH₃. "
      "The mass of ketone needed to obtain 0.1 mol of this alcohol (100% yield) is (C = 12, H = 1, O = 16):",
      ["5.8 g", "8.8 g", "8.6 g", "7.2 g"], "D", "7.2 g",
      "Working back from a Grignard product",
      "The Grignard reagent adds its CH₃ group to the carbonyl carbon, which becomes the carbinol carbon. Removing "
      "one CH₃ from that carbon and restoring C=O gives the ketone.",
      ["Carbinol carbon of the product carries CH₃, CH₃ and C₂H₅",
       "One CH₃ came from CH₃MgBr → ketone = CH₃–CO–C₂H₅ (butanone, C₄H₈O, 72 g mol⁻¹)",
       "Mass = 0.1 × 72 = 7.2 g"],
      why_others_wrong="5.8 g is propanone, which would need C₂H₅MgBr. 8.8 g is the mass of the alcohol itself. "
                       "8.6 g is a C₅ ketone, which would give a C₆ alcohol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols from Grignard reagents", seconds=90),

    Q(T_OX, "Carboxylic acids", "Advanced", "assertion_reason",
      *ar("Benzoic acid does not undergo the Friedel–Crafts reaction.", True,
          "The –COOH group is an ortho–para directing, ring-activating group.", False),
      "Electrophilic substitution in aromatic acids",
      "The carboxyl group withdraws electrons from the ring (deactivating, meta-directing), and the Lewis acid "
      "catalyst AlCl₃ gets bonded to the carboxyl group. Both stop the Friedel–Crafts reaction.",
      ["A: true (NCERT)", "R: –COOH is deactivating and meta-directing → false"],
      why_others_wrong="If –COOH were activating, the Friedel–Crafts reaction would go more easily, so R cannot "
                       "explain A even in principle.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', substitution reactions in the ring", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following methods give the stated carbonyl compound?",
          [("Passing the vapour of a primary alcohol over heated copper at 573 K gives an aldehyde.", True),
           ("Reducing a nitrile with diisobutylaluminium hydride (DIBAL-H), followed by hydrolysis, gives an "
            "aldehyde.", True),
           ("Treating an acyl chloride with a dialkylcadmium gives a ketone.", True),
           ("Oxidising a primary alcohol with PCC gives a ketone.", False),
           ("Reducing a carboxylic acid with LiAlH₄ gives an aldehyde.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Preparation of aldehydes and ketones",
      "Each method is a controlled oxidation or reduction that stops at the carbonyl level, or a carbon–carbon bond "
      "formation that makes a ketone.",
      ["(a) RCH₂OH → RCHO + H₂ (Cu, 573 K) → true",
       "(b) R–C≡N → R–CH=NH → RCHO (DIBAL-H, then H₂O) → true",
       "(c) 2R′COCl + R₂Cd → 2R′COR + CdCl₂ → true",
       "(d) PCC gives an aldehyde from a primary alcohol, not a ketone → false",
       "(e) LiAlH₄ reduces RCOOH all the way to RCH₂OH → false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes and ketones", seconds=80),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "direct",
      "Ethanol is oxidised with PCC to give X. X is treated with dilute NaOH to give Y, and Y is heated to give Z. "
      "Z is:",
      ["Butanal", "But-2-enal", "3-Hydroxybutanal", "Butan-1-ol"], "B",
      "Aldol condensation in a reaction sequence",
      "PCC stops at the aldehyde. Ethanal has α-hydrogens, so dilute alkali gives the aldol, which loses water on "
      "heating to give the α,β-unsaturated aldehyde.",
      ["X: CH₃CH₂OH → CH₃CHO (ethanal)", "Y: 2CH₃CHO → CH₃CH(OH)CH₂CHO (3-hydroxybutanal, the aldol)",
       "Z: CH₃CH(OH)CH₂CHO → CH₃CH=CHCHO + H₂O (but-2-enal)"],
      why_others_wrong="3-Hydroxybutanal is Y, not Z. Butanal and butan-1-ol would need a reduction step that is not "
                       "in the sequence.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol condensation", seconds=60),
]


# ================================================================ Organic Compounds Containing Nitrogen (471-480)
# 473: nitrobenzene (123) -> aniline (93)
m_pno2, m_anil = mm(C=6, H=5, N=1, O=2), mm(C=6, H=7, N=1)
assert m_pno2 == 123 and m_anil == 93 and F(123, 10) / m_pno2 * m_anil == F(93, 10)
# 475: aniline + 3Br2 -> 2,4,6-tribromoaniline (330)
m_tba = mm(C=6, H=4, Br=3, N=1)
assert m_tba == 330 and F(93, 100) / m_anil * m_tba == F(330, 100)
assert mm(C=6, H=6, Br=1, N=1) == 172 and mm(C=6, H=5, Br=2, N=1) == 251
# 478: C6H5NH2 + NaNO2 + 2HCl -> C6H5N2Cl + NaCl + 2H2O ; 9.3 g aniline
n_an = F(93, 10) / m_anil
assert n_an == F(1, 10) and n_an * mm(Na=1, N=1, O=2) == F(69, 10) and n_an * 2 == F(2, 10)
# 480: pKb values (NCERT table): lower pKb = stronger base
pkb = {"(C2H5)2NH": 3.00, "(C2H5)3N": 3.25, "C2H5NH2": 3.29, "C6H5NH2": 9.38}
assert sorted(pkb, key=pkb.get) == ["(C2H5)2NH", "(C2H5)3N", "C2H5NH2", "C6H5NH2"]

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Which of the following is a secondary (2°) amine?",
      ["(CH₃)₃C–NH₂", "(CH₃)₃N", "CH₃–NH–C₂H₅", "C₆H₅–NH₂"], "C",
      "Classification of amines",
      "Amines are classed by the number of hydrogen atoms of NH₃ replaced by alkyl or aryl groups, that is, by the "
      "number of carbon groups on the nitrogen atom, not by the type of carbon atom.",
      ["(CH₃)₃C–NH₂: one carbon group on N → primary (even though the carbon is tertiary)",
       "(CH₃)₃N: three groups on N → tertiary", "CH₃–NH–C₂H₅: two groups on N → secondary",
       "C₆H₅NH₂: one group on N → primary"],
      why_others_wrong="tert-Butylamine is the trap: the 'tertiary' refers to its carbon, but the amine is primary.",
      ncert=f"{NC12}, 'Amines', classification of amines", seconds=25),

    Q(T_NI, "Diazonium salts", "Basic", "statement_pair",
      *sp("Benzenediazonium chloride reacts with phenol in mildly alkaline medium to give p-hydroxyazobenzene, an "
          "orange dye.", True,
          "In this coupling reaction, the diazonium ion acts as an electrophile and attacks the para position of "
          "the phenoxide ion.", True),
      "Coupling reactions of diazonium salts",
      "The terminal nitrogen of ArN₂⁺ is electron-poor; it attacks the electron-rich para position of the "
      "phenoxide ion (electrophilic substitution), forming an –N=N– (azo) link.",
      ["Statement I: C₆H₅N₂⁺Cl⁻ + C₆H₅O⁻ → p-HO–C₆H₄–N=N–C₆H₅ (orange) → true",
       "Statement II: coupling is electrophilic substitution with ArN₂⁺ as the electrophile → true"],
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts (coupling reactions)", seconds=35),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "12.3 g of nitrobenzene is reduced completely with Sn and HCl, and the product is made alkaline to free the "
      "amine. The mass of aniline obtained is (C = 12, H = 1, N = 14, O = 16):",
      ["12.3 g", "9.3 g", "4.65 g", "18.6 g"], "B", "9.3 g",
      "Mole-to-mole conversion in the reduction of a nitro group",
      "Each nitrobenzene molecule gives one aniline molecule.",
      ["Moles of C₆H₅NO₂ = 12.3/123 = 0.1 mol", "Mass of C₆H₅NH₂ = 0.1 × 93 = 9.3 g"],
      why_others_wrong="12.3 g ignores the change in molar mass. 4.65 g and 18.6 g halve and double the moles.",
      seconds=30),

    Q(T_NI, "Diazonium salts", "Intermediate", "direct",
      "Benzenediazonium chloride is treated with hypophosphorous acid (H₃PO₂) and water. The organic product is:",
      ["Phenol", "Chlorobenzene", "Aniline", "Benzene"], "D",
      "Replacement of the diazo group by hydrogen",
      "Mild reducing agents such as hypophosphorous acid (or ethanol) replace –N₂⁺ by –H, with loss of N₂.",
      ["C₆H₅N₂⁺Cl⁻ + H₃PO₂ + H₂O → C₆H₆ + N₂ + H₃PO₃ + HCl"],
      why_others_wrong="Phenol forms on warming with water alone, and chlorobenzene with CuCl/HCl. The diazo group "
                       "is not reduced back to –NH₂.",
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts (replacement by hydrogen)", seconds=30),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "0.93 g of aniline is treated with excess bromine water at room temperature. The mass of the white precipitate "
      "formed is (C = 12, H = 1, N = 14, Br = 80):",
      ["3.30 g", "1.72 g", "2.51 g", "9.90 g"], "A", "3.30 g",
      "Bromination of aniline",
      "The –NH₂ group activates the ring so strongly that bromine water substitutes all the ortho and para "
      "positions at once, giving 2,4,6-tribromoaniline.",
      ["C₆H₅NH₂ + 3Br₂ → C₆H₂Br₃NH₂ + 3HBr", "Moles of aniline = 0.93/93 = 0.01 mol",
       "Molar mass of C₆H₄Br₃N = 72 + 4 + 240 + 14 = 330 g mol⁻¹ → mass = 3.30 g"],
      why_others_wrong="1.72 g and 2.51 g assume mono- and dibromination. 9.90 g multiplies by the three Br₂ "
                       "molecules used.",
      ncert=f"{NC12}, 'Amines', electrophilic substitution (bromination of aniline)", seconds=50),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("To prepare p-nitroaniline as the main product, aniline is first acetylated and the acetanilide formed is "
          "nitrated, followed by hydrolysis.", True,
          "Acetylation reduces the activating effect of the –NH₂ group and protects it from oxidation and "
          "protonation during nitration.", True, explains=True),
      "Controlling the reactivity of aniline",
      "Direct nitration of aniline gives tarry oxidation products and, because the anilinium ion is formed in the "
      "acid, a large amount of the meta product. In –NHCOCH₃ the nitrogen lone pair is shared with the C=O group, "
      "so the group is only moderately activating and still ortho/para directing.",
      ["A: acetylation → nitration → hydrolysis gives mainly p-nitroaniline → true",
       "R: –NHCOCH₃ is less activating and is not protonated or oxidised → true",
       "R is why the acetyl step is used → R explains A"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution (nitration of aniline)", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the reaction or test in List-I with the reagent it uses in List-II.",
          ["Gabriel phthalimide synthesis", "Carbylamine test", "Hinsberg's test", "Gattermann reaction"],
          ["Benzenesulphonyl chloride", "Copper powder and HCl, with a diazonium salt",
           "Phthalimide and ethanolic KOH, then an alkyl halide", "Chloroform and ethanolic KOH"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "III", "B": "I", "C": "IV", "D": "II"}], "C"),
      "Named reactions and tests of amines",
      "Each named reaction has a characteristic reagent: Gabriel uses potassium phthalimide, the carbylamine test "
      "uses CHCl₃ and KOH, Hinsberg's reagent is C₆H₅SO₂Cl, and the Gattermann reaction uses copper powder with HX.",
      ["Gabriel → phthalimide/KOH, then R–X → III", "Carbylamine → CHCl₃ + ethanolic KOH → IV",
       "Hinsberg → benzenesulphonyl chloride → I", "Gattermann → Cu powder/HCl with ArN₂⁺Cl⁻ → II"],
      ncert=f"{NC12}, 'Amines', preparation and chemical reactions of amines and diazonium salts", seconds=40),

    N(T_NI, "Diazonium salts", "Advanced",
      "9.3 g of aniline is diazotised completely according to\n"
      "C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O\n"
      "The minimum mass of NaNO₂ and the minimum amount of HCl needed are, respectively (C = 12, H = 1, N = 14, "
      "O = 16, Na = 23):",
      ["6.9 g and 0.1 mol", "13.8 g and 0.2 mol", "3.45 g and 0.1 mol", "6.9 g and 0.2 mol"], "D",
      "6.9 g and 0.2 mol",
      "Stoichiometry of diazotisation",
      "The balanced equation uses two HCl per aniline: one converts NaNO₂ into nitrous acid "
      "(NaNO₂ + HCl → HNO₂ + NaCl) and the other ends up as the chloride of the diazonium salt.",
      ["Moles of aniline = 9.3/93 = 0.1 mol", "NaNO₂ = 0.1 mol × 69 = 6.9 g", "HCl = 2 × 0.1 = 0.2 mol"],
      why_others_wrong="'6.9 g and 0.1 mol' forgets that two HCl are used. 13.8 g doubles the nitrite as well. "
                       "3.45 g halves it.",
      ncert=f"{NC12}, 'Amines', method of preparation of diazonium salts", seconds=70),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "multi_statement",
      *ms("Which of the following statements about amines and diazonium salts are correct?",
          [("Primary amines have higher boiling points than tertiary amines of comparable molecular mass.", True),
           ("Aliphatic amines are stronger bases than ammonia because of the +I effect of the alkyl groups.", True),
           ("Benzenediazonium chloride is stable at room temperature and can be stored for long periods.", False),
           ("In the gas phase, the basic strength follows the order tertiary > secondary > primary amine > NH₃.",
            True),
           ("Ammonolysis of an alkyl halide gives only the primary amine.", False)],
          [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "e"]], "A"),
      "Physical properties, basicity and stability",
      "Primary amines are associated through N–H···N hydrogen bonds; tertiary amines have no N–H. In the gas phase "
      "only the +I effect operates. Diazonium salts are made at 273–278 K and used at once. Ammonolysis gives a "
      "mixture, because the amine formed reacts further with the alkyl halide.",
      ["(a) 1° amines hydrogen bond; 3° cannot → true", "(b) +I effect raises electron density on N → true",
       "(c) Benzenediazonium chloride is stable only in cold solution and is used immediately → false",
       "(d) Gas phase: 3° > 2° > 1° > NH₃ → true",
       "(e) Ammonolysis gives a mixture of 1°, 2°, 3° amines and the quaternary salt → false"],
      ncert=f"{NC12}, 'Amines', physical properties and chemical reactions", seconds=75),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "The correct order of basic strength in aqueous solution is:",
      ["(C₂H₅)₃N > (C₂H₅)₂NH > C₂H₅NH₂ > C₆H₅NH₂", "(C₂H₅)₂NH > (C₂H₅)₃N > C₂H₅NH₂ > C₆H₅NH₂",
       "(C₂H₅)₂NH > C₂H₅NH₂ > (C₂H₅)₃N > C₆H₅NH₂", "C₂H₅NH₂ > (C₂H₅)₂NH > (C₂H₅)₃N > C₆H₅NH₂"], "B",
      "Basicity of amines in water: inductive, solvation and steric effects",
      "In water, basicity depends on the +I effect, on hydrogen-bond solvation of the protonated amine, and on "
      "steric hindrance. For ethyl groups the order is 2° > 3° > 1°; aniline is far weaker because its lone pair is "
      "delocalised into the ring. NCERT pKb values: (C₂H₅)₂NH 3.00, (C₂H₅)₃N 3.25, C₂H₅NH₂ 3.29, C₆H₅NH₂ 9.38.",
      ["Lower pKb → stronger base", "3.00 < 3.25 < 3.29 < 9.38",
       "(C₂H₅)₂NH > (C₂H₅)₃N > C₂H₅NH₂ > C₆H₅NH₂"],
      why_others_wrong="3° > 2° > 1° is the gas-phase order. 2° > 1° > 3° is the order for the methyl amines, not the "
                       "ethyl amines. 1° > 2° > 3° considers only solvation.",
      ncert=f"{NC12}, 'Amines', basic character of amines (pKb table)", seconds=60),
]


# ================================================================ Biomolecules (Chemistry) (481-490)
# 484: glucose (180) + 5 acetyl groups: each -OH -> -OCOCH3 adds C2H2O (42)
m_glc = mm(C=6, H=12, O=6)
m_penta = m_glc + 5 * mm(C=2, H=2, O=1)
assert m_glc == 180 and m_penta == 390 == mm(C=16, H=22, O=11)
assert m_glc + 4 * 42 == 348 and m_glc + 6 * 42 == 432 and m_glc + 42 == 222
# 488: Gly (75) + Ala (89) + Val (117) - 2 H2O
aa = {"Gly": mm(C=2, H=5, N=1, O=2), "Ala": mm(C=3, H=7, N=1, O=2), "Val": mm(C=5, H=11, N=1, O=2)}
assert aa == {"Gly": 75, "Ala": 89, "Val": 117}
tri = sum(aa.values()) - 2 * 18
assert tri == 245 and sum(aa.values()) == 281 and sum(aa.values()) - 18 == 263 and sum(aa.values()) - 54 == 227

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "On prolonged heating with HI, glucose gives:",
      ["Hexan-1-ol", "n-Hexane", "Gluconic acid", "Sorbitol"], "B",
      "Evidence for the straight carbon chain of glucose",
      "HI reduces all the oxygen-containing groups, and the product n-hexane shows that the six carbon atoms of "
      "glucose are joined in a straight chain.",
      ["C₆H₁₂O₆ + HI (heat, long time) → CH₃–(CH₂)₄–CH₃"],
      why_others_wrong="Gluconic acid comes from oxidation with bromine water. Sorbitol and hexan-1-ol keep oxygen, "
                       "which prolonged heating with HI removes.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose", seconds=20),

    Q(T_BM, "Amino acids and proteins", "Basic", "direct",
      "Which of the following is an essential amino acid?",
      ["Glycine", "Alanine", "Serine", "Valine"], "D",
      "Essential and non-essential amino acids",
      "Essential amino acids cannot be synthesised in the body and must be obtained from the diet. NCERT's table "
      "marks valine, leucine, isoleucine, arginine, lysine, threonine, methionine, phenylalanine, tryptophan and "
      "histidine as essential.",
      ["Valine → essential", "Glycine, alanine, serine → synthesised in the body (non-essential)"],
      ncert=f"{NC12}, 'Biomolecules', classification of amino acids", seconds=20),

    Q(T_BM, "Vitamins", "Basic", "match_list",
      *ml("Match the vitamin in List-I with the disease or condition caused by its deficiency in List-II.",
          ["Vitamin B₂ (riboflavin)", "Vitamin B₆ (pyridoxine)", "Vitamin B₁₂", "Vitamin K"],
          ["Pernicious anaemia", "Increased blood clotting time", "Convulsions",
           "Cheilosis (fissuring at the corners of the mouth and lips)"],
          {"A": "IV", "B": "III", "C": "I", "D": "II"},
          [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
           {"A": "IV", "B": "I", "C": "III", "D": "II"}], "A"),
      "Deficiency diseases of vitamins",
      "NCERT lists the main deficiency condition of each vitamin.",
      ["B₂ → cheilosis, digestive disorders → IV", "B₆ → convulsions → III", "B₁₂ → pernicious anaemia → I",
       "K → increased blood clotting time → II"],
      why_others_wrong="A-III, B-IV swaps B₂ and B₆. C-II, D-I swaps B₁₂ and K. B-I, C-III swaps B₆ and B₁₂.",
      ncert=f"{NC12}, 'Biomolecules', vitamins (table of deficiency diseases)", seconds=40),

    N(T_BM, "Carbohydrates", "Intermediate",
      "Acetylation of glucose with acetic anhydride gives glucose pentaacetate, which shows that glucose has five "
      "–OH groups. The molar mass of glucose pentaacetate is (C = 12, H = 1, O = 16):",
      ["348 g mol⁻¹", "432 g mol⁻¹", "390 g mol⁻¹", "222 g mol⁻¹"], "C", "390 g mol⁻¹",
      "Mass change on acetylation",
      "Each –OH becomes –OCOCH₃: one H is replaced by COCH₃, a net gain of C₂H₂O (42 g mol⁻¹) per hydroxyl group.",
      ["Glucose C₆H₁₂O₆ = 180 g mol⁻¹", "Five acetylations: 180 + 5 × 42 = 390 g mol⁻¹",
       "Formula of the pentaacetate: C₁₆H₂₂O₁₁ = 192 + 22 + 176 = 390"],
      why_others_wrong="348 counts four –OH groups, 432 six, and 222 only one.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose (acetylation)", seconds=50),

    Q(T_BM, "Carbohydrates", "Intermediate", "statement_pair",
      *sp("Fructose is a ketohexose, and its cyclic form has a five-membered (furanose) ring.", True,
          "Oxidation of glucose with bromine water gives saccharic acid.", False),
      "Fructose and the oxidation of glucose",
      "Fructose has a keto group at C-2 and forms a five-membered ring (C-2 to C-5 oxygen). Bromine water is a mild "
      "oxidant: it oxidises only the –CHO group of glucose, giving gluconic acid. Nitric acid oxidises both ends to "
      "saccharic acid.",
      ["Statement I: fructose, C₆H₁₂O₆, ketohexose, furanose ring → true",
       "Statement II: Br₂ water gives gluconic acid; saccharic acid needs HNO₃ → false"],
      ncert=f"{NC12}, 'Biomolecules', glucose and fructose", seconds=40),

    Q(T_BM, "Vitamins", "Intermediate", "assertion_reason",
      *ar("Vitamin B₁₂ is a fat-soluble vitamin.", False,
          "Fat-soluble vitamins are stored in the liver and adipose (fat-storing) tissues.", True),
      "Classification of vitamins by solubility",
      "Vitamins A, D, E and K are fat-soluble. The B-group vitamins and vitamin C are water-soluble. Among the "
      "water-soluble vitamins, B₁₂ is the exception that can be stored in the body, but it is still water-soluble.",
      ["A: B₁₂ belongs to the water-soluble B group → false",
       "R: NCERT states that fat-soluble vitamins are stored in the liver and adipose tissues → true"],
      why_others_wrong="The fact that B₁₂ can be stored tempts students to call it fat-soluble; A is false.",
      ncert=f"{NC12}, 'Biomolecules', classification of vitamins", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "multi_statement",
      *ms("Which of the following statements about proteins are correct?",
          [("Fibrous proteins such as keratin and myosin are generally insoluble in water.", True),
           ("Globular proteins such as insulin and albumins are insoluble in water.", False),
           ("In the α-helix, the polypeptide chain twists into a right-handed helix held by hydrogen bonds between "
            "the –NH group of one amino acid residue and the >C=O group of an adjacent turn.", True),
           ("The primary structure of a protein means its α-helix and β-pleated sheet arrangement.", False),
           ("In the β-pleated sheet, the peptide chains are stretched out nearly to their maximum extension and lie "
            "side by side, held together by hydrogen bonds.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
      "Classification and structure of proteins",
      "Fibrous proteins have parallel chains held by hydrogen and disulphide bonds and are insoluble; globular "
      "proteins are folded into spheres and are usually soluble. The primary structure is the sequence of amino "
      "acids; α-helix and β-pleated sheet are secondary structures.",
      ["(a) Keratin (hair, wool) and myosin (muscle) → insoluble → true",
       "(b) Insulin and albumins are usually soluble → false",
       "(c) α-Helix: right-handed screw, N–H···O=C hydrogen bonds between turns → true",
       "(d) α-Helix and β-sheet are secondary structure; primary = amino acid sequence → false",
       "(e) β-Pleated sheet: extended chains side by side, hydrogen bonded → true"],
      ncert=f"{NC12}, 'Biomolecules', proteins (classification and structure)", seconds=75),

    N(T_BM, "Amino acids and proteins", "Advanced",
      "The molar mass of the tripeptide Gly–Ala–Val, formed from glycine (75 g mol⁻¹), alanine (89 g mol⁻¹) and "
      "valine (117 g mol⁻¹), is:",
      ["245 g mol⁻¹", "281 g mol⁻¹", "263 g mol⁻¹", "227 g mol⁻¹"], "A", "245 g mol⁻¹",
      "Peptide bond formation is a condensation",
      "Each peptide bond forms with loss of one molecule of water. A tripeptide has two peptide bonds.",
      ["Sum of amino acids = 75 + 89 + 117 = 281 g mol⁻¹",
       "Two peptide bonds → 2 H₂O lost = 36 g mol⁻¹",
       "Molar mass = 281 − 36 = 245 g mol⁻¹"],
      why_others_wrong="281 forgets the water lost. 263 removes only one water. 227 removes three (one per amino "
                       "acid).",
      ncert=f"{NC12}, 'Biomolecules', structure of proteins (peptide bond)", seconds=60),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about glucose are correct?",
          [("α-D-Glucose and β-D-glucose are anomers; they differ only in the configuration at C-1.", True),
           ("Glucose reacts with hydroxylamine to form an oxime, showing the presence of a carbonyl group.", True),
           ("Glucose adds HCN to form a cyanohydrin.", True),
           ("The prefix D in D-glucose shows that glucose is dextrorotatory.", False),
           ("Glucose pentaacetate reacts with hydroxylamine to form an oxime.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
      "Open-chain and cyclic structure of glucose",
      "The open-chain form reacts as an aldehyde, but in the cyclic hemiacetal the C-1 becomes a new stereocentre "
      "(anomers). In the pentaacetate there is no free –OH at C-1 to open the ring, so it does not react with "
      "hydroxylamine. D and L describe configuration, not the sign of rotation.",
      ["(a) α and β forms differ at C-1 (the anomeric carbon) → true",
       "(b) Oxime formation → >C=O present → true", "(c) Cyanohydrin formation → true",
       "(d) D refers to the configuration related to glyceraldehyde; (+) or (−) shows rotation → false",
       "(e) The pentaacetate does not react with NH₂OH → false"],
      ncert=f"{NC12}, 'Biomolecules', glucose (structure and cyclic structure)", seconds=80),

    Q(T_BM, "Carbohydrates", "Advanced", "statement_pair",
      *sp("In amylopectin, the chain branches through C1–C6 glycosidic linkages.", True,
          "Glycogen is more highly branched than amylopectin and is stored in the liver, muscles and brain of "
          "animals.", True),
      "Polysaccharides: amylopectin and glycogen",
      "Amylopectin is a branched polymer of α-D-glucose: C1–C4 links along the chain and C1–C6 links at branch "
      "points. Glycogen, the storage polysaccharide of animals, has a similar structure but is even more highly "
      "branched.",
      ["Statement I: branching by C1–C6 glycosidic linkage → true",
       "Statement II: glycogen ('animal starch') is more highly branched; found in liver, muscles and brain → true"],
      ncert=f"{NC12}, 'Biomolecules', polysaccharides (starch and glycogen)", seconds=40),
]


# ================================================================ Principles Related to Practical Chemistry (491-500)
# 493: oxalic acid dihydrate H2C2O4.2H2O = 126 ; 250 mL of 0.1 M
m_oxd = mm(C=2, H=6, O=6)
assert m_oxd == 126 and F(1, 10) * F(250, 1000) * m_oxd == F(315, 100)
assert F(1, 10) * F(250, 1000) * 90 == F(225, 100) and F(1, 10) * m_oxd == F(126, 10) and F(315, 200) == F(1575, 1000)
# 494: 3.19 g anhydrous CuSO4 (159.5) ; dH = -66 kJ/mol ; 100 g water ; c = 4.2 J/g/K
n_cu = F(319, 100) / F(1595, 10)
dT = n_cu * 66000 / (100 * F(42, 10))
assert n_cu == F(2, 100) and r2(dT) == 3.14
assert r2(F(319, 100) / F(2495, 10) * 66000 / 420) == 2.01 and r2(n_cu * 66000 / 840) == 1.57 and n_cu * 66000 / 100 == F(132, 10)
# 498: H2C2O4 + 2NaOH ; 10.0 mL of 0.05 M acid needs 12.5 mL NaOH
m_naoh = 2 * 10 * F(5, 100) / F(125, 10)
assert m_naoh == F(8, 100) and 10 * F(5, 100) / F(125, 10) == F(4, 100)
assert F(125, 10) * F(5, 100) / 10 == F(625, 10000) and 4 * 10 * F(5, 100) / F(125, 10) == F(16, 100)
# 499: rate = k[H2O2][I-]
r0 = F(2, 100000)
r1 = r0 * (F(3, 100) / F(2, 100)) * (F(4, 100) / F(1, 100))
assert r1 == F(12, 100000) and r0 * 4 == F(8, 100000) and r0 * F(3, 2) == F(3, 100000) and r0 * F(3, 2) * 16 == F(48, 100000)

QUESTIONS += [
    Q(T_PR, "Titrimetric analysis", "Basic", "direct",
      "Which indicator is suitable for titrating oxalic acid (a weak acid) against sodium hydroxide (a strong "
      "base)?",
      ["Methyl orange", "Starch", "Phenolphthalein", "Potassium permanganate"], "C",
      "Choice of acid–base indicator",
      "At the equivalence point of a weak acid–strong base titration the solution is slightly basic. "
      "Phenolphthalein changes colour in the basic range (about pH 8.2–10), so it marks the end point sharply.",
      ["Weak acid + strong base → end point in basic range → phenolphthalein (colourless → pink)"],
      why_others_wrong="Methyl orange changes in the acidic range and gives an early, unsharp end point. Starch is "
                       "an indicator for iodine, and KMnO₄ is a self-indicator only in redox titrations.",
      ncert=f"{LAB}, titrimetric analysis (acids, bases and indicators)", seconds=25),

    Q(T_PR, "Preparations", "Basic", "direct",
      "While preparing Mohr's salt, a few drops of dilute sulphuric acid are added to the solution of ferrous "
      "sulphate and ammonium sulphate. This is done to prevent:",
      ["Hydrolysis of ferrous sulphate", "Oxidation of ammonium ions", "Precipitation of ammonium sulphate",
       "Evaporation of the water"], "A",
      "Preparation of a double salt",
      "Fe²⁺ salts hydrolyse in water to give a basic salt, which makes the solution turbid. A little dilute H₂SO₄ "
      "suppresses this hydrolysis, so clear crystals of FeSO₄·(NH₄)₂SO₄·6H₂O form on cooling.",
      ["FeSO₄ + 2H₂O ⇌ Fe(OH)₂ + H₂SO₄; added H₂SO₄ shifts this to the left"],
      ncert=f"{LAB}, preparation of inorganic compounds (Mohr's salt)", seconds=25),

    N(T_PR, "Titrimetric analysis", "Basic",
      "The mass of oxalic acid crystals, H₂C₂O₄·2H₂O, needed to prepare 250 mL of a 0.1 M solution is (C = 12, "
      "H = 1, O = 16):",
      ["2.25 g", "3.15 g", "12.6 g", "1.575 g"], "B", "3.15 g",
      "Preparing a standard solution",
      "Mass = molarity × volume (L) × molar mass of the crystals actually weighed, including the water of "
      "crystallisation.",
      ["Molar mass of H₂C₂O₄·2H₂O = 90 + 36 = 126 g mol⁻¹", "Moles = 0.1 × 0.250 = 0.025 mol",
       "Mass = 0.025 × 126 = 3.15 g"],
      why_others_wrong="2.25 g uses anhydrous oxalic acid (90). 12.6 g is for 1 L. 1.575 g is for 0.05 M, as if the "
                       "molarity had been halved for the two acidic hydrogens.",
      ncert=f"{LAB}, titrimetric analysis (preparing a standard solution)", seconds=35),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "3.19 g of anhydrous copper(II) sulphate (molar mass 159.5 g mol⁻¹) is dissolved in 100 g of water in a "
      "calorimeter. Take the enthalpy of solution of anhydrous CuSO₄ as −66 kJ mol⁻¹, the specific heat as "
      "4.2 J g⁻¹ K⁻¹, the mass of the solution as 100 g, and ignore the heat taken up by the calorimeter. The "
      "temperature rises by about:",
      ["2.01 K", "1.57 K", "13.2 K", "3.14 K"], "D", "3.14 K",
      "Enthalpy of solution and temperature change",
      "The heat released by dissolving the salt warms the solution: n × |ΔsolH| = m × c × ΔT.",
      ["n = 3.19/159.5 = 0.02 mol", "Heat released = 0.02 × 66 000 = 1320 J",
       "ΔT = 1320/(100 × 4.2) = 3.14 K"],
      why_others_wrong="2.01 K uses the molar mass of CuSO₄·5H₂O (249.5). 1.57 K takes the mass as 200 g. 13.2 K "
                       "leaves out the specific heat.",
      ncert=f"{LAB}, thermochemistry (enthalpy of dissolution of copper sulphate)", seconds=75),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "direct",
      "In group I analysis, the white precipitate obtained with dilute HCl is boiled with water, and potassium "
      "chromate solution is added to the hot filtrate. A yellow precipitate forms. It is:",
      ["PbCrO₄", "PbCl₂", "PbI₂", "Ag₂CrO₄"], "A",
      "Confirmatory test for Pb²⁺",
      "PbCl₂ is soluble in hot water (unlike AgCl). The hot solution gives yellow lead chromate with potassium "
      "chromate.",
      ["Pb²⁺ + 2Cl⁻ → PbCl₂ (white, dissolves in hot water)", "Pb²⁺ + CrO₄²⁻ → PbCrO₄ (yellow)"],
      why_others_wrong="PbCl₂ is white and is the precipitate that was dissolved. PbI₂ would need KI. Silver chromate "
                       "is brick-red, and AgCl does not dissolve in hot water.",
      ncert=f"{LAB}, systematic qualitative analysis of cations (group I)", seconds=35),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "assertion_reason",
      *ar("When a sulphide is warmed with dilute H₂SO₄, the gas evolved turns lead acetate paper black.", True,
          "The gas evolved is H₂S, which reacts with lead acetate to form black lead sulphide.", True, explains=True),
      "Test for the sulphide ion",
      "Dilute acid liberates H₂S from a sulphide; H₂S forms black PbS on paper soaked in lead acetate solution.",
      ["S²⁻ + 2H⁺ → H₂S↑", "(CH₃COO)₂Pb + H₂S → PbS (black) + 2CH₃COOH", "R explains A"],
      ncert=f"{LAB}, qualitative analysis (tests for anions)", seconds=30),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the anion in List-I with an observation that identifies it in List-II.",
          ["CO₃²⁻", "Cl⁻", "Br⁻", "I⁻"],
          ["White precipitate with AgNO₃, soluble in NH₄OH", "Violet vapours with conc. H₂SO₄ that turn starch paper "
           "blue", "Brisk effervescence with dilute H₂SO₄; the gas turns lime water milky",
           "Reddish-brown vapours on warming with conc. H₂SO₄"],
          {"A": "III", "B": "I", "C": "IV", "D": "II"},
          [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
           {"A": "III", "B": "I", "C": "II", "D": "IV"}], "B"),
      "Tests for anions",
      "Carbonate gives CO₂ with dilute acid. Halides are distinguished by the vapours they give with concentrated "
      "sulphuric acid and by their silver salts.",
      ["CO₃²⁻ → CO₂ → lime water milky → III", "Cl⁻ → AgCl (white, soluble in NH₄OH) → I",
       "Br⁻ → Br₂ vapours (reddish brown) → IV", "I⁻ → I₂ vapours (violet), starch blue → II"],
      why_others_wrong="B-IV, C-I swaps chloride and bromide. C-II, D-IV swaps the bromine and iodine vapours.",
      ncert=f"{LAB}, qualitative analysis (tests for anions)", seconds=45),

    N(T_PR, "Titrimetric analysis", "Advanced",
      "10.0 mL of 0.05 M oxalic acid solution needs 12.5 mL of a sodium hydroxide solution for complete "
      "neutralisation (phenolphthalein indicator). The molarity of the NaOH solution is:",
      ["0.04 M", "0.0625 M", "0.08 M", "0.16 M"], "C", "0.08 M",
      "Acid–base titration with a dibasic acid",
      "Oxalic acid has two replaceable hydrogens: H₂C₂O₄ + 2NaOH → Na₂C₂O₄ + 2H₂O.",
      ["mmol oxalic acid = 10.0 × 0.05 = 0.50 mmol", "mmol NaOH = 2 × 0.50 = 1.00 mmol",
       "Molarity = 1.00/12.5 = 0.08 M"],
      why_others_wrong="0.04 M ignores the factor 2. 0.0625 M inverts the volumes. 0.16 M uses the factor 2 twice.",
      ncert=f"{LAB}, titrimetric analysis (acid–base titration)", seconds=60),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "In a study of the reaction H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O at room temperature, the rate law is "
      "rate = k[H₂O₂][I⁻]. The initial rate is 2.0 × 10⁻⁵ mol L⁻¹ s⁻¹ when [H₂O₂] = 0.02 M and [I⁻] = 0.01 M. "
      "At the same temperature and acidity, the initial rate when [H₂O₂] = 0.03 M and [I⁻] = 0.04 M is:",
      ["8.0 × 10⁻⁵ mol L⁻¹ s⁻¹", "3.0 × 10⁻⁵ mol L⁻¹ s⁻¹", "4.8 × 10⁻⁴ mol L⁻¹ s⁻¹",
       "1.2 × 10⁻⁴ mol L⁻¹ s⁻¹"], "D", "1.2 × 10⁻⁴ mol L⁻¹ s⁻¹",
      "Using a rate law with two reactants",
      "Each concentration enters the rate law to the first power, so the rate changes by the product of the two "
      "concentration ratios.",
      ["[H₂O₂] ratio = 0.03/0.02 = 1.5", "[I⁻] ratio = 0.04/0.01 = 4",
       "New rate = 2.0 × 10⁻⁵ × 1.5 × 4 = 1.2 × 10⁻⁴ mol L⁻¹ s⁻¹"],
      why_others_wrong="8.0 × 10⁻⁵ changes only [I⁻]; 3.0 × 10⁻⁵ changes only [H₂O₂]. 4.8 × 10⁻⁴ treats the "
                       "reaction as second order in I⁻ (using 2I⁻ from the equation).",
      ncert=f"{LAB}, chemical kinetics (reaction of iodide ion with hydrogen peroxide)", seconds=75),

    Q(T_PR, "Preparations", "Advanced", "multi_statement",
      *ms("Which of the following statements about the laboratory preparations are correct?",
          [("Acetanilide is prepared by acetylating aniline with acetic anhydride (in glacial acetic acid).", True),
           ("p-Nitroacetanilide is prepared by nitrating aniline directly and then acetylating the product.", False),
           ("Aniline yellow (p-aminoazobenzene) is prepared by coupling benzenediazonium chloride with aniline.",
            True),
           ("Potash alum is the double salt K₂SO₄·Al₂(SO₄)₃·24H₂O.", True),
           ("Iodoform prepared in the laboratory is a colourless liquid.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["c", "d", "e"]], "B"),
      "Organic and inorganic preparations",
      "Aniline is protected by acetylation before nitration; the acetanilide is nitrated to p-nitroacetanilide. "
      "Iodoform is a yellow crystalline solid.",
      ["(a) C₆H₅NH₂ + (CH₃CO)₂O → C₆H₅NHCOCH₃ + CH₃COOH → true",
       "(b) Acetanilide (not aniline) is nitrated → false",
       "(c) C₆H₅N₂⁺Cl⁻ + C₆H₅NH₂ → p-H₂N–C₆H₄–N=N–C₆H₅ → true",
       "(d) Potash alum formula → true", "(e) Iodoform is a pale yellow solid → false"],
      ncert=f"{LAB}, preparation of organic and inorganic compounds", seconds=75),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_DF: (3, 5, 4), T_CC: (5, 6, 5), T_PU: (2, 2, 2), T_GO: (5, 7, 5), T_HC: (4, 6, 4), T_HX: (3, 4, 3),
        T_OX: (5, 7, 5), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 122
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert all(27 <= keys[k] <= 34 for k in LETTERS), keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "Package CHE_002_p2: 122 original Chemistry questions (d/f block, coordination compounds, "
                    "organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_002/CHE_002_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
