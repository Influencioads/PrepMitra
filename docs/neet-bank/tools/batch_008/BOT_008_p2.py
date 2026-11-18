"""Builder for BATCH_008, package BOT_008_p2 (Botany, NEET_BOT_001881..NEET_BOT_002000, 120 questions).

Topics: Sexual Reproduction in Flowering Plants; Principles of Inheritance and Variation; Molecular Basis of
Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem; Biodiversity and Conservation.
All questions are original and every fact is taken from the rationalised NCERT Class 12 Biology textbook. Facts
already tested in BATCH_000 to BATCH_007 on these topics were avoided or approached from a new angle (see
`python tools/merge_batch.py stems 008 BOT_008_p2`). Computable answers are re-derived below; the file is written
only if every assert, the plan quota, the format mix and the answer-key balance pass.

    cd docs/neet-bank && python tools/batch_008/BOT_008_p2.py
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
PACKAGE = "BOT_008_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_008_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_008_BOT_p2.json"
FIRST_ID = 1881

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


def mc(s):
    """'III,IV,I,II' -> {'A': 'III', 'B': 'IV', 'C': 'I', 'D': 'II'}"""
    return dict(zip("ABCD", s.split(",")))


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

# ================================================================ Sexual Reproduction in Flowering Plants (6 / 9 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "In the gynoecium of a flower, NCERT describes structures that arise from the placenta and are the "
    "megasporangia. These megasporangia are commonly called:",
    P("Ovules", ["Ovaries", "Embryo sacs", "Locules"], "A"),
    "The ovule is the megasporangium",
    "NCERT: inside the ovary is the ovarian cavity (locule); the placenta is located inside it, and arising from "
    "the placenta are the megasporangia, commonly called ovules. The embryo sac (female gametophyte) lies inside "
    "the nucellus of the ovule, so it is not the sporangium itself.",
    ["Ovary → locule → placenta", "Megasporangia arise from the placenta", "Megasporangia = ovules"],
    C12_SR("pre-fertilisation: the pistil, megasporangium (ovule) and embryo sac"),
    why="The ovary encloses the ovules, the locule is the ovarian cavity, and the embryo sac is the female "
        "gametophyte formed inside the ovule.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "In transverse section, a typical angiosperm anther is a four-sided (tetragonal) structure. Where are its "
    "microsporangia located?",
    P("At the four corners, two in each lobe",
      ["All four in the centre, around the connective", "One at each corner of a single lobe, the other lobe being "
       "sterile", "Two at the corners and two along the middle of the anther"], "C"),
    "Arrangement of microsporangia in an anther",
    "NCERT: the anther is a four-sided (tetragonal) structure consisting of four microsporangia located at the "
    "corners, two in each lobe. This fits the bilobed, dithecous anther: each lobe has two theca, and each theca "
    "contains one microsporangium.",
    ["Bilobed, dithecous anther", "Four microsporangia", "At the corners, two in each lobe"],
    C12_SR("pre-fertilisation: stamen, microsporangium and pollen grain"),
    why="NCERT places the microsporangia at the corners, not in the centre, and both lobes are fertile, with two "
        "microsporangia each.",
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "The nucleus of the functional megaspore divides mitotically to form two nuclei. According to NCERT, these two "
    "nuclei:",
    P("Move to the opposite poles, forming the 2-nucleate embryo sac",
      ["Fuse with each other to form a diploid nucleus", "Move to the opposite poles, and a cell wall is laid down "
       "between them at once", "Both remain at the micropylar end and directly form the egg apparatus"], "B"),
    "Early development of the embryo sac",
    "NCERT: the nucleus of the functional megaspore divides mitotically to form two nuclei, which move to the "
    "opposite poles, forming the 2-nucleate embryo sac. Two more sequential mitotic nuclear divisions give the "
    "4-nucleate and then the 8-nucleate stages. These divisions are strictly free nuclear: cell walls are laid "
    "down only after the 8-nucleate stage.",
    ["First mitosis → two nuclei", "They move to opposite poles", "2-nucleate embryo sac; walls come only after "
     "the 8-nucleate stage"],
    C12_SR("pre-fertilisation: female gametophyte"),
    why="The nuclei do not fuse; no wall forms at this stage because the divisions are free nuclear; and the egg "
        "apparatus is organised only after the 8-nucleate stage.",
    seconds=25)

add(SRFP, "Pollination", "Basic", "direct",
    "Plants such as Viola, Oxalis and Commelina bear cleistogamous flowers, which do not open at all. How does "
    "pollination take place in these flowers?",
    P("The anthers dehisce in the flower buds, and the pollen grains come in contact with the stigma",
      ["Insects carry pollen to them from the chasmogamous flowers of the same plant",
       "Wind carries pollen from other plants through small openings in the petals",
       "Pollen grains are carried by water to the stigma after the bud is submerged"], "D"),
    "Pollination in cleistogamous flowers",
    "NCERT: in cleistogamous flowers the anthers and stigma lie close to each other. When the anthers dehisce in "
    "the flower buds, the pollen grains come in contact with the stigma to effect pollination. Such flowers are "
    "invariably autogamous, since there is no chance of cross-pollen landing on the stigma.",
    ["Flower never opens", "Anthers and stigma lie close together", "Anthers dehisce inside the bud → autogamy"],
    C12_SR("pollination: kinds of pollination (autogamy)"),
    why="A closed flower cannot receive pollen from insects, wind or water; that is why cleistogamous flowers are "
        "invariably autogamous.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "statement_pair",
    sp("As the ovules mature into seeds, the ovary develops into a fruit; the transformation of ovules into seeds "
       "and of the ovary into a fruit proceeds simultaneously.",
       "Most fruits develop only from the ovary and are called true fruits."),
    SP("A"),
    "Seed and fruit formation; true fruits",
    "NCERT: as ovules mature into seeds, the ovary develops into a fruit, i.e. the transformation of ovules into "
    "seeds and ovary into fruit proceeds simultaneously (Statement I true). In a few species such as apple, "
    "strawberry and cashew, the thalamus also contributes to the fruit (false fruits); most fruits, however, develop "
    "only from the ovary and are called true fruits (Statement II true).",
    ["Statement I: true (simultaneous)", "Statement II: true (true fruits from the ovary only)"],
    C12_SR("post-fertilisation: seed and fruit"),
    seconds=30)

add(SRFP, "Pollination", "Basic", "assertion_reason",
    ar("It is believed that the distribution of some bryophytes and pteridophytes is limited.",
       "In these plants, water is needed for the transport of the male gametes and for fertilisation."),
    AR("A"),
    "Water and the male gametes of lower plants",
    "NCERT contrasts the rarity of water pollination in flowering plants with lower plant groups (algae, "
    "bryophytes and pteridophytes), in which water is a regular mode of transport for the male gametes. It states "
    "that, particularly for some bryophytes and pteridophytes, their distribution is believed to be limited because "
    "of the need for water for the transport of male gametes and fertilisation. R is the very reason given for A.",
    ["A: true (NCERT)", "R: true (water carries the male gametes)", "R is the stated cause of A"],
    C12_SR("pollination: agents of pollination (water)"),
    seconds=35)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "direct",
    "NCERT describes two ways in which apomictic seeds may develop. Which of them does it say happens more often?",
    P("Some nucellar cells surrounding the embryo sac start dividing, protrude into the embryo sac and develop into "
      "embryos, as in many Citrus and mango varieties",
      ["A diploid egg cell is formed without reduction division and develops into the embryo without fertilisation",
       "The primary endosperm cell develops into an embryo instead of an endosperm",
       "A synergid is fertilised by the second male gamete and develops into an extra embryo"], "C"),
    "Ways of developing apomictic seeds",
    "NCERT: there are several ways of development of apomictic seeds. In some species, the diploid egg cell is "
    "formed without reduction division and develops into the embryo without fertilisation. More often, as in many "
    "Citrus and mango varieties, some of the nucellar cells surrounding the embryo sac start dividing, protrude into "
    "the embryo sac and develop into embryos; in such species each ovule contains many embryos.",
    ["Way 1 ('in some species'): unreduced diploid egg → embryo", "Way 2 ('more often'): nucellar cells → embryos",
     "Example of way 2: Citrus, mango"],
    C12_SR("apomixis and polyembryony"),
    why="The unreduced-egg route is described for 'some species', not as the commoner route; NCERT gives no "
        "apomixis from the primary endosperm cell or from a fertilised synergid.",
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "statement_pair",
    sp("Following compatible pollination, the contents of the pollen grain move into the pollen tube, which grows "
       "through the tissues of the stigma and style and reaches the ovary.",
       "The pollen tube can emerge from any point on the pollen grain, because sporopollenin forms a continuous "
       "layer over the whole exine."),
    SP("C"),
    "Germination of the pollen grain on the stigma",
    "NCERT: following compatible pollination, the pollen grain germinates on the stigma to produce a pollen tube "
    "through one of the germ pores; the contents of the pollen grain move into the pollen tube, which grows through "
    "the tissues of the stigma and style and reaches the ovary (Statement I true). The exine has prominent "
    "apertures, the germ pores, where sporopollenin is absent; the tube emerges through one of them, not from any "
    "point (Statement II false).",
    ["Statement I: true", "Germ pores: sporopollenin absent", "Tube emerges through a germ pore → Statement II "
     "false"],
    C12_SR("pollination: pollen-pistil interaction"),
    seconds=35)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "multi_statement",
    ms("Compare microsporogenesis and megasporogenesis in a typical flowering plant. Which of the following "
       "statements are correct?",
       ["In both, a diploid spore mother cell divides by meiosis to give four haploid spores.",
        "All four microspores of a tetrad normally develop into pollen grains, whereas in a majority of flowering "
        "plants only one of the four megaspores is functional.",
        "Both the male and the female gametophyte develop from a haploid spore by mitotic division.",
        "The pollen mother cell is differentiated in the micropylar region of the nucellus.",
        "The four megaspores dissociate from each other as the anther dehydrates."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Spore formation and gametophyte development compared",
    "(a) True: a pollen mother cell gives a microspore tetrad by meiosis, and the megaspore mother cell gives four "
    "megaspores by meiosis. (b) True: as the anthers mature, the microspores dissociate and develop into pollen "
    "grains, while in most flowering plants one megaspore is functional and three degenerate. (c) True: the "
    "microspore nucleus divides mitotically to form the vegetative and generative cells, and the functional "
    "megaspore nucleus divides mitotically to form the embryo sac. (d) False: it is the megaspore mother cell that "
    "is differentiated in the micropylar region of the nucellus. (e) False: it is the microspores that dissociate "
    "as the anther dehydrates.",
    ["Meiosis in both (a)", "4 pollen grains vs 1 functional megaspore (b)", "Gametophytes by mitosis (c)",
     "(d), (e): male and female features swapped"],
    C12_SR("pre-fertilisation: microsporogenesis, megasporogenesis and the female gametophyte"),
    why="Options with (d) or (e) include a male feature given to the female side or the reverse; '(b), (c) and (e)' "
        "also leaves out the true statement (a).",
    seconds=55)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "In an artificial hybridisation experiment with a female parent bearing bisexual flowers, a worker removes the "
    "anthers only after they have dehisced. Why is this a mistake, according to the logic of NCERT's procedure?",
    P("Pollen of the same flower may already have reached the stigma, so some seeds may come from self-pollination "
      "instead of the desired cross",
      ["Anthers that have dehisced can no longer be removed with forceps",
       "Dehisced anthers secrete chemicals that make the stigma permanently non-receptive",
       "Emasculation is never needed in bisexual flowers, so the worker should not have removed the anthers"], "D"),
    "Purpose of emasculation before anther dehiscence",
    "NCERT: in crossing experiments it is important that only the desired pollen grains are used and the stigma is "
    "protected from contamination. If the female parent bears bisexual flowers, the anthers are removed from the "
    "flower bud before the anther dehisces (emasculation), and the flower is then bagged. Once the anthers have "
    "dehisced, the flower's own pollen may already have contaminated the stigma, defeating the purpose.",
    ["Goal: only the desired pollen on the stigma", "Own anthers → self-pollen", "Remove them in the bud, before "
     "dehiscence"],
    C12_SR("pollination: artificial hybridisation"),
    why="The problem is contamination, not difficulty of removal or a chemical effect; and emasculation is exactly "
        "what NCERT requires for bisexual flowers.",
    seconds=40)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("Wind-pollinated flowers often have a large, often feathery stigma.",
       "A large, feathery stigma can easily trap air-borne pollen grains."),
    AR("A"),
    "Adaptations of wind-pollinated flowers",
    "NCERT: wind-pollinated flowers often have well-exposed stamens (so that pollen is easily dispersed into wind "
    "currents) and a large, often feathery stigma to easily trap air-borne pollen grains. Since wind carries pollen "
    "at random, a large trapping surface raises the chance that pollen lands on the stigma. R gives the function "
    "for which the feature in A exists.",
    ["A: true", "R: true, the purpose of the feathery stigma", "R explains A"],
    C12_SR("pollination: agents of pollination (wind)"),
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "multi_statement",
    ms("Consider where reserve food is found in mature seeds of the plants named in NCERT. Which of the following "
       "statements are correct?",
       ["In a mature pea seed, the endosperm has been consumed, and the food reserves lie in the thick, swollen "
        "cotyledons.",
        "In a mature castor seed, a part of the endosperm persists and is used up during seed germination.",
        "In a mature beet seed, a persistent remnant of the nucellus is present.",
        "In coconut, the endosperm is completely consumed by the embryo before the seed matures.",
        "In groundnut, the endosperm persists in the mature seed."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
    "Persistence of endosperm and perisperm",
    "NCERT: the endosperm may be completely consumed by the developing embryo before seed maturation (pea, "
    "groundnut, beans), or it may persist in the mature seed (castor and coconut) and be used up during seed "
    "germination. In legumes the cotyledons are thick and swollen due to storage of food reserves. In black pepper "
    "and beet, remnants of the nucellus persist as the perisperm. So (a), (b) and (c) are true; (d) and (e) "
    "reverse the cases of coconut and groundnut.",
    ["Pea, groundnut: endosperm consumed; cotyledons store food", "Castor, coconut: endosperm persists",
     "Beet: perisperm"],
    C12_SR("post-fertilisation: endosperm; seed"),
    why="Coconut keeps its endosperm and groundnut does not, so options with (d) or (e) are wrong.",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "statement_pair",
    sp("The megaspore mother cell is differentiated in the micropylar region of the nucellus, and the embryo later "
       "develops at the micropylar end of the embryo sac, where the zygote is situated.",
       "In a mature embryo sac, the three antipodal cells lie at the micropylar end, next to the egg apparatus."),
    SP("C"),
    "Polarity of the ovule and embryo sac",
    "NCERT: ovules generally differentiate a single megaspore mother cell in the micropylar region of the nucellus, "
    "and the embryo develops at the micropylar end of the embryo sac where the zygote is situated (Statement I "
    "true). In the mature embryo sac, three cells are grouped together at the micropylar end (the egg apparatus) "
    "and three cells, the antipodals, are at the chalazal end (Statement II false).",
    ["MMC: micropylar region; embryo: micropylar end → I true", "Antipodals: chalazal end → II false"],
    C12_SR("pre-fertilisation: female gametophyte; post-fertilisation: embryo"),
    seconds=35)

add(SRFP, "Double fertilisation", "Intermediate", "match_list",
    ml(("event", "where it takes place"),
       ["Meiosis of the megaspore mother cell", "Meiosis of the pollen mother cell",
        "Syngamy and triple fusion", "Germination of a compatible pollen grain"],
       ["Stigma", "Embryo sac", "Nucellus of the ovule", "Microsporangium of the anther"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "D"),
    "Sites of the main reproductive events",
    "The megaspore mother cell lies in the micropylar region of the nucellus and divides there by meiosis (A-III). "
    "Pollen mother cells develop from the sporogenous tissue of the microsporangium and undergo meiosis there "
    "(B-IV). The pollen tube releases "
    "the two male gametes into a synergid of the embryo sac, where one fuses with the egg (syngamy) and the other "
    "with the polar nuclei in the central cell (triple fusion) (C-II). A compatible pollen grain germinates on "
    "the stigma (D-I).",
    ["A → nucellus", "B → microsporangium", "C → embryo sac", "D → stigma"],
    C12_SR("pre-fertilisation events; double fertilisation"),
    why="The other codes swap the two meiotic sites, put fertilisation on the stigma, or put megaspore formation "
        "in the embryo sac, which forms only after meiosis.",
    seconds=40)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "multi_statement",
    ms("Which of the following statements about apomixis and polyembryony are correct according to NCERT?",
       ["When seeds of orange are squeezed, many embryos of different sizes and shapes can be seen from each seed.",
        "In species in which nucellar cells develop into embryos, each ovule contains many embryos.",
        "Scientists are working to understand the genetics of apomixis and to transfer apomictic genes into hybrid "
        "varieties.",
        "Polyembryony means the presence of more than one embryo sac in an ovule.",
        "Apomixis is found in all members of Asteraceae and grasses."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "b", "e"], ["c", "d", "e"]], "D"),
    "Polyembryony and the hope of apomictic hybrids",
    "NCERT: in many Citrus and mango varieties, nucellar cells protrude into the embryo sac and develop into "
    "embryos, so each ovule contains many embryos (b); squeezing orange seeds shows many embryos of different sizes "
    "and shapes from each seed (a). Many scientists are working to understand the genetics of apomixis and to "
    "transfer apomictic genes into hybrid varieties (c). Polyembryony is the occurrence of more than one embryo "
    "in a seed, not of extra embryo sacs (d false), and apomixis is seen in some species of Asteraceae and grasses, "
    "not all (e false).",
    ["(a), (b), (c): NCERT statements", "(d): embryos, not embryo sacs", "(e): 'some species', not all"],
    C12_SR("apomixis and polyembryony"),
    why="Any option with (d) or (e) contains a false statement.",
    seconds=45)

_seeds = Counter()
for _f, _m in product("Aa", repeat=2):          # female gametophyte allele, male gamete allele (each 1/2)
    _seeds[("".join(sorted(_f + _m)), "".join(sorted(_f + _f + _m)))] += F(1, 4)
assert _seeds[("Aa", "AAa")] == F(1, 4) and sum(v for (e, _), v in _seeds.items() if e == "Aa") == F(1, 2)

add(SRFP, "Double fertilisation", "Advanced", "numerical",
    "A plant of genotype Aa is self-pollinated. Megasporogenesis is normal and monosporic, and each seed forms by "
    "normal double fertilisation. In what fraction of the seeds will the embryo be Aa and the endosperm AAa?",
    P("1/4", ["1/2", "1/16", "3/4"], "B"),
    "Genotypes of embryo and endosperm in the same seed",
    "All nuclei of an embryo sac come by mitosis from one haploid megaspore, so the egg and both polar nuclei carry "
    "the same allele (A or a, probability 1/2 each). Both male gametes of a pollen grain come from one generative "
    "cell, so they carry the same allele (A or a, 1/2 each). Embryo Aa with endosperm AAa needs a female "
    "gametophyte carrying A (endosperm gets A + A from the polar nuclei) and a pollen grain carrying a: "
    "1/2 × 1/2 = 1/4. (The other Aa embryos, from an a embryo sac and an A pollen grain, have endosperm Aaa.)",
    ["P(embryo sac carries A) = 1/2", "P(pollen carries a) = 1/2", "Embryo Aa and endosperm AAa: 1/2 × 1/2 = 1/4"],
    C12_SR("pre-fertilisation: female gametophyte; double fertilisation"),
    why="1/2 counts every Aa embryo, including those with endosperm Aaa; 1/16 wrongly treats the egg and each polar "
        "nucleus as receiving alleles independently; 3/4 is the fraction of embryos carrying at least one A.",
    seconds=90, verified_by=RECOMPUTED)

add(SRFP, "Endosperm and embryo", "Advanced", "multi_statement",
    ms("In a plant of genotype Aa, seeds are formed after cross-pollination with pollen from a plant of genotype "
       "aa. Which of the following are expected to be genetically identical to the mother plant (Aa) in every "
       "seed or fruit?",
       ["The seed coat", "The perisperm, in a species that has one", "The pericarp",
        "A nucellar embryo, in a species with nucellar polyembryony", "The endosperm"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "C"),
    "Maternal tissues in seeds and fruits",
    "The seed coat develops from the integuments, the perisperm is the persistent nucellus, and the pericarp "
    "develops from the ovary wall: all three are tissues of the mother sporophyte, so they are Aa. A nucellar "
    "embryo arises from a diploid nucellar cell without fertilisation, so it is also Aa. The endosperm develops "
    "from the triple-fused primary endosperm cell: here it is AAa or aaa, never identical to the mother.",
    ["Integuments → seed coat (maternal)", "Nucellus → perisperm (maternal)", "Ovary wall → pericarp (maternal)",
     "Nucellar embryo: maternal; endosperm: AAa or aaa"],
    C12_SR("post-fertilisation: seed and fruit; apomixis and polyembryony"),
    why="'(a), (b) and (c) only' leaves out the nucellar embryo; options with (e) include the triploid endosperm, "
        "which carries the paternal allele.",
    seconds=60)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "direct",
    "A species with bisexual flowers shows self-incompatibility. A bee carries pollen from one flower to the stigma "
    "of another flower on the same plant. What is the expected outcome?",
    P("The pistil recognises the pollen as 'self' and inhibits pollen germination or pollen tube growth, so the "
      "ovules are not fertilised by it",
      ["Fertilisation occurs, because the pollen came from a different flower and so counts as cross-pollen",
       "The pollen tube grows normally, but the endosperm fails to form",
       "Fertilisation occurs, because self-incompatibility acts only against autogamy within a flower"], "B"),
    "Self-incompatibility blocks geitonogamous pollen too",
    "Transfer of pollen to another flower of the same plant is geitonogamy, which is genetically similar to "
    "autogamy since the pollen comes from the same plant. Self-incompatibility is a genetic mechanism that "
    "prevents self-pollen (from the same flower or other flowers of the same plant) from fertilising the ovules by "
    "inhibiting pollen germination or pollen tube growth in the pistil. The pistil's recognition of the pollen, "
    "followed by acceptance or rejection, is the result of a dialogue between pollen and pistil.",
    ["Same plant → geitonogamy → 'self' pollen", "Self-incompatibility rejects self-pollen", "Germination or tube "
     "growth inhibited → no fertilisation"],
    C12_SR("outbreeding devices; pollen-pistil interaction"),
    why="Geitonogamous pollen is genetically self-pollen, so it is rejected at germination or tube growth; NCERT "
        "does not describe rejection at the endosperm stage.",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "assertion_reason",
    ar("An ovule generally has a single embryo sac.",
       "Ovules generally differentiate a single megaspore mother cell, and in a majority of flowering plants only "
       "one of the four megaspores it forms is functional and develops into the embryo sac."),
    AR("A"),
    "Why one embryo sac per ovule",
    "NCERT: an ovule generally has a single embryo sac formed from a megaspore. Ovules generally differentiate a "
    "single megaspore mother cell; its meiosis gives four megaspores, and in a majority of flowering plants one is "
    "functional while the other three degenerate. Only the functional megaspore develops into the female "
    "gametophyte. One mother cell × one functional megaspore = one embryo sac, so R explains A.",
    ["One MMC per ovule", "Meiosis → 4 megaspores, 1 functional", "1 functional megaspore → 1 embryo sac"],
    C12_SR("pre-fertilisation: megasporogenesis and the female gametophyte"),
    seconds=40)

_haploid = 24 // 2
assert 3 * _haploid == 36 and 2 * _haploid == 24

add(SRFP, "Microsporogenesis and male gametophyte", "Advanced", "statement_pair",
    "A flowering plant has 2n = 24 and sheds its pollen at the 3-celled stage.\n\n" +
    sp("At the time of shedding, one pollen grain contains 36 chromosomes in all, counting all its nuclei.",
       "Before fertilisation, the central cell of a mature embryo sac of this plant contains 36 chromosomes."),
    SP("C"),
    "Counting chromosomes in gametophytes",
    "n = 12. A pollen grain shed at the 3-celled stage has one vegetative cell and two male gametes, i.e. three "
    "haploid nuclei: 3 × 12 = 36 (Statement I true). The central cell of the embryo sac has two haploid polar "
    "nuclei: 2 × 12 = 24 chromosomes before fertilisation. It becomes triploid (36) only after triple fusion "
    "(Statement II false).",
    ["n = 12", "Pollen: 3 haploid nuclei → 36 (true)", "Central cell: 2 polar nuclei → 24, not 36 (false)"],
    C12_SR("pre-fertilisation: pollen grain and female gametophyte"),
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Pollination", "Advanced", "multi_statement",
    ms("A plant species has small flowers that are not colourful and produce no nectar. The pollen grains are light, "
       "non-sticky and produced in very large numbers, the stigma is large and feathery, each ovary has a single "
       "ovule, and many flowers are packed into an inflorescence. Which inferences are reasonable on the basis of "
       "NCERT?",
       ["The species is most probably wind-pollinated.",
        "The pollen grains reaching a given stigma is a chance factor, which is why so much pollen is produced.",
        "The species could well be a grass, in which this mode of pollination is quite common.",
        "Nectar-robbing insects are probably its main pollinators.",
        "Its pollen grains are probably protected from wetting by a mucilaginous covering."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["a", "d", "e"], ["b", "c", "d"]], "D"),
    "Recognising a wind-pollinated flower",
    "All the features listed match NCERT's description of wind-pollinated flowers: light, non-sticky pollen; a "
    "large, often feathery stigma; a single ovule in each ovary and numerous flowers packed into an inflorescence; "
    "flowers not very colourful and without nectar (a). Since contact of pollen with the stigma is a chance factor "
    "in wind pollination, the flowers produce an enormous amount of pollen compared with the number of ovules (b). "
    "NCERT notes that wind pollination is quite common in grasses (c). Pollen and nectar robbers do not pollinate, "
    "and this flower has no nectar (d false); a mucilaginous covering is a feature of water-pollinated pollen (e "
    "false).",
    ["Features → wind pollination (a)", "Chance factor → enormous pollen (b)", "Common in grasses (c)",
     "(d) robbers do not pollinate; (e) water-pollination feature"],
    C12_SR("pollination: agents of pollination"),
    why="Options with (d) or (e) attribute insect or water features to a wind-pollinated flower; '(b), (c) and (d)' "
        "also omits the main inference (a).",
    seconds=60)

# ================================================================ Principles of Inheritance and Variation (7 / 10 / 7)
C12_PI = lambda s: ref(12, PIV, s)

add(PIV, "Linkage and crossing over", "Basic", "direct",
    "Alfred Sturtevant used the frequency of recombination between gene pairs on the same chromosome to 'map' "
    "their positions. According to NCERT, such genetic maps are used today:",
    P("Extensively, as a starting point in the sequencing of whole genomes, as was done in the Human Genome "
      "Sequencing Project",
      ["Only to predict the sex of the offspring in Drosophila", "To count the number of chromosomes in a "
       "karyotype", "Only to identify the dominant allele of each gene pair"], "B"),
    "Use of genetic maps",
    "NCERT: Sturtevant used the frequency of recombination between gene pairs on the same chromosome as a measure "
    "of the distance between genes and 'mapped' their position on the chromosome. Today genetic maps are "
    "extensively used as a starting point in the sequencing of whole genomes, as was done in the case of the Human "
    "Genome Sequencing Project.",
    ["Recombination frequency → distance between genes", "Genetic map of gene positions", "Starting point for "
     "whole-genome sequencing (HGP)"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="A map of gene positions is not used to predict sex, count chromosomes or decide dominance.",
    seconds=25)

_n_f = 24
_n_m = _n_f - 1
_sperm = sorted({(_n_f - 2) // 2 + 1, (_n_f - 2) // 2})
assert (_n_m, _sperm) == (23, [11, 12])

add(PIV, "Sex determination", "Basic", "numerical",
    "In a grasshopper species, the somatic cells of the female have 24 chromosomes. Sex is determined by the XO "
    "mechanism. How many chromosomes are present in a somatic cell of the male, and in the two kinds of sperm it "
    "produces?",
    P("23; sperms with 12 and with 11 chromosomes",
      ["24; sperms with 12 and with 12 chromosomes", "23; all sperms with 12 chromosomes",
       "22; sperms with 11 and with 11 chromosomes"], "D"),
    "XO type of sex determination",
    "In the XO type (grasshopper), females have a pair of X chromosomes and males have only one X besides the "
    "autosomes. Female: 22 autosomes + XX = 24, so the male has 22 + X = 23. In meiosis, each sperm receives 11 "
    "autosomes; half the sperms also receive the X (12 chromosomes) and half do not (11 chromosomes).",
    ["Female 24 = 22A + XX", "Male = 22A + X = 23", "Sperms: 11A + X = 12, or 11A = 11"],
    C12_PI("sex determination"),
    why="24 would give the male two sex chromosomes (not XO); 'all 12' forgets the sperms without an X; 22 removes "
        "the X altogether.",
    seconds=45, verified_by=RECOMPUTED)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "assertion_reason",
    ar("In phenylketonuria, phenylpyruvic acid and other derivatives of phenylalanine are excreted through urine.",
       "These derivatives are poorly absorbed by the kidney."),
    AR("A"),
    "Why phenylpyruvic acid appears in urine",
    "NCERT: in phenylketonuria the affected individual lacks an enzyme that converts phenylalanine into tyrosine, "
    "so phenylalanine accumulates and is converted into phenylpyruvic acid and other derivatives. Their accumulation "
    "in the brain causes mental retardation. They are also excreted through urine because of their poor absorption "
    "by the kidney. R is the reason NCERT gives for A.",
    ["A: true", "R: true (poor absorption by the kidney)", "R is the stated cause of A"],
    C12_PI("genetic disorders: Mendelian disorders (phenylketonuria)"),
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "statement_pair",
    sp("During Mendel's investigations into inheritance patterns, statistical analysis and mathematical logic were "
       "applied to problems in biology for the first time.",
       "The confirmation of Mendel's inferences from experiments on successive generations of his test plants "
       "showed that his results pointed to general rules of inheritance rather than unsubstantiated ideas."),
    SP("A"),
    "What made Mendel's work scientific",
    "NCERT: it was during Mendel's investigations into inheritance patterns that, for the first time, statistical "
    "analysis and mathematical logic were applied to problems in biology (Statement I true). His experiments had a "
    "large sampling size, and the confirmation of his inferences from experiments on successive generations of his "
    "test plants proved that his results pointed to general rules of inheritance rather than unsubstantiated ideas "
    "(Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_PI("Mendel's laws of inheritance"),
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "Among the seven pairs of contrasting traits studied by Mendel in pea, which option gives the recessive traits "
    "for pod shape and pod colour, respectively?",
    P("Constricted and yellow", ["Inflated and green", "Constricted and green", "Inflated and yellow"], "B"),
    "Mendel's contrasting traits in pea",
    "In NCERT's table of the seven characters, pod shape is inflated (dominant) or constricted (recessive), and pod "
    "colour is green (dominant) or yellow (recessive). Note the trap: for pod colour green is dominant, whereas for "
    "seed colour yellow is dominant.",
    ["Pod shape: inflated > constricted", "Pod colour: green > yellow", "Recessive: constricted, yellow"],
    C12_PI("inheritance of one gene"),
    why="Inflated and green are the dominant traits; 'constricted and green' and 'inflated and yellow' each pair one "
        "dominant trait with one recessive trait.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Phenotype", "Genotype", "Homozygous", "Monohybrid cross"],
       ["A cross between parents that differ in one character", "Having two identical alleles of a gene, as TT or tt",
        "Observable expression of a character, such as tall or dwarf", "Genetic constitution, such as TT, Tt or tt"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "D"),
    "Basic terms of Mendelian genetics",
    "Phenotype is the observable expression of a character (tall, dwarf) (A-III); genotype is the genetic make-up "
    "(TT, Tt, tt) (B-IV); a homozygous individual has two identical alleles, TT or tt (C-II); a monohybrid cross "
    "involves parents differing in one character, such as Mendel's tall × dwarf cross (D-I).",
    ["A → III", "B → IV", "C → II", "D → I"],
    C12_PI("inheritance of one gene"),
    why="The other codes swap phenotype with genotype, homozygous with monohybrid cross, or phenotype with "
        "homozygous.",
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "direct",
    "Which of the following is described in NCERT as a feature of individuals with Down's syndrome?",
    P("Retarded physical, psychomotor and mental development",
      ["Development of breasts (gynaecomastia) in an individual with overall masculine development",
       "Rudimentary ovaries in a sterile female", "Non-stop bleeding from a simple cut"], "C"),
    "Features of Down's syndrome",
    "NCERT: Down's syndrome is caused by an additional copy of chromosome 21. The affected individual is short "
    "statured with a small round head, furrowed tongue and partially open mouth; the palm is broad with a "
    "characteristic palm crease; and physical, psychomotor and mental development is retarded.",
    ["Trisomy 21", "Physical features listed in NCERT", "Physical, psychomotor and mental development retarded"],
    C12_PI("genetic disorders: chromosomal disorders"),
    why="Gynaecomastia belongs to Klinefelter's syndrome, rudimentary ovaries to Turner's syndrome and non-stop "
        "bleeding to haemophilia.",
    seconds=25)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "match_list",
    ml(("fertilisation event", "result"),
       ["An egg with 22 autosomes + XX fertilised by a sperm with 22 autosomes + Y",
        "An egg with 22 autosomes and no sex chromosome fertilised by a sperm with 22 autosomes + X",
        "An egg with 23 autosomes (an extra chromosome 21) + X fertilised by a sperm with 22 autosomes + Y",
        "An egg with 22 autosomes + X fertilised by a sperm with 22 autosomes + Y"],
       ["Normal male (46, XY)", "Male with Down's syndrome (47 chromosomes)", "Turner's syndrome (45, X0)",
        "Klinefelter's syndrome (47, XXY)"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("II,III,IV,I")], "B"),
    "Aneuploid gametes and the resulting disorders",
    "Failure of segregation of chromatids (aneuploidy) can give eggs with an extra or a missing chromosome. "
    "A: 44 + XXY = 47, Klinefelter's syndrome (IV). B: 44 + X = 45, X0, Turner's syndrome (III). C: an extra "
    "chromosome 21 gives trisomy 21 with XY, a male with Down's syndrome, 47 chromosomes (II). D: normal gametes "
    "give 46, XY (I).",
    ["Count autosomes and sex chromosomes in the zygote", "XXY → Klinefelter's; X0 → Turner's",
     "Trisomy 21 → Down's; 44 + XY → normal male"],
    C12_PI("genetic disorders: chromosomal disorders; mutation (aneuploidy)"),
    why="The other codes swap Klinefelter's with Turner's, Down's with the normal male, or Down's with "
        "Klinefelter's.",
    seconds=50)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "assertion_reason",
    ar("A man with blood group O cannot be the biological father of a child with blood group AB.",
       "The allele i is dominant over both Iᴬ and Iᴮ."),
    AR("C"),
    "ABO alleles and paternity",
    "A child with blood group AB (IᴬIᴮ) must receive Iᴬ from one parent and Iᴮ from the other. A man with blood "
    "group O is ii and can pass on only i, so he cannot be the father: A is true. R is false: Iᴬ and Iᴮ are "
    "co-dominant with each other and both are dominant over i; i is recessive and produces no sugar.",
    ["AB child = IᴬIᴮ", "O father = ii → can give only i", "i is recessive, not dominant → R false"],
    C12_PI("inheritance of one gene: co-dominance and multiple alleles"),
    seconds=35)

add(PIV, "Sex determination", "Intermediate", "statement_pair",
    sp("In both the XO and the XY types of sex determination, the males produce two different kinds of sperms with "
       "respect to the sex chromosomes.",
       "In the ZW type of sex determination seen in birds, it is the male that produces two different kinds of "
       "gametes."),
    SP("C"),
    "Male and female heterogamety",
    "In the XO type (grasshopper), males produce sperms with an X and sperms without it; in the XY type (Drosophila, "
    "humans), males produce X-bearing and Y-bearing sperms. In both, the male is heterogametic (Statement I true). "
    "In birds the female is heterogametic (ZW) and produces two kinds of eggs, Z-bearing and W-bearing, while the "
    "male (ZZ) produces one kind of sperm (Statement II false).",
    ["XO and XY: male heterogamety → I true", "ZW: female heterogamety → II false"],
    C12_PI("sex determination"),
    seconds=35)

_f3_dwarf = F(2, 3) * F(1, 4)
assert _f3_dwarf == F(1, 6)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "True-breeding tall (TT) and dwarf (tt) pea plants are crossed and the F1 is self-pollinated. All the tall F2 "
    "plants are then self-pollinated, each tall plant contributing an equal number of progeny. What fraction of the "
    "F3 progeny raised from them will be dwarf?",
    P("1/6", ["1/4", "1/3", "1/8"], "C"),
    "Selfing the dominant class of F2",
    "Tall F2 plants are TT and Tt in the ratio 1 : 2, i.e. 1/3 TT and 2/3 Tt. TT plants give only tall progeny; Tt "
    "plants give 1/4 dwarf. Fraction dwarf in F3 = 2/3 × 1/4 = 1/6.",
    ["Tall F2: 1/3 TT, 2/3 Tt", "Dwarf only from Tt: 1/4 of its progeny", "2/3 × 1/4 = 1/6"],
    C12_PI("inheritance of one gene"),
    why="1/4 assumes every tall F2 plant is Tt; 1/3 is the fraction of tall F2 plants that are TT; 1/8 wrongly "
        "takes half the tall plants as Tt.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Linkage and crossing over", "Intermediate", "multi_statement",
    ms("Which of the following statements linking Mendel's laws with the behaviour of chromosomes are correct?",
       ["Segregation of the two alleles of a gene can be explained by the separation of the pair of homologous "
        "chromosomes carrying them during gamete formation.",
        "Independent assortment of two genes can be explained by the independent segregation of two different "
        "pairs of chromosomes carrying them.",
        "Two genes that are very tightly linked on the same chromosome do not assort independently, and parental "
        "combinations predominate among the progeny.",
        "A gamete receives both chromosomes of each homologous pair.",
        "The law of independent assortment applies to every pair of genes, whatever their location."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "Chromosomal basis of Mendel's laws",
    "Sutton and Boveri argued that the pairing and separation of a pair of chromosomes would lead to the "
    "segregation of the pair of factors they carried (a). In NCERT's comparison of chromosomes and genes, "
    "independent pairs segregate independently of each other, which explains independent assortment (b). Morgan "
    "found that genes on the same chromosome, especially tightly linked ones, give mostly parental combinations, so "
    "they do not assort independently (c). Only one chromosome of each pair goes to a gamete (d false), and linkage "
    "shows that independent assortment does not apply to every gene pair (e false).",
    ["(a) segregation ↔ homologues separating", "(b) assortment ↔ independent pairs", "(c) linkage exception",
     "(d), (e) false"],
    C12_PI("chromosomal theory of inheritance; linkage and recombination"),
    why="Options with (d) or (e) include a false statement; '(b), (c) and (d)' also leaves out (a).",
    seconds=50)

add(PIV, "Sex-linked inheritance", "Intermediate", "multi_statement",
    ms("A woman with normal vision is heterozygous (a carrier) for red-green colour blindness. Which of the "
       "following statements are correct?",
       ["Her vision is normal because the effect of the recessive allele is suppressed by her matching dominant "
        "normal allele.",
        "Each of her sons has a 50 per cent chance of being colour blind.",
        "She may have received the allele for colour blindness from either her mother or her father.",
        "All her daughters will necessarily be carriers.",
        "Her father must be colour blind."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "b", "e"], ["c", "d", "e"]], "B"),
    "A carrier of colour blindness",
    "Colour blindness is a sex-linked recessive disorder due to a mutation in a gene on the X chromosome. NCERT: "
    "the son of a woman who carries the gene has a 50 per cent chance of being colour blind; the mother is not "
    "herself colour blind because the gene is recessive, its effect being suppressed by her matching dominant "
    "normal gene (a, b). She has two X chromosomes, one from each parent, so the allele could have come from "
    "either a carrier mother or a colour-blind father (c), and her father need not be colour blind (e false). Each "
    "daughter receives one of her two X chromosomes, so a daughter is not necessarily a carrier (d false).",
    ["Recessive allele masked → normal vision (a)", "Son: 50% chance (b)", "Allele from either parent (c)",
     "(d), (e) need not be true"],
    C12_PI("sex-linked inheritance: colour blindness"),
    why="(d) ignores that each daughter has a 1/2 chance of receiving the normal X; (e) ignores a carrier mother as "
        "the source.",
    seconds=50)

_snap = {"RR x rr": Counter({"pink": 4}), "Rr x Rr": Counter({"red": 1, "pink": 2, "white": 1}),
         "Rr x rr": Counter({"pink": 2, "white": 2}), "Rr x RR": Counter({"red": 2, "pink": 2})}
_col = {"RR": "red", "Rr": "pink", "rr": "white"}
for _k, _v in _snap.items():
    _a, _b = _k.split(" x ")
    _got = Counter(_col["".join(sorted(x + y))] for x in _a for y in _b)
    assert _got == _v, (_k, _got)

add(PIV, "Incomplete and co-dominance", "Intermediate", "match_list",
    "In snapdragon, flower colour shows incomplete dominance: RR is red, Rr is pink and rr is white.\n\n" +
    ml(("cross", "flower colours among the progeny"),
       ["RR × rr", "Rr × Rr", "Rr × rr", "Rr × RR"],
       ["1 red : 1 pink", "All pink", "1 pink : 1 white", "1 red : 2 pink : 1 white"]),
    M(mc("II,IV,III,I"), [mc("II,IV,I,III"), mc("IV,II,III,I"), mc("II,III,IV,I")], "D"),
    "Crosses under incomplete dominance",
    "With incomplete dominance every genotype has its own phenotype, so phenotypic ratios equal genotypic ratios. "
    "RR × rr gives only Rr: all pink (A-II). Rr × Rr gives RR : Rr : rr = 1 : 2 : 1, i.e. 1 red : 2 pink : 1 white "
    "(B-IV). Rr × rr gives Rr : rr = 1 pink : 1 white (C-III). Rr × RR gives RR : Rr = 1 red : 1 pink (D-I).",
    ["Phenotype ratio = genotype ratio", "Work each cross with gametes", "A-II, B-IV, C-III, D-I"],
    C12_PI("inheritance of one gene: incomplete dominance"),
    why="The other codes swap the two back-crosses (with RR and with rr) or the F1 cross with the F2 cross.",
    seconds=50, verified_by=RECOMPUTED)

add(PIV, "Sex determination", "Intermediate", "assertion_reason",
    ar("In humans, the female produces two kinds of eggs, X-bearing and Y-bearing.",
       "Human females are homogametic, with two X chromosomes."),
    AR("D"),
    "Homogametic human female",
    "Human females have a pair of X chromosomes (XX), so every egg receives an X besides 22 autosomes; there are "
    "no Y-bearing eggs (A false). R is true: having two sex chromosomes of the same type, the female is "
    "homogametic. It is the male (XY) that produces two kinds of sperms, X-bearing and Y-bearing, so the sex of the "
    "child is decided by the sperm.",
    ["Female XX → all eggs carry X → A false", "R: true (homogametic female)"],
    C12_PI("sex determination: sex determination in humans"),
    seconds=30)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "statement_pair",
    sp("α-Thalassemia is observed due to mutation or deletion of one or more of the four genes HBA1 and HBA2 "
       "(two on chromosome 16 from each parent); the more genes affected, the fewer α-globin molecules are "
       "produced.",
       "β-Thalassemia is controlled by a single gene, HBB, on chromosome 11 of each parent and occurs due to "
       "mutation of one or both the genes."),
    SP("A"),
    "Genetic basis of α- and β-thalassemia",
    "NCERT: α-thalassemia is controlled by two closely linked genes, HBA1 and HBA2, on chromosome 16 of each "
    "parent, and is observed due to mutation or deletion of one or more of the four genes; the more genes "
    "affected, the less α-globin is produced (Statement I true). β-Thalassemia is controlled by a single gene, "
    "HBB, on chromosome 11 of each parent and occurs due to mutation of one or both the genes (Statement II true).",
    ["α: HBA1 + HBA2 on chr 16 × 2 parents = 4 genes", "β: HBB on chr 11 × 2 parents = 2 genes", "Both true"],
    C12_PI("genetic disorders: Mendelian disorders (thalassemia)"),
    seconds=40)

add(PIV, "Sex determination", "Intermediate", "direct",
    "Henking traced a specific nuclear structure through spermatogenesis in a few insects and named it the 'X "
    "body'. What did further investigations by other scientists conclude about it?",
    P("The 'X body' was in fact a chromosome, which is why it was given the name X chromosome",
      ["The 'X body' was a cytoplasmic granule unrelated to sex", "The 'X body' was the nucleolus of the "
       "spermatocyte", "The 'X body' was a Y chromosome that had lost its genes"], "A"),
    "From Henking's X body to the X chromosome",
    "NCERT: Henking (1891) observed that 50 per cent of the sperm received the X body after spermatogenesis and "
    "the other 50 per cent did not, but he could not explain its significance. Further investigations by other "
    "scientists led to the conclusion that the 'X body' was in fact a chromosome, and that is why it was given the "
    "name X chromosome.",
    ["Henking: 'X body', significance unexplained", "Later work: it is a chromosome", "Hence 'X chromosome'"],
    C12_PI("sex determination"),
    why="The structure was shown to be a chromosome, not a cytoplasmic granule, a nucleolus or a Y chromosome.",
    seconds=25)

_rf = F(20, 100)
_ab_gamete = (1 - _rf) / 2
assert _ab_gamete ** 2 == F(16, 100) and (_rf / 2) ** 2 == F(1, 100)

add(PIV, "Linkage and crossing over", "Advanced", "numerical",
    "Genes A and B lie on the same chromosome, and the frequency of recombination between them is 20 per cent. A "
    "plant that received AB from one parent and ab from the other is self-pollinated. Assume the same "
    "recombination frequency in male and female gamete formation. What percentage of the progeny is expected to "
    "be aabb?",
    P("16 per cent", ["1 per cent", "4 per cent", "6.25 per cent"], "B"),
    "Gamete frequencies of a linked dihybrid",
    "With AB/ab and 20 per cent recombination, the gametes are parental AB 40 per cent and ab 40 per cent, and "
    "recombinant Ab 10 per cent and aB 10 per cent. An aabb plant needs an ab gamete from each parent: "
    "0.40 × 0.40 = 0.16, i.e. 16 per cent.",
    ["Parental gametes: (100 − 20)/2 = 40% each", "Recombinant gametes: 10% each", "aabb = 0.4 × 0.4 = 16%"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="1 per cent would apply if ab were a recombinant gamete (parents Ab/aB); 4 per cent squares the "
        "recombination frequency; 6.25 per cent (1/16) assumes independent assortment.",
    seconds=90, verified_by=RECOMPUTED)

_dark = Counter()
for _alleles in product((0, 1), repeat=6):         # each of six alleles in AaBbCc x AaBbCc dominant or not
    _dark[sum(_alleles)] += F(1, 64)
assert _dark[5] + _dark[6] == F(7, 64) and _dark[4] == F(15, 64)

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "Suppose a polygenic trait is controlled by three genes A, B and C, and each dominant allele adds an equal "
    "amount to the phenotype. Plants AABBcc and aabbCC are crossed, and the F1 is self-pollinated. What fraction "
    "of the F2 will show a phenotype beyond (more extreme than) that of the parent with more dominant alleles?",
    P("7/64", ["1/64", "15/64", "11/32"], "C"),
    "Polygenic F2 can exceed the parental range",
    "The parents have 4 (AABBcc) and 2 (aabbCC) dominant alleles. The F1 is AaBbCc (3 dominant alleles). In its "
    "F2, the number of dominant alleles ranges from 0 to 6, with frequencies 1, 6, 15, 20, 15, 6, 1 (out of 64). "
    "More than 4 dominant alleles: 6/64 (five) + 1/64 (six) = 7/64.",
    ["Parents: 4 and 2 dominant alleles", "F2 classes 0–6: 1 : 6 : 15 : 20 : 15 : 6 : 1 (/64)", "Five or six: "
     "(6 + 1)/64 = 7/64"],
    C12_PI("polygenic inheritance"),
    why="1/64 counts only AABBCC; 15/64 is the class equal to the darker parent; 11/32 (22/64) includes that "
        "equal class as well.",
    seconds=100, verified_by=RECOMPUTED)

assert F(1, 2) * F(1, 2) == F(1, 4)

add(PIV, "Sex-linked inheritance", "Advanced", "multi_statement",
    ms("A man with normal colour vision and blood group AB marries a colour-blind woman with blood group O. "
       "Which of the following statements about their children are correct?",
       ["All their sons will be colour blind.",
        "None of their children will have blood group O or blood group AB.",
        "All their daughters will have normal vision but will be carriers of colour blindness.",
        "The probability that their first child is a colour-blind son with blood group A is 1/4.",
        "Half of their daughters will be colour blind."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
    "Combining an X-linked and an autosomal gene",
    "Colour vision: mother XᶜXᶜ, father XY (normal). Every son gets Xᶜ from his mother and Y from his father: "
    "colour blind (a). Every daughter gets Xᶜ from her mother and the normal X from her father: normal vision, "
    "carrier (c), so no daughter is colour blind (e false). Blood group: IᴬIᴮ × ii gives Iᴬi (A) or Iᴮi (B), each "
    "1/2, never O or AB (b). First child a son (1/2, and then certainly colour blind) with blood group A (1/2): "
    "1/2 × 1/2 = 1/4 (d).",
    ["Sons: all colour blind; daughters: all carriers", "Blood groups: A or B, 1/2 each",
     "P(colour-blind son with A) = 1/2 × 1/2 = 1/4"],
    C12_PI("sex-linked inheritance; co-dominance and multiple alleles"),
    why="'(a), (b) and (c) only' leaves out the true probability in (d); options with (e) are wrong because every "
        "daughter receives the father's normal X.",
    seconds=90, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Advanced", "assertion_reason",
    ar("Among the children of a man of genotype Iᴬi and a woman of genotype Iᴮi, all four blood groups, A, B, AB "
       "and O, are expected in equal proportions.",
       "Each parent forms its two kinds of gametes in equal numbers; Iᴬ and Iᴮ are co-dominant while both are "
       "dominant over i, so the four equally likely genotypes IᴬIᴮ, Iᴬi, Iᴮi and ii each give a different blood "
       "group."),
    AR("A"),
    "All four ABO phenotypes from one couple",
    "Gametes: Iᴬ and i (1/2 each) from the father, Iᴮ and i (1/2 each) from the mother. The four combinations "
    "IᴬIᴮ, Iᴬi, Iᴮi and ii are each 1/4. Because of co-dominance (IᴬIᴮ → AB) and the recessiveness of i "
    "(Iᴬi → A, Iᴮi → B, ii → O), each genotype gives a different phenotype, so the four blood groups appear in a "
    "1 : 1 : 1 : 1 ratio. R is exactly the reason for A.",
    ["Gametes 1 : 1 from each parent", "Four genotypes, 1/4 each", "Each genotype → a distinct blood group"],
    C12_PI("inheritance of one gene: co-dominance and multiple alleles"),
    seconds=50)

add(PIV, "Sex-linked inheritance", "Advanced", "direct",
    "A couple with normal colour vision has a son with Klinefelter's syndrome (XXY) who is red-green colour blind. "
    "Assuming no new mutation, which explanation fits these facts?",
    P("The mother is a carrier, and an egg carrying two X chromosomes, both with the colour-blindness allele, was "
      "fertilised by a Y-bearing sperm",
      ["A sperm carrying both the X and the Y chromosome of the father fertilised a normal egg carrying the "
       "colour-blindness allele",
       "An egg with no sex chromosome was fertilised by a sperm carrying both the X and the Y chromosome of the "
       "father",
       "The father is a carrier of colour blindness and passed the allele to his son on the Y chromosome"], "B"),
    "Tracing an extra X chromosome with an X-linked marker",
    "Colour blindness is X-linked recessive, so an XXY son is colour blind only if both his X chromosomes carry "
    "the allele. The father has normal vision, so his X carries the normal allele; any X from him would make the "
    "son see normally. Both X chromosomes must therefore come from the mother, who must be a carrier (she sees "
    "normally); her egg had two X chromosomes (failure of segregation, aneuploidy) and was fertilised by a "
    "Y-bearing sperm.",
    ["Son needs the allele on both X chromosomes", "Father's X is normal → neither X came from him",
     "Both X from a carrier mother + Y from father"],
    C12_PI("sex-linked inheritance; chromosomal disorders"),
    why="Any option in which the son receives his father's X gives him a normal allele; a male cannot be a "
        "carrier, and the gene is not on the Y chromosome.",
    seconds=90)

_tc = {"unlinked": F(1, 4), "coupling RF 20%": (1 - F(20, 100)) / 2, "repulsion RF 20%": F(20, 100) / 2,
       "complete linkage": F(1, 2)}
assert list(_tc.values()) == [F(1, 4), F(2, 5), F(1, 10), F(1, 2)]

add(PIV, "Linkage and crossing over", "Advanced", "match_list",
    "Each dihybrid in List-I is test-crossed with aabb.\n\n" +
    ml(("dihybrid test-crossed with aabb", "expected fraction of aabb progeny"),
       ["AaBb, with the two genes on different chromosomes",
        "A dihybrid that received AB from one parent and ab from the other, with 20 per cent recombination",
        "A dihybrid that received Ab from one parent and aB from the other, with 20 per cent recombination",
        "A dihybrid that received AB from one parent and ab from the other, with genes so tightly linked that no "
        "recombination occurs"],
       ["1/2", "1/4", "1/10", "2/5"]),
    M(mc("II,IV,III,I"), [mc("II,III,IV,I"), mc("I,IV,III,II"), mc("II,IV,I,III")], "C"),
    "Test-cross outcomes with and without linkage",
    "In a test cross, the fraction of aabb progeny equals the fraction of ab gametes of the dihybrid. Independent "
    "genes: 1/4 (A-II). AB/ab with 20 per cent recombination: ab is parental, (1 − 0.2)/2 = 0.4 = 2/5 (B-IV). "
    "Ab/aB with 20 per cent recombination: ab is recombinant, 0.2/2 = 0.1 = 1/10 (C-III). Complete linkage of "
    "AB/ab: only AB and ab gametes, 1/2 (D-I).",
    ["aabb fraction = ab gamete fraction", "Parental class: (1 − RF)/2; recombinant: RF/2",
     "A-II, B-IV, C-III, D-I"],
    C12_PI("chromosomal theory of inheritance: linkage and recombination"),
    why="The other codes confuse the coupling (AB/ab) and repulsion (Ab/aB) arrangements, or treat complete "
        "linkage as independent assortment.",
    seconds=100, verified_by=RECOMPUTED)

_chicken = 78
assert _chicken // 2 == 39 and _chicken - 2 == 76

add(PIV, "Sex determination", "Advanced", "multi_statement",
    ms("In a bird species, the somatic cells of both sexes have 78 chromosomes. Which of the following statements "
       "are correct?",
       ["The hen produces two kinds of eggs, each with 39 chromosomes: one kind carries a Z chromosome and the "
        "other a W chromosome.",
        "The cock produces only one kind of sperm with respect to the sex chromosomes.",
        "The sex of a chick is decided by the kind of egg that is fertilised.",
        "The somatic cells of the hen have 77 chromosomes, because she has only one Z chromosome.",
        "Each sperm of the cock carries 38 autosomes and a W chromosome."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Female heterogamety in birds",
    "In birds the female is ZW and the male ZZ, so both sexes have the same number of chromosomes, 76 autosomes + "
    "2 sex chromosomes = 78 (d false). The hen gives eggs with 38 autosomes + Z or 38 autosomes + W, 39 each (a). "
    "The cock gives only sperms with 38 autosomes + Z (b); it has no W (e false). Since the egg type varies and "
    "the sperm does not, the egg decides the sex of the chick (c).",
    ["Hen ZW, cock ZZ: 78 in both", "Eggs: 38 + Z or 38 + W", "Sperms: 38 + Z only → egg decides sex"],
    C12_PI("sex determination"),
    why="(d) treats the ZW female like an XO male; (e) gives the male a W chromosome, which only females carry.",
    seconds=60, verified_by=RECOMPUTED)

# ================================================================ Molecular Basis of Inheritance (7 / 10 / 8)
C12_MB = lambda s: ref(12, MBI, s)

add(MBI, "Replication", "Basic", "direct",
    "The scheme of DNA replication in which each strand of the double helix acts as a template for the synthesis "
    "of a new complementary strand was proposed by:",
    P("Watson and Crick themselves", ["Meselson and Stahl", "Taylor and colleagues", "Hershey and Chase"], "A"),
    "Proposal and proof of semiconservative replication",
    "NCERT: while proposing the double helix structure, Watson and Crick also proposed a scheme for replication: "
    "the two strands separate and each acts as a template for a new complementary strand, so that each daughter "
    "molecule has one parental and one new strand (semiconservative). Meselson and Stahl (1958) later proved it "
    "experimentally in E. coli, and Taylor and colleagues showed it for chromosomes of Vicia faba.",
    ["Proposed: Watson and Crick", "Proved in E. coli: Meselson and Stahl", "Shown in chromosomes: Taylor"],
    C12_MB("replication: the experimental proof"),
    why="Meselson and Stahl and Taylor provided experimental proof; Hershey and Chase showed that DNA is the "
        "genetic material.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "According to NCERT, a nucleotide has three components. They are:",
    P("A nitrogenous base, a pentose sugar and a phosphate group",
      ["A nitrogenous base, a hexose sugar and a phosphate group", "A nitrogenous base, a pentose sugar and an "
       "amino acid", "Two nitrogenous bases joined by hydrogen bonds and a phosphate group"], "D"),
    "Components of a nucleotide",
    "NCERT: a nucleotide has three components: a nitrogenous base, a pentose sugar (ribose in RNA, deoxyribose in "
    "DNA) and a phosphate group. A base linked to the sugar is a nucleoside; adding a phosphate at the 5'-OH gives "
    "a nucleotide.",
    ["Base + pentose = nucleoside", "Nucleoside + phosphate = nucleotide"],
    C12_MB("structure of polynucleotide chain"),
    why="The sugar is a pentose, not a hexose; amino acids are not part of nucleotides; hydrogen-bonded base pairs "
        "belong to the double helix, not to a single nucleotide.",
    seconds=20)

add(MBI, "Transcription", "Basic", "assertion_reason",
    ar("The base sequence of an mRNA is the same as that of the coding strand of its gene, except that the mRNA "
       "has uracil in place of thymine.",
       "The mRNA is synthesised complementary to the template strand, and the template strand is itself "
       "complementary to the coding strand."),
    AR("A"),
    "Why mRNA matches the coding strand",
    "NCERT: in a transcription unit, the strand with 3'→5' polarity acts as the template, and the other strand, "
    "with 5'→3' polarity, has the same sequence as the RNA (except thymine at the place of uracil) and is called "
    "the coding strand. The RNA is built by complementary base pairing on the template; since the coding strand "
    "is also complementary to the template, the RNA and the coding strand carry the same sequence, with U in RNA "
    "where DNA has T. R is the direct cause of A.",
    ["RNA = complement of template", "Coding strand = complement of template", "So RNA = coding strand (U for T)"],
    C12_MB("transcription: transcription unit"),
    seconds=30)

add(MBI, "DNA as genetic material", "Basic", "statement_pair",
    sp("RNA, being a catalyst as well as genetic material, was reactive and hence unstable.",
       "DNA has evolved from RNA with chemical modifications that make it more stable."),
    SP("A"),
    "From the RNA world to DNA",
    "NCERT (RNA world): RNA was the first genetic material and used to act both as genetic material and as a "
    "catalyst. But RNA, being a catalyst, was reactive and hence unstable (Statement I true). Therefore DNA has "
    "evolved from RNA with chemical modifications that make it more stable; being double stranded, with a "
    "complementary strand, DNA further resists changes by evolving a process of repair (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_MB("RNA world"),
    seconds=30)

add(MBI, "Replication", "Basic", "match_list",
    ml(("enzyme or catalyst", "role"),
       ["DNA-dependent DNA polymerase", "DNA ligase", "DNA-dependent RNA polymerase",
        "23S rRNA in bacteria (ribozyme)"],
       ["Joins the discontinuously synthesised fragments", "Forms peptide bonds during translation",
        "Synthesises RNA on a DNA template", "Polymerises deoxyribonucleotides on a DNA template"]),
    M(mc("IV,I,III,II"), [mc("III,I,IV,II"), mc("IV,II,III,I"), mc("I,IV,III,II")], "C"),
    "Enzymes of replication, transcription and translation",
    "DNA-dependent DNA polymerases polymerise deoxyribonucleotides using a DNA template (A-IV). The discontinuously "
    "synthesised fragments of the lagging strand are later joined by DNA ligase (B-I). Transcription is catalysed "
    "by DNA-dependent RNA polymerase (C-III). In bacteria, 23S rRNA acts as the enzyme (ribozyme) for peptide bond "
    "formation (D-II).",
    ["A → IV", "B → I", "C → III", "D → II"],
    C12_MB("replication: the machinery and the enzymes; transcription; translation"),
    why="The other codes swap DNA and RNA polymerase, ligase with the ribozyme, or the polymerase with ligase.",
    seconds=35)

add(MBI, "DNA and RNA structure", "Basic", "direct",
    "The pentose sugar present in the nucleotides of DNA is:",
    P("2'-deoxyribose", ["Ribose", "Glucose", "3'-deoxyribose"], "B"),
    "Sugar of DNA",
    "NCERT: the pentose sugar is ribose in RNA and 2'-deoxyribose in DNA, which is why the nucleic acids are "
    "named ribonucleic acid and deoxyribonucleic acid. RNA retains a 2'-OH group on every nucleotide, which makes "
    "it labile; DNA lacks it.",
    ["RNA: ribose", "DNA: 2'-deoxyribose (no 2'-OH)"],
    C12_MB("structure of polynucleotide chain"),
    why="Ribose is the sugar of RNA, glucose is a hexose, and the missing oxygen in DNA's sugar is at the 2' "
        "carbon, not the 3' carbon.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "multi_statement",
    ms("Which of the following nitrogenous bases are pyrimidines?",
       ["Cytosine", "Thymine", "Uracil", "Adenine", "Guanine"]),
    MS(["a", "b", "c"], [["a", "d", "e"], ["d", "e"], ["a", "b", "d"]], "D"),
    "Purines and pyrimidines",
    "NCERT: nitrogenous bases are of two types, purines (adenine and guanine) and pyrimidines (cytosine, uracil "
    "and thymine). Cytosine is common to DNA and RNA; thymine is present in DNA and uracil in RNA.",
    ["Purines: A, G", "Pyrimidines: C, T, U"],
    C12_MB("structure of polynucleotide chain"),
    why="Adenine and guanine are purines, so options with (d) or (e) are wrong.",
    seconds=25)

add(MBI, "Lac operon", "Intermediate", "direct",
    "A mutant E. coli has an altered operator to which the lac repressor can no longer bind; its i, z, y and a "
    "genes and its promoter are normal. Glucose is absent. What happens in this mutant?",
    P("The z, y and a genes are transcribed even when lactose is absent",
      ["The z, y and a genes are never transcribed, even when lactose is present",
       "The z, y and a genes are transcribed only when lactose is present, as in the wild type",
       "Only the i gene is transcribed, and the repressor accumulates in the cell"], "C"),
    "Role of the operator in negative regulation",
    "In the lac operon, the repressor (from the i gene) binds to the operator and prevents RNA polymerase from "
    "transcribing the structural genes; the inducer acts by inactivating the repressor. If the repressor cannot "
    "bind the operator, nothing blocks RNA polymerase, so the polycistronic z-y-a mRNA is made whether or not "
    "lactose is present: the operon is expressed all the time.",
    ["Repressor must bind operator to switch the operon off", "Operator cannot bind repressor → never switched "
     "off", "z, y, a transcribed even without lactose"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="Nothing stops transcription in this mutant, so it cannot be 'never' or 'only with lactose'; the i gene is "
        "transcribed in the wild type too and its product simply cannot act here.",
    seconds=45)

add(MBI, "Lac operon", "Intermediate", "assertion_reason",
    ar("When the lac operon is switched on, the z, y and a genes are transcribed together.",
       "In the lac operon, a polycistronic structural gene is regulated by a common promoter and regulatory genes."),
    AR("A"),
    "Polycistronic organisation of the lac operon",
    "NCERT: in bacteria, the arrangement in which a polycistronic structural gene is regulated by a common promoter "
    "and regulatory genes is called an operon. The lac operon's structural genes z, y and a share one promoter and "
    "operator, so when the repressor is removed by the inducer, RNA polymerase transcribes them as one "
    "polycistronic mRNA. R explains A.",
    ["One promoter for z, y, a", "Polycistronic transcript", "R explains A"],
    C12_MB("regulation of gene expression: the lac operon"),
    seconds=35)

_phx = 5386
assert 2 * _phx == 10772

add(MBI, "DNA and RNA structure", "Intermediate", "statement_pair",
    sp("Because the bases pair in a complementary way, if the sequence of bases in one strand of a DNA double "
       "helix is known, the sequence in the other strand can be predicted.",
       "A circular double-stranded DNA molecule of 5386 base pairs has 10,772 phosphodiester linkages in all."),
    SP("A"),
    "Complementarity and counting linkages",
    "NCERT: base pairing confers a very unique property on the polynucleotide chains: they are complementary, so "
    "if the sequence of one strand is known, the other can be predicted (Statement I true). In a circular strand "
    "of n nucleotides there are n phosphodiester linkages (a linear strand has n − 1). Two strands of 5386 "
    "nucleotides each: 2 × 5386 = 10,772 (Statement II true).",
    ["Statement I: true", "Circular strand: n linkages", "2 × 5386 = 10,772 → Statement II true"],
    C12_MB("structure of polynucleotide chain"),
    seconds=50, verified_by=RECOMPUTED)

add(MBI, "Human genome project and DNA fingerprinting", "Intermediate", "multi_statement",
    ms("Which of the following statements about the significance and findings of the Human Genome Project are "
       "correct according to NCERT?",
       ["Knowledge about the effects of DNA variations among individuals can lead to revolutionising the ways to "
        "diagnose, treat and someday prevent thousands of disorders that affect human beings.",
        "Learning about non-human organisms' DNA sequences can lead to an understanding of their natural "
        "capabilities that can be applied to challenges in health care, agriculture, energy production and "
        "environmental remediation.",
        "Since less than 2 per cent of the genome codes for proteins, the remaining DNA has been shown to have no "
        "role at all.",
        "The human genome contains about 80,000 genes.",
        "The functions of all the discovered human genes are now known."]),
    MS(["a", "b"], [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "D"),
    "Why the Human Genome Project matters",
    "NCERT: knowledge about the effects of DNA variations among individuals can revolutionise the ways to "
    "diagnose, treat and someday prevent thousands of disorders (a); learning about the DNA of non-human "
    "organisms can lead to an understanding of their natural capabilities, applicable to health care, "
    "agriculture, energy production and environmental remediation (b). Repetitive sequences, though thought to "
    "have no direct coding function, shed light on chromosome structure, dynamics and evolution (c false). The "
    "genome has about 30,000 genes, not 80,000 (d false), and functions are unknown for over 50 per cent of the "
    "discovered genes (e false).",
    ["(a), (b): NCERT's significance of HGP", "(c), (d), (e): contradict NCERT's salient features"],
    C12_MB("human genome project: goals, methodologies and salient features"),
    why="Every other option includes at least one false statement.",
    seconds=55)

add(MBI, "DNA as genetic material", "Intermediate", "match_list",
    ml(("experiment", "label used"),
       ["Hershey and Chase: labelling the DNA of bacteriophages",
        "Hershey and Chase: labelling the protein coat of bacteriophages",
        "Meselson and Stahl: replication in E. coli",
        "Taylor and colleagues: replication in chromosomes of Vicia faba"],
       ["Radioactive thymidine", "¹⁵NH₄Cl as the only nitrogen source", "Radioactive sulphur",
        "Radioactive phosphorus"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("II,III,IV,I")], "A"),
    "Labels used in classic experiments",
    "DNA contains phosphorus but not sulphur, and protein contains sulphur but not phosphorus, so Hershey and Chase "
    "labelled phage DNA with radioactive phosphorus (A-IV) and the protein coat with radioactive sulphur (B-III). "
    "Meselson and Stahl grew E. coli on ¹⁵NH₄Cl as the only nitrogen source to make heavy DNA (C-II). Taylor and "
    "colleagues used radioactive thymidine on Vicia faba to detect the distribution of newly synthesised DNA in "
    "chromosomes (D-I).",
    ["P in DNA, S in protein", "Heavy nitrogen for density separation", "Radioactive thymidine for chromosomes"],
    C12_MB("the search for genetic material; replication: the experimental proof"),
    why="The other codes swap the two Hershey–Chase labels or the two replication experiments.",
    seconds=40)

add(MBI, "DNA as genetic material", "Intermediate", "direct",
    "In a variation of Griffith's experiment, mice are injected with a mixture of heat-killed S strain and "
    "heat-killed R strain Streptococcus pneumoniae. What is expected?",
    P("The mice live, because no living bacteria are present to be transformed or to multiply",
      ["The mice die, because the R strain is transformed by the S strain",
       "The mice die, because heat-killed S strain bacteria alone are virulent",
       "The mice live, but living S strain bacteria are recovered from them"], "C"),
    "Transformation needs living recipient cells",
    "NCERT (Griffith): live S strain kills mice; live R strain and heat-killed S strain alone do not. Only when "
    "heat-killed S was mixed with live R did the mice die, because the living R bacteria were transformed into "
    "virulent S bacteria. With both strains heat-killed, there are no living cells to be transformed or to cause "
    "infection, so the mice survive and no living bacteria can be recovered.",
    ["Heat-killed S alone: mice live", "Transformation needs living R cells", "Both killed → mice live"],
    C12_MB("the search for genetic material: transforming principle"),
    why="Dead R cells cannot be transformed; heat-killed S alone is not virulent; and no living S cells can be "
        "recovered without living bacteria.",
    seconds=40)

add(MBI, "Transcription", "Intermediate", "multi_statement",
    ms("The template strand of a short stretch of a structural gene reads 3'-TACGAT-5'. Which of the following "
       "statements are correct?",
       ["The mRNA transcribed from it reads 5'-AUGCUA-3'.",
        "The coding strand reads 5'-ATGCTA-3'.",
        "The first codon of the mRNA is the initiation codon AUG.",
        "The mRNA contains thymine at two positions.",
        "The RNA is polymerised in the 3'→5' direction."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Reading template and coding strands",
    "RNA is complementary and antiparallel to the template: template 3'-TACGAT-5' gives mRNA 5'-AUGCUA-3' (a). The "
    "coding strand has the same sequence as the mRNA with T for U: 5'-ATGCTA-3' (b). The first codon AUG is the "
    "initiation codon (c). RNA has uracil, not thymine (d false), and all nucleic acid polymerases add "
    "nucleotides in the 5'→3' direction (e false).",
    ["Template 3'-TAC GAT-5' → mRNA 5'-AUG CUA-3'", "Coding strand = mRNA with T for U", "(d), (e) false"],
    C12_MB("transcription: transcription unit"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (e)' also omits (a).",
    seconds=50)

add(MBI, "Transcription", "Intermediate", "statement_pair",
    sp("In eukaryotes, RNA polymerase I transcribes the rRNAs 28S, 18S and 5.8S, whereas RNA polymerase III "
       "transcribes the 5S rRNA.",
       "In eukaryotes, the heterogeneous nuclear RNA, the precursor of mRNA, is transcribed by RNA polymerase III."),
    SP("C"),
    "Division of labour among eukaryotic RNA polymerases",
    "NCERT: in eukaryotes there are at least three RNA polymerases in the nucleus. RNA polymerase I transcribes "
    "rRNAs (28S, 18S and 5.8S); RNA polymerase III transcribes tRNA, 5S rRNA and snRNAs (Statement I true); RNA "
    "polymerase II transcribes the precursor of mRNA, hnRNA (Statement II false).",
    ["Pol I: 28S, 18S, 5.8S rRNA", "Pol II: hnRNA", "Pol III: tRNA, 5S rRNA, snRNA"],
    C12_MB("transcription: transcription unit and gene"),
    seconds=35)

add(MBI, "Transcription", "Intermediate", "assertion_reason",
    ar("In bacteria, the mRNA does not require any processing to become active.",
       "Bacterial structural genes are split genes, with coding sequences interrupted by introns."),
    AR("C"),
    "Bacterial versus eukaryotic genes",
    "NCERT: in bacteria the mRNA does not require any processing to become active, and since transcription and "
    "translation occur in the same compartment, translation can begin before the mRNA is fully transcribed (A "
    "true). Split genes, with exons interrupted by introns, are a feature of eukaryotes; their hnRNA must be "
    "spliced. Bacterial genes are not split, so R is false.",
    ["A: true", "Split genes → eukaryotes", "R: false"],
    C12_MB("transcription: transcription unit and gene; processing of hnRNA"),
    seconds=30)

_strand = {"A": 30, "T": 20, "G": 15, "C": 35}
_g_ds = F(_strand["G"] + _strand["C"], 2)
assert _g_ds == 25

add(MBI, "DNA and RNA structure", "Intermediate", "direct",
    "One strand of a double-stranded DNA molecule has the base composition A 30 per cent, T 20 per cent, G 15 per "
    "cent and C 35 per cent. What percentage of all the bases in the double-stranded molecule is guanine?",
    P("25 per cent", ["15 per cent", "35 per cent", "50 per cent"], "D"),
    "Base composition of a double helix from one strand",
    "Each G in one strand pairs with a C in the other. The complementary strand therefore has G = 35 per cent "
    "(opposite the C of the first strand). Total G = (15 + 35)/2 = 25 per cent of the bases of the double "
    "helix. Check with Chargaff's rule: then C = 25, and A = T = (30 + 20)/2 = 25 per cent each.",
    ["Strand 1: G 15, C 35 → strand 2: G 35", "Average over two strands: (15 + 35)/2 = 25%"],
    C12_MB("structure of polynucleotide chain: double helix and Chargaff's rule"),
    why="15 per cent is the G of one strand only; 35 per cent is the G of the other strand only; 50 per cent is "
        "G + C, not G alone.",
    seconds=50, verified_by=RECOMPUTED)

add(MBI, "Lac operon", "Advanced", "match_list",
    ml(("E. coli strain (glucose absent)", "behaviour of the lac operon"),
       ["Wild type", "Mutant whose operator cannot bind the repressor",
        "Mutant whose repressor binds the operator but cannot interact with the inducer",
        "Mutant lacking the lac promoter"],
       ["Expressed only when lactose is present", "Expressed even when lactose is absent",
        "Not expressed even when lactose is present, because the repressor stays bound",
        "Not expressed, because RNA polymerase has no binding site"]),
    M(mc("I,II,III,IV"), [mc("I,III,II,IV"), mc("II,I,III,IV"), mc("I,II,IV,III")], "B"),
    "Predicting lac operon behaviour in mutants",
    "Wild type: the repressor blocks the operator; lactose (inducer) inactivates it, so the operon is inducible "
    "(A-I). If the operator cannot bind the repressor, nothing blocks RNA polymerase and the genes are expressed "
    "even without lactose (B-II). If the repressor cannot interact with the inducer, it stays bound to the "
    "operator even when lactose is present (C-III). The promoter provides the binding site for RNA polymerase; "
    "without it, transcription cannot start (D-IV).",
    ["Inducer inactivates repressor", "Operator must bind repressor to switch off", "Promoter is needed to start"],
    C12_MB("regulation of gene expression: the lac operon; transcription unit"),
    why="The other codes swap the inducible and constitutive states, or the two non-expressing mutants, whose "
        "causes differ.",
    seconds=70)

add(MBI, "Genetic code and translation", "Advanced", "multi_statement",
    "The coding strand of a short gene reads 5'-ATGGCATTCTAA-3'. Use: AUG = methionine, GCA = alanine, "
    "UUC = phenylalanine, UUU = phenylalanine, UAA = stop.\n\n" +
    ms("Which of the following statements are correct?",
       ["The mRNA reads 5'-AUGGCAUUCUAA-3'.",
        "The polypeptide formed is methionine–alanine–phenylalanine.",
        "Deleting the fifth base of the gene would leave the amino acid sequence unchanged.",
        "Changing the ninth base of the coding strand from C to T would not change the polypeptide.",
        "The template strand, written 5'→3', reads 5'-ATGGCATTCTAA-3'."]),
    MS(["a", "b", "d"], [["a", "b", "c", "d"], ["a", "d", "e"], ["b", "c", "e"]], "A"),
    "Codons, mutations and the degenerate code",
    "mRNA = coding strand with U for T: AUG GCA UUC UAA (a): Met–Ala–Phe, then stop (b). Deleting the fifth base "
    "(C) gives AUG GAU UCU AA…: the reading frame shifts and the amino acids after the first change (c false). C→T "
    "at the ninth base turns UUC into UUU, which also codes for phenylalanine, since the code is degenerate (d). "
    "The sequence in (e) is the coding strand; the template, written 5'→3', is 5'-TTAGAATGCCAT-3' (e false).",
    ["mRNA: AUG GCA UUC UAA", "Met–Ala–Phe", "Deletion → frameshift", "UUC → UUU: same amino acid"],
    C12_MB("genetic code; mutations and genetic code; translation"),
    why="(c) ignores the frameshift caused by a single-base deletion; (e) gives the coding strand, not the "
        "template.",
    seconds=90)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "assertion_reason",
    ar("DNA fingerprinting uses repetitive (satellite) DNA rather than the protein-coding sequences.",
       "Satellite DNA sequences show a high degree of polymorphism among individuals."),
    AR("A"),
    "Why satellite DNA is used in fingerprinting",
    "NCERT: DNA fingerprinting involves identifying differences in some specific regions of the DNA sequence "
    "called repetitive DNA. Satellite DNA sequences normally do not code for any proteins, but they form a large "
    "portion of the human genome and show a high degree of polymorphism, which forms the basis of DNA "
    "fingerprinting. Since 99.9 per cent of the bases are the same in all people, it is the highly polymorphic "
    "regions that can tell individuals apart: R explains A.",
    ["Goal: tell individuals apart", "Need highly variable DNA", "Satellite DNA is highly polymorphic → R explains "
     "A"],
    C12_MB("DNA fingerprinting"),
    seconds=40)

_mols = [("H", "H")]
for _gen in range(1, 6):
    _mols = [m for (a, b) in _mols for m in ((a, "L"), (b, "L"))]
    assert sum(1 for m in _mols if "H" in m) == 2 and ("H", "H") not in _mols

add(MBI, "Replication", "Advanced", "statement_pair",
    "One DNA molecule of E. coli fully labelled with ¹⁵N (both strands heavy) replicates semiconservatively for "
    "several generations in a medium containing only ¹⁴NH₄Cl.\n\n" +
    sp("After any number of generations (one or more), exactly two of the descendant molecules are hybrid "
       "(¹⁵N/¹⁴N), and all the others are light.",
       "Heavy (¹⁵N/¹⁵N) DNA reappears after the third generation in the ¹⁴N medium."),
    SP("C"),
    "Fate of parental strands in semiconservative replication",
    "In semiconservative replication the two parental heavy strands are never broken or lost; in each generation "
    "each one is paired with a new light strand. So after every generation exactly two molecules are hybrid and "
    "the rest are ¹⁴N/¹⁴N (Statement I true): e.g. 2 of 4 after two generations, 2 of 8 after three. A heavy/heavy "
    "molecule needs two ¹⁵N strands together, which cannot form in a medium supplying only ¹⁴N (Statement II "
    "false).",
    ["Two parental strands persist, each in a hybrid", "Hybrid count stays 2; light molecules increase",
     "No new ¹⁵N strands → no heavy DNA"],
    C12_MB("replication: the experimental proof"),
    seconds=60, verified_by=RECOMPUTED)

_aa = 150
assert 3 * _aa + 3 == 453 and _aa - 1 == 149

add(MBI, "Genetic code and translation", "Advanced", "direct",
    "A polypeptide of 150 amino acids is translated from an mRNA. What is the minimum length of the mRNA region "
    "from the first base of the start codon to the last base of the stop codon, and how many peptide bonds does "
    "the polypeptide contain?",
    P("453 nucleotides; 149 peptide bonds",
      ["450 nucleotides; 150 peptide bonds", "453 nucleotides; 150 peptide bonds", "450 nucleotides; 149 peptide "
       "bonds"], "C"),
    "Codons, stop codon and peptide bonds",
    "Each amino acid needs one triplet codon (the start codon AUG codes for the first methionine): 150 × 3 = 450 "
    "nucleotides. The stop codon codes for no amino acid but is part of the reading frame: + 3 = 453. A linear "
    "chain of n amino acids has n − 1 peptide bonds: 149.",
    ["150 codons × 3 = 450", "+ stop codon 3 = 453", "Peptide bonds = 150 − 1 = 149"],
    C12_MB("genetic code; translation"),
    why="450 forgets the stop codon; 150 peptide bonds counts one bond per amino acid instead of n − 1.",
    seconds=50, verified_by=RECOMPUTED)

add(MBI, "DNA as genetic material", "Advanced", "multi_statement",
    ms("Suppose Hershey and Chase had used bacteriophages labelled with both radioactive phosphorus (in DNA) and "
       "radioactive sulphur (in protein) to infect bacteria, followed by blending and centrifugation. Which "
       "results are expected?",
       ["The bacterial cells in the pellet would carry radioactive phosphorus.",
        "Radioactive sulphur would be found mainly in the supernatant.",
        "Blending would separate the viral coats from the bacteria.",
        "Radioactive sulphur would be found inside the bacterial cells.",
        "The result would show that protein is the genetic material."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "d", "e"], ["b", "c", "e"]], "D"),
    "Predicting a double-label Hershey–Chase experiment",
    "Only phage DNA enters the bacterium; the protein coat stays outside. Blending removes the viral coats from "
    "the bacteria (c), and centrifugation separates the light viral particles (supernatant, carrying ³⁵S protein) "
    "from the heavier bacteria (pellet, carrying ³²P DNA) (a, b). Sulphur-labelled protein does not enter (d "
    "false), so the result shows that DNA, not protein, is the genetic material (e false).",
    ["DNA (³²P) enters → pellet", "Protein coat (³⁵S) stays out → supernatant", "DNA is the genetic material"],
    C12_MB("the search for genetic material"),
    why="Options with (d) or (e) contradict the experiment's key finding that protein does not enter the cell.",
    seconds=60)

add(MBI, "Human genome project and DNA fingerprinting", "Advanced", "match_list",
    ml(("change in DNA or in the cell cycle", "consequence"),
       ["A mutation in non-coding repetitive DNA that does not affect reproductive ability",
        "Change of the sixth codon of the β-globin gene from GAG to GUG",
        "Insertion of a single base within the coding region of a gene",
        "Failure of cell division after DNA replication"],
       ["Polyploidy", "Shift of the reading frame from the point of insertion",
        "Glutamic acid replaced by valine in the β-globin chain", "Accumulation over generations, giving DNA "
        "polymorphism"]),
    M(mc("IV,III,II,I"), [mc("IV,II,III,I"), mc("I,III,II,IV"), mc("III,IV,II,I")], "D"),
    "Consequences of changes in DNA",
    "Mutations in non-coding DNA may have no immediate effect on reproductive ability, so they accumulate "
    "generation after generation, one cause of DNA polymorphism (A-IV). GAG→GUG at the sixth codon of β-globin "
    "replaces glutamic acid by valine, causing sickle-cell anaemia (B-III). A single-base insertion shifts the "
    "reading frame (C-II). NCERT: a failure in cell division after DNA replication results in polyploidy (D-I).",
    ["A → IV", "B → III", "C → II", "D → I"],
    C12_MB("DNA fingerprinting; mutations and genetic code; replication"),
    why="The other codes swap the substitution with the frameshift, or polyploidy with polymorphism.",
    seconds=55)

add(MBI, "Replication", "Advanced", "multi_statement",
    ms("Which of the following statements about events at a replication fork are correct?",
       ["On the template strand with 3'→5' polarity, the new strand is synthesised continuously.",
        "On the template strand with 5'→3' polarity, the new strand is synthesised discontinuously.",
        "The discontinuously synthesised fragments are later joined by DNA ligase.",
        "DNA polymerase can initiate replication at any random place in the DNA.",
        "The new strands are polymerised in the 3'→5' direction."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Continuous and discontinuous synthesis",
    "NCERT: DNA-dependent DNA polymerases catalyse polymerisation only in the 5'→3' direction. Consequently, on "
    "the template with 3'→5' polarity replication is continuous (a), while on the template with 5'→3' polarity it "
    "is discontinuous (b); the fragments are joined by DNA ligase (c). Replication does not start randomly: it "
    "begins at a definite region, the origin of replication (d false). Polymerisation is 5'→3', not 3'→5' (e "
    "false).",
    ["5'→3' polymerisation only", "3'→5' template: continuous; 5'→3' template: discontinuous", "Ligase joins "
     "fragments; start at origin"],
    C12_MB("replication: the machinery and the enzymes"),
    why="Options with (d) or (e) contain a false statement.",
    seconds=50)

# ================================================================ Microbes in Human Welfare (3 / 4 / 3)
C12_MW = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "direct",
    "NCERT points out that microbes are present everywhere. Which of the following places does it name as "
    "habitats where microbes are found?",
    P("Thermal vents (where the temperature may be as high as 100 °C), deep in the soil, under layers of snow and "
      "highly acidic environments",
      ["Only in soil, water and air, never inside the bodies of animals and plants",
       "Only in moderate environments, never above 50 °C or in acidic conditions",
       "Only inside the bodies of animals and plants, never free in nature"], "B"),
    "Microbes are ubiquitous",
    "NCERT: microbes are present everywhere: in soil, water and air, inside our bodies and those of other animals "
    "and plants, and even where no other life form could possibly exist, such as deep inside geysers (thermal "
    "vents) where the temperature may be as high as 100 °C, deep in the soil, under the layers of snow several "
    "metres thick, and in highly acidic environments.",
    ["Everywhere: soil, water, air, inside organisms", "Extreme habitats: thermal vents up to 100 °C, deep soil, "
     "under snow, acidic places"],
    C12_MW("introduction"),
    why="Each wrong option restricts microbes to some habitats, whereas NCERT stresses that they are found "
        "everywhere, including inside bodies and in extreme environments.",
    seconds=25)

add(MHW, "Sewage treatment", "Basic", "direct",
    "In a sewage treatment plant, the secondary treatment, in which the primary effluent is passed into aeration "
    "tanks and microbes consume its organic matter, is also called:",
    P("Biological treatment", ["Physical treatment", "Chemical treatment", "Tertiary treatment"], "D"),
    "Secondary treatment is biological",
    "NCERT: primary treatment involves the physical removal of particles (filtration and sedimentation). Secondary "
    "treatment, or biological treatment, uses the vigorous growth of useful aerobic microbes into flocs in the "
    "aeration tanks; these consume the major part of the organic matter and reduce the BOD of the effluent.",
    ["Primary: physical removal", "Secondary: microbes digest organic matter = biological treatment"],
    C12_MW("microbes in sewage treatment: secondary treatment"),
    why="Physical removal is primary treatment; NCERT does not describe the aeration step as chemical or tertiary "
        "treatment.",
    seconds=20)

add(MHW, "Household and industrial products", "Basic", "statement_pair",
    sp("Microbes such as bacteria and fungi can be grown on nutritive media to form colonies that can be seen with "
       "the naked eye.",
       "Prions, mentioned by NCERT among the diverse microbes, are proteinaceous infectious agents."),
    SP("A"),
    "Diversity and culture of microbes",
    "NCERT: microbes are diverse: protozoa, bacteria, fungi, microscopic plant and animal viruses, viroids and "
    "also prions, which are proteinaceous infectious agents (Statement II true). Microbes like bacteria and many "
    "fungi can be grown on nutritive media to form colonies that can be seen with the naked eye, and such cultures "
    "are useful in studies on micro-organisms (Statement I true).",
    ["Statement I: true", "Statement II: true"],
    C12_MW("introduction"),
    seconds=30)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "assertion_reason",
    ar("Biofertilisers are not yet available commercially in India, so farmers cannot use them in their fields.",
       "Biofertilisers are organisms that enrich the nutrient quality of the soil."),
    AR("D"),
    "Biofertilisers in use",
    "NCERT: biofertilisers are organisms that enrich the nutrient quality of the soil; the main sources are "
    "bacteria, fungi and cyanobacteria (R true). Currently, in our country, a number of biofertilisers are "
    "available commercially in the market, and farmers use these regularly in their fields to replenish soil "
    "nutrients and to reduce dependence on chemical fertilisers. So A is false.",
    ["A: false (commercially available, used regularly)", "R: true (definition)"],
    C12_MW("microbes as biofertilisers"),
    seconds=30)

add(MHW, "Biogas", "Intermediate", "multi_statement",
    ms("Which of the following statements are correct according to NCERT?",
       ["The excreta of cattle, rich in methanogenic bacteria, is used to generate biogas, commonly called gobar "
        "gas.",
        "Rhizobium fixes atmospheric nitrogen in symbiotic association with the root nodules of leguminous plants.",
        "Cyanobacteria are autotrophic microbes widely distributed in aquatic and terrestrial environments.",
        "Methanogens grow aerobically and need constant aeration.",
        "Mycorrhizal fungi such as Glomus fix atmospheric nitrogen for the plant."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "d", "e"], ["a", "c", "d"]], "B"),
    "Microbes in biogas and as biofertilisers",
    "Cattle excreta (gobar), rich in methanogens, is used for biogas, commonly called gobar gas (a). The bacteria "
    "forming nodules on the roots of leguminous plants by symbiotic association are Rhizobium, which fix "
    "atmospheric nitrogen (b). Cyanobacteria are autotrophic microbes widely distributed in aquatic and terrestrial "
    "environments, many of which fix nitrogen (c). Methanogens grow anaerobically (d false). Glomus forms "
    "mycorrhiza and absorbs phosphorus from the soil for the plant; it is not described as fixing nitrogen (e "
    "false).",
    ["(a) gobar gas", "(b) Rhizobium in legume nodules", "(c) cyanobacteria", "(d) anaerobic; (e) phosphorus, not "
     "nitrogen"],
    C12_MW("microbes in production of biogas; microbes as biofertilisers"),
    why="Options with (d) or (e) contain a false statement; '(a), (c) and (d)' also omits (b).",
    seconds=50)

add(MHW, "Sewage treatment", "Intermediate", "statement_pair",
    sp("In primary treatment, all the solids that settle form the primary sludge, and the supernatant forms the "
       "effluent, which is taken for secondary treatment.",
       "Once the BOD has been reduced in the aeration tanks, the effluent is released directly into rivers without "
       "being passed through any settling tank."),
    SP("C"),
    "Sludge and effluent in sewage treatment",
    "NCERT: after filtration and sedimentation in primary treatment, all solids that settle form the primary "
    "sludge, and the supernatant forms the effluent, which goes for secondary treatment (Statement I true). Once "
    "the BOD is reduced significantly, the effluent is passed into a settling tank where the bacterial flocs "
    "sediment as activated sludge; only then is the effluent from secondary treatment released into natural "
    "water bodies (Statement II false).",
    ["Statement I: true", "Settling tank comes before release → Statement II false"],
    C12_MW("microbes in sewage treatment"),
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "match_list",
    ml(("biocontrol agent", "pest or pathogen it controls"),
       ["Ladybird beetle", "Dragonflies", "Bacillus thuringiensis", "Trichoderma"],
       ["Several plant pathogens", "Aphids", "Mosquitoes", "Butterfly caterpillars"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,III,I,IV"), mc("IV,III,II,I")], "D"),
    "Matching biocontrol agents with their targets",
    "NCERT: the ladybird and dragonflies are useful to get rid of aphids and mosquitoes, respectively (A-II, "
    "B-III). Bacillus thuringiensis is used to control butterfly caterpillars (C-IV). Trichoderma species are "
    "free-living fungi that are effective biocontrol agents of several plant pathogens (D-I).",
    ["Ladybird → aphids", "Dragonflies → mosquitoes", "Bt → caterpillars", "Trichoderma → plant pathogens"],
    C12_MW("microbes as biocontrol agents"),
    why="The other codes swap the targets of the ladybird and dragonflies, of Bt and Trichoderma, or of the "
        "ladybird and Bt.",
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "assertion_reason",
    ar("Baculoviruses of the genus Nucleopolyhedrovirus are desirable for biological control in an integrated pest "
       "management programme in which beneficial insects are being conserved.",
       "These viruses are species-specific, narrow-spectrum insecticidal agents with no negative impact on plants, "
       "mammals, birds, fish or even non-target insects."),
    AR("A"),
    "Why baculoviruses suit integrated pest management",
    "NCERT: baculoviruses (mostly genus Nucleopolyhedrovirus) attack insects and other arthropods. They have been "
    "shown to have no negative impacts on plants, mammals, birds, fish or even on non-target insects. This is "
    "especially desirable when beneficial insects are being conserved to aid an overall IPM programme, or when an "
    "ecologically sensitive area is being treated. Their species-specific, narrow-spectrum action is the reason "
    "for A.",
    ["Species-specific, narrow-spectrum", "Spares non-target and beneficial insects", "Hence suitable for IPM"],
    C12_MW("microbes as biocontrol agents"),
    seconds=40)

add(MHW, "Household and industrial products", "Advanced", "multi_statement",
    ms("Which of the following statements about microbes in household and industrial products are correct?",
       ["Both the large holes in Swiss cheese and the puffed-up appearance of dosa and idli dough result from "
        "carbon dioxide produced by microbes.",
        "Whisky is produced by distillation of the fermented broth, whereas wine is produced without distillation.",
        "Lactic acid bacteria convert milk to curd and also increase its vitamin B₁₂ content.",
        "Roquefort cheese is ripened by growing a specific bacterium on it.",
        "Citric acid is produced commercially by the bacterium Acetobacter aceti."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "B"),
    "Microbes in food and industry",
    "Propionibacterium sharmanii produces a large amount of CO₂ that makes the holes in Swiss cheese, and the "
    "dough for dosa and idli puffs up due to CO₂ produced by bacteria (a). Wine and beer are produced without "
    "distillation, whereas whisky, brandy and rum are produced by distillation of the fermented broth (b). LAB "
    "convert milk to curd and improve its nutritional quality by increasing vitamin B₁₂ (c). Roquefort cheese is "
    "ripened by a specific fungus (d false), and citric acid comes from the fungus Aspergillus niger, while "
    "Acetobacter aceti makes acetic acid (e false).",
    ["(a) CO₂ in both", "(b) distilled vs not", "(c) LAB and B₁₂", "(d) fungus; (e) Aspergillus niger"],
    C12_MW("microbes in household products; microbes in industrial products"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (d)' also omits (a).",
    seconds=55)

add(MHW, "Household and industrial products", "Advanced", "direct",
    "Which pair of products are both obtained from bacteria, according to NCERT?",
    P("Streptokinase and butyric acid",
      ["Cyclosporin A and citric acid", "Statins and ethanol", "Penicillin and statins"], "D"),
    "Bacterial, fungal and yeast products",
    "Streptokinase is produced by the bacterium Streptococcus, and butyric acid by the bacterium Clostridium "
    "butylicum. Cyclosporin A comes from the fungus Trichoderma polysporum and citric acid from the fungus "
    "Aspergillus niger; statins come from the fungus Monascus purpureus and ethanol is produced commercially using "
    "the yeast Saccharomyces cerevisiae; penicillin comes from the mould Penicillium notatum.",
    ["Streptokinase: Streptococcus (bacterium)", "Butyric acid: Clostridium butylicum (bacterium)",
     "Others: fungi or yeasts"],
    C12_MW("microbes in industrial products"),
    why="Each of the other pairs contains products of fungi or yeasts only.",
    seconds=40)

# ================================================================ Organisms and Populations (4 / 6 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population growth", "Basic", "direct",
    "According to NCERT, populations evolve to maximise their reproductive fitness, also called Darwinian fitness, "
    "in the habitat in which they live. Such fitness is indicated by:",
    P("A high value of r, the intrinsic rate of natural increase",
      ["A high carrying capacity K of the habitat", "A high death rate", "A large body size of the individuals"],
      "B"),
    "Darwinian fitness and r",
    "NCERT (life history variation): populations evolve to maximise their reproductive fitness, also called "
    "Darwinian fitness (high r value), in the habitat in which they live. r is the intrinsic rate of natural "
    "increase, the parameter NCERT also uses to assess the impact of any factor on population growth.",
    ["Reproductive (Darwinian) fitness", "Measured as high r"],
    C12_OP("populations: life history variation"),
    why="K is a property of the habitat, a high death rate lowers r, and NCERT does not equate fitness with body "
        "size.",
    seconds=25)

add(OAP, "Population interactions", "Basic", "assertion_reason",
    ar("In amensalism, both interacting species benefit.",
       "In commensalism, one species benefits and the other is neither harmed nor benefited."),
    AR("D"),
    "Amensalism and commensalism",
    "NCERT: in amensalism one species is harmed whereas the other is unaffected; it is not an interaction in "
    "which both benefit (that is mutualism), so A is false. Commensalism is the interaction in which one species "
    "benefits and the other is neither harmed nor benefited, as with an orchid growing as an epiphyte on a mango "
    "branch (R true).",
    ["Amensalism: (−, 0) → A false", "Commensalism: (+, 0) → R true"],
    C12_OP("populations: population interactions"),
    seconds=25)

add(OAP, "Population attributes", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Carrying capacity (K)", "Intrinsic rate of natural increase (r)", "Age pyramid", "Population density"],
       ["Per capita birth rate minus per capita death rate (b − d)", "Size of a population per unit area, as "
        "numbers, biomass or per cent cover", "Maximum number of individuals that the habitat can support",
        "Plot of the age distribution of a population"]),
    M(mc("III,I,IV,II"), [mc("I,III,IV,II"), mc("III,I,II,IV"), mc("III,IV,I,II")], "C"),
    "Basic terms of population ecology",
    "Carrying capacity K is the limit beyond which no further growth is possible, the maximum the habitat's "
    "resources can support (A-III). In dN/dt = (b − d)N, r = b − d is the intrinsic rate of natural increase "
    "(B-I). Plotting the per cent of individuals in each age group gives the age pyramid (C-IV). Population "
    "density is population size per unit area, measured as numbers, biomass or per cent cover (D-II).",
    ["A → III", "B → I", "C → IV", "D → II"],
    C12_OP("populations: population attributes; population growth"),
    why="The other codes swap K with r, the age pyramid with density, or r with the age pyramid.",
    seconds=30)

add(OAP, "Population growth", "Basic", "statement_pair",
    sp("Some organisms breed only once in their lifetime, such as Pacific salmon fish and bamboo, while others "
       "breed many times during their lifetime, such as most birds and mammals.",
       "Some organisms produce a large number of small-sized offspring, such as oysters and pelagic fishes, while "
       "others produce a small number of large-sized offspring, such as birds and mammals."),
    SP("A"),
    "Life history variation",
    "NCERT: under a particular set of selection pressures, organisms evolve towards the most efficient "
    "reproductive strategy. Some breed only once in their lifetime (Pacific salmon fish, bamboo), while others "
    "breed many times (most birds and mammals) (Statement I true). Some produce a large number of small-sized "
    "offspring (oysters, pelagic fishes), while others produce a small number of large-sized offspring (birds, "
    "mammals) (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_OP("populations: life history variation"),
    seconds=30)

add(OAP, "Population growth", "Intermediate", "assertion_reason",
    ar("A population growing in a habitat with limited resources shows a deceleration phase as its density "
       "approaches the carrying capacity.",
       "In the logistic equation dN/dt = rN[(K − N)/K], the factor (K − N)/K becomes smaller as N increases, "
       "lowering the growth rate per individual."),
    AR("A"),
    "Why logistic growth decelerates",
    "In logistic growth the per capita growth rate is r(K − N)/K. As N rises towards K, (K − N)/K falls towards "
    "zero, so each individual contributes less and less to growth: the curve passes from acceleration into "
    "deceleration and finally reaches an asymptote at K. R is the mathematical reason for A.",
    ["Per capita rate = r(K − N)/K", "Falls as N → K", "Deceleration, then asymptote"],
    C12_OP("populations: population growth (logistic growth)"),
    seconds=40)

_r, _K = F(2, 5), 2000
_rate = lambda n: _r * n * F(_K - n, _K)
assert max(range(0, _K + 1), key=_rate) == 1000 and _rate(1000) == 200

add(OAP, "Population growth", "Intermediate", "numerical",
    "A population grows according to the logistic model, dN/dt = rN[(K − N)/K], with r = 0.4 per year and "
    "K = 2000. At what population size is the growth rate dN/dt the highest, and what is that rate?",
    P("At N = 1000; 200 individuals per year",
      ["At N = 2000; 800 individuals per year", "At N = 1000; 400 individuals per year",
       "At N = 500; 150 individuals per year"], "D"),
    "Maximum growth rate in logistic growth",
    "dN/dt = rN(K − N)/K is a product that is largest when N = K/2 (the middle of the S-shaped curve). Here "
    "N = 2000/2 = 1000, and dN/dt = 0.4 × 1000 × (2000 − 1000)/2000 = 0.4 × 1000 × 0.5 = 200 individuals per "
    "year (the maximum, rK/4).",
    ["Maximum at N = K/2 = 1000", "dN/dt = 0.4 × 1000 × 0.5 = 200"],
    C12_OP("populations: population growth (logistic growth)"),
    why="At N = K growth is zero, not maximum; 400 forgets the (K − N)/K factor; at N = 500 the rate is "
        "0.4 × 500 × 0.75 = 150, which is less than 200.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population growth", "Intermediate", "multi_statement",
    ms("Which of the following statements about life history variation are correct according to NCERT?",
       ["Under a particular set of selection pressures, organisms evolve towards the most efficient reproductive "
        "strategy.",
        "Ecologists suggest that life history traits of organisms have evolved in relation to the constraints "
        "imposed by the abiotic and biotic components of the habitat.",
        "All populations have the same intrinsic rate of natural increase.",
        "The number and size of offspring are the same in all species.",
        "Life history traits do not depend in any way on the habitat."]),
    MS(["a", "b"], [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
    "Evolution of reproductive strategies",
    "NCERT: populations evolve to maximise reproductive fitness in their habitat; under a particular set of "
    "selection pressures, organisms evolve towards the most efficient reproductive strategy (a), and ecologists "
    "suggest that life history traits have evolved in relation to the constraints imposed by the abiotic and "
    "biotic components of the habitat (b). NCERT's r values differ widely (0.12 for the flour beetle, 0.015 for "
    "the Norway rat) (c false); species differ in the number and size of their offspring (d false); and life "
    "history traits are shaped by the habitat (e false).",
    ["(a), (b): NCERT statements", "(c), (d), (e) contradict NCERT"],
    C12_OP("populations: life history variation"),
    why="Every other option includes at least one false statement.",
    seconds=45)

add(OAP, "Population growth", "Intermediate", "direct",
    "For a population growing exponentially (dN/dt = rN) with a constant r, what is the shape of the graph of the "
    "growth rate dN/dt plotted against population size N?",
    P("A straight line through the origin, with slope r",
      ["A horizontal straight line, since dN/dt stays constant", "A bell-shaped curve with its peak at N = K/2",
       "An S-shaped curve that levels off at K"], "C"),
    "Growth rate in exponential growth",
    "In dN/dt = rN, dN/dt is directly proportional to N with constant r, so the graph of dN/dt against N is a "
    "straight line through the origin with slope r: the bigger the population, the faster it grows (this is why "
    "N plotted against time gives a J-shaped curve). A hump-shaped dN/dt with a peak at K/2 belongs to logistic "
    "growth, and the S-shaped curve is N against time in logistic growth.",
    ["dN/dt = rN → proportional to N", "Straight line through origin, slope r", "N vs time → J-shaped"],
    C12_OP("populations: population growth (exponential growth)"),
    why="dN/dt is not constant (it rises with N); the peak at K/2 and the S-shape belong to logistic growth.",
    seconds=45)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("When certain exotic species are introduced into a geographical area, they may become invasive and spread "
       "fast, because the invaded land does not have their natural predators.",
       "Predators always drive their prey species to extinction."),
    SP("C"),
    "Predators and population regulation",
    "NCERT: one reason why certain exotic species become invasive and spread fast when introduced into a "
    "geographical area is that the invaded land does not have their natural predators, as with the prickly pear "
    "cactus in Australia (Statement I true). Predators in nature are 'prudent': a predator that overexploits its "
    "prey might itself become extinct for lack of food, and predators keep prey populations under control rather "
    "than eliminating them (Statement II false).",
    ["Statement I: true", "Prudent predators; prey kept under control → Statement II false"],
    C12_OP("populations: population interactions (predation)"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following statements about plant defences against herbivores are correct?",
       ["Thorns, as in Acacia and cactus, are the most common morphological means of defence.",
        "Many plants produce and store chemicals that make the herbivore sick when eaten, inhibit feeding or "
        "digestion, disrupt its reproduction or even kill it.",
        "Nicotine, caffeine, quinine, strychnine and opium are produced by plants as defences against grazers and "
        "browsers.",
        "Plants produce these chemicals mainly to attract herbivores.",
        "Calotropis is heavily browsed by cattle and goats."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "A"),
    "Morphological and chemical defences of plants",
    "NCERT: since plants cannot run away, they have evolved morphological and chemical defences. Thorns (Acacia, "
    "cactus) are the most common morphological means of defence (a). Many plants produce and store chemicals that "
    "make the herbivore sick, inhibit feeding or digestion, disrupt reproduction or kill it (b); nicotine, "
    "caffeine, quinine, strychnine and opium are such defences (c). These chemicals deter rather than attract "
    "herbivores (d false), and Calotropis produces highly poisonous cardiac glycosides, so cattle and goats never "
    "browse on it (e false).",
    ["(a) thorns", "(b) defence chemicals", "(c) named chemicals", "(d), (e) false"],
    C12_OP("populations: population interactions (predation)"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (d)' also omits (a).",
    seconds=45)

_rr, _KK = F(1, 5), 1000
_vals = [_rr * 400, _rr * 400 * F(_KK - 400, _KK), _rr * 900 * F(_KK - 900, _KK), _rr * 1000 * 0]
assert _vals == [80, 48, 18, 0]

add(OAP, "Population growth", "Advanced", "match_list",
    "For a population with r = 0.2 per year, compare the exponential model dN/dt = rN with the logistic model "
    "dN/dt = rN[(K − N)/K], taking K = 1000.\n\n" +
    ml(("model and population size", "growth rate (individuals per year)"),
       ["Exponential, N = 400", "Logistic, N = 400", "Logistic, N = 900", "Logistic, N = 1000"],
       ["0", "18", "48", "80"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,II,III,I"), mc("IV,III,I,II")], "D"),
    "Exponential and logistic growth rates compared",
    "Exponential: 0.2 × 400 = 80 (A-IV). Logistic at 400: 0.2 × 400 × 600/1000 = 48 (B-III). Logistic at 900: "
    "0.2 × 900 × 100/1000 = 18 (C-II). At N = K = 1000: 0.2 × 1000 × 0 = 0; the population has reached its "
    "asymptote (D-I).",
    ["Exponential: rN", "Logistic: rN(K − N)/K", "A-IV, B-III, C-II, D-I"],
    C12_OP("populations: population growth"),
    why="The other codes swap the exponential and logistic values at N = 400, or the logistic values at 900 and "
        "1000.",
    seconds=70, verified_by=RECOMPUTED)

add(OAP, "Population attributes", "Advanced", "multi_statement",
    "The age structure of three populations is: P: pre-reproductive 45 per cent, reproductive 40 per cent, "
    "post-reproductive 15 per cent; Q: 35, 36 and 29 per cent; R: 15, 45 and 40 per cent.\n\n" +
    ms("Which of the following inferences are correct?",
       ["The age pyramid of P has a broad base and indicates an expanding population.",
        "The age pyramid of R is urn-shaped and indicates a declining population.",
        "The age pyramid of Q is bell-shaped and indicates a stable population.",
        "Population P is declining, since its post-reproductive group is the smallest.",
        "Population R has the broadest base of the three pyramids."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Reading age pyramids",
    "The shape of the age pyramid reflects the growth status of a population. P has more pre-reproductive than "
    "reproductive individuals: broad base, expanding (a). R has far fewer pre-reproductive than reproductive "
    "individuals: narrow base, urn-shaped, declining (b). In Q the pre-reproductive and reproductive groups are "
    "nearly equal: bell-shaped, stable (c). A small post-reproductive group does not make P decline (d false), "
    "and R has the narrowest, not the broadest, base (e false).",
    ["P: 45 > 40 → expanding", "Q: 35 ≈ 36 → stable", "R: 15 < 45 → declining"],
    C12_OP("populations: population attributes (age pyramids)"),
    why="(d) judges growth from the post-reproductive group; (e) reverses the base widths.",
    seconds=60)

assert abs(math.log(2) / 0.02 - 34.66) < 0.01

add(OAP, "Population growth", "Advanced", "direct",
    "Two populations of the same species grow exponentially with the same r = 0.02 per year: one starts with 100 "
    "individuals and the other with 10,000. Which statement about the time each takes to double is correct? "
    "(Nₜ = N₀e^(rt); ln 2 = 0.693)",
    P("Both take the same time, about 35 years, because the doubling time depends only on r",
      ["The smaller population doubles 100 times faster", "The larger population doubles 100 times faster",
       "The doubling times cannot be compared without knowing the carrying capacity"], "D"),
    "Doubling time in exponential growth",
    "Doubling means Nₜ = 2N₀: 2N₀ = N₀e^(rt), so e^(rt) = 2 and t = ln 2/r = 0.693/0.02 ≈ 34.7 years. N₀ "
    "cancels: under exponential growth, every population with the same r doubles in the same time, whatever its "
    "starting size, although the larger population adds far more individuals in that time.",
    ["2N₀ = N₀e^(rt) → t = ln 2/r", "N₀ cancels", "t = 0.693/0.02 ≈ 35 years for both"],
    C12_OP("populations: population growth (exponential growth)"),
    why="Starting size does not affect the doubling time in the exponential model, and K does not appear in it.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    "Write the effect of an interaction on each partner as + (benefit), − (harm) or 0 (no effect).\n\n" +
    ms("Which of the following pairings are correct?",
       ["Fig and its pollinating wasp: (+, +)",
        "Cattle egret and grazing cattle: (+, 0)",
        "Orchid growing as an epiphyte and the mango branch it grows on: (+, 0)",
        "Cuscuta and the hedge plant on which it grows: (+, 0)",
        "Clown fish and the sea anemone among whose tentacles it lives: (+, +)"]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "A"),
    "Classifying interactions by their effects",
    "Fig and wasp: the wasp pollinates the fig while using its fruit for egg laying and larval food; both "
    "benefit, mutualism (a). Cattle egrets catch insects stirred up by cattle, which are not affected: "
    "commensalism (b). The epiphytic orchid benefits while the mango tree gets no benefit or harm: commensalism "
    "(c). Cuscuta is a parasite deriving nutrition from the host, so the host is harmed: (+, −) (d false). The "
    "clown fish gets protection, and the sea anemone does not appear to derive any benefit: (+, 0), not (+, +) "
    "(e false).",
    ["Mutualism (+, +)", "Commensalism (+, 0)", "Parasitism (+, −)"],
    C12_OP("populations: population interactions"),
    why="Options with (d) or (e) mislabel parasitism or commensalism; '(b), (c) and (d)' also omits (a).",
    seconds=50)

# ================================================================ Ecosystem (4 / 5 / 4)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Structure and components", "Basic", "multi_statement",
    ms("NCERT lists the important components of the functional aspects of an ecosystem, with a pond as its "
       "example. Which of the following are among them?",
       ["Productivity", "Decomposition", "Energy flow", "Stratification", "Species composition"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["c", "d", "e"], ["a", "d", "e"]], "B"),
    "Structural and functional aspects of an ecosystem",
    "NCERT: the important components of an ecosystem's function are (i) productivity, (ii) decomposition, "
    "(iii) energy flow and (iv) nutrient cycling. Species composition (identification and enumeration of species) "
    "and stratification (vertical distribution of species at different levels) are features of an ecosystem's "
    "structure.",
    ["Functions: productivity, decomposition, energy flow, nutrient cycling", "Structure: species composition, "
     "stratification"],
    C12_EC("ecosystem: structure and function"),
    why="Stratification and species composition describe structure, not function, so options with (d) or (e) are "
        "wrong.",
    seconds=30)

add(ECO, "Structure and components", "Basic", "direct",
    "According to NCERT, the autotrophic components of a pond ecosystem include:",
    P("Phytoplankton, some algae, and the floating, submerged and marginal plants found at the edges",
      ["Zooplankton and the free-swimming and bottom-dwelling animals", "Fungi, bacteria and flagellates at the "
       "bottom of the pond", "Only the rooted plants at the edges; phytoplankton are consumers"], "B"),
    "Producers of a pond",
    "NCERT describes the pond: the abiotic component is the water with dissolved inorganic and organic substances "
    "and the rich soil deposit at the bottom; the autotrophic components include the phytoplankton, some algae and "
    "the floating, submerged and marginal plants found at the edges; the consumers are zooplankton and the "
    "free-swimming and bottom-dwelling forms; and the decomposers are fungi, bacteria and flagellates, especially "
    "abundant at the bottom.",
    ["Autotrophs: phytoplankton, algae, floating, submerged and marginal plants", "Consumers: zooplankton and "
     "animals", "Decomposers: fungi, bacteria, flagellates"],
    C12_EC("ecosystem: structure and function (pond)"),
    why="Zooplankton and animals are consumers; fungi, bacteria and flagellates are decomposers; phytoplankton "
        "are producers.",
    seconds=25)

add(ECO, "Ecological pyramids", "Basic", "statement_pair",
    sp("NCERT's ideal pyramid of energy shows that primary producers convert only about 1 per cent of the energy "
       "in the sunlight available to them into net primary productivity.",
       "In an energy pyramid, the energy at a lower trophic level is always more than at a higher level."),
    SP("A"),
    "The ideal pyramid of energy",
    "NCERT's figure of an ideal pyramid of energy notes that primary producers convert only 1 per cent of the "
    "energy in the sunlight available to them into NPP (Statement I true). The pyramid of energy is always "
    "upright: energy at a lower trophic level is always more than at a higher level, because some energy is lost "
    "as heat at each step (Statement II true).",
    ["Statement I: true (1 per cent into NPP)", "Statement II: true (always upright)"],
    C12_EC("ecological pyramids"),
    seconds=30)

add(ECO, "Productivity and decomposition", "Basic", "assertion_reason",
    ar("Decomposers are heterotrophic organisms.",
       "Decomposers make their own food by photosynthesis."),
    AR("C"),
    "Decomposers are heterotrophs",
    "NCERT: decomposers are heterotrophic organisms, mainly fungi and bacteria, which meet their energy and "
    "nutrient requirements by degrading dead organic matter (detritus); they are also called saprotrophs. A is "
    "true. They do not photosynthesise, so R is false.",
    ["A: true", "Energy from dead organic matter, not photosynthesis → R false"],
    C12_EC("energy flow: detritus food chain"),
    seconds=25)

_npp_year = (4 - 4 * F(25, 100)) * 365
assert _npp_year == 1095

add(ECO, "Productivity and decomposition", "Intermediate", "numerical",
    "The gross primary productivity of a grassland averages 4 g m⁻² day⁻¹ (dry weight), and the plants use 25 per "
    "cent of it in respiration. Taking a year as 365 days, what is the net primary productivity of the grassland in "
    "g m⁻² yr⁻¹?",
    P("1,095", ["1,460", "365", "3"], "B"),
    "Net primary productivity and its units",
    "NPP = GPP − R = 4 − (0.25 × 4) = 3 g m⁻² day⁻¹. NCERT expresses productivity per unit area per year, so "
    "3 × 365 = 1,095 g m⁻² yr⁻¹.",
    ["R = 25% of 4 = 1 g m⁻² day⁻¹", "NPP = 3 g m⁻² day⁻¹", "× 365 = 1,095 g m⁻² yr⁻¹"],
    C12_EC("productivity"),
    why="1,460 is the annual GPP (respiration not subtracted); 365 is the annual respiration loss; 3 is the daily "
        "NPP, not the yearly value.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Intermediate", "direct",
    "In cold, waterlogged bogs, partly decomposed plant remains accumulate over many years. Which explanation "
    "fits NCERT's account of decomposition?",
    P("Low temperature and anaerobiosis inhibit decomposition, resulting in a build-up of organic materials",
      ["Water-soluble nutrients are leached away, so decomposers have nothing to act on",
       "Cold, wet conditions speed up humification and mineralisation",
       "Detritivores multiply rapidly in waterlogged soil and convert all detritus into humus at once"], "D"),
    "Climatic control of decomposition",
    "NCERT: decomposition is largely an oxygen-requiring process, and its rate is controlled by the chemical "
    "composition of the detritus and by climatic factors. Warm and moist environments favour decomposition, "
    "whereas low temperature and anaerobiosis inhibit it, resulting in the build-up of organic materials. A cold, "
    "waterlogged bog combines both inhibiting conditions.",
    ["Decomposition needs oxygen and warmth", "Bog: cold + anaerobic", "Decomposition inhibited → organic matter "
     "builds up"],
    C12_EC("decomposition"),
    why="Leaching removes only soluble nutrients, not the detritus; cold, wet, anoxic conditions slow, not speed, "
        "decomposition; and detritivores do not thrive under anaerobiosis.",
    seconds=40)

add(ECO, "Energy flow", "Intermediate", "multi_statement",
    "In a lake, phytoplankton are eaten by zooplankton and by molluscs; small fish eat zooplankton; large fish eat "
    "small fish and molluscs; and kingfishers eat small fish and large fish. Take producers as the first trophic "
    "level.\n\n" +
    ms("Which of the following statements are correct?",
       ["The molluscs are herbivores (primary consumers).",
        "The large fish occupies the third and the fourth trophic levels.",
        "The kingfisher occupies the fourth and the fifth trophic levels.",
        "The small fish is a primary consumer.",
        "The zooplankton are producers."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Trophic levels in a food web",
    "Phytoplankton (1) → molluscs and zooplankton (2): both are primary consumers; NCERT names molluscs as the "
    "common herbivores of aquatic ecosystems (a). Small fish eat zooplankton: level 3, a secondary consumer (d "
    "false). Large fish eat molluscs (level 3) and small fish (level 4) (b). Kingfishers eat small fish (level 4) "
    "and large fish (levels 4 and 5) (c). Zooplankton are consumers (e false).",
    ["Molluscs, zooplankton: level 2", "Small fish: level 3", "Large fish: 3 and 4", "Kingfisher: 4 and 5"],
    C12_EC("energy flow: food chains and food web"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (e)' also omits (a).",
    seconds=70)

add(ECO, "Productivity and decomposition", "Intermediate", "statement_pair",
    sp("Identical leaf litter can decompose at different rates in two regions, because decomposition is controlled "
       "by climatic factors such as temperature and soil moisture.",
       "Humus is decomposed rapidly by microbes, so it cannot serve as a reservoir of nutrients."),
    SP("C"),
    "Rate of decomposition and humus",
    "NCERT: the rate of decomposition is controlled by the chemical composition of the detritus and by climatic "
    "factors; temperature and soil moisture are the most important climatic factors (Statement I true). Humus is "
    "highly resistant to microbial action and undergoes decomposition at an extremely slow rate; being colloidal, "
    "it serves as a reservoir of nutrients (Statement II false).",
    ["Statement I: true", "Humus: extremely slow decomposition, nutrient reservoir → Statement II false"],
    C12_EC("decomposition"),
    seconds=35)

_pc, _tc = 708_000, 3
assert round(_pc / _tc) == 236_000

add(ECO, "Ecological pyramids", "Intermediate", "direct",
    "In a grassland, the counts per unit area are: primary producers 58,42,000; primary consumers 7,08,000; "
    "secondary consumers 3,54,000; tertiary consumers 3. About how many primary consumers are there for each "
    "tertiary consumer, and what is the shape of this pyramid of numbers?",
    P("About 2.4 lakh; upright", ["About 2; upright", "About 2.4 lakh; inverted", "About 19 lakh; inverted"], "B"),
    "Reading a pyramid of numbers",
    "Primary consumers per tertiary consumer = 7,08,000/3 = 2,36,000 ≈ 2.4 lakh. The numbers fall at each higher "
    "trophic level (58,42,000 > 7,08,000 > 3,54,000 > 3), with producers forming the broad base and top "
    "carnivores the apex, so the pyramid is upright.",
    ["7,08,000 ÷ 3 ≈ 2,36,000", "Numbers decrease upward → upright"],
    C12_EC("ecological pyramids"),
    why="2 is the ratio of primary to secondary consumers; the pyramid is not inverted, since every level has fewer "
        "individuals than the one below; 19 lakh divides the producers by 3.",
    seconds=45, verified_by=RECOMPUTED)

_e = [50_000]
for _eff in (F(10, 100), F(15, 100), F(20, 100)):
    _e.append(_e[-1] * _eff)
assert _e == [50_000, 5_000, 750, 150] and _e[0] - _e[1] == 45_000

add(ECO, "Energy flow", "Advanced", "match_list",
    "In a grazing food chain, the producers fix 50,000 kJ. The herbivores obtain 10 per cent of the producers' "
    "energy, the primary carnivores 15 per cent of the herbivores' energy, and the secondary carnivores 20 per "
    "cent of the primary carnivores' energy.\n\n" +
    ml(("quantity", "energy (kJ)"),
       ["Energy obtained by the herbivores", "Energy obtained by the primary carnivores",
        "Energy obtained by the secondary carnivores", "Energy of the producers not passed on to the herbivores"],
       ["150", "750", "5,000", "45,000"]),
    M(mc("III,II,I,IV"), [mc("III,I,II,IV"), mc("IV,II,I,III"), mc("III,II,IV,I")], "B"),
    "Energy transfer with different efficiencies",
    "Herbivores: 10% of 50,000 = 5,000 kJ (A-III). Primary carnivores: 15% of 5,000 = 750 kJ (B-II). Secondary "
    "carnivores: 20% of 750 = 150 kJ (C-I). Energy not passed to herbivores: 50,000 − 5,000 = 45,000 kJ, lost in "
    "respiration as heat or passed to the detritus food chain (D-IV).",
    ["5,000", "750", "150", "45,000"],
    C12_EC("energy flow"),
    why="The other codes swap the carnivore values, or the herbivore energy with the energy not passed on.",
    seconds=70, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Advanced", "multi_statement",
    ms("Which of the following predictions about decomposition are correct according to NCERT?",
       ["Identical nitrogen-rich litter decomposes faster in a warm, moist plot than in a cold plot.",
        "In waterlogged soil with anaerobic conditions, organic matter tends to build up.",
        "Leaching can carry water-soluble inorganic nutrients down into the soil horizon, where they precipitate "
        "as unavailable salts.",
        "Earthworms carry out the catabolism of detritus by secreting enzymes that convert it into simple inorganic "
        "substances.",
        "Detritus rich in lignin decomposes faster than detritus rich in water-soluble sugars."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
    "Applying the controls of decomposition",
    "Warm, moist conditions favour decomposition (a); low temperature and anaerobiosis inhibit it, so organic "
    "matter builds up (b). In leaching, water-soluble inorganic nutrients go down into the soil horizon and get "
    "precipitated as unavailable salts (c). Earthworms are detritivores that fragment detritus; catabolism is the "
    "enzymatic degradation by bacteria and fungi (d false). Lignin- and chitin-rich detritus decomposes slowly, "
    "while nitrogen- and sugar-rich detritus decomposes quickly (e false).",
    ["(a), (b) climate", "(c) leaching", "(d) fragmentation, not catabolism", "(e) lignin is slow"],
    C12_EC("decomposition"),
    why="Options with (d) or (e) contain a false statement.",
    seconds=50)

_e2 = 10**6 * F(1, 100) * F(1, 10) * F(1, 10)
assert _e2 == 100

add(ECO, "Energy flow", "Advanced", "direct",
    "The sunlight available to the producers of an ecosystem is 10⁶ J. Assume that the producers convert 1 per "
    "cent of it into net primary productivity and that 10 per cent of the energy passes from each trophic level to "
    "the next. How much energy reaches the primary carnivores?",
    P("100 J", ["1,000 J", "10,000 J", "10 J"], "C"),
    "From sunlight to carnivores",
    "NPP = 1% of 10⁶ J = 10⁴ J. Herbivores (second trophic level) get 10% of this = 10³ J. Primary carnivores "
    "(third trophic level) get 10% of that = 100 J.",
    ["NPP = 10⁶ × 0.01 = 10,000 J", "Herbivores = 1,000 J", "Primary carnivores = 100 J"],
    C12_EC("energy flow; ecological pyramids"),
    why="10,000 J is the NPP, 1,000 J reaches the herbivores, and 10 J would be the secondary carnivores' share.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Ecological pyramids", "Advanced", "statement_pair",
    sp("In a sea, the pyramid of biomass is generally inverted, while the pyramid of energy is upright.",
       "This shows that the 10 per cent law of energy transfer does not apply in the sea."),
    SP("C"),
    "Inverted biomass but upright energy",
    "NCERT: the pyramid of biomass in a sea is generally inverted because the biomass of fishes far exceeds that "
    "of phytoplankton, but the pyramid of energy is always upright, because some energy is always lost as heat at "
    "each step (Statement I true). The upright energy pyramid of the sea shows that energy still decreases at each "
    "trophic level; the inverted biomass pyramid concerns standing crop at one time, not energy flow, so it gives "
    "no reason to reject the 10 per cent law (Statement II false).",
    ["Statement I: true", "Energy still decreases upward → Statement II false"],
    C12_EC("ecological pyramids"),
    seconds=45)

# ================================================================ Biodiversity and Conservation (4 / 5 / 4)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Hotspots and Red Data Book", "Basic", "direct",
    "India's regions of exceptionally high biodiversity are covered by three of the world's biodiversity hotspots. "
    "Which option names them?",
    P("Western Ghats and Sri Lanka, Indo-Burma, and Himalaya",
      ["Western Ghats and Sri Lanka, Eastern Ghats, and Himalaya", "Indo-Burma, Thar Desert, and Sundarbans",
       "Himalaya, Eastern Ghats, and Andaman Islands"], "A"),
    "Hotspots covering India",
    "NCERT: three hotspots, Western Ghats and Sri Lanka, Indo-Burma and Himalaya, cover our country's "
    "exceptionally high biodiversity regions. Hotspots are regions with very high levels of species richness and "
    "a high degree of endemism.",
    ["Western Ghats and Sri Lanka", "Indo-Burma", "Himalaya"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity (hotspots)"),
    why="The Eastern Ghats, Thar Desert, Sundarbans and Andaman Islands are not among the three hotspots NCERT "
        "lists for India.",
    seconds=25)

add(BDC, "Patterns of biodiversity", "Basic", "statement_pair",
    sp("For many taxonomic groups, species inventories are more complete in temperate than in tropical countries.",
       "An overwhelmingly large proportion of the species waiting to be discovered are in the tropics."),
    SP("A"),
    "Where species remain to be discovered",
    "NCERT: there are two kinds of estimates of species numbers: those already described and an estimate of the "
    "total. For many taxonomic groups, species inventories are more complete in temperate than in tropical "
    "countries (Statement I true), and an overwhelmingly large proportion of the species waiting to be discovered "
    "are in the tropics (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_BD("biodiversity: how many species are there on earth"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "According to NCERT, some extreme estimates of the total number of species on earth range from:",
    P("20 to 50 million", ["2 to 5 million", "1.5 to 2 million", "200 to 500 million"], "D"),
    "Estimates of global species diversity",
    "NCERT: some extreme estimates range from 20 to 50 million, but a more conservative and scientifically sound "
    "estimate made by Robert May places global species diversity at about 7 million. The number of species "
    "already described is slightly more than 1.5 million (IUCN, 2004).",
    ["Extreme estimates: 20–50 million", "May's estimate: about 7 million", "Described: about 1.5 million"],
    C12_BD("biodiversity: how many species are there on earth"),
    why="1.5–2 million is near the number already described; 2–5 million is below May's estimate; 200–500 million "
        "is a factor-of-ten slip.",
    seconds=25)

add(BDC, "Importance and loss", "Basic", "assertion_reason",
    ar("Nations endowed with rich biodiversity can expect to reap enormous benefits.",
       "With increasing resources put into bioprospecting, the molecular, genetic and species-level diversity is "
       "being explored for products of economic importance."),
    AR("A"),
    "Bioprospecting and the narrowly utilitarian argument",
    "NCERT (narrowly utilitarian argument): bioprospecting is exploring molecular, genetic and species-level "
    "diversity for products of economic importance. With increasing resources put into bioprospecting, nations "
    "endowed with rich biodiversity can expect to reap enormous benefits. The benefits arise because the diversity "
    "is being explored for valuable products, so R explains A.",
    ["Bioprospecting explores diversity for products", "More diversity → more potential products", "R explains "
     "A"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Intermediate", "direct",
    "Robert May's estimate of global species diversity rests on a method described in NCERT. Biologists:",
    P("Make a statistical comparison of the temperate–tropical species richness of an exhaustively studied group "
      "of insects and extrapolate this ratio to other groups of animals and plants",
      ["Count every species in a sample plot of tropical forest and multiply by the area of the earth",
       "Use the slope Z of the species–area relationship for whole continents",
       "Add up the species listed in the IUCN Red List"], "D"),
    "How the total number of species is estimated",
    "NCERT: since an overwhelmingly large proportion of undiscovered species are in the tropics, biologists make a "
    "statistical comparison of the temperate–tropical species richness of an exhaustively studied group of "
    "insects and extrapolate this ratio to other groups of animals and plants to come up with a gross estimate of "
    "the total number of species on earth. May's conservative estimate is about 7 million.",
    ["Well-studied insect group", "Temperate : tropical richness ratio", "Extrapolated to other groups → ~7 "
     "million"],
    C12_BD("biodiversity: how many species are there on earth"),
    why="NCERT describes extrapolation of a temperate–tropical ratio, not plot counts scaled to the earth, the "
        "species–area slope or Red List totals.",
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "multi_statement",
    ms("A large forest is broken up by roads and farms into small, isolated fragments. According to NCERT, which "
       "of the following consequences are expected?",
       ["Mammals and birds requiring large territories are badly affected.",
        "Certain animals with migratory habits are badly affected.",
        "Populations of such animals decline.",
        "All species benefit, because the forest edges increase.",
        "Only plant species are affected; animals simply move elsewhere."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
    "Effects of habitat fragmentation",
    "NCERT: when large habitats are broken up into small fragments due to various human activities, mammals and "
    "birds requiring large territories and certain animals with migratory habits are badly affected, leading to "
    "population declines. Habitat loss and fragmentation is the most important cause driving animals and plants to "
    "extinction, so (d) and (e) are false.",
    ["Large-territory mammals and birds (a)", "Migratory animals (b)", "Population declines (c)"],
    C12_BD("loss of biodiversity: causes (habitat loss and fragmentation)"),
    why="Options with (d) or (e) contradict NCERT; '(a), (c) and (e)' also omits migratory animals.",
    seconds=40)

add(BDC, "In situ and ex situ conservation", "Intermediate", "assertion_reason",
    ar("Ex situ conservation is the approach that protects the whole ecosystem in which a threatened species "
       "lives.",
       "When we conserve and protect the whole ecosystem, its biodiversity at all levels is protected; for "
       "example, we save the entire forest to save the tiger."),
    AR("D"),
    "In situ protects the whole ecosystem",
    "NCERT: when we conserve and protect the whole ecosystem, its biodiversity at all levels is protected, as in "
    "saving the entire forest to save the tiger: this is in situ (on site) conservation (R true). Ex situ (off "
    "site) conservation takes threatened animals and plants out of their natural habitat and places them in "
    "special settings such as zoological parks, botanical gardens and seed banks, so A is false.",
    ["Whole ecosystem protected → in situ", "Ex situ: outside the natural habitat → A false", "R: true"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity"),
    seconds=35)

_ratio = 8.1 / 2.4
assert 3.3 < _ratio < 3.5

add(BDC, "Patterns of biodiversity", "Intermediate", "direct",
    "India has only 2.4 per cent of the world's land area but 8.1 per cent of the global species diversity. Relative "
    "to the world average, about how many times as many species per unit land area does this imply for India?",
    P("About 3.4 times", ["About 5.7 times", "About 0.3 times", "About 19 times"], "B"),
    "India's share of global species diversity",
    "Species per unit area relative to the world average = (share of species)/(share of land) = 8.1/2.4 ≈ 3.4. "
    "NCERT uses these figures to show that India, one of the 12 megadiversity countries, is far richer in species "
    "than its land area alone would suggest.",
    ["Ratio = 8.1 ÷ 2.4", "≈ 3.4 times"],
    C12_BD("biodiversity: how many species are there on earth and how many in India"),
    why="5.7 is the difference of the percentages, not a ratio; 0.3 inverts the ratio; 19 multiplies the two "
        "percentages.",
    seconds=35, verified_by=RECOMPUTED)

add(BDC, "Patterns of biodiversity", "Intermediate", "multi_statement",
    ms("Which of the following are examples of genetic diversity given in NCERT?",
       ["Variation in the potency and concentration of the active chemical reserpine in Rauwolfia vomitoria growing "
        "in different Himalayan ranges",
        "India has more than 50,000 genetically different strains of rice.",
        "India has 1,000 varieties of mango.",
        "The Western Ghats have a greater amphibian species diversity than the Eastern Ghats.",
        "India has a greater ecosystem diversity than a Scandinavian country like Norway."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "A"),
    "Levels of biodiversity",
    "NCERT's examples of genetic diversity within a species: Rauwolfia vomitoria from different Himalayan ranges, "
    "differing in the potency and concentration of reserpine (a); more than 50,000 genetically different strains "
    "of rice (b) and 1,000 varieties of mango (c) in India. The Western Ghats' amphibian richness is NCERT's "
    "example of species diversity (d), and India versus Norway illustrates ecological diversity (e).",
    ["Genetic: (a), (b), (c)", "Species: (d)", "Ecological: (e)"],
    C12_BD("biodiversity: levels of biodiversity"),
    why="Options with (d) or (e) mix in NCERT's examples of species and ecological diversity.",
    seconds=40)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Community P has many more species than an otherwise similar community Q. On the basis of NCERT's account "
       "of biodiversity and ecosystem stability, which predictions are reasonable?",
       ["P will show less year-to-year variation in total biomass than Q.",
        "P will tend to have higher productivity than Q.",
        "P will be more resistant to invasions by alien species than Q.",
        "P will be more susceptible to environmental perturbations such as drought than Q.",
        "Loss of a few species from P can never affect any of its ecosystem processes."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "Species richness and stability",
    "NCERT: ecologists believe communities with more species tend to be more stable. A stable community should "
    "not show too much variation in productivity from year to year, should be resistant or resilient to "
    "occasional disturbance, and should be resistant to invasions by alien species. Tilman found that plots with "
    "more species showed less year-to-year variation in total biomass and that increased diversity contributed to "
    "higher productivity (a, b, c). Loss of biodiversity lowers resistance to perturbations such as drought (d "
    "false) and may increase variability in ecosystem processes; losing a key species can be serious (e false).",
    ["Tilman: less variation, higher productivity", "Stable: resistant to aliens", "(d), (e) contradict NCERT"],
    C12_BD("patterns of biodiversity: importance of species diversity to the ecosystem"),
    why="Options with (d) or (e) contain a false prediction; '(b), (c) and (d)' also omits (a).",
    seconds=55)

_C, _Z, _A = 10, F(1, 5), 10**5
assert 10 ** (math.log10(_C) + float(_Z) * math.log10(_A)) == 100

add(BDC, "Patterns of biodiversity", "Advanced", "direct",
    "For islands within a region, the species–area relationship is log S = log C + Z log A, with C = 10 and Z = 0.2 "
    "(area in km²). How many species are expected on an island of 1,00,000 km²?",
    P("100", ["20,000", "50", "1,000"], "C"),
    "Using the species–area equation",
    "log A = log 10⁵ = 5. log S = log 10 + 0.2 × 5 = 1 + 1 = 2, so S = 10² = 100 species. Equivalently, "
    "S = C·A^Z = 10 × (10⁵)^0.2 = 10 × 10 = 100.",
    ["log A = 5", "log S = 1 + 0.2 × 5 = 2", "S = 100"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    why="20,000 multiplies Z by A instead of using logarithms; 50 halves the answer; 1,000 comes from slips such as "
        "taking Z = 0.4 (log S = 1 + 2 = 3).",
    seconds=60, verified_by=RECOMPUTED)

add(BDC, "Importance and loss", "Advanced", "assertion_reason",
    ar("When alien species are introduced unintentionally or deliberately, some of them turn invasive and cause "
       "the decline or extinction of indigenous species.",
       "Parthenium, Lantana and water hyacinth are indigenous Indian species that have been threatened by "
       "over-exploitation."),
    AR("C"),
    "Alien species invasions",
    "NCERT: when alien species are introduced, some of them turn invasive and cause decline or extinction of "
    "indigenous species (A true), as with the Nile perch in Lake Victoria. NCERT cites carrot grass (Parthenium), "
    "Lantana and water hyacinth (Eichhornia) as invasive weed species that have posed a threat to our native "
    "species; they are aliens, not threatened indigenous species, so R is false.",
    ["A: true", "Parthenium, Lantana, Eichhornia: invasive aliens → R false"],
    C12_BD("loss of biodiversity: causes (alien species invasions)"),
    seconds=40)

add(BDC, "In situ and ex situ conservation", "Advanced", "multi_statement",
    ms("Which of the following measures are correctly classified?",
       ["Propagating a rare orchid by tissue culture: ex situ conservation",
        "Declaring the forest habitat of an endangered deer a biosphere reserve: in situ conservation",
        "Storing the sperm of a threatened mammal by cryopreservation: ex situ conservation",
        "Keeping animals in a wildlife safari park: in situ conservation",
        "Protecting a sacred grove: ex situ conservation"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Classifying conservation measures",
    "NCERT: in situ conservation protects species in their natural habitat, e.g. biosphere reserves, national "
    "parks, wildlife sanctuaries and sacred groves. Ex situ conservation protects them outside their natural "
    "habitat: zoological parks, botanical gardens, wildlife safari parks, cryopreservation of gametes, in vitro "
    "fertilisation, tissue culture propagation and seed banks. So (a), (b) and (c) are correctly classified, while "
    "safari parks are ex situ (d false) and sacred groves are in situ (e false).",
    ["In situ: biosphere reserve, sacred grove", "Ex situ: tissue culture, cryopreservation, safari park"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity"),
    why="Options with (d) or (e) reverse the class of safari parks or sacred groves.",
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
    assert len(QUESTIONS) == pkg["count"] == 120, len(QUESTIONS)
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_008", "created_at": TODAY,
           "notes": "BATCH_008 package BOT_008_p2: 120 original Botany questions (Sexual Reproduction in Flowering Plants to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 to "
                    "BATCH_006 were avoided or approached from a new angle. Numerical and other computable answers "
                    "re-derived by tools/batch_008/BOT_008_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()
