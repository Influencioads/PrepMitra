"""Builder for BATCH_005, package BOT_005_p2 (Botany, NEET_BOT_001126..NEET_BOT_001250, 125 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Facts already tested in BATCH_000 to BATCH_004 on these topics were avoided (see
`python tools/merge_batch.py stems 005 BOT_005_p2`). Numerical answers are re-derived below; the file is written
only if every assert, the plan quota, the format mix and the answer-key balance pass.

    cd docs/neet-bank && python tools/batch_005/BOT_005_p2.py
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
PACKAGE = "BOT_005_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_005_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_005_BOT_p2.json"
FIRST_ID = 1126

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




# ================================================================ Plant Growth and Development (4 / 5 / 4)
C11_PGD = lambda s: ref(11, PGD, s)

add(PGD, "Growth rate", "Basic", "direct",
    "NCERT gives examples of growth measured in different ways. According to it, cells of a watermelon may increase "
    "in size by up to:",
    P("3,50,000 times", ["3,500 times", "17,500 times", "35 times"], "B"),
    "Measurement of growth by increase in cell size",
    "Growth can be measured as an increase in cell number (a maize root apical meristem gives more than 17,500 new "
    "cells per hour) or as an increase in cell size: cells of a watermelon may increase in size by up to 3,50,000 "
    "times.",
    ["Growth parameter for watermelon cells: increase in cell size", "NCERT figure: up to 3,50,000 times"],
    C11_PGD("growth: plant growth is measurable"),
    why="17,500 is the maize root apical meristem figure (cells per hour), not a size increase; 3,500 and 35 are "
        "invented scalings of the NCERT figure.",
    seconds=25)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "Kinetin, the first cytokinin to be discovered, is chemically:",
    P("N6-furfurylamino purine", ["Indole-3-butyric acid", "2,4-dichlorophenoxyacetic acid",
                                  "Naphthalene acetic acid"], "D"),
    "Chemical nature of kinetin",
    "Skoog and Miller crystallised the cytokinesis-promoting substance and named it kinetin; NCERT describes cytokinins "
    "as adenine derivatives, kinetin being N6-furfurylamino purine. IBA, 2,4-D and NAA are auxins.",
    ["Cytokinins: adenine (purine) derivatives", "Kinetin = N6-furfurylamino purine"],
    C11_PGD("plant growth regulators: physiological effects - cytokinins"),
    why="Indole-3-butyric acid is a natural auxin; 2,4-D and NAA are synthetic auxins.",
    seconds=25)

add(PGD, "Differentiation and redifferentiation", "Basic", "direct",
    "According to NCERT, development of a mature plant from a zygote is the sum of which two processes?",
    P("Growth and differentiation", ["Dedifferentiation and redifferentiation", "Cell division and senescence",
                                     "Germination and flowering"], "C"),
    "Meaning of development",
    "NCERT opens the chapter by stating that development is the sum of two processes, growth and differentiation; the "
    "development of a mature plant from a zygote follows a precise and highly ordered succession of events.",
    ["Development = growth + differentiation"],
    C11_PGD("introduction"),
    why="Dedifferentiation and redifferentiation are special events within development; cell division, senescence, "
        "germination and flowering are individual events, not the two component processes.",
    seconds=20)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "Which of the following auxins has been isolated from plants (a natural auxin)?",
    P("Indole-3-butyric acid (IBA)", ["Naphthalene acetic acid (NAA)", "2,4-dichlorophenoxyacetic acid (2,4-D)",
                                      "Gibberellic acid (GA₃)"], "A"),
    "Natural and synthetic auxins",
    "NCERT: IAA and indole butyric acid (IBA) have been isolated from plants, whereas NAA (naphthalene acetic acid) and "
    "2,4-D (2,4-dichlorophenoxyacetic acid) are synthetic auxins. GA₃ is a gibberellin, not an auxin.",
    ["Natural auxins: IAA, IBA", "Synthetic auxins: NAA, 2,4-D"],
    C11_PGD("plant growth regulators: physiological effects - auxins"),
    why="NAA and 2,4-D are synthetic auxins; GA₃ is a gibberellin.",
    seconds=25)

add(PGD, "Plant growth regulators", "Intermediate", "direct",
    "Charles Darwin and his son Francis Darwin observed that coleoptiles of canary grass grew towards a unilateral "
    "source of light. After a series of experiments, they concluded that:",
    P("The tip of the coleoptile was the site of a transmissible influence that caused the bending of the entire "
      "coleoptile",
      ["The base of the coleoptile perceived the light and pushed the tip towards it",
       "A gas released from the coleoptile tip hastened the bending, as ethylene does",
       "Auxin could be isolated from the coleoptile tips and applied to cause bending"], "D"),
    "Discovery of auxin: the Darwins' experiments",
    "The Darwins found that canary grass coleoptiles responded to unilateral illumination by growing towards the light "
    "(phototropism) and concluded that the tip was the site of a transmissible influence that caused the bending of "
    "the entire coleoptile. Auxin itself was later isolated by F.W. Went from tips of oat coleoptiles.",
    ["Observation: bending towards unilateral light", "Conclusion: tip = site of a transmissible influence",
     "Isolation of auxin came later (Went, oat coleoptiles)"],
    C11_PGD("plant growth regulators: the discovery of plant growth regulators"),
    why="The base does not perceive the stimulus in this account; the gas (ethylene) story belongs to Cousins and "
        "ripening; isolating auxin was Went's later work, not the Darwins' conclusion.",
    seconds=40)

add(PGD, "Germination and growth phases", "Intermediate", "direct",
    "In a root, starting at the apex and moving away from it (proximally), the phases of growth are met in the "
    "order:",
    P("Meristematic phase → phase of elongation → phase of maturation",
      ["Phase of elongation → meristematic phase → phase of maturation",
       "Phase of maturation → phase of elongation → meristematic phase",
       "Meristematic phase → phase of maturation → phase of elongation"], "B"),
    "Location of the phases of growth along the axis",
    "The constantly dividing cells at the root apex are in the meristematic phase. The cells just next to it, away "
    "from the tip, are in the phase of elongation. Further away, proximal to the elongation zone, the axis is "
    "undergoing the phase of maturation.",
    ["Apex: meristematic", "Just proximal: elongation", "Further proximal: maturation"],
    C11_PGD("growth: phases of growth"),
    why="Every other order places a phase out of its position relative to the apex; maturation is the farthest from "
        "the tip.",
    seconds=30)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Gibberellins promote bolting in beet, cabbages and many other plants with a rosette habit.",
       "Gibberellins promote internode elongation just prior to flowering."),
    AR("A"),
    "Gibberellins and bolting",
    "Bolting is internode elongation just prior to flowering, and NCERT states that gibberellins promote it in beet, "
    "cabbages and many plants with rosette habit. Because gibberellins cause this internode elongation, R directly "
    "explains A.",
    ["A: true", "R: true", "Bolting = internode elongation before flowering, which GA promotes, so R explains A"],
    C11_PGD("plant growth regulators: physiological effects - gibberellins"),
    seconds=35)

add(PGD, "Plant growth regulators", "Intermediate", "multi_statement",
    ms("Which of the following statements about the action of plant growth regulators (PGRs) are correct?",
       ["The roles of PGRs in a given event can be complementary or antagonistic.",
        "PGRs may act individualistically or synergistically.",
        "Dormancy in seeds and buds, abscission, senescence and apical dominance are events in which more than one "
        "PGR interacts to affect the event.",
        "Extrinsic factors such as light and temperature never act on plant growth through PGRs.",
        "Each physiological event in a plant is controlled by a single PGR acting alone."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["c", "d", "e"]], "C"),
    "Interaction of PGRs",
    "NCERT: PGRs are one kind of intrinsic control; along with genomic control and extrinsic factors they regulate "
    "growth and development. Their roles can be complementary or antagonistic, individualistic or synergistic, and "
    "several events (seed/bud dormancy, abscission, senescence, apical dominance) are influenced by more than one PGR. "
    "Many extrinsic factors such as temperature and light control plant growth and development via PGRs.",
    ["(a), (b), (c): true", "(d): false, light and temperature act via PGRs",
     "(e): false, many events involve more than one PGR"],
    C11_PGD("plant growth regulators: interaction of PGRs"),
    why="Options A, B and D each include (d) or (e), which contradict the NCERT account.",
    seconds=50)

add(PGD, "Growth rate", "Intermediate", "match_list",
    ml(("symbol in W₁ = W₀e^(rt)", "meaning"),
       ["W₁", "W₀", "t", "e"],
       ["Base of natural logarithms", "Time of growth", "Final size (weight, height, number, etc.)",
        "Initial size, at the beginning of the period"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
       {"A": "II", "B": "IV", "C": "III", "D": "I"}], "D"),
    "Exponential growth equation",
    "Geometric (exponential) growth is expressed as W₁ = W₀e^(rt), where W₁ is the final size (weight, height, number "
    "etc.), W₀ the initial size at the beginning of the period, r the growth rate, t the time of growth and e the base "
    "of natural logarithms.",
    ["W₁: final size", "W₀: initial size", "t: time of growth", "e: base of natural logarithms"],
    C11_PGD("growth: growth rates"),
    why="Option A swaps the final and initial sizes; option B swaps time and e; option C confuses W₁ with time.",
    seconds=35)

add(PGD, "Growth rate", "Advanced", "multi_statement",
    ms("Which of the following statements about the measurement and rates of plant growth are correct?",
       ["Growth can be measured by a variety of parameters, such as fresh weight, dry weight, length, area, volume "
        "and cell number.",
        "In geometric growth, the initial growth is slow (lag phase), and thereafter it increases rapidly at an "
        "exponential rate (log or exponential phase).",
        "In arithmetic growth, both daughter cells of every mitotic division retain the ability to divide.",
        "With a limited nutrient supply, exponential growth can continue indefinitely.",
        "Relative growth rate is the growth of the given system per unit time expressed on a common basis, for "
        "example per unit initial parameter."]),
    MS(["a", "b", "e"], [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "B"),
    "Growth parameters, lag and log phases, arithmetic growth and RGR",
    "NCERT lists fresh weight, dry weight, length, area, volume and cell number as growth parameters. In geometric "
    "growth the initial lag phase is slow and is followed by the log phase; with limited nutrients growth slows and a "
    "stationary phase follows, so exponential growth cannot go on indefinitely. In arithmetic growth only one "
    "daughter cell continues to divide while the other differentiates and matures. Relative growth rate is growth per "
    "unit time on a common basis, such as per unit initial parameter.",
    ["(a), (b), (e): true", "(c): false, only one daughter cell keeps dividing",
     "(d): false, limited nutrients lead to a stationary phase"],
    C11_PGD("growth: growth rates"),
    why="Option A includes (c), option C includes (d), and option D includes both (c) and (d).",
    seconds=60)

add(PGD, "Plant growth regulators", "Advanced", "statement_pair",
    sp("The discovery of each of the five major groups of plant growth regulators has been accidental.",
       "E. Kurosawa observed the symptoms of 'bakanae' disease in uninfected rice seedlings only when they were "
       "inoculated with the living fungus Gibberella fujikuroi."),
    SP("C"),
    "Discovery of PGRs; Kurosawa's experiment",
    "NCERT notes that the discovery of each of the five major groups of PGRs was accidental, so Statement I is true. "
    "Kurosawa reported the appearance of bakanae symptoms in uninfected rice seedlings when they were treated with "
    "sterile filtrates of the fungus Gibberella fujikuroi; the active substance was later identified as gibberellic "
    "acid. The living fungus was not needed, so Statement II is false.",
    ["Statement I: true", "Statement II: false, sterile filtrates of the fungus produced the symptoms"],
    C11_PGD("plant growth regulators: the discovery of plant growth regulators"),
    seconds=40)

add(PGD, "Differentiation and redifferentiation", "Advanced", "direct",
    "In a woody dicot stem, which of the following is an example of redifferentiation?",
    P("Cells cut off by the interfascicular cambium that lose the capacity to divide and mature into secondary "
      "phloem cells",
      ["Formation of the interfascicular cambium from fully differentiated medullary ray parenchyma cells",
       "Formation of the cork cambium from fully differentiated parenchyma cells",
       "Maturation of cells derived from the root apical meristem into tracheary elements"], "A"),
    "Differentiation, dedifferentiation and redifferentiation",
    "Cells from the root and shoot apical meristems and the cambium that mature to perform specific functions undergo "
    "differentiation. Fully differentiated cells regaining the capacity to divide (interfascicular cambium, cork "
    "cambium) show dedifferentiation. Cells produced by such dedifferentiated meristems that again lose the capacity "
    "to divide and mature to perform specific functions are redifferentiated, e.g. secondary phloem formed from the "
    "interfascicular cambium.",
    ["Interfascicular and cork cambium formation: dedifferentiation",
     "Tracheary elements from apical meristem derivatives: differentiation",
     "Secondary tissues formed by a dedifferentiated meristem: redifferentiation"],
    C11_PGD("differentiation, dedifferentiation and redifferentiation"),
    why="Options B and C describe dedifferentiation; option D describes differentiation of cells from a primary "
        "(apical) meristem.",
    seconds=45)

add(PGD, "Germination and growth phases", "Advanced", "multi_statement",
    ms("Which of the following statements about the conditions for plant growth are correct?",
       ["Oxygen helps in releasing the metabolic energy essential for growth activities.",
        "Nutrients (macro and micro essential elements) are required for the synthesis of protoplasm and act as a "
        "source of energy.",
        "Environmental signals such as light and gravity also affect certain phases or stages of growth.",
        "Once a seed has germinated, the growth of the plant no longer depends on water.",
        "Light is the only environmental signal that influences plant growth."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["a", "c", "e"], ["b", "d", "e"]], "D"),
    "Conditions for growth",
    "NCERT lists water, oxygen and nutrients as very essential for growth. Cell enlargement needs water and turgidity "
    "throughout life, so growth never becomes independent of water. Oxygen releases metabolic energy for growth; "
    "nutrients are needed for protoplasm synthesis and as a source of energy. Each plant has an optimum temperature "
    "range, and environmental signals such as light and gravity also affect certain phases of growth, so light is not "
    "the only signal.",
    ["(a), (b), (c): true", "(d): false, growth needs water throughout", "(e): false, gravity (and temperature) also act"],
    C11_PGD("growth: conditions for growth"),
    why="Option A includes (d), option B includes (e), and option C includes both.",
    seconds=50)


# ================================================================ Sexual Reproduction in Flowering Plants (6 / 8 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "A typical stamen has two parts, the filament and the anther. The proximal end of the filament is attached to:",
    P("The thalamus or the petal of the flower", ["The stigma of the same flower", "The ovary wall",
                                                  "The connective of the anther only"], "C"),
    "Parts of a stamen",
    "The stamen consists of a long, slender stalk called the filament and a terminal, generally bilobed structure "
    "called the anther. The proximal end of the filament is attached to the thalamus or the petal of the flower.",
    ["Stamen = filament + anther", "Filament's proximal end: thalamus or petal"],
    C12_SR("flower: stamen, microsporangium and pollen grain"),
    why="The stigma and ovary wall belong to the pistil; the connective joins the anther lobes at the distal end of "
        "the filament, not its proximal end.",
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "The egg apparatus of a typical angiosperm embryo sac consists of:",
    P("Two synergids and one egg cell", ["Three antipodal cells", "One egg cell and two polar nuclei",
                                         "Two synergids and two polar nuclei"], "B"),
    "Organisation of the embryo sac",
    "Six of the eight nuclei of the embryo sac are surrounded by cell walls. Three cells at the micropylar end are "
    "grouped together as the egg apparatus, which consists of two synergids and one egg cell. Three cells at the "
    "chalazal end are the antipodals, and the two polar nuclei lie in the large central cell.",
    ["Micropylar end: 2 synergids + 1 egg = egg apparatus", "Chalazal end: 3 antipodals",
     "Centre: central cell with 2 polar nuclei"],
    C12_SR("pistil, megasporangium (ovule) and embryo sac: female gametophyte"),
    why="Antipodals are at the chalazal end; the polar nuclei lie in the central cell, not in the egg apparatus.",
    seconds=25)

add(SRFP, "Pollination", "Basic", "direct",
    "Which of the following aquatic plants is pollinated by water?",
    P("Hydrilla", ["Water hyacinth", "Water lily", "Maize"], "D"),
    "Water pollination",
    "Pollination by water is quite rare and is limited to about 30 genera, mostly monocots; examples given by NCERT "
    "are Vallisneria, Hydrilla and the marine sea-grass Zostera. In most aquatic plants such as water hyacinth and "
    "water lily the flowers emerge above the water and are pollinated by insects or wind, as in most land plants. "
    "Maize is wind-pollinated.",
    ["Water-pollinated: Vallisneria, Hydrilla, Zostera", "Water hyacinth, water lily: insects or wind",
     "Maize: wind"],
    C12_SR("pre-fertilisation: pollination - agents of pollination"),
    why="Water hyacinth and water lily are aquatic but their flowers are pollinated above the water by insects or "
        "wind; maize is a classic wind-pollinated plant.",
    seconds=25)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "As the anther matures, the microsporangia develop further and extend longitudinally all through the length of "
    "the anther, packed with pollen grains. These mature microsporangia are called:",
    P("Pollen sacs", ["Microspore tetrads", "Sporogenous tissue", "Germ pores"], "A"),
    "Microsporangia become pollen sacs",
    "NCERT: the microsporangia develop further and become pollen sacs. They extend longitudinally all through the "
    "length of an anther and are packed with pollen grains.",
    ["Mature microsporangium = pollen sac"],
    C12_SR("flower: stamen, microsporangium and pollen grain - the microsporangium"),
    why="Microspore tetrads are the four-celled products of meiosis; sporogenous tissue occupies the centre of a young "
        "microsporangium; germ pores are apertures in the pollen exine.",
    seconds=20)

add(SRFP, "Double fertilisation", "Basic", "direct",
    "Syngamy and triple fusion together make up double fertilisation. According to NCERT, double fertilisation is an "
    "event unique to:",
    P("Flowering plants", ["Gymnosperms", "Bryophytes", "Pteridophytes"], "C"),
    "Double fertilisation",
    "Since two types of fusion, syngamy and triple fusion, take place in an embryo sac, the phenomenon is termed "
    "double fertilisation, an event unique to flowering plants.",
    ["Syngamy: male gamete + egg → zygote", "Triple fusion: male gamete + two polar nuclei → PEN",
     "Double fertilisation: unique to angiosperms"],
    C12_SR("double fertilisation"),
    why="Gymnosperms, bryophytes and pteridophytes do not have triple fusion and so lack double fertilisation.",
    seconds=20)

add(SRFP, "Endosperm and embryo", "Basic", "direct",
    "The early stages of embryo development, which are similar in both monocotyledons and dicotyledons, are referred "
    "to as:",
    P("Embryogeny", ["Megasporogenesis", "Microsporogenesis", "Apomixis"], "B"),
    "Embryogeny",
    "The embryo develops at the micropylar end of the embryo sac where the zygote is situated. Though seeds differ "
    "greatly, the early stages of embryo development (embryogeny) are similar in both monocotyledons and "
    "dicotyledons.",
    ["Early stages of embryo development = embryogeny"],
    C12_SR("post-fertilisation: structures and events - embryo"),
    why="Megasporogenesis and microsporogenesis form megaspores and microspores by meiosis; apomixis is seed formation "
        "without fertilisation.",
    seconds=20)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "In a tender coconut, the coconut water is free-nuclear endosperm. The white kernel that surrounds it is:",
    P("Cellular endosperm", ["Perisperm, a persistent part of the nucellus", "The cotyledon of the embryo",
                             "The pericarp formed from the ovary wall"], "D"),
    "Free-nuclear and cellular endosperm in coconut",
    "NCERT: the coconut water from tender coconut is free-nuclear endosperm (made up of thousands of nuclei), and the "
    "surrounding white kernel is the cellular endosperm.",
    ["Coconut water: free-nuclear endosperm", "White kernel: cellular endosperm"],
    C12_SR("post-fertilisation: structures and events - endosperm"),
    why="Perisperm is residual nucellus (black pepper, beet); the cotyledon is part of the embryo; the pericarp is the "
        "fruit wall.",
    seconds=30)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "statement_pair",
    sp("In some species, the anther and stigma are placed at different positions, so that pollen cannot come in "
       "contact with the stigma of the same flower.",
       "Self-incompatibility is a genetic mechanism that prevents self-pollen from fertilising the ovules."),
    SP("A"),
    "Outbreeding devices",
    "NCERT lists several devices that discourage self-pollination: non-synchrony of pollen release and stigma "
    "receptivity, placement of anther and stigma at different positions, self-incompatibility and unisexual flowers. "
    "Self-incompatibility is described as a genetic mechanism that prevents self-pollen (from the same flower or other "
    "flowers of the same plant) from fertilising the ovules. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_SR("pre-fertilisation: pollination - outbreeding devices"),
    seconds=30)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "multi_statement",
    ms("Which of the following statements about the pistil and the ovule are correct?",
       ["The stigma serves as a landing platform for pollen grains.",
        "Inside the ovary is the ovarian cavity (locule).",
        "Each ovule has one or two protective envelopes called integuments.",
        "The placenta is located on the outer surface of the ovary wall.",
        "The embryo sac encloses the nucellus."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Structure of the pistil and ovule",
    "The stigma is the landing platform for pollen; the style lies beneath it, and the basal bulged ovary encloses the "
    "ovarian cavity (locule). The placenta lies inside the ovarian cavity, and the ovules (megasporangia) arise from "
    "it. Each ovule has one or two integuments, which enclose the nucellus; the embryo sac (female gametophyte) lies "
    "within the nucellus.",
    ["(a), (b), (c): true", "(d): false, the placenta is inside the ovarian cavity",
     "(e): false, the nucellus encloses the embryo sac"],
    C12_SR("pistil, megasporangium (ovule) and embryo sac"),
    why="Options A, C and D each include (d) or (e).",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "match_list",
    ml(("cell(s) of the embryo sac", "feature"),
       ["Synergids", "Antipodals", "Central cell", "Egg cell"],
       ["Contains two polar nuclei", "Fuses with a male gamete to form the zygote",
        "Have special cellular thickenings, the filiform apparatus, at the micropylar tip",
        "Three cells grouped together at the chalazal end"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
    "Cells of the mature embryo sac",
    "The synergids have special cellular thickenings at the micropylar tip, the filiform apparatus, which guides the "
    "pollen tube into the synergid. Three antipodal cells lie at the chalazal end. The large central cell holds the two "
    "polar nuclei (which take part in triple fusion), and the egg cell fuses with a male gamete in syngamy to form the "
    "zygote.",
    ["Synergids: filiform apparatus", "Antipodals: 3 cells at the chalazal end", "Central cell: 2 polar nuclei",
     "Egg: syngamy → zygote"],
    C12_SR("pistil, megasporangium (ovule) and embryo sac; double fertilisation"),
    why="Option A swaps synergids and antipodals; option B swaps the central cell and the egg; option D gives the "
        "polar nuclei to the synergids.",
    seconds=40)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "statement_pair",
    sp("The exine of pollen grains exhibits a fascinating array of patterns and designs.",
       "Pollen grains of different species are alike in their shape, size, colour and design."),
    SP("C"),
    "Pollen grain wall and diversity of pollen",
    "NCERT describes the exine as exhibiting a fascinating array of patterns and designs, so Statement I is true. It "
    "also asks students to compare pollen grains of different species, which differ in shape, size, colour and design "
    "(scanning electron micrographs of a few pollen grains are shown). Statement II is false.",
    ["Statement I: true", "Statement II: false, pollen grains of different species differ"],
    C12_SR("flower: stamen, microsporangium and pollen grain - the pollen grain"),
    seconds=30)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "NCERT suggests studying pollen germination by dusting pollen from flowers such as pea, chickpea, Crotalaria, "
    "balsam and Vinca on a glass slide containing a drop of:",
    P("Sugar solution (about 10 per cent)", ["Saturated common salt solution", "Absolute alcohol",
                                             "Liquid nitrogen"], "A"),
    "Observing pollen germination",
    "Pollen grains germinate on a suitable medium. NCERT's suggested activity is to dust pollen on a glass slide with a "
    "drop of sugar solution (about 10 per cent) and observe after about 15-30 minutes under the low-power lens of a "
    "microscope; pollen tubes are seen coming out of the pollen grains.",
    ["Medium: about 10 per cent sugar solution", "Pollen tubes appear after about 15-30 minutes"],
    C12_SR("pre-fertilisation: pollination - pollen-pistil interaction"),
    why="A strong salt solution or alcohol would dehydrate or kill the pollen; liquid nitrogen (−196 °C) is used to "
        "store pollen, not to germinate it.",
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "direct",
    "A mature seed that is not dormant will germinate if favourable conditions are available. According to NCERT, "
    "these conditions are:",
    P("Adequate moisture, oxygen and suitable temperature",
      ["Light, carbon dioxide and nitrogen", "Darkness, carbon dioxide and a low temperature",
       "Adequate moisture in the complete absence of oxygen"], "D"),
    "Conditions for seed germination",
    "As a seed matures, its water content falls and the embryo may become dormant. If favourable conditions are "
    "available (adequate moisture, oxygen and suitable temperature), the seed germinates.",
    ["Favourable conditions: moisture + oxygen + suitable temperature"],
    C12_SR("post-fertilisation: structures and events - seed"),
    why="Light, CO₂ and nitrogen are not the conditions NCERT lists; germination needs oxygen, so its absence (option "
        "C) prevents it.",
    seconds=25)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "In an artificial hybridisation programme, the female parent bears unisexual flowers. According to NCERT, the "
    "correct procedure for the female parent is:",
    P("The female flower buds are bagged before the flowers open, without any emasculation",
      ["The female flowers are emasculated and then bagged after they open",
       "The female flowers are left unbagged, because they have no anthers",
       "The female flowers are dusted with pollen while still in bud and then left open"], "B"),
    "Artificial hybridisation with unisexual female flowers",
    "Emasculation (removal of anthers) is needed only when the female parent has bisexual flowers. If the female "
    "parent bears unisexual flowers there is no need for emasculation; the female flower buds are bagged before the "
    "flowers open. When the stigma becomes receptive, pollination is done with the desired pollen and the flower is "
    "rebagged.",
    ["Unisexual female flower: no emasculation", "Bag the female buds before opening",
     "Pollinate when receptive, then rebag"],
    C12_SR("pre-fertilisation: pollination - artificial hybridisation"),
    why="Unisexual female flowers have no anthers to remove; leaving them unbagged risks contamination with unwanted "
        "pollen; pollination is done when the stigma is receptive, and the flower is rebagged.",
    seconds=35)

# Genotypes in a seed: female parent Aa, pollen parent aa (monosporic embryo sac, all nuclei from one megaspore).
_sr_embryos = sorted({"".join(sorted(m + "a")) for m in "Aa"})
_sr_endosperms = sorted({"".join(sorted(m + m + "a")) for m in "Aa"})
assert _sr_embryos == ["Aa", "aa"] and _sr_endosperms == ["AAa", "aaa"]

add(SRFP, "Double fertilisation", "Advanced", "direct",
    "A plant of genotype Aa (female parent) is pollinated with pollen from a plant of genotype aa. Assuming normal "
    "megasporogenesis (monosporic development) and double fertilisation, which of the following correctly gives the "
    "possible genotypes of the seed coat, the embryo and the endosperm of the seeds formed?",
    P("Seed coat Aa; embryo Aa or aa; endosperm AAa or aaa",
      ["Seed coat Aa; embryo Aa or aa; endosperm Aaa only",
       "Seed coat aa; embryo Aa or aa; endosperm Aaa or aaa",
       "Seed coat Aa; embryo AA or Aa; endosperm AAA or AAa"], "D"),
    "Genetics of double fertilisation",
    "The seed coat develops from the integuments, which are maternal tissue (Aa). All nuclei of an embryo sac arise by "
    "mitosis from a single functional megaspore, which carries either A or a. So the egg and both polar nuclei carry "
    "the same allele. Male gametes carry a. Embryo = egg + male gamete: Aa or aa. Endosperm = two polar nuclei + male "
    "gamete: AA + a = AAa, or aa + a = aaa.",
    ["Seed coat: maternal tissue = Aa", "Egg and polar nuclei from one megaspore: both A or both a",
     "Embryo: Aa or aa", "Endosperm: AAa or aaa"],
    C12_SR("pistil and embryo sac; double fertilisation; seed"),
    why="'Aaa only' wrongly assumes the two polar nuclei carry different alleles; option C gives the seed coat the "
        "pollen parent's genotype; option D forgets that the male gamete always carries a.",
    seconds=90, verified_by=RECOMPUTED)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "assertion_reason",
    ar("In a typical angiosperm embryo sac, the egg cell and the two polar nuclei are genetically identical.",
       "All the nuclei of the embryo sac are formed by mitotic divisions of the nucleus of a single functional "
       "megaspore."),
    AR("A"),
    "Monosporic development of the embryo sac",
    "In most flowering plants only one of the four megaspores is functional. Its nucleus divides mitotically, and two "
    "more sequential mitotic nuclear divisions give the 8-nucleate embryo sac. Mitosis produces genetically identical "
    "nuclei, so the egg and the polar nuclei (indeed all eight nuclei) carry the same genes. R is the direct cause of "
    "A.",
    ["A: true", "R: true (monosporic, mitotic free-nuclear divisions)", "Mitosis from one nucleus → identical nuclei, so "
     "R explains A"],
    C12_SR("pistil, megasporangium (ovule) and embryo sac: megasporogenesis and female gametophyte"),
    seconds=40)

# 30 ovules, one MMC each, meiosis gives 4 megaspores, 3 degenerate; each embryo sac has 8 nuclei.
_sr_ovules = 30
_sr_degenerate = _sr_ovules * (4 - 1)
_sr_nuclei = _sr_ovules * 8
assert (_sr_degenerate, _sr_nuclei) == (90, 240)
assert (_sr_ovules * 4, _sr_ovules * 7) == (120, 210)   # distractors: all megaspores; cells instead of nuclei

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "numerical",
    "An ovary has 30 ovules. Each ovule has a single megaspore mother cell, megasporogenesis is normal and monosporic, "
    "and every ovule forms a typical mature embryo sac. How many megaspores degenerate in all, and how many nuclei are "
    "present in all the mature embryo sacs together?",
    P("90 megaspores degenerate; 240 nuclei", ["120 megaspores degenerate; 240 nuclei",
                                                "90 megaspores degenerate; 210 nuclei",
                                                "30 megaspores degenerate; 240 nuclei"], "B"),
    "Megasporogenesis and the 8-nucleate embryo sac",
    "Each MMC undergoes meiosis to give four megaspores; in a majority of flowering plants one is functional and the "
    "other three degenerate. The functional megaspore forms an 8-nucleate, 7-celled embryo sac.",
    ["Degenerating megaspores = 30 × 3 = 90", "Nuclei = 30 × 8 = 240"],
    C12_SR("pistil, megasporangium (ovule) and embryo sac: megasporogenesis and female gametophyte"),
    why="120 counts all four megaspores as degenerating; 210 counts the 7 cells instead of the 8 nuclei; 30 assumes "
        "one degenerating megaspore per ovule.",
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Pollination", "Advanced", "multi_statement",
    ms("Which of the following statements about pollinating agents are correct?",
       ["Bees, butterflies, flies, beetles, wasps, ants, moths, birds (sunbirds and humming birds) and bats are the "
        "common pollinating agents.",
        "Often, the flowers of an animal-pollinated species are specifically adapted for a particular species of "
        "animal.",
        "Pollination by wind is more common than pollination by water among abiotic pollinations.",
        "The majority of flowering plants use abiotic agents for pollination.",
        "Flowers pollinated by water are generally brightly coloured and rich in nectar."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
    "Agents of pollination",
    "NCERT: the majority of plants use biotic agents and only a small number use abiotic agents (wind, water); among "
    "abiotic pollinations, wind is more common. The listed animals are the common pollinating agents, and flowers of "
    "animal-pollinated species are often specifically adapted to a particular animal. Flowers pollinated by wind or "
    "water are not very colourful and do not produce nectar.",
    ["(a), (b), (c): true", "(d): false, most plants use biotic agents",
     "(e): false, water-pollinated flowers are not colourful and lack nectar"],
    C12_SR("pre-fertilisation: pollination - agents of pollination"),
    why="Options A, B and D each include (d) or (e).",
    seconds=55)

add(SRFP, "Pollination", "Advanced", "assertion_reason",
    ar("Wind- and water-pollinated flowers produce an enormous amount of pollen compared with the number of ovules "
       "available for pollination.",
       "In both wind and water pollination, the pollen grains coming in contact with the stigma is a chance factor."),
    AR("A"),
    "Why abiotic pollination needs much pollen",
    "NCERT: pollen grains coming in contact with the stigma is a chance factor in both wind and water pollination. To "
    "compensate for this uncertainty and the associated loss of pollen grains, the flowers produce an enormous amount "
    "of pollen compared with the number of ovules. R is the direct reason for A.",
    ["A: true", "R: true", "Chance contact → pollen loss → enormous pollen production; R explains A"],
    C12_SR("pre-fertilisation: pollination - agents of pollination"),
    seconds=35)

add(SRFP, "Double fertilisation", "Advanced", "direct",
    "During double fertilisation, which cells of the embryo sac have their nucleus (or nuclei) fuse with a male gamete?",
    P("The egg cell and the central cell",
      ["The egg cell and one synergid", "The two synergids", "The central cell and the antipodal cells"], "B"),
    "Fusions in double fertilisation",
    "The pollen tube releases the two male gametes into the cytoplasm of a synergid, but neither fuses with the synergid "
    "nucleus. One male gamete fuses with the egg nucleus (syngamy) to form the zygote; the other fuses with the two "
    "polar nuclei in the central cell (triple fusion) to form the primary endosperm nucleus. The synergids and "
    "antipodals degenerate after fertilisation.",
    ["Syngamy: egg cell", "Triple fusion: central cell (two polar nuclei)",
     "Synergid only receives the gametes; antipodals degenerate"],
    C12_SR("double fertilisation"),
    why="The synergid receives the pollen tube contents but no fusion occurs with its nucleus; the antipodals take no "
        "part in fertilisation.",
    seconds=40)


# ================================================================ Principles of Inheritance and Variation (7 / 10 / 7)
from itertools import combinations_with_replacement  # noqa: E402
C12_PI = lambda s: ref(12, PIV, s)


def gametes(genotype):
    """Gametes of a diploid genotype written as allele pairs, e.g. 'AaBb' -> ['AB', 'Ab', 'aB', 'ab']."""
    pairs = [genotype[i:i + 2] for i in range(0, len(genotype), 2)]
    return ["".join(p) for p in product(*pairs)]


def cross(p1, p2):
    """All equally likely zygotes of p1 x p2, each as a list of per-gene sorted allele pairs."""
    kids = []
    for g1 in gametes(p1):
        for g2 in gametes(p2):
            kids.append(["".join(sorted(a + b)) for a, b in zip(g1, g2)])
    return kids


def frac_dominant_all(p1, p2):
    kids = cross(p1, p2)
    return F(sum(all(any(ch.isupper() for ch in g) for g in k) for k in kids), len(kids))


add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Inheritance", "Variation", "Alleles", "Heterozygous"],
       ["Slightly different forms of the same gene, coding for a pair of contrasting traits",
        "Having two different alleles of a gene, as in Tt",
        "Process by which characters are passed on from parent to progeny; the basis of heredity",
        "Degree by which progeny differ from their parents"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "D"),
    "Basic terms of genetics",
    "NCERT: inheritance is the process by which characters are passed on from parent to progeny and is the basis of "
    "heredity; variation is the degree by which progeny differ from their parents. Alleles are slightly different "
    "forms of the same gene that code for a pair of contrasting traits. TT and tt are homozygous, while Tt, which "
    "carries two different alleles, is heterozygous.",
    ["Inheritance: parent → progeny", "Variation: progeny differ from parents", "Alleles: forms of one gene",
     "Heterozygous: two different alleles (Tt)"],
    C12_PI("introduction; inheritance of one gene"),
    why="Option A swaps inheritance and variation; option B swaps alleles and heterozygous; option C swaps "
        "inheritance and alleles.",
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Humans knew as early as 8000-1000 B.C. that one of the causes of variation was hidden in sexual reproduction, "
    "and they exploited the variations present in wild populations through artificial selection and domestication. "
    "The example NCERT gives of the result of such selection is:",
    P("Sahiwal cows in Punjab", ["Murrah buffaloes in Haryana", "Hisardale sheep in Punjab",
                                 "Jersey cattle in Gujarat"], "C"),
    "Early human use of variation",
    "NCERT: humans exploited variations in wild populations through artificial selection and domestication to create "
    "plants and animals with desired characters; for example, artificial selection and domestication from ancestral "
    "wild cows gave well-known Indian breeds such as Sahiwal cows in Punjab.",
    ["Artificial selection and domestication of wild cows → Sahiwal cows of Punjab"],
    C12_PI("introduction"),
    why="The other breeds are not the example NCERT uses in this chapter.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Mendel proposed that something was being stably passed down, unchanged, from parent to offspring through the "
    "gametes over successive generations. He called these things:",
    P("Factors", ["Genes", "Chromosomes", "Alleles"], "B"),
    "Mendel's factors",
    "Mendel called the units being passed on 'factors'. Today we call them genes; genes are the units of inheritance "
    "that contain the information required to express a particular trait.",
    ["Mendel's term: factors", "Modern term: genes"],
    C12_PI("inheritance of one gene"),
    why="'Genes' is the modern name, not Mendel's term; chromosomes and alleles were not part of Mendel's vocabulary.",
    seconds=20)

_pi_dwarf = {k: F(sum(g == ["tt"] for g in cross(*v)), len(cross(*v)))
             for k, v in {"A": ("Tt", "tt"), "B": ("Tt", "Tt"), "C": ("TT", "tt"), "D": ("tt", "tt")}.items()}
assert _pi_dwarf == {"A": F(1, 2), "B": F(1, 4), "C": F(0), "D": F(1)}

add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("cross between pea plants (T, tall, dominant over t, dwarf)", "fraction of progeny that are dwarf"),
       ["Tt × tt", "Tt × Tt", "TT × tt", "tt × tt"],
       ["0", "1/4", "1", "1/2"]),
    M({"A": "IV", "B": "II", "C": "I", "D": "III"},
      [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
       {"A": "IV", "B": "I", "C": "II", "D": "III"}], "A"),
    "Monohybrid crosses and segregation",
    "Each parent passes one allele to each gamete. Tt × tt: gametes T, t × t → Tt : tt = 1 : 1, so 1/2 dwarf. "
    "Tt × Tt → TT : Tt : tt = 1 : 2 : 1, so 1/4 dwarf. TT × tt → all Tt (tall), so 0 dwarf. tt × tt → all tt, so all "
    "(1) dwarf.",
    ["Tt × tt → 1/2 tt", "Tt × Tt → 1/4 tt", "TT × tt → no tt", "tt × tt → all tt"],
    C12_PI("inheritance of one gene"),
    why="Option B swaps the test cross and the F1 self-cross; option C swaps TT × tt and tt × tt; option D swaps "
        "Tt × Tt and TT × tt.",
    seconds=35, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "A mutation arising due to a change in a single base pair of DNA is called a point mutation. A classical example of "
    "such a mutation is:",
    P("Sickle-cell anaemia", ["Down's syndrome", "Turner's syndrome", "Klinefelter's syndrome"], "C"),
    "Point mutation",
    "NCERT: mutation arising due to change in a single base pair of DNA is known as point mutation; a classical example "
    "is sickle-cell anaemia (GAG → GUG in the β-globin gene). Down's, Turner's and Klinefelter's syndromes involve "
    "the gain or loss of a whole chromosome (aneuploidy).",
    ["Single base-pair change = point mutation", "Example: sickle-cell anaemia"],
    C12_PI("mutation; genetic disorders"),
    why="The three syndromes are chromosomal disorders caused by aneuploidy, not by a single base change.",
    seconds=20)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "In phenylketonuria, the affected individual lacks an enzyme that converts the amino acid phenylalanine into:",
    P("Tyrosine", ["Phenylpyruvic acid", "Tryptophan", "Glutamic acid"], "D"),
    "Phenylketonuria",
    "Phenylketonuria is an inborn error of metabolism inherited as an autosomal recessive trait. The affected "
    "individual lacks the enzyme that converts phenylalanine into tyrosine. As a result phenylalanine accumulates and "
    "is converted into phenylpyruvic acid and other derivatives, which accumulate in the brain and are excreted in "
    "urine.",
    ["Missing step: phenylalanine → tyrosine", "Phenylalanine instead → phenylpyruvic acid (accumulates)"],
    C12_PI("genetic disorders: Mendelian disorders - phenylketonuria"),
    why="Phenylpyruvic acid is what phenylalanine is converted into because the normal conversion to tyrosine is "
        "blocked; tryptophan and glutamic acid are unrelated.",
    seconds=25)

add(PIV, "Linkage and crossing over", "Basic", "statement_pair",
    sp("In Drosophila there is a clear differentiation of the sexes: the male and female flies are easily "
       "distinguishable.",
       "The hereditary variations of Drosophila can be seen only with an electron microscope."),
    SP("C"),
    "Why Morgan chose Drosophila",
    "NCERT lists the features that made Drosophila suitable for Morgan's genetic studies: it can be grown on a simple "
    "synthetic medium, completes its life cycle in about two weeks, a single mating gives a large number of progeny, "
    "there is a clear differentiation of the sexes (male and female flies are easily distinguishable) (Statement I "
    "true), and it has many types of hereditary variations that can be seen with low power microscopes, so "
    "Statement II is false.",
    ["Statement I: true", "Statement II: false, the variations are visible with low power microscopes"],
    C12_PI("chromosomal theory of inheritance"),
    seconds=25)

# Linkage: AB/ab x ab/ab with 20 per cent recombination, 1000 progeny.
_pi_n, _pi_rf = 1000, F(20, 100)
_pi_ab_recomb = _pi_n * _pi_rf / 2
assert _pi_ab_recomb == 100 and _pi_n * _pi_rf == 200 and _pi_n * (1 - _pi_rf) / 2 == 400 and _pi_n / 4 == 250

add(PIV, "Linkage and crossing over", "Intermediate", "numerical",
    "Genes A and B lie on the same chromosome, and the frequency of recombination between them is 20 per cent. A "
    "dihybrid that received AB from one parent and ab from the other is test-crossed with an aabb plant, and 1000 "
    "progeny are obtained. How many progeny of genotype Aabb are expected?",
    P("100", ["200", "400", "250"], "B"),
    "Recombination frequency and test-cross progeny",
    "The dihybrid forms parental gametes AB and ab and recombinant gametes Ab and aB. With 20 per cent recombination, "
    "recombinant gametes make up 20 per cent of the total, shared equally between Ab and aB (10 per cent each). In a "
    "test cross each gamete type appears directly as a progeny class, so Aabb = 10 per cent of 1000.",
    ["Recombinants = 20% of 1000 = 200", "Ab (Aabb) = half of recombinants = 100",
     "Parentals AaBb and aabb = 400 each"],
    C12_PI("inheritance of two genes: linkage and recombination"),
    shortcut="Each recombinant class = recombination frequency / 2.",
    why="200 is the total of both recombinant classes; 400 is each parental class; 250 assumes independent "
        "assortment (1 : 1 : 1 : 1).",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "assertion_reason",
    ar("A single pleiotropic gene can affect several different phenotypic traits.",
       "In most cases, the gene exerts its effect on metabolic pathways that contribute towards different "
       "phenotypes."),
    AR("A"),
    "Mechanism of pleiotropy",
    "A pleiotropic gene is a single gene that can exhibit multiple phenotypic expressions. NCERT: the underlying "
    "mechanism of pleiotropy in most cases is the effect of a gene on metabolic pathways which contribute towards "
    "different phenotypes. R gives the cause of A.",
    ["A: true", "R: true", "One gene → metabolic pathway → several phenotypes; R explains A"],
    C12_PI("inheritance of one gene: pleiotropy"),
    seconds=35)

# Single autosomal gene, both parents affected, an unaffected child.
_pi_ok = []
for mode in ("dominant", "recessive"):
    for p1, p2 in product(["DD", "Dd", "dd"], repeat=2):
        aff = (lambda g: "D" in g) if mode == "dominant" else (lambda g: g == "dd")
        if aff(p1) and aff(p2) and any(not aff("".join(sorted(a + b))) for a in p1 for b in p2):
            _pi_ok.append((mode, p1, p2))
assert _pi_ok == [("dominant", "Dd", "Dd")]

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "direct",
    "In a family, both parents are affected by a trait controlled by a single autosomal gene, but one of their "
    "children is unaffected. The trait must be:",
    P("Dominant, with both parents heterozygous",
      ["Recessive, with both parents heterozygous", "Recessive, with one parent homozygous",
       "Dominant, with both parents homozygous"], "C"),
    "Dominant and recessive inheritance of a single autosomal gene",
    "If the trait were recessive, affected parents would both be homozygous recessive and every child would be "
    "affected. An unaffected child of two affected parents is possible only if the trait is dominant and each parent "
    "carries one recessive (normal) allele, i.e. both are heterozygous; then 1/4 of the children are expected to be "
    "unaffected.",
    ["Recessive: affected × affected → all affected", "Dominant: Dd × Dd → 1/4 dd (unaffected)"],
    C12_PI("inheritance of one gene: law of dominance and law of segregation"),
    why="Affected individuals cannot be heterozygous for a recessive trait; two homozygous dominant parents cannot "
        "produce an unaffected (recessive homozygous) child.",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "multi_statement",
    ms("Which of the following statements about mutation are correct?",
       ["Besides recombination, mutation is another phenomenon that leads to variation in DNA.",
        "Many chemical and physical factors that induce mutations are referred to as mutagens.",
        "Mutation results in alteration of DNA sequences and consequently in changes in the genotype and the "
        "phenotype of an organism.",
        "Mutations occur only in genes located on the sex chromosomes.",
        "A change in the number of chromosomes cannot cause any disorder."]),
    MS(["a", "b", "c"], [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "e"]], "D"),
    "Mutation as a source of variation",
    "NCERT: mutation is a phenomenon that results in alteration of DNA sequences and consequently changes in the "
    "genotype and phenotype; besides recombination, it is another phenomenon that leads to variation in DNA. Many "
    "chemical and physical factors (e.g. UV radiation) induce mutations and are called mutagens. Mutations occur in "
    "autosomal as well as sex-linked genes, and changes in chromosome number cause disorders such as Down's syndrome.",
    ["(a), (b), (c): true", "(d): false, autosomal genes also mutate (e.g. sickle-cell anaemia)",
     "(e): false, aneuploidy causes Down's, Turner's and Klinefelter's syndromes"],
    C12_PI("mutation"),
    why="Options A, B and C each include (d) or (e).",
    seconds=45)

add(PIV, "Linkage and crossing over", "Intermediate", "statement_pair",
    sp("Sutton united the knowledge of chromosomal segregation with Mendelian principles and called it the chromosomal "
       "theory of inheritance.",
       "Thomas Hunt Morgan and his colleagues worked with the tiny fruit fly, Drosophila melanogaster."),
    SP("A"),
    "Chromosomal theory of inheritance",
    "NCERT: Sutton united the knowledge of chromosomal segregation with Mendelian principles and called it the "
    "chromosomal theory of inheritance. Its experimental verification came from Thomas Hunt Morgan and his colleagues, "
    "who worked with the tiny fruit fly Drosophila melanogaster. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_PI("chromosomal theory of inheritance"),
    seconds=30)

add(PIV, "Sex-linked inheritance", "Intermediate", "direct",
    "A woman is red-green colour blind. Which of the following must be true of her parents?",
    P("Her father must be colour blind",
      ["Her mother must be colour blind", "Her father may have normal vision if her mother is a carrier",
       "Both her parents must be colour blind"], "B"),
    "Inheritance of an X-linked recessive trait",
    "Colour blindness is a sex-linked recessive disorder; a colour-blind woman has the recessive allele on both her X "
    "chromosomes. One X came from her father, who has only one X, so he must be colour blind. Her other X came from "
    "her mother, who must carry the allele but may be only a carrier (normal vision).",
    ["Woman: XᶜXᶜ", "Paternal X: Xᶜ → father XᶜY, colour blind", "Maternal X: Xᶜ → mother at least a carrier"],
    C12_PI("genetic disorders: Mendelian disorders - colour blindness"),
    why="The mother need only be a carrier, so neither A nor D must be true; a father with normal vision has a normal "
        "X and could not give his daughter Xᶜ.",
    seconds=40)

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "According to NCERT, the 9 : 3 : 3 : 1 ratio of Mendel's dihybrid F2 can be derived as:",
    P("A combination series of 3 yellow : 1 green with 3 round : 1 wrinkled, i.e. (3 : 1) × (3 : 1)",
      ["The sum of two monohybrid ratios, i.e. (3 : 1) + (3 : 1)",
       "The product of two genotypic ratios, i.e. (1 : 2 : 1) × (1 : 2 : 1)",
       "The product of two test-cross ratios, i.e. (1 : 1) × (1 : 1)"], "D"),
    "Derivation of the dihybrid ratio",
    "Because the two genes segregate independently, the dihybrid phenotypic ratio is the product of the two monohybrid "
    "phenotypic ratios: (3 Round : 1 Wrinkled)(3 Yellow : 1 Green) = 9 round yellow : 3 wrinkled yellow : 3 round "
    "green : 1 wrinkled green.",
    ["(3 R : 1 r)(3 Y : 1 y)", "= 9 RY : 3 rY : 3 Ry : 1 ry"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="Adding ratios has no meaning for combined traits; (1:2:1)² gives the 9 genotypic classes; (1:1)² is the "
        "dihybrid test-cross ratio.",
    seconds=30)

add(PIV, "Sex determination", "Intermediate", "statement_pair",
    sp("Henking gave the name 'X body' to the structure he observed during spermatogenesis, but he could not explain "
       "its significance.",
       "Henking himself identified the X body as a chromosome that determines maleness."),
    SP("C"),
    "Discovery of the X chromosome",
    "Henking (1891) traced a specific nuclear structure through spermatogenesis in a few insects, named it the X body "
    "and could not explain its significance (Statement I true). Further investigations by other scientists led to the "
    "conclusion that the X body was in fact a chromosome, which was named the X chromosome (Statement II false).",
    ["Statement I: true", "Statement II: false, later workers showed it was a chromosome"],
    C12_PI("sex determination"),
    seconds=30)

_pi_tc = Counter(tuple(k) for k in cross("RRYy", "rryy"))
assert set(_pi_tc) == {("Rr", "Yy"), ("Rr", "yy")} and len(set(_pi_tc.values())) == 1
assert len(set(tuple(k) for k in cross("RrYy", "rryy"))) == 4
assert {tuple(k) for k in cross("RrYY", "rryy")} == {("Rr", "Yy"), ("rr", "Yy")}
assert {tuple(k) for k in cross("RRYY", "rryy")} == {("Rr", "Yy")}

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "A pea plant with round yellow seeds is crossed with a plant with wrinkled green seeds (rryy). The progeny have "
    "round yellow and round green seeds in a 1 : 1 ratio. The genotype of the round yellow parent is:",
    P("RRYy", ["RrYy", "RrYY", "RRYY"], "A"),
    "Test cross with two genes",
    "In a test cross, the progeny classes reflect the gametes of the tested parent. All progeny are round, so the "
    "parent gives only R gametes (RR). Yellow and green appear 1 : 1, so it is Yy. Hence RRYy, giving RY and Ry "
    "gametes in equal numbers.",
    ["All round → RR", "Yellow : green = 1 : 1 → Yy", "Genotype RRYy"],
    C12_PI("inheritance of one gene: test cross; inheritance of two genes"),
    why="RrYy would give four classes (1 : 1 : 1 : 1); RrYY would give round yellow and wrinkled yellow; RRYY would "
        "give only round yellow.",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "assertion_reason",
    ar("Individuals with Klinefelter's syndrome are sterile.",
       "Turner's syndrome is caused by the absence of one of the X chromosomes, i.e. the karyotype 45 with X0."),
    AR("B"),
    "Sex-chromosome aneuploidies",
    "Klinefelter's syndrome (47, XXY) gives an overall masculine development with some feminine features "
    "(gynaecomastia), and such individuals are sterile, so A is true. Turner's syndrome is caused by the absence of "
    "one X chromosome (45 with X0), so R is true. R describes a different disorder and does not explain why "
    "Klinefelter individuals are sterile.",
    ["A: true", "R: true", "R concerns Turner's syndrome, not the sterility of Klinefelter males"],
    C12_PI("genetic disorders: chromosomal disorders"),
    seconds=30)

# Number of genotypes with 4 alleles at one locus.
_pi_alleles = ["a1", "a2", "a3", "a4"]
_pi_geno = list(combinations_with_replacement(_pi_alleles, 2))
_pi_het = [g for g in _pi_geno if g[0] != g[1]]
assert (len(_pi_geno), len(_pi_het)) == (10, 6)
assert len(list(combinations_with_replacement(["IA", "IB", "i"], 2))) == 6     # NCERT's ABO case
assert 4 * 4 == 16 and 2 * 4 == 8                                              # distractors

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "numerical",
    "With three alleles (Iᴬ, Iᴮ and i), the ABO gene gives six possible genotypes in the human population. Using the "
    "same reasoning, how many genotypes would be possible in a population for a gene with four alleles, and how many "
    "of these would be heterozygous?",
    P("10 genotypes, of which 6 are heterozygous",
      ["16 genotypes, of which 12 are heterozygous", "10 genotypes, of which 4 are heterozygous",
       "8 genotypes, of which 4 are heterozygous"], "C"),
    "Multiple alleles: counting genotypes",
    "A diploid individual carries only two alleles. With n alleles, the homozygotes number n and the heterozygotes "
    "number n(n − 1)/2, giving n(n + 1)/2 genotypes in all. For ABO, n = 3: 3 + 3 = 6. For n = 4: 4 homozygotes + 6 "
    "heterozygotes = 10.",
    ["Homozygotes = 4", "Heterozygotes = 4 × 3 / 2 = 6", "Total = 10"],
    C12_PI("inheritance of one gene: co-dominance (multiple alleles in ABO blood groups)"),
    shortcut="Genotypes = n(n + 1)/2.",
    why="16 counts ordered pairs (a1a2 and a2a1 separately); '4 heterozygous' confuses the homozygote count; 8 (2n) "
        "has no basis.",
    seconds=60, verified_by=RECOMPUTED)

# Honey bee: queen Aa x drone A. Sons from unfertilised eggs (haploid); daughters from fertilised eggs.
_pi_eggs = ["A", "a"]
_pi_sons = Counter(_pi_eggs)
_pi_daughters = Counter("".join(sorted(e + "A")) for e in _pi_eggs)
assert _pi_sons == Counter({"A": 1, "a": 1}) and _pi_daughters == Counter({"AA": 1, "Aa": 1})

add(PIV, "Sex determination", "Advanced", "direct",
    "In honey bees, a queen of genotype Aa mates with a drone of genotype A. What genotypes are expected among their "
    "sons and their daughters?",
    P("Sons: A or a (1 : 1); daughters: AA or Aa (1 : 1)",
      ["Sons: AA or Aa (1 : 1); daughters: A or a (1 : 1)",
       "Sons: all A, like their father; daughters: AA or Aa (1 : 1)",
       "Sons: Aa only; daughters: AA, Aa and aa (1 : 2 : 1)"], "D"),
    "Haplodiploid sex determination",
    "An offspring formed from the union of a sperm and an egg develops as a female, while an unfertilised egg "
    "develops as a male by parthenogenesis; males are haploid. Sons therefore carry only one maternal allele (A or a, "
    "1 : 1) and have no father. Daughters get one allele from the egg (A or a) and the drone's A from the sperm: AA "
    "or Aa (1 : 1).",
    ["Sons: unfertilised eggs → A or a", "Daughters: egg (A/a) + sperm (A) → AA or Aa"],
    C12_PI("sex determination: sex determination in honey bee"),
    why="Option A reverses the sexes; sons have no father, so they cannot inherit the drone's allele (option B); the "
        "drone is haploid and gives only A, so no aa daughter is possible (option C).",
    seconds=60, verified_by=RECOMPUTED)

# Woman with normal parents and a haemophilic brother marries a normal man.
_pi_p_carrier = F(1, 2)                  # her mother is a carrier (XH Xh); she received Xh with probability 1/2
_pi_son_affected = _pi_p_carrier * F(1, 2)
assert _pi_son_affected == F(1, 4)

add(PIV, "Sex-linked inheritance", "Advanced", "numerical",
    "A woman's parents both have normal blood clotting, but her brother is haemophilic. She marries a normal man. What "
    "is the probability that their first son will be haemophilic?",
    P("1/4", ["1/2", "1/8", "0"], "A"),
    "Conditional probability in X-linked inheritance",
    "The brother received his only X from the mother, and the father is normal, so the mother must be a carrier (XᴴXʰ). "
    "The woman received the mother's Xʰ with probability 1/2. If she is a carrier, each son has a 1/2 chance of being "
    "haemophilic. So P = 1/2 × 1/2 = 1/4.",
    ["Mother of the woman: carrier (XᴴXʰ)", "P(woman is a carrier) = 1/2", "P(son affected | carrier) = 1/2",
     "P = 1/4"],
    C12_PI("genetic disorders: Mendelian disorders - haemophilia"),
    why="1/2 assumes the woman is certainly a carrier; 1/8 multiplies again by the chance of the child being a son, "
        "though the question already concerns a son; 0 ignores that she may be a carrier.",
    seconds=75, verified_by=RECOMPUTED)

# ABO exclusion: mother B, child O (ii). The child needs i from the father.
_pi_abo = {"A": [("IA", "IA"), ("IA", "i")], "B": [("IB", "IB"), ("IB", "i")], "AB": [("IA", "IB")],
           "O": [("i", "i")]}
_pi_can_father = {g: any("i" in gt for gt in gts) for g, gts in _pi_abo.items()}
assert _pi_can_father == {"A": True, "B": True, "AB": False, "O": True}

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "direct",
    "A mother has blood group B and her child has blood group O. Which of the following men can be excluded as the "
    "child's biological father?",
    P("A man with blood group AB", ["A man with blood group A", "A man with blood group B",
                                    "A man with blood group O"], "B"),
    "Using ABO genetics to exclude parentage",
    "A child of blood group O has genotype ii and must receive an i allele from each parent. The mother (B) must be "
    "Iᴮi. A father of group A (Iᴬi), B (Iᴮi) or O (ii) can carry i, but a man of group AB (IᴬIᴮ) has no i allele and "
    "cannot be the father.",
    ["Child O = ii → needs i from father", "AB man = IᴬIᴮ → no i", "A, B and O men can carry i"],
    C12_PI("inheritance of one gene: co-dominance (ABO blood groups)"),
    why="Men of groups A and B can be heterozygous (Iᴬi, Iᴮi) and a group O man is ii; each can pass on i.",
    seconds=45, verified_by=RECOMPUTED)

_pi_crosses = {"A": ("AaBb", "AaBb"), "B": ("AaBb", "aabb"), "C": ("AaBB", "aabb"), "D": ("AABb", "aaBb")}
_pi_vals = {k: frac_dominant_all(*v) for k, v in _pi_crosses.items()}
assert _pi_vals == {"A": F(9, 16), "B": F(1, 4), "C": F(1, 2), "D": F(3, 4)}

add(PIV, "Mendelian inheritance", "Advanced", "match_list",
    ml(("cross (genes assort independently; A and B completely dominant)",
        "fraction of progeny showing both dominant traits"),
       ["AaBb × AaBb", "AaBb × aabb", "AaBB × aabb", "AABb × aaBb"],
       ["3/4", "1/2", "9/16", "1/4"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "I", "B": "IV", "C": "II", "D": "III"},
       {"A": "III", "B": "IV", "C": "I", "D": "II"}], "D"),
    "Product rule for independently assorting genes",
    "Multiply the probabilities for each gene. AaBb × AaBb: 3/4 × 3/4 = 9/16. AaBb × aabb: 1/2 × 1/2 = 1/4. AaBB × "
    "aabb: 1/2 (A_) × 1 (all Bb) = 1/2. AABb × aaBb: 1 (all Aa) × 3/4 (B_) = 3/4.",
    ["A: 9/16", "B: 1/4", "C: 1/2", "D: 3/4"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="Option A swaps the test cross and the AaBB cross; option B swaps the first and last crosses; option C swaps "
        "AaBB × aabb with AABb × aaBb.",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "statement_pair",
    sp("For an autosomal recessive trait, two affected parents can have only affected children.",
       "For an X-linked recessive trait, an affected father passes the recessive allele to all his daughters."),
    SP("A"),
    "Autosomal recessive and sex-linked recessive inheritance",
    "Affected individuals for an autosomal recessive trait are homozygous recessive; two such parents can pass on only "
    "the recessive allele, so every child is affected (Statement I true). A man has a single X chromosome and passes "
    "it to every daughter (sons receive his Y), so all daughters of an affected father receive the recessive allele "
    "(Statement II true).",
    ["Statement I: true (aa × aa → all aa)", "Statement II: true (father's X goes to every daughter)"],
    C12_PI("inheritance of one gene: law of segregation; sex determination; genetic disorders - sex-linked inheritance"),
    seconds=45)

add(PIV, "Incomplete and co-dominance", "Advanced", "multi_statement",
    ms("Which of the following statements about the inheritance of ABO blood groups are correct?",
       ["A child with blood group AB must have received Iᴬ from one parent and Iᴮ from the other.",
        "Two parents who both have blood group O can have only children with blood group O.",
        "The six possible ABO genotypes give four blood-group phenotypes.",
        "Two parents who both have blood group A can never have a child with blood group O.",
        "A man with blood group B and a woman with blood group A cannot have a child with blood group AB."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "B"),
    "Co-dominance and multiple alleles in ABO",
    "Iᴬ and Iᴮ are co-dominant and both are dominant over i. An AB child (IᴬIᴮ) must get one of these alleles from each "
    "parent. O parents (ii × ii) give only ii children. The six genotypes (IᴬIᴬ, Iᴬi, IᴮIᴮ, Iᴮi, IᴬIᴮ, ii) give four "
    "phenotypes (A, B, AB, O). Two group A parents who are both Iᴬi can have an ii (O) child, and a B man and an A "
    "woman can have an AB child.",
    ["(a), (b), (c): true", "(d): false, Iᴬi × Iᴬi gives 1/4 ii", "(e): false, Iᴮ_ × Iᴬ_ can give IᴬIᴮ"],
    C12_PI("inheritance of one gene: co-dominance"),
    why="Options A, C and D each include (d) or (e), which ignore heterozygous parents and co-dominance.",
    seconds=60)


# ================================================================ Molecular Basis of Inheritance (7 / 10 / 7)
C12_MB = lambda s: ref(12, MBI, s)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "Which of the following is a nucleoside?",
    P("Cytidine", ["Cytosine", "Uracil", "Thymine"], "C"),
    "Nitrogenous base, nucleoside and nucleotide",
    "A nitrogenous base linked to a pentose sugar through an N-glycosidic linkage forms a nucleoside, such as adenosine "
    "or deoxyadenosine, guanosine or deoxyguanosine, cytidine or deoxycytidine, and uridine or deoxythymidine. Adding "
    "a phosphate group gives a nucleotide. Cytosine, uracil and thymine are free nitrogenous bases (pyrimidines).",
    ["Base + sugar = nucleoside (e.g. cytidine)", "Nucleoside + phosphate = nucleotide"],
    C12_MB("the DNA: structure of polynucleotide chain"),
    why="Cytosine, uracil and thymine are nitrogenous bases, not nucleosides.",
    seconds=20)

add(MBI, "Genetic code and translation", "Basic", "direct",
    "A tRNA molecule has an anticodon loop with bases complementary to the code. The specific amino acid that a tRNA "
    "carries is attached to its:",
    P("Amino acid acceptor end", ["Anticodon loop", "Untranslated region", "Initiator codon"], "A"),
    "Structure of tRNA (the adapter molecule)",
    "tRNA has an anticodon loop with bases complementary to the code, and an amino acid acceptor end to which it binds "
    "the amino acid. tRNAs are specific for each amino acid.",
    ["Anticodon loop: reads the codon", "Amino acid acceptor end: binds the amino acid"],
    C12_MB("tRNA - the adapter molecule"),
    why="The anticodon loop pairs with the codon; untranslated regions and the initiator codon belong to mRNA.",
    seconds=20)

add(MBI, "Replication", "Basic", "direct",
    "In the Meselson and Stahl experiment, DNA molecules containing ¹⁵N and ¹⁴N were separated from each other on the "
    "basis of their densities by:",
    P("Centrifugation in a caesium chloride (CsCl) density gradient",
      ["Agarose gel electrophoresis", "Autoradiography with radioactive thymidine",
       "Digestion with restriction endonucleases"], "D"),
    "Technique used by Meselson and Stahl",
    "¹⁵N is not radioactive. Heavy (¹⁵N) DNA can be separated from normal (¹⁴N) DNA by centrifugation in a caesium "
    "chloride (CsCl) density gradient, which is how Meselson and Stahl identified heavy, hybrid and light DNA.",
    ["Heavy and light DNA differ in density", "Separated by CsCl density gradient centrifugation"],
    C12_MB("replication: the experimental proof"),
    why="Electrophoresis separates DNA by size, not by isotope density; autoradiography with thymidine was used by "
        "Taylor; restriction enzymes cut DNA and do not separate isotopic forms.",
    seconds=25)

add(MBI, "DNA packaging", "Basic", "direct",
    "Prokaryotes such as E. coli lack a defined nucleus. According to NCERT, their DNA:",
    P("Is held with some positively charged proteins in the nucleoid and organised in large loops held by proteins",
      ["Is wrapped around histone octamers to form nucleosomes",
       "Is enclosed in a nuclear envelope as euchromatin and heterochromatin",
       "Is not associated with any proteins at all"], "B"),
    "Packaging of DNA in prokaryotes",
    "In prokaryotes the DNA is not scattered throughout the cell. Being negatively charged, it is held with some "
    "proteins that have positive charges in a region termed the nucleoid; the DNA in the nucleoid is organised in large "
    "loops held by proteins. Histone octamers and nucleosomes are features of eukaryotic packaging.",
    ["Prokaryotes: nucleoid, positively charged proteins, large loops"],
    C12_MB("packaging of DNA helix"),
    why="Nucleosomes and chromatin types are eukaryotic; prokaryotic DNA is associated with proteins in the nucleoid.",
    seconds=25)

add(MBI, "Transcription", "Basic", "match_list",
    ml(("component of bacterial transcription", "role"),
       ["Initiation factor (σ)", "Termination factor (ρ)", "RNA polymerase on its own", "Promoter"],
       ["Catalyses only the elongation of RNA", "Provides the binding site for RNA polymerase",
        "Helps RNA polymerase to initiate transcription", "Helps RNA polymerase to terminate transcription"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
       {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
    "RNA polymerase and its factors",
    "NCERT: in bacteria the RNA polymerase is only capable of catalysing the process of elongation. It associates "
    "transiently with the initiation factor (σ) and the termination factor (ρ) to initiate and terminate transcription "
    "respectively. The promoter is the DNA sequence that provides the binding site for RNA polymerase.",
    ["σ: initiation", "ρ: termination", "RNA polymerase alone: elongation", "Promoter: binding site"],
    C12_MB("transcription"),
    why="Option A swaps σ and ρ; option B swaps the polymerase and the promoter; option D gives elongation to σ.",
    seconds=30)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "direct",
    "Besides forensic science and paternity testing, NCERT states that DNA fingerprinting has a much wider "
    "application in:",
    P("Determining population and genetic diversities",
      ["Measuring the BOD of waste water", "Estimating the age of fossils",
       "Counting the number of chromosomes in a cell"], "D"),
    "Applications of DNA fingerprinting",
    "DNA fingerprinting is a very quick way to compare DNA sequences of any two individuals. It is used in forensic "
    "science and is the basis of paternity testing in case of disputes; NCERT adds that it has a much wider "
    "application in determining population and genetic diversities.",
    ["Uses: forensics, paternity testing, population and genetic diversity"],
    C12_MB("DNA fingerprinting"),
    why="BOD, fossil dating and chromosome counts are not determined by DNA fingerprinting.",
    seconds=25)

add(MBI, "Lac operon", "Basic", "statement_pair",
    sp("Besides negative regulation by the repressor, the lac operon is also under the control of positive "
       "regulation.",
       "In most operons, the operator region is adjacent to the promoter elements."),
    SP("A"),
    "Regulation of the lac operon",
    "NCERT: regulation of the lac operon by the repressor is referred to as negative regulation; the lac operon is "
    "under the control of positive regulation as well (beyond the scope of the book). The accessibility of promoter "
    "regions in prokaryotes is often regulated by proteins binding to sequences called operators; the operator region "
    "is adjacent to the promoter elements in most operons. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=25)

_mb_bp, _mb_min = 4.6e6, 38
_mb_rate = _mb_bp / (_mb_min * 60)
assert 1950 < _mb_rate < 2050                         # ≈ 2000 bp per second
assert 1.2e5 < _mb_bp / _mb_min < 1.22e5              # distractor: per minute mistaken for per second

add(MBI, "Replication", "Intermediate", "numerical",
    "E. coli has 4.6 × 10⁶ bp of DNA and completes replication of it in about 38 minutes. What is the approximate "
    "average rate of polymerisation?",
    P("About 2000 bp per second", ["About 1,21,000 bp per second", "About 20,000 bp per second",
                                   "About 34 bp per second"], "B"),
    "Rate of DNA replication",
    "Rate = number of base pairs ÷ time. 38 minutes = 2280 seconds; 4.6 × 10⁶ ÷ 2280 ≈ 2017, i.e. approximately 2000 "
    "bp per second, which is the figure NCERT gives. Such a fast rate must also be highly accurate, since errors would "
    "cause mutations.",
    ["Time = 38 × 60 = 2280 s", "Rate = 4.6 × 10⁶ / 2280 ≈ 2.0 × 10³ bp s⁻¹"],
    C12_MB("replication: the machinery and the enzymes"),
    why="About 1,21,000 is the rate per minute (minutes not converted to seconds); 20,000 is a power-of-ten slip; "
        "about 34 has no valid basis (it divides the per-second rate by 60 once more).",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "assertion_reason",
    ar("DNA polymorphism is more likely to be observed in non-coding DNA sequences than in coding sequences.",
       "Mutations in non-coding sequences may not have any immediate effect on an individual's reproductive ability, "
       "so they keep accumulating generation after generation."),
    AR("A"),
    "Basis of DNA polymorphism",
    "An inheritable mutation observed in a population at high frequency is called DNA polymorphism. NCERT: the "
    "probability of such variation being observed in non-coding DNA is higher, because mutations in these sequences "
    "may not have any immediate effect on an individual's reproductive ability; they keep accumulating generation "
    "after generation and form one of the bases of polymorphism. R is the reason for A.",
    ["A: true", "R: true", "No effect on reproduction → mutations accumulate → more polymorphism; R explains A"],
    C12_MB("DNA fingerprinting"),
    seconds=40)

add(MBI, "Transcription", "Intermediate", "statement_pair",
    sp("The terminator of a transcription unit is located towards the 5'-end (upstream) of the coding strand.",
       "The promoter is a DNA sequence that provides the binding site for RNA polymerase."),
    SP("D"),
    "Promoter and terminator",
    "The promoter lies towards the 5'-end (upstream) of the structural gene, with reference to the polarity of the "
    "coding strand, and provides the binding site for RNA polymerase (Statement II true). The terminator lies towards "
    "the 3'-end (downstream) of the coding strand and usually defines the end of transcription (Statement I false).",
    ["Statement I: false, the terminator is at the 3' (downstream) end", "Statement II: true"],
    C12_MB("transcription: transcription unit"),
    seconds=30)

add(MBI, "Genetic code and translation", "Intermediate", "multi_statement",
    ms("Which of the following statements about translation are correct?",
       ["Translation refers to the process of polymerisation of amino acids to form a polypeptide.",
        "The order and sequence of amino acids are defined by the sequence of bases in the mRNA.",
        "The amino acids are joined by a bond known as a peptide bond.",
        "Formation of a peptide bond does not require energy.",
        "During translation, the ribosome moves from codon to codon along the mRNA."]),
    MS(["a", "b", "c", "e"], [["a", "b", "d"], ["b", "c", "d", "e"], ["a", "c", "d"]], "C"),
    "The process of translation",
    "NCERT: translation is the polymerisation of amino acids to form a polypeptide, the order of amino acids being "
    "defined by the base sequence of the mRNA; amino acids are joined by peptide bonds. Formation of a peptide bond "
    "requires energy, which is why amino acids are first activated in the presence of ATP and linked to their cognate "
    "tRNA. The ribosome moves from codon to codon along the mRNA, adding amino acids one by one.",
    ["(a), (b), (c), (e): true", "(d): false, peptide bond formation requires energy (ATP used in charging)"],
    C12_MB("translation"),
    why="Every other option includes the false statement (d).",
    seconds=45)

add(MBI, "Lac operon", "Intermediate", "direct",
    "According to NCERT, lactose is transported into E. coli cells and switches on the lac operon when it is provided "
    "in the growth medium in the absence of a preferred carbon source such as:",
    P("Glucose", ["Galactose", "Sucrose", "Maltose"], "D"),
    "Conditions for induction of the lac operon",
    "In the absence of a preferred carbon source such as glucose, if lactose is provided in the growth medium, it is "
    "transported into the cells through the action of permease and induces the operon (a very low level of lac "
    "operon expression is always present for this).",
    ["Preferred carbon source: glucose", "Lactose (inducer) used when glucose is absent"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Galactose is a product of lactose hydrolysis; sucrose and maltose are not mentioned as the preferred carbon "
        "source.",
    seconds=25)

add(MBI, "DNA as genetic material", "Intermediate", "match_list",
    ml(("scientist(s)", "year of the work, as given in NCERT"),
       ["Frederick Griffith (transformation in Streptococcus pneumoniae)",
        "Watson and Crick (double helix model of DNA)",
        "Hershey and Chase (bacteriophage experiments)",
        "Meselson and Stahl (semiconservative replication)"],
       ["1952", "1958", "1928", "1953"]),
    M({"A": "III", "B": "IV", "C": "I", "D": "II"},
      [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
       {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Chronology of key experiments",
    "NCERT dates: Griffith's transformation experiments, 1928; Hershey and Chase's proof that DNA is the genetic "
    "material, 1952; Watson and Crick's double helix model, 1953; Meselson and Stahl's experiment on semiconservative "
    "replication, 1958.",
    ["Griffith: 1928", "Watson and Crick: 1953", "Hershey and Chase: 1952", "Meselson and Stahl: 1958"],
    C12_MB("the search for genetic material; the DNA; replication"),
    why="Option A swaps 1952 and 1953; option C moves Griffith to 1953; option D swaps 1952 and 1958.",
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "statement_pair",
    sp("The size of a VNTR varies from 0.1 to 20 kb.",
       "After hybridisation with a VNTR probe, the autoradiogram gives many bands of differing sizes."),
    SP("A"),
    "VNTRs in DNA fingerprinting",
    "NCERT: the VNTR (a mini-satellite) varies in size from 0.1 to 20 kb; consequently, after hybridisation with the "
    "VNTR probe, the autoradiogram gives many bands of differing sizes, and these bands give the characteristic "
    "pattern of an individual's DNA. Both statements are true.",
    ["Statement I: true", "Statement II: true"],
    C12_MB("DNA fingerprinting"),
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "direct",
    "According to NCERT, the unequivocal proof that DNA is the genetic material came from the experiments of:",
    P("Alfred Hershey and Martha Chase",
      ["Frederick Griffith", "Oswald Avery, Colin MacLeod and Maclyn McCarty", "Matthew Meselson and Franklin Stahl"],
      "C"),
    "Proof that DNA is the genetic material",
    "Griffith showed transformation; Avery, MacLeod and McCarty showed that DNA from S bacteria caused the "
    "transformation, but not all biologists were convinced. The unequivocal proof came from Hershey and Chase, who "
    "showed with radioactive phosphorus and sulphur that the DNA of bacteriophages, not their protein, enters the "
    "bacteria. Meselson and Stahl worked on replication.",
    ["Hershey and Chase: unequivocal proof (bacteriophage, ³²P and ³⁵S)"],
    C12_MB("the search for genetic material"),
    why="Griffith did not identify the transforming principle; Avery and colleagues' result did not convince all "
        "biologists; Meselson and Stahl studied the mode of replication.",
    seconds=25)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("The development and differentiation of an embryo into an adult organism are a result of the coordinated "
       "regulation of expression of several sets of genes.",
       "In eukaryotes, gene expression is regulated only at the level of translation."),
    AR("C"),
    "Regulation of gene expression",
    "NCERT states A in these words. In eukaryotes, however, regulation can be exerted at the transcriptional level "
    "(formation of the primary transcript), the processing level (regulation of splicing), the transport of mRNA from "
    "the nucleus to the cytoplasm and the translational level, so R is false.",
    ["A: true", "R: false, four levels of regulation exist in eukaryotes"],
    C12_MB("regulation of gene expression"),
    seconds=30)

add(MBI, "Lac operon", "Intermediate", "multi_statement",
    ms("Which of the following statements about operons are correct?",
       ["In the lac operon, a polycistronic structural gene is regulated by a common promoter and regulatory genes.",
        "Such an arrangement, called an operon, is very common in bacteria.",
        "Lactose is the substrate for the enzyme β-galactosidase.",
        "The repressor binds to the operator in the presence of the inducer.",
        "The z, y and a genes are transcribed as three separate monocistronic mRNAs."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "The operon concept",
    "NCERT: in the lac operon a polycistronic structural gene is regulated by a common promoter and regulatory genes; "
    "such an arrangement is very common in bacteria and is called an operon. Lactose is the substrate for "
    "β-galactosidase and acts as the inducer: it binds the repressor and inactivates it, so the repressor cannot bind "
    "the operator. The structural genes are transcribed together as one polycistronic mRNA.",
    ["(a), (b), (c): true", "(d): false, the inducer prevents repressor binding",
     "(e): false, the structural gene is polycistronic"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Options A, C and D each include (d) or (e).",
    seconds=45)

_mb_pair = {"A": "U", "T": "A", "G": "C", "C": "G"}
_mb_template = "GCATTA"                                              # written 5'->3'
_mb_mrna = "".join(_mb_pair[b] for b in reversed(_mb_template))     # antiparallel complement, written 5'->3'
assert _mb_mrna == "UAAUGC"
assert "".join(_mb_pair[b] for b in _mb_template) == "CGUAAU"      # distractor: complement not reversed
assert _mb_template.replace("T", "U") == "GCAUUA"                   # distractor: template copied with U

add(MBI, "Transcription", "Advanced", "direct",
    "The template strand of a short stretch of a structural gene, written in the 5'→3' direction, is 5'-GCATTA-3'. "
    "The mRNA transcribed from it, written in the 5'→3' direction, is:",
    P("5'-UAAUGC-3'", ["5'-CGUAAU-3'", "5'-GCAUUA-3'", "5'-AUUACG-3'"], "D"),
    "Antiparallel complementarity in transcription",
    "RNA polymerase reads the template 3'→5' and builds RNA 5'→3', complementary and antiparallel to the template. "
    "Template 5'-GCATTA-3' read from its 3' end: A, T, T, A, C, G → complementary RNA U, A, A, U, G, C. So the mRNA is "
    "5'-UAAUGC-3' (the same as the coding strand 5'-TAATGC-3', with U for T).",
    ["Reverse the template: 3'-ATTACG-5'", "Complement with U for A: 5'-UAAUGC-3'"],
    C12_MB("transcription"),
    shortcut="mRNA = reverse complement of the template (with U).",
    why="5'-CGUAAU-3' is the complement written without reversing the polarity; 5'-GCAUUA-3' copies the template "
        "itself; 5'-AUUACG-3' is the template reversed with U, not complemented.",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "Transcription", "Advanced", "direct",
    "In a transcription unit, the positions of the promoter and the terminator are experimentally switched. According "
    "to NCERT, what is the expected consequence?",
    P("The definitions of the template strand and the coding strand would be reversed",
      ["Transcription would stop completely, because a terminator can never lie upstream of a gene",
       "Both strands of the DNA would be transcribed at the same time",
       "The same strand would remain the template, but RNA would be synthesised in the 3'→5' direction"], "A"),
    "Promoter defines the template and coding strands",
    "The promoter is the binding site for RNA polymerase, and its presence in a transcription unit also defines which "
    "strand is the template and which is the coding strand. NCERT notes that by switching its position with the "
    "terminator, the definition of coding and template strands could be reversed. RNA is always synthesised 5'→3'.",
    ["Promoter position defines the template strand", "Switch promoter and terminator → strands reverse roles"],
    C12_MB("transcription: transcription unit"),
    why="NCERT states that the strands' roles reverse, not that transcription stops; only one strand is ever "
        "transcribed in a given segment; RNA polymerase always polymerises 5'→3'.",
    seconds=45)

add(MBI, "DNA as genetic material", "Advanced", "direct",
    "Avery, MacLeod and McCarty found that treating the purified extract of heat-killed S-strain bacteria with "
    "proteases or with RNases did not stop it from transforming R-strain bacteria. This result showed that:",
    P("Neither protein nor RNA was the transforming substance",
      ["Protein was the transforming substance", "RNA was the transforming substance",
       "DNA was not needed for transformation"], "B"),
    "Biochemical characterisation of the transforming principle",
    "If the transforming substance were a protein, proteases would destroy it; if it were RNA, RNases would destroy it. "
    "Since transformation still occurred after both treatments, the substance was neither protein nor RNA. Digestion "
    "with DNase did inhibit transformation, suggesting that DNA caused the transformation.",
    ["Protease: no effect → not protein", "RNase: no effect → not RNA", "DNase: blocks → DNA"],
    C12_MB("the search for genetic material: biochemical characterisation of transforming principle"),
    why="Activity surviving protease and RNase rules out protein and RNA; the separate DNase result shows DNA was "
        "required.",
    seconds=40)

add(MBI, "Genetic code and translation", "Advanced", "direct",
    "A point mutation changes an mRNA codon from UUU to UUC. Both codons code for phenylalanine. What is the effect on "
    "the polypeptide, and which property of the genetic code explains it?",
    P("The amino acid sequence is unchanged, because the code is degenerate",
      ["All amino acids after this point are altered, because the reading frame shifts",
       "Translation stops at this point, because UUC is a stop codon",
       "A different amino acid is inserted, because the code is unambiguous"], "C"),
    "Degeneracy of the genetic code",
    "Some amino acids are coded by more than one codon; hence the code is degenerate. A substitution that turns UUU "
    "into UUC still specifies phenylalanine, so the protein is unchanged. A single-base substitution does not shift the "
    "reading frame, and UUC is not a stop codon (the stop codons are UAA, UAG and UGA).",
    ["Substitution, not insertion/deletion → no frame-shift", "UUU and UUC both = Phe → degenerate code",
     "Protein unchanged"],
    C12_MB("genetic code; mutations and genetic code"),
    why="Frame-shifts come from insertions or deletions; UUC codes for phenylalanine, not 'stop'; unambiguity means "
        "one codon codes for one amino acid, which here is still phenylalanine.",
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "multi_statement",
    ms("Which of the following statements about the methods of the Human Genome Project are correct?",
       ["For sequencing, the total DNA from a cell was isolated and converted into random fragments of relatively "
        "smaller sizes.",
        "The sequences of the fragments were arranged on the basis of overlapping regions, using specialised "
        "computer-based programs.",
        "Genetic and physical maps were assigned using information on polymorphism of restriction endonuclease "
        "recognition sites and repetitive sequences known as microsatellites.",
        "The human DNA was sequenced as one intact molecule, without breaking it into fragments.",
        "Expressed sequence tags (ESTs) refers to sequencing the whole genome, coding and non-coding, and assigning "
        "functions to its regions later."]),
    MS(["a", "b", "c"], [["a", "b", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "Methodology of the Human Genome Project",
    "NCERT: total DNA was converted into random small fragments, cloned in hosts using vectors and sequenced with "
    "automated sequencers. The sequences were arranged using overlapping regions, which needed specialised computer "
    "programs because alignment was humanly impossible. Genetic and physical maps were generated using polymorphism "
    "of restriction endonuclease recognition sites and microsatellites. ESTs focus on genes expressed as RNA; "
    "sequencing the whole genome and assigning functions later is sequence annotation.",
    ["(a), (b), (c): true", "(d): false, DNA was fragmented", "(e): false, that describes sequence annotation"],
    C12_MB("human genome project: methodologies"),
    why="Options A, B and C each include (d) or (e).",
    seconds=60)

add(MBI, "Transcription", "Advanced", "direct",
    "A eukaryotic structural gene consists of exons E1, E2 and E3 separated by introns I1 and I2 "
    "(E1-I1-E2-I2-E3). After processing in the nucleus, the mRNA transported to the cytoplasm contains:",
    P("E1-E2-E3 joined in the same order, with a methyl guanosine triphosphate cap at the 5'-end and a poly-A tail at "
      "the 3'-end",
      ["E1-I1-E2-I2-E3, with a cap at the 5'-end and a poly-A tail at the 3'-end",
       "I1-I2 joined together, with a cap and a tail",
       "E1-E2-E3 joined in the same order, without any cap or tail"], "A"),
    "Processing of hnRNA",
    "The primary transcript (hnRNA) contains both exons and introns and is non-functional. It undergoes splicing, in "
    "which introns are removed and exons are joined in a defined order, and capping (methyl guanosine triphosphate "
    "added to the 5'-end) and tailing (200-300 adenylate residues added to the 3'-end). The fully processed hnRNA, now "
    "mRNA, is transported out of the nucleus for translation.",
    ["Splicing: introns out, exons joined in order", "Capping at 5'; tailing at 3'", "Processed mRNA leaves the "
     "nucleus"],
    C12_MB("transcription: processing in eukaryotes"),
    why="Option B is the unspliced primary transcript; introns are removed, not retained (option C); mature mRNA is "
        "capped and tailed (option D).",
    seconds=45)

add(MBI, "Genetic code and translation", "Advanced", "assertion_reason",
    ar("The genetic code is degenerate.",
       "One codon codes for only one amino acid; hence the code is unambiguous and specific."),
    AR("B"),
    "Degeneracy versus unambiguity",
    "Degeneracy means that some amino acids are coded by more than one codon (e.g. UUU and UUC for phenylalanine), so "
    "A is true. Unambiguity means that each codon specifies only one amino acid, so R is true. R describes a different "
    "property: it says nothing about several codons sharing one amino acid, so it does not explain A.",
    ["A: true (many codons → one amino acid)", "R: true (one codon → one amino acid)",
     "Different properties; R does not explain A"],
    C12_MB("genetic code"),
    seconds=35)


# ================================================================ Microbes in Human Welfare (3 / 3 / 2)
C12_MH = lambda s: ref(12, MHW, s)

add(MHW, "Sewage treatment", "Basic", "direct",
    "Which of the following statements about the microbial treatment of sewage is made in NCERT?",
    P("It has been practised for more than a century, and no man-made technology has so far been able to rival it",
      ["It was introduced only after the Ganga Action Plan and is still at an experimental stage",
       "It has now been fully replaced by chemical treatment in most parts of the world",
       "It relies only on anaerobic bacteria from start to finish"], "A"),
    "Microbes in sewage treatment",
    "Sewage is treated in sewage treatment plants (STPs) by heterotrophic microbes naturally present in it. NCERT notes "
    "that this methodology has been practised for more than a century in almost all parts of the world, and till date "
    "no man-made technology has been able to rival the microbial treatment of sewage.",
    ["Microbial STP methodology: over a century old", "Not rivalled by any man-made technology"],
    C12_MH("microbes in sewage treatment"),
    why="The method long predates the Ganga Action Plan; it has not been replaced; secondary treatment begins with "
        "aerobic microbes in aeration tanks, and only the sludge digesters are anaerobic.",
    seconds=25)

add(MHW, "Household and industrial products", "Basic", "direct",
    "'Anti' is a Greek word meaning 'against', and 'bio' means 'life'. According to NCERT, with reference to human "
    "beings, antibiotics are:",
    P("'Pro life', although the word means 'against life' in the context of disease-causing organisms",
      ["'Against life', because they harm the cells of the human body",
       "Neither pro life nor against life, because they act only on viruses",
       "'Against life', because they are produced only by human cells"], "C"),
    "Meaning of the term antibiotic",
    "Antibiotics are chemical substances produced by some microbes that can kill or retard the growth of other "
    "(disease-causing) microbes. Together, 'anti' and 'bio' mean 'against life' in the context of disease-causing "
    "organisms, whereas with reference to human beings they are 'pro life' and not against.",
    ["Against disease-causing organisms", "Pro life for human beings"],
    C12_MH("microbes in industrial products: antibiotics"),
    why="Antibiotics are produced by microbes and act on other microbes; NCERT explicitly calls them 'pro life' for "
        "humans.",
    seconds=25)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "Baculoviruses of the genus Nucleopolyhedrovirus are described by NCERT as especially desirable as biocontrol "
    "agents when:",
    P("Beneficial insects are being conserved as part of an integrated pest management (IPM) programme, or an "
      "ecologically sensitive area is being treated",
      ["A broad-spectrum insecticide is needed to kill all the insects in a field",
       "Weeds have to be removed from paddy fields",
       "Nitrogen fixation has to be increased in leguminous crops"], "B"),
    "Baculoviruses as narrow-spectrum biocontrol agents",
    "Baculoviruses attack insects and other arthropods. They are species-specific, narrow-spectrum insecticidal "
    "applications with no negative impacts on plants, mammals, birds, fish or even non-target insects. This is "
    "especially desirable when beneficial insects are being conserved to aid an overall IPM programme, or when an "
    "ecologically sensitive area is being treated.",
    ["Species-specific, narrow spectrum", "Safe for non-target organisms → useful in IPM and sensitive areas"],
    C12_MH("microbes as biocontrol agents"),
    why="Baculoviruses are narrow-spectrum, not broad-spectrum; they are not herbicides or nitrogen fixers.",
    seconds=30)

add(MHW, "Sewage treatment", "Intermediate", "assertion_reason",
    ar("Sewage water cannot be discharged directly into natural water bodies such as rivers and streams.",
       "Sewage contains large amounts of organic matter and microbes, many of which are pathogenic."),
    AR("A"),
    "Why sewage must be treated",
    "NCERT: municipal waste-water (sewage) contains large amounts of organic matter and microbes, many of which are "
    "pathogenic; this is why it cannot be discharged into natural water bodies directly and is first treated in "
    "sewage treatment plants. R is the reason for A.",
    ["A: true", "R: true", "Organic load + pathogens → must be treated before discharge; R explains A"],
    C12_MH("microbes in sewage treatment"),
    seconds=30)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "multi_statement",
    ms("Which of the following statements are correct according to NCERT?",
       ["Chemical pesticides and insecticides are toxic and extremely harmful to human beings and animals alike.",
        "These chemicals have been polluting our environment (soil, ground water), fruits, vegetables and crop "
        "plants.",
        "Our soil is also polluted through the use of weedicides to remove weeds.",
        "Nucleopolyhedroviruses harm birds, mammals and fish along with the target insects.",
        "The ladybird beetle is used mainly to get rid of mosquitoes."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
    "Problems with chemical pest control",
    "NCERT: chemical pesticides and insecticides are toxic and extremely harmful to human beings and animals, and "
    "pollute soil, ground water, fruits, vegetables and crop plants; weedicides also pollute the soil. "
    "Nucleopolyhedroviruses are species-specific with no negative impacts on plants, mammals, birds, fish or "
    "non-target insects. Ladybird beetles control aphids; dragonflies control mosquitoes.",
    ["(a), (b), (c): true", "(d): false, NPVs are narrow-spectrum", "(e): false, ladybirds control aphids"],
    C12_MH("microbes as biocontrol agents"),
    why="Options A, B and C each include (d) or (e).",
    seconds=45)

add(MHW, "Household and industrial products", "Intermediate", "match_list",
    ml(("microbe named in NCERT", "kind of organism"),
       ["Trichoderma polysporum (source of cyclosporin A)",
        "Saccharomyces cerevisiae (commercial production of ethanol)", "Streptococcus (source of streptokinase)", "Nucleopolyhedrovirus (biocontrol agent)"],
       ["Virus", "Bacterium", "Fungus", "Yeast"]),
    M({"A": "III", "B": "IV", "C": "II", "D": "I"},
      [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
       {"A": "II", "B": "IV", "C": "III", "D": "I"}], "C"),
    "Kinds of microbes used by humans",
    "NCERT: cyclosporin A is produced by the fungus Trichoderma polysporum; ethanol is produced commercially using "
    "the yeast Saccharomyces cerevisiae (brewer's yeast); streptokinase by the bacterium Streptococcus; and "
    "baculoviruses of the genus Nucleopolyhedrovirus are viral biocontrol agents.",
    ["Trichoderma polysporum: fungus", "Saccharomyces cerevisiae: yeast", "Streptococcus: bacterium",
     "Nucleopolyhedrovirus: virus"],
    C12_MH("microbes in industrial products: fermented beverages; chemicals, enzymes and other bioactive "
           "molecules; biocontrol agents"),
    why="Option A swaps the fungus and the yeast; option B swaps the bacterium and the virus; option D calls "
        "Trichoderma a bacterium.",
    seconds=40)

add(MHW, "Sewage treatment", "Advanced", "direct",
    "Which of the following gives the correct sequence of steps in the treatment of municipal sewage?",
    P("Sequential filtration → sedimentation → aeration tank (flocs form) → settling tank (activated sludge) → "
      "anaerobic sludge digester",
      ["Sedimentation → sequential filtration → settling tank → aeration tank → anaerobic sludge digester",
       "Sequential filtration → sedimentation → anaerobic sludge digester → aeration tank → settling tank",
       "Sequential filtration → aeration tank → sedimentation → anaerobic sludge digester → settling tank"], "D"),
    "Stages of sewage treatment",
    "Primary treatment removes floating debris by sequential filtration and grit by sedimentation, giving the primary "
    "effluent. In secondary treatment the effluent is aerated in large tanks where aerobic microbes form flocs and "
    "reduce the BOD; it is then passed to a settling tank where the flocs sediment as activated sludge. A small part "
    "of the sludge is pumped back as inoculum; the major part goes to anaerobic sludge digesters.",
    ["Primary: filtration, sedimentation", "Secondary: aeration tank → settling tank",
     "Sludge: anaerobic sludge digester"],
    C12_MH("microbes in sewage treatment"),
    why="Filtration precedes sedimentation; the aeration tank comes before the settling tank; the anaerobic digester "
        "receives activated sludge from the settling tank, so it comes last.",
    seconds=45)

add(MHW, "Household and industrial products", "Advanced", "statement_pair",
    sp("Antibiotics produced by microbes are regarded as one of the most significant discoveries of the twentieth "
       "century.",
       "Penicillin, the first antibiotic to be discovered, was found through a planned, systematic screening of "
       "moulds."),
    SP("C"),
    "Discovery of penicillin",
    "NCERT regards antibiotics as one of the most significant discoveries of the twentieth century (Statement I true). "
    "Penicillin was the first antibiotic to be discovered, and it was a chance discovery: Fleming noticed a mould "
    "growing in one of his unwashed culture plates around which Staphylococci could not grow (Statement II false).",
    ["Statement I: true", "Statement II: false, penicillin was a chance discovery"],
    C12_MH("microbes in industrial products: antibiotics"),
    seconds=30)


# ================================================================ Organisms and Populations (4 / 6 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population attributes", "Basic", "direct",
    "In ecology, a population is best described as a group of individuals:",
    P("Of a given species living in a well-defined geographical area, sharing or competing for similar resources and "
      "potentially interbreeding",
      ["Of different species living together and interacting in an area",
       "Of all species, together with the physical environment in which they live",
       "Of a given species, wherever they occur in the world, whether or not they can interbreed"], "B"),
    "Definition of a population",
    "NCERT: in nature we rarely find isolated single individuals; they live in groups in a well-defined geographical "
    "area, share or compete for similar resources and potentially interbreed, and thus constitute a population.",
    ["Same species + defined area + shared resources + potential interbreeding = population"],
    C12_OP("populations: population attributes"),
    why="Several interacting species form a community; organisms plus their physical environment form an ecosystem; a "
        "population is restricted to a defined area.",
    seconds=25)

add(OAP, "Population interactions", "Basic", "direct",
    "Many parasites need intermediate hosts or vectors. According to NCERT, the malarial parasite needs:",
    P("A vector (mosquito) to spread to other hosts",
      ["A snail as its intermediate host", "A fish as its intermediate host",
       "No other organism, because it spreads by direct contact"], "D"),
    "Parasites with complex life cycles",
    "NCERT: many parasites have complex life cycles involving one or two intermediate hosts or vectors to parasitise "
    "the primary host. The human liver fluke depends on two intermediate hosts (a snail and a fish), and the malarial "
    "parasite needs a vector (mosquito) to spread to other hosts.",
    ["Liver fluke: snail and fish", "Malarial parasite: mosquito vector"],
    C12_OP("population interactions: parasitism"),
    why="The snail and the fish are the intermediate hosts of the human liver fluke; the malarial parasite does not "
        "spread by direct contact.",
    seconds=25)

add(OAP, "Population attributes", "Basic", "statement_pair",
    sp("The size of a population is not a static parameter; it keeps changing with time depending on factors such as "
       "food availability, predation pressure and adverse weather.",
       "Sex ratio and age distribution are attributes of an individual organism rather than of a population."),
    SP("C"),
    "Population size and population attributes",
    "NCERT: the size of a population for any species keeps changing with time, depending on various factors including "
    "food availability, predation pressure and adverse weather (Statement I true). Birth rate, death rate, sex ratio "
    "and age distribution are attributes of a population, not of an individual (Statement II false).",
    ["Statement I: true", "Statement II: false, these are population attributes"],
    C12_OP("populations: population attributes; population growth"),
    seconds=30)

add(OAP, "Population interactions", "Basic", "direct",
    "Lice living on humans, which feed from the external surface of the host, are examples of:",
    P("Ectoparasites", ["Endoparasites", "Brood parasites", "Commensals"], "A"),
    "Ectoparasites",
    "Parasites that feed on the external surface of the host organism are called ectoparasites; NCERT's examples are "
    "the lice on humans and ticks on dogs. Endoparasites live inside the host body; brood parasites (the cuckoo) lay "
    "eggs in the host's nest.",
    ["External surface → ectoparasite", "Examples: lice on humans, ticks on dogs"],
    C12_OP("population interactions: parasitism"),
    why="Endoparasites live inside the host; brood parasitism involves egg-laying in the host's nest; commensals do not "
        "harm their partner.",
    seconds=20)

_op_K, _op_N = 500, 400
_op_frac = F(_op_K - _op_N, _op_K)
assert _op_frac == F(1, 5) and F(_op_N, _op_K) == F(4, 5) and F(_op_K - _op_N, _op_N) == F(1, 4)

add(OAP, "Population growth", "Intermediate", "numerical",
    "A population grows according to the logistic model, dN/dt = rN[(K − N)/K], in a habitat with carrying capacity "
    "K = 500. When N = 400, its actual growth rate is what percentage of the growth rate it would have had under "
    "exponential growth (dN/dt = rN) with the same r and the same N?",
    P("20 per cent", ["80 per cent", "25 per cent", "0 per cent"], "C"),
    "Effect of the logistic factor (K − N)/K",
    "Dividing the logistic rate by the exponential rate gives (K − N)/K = (500 − 400)/500 = 0.2, i.e. 20 per cent. "
    "As N approaches K, this factor falls towards zero and the growth rate slows.",
    ["Ratio = rN(K − N)/K ÷ rN = (K − N)/K", "= 100/500 = 0.2 = 20%"],
    C12_OP("populations: population growth - growth models"),
    why="80 per cent is N/K (the fraction of K already reached); 25 per cent divides by N instead of K; 0 per cent "
        "applies only when N = K.",
    seconds=50, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Intermediate", "direct",
    "According to NCERT, competition is best defined as a process in which:",
    P("The fitness of one species, measured in terms of its 'r' (intrinsic rate of increase), is significantly lower "
      "in the presence of another species",
      ["The fitness of both species increases in each other's presence",
       "One species benefits while the other is neither harmed nor benefited",
       "One species lives on or in another and derives its nourishment from it"], "B"),
    "Definition of competition",
    "NCERT defines competition as a process in "
    "which the fitness of one species (measured in terms of its 'r', intrinsic rate of increase) is significantly "
    "lower in the presence of another species. It can occur even between unrelated species and even when resources "
    "are not limiting (interference competition).",
    ["Competition: lowered r of one species in the presence of another"],
    C12_OP("population interactions: competition"),
    why="Mutual benefit is mutualism; one benefiting with the other unaffected is commensalism; living on or in a host "
        "for nourishment is parasitism.",
    seconds=30)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("Mycorrhizae, associations between fungi and the roots of higher plants, are an example of mutualism.",
       "The fungi help the plant absorb essential nutrients from the soil, while the plant provides the fungi with "
       "energy-yielding carbohydrates."),
    AR("A"),
    "Mycorrhizal mutualism",
    "In mutualism both interacting species benefit. In mycorrhizae, the fungi help the plant absorb essential "
    "nutrients from the soil, and the plant in turn provides the fungi with energy-yielding carbohydrates. This "
    "two-way benefit is exactly why the association is mutualism, so R explains A.",
    ["A: true", "R: true", "Both partners benefit → mutualism; R explains A"],
    C12_OP("population interactions: mutualism"),
    seconds=30)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following statements about mutualism are correct?",
       ["Lichens represent an intimate mutualistic relationship between a fungus and photosynthesising algae or "
        "cyanobacteria.",
        "The fig wasp pollinates the fig inflorescence while searching for suitable egg-laying sites.",
        "Plant-animal interactions often involve co-evolution of the mutualists.",
        "In mutualism, one species benefits while the other is harmed.",
        "Mutualism occurs only between plants and animals."]),
    MS(["a", "b", "c"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
    "Examples and nature of mutualism",
    "Mutualism benefits both species. Lichens are an intimate mutualism between a fungus and photosynthesising algae "
    "or cyanobacteria; mycorrhizae link fungi and plant roots, so mutualism is not limited to plants and animals. In "
    "the fig-wasp association, the wasp pollinates the fig inflorescence while searching for egg-laying sites. NCERT "
    "notes that plant-animal interactions often involve co-evolution of the mutualists.",
    ["(a), (b), (c): true", "(d): false, that is parasitism or predation",
     "(e): false, lichens and mycorrhizae involve fungi"],
    C12_OP("population interactions: mutualism"),
    why="Options A, B and C each include (d) or (e).",
    seconds=45)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("In commensalism, both the interacting species benefit.",
       "In amensalism, one species benefits while the other is unaffected."),
    SP("B"),
    "Commensalism and amensalism",
    "Commensalism is an interaction in which one species benefits and the other is neither harmed nor benefited "
    "(Statement I false). Amensalism is one in which one species is harmed and the other is unaffected (Statement II "
    "false; 'benefits and unaffected' describes commensalism).",
    ["Statement I: false (+/0, not +/+)", "Statement II: false (−/0, not +/0)"],
    C12_OP("population interactions"),
    seconds=30)

add(OAP, "Population growth", "Intermediate", "direct",
    "No population of any species in nature has unlimited resources at its disposal to permit exponential growth. "
    "According to NCERT, this leads to:",
    P("Competition between individuals for the limited resources, so that eventually the 'fittest' individuals "
      "survive and reproduce",
      ["Unlimited growth of the population until it reaches a J-shaped peak and then stays there",
       "Equal survival of all individuals irrespective of their fitness",
       "Immediate extinction of the population"], "C"),
    "Resource limitation and logistic growth",
    "Because resources are finite, individuals compete for limited resources, and eventually the 'fittest' individual "
    "survives and reproduces. A population growing in a habitat with limited resources therefore shows logistic "
    "(sigmoid) growth that levels off at the carrying capacity.",
    ["Limited resources → competition between individuals", "Fittest survive and reproduce → logistic growth"],
    C12_OP("populations: population growth - logistic growth"),
    why="A J-shaped curve does not level off; NCERT stresses unequal survival of the fittest; limited resources slow "
        "growth rather than cause immediate extinction.",
    seconds=30)

add(OAP, "Population interactions", "Advanced", "assertion_reason",
    ar("Pollination of the Mediterranean orchid Ophrys would decline if, during evolution, the colour pattern of the "
       "female bee changed even slightly and the orchid did not co-evolve.",
       "Ophrys employs sexual deceit: one petal bears an uncanny resemblance to the female of the bee in size, colour "
       "and markings, and the male bee pseudocopulates with the flower, getting dusted with pollen."),
    AR("A"),
    "Co-evolution of Ophrys and its pollinator",
    "Ophrys is pollinated only because a petal mimics the female bee; the male bee is attracted, 'pseudocopulates' and "
    "transfers pollen when it visits another flower. NCERT notes that if the female bee's colour patterns change even "
    "slightly for any reason during evolution, pollination success will be reduced unless the orchid flower "
    "co-evolves to maintain the resemblance. Since the dependence on mimicry (R) is what makes pollination sensitive to "
    "the bee's appearance, R explains A.",
    ["A: true", "R: true", "Pollination depends on resemblance → any change in the bee reduces success; R explains A"],
    C12_OP("population interactions: mutualism"),
    seconds=45)

add(OAP, "Population growth", "Advanced", "multi_statement",
    ms("Consider the exponential model dN/dt = rN and the logistic model dN/dt = rN[(K − N)/K]. Which of the "
       "following statements are correct?",
       ["When N is very small compared with K, logistic growth is nearly exponential.",
        "In logistic growth, dN/dt is maximum when N = K.",
        "In logistic growth, the per capita growth rate decreases as N increases.",
        "In exponential growth, the per capita growth rate remains constant at r.",
        "In exponential growth, dN/dt does not depend on N."]),
    MS(["a", "c", "d"], [["a", "b", "d"], ["b", "c", "e"], ["c", "d", "e"]], "C"),
    "Comparing the growth models",
    "Per capita rate = (dN/dt)/N. Exponential: (dN/dt)/N = r, a constant, while dN/dt = rN rises with N. Logistic: "
    "per capita rate = r(K − N)/K, which falls as N rises; when N ≪ K the factor (K − N)/K ≈ 1 and growth is nearly "
    "exponential. When N = K the factor is zero, so dN/dt = 0 (the asymptote), not maximum.",
    ["(a): (K − N)/K ≈ 1 → true", "(b): at N = K, dN/dt = 0 → false", "(c): r(K − N)/K falls → true",
     "(d): (dN/dt)/N = r → true", "(e): dN/dt = rN depends on N → false"],
    C12_OP("populations: population growth - growth models"),
    why="Option A includes (b), option B includes (b) and (e), and option D includes (e).",
    seconds=75)

_op_N0, _op_b, _op_d, _op_I, _op_E = 2000, F(1, 10), F(4, 100), 30, 50
_op_N1 = _op_N0 + _op_b * _op_N0 - _op_d * _op_N0 + _op_I - _op_E
assert _op_N1 == 2100
assert _op_N0 + _op_b * _op_N0 - _op_d * _op_N0 == 2120                          # migration ignored
assert _op_N0 + _op_b * _op_N0 - _op_d * _op_N0 + _op_I + _op_E == 2200          # emigration added

add(OAP, "Population growth", "Advanced", "numerical",
    "A population of 2000 individuals has a per capita birth rate of 0.1 and a per capita death rate of 0.04 per "
    "individual per year. During the year, 30 individuals immigrate and 50 emigrate. Using "
    "N(t+1) = N(t) + [(B + I) − (D + E)], the population after one year is:",
    P("2100", ["2120", "2200", "1980"], "B"),
    "Population density change from birth and death rates and migration",
    "Convert per capita rates into numbers: B = 0.1 × 2000 = 200 births and D = 0.04 × 2000 = 80 deaths. Then "
    "N(t+1) = 2000 + (200 + 30) − (80 + 50) = 2100.",
    ["B = 200, D = 80", "I = 30, E = 50", "N(t+1) = 2000 + 230 − 130 = 2100"],
    C12_OP("populations: population growth"),
    why="2120 ignores migration; 2200 adds emigrants instead of subtracting them; 1980 treats the rates 0.1 and 0.04 "
        "as numbers of individuals.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "assertion_reason",
    ar("In both predation and parasitism, both the interacting species benefit.",
       "In predation and parasitism, only one species (the predator or the parasite) benefits, and the interaction is "
       "detrimental to the other (the prey or the host)."),
    AR("D"),
    "Effect of predation and parasitism on the two species",
    "NCERT: both species benefit in mutualism and both lose in competition. In both parasitism and predation only one "
    "species benefits (parasite and predator, respectively) and the interaction is detrimental to the other (host and "
    "prey, respectively). So A is false and R is true.",
    ["A: false", "R: true (+/− interactions)"],
    C12_OP("population interactions"),
    seconds=30)


# ================================================================ Ecosystem (3 / 5 / 3)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Structure and components", "Basic", "match_list",
    ml(("functional group", "example given in NCERT"),
       ["Herbivores of terrestrial ecosystems", "Herbivores of aquatic ecosystems",
        "Producers of aquatic ecosystems", "Decomposers"],
       ["Molluscs", "Fungi and bacteria", "Insects, birds and mammals", "Phytoplankton, some algae and higher plants"]),
    M({"A": "III", "B": "I", "C": "IV", "D": "II"},
      [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
       {"A": "IV", "B": "I", "C": "III", "D": "II"}], "A"),
    "Members of the functional groups of ecosystems",
    "NCERT: the common herbivores are insects, birds and mammals in terrestrial ecosystems and molluscs in aquatic "
    "ecosystems. In aquatic ecosystems the primary producers are phytoplankton, some algae and higher plants. "
    "Decomposers are heterotrophic organisms, mainly fungi and bacteria.",
    ["Terrestrial herbivores: insects, birds, mammals", "Aquatic herbivores: molluscs",
     "Aquatic producers: phytoplankton, some algae, higher plants", "Decomposers: fungi, bacteria"],
    C12_EC("ecosystem - structure and function; energy flow"),
    why="Option B swaps the terrestrial and aquatic herbivores; option C swaps producers and decomposers; option D "
        "gives the producers to the terrestrial herbivores.",
    seconds=30)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "According to NCERT, the basic requirement for any ecosystem to function and sustain itself is:",
    P("A constant input of solar energy",
      ["A constant input of chemical fertilisers", "The absence of decomposers",
       "An inverted pyramid of biomass"], "D"),
    "Solar energy as the driving input",
    "NCERT opens the section on productivity by stating that a constant input of solar energy is the basic requirement "
    "for any ecosystem to function and sustain. Plants convert part of this energy into organic matter (primary "
    "production).",
    ["Constant solar input → primary production → rest of the ecosystem"],
    C12_EC("productivity"),
    why="Fertilisers are not a basic requirement of natural ecosystems; decomposers are essential; pyramids describe "
        "structure and are not a requirement.",
    seconds=20)

add(ECO, "Structure and components", "Basic", "direct",
    "Decomposers secrete digestive enzymes that break down dead and waste materials into simple inorganic materials, "
    "which they then absorb. Decomposers are therefore also known as:",
    P("Saprotrophs", ["Autotrophs", "Producers", "Herbivores"], "C"),
    "Decomposers as saprotrophs",
    "NCERT: decomposers are also known as saprotrophs (sapro: to decompose). They secrete digestive enzymes that break "
    "down dead and waste materials into simple inorganic materials, which are subsequently absorbed by them.",
    ["Decomposers = saprotrophs ('sapro' = to decompose)"],
    C12_EC("energy flow"),
    why="Autotrophs and producers make their own food; herbivores feed on living plants.",
    seconds=20)

add(ECO, "Energy flow", "Intermediate", "direct",
    "According to NCERT, the energy trapped by a producer is either passed on to a consumer or:",
    P("The organism dies, and its death is the beginning of the detritus food chain/web",
      ["It is returned to the sun as reflected light", "It is stored permanently in the producer and never released",
       "It is recycled back to the same producer by herbivores"], "B"),
    "Fate of energy fixed by producers",
    "NCERT: the energy trapped by the producer is either passed on to a consumer or the organism dies. Death of the "
    "organism is the beginning of the detritus food chain/web, through which decomposers obtain energy.",
    ["Producer energy → consumer, or", "Producer dies → detritus food chain/web begins"],
    C12_EC("energy flow"),
    why="Energy flow is unidirectional and is not returned to the sun or recycled to the producer; stored energy is "
        "released when the producer is eaten or decomposed.",
    seconds=25)

add(ECO, "Structure and components", "Intermediate", "statement_pair",
    sp("The interaction of biotic and abiotic components results in a physical structure that is characteristic of "
       "each type of ecosystem.",
       "Primary productivity is the same in all ecosystems, because it does not depend on the plant species or on "
       "environmental factors."),
    SP("C"),
    "Structure of ecosystems; factors affecting productivity",
    "NCERT: interaction of biotic and abiotic components results in a physical structure characteristic of each type "
    "of ecosystem (Statement I true). Primary productivity depends on the plant species inhabiting an area and on "
    "environmental factors, the availability of nutrients and the photosynthetic capacity of plants, so it varies in "
    "different types of ecosystems (Statement II false).",
    ["Statement I: true", "Statement II: false, productivity varies between ecosystems"],
    C12_EC("ecosystem - structure and function; productivity"),
    seconds=30)

add(ECO, "Ecological pyramids", "Intermediate", "multi_statement",
    ms("Which of the following statements about ecological pyramids are correct?",
       ["In a pyramid of energy, the bar for the producers is the widest.",
        "In the pyramid of biomass of a sea, the bar for the phytoplankton is narrower than the bar for the fishes.",
        "A pyramid of energy becomes inverted when the producers are small in size.",
        "In a grassland, the pyramid of numbers is narrowest at the level of the top carnivores.",
        "The apex of an ecological pyramid is formed by the decomposers."]),
    MS(["a", "b", "d"], [["a", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "A"),
    "Reading the three ecological pyramids",
    "Energy is always lost as heat at each step, so the producer bar of the energy pyramid is always the widest and the "
    "pyramid can never be inverted. In the sea, the biomass of fishes far exceeds that of phytoplankton, so the biomass "
    "pyramid is inverted (narrow producer bar). In a grassland, producers far outnumber herbivores, which outnumber "
    "carnivores, so the top carnivores form the narrow apex. Decomposers (saprophytes) are not given any place in "
    "ecological pyramids.",
    ["(a), (b), (d): true", "(c): false, the energy pyramid is never inverted",
     "(e): false, saprophytes have no place in pyramids"],
    C12_EC("ecological pyramids"),
    why="Options B, C and D each include (c) or (e).",
    seconds=50)

add(ECO, "Productivity and decomposition", "Intermediate", "assertion_reason",
    ar("The net primary productivity of an ecosystem is always less than its gross primary productivity.",
       "A considerable amount of gross primary productivity is utilised by plants in respiration."),
    AR("A"),
    "GPP, respiration and NPP",
    "Gross primary productivity is the rate of production of organic matter during photosynthesis. A considerable part "
    "of it is used by the plants in respiration (R), and NPP = GPP − R. Because R is always subtracted, NPP is less "
    "than GPP; R is the direct reason.",
    ["A: true", "R: true", "NPP = GPP − R → R explains A"],
    C12_EC("productivity"),
    seconds=30)

add(ECO, "Ecological pyramids", "Intermediate", "assertion_reason",
    ar("Like its pyramid of biomass, the pyramid of energy of a sea is inverted.",
       "In a sea, the biomass of fishes far exceeds that of the phytoplankton."),
    AR("D"),
    "Inverted biomass pyramid versus upright energy pyramid",
    "The pyramid of biomass in a sea is generally inverted because the biomass of fishes far exceeds that of the "
    "phytoplankton, so R is true. The pyramid of energy, however, is always upright and can never be inverted, "
    "because energy is lost as heat at every step from one trophic level to the next. So A is false.",
    ["A: false, energy pyramids are always upright", "R: true"],
    C12_EC("ecological pyramids"),
    seconds=30)

_ec_levels = [8000, 640, 64]
_ec_eff = [F(_ec_levels[i + 1], _ec_levels[i]) * 100 for i in range(2)]
assert _ec_eff == [8, 10]
assert F(_ec_levels[0], _ec_levels[1]) == F(25, 2)          # distractor: ratio inverted (12.5)

add(ECO, "Energy flow", "Advanced", "numerical",
    "In an ecosystem, the energy present at successive trophic levels is: producers 8,000 kJ m⁻² yr⁻¹, herbivores "
    "640 kJ m⁻² yr⁻¹ and primary carnivores 64 kJ m⁻² yr⁻¹. What percentage of energy is transferred from producers to "
    "herbivores, and from herbivores to primary carnivores, respectively?",
    P("8 per cent and 10 per cent", ["10 per cent and 8 per cent", "12.5 per cent and 10 per cent",
                                     "92 per cent and 90 per cent"], "C"),
    "Efficiency of energy transfer between trophic levels",
    "Transfer efficiency = energy at the higher level ÷ energy at the lower level × 100. Producers → herbivores: "
    "640/8000 × 100 = 8 per cent. Herbivores → carnivores: 64/640 × 100 = 10 per cent. NCERT's 10 per cent law is an "
    "approximation; the rest of the energy is lost, mostly as heat.",
    ["640/8000 = 0.08 → 8%", "64/640 = 0.10 → 10%"],
    C12_EC("energy flow; ecological pyramids"),
    why="Option A reverses the order; 12.5 is the inverted ratio 8000/640 (not a percentage); 92 and 90 per cent are "
        "the fractions not transferred.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Structure and components", "Advanced", "assertion_reason",
    ar("Decomposers are heterotrophic organisms.",
       "Humus is highly resistant to microbial action and undergoes decomposition at an extremely slow rate."),
    AR("B"),
    "Decomposers and humus",
    "Decomposers, mainly fungi and bacteria, are heterotrophs that meet their energy and nutrient requirements by "
    "degrading dead organic matter, so A is true. Humus is highly resistant to microbial action and decomposes "
    "extremely slowly, so R is true. R describes a property of humus and does not explain why decomposers are "
    "heterotrophic.",
    ["A: true", "R: true", "R concerns humus, not the nutrition of decomposers"],
    C12_EC("energy flow; decomposition"),
    seconds=35)

add(ECO, "Ecological pyramids", "Advanced", "assertion_reason",
    ar("In NCERT's pyramid of numbers for a grassland ecosystem, the top carnivores are the fewest in number.",
       "Top carnivores capture the largest share of the energy that flows through the ecosystem."),
    AR("C"),
    "Numbers and energy at the top of the food chain",
    "In the grassland pyramid of numbers, producers far outnumber herbivores, herbivores outnumber carnivores, and the "
    "top carnivores are the fewest, so A is true. Energy decreases at each successive trophic level because energy is "
    "lost as heat at every transfer, so the top carnivores receive the smallest share of energy, not the largest; R is "
    "false.",
    ["A: true", "R: false, the top level receives the least energy"],
    C12_EC("ecological pyramids; energy flow"),
    seconds=35)


# ================================================================ Biodiversity and Conservation (3 / 5 / 3)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "The term 'biodiversity', popularised by the sociobiologist Edward Wilson, describes:",
    P("The combined diversity at all the levels of biological organisation",
      ["Only the number of species found in a region", "Only the genetic variation within a single species",
       "Only the variety of ecosystems in a country"], "C"),
    "Meaning of biodiversity",
    "NCERT: biodiversity is the term popularised by Edward Wilson to describe the combined diversity at all the levels "
    "of biological organisation. The most important of these are genetic diversity, species diversity and ecological "
    "diversity.",
    ["Biodiversity = combined diversity at all levels of biological organisation",
     "Main levels: genetic, species, ecological"],
    C12_BD("biodiversity"),
    why="Species richness, genetic variation and ecosystem variety are each only one level of biodiversity.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "Besides finding that plots with more species showed less year-to-year variation in total biomass, David Tilman's "
    "outdoor-plot experiments showed that increased diversity contributed to:",
    P("Higher productivity", ["Lower productivity", "Greater invasion by alien species",
                              "More frequent pest outbreaks"], "B"),
    "Diversity and productivity",
    "Tilman's long-term ecosystem experiments with outdoor plots found that plots with more species showed less "
    "year-to-year variation in total biomass, and that increased diversity contributed to higher productivity.",
    ["More species → more stable biomass", "More species → higher productivity"],
    C12_BD("biodiversity: importance of species diversity to the ecosystem"),
    why="Tilman's results showed the opposite of lower productivity; NCERT links stable, species-rich communities with "
        "resistance to invasions and less variability in pest cycles.",
    seconds=25)

add(BDC, "In situ and ex situ conservation", "Basic", "direct",
    "Besides the Khasi and Jaintia Hills of Meghalaya, NCERT lists sacred groves in:",
    P("The Aravalli Hills of Rajasthan, the Western Ghat regions of Karnataka and Maharashtra, and the Sarguja, Chanda "
      "and Bastar areas of Madhya Pradesh",
      ["The Thar desert of Rajasthan and the Rann of Kutch in Gujarat",
       "The Sundarbans of West Bengal and the Andaman Islands",
       "The Deccan plateau of Telangana and the coastal plains of Odisha"], "D"),
    "Sacred groves in India",
    "In India, ecologically unique and biodiversity-rich regions are legally protected, and many cultures also set "
    "aside tracts of forest as sacred groves. NCERT: such sacred groves are found in the Khasi and Jaintia Hills in "
    "Meghalaya, the Aravalli Hills of Rajasthan, the Western Ghat regions of Karnataka and Maharashtra and the "
    "Sarguja, Chanda and Bastar areas of Madhya Pradesh.",
    ["Sacred grove regions: Khasi-Jaintia Hills, Aravalli Hills, Western Ghats (Karnataka, Maharashtra), "
     "Sarguja-Chanda-Bastar (MP)"],
    C12_BD("biodiversity conservation: in situ conservation"),
    why="None of the regions in the other options is listed by NCERT as a location of sacred groves.",
    seconds=30)

add(BDC, "In situ and ex situ conservation", "Intermediate", "assertion_reason",
    ar("In Meghalaya, the sacred groves are the last refuges for a large number of rare and threatened plants.",
       "The last twenty years alone have witnessed the disappearance of 27 species."),
    AR("B"),
    "Sacred groves; recent extinctions",
    "NCERT: in Meghalaya, the sacred groves are the last refuges for a large number of rare and threatened plants (A "
    "true). In discussing the loss of biodiversity, NCERT notes that the last twenty years alone have witnessed the "
    "disappearance of 27 species (R true). R is a general statement about recent extinctions and does not explain why "
    "the sacred groves of Meghalaya shelter rare plants (their total protection does).",
    ["A: true", "R: true", "R does not explain A"],
    C12_BD("biodiversity conservation: in situ conservation; loss of biodiversity"),
    seconds=30)

add(BDC, "In situ and ex situ conservation", "Intermediate", "direct",
    "Seeds of different genetic strains of commercially important plants can be kept for long periods in:",
    P("Seed banks", ["Sacred groves", "Biosphere reserves", "National parks"], "A"),
    "Seed banks as ex situ conservation",
    "Ex situ conservation now uses advanced techniques: gametes of threatened species can be cryopreserved, eggs "
    "fertilised in vitro and plants propagated by tissue culture. NCERT adds that seeds of different genetic strains "
    "of commercially important plants can be kept for long periods in seed banks.",
    ["Long-term storage of seeds of genetic strains: seed banks (ex situ)"],
    C12_BD("biodiversity conservation: ex situ conservation"),
    why="Sacred groves, biosphere reserves and national parks are in situ methods that protect living plants in their "
        "habitat; they do not store seeds.",
    seconds=20)

add(BDC, "Importance and loss", "Intermediate", "match_list",
    ml(("scientist", "contribution described in NCERT"),
       ["Edward Wilson", "Robert May", "Paul Ehrlich", "David Tilman"],
       ["'Rivet popper' hypothesis", "Long-term ecosystem experiments using outdoor plots",
        "Estimate of global species diversity at about 7 million", "Popularised the term 'biodiversity'"]),
    M({"A": "IV", "B": "III", "C": "I", "D": "II"},
      [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
       {"A": "I", "B": "III", "C": "IV", "D": "II"}], "D"),
    "Scientists in the study of biodiversity",
    "Edward Wilson popularised the term biodiversity; Robert May placed the global species diversity at about 7 "
    "million; Paul Ehrlich proposed the 'rivet popper' hypothesis comparing species to the rivets of an airplane; and "
    "David Tilman carried out long-term ecosystem experiments using outdoor plots.",
    ["Wilson: biodiversity", "May: 7 million", "Ehrlich: rivet popper", "Tilman: outdoor plots"],
    C12_BD("biodiversity; importance of species diversity to the ecosystem"),
    why="Option A swaps Ehrlich and Tilman; option B swaps Wilson and May; option C swaps Wilson and Ehrlich.",
    seconds=35)

add(BDC, "Patterns of biodiversity", "Intermediate", "statement_pair",
    sp("The diversity of plants and animals is not uniform throughout the world but shows a rather uneven "
       "distribution.",
       "In general, species diversity increases as we move away from the equator towards the poles."),
    SP("C"),
    "Global patterns of biodiversity",
    "NCERT: the diversity of plants and animals is not uniform throughout the world but shows a rather uneven "
    "distribution (Statement I true). The best-known pattern is the latitudinal gradient: species diversity decreases "
    "as we move away from the equator towards the poles, so Statement II is false.",
    ["Statement I: true", "Statement II: false, diversity decreases towards the poles"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    seconds=25)

add(BDC, "Patterns of biodiversity", "Intermediate", "assertion_reason",
    ar("When species richness is plotted against area on ordinary (linear) axes, the species-area relationship is a "
       "straight line.",
       "On a logarithmic scale, the species-area relationship is a straight line described by log S = log C + Z log A."),
    AR("D"),
    "Form of the species-area relationship",
    "Within a region, species richness increases with explored area, but only up to a limit; on linear axes the "
    "relation turns out to be a rectangular hyperbola, so A is false. On a logarithmic scale it is a straight line, "
    "log S = log C + Z log A, so R is true.",
    ["A: false, it is a rectangular hyperbola", "R: true"],
    C12_BD("patterns of biodiversity: species-area relationships"),
    seconds=30)

add(BDC, "In situ and ex situ conservation", "Advanced", "direct",
    "To save a threatened orchid, a state government plans to: (i) declare its forest habitat a national park; (ii) "
    "store its seeds in a seed bank; (iii) grow it in a botanical garden; (iv) propagate it by tissue culture. Which of "
    "these are means of ex situ conservation?",
    P("(ii), (iii) and (iv) only", ["(i) and (iii) only", "(i), (ii) and (iv) only", "(i), (ii), (iii) and (iv)"],
      "B"),
    "Classifying conservation measures",
    "In situ conservation protects species in their natural habitat (national parks, wildlife sanctuaries, biosphere "
    "reserves, sacred groves). Ex situ conservation takes threatened species out of their natural habitat into special "
    "settings: botanical gardens, zoological parks, wildlife safari parks, seed banks, cryopreservation, in vitro "
    "fertilisation and tissue culture. So (ii), (iii) and (iv) are ex situ; (i) is in situ.",
    ["(i) national park: in situ", "(ii) seed bank, (iii) botanical garden, (iv) tissue culture: ex situ"],
    C12_BD("biodiversity conservation: in situ and ex situ conservation"),
    why="Every other option includes the national park (in situ) or leaves out an ex situ measure.",
    seconds=40)

add(BDC, "Patterns of biodiversity", "Advanced", "statement_pair",
    sp("For frugivorous (fruit-eating) birds and mammals in the tropical forests of different continents, the slope Z "
       "of the species-area regression line is found to be 1.15.",
       "For areas within a region, the value of Z lies in the range 0.6 to 1.2."),
    SP("C"),
    "Values of Z in the species-area relationship",
    "NCERT: within a region, Z values are amazingly similar, in the range 0.1 to 0.2, regardless of the taxonomic group "
    "or the region, so Statement II is false. When very large areas such as entire continents are analysed, the slope "
    "is much steeper (0.6 to 1.2); for frugivorous birds and mammals in the tropical forests of different continents, "
    "it is 1.15 (Statement I true).",
    ["Statement I: true (1.15, continental scale)", "Statement II: false, within a region Z = 0.1 to 0.2"],
    C12_BD("patterns of biodiversity: species-area relationships"),
    seconds=35)

# log S2/S1 = Z log A2/A1 with A2/A1 = 1000 and S2/S1 = 100.
_bd_Z = math.log10(100) / math.log10(1000)
assert abs(_bd_Z - 2 / 3) < 1e-12 and 0.6 <= _bd_Z <= 1.2
assert abs(math.log10(1000) / math.log10(100) - 1.5) < 1e-12           # distractor: ratio inverted
assert abs(100 / 1000 - 0.1) < 1e-12                                   # distractor: S ratio / A ratio

add(BDC, "Patterns of biodiversity", "Advanced", "numerical",
    "Species richness and area follow log S = log C + Z log A. Two very large areas, one 1000 times larger than the "
    "other, are compared, and the larger area has 100 times as many species. What is Z, and how does it compare with "
    "the ranges given in NCERT?",
    P("Z ≈ 0.67, within the range found for very large areas such as entire continents",
      ["Z = 1.5, steeper than any range given in NCERT",
       "Z = 0.1, the value typical of areas within a region",
       "Z ≈ 0.67, the value typical of areas within a region"], "A"),
    "Calculating the slope Z",
    "Subtracting the equations for the two areas: log(S₂/S₁) = Z log(A₂/A₁). So log 100 = Z × log 1000, i.e. 2 = 3Z "
    "and Z = 2/3 ≈ 0.67. NCERT: Z is 0.1-0.2 for areas within a region but much steeper, 0.6-1.2, for very large areas "
    "such as entire continents; 0.67 falls in the second range.",
    ["log(S₂/S₁) = Z log(A₂/A₁)", "2 = Z × 3 → Z ≈ 0.67", "0.6 ≤ 0.67 ≤ 1.2: continental range"],
    C12_BD("patterns of biodiversity: species-area relationships"),
    why="1.5 inverts the logarithms (3/2); 0.1 divides the ratios themselves (100/1000) instead of their logarithms; "
        "0.67 is outside the within-region range of 0.1-0.2.",
    seconds=75, verified_by=RECOMPUTED)


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
    assert len(QUESTIONS) == pkg["count"] == 125, len(QUESTIONS)
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_005", "created_at": TODAY,
           "notes": "BATCH_005 package BOT_005_p2: 125 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 to "
                    "BATCH_004 were avoided. Numerical and other computable answers re-derived by "
                    "tools/batch_005/BOT_005_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()
