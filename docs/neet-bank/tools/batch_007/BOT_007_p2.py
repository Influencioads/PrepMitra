"""Builder for BATCH_007, package BOT_007_p2 (Botany, NEET_BOT_001626..NEET_BOT_001750, 125 questions).

Topics: Plant Growth and Development; Sexual Reproduction in Flowering Plants; Principles of Inheritance and
Variation; Molecular Basis of Inheritance; Microbes in Human Welfare; Organisms and Populations; Ecosystem;
Biodiversity and Conservation. All questions are original and every fact is taken from the rationalised NCERT
Class 11-12 Biology textbooks. Facts already tested in BATCH_000 to BATCH_006 on these topics were avoided or
approached from a new angle (see `python tools/merge_batch.py stems 007 BOT_007_p2`). Computable answers are
re-derived below; the file is written only if every assert, the plan quota, the format mix and the answer-key
balance pass.

    cd docs/neet-bank && python tools/batch_007/BOT_007_p2.py
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
PACKAGE = "BOT_007_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_007_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_007_BOT_p2.json"
FIRST_ID = 1626

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


# ================================================================ Plant Growth and Development (4 / 5 / 4)
C11_PGD = lambda s: ref(11, PGD, s)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "According to NCERT, spraying a sugarcane crop with gibberellins increases the length of the stem and so "
    "increases the yield by as much as:",
    P("20 tonnes per acre", ["2 tonnes per acre", "200 tonnes per acre", "20 kilograms per acre"], "A"),
    "Commercial use of gibberellins in sugarcane",
    "NCERT: sugarcane stores carbohydrate as sugar in its stem. Spraying the crop with gibberellins increases the "
    "length of the stem, thus increasing the yield by as much as 20 tonnes per acre.",
    ["GA spray lengthens the sugarcane stem", "Longer stem stores more sugar", "Yield increase: up to 20 tonnes per "
     "acre"],
    C11_PGD("plant growth regulators: physiological effects of gibberellins"),
    why="2 and 200 tonnes are factor-of-ten slips; 20 kilograms per acre changes the unit.",
    seconds=20)

add(PGD, "Germination and growth phases", "Basic", "direct",
    "NCERT illustrates the phases of growth in a root with the 'parallel line technique'. This technique is used to "
    "detect:",
    P("The zone of elongation: the zones immediately behind the apex are found to have elongated the most",
      ["The zone of cell division: the root cap is found to have elongated the most",
       "The zone of maturation: the region farthest from the apex is found to have elongated the most",
       "Geometric growth: every zone of the root is found to have elongated equally"], "C"),
    "Detecting the zone of elongation",
    "Lines are marked at equal distances on a growing root and their spacing is checked after some time. NCERT's "
    "figure: detection of zones of elongation by the parallel line technique; the zones immediately behind the apex "
    "have elongated most. These lie proximal to the meristematic phase, in the phase of elongation.",
    ["Equally spaced marks on a young root", "After growth, marks just behind the apex have moved apart the most",
     "That region is the zone of elongation"],
    C11_PGD("growth: phases of growth"),
    why="The root cap and the zone of maturation do not show the largest elongation, and the marks do not move apart "
        "equally, so the elongation is not uniform along the root.",
    seconds=30)

add(PGD, "Plant growth regulators", "Basic", "statement_pair",
    sp("Auxins are generally produced by the growing apices of the stems and roots, from where they migrate to the "
       "regions of their action.",
       "IAA and IBA are synthetic auxins, whereas NAA and 2,4-D have been isolated from plants."),
    SP("C"),
    "Natural and synthetic auxins",
    "NCERT: auxins are generally produced by the growing apices of the stems and roots, from where they migrate to "
    "the regions of their action (Statement I true). Auxins like IAA and indole butyric acid (IBA) have been isolated "
    "from plants, while NAA (naphthalene acetic acid) and 2,4-D (2,4-dichlorophenoxyacetic acid) are synthetic "
    "auxins. Statement II swaps the two groups, so it is false.",
    ["Statement I: true", "IAA, IBA: natural; NAA, 2,4-D: synthetic", "Statement II: false"],
    C11_PGD("plant growth regulators: auxins"),
    seconds=30)

add(PGD, "Plant growth regulators", "Basic", "direct",
    "According to NCERT, the term 'auxin' is applied to:",
    P("Indole-3-acetic acid (IAA) and other natural and synthetic compounds having certain growth-regulating "
      "properties",
      ["Only the indole-3-acetic acid isolated from the tips of oat coleoptiles",
       "Only the synthetic compounds NAA and 2,4-D used as herbicides",
       "All five major groups of plant growth regulators taken together"], "D"),
    "Meaning of the term auxin",
    "NCERT: auxin (from the Greek 'auxein', to grow) was first isolated from human urine. The term 'auxin' is "
    "applied to indole-3-acetic acid (IAA) and to other natural and synthetic compounds having certain growth "
    "regulating properties.",
    ["Auxin: IAA plus other natural and synthetic compounds", "Common feature: certain growth-regulating "
     "properties"],
    C11_PGD("plant growth regulators: auxins"),
    why="The term is not limited to IAA alone or to the synthetic compounds alone, and it does not cover the other "
        "PGR groups (gibberellins, cytokinins, ABA, ethylene).",
    seconds=25)

add(PGD, "Differentiation and redifferentiation", "Intermediate", "direct",
    "NCERT presents the sequence of the developmental process in a plant cell as a flow chart, starting from a "
    "meristematic cell. Which order of steps is correct?",
    P("Cell division → plasmatic growth → expansion (elongation) → cell differentiation",
      ["Cell division → expansion (elongation) → plasmatic growth → cell differentiation",
       "Plasmatic growth → cell division → cell differentiation → expansion (elongation)",
       "Cell division → cell differentiation → plasmatic growth → expansion (elongation)"], "B"),
    "Sequence of developmental process in a plant cell",
    "In NCERT's flow chart, a meristematic cell undergoes cell division, then plasmatic growth (increase in "
    "protoplasm), then expansion (elongation), and then cell differentiation, giving a mature cell; a mature cell "
    "may later dedifferentiate and redifferentiate. The order matches the phases of growth: meristematic cells rich "
    "in protoplasm come first, cells of the elongation zone enlarge and become vacuolated next, and differentiation "
    "into mature cells comes last.",
    ["Start: cell division in the meristematic cell", "Then plasmatic growth, then expansion (elongation)",
     "Last: cell differentiation to a mature cell"],
    C11_PGD("development: sequence of the developmental process in a plant cell"),
    why="Expansion does not come before plasmatic growth, division does not follow plasmatic growth at the start, "
        "and differentiation is the last step, not the second.",
    seconds=40)

add(PGD, "Plant growth regulators", "Intermediate", "assertion_reason",
    ar("Cytokinins help to delay leaf senescence.",
       "Cytokinins promote nutrient mobilisation."),
    AR("A"),
    "Cytokinins and senescence",
    "NCERT: cytokinins promote nutrient mobilisation, which helps in the delay of leaf senescence. Both statements are "
    "true, and the nutrient mobilisation stated in R is the very process through which cytokinins delay senescence "
    "(A).",
    ["A: true", "R: true", "Nutrient mobilisation (R) delays leaf senescence (A): R explains A"],
    C11_PGD("plant growth regulators: physiological effects of cytokinins"),
    seconds=30)

add(PGD, "Plant growth regulators", "Intermediate", "statement_pair",
    sp("Ethylene influences horizontal growth of seedlings and swelling of the axis in dicot seedlings.",
       "All gibberellins are acidic."),
    SP("A"),
    "Ethylene on seedlings; nature of gibberellins",
    "NCERT: ethylene influences horizontal growth of seedlings, swelling of the axis and apical hook formation in "
    "dicot seedlings (Statement I true). There are more than 100 gibberellins (GA1, GA2, GA3 and so on) and all GAs "
    "are acidic (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C11_PGD("plant growth regulators: gibberellins and ethylene"),
    seconds=30)

add(PGD, "Plant growth regulators", "Intermediate", "match_list",
    ml(("aim of the grower", "plant growth regulator used, as described in NCERT"),
       ["Obtaining parthenocarpic (seedless) tomatoes", "Making a rosette plant such as cabbage bolt",
        "Hastening the ripening of apples with an aqueous spray", "Promoting adventitious shoot formation"],
       ["Ethephon", "Cytokinin", "Auxin", "Gibberellin"]),
    M(mc("III,IV,I,II"), [mc("IV,III,I,II"), mc("III,IV,II,I"), mc("I,IV,III,II")], "B"),
    "Practical uses of PGRs",
    "Auxins induce parthenocarpy, e.g. in tomatoes. Gibberellins promote bolting (internode elongation just prior to "
    "flowering) in beet, cabbages and other rosette plants. Ethephon, an aqueous solution readily absorbed and "
    "transported in the plant, releases ethylene slowly and hastens fruit ripening in tomatoes and apples. "
    "Cytokinins help to produce new leaves, chloroplasts, lateral shoot growth and adventitious shoot formation.",
    ["A: auxin (III)", "B: gibberellin (IV)", "C: ethephon (I)", "D: cytokinin (II)"],
    C11_PGD("plant growth regulators: physiological effects"),
    why="Other codes swap auxin with gibberellin, ethephon with cytokinin, or auxin with ethephon; none of these "
        "pairings is given in NCERT.",
    seconds=45)

add(PGD, "Plant growth regulators", "Intermediate", "direct",
    "Which one of the following is NOT an effect of gibberellins described in NCERT?",
    P("Inducing dormancy in seeds and helping them to withstand desiccation",
      ["Promoting bolting in beet, cabbages and other plants with a rosette habit",
       "Speeding up the malting process in the brewing industry",
       "Increasing the length of grape stalks"], "C"),
    "Gibberellins versus abscisic acid",
    "NCERT lists for gibberellins: increase in the length of grape stalks, elongation of fruits such as apple, delay "
    "of senescence, malting in the brewing industry, increase in sugarcane yield, early seed production in conifers "
    "and bolting in rosette plants. Inducing seed dormancy and helping seeds to withstand desiccation are roles of "
    "abscisic acid, which in most situations acts as an antagonist to gibberellins.",
    ["Bolting, malting and grape stalk elongation: gibberellins", "Seed dormancy and desiccation tolerance: abscisic "
     "acid"],
    C11_PGD("plant growth regulators: gibberellins and abscisic acid"),
    why="Bolting, malting and the elongation of grape stalks are all effects of gibberellins named in NCERT.",
    seconds=30)

add(PGD, "Plant growth regulators", "Advanced", "multi_statement",
    ms("Each statement below credits one plant growth regulator with two effects. In which statements are BOTH "
       "effects correctly assigned according to NCERT?",
       ["Auxin: initiates rooting in stem cuttings and induces parthenocarpy in tomatoes.",
        "Gibberellin: increases the length of grape stalks and speeds up the malting process.",
        "Cytokinin: helps to overcome apical dominance and promotes adventitious shoot formation.",
        "Ethylene: initiates germination in peanut seeds and stimulates the closure of stomata.",
        "Abscisic acid: inhibits seed germination and promotes female flowers in cucumbers."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "c", "d"]], "D"),
    "Matching paired effects to one PGR",
    "(a) Both are auxin effects. (b) Both are gibberellin effects. (c) Both are cytokinin effects. (d) Ethylene does "
    "break seed and bud dormancy and initiates germination in peanut seeds, but the closure of stomata is stimulated "
    "by abscisic acid, so (d) is wrong. (e) Abscisic acid does inhibit seed germination, but promoting female "
    "flowers in cucumbers is an ethylene effect, so (e) is wrong.",
    ["(a), (b), (c): both halves correct", "(d): stomatal closure is ABA, not ethylene",
     "(e): female flowers in cucumber is ethylene, not ABA"],
    C11_PGD("plant growth regulators: physiological effects"),
    why="Each wrong option includes (d) or (e), each of which pairs one correct effect with an effect of a different "
        "PGR; '(b), (c) and (d) only' also leaves out the correct (a).",
    seconds=70)

add(PGD, "Plant growth regulators", "Advanced", "assertion_reason",
    ar("Spraying juvenile conifers with gibberellins leads to early seed production.",
       "Gibberellins are used to speed up the malting process in the brewing industry."),
    AR("B"),
    "Two separate uses of gibberellins",
    "NCERT: spraying juvenile conifers with GAs hastens the maturity period, thus leading to early seed production "
    "(A true). Gibberellins are also used to speed up the malting process in the brewing industry (R true). R is a "
    "different application of the same hormone in a different setting; malting has nothing to do with why conifers "
    "mature early, so R does not explain A.",
    ["A: true (GAs hasten the maturity period)", "R: true (malting)", "R is an unrelated use: not the explanation"],
    C11_PGD("plant growth regulators: physiological effects of gibberellins"),
    seconds=35)

add(PGD, "Plant growth regulators", "Advanced", "direct",
    "F. Skoog observed that callus from the internodal segments of tobacco stems proliferated only if, in addition "
    "to auxins, the nutrient medium contained extracts such as yeast extract or coconut milk. According to NCERT, "
    "which naturally occurring plant growth regulator was later isolated from coconut milk?",
    P("Zeatin, a cytokinin",
      ["Kinetin, a cytokinin", "Indole-3-butyric acid, an auxin", "Gibberellic acid (GA₃), a gibberellin"], "A"),
    "From Skoog's observation to natural cytokinins",
    "Skoog and Miller later crystallised the cytokinesis-promoting substance and named it kinetin, but kinetin was "
    "obtained from autoclaved herring sperm DNA and does not occur naturally in plants. The search for natural "
    "substances with cytokinin-like activity led to the isolation of zeatin from corn kernels and coconut milk.",
    ["Coconut milk supported cell division in tobacco callus", "Kinetin: from autoclaved herring sperm DNA, not "
     "natural", "Natural cytokinin from corn kernels and coconut milk: zeatin"],
    C11_PGD("plant growth regulators: discovery of cytokinins"),
    why="Kinetin came from autoclaved herring sperm DNA and does not occur naturally in plants; IBA and GA₃ are not "
        "described as isolated from coconut milk.",
    seconds=50)

add(PGD, "Plant growth regulators", "Advanced", "statement_pair",
    sp("Abscisic acid plays an important role in seed development, maturation and dormancy.",
       "In most situations, abscisic acid acts synergistically with gibberellins."),
    SP("C"),
    "Abscisic acid and its relation to gibberellins",
    "NCERT: ABA plays an important role in seed development, maturation and dormancy; by inducing dormancy it helps "
    "seeds to withstand desiccation (Statement I true). NCERT adds that in most situations ABA acts as an antagonist "
    "to GAs, not synergistically (Statement II false).",
    ["Statement I: true", "ABA and GAs: antagonists in most situations", "Statement II: false"],
    C11_PGD("plant growth regulators: abscisic acid"),
    seconds=35)

# ================================================================ Sexual Reproduction in Flowering Plants (7 / 9 / 7)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "NCERT states that the mitotic divisions leading from the functional megaspore to the 8-nucleate embryo sac are "
    "strictly free nuclear. This means that:",
    P("The nuclear divisions are not followed immediately by cell wall formation",
      ["Each nuclear division is immediately followed by cell wall formation",
       "The divisions are meiotic, so the chromosome number is halved at each step",
       "The nuclei divide without any replication of their DNA"], "B"),
    "Free-nuclear divisions in the embryo sac",
    "NCERT: the nucleus of the functional megaspore divides mitotically to form two nuclei, which move to opposite "
    "poles; two more sequential mitotic nuclear divisions give the 4-nucleate and 8-nucleate stages. These mitotic "
    "divisions are strictly free nuclear, that is, nuclear divisions are not followed immediately by cell wall "
    "formation. Walls form only later, around six of the eight nuclei.",
    ["Free nuclear = nuclei divide, walls do not form at once", "The divisions are mitotic, not meiotic"],
    C12_SR("pistil, megasporangium and embryo sac: megasporogenesis"),
    why="Immediate wall formation is the opposite of free-nuclear division; the divisions are mitotic (the megaspore "
        "is already haploid), and mitosis involves DNA replication.",
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "Of the eight nuclei present in a typical mature angiosperm embryo sac, how many are surrounded by cell walls "
    "and organised into cells?",
    P("Six", ["Seven", "Eight", "Three"], "D"),
    "Cellular organisation of the embryo sac",
    "NCERT: six of the eight nuclei are surrounded by cell walls and organised into cells (three in the egg "
    "apparatus and three antipodals); the remaining two nuclei, called polar nuclei, lie below the egg apparatus in "
    "the large central cell. Hence the embryo sac is 7-celled (six cells plus the central cell) but 8-nucleate.",
    ["Egg apparatus: 3 cells", "Antipodals: 3 cells", "Two polar nuclei share the central cell", "Nuclei walled "
     "individually: 6"],
    C12_SR("pistil, megasporangium and embryo sac: female gametophyte"),
    why="Seven is the number of cells (it counts the binucleate central cell); eight is the number of nuclei; three "
        "counts only one group of cells.",
    seconds=25)

add(SRFP, "Double fertilisation", "Basic", "direct",
    "In a few species, the thalamus also contributes to fruit formation, giving false fruits. Which of the following "
    "is named in NCERT as such a species?",
    P("Strawberry", ["Mango", "Orange", "Guava"], "A"),
    "False fruits",
    "NCERT: in a few species such as apple, strawberry and cashew, the thalamus also contributes to fruit formation; "
    "such fruits are called false fruits. Most fruits develop only from the ovary and are true fruits.",
    ["False fruit: thalamus also contributes", "NCERT examples: apple, strawberry, cashew"],
    C12_SR("post-fertilisation: structures and events, fruit"),
    why="Mango, orange and guava are NCERT's examples of fruits with a fleshy pericarp developed from the ovary.",
    seconds=20)

add(SRFP, "Endosperm and embryo", "Basic", "assertion_reason",
    ar("Mature seeds of crop plants can be stored for long periods and used to raise a crop in the next season.",
       "As a seed matures, it becomes dehydrated, with only about 10–15 per cent moisture by mass, and its embryo "
       "may enter a state of inactivity called dormancy."),
    AR("A"),
    "Why seeds can be stored",
    "NCERT: as the seed matures its water content is reduced (10–15 per cent moisture by mass), general metabolic "
    "activity slows down and the embryo may enter dormancy. It then states that dehydration and dormancy of mature "
    "seeds are crucial for the storage of seeds, which can be used as food throughout the year and to raise a crop "
    "in the next season. R gives exactly this cause of A.",
    ["A: true", "R: true", "Dehydration and dormancy make storage possible: R explains A"],
    C12_SR("post-fertilisation: seed"),
    seconds=30)

add(SRFP, "Double fertilisation", "Basic", "statement_pair",
    sp("After reaching the ovary, the pollen tube enters the ovule through the micropyle.",
       "The pollen tube then enters one of the antipodal cells through the filiform apparatus and releases the two "
       "male gametes into it."),
    SP("C"),
    "Entry of the pollen tube",
    "NCERT: after reaching the ovary, the pollen tube enters the ovule through the micropyle and then enters one of "
    "the synergids through the filiform apparatus, releasing the two male gametes into the cytoplasm of the "
    "synergid. The filiform apparatus is at the micropylar tip of the synergids; the antipodals lie at the chalazal "
    "end. Statement I is true; Statement II is false.",
    ["Statement I: true", "The tube enters a synergid, not an antipodal cell", "Statement II: false"],
    C12_SR("double fertilisation"),
    seconds=30)

add(SRFP, "Pollination", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Chasmogamous flowers", "Cleistogamous flowers", "Geitonogamy", "Xenogamy"],
       ["Transfer of pollen grains to the stigma of a different plant",
        "Flowers that do not open at all",
        "Flowers with exposed anthers and stigma, similar to the flowers of other species",
        "Transfer of pollen grains to the stigma of another flower of the same plant"]),
    M(mc("III,II,IV,I"), [mc("II,III,IV,I"), mc("III,II,I,IV"), mc("IV,II,III,I")], "C"),
    "Kinds of flowers and of pollination",
    "Chasmogamous flowers are similar to the flowers of other species, with exposed anthers and stigma. Cleistogamous "
    "flowers do not open at all. Geitonogamy is the transfer of pollen grains from the anther to the stigma of another "
    "flower of the same plant. Xenogamy is the transfer of pollen grains from the anther to the stigma of a "
    "different plant.",
    ["A-III", "B-II", "C-IV", "D-I"],
    C12_SR("pollination: kinds of pollination"),
    why="The other codes swap chasmogamous with cleistogamous flowers or geitonogamy with xenogamy.",
    seconds=35)

add(SRFP, "Double fertilisation", "Basic", "direct",
    "The pericarp of a fruit may be fleshy or dry. Which pair is named in NCERT as fruits with a fleshy pericarp?",
    P("Guava and mango",
      ["Groundnut and mustard", "Guava and groundnut", "Mustard and orange"], "C"),
    "Fleshy and dry pericarp",
    "NCERT: the fruit develops from the ovary and its wall forms the pericarp. The pericarp is fleshy as in guava, "
    "orange and mango, or may be dry, as in groundnut and mustard.",
    ["Fleshy pericarp: guava, orange, mango", "Dry pericarp: groundnut, mustard"],
    C12_SR("post-fertilisation: fruit"),
    why="Groundnut and mustard both have a dry pericarp; the other two pairs mix one fleshy and one dry example.",
    seconds=20)

# Mature embryo sac: 8 haploid nuclei; endosperm cell: triploid.
_n = 20 // 2
_sac, _endo = 8 * _n, 3 * _n
assert (_sac, _endo) == (80, 30)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "numerical",
    "A flowering plant has 2n = 20. Assuming normal monosporic development, what is the total number of chromosomes "
    "in all the nuclei of one mature embryo sac taken together, and the number of chromosomes in one cell of the "
    "endosperm formed after fertilisation?",
    P("80 and 30", ["160 and 30", "70 and 30", "80 and 20"], "B"),
    "Ploidy of the female gametophyte and the endosperm",
    "The functional megaspore is formed by meiosis, so it and all eight nuclei derived from it by mitosis are haploid "
    "(n = 10). Total in the embryo sac = 8 × 10 = 80. The endosperm develops from the primary endosperm nucleus, "
    "formed by the fusion of two polar nuclei with a male gamete, so it is triploid: 3 × 10 = 30.",
    ["n = 20/2 = 10", "8 haploid nuclei × 10 = 80", "Endosperm: 3n = 30"],
    C12_SR("pistil, megasporangium and embryo sac; double fertilisation"),
    shortcut="Embryo sac total = 8n; endosperm = 3n.",
    why="160 treats the embryo-sac nuclei as diploid; 70 counts 7 cells instead of 8 nuclei; 20 is the diploid "
        "number, not the triploid endosperm.",
    seconds=50, verified_by=RECOMPUTED)

add(SRFP, "Pollination", "Intermediate", "multi_statement",
    ms("Which of the following statements about pollination by water are correct?",
       ["Pollination by water is quite rare in flowering plants and is limited to about 30 genera, mostly "
        "monocotyledons.",
        "Vallisneria and Hydrilla grow in fresh water, while Zostera is a marine sea-grass.",
        "In water hyacinth and water lily, the flowers emerge above the level of water and are pollinated by insects "
        "or wind.",
        "In Zostera, the female flowers reach the water surface on long stalks.",
        "Water-pollinated flowers are usually colourful and produce nectar."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "A"),
    "Hydrophily",
    "(a), (b) and (c) are NCERT statements: water pollination is rare (about 30 genera, mostly monocots); Vallisneria "
    "and Hydrilla are freshwater, Zostera is a marine sea-grass; not all aquatic plants use water, since in water "
    "hyacinth and water lily the flowers emerge above water and are pollinated by insects or wind. (d) is false: in "
    "sea-grasses the female flowers remain submerged and the pollen is released inside the water; the female flower "
    "reaching the surface on a long stalk is Vallisneria. (e) is false: wind- and water-pollinated flowers are not "
    "very colourful and do not produce nectar.",
    ["(a), (b), (c): true", "(d): describes Vallisneria, not Zostera", "(e): such flowers lack colour and nectar"],
    C12_SR("pollination: agents of pollination"),
    why="Options with (d) or (e) include a false statement; '(b), (d) and (e)' also drops (a) and (c).",
    seconds=50)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "assertion_reason",
    ar("Unisexual flowers on a monoecious plant such as castor or maize prevent autogamy but not geitonogamy.",
       "In a monoecious plant, both male and female flowers are present on the same plant."),
    AR("A"),
    "Monoecy as an outbreeding device",
    "NCERT: production of unisexual flowers is an outbreeding device. If both male and female flowers are present on "
    "the same plant, as in castor and maize (monoecious), it prevents autogamy but not geitonogamy. Because each "
    "flower is unisexual, pollen cannot reach the stigma of its own flower (no autogamy); but because male and "
    "female flowers are on the same plant (R), pollen can reach a female flower of the same plant (geitonogamy). R "
    "explains why geitonogamy is still possible.",
    ["A: true", "R: true", "Male and female flowers on one plant allow geitonogamy: R explains A"],
    C12_SR("outbreeding devices"),
    seconds=35)

add(SRFP, "Microsporogenesis and male gametophyte", "Intermediate", "statement_pair",
    sp("In plants that shed pollen at the two-celled stage, the generative cell divides to form the two male "
       "gametes during the growth of the pollen tube.",
       "The intine of the pollen grain is made of sporopollenin."),
    SP("C"),
    "Male gametophyte and pollen wall",
    "NCERT: in plants that shed pollen in the 2-celled condition, the generative cell divides and forms the two male "
    "gametes during the growth of the pollen tube in the stigma (Statement I true). The pollen grain has a hard outer "
    "exine made of sporopollenin and a thin, continuous inner intine made of cellulose and pectin (Statement II "
    "false).",
    ["Statement I: true", "Exine: sporopollenin; intine: cellulose and pectin", "Statement II: false"],
    C12_SR("stamen, microsporangium and pollen grain"),
    seconds=30)

add(SRFP, "Double fertilisation", "Intermediate", "direct",
    "After double fertilisation in a typical embryo sac, how many of its cells degenerate, and which cells develop "
    "further?",
    P("Five (two synergids and three antipodals); the zygote and the primary endosperm cell develop further",
      ["Three (the antipodals); the zygote, the primary endosperm cell and both synergids develop further",
       "Two (the synergids); the zygote, the primary endosperm cell and the antipodals develop further",
       "Seven (all of them); new cells arise from the integuments"], "D"),
    "Fate of the cells of the embryo sac",
    "Syngamy turns the egg into the zygote (which develops into the embryo), and triple fusion turns the central cell "
    "into the primary endosperm cell (which develops into the endosperm). NCERT: the synergids and antipodals "
    "degenerate after fertilisation. A 7-celled embryo sac therefore loses 2 synergids + 3 antipodals = 5 cells.",
    ["Egg → zygote → embryo", "Central cell → primary endosperm cell → endosperm", "Degenerate: 2 synergids + 3 "
     "antipodals = 5"],
    C12_SR("double fertilisation"),
    why="Both synergids and all three antipodals degenerate, so counts of 3 or 2 are incomplete; the zygote and the "
        "primary endosperm cell do not degenerate.",
    seconds=40)

add(SRFP, "Endosperm and embryo", "Intermediate", "match_list",
    ml(("structure of the seed or fruit", "structure from which it develops or remains"),
       ["Seed coat", "Perisperm", "Pericarp", "Endosperm"],
       ["Primary endosperm cell", "Ovary wall", "Integuments", "Nucellus"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "D"),
    "Origin of seed and fruit parts",
    "NCERT: the integuments of the ovule harden as tough protective seed coats. In some seeds, such as black pepper "
    "and beet, remnants of the nucellus persist; this residual, persistent nucellus is the perisperm. The wall of the "
    "ovary develops into the wall of the fruit, the pericarp. The primary endosperm cell divides repeatedly to form "
    "the triploid endosperm tissue.",
    ["Seed coat ← integuments (III)", "Perisperm ← nucellus (IV)", "Pericarp ← ovary wall (II)", "Endosperm ← "
     "primary endosperm cell (I)"],
    C12_SR("post-fertilisation: structures and events"),
    why="The other codes swap the origins of the seed coat and perisperm, of the pericarp and endosperm, or of the "
        "seed coat and pericarp.",
    seconds=40)

add(SRFP, "Endosperm and embryo", "Intermediate", "multi_statement",
    ms("Which of the following statements about the embryo are correct?",
       ["A typical dicotyledonous embryo consists of an embryonal axis and two cotyledons.",
        "In the grass embryo, the coleorhiza encloses the plumule.",
        "The single cotyledon of the grass family is called the scutellum.",
        "The embryo develops from the primary endosperm cell.",
        "In the grass embryo, the epicotyl has a shoot apex and a few leaf primordia enclosed in a hollow foliar "
        "structure, the coleoptile."]),
    MS(["a", "c", "e"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "B"),
    "Structure of dicot and monocot embryos",
    "(a) True. (b) False: the coleorhiza is an undifferentiated sheath enclosing the radicle and root cap. (c) True: "
    "the embryo of monocots has one cotyledon, called the scutellum in the grass family. (d) False: the embryo "
    "develops from the zygote; the primary endosperm cell forms the endosperm. (e) True.",
    ["True: (a), (c), (e)", "(b): coleorhiza encloses radicle and root cap", "(d): embryo comes from the zygote"],
    C12_SR("post-fertilisation: embryo"),
    why="Options including (b) or (d) include a false statement.",
    seconds=45)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("A species of moth and the plant Yucca cannot complete their life cycles without each other.",
       "The moth deposits its eggs in the locule of the ovary, the flower in turn gets pollinated by the moth, and "
       "the moth larvae come out of the eggs as the seeds start developing."),
    AR("A"),
    "Obligate moth–Yucca relationship",
    "NCERT: in some species the floral reward is a safe place to lay eggs. A similar relationship exists between a "
    "species of moth and Yucca, where both cannot complete their life cycles without each other: the moth deposits "
    "its eggs in the locule of the ovary, the flower is pollinated by the moth, and the larvae emerge as the seeds "
    "develop. The plant depends on the moth for pollination and the moth on the developing ovary for its larvae, so "
    "R explains A.",
    ["A: true", "R: true", "Pollination by the moth and egg-laying in the ovary make each depend on the other"],
    C12_SR("pollination: agents of pollination"),
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "A breeder crosses two varieties of a plant with bisexual flowers. Which sequence of steps, as described in "
    "NCERT, must be followed for the female parent?",
    P("Emasculation of the flower bud before the anthers dehisce → bagging → dusting of pollen from the male parent "
      "when the stigma becomes receptive → rebagging",
      ["Bagging → emasculation after the anthers dehisce → dusting of pollen from the male parent → rebagging",
       "Emasculation → dusting of pollen from the male parent → bagging after the fruit sets",
       "Dusting of pollen from the male parent → emasculation → bagging → rebagging"], "B"),
    "Artificial hybridisation",
    "NCERT: if the female parent bears bisexual flowers, the anthers are removed from the flower bud before they "
    "dehisce (emasculation); the emasculated flower is covered with a bag, generally of butter paper, to prevent "
    "contamination by unwanted pollen (bagging); when the stigma attains receptivity, mature pollen collected from "
    "the male parent is dusted on it and the flower is rebagged and the fruit allowed to develop.",
    ["Emasculate before dehiscence", "Bag", "Dust selected pollen on the receptive stigma", "Rebag"],
    C12_SR("artificial hybridisation"),
    why="Emasculating after dehiscence allows self-pollen to reach the stigma; leaving the flower unbagged until fruit "
        "set allows contamination; dusting pollen before emasculation makes self-pollination possible.",
    seconds=40)

add(SRFP, "Endosperm and embryo", "Advanced", "direct",
    "A seed of black pepper has been formed after cross-pollination and normal double fertilisation. Which pair of "
    "its tissues is genetically identical to each other?",
    P("The perisperm and the seed coat",
      ["The embryo and the endosperm", "The embryo and the seed coat",
       "The endosperm and the perisperm"], "B"),
    "Maternal and filial tissues of a seed",
    "The perisperm is the persistent remnant of the nucellus, and the seed coat develops from the integuments; both "
    "are diploid tissues of the mother plant formed without fertilisation, so they are genetically identical (both "
    "carry the mother's genotype). The embryo (from the zygote: egg + one male gamete) and the endosperm (from the "
    "primary endosperm nucleus: two polar nuclei + the other male gamete) carry paternal genes and differ from each "
    "other in ploidy (2n and 3n).",
    ["Perisperm ← nucellus (maternal, 2n)", "Seed coat ← integuments (maternal, 2n)", "Embryo and endosperm include "
     "paternal genes and differ in ploidy"],
    C12_SR("post-fertilisation: seed"),
    why="Embryo (2n) and endosperm (3n) differ in ploidy; the embryo carries paternal genes while the maternal seed "
        "coat does not; the endosperm (3n, with paternal genes) differs from the maternal perisperm (2n).",
    seconds=60)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "multi_statement",
    ms("Which of the following statements are correct?",
       ["In a dioecious species such as papaya, every seed formed by sexual reproduction results from xenogamy.",
        "Geitonogamy brings genetically different types of pollen grains to the stigma.",
        "Cleistogamous flowers produce assured seed set even in the absence of pollinators.",
        "In a monoecious plant such as maize, geitonogamy can occur.",
        "Self-incompatibility prevents autogamy but still allows pollen from other flowers of the same plant to "
        "fertilise the ovules."]),
    MS(["a", "c", "d"], [["a", "b", "c", "d"], ["c", "d", "e"], ["a", "b", "e"]], "C"),
    "Consequences of the different pollination patterns",
    "(a) True: dioecy prevents both autogamy and geitonogamy, so the pollen must come from a different plant. (b) "
    "False: geitonogamy is functionally cross-pollination but genetically similar to autogamy, since the pollen comes "
    "from the same plant; only xenogamy brings genetically different pollen. (c) True. (d) True: monoecy prevents "
    "autogamy but not geitonogamy. (e) False: self-incompatibility prevents self-pollen, from the same flower or other "
    "flowers of the same plant, from fertilising the ovules.",
    ["True: (a), (c), (d)", "(b): geitonogamy pollen is from the same plant", "(e): self-incompatibility blocks "
     "pollen of the same plant too"],
    C12_SR("pollination; outbreeding devices"),
    why="Options with (b) or (e) include a false statement; '(c), (d) and (e)' also drops the true (a).",
    seconds=60)

add(SRFP, "Double fertilisation", "Advanced", "assertion_reason",
    ar("Because the egg and the two polar nuclei of an embryo sac are genetically identical, the embryo and the "
       "endosperm of a seed always have the same genotype.",
       "The two male gametes of a pollen grain are formed by the mitotic division of a single generative cell."),
    AR("D"),
    "Genotypes of embryo and endosperm",
    "R is true: the generative cell divides mitotically to give the two male gametes, so they carry the same "
    "alleles. The egg and polar nuclei are indeed identical, but A's conclusion is false: the embryo comes from one "
    "egg + one male gamete (2n), whereas the endosperm comes from two polar nuclei + one male gamete (3n). For "
    "example, in aa (female) × AA (male), the embryo is Aa but the endosperm is aaA. So A is false and R is true.",
    ["Embryo: n (egg) + n (male) = 2n", "Endosperm: 2n (polar nuclei) + n (male) = 3n", "Different dosage, so "
     "different genotype: A false", "R: true"],
    C12_SR("stamen, microsporangium and pollen grain; double fertilisation"),
    seconds=55)

add(SRFP, "Double fertilisation", "Advanced", "match_list",
    ml(("part related to a seed from the cross aa (female parent) × AA (male parent)", "its genotype"),
       ["Seed coat", "Endosperm", "Embryo", "Vegetative cell of the pollen grain that fertilised the ovule"],
       ["Aa", "A", "aa", "aaA"]),
    M(mc("III,IV,I,II"), [mc("I,IV,III,II"), mc("III,I,IV,II"), mc("II,IV,I,III")], "A"),
    "Genotypes of maternal tissue, endosperm, embryo and male gametophyte",
    "The seed coat develops from the integuments of the mother plant: aa. The pollen of the AA male parent is "
    "haploid, so its vegetative cell and both male gametes carry A. Egg (a) + male gamete (A) gives the embryo Aa. "
    "Two polar nuclei (a + a) + male gamete (A) give the endosperm aaA.",
    ["Seed coat: maternal, aa (III)", "Endosperm: a + a + A = aaA (IV)", "Embryo: a + A = Aa (I)", "Vegetative cell: "
     "haploid, A (II)"],
    C12_SR("double fertilisation; post-fertilisation: seed"),
    why="The other codes give the seed coat a paternal allele, swap the embryo and endosperm, or treat the haploid "
        "vegetative cell as triploid.",
    seconds=60)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Advanced", "direct",
    "A plant of genotype Aa reproduces in different ways. Which of the following is NOT expected to give offspring "
    "that are all genetically identical to this mother plant?",
    P("Seeds from its cleistogamous flowers, formed by self-fertilisation",
      ["Seeds formed by apomixis, as in some Asteraceae and grasses",
       "Nucellar embryos that arise from diploid nucellar cells protruding into the embryo sac",
       "An embryo that develops without fertilisation from a diploid egg cell formed without reduction division"],
      "C"),
    "Sexual versus apomictic seeds",
    "In apomixis, seeds form without fertilisation: e.g. a diploid egg formed without reduction division develops "
    "into an embryo, or nucellar cells develop into embryos. No meiosis and no fertilisation means no segregation, so "
    "all such offspring are Aa. Cleistogamous flowers are autogamous: meiosis gives A and a gametes, and "
    "self-fertilisation gives AA, Aa and aa offspring, so not all are identical to the mother.",
    ["Apomictic and nucellar embryos: no segregation, all Aa", "Cleistogamy: autogamy with meiosis and "
     "fertilisation", "Aa × Aa (self) → AA, Aa, aa"],
    C12_SR("apomixis and polyembryony; pollination: kinds of pollination"),
    why="The other three are forms of apomixis, which NCERT describes as asexual reproduction that mimics sexual "
        "reproduction; the embryo forms without meiosis and fertilisation, so there is no segregation.",
    seconds=55)

add(SRFP, "Microsporogenesis and male gametophyte", "Advanced", "multi_statement",
    ms("Which of the following are haploid?",
       ["The primary endosperm nucleus", "A microspore", "A cell of the nucellus", "The generative cell of a "
        "pollen grain", "A synergid"]),
    MS(["b", "d", "e"], [["a", "b", "d", "e"], ["b", "c", "d"], ["a", "c", "e"]], "D"),
    "Ploidy of reproductive structures",
    "(a) The primary endosperm nucleus forms by fusion of two polar nuclei with a male gamete: triploid. (b) "
    "Microspores are formed by meiosis of the pollen mother cell: haploid. (c) The nucellus is tissue of the ovule of "
    "the diploid parent: diploid. (d) The generative cell arises by mitosis of the haploid microspore: haploid. (e) "
    "The synergid is part of the female gametophyte, formed by mitosis from the haploid megaspore: haploid.",
    ["Haploid: microspore, generative cell, synergid", "Triploid: PEN", "Diploid: nucellus"],
    C12_SR("microsporogenesis; megasporogenesis; double fertilisation"),
    why="Options containing (a) (triploid) or (c) (diploid) are wrong; '(b), (c) and (d)' also omits the synergid.",
    seconds=50)

add(SRFP, "Endosperm and embryo", "Advanced", "assertion_reason",
    ar("Seeds of wheat are albuminous.",
       "The ovary of wheat contains a single ovule."),
    AR("B"),
    "Two unrelated features of wheat",
    "NCERT: albuminous seeds retain a part of the endosperm, as it is not completely used up during embryo "
    "development; wheat, maize, barley and castor are examples (A true). NCERT also gives wheat, paddy and mango as "
    "plants with a single ovule in the ovary (R true). Whether the endosperm is used up depends on embryo development, "
    "not on how many ovules the ovary holds, so R does not explain A.",
    ["A: true", "R: true", "The number of ovules has no bearing on endosperm persistence"],
    C12_SR("post-fertilisation: seed; pistil, megasporangium and embryo sac"),
    seconds=35)

# ================================================================ Principles of Inheritance and Variation (8 / 10 / 7)
C12_PI = lambda s: ref(12, PIV, s)


def cross(p1, p2):
    """Offspring genotype distribution for two genotypes written as lists of allele pairs (independent loci)."""
    out = Counter()
    g1 = list(product(*p1))
    g2 = list(product(*p2))
    for a in g1:
        for b in g2:
            out[tuple("".join(sorted(x + y)) for x, y in zip(a, b))] += F(1, len(g1) * len(g2))
    return out


assert F(1, 2) ** 3 == F(1, 8)

add(PIV, "Sex determination", "Basic", "direct",
    "In humans, every pregnancy has a 50 per cent chance of producing a male or a female child. A couple plans to "
    "have three children. What is the probability that all three will be sons?",
    P("1/8", ["1/2", "1/6", "3/8"], "D"),
    "Independent chance of a son in each pregnancy",
    "The father produces X-bearing and Y-bearing sperms in equal proportion, so each pregnancy independently has a "
    "probability of 1/2 of being a son. Three sons in a row: 1/2 × 1/2 × 1/2 = 1/8.",
    ["P(son) = 1/2 in each pregnancy", "Independent events: multiply", "(1/2)³ = 1/8"],
    C12_PI("sex determination: sex determination in humans"),
    why="1/2 is the chance for one pregnancy only; 1/6 wrongly divides by 3; 3/8 is the chance of exactly two sons "
        "(or exactly one).",
    seconds=30, verified_by=RECOMPUTED)

add(PIV, "Multiple alleles and pleiotropy", "Basic", "direct",
    "In the human ABO blood group system, how many of the six possible genotypes give blood group A?",
    P("Two", ["One", "Three", "Four"], "A"),
    "Genotypes behind the A phenotype",
    "Iᴬ is dominant over i, so both IᴬIᴬ and Iᴬi produce only sugar A and give blood group A. IᴬIᴮ gives AB, "
    "IᴮIᴮ and Iᴮi give B, and ii gives O: six genotypes, four phenotypes.",
    ["Blood group A: IᴬIᴬ and Iᴬi", "Count = 2"],
    C12_PI("deviations from Mendelism: co-dominance"),
    why="'One' forgets the heterozygote Iᴬi; three or four would include IᴬIᴮ (blood group AB) or other genotypes.",
    seconds=20)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "On the basis of his observations on monohybrid crosses, Mendel proposed two general rules, today called the "
    "first and second laws of inheritance. They are the:",
    P("Law of dominance and law of segregation",
      ["Law of segregation and law of independent assortment",
       "Law of dominance and law of independent assortment",
       "Law of linkage and law of segregation"], "C"),
    "Laws from monohybrid crosses",
    "NCERT: based on his observations on monohybrid crosses, Mendel proposed two general rules, the First Law or Law "
    "of Dominance and the Second Law or Law of Segregation. The law of independent assortment came from his "
    "dihybrid crosses.",
    ["Monohybrid crosses → dominance (first law) and segregation (second law)", "Dihybrid crosses → independent "
     "assortment"],
    C12_PI("inheritance of one gene"),
    why="Independent assortment was proposed from dihybrid crosses; 'linkage' is Morgan's term, not one of "
        "Mendel's laws.",
    seconds=25)

add(PIV, "Mendelian inheritance", "Basic", "statement_pair",
    sp("The law of segregation is based on the fact that the alleles do not show any blending and that both the "
       "characters are recovered as such in the F2 generation, though one of them is not seen at the F1 stage.",
       "The law of independent assortment states that when two pairs of traits are combined in a hybrid, the "
       "segregation of one pair of characters is independent of the other pair of characters."),
    SP("A"),
    "Mendel's second and third laws",
    "Both statements are NCERT's own descriptions: the law of segregation rests on the non-blending of alleles and "
    "the recovery of both parental characters in F2 (Statement I true), and the law of independent assortment says "
    "that in a hybrid the segregation of one pair of characters is independent of the other pair (Statement II "
    "true).",
    ["Statement I: true", "Statement II: true"],
    C12_PI("inheritance of one gene; inheritance of two genes"),
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "match_list",
    ml(("scientist", "contribution described in NCERT"),
       ["Reginald C. Punnett", "Alfred Sturtevant", "Henking", "Langdon Down"],
       ["First described a disorder caused by an additional copy of chromosome 21, in 1866",
        "Traced a specific nuclear structure through spermatogenesis in a few insects and named it the X body",
        "Used the frequency of recombination between gene pairs on the same chromosome to map their positions",
        "Developed a graphical representation to calculate the probability of all possible genotypes of offspring"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("IV,II,III,I")], "B"),
    "Contributors to genetics",
    "Punnett developed the Punnett square. Sturtevant used the frequency of recombination between gene pairs on the "
    "same chromosome as a measure of distance and mapped their positions. Henking (1891) traced a nuclear structure "
    "through spermatogenesis and named it the X body. Langdon Down first described Down's syndrome in 1866.",
    ["A-IV", "B-III", "C-II", "D-I"],
    C12_PI("inheritance of one gene; chromosomal theory; sex determination; chromosomal disorders"),
    why="The other codes swap Punnett with Sturtevant, Henking with Langdon Down, or Sturtevant with Henking.",
    seconds=40)

add(PIV, "Mendelian and chromosomal disorders", "Basic", "multi_statement",
    ms("Which of the following are Mendelian disorders, i.e. disorders determined by alteration or mutation in a "
       "single gene?",
       ["Turner's syndrome", "Cystic fibrosis", "Thalassemia", "Klinefelter's syndrome", "Colour blindness"]),
    MS(["b", "c", "e"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d"]], "D"),
    "Mendelian versus chromosomal disorders",
    "NCERT's examples of Mendelian disorders: haemophilia, cystic fibrosis, sickle-cell anaemia, colour blindness, "
    "phenylketonuria and thalassemia. Turner's syndrome (45, X0) and Klinefelter's syndrome (47, XXY) are "
    "chromosomal disorders caused by the absence or excess of a chromosome.",
    ["Single-gene (Mendelian): cystic fibrosis, thalassemia, colour blindness", "Chromosomal: Turner's, "
     "Klinefelter's"],
    C12_PI("genetic disorders: Mendelian disorders"),
    why="Options containing (a) or (d) include a chromosomal disorder.",
    seconds=30)

add(PIV, "Mendelian inheritance", "Basic", "assertion_reason",
    ar("When the tall F1 plants of Mendel's monohybrid cross between tall and dwarf pea plants were self-pollinated, "
       "some dwarf plants appeared in the F2 generation.",
       "The factor for dwarfness was present in the F1 plants, but it was not expressed because the factor for "
       "tallness is dominant."),
    AR("A"),
    "Reappearance of the recessive trait",
    "In F1 (Tt) the dwarf factor t is carried but masked by the dominant T. During gamete formation the two factors "
    "segregate, so F1 plants produce t gametes; when two t gametes meet, tt (dwarf) plants appear in F2 (about one in "
    "four). The presence of the unexpressed recessive factor in F1 (R) is why dwarf plants reappear (A).",
    ["A: true (about 1/4 of F2 are dwarf)", "R: true", "Hidden t in F1 segregates into gametes → tt in F2: R "
     "explains A"],
    C12_PI("inheritance of one gene"),
    seconds=30)

_f2 = cross([("R", "r"), ("Y", "y")], [("R", "r"), ("Y", "y")])
_tb = sum(p for g, p in _f2.items() if all(x[0] == x[1] for x in g))
assert _tb == F(1, 4)

add(PIV, "Mendelian inheritance", "Basic", "direct",
    "In Mendel's dihybrid cross RRYY × rryy, the F1 plants were self-pollinated. What fraction of the F2 plants "
    "would be true-breeding for both seed shape and seed colour?",
    P("1/4", ["1/16", "9/16", "1/2"], "B"),
    "True-breeding (doubly homozygous) F2 plants",
    "A plant breeds true for both characters only if it is homozygous at both loci: RRYY, RRyy, rrYY or rryy. Each "
    "of these occurs in 1/16 of the F2, so together they make 4/16 = 1/4. (Equivalently, P(homozygous) = 1/2 for "
    "each gene, and 1/2 × 1/2 = 1/4.)",
    ["Homozygous at both loci: RRYY, RRyy, rrYY, rryy", "4 × 1/16 = 1/4"],
    C12_PI("inheritance of two genes"),
    shortcut="P(homozygous) per gene = 1/2; two genes: (1/2)² = 1/4.",
    why="1/16 counts only RRYY; 9/16 is the fraction with both dominant traits; 1/2 is the homozygous fraction for "
        "one gene only.",
    seconds=40, verified_by=RECOMPUTED)

_tri = cross([("A", "a"), ("B", "b"), ("C", "c")], [("A", "a"), ("B", "b"), ("C", "c")])
_hom3 = sum(p for g, p in _tri.items() if all(x[0] == x[1] for x in g))
assert _hom3 == F(1, 8)

add(PIV, "Mendelian inheritance", "Intermediate", "numerical",
    "In the cross AaBbCc × AaBbCc, the three genes assort independently. What fraction of the offspring will be "
    "homozygous at all three loci (dominant or recessive)?",
    P("1/8", ["1/64", "27/64", "1/2"], "C"),
    "Product rule for independent genes",
    "For one gene, Aa × Aa gives AA (1/4), Aa (1/2) and aa (1/4), so the chance of being homozygous (AA or aa) is "
    "1/2. The three genes assort independently, so the chance of being homozygous at all three loci is "
    "1/2 × 1/2 × 1/2 = 1/8.",
    ["Per gene: P(homozygous) = 1/4 + 1/4 = 1/2", "Three independent genes: (1/2)³ = 1/8"],
    C12_PI("inheritance of two genes: law of independent assortment"),
    why="1/64 counts only one homozygous genotype (e.g. AABBCC); 27/64 is the fraction showing all three dominant "
        "traits; 1/2 is the answer for a single gene.",
    seconds=50, verified_by=RECOMPUTED)

_ab2 = Counter()
for a in ("A", "i"):
    for b in ("B", "i"):
        _ab2["".join(sorted(a + b))] += F(1, 4)
assert _ab2["AB"] * F(1, 2) == F(1, 8)

add(PIV, "Incomplete and co-dominance", "Intermediate", "numerical",
    "A man with blood group A (genotype Iᴬi) marries a woman with blood group B (genotype Iᴮi). What is the "
    "probability that their first child will be a daughter with blood group AB?",
    P("1/8", ["1/4", "1/2", "3/8"], "A"),
    "Combining an autosomal cross with the sex of the child",
    "Iᴬi × Iᴮi gives IᴬIᴮ, Iᴬi, Iᴮi and ii in equal proportion, so P(blood group AB) = 1/4. The chance that the "
    "child is a daughter is 1/2, independently. P(daughter with AB) = 1/4 × 1/2 = 1/8.",
    ["P(IᴬIᴮ) = 1/4", "P(daughter) = 1/2", "1/4 × 1/2 = 1/8"],
    C12_PI("co-dominance; sex determination in humans"),
    why="1/4 ignores the sex of the child; 1/2 is the chance of a daughter alone; 3/8 adds instead of multiplying "
        "(1/4 + 1/8).",
    seconds=45, verified_by=RECOMPUTED)

_ry = Counter()
for g, p in _f2.items():
    if g[0] != "rr" and g[1] != "yy":
        _ry[g] += p
assert len(_ry) == 4 and max(_ry, key=_ry.get) == ("Rr", "Yy") and _ry[("Rr", "Yy")] == F(4, 16)

add(PIV, "Mendelian inheritance", "Intermediate", "direct",
    "In the F2 generation of Mendel's dihybrid cross RRYY × rryy, consider only the seeds that are round and yellow. "
    "How many different genotypes are found among them, and which genotype is the most frequent?",
    P("Four; RrYy",
      ["Four; RRYY", "Nine; RrYy", "Two; RrYy"], "D"),
    "Genotypes behind one dihybrid phenotype",
    "Round yellow seeds need at least one R and one Y. In the 16-box Punnett square they are RRYY (1), RRYy (2), RrYY "
    "(2) and RrYy (4): four genotypes making up 9/16 of the F2. RrYy (4/16) is the most frequent.",
    ["Round yellow: R_ Y_", "RRYY 1, RRYy 2, RrYY 2, RrYy 4 (out of 16)", "4 genotypes; RrYy most frequent"],
    C12_PI("inheritance of two genes"),
    why="RRYY is the rarest round-yellow genotype (1/16); nine is the number of F2 genotypes in all; two ignores the "
        "RRYy and RrYY classes.",
    seconds=50, verified_by=RECOMPUTED)

add(PIV, "Incomplete and co-dominance", "Intermediate", "assertion_reason",
    ar("When a person of genotype IᴬIᴬ marries a person of genotype IᴮIᴮ, all their children have blood group AB.",
       "Iᴬ and Iᴮ are co-dominant: when both are present together, each expresses its own type of sugar."),
    AR("A"),
    "Co-dominance in the F1",
    "Every child receives Iᴬ from one parent and Iᴮ from the other, so all are IᴬIᴮ. NCERT: when Iᴬ and Iᴮ are "
    "present together they both express their own types of sugars, which is co-dominance, and red blood cells carry "
    "both A and B sugars, giving blood group AB. R is the reason why IᴬIᴮ children are AB rather than A or B.",
    ["All children IᴬIᴮ", "Both alleles expressed (co-dominance)", "R explains why they are AB"],
    C12_PI("deviations from Mendelism: co-dominance"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "statement_pair",
    sp("Individuals with Turner's syndrome have 45 chromosomes and those with Klinefelter's syndrome have 47 "
       "chromosomes, and individuals with either condition are sterile.",
       "Both Turner's syndrome and Klinefelter's syndrome arise from polyploidy."),
    SP("C"),
    "Sex-chromosome aneuploidies",
    "Turner's syndrome: absence of one X chromosome, 45 with X0; such females are sterile as the ovaries are "
    "rudimentary. Klinefelter's syndrome: an additional X chromosome, 47 with XXY; such individuals are sterile "
    "(Statement I true). Both involve the gain or loss of a single chromosome, which is aneuploidy; polyploidy is an "
    "increase in whole sets of chromosomes caused by failure of cytokinesis (Statement II false).",
    ["Turner: 45, X0, sterile; Klinefelter: 47, XXY, sterile → Statement I true", "Single-chromosome change = "
     "aneuploidy → Statement II false"],
    C12_PI("genetic disorders: chromosomal disorders"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "match_list",
    ml(("disorder", "underlying defect"),
       ["Sickle-cell anaemia", "α-thalassemia", "Phenylketonuria", "Down's syndrome"],
       ["Reduced synthesis of α-globin due to mutation or deletion of the genes HBA1 and HBA2 on chromosome 16",
        "Presence of an additional copy of chromosome 21",
        "Substitution of a single base (GAG to GUG) at the sixth codon of the β-globin gene",
        "Lack of the enzyme that converts the amino acid phenylalanine into tyrosine"]),
    M(mc("III,I,IV,II"), [mc("I,III,IV,II"), mc("III,I,II,IV"), mc("IV,I,III,II")], "B"),
    "Molecular and chromosomal basis of disorders",
    "Sickle-cell anaemia: a single base substitution GAG → GUG at the sixth codon of the β-globin gene, replacing "
    "glutamic acid by valine. α-thalassemia: controlled by two closely linked genes HBA1 and HBA2 on chromosome 16; "
    "mutation or deletion reduces α-globin synthesis. Phenylketonuria: the affected individual lacks the enzyme that "
    "converts phenylalanine into tyrosine. Down's syndrome: trisomy of chromosome 21.",
    ["A-III", "B-I", "C-IV", "D-II"],
    C12_PI("genetic disorders"),
    why="The other codes swap the two haemoglobin disorders, or PKU with Down's syndrome, or sickle-cell anaemia "
        "with PKU.",
    seconds=45)

add(PIV, "Sex determination", "Intermediate", "multi_statement",
    ms("Which of the following statements about sex determination are correct?",
       ["In grasshoppers, the males produce two kinds of sperms: with an X chromosome and without it.",
        "In birds, the sex of the offspring depends on the type of egg that is fertilised.",
        "In Drosophila, the female is heterogametic.",
        "In honey bees, the males produce sperms by mitosis.",
        "In humans, a couple who already have two sons have a lower chance than 50 per cent of having another son."]),
    MS(["a", "b", "d"], [["a", "b", "c", "d"], ["a", "d", "e"], ["b", "c", "d"]], "C"),
    "Mechanisms of sex determination",
    "(a) True: XO males produce sperms with and without X (male heterogamety). (b) True: in birds the female (ZW) "
    "produces Z and W eggs, so the egg decides the sex. (c) False: Drosophila follows the XY type; the male is "
    "heterogametic. (d) True: the haploid male bee produces sperms by mitosis. (e) False: each pregnancy has an "
    "independent 50 per cent chance of a son.",
    ["True: (a), (b), (d)", "(c): male heterogamety in Drosophila", "(e): each pregnancy is independent"],
    C12_PI("sex determination"),
    why="Options including (c) or (e) include a false statement; '(b), (c) and (d)' also omits (a).",
    seconds=50)

add(PIV, "Multiple alleles and pleiotropy", "Intermediate", "multi_statement",
    ms("Which of the following statements are correct?",
       ["In phenylketonuria, a mutation in a single gene shows several phenotypic effects.",
        "Human skin colour, controlled by three genes, is an example of pleiotropy.",
        "In most cases, a pleiotropic gene acts through its effect on metabolic pathways that contribute towards "
        "different phenotypes.",
        "In polygenic inheritance, the effect of each allele is additive.",
        "In pleiotropy, a single phenotype is controlled by several genes."]),
    MS(["a", "c", "d"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
    "Pleiotropy and polygenic inheritance contrasted",
    "Pleiotropy: a single gene exhibits multiple phenotypic expressions, usually by affecting metabolic pathways; "
    "phenylketonuria is NCERT's example ((a) and (c) true). Polygenic inheritance: several genes control one trait, "
    "e.g. human skin colour, and the phenotype reflects the additive contribution of each allele ((d) true). So (b) "
    "and (e) describe polygenic inheritance, not pleiotropy, and are false.",
    ["Pleiotropy: one gene → many effects (PKU)", "Polygenic: many genes → one trait, additive (skin colour)",
     "(b), (e): false"],
    C12_PI("deviations from Mendelism: pleiotropy; polygenic inheritance"),
    why="Options with (b) or (e) mislabel polygenic inheritance as pleiotropy.",
    seconds=45)

_tc = {"Aabb": 425, "aaBb": 425, "AaBb": 75, "aabb": 75}
_rf = F(_tc["AaBb"] + _tc["aabb"], sum(_tc.values()))
assert _rf == F(15, 100)

add(PIV, "Linkage and crossing over", "Intermediate", "direct",
    "A plant heterozygous for two genes (AaBb) is test-crossed with aabb. The 1000 progeny are: 425 Aabb, 425 aaBb, "
    "75 AaBb and 75 aabb. Which conclusion is correct?",
    P("The two genes are linked; the heterozygous parent had received Ab from one parent and aB from the other, and "
      "the recombination frequency is 15 per cent",
      ["The two genes are linked; the heterozygous parent had received AB from one parent and ab from the other, and "
       "the recombination frequency is 15 per cent",
       "The two genes are linked, and the recombination frequency is 85 per cent",
       "The two genes assort independently, since all four classes appear"], "D"),
    "Identifying parental and recombinant classes",
    "In a test cross, the most frequent classes are the parental (non-recombinant) types. Here Aabb and aaBb (850) "
    "are frequent, so the dihybrid carried the combinations Ab and aB. The rare AaBb and aabb (150) are recombinants: "
    "recombination frequency = 150/1000 = 15 per cent. Independent assortment would give the four classes in about "
    "equal numbers.",
    ["Frequent classes = parental: Ab and aB", "Recombinants: 75 + 75 = 150", "RF = 150/1000 = 15%"],
    C12_PI("linkage and recombination"),
    why="AB/ab would make AaBb and aabb the frequent classes; 85 per cent is the parental fraction, not the "
        "recombinant one; independent assortment would give a 1 : 1 : 1 : 1 ratio.",
    seconds=55, verified_by=RECOMPUTED)

assert F(1, 4) * F(1, 2) == F(1, 8)

add(PIV, "Mendelian and chromosomal disorders", "Intermediate", "direct",
    "Two unaffected parents have a daughter with sickle-cell anaemia. What is the probability that their next child "
    "will be a son affected by sickle-cell anaemia?",
    P("1/8", ["1/4", "1/2", "1/16"], "B"),
    "Autosomal recessive disorder and sex of the child",
    "Sickle-cell anaemia is an autosome-linked recessive disorder; only HbˢHbˢ individuals show the disease. An "
    "affected child of unaffected parents means both parents are carriers (HbᴬHbˢ). P(affected) = 1/4, P(son) = 1/2, "
    "so P(affected son) = 1/4 × 1/2 = 1/8.",
    ["Both parents HbᴬHbˢ", "P(HbˢHbˢ) = 1/4", "× P(son) 1/2 = 1/8"],
    C12_PI("genetic disorders: sickle-cell anaemia"),
    why="1/4 ignores the sex of the child; 1/2 treats the disorder as if half the children were affected; 1/16 "
        "multiplies 1/4 twice.",
    seconds=45, verified_by=RECOMPUTED)

_p_hson = F(1, 4)          # carrier mother x normal father: haemophilic son among all children
_p_pku = F(1, 4)           # Aa x Aa
assert _p_hson * _p_pku == F(1, 16)

add(PIV, "Sex-linked inheritance", "Advanced", "numerical",
    "A woman is a carrier of haemophilia and is also heterozygous for phenylketonuria (an autosomal recessive "
    "disorder). Her husband has normal blood clotting and is also heterozygous for phenylketonuria. The two genes "
    "are inherited independently. What is the probability that their first child will be a haemophilic son who "
    "also has phenylketonuria?",
    P("1/16", ["1/32", "1/8", "1/4"], "D"),
    "Combining a sex-linked and an autosomal trait",
    "Haemophilia: XᴴXʰ × XᴴY gives XᴴXᴴ, XᴴXʰ, XᴴY and XʰY in equal proportion, so P(haemophilic son) = 1/4. "
    "Phenylketonuria: Pp × Pp gives pp with probability 1/4. Independent genes: 1/4 × 1/4 = 1/16.",
    ["P(XʰY) among all children = 1/4", "P(pp) = 1/4", "Product = 1/16"],
    C12_PI("Mendelian disorders: haemophilia, phenylketonuria"),
    why="1/32 multiplies by an extra 1/2 for the sex, although the 1/4 already includes it; 1/8 is the probability "
        "for a son already known to be male (1/2 × 1/4); 1/4 considers only one of the two disorders.",
    seconds=70, verified_by=RECOMPUTED)

_poly = Counter()
for g, p in _tri.items():
    _poly[sum(x.count(c) for x, c in zip(g, "ABC"))] += p
assert _poly[6] + _poly[0] == F(1, 32) and len(_poly) == 7

add(PIV, "Polygenic inheritance", "Advanced", "numerical",
    "Suppose a polygenic trait is controlled by three genes A, B and C, and each dominant allele adds an equal amount "
    "to the phenotype. Two plants, AABBCC and aabbcc, are crossed and the AaBbCc F1 plants are intercrossed. What "
    "fraction of the F2 will match either of the two original parents in phenotype?",
    P("1/32", ["1/64", "1/16", "1/8"], "B"),
    "Extreme classes of a polygenic trait",
    "The phenotype depends only on the number of dominant alleles. Only AABBCC has 6 and only aabbcc has 0. For each "
    "gene P(AA) = 1/4, so P(AABBCC) = (1/4)³ = 1/64; likewise P(aabbcc) = 1/64. Either extreme: 1/64 + 1/64 = 2/64 "
    "= 1/32.",
    ["6 dominant alleles: only AABBCC, 1/64", "0 dominant alleles: only aabbcc, 1/64", "Sum = 1/32"],
    C12_PI("polygenic inheritance"),
    why="1/64 counts only one parental type; 1/16 and 1/8 come from using 1/2 or (1/2)² per gene instead of 1/4.",
    seconds=60, verified_by=RECOMPUTED)

add(PIV, "Sex-linked inheritance", "Advanced", "direct",
    "A woman of blood group A with normal colour vision has a son who is colour blind and has blood group O. Which "
    "of the following men could be the boy's biological father?",
    P("A man with normal colour vision and blood group B",
      ["A colour-blind man with blood group AB",
       "A man with normal colour vision and blood group AB",
       "Any of these three men, since the son received both traits from his mother"], "C"),
    "ABO exclusion combined with X-linked inheritance",
    "Blood group O is ii, so the son received i from each parent. The mother must be Iᴬi, and the father must carry "
    "i; a man with blood group AB (IᴬIᴮ) cannot be the father. Colour blindness in a son comes from his mother's X "
    "chromosome (she is a carrier), since he receives only the Y from his father; the father's vision therefore "
    "gives no information. A man of blood group B (genotype Iᴮi) could be the father.",
    ["Son ii: father must carry i → AB excluded", "Son's X (and colour blindness) from mother → father's vision "
     "irrelevant", "Possible father: group B (Iᴮi)"],
    C12_PI("co-dominance; sex-linked inheritance: colour blindness"),
    why="Both AB men cannot supply i; the son's blood group O needs an i from the father, so it is not true that any "
        "man could be the father.",
    seconds=60)

add(PIV, "Sex-linked inheritance", "Advanced", "assertion_reason",
    ar("A colour-blind woman married to a man with normal colour vision can have sons with normal vision.",
       "A son receives his only X chromosome from his mother."),
    AR("D"),
    "X-linked recessive inheritance through the mother",
    "A colour-blind woman has the recessive allele on both X chromosomes. Every son receives one of her X "
    "chromosomes and a Y from his father, so all her sons are colour blind, whatever the father's vision. A is "
    "false; R is true (and is exactly why A is false).",
    ["Mother XᶜXᶜ: every egg carries Xᶜ", "Son = Xᶜ (mother) + Y (father) → colour blind", "A false, R true"],
    C12_PI("sex-linked inheritance: colour blindness"),
    seconds=35)

add(PIV, "Mendelian and chromosomal disorders", "Advanced", "multi_statement",
    ms("Which of the following statements about chromosomal disorders are correct?",
       ["An individual with Turner's syndrome is a male with gynaecomastia.",
        "An individual with Klinefelter's syndrome has 44 autosomes and the sex chromosomes XXY, i.e. 47 "
        "chromosomes.",
        "Down's syndrome results from polyploidy.",
        "An individual with Turner's syndrome has 44 autosomes and one X chromosome, i.e. 45 chromosomes.",
        "An individual with Down's syndrome has an additional copy of chromosome 21, i.e. 47 chromosomes."]),
    MS(["b", "d", "e"], [["a", "b", "d", "e"], ["b", "c", "d"], ["c", "e"]], "A"),
    "Karyotypes of chromosomal disorders",
    "(a) False: Turner's syndrome individuals are sterile females with rudimentary ovaries; masculine development "
    "with gynaecomastia describes Klinefelter's syndrome. (b) True: 44 + XXY = 47. (c) False: Down's syndrome is "
    "trisomy 21, an aneuploidy, not polyploidy. (d) True: 44 + X0 = 45. (e) True: 45 autosomes + 2 sex chromosomes "
    "= 47.",
    ["Klinefelter 47, Turner 45, Down 47", "All three: aneuploidy", "(a), (c): false"],
    C12_PI("genetic disorders: chromosomal disorders; mutation"),
    why="Options with (a) or (c) include a false statement; '(c) and (e) only' also leaves out (b) and (d).",
    seconds=55)

add(PIV, "Linkage and crossing over", "Advanced", "match_list",
    ml(("result of the test cross AaBb × aabb", "interpretation"),
       ["Four classes in the ratio 1 : 1 : 1 : 1",
        "Only the two parental classes, in the ratio 1 : 1",
        "Parental classes 90 per cent, recombinant classes 10 per cent",
        "Parental classes 63 per cent, recombinant classes 37 per cent"],
       ["Genes on the same chromosome, loosely linked", "Genes assort independently",
        "Genes so tightly linked that no recombination occurs", "Genes on the same chromosome, tightly linked"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,III,I,IV"), mc("II,IV,III,I")], "C"),
    "Reading linkage from test-cross ratios",
    "Independent genes give the four test-cross classes in equal proportion. With no recombination, only the two "
    "parental combinations appear. Morgan found that tightly linked genes show very low recombination and loosely "
    "linked genes show higher recombination (e.g. 1.3 per cent between yellow body and white eye, 37.2 per cent "
    "between white eye and miniature wing in Drosophila).",
    ["1:1:1:1 → independent (II)", "Parentals only → complete linkage (III)", "10% recombinants → tight linkage "
     "(IV)", "37% recombinants → loose linkage (I)"],
    C12_PI("linkage and recombination"),
    why="The other codes confuse independent assortment with complete linkage, or tight with loose linkage.",
    seconds=55)

add(PIV, "Incomplete and co-dominance", "Advanced", "statement_pair",
    sp("A man with blood group AB cannot be the biological father of a child with blood group O.",
       "Two parents who both have blood group B can have a child with blood group A."),
    SP("C"),
    "Inheritance of ABO blood groups",
    "A child with blood group O is ii and must receive i from each parent; an AB (IᴬIᴮ) man has no i, so Statement I "
    "is true. Parents with blood group B are IᴮIᴮ or Iᴮi; neither can pass on Iᴬ, so their children can only be B "
    "or O. Statement II is false.",
    ["O child needs i from both parents → I true", "B × B parents have no Iᴬ → II false"],
    C12_PI("deviations from Mendelism: co-dominance"),
    seconds=40)

# ================================================================ Molecular Basis of Inheritance (8 / 9 / 7)
C12_MB = lambda s: ref(12, MBI, s)

add(MBI, "Genetic code and translation", "Basic", "direct",
    "According to NCERT, the genetic code is nearly universal; for example, from bacteria to humans UUU codes for "
    "phenylalanine. Exceptions to this rule have been found in:",
    P("Mitochondrial codons and some protozoans",
      ["Bacteria and bacteriophages", "Chloroplast codons of all green plants", "The nuclear genes of humans"], "D"),
    "Universality of the genetic code",
    "NCERT lists 'nearly universal' among the features of the genetic code: UUU codes for phenylalanine from "
    "bacteria to humans, and some exceptions to this rule have been found in mitochondrial codons and in some "
    "protozoans.",
    ["Code is nearly universal", "Exceptions: mitochondrial codons, some protozoans"],
    C12_MB("genetic code"),
    why="Bacteria and human nuclear genes follow the standard code (UUU for phenylalanine from bacteria to humans); "
        "NCERT does not name chloroplasts as an exception.",
    seconds=20)

add(MBI, "Genetic code and translation", "Basic", "direct",
    "In a tRNA molecule, the region that has bases complementary to the code (codon) on the mRNA is the:",
    P("Anticodon loop", ["Amino acid acceptor end", "Methyl guanosine cap", "Poly-A tail"], "B"),
    "Adapter function of tRNA",
    "NCERT: tRNA has an anticodon loop that has bases complementary to the code, and an amino acid acceptor end to "
    "which it binds amino acids. Each amino acid has a specific tRNA.",
    ["Codon recognition: anticodon loop", "Amino acid attachment: acceptor end"],
    C12_MB("tRNA – the adapter molecule"),
    why="The acceptor end carries the amino acid; the cap and poly-A tail are features of processed eukaryotic mRNA, "
        "not of tRNA.",
    seconds=20)

add(MBI, "DNA and RNA structure", "Basic", "statement_pair",
    sp("The end of a polynucleotide chain at which the sugar has a free 3'-OH group is referred to as the 3'-end of "
       "the chain.",
       "Two nucleotides in a polynucleotide chain are linked to each other through an N-glycosidic linkage."),
    SP("C"),
    "Polarity and linkages of a polynucleotide",
    "NCERT: at one end of the polymer the phosphate moiety at the 5'-end of the sugar is free (5'-end), and at the "
    "other end the sugar has a free 3'-OH group, which is the 3'-end (Statement I true). Two nucleotides are linked "
    "through a 3'-5' phosphodiester linkage; the N-glycosidic linkage joins a nitrogenous base to the pentose sugar "
    "within a nucleoside (Statement II false).",
    ["Statement I: true", "Nucleotide–nucleotide: 3'-5' phosphodiester; base–sugar: N-glycosidic", "Statement II: "
     "false"],
    C12_MB("structure of polynucleotide chain"),
    seconds=30)

add(MBI, "Transcription", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Exon", "Intron", "Cistron", "Capping"],
       ["Addition of methyl guanosine triphosphate to the 5'-end of hnRNA",
        "Coding sequence that appears in the mature, processed RNA",
        "Segment of DNA coding for a polypeptide",
        "Intervening sequence that is removed by splicing"]),
    M(mc("II,IV,III,I"), [mc("IV,II,III,I"), mc("II,IV,I,III"), mc("III,IV,II,I")], "D"),
    "Terms of eukaryotic transcription",
    "Exons are the coding or expressed sequences that appear in mature, processed RNA; introns are intervening "
    "sequences that do not appear in mature RNA and are removed by splicing. A cistron is a segment of DNA coding for "
    "a polypeptide. In capping, an unusual nucleotide, methyl guanosine triphosphate, is added to the 5'-end of hnRNA.",
    ["A-II", "B-IV", "C-III", "D-I"],
    C12_MB("transcription unit and the gene; transcription"),
    why="The other codes swap exon and intron, cistron and capping, or exon and cistron.",
    seconds=35)

add(MBI, "DNA and RNA structure", "Basic", "multi_statement",
    ms("Which of the following statements comparing RNA and DNA are correct?",
       ["DNA is chemically less stable than RNA.",
        "In RNA, uracil is found in place of thymine.",
        "RNA is known to be catalytic, and hence reactive.",
        "RNA is preferred over DNA for the storage of genetic information.",
        "The 2'-OH group present at every nucleotide in RNA makes it labile and easily degradable."]),
    MS(["b", "c", "e"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "B"),
    "Why DNA, and not RNA, is the predominant genetic material",
    "(b), (c) and (e) are NCERT statements. Because of its 2'-OH group and catalytic reactivity, RNA is less stable; "
    "DNA is chemically less reactive and structurally more stable, so (a) is false and DNA is preferred for the "
    "storage of genetic information, making (d) false. RNA is better for the transmission and expression of genetic "
    "information.",
    ["True: (b), (c), (e)", "(a): DNA is the more stable", "(d): DNA is preferred for storage"],
    C12_MB("the search for genetic material: properties of genetic material (DNA versus RNA)"),
    why="Options including (a) or (d) reverse the comparison of stability or of storage.",
    seconds=40)

add(MBI, "DNA as genetic material", "Basic", "assertion_reason",
    ar("In the Hershey–Chase experiment, bacteria infected with bacteriophages that had been grown in a medium "
       "containing radioactive phosphorus became radioactive.",
       "The phage DNA, which contains phosphorus, entered the bacteria, whereas the phage protein coat did not."),
    AR("A"),
    "Radioactive DNA enters the host",
    "Phages grown with radioactive phosphorus have radioactive DNA, because DNA contains phosphorus and protein does "
    "not. NCERT: bacteria infected with viruses that had radioactive DNA were radioactive, indicating that DNA was the "
    "material that passed from the virus to the bacteria. R gives the reason the bacteria became radioactive.",
    ["³²P labels DNA, not protein", "DNA entered the bacteria → bacteria radioactive", "R explains A"],
    C12_MB("the search for genetic material: the genetic material is DNA"),
    seconds=30)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "direct",
    "NCERT notes that the sensitivity of DNA fingerprinting has been increased by the use of the polymerase chain "
    "reaction (PCR). As a consequence:",
    P("DNA from a single cell is enough to perform DNA fingerprinting analysis",
      ["Satellite DNA probes are no longer required", "Only blood samples can now be used",
       "The DNA of monozygotic twins can now be told apart"], "D"),
    "PCR and DNA fingerprinting",
    "NCERT: the sensitivity of the technique has been increased by the use of PCR; consequently, DNA from a single "
    "cell is enough to perform DNA fingerprinting analysis.",
    ["PCR raises sensitivity", "A single cell's DNA is enough"],
    C12_MB("DNA fingerprinting"),
    why="Labelled VNTR (satellite DNA) probes are still used; DNA from any tissue (blood, hair follicle, skin, bone, "
        "saliva, sperm) can be used; identical twins still give the same pattern.",
    seconds=25)

add(MBI, "Human genome project and DNA fingerprinting", "Basic", "direct",
    "According to NCERT, which human chromosome was the last of the 24 human chromosomes (22 autosomes, X and Y) to "
    "be completely sequenced, in May 2006?",
    P("Chromosome 1", ["The Y chromosome", "Chromosome 21", "The X chromosome"], "B"),
    "Completion of the human genome sequence",
    "NCERT: the sequence of chromosome 1 was completed only in May 2006; this was the last of the 24 human "
    "chromosomes (22 autosomes and X and Y) to be sequenced. Chromosome 1 is also the chromosome with the most genes "
    "(2968).",
    ["Last chromosome sequenced: chromosome 1", "Completed in May 2006"],
    C12_MB("human genome project"),
    why="NCERT names chromosome 1, not the Y, 21 or X chromosome, as the last to be sequenced.",
    seconds=20)

# Linear dsDNA of n bp: each strand of n nucleotides has n - 1 phosphodiester linkages.
_n_bp = 100
assert 2 * (_n_bp - 1) == 198

add(MBI, "DNA and RNA structure", "Intermediate", "numerical",
    "A linear double-stranded DNA molecule has 100 base pairs. How many 3'–5' phosphodiester linkages join the "
    "nucleotides of its two strands in all?",
    P("198", ["200", "99", "400"], "D"),
    "Counting phosphodiester linkages",
    "In a polynucleotide chain, nucleotides are linked through 3'-5' phosphodiester linkages, one between each pair "
    "of neighbouring nucleotides. A linear strand of 100 nucleotides has 99 such linkages, and the two strands "
    "together have 2 × 99 = 198.",
    ["Each strand: 100 nucleotides → 99 linkages", "Two strands: 2 × 99 = 198"],
    C12_MB("structure of polynucleotide chain"),
    why="200 assumes one linkage per nucleotide (as in a closed circle); 99 counts only one strand; 400 counts two "
        "linkages per nucleotide.",
    seconds=40, verified_by=RECOMPUTED)

_coding = "ATGGCATTC"
_mrna = _coding.replace("T", "U")
_codon2 = _mrna[3:6]
_pair = {"A": "U", "U": "A", "G": "C", "C": "G"}
_anti = "".join(_pair[b] for b in reversed(_codon2))
assert _codon2 == "GCA" and _anti == "UGC"

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "The coding strand of a short stretch of a gene reads 5'-ATGGCATTC-3', and translation starts at the first "
    "codon. What is the anticodon of the tRNA that pairs with the second codon of the mRNA, written in the 5'→3' "
    "direction?",
    P("5'-UGC-3'", ["5'-CGU-3'", "5'-GCA-3'", "5'-TGC-3'"], "D"),
    "From coding strand to anticodon",
    "The mRNA has the same sequence as the coding strand, with U for T: 5'-AUG GCA UUC-3'. The second codon is "
    "5'-GCA-3'. The anticodon pairs with it in antiparallel fashion: 3'-CGU-5', which written 5'→3' is 5'-UGC-3'.",
    ["mRNA = coding strand with U: 5'-AUGGCAUUC-3'", "Codon 2: 5'-GCA-3'", "Anticodon 3'-CGU-5' = 5'-UGC-3'"],
    C12_MB("transcription; tRNA – the adapter molecule"),
    why="5'-CGU-3' writes the anticodon in the wrong direction; 5'-GCA-3' copies the codon itself; 5'-TGC-3' uses "
        "thymine, which RNA does not contain.",
    seconds=55, verified_by=RECOMPUTED)

add(MBI, "Genetic code and translation", "Intermediate", "direct",
    "In the middle of the coding region of an mRNA, a point mutation changes one codon into UAG. What is the most "
    "likely effect on the polypeptide?",
    P("Translation stops at this codon, giving a shorter polypeptide, because UAG is a stop codon at which a release "
      "factor binds",
      ["The reading frame shifts, so every amino acid after this point is changed",
       "UAG is read by its own specific tRNA, so the polypeptide is unchanged",
       "The polypeptide becomes longer, because translation continues past the normal stop codon"], "A"),
    "Stop codons and termination",
    "UAG is one of the three codons (UAA, UAG, UGA) that do not code for any amino acid and act as stop codons. At "
    "the end of translation, a release factor binds to the stop codon, terminating translation and releasing the "
    "polypeptide. A stop codon created in the middle of the message therefore ends the polypeptide early.",
    ["UAG = stop codon", "Release factor binds → translation terminates", "Polypeptide is truncated"],
    C12_MB("genetic code; translation"),
    why="A substitution does not shift the reading frame (that needs an insertion or deletion); stop codons have no "
        "tRNA; an early stop shortens rather than lengthens the polypeptide.",
    seconds=40)

add(MBI, "DNA packaging", "Intermediate", "assertion_reason",
    ar("Histones are positively charged proteins.",
       "Histones are rich in the basic amino acid residues lysine and arginine, which carry positive charges in their "
       "side chains."),
    AR("A"),
    "Charge of histones",
    "NCERT: in eukaryotes there is a set of positively charged, basic proteins called histones. A protein acquires "
    "charge depending on the abundance of amino acid residues with charged side chains; histones are rich in lysine "
    "and arginine, both of which carry positive charges in their side chains. R therefore explains A.",
    ["A: true", "R: true", "Positive side chains of lysine and arginine make histones positive"],
    C12_MB("packaging of DNA helix"),
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "statement_pair",
    sp("Griffith concluded that the R strain bacteria had somehow been transformed by the heat-killed S strain "
       "bacteria, through some 'transforming principle'.",
       "Griffith identified this transforming principle as DNA."),
    SP("C"),
    "From transformation to its biochemical basis",
    "NCERT: Griffith concluded that the R strain bacteria had somehow been transformed by the heat-killed S strain "
    "bacteria; some 'transforming principle' transferred from the heat-killed S strain enabled the R strain to make "
    "a smooth polysaccharide coat (Statement I true). However, the biochemical nature of the genetic material was not "
    "defined from his experiments; Avery, MacLeod and McCarty later worked out that it was DNA (Statement II false).",
    ["Statement I: true", "Biochemical nature identified later by Avery, MacLeod and McCarty", "Statement II: false"],
    C12_MB("the search for genetic material: transforming principle"),
    seconds=30)

add(MBI, "DNA as genetic material", "Intermediate", "match_list",
    ml(("experiment", "observation"),
       ["Meselson and Stahl: E. coli from ¹⁵N medium grown for one generation (20 minutes) in ¹⁴N medium",
        "Hershey and Chase: bacteria infected with phages grown in radioactive sulphur",
        "Avery, MacLeod and McCarty: transforming extract treated with DNase",
        "Griffith: mice injected with heat-killed S strain bacteria alone"],
       ["The mice lived", "Transformation of R strain bacteria was inhibited", "The bacterial cells were not "
        "radioactive", "The DNA had a hybrid (intermediate) density"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,III,I,II"), mc("IV,II,III,I")], "B"),
    "Classic experiments on the genetic material",
    "After one generation in ¹⁴N, all the DNA was of hybrid density (semiconservative replication). Bacteria infected "
    "with phages carrying radioactive (sulphur-labelled) protein were not radioactive, since the protein did not "
    "enter. DNase inhibited transformation, showing the transforming principle was DNA. Heat-killed S strain "
    "bacteria alone did not kill the mice.",
    ["A-IV", "B-III", "C-II", "D-I"],
    C12_MB("the search for genetic material; replication: the experimental proof"),
    why="The other codes swap the Meselson–Stahl and Hershey–Chase results, the Avery and Griffith results, or the "
        "Hershey–Chase and Avery results.",
    seconds=45)

add(MBI, "Transcription", "Intermediate", "multi_statement",
    ms("Which of the following statements about the processing of RNA in eukaryotes are correct?",
       ["The precursor of mRNA, the heterogeneous nuclear RNA (hnRNA), is transcribed by RNA polymerase II.",
        "In capping, an unusual nucleotide (methyl guanosine triphosphate) is added to the 5'-end of hnRNA.",
        "In tailing, adenylate residues are added at the 3'-end in a template-dependent manner.",
        "In splicing, the introns are removed and the exons are joined in a defined order.",
        "The fully processed hnRNA, now called mRNA, is translated inside the nucleus."]),
    MS(["a", "b", "d"], [["a", "b", "c", "d"], ["b", "d", "e"], ["a", "c", "e"]], "D"),
    "Processing of the primary transcript",
    "(a), (b) and (d) are NCERT statements. (c) is false: in tailing, adenylate residues (200–300) are added at the "
    "3'-end in a template-independent manner. (e) is false: the fully processed hnRNA, now called mRNA, is "
    "transported out of the nucleus for translation.",
    ["True: (a), (b), (d)", "(c): tailing is template-independent", "(e): mRNA is transported to the cytoplasm"],
    C12_MB("transcription: transcription in eukaryotes"),
    why="Options containing (c) or (e) include a false statement.",
    seconds=45)

# Reverse Meselson-Stahl: start light (14N/14N), grow in 15N.
_mols = [("L", "L")]
for _ in range(2):
    _mols = [m for d in _mols for m in ((d[0], "H"), (d[1], "H"))]
_kinds = Counter("".join(sorted(m)) for m in _mols)
assert _kinds == Counter({"HL": 2, "HH": 2})

add(MBI, "Replication", "Intermediate", "direct",
    "E. coli grown for many generations in a ¹⁴NH₄Cl medium is transferred to a ¹⁵NH₄Cl medium and allowed to "
    "divide twice (40 minutes; generation time 20 minutes). If replication is semiconservative, the DNA extracted "
    "after 40 minutes will be:",
    P("Half hybrid (¹⁵N/¹⁴N) and half heavy (¹⁵N/¹⁵N)",
      ["Half hybrid (¹⁵N/¹⁴N) and half light (¹⁴N/¹⁴N)", "All hybrid (¹⁵N/¹⁴N)",
       "One-fourth hybrid and three-fourths heavy"], "B"),
    "Semiconservative replication in reverse",
    "Each new DNA molecule keeps one parental strand and gets one new strand. After the first division in ¹⁵N, both "
    "molecules are ¹⁴N/¹⁵N (hybrid). In the second division, each hybrid gives one ¹⁴N/¹⁵N and one ¹⁵N/¹⁵N molecule. "
    "So after 40 minutes: 2 hybrid and 2 heavy out of 4, i.e. half and half. (This mirrors Meselson and Stahl's "
    "result of equal light and hybrid DNA after 40 minutes, with the isotopes reversed.)",
    ["Generation 1: all ¹⁴N/¹⁵N", "Generation 2: 2 hybrid + 2 heavy", "Half hybrid, half heavy"],
    C12_MB("replication: the experimental proof"),
    why="'Half hybrid and half light' is the result for the original direction (¹⁵N → ¹⁴N); 'all hybrid' is the "
        "result after one generation; three-fourths heavy would be the result after three generations.",
    seconds=55, verified_by=RECOMPUTED)

add(MBI, "DNA packaging", "Intermediate", "direct",
    "Which sequence correctly shows increasing levels of DNA packaging in a eukaryotic nucleus, as described in "
    "NCERT?",
    P("DNA wrapped around a histone octamer (nucleosome) → 'beads-on-string' chromatin → chromatin fibres → "
      "condensed chromosome at metaphase",
      ["Chromatin fibres → nucleosome → 'beads-on-string' chromatin → condensed chromosome at metaphase",
       "Nucleosome → condensed chromosome at metaphase → chromatin fibres → 'beads-on-string' chromatin",
       "'Beads-on-string' chromatin → nucleosome → chromatin fibres → condensed chromosome at metaphase"], "C"),
    "Levels of chromatin organisation",
    "NCERT: the negatively charged DNA is wrapped around the positively charged histone octamer to form a nucleosome. "
    "Nucleosomes are the repeating units of chromatin, which looks like 'beads-on-string' under the electron "
    "microscope. The beads-on-string structure is packaged into chromatin fibres, which are further coiled and "
    "condensed at metaphase to form chromosomes.",
    ["Nucleosome", "Beads-on-string", "Chromatin fibres", "Metaphase chromosome"],
    C12_MB("packaging of DNA helix"),
    why="In the other sequences a higher level of packaging is placed before the nucleosome, or the beads-on-string "
        "stage (a chain of nucleosomes) is placed before the nucleosome itself.",
    seconds=35)

add(MBI, "Lac operon", "Advanced", "direct",
    "A mutant E. coli makes a lac repressor that still binds normally to the operator but can no longer interact "
    "with the inducer. The mutant is placed in a medium containing lactose and no glucose. What happens to the lac "
    "operon?",
    P("It remains switched off, because the repressor cannot be inactivated by the inducer and stays bound to the "
      "operator",
      ["It is switched on, because lactose binds directly to the operator and displaces the repressor",
       "It is switched on, because permease brings lactose into the cell",
       "It is expressed all the time, whether or not lactose is present"], "D"),
    "Role of the repressor–inducer interaction",
    "NCERT: the repressor, synthesised all the time from the i gene, binds to the operator and prevents RNA "
    "polymerase from transcribing the operon. In the presence of an inducer such as lactose or allolactose, the "
    "repressor is inactivated by interaction with the inducer, allowing RNA polymerase access to the promoter. If the "
    "repressor cannot interact with the inducer, it is never inactivated, stays on the operator, and the z, y and a "
    "genes are not transcribed even when lactose is available.",
    ["Induction needs inducer–repressor interaction", "No interaction → repressor stays on the operator",
     "Operon stays off despite lactose"],
    C12_MB("regulation of gene expression: the lac operon"),
    why="The inducer acts on the repressor, not on the operator; lactose entry alone cannot switch the operon on if "
        "the repressor is not inactivated; constitutive expression would need a repressor that cannot bind the "
        "operator, the opposite of this mutant.",
    seconds=60)

# Spliced gene: coding exons only (no UTRs); start codon at the beginning of E1, stop codon at the end of E3.
_exons, _introns = [150, 120, 90], [180, 60]
_aa = sum(_exons) // 3 - 1
assert sum(_exons) % 3 == 0 and _aa == 119 and (sum(_exons) + sum(_introns)) // 3 - 1 == 199

add(MBI, "Transcription", "Advanced", "numerical",
    "A eukaryotic structural gene has three exons of 150, 120 and 90 nucleotides, separated by two introns of 180 and "
    "60 nucleotides. Assume the exons contain no untranslated regions: the start codon AUG begins the first exon and "
    "a stop codon ends the third exon. How many amino acids will the polypeptide translated from the mature mRNA "
    "have (before any processing)?",
    P("119", ["120", "199", "200"], "B"),
    "Splicing and codon counting",
    "Splicing removes the introns, so the mature mRNA carries only the exons: 150 + 120 + 90 = 360 nucleotides = 120 "
    "codons. The last codon is a stop codon, which does not code for any amino acid, so the polypeptide has "
    "120 − 1 = 119 amino acids.",
    ["Mature mRNA: exons only = 360 nucleotides", "360/3 = 120 codons", "Minus the stop codon: 119 amino acids"],
    C12_MB("transcription: split genes and splicing; genetic code"),
    why="120 counts the stop codon as an amino acid; 199 and 200 wrongly keep the 240 intron nucleotides in the "
        "mRNA (600 nucleotides).",
    seconds=60, verified_by=RECOMPUTED)

add(MBI, "Genetic code and translation", "Advanced", "assertion_reason",
    ar("Deletion of a single base near the beginning of the coding region of a gene changes the amino acid sequence "
       "of the polypeptide from that point onwards.",
       "The genetic code is degenerate: some amino acids are coded by more than one codon."),
    AR("B"),
    "Frameshift mutation versus degeneracy",
    "NCERT: insertion or deletion of one or two bases changes the reading frame from the point of insertion or "
    "deletion (A true). This happens because the codon is a triplet read in a contiguous fashion without "
    "punctuation. Degeneracy (R) is a true feature of the code, but it concerns how many codons specify an amino "
    "acid and has nothing to do with the shift of the reading frame.",
    ["A: true (frameshift)", "R: true", "Cause of A: triplet code read without punctuation, not degeneracy"],
    C12_MB("genetic code: mutations and genetic code"),
    seconds=40)

add(MBI, "Transcription", "Advanced", "multi_statement",
    ms("Which of the following statements comparing gene expression in bacteria and eukaryotes are correct?",
       ["In bacteria, a single DNA-dependent RNA polymerase catalyses the transcription of all types of RNA.",
        "Bacterial structural genes are mostly monocistronic.",
        "In bacteria, translation can begin much before the mRNA is fully transcribed.",
        "In eukaryotes, the primary transcript is functional without any processing.",
        "In eukaryotes, the structural genes are split, with exons interrupted by introns."]),
    MS(["a", "c", "e"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "A"),
    "Prokaryotic and eukaryotic gene expression",
    "(a) True. (b) False: the structural gene in a transcription unit is mostly monocistronic in eukaryotes and "
    "polycistronic in bacteria. (c) True: bacterial mRNA needs no processing and there is no nuclear separation, so "
    "transcription and translation can be coupled. (d) False: the eukaryotic primary transcript contains introns and "
    "is non-functional until it is processed by capping, tailing and splicing. (e) True.",
    ["True: (a), (c), (e)", "(b): bacteria are mostly polycistronic", "(d): primary transcript needs processing"],
    C12_MB("transcription unit and the gene; transcription"),
    why="Options with (b) or (d) include a false statement.",
    seconds=50)

_bp = 500
_A = 2 * _bp * 20 // 100
_G = _bp - _A
_hb = 2 * _A + 3 * _G
_turns = _bp // 10
assert (_A, _G, _hb, _turns) == (200, 300, 1300, 50)

add(MBI, "DNA and RNA structure", "Advanced", "match_list",
    ml(("quantity for a B-DNA double helix of 500 base pairs in which 20 per cent of all the bases are adenine",
        "value"),
       ["Number of adenine bases", "Number of guanine bases",
        "Number of hydrogen bonds between the two strands (A=T two, G≡C three)",
        "Number of complete turns of the helix (about 10 base pairs per turn)"],
       ["50", "300", "1300", "200"]),
    M(mc("IV,II,III,I"), [mc("II,IV,III,I"), mc("IV,II,I,III"), mc("IV,III,II,I")], "D"),
    "Chargaff's rule and the dimensions of B-DNA",
    "500 bp = 1000 bases. A = 20% of 1000 = 200, and A = T, so T = 200. G + C = 600 and G = C, so G = 300. Hydrogen "
    "bonds = 2 × 200 (A=T pairs) + 3 × 300 (G≡C pairs) = 1300. The pitch is 3.4 nm and the rise per base pair 0.34 "
    "nm, so there are about 10 bp per turn: 500/10 = 50 turns.",
    ["A = 0.2 × 1000 = 200", "G = (1000 − 400)/2 = 300", "H-bonds = 400 + 900 = 1300", "Turns = 500/10 = 50"],
    C12_MB("structure of polynucleotide chain"),
    why="The other codes swap the adenine and guanine counts, the turns and hydrogen bonds, or the guanine and "
        "hydrogen-bond values.",
    seconds=75, verified_by=RECOMPUTED)

_s1 = {"A": 1, "G": 2, "T": 3, "C": 4}
_s2 = {"A": _s1["T"], "G": _s1["C"], "T": _s1["A"], "C": _s1["G"]}
assert _s2 == {"A": 3, "G": 4, "T": 1, "C": 2} and F(_s1["A"] + _s1["G"], _s1["T"] + _s1["C"]) == F(3, 7)

add(MBI, "DNA and RNA structure", "Advanced", "statement_pair",
    sp("If one strand of a DNA double helix has its bases in the ratio A : G : T : C = 1 : 2 : 3 : 4, the "
       "complementary strand has A : G : T : C = 3 : 4 : 1 : 2.",
       "In the first strand, the ratio (A + G)/(T + C) is equal to one."),
    SP("C"),
    "Base pairing within and between strands",
    "Base pairing makes the bases of one strand complementary to those of the other: A of strand 2 = T of strand 1 "
    "(3), G of strand 2 = C of strand 1 (4), T of strand 2 = A of strand 1 (1), C of strand 2 = G of strand 1 (2). "
    "Statement I is true. Chargaff's equalities (A = T, G = C) hold for double-stranded DNA as a whole, not for a "
    "single strand: here (A + G)/(T + C) = (1 + 2)/(3 + 4) = 3/7. Statement II is false.",
    ["Strand 2: A 3, G 4, T 1, C 2 → I true", "Strand 1: (1 + 2)/(3 + 4) = 3/7 ≠ 1 → II false"],
    C12_MB("structure of polynucleotide chain: Chargaff's rules"),
    seconds=55, verified_by=RECOMPUTED)

add(MBI, "DNA as genetic material", "Advanced", "direct",
    "In Griffith's experiments with Streptococcus pneumoniae, what would be expected if mice were injected with a "
    "mixture of heat-killed R strain bacteria and live S strain bacteria?",
    P("The mice would die, because the live S strain bacteria are virulent on their own",
      ["The mice would live, because the heat-killed R strain transforms the S strain into the R form",
       "The mice would live, because heat-killed bacteria protect the mice from infection",
       "The mice would die only if the mixture were first treated with DNase"], "A"),
    "Reading Griffith's results",
    "Griffith found that mice injected with live S strain bacteria (which have a mucous polysaccharide coat) died, "
    "while those injected with live R strain lived. Transformation in his experiment converted harmless R into "
    "virulent S using the transforming principle from heat-killed S. In the mixture here, live S bacteria are "
    "already present and virulent, so the mice die whatever the heat-killed R bacteria do.",
    ["Live S strain alone kills mice", "Heat-killed R cannot remove the coat of live S", "Mice die"],
    C12_MB("the search for genetic material: transforming principle"),
    why="Griffith's transformation turned R into S, not S into R; heat-killed bacteria give no protection in his "
        "experiments; DNase destroys DNA and is irrelevant when live S bacteria are injected.",
    seconds=45)

# ================================================================ Microbes in Human Welfare (2 / 3 / 2)
C12_MW = lambda s: ref(12, MHW, s)

add(MHW, "Biocontrol agents and biofertilisers", "Basic", "direct",
    "Cyanobacteria such as Anabaena, Nostoc and Oscillatoria serve as important biofertilisers in paddy fields. "
    "Besides fixing atmospheric nitrogen, NCERT notes that they also:",
    P("Add organic matter to the soil and increase its fertility",
      ["Absorb phosphorus from the soil and pass it to the rice plants",
       "Kill the caterpillars that feed on the rice plants",
       "Release antibiotics that kill the weeds of paddy fields"], "C"),
    "Cyanobacteria as biofertilisers",
    "NCERT: cyanobacteria are autotrophic microbes widely distributed in aquatic and terrestrial environments, many "
    "of which can fix atmospheric nitrogen; in paddy fields they serve as an important biofertiliser. Blue-green "
    "algae also add organic matter to the soil and increase its fertility.",
    ["Nitrogen fixation", "Also add organic matter → greater soil fertility"],
    C12_MW("microbes as biofertilisers"),
    why="Absorbing phosphorus for the plant is the role of mycorrhizal fungi such as Glomus; killing caterpillars is "
        "the role of Bacillus thuringiensis; weed killing by antibiotics is not described in NCERT.",
    seconds=25)

add(MHW, "Household and industrial products", "Basic", "match_list",
    ml(("need", "microbial product used"),
       ["Suppressing the immune response of an organ-transplant patient",
        "Removing a clot from the blood vessels of a patient with myocardial infarction",
        "Lowering blood cholesterol",
        "Removing oily stains from laundry"],
       ["Lipases", "Statins", "Cyclosporin A", "Streptokinase"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "A"),
    "Bioactive molecules and enzymes from microbes",
    "Cyclosporin A, from the fungus Trichoderma polysporum, is used as an immunosuppressive agent in organ-transplant "
    "patients. Streptokinase, produced by Streptococcus and modified by genetic engineering, is a 'clot buster' for "
    "patients with myocardial infarction. Statins from Monascus purpureus are blood-cholesterol lowering "
    "agents. Lipases are used in detergent formulations to remove oily stains from laundry.",
    ["A-III", "B-IV", "C-II", "D-I"],
    C12_MW("microbes in industrial products: enzymes and other bioactive molecules"),
    why="The other codes swap cyclosporin A with streptokinase, lipases with statins, or cyclosporin A with statins.",
    seconds=35)

add(MHW, "Biogas", "Intermediate", "direct",
    "Which gas does NCERT list among the gases produced in the anaerobic sludge digesters of a sewage treatment "
    "plant, but not among the gases produced by methanogens growing anaerobically on cellulosic material?",
    P("Hydrogen sulphide", ["Methane", "Carbon dioxide", "Hydrogen"], "D"),
    "Comparing two NCERT lists of gases",
    "NCERT: certain bacteria that grow anaerobically on cellulosic material produce large amounts of methane along "
    "with CO₂ and H₂ (methanogens). In the anaerobic sludge digesters, bacteria produce a mixture of gases such as "
    "methane, hydrogen sulphide and carbon dioxide, which form biogas. Hydrogen sulphide appears only in the second "
    "list; hydrogen appears only in the first.",
    ["Methanogens on cellulose: CH₄, CO₂, H₂", "Sludge digester: CH₄, H₂S, CO₂", "Only in the digester list: H₂S"],
    C12_MW("microbes in sewage treatment; microbes in production of biogas"),
    why="Methane and carbon dioxide are in both lists; hydrogen is in the methanogen list only.",
    seconds=35)

add(MHW, "Household and industrial products", "Intermediate", "assertion_reason",
    ar("The large holes in 'Swiss cheese' are due to the production of a large amount of CO₂ by the bacterium "
       "Propionibacterium sharmanii.",
       "'Roquefort cheese' is ripened by growing a specific bacterium on it, which gives it a particular flavour."),
    AR("C"),
    "Microbes in cheese making",
    "NCERT: the large holes in Swiss cheese are due to the production of a large amount of CO₂ by a bacterium named "
    "Propionibacterium sharmanii (A true). 'Roquefort cheese' is ripened by growing a specific fungus on it, not a "
    "bacterium, which gives it a particular flavour (R false).",
    ["A: true", "Roquefort cheese: ripened by a fungus", "R: false"],
    C12_MW("microbes in household products"),
    seconds=30)

add(MHW, "Sewage treatment", "Intermediate", "multi_statement",
    ms("Which of the following statements about municipal sewage treatment are correct?",
       ["In primary treatment, floating debris is removed by sequential filtration, and grit is removed by "
        "sedimentation.",
        "The primary sludge, rather than the primary effluent, is taken for secondary treatment in the aeration "
        "tanks.",
        "In the aeration tanks, the vigorous growth of aerobic microbes into flocs reduces the BOD of the effluent.",
        "A small part of the activated sludge is pumped back into the aeration tank to serve as the inoculum.",
        "The flocs in the aeration tank consist of anaerobic methanogens."]),
    MS(["a", "c", "d"], [["a", "b", "c", "d"], ["c", "d", "e"], ["a", "b", "e"]], "B"),
    "Stages of sewage treatment",
    "(a) True. (b) False: all the solids that settle form the primary sludge, and the supernatant forms the primary "
    "effluent, which is taken for secondary treatment. (c) True: aerobic microbes grow into flocs (masses of "
    "bacteria associated with fungal filaments) and consume the organic matter, reducing BOD. (d) True; the major part "
    "of the sludge goes to anaerobic sludge digesters. (e) False: flocs form from aerobic microbes in the aerated "
    "tank.",
    ["True: (a), (c), (d)", "(b): primary effluent goes to aeration", "(e): flocs are aerobic"],
    C12_MW("microbes in sewage treatment"),
    why="Options with (b) or (e) include a false statement.",
    seconds=50)

add(MHW, "Household and industrial products", "Advanced", "statement_pair",
    sp("Alexander Fleming, while working on Staphylococci bacteria, observed a mould growing in one of his unwashed "
       "culture plates, around which the Staphylococci could not grow.",
       "The fungus Trichoderma polysporum is the source of cyclosporin A, and Trichoderma species are also used as "
       "biological control agents against several plant pathogens."),
    SP("A"),
    "Fungi as sources of drugs and as biocontrol agents",
    "NCERT: Fleming, while working on Staphylococci, once observed a mould growing in one of his unwashed culture "
    "plates around which Staphylococci could not grow; the chemical was penicillin, from Penicillium notatum "
    "(Statement I true). Cyclosporin A, an immunosuppressive agent, is produced by the fungus Trichoderma polysporum, "
    "and Trichoderma species, free-living fungi common in root ecosystems, are effective biocontrol agents of several "
    "plant pathogens (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_MW("antibiotics; bioactive molecules; microbes as biocontrol agents"),
    seconds=40)

add(MHW, "Biogas", "Advanced", "multi_statement",
    ms("Which of the following statements about methanogens are correct?",
       ["They grow anaerobically on cellulosic material.",
        "They are commonly found in the anaerobic sludge during sewage treatment.",
        "They are present in the rumen of cattle, where they help in the breakdown of cellulose.",
        "The excreta (dung) of cattle, commonly called gobar, is rich in these bacteria.",
        "The gas they produce is mainly hydrogen."]),
    MS(["a", "b", "c", "d"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "D"),
    "Methanogens in nature and in biogas plants",
    "NCERT: bacteria that grow anaerobically on cellulosic material produce large amounts of methane along with CO₂ "
    "and H₂; they are collectively called methanogens, e.g. Methanobacterium. They are commonly found in the "
    "anaerobic sludge during sewage treatment and in the rumen of cattle, where they help break down cellulose; cattle "
    "dung (gobar) is rich in them and is used to make biogas. The gas they produce is mainly methane, so (e) is "
    "false.",
    ["True: (a)–(d)", "(e): mainly methane, not hydrogen"],
    C12_MW("microbes in production of biogas"),
    why="Options with (e) include a false statement; '(a), (c) and (d) only' leaves out the true (b).",
    seconds=45)

# ================================================================ Organisms and Populations (4 / 5 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population interactions", "Basic", "direct",
    "NCERT notes that totally unrelated species can also compete for the same resource. In some shallow South "
    "American lakes, visiting flamingoes and resident fishes compete for their common food, which is the:",
    P("Zooplankton in the lake", ["Phytoplankton in the lake", "Aquatic insect larvae", "Snails on the lake bed"],
      "B"),
    "Competition between unrelated species",
    "NCERT: competition is thought to occur when closely related species compete for the same resources that are "
    "limiting, but totally unrelated species could also compete; in some shallow South American lakes, visiting "
    "flamingoes and resident fishes compete for their common food, the zooplankton in the lake.",
    ["Unrelated species can compete", "Flamingoes and fishes: common food = zooplankton"],
    C12_OP("population interactions: competition"),
    why="NCERT names zooplankton as the shared food; phytoplankton, insect larvae and snails are not mentioned.",
    seconds=20)

_tbl = {"mutualism": ("+", "+"), "competition": ("-", "-"), "predation": ("+", "-"), "parasitism": ("+", "-"),
        "commensalism": ("+", "0"), "amensalism": ("-", "0")}
assert sum("+" in v for v in _tbl.values()) == 4

add(OAP, "Population interactions", "Basic", "direct",
    "Consider the six population interactions described in NCERT: mutualism, competition, predation, parasitism, "
    "commensalism and amensalism. In how many of them does at least one of the two interacting species benefit?",
    P("Four", ["Two", "Three", "Five"], "D"),
    "Signs of population interactions",
    "Mutualism (+, +), predation (+, −), parasitism (+, −) and commensalism (+, 0) each have at least one species "
    "that benefits. In competition (−, −) both lose, and in amensalism (−, 0) one is harmed and the other unaffected, "
    "so neither of these benefits any species. Count = 4.",
    ["Benefit present: mutualism, predation, parasitism, commensalism", "No benefit: competition, amensalism",
     "4"],
    C12_OP("population interactions"),
    why="Two counts only the interactions in which one benefits and one is harmed; three leaves out mutualism or "
        "commensalism; five wrongly includes amensalism or competition.",
    seconds=30, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Basic", "match_list",
    ml(("example", "interaction"),
       ["A sparrow eating seeds", "A koel (cuckoo) laying its eggs in a crow's nest",
        "The fig and its pollinating wasp", "Introduced goats and the Abingdon tortoise of the Galapagos"],
       ["Competition", "Mutualism", "Predation", "Brood parasitism"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "C"),
    "Identifying interactions from NCERT examples",
    "NCERT: a sparrow eating any seed is no less a predator than a tiger eating a deer. The cuckoo (koel) lays its "
    "eggs in the nest of its host, the crow, which incubates them (brood parasitism). The fig and its wasp are "
    "mutualists: the wasp pollinates the fig and uses its fruit for egg-laying. The Abingdon tortoise became "
    "extinct within a decade of goats being introduced, apparently because the goats were better browsers "
    "(competition).",
    ["A-III", "B-IV", "C-II", "D-I"],
    C12_OP("population interactions"),
    why="The other codes swap predation with brood parasitism, mutualism with competition, or predation with "
        "mutualism.",
    seconds=40)

add(OAP, "Population growth", "Basic", "statement_pair",
    sp("In logistic growth, the population density eventually reaches an asymptote when it reaches the carrying "
       "capacity (K) of the habitat.",
       "In nature, a given habitat has enough resources to support an unlimited number of individuals."),
    SP("C"),
    "Carrying capacity",
    "NCERT: in nature, a given habitat has enough resources to support a maximum possible number, beyond which no "
    "further growth is possible; this limit is the carrying capacity (K). A population growing in a habitat with "
    "limited resources shows lag, acceleration and deceleration phases and finally an asymptote at K (Statement I "
    "true). Resources are not unlimited (Statement II false).",
    ["Statement I: true", "Statement II: false (resources are limited; K exists)"],
    C12_OP("population: population growth models"),
    seconds=25)

_pre, _rep, _post = 600, 300, 100
assert F(_pre, _pre + _rep + _post) == F(60, 100)

add(OAP, "Population attributes", "Intermediate", "numerical",
    "In a population of 1000 individuals, 600 are pre-reproductive, 300 are reproductive and 100 are "
    "post-reproductive. What percentage of the population is pre-reproductive, and what does the age pyramid of this "
    "population indicate?",
    P("60 per cent; an expanding (growing) population",
      ["60 per cent; a stable population", "30 per cent; a declining population",
       "40 per cent; an expanding (growing) population"], "A"),
    "Age distribution and the age pyramid",
    "Pre-reproductive share = 600/1000 = 60 per cent. Plotting the per cent of individuals in each age group gives an "
    "age pyramid; here the pre-reproductive base is the broadest and each older group is narrower, giving a "
    "triangular pyramid, which NCERT associates with an expanding (growing) population. A bell shape indicates a "
    "stable population and an urn shape a declining one.",
    ["600/1000 = 60%", "Broad base, narrow top → triangular", "Triangular pyramid = expanding population"],
    C12_OP("population attributes: age pyramids"),
    why="The broad base is not the bell shape of a stable population; 30 per cent is the reproductive share; 40 per "
        "cent is the share that is not pre-reproductive.",
    seconds=40, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Intermediate", "direct",
    "On the rocky sea coasts of Scotland, the larger and competitively superior barnacle Balanus dominates the "
    "intertidal area and excludes the smaller barnacle Chthamalus from that zone. If Balanus were experimentally "
    "removed from the area, what would be expected?",
    P("Chthamalus would expand its distribution into that zone, an example of competitive release",
      ["Chthamalus would decline, because it depends on Balanus for food",
       "Both barnacles would decline, because the interaction is mutualism",
       "There would be no change, because barnacles do not compete for space"], "B"),
    "Competitive release",
    "NCERT cites Connell's field experiments: on the rocky sea coasts of Scotland, the larger and competitively "
    "superior barnacle Balanus dominates the intertidal area and excludes the smaller barnacle Chthamalus from that "
    "zone. It also explains competitive release: a species whose distribution is restricted to a small area because "
    "of a competitively superior species expands its range dramatically when the competing species is removed.",
    ["Balanus excludes Chthamalus (competition)", "Remove the superior competitor", "Chthamalus expands: "
     "competitive release"],
    C12_OP("population interactions: competition"),
    why="The barnacles compete; Chthamalus does not depend on Balanus, the interaction is not mutualism, and "
        "competition for space is exactly what restricts Chthamalus.",
    seconds=40)

add(OAP, "Population interactions", "Intermediate", "assertion_reason",
    ar("Predators help in maintaining species diversity in a community.",
       "Predators reduce the intensity of competition among competing prey species."),
    AR("A"),
    "Predators and species diversity",
    "NCERT: predators also help in maintaining species diversity in a community, by reducing the intensity of "
    "competition among competing prey species. Without them, a competitively superior prey species could eliminate "
    "others (as in the Pisaster removal experiment). R is the mechanism behind A.",
    ["A: true", "R: true", "Less competition among prey → more prey species coexist: R explains A"],
    C12_OP("population interactions: predation"),
    seconds=30)

add(OAP, "Population attributes", "Intermediate", "multi_statement",
    ms("Which of the following statements about measuring population size are correct according to NCERT?",
       ["Total number of individuals is always the most appropriate measure of population density.",
        "Where a single huge banyan tree grows among 200 Parthenium plants, percent cover or biomass is a more "
        "meaningful measure of population size than numbers.",
        "Absolute population densities are always required for every ecological investigation.",
        "To know whether the fish population of a lake has changed, the number of fish caught per trap is good "
        "enough.",
        "The tiger census in national parks and tiger reserves is often based on pug marks and fecal pellets."]),
    MS(["b", "d", "e"], [["a", "b", "d", "e"], ["b", "c", "d"], ["a", "c", "e"]], "D"),
    "Absolute and relative measures of population density",
    "(a) False: total number is generally, not always, the most appropriate measure; it is sometimes meaningless or "
    "difficult to determine. (b) True. (c) False: for certain investigations absolute numbers are not needed and "
    "relative densities serve the purpose. (d) True. (e) True: population density can be estimated indirectly.",
    ["True: (b), (d), (e)", "(a), (c): 'always' makes them false"],
    C12_OP("population attributes"),
    why="Options with (a) or (c) include a false statement; '(b), (c) and (d)' also leaves out (e).",
    seconds=45)

add(OAP, "Population growth", "Intermediate", "match_list",
    ml(("process affecting population density", "meaning"),
       ["Natality", "Mortality", "Immigration", "Emigration"],
       ["Number of individuals of the population who left the habitat and went elsewhere during a given period",
        "Number of births during a given period that are added to the initial density",
        "Number of individuals of the same species that have come into the habitat from elsewhere during a given "
        "period",
        "Number of deaths in the population during a given period"]),
    M(mc("II,IV,III,I"), [mc("IV,II,III,I"), mc("II,IV,I,III"), mc("III,IV,II,I")], "B"),
    "Four basic processes that change population density",
    "NCERT: natality is the number of births during a given period added to the initial density; mortality is the "
    "number of deaths during a given period; immigration is the number of individuals of the same species that have "
    "come into the habitat from elsewhere; emigration is the number of individuals of the population who left the "
    "habitat and gone elsewhere. Natality and immigration increase density; mortality and emigration decrease it.",
    ["A-II", "B-IV", "C-III", "D-I"],
    C12_OP("population: population growth"),
    why="The other codes swap births with deaths, arrivals with departures, or births with arrivals.",
    seconds=35)

_r = {"flour beetle": 0.12, "Norway rat": 0.015, "human population of India (1981)": 0.0205}
_td = {k: 0.693 / v for k, v in _r.items()}
assert min(_td, key=_td.get) == "flour beetle" and max(_td, key=_td.get) == "Norway rat"

add(OAP, "Population growth", "Advanced", "direct",
    "NCERT gives the intrinsic rate of natural increase (r) as 0.12 for the flour beetle, 0.015 for the Norway rat "
    "and 0.0205 for the human population of India in 1981. If each population grew exponentially at its r (taking the "
    "same unit of time for all, and ln 2 = 0.693), which would double in the shortest time and which in the longest?",
    P("Shortest: flour beetle; longest: Norway rat",
      ["Shortest: Norway rat; longest: flour beetle",
       "Shortest: flour beetle; longest: human population of India",
       "Shortest: human population of India; longest: Norway rat"], "C"),
    "Doubling time from r",
    "For exponential growth, Nₜ = N₀e^(rt); the population doubles when e^(rt) = 2, i.e. t = ln 2/r = 0.693/r. "
    "Flour beetle: 0.693/0.12 ≈ 5.8; human (India): 0.693/0.0205 ≈ 33.8; Norway rat: 0.693/0.015 ≈ 46.2 time units. "
    "The larger the r, the shorter the doubling time.",
    ["Doubling time = 0.693/r", "Beetle ≈ 5.8, India ≈ 33.8, rat ≈ 46.2", "Shortest: beetle; longest: rat"],
    C12_OP("population growth: exponential growth"),
    shortcut="Doubling time is inversely proportional to r: largest r doubles fastest, smallest r slowest.",
    why="The first option reverses the relation between r and doubling time; the human population (r = 0.0205) "
        "doubles faster than the Norway rat (r = 0.015), so it is neither the slowest nor the fastest.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "assertion_reason",
    ar("The Abingdon tortoise in the Galapagos Islands became extinct within a decade after goats were introduced on "
       "the island.",
       "The introduced goats had a greater browsing efficiency than the tortoise."),
    AR("A"),
    "Competition leading to extinction",
    "NCERT gives this as an example of competition: the Abingdon tortoise became extinct within a decade after goats "
    "were introduced on the island, apparently due to the greater browsing efficiency of the goats. The goats' "
    "superior efficiency in using the shared food (R) is the stated reason for the tortoise's extinction (A).",
    ["A: true", "R: true", "Superior competitor for the same food eliminated the tortoise: R explains A"],
    C12_OP("population interactions: competition"),
    seconds=35)

add(OAP, "Population interactions", "Advanced", "statement_pair",
    sp("In interference competition, the feeding efficiency of one species may be reduced by the interfering and "
       "inhibitory presence of the other species, even if resources (food and space) are abundant.",
       "According to Gause's competitive exclusion principle, two closely related species competing for the same "
       "resources can co-exist indefinitely if they are equally abundant."),
    SP("C"),
    "Interference competition and competitive exclusion",
    "NCERT: in interspecific competition the feeding efficiency of one species might be reduced due to the "
    "interfering and inhibitory presence of the other species, even if resources are abundant (Statement I true). "
    "Gause's principle states that two closely related species competing for the same resources cannot co-exist "
    "indefinitely, and the competitively inferior one will be eliminated eventually (Statement II false).",
    ["Statement I: true", "Gause: they cannot co-exist indefinitely", "Statement II: false"],
    C12_OP("population interactions: competition"),
    seconds=35)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    ms("Which of the following statements about parasitism are correct?",
       ["The life cycles of endoparasites are simpler than those of ectoparasites.",
        "Parasites might render the host more vulnerable to predation by making it physically weak.",
        "The eggs of a brood-parasitic bird have evolved to resemble the host's eggs in size and colour.",
        "Parasites always kill their hosts quickly.",
        "Many parasites have evolved to be host-specific, so that the host and the parasite tend to co-evolve."]),
    MS(["b", "c", "e"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "A"),
    "Effects and adaptations of parasites",
    "(a) False: the life cycles of endoparasites are more complex because of their extreme specialisation. (b) True. "
    "(c) True: this reduces the chances of the host bird detecting and ejecting the foreign eggs. (d) False: "
    "parasites may reduce the survival, growth and reproduction of the host and reduce its population density; NCERT "
    "does not say they always kill quickly. (e) True.",
    ["True: (b), (c), (e)", "(a): endoparasite life cycles are more complex", "(d): parasites harm, not "
     "necessarily kill quickly"],
    C12_OP("population interactions: parasitism"),
    why="Options with (a) or (d) include a false statement; '(b), (c) and (d)' also leaves out (e).",
    seconds=50)

# ================================================================ Ecosystem (3 / 4 / 3)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Productivity and decomposition", "Basic", "direct",
    "Which of the following is NOT one of the processes of decomposition described in NCERT?",
    P("Stratification",
      ["Fragmentation", "Leaching", "Mineralisation"], "A"),
    "Steps of decomposition",
    "NCERT: the important steps in the process of decomposition are fragmentation (detritivores break detritus into "
    "smaller particles), leaching (water-soluble inorganic nutrients go down into the soil horizon and get "
    "precipitated as unavailable salts) and catabolism (bacterial and fungal enzymes degrade detritus into simpler "
    "inorganic substances); humification and mineralisation (release of inorganic nutrients from humus) follow. "
    "Stratification is a structural feature of an ecosystem: the vertical distribution of different species "
    "occupying different levels, as in a forest.",
    ["Decomposition: fragmentation, leaching, catabolism, humification, mineralisation", "Stratification: vertical "
     "layering of species, a feature of ecosystem structure"],
    C12_EC("decomposition; ecosystem: structure and function"),
    why="Fragmentation, leaching and mineralisation are all processes of decomposition named in NCERT.",
    seconds=20)

add(ECO, "Productivity and decomposition", "Basic", "statement_pair",
    sp("Decomposers are heterotrophic organisms, mainly fungi and bacteria, which meet their energy and nutrient "
       "requirements by degrading dead organic matter.",
       "Detritivores such as earthworms carry out catabolism by secreting enzymes that degrade detritus into simpler "
       "inorganic substances."),
    SP("C"),
    "Roles in decomposition",
    "NCERT: decomposers are heterotrophic organisms, mainly fungi and bacteria, that meet their energy and nutrient "
    "requirements by degrading dead organic matter (Statement I true). Detritivores such as earthworms carry out "
    "fragmentation, breaking detritus into smaller particles; catabolism is carried out by bacterial and fungal "
    "enzymes (Statement II false).",
    ["Statement I: true", "Earthworm: fragmentation; bacteria and fungi: catabolism", "Statement II: false"],
    C12_EC("ecosystem: structure and function; decomposition"),
    seconds=30)

add(ECO, "Productivity and decomposition", "Basic", "assertion_reason",
    ar("Primary productivity is not the same in all types of ecosystems.",
       "Primary productivity depends on the plant species inhabiting a particular area, on a variety of environmental "
       "factors, on the availability of nutrients and on the photosynthetic capacity of plants."),
    AR("A"),
    "Why primary productivity varies",
    "NCERT: primary productivity depends on the plant species inhabiting a particular area; it also depends on a "
    "variety of environmental factors, availability of nutrients and the photosynthetic capacity of plants. "
    "Therefore, it varies in different types of ecosystems. R states the factors that cause the variation in A.",
    ["A: true", "R: true", "Different species and conditions → different productivity: R explains A"],
    C12_EC("productivity"),
    seconds=30)

add(ECO, "Energy flow", "Intermediate", "match_list",
    ml(("quantity", "value given in NCERT"),
       ["Photosynthetically active radiation (PAR) as a share of the incident solar radiation",
        "Share of the PAR captured by plants",
        "Energy transferred from one trophic level to the next",
        "Annual net primary productivity of the oceans"],
       ["55 billion tons", "Less than 50 per cent", "2–10 per cent", "About 10 per cent"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,IV,III,I"), mc("II,III,I,IV")], "D"),
    "Key numbers of energy flow and productivity",
    "NCERT: of the incident solar radiation, less than 50 per cent is PAR; plants capture only 2–10 per cent of the "
    "PAR; only about 10 per cent of the energy is transferred to each trophic level from the lower trophic level (10 "
    "per cent law); of the biosphere's annual NPP of about 170 billion tons (dry weight), the oceans contribute only "
    "55 billion tons.",
    ["A-II", "B-III", "C-IV", "D-I"],
    C12_EC("productivity; energy flow"),
    why="The other codes swap PAR with its captured fraction, the captured fraction with the 10 per cent law, or the "
        "10 per cent law with the ocean NPP.",
    seconds=40)

add(ECO, "Energy flow", "Intermediate", "multi_statement",
    ms("Consider the food chain: phytoplankton → zooplankton → small fish → large fish → fish-eating bird. Taking "
       "producers as the first trophic level, which of the following statements are correct?",
       ["Zooplankton are primary consumers.",
        "The small fish is a herbivore.",
        "The large fish is a secondary carnivore (tertiary consumer).",
        "The fish-eating bird occupies the fifth trophic level.",
        "Phytoplankton occupy the second trophic level."]),
    MS(["a", "c", "d"], [["a", "b", "c", "d"], ["c", "d", "e"], ["a", "d"]], "B"),
    "Trophic levels in an aquatic grazing food chain",
    "Phytoplankton are the producers (first level). Zooplankton eat them: herbivores, primary consumers (second). "
    "The small fish eats zooplankton: primary carnivore, secondary consumer (third). The large fish: secondary "
    "carnivore, tertiary consumer (fourth). The fish-eating bird: fifth level. So (b) and (e) are false.",
    ["1 phytoplankton, 2 zooplankton, 3 small fish, 4 large fish, 5 bird", "True: (a), (c), (d)"],
    C12_EC("energy flow: food chains and trophic levels"),
    why="Options with (b) or (e) misplace the small fish or the producers; '(a) and (d) only' leaves out the true "
        "(c).",
    seconds=45)

add(ECO, "Ecological pyramids", "Intermediate", "statement_pair",
    sp("A given species may occupy more than one trophic level in the same ecosystem at the same time.",
       "Ecological pyramids deal with this by placing such a species at every trophic level it occupies."),
    SP("C"),
    "A limitation of ecological pyramids",
    "NCERT: a given species may occupy more than one trophic level in the same ecosystem at the same time; for "
    "example, a sparrow is a primary consumer when it eats seeds and a secondary consumer when it eats worms "
    "(Statement I true). Among the limitations of ecological pyramids, NCERT notes that a pyramid does not take into "
    "account the same species belonging to two or more trophic levels (Statement II false).",
    ["Statement I: true", "Pyramids do not account for such species", "Statement II: false"],
    C12_EC("energy flow; ecological pyramids"),
    seconds=30)

_energy_snake, _levels_up = 30, 3
assert _energy_snake * 10 ** _levels_up == 30_000

add(ECO, "Energy flow", "Intermediate", "direct",
    "In the grazing food chain grass → grasshopper → frog → snake, the snakes receive 30 kJ of energy. Assuming that "
    "only 10 per cent of the energy is transferred from each trophic level to the next, how much energy did the grass "
    "fix?",
    P("30,000 kJ", ["3,000 kJ", "3,00,000 kJ", "300 kJ"], "B"),
    "Working back with the 10 per cent law",
    "The snake is at the fourth trophic level, three transfers above the grass. Going down one level multiplies the "
    "energy by 10: frog 300 kJ, grasshopper 3,000 kJ, grass 30,000 kJ (30 × 10³).",
    ["Snake (4th level) = 30 kJ", "Frog = 300 kJ, grasshopper = 3,000 kJ", "Grass = 30,000 kJ"],
    C12_EC("energy flow: 10 per cent law"),
    shortcut="Energy at producers = energy at level n × 10^(n − 1).",
    why="3,000 kJ stops at the grasshopper (one transfer too few); 3,00,000 kJ adds an extra transfer; 300 kJ is the "
        "frog's share.",
    seconds=45, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Advanced", "multi_statement",
    ms("Which of the following statements about decomposition are correct?",
       ["In cold, waterlogged soil with anaerobic conditions, organic matter tends to build up.",
        "In leaching, water-soluble inorganic nutrients go down into the soil horizon and are thereby always made "
        "available to plant roots.",
        "Detritus rich in chitin decomposes slowly.",
        "Humus is degraded rapidly by soil microbes.",
        "Warm, moist conditions and nitrogen-rich detritus favour quick decomposition."]),
    MS(["a", "c", "e"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "C"),
    "Factors and steps of decomposition",
    "(a) True: low temperature and anaerobiosis inhibit decomposition, resulting in the build-up of organic matter. "
    "(b) False: leached nutrients get precipitated as unavailable salts. (c) True: decomposition is slower if "
    "detritus is rich in lignin and chitin. (d) False: humus is highly resistant to microbial action and decomposes "
    "at an extremely slow rate. (e) True: decomposition is quicker if detritus is rich in nitrogen and water-soluble "
    "substances like sugars, and a warm, moist environment favours it.",
    ["True: (a), (c), (e)", "(b): leached nutrients become unavailable salts", "(d): humus decomposes extremely "
     "slowly"],
    C12_EC("decomposition"),
    why="Options with (b) or (d) include a false statement.",
    seconds=55)

add(ECO, "Energy flow", "Advanced", "assertion_reason",
    ar("In an aquatic ecosystem, the grazing food chain is the major conduit for energy flow.",
       "Decomposition is quicker if the detritus is rich in nitrogen and water-soluble substances like sugars."),
    AR("B"),
    "Two independent ecosystem facts",
    "NCERT: in an aquatic ecosystem, the grazing food chain is the major conduit for energy flow, whereas in a "
    "terrestrial ecosystem a much larger fraction of energy flows through the detritus food chain (A true). NCERT "
    "also states that decomposition is quicker if detritus is rich in nitrogen and water-soluble substances like "
    "sugars (R true). The chemical composition of detritus has nothing to do with which food chain dominates energy "
    "flow in water, so R does not explain A.",
    ["A: true", "R: true", "R concerns decomposition rate, not the main energy pathway"],
    C12_EC("energy flow; decomposition"),
    seconds=35)

_frac = F(1, 10) ** 4
assert _frac == F(1, 10_000)          # 0.01 per cent

add(ECO, "Energy flow", "Advanced", "statement_pair",
    sp("If only 10 per cent of the energy passes from each trophic level to the next, a top carnivore at the fifth "
       "trophic level receives about 0.01 per cent of the energy fixed by the producers.",
       "The number of trophic levels in a grazing food chain is restricted, as the transfer of energy follows the "
       "10 per cent law."),
    SP("A"),
    "Consequence of the 10 per cent law",
    "From producers (level 1) to level 5 there are four transfers: (1/10)⁴ = 1/10,000 = 0.01 per cent (Statement I "
    "true). NCERT: the number of trophic levels in the grazing food chain is restricted, as the transfer of energy "
    "follows the 10 per cent law; only 10 per cent of the energy is transferred to each trophic level from the lower "
    "one (Statement II true).",
    ["Four transfers: 0.1⁴ = 0.0001 = 0.01% → I true", "Statement II: true (NCERT)"],
    C12_EC("energy flow"),
    seconds=50, verified_by=RECOMPUTED)

# ================================================================ Biodiversity and Conservation (3 / 4 / 3)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "In describing the latitudinal gradient in diversity, NCERT states that the tropics harbour more species than "
    "temperate or polar areas. The tropics are taken as the latitudinal range:",
    P("23.5° N to 23.5° S", ["0° to 23.5° N only", "66.5° N to 66.5° S", "23.5° N to 66.5° N"], "C"),
    "Latitudinal gradient in diversity",
    "NCERT: in general, species diversity decreases as we move away from the equator towards the poles. With very "
    "few exceptions, the tropics (latitudinal range of 23.5° N to 23.5° S) harbour more species than temperate or "
    "polar areas.",
    ["Tropics: between the Tropic of Cancer (23.5° N) and the Tropic of Capricorn (23.5° S)"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    why="0° to 23.5° N covers only the northern half of the tropics. 66.5° N to 66.5° S is the whole belt between "
        "the polar circles, including the temperate zones. 23.5° N to 66.5° N is the northern temperate zone.",
    seconds=20)

add(BDC, "Importance and loss", "Basic", "direct",
    "According to NCERT, the colonisation of tropical Pacific islands by humans is said to have led to the "
    "extinction of more than how many species of native birds?",
    P("2,000", ["200", "20,000", "784"], "A"),
    "Human colonisation and loss of birds",
    "NCERT: the colonisation of tropical Pacific islands by humans is said to have led to the extinction of more than "
    "2,000 species of native birds.",
    ["Tropical Pacific islands: more than 2,000 native bird species lost"],
    C12_BD("loss of biodiversity"),
    why="200 and 20,000 are factor-of-ten slips; 784 is the IUCN (2004) count of documented extinctions of all kinds "
        "in the last 500 years.",
    seconds=20)

add(BDC, "Patterns of biodiversity", "Basic", "statement_pair",
    sp("The largely tropical Amazonian rain forest in South America has the greatest biodiversity on earth.",
       "The Amazonian rain forest is home to more species of birds than of fishes."),
    SP("C"),
    "Amazonian diversity",
    "NCERT: the largely tropical Amazonian rain forest has the greatest biodiversity on earth (Statement I true). "
    "It gives 3,000 species of fishes and 1,300 of birds for this forest, so fishes outnumber birds (Statement II "
    "false).",
    ["Statement I: true", "Fishes 3,000 > birds 1,300", "Statement II: false"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    seconds=25)

_ratio = F(1400, 56)
assert _ratio == 25

add(BDC, "Patterns of biodiversity", "Intermediate", "numerical",
    "NCERT illustrates the latitudinal gradient in diversity with bird species: Colombia, near the equator, has "
    "nearly 1,400 species of birds, New York (41° N) has 105 and Greenland (71° N) has 56. How many times as many "
    "bird species as Greenland does Colombia have?",
    P("25", ["2.5", "13", "250"], "D"),
    "Latitudinal gradient in species diversity",
    "Ratio = 1,400/56 = 25. Species diversity decreases as we move away from the equator towards the poles.",
    ["1,400 ÷ 56 = 25"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    why="2.5 and 250 are factor-of-ten slips; 13 (1,400/105) compares Colombia with New York, not Greenland.",
    seconds=30, verified_by=RECOMPUTED)

add(BDC, "Patterns of biodiversity", "Intermediate", "assertion_reason",
    ar("The Western Ghats have a greater amphibian species diversity than the Eastern Ghats.",
       "This is NCERT's example of genetic diversity."),
    AR("C"),
    "Levels of biodiversity",
    "NCERT gives the greater amphibian species diversity of the Western Ghats compared with the Eastern Ghats as its "
    "example of species diversity (A true). Its example of genetic diversity is Rauwolfia vomitoria, which shows "
    "genetic variation in the potency and concentration of reserpine in different Himalayan ranges; the example of "
    "ecological diversity is India compared with Norway (R false).",
    ["A: true", "It illustrates species diversity, not genetic diversity", "R: false"],
    C12_BD("biodiversity"),
    seconds=30)

add(BDC, "In situ and ex situ conservation", "Intermediate", "match_list",
    ml(("conservation term", "description in NCERT"),
       ["Biodiversity hotspots", "Sacred groves", "Cryopreservation", "Seed banks"],
       ["Long-term storage of seeds of different genetic strains of commercially important plants",
        "Regions with very high levels of species richness and a high degree of endemism",
        "Tracts of forest set aside in which all the trees and wildlife are venerated and given total protection",
        "Preservation of gametes of threatened species in viable and fertile condition for long periods"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,IV,III,I"), mc("II,III,I,IV")], "B"),
    "Tools of in situ and ex situ conservation",
    "NCERT: biodiversity hotspots are regions with very high levels of species richness and a high degree of "
    "endemism (in situ priority areas). In many cultures, tracts of forest were set aside as sacred groves, where all "
    "the trees and wildlife were venerated and given total protection (in situ). Gametes of threatened species can be "
    "preserved in viable and fertile condition for long periods using cryopreservation, and seeds of different "
    "genetic strains of commercially important plants can be kept for long periods in seed banks (both ex situ).",
    ["Hotspots (II)", "Sacred groves (III)", "Cryopreservation (IV)", "Seed banks (I)"],
    C12_BD("biodiversity conservation: in situ and ex situ"),
    why="The other codes swap hotspots with sacred groves, sacred groves with cryopreservation, or cryopreservation "
        "with seed banks.",
    seconds=35)

add(BDC, "Patterns of biodiversity", "Intermediate", "multi_statement",
    ms("Which of the following are among the hypotheses or observations given in NCERT to explain the greater "
       "biological diversity of the tropics?",
       ["Species diversity increases as we move from the equator towards the poles.",
        "Temperate regions were subjected to frequent glaciations in the past, while tropical latitudes remained "
        "relatively undisturbed for millions of years, allowing a long evolutionary time for diversification.",
        "Tropical environments are less seasonal, relatively more constant and predictable, which promotes niche "
        "specialisation.",
        "Temperate regions have had a longer undisturbed evolutionary time than the tropics.",
        "More solar energy is available in the tropics, which contributes to higher productivity and might "
        "contribute indirectly to greater diversity."]),
    MS(["b", "c", "e"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "Why the tropics are more diverse",
    "NCERT gives three hypotheses: speciation is a function of time and the tropics remained undisturbed while "
    "temperate regions underwent glaciations (b); tropical environments are less seasonal, more constant and "
    "predictable, promoting niche specialisation (c); more solar energy is available in the tropics, contributing to "
    "higher productivity (e). (a) reverses the latitudinal gradient, and (d) reverses the time hypothesis.",
    ["True: (b), (c), (e)", "(a): diversity decreases towards the poles", "(d): it is the tropics that were "
     "undisturbed"],
    C12_BD("patterns of biodiversity: latitudinal gradients"),
    why="Options with (a) or (d) include a false statement.",
    seconds=45)

add(BDC, "In situ and ex situ conservation", "Advanced", "direct",
    "Consider these measures: (i) storing pollen grains of a crop in liquid nitrogen at −196 °C; (ii) protecting a "
    "sacred grove; (iii) propagating a threatened plant by tissue culture; (iv) declaring a biosphere reserve. Which "
    "of these are means of ex situ conservation?",
    P("(i) and (iii) only", ["(ii) and (iv) only", "(i), (ii) and (iii) only", "(iii) only"], "D"),
    "In situ versus ex situ conservation",
    "Ex situ conservation protects species outside their natural habitat. NCERT lists cryopreservation of gametes, "
    "in vitro fertilisation, tissue culture propagation and seed banks among ex situ methods; pollen stored in "
    "liquid nitrogen in pollen banks (described in the chapter on sexual reproduction in flowering plants) is likewise "
    "kept outside the habitat. Sacred groves and biosphere reserves protect the whole ecosystem in place: in situ.",
    ["Outside the habitat: pollen bank (i), tissue culture (iii) → ex situ", "In place: sacred grove (ii), "
     "biosphere reserve (iv) → in situ"],
    C12_BD("biodiversity conservation: in situ and ex situ"),
    why="Sacred groves and biosphere reserves are in situ; '(iii) only' leaves out cryopreserved pollen, which is "
        "also stored away from the natural habitat.",
    seconds=45)

_z_reg = (2 ** 0.1, 2 ** 0.2)
_z_frug = 2 ** 1.15
assert 1.06 < _z_reg[0] < 1.08 and 1.14 < _z_reg[1] < 1.16 and abs(_z_frug - 2.22) < 0.01

add(BDC, "Patterns of biodiversity", "Advanced", "statement_pair",
    "Species richness and area follow log S = log C + Z log A, so S₂/S₁ = (A₂/A₁)^Z. "
    "(Take 2^0.1 ≈ 1.07, 2^0.2 ≈ 1.15 and 2^1.15 ≈ 2.22.)\n\n" +
    sp("Within a region, where Z lies between 0.1 and 0.2, doubling the area studied increases species richness by "
       "only about 7 to 15 per cent.",
       "For frugivorous birds and mammals in the tropical forests of different continents, where Z is 1.15, "
       "doubling the area more than doubles species richness."),
    SP("A"),
    "Using the slope Z of the species–area relationship",
    "From log S = log C + Z log A, S₂/S₁ = (A₂/A₁)^Z. For doubling, S₂/S₁ = 2^Z. Within a region: 2^0.1 ≈ 1.07 and "
    "2^0.2 ≈ 1.15, i.e. about 7–15 per cent more species (Statement I true). For Z = 1.15 (NCERT's value for "
    "frugivorous birds and mammals across continents): 2^1.15 ≈ 2.22, more than double (Statement II true). The "
    "needed powers of 2 are given in the stem.",
    ["S₂/S₁ = 2^Z", "Z = 0.1–0.2 → 1.07–1.15", "Z = 1.15 → ≈ 2.22"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    seconds=75, verified_by=RECOMPUTED)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Each NCERT example below is paired with one cause from the 'Evil Quartet'. Which pairings are correct?",
       ["Clearing of the Amazon rain forest for soya bean cultivation and cattle grazing: habitat loss and "
        "fragmentation",
        "Extinction of more than 200 species of cichlid fish after the Nile perch was introduced into Lake Victoria: "
        "co-extinction",
        "Extinction of Steller's sea cow and the passenger pigeon: over-exploitation",
        "Loss of the unique parasites of a host fish species that becomes extinct: over-exploitation",
        "Threat to indigenous catfishes from the illegal introduction of the African catfish Clarias gariepinus: "
        "alien species invasion"]),
    MS(["a", "c", "e"], [["a", "b", "c", "e"], ["a", "c", "d"], ["b", "d", "e"]], "B"),
    "Causes of biodiversity loss",
    "(a) Habitat loss and fragmentation: correct. (b) The Nile perch is NCERT's example of alien species invasion, "
    "not co-extinction. (c) Over-exploitation by humans: correct. (d) Parasites dying with their extinct host is "
    "NCERT's example of co-extinction, not over-exploitation. (e) Alien species invasion: correct.",
    ["Correct: (a), (c), (e)", "(b): alien invasion", "(d): co-extinction"],
    C12_BD("loss of biodiversity: causes"),
    why="Options with (b) or (d) contain a wrongly labelled cause.",
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

    doc = {"schema_version": "1.0", "batch_id": "BATCH_007", "created_at": TODAY,
           "notes": "BATCH_007 package BOT_007_p2: 125 original Botany questions (Plant Growth and Development to "
                    "Biodiversity and Conservation), each with an NCERT reference. Facts tested in BATCH_000 to "
                    "BATCH_006 were avoided or approached from a new angle. Numerical and other computable answers "
                    "re-derived by tools/batch_007/BOT_007_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions")
    print("difficulty", dict(Counter(q["difficulty"] for q in QUESTIONS)))


if __name__ == "__main__":
    main()
