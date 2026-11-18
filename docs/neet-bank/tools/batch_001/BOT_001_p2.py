"""Builder for BATCH_001, package BOT_001_p2 (Botany, NEET_BOT_000127..NEET_BOT_000250, 124 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Numerical answers are re-derived below; the file is written only if every assert,
the plan quota and the format mix pass.

    cd docs/neet-bank && python tools/batch_001/BOT_001_p2.py
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
TODAY = "2026-11-16"
LETTERS = "ABCD"
BOT = "Botany"
PACKAGE = "BOT_001_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_001_BOT_p2.json"
FIRST_ID = 127

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


# ---------------------------------------------------------------- verification of computable answers
# PGD: relative growth rate = absolute growth in unit time / size at the start of that time
P0, P1, Q0, Q1 = F(4), F(10), F(30), F(36)
assert P1 - P0 == Q1 - Q0 == 6                       # equal absolute growth rates
assert (P1 - P0) / P0 == F(3, 2) and (Q1 - Q0) / Q0 == F(1, 5)
assert round(float((P1 - P0) / P1), 2) == 0.6 and round(float((Q1 - Q0) / Q1), 2) == 0.17   # distractor: final size
assert (P1 / P0, Q1 / Q0) == (F(5, 2), F(6, 5))      # distractor: ratio of sizes

# PIV: colour blindness. Carrier mother (X^c X) x colour-blind father (X^c Y): daughters get X^c from father
daughters = [m + "c" for m in ("c", "+")]           # mother's X (c or +) with father's X^c
assert F(sum(1 for d in daughters if d == "cc"), len(daughters)) == F(1, 2)

# PIV: AaBBCc x aaBbCc, fraction dominant for all three traits
pA, pB, pC = F(1, 2), F(1), F(3, 4)                 # Aa x aa; BB x Bb; Cc x Cc
assert pA * pB * pC == F(3, 8)
assert F(1, 2) * F(3, 4) * F(3, 4) == F(9, 32)       # distractor: treats BB x Bb like Bb x Bb
assert F(1, 2) * F(1, 2) * F(3, 4) == F(3, 16)       # distractor: treats BB x Bb like Bb x bb

# PIV: polygenic, AaBbCc x AaBbCc, fraction with exactly three dominant (contributing) alleles out of six
assert F(math.comb(6, 3), 2 ** 6) == F(5, 16)
assert F(math.comb(6, 2), 64) == F(15, 64) and F(math.comb(6, 1), 64) == F(3, 32)

# MBI: hydrogen bonds in a 1000 bp duplex with 30 % guanine
bp, g_frac = 1000, F(3, 10)
G = 2 * bp * g_frac                                   # guanine bases = G-C pairs
AT = bp - G
assert (G, AT) == (600, 400) and 3 * G + 2 * AT == 2600
assert 3 * AT + 2 * G == 2400                         # distractor: bond numbers swapped

# MBI: coding stretch from AUG to the stop codon (both included) of 336 nucleotides
codons = 336 // 3
assert 336 % 3 == 0 and codons - 1 == 111

# OAP: 250 fruit flies, 50 births and 25 deaths in a week
N0, births, deaths = 250, 50, 25
assert (F(births, N0), F(deaths, N0)) == (F(1, 5), F(1, 10))
assert round(births / (N0 + births - deaths), 2) == 0.18 and round(deaths / (N0 + births - deaths), 2) == 0.09

# ECO: grass -> grasshopper -> frog -> snake -> hawk, 10 % transfer, grass fixes 1,00,000 J
energy = 100000
for _ in range(4):
    energy //= 10
assert energy == 10

# ================================================================ Plant Growth and Development (4 / 5 / 4)
C11_PGD = lambda s: ref(11, PGD, s)

add(PGD, "Germination and growth phases", "Basic", "direct",
    "In the growing region of a root or shoot, cells showing increased vacuolation, cell enlargement and new cell "
    "wall deposition belong to which phase of growth?",
    P("Phase of elongation", ["Meristematic phase", "Phase of maturation", "Phase of dedifferentiation"], "B"),
    "Phases of growth: meristematic, elongation and maturation",
    "Growth at a root or shoot apex passes through three phases. Meristematic cells divide constantly and have thin "
    "cellulosic walls, rich protoplasm and large nuclei. Cells just behind them elongate: they become vacuolated, "
    "enlarge and lay down new wall material. Further away, cells reach their maximum size and mature.",
    ["Meristematic phase: rich protoplasm, large conspicuous nuclei, thin primary walls",
     "Elongation phase: increased vacuolation, cell enlargement, new cell wall deposition",
     "Maturation phase: cells attain maximal size in wall thickening and protoplasmic modification"],
    C11_PGD("phases of growth"),
    why="Meristematic cells are dense and dividing, not vacuolated and enlarging. Maturation follows elongation. "
        "Dedifferentiation is regaining the ability to divide, not a phase of the growth zone.",
    seconds=30)

add(PGD, "Growth rate", "Basic", "direct",
    "Following mitotic division at the root apex, only one daughter cell continues to divide while the other "
    "differentiates and matures. Growth of this kind is called:",
    P("Arithmetic growth", ["Geometric growth", "Exponential growth", "Sigmoid growth of a cell population"], "C"),
    "Arithmetic and geometric growth",
    "In arithmetic growth one daughter cell keeps dividing and the other matures, so new cells are added at a "
    "constant rate. A root elongating at a constant rate is the NCERT example; length plotted against time gives a "
    "straight line (Lt = L0 + rt).",
    ["One daughter cell divides, the other matures → constant rate of addition",
     "Constant rate → arithmetic growth, a linear curve"],
    C11_PGD("growth rates: arithmetic growth"),
    why="In geometric (exponential) growth both daughter cells keep dividing; a cell population grown in limited "
        "nutrients then gives a sigmoid curve.",
    seconds=30)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "The cytokinin first discovered as a modified form of adenine in autoclaved herring sperm DNA was named:",
    P("Kinetin", ["Zeatin", "Gibberellic acid", "Indole-3-acetic acid"], "A"),
    "Discovery of cytokinins",
    "Skoog and his co-workers found that DNA, among other materials, promoted callus growth. Skoog and Miller then "
    "identified and crystallised the active substance that promotes cytokinesis and called it kinetin. It is a "
    "modified adenine (a purine) from autoclaved herring sperm DNA. Zeatin is a natural cytokinin later isolated "
    "from corn kernels and coconut milk.",
    ["Promotes cytokinesis → cytokinin", "Isolated from autoclaved herring sperm DNA → kinetin"],
    C11_PGD("cytokinins"),
    why="Zeatin came from corn kernels and coconut milk. Gibberellic acid and IAA are not adenine derivatives.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "2,4-D is widely used by gardeners and farmers to:",
    P("Kill dicotyledonous weeds without affecting mature monocotyledonous plants",
      ["Promote female flowers in cucumbers", "Increase the yield of sugarcane by lengthening its stem",
       "Close stomata during water stress"], "D"),
    "Auxins as herbicides",
    "2,4-D (2,4-dichlorophenoxyacetic acid) is a synthetic auxin. It is used as a weedicide to kill dicot weeds; "
    "it does not affect mature monocots, so lawns and cereal fields are cleared of broad-leaved weeds.",
    ["2,4-D is a synthetic auxin", "Use: herbicide against dicot weeds; mature monocots unaffected"],
    C11_PGD("auxins"),
    why="Female flowers in cucumber: ethylene (ethephon). Longer sugarcane stems: gibberellins. Stomatal closure: "
        "abscisic acid.",
    seconds=25)

add(PGD, "Differentiation and redifferentiation", "Intermediate", "statement_pair",
    sp("Living differentiated plant cells that have lost the capacity to divide can regain it under certain "
       "conditions; this phenomenon is called dedifferentiation.",
       "To form a tracheary element, a cell loses its protoplasm and develops a strong, elastic, lignocellulosic "
       "secondary cell wall."),
    SP("A"),
    "Differentiation, dedifferentiation and redifferentiation",
    "Cells from the apical meristems and cambium differentiate and mature to perform specific functions; tracheary "
    "elements lose their protoplasm and build lignocellulosic secondary walls to carry water. Differentiated cells "
    "can regain the ability to divide (dedifferentiation), as when interfascicular cambium and cork cambium form "
    "from fully differentiated parenchyma.",
    ["Statement I: definition of dedifferentiation → true",
     "Statement II: NCERT's example of differentiation (tracheary element) → true"],
    C11_PGD("differentiation, dedifferentiation and redifferentiation"),
    seconds=40)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Spraying a sugarcane crop with gibberellins can increase its yield.",
       "Gibberellins increase the length of the sugarcane stem, which stores carbohydrate as sugar."),
    AR("A"),
    "Gibberellins and stem elongation",
    "Sugarcane stores sugar in its stem. Gibberellins cause stem (internode) elongation, so a longer stem holds "
    "more sugar; NCERT states the yield can rise by as much as 20 tonnes per acre. R is true and is exactly why A "
    "is true.",
    ["A: true, gibberellins raise sugarcane yield", "R: true, GA lengthens the stem that stores sugar",
     "Longer stem → more stored sugar → R explains A"],
    C11_PGD("gibberellins"),
    seconds=40)

add(PGD, "Plant growth regulators", "Intermediate", "match_list",
    ml(("observation", "worker"),
       ["Bending of canary grass coleoptiles towards unilateral light",
        "Isolation of auxin from the tips of oat coleoptiles",
        "'Bakanae' (foolish seedling) disease of rice seedlings caused by a fungus",
        "A volatile substance from ripened oranges hastened ripening of stored unripe bananas"],
       ["Cousins", "Charles Darwin and Francis Darwin", "E. Kurosawa", "F.W. Went"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "II", "B": "III", "C": "IV", "D": "I"}], "C"),
    "Discovery of plant growth regulators",
    "Each PGR was discovered through a separate observation.",
    ["Darwins: coleoptiles of canary grass bend towards light (phototropism) → A-II",
     "F.W. Went: isolated auxin from tips of oat (Avena) coleoptiles → B-IV",
     "E. Kurosawa: bakanae disease of rice caused by Gibberella fujikuroi; active substance gibberellic acid → C-III",
     "Cousins: volatile substance (later ethylene) from ripened oranges → D-I"],
    C11_PGD("discovery of plant growth regulators"),
    seconds=45)

add(PGD, "Plant growth regulators", "Intermediate", "multi_statement",
    ms("Which of the following are effects of ethylene on plants?",
       ["It promotes apical hook formation in dicot seedlings.",
        "It breaks seed and bud dormancy and initiates germination in peanut seeds.",
        "It promotes rapid internode or petiole elongation in deep-water rice plants.",
        "It inhibits root growth and the formation of root hairs.",
        "It promotes female flowers in cucumbers, thereby increasing the yield."]),
    P("(a), (b), (c) and (e) only",
      ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c), (d) and (e) only"], "B"),
    "Physiological effects of ethylene",
    "Ethylene is a gaseous PGR with many effects: horizontal growth of seedlings, swelling of the axis and apical "
    "hook formation in dicot seedlings, breaking of seed and bud dormancy (peanut germination, potato sprouting), "
    "internode elongation in deep-water rice, and more female flowers in cucumber. It promotes, not inhibits, root "
    "growth and root hair formation, which increases the absorption surface.",
    ["(a) True", "(b) True", "(c) True: keeps leaves and upper parts above water",
     "(d) False: ethylene promotes root growth and root hair formation", "(e) True"],
    C11_PGD("ethylene"),
    why="Every option except B includes (d), which reverses an NCERT statement.",
    seconds=55)

add(PGD, "Growth rate", "Intermediate", "numerical",
    "In one day, leaf P grows from 4 cm² to 10 cm² and leaf Q grows from 30 cm² to 36 cm². The relative growth "
    "rates (per day) of P and Q are respectively:",
    P("1.5 and 0.2", ["6 and 6", "0.6 and 0.17", "2.5 and 1.2"], "A"),
    "Absolute and relative growth rates",
    "Absolute growth rate is the total growth per unit time. Relative growth rate is the growth per unit time "
    "per unit initial size. Two leaves can have the same absolute growth rate but very different relative growth "
    "rates.",
    ["Absolute growth: P = 10 − 4 = 6 cm²/day; Q = 36 − 30 = 6 cm²/day (equal)",
     "Relative growth rate of P = 6/4 = 1.5 per day",
     "Relative growth rate of Q = 6/30 = 0.2 per day"],
    C11_PGD("growth rates"),
    shortcut="The smaller leaf with the same absolute gain always has the higher relative growth rate.",
    why="6 and 6 are the absolute growth rates. 0.6 and 0.17 divide by the final size instead of the initial size. "
        "2.5 and 1.2 are ratios of final to initial size, not growth per unit size.",
    seconds=60, verified_by=RECOMPUTED)

add(PGD, "Growth rate", "Advanced", "direct",
    "Geometric growth is expressed as W₁ = W₀e^(rt). In this equation, r is best described as the:",
    P("Relative growth rate, which is also a measure of the plant's ability to produce new plant material "
      "(efficiency index)",
      ["Absolute growth rate, i.e. the total increase in size per unit time",
       "Constant amount of growth added per unit time, as in a root elongating at a steady rate",
       "Size of the plant at the end of the growth period"], "D"),
    "Exponential (geometric) growth equation",
    "In W₁ = W₀e^(rt), W₁ is the final size, W₀ the initial size, t the time of growth and e the base of natural "
    "logarithms. r is the relative growth rate and also measures the ability of the plant to produce new plant "
    "material, referred to as the efficiency index. Final size therefore depends on initial size.",
    ["Identify each symbol: W₀ initial size, W₁ final size, t time",
     "r multiplies t inside the exponent → a rate per unit size → relative growth rate (efficiency index)"],
    C11_PGD("growth rates: geometric growth"),
    why="Absolute growth rate is total growth per unit time, not per unit size. A constant amount added per unit "
        "time is arithmetic growth (Lt = L0 + rt), where r is the elongation rate. Final size is W₁.",
    seconds=45)

add(PGD, "Plant growth regulators", "Advanced", "assertion_reason",
    ar("Auxins promote the abscission of older, mature leaves and fruits.",
       "Auxins are applied to induce parthenocarpy in tomatoes."),
    AR("B"),
    "Multiple, independent roles of auxin",
    "NCERT states that auxins help prevent fruit and leaf drop at early stages but promote the abscission of older, "
    "mature leaves and fruits, so A is true. Auxins also induce parthenocarpy, e.g. in tomatoes, so R is true. "
    "Fruit development without fertilisation has nothing to do with the shedding of old leaves and fruits, so R "
    "does not explain A.",
    ["A: true (abscission of older leaves and fruits)", "R: true (parthenocarpy in tomato)",
     "R describes a different use of auxin → not the explanation"],
    C11_PGD("auxins"),
    why="Option A is the trap: both statements are about auxin and both are true, but one does not cause the other. "
        "Students who remember that auxins prevent early fruit drop may wrongly mark A as false.",
    seconds=50)

add(PGD, "Differentiation and redifferentiation", "Advanced", "multi_statement",
    ms("Which of the following statements about development in plants are correct?",
       ["In cotton, coriander and larkspur, the leaves of the juvenile plant differ in shape from those of the "
        "mature plant.",
        "The different shapes of leaves produced in air and in water by buttercup are heterophylly caused by the "
        "environment.",
        "Growth in plants is closed: it stops once the plant reaches maturity.",
        "Formation of interfascicular cambium from fully differentiated parenchyma cells is an example of "
        "dedifferentiation.",
        "The final structure of a cell at maturity is also determined by the location of the cell within the "
        "tissue."]),
    P("(a), (b), (d) and (e) only",
      ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c), (d) and (e)"], "C"),
    "Plasticity, heterophylly and open differentiation",
    "Plants follow different pathways in response to environment or phase of life (plasticity). Heterophylly in "
    "cotton, coriander and larkspur is linked to the phase of life; in buttercup it is caused by the environment "
    "(air versus water). Plant growth is open: meristems keep adding cells throughout life, and differentiation is "
    "also open, since a cell's final form depends on its position.",
    ["(a) True: heterophylly with plant age", "(b) True: environmental heterophylly",
     "(c) False: plant growth is indeterminate (open)",
     "(d) True: NCERT's example of dedifferentiation", "(e) True: open differentiation"],
    C11_PGD("development; plasticity"),
    why="Every other option includes (c), the only false statement, or leaves out a true one.",
    seconds=70)

add(PGD, "Plant growth regulators", "Advanced", "statement_pair",
    sp("Spraying juvenile conifers with gibberellins hastens their maturity period, leading to early seed "
       "production.",
       "Cytokinins are synthesised mainly in regions of rapid cell division, such as root apices, developing shoot "
       "buds and young fruits, and they strengthen apical dominance."),
    SP("C"),
    "Gibberellins in forestry; cytokinins and apical dominance",
    "Gibberellins hasten maturity in juvenile conifers, so Statement I is true. Cytokinins are indeed made where "
    "cell division is rapid, but they help overcome apical dominance by promoting lateral shoot growth; apical "
    "dominance is caused by auxin from the apical bud. The last part makes Statement II false.",
    ["Statement I: true", "Statement II: first part true, but cytokinins overcome (not strengthen) apical "
     "dominance → false"],
    C11_PGD("gibberellins; cytokinins"),
    why="Statement II is a half-true trap: its first clause is correct, so a quick reader marks both true.",
    seconds=50)

# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "The innermost wall layer of a microsporangium, whose cells have dense cytoplasm and often more than one "
    "nucleus and which nourishes the developing pollen grains, is the:",
    P("Tapetum", ["Endothecium", "Middle layer", "Epidermis"], "D"),
    "Wall layers of the microsporangium",
    "A typical microsporangium is surrounded by four wall layers: epidermis, endothecium, middle layers and "
    "tapetum. The outer three protect the sporangium and help the anther dehisce. The innermost tapetum nourishes "
    "the developing pollen grains; its cells have dense cytoplasm and generally more than one nucleus.",
    ["Order from outside: epidermis → endothecium → middle layers → tapetum",
     "Nourishing layer = innermost = tapetum"],
    C12_SR("stamen, microsporangium and pollen grain"),
    why="Epidermis, endothecium and middle layers protect and help in dehiscence; they do not nourish pollen.",
    seconds=25)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "The exine of a pollen grain can withstand high temperatures and strong acids and alkalis, and no enzyme that "
    "degrades it is known. It is made of:",
    P("Sporopollenin", ["Cellulose and pectin", "Lignin", "Suberin"], "B"),
    "Structure of the pollen wall",
    "The hard outer layer (exine) is made of sporopollenin, one of the most resistant organic materials known. "
    "This is why pollen grains are well preserved as fossils. The inner wall (intine) is thin and continuous, made "
    "of cellulose and pectin.",
    ["Exine → sporopollenin (very resistant)", "Intine → cellulose and pectin"],
    C12_SR("pollen grain"),
    why="Cellulose and pectin form the intine, not the exine. Lignin and suberin are not the pollen-wall material "
        "NCERT names.",
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "A typical angiosperm embryo sac at maturity is:",
    P("8-nucleate and 7-celled", ["7-nucleate and 8-celled", "8-nucleate and 8-celled", "7-nucleate and 7-celled"],
      "A"),
    "Structure of the mature embryo sac",
    "Three successive free-nuclear mitotic divisions of the functional megaspore give 8 nuclei. Six of them are "
    "enclosed by walls as cells (3 at the micropylar end forming the egg apparatus, 3 antipodals at the chalazal "
    "end). The remaining 2 polar nuclei lie in one large central cell. So there are 8 nuclei but only 7 cells.",
    ["Egg apparatus: 2 synergids + 1 egg cell = 3 cells, 3 nuclei", "Antipodals: 3 cells, 3 nuclei",
     "Central cell: 1 cell with 2 polar nuclei", "Total: 7 cells, 8 nuclei"],
    C12_SR("the pistil, megasporangium (ovule) and embryo sac"),
    why="The central cell has two nuclei, so cells are one fewer than nuclei; options with 8 cells or 7 nuclei "
        "miss this.",
    seconds=25)

add(SRFP, "Pollination", "Basic", "direct",
    "Which of the following plants is pollinated by water?",
    P("Zostera", ["Water hyacinth", "Water lily", "Maize"], "C"),
    "Pollination by water (hydrophily)",
    "Hydrophily is rare and limited to about 30 genera, mostly monocots, e.g. Vallisneria, Hydrilla and the marine "
    "sea-grass Zostera. Not all aquatic plants use water: in water hyacinth and water lily the flowers emerge "
    "above the water and are pollinated by insects or wind.",
    ["Water-pollinated: Vallisneria, Hydrilla, Zostera",
     "Aquatic but insect- or wind-pollinated: water hyacinth, water lily", "Maize: wind-pollinated"],
    C12_SR("pollination: agents of pollination"),
    why="Water hyacinth and water lily are the usual trap: they grow in water but are not water-pollinated.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "direct",
    "The 'coconut water' of a tender coconut is:",
    P("Free-nuclear endosperm made up of thousands of nuclei",
      ["Cellular endosperm", "Perisperm, the remnant of the nucellus", "Fluid stored in the cotyledon of the embryo"],
      "D"),
    "Free-nuclear and cellular endosperm",
    "The primary endosperm nucleus divides repeatedly without wall formation, giving free-nuclear endosperm. In "
    "coconut, the water from a tender coconut is this free-nuclear endosperm, and the surrounding white kernel is "
    "the cellular endosperm formed later by wall formation.",
    ["Tender coconut water → free-nuclear endosperm", "White kernel → cellular endosperm"],
    C12_SR("post-fertilisation events: endosperm"),
    why="The white kernel, not the water, is cellular endosperm. Perisperm (black pepper, beet) is persistent "
        "nucellus.",
    seconds=25)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Basic", "direct",
    "Banana, in which fruits develop without fertilisation, is an example of:",
    P("Parthenocarpy", ["Polyembryony", "Apomixis", "Cleistogamy"], "A"),
    "Parthenocarpy",
    "Parthenocarpic fruits develop without fertilisation and so are seedless; banana is the NCERT example. "
    "Parthenocarpy can also be induced with growth hormones.",
    ["Fruit without fertilisation, no seeds → parthenocarpy"],
    C12_SR("apomixis and polyembryony; parthenocarpy"),
    why="Apomixis forms seeds without fertilisation; banana fruits are seedless. Polyembryony is more than one "
        "embryo in a seed. Cleistogamy concerns closed flowers.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "statement_pair",
    sp("In over 60 per cent of angiosperms, pollen grains are shed at the 2-celled stage.",
       "In a 2-celled pollen grain, the generative cell is bigger than the vegetative cell and has abundant food "
       "reserve."),
    SP("C"),
    "Vegetative and generative cells of the pollen grain",
    "A mature pollen grain has a large vegetative cell, with abundant food reserve and a large, irregularly shaped "
    "nucleus, and a small, spindle-shaped generative cell with dense cytoplasm that floats in the cytoplasm of the "
    "vegetative cell. Pollen is shed at the 2-celled stage in over 60% of angiosperms; in the rest the generative "
    "cell divides first and pollen is shed at the 3-celled stage.",
    ["Statement I: true", "Statement II: reverses the two cells → false"],
    C12_SR("pollen grain"),
    seconds=40)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("Wind-pollinated flowers often have a single ovule in each ovary and numerous flowers packed into an "
       "inflorescence.",
       "Wind-pollinated flowers produce plenty of nectar to attract pollinators."),
    AR("C"),
    "Adaptations for wind pollination",
    "Wind-pollinated flowers have light, non-sticky pollen, well-exposed stamens, large feathery stigmas, often a "
    "single ovule per ovary and many flowers in an inflorescence (e.g. the corn cob). So A is true. Wind- and "
    "water-pollinated flowers are not very colourful and do not produce nectar; there is no pollinator to attract. "
    "So R is false.",
    ["A: true (NCERT feature list)", "R: false (no nectar in anemophilous flowers)"],
    C12_SR("pollination: agents of pollination"),
    seconds=40)

add(SRFP, "Pollination", "Intermediate", "match_list",
    ml(("plant", "pollination feature"),
       ["Vallisneria", "Sea-grasses such as Zostera", "Amorphophallus", "Yucca"],
       ["A moth lays its eggs in the locule of the ovary and pollinates the flower",
        "Female flowers reach the water surface on long stalks; male flowers or pollen are released onto the "
        "surface",
        "The flower itself is about 6 feet tall",
        "Female flowers stay submerged and the pollen grains are long and ribbon-like"]),
    M({"A": "II", "B": "IV", "C": "III", "D": "I"},
      [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Pollination by water and by animals",
    "In Vallisneria pollination happens at the water surface; in sea-grasses it happens under water. "
    "Amorphophallus has the tallest flower (about 6 feet). Yucca and its moth cannot complete their life cycles "
    "without each other.",
    ["Vallisneria → surface pollination → A-II", "Sea-grasses → submerged, ribbon-like pollen → B-IV",
     "Amorphophallus → 6-feet flower → C-III", "Yucca → moth lays eggs in ovary locule → D-I"],
    C12_SR("pollination: agents of pollination"),
    seconds=45)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "multi_statement",
    ms("Which of the following statements about outbreeding devices are correct?",
       ["Unisexual flowers on a monoecious plant such as castor prevent autogamy but not geitonogamy.",
        "Dioecy, as in papaya, prevents both autogamy and geitonogamy.",
        "Self-incompatibility prevents self-pollen from fertilising the ovules by inhibiting pollen germination or "
        "pollen tube growth in the pistil.",
        "Geitonogamy is genetically similar to xenogamy because the pollen comes from a different flower.",
        "In some species, pollen release and stigma receptivity are not synchronised."]),
    P("(a), (b), (c) and (e) only",
      ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only"], "B"),
    "Devices that discourage self-pollination",
    "Flowering plants avoid inbreeding by non-synchronised pollen release and stigma receptivity, different "
    "positions of anther and stigma, self-incompatibility, and unisexual flowers. In a monoecious plant (castor, "
    "maize) male and female flowers are on the same plant, so pollen can still reach another flower of the same "
    "plant (geitonogamy). In a dioecious plant (papaya) this is impossible.",
    ["(a) True", "(b) True", "(c) True",
     "(d) False: geitonogamy uses pollen from the same plant, so it is genetically similar to autogamy",
     "(e) True"],
    C12_SR("outbreeding devices"),
    why="Only option B leaves out (d) and keeps all four true statements.",
    seconds=60)

add(SRFP, "Double fertilisation", "Intermediate", "direct",
    "In a flowering plant, the ploidy of the primary endosperm nucleus, a synergid and the zygote is respectively:",
    P("3n, n and 2n", ["2n, n and 2n", "3n, 2n and n", "n, n and 2n"], "D"),
    "Products of double fertilisation",
    "One male gamete fuses with the haploid egg (syngamy) to give a diploid zygote. The other fuses with the two "
    "haploid polar nuclei (triple fusion) to give the triploid primary endosperm nucleus. Synergids are cells of "
    "the haploid embryo sac (female gametophyte), so they are haploid.",
    ["Zygote = egg (n) + male gamete (n) = 2n", "PEN = 2 polar nuclei (n + n) + male gamete (n) = 3n",
     "Synergid = cell of the female gametophyte = n"],
    C12_SR("double fertilisation"),
    why="2n for the PEN forgets that two polar nuclei fuse with the male gamete; n for the PEN confuses it with the "
        "unfused polar nucleus; 2n for the synergid forgets the embryo sac is haploid.",
    seconds=35)

add(SRFP, "Endosperm and embryo", "Intermediate", "statement_pair",
    sp("In pea, groundnut and beans, the endosperm is completely consumed by the developing embryo before the seed "
       "matures.",
       "In black pepper and beet, remnants of the nucellus persist in the seed as perisperm."),
    SP("A"),
    "Non-albuminous seeds and perisperm",
    "Seeds in which the endosperm is used up during embryo development are non-albuminous (pea, groundnut, beans). "
    "In some seeds such as black pepper and beet, part of the nucellus is not used up and persists as perisperm.",
    ["Statement I: true (non-albuminous seeds)", "Statement II: true (perisperm)"],
    C12_SR("post-fertilisation events: endosperm; seed"),
    seconds=35)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "In the embryo of a grass, the radicle and root cap are enclosed in an undifferentiated sheath called the:",
    P("Coleorhiza", ["Coleoptile", "Scutellum", "Hypocotyl"], "C"),
    "Parts of the monocot embryo",
    "A monocot (grass) embryo has one cotyledon, the scutellum, at the side of the embryonal axis. At its lower "
    "end the axis has the radicle and root cap enclosed in the coleorhiza. The epicotyl has the shoot apex and leaf "
    "primordia enclosed in a hollow foliar structure, the coleoptile.",
    ["Sheath over radicle and root cap → coleorhiza", "Sheath over shoot apex → coleoptile",
     "Single cotyledon → scutellum"],
    C12_SR("post-fertilisation events: embryo"),
    why="The coleoptile covers the shoot apex, not the radicle. The scutellum is the cotyledon. The hypocotyl is "
        "the part of the axis below the cotyledons, not a sheath.",
    seconds=30)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "assertion_reason",
    ar("If hybrid varieties are made into apomicts, farmers can keep using the hybrid seed to raise new crops year "
       "after year.",
       "In apomictic seeds the embryo forms without fertilisation, so there is no segregation of characters in the "
       "progeny."),
    AR("A"),
    "Importance of apomixis for hybrid seed",
    "Hybrid seed must normally be bought every year, because the progeny of a hybrid segregate and lose the hybrid "
    "characters. An apomictic hybrid forms its embryo without meiosis and fertilisation, so its offspring keep the "
    "hybrid characters. R is true and explains A.",
    ["A: true (NCERT application of apomixis)", "R: true (no fertilisation → no segregation)",
     "No segregation is exactly why the hybrid seed can be reused → R explains A"],
    C12_SR("apomixis and polyembryony"),
    seconds=45)

add(SRFP, "Pollination", "Advanced", "direct",
    "Commelina produces both chasmogamous and cleistogamous flowers. Which statement about its cleistogamous "
    "flowers is correct?",
    P("They are invariably autogamous and give assured seed set even in the absence of pollinators",
      ["They open and expose their anthers and stigma, like chasmogamous flowers",
       "They favour cross-pollination because pollen reaches them from other plants",
       "They are pollinated by water currents"], "C"),
    "Cleistogamy",
    "Cleistogamous flowers never open. Their anthers and stigma lie close together, so when the anthers dehisce "
    "the pollen reaches the stigma of the same flower. Such flowers are invariably autogamous, with no chance of "
    "cross-pollen landing on the stigma, and they produce assured seed set without pollinators. Viola, Oxalis and "
    "Commelina have both types of flower.",
    ["Closed flowers → only own pollen can reach the stigma → autogamy",
     "No dependence on pollinators → assured seed set"],
    C12_SR("pollination: kinds of pollination"),
    why="Exposed anthers and stigma describe chasmogamous flowers. Closed flowers cannot receive cross-pollen or be "
        "reached by water.",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "multi_statement",
    ms("Which of the following statements about the development and structure of the embryo sac are correct?",
       ["In a majority of flowering plants, one of the four megaspores is functional while the other three "
        "degenerate.",
        "Formation of the embryo sac from a single megaspore is termed bisporic development.",
        "The nucleus of the functional megaspore divides mitotically, and two more sequential free-nuclear "
        "divisions give the 8-nucleate stage.",
        "The filiform apparatus is present at the chalazal tip of the antipodal cells.",
        "The two polar nuclei are situated below the egg apparatus in the large central cell."]),
    P("(a), (c) and (e) only",
      ["(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"], "D"),
    "Megasporogenesis and the Polygonum-type embryo sac",
    "The megaspore mother cell divides by meiosis to form four megaspores; usually one is functional and develops "
    "into the embryo sac. Development from a single megaspore is monosporic. Three rounds of free-nuclear mitosis "
    "give 8 nuclei, followed by cell wall formation. The synergids carry the filiform apparatus at their "
    "micropylar tip; it guides the pollen tube.",
    ["(a) True", "(b) False: one megaspore → monosporic development", "(c) True",
     "(d) False: filiform apparatus is at the micropylar tip of the synergids", "(e) True"],
    C12_SR("the pistil, megasporangium (ovule) and embryo sac"),
    why="Options with (b) or (d) include a false statement; option D is the only one with exactly (a), (c), (e).",
    seconds=70)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "assertion_reason",
    ar("In artificial hybridisation, emasculation is not needed if the female parent bears unisexual flowers.",
       "Bagging protects the stigma of the emasculated flower from contamination by unwanted pollen."),
    AR("B"),
    "Emasculation and bagging in artificial hybridisation",
    "Emasculation means removing the anthers from a bisexual flower bud before they dehisce, so the flower cannot "
    "self-pollinate. A female (pistillate) flower has no anthers, so emasculation is unnecessary; the female buds "
    "are simply bagged before they open. Bagging prevents contamination by unwanted pollen, which is true but is "
    "not why emasculation is unnecessary. The real reason is that unisexual female flowers have no anthers.",
    ["A: true", "R: true", "Reason for A = absence of anthers, not bagging → R does not explain A"],
    C12_SR("pollen-pistil interaction; artificial hybridisation"),
    why="Option A is the trap: bagging is needed in both cases, so it cannot explain why one case skips "
        "emasculation.",
    seconds=55)

add(SRFP, "Double fertilisation", "Advanced", "match_list",
    ml(("structure", "what it develops into"),
       ["Ovule", "Ovary wall", "Integuments", "Fleshy edible part of an apple"],
       ["Seed coat", "Thalamus", "Seed", "Pericarp"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "B"),
    "Seed and fruit formation after fertilisation; false fruits",
    "After fertilisation the ovules mature into seeds and the ovary into a fruit. The integuments harden into the "
    "seed coat and the ovary wall becomes the pericarp. In apple, strawberry and cashew the thalamus also "
    "contributes to the fruit; these are false fruits, and the fleshy part of an apple is thalamus.",
    ["Ovule → seed (A-III)", "Ovary wall → pericarp (B-IV)", "Integuments → seed coat (C-I)",
     "Apple flesh → thalamus (D-II)"],
    C12_SR("post-fertilisation events: seed and fruit"),
    why="The usual trap is to treat apple flesh as pericarp; apple is a false fruit.",
    seconds=45)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Advanced", "statement_pair",
    sp("In many Citrus and mango varieties, some nucellar cells surrounding the embryo sac divide, protrude into the "
       "embryo sac and develop into embryos.",
       "Such nucellar embryos are genetically identical to the zygotic embryo present in the same seed."),
    SP("C"),
    "Nucellar polyembryony",
    "Nucellar cells are diploid cells of the mother plant, so embryos formed from them are genetically like the "
    "mother plant (they form without fertilisation). The zygotic embryo comes from fertilisation of the egg by a "
    "male gamete, which may carry different alleles. So Statement I is true and Statement II is false.",
    ["Statement I: true (NCERT example of polyembryony)",
     "Nucellar embryo = maternal tissue; zygotic embryo = egg + male gamete → not identical → Statement II false"],
    C12_SR("apomixis and polyembryony"),
    why="Students who think 'same seed, same genes' mark both true; the zygotic embryo has a paternal contribution.",
    seconds=50)

add(SRFP, "Endosperm and embryo", "Advanced", "multi_statement",
    ms("Which of the following statements about seed and pollen viability are correct?",
       ["Seeds of some species lose their viability within a few months, whereas seeds of a large number of "
        "species remain viable for several years.",
        "A 2000-year-old viable seed of the date palm, Phoenix dactylifera, was discovered during excavations at "
        "King Herod's palace near the Dead Sea.",
        "Orchid seeds are large and contain abundant endosperm.",
        "Pollen grains of rice and wheat remain viable for several months after release.",
        "Pollen grains of many species can be stored for years in liquid nitrogen at −196 °C."]),
    P("(a), (b) and (e) only",
      ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"], "A"),
    "Viability of seeds and pollen",
    "The viability of seeds after dispersal varies with the species: seeds of some species lose viability within "
    "a few months, while those of a large number of species live for several years, and some seeds stay viable "
    "far longer (a 2000-year-old viable seed of Phoenix dactylifera was recovered near the Dead Sea). Orchid fruits contain thousands of tiny seeds. Pollen of rice and wheat loses viability "
    "within about 30 minutes of release, but pollen can be stored for years in liquid nitrogen at −196 °C in "
    "pollen banks.",
    ["(a) True", "(b) True", "(c) False: orchid seeds are tiny",
     "(d) False: rice and wheat pollen stays viable for about 30 minutes", "(e) True"],
    C12_SR("seed; pollen viability"),
    why="Every other option includes (c) or (d).",
    seconds=60)

# ================================================================ Principles of Inheritance and Variation (7 / 9 / 7)
C12_PIV = lambda s: ref(12, PIV, s)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Mendel proposed the law of independent assortment on the basis of the results of:",
    P("Dihybrid crosses", ["Monohybrid crosses", "Test crosses",
                           "Self-pollination of true-breeding plants"], "B"),
    "Law of independent assortment",
    "When Mendel followed two pairs of traits together (e.g. seed colour and seed shape), the F2 showed the "
    "9 : 3 : 3 : 1 ratio, which is the product of two independent 3 : 1 ratios. From these dihybrid crosses he "
    "stated that when two pairs of traits are combined in a hybrid, segregation of one pair is independent of the "
    "other.",
    ["Independent assortment concerns two or more pairs of traits", "Two pairs of traits → dihybrid cross"],
    C12_PIV("inheritance of two genes"),
    why="Monohybrid crosses (one trait) gave the laws of dominance and segregation. Selfing true-breeding plants "
        "only confirms they breed true.",
    seconds=25)

add(PIV, "Incomplete and co-dominance", "Basic", "direct",
    "In snapdragon, a cross between true-breeding red-flowered (RR) and white-flowered (rr) plants gives pink F1 "
    "plants. The phenotypic ratio in the F2 generation is:",
    P("1 red : 2 pink : 1 white", ["3 red : 1 white", "9 : 3 : 3 : 1", "1 red : 1 white"], "D"),
    "Incomplete dominance",
    "With incomplete dominance the heterozygote (Rr) is intermediate (pink). Because every genotype now has its own "
    "phenotype, the F2 phenotypic ratio equals the genotypic ratio, 1 RR : 2 Rr : 1 rr.",
    ["F1: Rr (pink)", "F2 genotypes: 1 RR : 2 Rr : 1 rr", "Phenotypes: 1 red : 2 pink : 1 white"],
    C12_PIV("deviations from Mendelism: incomplete dominance"),
    why="3 : 1 would need complete dominance of R. 9 : 3 : 3 : 1 is a dihybrid ratio. 1 : 1 is a test-cross ratio.",
    seconds=25)

add(PIV, "Multiple alleles and pleiotropy", "Basic", "direct",
    "The ABO blood groups of humans are controlled by the gene I. In the human population this gene has:",
    P("Three alleles, giving six genotypes",
      ["Two alleles, giving three genotypes", "Three alleles, giving four genotypes",
       "Four alleles, giving six genotypes"], "B"),
    "Multiple alleles",
    "Gene I has three alleles: Iᴬ, Iᴮ and i. Since each person carries any two of them, there are six genotypes "
    "(IᴬIᴬ, Iᴬi, IᴮIᴮ, Iᴮi, IᴬIᴮ, ii) but only four phenotypes (A, B, AB, O). A gene with more than two alleles in "
    "a population is an example of multiple alleles.",
    ["Alleles: Iᴬ, Iᴮ, i = 3", "Genotypes = 3 homozygous + 3 heterozygous = 6", "Phenotypes (blood groups) = 4"],
    C12_PIV("co-dominance; multiple alleles"),
    why="Four is the number of phenotypes, not genotypes. Two alleles would not explain group O alongside A and B.",
    seconds=25)

add(PIV, "Polygenic inheritance", "Basic", "direct",
    "Human skin colour, which shows a range of shades in a population, is a classic example of:",
    P("Polygenic inheritance", ["Pleiotropy", "Co-dominance", "Multiple allelism"], "D"),
    "Polygenic traits",
    "Traits controlled by three or more genes, each adding a small effect, show a continuous range of phenotypes. "
    "Human skin colour (and height) are NCERT examples of polygenic inheritance.",
    ["Many genes, additive effect, continuous variation → polygenic"],
    C12_PIV("polygenic inheritance"),
    why="Pleiotropy is one gene with many effects. Co-dominance and multiple alleles describe alleles of a single "
        "gene (as in ABO).",
    seconds=20)

add(PIV, "Sex determination", "Basic", "direct",
    "In birds, the sex of the offspring is decided by:",
    P("The female, because she produces two kinds of eggs, with either a Z or a W chromosome",
      ["The male, because he produces two kinds of sperm",
       "The temperature at which the eggs are incubated",
       "Whether or not the egg is fertilised"], "B"),
    "ZW–ZZ sex determination",
    "In birds the female has one Z and one W chromosome, while the male has two Z chromosomes. The female is "
    "heterogametic and produces two kinds of eggs, so the egg decides the sex of the chick.",
    ["Female: ZW (heterogametic) → Z or W eggs", "Male: ZZ (homogametic) → only Z sperm",
     "Sex decided by which egg is fertilised"],
    C12_PIV("sex determination"),
    why="Male heterogamety is the human (XY) pattern. Fertilised versus unfertilised eggs decides sex in honey bees.",
    seconds=25)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "Sickle-cell anaemia is caused by the substitution of:",
    P("Glutamic acid by valine at the sixth position of the β-globin chain",
      ["Valine by glutamic acid at the sixth position of the β-globin chain",
       "Glutamic acid by valine at the sixth position of the α-globin chain",
       "Lysine by valine at the sixth position of the β-globin chain"], "D"),
    "Molecular basis of sickle-cell anaemia",
    "A single base change (GAG to GUG) in the β-globin gene replaces glutamic acid (Glu) by valine (Val) at the "
    "sixth position of the β-globin chain. The mutant haemoglobin polymerises at low oxygen tension and the RBCs "
    "become sickle-shaped.",
    ["Point mutation GAG → GUG in the β-globin gene", "Glu → Val at position 6 of β-globin"],
    C12_PIV("Mendelian disorders: sickle-cell anaemia"),
    why="The other options reverse the amino acids, name the wrong chain or the wrong amino acid.",
    seconds=25)

add(PIV, "Linkage and crossing over", "Basic", "direct",
    "The term 'linkage', to describe the physical association of genes on a chromosome, was coined by:",
    P("T.H. Morgan", ["Gregor Mendel", "Walter Sutton", "Alfred Sturtevant"], "A"),
    "Linkage",
    "Working with Drosophila, Morgan found that some genes did not assort independently because they lay on the "
    "same chromosome. He coined the term linkage for this physical association, and recombination for the "
    "generation of non-parental gene combinations.",
    ["Physical association of genes on a chromosome → linkage, term coined by Morgan"],
    C12_PIV("chromosomal theory of inheritance; linkage and recombination"),
    why="Sturtevant used recombination frequency to map genes; Sutton (with Boveri) proposed the chromosomal "
        "theory; Mendel did not know of chromosomes.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "A tall pea plant is crossed with a dwarf pea plant, and the progeny show tall and dwarf plants in a 1 : 1 "
    "ratio. The genotype of the tall parent is:",
    # Allele symbols differ only in case, and the validator compares options case-insensitively, so each option
    # also names the genotype in words.
    P("Tt (heterozygous tall)",
      ["TT (homozygous tall)", "tt (homozygous dwarf)", "Cannot be determined from this cross"], "B"),
    "Test cross",
    "Crossing a dominant-phenotype plant with a recessive (dwarf) plant is a test cross. The dwarf parent gives "
    "only t gametes, so the progeny reveal the gametes of the tall parent. A 1 : 1 ratio means the tall parent "
    "produced T and t gametes equally, so it is heterozygous.",
    ["Dwarf parent: tt → all gametes t", "Progeny 1 tall (Tt) : 1 dwarf (tt) → tall parent gave T and t equally",
     "Tall parent = Tt"],
    C12_PIV("inheritance of one gene: test cross"),
    why="TT × tt would give only tall (Tt) progeny. tt is dwarf. The test cross is exactly the method that decides "
        "the genotype.",
    seconds=35)

add(PIV, "Incomplete and co-dominance", "Intermediate", "statement_pair",
    sp("In the ABO blood group system, the allele i produces a third kind of sugar on the surface of red blood "
       "cells.",
       "When Iᴬ and Iᴮ are present together, both express their own sugar, giving blood group AB; this is "
       "co-dominance."),
    SP("D"),
    "Co-dominance in ABO blood groups",
    "The plasma membrane of RBCs has sugar polymers whose kind is controlled by gene I. Alleles Iᴬ and Iᴮ produce "
    "slightly different sugars, while allele i does not produce any sugar. Iᴬ and Iᴮ are completely dominant over "
    "i, but when present together both are expressed (co-dominance).",
    ["Statement I: i produces no sugar → false", "Statement II: IᴬIᴮ expresses both → co-dominance → true"],
    C12_PIV("co-dominance"),
    seconds=40)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "assertion_reason",
    ar("Phenylketonuria in humans is an example of pleiotropy.",
       "A mutation in the single gene coding for the enzyme phenylalanine hydroxylase shows several phenotypic "
       "effects, such as mental retardation and reduced hair and skin pigmentation."),
    AR("A"),
    "Pleiotropy",
    "A pleiotropic gene is a single gene that affects several phenotypic traits. In phenylketonuria a mutation in "
    "one gene (phenylalanine hydroxylase) produces several effects: mental retardation and reduced pigmentation of "
    "hair and skin. R describes exactly what makes PKU pleiotropic.",
    ["A: true", "R: true", "One gene, many effects = definition of pleiotropy → R explains A"],
    C12_PIV("pleiotropy"),
    seconds=40)

add(PIV, "Sex determination", "Intermediate", "match_list",
    ml(("organism", "mechanism of sex determination"),
       ["Grasshopper", "Human", "Bird", "Honey bee"],
       ["Female heterogamety (ZW female, ZZ male)", "Haplodiploidy: sex decided by the number of chromosome sets",
        "XO type: males have only one X and no other sex chromosome", "XY type with male heterogamety"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "B"),
    "Mechanisms of sex determination",
    "Different organisms determine sex differently.",
    ["Grasshopper: XO type, males have one X (A-III)", "Human: XX female, XY male (B-IV)",
     "Bird: ZW female, ZZ male (C-I)", "Honey bee: fertilised eggs → diploid females, unfertilised → haploid males "
     "(D-II)"],
    C12_PIV("sex determination"),
    seconds=40)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "multi_statement",
    ms("Which of the following statements about genetic disorders are correct?",
       ["Down's syndrome is caused by an additional copy of chromosome 21.",
        "Klinefelter's syndrome is caused by the karyotype 47, XYY.",
        "Colour blindness is a sex-linked recessive disorder caused by a defect in either the red or the green cone "
        "of the eye.",
        "Chromosomal disorders are caused by an alteration or mutation in a single gene.",
        "Thalassemia and sickle-cell anaemia are both autosome-linked recessive disorders."]),
    P("(a), (c) and (e) only",
      ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"], "B"),
    "Mendelian and chromosomal disorders",
    "Mendelian disorders come from a change in a single gene; chromosomal disorders come from absence, excess or "
    "abnormal arrangement of one or more chromosomes.",
    ["(a) True: trisomy 21", "(b) False: Klinefelter's syndrome is 47, XXY",
     "(c) True", "(d) False: that describes Mendelian disorders", "(e) True"],
    C12_PIV("genetic disorders"),
    why="XYY is the usual trap for Klinefelter's syndrome; the extra chromosome is an X.",
    seconds=55)

add(PIV, "Linkage and crossing over", "Intermediate", "direct",
    "In Drosophila, Morgan found 1.3% recombination between the genes for yellow body and white eye, and 37.2% "
    "recombination between the genes for white eye and miniature wing. This shows that:",
    P("The genes for body colour and eye colour lie closer together than the genes for eye colour and wing size",
      ["The genes for white eye and miniature wing are on different chromosomes",
       "Recombination frequency does not depend on the distance between genes",
       "The genes for yellow body and white eye assort independently"], "D"),
    "Recombination frequency and linkage strength",
    "Genes on the same chromosome are linked; the closer they are, the less often crossing over separates them. "
    "Very low recombination (1.3%) means tight linkage; higher recombination (37.2%) means looser linkage, i.e. a "
    "greater distance. Sturtevant used such frequencies to map genes.",
    ["1.3% → tightly linked → close together", "37.2% → loosely linked → farther apart"],
    C12_PIV("linkage and recombination"),
    why="Below 50% recombination the genes are still linked, so they are not on different chromosomes and do not "
        "assort independently. Recombination frequency is used precisely because it reflects distance.",
    seconds=45)

add(PIV, "Sex-linked inheritance", "Intermediate", "numerical",
    "A woman with normal vision, whose father was colour blind, marries a colour-blind man. What fraction of their "
    "daughters are expected to be colour blind?",
    P("1/2", ["0", "1/4", "1"], "B"),
    "X-linked recessive inheritance",
    "The woman received her father's X with the colour-blindness allele (Xᶜ), so she is a carrier, XᶜX. Her "
    "husband is XᶜY. Every daughter receives the father's Xᶜ, so whether she is colour blind depends only on the X "
    "she gets from her mother.",
    ["Mother XᶜX × father XᶜY", "Daughters: XᶜXᶜ (colour blind) or XᶜX (carrier), each with probability 1/2",
     "Fraction of daughters colour blind = 1/2"],
    C12_PIV("Mendelian disorders: colour blindness"),
    shortcut="With a colour-blind father, daughters get Xᶜ for certain; only the mother's X matters.",
    why="0 assumes daughters can only be carriers, which is true only if the father has normal vision. 1/4 is the "
        "fraction of all children who are colour-blind daughters. 1 would need a colour-blind mother.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Polygenic inheritance", "Intermediate", "statement_pair",
    sp("In polygenic inheritance, the phenotype is decided only by the dominant allele at a single locus.",
       "Besides the involvement of multiple genes, polygenic inheritance also takes into account the influence of "
       "the environment."),
    SP("D"),
    "Features of polygenic traits",
    "Polygenic traits are controlled by three or more genes, and the phenotype reflects the contribution of each "
    "allele: the effect of each allele is additive. NCERT adds that polygenic inheritance also takes the "
    "influence of the environment into account.",
    ["Statement I: many genes with additive effects, not one locus → false", "Statement II: true"],
    C12_PIV("polygenic inheritance"),
    seconds=35)

add(PIV, "Mendelian inheritance", "Intermediate", "assertion_reason",
    ar("When true-breeding tall and dwarf pea plants are crossed, all F1 plants are of intermediate height.",
       "In a dissimilar pair of factors, one member of the pair dominates the other."),
    AR("D"),
    "Law of dominance",
    "Mendel's F1 plants from tall × dwarf were all tall, like one parent; none was of intermediate height. This "
    "is explained by the law of dominance: in a dissimilar pair of factors one (dominant) masks the other "
    "(recessive). So A is false and R is true.",
    ["A: false (F1 all tall)", "R: true (law of dominance)"],
    C12_PIV("inheritance of one gene: law of dominance"),
    why="Intermediate F1 phenotypes occur with incomplete dominance (e.g. snapdragon), not in Mendel's height cross.",
    seconds=35)

add(PIV, "Mendelian inheritance", "Advanced", "numerical",
    "In the cross AaBBCc × aaBbCc, the three genes assort independently and each shows complete dominance. What "
    "fraction of the offspring will show the dominant phenotype for all three traits?",
    P("3/8", ["27/64", "9/32", "3/16"], "C"),
    "Product rule for independently assorting genes",
    "Work out each gene separately, then multiply the probabilities.",
    ["Aa × aa → 1/2 Aa (dominant), 1/2 aa", "BB × Bb → all B_ → probability 1",
     "Cc × Cc → 3/4 C_", "All three dominant = 1/2 × 1 × 3/4 = 3/8"],
    C12_PIV("inheritance of two genes; law of independent assortment"),
    shortcut="A homozygous dominant parent (BB) makes that gene drop out of the calculation (probability 1).",
    why="27/64 assumes all three genes are Aa × Aa type crosses. 9/32 treats BB × Bb as if it gave 3/4 dominant. "
        "3/16 treats it as if it gave 1/2.",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "Suppose human skin colour is controlled by three genes A, B and C, each dominant allele adding equally to "
    "pigmentation. AABBCC (darkest) is married to aabbcc (lightest), and two of their AaBbCc children have "
    "offspring. What fraction of these grandchildren will have the same skin colour as their AaBbCc parents?",
    P("5/16", ["15/64", "1/64", "3/32"], "A"),
    "Additive effect in polygenic inheritance",
    "Skin colour depends only on the number of dominant alleles, not on which gene carries them. AaBbCc has 3 "
    "dominant alleles out of 6. Each of the 6 allele positions in a grandchild is dominant with probability 1/2.",
    ["Each parent passes one allele of each gene: 6 independent alleles, each dominant with p = 1/2",
     "P(exactly 3 dominant) = ⁶C₃ × (1/2)⁶ = 20/64",
     "20/64 = 5/16"],
    C12_PIV("polygenic inheritance"),
    shortcut="Phenotype classes follow the binomial coefficients 1 : 6 : 15 : 20 : 15 : 6 : 1 (out of 64); the "
             "middle class is 20/64.",
    why="15/64 is the class with 2 (or 4) dominant alleles. 1/64 is the darkest (or lightest) class. 3/32 (6/64) "
        "is the class with 1 (or 5) dominant alleles.",
    seconds=120, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "multi_statement",
    ms("Which of the following statements about haemophilia are correct?",
       ["A haemophilic son must have received the defective allele from his mother.",
        "A haemophilic female is extremely rare because her mother must be at least a carrier and her father must "
        "be haemophilic.",
        "A woman heterozygous (carrier) for haemophilia is herself haemophilic.",
        "Queen Victoria was a carrier, and her family pedigree shows several haemophilic descendants.",
        "Haemophilia is a Y-linked disorder, passed only from father to son."]),
    P("(a), (b) and (d) only",
      ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"], "D"),
    "Haemophilia, a sex-linked recessive disorder",
    "The haemophilia gene is on the X chromosome and is recessive. A son gets his only X from his mother, so an "
    "affected son inherits the allele from her. A carrier (heterozygous) female is unaffected but may pass the "
    "allele to her sons. An affected female needs the allele on both X chromosomes.",
    ["(a) True: a son's X comes from the mother", "(b) True: NCERT's reason why affected females are rare",
     "(c) False: carriers are unaffected", "(d) True: NCERT example", "(e) False: it is X-linked"],
    C12_PIV("Mendelian disorders: haemophilia"),
    why="Options A, B and D each include a false statement, (c) or (e).",
    seconds=60)

add(PIV, "Sex determination", "Advanced", "assertion_reason",
    ar("A male honey bee has no father and so cannot have sons, but it has a grandfather and can have grandsons.",
       "Male honey bees develop from unfertilised eggs by parthenogenesis and are haploid, while females develop "
       "from fertilised eggs."),
    AR("A"),
    "Haplodiploid sex determination in honey bees",
    "A drone comes from an unfertilised egg, so it has a mother but no father. Its sperm can only fertilise eggs, "
    "and fertilised eggs become females, so it cannot have sons. Its mother had a father, so it has a grandfather; "
    "its daughters can lay unfertilised eggs, so it can have grandsons. All of this follows from R.",
    ["A: true", "R: true (haplodiploidy)",
     "Unfertilised egg → no father; its sperm → only daughters → no sons; daughters' unfertilised eggs → grandsons"],
    C12_PIV("sex determination: honey bee"),
    seconds=60)

add(PIV, "Linkage and crossing over", "Advanced", "statement_pair",
    sp("Sutton and Boveri provided the experimental verification of the chromosomal theory of inheritance using "
       "Drosophila.",
       "Alfred Sturtevant used the frequency of recombination between gene pairs on the same chromosome as a "
       "measure of the distance between them and mapped their positions on the chromosome."),
    SP("D"),
    "Chromosomal theory of inheritance and gene mapping",
    "Sutton and Boveri proposed the chromosomal theory of inheritance by uniting chromosomal segregation with "
    "Mendel's principles. Its experimental verification came from Thomas Hunt Morgan and his colleagues, working "
    "with Drosophila melanogaster. Sturtevant, Morgan's student, used recombination frequencies to make genetic "
    "maps.",
    ["Statement I: verification was by Morgan, not Sutton and Boveri → false", "Statement II: true"],
    C12_PIV("chromosomal theory of inheritance; linkage and recombination"),
    why="Statement I swaps the people who proposed the theory with the one who verified it.",
    seconds=45)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "match_list",
    ml(("features", "disorder"),
       ["Overall masculine development with gynaecomastia; sterile",
        "Sterile female with rudimentary ovaries and lack of other secondary sexual characters",
        "Short stature, small round head, furrowed tongue, partially open mouth and a characteristic palm crease",
        "Phenylpyruvic acid accumulates in the brain, causing mental retardation, and is excreted in urine"],
       ["Down's syndrome", "Turner's syndrome", "Klinefelter's syndrome", "Phenylketonuria"]),
    M({"A": "III", "B": "II", "C": "I", "D": "IV"},
      [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
       {"A": "I", "B": "II", "C": "III", "D": "IV"}], "C"),
    "Identifying genetic disorders from symptoms",
    "Klinefelter's syndrome (47, XXY): masculine development with feminine features such as gynaecomastia, sterile. "
    "Turner's syndrome (45, X0): sterile female with rudimentary ovaries. Down's syndrome (trisomy 21): short "
    "stature, small round head, furrowed tongue, palm crease. Phenylketonuria: an inborn error of metabolism in "
    "which phenylalanine is converted to phenylpyruvic acid and its derivatives.",
    ["A → Klinefelter's (III)", "B → Turner's (II)", "C → Down's (I)", "D → Phenylketonuria (IV)"],
    C12_PIV("genetic disorders"),
    why="The trap is swapping Klinefelter's and Turner's: one is a sterile male with feminine features, the other a "
        "sterile female.",
    seconds=55)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "direct",
    "A man with blood group A and a woman with blood group B have a first child with blood group O. Which statement "
    "about their future children is correct?",
    P("Each child has a 1/4 chance of having blood group AB",
      ["No child can have blood group AB", "Only children with blood group A or B are possible",
       "Every later child must also have blood group O"], "B"),
    "Working out parental genotypes from a child (ABO)",
    "An O child is ii, so each parent must carry i: the father is Iᴬi and the mother Iᴮi. Their gametes are Iᴬ or "
    "i, and Iᴮ or i, each with probability 1/2, so all four blood groups are equally likely.",
    ["Child O = ii → father Iᴬi, mother Iᴮi",
     "Children: IᴬIᴮ (AB), Iᴬi (A), Iᴮi (B), ii (O), each 1/4",
     "P(AB) = 1/4"],
    C12_PIV("co-dominance; multiple alleles"),
    why="AB is possible because Iᴬ and Iᴮ are co-dominant. A and B are not the only outcomes, and an O child does "
        "not fix later children as O.",
    seconds=60)

# ================================================================ Molecular Basis of Inheritance (7 / 9 / 7)
C12_MBI = lambda s: ref(12, MBI, s)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "According to Erwin Chargaff's observations, which of the following ratios is always equal to 1 in a "
    "double-stranded DNA?",
    P("A/T", ["A/G", "(A + T)/(G + C)", "T/C"], "C"),
    "Chargaff's rule",
    "In double-stranded DNA, adenine always pairs with thymine and guanine with cytosine, so the amount of A equals "
    "that of T and the amount of G equals that of C. A/T = G/C = 1. The ratio (A + T)/(G + C) differs from one "
    "species to another.",
    ["A pairs with T → A = T → A/T = 1", "A/G, T/C and (A + T)/(G + C) depend on base composition"],
    C12_MBI("structure of polynucleotide chain; double helix"),
    why="(A + T)/(G + C) varies between species; A/G and T/C equal 1 only by chance in a DNA with equal A and G.",
    seconds=25)

add(MBI, "DNA as genetic material", "Basic", "direct",
    "In the Hershey–Chase experiment, bacteriophages grown on a medium containing radioactive phosphorus had "
    "radioactivity in their:",
    P("DNA", ["Protein coat", "Both DNA and protein coat equally", "Tail fibres only"], "A"),
    "Labelling DNA and protein separately",
    "DNA contains phosphorus but no sulphur; protein contains sulphur but no phosphorus. So ³²P labels phage DNA and "
    "³⁵S labels phage protein. Bacteria infected with ³²P-labelled phages became radioactive, showing that DNA, not "
    "protein, enters the bacterium and is the genetic material.",
    ["Phosphorus is in DNA (phosphate backbone), not in protein", "Radioactive phosphorus → DNA labelled"],
    C12_MBI("the search for genetic material: the genetic material is DNA"),
    why="The protein coat (including the tail) was labelled with radioactive sulphur in the other set of phages.",
    seconds=25)

add(MBI, "DNA packaging", "Basic", "direct",
    "Under the electron microscope, chromatin appears as 'beads-on-string'. Each 'bead' is a:",
    P("Nucleosome", ["Chromatid", "Centromere", "Ribosome"], "C"),
    "Nucleosome as the repeating unit of chromatin",
    "In eukaryotes, negatively charged DNA is wrapped around a positively charged histone octamer to form a "
    "nucleosome, which holds about 200 bp of DNA. Nucleosomes are the repeating units of chromatin and look like "
    "beads on a string.",
    ["Histone octamer + ~200 bp DNA = nucleosome", "Repeated nucleosomes → beads-on-string chromatin"],
    C12_MBI("packaging of DNA helix"),
    why="A chromatid is one half of a replicated chromosome; a centromere is a single constriction; ribosomes are "
        "not part of chromatin.",
    seconds=20)

add(MBI, "Replication", "Basic", "direct",
    "During DNA replication, the discontinuously synthesised fragments on one strand are later joined by:",
    P("DNA ligase", ["DNA-dependent RNA polymerase", "Helicase", "Restriction endonuclease"], "A"),
    "Discontinuous replication",
    "DNA polymerase can add nucleotides only in the 5'→3' direction, so on one template strand the new DNA is made "
    "in short pieces (Okazaki fragments). These are joined by the enzyme DNA ligase.",
    ["Fragments formed on the discontinuous strand", "Joined by DNA ligase"],
    C12_MBI("replication: the machinery and the enzymes"),
    why="RNA polymerase transcribes; restriction enzymes cut DNA; neither joins Okazaki fragments.",
    seconds=20)

add(MBI, "Transcription", "Basic", "direct",
    "In eukaryotes, RNA polymerase III is responsible for the transcription of:",
    P("tRNA, 5S rRNA and snRNAs",
      ["28S, 18S and 5.8S rRNAs", "hnRNA, the precursor of mRNA", "Only mRNA of mitochondria"], "C"),
    "The three eukaryotic RNA polymerases",
    "Eukaryotic nuclei have three RNA polymerases: RNA polymerase I transcribes rRNAs (28S, 18S and 5.8S); RNA "
    "polymerase II transcribes the precursor of mRNA, the heterogeneous nuclear RNA (hnRNA); RNA polymerase III "
    "transcribes tRNA, 5S rRNA and snRNAs.",
    ["Pol I → 28S, 18S, 5.8S rRNA", "Pol II → hnRNA", "Pol III → tRNA, 5S rRNA, snRNA"],
    C12_MBI("transcription: transcription in eukaryotes"),
    why="28S, 18S and 5.8S rRNAs are made by RNA polymerase I and hnRNA by RNA polymerase II.",
    seconds=25)

add(MBI, "Genetic code and translation", "Basic", "direct",
    "The codon AUG has a dual function. It:",
    P("Codes for methionine and also acts as the initiator codon",
      ["Codes for methionine and also acts as a stop codon", "Codes for no amino acid and acts as the initiator codon",
       "Codes for both methionine and valine"], "A"),
    "Special codons",
    "Of the 64 codons, 61 code for amino acids and 3 (UAA, UAG, UGA) are stop codons. AUG codes for methionine and "
    "also serves as the initiator codon.",
    ["AUG → methionine", "AUG → start signal for translation"],
    C12_MBI("genetic code"),
    why="Stop codons (UAA, UAG, UGA) code for no amino acid. The code is unambiguous, so AUG cannot code for two "
        "amino acids.",
    seconds=20)

add(MBI, "Lac operon", "Basic", "direct",
    "In the lac operon of E. coli, the y gene codes for:",
    P("Permease", ["β-galactosidase", "Transacetylase", "The repressor protein"], "B"),
    "Structural genes of the lac operon",
    "The lac operon has three structural genes: z codes for β-galactosidase (hydrolyses lactose into galactose and "
    "glucose), y for permease (increases permeability of the cell to β-galactosides) and a for transacetylase. The "
    "repressor is coded by the regulatory i gene.",
    ["z → β-galactosidase", "y → permease", "a → transacetylase", "i → repressor"],
    C12_MBI("regulation of gene expression: the lac operon"),
    why="β-galactosidase is coded by z, transacetylase by a and the repressor by i.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Intermediate", "direct",
    "In the B-form of DNA described by Watson and Crick, the pitch of the helix is 3.4 nm and the distance between "
    "two consecutive base pairs is 0.34 nm. The number of base pairs in each turn is roughly:",
    P("10", ["20", "34", "3.4"], "C"),
    "Dimensions of the double helix",
    "One complete turn (pitch) is 3.4 nm and consecutive base pairs are 0.34 nm apart, so one turn contains "
    "3.4/0.34 = 10 base pairs.",
    ["bp per turn = pitch / distance between base pairs", "= 3.4 nm / 0.34 nm = 10"],
    C12_MBI("double-helix model: salient features"),
    why="20 counts the bases of both strands; 34 and 3.4 confuse the units or invert the ratio.",
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "statement_pair",
    sp("The 2'-OH group present on every nucleotide in RNA makes RNA labile and easily degradable.",
       "The presence of thymine in place of uracil confers additional stability to DNA."),
    SP("A"),
    "Why DNA is a more stable genetic material than RNA",
    "RNA's 2'-OH group is reactive, so RNA is labile and also acts as a catalyst. DNA lacks it and is chemically "
    "less reactive. Thymine (5-methyl uracil) in place of uracil further adds stability. This is why DNA is the "
    "preferred store of genetic information.",
    ["Statement I: true", "Statement II: true"],
    C12_MBI("RNA world; properties of genetic material"),
    seconds=35)

add(MBI, "Replication", "Intermediate", "assertion_reason",
    ar("When E. coli grown for many generations in ¹⁵N medium is shifted to ¹⁴N medium for 40 minutes, the extracted "
       "DNA contains equal amounts of light and hybrid DNA.",
       "In E. coli, both new strands of DNA are synthesised continuously during replication."),
    AR("C"),
    "Meselson–Stahl experiment",
    "E. coli divides in about 20 minutes, so 40 minutes is two generations. With semiconservative replication, the "
    "first generation is all hybrid (¹⁵N/¹⁴N) and the second has equal amounts of hybrid and light (¹⁴N/¹⁴N) DNA. "
    "So A is true. Because DNA polymerase works only 5'→3', one strand is made continuously and the other "
    "discontinuously, so R is false.",
    ["40 min = 2 generations → 1 hybrid : 1 light → A true",
     "Replication is continuous on one strand and discontinuous on the other → R false"],
    C12_MBI("replication: the experimental proof; the machinery and the enzymes"),
    seconds=50)

add(MBI, "DNA as genetic material", "Intermediate", "match_list",
    ml(("scientist(s)", "contribution"),
       ["Frederick Griffith", "Avery, MacLeod and McCarty", "Meselson and Stahl", "Jacob and Monod"],
       ["Elucidated the lac operon", "Showed that the transforming principle is DNA",
        "Transformation of R-strain Streptococcus pneumoniae by heat-killed S-strain bacteria",
        "Proved semiconservative replication of DNA using ¹⁵N"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Landmark experiments in molecular genetics",
    "Each name goes with one classic experiment.",
    ["Griffith (1928): heat-killed S strain transformed live R strain → A-III",
     "Avery, MacLeod and McCarty: the transforming principle was destroyed only by DNase → DNA → B-II",
     "Meselson and Stahl (1958): ¹⁵N/¹⁴N density labelling → semiconservative replication → C-IV",
     "Jacob and Monod: first described a transcriptionally regulated system, the lac operon → D-I"],
    C12_MBI("the search for genetic material; replication; the lac operon"),
    seconds=45)

add(MBI, "Transcription", "Intermediate", "multi_statement",
    ms("Which of the following statements about transcription are correct?",
       ["The DNA strand with 3'→5' polarity acts as the template.",
        "The coding strand acts as the template for RNA synthesis.",
        "The promoter is located towards the 3' end (downstream) of the structural gene, with reference to the "
        "coding strand.",
        "In bacteria, the sigma factor helps in initiation and the rho factor helps in termination of "
        "transcription.",
        "In bacteria, translation can begin much before the mRNA is fully transcribed."]),
    P("(a), (d) and (e) only",
      ["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"], "C"),
    "The transcription unit",
    "RNA is made 5'→3', so the template strand has 3'→5' polarity. The other strand, the coding strand, has the "
    "same sequence as the RNA (with T for U) and is not copied. The promoter lies upstream, towards the 5' end of "
    "the coding strand. In bacteria, σ and ρ factors help initiation and termination; since mRNA needs no processing "
    "and transcription and translation occur in the same compartment, translation can start before transcription "
    "ends.",
    ["(a) True", "(b) False: the coding strand is not copied", "(c) False: the promoter is upstream (5' end)",
     "(d) True", "(e) True"],
    C12_MBI("transcription: transcription unit; transcription in bacteria"),
    why="Options A, B and D contain (b) or (c), or both.",
    seconds=60)

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "The fact that a particular codon codes for only one amino acid is expressed by saying that the genetic code "
    "is:",
    P("Unambiguous and specific", ["Degenerate", "Comma-less", "Nearly universal"], "C"),
    "Salient features of the genetic code",
    "The genetic code is triplet, unambiguous and specific (one codon → one amino acid), degenerate (some amino "
    "acids are coded by more than one codon), read continuously without punctuation (comma-less) and nearly "
    "universal.",
    ["One codon → only one amino acid → unambiguous and specific"],
    C12_MBI("genetic code"),
    why="Degeneracy is the reverse idea: one amino acid → many codons. Comma-less refers to continuous reading; "
        "universality to the same code in different organisms.",
    seconds=25)

add(MBI, "Transcription", "Intermediate", "statement_pair",
    sp("In capping, an unusual nucleotide (methyl guanosine triphosphate) is added to the 5' end of hnRNA.",
       "In tailing, 200–300 adenylate residues are added to the 3' end of hnRNA in a template-dependent manner."),
    SP("C"),
    "Processing of hnRNA in eukaryotes",
    "The primary transcript (hnRNA) is spliced to remove introns, capped at the 5' end with methyl guanosine "
    "triphosphate and tailed at the 3' end with 200–300 adenylate residues. Tailing is template-independent: the "
    "poly-A tail is not copied from DNA.",
    ["Statement I: true", "Statement II: tailing is template-independent → false"],
    C12_MBI("transcription in eukaryotes"),
    why="Statement II is right about the number and position of residues; only 'template-dependent' is wrong.",
    seconds=40)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("Regulation of the lac operon by the repressor is referred to as negative regulation.",
       "In the absence of an inducer, the repressor binds to the operator and prevents RNA polymerase from "
       "transcribing the operon."),
    AR("A"),
    "Negative regulation of the lac operon",
    "The i gene makes a repressor that binds the operator and blocks transcription. When lactose (the inducer) is "
    "present, it inactivates the repressor and the genes are transcribed. Because the regulatory protein switches "
    "genes off, this is negative regulation. R describes that switching-off, so it explains A.",
    ["A: true", "R: true", "Repressor switches the operon off → negative regulation → R explains A"],
    C12_MBI("regulation of gene expression: the lac operon"),
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "direct",
    "According to the salient features of the human genome, which chromosome has the most genes and which has the "
    "fewest?",
    P("Chromosome 1 has the most genes and the Y chromosome has the fewest",
      ["The X chromosome has the most genes and chromosome 1 has the fewest",
       "Chromosome 21 has the most genes and the Y chromosome has the fewest",
       "The Y chromosome has the most genes and chromosome 21 has the fewest"], "D"),
    "Salient features of the human genome",
    "The Human Genome Project found that chromosome 1 has the most genes (2968) and the Y chromosome has the fewest "
    "(231).",
    ["Most genes: chromosome 1 (2968)", "Fewest genes: Y (231)"],
    C12_MBI("human genome project: salient features"),
    seconds=25)

add(MBI, "DNA and RNA structure", "Advanced", "numerical",
    "A double-stranded DNA molecule has 1000 base pairs, and 30% of its bases are guanine. Adenine pairs with "
    "thymine through two hydrogen bonds and guanine with cytosine through three. The total number of hydrogen bonds "
    "between the two strands is:",
    P("2600", ["2400", "3000", "1300"], "B"),
    "Base pairing and hydrogen bonds",
    "Find the number of G–C and A–T pairs from the percentage of guanine, then add their hydrogen bonds.",
    ["Total bases = 2 × 1000 = 2000; G = 30% of 2000 = 600 → 600 G–C pairs",
     "A–T pairs = 1000 − 600 = 400",
     "Hydrogen bonds = 600 × 3 + 400 × 2 = 1800 + 800 = 2600"],
    C12_MBI("structure of polynucleotide chain; double helix"),
    why="2400 swaps the bond numbers (3 for A–T, 2 for G–C). 3000 gives every pair three bonds. 1300 counts only "
        "half the pairs.",
    seconds=90, verified_by=RECOMPUTED)

add(MBI, "Genetic code and translation", "Advanced", "numerical",
    "The coding part of an mRNA, counted from the first base of the initiation codon AUG to the last base of the "
    "stop codon UAG, is 336 nucleotides long. How many amino acids will the polypeptide translated from it have "
    "(before any processing)?",
    P("111", ["112", "336", "110"], "D"),
    "Codons, start and stop signals",
    "The code is triplet and comma-less, so 336 nucleotides are 112 codons. The first codon, AUG, codes for "
    "methionine. The last codon, UAG, is a stop codon and codes for no amino acid.",
    ["Codons = 336 / 3 = 112", "AUG codes methionine → counted", "UAG is a stop codon → not counted",
     "Amino acids = 112 − 1 = 111"],
    C12_MBI("genetic code; translation"),
    why="112 counts the stop codon as an amino acid. 110 also drops the start codon, though AUG codes for "
        "methionine. 336 forgets that the code is a triplet.",
    seconds=75, verified_by=RECOMPUTED)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "multi_statement",
    ms("Which of the following are salient features of the human genome as revealed by the Human Genome Project?",
       ["The total number of genes is about 80,000 to 1,40,000.",
        "The average gene has 3000 bases, and the largest known human gene, dystrophin, has 2.4 million bases.",
        "Less than 2 per cent of the genome codes for proteins.",
        "The functions are known for over 50 per cent of the discovered genes.",
        "Scientists have identified about 1.4 million locations where single-base DNA differences (SNPs) occur in "
        "humans."]),
    P("(b), (c) and (e) only",
      ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only"], "A"),
    "Salient features of the human genome",
    "The human genome has 3164.7 million bp and an estimated 30,000 genes, much lower than the earlier estimates of "
    "80,000 to 1,40,000. The average gene has 3000 bases; dystrophin, the largest, has 2.4 million. Less than 2% of "
    "the genome codes for proteins. The functions are unknown for over 50% of the discovered genes. About 1.4 "
    "million SNP locations were identified.",
    ["(a) False: about 30,000 genes; 80,000–1,40,000 were the earlier estimates", "(b) True", "(c) True",
     "(d) False: functions are unknown for over 50% of genes", "(e) True"],
    C12_MBI("human genome project: salient features"),
    why="Statements (a) and (d) are NCERT facts turned around; every option except A includes one of them.",
    seconds=70)

add(MBI, "Replication", "Advanced", "assertion_reason",
    ar("Replication is discontinuous on the template strand that has 5'→3' polarity.",
       "DNA-dependent DNA polymerases catalyse polymerisation only in one direction, that is 5'→3'."),
    AR("A"),
    "Continuous and discontinuous synthesis at the replication fork",
    "A new strand grows only 5'→3', so it must run antiparallel to its template. On the template with 3'→5' "
    "polarity the new strand grows towards the fork, continuously. On the template with 5'→3' polarity it can only "
    "be made in short pieces away from the fork, which are joined by DNA ligase. The one-direction activity of DNA "
    "polymerase (R) is exactly why A happens.",
    ["A: true (NCERT: template 5'→3' → discontinuous)", "R: true",
     "Polymerase works only 5'→3' → one strand must be made in fragments → R explains A"],
    C12_MBI("replication: the machinery and the enzymes"),
    why="Students who remember 'the 3'→5' template is continuous' sometimes mark A false; the question names the "
        "other template.",
    seconds=55)

add(MBI, "Genetic code and translation", "Advanced", "match_list",
    ml(("component", "role in protein synthesis"),
       ["tRNA", "23S rRNA in bacteria", "mRNA", "Untranslated regions (UTRs)"],
       ["Acts as an adapter that reads the codon and carries a specific amino acid",
        "Provides the template whose codons are translated",
        "Sequences at the 5' and 3' ends that are not translated but are needed for efficient translation",
        "Acts as an enzyme (ribozyme) for peptide bond formation"]),
    M({"A": "I", "B": "IV", "C": "II", "D": "III"},
      [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "IV", "B": "I", "C": "II", "D": "III"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "D"),
    "RNAs and their roles in translation",
    "tRNA has an anticodon loop that pairs with the codon and an amino-acid acceptor end, so it is the adapter "
    "molecule. In bacteria, 23S rRNA acts as the catalyst (ribozyme) for peptide bond formation. mRNA carries the "
    "codons, and its UTRs at both ends are not translated but are required for efficient translation.",
    ["tRNA → adapter (A-I)", "23S rRNA → ribozyme (B-IV)", "mRNA → template (C-II)", "UTRs → untranslated but needed "
     "(D-III)"],
    C12_MBI("tRNA, the adapter molecule; translation"),
    why="The common trap is to give the catalytic role to a protein enzyme or to tRNA; NCERT names 23S rRNA.",
    seconds=50)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "statement_pair",
    sp("DNA fingerprinting involves identifying differences in some specific regions of the DNA sequence called "
       "repetitive DNA.",
       "Satellite DNA sequences normally code for proteins, which is why they differ between individuals."),
    SP("C"),
    "Basis of DNA fingerprinting",
    "Small stretches of DNA are repeated many times; these repetitive sequences separate as satellite peaks in "
    "density gradient centrifugation and are called satellite DNA. They normally do not code for any proteins but "
    "form a large part of the genome and show a high degree of polymorphism, which is the basis of DNA "
    "fingerprinting.",
    ["Statement I: true", "Statement II: satellite DNA normally does not code for proteins → false"],
    C12_MBI("DNA fingerprinting"),
    why="Polymorphism in satellite DNA arises because these non-coding regions tolerate variation, not because they "
        "code for proteins.",
    seconds=45)

add(MBI, "DNA packaging", "Advanced", "direct",
    "Which of the following statements about chromatin is correct?",
    P("Euchromatin is loosely packed, stains light and is transcriptionally active",
      ["Heterochromatin is loosely packed, stains light and is transcriptionally active",
       "A nucleosome contains about 200 bp of DNA wrapped around a histone tetramer",
       "Histones are negatively charged proteins rich in lysine and arginine"], "B"),
    "Euchromatin, heterochromatin and nucleosomes",
    "Loosely packed, lightly staining chromatin is euchromatin and is transcriptionally active. Densely packed, "
    "darkly staining heterochromatin is inactive. A nucleosome is about 200 bp of DNA around an octamer (eight "
    "molecules) of histones. Histones are positively charged because they are rich in the basic amino acids lysine "
    "and arginine.",
    ["Euchromatin: loose, light, active → correct",
     "Heterochromatin: dense, dark, inactive", "Histone octamer, not tetramer", "Histones are positive (basic)"],
    C12_MBI("packaging of DNA helix"),
    why="Each wrong option changes one word: heterochromatin for euchromatin, tetramer for octamer, negative for "
        "positive.",
    seconds=45)

# ================================================================ Microbes in Human Welfare (3 / 3 / 3)
C12_MHW = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "direct",
    "The large holes in 'Swiss cheese' are due to the production of a large amount of CO₂ by:",
    P("Propionibacterium sharmanii", ["Lactobacillus", "Saccharomyces cerevisiae", "Penicillium notatum"], "B"),
    "Microbes in cheese making",
    "Different cheeses get their texture, flavour and taste from specific microbes. The large holes in Swiss cheese "
    "are made by CO₂ released by the bacterium Propionibacterium sharmanii.",
    ["Swiss cheese holes → CO₂ → Propionibacterium sharmanii"],
    C12_MHW("microbes in household products"),
    why="Lactobacillus sets milk into curd; S. cerevisiae is baker's and brewer's yeast; Penicillium notatum gives "
        "penicillin.",
    seconds=20)

add(MHW, "Biogas", "Basic", "direct",
    "Bacteria that grow anaerobically on cellulosic material and produce large amounts of methane along with CO₂ and "
    "H₂ belong to the group of methanogens. An example is:",
    P("Methanobacterium", ["Rhizobium", "Azotobacter", "Lactobacillus"], "D"),
    "Methanogens and biogas",
    "Methanogens such as Methanobacterium grow anaerobically on cellulosic material and produce methane-rich "
    "biogas. They are found in the anaerobic sludge of sewage treatment and in the rumen of cattle, which is why "
    "cattle dung (gobar) is used in biogas plants.",
    ["Methane production under anaerobic conditions → methanogens → Methanobacterium"],
    C12_MHW("microbes in production of biogas"),
    why="Rhizobium and Azotobacter fix nitrogen; Lactobacillus makes lactic acid.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "Spores of Bacillus thuringiensis are sprayed on crops such as Brassicas and fruit trees mainly to control:",
    P("Butterfly caterpillars", ["Aphids", "Fungal plant pathogens", "Nitrogen deficiency in the soil"], "B"),
    "Microbial biocontrol agents",
    "Bt spores are mixed with water and sprayed on plants. Insect larvae eat them, the toxin is released in the gut "
    "and the larvae are killed, while other insects remain unharmed. NCERT names butterfly caterpillars as the "
    "target.",
    ["Bt → toxin released in larval gut → kills butterfly caterpillars"],
    C12_MHW("microbes as biocontrol agents"),
    why="Aphids are controlled by ladybird beetles; fungal pathogens by Trichoderma; Bt is not a biofertiliser.",
    seconds=20)

add(MHW, "Household and industrial products", "Intermediate", "match_list",
    ml(("microbe", "organic acid produced"),
       ["Aspergillus niger", "Acetobacter aceti", "Clostridium butylicum", "Lactobacillus"],
       ["Lactic acid", "Butyric acid", "Citric acid", "Acetic acid"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
       {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C"),
    "Commercial production of organic acids by microbes",
    "Microbes are used industrially to make organic acids.",
    ["Aspergillus niger (fungus) → citric acid (A-III)", "Acetobacter aceti (bacterium) → acetic acid (B-IV)",
     "Clostridium butylicum (bacterium) → butyric acid (C-II)", "Lactobacillus (bacterium) → lactic acid (D-I)"],
    C12_MHW("microbes in industrial products: chemicals, enzymes and other bioactive molecules"),
    seconds=35)

add(MHW, "Sewage treatment", "Intermediate", "assertion_reason",
    ar("In sewage treatment, the primary sludge is passed into large aeration tanks.",
       "In aeration tanks, the vigorous growth of aerobic microbes into flocs consumes the major part of the organic "
       "matter and significantly reduces the BOD of the effluent."),
    AR("D"),
    "Primary and secondary sewage treatment",
    "Primary treatment removes particles by filtration and sedimentation. The settled solids form the primary "
    "sludge; the supernatant, the primary effluent, is what goes to the aeration tanks for secondary (biological) "
    "treatment. There, aerobic bacteria and fungi grow as flocs and consume organic matter, cutting the BOD. So A is "
    "false and R is true.",
    ["Primary effluent (not sludge) → aeration tanks → A false", "Flocs reduce BOD → R true"],
    C12_MHW("microbes in sewage treatment"),
    why="A swaps primary sludge with primary effluent; the second clause (R) is correct as written.",
    seconds=45)

add(MHW, "Household and industrial products", "Intermediate", "statement_pair",
    sp("Streptokinase, produced by the bacterium Streptococcus and modified by genetic engineering, is used as a "
       "'clot buster' to remove clots from blood vessels.",
       "Cyclosporin A, used as an immunosuppressive agent in organ-transplant patients, is produced by the fungus "
       "Trichoderma polysporum."),
    SP("A"),
    "Bioactive molecules from microbes",
    "Streptokinase from Streptococcus, modified by genetic engineering, is used as a clot buster in patients who "
    "have had myocardial infarction. Cyclosporin A, an immunosuppressant used in organ transplantation, is made by "
    "the fungus Trichoderma polysporum.",
    ["Statement I: true", "Statement II: true"],
    C12_MHW("microbes in industrial products: chemicals, enzymes and other bioactive molecules"),
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "multi_statement",
    ms("Which of the following statements are correct?",
       ["Fungi of the genus Glomus form mycorrhiza and help the plant absorb phosphorus from the soil.",
        "Rhizobium fixes atmospheric nitrogen only while living free in the soil, without forming root nodules.",
        "Anabaena, Nostoc and Oscillatoria are cyanobacteria that can fix atmospheric nitrogen.",
        "Baculoviruses of the genus Nucleopolyhedrovirus are broad-spectrum insecticides that also harm non-target "
        "insects.",
        "Trichoderma species are free-living fungi that act as biocontrol agents against several plant pathogens."]),
    P("(a), (c) and (e) only",
      ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"], "B"),
    "Biofertilisers and biocontrol agents",
    "Glomus forms mycorrhiza and helps phosphorus uptake. Rhizobium fixes nitrogen symbiotically in root nodules of "
    "legumes; Azospirillum and Azotobacter are the free-living fixers. Cyanobacteria fix nitrogen, important in "
    "paddy fields. Baculoviruses (Nucleopolyhedrovirus) are species-specific, narrow-spectrum insecticides with no "
    "negative effect on non-target insects, so they suit IPM. Trichoderma is a free-living fungal biocontrol agent.",
    ["(a) True", "(b) False: Rhizobium is symbiotic in root nodules",
     "(c) True", "(d) False: baculoviruses are narrow-spectrum and spare non-target insects", "(e) True"],
    C12_MHW("microbes as biocontrol agents; microbes as biofertilisers"),
    why="Every option except B includes (b) or (d), each of which reverses an NCERT statement.",
    seconds=60)

add(MHW, "Household and industrial products", "Advanced", "statement_pair",
    sp("Wine and beer are produced by distilling the fermented broth, whereas whisky, brandy and rum are produced "
       "without distillation.",
       "Statins produced by Monascus purpureus lower blood cholesterol by competitively inhibiting the enzyme "
       "responsible for cholesterol synthesis."),
    SP("D"),
    "Alcoholic beverages; statins",
    "Wine and beer are produced without distillation, while whisky, brandy and rum are made by distilling the "
    "fermented broth; Statement I swaps the two groups. Statins from Monascus purpureus act as "
    "competitive inhibitors of the enzyme responsible for cholesterol synthesis, so Statement II is true.",
    ["Statement I: reversed → false", "Statement II: true"],
    C12_MHW("microbes in industrial products: fermented beverages; bioactive molecules"),
    why="Statement I keeps the right beverages but reverses the process, a common NEET trap.",
    seconds=45)

add(MHW, "Household and industrial products", "Advanced", "direct",
    "Which of the following statements about microbes in household products is correct?",
    P("Lactic acid bacteria convert milk to curd and also increase its vitamin B₁₂ content",
      ["Lactic acid bacteria convert milk to curd by producing ethyl alcohol",
       "In our stomach, lactic acid bacteria are harmful because they produce toxins",
       "Roquefort cheese is ripened by growing a specific bacterium on it"], "C"),
    "Lactic acid bacteria and cheese",
    "LAB grow in milk and produce acids that coagulate and partially digest the milk proteins, forming curd. They "
    "also improve its nutritional quality by increasing vitamin B₁₂. In our stomach, LAB play a beneficial role in "
    "checking disease-causing microbes. Roquefort cheese is ripened by growing a specific fungus on it.",
    ["Curd: acid (lactic) production by LAB, plus more vitamin B₁₂ → correct",
     "LAB in the stomach: beneficial", "Roquefort: fungus, not bacterium"],
    C12_MHW("microbes in household products"),
    why="LAB produce acid, not alcohol; they are beneficial in the gut; Roquefort ripening uses a fungus.",
    seconds=40)

# ================================================================ Organisms and Populations (4 / 5 / 4)
C12_OAP = lambda s: ref(12, OAP, s)

add(OAP, "Population interactions", "Basic", "direct",
    "An interaction in which one species benefits and the other is neither harmed nor benefited is called:",
    P("Commensalism", ["Amensalism", "Mutualism", "Competition"], "B"),
    "Types of population interactions",
    "Interactions are classified by the effect on each species: mutualism (+, +), competition (−, −), predation and "
    "parasitism (+, −), commensalism (+, 0) and amensalism (−, 0).",
    ["One benefits (+), other unaffected (0) → commensalism"],
    C12_OAP("population interactions"),
    why="Amensalism is (−, 0), mutualism (+, +) and competition (−, −).",
    seconds=20)

add(OAP, "Population growth", "Basic", "direct",
    "In the logistic growth equation dN/dt = rN[(K − N)/K], the symbol K stands for:",
    P("The carrying capacity of the habitat",
      ["The intrinsic rate of natural increase", "The population density at time t", "The number of births per unit "
       "time"], "D"),
    "Logistic (Verhulst–Pearl) growth",
    "In a habitat with limited resources, the population grows until it reaches the maximum the habitat can "
    "support. This limit is the carrying capacity, K. N is the population density at time t and r is the intrinsic "
    "rate of natural increase.",
    ["K = carrying capacity", "N = population density at time t", "r = intrinsic rate of natural increase"],
    C12_OAP("population growth: logistic growth"),
    why="r, N and births are separate terms; K is the upper limit set by resources.",
    seconds=20)

add(OAP, "Population attributes", "Basic", "direct",
    "An age pyramid with a broad base, i.e. a large proportion of pre-reproductive individuals, indicates a "
    "population that is:",
    P("Expanding (growing)", ["Declining", "Stable", "At its carrying capacity and about to crash"], "C"),
    "Age pyramids",
    "Plotting pre-reproductive, reproductive and post-reproductive individuals gives an age pyramid. A broad base "
    "(many young individuals) shows a growing population, a bell shape a stable one, and a narrow base a declining "
    "one.",
    ["Broad base → many young → expanding", "Bell-shaped → stable", "Narrow base (urn-shaped) → declining"],
    C12_OAP("population attributes"),
    why="A declining population has a narrow base; a stable one is bell-shaped.",
    seconds=20)

add(OAP, "Population interactions", "Basic", "direct",
    "The Mediterranean orchid Ophrys gets pollinated by a species of bee through:",
    P("Sexual deceit: one petal resembles the female bee and the male bee 'pseudocopulates' with the flower",
      ["Offering large amounts of nectar as a reward", "Providing a site for the bee to lay its eggs",
       "Trapping the bee inside the flower until pollination is complete"], "B"),
    "Plant–pollinator mutualism and sexual deceit",
    "One petal of the Ophrys flower looks like a female bee in size, colour and markings. The male bee tries to mate "
    "with it ('pseudocopulation') and is dusted with pollen, which it transfers to another flower. If the female "
    "bee's colour pattern changes slightly in evolution, pollination success falls unless the orchid flower "
    "co-evolves.",
    ["Petal mimics female bee → male bee pseudocopulates → pollen transferred"],
    C12_OAP("population interactions: mutualism"),
    why="Nectar is a common floral reward, but not Ophrys's strategy. Egg-laying in the flower describes the "
        "fig–wasp and Yucca–moth relationships.",
    seconds=30)

add(OAP, "Population attributes", "Intermediate", "numerical",
    "A laboratory population of 250 fruit flies produced 50 offspring and lost 25 individuals to death during one "
    "week. The birth rate and death rate of this population, per individual per week, are respectively:",
    P("0.2 and 0.1", ["50 and 25", "0.1 and 0.2", "0.18 and 0.09"], "A"),
    "Birth rate and death rate as per capita rates",
    "Birth and death rates are expressed per individual of the population at the start of the period, i.e. as "
    "rates relative to the members of the population.",
    ["Birth rate = 50 / 250 = 0.2 offspring per fly per week",
     "Death rate = 25 / 250 = 0.1 death per fly per week"],
    C12_OAP("population attributes"),
    why="50 and 25 are absolute numbers, not rates per individual. 0.1 and 0.2 swap the two rates. 0.18 and 0.09 "
        "divide by the population at the end of the week (275).",
    seconds=50, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("The monarch butterfly is highly distasteful to its predators, such as birds.",
       "During its caterpillar stage, the monarch butterfly feeds on a poisonous weed and acquires a special "
       "chemical from it."),
    AR("A"),
    "Chemical defence against predators",
    "Prey species have evolved defences against predation. The monarch butterfly acquires a chemical from a "
    "poisonous weed it eats as a caterpillar; this chemical makes the adult distasteful to birds. R gives the cause "
    "of A.",
    ["A: true", "R: true", "Chemical from the weed → distasteful → R explains A"],
    C12_OAP("population interactions: predation"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "match_list",
    ml(("example", "interaction"),
       ["Cuscuta growing on hedge plants", "An orchid growing as an epiphyte on a mango branch",
        "Lichens", "Balanus and Chthamalus on the rocky sea coasts of Scotland"],
       ["Mutualism", "Competition", "Commensalism", "Parasitism"]),
    M({"A": "IV", "B": "III", "C": "I", "D": "II"},
      [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "I", "C": "III", "D": "II"},
       {"A": "IV", "B": "III", "C": "II", "D": "I"}], "D"),
    "Examples of population interactions",
    "Each example is an NCERT illustration of one interaction.",
    ["Cuscuta: a parasitic plant without chlorophyll that takes nutrition from the host → parasitism (A-IV)",
     "Epiphytic orchid on mango: orchid benefits, mango unaffected → commensalism (B-III)",
     "Lichen: fungus and photosynthesising alga or cyanobacterium both benefit → mutualism (C-I)",
     "Connell's barnacles: the larger Balanus excludes Chthamalus from the intertidal zone → competition (D-II)"],
    C12_OAP("population interactions"),
    seconds=40)

add(OAP, "Population growth", "Intermediate", "statement_pair",
    sp("Exponential growth occurs when resources in the habitat are limited, and it gives an S-shaped curve.",
       "A population growing in a habitat with limited resources shows an initial lag phase, followed by phases "
       "of acceleration and deceleration, and finally an asymptote when the population density reaches the "
       "carrying capacity."),
    SP("D"),
    "Exponential and logistic growth",
    "Exponential growth happens when resources are unlimited; plotting N against time gives a J-shaped curve. With "
    "limited resources, growth is logistic: lag, acceleration, deceleration and an asymptote at K, giving a "
    "sigmoid (S-shaped) curve.",
    ["Statement I: exponential growth needs unlimited resources and gives a J-shaped curve → false",
     "Statement II: correct description of logistic growth → true"],
    C12_OAP("population growth"),
    seconds=40)

add(OAP, "Population attributes", "Intermediate", "direct",
    "For estimating the number of tigers in our national parks and tiger reserves, the tiger census is often based "
    "on:",
    P("Pug marks and fecal pellets", ["Percent cover of the area", "Total biomass of the tigers",
                                      "Number of tigers caught per trap"], "C"),
    "Indirect estimation of population size",
    "Population size need not be counted directly. For tigers, the census in national parks and tiger reserves is "
    "often based on pug marks and fecal pellets.",
    ["Large, elusive animals → indirect indices → pug marks and fecal pellets"],
    C12_OAP("population attributes"),
    why="Percent cover and biomass suit plants such as Parthenium or a banyan tree; catch per trap is used for fish.",
    seconds=25)

add(OAP, "Population growth", "Advanced", "direct",
    "For a population showing logistic growth according to dN/dt = rN[(K − N)/K], which statement is correct?",
    P("As N approaches K, the growth rate dN/dt approaches zero",
      ["The growth rate dN/dt is highest when N equals K",
       "When N is very small compared with K, the growth rate is zero",
       "The growth rate is the same at every population density"], "B"),
    "Behaviour of the logistic equation",
    "The factor (K − N)/K shrinks as N rises. When N is far below K the factor is close to 1 and growth is nearly "
    "exponential (rN). When N reaches K, (K − N) = 0, so dN/dt = 0: the population has reached its asymptote.",
    ["N ≪ K: (K − N)/K ≈ 1 → dN/dt ≈ rN (fast growth)", "N = K: (K − N)/K = 0 → dN/dt = 0"],
    C12_OAP("population growth: logistic growth"),
    why="At N = K the growth rate is zero, not maximum. At small N it is close to rN, not zero. The rate clearly "
        "changes with N.",
    seconds=50)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    ms("Which of the following statements about competition and parasitism are correct?",
       ["The Abingdon tortoise of the Galapagos Islands became extinct within a decade after goats were introduced, "
        "apparently due to the greater browsing efficiency of the goats.",
        "Gause's competitive exclusion principle states that two closely related species competing for the same "
        "resources cannot co-exist indefinitely, and the competitively inferior one will be eliminated.",
        "MacArthur found that five closely related species of warblers living on the same tree could not co-exist, "
        "and all but one were eliminated.",
        "The cuckoo (koel) lays its eggs in the nest of its host, the crow, which incubates them; this is brood "
        "parasitism.",
        "In amensalism, both interacting species are harmed."]),
    P("(a), (b) and (d) only",
      ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"], "D"),
    "Competition, resource partitioning and brood parasitism",
    "The Abingdon tortoise is NCERT's example of competition. Gause's principle says two closely related species "
    "competing for the same resources cannot co-exist indefinitely. MacArthur's warblers avoided competition and "
    "co-existed because of behavioural differences in their foraging activities (resource partitioning). The "
    "cuckoo is a brood parasite of the crow. In amensalism one species is harmed and the other unaffected.",
    ["(a) True", "(b) True", "(c) False: the warblers co-existed by resource partitioning", "(d) True",
     "(e) False: amensalism is (−, 0); both harmed is competition"],
    C12_OAP("population interactions: competition; parasitism"),
    why="Options A, B and C each contain (c) or (e).",
    seconds=70)

add(OAP, "Population interactions", "Advanced", "assertion_reason",
    ar("The human liver fluke depends on two intermediate hosts, a snail and a fish, to complete its life cycle.",
       "Parasites that feed on the external surface of the host organism are called ectoparasites."),
    AR("B"),
    "Complex life cycles of parasites; ectoparasites",
    "Many parasites have complex life cycles with one or two intermediate hosts or vectors; the human liver fluke, "
    "a trematode, needs a snail and a fish. So A is true. Ectoparasites (lice on humans, ticks on dogs) feed on "
    "the external surface of the host, so R is true. But the liver fluke is an endoparasite living inside its host, "
    "so the definition of ectoparasites cannot explain its life cycle.",
    ["A: true (NCERT example)", "R: true (definition)", "Liver fluke is an endoparasite → R is unrelated to A"],
    C12_OAP("population interactions: parasitism"),
    why="Option A is the trap: both statements are about parasites and both are true, but R does not explain A.",
    seconds=45)

add(OAP, "Population interactions", "Advanced", "statement_pair",
    sp("The prickly pear cactus introduced into Australia spread rapidly and was brought under control only after a "
       "cactus-feeding predator (a moth) from its natural habitat was introduced.",
       "Predators help to maintain species diversity in a community by reducing the intensity of competition among "
       "competing prey species."),
    SP("A"),
    "Roles of predators in nature",
    "An exotic species can spread fast in a new area because its natural predators are absent; the prickly pear in "
    "Australia was controlled only after a cactus-feeding moth from its native range was introduced. Predators also "
    "keep prey populations in check and so reduce competition among prey species, helping maintain diversity.",
    ["Statement I: true (NCERT example; the basis of biological control)", "Statement II: true"],
    C12_OAP("population interactions: predation"),
    seconds=40)

# ================================================================ Ecosystem (3 / 5 / 4)
C12_ECO = lambda s: ref(12, ECO, s)

add(ECO, "Ecological pyramids", "Basic", "direct",
    "The mass of living material present at a particular trophic level at a particular time is called the:",
    P("Standing crop", ["Net primary productivity", "Detritus", "Secondary productivity"], "C"),
    "Standing crop",
    "Each trophic level has a certain mass of living material at a given time, called the standing crop. It is "
    "measured as the biomass of living organisms or as their number per unit area. It is a quantity present at one "
    "time, not a rate.",
    ["Mass of living material at a trophic level, at one time → standing crop"],
    C12_ECO("energy flow; ecological pyramids"),
    why="Productivity terms are rates of production of organic matter; detritus is dead organic matter.",
    seconds=20)

add(ECO, "Structure and components", "Basic", "direct",
    "In an aquatic ecosystem, the primary producers are mainly:",
    P("Phytoplankton, some algae and higher plants", ["Zooplankton", "Fishes", "Fungi and bacteria"], "D"),
    "Producers in different ecosystems",
    "All organisms depend on producers for food. In terrestrial ecosystems the major producers are herbaceous and "
    "woody plants; in aquatic ecosystems they are phytoplankton, some algae and higher plants.",
    ["Producers make food by photosynthesis", "Aquatic producers: phytoplankton, some algae, higher plants"],
    C12_ECO("energy flow: producers"),
    why="Zooplankton and fishes are consumers; fungi and bacteria are decomposers.",
    seconds=20)

add(ECO, "Energy flow", "Basic", "direct",
    "The detritus food chain (DFC) begins with:",
    P("Dead organic matter", ["Living green plants", "Herbivores", "Top carnivores"], "B"),
    "Grazing and detritus food chains",
    "The grazing food chain starts with producers. The detritus food chain starts with dead organic matter "
    "(detritus) and is made up of decomposers, heterotrophs such as fungi and bacteria (saprotrophs), that meet "
    "their energy and nutrient needs by degrading it.",
    ["GFC: producer → herbivore → carnivore", "DFC: dead organic matter → decomposers"],
    C12_ECO("energy flow: food chains"),
    why="Living green plants start the grazing food chain; herbivores and carnivores are later links.",
    seconds=20)

add(ECO, "Productivity and decomposition", "Intermediate", "statement_pair",
    sp("Decomposition is slower when the detritus is rich in lignin and chitin.",
       "A warm and moist environment favours decomposition, whereas low temperature and anaerobiosis inhibit it."),
    SP("A"),
    "Factors that regulate decomposition",
    "Decomposition depends on the chemical composition of the detritus and on climate. Detritus rich in lignin and "
    "chitin decomposes slowly; detritus rich in nitrogen and water-soluble substances such as sugars decomposes "
    "faster. Temperature and soil moisture regulate the activity of soil microbes: warmth and moisture favour "
    "decomposition, while cold and lack of oxygen inhibit it, so organic matter builds up.",
    ["Statement I: true (chemical composition)", "Statement II: true (climatic factors)"],
    C12_ECO("decomposition"),
    seconds=35)

add(ECO, "Ecological pyramids", "Intermediate", "assertion_reason",
    ar("The pyramid of energy is always upright and can never be inverted.",
       "When energy flows from one trophic level to the next, some energy is always lost as heat at each step."),
    AR("A"),
    "Why the energy pyramid is always upright",
    "Each trophic level receives only part of the energy of the level below, because some is lost as heat at "
    "every transfer (in line with the second law of thermodynamics). So each higher level always has less energy "
    "than the one below, and the energy pyramid cannot be inverted. R explains A.",
    ["A: true", "R: true", "Loss at every step → each higher level has less energy → always upright"],
    C12_ECO("ecological pyramids"),
    seconds=35)

add(ECO, "Productivity and decomposition", "Intermediate", "match_list",
    ml(("step of decomposition", "what happens"),
       ["Fragmentation", "Leaching", "Catabolism", "Humification"],
       ["Bacterial and fungal enzymes degrade detritus into simpler inorganic substances",
        "Water-soluble inorganic nutrients go down into the soil horizon and are precipitated as unavailable salts",
        "Accumulation of a dark-coloured, amorphous substance that is highly resistant to microbial action",
        "Detritivores such as earthworms break detritus into smaller particles"]),
    M({"A": "IV", "B": "II", "C": "I", "D": "III"},
      [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "IV", "B": "I", "C": "II", "D": "III"}], "C"),
    "Steps of decomposition",
    "Decomposition breaks complex organic matter into inorganic substances through fragmentation, leaching, "
    "catabolism, humification and mineralisation.",
    ["Fragmentation: detritivores (earthworm) → smaller particles (A-IV)",
     "Leaching: soluble nutrients move down and precipitate (B-II)",
     "Catabolism: microbial enzymes → simpler inorganic substances (C-I)",
     "Humification: humus, dark, amorphous, resistant (D-III)"],
    C12_ECO("decomposition"),
    seconds=45)

add(ECO, "Energy flow", "Intermediate", "multi_statement",
    ms("Which of the following statements about energy flow in ecosystems are correct?",
       ["Except for deep-sea hydrothermal ecosystems, the sun is the only source of energy for all ecosystems on "
        "Earth.",
        "More than 80 per cent of the incident solar radiation is photosynthetically active radiation (PAR).",
        "Ecosystems are exempt from the second law of thermodynamics.",
        "Plants capture only 2–10 per cent of the PAR, and this small amount sustains the entire living world.",
        "Energy moves in one direction, from producers towards the higher trophic levels, and is lost as heat to "
        "the environment."]),
    P("(a), (d) and (e) only",
      ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"], "D"),
    "Energy flow and the laws of thermodynamics",
    "Of the incident solar radiation, less than 50% is PAR, and plants capture only 2–10% of it. Ecosystems are not "
    "exempt from the second law of thermodynamics: they need a constant supply of energy to synthesise molecules "
    "and counteract the universal tendency towards disorder. Energy flow is unidirectional, from the sun to "
    "producers and then to consumers.",
    ["(a) True", "(b) False: less than 50% of incident radiation is PAR", "(c) False",
     "(d) True", "(e) True"],
    C12_ECO("energy flow"),
    why="Options A, B and C contain (b) or (c), which reverse NCERT statements.",
    seconds=60)

add(ECO, "Ecological pyramids", "Intermediate", "direct",
    "The pyramid of biomass in a sea is generally inverted because:",
    P("The biomass of fishes far exceeds that of the phytoplankton",
      ["Phytoplankton have a greater biomass than all the consumers together",
       "Energy increases at each higher trophic level in the sea",
       "Decomposers are placed at the base of the pyramid in the sea"], "B"),
    "Inverted pyramid of biomass",
    "In the sea, the standing crop of phytoplankton at any moment is small, although they reproduce fast. The "
    "biomass of fishes is much larger. Biomass increases at higher trophic levels, so the pyramid of biomass is "
    "inverted. The pyramid of energy still remains upright.",
    ["Small standing crop of phytoplankton", "Large biomass of fishes", "Biomass increases upwards → inverted"],
    C12_ECO("ecological pyramids"),
    why="If phytoplankton had the larger biomass, the pyramid would be upright. Energy never increases upwards. "
        "Decomposers are not given a place in ecological pyramids.",
    seconds=35)

add(ECO, "Energy flow", "Advanced", "numerical",
    "In the food chain grass → grasshopper → frog → snake → hawk, the grass fixes 1,00,000 J of energy. Assuming the "
    "10 per cent law, how much energy is available to the hawk?",
    P("10 J", ["100 J", "1 J", "1000 J"], "C"),
    "Ten per cent law of energy transfer",
    "Only about 10% of the energy at one trophic level is transferred to the next. Count the number of transfers "
    "from the grass to the hawk.",
    ["Grass → grasshopper: 1,00,000 × 0.1 = 10,000 J", "Grasshopper → frog: 1000 J", "Frog → snake: 100 J",
     "Snake → hawk: 10 J"],
    C12_ECO("energy flow"),
    shortcut="Four transfers: 1,00,000 × (0.1)⁴ = 10 J.",
    why="100 J counts only three transfers (energy reaching the snake). 1000 J is the energy reaching the frog. "
        "1 J counts five transfers.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Ecological pyramids", "Advanced", "statement_pair",
    sp("Ecological pyramids assume a simple food chain, something that almost never exists in nature, and do not "
       "accommodate a food web.",
       "Saprophytes are given a separate trophic level at the apex of ecological pyramids."),
    SP("C"),
    "Limitations of ecological pyramids",
    "NCERT lists the limitations of ecological pyramids: they do not take into account the same species belonging "
    "to two or more trophic levels; they assume a simple food chain and do not accommodate a food web; and "
    "saprophytes are not given any place in ecological pyramids even though they play a vital role in the "
    "ecosystem.",
    ["Statement I: true", "Statement II: saprophytes have no place in the pyramids → false"],
    C12_ECO("ecological pyramids"),
    seconds=40)

add(ECO, "Energy flow", "Advanced", "assertion_reason",
    ar("In most terrestrial ecosystems, a much larger fraction of energy flows through the detritus food chain than "
       "through the grazing food chain.",
       "In an aquatic ecosystem, the grazing food chain is the major conduit for energy flow."),
    AR("B"),
    "GFC and DFC in different ecosystems",
    "NCERT states both facts: in aquatic ecosystems the GFC is the major conduit for energy flow, whereas in "
    "terrestrial ecosystems a much larger fraction of energy flows through the DFC. R describes aquatic "
    "ecosystems, so it cannot explain a statement about terrestrial ones.",
    ["A: true (terrestrial)", "R: true (aquatic)", "Different ecosystems → R does not explain A"],
    C12_ECO("energy flow: food chains"),
    why="Option A is the trap: the two statements form a contrast, not a cause and effect.",
    seconds=45)

add(ECO, "Energy flow", "Advanced", "multi_statement",
    ms("Which of the following statements about food chains and trophic levels are correct?",
       ["A sparrow is a primary consumer when it eats seeds and fruits, and a secondary consumer when it eats "
        "insects and worms.",
        "The number of trophic levels in a grazing food chain is restricted because only about 10 per cent of the "
        "energy is transferred from one trophic level to the next.",
        "Decomposers are heterotrophic organisms, mainly fungi and bacteria, that meet their energy and nutrient "
        "needs by degrading dead organic matter.",
        "The detritus food chain is not connected to the grazing food chain at any level.",
        "Herbivores are called secondary consumers."]),
    P("(a), (b) and (c) only",
      ["(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"], "D"),
    "Food chains, food webs and trophic levels",
    "A species can occupy more than one trophic level at the same time, as the sparrow does. Because only about 10% "
    "of energy passes to each higher level, grazing food chains have few trophic levels. Decomposers are "
    "saprotrophs, mainly fungi and bacteria. The DFC may be connected with the GFC at some levels (some DFC "
    "organisms are prey to GFC animals), forming food webs. Herbivores are primary consumers.",
    ["(a) True", "(b) True", "(c) True", "(d) False: the two chains are connected at some levels",
     "(e) False: herbivores are primary consumers"],
    C12_ECO("energy flow: food chains and food webs"),
    why="Options A, B and C each include (d) or (e).",
    seconds=60)

# ================================================================ Biodiversity and Conservation (3 / 5 / 3)
C12_BDC = lambda s: ref(12, BDC, s)

add(BDC, "Hotspots and Red Data Book", "Basic", "direct",
    "Which of the following is NOT one of the biodiversity hotspots that cover India's regions of exceptionally high "
    "biodiversity?",
    P("Eastern Ghats", ["Western Ghats and Sri Lanka", "Indo-Burma", "Himalaya"], "D"),
    "Biodiversity hotspots and India",
    "Of the 34 biodiversity hotspots in the world, three cover India's exceptionally high biodiversity regions: "
    "the Western Ghats and Sri Lanka, Indo-Burma, and the Himalaya. The Eastern Ghats are not among them.",
    ["India's hotspots: Western Ghats and Sri Lanka; Indo-Burma; Himalaya", "Eastern Ghats → not a hotspot"],
    C12_BDC("biodiversity conservation: how do we conserve biodiversity"),
    why="The other three options are exactly the three hotspots NCERT names.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "During his pioneering explorations in the wilderness of South American jungles, who observed that within a "
    "region species richness increases with increasing explored area, but only up to a limit?",
    P("Alexander von Humboldt", ["Paul Ehrlich", "David Tilman", "Edward Wilson"], "B"),
    "Species–area relationship",
    "The German naturalist and geographer Alexander von Humboldt observed the species–area relationship. On a "
    "logarithmic scale it is a straight line: log S = log C + Z log A.",
    ["Species–area relationship → Alexander von Humboldt"],
    C12_BDC("patterns of biodiversity: species-area relationships"),
    why="Ehrlich proposed the rivet popper hypothesis; Tilman ran long-term ecosystem experiments on stability; "
        "Wilson popularised the term biodiversity.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "The introduction of the Nile perch into Lake Victoria in East Africa led to the extinction of more than 200 "
    "species of:",
    P("Cichlid fish", ["Catfish", "Frogs", "Water snails"], "D"),
    "Alien species invasions",
    "When alien species are introduced, some become invasive and cause decline or extinction of indigenous species. "
    "The Nile perch introduced into Lake Victoria eventually led to the extinction of an ecologically unique "
    "assemblage of more than 200 species of cichlid fish.",
    ["Nile perch in Lake Victoria → loss of >200 cichlid fish species → alien species invasion"],
    C12_BDC("loss of biodiversity: causes"),
    why="Catfish is the trap: the threat to indigenous catfishes in Indian rivers comes from the African catfish "
        "Clarias gariepinus, a different example.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Intermediate", "direct",
    "On a logarithmic scale the species–area relationship is a straight line, log S = log C + Z log A. When very "
    "large areas such as entire continents are analysed, the slope Z of the line is:",
    P("Much steeper, in the range 0.6 to 1.2",
      ["In the range 0.1 to 0.2, as for any region", "Close to zero", "Negative"], "B"),
    "Regression coefficient Z in the species–area relationship",
    "For smaller areas, Z values lie in the range 0.1 to 0.2, regardless of the taxonomic group or region. When "
    "very large areas such as entire continents are analysed, the slope becomes much steeper, with Z values of "
    "0.6 to 1.2. For frugivorous birds and mammals in the tropical forests of different continents the slope is "
    "1.15.",
    ["Small regions: Z ≈ 0.1–0.2", "Very large areas (continents): Z ≈ 0.6–1.2"],
    C12_BDC("patterns of biodiversity: species-area relationships"),
    why="0.1–0.2 is the usual range for smaller areas. Species richness rises with area, so Z is positive.",
    seconds=35)

add(BDC, "Patterns of biodiversity", "Intermediate", "statement_pair",
    sp("Although India has only 2.4 per cent of the world's land area, its share of the global species diversity is "
       "an impressive 8.1 per cent.",
       "India is one of the 12 megadiversity countries of the world."),
    SP("A"),
    "Biodiversity of India",
    "India has 2.4% of the world's land area but 8.1% of global species diversity, which makes it one of the 12 "
    "megadiversity countries. Nearly 45,000 species of plants and twice as many animals have been recorded from "
    "India.",
    ["Statement I: true", "Statement II: true"],
    C12_BDC("biodiversity: how many species are there on earth and how many in India"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Intermediate", "assertion_reason",
    ar("In general, species diversity decreases as we move away from the equator towards the poles.",
       "Tropical environments, unlike temperate ones, are less seasonal, relatively more constant and predictable, "
       "which promotes niche specialisation and leads to greater species diversity."),
    AR("A"),
    "Latitudinal gradient in species diversity",
    "Tropics (23.5° N to 23.5° S) harbour more species than temperate or polar areas; for example Colombia has "
    "nearly 1400 species of birds while New York has 105 and Greenland 56. One of NCERT's explanations is that "
    "tropical environments are less seasonal and more constant and predictable, which promotes niche "
    "specialisation and greater diversity. R is one of the accepted reasons for A.",
    ["A: true (latitudinal gradient)", "R: true and one of the NCERT explanations for the gradient"],
    C12_BDC("patterns of biodiversity: latitudinal gradients"),
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "match_list",
    ml(("extinct animal", "where it lived"),
       ["Dodo", "Quagga", "Thylacine", "Steller's sea cow"],
       ["Russia", "Africa", "Mauritius", "Australia"]),
    M({"A": "III", "B": "II", "C": "IV", "D": "I"},
      [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
       {"A": "III", "B": "II", "C": "I", "D": "IV"}], "D"),
    "Recent extinctions",
    "The IUCN Red List (2004) documents 784 extinctions in the last 500 years. NCERT gives these examples with their "
    "regions.",
    ["Dodo → Mauritius (A-III)", "Quagga → Africa (B-II)", "Thylacine → Australia (C-IV)",
     "Steller's sea cow → Russia (D-I)"],
    C12_BDC("loss of biodiversity"),
    seconds=35)

add(BDC, "Importance and loss", "Intermediate", "multi_statement",
    ms("Which of the following statements about the causes of biodiversity loss are correct?",
       ["Habitat loss and fragmentation is the most important cause driving animals and plants to extinction.",
        "Steller's sea cow and the passenger pigeon became extinct in the last 500 years due to over-exploitation "
        "by humans.",
        "The illegal introduction of the African catfish Clarias gariepinus for aquaculture poses a threat to the "
        "indigenous catfishes of our rivers.",
        "When a host fish species becomes extinct, its unique assemblage of parasites also meets the same fate.",
        "Parthenium, Lantana and water hyacinth are native Indian species threatened by over-exploitation."]),
    P("(a), (b), (c) and (d) only",
      ["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (b), (c), (d) and (e)"], "A"),
    "The 'Evil Quartet'",
    "The four major causes of biodiversity loss are habitat loss and fragmentation (the most important), "
    "over-exploitation, alien species invasions and co-extinctions. Parthenium (carrot grass), Lantana and water "
    "hyacinth (Eichhornia) are invasive alien weeds that threaten native species; they are not native species "
    "threatened by over-exploitation.",
    ["(a) True: habitat loss", "(b) True: over-exploitation", "(c) True: alien species invasion",
     "(d) True: co-extinction", "(e) False: they are invasive alien weeds"],
    C12_BDC("loss of biodiversity: causes"),
    why="Options B, C and D include (e).",
    seconds=55)

add(BDC, "Importance and loss", "Advanced", "statement_pair",
    sp("David Tilman's long-term ecosystem experiments using outdoor plots showed that plots with more species had "
       "less year-to-year variation in total biomass.",
       "The 'rivet popper' hypothesis, which compares species in an ecosystem to the rivets of an airplane, was "
       "proposed by David Tilman."),
    SP("C"),
    "Biodiversity and ecosystem stability",
    "Tilman found that plots with more species showed less year-to-year variation in total biomass and that "
    "increased diversity contributed to higher productivity. The rivet popper hypothesis was proposed by the "
    "Stanford ecologist Paul Ehrlich: losing rivets (species) on key parts such as the wings is a more serious "
    "threat than losing a few on the seats.",
    ["Statement I: true", "Statement II: proposed by Paul Ehrlich, not Tilman → false"],
    C12_BDC("importance of species diversity to the ecosystem"),
    why="Both ideas are about stability and come from the same NCERT section, which makes the swap of names easy "
        "to miss.",
    seconds=45)

add(BDC, "Hotspots and Red Data Book", "Advanced", "assertion_reason",
    ar("All the biodiversity hotspots of the world put together cover less than 2 per cent of the earth's land "
       "area.",
       "Biodiversity hotspots are identified on the basis of very high levels of species richness and a high degree "
       "of endemism."),
    AR("B"),
    "Biodiversity hotspots",
    "Hotspots are regions with very high species richness and a high degree of endemism. Together they cover less "
    "than 2% of the earth's land area, yet the number of species they harbour is extremely high, and strict "
    "protection of them could reduce ongoing mass extinctions by almost 30%. The criteria in R define what a "
    "hotspot is; they do not explain why the hotspots together occupy so small an area.",
    ["A: true", "R: true", "R gives the criteria, not the reason for the small total area → B"],
    C12_BDC("biodiversity conservation: hotspots"),
    why="Option A is the trap: R is the definition of a hotspot, which does not account for their total area.",
    seconds=45)

add(BDC, "In situ and ex situ conservation", "Advanced", "multi_statement",
    ms("Which of the following statements about conservation of biodiversity are correct?",
       ["Biosphere reserves, national parks and wildlife sanctuaries are means of in situ conservation.",
        "Zoological parks, botanical gardens and wildlife safari parks are means of ex situ conservation.",
        "Preserving gametes of threatened species by cryopreservation is a method of in situ conservation.",
        "Sacred groves are found in the Khasi and Jaintia Hills of Meghalaya.",
        "Seed banks conserve plants in their natural habitat."]),
    P("(a), (b) and (d) only",
      ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"], "C"),
    "In situ and ex situ conservation",
    "In situ (on site) conservation protects the whole ecosystem: biosphere reserves, national parks, wildlife "
    "sanctuaries and sacred groves (Khasi and Jaintia Hills, Aravalli Hills, Western Ghats, Sarguja, Chanda and "
    "Bastar). Ex situ (off site) conservation removes threatened species from their habitat: zoological parks, "
    "botanical gardens, wildlife safari parks, cryopreservation of gametes, and seed banks.",
    ["(a) True: in situ", "(b) True: ex situ", "(c) False: cryopreservation is ex situ", "(d) True",
     "(e) False: seed banks store seeds away from the habitat (ex situ)"],
    C12_BDC("biodiversity conservation: in situ and ex situ conservation"),
    why="Options A, B and D include (c) or (e), both ex situ methods described as in situ.",
    seconds=55)


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
    assert len(QUESTIONS) == pkg["count"] == 124
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "BATCH_001 package BOT_001_p2: 124 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Numerical answers re-derived by "
                    "tools/batch_001/BOT_001_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
