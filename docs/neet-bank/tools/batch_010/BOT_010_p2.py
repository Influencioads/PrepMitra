"""Builder for BATCH_010, package BOT_010_p2 (Botany, NEET_BOT_002376..NEET_BOT_002500, 125 questions).

Topics: Sexual Reproduction in Flowering Plants; Principles of Inheritance and Variation; Molecular Basis of
Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem; Biodiversity and Conservation. All
questions are original and every fact is taken from the rationalised NCERT Class 12 Biology textbook. Facts already
tested in BATCH_000 to BATCH_009 on these topics were avoided or approached from a new angle (see
`python tools/merge_batch.py stems 10 BOT_010_p2`). Computable answers are re-derived below; the file is written
only if every assert, the plan quota, the format mix and the answer-key balance pass.

    cd docs/neet-bank && python tools/batch_010/BOT_010_p2.py
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
PACKAGE = "BOT_010_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_010_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_010_BOT_p2.json"
FIRST_ID = 2376

AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

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


C12_SR = lambda s: ref(12, SRFP, s)  # noqa: E731
C12_PI = lambda s: ref(12, PIV, s)  # noqa: E731
C12_MB = lambda s: ref(12, MBI, s)  # noqa: E731
C12_MW = lambda s: ref(12, MHW, s)  # noqa: E731
C12_OP = lambda s: ref(12, OAP, s)  # noqa: E731
C12_EC = lambda s: ref(12, ECO, s)  # noqa: E731
C12_BD = lambda s: ref(12, BDC, s)  # noqa: E731


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
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")  # noqa: E731
    assert sorted(correct.values()) == sorted(["I", "II", "III", "IV"])
    for w in wrong:
        assert sorted(w.values()) == sorted(["I", "II", "III", "IV"]), w
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4, opts
    return opts, at


def mc(s):
    """'III,IV,I,II' -> {'A': 'III', 'B': 'IV', 'C': 'I', 'D': 'II'}"""
    return dict(zip("ABCD", s.split(",")))


def MS(correct, wrong, at):
    """Multi-statement options: each option is a set of statement letters; the correct set goes at `at`."""
    fmt = lambda s: (", ".join(f"({x})" for x in s[:-1]) + f" and ({s[-1]})" if len(s) > 1 else f"({s[0]})") + " only"  # noqa: E731
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
    if fmt in ("direct", "numerical", "match_list", "multi_statement"):
        assert why, (topic, text[:60])
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

# ================================================================ Sexual Reproduction in Flowering Plants (7 / 8 / 7)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "A typical angiosperm anther is a four-sided (tetragonal) structure in transverse section. In a transverse "
    "section, a typical microsporangium itself appears:",
    P("Near circular in outline", ["Tetragonal in outline", "Triangular in outline", "Long and rectangular in "
                                                                                     "outline"], "B"),
    "Shape of a microsporangium",
    "NCERT: in a transverse section, a typical microsporangium appears near circular in outline. It is generally "
    "surrounded by four wall layers — the epidermis, endothecium, middle layers and the tapetum. The anther as a "
    "whole is tetragonal, with a microsporangium at each corner.",
    ["Anther in T.S.: tetragonal", "Microsporangium in T.S.: near circular"],
    C12_SR("pre-fertilisation: structures and events — the stamen, microsporangium and pollen grain"),
    why="'Tetragonal' describes the whole anther in transverse section, not one microsporangium; NCERT does not "
        "describe the microsporangium as triangular or rectangular in section.",
    seconds=20)

add(SRFP, "Pollination", "Basic", "direct",
    "Pollen grains are shed from the anther and must reach the stigma of a pistil for fertilisation. NCERT terms "
    "this transfer of pollen grains to the stigma of a pistil:",
    P("Pollination", ["Fertilisation", "Syngamy", "Emasculation"], "D"),
    "Definition of pollination",
    "NCERT: in flowering plants, both the male and female gametes are non-motile, so they have to be brought "
    "together for fertilisation to occur. Pollination is the mechanism to achieve this objective: the transfer "
    "of pollen grains (shed from the anther) to the stigma of a pistil is termed pollination.",
    ["Anther → stigma transfer of pollen = pollination"],
    C12_SR("pre-fertilisation: structures and events — pollination"),
    why="Fertilisation and syngamy are fusions of gametes inside the embryo sac, which come after pollination; "
        "emasculation is the removal of anthers in artificial hybridisation.",
    seconds=20)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "Enclosed within the integuments of an ovule is a mass of cells that have abundant reserve food materials. "
    "This mass of cells is the:",
    P("Nucellus", ["Funicle", "Chalaza", "Hilum"], "A"),
    "Parts of the ovule",
    "NCERT: enclosed within the integuments is a mass of cells called the nucellus. Cells of the nucellus have "
    "abundant reserve food materials. Located in the nucellus is the embryo sac or female gametophyte.",
    ["Integuments enclose the nucellus", "Nucellus: food-rich cells; contains the embryo sac"],
    C12_SR("pre-fertilisation: structures and events — the pistil, megasporangium (ovule) and embryo sac"),
    why="The funicle is the stalk that attaches the ovule to the placenta; the hilum is the region where the "
        "ovule's body fuses with the funicle; the chalaza is the basal part of the ovule.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "statement_pair",
    sp("Much before the actual flower is seen on a plant, several hormonal and structural changes lead to the "
       "differentiation and further development of the floral primordium.",
       "In the majority of angiosperms, pollen grains are shed at the 3-celled stage."),
    SP("C"),
    "Floral development and the stage of pollen shedding",
    "NCERT: several hormonal and structural changes are initiated which lead to the differentiation and further "
    "development of the floral primordium; inflorescences then bear floral buds and flowers (Statement I true). "
    "In over 60 per cent of angiosperms, pollen grains are shed at the 2-celled stage; only in the remaining "
    "species is the generative cell divided into two male gametes before shedding (Statement II false).",
    ["Floral primordium develops before the flower appears", "Over 60% shed 2-celled pollen"],
    C12_SR("flower – a fascinating organ of angiosperms; pre-fertilisation: structures and events"),
    seconds=30)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "In a majority of flowering plants, only one of the four megaspores is functional and develops into the female "
    "gametophyte. This method of embryo sac formation from a single megaspore is termed:",
    P("Monosporic development", ["Bisporic development", "Tetrasporic development", "Free-nuclear development"],
      "C"),
    "Monosporic embryo sac",
    "NCERT: in a majority of flowering plants, one of the megaspores is functional while the other three "
    "degenerate. Only the functional megaspore develops into the female gametophyte (embryo sac). This method of "
    "embryo sac formation from a single megaspore is termed monosporic development.",
    ["One functional megaspore", "Embryo sac from a single megaspore = monosporic"],
    C12_SR("pre-fertilisation: structures and events — megasporogenesis and the female gametophyte"),
    why="Bi- and tetrasporic would involve two or four megaspores; 'free nuclear' describes the type of nuclear "
        "divisions inside the developing embryo sac, not the number of megaspores used.",
    seconds=20)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Basic", "assertion_reason",
    ar("Cleistogamous flowers produce assured seed set even in the absence of pollinators.",
       "Pollen grains are rich in nutrients."),
    AR("B"),
    "Cleistogamy versus pollen nutrition",
    "NCERT: cleistogamous flowers do not open at all; their anthers dehisce in the flower buds and the pollen "
    "comes in contact with the stigma, so they are invariably autogamous and produce assured seed set even "
    "without pollinators (A true). Pollen grains are rich in nutrients, which is why pollen tablets are used as "
    "food supplements (R true). R has nothing to do with why cleistogamous flowers set seed.",
    ["A: closed flowers → self-pollination → assured seed set", "R: true, but about pollen as food"],
    C12_SR("pre-fertilisation: pollination; pollen grain"),
    seconds=30)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "In pollen grains that are shed at the 3-celled stage, the generative cell has already given rise to the two "
    "male gametes. The generative cell forms them by:",
    P("Mitotic division", ["Meiotic division", "Fusion with the vegetative cell", "Budding from the vegetative "
                                                                                 "nucleus"], "A"),
    "Origin of the male gametes",
    "NCERT: the generative cell is small and floats in the cytoplasm of the vegetative cell. In over 60 per cent "
    "of angiosperms pollen is shed at the 2-celled stage; in the remaining species, the generative cell divides "
    "mitotically to give rise to the two male gametes before the pollen grains are shed (3-celled stage).",
    ["Pollen grain is already haploid", "Generative cell → 2 male gametes by mitosis"],
    C12_SR("pre-fertilisation: structures and events — pollen grain"),
    why="Meiosis took place earlier, in the pollen mother cell; the gametes do not form by fusion with the "
        "vegetative cell or by budding.",
    seconds=20)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "direct",
    "Which of the following gives the correct sequence of events in the formation of a typical (monosporic) embryo "
    "sac?",
    P("Meiosis of the megaspore mother cell → three of the four megaspores degenerate → nucleus of the functional "
      "megaspore divides to give a 2-nucleate embryo sac → two more free-nuclear divisions give 4- and then "
      "8-nucleate stages → cell walls are laid down, organising the 7-celled embryo sac",
      ["Meiosis of the megaspore mother cell → all four megaspores fuse → three free-nuclear divisions give the "
       "8-nucleate stage → cell walls are laid down, organising the 7-celled embryo sac",
       "Mitosis of the megaspore mother cell → three of the four megaspores degenerate → cell walls are laid down "
       "around each new nucleus after every division → 7-celled embryo sac",
       "Meiosis of the megaspore mother cell → three of the four megaspores degenerate → cell walls are laid down "
       "after the 4-nucleate stage → one more division gives the 7-celled embryo sac"], "D"),
    "Development of the female gametophyte",
    "NCERT: the MMC undergoes meiosis to give four megaspores; in most plants one is functional and three "
    "degenerate. The nucleus of the functional megaspore divides mitotically to form two nuclei that move to "
    "opposite poles (2-nucleate embryo sac). Two more sequential mitotic nuclear divisions give the 4-nucleate "
    "and then 8-nucleate stages. These divisions are strictly free nuclear; only after the 8-nucleate stage are "
    "cell walls laid down, giving the typical female gametophyte — 8-nucleate and 7-celled.",
    ["MMC → meiosis → 4 megaspores (3 degenerate)", "Functional megaspore: 2 → 4 → 8 nuclei (free nuclear)",
     "Then cell walls → 7 cells"],
    C12_SR("pre-fertilisation: megasporogenesis and the female gametophyte"),
    why="The megaspores do not fuse; the MMC divides by meiosis, not mitosis; and walls are laid down only after "
        "the 8-nucleate stage, since the divisions are strictly free nuclear.",
    seconds=60)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "direct",
    "Which of the following gives the correct sequence in the development of the male gametophyte in a species "
    "that sheds its pollen at the 2-celled stage?",
    P("Pollen mother cell undergoes meiosis → microspore tetrad → microspores dissociate as the anther dehydrates "
      "→ pollen grain with a vegetative and a generative cell is shed → generative cell divides in the pollen "
      "tube to form two male gametes",
      ["Pollen mother cell undergoes mitosis → microspore tetrad → pollen grain with a vegetative and a "
       "generative cell → generative cell divides by meiosis to form two male gametes",
       "Pollen mother cell undergoes meiosis → microspores dissociate → generative cell divides to form two male "
       "gametes → pollen grain is shed at the 3-celled stage",
       "Microspore tetrad → pollen mother cell undergoes meiosis → microspores dissociate → pollen grain is "
       "shed with two male gametes"], "B"),
    "Development of the male gametophyte",
    "NCERT: each pollen mother cell undergoes meiosis to form a microspore tetrad. As the anthers mature and "
    "dehydrate, the microspores dissociate and develop into pollen grains. A mature pollen grain contains a "
    "vegetative and a generative cell; in over 60 per cent of angiosperms it is shed at this 2-celled stage. In "
    "these plants, the generative cell divides to form the two male gametes during the growth of the pollen "
    "tube in the stigma.",
    ["PMC → meiosis → tetrad", "Dissociation → pollen grain (vegetative + generative)",
     "2-celled shedding → gametes formed in the pollen tube"],
    C12_SR("pre-fertilisation: microsporogenesis and pollen grain"),
    why="The PMC divides by meiosis and the generative cell by mitosis; a species that sheds 2-celled pollen does "
        "not form the male gametes before shedding; and the tetrad is the product, not the starting point, of "
        "the PMC's meiosis.",
    seconds=60)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "After compatible pollination, which of the following gives the correct path of the pollen tube up to the "
    "release of the male gametes?",
    P("Emerges through a germ pore → grows through the tissues of the stigma and style → reaches the ovary → "
      "enters the ovule through the micropyle → enters a synergid through the filiform apparatus and releases the "
      "male gametes",
      ["Emerges through a germ pore → grows through the style → enters the ovule through the chalaza → enters an "
       "antipodal cell and releases the male gametes",
       "Emerges through any point of the exine → grows through the ovary wall → enters the ovule through the "
       "micropyle → releases the male gametes directly into the central cell",
       "Emerges through a germ pore → grows through the stigma and style → enters the ovule through the "
       "micropyle → enters the egg cell through the filiform apparatus"], "C"),
    "Path of the pollen tube",
    "NCERT: following compatible pollination, the pollen grain germinates on the stigma to produce a pollen tube "
    "through one of the germ pores. The tube grows through the tissues of the stigma and style and reaches the "
    "ovary. Pollen tubes, after reaching the ovary, enter the ovule through the micropyle and then enter one of "
    "the synergids through the filiform apparatus; the filiform apparatus present at the micropylar part of the "
    "synergids guides the entry of the pollen tube. The male gametes are released into the cytoplasm of the "
    "synergid.",
    ["Germ pore → stigma → style → ovary", "Micropyle → synergid (filiform apparatus) → gametes released"],
    C12_SR("pre-fertilisation: pollen-pistil interaction; double fertilisation"),
    why="The tube enters the ovule through the micropyle, not the chalaza; it emerges through a germ pore, where "
        "sporopollenin is absent; and the filiform apparatus belongs to the synergids, not to the egg or the "
        "antipodals.",
    seconds=50)

add(SRFP, "Pollination", "Intermediate", "match_list",
    ml(("value given in NCERT", "what it refers to"),
       ["About 30 genera", "Over 60 per cent", "About 25–50 micrometres", "−196 °C"],
       ["Temperature of the liquid nitrogen in which pollen grains are stored in pollen banks",
        "Usual diameter of pollen grains",
        "Share of angiosperms whose pollen is shed at the 2-celled stage",
        "Number of genera, mostly monocotyledons, to which pollination by water is limited"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,II,III,I"), mc("IV,III,I,II")], "A"),
    "Numbers in NCERT's account of pollen and pollination",
    "NCERT: pollination by water is quite rare and limited to about 30 genera, mostly monocotyledons (A-IV); in "
    "over 60 per cent of angiosperms pollen is shed at the 2-celled stage (B-III); pollen grains are generally "
    "spherical, measuring about 25–50 micrometres in diameter (C-II); pollen of many species can be stored for "
    "years in liquid nitrogen at −196 °C (D-I).",
    ["30 genera → water pollination", "> 60% → 2-celled shedding", "25–50 µm → pollen size",
     "−196 °C → pollen banks"],
    C12_SR("pre-fertilisation: pollen grain; pollination"),
    why="The wrong codes interchange the two figures about pollen shedding and water pollination, the size and "
        "the shedding share, or the size and the storage temperature.",
    seconds=40)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "assertion_reason",
    ar("Pollen grains of rice and wheat lose their viability within 30 minutes of their release.",
       "The intine of a pollen grain is a thin and continuous layer made up of cellulose and pectin."),
    AR("B"),
    "Pollen viability versus pollen wall",
    "NCERT: the period for which pollen grains remain viable is highly variable; in rice and wheat they lose "
    "viability within 30 minutes of release, while in some members of Rosaceae, Leguminoseae and Solanaceae they "
    "remain viable for months (A true). The inner wall, the intine, is a thin and continuous layer made of "
    "cellulose and pectin (R true). NCERT links viability to the species and to temperature and humidity, not to "
    "the composition of the intine, so R does not explain A.",
    ["A: rice and wheat pollen viable < 30 min (true)", "R: intine of cellulose and pectin (true)",
     "Unrelated → option B"],
    C12_SR("pre-fertilisation: pollen grain"),
    seconds=30)

add(SRFP, "Pollination", "Intermediate", "direct",
    "In NCERT's activity to study pollen germination, pollen from flowers such as pea, chickpea, Crotalaria, "
    "balsam or Vinca is dusted on a drop of sugar solution on a glass slide. After about how long is the slide "
    "observed under the low power lens to see pollen tubes coming out of the pollen grains?",
    P("About 15–30 minutes", ["About 24 hours", "About 2–3 days", "About one week"], "D"),
    "Pollen germination in the laboratory",
    "NCERT: dust some pollen from flowers such as pea, chickpea, Crotalaria, balsam and Vinca on a glass slide "
    "containing a drop of sugar solution (about 10 per cent). After about 15–30 minutes, observe the slide under "
    "the low power lens of the microscope; you are likely to see pollen tubes coming out of the pollen grains.",
    ["10% sugar solution", "Observe after about 15–30 minutes"],
    C12_SR("pre-fertilisation: pollination — pollen-pistil interaction"),
    why="Pollen tubes appear within minutes in this activity; periods of a day or more are far longer than NCERT "
        "states (and the pollen of some species loses viability within 30 minutes).",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Intermediate", "statement_pair",
    sp("In a dicotyledonous embryo, the portion of the embryonal axis above the level of the cotyledons is the "
       "epicotyl, which terminates with the plumule or stem tip.",
       "In the embryo of a grass, the coleoptile is the undifferentiated sheath that encloses the radicle and the "
       "root cap."),
    SP("C"),
    "Parts of dicot and grass embryos",
    "NCERT: in a typical dicot embryo, the portion of the embryonal axis above the level of the cotyledons is the "
    "epicotyl, which terminates with the plumule or stem tip (Statement I true). In the grass embryo, the radicle "
    "and root cap are enclosed in an undifferentiated sheath called the coleorhiza; the coleoptile is a hollow "
    "foliar structure that encloses the shoot apex and a few leaf primordia (Statement II false).",
    ["Epicotyl → plumule", "Coleorhiza encloses radicle + root cap", "Coleoptile encloses shoot apex"],
    C12_SR("post-fertilisation: structures and events — embryo"),
    seconds=30)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("Water hyacinth and water lily are aquatic plants, yet they are not pollinated by water.",
       "In these plants, the flowers emerge above the level of water and are pollinated by insects or wind."),
    AR("A"),
    "Not all aquatic plants are water-pollinated",
    "NCERT: not all aquatic plants use water for pollination; in a majority of aquatic plants such as water "
    "hyacinth and water lily, the flowers emerge above the level of water and are pollinated by insects or wind "
    "as in most land plants. R gives the reason for A.",
    ["Flowers held above water", "So pollinated by insects or wind, not water"],
    C12_SR("pre-fertilisation: pollination — agents of pollination"),
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "multi_statement",
    ms("Which of the following statements about the micropylar and chalazal ends of the ovule and the embryo sac "
       "are correct?",
       ["The egg apparatus is situated at the micropylar end of the embryo sac.",
        "The three antipodal cells are situated at the chalazal end.",
        "The megaspore mother cell is differentiated in the micropylar region of the nucellus.",
        "The filiform apparatus is present at the micropylar tip of the synergids.",
        "The pollen tube enters the ovule through the chalaza."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "c", "d", "e"]], "B"),
    "Polarity of the ovule and embryo sac",
    "NCERT: ovules generally differentiate a single MMC in the micropylar region of the nucellus (c). In the "
    "mature embryo sac, three cells are grouped at the micropylar end to form the egg apparatus (a), and three "
    "cells at the chalazal end are the antipodals (b). The synergids have special cellular thickenings at the "
    "micropylar tip, the filiform apparatus (d). The pollen tube enters the ovule through the micropyle, not the "
    "chalaza (e false).",
    ["Micropylar end: MMC, egg apparatus, filiform apparatus, pollen-tube entry", "Chalazal end: antipodals"],
    C12_SR("pre-fertilisation: megasporogenesis and the female gametophyte; double fertilisation"),
    why="(e) is false, so every option with it is wrong; '(a), (c) and (d) only' leaves out the chalazal "
        "position of the antipodals (b).",
    seconds=50)

add(SRFP, "Endosperm and embryo", "Advanced", "match_list",
    ml(("seed named in NCERT", "where the food reserve of the mature seed lies"),
       ["Pea", "Castor", "Beet", "Coconut"],
       ["Endosperm that is partly free-nuclear (liquid) and partly cellular",
        "A persistent remnant of the nucellus (perisperm)",
        "A part of the endosperm that persists in the mature seed",
        "Thick, swollen cotyledons, the endosperm having been completely consumed"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,II,III,I"), mc("IV,III,I,II")], "D"),
    "Food reserves of mature seeds",
    "NCERT: in pea, groundnut and beans the endosperm is completely consumed by the developing embryo before seed "
    "maturation (non-albuminous seeds), and the cotyledons are thick and swollen with stored food (A-IV). Castor, "
    "like wheat, maize and barley, retains a part of the endosperm that is not completely used up during embryo "
    "development (albuminous seed) (B-III). In some seeds such as black pepper and beet, remnants of the nucellus "
    "persist; this residual, persistent nucellus is the perisperm (C-II). In coconut, the coconut water is "
    "free-nuclear endosperm made up of thousands of nuclei and the surrounding white kernel is cellular endosperm "
    "(D-I).",
    ["Pea: non-albuminous, food in cotyledons", "Castor: albuminous", "Beet: perisperm",
     "Coconut: free-nuclear + cellular endosperm"],
    C12_SR("post-fertilisation: structures and events — endosperm; seed"),
    why="The wrong codes interchange the non-albuminous pea with albuminous castor, the castor endosperm with the "
        "beet perisperm, or the beet perisperm with the coconut endosperm.",
    seconds=50)
add(SRFP, "Pollination", "Advanced", "assertion_reason",
    ar("Geitonogamy is functionally cross-pollination, since it involves a pollinating agent.",
       "In geitonogamy, pollen grains are transferred to the stigma of a flower borne on a different plant."),
    AR("C"),
    "Geitonogamy: functional versus genetic",
    "NCERT: geitonogamy is the transfer of pollen grains from the anther to the stigma of another flower of the "
    "SAME plant. Although it is functionally cross-pollination involving a pollinating agent (A true), it is "
    "genetically similar to autogamy, since the pollen grains come from the same plant. Transfer to a flower of a "
    "different plant is xenogamy, so R is false.",
    ["Geitonogamy: another flower, same plant", "Functionally cross-, genetically self-pollination",
     "Different plant = xenogamy"],
    C12_SR("pre-fertilisation: pollination — kinds of pollination"),
    seconds=35)

add(SRFP, "Microsporogenesis and male gametophyte", "Advanced", "assertion_reason",
    ar("In a two-celled pollen grain, the generative cell is the larger of the two cells and has abundant food "
       "reserve.",
       "The generative cell is small and spindle-shaped, with dense cytoplasm and a nucleus, and it floats in the "
       "cytoplasm of the vegetative cell."),
    AR("D"),
    "Vegetative and generative cells",
    "NCERT: the vegetative cell is bigger, has abundant food reserve and a large irregularly shaped nucleus; the "
    "generative cell is small and floats in the cytoplasm of the vegetative cell, and it is spindle-shaped with "
    "dense cytoplasm and a nucleus. A attributes the vegetative cell's features to the generative cell (false); "
    "R is NCERT's description of the generative cell (true).",
    ["Vegetative cell: big, food reserve, irregular nucleus", "Generative cell: small, spindle-shaped, floats"],
    C12_SR("pre-fertilisation: pollen grain"),
    seconds=30)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "statement_pair",
    sp("The two male gametes of a pollen grain are genetically identical, since both arise by mitosis from a "
       "single generative cell.",
       "The four megaspores formed from one megaspore mother cell are genetically identical to one another, "
       "since all four come from a single cell."),
    SP("C"),
    "Mitotic versus meiotic products",
    "NCERT: the generative cell divides mitotically to give rise to the two male gametes, so they carry the same "
    "genetic information (Statement I true). The megaspore mother cell, however, undergoes MEIOSIS to produce "
    "four megaspores; meiosis separates homologous chromosomes (and their alleles), so the four megaspores of a "
    "heterozygous plant are not all genetically identical (Statement II false). Coming from a single cell does "
    "not make the products identical when the division is meiotic.",
    ["Male gametes: mitosis of one cell → identical", "Megaspores: meiosis → not identical"],
    C12_SR("pre-fertilisation: pollen grain; megasporogenesis"),
    seconds=40)

add(SRFP, "Endosperm and embryo", "Advanced", "direct",
    "NCERT describes two developmental processes in the ovule in which nuclear divisions are not immediately "
    "followed by cell wall formation (free-nuclear divisions). These two processes are:",
    P("Development of the embryo sac from the functional megaspore, and the most common type of endosperm "
      "development",
      ["Meiosis of the megaspore mother cell, and the development of the embryo from the zygote",
       "Development of the embryo from the zygote, and the formation of the seed coat from the integuments",
       "Formation of the microspore tetrad, and the development of the embryo sac from the functional "
       "megaspore"], "A"),
    "Free-nuclear divisions in the ovule",
    "NCERT: the nucleus of the functional megaspore divides mitotically, and two more sequential divisions give "
    "the 8-nucleate stage; these divisions are strictly free nuclear, i.e. not followed immediately by cell wall "
    "formation. In the most common type of endosperm development, the primary endosperm nucleus undergoes "
    "successive nuclear divisions to give free nuclei; cell wall formation follows later and the endosperm "
    "becomes cellular.",
    ["Embryo sac: 2 → 4 → 8 free nuclei, then walls", "Endosperm (common type): free nuclei, then cellular"],
    C12_SR("pre-fertilisation: female gametophyte; post-fertilisation: endosperm"),
    why="NCERT does not describe the embryo, the seed coat or the meiosis of spore mother cells as free nuclear; "
        "the microspore tetrad forms in the anther, not in the ovule.",
    seconds=45)

_total, _sporangia = 2560, 4
_pmc = _total // _sporangia // 4
assert _pmc == 160 and _pmc * 4 * _sporangia == _total
assert _total // _sporangia == 640 and _total // 2 // 4 == 320 and _total // 4 // 4 // 4 == 40

add(SRFP, "Microsporogenesis and male gametophyte", "Advanced", "numerical",
    "A typical angiosperm anther (bilobed, each lobe dithecous) releases 2560 pollen grains in all, and its "
    "microsporangia contain equal numbers of pollen mother cells. If every pollen mother cell completed "
    "microsporogenesis normally and every microspore became a pollen grain, how many pollen mother cells were "
    "present in each microsporangium?",
    P("160", ["640", "320", "40"], "B"),
    "From pollen grains back to pollen mother cells",
    "A bilobed anther with dithecous lobes has 2 × 2 = 4 microsporangia, so each microsporangium yields 2560/4 = "
    "640 pollen grains. Each pollen mother cell gives a tetrad of four microspores, i.e. four pollen grains, so "
    "each microsporangium had 640/4 = 160 pollen mother cells.",
    ["Microsporangia = 2 lobes × 2 theca = 4", "Per microsporangium: 2560/4 = 640 pollen grains",
     "PMCs = 640/4 = 160"],
    C12_SR("pre-fertilisation: the stamen, microsporangium and pollen grain; microsporogenesis"),
    why="640 is the number of pollen grains per microsporangium (the tetrad step is skipped); 320 counts only two "
        "microsporangia per anther; 40 divides by four once too often.",
    seconds=60, verified_by=RECOMPUTED)

# ================================================================ Principles of Inheritance and Variation (8 / 9 / 8)


def cross(p1, p2):
    """Offspring genotype distribution for independent genes; genotypes as strings like 'AaBb'."""
    g1 = [p1[i:i + 2] for i in range(0, len(p1), 2)]
    g2 = [p2[i:i + 2] for i in range(0, len(p2), 2)]
    out = Counter()
    for a in product(*g1):
        for b in product(*g2):
            out["".join("".join(sorted(x + y)) for x, y in zip(a, b))] += 1
    tot = sum(out.values())
    return {k: F(v, tot) for k, v in out.items()}


add(PIV, "Mendelian inheritance", "Basic", "direct",
    "NCERT represents the gametes of a Tt pea plant as carrying T or t, each with a chance of 1/2. The genotypes "
    "of the F2 (Tt × Tt) are then obtained from the binomial expression:",
    P("(1/2 T + 1/2 t)² = 1/4 TT + 1/2 Tt + 1/4 tt",
      ["(1/2 T + 1/2 t)² = 1/2 TT + 1/2 tt", "(1/2 T + 1/2 t)² = 3/4 TT + 1/4 tt",
       "(1/2 T + 1/2 t)² = 1/4 TT + 1/4 Tt + 1/2 tt"], "A"),
    "Binomial representation of a monohybrid cross",
    "NCERT: the gametes of a Tt plant carry T or t with equal (1/2) chance. Random fusion of gametes is shown by "
    "(1/2 T + 1/2 t)(1/2 T + 1/2 t) = (1/2 T + 1/2 t)² = 1/4 TT + 1/2 Tt + 1/4 tt, the same 1 : 2 : 1 genotypic "
    "ratio obtained from the Punnett square.",
    ["(a + b)² = a² + 2ab + b²", "a = b = 1/2 → 1/4 TT + 2(1/4) Tt + 1/4 tt"],
    C12_PI("inheritance of one gene: law of segregation"),
    why="1/2 TT + 1/2 tt and 3/4 TT + 1/4 tt drop the 2ab (Tt) term; 1/4 TT + 1/4 Tt + 1/2 tt misplaces the "
        "coefficients of the expansion.",
    seconds=25)

add(PIV, "Incomplete and co-dominance", "Basic", "direct",
    "NCERT's example of incomplete dominance is the inheritance of flower colour in the dog flower (snapdragon). "
    "The dog flower belongs to the genus:",
    P("Antirrhinum", ["Pisum", "Mirabilis", "Rauwolfia"], "C"),
    "NCERT's example of incomplete dominance",
    "NCERT: the inheritance of flower colour in the dog flower (snapdragon or Antirrhinum sp.) is a good example "
    "to understand incomplete dominance: RR (red) × rr (white) gives pink (Rr) F1 plants.",
    ["Dog flower = snapdragon = Antirrhinum sp."],
    C12_PI("inheritance of one gene: incomplete dominance"),
    why="Pisum is the garden pea used by Mendel; Rauwolfia is NCERT's example of genetic diversity (reserpine); "
        "Mirabilis is not the snapdragon.",
    seconds=20)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "NCERT describes phenylketonuria, in which the affected individual lacks an enzyme that converts "
    "phenylalanine into tyrosine, as:",
    P("An inborn error of metabolism, inherited as an autosomal recessive trait",
      ["A chromosomal disorder caused by trisomy of chromosome 21",
       "A sex-linked dominant disorder carried on the Y chromosome",
       "A disorder caused by an increase in a whole set of chromosomes"], "D"),
    "Phenylketonuria",
    "NCERT: phenylketonuria is an inborn error of metabolism that is also inherited as an autosomal recessive "
    "trait. The affected individual lacks an enzyme that converts the amino acid phenylalanine into tyrosine; "
    "phenylalanine accumulates and is converted into phenylpyruvic acid and other derivatives.",
    ["Single-gene (Mendelian) disorder", "Inborn error of metabolism, autosomal recessive"],
    C12_PI("genetic disorders: Mendelian disorders"),
    why="Trisomy of chromosome 21 is Down's syndrome; PKU is not sex-linked; an increase in a whole set of "
        "chromosomes is polyploidy.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Mendel published his work in 1865, but it remained unrecognised till 1900. Which of the following does "
    "NCERT give as one of the reasons?",
    P("Communication was not easy in those days, and his work could not be widely publicised",
      ["His experiments were based on too small a sample of plants",
       "His results were contradicted by Morgan's experiments on Drosophila",
       "He studied characters that did not show contrasting traits"], "B"),
    "Why Mendel's work was ignored",
    "NCERT gives several reasons: communication was not easy (as it is now) in those days and his work could not "
    "be widely publicised; his concept of factors as stable and discrete units was not accepted as an "
    "explanation for the apparently continuous variation seen in nature; the use of mathematics to explain "
    "biological phenomena was new and unacceptable to many biologists; and he could not provide any physical "
    "proof for the existence of factors.",
    ["Poor communication", "Discrete factors vs continuous variation", "Mathematics new to biology",
     "No physical proof of factors"],
    C12_PI("inheritance of two genes: chromosomal theory of inheritance"),
    why="NCERT credits Mendel with a large sampling size and with characters showing contrasting traits; "
        "Morgan's work came decades later and supported, not contradicted, Mendelian inheritance.",
    seconds=25)

_f2 = cross("Rr", "Rr")
assert _f2["Rr"] == F(1, 2) and 400 * _f2["Rr"] == 200 and 400 * _f2["RR"] == 100

add(PIV, "Incomplete and co-dominance", "Basic", "numerical",
    "In snapdragon, red-flowered (RR) and white-flowered (rr) plants give pink-flowered F1 plants. The F1 plants "
    "are self-pollinated and 400 F2 plants are raised. How many of these are expected to have pink flowers?",
    P("200", ["100", "300", "400"], "C"),
    "F2 of incomplete dominance",
    "Rr × Rr gives 1/4 RR (red) : 1/2 Rr (pink) : 1/4 rr (white). Pink = 1/2 × 400 = 200.",
    ["F2: 1 RR : 2 Rr : 1 rr", "Pink = Rr = 1/2", "1/2 × 400 = 200"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    why="100 is the number of red (or white) plants; 300 treats pink as a dominant phenotype (3/4); 400 assumes "
        "the F2 stays uniform like the F1.",
    seconds=25, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Basic", "assertion_reason",
    ar("Haemophilia is transmitted from an unaffected carrier female to some of the male progeny.",
       "In haemophilia, a single protein that is a part of the cascade of proteins involved in the clotting of "
       "blood is affected."),
    AR("B"),
    "Haemophilia: pattern of transmission versus molecular defect",
    "NCERT: haemophilia is a sex-linked recessive disease that shows its transmission from an unaffected carrier "
    "female to some of the male progeny (A true). In this disease a single protein of the clotting cascade is "
    "affected, so a simple cut results in non-stop bleeding (R true). R explains the symptom, not the pattern of "
    "transmission, which follows from the gene being on the X chromosome.",
    ["A: carrier mother → affected sons (X-linkage)", "R: the defective clotting protein", "R does not explain A"],
    C12_PI("genetic disorders: Mendelian disorders — haemophilia"),
    seconds=30)

add(PIV, "Incomplete and co-dominance", "Basic", "match_list",
    ml(("genotype", "phenotype"),
       ["Rr in snapdragon", "IᴬIᴮ", "Iᴬi", "ii"],
       ["Blood group O", "Pink flowers", "Blood group A", "Blood group AB"]),
    M(mc("II,IV,III,I"), [mc("II,III,IV,I"), mc("IV,II,III,I"), mc("II,IV,I,III")], "D"),
    "Genotype to phenotype under different dominance relations",
    "Snapdragon Rr is pink (incomplete dominance) (A-II). Iᴬ and Iᴮ are co-dominant, so IᴬIᴮ is blood group AB "
    "(B-IV). Iᴬ is dominant over i, so Iᴬi is blood group A (C-III). i produces no sugar, so ii is blood group O "
    "(D-I).",
    ["Rr → pink", "IᴬIᴮ → AB", "Iᴬi → A", "ii → O"],
    C12_PI("inheritance of one gene: incomplete dominance; co-dominance"),
    why="The wrong codes give IᴬIᴮ blood group A and Iᴬi blood group AB, make Rr blood group AB, or interchange "
        "the A and O groups.",
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "In sickle-cell anaemia, the mutant haemoglobin molecule undergoes polymerisation, which changes the shape of "
    "the RBC from a biconcave disc to an elongated sickle-like structure. According to NCERT, this happens under:",
    P("Low oxygen tension", ["High oxygen tension", "High body temperature", "Exposure to UV radiation"], "A"),
    "Sickling of RBCs",
    "NCERT: the mutant haemoglobin molecule undergoes polymerisation under low oxygen tension, causing the change "
    "in the shape of the RBC from biconcave disc to elongated sickle-like structure.",
    ["Hbˢ polymerises at low O₂ tension", "RBC becomes sickle-shaped"],
    C12_PI("genetic disorders: Mendelian disorders — sickle-cell anaemia"),
    why="NCERT links sickling to low, not high, oxygen tension; it does not attribute sickling to body "
        "temperature or to UV light.",
    seconds=20)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "assertion_reason",
    ar("Loss (deletion) or gain (insertion or duplication) of a segment of DNA results in alteration in "
       "chromosomes.",
       "The DNA helix runs continuously from one end to the other in each chromatid, in a highly supercoiled "
       "form."),
    AR("A"),
    "Why DNA changes alter chromosomes",
    "NCERT (mutation): since the DNA helix runs continuously from one end to the other in each chromatid, in a "
    "highly supercoiled form, loss (deletion) or gain (insertion/duplication) of a segment of DNA results in "
    "alteration in chromosomes. R is the reason NCERT gives for A.",
    ["A chromatid = one continuous supercoiled DNA helix", "So changing a DNA segment changes the chromosome"],
    C12_PI("mutation"),
    seconds=30)

_p = cross("RrYy", "RrYy")
_one = sum(v for k, v in _p.items() if (k[0] != k[1]) != (k[2] != k[3]))
_both = sum(v for k, v in _p.items() if k[0] != k[1] and k[2] != k[3])
assert _one == F(1, 2) and 1600 * _one == 800 and 1600 * _both == 400 and 1600 * (_one + _both) == 1200

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "A pea plant heterozygous for seed shape and seed colour (RrYy; the two genes assort independently) is "
    "self-pollinated, and 1600 seeds are obtained. How many seeds are expected to be heterozygous for exactly one "
    "of the two genes?",
    P("800", ["400", "1200", "200"], "D"),
    "Genotype classes in a dihybrid F2",
    "For each gene, Rr × Rr gives 1/2 heterozygous and 1/2 homozygous (likewise for Y). Exactly one heterozygous "
    "= P(Rr)·P(YY or yy) + P(RR or rr)·P(Yy) = 1/2·1/2 + 1/2·1/2 = 1/2. Expected = 1/2 × 1600 = 800.",
    ["P(het) = 1/2 per gene", "Exactly one: 2 × (1/2 × 1/2) = 1/2", "1/2 × 1600 = 800"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    shortcut="Exactly one of two independent 1/2 events: 2 × 1/4 = 1/2.",
    why="400 counts seeds heterozygous for both genes (1/4); 1200 counts seeds heterozygous for at least one gene "
        "(3/4); 200 counts only one of the two ways (e.g. Rr with homozygous Y) and halves it again.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Incomplete and co-dominance", "Intermediate", "match_list",
    ml(("cross", "ratio expected among the progeny"),
       ["Rr × Rr in snapdragon (flower colours)", "Iᴬi × Iᴮi (blood groups)", "Tt × Tt in pea (phenotypes)",
        "Tt × tt in pea (phenotypes)"],
       ["3 : 1", "1 : 1 : 1 : 1", "1 : 1", "1 : 2 : 1"]),
    M(mc("IV,II,I,III"), [mc("I,II,IV,III"), mc("IV,I,II,III"), mc("IV,II,III,I")], "B"),
    "Ratios under different dominance relations",
    "Snapdragon Rr × Rr: red : pink : white = 1 : 2 : 1 (A-IV). Iᴬi × Iᴮi: IᴬIᴮ (AB), Iᴬi (A), Iᴮi (B) and ii (O) "
    "each 1/4, i.e. 1 : 1 : 1 : 1 (B-II). Pea Tt × Tt with complete dominance: tall : dwarf = 3 : 1 (C-I). "
    "Tt × tt (test cross): tall : dwarf = 1 : 1 (D-III).",
    ["Incomplete dominance F2 → 1:2:1", "Iᴬi × Iᴮi → four groups equally", "Monohybrid F2 → 3:1",
     "Test cross → 1:1"],
    C12_PI("inheritance of one gene"),
    why="The wrong codes give the snapdragon F2 the 3 : 1 ratio of complete dominance, give the blood-group cross "
        "3 : 1, or interchange the monohybrid F2 and the test cross.",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "assertion_reason",
    ar("Individuals with Down's syndrome have 47 chromosomes in their somatic cells.",
       "Down's syndrome results from polyploidy, an increase in a whole set of chromosomes."),
    AR("C"),
    "Aneuploidy versus polyploidy",
    "NCERT: Down's syndrome is caused by the presence of an additional copy of chromosome 21 (trisomy of 21), so "
    "the cells have 46 + 1 = 47 chromosomes (A true). This gain of a single chromosome is aneuploidy, which "
    "results from failure of segregation of chromatids; polyploidy (an increase in a whole set of chromosomes, "
    "from failure of cytokinesis) is often seen in plants. R is false.",
    ["Trisomy 21 → 47 chromosomes", "One extra chromosome = aneuploidy, not polyploidy"],
    C12_PI("genetic disorders: chromosomal disorders"),
    seconds=30)

add(PIV, "Incomplete and co-dominance", "Intermediate", "assertion_reason",
    ar("A cross between a pink-flowered and a red-flowered snapdragon gives no white-flowered offspring.",
       "Every offspring of this cross receives an R allele from the red-flowered (RR) parent."),
    AR("A"),
    "Predicting a cross under incomplete dominance",
    "Red is RR and pink is Rr. Every gamete of the red parent carries R, so every offspring is RR (red) or Rr "
    "(pink), in a 1 : 1 ratio. A white flower needs rr, which requires r from both parents; because each "
    "offspring gets R from the red parent, rr cannot arise. R therefore explains A.",
    ["Red = RR → gametes all R", "Offspring RR or Rr → red or pink", "No rr → no white"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    seconds=35, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "multi_statement",
    ms("For which of the following can the genotype be stated with certainty from the phenotype alone?",
       ["A person with blood group AB", "A person with blood group O", "A person with blood group A",
        "A pink-flowered snapdragon", "A tall pea plant"]),
    MS(["a", "b", "d"], [["a", "b", "c", "d"], ["a", "d", "e"], ["b", "c", "e"]], "B"),
    "When phenotype reveals genotype",
    "Blood group AB arises only from IᴬIᴮ (co-dominance) (a), and blood group O only from ii (b). A pink "
    "snapdragon must be Rr, since under incomplete dominance the heterozygote has its own phenotype (d). Blood "
    "group A may be IᴬIᴬ or Iᴬi (c), and a tall pea plant may be TT or Tt (e) — which is why a test cross is "
    "needed to find the genotype of a plant with the dominant phenotype.",
    ["AB → IᴬIᴮ only", "O → ii only", "Pink → Rr only", "A → IᴬIᴬ or Iᴬi; tall → TT or Tt"],
    C12_PI("inheritance of one gene: co-dominance; incomplete dominance; test cross"),
    why="Blood group A (c) and tall (e) each correspond to two genotypes, so options containing them are wrong; "
        "'(a), (d) and (e)' also omits blood group O.",
    seconds=45)

_ways = sum(1 for kids in product("MF", repeat=4) if kids.count("M") == 2)
assert F(_ways, 16) == F(3, 8)

add(PIV, "Sex determination", "Intermediate", "numerical",
    "In humans, each pregnancy has an equal (50 per cent) chance of producing a male or a female child. A couple "
    "has four children. What is the probability that exactly two of them are sons and two are daughters, in any "
    "order of birth?",
    P("3/8", ["1/2", "1/16", "1/4"], "C"),
    "Probability of a mix of sons and daughters",
    "NCERT: in each pregnancy there is always a 50 per cent probability of a male or a female child. For four "
    "children there are 2⁴ = 16 equally likely birth orders. The number of orders with exactly two sons is "
    "4C2 = 6, so the probability is 6/16 = 3/8.",
    ["16 equally likely orders", "Orders with 2 sons = 4C2 = 6", "6/16 = 3/8"],
    C12_PI("sex determination: sex determination in humans"),
    why="1/2 assumes 'half sons' is the most likely outcome with probability 1/2; 1/16 counts only one particular "
        "order; 1/4 has no basis in the count of orders.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "Among the seven pairs of contrasting traits of garden pea studied by Mendel, in how many characters is the "
    "DOMINANT trait a colour?",
    P("Three", ["One", "Two", "Four"], "D"),
    "Mendel's seven characters",
    "NCERT's table: stem height (tall/dwarf), flower colour (violet/white), flower position (axial/terminal), pod "
    "shape (inflated/constricted), pod colour (green/yellow), seed shape (round/wrinkled) and seed colour "
    "(yellow/green). The dominant trait is a colour for flower colour (violet), pod colour (green) and seed "
    "colour (yellow): three characters.",
    ["Colour characters: flower, pod, seed", "Dominant: violet, green, yellow → 3"],
    C12_PI("Mendel's laws of inheritance (contrasting traits studied by Mendel in pea)"),
    why="Height, flower position, pod shape and seed shape have non-colour dominant traits (tall, axial, "
        "inflated, round), so the count is neither one, two nor four.",
    seconds=40)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "statement_pair",
    sp("Klinefelter's syndrome is caused by the absence of one of the X chromosomes.",
       "Turner's syndrome is caused by the absence of one of the X chromosomes, i.e. 45 with X0."),
    SP("D"),
    "Klinefelter's and Turner's syndromes",
    "NCERT: Klinefelter's syndrome is caused by the presence of an additional copy of the X chromosome, resulting "
    "in the karyotype 47, XXY (Statement I false). Turner's syndrome is caused by the absence of one of the X "
    "chromosomes, i.e. 45 with X0; such females are sterile (Statement II true).",
    ["Klinefelter: extra X (XXY, 47)", "Turner: missing X (X0, 45)"],
    C12_PI("genetic disorders: chromosomal disorders"),
    seconds=30)

# skin-colour model: offspring of AaBbCc x AABBcc; count dominant alleles
_dist = Counter()
for g in product("Aa", "Bb", "Cc"):
    _dist[sum(ch.isupper() for ch in g) + 2] += 1
assert F(_dist[4], 8) == F(3, 8)
_naive = Counter(sum(ch.isupper() for ch in g) for g in product("Aa", "Bb", "Cc", "Aa", "Bb", "Cc"))
assert F(_naive[4], 64) == F(15, 64) and F(_dist[5], 8) == F(1, 8)

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "Take NCERT's model of human skin colour controlled by three genes A, B and C, in which every dominant allele "
    "adds equally to the colour. A person of genotype AaBbCc marries a person of genotype AABBcc. What fraction of "
    "their children are expected to carry exactly four dominant alleles?",
    P("3/8", ["15/64", "1/8", "1/4"], "A"),
    "Additive alleles with one parent of fixed contribution",
    "Every gamete of the AABBcc parent is ABc, carrying two dominant alleles. The AaBbCc parent passes 0–3 "
    "dominant alleles, each gene independently with probability 1/2, giving 1/8, 3/8, 3/8, 1/8 for 0, 1, 2, 3. A "
    "child with four dominant alleles needs exactly two from the AaBbCc parent: probability 3C2/8 = 3/8.",
    ["AABBcc gametes: ABc → 2 dominant", "Need 2 more from AaBbCc", "P(2 of 3) = 3/8"],
    C12_PI("polygenic inheritance"),
    why="15/64 is the answer for AaBbCc × AaBbCc; 1/8 is the chance of three dominant alleles from the "
        "heterozygous parent (five in all); 1/4 does not follow from the binomial distribution.",
    seconds=90, verified_by=RECOMPUTED)

_cb_son = F(1, 2) * F(1, 2)
_car_dau = F(1, 2) * F(1, 2)
assert 2 * _cb_son * _car_dau == F(1, 8)

add(PIV, "Sex-linked inheritance", "Advanced", "numerical",
    "A woman with normal vision who is a carrier of red-green colour blindness marries a man with normal colour "
    "vision. They have two children. What is the probability that one of them is a colour-blind son and the other "
    "is a carrier daughter, in either order of birth?",
    P("1/8", ["1/16", "1/4", "1/2"], "B"),
    "X-linked inheritance over two children",
    "For each child: P(son) = 1/2 and a son is colour blind if he gets the mother's affected X (1/2), so "
    "P(colour-blind son) = 1/4. P(daughter) = 1/2, and every daughter gets the father's normal X; she is a carrier "
    "if she gets the mother's affected X (1/2), so P(carrier daughter) = 1/4. Two orders are possible: 2 × "
    "(1/4 × 1/4) = 1/8.",
    ["P(colour-blind son) = 1/4", "P(carrier daughter) = 1/4", "Either order: 2 × 1/16 = 1/8"],
    C12_PI("genetic disorders: Mendelian disorders — colour blindness"),
    why="1/16 takes only one birth order; 1/4 is the probability for a single child of one type; 1/2 is the chance "
        "that a son is colour blind, not the combined probability.",
    seconds=90, verified_by=RECOMPUTED)

_2n = 14
assert (_2n + 1, _2n - 1, 3 * _2n // 2, 2 * _2n) == (15, 13, 21, 28)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "match_list",
    ml(("change in a plant whose normal somatic cells have 2n = 14", "chromosome number of the resulting somatic "
                                                                     "cells"),
       ["Gain of one chromosome (aneuploidy)", "Loss of one chromosome (aneuploidy)",
        "Increase by one whole set, to three sets (polyploidy)", "Increase by two whole sets, to four sets "
                                                                 "(polyploidy)"],
       ["28", "13", "21", "15"]),
    M(mc("IV,II,III,I"), [mc("II,IV,III,I"), mc("IV,II,I,III"), mc("IV,III,II,I")], "C"),
    "Counting chromosomes in aneuploids and polyploids",
    "NCERT: failure of segregation of chromatids gives the gain or loss of a chromosome(s) (aneuploidy); failure "
    "of cytokinesis after telophase gives an increase in a whole set of chromosomes (polyploidy), often seen in "
    "plants. With 2n = 14, one set (n) = 7: 14 + 1 = 15 (A-IV), 14 − 1 = 13 (B-II), three sets = 21 (C-III) and "
    "four sets = 28 (D-I).",
    ["n = 7", "Aneuploidy: 14 ± 1 → 15, 13", "Polyploidy: 3n = 21, 4n = 28"],
    C12_PI("mutation; genetic disorders: chromosomal disorders"),
    why="The wrong codes swap gain with loss of a chromosome, three sets with four sets, or confuse 13 with 21.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "assertion_reason",
    ar("A man with blood group AB and a woman with blood group O can have children with blood group A or B only.",
       "The allele Iᴬ is completely dominant over the allele Iᴮ."),
    AR("C"),
    "Co-dominance of Iᴬ and Iᴮ",
    "The man (IᴬIᴮ) gives Iᴬ or Iᴮ and the woman (ii) gives i, so the children are Iᴬi (A) or Iᴮi (B) in equal "
    "numbers; groups AB and O cannot occur (A true). NCERT: Iᴬ and Iᴮ are co-dominant — when present together, "
    "both express their own type of sugar, giving AB. Neither is dominant over the other, so R is false.",
    ["IᴬIᴮ × ii → Iᴬi or Iᴮi", "Iᴬ and Iᴮ: co-dominant, both dominant over i"],
    C12_PI("inheritance of one gene: co-dominance"),
    seconds=40, verified_by=RECOMPUTED)

add(PIV, "Mendelian inheritance", "Advanced", "statement_pair",
    sp("In the F2 of Mendel's dihybrid cross (RRYY × rryy, F1 self-pollinated), round and wrinkled seeds occur in "
       "the ratio 3 : 1, just as in a monohybrid cross.",
       "Among the wrinkled seeds of this F2, yellow and green seeds occur in equal numbers."),
    SP("C"),
    "Reading the 9 : 3 : 3 : 1 ratio",
    "The F2 is 9 round yellow : 3 round green : 3 wrinkled yellow : 1 wrinkled green. Round : wrinkled = (9 + 3) : "
    "(3 + 1) = 12 : 4 = 3 : 1, the monohybrid ratio, because the two genes assort independently (Statement I "
    "true). Among the wrinkled seeds, yellow : green = 3 : 1, not 1 : 1 (Statement II false).",
    ["Round : wrinkled = 12 : 4 = 3 : 1", "Wrinkled yellow : wrinkled green = 3 : 1"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Sex determination", "Advanced", "multi_statement",
    ms("Consider four species in each of which the diploid female has 20 chromosomes in her somatic cells. Sex is "
       "determined in them by the XO, XY, ZW and haplodiploid mechanisms described in NCERT, respectively. "
       "Which of the following statements are correct?",
       ["In the XO species, a somatic cell of the male has 19 chromosomes.",
        "In the XY species, a somatic cell of the male has 20 chromosomes.",
        "In the haplodiploid species, the male has 10 chromosomes.",
        "In the ZW species, a somatic cell of the female has 19 chromosomes.",
        "In the XO species, every sperm carries 10 chromosomes."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "A"),
    "Chromosome numbers under different mechanisms",
    "XO type (grasshopper): females have a pair of X chromosomes, males only one X, so the male has 20 − 1 = 19 "
    "(a), and half the sperms carry the X (10 chromosomes) while half lack it (9), so (e) is false. XY type: "
    "males have X and Y, so both sexes have 20 (b). ZW type (birds): the female has one Z and one W, so she still "
    "has 20 (d false). Haplodiploidy (honey bee): males develop from unfertilised eggs and are haploid, with "
    "10 (c).",
    ["XO male = 2n − 1", "XY: equal numbers", "ZW female: Z + W, equal numbers", "Haploid male = n"],
    C12_PI("sex determination"),
    why="(d) forgets that the ZW female has a W chromosome, and (e) ignores the sperms that lack the X, so every "
        "option containing them is wrong.",
    seconds=75, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "assertion_reason",
    ar("Two parents who both have blood group O can have a child with blood group A.",
       "The allele i does not produce any sugar."),
    AR("D"),
    "ABO inheritance from O parents",
    "Blood group O is ii, so both parents can pass only i, and every child is ii (blood group O); A is false. "
    "NCERT: the allele i does not produce any sugar, whereas Iᴬ and Iᴮ produce slightly different forms of the "
    "sugar (R true).",
    ["O × O = ii × ii → all ii", "i makes no sugar"],
    C12_PI("inheritance of one gene: co-dominance"),
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "multi_statement",
    ms("Two parents with normal phenotype are both heterozygous carriers of phenylketonuria. Which of the "
       "following statements are correct?",
       ["Each of their children has a 1/4 chance of being affected.",
        "An affected child lacks the enzyme that converts the amino acid phenylalanine into tyrosine.",
        "In an affected child, phenylalanine is converted into phenylpyruvic acid and other derivatives, whose "
        "accumulation in the brain results in mental retardation.",
        "Only their sons can be affected, because the trait is sex-linked.",
        "All their children with normal phenotype will be carriers."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "B"),
    "Phenylketonuria in a carrier family",
    "PKU is an autosomal recessive trait, so Pp × Pp gives 1/4 PP, 1/2 Pp and 1/4 pp; each child has a 1/4 chance "
    "of being affected (a), sons and daughters alike (d false). Children with normal phenotype are PP or Pp, so "
    "not all are carriers (e false). NCERT: the affected individual lacks an enzyme that converts phenylalanine "
    "into tyrosine (b); phenylalanine accumulates and is converted into phenylpyruvic acid and other derivatives, "
    "whose accumulation in the brain results in mental retardation (c).",
    ["Pp × Pp → 1/4 affected", "Autosomal: either sex", "Normal children: PP or Pp",
     "Enzyme missing: phenylalanine → tyrosine"],
    C12_PI("genetic disorders: Mendelian disorders — phenylketonuria"),
    why="(d) makes an autosomal trait sex-linked and (e) ignores the normal homozygous (PP) children, so every "
        "option containing either is wrong.",
    seconds=60, verified_by=RECOMPUTED)

# ================================================================ Molecular Basis of Inheritance (8 / 10 / 8)

add(MBI, "Transcription", "Basic", "direct",
    "During transcription, the DNA strand with 5'→3' polarity, whose sequence is the same as that of the RNA "
    "(except for thymine in place of uracil), is displaced. NCERT notes that this strand, strangely, does not code "
    "for anything, yet it is called the:",
    P("Coding strand", ["Template strand", "Leading strand", "Lagging strand"], "D"),
    "Template and coding strands",
    "NCERT: in a transcription unit, the strand with 3'→5' polarity acts as the template. The other strand, which "
    "has 5'→3' polarity and the same sequence as the RNA (except thymine at the place of uracil), is displaced "
    "during transcription. Strangely, this strand (which does not code for anything) is referred to as the coding "
    "strand.",
    ["Template strand: 3'→5', copied", "Coding strand: 5'→3', same sequence as RNA, displaced"],
    C12_MB("transcription: transcription unit"),
    why="The template strand is the one copied into RNA; leading and lagging strands are terms for the new strands "
        "made during DNA replication.",
    seconds=20)

add(MBI, "Genetic code and translation", "Basic", "direct",
    "According to NCERT, the cellular factory responsible for synthesising proteins, which consists of structural "
    "RNAs and about 80 different proteins, is the:",
    P("Ribosome", ["Nucleosome", "Golgi apparatus", "Nucleolus"], "A"),
    "The ribosome",
    "NCERT: the cellular factory responsible for synthesising proteins is the ribosome. The ribosome consists of "
    "structural RNAs and about 80 different proteins. In its inactive state it exists as two subunits, a large and "
    "a small one.",
    ["Protein synthesis factory = ribosome", "Structural RNAs + ~80 proteins"],
    C12_MB("translation"),
    why="A nucleosome is DNA wrapped round a histone octamer; the Golgi apparatus packages materials; the "
        "nucleolus is a site of rRNA synthesis, not the factory that synthesises proteins.",
    seconds=20)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "direct",
    "In the Human Genome Project, the random DNA fragments were cloned using specialised vectors called BAC and "
    "YAC. According to NCERT, the commonly used hosts for this cloning were:",
    P("Bacteria and yeast", ["Mammalian cells and viruses", "Plant cells and fungi", "Bacteriophages and "
                                                                                    "protozoans"], "C"),
    "Cloning in the HGP",
    "NCERT: the random fragments were cloned in suitable hosts using specialised vectors; cloning amplified each "
    "piece so that it could be sequenced with ease. The commonly used hosts were bacteria and yeast, and the "
    "vectors were called BAC (bacterial artificial chromosomes) and YAC (yeast artificial chromosomes).",
    ["Hosts: bacteria and yeast", "Vectors: BAC and YAC"],
    C12_MB("human genome project: methodologies"),
    why="The vector names themselves (bacterial and yeast artificial chromosomes) point to the hosts; NCERT does "
        "not name mammalian cells, plants, fungi other than yeast, phages or protozoans as hosts.",
    seconds=20)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "direct",
    "According to NCERT, polymorphism in DNA sequence is the basis of:",
    P("Genetic mapping of the human genome as well as DNA fingerprinting",
      ["The universality of the genetic code", "Semiconservative replication of DNA",
       "The formation of nucleosomes"], "B"),
    "Uses of DNA polymorphism",
    "NCERT: polymorphism (variation at the genetic level) arises due to mutations; an inheritable mutation "
    "observed in a population at high frequency is DNA polymorphism. Polymorphism in DNA sequence is the basis of "
    "genetic mapping of the human genome as well as of DNA fingerprinting.",
    ["Polymorphism → genetic mapping", "Polymorphism → DNA fingerprinting"],
    C12_MB("DNA fingerprinting"),
    why="The universality of the code, semiconservative replication and nucleosome formation are shared by all "
        "individuals; they do not depend on variation between them.",
    seconds=20)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "statement_pair",
    sp("In a VNTR, a small DNA sequence is arranged tandemly in many copy numbers, and the copy number varies from "
       "chromosome to chromosome in an individual.",
       "The numbers of repeats in VNTRs show a very high degree of polymorphism."),
    SP("A"),
    "Nature of VNTRs",
    "NCERT: the VNTR belongs to a class of satellite DNA referred to as mini-satellite. A small DNA sequence is "
    "arranged tandemly in many copy numbers. The copy number varies from chromosome to chromosome in an "
    "individual (Statement I true). The numbers of repeat show a very high degree of polymorphism, and as a "
    "result the size of VNTR varies from 0.1 to 20 kb (Statement II true).",
    ["VNTR = tandem repeats, copy number varies", "Highly polymorphic → size 0.1–20 kb"],
    C12_MB("DNA fingerprinting"),
    seconds=30)

add(MBI, "Lac operon", "Basic", "match_list",
    ml(("gene of the lac operon", "its product"),
       ["i gene", "z gene", "y gene", "a gene"],
       ["Transacetylase", "Repressor", "Permease", "β-galactosidase"]),
    M(mc("II,IV,III,I"), [mc("IV,II,III,I"), mc("II,III,IV,I"), mc("II,IV,I,III")], "D"),
    "Genes of the lac operon",
    "NCERT: the lac operon consists of one regulatory gene (the i gene, coding for the repressor) and three "
    "structural genes: z codes for β-galactosidase, which hydrolyses lactose into galactose and glucose; y codes "
    "for permease, which increases the permeability of the cell to β-galactosides; and a codes for "
    "transacetylase.",
    ["i → repressor", "z → β-galactosidase", "y → permease", "a → transacetylase"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="The wrong codes swap the repressor with β-galactosidase, β-galactosidase with permease, or permease with "
        "transacetylase.",
    seconds=30)

add(MBI, "Replication", "Basic", "assertion_reason",
    ar("In eukaryotes, DNA replication takes place in the S-phase of the cell cycle.",
       "The 2'-OH group present at every nucleotide in RNA makes RNA labile and easily degradable."),
    AR("B"),
    "Two unrelated facts",
    "NCERT: in eukaryotes, the replication of DNA takes place at the S-phase of the cell cycle (A true). The "
    "2'-OH group present at every nucleotide in RNA is a reactive group that makes RNA labile and easily "
    "degradable (R true). R is about the chemistry of RNA and has nothing to do with the timing of DNA replication.",
    ["A: replication in S-phase (true)", "R: 2'-OH makes RNA labile (true)", "Unrelated → option B"],
    C12_MB("replication; the search for genetic material: properties of genetic material"),
    seconds=25)

add(MBI, "DNA as genetic material", "Basic", "direct",
    "RNA acts as the genetic material in some viruses and mostly functions as a messenger. According to NCERT, RNA "
    "has additional roles as well. It also functions as:",
    P("An adapter, a structural and in some cases a catalytic molecule",
      ["The main store of genetic information in most organisms", "A positively charged packaging protein around "
                                                                  "which DNA is wrapped",
       "The template for DNA replication in all cells"], "C"),
    "Roles of RNA",
    "NCERT: DNA acts as the genetic material in most organisms. RNA, though it also acts as the genetic material in "
    "some viruses, mostly functions as a messenger. RNA has additional roles as well: it functions as adapter, "
    "structural, and in some cases as a catalytic molecule.",
    ["RNA: messenger", "Also adapter (tRNA), structural (rRNA), catalytic (ribozyme)"],
    C12_MB("introduction; the RNA world"),
    why="DNA, not RNA, is the main genetic material and the template for DNA replication; DNA is wrapped round "
        "positively charged histone proteins, not round RNA.",
    seconds=20)

add(MBI, "Replication", "Intermediate", "assertion_reason",
    ar("In the Meselson and Stahl experiment, DNA containing ¹⁵N was distinguished from DNA containing ¹⁴N by "
       "density, not by detecting radioactivity.",
       "¹⁵N is not a radioactive isotope; it can be separated from ¹⁴N only on the basis of densities."),
    AR("A"),
    "¹⁵N is a heavy, non-radioactive isotope",
    "NCERT: Meselson and Stahl grew E. coli in a medium containing ¹⁵NH₄Cl as the only nitrogen source, so that "
    "¹⁵N was incorporated into newly synthesised DNA. Heavy DNA was distinguished from normal DNA by "
    "centrifugation in a caesium chloride density gradient. NCERT notes that ¹⁵N is not a radioactive isotope and "
    "can be separated from ¹⁴N only based on densities — which is exactly why density, not radioactivity, was used.",
    ["¹⁵N: heavy but not radioactive", "Detected by CsCl density-gradient centrifugation"],
    C12_MB("replication: the experimental proof"),
    seconds=30)

add(MBI, "Replication", "Intermediate", "assertion_reason",
    ar("In long DNA molecules, replication occurs within a small opening of the DNA helix, the replication fork.",
       "The two strands of a long DNA molecule cannot be separated in their entire length because of the very high "
       "energy requirement."),
    AR("A"),
    "Why replication forks",
    "NCERT: for long DNA molecules, since the two strands of DNA cannot be separated in their entire length (due "
    "to very high energy requirement), replication occurs within a small opening of the DNA helix, referred to as "
    "the replication fork. R is the reason given for A.",
    ["Separating the whole length: too much energy", "So replication proceeds at a small opening — the fork"],
    C12_MB("replication: the machinery and the enzymes"),
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "statement_pair",
    sp("Avery, MacLeod and McCarty purified biochemicals such as proteins, DNA and RNA from heat-killed S cells to "
       "see which of them could transform live R cells into S cells.",
       "Avery, MacLeod and McCarty concluded that DNA is the hereditary material, but not all biologists were "
       "convinced."),
    SP("A"),
    "The work of Avery, MacLeod and McCarty",
    "NCERT: Oswald Avery, Colin MacLeod and Maclyn McCarty (1933–44) worked to determine the biochemical nature of "
    "the 'transforming principle'. They purified biochemicals (proteins, DNA, RNA, etc.) from the heat-killed S "
    "cells to see which ones could transform live R cells into S cells (Statement I true). They discovered that DNA "
    "alone from S bacteria caused R bacteria to become transformed and concluded that DNA is the hereditary "
    "material, but not all biologists were convinced (Statement II true). The unequivocal proof came later from "
    "Hershey and Chase.",
    ["Purified S-cell biochemicals tested on live R cells", "Concluded DNA; not all were convinced"],
    C12_MB("the search for genetic material: biochemical characterisation of transforming principle"),
    seconds=30)

add(MBI, "Lac operon", "Intermediate", "statement_pair",
    sp("Each operon has its specific operator and specific repressor.",
       "The lac repressor can also bind to the operators of other operons, such as the trp operon, and switch them "
       "off."),
    SP("C"),
    "Specificity of operators and repressors",
    "NCERT: each operon has its specific operator and specific repressor. For example, the lac operator is present "
    "only in the lac operon and it interacts specifically with the lac repressor only (Statement I true). So the "
    "lac repressor does not act on the operators of other operons such as trp, ara, his or val (Statement II "
    "false).",
    ["Operon-specific operator and repressor", "lac operator ↔ lac repressor only"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "direct",
    "Which of the following arranges these investigations in the chronological order in which NCERT dates them?",
    P("Griffith's transformation experiments → work of Avery, MacLeod and McCarty → Hershey and Chase's bacteriophage "
      "experiments → Meselson and Stahl's proof of semiconservative replication",
      ["Avery, MacLeod and McCarty → Griffith → Hershey and Chase → Meselson and Stahl",
       "Griffith → Hershey and Chase → Avery, MacLeod and McCarty → Meselson and Stahl",
       "Griffith → Avery, MacLeod and McCarty → Meselson and Stahl → Hershey and Chase"], "B"),
    "History of the search for the genetic material",
    "NCERT dates Griffith's experiments to 1928, the work of Avery, MacLeod and McCarty to 1933–44, Hershey and "
    "Chase's experiments to 1952 and Meselson and Stahl's experiment to 1958. Avery and colleagues worked on the "
    "'transforming principle' that Griffith had described, and Hershey and Chase then gave the unequivocal proof "
    "that DNA is the genetic material.",
    ["Griffith 1928", "Avery et al. 1933–44", "Hershey–Chase 1952", "Meselson–Stahl 1958"],
    C12_MB("the search for genetic material; replication"),
    why="Avery's group studied Griffith's transforming principle, so it could not come first; Hershey and Chase "
        "(1952) came after Avery's work and before Meselson and Stahl (1958).",
    seconds=40)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "direct",
    "Which of the following gives the correct order of the steps in DNA fingerprinting as listed in NCERT?",
    P("Isolation of DNA → digestion by restriction endonucleases → separation of fragments by electrophoresis → "
      "blotting onto nitrocellulose or nylon membranes → hybridisation with a labelled VNTR probe → detection by "
      "autoradiography",
      ["Isolation of DNA → electrophoresis → digestion by restriction endonucleases → hybridisation with a labelled "
       "VNTR probe → blotting → autoradiography",
       "Isolation of DNA → digestion by restriction endonucleases → blotting → electrophoresis → autoradiography → "
       "hybridisation with a labelled VNTR probe",
       "Digestion by restriction endonucleases → isolation of DNA → electrophoresis → blotting → hybridisation with "
       "a labelled VNTR probe → autoradiography"], "D"),
    "Steps of DNA fingerprinting",
    "NCERT lists the steps as (i) isolation of DNA, (ii) digestion of DNA by restriction endonucleases, (iii) "
    "separation of DNA fragments by electrophoresis, (iv) transferring (blotting) of the separated fragments to "
    "synthetic membranes such as nitrocellulose or nylon, (v) hybridisation using a labelled VNTR probe, and (vi) "
    "detection of hybridised DNA fragments by autoradiography.",
    ["Isolate → cut → separate", "Blot → hybridise → detect"],
    C12_MB("DNA fingerprinting"),
    why="DNA must be isolated before it can be cut, and cut before the fragments can be separated; blotting "
        "follows electrophoresis, and autoradiography detects the fragments only after hybridisation with the "
        "probe.",
    seconds=45)

add(MBI, "DNA and RNA structure", "Intermediate", "multi_statement",
    ms("NCERT names the nucleosides adenosine or deoxyadenosine, guanosine or deoxyguanosine, cytidine or "
       "deoxycytidine, and uridine or deoxythymidine. Which of the following nucleosides contain a pyrimidine "
       "base?",
       ["Cytidine", "Uridine", "Deoxythymidine", "Adenosine", "Deoxyguanosine"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
    "Nucleosides and their bases",
    "A nucleoside is a nitrogenous base linked to a pentose sugar by an N-glycosidic linkage. NCERT: the purines "
    "are adenine and guanine; the pyrimidines are cytosine, uracil and thymine. Cytidine (cytosine), uridine "
    "(uracil) and deoxythymidine (thymine) therefore contain pyrimidines, whereas adenosine (adenine) and "
    "deoxyguanosine (guanine) contain purines.",
    ["Pyrimidines: C, U, T → cytidine, uridine, deoxythymidine", "Purines: A, G → adenosine, deoxyguanosine"],
    C12_MB("the DNA: structure of polynucleotide chain"),
    why="Adenosine and deoxyguanosine contain the purines adenine and guanine, so every option containing (d) or "
        "(e) is wrong.",
    seconds=40)

add(MBI, "Transcription", "Intermediate", "match_list",
    ml(("factor or enzyme", "its role"),
       ["DNA ligase", "Initiation factor (σ)", "Termination factor (ρ)", "Release factor"],
       ["Terminates translation at a stop codon", "Joins the discontinuously synthesised DNA fragments",
        "Helps RNA polymerase to terminate transcription", "Helps RNA polymerase to initiate transcription"]),
    M(mc("II,IV,III,I"), [mc("II,III,IV,I"), mc("II,IV,I,III"), mc("IV,II,III,I")], "B"),
    "Factors acting at different stages",
    "NCERT: the discontinuously synthesised fragments of DNA are later joined by DNA ligase (A-II). In bacteria, "
    "RNA polymerase associates transiently with the initiation factor σ to initiate transcription (B-IV) and with "
    "the termination factor ρ to terminate it (C-III). At the end of translation, a release factor binds to the "
    "stop codon, terminating translation and releasing the polypeptide from the ribosome (D-I).",
    ["Ligase → DNA replication", "σ → start of transcription", "ρ → end of transcription",
     "Release factor → end of translation"],
    C12_MB("replication; transcription; translation"),
    why="The wrong codes interchange σ and ρ, ρ and the release factor (one ends transcription, the other "
        "translation), or ligase and σ.",
    seconds=40)

add(MBI, "DNA packaging", "Intermediate", "assertion_reason",
    ar("Heterochromatin is the loosely packed region of chromatin that stains light.",
       "Euchromatin is said to be transcriptionally active chromatin."),
    AR("D"),
    "Euchromatin and heterochromatin",
    "NCERT: in some regions chromatin is loosely packed and stains light; this is euchromatin, which is "
    "transcriptionally active (R true). In other regions chromatin is densely packed and stains dark; this is "
    "heterochromatin, which is inactive. A attributes the features of euchromatin to heterochromatin, so A is "
    "false.",
    ["Euchromatin: loose, light, active", "Heterochromatin: dense, dark, inactive"],
    C12_MB("packaging of DNA helix"),
    seconds=25)

add(MBI, "Lac operon", "Intermediate", "statement_pair",
    sp("In E. coli, if the bacteria do not have lactose around them to be utilised as an energy source, they no "
       "longer require the synthesis of the enzyme β-galactosidase.",
       "In eukaryotes, the expression of genes is regulated only at the transcriptional level."),
    SP("C"),
    "Need-based regulation of gene expression",
    "NCERT: in E. coli, β-galactosidase catalyses the hydrolysis of lactose into galactose and glucose; if the "
    "bacteria do not have lactose around them to be utilised for energy, they no longer require the synthesis of "
    "this enzyme (Statement I true). In eukaryotes, regulation can be exerted at the transcriptional level "
    "(formation of the primary transcript), the processing level (regulation of splicing), the transport of mRNA "
    "from nucleus to cytoplasm, and the translational level (Statement II false).",
    ["Enzyme made only when its substrate is available", "Eukaryotes: four levels of regulation"],
    C12_MB("regulation of gene expression"),
    seconds=35)

add(MBI, "Transcription", "Advanced", "assertion_reason",
    ar("In eukaryotes, RNA polymerase I transcribes the rRNAs 28S, 18S and 5.8S.",
       "RNA polymerase I also transcribes the 5S rRNA."),
    AR("C"),
    "Division of labour among eukaryotic RNA polymerases",
    "NCERT: in the nucleus there are at least three RNA polymerases. RNA polymerase I transcribes rRNAs (28S, 18S "
    "and 5.8S) (A true); RNA polymerase III is responsible for transcription of tRNA, 5S rRNA and snRNAs; RNA "
    "polymerase II transcribes the precursor of mRNA, the hnRNA. Since the 5S rRNA is made by RNA polymerase III, "
    "R is false.",
    ["Pol I: 28S, 18S, 5.8S rRNA", "Pol II: hnRNA", "Pol III: tRNA, 5S rRNA, snRNAs"],
    C12_MB("transcription: transcription in eukaryotes"),
    seconds=35)

add(MBI, "DNA packaging", "Advanced", "assertion_reason",
    ar("A typical nucleosome contains about 2000 bp of DNA helix.",
       "Under the electron microscope, nucleosomes in chromatin are seen as 'beads-on-string'."),
    AR("D"),
    "Size of a nucleosome",
    "NCERT: the positively charged histone octamer has the negatively charged DNA wrapped around it to form the "
    "nucleosome; a typical nucleosome contains 200 bp of DNA helix, not 2000 bp (A false). Nucleosomes constitute "
    "the repeating unit of a structure in the nucleus called chromatin, which is seen as 'beads-on-string' under "
    "the electron microscope (R true).",
    ["Nucleosome ≈ 200 bp", "Chromatin = beads (nucleosomes) on a string (DNA)"],
    C12_MB("packaging of DNA helix"),
    seconds=30)

add(MBI, "DNA and RNA structure", "Advanced", "direct",
    "NCERT lists nucleosides in pairs: adenosine or deoxyadenosine, guanosine or deoxyguanosine, cytidine or "
    "deoxycytidine, and uridine or deoxythymidine. Which of the following pairs contain the SAME nitrogenous base "
    "and differ only in their sugar?",
    P("Adenosine and deoxyadenosine",
      ["Uridine and deoxythymidine", "Cytidine and guanosine", "Deoxyguanosine and deoxyadenosine"], "A"),
    "Reading NCERT's list of nucleosides",
    "Adenosine (adenine + ribose) and deoxyadenosine (adenine + deoxyribose) share the base and differ only in "
    "the sugar. Uridine and deoxythymidine, although paired in NCERT's list, contain different bases — uracil in "
    "RNA and thymine (5-methyl uracil) in DNA — as well as different sugars. Cytidine and guanosine, and "
    "deoxyguanosine and deoxyadenosine, contain different bases.",
    ["Same base, different sugar: adenosine / deoxyadenosine", "Uridine (U) ≠ deoxythymidine (T)"],
    C12_MB("the DNA: structure of polynucleotide chain"),
    why="Uridine and deoxythymidine differ in base (uracil versus thymine); cytidine/guanosine and "
        "deoxyguanosine/deoxyadenosine pair a pyrimidine with a purine or two different purines.",
    seconds=45)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "direct",
    "Which of the following gives the correct order of the steps in the methodology of sequencing the human "
    "genome, as described in NCERT?",
    P("Total DNA isolated and broken into random fragments → fragments cloned in bacteria or yeast using BAC or YAC "
      "vectors → fragments sequenced by automated DNA sequencers → sequences arranged on the basis of overlapping "
      "regions using computer programs → sequences annotated and assigned to chromosomes",
      ["Whole chromosome sequenced intact → cut into random fragments → fragments cloned in BAC or YAC vectors → "
       "overlapping regions aligned by computer programs",
       "Total DNA isolated → fragments arranged on the basis of overlapping regions → fragments cloned in bacteria "
       "or yeast → fragments sequenced by automated DNA sequencers",
       "Total DNA isolated and broken into random fragments → fragments sequenced by automated DNA sequencers → "
       "fragments cloned in bacteria or yeast to amplify them → sequences annotated"], "D"),
    "HGP methodology",
    "NCERT: the total DNA from a cell was isolated and converted into random fragments of relatively smaller sizes "
    "(very long pieces cannot be sequenced). These were cloned in suitable hosts (bacteria and yeast) using BAC and "
    "YAC vectors, which amplified each piece so that it could be sequenced with ease. The fragments were sequenced "
    "using automated DNA sequencers working on Sanger's method. The sequences were then arranged on the basis of "
    "overlapping regions, using specialised computer-based programs, and were subsequently annotated and assigned "
    "to each chromosome.",
    ["Isolate and fragment", "Clone (amplify)", "Sequence", "Align overlaps by computer", "Annotate and assign"],
    C12_MB("human genome project: methodologies"),
    why="Very long DNA cannot be sequenced intact; overlaps can be aligned only after the fragments are sequenced; "
        "and cloning is done before sequencing, to amplify each fragment.",
    seconds=60)

add(MBI, "Genetic code and translation", "Advanced", "multi_statement",
    ms("Which of the following statements about the chemistry of translation are made in NCERT?",
       ["Amino acids are activated in the presence of ATP and linked to their cognate tRNA (charging of tRNA).",
        "If two charged tRNAs are brought close enough, the formation of a peptide bond between them is favoured "
        "energetically.",
        "The presence of a catalyst enhances the rate of peptide bond formation.",
        "In bacteria, the 23S rRNA acts as the enzyme (ribozyme) that forms the peptide bond.",
        "Specific tRNAs read the stop codons and bring a terminal amino acid."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "b", "d"], ["b", "c", "d", "e"]], "A"),
    "Charging, energetics and catalysis in translation",
    "NCERT: translation begins with the charging (aminoacylation) of tRNA, in which amino acids are activated in "
    "the presence of ATP and linked to their cognate tRNA (a). If two such charged tRNAs are brought close enough, "
    "peptide bond formation between them is favoured energetically (b), and the presence of a catalyst enhances "
    "the rate (c). In bacteria the 23S rRNA acts as the enzyme — a ribozyme (d). There are no tRNAs for the stop "
    "codons; a release factor binds there (e false).",
    ["Charging uses ATP", "Charged tRNAs close together → bond favoured", "Catalyst (23S rRNA ribozyme) speeds it",
     "Stop codons: release factor, no tRNA"],
    C12_MB("translation"),
    why="(e) is false — there are no tRNAs for stop codons — so options containing it are wrong; '(a), (b) and "
        "(d) only' leaves out the role of the catalyst (c).",
    seconds=60)

add(MBI, "DNA as genetic material", "Advanced", "match_list",
    ml(("observation", "conclusion drawn from it"),
       ["Bacteria infected with phages grown on radioactive sulphur were not radioactive",
        "Digesting the transforming extract with DNase inhibited transformation",
        "¹⁵N-DNA showed only hybrid density after one generation in ¹⁴N medium, and equal hybrid and light DNA "
        "after two generations",
        "Mice injected with heat-killed S strain plus live R strain bacteria died, and live S strain bacteria were "
        "recovered from them"],
       ["The R strain bacteria had been transformed by a 'transforming principle' from the heat-killed S strain",
        "DNA replicates semiconservatively", "DNA is the transforming principle",
        "The viral protein did not enter the bacteria"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,II,III,I"), mc("IV,III,I,II")], "D"),
    "Interpreting the classic experiments",
    "Hershey and Chase: bacteria infected with phages carrying radioactive (sulphur-labelled) protein were not "
    "radioactive, so the protein did not enter the bacteria (A-IV). Avery, MacLeod and McCarty: DNase inhibited "
    "transformation, so DNA is the transforming principle (B-III). Meselson and Stahl: hybrid DNA after 20 minutes "
    "and equal hybrid and light DNA after 40 minutes showed semiconservative replication (C-II). Griffith: the "
    "R strain had been transformed by some 'transforming principle' from the heat-killed S strain (D-I).",
    ["³⁵S result → protein stays out", "DNase → DNA transforms", "Density pattern → semiconservative",
     "Mixed injection → transformation"],
    C12_MB("the search for genetic material; replication: the experimental proof"),
    why="The wrong codes give the sulphur result Avery's conclusion, mix up Avery's and Meselson–Stahl's "
        "conclusions, or interchange Meselson–Stahl's and Griffith's.",
    seconds=60)

add(MBI, "Transcription", "Advanced", "multi_statement",
    ms("Which of the following involve polymerisation of nucleotides in a template-independent manner, according to "
       "NCERT?",
       ["Addition of adenylate residues at the 3'-end of hnRNA (tailing)",
        "Polymerisation of RNA with defined sequences by the enzyme (polynucleotide phosphorylase) used by Severo "
        "Ochoa",
        "Synthesis of RNA by DNA-dependent RNA polymerase during transcription",
        "Synthesis of DNA by DNA-dependent DNA polymerase during replication",
        "Synthesis of the discontinuous strand at the replication fork"]),
    MS(["a", "b"], [["a", "b", "c"], ["a", "c", "e"], ["b", "d"]], "B"),
    "Template-dependent and template-independent synthesis",
    "NCERT: in tailing, adenylate residues (200–300) are added at the 3'-end in a template-independent manner (a). "
    "Severo Ochoa's enzyme (polynucleotide phosphorylase) was helpful in polymerising RNA with defined sequences in "
    "a template-independent manner (b). DNA-dependent RNA polymerase and DNA-dependent DNA polymerase both copy a "
    "DNA template (c, d false), and the discontinuous strand at the fork is also made on a template (e false).",
    ["Template-independent: tailing; Ochoa's enzyme", "Template-dependent: transcription, replication (both "
                                                      "strands)"],
    C12_MB("transcription; genetic code"),
    why="Transcription and replication (including the discontinuous strand) are template-dependent, so every option "
        "containing (c), (d) or (e) is wrong.",
    seconds=50)

add(MBI, "Replication", "Advanced", "assertion_reason",
    ar("When E. coli grown for many generations in ¹⁵NH₄Cl medium is transferred to ¹⁴NH₄Cl medium, the DNA "
       "extracted after 20 minutes (one generation) has a hybrid, intermediate density.",
       "Taylor and colleagues used radioactive thymidine to show that DNA in the chromosomes of Vicia faba also "
       "replicates semiconservatively."),
    AR("B"),
    "Meselson–Stahl result and Taylor's experiment",
    "NCERT: in the Meselson and Stahl experiment, DNA extracted after one generation (20 minutes) in ¹⁴N medium had "
    "a hybrid or intermediate density, because each molecule had one old (¹⁵N) and one new (¹⁴N) strand (A true). "
    "Taylor and colleagues (1958) used radioactive thymidine in Vicia faba to show semiconservative replication in "
    "chromosomes (R true). R reports a separate experiment on a different organism; it is not the reason for the "
    "density observed in E. coli.",
    ["A: one ¹⁵N + one ¹⁴N strand → hybrid density (true)", "R: Taylor's Vicia faba work (true)",
     "R does not explain A"],
    C12_MB("replication: the experimental proof"),
    seconds=35)

# ================================================================ Microbes in Human Welfare (3 / 4 / 3)

add(MHW, "Sewage treatment", "Basic", "direct",
    "Before sewage is disposed of, it is treated in sewage treatment plants (STPs) to make it less polluting. "
    "According to NCERT, this treatment is carried out by:",
    P("Heterotrophic microbes naturally present in the sewage",
      ["Autotrophic cyanobacteria added to the sewage from paddy fields",
       "Chemical oxidising agents added at each stage of the plant",
       "Photosynthetic algae grown on the surface of the aeration tanks"], "A"),
    "Who treats sewage in an STP",
    "NCERT: sewage is treated in sewage treatment plants to make it less polluting, and this treatment is carried "
    "out by heterotrophic microbes naturally present in the sewage. In the aeration tanks, for example, aerobic "
    "microbes grow into flocs and consume the organic matter, and in the anaerobic sludge digesters other "
    "bacteria digest the sludge.",
    ["STP treatment = microbial", "Done by heterotrophic microbes already present in the sewage"],
    C12_MW("microbes in sewage treatment"),
    why="The microbes are not added from outside and are not autotrophs: they feed on the organic matter of the "
        "sewage. NCERT describes the process as a biological (microbial) one, not chemical oxidation.",
    seconds=25)

add(MHW, "Household and industrial products", "Basic", "direct",
    "NCERT lists the deadly diseases that antibiotics have greatly improved our capacity to treat, giving the "
    "common Indian name of some of them. The disease that NCERT calls 'kusht rog' is:",
    P("Leprosy", ["Plague", "Whooping cough", "Diphtheria"], "C"),
    "Antibiotics and the diseases they treat",
    "NCERT: antibiotics have greatly improved our capacity to treat deadly diseases such as plague, whooping cough "
    "(kali khansi), diphtheria (gal ghotu) and leprosy (kusht rog), which used to kill millions all over the "
    "globe.",
    ["kali khansi = whooping cough", "gal ghotu = diphtheria", "kusht rog = leprosy"],
    C12_MW("microbes in industrial products: antibiotics"),
    why="Whooping cough is 'kali khansi' and diphtheria is 'gal ghotu' in NCERT; NCERT gives no Indian name for "
        "plague.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "Trichoderma species, which NCERT describes as effective biocontrol agents of several plant pathogens, are "
    "free-living fungi that are very common in:",
    P("Root ecosystems", ["The rumen of cattle", "Anaerobic sludge digesters", "The gut of insect larvae"], "D"),
    "Trichoderma as a biocontrol agent",
    "NCERT: Trichoderma species are free-living fungi that are very common in the root ecosystems; they are "
    "effective biocontrol agents of several plant pathogens.",
    ["Trichoderma: free-living fungus", "Common in root ecosystems; controls plant pathogens"],
    C12_MW("microbes as biocontrol agents"),
    why="The rumen of cattle and sludge digesters are where NCERT places methanogenic bacteria; the gut of insect "
        "larvae is where the Bt toxin is released.",
    seconds=20)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "direct",
    "Rhizobium, Azotobacter and Anabaena are all named by NCERT as biofertilisers, while Glomus is named as a "
    "biofertiliser of a different kind. Which feature do the first three share that NCERT does NOT give for "
    "Glomus?",
    P("They fix atmospheric nitrogen",
      ["They live in symbiotic association with plant roots",
       "They are autotrophs that add organic matter to the soil",
       "They absorb phosphorus from the soil and pass it to the plant"], "B"),
    "Comparing NCERT's biofertilisers",
    "NCERT: Rhizobium fixes atmospheric nitrogen in the root nodules of legumes; Azospirillum and Azotobacter fix "
    "atmospheric nitrogen while free-living in the soil; cyanobacteria such as Anabaena, Nostoc and Oscillatoria "
    "fix atmospheric nitrogen. Glomus forms mycorrhiza, a symbiosis in which the fungus absorbs phosphorus from "
    "the soil and passes it to the plant; NCERT does not describe it as fixing nitrogen.",
    ["Rhizobium, Azotobacter, Anabaena: N₂ fixers", "Glomus: mycorrhiza, phosphorus absorption"],
    C12_MW("microbes as biofertilisers"),
    why="Symbiosis with roots applies to Rhizobium and Glomus but not to free-living Azotobacter or Anabaena; "
        "only the cyanobacteria are autotrophs that add organic matter; phosphorus absorption is Glomus's own "
        "role.",
    seconds=40)

add(MHW, "Biogas", "Intermediate", "assertion_reason",
    ar("In a biogas plant fed with a slurry of dung, the floating cover placed over the slurry keeps on rising.",
       "Gas is produced in the tank by microbial activity on the slurry."),
    AR("A"),
    "Working of a biogas plant",
    "NCERT: the biogas plant consists of a concrete tank (10–15 feet deep) in which bio-wastes are collected and "
    "a slurry of dung is fed. A floating cover is placed over the slurry, which keeps on rising as the gas is "
    "produced in the tank due to microbial activity. The rising of the cover (A) is caused by the gas produced "
    "(R).",
    ["Methanogens in dung produce gas", "Gas collects under the floating cover and pushes it up"],
    C12_MW("microbes in production of biogas"),
    seconds=30)

add(MHW, "Household and industrial products", "Intermediate", "statement_pair",
    sp("Depending on the type of raw material used for fermentation and the type of processing (with or without "
       "distillation), different types of alcoholic drinks are obtained.",
       "The yeast used for bread-making and the brewer's yeast used for producing ethanol from malted cereals and "
       "fruit juices are two different species of Saccharomyces."),
    SP("C"),
    "Fermented beverages",
    "NCERT: Saccharomyces cerevisiae, used for bread-making and commonly called brewer's yeast, is used for "
    "fermenting malted cereals and fruit juices to produce ethanol; depending on the raw material and the type of "
    "processing (with or without distillation), different types of alcoholic drinks are obtained (Statement I "
    "true). The same species serves both purposes, so Statement II is false.",
    ["Drink type depends on raw material + processing", "Baker's and brewer's yeast: both Saccharomyces "
     "cerevisiae"],
    C12_MW("microbes in industrial products: fermented beverages"),
    seconds=35)

add(MHW, "Household and industrial products", "Intermediate", "statement_pair",
    sp("Colonies of bacteria and fungi grown on nutritive media can be seen only with the help of a microscope.",
       "Among the diverse microbes, NCERT includes viroids and also prions, which are proteinaceous infectious "
       "agents."),
    SP("D"),
    "Diversity of microbes",
    "NCERT: microbes are diverse — protozoa, bacteria, fungi and microscopic animal and plant viruses, viroids and "
    "also prions that are proteinaceous infectious agents (Statement II true). Microbes like bacteria and fungi "
    "can be grown on nutritive media to form colonies that can be seen with the naked eyes, so Statement I is "
    "false.",
    ["Colonies: visible to the naked eye", "Microbes include viruses, viroids and prions"],
    C12_MW("introduction"),
    seconds=30)

add(MHW, "Household and industrial products", "Advanced", "direct",
    "Which of the following pairs consists of a product obtained from a BACTERIUM followed by a product obtained "
    "from a FUNGUS, according to NCERT?",
    P("Butyric acid; citric acid",
      ["Citric acid; acetic acid", "Penicillin; streptokinase", "Lactic acid; acetic acid"], "B"),
    "Bacterial and fungal products",
    "NCERT: butyric acid is produced by the bacterium Clostridium butylicum, and citric acid by the fungus "
    "Aspergillus niger. Acetic acid comes from the bacterium Acetobacter aceti, lactic acid from Lactobacillus (a "
    "bacterium), streptokinase from the bacterium Streptococcus, and penicillin from the mould Penicillium "
    "notatum.",
    ["Clostridium (bacterium) → butyric acid", "Aspergillus niger (fungus) → citric acid"],
    C12_MW("microbes in industrial products: chemicals, enzymes and other bioactive molecules; antibiotics"),
    why="'Citric acid; acetic acid' and 'penicillin; streptokinase' are fungus-then-bacterium, the reverse order; "
        "lactic acid and acetic acid both come from bacteria.",
    seconds=45)
add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "multi_statement",
    ms("A farmer in an ecologically sensitive area grows cabbage (a brassica). The crop has butterfly "
       "caterpillars and aphids, and the soil has several fungal plant pathogens. The farmer wants to avoid "
       "chemical pesticides and to spare the other insects of the field. Which of the following choices are "
       "supported by NCERT?",
       ["Spraying a suspension of Bacillus thuringiensis spores to kill the caterpillars",
        "Encouraging ladybird beetles to get rid of the aphids",
        "Using Trichoderma species against the plant pathogens",
        "Encouraging dragonflies, which NCERT names as the main control of aphids",
        "Spraying a broad-spectrum insecticide, since it kills the caterpillars and aphids together"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "C"),
    "Choosing biocontrol agents",
    "NCERT: Bt spores sprayed on brassicas kill butterfly caterpillars but leave other insects unharmed (a). The "
    "ladybird beetle is useful to get rid of aphids (b), and dragonflies are useful to get rid of mosquitoes, not "
    "aphids (d false). Trichoderma species are effective biocontrol agents of several plant pathogens (c). "
    "Broad-spectrum chemicals are toxic, kill useful as well as harmful insects and pollute the environment, so "
    "they defeat the farmer's aim (e false).",
    ["Caterpillars → Bt", "Aphids → ladybird beetle", "Plant pathogens → Trichoderma",
     "Dragonflies → mosquitoes", "Broad-spectrum chemicals: avoided in biocontrol"],
    C12_MW("microbes as biocontrol agents"),
    why="Dragonflies control mosquitoes, not aphids (d), and a broad-spectrum insecticide is the opposite of the "
        "biocontrol approach (e), so every option containing (d) or (e) is wrong.",
    seconds=60)

add(MHW, "Household and industrial products", "Advanced", "assertion_reason",
    ar("Bottled fruit juices bought from the market are clearer than those made at home.",
       "Lipases are used in detergent formulations and are helpful in removing oily stains from the laundry."),
    AR("B"),
    "Microbial enzymes and their separate uses",
    "NCERT: bottled juices are clearer than home-made ones because they are clarified by the use of pectinases and "
    "proteases (A true). Lipases are used in detergents to remove oily stains (R true), but this is a different "
    "use of a different enzyme and has nothing to do with the clarity of juices.",
    ["Juice clarification: pectinases and proteases", "Lipases: detergents, oily stains", "R true but unrelated"],
    C12_MW("microbes in industrial products: chemicals, enzymes and other bioactive molecules"),
    seconds=40)

# ================================================================ Organisms and Populations (5 / 6 / 5)

add(OAP, "Population attributes", "Basic", "direct",
    "The term 'interbreeding' in the definition of a population implies sexual reproduction. According to NCERT, "
    "a group of individuals resulting from asexual reproduction is:",
    P("Also generally considered a population for the purpose of ecological studies",
      ["Never treated as a population, because its members do not interbreed",
       "Treated as a community rather than a population",
       "Treated as a population only if its members show different sex ratios"], "D"),
    "Asexual groups as populations",
    "NCERT: in nature we rarely find isolated, single individuals; most live in groups in a well-defined area, "
    "share or compete for similar resources, potentially interbreed and so constitute a population. Although the "
    "term interbreeding implies sexual reproduction, a group of individuals resulting from even asexual "
    "reproduction is also generally considered a population for the purpose of ecological studies.",
    ["Population: same species, one area, shared resources, potential interbreeding",
     "Asexual groups are also generally treated as populations"],
    C12_OP("populations: population attributes"),
    why="NCERT explicitly includes asexually produced groups; a community contains several species; sex ratio is "
        "an attribute of a population, not a condition for being one.",
    seconds=25)

add(OAP, "Population interactions", "Basic", "direct",
    "When Darwin spoke of the struggle for existence and survival of the fittest in nature, he was convinced, "
    "according to NCERT, that a potent force in organic evolution is:",
    P("Interspecific competition", ["Mutualism", "Commensalism", "Amensalism"], "B"),
    "Darwin and competition",
    "NCERT (competition): when Darwin spoke of the struggle for existence and survival of the fittest in nature, "
    "he was convinced that interspecific competition is a potent force in organic evolution.",
    ["Struggle for existence → competition", "Darwin: interspecific competition drives organic evolution"],
    C12_OP("population interactions: competition"),
    why="Mutualism, commensalism and amensalism are other interactions; NCERT links Darwin's struggle for "
        "existence to competition.",
    seconds=20)

add(OAP, "Population interactions", "Basic", "statement_pair",
    sp("Interspecific interactions arise from the interaction of populations of two different species.",
       "Such interactions could be beneficial, detrimental or neutral (neither harm nor benefit) to one of the "
       "species or to both."),
    SP("A"),
    "Nature of interspecific interactions",
    "NCERT: interspecific interactions arise from the interaction of populations of two different species. They "
    "could be beneficial, detrimental or neutral (neither harm nor benefit) to one of the species or both. Both "
    "statements are NCERT's own lines.",
    ["Interspecific = two different species", "Effect: +, − or 0 on one or both"],
    C12_OP("population interactions"),
    seconds=25)

_N0, _B, _D, _E, _N1 = 400, 60, 20, 10, 450
_I = _N1 - _N0 - _B + _D + _E
assert _I == 20 and _N0 + (_B + _I) - (_D + _E) == _N1
assert _N1 - _N0 - _B + _D == 10          # emigrants ignored
assert _N1 - _N0 - _B + _D - _E == 0      # emigrants added instead of subtracted
assert _N1 - _N0 + _D + _E == 80          # births ignored

add(OAP, "Population growth", "Basic", "numerical",
    "A population of 400 individuals at the start of a year shows, during the year, 60 births, 20 deaths and 10 "
    "emigrants, and has 450 individuals at the end of the year. Using N(t+1) = N(t) + [(B + I) − (D + E)], how "
    "many individuals immigrated into the population during the year?",
    P("20", ["10", "0", "80"], "C"),
    "Change in population density",
    "N(t+1) = N(t) + [(B + I) − (D + E)], so 450 = 400 + (60 + I) − (20 + 10). Hence 450 = 430 + I and I = 20.",
    ["450 = 400 + 60 + I − 20 − 10", "450 = 430 + I", "I = 20"],
    C12_OP("populations: population growth"),
    why="10 ignores the emigrants; 0 adds the emigrants instead of subtracting them; 80 leaves out the births.",
    seconds=40, verified_by=RECOMPUTED)

add(OAP, "Population growth", "Basic", "direct",
    "In the exponential growth equation dN/dt = rN, r = b − d, where b and d are the per capita birth and death "
    "rates. In a population with no immigration or emigration, if b equals d, the population size will:",
    P("Remain constant", ["Increase exponentially", "Decline steadily to zero", "Rise to the carrying capacity "
                                                                                "and then crash"], "A"),
    "r = b − d",
    "NCERT writes the increase or decrease in N during a unit time period as dN/dt = (b − d) × N, and lets "
    "(b − d) = r. If b = d, then r = 0 and dN/dt = 0 × N = 0: the population neither grows nor declines.",
    ["r = b − d = 0", "dN/dt = 0 × N = 0", "Size stays constant"],
    C12_OP("populations: population growth (exponential growth)"),
    why="Exponential increase needs r > 0, a steady decline needs r < 0, and the carrying capacity belongs to the "
        "logistic model, not to a population with zero r.",
    seconds=25)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("Two species that face competition for a resource may co-exist rather than one of them being eliminated.",
       "Species facing competition might evolve mechanisms that promote co-existence rather than exclusion, one "
       "such mechanism being resource partitioning."),
    AR("A"),
    "Co-existence through resource partitioning",
    "NCERT: more recent studies do not rule out interspecific competition, but point out that species facing "
    "competition might evolve mechanisms that promote co-existence rather than exclusion. One such mechanism is "
    "resource partitioning: if two species compete for the same resource, they could avoid competition by "
    "choosing, for instance, different times for feeding or different foraging patterns. R directly explains A.",
    ["Competition need not lead to exclusion", "Resource partitioning promotes co-existence"],
    C12_OP("population interactions: competition"),
    seconds=35)

add(OAP, "Population attributes", "Intermediate", "match_list",
    ml(("example from NCERT", "what NCERT uses it to illustrate"),
       ["Siberian cranes at the Bharatpur wetlands", "Pacific salmon fish", "Oysters", "Flour beetle"],
       ["Breeds only once in its lifetime",
        "Produces a large number of small-sized offspring",
        "An intrinsic rate of natural increase (r) of 0.12",
        "A population that in any year may number fewer than 10"]),
    M(mc("IV,I,II,III"), [mc("IV,II,I,III"), mc("I,IV,II,III"), mc("IV,I,III,II")], "C"),
    "NCERT's population examples",
    "NCERT: the size of a population could be as low as fewer than 10 (Siberian cranes at Bharatpur wetlands in "
    "any year) (A-IV). Some organisms breed only once in their lifetime, such as Pacific salmon fish and bamboo "
    "(B-I). Some produce a large number of small-sized offspring, such as oysters and pelagic fishes (C-II). The "
    "r value for the flour beetle is 0.12 (D-III).",
    ["Siberian cranes: < 10", "Pacific salmon: breeds once", "Oysters: many small offspring",
     "Flour beetle: r = 0.12"],
    C12_OP("populations: population attributes; population growth; life history variation"),
    why="The wrong codes swap the salmon with the oysters, the cranes with the salmon, or the oysters with the "
        "flour beetle.",
    seconds=40)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following statements about predation agree with NCERT?",
       ["Predation can be thought of as nature's way of transferring to higher trophic levels the energy fixed by "
        "plants.",
        "Predators keep prey populations under control.",
        "Predators help in maintaining species diversity in a community by reducing the intensity of competition "
        "among competing prey species.",
        "In a broad ecological context, herbivores are not very different from predators.",
        "A predator that over-exploits its prey benefits in the long run, as it never runs short of food."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "c", "d", "e"]], "D"),
    "Roles of predators",
    "NCERT: predation is nature's way of transferring to higher trophic levels the energy fixed by plants (a). "
    "Besides acting as conduits for energy transfer, predators keep prey populations under control (b) and help "
    "in maintaining species diversity by reducing the intensity of competition among competing prey species (c). "
    "In a broad ecological context, herbivores are not very different from predators (d). Predators are "
    "'prudent': one that over-exploits its prey may drive the prey extinct and then become extinct itself for "
    "lack of food (e false).",
    ["Energy conduit", "Control of prey", "Maintenance of diversity", "Herbivores ≈ predators",
     "Over-exploitation harms the predator too"],
    C12_OP("population interactions: predation"),
    why="(e) contradicts NCERT's 'prudent predator' argument; '(a), (c) and (d) only' leaves out the control of "
        "prey populations (b).",
    seconds=50)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("Competition need not involve a limiting resource: in interference competition, the feeding efficiency of "
       "one species may be reduced by the inhibitory presence of the other even if food and space are abundant.",
       "Competitive release is the dramatic expansion in the range of the competitively superior species after "
       "the inferior species is experimentally removed."),
    SP("C"),
    "Interference competition and competitive release",
    "NCERT: resources need not be limiting for competition to occur; in interference competition, the feeding "
    "efficiency of one species might be reduced due to the interfering and inhibitory presence of the other "
    "species, even if resources are abundant (Statement I true). Competitive release refers to the species whose "
    "distribution is restricted by a competitively SUPERIOR species: it expands its range dramatically when the "
    "superior competitor is experimentally removed. Statement II reverses the roles (false).",
    ["Interference: works even with abundant resources", "Competitive release: the restricted (inferior) "
     "species expands"],
    C12_OP("population interactions: competition"),
    seconds=40)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("Lichens are an example of commensalism.",
       "Lichens represent an intimate mutualistic relationship between a fungus and photosynthesising algae or "
       "cyanobacteria."),
    AR("D"),
    "Lichens are mutualistic",
    "NCERT gives lichens as an example of mutualism, an intimate relationship between a fungus and "
    "photosynthesising algae or cyanobacteria in which both partners benefit (R true). In commensalism one species "
    "benefits and the other is neither harmed nor benefited, so A is false.",
    ["Lichen: fungus + alga/cyanobacterium", "Both benefit → mutualism, not commensalism"],
    C12_OP("population interactions: mutualism"),
    seconds=30)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following are described in NCERT as examples of parasitism?",
       ["Ectoparasitic copepods infesting many marine fish",
        "A koel (cuckoo) laying its eggs in the nest of a crow",
        "The human liver fluke, with a snail and a fish as intermediate hosts",
        "Barnacles growing on the back of a whale",
        "An orchid growing as an epiphyte on a mango branch"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
    "Recognising parasitism",
    "NCERT's parasitism section names ectoparasitic copepods on many marine fish (a), brood parasitism in birds, in "
    "which the cuckoo (koel) lays its eggs in the crow's nest (b), and the human liver fluke, a trematode that "
    "depends on two intermediate hosts (a snail and a fish) (c). Barnacles on a whale and an orchid epiphyte on a "
    "mango branch are NCERT's examples of commensalism: the whale and the mango tree derive no apparent benefit "
    "and are not harmed (d, e).",
    ["Copepods, brood parasitism, liver fluke → parasitism", "Barnacle–whale, orchid–mango → commensalism"],
    C12_OP("population interactions: parasitism; commensalism"),
    why="Options containing (d) or (e) include NCERT's commensals; '(a), (c) and (e)' also leaves out brood "
        "parasitism.",
    seconds=40)

_r, _N, _rate = F(1, 2), 200, 80
_K = _N / (1 - _rate / (_r * _N))
assert _K == 1000 and _r * _N * (_K - _N) / _K == _rate
assert _N / (_rate / (_r * _N)) == 250          # took N/K = 0.8
assert _K - _N == 800                           # stopped at K − N
assert _N * (1 + _rate / (_r * _N)) == 360      # used (K − N)/N = 0.8

add(OAP, "Population growth", "Advanced", "numerical",
    "A population grows according to the logistic model, dN/dt = rN[(K − N)/K], with r = 0.5 per year. When the "
    "population has 200 individuals, its growth rate is 80 individuals per year. What is the carrying capacity "
    "(K) of the habitat?",
    P("1000", ["250", "800", "360"], "B"),
    "Solving the logistic equation for K",
    "Under exponential growth the rate would be rN = 0.5 × 200 = 100 per year. The actual rate is 80, so "
    "(K − N)/K = 80/100 = 0.8. Then N/K = 0.2 and K = 200/0.2 = 1000.",
    ["rN = 100", "(K − N)/K = 80/100 = 0.8", "N/K = 0.2 → K = 1000"],
    C12_OP("populations: population growth (logistic growth)"),
    shortcut="(K − N)/K = actual rate ÷ rN; then K = N ÷ (1 − that fraction).",
    why="250 treats N/K (instead of (K − N)/K) as 0.8; 800 is K − N, not K; 360 uses (K − N)/N in place of "
        "(K − N)/K.",
    seconds=75, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    ms("Which of the following statements about competition are made in NCERT?",
       ["Totally unrelated species could also compete for the same resource.",
        "In some shallow South American lakes, visiting flamingoes and resident fishes compete for their common "
        "food, the zooplankton.",
        "Competition is a process in which the fitness of one species (measured in terms of its 'r') is "
        "significantly lower in the presence of another species.",
        "Gause's competitive exclusion principle may be true if resources are limiting, but not otherwise.",
        "More recent studies rule out the occurrence of interspecific competition in nature."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "b", "d"], ["b", "c", "d", "e"]], "C"),
    "NCERT's account of competition",
    "NCERT: competition is generally believed to occur between closely related species competing for limiting "
    "resources, but this is not entirely true: totally unrelated species could also compete (a), as flamingoes "
    "and fishes do for zooplankton in South American lakes (b). Competition is a process in which the fitness of "
    "one species, measured as its 'r', is significantly lower in the presence of another (c). Gause's principle "
    "'may be true if resources are limiting, but not otherwise' (d). More recent studies do NOT rule out "
    "interspecific competition; they point out that competing species might evolve mechanisms that promote "
    "co-existence (e false).",
    ["Unrelated species can compete", "Fitness (r) lowered", "Gause: only when resources are limiting",
     "Recent studies do not rule competition out"],
    C12_OP("population interactions: competition"),
    why="(e) reverses NCERT's statement about recent studies; '(a), (b) and (d) only' omits NCERT's definition of "
        "competition (c).",
    seconds=60)

_r_true = 1.386 / 20
assert abs(_r_true - 0.0693) < 1e-12
assert abs(0.693 / 20 - 0.03465) < 1e-12            # used ln 2 instead of ln 4
assert (2000 - 500) / (500 * 20) == 0.15            # simple (linear) growth per year

add(OAP, "Population growth", "Advanced", "numerical",
    "A population grows exponentially according to Nₜ = N₀e^(rt). It increases from 500 to 2000 individuals in "
    "20 years. What is its intrinsic rate of natural increase, r? (Take ln 4 = 1.386.)",
    P("0.0693 per year", ["0.0347 per year", "0.15 per year", "1.386 per year"], "D"),
    "Finding r from the integral form",
    "Nₜ/N₀ = 2000/500 = 4 = e^(r × 20). Taking natural logarithms, 20r = ln 4 = 1.386, so r = 1.386/20 = 0.0693 "
    "per year.",
    ["Nₜ/N₀ = 4", "rt = ln 4 = 1.386", "r = 1.386/20 = 0.0693 per year"],
    C12_OP("populations: population growth (exponential growth)"),
    why="0.0347 uses ln 2 (one doubling) although the population quadrupled; 0.15 treats the growth as simple "
        "(linear) increase, (2000 − 500)/(500 × 20); 1.386 forgets to divide by t.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "direct",
    "Which of the following pairs consists of two NCERT examples of the SAME type of population interaction?",
    P("Clown fish living among the tentacles of a sea anemone; barnacles growing on the back of a whale",
      ["Cuscuta growing on hedge plants; lichens",
       "A fig and its pollinating wasp; cattle egrets foraging near grazing cattle",
       "Balanus and Chthamalus on the rocky coasts of Scotland; the monarch butterfly and the birds that avoid it"],
      "B"),
    "Classifying NCERT's examples of interactions",
    "NCERT: the clown fish gets protection from predators among the stinging tentacles of the sea anemone, which "
    "does not appear to derive any benefit; barnacles on a whale benefit while the whale derives no apparent "
    "benefit — both are commensalism. Cuscuta is a parasite while lichens are mutualism; the fig–wasp association "
    "is mutualism while cattle egrets and cattle are commensalism; Balanus and Chthamalus compete, while the "
    "monarch butterfly's distastefulness is a defence against predators.",
    ["Clown fish–anemone: commensalism", "Barnacle–whale: commensalism", "Other pairs mix two different "
     "interactions"],
    C12_OP("population interactions"),
    why="Each wrong pair mixes two interactions: parasitism with mutualism, mutualism with commensalism, and "
        "competition with predation.",
    seconds=45)

_n0 = 1000
assert _n0 + (50 + 40) - (70 + 0) > _n0          # deaths exceed births, yet density rises
assert _n0 + (60 + 25) - (60 + 25) == _n0         # B = D and I = E → unchanged

add(OAP, "Population growth", "Advanced", "statement_pair",
    sp("By N(t+1) = N(t) + [(B + I) − (D + E)], a population's density can increase during a period in which its "
       "deaths exceed its births.",
       "If, during a period, natality equals mortality and immigration equals emigration, the population "
       "density at the end of the period equals that at the start."),
    SP("A"),
    "Reading the population-density equation",
    "NCERT: population density changes through natality (B) and immigration (I), which increase it, and mortality "
    "(D) and emigration (E), which decrease it. Statement I: if D > B but immigration is large enough, B + I can "
    "still exceed D + E (e.g. N = 1000, B = 50, I = 40, D = 70, E = 0 → N(t+1) = 1020), so it is true. Statement "
    "II: if B = D and I = E, the bracket is zero and N(t+1) = N(t), so it is true.",
    ["Increase if (B + I) > (D + E), regardless of B versus D", "B = D and I = E → bracket = 0"],
    C12_OP("populations: population growth"),
    seconds=50, verified_by=RECOMPUTED)

# ================================================================ Ecosystem (4 / 5 / 4)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "In decomposition, decomposers break down complex organic matter into inorganic substances. According to "
    "NCERT, these inorganic substances are:",
    P("Carbon dioxide, water and nutrients",
      ["Glucose, amino acids and fatty acids", "Humus, lignin and chitin", "Methane, hydrogen sulphide and ammonia only"],
      "C"),
    "What decomposition produces",
    "NCERT: decomposers break down complex organic matter into inorganic substances like carbon dioxide, water and "
    "nutrients, and the process is called decomposition.",
    ["Complex organic matter → CO₂ + water + nutrients", "Process = decomposition"],
    C12_EC("decomposition"),
    why="Glucose, amino acids and fatty acids are organic; lignin and chitin are components of detritus that slow "
        "decomposition, and humus is an organic product of humification; NCERT does not give methane, H₂S and "
        "ammonia as the products of decomposition.",
    seconds=20)

add(ECO, "Energy flow", "Basic", "direct",
    "Based on the source of their nutrition or food, organisms occupy a specific place in the food chain. NCERT "
    "calls this place the organism's:",
    P("Trophic level", ["Standing crop", "Habitat", "Stratum"], "A"),
    "Definition of a trophic level",
    "NCERT: organisms occupy a place in the natural surroundings or in a community according to their feeding "
    "relationship with other organisms; based on the source of their nutrition or food, organisms occupy a "
    "specific place in the food chain that is known as their trophic level.",
    ["Place in a food chain by source of food = trophic level"],
    C12_EC("energy flow"),
    why="Standing crop is the mass of living material at a trophic level; habitat is where an organism lives; a "
        "stratum is a vertical layer of vegetation (stratification).",
    seconds=20)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "According to NCERT, the rate of biomass production is called:",
    P("Productivity", ["Standing crop", "Biomass", "Mineralisation"], "D"),
    "Productivity is a rate",
    "NCERT: a constant input of solar energy is the basic requirement for any ecosystem to function and sustain; "
    "the amount of biomass or organic matter produced per unit area over a time period by plants during "
    "photosynthesis is primary production, and the rate of biomass production is called productivity.",
    ["Biomass produced per unit area per unit time", "Rate of biomass production = productivity"],
    C12_EC("productivity"),
    why="Standing crop and biomass are amounts present at a given time, not rates; mineralisation is the release "
        "of inorganic nutrients from humus.",
    seconds=20)

add(ECO, "Energy flow", "Basic", "statement_pair",
    sp("All animals depend on plants, directly or indirectly, for their food needs; they are hence called "
       "consumers and also heterotrophs.",
       "Producers belong to the first trophic level, herbivores (primary consumers) to the second and carnivores "
       "(secondary consumers) to the third."),
    SP("A"),
    "Consumers and trophic levels",
    "NCERT: all animals depend on plants (directly or indirectly) for their food needs and are hence called "
    "consumers and also heterotrophs (Statement I true). It also states that the producers belong to the first "
    "trophic level, herbivores (primary consumers) to the second and carnivores (secondary consumers) to the third "
    "(Statement II true).",
    ["Animals = consumers = heterotrophs", "Producers 1st, herbivores 2nd, carnivores 3rd trophic level"],
    C12_EC("energy flow"),
    seconds=30)

add(ECO, "Productivity and decomposition", "Intermediate", "assertion_reason",
    ar("The earthworm is referred to as the farmer's 'friend'.",
       "Earthworms help in the breakdown of complex organic matter as well as in loosening of the soil."),
    AR("A"),
    "Why the earthworm helps the farmer",
    "NCERT opens its account of decomposition by noting that the earthworm is called the farmer's 'friend' because "
    "it helps in the breakdown of complex organic matter as well as in loosening of the soil. R gives exactly the "
    "reason for A.",
    ["Earthworm: breaks down complex organic matter", "Loosens the soil → farmer's friend"],
    C12_EC("decomposition"),
    seconds=25)

add(ECO, "Ecological pyramids", "Intermediate", "statement_pair",
    sp("NCERT's inverted pyramid of biomass shows a large standing crop of phytoplankton supporting a small "
       "standing crop of zooplankton.",
       "NCERT's upright pyramid of biomass shows a sharp decrease in biomass at higher trophic levels."),
    SP("D"),
    "Reading NCERT's pyramids of biomass",
    "NCERT's inverted pyramid of biomass is captioned as a small standing crop of phytoplankton supporting a large "
    "standing crop of zooplankton; it is inverted precisely because the producers' bar is the smaller one, so "
    "Statement I reverses it (false). The upright pyramid of biomass shows a sharp decrease in biomass at higher "
    "trophic levels (Statement II true).",
    ["Inverted: small phytoplankton crop supports a large zooplankton crop", "Upright: sharp decrease in biomass "
     "upwards"],
    C12_EC("ecological pyramids"),
    seconds=35)

add(ECO, "Structure and components", "Intermediate", "assertion_reason",
    ar("For study, ecologists divide the biosphere, regarded as a global ecosystem, into two basic categories: "
       "terrestrial and aquatic.",
       "The biosphere, a composite of all the local ecosystems on Earth, is too big and complex to be studied at "
       "one time."),
    AR("A"),
    "Why ecosystems are divided into categories",
    "NCERT: some ecologists regard the entire biosphere as a global ecosystem, a composite of all local "
    "ecosystems on Earth. Since this system is too much big and complex to be studied at one time, it is "
    "convenient to divide it into two basic categories, namely the terrestrial and the aquatic. R is the stated "
    "reason for A.",
    ["Biosphere = global ecosystem", "Too big and complex → divided into terrestrial and aquatic"],
    C12_EC("ecosystem – structure and function"),
    seconds=30)

add(ECO, "Energy flow", "Intermediate", "match_list",
    ml(("organism named in NCERT", "its role as described in NCERT"),
       ["Cockroach", "Earthworm", "Molluscs", "Phytoplankton"],
       ["Producer of an aquatic ecosystem",
        "Detritivore that breaks detritus into smaller particles",
        "Common herbivore of an aquatic ecosystem",
        "Omnivore, through which the detritus and grazing food chains may be connected"]),
    M(mc("IV,II,III,I"), [mc("IV,III,II,I"), mc("II,IV,III,I"), mc("IV,II,I,III")], "B"),
    "Roles of organisms in the ecosystem",
    "NCERT: the DFC may be connected with the GFC at some levels, and some animals like cockroaches and crows are "
    "omnivores (A-IV). Detritivores such as the earthworm break down detritus into smaller particles "
    "(fragmentation) (B-II). Common herbivores are insects, birds and mammals on land and molluscs in water "
    "(C-III). The producers of an aquatic ecosystem are phytoplankton, some algae and higher plants (D-I).",
    ["Cockroach → omnivore", "Earthworm → detritivore", "Molluscs → aquatic herbivore",
     "Phytoplankton → aquatic producer"],
    C12_EC("energy flow; decomposition"),
    why="The wrong codes make the earthworm an aquatic herbivore or an omnivore, or make molluscs producers and "
        "phytoplankton herbivores.",
    seconds=40)

add(ECO, "Energy flow", "Intermediate", "multi_statement",
    ms("NCERT gives Grass → Goat → Man as an example of a grazing food chain. Which of the following statements "
       "about this chain are correct?",
       ["Grass is the producer and belongs to the first trophic level.",
        "The goat is a herbivore, i.e. a primary consumer at the second trophic level.",
        "Man is a primary carnivore, i.e. a secondary consumer at the third trophic level.",
        "The goat is a primary carnivore because it is eaten by man.",
        "Man receives more energy than the grass fixes, because man is at the top of the chain."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "D"),
    "Trophic levels in NCERT's grazing food chain",
    "Grass produces food by photosynthesis (first trophic level). The goat feeds on the grass, so it is a "
    "herbivore or primary consumer (second level). Man eats the goat, which eats plants, so man is a primary "
    "carnivore or secondary consumer (third level). Being eaten does not make the goat a carnivore (d false). "
    "Energy decreases at successive trophic levels, so man receives far less than the grass fixes (e false).",
    ["Grass: producer, level 1", "Goat: herbivore, level 2", "Man: primary carnivore, level 3",
     "Energy decreases upwards"],
    C12_EC("energy flow"),
    why="(d) confuses being eaten with eating animals, and (e) reverses the decrease of energy at successive "
        "trophic levels; every option with (d) or (e) is wrong.",
    seconds=45)

add(ECO, "Structure and components", "Advanced", "multi_statement",
    ms("A home aquarium contains water plants and algae, snails that graze on the algae, small fish that eat the "
       "snails, and bacteria and fungi in the gravel that break down fish waste and dead leaves. Using NCERT, "
       "which of the following statements are correct?",
       ["An aquarium is an example of a man-made ecosystem.",
        "The snails grazing on the algae are primary consumers.",
        "The bacteria and fungi in the gravel are decomposers (saprotrophs).",
        "The heat released by the respiring fish is captured by the plants and reused in photosynthesis.",
        "The small fish that eat the snails are secondary consumers (primary carnivores)."]),
    MS(["a", "b", "c", "e"], [["a", "b", "c", "d"], ["a", "b", "e"], ["b", "c", "d", "e"]], "B"),
    "Applying ecosystem components to an aquarium",
    "NCERT names crop fields and an aquarium as man-made ecosystems (a). Herbivores (molluscs, in water) feeding "
    "on producers are primary consumers (b); animals feeding on herbivores are primary carnivores or secondary "
    "consumers (e). Fungi and bacteria that secrete enzymes to break down dead and waste materials are decomposers, "
    "also called saprotrophs (c). Energy flow is unidirectional, and the energy released as heat is lost to the "
    "environment, not reused by producers (d false).",
    ["Aquarium: man-made", "Snails: primary consumers; small fish: primary carnivores",
     "Gravel microbes: saprotrophs", "Heat is lost, not recycled"],
    C12_EC("ecosystem – structure and function; energy flow"),
    why="Options with (d) treat energy as cycling back to the producers; '(a), (b) and (e) only' leaves out the "
        "decomposers (c).",
    seconds=60)

add(ECO, "Productivity and decomposition", "Advanced", "multi_statement",
    ms("In a field experiment, all earthworms and other detritivores are removed from one plot of leaf litter, "
       "while bacteria, fungi, rain and soil are left unchanged. Using NCERT's account of decomposition, which of "
       "the following statements about this plot are correct?",
       ["Fragmentation of the detritus into smaller particles would be reduced.",
        "Leaching of water-soluble inorganic nutrients into the soil can still occur.",
        "Catabolism of the detritus by bacterial and fungal enzymes can still occur.",
        "Catabolism would stop, because earthworms secrete the enzymes that degrade detritus into inorganic "
        "substances.",
        "Leaching would stop, because detritivores are the agents that carry nutrients down the soil horizon."]),
    MS(["a", "b", "c"], [["a", "d", "e"], ["a", "b", "c", "d"], ["b", "c", "e"]], "A"),
    "Agents of the steps of decomposition",
    "NCERT: detritivores (e.g. earthworm) break down detritus into smaller particles — fragmentation — so removing "
    "them reduces it (a). By leaching, water-soluble inorganic nutrients go down into the soil horizon; this is "
    "done by water, not by detritivores (b true, e false). Bacterial and fungal enzymes degrade detritus into "
    "simpler inorganic substances — catabolism — so it continues with the microbes present (c true, d false).",
    ["Fragmentation: detritivores", "Leaching: water", "Catabolism: bacterial and fungal enzymes"],
    C12_EC("decomposition"),
    why="(d) gives catabolism to earthworms and (e) gives leaching to detritivores; NCERT assigns catabolism to "
        "bacterial and fungal enzymes and leaching to water.",
    seconds=60)

add(ECO, "Ecological pyramids", "Advanced", "assertion_reason",
    ar("In NCERT's pyramid of numbers for a grassland, only three top carnivores are supported by an ecosystem "
       "based on the production of nearly six million plants.",
       "Ecological pyramids assume a simple food chain, something that almost never exists in nature, and do not "
       "accommodate a food web."),
    AR("B"),
    "Pyramid of numbers versus the limitations of pyramids",
    "A is NCERT's caption for the grassland pyramid of numbers; the steep fall in numbers results from the loss of "
    "energy at each transfer (only about 10 per cent passes to the next level). R is one of NCERT's stated "
    "limitations of ecological pyramids — true, but it describes a shortcoming of the method, not why so few top "
    "carnivores are supported.",
    ["A: ~6 million plants support 3 top carnivores (true)", "R: limitation of pyramids (true)",
     "R does not explain A"],
    C12_EC("ecological pyramids"),
    seconds=45)

add(ECO, "Productivity and decomposition", "Advanced", "match_list",
    ml(("observation", "explanation given in NCERT"),
       ["Organic matter builds up in cold, waterlogged soil",
        "The net primary productivity of a field is less than its gross primary productivity",
        "The pyramid of biomass in a sea is generally inverted",
        "The pyramid of energy of any ecosystem is upright"],
       ["Some energy is always lost as heat at each step of energy flow",
        "The biomass of fishes far exceeds that of the phytoplankton",
        "A considerable amount of GPP is utilised by plants in respiration",
        "Low temperature and anaerobiosis inhibit decomposition"]),
    M(mc("IV,III,II,I"), [mc("IV,II,III,I"), mc("III,IV,II,I"), mc("IV,III,I,II")], "D"),
    "Linking observations to NCERT's explanations",
    "NCERT: low temperature and anaerobiosis inhibit decomposition, resulting in build-up of organic materials "
    "(A-IV). A considerable amount of GPP is utilised by plants in respiration, and GPP minus respiration losses is "
    "NPP (B-III). The pyramid of biomass in sea is generally inverted because the biomass of fishes far exceeds "
    "that of phytoplankton (C-II). The pyramid of energy is always upright because some energy is always lost as "
    "heat at each step (D-I).",
    ["Cold, waterlogged → slow decomposition", "NPP < GPP → respiration", "Sea biomass pyramid → fish > "
     "phytoplankton", "Energy pyramid upright → heat loss"],
    C12_EC("productivity; decomposition; ecological pyramids"),
    why="The wrong codes swap the explanations of the two pyramids, or of NPP and the decomposition build-up.",
    seconds=50)

# ================================================================ Biodiversity and Conservation (4 / 5 / 4)

add(BDC, "In situ and ex situ conservation", "Basic", "direct",
    "The historic Convention on Biological Diversity ('The Earth Summit'), which called upon all nations to take "
    "appropriate measures for the conservation of biodiversity and the sustainable utilisation of its benefits, "
    "was held in 1992 in:",
    P("Rio de Janeiro", ["Johannesburg", "Stockholm", "Kyoto"], "A"),
    "International efforts for conservation",
    "NCERT: biodiversity knows no political boundaries, and its conservation is a collective responsibility of "
    "all nations. The historic Convention on Biological Diversity ('The Earth Summit') held in Rio de Janeiro in "
    "1992 called upon all nations to take appropriate measures for conservation of biodiversity and sustainable "
    "utilisation of its benefits. The follow-up World Summit on Sustainable Development was held in 2002 in "
    "Johannesburg, South Africa.",
    ["Earth Summit: Rio de Janeiro, 1992", "World Summit on Sustainable Development: Johannesburg, 2002"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity?"),
    why="Johannesburg hosted the 2002 World Summit on Sustainable Development; NCERT names neither Stockholm nor "
        "Kyoto as the venue of a biodiversity convention.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "Discussing habitat loss and fragmentation, NCERT notes that besides the total loss of habitats, the survival "
    "of many species is also threatened by:",
    P("The degradation of many habitats by pollution",
      ["The setting up of national parks and sanctuaries", "The keeping of threatened animals in zoological parks",
       "The strict protection of biodiversity hotspots"], "C"),
    "Habitat degradation",
    "NCERT: habitat loss and fragmentation is the most important cause driving animals and plants to extinction "
    "(e.g. the clearing of tropical rain forests). Besides total loss, the degradation of many habitats by "
    "pollution also threatens the survival of many species.",
    ["Total habitat loss", "Plus degradation of habitats by pollution"],
    C12_BD("loss of biodiversity: causes of biodiversity losses"),
    why="National parks, sanctuaries, zoological parks and the protection of hotspots are means of conservation, "
        "not threats to survival.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "NCERT lists some recent extinctions of animals. Which of the following is NOT among them?",
    P("The Indian one-horned rhinoceros", ["The dodo of Mauritius", "The quagga of Africa",
                                           "The thylacine of Australia"], "D"),
    "Recent extinctions",
    "NCERT: some examples of recent extinctions include the dodo (Mauritius), quagga (Africa), thylacine "
    "(Australia), Steller's sea cow (Russia) and three subspecies (Bali, Javan, Caspian) of tiger. The Indian "
    "one-horned rhinoceros is not in this list.",
    ["Dodo – Mauritius", "Quagga – Africa", "Thylacine – Australia", "Steller's sea cow – Russia",
     "Tiger subspecies – Bali, Javan, Caspian"],
    C12_BD("loss of biodiversity"),
    why="The dodo, quagga and thylacine are all in NCERT's list of recent extinctions.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "Pollination of plants by bees, bumblebees, birds and bats, without which plants cannot give us fruits or "
    "seeds, is an ecosystem service that NCERT uses to illustrate the:",
    P("Broadly utilitarian argument for conserving biodiversity",
      ["Narrowly utilitarian argument for conserving biodiversity", "Ethical argument for conserving biodiversity",
       "Idea of bioprospecting"], "B"),
    "Arguments for conservation",
    "NCERT: the broadly utilitarian argument says that biodiversity plays a major role in many ecosystem services "
    "that nature provides, such as pollination (without which plants cannot give us fruits or seeds) by bees, "
    "bumblebees, birds and bats, and aesthetic pleasures.",
    ["Ecosystem services (pollination, aesthetic pleasure) → broadly utilitarian"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity?"),
    why="The narrowly utilitarian argument concerns direct economic products (food, firewood, fibre, drugs); the "
        "ethical argument concerns the intrinsic value of every species; bioprospecting is the search for "
        "products of economic importance.",
    seconds=25)

add(BDC, "Patterns of biodiversity", "Intermediate", "match_list",
    ml(("example given in NCERT", "concept it illustrates"),
       ["More than 50,000 genetically different strains of rice in India",
        "A greater amphibian species diversity in the Western Ghats than in the Eastern Ghats",
        "The extinction of more than 200 species of cichlid fish in Lake Victoria",
        "Industrial products such as tannins, lubricants, dyes, resins and perfumes obtained from nature"],
       ["Narrowly utilitarian argument for conservation", "Alien species invasion", "Species diversity",
        "Genetic diversity"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("IV,II,III,I")], "D"),
    "Linking NCERT examples to concepts",
    "NCERT: India has more than 50,000 genetically different strains of rice (genetic diversity, A-IV). The "
    "Western Ghats have a greater amphibian species diversity than the Eastern Ghats (species diversity, B-III). "
    "The introduction of the Nile perch into Lake Victoria led to the extinction of more than 200 cichlid species "
    "(alien species invasion, C-II). Industrial products such as tannins, lubricants, dyes, resins and perfumes "
    "are among the direct economic benefits of the narrowly utilitarian argument (D-I).",
    ["Rice strains → genetic", "Ghats amphibians → species", "Cichlids → alien invasion",
     "Industrial products → narrowly utilitarian"],
    C12_BD("biodiversity; loss of biodiversity; biodiversity conservation"),
    why="The wrong codes swap genetic with species diversity, the alien invasion with the utilitarian argument, "
        "or species diversity with alien invasion.",
    seconds=45)

add(BDC, "Importance and loss", "Intermediate", "assertion_reason",
    ar("Careful analysis of records shows that extinctions across taxa are not random, and some groups such as "
       "amphibians appear to be more vulnerable to extinction.",
       "Among animals, insects are the most species-rich taxonomic group, making up more than 70 per cent of the "
       "total."),
    AR("B"),
    "Vulnerability to extinction versus species richness",
    "Both are NCERT statements: extinctions across taxa are not random, and amphibians appear more vulnerable "
    "(A true); insects are the most species-rich animal group, more than 70 per cent of animals (R true). The "
    "species richness of insects says nothing about why amphibians are more vulnerable, so R does not explain A.",
    ["A: amphibians more vulnerable (true)", "R: insects most species-rich (true)", "Unrelated → option B"],
    C12_BD("biodiversity: how many species are there on earth; loss of biodiversity"),
    seconds=30)

add(BDC, "Importance and loss", "Intermediate", "multi_statement",
    ms("Paul Ehrlich's 'rivet popper hypothesis' uses an analogy to explain the contribution of species richness "
       "to ecosystem well-being. Which of the following statements about it are correct?",
       ["In the analogy, the ecosystem is an airplane and the species are the rivets joining its parts.",
        "Removing rivets may not affect flight safety initially, but as more are removed the plane becomes "
        "dangerously weak.",
        "Which rivet is removed may also be critical.",
        "Loss of rivets on the wings stands for the loss of key species that drive major ecosystem functions.",
        "Loss of a few rivets on the seats or windows inside the plane is a more serious threat to flight safety "
        "than loss of rivets on the wings."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "b", "d"], ["b", "c", "d", "e"]], "C"),
    "The rivet popper hypothesis",
    "NCERT: in an airplane (ecosystem) all parts are joined together using thousands of rivets (species). If "
    "every passenger pops a rivet to take home (causing a species to become extinct), it may not affect flight "
    "safety (proper functioning of the ecosystem) initially, but as more rivets are removed the plane becomes "
    "dangerously weak over time (a, b). Which rivet is removed may also be critical (c): loss of rivets on the "
    "wings (key species that drive major ecosystem functions) is obviously a more serious threat to flight safety "
    "than loss of a few rivets on the seats or windows inside the plane (d true, e false).",
    ["Airplane = ecosystem; rivets = species", "Gradual weakening", "Wing rivets = key species"],
    C12_BD("patterns of biodiversity: the importance of species diversity to the ecosystem"),
    why="(e) reverses NCERT's comparison of wing rivets with seat and window rivets; '(a), (b) and (d) only' "
        "leaves out (c), which NCERT states.",
    seconds=50)

add(BDC, "In situ and ex situ conservation", "Intermediate", "assertion_reason",
    ar("Zoological parks are a means of ex situ conservation.",
       "Zoological parks maintain only those animal species that are still common in the wild."),
    AR("C"),
    "Zoos and ex situ conservation",
    "NCERT: in ex situ conservation, threatened animals and plants are taken out of their natural habitat and "
    "placed in special settings; zoological parks, botanical gardens and wildlife safari parks serve this purpose "
    "(A true). NCERT adds that many animals that have become extinct in the wild continue to be maintained in "
    "zoological parks, so R is false.",
    ["Zoo = ex situ", "Zoos keep even species extinct in the wild"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity?"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Intermediate", "statement_pair",
    sp("During his explorations of South American jungles, Alexander von Humboldt observed that within a region, "
       "species richness increases with increasing explored area, but only up to a limit.",
       "Plotted on a logarithmic scale, the relationship between species richness and area is a curve (a "
       "rectangular hyperbola) rather than a straight line."),
    SP("C"),
    "Species–area relationship",
    "NCERT: Humboldt observed that within a region species richness increased with increasing explored area, but "
    "only up to a limit (Statement I true). The relation between species richness and area turns out to be a "
    "rectangular hyperbola for a wide variety of taxa; on a logarithmic scale it is a straight line described by "
    "log S = log C + Z log A (Statement II false).",
    ["Richness rises with area, up to a limit", "Linear axes: rectangular hyperbola; log axes: straight line"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    seconds=35)

add(BDC, "In situ and ex situ conservation", "Advanced", "assertion_reason",
    ar("Seed banks are a means of in situ conservation, because they preserve plants for long periods.",
       "Seeds of different genetic strains of commercially important plants can be kept for long periods in seed "
       "banks."),
    AR("D"),
    "Seed banks are ex situ",
    "NCERT: in ex situ conservation, threatened plants and animals are taken out of their natural habitat and "
    "placed in special settings; in recent years this has advanced beyond keeping species, and seeds of different "
    "genetic strains of commercially important plants can be kept for long periods in seed banks (R true). Seeds "
    "kept in a seed bank are outside their natural habitat, so seed banks are ex situ, not in situ (A false). In "
    "situ conservation protects species in their natural habitat, as in biosphere reserves, national parks, "
    "sanctuaries and sacred groves.",
    ["Seed bank: storage outside the habitat → ex situ (A false)", "Long-term storage of seed strains (R true)"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity?"),
    seconds=35)
add(BDC, "Importance and loss", "Advanced", "direct",
    "Three people value a tropical forest for different reasons: (i) a company screens the forest's plants for "
    "molecules of medicinal value; (ii) a trekker enjoys waking up to the song of a bulbul in the forest; (iii) "
    "a philosopher argues that even a species of no known use has an intrinsic value and must be protected. "
    "Using NCERT's arguments for conserving biodiversity, these are, respectively:",
    P("Narrowly utilitarian (bioprospecting); broadly utilitarian; ethical",
      ["Broadly utilitarian; narrowly utilitarian; ethical",
       "Narrowly utilitarian (bioprospecting); ethical; broadly utilitarian",
       "Ethical; broadly utilitarian; narrowly utilitarian"], "A"),
    "Classifying the arguments for conservation",
    "NCERT: the narrowly utilitarian argument rests on direct economic benefits, including products of medicinal "
    "value; exploring molecular, genetic and species-level diversity for products of economic importance is "
    "bioprospecting (i). The broadly utilitarian argument covers ecosystem services, including aesthetic "
    "pleasures such as waking up to the song of a bulbul (ii). The ethical argument holds that every species has "
    "an intrinsic value even if it is not of current economic value to us (iii).",
    ["Medicinal screening → narrowly utilitarian (bioprospecting)", "Bulbul's song → broadly utilitarian "
     "(aesthetic)", "Intrinsic value → ethical"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity?"),
    why="The wrong options swap the narrowly and broadly utilitarian arguments, or the broadly utilitarian and "
        "ethical arguments.",
    seconds=50)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Which of the following NCERT examples are correctly paired with a cause of biodiversity loss from the "
       "'Evil Quartet'?",
       ["Many marine fish populations around the world being over-harvested: over-exploitation",
        "Tropical rain forests shrinking from more than 14 per cent to no more than 6 per cent of the earth's "
        "land surface: habitat loss and fragmentation",
        "The spread of carrot grass (Parthenium), Lantana and water hyacinth (Eichhornia): alien species "
        "invasions",
        "In a coevolved plant–pollinator mutualism, the extinction of one partner leading to that of the other: "
        "co-extinction",
        "The extinction of Steller's sea cow and the passenger pigeon: co-extinction"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "b", "d"], ["b", "c", "d", "e"]], "B"),
    "Applying the Evil Quartet",
    "NCERT: many marine fish populations are over-harvested (over-exploitation, a). Tropical rain forests once "
    "covering more than 14 per cent of the land surface now cover no more than 6 per cent (habitat loss, b). "
    "Carrot grass, Lantana and water hyacinth are invasive weed species that threaten native species "
    "(alien species invasions, c). In a coevolved plant–pollinator mutualism, the extinction of one invariably "
    "leads to the extinction of the other (co-extinction, d). Steller's sea cow and the passenger pigeon became "
    "extinct due to over-exploitation by humans, not co-extinction (e false).",
    ["Fish over-harvesting → over-exploitation", "Rain forest shrinkage → habitat loss",
     "Parthenium, Lantana, Eichhornia → alien invasion", "Plant–pollinator → co-extinction",
     "Sea cow, passenger pigeon → over-exploitation"],
    C12_BD("loss of biodiversity: causes of biodiversity losses"),
    why="(e) misattributes over-exploitation to co-extinction; '(a), (b) and (d) only' leaves out the invasive "
        "weeds (c).",
    seconds=60)

add(BDC, "Patterns of biodiversity", "Advanced", "direct",
    "Working within a single region, an ecologist finds the slope Z of the species–area line (log S = log C + "
    "Z log A) to be 0.15 for birds. Another ecologist studies molluscs in the same way within a different region. "
    "On the basis of NCERT, the Z value expected for the molluscs is:",
    P("Also in the range 0.1 to 0.2, since within a region Z is amazingly similar regardless of the taxonomic "
      "group or the region",
      ["In the range 0.6 to 1.2, since molluscs are a different taxonomic group from birds",
       "About 1.15, the value NCERT gives for frugivorous animals",
       "Unpredictable, since Z depends entirely on the taxonomic group studied"], "A"),
    "Constancy of Z within a region",
    "NCERT: ecologists have discovered that the value of Z lies in the range of 0.1 to 0.2 regardless of the "
    "taxonomic group or the region (whether it is the plants in Britain, birds in California or molluscs in New "
    "York state). Z becomes much steeper (0.6 to 1.2) only when very large areas such as entire continents are "
    "analysed; 1.15 is NCERT's value for frugivorous birds and mammals in the tropical forests of different "
    "continents.",
    ["Within a region: Z = 0.1–0.2 for any group", "Continents: 0.6–1.2", "Frugivores across continents: 1.15"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    why="0.6–1.2 and 1.15 apply to very large areas (continents), not to studies within a region; NCERT stresses "
        "that within-region Z does NOT depend on the taxonomic group.",
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
    have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
    assert have == quota, {k: (have[k], quota[k]) for k in set(have) | set(quota) if have[k] != quota[k]}
    assert len(QUESTIONS) == pkg["count"] == 125, len(QUESTIONS)
    assert [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]] == pkg["question_ids"]
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "BATCH_010 package BOT_010_p2: 125 original Botany questions (Sexual Reproduction in Flowering "
                    "Plants to Biodiversity and Conservation), each with an NCERT reference. Facts tested in "
                    "BATCH_000 to BATCH_009 were avoided or approached from a new angle. Numerical and other "
                    "computable answers re-derived by tools/batch_010/BOT_010_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()
