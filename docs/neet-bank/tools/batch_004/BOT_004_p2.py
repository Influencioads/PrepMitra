"""Builder for BATCH_004, package BOT_004_p2 (Botany, NEET_BOT_000874..NEET_BOT_001000, 127 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Facts already tested in BATCH_000 to BATCH_003 on these topics were avoided (see
`python tools/merge_batch.py stems 004 BOT_004_p2`). Numerical answers are re-derived below; the file is written
only if every assert, the plan quota, the format mix and the answer-key balance pass.

    cd docs/neet-bank && python tools/batch_004/BOT_004_p2.py
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
PACKAGE = "BOT_004_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_004_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_004_BOT_p2.json"
FIRST_ID = 874

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


# ================================================================ Plant Growth and Development (4 / 4 / 4)
C11_PGD = lambda s: ref(11, PGD, s)

add(PGD, "Plant growth regulators", "Basic", "multi_statement",
    ms("Which of the following statements about plant growth regulators (PGRs) are correct?",
       ["PGRs are also variously described as plant growth substances, plant hormones or phytohormones.",
        "Growth promoters are involved in activities such as cell division, cell enlargement, pattern formation, "
        "tropic growth, flowering, fruiting and seed formation.",
        "Growth-inhibiting PGRs play an important role in plant responses to wounds and to stresses of biotic and "
        "abiotic origin, and in dormancy and abscission.",
        "Abscisic acid belongs to the group of plant growth promoters.",
        "Auxins, gibberellins and cytokinins belong to the group of plant growth inhibitors."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Classification of PGRs by function",
    "PGRs are small, simple molecules of diverse chemical composition, also called plant growth substances, plant "
    "hormones or phytohormones. One group promotes growth (cell division, cell enlargement, pattern formation, "
    "tropic growth, flowering, fruiting, seed formation): auxins, gibberellins and cytokinins. The other group acts "
    "in responses to wounds and stresses and in growth-inhibiting activities such as dormancy and abscission: "
    "abscisic acid belongs here.",
    ["(a), (b), (c): true", "(d): false, ABA is an inhibitor", "(e): false, these three are promoters"],
    C11_PGD("plant growth regulators: characteristics"),
    why="Every other option includes (d) or (e), which swap the promoter and inhibitor groups.",
    seconds=40)

add(PGD, "Germination and growth phases", "Basic", "match_list",
    ml(("term", "description"),
       ["Meristematic phase", "Phase of elongation", "Phase of maturation", "Redifferentiation"],
       ["Cells attain their maximal size in terms of wall thickening and protoplasmic modifications",
        "Cells derived from a dedifferentiated meristem again lose the capacity to divide and mature to perform "
        "specific functions",
        "Cells are rich in protoplasm, with large conspicuous nuclei and thin, primary, cellulosic walls having "
        "abundant plasmodesmatal connections",
        "Cells show increased vacuolation, cell enlargement and new cell wall deposition"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "D"),
    "Phases of growth and redifferentiation",
    "The constantly dividing cells at the root and shoot apex form the meristematic phase: rich protoplasm, large "
    "conspicuous nuclei, thin primary cellulosic walls with abundant plasmodesmata. Cells just behind it are in the "
    "phase of elongation (vacuolation, enlargement, new wall deposition). Further away lies the phase of "
    "maturation, where cells reach their maximal size in wall thickening and protoplasmic modification. Cells "
    "produced by a dedifferentiated meristem that again lose the capacity to divide are redifferentiated.",
    ["A-III", "B-IV", "C-I", "D-II"],
    C11_PGD("phases of growth; differentiation, dedifferentiation and redifferentiation"),
    why="Option A swaps the meristematic and elongation descriptions; option B swaps elongation and maturation; "
        "option C swaps maturation and redifferentiation.",
    seconds=45)

add(PGD, "Differentiation and redifferentiation", "Basic", "direct",
    "Plants follow different pathways in response to the environment or to phases of life, and so form different "
    "kinds of structures; heterophylly is an example. This ability of plants is called:",
    P("Plasticity", ["Dedifferentiation", "Apical dominance", "Senescence"], "B"),
    "Plasticity in plant development",
    "NCERT defines plasticity as the ability of plants to follow different pathways in response to the environment "
    "or phases of life to form different kinds of structures. Heterophylly (different leaf shapes in juvenile and "
    "mature plants, or in air and water) is the standard example.",
    ["Different structures in response to environment/phase of life → plasticity"],
    C11_PGD("development: plasticity"),
    why="Dedifferentiation is the regaining of the capacity to divide; apical dominance is the inhibition of lateral "
        "buds by the apical bud; senescence is ageing.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "Which plant growth regulator acts as a general plant growth inhibitor and an inhibitor of plant metabolism?",
    P("Abscisic acid", ["Gibberellic acid", "Zeatin", "Indole-3-acetic acid"], "C"),
    "Abscisic acid as a growth inhibitor",
    "NCERT states that ABA acts as a general plant growth inhibitor and an inhibitor of plant metabolism. It also "
    "inhibits seed germination and stimulates the closure of stomata.",
    ["General growth inhibitor + metabolic inhibitor → abscisic acid"],
    C11_PGD("plant growth regulators: abscisic acid"),
    why="Gibberellic acid, zeatin (a cytokinin) and IAA (an auxin) are all plant growth promoters.",
    seconds=25)

add(PGD, "Germination and growth phases", "Intermediate", "statement_pair",
    sp("Water is not needed for the extension growth of plant cells, because cell enlargement does not depend on "
       "the turgidity of cells.",
       "Every plant organism has an optimum temperature range best suited for its growth, and any deviation from "
       "this range could be detrimental to its survival."),
    SP("D"),
    "Conditions for growth",
    "Plant cells grow in size by cell enlargement, which requires water; turgidity of cells helps in extension "
    "growth, and water also provides the medium for enzymatic activities. So Statement I is false. NCERT also notes "
    "that every plant organism has an optimum temperature range best suited for its growth and deviation from it "
    "could be detrimental, so Statement II is true.",
    ["Statement I: false, turgidity helps extension growth", "Statement II: true"],
    C11_PGD("conditions for growth"),
    seconds=35)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Abscisic acid helps seeds to withstand desiccation and other factors unfavourable for growth.",
       "Abscisic acid breaks seed dormancy and initiates germination."),
    AR("C"),
    "Role of ABA in seeds",
    "ABA plays an important role in seed development, maturation and dormancy. By inducing dormancy, ABA helps seeds "
    "to withstand desiccation and other factors unfavourable for growth, so A is true. ABA induces dormancy and "
    "inhibits seed germination; it does not break dormancy, so R is false. (Breaking seed and bud dormancy is an "
    "effect of ethylene.)",
    ["A: true (via inducing dormancy)", "R: false, ABA induces dormancy and inhibits germination"],
    C11_PGD("plant growth regulators: abscisic acid"),
    seconds=35)

add(PGD, "Plant growth regulators", "Intermediate", "match_list",
    ml(("plant growth regulator", "physiological effect"),
       ["Auxin", "Gibberellin", "Cytokinin", "Ethylene"],
       ["Sprouting of potato tubers", "Adventitious shoot formation", "Prevents fruit and leaf drop at early stages",
        "Speeds up the malting process in the brewing industry"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
       {"A": "II", "B": "IV", "C": "III", "D": "I"}], "A"),
    "Physiological effects of PGRs",
    "Auxins prevent fruit and leaf drop at early stages (though they promote abscission of older, mature leaves and "
    "fruits). Gibberellins are used to speed up malting in brewing. Cytokinins help produce new leaves, chloroplasts, "
    "lateral shoot growth and adventitious shoots. Ethylene breaks seed and bud dormancy, including the sprouting of "
    "potato tubers.",
    ["A-III", "B-IV", "C-II", "D-I"],
    C11_PGD("plant growth regulators: physiological effects"),
    why="Option B swaps auxin and gibberellin; option C swaps cytokinin and ethylene; option D gives auxin the "
        "cytokinin effect.",
    seconds=45)

add(PGD, "Growth rate", "Intermediate", "multi_statement",
    ms("Which of the following statements about the measurement of plant growth are correct?",
       ["At the cellular level, growth is principally a consequence of an increase in the amount of protoplasm.",
        "Since an increase in protoplasm is difficult to measure directly, a quantity more or less proportional to "
        "it is generally measured.",
        "Growth is a reversible increase in the size of an organ or a cell.",
        "Growth is accompanied by anabolic and catabolic metabolic processes that occur at the expense of energy.",
        "The swelling of a piece of dry wood placed in water is an example of growth."]),
    MS(["a", "b", "d"], [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
    "Growth and its measurement",
    "Growth is an irreversible permanent increase in size of an organ, its parts or a cell, and it is accompanied by "
    "metabolic (anabolic and catabolic) processes at the expense of energy. At the cellular level growth is mainly "
    "an increase in protoplasm; since this is hard to measure directly, a proportional quantity (fresh or dry "
    "weight, length, area, volume, cell number) is measured. Swelling of dead wood in water is reversible physical "
    "imbibition, not growth.",
    ["(a), (b), (d): true", "(c): false, growth is irreversible", "(e): false, not growth"],
    C11_PGD("growth; growth is measurable"),
    why="Options A, C and D each include (c) or (e).",
    seconds=45)

add(PGD, "Germination and growth phases", "Advanced", "multi_statement",
    ms("Which of the following statements about primary and secondary growth are correct?",
       ["The root apical and shoot apical meristems are responsible for primary growth and principally contribute "
        "to elongation of the plant along its axis.",
        "In dicotyledonous plants and gymnosperms, the lateral meristems, vascular cambium and cork cambium, appear "
        "later in life.",
        "The lateral meristems increase the girth of the organs in which they are active; this is secondary growth.",
        "The lateral meristems are responsible for the elongation of the plant along its axis.",
        "Secondary growth by vascular cambium is a common feature of monocotyledons."]),
    MS(["a", "b", "c"], [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "c", "e"]], "A"),
    "Primary and secondary growth",
    "NCERT: the root and shoot apical meristems are responsible for primary growth and principally contribute to "
    "elongation along the axis. In dicotyledons and gymnosperms the lateral meristems, vascular cambium and cork "
    "cambium, appear later in life and increase the girth of the organs (secondary growth). Elongation is not their "
    "job, and monocots generally lack such secondary growth.",
    ["(a), (b), (c): true", "(d): false, lateral meristems increase girth", "(e): false"],
    C11_PGD("plant growth generally is indeterminate"),
    why="Option B includes (d); option C includes (e) and leaves out (a); option D adds (e).",
    seconds=50)

add(PGD, "Growth rate", "Advanced", "statement_pair",
    sp("A sigmoid growth curve is characteristic of a living organism growing in a natural environment, and it is "
       "typical for all cells, tissues and organs of a plant.",
       "With a limited nutrient supply, exponential growth cannot continue; growth slows down, leading to a "
       "stationary phase."),
    SP("A"),
    "Sigmoid growth curve",
    "In geometric growth the initial growth is slow (lag phase), then rapid (log or exponential phase). With limited "
    "nutrients the growth slows down to a stationary phase, giving an S-shaped (sigmoid) curve. NCERT states that "
    "a sigmoid curve is characteristic of a living organism growing in a natural environment and is typical for "
    "all cells, tissues and organs of a plant. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C11_PGD("growth rates: geometric growth"),
    seconds=35)

add(PGD, "Germination and growth phases", "Advanced", "assertion_reason",
    ar("Plants retain the capacity for unlimited growth throughout their life.",
       "Plants have meristems at certain locations in their body, whose cells have the capacity to divide and "
       "self-perpetuate."),
    AR("A"),
    "Indeterminate (open) growth",
    "NCERT: plant growth is unique because plants retain the capacity for unlimited growth throughout their life. "
    "This ability is due to the presence of meristems at certain locations in their body, whose cells can divide "
    "and self-perpetuate. R is exactly the cause of A.",
    ["A: true", "R: true", "Meristems → unlimited growth, so R explains A"],
    C11_PGD("plant growth generally is indeterminate"),
    seconds=35)

add(PGD, "Differentiation and redifferentiation", "Advanced", "statement_pair",
    sp("Development includes all the changes that an organism goes through during its life cycle, from germination "
       "of the seed to senescence.",
       "The act by which cells derived from the root apical and shoot apical meristems and the cambium mature to "
       "perform specific functions is termed dedifferentiation."),
    SP("C"),
    "Development and differentiation",
    "Development is the sum of all changes an organism goes through in its life cycle, from seed germination to "
    "senescence, so Statement I is true. Cells derived from the apical meristems and the cambium differentiate and "
    "mature to perform specific functions; this act leading to maturation is differentiation, not "
    "dedifferentiation (which is the regaining of the capacity to divide). Statement II is false.",
    ["Statement I: true", "Statement II: false, this is differentiation"],
    C11_PGD("differentiation, dedifferentiation and redifferentiation; development"),
    seconds=35)


# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

# 40 seeds, each from its own ovule by normal double fertilisation (one pollen tube with two male gametes per ovule)
n_seeds = 40
male_gametes = 2 * n_seeds                       # one fuses with the egg, one with the two polar nuclei
fusing_nuclei = n_seeds * ((1 + 1) + (1 + 2))    # syngamy: male + egg; triple fusion: male + two polar nuclei
assert (male_gametes, fusing_nuclei) == (80, 200)
assert n_seeds * 3 == 120 and n_seeds * 4 == 160 and n_seeds * 5 == 200   # distractors (see why_others_wrong)

# endosperm genotype: female AA (both polar nuclei carry A), male aa (male gamete carries a)
polar_nuclei, male_gamete, egg = ("A", "A"), "a", "A"
assert "".join(sorted(polar_nuclei + (male_gamete,))) == "AAa" and "".join(sorted(egg + male_gamete)) == "Aa"

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "match_list",
    ml(("plant or plant group", "feature described in NCERT"),
       ["Grasses", "Algae, bryophytes and pteridophytes", "Wheat, paddy and mango", "Papaya, watermelon and orchids"],
       ["Many ovules in the ovary", "Wind pollination is quite common",
        "A single ovule in the ovary", "Water is a regular mode of transport for the male gametes"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
    "Ovule number and pollinating agents",
    "The number of ovules in an ovary may be one (wheat, paddy, mango) or many (papaya, watermelon, orchids). Wind "
    "pollination is quite common in grasses. Water is a regular mode of transport for the male gametes among the "
    "lower plant groups such as algae, bryophytes and pteridophytes, whereas pollination by water is rare in "
    "flowering plants.",
    ["A-II", "B-IV", "C-III", "D-I"],
    C12_SR("the pistil, megasporangium (ovule); pollination: agents of pollination"),
    why="Option A swaps the two pollination statements; option B swaps the single-ovule and many-ovule groups; "
        "option D gives grasses many ovules.",
    seconds=40)

add(SRFP, "Double fertilisation", "Basic", "direct",
    "Inside the embryo sac, one male gamete moves towards the egg cell and fuses with its nucleus to form a diploid "
    "zygote. This fusion is called:",
    P("Syngamy", ["Triple fusion", "Apomixis", "Emasculation"], "B"),
    "Syngamy",
    "One male gamete fuses with the nucleus of the egg cell, completing syngamy and giving the diploid zygote. The "
    "other male gamete fuses with the two polar nuclei (triple fusion). Because both syngamy and triple fusion "
    "occur in one embryo sac, the phenomenon is called double fertilisation, an event unique to flowering plants.",
    ["Male gamete + egg → zygote: syngamy"],
    C12_SR("double fertilisation"),
    why="Triple fusion involves the two polar nuclei; apomixis is seed formation without fertilisation; "
        "emasculation is removal of anthers in artificial hybridisation.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "In a young anther, what occupies the centre of each microsporangium?",
    P("A group of compactly arranged homogeneous cells called the sporogenous tissue",
      ["The tapetum, a layer of cells with dense cytoplasm", "The endothecium",
       "A single large microspore tetrad"], "D"),
    "Structure of a young microsporangium",
    "When the young anther is cut transversely, a group of compactly arranged homogeneous cells, the sporogenous "
    "tissue, occupies the centre of each microsporangium. It is surrounded by the wall layers: epidermis, "
    "endothecium, middle layers and, innermost, the tapetum. Each sporogenous cell is a potential pollen mother "
    "cell.",
    ["Centre of a young microsporangium = sporogenous tissue"],
    C12_SR("the stamen, microsporangium and pollen grain"),
    why="The tapetum and endothecium are wall layers, not the centre; tetrads form later, after meiosis of the "
        "sporogenous cells.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "direct",
    "Which of the following is a post-fertilisation event in a flowering plant?",
    P("Maturation of the ovule into a seed and of the ovary into a fruit",
      ["Formation of microspores from a pollen mother cell",
       "Formation of megaspores from the megaspore mother cell",
       "Transfer of pollen grains from the anther to the stigma"], "A"),
    "Pre- and post-fertilisation events",
    "Following double fertilisation, the development of endosperm and embryo, maturation of the ovule(s) into "
    "seed(s) and of the ovary into a fruit are collectively termed post-fertilisation events. Microsporogenesis, "
    "megasporogenesis and pollination all take place before fertilisation.",
    ["Post-fertilisation: endosperm, embryo, seed, fruit"],
    C12_SR("post-fertilisation: structures and events"),
    why="The other three options (microsporogenesis, megasporogenesis and pollination) are pre-fertilisation "
        "events.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "According to NCERT, the period for which pollen grains remain viable is highly variable and, to some extent, "
    "depends on:",
    P("The prevailing temperature and humidity", ["The number of germ pores only", "The colour of the petals",
                                                 "The number of ovules in the ovary"], "C"),
    "Pollen viability",
    "NCERT: the period for which pollen grains remain viable is highly variable and to some extent depends on the "
    "prevailing temperature and humidity. In rice and wheat it is about 30 minutes; in some members of Rosaceae, "
    "Leguminosae and Solanaceae it is months.",
    ["Viability depends partly on temperature and humidity"],
    C12_SR("the stamen, microsporangium and pollen grain"),
    why="Germ pore number, petal colour and ovule number are not given by NCERT as factors in pollen viability.",
    seconds=20)

add(SRFP, "Endosperm and embryo", "Basic", "direct",
    "The cells of the endosperm are filled with reserve food materials. These reserves are used for:",
    P("The nutrition of the developing embryo",
      ["Attracting pollinators to the flower", "Forming the seed coat", "Producing the male gametes"], "D"),
    "Function of the endosperm",
    "The primary endosperm cell divides repeatedly to form the triploid endosperm. The endosperm cells are filled "
    "with reserve food materials and are used for the nutrition of the developing embryo.",
    ["Endosperm = food for the developing embryo"],
    C12_SR("post-fertilisation: endosperm"),
    why="The seed coat comes from the integuments, male gametes from the generative cell of the pollen, and the "
        "endosperm lies inside the seed, so it plays no part in attracting pollinators.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "statement_pair",
    sp("Pollen grains represent the female gametophytes of flowering plants.",
       "The outer three wall layers of a microsporangium perform the function of protection and help in the "
       "dehiscence of the anther to release the pollen."),
    SP("D"),
    "Microsporangium wall and pollen grain",
    "Pollen grains represent the male gametophytes; the embryo sac is the female gametophyte. So Statement I is "
    "false. Of the four wall layers of a microsporangium, the outer three (epidermis, endothecium and middle layers) "
    "protect it and help in dehiscence, while the innermost tapetum nourishes the developing pollen. Statement II "
    "is true.",
    ["Statement I: false, pollen = male gametophyte", "Statement II: true"],
    C12_SR("the stamen, microsporangium and pollen grain"),
    seconds=30)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "assertion_reason",
    ar("Pollen grains are well preserved as fossils.",
       "The exine of pollen grains is made of sporopollenin, one of the most resistant organic materials known."),
    AR("A"),
    "Sporopollenin and fossil pollen",
    "Sporopollenin withstands high temperatures and strong acids and alkalis, and no enzyme that degrades it is "
    "known. NCERT states that pollen grains are well preserved as fossils because of the presence of sporopollenin. "
    "R therefore explains A.",
    ["A: true", "R: true", "Resistant sporopollenin → preserved fossils"],
    C12_SR("the stamen, microsporangium and pollen grain"),
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "match_list",
    ml(("plant", "feature of its fruit or seed"),
       ["Orange", "Groundnut", "Cashew", "Wheat"],
       ["Dry fruit", "Seed that retains a part of the endosperm (albuminous seed)",
        "Fleshy fruit", "False fruit: the thalamus also contributes to fruit formation"]),
    M({"A": "III", "B": "I", "C": "IV", "D": "II"},
      [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
       {"A": "IV", "B": "I", "C": "III", "D": "II"}], "B"),
    "Fruits and seeds",
    "Fruits may be fleshy (guava, orange, mango) or dry (groundnut, mustard). In apple, strawberry and cashew the "
    "thalamus also contributes to fruit formation; such fruits are false fruits. Albuminous seeds such as wheat, "
    "maize, barley and castor retain a part of the endosperm.",
    ["A-III", "B-I", "C-IV", "D-II"],
    C12_SR("post-fertilisation: seed; fruit"),
    why="Option A swaps orange and groundnut; option C swaps cashew and wheat; option D calls orange a false fruit "
        "and cashew a simple fleshy fruit.",
    seconds=40)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "direct",
    "In a mature two-celled pollen grain, the generative cell is:",
    P("Small, spindle-shaped, with dense cytoplasm and a nucleus, and floats in the cytoplasm of the vegetative cell",
      ["Large, with abundant food reserve and a large irregularly shaped nucleus",
       "Attached to the intine and divides to form the tube nucleus",
       "Bigger than the vegetative cell and surrounded by its own exine"], "D"),
    "Vegetative and generative cells",
    "The vegetative cell is bigger, has abundant food reserve and a large irregularly shaped nucleus. The generative "
    "cell is small and floats in the cytoplasm of the vegetative cell; it is spindle-shaped with dense cytoplasm "
    "and a nucleus. It later divides to give the two male gametes.",
    ["Generative cell: small, spindle-shaped, floats in vegetative cell"],
    C12_SR("the stamen, microsporangium and pollen grain: pollen grain"),
    why="Option A describes the vegetative cell. The generative cell forms the two male gametes, not a tube "
        "nucleus, and it has no exine of its own; it is the smaller of the two cells.",
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "statement_pair",
    sp("All the events from pollen deposition on the stigma until the pollen tubes enter the ovule are together "
       "referred to as pollen-pistil interaction.",
       "In artificial hybridisation, emasculation is the removal of the anthers from a bisexual flower after the "
       "anthers have dehisced."),
    SP("C"),
    "Pollen-pistil interaction and emasculation",
    "NCERT defines pollen-pistil interaction as all the events from pollen deposition on the stigma until pollen "
    "tubes enter the ovule; Statement I is true. Emasculation is the removal of anthers from the flower bud before "
    "the anthers dehisce, using a pair of forceps. Removing them after dehiscence would allow self-pollination, so "
    "Statement II is false.",
    ["Statement I: true", "Statement II: false, anthers are removed before dehiscence"],
    C12_SR("pollination: pollen-pistil interaction; artificial hybridisation"),
    seconds=35)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("Pollen grains of many species cause severe allergies and bronchial afflictions in some people, often leading "
       "to chronic respiratory disorders such as asthma and bronchitis.",
       "Pollen grains are rich in nutrients."),
    AR("B"),
    "Pollen allergy and pollen as food",
    "Both statements are NCERT facts. Pollen allergy is a reaction of some people's airways to pollen of certain "
    "species (for example Parthenium). The nutrient content of pollen is why pollen tablets are used as food "
    "supplements. Nutrient richness does not explain why pollen causes allergy, so R is not the explanation of A.",
    ["A: true", "R: true", "R explains pollen as a food supplement, not allergy"],
    C12_SR("the stamen, microsporangium and pollen grain"),
    seconds=35)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "In the embryo of a monocotyledon such as a grass, the portion of the embryonal axis above the level of "
    "attachment of the scutellum is the:",
    P("Epicotyl", ["Hypocotyl", "Coleorhiza", "Radicle"], "B"),
    "Monocot embryo",
    "Monocot embryos have one cotyledon, the scutellum, on one side of the embryonal axis. The radicle and root cap "
    "at the lower end are enclosed in the coleorhiza. The portion of the axis above the level of attachment of the "
    "scutellum is the epicotyl, which has the shoot apex and a few leaf primordia enclosed in the coleoptile.",
    ["Above scutellum attachment → epicotyl"],
    C12_SR("post-fertilisation: embryo"),
    why="The hypocotyl is below the cotyledon level, the radicle is the root tip and the coleorhiza is the sheath "
        "around the radicle and root cap.",
    seconds=25)

add(SRFP, "Pollination", "Intermediate", "multi_statement",
    ms("Plants such as Viola (common pansy), Oxalis and Commelina produce two types of flowers. Which of the following "
       "statements about these flowers are correct?",
       ["Chasmogamous flowers are similar to the flowers of other species, with exposed anthers and stigma.",
        "Cleistogamous flowers do not open at all.",
        "In cleistogamous flowers, the anthers and the stigma lie close to each other.",
        "Cleistogamous flowers promote cross-pollination.",
        "Cleistogamous flowers depend on pollinators to bring pollen from other plants."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Chasmogamous and cleistogamous flowers",
    "Chasmogamous flowers have exposed anthers and stigma like other flowers. Cleistogamous flowers do not open at "
    "all; their anthers and stigma lie close together, and when the anthers dehisce in the bud the pollen reaches "
    "the stigma. They are autogamous and produce assured seed set even without pollinators, so they do not promote "
    "cross-pollination.",
    ["(a), (b), (c): true", "(d), (e): false, cleistogamous flowers are self-pollinated"],
    C12_SR("pollination: kinds of pollination"),
    why="Options A, B and D include (d) or (e).",
    seconds=40)

add(SRFP, "Double fertilisation", "Advanced", "direct",
    "A homozygous plant AA (female parent) is pollinated with pollen from a homozygous plant aa. Assuming normal "
    "double fertilisation, what are the genotypes of the seed coat, the embryo and the endosperm of the resulting "
    "seeds, respectively?",
    P("AA, Aa and AAa", ["Aa, Aa and Aaa", "AA, Aa and Aaa", "Aa, AA and AAa"], "D"),
    "Origin of seed tissues",
    "The seed coat develops from the integuments of the ovule, which are tissues of the mother plant: AA. The "
    "zygote is egg (A) + male gamete (a): Aa. The primary endosperm nucleus is two polar nuclei (both A, from the "
    "same megaspore as the egg) + one male gamete (a): AAa.",
    ["Seed coat = maternal integuments → AA", "Embryo = A + a → Aa", "Endosperm = A + A + a → AAa"],
    C12_SR("double fertilisation; post-fertilisation: seed"),
    why="Option A treats the seed coat as hybrid tissue and the endosperm as two paternal sets; option B gives the "
        "endosperm two paternal sets; option C swaps the seed coat and embryo genotypes.",
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Endosperm and embryo", "Advanced", "direct",
    "In seeds of black pepper and beet, a persistent remnant of the nucellus, the perisperm, is present. Which "
    "pair of structures has the same ploidy?",
    P("Perisperm and pericarp", ["Perisperm and endosperm", "Endosperm and zygote",
                                 "Pericarp and the egg cell"], "B"),
    "Ploidy of seed and fruit tissues",
    "The nucellus is diploid tissue of the parent sporophyte, so the perisperm is 2n. The pericarp develops from "
    "the ovary wall, also 2n tissue of the mother plant. The endosperm is triploid (3n), the zygote is diploid (2n) "
    "and the egg cell is haploid (n).",
    ["Perisperm (nucellus) = 2n", "Pericarp (ovary wall) = 2n", "Endosperm 3n; zygote 2n; egg n"],
    C12_SR("post-fertilisation: seed; fruit"),
    why="Perisperm (2n) differs from endosperm (3n); endosperm (3n) differs from the zygote (2n); the pericarp (2n) "
        "differs from the haploid egg.",
    seconds=50)

add(SRFP, "Double fertilisation", "Advanced", "numerical",
    "A fruit contains 40 seeds. Each seed has developed from a separate ovule by normal double fertilisation, with "
    "one pollen tube entering each ovule. How many male gametes take part, and how many nuclei (male and female "
    "together) fuse in all?",
    P("80 male gametes; 200 nuclei", ["40 male gametes; 120 nuclei", "80 male gametes; 160 nuclei",
                                      "40 male gametes; 200 nuclei"], "C"),
    "Counting nuclei in double fertilisation",
    "In each embryo sac, one pollen tube releases two male gametes. Syngamy fuses one male gamete with the egg "
    "nucleus (2 nuclei); triple fusion fuses the other male gamete with the two polar nuclei (3 nuclei). So each "
    "ovule uses 2 male gametes and 5 nuclei fuse. For 40 seeds: 2 × 40 = 80 male gametes and 5 × 40 = 200 nuclei.",
    ["Per ovule: 2 male gametes", "Per ovule: 2 (syngamy) + 3 (triple fusion) = 5 nuclei",
     "× 40 → 80 male gametes; 200 nuclei"],
    C12_SR("double fertilisation"),
    shortcut="Double fertilisation = 2 male gametes and 5 fusing nuclei per seed.",
    why="Option A counts one male gamete and only the three nuclei of triple fusion per seed; option B "
        "counts only one polar nucleus in triple fusion (4 per seed); option D counts one male gamete per seed.",
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Endosperm and embryo", "Advanced", "multi_statement",
    ms("Which of the following statements about seeds and fruits are correct?",
       ["A seed is often described as a fertilised ovule, and seeds are formed inside fruits.",
        "A seed typically consists of seed coat(s), cotyledon(s) and an embryo axis.",
        "The cotyledons are generally thick and swollen due to the storage of food reserves, as in legumes.",
        "In most plants, the other floral parts persist and enlarge along with the ovary as the fruit develops.",
        "The seed is the final product of asexual reproduction in angiosperms."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
    "The seed and the fruit",
    "NCERT: the seed is the final product of sexual reproduction in angiosperms and is often described as a "
    "fertilised ovule; seeds form inside fruits. A seed has seed coat(s), cotyledon(s) and an embryo axis, and the "
    "cotyledons are generally thick and swollen with food reserves (legumes). In most plants, by the time the fruit "
    "develops from the ovary, the other floral parts degenerate and fall off.",
    ["(a), (b), (c): true", "(d): false, other floral parts degenerate and fall off",
     "(e): false, seeds result from sexual reproduction"],
    C12_SR("post-fertilisation: seed; fruit"),
    why="Options A, B and C include (d) or (e).",
    seconds=45)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "statement_pair",
    sp("In artificial hybridisation, emasculated flowers are covered with a bag of suitable size, generally made up "
       "of butter paper, to prevent contamination of the stigma with unwanted pollen.",
       "When the stigma of the bagged flower attains receptivity, mature pollen grains collected from the anthers of "
       "the male parent are dusted on it, and the flowers are rebagged and the fruits allowed to develop."),
    SP("A"),
    "Artificial hybridisation: bagging and rebagging",
    "Both statements follow NCERT's account of artificial hybridisation: after emasculation, the flowers are covered "
    "with a bag, generally of butter paper (bagging). When the stigma becomes receptive, pollen from the desired "
    "male parent is dusted on it, and the flowers are rebagged so that fruits develop only from the intended cross.",
    ["Statement I: true", "Statement II: true"],
    C12_SR("pollination: artificial hybridisation"),
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "direct",
    "A plant species with bisexual flowers is self-incompatible. Which kind of pollination can lead to seed set by "
    "fertilisation in this species?",
    P("Xenogamy only", ["Autogamy only", "Geitonogamy only", "Both autogamy and geitonogamy, but not xenogamy"], "A"),
    "Self-incompatibility as an outbreeding device",
    "Self-incompatibility is a genetic mechanism that prevents self-pollen, from the same flower or from other "
    "flowers of the same plant, from fertilising the ovules, by inhibiting pollen germination or pollen tube growth "
    "in the pistil. Autogamy (same flower) and geitonogamy (another flower of the same plant) both bring self-pollen. "
    "Only xenogamy, which brings pollen from a different plant, can lead to fertilisation.",
    ["Self-pollen = same flower + other flowers of same plant", "Both blocked → only xenogamy works"],
    C12_SR("outbreeding devices"),
    why="Autogamy and geitonogamy both deliver self-pollen, which self-incompatibility rejects; geitonogamy is "
        "genetically similar to autogamy.",
    seconds=45)


# ================================================================ Principles of Inheritance and Variation (7 / 9 / 7)
C12_PI = lambda s: ref(12, PIV, s)


def gametes(genotype):
    """All gametes (equally likely) of a genotype written as gene pairs, e.g. 'AaBb' -> AB, Ab, aB, ab."""
    pairs = [genotype[i:i + 2] for i in range(0, len(genotype), 2)]
    return ["".join(g) for g in product(*pairs)]


def offspring(p1, p2):
    return [tuple("".join(sorted(x + y)) for x, y in zip(g1, g2)) for g1 in gametes(p1) for g2 in gametes(p2)]


# trihybrid F2 (AaBbCc selfed, complete dominance): phenotype and genotype classes
tri = offspring("AaBbCc", "AaBbCc")
assert len(tri) == 64
tri_genotypes = set(tri)
tri_phenotypes = {tuple(p[0].isupper() for p in o) for o in tri}
assert (len(tri_phenotypes), len(tri_genotypes)) == (8, 27)
assert 2 * 3 == 6 and 3 ** 3 == 27 and 4 ** 3 == 64     # distractors: 6 (2 x 3), 64 (gamete combinations)

# polygenic: number of dominant (pigment) alleles in AaBbCc x AaBbCc offspring
poly_classes = Counter(sum(ch.isupper() for p in o for ch in p) for o in tri)
assert sorted(poly_classes) == list(range(7)) and len(poly_classes) == 7
assert poly_classes[3] == 20 and poly_classes[0] == 1

# among round-yellow F2 seeds of RrYy x RrYy, fraction that is RRYY
f2 = offspring("RrYy", "RrYy")
round_yellow = [o for o in f2 if o[0][0] == "R" and o[1][0] == "Y"]
assert F(len(round_yellow), 16) == F(9, 16)
assert F(sum(o == ("RR", "YY") for o in round_yellow), len(round_yellow)) == F(1, 9)
assert F(sum(o == ("RR", "YY") for o in f2), 16) == F(1, 16)          # distractor 1/16: fraction of all F2
assert F(sum(o == ("Rr", "Yy") for o in round_yellow), len(round_yellow)) == F(4, 9)   # distractor 4/9 (RrYy)


def abo(p1, p2):
    """Blood groups of the children of two ABO genotypes, as a Counter over 4 equally likely zygotes."""
    group = {"AA": "A", "Ai": "A", "BB": "B", "Bi": "B", "AB": "AB", "ii": "O"}
    kids = Counter()
    for x in p1:
        for y in p2:
            kids[group["".join(sorted(x + y, key="ABi".index))]] += 1
    return kids


assert set(abo("AA", "ii")) == {"A"}
assert set(abo("AB", "ii")) == {"A", "B"}
assert set(abo("Ai", "ii")) == {"A", "O"}
assert set(abo("AA", "BB")) == {"AB"}
assert abo("AB", "AB") == Counter({"A": 1, "AB": 2, "B": 1})

# haemophilia (X-linked recessive, h): carrier mother XHXh x normal father XHY
kids = [(m, f) for m in ("XH", "Xh") for f in ("XH", "Y")]
sons = [k for k in kids if k[1] == "Y"]
daughters = [k for k in kids if k[1] != "Y"]
assert F(sum(k[0] == "Xh" for k in sons), len(sons)) == F(1, 2)                  # half the sons affected
assert F(sum(k[0] == "Xh" and k[1] == "Y" for k in kids), len(kids)) == F(1, 4)  # 1/4 of all children
assert not any(k[0] == "Xh" and k[1] == "Xh" for k in daughters)                 # no affected daughter
assert F(sum("Xh" in k for k in daughters), len(daughters)) == F(1, 2)           # half the daughters carriers
# haemophilic father XhY x normal (non-carrier) mother XHXH
kids2 = [(m, f) for m in ("XH", "XH") for f in ("Xh", "Y")]
assert all(k[0] == "XH" for k in kids2 if k[1] == "Y")                            # all sons normal
assert all(k[1] == "Xh" for k in kids2 if k[1] != "Y")                            # all daughters carriers

add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("character studied by Mendel in pea", "recessive trait"),
       ["Flower colour", "Seed shape", "Stem height", "Flower position"],
       ["Terminal", "Dwarf", "White", "Wrinkled"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
       {"A": "II", "B": "IV", "C": "III", "D": "I"}], "B"),
    "Contrasting traits in Mendel's pea",
    "Mendel studied seven pairs of contrasting traits. For these four characters the dominant and recessive traits "
    "are: flower colour violet/white, seed shape round/wrinkled, stem height tall/dwarf, flower position "
    "axial/terminal. The recessive forms are white, wrinkled, dwarf and terminal.",
    ["A-III (white)", "B-IV (wrinkled)", "C-II (dwarf)", "D-I (terminal)"],
    C12_PI("Mendel's laws of inheritance"),
    why="Option A swaps flower colour and seed shape; option C swaps stem height and flower position; option D "
        "swaps flower colour and stem height.",
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "Which of the following is a Mendelian disorder, i.e. one determined by alteration or mutation in a single gene?",
    P("Cystic fibrosis", ["Down's syndrome", "Klinefelter's syndrome", "Turner's syndrome"], "D"),
    "Mendelian versus chromosomal disorders",
    "NCERT lists the most common Mendelian disorders as haemophilia, cystic fibrosis, sickle-cell anaemia, colour "
    "blindness, phenylketonuria and thalassemia. Down's, Klinefelter's and Turner's syndromes are chromosomal "
    "disorders caused by an extra or missing chromosome.",
    ["Single-gene disorder → cystic fibrosis"],
    C12_PI("genetic disorders: Mendelian disorders"),
    why="The other three are chromosomal disorders (trisomy 21, 47 XXY and 45 X0).",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "In genetics, 'variation' is best defined as:",
    P("The degree by which progeny differ from their parents",
      ["The process by which characters are passed on from parent to progeny",
       "The complete expression of a dominant allele in the heterozygote",
       "The physical association of two genes on a chromosome"], "A"),
    "Inheritance and variation",
    "Genetics deals with inheritance as well as variation of characters. Inheritance is the process by which "
    "characters are passed on from parent to progeny; it is the basis of heredity. Variation is the degree by which "
    "progeny differ from their parents.",
    ["Variation = degree of difference between progeny and parents"],
    C12_PI("introduction"),
    why="Option B defines inheritance, option C describes dominance and option D describes linkage.",
    seconds=20)

add(PIV, "Sex determination", "Basic", "direct",
    "In the haplodiploid sex-determination system of honey bees, the male (drone) produces sperms by:",
    P("Mitosis, because the male is haploid",
      ["Meiosis, which halves its 32 chromosomes to 16", "Meiosis, because the male is diploid",
       "Parthenogenesis from unfertilised eggs"], "C"),
    "Haplodiploidy in honey bees",
    "In honey bees, a fertilised egg develops into a female (queen or worker) with 32 chromosomes, and an "
    "unfertilised egg develops into a haploid male (drone) with 16 chromosomes by parthenogenesis. NCERT notes as a "
    "special feature that the males produce sperms by mitosis.",
    ["Drone = haploid (16)", "Haploid cell cannot undergo normal meiosis → sperms by mitosis"],
    C12_PI("sex determination: sex determination in honey bee"),
    why="The male has only 16 chromosomes and is haploid, so it does not halve 32 chromosomes by meiosis. "
        "Parthenogenesis is how the male itself develops, not how it makes sperms.",
    seconds=25)

add(PIV, "Sex-linked inheritance", "Basic", "direct",
    "In haemophilia, why does a simple cut in an affected individual result in non-stop bleeding?",
    P("A single protein that is part of the cascade of proteins involved in blood clotting is affected",
      ["The red blood cells become sickle-shaped under low oxygen tension",
       "Too few globin molecules are synthesised", "The enzyme phenylalanine hydroxylase is absent"], "B"),
    "Haemophilia",
    "Haemophilia is a sex-linked recessive disease. In it, a single protein that is a part of the cascade of "
    "proteins involved in the clotting of blood is affected, so a simple cut results in non-stop bleeding.",
    ["Haemophilia → defect in one clotting-cascade protein"],
    C12_PI("genetic disorders: haemophilia"),
    why="Option A describes sickle-cell anaemia, option C thalassemia and option D phenylketonuria.",
    seconds=25)

add(PIV, "Polygenic inheritance", "Basic", "direct",
    "In a polygenic trait, the phenotype reflects the contribution of each allele. The effect of each allele is "
    "therefore described as:",
    P("Additive", ["Epistatic and masked by one dominant allele", "Lethal", "Expressed only in males"], "D"),
    "Polygenic inheritance",
    "Polygenic traits are controlled by three or more genes. NCERT notes that in a polygenic trait the phenotype "
    "reflects the contribution of each allele, i.e. the effect of each allele is additive, which is why skin colour "
    "shows a gradation of shades.",
    ["Each allele adds its share → additive effect"],
    C12_PI("polygenic inheritance"),
    why="Polygenic alleles are not masked by a single dominant allele, are not lethal and are not sex-limited.",
    seconds=20)

add(PIV, "Sex determination", "Basic", "direct",
    "In humans, the male is heterogametic. In what proportion does he produce sperms carrying the X and the Y "
    "chromosome?",
    P("50 per cent X-bearing and 50 per cent Y-bearing", ["All X-bearing", "All Y-bearing",
                                                          "75 per cent X-bearing and 25 per cent Y-bearing"], "C"),
    "Sex determination in humans",
    "Human males have XY sex chromosomes and produce two types of gametes: 50 per cent of the sperms carry the X "
    "chromosome and 50 per cent carry the Y. Females (XX) produce only X-bearing ova, so the sex of the child is "
    "decided by the type of sperm that fertilises the ovum.",
    ["XY male → X and Y sperms in 1 : 1"],
    C12_PI("sex determination: sex determination in humans"),
    why="An XY cell gives X and Y to its products equally at meiosis, so neither all-X, all-Y nor 3 : 1 is "
        "possible.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "A plant heterozygous for three independently assorting genes (AaBbCc), each with complete dominance, is "
    "self-pollinated. How many different phenotypes and how many different genotypes are expected in the progeny?",
    P("8 phenotypes and 27 genotypes", ["6 phenotypes and 27 genotypes", "8 phenotypes and 64 genotypes",
                                        "27 phenotypes and 8 genotypes"], "A"),
    "Phenotype and genotype classes in a trihybrid cross",
    "For each gene, Aa × Aa gives 2 phenotypes (dominant, recessive) and 3 genotypes (AA, Aa, aa). With independent "
    "assortment the classes multiply: phenotypes 2³ = 8, genotypes 3³ = 27.",
    ["Per gene: 2 phenotypes, 3 genotypes", "Phenotypes = 2³ = 8", "Genotypes = 3³ = 27"],
    C12_PI("inheritance of two genes; law of independent assortment"),
    shortcut="n heterozygous genes selfed: 2ⁿ phenotypes, 3ⁿ genotypes, 4ⁿ gamete combinations.",
    why="Option B multiplies 2 × 3 instead of raising to the power of three; option C gives 4³ = 64, the number of "
        "gamete combinations (boxes in the Punnett square), not distinct genotypes; option D swaps the two numbers.",
    seconds=50, verified_by=RECOMPUTED)

add(PIV, "Mendelian inheritance", "Intermediate", "statement_pair",
    sp("One reason Mendel's work remained unrecognised was that he could not provide any physical proof for the "
       "existence of factors or say what they were made of.",
       "By 1900, advances in microscopy allowed scientists to observe cell division carefully, which led to the "
       "discovery of nuclear structures that appeared to double and divide just before each cell division."),
    SP("A"),
    "Rediscovery of Mendel and the chromosomal theory",
    "NCERT gives several reasons why Mendel's work stayed unrecognised; one is that he could not provide any "
    "physical proof for the existence of factors or say what they were made of. By 1900 advances in microscopy "
    "allowed careful observation of cell division and led to the discovery of structures in the nucleus that doubled "
    "and divided before each division: the chromosomes ('coloured bodies', as they were seen after staining). Both "
    "statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_PI("chromosomal theory of inheritance"),
    seconds=35)

add(PIV, "Incomplete and co-dominance", "Intermediate", "assertion_reason",
    ar("Dominance is not an autonomous feature of a gene or of the product that it has information for.",
       "Dominance depends on the gene product and the production of a particular phenotype from it, as well as on the "
       "particular phenotype that we choose to examine when more than one phenotype is influenced by the same gene."),
    AR("A"),
    "Concept of dominance",
    "NCERT: dominance is not an autonomous feature of a gene or its product. It depends as much on the gene product "
    "and the production of a particular phenotype from this product as on the phenotype we choose to examine (as in "
    "the pea gene for starch synthesis, which is dominant for seed shape but incompletely dominant for starch grain "
    "size). R explains why A is true.",
    ["A: true", "R: true", "Dominance depends on the product and the phenotype examined → not autonomous"],
    C12_PI("inheritance of one gene: concept of dominance"),
    seconds=45)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "match_list",
    ml(("cross between parents of given ABO genotypes", "blood groups possible among the children"),
       ["IᴬIᴬ × ii", "IᴬIᴮ × ii", "Iᴬi × ii", "IᴬIᴬ × IᴮIᴮ"],
       ["Blood groups A and O only", "Blood group AB only", "Blood group A only", "Blood groups A and B only"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
       {"A": "III", "B": "I", "C": "IV", "D": "II"}], "C"),
    "Multiple alleles and co-dominance in the ABO system",
    "The gene I has three alleles, Iᴬ, Iᴮ and i; Iᴬ and Iᴮ are co-dominant and both are dominant over i. "
    "IᴬIᴬ × ii gives only Iᴬi (A). IᴬIᴮ × ii gives Iᴬi (A) and Iᴮi (B). Iᴬi × ii gives Iᴬi (A) and ii (O). "
    "IᴬIᴬ × IᴮIᴮ gives only IᴬIᴮ (AB).",
    ["A: Iᴬi only → III", "B: Iᴬi, Iᴮi → IV", "C: Iᴬi, ii → I", "D: IᴬIᴮ only → II"],
    C12_PI("inheritance of one gene: co-dominance (ABO blood groups)"),
    why="Option A swaps the crosses IᴬIᴬ × ii and Iᴬi × ii; option B treats IᴬIᴮ × ii as giving AB children; "
        "option D gives the IᴬIᴮ × ii parents children of groups A and O.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Linkage and crossing over", "Intermediate", "multi_statement",
    ms("Which of the following statements about the chromosomal theory of inheritance and Morgan's work are correct?",
       ["Sutton and Boveri argued that the pairing and separation of a pair of chromosomes would lead to the "
        "segregation of the pair of factors they carried.",
        "Morgan crossed yellow-bodied, white-eyed female Drosophila with brown-bodied, red-eyed males and "
        "intercrossed their F1 progeny.",
        "Genes that are very tightly linked show a high frequency of recombination.",
        "Genes that are loosely linked show a higher recombination than tightly linked genes.",
        "Chromosomes and genes both segregate at gamete formation such that only one of each pair is transmitted "
        "to a gamete."]),
    MS(["a", "b", "d", "e"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "c", "e"]], "B"),
    "Chromosomal theory and linkage",
    "Sutton and Boveri linked the pairing and separation of chromosomes to the segregation of Mendel's factors; "
    "genes and chromosomes both occur in pairs and both segregate so that only one of each pair goes to a gamete. "
    "Morgan crossed yellow-bodied, white-eyed females with brown-bodied, red-eyed males and intercrossed the F1. He "
    "found that some genes were very tightly linked (very low recombination) while others were loosely linked "
    "(higher recombination).",
    ["(a), (b), (d), (e): true", "(c): false, tight linkage means low recombination"],
    C12_PI("chromosomal theory of inheritance; linkage and recombination"),
    why="Every other option contains (c), which reverses the relation between linkage and recombination.",
    seconds=50)

add(PIV, "Sex-linked inheritance", "Intermediate", "multi_statement",
    ms("A haemophilic man marries a woman who is neither haemophilic nor a carrier. Which of the following "
       "statements about their children are correct?",
       ["All their sons will be normal.",
        "All their daughters will be carriers.",
        "Half of their sons will be haemophilic.",
        "Half of their daughters will be haemophilic.",
        "A son can inherit the defective allele from his father."]),
    MS(["a", "b"], [["a", "b", "e"], ["b", "c"], ["c", "d", "e"]], "D"),
    "Inheritance of haemophilia",
    "Haemophilia is X-linked recessive. The father is XʰY and the mother XᴴXᴴ. Sons receive the Y from the father "
    "and an Xᴴ from the mother, so all sons are normal. Daughters receive Xʰ from the father and Xᴴ from the mother, "
    "so all daughters are unaffected carriers. A father never passes his X chromosome to a son.",
    ["Sons: Xᴴ (mother) + Y (father) → all normal", "Daughters: Xᴴ + Xʰ → all carriers"],
    C12_PI("genetic disorders: haemophilia"),
    why="Option A includes (e), but sons get the father's Y, not his X. Options B and C include (c) or (d), which "
        "would need a carrier mother.",
    seconds=50, verified_by=RECOMPUTED)

add(PIV, "Polygenic inheritance", "Intermediate", "numerical",
    "Suppose a polygenic trait is controlled by three genes A, B and C, and each dominant allele adds an equal "
    "amount to the phenotype (additive effect). In the progeny of AaBbCc × AaBbCc, how many distinct phenotypic "
    "classes are expected?",
    P("7", ["8", "27", "6"], "B"),
    "Number of phenotypic classes in polygenic inheritance",
    "With additive alleles, the phenotype depends only on the number of dominant alleles an individual carries. "
    "Offspring of AaBbCc × AaBbCc can carry 0, 1, 2, 3, 4, 5 or 6 dominant alleles, giving 7 distinct classes "
    "(from the lightest, aabbcc, to the darkest, AABBCC).",
    ["Possible dominant-allele counts: 0 to 6", "Number of classes = 6 + 1 = 7"],
    C12_PI("polygenic inheritance"),
    shortcut="n additive genes → 2n + 1 phenotypic classes.",
    why="8 is the number of phenotypes if each gene showed complete dominance; 27 is the number of genotypes; 6 leaves out "
        "the class with no dominant allele (aabbcc).",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "statement_pair",
    sp("Chromosomal disorders are caused by the absence or excess or abnormal arrangement of one or more chromosomes.",
       "Individuals with Klinefelter's syndrome are sterile females with rudimentary ovaries."),
    SP("C"),
    "Chromosomal disorders",
    "NCERT: chromosomal disorders are caused by absence or excess or abnormal arrangement of one or more "
    "chromosomes, so Statement I is true. Klinefelter's syndrome (47, XXY) individuals show overall masculine "
    "development with some feminine development (gynaecomastia) and are sterile males. Sterile females with "
    "rudimentary ovaries describe Turner's syndrome. Statement II is false.",
    ["Statement I: true", "Statement II: false, describes Turner's syndrome"],
    C12_PI("genetic disorders: chromosomal disorders"),
    seconds=35)

add(PIV, "Mendelian inheritance", "Intermediate", "assertion_reason",
    ar("In the F2 generation of Mendel's dihybrid cross between round yellow and wrinkled green pea plants, only the "
       "parental combinations of traits appeared.",
       "During gamete formation, the segregation of one pair of alleles is independent of the other pair."),
    AR("D"),
    "Recombinant phenotypes in a dihybrid cross",
    "R is the law of independent assortment and is true. Because the two pairs assort independently, the F2 showed "
    "the new combinations round green and wrinkled yellow as well as the parental types, in the ratio 9 : 3 : 3 : 1. "
    "A is false.",
    ["A: false, round green and wrinkled yellow also appeared", "R: true (independent assortment)"],
    C12_PI("inheritance of two genes"),
    seconds=35)

add(PIV, "Mendelian inheritance", "Advanced", "numerical",
    "In Mendel's dihybrid cross RRYY × rryy, the F1 plants (RrYy) are self-pollinated. If one F2 seed is picked at "
    "random from among the round yellow seeds only, what is the probability that it is true-breeding (RRYY)?",
    P("1/9", ["1/16", "4/9", "9/16"], "D"),
    "Conditional probability in the dihybrid F2",
    "Round yellow seeds make up 9 of the 16 F2 combinations: 1 RRYY, 2 RRYy, 2 RrYY and 4 RrYy. Only RRYY breeds "
    "true for both traits. Given that the seed is round yellow, the probability is 1/9.",
    ["Round yellow = 9/16 of F2", "RRYY = 1/16 of F2", "P(RRYY | round yellow) = (1/16)/(9/16) = 1/9"],
    C12_PI("inheritance of two genes"),
    shortcut="Within the 9 class: genotypes are 1 : 2 : 2 : 4 (RRYY : RRYy : RrYY : RrYy).",
    why="1/16 is the fraction of RRYY among all F2 seeds, ignoring the condition; 4/9 is the chance of RrYy; 9/16 is "
        "the fraction of round yellow seeds itself.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "multi_statement",
    ms("A woman who is a carrier for haemophilia marries a normal man. Which of the following statements about their "
       "children are correct?",
       ["Half of their sons are expected to be haemophilic.",
        "One-fourth of all their children are expected to be haemophilic sons.",
        "None of their daughters is expected to be haemophilic.",
        "Half of their daughters are expected to be carriers.",
        "Half of all their children are expected to be haemophilic."]),
    MS(["a", "b", "c", "d"], [["a", "c", "e"], ["b", "c", "d", "e"], ["a", "d", "e"]], "A"),
    "Probability in X-linked recessive inheritance",
    "Mother XᴴXʰ × father XᴴY gives four equally likely children: XᴴXᴴ (normal daughter), XᴴXʰ (carrier daughter), "
    "XᴴY (normal son) and XʰY (haemophilic son). So 1/2 of the sons and 1/4 of all children are haemophilic; no "
    "daughter is haemophilic (each gets the father's Xᴴ); 1/2 of the daughters are carriers.",
    ["Children: XᴴXᴴ, XᴴXʰ, XᴴY, XʰY", "Affected: XʰY only = 1/2 of sons = 1/4 of all",
     "Daughters: none affected, half carriers"],
    C12_PI("genetic disorders: haemophilia"),
    why="Options B, C and D include (e), which confuses 'half of the sons' with 'half of all the children'.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "assertion_reason",
    ar("A colour-blind man cannot pass the gene for colour blindness on to his son.",
       "A son receives his X chromosome from his mother and his Y chromosome from his father."),
    AR("A"),
    "No father-to-son transmission of X-linked genes",
    "The gene for red-green colour blindness is on the X chromosome. A son gets the Y chromosome from his father "
    "and the X from his mother, so a colour-blind father can never transmit the gene to his sons (he passes it to "
    "all his daughters). R correctly explains A.",
    ["A: true", "R: true", "Father's X goes only to daughters → R explains A"],
    C12_PI("sex-linked inheritance; genetic disorders: colour blindness"),
    seconds=40)

add(PIV, "Incomplete and co-dominance", "Advanced", "statement_pair",
    sp("In snapdragon, the F2 genotypic ratio for flower colour differs from that of a Mendelian monohybrid cross.",
       "A cross between a pink-flowered and a white-flowered snapdragon gives pink and white offspring in a 1 : 1 "
       "ratio, with no red-flowered offspring."),
    SP("D"),
    "Incomplete dominance in snapdragon",
    "In snapdragon (RR red, Rr pink, rr white), the F2 genotypes are 1 RR : 2 Rr : 1 rr, exactly as in a Mendelian "
    "monohybrid cross; only the phenotypic ratio changes from 3 : 1 to 1 : 2 : 1. So Statement I is false. "
    "Pink × white is Rr × rr, giving 1 Rr (pink) : 1 rr (white) and no RR (red), so Statement II is true.",
    ["Statement I: false, genotypic ratio is the usual 1 : 2 : 1", "Statement II: Rr × rr → 1 pink : 1 white; true"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    seconds=45)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "multi_statement",
    ms("Aneuploidy is the gain or loss of chromosome(s) due to failure of segregation of chromatids during cell "
       "division. Which of the following conditions result from aneuploidy?",
       ["Down's syndrome", "Klinefelter's syndrome", "Turner's syndrome", "Sickle-cell anaemia", "Haemophilia"]),
    MS(["a", "b", "c"], [["a", "c"], ["a", "b", "c", "d"], ["b", "d", "e"]], "C"),
    "Aneuploidy in chromosomal disorders",
    "Down's syndrome is trisomy of chromosome 21 (gain), Klinefelter's syndrome is 47, XXY (gain of an X) and "
    "Turner's syndrome is 45, X0 (loss of an X); all three are aneuploid chromosomal disorders. Sickle-cell anaemia "
    "and haemophilia are Mendelian disorders caused by alteration of a single gene; the chromosome number is normal.",
    ["Down 47 (+21), Klinefelter 47 (XXY), Turner 45 (X0): aneuploid", "Sickle-cell, haemophilia: single-gene"],
    C12_PI("genetic disorders: chromosomal disorders"),
    why="Option A leaves out Klinefelter's syndrome, a gain of a sex chromosome; options B and D include "
        "single-gene (Mendelian) disorders.",
    seconds=45)

add(PIV, "Linkage and crossing over", "Advanced", "direct",
    "Two genes are so tightly linked on one chromosome that no recombination occurs between them. A dihybrid that "
    "received AB from one parent and ab from the other is test-crossed with an ab/ab plant. The progeny are expected "
    "to be:",
    P("Only the two parental types, AaBb and aabb, in a 1 : 1 ratio",
      ["AaBb, Aabb, aaBb and aabb in a 1 : 1 : 1 : 1 ratio", "Only AaBb",
       "Mostly Aabb and aaBb, with few AaBb and aabb"], "B"),
    "Complete linkage in a test cross",
    "With no recombination, the dihybrid forms only the parental gametes AB and ab, in equal numbers. Crossed with "
    "ab gametes, these give AaBb and aabb in a 1 : 1 ratio. The 1 : 1 : 1 : 1 ratio is expected only for "
    "independently assorting genes, and recombinant types (Aabb, aaBb) need crossing over.",
    ["No crossing over → gametes AB and ab only", "Test cross → AaBb : aabb = 1 : 1"],
    C12_PI("linkage and recombination"),
    why="Option A is the result for independent assortment; option C ignores the ab gametes; option D makes the "
        "recombinants the majority, the reverse of linkage.",
    seconds=50)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "direct",
    "Both parents have blood group AB. Which of the following correctly describes their children?",
    P("Blood groups A, AB and B in the ratio 1 : 2 : 1; no child has blood group O",
      ["All children have blood group AB", "Blood groups A, B, AB and O in equal proportions",
       "Blood groups A and B in the ratio 1 : 1; no child has blood group AB"], "D"),
    "Co-dominance in a cross of two heterozygotes",
    "IᴬIᴮ × IᴮIᴬ gives IᴬIᴬ, IᴬIᴮ, IᴮIᴬ and IᴮIᴮ, i.e. 1 A : 2 AB : 1 B. Because Iᴬ and Iᴮ are co-dominant, the "
    "heterozygotes show group AB. Neither parent carries i, so no child can be group O. The phenotypic ratio equals "
    "the genotypic ratio, as in any co-dominant monohybrid cross.",
    ["Gametes: Iᴬ, Iᴮ from each parent", "IᴬIᴬ : IᴬIᴮ : IᴮIᴮ = 1 : 2 : 1 → A : AB : B", "No i allele → no O"],
    C12_PI("inheritance of one gene: co-dominance"),
    why="Option A treats AB parents as true-breeding; option B needs both parents to carry i; option C ignores the "
        "IᴬIᴮ children.",
    seconds=45, verified_by=RECOMPUTED)


# ================================================================ Molecular Basis of Inheritance (7 / 9 / 7)
C12_MB = lambda s: ref(12, MBI, s)

# mRNA from a coding strand: same sequence and polarity, U in place of T
coding = "ATGCCGTTAGCA"
pair = {"A": "U", "T": "A", "G": "C", "C": "G"}
mrna = coding.replace("T", "U")
assert mrna == "AUGCCGUUAGCA"
template_3to5 = "".join({"A": "T", "T": "A", "G": "C", "C": "G"}[b] for b in coding)       # read 3'->5'
assert "".join(pair[b] for b in template_3to5) == mrna       # RNA built on the template = coding strand with U
assert "".join(pair[b] for b in coding) == "UACGGCAAUCGU"    # distractor: complement of the coding strand
assert mrna[::-1] == "ACGAUUGCCGUA"                           # distractor: coding sequence reversed

# HGP cost: 3 x 10^9 bp at US $3 per bp
assert 3 * 10 ** 9 * 3 == 9 * 10 ** 9
assert 2 * 3 * 10 ** 9 * 3 == 18 * 10 ** 9                   # distractor: diploid 6.6 x 10^9 rounded to 6 x 10^9

# Meselson-Stahl: 15N DNA moved to 14N; E. coli divides every 20 minutes; after 80 minutes = 4 generations
molecules = ["HH"]
for _ in range(80 // 20):
    molecules = [s + "L" for m in molecules for s in m]       # each old strand pairs with a new light strand
hybrid = sum(m == "HL" for m in molecules)
light = sum(m == "LL" for m in molecules)
assert len(molecules) == 16 and F(hybrid, 16) == F(1, 8) and F(light, 16) == F(7, 8)
assert F(2, 2 ** 3) == F(1, 4) and F(2, 2 ** 2) == F(1, 2)    # distractors: 3 generations; 2 generations

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "A nucleotide is formed when a phosphate group is linked to the 5'-OH of a nucleoside. This linkage is a:",
    P("Phosphoester linkage", ["N-glycosidic linkage", "3'–5' phosphodiester linkage", "Hydrogen bond"], "B"),
    "Nucleoside and nucleotide",
    "A nitrogenous base linked to the pentose sugar through an N-glycosidic linkage forms a nucleoside. When a "
    "phosphate group is linked to the 5'-OH of a nucleoside through a phosphoester linkage, a nucleotide is formed. "
    "Two nucleotides are then joined to each other through a 3'–5' phosphodiester linkage.",
    ["Base + sugar: N-glycosidic", "Nucleoside + phosphate (5'-OH): phosphoester", "Nucleotide–nucleotide: phosphodiester"],
    C12_MB("structure of polynucleotide chain"),
    why="The N-glycosidic linkage joins base and sugar; the phosphodiester linkage joins two nucleotides; hydrogen "
        "bonds join bases of opposite strands.",
    seconds=25)

add(MBI, "DNA as genetic material", "Basic", "direct",
    "In which of the following does RNA act as the genetic material?",
    P("Tobacco mosaic virus and QB bacteriophage", ["Escherichia coli and Streptococcus pneumoniae",
                                                    "Bacteriophage lambda and bacteriophage φX174",
                                                    "Humans and Drosophila"], "D"),
    "RNA as genetic material",
    "DNA is the genetic material in most organisms. NCERT notes that in some viruses, such as tobacco mosaic viruses "
    "and QB bacteriophage, RNA is the genetic material.",
    ["RNA genomes: TMV, QB bacteriophage"],
    C12_MB("properties of genetic material (DNA versus RNA)"),
    why="Bacteria, humans and Drosophila have DNA genomes; NCERT gives the genome sizes of bacteriophages lambda "
        "and φX174 as DNA (base pairs and nucleotides of DNA).",
    seconds=20)

add(MBI, "DNA packaging", "Basic", "match_list",
    ml(("term", "description"),
       ["Cistron", "sRNA", "Nucleoside", "Heterochromatin"],
       ["A nitrogenous base linked to a pentose sugar", "Densely packed, dark-staining and transcriptionally inactive "
        "chromatin", "Segment of DNA coding for a polypeptide", "Earlier name of tRNA (soluble RNA)"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Terms in molecular biology",
    "A cistron is a segment of DNA coding for a polypeptide. tRNA was called sRNA (soluble RNA) before the genetic "
    "code was postulated. A nucleoside is a nitrogenous base linked to a pentose sugar (by an N-glycosidic "
    "linkage). Chromatin that is densely packed and stains dark is heterochromatin; it is transcriptionally inactive.",
    ["A-III", "B-IV", "C-I", "D-II"],
    C12_MB("packaging of DNA helix; transcription unit and the gene; tRNA"),
    why="Option B swaps cistron and sRNA; option C swaps nucleoside and heterochromatin; option D swaps cistron and "
        "nucleoside.",
    seconds=40)

add(MBI, "DNA as genetic material", "Basic", "direct",
    "In the Hershey–Chase experiment, bacteria were infected with bacteriophages grown on a medium containing "
    "radioactive sulphur and were then blended and centrifuged. The bacterial cells were found to be:",
    P("Not radioactive, showing that the viral protein did not enter the bacteria",
      ["Radioactive, showing that the viral protein entered the bacteria",
       "Radioactive, showing that the viral DNA contains sulphur",
       "Not radioactive, because the bacteria were killed before infection"], "C"),
    "Hershey–Chase experiment",
    "Viruses grown with radioactive sulphur had radioactive protein (proteins contain sulphur, DNA does not). "
    "Bacteria infected with these viruses were not radioactive after blending and centrifugation, indicating that "
    "proteins did not enter the bacteria. Bacteria infected with viruses carrying radioactive (phosphorus-labelled) "
    "DNA were radioactive. Hence DNA, not protein, passes from virus to bacterium.",
    ["³⁵S labels protein", "Bacteria not radioactive → protein did not enter"],
    C12_MB("the search for genetic material: Hershey–Chase experiment"),
    why="The labelled protein coats were removed by blending; DNA contains phosphorus, not sulphur; the bacteria "
        "were live hosts during infection.",
    seconds=30)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "Which of the following pairs of nitrogenous bases are both purines?",
    P("Adenine and guanine", ["Cytosine and thymine", "Cytosine and uracil", "Thymine and uracil"], "A"),
    "Purines and pyrimidines",
    "Nitrogenous bases are of two types: purines (adenine and guanine) and pyrimidines (cytosine, uracil and "
    "thymine). Cytosine is common to DNA and RNA; thymine is in DNA and uracil in RNA in place of thymine.",
    ["Purines: A, G", "Pyrimidines: C, T, U"],
    C12_MB("structure of polynucleotide chain"),
    why="Cytosine, thymine and uracil are all pyrimidines.",
    seconds=20)

add(MBI, "Lac operon", "Basic", "direct",
    "Besides the lac operon, which of the following bacterial operons are named in NCERT?",
    P("trp, ara, his and val operons", ["z, y and a operons", "σ and ρ operons", "VNTR and SNP operons"], "D"),
    "Operons",
    "In bacteria, a polycistronic structural gene regulated by a common promoter and regulatory genes is called an "
    "operon. NCERT names the lac operon, trp operon, ara operon, his operon and val operon as examples.",
    ["Operon examples: lac, trp, ara, his, val"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="z, y and a are structural genes within the lac operon; σ and ρ are transcription factors of bacterial RNA "
        "polymerase; VNTRs and SNPs are DNA sequence variations, not operons.",
    seconds=20)

add(MBI, "Lac operon", "Basic", "direct",
    "In prokaryotes, the predominant site for the control of gene expression is:",
    P("Control of the rate of transcriptional initiation", ["Regulation of splicing of hnRNA",
                                                            "Transport of mRNA from the nucleus to the cytoplasm",
                                                            "Capping and tailing of the primary transcript"], "B"),
    "Regulation of gene expression in prokaryotes",
    "NCERT: in prokaryotes, control of the rate of transcriptional initiation is the predominant site for control "
    "of gene expression. The activity of RNA polymerase at a promoter is regulated by accessory proteins, and "
    "repressors acting at the operator regulate access to the promoter.",
    ["Prokaryotes → transcriptional initiation"],
    C12_MB("regulation of gene expression"),
    why="Splicing, capping and tailing, and transport from a nucleus are features of eukaryotic gene expression; "
        "prokaryotes have no nucleus and their genes are not split.",
    seconds=25)

add(MBI, "Transcription", "Intermediate", "assertion_reason",
    ar("During transcription, only one strand of a DNA segment is copied into RNA.",
       "If both strands were copied, the two RNAs would have different sequences and could code for two different "
       "proteins, and, being complementary, they would form double-stranded RNA that could not be translated."),
    AR("A"),
    "Why only one DNA strand is transcribed",
    "NCERT gives two reasons why both strands are not copied. Two RNAs from the two strands would have different "
    "sequences, so one DNA segment would code for two different proteins and complicate information transfer. Also, "
    "the two RNAs would be complementary and would form double-stranded RNA, preventing translation and making "
    "transcription futile. R explains A.",
    ["A: true", "R: true", "R gives NCERT's reasons for A"],
    C12_MB("transcription"),
    seconds=40)

add(MBI, "Transcription", "Intermediate", "direct",
    "The coding strand of a short stretch of a structural gene reads 5'-ATGCCGTTAGCA-3'. The mRNA transcribed from "
    "this stretch will be:",
    P("5'-AUGCCGUUAGCA-3'", ["5'-UACGGCAAUCGU-3'", "5'-ACGAUUGCCGUA-3'", "5'-ATGCCGTTAGCA-3'"], "C"),
    "Template and coding strands",
    "The template strand (3'→5') is copied, so the RNA is complementary to the template and therefore has the same "
    "sequence and polarity as the coding strand, with uracil in place of thymine: 5'-AUGCCGUUAGCA-3'.",
    ["mRNA = coding strand with U for T", "Polarity unchanged: 5' → 3'"],
    C12_MB("transcription: transcription unit"),
    why="Option A is the complement of the coding strand (it would be built on the coding strand, which is not "
        "copied); option B reverses the sequence; option D keeps thymine, which RNA does not contain.",
    seconds=40, verified_by=RECOMPUTED)

add(MBI, "DNA as genetic material", "Intermediate", "multi_statement",
    ms("In Griffith's experiments with Streptococcus pneumoniae, which of the following observations were made?",
       ["Mice injected with live S strain bacteria died.",
        "Mice injected with live R strain bacteria lived.",
        "Mice injected with heat-killed S strain bacteria died.",
        "Mice injected with a mixture of heat-killed S strain and live R strain bacteria died.",
        "Living S strain bacteria were recovered from the mice that died after the mixed injection."]),
    MS(["a", "b", "d", "e"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "c", "d", "e"]], "A"),
    "Griffith's transforming principle",
    "Live S strain (virulent) killed mice; live R strain did not. Heat-killed S strain did not kill mice. A mixture of "
    "heat-killed S and live R killed the mice, and living S bacteria were recovered from them: the R strain had been "
    "transformed by some 'transforming principle' from the heat-killed S strain.",
    ["(a), (b), (d), (e): true", "(c): false, heat-killed S bacteria did not kill the mice"],
    C12_MB("the search for genetic material: transforming principle"),
    why="Options B, C and D include (c); heat-killed S bacteria alone are harmless.",
    seconds=45)

add(MBI, "DNA as genetic material", "Intermediate", "statement_pair",
    sp("RNA cannot directly code for the synthesis of proteins; it depends on DNA to express characters.",
       "DNA, being double-stranded and having a complementary strand, further resists changes by evolving a process "
       "of repair."),
    SP("D"),
    "DNA versus RNA as genetic material",
    "NCERT: RNA can directly code for the synthesis of proteins and hence can easily express characters, whereas DNA "
    "depends on RNA for protein synthesis. Statement I reverses this and is false. DNA evolved from RNA with chemical "
    "modifications that make it more stable; being double-stranded with a complementary strand, it further resists "
    "changes by evolving a repair process. Statement II is true.",
    ["Statement I: false, it is DNA that depends on RNA", "Statement II: true"],
    C12_MB("properties of genetic material; RNA world"),
    seconds=35)

add(MBI, "Transcription", "Intermediate", "match_list",
    ml(("level of regulation of gene expression in eukaryotes", "event regulated"),
       ["Transcriptional level", "Processing level", "Transport level", "Translational level"],
       ["Synthesis of the polypeptide on ribosomes from mRNA", "Formation of the primary transcript",
        "Regulation of splicing", "Movement of mRNA from the nucleus to the cytoplasm"]),
    M({"A": "II", "B": "III", "C": "IV", "D": "I"},
      [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
       {"A": "I", "B": "III", "C": "IV", "D": "II"}], "D"),
    "Levels of regulation of gene expression",
    "In eukaryotes, regulation can be exerted at (i) the transcriptional level (formation of the primary transcript), "
    "(ii) the processing level (regulation of splicing), (iii) transport of mRNA from the nucleus to the cytoplasm "
    "and (iv) the translational level.",
    ["A-II", "B-III", "C-IV", "D-I"],
    C12_MB("regulation of gene expression"),
    why="Option A swaps transcription and processing; option B swaps transport and translation; option C swaps "
        "transcription and translation.",
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "numerical",
    "The haploid human genome has approximately 3 × 10⁹ bp. If the cost of sequencing was US $3 per bp (the "
    "estimated cost at the beginning of the Human Genome Project), the approximate total cost of sequencing would be:",
    P("9 billion US dollars", ["3 billion US dollars", "1 billion US dollars", "18 billion US dollars"], "B"),
    "Scale of the Human Genome Project",
    "Cost = number of base pairs × cost per base pair = 3 × 10⁹ × 3 = 9 × 10⁹ US dollars, i.e. about 9 billion US "
    "dollars, the figure NCERT gives to show the enormity of the project.",
    ["3 × 10⁹ bp × $3/bp", "= 9 × 10⁹ = 9 billion US dollars"],
    C12_MB("human genome project"),
    why="3 billion forgets to multiply by the cost per bp; 1 billion divides instead of multiplying; 18 billion "
        "counts both copies of a diploid genome, but the estimate is for the 3 × 10⁹ bp genome.",
    seconds=40, verified_by=RECOMPUTED)

add(MBI, "Transcription", "Intermediate", "statement_pair",
    sp("The split-gene arrangement probably represents an ancient feature of the genome; the presence of introns is "
       "reminiscent of antiquity, and splicing represents the dominance of the RNA world.",
       "Split genes are typical of bacterial genes, and introns are absent from eukaryotic genes."),
    SP("C"),
    "Split genes",
    "NCERT states that split-gene arrangements probably represent an ancient feature of the genome, that introns are "
    "reminiscent of antiquity and that splicing represents the dominance of the RNA world; Statement I is true. "
    "Split genes, with exons interrupted by introns, are a feature of eukaryotes; bacterial genes are not split. "
    "Statement II is false.",
    ["Statement I: true", "Statement II: false, split genes are eukaryotic"],
    C12_MB("transcription: transcription in eukaryotes"),
    seconds=35)

add(MBI, "Replication", "Intermediate", "assertion_reason",
    ar("DNA-dependent DNA polymerases must catalyse polymerisation not only fast but also with a high degree of "
       "accuracy.",
       "Errors made during DNA replication never lead to mutations."),
    AR("C"),
    "Accuracy of DNA replication",
    "DNA polymerases have to polymerise a large number of nucleotides in a very short time and with high accuracy, "
    "so A is true. NCERT notes that any mistake during replication would result in mutations, so R is false.",
    ["A: true", "R: false, replication errors result in mutations"],
    C12_MB("replication: the machinery and the enzymes"),
    seconds=30)

add(MBI, "Genetic code and translation", "Intermediate", "statement_pair",
    sp("In its inactive state, the ribosome exists as a single, undivided particle.",
       "The translation of an mRNA into protein begins when the small subunit of the ribosome encounters the mRNA."),
    SP("D"),
    "Ribosome and initiation of translation",
    "The ribosome is the cellular factory for protein synthesis. In its inactive state it exists as two subunits, a "
    "large and a small one, so Statement I is false. When the small subunit encounters an mRNA, the process of "
    "translation begins. Statement II is true.",
    ["Statement I: false, two separate subunits", "Statement II: true"],
    C12_MB("translation"),
    seconds=30)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "multi_statement",
    ms("Which of the following statements about DNA fingerprinting are correct?",
       ["DNA from every tissue of an individual, such as blood, hair follicle, skin, bone, saliva or sperm, shows the "
        "same degree of polymorphism.",
        "The band pattern obtained differs from individual to individual in a population, except in monozygotic "
        "(identical) twins.",
        "The VNTR used as a probe belongs to a class of satellite DNA referred to as mini-satellite.",
        "The use of PCR has reduced the sensitivity of the technique, so large amounts of tissue are now needed.",
        "DNA fingerprinting is based on differences in the protein-coding sequences, which make up most of the "
        "human genome."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
    "Basis of DNA fingerprinting",
    "DNA from any tissue of an individual shows the same polymorphism, which is why blood, hair follicles, saliva or "
    "sperm can be used. The VNTR probe is a mini-satellite; VNTR sizes vary, giving bands that differ between "
    "individuals except monozygotic twins. PCR has increased the sensitivity, so DNA from a single cell is enough. "
    "Fingerprinting uses repetitive (satellite) DNA, and less than 2 per cent of the genome codes for proteins.",
    ["(a), (b), (c): true", "(d): false, PCR increased sensitivity", "(e): false, repetitive DNA is used"],
    C12_MB("DNA fingerprinting"),
    why="Options A, B and D include (d) or (e).",
    seconds=50)

add(MBI, "Replication", "Advanced", "numerical",
    "E. coli grown for many generations in a ¹⁵NH₄Cl medium is transferred to a ¹⁴NH₄Cl medium. E. coli divides once "
    "every 20 minutes and DNA replicates semiconservatively. After 80 minutes, what fractions of the DNA molecules "
    "are hybrid (¹⁵N/¹⁴N) and light (¹⁴N/¹⁴N)?",
    P("1/8 hybrid and 7/8 light", ["1/4 hybrid and 3/4 light", "1/2 hybrid and 1/2 light",
                                   "1/16 hybrid and 15/16 light"], "A"),
    "Semiconservative replication over several generations",
    "80 minutes = 4 generations, so one ¹⁵N molecule becomes 2⁴ = 16 molecules. The two original heavy strands are "
    "never lost; each ends up in one hybrid molecule. So 2 of 16 molecules (1/8) are hybrid and the remaining 14 "
    "(7/8) are light.",
    ["Generations = 80/20 = 4", "Molecules = 2⁴ = 16", "Hybrid = 2 → 2/16 = 1/8; light = 14/16 = 7/8"],
    C12_MB("replication: the experimental proof"),
    shortcut="After n generations, hybrid = 2/2ⁿ; light = 1 − 2/2ⁿ.",
    why="1/4 hybrid is the result after 60 minutes (3 generations); 1/2 after 40 minutes (2 generations); 1/16 "
        "counts only one hybrid molecule instead of two.",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "multi_statement",
    ms("Which of the following statements related to the methods and findings of the Human Genome Project are "
       "correct?",
       ["Sequence annotation is the approach of sequencing the whole genome, coding and non-coding, and later "
        "assigning functions to different regions of the sequence.",
        "The genome sequences of several non-human model organisms, such as bacteria, yeast, Caenorhabditis elegans, "
        "Drosophila, rice and Arabidopsis, have also been determined.",
        "Repetitive sequences are thought to have no direct coding functions, but they shed light on chromosome "
        "structure, dynamics and evolution.",
        "Repetitive sequences make up less than 2 per cent of the human genome and code for most proteins.",
        "The commonly used hosts for cloning DNA fragments in the project were mammalian cells."]),
    MS(["a", "b", "c"], [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "c", "e"]], "D"),
    "Methodologies and findings of the HGP",
    "Sequence annotation sequences the whole genome and later assigns functions; ESTs instead identify expressed "
    "genes. Genomes of model organisms such as bacteria, yeast, C. elegans, Drosophila, rice and Arabidopsis have "
    "also been sequenced. Repetitive sequences, repeated hundreds to thousands of times, make up a large portion of "
    "the genome, have no direct coding function, but shed light on chromosome structure, dynamics and evolution. "
    "DNA fragments were cloned in bacteria and yeast using BAC and YAC vectors.",
    ["(a), (b), (c): true", "(d): false, repeats are a large, non-coding part", "(e): false, bacteria and yeast"],
    C12_MB("human genome project: methodologies; salient features"),
    why="Options A, B and C include (d) or (e).",
    seconds=55)

add(MBI, "Lac operon", "Advanced", "direct",
    "A mutant E. coli has an altered i gene whose product (the repressor) can no longer bind to the operator. What "
    "happens to the structural genes of the lac operon in this mutant when lactose is absent?",
    P("The z, y and a genes are transcribed even though lactose is absent",
      ["The z, y and a genes stay switched off until lactose is supplied",
       "Only the i gene is transcribed; the structural genes stay silent",
       "The structural genes are transcribed but cannot be translated in the absence of lactose"], "B"),
    "Negative regulation of the lac operon",
    "Normally, in the absence of an inducer, the repressor binds the operator and prevents RNA polymerase from "
    "transcribing the operon. If the repressor cannot bind the operator, nothing blocks RNA polymerase, so the "
    "structural genes z, y and a are transcribed all the time, whether or not lactose is present.",
    ["Operon is switched off only by repressor bound to operator", "No binding → no block → continuous transcription"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Lactose acts only by inactivating the repressor, and here the repressor is already unable to act. The "
        "mRNA of the operon needs no lactose to be translated.",
    seconds=50)

add(MBI, "DNA packaging", "Advanced", "statement_pair",
    sp("The length of the DNA double helix in a typical mammalian cell is about 2.2 metres, far greater than the "
       "dimension of a typical nucleus (about 10⁻⁶ m).",
       "In eukaryotes, chromatin fibres are further coiled and condensed at the metaphase stage of cell division to "
       "form chromosomes."),
    SP("A"),
    "Packaging of the DNA helix",
    "NCERT multiplies 6.6 × 10⁹ bp by 0.34 × 10⁻⁹ m per bp to get about 2.2 m of DNA, which must fit into a "
    "nucleus of about 10⁻⁶ m; hence the need for packaging. Nucleosomes form the chromatin fibre, which is further "
    "coiled and condensed at the metaphase stage of cell division to form chromosomes. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("packaging of DNA helix"),
    seconds=35)

add(MBI, "Genetic code and translation", "Advanced", "assertion_reason",
    ar("The genetic code is nearly universal; for example, from bacteria to humans UUU codes for phenylalanine.",
       "AUG has dual functions: it codes for methionine and also acts as the initiator codon."),
    AR("B"),
    "Universality of the code and the initiator codon",
    "Both statements are features of the genetic code listed by NCERT. The near-universality of the code (with some "
    "exceptions in mitochondrial codons and some protozoans) is a separate feature from the dual role of AUG. R does "
    "not explain why UUU means phenylalanine in all these organisms.",
    ["A: true", "R: true", "Different features of the code → R does not explain A"],
    C12_MB("genetic code"),
    seconds=35)

add(MBI, "DNA and RNA structure", "Advanced", "assertion_reason",
    ar("If one strand of a DNA segment reads 5'-ATGC-3', its complementary strand, also written in the 5'→3' "
       "direction, reads 5'-GCAT-3'.",
       "In double-stranded DNA, the two polynucleotide chains run in the same direction (parallel polarity)."),
    AR("C"),
    "Antiparallel complementary strands",
    "Base pairing gives the complement 3'-TACG-5' opposite 5'-ATGC-3'. Written 5'→3', this is 5'-GCAT-3', so A is "
    "true. This works only because the two chains have antiparallel polarity (one 5'→3', the other 3'→5'); R says "
    "they are parallel and is false.",
    ["Complement of 5'-ATGC-3' = 3'-TACG-5' = 5'-GCAT-3'", "A: true", "R: false, the chains are antiparallel"],
    C12_MB("structure of polynucleotide chain: double helix"),
    seconds=45)


# ================================================================ Microbes in Human Welfare (3 / 4 / 3)
C12_MH = lambda s: ref(12, MHW, s)

add(MHW, "Biogas", "Basic", "direct",
    "In a biogas plant, the biogas produced from a slurry of cattle dung is supplied through an outlet pipe to "
    "nearby houses. NCERT states that it is used for:",
    P("Cooking and lighting", ["Producing statins", "Clarifying fruit juices", "Making Swiss cheese"], "C"),
    "Use of biogas",
    "A biogas plant has a concrete tank in which bio-wastes are collected and a slurry of dung is fed; a floating "
    "cover rises as microbial activity produces gas. An outlet pipe carries the gas to nearby houses, where the "
    "biogas is used for cooking and lighting.",
    ["Biogas (mainly methane) → cooking and lighting"],
    C12_MH("microbes in production of biogas"),
    why="Statins come from the fungus Monascus purpureus, fruit juices are clarified with pectinases and proteases, "
        "and Swiss cheese is ripened by Propionibacterium sharmanii; none uses biogas.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "The ladybird beetle (with red and black markings) and dragonflies are useful biocontrol agents. They help to get "
    "rid of, respectively:",
    P("Aphids and mosquitoes", ["Mosquitoes and aphids", "Butterfly caterpillars and aphids",
                                "Fungal plant pathogens and mosquitoes"], "A"),
    "Insect predators as biocontrol agents",
    "NCERT gives the Ladybird beetle and dragonflies as familiar examples of biological control: the Ladybird is "
    "useful to get rid of aphids and dragonflies to get rid of mosquitoes.",
    ["Ladybird → aphids", "Dragonflies → mosquitoes"],
    C12_MH("microbes as biocontrol agents"),
    why="Option B reverses the pair. Butterfly caterpillars are controlled by Bacillus thuringiensis, and fungal "
        "pathogens by Trichoderma.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "According to NCERT, the main sources of biofertilisers are:",
    P("Bacteria, fungi and cyanobacteria", ["Viruses, protozoa and algae only", "Insects and nematodes",
                                            "Synthetic urea and phosphate salts"], "D"),
    "Biofertilisers",
    "Biofertilisers are organisms that enrich the nutrient quality of the soil. The main sources are bacteria (e.g. "
    "Rhizobium, Azotobacter, Azospirillum), fungi (mycorrhiza-forming Glomus) and cyanobacteria (Anabaena, Nostoc, "
    "Oscillatoria).",
    ["Biofertilisers: bacteria, fungi, cyanobacteria"],
    C12_MH("microbes as biofertilisers"),
    why="Urea and phosphate salts are chemical fertilisers; insects, nematodes, viruses and protozoa are not the "
        "sources NCERT lists.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "statement_pair",
    sp("In paddy fields, cyanobacteria are weeds that reduce soil fertility.",
       "Plants having mycorrhizal associations show resistance to root-borne pathogens, tolerance to salinity and "
       "drought, and an overall increase in plant growth and development."),
    SP("D"),
    "Cyanobacteria and mycorrhiza as biofertilisers",
    "Cyanobacteria are autotrophic microbes, many of which fix atmospheric nitrogen; in paddy fields they serve as an "
    "important biofertiliser and also add organic matter, increasing fertility. Statement I is false. Besides helping "
    "in phosphorus absorption, mycorrhiza (e.g. Glomus) gives the plant resistance to root-borne pathogens, tolerance "
    "to salinity and drought and better overall growth. Statement II is true.",
    ["Statement I: false, cyanobacteria are an important biofertiliser in paddy", "Statement II: true"],
    C12_MH("microbes as biofertilisers"),
    seconds=35)

add(MHW, "Sewage treatment", "Intermediate", "assertion_reason",
    ar("In secondary treatment, the primary effluent is passed into large aeration tanks where it is constantly "
       "agitated mechanically and air is pumped into it.",
       "Agitation and aeration promote the growth of anaerobic methanogens, which form flocs in the aeration tank."),
    AR("C"),
    "Aeration tanks in secondary treatment",
    "A is NCERT's description of the aeration tank. The purpose is to allow vigorous growth of useful aerobic microbes "
    "into flocs (bacteria associated with fungal filaments), which consume the organic matter and reduce the BOD. "
    "Methanogens are anaerobic and act later, in the anaerobic sludge digesters. R is false.",
    ["A: true", "R: false, aeration favours aerobic flocs; methanogens work in anaerobic digesters"],
    C12_MH("microbes in sewage treatment: secondary treatment"),
    seconds=35)

add(MHW, "Household and industrial products", "Intermediate", "statement_pair",
    sp("Microbes are also used to ferment fish, soybean and bamboo shoots to make foods.",
       "Saccharomyces cerevisiae, commonly called brewer's yeast, is used for fermenting malted cereals and fruit "
       "juices to produce citric acid."),
    SP("C"),
    "Microbes in foods and beverages",
    "NCERT notes that microbes are used to ferment fish, soybean and bamboo shoots to make foods; Statement I is true. "
    "Saccharomyces cerevisiae (brewer's yeast) ferments malted cereals and fruit juices to produce ethanol, not citric "
    "acid; citric acid is produced by the fungus Aspergillus niger. Statement II is false.",
    ["Statement I: true", "Statement II: false, the product is ethanol"],
    C12_MH("microbes in household products; fermented beverages"),
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "multi_statement",
    ms("Which of the following statements about Bacillus thuringiensis (Bt) as a biocontrol agent are correct?",
       ["It is available in sachets as dried spores, which are mixed with water and sprayed onto vulnerable plants.",
        "When the insect larvae eat the sprayed spores, the toxin is released in their gut and the larvae are killed.",
        "The bacterial disease kills the caterpillars but leaves other insects unharmed.",
        "Its toxin genes have been introduced into plants, such as Bt cotton, making them resistant to insect pests.",
        "Bt is a fungus that is used mainly to kill weeds."]),
    MS(["a", "b", "c", "d"], [["a", "b", "e"], ["a", "c", "d", "e"], ["b", "d", "e"]], "B"),
    "Bacillus thuringiensis",
    "Bt spores are sold as dried spores in sachets, mixed with water and sprayed on plants such as brassicas and fruit "
    "trees. Insect larvae eat them; the toxin is released in the gut and kills the larvae. The disease kills the "
    "caterpillars but leaves other insects unharmed. Using genetic engineering, Bt toxin genes have been put into "
    "plants (Bt cotton) to make them resistant to insect pests. Bt is a bacterium, and it controls insects, not "
    "weeds.",
    ["(a)-(d): true", "(e): false, Bt is a bacterium acting on insects"],
    C12_MH("microbes as biocontrol agents"),
    why="Options A, C and D include (e).",
    seconds=45)

add(MHW, "Sewage treatment", "Advanced", "match_list",
    ml(("step in municipal sewage treatment", "what happens"),
       ["Sequential filtration in primary treatment", "Sedimentation in primary treatment",
        "Settling tank after the aeration tank", "Effluent from secondary treatment"],
       ["Generally released into natural water bodies such as rivers and streams",
        "Removal of grit (soil and small pebbles)", "Removal of floating debris",
        "Bacterial flocs sediment to form activated sludge"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Stages of sewage treatment",
    "In primary treatment, floating debris is removed by sequential filtration and then grit (soil and small "
    "pebbles) by sedimentation; the settled solids form the primary sludge and the supernatant is the primary "
    "effluent. After the aeration tanks, the effluent passes to a settling tank where the bacterial flocs sediment as "
    "activated sludge. The effluent from secondary treatment is generally released into natural water bodies such as "
    "rivers and streams.",
    ["A-III", "B-II", "C-IV", "D-I"],
    C12_MH("microbes in sewage treatment"),
    why="Option B swaps filtration and sedimentation; option C swaps the settling tank and the final effluent; "
        "option D places grit removal in the settling tank.",
    seconds=50)

add(MHW, "Household and industrial products", "Advanced", "assertion_reason",
    ar("A small amount of curd added to fresh milk as an inoculum or starter converts the milk into curd.",
       "The starter contains millions of lactic acid bacteria, which multiply at suitable temperatures and convert the "
       "milk to curd."),
    AR("A"),
    "Curd starter",
    "NCERT: a small amount of curd added to fresh milk as inoculum or starter contains millions of LAB, which at "
    "suitable temperatures multiply, thus converting milk to curd (LAB produce acids that coagulate and partially "
    "digest the milk proteins). R explains A.",
    ["A: true", "R: true", "The LAB in the starter are what convert the milk"],
    C12_MH("microbes in household products"),
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "multi_statement",
    ms("Which of the following statements reflect the approach of organic farming and biological control described "
       "in NCERT?",
       ["A key belief of the organic farmer is that biodiversity furthers health.",
        "The more variety a landscape has, the more sustainable it is.",
        "Becoming familiar with the life forms in the field, predators and pests, their life cycles, patterns of "
        "feeding and preferred habitats, helps develop appropriate means of biocontrol.",
        "The use of biocontrol measures increases our dependence on toxic chemicals and pesticides.",
        "Chemical pesticides kill only harmful insects and spare the useful ones."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["c", "d", "e"], ["a", "b", "c", "e"]], "D"),
    "Biological farming approach",
    "The organic farmer believes that biodiversity furthers health and that the more variety a landscape has, the "
    "more sustainable it is. Knowing the life forms of the field, predators as well as pests, with their life cycles, "
    "feeding patterns and habitats, helps develop appropriate biocontrol. Biocontrol reduces dependence on toxic "
    "chemicals, which kill useful and harmful organisms alike and pollute soil, ground water and crops.",
    ["(a), (b), (c): true", "(d): false, biocontrol reduces dependence", "(e): false"],
    C12_MH("microbes as biocontrol agents"),
    why="Options A, B and C include (d) or (e).",
    seconds=45)

# ================================================================ Organisms and Populations (4 / 5 / 4)
C12_OP = lambda s: ref(12, OAP, s)

# exponential growth Nt = N0 e^(rt) with ln 2 = 0.693
N0, r_e, t_e = 250, 0.0231, 60
assert abs(r_e * t_e - 2 * 0.693) < 1e-9          # rt = 1.386 = 2 ln 2, i.e. two doublings
assert N0 * 2 ** 2 == 1000
assert abs(N0 * math.exp(r_e * t_e) - 1000) < 1                # direct check with e
assert N0 * 2 == 500 and N0 * 2 ** 3 == 2000 and int(N0 * (1 + r_e * t_e) + 0.5) == 597   # distractors

# interactions: effect on (species 1, species 2)
interactions = {"mutualism": (+1, +1), "competition": (-1, -1), "predation": (+1, -1), "parasitism": (+1, -1),
                "commensalism": (+1, 0), "amensalism": (-1, 0)}
no_gain = sorted(k for k, v in interactions.items() if max(v) <= 0)
assert no_gain == ["amensalism", "competition"]

add(OAP, "Population attributes", "Basic", "direct",
    "An age pyramid in which the pre-reproductive and reproductive age groups are nearly equal, giving a bell shape, "
    "represents a population that is:",
    P("Stable", ["Expanding", "Declining", "Becoming extinct within a generation"], "C"),
    "Age pyramids",
    "Age pyramids show the proportions of pre-reproductive, reproductive and post-reproductive individuals. A "
    "triangular pyramid with a broad base indicates an expanding population, a bell-shaped one a stable population "
    "and an urn-shaped one a declining population.",
    ["Bell-shaped age pyramid → stable population"],
    C12_OP("population attributes"),
    why="Expanding populations give a broad-based triangular pyramid and declining ones an urn shape; NCERT does not "
        "link any shape to extinction within a generation.",
    seconds=20)

add(OAP, "Population attributes", "Basic", "direct",
    "NCERT illustrates that population size can vary enormously, from fewer than 10 individuals to millions. Which "
    "pair does it use as examples of these two extremes?",
    P("Siberian cranes at the Bharatpur wetlands in any year; Chlamydomonas in a pond",
      ["Tigers in a national park; Parthenium plants in a field", "Banyan trees in a village; fish in a lake",
       "Elephants in a forest; fruit flies in a laboratory culture"], "B"),
    "Population size",
    "NCERT: the size of a population could be as low as fewer than 10 (Siberian cranes at Bharatpur wetlands in any "
    "year) or go into millions (Chlamydomonas in a pond). Population size, technically called population density "
    "(N), is not a static parameter.",
    ["< 10: Siberian cranes at Bharatpur", "Millions: Chlamydomonas in a pond"],
    C12_OP("population attributes"),
    why="The other pairs mix organisms NCERT uses for other points (tiger census, percent cover of a banyan, the "
        "elephant in exponential growth), not as the extremes of population size.",
    seconds=25)

add(OAP, "Population interactions", "Basic", "direct",
    "In interference competition between two species:",
    P("The feeding efficiency of one species is reduced by the interfering and inhibitory presence of the other, even "
      "if resources are abundant",
      ["Both species benefit from sharing the same food", "One species benefits and the other is unaffected",
       "Competition occurs only when food and space are in short supply"], "D"),
    "Interference competition",
    "Competition is usually thought to occur when species compete for the same limiting resources. But NCERT notes "
    "that in interference competition, the feeding efficiency of one species might be reduced due to the interfering "
    "and inhibitory presence of the other species, even if resources (food and space) are abundant.",
    ["Interference competition can occur even with abundant resources"],
    C12_OP("population interactions: competition"),
    why="Option A describes mutualism and option B commensalism; option C is exactly what interference competition "
        "contradicts.",
    seconds=25)

add(OAP, "Population growth", "Basic", "direct",
    "To show that any species growing exponentially under unlimited resources can reach enormous population "
    "densities in a short time, Darwin used the example of a slow-growing animal. That animal was the:",
    P("Elephant", ["Fruit fly", "Flour beetle", "Norway rat"], "A"),
    "Exponential growth",
    "NCERT: any species growing exponentially under unlimited resource conditions can reach enormous population "
    "densities in a short time. Darwin showed how even a slow-growing animal like the elephant could reach enormous "
    "numbers in the absence of checks.",
    ["Even the slow-breeding elephant → enormous numbers without checks"],
    C12_OP("population growth: exponential growth"),
    why="Fruit flies, flour beetles and Norway rats are fast breeders, so they would not make Darwin's point about a "
        "slow-growing animal.",
    seconds=20)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("In the absence of predators, prey populations would always decline because they lose their source of food.",
       "Interspecific interactions arise from the interaction of populations of the same species."),
    SP("B"),
    "Role of predators; interspecific interactions",
    "NCERT: predators keep prey populations under control; but for predators, prey species could achieve very high "
    "population densities and cause ecosystem instability. Predators are not the food of their prey, so Statement I is "
    "false. Interspecific interactions arise from the interaction of populations of two different species, so "
    "Statement II is also false.",
    ["Statement I: false, prey could reach very high densities", "Statement II: false, two different species"],
    C12_OP("population interactions: predation"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("Many marine fish are infested with ectoparasitic copepods.",
       "The life cycles of endoparasites are simpler than those of ectoparasites, because endoparasites live in a "
       "protected environment."),
    SP("C"),
    "Ectoparasites and endoparasites",
    "Ectoparasites feed on the external surface of the host: lice on humans, ticks on dogs and copepods on many marine "
    "fish; Statement I is true. Endoparasites live inside the host body at different sites (liver, kidney, lungs, red "
    "blood cells); NCERT states that their life cycles are more complex because of their extreme specialisation. "
    "Statement II is false.",
    ["Statement I: true", "Statement II: false, endoparasite life cycles are more complex"],
    C12_OP("population interactions: parasitism"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("When certain exotic species are introduced into a geographical area, they become invasive and start spreading "
       "fast.",
       "Predators act as conduits for energy transfer across trophic levels."),
    AR("B"),
    "Invasive species and the roles of predators",
    "Both are NCERT statements. Exotic species become invasive because the invaded land does not have their natural "
    "predators (as with the prickly pear cactus in Australia). R describes a different role of predators, transferring "
    "energy across trophic levels, and does not explain why exotics spread.",
    ["A: true (no natural predators in the new land)", "R: true", "R is a different role of predators"],
    C12_OP("population interactions: predation"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("In nature, plants rarely need the help of animals for pollinating their flowers or dispersing their seeds.",
       "Plants offer rewards or 'fees' to animals in the form of pollen and nectar for pollinators and juicy and "
       "nutritious fruits for seed dispersers."),
    AR("D"),
    "Plant-animal mutualism",
    "NCERT: plants need the help of animals for pollinating their flowers and dispersing their seeds, so A is false. "
    "Animals have to be 'paid' for these services: plants offer pollen and nectar to pollinators and juicy, "
    "nutritious fruits to seed dispersers. R is true.",
    ["A: false, plants commonly depend on animals for pollination and dispersal", "R: true"],
    C12_OP("population interactions: mutualism"),
    seconds=30)

add(OAP, "Population attributes", "Intermediate", "statement_pair",
    sp("Population density must always be expressed as the number of individuals.",
       "The total number of individuals in a population is always easy to determine and is never meaningless as a "
       "measure of population size."),
    SP("B"),
    "Measuring population density",
    "NCERT: population size, technically called population density (N), need not necessarily be measured in numbers "
    "only; percent cover or biomass may be used. Although the total number is generally the most appropriate measure, "
    "it is in some cases either meaningless or difficult to determine. Both statements are false.",
    ["Statement I: false, cover or biomass may be used", "Statement II: false, sometimes meaningless or difficult"],
    C12_OP("population attributes"),
    seconds=30)

add(OAP, "Population interactions", "Advanced", "statement_pair",
    sp("Two species competing for the same resource could avoid competition by choosing, for instance, different times "
       "for feeding or different foraging patterns.",
       "A species whose distribution is restricted to a small geographical area because of a competitively superior "
       "species is found to expand its distributional range dramatically when the competing species is experimentally "
       "removed; this is called competitive release."),
    SP("A"),
    "Resource partitioning and competitive release",
    "NCERT notes that species facing competition might evolve mechanisms that promote co-existence rather than "
    "exclusion, such as resource partitioning: different feeding times or foraging patterns. It also cites competitive "
    "release, the dramatic range expansion of a restricted species when its superior competitor is removed, as "
    "evidence that competition occurs in nature. Both statements are true.",
    ["Statement I: true (resource partitioning)", "Statement II: true (competitive release)"],
    C12_OP("population interactions: competition"),
    seconds=45)

add(OAP, "Population growth", "Advanced", "numerical",
    "A population of 250 individuals grows exponentially according to Nₜ = N₀e^(rt), with r = 0.0231 per year. "
    "Taking ln 2 = 0.693, what will the population size be after 60 years?",
    P("1000", ["500", "597", "2000"], "D"),
    "Integral form of exponential growth",
    "rt = 0.0231 × 60 = 1.386 = 2 × 0.693 = 2 ln 2. So e^(rt) = e^(2 ln 2) = 2² = 4, and Nₜ = 250 × 4 = 1000. The "
    "population doubles every 0.693/0.0231 = 30 years, i.e. twice in 60 years.",
    ["rt = 0.0231 × 60 = 1.386", "1.386 = 2 ln 2 → e^(rt) = 4", "Nₜ = 250 × 4 = 1000"],
    C12_OP("population growth: exponential growth"),
    shortcut="Doubling time = ln 2 / r = 30 years; 60 years = 2 doublings.",
    why="500 counts only one doubling; 597 treats growth as linear, 250 × (1 + rt); 2000 counts three doublings.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    ms("Which of the following statements about parasitism are correct?",
       ["Parasites may reduce the survival, growth and reproduction of the host and reduce its population density.",
        "Parasites might render the host more vulnerable to predation by making it physically weak.",
        "Brood parasitism is shown by Cuscuta growing on hedge plants.",
        "Endoparasites have elaborate morphological and anatomical features and a low reproductive potential.",
        "The eggs of a brood-parasitic bird have evolved to resemble the host's eggs in size and colour."]),
    MS(["a", "b", "e"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "B"),
    "Effects and adaptations of parasites",
    "Parasites may reduce host survival, growth, reproduction and population density, and can make the host "
    "physically weak and more vulnerable to predation. In brood parasitism (e.g. the cuckoo laying eggs in the crow's "
    "nest) the parasite's eggs resemble the host's in size and colour, reducing the chance of detection. Cuscuta is a "
    "parasitic plant, not a brood parasite. Endoparasites have greatly simplified morphological and anatomical features "
    "while emphasising their reproductive potential.",
    ["(a), (b), (e): true", "(c): false, Cuscuta is a plant parasite", "(d): false, features simplified, high "
     "reproductive potential"],
    C12_OP("population interactions: parasitism"),
    why="Options A, C and D include (c) or (d).",
    seconds=50)

add(OAP, "Population interactions", "Advanced", "direct",
    "Considering the effect of each interspecific interaction on the two species involved, in which pair of "
    "interactions does neither species benefit?",
    P("Competition and amensalism", ["Predation and parasitism", "Mutualism and commensalism",
                                     "Commensalism and amensalism"], "A"),
    "Classification of population interactions",
    "Mutualism (+, +) benefits both; predation and parasitism (+, −) benefit one species; commensalism (+, 0) "
    "benefits one. In competition (−, −) both lose, and in amensalism (−, 0) one is harmed and the other unaffected, "
    "so neither species benefits in these two.",
    ["Competition: −/−", "Amensalism: −/0", "All others have at least one +"],
    C12_OP("population interactions"),
    why="Predation, parasitism and commensalism each benefit one species, and mutualism benefits both.",
    seconds=40, verified_by=RECOMPUTED)


# ================================================================ Ecosystem (4 / 5 / 4)
C12_EC = lambda s: ref(12, ECO, s)

# energy flow: incident 10^6 kJ, 40 % PAR, 2 % of PAR fixed as GPP, producers respire 30 % of GPP
incident, par_frac, capture, resp = 10 ** 6, F(40, 100), F(2, 100), F(30, 100)
gpp = incident * par_frac * capture
npp = gpp * (1 - resp)
assert gpp == 8000 and npp == 5600
assert incident * capture * (1 - resp) == 14000 and gpp * resp == 2400    # distractors

# trophic levels of the snake in a small food web (producer = level 1)
web = {"grass": [], "grasshopper": ["grass"], "rabbit": ["grass"], "frog": ["grasshopper"],
       "snake": ["frog", "rabbit"], "hawk": ["snake"]}


def levels(sp_):
    if not web[sp_]:
        return {1}
    return {lv + 1 for food in web[sp_] for lv in levels(food)}


assert levels("snake") == {3, 4} and levels("hawk") == {4, 5}

add(ECO, "Structure and components", "Basic", "direct",
    "Which of the following may be considered a man-made ecosystem?",
    P("An aquarium", ["A grassland", "An estuary", "A desert"], "B"),
    "Types of ecosystems",
    "Ecosystems are broadly terrestrial (forest, grassland, desert) or aquatic (pond, lake, wetland, river, estuary). "
    "NCERT adds that crop fields and an aquarium may also be considered man-made ecosystems.",
    ["Man-made ecosystems: crop field, aquarium"],
    C12_EC("ecosystem: structure and function"),
    why="Grasslands and deserts are natural terrestrial ecosystems; an estuary is a natural aquatic ecosystem.",
    seconds=20)

add(ECO, "Structure and components", "Basic", "direct",
    "The common herbivores (primary consumers) of an aquatic ecosystem, according to NCERT, are:",
    P("Molluscs", ["Mammals", "Fishes that feed on other fishes", "Fungi and bacteria"], "B"),
    "Consumers in aquatic ecosystems",
    "Animals that feed on producers are primary consumers (herbivores). NCERT names insects, birds and mammals as the "
    "common herbivores of terrestrial ecosystems and molluscs in aquatic ecosystems.",
    ["Aquatic herbivores: molluscs"],
    C12_EC("energy flow"),
    why="Mammals are listed as terrestrial herbivores; fish-eating fishes are carnivores; fungi and bacteria are "
        "decomposers.",
    seconds=20)

add(ECO, "Ecological pyramids", "Basic", "direct",
    "The three ecological pyramids that are usually studied are the pyramids of:",
    P("Number, biomass and energy", ["Number, area and age", "Biomass, productivity and decomposition",
                                     "Energy, sex ratio and natality"], "A"),
    "Types of ecological pyramids",
    "In an ecological pyramid the base is formed by the producers (first trophic level) and the apex by the top-level "
    "consumers. The three pyramids usually studied are the pyramid of number, the pyramid of biomass and the pyramid "
    "of energy.",
    ["Pyramids of number, biomass and energy"],
    C12_EC("ecological pyramids"),
    why="Area, age, sex ratio and natality are population attributes or measures, and productivity and "
        "decomposition are ecosystem functions, not types of pyramid.",
    seconds=20)

add(ECO, "Energy flow", "Basic", "direct",
    "The natural interconnection of food chains in an ecosystem makes a:",
    P("Food web", ["Trophic level", "Standing crop", "Ecological pyramid"], "C"),
    "Food web",
    "In nature, food chains do not run in isolation. NCERT: the natural interconnection of food chains makes it a "
    "food web.",
    ["Interconnected food chains = food web"],
    C12_EC("energy flow"),
    why="A trophic level is a specific place in a food chain; standing crop is the biomass at a trophic level; an "
        "ecological pyramid represents the food or energy relationship between levels.",
    seconds=20)

add(ECO, "Energy flow", "Intermediate", "assertion_reason",
    ar("Ecosystems need a constant supply of energy to synthesise the molecules they require.",
       "Ecosystems are not exempt from the second law of thermodynamics, and the energy supply counteracts the "
       "universal tendency towards increasing disorderliness."),
    AR("A"),
    "Energy flow and the second law of thermodynamics",
    "NCERT: ecosystems are not exempt from the second law of thermodynamics. They need a constant supply of energy to "
    "synthesise the molecules they require, to counteract the universal tendency toward increasing disorderliness. "
    "R gives the reason for A.",
    ["A: true", "R: true", "Second law → constant energy input needed → R explains A"],
    C12_EC("energy flow"),
    seconds=35)

add(ECO, "Productivity and decomposition", "Intermediate", "assertion_reason",
    ar("Decomposition is quicker if the detritus is rich in nitrogen and water-soluble substances such as sugars.",
       "Temperature and soil moisture have no influence on the rate of decomposition."),
    AR("C"),
    "Factors affecting decomposition",
    "The rate of decomposition is controlled by the chemical composition of the detritus and by climatic factors. "
    "Decomposition is quicker if the detritus is rich in nitrogen and water-soluble substances like sugars, and slower "
    "if it is rich in lignin and chitin, so A is true. Temperature and soil moisture are the most important climatic "
    "factors that regulate decomposition through their effects on soil microbes, so R is false.",
    ["A: true", "R: false, temperature and moisture are the key climatic regulators"],
    C12_EC("decomposition"),
    seconds=35)

add(ECO, "Productivity and decomposition", "Intermediate", "statement_pair",
    sp("Primary production is expressed in terms of weight (g m⁻²) or energy (kcal m⁻²).",
       "The rate of biomass production is called the standing crop."),
    SP("C"),
    "Primary production and productivity",
    "Primary production is the amount of biomass or organic matter produced per unit area over a time period by "
    "plants during photosynthesis, expressed as weight (g m⁻²) or energy (kcal m⁻²); Statement I is true. The rate "
    "of biomass production is called productivity. Standing crop is the mass of living material at a trophic level "
    "at a particular time, a quantity rather than a rate. Statement II is false.",
    ["Statement I: true", "Statement II: false, the rate is productivity"],
    C12_EC("productivity"),
    seconds=30)

add(ECO, "Ecological pyramids", "Intermediate", "direct",
    "In a pyramid of energy, each bar indicates:",
    P("The amount of energy present at each trophic level in a given time, or annually, per unit area",
      ["The number of species present at each trophic level", "The dry weight of a single individual of each "
                                                              "trophic level",
       "The energy lost as heat by the whole ecosystem in a year"], "D"),
    "Pyramid of energy",
    "The pyramid of energy is always upright, because some energy is lost as heat at each transfer. NCERT states that "
    "each bar in the energy pyramid indicates the amount of energy present at each trophic level in a given time or "
    "annually per unit area.",
    ["Each bar = energy at that trophic level per unit area per unit time"],
    C12_EC("ecological pyramids"),
    why="Pyramids deal with individuals, biomass or energy at a trophic level, not the number of species; biomass "
        "pyramids use all organisms, not a single individual; heat loss is not what the bars show.",
    seconds=30)

add(ECO, "Energy flow", "Intermediate", "match_list",
    ml(("organism in the food chain grass → grasshopper → frog → snake", "position in the food chain"),
       ["Grasshopper", "Frog", "Snake", "Grass"],
       ["Primary carnivore (secondary consumer), third trophic level", "Producer, first trophic level",
        "Herbivore (primary consumer), second trophic level",
        "Secondary carnivore (tertiary consumer), fourth trophic level"]),
    M({"A": "III", "B": "I", "C": "IV", "D": "II"},
      [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
       {"A": "II", "B": "I", "C": "IV", "D": "III"}], "B"),
    "Trophic levels in a grazing food chain",
    "Producers (grass) form the first trophic level. Herbivores (grasshopper) are primary consumers at the second "
    "level. Consumers that eat herbivores (frog) are primary carnivores, i.e. secondary consumers, at the third "
    "level. Those that eat primary carnivores (snake) are secondary carnivores, i.e. tertiary consumers, at the "
    "fourth level.",
    ["A-III", "B-I", "C-IV", "D-II"],
    C12_EC("energy flow: trophic levels"),
    why="Option A swaps grasshopper and frog; option C swaps frog and snake; option D swaps grass and grasshopper.",
    seconds=40)

add(ECO, "Productivity and decomposition", "Advanced", "numerical",
    "A field receives 10,00,000 kJ of incident solar radiation. Assume that 40 per cent of it is photosynthetically "
    "active radiation (PAR), that the plants fix 2 per cent of the PAR as gross primary productivity (GPP), and that "
    "the plants use 30 per cent of their GPP in respiration. What is the net primary productivity (NPP)?",
    P("5,600 kJ", ["8,000 kJ", "14,000 kJ", "2,400 kJ"], "A"),
    "From incident radiation to net primary productivity",
    "PAR = 40% of 10,00,000 = 4,00,000 kJ. GPP = 2% of PAR = 8,000 kJ. Respiration = 30% of GPP = 2,400 kJ. "
    "NPP = GPP − respiration = 8,000 − 2,400 = 5,600 kJ. (NCERT: less than 50 per cent of incident radiation is PAR, "
    "and plants capture only 2–10 per cent of the PAR.)",
    ["PAR = 0.4 × 10⁶ = 4 × 10⁵ kJ", "GPP = 0.02 × 4 × 10⁵ = 8,000 kJ", "NPP = 8,000 × 0.7 = 5,600 kJ"],
    C12_EC("productivity; energy flow"),
    why="8,000 kJ is the GPP (respiration not subtracted); 14,000 kJ applies 2 per cent to the total radiation "
        "instead of the PAR; 2,400 kJ is the respiratory loss.",
    seconds=70, verified_by=RECOMPUTED)

add(ECO, "Energy flow", "Advanced", "direct",
    "In a food web, grass is eaten by grasshoppers and rabbits; frogs eat grasshoppers; snakes eat frogs and rabbits; "
    "and hawks eat snakes. Taking producers as the first trophic level, the snake occupies:",
    P("The third and fourth trophic levels at the same time", ["Only the third trophic level",
                                                               "Only the fourth trophic level",
                                                               "The second and third trophic levels"], "C"),
    "An organism at more than one trophic level",
    "Through grass → rabbit → snake, the snake is at the third trophic level (primary carnivore). Through grass → "
    "grasshopper → frog → snake, it is at the fourth (secondary carnivore). A species can occupy more than one trophic "
    "level in the same ecosystem at the same time, because a trophic level is a functional level, not a species.",
    ["Via rabbit: level 3", "Via grasshopper → frog: level 4", "Snake: levels 3 and 4"],
    C12_EC("energy flow: trophic levels"),
    why="Options A and B each take only one of the two chains; the snake never eats producers, so it cannot be at the "
        "second level.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Advanced", "direct",
    "Four samples of detritus are left to decompose under different conditions. Which is expected to decompose "
    "fastest?",
    P("Nitrogen-rich leaf litter with plenty of soluble sugars, in warm, moist, well-aerated soil",
      ["Woody bark rich in lignin, in warm, moist, well-aerated soil",
       "Nitrogen-rich leaf litter with plenty of soluble sugars, in cold, waterlogged (anaerobic) soil",
       "Insect exoskeletons rich in chitin, in cold, dry soil"], "B"),
    "Chemical and climatic control of decomposition",
    "Decomposition is quicker when detritus is rich in nitrogen and water-soluble substances such as sugars, and slower "
    "when it is rich in lignin and chitin. A warm and moist environment favours decomposition, while low temperature "
    "and anaerobiosis inhibit it; decomposition is largely an oxygen-requiring process. Both favourable factors occur "
    "together only in the keyed option.",
    ["Favourable chemistry: N and sugars", "Favourable climate: warm, moist, aerobic", "Both together → fastest"],
    C12_EC("decomposition"),
    why="Option A has resistant lignin; option C has good chemistry but cold, anaerobic conditions; option D has "
        "both resistant chitin and cold, dry conditions.",
    seconds=45)

add(ECO, "Structure and components", "Advanced", "multi_statement",
    ms("Which of the following statements about a pond as an ecosystem are correct?",
       ["A pond is a shallow water body in which all the basic components of an ecosystem are well exhibited.",
        "A pond is fairly a self-sustainable unit and a rather simple example that explains even the complex "
        "interactions in an aquatic ecosystem.",
        "Energy flow in a pond is cyclic: the heat released by consumers is reused by the autotrophs.",
        "A pond lacks decomposers because decomposition takes place only on land.",
        "The rate of function of the pond community is regulated by solar input, the cycle of temperature, day-length "
        "and other climatic conditions."]),
    MS(["a", "b", "e"], [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d", "e"]], "D"),
    "The pond ecosystem",
    "NCERT uses the pond as a fairly self-sustainable and simple example of an aquatic ecosystem in which all the "
    "basic components are well exhibited. Its functioning depends on solar input, the temperature cycle, day-length "
    "and other climatic conditions. Energy flows in one direction towards higher trophic levels and is lost as heat; "
    "it is not recycled. Decomposers such as fungi, bacteria and flagellates are especially abundant at the bottom of "
    "the pond.",
    ["(a), (b), (e): true", "(c): false, energy flow is unidirectional", "(d): false, decomposers are present"],
    C12_EC("ecosystem: structure and function"),
    why="Options A, B and C include (c) or (d).",
    seconds=45)

# ================================================================ Biodiversity and Conservation (4 / 5 / 4)
C12_BD = lambda s: ref(12, BDC, s)

# species-area relationship log S = log C + Z log A, i.e. S = C A^Z; area x32 with Z = 0.2
Z, area_factor = F(1, 5), 32
species_factor = 2 ** (5 * Z)                     # 32^0.2 = (2^5)^(1/5) = 2
assert species_factor == 2 and abs(area_factor ** float(Z) - 2) < 1e-12
assert area_factor * Z == F(32, 5) and 1 + Z == F(6, 5)                # distractors 6.4 and 1.2

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "For the species–area relationship, log S = log C + Z log A, NCERT notes that the value of Z for areas within a "
    "region is amazingly similar, regardless of the taxonomic group or the region. It lies in the range:",
    P("0.1 to 0.2", ["0.6 to 1.2", "1.5 to 2.0", "0.01 to 0.02"], "B"),
    "Species–area relationship",
    "Whether it is plants in Britain, birds in California or molluscs in New York state, the slopes (Z) of the "
    "regression lines are amazingly similar, in the range 0.1 to 0.2. Much steeper slopes (0.6 to 1.2) are found only "
    "when very large areas such as entire continents are analysed.",
    ["Within a region: Z = 0.1–0.2"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    why="0.6 to 1.2 is the range for very large areas such as continents; the other ranges are not given by NCERT.",
    seconds=25)

add(BDC, "In situ and ex situ conservation", "Basic", "direct",
    "In many cultures, tracts of forest were set aside as sacred groves. In such groves:",
    P("All the trees and wildlife are venerated and given total protection",
      ["Only commercially valuable timber trees are protected",
       "Trees may be felled freely but wildlife is protected", "Exotic species are planted to raise productivity"], "C"),
    "Sacred groves",
    "NCERT: in many cultures tracts of forest were set aside, and all the trees and wildlife within were venerated "
    "and given total protection. Such sacred groves are found in the Khasi and Jaintia Hills in Meghalaya, the "
    "Aravalli Hills of Rajasthan, the Western Ghat regions of Karnataka and Maharashtra, and the Sarguja, Chanda and "
    "Bastar areas of Madhya Pradesh. They are an in situ means of conservation.",
    ["Sacred groves: total protection of all trees and wildlife"],
    C12_BD("biodiversity conservation: in situ conservation"),
    why="Protection in sacred groves is total, not selective, and they preserve native vegetation rather than "
        "introducing exotic species.",
    seconds=20)

add(BDC, "In situ and ex situ conservation", "Basic", "direct",
    "Which statement about zoological parks as a means of conservation is correct according to NCERT?",
    P("Many animals that have become extinct in the wild continue to be maintained in zoological parks",
      ["They are a means of in situ conservation", "They protect the whole ecosystem of the animals they keep",
       "No animal that is extinct in the wild is kept in them"], "D"),
    "Ex situ conservation in zoos",
    "Zoological parks, botanical gardens and wildlife safari parks are means of ex situ conservation, in which "
    "threatened species are taken out of their natural habitat and given special care. NCERT notes that many "
    "animals that have become extinct in the wild continue to be maintained in zoological parks.",
    ["Zoos: ex situ", "Some species extinct in the wild survive in zoos"],
    C12_BD("biodiversity conservation: ex situ conservation"),
    why="Zoos are ex situ, not in situ; they keep individual species, not whole ecosystems; option D contradicts "
        "NCERT's statement.",
    seconds=25)

add(BDC, "Importance and loss", "Basic", "direct",
    "Careful analysis of records shows that extinctions across taxa are not random. Which group does NCERT mention as "
    "appearing more vulnerable to extinction?",
    P("Amphibians", ["Insects", "Bacteria", "Fungi"], "A"),
    "Vulnerability to extinction",
    "NCERT: extinctions across taxa are not random; some groups, like amphibians, appear to be more vulnerable to "
    "extinction.",
    ["More vulnerable group: amphibians"],
    C12_BD("loss of biodiversity"),
    why="NCERT names amphibians, not insects, bacteria or fungi, as the more vulnerable group.",
    seconds=20)

add(BDC, "In situ and ex situ conservation", "Intermediate", "statement_pair",
    sp("Biodiversity knows no political boundaries, and its conservation is therefore a collective responsibility of "
       "all nations.",
       "When we conserve and protect a whole ecosystem, its biodiversity at all levels is protected; for example, we "
       "save the entire forest to save the tiger."),
    SP("A"),
    "In situ conservation and global responsibility",
    "NCERT states that biodiversity knows no political boundaries and its conservation is a collective "
    "responsibility of all nations, as recognised at the Earth Summit (1992). It also explains in situ (on site) "
    "conservation: protecting the whole ecosystem protects biodiversity at all levels, e.g. saving the entire forest "
    "to save the tiger. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_BD("biodiversity conservation"),
    seconds=35)

add(BDC, "Importance and loss", "Intermediate", "assertion_reason",
    ar("Loss of a key species that drives a major ecosystem function is a more serious threat to the ecosystem than "
       "the loss of a few other species.",
       "A key species drives a major ecosystem function, so its removal disrupts that function for the whole "
       "ecosystem, whereas the functions of many other species overlap."),
    AR("A"),
    "Rivet popper hypothesis",
    "Paul Ehrlich compared an ecosystem to an airplane and species to its rivets. Removing rivets one by one may not "
    "affect flight safety at first, but over time the plane weakens. Which rivets are lost also matters: losing rivets "
    "on the wings (key species that drive major ecosystem functions) is a more serious threat than losing a few on the "
    "seats or windows. R is the reasoning that supports A.",
    ["A: true", "R: true", "Wing rivets = key species → R explains A"],
    C12_BD("biodiversity: importance of species diversity to the ecosystem"),
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "multi_statement",
    ms("Which of the following statements about the reasons for conserving biodiversity are correct?",
       ["Industrial products such as tannins, lubricants, dyes, resins and perfumes illustrate the narrowly "
        "utilitarian argument.",
        "Aesthetic pleasures, such as walking through thick woods or waking up to a bulbul's song, are among the "
        "intangible benefits of the broadly utilitarian argument.",
        "About 25,000 species of plants contribute to the traditional medicines used by native peoples around the "
        "world.",
        "Pollination by bees, birds and bats is the standard example of the ethical argument.",
        "According to the ethical argument, species that have no current economic value need not be conserved."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["a", "c", "e"], ["b", "c", "d", "e"]], "C"),
    "Why conserve biodiversity",
    "Narrowly utilitarian: direct economic benefits, such as food, firewood, fibre and industrial products (tannins, "
    "lubricants, dyes, resins, perfumes), and medicines; 25,000 plant species contribute to traditional medicines. "
    "Broadly utilitarian: ecosystem services such as oxygen production and pollination, and intangible aesthetic "
    "pleasures. Ethical: every species has an intrinsic value, even if it has no current economic value, and we have a "
    "moral duty to care for it.",
    ["(a), (b), (c): true", "(d): false, pollination is a broadly utilitarian service",
     "(e): false, the ethical argument values every species"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity"),
    why="Options A, B and D include (d) or (e).",
    seconds=50)

add(BDC, "Hotspots and Red Data Book", "Intermediate", "direct",
    "Biodiversity hotspots are regions with very high levels of species richness and a high degree of endemism. "
    "NCERT adds that they are also regions of:",
    P("Accelerated habitat loss", ["Low species richness", "Complete protection from human activity",
                                   "Very low rates of extinction"], "B"),
    "Biodiversity hotspots",
    "Hotspots are identified for very high species richness and high endemism, and NCERT notes that they are also "
    "regions of accelerated habitat loss. That is why strict protection of the hotspots could greatly reduce ongoing "
    "extinctions.",
    ["Hotspot: high richness + endemism + accelerated habitat loss"],
    C12_BD("biodiversity conservation: hotspots"),
    why="Hotspots have high, not low, species richness; they face accelerated habitat loss, so they are neither "
        "protected from human activity nor places of low extinction risk.",
    seconds=25)

add(BDC, "Patterns of biodiversity", "Intermediate", "match_list",
    ml(("symbol in log S = log C + Z log A", "meaning"),
       ["S", "A", "Z", "C"],
       ["Y-intercept", "Area", "Slope of the line (regression coefficient)", "Species richness"]),
    M({"A": "IV", "B": "II", "C": "III", "D": "I"},
      [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
       {"A": "I", "B": "II", "C": "III", "D": "IV"}], "D"),
    "Species–area equation",
    "On a logarithmic scale the species–area relationship is a straight line, log S = log C + Z log A, where S is "
    "species richness, A is area, Z is the slope of the line (regression coefficient) and C is the Y-intercept.",
    ["A-IV", "B-II", "C-III", "D-I"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    why="Option A swaps S and A; option B swaps Z and C; option C swaps S and C.",
    seconds=30)

add(BDC, "Patterns of biodiversity", "Advanced", "numerical",
    "For islands within one region, the species–area relationship follows log S = log C + Z log A with Z = 0.2. "
    "If island Q is 32 times larger in area than island P, how many times more species is island Q expected to have?",
    P("2 times", ["6.4 times", "32 times", "1.2 times"], "C"),
    "Using the species–area relationship",
    "log S = log C + Z log A means S = C·A^Z. So S_Q/S_P = (A_Q/A_P)^Z = 32^0.2. Since 32 = 2⁵, 32^0.2 = 2^(5 × 0.2) "
    "= 2¹ = 2.",
    ["S = C·A^Z", "S_Q/S_P = 32^0.2", "32 = 2⁵ → 2^(5 × 0.2) = 2"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    shortcut="Ratio of species = (ratio of areas)^Z.",
    why="6.4 multiplies the area ratio by Z instead of raising it to the power Z; 32 assumes species are directly "
        "proportional to area (Z = 1); 1.2 simply adds Z to 1.",
    seconds=60, verified_by=RECOMPUTED)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Which of the following statements about the loss and conservation of biodiversity are correct?",
       ["The 'Evil Quartet' consists of habitat loss and fragmentation, over-exploitation, alien species invasions and "
        "pollution.",
        "When alien species are introduced, some of them turn invasive and cause the decline or extinction of "
        "indigenous species.",
        "Ex situ conservation protects the whole ecosystem in which a threatened species lives.",
        "Cryopreservation of gametes, in vitro fertilisation and tissue culture propagation help to conserve "
        "threatened species ex situ.",
        "Biosphere reserves are a means of ex situ conservation."]),
    MS(["b", "d"], [["a", "b", "d"], ["b", "c", "d"], ["c", "e"]], "A"),
    "Causes of loss and means of conservation",
    "The Evil Quartet is habitat loss and fragmentation, over-exploitation, alien species invasions and "
    "co-extinctions (not pollution). Some introduced alien species turn invasive and cause decline or extinction of "
    "native species (e.g. Nile perch). Ex situ conservation takes threatened species out of their habitat; it does not "
    "protect whole ecosystems. It now includes cryopreservation of gametes, in vitro fertilisation and tissue culture. "
    "Biosphere reserves are in situ.",
    ["(b), (d): true", "(a): false, the fourth cause is co-extinctions", "(c), (e): false"],
    C12_BD("loss of biodiversity: causes; biodiversity conservation"),
    why="Option B adds (a), option C adds (c), and option D contains only false statements.",
    seconds=55)

add(BDC, "Importance and loss", "Advanced", "statement_pair",
    sp("Animals with migratory habits are the least affected when large habitats are broken up into small fragments.",
       "When 'need' turns to 'greed', it leads to over-exploitation of natural resources."),
    SP("D"),
    "Habitat fragmentation and over-exploitation",
    "NCERT: when large habitats are broken up into fragments, mammals and birds requiring large territories and "
    "certain animals with migratory habits are badly affected, leading to population declines; Statement I is false. "
    "Humans have always depended on nature, but when 'need' turns to 'greed', it leads to over-exploitation of natural "
    "resources; Statement II is true.",
    ["Statement I: false, migratory animals are badly affected", "Statement II: true"],
    C12_BD("loss of biodiversity: causes"),
    seconds=35)

add(BDC, "In situ and ex situ conservation", "Advanced", "assertion_reason",
    ar("Ex situ conservation protects threatened species within their natural habitats.",
       "In ex situ conservation, threatened animals and plants are taken out of their natural habitat and placed in "
       "special settings where they can be protected and given special care."),
    AR("D"),
    "Meaning of ex situ conservation",
    "Ex situ ('off site') conservation removes threatened species from their natural habitat to special settings "
    "(zoos, botanical gardens, seed banks, cryopreservation) where they are protected and cared for, so R is true. "
    "Protection within natural habitats is in situ conservation, so A is false.",
    ["A: false, that is in situ conservation", "R: true"],
    C12_BD("biodiversity conservation: ex situ conservation"),
    seconds=30)


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
    assert [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]] == pkg["question_ids"]
    assert len(QUESTIONS) == pkg["count"] == 127
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_004", "created_at": TODAY,
           "notes": "BATCH_004 package BOT_004_p2: 127 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 to "
                    "BATCH_003 were avoided. Numerical and other computable answers re-derived by "
                    "tools/batch_004/BOT_004_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()
