"""Writes batches/parts/BATCH_009_CHE_p2.json: package CHE_009_p2 of BATCH_009 (Chemistry, 127 questions).

Topics: p-Block Elements, d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of
Organic Compounds, Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens /
Oxygen / Nitrogen, Biomolecules (Chemistry), Principles Related to Practical Chemistry. IDs NEET_CHE_002124..002250.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_009/CHE_009_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_009_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 2124, 2250
# ai:self-recheck = a second, separate solve of every question by the author after the file was written.
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

T_PB = "p-Block Elements"
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
      "Ca": 40, "Ba": 137, "P": 31, "B": F(108, 10), "Al": 27, "As": 75, "Sb": 122, "Sn": 119}


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    return sum(AM[k] * v for k, v in atoms.items())


def bm(n):
    """Spin-only magnetic moment sqrt(n(n+2)) in BM."""
    return math.sqrt(n * (n + 2))


QUESTIONS = []

# ================================================================ p-Block Elements (2124-2136)
# 2125: group 16, period 4: [Ar] 3d10 4s2 4p4
z_2125 = 18 + 10 + 2 + 4
assert z_2125 == 34
# 2130: decomposition of AsH3 into its elements: dH = -n * dfH
n_2130 = F(156, 10) / mm(As=1, H=3)
dh_2130 = -n_2130 * F(664, 10)
assert n_2130 == F(1, 5) and f"{float(dh_2130):.1f}" == "-13.3"
v_2130 = f"{float(dh_2130):.1f} kJ".replace("-", "−")
# 2135: energy that turns 1.08 g B(g) into B3+(g) is used for Al(g) -> Al3+(g)
ie_B, ie_Al = 801 + 2427 + 3659, 577 + 1816 + 2744
assert (ie_B, ie_Al) == (6887, 5137)
e_2135 = F(108, 100) / AM["B"] * ie_B
m_2135 = e_2135 / ie_Al * AM["Al"]
assert f"{float(m_2135):.2f}" == "3.62"
assert f"{float(F(1, 10) * ie_Al / ie_B * 27):.2f}" == "2.01"            # ratio inverted
assert f"{float(F(1, 10) * 801 / 577 * 27):.2f}" == "3.75"              # first IE only
v_2135 = f"{float(m_2135):.2f} g"

QUESTIONS += [
    Q(T_PB, "Group 13 and 14 trends", "Basic", "direct",
      "Which of the following elements of group 14 is a metalloid?",
      ["Carbon", "Germanium", "Tin", "Lead"], "B",
      "Metallic character down group 14",
      "Metallic character increases down group 14. Carbon is a non-metal, germanium is a metalloid, and tin and lead "
      "are soft metals with low melting points.",
      ["Group 14: C, Si, Ge, Sn, Pb", "Non-metal → metalloid → metals on going down", "Germanium is the metalloid"],
      why_others_wrong="Carbon is a non-metal; tin and lead are metals.",
      ncert=f"{NC11}, 'The p-Block Elements', group 14: physical and chemical properties", seconds=20),

    N(T_PB, "Group 15 and 16 trends", "Basic",
      "An element of group 16 lies in the fourth period of the periodic table. Its atomic number is:",
      ["32", "33", "34", "35"], "C", str(z_2125),
      "Locating a p-block element from its group and period",
      "A group 16 element has the valence configuration ns² np⁴. In the fourth period this is 4s² 4p⁴, which follows the "
      "argon core and the filled 3d subshell.",
      ["Configuration: [Ar] 3d¹⁰ 4s² 4p⁴", "Z = 18 + 10 + 2 + 4 = 34 (selenium)"],
      shortcut="Period 4 ends at Kr (Z = 36); group 16 is two places before group 18, so Z = 36 − 2 = 34.",
      why_others_wrong="32 is germanium (group 14), 33 is arsenic (group 15) and 35 is bromine (group 17).",
      seconds=30),

    Q(T_PB, "Group 15 and 16 trends", "Basic", "statement_pair",
      *sp("In group 16, the electron gain enthalpy becomes less negative on going down from sulphur to polonium.", True,
          "The atomic radius of tellurium is smaller than that of sulphur.", False),
      "Electron gain enthalpy and atomic size in group 16",
      "Oxygen has a less negative electron gain enthalpy than sulphur because of its compact 2p subshell, but from "
      "sulphur onwards the value again becomes less negative up to polonium, as the atoms grow larger. Atomic radius "
      "increases down the group because a new shell is added each time, so tellurium is larger than sulphur.",
      ["Statement I: S → Se → Te → Po, electron gain enthalpy less negative: true",
       "Statement II: radius increases down the group, so Te > S: false"],
      ncert=f"{NC12}, 'The p-Block Elements', group 16: atomic and physical properties", seconds=35),

    Q(T_PB, "Group 17 and 18 trends", "Basic", "match_list",
      *ml("Match the halogen in List-I with its ground-state electronic configuration in List-II.",
          ["Fluorine (Z = 9)", "Chlorine (Z = 17)", "Bromine (Z = 35)", "Iodine (Z = 53)"],
          ["[Kr] 4d¹⁰ 5s² 5p⁵", "[Ar] 3d¹⁰ 4s² 4p⁵", "[Ne] 3s² 3p⁵", "[He] 2s² 2p⁵"],
          "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D"),
      "Electronic configuration of group 17 elements",
      "All halogens have the valence configuration ns² np⁵, with n equal to the period number. From period 4 "
      "onwards the filled (n−1)d¹⁰ subshell appears before the ns² np⁵ valence shell.",
      ["F (period 2): [He] 2s² 2p⁵ (IV)", "Cl (period 3): [Ne] 3s² 3p⁵ (III)",
       "Br (period 4): [Ar] 3d¹⁰ 4s² 4p⁵ (II)", "I (period 5): [Kr] 4d¹⁰ 5s² 5p⁵ (I)"],
      shortcut="Check the electron count: core + 2 + 5 (+10 for the d subshell) must equal Z.",
      why_others_wrong="Codes that swap fluorine and chlorine, or bromine and iodine, give configurations whose "
                       "electron count does not equal the atomic number.",
      ncert=f"{NC12}, 'The p-Block Elements', group 17: electronic configuration", seconds=35),

    Q(T_PB, "Anomalous first element", "Intermediate", "assertion_reason",
      *ar("Carbon cannot show a covalency greater than four, whereas silicon and the heavier elements of group 14 "
          "can expand their covalency beyond four.", True,
          "The valence shell of carbon has only the 2s and 2p orbitals (four orbitals in all) and no d orbitals, "
          "whereas the heavier elements have vacant d orbitals in their valence shell.", True, explains=True),
      "Anomalous behaviour of carbon",
      "The first member of group 14 has only four valence orbitals (2s, 2px, 2py, 2pz), so it can form at most four "
      "covalent bonds. Silicon and the heavier members have vacant d orbitals in the valence shell and can use them to "
      "show a covalency of six. R gives the cause of A.",
      ["Carbon: n = 2, no 2d subshell → 4 valence orbitals → maximum covalency 4",
       "Si onwards: vacant d orbitals → covalency can exceed 4", "R explains A"],
      ncert=f"{NC11}, 'The p-Block Elements', group 14: anomalous behaviour of carbon", seconds=35),

    Q(T_PB, "Group 15 and 16 trends", "Intermediate", "statement_pair",
      *sp("The stability of the halides of the group 16 elements decreases in the order fluoride > chloride > "
          "bromide > iodide.", True,
          "The first ionisation enthalpy decreases down group 16 from oxygen to tellurium.", True),
      "Group 16: halides and ionisation enthalpy",
      "Group 16 elements form many halides, and their stability falls from fluorides to iodides, in line with the "
      "falling strength of the E–X bond. Ionisation enthalpy decreases down the group because atomic size increases.",
      ["Statement I: stability of halides F > Cl > Br > I: true",
       "Statement II: ionisation enthalpy falls down the group: true"],
      ncert=f"{NC12}, 'The p-Block Elements', group 16: chemical properties", seconds=35),

    N(T_PB, "Group 15 and 16 trends", "Intermediate",
      "The standard enthalpies of formation (in kJ mol⁻¹) of some group 15 hydrides are: NH₃ −46.1, PH₃ +13.4, "
      "AsH₃ +66.4. What is the enthalpy change when 15.6 g of AsH₃(g) decomposes completely into arsenic and "
      "hydrogen (As = 75, H = 1)?",
      [v_2130, v_2130.replace("−", "+"), "−66.4 kJ", "−26.6 kJ"], "A", v_2130,
      "Enthalpy of decomposition and thermal stability of hydrides",
      "Decomposition into the elements is the reverse of formation, so ΔH(decomposition) = −ΔfH per mole. The values "
      "of ΔfH become more positive from NH₃ to AsH₃, which is why thermal stability falls down the group: the heavier "
      "hydrides decompose exothermically.",
      ["Molar mass of AsH₃ = 75 + 3 = 78 g mol⁻¹; n = 15.6/78 = 0.20 mol",
       "AsH₃ → As + 3/2 H₂: ΔH = −66.4 kJ mol⁻¹", "ΔH = 0.20 × (−66.4) ≈ −13.3 kJ"],
      why_others_wrong="+13.3 kJ keeps the sign of ΔfH instead of reversing it; −66.4 kJ is for one mole, not 0.20 mol; "
                       "−26.6 kJ uses 0.40 mol (doubling for 2AsH₃).",
      seconds=60),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the p-block elements are correct?",
          [("Across a period, from group 13 to group 17, the non-metallic character of the elements generally "
            "increases.", True),
           ("The p-block contains metals, non-metals and metalloids.", True),
           ("Down a group of the p-block, the metallic character of the elements decreases.", False),
           ("The inert pair effect becomes more marked for the heavier members of groups 13 to 16.", True),
           ("Metalloids are found only in group 14.", False)],
          [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "d", "e"]], "D"),
      "General features of the p-block",
      "The p-block has metals (Al, Sn, Pb, Bi, ...), non-metals (C, N, O, halogens, ...) and metalloids. Non-metallic "
      "character increases across a period and decreases (metallic character increases) down a group. The reluctance "
      "of the ns² pair to take part in bonding increases for the heavier elements, so the oxidation state two units "
      "below the group oxidation state becomes more stable in groups 13 to 16. Metalloids occur in several groups "
      "(Ge in 14, As and Sb in 15, Se and Te in 16).",
      ["(a) true", "(b) true", "(c) false: metallic character increases down a group", "(d) true",
       "(e) false: As, Sb, Se and Te are also metalloids"],
      ncert=f"{NC12}, 'The p-Block Elements', introduction and groups 15-16", seconds=50),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "direct",
      "Which of the following shows the p-block elements of the third period in order of DECREASING metallic "
      "character?",
      ["Cl > S > P > Si > Al", "Si > Al > P > S > Cl", "Al > P > Si > S > Cl", "Al > Si > P > S > Cl"], "D",
      "Trend in metallic character across a period",
      "Across a period the nuclear charge increases and the atomic radius decreases, so ionisation enthalpy and "
      "electronegativity rise and the tendency to lose electrons falls. Metallic character therefore decreases from "
      "left to right: aluminium (group 13) is a metal and chlorine (group 17) a typical non-metal.",
      ["Period 3 p-block, left to right: Al (13), Si (14), P (15), S (16), Cl (17)",
       "Metallic character decreases across the period", "Order: Al > Si > P > S > Cl"],
      why_others_wrong="The first option is the order of increasing metallic character; the other two break the "
                       "left-to-right sequence of the period.",
      ncert=f"{NC12}, 'The p-Block Elements', introduction: metallic and non-metallic character", seconds=30),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "assertion_reason",
      *ar("Down group 15, the stability of the +5 oxidation state decreases and that of the +3 oxidation state "
          "increases.", True,
          "The ns² electrons of the heavier elements are increasingly reluctant to take part in bond formation "
          "(inert pair effect).", True, explains=True),
      "Inert pair effect in group 15",
      "The group 15 elements show +3 and +5. Because the ns² electrons of the heavier elements hold back from bonding "
      "(inert pair effect), only three electrons are commonly used by bismuth, so +3 becomes the more stable state and "
      "Bi(V) compounds are rare. R explains A.",
      ["Valence configuration ns² np³", "Heavier elements: ns² pair reluctant to bond",
       "So +3 more stable than +5 down the group"],
      ncert=f"{NC12}, 'The p-Block Elements', group 15: oxidation states and trends in chemical reactivity",
      seconds=40),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "statement_pair",
      *sp("The E–H bond length increases from NH₃ to SbH₃ in group 15.", True,
          "Since the F–F bond is the shortest X–X bond, F₂ has the highest bond dissociation enthalpy among the "
          "halogens.", False),
      "Bond length and bond strength trends",
      "As the size of E increases down group 15, the E–H bond becomes longer (about 102 pm in NH₃ to about 171 pm in "
      "SbH₃). F₂ does have the shortest bond, but its bond dissociation enthalpy (158.8 kJ mol⁻¹) is lower than those "
      "of Cl₂ and Br₂, because of the large repulsion between the lone pairs of the small fluorine atoms. Cl₂ has the "
      "highest value.",
      ["Statement I: E–H bond length increases with size of E: true",
       "Statement II: bond dissociation enthalpy order Cl₂ > Br₂ > F₂ > I₂: false"],
      ncert=f"{NC12}, 'The p-Block Elements', groups 15 and 17", seconds=45),

    N(T_PB, "Group 13 and 14 trends", "Advanced",
      "The first three ionisation enthalpies (in kJ mol⁻¹) are: boron 801, 2427, 3659; aluminium 577, 1816, 2744. The "
      "energy needed to convert 1.08 g of gaseous boron atoms completely into B³⁺(g) ions would convert what mass of "
      "gaseous aluminium atoms into Al³⁺(g) ions? (B = 10.8, Al = 27)",
      ["2.70 g", v_2135, "2.01 g", "3.75 g"], "B", v_2135,
      "Sum of ionisation enthalpies in group 13",
      "Forming M³⁺(g) needs the sum of the first three ionisation enthalpies. This sum is much larger for boron "
      "(6887 kJ mol⁻¹) than for aluminium (5137 kJ mol⁻¹), which is one reason boron does not form B³⁺ ions.",
      ["Boron: n = 1.08/10.8 = 0.10 mol; energy = 0.10 × 6887 = 688.7 kJ",
       "Aluminium: ΣIE = 577 + 1816 + 2744 = 5137 kJ mol⁻¹", "n(Al) = 688.7/5137 = 0.134 mol",
       "Mass = 0.134 × 27 ≈ 3.62 g"],
      why_others_wrong="2.70 g assumes equal moles; 2.01 g inverts the ratio of the sums; 3.75 g uses only the first "
                       "ionisation enthalpies.",
      seconds=100),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "multi_statement",
      *ms("The electron gain enthalpies (in kJ mol⁻¹) of some elements are: O −141, S −200, Se −195, Te −190; "
          "F −333, Cl −349, Br −325, I −296. Which of the following conclusions are correct?",
          [("In both groups, the element of the second period has a less negative electron gain enthalpy than the "
            "element of the third period.", True),
           ("Each halogen has a more negative electron gain enthalpy than the group 16 element of the same period.",
            True),
           ("From the third period downwards, the electron gain enthalpy becomes less negative in both groups.", True),
           ("Oxygen has a less negative value than sulphur because the oxygen atom is larger than the sulphur atom.",
            False),
           ("Adding an electron to a gaseous oxygen atom releases more energy than adding one to a gaseous fluorine "
            "atom.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "B"),
      "Reading electron gain enthalpy data for groups 16 and 17",
      "The data show the second-period anomaly (O and F less negative than S and Cl), the steady fall from the third "
      "period downwards, and the much more negative values of the halogens, which need only one electron to reach a "
      "noble gas configuration. The anomaly arises because oxygen and fluorine are very small, so the incoming "
      "electron is strongly repelled by the electrons already in the compact 2p subshell.",
      ["(a) −141 > −200 and −333 > −349: true", "(b) −333 < −141, −349 < −200, ...: true",
       "(c) S → Se → Te and Cl → Br → I become less negative: true",
       "(d) false: oxygen is smaller, not larger", "(e) false: −141 is less negative than −333"],
      ncert=f"{NC12}, 'The p-Block Elements', groups 16 and 17: atomic properties", seconds=75),
]

# ================================================================ d- and f-Block Elements (2137-2147)
# 2137: 3d metals whose atoms have a 4s1 configuration (aufbau exceptions Cr and Cu)
conf_3d = {"Sc": (1, 2), "Ti": (2, 2), "V": (3, 2), "Cr": (5, 1), "Mn": (5, 2), "Fe": (6, 2), "Co": (7, 2),
           "Ni": (8, 2), "Cu": (10, 1), "Zn": (10, 2)}
assert all(d + s == z - 18 for (d, s), z in zip(conf_3d.values(), range(21, 31)))
v_2137 = str(sum(1 for d, s in conf_3d.values() if s == 1))
assert v_2137 == "2"
# 2141: Cr(VI) in dichromate is d0; Cr3+ is d3
v_2141 = f"{bm(0):.0f} BM to {bm(3):.2f} BM"
assert v_2141 == "0 BM to 3.87 BM"
# 2142: electrons accepted: Cr2O7(2-) -> 2Cr3+ : 2 x 3 = 6; MnO4- -> Mn2+ : 5
v_2142 = f"{float(F(2 * (6 - 3), 7 - 2)):.1f} mol"
assert v_2142 == "1.2 mol"
# 2145: I- per MnO4-: acidic (I- -> 1/2 I2, 1 e; MnO4- 5 e) = 5; neutral (I- -> IO3-, 6 e; MnO4- -> MnO2, 3 e) = 1/2
acid, neutral = F(5, 1), F(3, 6)
r_2145 = acid / neutral
assert r_2145 == 10
v_2145 = f"{r_2145} : 1"

QUESTIONS += [
    N(T_DF, "Transition element trends", "Basic",
      "How many elements of the first transition series (scandium to zinc) have only one electron in the 4s orbital "
      "in the ground state of the atom?",
      ["1", "2", "3", "4"], "B", v_2137,
      "Electronic configurations of the 3d series",
      "The 3d and 4s energies are close. Chromium and copper take one 4s electron into the 3d subshell to reach the "
      "more stable half-filled (3d⁵) and completely filled (3d¹⁰) arrangements: Cr [Ar] 3d⁵ 4s¹, Cu [Ar] 3d¹⁰ 4s¹. "
      "All the other 3d metals are 4s².",
      ["Sc to Zn: (n−1)d¹⁻¹⁰ ns², except", "Cr: 3d⁵ 4s¹", "Cu: 3d¹⁰ 4s¹", "Count = 2"],
      why_others_wrong="1 misses one of the two exceptions; 3 or 4 wrongly add manganese or zinc, which are 4s².",
      ncert=f"{NC12}, 'The d- and f-Block Elements', electronic configurations of the d-block elements", seconds=30),

    Q(T_DF, "Transition element trends", "Basic", "direct",
      "The metals of the second (4d) and third (5d) transition series have greater enthalpies of atomisation than the "
      "corresponding metals of the first (3d) series. According to NCERT, this is an important factor in accounting "
      "for:",
      ["the lanthanoid contraction", "the colour of their compounds", "the lower densities of the heavier metals",
       "the much more frequent metal–metal bonding in compounds of the heavy transition metals"], "D",
      "Enthalpy of atomisation of the 4d and 5d metals",
      "A greater enthalpy of atomisation means stronger metal–metal interaction. This is why metal–metal bonds occur "
      "much more often in compounds of the heavy (4d and 5d) transition metals than in those of the 3d metals.",
      ["4d, 5d metals: higher ΔaH than 3d", "Stronger M–M bonding", "→ metal–metal bonds common in their compounds"],
      why_others_wrong="The lanthanoid contraction comes from poor shielding by 4f electrons; colour comes from d–d "
                       "transitions; the 4d and 5d metals are denser, not less dense, than the 3d metals.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', physical properties of the transition elements", seconds=30),

    Q(T_DF, "Transition element trends", "Basic", "assertion_reason",
      *ar("Scandium (Z = 21) is regarded as a transition element, although its only common ion, Sc³⁺, has no d "
          "electron.", True,
          "In its ground state, the scandium atom has an incompletely filled 3d subshell (3d¹).", True, explains=True),
      "Definition of a transition element",
      "A transition element is one that has an incompletely filled d subshell in its ground state or in any of its "
      "common oxidation states. The scandium atom is [Ar] 3d¹ 4s², so it qualifies through its atom even though Sc³⁺ "
      "is 3d⁰. R gives the reason for A.",
      ["Sc: [Ar] 3d¹ 4s²", "Incomplete d subshell in the atom", "→ transition element"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', position in the periodic table and definition", seconds=30),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "statement_pair",
      *sp("Across the actinoid series, the maximum oxidation state first increases, from +4 for thorium to +5, +6 and "
          "+7 for protactinium, uranium and neptunium, and then decreases in the later elements.", True,
          "The ground-state electronic configuration of cerium (Z = 58) is [Xe] 4f² 6s².", False),
      "Oxidation states of actinoids; configuration of cerium",
      "NCERT notes that the maximum oxidation state of the actinoids rises up to the middle of the series and then "
      "falls. Cerium, the first lanthanoid, has the configuration [Xe] 4f¹ 5d¹ 6s², not 4f² 6s².",
      ["Statement I: true (Th +4, Pa +5, U +6, Np +7, then decrease)",
       "Statement II: false; Ce is [Xe] 4f¹ 5d¹ 6s²"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids and the actinoids", seconds=40),

    N(T_DF, "Magnetic and colour properties", "Intermediate",
      "When acidified potassium dichromate acts as an oxidising agent, chromium changes from the dichromate ion to "
      "Cr³⁺. The spin-only magnetic moment of the chromium species changes from (Z of Cr = 24):",
      ["0 BM to 2.83 BM", v_2141, "1.73 BM to 3.87 BM", "3.87 BM to 0 BM"], "B", v_2141,
      "Spin-only magnetic moment and oxidation state",
      "In Cr₂O₇²⁻ chromium is +6, which is 3d⁰: no unpaired electron. Cr³⁺ is 3d³ with three unpaired electrons.",
      ["Cr: [Ar] 3d⁵ 4s¹", "Cr(VI): 3d⁰ → n = 0 → μ = 0", "Cr³⁺: 3d³ → n = 3 → μ = √(3 × 5) = √15 ≈ 3.87 BM"],
      why_others_wrong="2.83 BM is for two unpaired electrons; 1.73 BM would need one unpaired electron in the "
                       "dichromate ion; the last option reverses the direction of the change.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', magnetic properties; potassium dichromate", seconds=45),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "In acidic solution, the dichromate ion is reduced to Cr³⁺ and the permanganate ion to Mn²⁺. How many moles of "
      "KMnO₄ have the same oxidising capacity (accept the same number of electrons) as 1 mol of K₂Cr₂O₇?",
      ["0.83 mol", "1.0 mol", "2.4 mol", v_2142], "D", v_2142,
      "Electrons accepted by dichromate and permanganate",
      "Each Cr goes from +6 to +3, so one Cr₂O₇²⁻ ion accepts 2 × 3 = 6 electrons. Each MnO₄⁻ goes from +7 to +2 and "
      "accepts 5 electrons.",
      ["Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O", "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O",
       "Moles of KMnO₄ = 6/5 = 1.2 mol"],
      why_others_wrong="0.83 mol inverts the ratio (5/6); 1.0 mol ignores the different electron counts; 2.4 mol counts "
                       "6 electrons per chromium atom.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxidising action of K₂Cr₂O₇ and KMnO₄", seconds=45),

    Q(T_DF, "Lanthanoids and actinoids", "Intermediate", "match_list",
      *ml("Match the actinoid in List-I with its ground-state electronic configuration in List-II (Rn = radon core).",
          ["Thorium (Z = 90)", "Uranium (Z = 92)", "Plutonium (Z = 94)", "Curium (Z = 96)"],
          ["[Rn] 5f⁶ 7s²", "[Rn] 6d² 7s²", "[Rn] 5f⁷ 6d¹ 7s²", "[Rn] 5f³ 6d¹ 7s²"],
          "II IV I III", ["II III I IV", "IV II I III", "II IV III I"], "C"),
      "Electronic configurations of actinoids",
      "Thorium has no 5f electron in its ground state (6d² 7s²). Uranium is 5f³ 6d¹ 7s². Plutonium places all its "
      "electrons beyond the 7s² pair in 5f (5f⁶ 7s²), while curium keeps a half-filled 5f⁷ and puts the next "
      "electron in 6d (5f⁷ 6d¹ 7s²).",
      ["Th (90): [Rn] 6d² 7s² (II)", "U (92): [Rn] 5f³ 6d¹ 7s² (IV)", "Pu (94): [Rn] 5f⁶ 7s² (I)",
       "Cm (96): [Rn] 5f⁷ 6d¹ 7s² (III)"],
      shortcut="Count electrons beyond the radon core (Z − 86): Th 4, U 6, Pu 8, Cm 10; each configuration in "
               "List-II adds up to one of these.",
      why_others_wrong="Codes that swap uranium and curium, or plutonium and curium, give a configuration whose "
                       "electron count does not match Z − 86.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the actinoids: electronic configurations", seconds=50),

    Q(T_DF, "Transition element trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the oxidation states of the d-block elements are correct?",
          [("The elements showing the greatest number of oxidation states occur in or near the middle of the 3d "
            "series.", True),
           ("Scandium and zinc show few oxidation states, scandium because it has few electrons to lose and zinc "
            "because it has a full d subshell.", True),
           ("In the d-block, higher oxidation states are favoured by the heavier members of a group, the opposite of "
            "the trend in the p-block.", True),
           ("Cr(VI) compounds are weaker oxidising agents than Mo(VI) and W(VI) compounds.", False)],
          [["a", "d"], ["b", "c", "d"], ["a", "b", "c", "d"]], "B"),
      "Trends in oxidation states of the transition elements",
      "Manganese, near the middle of the 3d series, shows every state from +2 to +7. Near the ends there are either "
      "too few electrons to lose or share (Sc, Ti) or too many d electrons and hence fewer orbitals available (Cu, "
      "Zn). In group 6, Mo(VI) and W(VI) are more stable than Cr(VI); so dichromate (Cr(VI)) in acid is a strong "
      "oxidising agent, whereas MoO₃ and WO₃ are not.",
      ["(a) true", "(b) true", "(c) true", "(d) false: Cr(VI) is the stronger oxidising agent"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', variation in oxidation states", seconds=55),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "Permanganate oxidises iodide to iodine in acidic solution (MnO₄⁻ → Mn²⁺), but to iodate, IO₃⁻, in neutral or "
      "faintly alkaline solution (MnO₄⁻ → MnO₂). For the same amount of KMnO₄, the ratio of the moles of iodide "
      "oxidised in acidic solution to that in neutral solution is:",
      ["1 : 10", "5 : 3", v_2145, "5 : 1"], "C", v_2145,
      "Electron balance in permanganate oxidations",
      "Count electrons per MnO₄⁻ and per I⁻ in each medium. In acid each MnO₄⁻ takes 5 electrons and each I⁻ gives "
      "1 (to ½I₂). In neutral solution each MnO₄⁻ takes 3 electrons and each I⁻ gives 6 (from −1 to +5 in IO₃⁻).",
      ["Acidic: 2MnO₄⁻ + 10I⁻ + 16H⁺ → 2Mn²⁺ + 5I₂ + 8H₂O → 5 mol I⁻ per mol MnO₄⁻",
       "Neutral: 2MnO₄⁻ + I⁻ + H₂O → 2MnO₂ + IO₃⁻ + 2OH⁻ → 0.5 mol I⁻ per mol MnO₄⁻",
       "Ratio = 5 : 0.5 = 10 : 1"],
      why_others_wrong="1 : 10 inverts the ratio; 5 : 3 compares only the electrons taken by MnO₄⁻ and ignores the "
                       "change in the iodide product; 5 : 1 assumes iodide gives one electron in both media.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate: oxidising properties", seconds=90),

    Q(T_DF, "Transition element trends", "Advanced", "assertion_reason",
      *ar("Iron(III) ions catalyse the reaction between iodide and persulphate ions, 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻.", True,
          "Fe³⁺ oxidises I⁻ to I₂ and is itself reduced to Fe²⁺, which is then oxidised back to Fe³⁺ by S₂O₈²⁻; this "
          "is possible because iron changes readily between the +2 and +3 oxidation states.", True, explains=True),
      "Catalytic action of transition metal ions",
      "Transition metal ions catalyse reactions largely because they can change their oxidation state. Here the "
      "catalyst is used up in the first step (2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂) and regenerated in the second "
      "(2Fe²⁺ + S₂O₈²⁻ → 2Fe³⁺ + 2SO₄²⁻). R describes exactly how the catalysis occurs.",
      ["Step 1: 2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂", "Step 2: 2Fe²⁺ + S₂O₈²⁻ → 2Fe³⁺ + 2SO₄²⁻",
       "Net: 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻, Fe³⁺ regenerated"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', catalytic properties", seconds=45),

    Q(T_DF, "Transition element trends", "Advanced", "direct",
      "The standard electrode potentials E°(M³⁺/M²⁺) of some 3d metals are: Cr −0.41 V, Mn +1.57 V, Fe +0.77 V, "
      "Co +1.97 V. Which of the following conclusions is correct?",
      ["Mn³⁺ is a weaker oxidising agent than Fe³⁺.",
       "Co²⁺ is oxidised to Co³⁺ more easily than Fe²⁺ is oxidised to Fe³⁺.",
       "Fe³⁺ is the strongest oxidising agent among the four M³⁺ ions.",
       "Cr²⁺ is the strongest reducing agent among the four M²⁺ ions."], "D",
      "Using E°(M³⁺/M²⁺) to compare oxidising and reducing power",
      "The more positive E°(M³⁺/M²⁺), the more readily M³⁺ is reduced (strong oxidising agent) and the harder it is "
      "to oxidise M²⁺. The most negative value, for chromium, means Cr²⁺ is the most easily oxidised, i.e. the "
      "strongest reducing agent (Cr²⁺ d⁴ → Cr³⁺ d³, a half-filled t₂g level).",
      ["Order of oxidising power of M³⁺: Co³⁺ > Mn³⁺ > Fe³⁺ > Cr³⁺",
       "Order of reducing power of M²⁺: Cr²⁺ > Fe²⁺ > Mn²⁺ > Co²⁺", "Strongest reducing agent: Cr²⁺"],
      why_others_wrong="Mn³⁺ (+1.57 V) is a stronger oxidising agent than Fe³⁺ (+0.77 V); Co²⁺ is harder to oxidise "
                       "than Fe²⁺ because its E° is more positive; Co³⁺, not Fe³⁺, is the strongest oxidising agent.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', trends in the M³⁺/M²⁺ standard electrode potentials",
      seconds=60),
]

# ================================================================ Coordination Compounds (2148-2161)
# 2149: anionic ligands in the list
lig_2149 = {"en": 0, "C2O4": -2, "py": 0, "CN": -1, "NH3": 0, "NO2": -1, "H2O": 0, "Cl": -1, "CO": 0}
v_2149 = str(sum(1 for c in lig_2149.values() if c < 0))
assert v_2149 == "4"
# 2152: [Cr(H2O)6]2+ high spin d4 (4 unpaired) vs [Cr(CN)6]4- low spin t2g4 (2 unpaired)
v_2152 = f"{bm(4) - bm(2):.2f} BM"
assert v_2152 == "2.07 BM" and f"{bm(4) - bm(3):.2f}" == "1.03"
# 2153: Ag+ + e- -> Ag from K[Ag(CN)2]; 965 C
m_2153 = F(965, 96500) * AM["Ag"]
assert m_2153 == F(108, 100)
v_2153 = f"{float(m_2153):.2f} g"
# 2158: d6, E(LS) - E(HS) = (-2.4 + 0.4) Do + 2P (two extra pairs in t2g6)
Do, Pe = 23000, 21000
cfse = lambda t2g, eg: F(-4, 10) * t2g + F(6, 10) * eg
pairs = lambda t2g, eg: max(0, t2g - 3) + max(0, eg - 2)
e_ls = cfse(6, 0) * Do + pairs(6, 0) * Pe
e_hs = cfse(4, 2) * Do + pairs(4, 2) * Pe
assert cfse(6, 0) == F(-24, 10) and cfse(4, 2) == F(-4, 10) and (pairs(6, 0), pairs(4, 2)) == (3, 1)
assert e_ls - e_hs == -4000
v_2158 = "Low spin, by 4000 cm⁻¹"

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The formula of tris(ethane-1,2-diamine)cobalt(III) sulphate is:",
      ["[Co(en)₃](SO₄)₃", "[Co(en)₃]₃(SO₄)₂", "[Co(en)₃]₂(SO₄)₃", "[Co(en)₂]₂(SO₄)₃"], "C",
      "Writing the formula from the name",
      "'Tris(ethane-1,2-diamine)' means three neutral en ligands, so the complex ion is [Co(en)₃]³⁺. Two such cations "
      "(total +6) are balanced by three sulphate ions (total −6).",
      ["Complex ion: [Co(en)₃]³⁺ (en is neutral)", "Charge balance: 2 × (+3) = 3 × (−2)", "Formula: [Co(en)₃]₂(SO₄)₃"],
      why_others_wrong="[Co(en)₃](SO₄)₃ and [Co(en)₃]₃(SO₄)₂ are not electrically neutral; [Co(en)₂]₂(SO₄)₃ has only "
                       "two en ligands, which would be 'bis'.",
      ncert=f"{NC12}, 'Coordination Compounds', formulas of mononuclear coordination entities", seconds=30),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "How many of the following ligands are anionic?\n"
      "H₂NCH₂CH₂NH₂ (en), C₂O₄²⁻, C₅H₅N (pyridine), CN⁻, NH₃, NO₂⁻, H₂O, Cl⁻, CO",
      ["1", "2", "3", "4"], "D", v_2149,
      "Classifying ligands by charge",
      "Ligands may be neutral molecules with a lone pair (en, pyridine, NH₃, H₂O, CO) or anions (C₂O₄²⁻, CN⁻, NO₂⁻, "
      "Cl⁻).",
      ["Neutral: en, pyridine, NH₃, H₂O, CO (5)", "Anionic: C₂O₄²⁻, CN⁻, NO₂⁻, Cl⁻ (4)"],
      why_others_wrong="Lower counts usually miss the oxalate or nitrite ion; en and pyridine are neutral even though "
                       "they are named as ligands without 'o' endings.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms: ligands", seconds=30),

    Q(T_CC, "Applications", "Basic", "statement_pair",
      *sp("EDTA is used in the treatment of lead poisoning.", True,
          "The coordination polyhedron of [PtCl₄]²⁻ is square planar.", True),
      "Chelate therapy; coordination polyhedra",
      "In chelate therapy, a chelating ligand binds a toxic metal so that it can be removed from the body; NCERT cites "
      "EDTA for lead poisoning. The four chloride ligands in [PtCl₄]²⁻ lie at the corners of a square around "
      "platinum, so its coordination polyhedron is square planar.",
      ["Statement I: true (chelate therapy)", "Statement II: true"],
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications; coordination polyhedron", seconds=30),

    Q(T_CC, "Werner's theory and ligands", "Basic", "assertion_reason",
      *ar("Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O, is a double salt, whereas [Co(NH₃)₆]Cl₃ is a coordination compound.",
          True,
          "In water, Mohr's salt dissociates completely into simple ions, whereas the [Co(NH₃)₆]³⁺ ion does not "
          "dissociate into Co³⁺ and NH₃.", True, explains=True),
      "Double salts and complexes",
      "Double salts such as Mohr's salt and carnallite exist only in the solid state and give all their simple ions "
      "(Fe²⁺, NH₄⁺, SO₄²⁻) in solution. A coordination compound keeps its complex ion intact in solution. That "
      "difference in behaviour in water is what classifies them, so R explains A.",
      ["Mohr's salt → Fe²⁺ + 2NH₄⁺ + 2SO₄²⁻ (all simple ions)", "[Co(NH₃)₆]Cl₃ → [Co(NH₃)₆]³⁺ + 3Cl⁻",
       "Complex ion stays intact → coordination compound"],
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory: double salts and complexes", seconds=35),

    N(T_CC, "Crystal field theory", "Intermediate",
      "[Cr(H₂O)₆]²⁺ is a high-spin complex and [Cr(CN)₆]⁴⁻ is a low-spin complex (Z of Cr = 24). The difference "
      "between their spin-only magnetic moments is about:",
      ["4.90 BM", "2.83 BM", v_2152, "1.03 BM"], "C", v_2152,
      "High-spin and low-spin d⁴ octahedral complexes",
      "Cr²⁺ is 3d⁴. With the weak field ligand H₂O (Δo < P) the fourth electron enters eg: t₂g³ eg¹, four unpaired "
      "electrons. With the strong field ligand CN⁻ (Δo > P) it pairs in t₂g: t₂g⁴ eg⁰, two unpaired electrons.",
      ["High spin: n = 4, μ = √24 ≈ 4.90 BM", "Low spin: n = 2, μ = √8 ≈ 2.83 BM", "Difference ≈ 2.07 BM"],
      why_others_wrong="4.90 BM treats the low-spin complex as diamagnetic; 2.83 BM applies the formula to the "
                       "difference in the number of unpaired electrons; 1.03 BM takes three unpaired electrons for the "
                       "low-spin complex.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=60),

    N(T_CC, "Applications", "Intermediate",
      "Articles are electroplated with silver from a solution of the complex K[Ag(CN)₂]. What mass of silver is "
      "deposited at the cathode when 965 C of charge is passed? (Ag = 108, F = 96500 C mol⁻¹)",
      ["0.54 g", "2.16 g", "10.8 g", v_2153], "D", v_2153,
      "Electroplating from a complex; Faraday's law",
      "Silver is +1 in [Ag(CN)₂]⁻. The complex keeps the concentration of free Ag⁺ low, which gives a smooth, even "
      "deposit, but each silver atom deposited still needs one electron.",
      ["Moles of electrons = 965/96500 = 0.010 mol", "Ag⁺ + e⁻ → Ag: 0.010 mol Ag", "Mass = 0.010 × 108 = 1.08 g"],
      why_others_wrong="0.54 g assumes two electrons per silver atom; 2.16 g assumes two silver atoms per electron; "
                       "10.8 g is a tenfold slip in the moles of electrons.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications", seconds=50),

    Q(T_CC, "Isomerism", "Intermediate", "multi_statement",
      *ms("Which of the following statements about structural isomerism in coordination compounds are correct?",
          [("Solvate isomerism is called hydrate isomerism when water is the solvent involved.", True),
           ("Linkage isomerism arises in a coordination compound that contains an ambidentate ligand.", True),
           ("Coordination isomerism arises from the interchange of ligands between the cationic and anionic entities "
            "of different metal ions in a complex.", True),
           ("Ionisation isomerism arises when the counter ion is itself a potential ligand and can displace a ligand, "
            "which then becomes the counter ion.", True),
           ("Stereoisomers have the same chemical bonds but different chemical formulae.", False)],
          [["a", "b", "e"], ["b", "c", "d"], ["a", "c", "d", "e"]], "C"),
      "Kinds of isomerism in coordination compounds",
      "Statements (a) to (d) are NCERT's descriptions of the four kinds of structural isomerism. Stereoisomers have the "
      "same chemical formula and the same chemical bonds but a different spatial arrangement, so (e) is false.",
      ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: same formula, different spatial arrangement"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=45),

    Q(T_CC, "Crystal field theory", "Intermediate", "direct",
      "For an octahedral complex, the number of unpaired electrons can differ between weak field (high spin) and strong "
      "field (low spin) ligands only when the metal ion has the configuration:",
      ["d¹ to d³", "d⁴ to d⁷", "d⁸ to d¹⁰", "d³ to d⁸"], "B",
      "When high-spin and low-spin arrangements are possible",
      "For d¹ to d³ the electrons simply occupy t₂g singly. From d⁴ the next electron can either enter eg (Δo < P) or "
      "pair in t₂g (Δo > P). For d⁸ to d¹⁰, t₂g is full and eg receives the rest in the same way whatever Δo is "
      "(t₂g⁶ eg², t₂g⁶ eg³, t₂g⁶ eg⁴).",
      ["d⁴: t₂g³ eg¹ or t₂g⁴", "d⁵: t₂g³ eg² or t₂g⁵", "d⁶: t₂g⁴ eg² or t₂g⁶", "d⁷: t₂g⁵ eg² or t₂g⁶ eg¹",
       "d¹–d³ and d⁸–d¹⁰: only one arrangement"],
      why_others_wrong="d¹–d³ and d⁸–d¹⁰ have only one possible arrangement; d³ to d⁸ wrongly includes d³ and d⁸.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Match the coordination compound in List-I with the description of its coordination entity in List-II.",
          ["K₄[Fe(CN)₆]", "[Co(NH₃)₅Cl]Cl₂", "[Ni(CO)₄]", "[Pt(NH₃)₂Cl₂]"],
          ["Heteroleptic, neutral", "Homoleptic, anionic", "Homoleptic, neutral", "Heteroleptic, cationic"],
          "II IV III I", ["II I III IV", "III IV II I", "IV II I III"], "D"),
      "Homoleptic and heteroleptic entities; charge of the entity",
      "A homoleptic entity has only one kind of donor group; a heteroleptic one has more than one kind. The charge of "
      "the entity is found from the metal's oxidation state and the ligand charges.",
      ["[Fe(CN)₆]⁴⁻: only CN⁻, charge −4 → homoleptic, anionic (II)",
       "[Co(NH₃)₅Cl]²⁺: NH₃ and Cl⁻, charge +2 → heteroleptic, cationic (IV)",
       "[Ni(CO)₄]: only CO, charge 0 → homoleptic, neutral (III)",
       "[Pt(NH₃)₂Cl₂]: NH₃ and Cl⁻, charge 0 → heteroleptic, neutral (I)"],
      why_others_wrong="Codes that call [Co(NH₃)₅Cl]²⁺ neutral forget that only two of the three chlorides are "
                       "counter ions; [Ni(CO)₄] has a single kind of ligand and is not heteroleptic.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=45),

    Q(T_CC, "Isomerism", "Intermediate", "assertion_reason",
      *ar("The square planar complex [Pt(NH₃)₂Cl₂] exists as cis and trans isomers.", True,
          "cis-Platin, the cis isomer of [Pt(NH₃)₂Cl₂], is used to inhibit the growth of tumours.", True),
      "Geometrical isomerism in square planar complexes",
      "In a square planar [MX₂L₂] complex the two Cl ligands can be next to each other (cis) or opposite each other "
      "(trans), so two geometrical isomers exist. R is a true statement about the medical use of the cis isomer; it "
      "says nothing about why two arrangements are possible, so it does not explain A.",
      ["Square planar MX₂L₂ → cis and trans", "R: medical use of one isomer, not the cause of isomerism"],
      ncert=f"{NC12}, 'Coordination Compounds', geometric isomerism; applications", seconds=35),

    N(T_CC, "Crystal field theory", "Advanced",
      "For a certain d⁶ metal ion in an octahedral field, Δo = 23000 cm⁻¹ and the pairing energy P = 21000 cm⁻¹. "
      "Taking into account both the crystal field stabilisation energy and the extra electron pairing, which "
      "arrangement is more stable, and by how much?",
      ["High spin, by 4000 cm⁻¹", v_2158, "Low spin, by 46000 cm⁻¹", "Low spin, by 2000 cm⁻¹"], "B", v_2158,
      "Balance between Δo and pairing energy",
      "In an octahedral field t₂g lies (2/5)Δo below and eg (3/5)Δo above the barycentre. High spin d⁶ is t₂g⁴ eg² "
      "with one pair; low spin d⁶ is t₂g⁶ with three pairs. The low-spin form gains crystal field stabilisation but "
      "must pay for two extra pairs.",
      ["High spin: CFSE = 4(−0.4Δo) + 2(0.6Δo) = −0.4Δo; 1 pair",
       "Low spin: CFSE = 6(−0.4Δo) = −2.4Δo; 3 pairs",
       "E(low) − E(high) = −2.0Δo + 2P = −46000 + 42000 = −4000 cm⁻¹",
       "Low spin is more stable by 4000 cm⁻¹ (consistent with Δo > P)"],
      why_others_wrong="'High spin' reverses the sign; 46000 cm⁻¹ ignores the pairing energy; 2000 cm⁻¹ counts only "
                       "one extra pair and half the CFSE difference.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory: octahedral complexes", seconds=110),

    Q(T_CC, "Isomerism", "Advanced", "multi_statement",
      *ms("Consider the octahedral complex [Co(NH₃)₄Cl₂]NO₂. Which of the following statements are correct?",
          [("It can exist as cis and trans isomers.", True),
           ("[Co(NH₃)₄Cl(NO₂)]Cl is an ionisation isomer of it.", True),
           ("The ionisation isomer [Co(NH₃)₄Cl(NO₂)]Cl can itself show linkage isomerism.", True),
           ("One mole of [Co(NH₃)₄Cl₂]NO₂ gives two moles of AgCl with excess AgNO₃ solution.", False),
           ("The coordination number of cobalt in it is 4.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "D"),
      "Combining geometrical, ionisation and linkage isomerism",
      "The entity [Co(NH₃)₄Cl₂]⁺ is of the type [MA₄B₂] and has cis and trans forms. Exchanging the counter ion NO₂⁻ "
      "with one coordinated Cl⁻ gives the ionisation isomer [Co(NH₃)₄Cl(NO₂)]Cl, and in that compound the ambidentate "
      "nitrite can bind through N or O. Both chlorides of the original compound are inside the coordination sphere, "
      "so it gives no AgCl. Four NH₃ and two Cl make the coordination number 6.",
      ["(a) true: [MA₄B₂]", "(b) true", "(c) true: NO₂⁻ / ONO⁻", "(d) false: Cl⁻ is coordinated, NO₂⁻ is the counter ion",
       "(e) false: CN = 6"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=80),

    Q(T_CC, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of [Pt(NH₃)₄][PtCl₄] is:",
      ["Tetraammineplatinum(II) tetrachloridoplatinum(II)", "Tetrachloridoplatinum(II) tetraammineplatinate(II)",
       "Tetraammineplatinum(II) tetrachloridoplatinate(II)", "Tetraammineplatinate(II) tetrachloridoplatinum(II)"],
      "C",
      "Naming a salt in which both ions are complex",
      "The cation is named first. [Pt(NH₃)₄]²⁺ is a cation, so platinum keeps its plain name. [PtCl₄]²⁻ is an anion, so "
      "the metal name takes the ending '-ate'. In each ion platinum is +2.",
      ["Cation [Pt(NH₃)₄]²⁺: x + 0 = +2 → Pt(II): tetraammineplatinum(II)",
       "Anion [PtCl₄]²⁻: x − 4 = −2 → Pt(II): tetrachloridoplatinate(II)",
       "Name: tetraammineplatinum(II) tetrachloridoplatinate(II)"],
      why_others_wrong="The anion needs the '-ate' ending; the cation must be named first; '-ate' is never used for a "
                       "cationic entity.",
      ncert=f"{NC12}, 'Coordination Compounds', naming of mononuclear coordination compounds", seconds=40),

    Q(T_CC, "Isomerism", "Advanced", "statement_pair",
      *sp("cis-[Co(NH₃)₄Cl₂]⁺ is optically inactive.", True,
          "cis-[Co(en)₂(NH₃)Cl]²⁺ is optically active.", True),
      "Optical activity of cis octahedral complexes",
      "cis-[Co(NH₃)₄Cl₂]⁺ has a mirror plane that contains the cobalt and both chlorine atoms, so it is superimposable "
      "on its mirror image. In cis-[Co(en)₂(NH₃)Cl]²⁺ the two didentate en rings are arranged in a propeller-like way "
      "(as in cis-[Co(en)₂Cl₂]⁺); it has no plane of symmetry and exists as a pair of enantiomers.",
      ["Statement I: unidentate ligands only, mirror plane → inactive: true",
       "Statement II: two chelate rings in cis arrangement, no mirror plane → active: true"],
      ncert=f"{NC12}, 'Coordination Compounds', optical isomerism", seconds=60),
]

# ================================================================ Purification and Characterisation (2162-2165)
# 2163: acetone-like sample: 0.29 g -> 0.66 g CO2, 0.27 g H2O; O by difference
mC = F(66, 100) * 12 / 44
mH = F(27, 100) * 2 / 18
mO = F(29, 100) - mC - mH
assert (mC, mH) == (F(18, 100), F(3, 100))
v_2163 = pct(mO / F(29, 100))
assert v_2163 == "27.6%" and pct(mC / F(29, 100)) == "62.1%"
assert pct((F(29, 100) - mC) / F(29, 100)) == "37.9%"                                   # H forgotten
assert pct((F(29, 100) - mC - F(27, 100) / 18) / F(29, 100)) == "32.8%"                 # H2O/18 slip
# 2165: C2H4Br2 from Carius + combustion + vapour density
s = F(188, 1000)
nBr = F(376, 1000) / 188
nC = F(88, 1000) / 44
nH = 2 * F(36, 1000) / 18
assert (nBr, nC, nH) == (F(2, 1000), F(2, 1000), F(4, 1000))
assert nBr * 80 + nC * 12 + nH * 1 == s                                                   # nothing else present
mn = min(nC, nH, nBr)
emp = (nC / mn, nH / mn, nBr / mn)
assert emp == (1, 2, 1)                                                                  # CH2Br
emp_mass = 12 + 2 + 80
k = 2 * 94 // emp_mass
assert emp_mass == 94 and k == 2
v_2165 = "C₂H₄Br₂"

QUESTIONS += [
    Q(T_PU, "Qualitative analysis", "Basic", "direct",
      "The sodium fusion extract of an organic compound gives a violet colour on adding sodium nitroprusside. The "
      "element shown to be present is:",
      ["Nitrogen", "Sulphur", "Chlorine", "Phosphorus"], "B",
      "Lassaigne's test for sulphur",
      "Sulphur in the compound is converted into sodium sulphide during fusion. Sulphide ions react with sodium "
      "nitroprusside to give a violet colour.",
      ["Na + S → Na₂S during fusion", "S²⁻ + [Fe(CN)₅NO]²⁻ → violet complex", "Sulphur present"],
      why_others_wrong="Nitrogen is detected by the Prussian blue test, chlorine by a white precipitate with AgNO₃ "
                       "and phosphorus by a yellow colour with ammonium molybdate.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis: test for "
            f"sulphur", seconds=20),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "0.29 g of an organic compound containing only carbon, hydrogen and oxygen gives 0.66 g of CO₂ and 0.27 g of "
      "H₂O on complete combustion. The percentage of oxygen in the compound is (C = 12, H = 1, O = 16):",
      [v_2163, "62.1%", "37.9%", "32.8%"], "A", v_2163,
      "Percentage of oxygen by difference",
      "Oxygen is usually estimated by difference: the masses of carbon and hydrogen found from CO₂ and H₂O are "
      "subtracted from the mass of the sample.",
      ["Mass of C = 0.66 × 12/44 = 0.18 g", "Mass of H = 0.27 × 2/18 = 0.03 g",
       "Mass of O = 0.29 − 0.18 − 0.03 = 0.08 g", "% O = 0.08/0.29 × 100 ≈ 27.6%"],
      why_others_wrong="62.1% is the percentage of carbon; 37.9% leaves out the hydrogen; 32.8% takes the mass of "
                       "hydrogen as 0.27/18 instead of 0.27 × 2/18.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis: oxygen",
      seconds=60),

    Q(T_PU, "Qualitative analysis", "Intermediate", "statement_pair",
      *sp("In the silver nitrate test on the sodium fusion extract, a white precipitate soluble in ammonium hydroxide "
          "shows chlorine, whereas a yellowish precipitate sparingly soluble in ammonium hydroxide shows bromine.",
          True,
          "In thin layer chromatography, the spots of the components always travel farther from the base line than the "
          "solvent front.", False),
      "Test for halogens; Rf in chromatography",
      "AgCl is white and dissolves in NH₄OH; AgBr is pale yellow and only sparingly soluble; AgI is yellow and "
      "insoluble. In TLC every component moves behind the solvent, so the distance moved by a spot is less than that "
      "of the solvent front, and the retardation factor Rf is less than 1.",
      ["Statement I: true", "Statement II: false; spots lag behind the solvent front (Rf < 1)"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', test for halogens; chromatography",
      seconds=40),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "An organic compound contains carbon, hydrogen and bromine only. In a Carius determination, 0.188 g of it gives "
      "0.376 g of AgBr. On complete combustion, 0.188 g of it gives 0.088 g of CO₂ and 0.036 g of H₂O. Its vapour "
      "density is 94. The molecular formula of the compound is (C = 12, H = 1, Br = 80, Ag = 108):",
      ["CH₂Br", v_2165, "C₂H₅Br", "C₂H₂Br₂"], "B", v_2165,
      "Molecular formula from Carius and combustion data",
      "Find the moles of each element in the same mass of sample, take the simplest ratio for the empirical formula, "
      "and scale it with the molar mass (2 × vapour density).",
      ["AgBr = 188 g mol⁻¹: n(Br) = 0.376/188 = 0.002 mol (0.160 g)",
       "n(C) = 0.088/44 = 0.002 mol (0.024 g); n(H) = 2 × 0.036/18 = 0.004 mol (0.004 g)",
       "Check: 0.160 + 0.024 + 0.004 = 0.188 g, so no other element is present",
       "C : H : Br = 0.002 : 0.004 : 0.002 = 1 : 2 : 1 → empirical formula CH₂Br (94 g mol⁻¹)",
       "Molar mass = 2 × 94 = 188 g mol⁻¹ → n = 188/94 = 2 → C₂H₄Br₂"],
      why_others_wrong="CH₂Br is only the empirical formula; C₂H₅Br (109 g mol⁻¹) and C₂H₂Br₂ (186 g mol⁻¹) do not fit "
                       "the element ratio or the vapour density.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis: halogens "
            f"(Carius method)",
      seconds=120),
]

# ================================================================ Some Basic Principles of Organic Chemistry (2166-2182)
# 2167: carbonyl compounds C4H8O: butanal, 2-methylpropanal, butan-2-one
carbonyl_c4h8o = ["CH3CH2CH2CHO", "(CH3)2CHCHO", "CH3COCH2CH3"]
v_2167 = str(len(carbonyl_c4h8o))
assert v_2167 == "3"
# 2171: 2-methylbutane (CH3)2CH-CH2-CH3: H on 1 deg, 2 deg, 3 deg carbons
h1, h2, h3 = 3 + 3 + 3, 2, 1
assert h1 + h2 + h3 == 12                                                                 # C5H12
v_2171 = f"{h1} : {h2} : {h3}"
assert v_2171 == "9 : 2 : 1"
# 2172: acids stronger than ethanoic acid (EWG or H in place of CH3: stronger; extra alkyl: weaker)
stronger = {"HCOOH": True, "ClCH2COOH": True, "CH3CH2COOH": False, "FCH2COOH": True, "Cl2CHCOOH": True,
            "(CH3)3CCOOH": False}
v_2172 = str(sum(stronger.values()))
assert v_2172 == "4"
# 2178: cycloalkanes C5H10 (structural isomers only)
rings = {5: ["cyclopentane"], 4: ["methylcyclobutane"],
         3: ["ethylcyclopropane", "1,1-dimethylcyclopropane", "1,2-dimethylcyclopropane"]}
v_2178 = str(sum(len(v) for v in rings.values()))
assert v_2178 == "5"

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of (CH₃)₂CH–CH₂–C≡N is:",
      ["2-Methylbutanenitrile", "4-Methylbutanenitrile", "1-Cyano-2-methylpropane", "3-Methylbutanenitrile"], "D",
      "Naming nitriles",
      "For a nitrile, the carbon of the –C≡N group is part of the parent chain and is numbered C-1; the suffix is "
      "'-nitrile' added to the name of the alkane.",
      ["Chain including the CN carbon: N≡C1–C2H₂–C3H(CH₃)–C4H₃", "Four carbons → butanenitrile",
       "Methyl on C-3 → 3-methylbutanenitrile"],
      why_others_wrong="2-methyl numbers the chain from the wrong end; 4-methylbutane would make the chain longer; "
                       "'cyano' is used as a prefix only when a higher-priority group is present.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of compounds with "
            f"functional groups", seconds=35),

    N(T_GO, "Isomerism", "Basic",
      "How many structural isomers with the molecular formula C₄H₈O are aldehydes or ketones?",
      ["2", "3", "4", "5"], "B", v_2167,
      "Counting carbonyl isomers",
      "C₄H₈O fits CₙH₂ₙO, the formula of saturated open-chain aldehydes and ketones.",
      ["Aldehydes: butanal, CH₃CH₂CH₂CHO; 2-methylpropanal, (CH₃)₂CHCHO",
       "Ketone: butan-2-one, CH₃COCH₂CH₃ (a ketone needs C=O inside the chain)", "Total = 3"],
      why_others_wrong="2 forgets the branched aldehyde or the ketone; 4 or 5 count 'butan-1-one' or repeat butan-2-one "
                       "numbered from the other end, which is the same compound.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', isomerism", seconds=40),

    Q(T_GO, "Types of organic reactions", "Basic", "statement_pair",
      *sp("Organic reactions that proceed by homolytic fission of bonds are called free radical, homopolar or non-polar "
          "reactions.", True,
          "Organic reactions that proceed by heterolytic fission of bonds are called ionic, heteropolar or polar "
          "reactions.", True),
      "Classifying reactions by the type of bond fission",
      "In homolytic fission each atom keeps one electron of the shared pair and neutral free radicals are formed; the "
      "reactions are called free radical (homopolar, non-polar) reactions. Heterolytic fission gives ions such as "
      "carbocations and carbanions, and these reactions are called ionic (heteropolar, polar) reactions.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fission of a covalent bond",
      seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "match_list",
      *ml("Match the carbon–carbon bond in List-I with its bond length in List-II.",
          ["C–C bond in ethane", "C=C bond in ethene", "C≡C bond in ethyne", "Carbon–carbon bond in benzene"],
          ["139 pm", "154 pm", "120 pm", "134 pm"],
          "II IV III I", ["II I III IV", "IV II III I", "II IV I III"], "C"),
      "Bond length and bond order",
      "The more bonds between two carbon atoms (and the greater the s character of the hybrid orbitals), the shorter "
      "the bond: C–C 154 pm > C=C 134 pm > C≡C 120 pm. All six C–C bonds of benzene have the same length, 139 pm, "
      "between the single and double bond values, because of resonance.",
      ["Ethane C–C: 154 pm (II)", "Ethene C=C: 134 pm (IV)", "Ethyne C≡C: 120 pm (III)", "Benzene: 139 pm (I)"],
      why_others_wrong="Codes that give benzene 134 pm treat it as having isolated double bonds (Kekulé); giving "
                       "ethyne 139 pm ignores that the triple bond is the shortest.",
      ncert=f"{NC11}, 'Hydrocarbons', structure of ethene, ethyne and benzene", seconds=40),

    Q(T_GO, "Types of organic reactions", "Basic", "assertion_reason",
      *ar("The reaction of ethene with bromine to give 1,2-dibromoethane is an addition reaction.", True,
          "Ethene is a planar molecule in which all six atoms lie in the same plane.", True),
      "Addition reactions",
      "Ethene adds Br₂ across its C=C double bond, so the two reactants combine into one product: an addition "
      "reaction, made possible by the π bond. R is a correct statement about the shape of ethene, but the planar shape "
      "is not why the reaction is an addition; R does not explain A.",
      ["CH₂=CH₂ + Br₂ → BrCH₂–CH₂Br: two molecules give one → addition",
       "R: true (sp² carbons, planar) but about geometry, not reaction type"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', types of organic reactions",
      seconds=30),

    N(T_GO, "Hybridisation and functional groups", "Intermediate",
      "In 2-methylbutane, (CH₃)₂CH–CH₂–CH₃, the ratio of the numbers of hydrogen atoms attached to primary, "
      "secondary and tertiary carbon atoms is:",
      ["6 : 2 : 1", "9 : 1 : 2", "3 : 2 : 1", v_2171], "D", v_2171,
      "Primary, secondary and tertiary hydrogens",
      "A hydrogen is called primary, secondary or tertiary according to the carbon it is attached to (bonded to one, "
      "two or three other carbons).",
      ["Three CH₃ groups (primary carbons): 3 × 3 = 9 H", "One CH₂ (secondary carbon): 2 H",
       "One CH (tertiary carbon): 1 H", "Ratio 9 : 2 : 1 (total 12 H, C₅H₁₂)"],
      why_others_wrong="6 : 2 : 1 misses the CH₃ of the ethyl group; 9 : 1 : 2 swaps secondary and tertiary; 3 : 2 : 1 "
                       "counts primary carbons, not hydrogens.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', classification of carbon atoms",
      seconds=40),

    N(T_GO, "Electronic effects", "Intermediate",
      "How many of the following acids are stronger than ethanoic acid, CH₃COOH?\n"
      "HCOOH, ClCH₂COOH, CH₃CH₂COOH, FCH₂COOH, Cl₂CHCOOH, (CH₃)₃CCOOH",
      ["2", "3", v_2172, "5"], "C", v_2172,
      "Inductive effect and acid strength",
      "Electron-withdrawing (−I) groups stabilise the carboxylate ion and increase acid strength; electron-releasing "
      "(+I) alkyl groups do the opposite. Methanoic acid lacks the +I methyl group of ethanoic acid, so it is the "
      "stronger acid.",
      ["Stronger: HCOOH (no +I alkyl group), ClCH₂COOH, FCH₂COOH, Cl₂CHCOOH (−I halogens)",
       "Weaker: CH₃CH₂COOH and (CH₃)₃CCOOH (more +I alkyl)", "Count = 4"],
      why_others_wrong="2 or 3 usually leave out HCOOH or the dichloro acid; 5 wrongly counts propanoic acid, whose "
                       "ethyl group releases electrons.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', effect of substituents on acidity", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of OHC–CH₂–CH₂–C≡N is:",
      ["4-Oxobutanenitrile", "3-Cyanopropanal", "3-Formylpropanenitrile", "4-Cyanobutanal"], "A",
      "Priority of functional groups",
      "The nitrile group ranks above the aldehyde group, so –CN is the principal group (suffix '-nitrile') and the "
      "–CHO carbon, which is a chain carbon, is shown by the prefix 'oxo'.",
      ["Principal group: –C≡N; its carbon is C-1", "Chain: N≡C1–C2–C3–C4HO → butanenitrile",
       "C-4 carries =O → 4-oxobutanenitrile"],
      why_others_wrong="'3-Cyanopropanal' makes the lower-priority aldehyde the suffix; 'formyl' is used only when the "
                       "CHO carbon is outside the parent chain; '4-cyanobutanal' counts one carbon too many.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature: polyfunctional "
            f"compounds", seconds=45),

    Q(T_GO, "Reactive intermediates", "Intermediate", "assertion_reason",
      *ar("Anhydrous AlCl₃ acts as a nucleophile.", False,
          "The aluminium atom in AlCl₃ has only six electrons in its valence shell.", True),
      "Electrophiles and nucleophiles",
      "A nucleophile donates an electron pair; an electrophile accepts one. Aluminium in AlCl₃ has an incomplete "
      "octet and accepts an electron pair, so AlCl₃ is an electrophile (as in Friedel–Crafts reactions). A is false; "
      "R is true.",
      ["Al in AlCl₃: 3 bonds, 6 valence electrons", "Electron-pair acceptor → electrophile, not nucleophile"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "multi_statement",
      *ms("Which of the following structures are correctly named?",
          [("CH₃–O–CH₂–CH₂–CH₃: 1-methoxypropane", True),
           ("Br–CH₂–CH₂–COOH: 3-bromopropanoic acid", True),
           ("(CH₃)₃C–COOH: 2,2-dimethylpropanoic acid", True),
           ("CH₃–CH(CH₃)–CO–CH₃: 2-methylbutan-3-one", False),
           ("Cl–CH₂–CH₂–CHO: 3-chloropropanal", True)],
          [["a", "b", "d"], ["b", "c", "d", "e"], ["a", "c", "e"]], "B"),
      "IUPAC names of compounds with functional groups",
      "The chain is numbered so that the principal functional group gets the lowest locant. In (d) the carbonyl must "
      "be at C-2, so the name is 3-methylbutan-2-one.",
      ["(a) true", "(b) true: COOH carbon is C-1", "(c) true", "(d) false: 3-methylbutan-2-one",
       "(e) true: CHO carbon is C-1"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature", seconds=55),

    Q(T_GO, "Isomerism", "Intermediate", "statement_pair",
      *sp("1-Chloropropane, CH₃CH₂CH₂Cl, and 2-chloropropane, CH₃CHClCH₃, differ only in where the chlorine atom "
          "sits on the same three-carbon chain.", True,
          "Hexane and 2-methylpentane, which have different carbon skeletons, are classified as position isomers.",
          False),
      "Position and chain isomerism",
      "Compounds with the same carbon skeleton but a substituent or functional group at a different position are "
      "position isomers, as the two chloropropanes are. Hexane (unbranched) and 2-methylpentane (branched) have "
      "different carbon skeletons, so they are chain isomers, not position isomers.",
      ["Statement I: same chain, Cl on C-1 vs C-2: true",
       "Statement II: different skeletons → chain isomers, so the classification is false"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "match_list",
      *ml("Match the compound in List-I with the kinds of hybridised carbon atoms present in it (List-II).",
          ["Propyne, CH₃–C≡CH", "Propenenitrile, CH₂=CH–C≡N", "Propanal, CH₃CH₂CHO", "Benzene"],
          ["sp² only", "sp³ and sp²", "sp² and sp", "sp³ and sp"],
          "IV III II I", ["IV II III I", "III IV II I", "IV III I II"], "D"),
      "Hybridisation of carbon in different functional groups",
      "A carbon with four σ bonds is sp³, a carbon in a double bond is sp², and a carbon in a triple bond is sp.",
      ["Propyne: CH₃ sp³; both C≡C carbons sp → sp³ and sp (IV)",
       "Propenenitrile: CH₂=CH sp², C≡N carbon sp → sp² and sp (III)",
       "Propanal: CH₃, CH₂ sp³; CHO sp² → sp³ and sp² (II)", "Benzene: all sp² (I)"],
      why_others_wrong="Treating the nitrile carbon as sp² or the CHO carbon as sp³ gives the wrong pairings.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', shapes of carbon compounds",
      seconds=45),

    N(T_GO, "Isomerism", "Advanced",
      "How many structural isomers with the molecular formula C₅H₁₀ are cycloalkanes (saturated ring compounds)? "
      "Do not count stereoisomers separately.",
      ["3", "4", v_2178, "6"], "C", v_2178,
      "Ring-size and position isomers of cycloalkanes",
      "C₅H₁₀ fits CₙH₂ₙ, the formula of cycloalkanes as well as alkenes. Work through the possible ring sizes and place "
      "the remaining carbons as substituents.",
      ["Five-membered ring: cyclopentane", "Four-membered ring: methylcyclobutane",
       "Three-membered ring: ethylcyclopropane, 1,1-dimethylcyclopropane, 1,2-dimethylcyclopropane",
       "Total = 1 + 1 + 3 = 5"],
      why_others_wrong="3 or 4 miss the dimethylcyclopropanes or methylcyclobutane; 6 counts cis- and "
                       "trans-1,2-dimethylcyclopropane separately, which the question excludes.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=70),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₃–CH(CH₃)–CH(CH₃)–CH₂–CH(CH₂CH₃)–CH₃ is:",
      ["5-Ethyl-2,3-dimethylhexane", "3,5,6-Trimethylheptane", "2-Ethyl-4,5-dimethylhexane",
       "2,3,5-Trimethylheptane"], "D",
      "Choosing the longest chain and the lowest locants",
      "The longest chain runs through the ethyl group and has seven carbons. Numbering from the end nearer the first "
      "branch gives the methyl groups the locants 2, 3 and 5, lower at the first point of difference than 3, 5, 6.",
      ["Longest chain: CH₃–CH–CH–CH₂–CH–CH₂–CH₃ (7 C, heptane)",
       "Substituents: CH₃ on three carbons", "Left to right: 2, 3, 5; right to left: 3, 5, 6",
       "Name: 2,3,5-trimethylheptane"],
      why_others_wrong="'Hexane' names miss the longer chain through the ethyl group (and an ethyl at C-2 is never "
                       "correct); 3,5,6 numbers from the wrong end.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of branched alkanes",
      seconds=60),

    Q(T_GO, "Types of organic reactions", "Advanced", "multi_statement",
      *ms("For the base-catalysed reaction CH₃CHO + HCN → CH₃CH(OH)CN, which of the following statements are correct?",
          [("The cyanide ion acts as the nucleophile.", True),
           ("The carbonyl carbon is the electrophilic centre that is attacked.", True),
           ("The carbonyl carbon changes from sp² to sp³ hybridisation.", True),
           ("The reaction is a nucleophilic substitution.", False),
           ("The product contains a carbon atom bonded to four different groups.", True)],
          [["a", "b", "d"], ["a", "c", "d", "e"], ["b", "c", "e"]], "B"),
      "Nucleophilic addition to the carbonyl group",
      "The base produces CN⁻, which attacks the electron-deficient carbonyl carbon; the oxygen then takes up H⁺. Two "
      "molecules combine into one, so it is a nucleophilic addition. The carbonyl carbon goes from trigonal (sp²) to "
      "tetrahedral (sp³) and carries CH₃, H, OH and CN, four different groups.",
      ["(a) true", "(b) true", "(c) true", "(d) false: addition, not substitution",
       "(e) true: C bonded to CH₃, H, OH, CN"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition reactions", seconds=60),

    Q(T_GO, "Isomerism", "Advanced", "assertion_reason",
      *ar("2-Methylbut-2-ene, (CH₃)₂C=CH–CH₃, does not show geometrical isomerism, although both of its doubly bonded "
          "carbon atoms carry alkyl groups.", True,
          "One of its doubly bonded carbon atoms carries two identical groups (two methyl groups).", True,
          explains=True),
      "Condition for geometrical isomerism",
      "Cis and trans forms exist only when each carbon of the double bond carries two different groups. In "
      "2-methylbut-2-ene, C-2 bears two CH₃ groups, so interchanging them gives the same molecule. R is exactly why "
      "A holds.",
      ["C-2: CH₃ and CH₃ (identical)", "C-3: H and CH₃", "One carbon with identical groups → no cis/trans"],
      ncert=f"{NC11}, 'Hydrocarbons', geometrical isomerism in alkenes", seconds=40),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("In propene, CH₃–CH=CH₂, the three C–H bonds of the methyl group can take part in hyperconjugation with the "
          "π bond.", True,
          "As a result of this hyperconjugation, the =CH₂ carbon of propene acquires some negative charge.",
          True),
      "Hyperconjugation in alkenes",
      "The σ electrons of the C–H bonds of an alkyl group attached to a C=C bond are partly delocalised into the π "
      "system. In the hyperconjugation structures of propene, H⁺ is shown separated from the methyl carbon, the "
      "double bond shifts to C2–C3, and the negative charge appears on the terminal CH₂ carbon (C-1).",
      ["Statement I: three α C–H bonds → true",
       "Statement II: structure H⁺ ⁻CH₂–CH=CH₂ (old methyl carbon now double bonded), charge on the former =CH₂ carbon → true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hyperconjugation", seconds=50),
]

# ================================================================ Hydrocarbons (2183-2196)
# 2184: C2H5Cl + H2 (Zn, H+) -> C2H6 + HCl
n_2184 = F(645, 100) / mm(C=2, H=5, Cl=1)
assert n_2184 == F(1, 10)
v_2184 = g(n_2184 * mm(C=2, H=6))
assert v_2184 == "3.0 g"
# 2187: CH3C=CH + 2HBr -> CH3CBr2CH3
n_2187 = F(4) / mm(C=3, H=4)
v_2187 = g(2 * n_2187 * mm(H=1, Br=1))
assert n_2187 == F(1, 10) and v_2187 == "16.2 g"
# 2188: terminal alkynes (acidic H on sp carbon)
alkynes = {"ethyne": True, "propyne": True, "but-1-yne": True, "but-2-yne": False, "pent-2-yne": False,
           "3-methylbut-1-yne": True}
v_2188 = str(sum(alkynes.values()))
assert v_2188 == "4"
# 2193: (CH3)2C=CH-CH3 + [O] (KMnO4/H+) -> (CH3)2CO + CH3COOH
n_2193 = F(7) / mm(C=5, H=10)
v_2193 = g(n_2193 * mm(C=3, H=6, O=1))
assert n_2193 == F(1, 10) and v_2193 == "5.8 g" and g(n_2193 * mm(C=2, H=4, O=2)) == "6.0 g"

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "In the conformations of ethane, the repulsive interaction between the electron clouds of the C–H bonds on the "
      "two carbon atoms, which affects the stability of a conformation, is called:",
      ["Torsional strain", "Angle strain", "Steric inhibition of resonance", "Hyperconjugation"], "A",
      "Torsional strain in ethane",
      "When the C–H bonds of the two carbons face each other (eclipsed form) their electron clouds repel most. NCERT "
      "calls this repulsion torsional strain; it is least in the staggered form, which is therefore more stable.",
      ["Eclipsed: maximum torsional strain", "Staggered: minimum torsional strain",
       "Energy difference about 12.5 kJ mol⁻¹"],
      why_others_wrong="Angle strain arises from distorted bond angles in small rings; steric inhibition of resonance "
                       "and hyperconjugation are electronic effects, not this repulsion.",
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane", seconds=25),

    N(T_HC, "Alkanes and conformations", "Basic",
      "Alkyl halides (other than fluorides) are reduced to alkanes by zinc and dilute hydrochloric acid. The mass of "
      "ethane obtained from 6.45 g of chloroethane, assuming complete conversion, is (C = 12, H = 1, Cl = 35.5):",
      ["1.5 g", v_2184, "6.0 g", "2.8 g"], "B", v_2184,
      "Preparation of alkanes by reduction of alkyl halides",
      "Each chloroethane molecule gives one ethane molecule: CH₃CH₂Cl + H₂ (Zn, H⁺) → CH₃CH₃ + HCl.",
      ["Molar mass of C₂H₅Cl = 64.5 g mol⁻¹; n = 6.45/64.5 = 0.10 mol", "n(C₂H₆) = 0.10 mol",
       "Mass = 0.10 × 30 = 3.0 g"],
      why_others_wrong="1.5 g and 6.0 g use a 1 : 2 or 2 : 1 ratio, as in the Wurtz reaction; 2.8 g is the mass of "
                       "ethene, not ethane.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes from alkyl halides", seconds=40),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "assertion_reason",
      *ar("Propene reacts with cold, dilute, aqueous alkaline KMnO₄ (Baeyer's reagent) to give propane-1,2-diol.", True,
          "Propene is a gas at room temperature.", True),
      "Oxidation of alkenes by Baeyer's reagent",
      "Cold dilute alkaline KMnO₄ adds two –OH groups across the C=C bond (the purple colour is discharged), giving "
      "the vicinal glycol CH₃CH(OH)CH₂OH. R is a correct physical fact about propene, but its being a gas has nothing "
      "to do with this reaction.",
      ["CH₃–CH=CH₂ + H₂O + [O] → CH₃–CH(OH)–CH₂OH", "R: true, unrelated to the reaction"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: oxidation", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "statement_pair",
      *sp("Among the alkenes, the first three members are gases, the next fourteen are liquids and the higher members "
          "are solids.", True,
          "Alkenes are highly soluble in water.", False),
      "Physical properties of alkenes",
      "NCERT describes the physical state of alkenes exactly as in Statement I. Alkenes, like alkanes, are non-polar "
      "or weakly polar and are insoluble in water but soluble in non-polar organic solvents.",
      ["Statement I: true", "Statement II: false; alkenes are insoluble in water"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: physical properties", seconds=25),

    N(T_HC, "Alkynes", "Intermediate",
      "Propyne reacts with an excess of HBr (no peroxide) to give 2,2-dibromopropane. The minimum mass of HBr needed "
      "for 4.0 g of propyne is (C = 12, H = 1, Br = 80):",
      ["8.1 g", "32.4 g", "16.0 g", v_2187], "D", v_2187,
      "Addition of two molecules of HX to an alkyne",
      "The triple bond takes up two molecules of HBr, both following Markovnikov's rule: CH₃C≡CH → CH₃CBr=CH₂ → "
      "CH₃CBr₂CH₃.",
      ["Molar mass of propyne = 40 g mol⁻¹; n = 4.0/40 = 0.10 mol", "HBr needed = 2 × 0.10 = 0.20 mol",
       "Mass = 0.20 × 81 = 16.2 g"],
      why_others_wrong="8.1 g adds only one HBr; 32.4 g adds four; 16.0 g is the mass of Br₂ for one addition, not HBr.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of hydrogen halides", seconds=45),

    N(T_HC, "Alkynes", "Intermediate",
      "How many of the following react with sodamide (NaNH₂) to form a sodium salt?\n"
      "Ethyne, propyne, but-1-yne, but-2-yne, pent-2-yne, 3-methylbut-1-yne",
      ["2", "3", v_2188, "5"], "C", v_2188,
      "Acidic character of terminal alkynes",
      "Only a hydrogen attached to a triply bonded carbon is acidic enough to be removed by NaNH₂. The sp carbon has "
      "50% s character and holds the bonding pair close to itself. Internal alkynes have no such hydrogen.",
      ["Terminal (≡C–H present): ethyne, propyne, but-1-yne, 3-methylbut-1-yne",
       "Internal: but-2-yne, pent-2-yne", "Count = 4"],
      why_others_wrong="2 or 3 leave out ethyne or the branched terminal alkyne; 5 counts an internal alkyne.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: acidic character", seconds=40),

    Q(T_HC, "Alkynes", "Intermediate", "direct",
      "Which of the following is the correct order of acidic character?",
      ["CH₃–C≡CH > HC≡CH > CH₃–C≡C–CH₃", "CH₃–C≡C–CH₃ > CH₃–C≡CH > HC≡CH", "HC≡CH > CH₃–C≡C–CH₃ > CH₃–C≡CH",
       "HC≡CH > CH₃–C≡CH ≫ CH₃–C≡C–CH₃"], "D",
      "Acidity of alkynes",
      "Acidity comes from H attached to the sp carbon. Ethyne has two such hydrogens; in propyne the electron-releasing "
      "methyl group lowers the acidity; but-2-yne has no acetylenic hydrogen and is far less acidic.",
      ["Ethyne: two ≡C–H, no alkyl group", "Propyne: one ≡C–H, +I methyl group", "But-2-yne: no ≡C–H"],
      why_others_wrong="Placing propyne above ethyne ignores the +I effect of CH₃; placing but-2-yne high ignores that it "
                       "has no hydrogen on an sp carbon.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: acidic character of alkyne", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with the type of reaction it is in List-II.",
          ["CH₄ + Cl₂ in diffused sunlight → CH₃Cl + HCl", "C₆H₆ + CH₃Cl (anhydrous AlCl₃) → C₆H₅CH₃ + HCl",
           "CH₂=CH₂ + HBr → CH₃CH₂Br", "CH₃CH=CH₂ + HBr (benzoyl peroxide) → CH₃CH₂CH₂Br"],
          ["Free radical addition", "Electrophilic addition", "Electrophilic substitution",
           "Free radical substitution"],
          "IV III II I", ["IV II III I", "III IV I II", "IV III I II"], "A"),
      "Classifying reactions of hydrocarbons by mechanism",
      "Halogenation of alkanes in light is a free radical chain substitution. Friedel–Crafts alkylation substitutes an "
      "H of benzene through the electrophile formed with AlCl₃. HBr adds to ethene through a carbocation (electrophilic "
      "addition), whereas in the presence of a peroxide it adds to propene through bromine free radicals.",
      ["Chlorination of methane: free radical substitution (IV)", "Friedel–Crafts: electrophilic substitution (III)",
       "HBr + ethene: electrophilic addition (II)", "HBr + propene with peroxide: free radical addition (I)"],
      why_others_wrong="Codes that call Friedel–Crafts an addition, or that treat the peroxide reaction as ionic, mix "
                       "up the mechanisms.",
      ncert=f"{NC11}, 'Hydrocarbons', reactions of alkanes, alkenes and arenes", seconds=45),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "multi_statement",
      *ms("Which of the following give benzene or a benzene derivative as stated?",
          [("Ethyne passed through a red-hot iron tube at 873 K gives benzene.", True),
           ("Sodium benzoate heated with soda lime gives benzene.", True),
           ("Phenol vapour passed over heated zinc dust gives benzene.", True),
           ("Benzene treated with CH₃Cl and anhydrous AlCl₃ gives toluene.", True),
           ("Benzene treated with chlorine in ultraviolet light gives chlorobenzene by substitution.", False)],
          [["a", "b", "e"], ["b", "c", "d", "e"], ["a", "c", "e"]], "D"),
      "Preparation and reactions of benzene",
      "Benzene is made by cyclic polymerisation of ethyne, by decarboxylation of sodium benzoate with soda lime, and by "
      "reduction of phenol with zinc dust. Friedel–Crafts alkylation with CH₃Cl gives toluene. In ultraviolet light, "
      "however, benzene adds three molecules of chlorine to give benzene hexachloride, C₆H₆Cl₆; this is addition, "
      "not substitution.",
      ["(a) 3HC≡CH → C₆H₆: true", "(b) C₆H₅COONa + NaOH (CaO) → C₆H₆ + Na₂CO₃: true",
       "(c) C₆H₅OH + Zn → C₆H₆ + ZnO: true", "(d) Friedel–Crafts alkylation: true",
       "(e) false: UV light gives addition (C₆H₆Cl₆)"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: preparation and chemical properties", seconds=55),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "statement_pair",
      *sp("Aromatic hydrocarbons burn with a sooty flame.", True,
          "Aromatic hydrocarbons are immiscible with water but are readily miscible with organic solvents.", True),
      "Physical properties of arenes",
      "NCERT lists both properties: arenes are non-polar, usually colourless liquids or solids with a characteristic "
      "aroma, immiscible with water and miscible with organic solvents, and they burn with a sooty flame.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: physical properties", seconds=25),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "An open-chain alkene X, C₅H₁₀, is oxidised by acidic potassium permanganate to give a mixture of propanone and "
      "ethanoic acid only. The mass of propanone obtained from 7.0 g of X, assuming complete reaction, is "
      "(C = 12, H = 1, O = 16):",
      [v_2193, "6.0 g", "2.9 g", "11.6 g"], "A", v_2193,
      "Oxidative cleavage of alkenes by acidic KMnO₄",
      "Acidic KMnO₄ breaks the C=C bond: a carbon carrying two alkyl groups ends up as a ketone, and a carbon carrying "
      "one alkyl group and one H ends up as a carboxylic acid. Propanone plus ethanoic acid points to "
      "(CH₃)₂C=CH–CH₃, 2-methylbut-2-ene.",
      ["(CH₃)₂C= → (CH₃)₂C=O (propanone); =CH–CH₃ → CH₃COOH", "X = 2-methylbut-2-ene, M = 70 g mol⁻¹",
       "n(X) = 7.0/70 = 0.10 mol → 0.10 mol propanone", "Mass = 0.10 × 58 = 5.8 g"],
      why_others_wrong="6.0 g is the mass of ethanoic acid; 2.9 g halves the moles; 11.6 g assumes two propanone units "
                       "per molecule, as for 2,3-dimethylbut-2-ene (C₆H₁₂).",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: oxidation with acidic KMnO₄", seconds=90),

    Q(T_HC, "Alkanes and conformations", "Advanced", "assertion_reason",
      *ar("The staggered and eclipsed conformations of ethane cannot be separated and isolated at room temperature.",
          True,
          "The energy barrier to rotation about the C–C single bond of ethane is only about 12.5 kJ mol⁻¹, so the "
          "conformations change into one another rapidly.", True, explains=True),
      "Interconversion of conformations",
      "Conformations differ only by rotation about a σ bond. For ethane the difference in energy between the staggered "
      "and eclipsed forms is so small that ordinary thermal energy keeps them interconverting, so they cannot be "
      "separated. R gives the reason.",
      ["Rotation barrier ≈ 12.5 kJ mol⁻¹ (small)", "Rapid interconversion at room temperature",
       "→ not separable"],
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane: relative stability", seconds=35),

    Q(T_HC, "Alkynes", "Advanced", "direct",
      "An alkyne X, C₄H₆, does not react with sodamide. X is hydrogenated with H₂ over palladium on charcoal partly "
      "deactivated with quinoline, giving Y, which shows geometrical isomerism. Y is subjected to ozonolysis (O₃, then "
      "Zn/H₂O). The product is:",
      ["Propanal and methanal", "Butan-2-one", "Ethanal only", "Butanal"], "C",
      "Identifying an internal alkyne and following it through reduction and ozonolysis",
      "An alkyne C₄H₆ with no acidic hydrogen must be the internal alkyne but-2-yne. Lindlar-type hydrogenation stops "
      "at the alkene and gives cis-but-2-ene (which has cis and trans forms). Ozonolysis cleaves CH₃CH=CHCH₃ into two "
      "molecules of ethanal.",
      ["X: CH₃–C≡C–CH₃ (no ≡C–H)", "Y: cis-CH₃CH=CHCH₃", "Ozonolysis: 2 CH₃CHO"],
      why_others_wrong="Propanal and methanal come from but-1-ene, which would arise from but-1-yne (which reacts with "
                       "NaNH₂); butan-2-one and butanal come from hydration, not ozonolysis.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes and alkenes: reactions", seconds=60),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "match_list",
      *ml("Match the reaction in List-I with its main product in List-II.",
          ["Ethyne + H₂ (Pd/charcoal deactivated with quinoline)", "But-2-yne + sodium in liquid ammonia",
           "Ethene + H₂ (finely divided Ni)", "Benzene + H₂ (Ni, high temperature and pressure)"],
          ["Cyclohexane", "Ethane", "trans-But-2-ene", "Ethene"],
          "IV III II I", ["II III IV I", "IV I II III", "II I IV III"], "D"),
      "Controlled and complete hydrogenation",
      "The deactivated (Lindlar-type) catalyst stops the reduction of an alkyne at the alkene. Sodium in liquid "
      "ammonia also stops at the alkene but gives the trans isomer. Ordinary metal catalysts saturate C=C fully, and "
      "benzene adds three H₂ only under vigorous conditions.",
      ["Ethyne → ethene (IV)", "But-2-yne → trans-but-2-ene (III)", "Ethene → ethane (II)",
       "Benzene → cyclohexane (I)"],
      why_others_wrong="Codes giving ethane from the deactivated catalyst ignore that the catalyst is poisoned to stop "
                       "at the alkene; cyclohexane does not come from an alkene of two or four carbons.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of hydrogen; arenes: addition reactions", seconds=45),
]

# ================================================================ Organic Compounds Containing Halogens (2197-2206)
# 2197: geminal dihalides (both X on one carbon) in the list
dihal = {"CH3CHCl2": "gem", "ClCH2CH2Cl": "vic", "CH3CBr2CH3": "gem", "CH3CHBrCH2Br": "vic",
         "ClCH2CH2CH2Cl": "neither"}
v_2197 = str(sum(1 for t in dihal.values() if t == "gem"))
assert v_2197 == "2"
# 2200: 1.09 g C2H5Br -> Br- -> AgBr with 0.1 M AgNO3
n_2200 = F(109, 100) / mm(C=2, H=5, Br=1)
v_2200 = f"{float(n_2200 / F(1, 10) * 1000):.0f} mL"
assert n_2200 == F(1, 100) and v_2200 == "100 mL"
# 2206: C4H9Cl isomers, enantiomers counted separately
c4h9cl = {"1-chlorobutane": 1, "2-chlorobutane": 2, "1-chloro-2-methylpropane": 1, "2-chloro-2-methylpropane": 1}
v_2206 = str(sum(c4h9cl.values()))
assert v_2206 == "5" and len(c4h9cl) == 4

QUESTIONS += [
    N(T_HX, "C-X bond and preparation", "Basic",
      "Dihalogen derivatives with both halogen atoms on the same carbon are called geminal (gem) dihalides. How many of "
      "the following are gem-dihalides?\nCH₃CHCl₂, ClCH₂–CH₂Cl, CH₃CBr₂CH₃, CH₃CHBr–CH₂Br, ClCH₂–CH₂–CH₂Cl",
      ["1", v_2197, "3", "4"], "B", v_2197,
      "Classification of dihalogen compounds",
      "Gem-dihalides (alkylidene halides) have both halogens on one carbon; vicinal dihalides (alkylene dihalides) have "
      "them on adjacent carbons.",
      ["CH₃CHCl₂ (ethylidene chloride): gem", "ClCH₂CH₂Cl (ethylene dichloride): vic", "CH₃CBr₂CH₃: gem",
       "CH₃CHBrCH₂Br: vic", "ClCH₂CH₂CH₂Cl: halogens on C-1 and C-3, neither", "Count = 2"],
      why_others_wrong="Counting the vicinal compounds or the 1,3-dichloride as gem-dihalides gives 3 or 4.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification", seconds=30),

    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "Which of the following has the highest boiling point?",
      ["CH₃CH₂Cl", "CH₃CH₂F", "CH₃CH₂I", "CH₃CH₂Br"], "C",
      "Boiling points of haloalkanes",
      "For the same alkyl group, the boiling point rises with the size and mass of the halogen, because larger, more "
      "polarisable halogen atoms give stronger van der Waals forces: RI > RBr > RCl > RF.",
      ["Same alkyl group, different halogen", "Molar mass and van der Waals forces: I > Br > Cl > F",
       "Highest boiling point: CH₃CH₂I"],
      why_others_wrong="The C–F bond is the most polar, but polarity is not the deciding factor here; the heavier "
                       "halides have the stronger intermolecular forces.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties: boiling points", seconds=25),

    Q(T_HX, "Polyhalogen compounds", "Basic", "match_list",
      *ml("Match the polyhalogen compound in List-I with its use in List-II.",
          ["Dichloromethane", "Iodoform", "Freons", "DDT"],
          ["Refrigeration and air conditioning", "Paint remover", "Insecticide",
           "Antiseptic (formerly), acting through the free iodine it liberates"],
          "II IV I III", ["IV II I III", "II I IV III", "II IV III I"], "B"),
      "Uses of polyhalogen compounds",
      "Dichloromethane is a solvent used as a paint remover and in drug manufacture. Iodoform was used as an "
      "antiseptic because it liberates free iodine. Freons (chlorofluorocarbons) are used in refrigeration, air "
      "conditioning and as aerosol propellants. DDT was the first chlorinated organic insecticide.",
      ["Dichloromethane: paint remover (II)", "Iodoform: antiseptic (IV)", "Freons: refrigeration (I)",
       "DDT: insecticide (III)"],
      why_others_wrong="Swapping dichloromethane and iodoform, or freons and DDT, mismatches a solvent with an "
                       "antiseptic or a refrigerant with an insecticide.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=35),

    N(T_HX, "SN1 and SN2", "Intermediate",
      "1.09 g of bromoethane is boiled with excess aqueous NaOH until it is completely hydrolysed. The solution is "
      "acidified with dilute nitric acid and then titrated with 0.10 M AgNO₃. The volume of AgNO₃ solution needed to "
      "precipitate all the bromide is (C = 12, H = 1, Br = 80):",
      [v_2200, "50 mL", "200 mL", "10 mL"], "A", v_2200,
      "Nucleophilic substitution releases the halide ion",
      "The C–Br bond is covalent, so bromoethane itself gives no precipitate with AgNO₃. Hydrolysis "
      "(C₂H₅Br + OH⁻ → C₂H₅OH + Br⁻) frees bromide ions; nitric acid removes the excess OH⁻, which would otherwise "
      "precipitate silver oxide.",
      ["Molar mass of C₂H₅Br = 109 g mol⁻¹; n = 1.09/109 = 0.010 mol", "n(Br⁻) = 0.010 mol = n(Ag⁺) needed",
       "V = 0.010/0.10 = 0.10 L = 100 mL"],
      why_others_wrong="50 mL and 200 mL use a 1 : 2 or 2 : 1 ratio; 10 mL is a tenfold slip in the conversion to mL.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions", seconds=60),

    Q(T_HX, "SN1 and SN2", "Intermediate", "assertion_reason",
      *ar("Allylic and benzylic halides show high reactivity towards the SN1 reaction.", True,
          "The allylic or benzylic carbocation formed in the slow step is stabilised by resonance.", True,
          explains=True),
      "Reactivity of allylic and benzylic halides in SN1",
      "The rate of an SN1 reaction depends on how easily the carbocation forms. In CH₂=CH–CH₂⁺ and C₆H₅–CH₂⁺ the "
      "positive charge is delocalised over the double bond or the benzene ring, so these carbocations form readily. "
      "R explains A.",
      ["SN1: rate-determining ionisation to a carbocation", "Allyl and benzyl cations: resonance stabilised",
       "→ faster SN1"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the physical properties of haloalkanes are correct?",
          [("Bromo, iodo and polychloro derivatives of hydrocarbons are heavier than water.", True),
           ("The density of haloalkanes increases with the number of carbon atoms, the number of halogen atoms and "
            "the atomic mass of the halogen.", True),
           ("Methyl bromide is a liquid at room temperature.", False),
           ("Haloalkanes dissolve in organic solvents.", True),
           ("Among isomeric haloalkanes, the boiling point increases with branching.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d", "e"]], "C"),
      "Density, state and solubility of haloalkanes",
      "NCERT notes that bromo, iodo and polychloro compounds are denser than water and that density rises with more "
      "carbon atoms, more halogen atoms and heavier halogens. Methyl chloride, methyl bromide, ethyl chloride and some "
      "chlorofluoromethanes are gases at room temperature. Haloalkanes dissolve in organic solvents. Branching lowers "
      "the surface area and hence the boiling point.",
      ["(a) true", "(b) true", "(c) false: CH₃Br is a gas", "(d) true", "(e) false: branching lowers the boiling point"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties", seconds=50),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "statement_pair",
      *sp("In the preparation of iodoarenes by electrophilic substitution, an oxidising agent such as HNO₃ or HIO₄ is "
          "needed, because the reaction is reversible and the HI formed must be oxidised.", True,
          "Fluoroarenes are not prepared by direct electrophilic fluorination, because fluorine is far too reactive.",
          True),
      "Preparation of haloarenes by electrophilic substitution",
      "Chlorination and bromination of arenes with a Lewis acid catalyst work well. Iodination is reversible, so HI is "
      "removed by oxidation. Fluorine reacts too violently for controlled substitution.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloarenes from hydrocarbons", seconds=35),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "Bromoethane is heated with silver nitrite to give X as the main product. X is reduced with tin and hydrochloric "
      "acid to give Y. Y is:",
      ["Ethanol", "Ethanenitrile", "Ethyl nitrite", "Ethanamine"], "D",
      "Ambident nucleophiles and reduction of nitro compounds",
      "Silver nitrite is covalent, so the nitrite ion attacks through nitrogen and gives the nitroalkane (KNO₂, which "
      "is ionic, gives the alkyl nitrite through oxygen). A nitro group is reduced to –NH₂ by a metal and acid.",
      ["C₂H₅Br + AgNO₂ → C₂H₅–NO₂ (nitroethane) + AgBr", "C₂H₅NO₂ + 6[H] (Sn/HCl) → C₂H₅NH₂ + 2H₂O",
       "Y = ethanamine"],
      why_others_wrong="Ethyl nitrite would be the product with KNO₂ and gives no amine on reduction; ethanol and "
                       "ethanenitrile need OH⁻ and CN⁻ respectively.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution; 'Amines', reduction of nitro "
            f"compounds", seconds=50),

    Q(T_HX, "SN1 and SN2", "Advanced", "match_list",
      *ml("Nitro groups ortho and para to the halogen make aryl halides much more reactive towards nucleophiles. Match "
          "the aryl chloride in List-I with the condition needed to convert it into the corresponding phenol (List-II).",
          ["Chlorobenzene", "1-Chloro-4-nitrobenzene", "1-Chloro-2,4-dinitrobenzene", "2,4,6-Trinitrochlorobenzene"],
          ["Warm water, 323 K", "Aqueous NaOH, 443 K, then H⁺", "Aqueous NaOH, 623 K and 300 atm, then H⁺",
           "Aqueous NaOH, 368 K, then H⁺"],
          "III II IV I", ["III IV II I", "I II IV III", "III II I IV"], "C"),
      "Effect of electron-withdrawing groups on haloarenes",
      "An –NO₂ group at the ortho or para position withdraws electron density from the ring and stabilises the "
      "negatively charged intermediate (the charge can reach the nitro group by resonance). The more such groups, the "
      "milder the conditions.",
      ["No NO₂: 623 K, 300 atm (III)", "One p-NO₂: 443 K (II)", "Two (o, p): 368 K (IV)", "Three (o, o, p): warm "
       "water, 323 K (I)"],
      why_others_wrong="Any code that gives a more nitrated compound a harsher condition than a less nitrated one "
                       "reverses the activating effect of the nitro groups.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes: effect of substituents", seconds=50),

    N(T_HX, "SN1 and SN2", "Advanced",
      "Counting the two enantiomers of a chiral compound separately, how many isomers have the molecular formula "
      "C₄H₉Cl?",
      ["4", v_2206, "6", "7"], "B", v_2206,
      "Structural isomers and enantiomers of chlorobutanes",
      "First list the structural isomers, then look for a carbon bonded to four different groups.",
      ["1-Chlorobutane: achiral", "2-Chlorobutane: C-2 has H, Cl, CH₃, C₂H₅ → chiral, two enantiomers",
       "1-Chloro-2-methylpropane: achiral", "2-Chloro-2-methylpropane: achiral", "Total = 1 + 2 + 1 + 1 = 5"],
      why_others_wrong="4 counts structures only; 6 or 7 wrongly treat 1-chloro-2-methylpropane (C-2 has two CH₃) or "
                       "2-chloro-2-methylpropane as chiral.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', optical isomerism", seconds=60),
]

# ================================================================ Organic Compounds Containing Oxygen (2207-2223)
# 2208: 2CH3COCl + (CH3)2Cd -> 2CH3COCH3 + CdCl2
n_2208 = F(157, 10) / mm(C=2, H=3, O=1, Cl=1)
v_2208 = g(n_2208 * mm(C=3, H=6, O=1))
assert n_2208 == F(1, 5) and v_2208 == "11.6 g"
# 2213: CH3COONH4 -> (heat) CH3CONH2 + H2O
n_2213 = F(77, 10) / mm(C=2, H=7, O=2, N=1)
v_2213 = g(n_2213 * mm(C=2, H=5, O=1, N=1))
assert n_2213 == F(1, 10) and v_2213 == "5.9 g"
# 2214: alcohols oxidised to ketones (secondary alcohols)
kind = {"propan-2-ol": 2, "butan-2-ol": 2, "cyclohexanol": 2, "2-methylpropan-2-ol": 3, "propan-1-ol": 1,
        "pentan-3-ol": 2, "benzyl alcohol": 1}
v_2214 = str(sum(1 for c in kind.values() if c == 2))
assert v_2214 == "4"
# 2219: C5H12O alcohols by class
c5_alcohols = {"pentan-1-ol": 1, "2-methylbutan-1-ol": 1, "3-methylbutan-1-ol": 1, "2,2-dimethylpropan-1-ol": 1,
               "pentan-2-ol": 2, "pentan-3-ol": 2, "3-methylbutan-2-ol": 2, "2-methylbutan-2-ol": 3}
assert len(c5_alcohols) == 8
v_2219 = str(sum(1 for c in c5_alcohols.values() if c == 1))
assert v_2219 == "4"

QUESTIONS += [
    Q(T_OX, "Aldehydes and ketones", "Basic", "direct",
      "Formalin, a 40% aqueous solution of methanal, is mainly used:",
      ["as a food preservative", "as a solvent for paints", "as a fuel in spirit lamps",
       "to preserve biological specimens"], "D",
      "Uses of methanal",
      "NCERT lists formalin (about 40% methanal in water) as the liquid used to preserve biological specimens.",
      ["Formalin = 40% HCHO(aq)", "Use: preserving biological specimens"],
      why_others_wrong="Sodium benzoate, not formalin, is the common food preservative; formalin is neither a paint "
                       "solvent nor a lamp fuel.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', uses of aldehydes and ketones", seconds=20),

    N(T_OX, "Aldehydes and ketones", "Basic",
      "Ketones are prepared by treating acyl chlorides with dialkylcadmium: 2CH₃COCl + (CH₃)₂Cd → 2CH₃COCH₃ + CdCl₂. "
      "The mass of propanone obtained from 15.7 g of ethanoyl chloride, assuming complete conversion, is "
      "(C = 12, H = 1, O = 16, Cl = 35.5):",
      ["5.8 g", v_2208, "23.2 g", "15.7 g"], "B", v_2208,
      "Preparation of ketones from acyl chlorides",
      "Each molecule of acyl chloride gives one molecule of ketone; the dialkylcadmium supplies one alkyl group to each.",
      ["Molar mass of CH₃COCl = 78.5 g mol⁻¹; n = 15.7/78.5 = 0.20 mol", "n(CH₃COCH₃) = 0.20 mol",
       "Mass = 0.20 × 58 = 11.6 g"],
      why_others_wrong="5.8 g takes the 2 : 1 ratio the wrong way; 23.2 g doubles the moles; 15.7 g assumes equal "
                       "masses.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of ketones from acyl chlorides",
      seconds=40),

    Q(T_OX, "Carboxylic acids", "Basic", "match_list",
      *ml("Match the substance in List-I with its use in List-II.",
          ["Methanoic acid", "Ethanoic acid", "Sodium benzoate", "Sodium or potassium salts of higher fatty acids"],
          ["Soaps and detergents", "Rubber, textile, dyeing, leather and electroplating industries",
           "Food preservative", "Solvent, and as vinegar in the food industry"],
          "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "D"),
      "Uses of carboxylic acids and their salts",
      "These are the uses NCERT gives: methanoic acid in rubber, textile, dyeing, leather and electroplating; "
      "ethanoic acid as a solvent and as vinegar; sodium benzoate as a food preservative; and salts of higher fatty "
      "acids as soaps.",
      ["Methanoic acid: II", "Ethanoic acid: IV", "Sodium benzoate: III", "Salts of fatty acids: I"],
      why_others_wrong="Swapping methanoic and ethanoic acids, or the preservative and soaps, mismatches the uses.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', uses of carboxylic acids", seconds=35),

    Q(T_OX, "Ethers", "Basic", "statement_pair",
      *sp("The miscibility of ethers with water resembles that of alcohols of the same molecular mass.", True,
          "Ether molecules are associated through intermolecular hydrogen bonds, as alcohol molecules are.", False),
      "Solubility and boiling points of ethers",
      "Ethers can accept hydrogen bonds from water through the lone pairs on oxygen, so ethoxyethane and butan-1-ol "
      "are miscible with water to almost the same extent. But ethers have no O–H group, so their molecules cannot "
      "hydrogen bond with one another; this is why their boiling points are much lower than those of isomeric "
      "alcohols.",
      ["Statement I: true (ethoxyethane ≈ butan-1-ol in miscibility)", "Statement II: false; no O–H in ethers"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties of ethers", seconds=30),

    Q(T_OX, "Phenols", "Basic", "assertion_reason",
      *ar("Phenol dissolves in aqueous sodium hydroxide.", True,
          "Phenol reacts with bromine water to give a white precipitate.", True),
      "Acidic character of phenol",
      "Phenol is acidic enough to react with NaOH and form the soluble salt sodium phenoxide. R is a true reaction of "
      "phenol (bromination of the activated ring to 2,4,6-tribromophenol), but it is about ring substitution, not "
      "acidity, so it does not explain A.",
      ["C₆H₅OH + NaOH → C₆H₅O⁻Na⁺ + H₂O (soluble)", "R: electrophilic substitution, unrelated to A"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols; electrophilic substitution", seconds=30),

    Q(T_OX, "Alcohols", "Intermediate", "match_list",
      *ml("Match the conversion in List-I with the conditions used for it in List-II.",
          ["Ethanol → ethene", "A secondary alcohol → alkene", "A tertiary alcohol → alkene",
           "Ethanol (in excess) → ethoxyethane"],
          ["20% H₃PO₄, 358 K", "Concentrated H₂SO₄, 443 K", "Concentrated H₂SO₄, 413 K", "85% H₃PO₄, 440 K"],
          "II IV I III", ["IV II I III", "II I IV III", "III IV I II"], "B"),
      "Ease of dehydration of alcohols",
      "The ease of dehydration is tertiary > secondary > primary, so the conditions needed become milder from primary "
      "to tertiary. With ethanol in excess and a lower temperature (413 K), intermolecular dehydration gives the ether.",
      ["Primary (ethanol): conc. H₂SO₄, 443 K (II)", "Secondary: 85% H₃PO₄, 440 K (IV)",
       "Tertiary: 20% H₃PO₄, 358 K (I)", "Ether from ethanol: conc. H₂SO₄, 413 K (III)"],
      why_others_wrong="Codes that give the tertiary alcohol the harshest conditions reverse the order of ease of "
                       "dehydration; 443 K versus 413 K decides alkene versus ether for ethanol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of alcohols: dehydration", seconds=45),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "Ethanoic acid reacts with ammonia to give ammonium ethanoate, which on strong heating loses water to give "
      "ethanamide. The mass of ethanamide obtained from 7.7 g of ammonium ethanoate, assuming complete conversion, is "
      "(C = 12, H = 1, N = 14, O = 16):",
      ["7.7 g", "6.0 g", "4.5 g", v_2213], "D", v_2213,
      "Formation of amides from carboxylic acids",
      "CH₃COOH + NH₃ ⇌ CH₃COONH₄; on heating, CH₃COONH₄ → CH₃CONH₂ + H₂O. One mole of salt gives one mole of amide.",
      ["Molar mass of CH₃COONH₄ = 77 g mol⁻¹; n = 7.7/77 = 0.10 mol", "Molar mass of CH₃CONH₂ = 59 g mol⁻¹",
       "Mass = 0.10 × 59 = 5.9 g"],
      why_others_wrong="7.7 g ignores the loss of water; 6.0 g is the mass of ethanoic acid; 4.5 g subtracts the "
                       "ammonia instead of water.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions of carboxylic acids: with ammonia",
      seconds=45),

    N(T_OX, "Alcohols", "Intermediate",
      "How many of the following alcohols give a ketone on oxidation with acidified potassium dichromate?\n"
      "Propan-2-ol, butan-2-ol, cyclohexanol, 2-methylpropan-2-ol, propan-1-ol, pentan-3-ol, benzyl alcohol",
      ["2", "3", v_2214, "5"], "C", v_2214,
      "Oxidation of primary, secondary and tertiary alcohols",
      "Secondary alcohols are oxidised to ketones. Primary alcohols give aldehydes and then carboxylic acids; tertiary "
      "alcohols resist oxidation under these conditions.",
      ["Secondary: propan-2-ol, butan-2-ol, cyclohexanol, pentan-3-ol → ketones",
       "Primary: propan-1-ol, benzyl alcohol → aldehyde/acid", "Tertiary: 2-methylpropan-2-ol → no ketone",
       "Count = 4"],
      why_others_wrong="3 usually misses cyclohexanol (a secondary ring alcohol); 5 counts benzyl alcohol or the "
                       "tertiary alcohol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', oxidation of alcohols", seconds=45),

    Q(T_OX, "Phenols", "Intermediate", "assertion_reason",
      *ar("o-Nitrophenol and p-nitrophenol can be separated by steam distillation, o-nitrophenol passing over with the "
          "steam.", True,
          "o-Nitrophenol has intramolecular hydrogen bonding, whereas p-nitrophenol molecules are associated through "
          "intermolecular hydrogen bonds.", True, explains=True),
      "Hydrogen bonding and volatility of nitrophenols",
      "Nitration of phenol with dilute nitric acid gives a mixture of o- and p-nitrophenols. In the ortho isomer the "
      "–OH and –NO₂ groups are hydrogen bonded within the molecule, so it is not associated and is steam volatile. "
      "The para isomer is held together by intermolecular hydrogen bonds and is much less volatile. R explains A.",
      ["o-Nitrophenol: intramolecular H-bond → volatile in steam", "p-Nitrophenol: intermolecular H-bonds → not",
       "Steam distillation separates them"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', electrophilic substitution in phenols: nitration", seconds=40),

    Q(T_OX, "Carboxylic acids", "Intermediate", "assertion_reason",
      *ar("Carboxylic acids do not give the characteristic nucleophilic addition reactions of aldehydes and ketones, "
          "although they contain a C=O group.", True,
          "The carbonyl carbon of a carboxylic acid is sp³ hybridised.", False),
      "Structure of the carboxyl group",
      "The carboxyl carbon is sp² hybridised and lies in a planar group, just as in aldehydes and ketones. It is less "
      "electrophilic because the lone pair on the –OH oxygen is delocalised onto the C=O group by resonance, so "
      "carboxylic acids do not show typical carbonyl reactions. A is true; R is false.",
      ["Carboxyl carbon: three σ bonds + one π bond → sp²", "Resonance lowers the electrophilic character",
       "A true, R false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', structure of the carboxyl group", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "direct",
      "Propanal is treated with dilute NaOH and the aldol formed is heated. The final product is:",
      ["Hex-2-enal", "3-Hydroxyhexanal", "2-Methylpent-3-enal", "2-Methylpent-2-enal"], "D",
      "Aldol condensation",
      "The α-carbon of one propanal molecule (C-2) adds to the carbonyl carbon of another, giving "
      "3-hydroxy-2-methylpentanal. On heating, water is lost between the α and β carbons to give the α,β-unsaturated "
      "aldehyde.",
      ["2CH₃CH₂CHO → CH₃CH₂CH(OH)–CH(CH₃)–CHO (aldol)", "−H₂O → CH₃CH₂CH=C(CH₃)–CHO",
       "Name: 2-methylpent-2-enal"],
      why_others_wrong="Hex-2-enal and 3-hydroxyhexanal would need the bond to form at the terminal CH₃, which is not "
                       "the α-carbon; in 2-methylpent-3-enal the double bond is not conjugated with C=O.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol condensation", seconds=50),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Aldehydes react with one equivalent of a monohydric alcohol in the presence of dry HCl to give a hemiacetal, "
          "which reacts with a second molecule of alcohol to give an acetal.", True,
          "Acetals and ketals are hydrolysed by aqueous mineral acids back to the corresponding aldehydes and "
          "ketones.", True),
      "Hemiacetals, acetals and ketals",
      "Dry HCl protonates the carbonyl oxygen and makes the carbonyl carbon more electrophilic, so the weak "
      "nucleophile ROH can add (hemiacetal); a second ROH replaces the –OH (acetal, a gem-dialkoxy compound). With "
      "aqueous acid the reaction runs backwards and the carbonyl compound is regenerated.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', addition of alcohols", seconds=35),

    N(T_OX, "Alcohols", "Advanced",
      "How many of the structural isomers with the molecular formula C₅H₁₂O are primary alcohols (and so can be "
      "oxidised to aldehydes)?",
      ["3", v_2219, "5", "8"], "B", v_2219,
      "Classifying the isomeric pentanols",
      "There are eight alcohols C₅H₁₁OH. An alcohol is primary when the –OH carbon is attached to only one other "
      "carbon (–CH₂OH).",
      ["Primary: pentan-1-ol, 2-methylbutan-1-ol, 3-methylbutan-1-ol, 2,2-dimethylpropan-1-ol (4)",
       "Secondary: pentan-2-ol, pentan-3-ol, 3-methylbutan-2-ol (3)", "Tertiary: 2-methylbutan-2-ol (1)"],
      why_others_wrong="3 misses 2,2-dimethylpropan-1-ol (neopentyl alcohol), which is primary although its "
                       "neighbouring carbon is quaternary; 5 adds a secondary alcohol; 8 counts all alcohols.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', classification and oxidation of alcohols", seconds=75),

    Q(T_OX, "Ethers", "Advanced", "assertion_reason",
      *ar("When (CH₃)₃C–Br is heated with sodium methoxide, the main product is 2-methylpropene and not "
          "tert-butyl methyl ether.", True,
          "Alkoxides are strong bases as well as nucleophiles, and with a tertiary alkyl halide elimination competes "
          "over substitution.", True, explains=True),
      "Limitation of Williamson synthesis",
      "Williamson synthesis works best with primary alkyl halides. A tertiary halide is crowded, so the alkoxide removes "
      "a β-hydrogen instead of attacking carbon, and an alkene is formed. tert-Butyl methyl ether is therefore made from "
      "sodium tert-butoxide and bromomethane. R explains A.",
      ["(CH₃)₃C–Br + CH₃O⁻ → CH₂=C(CH₃)₂ + CH₃OH + Br⁻", "Better route: (CH₃)₃C–O⁻Na⁺ + CH₃Br → (CH₃)₃C–O–CH₃"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of ethers: Williamson synthesis", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "match_list",
      *ml("Match each pair of compounds in List-I with the test in List-II that distinguishes them. Use each test once.",
          ["Ethanal and propanone", "Ethanol and methanol", "Phenol and ethanol", "Ethanoic acid and phenol"],
          ["Effervescence with aqueous NaHCO₃", "Tollens' reagent", "Iodoform test (I₂ and NaOH)",
           "White precipitate with bromine water"],
          "II III IV I", ["III II IV I", "II III I IV", "II IV III I"], "D"),
      "Chemical tests for oxygen compounds",
      "Tollens' reagent is reduced by ethanal but not by propanone (both give iodoform, so that test fails here). "
      "Ethanol gives iodoform and methanol does not. Phenol gives a white precipitate of 2,4,6-tribromophenol with "
      "bromine water; ethanol does not. Ethanoic acid is strong enough to liberate CO₂ from NaHCO₃; phenol is not. "
      "Once ethanol/methanol has taken the iodoform test, phenol/ethanol must take bromine water and the acid/phenol "
      "pair NaHCO₃.",
      ["Ethanal/propanone: Tollens' (II)", "Ethanol/methanol: iodoform (III)", "Phenol/ethanol: bromine water (IV)",
       "Ethanoic acid/phenol: NaHCO₃ (I)"],
      why_others_wrong="Iodoform cannot distinguish ethanal from propanone; NaHCO₃ cannot distinguish phenol from "
                       "ethanol, as neither reacts.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids' and 'Alcohols, Phenols and Ethers', chemical tests",
      seconds=80),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following compounds give BOTH a positive iodoform test and an orange-yellow precipitate with "
          "2,4-dinitrophenylhydrazine?",
          [("Ethanal", True), ("Propanal", False), ("Butan-2-one", True), ("Ethanol", False),
           ("Acetophenone (C₆H₅COCH₃)", True)],
          [["a", "b", "c"], ["a", "d", "e"], ["c", "d", "e"]], "B"),
      "Combining the iodoform and 2,4-DNP tests",
      "2,4-DNP reacts with the C=O group of aldehydes and ketones. The iodoform test needs a CH₃CO– group (or a "
      "CH₃CH(OH)– group, which is first oxidised to it).",
      ["(a) ethanal: CH₃CHO, C=O and CH₃CO– → both", "(b) propanal: no CH₃CO– → no iodoform",
       "(c) butan-2-one: CH₃COC₂H₅ → both", "(d) ethanol: iodoform yes, but no C=O → no 2,4-DNP",
       "(e) acetophenone: C₆H₅COCH₃ → both"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', haloform reaction; reactions with ammonia "
            f"derivatives", seconds=60),

    Q(T_OX, "Carboxylic acids", "Advanced", "multi_statement",
      *ms("Which of the following statements about reactions of carboxylic acids are correct?",
          [("With PCl₅, a carboxylic acid gives the acyl chloride, POCl₃ and HCl.", True),
           ("Thionyl chloride is preferred for making acyl chlorides, because the other two products are gases that "
            "escape.", True),
           ("With PCl₃, a carboxylic acid gives the acyl chloride and H₃PO₃.", True),
           ("Carboxylic acids are reduced to primary alcohols by sodium borohydride.", False),
           ("On heating with P₂O₅, a carboxylic acid gives the acid anhydride.", True)],
          [["a", "b", "d"], ["b", "c", "d", "e"], ["a", "c", "d", "e"]], "D"),
      "Reactions of the –OH part of the carboxyl group",
      "The –OH of a carboxylic acid is replaced by Cl with PCl₅, PCl₃ or SOCl₂ (SO₂ and HCl escape, leaving a pure "
      "product). Strong dehydrating agents such as P₂O₅ give anhydrides. Carboxylic acids are reduced by LiAlH₄ or "
      "diborane; NaBH₄ does not reduce the carboxyl group.",
      ["(a) RCOOH + PCl₅ → RCOCl + POCl₃ + HCl: true", "(b) RCOOH + SOCl₂ → RCOCl + SO₂ + HCl: true",
       "(c) 3RCOOH + PCl₃ → 3RCOCl + H₃PO₃: true", "(d) false: NaBH₄ does not reduce –COOH",
       "(e) true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions of carboxylic acids",
      seconds=55),
]

# ================================================================ Organic Compounds Containing Nitrogen (2224-2233)
# 2225: primary amines (one carbon on N)
amine_class = {"(CH3)3CNH2": 1, "CH3NHCH3": 2, "C6H5NH2": 1, "C6H5CH2NH2": 1, "(C2H5)3N": 3, "CH3CH2NH2": 1}
v_2225 = str(sum(1 for c in amine_class.values() if c == 1))
assert v_2225 == "4"
# 2227: Gabriel synthesis gives only primary amines from alkyl (not aryl) halides
gabriel = {"ethanamine": True, "propan-1-amine": True, "benzylamine": True, "aniline": False,
           "N-methylethanamine": False, "triethylamine": False}
v_2227 = str(sum(gabriel.values()))
assert v_2227 == "3"

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "The IUPAC name of benzylamine, C₆H₅–CH₂–NH₂, is:",
      ["Benzenamine", "N-Phenylmethanamine", "Phenylmethanamine", "2-Phenylethanamine"], "C",
      "Naming amines",
      "The –NH₂ group is on the CH₂ carbon, so the parent is methanamine and the phenyl group is a substituent on that "
      "carbon: phenylmethanamine. Benzenamine is aniline, where –NH₂ is on the ring.",
      ["Parent chain: CH₂–NH₂ → methanamine", "Substituent on carbon: phenyl", "Name: phenylmethanamine"],
      why_others_wrong="Benzenamine is C₆H₅NH₂; 'N-phenyl' would put the phenyl group on nitrogen (C₆H₅NHCH₃); "
                       "2-phenylethanamine has two CH₂ groups.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=25),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "How many of the following are primary amines?\n"
      "(CH₃)₃C–NH₂, CH₃–NH–CH₃, C₆H₅NH₂, C₆H₅CH₂NH₂, (C₂H₅)₃N, CH₃CH₂NH₂",
      ["3", v_2225, "5", "6"], "B", v_2225,
      "Classification of amines",
      "An amine is primary, secondary or tertiary according to the number of hydrogen atoms of ammonia replaced by "
      "alkyl or aryl groups (one, two or three), not according to the kind of carbon atom attached to nitrogen.",
      ["Primary (–NH₂): (CH₃)₃CNH₂, C₆H₅NH₂, C₆H₅CH₂NH₂, CH₃CH₂NH₂", "Secondary: CH₃NHCH₃",
       "Tertiary: (C₂H₅)₃N", "Count = 4"],
      why_others_wrong="3 usually treats (CH₃)₃CNH₂ as tertiary because its carbon is tertiary; 5 or 6 count the "
                       "secondary or tertiary amine.",
      ncert=f"{NC12}, 'Amines', structure and classification", seconds=30),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("The lower aliphatic amines are gases with a fishy odour, and primary amines with three or more carbon atoms "
          "are liquids.", True,
          "The higher amines are highly soluble in water.", False),
      "Physical properties of amines",
      "NCERT describes the lower aliphatic amines as gases with a fishy smell; primary amines with three or more carbon "
      "atoms are liquids and still higher ones solids. Solubility in water falls as the hydrophobic alkyl part grows, "
      "so the higher amines are essentially insoluble.",
      ["Statement I: true", "Statement II: false; solubility decreases with increasing molar mass"],
      ncert=f"{NC12}, 'Amines', physical properties", seconds=25),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "How many of the following amines can be prepared by Gabriel phthalimide synthesis?\n"
      "Ethanamine, propan-1-amine, benzylamine, aniline, N-methylethanamine, triethylamine",
      ["2", v_2227, "4", "5"], "B", v_2227,
      "Scope of Gabriel phthalimide synthesis",
      "Potassium phthalimide is alkylated by an alkyl halide and the product is hydrolysed, so only primary amines are "
      "obtained. Aromatic primary amines cannot be made this way because aryl halides do not undergo nucleophilic "
      "substitution with the phthalimide anion. Benzyl chloride is an alkyl-type halide and reacts normally.",
      ["Yes: ethanamine, propan-1-amine, benzylamine (primary, from alkyl or benzyl halides)",
       "No: aniline (aryl halide unreactive), N-methylethanamine (2°), triethylamine (3°)", "Count = 3"],
      why_others_wrong="2 wrongly excludes benzylamine; 4 or 5 include aniline or a secondary/tertiary amine.",
      ncert=f"{NC12}, 'Amines', preparation: Gabriel phthalimide synthesis", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Aniline does not undergo the Friedel–Crafts reaction.", True,
          "Aniline forms a salt with the Lewis acid AlCl₃; the nitrogen then carries a positive charge and acts as a "
          "strongly deactivating group.", True, explains=True),
      "Why aniline fails in Friedel–Crafts reactions",
      "The basic –NH₂ group donates its lone pair to AlCl₃. The resulting positively charged nitrogen withdraws "
      "electrons from the ring, so the ring is deactivated and no alkylation or acylation occurs. R explains A.",
      ["C₆H₅NH₂ + AlCl₃ → C₆H₅NH₂⁺–AlCl₃⁻", "Positive N deactivates the ring", "→ no Friedel–Crafts reaction"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution in aromatic amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "direct",
      "In the gaseous phase, where solvation is absent, the basic strength of the methyl-substituted amines and ammonia "
      "follows the order:",
      ["(CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃", "NH₃ > CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N", "CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N > NH₃",
       "(CH₃)₃N > (CH₃)₂NH > CH₃NH₂ > NH₃"], "D",
      "Basicity of amines in the gas phase",
      "In the gas phase only the +I effect of the alkyl groups matters: each methyl group pushes electron density onto "
      "nitrogen, so tertiary > secondary > primary > NH₃. In water, solvation of the ammonium ions and steric "
      "factors change the order to (CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃.",
      ["Gas phase: +I effect only", "More alkyl groups → more basic", "3° > 2° > 1° > NH₃"],
      why_others_wrong="(CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃ is the order in aqueous solution; the other two orders ignore "
                       "the +I effect.",
      ncert=f"{NC12}, 'Amines', basic character of amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the test in List-I with the observation in List-II.",
          ["A primary amine warmed with chloroform and ethanolic KOH",
           "Aniline treated with NaNO₂ and HCl at 273–278 K, then with phenol in mildly alkaline solution",
           "N-Methylethanamine shaken with benzenesulphonyl chloride",
           "Aniline treated with bromine water at room temperature"],
          ["White precipitate", "Foul-smelling product", "Orange dye", "Product insoluble in aqueous alkali"],
          "II III IV I", ["II I IV III", "III II IV I", "II III I IV"], "A"),
      "Tests for amines",
      "Primary amines give foul-smelling isocyanides (carbylamine test). Aniline is diazotised and the diazonium salt "
      "couples with phenol to give orange p-hydroxyazobenzene. A secondary amine gives an N,N-dialkylsulphonamide, "
      "which has no acidic H on nitrogen and is insoluble in alkali. Aniline and bromine water give a white precipitate "
      "of 2,4,6-tribromoaniline.",
      ["Carbylamine: foul smell (II)", "Diazotisation + coupling: orange dye (III)",
       "Hinsberg with 2° amine: alkali-insoluble product (IV)", "Bromine water: white precipitate (I)"],
      why_others_wrong="Codes that give the secondary amine a white precipitate or the coupling reaction a foul smell "
                       "mix up the tests.",
      ncert=f"{NC12}, 'Amines', chemical reactions and tests", seconds=45),

    Q(T_NI, "Diazonium salts", "Advanced", "multi_statement",
      *ms("1,3,5-Tribromobenzene cannot be made by direct bromination of benzene, but it can be made from aniline. "
          "Which of the following statements about this conversion are correct?",
          [("Aniline reacts with bromine water at room temperature to give 2,4,6-tribromoaniline.", True),
           ("2,4,6-Tribromoaniline is diazotised with NaNO₂ and HCl at 273–278 K.", True),
           ("The diazonium group is then replaced by hydrogen using hypophosphorous acid (H₃PO₂).", True),
           ("Direct bromination of benzene with excess Br₂ and FeBr₃ gives 1,3,5-tribromobenzene, because bromine is "
            "a meta-directing group.", False),
           ("In bromine water, the –NH₂ group directs bromine mainly to the meta positions.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
      "Using the –NH₂ group as a temporary directing group",
      "Bromine on a benzene ring is ortho/para directing, so direct bromination cannot give the 1,3,5 pattern. The "
      "strongly activating, ortho/para-directing –NH₂ group places three Br atoms at 2, 4 and 6, which are mutually "
      "meta. The –NH₂ group is then removed: diazotisation followed by H₃PO₂ replaces –N₂⁺ by –H.",
      ["(a) true", "(b) true", "(c) true: ArN₂⁺ + H₃PO₂ + H₂O → ArH + N₂ + H₃PO₃ + H⁺",
       "(d) false: Br is ortho/para directing", "(e) false: –NH₂ is ortho/para directing"],
      ncert=f"{NC12}, 'Amines', diazonium salts: replacement by hydrogen; bromination of aniline", seconds=70),

    Q(T_NI, "Diazonium salts", "Advanced", "assertion_reason",
      *ar("Benzenediazonium chloride is prepared at 273–278 K and used immediately after preparation.", True,
          "Benzenediazonium chloride couples with phenol to give an orange azo dye.", True),
      "Stability and reactions of diazonium salts",
      "Arenediazonium salts are stable only for a short time and only at low temperature, so they are made in ice-cold "
      "solution and used at once. R states a true reaction of the salt (coupling), but coupling has nothing to do "
      "with why the salt must be kept cold and used immediately.",
      ["A: true (low stability)", "R: true (coupling reaction), not the reason for A"],
      ncert=f"{NC12}, 'Amines', diazonium salts: preparation and properties", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "Benzamide is reduced with lithium aluminium hydride to give X. X is treated with NaNO₂ and dilute HCl. The main "
      "organic product is:",
      ["Phenol", "Benzenediazonium chloride", "Aniline", "Benzyl alcohol"], "D",
      "Reduction of amides; nitrous acid and primary amines",
      "LiAlH₄ reduces the amide C=O to CH₂ without losing carbon, so benzamide gives benzylamine, C₆H₅CH₂NH₂, a "
      "primary amine with –NH₂ on an sp³ carbon. Like aliphatic primary amines, it reacts with nitrous acid with loss "
      "of N₂ to give the alcohol. (Hofmann degradation with Br₂/NaOH would instead give aniline, which forms a stable "
      "diazonium salt.)",
      ["C₆H₅CONH₂ + 4[H] (LiAlH₄) → C₆H₅CH₂NH₂ + H₂O", "C₆H₅CH₂NH₂ + HNO₂ → C₆H₅CH₂OH + N₂ + H₂O",
       "Product: benzyl alcohol"],
      why_others_wrong="Aniline, its diazonium salt and phenol all come from the Hofmann route, which removes the "
                       "carbonyl carbon; LiAlH₄ keeps it.",
      ncert=f"{NC12}, 'Amines', preparation by reduction of amides; reaction with nitrous acid", seconds=60),
]

# ================================================================ Biomolecules (Chemistry) (2234-2243)
# 2234: fat-soluble vitamins in the list
fat_soluble = {"A": True, "B1": False, "C": False, "D": True, "E": True, "K": True, "B12": False}
v_2234 = str(sum(fat_soluble.values()))
assert v_2234 == "4"
# 2237: moles of glucose from 1 mol each of maltose, sucrose, lactose
glucose_units = {"maltose": 2, "sucrose": 1, "lactose": 1}
v_2237 = str(sum(glucose_units.values()))
assert v_2237 == "4"

QUESTIONS += [
    N(T_BM, "Vitamins", "Basic",
      "How many of the following vitamins are fat soluble?\nA, B₁, C, D, E, K, B₁₂",
      ["3", v_2234, "5", "6"], "B", v_2234,
      "Fat-soluble and water-soluble vitamins",
      "Vitamins A, D, E and K are fat soluble and are stored in the liver and adipose tissue. The B group vitamins and "
      "vitamin C are water soluble.",
      ["Fat soluble: A, D, E, K", "Water soluble: B₁, B₁₂, C", "Count = 4"],
      why_others_wrong="3 leaves out one of A, D, E, K; 5 or 6 wrongly include vitamin B₁₂ or C.",
      ncert=f"{NC12}, 'Biomolecules', classification of vitamins", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "direct",
      "Increased blood clotting time is caused by a deficiency of:",
      ["Vitamin A", "Vitamin B₁", "Vitamin K", "Vitamin D"], "C",
      "Vitamin deficiency diseases",
      "NCERT's table of vitamins links vitamin K deficiency with an increased blood clotting time.",
      ["Vitamin K: needed for normal blood clotting", "Deficiency → increased clotting time"],
      why_others_wrong="Vitamin A deficiency causes xerophthalmia and night blindness, vitamin B₁ deficiency beri beri, "
                       "and vitamin D deficiency rickets and osteomalacia.",
      ncert=f"{NC12}, 'Biomolecules', vitamins: deficiency diseases", seconds=20),

    Q(T_BM, "Amino acids and proteins", "Basic", "statement_pair",
      *sp("In the α-helix, a polypeptide chain twists into a right-handed screw, with the –NH group of each amino acid "
          "residue hydrogen bonded to the >C=O of an adjacent turn.", True,
          "In the β-pleated sheet, the peptide chains are stretched out nearly to their maximum extension and laid side "
          "by side, held together by intermolecular hydrogen bonds.", True),
      "Secondary structure of proteins",
      "These are NCERT's descriptions of the two common secondary structures. In both, hydrogen bonds between the "
      "–NH and >C=O groups of peptide bonds hold the shape.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Biomolecules', structure of proteins: secondary structure", seconds=30),

    N(T_BM, "Carbohydrates", "Intermediate",
      "One mole each of maltose, sucrose and lactose is hydrolysed completely. The total number of moles of D-glucose "
      "formed is:",
      ["1", "2", "3", v_2237], "D", v_2237,
      "Composition of disaccharides",
      "Maltose is made of two glucose units; sucrose of one glucose and one fructose unit; lactose of one galactose and "
      "one glucose unit.",
      ["Maltose → 2 glucose", "Sucrose → 1 glucose + 1 fructose", "Lactose → 1 galactose + 1 glucose",
       "Total glucose = 2 + 1 + 1 = 4 mol"],
      why_others_wrong="3 counts maltose as giving only one glucose; 2 or 1 forget the glucose units in sucrose or "
                       "lactose.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides", seconds=40),

    Q(T_BM, "Carbohydrates", "Intermediate", "direct",
      "In the name D-(+)-glucose, the sign '(+)' indicates that glucose:",
      ["has its –OH group on the right at the lowest asymmetric carbon",
       "is dextrorotatory, rotating plane-polarised light to the right",
       "is a reducing sugar", "has a positive charge in solution"], "B",
      "D/L and (+)/(−) notation",
      "The letter D refers to the configuration (related to glyceraldehyde), while (+) or (−) gives the experimentally "
      "observed direction of optical rotation. The two are independent: D-fructose, for example, is laevorotatory.",
      ["'D': relative configuration", "'(+)': dextrorotatory"],
      why_others_wrong="The –OH on the right at the lowest asymmetric carbon is what 'D' means, not '(+)'; the sign "
                       "says nothing about reducing behaviour or charge.",
      ncert=f"{NC12}, 'Biomolecules', glucose: D- and L- configuration", seconds=30),

    Q(T_BM, "Carbohydrates", "Intermediate", "assertion_reason",
      *ar("Glucose pentaacetate does not react with hydroxylamine.", True,
          "In the pentaacetate the –OH at C-1 of the cyclic (hemiacetal) form is acetylated, so the ring cannot open "
          "to give a free –CHO group.", True, explains=True),
      "Evidence for the cyclic structure of glucose",
      "Glucose itself forms an oxime because its ring opens to the free aldehyde in solution. In the pentaacetate the "
      "anomeric –OH is converted into an acetate, the hemiacetal cannot open, and no free –CHO is available. NCERT uses "
      "this as evidence for the cyclic structure. R explains A.",
      ["Glucose ⇌ open chain (free CHO) → oxime", "Pentaacetate: C-1 –OH acetylated → ring locked",
       "→ no reaction with NH₂OH"],
      ncert=f"{NC12}, 'Biomolecules', cyclic structure of glucose", seconds=45),

    Q(T_BM, "Carbohydrates", "Intermediate", "match_list",
      *ml("Match the carbohydrate in List-I with the glycosidic linkage found in it (List-II).",
          ["Maltose", "Lactose", "Sucrose", "Amylopectin (at the branch points)"],
          ["C1 of α-D-glucose to C2 of β-D-fructose", "C1–C6 linkage between α-D-glucose units",
           "C1 of α-D-glucose to C4 of another glucose unit", "C1 of β-D-galactose to C4 of β-D-glucose"],
          "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D"),
      "Glycosidic linkages in di- and polysaccharides",
      "Maltose: two α-D-glucose units, C1–C4. Lactose: β-D-galactose and β-D-glucose, C1 of galactose to C4 of glucose. "
      "Sucrose: C1 of α-D-glucose to C2 of β-D-fructose, which uses both reducing groups. Amylopectin: C1–C4 in the "
      "chains and C1–C6 at the branches.",
      ["Maltose: III", "Lactose: IV", "Sucrose: I", "Amylopectin branches: II"],
      why_others_wrong="Swapping maltose and lactose ignores that lactose contains galactose; sucrose is the only one "
                       "with a C1–C2 linkage.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides and polysaccharides", seconds=45),

    Q(T_BM, "Carbohydrates", "Advanced", "assertion_reason",
      *ar("Sucrose is dextrorotatory, but after hydrolysis the solution becomes laevorotatory.", True,
          "Both glucose and fructose are laevorotatory.", False),
      "Inversion of cane sugar",
      "Hydrolysis gives equal amounts of D-(+)-glucose (+52.5°) and D-(−)-fructose (−92.4°). Fructose has the larger "
      "rotation, so the mixture is laevorotatory and the change in sign is called inversion. Glucose itself is "
      "dextrorotatory, so R is false.",
      ["Sucrose: +66.5°", "Glucose +52.5°, fructose −92.4°", "Mixture: net laevorotatory (invert sugar)"],
      ncert=f"{NC12}, 'Biomolecules', sucrose: invert sugar", seconds=40),

    Q(T_BM, "Nucleic acids", "Advanced", "match_list",
      *ml("Match the term in List-I with its description in List-II.",
          ["Nucleoside", "Nucleotide", "Phosphodiester linkage", "Complementary base pairing"],
          ["Joins the 5′ and 3′ carbon atoms of the pentose sugars of successive nucleotides",
           "Base + sugar + phosphoric acid (at the 5′ position of the sugar)",
           "Adenine with thymine and guanine with cytosine, through hydrogen bonds", "Base attached to C-1′ of the sugar"],
          "IV II I III", ["II IV I III", "IV II III I", "IV I II III"], "B"),
      "Structure of nucleic acids",
      "A nucleoside is a base joined at the 1′ position of the sugar; a nucleotide also has a phosphate at the 5′ "
      "position. Nucleotides are joined by phosphodiester links between C-5′ and C-3′ of the sugars, and the two "
      "strands of DNA are held together by hydrogen bonds between complementary bases.",
      ["Nucleoside: IV", "Nucleotide: II", "Phosphodiester linkage: I", "Base pairing: III"],
      why_others_wrong="Confusing nucleoside and nucleotide misses the phosphate group; the phosphodiester link joins "
                       "sugars, not bases.",
      ncert=f"{NC12}, 'Biomolecules', nucleic acids: chemical composition and structure", seconds=45),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about carbohydrates are correct?",
          [("Carbohydrates that yield two to ten monosaccharide units on hydrolysis are called oligosaccharides.", True),
           ("Glucose occurs freely in nature as well as in combined form.", True),
           ("Starch is the main storage polysaccharide of plants.", True),
           ("Sucrose is a reducing sugar.", False),
           ("Monosaccharides can be hydrolysed further into simpler polyhydroxy aldehydes or ketones.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
      "Classification and occurrence of carbohydrates",
      "Oligosaccharides give 2–10 monosaccharide units on hydrolysis. Glucose is found free (in fruits, honey) and "
      "combined (in sucrose, starch, cellulose). Starch is the main storage polysaccharide of plants. Sucrose is "
      "non-reducing because the reducing groups of both units form the glycosidic bond, and monosaccharides cannot be "
      "hydrolysed further.",
      ["(a) true", "(b) true", "(c) true", "(d) false: non-reducing", "(e) false: simplest carbohydrates"],
      ncert=f"{NC12}, 'Biomolecules', carbohydrates: classification", seconds=45),
]

# ================================================================ Principles Related to Practical Chemistry (2244-2250)
# 2244: FeSO4.7H2O + (NH4)2SO4 + 6H2O -> FeSO4.(NH4)2SO4.6H2O (1 : 1)
n_2244 = F(278, 100) / mm(Fe=1, S=1, O=11, H=14)
v_2244 = g(n_2244 * 392, 2)
assert mm(Fe=1, S=1, O=11, H=14) == 278 and mm(Fe=1, S=2, O=14, N=2, H=20) == 392 and v_2244 == "3.92 g"
# 2246: 2MnO4- + 5H2C2O4 ; 20.0 mL 0.020 M KMnO4 vs 25.0 mL oxalic acid
n_ox = F(5, 2) * F(20, 1000) * F(20, 1000)
M_ox = n_ox / F(25, 1000)
v_2246 = f"{float(M_ox * mm(C=2, H=6, O=6)):.2f} g L⁻¹"
assert M_ox == F(4, 100) and mm(C=2, H=6, O=6) == 126 and v_2246 == "5.04 g L⁻¹"
assert f"{float(M_ox * 90):.2f}" == "3.60"                                               # anhydrous molar mass
# 2248: group II cations (H2S in dilute HCl)
group = {"Cu2+": 2, "Cd2+": 2, "As3+": 2, "Zn2+": 4, "Ni2+": 4, "Al3+": 3, "Ba2+": 5}
v_2248 = str(sum(1 for gr in group.values() if gr == 2))
assert v_2248 == "3"
# 2249: C2H5OH + 4I2 + 6NaOH -> CHI3 + HCOONa + 5NaI + 5H2O
n_2249 = F(23, 10) / mm(C=2, H=6, O=1)
m_i2 = n_2249 * 4 * 254
m_chi3 = n_2249 * mm(C=1, H=1, I=3)
assert n_2249 == F(1, 20) and (m_i2, m_chi3) == (F(508, 10), F(197, 10))
v_2249 = f"{float(m_i2):.1f} g and {float(m_chi3):.1f} g"
assert v_2249 == "50.8 g and 19.7 g"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O (molar mass 392 g mol⁻¹), is prepared by crystallising an equimolar solution "
      "of ferrous sulphate and ammonium sulphate. The maximum mass of Mohr's salt that can be obtained from 2.78 g of "
      "FeSO₄·7H₂O (molar mass 278 g mol⁻¹) with excess ammonium sulphate is:",
      [v_2244, "2.78 g", "1.96 g", "7.84 g"], "A", v_2244,
      "Preparation of a double salt",
      "One mole of FeSO₄·7H₂O gives one mole of the double salt, which crystallises with six molecules of water.",
      ["n(FeSO₄·7H₂O) = 2.78/278 = 0.010 mol", "n(Mohr's salt) = 0.010 mol", "Mass = 0.010 × 392 = 3.92 g"],
      why_others_wrong="2.78 g assumes equal masses; 1.96 g and 7.84 g halve or double the moles.",
      ncert=f"{LAB}, preparation of double salts: Mohr's salt", seconds=40),

    Q(T_PR, "Detection of elements and functional groups", "Basic", "direct",
      "A sample is heated with a little solid potassium hydrogensulphate, and a pungent, irritating smell of acrolein "
      "is noticed. The sample is most likely:",
      ["a protein", "a carbohydrate", "a fat or oil", "an amino acid"], "C",
      "Test for fats and oils",
      "On heating with KHSO₄ (a dehydrating agent), the glycerol part of a fat or oil is dehydrated to acrolein "
      "(propenal), which has a sharp, irritating smell. This acrolein test identifies fats and oils.",
      ["Fat/oil → glycerol part", "KHSO₄, heat: glycerol → CH₂=CH–CHO (acrolein)", "Pungent smell → fat or oil"],
      why_others_wrong="Proteins and amino acids are tested by the biuret and ninhydrin tests, carbohydrates by "
                       "Molisch's test.",
      ncert=f"{LAB}, tests for carbohydrates, fats and proteins", seconds=25),

    N(T_PR, "Titrimetric analysis", "Intermediate",
      "25.0 mL of an oxalic acid solution needs 20.0 mL of 0.020 M KMnO₄ for complete reaction in dilute H₂SO₄. The "
      "strength of the oxalic acid solution, expressed as grams of crystalline oxalic acid, H₂C₂O₄·2H₂O, per litre, "
      "is (C = 12, H = 1, O = 16):",
      ["3.60 g L⁻¹", "2.02 g L⁻¹", v_2246, "12.6 g L⁻¹"], "C", v_2246,
      "Permanganate–oxalic acid titration",
      "In acid, 2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O, so 2 mol MnO₄⁻ react with 5 mol oxalic acid.",
      ["n(MnO₄⁻) = 0.020 × 0.0200 = 4.0 × 10⁻⁴ mol", "n(oxalic acid) = 5/2 × 4.0 × 10⁻⁴ = 1.0 × 10⁻³ mol",
       "Molarity = 1.0 × 10⁻³/0.0250 = 0.040 M", "Strength = 0.040 × 126 = 5.04 g L⁻¹"],
      why_others_wrong="3.60 g L⁻¹ uses the anhydrous molar mass (90); 2.02 g L⁻¹ takes a 1 : 1 mole ratio; "
                       "12.6 g L⁻¹ takes the solution as 0.1 M.",
      ncert=f"{LAB}, titrimetric exercises: oxalic acid vs KMnO₄", seconds=75),

    Q(T_PR, "Titrimetric analysis", "Intermediate", "assertion_reason",
      *ar("In the titration of oxalic acid with KMnO₄, the first few drops of permanganate are decolourised slowly, "
          "but later drops are decolourised almost at once.", True,
          "The Mn²⁺ ions formed in the reaction catalyse the reaction between permanganate and oxalic acid "
          "(autocatalysis).", True, explains=True),
      "Autocatalysis in permanganate titrations",
      "At the start no Mn²⁺ is present and the reaction is slow even in warm solution. As soon as some Mn²⁺ forms, it "
      "catalyses the reaction, so it speeds up. R explains A.",
      ["Start: no Mn²⁺ → slow", "Mn²⁺ produced → catalyst", "Reaction becomes fast (autocatalysis)"],
      ncert=f"{LAB}, titration of oxalic acid with potassium permanganate", seconds=35),

    N(T_PR, "Qualitative salt analysis", "Intermediate",
      "In systematic salt analysis, how many of the following cations are precipitated in group II, as sulphides by "
      "H₂S in the presence of dilute HCl?\nCu²⁺, Cd²⁺, As³⁺, Zn²⁺, Ni²⁺, Al³⁺, Ba²⁺",
      ["1", "2", v_2248, "4"], "C", v_2248,
      "Group separation of cations",
      "In dilute HCl the sulphide ion concentration is kept low (common ion effect on H₂S), so only the sulphides with "
      "very low solubility products (group II) precipitate. Zn²⁺ and Ni²⁺ come down as sulphides only in ammoniacal "
      "solution (group IV); Al³⁺ is precipitated as hydroxide in group III and Ba²⁺ as carbonate in group V.",
      ["Group II: Cu²⁺, Cd²⁺, As³⁺", "Group III: Al³⁺; group IV: Zn²⁺, Ni²⁺; group V: Ba²⁺", "Count = 3"],
      why_others_wrong="4 wrongly places Zn²⁺ or Ni²⁺ in group II; 1 or 2 miss Cd²⁺ or As³⁺.",
      ncert=f"{LAB}, qualitative analysis of cations", seconds=45),

    N(T_PR, "Preparations", "Advanced",
      "Iodoform is prepared in the laboratory by warming ethanol with iodine and aqueous NaOH:\n"
      "C₂H₅OH + 4I₂ + 6NaOH → CHI₃ + HCOONa + 5NaI + 5H₂O\n"
      "For complete conversion of 2.3 g of ethanol, the minimum mass of iodine needed and the mass of iodoform "
      "formed are, respectively (C = 12, H = 1, O = 16, I = 127):",
      [v_2249, "12.7 g and 19.7 g", "50.8 g and 39.4 g", "38.1 g and 19.7 g"], "A", v_2249,
      "Stoichiometry of the iodoform reaction",
      "Ethanol is first oxidised to ethanal by the hypoiodite (one I₂), and the CH₃ group of ethanal is then "
      "tri-iodinated (three I₂) before cleavage, so 4 mol I₂ are used per mole of ethanol.",
      ["n(C₂H₅OH) = 2.3/46 = 0.050 mol", "I₂ = 4 × 0.050 = 0.20 mol × 254 = 50.8 g",
       "CHI₃ (394 g mol⁻¹) = 0.050 × 394 = 19.7 g"],
      why_others_wrong="12.7 g uses one I₂ per ethanol; 38.1 g uses three (forgets the oxidation step); 39.4 g doubles "
                       "the iodoform.",
      ncert=f"{LAB}, preparation of iodoform", seconds=90),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "multi_statement",
      *ms("Which of the following statements about the kinetics experiments in the laboratory are correct?",
          [("In the reaction of sodium thiosulphate with hydrochloric acid, the time for a cross mark under the flask to "
            "disappear is taken as inversely proportional to the rate.", True),
           ("In that reaction, the turbidity is due to colloidal sulphur formed in the reaction.", True),
           ("In the iodide–hydrogen peroxide clock reaction with starch and a little thiosulphate, the blue colour "
            "appears only after all the added thiosulphate has been used up.", True),
           ("Raising the temperature increases the time taken for the cross to disappear.", False),
           ("Starch acts as a catalyst in the iodide–hydrogen peroxide reaction.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
      "Following reaction rates by a visual end point",
      "Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S + H₂O: the sulphur makes the solution turbid, and the faster the reaction the "
      "sooner the cross is hidden, so rate ∝ 1/t. In the clock reaction, the iodine formed is reduced back to iodide "
      "by thiosulphate; only when the thiosulphate is used up does iodine remain and give the blue starch–iodine "
      "colour. Starch is only an indicator. A higher temperature speeds up the reaction and shortens the time.",
      ["(a) true", "(b) true", "(c) true", "(d) false: higher temperature → shorter time",
       "(e) false: starch is an indicator"],
      ncert=f"{LAB}, chemical kinetics experiments", seconds=55),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_PB: (4, 5, 4), T_DF: (4, 4, 3), T_CC: (4, 6, 4), T_PU: (1, 2, 1), T_GO: (5, 7, 5), T_HC: (4, 6, 4),
        T_HX: (3, 4, 3), T_OX: (5, 7, 5), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (2, 3, 2)}
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "Package CHE_009_p2: 127 original Chemistry questions (p-block, d- and f-block, coordination compounds, "
                    "organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_009/CHE_009_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
