"""Builder for BATCH_003, package BOT_003_p2 (Botany, NEET_BOT_000623..NEET_BOT_000750, 128 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Facts already tested in BATCH_000, BATCH_001 and BATCH_002 on these topics were
avoided. Numerical answers are re-derived below; the file is written only if every assert, the plan quota and the
format mix pass.

    cd docs/neet-bank && python tools/batch_003/BOT_003_p2.py
"""

import json
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
PACKAGE = "BOT_003_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_003_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_003_BOT_p2.json"
FIRST_ID = 623

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

# arithmetic growth Lt = L0 + rt: L0 = 3 cm, r = 0.4 cm per day, t = 15 days
L0, r_a, t_a = F(3), F(4, 10), 15
assert L0 + r_a * t_a == 9                      # correct
assert r_a * t_a == 6 and L0 * r_a * t_a == 18  # distractors: forgot L0; multiplied L0 by rt

# one cell, five rounds of division: geometric (both daughters divide) vs arithmetic (one daughter divides)
cells_geo, cells_ari = 1, 1
for _ in range(5):
    cells_geo *= 2
    cells_ari += 1
assert (cells_geo, cells_ari) == (32, 6)
assert 2 * 5 == 10 and 2 ** 6 == 64 and cells_ari + 1 == 7   # distractors

add(PGD, "Plant growth regulators", "Basic", "direct",
    "The term 'auxin' comes from the Greek word 'auxein', meaning 'to grow'. According to NCERT, auxin was first "
    "isolated from:",
    P("Human urine", ["Autoclaved herring sperm DNA", "Ripened oranges",
                      "Rice seedlings infected with the fungus Gibberella fujikuroi"], "B"),
    "Discovery of auxins",
    "NCERT states that auxins (from the Greek 'auxein': to grow) were first isolated from human urine. The term "
    "auxin is applied to indole-3-acetic acid (IAA) and to other natural and synthetic compounds having certain "
    "growth-regulating properties.",
    ["Auxin: 'auxein' = to grow", "First isolated from human urine"],
    C11_PGD("plant growth regulators: auxins"),
    why="Autoclaved herring sperm DNA gave kinetin (a cytokinin). Ripened oranges released a volatile substance later "
        "identified as ethylene. Gibberella fujikuroi, the fungus causing 'bakanae' of rice, is the source of "
        "gibberellic acid.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "The search for natural substances with cytokinin-like activity led to the isolation of zeatin from corn kernels "
    "and coconut milk. Zeatin is therefore:",
    P("A naturally occurring cytokinin",
      ["A naturally occurring auxin", "A gibberellin produced by a fungus", "A synthetic derivative of carotenoids"],
      "C"),
    "Natural cytokinins",
    "Kinetin, the first cytokinin discovered (from autoclaved herring sperm DNA), does not occur naturally in plants. "
    "The search for natural substances with cytokinin-like activities led to the isolation of zeatin from corn "
    "kernels and coconut milk.",
    ["Kinetin: not natural in plants", "Zeatin: natural cytokinin from corn kernels and coconut milk"],
    C11_PGD("plant growth regulators: cytokinins"),
    why="Zeatin is an adenine-type cytokinin, not an auxin or a gibberellin. Carotenoid derivatives (ABA) are growth "
        "inhibitors, and zeatin is natural, not synthetic.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "statement_pair",
    sp("In the mid-1960s, three different inhibitors, inhibitor-B, abscission II and dormin, were reported "
       "independently; they were later proved to be chemically identical and named abscisic acid.",
       "Abscisic acid is a derivative of adenine."),
    SP("C"),
    "Discovery and chemical nature of abscisic acid",
    "During the mid-sixties three independent researchers purified and characterised inhibitor-B, abscission II and "
    "dormin. All three were later found to be chemically identical and the substance was named abscisic acid (ABA). "
    "Chemically, ABA is a derivative of carotenoids; kinetin and zeatin (cytokinins) are adenine derivatives.",
    ["Statement I: true", "Statement II: false, ABA is a carotenoid derivative"],
    C11_PGD("plant growth regulators: abscisic acid"),
    seconds=30)

add(PGD, "Growth rate", "Intermediate", "numerical",
    "A root elongates at a constant rate and shows arithmetic growth, described by Lₜ = L₀ + rt. Its length is "
    "3 cm at the start and it elongates by 0.4 cm per day. What is its length after 15 days, and what is the shape "
    "of the curve when length is plotted against time?",
    P("9 cm; a straight line", ["9 cm; a sigmoid curve", "6 cm; a straight line", "18 cm; a sigmoid curve"], "A"),
    "Arithmetic growth",
    "In arithmetic growth only one daughter cell of each mitotic division keeps dividing, so the length increases "
    "by a constant amount per unit time. Lₜ = L₀ + rt = 3 + 0.4 × 15 = 3 + 6 = 9 cm. A plot of length against time "
    "gives a linear curve (a straight line); the sigmoid curve is typical of geometric growth.",
    ["rt = 0.4 × 15 = 6 cm", "Lₜ = 3 + 6 = 9 cm", "Arithmetic growth → linear (straight-line) curve"],
    C11_PGD("growth rates: arithmetic growth"),
    why="Option B gives the curve of geometric growth. Option C forgets to add L₀. Option D multiplies L₀ by rt and "
        "also gives the wrong curve.",
    seconds=50, verified_by=RECOMPUTED)

add(PGD, "Growth rate", "Intermediate", "match_list",
    ml(("plant part", "parameter by which NCERT expresses its growth"),
       ["Maize root apical meristem", "Cells of a watermelon", "Pollen tube", "Dorsiventral leaf"],
       ["Increase in length", "Increase in surface area", "Increase in cell number", "Increase in cell size"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "D"),
    "Measurement of growth",
    "Growth can be measured by increase in fresh weight, dry weight, length, area, volume or cell number. A maize "
    "root apical meristem gives rise to more than 17,500 new cells per hour (increase in cell number), while "
    "watermelon cells may increase in size up to 3,50,000 times (increase in cell size). Growth of a pollen tube is "
    "measured as its length, and growth of a dorsiventral leaf as increase in surface area.",
    ["Maize root apex → cell number (A-III)", "Watermelon → cell size (B-IV)", "Pollen tube → length (C-I)",
     "Dorsiventral leaf → surface area (D-II)"],
    C11_PGD("growth is measurable"),
    why="The wrong codes swap cell number with cell size, or length with surface area.",
    seconds=45)

add(PGD, "Plant growth regulators", "Intermediate", "statement_pair",
    sp("Ethylene could fit into either the growth-promoter or the growth-inhibitor group of plant growth regulators, "
       "but it is largely an inhibitor of growth activities.",
       "The rise in the rate of respiration that ethylene brings about during the ripening of fruits is called the "
       "respiratory climactic."),
    SP("A"),
    "Ethylene",
    "PGRs are broadly grouped as growth promoters (auxins, gibberellins, cytokinins) and growth inhibitors (ABA). "
    "The gaseous PGR ethylene could fit either group, but it is largely an inhibitor of growth activities. Ethylene "
    "promotes fruit ripening and enhances the respiration rate during ripening; this rise is the respiratory "
    "climactic.",
    ["Statement I: true", "Statement II: true"],
    C11_PGD("plant growth regulators: ethylene"),
    seconds=35)

add(PGD, "Differentiation and redifferentiation", "Intermediate", "direct",
    "In a woody dicot stem, cork cambium arises from fully differentiated parenchyma cells. The cork cells that the "
    "cork cambium then cuts off lose the capacity to divide and mature to perform a specific function. These cork "
    "cells are best described as products of:",
    P("Redifferentiation", ["Dedifferentiation", "Arithmetic growth of the shoot apex", "Apical dominance"], "B"),
    "Dedifferentiation and redifferentiation",
    "Living differentiated cells that regain the capacity to divide are said to dedifferentiate; formation of cork "
    "cambium from parenchyma is an example. Such meristems produce cells that once again lose the capacity to "
    "divide but mature to perform specific functions, i.e. they are redifferentiated. Cork cells cut off by the "
    "cork cambium are therefore products of redifferentiation.",
    ["Parenchyma → cork cambium: dedifferentiation", "Cork cambium → cork cells that stop dividing and mature: "
     "redifferentiation"],
    C11_PGD("differentiation, dedifferentiation and redifferentiation"),
    why="Dedifferentiation describes the formation of the cork cambium itself, not of the cork cells. Arithmetic "
        "growth and apical dominance are unrelated to secondary tissues formed by the cork cambium.",
    seconds=40)

add(PGD, "Plant growth regulators", "Intermediate", "multi_statement",
    ms("Which of the following statements about cytokinins are correct?",
       ["They help to produce new leaves, chloroplasts in leaves, lateral shoot growth and adventitious shoot "
        "formation.",
        "They help to overcome apical dominance.",
        "They promote nutrient mobilisation, which helps in the delay of leaf senescence.",
        "Chemically, they are derivatives of carotenoids.",
        "They have specific effects on cytokinesis."]),
    P("(a), (b), (c) and (e) only",
      ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"], "D"),
    "Physiological effects of cytokinins",
    "Cytokinins have specific effects on cytokinesis. They help to produce new leaves, chloroplasts in leaves, "
    "lateral shoot growth and adventitious shoot formation; they help to overcome apical dominance; and they "
    "promote nutrient mobilisation, which helps in the delay of leaf senescence. Kinetin and zeatin are adenine "
    "derivatives; carotenoid derivatives are ABA.",
    ["(a) True", "(b) True", "(c) True", "(d) False: cytokinins are adenine derivatives", "(e) True"],
    C11_PGD("plant growth regulators: cytokinins"),
    why="Option A misses the true statement (e). Options B and C include the false statement (d), and option C also "
        "leaves out (b).",
    seconds=50)

add(PGD, "Growth rate", "Advanced", "numerical",
    "A single meristematic cell undergoes five successive rounds of mitosis. Compare two patterns: (i) geometric "
    "growth, in which both progeny cells of every division continue to divide; (ii) arithmetic growth, in which "
    "after every division only one daughter cell continues to divide while the other differentiates and matures. "
    "How many cells are present in all after the five rounds in (i) and (ii), respectively?",
    P("32 and 6", ["32 and 10", "64 and 7", "10 and 6"], "C"),
    "Geometric versus arithmetic growth",
    "In geometric growth every cell divides in each round, so the number doubles: 2⁵ = 32 cells. In arithmetic "
    "growth only one cell is dividing at any time; each division adds just one new (differentiating) cell, so after "
    "five divisions there are 1 + 5 = 6 cells (five differentiated cells and one cell that still divides).",
    ["(i) 1 → 2 → 4 → 8 → 16 → 32", "(ii) 1 → 2 → 3 → 4 → 5 → 6", "Answer: 32 and 6"],
    C11_PGD("growth rates: arithmetic and geometric growth"),
    shortcut="Geometric: 2ⁿ cells; arithmetic: n + 1 cells after n divisions.",
    why="'32 and 10' adds two cells per arithmetic division. '64 and 7' counts six rounds instead of five. "
        "'10 and 6' treats geometric growth as adding two cells per round.",
    seconds=60, verified_by=RECOMPUTED)

add(PGD, "Plant growth regulators", "Advanced", "multi_statement",
    ms("Which of the following statements about plant growth regulators are correct?",
       ["F. Skoog observed that callus from internodal segments of tobacco stems proliferated only if, in addition "
        "to auxins, the nutrient medium was supplemented with extracts of vascular tissues, yeast extract, coconut "
        "milk or DNA.",
        "Kinetin occurs naturally in plants in large amounts.",
        "Abscisic acid stimulates the closure of stomata.",
        "Skoog and Miller identified and crystallised the cytokinesis-promoting active substance and named it auxin.",
        "In most situations, abscisic acid acts as an antagonist to gibberellins."]),
    P("(a), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(c), (d) and (e) only", "(a), (b) and (d) only"], "B"),
    "Cytokinin discovery and ABA functions",
    "Skoog found that tobacco internodal callus proliferated only when, besides auxin, the medium had vascular "
    "tissue extract, yeast extract, coconut milk or DNA. Skoog and Miller later identified and crystallised this "
    "cytokinesis-promoting substance and named it kinetin, which does not occur naturally in plants. ABA "
    "stimulates stomatal closure and, in most situations, acts as an antagonist to GAs.",
    ["(a) True", "(b) False: kinetin does not occur naturally in plants", "(c) True",
     "(d) False: the substance was named kinetin", "(e) True"],
    C11_PGD("plant growth regulators: cytokinins and abscisic acid"),
    why="Every other option contains (b) or (d), or leaves out a true statement.",
    seconds=60)

add(PGD, "Plant growth regulators", "Advanced", "assertion_reason",
    ar("Ethylene is used to initiate flowering and to synchronise fruit-set in pineapples, and it also induces "
       "flowering in mango.",
       "Ethylene is synthesised in large amounts by tissues undergoing senescence and by ripening fruits."),
    AR("B"),
    "Ethylene: sources and applications",
    "Both statements are NCERT facts. A is an application of ethylene (flowering and synchronised fruit-set in "
    "pineapple, flowering in mango). R tells where ethylene is synthesised in large amounts. The site of its "
    "synthesis does not explain why applied ethylene initiates flowering, so R is not the explanation of A.",
    ["A: true (applications of ethylene)", "R: true (sources of ethylene)",
     "R describes where ethylene is made, not why it promotes flowering → B"],
    C11_PGD("plant growth regulators: ethylene"),
    seconds=40)


# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

# meioses needed for 100 seeds: one MMC per ovule (one functional megaspore), one PMC gives four pollen grains
seeds = 100
mmc_meioses = seeds                 # each ovule needs its own megaspore mother cell
pmc_meioses = F(seeds, 4)           # each seed needs one pollen grain; one meiosis gives four
assert mmc_meioses + pmc_meioses == 125
assert seeds + F(2 * seeds, 4) == 150 and seeds * 2 == 200    # distractors: two pollen per seed; one meiosis per pollen

# endosperm: two polar nuclei (maternal) + one male gamete (paternal)
maternal_sets, paternal_sets = 2, 1
assert F(maternal_sets, paternal_sets) == 2

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "Pollen grains are generally spherical. Their diameter usually measures about:",
    P("25–50 micrometres", ["2.5–5 micrometres", "250–500 micrometres", "2.5–5 millimetres"], "C"),
    "Size of pollen grains",
    "Pollen grains represent the male gametophytes. NCERT describes them as generally spherical, measuring about "
    "25–50 micrometres in diameter.",
    ["Pollen grains: generally spherical", "Diameter about 25–50 µm"],
    C12_SR("pre-fertilisation: the pollen grain"),
    why="The other options are ten times too small, ten times too large, or in millimetres instead of micrometres.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "The inner wall of a pollen grain, the intine, is a thin and continuous layer made up of:",
    P("Cellulose and pectin", ["Sporopollenin", "Lignin and suberin", "Chitin"], "B"),
    "Pollen wall layers",
    "A pollen grain has a two-layered wall. The hard outer exine is made of sporopollenin. The inner intine is a "
    "thin and continuous layer made up of cellulose and pectin.",
    ["Exine: sporopollenin", "Intine: cellulose and pectin"],
    C12_SR("pre-fertilisation: the pollen grain"),
    why="Sporopollenin forms the exine. Lignin, suberin and chitin are not components of the intine.",
    seconds=20)

add(SRFP, "Pollination", "Basic", "direct",
    "The 'tassels' seen on a corn cob are:",
    P("The stigma and style, which wave in the wind to trap pollen grains",
      ["The anthers, which release pollen grains into the wind", "Bracts that protect the developing grains",
       "Hairs that attract insect pollinators"], "A"),
    "Wind pollination in maize",
    "Wind pollination is quite common in grasses. Wind-pollinated flowers have large, often feathery stigmas to "
    "trap air-borne pollen. NCERT points out that the tassels of the corn cob are nothing but the stigma and style, "
    "which wave in the wind to trap pollen grains.",
    ["Corn is wind-pollinated", "Tassels on the cob = stigma + style that trap pollen"],
    C12_SR("pollination: agents of pollination"),
    why="The tassels belong to the female part of the flower; they neither release pollen nor serve to attract "
        "insects, and they are not protective bracts.",
    seconds=20)

add(SRFP, "Pollination", "Basic", "direct",
    "Not all aquatic plants use water for pollination. In aquatic plants such as water hyacinth and water lily, the "
    "flowers emerge above the level of water and are pollinated by:",
    P("Insects or wind", ["Water currents", "Cleistogamy only", "Bats only"], "B"),
    "Pollination in aquatic plants",
    "Pollination by water is limited to about 30 genera, mostly monocots, such as Vallisneria, Hydrilla and Zostera. "
    "NCERT notes that not all aquatic plants use water: in a majority of aquatic plants such as water hyacinth and "
    "water lily, the flowers emerge above the water level and are pollinated by insects or wind, as in most land "
    "plants.",
    ["Water pollination: Vallisneria, Hydrilla, Zostera", "Water hyacinth, water lily: flowers above water → "
     "insects or wind"],
    C12_SR("pollination: agents of pollination"),
    why="Their flowers emerge above the water, so water currents do not carry their pollen. NCERT does not describe "
        "them as cleistogamous or bat-pollinated.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "direct",
    "During the development of a dicot embryo from the zygote, the correct sequence of stages is:",
    P("Proembryo → globular embryo → heart-shaped embryo → mature embryo",
      ["Globular embryo → proembryo → heart-shaped embryo → mature embryo",
       "Proembryo → heart-shaped embryo → globular embryo → mature embryo",
       "Heart-shaped embryo → globular embryo → proembryo → mature embryo"], "D"),
    "Embryogeny in dicots",
    "The embryo develops at the micropylar end of the embryo sac where the zygote is situated. The zygote gives rise "
    "to the proembryo and subsequently to the globular, heart-shaped and mature embryo.",
    ["Zygote → proembryo", "→ globular → heart-shaped → mature embryo"],
    C12_SR("post-fertilisation: embryo"),
    why="The other options place the globular and heart-shaped stages, or the proembryo, in the wrong order.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "statement_pair",
    sp("As a seed matures, its water content is reduced and it becomes relatively dry, with about 10–15 per cent "
       "moisture by mass.",
       "The micropyle remains as a small pore in the seed coat, which facilitates the entry of oxygen and water into "
       "the seed during germination."),
    SP("A"),
    "Seed maturation",
    "Integuments of the ovule harden into tough protective seed coats. The micropyle remains as a small pore in the "
    "seed coat and allows entry of oxygen and water during germination. As the seed matures, its water content is "
    "reduced and seeds become relatively dry (10–15 per cent moisture by mass); the general metabolic activity of "
    "the embryo slows down.",
    ["Statement I: true", "Statement II: true"],
    C12_SR("post-fertilisation: seed"),
    seconds=30)

add(SRFP, "Pollination", "Intermediate", "multi_statement",
    ms("Which of the following statements about animal pollination are correct?",
       ["Some primates (lemurs), arboreal rodents and reptiles such as the gecko lizard and garden lizard have been "
        "reported as pollinators in some species.",
        "Flowers pollinated by flies and beetles secrete foul odours to attract these animals.",
        "Many insects consume pollen or nectar without bringing about pollination; they are called pollen or nectar "
        "robbers.",
        "Nectar is the only floral reward; pollen grains are never a reward for animal visitors.",
        "Animals are attracted to flowers only by their colour and never by fragrance."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "C"),
    "Pollination by animals",
    "Besides insects, larger animals such as lemurs, arboreal rodents and reptiles (gecko and garden lizard) are "
    "reported as pollinators. Animals are attracted to flowers by colour and/or fragrance; flowers pollinated by "
    "flies and beetles secrete foul odours. Nectar and pollen grains are the usual floral rewards. Many insects "
    "consume pollen or nectar without pollinating the flower; they are pollen or nectar robbers.",
    ["(a) True", "(b) True", "(c) True", "(d) False: nectar and pollen are the usual rewards",
     "(e) False: colour and/or fragrance attract animals"],
    C12_SR("pollination: agents of pollination"),
    why="Options A, B and D include (d) or (e), or leave out a true statement.",
    seconds=50)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "statement_pair",
    sp("Following compatible pollination, the pollen grain germinates on the stigma to produce a pollen tube through "
       "one of the germ pores.",
       "In some members of Rosaceae, Leguminosae and Solanaceae, pollen grains lose their viability within "
       "30 minutes of their release."),
    SP("C"),
    "Pollen germination and viability",
    "After compatible pollination, the pollen grain germinates on the stigma and the pollen tube emerges through one "
    "of the germ pores; the contents of the pollen grain move into the tube. Pollen viability varies: in rice and "
    "wheat pollen loses viability within 30 minutes of release, whereas in some members of Rosaceae, Leguminosae "
    "and Solanaceae it remains viable for months.",
    ["Statement I: true", "Statement II: false, these families keep pollen viable for months"],
    C12_SR("pre-fertilisation: pollen viability; pollen-pistil interaction"),
    seconds=35)

add(SRFP, "Double fertilisation", "Intermediate", "direct",
    "After reaching the ovary, the pollen tube enters the ovule through the micropyle. It then enters one of the "
    "synergids through:",
    P("The filiform apparatus", ["The chalaza", "The antipodal cells", "The hilum"], "B"),
    "Entry of the pollen tube into the embryo sac",
    "The pollen tube enters the ovule through the micropyle and then enters one of the synergids through the "
    "filiform apparatus. The filiform apparatus, present at the micropylar part of the synergids, guides the entry "
    "of the pollen tube. The tube then releases the two male gametes into the cytoplasm of the synergid.",
    ["Pollen tube → micropyle → filiform apparatus → synergid"],
    C12_SR("pollen-pistil interaction; double fertilisation"),
    why="The chalaza and antipodal cells are at the opposite (chalazal) end; the hilum is where the ovule joins the "
        "funicle.",
    seconds=30)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("Wind-pollinated flowers often have well-exposed stamens and a large, often feathery stigma.",
       "Wind-pollinated flowers produce pollen grains that are heavy and sticky."),
    AR("C"),
    "Adaptations for wind pollination",
    "Wind pollination requires pollen grains that are light and non-sticky, so that they can be carried by wind "
    "currents. Such flowers have well-exposed stamens (so that pollen is easily dispersed into the wind) and large, "
    "often feathery stigmas (to trap air-borne pollen). A is true; R is false.",
    ["A: true", "R: false, the pollen is light and non-sticky"],
    C12_SR("pollination: agents of pollination"),
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "match_list",
    ml(("plant", "feature described in NCERT"),
       ["Papaver", "Michelia", "Castor", "Mustard"],
       ["Seed that retains a part of the endosperm (albuminous)", "Fruit with a dry pericarp",
        "Multicarpellary, apocarpous pistil", "Multicarpellary, syncarpous pistil"]),
    M({"A": "IV", "B": "III", "C": "I", "D": "II"},
      [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Pistil types, seeds and fruits",
    "When a pistil is multicarpellary, the carpels may be fused (syncarpous), as in Papaver, or free (apocarpous), "
    "as in Michelia. Seeds such as those of wheat, maize, barley and castor retain a part of the endosperm "
    "(albuminous). The pericarp may be fleshy (guava, orange, mango) or dry, as in groundnut and mustard.",
    ["Papaver → syncarpous (A-IV)", "Michelia → apocarpous (B-III)", "Castor → albuminous (C-I)",
     "Mustard → dry pericarp (D-II)"],
    C12_SR("the pistil; post-fertilisation: seed and fruit"),
    why="The wrong codes swap Papaver with Michelia, or castor with mustard.",
    seconds=45)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "multi_statement",
    ms("Which of the following statements about the anther and microsporogenesis are correct?",
       ["Each cell of the sporogenous tissue of a young anther is a potential pollen (microspore) mother cell.",
        "Microsporogenesis is the formation of microspores from a pollen mother cell through mitosis.",
        "The microspores, as they are formed, are arranged in a cluster of four cells, the microspore tetrad.",
        "The endothecium and middle layers nourish the developing pollen grains.",
        "As the anthers mature and dehydrate, the microspores dissociate from each other and develop into pollen "
        "grains."]),
    P("(a), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"], "A"),
    "Microsporogenesis",
    "In a young anther, a group of compactly arranged homogenous cells forms the sporogenous tissue; each of its "
    "cells is a potential pollen mother cell. Formation of microspores from a PMC through meiosis is "
    "microsporogenesis. The microspores form a tetrad, and as the anther matures and dehydrates they separate and "
    "develop into pollen grains. The outer wall layers (epidermis, endothecium, middle layers) protect and help in "
    "dehiscence; nourishment is the role of the tapetum.",
    ["(a) True", "(b) False: meiosis, not mitosis", "(c) True",
     "(d) False: these layers protect and help in dehiscence; the tapetum nourishes", "(e) True"],
    C12_SR("pre-fertilisation: microsporangium and microsporogenesis"),
    why="Options B, C and D include (b) or (d).",
    seconds=50)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "assertion_reason",
    ar("Pollen tablets are used as food supplements, and pollen consumption has been claimed to increase the "
       "performance of athletes and race horses.",
       "Pollen grains are rich in nutrients."),
    AR("A"),
    "Pollen as a food supplement",
    "NCERT notes that pollen grains are rich in nutrients. This is why pollen tablets are used as food supplements, "
    "pollen products are sold as tablets and syrups in western countries, and pollen consumption has been claimed "
    "to increase the performance of athletes and race horses.",
    ["A: true", "R: true", "The nutrient content is the reason pollen is used as a supplement → R explains A"],
    C12_SR("pre-fertilisation: the pollen grain"),
    seconds=30)

add(SRFP, "Endosperm and embryo", "Advanced", "direct",
    "In the triploid endosperm of an angiosperm seed, what is the ratio of chromosome sets contributed by the female "
    "parent to those contributed by the male parent?",
    P("2 : 1", ["1 : 2", "1 : 1", "3 : 1"], "B"),
    "Origin of the primary endosperm nucleus",
    "In triple fusion, one male gamete (from the pollen, i.e. the male parent) fuses with the two polar nuclei of "
    "the central cell (from the embryo sac, i.e. the female parent). The primary endosperm nucleus therefore carries "
    "two maternal sets and one paternal set of chromosomes; the endosperm develops from it.",
    ["Two polar nuclei (n + n) → maternal", "One male gamete (n) → paternal", "Ratio 2 : 1"],
    C12_SR("double fertilisation; post-fertilisation: endosperm"),
    why="1 : 2 reverses the contributions. 1 : 1 is the ratio in the zygote, which forms by syngamy of one egg and "
        "one male gamete. 3 : 1 treats all three sets as coming from different sources.",
    seconds=45, verified_by=RECOMPUTED)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "numerical",
    "In a flowering plant, each ovule has one megaspore mother cell that gives a single functional megaspore, each "
    "pollen mother cell gives four pollen grains, and each seed results from the fertilisation of one ovule by the "
    "gametes of one pollen grain. What is the minimum number of meiotic divisions needed to produce 100 seeds?",
    P("125", ["100", "150", "200"], "D"),
    "Meiosis in megasporogenesis and microsporogenesis",
    "Each seed develops from one ovule, whose megaspore mother cell must undergo one meiosis: 100 meioses for 100 "
    "ovules. Each seed also needs one pollen grain; one pollen mother cell gives four pollen grains through one "
    "meiosis, so 100 pollen grains need 100 ÷ 4 = 25 meioses. Total = 100 + 25 = 125. The two male gametes of a "
    "pollen grain form by mitosis, and one pollen grain serves both syngamy and triple fusion.",
    ["Female side: 100 MMC meioses", "Male side: 100 pollen ÷ 4 = 25 PMC meioses", "Total = 125"],
    C12_SR("pre-fertilisation: microsporogenesis and megasporogenesis"),
    shortcut="Meioses = n + n/4 for n seeds.",
    why="100 counts only the female side. 150 assumes two pollen grains per seed (one for each fusion). 200 assumes "
        "one meiosis per pollen grain.",
    seconds=75, verified_by=RECOMPUTED)

add(SRFP, "Pollination", "Advanced", "assertion_reason",
    ar("In a normal flower that opens and exposes its anthers and stigma, complete autogamy is rather rare.",
       "Autogamy in such flowers requires synchrony between pollen release and stigma receptivity, and the anthers "
       "and stigma must lie close to each other."),
    AR("A"),
    "Autogamy in chasmogamous flowers",
    "NCERT states that in a normal (chasmogamous) flower, complete autogamy is rather rare, because autogamy in such "
    "flowers requires synchrony in pollen release and stigma receptivity, and the anthers and stigma should lie "
    "close to each other so that self-pollination can occur. These two conditions are seldom met together, which "
    "is why complete autogamy is rare. R explains A.",
    ["A: true", "R: true", "The demanding conditions in R are why complete autogamy is rare → A"],
    C12_SR("pollination: kinds of pollination"),
    seconds=45)

add(SRFP, "Endosperm and embryo", "Advanced", "multi_statement",
    ms("Which of the following statements about endosperm and embryo development are correct?",
       ["In the most common type of endosperm development, the primary endosperm nucleus undergoes successive "
        "nuclear divisions to give rise to free nuclei.",
        "In such endosperm, cell wall formation occurs subsequently and the endosperm becomes cellular.",
        "The number of free nuclei formed before cellularisation is always exactly eight.",
        "The embryo develops at the chalazal end of the embryo sac.",
        "As the seed matures, the embryo may enter a state of inactivity called dormancy."]),
    P("(a), (b) and (e) only",
      ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"], "C"),
    "Endosperm and embryo development",
    "The PEN usually divides repeatedly to give free nuclei (free-nuclear endosperm); cell walls form later and the "
    "endosperm becomes cellular. The number of free nuclei formed before cellularisation varies greatly. The "
    "embryo develops at the micropylar end of the embryo sac, where the zygote lies. As the seed matures, metabolic "
    "activity slows and the embryo may enter dormancy.",
    ["(a) True", "(b) True", "(c) False: the number varies greatly", "(d) False: micropylar end", "(e) True"],
    C12_SR("post-fertilisation: endosperm, embryo and seed"),
    why="Options A, B and D include (c) or (d).",
    seconds=55)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "Which one of the following is NOT an advantage of seeds to angiosperms?",
    P("Being products of asexual reproduction, seeds preserve the exact genotype of the parent",
      ["Seeds have better adaptive strategies for dispersal to new habitats",
       "Their food reserves nourish young seedlings until they can photosynthesise on their own",
       "The hard seed coat protects the young embryo"], "D"),
    "Advantages of seeds",
    "NCERT lists the advantages of seeds: seed formation is more dependable as pollination and fertilisation are "
    "independent of water; seeds have better adaptive strategies for dispersal; food reserves nourish seedlings "
    "until they photosynthesise; the hard seed coat protects the embryo; and, being products of sexual "
    "reproduction, seeds generate new genetic combinations leading to variations.",
    ["Seeds arise from sexual reproduction", "They generate variation; they do not preserve the parent's exact "
     "genotype"],
    C12_SR("post-fertilisation: seed"),
    why="Options A, B and C are advantages listed by NCERT.",
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "assertion_reason",
    ar("Pollen-pistil interaction is a passive process that does not involve any recognition by the pistil.",
       "Knowledge of pollen-pistil interaction can help a plant breeder manipulate it, even in incompatible "
       "pollinations, to get desired hybrids."),
    AR("D"),
    "Pollen-pistil interaction",
    "The pistil can recognise whether a pollen grain is compatible or incompatible; it accepts compatible pollen and "
    "rejects incompatible pollen by preventing pollen germination on the stigma or pollen tube growth in the style. "
    "All these events constitute pollen-pistil interaction, a dynamic process involving pollen recognition followed "
    "by promotion or inhibition of the pollen. Understanding it helps breeders manipulate even incompatible "
    "pollinations to obtain desired hybrids. A is false; R is true.",
    ["A: false, it is a dynamic process with recognition by the pistil", "R: true"],
    C12_SR("pre-fertilisation: pollen-pistil interaction"),
    seconds=40)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "multi_statement",
    ms("Which of the following statements about the ovule and megasporogenesis are correct?",
       ["The megaspore mother cell is a large cell containing dense cytoplasm and a prominent nucleus.",
        "The megaspore mother cell undergoes meiotic division, resulting in the production of four megaspores.",
        "Each ovule generally has a single embryo sac formed from a megaspore.",
        "Megasporogenesis is the development of the embryo sac from the functional megaspore by mitosis.",
        "The cells of the nucellus have very little reserve food."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "A"),
    "The megasporangium and megasporogenesis",
    "Within the integuments lies the nucellus, whose cells have abundant reserve food. The MMC is a large cell with "
    "dense cytoplasm and a prominent nucleus; it undergoes meiosis to form four megaspores. Megasporogenesis is the "
    "formation of megaspores from the MMC. Development of the embryo sac (female gametophyte) from the functional "
    "megaspore by mitotic divisions is a later step. Each ovule generally has a single embryo sac.",
    ["(a) True", "(b) True", "(c) True", "(d) False: megasporogenesis = formation of megaspores from the MMC",
     "(e) False: nucellar cells have abundant reserve food"],
    C12_SR("pre-fertilisation: the megasporangium (ovule)"),
    why="Options B, C and D include (d) or (e).",
    seconds=50)


# ================================================================ Principles of Inheritance and Variation (7 / 10 / 7)
C12_PI = lambda s: ref(12, PIV, s)

# gametes of AaBbCCDd with independent assortment
gametes = set(product("Aa", "Bb", "C", "Dd"))
assert len(gametes) == 8
assert 2 ** 4 == 16 and 2 ** 2 == 4                       # distractors: CC counted as heterozygous; only 2 genes

# RrYy x RrYy, 1600 progeny: round (R_) and green (yy)
f2 = Counter()
for g1, g2 in product(product("Rr", "Yy"), repeat=2):
    shape = "round" if "R" in g1[0] + g2[0] else "wrinkled"
    colour = "yellow" if "Y" in g1[1] + g2[1] else "green"
    f2[(shape, colour)] += 1
assert F(f2[("round", "green")], 16) * 1600 == 300
assert F(f2[("round", "yellow")], 16) * 1600 == 900 and F(f2[("wrinkled", "green")], 16) * 1600 == 100
assert F(3, 8) * 1600 == 600

# two carriers (Aa x Aa): probability that a child of normal phenotype is a carrier
kids = Counter("".join(sorted(a + b)) for a, b in product("Aa", "Aa"))
normal = kids["AA"] + kids["Aa"]
assert F(kids["Aa"], normal) == F(2, 3)
assert F(kids["Aa"], 4) == F(1, 2) and F(kids["aa"], 4) == F(1, 4)    # distractors

# gene order from recombination frequencies: P-Q 8 %, Q-R 15 %, P-R 7 %  -> P lies between Q and R
d = {("P", "Q"): 8, ("Q", "R"): 15, ("P", "R"): 7}
assert d[("P", "Q")] + d[("P", "R")] == d[("Q", "R")]     # the two short distances add up to the long one
assert max(d, key=d.get) == ("Q", "R")                    # Q and R are the outer genes

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "For his hybridisation experiments on garden peas, Mendel selected true-breeding pea plant varieties as pairs "
    "that were similar except for one character with contrasting traits. He used:",
    P("14 true-breeding varieties, i.e. 7 pairs, each pair differing in one character",
      ["7 true-breeding varieties, together differing in 14 characters",
       "14 true-breeding varieties, each differing from all others in 14 characters",
       "21 true-breeding varieties, forming 7 groups of three"], "A"),
    "Mendel's choice of material",
    "Mendel selected 14 true-breeding pea plant varieties as pairs that were similar except for one character with "
    "contrasting traits, for example smooth or wrinkled seeds, yellow or green seeds, tall or dwarf plants. This gave "
    "him 7 pairs of contrasting traits.",
    ["14 true-breeding varieties", "Arranged as 7 pairs, each pair contrasting in one character"],
    C12_PI("Mendel's laws of inheritance"),
    why="The other options change the number of varieties or the number of characters per pair.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "The graphical representation used to calculate the probability of all possible genotypes of offspring in a "
    "genetic cross was developed by:",
    P("Reginald C. Punnett", ["Gregor Mendel", "Hugo de Vries", "Walter Sutton"], "C"),
    "Punnett square",
    "The Punnett square, developed by the British geneticist Reginald C. Punnett, is a graphical representation to "
    "calculate the probability of all possible genotypes of offspring in a genetic cross. The possible gametes of "
    "one parent are written along the top row and those of the other along the left column.",
    ["Punnett square → Reginald C. Punnett"],
    C12_PI("inheritance of one gene"),
    why="Mendel did the experiments, de Vries was one of the rediscoverers of his work, and Sutton proposed the "
        "chromosomal theory with Boveri; none of them devised the Punnett square.",
    seconds=20)

add(PIV, "Sex determination", "Basic", "direct",
    "In honey bees, a female has 32 chromosomes. A male honey bee (drone) has:",
    P("16 chromosomes, because it develops from an unfertilised egg and is haploid",
      ["32 chromosomes, like the female", "64 chromosomes, because it develops from a fertilised egg",
       "31 chromosomes, because it lacks one sex chromosome"], "D"),
    "Haplodiploid sex determination",
    "In honey bees, an offspring formed from the union of a sperm and an egg develops as a female (queen or worker), "
    "and an unfertilised egg develops as a male (drone) by parthenogenesis. The females are diploid with 32 "
    "chromosomes and the males are haploid with 16 chromosomes.",
    ["Female: fertilised egg, diploid, 32", "Male: unfertilised egg, haploid, 16"],
    C12_PI("sex determination: sex determination in honey bee"),
    why="Males are haploid, so they cannot have the diploid number 32 or a doubled 64. The 'one sex chromosome less' "
        "pattern is the XO type of grasshoppers, not honey bees.",
    seconds=25)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "The genetic disorder caused by the presence of an additional copy of chromosome 21 was first described in 1866 "
    "by:",
    P("Langdon Down", ["Henry Turner", "Harry Klinefelter", "Thomas Hunt Morgan"], "B"),
    "Down's syndrome",
    "Down's syndrome (trisomy of chromosome 21) is named after Langdon Down, who first described this genetic "
    "disorder in 1866.",
    ["Trisomy 21 → Down's syndrome", "First described by Langdon Down in 1866"],
    C12_PI("genetic disorders: chromosomal disorders"),
    why="Turner and Klinefelter syndromes are other chromosomal disorders named after other workers; Morgan worked "
        "on linkage in Drosophila.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "statement_pair",
    sp("Genes that code for a pair of contrasting traits are known as alleles, i.e. they are slightly different forms "
       "of the same gene.",
       "A homozygous tall pea plant (TT) produces two kinds of gametes, T and t, in equal proportion."),
    SP("C"),
    "Alleles and gamete formation",
    "Alleles are slightly different forms of the same gene coding for a pair of contrasting traits. During gamete "
    "formation the two alleles of a pair segregate, so a homozygous plant (TT) produces only one kind of gamete (T); "
    "a heterozygote (Tt) produces two kinds, T and t, in equal proportion.",
    ["Statement I: true", "Statement II: false, TT gives only T gametes"],
    C12_PI("inheritance of one gene; law of segregation"),
    seconds=25)

add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("character studied by Mendel in pea", "dominant trait"),
       ["Flower position", "Pod shape", "Pod colour", "Seed colour"],
       ["Yellow", "Axial", "Green", "Inflated"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
       {"A": "II", "B": "III", "C": "IV", "D": "I"}], "D"),
    "Contrasting traits studied by Mendel",
    "Among Mendel's seven pairs of contrasting traits: flower position axial (dominant) / terminal; pod shape "
    "inflated (dominant) / constricted; pod colour green (dominant) / yellow; seed colour yellow (dominant) / green. "
    "Note that green is dominant for the pod but yellow is dominant for the seed.",
    ["Flower position → axial (A-II)", "Pod shape → inflated (B-IV)", "Pod colour → green (C-III)",
     "Seed colour → yellow (D-I)"],
    C12_PI("Mendel's laws of inheritance: seven pairs of contrasting traits"),
    why="The commonest error swaps the dominant colours of pod and seed (option A). The other codes interchange "
        "axial and inflated, or green and inflated.",
    seconds=40)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Mendel used 'true-breeding' lines in his experiments. A true-breeding line is one that:",
    P("Has undergone continuous self-pollination and shows stable inheritance and expression of a trait for several "
      "generations",
      ["Is produced afresh by crossing two different varieties in every generation",
       "Shows a 3 : 1 ratio of the contrasting traits in every generation",
       "Has been raised only from cross-pollinated, emasculated flowers"], "B"),
    "True-breeding lines",
    "NCERT defines a true-breeding line as one that, having undergone continuous self-pollination, shows stable "
    "trait inheritance and expression for several generations.",
    ["Continuous self-pollination", "Stable trait for several generations"],
    C12_PI("Mendel's laws of inheritance"),
    why="Crossing different varieties produces hybrids, not true-breeding lines; a 3 : 1 ratio means the parent was "
        "heterozygous; emasculation and cross-pollination are used to make hybrids.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "The genes A, B, C and D assort independently. How many genetically different kinds of gametes can a plant of "
    "genotype AaBbCCDd produce?",
    P("8", ["16", "4", "6"], "C"),
    "Number of gamete types",
    "Each heterozygous gene pair gives two kinds of gametes and each homozygous pair only one. AaBbCCDd has three "
    "heterozygous pairs (Aa, Bb, Dd), so the number of gamete types = 2³ = 8.",
    ["Heterozygous pairs: Aa, Bb, Dd → n = 3", "CC is homozygous → contributes one kind", "Gamete types = 2ⁿ = 8"],
    C12_PI("inheritance of two genes; law of independent assortment"),
    shortcut="Gamete types = 2ⁿ, n = number of heterozygous gene pairs.",
    why="16 counts CC as heterozygous. 4 counts only two heterozygous pairs. 6 adds up 2 per heterozygous pair instead "
        "of multiplying.",
    seconds=40, verified_by=RECOMPUTED)

add(PIV, "Mendelian inheritance", "Intermediate", "statement_pair",
    sp("In Mendel's dihybrid cross, the F2 ratio of 9 : 3 : 3 : 1 can be derived as a combination of the series "
       "3 yellow : 1 green with the series 3 round : 1 wrinkled, i.e. (3 : 1)(3 : 1).",
       "For each of the other traits Mendel studied, only one of the parental traits was expressed in the F1, while "
       "both traits were expressed in the F2 in the proportion 3 : 1."),
    SP("A"),
    "Monohybrid and dihybrid ratios",
    "Mendel found that, for every trait pair he studied, the F1 showed only one parental trait and the F2 showed "
    "both in a 3 : 1 proportion. In the dihybrid cross the two characters behave independently, so the F2 ratio "
    "9 : 3 : 3 : 1 is the product of two independent 3 : 1 series: (3 yellow : 1 green) × (3 round : 1 wrinkled).",
    ["Statement I: true, (3 : 1)(3 : 1) = 9 : 3 : 3 : 1", "Statement II: true"],
    C12_PI("inheritance of one gene; inheritance of two genes"),
    seconds=35)

add(PIV, "Mendelian inheritance", "Intermediate", "assertion_reason",
    ar("A modified allele of a gene is generally the dominant allele.",
       "The unmodified (functioning) allele of a gene represents the original phenotype."),
    AR("D"),
    "Concept of dominance",
    "A modified allele may produce a normal or less efficient enzyme, a non-functional enzyme, or no enzyme at all. "
    "In the last two cases the phenotype depends only on the unmodified allele. NCERT therefore states that the "
    "unmodified (functioning) allele, which represents the original phenotype, is the dominant allele and the "
    "modified allele is generally the recessive allele. A is false; R is true.",
    ["A: false, the modified allele is generally recessive", "R: true"],
    C12_PI("inheritance of one gene: concept of dominance"),
    seconds=35)

add(PIV, "Mendelian inheritance", "Intermediate", "multi_statement",
    ms("Which of the following statements about Mendel's laws are correct?",
       ["A homozygous parent produces gametes that are all similar.",
        "A heterozygous parent produces two kinds of gametes, each having one allele, in equal proportion.",
        "The law of dominance explains why only one of the parental characters is expressed in a monohybrid cross "
        "in the F1.",
        "Mendel's factors occur singly in each individual.",
        "In a monohybrid cross with complete dominance, the F2 genotypic ratio is 3 : 1."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "B"),
    "Laws of dominance and segregation",
    "Characters are controlled by discrete units called factors, which occur in pairs; in a dissimilar pair one "
    "dominates. The law of dominance explains the expression of only one parental character in the monohybrid F1. "
    "By the law of segregation, a homozygous parent produces one kind of gamete and a heterozygote two kinds in "
    "equal proportion. The monohybrid F2 genotypic ratio is 1 : 2 : 1 (phenotypic 3 : 1).",
    ["(a) True", "(b) True", "(c) True", "(d) False: factors occur in pairs",
     "(e) False: genotypic ratio is 1 : 2 : 1; 3 : 1 is the phenotypic ratio"],
    C12_PI("inheritance of one gene: law of dominance and law of segregation"),
    why="Options A, C and D include (d) or (e).",
    seconds=45)

add(PIV, "Sex-linked inheritance", "Intermediate", "direct",
    "T.H. Morgan carried out several dihybrid crosses in Drosophila to study genes that were:",
    P("Sex-linked, i.e. located on the X chromosome",
      ["Present on the Y chromosome only", "Located in the mitochondria", "Each on a different autosome"], "C"),
    "Morgan's experiments",
    "Morgan carried out several dihybrid crosses in Drosophila to study genes that were sex-linked, i.e. located on "
    "the X chromosome (e.g. yellow body and white eye). He found that the two genes did not segregate independently "
    "and the F2 ratio deviated very significantly from 9 : 3 : 3 : 1.",
    ["Morgan's dihybrid crosses → sex-linked (X-linked) genes", "Result: linkage, deviation from 9 : 3 : 3 : 1"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="Genes on different autosomes would assort independently and give 9 : 3 : 3 : 1; Morgan did not study "
        "Y-linked or mitochondrial genes in these crosses.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Intermediate", "match_list",
    ml(("cross", "expected ratio of progeny"),
       ["Monohybrid F2 (complete dominance), phenotypes", "Monohybrid F2, genotypes",
        "Dihybrid F2 (independent genes, complete dominance), phenotypes", "Test cross AaBb × aabb (independent genes)"],
       ["1 : 1 : 1 : 1", "9 : 3 : 3 : 1", "1 : 2 : 1", "3 : 1"]),
    M({"A": "IV", "B": "III", "C": "II", "D": "I"},
      [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "IV", "B": "I", "C": "II", "D": "III"}], "C"),
    "Mendelian ratios",
    "A monohybrid F2 shows 3 : 1 phenotypes and 1 : 2 : 1 genotypes (TT : Tt : tt). A dihybrid F2 with independent "
    "assortment shows 9 : 3 : 3 : 1 phenotypes. A dihybrid test cross gives the four gamete types of AaBb in equal "
    "frequency against ab, i.e. 1 : 1 : 1 : 1.",
    ["Monohybrid phenotypes → 3 : 1 (A-IV)", "Monohybrid genotypes → 1 : 2 : 1 (B-III)",
     "Dihybrid phenotypes → 9 : 3 : 3 : 1 (C-II)", "Dihybrid test cross → 1 : 1 : 1 : 1 (D-I)"],
    C12_PI("inheritance of one gene; inheritance of two genes"),
    why="The wrong codes swap the monohybrid phenotypic and genotypic ratios, or the dihybrid F2 and test-cross "
        "ratios.",
    seconds=40)

add(PIV, "Mendelian inheritance", "Intermediate", "assertion_reason",
    ar("Mendel's concept of factors as stable and discrete units was not accepted by his contemporaries.",
       "Most of his contemporaries saw variation in nature as apparently continuous, and discrete, non-blending "
       "factors did not seem to explain it."),
    AR("A"),
    "Why Mendel's work was not recognised",
    "Mendel published his work in 1865, but it remained unrecognised till 1900. Among the reasons NCERT gives: his "
    "concept of genes (factors) as stable and discrete units controlling the expression of traits, and of pairs of "
    "alleles that did not blend, was not accepted as an explanation for the apparently continuous variation seen "
    "in nature. R is therefore the reason for A.",
    ["A: true", "R: true", "Discrete factors seemed to conflict with continuous variation → R explains A"],
    C12_PI("chromosomal theory of inheritance"),
    seconds=40)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "A pea plant heterozygous for seed shape and seed colour (RrYy) is self-pollinated. The two genes assort "
    "independently; round (R) is dominant over wrinkled and yellow (Y) over green. Out of 1600 seeds obtained, how "
    "many are expected to be round and green?",
    P("300", ["900", "100", "600"], "D"),
    "Dihybrid F2 phenotypic classes",
    "The F2 shows 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green. Round green = 3/16 of the "
    "progeny = 3/16 × 1600 = 300.",
    ["Round green (R_yy) = 3/4 × 1/4 = 3/16", "3/16 × 1600 = 300"],
    C12_PI("inheritance of two genes"),
    why="900 is the round yellow class (9/16). 100 is wrinkled green (1/16). 600 uses 3/8, adding the two 3/16 "
        "classes together.",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "multi_statement",
    ms("Which of the following statements about mutation are correct?",
       ["Loss (deletion) or gain (insertion or duplication) of a segment of DNA results in alteration in "
        "chromosomes.",
        "UV radiation is not a mutagen.",
        "Chromosomal aberrations are commonly observed in cancer cells.",
        "A point mutation involves the change of a large segment of a chromosome.",
        "Deletions and insertions of base pairs of DNA cause frame-shift mutations."]),
    P("(a), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"], "A"),
    "Mutation",
    "Mutation is a phenomenon that results in alteration of DNA sequences. Loss or gain of a segment of DNA alters "
    "chromosomes, and chromosomal aberrations are commonly seen in cancer cells. A point mutation arises from a "
    "change in a single base pair (e.g. sickle-cell anaemia). Deletions and insertions of base pairs cause "
    "frame-shift mutations. Chemical and physical factors that induce mutations are mutagens; UV radiation is one.",
    ["(a) True", "(b) False: UV radiation is a mutagen", "(c) True",
     "(d) False: a point mutation is a change in a single base pair", "(e) True"],
    C12_PI("mutation"),
    why="Options B, C and D include (b) or (d).",
    seconds=45)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "direct",
    "In the ABO blood group system, Iᴬ and Iᴮ are co-dominant and both are dominant over i. How many different blood "
    "group phenotypes can the possible genotypes of this gene produce in the human population?",
    P("Four (A, B, AB and O)", ["Three (A, B and O)", "Six, one for each genotype", "Two (A and B)"], "B"),
    "Phenotypes of the ABO system",
    "With three alleles, six genotypes are possible: IᴬIᴬ and Iᴬi give blood group A; IᴮIᴮ and Iᴮi give B; IᴬIᴮ "
    "gives AB, because Iᴬ and Iᴮ are co-dominant and both sugars are expressed; and ii gives O. The six genotypes "
    "therefore produce four phenotypes.",
    ["IᴬIᴬ, Iᴬi → A", "IᴮIᴮ, Iᴮi → B", "IᴬIᴮ → AB (co-dominance)", "ii → O", "4 phenotypes"],
    C12_PI("inheritance of one gene: co-dominance (ABO blood groups)"),
    why="'Three' ignores the AB group produced by co-dominance. 'Six' counts genotypes, not phenotypes; IᴬIᴬ and "
        "Iᴬi (and IᴮIᴮ and Iᴮi) look alike because Iᴬ and Iᴮ dominate i. 'Two' ignores AB and O.",
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "numerical",
    "Two individuals with normal phenotype, both heterozygous carriers of an autosomal recessive disorder such as "
    "sickle-cell anaemia, have a child with normal phenotype. What is the probability that this child is a carrier?",
    P("2/3", ["1/2", "1/4", "3/4"], "B"),
    "Conditional probability in an autosomal recessive cross",
    "Aa × Aa gives AA : Aa : aa = 1 : 2 : 1. The child is known to be normal, so aa is excluded. Among the three "
    "remaining equally likely outcomes (AA, Aa, Aa), two are carriers. Probability = 2/3.",
    ["Aa × Aa → 1 AA : 2 Aa : 1 aa", "Normal phenotype → only AA or Aa (3 parts)", "Carrier = 2 of 3 → 2/3"],
    C12_PI("Mendelian disorders: sickle-cell anaemia"),
    shortcut="Normal child of two carriers: P(carrier) = 2/3.",
    why="1/2 is the chance that any child (before its phenotype is known) is a carrier. 1/4 is the chance of an "
        "affected child. 3/4 is the chance of a normal phenotype.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Mendelian inheritance", "Advanced", "direct",
    "A modified allele of a gene may produce (i) a normal or less efficient enzyme, (ii) a non-functional enzyme or "
    "(iii) no enzyme at all. According to NCERT, in which case is the modified allele equivalent to the unmodified "
    "allele, so that it produces the same phenotype?",
    P("Case (i) only", ["Case (ii) only", "Cases (ii) and (iii) only", "Case (iii) only"], "C"),
    "Concept of dominance",
    "NCERT explains that in the first case, where the modified allele produces a normal or less efficient enzyme, "
    "the modified allele is equivalent to the unmodified allele and produces the same phenotype. If it produces a "
    "non-functional enzyme or no enzyme, the phenotype depends only on the functioning of the unmodified allele, "
    "and the modified allele behaves as the recessive allele.",
    ["(i) normal/less efficient enzyme → same phenotype", "(ii), (iii) → phenotype depends on the unmodified allele; "
     "modified allele is recessive"],
    C12_PI("inheritance of one gene: concept of dominance"),
    why="In cases (ii) and (iii) the modified allele makes no working enzyme, so it is not equivalent to the "
        "unmodified allele.",
    seconds=45)

add(PIV, "Linkage and crossing over", "Advanced", "direct",
    "Three genes P, Q and R lie on the same chromosome. The recombination frequencies between them are: P–Q 8%, "
    "Q–R 15% and P–R 7%. Using recombination frequency as a measure of the distance between genes, the gene that "
    "lies in the middle is:",
    P("P, because the P–Q and P–R distances add up to the Q–R distance",
      ["Q, because it shows the largest recombination frequency with R",
       "R, because it shows the smallest recombination frequency with P",
       "None; the data show that the three genes are not linked"], "D"),
    "Chromosome mapping",
    "Sturtevant used the frequency of recombination between gene pairs on the same chromosome as a measure of the "
    "distance between them. The two outer genes show the largest distance: Q–R = 15. The middle gene's distances to "
    "the two ends must add up to this: P–Q + P–R = 8 + 7 = 15. So the order is Q–P–R and P is in the middle.",
    ["Largest value Q–R = 15 → Q and R are at the ends", "8 + 7 = 15 → P lies between them", "Order: Q–P–R"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    shortcut="The gene absent from the largest-distance pair is the middle one.",
    why="Q and R form the most distant pair, so neither can be in the middle. Recombination frequencies well below "
        "50% show that the genes are linked.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "assertion_reason",
    ar("Down's syndrome is a chromosomal disorder, not a Mendelian disorder.",
       "It is caused by the gain of a whole chromosome (an additional copy of chromosome 21), not by an alteration or "
       "mutation in a single gene."),
    AR("A"),
    "Mendelian versus chromosomal disorders",
    "Mendelian disorders are mainly determined by alteration or mutation in a single gene. Chromosomal disorders are "
    "caused by absence, excess or abnormal arrangement of one or more chromosomes. Down's syndrome results from an "
    "additional copy of chromosome 21 (trisomy, an aneuploidy), so it is a chromosomal disorder. R gives exactly the "
    "basis of this classification.",
    ["A: true", "R: true", "Classification depends on single-gene versus whole-chromosome change → R explains A"],
    C12_PI("genetic disorders: Mendelian and chromosomal disorders"),
    seconds=40)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "multi_statement",
    ms("Which of the following statements about sickle-cell anaemia and thalassemia are correct?",
       ["Sickle-cell anaemia results from a single base substitution at the sixth codon of the β-globin gene, from "
        "GAG to GUG.",
        "Under low oxygen tension, the mutant haemoglobin of sickle-cell anaemia polymerises, changing the shape of "
        "the RBC from a biconcave disc to an elongated sickle-like structure.",
        "Thalassemia is caused by mutation or deletion that results in a reduced rate of synthesis of one of the "
        "globin chains of haemoglobin.",
        "α-thalassemia is controlled by two closely linked genes, HBA1 and HBA2, on chromosome 16 of each parent.",
        "β-thalassemia is controlled by two closely linked genes on chromosome 16."]),
    P("(a), (b), (c) and (d) only",
      ["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only"], "B"),
    "Sickle-cell anaemia and thalassemia",
    "In sickle-cell anaemia, a single base substitution (GAG → GUG) at the sixth codon of the β-globin gene replaces "
    "glutamic acid by valine; under low oxygen tension the mutant haemoglobin polymerises and the RBC becomes "
    "sickle-shaped. Thalassemia results from mutation or deletion that reduces synthesis of α or β globin chains. "
    "α-thalassemia is controlled by HBA1 and HBA2 on chromosome 16; β-thalassemia by a single gene, HBB, on "
    "chromosome 11.",
    ["(a) True", "(b) True", "(c) True", "(d) True",
     "(e) False: β-thalassemia is controlled by the single gene HBB on chromosome 11"],
    C12_PI("genetic disorders: sickle-cell anaemia and thalassemia"),
    why="Options A and C include the false statement (e); option D leaves out the true statement (b).",
    seconds=60)

add(PIV, "Sex determination", "Advanced", "statement_pair",
    sp("In the XO type of sex determination, seen in grasshoppers, the males have one chromosome fewer than the "
       "females.",
       "In the XY type of sex determination, seen in many insects and in mammals including humans, males and females "
       "have the same number of chromosomes."),
    SP("A"),
    "XO and XY mechanisms",
    "In grasshoppers (XO type), females have a pair of X chromosomes besides the autosomes, while males have only "
    "one X, so males have one chromosome fewer. In the XY type (Drosophila, humans), the male has one X and one Y "
    "and the female two X chromosomes, so both sexes have the same chromosome number.",
    ["Statement I: true (XX female, XO male)", "Statement II: true (XX female, XY male)"],
    C12_PI("sex determination"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "direct",
    "In a family, both parents are unaffected, but one of their daughters is affected by a disorder caused by a "
    "single gene. Which mode of inheritance best fits this observation?",
    P("Autosomal recessive",
      ["Autosomal dominant", "X-linked recessive", "Y-linked"], "D"),
    "Mendelian inheritance of dominant and recessive traits",
    "A dominant trait would show up in at least one parent of an affected child, so autosomal dominant is ruled out. "
    "An X-linked recessive daughter must receive the recessive allele from her father, who would then be affected; "
    "the father is unaffected, so this is ruled out. Y-linked traits never appear in daughters. Unaffected carrier "
    "parents (Aa × Aa) can have an affected daughter (aa): autosomal recessive.",
    ["Dominant: an affected child needs an affected parent → no", "X-linked recessive daughter → father must be "
     "affected → no", "Y-linked → males only → no", "Autosomal recessive (carrier parents) → yes"],
    C12_PI("Mendelian disorders: dominant and recessive inheritance"),
    why="Each of the other modes is excluded by the unaffected father or by the affected individual being female.",
    seconds=60)


# ================================================================ Molecular Basis of Inheritance (7 / 10 / 7)
C12_MB = lambda s: ref(12, MBI, s)

# nucleosomes in a diploid human cell: 6.6 x 10^9 bp, about 200 bp per nucleosome
bp_diploid, bp_per_nuc = 66 * 10 ** 8, 200
assert F(bp_diploid, bp_per_nuc) == 33 * 10 ** 6                  # 3.3 x 10^7
assert F(bp_diploid, 2 * bp_per_nuc) == F(165, 10) * 10 ** 6       # distractor 1.65 x 10^7: halved for diploidy again
assert bp_diploid * bp_per_nuc == 132 * 10 ** 10                   # distractor 1.32 x 10^12: multiplied
assert F(bp_diploid, 2000) == 33 * 10 ** 5                         # distractor 3.3 x 10^6: 2000 bp per nucleosome

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "In a polynucleotide chain, two nucleotides are linked to each other through a:",
    P("3'–5' phosphodiester linkage", ["N-glycosidic linkage", "Peptide bond", "Hydrogen bond between bases"], "A"),
    "Polynucleotide chain",
    "A nitrogenous base joins the pentose sugar through an N-glycosidic linkage to form a nucleoside; a phosphate "
    "group joins the 5'-OH of a nucleoside through a phosphoester linkage to form a nucleotide. Two nucleotides are "
    "linked through a 3'–5' phosphodiester linkage to form a dinucleotide, and more nucleotides join in the same "
    "way to form a polynucleotide.",
    ["Base + sugar: N-glycosidic", "Nucleotide + nucleotide: 3'–5' phosphodiester"],
    C12_MB("structure of polynucleotide chain"),
    why="The N-glycosidic bond joins the base to the sugar within a nucleotide. Peptide bonds join amino acids. "
        "Hydrogen bonds join bases of the two strands, not adjacent nucleotides of one chain.",
    seconds=20)

add(MBI, "DNA as genetic material", "Basic", "direct",
    "DNA, as an acidic substance present in the nucleus, was first identified in 1869 by:",
    P("Friedrich Meischer, who named it 'nuclein'",
      ["Erwin Chargaff, who named it 'nuclein'", "Frederick Griffith, who called it the 'transforming principle'",
       "James Watson, who named it 'deoxyribonucleic acid'"], "C"),
    "Discovery of DNA",
    "NCERT records that DNA as an acidic substance present in the nucleus was first identified by Friedrich Meischer "
    "in 1869. He named it 'nuclein'. Due to technical limitations, its structure was worked out only much later, in "
    "1953.",
    ["1869: Friedrich Meischer", "Name given: 'nuclein'"],
    C12_MB("structure of polynucleotide chain"),
    why="Chargaff studied base ratios much later. Griffith's 'transforming principle' (1928) came from experiments "
        "on Streptococcus pneumoniae. Watson worked out the double helix in 1953.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "Watson and Crick proposed the double helix model of DNA in 1953 on the basis of X-ray diffraction data "
    "produced by:",
    P("Maurice Wilkins and Rosalind Franklin",
      ["Meselson and Stahl", "Hershey and Chase", "Avery, MacLeod and McCarty"], "D"),
    "Double helix model",
    "Based on the X-ray diffraction data produced by Maurice Wilkins and Rosalind Franklin, James Watson and Francis "
    "Crick proposed a very simple but famous double helix model for the structure of DNA in 1953.",
    ["X-ray diffraction data → Wilkins and Franklin", "Model → Watson and Crick (1953)"],
    C12_MB("structure of polynucleotide chain"),
    why="Meselson and Stahl proved semiconservative replication; Hershey and Chase and Avery, MacLeod and McCarty "
        "showed that DNA is the genetic material. None of them produced the X-ray data.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "Thymine, the base present in DNA in place of uracil, is chemically:",
    P("5-methyl uracil", ["5-methyl cytosine", "A purine related to adenine", "Uracil with an extra 2'-OH group"],
      "B"),
    "Thymine and uracil",
    "Adenine and guanine are purines; cytosine, uracil and thymine are pyrimidines. Cytosine is common to DNA and "
    "RNA; thymine is present in DNA, and uracil is present in RNA at the place of thymine. Thymine is 5-methyl "
    "uracil.",
    ["Thymine = 5-methyl uracil (a pyrimidine)"],
    C12_MB("structure of polynucleotide chain"),
    why="Thymine is a pyrimidine, not a purine. Methyl cytosine is a different compound. The 2'-OH group belongs to "
        "the ribose sugar of RNA, not to a base.",
    seconds=20)

add(MBI, "Replication", "Basic", "direct",
    "Taylor and colleagues (1958) showed that DNA in chromosomes also replicates semiconservatively. They used:",
    P("Vicia faba (faba beans) and radioactive thymidine",
      ["E. coli and ¹⁵NH₄Cl", "Bacteriophages and radioactive sulphur", "Drosophila and radioactive phosphorus"], "C"),
    "Semiconservative replication in eukaryotic chromosomes",
    "Meselson and Stahl showed semiconservative replication in E. coli using ¹⁵N. Similar experiments by Taylor and "
    "colleagues in 1958 on Vicia faba (faba beans), using radioactive thymidine to detect the distribution of newly "
    "synthesised DNA in the chromosomes, proved that DNA in chromosomes also replicates semiconservatively.",
    ["Taylor and colleagues, 1958", "Vicia faba + radioactive thymidine"],
    C12_MB("replication: the experimental proof"),
    why="E. coli with ¹⁵N was the Meselson–Stahl system. Radioactive sulphur and phage were used by Hershey and "
        "Chase. Drosophila was not used for this proof.",
    seconds=25)

add(MBI, "Transcription", "Basic", "statement_pair",
    sp("In bacteria, a single DNA-dependent RNA polymerase catalyses the transcription of all types of RNA.",
       "In eukaryotes, RNA polymerase I transcribes the rRNAs 28S, 18S and 5.8S."),
    SP("A"),
    "RNA polymerases",
    "Bacteria have a single DNA-dependent RNA polymerase that transcribes mRNA, tRNA and rRNA. In the eukaryotic "
    "nucleus there are at least three RNA polymerases: RNA polymerase I transcribes rRNAs (28S, 18S and 5.8S), "
    "RNA polymerase III transcribes tRNA, 5S rRNA and snRNAs, and RNA polymerase II transcribes hnRNA.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("transcription: transcription unit and types of RNA"),
    seconds=25)

add(MBI, "Lac operon", "Basic", "direct",
    "In the lac operon, the i gene codes for the repressor. The letter 'i' in the name of this gene is derived from "
    "the word:",
    P("Inhibitor", ["Inducer", "Initiator", "Intron"], "D"),
    "The i gene of the lac operon",
    "The lac operon has a regulatory gene, i, and three structural genes, z, y and a. NCERT points out that the term "
    "i here does not refer to inducer; it is derived from the word inhibitor, because i codes for the repressor of "
    "the lac operon.",
    ["i gene → repressor", "'i' = inhibitor, not inducer"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="The inducer is lactose, a substance, not the source of the gene's name. Initiator and intron are unrelated "
        "terms.",
    seconds=20)

add(MBI, "DNA as genetic material", "Intermediate", "multi_statement",
    ms("A molecule that can act as genetic material must fulfil certain criteria. Which of the following are among "
       "these criteria?",
       ["It should be able to generate its replica.",
        "It should be chemically and structurally stable.",
        "It should provide scope for slow changes (mutation) that are required for evolution.",
        "It should never undergo any change.",
        "It should be chemically highly reactive."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only"], "D"),
    "Properties of genetic material",
    "NCERT lists the criteria: the genetic material should be able to generate its replica (replication); it should "
    "be chemically and structurally stable; it should provide scope for slow changes (mutation) required for "
    "evolution; and it should be able to express itself in the form of 'Mendelian characters'. DNA, being "
    "chemically less reactive and structurally more stable, is better suited than RNA for storing genetic "
    "information.",
    ["(a) True", "(b) True", "(c) True", "(d) False: slow changes (mutation) are needed for evolution",
     "(e) False: stability, not high reactivity, is required"],
    C12_MB("the search for genetic material: properties of genetic material"),
    why="Options A, B and C include (d) or (e).",
    seconds=45)

add(MBI, "DNA as genetic material", "Intermediate", "assertion_reason",
    ar("Viruses having an RNA genome and a shorter life span mutate and evolve faster.",
       "RNA is unstable and mutates at a faster rate."),
    AR("A"),
    "Stability of RNA and DNA",
    "NCERT explains that RNA, being unstable, mutates at a faster rate. Consequently, viruses having an RNA genome "
    "and a shorter life span mutate and evolve faster. R is the cause of A.",
    ["A: true", "R: true", "Faster mutation of the unstable RNA genome → faster evolution → R explains A"],
    C12_MB("properties of genetic material: DNA versus RNA"),
    seconds=35)

add(MBI, "DNA packaging", "Intermediate", "statement_pair",
    sp("A typical nucleosome contains about 200 bp of DNA helix, and nucleosomes constitute the repeating unit of "
       "chromatin.",
       "In a nucleosome, the negatively charged DNA is wrapped around a negatively charged histone octamer."),
    SP("C"),
    "Nucleosome",
    "Histones are positively charged proteins organised into a unit of eight molecules, the histone octamer. The "
    "negatively charged DNA is wrapped around the positively charged histone octamer to form a nucleosome, which "
    "contains about 200 bp of DNA. Nucleosomes are the repeating units of chromatin, the thread-like stained "
    "bodies seen in the nucleus.",
    ["Statement I: true", "Statement II: false, the histone octamer is positively charged"],
    C12_MB("packaging of DNA helix"),
    seconds=30)

add(MBI, "Transcription", "Intermediate", "direct",
    "Structural genes in a transcription unit may be monocistronic or polycistronic. Which statement is correct?",
    P("They are mostly monocistronic in eukaryotes and polycistronic in bacteria or prokaryotes",
      ["They are mostly polycistronic in eukaryotes and monocistronic in bacteria",
       "They are always monocistronic in all organisms",
       "They are always polycistronic in all organisms"], "B"),
    "Monocistronic and polycistronic genes",
    "A cistron is a segment of DNA coding for a polypeptide. NCERT states that the structural gene in a "
    "transcription unit could be monocistronic (mostly in eukaryotes) or polycistronic (mostly in bacteria or "
    "prokaryotes). The lac operon, whose three structural genes are transcribed together, is an example of the "
    "prokaryotic, polycistronic arrangement.",
    ["Eukaryotes: mostly monocistronic", "Prokaryotes: mostly polycistronic (e.g. lac operon)"],
    C12_MB("transcription: transcription unit and the gene"),
    why="Option A reverses the two groups, and options C and D ignore the difference between them.",
    seconds=30)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "match_list",
    ml(("step of DNA fingerprinting", "technique used"),
       ["Cutting the isolated DNA into fragments", "Separating the DNA fragments by size",
        "Transferring the separated fragments to nitrocellulose or nylon membranes",
        "Detecting the fragments that hybridised with the labelled VNTR probe"],
       ["Blotting", "Autoradiography", "Digestion by restriction endonucleases", "Electrophoresis"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "III", "B": "I", "C": "IV", "D": "II"}], "B"),
    "Steps of DNA fingerprinting",
    "The steps are: isolation of DNA; digestion by restriction endonucleases; separation of the fragments by "
    "electrophoresis; transfer (blotting) of the separated fragments to synthetic membranes such as nitrocellulose "
    "or nylon; hybridisation using a labelled VNTR probe; and detection of the hybridised fragments by "
    "autoradiography.",
    ["Cutting → restriction endonucleases (A-III)", "Separation → electrophoresis (B-IV)",
     "Transfer → blotting (C-I)", "Detection → autoradiography (D-II)"],
    C12_MB("DNA fingerprinting"),
    why="The wrong codes interchange cutting with separation, transfer with detection, or separation with transfer.",
    seconds=40)

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "The secondary structure of tRNA is drawn as a clover-leaf. In its actual three-dimensional form, tRNA is a "
    "compact molecule that looks like:",
    P("An inverted L", ["A double helix", "A straight rod", "A closed circle"], "D"),
    "Structure of tRNA",
    "tRNA, the adapter molecule, has an anticodon loop with bases complementary to the codon and an amino acid "
    "acceptor end. Its secondary structure is depicted as a clover-leaf, but in actual structure tRNA is a compact "
    "molecule that looks like an inverted L.",
    ["Secondary structure: clover-leaf", "Actual 3-D structure: inverted L"],
    C12_MB("genetic code: tRNA, the adapter molecule"),
    why="tRNA is a single chain folded on itself, not a double helix, a straight rod or a closed circle.",
    seconds=20)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("The repressor of the lac operon is synthesised all the time (constitutively) from the i gene.",
       "β-galactosidase is primarily responsible for the hydrolysis of the disaccharide lactose into its monomeric "
       "units, galactose and glucose."),
    AR("B"),
    "Lac operon: repressor and β-galactosidase",
    "Both are NCERT statements. A describes the regulatory gene: the repressor is made constitutively from the i "
    "gene. R describes the product of the structural z gene and its catalytic role. What β-galactosidase does to "
    "lactose has no bearing on why the repressor is produced all the time, so R does not explain A.",
    ["A: true", "R: true", "R is about the z-gene enzyme, not about the i-gene repressor → B"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "statement_pair",
    sp("The Human Genome Project was launched in 1990 and completed in 2003.",
       "The Human Genome Project was coordinated solely by the U.S. Department of Energy, with no participation "
       "from any other organisation or country."),
    SP("C"),
    "Human Genome Project",
    "The HGP, a mega project launched in 1990 and completed in 2003, was coordinated by the U.S. Department of "
    "Energy and the National Institute of Health. During its early years the Wellcome Trust (U.K.) became a major "
    "partner, and additional contributions came from Japan, France, Germany, China and others.",
    ["Statement I: true", "Statement II: false, it was coordinated by DOE and NIH, with international partners"],
    C12_MB("human genome project"),
    seconds=30)

add(MBI, "DNA and RNA structure", "Intermediate", "multi_statement",
    ms("Which of the following are salient features of the double helix structure of DNA?",
       ["The two polynucleotide chains have antiparallel polarity.",
        "A purine always comes opposite a pyrimidine, which generates an approximately uniform distance between the "
        "two strands.",
        "The two chains are coiled in a left-handed fashion.",
        "The plane of one base pair stacks over the other, which, in addition to hydrogen bonds, confers stability "
        "on the helix.",
        "The sequence of bases in one strand is identical to that in the other strand."]),
    P("(a), (b) and (d) only",
      ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "C"),
    "Double helix model",
    "In the double helix, the two chains are antiparallel; bases pair so that a purine always faces a pyrimidine, "
    "keeping the distance between strands roughly uniform; the chains are coiled in a right-handed fashion; and "
    "base-pair stacking, together with hydrogen bonds, stabilises the helix. The two strands are complementary, "
    "not identical, in sequence.",
    ["(a) True", "(b) True", "(c) False: right-handed coiling", "(d) True",
     "(e) False: the sequences are complementary"],
    C12_MB("structure of polynucleotide chain: double helix"),
    why="Options A, B and D include (c) or (e).",
    seconds=45)

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "Which of the following statements about the central dogma of molecular biology is correct?",
    P("In some viruses, the flow of information is in the reverse direction, from RNA to DNA",
      ["Genetic information normally flows from protein to RNA to DNA",
       "Translation is the copying of DNA into RNA",
       "Transcription is the synthesis of a polypeptide using an mRNA template"], "A"),
    "Central dogma",
    "The central dogma states that genetic information flows from DNA → RNA → protein: DNA is copied into RNA "
    "(transcription), and RNA is translated into protein (translation). NCERT adds that in some viruses the flow of "
    "information is in the reverse direction, from RNA to DNA.",
    ["Normal flow: DNA → RNA → protein", "Exception: some viruses, RNA → DNA"],
    C12_MB("RNA world; central dogma"),
    why="Option B reverses the flow. Options C and D swap the definitions of transcription and translation.",
    seconds=30)

add(MBI, "DNA packaging", "Advanced", "numerical",
    "A diploid human cell contains about 6.6 × 10⁹ bp of DNA, and a typical nucleosome contains about 200 bp of DNA "
    "helix. Approximately how many nucleosomes are present in such a cell?",
    P("3.3 × 10⁷", ["3.3 × 10⁶", "1.65 × 10⁷", "1.32 × 10¹²"], "D"),
    "Nucleosome count",
    "Number of nucleosomes ≈ total bp ÷ bp per nucleosome = 6.6 × 10⁹ ÷ 200 = 3.3 × 10⁷. The 6.6 × 10⁹ bp is "
    "already the diploid content, so it should not be halved or doubled again.",
    ["6.6 × 10⁹ ÷ 2 × 10² = 3.3 × 10⁷"],
    C12_MB("packaging of DNA helix"),
    why="3.3 × 10⁶ uses 2000 bp per nucleosome. 1.65 × 10⁷ halves the diploid content again. 1.32 × 10¹² "
        "multiplies instead of dividing.",
    seconds=45, verified_by=RECOMPUTED)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "multi_statement",
    ms("Which of the following statements related to DNA fingerprinting are correct?",
       ["Any two individuals differ in about 99.9 per cent of the base pairs of their genomes.",
        "In density gradient centrifugation, the bulk DNA forms a major peak, while repetitive DNA forms small peaks "
        "referred to as satellite DNA.",
        "Satellite DNA is classified into categories such as micro-satellites and mini-satellites on the basis of "
        "base composition, length of segment and number of repetitive units.",
        "The size of a VNTR is the same in all individuals of a population.",
        "An inheritable mutation observed in a population at high frequency is referred to as DNA polymorphism."]),
    P("(b), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"], "B"),
    "Basis of DNA fingerprinting",
    "99.9 per cent of the base pairs of the human genome are identical between individuals; differences lie in "
    "repetitive DNA. In density gradient centrifugation, bulk DNA forms a major peak and repetitive DNA forms "
    "satellite peaks. Satellite DNA is classified by base composition (A:T-rich or G:C-rich), segment length and "
    "number of repeats into micro- and mini-satellites. VNTRs vary in size from 0.1 to 20 kb, which is the basis of "
    "the different band patterns. A heritable mutation present at high frequency in a population is called DNA "
    "polymorphism.",
    ["(a) False: 99.9% of base pairs are identical", "(b) True", "(c) True",
     "(d) False: VNTR size varies from 0.1 to 20 kb", "(e) True"],
    C12_MB("DNA fingerprinting"),
    why="Options A, C and D include the false statements (a) or (d).",
    seconds=55)

add(MBI, "Replication", "Advanced", "assertion_reason",
    ar("A piece of DNA that is to be propagated during recombinant DNA procedures requires a vector.",
       "DNA replication does not initiate randomly at any place in DNA; it starts at a definite region called the "
       "origin of replication, which the vector provides."),
    AR("A"),
    "Origin of replication",
    "DNA polymerases cannot initiate replication on their own, and replication does not start randomly: it begins "
    "at a definite region, the origin of replication. NCERT explains that it is because of this that a piece of "
    "DNA to be propagated during recombinant DNA procedures requires a vector, which provides the origin of "
    "replication. R explains A.",
    ["A: true", "R: true", "Need for an origin of replication → need for a vector → R explains A"],
    C12_MB("replication: the machinery and the enzymes"),
    seconds=40)

add(MBI, "Transcription", "Advanced", "assertion_reason",
    ar("In eukaryotes, the primary transcript contains both exons and introns and is non-functional.",
       "In eukaryotes there are at least three RNA polymerases in the nucleus, in addition to the RNA polymerase "
       "found in the organelles."),
    AR("B"),
    "Processing of the primary transcript",
    "Both statements are true. The primary transcript (hnRNA) is non-functional because it contains introns, which "
    "must be removed by splicing (with capping and tailing) before it becomes mRNA. The number of RNA polymerases "
    "in the eukaryotic nucleus is a separate fact and does not explain why the primary transcript is "
    "non-functional.",
    ["A: true (introns make the primary transcript non-functional)", "R: true (RNA pol I, II, III)",
     "R does not explain A → B"],
    C12_MB("transcription in eukaryotes"),
    seconds=40)

add(MBI, "Genetic code and translation", "Advanced", "direct",
    "Within the coding region of a gene, one base is inserted just after the third codon, and one base is deleted "
    "just after the seventh codon. Assuming no stop codon is created, what is the most likely effect on the "
    "encoded protein?",
    P("The amino acids coded from the fourth to about the seventh codon are altered, and the reading frame is "
      "restored after the deletion",
      ["Only one amino acid is added and the rest of the protein is unchanged",
       "Every amino acid after the third codon is altered up to the end of the protein",
       "The protein is unchanged, because an insertion and a deletion cancel out at once"], "C"),
    "Frame-shift mutations",
    "Insertion or deletion of one or two bases changes the reading frame from the point of insertion or deletion "
    "onwards, while insertion or deletion of three bases adds or removes a codon without altering the frame. Here "
    "the insertion after codon 3 shifts the frame, so the codons read from codon 4 onward are altered. The deletion "
    "after codon 7 removes one base and brings the frame back, so codons downstream of it are read correctly. Only "
    "the stretch between the two changes is altered.",
    ["Insertion after codon 3 → frame shifts from codon 4", "Deletion after codon 7 → frame restored",
     "Only codons 4 to about 7 are altered"],
    C12_MB("genetic code: mutations and genetic code"),
    why="Option A describes an in-frame insertion of a whole codon. Option B ignores the deletion that restores the "
        "frame. Option D ignores the codons read in the shifted frame between the two sites.",
    seconds=60)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "statement_pair",
    sp("If the human DNA sequence were printed in books, each page having 1000 letters and each book 1000 pages, "
       "3300 such books would be needed to store the information of a single human cell.",
       "The automated DNA sequencers used in the Human Genome Project work on the principle of a method developed "
       "by Frederick Sanger."),
    SP("A"),
    "Scale and methods of the HGP",
    "NCERT illustrates the size of the human genome: typed in books with 1000 letters per page and 1000 pages per "
    "book, the DNA sequence of a single human cell would need 3300 books. Sequencing was done with automated DNA "
    "sequencers working on the principle of a method developed by Frederick Sanger.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("human genome project: goals and methodologies"),
    seconds=35)

add(MBI, "DNA and RNA structure", "Advanced", "match_list",
    ml(("genome", "size given in NCERT"),
       ["Bacteriophage φX174", "Bacteriophage lambda", "Escherichia coli", "Haploid human genome"],
       ["4.6 × 10⁶ bp", "3.3 × 10⁹ bp", "5386 nucleotides", "48,502 bp"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "IV", "B": "I", "C": "III", "D": "II"}], "D"),
    "Length of DNA in different genomes",
    "The length of DNA is usually given as the number of nucleotides (or base pairs). NCERT gives: bacteriophage "
    "φX174, 5386 nucleotides; bacteriophage lambda, 48,502 bp; Escherichia coli, 4.6 × 10⁶ bp; haploid human "
    "genome, 3.3 × 10⁹ bp.",
    ["φX174 → 5386 nucleotides (A-III)", "Lambda → 48,502 bp (B-IV)", "E. coli → 4.6 × 10⁶ bp (C-I)",
     "Human (haploid) → 3.3 × 10⁹ bp (D-II)"],
    C12_MB("the DNA: length of DNA"),
    why="The wrong codes interchange the two bacteriophages, E. coli with the human genome, or the phages with "
        "E. coli.",
    seconds=45)


# ================================================================ Microbes in Human Welfare (3 / 3 / 3)
C12_MH = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "direct",
    "The dough used for making foods such as dosa and idli is fermented by bacteria. Its puffed-up appearance is due "
    "to the production of:",
    P("Carbon dioxide", ["Oxygen", "Methane", "Hydrogen sulphide"], "B"),
    "Microbes in household products",
    "NCERT notes that the dough used for making dosa and idli is fermented by bacteria. The puffed-up appearance of "
    "the dough is due to the production of CO₂ gas.",
    ["Bacterial fermentation of dough → CO₂ → puffed-up dough"],
    C12_MH("microbes in household products"),
    why="Fermentation releases CO₂, not oxygen. Methane and hydrogen sulphide are produced by anaerobic bacteria in "
        "sludge digesters and biogas plants, not in dough.",
    seconds=20)

add(MHW, "Household and industrial products", "Basic", "direct",
    "Alexander Fleming discovered penicillin, but its full potential as an effective antibiotic was established much "
    "later by:",
    P("Ernest Chain and Howard Florey",
      ["Louis Pasteur and Robert Koch", "Jacob and Monod", "Herbert Boyer and Stanley Cohen"], "D"),
    "Discovery of penicillin",
    "Fleming found that a chemical produced by the mould Penicillium notatum inhibited Staphylococci, and named it "
    "penicillin. Its full potential as an effective antibiotic was established much later by Ernest Chain and "
    "Howard Florey. Penicillin was extensively used to treat American soldiers wounded in World War II, and Fleming, "
    "Chain and Florey were awarded the Nobel Prize in 1945.",
    ["Discovery: Fleming", "Full potential established: Chain and Florey", "Nobel Prize 1945 (all three)"],
    C12_MH("microbes in industrial products: antibiotics"),
    why="The other pairs are known for different work (germ theory, the lac operon, recombinant DNA) and did not "
        "develop penicillin.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "Azospirillum and Azotobacter are used as biofertilisers because they:",
    P("Fix atmospheric nitrogen while free-living in the soil",
      ["Fix nitrogen only inside root nodules of leguminous plants",
       "Are fungi that form mycorrhiza and absorb phosphorus for the plant",
       "Are cyanobacteria that add organic matter to paddy fields"], "A"),
    "Free-living nitrogen-fixing bacteria",
    "Biofertilisers are organisms that enrich the nutrient quality of the soil; the main sources are bacteria, fungi "
    "and cyanobacteria. Rhizobium fixes nitrogen in root nodules of legumes, while other bacteria such as "
    "Azospirillum and Azotobacter can fix atmospheric nitrogen while free-living in the soil, enriching its nitrogen "
    "content.",
    ["Symbiotic in nodules: Rhizobium", "Free-living in soil: Azospirillum, Azotobacter"],
    C12_MH("microbes as biofertilisers"),
    why="Root-nodule fixation is done by Rhizobium. Mycorrhizal fungi (e.g. Glomus) absorb phosphorus. Azospirillum "
        "and Azotobacter are bacteria, not cyanobacteria.",
    seconds=25)

add(MHW, "Sewage treatment", "Intermediate", "statement_pair",
    sp("BOD refers to the amount of oxygen that would be consumed if all the organic matter in one litre of water "
       "were oxidised by bacteria.",
       "The greater the BOD of waste water, the lower is its polluting potential."),
    SP("C"),
    "Biochemical oxygen demand",
    "BOD is the amount of oxygen that would be consumed if all the organic matter in one litre of water were "
    "oxidised by bacteria. It is an indirect measure of the organic matter present, so the greater the BOD of waste "
    "water, the more is its polluting potential. Sewage is treated until its BOD is reduced.",
    ["Statement I: true (definition of BOD)", "Statement II: false, higher BOD means higher polluting potential"],
    C12_MH("microbes in sewage treatment: secondary treatment"),
    seconds=30)

add(MHW, "Sewage treatment", "Intermediate", "match_list",
    ml(("term in sewage treatment", "description"),
       ["Flocs", "Primary sludge", "Gas produced in anaerobic sludge digesters", "Ganga Action Plan and Yamuna Action "
        "Plan"],
       ["Initiated by the Ministry of Environment and Forests to save major rivers from water pollution",
        "Masses of bacteria associated with fungal filaments that form mesh-like structures",
        "A mixture of methane, hydrogen sulphide and carbon dioxide",
        "All the solids that settle during primary treatment"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "II", "B": "III", "C": "IV", "D": "I"}], "A"),
    "Sewage treatment",
    "In primary treatment, all the solids that settle form the primary sludge. In secondary treatment, aerobic "
    "microbes grow into flocs, masses of bacteria associated with fungal filaments forming mesh-like structures. In "
    "anaerobic sludge digesters, bacteria digest the sludge and produce a mixture of gases such as methane, H₂S and "
    "CO₂ (biogas). The Ministry of Environment and Forests initiated the Ganga Action Plan and Yamuna Action Plan to "
    "save these major rivers from pollution.",
    ["Flocs → bacteria + fungal filaments (A-II)", "Primary sludge → settled solids (B-IV)",
     "Digester gas → methane, H₂S, CO₂ (C-III)", "Action Plans → Ministry of Environment and Forests (D-I)"],
    C12_MH("microbes in sewage treatment"),
    why="The wrong codes swap flocs with primary sludge, the digester gases with the Action Plans, or primary sludge "
        "with the digester gases.",
    seconds=45)

add(MHW, "Household and industrial products", "Intermediate", "assertion_reason",
    ar("Antibiotics have greatly improved our capacity to treat deadly diseases such as plague, whooping cough, "
       "diphtheria and leprosy.",
       "Antibiotics are chemical substances produced by some microbes that can kill or retard the growth of other "
       "(disease-causing) microbes."),
    AR("A"),
    "Antibiotics",
    "Antibiotics, produced by some microbes, kill or retard the growth of disease-causing microbes. Because they act "
    "on the pathogens themselves, they have greatly improved our capacity to treat deadly diseases such as plague, "
    "whooping cough (kali khansi), diphtheria (gal ghotu) and leprosy (kusht rog). R explains A.",
    ["A: true", "R: true", "Killing or inhibiting the pathogens is why these diseases became treatable → A"],
    C12_MH("microbes in industrial products: antibiotics"),
    seconds=35)

add(MHW, "Biogas", "Advanced", "multi_statement",
    ms("Which of the following statements are correct?",
       ["Bread dough is fermented using baker's yeast, Saccharomyces cerevisiae.",
        "Lactic acid bacteria in our stomach play a beneficial role in checking disease-causing microbes.",
        "A biogas plant has a concrete tank, 10–15 feet deep, fed with a slurry of dung, and a floating cover that "
        "keeps rising as gas is produced.",
        "Fleming discovered penicillin while working on Streptococcus bacteria.",
        "Microbial products are produced on an industrial scale in very small vessels called fermentors."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Microbes in household products, industry and biogas",
    "Baker's yeast (Saccharomyces cerevisiae) ferments bread dough. Lactic acid bacteria in our stomach help check "
    "disease-causing microbes. A biogas plant has a 10–15 feet deep concrete tank fed with dung slurry, with a "
    "floating cover that rises as the gas is produced. Fleming was working on Staphylococci when he noticed the "
    "Penicillium mould. Industrial production needs very large vessels called fermentors.",
    ["(a) True", "(b) True", "(c) True", "(d) False: he was working on Staphylococci",
     "(e) False: fermentors are very large vessels"],
    C12_MH("household products; industrial products; microbes in production of biogas"),
    why="Options A, B and C include (d) or (e), or leave out (a).",
    seconds=50)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "assertion_reason",
    ar("The use of biocontrol measures will greatly reduce our dependence on toxic chemicals and pesticides.",
       "Biocontrol refers to the use of chemical methods for controlling plant diseases and pests."),
    AR("C"),
    "Biocontrol",
    "Biocontrol refers to the use of biological methods for controlling plant diseases and pests, for example "
    "ladybirds against aphids, dragonflies against mosquitoes, Bacillus thuringiensis against caterpillars and "
    "Trichoderma against plant pathogens. Using such measures greatly reduces dependence on toxic chemicals and "
    "pesticides. A is true; R is false because biocontrol uses biological, not chemical, methods.",
    ["A: true", "R: false, biocontrol uses biological methods"],
    C12_MH("microbes as biocontrol agents"),
    seconds=35)

add(MHW, "Sewage treatment", "Advanced", "statement_pair",
    sp("Once the BOD of the waste water is reduced significantly in the aeration tanks, the effluent is passed into a "
       "settling tank where the bacterial flocs are allowed to sediment; this sediment is called activated sludge.",
       "In anaerobic sludge digesters, bacteria that grow aerobically digest the bacteria and fungi present in the "
       "sludge."),
    SP("C"),
    "Secondary treatment and sludge digestion",
    "After the BOD is reduced, the effluent goes to a settling tank where the flocs sediment as activated sludge. A "
    "small part of it is pumped back into the aeration tank as inoculum, and the major part goes to large tanks "
    "called anaerobic sludge digesters. There, other kinds of bacteria, which grow anaerobically, digest the "
    "bacteria and fungi in the sludge and release gases such as methane, H₂S and CO₂.",
    ["Statement I: true", "Statement II: false, the digester bacteria grow anaerobically"],
    C12_MH("microbes in sewage treatment: secondary treatment"),
    seconds=40)


# ================================================================ Organisms and Populations (4 / 6 / 4)
C12_OP = lambda s: ref(12, OAP, s)

# exponential growth: dN/dt = (b - d) N
b_, d_, N_ = F(30, 100), F(18, 100), 1000
assert (b_ - d_) * N_ == 120
assert (b_ + d_) * N_ == 480 and b_ * N_ == 300 and (b_ - d_) == F(12, 100)   # distractors

add(OAP, "Population attributes", "Basic", "direct",
    "An age pyramid that is urn-shaped, with a narrow base of pre-reproductive individuals, represents a population "
    "that is:",
    P("Declining", ["Expanding", "Stable", "Growing exponentially"], "C"),
    "Age pyramids",
    "Plotting the age distribution (pre-reproductive, reproductive and post-reproductive individuals) gives an age "
    "pyramid. Its shape reflects the growth status of the population: a triangular pyramid with a broad base shows "
    "an expanding population, a bell-shaped pyramid a stable population, and an urn-shaped pyramid a declining "
    "population.",
    ["Triangular → expanding", "Bell-shaped → stable", "Urn-shaped → declining"],
    C12_OP("population attributes: age pyramids"),
    why="Expanding (and exponentially growing) populations have a broad base; a stable population gives a "
        "bell-shaped pyramid.",
    seconds=20)

add(OAP, "Population growth", "Basic", "direct",
    "The logistic model of population growth, dN/dt = rN[(K − N)/K], is also called the:",
    P("Verhulst-Pearl logistic growth", ["Gause's competitive exclusion model", "MacArthur's resource-partitioning "
                                         "model", "Humboldt's species-area model"], "A"),
    "Logistic growth",
    "A population growing in a habitat with limited resources shows an initial lag phase, then acceleration and "
    "deceleration, and finally an asymptote at the carrying capacity. This type of growth is called Verhulst-Pearl "
    "logistic growth and is described by dN/dt = rN[(K − N)/K].",
    ["Logistic growth = Verhulst-Pearl logistic growth"],
    C12_OP("population growth: growth models"),
    why="Gause's principle concerns competition, MacArthur's warblers illustrate resource partitioning, and Humboldt "
        "described the species-area relationship.",
    seconds=20)

add(OAP, "Population interactions", "Basic", "direct",
    "Cattle egrets always forage close to where cattle are grazing, because the moving cattle stir up and flush out "
    "insects that the egrets would otherwise find hard to catch. The cattle are not affected. This association is "
    "an example of:",
    P("Commensalism", ["Mutualism", "Parasitism", "Amensalism"], "D"),
    "Commensalism",
    "Commensalism is an interaction in which one species benefits and the other is neither harmed nor benefited. "
    "NCERT describes the cattle egret and grazing cattle as a classic example: the egret benefits by catching the "
    "insects flushed out by the cattle, and the cattle are unaffected.",
    ["Egret: benefits (+)", "Cattle: unaffected (0)", "+/0 → commensalism"],
    C12_OP("population interactions: commensalism"),
    why="Mutualism needs both to benefit; parasitism harms the cattle; amensalism harms one partner and leaves the "
        "other unaffected.",
    seconds=25)

add(OAP, "Population attributes", "Basic", "direct",
    "Absolute population numbers are not always needed. To find out whether the fish population of a lake has "
    "changed, NCERT suggests that a good enough measure of its population density is:",
    P("The number of fish caught per trap",
      ["The total number of fish species in the lake", "The percent cover of aquatic plants",
       "The biomass of the phytoplankton"], "B"),
    "Relative density",
    "Total number is generally the most appropriate measure of population density, but it is sometimes hard to "
    "obtain or not needed. If we only want to know whether a population is growing or declining, relative density "
    "serves well: the number of fish caught per trap is a good enough measure of the total fish population density "
    "in a lake.",
    ["Relative density can replace absolute numbers", "Fish in a lake → number caught per trap"],
    C12_OP("population attributes: population density"),
    why="The number of species measures diversity, not density of one population. Plant cover and phytoplankton "
        "biomass do not measure the fish population.",
    seconds=25)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("Chemicals such as nicotine, caffeine, quinine, strychnine and opium are produced by plants as defences "
       "against grazers and browsers.",
       "In the association between the clown fish and the sea anemone, the sea anemone benefits by hosting the clown "
       "fish."),
    SP("C"),
    "Plant defences and commensalism",
    "Plants produce many chemicals, such as nicotine, caffeine, quinine, strychnine and opium, as defences against "
    "grazers and browsers. The clown fish living among the stinging tentacles of a sea anemone gets protection from "
    "predators, but the anemone does not appear to derive any benefit: this is commensalism.",
    ["Statement I: true", "Statement II: false, the anemone does not appear to benefit"],
    C12_OP("population interactions: predation and commensalism"),
    seconds=35)

add(OAP, "Population growth", "Intermediate", "numerical",
    "In a population growing exponentially, the per capita birth rate is 0.30 and the per capita death rate is 0.18 "
    "per individual per year. Using dN/dt = (b − d)N, what is the rate of increase of the population when it has "
    "1000 individuals?",
    P("120 individuals per year", ["480 individuals per year", "300 individuals per year",
                                   "0.12 individuals per year"], "A"),
    "Exponential growth",
    "In exponential growth, dN/dt = (b − d) × N, where (b − d) = r, the intrinsic rate of natural increase. "
    "r = 0.30 − 0.18 = 0.12 per individual per year, so dN/dt = 0.12 × 1000 = 120 individuals per year.",
    ["r = b − d = 0.30 − 0.18 = 0.12", "dN/dt = rN = 0.12 × 1000 = 120 per year"],
    C12_OP("population growth: exponential growth"),
    why="480 adds the death rate instead of subtracting it. 300 ignores deaths. 0.12 is r itself, not multiplied "
        "by N.",
    seconds=40, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following are features of parasites, as described by NCERT?",
       ["Loss of unnecessary sense organs.",
        "Presence of adhesive organs or suckers to cling on to the host.",
        "Loss of the digestive system.",
        "Low reproductive capacity.",
        "Many parasites are host-specific, so that the host and the parasite tend to co-evolve."]),
    P("(a), (b), (c) and (e) only",
      ["(a), (b) and (c) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only"], "D"),
    "Adaptations of parasites",
    "Many parasites have evolved to be host-specific, so that host and parasite tend to co-evolve. In accordance with "
    "their life styles, parasites show special adaptations: loss of unnecessary sense organs, presence of adhesive "
    "organs or suckers to cling on to the host, loss of the digestive system and high reproductive capacity.",
    ["(a) True", "(b) True", "(c) True", "(d) False: they have high reproductive capacity", "(e) True"],
    C12_OP("population interactions: parasitism"),
    why="Option A leaves out the true statement (e); options B and C include the false statement (d).",
    seconds=45)

add(OAP, "Population interactions", "Intermediate", "match_list",
    ml(("pair of organisms", "interaction"),
       ["Flamingoes and resident fishes in South American lakes", "Tiger and deer", "Ticks and dog",
        "Barnacles growing on the back of a whale"],
       ["Commensalism", "Competition", "Parasitism", "Predation"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "B"),
    "Population interactions: examples",
    "Flamingoes and resident fishes in some shallow South American lakes compete for their common food, the "
    "zooplankton. A tiger eating a deer is predation. Ticks on dogs are ectoparasites. Barnacles growing on the back "
    "of a whale benefit while the whale derives no noticeable benefit: commensalism.",
    ["Flamingoes–fishes → competition (A-II)", "Tiger–deer → predation (B-IV)", "Ticks–dog → parasitism (C-III)",
     "Barnacles–whale → commensalism (D-I)"],
    C12_OP("population interactions"),
    why="The wrong codes swap competition with predation, parasitism with commensalism, or competition with "
        "commensalism.",
    seconds=40)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("In a broad ecological context, herbivores are not very different from predators.",
       "Biological control methods adopted in agricultural pest control are based on the ability of the predator "
       "to regulate the prey population."),
    AR("B"),
    "Predation",
    "Both statements come from NCERT's account of predation. A says herbivores, which eat plants, behave like "
    "predators in an ecological sense. R describes the use of predators in biological pest control. The basis of "
    "biological control does not explain why herbivores resemble predators, so R is not the explanation of A.",
    ["A: true", "R: true", "R is about biological pest control, not about herbivores → B"],
    C12_OP("population interactions: predation"),
    seconds=35)

add(OAP, "Population growth", "Intermediate", "statement_pair",
    sp("In 1981, the intrinsic rate of natural increase (r) for the human population in India was 0.0205.",
       "The r values given by NCERT for the Norway rat and the flour beetle are 0.015 and 0.12 respectively."),
    SP("A"),
    "Intrinsic rate of natural increase",
    "In dN/dt = rN, r is the intrinsic rate of natural increase, an important parameter for assessing the impact "
    "of any biotic or abiotic factor on population growth. NCERT gives r = 0.015 for the Norway rat and 0.12 for "
    "the flour beetle; in 1981, r for the human population in India was 0.0205.",
    ["Statement I: true", "Statement II: true"],
    C12_OP("population growth: exponential growth"),
    seconds=30)

add(OAP, "Population interactions", "Advanced", "assertion_reason",
    ar("When all the starfish Pisaster were removed from an enclosed intertidal area of the American Pacific Coast, "
       "more than 10 species of invertebrates became extinct within a year.",
       "In the absence of the predator, interspecific competition among the prey species increased."),
    AR("A"),
    "Role of predators in maintaining diversity",
    "In the rocky intertidal communities of the American Pacific Coast, Pisaster is an important predator. When it "
    "was removed experimentally, more than 10 invertebrate species became extinct within a year because of "
    "interspecific competition. Predators reduce the intensity of competition among prey; without them, superior "
    "competitors eliminate others. R explains A.",
    ["A: true (field experiment)", "R: true", "Loss of predator → stronger competition → extinctions → A"],
    C12_OP("population interactions: predation"),
    seconds=45)

add(OAP, "Population growth", "Advanced", "multi_statement",
    ms("Which of the following statements about population growth are correct?",
       ["Exponential growth can be written in integral form as Nₜ = N₀e^(rt), where e is the base of natural "
        "logarithms (2.71828).",
        "Population density depends on four basic processes, of which natality and immigration increase it.",
        "Under normal conditions, births and deaths are the most important factors influencing population density.",
        "When resources in the habitat are unlimited, a population grows in a logistic fashion.",
        "In nature, a habitat has unlimited resources and supports exponential growth indefinitely."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "C"),
    "Population growth",
    "Population density changes through natality and immigration (which increase it) and mortality and emigration "
    "(which decrease it); normally births and deaths matter most. With unlimited resources a population grows "
    "exponentially, Nₜ = N₀e^(rt). In nature resources are finite, so no population can grow exponentially "
    "indefinitely; growth is logistic and levels off at the carrying capacity.",
    ["(a) True", "(b) True", "(c) True", "(d) False: unlimited resources give exponential growth",
     "(e) False: resources in nature are finite"],
    C12_OP("population growth"),
    why="Options A, B and D include (d) or (e), or leave out a true statement.",
    seconds=50)

add(OAP, "Population growth", "Advanced", "direct",
    "Under normal conditions, births and deaths are the most important factors influencing population density. When "
    "a new habitat is just being colonised, however, which factor may contribute more significantly to population "
    "growth than birth rates?",
    P("Immigration", ["Mortality", "Emigration", "Natality"], "D"),
    "Factors affecting population density",
    "Of the four processes that change population density, natality and mortality are the most important under "
    "normal conditions. Immigration and emigration assume importance only under special conditions: for instance, "
    "when a new habitat is just being colonised, immigration may contribute more significantly to population growth "
    "than birth rates.",
    ["Normal conditions → births and deaths dominate", "Newly colonised habitat → immigration may dominate"],
    C12_OP("population growth"),
    why="Natality is the birth rate itself, which the question compares against. Mortality and emigration decrease "
        "population density.",
    seconds=35)

add(OAP, "Population growth", "Advanced", "assertion_reason",
    ar("A population growing exponentially gives a J-shaped curve when its size N is plotted against time.",
       "In exponential growth, the per capita growth rate decreases as the population size N approaches the "
       "carrying capacity K."),
    AR("C"),
    "Exponential versus logistic growth",
    "With unlimited resources, a population grows exponentially (dN/dt = rN) and a plot of N against time gives a "
    "J-shaped curve; the per capita growth rate r stays constant. A growth rate that slows as N approaches the "
    "carrying capacity K is the feature of logistic growth, dN/dt = rN[(K − N)/K]. A is true; R is false.",
    ["A: true", "R: false, slowing near K is a feature of logistic growth; r is constant in exponential growth"],
    C12_OP("population growth: growth models"),
    seconds=40)


# ================================================================ Ecosystem (4 / 5 / 4)
C12_EC = lambda s: ref(12, ECO, s)

# NPP = GPP - R; GPP 25,000 kJ m^-2 yr^-1, respiration 40 % of GPP
GPP = 25000
R_loss = GPP * F(40, 100)
assert GPP - R_loss == 15000
assert R_loss == 10000 and GPP + R_loss == 35000 and GPP * F(10, 100) == 2500    # distractors

add(ECO, "Structure and components", "Basic", "direct",
    "The identification and enumeration of the plant and animal species of an ecosystem gives its:",
    P("Species composition", ["Stratification", "Standing crop", "Net primary productivity"], "D"),
    "Ecosystem structure",
    "The interaction of biotic and abiotic components results in a physical structure characteristic of each type "
    "of ecosystem. Identification and enumeration of the plant and animal species of an ecosystem gives its species "
    "composition; the vertical distribution of species at different levels is called stratification.",
    ["Listing and counting species → species composition"],
    C12_EC("ecosystem: structure and function"),
    why="Stratification is the vertical layering of species. Standing crop is the living mass at a trophic level. "
        "NPP is a rate of biomass production; none of these is obtained by listing species.",
    seconds=20)

add(ECO, "Ecological pyramids", "Basic", "direct",
    "The biomass of a species at a trophic level can be expressed in terms of fresh weight or dry weight. According to "
    "NCERT, which of these is the more accurate measure?",
    P("Dry weight", ["Fresh weight", "Both are equally accurate", "Neither; biomass can only be expressed as number "
                                                                    "of individuals"], "B"),
    "Measurement of biomass",
    "The standing crop of a trophic level is measured as the biomass of living organisms or as their number in a "
    "unit area. Biomass is expressed as fresh or dry weight; measurement in terms of dry weight is more accurate.",
    ["Biomass: fresh or dry weight", "Dry weight → more accurate"],
    C12_EC("energy flow: standing crop and biomass"),
    why="Fresh weight varies with the water content of the organisms, which is why NCERT calls dry weight the more "
        "accurate measure; biomass is not limited to counts of individuals.",
    seconds=20)

add(ECO, "Structure and components", "Basic", "direct",
    "Which of the following is an aquatic ecosystem?",
    P("Estuary", ["Forest", "Grassland", "Desert"], "D"),
    "Types of ecosystems",
    "Ecosystems are broadly terrestrial or aquatic. Forest, grassland and desert are terrestrial ecosystems; pond, "
    "lake, wetland, river and estuary are aquatic ecosystems. Crop fields and an aquarium may be considered "
    "man-made ecosystems.",
    ["Terrestrial: forest, grassland, desert", "Aquatic: pond, lake, wetland, river, estuary"],
    C12_EC("ecosystem"),
    why="Forest, grassland and desert are the terrestrial examples given by NCERT.",
    seconds=20)

add(ECO, "Energy flow", "Basic", "statement_pair",
    sp("In a terrestrial ecosystem, the major producers are herbaceous and woody plants.",
       "All organisms in an ecosystem depend for their food on producers, either directly or indirectly."),
    SP("A"),
    "Producers",
    "Producers are autotrophs that fix solar energy into food. In terrestrial ecosystems the major producers are "
    "herbaceous and woody plants; in aquatic ecosystems they are phytoplankton, algae and higher plants. All "
    "organisms depend on producers for food, directly (herbivores) or indirectly (carnivores and decomposers).",
    ["Statement I: true", "Statement II: true"],
    C12_EC("energy flow"),
    seconds=25)

add(ECO, "Productivity and decomposition", "Intermediate", "numerical",
    "The gross primary productivity of a grassland is 25,000 kJ m⁻² yr⁻¹, and the producers use 40 per cent of it "
    "in respiration. What is the net primary productivity of the grassland?",
    P("15,000 kJ m⁻² yr⁻¹", ["10,000 kJ m⁻² yr⁻¹", "35,000 kJ m⁻² yr⁻¹", "2,500 kJ m⁻² yr⁻¹"], "D"),
    "Gross and net primary productivity",
    "Net primary productivity is the gross primary productivity minus respiration losses (R) of the producers: "
    "NPP = GPP − R. R = 40% of 25,000 = 10,000 kJ m⁻² yr⁻¹, so NPP = 25,000 − 10,000 = 15,000 kJ m⁻² yr⁻¹. NPP is "
    "the biomass available for consumption by heterotrophs.",
    ["R = 0.40 × 25,000 = 10,000", "NPP = GPP − R = 15,000 kJ m⁻² yr⁻¹"],
    C12_EC("productivity"),
    why="10,000 is the respiratory loss, not NPP. 35,000 adds respiration instead of subtracting it. 2,500 wrongly "
        "applies the 10 per cent law, which concerns transfer between trophic levels.",
    seconds=40, verified_by=RECOMPUTED)

add(ECO, "Structure and components", "Intermediate", "match_list",
    ml(("component of a pond ecosystem", "description"),
       ["Abiotic component", "Autotrophs", "Consumers", "Decomposers"],
       ["Fungi, bacteria and flagellates, especially abundant at the bottom of the pond",
        "Water with dissolved inorganic and organic substances, and the rich soil deposit at the bottom",
        "Convert inorganic material into organic material with the help of the radiant energy of the sun",
        "Zooplankton, and free-swimming and bottom-dwelling animals"]),
    M({"A": "II", "B": "III", "C": "IV", "D": "I"},
      [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
       {"A": "II", "B": "IV", "C": "III", "D": "I"}], "B"),
    "The pond as an ecosystem",
    "A pond is a shallow water body in which all the basic components of an ecosystem are well exhibited. The "
    "abiotic component is the water with dissolved inorganic and organic substances and the rich soil deposit at "
    "the bottom. Autotrophs (phytoplankton, some algae and floating, submerged and marginal plants) convert "
    "inorganic into organic material using solar energy. Consumers are zooplankton and free-swimming and bottom "
    "forms. Decomposers are fungi, bacteria and flagellates, especially abundant at the bottom.",
    ["Abiotic → water, dissolved substances, soil deposit (A-II)", "Autotrophs → solar energy to organic matter "
     "(B-III)", "Consumers → zooplankton and animals (C-IV)", "Decomposers → fungi, bacteria, flagellates (D-I)"],
    C12_EC("ecosystem: structure and function (pond)"),
    why="The wrong codes swap the abiotic component with the autotrophs, the consumers with the decomposers, or the "
        "autotrophs with the consumers.",
    seconds=45)

add(ECO, "Productivity and decomposition", "Intermediate", "assertion_reason",
    ar("Humus serves as a reservoir of nutrients.",
       "Humus is colloidal in nature."),
    AR("A"),
    "Humus",
    "Humification leads to the accumulation of humus, a dark-coloured amorphous substance that is highly resistant "
    "to microbial action and decomposes at an extremely slow rate. NCERT states that, being colloidal in nature, it "
    "serves as a reservoir of nutrients. R gives the reason for A.",
    ["A: true", "R: true", "NCERT: 'being colloidal in nature it serves as a reservoir of nutrients' → R explains A"],
    C12_EC("decomposition"),
    seconds=30)

add(ECO, "Ecological pyramids", "Intermediate", "multi_statement",
    ms("Which of the following statements about trophic levels are correct?",
       ["A trophic level represents a functional level, not a species as such.",
        "Herbivores are primary consumers; the consumers that feed on herbivores are primary carnivores (secondary "
        "consumers).",
        "The standing crop of a trophic level is measured as the biomass of living organisms or their number in a "
        "unit area.",
        "The number of trophic levels in a grazing food chain is unlimited.",
        "Primary carnivores are also called primary consumers."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Trophic levels and standing crop",
    "Organisms occupy a place in the food chain called the trophic level. A trophic level is a functional level, "
    "not a species. Herbivores are primary consumers; animals eating them are primary carnivores, i.e. secondary "
    "consumers. The standing crop is measured as biomass or number per unit area. Because only about 10% of energy "
    "passes to the next level, the number of trophic levels in a grazing food chain is restricted.",
    ["(a) True", "(b) True", "(c) True", "(d) False: the number of trophic levels is restricted",
     "(e) False: primary carnivores are secondary consumers"],
    C12_EC("energy flow; ecological pyramids"),
    why="Options A, B and C include (d) or (e), or leave out (a).",
    seconds=45)

add(ECO, "Ecological pyramids", "Intermediate", "statement_pair",
    sp("In ecological pyramids, the base is always formed by the producers and the apex by the top-level consumers.",
       "Ecological pyramids take into account a species that belongs to two or more trophic levels."),
    SP("C"),
    "Ecological pyramids and their limitations",
    "The base of each pyramid represents the producers (first trophic level) and the apex the tertiary or top-level "
    "consumers. Among the limitations of ecological pyramids, NCERT notes that they do not take into account the "
    "same species belonging to two or more trophic levels.",
    ["Statement I: true", "Statement II: false, this is a limitation of ecological pyramids"],
    C12_EC("ecological pyramids"),
    seconds=30)

add(ECO, "Ecological pyramids", "Advanced", "assertion_reason",
    ar("The pyramid of numbers in a grassland ecosystem is upright.",
       "In a grassland, the producers (about 58 lakh in NCERT's example) far outnumber the herbivores, which in turn "
       "far outnumber the carnivores."),
    AR("A"),
    "Pyramid of numbers in a grassland",
    "In NCERT's grassland pyramid of numbers, about 58 lakh producers support far fewer primary consumers, still "
    "fewer secondary consumers and only a handful of tertiary consumers. Because the number of individuals falls steeply at each "
    "higher trophic level, the pyramid is broad at the base and narrow at the top, i.e. upright. R explains A.",
    ["Producers ≫ herbivores ≫ carnivores", "Numbers shrink upward → upright pyramid → R explains A"],
    C12_EC("ecological pyramids: pyramid of numbers"),
    seconds=40)

add(ECO, "Productivity and decomposition", "Advanced", "multi_statement",
    ms("Which of the following statements about productivity are correct?",
       ["Gross primary productivity of an ecosystem is the rate of production of organic matter during "
        "photosynthesis.",
        "A considerable amount of gross primary productivity is utilised by plants in respiration.",
        "Net primary productivity is the biomass available for consumption by heterotrophs, i.e. herbivores and "
        "decomposers.",
        "Net primary productivity is the energy fixed by the consumers per unit time.",
        "The amount of biomass produced per unit area over a time period by plants during photosynthesis is called "
        "the standing crop."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Primary production and productivity",
    "Primary production is the amount of biomass or organic matter produced per unit area over a time period by "
    "plants during photosynthesis. GPP is the rate of production of organic matter during photosynthesis; a "
    "considerable part of it is used in plant respiration. GPP minus respiration losses is NPP, the biomass "
    "available to heterotrophs (herbivores and decomposers). The standing crop is the living mass present at a "
    "trophic level at a given time.",
    ["(a) True", "(b) True", "(c) True", "(d) False: NPP refers to producers, not consumers",
     "(e) False: that is primary production, not standing crop"],
    C12_EC("productivity"),
    why="Options A, B and C include (d) or (e), or leave out (a).",
    seconds=50)

add(ECO, "Energy flow", "Advanced", "direct",
    "A person eats rice and also eats a fish. The fish fed on zooplankton, which fed on phytoplankton. In these two "
    "food chains, the person occupies the trophic levels of:",
    P("Primary consumer and tertiary consumer at the same time",
      ["Only the secondary consumer", "Only the tertiary consumer", "Primary consumer and secondary consumer at the "
                                                                    "same time"], "B"),
    "One species, several trophic levels",
    "Rice is a producer, so in the chain rice → person the person is a primary consumer. In the chain phytoplankton "
    "→ zooplankton → fish → person, the person is a tertiary consumer (fourth trophic level). A given species may "
    "occupy more than one trophic level in the same ecosystem at the same time.",
    ["Rice → person: primary consumer", "Phytoplankton → zooplankton → fish → person: tertiary consumer",
     "Both at once"],
    C12_EC("energy flow; ecological pyramids"),
    why="'Only' options ignore one of the two chains. The fish is the secondary consumer, so the person eating it "
        "is tertiary, not secondary.",
    seconds=50)

add(ECO, "Structure and components", "Advanced", "statement_pair",
    sp("In a pond, the decomposition and mineralisation of dead organic matter release nutrients back for reuse by "
       "the autotrophs.",
       "In a pond, the radiant energy of the sun is converted into chemical energy when the heterotrophs consume the "
       "autotrophs."),
    SP("C"),
    "Functions of a pond ecosystem",
    "A pond performs all the functions of an ecosystem: autotrophs convert inorganic into organic material using "
    "the radiant energy of the sun; heterotrophs consume the autotrophs; and dead organic matter is decomposed and "
    "mineralised to release nutrients for reuse by the autotrophs. Energy moves in one direction towards the higher "
    "trophic levels and is lost as heat. Conversion of radiant energy is done by the autotrophs, not by the "
    "heterotrophs.",
    ["Statement I: true", "Statement II: false, autotrophs convert solar energy; heterotrophs only consume them"],
    C12_EC("ecosystem: structure and function (pond)"),
    seconds=40)


# ================================================================ Biodiversity and Conservation (4 / 5 / 4)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Importance and loss", "Basic", "direct",
    "The four major causes of the accelerated loss of biodiversity, namely habitat loss and fragmentation, "
    "over-exploitation, alien species invasions and co-extinctions, are together described as:",
    P("The Evil Quartet", ["The sixth extinction", "The rivet popper hypothesis", "The species-area relationship"],
      "D"),
    "Causes of biodiversity losses",
    "NCERT names four major causes of the accelerated rates of species extinctions: habitat loss and fragmentation, "
    "over-exploitation, alien species invasions and co-extinctions. Together they are called 'The Evil Quartet'.",
    ["Four causes → 'The Evil Quartet'"],
    C12_BD("loss of biodiversity: causes"),
    why="The sixth extinction is the present episode of mass extinction. The rivet popper hypothesis (Paul Ehrlich) "
        "is an analogy for species in ecosystems. The species-area relationship describes how species richness "
        "varies with area.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "According to the ethical argument for conserving biodiversity, besides realising that every species has an "
    "intrinsic value, NCERT says that we have a moral duty to:",
    P("Care for the well-being of all species and pass on our biological legacy in good order to future "
      "generations",
      ["Conserve only those species that are of current economic value to us",
       "Explore molecular, genetic and species-level diversity for products of economic importance",
       "Protect only the species that provide ecosystem services such as pollination"], "B"),
    "Ethical argument for conserving biodiversity",
    "The ethical argument relates to what we owe to the millions of plant, animal and microbe species with whom we "
    "share this planet. Every species has an intrinsic value, even if it may not be of current economic value to "
    "us, and we have a moral duty to care for their well-being and pass on our biological legacy in good order to "
    "future generations.",
    ["Ethical argument: intrinsic value of every species → moral duty to care for all species and hand on the "
     "biological legacy"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity"),
    why="Conserving only economically useful species contradicts the ethical argument. Exploring diversity for "
        "products of economic importance is bioprospecting (narrowly utilitarian). Ecosystem services such as "
        "pollination belong to the broadly utilitarian argument.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "Among recent extinctions, NCERT lists three subspecies of tiger. They are:",
    P("Bali, Javan and Caspian", ["Bengal, Javan and Caspian", "Bali, Siberian and Sumatran",
                                  "Bengal, Siberian and Caspian"], "D"),
    "Recent extinctions",
    "Examples of recent extinctions given by NCERT include the dodo (Mauritius), quagga (Africa), thylacine "
    "(Australia), Steller's sea cow (Russia) and three subspecies of tiger: Bali, Javan and Caspian.",
    ["Extinct tiger subspecies: Bali, Javan, Caspian"],
    C12_BD("loss of biodiversity"),
    why="The Bengal, Siberian and Sumatran tigers are not among the extinct subspecies listed by NCERT.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Basic", "statement_pair",
    sp("Greenland, at 71° N, has only 56 species of birds, whereas New York, at 41° N, has 105 species.",
       "India, with much of its land area in the tropical latitudes, has more than 1,200 species of birds."),
    SP("A"),
    "Latitudinal gradients",
    "Species diversity generally decreases from the equator towards the poles. NCERT's bird example: Colombia near "
    "the equator has nearly 1,400 species, New York (41° N) 105 species and Greenland (71° N) only 56 species. "
    "India, with much of its land area in the tropical latitudes, has more than 1,200 species of birds.",
    ["Statement I: true", "Statement II: true"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Intermediate", "multi_statement",
    ms("Which of the following statements about global species diversity are correct?",
       ["The number of fungi species in the world is more than the combined total of the species of fishes, "
        "amphibians, reptiles and mammals.",
        "Global estimates of species diversity do not give any figures for prokaryotes.",
        "Conventional taxonomic methods are not suitable for identifying microbial species, and many species are "
        "simply not culturable under laboratory conditions.",
        "The diversity of prokaryotes has been fully documented.",
        "The total number of species described so far is slightly more than 15 million."]),
    P("(a), (b) and (c) only",
      ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], "D"),
    "Global species diversity",
    "According to the IUCN (2004), slightly more than 1.5 million plant and animal species have been described so "
    "far. The number of fungi species exceeds the combined species of fishes, amphibians, reptiles and mammals. "
    "Estimates give no figures for prokaryotes, because conventional taxonomic methods do not suit microbes and many "
    "are not culturable in the laboratory; their diversity could run into millions.",
    ["(a) True", "(b) True", "(c) True", "(d) False: prokaryote diversity is not known",
     "(e) False: about 1.5 million species have been described"],
    C12_BD("biodiversity: how many species are there on earth"),
    why="Options A, B and C include (d) or (e), or leave out (a).",
    seconds=50)

add(BDC, "Patterns of biodiversity", "Intermediate", "match_list",
    ml(("group in the Amazonian rain forest", "approximate number of species given by NCERT"),
       ["Plants", "Fishes", "Birds", "Invertebrates"],
       ["1,300", "More than 1,25,000", "40,000", "3,000"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Species richness of the Amazon",
    "The largely tropical Amazonian rain forest in South America has the greatest biodiversity on earth. NCERT "
    "notes that it is home to more than 40,000 species of plants, 3,000 of fishes, 1,300 of birds, 427 of mammals, "
    "427 of amphibians, 378 of reptiles and more than 1,25,000 invertebrates.",
    ["Plants → 40,000 (A-III)", "Fishes → 3,000 (B-IV)", "Birds → 1,300 (C-I)", "Invertebrates → > 1,25,000 (D-II)"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    why="The wrong codes swap plants with invertebrates, fishes with birds, or birds with invertebrates.",
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "assertion_reason",
    ar("Tropical rain forests, which once covered more than 14 per cent of the earth's land surface, now cover no "
       "more than 6 per cent.",
       "Many marine fish populations around the world are over-harvested, endangering the continued existence of "
       "some commercially important species."),
    AR("B"),
    "Habitat loss and over-exploitation",
    "Both statements are NCERT examples of causes of biodiversity loss. A is an example of habitat loss: tropical "
    "rain forests have shrunk from over 14% to no more than 6% of the land surface. R is an example of "
    "over-exploitation of marine fish. Over-harvesting of fish does not explain the shrinking of rain forests, so R "
    "is not the explanation of A.",
    ["A: true (habitat loss)", "R: true (over-exploitation)", "Different causes → B"],
    C12_BD("loss of biodiversity: causes"),
    seconds=35)

add(BDC, "Importance and loss", "Intermediate", "statement_pair",
    sp("Ecologists believe that communities with more species generally tend to be more stable than those with fewer "
       "species.",
       "A stable community should show a great deal of variation in productivity from year to year."),
    SP("C"),
    "Biodiversity and ecosystem stability",
    "Ecologists believe that communities with more species tend to be more stable. A stable community should not "
    "show too much variation in productivity from year to year; it must be either resistant or resilient to "
    "occasional disturbances (natural or man-made) and resistant to invasions by alien species.",
    ["Statement I: true", "Statement II: false, a stable community shows little year-to-year variation"],
    C12_BD("biodiversity and ecosystem stability"),
    seconds=30)

add(BDC, "Hotspots and Red Data Book", "Intermediate", "match_list",
    ml(("group", "percentage of its species facing the threat of extinction, as given by NCERT"),
       ["Birds", "Mammals", "Amphibians", "Gymnosperms"],
       ["12 per cent", "23 per cent", "32 per cent", "31 per cent"]),
    M({"A": "I", "B": "II", "C": "III", "D": "IV"},
      [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "I", "B": "II", "C": "IV", "D": "III"},
       {"A": "I", "B": "III", "C": "II", "D": "IV"}], "A"),
    "Threatened species",
    "More than 15,500 species world-wide are facing the threat of extinction. NCERT gives the present figures: "
    "12 per cent of all bird species, 23 per cent of all mammal species, 32 per cent of all amphibian species and "
    "31 per cent of all gymnosperm species in the world face the threat of extinction.",
    ["Birds → 12% (A-I)", "Mammals → 23% (B-II)", "Amphibians → 32% (C-III)", "Gymnosperms → 31% (D-IV)"],
    C12_BD("loss of biodiversity"),
    why="The wrong codes swap birds with mammals, amphibians with gymnosperms, or mammals with amphibians.",
    seconds=40)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Which of the following statements about the effects of biodiversity loss and ecosystem stability are "
       "correct?",
       ["Loss of biodiversity in a region may lead to a decline in plant production.",
        "Loss of biodiversity in a region increases the resistance of the ecosystem to environmental perturbations "
        "such as drought.",
        "Loss of biodiversity may increase the variability in certain ecosystem processes such as plant "
        "productivity, water use, and pest and disease cycles.",
        "Loss of biodiversity does not affect any ecosystem process.",
        "A stable community is either resistant or resilient to occasional disturbance and is resistant to "
        "invasions by alien species."]),
    P("(a), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"], "D"),
    "Effects of loss of biodiversity",
    "NCERT states that loss of biodiversity in a region may lead to (a) a decline in plant production, (b) lowered "
    "resistance to environmental perturbations such as drought, and (c) increased variability in certain ecosystem "
    "processes such as plant productivity, water use, and pest and disease cycles. A stable community is resistant "
    "or resilient to occasional disturbance and resistant to invasions by alien species.",
    ["(a) True", "(b) False: resistance is lowered", "(c) True",
     "(d) False: ecosystem processes are affected", "(e) True"],
    C12_BD("loss of biodiversity; biodiversity and ecosystem stability"),
    why="Options A, B and C include (b) or (d).",
    seconds=50)

add(BDC, "Patterns of biodiversity", "Advanced", "statement_pair",
    sp("More solar energy is available in the tropics, which contributes to higher productivity and might, in turn, "
       "contribute indirectly to greater diversity.",
       "Unlike the tropics, temperate regions have remained relatively undisturbed by glaciations for millions of "
       "years, giving them a long evolutionary time for species diversification."),
    SP("C"),
    "Why the tropics are more diverse",
    "NCERT gives several hypotheses: speciation is generally a function of time, and unlike temperate regions, which "
    "were subjected to frequent glaciations in the past, tropical latitudes have remained relatively undisturbed for "
    "millions of years, giving a long evolutionary time for diversification; tropical environments are less "
    "seasonal and more predictable; and more solar energy in the tropics gives higher productivity, which might "
    "indirectly contribute to greater diversity. Statement II reverses the roles of the tropical and temperate "
    "regions.",
    ["Statement I: true", "Statement II: false, it is the tropics that remained undisturbed; temperate regions "
     "faced frequent glaciations"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    seconds=40)

add(BDC, "Hotspots and Red Data Book", "Advanced", "match_list",
    ml(("item from the IUCN Red List and NCERT", "number"),
       ["Vertebrate species documented as extinct in the last 500 years (IUCN, 2004)",
        "Invertebrate species documented as extinct in the last 500 years (IUCN, 2004)",
        "Plant species documented as extinct in the last 500 years (IUCN, 2004)",
        "Species world-wide currently facing the threat of extinction"],
       ["87", "More than 15,500", "359", "338"]),
    M({"A": "IV", "B": "III", "C": "I", "D": "II"},
      [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "I", "C": "III", "D": "II"},
       {"A": "I", "B": "III", "C": "IV", "D": "II"}], "B"),
    "Recorded extinctions and threatened species",
    "The IUCN Red List (2004) documents the extinction of 784 species in the last 500 years: 338 vertebrates, "
    "359 invertebrates and 87 plants. More than 15,500 species world-wide currently face the threat of extinction.",
    ["Vertebrates → 338 (A-IV)", "Invertebrates → 359 (B-III)", "Plants → 87 (C-I)", "Threatened → > 15,500 (D-II)"],
    C12_BD("loss of biodiversity"),
    shortcut="338 + 359 + 87 = 784, the total recorded extinctions.",
    why="The commonest error swaps the two close numbers 338 and 359 between vertebrates and invertebrates; the "
        "other codes give plants a vertebrate or invertebrate figure.",
    seconds=45, verified_by=RECOMPUTED)

add(BDC, "Hotspots and Red Data Book", "Advanced", "assertion_reason",
    ar("Strict protection of the biodiversity hotspots could reduce the ongoing mass extinctions by almost "
       "30 per cent.",
       "Biodiversity hotspots are regions with low species richness but a very high degree of endemism."),
    AR("C"),
    "Biodiversity hotspots",
    "Hotspots are regions with very high levels of species richness and a high degree of endemism. Although all "
    "the hotspots together cover less than 2 per cent of the earth's land area, they harbour so many species that "
    "their strict protection could reduce the ongoing mass extinctions by almost 30 per cent. A is true; R is false "
    "because hotspots have very high, not low, species richness.",
    ["A: true", "R: false, hotspots have very high species richness and high endemism"],
    C12_BD("biodiversity conservation: hotspots"),
    seconds=40)

assert 338 + 359 + 87 == 784


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
    assert len(QUESTIONS) == pkg["count"] == 128
    have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
    assert have == quota, {k: (have[k], quota[k]) for k in set(have) | set(quota) if have[k] != quota[k]}
    order = [q["topic"] for q in QUESTIONS]
    assert sorted(order, key=pkg["topics"].index) == order       # topics in plan order

    fmts = Counter(q["format"] for q in QUESTIONS)
    keys = Counter(q["correct_answer"] for q in QUESTIONS)
    n = len(QUESTIONS)
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "BATCH_003 package BOT_003_p2: 128 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000, "
                    "BATCH_001 and BATCH_002 were avoided. Numerical answers re-derived by "
                    "tools/batch_003/BOT_003_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
