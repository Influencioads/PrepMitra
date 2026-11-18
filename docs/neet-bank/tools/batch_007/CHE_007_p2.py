"""Writes batches/parts/BATCH_007_CHE_p2.json: package CHE_007_p2 of BATCH_007 (Chemistry, 130 questions).

Topics: p-Block Elements, d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of
Organic Compounds, Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens /
Oxygen / Nitrogen, Biomolecules (Chemistry), Principles Related to Practical Chemistry.
IDs NEET_CHE_001621..NEET_CHE_001750.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_007/CHE_007_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_007_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 1621, 1750
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
OLD11 = "Class 11 Chemistry (pre-2023 edition)"
OLD12 = "Class 12 Chemistry (pre-2023 edition)"
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


# Atomic masses used in the stems
AM = {"C": 12, "H": 1, "O": 16, "N": 14, "S": 32, "Na": 23, "Cl": F(355, 10), "K": 39, "Br": 80, "I": 127,
      "Ag": 108, "Mn": 55, "Cr": 52, "Fe": 56, "Au": 197, "Zn": 65, "Mg": 24, "Ca": 40}


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    return sum(AM[k] * v for k, v in atoms.items())


QUESTIONS = []

# ================================================================ p-Block Elements (1621-1633)
def unpaired_p(n):
    """Unpaired electrons in an np^n subshell (Hund's rule)."""
    return n if n <= 3 else 6 - n


# 1623: P (3p3), S (3p4), Cl (3p5), Ar (3p6)
n3p = {"P": 3, "S": 4, "Cl": 5, "Ar": 6}
v_1623 = str(sum(unpaired_p(n) for n in n3p.values()))
assert v_1623 == "6" and sum(n3p.values()) == 18
# 1628: Pb (Z 82) = [Xe] 4f14 5d10 6s2 6p2 ; Pb2+ loses the two 6p electrons -> 6th shell keeps 6s2
pb_shell6 = {"6s": 2, "6p": 2}
pb2_shell6 = {"6s": 2, "6p": 0}
v_1628 = str(sum(pb2_shell6.values()))
assert v_1628 == "2" and sum(pb_shell6.values()) == 4 and 2 + 6 + 10 == 18
# 1625: atomic number -> group (Z of the noble gas before it, then count)
groups = {32: 14, 52: 16, 83: 15, 86: 18}
assert groups[32] == 32 - 18 and groups[52] == 52 - 36 and groups[86] == 18
assert groups[83] == 83 - 54 - 14  # 6th period: 14 f-electrons sit between Ba and the d-block
# 1631: (n-1)d10 present? B, Al, C, Si: no ; Ga, In, Ge, Sn: yes
d10 = {"B": False, "Al": False, "Ga": True, "In": True, "C": False, "Si": False, "Ge": True, "Sn": True}
v_1631 = str(sum(d10.values()))
assert v_1631 == "4"

QUESTIONS += [
    Q(T_PB, "Group 17 and 18 trends", "Basic", "direct",
      "An element of the p-block has the ground-state electronic configuration [Kr] 4d¹⁰ 5s² 5p⁵. The element is:",
      ["Tellurium", "Iodine", "Antimony", "Xenon"], "B",
      "Valence-shell configuration of the p-block groups",
      "The valence shell is n = 5 with seven electrons (5s² 5p⁵), the configuration ns² np⁵ of group 17. The group 17 "
      "element of the fifth period is iodine (Z = 36 + 10 + 7 = 53).",
      ["Outer configuration 5s² 5p⁵ → ns² np⁵ → group 17", "n = 5 → period 5", "Group 17, period 5 → iodine"],
      why_others_wrong="Tellurium is 5p⁴ (group 16), antimony 5p³ (group 15) and xenon 5p⁶ (group 18).",
      ncert=f"{OLD12}, 'The p-Block Elements', group 17: electronic configuration", seconds=25),

    Q(T_PB, "Group 17 and 18 trends", "Basic", "direct",
      "In which group of the p-block do all the elements from the second period down to the fifth period exist as "
      "diatomic molecules in the free (elemental) state?",
      ["Group 15", "Group 16", "Group 17", "Group 18"], "C",
      "Molecular nature of the p-block elements",
      "The halogens F₂, Cl₂, Br₂ and I₂ are all diatomic. In group 15 only nitrogen is diatomic (phosphorus forms P₄), "
      "in group 16 only oxygen is diatomic (sulphur forms S₈), and the noble gases are monoatomic.",
      ["Group 15: N₂ but P₄", "Group 16: O₂ but S₈", "Group 17: F₂, Cl₂, Br₂, I₂ → all diatomic",
       "Group 18: monoatomic"],
      why_others_wrong="Groups 15 and 16 have only their first member diatomic; group 18 elements are monoatomic.",
      ncert=f"{OLD12}, 'The p-Block Elements', group 17 elements: physical properties", seconds=25),

    N(T_PB, "Group 15 and 16 trends", "Basic",
      "The total number of unpaired electrons in the ground-state atoms of phosphorus (Z = 15), sulphur (Z = 16), "
      "chlorine (Z = 17) and argon (Z = 18), taken together, is:",
      ["3", "6", "18", "9"], "B", v_1623,
      "Hund's rule applied to the np subshell of the p-block elements",
      "The 3p subshell holds three, four, five and six electrons in P, S, Cl and Ar. By Hund's rule the electrons "
      "occupy the three 3p orbitals singly before pairing.",
      ["P 3p³ → 3 unpaired", "S 3p⁴ → 2 unpaired", "Cl 3p⁵ → 1 unpaired", "Ar 3p⁶ → 0 unpaired",
       "Total = 3 + 2 + 1 + 0 = 6"],
      why_others_wrong="3 counts phosphorus only; 18 counts all the 3p electrons, paired or not; 9 takes S and Cl as "
                       "having three unpaired electrons each, like P.",
      ncert=f"{OLD12}, 'The p-Block Elements', electronic configuration of groups 15–18", seconds=40),

    Q(T_PB, "Group 13 and 14 trends", "Basic", "statement_pair",
      *sp("Every element placed in groups 13 to 18 of the periodic table has the valence-shell configuration "
          "ns² np¹⁻⁶.", False,
          "The number of valence electrons in an atom of a p-block element is equal to its group number.", False),
      "General configuration of the p-block elements",
      "The valence configuration ns² np¹⁻⁶ holds for the p-block elements except helium, which is placed in group 18 "
      "but has the configuration 1s². So Statement I ('every element') is false. A p-block element has (group "
      "number − 10) valence electrons, e.g. three for group 13 and seven for group 17, so Statement II is false.",
      ["Helium (group 18) is 1s², with no p electrons → Statement I false",
       "Valence electrons = group number − 10 (e.g. Cl, group 17 → 7) → Statement II false"],
      ncert=f"{NC11}, 'Classification of Elements and Periodicity in Properties', p-block elements", seconds=35),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "match_list",
      *ml("Match the atomic number of the element in List-I with the group of the periodic table to which it belongs "
          "in List-II.",
          ["Z = 32", "Z = 52", "Z = 83", "Z = 86"],
          ["Group 15", "Group 18", "Group 14", "Group 16"],
          "III IV I II", ["III I IV II", "IV III I II", "III IV II I"], "D"),
      "Locating p-block elements from their electronic configurations",
      "Z = 32: [Ar] 3d¹⁰ 4s² 4p² (germanium, group 14). Z = 52: [Kr] 4d¹⁰ 5s² 5p⁴ (tellurium, group 16). "
      "Z = 83: [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p³ (bismuth, group 15). Z = 86: [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁶ (radon, group 18).",
      ["32 → 4p² → group 14 (III)", "52 → 5p⁴ → group 16 (IV)", "83 → 6p³ → group 15 (I)",
       "86 → 6p⁶ → group 18 (II)"],
      why_others_wrong="The other codes interchange groups 15 and 16, or 14 and 16, or groups 15 and 18.",
      ncert=f"{NC11}, 'Classification of Elements and Periodicity in Properties', electronic configurations and "
            f"the periodic table", seconds=60),

    Q(T_PB, "Anomalous first element", "Intermediate", "assertion_reason",
      *ar("Oxygen has a less negative electron gain enthalpy than sulphur.", True,
          "The oxygen atom is very small, so an incoming electron is strongly repelled by the electrons already "
          "present in its compact 2p subshell.", True, explains=True),
      "Anomalous electron gain enthalpy of the first member of group 16",
      "Down a group the electron gain enthalpy normally becomes less negative, but oxygen (−141 kJ mol⁻¹) is less "
      "negative than sulphur (−200 kJ mol⁻¹). Because the oxygen atom is so compact, the added electron feels strong "
      "electron–electron repulsion, which outweighs its closeness to the nucleus. R is the reason for A.",
      ["ΔegH: O −141, S −200 kJ mol⁻¹ → A true", "Small 2p shell → strong interelectronic repulsion → R true",
       "R explains A"],
      ncert=f"{OLD12}, 'The p-Block Elements', group 16: electron gain enthalpy", seconds=40),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "statement_pair",
      *sp("Among the oxides of a group 14 element, the oxide in the higher oxidation state is more acidic than the "
          "oxide in the lower oxidation state.", True,
          "The tendency of the group 14 elements to form compounds in the +2 oxidation state decreases down the "
          "group from carbon to lead.", False),
      "Oxidation states and nature of oxides in group 14",
      "NCERT notes that for group 14 the oxides in higher oxidation states are generally more acidic than those in "
      "lower oxidation states, so Statement I is true. Because of the inert pair effect, the +2 state becomes more "
      "important down the group (lead prefers +2), so Statement II states the trend the wrong way round.",
      ["Higher oxidation state → more acidic oxide → Statement I true",
       "Inert pair effect → +2 state more stable down the group → Statement II false"],
      ncert=f"{OLD11}, 'The p-Block Elements', group 14: oxidation states and reactivity towards oxygen",
      seconds=40),

    N(T_PB, "Group 13 and 14 trends", "Intermediate",
      "Lead has the ground-state configuration [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p² (Z = 82). The number of electrons in the "
      "outermost (sixth) shell of the Pb²⁺ ion is:",
      ["4", "0", "2", "18"], "C", v_1628,
      "Inert pair effect in the configuration of Pb²⁺",
      "Pb²⁺ is formed by the loss of the two 6p electrons. The 6s² pair is retained (the inert pair), so the sixth "
      "shell of Pb²⁺ still holds two electrons.",
      ["Pb: sixth shell = 6s² 6p² (4 electrons)", "Pb²⁺: remove the two 6p electrons",
       "Sixth shell of Pb²⁺ = 6s² → 2 electrons"],
      why_others_wrong="4 is the count for the neutral atom; 0 treats Pb²⁺ as if all four valence electrons were lost "
                       "(that is Pb⁴⁺); 18 is the count of the fifth shell (5s² 5p⁶ 5d¹⁰).",
      ncert=f"{OLD11}, 'The p-Block Elements', group 14: electronic configuration and oxidation states",
      seconds=40),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "direct",
      "Which of the following p-block elements has a completely filled 4f subshell in its ground state?",
      ["Lead (Z = 82)", "Tin (Z = 50)", "Antimony (Z = 51)", "Iodine (Z = 53)"], "A",
      "Filled inner subshells in the heavier p-block elements",
      "The 4f subshell is filled only after the 6s level, in the lanthanoids (Z = 58–71). Elements of the sixth "
      "period beyond the lanthanoids, such as lead ([Xe] 4f¹⁴ 5d¹⁰ 6s² 6p²), carry a filled 4f subshell. Tin, "
      "antimony and iodine belong to the fifth period and have no 4f electrons.",
      ["4f fills from Ce to Lu (6th period)", "Pb (6th period, after the lanthanoids) → 4f¹⁴",
       "Sn, Sb, I (5th period) → [Kr] 4d¹⁰ 5s² 5pⁿ, no 4f electrons"],
      why_others_wrong="Tin, antimony and iodine have a filled 4d subshell but an empty 4f subshell.",
      ncert=f"{OLD12}, 'The p-Block Elements', electronic configurations of the heavier elements", seconds=35),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "direct",
      "An element X has the ground-state configuration [Ar] 3d¹⁰ 4s² 4p³. Which of the following statements about "
      "X is correct?",
      ["X is the most metallic element of its group.",
       "The hydride XH₃ is a stronger base than ammonia.",
       "Like nitrogen, X cannot show a covalency greater than four.",
       "The oxide X₂O₃ is amphoteric."], "D",
      "Identifying a group 15 element and applying group trends",
      "The configuration 4s² 4p³ is that of arsenic (group 15, period 4). Among the +3 oxides of group 15, those of "
      "nitrogen and phosphorus are acidic, those of arsenic and antimony are amphoteric, and that of bismuth is "
      "predominantly basic. Bismuth, not arsenic, is the most metallic member; the basicity of the hydrides falls "
      "from NH₃ down the group; and unlike nitrogen, arsenic has vacant d orbitals and can expand its covalency.",
      ["4s² 4p³ → group 15, period 4 → arsenic", "As₂O₃ → amphoteric", "Bi is the most metallic",
       "NH₃ is the most basic hydride", "As can exceed covalency 4 (e.g. pentahalides)"],
      why_others_wrong="Bismuth is the most metallic element of group 15; AsH₃ is a much weaker base than NH₃; only "
                       "nitrogen is limited to a covalency of four.",
      ncert=f"{OLD12}, 'The p-Block Elements', group 15: trends in properties of oxides and hydrides", seconds=60),

    N(T_PB, "Group 13 and 14 trends", "Advanced",
      "How many of the following elements have a completely filled d subshell in the shell just inside the valence "
      "shell, i.e. an (n − 1)d¹⁰ subshell?\n"
      "B (Z = 5), Al (Z = 13), Ga (Z = 31), In (Z = 49), C (Z = 6), Si (Z = 14), Ge (Z = 32), Sn (Z = 50)",
      ["4", "2", "6", "8"], "A", v_1631,
      "Inner d¹⁰ subshells in groups 13 and 14",
      "The elements of the second and third periods have no d electrons at all. The members of groups 13 and 14 "
      "from the fourth period onwards come after a transition series, so they carry a filled (n − 1)d¹⁰ subshell: "
      "Ga and Ge (3d¹⁰), In and Sn (4d¹⁰).",
      ["B, C: [He] 2s² 2pⁿ → no d", "Al, Si: [Ne] 3s² 3pⁿ → no d", "Ga, Ge: [Ar] 3d¹⁰ 4s² 4pⁿ → yes",
       "In, Sn: [Kr] 4d¹⁰ 5s² 5pⁿ → yes", "Count = 4"],
      why_others_wrong="2 counts only the fifth-period elements; 6 wrongly includes Al and Si, whose shell inside the "
                       "valence shell is the second shell (no d subshell); 8 counts every element.",
      ncert=f"{OLD11}, 'The p-Block Elements', groups 13 and 14: electronic configuration", seconds=60),

    Q(T_PB, "Group 13 and 14 trends", "Advanced", "multi_statement",
      *ms("Which of the following statements about the oxidation states of the group 14 elements are correct?",
          [("Tin(II) compounds act as reducing agents.", True),
           ("Lead(IV) compounds act as oxidising agents.", True),
           ("Germanium forms stable compounds mainly in the +2 oxidation state.", False),
           ("For carbon and silicon, the +2 oxidation state is more stable than the +4 state.", False)],
          [["a", "c"], ["b", "d"], ["a", "b", "d"]], "C"),
      "Inert pair effect and the redox behaviour of group 14 compounds",
      "Down group 14 the ns² pair becomes reluctant to take part in bonding, so the +2 state gains stability. "
      "Germanium forms stable compounds in the +4 state and only a few in +2. Tin shows both states, and Sn(II) "
      "readily changes to Sn(IV), so it is a reducing agent. For lead, +2 is the stable state, so Pb(IV) compounds "
      "are strong oxidising agents. Carbon and silicon are typically tetravalent (+4).",
      ["(a) Sn²⁺ → Sn⁴⁺ readily → reducing → true", "(b) Pb⁴⁺ → Pb²⁺ readily → oxidising → true",
       "(c) Ge: mainly +4 → false", "(d) C and Si: +4 is the stable state → false"],
      why_others_wrong="Every other option includes (c) or (d), or leaves out one of the two true statements.",
      ncert=f"{OLD11}, 'The p-Block Elements', group 14: oxidation states and trends in chemical reactivity",
      seconds=60),

    Q(T_PB, "Group 13 and 14 trends", "Advanced", "assertion_reason",
      *ar("The atomic radius of gallium is smaller than that of aluminium, although gallium lies below aluminium in "
          "group 13.", True,
          "The ten 3d electrons in gallium shield the nucleus poorly, so its outer electrons experience a larger "
          "effective nuclear charge.", True, explains=True),
      "Anomaly in the atomic radii of group 13",
      "Atomic radii normally increase down a group, but gallium (135 pm) is smaller than aluminium (143 pm). Between "
      "aluminium and gallium a full 3d subshell is added; d electrons screen the nucleus poorly, so the increase in "
      "nuclear charge is not offset and the outer electrons are pulled in. R explains A.",
      ["Al 143 pm, Ga 135 pm → A true", "3d¹⁰ poor shielding → higher effective nuclear charge → R true",
       "R explains A"],
      ncert=f"{OLD11}, 'The p-Block Elements', group 13: atomic radii", seconds=45),
]

# ================================================================ d- and f-Block Elements (1634-1646)
# 1637: % Mn in KMnO4
m_kmno4 = mm(K=1, Mn=1, O=4)
assert m_kmno4 == 158
v_1637 = pct(F(AM["Mn"]) / m_kmno4)
assert v_1637 == "34.8%" and pct(F(39, 158)) == "24.7%" and pct(F(64, 158)) == "40.5%" and pct(F(55, 119)) == "46.2%"
# 1638: Cr2O7(2-) + 3Sn2+ ; 20.0 mL of 0.050 M dichromate ; 0.10 M SnCl2
n_cr_1638 = F(20, 1000) * F(5, 100)
n_sn_1638 = 3 * n_cr_1638            # 6 e- gained by Cr2O7(2-), 2 e- lost per Sn2+
assert 6 / 2 == 3
v_1638 = g(n_sn_1638 / F(1, 10) * 1000, 1, " mL")
assert v_1638 == "30.0 mL" and g(n_cr_1638 / F(1, 10) * 1000, 1, " mL") == "10.0 mL"
assert g(6 * n_cr_1638 / F(1, 10) * 1000, 1, " mL") == "60.0 mL" and g(2 * n_cr_1638 / F(1, 10) * 1000, 1, " mL") == "20.0 mL"
# 1640: U (Z 92) = [Rn] 5f3 6d1 7s2 ; U4+ loses 7s2, 6d1 and one 5f electron
v_1640 = str(3 - (4 - 2 - 1))
assert v_1640 == "2"
# 1643: 0.20 g impure K2Cr2O7 ; 30.0 mL of 0.10 M Fe2+ ; Cr2O7(2-) : Fe2+ = 1 : 6
m_k2cr2o7 = mm(K=2, Cr=2, O=7)
m_na2cr2o7 = mm(Na=2, Cr=2, O=7)
assert m_k2cr2o7 == 294 and m_na2cr2o7 == 262
n_fe_1643 = F(30, 1000) * F(1, 10)
v_1643 = pct(n_fe_1643 / 6 * m_k2cr2o7 / F(2, 10))
assert v_1643 == "73.5%"
assert pct(n_fe_1643 / 5 * m_k2cr2o7 / F(2, 10)) == "88.2%"
assert pct(n_fe_1643 / 12 * m_k2cr2o7 / F(2, 10)) == "36.8%"
assert pct(n_fe_1643 / 6 * m_na2cr2o7 / F(2, 10)) == "65.5%"
# 1644: 4f electrons of Ln(n+) = Z - 54 - n (the 6s electrons go first, then 5d if present, then 4f)
ions_1644 = {"Sm2+": (62, 2), "Eu2+": (63, 2), "Eu3+": (63, 3), "Gd3+": (64, 3), "Tb4+": (65, 4), "Dy3+": (66, 3)}
f_count = {k: z - 54 - n for k, (z, n) in ions_1644.items()}
assert f_count == {"Sm2+": 6, "Eu2+": 7, "Eu3+": 6, "Gd3+": 7, "Tb4+": 7, "Dy3+": 9}
v_1644 = str(sum(1 for v in f_count.values() if v == 7))
assert v_1644 == "3"

QUESTIONS += [
    Q(T_DF, "Transition element trends", "Basic", "match_list",
      *ml("Transition metals and their compounds are good catalysts. Match the process in List-I with the catalyst "
          "used in it in List-II.",
          ["Contact process (oxidation of SO₂ to SO₃)", "Haber's process (synthesis of ammonia)",
           "Catalytic hydrogenation", "Reaction between iodide and persulphate ions"],
          ["Nickel", "Fe³⁺ ions", "Vanadium(V) oxide", "Finely divided iron"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "C"),
      "Catalytic properties of transition metals and their compounds",
      "NCERT gives V₂O₅ (Contact process), finely divided iron (Haber's process) and nickel (catalytic "
      "hydrogenation) as examples of transition metal catalysts. The reaction 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻ is "
      "catalysed by Fe³⁺ ions, which are reduced by iodide and re-oxidised by persulphate.",
      ["A → V₂O₅ (III)", "B → finely divided iron (IV)", "C → nickel (I)", "D → Fe³⁺ ions (II)"],
      why_others_wrong="The other codes interchange V₂O₅ with iron, nickel with Fe³⁺, or iron with nickel.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', catalytic properties", seconds=40),

    Q(T_DF, "Magnetic and colour properties", "Basic", "match_list",
      *ml("Match the aquated metal ion in List-I with its colour in aqueous solution in List-II.",
          ["Cr³⁺", "Fe³⁺", "Co²⁺", "Ni²⁺"],
          ["Green", "Pink", "Violet", "Yellow"],
          "III IV II I", ["I IV II III", "III II IV I", "IV III II I"], "A"),
      "Colours of hydrated ions of the first transition series",
      "Colour arises from d–d transitions of the partly filled 3d subshell. NCERT lists the aquated ions: Cr³⁺ "
      "violet, Fe³⁺ yellow, Co²⁺ pink and Ni²⁺ green.",
      ["Cr³⁺ (3d³) → violet (III)", "Fe³⁺ (3d⁵) → yellow (IV)", "Co²⁺ (3d⁷) → pink (II)",
       "Ni²⁺ (3d⁸) → green (I)"],
      why_others_wrong="The other codes interchange the violet and green ions, or the yellow and pink ones.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', formation of coloured ions (table of colours)", seconds=35),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "direct",
      "Which lanthanoid has the ground-state electronic configuration [Xe] 4f¹⁴ 5d¹ 6s²?",
      ["Ytterbium (Z = 70)", "Gadolinium (Z = 64)", "Cerium (Z = 58)", "Lutetium (Z = 71)"], "D",
      "Electronic configurations of the lanthanoids",
      "The configuration contains 54 + 14 + 1 + 2 = 71 electrons, which is lutetium, the last lanthanoid: the 4f "
      "subshell is full and one electron enters 5d. Ytterbium is [Xe] 4f¹⁴ 6s², gadolinium [Xe] 4f⁷ 5d¹ 6s² and "
      "cerium [Xe] 4f¹ 5d¹ 6s².",
      ["Electrons = 54 + 14 + 1 + 2 = 71", "Z = 71 → lutetium"],
      why_others_wrong="Yb has no 5d electron (4f¹⁴ 6s²); Gd has only seven 4f electrons; Ce has one 4f electron.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', lanthanoids: electronic configurations", seconds=30),

    N(T_DF, "K2Cr2O7 and KMnO4", "Basic",
      "The percentage of manganese by mass in potassium permanganate, KMnO₄, is (K = 39, Mn = 55, O = 16):",
      ["46.2%", "34.8%", "24.7%", "40.5%"], "B", v_1637,
      "Percentage composition of potassium permanganate",
      "Molar mass of KMnO₄ = 39 + 55 + 4 × 16 = 158 g mol⁻¹, of which manganese contributes 55 g.",
      ["M(KMnO₄) = 158 g mol⁻¹", "% Mn = 55/158 × 100 = 34.8%"],
      why_others_wrong="46.2% leaves potassium out of the molar mass; 24.7% is the percentage of potassium; 40.5% is "
                       "the percentage of oxygen.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate", seconds=30),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "In acidic solution, dichromate ions oxidise tin(II) to tin(IV) and are themselves reduced to Cr³⁺:\n"
      "Cr₂O₇²⁻ + 14H⁺ + 3Sn²⁺ → 2Cr³⁺ + 3Sn⁴⁺ + 7H₂O\n"
      "The volume of 0.10 M SnCl₂ solution that is oxidised completely by 20.0 mL of 0.050 M K₂Cr₂O₇ solution is:",
      ["10.0 mL", "60.0 mL", "30.0 mL", "20.0 mL"], "C", v_1638,
      "Stoichiometry of oxidation by acidified dichromate",
      "Each Cr₂O₇²⁻ gains six electrons (2Cr: +6 → +3), and each Sn²⁺ loses two electrons, so one dichromate ion "
      "oxidises three Sn²⁺ ions.",
      ["n(Cr₂O₇²⁻) = 0.020 L × 0.050 M = 1.0 × 10⁻³ mol", "n(Sn²⁺) = 3 × 1.0 × 10⁻³ = 3.0 × 10⁻³ mol",
       "V = 3.0 × 10⁻³ / 0.10 = 0.030 L = 30.0 mL"],
      why_others_wrong="10.0 mL takes a 1 : 1 ratio and 20.0 mL a 1 : 2 ratio; 60.0 mL treats Sn²⁺ → Sn⁴⁺ as a "
                       "one-electron change.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate: oxidising action (tin(II) salts)",
      seconds=60),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Intermediate", "statement_pair",
      *sp("Potassium dichromate cannot be used as a primary standard in volumetric analysis.", False,
          "The use of potassium permanganate for bleaching wool, cotton and silk and for decolourising oils depends "
          "on its strong oxidising power.", True),
      "Uses of potassium dichromate and potassium permanganate",
      "NCERT states that potassium dichromate is used as a primary standard in volumetric analysis, so Statement I "
      "is false. NCERT also notes that the uses of KMnO₄ in bleaching textile fibres and decolourising oils depend "
      "on its strong oxidising power, so Statement II is true.",
      ["K₂Cr₂O₇: a primary standard → Statement I false", "KMnO₄: bleaching depends on oxidising power → true"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate (uses)",
      seconds=35),

    N(T_DF, "Lanthanoids and actinoids", "Intermediate",
      "The ground-state configuration of uranium (Z = 92) is [Rn] 5f³ 6d¹ 7s². The number of 5f electrons in the "
      "U⁴⁺ ion is:",
      ["3", "2", "1", "0"], "B", v_1640,
      "Configurations of actinoid ions",
      "On ionisation the 7s electrons are lost first, then the 6d electron, and only then 5f electrons. Removing "
      "four electrons from U takes away 7s², 6d¹ and one 5f electron, leaving 5f².",
      ["U: 5f³ 6d¹ 7s²", "Remove 7s² (2) and 6d¹ (1) → 3 electrons", "Fourth electron from 5f → U⁴⁺ = [Rn] 5f²"],
      why_others_wrong="3 is the 5f count of the neutral atom (or of U³⁺); 1 and 0 remove too many 5f electrons, "
                       "as if the 7s or 6d electrons were kept.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', actinoids: electronic configurations", seconds=40),

    Q(T_DF, "Transition element trends", "Intermediate", "assertion_reason",
      *ar("The highest fluorides formed by vanadium and chromium are VF₅ and CrF₆ respectively.", True,
          "Fluorine stabilises high oxidation states only through the high lattice energy of ionic fluorides.",
          False),
      "Stabilisation of high oxidation states by fluorine",
      "NCERT lists VF₅ and CrF₆ as the halides showing the highest oxidation states of these metals, so A is true. "
      "NCERT explains that fluorine stabilises the highest oxidation state either through a higher lattice energy "
      "(as in CoF₃) or through higher bond enthalpy terms in the higher covalent fluorides (as in VF₅ and CrF₆). "
      "The word 'only' makes R false, and the covalent fluorides VF₅ and CrF₆ are exactly the cases R leaves out.",
      ["VF₅ (+5) and CrF₆ (+6) → A true", "Two factors: lattice energy (CoF₃) or bond enthalpy (VF₅, CrF₆)",
       "R claims lattice energy only → false"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxidation states (halides of the 3d metals)", seconds=45),

    Q(T_DF, "Transition element trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the oxides of vanadium and chromium are correct?",
          [("V₂O₅ is amphoteric, though mainly acidic.", True),
           ("CrO₃ is an acidic oxide.", True),
           ("CrO is a basic oxide.", True),
           ("V₂O₃ is an acidic oxide.", False)],
          [["a", "b"], ["b", "c", "d"], ["a", "c", "d"]], "A"),
      "Acid–base character of transition metal oxides and the oxidation state",
      "For a given metal, the oxide becomes less basic and more acidic as the oxidation state rises. For vanadium "
      "the change is from basic V₂O₃ to less basic V₂O₄ and to amphoteric V₂O₅, which is mainly acidic. For "
      "chromium, CrO is basic, Cr₂O₃ amphoteric and CrO₃ acidic (it gives H₂CrO₄ and H₂Cr₂O₇).",
      ["(a) true", "(b) true", "(c) true", "(d) V₂O₃ (+3, lowest state) is basic → false"],
      why_others_wrong="Options containing (d) are wrong, and (a) and (b) only leaves out the true statement (c).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxides of the 3d metals", seconds=50),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "0.20 g of an impure sample of potassium dichromate is dissolved in dilute H₂SO₄ and titrated with 0.10 M "
      "Fe²⁺ solution. 30.0 mL of the Fe²⁺ solution is needed to reduce all the dichromate to Cr³⁺. Assuming the "
      "impurities do not react, the percentage purity of the sample is (K = 39, Cr = 52, O = 16, Na = 23):",
      ["88.2%", "65.5%", "73.5%", "36.8%"], "C", v_1643,
      "Redox titration of dichromate with iron(II)",
      "Cr₂O₇²⁻ + 14H⁺ + 6Fe²⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O. One dichromate ion accepts six electrons, each Fe²⁺ gives "
      "one, so 6 mol of Fe²⁺ reduce 1 mol of dichromate.",
      ["n(Fe²⁺) = 0.030 × 0.10 = 3.0 × 10⁻³ mol", "n(K₂Cr₂O₇) = 3.0 × 10⁻³ / 6 = 5.0 × 10⁻⁴ mol",
       "Mass = 5.0 × 10⁻⁴ × 294 = 0.147 g", "Purity = 0.147/0.20 × 100 = 73.5%"],
      why_others_wrong="88.2% uses the 1 : 5 ratio of permanganate; 36.8% counts six Fe²⁺ per chromium atom (1 : 12); "
                       "65.5% uses the molar mass of sodium dichromate (262).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate: oxidising action (Fe²⁺ → Fe³⁺)",
      seconds=90),

    N(T_DF, "Lanthanoids and actinoids", "Advanced",
      "How many of the following ions have a half-filled 4f subshell (4f⁷)?\n"
      "Sm²⁺, Eu²⁺, Eu³⁺, Gd³⁺, Tb⁴⁺, Dy³⁺\n"
      "(Atomic numbers: Sm 62, Eu 63, Gd 64, Tb 65, Dy 66; Xe = 54. The atoms are Sm [Xe] 4f⁶ 6s², Eu [Xe] 4f⁷ 6s², "
      "Gd [Xe] 4f⁷ 5d¹ 6s², Tb [Xe] 4f⁹ 6s², Dy [Xe] 4f¹⁰ 6s².)",
      ["2", "4", "5", "3"], "D", v_1644,
      "Configurations of lanthanoid ions in the +2, +3 and +4 states",
      "A lanthanoid ion Lnⁿ⁺ loses the 6s electrons first, then any 5d electron, then 4f electrons, so its number of "
      "4f electrons is Z − 54 − n.",
      ["Sm²⁺: 62 − 56 = 6", "Eu²⁺: 63 − 56 = 7 ✓", "Eu³⁺: 63 − 57 = 6", "Gd³⁺: 64 − 57 = 7 ✓",
       "Tb⁴⁺: 65 − 58 = 7 ✓", "Dy³⁺: 66 − 57 = 9", "Count = 3"],
      shortcut="4f⁷ means Z − n = 61: Eu²⁺ (63 − 2), Gd³⁺ (64 − 3) and Tb⁴⁺ (65 − 4).",
      why_others_wrong="2 misses one of the three f⁷ ions (often Tb⁴⁺); 4 or 5 wrongly include Eu³⁺ or Sm²⁺ (4f⁶) "
                       "or Dy³⁺ (4f⁹).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', lanthanoids: electronic configurations and oxidation states",
      seconds=80),

    Q(T_DF, "Lanthanoids and actinoids", "Advanced", "assertion_reason",
      *ar("Ce(IV) is used as an oxidising agent in analytical work, although the value E°(Ce⁴⁺/Ce³⁺) = +1.74 V "
          "suggests that it could oxidise water.", True,
          "The reaction of Ce⁴⁺ ions with water is very slow.", True, explains=True),
      "Thermodynamic and kinetic factors in the chemistry of cerium(IV)",
      "Ce⁴⁺ (noble gas configuration) is a strong oxidant that reverts to the common +3 state. Its E° value shows "
      "that oxidising water is thermodynamically favourable, but the reaction is very slow, so Ce(IV) solutions "
      "remain usable and Ce(IV) is a good analytical reagent. The slow rate is exactly why A holds.",
      ["E° = +1.74 V → oxidation of water feasible", "Rate of that reaction is very slow",
       "So Ce(IV) solutions are usable → R explains A"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', lanthanoids: oxidation states", seconds=45),

    Q(T_DF, "Lanthanoids and actinoids", "Advanced", "multi_statement",
      *ms("Which of the following statements about the oxidation states of the f-block elements are correct?",
          [("Pr, Nd, Tb and Dy also show the +4 oxidation state, but only in oxides of the type MO₂.", True),
           ("The maximum oxidation state shown by protactinium is +5.", True),
           ("In general, the +2 oxidation state of the lanthanoids is more stable than the +3 state.", False),
           ("All the actinoids show only the +3 oxidation state.", False)],
          [["a", "b", "c"], ["b", "d"], ["a", "c"]], "B"),
      "Oxidation states of the lanthanoids and actinoids",
      "The common oxidation state of the lanthanoids is +3; +2 and +4 occur less often, and Pr, Nd, Tb and Dy show +4 "
      "only in their oxides MO₂. Among the actinoids, the maximum oxidation state rises from +4 in Th to +5, +6 and "
      "+7 in Pa, U and Np, and then decreases. So the actinoids show a wide range of states, not +3 alone.",
      ["(a) true (NCERT)", "(b) Pa → +5 → true", "(c) +3 is the common, most stable state → false",
       "(d) Th +4, U up to +6, Np up to +7 → false"],
      why_others_wrong="The other options include (c) or (d), or leave out (a).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', lanthanoids and actinoids: oxidation states", seconds=55),
]

# ================================================================ Coordination Compounds (1647-1661)
# 1651: [Cr(NH3)4(C2O4)]^x with Cr(III); NH3 neutral, oxalate 2-, didentate
x_1651 = 3 + 4 * 0 + (-2)
cn_1651 = 4 * 1 + 1 * 2
assert (x_1651, cn_1651) == (1, 6)
v_1651 = "+1 and 6"
# 1654: 2[Au(CN)2]- + Zn -> [Zn(CN)4]2- + 2Au ; 1.30 g Zn (Zn = 65)
n_zn_1654 = F(130, 100) / AM["Zn"]
assert n_zn_1654 == F(2, 100)
v_1654 = g(2 * n_zn_1654 * AM["Au"], 2)
assert v_1654 == "7.88 g" and g(n_zn_1654 * AM["Au"], 2) == "3.94 g"
assert g(4 * n_zn_1654 * AM["Au"], 2) == "15.76 g" and g(n_zn_1654 / 2 * AM["Au"], 2) == "1.97 g"
# 1658: [Co(NH3)4Cl(NO2)]+ : MA4BC -> cis/trans (2) ; NO2- bonded through N or O (2) ; no optical isomer
geo_1658, link_1658 = 2, 2
v_1658 = str(geo_1658 * link_1658)
assert v_1658 == "4"

QUESTIONS += [
    Q(T_CC, "Werner's theory and ligands", "Basic", "direct",
      "Which of the following ligands can bind to a metal ion through either of two different kinds of donor atom "
      "(one at a time)?",
      ["Ethane-1,2-diamine", "Thiocyanate ion, SCN⁻", "Oxalate ion, C₂O₄²⁻", "Ammonia"], "B",
      "Ambidentate ligands",
      "A ligand that can ligate through two different atoms is ambidentate. The thiocyanate ion can bind through "
      "sulphur (M–SCN) or through nitrogen (M–NCS). Ethane-1,2-diamine and oxalate are didentate: they bind through "
      "two atoms of the same element (two N or two O) at the same time. Ammonia is unidentate.",
      ["SCN⁻: donor atom S or N → ambidentate", "en: two N at once → didentate", "C₂O₄²⁻: two O at once → didentate",
       "NH₃: one N → unidentate"],
      why_others_wrong="en and oxalate use two donor atoms of the same kind simultaneously (chelation); NH₃ has only "
                       "one donor atom.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions: ligands (ambidentate ligands)", seconds=25),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "In the complex Na₃[Co(NO₂)₆], each nitrite ligand is bonded to cobalt through its nitrogen atom. The IUPAC "
      "name of the compound is:",
      ["Sodium hexanitrito-N-cobaltate(II)", "Sodium hexanitrito-N-cobalt(III)",
       "Sodium hexanitrito-N-cobaltate(III)", "Hexanitrito-N-cobaltate(III) sodium"], "C",
      "Naming an anionic coordination entity",
      "The cation is named first. Oxidation state of Co: x + 6(−1) = −3 → x = +3. Because the complex ion is an "
      "anion, the metal name ends in -ate: cobaltate(III). The N-bonded nitrite ligand is nitrito-N.",
      ["Charge on complex ion = −3 (three Na⁺)", "x − 6 = −3 → Co(III)", "Anionic entity → 'cobaltate'",
       "Name: sodium hexanitrito-N-cobaltate(III)"],
      why_others_wrong="'cobalt(III)' omits the -ate ending needed for an anionic entity; (II) is the wrong oxidation "
                       "state; the cation must be named first.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=35),

    Q(T_CC, "Valence bond theory", "Basic", "statement_pair",
      *sp("Valence bond theory does not make exact predictions about whether a 4-coordinate complex will be "
          "tetrahedral or square planar.", True,
          "Valence bond theory gives a quantitative interpretation of the thermodynamic and kinetic stabilities of "
          "coordination compounds.", False),
      "Limitations of valence bond theory",
      "NCERT lists among the limitations of VBT that it does not make exact predictions regarding the tetrahedral "
      "and square planar structures of 4-coordinate complexes (Statement I true) and that it does not give a "
      "quantitative interpretation of the thermodynamic or kinetic stabilities of coordination compounds "
      "(Statement II false).",
      ["Statement I: a listed limitation → true", "Statement II: VBT cannot do this → false"],
      ncert=f"{NC12}, 'Coordination Compounds', limitations of valence bond theory", seconds=30),

    Q(T_CC, "IUPAC nomenclature", "Basic", "match_list",
      *ml("Match the ligand in List-I with the name used for it in the IUPAC name of a coordination compound "
          "(List-II).",
          ["C₂O₄²⁻", "H₂N–CH₂–CH₂–NH₂", "OH⁻", "CN⁻"],
          ["Cyanido", "Oxalato", "Ethane-1,2-diamine", "Hydroxido"],
          "II III IV I", ["II IV III I", "I III IV II", "IV III II I"], "D"),
      "Names of ligands in IUPAC nomenclature",
      "Anionic ligands take names ending in -o (oxalato, hydroxido, cyanido), while neutral ligands keep their "
      "names (ethane-1,2-diamine), apart from the special names aqua, ammine, carbonyl and nitrosyl.",
      ["C₂O₄²⁻ → oxalato (II)", "en → ethane-1,2-diamine (III)", "OH⁻ → hydroxido (IV)", "CN⁻ → cyanido (I)"],
      why_others_wrong="The other codes interchange the names of the two neutral/anionic ligands or of hydroxido "
                       "and cyanido.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature: naming of ligands", seconds=30),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "In the complex ion [Cr(NH₃)₄(C₂O₄)]ˣ, chromium is in the +3 oxidation state and the oxalate ion acts as a "
      "didentate ligand. The charge x on the complex ion and the coordination number of chromium are, respectively:",
      ["+1 and 6", "+1 and 5", "−1 and 6", "+3 and 6"], "A", v_1651,
      "Charge and coordination number of a coordination entity",
      "Charge = oxidation state of the metal + sum of ligand charges. Coordination number = number of donor atoms "
      "bonded to the metal; a didentate ligand supplies two.",
      ["x = (+3) + 4(0) + (−2) = +1", "CN = 4 (from NH₃) + 2 (from C₂O₄²⁻) = 6"],
      why_others_wrong="5 counts oxalate as unidentate; −1 adds the oxalate charge with the wrong sign; +3 ignores the "
                       "charge of the oxalate ion.",
      ncert=f"{NC12}, 'Coordination Compounds', coordination number and oxidation number", seconds=30),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "direct",
      "The formula of pentaamminecarbonatocobalt(III) chloride is:",
      ["[Co(NH₃)₅(CO₃)]Cl", "[Co(NH₃)₅(CO₃)]Cl₂", "[Co(NH₃)₅Cl]CO₃", "[Co(NH₃)₄(CO₃)]Cl"], "A",
      "Writing a formula from an IUPAC name",
      "The coordination sphere contains five NH₃ ligands and one carbonate ion bonded to Co³⁺. Its charge is "
      "+3 + 5(0) + (−2) = +1, so one chloride ion is needed as the counter ion.",
      ["Ligands: 5 NH₃ + 1 CO₃²⁻", "Charge of [Co(NH₃)₅(CO₃)] = +1", "Formula: [Co(NH₃)₅(CO₃)]Cl"],
      why_others_wrong="[Co(NH₃)₅Cl]CO₃ is pentaamminechloridocobalt(III) carbonate (an ionisation isomer); "
                       "two chlorides would not balance a +1 ion; [Co(NH₃)₄(CO₃)]Cl has only four ammine ligands.",
      ncert=f"{NC12}, 'Coordination Compounds', formulas and nomenclature of mononuclear compounds", seconds=35),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "multi_statement",
      *ms("Which of the following are correct rules for writing the formula of a mononuclear coordination entity?",
          [("The central atom is listed first.", True),
           ("The ligands are then listed in alphabetical order, irrespective of their charge.", True),
           ("For an abbreviated polydentate ligand, the first letter of the abbreviation decides its place in the "
            "alphabetical order.", True),
           ("The charge of a complex ion is written inside the square brackets.", False),
           ("A space is left between the ligands and the metal within the coordination sphere.", False)],
          [["a", "b"], ["a", "c", "d"], ["b", "c", "e"]], "B"),
      "Rules for writing formulas of coordination entities",
      "NCERT's rules: the central atom is listed first; ligands follow in alphabetical order, and their place does "
      "not depend on charge; abbreviated polydentate ligands are placed by the first letter of the abbreviation; "
      "the entire entity is enclosed in square brackets with no space between ligands and metal; the charge of a "
      "complex ion is written outside the brackets as a right superscript.",
      ["(a), (b), (c) true", "(d) charge goes outside the brackets → false", "(e) no space is left → false"],
      why_others_wrong="The other options contain (d) or (e), or leave out one of the true rules.",
      ncert=f"{NC12}, 'Coordination Compounds', formulas of mononuclear coordination entities", seconds=45),

    N(T_CC, "Applications", "Intermediate",
      "In the extraction of gold, the soluble complex [Au(CN)₂]⁻ is treated with zinc:\n"
      "2[Au(CN)₂]⁻ + Zn → [Zn(CN)₄]²⁻ + 2Au\n"
      "The mass of gold recovered when 1.30 g of zinc reacts completely is (Zn = 65, Au = 197):",
      ["3.94 g", "15.76 g", "1.97 g", "7.88 g"], "D", v_1654,
      "Stoichiometry of the recovery of gold from its cyanide complex",
      "Zinc displaces gold from the complex; each zinc atom releases two gold atoms.",
      ["n(Zn) = 1.30/65 = 0.020 mol", "n(Au) = 2 × 0.020 = 0.040 mol", "Mass = 0.040 × 197 = 7.88 g"],
      why_others_wrong="3.94 g takes Zn : Au as 1 : 1; 15.76 g as 1 : 4; 1.97 g inverts the ratio (2 : 1).",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (extraction of gold)", seconds=40),

    Q(T_CC, "Valence bond theory", "Intermediate", "statement_pair",
      *sp("In Mn₂(CO)₁₀, two Mn(CO)₅ units are joined by a manganese–manganese bond.", True,
          "Co₂(CO)₈ contains a cobalt–cobalt bond, which is bridged by two CO groups.", True),
      "Structures of polynuclear metal carbonyls",
      "Besides the mononuclear carbonyls Ni(CO)₄, Fe(CO)₅ and Cr(CO)₆, NCERT shows two dinuclear carbonyls: "
      "Mn₂(CO)₁₀, made of two square pyramidal Mn(CO)₅ units joined by a Mn–Mn bond, and Co₂(CO)₈, which has a "
      "Co–Co bond bridged by two CO groups. Both statements are true.",
      ["Mn₂(CO)₁₀: Mn–Mn bond → Statement I true", "Co₂(CO)₈: Co–Co bond with two bridging CO → Statement II true"],
      ncert=f"{NC12}, 'Coordination Compounds', bonding in metal carbonyls (structures)", seconds=35),

    Q(T_CC, "Crystal field theory", "Intermediate", "assertion_reason",
      *ar("The spectrochemical series is an experimentally determined series, based on the absorption of light by "
          "complexes with different ligands.", True,
          "Carbon monoxide lies at the strong-field end of the spectrochemical series.", True),
      "Origin of the spectrochemical series",
      "A is NCERT's description of how the series is obtained: from absorption spectra of complexes of a metal ion "
      "with different ligands. R is also true, but it only states the position of one ligand in the series; it says "
      "nothing about how the series is determined. So R does not explain A.",
      ["A: series obtained from absorption of light → true", "R: CO causes the largest splitting → true",
       "R is a fact about the series, not the reason for A"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory (spectrochemical series)", seconds=40),

    Q(T_CC, "Applications", "Intermediate", "direct",
      "Metal ions give characteristic colour reactions with chelating reagents such as EDTA, dimethylglyoxime, "
      "α-nitroso-β-naphthol and cupron, because coordination entities are formed. These reactions are used mainly "
      "for:",
      ["purifying metals by forming volatile complexes",
       "the detection and estimation of metal ions",
       "electroplating articles with a smooth coating of metal",
       "removing excess metal ions from the body by chelate therapy"], "B",
      "Coordination compounds in chemical analysis",
      "NCERT states that colour reactions of metal ions with ligands, especially chelating ligands, form the basis of "
      "their detection and estimation by classical and instrumental methods of analysis; EDTA, DMG, "
      "α-nitroso-β-naphthol and cupron are examples of such reagents.",
      ["Coloured coordination entities → qualitative detection", "Measured quantitatively → estimation"],
      why_others_wrong="Purification uses volatile complexes such as Ni(CO)₄; electroplating uses cyanido complexes; "
                       "chelate therapy uses EDTA, D-penicillamine or desferrioxime B, not these colour reactions.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (qualitative and quantitative analysis)",
      seconds=30),

    N(T_CC, "Isomerism", "Advanced",
      "Counting geometrical and linkage isomers together, how many isomers are possible for the octahedral complex "
      "ion [Co(NH₃)₄Cl(NO₂)]⁺? (No optical isomer exists for this ion.)",
      ["2", "6", "3", "4"], "D", v_1658,
      "Combining geometrical and linkage isomerism",
      "[Co(NH₃)₄Cl(NO₂)]⁺ is of the type [MA₄BC], which has cis and trans forms. Independently, the ambidentate "
      "nitrite ligand may be bonded through N (nitrito-N) or through O (nitrito-O). Each geometrical form can carry "
      "either linkage.",
      ["Geometrical: cis and trans → 2", "Linkage: –NO₂ or –ONO → 2", "Total = 2 × 2 = 4"],
      why_others_wrong="2 counts only one kind of isomerism; 3 forgets one combination; 6 adds non-existent optical "
                       "isomers.",
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=60),

    Q(T_CC, "Valence bond theory", "Advanced", "match_list",
      *ml("Match the complex ion in List-I with its hybridisation and number of unpaired electrons, according to "
          "valence bond theory, in List-II. (Atomic numbers: Cr 24, Fe 26, Co 27, Pt 78)",
          ["[CoCl₄]²⁻ (tetrahedral)", "[Fe(H₂O)₆]³⁺ (high spin)", "[Pt(NH₃)₄]²⁺ (square planar)", "[Cr(NH₃)₆]³⁺"],
          ["d²sp³, three unpaired electrons", "dsp², no unpaired electron", "sp³d², five unpaired electrons",
           "sp³, three unpaired electrons"],
          "IV III II I", ["I III II IV", "IV II III I", "III IV II I"], "A"),
      "Hybridisation and magnetic behaviour from valence bond theory",
      "Co²⁺ (3d⁷) in tetrahedral [CoCl₄]²⁻ uses sp³ hybrids and keeps three unpaired electrons. High-spin Fe³⁺ (3d⁵) "
      "keeps five unpaired electrons and uses outer 4d orbitals (sp³d²). Pt²⁺ (5d⁸) in a square planar complex pairs "
      "its electrons and uses dsp² hybrids, so it is diamagnetic. Cr³⁺ (3d³) has two vacant inner 3d orbitals for "
      "d²sp³ hybridisation and three unpaired electrons.",
      ["A → sp³, 3 unpaired (IV)", "B → sp³d², 5 unpaired (III)", "C → dsp², 0 unpaired (II)",
       "D → d²sp³, 3 unpaired (I)"],
      why_others_wrong="The other codes interchange the two complexes with three unpaired electrons, or the inner "
                       "and outer orbital octahedral complexes.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory and magnetic properties", seconds=75),

    Q(T_CC, "Werner's theory and ligands", "Advanced", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("[Ni(CO)₄] is a neutral coordination entity.", True),
           ("In K₃[Al(C₂O₄)₃], the coordination number of aluminium is 6.", True),
           ("The EDTA⁴⁻ ion binds a metal ion through two nitrogen atoms and four oxygen atoms.", True),
           ("In [Co(en)₃]³⁺, the coordination number of cobalt is 3.", False),
           ("The oxidation state of iron in [Fe(CO)₅] is +2.", False)],
          [["a", "b"], ["a", "c", "d"], ["b", "c", "e"]], "C"),
      "Charge, denticity, coordination number and oxidation state",
      "[Ni(CO)₄] has Ni(0) and neutral CO ligands, so it is neutral. Three didentate oxalate ions give Al six donor "
      "atoms. EDTA⁴⁻ is hexadentate: two amine nitrogen atoms and four carboxylate oxygen atoms. Three didentate en "
      "ligands give cobalt a coordination number of 6, not 3. CO is neutral and [Fe(CO)₅] is uncharged, so iron is "
      "in the zero oxidation state.",
      ["(a) true", "(b) 3 × 2 = 6 → true", "(c) 2 N + 4 O → true", "(d) 3 × 2 = 6, not 3 → false",
       "(e) Fe(0) → false"],
      why_others_wrong="The other options include (d) or (e), or leave out (c).",
      ncert=f"{NC12}, 'Coordination Compounds', definitions (denticity, coordination number, oxidation number)",
      seconds=60),

    Q(T_CC, "Crystal field theory", "Advanced", "assertion_reason",
      *ar("[Fe(C₂O₄)₃]³⁻ is a low-spin complex with only one unpaired electron.", False,
          "The oxalate ion is a weak-field ligand, so for Fe³⁺ in this complex Δo is smaller than the pairing "
          "energy P.", True),
      "High-spin and low-spin complexes of a d⁵ ion",
      "Oxalate lies below water in the spectrochemical series, so it produces a small Δo. For Fe³⁺ (3d⁵), Δo < P "
      "means the electrons occupy t₂g and eg singly (t₂g³ eg²): the complex is high spin with five unpaired "
      "electrons. A is false and R is true.",
      ["Fe³⁺: 3d⁵", "Weak-field oxalate → Δo < P → t₂g³ eg²", "Five unpaired electrons → high spin → A false",
       "R true"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=50),
]

# ================================================================ Purification and Characterisation (1662-1665)
# 1663: TLC, solvent front 12.0 cm, Rf 0.65 and 0.40
d_a, d_b = F(65, 100) * 12, F(40, 100) * 12
assert (d_a, d_b) == (F(78, 10), F(48, 10))
v_1663 = g(d_a - d_b, 1, " cm")
assert v_1663 == "3.0 cm" and g(d_a + d_b, 1, " cm") == "12.6 cm" and g((d_a + d_b) / 2, 1, " cm") == "6.3 cm"
# 1665: 0.30 g of a compound (M = 60): CO2 0.22 g, H2O 0.18 g, NH3 neutralises 50.0 mL of 0.10 M H2SO4
n_c = F(22, 100) / 44
n_h = 2 * F(18, 100) / 18
n_n = 2 * F(50, 1000) * F(1, 10)
m_o = F(3, 10) - n_c * 12 - n_h * 1 - n_n * 14
n_o = m_o / 16
ratio_1665 = tuple(int(x / n_c) for x in (n_c, n_h, n_n, n_o))
assert ratio_1665 == (1, 4, 2, 1) and 12 + 4 + 28 + 16 == 60
v_1665 = "CH₄N₂O"
assert (n_n / 2) / n_c == 1   # one N per C if the 2 : 1 NH3 : H2SO4 ratio is missed -> CH4NO
assert (n_h / 2) / n_c == 2   # H not doubled -> CH2N2O

QUESTIONS += [
    Q(T_PU, "Quantitative analysis and formulae", "Basic", "direct",
      "In Dumas' method for estimating nitrogen, the gaseous products are passed over a heated copper gauze, and the "
      "nitrogen gas is then collected over:",
      ["water", "an aqueous solution of potassium hydroxide", "concentrated sulphuric acid",
       "anhydrous calcium chloride"], "B",
      "Dumas' method for nitrogen",
      "The compound is heated with copper(II) oxide in an atmosphere of CO₂, giving CO₂, H₂O and nitrogen (with some "
      "oxides of nitrogen). The hot copper gauze reduces the oxides of nitrogen to N₂. The gas is collected over "
      "aqueous KOH, which absorbs the carbon dioxide, so only nitrogen is measured.",
      ["CuO oxidises C and H to CO₂ and H₂O", "Cu gauze: oxides of N → N₂", "KOH(aq) absorbs CO₂ → pure N₂ collected"],
      why_others_wrong="Water would not remove CO₂; conc. H₂SO₄ and anhydrous CaCl₂ absorb water vapour, not CO₂.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of nitrogen "
            f"(Dumas method)", seconds=25),

    N(T_PU, "Purification methods", "Intermediate",
      "In a thin layer chromatography experiment, the solvent front rises 12.0 cm from the base line. Two "
      "components A and B of a mixture have Rf values of 0.65 and 0.40. The distance between the centres of the two "
      "spots on the plate is:",
      ["0.25 cm", "3.0 cm", "6.3 cm", "12.6 cm"], "B", v_1663,
      "Retardation factor in TLC",
      "Rf = distance moved by the substance / distance moved by the solvent, both from the base line. So each spot "
      "lies at Rf × 12.0 cm from the base line.",
      ["A: 0.65 × 12.0 = 7.8 cm", "B: 0.40 × 12.0 = 4.8 cm", "Separation = 7.8 − 4.8 = 3.0 cm"],
      why_others_wrong="0.25 cm takes the difference of the Rf values as a distance; 12.6 cm adds the two distances; "
                       "6.3 cm averages them.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', chromatography (TLC, Rf)",
      seconds=40),

    Q(T_PU, "Quantitative analysis and formulae", "Intermediate", "assertion_reason",
      *ar("The nitrogen of nitrobenzene cannot be estimated by Kjeldahl's method.", True,
          "During digestion in Kjeldahl's method, the nitrogen of nitro compounds is converted into sodium cyanide.",
          False),
      "Limitations of Kjeldahl's method",
      "Kjeldahl's method works only when the nitrogen of the compound is converted into ammonium sulphate on heating "
      "with concentrated H₂SO₄. NCERT notes that the nitrogen of nitro and azo groups and of ring nitrogen (as in "
      "pyridine) does not change to ammonium sulphate, so A is true. No sodium is used in this digestion; conversion "
      "into sodium cyanide happens in sodium fusion (Lassaigne's test), so R is false.",
      ["Nitro N is not converted into (NH₄)₂SO₄ → A true",
       "NaCN forms in Lassaigne's test, not in Kjeldahl digestion → R false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', Kjeldahl's method", seconds=40),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "0.30 g of an organic compound containing C, H, N and O gave 0.22 g of CO₂ and 0.18 g of H₂O on complete "
      "combustion. In a Kjeldahl estimation, the ammonia obtained from another 0.30 g of the compound exactly "
      "neutralised 50.0 mL of 0.10 M H₂SO₄. The molar mass of the compound is 60 g mol⁻¹. Its molecular formula is "
      "(C = 12, H = 1, N = 14, O = 16):",
      ["CH₄NO", "CH₂N₂O", "CH₄N₂O", "C₂H₈N₄O₂"], "C", v_1665,
      "Molecular formula from combustion and Kjeldahl data",
      "Moles of C come from CO₂, moles of H from twice the moles of H₂O, and moles of N from twice the moles of "
      "H₂SO₄ (2NH₃ + H₂SO₄ → (NH₄)₂SO₄). Oxygen is found by difference.",
      ["n(C) = 0.22/44 = 0.005 mol (0.06 g)", "n(H) = 2 × 0.18/18 = 0.02 mol (0.02 g)",
       "n(N) = 2 × 0.050 × 0.10 = 0.01 mol (0.14 g)", "m(O) = 0.30 − 0.06 − 0.02 − 0.14 = 0.08 g → 0.005 mol",
       "C : H : N : O = 1 : 4 : 2 : 1 → CH₄N₂O (M = 60) → molecular formula CH₄N₂O (urea)"],
      why_others_wrong="CH₄NO forgets that one H₂SO₄ takes two NH₃; CH₂N₂O takes the moles of H equal to the moles of "
                       "water; C₂H₈N₄O₂ doubles the formula, ignoring the molar mass of 60.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis",
      seconds=120),
]

# ================================================================ Some Basic Principles of Organic Chemistry (1666-1682)
# 1668: classes of the listed compounds
classes_1668 = {"CH3COCH3": "ketone", "CH3CHO": "aldehyde", "CH3COOCH3": "ester", "C6H5COCH3": "ketone",
                "CH3CONH2": "amide", "cyclohexanone": "ketone", "CH3COOH": "carboxylic acid"}
v_1668 = str(sum(1 for c in classes_1668.values() if c == "ketone"))
assert v_1668 == "3"
# 1672: reaction types
types_1672 = ["addition", "substitution", "addition", "elimination", "substitution", "addition"]
v_1672 = str(types_1672.count("addition"))
assert v_1672 == "3"
# 1680: is -OH the principal group?  (seniority: COOH > CN > CHO > C=O > OH > NH2 > C=C)
seniority = ["COOH", "CN", "CHO", "CO", "OH", "NH2", "C=C"]
others_1680 = ["COOH", "CHO", "NH2", "C=C", "CN", "CO"]
v_1680 = str(sum(1 for grp in others_1680 if seniority.index(grp) < seniority.index("OH")))
assert v_1680 == "4"

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of CH₂=CH–C≡CH is:",
      ["But-3-en-1-yne", "But-1-en-3-yne", "But-1-yn-3-ene", "Buta-1,3-dienyne"], "B",
      "Numbering a chain containing both a double and a triple bond",
      "Numbering from either end gives the multiple bonds the locants 1 and 3. When there is such a tie, the double "
      "bond is given the lower number. The name ends in -yne, with -en- placed before it: but-1-en-3-yne.",
      ["Lowest locants: {1, 3} from either end → tie", "Tie → double bond gets the lower locant (1)",
       "Name: but-1-en-3-yne"],
      why_others_wrong="But-3-en-1-yne gives the triple bond the lower number in a tie; 'yn-ene' reverses the order of "
                       "the endings; 'dienyne' wrongly implies two double bonds.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature "
            f"(compounds with multiple bonds)", seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Basic", "match_list",
      *ml("Match the common name of the alkyl group in List-I with its structure in List-II.",
          ["Isopropyl", "sec-Butyl", "Isobutyl", "tert-Butyl"],
          ["(CH₃)₃C–", "(CH₃)₂CH–CH₂–", "(CH₃)₂CH–", "CH₃–CH₂–CH(CH₃)–"],
          "III IV II I", ["III II IV I", "II IV III I", "III IV I II"], "C"),
      "Common names of branched alkyl groups",
      "Isopropyl is attached through the middle carbon of propane. sec-Butyl is attached through a secondary carbon "
      "of a straight four-carbon chain. Isobutyl, (CH₃)₂CHCH₂–, is attached through the CH₂ of the branched chain. "
      "tert-Butyl is attached through the tertiary carbon.",
      ["A → (CH₃)₂CH– (III)", "B → CH₃CH₂CH(CH₃)– (IV)", "C → (CH₃)₂CHCH₂– (II)", "D → (CH₃)₃C– (I)"],
      why_others_wrong="The other codes interchange sec-butyl with isobutyl, isopropyl with isobutyl, or isobutyl "
                       "with tert-butyl.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of alkyl groups",
      seconds=35),

    N(T_GO, "Hybridisation and functional groups", "Basic",
      "How many of the following compounds are ketones?\n"
      "CH₃COCH₃, CH₃CHO, CH₃COOCH₃, C₆H₅COCH₃, CH₃CONH₂, cyclohexanone, CH₃COOH",
      ["2", "4", "5", "3"], "D", v_1668,
      "Recognising functional groups",
      "A ketone has the >C=O group bonded to two carbon atoms. In an aldehyde one of the groups is H; in esters, "
      "amides and acids the carbonyl carbon is also bonded to O or N.",
      ["CH₃COCH₃ (propanone): ketone", "CH₃CHO: aldehyde", "CH₃COOCH₃: ester", "C₆H₅COCH₃ (acetophenone): ketone",
       "CH₃CONH₂: amide", "Cyclohexanone: ketone", "CH₃COOH: acid", "Ketones = 3"],
      why_others_wrong="4 or 5 count the ester, amide or acid as ketones because they contain C=O; 2 misses "
                       "acetophenone or the cyclic ketone.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', functional groups", seconds=35),

    Q(T_GO, "IUPAC nomenclature", "Basic", "statement_pair",
      *sp("In IUPAC nomenclature, the prefix 'cyclo' is used for alicyclic compounds, as in cyclohexane.", True,
          "A carbon atom bonded to three other carbon atoms is called a tertiary (3°) carbon atom.", True),
      "Nomenclature of cyclic compounds and classification of carbon atoms",
      "Saturated monocyclic compounds are named by adding 'cyclo' to the name of the corresponding straight-chain "
      "alkane. A carbon atom is called primary, secondary, tertiary or quaternary when it is bonded to one, two, "
      "three or four other carbon atoms. Both statements are true.",
      ["Statement I: cyclohexane, cyclopentane, ... → true", "Statement II: 3 C neighbours → 3° → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of cyclic compounds",
      seconds=25),

    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The group C₆H₅–CH₂– is called:",
      ["Phenyl", "Benzoyl", "Benzyl", "Tolyl"], "C",
      "Names of aryl and arylalkyl groups",
      "C₆H₅– is phenyl. When a CH₂ group links the benzene ring to the rest of the molecule, the group C₆H₅CH₂– is "
      "benzyl (as in the benzyl carbocation, C₆H₅CH₂⁺).",
      ["C₆H₅– = phenyl", "C₆H₅CH₂– = benzyl", "C₆H₅CO– = benzoyl", "CH₃C₆H₄– = tolyl"],
      why_others_wrong="Phenyl lacks the CH₂ group; benzoyl contains C=O; tolyl is a methyl-substituted phenyl group "
                       "attached through the ring.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', reactive intermediates "
            f"(benzyl carbocation)", seconds=20),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "A compound contains an ester group (–COOR), a nitrile group (–CN), an amide group (–CONH₂) and an aldehyde "
      "group (–CHO). In its IUPAC name, the group cited as the suffix (the principal functional group) is:",
      ["–CHO", "–CN", "–CONH₂", "–COOR"], "D",
      "Order of seniority of functional groups",
      "NCERT's order of preference is –COOH, –SO₃H, –COOR, –COCl, –CONH₂, –CN, –HC=O, >C=O, –OH, –NH₂, >C=C<, "
      "–C≡C–. Of the groups present, the ester comes first, so it is the principal group; the others are named as "
      "prefixes.",
      ["Seniority: –COOR > –CONH₂ > –CN > –CHO", "Principal group = ester"],
      why_others_wrong="Amide, nitrile and aldehyde groups all rank below the ester group.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            f"compounds", seconds=30),

    N(T_GO, "Types of organic reactions", "Intermediate",
      "How many of the following are addition reactions?\n"
      "(i) CH₂=CH₂ + Br₂ (in CCl₄) → BrCH₂–CH₂Br\n"
      "(ii) CH₄ + Cl₂ (light) → CH₃Cl + HCl\n"
      "(iii) CH₃CHO + HCN → CH₃CH(OH)CN\n"
      "(iv) CH₃CH₂Br + alcoholic KOH → CH₂=CH₂ + KBr + H₂O\n"
      "(v) C₆H₆ + HNO₃ (conc. H₂SO₄) → C₆H₅NO₂ + H₂O\n"
      "(vi) HC≡CH + HCl → CH₂=CHCl",
      ["2", "3", "4", "1"], "B", v_1672,
      "Classifying organic reactions",
      "In an addition reaction two molecules combine to give a single product, with no atom or group lost; the "
      "multiple bond (C=C, C≡C or C=O) is used up.",
      ["(i) addition to C=C", "(ii) substitution", "(iii) addition to C=O", "(iv) elimination",
       "(v) substitution", "(vi) addition to C≡C", "Addition reactions = 3"],
      why_others_wrong="2 misses the nucleophilic addition to C=O or the addition to C≡C; 4 counts the elimination "
                       "or a substitution as addition.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', types of organic reactions",
      seconds=45),

    Q(T_GO, "Reactive intermediates", "Intermediate", "assertion_reason",
      *ar("Water cannot act as a nucleophile because it is a neutral molecule.", False,
          "Neutral molecules having an unshared pair of electrons, such as H₂O and R₃N, can act as nucleophiles.",
          True),
      "Neutral nucleophiles",
      "A nucleophile is a species that brings an electron pair to an electron-deficient centre. It need not be "
      "negatively charged: NCERT lists neutral molecules with lone pairs, such as H₂O, R₃N: and R₂NH, as "
      "nucleophiles. So A is false and R is true.",
      ["A nucleophile needs an available electron pair, not a charge", "H₂O has two lone pairs on O → nucleophile",
       "A false, R true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "multi_statement",
      *ms("Which of the following IUPAC names are correct?",
          [("CH₃–CH₂–CH₂–CN: butanenitrile", True),
           ("CH₃–CH₂–CONH₂: propanamide", True),
           ("CH₃–COO–CH₃: methyl methanoate", False),
           ("(CH₃)₂CH–COOH: 2-methylpropanoic acid", True),
           ("CH₃–CH₂–COO–CH₃: ethyl ethanoate", False)],
          [["a", "b"], ["b", "c", "d"], ["a", "d", "e"]], "C"),
      "Naming nitriles, amides, esters and acids",
      "In nitriles and amides the carbon of the functional group is counted in the parent chain. An ester R′COOR is "
      "named as alkyl alkanoate, the alkyl group R coming from the alcohol and the alkanoate from the acid.",
      ["(a) four C including CN → butanenitrile → correct", "(b) three C → propanamide → correct",
       "(c) acid part has two C → methyl ethanoate → incorrect", "(d) correct",
       "(e) acid part propanoate, alcohol part methyl → methyl propanoate → incorrect"],
      why_others_wrong="The other options include (c) or (e), or leave out (d).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature of "
            f"functional compounds", seconds=50),

    Q(T_GO, "Types of organic reactions", "Intermediate", "statement_pair",
      *sp("In an organic reaction, the reactant that supplies carbon to the new bond being formed is called the "
          "substrate.", True,
          "In the reaction CH₃Br + OH⁻ → CH₃OH + Br⁻, the hydroxide ion is the substrate.", False),
      "Substrate and reagent",
      "NCERT defines the substrate as the reactant that supplies carbon to the new bond, and the other reactant as "
      "the reagent. In the hydrolysis of CH₃Br, the new C–O bond gets its carbon from CH₃Br, so CH₃Br is the "
      "substrate and OH⁻ is the attacking reagent (a nucleophile).",
      ["Statement I: NCERT definition → true", "Carbon of the new C–O bond comes from CH₃Br → CH₃Br is the substrate",
       "Statement II false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', fundamental concepts in organic "
            f"reaction mechanism", seconds=30),

    Q(T_GO, "Electronic effects", "Intermediate", "assertion_reason",
      *ar("In propenal, CH₂=CH–CHO, the terminal carbon atom (C-3) carries a partial positive charge.", True,
          "The –CHO group withdraws π electrons from the C=C bond by its −R (resonance) effect.", True,
          explains=True),
      "−R effect of a carbonyl group in a conjugated system",
      "In CH₂=CH–CH=O the π electrons of C=C are delocalised towards the electronegative oxygen. One canonical "
      "structure is ⁺CH₂–CH=CH–O⁻, so the terminal carbon becomes electron-deficient. This delocalisation is the −R "
      "effect of the –CHO group, so R explains A.",
      ["Canonical form: ⁺CH₂–CH=CH–O⁻", "C-3 becomes δ+ → A true", "Cause: −R effect of –CHO → R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance effect", seconds=40),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "A benzene ring carries a –CH₃ group, a –Cl group on the carbon next to it, and a –NO₂ group para to the –CH₃ "
      "group. The IUPAC name of the compound is:",
      ["2-Chloro-1-methyl-4-nitrobenzene", "1-Chloro-2-methyl-5-nitrobenzene", "4-Nitro-2-chloro-1-methylbenzene",
       "3-Chloro-4-methyl-1-nitrobenzene"], "A",
      "Naming polysubstituted benzene derivatives",
      "The ring is numbered to give the substituents the lowest set of locants, and the prefixes are written in "
      "alphabetical order. Numbering from the CH₃ carbon towards Cl gives {1, 2, 4}; every other numbering gives a "
      "higher set (e.g. {1, 2, 5} or {1, 3, 4}).",
      ["CH₃ = 1, Cl = 2, NO₂ = 4 → locant set {1, 2, 4} (lowest)",
       "Alphabetical order: chloro, methyl, nitro", "Name: 2-chloro-1-methyl-4-nitrobenzene"],
      why_others_wrong="{1, 2, 5} and {1, 3, 4} are not the lowest locant sets; '4-nitro-2-chloro-1-methyl' does not "
                       "list the prefixes alphabetically.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of substituted benzene "
            f"compounds", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₃–CH(OH)–CH₂–C(CH₃)₂–CHO is:",
      ["2,2-Dimethyl-4-hydroxypentanal", "4-Hydroxy-2,2-dimethylpentanal", "2-Hydroxy-4,4-dimethylpentanal",
       "5-Oxo-4,4-dimethylpentan-2-ol"], "B",
      "Naming a polyfunctional compound",
      "The aldehyde group is senior to –OH, so the suffix is -al and C-1 is the CHO carbon. The chain of five carbons "
      "carries two methyl groups on C-2 and an –OH on C-4. Prefixes are written alphabetically: hydroxy before "
      "dimethyl ('di' is ignored in alphabetising).",
      ["Principal group –CHO → C-1, suffix '-al'", "Parent chain: 5 C → pentanal",
       "Substituents: 2,2-dimethyl; 4-hydroxy", "Alphabetical (h before m) → 4-hydroxy-2,2-dimethylpentanal"],
      why_others_wrong="'2,2-Dimethyl-4-hydroxy' ignores alphabetical order; '2-hydroxy-4,4-dimethyl' numbers from the "
                       "wrong end; the '-ol' name wrongly treats –OH as the principal group.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            f"compounds", seconds=60),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "multi_statement",
      *ms("Which of the following are correct rules of IUPAC nomenclature?",
          [("The prefixes iso- and neo- are treated as part of the fundamental name of an alkyl group when "
            "substituents are arranged alphabetically.", True),
           ("The prefixes sec- and tert- are taken into account when substituents are arranged alphabetically.",
            False),
           ("If two chains of equal length are possible, the chain with the greater number of side chains is "
            "chosen as the parent chain.", True),
           ("The chain is numbered so that the substituents get the highest possible locants.", False)],
          [["a", "b"], ["a", "c", "d"], ["b", "c"]], "D"),
      "Finer rules of IUPAC nomenclature",
      "NCERT states that iso- and neo- are part of the fundamental name of the alkyl group (isopropyl is "
      "alphabetised under 'i'), whereas sec- and tert- are not (tert-butyl is alphabetised under 'b'). When two "
      "chains are of equal size, the one with more side chains is selected. Numbering always aims at the lowest "
      "locants.",
      ["(a) true", "(b) sec-/tert- are ignored → false", "(c) true", "(d) lowest locants → false"],
      why_others_wrong="Options containing (b) or (d) are wrong.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC rules for branched alkanes",
      seconds=50),

    Q(T_GO, "Electronic effects", "Advanced", "match_list",
      *ml("Match the group attached to a benzene ring in List-I with its electronic effects in List-II.",
          ["–NH₂", "–Cl", "–NO₂", "–CH₃"],
          ["−I and +R, the +R effect being dominant", "−I and +R, the −I effect being dominant",
           "−I and −R", "+I and hyperconjugation"],
          "I II III IV", ["II I III IV", "I III II IV", "I II IV III"], "A"),
      "Inductive and resonance effects of substituents",
      "–NH₂ is more electronegative than carbon (−I) but its lone pair is delocalised into the ring (+R), and the "
      "+R effect dominates, so it activates the ring. A halogen also shows −I and +R, but here −I dominates, so the "
      "ring is deactivated. –NO₂ withdraws electrons both inductively and by resonance. –CH₃ releases electrons by "
      "the +I effect and hyperconjugation.",
      ["–NH₂ → I", "–Cl → II", "–NO₂ → III", "–CH₃ → IV"],
      why_others_wrong="The other codes interchange –NH₂ and –Cl (which differ in which effect dominates), –Cl and "
                       "–NO₂, or –NO₂ and –CH₃.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', inductive and resonance effects",
      seconds=50),

    N(T_GO, "IUPAC nomenclature", "Advanced",
      "In how many of the following compounds is the –OH group NOT the principal functional group (i.e. it is cited "
      "as the prefix 'hydroxy')?\n"
      "HO–CH₂–CH₂–COOH, HO–CH₂–CHO, HO–CH₂–CH₂–NH₂, HO–CH₂–CH=CH₂, HO–CH₂–CH₂–CN, HO–CH₂–CO–CH₃",
      ["4", "3", "5", "2"], "A", v_1680,
      "Seniority of –OH among functional groups",
      "–OH ranks below –COOH, –CN, –CHO and >C=O, but above –NH₂ and the C=C bond. So –OH is a prefix (hydroxy) only "
      "when one of the higher groups is present.",
      ["HOCH₂CH₂COOH: 3-hydroxypropanoic acid → prefix", "HOCH₂CHO: hydroxyethanal → prefix",
       "HOCH₂CH₂NH₂: 2-aminoethan-1-ol → –OH principal", "HOCH₂CH=CH₂: prop-2-en-1-ol → –OH principal",
       "HOCH₂CH₂CN: 3-hydroxypropanenitrile → prefix", "HOCH₂COCH₃: 1-hydroxypropan-2-one → prefix", "Count = 4"],
      why_others_wrong="5 wrongly ranks –NH₂ above –OH; 3 misses the nitrile or ketone; 2 ranks –OH above >C=O and "
                       "–CN.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            f"compounds", seconds=60),

    Q(T_GO, "Reactive intermediates", "Advanced", "match_list",
      *ml("Match the carbocation in List-I with the main factor that stabilises its positive charge in List-II.",
          ["CH₂=CH–CH₂⁺", "C₆H₅–CH₂⁺", "(CH₃)₃C⁺", "CH₃–CH₂⁺"],
          ["Delocalisation of the charge over the benzene ring", "Delocalisation of the charge through an adjacent "
           "C=C bond", "Hyperconjugation involving nine C–H bonds", "Hyperconjugation involving three C–H bonds"],
          "II I III IV", ["I II III IV", "II I IV III", "II III I IV"], "C"),
      "Stabilisation of carbocations by resonance and hyperconjugation",
      "The allyl and benzyl carbocations are stabilised by resonance: the vacant p orbital overlaps with the π "
      "system of the adjacent C=C bond or of the benzene ring. In (CH₃)₃C⁺ three methyl groups provide nine C–H bonds "
      "for hyperconjugation; in CH₃CH₂⁺ one methyl group provides three.",
      ["Allyl → C=C conjugation (II)", "Benzyl → ring delocalisation (I)", "tert-Butyl → 9 C–H (III)",
       "Ethyl → 3 C–H (IV)"],
      why_others_wrong="The other codes interchange the allyl and benzyl cations or the numbers of C–H bonds.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', carbocations and hyperconjugation",
      seconds=45),
]

# ================================================================ Hydrocarbons (1683-1696)
# 1685: CH3CH2COONa + NaOH (CaO) -> C2H6 + Na2CO3 ; 2.24 L ethane at STP
m_prop_na = mm(C=3, H=5, O=2, Na=1)
m_eth_na = mm(C=2, H=3, O=2, Na=1)
assert (m_prop_na, m_eth_na) == (96, 82)
n_1685 = F(224, 100) / F(224, 10)
v_1685 = g(n_1685 * m_prop_na, 1)
assert v_1685 == "9.6 g" and g(n_1685 * m_eth_na, 1) == "8.2 g" and g(2 * n_1685 * m_prop_na, 1) == "19.2 g"
assert g(n_1685 / 2 * m_prop_na, 1) == "4.8 g"
# 1686: CH2=CH2 + [O] + H2O (cold dilute alkaline KMnO4) -> HOCH2CH2OH ; 5.6 g ethene
n_1686 = F(56, 10) / mm(C=2, H=4)
assert n_1686 == F(1, 5) and mm(C=2, H=6, O=2) == 62
v_1686 = g(n_1686 * 62, 1)
assert v_1686 == "12.4 g" and g(n_1686 * 31, 1) == "6.2 g" and g(n_1686 * mm(C=2, H=6, O=1), 1) == "9.2 g"
assert g(2 * n_1686 * 62, 1) == "24.8 g"
# 1690: HC≡CH + H2O (Hg2+, H2SO4) -> CH3CHO ; 5.2 g ethyne
n_1690 = F(52, 10) / mm(C=2, H=2)
assert n_1690 == F(1, 5)
v_1690 = g(n_1690 * mm(C=2, H=4, O=1), 1)
assert v_1690 == "8.8 g" and g(n_1690 * 46, 1) == "9.2 g" and g(n_1690 * 60, 1) == "12.0 g" and g(n_1690 * 22, 1) == "4.4 g"
# 1691: C6H6 + 3Cl2 (UV) -> C6H6Cl6 ; 7.8 g benzene
m_bhc = mm(C=6, H=6, Cl=6)
assert m_bhc == 291 and mm(C=6, H=5, Cl=1) == F(2250, 20) and mm(C=6, H=6, Cl=4) == 220
n_1691 = F(78, 10) / 78
v_1691 = g(n_1691 * m_bhc, 2)
assert v_1691 == "29.10 g" and g(n_1691 * mm(C=6, H=5, Cl=1), 2) == "11.25 g"
assert g(n_1691 * m_bhc / 2, 2) == "14.55 g" and g(n_1691 * 220, 2) == "22.00 g"
# 1692: naphthalene: 5 C=C in a Kekule structure -> 10 pi electrons ; 4n + 2 = 10 -> n = 2
pi_1692 = 5 * 2
n_huckel = (pi_1692 - 2) // 4
assert (pi_1692, n_huckel) == (10, 2) and 4 * n_huckel + 2 == pi_1692
v_1692 = "10 and 2"
# 1696: C6H14 -> C6H6 + 4H2 ; 8.6 g n-hexane, 80% yield
n_hex = F(86, 10) / mm(C=6, H=14)
assert n_hex == F(1, 10)
v_1696 = g(n_hex * F(8, 10) * 4 * F(224, 10), 2, " L")
assert v_1696 == "7.17 L" and g(n_hex * 4 * F(224, 10), 2, " L") == "8.96 L"
assert g(n_hex * F(8, 10) * 3 * F(224, 10), 2, " L") == "5.38 L" and g(n_hex * F(8, 10) * F(224, 10), 2, " L") == "1.79 L"

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "Rotation about the C–C single bond of ethane gives an infinite number of spatial arrangements. Those "
      "arrangements other than the staggered and the eclipsed forms are called:",
      ["Eclipsed conformations", "Staggered conformations", "Geometrical isomers", "Skew conformations"], "D",
      "Conformations of ethane",
      "The staggered and eclipsed forms are the two extreme conformations of ethane. NCERT calls all the other, "
      "intermediate conformations skew conformations.",
      ["Extreme forms: staggered and eclipsed", "All intermediate forms: skew"],
      why_others_wrong="Staggered and eclipsed are the two extreme conformations themselves; conformations are not "
                       "geometrical isomers, which arise from restricted rotation about a double bond.",
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane", seconds=20),

    Q(T_HC, "Alkanes and conformations", "Basic", "statement_pair",
      *sp("Methane cannot be prepared by Kolbe's electrolytic method.", True,
          "Like alkenes, alkynes such as but-2-yne show geometrical (cis–trans) isomerism about the triple bond.",
          False),
      "Kolbe's method and the geometry of alkynes",
      "In Kolbe's electrolysis two alkyl radicals R• from RCOO⁻ couple to give R–R, so the product always has an even "
      "number of carbon atoms (at least two); methane cannot be obtained. The C≡C unit and the two atoms attached to "
      "it are linear, so there is only one way to arrange the substituents and no cis–trans isomerism.",
      ["Kolbe: 2RCOO⁻ → R–R (+ 2CO₂) → smallest product ethane → Statement I true",
       "Alkyne: linear C–C≡C–C → no cis/trans forms → Statement II false"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes (Kolbe's electrolytic method); structure of triple bond",
      seconds=35),

    N(T_HC, "Alkanes and conformations", "Basic",
      "Ethane is prepared by heating sodium propanoate with soda lime:\n"
      "CH₃CH₂COONa + NaOH → CH₃–CH₃ + Na₂CO₃ (CaO)\n"
      "The minimum mass of sodium propanoate needed to obtain 2.24 L of ethane, measured at STP, is "
      "(C = 12, H = 1, O = 16, Na = 23; molar volume at STP = 22.4 L mol⁻¹):",
      ["8.2 g", "19.2 g", "4.8 g", "9.6 g"], "D", v_1685,
      "Decarboxylation of sodium salts of carboxylic acids",
      "The sodium salt loses CO₂ (as Na₂CO₃) and gives an alkane with one carbon atom fewer. One mole of sodium "
      "propanoate gives one mole of ethane.",
      ["n(C₂H₆) = 2.24/22.4 = 0.10 mol", "n(CH₃CH₂COONa) = 0.10 mol",
       "M = 3(12) + 5(1) + 2(16) + 23 = 96 g mol⁻¹", "Mass = 0.10 × 96 = 9.6 g"],
      why_others_wrong="8.2 g uses sodium ethanoate (which gives methane, not ethane); 19.2 g assumes two moles of "
                       "salt per mole of ethane, as in Kolbe's electrolysis; 4.8 g halves the amount.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes (decarboxylation)", seconds=40),

    N(T_HC, "Alkenes: addition and ozonolysis", "Basic",
      "Ethene is passed into cold, dilute, aqueous alkaline potassium permanganate (Baeyer's reagent), which converts "
      "it into ethane-1,2-diol. The mass of the diol formed from 5.6 g of ethene, assuming complete conversion, is "
      "(C = 12, H = 1, O = 16):",
      ["6.2 g", "12.4 g", "9.2 g", "24.8 g"], "B", v_1686,
      "Oxidation of alkenes by Baeyer's reagent",
      "Each C=C unit adds two –OH groups: CH₂=CH₂ → HOCH₂–CH₂OH. One mole of ethene gives one mole of the diol "
      "(M = 62 g mol⁻¹).",
      ["n(C₂H₄) = 5.6/28 = 0.20 mol", "n(diol) = 0.20 mol", "Mass = 0.20 × 62 = 12.4 g"],
      why_others_wrong="6.2 g halves the amount; 9.2 g is the mass of ethanol (a single –OH), not the diol; 24.8 g "
                       "doubles the amount.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkenes (oxidation with Baeyer's reagent)", seconds=35),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "assertion_reason",
      *ar("Addition of HI to propene gives 2-iodopropane as the main product even in the presence of a peroxide.",
          True,
          "Iodine free radicals formed under these conditions combine with one another to give iodine molecules "
          "instead of adding to the double bond.", True, explains=True),
      "Why the peroxide effect is shown by HBr but not by HI",
      "The anti-Markovnikov (peroxide) effect needs halogen free radicals to add to the alkene. With HI the H–I bond "
      "(296.8 kJ mol⁻¹) is weak, but the iodine atoms formed combine to give I₂ rather than adding to C=C, so the "
      "ionic Markovnikov addition continues and gives 2-iodopropane. R is the reason for A.",
      ["Peroxide → radicals; with HI, I• + I• → I₂", "No radical chain addition → Markovnikov product",
       "R explains A"],
      ncert=f"{NC11}, 'Hydrocarbons', addition of hydrogen halides to alkenes (peroxide effect)", seconds=45),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "direct",
      "Which of the following alkyl halides undergoes dehydrohalogenation fastest when heated with alcoholic KOH?",
      ["(CH₃)₃C–Cl", "(CH₃)₃C–I", "CH₃CH₂CH₂CH₂–I", "CH₃CH₂CH₂CH₂–Cl"], "B",
      "Rate of dehydrohalogenation",
      "NCERT states that the rate of dehydrohalogenation depends on both the halogen (iodine > bromine > chlorine) "
      "and the alkyl group (tertiary > secondary > primary). A tertiary iodide combines the best of both.",
      ["Halogen: I > Br > Cl", "Alkyl group: 3° > 2° > 1°", "Fastest: (CH₃)₃C–I"],
      why_others_wrong="(CH₃)₃CCl has the less reactive halogen; 1-iodobutane and 1-chlorobutane are primary.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes (dehydrohalogenation)", seconds=30),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with the type of reaction in List-II.",
          ["n-Hexane heated at 773 K and 10–20 atm over Cr₂O₃ on alumina → benzene",
           "CH₂=CH₂ + H₂O (a few drops of conc. H₂SO₄) → CH₃CH₂OH",
           "(CH₃)₃C–Br + alcoholic KOH → (CH₃)₂C=CH₂",
           "Ethyne passed through a red-hot iron tube at 873 K → benzene"],
          ["β-Elimination", "Cyclic polymerisation", "Aromatisation", "Addition"],
          "III IV I II", ["II IV I III", "III I IV II", "IV III I II"], "B"),
      "Types of reactions of hydrocarbons",
      "Alkanes with six or more carbon atoms are converted into benzene and its homologues over Cr₂O₃/V₂O₅/Mo₂O₃ "
      "(aromatisation). Alkenes add water in the presence of acid (Markovnikov addition). Alkyl halides lose HX from "
      "adjacent carbons with alcoholic KOH (β-elimination). Three ethyne molecules combine at 873 K over red-hot iron "
      "to form benzene (cyclic polymerisation).",
      ["A → aromatisation (III)", "B → addition (IV)", "C → β-elimination (I)", "D → cyclic polymerisation (II)"],
      why_others_wrong="Both A and D give benzene, but A starts from an alkane (aromatisation) and D joins three ethyne "
                       "molecules (polymerisation); the other codes also confuse addition with elimination.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkanes, alkenes and alkynes", seconds=50),

    N(T_HC, "Alkynes", "Intermediate",
      "Ethyne is hydrated by passing it into dilute sulphuric acid containing mercuric sulphate at 333 K. The mass "
      "of the carbonyl compound formed from 5.2 g of ethyne, assuming complete conversion, is "
      "(C = 12, H = 1, O = 16):",
      ["9.2 g", "4.4 g", "12.0 g", "8.8 g"], "D", v_1690,
      "Hydration of alkynes",
      "Water adds across the triple bond to give an unstable enol, CH₂=CHOH, which changes into ethanal, CH₃CHO "
      "(M = 44 g mol⁻¹). One mole of ethyne gives one mole of ethanal.",
      ["n(C₂H₂) = 5.2/26 = 0.20 mol", "Product: CH₃CHO (via the enol)", "Mass = 0.20 × 44 = 8.8 g"],
      why_others_wrong="9.2 g is for ethanol and 12.0 g for ethanoic acid, neither of which is formed; 4.4 g halves "
                       "the amount.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkynes (addition of water)", seconds=40),

    N(T_HC, "Benzene and aromaticity", "Intermediate",
      "In the presence of ultraviolet light, benzene adds chlorine to give benzene hexachloride, C₆H₆Cl₆. The mass of "
      "benzene hexachloride formed from 7.8 g of benzene, assuming complete reaction, is (C = 12, H = 1, Cl = 35.5):",
      ["11.25 g", "29.10 g", "14.55 g", "22.00 g"], "B", v_1691,
      "Addition reactions of benzene",
      "Under UV light and heat benzene undergoes addition rather than substitution: C₆H₆ + 3Cl₂ → C₆H₆Cl₆ "
      "(M = 72 + 6 + 213 = 291 g mol⁻¹).",
      ["n(C₆H₆) = 7.8/78 = 0.10 mol", "n(C₆H₆Cl₆) = 0.10 mol", "Mass = 0.10 × 291 = 29.10 g"],
      why_others_wrong="11.25 g is the mass of chlorobenzene, the substitution product formed in the dark with a "
                       "Lewis acid; 22.00 g adds only two Cl₂; 14.55 g halves the answer.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of benzene (addition reactions)", seconds=40),

    N(T_HC, "Benzene and aromaticity", "Intermediate",
      "Naphthalene, C₁₀H₈, is a planar molecule made of two fused benzene rings, with every ring carbon atom sp² "
      "hybridised and π electrons delocalised over both rings. The number of π electrons in naphthalene and the value "
      "of n for which it satisfies Hückel's (4n + 2) rule are, respectively:",
      ["10 and 2", "8 and 2", "10 and 3", "12 and 3"], "A", v_1692,
      "Hückel's rule",
      "A Kekulé-type structure of naphthalene has five C=C bonds, i.e. 10 π electrons. Setting 4n + 2 = 10 gives "
      "n = 2, so naphthalene satisfies the (4n + 2) π-electron condition for aromaticity.",
      ["π electrons = 5 × 2 = 10", "4n + 2 = 10 → n = 2"],
      why_others_wrong="12 π electrons would need six double bonds; 8 is the count for a 4n system; n = 3 corresponds "
                       "to 14 π electrons.",
      ncert=f"{NC11}, 'Hydrocarbons', aromaticity (Hückel rule)", seconds=35),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "direct",
      "Cyclohexene is treated with ozone and the ozonide formed is decomposed with zinc dust and water. The product "
      "is:",
      ["Cyclohexanone", "Two molecules of propanal", "Hexanedioic acid", "Hexane-1,6-dial, OHC–(CH₂)₄–CHO"], "D",
      "Ozonolysis of a cyclic alkene",
      "Ozonolysis cleaves the C=C bond and turns each doubly bonded carbon into a C=O group. In a ring, both new "
      "carbonyl groups stay in the same molecule, so the ring opens into a single six-carbon chain with an aldehyde "
      "group at each end. Zn/H₂O prevents further oxidation to acids.",
      ["C=C cleaved; each =CH– becomes –CHO", "Ring opens: one product, not two",
       "Product: OHC–CH₂–CH₂–CH₂–CH₂–CHO (hexane-1,6-dial)"],
      why_others_wrong="Cyclohexanone would keep the ring; two propanal molecules would need two separate fragments; "
                       "hexanedioic acid requires oxidative work-up, not zinc and water.",
      ncert=f"{NC11}, 'Hydrocarbons', ozonolysis of alkenes", seconds=50),

    Q(T_HC, "Alkynes", "Advanced", "direct",
      "Calcium carbide reacts with water to give X. X is hydrogenated with H₂ over palladium on charcoal partly "
      "deactivated with quinoline, giving Y. Y adds HBr to give Z, and Z is heated with sodium in dry ether to give W. "
      "W is:",
      ["Ethane", "Butane", "But-2-ene", "Hexane"], "B",
      "Sequence of reactions of ethyne",
      "CaC₂ + 2H₂O → HC≡CH (X). Lindlar's catalyst stops hydrogenation at the alkene: CH₂=CH₂ (Y). HBr adds to give "
      "CH₃CH₂Br (Z). The Wurtz reaction joins two ethyl groups: CH₃CH₂–CH₂CH₃, butane (W).",
      ["X = ethyne", "Y = ethene (partial hydrogenation)", "Z = bromoethane", "W = butane (Wurtz coupling)"],
      why_others_wrong="Ethane would need complete hydrogenation and no coupling; but-2-ene is not formed in a Wurtz "
                       "reaction; hexane would need a three-carbon halide.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation and properties of alkynes, alkenes and alkanes", seconds=60),

    Q(T_HC, "Alkynes", "Advanced", "statement_pair",
      *sp("Hydrogenation of ethyne over Lindlar's catalyst (palladised charcoal deactivated with quinoline) gives "
          "ethane.", False,
          "Cyclohexene decolourises a solution of bromine in CCl₄, but benzene does not under the same conditions.",
          True),
      "Partial hydrogenation of alkynes; addition reactions of alkenes versus benzene",
      "The partly poisoned palladium catalyst stops hydrogenation of an alkyne at the alkene stage, so ethyne gives "
      "ethene, not ethane (Statement I false). Cyclohexene has a localised C=C bond and adds bromine readily, whereas "
      "benzene, stabilised by delocalisation of its π electrons, does not add bromine in CCl₄ (Statement II true).",
      ["Lindlar's catalyst → alkene only → Statement I false",
       "Alkene adds Br₂; aromatic benzene resists addition → Statement II true"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from alkynes; properties of benzene", seconds=40),

    N(T_HC, "Alkanes and conformations", "Advanced",
      "n-Hexane is heated at 773 K under 10–20 atm over Cr₂O₃ supported on alumina and is converted into benzene:\n"
      "C₆H₁₄ → C₆H₆ + 4H₂\n"
      "If 8.6 g of n-hexane is used and the yield of benzene is 80%, the volume of hydrogen released, measured at "
      "STP, is (C = 12, H = 1; molar volume at STP = 22.4 L mol⁻¹):",
      ["7.17 L", "8.96 L", "5.38 L", "1.79 L"], "A", v_1696,
      "Aromatisation of alkanes",
      "Each mole of n-hexane converted into benzene releases four moles of hydrogen. Only 80% of the hexane is "
      "converted.",
      ["n(C₆H₁₄) = 8.6/86 = 0.10 mol", "Converted = 0.80 × 0.10 = 0.080 mol", "n(H₂) = 4 × 0.080 = 0.32 mol",
       "V = 0.32 × 22.4 = 7.17 L"],
      why_others_wrong="8.96 L ignores the 80% yield; 5.38 L releases three H₂ per hexane; 1.79 L releases one.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkanes (aromatisation)", seconds=60),
]

# ================================================================ Organic Compounds Containing Halogens (1697-1706)
# 1697: halogen on an sp2 carbon (vinylic or aryl)
sp2_1697 = {"CH2=CHCl": True, "C6H5Cl": True, "C6H5CH2Cl": False, "CH2=CHCH2Cl": False, "CH3CH=CHBr": True,
            "(CH3)3CCl": False, "4-ClC6H4CH3": True}
v_1697 = str(sum(sp2_1697.values()))
assert v_1697 == "4"
# 1700: C2H5Br + CH3COOAg -> CH3COOC2H5 + AgBr ; 10.9 g bromoethane
n_1700 = F(109, 10) / mm(C=2, H=5, Br=1)
assert n_1700 == F(1, 10)
v_1700 = g(n_1700 * mm(C=4, H=8, O=2), 1)
assert v_1700 == "8.8 g" and g(n_1700 * 46, 1) == "4.6 g" and g(n_1700 * mm(C=2, H=3, O=2, Ag=1), 1) == "16.7 g"
assert g(n_1700 * mm(C=4, H=10, O=1), 1) == "7.4 g"
# 1704: C6H5Cl (112.5) nitrated; 60% of the product is the para isomer C6H4ClNO2 (157.5)
m_cnb = mm(C=6, H=4, Cl=1, N=1, O=2)
assert m_cnb == F(315, 2)
n_1704 = F(1125, 100) / mm(C=6, H=5, Cl=1)
assert n_1704 == F(1, 10)
v_1704 = g(n_1704 * F(6, 10) * m_cnb, 2)
assert v_1704 == "9.45 g" and g(n_1704 * m_cnb, 2) == "15.75 g" and g(n_1704 * F(4, 10) * m_cnb, 2) == "6.30 g"
assert g(n_1704 * F(6, 10) * mm(C=6, H=5, Cl=1), 2) == "6.75 g"

QUESTIONS += [
    N(T_HX, "C-X bond and preparation", "Basic",
      "In how many of the following compounds is the halogen atom bonded to an sp²-hybridised carbon atom?\n"
      "CH₂=CHCl, C₆H₅Cl, C₆H₅CH₂Cl, CH₂=CH–CH₂Cl, CH₃–CH=CH–Br, (CH₃)₃C–Cl, 4-chlorotoluene (Cl on the ring)",
      ["3", "5", "2", "4"], "D", v_1697,
      "Classification of halogen compounds by the hybridisation of the C–X carbon",
      "Vinylic halides (X on a C=C carbon) and aryl halides (X on a ring carbon) have the halogen on an sp² carbon. "
      "In allylic and benzylic halides the halogen is on an sp³ carbon next to the C=C or the ring.",
      ["CH₂=CHCl: vinylic → sp²", "C₆H₅Cl: aryl → sp²", "C₆H₅CH₂Cl: benzylic → sp³", "CH₂=CHCH₂Cl: allylic → sp³",
       "CH₃CH=CHBr: vinylic → sp²", "(CH₃)₃CCl: sp³", "4-Chlorotoluene: aryl → sp²", "Count = 4"],
      why_others_wrong="5 wrongly counts the benzylic or allylic chloride (the CH₂ bearing Cl is sp³); 2 or 3 miss "
                       "4-chlorotoluene or 1-bromoprop-1-ene.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification (compounds containing sp³ and sp² C–X bonds)",
      seconds=45),

    Q(T_HX, "Polyhalogen compounds", "Basic", "direct",
      "The first chlorinated organic insecticide, originally prepared in 1873, whose effectiveness as an insecticide "
      "was discovered only in 1939, is:",
      ["Freon-12", "DDT", "Chloroform", "Iodoform"], "B",
      "Polyhalogen compounds: DDT",
      "NCERT describes DDT (p,p′-dichlorodiphenyltrichloroethane) as the first chlorinated organic insecticide. It "
      "was prepared in 1873, but its insecticidal action was discovered by Paul Müller in 1939.",
      ["First chlorinated organic insecticide → DDT"],
      why_others_wrong="Freon-12 is a refrigerant, chloroform a solvent and former anaesthetic, iodoform an antiseptic.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (DDT)", seconds=20),

    Q(T_HX, "C-X bond and preparation", "Basic", "statement_pair",
      *sp("Grignard reagents are obtained by treating haloalkanes with magnesium metal in dry ether.", True,
          "In a Grignard reagent the carbon–magnesium bond is covalent but highly polar, with carbon pulling "
          "electrons from the electropositive magnesium.", True),
      "Preparation and bonding of Grignard reagents",
      "R–X + Mg → RMgX (in dry ether). NCERT describes the C–Mg bond as covalent but highly polar, carbon being the "
      "negative end, while the Mg–X bond is essentially ionic. Both statements are true.",
      ["Statement I: RX + Mg (dry ether) → RMgX → true", "Statement II: polar covalent C–Mg bond → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reaction with metals (Grignard reagents)", seconds=30),

    N(T_HX, "SN1 and SN2", "Intermediate",
      "Haloalkanes react with silver salts of carboxylic acids to give esters: R–X + R′COOAg → R′COOR + AgX. "
      "The mass of ethyl ethanoate formed when 10.9 g of bromoethane reacts completely with silver ethanoate is "
      "(C = 12, H = 1, O = 16, Br = 80, Ag = 108):",
      ["4.6 g", "16.7 g", "7.4 g", "8.8 g"], "D", v_1700,
      "Nucleophilic substitution of haloalkanes by carboxylate ions",
      "The ethanoate ion replaces bromide: CH₃CH₂Br + CH₃COOAg → CH₃COOCH₂CH₃ + AgBr. One mole of bromoethane gives "
      "one mole of ethyl ethanoate (M = 88 g mol⁻¹).",
      ["n(C₂H₅Br) = 10.9/109 = 0.10 mol", "n(ester) = 0.10 mol", "Mass = 0.10 × 88 = 8.8 g"],
      why_others_wrong="4.6 g is the mass of ethanol and 7.4 g that of ethoxyethane, products with other reagents; "
                       "16.7 g is the mass of silver ethanoate used.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions (table of reagents)",
      seconds=40),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "multi_statement",
      *ms("Which of the following statements about electrophilic substitution in chlorobenzene are correct?",
          [("Friedel–Crafts methylation (CH₃Cl, anhydrous AlCl₃) gives 2-chlorotoluene and 4-chlorotoluene.", True),
           ("Friedel–Crafts acetylation (CH₃COCl, anhydrous AlCl₃) gives 2-chloroacetophenone and "
            "4-chloroacetophenone.", True),
           ("Sulphonation with concentrated H₂SO₄ gives mainly 3-chlorobenzenesulphonic acid.", False),
           ("Because of its −I effect, the chlorine atom directs the incoming group to the meta position.", False)],
          [["a", "b", "c"], ["b", "d"], ["a", "c"]], "B"),
      "Orientation of electrophilic substitution in haloarenes",
      "The chlorine atom withdraws electrons by the −I effect, which slows the reaction, but its +R effect raises "
      "the electron density at the ortho and para positions. So all electrophilic substitutions of chlorobenzene "
      "(alkylation, acylation, sulphonation, nitration, halogenation) give mainly ortho and para products.",
      ["(a) o- and p-chlorotoluene → true", "(b) o- and p-chloroacetophenone → true",
       "(c) sulphonation gives mainly 4-chlorobenzenesulphonic acid → false",
       "(d) orientation is ortho/para, set by the +R effect → false"],
      why_others_wrong="The other options include (c) or (d), or leave out (a).",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', electrophilic substitution reactions of haloarenes", seconds=50),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "assertion_reason",
      *ar("Exposure to carbon tetrachloride can cause liver cancer in humans.", True,
          "Carbon tetrachloride is used in the manufacture of refrigerants and propellants for aerosol cans.", True),
      "Uses and health effects of tetrachloromethane",
      "NCERT lists liver cancer among the effects of exposure to CCl₄, along with dizziness, nausea and possible "
      "damage to nerve cells, so A is true. R is also true (an industrial use of CCl₄), but a use of the compound "
      "says nothing about why it harms the liver, so R does not explain A.",
      ["A: health effect of CCl₄ → true", "R: industrial use of CCl₄ → true", "R is unrelated to A"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (tetrachloromethane)", seconds=35),

    Q(T_HX, "SN1 and SN2", "Intermediate", "direct",
      "Which reagent converts 1-bromobutane into butane?",
      ["Alcoholic KOH", "AgCN", "LiAlH₄", "NaI in dry acetone"], "C",
      "Reduction of haloalkanes by hydride",
      "Lithium aluminium hydride supplies the hydride ion, H⁻, which replaces the halogen: R–Br → R–H. With LiAlH₄, "
      "1-bromobutane gives butane.",
      ["H⁻ (from LiAlH₄) replaces Br⁻ → CH₃CH₂CH₂CH₃"],
      why_others_wrong="Alcoholic KOH gives but-1-ene by elimination; AgCN gives butyl isocyanide; NaI in acetone "
                       "gives 1-iodobutane (Finkelstein reaction).",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions (table of reagents)",
      seconds=25),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "11.25 g of chlorobenzene is nitrated completely with a mixture of concentrated nitric and sulphuric acids. "
      "The product is a mixture of 1-chloro-2-nitrobenzene and 1-chloro-4-nitrobenzene, of which 60% (by moles) is "
      "the para isomer. The mass of 1-chloro-4-nitrobenzene formed is (C = 12, H = 1, Cl = 35.5, N = 14, O = 16):",
      ["15.75 g", "9.45 g", "6.30 g", "6.75 g"], "B", v_1704,
      "Nitration of chlorobenzene (ortho/para orientation)",
      "One mole of C₆H₅Cl (112.5 g mol⁻¹) gives one mole of mononitro products, C₆H₄ClNO₂ (157.5 g mol⁻¹), split "
      "between the ortho and para isomers.",
      ["n(C₆H₅Cl) = 11.25/112.5 = 0.10 mol", "n(para) = 0.60 × 0.10 = 0.060 mol",
       "Mass = 0.060 × 157.5 = 9.45 g"],
      why_others_wrong="15.75 g treats the whole product as the para isomer; 6.30 g is the mass of the ortho isomer; "
                       "6.75 g uses the molar mass of chlorobenzene instead of the nitro compound.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', electrophilic substitution (nitration of haloarenes)",
      seconds=60),

    Q(T_HX, "Polyhalogen compounds", "Advanced", "statement_pair",
      *sp("Breathing about 900 parts of chloroform per million parts of air for a short time can cause dizziness, "
          "fatigue and headache.", True,
          "Chronic chloroform exposure may damage the liver, where chloroform is metabolised to carbon "
          "tetrachloride.", False),
      "Environmental and health effects of trichloromethane",
      "NCERT states that inhaling about 900 ppm of chloroform for a short time causes dizziness, fatigue and "
      "headache, so Statement I is true. NCERT also states that chronic exposure may damage the liver, where "
      "chloroform is metabolised to phosgene (COCl₂), and the kidneys. Statement II names the wrong metabolite, so "
      "it is false.",
      ["Statement I: NCERT data → true", "Liver metabolises CHCl₃ to phosgene, not CCl₄ → Statement II false"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (trichloromethane)", seconds=40),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "Toluene is treated with chlorine in the presence of light (no Lewis acid) to give the monochloro product X. "
      "X is heated with ethanolic KCN to give Y, and Y is hydrolysed completely with dilute acid to give Z. Z is:",
      ["Benzoic acid", "4-Methylbenzoic acid", "Benzyl alcohol", "Phenylethanoic acid"], "D",
      "Side-chain halogenation followed by nucleophilic substitution",
      "In light and without a Lewis acid, chlorine substitutes a hydrogen of the methyl group by a free-radical "
      "reaction: C₆H₅CH₂Cl (X, benzyl chloride). Being a benzylic halide, it reacts readily with CN⁻ to give "
      "C₆H₅CH₂CN (Y). Hydrolysis of the nitrile gives C₆H₅CH₂COOH (Z), phenylethanoic acid, which keeps the extra "
      "carbon introduced by cyanide.",
      ["X = C₆H₅CH₂Cl (side chain)", "Y = C₆H₅CH₂CN", "Z = C₆H₅CH₂COOH"],
      why_others_wrong="Benzoic acid would lose a carbon; 4-methylbenzoic acid would need ring chlorination (and aryl "
                       "chlorides do not react with KCN under these conditions); benzyl alcohol would come from "
                       "hydrolysis of X with aqueous alkali.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation by free radical halogenation and nucleophilic "
            f"substitution", seconds=60),
]

# ================================================================ Organic Compounds Containing Oxygen (1707-1723)
# 1711: 2C2H5OH -> C2H5OC2H5 + H2O (conc. H2SO4, 413 K) ; 9.2 g ethanol
n_1711 = F(92, 10) / mm(C=2, H=6, O=1)
assert n_1711 == F(1, 5)
v_1711 = g(n_1711 / 2 * mm(C=4, H=10, O=1), 1)
assert v_1711 == "7.4 g" and g(n_1711 * 74, 1) == "14.8 g" and g(n_1711 * 28, 1) == "5.6 g" and g(n_1711 / 4 * 74, 1) == "3.7 g"
# 1717: C6H5OH + 3Br2 -> C6H2Br3OH + 3HBr ; 9.4 g phenol
m_tbp = mm(C=6, H=3, Br=3, O=1)
assert m_tbp == 331 and mm(C=6, H=5, Br=1, O=1) == 173 and mm(C=6, H=4, Br=2, O=1) == 252
n_1717 = F(94, 10) / mm(C=6, H=6, O=1)
assert n_1717 == F(1, 10)
v_1717 = g(n_1717 * m_tbp, 1)
assert v_1717 == "33.1 g" and g(n_1717 * 173, 1) == "17.3 g" and g(n_1717 * 252, 1) == "25.2 g" and g(2 * n_1717 * m_tbp, 1) == "66.2 g"
# 1718: CH3COOH + 3Cl2 (red P) -> CCl3COOH + 3HCl ; 6.0 g acid
n_1718 = F(6) / mm(C=2, H=4, O=2)
assert n_1718 == F(1, 10)
v_1718 = g(n_1718 * 3 * 71, 1)
assert v_1718 == "21.3 g" and g(n_1718 * 71, 1) == "7.1 g" and g(n_1718 * 2 * 71, 1) == "14.2 g"
assert g(n_1718 * 3 * F(355, 10), 2) == "10.65 g"
# 1722: 7.0 g phenol + ethanol ; 50.0 mL of 1.0 M NaOH neutralises the phenol only ; excess Na then gives H2
n_ph = F(50, 1000) * 1
m_ph = n_ph * 94
m_et = 7 - m_ph
n_et = m_et / 46
assert (m_ph, m_et, n_et) == (F(47, 10), F(23, 10), F(1, 20))
v_1722 = g((n_ph + n_et) / 2 * F(224, 10), 2, " L")
assert v_1722 == "1.12 L" and g(n_ph / 2 * F(224, 10), 2, " L") == "0.56 L"
assert g((n_ph + n_et) * F(224, 10), 2, " L") == "2.24 L" and g((n_ph + m_et / 94) / 2 * F(224, 10), 2, " L") == "0.83 L"
# 1723: 2.32 g propanal + propanone ; Tollens gives 2.16 g Ag (2 Ag per CHO)
n_ag = F(216, 100) / 108
n_pal = n_ag / 2
m_pal = n_pal * mm(C=3, H=6, O=1)
assert (n_ag, m_pal) == (F(2, 100), F(58, 100))
v_1723 = pct((F(232, 100) - m_pal) / F(232, 100))
assert v_1723 == "75.0%" and pct(m_pal / F(232, 100)) == "25.0%"
assert pct((F(232, 100) - n_ag * 58) / F(232, 100)) == "50.0%" and pct((F(232, 100) - n_ag / 4 * 58) / F(232, 100)) == "87.5%"

QUESTIONS += [
    Q(T_OX, "Alcohols", "Basic", "direct",
      "In the commercial preparation of ethanol from molasses, sucrose is first converted into glucose and fructose. "
      "These are then converted into ethanol and carbon dioxide by the enzyme:",
      ["Invertase", "Zymase", "Maltase", "Diastase"], "B",
      "Fermentation in the manufacture of ethanol",
      "Invertase hydrolyses sucrose to glucose and fructose. Zymase, another enzyme present in yeast, converts "
      "glucose and fructose into ethanol and CO₂: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂.",
      ["Sucrose → glucose + fructose (invertase)", "Glucose/fructose → ethanol + CO₂ (zymase)"],
      why_others_wrong="Invertase only hydrolyses sucrose; maltase and diastase act on maltose and starch, not in this "
                       "fermentation step.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', commercially important alcohols (ethanol)", seconds=20),

    Q(T_OX, "Ethers", "Basic", "direct",
      "The boiling point of ethoxyethane (M = 74 g mol⁻¹) is closest to that of:",
      ["Butan-1-ol (M = 74 g mol⁻¹)", "Propanoic acid (M = 74 g mol⁻¹)", "Propan-1-ol (M = 60 g mol⁻¹)",
       "n-Pentane (M = 72 g mol⁻¹)"], "D",
      "Boiling points of ethers",
      "Ether molecules are only weakly polar and cannot form hydrogen bonds with one another, so the boiling points "
      "of ethers resemble those of alkanes of comparable molecular mass and are much lower than those of alcohols. "
      "NCERT compares ethoxyethane (307.6 K) with n-pentane (309.1 K) and butan-1-ol (390 K).",
      ["No intermolecular H-bonding in ethers", "Ethoxyethane 307.6 K ≈ n-pentane 309.1 K",
       "Butan-1-ol 390 K; propanoic acid and propan-1-ol are also H-bonded and boil much higher"],
      why_others_wrong="The alcohols and the acid have intermolecular hydrogen bonds, so they boil far above "
                       "ethoxyethane even though their molar masses are similar.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties of ethers", seconds=30),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("In wine making, if air gets into the fermentation mixture, the oxygen of air oxidises ethanol to ethanoic "
          "acid, which spoils the taste of the drink.", True,
          "Most of the methanol produced today is made by the fermentation of sugars.", False),
      "Ethanol and methanol: commercial preparation",
      "NCERT notes that fermentation is carried out in the absence of air; if air enters, ethanol is oxidised to "
      "ethanoic acid and the taste of the drink is destroyed (Statement I true). Methanol is now produced mainly by "
      "catalytic hydrogenation of carbon monoxide (CO + 2H₂ over ZnO–Cr₂O₃), not by fermentation (Statement II "
      "false).",
      ["Statement I: aerial oxidation of ethanol → ethanoic acid → true",
       "Statement II: methanol from CO + 2H₂ → false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', commercially important alcohols", seconds=30),

    Q(T_OX, "Carboxylic acids", "Basic", "match_list",
      *ml("Match the common name of the carboxylic acid in List-I with its IUPAC name in List-II.",
          ["Formic acid", "Acetic acid", "Propionic acid", "Butyric acid"],
          ["Butanoic acid", "Propanoic acid", "Methanoic acid", "Ethanoic acid"],
          "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "A"),
      "Common and IUPAC names of carboxylic acids",
      "The common names come from natural sources (formica, ant; acetum, vinegar; butyrum, butter). In IUPAC names "
      "the -e of the alkane with the same number of carbon atoms is replaced by -oic acid.",
      ["Formic (C₁) → methanoic (III)", "Acetic (C₂) → ethanoic (IV)", "Propionic (C₃) → propanoic (II)",
       "Butyric (C₄) → butanoic (I)"],
      why_others_wrong="The other codes interchange acids differing by one carbon atom.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nomenclature of carboxylic acids", seconds=25),

    N(T_OX, "Ethers", "Basic",
      "Ethanol is heated with concentrated sulphuric acid at 413 K, keeping the alcohol in excess, and is converted "
      "into ethoxyethane: 2C₂H₅OH → C₂H₅–O–C₂H₅ + H₂O. The mass of ethoxyethane obtained from 9.2 g of ethanol, "
      "assuming complete conversion, is (C = 12, H = 1, O = 16):",
      ["14.8 g", "5.6 g", "7.4 g", "3.7 g"], "C", v_1711,
      "Preparation of ethers by dehydration of alcohols",
      "Two molecules of ethanol lose one molecule of water to give one molecule of ethoxyethane (M = 74 g mol⁻¹).",
      ["n(C₂H₅OH) = 9.2/46 = 0.20 mol", "n(ether) = 0.20/2 = 0.10 mol", "Mass = 0.10 × 74 = 7.4 g"],
      why_others_wrong="14.8 g takes one ether per ethanol; 5.6 g is the mass of ethene, formed at 443 K, not 413 K; "
                       "3.7 g halves the correct amount again.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of ethers (dehydration of alcohols)", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "direct",
      "Propanone undergoes an aldol reaction in the presence of dilute alkali such as barium hydroxide. The "
      "β-hydroxy ketone (ketol) formed is:",
      ["4-Methylpent-3-en-2-one", "3-Hydroxybutanal", "4-Hydroxy-4-methylpentan-2-one", "Hexane-2,5-dione"], "C",
      "Aldol reaction of ketones",
      "The carbanion from one propanone molecule (formed by loss of an α-hydrogen) adds to the C=O group of a second "
      "molecule: CH₃COCH₂–C(OH)(CH₃)₂, i.e. 4-hydroxy-4-methylpentan-2-one. On heating it loses water to give the "
      "α,β-unsaturated ketone 4-methylpent-3-en-2-one.",
      ["⁻CH₂COCH₃ adds to (CH₃)₂C=O", "Ketol: (CH₃)₂C(OH)–CH₂–CO–CH₃", "Name: 4-hydroxy-4-methylpentan-2-one"],
      why_others_wrong="4-Methylpent-3-en-2-one is the dehydrated (condensation) product, not the ketol; "
                       "3-hydroxybutanal is the aldol of ethanal; hexane-2,5-dione is not an aldol product.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol reaction", seconds=40),

    Q(T_OX, "Phenols", "Intermediate", "statement_pair",
      *sp("With concentrated nitric acid, phenol is converted into 2,4,6-trinitrophenol, but the yield of the product "
          "is poor.", True,
          "Nowadays picric acid is prepared by treating phenol first with concentrated sulphuric acid, which "
          "converts it into phenol-2,4-disulphonic acid, and then with concentrated nitric acid.", True),
      "Preparation of picric acid",
      "Both statements are taken from NCERT. Direct nitration of phenol with concentrated nitric acid gives picric "
      "acid in poor yield (much of the phenol is oxidised). In the modern method, phenol is first sulphonated to "
      "phenol-2,4-disulphonic acid, which is then nitrated to 2,4,6-trinitrophenol.",
      ["Statement I true", "Statement II true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', electrophilic substitution in phenols (nitration)",
      seconds=35),

    Q(T_OX, "Carboxylic acids", "Intermediate", "assertion_reason",
      *ar("Ethylbenzene, on vigorous oxidation with alkaline KMnO₄ followed by acidification, gives phenylethanoic "
          "acid.", False,
          "On vigorous oxidation of an alkylbenzene, the entire side chain is oxidised to a carboxyl group, "
          "irrespective of its length.", True),
      "Oxidation of alkylbenzenes to aromatic carboxylic acids",
      "NCERT states that vigorous oxidation of alkylbenzenes with chromic acid or acidic or alkaline KMnO₄ converts "
      "the entire side chain into –COOH, whatever its length. Ethylbenzene therefore gives benzoic acid, not "
      "phenylethanoic acid. A is false and R is true.",
      ["C₆H₅–CH₂CH₃ → C₆H₅–COOH (whole side chain → COOH)", "A false", "R true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of carboxylic acids from alkylbenzenes",
      seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the physical properties of aldehydes and ketones are correct?",
          [("Methanal is a gas at room temperature.", True),
           ("Ethanal is a volatile liquid.", True),
           ("Methanal, ethanal and propanone are miscible with water in all proportions.", True),
           ("The solubility of aldehydes and ketones in water increases as the length of the alkyl chain "
            "increases.", False)],
          [["a", "b"], ["b", "c", "d"], ["a", "c", "d"]], "D"),
      "Physical properties of carbonyl compounds",
      "NCERT: methanal is a gas and ethanal a volatile liquid at room temperature; other aldehydes and ketones are "
      "liquids or solids. The lower members are miscible with water in all proportions because they form hydrogen "
      "bonds with water, but solubility falls rapidly as the alkyl chain grows.",
      ["(a) true", "(b) true", "(c) true", "(d) solubility decreases with chain length → false"],
      why_others_wrong="The other options include (d) or leave out (c).",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', physical properties", seconds=40),

    Q(T_OX, "Phenols", "Intermediate", "direct",
      "Phenol reacts with ethanoyl chloride in the presence of pyridine. The organic product is:",
      ["4-Hydroxyacetophenone", "Phenyl ethanoate, CH₃COOC₆H₅", "Methyl benzoate", "Benzyl ethanoate"], "B",
      "Esterification of phenols",
      "Like alcohols, phenols react with acid chlorides to form esters; the reaction is carried out in the presence "
      "of a base such as pyridine, which neutralises the HCl formed. The O–H hydrogen is replaced by the acyl group: "
      "C₆H₅OH + CH₃COCl → CH₃COOC₆H₅ + HCl.",
      ["Acylation at oxygen → ester", "Product: phenyl ethanoate"],
      why_others_wrong="4-Hydroxyacetophenone would need ring acylation; methyl benzoate and benzyl ethanoate have "
                       "different carbon skeletons.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', esterification of alcohols and phenols", seconds=25),

    N(T_OX, "Phenols", "Intermediate",
      "9.4 g of phenol is treated with excess bromine water at room temperature. The mass of the white precipitate "
      "formed, assuming complete reaction, is (C = 12, H = 1, O = 16, Br = 80):",
      ["17.3 g", "25.2 g", "66.2 g", "33.1 g"], "D", v_1717,
      "Bromination of phenol with bromine water",
      "The –OH group strongly activates the ring. With bromine water all three ortho and para positions are "
      "substituted, giving a white precipitate of 2,4,6-tribromophenol (C₆H₂Br₃OH, M = 331 g mol⁻¹).",
      ["n(C₆H₅OH) = 9.4/94 = 0.10 mol", "Product: 2,4,6-tribromophenol (1 : 1)", "Mass = 0.10 × 331 = 33.1 g"],
      why_others_wrong="17.3 g is for a monobromophenol (formed in CS₂ at low temperature) and 25.2 g for a "
                       "dibromophenol; 66.2 g doubles the amount.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', electrophilic substitution in phenols (halogenation)",
      seconds=40),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "6.0 g of ethanoic acid is treated with chlorine in the presence of a small amount of red phosphorus "
      "(Hell–Volhard–Zelinsky reaction) until all three α-hydrogen atoms are replaced by chlorine. The minimum mass "
      "of chlorine consumed is (C = 12, H = 1, O = 16, Cl = 35.5):",
      ["7.1 g", "21.3 g", "10.65 g", "14.2 g"], "B", v_1718,
      "α-Halogenation of carboxylic acids",
      "Each replacement of an α-hydrogen uses one molecule of Cl₂ (the other Cl atom leaves as HCl): "
      "CH₃COOH + 3Cl₂ → CCl₃COOH + 3HCl.",
      ["n(CH₃COOH) = 6.0/60 = 0.10 mol", "n(Cl₂) = 3 × 0.10 = 0.30 mol", "Mass = 0.30 × 71 = 21.3 g"],
      why_others_wrong="7.1 g replaces only one hydrogen and 14.2 g only two; 10.65 g counts chlorine atoms with the "
                       "atomic mass but forgets that each substitution consumes a whole Cl₂ molecule.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions of carboxylic acids (HVZ reaction)",
      seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "direct",
      "Benzene is treated with carbon monoxide and HCl in the presence of anhydrous AlCl₃/CuCl to give X. X is heated "
      "with concentrated NaOH to give Y and Z, where Z is an alcohol. Y is acidified to give the acid P. P is then "
      "heated with Z in the presence of a little concentrated H₂SO₄. The final product is:",
      ["Phenyl benzoate", "Dibenzyl ether", "Methyl benzoate", "Benzyl benzoate"], "D",
      "Gattermann–Koch reaction, Cannizzaro reaction and esterification",
      "Gattermann–Koch: benzene → benzaldehyde (X). Benzaldehyde has no α-hydrogen, so with concentrated NaOH it "
      "undergoes the Cannizzaro reaction: sodium benzoate (Y) and benzyl alcohol (Z). Acidification gives benzoic "
      "acid (P). Esterification of benzoic acid with benzyl alcohol gives benzyl benzoate, C₆H₅COOCH₂C₆H₅.",
      ["X = C₆H₅CHO", "Y = C₆H₅COONa, Z = C₆H₅CH₂OH (Cannizzaro)", "P = C₆H₅COOH",
       "P + Z → C₆H₅COOCH₂C₆H₅ (benzyl benzoate)"],
      why_others_wrong="Phenyl benzoate would need phenol; methyl benzoate would need methanol; an ether is not formed "
                       "from an acid and an alcohol.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Gattermann–Koch and Cannizzaro reactions; "
            f"esterification", seconds=75),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following reagents convert propanal, CH₃CH₂CHO, into propan-1-ol?",
          [("Sodium borohydride, NaBH₄", True),
           ("Lithium aluminium hydride, LiAlH₄, followed by hydrolysis", True),
           ("Hydrogen in the presence of finely divided nickel, platinum or palladium", True),
           ("Zinc amalgam and concentrated HCl", False),
           ("Hydrazine, followed by heating with KOH in ethylene glycol", False)],
          [["a", "b"], ["a", "b", "d"], ["c", "d", "e"]], "A"),
      "Reduction of aldehydes: to alcohols versus to hydrocarbons",
      "NaBH₄, LiAlH₄ and catalytic hydrogenation reduce the C=O group of an aldehyde to CH–OH, giving a primary "
      "alcohol. The Clemmensen (Zn–Hg/HCl) and Wolff–Kishner (NH₂NH₂, then KOH/ethylene glycol) reductions remove "
      "the oxygen completely and reduce C=O to CH₂, giving propane.",
      ["(a), (b), (c): >C=O → >CH–OH → propan-1-ol", "(d) Clemmensen → propane", "(e) Wolff–Kishner → propane"],
      why_others_wrong="Options containing (d) or (e) are wrong, and (a) and (b) only leaves out catalytic "
                       "hydrogenation.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reduction of aldehydes and ketones", seconds=50),

    Q(T_OX, "Phenols", "Advanced", "statement_pair",
      *sp("The carbon–oxygen bond length in phenol (136 pm) is slightly less than that in methanol (142 pm).", True,
          "In methanol, the C–O–H bond angle (108.9°) is slightly less than the tetrahedral angle, because of "
          "repulsion between the unshared electron pairs of oxygen.", True),
      "Structures of alcohols and phenols",
      "In phenol the C–O bond is shortened because the lone pair on oxygen is conjugated with the ring (partial "
      "double bond character) and because the carbon is sp² hybridised. In alcohols the oxygen is sp³ hybridised; "
      "its two lone pairs repel the bond pairs, closing the C–O–H angle slightly below 109.5°. Both statements are "
      "true.",
      ["Statement I: conjugation + sp² carbon → shorter C–O → true",
       "Statement II: lone pair–lone pair repulsion → 108.9° → true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', structures of functional groups", seconds=40),

    N(T_OX, "Phenols", "Advanced",
      "A 7.0 g mixture of phenol and ethanol needs exactly 50.0 mL of 1.0 M NaOH solution for neutralisation. The "
      "same mass of the mixture is then treated with an excess of sodium metal. The volume of hydrogen evolved, "
      "measured at STP, is (C = 12, H = 1, O = 16; molar volume at STP = 22.4 L mol⁻¹):",
      ["0.56 L", "2.24 L", "1.12 L", "0.83 L"], "C", v_1722,
      "Acidity of phenol versus ethanol",
      "Phenol is acidic enough to react with aqueous NaOH, but ethanol is not, so the NaOH measures the phenol only. "
      "Both phenol and ethanol react with sodium metal, each –OH group giving half a molecule of H₂.",
      ["n(phenol) = 0.050 × 1.0 = 0.050 mol → 4.7 g", "Ethanol = 7.0 − 4.7 = 2.3 g → 0.050 mol",
       "Total –OH = 0.10 mol → n(H₂) = 0.050 mol", "V = 0.050 × 22.4 = 1.12 L"],
      why_others_wrong="0.56 L counts only phenol; 2.24 L takes one H₂ per –OH; 0.83 L divides the ethanol mass by "
                       "the molar mass of phenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of alcohols and phenols", seconds=100),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "2.32 g of a mixture of propanal and propanone is warmed with an excess of Tollens' reagent, and 2.16 g of "
      "silver is deposited. The percentage by mass of propanone in the mixture is (C = 12, H = 1, O = 16, Ag = 108):",
      ["25.0%", "50.0%", "87.5%", "75.0%"], "D", v_1723,
      "Distinguishing aldehydes from ketones with Tollens' reagent",
      "Only the aldehyde reduces Tollens' reagent: RCHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → RCOO⁻ + 2Ag + 2H₂O + 4NH₃. Each "
      "mole of propanal deposits two moles of silver; propanone does not react.",
      ["n(Ag) = 2.16/108 = 0.020 mol", "n(propanal) = 0.010 mol → 0.58 g", "Propanone = 2.32 − 0.58 = 1.74 g",
       "% propanone = 1.74/2.32 × 100 = 75.0%"],
      why_others_wrong="25.0% is the percentage of propanal; 50.0% takes one Ag per aldehyde molecule; 87.5% takes "
                       "four Ag per aldehyde molecule.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', oxidation of aldehydes (Tollens' test)",
      seconds=90),
]

# ================================================================ Organic Compounds Containing Nitrogen (1724-1733)
# 1726: C6H5NH2 + C6H5SO2Cl -> C6H5SO2NHC6H5 + HCl ; 9.3 g aniline
m_sulf = mm(C=12, H=11, N=1, O=2, S=1)
assert m_sulf == 233 and mm(C=6, H=5, S=1, O=2, Cl=1) == F(353, 2)
n_1726 = F(93, 10) / mm(C=6, H=7, N=1)
assert n_1726 == F(1, 10)
v_1726 = g(n_1726 * m_sulf, 2)
assert v_1726 == "23.30 g" and g(n_1726 * m_sulf / 2, 2) == "11.65 g" and g(2 * n_1726 * m_sulf, 2) == "46.60 g"
assert g(n_1726 * F(353, 2), 2) == "17.65 g"
# 1730: CH3NH2 + CHCl3 + 3KOH -> CH3NC + 3KCl + 3H2O ; 3.1 g methanamine ; KOH = 56
n_1730 = F(31, 10) / mm(C=1, H=5, N=1)
assert n_1730 == F(1, 10)
v_1730 = g(3 * n_1730 * 56, 1)
assert v_1730 == "16.8 g" and g(n_1730 * 56, 1) == "5.6 g" and g(2 * n_1730 * 56, 1) == "11.2 g" and g(4 * n_1730 * 56, 1) == "22.4 g"
# 1733: C6H5N2Cl + C6H5NH2 -> p-H2N-C6H4-N=N-C6H5 (C12H11N3) + HCl ; 9.85 g of dye ; aniline for both parts
m_ay = mm(C=12, H=11, N=3)
assert m_ay == 197
n_1733 = F(985, 100) / m_ay
assert n_1733 == F(1, 20)
v_1733 = g(2 * n_1733 * 93, 2)
assert v_1733 == "9.30 g" and g(n_1733 * 93, 2) == "4.65 g" and g(4 * n_1733 * 93, 2) == "18.60 g"
assert g(3 * n_1733 * 93, 2) == "13.95 g"

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Aniline reacts with benzoyl chloride (in the presence of a base) to give:",
      ["4-Aminobenzophenone", "Benzamide, C₆H₅CONH₂", "N-Phenylbenzenesulphonamide",
       "N-Phenylbenzamide, C₆H₅CONHC₆H₅"], "D",
      "Benzoylation of amines",
      "Primary and secondary amines react with acid chlorides by nucleophilic substitution, replacing a hydrogen of "
      "–NH₂ by the acyl group. Benzoylation of aniline gives the amide C₆H₅NHCOC₆H₅ (N-phenylbenzamide, "
      "benzanilide).",
      ["C₆H₅NH₂ + C₆H₅COCl → C₆H₅NHCOC₆H₅ + HCl", "Base removes HCl"],
      why_others_wrong="Ring acylation of aniline does not occur under these conditions; benzamide would need ammonia; "
                       "a sulphonamide needs benzenesulphonyl chloride.",
      ncert=f"{NC12}, 'Amines', chemical reactions (acylation and benzoylation)", seconds=25),

    Q(T_NI, "Diazonium salts", "Basic", "statement_pair",
      *sp("The diazonium group is a very good leaving group, and it can be replaced by groups such as Cl⁻, Br⁻, I⁻, "
          "CN⁻ and OH⁻ with the loss of nitrogen gas.", True,
          "In the coupling reactions of arenediazonium salts with phenols or aromatic amines, both nitrogen atoms "
          "are retained in the product as an azo (–N=N–) group.", True),
      "Two kinds of reactions of diazonium salts",
      "NCERT classifies reactions of diazonium salts into those involving displacement of nitrogen (N₂ escapes and "
      "is replaced by Cl, Br, I, CN, OH, F, H, NO₂) and those involving retention of the diazo group (coupling "
      "reactions giving azo compounds such as p-hydroxyazobenzene). Both statements are true.",
      ["Statement I: displacement reactions → true", "Statement II: coupling gives Ar–N=N–Ar′ → true"],
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts", seconds=30),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "In Hinsberg's test, 9.3 g of aniline reacts completely with benzenesulphonyl chloride:\n"
      "C₆H₅NH₂ + C₆H₅SO₂Cl → C₆H₅SO₂NHC₆H₅ + HCl\n"
      "The mass of N-phenylbenzenesulphonamide formed is (C = 12, H = 1, N = 14, O = 16, S = 32, Cl = 35.5):",
      ["11.65 g", "46.60 g", "17.65 g", "23.30 g"], "D", v_1726,
      "Reaction of primary amines with benzenesulphonyl chloride",
      "One mole of aniline gives one mole of the sulphonamide C₁₂H₁₁NO₂S (M = 144 + 11 + 14 + 32 + 32 = 233 "
      "g mol⁻¹). Its N–H hydrogen is acidic, so the product of a primary amine dissolves in alkali.",
      ["n(aniline) = 9.3/93 = 0.10 mol", "n(product) = 0.10 mol", "Mass = 0.10 × 233 = 23.30 g"],
      why_others_wrong="11.65 g halves and 46.60 g doubles the amount; 17.65 g is the mass of benzenesulphonyl "
                       "chloride used.",
      ncert=f"{NC12}, 'Amines', reaction with arylsulphonyl chloride (Hinsberg's test)", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("The quantitative evolution of nitrogen when primary aliphatic amines react with nitrous acid is used in "
          "the estimation of amino acids and proteins.", True,
          "Primary aliphatic amines react with nitrous acid to form aliphatic diazonium salts, which, being "
          "unstable, liberate nitrogen gas quantitatively and give alcohols.", True, explains=True),
      "Reaction of primary aliphatic amines with nitrous acid",
      "RNH₂ + HNO₂ → [RN₂⁺Cl⁻] → ROH + N₂ + HCl. Because the aliphatic diazonium salt decomposes completely, one mole "
      "of N₂ is evolved per mole of –NH₂, so measuring the nitrogen gives the amount of amino groups. This is why the "
      "reaction is used to estimate amino acids and proteins: R explains A.",
      ["Unstable RN₂⁺ → N₂ quantitatively → R true", "Volume of N₂ measures –NH₂ groups → A true",
       "R explains A"],
      ncert=f"{NC12}, 'Amines', reaction with nitrous acid", seconds=40),

    Q(T_NI, "Diazonium salts", "Intermediate", "statement_pair",
      *sp("The cyano group cannot be introduced by nucleophilic substitution of chlorine in chlorobenzene, but "
          "cyanobenzene is easily obtained from benzenediazonium chloride.", True,
          "Benzenediazonium chloride on treatment with CuCN/KCN gives phenyl isocyanide, C₆H₅NC.", False),
      "Importance of diazonium salts in synthesis",
      "NCERT points out that aryl halides do not undergo easy nucleophilic substitution, so –CN cannot be introduced "
      "this way, whereas the diazonium group is readily replaced: C₆H₅N₂⁺Cl⁻ + CuCN/KCN → C₆H₅CN (benzonitrile, "
      "cyanobenzene) + N₂. So Statement I is true and Statement II, which names the isocyanide, is false.",
      ["Statement I: NCERT example of the use of diazonium salts → true",
       "CuCN/KCN gives benzonitrile, C₆H₅CN → Statement II false"],
      ncert=f"{NC12}, 'Amines', importance of diazonium salts in synthesis of aromatic compounds", seconds=35),

    Q(T_NI, "Diazonium salts", "Intermediate", "direct",
      "Which of the following tests distinguishes aniline from ethanamine?",
      ["Carbylamine test (CHCl₃ and ethanolic KOH)",
       "Treatment with NaNO₂ and HCl at 273–278 K, followed by alkaline β-naphthol",
       "Solubility in dilute hydrochloric acid",
       "Reaction with benzenesulphonyl chloride"], "B",
      "Azo dye test for primary aromatic amines",
      "Aniline forms a stable benzenediazonium salt at 273–278 K, which couples with alkaline β-naphthol to give an "
      "orange-red azo dye. Ethanamine forms an unstable aliphatic diazonium salt that decomposes at once to ethanol "
      "and N₂, so no dye is formed.",
      ["Aniline → C₆H₅N₂⁺ → azo dye with β-naphthol", "Ethanamine → N₂ + alcohol, no dye"],
      why_others_wrong="Both amines are primary, so both give the carbylamine test, both dissolve in dilute HCl and "
                       "both give alkali-soluble sulphonamides.",
      ncert=f"{NC12}, 'Amines', reactions with nitrous acid and coupling reactions", seconds=35),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "In the carbylamine reaction, CH₃NH₂ + CHCl₃ + 3KOH → CH₃NC + 3KCl + 3H₂O. The minimum mass of KOH needed for "
      "3.1 g of methanamine to react completely is (C = 12, H = 1, N = 14, K = 39, O = 16):",
      ["5.6 g", "16.8 g", "11.2 g", "22.4 g"], "B", v_1730,
      "Stoichiometry of the carbylamine (isocyanide) test",
      "Three moles of KOH remove the three HCl formed from one mole of amine and one mole of chloroform.",
      ["n(CH₃NH₂) = 3.1/31 = 0.10 mol", "n(KOH) = 3 × 0.10 = 0.30 mol", "Mass = 0.30 × 56 = 16.8 g"],
      why_others_wrong="5.6 g, 11.2 g and 22.4 g take one, two and four moles of KOH per mole of amine.",
      ncert=f"{NC12}, 'Amines', carbylamine reaction", seconds=35),

    Q(T_NI, "Diazonium salts", "Advanced", "direct",
      "Benzene is nitrated to give A. A is reduced with Sn and HCl, and the product is made alkaline to give B. B is "
      "treated with NaNO₂ and HCl at 273–278 K to give C. C is warmed with CuCN/KCN to give D, and D is reduced with "
      "LiAlH₄ to give E. E is:",
      ["Benzylamine", "Aniline", "N-Methylaniline", "Benzoic acid"], "A",
      "Synthesis through a diazonium salt",
      "A = nitrobenzene; B = aniline; C = benzenediazonium chloride; D = benzonitrile (–N₂⁺ replaced by –CN); "
      "reduction of the nitrile with LiAlH₄ gives the primary amine C₆H₅CH₂NH₂ (E), which has one carbon atom more "
      "than aniline.",
      ["A = C₆H₅NO₂", "B = C₆H₅NH₂", "C = C₆H₅N₂⁺Cl⁻", "D = C₆H₅CN", "E = C₆H₅CH₂NH₂"],
      why_others_wrong="Aniline is B, not E; N-methylaniline is an isomer of benzylamine but has the carbon on "
                       "nitrogen; benzoic acid would come from hydrolysis of D, not reduction.",
      ncert=f"{NC12}, 'Amines', preparation of amines (reduction of nitriles) and reactions of diazonium salts",
      seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "A compound X, C₇H₉N, contains a benzene ring. X gives a foul-smelling product when warmed with chloroform and "
      "ethanolic KOH. With NaNO₂ and HCl at 273–278 K, X liberates nitrogen gas and gives an alcohol instead of a "
      "stable diazonium salt. X is:",
      ["2-Methylaniline", "N-Methylaniline", "Benzylamine", "4-Methylaniline"], "C",
      "Identifying amines from the carbylamine and nitrous acid tests",
      "The carbylamine test shows that X is a primary amine, which rules out N-methylaniline (secondary). Primary "
      "arylamines (the methylanilines) form stable diazonium salts at 273–278 K. Evolution of N₂ with formation of "
      "an alcohol is characteristic of a primary amine whose –NH₂ is on an sp³ carbon, as in benzylamine, "
      "C₆H₅CH₂NH₂ (which gives C₆H₅CH₂OH).",
      ["Carbylamine positive → primary amine", "N₂ + alcohol with HNO₂ → –NH₂ not on the ring",
       "C₇H₉N with these properties → C₆H₅CH₂NH₂"],
      why_others_wrong="2- and 4-methylaniline are arylamines and give stable diazonium salts; N-methylaniline is a "
                       "secondary amine and gives no carbylamine reaction.",
      ncert=f"{NC12}, 'Amines', carbylamine reaction and reaction with nitrous acid", seconds=60),

    N(T_NI, "Diazonium salts", "Advanced",
      "Aniline yellow (p-aminoazobenzene, C₁₂H₁₁N₃) is prepared by coupling benzenediazonium chloride, made from "
      "aniline, with aniline:\n"
      "C₆H₅N₂⁺Cl⁻ + C₆H₅NH₂ → p-H₂N–C₆H₄–N=N–C₆H₅ + HCl\n"
      "The minimum total mass of aniline needed to prepare 9.85 g of aniline yellow, assuming every step is "
      "complete, is (C = 12, H = 1, N = 14):",
      ["4.65 g", "9.30 g", "18.60 g", "13.95 g"], "B", v_1733,
      "Coupling reaction of benzenediazonium chloride with aniline",
      "One aniline molecule is diazotised and a second aniline molecule is the coupling partner, so two moles of "
      "aniline are needed per mole of dye (M = 197 g mol⁻¹).",
      ["n(dye) = 9.85/197 = 0.050 mol", "Aniline: 0.050 mol (diazotised) + 0.050 mol (coupled) = 0.10 mol",
       "Mass = 0.10 × 93 = 9.30 g"],
      why_others_wrong="4.65 g counts only the aniline that is diazotised (or only the coupling partner); 13.95 g and "
                       "18.60 g use three or four moles of aniline per mole of dye.",
      ncert=f"{NC12}, 'Amines', coupling reactions of diazonium salts", seconds=60),
]

# ================================================================ Biomolecules (1734-1743)
# 1735: essential amino acids in the list
essential = {"glycine": False, "alanine": False, "leucine": True, "lysine": True, "serine": False,
             "tryptophan": True, "glutamic acid": False, "threonine": True}
v_1735 = str(sum(essential.values()))
assert v_1735 == "4"
# 1739: thyroxine C15H11I4NO4
AM["I"] = 127
m_thy = mm(C=15, H=11, I=4, N=1, O=4)
assert m_thy == 777
v_1739 = pct(F(4 * 127, m_thy))
assert v_1739 == "65.4%" and pct(F(127, 777)) == "16.3%" and pct(F(254, 777)) == "32.7%" and pct(F(381, 777)) == "49.0%"
# 1742: invert sugar = equal masses of glucose (+52.5) and fructose (-92.4)
rot = (F(525, 10) + F(-924, 10)) / 2
assert rot == F(-1995, 100)
v_1742 = "−19.95°"
assert F(525, 10) + F(-924, 10) == F(-399, 10)

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "statement_pair",
      *sp("Rhamnose, C₆H₁₂O₅, is a carbohydrate although its molecular formula does not fit the general formula "
          "Cₓ(H₂O)ᵧ.", True,
          "Ethanoic acid, C₂H₄O₂, fits the general formula Cₓ(H₂O)ᵧ but is not a carbohydrate.", True),
      "Definition of carbohydrates",
      "Carbohydrates were once regarded as hydrates of carbon, Cₓ(H₂O)ᵧ, but NCERT gives these two counter-examples: "
      "rhamnose is a carbohydrate that does not fit the formula, and ethanoic acid fits it but is not a "
      "carbohydrate. Carbohydrates are therefore defined as optically active polyhydroxy aldehydes or ketones, or "
      "compounds that give these on hydrolysis.",
      ["Statement I: NCERT example → true", "Statement II: NCERT example → true"],
      ncert=f"{NC12}, 'Biomolecules', carbohydrates (definition)", seconds=25),

    N(T_BM, "Amino acids and proteins", "Basic",
      "How many of the following amino acids are essential amino acids (cannot be synthesised in the human body)?\n"
      "Glycine, alanine, leucine, lysine, serine, tryptophan, glutamic acid, threonine",
      ["3", "5", "4", "6"], "C", v_1735,
      "Essential and non-essential amino acids",
      "Amino acids that must be obtained through the diet are essential. NCERT's table marks valine, leucine, "
      "isoleucine, arginine, lysine, threonine, methionine, phenylalanine, tryptophan and histidine as essential.",
      ["Essential: leucine, lysine, tryptophan, threonine", "Non-essential: glycine, alanine, serine, glutamic acid",
       "Count = 4"],
      why_others_wrong="5 or 6 wrongly include glutamic acid, serine or alanine; 3 misses threonine or lysine.",
      ncert=f"{NC12}, 'Biomolecules', amino acids (essential amino acids)", seconds=35),

    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "The disaccharide that is commonly known as milk sugar is:",
      ["Lactose", "Maltose", "Sucrose", "Fructose"], "A",
      "Common disaccharides",
      "NCERT: lactose is commonly known as milk sugar because this disaccharide is found in milk. It is made of "
      "β-D-galactose and β-D-glucose units.",
      ["Disaccharide present in milk → lactose (milk sugar)"],
      why_others_wrong="Maltose (malt sugar) and sucrose (cane sugar) are other disaccharides not found in milk; "
                       "fructose is a monosaccharide, not a disaccharide.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides (lactose)", seconds=20),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "match_list",
      *ml("Match the α-amino acid in List-I with its side chain (R in H₂N–CH(R)–COOH) in List-II.",
          ["Alanine", "Serine", "Phenylalanine", "Glutamic acid"],
          ["–CH₂–C₆H₅", "–CH₂–CH₂–COOH", "–CH₃", "–CH₂–OH"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A"),
      "Structures of α-amino acids",
      "From NCERT's table of α-amino acids: alanine has R = –CH₃, serine –CH₂OH, phenylalanine –CH₂C₆H₅ and glutamic "
      "acid –CH₂CH₂COOH (an acidic amino acid, with a second carboxyl group).",
      ["Alanine → –CH₃ (III)", "Serine → –CH₂OH (IV)", "Phenylalanine → –CH₂C₆H₅ (I)",
       "Glutamic acid → –CH₂CH₂COOH (II)"],
      why_others_wrong="The other codes interchange alanine and serine, phenylalanine and glutamic acid, or serine "
                       "and phenylalanine.",
      ncert=f"{NC12}, 'Biomolecules', amino acids (table of natural amino acids)", seconds=35),

    Q(T_BM, "Carbohydrates", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Complete hydrolysis of DNA gives a pentose sugar, phosphoric acid and nitrogen-containing heterocyclic "
            "bases.", True),
           ("Honey has long been used as an instant source of energy in the Ayurvedic system of medicine.", True),
           ("When the body needs glucose, enzymes break glycogen down to glucose.", True),
           ("Cellulose is the main storage polysaccharide of animals.", False),
           ("Glucose on its own is called invert sugar.", False)],
          [["a", "b"], ["a", "c", "d"], ["b", "c", "e"]], "D"),
      "Composition of nucleic acids and the importance of carbohydrates",
      "NCERT: complete hydrolysis of DNA (or RNA) yields a pentose sugar, phosphoric acid and nitrogen-containing "
      "heterocyclic compounds (the bases). Honey has long been used by Vaids as an instant source of energy. "
      "Glycogen is the storage polysaccharide of animals (liver, muscles, brain), and enzymes break it down to "
      "glucose when the body needs it. Cellulose is a structural polysaccharide of plant cell walls, not an animal "
      "store. Invert sugar is the equimolar mixture of glucose and fructose obtained by hydrolysing sucrose.",
      ["(a) true", "(b) true", "(c) true", "(d) glycogen is the animal storage polysaccharide → false",
       "(e) invert sugar = glucose + fructose mixture → false"],
      why_others_wrong="The other options include (d) or (e), or leave out (c).",
      ncert=f"{NC12}, 'Biomolecules', carbohydrates (importance; polysaccharides) and nucleic acids (chemical "
            f"composition)", seconds=45),

    N(T_BM, "Hormones", "Intermediate",
      "Thyroxine, the hormone produced by the thyroid gland, is an iodinated derivative of the amino acid tyrosine "
      "with the molecular formula C₁₅H₁₁I₄NO₄. The percentage of iodine by mass in thyroxine is "
      "(C = 12, H = 1, I = 127, N = 14, O = 16):",
      ["16.3%", "65.4%", "49.0%", "32.7%"], "B", v_1739,
      "Composition of thyroxine",
      "Molar mass = 15(12) + 11(1) + 4(127) + 14 + 4(16) = 180 + 11 + 508 + 14 + 64 = 777 g mol⁻¹, of which iodine "
      "contributes 4 × 127 = 508 g.",
      ["M = 777 g mol⁻¹", "Mass of I = 508 g", "% I = 508/777 × 100 = 65.4%"],
      why_others_wrong="16.3%, 32.7% and 49.0% count only one, two or three iodine atoms.",
      ncert=f"{OLD12}, 'Biomolecules', hormones (thyroxine)", seconds=40),

    Q(T_BM, "Carbohydrates", "Intermediate", "assertion_reason",
      *ar("Fructose is laevorotatory.", True,
          "Fructose belongs to the D-series, because the –OH group on its lowest asymmetric carbon (C-5) is on the "
          "right in the Fischer projection.", True),
      "D/L configuration versus the sign of optical rotation",
      "Natural fructose is D-(−)-fructose. Both statements are true, but the letter D only describes the relative "
      "configuration (compared with glyceraldehyde); it has no relation to the direction in which the compound "
      "rotates plane-polarised light (D-glucose, for example, is dextrorotatory). So R does not explain A.",
      ["A: D-(−)-fructose → laevorotatory → true", "R: configuration at C-5 like D-glyceraldehyde → true",
       "D/L is not the sign of rotation → R does not explain A"],
      ncert=f"{NC12}, 'Biomolecules', monosaccharides (D- and L- configuration; fructose)", seconds=40),

    Q(T_BM, "Amino acids and proteins", "Advanced", "assertion_reason",
      *ar("Curdling of milk is an example of the denaturation of a protein.", True,
          "Lactic acid formed by the bacteria present in milk changes the pH, which disturbs the hydrogen bonds that "
          "maintain the secondary and tertiary structures of the protein.", True, explains=True),
      "Denaturation of proteins",
      "A change in temperature or pH disturbs the hydrogen bonds that hold a native protein in its folded shape; "
      "the globules unfold, helices uncoil and biological activity is lost, while the primary structure stays "
      "intact. NCERT cites curdling of milk, caused by lactic acid formed by bacteria, as an example. R gives the "
      "mechanism of A.",
      ["Lactic acid → change in pH", "pH change → H-bonds disrupted → secondary/tertiary structure lost",
       "That is denaturation → R explains A"],
      ncert=f"{NC12}, 'Biomolecules', denaturation of proteins", seconds=45),

    N(T_BM, "Carbohydrates", "Advanced",
      "Sucrose is hydrolysed completely into an equimolar mixture of D-glucose and D-fructose (invert sugar). Taking "
      "the specific rotations of D-glucose and D-fructose as +52.5° and −92.4°, and noting that equal amounts in moles "
      "of these isomers are equal masses, the specific rotation of the invert sugar mixture is:",
      ["+66.5°", "−39.9°", "−19.95°", "+19.95°"], "C", v_1742,
      "Inversion of cane sugar",
      "Glucose and fructose are both C₆H₁₂O₆, so the mixture contains equal masses of each, and the specific "
      "rotation of the mixture is the average of the two values.",
      ["[α] = ½(+52.5°) + ½(−92.4°)", "= 26.25° − 46.2° = −19.95°",
       "The sign changes from (+) for sucrose to (−) → 'inversion'"],
      why_others_wrong="+66.5° is the rotation of sucrose itself; −39.9° adds the two values without averaging; "
                       "+19.95° has the wrong sign.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides (sucrose and invert sugar)", seconds=60),

    Q(T_BM, "Vitamins", "Advanced", "multi_statement",
      *ms("Which of the following statements about vitamins are correct?",
          [("Deficiency of vitamin A can cause night blindness.", True),
           ("Deficiency of vitamin D causes osteomalacia (soft bones and joint pain) in adults.", True),
           ("Deficiency of vitamin B₁₂ causes beriberi.", False),
           ("Vitamin K is a water-soluble vitamin.", False),
           ("An excess of vitamins is also harmful, so vitamin pills should not be taken without a doctor's "
            "advice.", True)],
          [["a", "b"], ["a", "c", "e"], ["b", "d", "e"]], "C"),
      "Deficiency diseases and solubility of vitamins",
      "NCERT's table lists xerophthalmia and night blindness for vitamin A, rickets (children) and osteomalacia "
      "(adults) for vitamin D, beriberi for vitamin B₁ and pernicious anaemia for vitamin B₁₂. Vitamins A, D, E and K "
      "are fat soluble. NCERT also warns that an excess of vitamins is harmful.",
      ["(a) true", "(b) true", "(c) beriberi is vitamin B₁ deficiency → false", "(d) K is fat soluble → false",
       "(e) true"],
      why_others_wrong="The other options include (c) or (d), or leave out (e).",
      ncert=f"{NC12}, 'Biomolecules', vitamins", seconds=50),
]

# ================================================================ Practical Chemistry (1744-1750)
# 1747: 50 mL water at 50.0 C + 50 mL water at 20.0 C in the calorimeter -> 34.0 C ; c = 4.2 J/g/K
lost = 50 * F(42, 10) * (50 - 34)
gained_water = 50 * F(42, 10) * (34 - 20)
w_cal = (lost - gained_water) / (34 - 20)
assert (lost, gained_water, w_cal) == (3360, 2940, 30)
v_1747 = "30 J K⁻¹"
assert lost - gained_water == 420 and F(420, 16) == F(2625, 100) and F(420, 30) == 14
# 1749: 1.0 mL of 0.010 M S2O3(2-) in 50.0 mL ; blue colour after 40 s
n_thio = F(1, 1000) * F(1, 100)
n_i2 = n_thio / 2
n_h2o2 = n_i2                      # H2O2 + 2I- + 2H+ -> I2 + 2H2O
rate = n_h2o2 / F(50, 1000) / 40
assert rate == F(25, 10 ** 7)
v_1749 = "2.5 × 10⁻⁶ mol L⁻¹ s⁻¹"
assert n_thio / F(50, 1000) / 40 == F(5, 10 ** 6) and n_h2o2 / 40 == F(125, 10 ** 9) and n_h2o2 / F(50, 1000) == F(1, 10 ** 4)

QUESTIONS += [
    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In the confirmatory test for Mg²⁺ ions in salt analysis, the solution is made alkaline with ammonium hydroxide "
      "and disodium hydrogen phosphate (or ammonium phosphate) is added. The white crystalline precipitate formed is:",
      ["Magnesium carbonate", "Magnesium hydroxide", "Magnesium ammonium phosphate, Mg(NH₄)PO₄",
       "Magnesium oxalate"], "C",
      "Confirmatory test for magnesium",
      "In the presence of NH₄OH, phosphate ions precipitate Mg²⁺ as white crystalline magnesium ammonium phosphate: "
      "Mg²⁺ + HPO₄²⁻ + NH₄OH → Mg(NH₄)PO₄ + H₂O.",
      ["Reagents: NH₄OH + Na₂HPO₄", "White crystalline Mg(NH₄)PO₄ confirms Mg²⁺"],
      why_others_wrong="Carbonate, hydroxide and oxalate are not the precipitate formed with the phosphate reagent.",
      ncert=f"{LAB}, systematic analysis of cations (group V: Mg²⁺)", seconds=25),

    Q(T_PR, "Preparations", "Basic", "statement_pair",
      *sp("Egg albumin forms a lyophobic sol with water.", False,
          "Aluminium hydroxide forms a lyophilic sol with water.", False),
      "Lyophilic and lyophobic sols",
      "In the laboratory manual, starch, gum and egg albumin are used to prepare lyophilic sols (they form colloids "
      "directly on mixing with water), whereas sols of aluminium hydroxide, ferric hydroxide and arsenious sulphide "
      "are lyophobic and are prepared by chemical methods. So both statements are false.",
      ["Egg albumin → lyophilic → Statement I false", "Al(OH)₃ → lyophobic → Statement II false"],
      ncert=f"{LAB}, preparation of lyophilic and lyophobic sols", seconds=30),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the anion (with the test performed) in List-I with the observation in List-II.",
          ["Cl⁻: salt heated with solid K₂Cr₂O₇ and concentrated H₂SO₄",
           "Br⁻: solution shaken with chlorine water and chloroform",
           "I⁻: solution shaken with chlorine water and chloroform",
           "SO₄²⁻: solution treated with lead acetate"],
          ["Violet colour in the chloroform layer", "White precipitate, soluble in ammonium acetate",
           "Orange-red vapours", "Orange-brown colour in the chloroform layer"],
          "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "D"),
      "Confirmatory tests for anions",
      "Chloride gives orange-red vapours of chromyl chloride, CrO₂Cl₂ (chromyl chloride test). Chlorine water "
      "liberates bromine and iodine from bromides and iodides; these dissolve in chloroform to give an orange-brown "
      "and a violet layer respectively. Sulphate gives white PbSO₄ with lead acetate, which dissolves in ammonium "
      "acetate.",
      ["A → orange-red vapours (III)", "B → orange-brown layer (IV)", "C → violet layer (I)",
       "D → white ppt soluble in ammonium acetate (II)"],
      why_others_wrong="The other codes interchange the bromide and iodide layer colours or the chloride and sulphate "
                       "observations.",
      ncert=f"{LAB}, systematic analysis of anions (confirmatory tests)", seconds=45),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "To find the heat capacity of a calorimeter, 50 mL of water at 20.0 °C is placed in it. Then 50 mL of water at "
      "50.0 °C is added, and the final temperature of the mixture is 34.0 °C. Taking the density of water as "
      "1.0 g mL⁻¹ and its specific heat as 4.2 J g⁻¹ K⁻¹, the heat capacity of the calorimeter is:",
      ["420 J K⁻¹", "26.25 J K⁻¹", "14 J K⁻¹", "30 J K⁻¹"], "D", v_1747,
      "Calorimeter constant (water equivalent) by the method of mixtures",
      "Heat lost by the hot water = heat gained by the cold water + heat gained by the calorimeter. The calorimeter "
      "starts at the temperature of the cold water and rises with it.",
      ["Heat lost by hot water = 50 × 4.2 × (50 − 34) = 3360 J",
       "Heat gained by cold water = 50 × 4.2 × (34 − 20) = 2940 J", "Heat gained by calorimeter = 420 J",
       "Heat capacity = 420/(34 − 20) = 30 J K⁻¹"],
      why_others_wrong="420 J K⁻¹ forgets to divide by the temperature rise; 26.25 J K⁻¹ divides by the fall in "
                       "temperature of the hot water (16 K); 14 J K⁻¹ divides by the sum of both changes (30 K).",
      ncert=f"{LAB}, thermochemistry (determination of the calorimeter constant)", seconds=70),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Intermediate", "assertion_reason",
      *ar("In studying the rate of the reaction between hydrogen peroxide and iodide ions, a small known amount of "
          "sodium thiosulphate and some starch are added, and the time taken for a blue colour to appear is noted.",
          True,
          "Thiosulphate reduces the iodine formed back to iodide until all the thiosulphate is used up; only then "
          "does free iodine give the blue colour with starch.", True, explains=True),
      "Iodine clock method for following a reaction rate",
      "H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O. The iodine formed is at once reduced by thiosulphate (I₂ + 2S₂O₃²⁻ → 2I⁻ + "
      "S₄O₆²⁻), so no colour appears until the thiosulphate is exhausted. The blue colour then appears suddenly, "
      "after a fixed amount of reaction, so the time measured gives the rate. R explains A.",
      ["Thiosulphate consumes I₂ as it forms", "Blue colour only after S₂O₃²⁻ is used up",
       "Time = time for a fixed amount of reaction → rate"],
      ncert=f"{LAB}, chemical kinetics: reaction of iodide ions with hydrogen peroxide", seconds=45),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "In an iodine clock experiment, the reaction mixture (total volume 50.0 mL) contains H₂O₂, iodide ions, acid, "
      "starch and 1.0 mL of 0.010 M Na₂S₂O₃. The reactions are:\n"
      "H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O ;  I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻\n"
      "The blue colour appears after 40 s. The average rate of consumption of H₂O₂ over this period is:",
      ["1.0 × 10⁻⁴ mol L⁻¹ s⁻¹", "5.0 × 10⁻⁶ mol L⁻¹ s⁻¹", "2.5 × 10⁻⁶ mol L⁻¹ s⁻¹",
       "1.25 × 10⁻⁷ mol L⁻¹ s⁻¹"], "C", v_1749,
      "Rate from an iodine clock reaction",
      "When the blue colour appears, all the thiosulphate has been used; the iodine it consumed came from H₂O₂ "
      "(1 H₂O₂ → 1 I₂ → reacts with 2 S₂O₃²⁻).",
      ["n(S₂O₃²⁻) = 1.0 × 10⁻³ L × 0.010 M = 1.0 × 10⁻⁵ mol", "n(I₂) = n(H₂O₂) = 5.0 × 10⁻⁶ mol",
       "Δ[H₂O₂] = 5.0 × 10⁻⁶ / 0.050 L = 1.0 × 10⁻⁴ mol L⁻¹", "Rate = 1.0 × 10⁻⁴ / 40 = 2.5 × 10⁻⁶ mol L⁻¹ s⁻¹"],
      why_others_wrong="1.0 × 10⁻⁴ is the change in concentration, not divided by time; 5.0 × 10⁻⁶ takes one H₂O₂ per "
                       "thiosulphate ion; 1.25 × 10⁻⁷ is in mol s⁻¹, as the volume was not used.",
      ncert=f"{LAB}, chemical kinetics: reaction of iodide ions with hydrogen peroxide", seconds=100),

    Q(T_PR, "Titrimetric analysis", "Advanced", "statement_pair",
      *sp("Ferrous ammonium sulphate (Mohr's salt) is preferred to ferrous sulphate as a primary standard, because it "
          "is less readily oxidised by air.", True,
          "Potassium permanganate is a primary standard, so its solution need not be standardised before use.",
          False),
      "Primary standards in redox titrations",
      "A primary standard must be pure, stable and not affected by air. Mohr's salt is a stable double salt that is "
      "not easily oxidised in air, unlike ferrous sulphate, so it is used to standardise KMnO₄ (Statement I true). "
      "KMnO₄ is not obtained in a pure state and its solution slowly deposits MnO₂, so it is not a primary standard "
      "and must be standardised, e.g. against oxalic acid or Mohr's salt (Statement II false).",
      ["Statement I true", "KMnO₄ is a secondary standard → Statement II false"],
      ncert=f"{LAB}, titrimetric analysis (redox titrations: primary and secondary standards)", seconds=40),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_PB: (4, 5, 4), T_DF: (4, 5, 4), T_CC: (5, 6, 4), T_PU: (1, 2, 1), T_GO: (5, 7, 5), T_HC: (4, 6, 4),
        T_HX: (3, 4, 3), T_OX: (5, 7, 5), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (2, 3, 2)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 130, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    assert sum(have.values()) == sum(sum(v) for v in PLAN.values())
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert all(29 <= keys[k] <= 36 for k in LETTERS), keys
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_007", "created_at": TODAY,
           "notes": "Package CHE_007_p2: 130 original Chemistry questions (p-block, d- and f-block, coordination "
                    "compounds, organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_007/CHE_007_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
