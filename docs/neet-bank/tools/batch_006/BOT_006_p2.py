"""Builder for BATCH_006, package BOT_006_p2 (Botany, NEET_BOT_001373..NEET_BOT_001500, 128 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Facts already tested in BATCH_000 to BATCH_005 on these topics were avoided or
approached from a new angle (see `python tools/merge_batch.py stems 006 BOT_006_p2`). Numerical answers are
re-derived below; the file is written only if every assert, the plan quota, the format mix and the answer-key
balance pass.

    cd docs/neet-bank && python tools/batch_006/BOT_006_p2.py
"""

import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
BOT = "Botany"
PACKAGE = "BOT_006_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_006_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_006_BOT_p2.json"
FIRST_ID = 1373

AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

PGD = "Plant Growth and Development"
SRFP = "Sexual Reproduction in Flowering Plants"
PIV = "Principles of Inheritance and Variation"
MBI = "Molecular Basis of Inheritance"
MHW = "Microbes in Human Welfare"
OAP = "Organisms and Populations"
ECO = "Ecosystem"
BDC = "Biodiversity and Conservation"

QUESTIONS = []


def ref(cls, chapter, section):
    return f"Class {cls} Biology, '{chapter}', {section}"


def P(correct, wrong, at):
    """Options with the correct text at position `at`."""
    opts = list(wrong)
    assert len(opts) == 3
    opts.insert(LETTERS.index(at), correct)
    assert len(set(opts)) == 4, opts
    return opts, at


def AR(at):
    return list(ASSERTION_REASON), at


def SP(at):
    return list(STATEMENT_PAIR), at


def M(correct, wrong, at):
    """Match-the-list codes with the correct code at position `at` (as match_options() in the sample builder)."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    assert sorted(correct.values()) == sorted(["I", "II", "III", "IV"])
    for w in wrong:
        assert sorted(w.values()) == sorted(["I", "II", "III", "IV"]), w
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4, opts
    return opts, at


def MS(correct, wrong, at):
    """Multi-statement options: each option is a set of statement letters; the correct set goes at `at`."""
    fmt = lambda s: (", ".join(f"({x})" for x in s[:-1]) + f" and ({s[-1]})" if len(s) > 1 else f"({s[0]})") + " only"
    sets = [correct] + list(wrong)
    assert len({tuple(s) for s in sets}) == 4
    return P(fmt(correct), [fmt(w) for w in wrong], at)


def ar(a, r):
    return ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {a}\nReason (R): {r}\n\n"
            "Choose the correct answer from the options given below:")


def sp(s1, s2):
    return (f"Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")


def ml(head, l1, l2):
    a = "\n".join(f"{k}. {t}" for k, t in zip("ABCD", l1))
    b = "\n".join(f"{k}. {t}" for k, t in zip(["I", "II", "III", "IV"], l2))
    return (f"Match List-I ({head[0]}) with List-II ({head[1]}).\n\nList-I:\n{a}\n\nList-II:\n{b}\n\n"
            "Choose the correct answer from the options given below:")


def ms(intro, statements):
    body = "\n".join(f"({k}) {t}" for k, t in zip("abcde", statements))
    return f"{intro}\n\n{body}\n\nChoose the correct answer from the options given below:"


def add(topic, subtopic, difficulty, fmt, text, oa, concept, explanation, steps, ncert,
        shortcut=None, why=None, seconds=45, verified_by=AUTHORED):
    options, answer = oa
    assert answer in LETTERS and len(options) == 4 and ncert
    QUESTIONS.append({
        "question_id": None, "exam_mappings": default_mappings(BOT), "subject": BOT, "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(verified_by), "verified_at": TODAY},
    })







# ================================================================ Plant Growth and Development (3 / 5 / 3)
C11_PGD = lambda s: ref(11, PGD, s)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "According to NCERT, plant growth regulators (PGRs) are best described as:",
    P("Small, simple molecules of diverse chemical composition",
      ["Large proteins that act only inside the cells that synthesise them",
       "Polysaccharides that all share one uniform chemical structure",
       "Nucleic acids that are synthesised only at the root apex"], "B"),
    "Nature of plant growth regulators",
    "NCERT: the plant growth regulators are small, simple molecules of diverse chemical composition. They can be "
    "indole compounds (IAA), adenine derivatives (kinetin), derivatives of carotenoids (abscisic acid), terpenes "
    "(gibberellic acid) or gases (ethylene). They are not large macromolecules and they are not all of one chemical "
    "type.",
    ["PGRs: small, simple molecules", "Chemically diverse: indole compound, adenine derivative, carotenoid "
     "derivative, terpene, gas"],
    C11_PGD("plant growth regulators: characteristics"),
    why="PGRs are not proteins, polysaccharides or nucleic acids, and they are of diverse (not uniform) chemical "
        "nature.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "NCERT notes that because it regulates so many physiological processes, one plant growth regulator is one of the "
    "most widely used PGRs in agriculture. This PGR is:",
    P("Ethylene", ["Abscisic acid", "Kinetin", "Zeatin"], "D"),
    "Agricultural use of ethylene",
    "NCERT: since ethylene regulates so many physiological processes, it is one of the most widely used PGRs in "
    "agriculture. It is applied mostly as ethephon, which releases ethylene slowly inside the plant.",
    ["PGR regulating many processes and widely used in agriculture: ethylene"],
    C11_PGD("plant growth regulators: ethylene"),
    why="Abscisic acid is described as a growth inhibitor and stress hormone; kinetin and zeatin are cytokinins. "
        "None of them is the PGR described in this NCERT line.",
    seconds=20)

add(PGD, "Germination and growth phases", "Basic", "direct",
    "In plants, new cells are always being added to the plant body by the activity of the meristems. NCERT calls this "
    "form of growth:",
    P("The open form of growth",
      ["The closed form of growth", "Arithmetic growth", "Determinate growth"], "C"),
    "Plant growth is generally indeterminate",
    "Plants retain the capacity for unlimited growth throughout their life because of meristems, whose cells can "
    "divide and self-perpetuate. NCERT: this form of growth, wherein new cells are always being added to the plant "
    "body by the activity of the meristem, is called the open form of growth.",
    ["Meristems keep adding new cells", "This is the open form of growth"],
    C11_PGD("growth: plant growth generally is indeterminate"),
    why="Closed or determinate growth stops at maturity, which is not the plant pattern; arithmetic growth is a type "
        "of growth rate (one daughter cell keeps dividing), not the name for this form of growth.",
    seconds=20)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("In deep-water rice plants, the leaves and upper parts of the shoot are able to remain above water.",
       "Ethylene promotes rapid internode or petiole elongation in deep-water rice plants."),
    AR("A"),
    "Ethylene and deep-water rice",
    "NCERT: ethylene promotes rapid internode/petiole elongation in deep-water rice plants, and this helps the leaves "
    "and upper parts of the shoot to remain above water. A is true, R is true, and the elongation stated in R is the "
    "direct cause of the shoot staying above water.",
    ["A: true", "R: true", "Rapid elongation (R) keeps the upper shoot above water (A): R explains A"],
    C11_PGD("plant growth regulators: physiological effects of ethylene"),
    seconds=30)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Ethylene helps plants to increase their absorption surface.",
       "Ethylene promotes root growth and root hair formation."),
    AR("A"),
    "Ethylene and the root system",
    "NCERT: ethylene promotes root growth and root hair formation, thus helping the plants to increase their "
    "absorption surface. Both statements are true; more root growth and more root hairs (R) are the very reason the "
    "absorption surface increases (A).",
    ["A: true", "R: true", "More roots and root hairs give a larger absorbing surface: R explains A"],
    C11_PGD("plant growth regulators: physiological effects of ethylene"),
    seconds=30)

add(PGD, "Differentiation and redifferentiation", "Intermediate", "direct",
    "NCERT points out that the final structure of a cell at maturity is also determined by its location within the "
    "tissue. Which example does it give?",
    P("Cells positioned away from the root apical meristem differentiate as root-cap cells, while those pushed to "
      "the periphery mature as epidermis",
      ["Cells positioned away from the root apical meristem mature as epidermis, while those pushed to the periphery "
       "differentiate as root-cap cells",
       "Cells of the interfascicular region regain the capacity to divide and form interfascicular cambium",
       "Leaves of buttercup produced in air differ in shape from those produced in water"], "B"),
    "Location of a cell decides its final structure",
    "NCERT: development in plants is open; cells and tissues arising from the same meristem have different structures "
    "at maturity, and the final structure is also determined by the location of the cell within the tissue. Example: "
    "cells positioned away from the root apical meristems differentiate as root-cap cells, while those pushed to the "
    "periphery mature as epidermis.",
    ["Same meristem, different fates", "Away from the root apical meristem: root cap", "Pushed to the periphery: "
     "epidermis"],
    C11_PGD("differentiation, dedifferentiation and redifferentiation"),
    why="The first wrong option swaps the two fates. Interfascicular cambium formation is NCERT's example of "
        "dedifferentiation, and buttercup leaves are its example of heterophylly caused by the environment.",
    seconds=40)

add(PGD, "Plant growth regulators", "Intermediate", "direct",
    "Flowering in pineapple is cited in NCERT as an effect of two different plant growth regulators. Which pair?",
    P("Auxin and ethylene",
      ["Gibberellin and abscisic acid", "Cytokinin and gibberellin", "Abscisic acid and ethylene"], "C"),
    "PGRs used in pineapple",
    "Among the effects of auxins, NCERT lists that they promote flowering, e.g. in pineapples. Among the effects of "
    "ethylene, it lists that ethylene is used to initiate flowering and to synchronise fruit-set in pineapples. So "
    "both auxin and ethylene are named for pineapple flowering.",
    ["Auxins: promote flowering, e.g. in pineapple", "Ethylene: initiates flowering and synchronises fruit-set in "
     "pineapple"],
    C11_PGD("plant growth regulators: auxins and ethylene"),
    why="Gibberellins, cytokinins and abscisic acid are not given any role in pineapple flowering in NCERT; abscisic "
        "acid is a general growth inhibitor.",
    seconds=35)

add(PGD, "Germination and growth phases", "Intermediate", "statement_pair",
    sp("Besides giving the turgidity needed for extension growth, water also provides the medium for the enzymatic "
       "activities needed for growth.",
       "Environmental signals such as light and gravity also affect certain phases or stages of plant growth."),
    SP("A"),
    "Conditions for growth",
    "NCERT: plant cells grow in size by cell enlargement, which requires water; turgidity helps extension growth, and "
    "water also provides the medium for enzymatic activities needed for growth (Statement I true). Light and gravity "
    "are named as environmental signals that also affect certain phases/stages of growth (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C11_PGD("growth: conditions for growth"),
    seconds=30)

add(PGD, "Plant growth regulators", "Advanced", "multi_statement",
    ms("Some plant responses are attributed in NCERT to more than one PGR. Which of the following statements are "
       "correct according to NCERT?",
       ["Both gibberellins and cytokinins delay senescence.",
        "Both auxins and ethylene promote abscission (of older leaves and fruits, or of leaves and flowers).",
        "Both abscisic acid and gibberellins promote seed germination.",
        "Both cytokinins and auxins strengthen apical dominance.",
        "Both abscisic acid and ethylene can be regarded as largely inhibitors of growth activities."]),
    MS(["a", "b", "e"], [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
    "Overlapping effects of different PGRs",
    "(a) True: gibberellins delay senescence (fruits can be left on the tree longer) and cytokinins delay leaf "
    "senescence by nutrient mobilisation. (b) True: auxins promote abscission of older mature leaves and fruits, and "
    "ethylene promotes senescence and abscission, especially of leaves and flowers. (c) False: abscisic acid inhibits "
    "seed germination. (d) False: auxins cause apical dominance, but cytokinins help to overcome it. (e) True: ABA is a "
    "general growth inhibitor, and NCERT says ethylene, though it fits either group, is largely an inhibitor of growth "
    "activities.",
    ["(a) true", "(b) true", "(c) false: ABA inhibits germination", "(d) false: cytokinins overcome apical dominance",
     "(e) true"],
    C11_PGD("plant growth regulators: physiological effects"),
    why="Any option with (c) or (d) is wrong; the option (a), (b), (c) leaves out (e).",
    seconds=70)

# Leaf areas (cm²) at the start and end of the same period.
_pgd_leaves = {"P": (2, 3), "Q": (10, 14), "R": (40, 46)}
_pgd_agr = {k: b - a for k, (a, b) in _pgd_leaves.items()}
_pgd_rgr = {k: F(b - a, a) for k, (a, b) in _pgd_leaves.items()}
assert _pgd_agr == {"P": 1, "Q": 4, "R": 6}
assert _pgd_rgr == {"P": F(1, 2), "Q": F(2, 5), "R": F(3, 20)}
assert max(_pgd_agr, key=_pgd_agr.get) == "R" and max(_pgd_rgr, key=_pgd_rgr.get) == "P"

add(PGD, "Growth rate", "Advanced", "numerical",
    "In the same period, three leaves grow as follows: leaf P from 2 cm² to 3 cm², leaf Q from 10 cm² to 14 cm² and "
    "leaf R from 40 cm² to 46 cm². Which leaf has the highest absolute growth rate and which has the highest relative "
    "growth rate, respectively?",
    P("R and P", ["P and R", "R and R", "Q and P"], "B"),
    "Absolute versus relative growth rate",
    "Absolute growth rate is the total growth per unit time: P = 1, Q = 4 and R = 6 cm², so R is highest. Relative "
    "growth rate is the growth per unit time expressed on a common basis, e.g. per unit initial parameter: P = 1/2 = "
    "50%, Q = 4/10 = 40%, R = 6/40 = 15%, so P is highest.",
    ["Absolute: P 1, Q 4, R 6 cm² → R highest", "Relative: P 50%, Q 40%, R 15% → P highest"],
    C11_PGD("growth: growth rates"),
    shortcut="A small leaf with a modest gain can still have the highest relative growth rate.",
    why="'P and R' swaps the two rates; 'R and R' treats the relative rate like the absolute one; 'Q and P' picks the "
        "middle leaf for absolute growth.",
    seconds=70, verified_by=RECOMPUTED)

# W1 = W0 e^(rt): 3 g -> 12 g in 10 days; ln 4 = 2 ln 2.
_pgd_r = 2 * 0.693 / 10
_pgd_w15 = 3 * math.exp(_pgd_r * 15)
assert abs(_pgd_r - 0.1386) < 1e-9 and abs(_pgd_w15 - 24) < 0.05
assert abs(12 + 0.9 * 5 - 16.5) < 1e-9                                  # distractor: linear extrapolation

add(PGD, "Growth rate", "Advanced", "numerical",
    "A plant tissue grows geometrically according to W₁ = W₀e^(rt). Its mass rises from 3 g to 12 g in 10 days. "
    "Taking ln 2 = 0.693, what is its relative growth rate r, and what mass is expected at the end of 15 days if the "
    "same growth continues?",
    P("r ≈ 0.139 per day; 24 g",
      ["r ≈ 0.139 per day; 16.5 g", "r = 0.4 per day; 24 g", "r ≈ 0.139 per day; 48 g"], "A"),
    "Exponential (geometric) growth",
    "12/3 = 4 = e^(10r), so 10r = ln 4 = 2 × 0.693 = 1.386 and r ≈ 0.1386 per day. Mass doubles every ln 2/r = 5 days; "
    "15 days is three doublings, so W = 3 × 2³ = 24 g (equivalently 3 × e^(0.1386 × 15) = 3 × e^2.079 = 24 g).",
    ["e^(10r) = 4 → r = 1.386/10 ≈ 0.139 per day", "Doubling time = 0.693/0.1386 = 5 days",
     "15 days = 3 doublings → 3 × 8 = 24 g"],
    C11_PGD("growth: growth rates (geometric growth)"),
    shortcut="Fourfold in 10 days means doubling every 5 days; 15 days = 2³.",
    why="16.5 g extends the growth linearly (0.9 g per day), which is arithmetic, not geometric, growth; 0.4 per day "
        "divides the fold change by time instead of taking its logarithm; 48 g applies another fourfold increase to "
        "the 12 g mass in only 5 days.",
    seconds=90, verified_by=RECOMPUTED)



# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "A typical angiosperm anther is bilobed, and each lobe has two theca. According to NCERT, what often runs "
    "lengthwise along the anther, separating the theca?",
    P("A longitudinal groove", ["The filament", "The connective tissue of the tapetum", "A transverse septum"], "A"),
    "Structure of the anther",
    "NCERT: a typical angiosperm anther is bilobed with each lobe having two theca, i.e. it is dithecous. Often a "
    "longitudinal groove runs lengthwise separating the theca.",
    ["Anther: bilobed, dithecous", "A longitudinal groove separates the theca"],
    C12_SR("pre-fertilisation: stamen, microsporangium and pollen grain"),
    why="The filament is the stalk of the stamen; the tapetum is the innermost wall layer of a microsporangium; the "
        "groove runs lengthwise, not across the anther.",
    seconds=20)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Basic", "direct",
    "The ability of the pistil to recognise the pollen, followed by its acceptance or rejection, is the result of a "
    "continuous dialogue between the pollen grain and the pistil. According to NCERT, this dialogue is mediated by:",
    P("Chemical components of the pollen interacting with those of the pistil",
      ["Electrical impulses passing from the stigma to the ovule",
       "The pollinating agent that carried the pollen to the stigma",
       "Light signals received by the pollen grain"], "C"),
    "Pollen-pistil interaction",
    "NCERT: the pistil can recognise compatible and incompatible pollen. This recognition, and the acceptance or "
    "rejection that follows, results from a continuous dialogue between pollen grain and pistil, mediated by chemical "
    "components of the pollen interacting with those of the pistil.",
    ["Recognition = dialogue between pollen and pistil", "Mediated by chemical components of both"],
    C12_SR("pre-fertilisation: pollination, pollen-pistil interaction"),
    why="NCERT does not attribute the recognition to electrical or light signals, and the pollinating agent only "
        "transfers the pollen; it has no role in the recognition.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "direct",
    "Orchid fruits contain thousands of tiny seeds. According to NCERT, the same is true of the fruits of some "
    "parasitic species such as:",
    P("Orobanche and Striga", ["Cuscuta and Rafflesia", "Lupinus and Phoenix", "Vallisneria and Hydrilla"], "D"),
    "Number of seeds in a fruit",
    "NCERT: orchid fruits contain thousands of tiny seeds; similar is the case of fruits of some parasitic species "
    "such as Orobanche and Striga.",
    ["Orchids and the parasites Orobanche and Striga: thousands of tiny seeds per fruit"],
    C12_SR("post-fertilisation: seed"),
    why="Cuscuta and Rafflesia are not the examples NCERT gives here; Lupinus arcticus and Phoenix dactylifera are its "
        "examples of long seed viability; Vallisneria and Hydrilla are water-pollinated plants.",
    seconds=20)

add(SRFP, "Pollination", "Basic", "direct",
    "Which type of pollination is functionally cross-pollination because it involves a pollinating agent, but is "
    "genetically similar to autogamy because the pollen comes from the same plant?",
    P("Geitonogamy", ["Xenogamy", "Cleistogamy", "Chasmogamy"], "B"),
    "Kinds of pollination",
    "Geitonogamy is the transfer of pollen grains from the anther to the stigma of another flower of the same plant. "
    "NCERT: although it is functionally cross-pollination involving a pollinating agent, it is genetically similar to "
    "autogamy, since the pollen grains come from the same plant.",
    ["Another flower, same plant: geitonogamy", "Needs an agent (functionally cross-pollination); same genotype "
     "(genetically like autogamy)"],
    C12_SR("pre-fertilisation: pollination, kinds of pollination"),
    why="Xenogamy brings pollen from a different plant (genetically different); cleistogamous flowers never open and "
        "are autogamous; chasmogamous flowers are open flowers, not a type of pollen transfer.",
    seconds=25)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "In a mature two-celled pollen grain, the vegetative cell is:",
    P("Bigger than the generative cell, with abundant food reserve and a large, irregularly shaped nucleus",
      ["Smaller than the generative cell and spindle-shaped, floating in the cytoplasm of the generative cell",
       "Bigger than the generative cell but without any nucleus",
       "Equal in size to the generative cell, and divides to form the two male gametes"], "A"),
    "Cells of the pollen grain",
    "NCERT: a mature pollen grain contains two cells. The vegetative cell is bigger, has abundant food reserve and a "
    "large irregularly shaped nucleus. The generative cell is small and floats in the cytoplasm of the vegetative "
    "cell; it is spindle-shaped with dense cytoplasm and a nucleus, and it is the generative cell that divides to "
    "give the two male gametes.",
    ["Vegetative cell: bigger, abundant food reserve, large irregular nucleus", "Generative cell: small, "
     "spindle-shaped, divides to give two male gametes"],
    C12_SR("pre-fertilisation: stamen, microsporangium and pollen grain"),
    why="The first wrong option describes the generative cell (and reverses which one floats in which); the vegetative "
        "cell has a nucleus; the generative cell, not the vegetative cell, gives the male gametes.",
    seconds=30)

add(SRFP, "Pollination", "Basic", "match_list",
    ml(("floral feature", "flowers in which NCERT describes it"),
       ["Not very colourful and do not produce nectar",
        "Pollen grains protected from wetting by a mucilaginous covering",
        "Large, colourful, fragrant and rich in nectar (in the majority)",
        "A single ovule in each ovary and numerous flowers packed into an inflorescence"],
       ["Insect-pollinated flowers", "Water-pollinated flowers", "Wind-pollinated flowers",
        "Both wind-pollinated and water-pollinated flowers"]),
    M({"A": "IV", "B": "II", "C": "I", "D": "III"},
      [{"A": "III", "B": "II", "C": "I", "D": "IV"},
       {"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "I", "B": "II", "C": "IV", "D": "III"}], "C"),
    "Floral features and agents of pollination",
    "NCERT: both wind- and water-pollinated flowers are not very colourful and do not produce nectar (A-IV). In most "
    "water-pollinated species, pollen grains are protected from wetting by a mucilaginous covering (B-II). The "
    "majority of insect-pollinated flowers are large, colourful, fragrant and rich in nectar (C-I). Wind-pollinated "
    "flowers often have a single ovule in each ovary and numerous flowers packed into an inflorescence (D-III).",
    ["A-IV", "B-II", "C-I", "D-III"],
    C12_SR("pre-fertilisation: pollination, agents of pollination"),
    why="The other codes give the shared feature (no colour, no nectar) to wind pollination alone, or swap the water- "
        "and wind-pollination features.",
    seconds=40)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "NCERT notes that most zygotes divide only after a certain amount of endosperm has formed. It explains this as:",
    P("An adaptation to provide assured nutrition to the developing embryo",
      ["A mechanism to prevent the formation of more than one embryo in a seed",
       "A consequence of the zygote being triploid",
       "A way to ensure that the endosperm is completely consumed before the seed matures"], "D"),
    "Timing of embryo development",
    "The embryo develops at the micropylar end of the embryo sac where the zygote is situated. NCERT: most zygotes "
    "divide only after a certain amount of endosperm is formed; this is an adaptation to provide assured nutrition to "
    "the developing embryo.",
    ["Endosperm forms first", "Zygote divides later", "Purpose: assured nutrition for the embryo"],
    C12_SR("post-fertilisation: embryo"),
    why="The timing has nothing to do with polyembryony; the zygote is diploid, not triploid; and many seeds (wheat, "
        "castor) keep part of the endosperm at maturity.",
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "multi_statement",
    ms("Which of the following are advantages of seeds to angiosperms, as given in NCERT?",
       ["Since pollination and fertilisation are independent of water, seed formation is more dependable.",
        "Seeds have better adaptive strategies for dispersal to new habitats and help the species to colonise other "
        "areas.",
        "Seeds have sufficient food reserves, so young seedlings are nourished until they are capable of "
        "photosynthesis.",
        "The seed coat is thin and offers no protection to the young embryo.",
        "Mature seeds retain a high water content, which is crucial for their storage."]),
    MS(["a", "b", "c"], [["a", "b", "e"], ["b", "c", "d"], ["a", "c", "d", "e"]], "B"),
    "Advantages of seeds",
    "NCERT lists these advantages: (a) reproductive processes like pollination and fertilisation are independent of "
    "water, so seed formation is more dependable; (b) seeds have better adaptive strategies for dispersal to new "
    "habitats; (c) their food reserves nourish young seedlings until they can photosynthesise. (d) is false: the hard "
    "seed coat protects the young embryo. (e) is false: dehydration of mature seeds (about 10–15% moisture) is what "
    "makes their storage possible.",
    ["(a), (b), (c): true", "(d): false, hard seed coat protects", "(e): false, mature seeds are dehydrated"],
    C12_SR("post-fertilisation: seed"),
    why="Every other option includes (d) or (e).",
    seconds=55)

add(SRFP, "Endosperm and embryo", "Intermediate", "assertion_reason",
    ar("Seeds of crop plants can be stored and used as food throughout the year and to raise a crop in the next "
       "season.",
       "Being products of sexual reproduction, seeds generate new genetic combinations leading to variations."),
    AR("B"),
    "Seeds as the basis of agriculture",
    "Both statements are NCERT lines about seeds. A is true: seeds are the basis of agriculture and can be stored for "
    "use as food and for raising the next crop; NCERT links this to the dehydration of mature seeds. R is also true, "
    "but it describes a different advantage of seeds (variation); generating new genetic combinations is not why seeds "
    "can be stored. So R does not explain A.",
    ["A: true (storage is possible because mature seeds are dehydrated)", "R: true (seeds give variation)",
     "R is a separate property: not the explanation"],
    C12_SR("post-fertilisation: seed"),
    seconds=35)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "direct",
    "In a species whose pollen grains are shed at the 3-celled stage, the pollen grain at the time of shedding "
    "contains:",
    P("One vegetative cell and two male gametes",
      ["One vegetative cell, one generative cell and one tube cell",
       "Three male gametes",
       "One generative cell and two vegetative cells"], "D"),
    "Two-celled and three-celled pollen",
    "The microspore divides to give the vegetative and the generative cell. In over 60% of angiosperms pollen is shed "
    "at this 2-celled stage. In the remaining species, the generative cell divides mitotically to give two male "
    "gametes before pollen is shed, so the pollen grain is 3-celled: one vegetative cell and two male gametes.",
    ["Microspore → vegetative + generative cell", "Generative cell → 2 male gametes",
     "3-celled pollen = vegetative cell + 2 male gametes"],
    C12_SR("pre-fertilisation: stamen, microsporangium and pollen grain"),
    why="A separate 'tube cell' in addition to the vegetative cell is not formed; there are only two male gametes; "
        "there is only one vegetative cell.",
    seconds=30)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "statement_pair",
    sp("Hybrid seeds have to be produced every year, and the production of hybrid seed is costly, so the cost of "
       "hybrid seeds becomes too expensive for farmers.",
       "If the seeds collected from hybrid plants are sown, the progeny maintain all the hybrid characters."),
    SP("C"),
    "Why apomixis matters to the hybrid-seed industry",
    "NCERT: hybrid seeds have to be produced every year, and the cost of hybrid seed is too expensive for farmers "
    "(Statement I true). If the seeds collected from hybrids are sown, the plants in the progeny will segregate and "
    "will not maintain the hybrid characters (Statement II false). This is why making hybrids into apomicts is of "
    "interest.",
    ["Statement I: true", "Statement II: false, the progeny segregate"],
    C12_SR("apomixis and polyembryony"),
    seconds=30)

add(SRFP, "Pollination", "Intermediate", "statement_pair",
    sp("Much before the actual flower is seen on a plant, the decision that the plant is going to flower has already "
       "taken place.",
       "In the flower, the androecium and the gynoecium, the male and female reproductive structures, differentiate "
       "and develop."),
    SP("A"),
    "Pre-fertilisation events in the flower",
    "NCERT: much before the actual flower is seen on a plant, the decision that the plant is going to flower has "
    "taken place; several hormonal and structural changes are initiated which lead to the differentiation and "
    "development of the floral primordium (Statement I true). Inflorescences bear the floral buds and then the "
    "flowers, in which the androecium and gynoecium differentiate and develop (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_SR("pre-fertilisation: structures and events"),
    seconds=30)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("In an animal-pollinated flower, the body of the visiting animal gets a coating of pollen grains.",
       "To harvest the floral reward, the animal visitor comes in contact with the anthers and the stigma."),
    AR("A"),
    "How animals pick up pollen",
    "NCERT: to harvest the reward from the flower, the animal visitor comes in contact with the anthers and the "
    "stigma; the body of the animal gets a coating of pollen grains, which are generally sticky in animal-pollinated "
    "flowers. Both are true, and the contact made while collecting the reward (R) is what coats the animal with pollen "
    "(A).",
    ["A: true", "R: true", "Contact with anthers during reward collection causes the coating: R explains A"],
    C12_SR("pre-fertilisation: pollination, agents of pollination"),
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "Albuminous seeds retain a part of the endosperm because it is not completely used up during embryo development. "
    "Which pair of plants, both named in NCERT, has albuminous seeds?",
    P("Maize and barley", ["Pea and groundnut", "Pea and maize", "Groundnut and barley"], "B"),
    "Albuminous and non-albuminous seeds",
    "NCERT: non-albuminous seeds have no residual endosperm, as it is completely consumed during embryo development "
    "(pea, groundnut). Albuminous seeds retain a part of the endosperm (wheat, maize, barley, castor).",
    ["Albuminous: wheat, maize, barley, castor", "Non-albuminous: pea, groundnut"],
    C12_SR("post-fertilisation: seed"),
    why="Pea and groundnut are NCERT's non-albuminous examples, so any pair containing either is wrong.",
    seconds=25)

# Nuclear division events (one nucleus dividing once = one event).
_sr_sac = sum(2 ** k for k in range(3))          # 1 + 2 + 4 free-nuclear divisions to reach 8 nuclei
_sr_pollen = 4 * 2                               # 4 microspores; each: microspore -> veg + gen, gen -> 2 gametes
assert _sr_sac == 7 and 2 ** 3 == 8 and _sr_pollen == 8 and _sr_sac + _sr_pollen == 15
assert 3 + 2 == 5 and 3 + 8 == 11 and 7 + 2 == 9                            # distractors

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "numerical",
    "Count every division of a single nucleus as one mitotic division event. Starting from (i) the functional megaspore "
    "of one ovule, which forms a typical mature embryo sac, and (ii) the four microspores formed from one pollen "
    "mother cell, each of which forms a pollen grain that produces two male gametes, how many mitotic division events "
    "take place in all?",
    P("15", ["5", "11", "9"], "C"),
    "Counting divisions in gametophyte development",
    "Embryo sac: the megaspore nucleus divides once (2 nuclei), then two more sequential free-nuclear divisions give "
    "4 and then 8 nuclei; each round doubles the number of nuclei, so the events are 1 + 2 + 4 = 7. Pollen: each "
    "microspore nucleus divides once (vegetative + generative cell) and the generative cell divides once more (two "
    "male gametes): 2 events per microspore × 4 = 8. Total = 7 + 8 = 15.",
    ["Embryo sac: 1 + 2 + 4 = 7 events", "Male side: 2 events × 4 microspores = 8", "Total = 15"],
    C12_SR("pre-fertilisation: megasporogenesis, female gametophyte and pollen grain"),
    shortcut="Going from 1 nucleus to n nuclei by mitosis always takes n − 1 division events: 8 − 1 = 7; each "
             "microspore goes to 3 nuclei, 3 − 1 = 2.",
    why="5 counts rounds of division (3) instead of events and only one pollen grain (2); 11 counts rounds for the "
        "embryo sac (3) but events for four pollen grains (8); 9 counts the embryo sac correctly but only one pollen "
        "grain.",
    seconds=100, verified_by=RECOMPUTED)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Advanced", "direct",
    "In a Citrus seed, one embryo is zygotic and two others have developed from nucellar cells that protruded into the "
    "embryo sac. The nucellar embryos are expected to be genetically:",
    P("Identical to the mother plant, since they arise from its diploid nucellar cells without fertilisation",
      ["Identical to the zygotic embryo in the same seed",
       "Haploid, since they arise from cells of the female gametophyte",
       "Triploid, since they develop alongside the endosperm"], "C"),
    "Nucellar polyembryony as apomixis",
    "In many Citrus and mango varieties, some nucellar cells surrounding the embryo sac divide, protrude into the "
    "embryo sac and develop into embryos. The nucellus is diploid tissue of the ovule, i.e. of the mother sporophyte. "
    "Since no meiosis or fertilisation is involved (apomixis is a form of asexual reproduction that mimics sexual "
    "reproduction), the nucellar embryos carry the mother plant's genotype. The zygotic embryo, formed by fusion of "
    "egg and male gamete, carries paternal genes too.",
    ["Nucellus = diploid maternal tissue", "No meiosis, no fertilisation", "Nucellar embryo = copy of the mother "
     "plant's genotype"],
    C12_SR("apomixis and polyembryony"),
    why="The zygotic embryo has a paternal contribution, so it differs; nucellar cells are not part of the haploid "
        "female gametophyte; ploidy is not determined by nearness to the endosperm.",
    seconds=50)

add(SRFP, "Double fertilisation", "Advanced", "direct",
    "A plant of genotype aa (female parent) is pollinated with pollen from a plant of genotype Aa. In one particular "
    "seed, the embryo is found to be Aa. Assuming normal double fertilisation, the endosperm of that same seed must be:",
    P("aaA, because both male gametes of a pollen grain arise by mitosis from one generative cell and carry the "
      "same allele",
      ["aaa, because the endosperm receives no paternal allele",
       "aaA or aaa with equal probability, because the two male gametes are formed independently",
       "AAa, because the endosperm receives two paternal alleles"], "D"),
    "Genetic identity of the two male gametes",
    "The embryo Aa received A from the male gamete that fused with the egg (the egg is a). Both male gametes delivered "
    "by one pollen tube come from mitotic division of the same generative cell of one pollen grain, so the second male "
    "gamete also carries A. It fuses with the two polar nuclei (a + a), giving a triploid endosperm aaA.",
    ["Embryo Aa: the male gamete fusing with the egg carried A", "Both male gametes of one pollen grain are mitotic "
     "products: both A", "Endosperm = a + a + A = aaA"],
    C12_SR("double fertilisation"),
    why="The endosperm does receive one paternal set (triple fusion); the two male gametes are not independent; the "
        "endosperm gets two maternal sets (polar nuclei) and only one paternal set.",
    seconds=70)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "direct",
    "Which pair of devices prevents both autogamy and geitonogamy?",
    P("Dioecy, as in papaya, and self-incompatibility",
      ["Dioecy, as in papaya, and monoecy, as in castor",
       "Self-incompatibility, and placing the anther and stigma at different positions in the flower",
       "Cleistogamy and monoecy, as in maize"], "B"),
    "Comparing outbreeding devices",
    "Monoecy (castor, maize) prevents autogamy but not geitonogamy. Dioecy (papaya) prevents both, since a plant bears "
    "flowers of only one sex. Self-incompatibility is a genetic mechanism that prevents self-pollen, from the same "
    "flower or from other flowers of the same plant, from fertilising the ovules, so it also blocks both. Placing "
    "anther and stigma at different positions acts only within a flower, and cleistogamous flowers are invariably "
    "autogamous.",
    ["Dioecy: prevents autogamy and geitonogamy", "Self-incompatibility: self-pollen of the same flower or other "
     "flowers of the same plant rejected", "Monoecy and anther-stigma placement: autogamy only; cleistogamy: ensures "
     "autogamy"],
    C12_SR("outbreeding devices"),
    why="Each wrong pair contains monoecy, anther-stigma placement or cleistogamy, none of which prevents "
        "geitonogamy.",
    seconds=55)

add(SRFP, "Endosperm and embryo", "Advanced", "statement_pair",
    sp("The endosperm that persists in a mature castor seed and the perisperm present in a beet seed differ in "
       "ploidy.",
       "Both the endosperm and the perisperm are formed as a result of fertilisation."),
    SP("C"),
    "Endosperm versus perisperm",
    "The endosperm develops from the primary endosperm cell formed by triple fusion, so it is triploid (3n); castor is "
    "an albuminous seed that keeps part of it. Perisperm, in black pepper and beet, is the residual, persistent "
    "nucellus, a diploid (2n) maternal tissue. So they differ in ploidy (Statement I true). Perisperm is a remnant of "
    "the nucellus and is not a product of fertilisation (Statement II false).",
    ["Endosperm: 3n, from triple fusion", "Perisperm: 2n, residual nucellus", "Statement I true; Statement II false"],
    C12_SR("post-fertilisation: endosperm and seed"),
    seconds=45)

# Fruit with 30 seeds, one ovule and one pollen tube per seed, one MMC per ovule.
_sr_seeds = 30
assert _sr_seeds * 2 == 60 and math.ceil(_sr_seeds / 4) == 8 < _sr_seeds

add(SRFP, "Double fertilisation", "Advanced", "multi_statement",
    ms("A fruit contains 30 seeds. Each seed developed from a separate ovule (with a single megaspore mother cell) by "
       "normal double fertilisation, and one pollen tube entered each ovule. Which of the following statements are "
       "correct?",
       ["At least 30 pollen grains germinated on the stigma.",
        "In all, 60 male gametes were released into the embryo sacs.",
        "At least 30 megaspore mother cells underwent meiosis.",
        "At least 30 pollen mother cells must have undergone meiosis.",
        "The fruit developed from 30 separate ovaries."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "D"),
    "Counting the events behind seed formation",
    "(a) True: each ovule received its own pollen tube, so at least 30 pollen grains germinated. (b) True: each pollen "
    "tube releases two male gametes into the embryo sac (one for syngamy, one for triple fusion): 30 × 2 = 60. (c) "
    "True: each ovule's embryo sac came from a megaspore produced by meiosis of its megaspore mother cell. (d) False: "
    "one pollen mother cell gives four pollen grains, so 30 pollen grains need only 8 pollen mother cells (30/4, "
    "rounded up). (e) False: the ovules of one ovary develop into the seeds of one fruit.",
    ["(a) true: one pollen tube per ovule", "(b) true: 2 × 30 = 60", "(c) true: one MMC per ovule",
     "(d) false: 8 PMCs give 32 pollen grains", "(e) false: one ovary, many ovules"],
    C12_SR("pre-fertilisation and double fertilisation"),
    why="Options with (d) forget that each pollen mother cell yields four pollen grains; options with (e) confuse "
        "ovules (which become seeds) with the ovary (which becomes the fruit); 'b, c and e' also leaves out (a).",
    seconds=90, verified_by=RECOMPUTED)



# ================================================================ Principles of Inheritance and Variation (7 / 10 / 7)
C12_PI = lambda s: ref(12, PIV, s)


def _cross(p1, p2):
    """Offspring genotype distribution for diploid crosses written as allele-pair strings, e.g. 'RrYy'."""
    loci1 = [p1[i:i + 2] for i in range(0, len(p1), 2)]
    loci2 = [p2[i:i + 2] for i in range(0, len(p2), 2)]
    out = Counter()
    for g1 in product(*loci1):
        for g2 in product(*loci2):
            out[tuple("".join(sorted(a + b)) for a, b in zip(g1, g2))] += 1
    return out


def _pheno_ratio(p1, p2):
    """Phenotype counts (complete dominance, upper case dominant) as a sorted ratio tuple, largest first."""
    ph = Counter()
    for g, n in _cross(p1, p2).items():
        ph[tuple(any(c.isupper() for c in locus) for locus in g)] += n
    vals = sorted(ph.values(), reverse=True)
    from math import gcd
    from functools import reduce
    d = reduce(gcd, vals)
    return tuple(v // d for v in vals)


add(PIV, "Mendelian inheritance", "Basic", "direct",
    "To determine the genotype of a tall pea plant, it is crossed with a dwarf (recessive) plant. Crossing an organism "
    "showing the dominant phenotype with the recessive parent in this way is called a:",
    P("Test cross", ["Back-mutation", "Reciprocal cross", "Dihybrid cross"], "C"),
    "Test cross",
    "NCERT: in a typical test cross, an organism showing a dominant phenotype (whose genotype is to be determined) is "
    "crossed with the recessive parent instead of being self-crossed. The progeny ratios then reveal the genotype: all "
    "dominant if the plant is homozygous, 1 : 1 if it is heterozygous.",
    ["Dominant phenotype × recessive parent", "Name: test cross"],
    C12_PI("inheritance of one gene: test cross"),
    why="A reciprocal cross exchanges the sexes of the two parents; a dihybrid cross involves two characters; "
        "'back-mutation' is not a type of cross.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "statement_pair",
    sp("Mendel published his work on the inheritance of characters in 1865, but it remained unrecognised till 1900.",
       "The 'factors' that Mendel proposed are now called genes."),
    SP("A"),
    "Mendel's work and his factors",
    "NCERT: Mendel published his work on inheritance of characters in 1865, but for several reasons it remained "
    "unrecognised till 1900, when it was rediscovered (Statement I true). Mendel's 'factors', which are passed down "
    "unchanged from parent to offspring through the gametes, are now called genes (Statement II true).",
    ["Statement I: true (1865; recognised from 1900)", "Statement II: true (factors = genes)"],
    C12_PI("Mendel's laws of inheritance; chromosomal theory of inheritance"),
    seconds=25)

add(PIV, "Sex determination", "Basic", "match_list",
    ml(("human cell or individual", "chromosome complement"),
       ["Ovum of a normal woman", "Somatic cell of a normal man", "Somatic cell of a person with Turner's syndrome",
        "Somatic cell of a person with Klinefelter's syndrome"],
       ["44 autosomes + XXY", "22 autosomes + X", "44 autosomes + XO", "44 autosomes + XY"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "IV", "B": "II", "C": "III", "D": "I"},
       {"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "II", "B": "III", "C": "IV", "D": "I"}], "D"),
    "Chromosome complements in normal and aneuploid humans",
    "Humans have 22 pairs of autosomes plus the sex chromosomes. A normal man is 44 + XY. A woman is 44 + XX, and "
    "meiosis gives every ovum 22 + X. Turner's syndrome is caused by the absence of one X chromosome (45, with XO), "
    "and Klinefelter's syndrome by an additional X chromosome (47, XXY).",
    ["A-II (n = 23)", "B-IV (46)", "C-III (45)", "D-I (47)"],
    C12_PI("sex determination; chromosomal disorders"),
    why="The other codes confuse the haploid ovum with a diploid cell, or swap the Turner (XO) and Klinefelter (XXY) "
        "karyotypes.",
    seconds=35)

add(PIV, "Incomplete and co-dominance", "Basic", "direct",
    "When the F1 phenotype does not resemble either of the two parents but is in between the two, the phenomenon is "
    "called:",
    P("Incomplete dominance", ["Co-dominance", "Pleiotropy", "Polygenic inheritance"], "B"),
    "Deviations from Mendel's dominance",
    "NCERT: in incomplete dominance the F1 has a phenotype that does not resemble either parent and is in between the "
    "two, as in snapdragon (pink F1 from red × white). In co-dominance the F1 resembles both parents (blood group AB).",
    ["F1 in between both parents → incomplete dominance"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    why="In co-dominance the F1 resembles both parents; pleiotropy is one gene affecting several traits; polygenic "
        "inheritance is one trait controlled by several genes.",
    seconds=20)

_pi_f2 = 640
assert _pi_f2 * F(1, 2) == 320 and _pi_f2 * F(1, 4) == 160 and _pi_f2 * F(3, 4) == 480

add(PIV, "Mendelian inheritance", "Basic", "numerical",
    "True-breeding tall (TT) and dwarf (tt) pea plants are crossed, and the F1 plants are self-pollinated. Out of 640 "
    "F2 plants, how many are expected to be heterozygous tall (Tt)?",
    P("320", ["160", "480", "213"], "D"),
    "Monohybrid F2 genotypic ratio",
    "F1 Tt × Tt gives the F2 genotypic ratio 1 TT : 2 Tt : 1 tt. Heterozygotes are 2/4 = 1/2 of the F2: 640 × 1/2 = "
    "320.",
    ["F2 genotypes: 1 TT : 2 Tt : 1 tt", "Tt = 1/2 × 640 = 320"],
    C12_PI("inheritance of one gene"),
    why="160 is the number of TT (or tt) plants; 480 counts all tall plants (TT + Tt); 213 takes 1/3 instead of 1/2.",
    seconds=30, verified_by=RECOMPUTED)

_pi_tc = _cross("AaBb", "aabb")
assert _pi_tc[("aa", "bb")] * 800 // sum(_pi_tc.values()) == 200

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "A plant of genotype AaBb, in which the two genes assort independently, is test-crossed with aabb, and 800 progeny "
    "are obtained. How many are expected to be aabb?",
    P("200", ["50", "450", "400"], "A"),
    "Dihybrid test cross",
    "AaBb forms four kinds of gametes, AB, Ab, aB and ab, in equal proportion; aabb gives only ab. So the progeny are "
    "AaBb, Aabb, aaBb and aabb in a 1 : 1 : 1 : 1 ratio, and aabb = 800/4 = 200.",
    ["Gametes of AaBb: 4 kinds, 1/4 each", "aabb = 1/4 × 800 = 200"],
    C12_PI("inheritance of two genes"),
    why="50 uses 1/16, the F2 fraction of aabb in a selfed dihybrid; 450 uses 9/16; 400 uses 1/2.",
    seconds=30, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Basic", "match_list",
    ml(("phenomenon", "NCERT example"),
       ["Incomplete dominance", "Co-dominance", "Pleiotropy", "Polygenic inheritance"],
       ["Phenylketonuria", "Human skin colour", "Flower colour in snapdragon", "ABO blood groups"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
    "Examples of non-Mendelian patterns",
    "Snapdragon flower colour (pink F1) shows incomplete dominance; the ABO blood groups (Iᴬ and Iᴮ both expressed in "
    "AB) show co-dominance; phenylketonuria (one gene, several phenotypic effects) is NCERT's example of pleiotropy; "
    "human skin colour is its example of polygenic inheritance.",
    ["A-III", "B-IV", "C-I", "D-II"],
    C12_PI("inheritance of one gene; polygenic inheritance; pleiotropy"),
    why="The other codes swap incomplete dominance with co-dominance, or pleiotropy with polygenic inheritance.",
    seconds=35)

_pi_snap = _cross("Rr", "Rr")
assert F(_pi_snap[("RR",)] + _pi_snap[("rr",)], sum(_pi_snap.values())) == F(1, 2)

add(PIV, "Incomplete and co-dominance", "Intermediate", "direct",
    "In snapdragon, red (RR) × white (rr) gives pink F1 plants, and the F1 is self-pollinated. What fraction of the F2 "
    "plants will breed true (give only their own flower colour) on self-pollination?",
    P("1/2", ["1/4", "3/4", "None of them"], "B"),
    "True-breeding plants under incomplete dominance",
    "Rr × Rr gives 1 RR (red) : 2 Rr (pink) : 1 rr (white). Only homozygotes breed true: red RR and white rr, which "
    "together are 1/4 + 1/4 = 1/2. Pink plants (Rr) segregate again into red, pink and white.",
    ["F2: 1 RR : 2 Rr : 1 rr", "Homozygous (true-breeding) = RR + rr = 1/2"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    shortcut="With incomplete dominance each phenotype shows its genotype: red and white breed true, pink does not.",
    why="1/4 counts only one homozygous class; 3/4 includes pink heterozygotes, which do not breed true; 'none' "
        "ignores the homozygous red and white plants.",
    seconds=40, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Intermediate", "assertion_reason",
    ar("Red-green colour blindness is much rarer in females than in males.",
       "A daughter will normally not be colour blind unless her mother is a carrier (or colour blind) and her father "
       "is colour blind."),
    AR("A"),
    "Why colour blindness is rare in women",
    "The gene for colour blindness is X-linked recessive. A male, with one X, is colour blind whenever his single X "
    "carries the allele. A female needs the allele on both X chromosomes, one from each parent: NCERT notes that the "
    "daughter will not normally be colour blind unless her mother is a carrier and her father is colour blind. This "
    "stringent requirement (R) is why colour blindness is much rarer in females (A).",
    ["A: true (about 8% of males, 0.4% of females)", "R: true", "Female must inherit the allele from both parents: "
     "R explains A"],
    C12_PI("sex-linked inheritance: colour blindness"),
    seconds=35)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "direct",
    "A mother has blood group A, and her child has blood group AB. The child's biological father could have blood "
    "group:",
    P("B or AB only", ["AB only", "A, B or AB", "O or B"], "D"),
    "Inferring a parent's ABO group",
    "Blood group AB is IᴬIᴮ, one allele from each parent. A group-A mother (IᴬIᴬ or Iᴬi) can give only Iᴬ or i, so "
    "the child's Iᴮ must have come from the father. Fathers carrying Iᴮ have blood group B (IᴮIᴮ or Iᴮi) or AB "
    "(IᴬIᴮ).",
    ["Child IᴬIᴮ", "Mother (group A) cannot give Iᴮ", "Father must carry Iᴮ: group B or AB"],
    C12_PI("inheritance of one gene: co-dominance, multiple alleles"),
    why="'AB only' forgets that a group-B father also carries Iᴮ; a group-A or group-O father has no Iᴮ to give.",
    seconds=40)

add(PIV, "Sex-linked inheritance", "Intermediate", "direct",
    "Two parents with normal colour vision have a colour-blind son. For their next child, if it is a daughter, what "
    "are the probabilities that she is colour blind and that she is a carrier, respectively?",
    P("0 and 1/2", ["1/2 and 1/2", "1/4 and 1/4", "0 and 1"], "C"),
    "X-linked recessive inheritance",
    "The son's X chromosome (carrying the allele) came from his mother, so the normal mother is a carrier (XᶜX). The "
    "father is normal (XY) and always gives his normal X to a daughter. A daughter therefore gets the father's normal X "
    "plus either the mother's normal X or her X carrying the allele: never colour blind, carrier with probability 1/2.",
    ["Mother: carrier (son got the X from her)", "Father: normal X to every daughter",
     "Daughter: colour blind 0; carrier 1/2"],
    C12_PI("sex-linked inheritance: colour blindness"),
    why="A daughter cannot be colour blind without receiving an affected X from the father; '1/4 and 1/4' gives "
        "fractions of all children, not of daughters; '0 and 1' assumes the mother always passes the affected X.",
    seconds=45)

add(PIV, "Incomplete and co-dominance", "Intermediate", "multi_statement",
    ms("Which of the following statements about dominance relationships are correct?",
       ["In incomplete dominance, the F2 phenotypic ratio is the same as the F2 genotypic ratio.",
        "In co-dominance, the heterozygote expresses the phenotypes of both alleles.",
        "When pink-flowered F1 snapdragons are self-pollinated, about one-fourth of the F2 plants are red-flowered.",
        "In a person of genotype Iᴬi, the alleles Iᴬ and i show co-dominance.",
        "In incomplete dominance the alleles blend permanently, so red flowers are never recovered in the F2."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "B"),
    "Incomplete dominance versus co-dominance",
    "(a) True: in snapdragon both ratios are 1 : 2 : 1, because each genotype has its own phenotype. (b) True: in "
    "co-dominance the F1 resembles both parents; Iᴬ and Iᴮ both express their sugars in group AB. (c) True: RR "
    "(red) is 1/4 of the F2. (d) False: Iᴬ is dominant over i; the person is group A. (e) False: the alleles do not "
    "blend; red and white reappear in the F2, which is why incomplete dominance does not violate segregation.",
    ["(a) true: 1 : 2 : 1 both ways", "(b) true", "(c) true: RR = 1/4", "(d) false: Iᴬ dominant over i",
     "(e) false: no blending; parental types reappear"],
    C12_PI("inheritance of one gene: incomplete dominance and co-dominance"),
    why="Any option with (d) or (e) is wrong.",
    seconds=60)

add(PIV, "Sex determination", "Intermediate", "statement_pair",
    sp("In humans, in each pregnancy there is always a 50 per cent probability of either a male or a female child.",
       "In the XO type of sex determination, as in grasshoppers, the female produces two kinds of eggs, with and "
       "without an X chromosome."),
    SP("C"),
    "Probability of sex in humans; XO type",
    "NCERT: the human male produces X- and Y-bearing sperm in equal proportion, while all ova carry X, so in each "
    "pregnancy there is always a 50% probability of either a male or a female child (Statement I true). In the XO "
    "type, all eggs bear an X chromosome besides the autosomes; it is the male (XO) that produces two kinds of sperm, "
    "with and without X (Statement II false).",
    ["Statement I: true", "Statement II: false, the XO male (not the female) produces two kinds of gametes"],
    C12_PI("sex determination"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "assertion_reason",
    ar("Individuals with Down's syndrome and individuals with Klinefelter's syndrome both have 47 chromosomes.",
       "Both disorders are caused by the gain of a chromosome (aneuploidy): an additional copy of chromosome 21 in "
       "Down's syndrome and an additional X chromosome (XXY) in Klinefelter's syndrome."),
    AR("A"),
    "Chromosome number in aneuploid disorders",
    "Normal humans have 46 chromosomes. Down's syndrome is trisomy of chromosome 21 and Klinefelter's syndrome is "
    "XXY; in each, one extra chromosome is gained through failure of segregation of chromatids (aneuploidy), giving "
    "47. The gain of one chromosome (R) is exactly why both have 47 chromosomes (A).",
    ["46 + 1 extra chromosome = 47 in both", "R states the cause of A"],
    C12_PI("chromosomal disorders"),
    seconds=35)

add(PIV, "Sex-linked inheritance", "Intermediate", "direct",
    "A woman who is a carrier for haemophilia marries a haemophilic man. Among their daughters, what is expected?",
    P("Half are haemophilic and half are carriers",
      ["All are carriers and none is haemophilic", "All are haemophilic",
       "Half are carriers and half are normal (non-carriers)"], "D"),
    "Haemophilia: carrier mother, affected father",
    "Mother XᴴXʰ, father XʰY. Every daughter receives the father's Xʰ. From the mother she gets Xᴴ or Xʰ with equal "
    "probability. So daughters are XᴴXʰ (carriers) or XʰXʰ (haemophilic), 1/2 each. NCERT notes that such haemophilic "
    "females are extremely rare, precisely because they need this combination of parents.",
    ["Father gives Xʰ to all daughters", "Mother gives Xᴴ or Xʰ (1/2 each)", "Daughters: 1/2 carriers, 1/2 "
     "haemophilic"],
    C12_PI("sex-linked inheritance: haemophilia"),
    why="'All carriers' applies when the mother is normal (non-carrier); 'all haemophilic' would need a haemophilic "
        "mother; non-carrier daughters are impossible because the father's X always carries the allele.",
    seconds=40)

add(PIV, "Linkage and crossing over", "Intermediate", "assertion_reason",
    ar("When a dihybrid is self-pollinated, the F2 always shows the phenotypic ratio 9 : 3 : 3 : 1.",
       "Morgan found that when the two genes in a dihybrid cross were situated on the same chromosome, the proportion "
       "of parental gene combinations was much higher than that of the non-parental type."),
    AR("D"),
    "Independent assortment versus linkage",
    "A is false: the 9 : 3 : 3 : 1 ratio is expected only when the two genes assort independently and show complete "
    "dominance; linked genes (as in Morgan's Drosophila crosses) give parental combinations far more often, and "
    "incomplete dominance changes the ratio. R is true: it is NCERT's account of Morgan's dihybrid crosses in "
    "Drosophila, and it is the reason why A cannot hold in every case.",
    ["A: false ('always' fails for linked genes or incomplete dominance)",
     "R: true (Morgan: parental combinations predominate for genes on the same chromosome)"],
    C12_PI("inheritance of two genes; linkage and recombination"),
    seconds=40)

add(PIV, "Linkage and crossing over", "Intermediate", "statement_pair",
    sp("When two genes are tightly linked, the recombinant classes in a test cross greatly outnumber the parental "
       "classes.",
       "In a test cross of a dihybrid AaBb whose two genes assort independently, the four progeny classes are "
       "expected in a 1 : 1 : 1 : 1 ratio."),
    SP("D"),
    "Reading test-cross results",
    "Statement I is false: tightly linked genes show very low recombination, so the parental classes greatly "
    "outnumber the recombinants (Morgan: 1.3% recombination for yellow body and white eye). Statement II is true: an "
    "independently assorting dihybrid forms AB, Ab, aB and ab gametes equally, giving 1 : 1 : 1 : 1 with aabb.",
    ["Statement I: false, parental types predominate with linkage", "Statement II: true"],
    C12_PI("linkage and recombination"),
    seconds=35)

# AaBbCc x aabbcc, additive polygene: count of dominant alleles in progeny.
_pi_poly = Counter(sum(c.isupper() for locus in g for c in locus) for g in _cross("AaBbCc", "aabbcc").elements())
assert sorted(_pi_poly) == [0, 1, 2, 3] and F(_pi_poly[3], sum(_pi_poly.values())) == F(1, 8)
assert F(_pi_poly[1], sum(_pi_poly.values())) == F(3, 8)

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "Suppose a polygenic trait is controlled by three genes A, B and C, and each dominant allele adds an equal amount "
    "to the phenotype. A plant AaBbCc is crossed with aabbcc. How many phenotypic classes will the progeny show, and "
    "what fraction of the progeny will have the same phenotype as the AaBbCc parent?",
    P("4 classes; 1/8", ["7 classes; 5/16", "4 classes; 3/8", "8 classes; 1/8"], "B"),
    "Additive polygenes in a test cross",
    "aabbcc contributes no dominant alleles, so each progeny's number of dominant alleles equals the number it gets "
    "from AaBbCc: 0, 1, 2 or 3, with probabilities 1/8, 3/8, 3/8, 1/8. With additive effects, phenotype depends only "
    "on this number, so there are 4 classes. The AaBbCc parent has 3 dominant alleles; progeny with 3 (genotype "
    "AaBbCc) are 1/8.",
    ["Dominant alleles from AaBbCc: 0 to 3", "Classes: 4", "P(3) = (1/2)³ = 1/8"],
    C12_PI("polygenic inheritance"),
    why="7 classes and 5/16 belong to the selfed cross AaBbCc × AaBbCc; 3/8 is the fraction with one (or two) dominant "
        "alleles; 8 counts genotypes, not additive phenotypes.",
    seconds=80, verified_by=RECOMPUTED)

_pi_two = 2 * F(1, 4) * F(3, 4)
assert _pi_two == F(3, 8) and F(1, 4) * F(3, 4) == F(3, 16)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "direct",
    "Both parents are unaffected carriers of phenylketonuria, an autosomal recessive disorder. If they have two "
    "children, what is the probability that exactly one of the two children is affected?",
    P("3/8", ["1/4", "3/16", "1/16"], "A"),
    "Probability for two independent births",
    "Each child of Aa × Aa is affected (aa) with probability 1/4 and unaffected with 3/4, independently. Exactly one "
    "affected can happen in two orders (first affected, second not; or the reverse): 2 × (1/4 × 3/4) = 6/16 = 3/8.",
    ["P(affected) = 1/4, P(unaffected) = 3/4", "Two orders: 2 × 1/4 × 3/4", "= 3/8"],
    C12_PI("Mendelian disorders: phenylketonuria"),
    why="1/4 is the probability for one child; 3/16 counts only one birth order; 1/16 is the probability that both "
        "children are affected.",
    seconds=60, verified_by=RECOMPUTED)

_pi_ml = {"RrYy×Rryy": (3, 3, 1, 1), "RrYy×rrYY": (1, 1), "RrYy×RRYy": (3, 1), "Rryy×rrYy": (1, 1, 1, 1)}
for _k, _v in _pi_ml.items():
    assert _pheno_ratio(*_k.split("×")) == _v, (_k, _pheno_ratio(*_k.split("×")))

add(PIV, "Mendelian inheritance", "Advanced", "match_list",
    ml(("cross (R round over r wrinkled; Y yellow over y green; independent assortment)",
        "phenotypic ratio of the progeny"),
       ["RrYy × Rryy", "RrYy × rrYY", "RrYy × RRYy", "Rryy × rrYy"],
       ["1 : 1 : 1 : 1", "3 : 3 : 1 : 1", "3 : 1", "1 : 1"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "II", "B": "III", "C": "IV", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"},
       {"A": "II", "B": "I", "C": "III", "D": "IV"}], "D"),
    "Combining monohybrid ratios",
    "Treat each gene separately and multiply. A: Rr × Rr (3 : 1) and Yy × yy (1 : 1) → 3 : 3 : 1 : 1. B: Rr × rr "
    "(1 : 1) and Yy × YY (all yellow) → 1 : 1. C: Rr × RR (all round) and Yy × Yy (3 : 1) → 3 : 1. D: Rr × rr (1 : 1) "
    "and yy × Yy (1 : 1) → 1 : 1 : 1 : 1.",
    ["A: (3 : 1)(1 : 1) = 3 : 3 : 1 : 1", "B: (1 : 1)(1) = 1 : 1", "C: (1)(3 : 1) = 3 : 1",
     "D: (1 : 1)(1 : 1) = 1 : 1 : 1 : 1"],
    C12_PI("inheritance of two genes"),
    shortcut="A gene whose cross gives only one phenotype (Rr × RR, Yy × YY) drops out of the ratio.",
    why="The other codes mix up B and C (which gene drops out) or A and D (one 3 : 1 factor versus two 1 : 1 factors).",
    seconds=90, verified_by=RECOMPUTED)

_pi_rf = F(20, 100)
assert 1000 * _pi_rf / 2 == 100 and 1000 * (1 - _pi_rf) / 2 == 400

add(PIV, "Linkage and crossing over", "Advanced", "direct",
    "Genes A and B lie on the same chromosome, with 20 per cent recombination between them. A dihybrid that received "
    "Ab from one parent and aB from the other is test-crossed with aabb, giving 1000 progeny. How many progeny of "
    "genotype AaBb are expected?",
    P("100", ["400", "250", "200"], "B"),
    "Recombinants depend on the parental combination",
    "The dihybrid's parental (non-recombinant) gametes are Ab and aB; the recombinant gametes are AB and ab. With 20% "
    "recombination, AB and ab together make 20% of the gametes, 10% each. AaBb progeny come from AB gametes: 10% of "
    "1000 = 100. (The parental classes Aabb and aaBb are 400 each.)",
    ["Parental gametes: Ab, aB (80%)", "Recombinant gametes: AB, ab (20%, 10% each)", "AaBb from AB = 100"],
    C12_PI("linkage and recombination"),
    why="400 treats AB as a parental gamete, which it would be only if the dihybrid had received AB and ab; 250 "
        "assumes independent assortment; 200 takes the whole recombinant fraction for one class.",
    seconds=75, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "multi_statement",
    ms("A colour-blind man marries a woman who is homozygous for normal vision. Their daughters later marry men with "
       "normal vision. Which of the following statements are correct?",
       ["All the daughters of the colour-blind man are carriers.",
        "None of the sons of the colour-blind man is colour blind.",
        "About half of the sons born to his daughters are expected to be colour blind.",
        "His sons can pass the allele for colour blindness to their own sons.",
        "About half of the daughters born to his daughters are expected to be colour blind."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "C"),
    "Criss-cross inheritance of an X-linked trait",
    "The man (XᶜY) gives Xᶜ to every daughter and Y to every son; the mother gives only normal X. (a) True: daughters "
    "are XXᶜ carriers. (b) True: sons are XY, normal. (c) True: a carrier daughter married to a normal man has sons "
    "XᶜY or XY, half colour blind. (d) False: his sons are normal and do not carry the allele; in any case a father "
    "gives Y, not X, to his sons. (e) False: granddaughters through a carrier daughter and a normal father always get "
    "a normal X from the father, so none is colour blind (half are carriers).",
    ["(a) true", "(b) true", "(c) true: grandsons 1/2 affected", "(d) false", "(e) false: granddaughters 0 affected"],
    C12_PI("sex-linked inheritance: colour blindness"),
    why="Options with (d) or (e) are wrong; 'b, d and e' also leaves out (a) and (c).",
    seconds=80)

_pi_het4 = F(1, 2) ** 4
assert _pi_het4 == F(1, 16) and F(3, 4) ** 4 == F(81, 256) and F(1, 4) ** 4 == F(1, 256)

add(PIV, "Mendelian inheritance", "Advanced", "direct",
    "A plant heterozygous for four independently assorting genes (AaBbCcDd) is self-pollinated. What fraction of the "
    "progeny will be heterozygous at all four loci?",
    P("1/16", ["1/256", "81/256", "1/8"], "D"),
    "Product rule for independent genes",
    "For each gene, Aa × Aa gives 1/4 AA, 1/2 Aa and 1/4 aa, so the chance of being heterozygous at one locus is 1/2. "
    "The four genes assort independently, so the probabilities multiply: (1/2)⁴ = 1/16.",
    ["P(heterozygous) per locus = 1/2", "Four independent loci: (1/2)⁴ = 1/16"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="1/256 uses 1/4 per locus (a homozygous class); 81/256 is the fraction showing all four dominant phenotypes; "
        "1/8 stops at three loci.",
    seconds=50, verified_by=RECOMPUTED)


# Woman: unaffected, parents unaffected, brother affected -> P(carrier) = 2/3; husband a known carrier.
_pi_p = F(2, 3) * F(1, 4)
assert _pi_p == F(1, 6) and F(1, 2) * F(1, 4) == F(1, 8)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "direct",
    "A woman with normal phenotype has unaffected parents but a brother with phenylketonuria (an autosomal recessive "
    "disorder). She marries a man who is known to be a carrier. What is the probability that their first child will "
    "have phenylketonuria?",
    P("1/6", ["1/4", "1/8", "2/3"], "B"),
    "Conditional carrier probability",
    "The brother is affected (aa), so both unaffected parents are carriers (Aa × Aa). The woman is unaffected, so she "
    "is AA or Aa in the ratio 1 : 2, i.e. a carrier with probability 2/3. A child of two carriers is affected with "
    "probability 1/4. Overall: 2/3 × 1/4 = 1/6.",
    ["Parents: Aa × Aa", "Unaffected sister: P(Aa) = 2/3", "Child affected = 2/3 × 1/4 = 1/6"],
    C12_PI("Mendelian disorders: phenylketonuria"),
    why="1/4 assumes the woman is certainly a carrier; 1/8 takes her carrier probability as 1/2 (forgetting that "
        "she is known to be unaffected); 2/3 is her probability of being a carrier, not the child's risk.",
    seconds=75, verified_by=RECOMPUTED)



# ================================================================ Molecular Basis of Inheritance (7 / 10 / 7)
C12_MB = lambda s: ref(12, MBI, s)
_STOP = {"UAA", "UAG", "UGA"}


def _peptide_length(mrna):
    """Amino acids made from the first AUG to the first in-frame stop codon."""
    start = mrna.index("AUG")
    n = 0
    for i in range(start, len(mrna) - 2, 3):
        if mrna[i:i + 3] in _STOP:
            return n
        n += 1
    raise ValueError("no stop codon")


add(MBI, "Genetic code and translation", "Basic", "direct",
    "Of the 64 codons, 3 do not code for any amino acid and function as stop codons. They are:",
    P("UAA, UAG and UGA", ["AUG, UAA and UAG", "UUU, UAA and UGA", "UAA, UGG and UGA"], "A"),
    "Stop codons",
    "NCERT: the codon is a triplet; 61 codons code for amino acids and 3 codons do not code for any amino acid, so "
    "they function as stop codons. In the table of codons these are UAA, UAG and UGA.",
    ["64 codons = 61 sense + 3 stop", "Stop codons: UAA, UAG, UGA"],
    C12_MB("genetic code"),
    why="AUG is the initiator codon (methionine); UUU codes for phenylalanine; UGG codes for an amino acid "
        "(tryptophan), not a stop signal.",
    seconds=20)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "statement_pair",
    sp("According to the salient features of the human genome, it contains 3164.7 million nucleotide bases.",
       "Chromosome 1 has the fewest genes (231), and the Y chromosome has the most (2968)."),
    SP("C"),
    "Salient features of the human genome",
    "NCERT: the human genome contains 3164.7 million nucleotide bases (Statement I true). Chromosome 1 has the most "
    "genes (2968) and the Y chromosome has the fewest (231); Statement II reverses them, so it is false.",
    ["Statement I: true", "Statement II: false, chromosome 1 has 2968 genes and Y has 231"],
    C12_MB("human genome project: salient features of the human genome"),
    seconds=25)

add(MBI, "DNA as genetic material", "Basic", "match_list",
    ml(("scientist(s)", "organism used in the experiment"),
       ["Frederick Griffith", "Alfred Hershey and Martha Chase", "Meselson and Stahl", "Taylor and colleagues"],
       ["Vicia faba (faba bean)", "Bacteriophages infecting bacteria", "Streptococcus pneumoniae",
        "Escherichia coli"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "IV", "B": "II", "C": "III", "D": "I"},
       {"A": "III", "B": "II", "C": "I", "D": "IV"}], "B"),
    "Organisms of the classic experiments",
    "Griffith (1928) worked with Streptococcus pneumoniae (S and R strains) in mice. Hershey and Chase (1952) worked "
    "with bacteriophages, viruses that infect bacteria. Meselson and Stahl (1958) grew Escherichia coli in ¹⁵N and "
    "¹⁴N media. Taylor and colleagues (1958) used Vicia faba (faba beans) with radioactive thymidine to show "
    "semiconservative replication in chromosomes.",
    ["A-III", "B-II", "C-IV", "D-I"],
    C12_MB("the search for genetic material; replication: the experimental proof"),
    why="The other codes swap E. coli with the bacteriophages or with Vicia faba, or give Griffith's bacterium to "
        "Meselson and Stahl.",
    seconds=35)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "statement_pair",
    sp("The Human Genome Project was coordinated by the U.S. Department of Energy and the National Institute of "
       "Health.",
       "During the early years of the project, the Wellcome Trust (U.K.) became a major partner, and additional "
       "contributions came from Japan, France, Germany, China and others."),
    SP("A"),
    "Organisation of the Human Genome Project",
    "NCERT: the HGP was a 13-year project coordinated by the U.S. Department of Energy and the National Institute of "
    "Health. During the early years, the Wellcome Trust (U.K.) became a major partner; additional contributions came "
    "from Japan, France, Germany, China and others. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("human genome project"),
    seconds=25)

add(MBI, "DNA and RNA structure", "Basic", "statement_pair",
    sp("Adenine and cytosine are both purines.",
       "In RNA, uracil is found at the place of thymine."),
    SP("D"),
    "Nitrogenous bases",
    "NCERT: nitrogenous bases are of two types: purines (adenine and guanine) and pyrimidines (cytosine, uracil and "
    "thymine). So Statement I is false (cytosine is a pyrimidine). Cytosine is common to DNA and RNA, thymine is "
    "present in DNA, and uracil is present in RNA at the place of thymine (Statement II true).",
    ["Statement I: false, cytosine is a pyrimidine", "Statement II: true"],
    C12_MB("structure of polynucleotide chain"),
    seconds=20)

add(MBI, "Genetic code and translation", "Basic", "assertion_reason",
    ar("tRNA is called an adapter molecule.",
       "tRNA has an anticodon loop whose bases are complementary to the code, and an amino acid acceptor end to which "
       "it binds an amino acid."),
    AR("A"),
    "tRNA as the adapter",
    "An adapter must read the code on one side and carry the corresponding amino acid on the other. NCERT: tRNA has "
    "an anticodon loop with bases complementary to the code, and an amino acid acceptor end to which it binds amino "
    "acids. These two features (R) are exactly what make tRNA the adapter between codon and amino acid (A).",
    ["A: true", "R: true", "Reads the codon + carries the amino acid = adapter: R explains A"],
    C12_MB("genetic code: tRNA, the adapter molecule"),
    seconds=30)

add(MBI, "Transcription", "Basic", "multi_statement",
    ms("In bacteria, three major types of RNA are needed for protein synthesis. Which of the following statements are "
       "correct?",
       ["mRNA provides the template.",
        "tRNA brings amino acids and reads the genetic code.",
        "rRNA plays a structural and catalytic role during translation.",
        "Each of the three types of RNA is transcribed by a different RNA polymerase.",
        "rRNA carries the codons that specify the sequence of amino acids."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
    "Roles of the three RNAs",
    "NCERT: in bacteria there are three major types of RNA: mRNA (messenger), tRNA (transfer) and rRNA (ribosomal); "
    "all three are needed to synthesise a protein. mRNA provides the template, tRNA brings amino acids and reads the "
    "genetic code, and rRNAs play structural and catalytic roles during translation. (d) is false: in bacteria a "
    "single DNA-dependent RNA polymerase transcribes all types of RNA. (e) is false: the codons are on mRNA.",
    ["(a), (b), (c): true", "(d): false, one RNA polymerase in bacteria", "(e): false, codons are in mRNA"],
    C12_MB("transcription: transcription unit and the gene"),
    why="Every other option includes (d) or (e).",
    seconds=40)

add(MBI, "Transcription", "Intermediate", "assertion_reason",
    ar("In bacteria, transcription and translation can be coupled: translation can begin much before the mRNA is "
       "fully transcribed.",
       "In bacteria, the mRNA does not require processing to become active, and transcription and translation take "
       "place in the same compartment, since there is no separation of cytosol and nucleus."),
    AR("A"),
    "Coupled transcription and translation",
    "NCERT: in bacteria, since the mRNA does not require any processing to become active, and since transcription and "
    "translation take place in the same compartment (there is no separation of cytosol and nucleus in bacteria), many "
    "times the translation can begin much before the mRNA is fully transcribed. Consequently, transcription and "
    "translation can be coupled. R gives exactly the reasons for A.",
    ["A: true", "R: true", "No processing + no nuclear envelope → coupling: R explains A"],
    C12_MB("transcription"),
    seconds=35)

add(MBI, "Transcription", "Intermediate", "statement_pair",
    sp("The inheritance of a character is affected only by the structural gene, and never by the promoter or "
       "regulatory sequences.",
       "The regulatory sequences of a structural gene are sometimes loosely defined as regulatory genes, even though "
       "they do not code for any RNA or protein."),
    SP("D"),
    "Regulatory sequences and the definition of a gene",
    "NCERT: the inheritance of a character is also affected by the promoter and regulatory sequences of a structural "
    "gene (Statement I false). Hence, sometimes the regulatory sequences are loosely defined as regulatory genes, even "
    "though these sequences do not code for any RNA or protein (Statement II true).",
    ["Statement I: false", "Statement II: true"],
    C12_MB("transcription: transcription unit and the gene"),
    seconds=30)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "multi_statement",
    ms("Which of the following were among the goals of the Human Genome Project?",
       ["To store the information obtained in databases.",
        "To improve tools for data analysis.",
        "To transfer related technologies to other sectors, such as industries.",
        "To address the ethical, legal and social issues (ELSI) that may arise from the project.",
        "To sequence the complete genomes of all the non-human organisms on earth."]),
    MS(["a", "b", "c", "d"], [["a", "b", "e"], ["a", "c", "d", "e"], ["b", "d", "e"]], "C"),
    "Goals of the HGP",
    "NCERT lists the goals of the HGP: identify all the approximately 20,000–25,000 genes in human DNA; determine the "
    "sequences of the 3 billion base pairs; store this information in databases; improve tools for data analysis; "
    "transfer related technologies to other sectors, such as industries; and address the ethical, legal and social "
    "issues (ELSI). The genomes of some model organisms (bacteria, yeast, C. elegans, Drosophila, rice, Arabidopsis) "
    "were also sequenced, but sequencing all non-human organisms was never a goal.",
    ["(a), (b), (c), (d): goals", "(e): not a goal"],
    C12_MB("human genome project: goals of HGP"),
    why="Options containing (e) are wrong; 'a, b and e' also leaves out (c) and (d).",
    seconds=45)

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "A codon in an mRNA reads 5'-AUG-3'. The anticodon of the tRNA that pairs with it, written in the 5'→3' "
    "direction, is:",
    P("5'-CAU-3'", ["5'-UAC-3'", "5'-TAC-3'", "5'-AUG-3'"], "B"),
    "Codon-anticodon pairing is antiparallel",
    "The anticodon bases are complementary to the codon, and the two pair in antiparallel fashion. Under 5'-A-U-G-3' "
    "the anticodon reads 3'-U-A-C-5'. Written 5'→3', it is 5'-CAU-3'.",
    ["Complement of 5'-AUG-3' (antiparallel): 3'-UAC-5'", "Rewritten 5'→3': 5'-CAU-3'"],
    C12_MB("genetic code: tRNA, the adapter molecule"),
    why="5'-UAC-3' is the complement written with the wrong polarity; T does not occur in RNA; the anticodon is "
        "complementary, not identical, to the codon.",
    seconds=40)

_mb_bp = 1.36e-3 / 0.34e-9
assert abs(_mb_bp - 4e6) < 1

add(MBI, "DNA packaging", "Intermediate", "numerical",
    "The DNA of Escherichia coli is a double helix about 1.36 mm long. Taking the distance between two consecutive "
    "base pairs as 0.34 nm, approximately how many base pairs does it contain?",
    P("4 × 10⁶", ["4 × 10³", "2 × 10⁶", "8 × 10⁶"], "C"),
    "Length of DNA and number of base pairs",
    "Number of bp = length / distance per bp = (1.36 × 10⁻³ m) / (0.34 × 10⁻⁹ m) = 4 × 10⁶ bp. (NCERT gives the E. "
    "coli genome as 4.6 × 10⁶ bp; the round figure here comes from the given length.)",
    ["1.36 mm = 1.36 × 10⁻³ m; 0.34 nm = 0.34 × 10⁻⁹ m", "1.36 × 10⁻³ / 0.34 × 10⁻⁹ = 4 × 10⁶"],
    C12_MB("packaging of DNA helix"),
    why="4 × 10³ treats millimetres as metres and nanometres as micrometres (a 10⁻³ slip); 2 × 10⁶ halves the answer "
        "for two strands, though the 0.34 nm spacing is already per base pair; 8 × 10⁶ counts nucleotides of both "
        "strands, not base pairs.",
    seconds=50, verified_by=RECOMPUTED)

_mb_T = 18
assert (100 - 2 * _mb_T) / 2 == 32

add(MBI, "DNA and RNA structure", "Intermediate", "numerical",
    "In a double-stranded DNA molecule, 18 per cent of the bases are thymine. What percentage of the bases are "
    "guanine?",
    P("32 per cent", ["18 per cent", "64 per cent", "82 per cent"], "B"),
    "Chargaff's rules",
    "In double-stranded DNA, A = T and G = C (Chargaff). T = 18%, so A = 18% and A + T = 36%. The remaining 64% is G + "
    "C, shared equally: G = 32%.",
    ["A = T = 18% → A + T = 36%", "G + C = 64%", "G = C = 32%"],
    C12_MB("structure of DNA: Chargaff's rule"),
    why="18% equates G with T; 64% is G + C together; 82% subtracts only the thymine from 100%.",
    seconds=35, verified_by=RECOMPUTED)

add(MBI, "DNA and RNA structure", "Intermediate", "statement_pair",
    sp("In every double-stranded DNA, the ratio (A + T)/(G + C) is equal to one.",
       "In every double-stranded DNA, the ratio (A + G)/(T + C) is equal to one."),
    SP("D"),
    "Which base ratios are constant",
    "Because a purine always pairs with a pyrimidine (A with T, G with C), A = T and G = C, so purines equal "
    "pyrimidines: (A + G)/(T + C) = 1 in every double-stranded DNA (Statement II true). But the amount of A + T "
    "relative to G + C differs from one DNA to another, so (A + T)/(G + C) need not be one (Statement I false).",
    ["A = T and G = C", "(A + G)/(T + C) = 1 always", "(A + T)/(G + C) varies between DNAs"],
    C12_MB("structure of DNA: Chargaff's rule and base pairing"),
    seconds=35)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("In the lac operon, the inducer binds directly to the operator, and this allows RNA polymerase to transcribe "
       "the structural genes.",
       "In the presence of an inducer such as lactose, the repressor is inactivated by interaction with the inducer, "
       "which allows RNA polymerase access to the promoter."),
    AR("D"),
    "How the inducer switches on the lac operon",
    "NCERT: in the absence of an inducer, the repressor (from the i gene) binds to the operator region and prevents "
    "RNA polymerase from transcribing the operon. In the presence of an inducer such as lactose or allolactose, the "
    "repressor is inactivated by interaction with the inducer, which allows RNA polymerase access to the promoter, and "
    "transcription proceeds. The inducer acts on the repressor; it is the repressor, not the inducer, that binds the "
    "operator. So A is false and R is true.",
    ["A: false (the inducer interacts with the repressor; the repressor binds the operator)", "R: true"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=35)

add(MBI, "Genetic code and translation", "Intermediate", "match_list",
    ml(("property of the genetic code", "description"),
       ["Degenerate", "Unambiguous and specific", "Comma-less", "Nearly universal"],
       ["The codon is read in mRNA in a contiguous fashion, without punctuation",
        "UUU codes for phenylalanine from bacteria to humans",
        "Some amino acids are coded by more than one codon",
        "One codon codes for only one amino acid"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Properties of the genetic code",
    "Degenerate: some amino acids are coded by more than one codon. Unambiguous and specific: one codon codes for "
    "only one amino acid. Comma-less: the codon is read in mRNA contiguously, with no punctuation. Nearly universal: "
    "from bacteria to humans UUU codes for phenylalanine (some exceptions exist in mitochondrial codons and in some "
    "protozoans).",
    ["A-III", "B-IV", "C-I", "D-II"],
    C12_MB("genetic code"),
    why="The usual confusion is between degenerate (many codons, one amino acid) and unambiguous (one codon, one amino "
        "acid), and between comma-less and universal.",
    seconds=40)

add(MBI, "Transcription", "Intermediate", "multi_statement",
    ms("Which of the following statements about the action of the bacterial RNA polymerase during transcription are "
       "correct?",
       ["It uses nucleoside triphosphates as substrates.",
        "Only a short stretch of RNA remains bound to the enzyme during elongation.",
        "Once the polymerase reaches the terminator region, the nascent RNA falls off, and so does the RNA "
        "polymerase.",
        "On its own, the RNA polymerase can initiate transcription at the promoter without any initiation factor.",
        "It polymerises nucleotides in a template-independent manner."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["a", "c", "e"], ["b", "c", "d", "e"]], "B"),
    "Steps of bacterial transcription",
    "NCERT: RNA polymerase binds to the promoter and initiates transcription. It uses nucleoside triphosphates as "
    "substrate and polymerises in a template-dependent fashion following the rule of complementarity (so (a) is true "
    "and (e) false). It also opens the helix and continues elongation; only a short stretch of RNA remains bound to "
    "the enzyme (b true). At the terminator, the nascent RNA falls off, and so does the polymerase (c true). The "
    "polymerase is only capable of catalysing elongation; it associates transiently with the initiation factor (σ) "
    "to initiate (d false).",
    ["(a) true", "(b) true", "(c) true", "(d) false: σ factor needed for initiation",
     "(e) false: template-dependent"],
    C12_MB("transcription"),
    why="Any option with (d) or (e) is wrong.",
    seconds=55)

add(MBI, "Replication", "Advanced", "multi_statement",
    ms("Compare DNA replication with transcription. Which of the following statements are correct?",
       ["In both, the new nucleic acid chain is polymerised in the 5'→3' direction.",
        "In transcription, only a segment of DNA and only one of its strands is copied into RNA.",
        "Both processes use deoxyribonucleoside triphosphates as substrates.",
        "Both processes require DNA ligase to join discontinuously synthesised fragments."]),
    MS(["a", "b"], [["a", "c"], ["b", "d"], ["a", "b", "c"]], "A"),
    "Replication versus transcription",
    "(a) True: DNA-dependent DNA polymerases catalyse polymerisation only in the 5'→3' direction, and RNA is made on "
    "the 3'→5' template strand, i.e. also 5'→3'. (b) True: NCERT says that in transcription only a segment of DNA "
    "and only one of the strands is copied into RNA. (c) False: replication uses deoxyribonucleoside triphosphates, "
    "but RNA polymerase uses (ribo)nucleoside triphosphates. (d) False: DNA ligase joins the discontinuously "
    "synthesised fragments of replication; RNA is synthesised continuously.",
    ["(a) true", "(b) true", "(c) false: transcription uses NTPs", "(d) false: no ligase in transcription"],
    C12_MB("replication; transcription"),
    why="Options with (c) or (d) are wrong; 'a, b and c' adds the false (c).",
    seconds=60)

add(MBI, "Replication", "Advanced", "direct",
    "Meselson and Stahl transferred E. coli grown in ¹⁵NH₄Cl into ¹⁴NH₄Cl medium and analysed the DNA after one "
    "generation (20 minutes) by CsCl density-gradient centrifugation. If DNA replication had been conservative (both "
    "parental strands staying together and both new strands forming a new molecule) instead of semiconservative, what "
    "would they have observed after this one generation?",
    P("Two bands, one heavy (¹⁵N/¹⁵N) and one light (¹⁴N/¹⁴N), and no hybrid band",
      ["A single hybrid (¹⁵N/¹⁴N) band",
       "Equal amounts of hybrid and light DNA",
       "A single light (¹⁴N/¹⁴N) band"], "D"),
    "Why the Meselson-Stahl result proved semiconservative replication",
    "Conservative replication would keep the parental ¹⁵N/¹⁵N duplex intact and make an entirely new ¹⁴N/¹⁴N duplex, "
    "giving a heavy and a light band after one generation, with no hybrid. What was actually observed after 20 "
    "minutes was a single hybrid (intermediate) band, which fits semiconservative replication: each daughter molecule "
    "has one old ¹⁵N strand and one new ¹⁴N strand.",
    ["Conservative: old duplex (heavy) + new duplex (light)", "Observed: one hybrid band at 20 min →"
     " semiconservative"],
    C12_MB("replication: the experimental proof"),
    why="A single hybrid band is the actual (semiconservative) result after one generation; equal hybrid and light DNA "
        "is the semiconservative result after two generations (40 minutes); a single light band would need all the "
        "parental ¹⁵N DNA to disappear.",
    seconds=60)

add(MBI, "Lac operon", "Advanced", "direct",
    "A mutant E. coli cannot make a functional permease (the y gene is defective), but its i, z and a genes and its "
    "promoter and operator are normal. It is placed in a medium containing lactose and no glucose. What happens to the "
    "lac operon?",
    P("It is not induced, because lactose cannot enter the cell to inactivate the repressor",
      ["It is induced normally, because the inducer acts from outside the cell",
       "It is transcribed all the time, because the repressor cannot bind to the operator",
       "Only the y gene is transcribed, because the other genes have their own promoters"], "C"),
    "Role of permease in induction",
    "The lac operon is switched on when lactose (the inducer) enters the cell and inactivates the repressor. NCERT: "
    "permease increases the permeability of the cell to β-galactosides, and a very low level of lac operon expression "
    "has to be present all the time, otherwise lactose cannot enter the cells. Without functional permease, lactose "
    "cannot get in, the repressor stays bound to the operator, and the operon remains switched off.",
    ["Inducer must enter the cell", "No permease → lactose cannot enter", "Repressor stays on operator → operon off"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="The inducer acts inside the cell on the repressor; the repressor and operator here are normal, so expression "
        "is not constitutive; z, y and a share one promoter and are transcribed together as one polycistronic unit.",
    seconds=60)

# Coding strand A30 T20 G15 C35 -> mRNA U20; template A = coding T.
_mb_coding = {"A": 30, "T": 20, "G": 15, "C": 35}
_mb_mrna_U = _mb_coding["T"]
_mb_template_A = _mb_coding["T"]
assert sum(_mb_coding.values()) == 100 and _mb_mrna_U == 20 and _mb_template_A == 20 != 30

add(MBI, "Transcription", "Advanced", "statement_pair",
    sp("If the coding strand of a gene has 30% A, 20% T, 15% G and 35% C, the mRNA transcribed from it will contain "
       "20% uracil.",
       "The template strand of the same gene will contain 30% adenine."),
    SP("C"),
    "Base composition of coding strand, template strand and mRNA",
    "The mRNA has the same sequence as the coding strand, with U in place of T, so it has 30% A, 20% U, 15% G and 35% "
    "C (Statement I true). The template strand is complementary to the coding strand: its A pairs with the coding "
    "strand's T, so template A = 20%, T = 30%, G = 35%, C = 15% (Statement II false).",
    ["mRNA = coding strand with U for T → U = 20%", "Template A = coding T = 20%, not 30%"],
    C12_MB("transcription: transcription unit"),
    seconds=55, verified_by=RECOMPUTED)

# Child's bands not explained by the mother must come from the father.
_mb_child, _mb_mother = {1, 3, 5, 7}, {1, 5, 8}
_mb_men = {"P": {3, 6, 7}, "Q": {2, 3, 9}, "R": {4, 7, 9}, "S": {1, 5, 6}}
_mb_need = _mb_child - _mb_mother
assert _mb_need == {3, 7} and [k for k, v in _mb_men.items() if _mb_need <= v] == ["P"]

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "direct",
    "In a paternity dispute, VNTR bands (in kb) are compared. Child: 1, 3, 5, 7. Mother: 1, 5, 8. Man P: 3, 6, 7. Man "
    "Q: 2, 3, 9. Man R: 4, 7, 9. Man S: 1, 5, 6. Assuming every band of the child must come from one of the two "
    "biological parents, who could be the father?",
    P("Man P", ["Man Q", "Man R", "Man S"], "B"),
    "DNA fingerprinting in paternity testing",
    "VNTRs are inherited, so each band in the child's fingerprint must come from the mother or the father. The child's "
    "bands 1 and 5 are present in the mother. Bands 3 and 7 are not, so they must come from the father. Only man P "
    "has both 3 and 7.",
    ["Child's bands from mother: 1, 5", "Bands to be explained by the father: 3 and 7", "Only P has both"],
    C12_MB("DNA fingerprinting"),
    why="Q lacks band 7, R lacks band 3, and S shares only the mother's bands and has neither 3 nor 7.",
    seconds=60, verified_by=RECOMPUTED)

_mb_mrna = "GAUGUUUGGCUAAUG"
assert _peptide_length(_mb_mrna) == 3

add(MBI, "Genetic code and translation", "Advanced", "direct",
    "An mRNA segment reads 5'-GAUGUUUGGCUAAUG-3'. Translation starts at the first AUG. How many amino acids will be "
    "joined into the polypeptide from this segment?",
    P("3", ["4", "5", "2"], "B"),
    "Finding the start and stop codons",
    "Reading from the first AUG in triplets: AUG (Met) UUU (Phe) GGC (Gly) UAA (stop). Translation ends at the stop "
    "codon UAA, which has no tRNA and codes for no amino acid. So three amino acids are joined: Met-Phe-Gly. The final "
    "AUG lies after the stop codon and is not translated in this reading.",
    ["Start: AUG at positions 2–4", "Codons: AUG UUU GGC | UAA", "3 amino acids"],
    C12_MB("genetic code; translation"),
    why="4 counts the stop codon as an amino acid; 5 divides the whole 15-base segment by 3; 2 leaves out "
        "methionine coded by the start codon.",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "Genetic code and translation", "Advanced", "match_list",
    ml(("change in the coding region of a gene", "effect on the encoded protein"),
       ["A codon UUU changes to UUC", "The sixth codon of the β-globin gene changes from GAG to GUG",
        "One base is inserted within the gene", "Three consecutive bases making up one codon are deleted"],
       ["The reading frame is shifted from the point of insertion",
        "Glutamic acid is replaced by valine",
        "One amino acid is lost; the reading frame is unaltered",
        "The same amino acid (phenylalanine) is incorporated"]),
    M({"A": "IV", "B": "II", "C": "I", "D": "III"},
      [{"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "IV", "B": "II", "C": "III", "D": "I"},
       {"A": "IV", "B": "I", "C": "II", "D": "III"}], "C"),
    "Point and frame-shift mutations",
    "A: UUU and UUC both code for phenylalanine (degenerate code), so the protein is unchanged. B: GAG → GUG changes "
    "glutamic acid to valine at the sixth position of the β-globin chain (sickle-cell anaemia, a point mutation). C: "
    "inserting one base shifts the reading frame from that point (frame-shift mutation). D: deleting one whole codon "
    "removes one amino acid and leaves the reading frame unaltered from that point onwards.",
    ["A-IV", "B-II", "C-I", "D-III"],
    C12_MB("genetic code: mutations and genetic code"),
    why="The other codes swap the silent change with the sickle-cell substitution, or the frame shift (one base) with "
        "the in-frame deletion (three bases).",
    seconds=55)



# ================================================================ Microbes in Human Welfare (2 / 4 / 3)
C12_MH = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "statement_pair",
    sp("Penicillin was used extensively to treat American soldiers wounded in World War II.",
       "Fleming, Chain and Florey were awarded the Nobel Prize in 1945 for their work on penicillin."),
    SP("A"),
    "History of penicillin",
    "NCERT: penicillin, discovered by Alexander Fleming and established as an effective antibiotic by Ernest Chain "
    "and Howard Florey, was extensively used to treat American soldiers wounded in World War II. Fleming, Chain and "
    "Florey were awarded the Nobel Prize in 1945. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_MH("microbes in industrial products: antibiotics"),
    seconds=25)

add(MHW, "Household and industrial products", "Basic", "assertion_reason",
    ar("Milk turns into curd when lactic acid bacteria (LAB) such as Lactobacillus grow in it.",
       "During their growth, LAB produce acids that coagulate and partially digest the milk proteins."),
    AR("A"),
    "How LAB make curd",
    "NCERT: micro-organisms such as Lactobacillus, commonly called lactic acid bacteria, grow in milk and convert it "
    "to curd. During growth, the LAB produce acids that coagulate and partially digest the milk proteins. The "
    "coagulation of milk proteins by these acids (R) is what turns milk into curd (A).",
    ["A: true", "R: true", "Acid coagulates milk proteins → curd: R explains A"],
    C12_MH("microbes in household products"),
    seconds=25)

add(MHW, "Sewage treatment", "Intermediate", "multi_statement",
    ms("Which of the following statements about the anaerobic sludge digesters of a sewage treatment plant are "
       "correct?",
       ["The major part of the activated sludge is pumped into the anaerobic sludge digesters.",
        "In the digesters, bacteria that grow anaerobically digest the bacteria and fungi present in the sludge.",
        "The gases produced during this digestion form biogas, which can be used as a source of energy as it is "
        "inflammable.",
        "The digesters are kept well aerated by pumping air into them continuously.",
        "The effluent from the settling tank, rather than the sludge, is sent to the digesters."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
    "Anaerobic sludge digesters",
    "NCERT: a small part of the activated sludge is pumped back into the aeration tank as inoculum, and the remaining "
    "major part is pumped into large tanks called anaerobic sludge digesters (a true). There, other kinds of bacteria, "
    "which grow anaerobically, digest the bacteria and fungi in the sludge (b true). They produce a mixture of methane, "
    "hydrogen sulphide and carbon dioxide; these gases form biogas, which can be used as a source of energy as it is "
    "inflammable (c true). Air is pumped into the aeration tanks, not the digesters (d false). The effluent from the "
    "secondary treatment is generally released into natural water bodies, not into the digesters (e false).",
    ["(a), (b), (c): true", "(d): false, digesters are anaerobic", "(e): false, the sludge (not the effluent) goes to "
     "the digesters"],
    C12_MH("microbes in sewage treatment: secondary treatment"),
    why="Every other option includes (d) or (e).",
    seconds=55)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "match_list",
    ml(("microbe", "role described in NCERT"),
       ["Trichoderma", "Nucleopolyhedrovirus", "Glomus", "Anabaena"],
       ["Autotrophic, nitrogen-fixing cyanobacterium that is an important biofertiliser in paddy fields",
        "Fungus that forms a symbiotic association (mycorrhiza) and absorbs phosphorus for the plant",
        "Free-living fungus used as a biological control agent against several plant pathogens",
        "Pathogen that attacks insects and other arthropods, used for species-specific biological control"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "II", "B": "IV", "C": "III", "D": "I"},
       {"A": "III", "B": "I", "C": "II", "D": "IV"},
       {"A": "IV", "B": "III", "C": "II", "D": "I"}], "D"),
    "Biocontrol agents and biofertilisers",
    "Trichoderma species are free-living fungi, very common in root ecosystems, that are effective biocontrol agents "
    "of several plant pathogens. Baculoviruses of the genus Nucleopolyhedrovirus attack insects and other arthropods "
    "and have species-specific, narrow-spectrum insecticidal applications. Glomus forms mycorrhiza; the fungal "
    "symbiont absorbs phosphorus from the soil and passes it to the plant. Anabaena is an autotrophic cyanobacterium "
    "that fixes atmospheric nitrogen and is an important biofertiliser in paddy fields.",
    ["A-III", "B-IV", "C-II", "D-I"],
    C12_MH("microbes as biocontrol agents; microbes as biofertilisers"),
    why="The other codes swap the two fungi (Trichoderma and Glomus), or the cyanobacterium with the insect virus.",
    seconds=40)

add(MHW, "Sewage treatment", "Intermediate", "statement_pair",
    sp("Under the Ganga Action Plan and the Yamuna Action Plan, it is proposed to build a large number of sewage "
       "treatment plants so that only treated sewage may be discharged into the rivers.",
       "Biofertilisers are synthetic chemicals that are added to the soil to enrich its nitrogen content."),
    SP("C"),
    "River action plans; nature of biofertilisers",
    "NCERT: the Ministry of Environment and Forests initiated the Ganga Action Plan and Yamuna Action Plan; under these "
    "plans, a large number of sewage treatment plants are proposed so that only treated sewage is discharged into the "
    "rivers (Statement I true). Biofertilisers are organisms (bacteria, fungi and cyanobacteria) that enrich the "
    "nutrient quality of the soil, not synthetic chemicals (Statement II false).",
    ["Statement I: true", "Statement II: false, biofertilisers are organisms"],
    C12_MH("microbes in sewage treatment; microbes as biofertilisers"),
    seconds=30)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "assertion_reason",
    ar("Organic farming and biological control rely on a holistic approach that seeks to understand the webs of "
       "interaction between the many organisms that make up the field fauna and flora.",
       "In biological control, the pests of a field are eradicated completely by spraying broad-spectrum chemical "
       "pesticides."),
    AR("C"),
    "The approach of biological control",
    "A is true: NCERT describes biological control of pests and diseases as relying on natural predation rather than "
    "introduced chemicals, with a holistic approach that seeks to understand the webs of interaction between the "
    "organisms of the field. R is false: biocontrol uses biological methods, not chemicals, and the organic farmer does "
    "not try to eradicate pests completely, since the beneficial predators and parasites depend on them.",
    ["A: true", "R: false (biocontrol avoids chemicals and does not aim at complete eradication)"],
    C12_MH("microbes as biocontrol agents"),
    seconds=35)

add(MHW, "Household and industrial products", "Advanced", "multi_statement",
    ms("Consider the microbes named in NCERT for various products. Which of the following statements are correct?",
       ["The same yeast species is used both for making bread and for producing alcoholic beverages.",
        "Aspergillus niger and Acetobacter aceti are both fungi.",
        "Streptokinase and lactic acid are both produced by bacteria.",
        "Cyclosporin A and statins are both produced by fungi (Trichoderma polysporum and Monascus purpureus "
        "respectively).",
        "Penicillin and citric acid are both produced by bacteria."]),
    MS(["a", "c", "d"], [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "d", "e"]], "B"),
    "Kinds of microbes behind microbial products",
    "(a) True: Saccharomyces cerevisiae is used as baker's yeast for bread and as brewer's yeast for beverages. (b) "
    "False: Aspergillus niger (citric acid) is a fungus but Acetobacter aceti (acetic acid) is a bacterium. (c) True: "
    "streptokinase comes from the bacterium Streptococcus and lactic acid from the bacterium Lactobacillus. (d) True: "
    "cyclosporin A is produced by the fungus Trichoderma polysporum and statins by the fungus Monascus purpureus. "
    "(e) False: penicillin is from the mould Penicillium notatum and citric acid from the fungus "
    "Aspergillus niger.",
    ["(a) true", "(b) false: Acetobacter is a bacterium", "(c) true", "(d) true", "(e) false: both are from fungi"],
    C12_MH("microbes in household products; microbes in industrial products"),
    why="Options with (b) or (e) are wrong.",
    seconds=70)

add(MHW, "Sewage treatment", "Advanced", "statement_pair",
    sp("A sample of river water just downstream of an outlet discharging untreated sewage is expected to show a higher "
       "BOD than a sample of clean river water upstream.",
       "The BOD test measures the rate of uptake of oxygen by micro-organisms in a sample of water, and thus "
       "indirectly measures the organic matter present in the water."),
    SP("A"),
    "Using BOD as an index of pollution",
    "Statement II is NCERT's description of the BOD test: it measures the rate of oxygen uptake by micro-organisms, "
    "and thus, indirectly, BOD is a measure of the organic matter present. Sewage contains large amounts of organic "
    "matter, so water receiving untreated sewage has more organic matter to be oxidised and a higher BOD; the greater "
    "the BOD, the greater the polluting potential. Statement I is therefore also true.",
    ["Statement II: true (NCERT definition of the test)", "Untreated sewage → more organic matter → higher BOD",
     "Statement I: true"],
    C12_MH("microbes in sewage treatment"),
    seconds=45)

add(MHW, "Household and industrial products", "Advanced", "assertion_reason",
    ar("Lactic acid bacteria improve the nutritional quality of curd by increasing its vitamin B₁₂ content.",
       "In our stomach, lactic acid bacteria play a very beneficial role in checking disease-causing microbes."),
    AR("B"),
    "Two separate benefits of LAB",
    "Both statements are NCERT lines about lactic acid bacteria. A is true: LAB increase vitamin B₁₂ and so improve the "
    "nutritional quality of curd. R is true: in our stomach LAB check disease-causing microbes. But R describes a "
    "different benefit, in the human stomach; checking pathogens is not why curd has more vitamin B₁₂. So R does not "
    "explain A.",
    ["A: true", "R: true", "R is a separate benefit (in the stomach): not the explanation of A"],
    C12_MH("microbes in household products"),
    seconds=35)



# ================================================================ Organisms and Populations (4 / 6 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population growth", "Basic", "statement_pair",
    sp("The intrinsic rate of natural increase (r) is an important parameter chosen for assessing the impacts of any "
       "biotic or abiotic factor on population growth.",
       "But for predators, prey species could achieve very high population densities and cause ecosystem "
       "instability."),
    SP("A"),
    "Use of r; role of predators",
    "NCERT: r is an important parameter chosen for assessing impacts of any biotic or abiotic factor on population "
    "growth (Statement I true). Predators keep prey populations under control; but for predators, prey species could "
    "achieve very high population densities and cause ecosystem instability (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_OP("populations: population growth; population interactions: predation"),
    seconds=25)

add(OAP, "Population interactions", "Basic", "assertion_reason",
    ar("Cuscuta, a parasitic plant commonly found growing on hedge plants, derives its nutrition from the host plant.",
       "In the course of evolution, Cuscuta has lost its chlorophyll and leaves."),
    AR("A"),
    "Parasitic adaptation in Cuscuta",
    "NCERT: Cuscuta, a parasitic plant commonly found growing on hedge plants, has lost its chlorophyll and leaves in "
    "the course of evolution, and it derives its nutrition from the host plant which it parasitises. Without "
    "chlorophyll and leaves it cannot make its own food (R), which is why it must draw nutrition from the host (A).",
    ["A: true", "R: true", "No chlorophyll or leaves → cannot photosynthesise → depends on host: R explains A"],
    C12_OP("population interactions: parasitism"),
    seconds=25)

add(OAP, "Population attributes", "Basic", "assertion_reason",
    ar("A population has attributes, such as birth rate, death rate, sex ratio and age distribution, that an "
       "individual organism does not have.",
       "An individual organism also has a birth rate and a death rate."),
    AR("C"),
    "Population versus individual",
    "NCERT: a population has certain attributes whereas an individual organism does not. An individual may have "
    "births and deaths, but a population has birth rates and death rates, expressed per capita; sex ratio and age "
    "distribution are also population attributes. So A is true and R is false.",
    ["A: true", "R: false (an individual has births and deaths, not rates)"],
    C12_OP("populations: population attributes"),
    seconds=25)

add(OAP, "Population interactions", "Basic", "direct",
    "Orchids show a bewildering diversity of floral patterns. According to NCERT, many of these patterns have evolved "
    "to:",
    P("Attract the right pollinator insect (bees and bumblebees) and ensure guaranteed pollination",
      ["Repel herbivores by mimicking poisonous plants",
       "Attract seed-dispersing birds to the fruits",
       "Reduce water loss from the flowers"], "D"),
    "Co-evolution of orchids and pollinators",
    "NCERT: orchids show a bewildering diversity of floral patterns, many of which have evolved to attract the right "
    "pollinator insect (bees and bumblebees) and ensure guaranteed pollination by it. Not all orchids offer rewards; "
    "Ophrys, for example, uses sexual deceit.",
    ["Diverse floral patterns → attract the right pollinator", "Guaranteed pollination by it"],
    C12_OP("population interactions: mutualism"),
    why="NCERT links these patterns to pollinators, not to herbivore defence, seed dispersal or water loss.",
    seconds=25)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("MacArthur showed that five closely related species of warblers living on the same tree were able to avoid "
       "competition and co-exist because of behavioural differences in their foraging activities.",
       "Connell's field experiments showed that, on the rocky sea coasts of Scotland, the smaller barnacle Chthamalus "
       "excludes the larger barnacle Balanus from the intertidal area."),
    SP("C"),
    "Resource partitioning and competitive exclusion",
    "Statement I is true: MacArthur's warblers co-existed by resource partitioning through differences in foraging "
    "behaviour. Statement II is false: Connell found that the larger and competitively superior barnacle Balanus "
    "dominates the intertidal area and excludes the smaller Chthamalus from that zone.",
    ["Statement I: true", "Statement II: false, Balanus (larger, superior) excludes Chthamalus"],
    C12_OP("population interactions: competition"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following are examples of commensalism described in NCERT?",
       ["An orchid growing as an epiphyte on a mango branch",
        "Barnacles growing on the back of a whale",
        "Cattle egrets foraging close to grazing cattle",
        "Clown fish living among the stinging tentacles of a sea anemone",
        "Lichens"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "D"),
    "Recognising commensalism",
    "In commensalism one species benefits and the other is neither harmed nor benefited. NCERT's examples: an orchid "
    "growing as an epiphyte on a mango branch; barnacles on the back of a whale; the cattle egret, which catches the "
    "insects flushed out by grazing cattle; and the clown fish, which gets protection from predators among the "
    "anemone's stinging tentacles while the anemone does not appear to benefit. Lichens are an example of mutualism "
    "(fungus and alga or cyanobacterium).",
    ["(a)-(d): commensalism", "(e) lichens: mutualism"],
    C12_OP("population interactions: commensalism"),
    why="Options containing (e) include a mutualism; '(a), (b) and (c)' leaves out the clown fish.",
    seconds=45)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("In brood parasitism, the host bird incubates the parasitic bird's eggs because they look very different from "
       "its own eggs.",
       "During evolution, the eggs of the parasitic bird have come to resemble the host's eggs in size and colour, "
       "reducing the chances of the host bird detecting the foreign eggs and ejecting them from the nest."),
    AR("D"),
    "Egg mimicry in brood parasitism",
    "NCERT: in brood parasitism (e.g. the cuckoo or koel laying eggs in the crow's nest), the parasitic bird's eggs "
    "have evolved to resemble the host's eggs in size and colour, to reduce the chances of the host bird detecting the "
    "foreign eggs and ejecting them. So the host incubates them because they look similar, not different: A is false "
    "and R is true.",
    ["A: false (the eggs look similar)", "R: true"],
    C12_OP("population interactions: parasitism"),
    seconds=30)

add(OAP, "Population growth", "Intermediate", "match_list",
    ml(("description", "expression"),
       ["Exponential growth (rate form)", "Logistic growth", "Integral form of exponential growth",
        "Change in population density over one time period"],
       ["Nₜ = N₀e^(rt)", "dN/dt = rN", "N(t+1) = N(t) + [(B + I) − (D + E)]", "dN/dt = rN[(K − N)/K]"]),
    M({"A": "II", "B": "IV", "C": "I", "D": "III"},
      [{"A": "I", "B": "IV", "C": "II", "D": "III"},
       {"A": "II", "B": "III", "C": "I", "D": "IV"},
       {"A": "IV", "B": "II", "C": "I", "D": "III"}], "B"),
    "Equations of population growth",
    "Exponential growth: dN/dt = rN; its integral form is Nₜ = N₀e^(rt). Logistic (Verhulst-Pearl) growth includes the "
    "carrying capacity: dN/dt = rN[(K − N)/K]. The density after one period is N(t+1) = N(t) + [(B + I) − (D + E)], "
    "since births and immigration add to it and deaths and emigration remove from it.",
    ["A-II", "B-IV", "C-I", "D-III"],
    C12_OP("populations: population growth"),
    why="The other codes swap the rate and integral forms of exponential growth, or the logistic equation with the "
        "density-change equation.",
    seconds=40)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("Plants have evolved an astonishing variety of morphological and chemical defences against herbivores.",
       "Unlike animals, plants cannot run away from their predators."),
    AR("A"),
    "Why plants need defences",
    "NCERT: for plants, herbivores are the predators. The problem is particularly severe for plants because, unlike "
    "animals, they cannot run away from their predators; plants therefore have evolved an astonishing variety of "
    "morphological (thorns of Acacia and cactus) and chemical (cardiac glycosides of Calotropis; nicotine, caffeine, "
    "quinine) defences. R is the reason given for A.",
    ["A: true", "R: true", "NCERT: 'therefore' links R to A"],
    C12_OP("population interactions: predation"),
    seconds=30)

add(OAP, "Population attributes", "Intermediate", "direct",
    "According to NCERT, population ecology is an important area of ecology because it links ecology to:",
    P("Population genetics and evolution",
      ["Biochemistry and molecular biology", "Taxonomy and systematics", "Physiology and anatomy"], "B"),
    "Importance of population ecology",
    "NCERT: in nature, we rarely find isolated single individuals; they live in populations. Population ecology is an "
    "important area of ecology because it links ecology to population genetics and evolution, since natural selection "
    "operates at the population level to evolve the desired traits.",
    ["Population ecology ↔ population genetics and evolution"],
    C12_OP("populations"),
    why="NCERT does not single out biochemistry, taxonomy or physiology as the fields that population ecology links "
        "ecology to.",
    seconds=20)

# Doubling time of an exponentially growing population: t = ln 2 / r.
_op_t = 0.693 / 0.0205
assert 33.5 < _op_t < 34.0
assert 48 < 1 / 0.0205 < 49.5 and 67 < 2 * 0.693 / 0.0205 < 68

add(OAP, "Population growth", "Advanced", "numerical",
    "NCERT gives the intrinsic rate of natural increase (r) of the human population of India in 1981 as 0.0205 per "
    "year. If a population grew exponentially (Nₜ = N₀e^(rt)) at this constant rate, in about how many years would it "
    "double? (Take ln 2 = 0.693.)",
    P("About 34 years", ["About 49 years", "About 3.4 years", "About 68 years"], "C"),
    "Doubling time under exponential growth",
    "Doubling means Nₜ/N₀ = 2 = e^(rt), so rt = ln 2 and t = 0.693/0.0205 ≈ 33.8, i.e. about 34 years.",
    ["2 = e^(rt) → t = ln 2 / r", "t = 0.693/0.0205 ≈ 33.8 years"],
    C12_OP("population growth: exponential growth"),
    shortcut="Doubling time ≈ 0.693/r.",
    why="49 years is 1/r (ln 2 left out); 3.4 years is a decimal slip; 68 years uses ln 4, the time to quadruple.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    ms("A plant species is introduced into an island where none of its natural predators or competitors occurs. Based "
       "on the examples and principles in NCERT, which of the following statements are reasonable?",
       ["Its population may spread rapidly, as the prickly pear cactus did in Australia.",
        "Introducing a predator from its natural habitat may bring it under control.",
        "Native species using the same resources may decline or even become extinct because of competition.",
        "It cannot become invasive, because invasion requires the presence of natural predators.",
        "Its population will grow exponentially for ever, because the resources of an island are unlimited."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
    "Exotic species, predators and competition",
    "(a) Reasonable: NCERT notes that exotic species introduced into an area become invasive and spread fast because "
    "the invaded land lacks their natural predators; the prickly pear cactus in Australia is its example. (b) "
    "Reasonable: the cactus was brought under control only after a cactus-feeding predator (a moth) from its natural "
    "habitat was introduced. (c) Reasonable: the Abingdon tortoise became extinct within a decade of goats arriving on "
    "its island. (d) is the reverse of the truth. (e) is false: no population in nature has unlimited resources, so "
    "exponential growth cannot continue indefinitely.",
    ["(a), (b), (c): reasonable", "(d): false, absence of predators favours invasion",
     "(e): false, resources are always limited"],
    C12_OP("population interactions: predation and competition; population growth"),
    why="Options with (d) or (e) are wrong.",
    seconds=70)

# Logistic growth with K = 1000.
_op_K = 1000
_op_rate = {N: N * (_op_K - N) / _op_K for N in (500, 900)}         # in units of r
_op_pc = {N: (_op_K - N) / _op_K for N in (500, 900)}               # per capita, in units of r
assert _op_rate[500] == 250 > _op_rate[900] == 90 and _op_pc[500] == 0.5 != _op_pc[900] == 0.1

add(OAP, "Population growth", "Advanced", "statement_pair",
    sp("For a population growing logistically according to dN/dt = rN[(K − N)/K] with K = 1000, the growth rate dN/dt "
       "is greater when N = 500 than when N = 900.",
       "In the same population, the per capita growth rate is the same when N = 500 and when N = 900."),
    SP("C"),
    "Growth rate and per capita rate in logistic growth",
    "At N = 500: dN/dt = r × 500 × 500/1000 = 250r. At N = 900: dN/dt = r × 900 × 100/1000 = 90r. So Statement I is "
    "true. The per capita growth rate, (1/N)(dN/dt) = r(K − N)/K, is 0.5r at N = 500 and only 0.1r at N = 900; it "
    "falls as N approaches K, so Statement II is false.",
    ["N = 500: 250r; N = 900: 90r → Statement I true", "Per capita: 0.5r versus 0.1r → Statement II false"],
    C12_OP("population growth: logistic growth"),
    seconds=70, verified_by=RECOMPUTED)

# N = 1000, b = 0.05, d = 0.07, I = 30, E = 0.
_op_N, _op_b, _op_d = 1000, F(5, 100), F(7, 100)
assert _op_N * (_op_b - _op_d) == -20 and _op_N * (_op_b - _op_d) + 30 == 10

add(OAP, "Population attributes", "Advanced", "statement_pair",
    sp("A closed population (no immigration or emigration) of 1000 individuals with a per capita birth rate of 0.05 "
       "and a per capita death rate of 0.07 per year is declining.",
       "If, during the year, 30 individuals immigrate into this population of 1000 and none emigrate, the population "
       "will increase in size."),
    SP("A"),
    "Births, deaths and immigration together",
    "Statement I: births = 0.05 × 1000 = 50 and deaths = 0.07 × 1000 = 70, so a closed population loses 20 a year: it "
    "is declining (true). Statement II: N(t+1) = N(t) + [(B + I) − (D + E)] = 1000 + [(50 + 30) − (70 + 0)] = 1010, "
    "an increase (true).",
    ["B = 50, D = 70 → net −20 (declining)", "With I = 30: 1000 + 80 − 70 = 1010 (increasing)"],
    C12_OP("populations: population attributes and growth"),
    seconds=60, verified_by=RECOMPUTED)



# ================================================================ Ecosystem (4 / 5 / 4)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Energy flow", "Basic", "statement_pair",
    sp("Of the incident solar radiation, less than 50 per cent is photosynthetically active radiation (PAR).",
       "Low temperature and anaerobiosis inhibit decomposition, resulting in the build-up of organic materials."),
    SP("A"),
    "PAR; conditions that slow decomposition",
    "NCERT: of the incident solar radiation, less than 50 per cent is photosynthetically active radiation, and plants "
    "capture only 2–10 per cent of the PAR (Statement I true). Warm and moist environments favour decomposition, "
    "whereas low temperature and anaerobiosis inhibit it, resulting in the build-up of organic materials (Statement "
    "II true).",
    ["Statement I: true", "Statement II: true"],
    C12_EC("energy flow; decomposition"),
    seconds=25)

add(ECO, "Structure and components", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Standing crop", "Detritus", "Stratification", "Species composition"],
       ["Vertical distribution of different species occupying different levels",
        "Identification and enumeration of the plant and animal species of an ecosystem",
        "Mass of living material at a trophic level at a particular time",
        "Dead plant remains such as leaves, bark and flowers, and dead remains of animals, including fecal matter"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "III", "B": "I", "C": "IV", "D": "II"}], "B"),
    "Basic ecosystem terms",
    "Standing crop: the mass of living material at a trophic level at a particular time. Detritus: dead plant remains "
    "(leaves, bark, flowers) and dead remains of animals, including fecal matter, the raw material for decomposition. "
    "Stratification: the vertical distribution of different species occupying different levels (trees, shrubs, "
    "herbs and grasses in a forest). Species composition: identification and enumeration of the plant and animal "
    "species of an ecosystem.",
    ["A-III", "B-IV", "C-I", "D-II"],
    C12_EC("ecosystem: structure and function; decomposition; energy flow"),
    why="The other codes swap standing crop with detritus, or stratification with species composition.",
    seconds=35)

add(ECO, "Productivity and decomposition", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Primary production", "Gross primary productivity", "Net primary productivity", "Secondary productivity"],
       ["Rate of production of organic matter during photosynthesis",
        "Rate of formation of new organic matter by consumers",
        "Amount of biomass or organic matter produced per unit area over a time period by plants during "
        "photosynthesis",
        "Gross primary productivity minus the respiration losses of plants"]),
    M({"A": "III", "B": "I", "C": "IV", "D": "II"},
      [{"A": "I", "B": "III", "C": "IV", "D": "II"},
       {"A": "III", "B": "I", "C": "II", "D": "IV"},
       {"A": "II", "B": "I", "C": "IV", "D": "III"}], "B"),
    "Productivity terms",
    "NCERT: primary production is the amount of biomass or organic matter produced per unit area over a time period "
    "by plants during photosynthesis. Gross primary productivity is the rate of production of organic matter during "
    "photosynthesis. Net primary productivity is GPP minus respiration losses (R) of plants. Secondary productivity is "
    "the rate of formation of new organic matter by consumers.",
    ["A-III", "B-I", "C-IV", "D-II"],
    C12_EC("productivity"),
    why="The other codes swap the amount (primary production) with the rate (GPP), or give secondary productivity to "
        "producers.",
    seconds=35)

add(ECO, "Structure and components", "Basic", "multi_statement",
    ms("Which of the following are listed in NCERT as aquatic ecosystems?",
       ["Lake", "Wetland", "Estuary", "Grassland", "River"]),
    MS(["a", "b", "c", "e"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "c", "d", "e"]], "D"),
    "Types of ecosystems",
    "NCERT divides ecosystems into terrestrial and aquatic. Forest, grassland and desert are terrestrial; pond, lake, "
    "wetland, river and estuary are aquatic. Crop fields and an aquarium may be considered man-made ecosystems.",
    ["Aquatic: pond, lake, wetland, river, estuary", "Grassland: terrestrial"],
    C12_EC("ecosystem: structure and function"),
    why="Any option containing (d) includes a terrestrial ecosystem; '(a), (c) and (e)' leaves out the wetland.",
    seconds=25)

# Biosphere NPP 170 billion t; oceans 55 billion t.
_ec_land = F(170 - 55, 170)
assert 67 < float(_ec_land) * 100 < 68 and 32 < 55 / 170 * 100 < 33

add(ECO, "Productivity and decomposition", "Intermediate", "numerical",
    "NCERT states that the annual net primary productivity of the whole biosphere is approximately 170 billion tons "
    "(dry weight) of organic matter, and that the oceans, despite occupying about 70 per cent of the surface, "
    "contribute only 55 billion tons of it. Approximately what percentage of the biosphere's annual net primary "
    "productivity comes from land?",
    P("About 68 per cent", ["About 32 per cent", "About 30 per cent", "About 70 per cent"], "D"),
    "Contribution of land and oceans to global productivity",
    "Land contributes 170 − 55 = 115 billion tons. 115/170 × 100 ≈ 67.6 per cent, i.e. about 68 per cent, even "
    "though land covers only about 30 per cent of the surface.",
    ["Land NPP = 170 − 55 = 115 billion t", "115/170 ≈ 0.676 → about 68%"],
    C12_EC("productivity"),
    why="32 per cent is the oceans' share; 30 per cent is the land's share of the earth's surface, not of "
        "productivity; 70 per cent is the oceans' share of the surface.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Intermediate", "multi_statement",
    ms("Which of the following conditions would slow down the decomposition of detritus?",
       ["Detritus rich in lignin", "Detritus rich in chitin", "Low temperature",
        "Anaerobic conditions in waterlogged soil", "A warm and moist environment"]),
    MS(["a", "b", "c", "d"], [["a", "b", "e"], ["c", "d", "e"], ["a", "c", "d"]], "A"),
    "Factors regulating decomposition",
    "NCERT: decomposition is controlled by the chemical composition of detritus and by climatic factors. It is slower "
    "when detritus is rich in lignin and chitin and quicker when it is rich in nitrogen and water-soluble substances "
    "like sugars. Warm and moist environments favour decomposition, whereas low temperature and anaerobiosis inhibit "
    "it. So (a)-(d) slow it; (e) speeds it up.",
    ["(a), (b): chemical composition that slows decomposition", "(c), (d): climatic conditions that inhibit it",
     "(e): favours decomposition"],
    C12_EC("decomposition"),
    why="Options containing (e) include a condition that favours decomposition; '(a), (c) and (d)' leaves out chitin.",
    seconds=40)

add(ECO, "Energy flow", "Intermediate", "assertion_reason",
    ar("The sun is not the source of energy for the deep-sea hydrothermal ecosystem.",
       "Plants capture only 2–10 per cent of the photosynthetically active radiation."),
    AR("B"),
    "Source of energy for ecosystems",
    "A is true: NCERT says that except for the deep-sea hydrothermal ecosystem, the sun is the only source of energy "
    "for all ecosystems on Earth. R is also true, but it concerns how much of the sunlight plants capture in sunlit "
    "ecosystems; it says nothing about why a deep-sea hydrothermal ecosystem does not run on solar energy. So R is not "
    "the explanation of A.",
    ["A: true (the stated exception)", "R: true", "R is about efficiency of capture, not about the deep sea: "
     "not the explanation"],
    C12_EC("energy flow"),
    seconds=30)

# NPP = GPP - respiration.
_ec_P = 20000 * F(75, 100)
_ec_Q = 30000 * F(40, 100)
assert _ec_P == 15000 and _ec_Q == 12000 and _ec_P - _ec_Q == 3000

add(ECO, "Productivity and decomposition", "Intermediate", "direct",
    "Grassland P has a gross primary productivity of 20,000 kJ m⁻² yr⁻¹, and its plants use 25 per cent of it in "
    "respiration. Forest Q has a gross primary productivity of 30,000 kJ m⁻² yr⁻¹, and its plants use 60 per cent of "
    "it in respiration. Which ecosystem has more biomass available for consumption by heterotrophs, and by how much?",
    P("P, by 3,000 kJ m⁻² yr⁻¹", ["Q, by 10,000 kJ m⁻² yr⁻¹", "Q, by 3,000 kJ m⁻² yr⁻¹",
                                   "P, by 13,000 kJ m⁻² yr⁻¹"], "C"),
    "Net primary productivity is what heterotrophs can use",
    "The biomass available to heterotrophs (herbivores and decomposers) is the net primary productivity, NPP = GPP − "
    "R. P: 20,000 − 5,000 = 15,000. Q: 30,000 − 18,000 = 12,000. P exceeds Q by 3,000 kJ m⁻² yr⁻¹.",
    ["NPP(P) = 20,000 × 0.75 = 15,000", "NPP(Q) = 30,000 × 0.40 = 12,000", "Difference = 3,000 in favour of P"],
    C12_EC("productivity"),
    why="'Q by 10,000' compares GPP instead of NPP; 'Q by 3,000' gets the difference right but the ecosystem wrong; "
        "'P by 13,000' compares respiration losses (18,000 − 5,000).",
    seconds=60, verified_by=RECOMPUTED)

add(ECO, "Ecological pyramids", "Intermediate", "assertion_reason",
    ar("The standing crop of a trophic level is measured as the biomass of living organisms or as their number in a "
       "unit area.",
       "For expressing biomass, fresh weight is a more accurate measure than dry weight."),
    AR("C"),
    "Measuring standing crop and biomass",
    "A is true: NCERT says the standing crop is measured as the biomass of living organisms (biomass) or the number in "
    "a unit area. R is false: the biomass of a species is expressed in terms of fresh or dry weight, but measurement "
    "of biomass in terms of dry weight is more accurate.",
    ["A: true", "R: false (dry weight is more accurate)"],
    C12_EC("energy flow; ecological pyramids"),
    seconds=30)

add(ECO, "Energy flow", "Advanced", "multi_statement",
    ms("In a food web, grass is eaten by rabbits and grasshoppers; sparrows eat grass seeds and grasshoppers; frogs eat "
       "grasshoppers; snakes eat frogs and rabbits; hawks eat snakes and sparrows. Taking producers as the first "
       "trophic level, which of the following statements are correct?",
       ["The sparrow occupies the second and third trophic levels.",
        "The hawk can occupy the fifth trophic level.",
        "The frog is a primary consumer.",
        "The snake occupies the third and fourth trophic levels.",
        "If the grass disappeared, only the rabbits and grasshoppers would be affected."]),
    MS(["a", "b", "d"], [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "c", "d"]], "B"),
    "Organisms at more than one trophic level",
    "(a) True: eating seeds, the sparrow is a primary consumer (2nd level); eating grasshoppers, a secondary consumer "
    "(3rd). (d) True: snake eating rabbit (2nd) is at the 3rd level; snake eating frog (frog eats grasshopper: 3rd) is "
    "at the 4th. (b) True: a hawk eating a snake that ate a frog is at the 5th level (it can also be at the 3rd or 4th "
    "via sparrows or rabbit-eating snakes). (c) False: the frog eats herbivorous grasshoppers, so it is a secondary "
    "consumer (primary carnivore). (e) False: all consumers depend on producers directly or indirectly.",
    ["Sparrow: 2nd and 3rd", "Snake: 3rd and 4th", "Hawk: up to 5th", "Frog: secondary consumer", "Loss of grass "
     "affects every consumer"],
    C12_EC("energy flow: food chains and trophic levels"),
    why="Options with (c) or (e) are wrong; 'b, d and e' also leaves out the sparrow.",
    seconds=90)

# 10 per cent law: 20,000 kJ at producers; top carnivore receives 2 kJ.
_ec_levels = 1 + round(math.log10(20000 / 2))
assert _ec_levels == 5

add(ECO, "Energy flow", "Advanced", "direct",
    "In a grazing food chain, the producers fix 20,000 kJ of energy, and only 10 per cent of the energy is transferred "
    "from each trophic level to the next. If the top carnivore of the chain receives 2 kJ, at which trophic level is "
    "it (taking producers as the first level)?",
    P("Fifth", ["Fourth", "Sixth", "Third"], "A"),
    "Using the 10 per cent law to count trophic levels",
    "Energy falls tenfold at each step: 20,000 (1st, producers) → 2,000 (2nd) → 200 (3rd) → 20 (4th) → 2 (5th). So "
    "the top carnivore is at the fifth trophic level. This rapid fall is why the number of trophic levels in a grazing "
    "food chain is restricted.",
    ["20,000 → 2,000 → 200 → 20 → 2", "Four transfers → fifth trophic level"],
    C12_EC("energy flow: 10 per cent law"),
    why="'Fourth' counts the transfers (4) instead of the levels; 'sixth' adds one level too many; 'third' would "
        "receive 200 kJ.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Ecological pyramids", "Advanced", "assertion_reason",
    ar("Because of the 10 per cent law of energy transfer, the pyramid of biomass of every ecosystem must be upright.",
       "The pyramid of energy is always upright, because some energy is always lost as heat at each step of energy "
       "flow from one trophic level to the next."),
    AR("D"),
    "Biomass and energy pyramids can differ",
    "A is false: the pyramid of biomass in a sea is generally inverted, because the biomass of fishes far exceeds that "
    "of phytoplankton; energy transfer rules do not fix the standing biomass at any moment. R is true: NCERT says the "
    "pyramid of energy is always upright and can never be inverted, because some energy is always lost as heat at "
    "each step.",
    ["A: false (inverted biomass pyramid in a sea)", "R: true"],
    C12_EC("ecological pyramids"),
    seconds=40)

_ec_frac = F(2, 100) * F(1, 2)
assert _ec_frac == F(1, 100)

add(ECO, "Ecological pyramids", "Advanced", "statement_pair",
    sp("Since less than 50 per cent of the incident solar radiation is PAR, and plants capture only 2–10 per cent of "
       "the PAR, plants capturing 2 per cent of the PAR fix less than 1 per cent of the incident solar radiation.",
       "Because producers fix such a small fraction of the incident radiation, they form the narrowest bar of the "
       "pyramid of energy."),
    SP("C"),
    "Small capture of sunlight versus the shape of the energy pyramid",
    "Statement I: 2% of less than 50% is less than 1% of the incident radiation (true). Statement II is false: the "
    "pyramid of energy compares the energy present at successive trophic levels, not the energy fixed compared with "
    "sunlight. Producers hold the most energy of any trophic level and form the widest bar at the base; the bars "
    "narrow towards the top carnivores, and the pyramid is always upright.",
    ["2% × (< 50%) < 1% → Statement I true", "Producers form the base (widest bar) → Statement II false"],
    C12_EC("energy flow; ecological pyramids"),
    seconds=50, verified_by=RECOMPUTED)



# ================================================================ Biodiversity and Conservation (4 / 5 / 4)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "According to NCERT, India has nearly how many species of plants, with roughly twice as many species of animals?",
    P("45,000", ["4,500", "1,00,000", "7,00,000"], "A"),
    "India's recorded species diversity",
    "NCERT: although India has only 2.4 per cent of the world's land area, its share of global species diversity is "
    "8.1 per cent. India has nearly 45,000 species of plants and twice as many of animals.",
    ["Plants: about 45,000", "Animals: about twice as many"],
    C12_BD("biodiversity: biodiversity in India"),
    why="4,500 is ten times too small; 1,00,000 is NCERT's figure for plant species India may yet discover; 7,00,000 "
        "has no basis in NCERT.",
    seconds=20)

add(BDC, "In situ and ex situ conservation", "Basic", "direct",
    "At the World Summit on Sustainable Development held in 2002, 190 countries pledged to achieve, by 2010, a "
    "significant reduction in the current rate of biodiversity loss. Where was this summit held?",
    P("Johannesburg, South Africa",
      ["Rio de Janeiro, Brazil", "Stockholm, Sweden", "New Delhi, India"], "C"),
    "International efforts for conservation",
    "NCERT: the historic Convention on Biological Diversity ('the Earth Summit') was held in Rio de Janeiro in 1992. "
    "The World Summit on Sustainable Development was held in 2002 in Johannesburg, South Africa, where 190 countries "
    "pledged to significantly reduce the rate of biodiversity loss by 2010.",
    ["1992: Earth Summit, Rio de Janeiro", "2002: WSSD, Johannesburg"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity"),
    why="Rio de Janeiro hosted the 1992 Earth Summit; Stockholm and New Delhi are not named in NCERT for these "
        "summits.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Basic", "statement_pair",
    sp("According to the IUCN (2004), the total number of plant and animal species described so far is slightly more "
       "than 1.5 million.",
       "Insects make up more than 70 per cent of all animal species, so that out of every 10 animals on the planet, 7 "
       "are insects."),
    SP("A"),
    "How many species are known",
    "NCERT: according to the IUCN (2004), the total number of plant and animal species described so far is slightly "
    "more than 1.5 million (Statement I true). Among animals, insects are the most species-rich group, making up more "
    "than 70 per cent of the total; out of every 10 animals on this planet, 7 are insects (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_BD("biodiversity: how many species are there on earth"),
    seconds=25)

add(BDC, "Importance and loss", "Basic", "match_list",
    ml(("example", "cause of biodiversity loss (the 'Evil Quartet')"),
       ["Extinction of Steller's sea cow and the passenger pigeon",
        "Extinction of more than 200 species of cichlid fish in Lake Victoria",
        "Clearing of the Amazon rain forest for soya bean cultivation and cattle grazing",
        "Extinction of the unique parasites of a host fish species that has become extinct"],
       ["Co-extinction", "Alien species invasion", "Over-exploitation", "Habitat loss and fragmentation"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "II", "B": "III", "C": "IV", "D": "I"},
       {"A": "III", "B": "II", "C": "I", "D": "IV"},
       {"A": "IV", "B": "II", "C": "III", "D": "I"}], "D"),
    "Causes of biodiversity loss",
    "Steller's sea cow and the passenger pigeon became extinct in the last 500 years due to over-exploitation by "
    "humans. The Nile perch introduced into Lake Victoria (an alien species invasion) led to the extinction of more "
    "than 200 species of cichlid fish. Clearing the Amazon forest for soya beans and beef cattle is habitat loss. When "
    "a host fish species becomes extinct, its unique assemblage of parasites also meets the same fate: co-extinction.",
    ["A-III", "B-II", "C-IV", "D-I"],
    C12_BD("loss of biodiversity: causes of biodiversity losses"),
    why="The other codes swap over-exploitation with alien invasion, or habitat loss with co-extinction.",
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "assertion_reason",
    ar("When large habitats are broken up into small fragments by human activities, mammals and birds requiring large "
       "territories are badly affected, leading to population declines.",
       "Fragmentation leaves only small pieces of habitat, which cannot provide the large territories these animals "
       "need."),
    AR("A"),
    "Effect of habitat fragmentation",
    "NCERT: when large habitats are broken up into small fragments due to various human activities, mammals and birds "
    "requiring large territories, and certain animals with migratory habits, are badly affected, leading to "
    "population declines. The reason is in R: small fragments cannot supply the large territories such animals "
    "require.",
    ["A: true", "R: true", "Small fragments cannot meet large-territory needs: R explains A"],
    C12_BD("loss of biodiversity: habitat loss and fragmentation"),
    seconds=30)

add(BDC, "In situ and ex situ conservation", "Intermediate", "multi_statement",
    ms("Which of the following statements about ex situ conservation are correct?",
       ["Gametes of threatened species can be preserved in viable and fertile condition for long periods using "
        "cryopreservation techniques.",
        "Eggs can be fertilised in vitro.",
        "Plants can be propagated using tissue culture methods.",
        "Wildlife safari parks are a means of in situ conservation.",
        "Seeds of different genetic strains of commercially important plants can be kept for long periods in seed "
        "banks."]),
    MS(["a", "b", "c", "e"], [["a", "b", "c", "d"], ["a", "c", "d", "e"], ["b", "d", "e"]], "B"),
    "Methods of ex situ conservation",
    "In ex situ conservation, threatened animals and plants are taken out of their natural habitat and placed in "
    "special settings: zoological parks, botanical gardens and wildlife safari parks. NCERT adds that gametes can be "
    "cryopreserved, eggs fertilised in vitro, plants propagated by tissue culture, and seeds of commercially "
    "important plants kept for long periods in seed banks. (d) is false: wildlife safari parks are ex situ.",
    ["(a), (b), (c), (e): true", "(d): false, safari parks are ex situ"],
    C12_BD("biodiversity conservation: ex situ conservation"),
    why="Options containing (d) are wrong; '(b), (d) and (e)' also leaves out (a) and (c).",
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "match_list",
    ml(("idea", "description in NCERT"),
       ["Narrowly utilitarian argument", "Broadly utilitarian argument", "Ethical argument", "Bioprospecting"],
       ["Every species has an intrinsic value, even if it is not of current economic value to us",
        "Exploring molecular, genetic and species-level diversity for products of economic importance",
        "Direct economic benefits such as food, firewood, fibre, construction material and medicinal products",
        "Ecosystem services such as oxygen production, pollination and aesthetic pleasures"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "II", "B": "IV", "C": "I", "D": "III"}], "A"),
    "Why we should conserve biodiversity",
    "Narrowly utilitarian: humans derive countless direct economic benefits from nature (food, firewood, fibre, "
    "construction material, industrial products, medicinal products). Broadly utilitarian: biodiversity provides "
    "ecosystem services, such as the Amazon producing about 20% of the earth's oxygen, pollination by bees, birds and "
    "bats, and aesthetic pleasures. Ethical: every species has an intrinsic value. Bioprospecting: exploring "
    "molecular, genetic and species-level diversity for products of economic importance.",
    ["A-III", "B-IV", "C-I", "D-II"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity"),
    why="The other codes swap the narrowly and broadly utilitarian arguments, or the ethical argument with "
        "bioprospecting.",
    seconds=40)

# IUCN (2004): 784 extinctions = 338 vertebrates + 359 invertebrates + 87 plants.
assert 338 + 359 + 87 == 784 and 359 > 338 and 87 < 784 / 2

add(BDC, "Hotspots and Red Data Book", "Intermediate", "statement_pair",
    sp("Among the 784 extinctions of the last 500 years documented in the IUCN Red List (2004), invertebrate species "
       "outnumber vertebrate species.",
       "Plants account for more than half of these 784 documented extinctions."),
    SP("C"),
    "Reading the IUCN Red List figures",
    "The IUCN Red List (2004) documents 784 extinctions in the last 500 years: 338 vertebrates, 359 invertebrates and "
    "87 plants. Invertebrates (359) outnumber vertebrates (338), so Statement I is true. Plants (87) are far fewer "
    "than half of 784, so Statement II is false.",
    ["338 + 359 + 87 = 784", "359 > 338 → Statement I true", "87 ≪ 392 → Statement II false"],
    C12_BD("loss of biodiversity"),
    seconds=40, verified_by=RECOMPUTED)

add(BDC, "Patterns of biodiversity", "Intermediate", "assertion_reason",
    ar("The ecological diversity of Norway is greater than that of India.",
       "India has a great variety of ecosystems, such as deserts, rain forests, mangroves, coral reefs, wetlands, "
       "estuaries and alpine meadows."),
    AR("D"),
    "Ecological diversity",
    "Ecological diversity is diversity at the ecosystem level. NCERT: India, with its deserts, rain forests, "
    "mangroves, coral reefs, wetlands, estuaries and alpine meadows, has a greater ecosystem diversity than a "
    "Scandinavian country like Norway. So A is false and R is true.",
    ["A: false (India has the greater ecological diversity)", "R: true"],
    C12_BD("biodiversity: levels of biodiversity"),
    seconds=30)

_bd_total = 1.5 / 0.22
assert 6.7 < _bd_total < 6.9 and abs(1.5 * 0.22 - 0.33) < 1e-9

add(BDC, "Patterns of biodiversity", "Advanced", "direct",
    "The IUCN (2004) puts the number of species described so far at slightly more than 1.5 million. If, as Robert "
    "May's estimate implies, only about 22 per cent of all species have been described, the total global species "
    "diversity works out to roughly:",
    P("7 million", ["0.33 million", "1.8 million", "70 million"], "D"),
    "Estimating global species diversity",
    "If 1.5 million species are 22 per cent of the total, the total = 1.5/0.22 ≈ 6.8 million, i.e. about 7 million. "
    "This matches Robert May's global estimate of species diversity, about 7 million.",
    ["Total × 0.22 = 1.5 million", "Total = 1.5/0.22 ≈ 6.8 ≈ 7 million"],
    C12_BD("biodiversity: how many species are there on earth"),
    why="0.33 million multiplies 1.5 by 0.22 instead of dividing; 1.8 million adds 22 per cent to 1.5 million; 70 "
        "million is a factor-of-ten slip.",
    seconds=50, verified_by=RECOMPUTED)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Which of the following are examples of the effect of alien species invasions given in NCERT?",
       ["The introduction of the Nile perch into Lake Victoria",
        "Carrot grass (Parthenium)",
        "Lantana",
        "Water hyacinth (Eichhornia)",
        "The extinction of Steller's sea cow"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "C"),
    "Alien species invasions",
    "NCERT: when alien species are introduced unintentionally or deliberately, some of them turn invasive and cause "
    "decline or extinction of indigenous species. Examples: the Nile perch in Lake Victoria (extinction of more than "
    "200 cichlid species); the invasive weeds carrot grass (Parthenium), Lantana and water hyacinth (Eichhornia), "
    "which threaten native species; and the illegal introduction of the African catfish Clarias gariepinus. Steller's "
    "sea cow became extinct through over-exploitation, not invasion.",
    ["(a)-(d): alien species invasions", "(e): over-exploitation"],
    C12_BD("loss of biodiversity: alien species invasions"),
    why="Options with (e) mix in over-exploitation; '(b), (c) and (d)' leaves out the Nile perch.",
    seconds=45)

# log S = log C + Z log A: S ratio for a tenfold area increase = 10^Z.
_bd_region, _bd_cont = 10 ** 0.1, 10 ** 1.0
assert abs(_bd_region - 1.26) < 0.01 and _bd_cont == 10

add(BDC, "Patterns of biodiversity", "Advanced", "direct",
    "Species richness follows log S = log C + Z log A. Take Z = 0.1 for areas within a region and Z = 1.0 for very "
    "large areas such as whole continents (both within NCERT's ranges). When the area studied increases tenfold, by "
    "about what factor does species richness increase in each case?",
    P("About 1.26 times within a region, but 10 times at the continental scale",
      ["About 1.26 times in both cases",
       "10 times within a region, but about 1.26 times at the continental scale",
       "About 1.1 times within a region, but 2 times at the continental scale"], "B"),
    "Effect of the slope Z",
    "From the equation, S₂/S₁ = (A₂/A₁)^Z. For a tenfold area increase: within a region, 10^0.1 ≈ 1.26; at the "
    "continental scale, 10^1.0 = 10. NCERT notes that Z lies between 0.1 and 0.2 within a region but is much steeper "
    "(0.6 to 1.2) for very large areas such as entire continents.",
    ["S₂/S₁ = 10^Z", "Z = 0.1 → ≈ 1.26", "Z = 1.0 → 10"],
    C12_BD("patterns of biodiversity: species-area relationships"),
    why="'1.26 in both' ignores the steeper continental slope; the third option swaps the two cases; 1.1 and 2 come "
        "from adding Z to 1 instead of raising 10 to the power Z.",
    seconds=75, verified_by=RECOMPUTED)

add(BDC, "Hotspots and Red Data Book", "Advanced", "statement_pair",
    sp("According to the percentages given in NCERT, a smaller proportion of gymnosperm species than of bird species "
       "faces the threat of extinction.",
       "According to the same percentages, a larger proportion of amphibian species than of mammal species faces the "
       "threat of extinction."),
    SP("D"),
    "Comparing threatened proportions across groups",
    "NCERT: presently, 12 per cent of all bird species, 23 per cent of all mammal species, 32 per cent of all "
    "amphibian species and 31 per cent of all gymnosperm species in the world face the threat of extinction. "
    "Gymnosperms (31%) face a larger, not smaller, proportion than birds (12%), so Statement I is false. Amphibians "
    "(32%) exceed mammals (23%), so Statement II is true.",
    ["Birds 12%, mammals 23%, amphibians 32%, gymnosperms 31%", "31 > 12 → Statement I false",
     "32 > 23 → Statement II true"],
    C12_BD("loss of biodiversity"),
    seconds=45)
# ---------------------------------------------------------------- checks and output
def main():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    quota = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                     for d, n in t["quota"].items() if n})
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}

    for i, q in enumerate(QUESTIONS):
        q["question_id"] = f"NEET_BOT_{FIRST_ID + i:06d}"
        assert q["subtopic"] in subtopics[q["topic"]], (q["topic"], q["subtopic"])
    assert len(QUESTIONS) == pkg["count"] == 128, len(QUESTIONS)
    assert [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]] == pkg["question_ids"]
    have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
    assert have == quota, {k: (have[k], quota[k]) for k in set(have) | set(quota) if have[k] != quota[k]}
    order = [q["topic"] for q in QUESTIONS]
    assert sorted(order, key=pkg["topics"].index) == order       # topics in plan order

    fmts = Counter(q["format"] for q in QUESTIONS)
    keys = Counter(q["correct_answer"] for q in QUESTIONS)
    n = len(QUESTIONS)
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))
    for f in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f] >= 0.08 * n, (f, fmts[f])
    assert 0.04 * n <= fmts["numerical"] <= 0.08 * n, fmts["numerical"]
    assert all(0.22 * n <= keys[k] <= 0.28 * n for k in LETTERS), keys
    for q in QUESTIONS:
        if q["format"] == "numerical":
            assert "script:recompute" in q["verification"]["verified_by"], q["question_id"]
        if q["format"] == "assertion_reason":
            assert q["question_text"].count("Assertion (A):") == 1
    texts = [q["question_text"] for q in QUESTIONS]
    assert len(set(texts)) == len(texts)

    doc = {"schema_version": "1.0", "batch_id": "BATCH_006", "created_at": TODAY,
           "notes": "BATCH_006 package BOT_006_p2: 128 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 to "
                    "BATCH_005 were avoided or approached from a new angle. Numerical and other computable answers re-derived by "
                    "tools/batch_006/BOT_006_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()

