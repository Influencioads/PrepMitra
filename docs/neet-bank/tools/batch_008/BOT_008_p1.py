"""Writes batches/parts/BATCH_008_BOT_p1.json: package BOT_008_p1 of batch 8 (Botany, 130 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants, Plant Growth and Development. IDs NEET_BOT_001751 .. NEET_BOT_001880.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books or outside the NMC 2026 list (secondary growth, taxonomical aids, plant life cycles and
alternation of generations, early experiments on photosynthesis, seed dormancy, photoperiodism, vernalisation) is not
used. Facts already tested in batches 1-7 were listed with `merge_batch.py stems 008 BOT_008_p1` and avoided; where a
topic is saturated, questions test new combinations, comparisons or applications. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_008/BOT_008_p1.py
"""

import json
import sys
from collections import Counter
from fractions import Fraction
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
PLAN = ROOT / "batches" / "plans" / "BATCH_008_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_008_BOT_p1.json"
PACKAGE = "BOT_008_p1"
BATCH = "BATCH_008"
TODAY = "2026-11-16"
LETTERS = "ABCD"
BOT = "Botany"
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

T_LIV = "The Living World and Classification"
T_PK = "Plant Kingdom"
T_MOR = "Morphology of Flowering Plants"
T_ANA = "Anatomy of Flowering Plants"
T_CELL = "Cell: The Unit of Life"
T_CC = "Cell Cycle and Cell Division"
T_PS = "Photosynthesis"
T_RES = "Respiration in Plants"
T_PGD = "Plant Growth and Development"

CHAPTER = {
    "LW": "The Living World", "BC": "Biological Classification", "PK": "Plant Kingdom",
    "MOR": "Morphology of Flowering Plants", "ANA": "Anatomy of Flowering Plants", "CELL": "Cell: The Unit of Life",
    "CC": "Cell Cycle and Cell Division", "PS": "Photosynthesis in Higher Plants", "RES": "Respiration in Plants",
    "PGD": "Plant Growth and Development",
}


def ref(ch, section):
    return f"Class 11 Biology, '{CHAPTER[ch]}', {section}"


QUESTIONS = []


def _record(topic, sub, diff, fmt, text, concept, expl, steps, why, ncert, secs, verified_by, short=None):
    assert diff in ("Basic", "Intermediate", "Advanced") and ncert and 20 <= secs <= 180 and steps
    return {
        "question_id": None, "exam_mappings": default_mappings(BOT), "subject": BOT, "topic": topic,
        "subtopic": sub, "difficulty": diff, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text, "options": None, "correct_answer": None,
        "solution": {"concept": concept, "explanation": expl, "steps": steps, "shortcut": short,
                     "why_others_wrong": why, "ncert_reference": ncert, "final_answer": None},
        "suggested_time_seconds": secs,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(verified_by), "verified_at": TODAY},
    }


def _fix(rec, options, answer):
    assert len(options) == 4 and len(set(options)) == 4 and answer in LETTERS
    rec["options"] = [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)]
    rec["correct_answer"] = answer
    rec["solution"]["final_answer"] = f"Option {answer}: {options[LETTERS.index(answer)]}"


def _place(correct, wrong, at):
    """Puts the correct option at the hand-chosen position `at`; the wrong ones keep their written order."""
    assert len(wrong) == 3 and correct not in wrong and at in LETTERS
    opts = list(wrong)
    opts.insert(LETTERS.index(at), correct)
    return opts


def direct(topic, sub, diff, text, correct, wrong, at, concept, expl, steps, why=None, ncert=None, secs=30,
           short=None):
    rec = _record(topic, sub, diff, "direct", text, concept, expl, steps, why, ncert, secs, AUTHORED, short)
    _fix(rec, _place(correct, wrong, at), at)
    QUESTIONS.append(rec)


def numerical(topic, sub, diff, text, correct, wrong, at, value_check, concept, expl, steps, why, ncert, secs=60,
              short=None):
    """value_check must be True: the builder's own recomputation of the answer."""
    assert value_check is True
    rec = _record(topic, sub, diff, "numerical", text, concept, expl, steps, why, ncert, secs, RECOMPUTED, short)
    _fix(rec, _place(correct, wrong, at), at)
    QUESTIONS.append(rec)


def assertion_reason(topic, sub, diff, a_text, r_text, a_true, r_true, explains, expect, concept, expl, steps,
                     why=None, ncert=None, secs=45):
    if a_true and r_true:
        key = "A" if explains else "B"
    elif a_true:
        key = "C"
    elif r_true:
        key = "D"
    else:
        raise AssertionError("A and R both false is not one of the fixed options")
    assert key == expect, (a_text, key, expect)
    text = ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {a_text}\nReason (R): {r_text}\n\n"
            "Choose the correct answer from the options given below:")
    rec = _record(topic, sub, diff, "assertion_reason", text, concept, expl, steps, why, ncert, secs, AUTHORED)
    _fix(rec, list(ASSERTION_REASON), key)
    QUESTIONS.append(rec)


def statement_pair(topic, sub, diff, s1, s2, t1, t2, expect, concept, expl, steps, why=None, ncert=None, secs=40):
    key = {(True, True): "A", (False, False): "B", (True, False): "C", (False, True): "D"}[(t1, t2)]
    assert key == expect, (s1, key, expect)
    text = (f"Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")
    rec = _record(topic, sub, diff, "statement_pair", text, concept, expl, steps, why, ncert, secs, AUTHORED)
    _fix(rec, list(STATEMENT_PAIR), key)
    QUESTIONS.append(rec)


def combo_label(combo):
    parts = [f"({c})" for c in combo]
    return (parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]) + " only"


def multi_statement(topic, sub, diff, lead, statements, wrong_combos, at, concept, expl, steps, why=None, ncert=None,
                    secs=60):
    """statements: list of (text, is_true). The correct combination is derived from the truth values."""
    labels = "abcde"[:len(statements)]
    correct = tuple(labels[i] for i, (_, t) in enumerate(statements) if t)
    assert correct and len(correct) < len(statements), "need at least one true and one false statement"
    wrong = [tuple(w) for w in wrong_combos]
    assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3
    assert all(set(w) <= set(labels) for w in wrong)
    body = "\n".join(f"({labels[i]}) {s}" for i, (s, _) in enumerate(statements))
    text = f"{lead}\n\n{body}\n\nChoose the correct answer from the options given below:"
    rec = _record(topic, sub, diff, "multi_statement", text, concept, expl, steps, why, ncert, secs, AUTHORED)
    _fix(rec, _place(combo_label(correct), [combo_label(w) for w in wrong], at), at)
    QUESTIONS.append(rec)


def _code(m):
    return ", ".join(f"{k}-{m[k]}" for k in "ABCD")


def _m(code):
    """'III IV II I' -> {'A': 'III', 'B': 'IV', 'C': 'II', 'D': 'I'}"""
    return dict(zip("ABCD", code.split()))


def match_list(topic, sub, diff, head1, head2, list1, list2, correct, wrongs, at, concept, expl, steps, why=None,
               ncert=None, secs=45):
    """list1: 4 items (A-D); list2: 4 items (I-IV); correct/wrongs: codes like 'III IV II I'."""
    nums = ["I", "II", "III", "IV"]
    correct, wrongs = _m(correct), [_m(w) for w in wrongs]
    assert len(list1) == 4 and len(list2) == 4
    for m in [correct, *wrongs]:
        assert sorted(m.values(), key=nums.index) == nums and sorted(m) == list("ABCD")
    assert len(wrongs) == 3 and len({_code(m) for m in [correct, *wrongs]}) == 4
    l1 = "\n".join(f"{k}. {t}" for k, t in zip("ABCD", list1))
    l2 = "\n".join(f"{n}. {t}" for n, t in zip(nums, list2))
    text = (f"Match List-I ({head1}) with List-II ({head2}).\n\nList-I:\n{l1}\n\nList-II:\n{l2}\n\n"
            "Choose the correct answer from the options given below:")
    rec = _record(topic, sub, diff, "match_list", text, concept, expl, steps, why, ncert, secs, AUTHORED)
    _fix(rec, _place(_code(correct), [_code(w) for w in wrongs], at), at)
    QUESTIONS.append(rec)


# =============================================================== 1. The Living World and Classification (6/7/5)
direct(T_LIV, "Binomial nomenclature", "Basic",
       "In the biological name Mangifera indica Linn., the abbreviation 'Linn.' written after the specific epithet "
       "indicates that:",
       "this species was first described by Linnaeus",
       ["the genus Mangifera belongs to an order named by Linnaeus", "the name is written in Latin",
        "the plant is kept in Linnaeus's herbarium"], "A",
       "Author citation in a biological name",
       "By the rules of binomial nomenclature, the name of the author appears after the specific epithet, that is, at "
       "the end of the biological name, and is written in an abbreviated form. In Mangifera indica Linn., 'Linn.' "
       "indicates that this species was first described by Linnaeus.",
       ["The author's name is written after the specific epithet in abbreviated form",
        "Linn. = the species was first described by Linnaeus"],
       why="The author citation says who first described the species. It says nothing about who named the order, "
           "about the Latin form of the name (that is shown by the Latinised words themselves) or about a herbarium.",
       ncert=ref("LW", "Diversity in the Living World (rules of binomial nomenclature)"), secs=25)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Bacteria are grouped into four categories based on their shape. Spiral-shaped bacteria are called:",
       "Spirillum",
       ["Coccus", "Bacillus", "Vibrio (Vibrium)"], "C",
       "Shapes of bacteria",
       "Based on their shape, bacteria are grouped under four categories: the spherical Coccus (pl. cocci), the "
       "rod-shaped Bacillus (pl. bacilli), the comma-shaped Vibrium (pl. vibrio) and the spiral Spirillum "
       "(pl. spirilla).",
       ["Spherical = coccus; rod = bacillus", "Comma = vibrium; spiral = spirillum"],
       why="Coccus is spherical, Bacillus rod-shaped and Vibrio (Vibrium) comma-shaped.",
       ncert=ref("BC", "Kingdom Monera"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "Classification involves a hierarchy of steps in which each step represents a rank or category. All the "
       "taxonomic categories taken together constitute the:",
       "taxonomic hierarchy",
       ["taxon", "nomenclature", "International Code for Botanical Nomenclature"], "D",
       "Taxonomic categories and hierarchy",
       "Classification is not a single-step process but involves a hierarchy of steps in which each step represents a "
       "rank or category. Since the category is a part of the overall taxonomic arrangement, it is called a taxonomic "
       "category, and all the categories together constitute the taxonomic hierarchy.",
       ["Each step = a rank or category", "All categories together = taxonomic hierarchy"],
       why="A taxon is a single unit (rank) of classification, not all of them together. Nomenclature is naming. "
           "ICBN is the code that gives the rules for naming plants.",
       ncert=ref("LW", "Taxonomic Categories"), secs=20)

direct(T_LIV, "Lichens, viruses and viroids", "Basic",
       "Bovine spongiform encephalopathy (BSE) is a prion disease of cattle. The analogous prion disease of humans "
       "named in NCERT is:",
       "Creutzfeldt–Jakob disease (CJD)",
       ["AIDS", "Potato spindle tuber disease", "Sleeping sickness"], "B",
       "Prion diseases",
       "Prions are infectious agents consisting of abnormally folded protein, similar in size to viruses, that "
       "transmit certain infectious neurological diseases. The most notable prion diseases are bovine spongiform "
       "encephalopathy (BSE), commonly called mad cow disease, in cattle and its analogous variant, "
       "Creutzfeldt–Jakob disease (CJD), in humans.",
       ["Prion = abnormally folded protein", "BSE in cattle; CJD in humans"],
       why="AIDS is caused by a virus. Potato spindle tuber disease is caused by a viroid. Sleeping sickness is caused "
           "by the flagellated protozoan Trypanosoma.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=20)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Basic",
               "Though the structure of bacteria is very simple, they are very complex in behaviour.",
               "Some heterotrophic bacteria are helpful in the production of antibiotics.",
               True, True, "A",
               "Bacteria: simple structure, complex behaviour and human uses",
               "NCERT notes that although bacterial structure is very simple, bacteria are very complex in behaviour, "
               "and as a group they show the most extensive metabolic diversity. Many heterotrophic bacteria have a "
               "significant impact on human affairs: they help in making curd from milk, in the production of "
               "antibiotics and in fixing nitrogen in legume roots.",
               ["Statement I: true", "Statement II: true; antibiotic production is one of the listed uses"],
               ncert=ref("BC", "Kingdom Monera (eubacteria)"), secs=30)

match_list(T_LIV, "Lichens, viruses and viroids", "Basic", "scientist", "year of the work as given in NCERT",
           ["Dmitri Ivanowsky (causal organism of mosaic disease of tobacco)",
            "M.W. Beijerinek ('Contagium vivum fluidum')",
            "W.M. Stanley (viruses can be crystallised)",
            "T.O. Diener (viroid)"],
           ["1935", "1971", "1892", "1898"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B",
           "History of the discovery of viruses and viroids",
           "Dmitri Ivanowsky (1892) recognised certain microbes, smaller than bacteria, as the causal organism of the "
           "mosaic disease of tobacco. M.W. Beijerinek (1898) called the fluid from infected plants 'Contagium vivum "
           "fluidum'. W.M. Stanley (1935) showed that viruses could be crystallised. T.O. Diener (1971) discovered the "
           "viroid, the agent of potato spindle tuber disease.",
           ["Ivanowsky 1892 → Beijerinek 1898", "Stanley 1935 → Diener 1971"],
           why="The wrong codes swap the two nineteenth-century dates, or the two twentieth-century dates, or put "
               "Stanley's 1935 work before Ivanowsky's.",
           ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=35)

direct(T_LIV, "Taxonomy and hierarchy", "Intermediate",
       "Which of the following lists the taxa of the lion (Panthera leo) correctly, going from the lower to the "
       "higher category?",
       "Panthera → Felidae → Carnivora → Mammalia → Chordata",
       ["Panthera → Carnivora → Felidae → Mammalia → Chordata",
        "Panthera → Felidae → Mammalia → Carnivora → Chordata",
        "Felidae → Panthera → Carnivora → Mammalia → Chordata"], "C",
       "Taxonomic hierarchy of the lion",
       "The lion (Panthera leo) belongs to genus Panthera, which with the genus Felis forms the family Felidae. The "
       "order Carnivora includes families like Felidae and Canidae. Class Mammalia includes order Carnivora (tiger, "
       "cat, dog) along with order Primata. Mammals, with fishes, amphibians, reptiles and birds, form phylum "
       "Chordata.",
       ["Genus Panthera → family Felidae", "Family Felidae → order Carnivora → class Mammalia → phylum Chordata"],
       why="Order is above family, so Carnivora cannot come before Felidae; class is above order, so Mammalia cannot "
           "come before Carnivora; family is above genus.",
       ncert=ref("LW", "Taxonomic Categories"), secs=40)

assertion_reason(T_LIV, "Five kingdom classification", "Intermediate",
                 "The boundaries of kingdom Protista are not well defined.",
                 "What may be 'a photosynthetic protistan' to one biologist may be 'a plant' to another.",
                 True, True, True, "A",
                 "Kingdom Protista",
                 "All single-celled eukaryotes are placed under Protista, but the boundaries of this kingdom are not well "
                 "defined. NCERT gives the reason in the same line: what may be 'a photosynthetic protistan' to one "
                 "biologist may be 'a plant' to another. Because the same organism can be placed differently by "
                 "different biologists, the limits of the kingdom are not sharp.",
                 ["A: true", "R: true, and it is the reason the boundaries are unclear"],
                 ncert=ref("BC", "Kingdom Protista"), secs=40)

statement_pair(T_LIV, "Lichens, viruses and viroids", "Intermediate",
               "In a lichen, the phycobiont is autotrophic and the mycobiont is heterotrophic.",
               "The association of the partners in a lichen is so close that, on seeing a lichen in nature, one would "
               "never imagine that it has two different organisms within it.",
               True, True, "A",
               "Lichens",
               "Lichens are symbiotic, mutually useful associations between algae and fungi. The algal component is "
               "the phycobiont and the fungal component the mycobiont; they are autotrophic and heterotrophic "
               "respectively. The algae prepare food for the fungi, and the fungi provide shelter and absorb mineral "
               "nutrients and water for their partner. Their association is so close that one would never imagine "
               "that a lichen has two different organisms within it.",
               ["Statement I: phycobiont = alga = autotrophic; mycobiont = fungus = heterotrophic: true",
                "Statement II: true"],
               ncert=ref("BC", "Viruses, Viroids, Prions and Lichens (lichens)"), secs=35)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate", "term used for the sexual cycle of fungi",
           "meaning",
           ["Plasmogamy", "Karyogamy", "Dikaryon", "Meiosis in the zygote"],
           ["Condition with two nuclei per cell (n + n)", "Formation of haploid spores",
            "Fusion of the protoplasms of two motile or non-motile gametes", "Fusion of two nuclei"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D",
           "Steps of sexual reproduction in fungi",
           "The sexual cycle of fungi has three steps: fusion of protoplasms between two motile or non-motile gametes "
           "(plasmogamy), fusion of two nuclei (karyogamy) and meiosis in the zygote, resulting in haploid spores. In "
           "ascomycetes and basidiomycetes an intervening stage with two nuclei per cell (n + n) occurs; this "
           "condition is called a dikaryon.",
           ["Plasmogamy = protoplasm fusion; karyogamy = nuclear fusion",
            "Dikaryon = n + n; meiosis in zygote → haploid spores"],
           why="The wrong codes interchange protoplasmic and nuclear fusion, or the dikaryon with the result of "
               "meiosis.",
           ncert=ref("BC", "Kingdom Fungi"), secs=40)

assertion_reason(T_LIV, "Lichens, viruses and viroids", "Intermediate",
                 "Once a virus infects a cell, the host cell is usually killed.",
                 "After infecting a cell, the virus takes over the machinery of the host cell to replicate itself.",
                 True, True, True, "A",
                 "Viruses as obligate parasites",
                 "Viruses are non-cellular and have an inert crystalline structure outside a living cell. Once they "
                 "infect a cell, they take over the machinery of the host cell to replicate themselves, killing the "
                 "host. The host dies because its machinery is used up to make new viruses, so R explains A.",
                 ["A: true", "R: true; using the host's machinery for its own replication is what kills the host"],
                 ncert=ref("BC", "Viruses, Viroids, Prions and Lichens (viruses)"), secs=40)

direct(T_LIV, "Five kingdom classification", "Intermediate",
       "The two kingdom system did not distinguish between photosynthetic and non-photosynthetic organisms. Which "
       "pair of organisms illustrates this, both having been placed in the same kingdom?",
       "Chlamydomonas (a green alga) and Mucor (a fungus)",
       ["Amoeba and Paramoecium", "Mango and wheat", "Lion and the housefly"], "B",
       "Drawbacks of the two kingdom system",
       "In the two kingdom system (Plantae and Animalia) of Linnaeus's time, green algae such as Chlamydomonas and "
       "fungi such as Mucor were both placed under plants. The system did not distinguish between photosynthetic "
       "(green algae) and non-photosynthetic (fungi) organisms, which is one reason it was found inadequate.",
       ["Two kingdoms: Plantae and Animalia", "Green alga (photosynthetic) and fungus (non-photosynthetic) both in Plantae"],
       why="Amoeba and Paramoecium were both animals and both non-photosynthetic; mango and wheat are both "
           "photosynthetic plants; the lion and the housefly are both animals.",
       ncert=ref("BC", "Introduction (two kingdom classification)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Neurospora is used extensively in biochemical and genetic work.",
                 "Morels and truffles are edible ascomycetes and are considered delicacies.",
                 True, True, False, "B",
                 "Ascomycetes and their uses",
                 "NCERT names Aspergillus, Claviceps and Neurospora as examples of ascomycetes and notes that Neurospora "
                 "is used extensively in biochemical and genetic work. Separately, it notes that many members, such as "
                 "morels and truffles, are edible and are considered delicacies. That some other ascomycetes are edible "
                 "has nothing to do with why Neurospora is used in research.",
                 ["A: true", "R: true", "R is about different members of the class, unrelated to A"],
                 ncert=ref("BC", "Kingdom Fungi (Ascomycetes)"), secs=40)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Advanced",
                "Which of the following spores are produced exogenously, that is, not inside a sporangium or a sac?",
                [("Conidia of Aspergillus, formed on conidiophores", True),
                 ("Basidiospores of Agaricus, formed on the basidium", True),
                 ("Aplanospores of Mucor", False),
                 ("Ascospores of Neurospora", False),
                 ("Zoospores of phycomycetes", False)],
                [("a", "b", "d"), ("b", "c"), ("a", "c", "e")], "D",
                "Exogenous and endogenous spores of fungi",
                "In phycomycetes, the asexual spores (motile zoospores or non-motile aplanospores) are produced "
                "endogenously in a sporangium. In ascomycetes, the asexual conidia are produced exogenously on special "
                "mycelium called conidiophores, while the sexual ascospores are produced endogenously in sac-like asci. "
                "In basidiomycetes, basidiospores are produced exogenously on the basidium.",
                ["(a) exogenous", "(b) exogenous", "(c), (e) endogenous in a sporangium", "(d) endogenous in an ascus"],
                why="Any combination with (c), (d) or (e) includes a spore formed inside a sporangium or an ascus.",
                ncert=ref("BC", "Kingdom Fungi"), secs=60)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following statements are true of both Euglena and Nostoc?",
                [("Both can make their own food by photosynthesis.", True),
                 ("Both have chlorophyll a.", True),
                 ("Both have a well-defined nucleus.", False),
                 ("Both have a cell wall made of cellulose.", False),
                 ("Both are placed in the same kingdom in Whittaker's system.", False)],
                [("a", "b", "e"), ("a", "c"), ("b", "d", "e")], "B",
                "Comparing a euglenoid with a cyanobacterium",
                "Euglena is a euglenoid protist: photosynthetic in sunlight, with pigments identical to those of higher "
                "plants; it has no cell wall but a protein-rich pellicle, and, being eukaryotic, a well-defined "
                "nucleus. Nostoc is a cyanobacterium (kingdom Monera): a photosynthetic autotroph with chlorophyll a "
                "similar to green plants, a prokaryotic cell without a well-defined nucleus, and a non-cellulosic cell "
                "wall.",
                ["(a) true for both", "(b) true: Nostoc has chlorophyll a; Euglena's pigments are those of higher plants",
                 "(c) false: Nostoc is prokaryotic", "(d) false: Euglena has a pellicle, Nostoc a non-cellulosic wall",
                 "(e) false: Protista vs Monera"],
                why="(c), (d) and (e) each fail for at least one of the two organisms.",
                ncert=ref("BC", "Kingdom Monera; Kingdom Protista (euglenoids)"), secs=75)

direct(T_LIV, "Five kingdom classification", "Advanced",
       "Which of the following features is shared by all members of kingdom Fungi and kingdom Animalia?",
       "They are eukaryotic and heterotrophic.",
       ["Their cells lack a cell wall.", "Their nutrition is holozoic, by ingestion of food.",
        "Their body is always multicellular."], "C",
       "Fungi and animals compared",
       "Both fungi and animals are eukaryotic and heterotrophic. Fungal cells, however, have cell walls made of "
       "chitin and polysaccharides, whereas animal cells lack cell walls. Animals show holozoic nutrition (ingestion), "
       "whereas most fungi absorb soluble organic matter as saprophytes or parasites. Yeasts are unicellular, so "
       "fungi are not always multicellular.",
       ["Shared: eukaryotic + heterotrophic", "Wall: fungi yes (chitin), animals no",
        "Nutrition: absorptive (fungi) vs holozoic (animals)", "Yeast is unicellular"],
       why="Fungi have chitinous walls, absorb rather than ingest food, and include unicellular yeasts.",
       ncert=ref("BC", "Kingdom Fungi; Kingdom Animalia"), secs=50)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Advanced",
               "The morphology of the mycelium, the mode of spore formation and the fruiting bodies form the basis for "
               "dividing the kingdom Fungi into various classes.",
               "Asexual reproduction in fungi takes place by oospores, ascospores and basidiospores.",
               True, False, "C",
               "Basis of classification of fungi and types of spores",
               "NCERT states that the morphology of the mycelium, the mode of spore formation and the fruiting bodies "
               "form the basis for the division of the kingdom into various classes. Asexual reproduction is by spores "
               "called conidia, sporangiospores or zoospores; oospores, ascospores and basidiospores are formed in "
               "sexual reproduction.",
               ["Statement I: true", "Statement II: false; oospores, ascospores and basidiospores are sexual spores"],
               ncert=ref("BC", "Kingdom Fungi"), secs=45)

_BACT = {"cholera": True, "typhoid": True, "malaria": False, "tetanus": True, "sleeping sickness": False,
         "citrus canker": True, "mumps": False, "wheat rust": False}
numerical(T_LIV, "Monera, Protista and Fungi", "Advanced",
          "How many of the following diseases are named in NCERT as diseases caused by bacteria?\n"
          "cholera, typhoid, malaria, tetanus, sleeping sickness, citrus canker, mumps, wheat rust",
          "4", ["3", "5", "6"], "D", sum(_BACT.values()) == 4,
          "Causal organisms of common diseases",
          "NCERT names cholera, typhoid, tetanus and citrus canker as well-known diseases caused by different bacteria. "
          "Malaria is caused by the sporozoan Plasmodium, sleeping sickness by the flagellated protozoan Trypanosoma, "
          "mumps by a virus and wheat rust by the fungus Puccinia.",
          ["Bacterial: cholera, typhoid, tetanus, citrus canker = 4",
           "Not bacterial: malaria (protozoan), sleeping sickness (protozoan), mumps (virus), wheat rust (fungus)"],
          why="3 leaves out citrus canker, a bacterial disease of plants; 5 adds wheat rust (a fungus) or malaria (a "
              "protozoan); 6 adds both protozoan diseases.",
          ncert=ref("BC", "Kingdom Monera; Kingdom Protista; Kingdom Fungi; Viruses"), secs=50)


# =============================================================== 2. Plant Kingdom (5/6/5)
direct(T_PK, "Bryophytes", "Basic",
       "The plant body of the liverwort Marchantia is a thallus that is:",
       "dorsiventral and closely appressed to the substrate",
       ["erect and radially symmetrical", "differentiated into true root, stem and leaves",
        "a creeping, branched, filamentous protonema"], "A",
       "Plant body of a liverwort",
       "The plant body of a liverwort is thalloid, e.g. Marchantia. The thallus is dorsiventral and closely appressed "
       "to the substrate. Liverworts grow in moist, shady habitats such as banks of streams, marshy ground, damp soil "
       "and the bark of trees.",
       ["Liverwort body = thallus", "Marchantia thallus: dorsiventral, closely appressed to the substrate"],
       why="The thallus is not erect or radially symmetrical. Bryophytes lack true roots, stems and leaves. The "
           "protonema is the first stage of the moss gametophyte, not the liverwort thallus.",
       ncert=ref("PK", "Bryophytes (liverworts)"), secs=25)

direct(T_PK, "Pteridophytes", "Basic",
       "Pteridophytes in which all the spores produced are of a similar kind are called:",
       "homosporous",
       ["heterosporous", "isogamous", "oogamous"], "B",
       "Homospory and heterospory",
       "In the majority of pteridophytes all the spores are of similar kinds; such plants are called homosporous. "
       "Genera like Selaginella and Salvinia, which produce two kinds of spores, macro (large) and micro (small) "
       "spores, are known as heterosporous.",
       ["One kind of spore = homosporous", "Two kinds (micro and macro) = heterosporous"],
       why="Heterosporous plants produce two kinds of spores. Isogamous and oogamous describe the kind of gametes that "
           "fuse, not the spores.",
       ncert=ref("PK", "Pteridophytes"), secs=20)

direct(T_PK, "Algae", "Basic",
       "Sexual reproduction in members of Phaeophyceae (brown algae) is:",
       "isogamous, anisogamous or oogamous",
       ["only oogamous", "only isogamous", "absent; they reproduce only by zoospores"], "C",
       "Sexual reproduction in brown algae",
       "In brown algae, asexual reproduction is mostly by biflagellate zoospores. Sexual reproduction may be "
       "isogamous, anisogamous or oogamous. Union of gametes may take place in water or within the oogonium "
       "(oogamous species).",
       ["Brown algae: all three types of sexual reproduction occur"],
       why="Brown algae are not restricted to one type of gamete fusion, and they do reproduce sexually.",
       ncert=ref("PK", "Algae (Phaeophyceae)"), secs=25)

statement_pair(T_PK, "Bryophytes", "Basic",
               "The sex organs of bryophytes are multicellular.",
               "The antheridium of a bryophyte produces a single antherozoid.",
               True, False, "C",
               "Sex organs of bryophytes",
               "The main plant body of a bryophyte is haploid and produces gametes, so it is a gametophyte. The sex "
               "organs in bryophytes are multicellular. The male sex organ, the antheridium, produces biflagellate "
               "antherozoids (many of them). The female sex organ, the archegonium, is flask-shaped and produces a "
               "single egg.",
               ["Statement I: true", "Statement II: false; it is the archegonium that produces a single egg; the "
                "antheridium produces antherozoids"],
               ncert=ref("PK", "Bryophytes"), secs=30)

match_list(T_PK, "Algae", "Basic", "plant", "group",
           ["Ulothrix", "Laminaria", "Gelidium", "Lycopodium"],
           ["Brown alga", "Pteridophyte", "Green alga", "Red alga"],
           "III I IV II", ["I III IV II", "III I II IV", "IV I III II"], "D",
           "Identifying members of the plant kingdom",
           "Ulothrix is a filamentous green alga (Chlorophyceae). Laminaria is a brown alga (Phaeophyceae). Gelidium is "
           "a red alga (Rhodophyceae), one of the sources of agar. Lycopodium is a pteridophyte of the class "
           "Lycopsida.",
           ["Ulothrix → green alga; Laminaria → brown alga", "Gelidium → red alga; Lycopodium → pteridophyte"],
           why="The wrong codes swap the green and brown algae, the red alga and the pteridophyte, or the green and red "
               "algae.",
           ncert=ref("PK", "Algae; Pteridophytes"), secs=30)

assertion_reason(T_PK, "Gymnosperms", "Intermediate",
                 "Gymnosperms are heterosporous.",
                 "The roots of Pinus have a fungal association in the form of mycorrhiza.",
                 True, True, False, "B",
                 "Gymnosperms: spores and roots",
                 "Gymnosperms are heterosporous: they produce haploid microspores and megaspores within sporangia "
                 "borne on sporophylls. Separately, the roots of some genera have a fungal association in the form of "
                 "mycorrhiza (Pinus), while in others (Cycas) coralloid roots are associated with nitrogen-fixing "
                 "cyanobacteria. The root association has nothing to do with the kinds of spores formed.",
                 ["A: true", "R: true", "R is a feature of the roots, unrelated to spore production"],
                 ncert=ref("PK", "Gymnosperms"), secs=35)

assertion_reason(T_PK, "Pteridophytes", "Intermediate",
                 "The prothallus that develops from a spore of a fern is haploid.",
                 "In pteridophytes, the spores are produced by meiosis in spore mother cells within the sporangia.",
                 True, True, True, "A",
                 "Origin of the pteridophyte gametophyte",
                 "The sporophyte bears sporangia, which produce spores by meiosis in spore mother cells. Each spore is "
                 "therefore haploid, and it germinates to give rise to a small, multicellular, free-living, mostly "
                 "photosynthetic thalloid gametophyte called the prothallus. The gametophyte is haploid because the "
                 "spore it grows from was formed by meiosis.",
                 ["Spore mother cell (2n) → meiosis → spores (n)", "Spore (n) → prothallus (n)"],
                 ncert=ref("PK", "Pteridophytes"), secs=40)

statement_pair(T_PK, "Algae", "Intermediate",
               "The red thalli of most red algae are multicellular, and some red algae have a complex body "
               "organisation.",
               "All members of Rhodophyceae live in salt water; none is found in fresh water.",
               True, False, "C",
               "Body and habitat of red algae",
               "NCERT states that the red thalli of most of the red algae are multicellular and some of them have "
               "complex body organisation. The majority of red algae are marine, but NCERT's table gives their habitat "
               "as fresh water (some), brackish water and salt water (most); so some red algae do live in fresh water.",
               ["Statement I: true", "Statement II: false; some red algae are fresh-water forms"],
               ncert=ref("PK", "Algae (Rhodophyceae; Table 3.1)"), secs=35)

direct(T_PK, "Gymnosperms", "Intermediate",
       "Which of the following pairs consists of two plants that are both heterosporous?",
       "Pinus and Salvinia",
       ["Funaria and Cycas", "Marchantia and Salvinia", "Polytrichum and Selaginella"], "D",
       "Heterospory in pteridophytes and gymnosperms",
       "Heterospory (production of two kinds of spores, microspores and megaspores) is found in some pteridophytes, "
       "such as Selaginella and Salvinia, and in all gymnosperms, which produce haploid microspores and megaspores. "
       "Bryophytes such as Funaria, Polytrichum (mosses) and Marchantia (a liverwort) do not produce two kinds of "
       "spores.",
       ["Gymnosperms (Pinus, Cycas): heterosporous", "Selaginella, Salvinia: heterosporous pteridophytes",
        "Mosses and liverworts: not heterosporous"],
       why="Each wrong pair contains a bryophyte (Funaria, Marchantia or Polytrichum), which does not form "
           "microspores and megaspores.",
       ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=40)

match_list(T_PK, "Algae", "Intermediate", "group", "habitat as given in NCERT",
           ["Chlorophyceae", "Phaeophyceae", "Rhodophyceae", "Bryophytes"],
           ["Fresh water (some), brackish water, salt water (most)", "Moist, shaded areas in the hills",
            "Fresh water, brackish water, salt water", "Fresh water (rare), brackish water, salt water"],
           "III IV I II", ["I IV III II", "III I IV II", "IV III I II"], "A",
           "Habitats of the classes of algae",
           "NCERT's table of the divisions of algae gives the habitat of Chlorophyceae as fresh water, brackish water "
           "and salt water; of Phaeophyceae as fresh water (rare), brackish water and salt water; and of Rhodophyceae "
           "as fresh water (some), brackish water and salt water (most). Bryophytes are found commonly growing in "
           "moist, shaded areas in the hills.",
           ["Green algae: all three waters, no qualifier", "Brown algae: fresh water rare",
            "Red algae: some fresh water, most marine", "Bryophytes: moist shaded hills"],
           why="The wrong codes interchange the 'rare' and 'some' qualifiers of the brown and red algae, or give the "
               "unqualified habitat to brown or red algae.",
           ncert=ref("PK", "Algae (Table 3.1); Bryophytes"), secs=45)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Sexual reproduction in all algae is oogamous.",
                 "In Spirogyra, fusion takes place between non-flagellated gametes that are similar in size.",
                 False, True, False, "D",
                 "Kinds of sexual reproduction in algae",
                 "Sexual reproduction in algae varies. Fusion of two gametes similar in size is isogamous: the gametes "
                 "may be flagellated (Chlamydomonas) or non-flagellated (Spirogyra). Fusion of two gametes dissimilar "
                 "in size is anisogamous (species of Eudorina). Fusion of a large, non-motile female gamete "
                 "with a smaller, motile male gamete is oogamous (Volvox, Fucus). So not all algae are oogamous; "
                 "Spirogyra itself is an exception.",
                 ["A: false; isogamy and anisogamy also occur", "R: true (isogamy with non-flagellated gametes)"],
                 ncert=ref("PK", "Algae"), secs=40)

multi_statement(T_PK, "Bryophytes", "Advanced",
                "A plant has a free-living, photosynthetic gametophyte that bears antheridia and archegonia. Its "
                "sporophyte remains attached to the gametophyte and is differentiated into a foot, seta and capsule. "
                "Which of the following statements about this plant are correct?",
                [("Its antherozoids are biflagellate.", True),
                 ("It needs water for fertilisation.", True),
                 ("Its spores are formed within the capsule after meiosis.", True),
                 ("Its sporophyte has xylem and phloem.", False),
                 ("Its zygote undergoes meiosis immediately to form spores.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "B",
                "Applying the features of bryophytes",
                "A dominant free-living gametophyte bearing antheridia and archegonia, with a dependent sporophyte of "
                "foot, seta and capsule, describes a bryophyte. Its antheridia produce biflagellate antherozoids, which "
                "are released into water and reach the archegonium, so water is needed for fertilisation. The zygote "
                "does not undergo reduction division immediately; it forms a multicellular sporophyte, and spores are "
                "produced within the capsule after meiosis. Bryophytes lack vascular tissue, which first appears in "
                "pteridophytes.",
                ["Identify: bryophyte", "(a), (b), (c) true", "(d) false: no vascular tissue",
                 "(e) false: the zygote forms the sporophyte first"],
                why="Any option containing (d) or (e) includes a false statement; (a), (b) and (c) are all true, so a "
                    "combination missing one of them is incomplete.",
                ncert=ref("PK", "Bryophytes"), secs=60)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following features are shared by members of Chlorophyceae and Rhodophyceae, according to "
                "NCERT's table of the divisions of algae?",
                [("Chlorophyll a is present.", True),
                 ("Cellulose is a component of the cell wall.", True),
                 ("Motile cells bear 2–8 equal, apical flagella.", False),
                 ("Food is stored as mannitol.", False),
                 ("Phycoerythrin is the major pigment.", False)],
                [("a", "c"), ("a", "b", "e"), ("b", "d")], "C",
                "Comparing green and red algae",
                "Chlorophyceae: chlorophyll a and b; stored food starch; cell wall cellulose; 2–8 equal, apical flagella. "
                "Rhodophyceae: chlorophyll a and d with phycoerythrin; stored food floridean starch; cell wall of "
                "cellulose, pectin and polysulphate esters; flagella absent. So both have chlorophyll a and cellulose "
                "in the cell wall. Mannitol is stored by brown algae.",
                ["(a) both: true", "(b) both have cellulose in the wall: true",
                 "(c) red algae lack flagella", "(d) mannitol = brown algae", "(e) phycoerythrin only in red algae"],
                why="(c), (e) apply only to one of the two classes and (d) to neither.",
                ncert=ref("PK", "Algae (Table 3.1)"), secs=60)

direct(T_PK, "Pteridophytes", "Advanced",
       "A plant has true roots, stem and leaves with vascular tissue but forms no seeds. Its sporophylls are "
       "compactly arranged in strobili, it produces two kinds of spores, and its female gametophyte is retained on "
       "the parent sporophyte for a variable period. Among the following, the plant is:",
       "Selaginella",
       ["Equisetum", "Pinus", "Dryopteris"], "A",
       "Identifying a heterosporous pteridophyte with strobili",
       "Vascular tissue without seeds indicates a pteridophyte. NCERT names Selaginella and Equisetum as pteridophytes "
       "whose sporophylls form compact strobili, and Selaginella and Salvinia as heterosporous genera whose female "
       "gametophytes are retained on the parent sporophyte. Only Selaginella has all these features.",
       ["Vascular, no seeds → pteridophyte", "Strobili: Selaginella, Equisetum",
        "Heterosporous: Selaginella, Salvinia", "Common to both → Selaginella"],
       why="Equisetum has strobili but is not one of the heterosporous genera named. Pinus is a gymnosperm and forms "
           "seeds. Dryopteris is a fern and is neither named as forming strobili nor as heterosporous.",
       ncert=ref("PK", "Pteridophytes"), secs=60)

statement_pair(T_PK, "Gymnosperms", "Advanced",
               "In gymnosperms, the female gametophyte that bears the archegonia develops from one of the four "
               "megaspores formed by meiosis of the megaspore mother cell.",
               "In gymnosperms, the pollen grains develop within the megasporangia.",
               True, False, "C",
               "Development of gametophytes in gymnosperms",
               "The megaspore mother cell, differentiated from a cell of the nucellus, divides meiotically to form four "
               "megaspores. One of them, enclosed within the megasporangium, develops into a multicellular female "
               "gametophyte that bears two or more archegonia. The microspores develop into the highly reduced male "
               "gametophyte, the pollen grain, and the development of pollen grains takes place within the "
               "microsporangia, not the megasporangia.",
               ["Statement I: true", "Statement II: false; pollen grains develop in microsporangia"],
               ncert=ref("PK", "Gymnosperms"), secs=45)

_BROWN = {"Ectocarpus": True, "Dictyota": True, "Porphyra": False, "Laminaria": True, "Polysiphonia": False,
          "Sargassum": True, "Fucus": True, "Gelidium": False, "Chara": False}
numerical(T_PK, "Algae", "Advanced",
          "How many of the following algae are members of Phaeophyceae?\n"
          "Ectocarpus, Dictyota, Porphyra, Laminaria, Polysiphonia, Sargassum, Fucus, Gelidium, Chara",
          "5", ["4", "6", "3"], "B", sum(_BROWN.values()) == 5,
          "Common members of the classes of algae",
          "NCERT names Ectocarpus, Dictyota, Laminaria, Sargassum and Fucus as common brown algae (Phaeophyceae). "
          "Porphyra, Polysiphonia and Gelidium are red algae (Rhodophyceae), and Chara is a green alga "
          "(Chlorophyceae).",
          ["Brown: Ectocarpus, Dictyota, Laminaria, Sargassum, Fucus = 5",
           "Red: Porphyra, Polysiphonia, Gelidium; green: Chara"],
          why="4 leaves out one brown alga (often Dictyota); 6 counts a red alga such as Porphyra or Gelidium as brown; "
              "3 counts only the kelps and Fucus.",
          ncert=ref("PK", "Algae (Phaeophyceae, Rhodophyceae, Chlorophyceae)"), secs=50)


# =============================================================== 3. Morphology of Flowering Plants (5/6/5)
direct(T_MOR, "Flower", "Basic",
       "In twisted aestivation, one margin of each petal overlaps that of the next one. Which of the following plants "
       "shows twisted aestivation?",
       "Lady's finger",
       ["Calotropis", "Pea", "Gulmohur"], "A",
       "Types of aestivation",
       "If one margin of an appendage overlaps that of the next one and so on, the aestivation is twisted, as in "
       "china rose, lady's finger and cotton. Calotropis shows valvate aestivation, Cassia and gulmohur imbricate, and "
       "pea and bean vexillary aestivation.",
       ["Twisted: china rose, lady's finger, cotton"],
       why="Calotropis is valvate, pea is vexillary and gulmohur is imbricate.",
       ncert=ref("MOR", "The Flower (aestivation)"), secs=20)

direct(T_MOR, "Flower", "Basic",
       "Each ovary bears one or more ovules attached to a flattened, cushion-like:",
       "placenta",
       ["thalamus", "style", "stigma"], "B",
       "Parts of the gynoecium",
       "Each carpel consists of three parts: stigma, style and ovary. The ovary is the enlarged basal part, on which "
       "lies the elongated style connecting the ovary to the stigma. Each ovary bears one or more ovules attached to "
       "a flattened, cushion-like placenta.",
       ["Ovules are attached to the placenta inside the ovary"],
       why="The thalamus is the swollen end of the pedicel bearing the floral whorls; the style connects the ovary to "
           "the stigma; the stigma receives pollen.",
       ncert=ref("MOR", "The Flower (gynoecium)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In the alternate type of phyllotaxy:",
       "a single leaf arises at each node in an alternate manner",
       ["a pair of leaves arises at each node, opposite each other",
        "more than two leaves arise at a node and form a whorl",
        "all the leaves arise from the base of the stem"], "D",
       "Phyllotaxy",
       "Phyllotaxy is the pattern of arrangement of leaves on the stem or branch, usually of three types: alternate, "
       "opposite and whorled. In the alternate type, a single leaf arises at each node in an alternate manner, as in "
       "china rose, mustard and sunflower. In the opposite type, a pair of leaves arises at each node opposite each "
       "other (Calotropis, guava). If more than two leaves arise at a node and form a whorl, it is whorled (Alstonia).",
       ["Alternate: one leaf per node", "Opposite: two per node", "Whorled: more than two per node"],
       why="The other options describe opposite and whorled phyllotaxy, or a basal arrangement that is not a type of "
           "phyllotaxy named by NCERT.",
       ncert=ref("MOR", "The Leaf (phyllotaxy)"), secs=20)

statement_pair(T_MOR, "Root, stem and leaf", "Basic",
               "A leaf develops at the node and bears a bud in its axil.",
               "The buds borne by a stem may be terminal or axillary.",
               True, True, "A",
               "Nodes, buds and leaves",
               "The stem bears nodes and internodes; the region where leaves are born is the node. The stem bears "
               "buds, which may be terminal or axillary. A leaf is a lateral, generally flattened structure borne on the "
               "stem; it develops at the node and bears a bud in its axil, which later develops into a branch.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Stem; The Leaf"), secs=25)

match_list(T_MOR, "Root, stem and leaf", "Basic", "plant", "root modification",
           ["Banyan", "Sugarcane", "Rhizophora", "Sweet potato"],
           ["Swollen adventitious roots that store food", "Stilt roots arising from the lower nodes of the stem",
            "Hanging prop roots from the branches", "Roots that grow vertically upwards to get oxygen for respiration"],
           "III II IV I", ["II III IV I", "III II I IV", "IV II III I"], "D",
           "Modifications of roots",
           "In the banyan tree, hanging structures from the branches (prop roots) support the tree. The supporting roots "
           "coming out of the lower nodes of the stem in maize and sugarcane are stilt roots. In Rhizophora growing in "
           "swampy areas, many roots come out of the ground and grow vertically upwards (pneumatophores) to get oxygen "
           "for respiration. Sweet potato stores food in swollen adventitious roots.",
           ["Banyan → prop roots; sugarcane → stilt roots", "Rhizophora → pneumatophores; sweet potato → storage"],
           why="The wrong codes swap the prop and stilt roots, the respiratory and storage roots, or the banyan and "
               "Rhizophora roots.",
           ncert=ref("MOR", "The Root (modifications of root)"), secs=35)

assertion_reason(T_MOR, "Plant families", "Intermediate",
                 "The seeds of members of the family Solanaceae are endospermous.",
                 "In members of the family Solanaceae, the calyx is persistent.",
                 True, True, False, "B",
                 "Features of Solanaceae",
                 "In the family Solanaceae the seeds are many and endospermous. Separately, the calyx has five united "
                 "sepals, is persistent and shows valvate aestivation. Whether the calyx persists has no bearing on "
                 "whether the seed keeps an endosperm.",
                 ["A: true", "R: true", "The calyx and the seed are unrelated features"],
                 ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=35)

assertion_reason(T_MOR, "Flower", "Intermediate",
                 "In a perigynous flower such as rose, the ovary is inferior.",
                 "In a perigynous flower, the gynoecium is situated in the centre and the other parts of the flower are "
                 "located on the rim of the thalamus almost at the same level.",
                 False, True, False, "D",
                 "Position of the ovary",
                 "If the gynoecium is situated in the centre and the other parts of the flower are located on the rim of "
                 "the thalamus almost at the same level, the flower is perigynous; the ovary here is said to be half "
                 "inferior (plum, rose, peach). An inferior ovary is found in epigynous flowers such as guava and "
                 "cucumber.",
                 ["A: false; the ovary of a perigynous flower is half inferior", "R: true"],
                 ncert=ref("MOR", "The Flower (position of floral parts on the thalamus)"), secs=40)

direct(T_MOR, "Plant families", "Intermediate",
       "Which pair of plants both bear zygomorphic flowers with a monocarpellary ovary?",
       "Pea and bean",
       ["Mustard and datura", "Canna and pea", "Chilli and bean"], "A",
       "Symmetry and gynoecium of Fabaceae",
       "Pea and bean belong to Fabaceae, whose flowers are bisexual and zygomorphic, with a superior, monocarpellary, "
       "unilocular ovary. NCERT names pea, gulmohur, bean and Cassia as having zygomorphic flowers. Mustard, datura "
       "and chilli have actinomorphic flowers, and canna has an asymmetric flower.",
       ["Zygomorphic: pea, bean, gulmohur, Cassia", "Fabaceae: monocarpellary ovary"],
       why="Mustard, datura and chilli are actinomorphic; canna is asymmetric (irregular).",
       ncert=ref("MOR", "The Flower (symmetry); Fabaceae"), secs=40)

multi_statement(T_MOR, "Plant families", "Intermediate",
                "In which of the following plants are the stamens epipetalous, that is, attached to the petals?",
                [("Brinjal", True), ("Tomato", True), ("Petunia", True), ("Pea", False), ("Lily", False)],
                [("a", "b", "e"), ("a", "d"), ("b", "c", "d", "e")], "C",
                "Epipetalous stamens",
                "Stamens attached to the petals are epipetalous, as in brinjal. In the family Solanaceae (brinjal, "
                "tomato, petunia, potato), the androecium has five epipetalous stamens. In pea (Fabaceae) the ten "
                "stamens are diadelphous, not attached to the petals, and in lily the stamens are attached to the "
                "perianth (epiphyllous).",
                ["Solanaceae → epipetalous: brinjal, tomato, Petunia", "Pea: diadelphous", "Lily: epiphyllous"],
                why="Pea and lily do not have epipetalous stamens, so options with (d) or (e) are wrong; (a) and (d) "
                    "alone also leave out tomato and Petunia.",
                ncert=ref("MOR", "The Flower (androecium); Solanaceae"), secs=45)

match_list(T_MOR, "Flower", "Intermediate", "term", "meaning",
           ["Apocarpous", "Syncarpous", "Epipetalous", "Polyadelphous"],
           ["Stamens attached to the petals", "Carpels fused", "Stamens united into more than two bundles",
            "Carpels free"],
           "IV II I III", ["II IV I III", "IV II III I", "II IV III I"], "B",
           "Terms for the androecium and gynoecium",
           "When more than one carpel is present, they may be free (apocarpous, as in lotus and rose) or fused "
           "(syncarpous, as in mustard and tomato). Stamens attached to the petals are epipetalous (brinjal). Stamens "
           "united into more than two bundles are polyadelphous (citrus).",
           ["Apocarpous = free carpels; syncarpous = fused carpels",
            "Epipetalous = on petals; polyadelphous = more than two bundles"],
           why="The wrong codes swap free and fused carpels, or the epipetalous and polyadelphous conditions.",
           ncert=ref("MOR", "The Flower (androecium, gynoecium)"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "In the semi-technical description of a flowering plant, the description is given in which sequence?",
       "Habit → vegetative characters (roots, stem, leaves) → floral characters (inflorescence, flower parts)",
       ["Floral characters → vegetative characters → habit",
        "Inflorescence → habit → roots, stem and leaves → flower parts",
        "Vegetative characters → habit → floral characters"], "C",
       "Semi-technical description of a plant",
       "A flowering plant is described in simple, scientific language and in a proper sequence. The description begins "
       "with the habit and the vegetative characters (roots, stem and leaves), and then the floral characters "
       "(inflorescence and flower parts). The floral diagram and floral formula are presented after this.",
       ["Habit first", "Then roots, stem, leaves", "Then inflorescence and flower"],
       why="Each wrong sequence moves the habit or the floral characters out of their NCERT position.",
       ncert=ref("MOR", "Semi-technical Description of a Typical Flowering Plant"), secs=30)

multi_statement(T_MOR, "Plant families", "Advanced",
                "A flower has the floral formula ⊕ ⚥ K(5) C(5) A5 G(2), with the stamens joined to the corolla "
                "(epipetalous) and the ovary superior. Which of the following conclusions about it are correct?",
                [("The calyx is gamosepalous.", True),
                 ("The corolla is gamopetalous.", True),
                 ("The stamens are not united with one another, though they are attached to the petals.", True),
                 ("The flower is zygomorphic.", False),
                 ("The gynoecium is bicarpellary and apocarpous.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "D",
                "Reading a floral formula",
                "In a floral formula, ⊕ shows an actinomorphic flower and ⚥ a bisexual one. Fusion is shown by "
                "enclosing the figure in brackets, and adhesion by a line drawn above the symbols of the floral parts. "
                "K(5) means five united sepals and C(5) five united petals. A5 has no bracket, so the five stamens are "
                "free from one another; the line joining C and A shows they are attached to the petals. G(2) means two "
                "fused carpels (syncarpous). This is the floral formula of Solanaceae.",
                ["(a) K(5): true", "(b) C(5): true", "(c) A5 + line to C: true", "(d) ⊕ = actinomorphic: false",
                 "(e) G(2) = syncarpous: false"],
                why="Options with (d) or (e) include a false conclusion; (a) and (c) alone leave out (b).",
                ncert=ref("MOR", "Semi-technical Description (floral formula); Solanaceae"), secs=75)

assertion_reason(T_MOR, "Fruit and seed", "Advanced",
                 "In a mango fruit, the seed lies enclosed within a hard, stony layer.",
                 "Mango is a drupe, a fruit in which the endocarp is stony and hard.",
                 True, True, True, "A",
                 "Pericarp of a drupe",
                 "When the pericarp is thick and fleshy, it is differentiated into the outer epicarp, the middle "
                 "mesocarp and the inner endocarp. In mango, a drupe developing from a monocarpellary superior ovary and "
                 "one-seeded, the pericarp is differentiated into a thin epicarp, a fleshy edible mesocarp and an inner "
                 "stony, hard endocarp. The hard layer around the seed is this endocarp, so R explains A.",
                 ["A: true", "R: true; the stony layer enclosing the seed is the endocarp"],
                 ncert=ref("MOR", "The Fruit"), secs=45)

statement_pair(T_MOR, "Root, stem and leaf", "Advanced",
               "The tendrils of both cucumber and pea help the plant to climb.",
               "The tendrils of both cucumber and pea develop from axillary buds.",
               True, False, "C",
               "Stem tendrils and leaf tendrils",
               "Tendrils that develop from axillary buds are stem tendrils; they are slender and spirally coiled and "
               "help plants to climb, as in gourds (cucumber, pumpkins, watermelon) and grapevines. In pea, leaves are "
               "modified into tendrils for climbing. So both help in climbing, but only the cucumber tendril develops "
               "from an axillary bud.",
               ["Statement I: true", "Statement II: false; the pea tendril is a modified leaf"],
               ncert=ref("MOR", "The Stem (modifications); The Leaf (modifications)"), secs=45)

multi_statement(T_MOR, "Fruit and seed", "Advanced",
                "Which of the following statements correctly compare the seed of bean with the grain of maize?",
                [("Both have cotyledons in the embryo: two in bean and one (the scutellum) in maize.", True),
                 ("The mature bean seed lacks an endosperm, whereas in maize the endosperm is bulky and stores food.",
                  True),
                 ("In both, the seed coat is fused with the fruit wall.", False),
                 ("In both, the plumule is enclosed in a sheath called the coleoptile.", False),
                 ("In both, an aleurone layer separates the endosperm from the embryo.", False)],
                [("a", "b", "c"), ("b", "d"), ("a", "e")], "B",
                "Dicotyledonous and monocotyledonous seeds compared",
                "The embryo of a dicot seed such as bean has an embryonal axis and two cotyledons; bean, gram and pea "
                "seeds have no endosperm at maturity (non-endospermous). In a maize grain, the seed coat is membranous "
                "and fused with the fruit wall; the endosperm is bulky and is separated from the embryo by the "
                "proteinaceous aleurone layer; the embryo has one large, shield-shaped cotyledon, the scutellum, and "
                "its plumule and radicle are enclosed in the coleoptile and coleorhiza.",
                ["(a) true", "(b) true", "(c), (d), (e) are features of maize only"],
                why="Statements (c), (d) and (e) describe cereal (maize) features that the bean seed does not have.",
                ncert=ref("MOR", "The Seed (dicotyledonous and monocotyledonous seeds)"), secs=70)

direct(T_MOR, "Plant families", "Advanced",
       "Which of the following features is common to the flowers of the families Fabaceae, Solanaceae and "
       "Liliaceae?",
       "Bisexual flowers with a superior ovary",
       ["Actinomorphic flowers with axile placentation", "Endospermous seeds",
        "A gamosepalous calyx with valvate aestivation"], "A",
       "Comparing three families",
       "In all three families the flowers are bisexual and the ovary is superior. Fabaceae flowers are zygomorphic "
       "with a monocarpellary, unilocular ovary and non-endospermous seeds, and the calyx shows imbricate "
       "aestivation. Solanaceae and Liliaceae flowers are actinomorphic with axile placentation and endospermous "
       "seeds. Liliaceae has a perianth of tepals rather than a separate calyx.",
       ["Fabaceae, Solanaceae, Liliaceae: all bisexual, ovary superior",
        "Fabaceae differs: zygomorphic, non-endospermous, imbricate calyx"],
       why="Fabaceae is zygomorphic and monocarpellary (no axile placentation), has non-endospermous seeds and an "
           "imbricate calyx; Liliaceae has no distinct calyx.",
       ncert=ref("MOR", "Description of Some Important Families"), secs=60)


# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
statement_pair(T_ANA, "Dicot and monocot anatomy", "Basic",
               "In a dorsiventral leaf, the epidermis that covers both the upper (adaxial) and the lower (abaxial) "
               "surface has a conspicuous cuticle.",
               "In a dorsiventral leaf, it is the abaxial epidermis that may even lack stomata.",
               True, False, "C",
               "Epidermis of a dorsiventral leaf",
               "The epidermis covers both the upper surface (adaxial epidermis) and the lower surface (abaxial "
               "epidermis) of a dorsiventral leaf and has a conspicuous cuticle. The abaxial epidermis generally bears "
               "more stomata than the adaxial epidermis; the adaxial (upper) epidermis may even lack stomata.",
               ["Statement I: true", "Statement II: false; the adaxial epidermis may lack stomata"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dorsiventral leaf)"), secs=35)

direct(T_ANA, "Plant tissues", "Basic",
       "The cells of parenchyma are generally:",
       "isodiametric, with thin walls made of cellulose",
       ["much elongated, with pointed, needle-like apices", "thickened at the corners by cellulose, hemicellulose "
        "and pectin", "dead, with thick and lignified walls"], "D",
       "Parenchyma",
       "Parenchyma forms the major component within organs. Its cells are generally isodiametric; they may be "
       "spherical, oval, round, polygonal or elongated in shape. Their walls are thin and made of cellulose. They may "
       "be closely packed or have small intercellular spaces.",
       ["Parenchyma: isodiametric, thin cellulose walls"],
       why="Needle-like apices describe phloem fibres; corner thickenings describe collenchyma; dead lignified cells "
           "describe sclerenchyma.",
       ncert=ref("ANA", "The Tissues (simple tissues: parenchyma)"), secs=20)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "In a dorsiventral leaf, the vascular bundles of the vascular system can be seen in the:",
       "veins and the midrib",
       ["palisade parenchyma only", "abaxial epidermis", "bulliform cells"], "B",
       "Vascular system of the leaf",
       "A vertical section of a dorsiventral leaf shows three main parts: epidermis, mesophyll and vascular system. "
       "The vascular system includes vascular bundles, which can be seen in the veins and the midrib. The size of the "
       "vascular bundles depends on the size of the veins.",
       ["Leaf: epidermis, mesophyll, vascular system", "Vascular bundles lie in the veins and midrib"],
       why="The palisade parenchyma is part of the mesophyll; the epidermis is the covering layer; bulliform cells are "
           "modified epidermal cells of grass leaves.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dorsiventral leaf)"), secs=20)

match_list(T_ANA, "Plant tissues", "Basic", "cell", "shape described in NCERT",
           ["Guard cells of a dicot", "Guard cells of a grass", "Sclereids", "Phloem fibres"],
           ["Dumb-bell shaped", "Much elongated and unbranched, with pointed, needle-like apices", "Bean-shaped",
            "Spherical, oval or cylindrical"],
           "III I IV II", ["I III IV II", "III I II IV", "IV I III II"], "A",
           "Shapes of some plant cells",
           "Each stoma has two bean-shaped guard cells; in grasses the guard cells are dumb-bell shaped. Sclereids are "
           "spherical, oval or cylindrical, highly thickened dead cells with very narrow lumen. Phloem fibres are much "
           "elongated, unbranched and have pointed, needle-like apices.",
           ["Dicot guard cell → bean; grass guard cell → dumb-bell", "Sclereid → spherical/oval/cylindrical; "
            "phloem fibre → needle-like"],
           why="The wrong codes interchange the two kinds of guard cells, or the sclereids and fibres.",
           ncert=ref("ANA", "The Tissues; The Tissue System (epidermal tissue system)"), secs=35)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Collenchyma cells may assimilate food.",
                 "In dicotyledonous plants, collenchyma is found below the epidermis either as a homogeneous layer or "
                 "in patches.",
                 True, True, False, "B",
                 "Collenchyma",
                 "Collenchyma cells often contain chloroplasts, and they assimilate food when they contain chloroplasts. "
                 "Separately, collenchyma occurs in layers below the epidermis in dicotyledonous plants, either as a "
                 "homogeneous layer or in patches. Its position does not explain its ability to assimilate food; the "
                 "chloroplasts do.",
                 ["A: true (when chloroplasts are present)", "R: true, but about position, not the cause of A"],
                 ncert=ref("ANA", "The Tissues (collenchyma)"), secs=40)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "The functions of a mature sieve tube element are controlled by the nucleus of a companion cell.",
                 "A mature sieve element possesses a peripheral cytoplasm and a large vacuole but lacks a nucleus.",
                 True, True, True, "A",
                 "Sieve tube elements and companion cells",
                 "Sieve tube elements are long tube-like structures associated with companion cells. A mature sieve "
                 "element possesses a peripheral cytoplasm and a large vacuole but lacks a nucleus. Because it has no "
                 "nucleus of its own, its functions are controlled by the nucleus of the companion cell, which is "
                 "connected to it by pit fields in their common longitudinal walls.",
                 ["A: true", "R: true; having no nucleus is why its functions depend on the companion cell"],
                 ncert=ref("ANA", "The Tissues (phloem)"), secs=40)

direct(T_ANA, "Plant tissues", "Intermediate",
       "In flowering plants, tracheids and vessels are the main water-transporting elements. In the xylem of "
       "gymnosperms, water is conducted mainly by:",
       "tracheids, as vessels are absent",
       ["vessels, as tracheids are absent", "xylem fibres", "albuminous cells"], "C",
       "Xylem of gymnosperms",
       "Xylem is composed of tracheids, vessels, xylem fibres and xylem parenchyma. In flowering plants, tracheids and "
       "vessels are the main water-transporting elements. Vessels are a characteristic feature of angiosperms; "
       "gymnosperms lack vessels in their xylem, so the tracheids conduct water.",
       ["Angiosperms: tracheids + vessels", "Gymnosperms: no vessels → tracheids"],
       why="Gymnosperms lack vessels, not tracheids. Xylem fibres are supporting cells. Albuminous cells are found in "
           "the phloem of gymnosperms.",
       ncert=ref("ANA", "The Tissues (xylem)"), secs=35)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "Which of the following features are common to the dicot root and the monocot root?",
                [("The vascular bundles are radial.", True),
                 ("A pericycle is present.", True),
                 ("There are usually more than six xylem bundles.", False),
                 ("The pith is large and well developed.", False),
                 ("The primary xylem is exarch.", True)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "e")], "D",
                "Dicot and monocot roots compared",
                "The anatomy of the monocot root is similar to that of the dicot root in many respects: it has "
                "epidermis, cortex, endodermis, pericycle, vascular bundles and pith. In roots the vascular bundles are "
                "radial and the primary xylem is exarch. They differ in that the monocot root usually has more than six "
                "xylem bundles (polyarch) and a large, well-developed pith, whereas the dicot root has two to four xylem "
                "patches and a small or inconspicuous pith.",
                ["(a), (b), (e): common", "(c), (d): monocot root only"],
                why="(c) and (d) apply only to the monocot root; (a) and (e) alone leave out the pericycle.",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (roots)"), secs=55)

match_list(T_ANA, "Dicot and monocot anatomy", "Intermediate", "feature seen in a section", "organ",
           ["Collenchymatous hypodermis", "Sclerenchymatous hypodermis", "Bulliform cells along the veins",
            "Usually more than six xylem bundles"],
           ["Monocot root", "Dicot stem", "Monocot stem", "Grass leaf"],
           "II III IV I", ["III II IV I", "II III I IV", "IV III II I"], "B",
           "Identifying organs from their anatomy",
           "In the dicot stem, the hypodermis consists of a few layers of collenchymatous cells; the monocot stem has a "
           "sclerenchymatous hypodermis. In grasses, certain adaxial epidermal cells along the veins are modified into "
           "large, empty, colourless bulliform cells. The monocot root usually has more than six xylem bundles "
           "(polyarch).",
           ["Collenchymatous hypodermis → dicot stem", "Sclerenchymatous hypodermis → monocot stem",
            "Bulliform cells → grass leaf", "Polyarch → monocot root"],
           why="The wrong codes swap the two kinds of hypodermis, or the grass leaf and the monocot root.",
           ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=40)

_VASC = {"phloem fibres": True, "xylem parenchyma": True, "pericycle": False, "companion cells": True,
         "medullary rays": False, "tracheids": True, "endodermis": False, "bulliform cells": False}
numerical(T_ANA, "Tissue systems", "Advanced",
          "How many of the following belong to the vascular (conducting) tissue system?\n"
          "phloem fibres, xylem parenchyma, pericycle, companion cells, medullary rays, tracheids, endodermis, "
          "bulliform cells",
          "4", ["3", "5", "6"], "A", sum(_VASC.values()) == 4,
          "The three tissue systems",
          "The vascular system consists of the complex tissues xylem (tracheids, vessels, xylem fibres, xylem "
          "parenchyma) and phloem (sieve tube elements, companion cells, phloem parenchyma, phloem fibres). All tissues "
          "except the epidermis and vascular bundles form the ground tissue: cortex, endodermis, pericycle, pith and "
          "medullary rays. Bulliform cells are modified epidermal cells.",
          ["Vascular: phloem fibres, xylem parenchyma, companion cells, tracheids = 4",
           "Ground: pericycle, medullary rays, endodermis", "Epidermal: bulliform cells"],
          why="3 leaves out a parenchyma or fibre component of xylem or phloem; 5 or 6 count the pericycle, medullary "
              "rays or endodermis, which are ground tissue even though they lie close to the vascular bundles.",
          ncert=ref("ANA", "The Tissue System"), secs=50)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "A leaf section shows stomata on both surfaces, a mesophyll not differentiated into palisade and spongy "
                "parenchyma, vascular bundles of nearly similar size except in the main veins, and large, empty, "
                "colourless cells in the adaxial epidermis along the veins. Which of the following conclusions are "
                "correct?",
                [("The leaf is an isobilateral leaf of a grass.", True),
                 ("When these large epidermal cells lose water and become flaccid, the leaf curls inwards.", True),
                 ("The near-similar size of the vascular bundles reflects the parallel venation of the leaf.", True),
                 ("The guard cells of its stomata are bean-shaped.", False),
                 ("Its palisade parenchyma lies adaxially.", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c")], "D",
                "Interpreting a section of an isobilateral leaf",
                "Stomata on both surfaces and an undifferentiated mesophyll mark an isobilateral (monocot) leaf. The "
                "large, empty, colourless adaxial cells along the veins are bulliform cells of grasses; when they are "
                "flaccid due to water stress, the leaf curls inwards to minimise water loss. The parallel venation of "
                "monocot leaves is reflected in the near-similar sizes of the vascular bundles (except in the main "
                "veins). In grasses the guard cells are dumb-bell shaped, and an isobilateral leaf has no palisade "
                "layer.",
                ["(a), (b), (c) true", "(d) false: dumb-bell shaped in grasses", "(e) false: mesophyll undifferentiated"],
                why="(d) and (e) are false; (b) and (c) alone leave out (a).",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (isobilateral leaf)"), secs=70)

assertion_reason(T_ANA, "Plant tissues", "Advanced",
                 "Phloem fibres lose their protoplasm and become dead at maturity.",
                 "Phloem fibres are present in the primary phloem but are absent in the secondary phloem.",
                 True, False, False, "C",
                 "Phloem fibres",
                 "Phloem fibres (bast fibres) are made up of sclerenchymatous cells. At maturity these fibres lose their "
                 "protoplasm and become dead. They are generally absent in the primary phloem but are found in the "
                 "secondary phloem, so R states the reverse of the NCERT position.",
                 ["A: true", "R: false; they are absent in primary and present in secondary phloem"],
                 ncert=ref("ANA", "The Tissues (phloem fibres)"), secs=40)

direct(T_ANA, "Dicot and monocot anatomy", "Advanced",
       "A stem section shows conjoint vascular bundles with no cambium between the xylem and the phloem, phloem "
       "parenchyma absent from the bundles, and water-containing cavities within the bundles. The stem is most "
       "likely that of:",
       "a monocotyledon",
       ["a dicotyledon", "a gymnosperm", "a dicotyledon, as the bundles are open"], "B",
       "Identifying a monocot stem",
       "Conjoint bundles without cambium are closed, as in monocot stems and leaves. In the monocot stem, phloem "
       "parenchyma is absent and water-containing cavities are present within the vascular bundles. Dicot stem "
       "bundles are conjoint and open, with cambium between phloem and xylem.",
       ["No cambium → closed bundles", "No phloem parenchyma + water cavities → monocot stem"],
       why="Dicot stems have open bundles with cambium. Bundles without cambium are closed, not open. Gymnosperms are "
           "not described with closed bundles having water-containing cavities.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (monocot stem)"), secs=45)


# =============================================================== 5. Cell: The Unit of Life (5/6/5)
direct(T_CELL, "Nucleus", "Basic",
       "In an interphase nucleus, the nucleoprotein fibres form a loose and indistinct network called chromatin. "
       "During the different stages of cell division, cells instead show:",
       "structured chromosomes in place of the nucleus",
       ["a larger number of nucleoli", "a nuclear envelope with more pores", "chromatin fibres fused with the "
        "endoplasmic reticulum"], "C",
       "Chromatin and chromosomes",
       "The interphase nucleus (a nucleus of a cell when it is not dividing) has highly extended and elaborate "
       "nucleoprotein fibres called chromatin, nuclear matrix and one or more spherical nucleoli. During different "
       "stages of cell division, cells show structured chromosomes in place of the nucleus.",
       ["Interphase: chromatin network", "Division: structured chromosomes in place of the nucleus"],
       why="The other options are not what NCERT describes for dividing cells; the nucleus is replaced by condensed, "
           "structured chromosomes.",
       ncert=ref("CELL", "Nucleus"), secs=25)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In chloroplasts, the light energy essential for photosynthesis is trapped by:",
       "chlorophyll and carotenoid pigments",
       ["the 70S ribosomes of the stroma", "the circular DNA of the stroma",
        "the enzymes of the outer membrane"], "D",
       "Pigments of chloroplasts",
       "Chloroplasts contain chlorophyll and carotenoid pigments, which are responsible for trapping light energy "
       "essential for photosynthesis. The stroma contains enzymes for the synthesis of carbohydrates and proteins, "
       "small double-stranded circular DNA and 70S ribosomes; chlorophyll pigments are present in the thylakoids.",
       ["Light trapping = chlorophyll + carotenoids"],
       why="Ribosomes, DNA and membrane enzymes do not absorb light; they serve protein synthesis, heredity and "
           "metabolism.",
       ncert=ref("CELL", "Plastids"), secs=20)

direct(T_CELL, "Cell theory", "Basic",
       "Cells vary greatly in shape; they may be disc-like, polygonal, columnar, cuboid, thread-like or even "
       "irregular. According to NCERT, the shape of a cell may vary with:",
       "the function it performs",
       ["the number of nuclei it contains", "the type of ribosomes it has", "the age of the organism"], "A",
       "Shapes of cells",
       "Cells differ greatly in size, shape and activities. They may be disc-like, polygonal, columnar, cuboid, thread "
       "like, or even irregular, and NCERT notes that the shape of the cell may vary with the function it performs. "
       "For example, nerve cells are branched and long, and red blood cells are round and biconcave.",
       ["Shape varies with function"],
       why="NCERT links cell shape to function, not to the number of nuclei, the ribosome type or the organism's age.",
       ncert=ref("CELL", "An Overview of Cell"), secs=20)

match_list(T_CELL, "Cell theory", "Basic", "scientist", "year of the work as given in NCERT",
           ["Matthias Schleiden", "Theodore Schwann", "Rudolf Virchow", "Singer and Nicolson"],
           ["1855", "1972", "1838", "1839"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B",
           "Dates in the history of the cell",
           "In 1838 Matthias Schleiden, a German botanist, observed that all plants are composed of different kinds of "
           "cells. In 1839 Theodore Schwann, a British zoologist, reported the thin outer layer of animal cells. Rudolf "
           "Virchow (1855) explained that cells divide and new cells are formed from pre-existing cells. Singer and "
           "Nicolson (1972) proposed the fluid mosaic model of the cell membrane.",
           ["Schleiden 1838 → Schwann 1839", "Virchow 1855 → Singer and Nicolson 1972"],
           why="The wrong codes swap Schleiden and Schwann, or Virchow and Singer–Nicolson, or put Virchow first.",
           ncert=ref("CELL", "Cell Theory; Cell Membrane"), secs=35)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Basic",
               "The two centrioles of a centrosome lie perpendicular to each other, and each has an organisation like "
               "a cartwheel.",
               "The centrioles of a centrosome are surrounded by amorphous pericentriolar materials.",
               True, True, "A",
               "Centrosome and centrioles",
               "The centrosome is an organelle usually containing two cylindrical structures called centrioles. They "
               "are surrounded by amorphous pericentriolar materials. Both centrioles in a centrosome lie "
               "perpendicular to each other, and each has an organisation like a cartwheel.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Centrosome and Centrioles"), secs=30)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "Plasmids can confer resistance to antibiotics on some bacteria.",
                 "Pili are elongated tubular structures made of a special protein.",
                 True, True, False, "B",
                 "Plasmids and pili",
                 "Plasmids are small circular DNA outside the genomic DNA; they confer certain unique phenotypic "
                 "characters on bacteria, one of which is resistance to antibiotics. Pili are elongated tubular "
                 "structures made of a special protein, a surface structure of the cell. The composition of pili has "
                 "nothing to do with how plasmids confer antibiotic resistance.",
                 ["A: true", "R: true", "R describes a different structure"],
                 ncert=ref("CELL", "Prokaryotic Cells"), secs=35)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "In a prokaryotic cell, several protein molecules can be made from a single mRNA at the same time.",
                 "Several ribosomes may attach to a single mRNA to form a polysome, and the ribosomes of a polysome "
                 "translate the mRNA into proteins.",
                 True, True, True, "A",
                 "Polysomes",
                 "In prokaryotes, ribosomes are associated with the plasma membrane. Several ribosomes may attach to a "
                 "single mRNA and form a chain called a polyribosome or polysome, and the ribosomes of a polysome "
                 "translate the mRNA into proteins. Because each attached ribosome translates the same mRNA, several "
                 "protein molecules are made from it at once.",
                 ["A: true", "R: true; many ribosomes on one mRNA → many proteins at once"],
                 ncert=ref("CELL", "Prokaryotic Cells (ribosomes and inclusion bodies)"), secs=40)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                "In which of the following does NCERT describe the presence of DNA?",
                [("The matrix of a mitochondrion", True),
                 ("The stroma of a chloroplast", True),
                 ("The Golgi apparatus", False),
                 ("A bacterial plasmid", True),
                 ("A lysosome", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "d")], "D",
                "DNA outside the nucleus",
                "The mitochondrial matrix possesses a single circular DNA molecule, a few RNA molecules and 70S "
                "ribosomes. The stroma of the chloroplast contains small, double-stranded circular DNA and 70S "
                "ribosomes. Plasmids are small circular DNA molecules outside the genomic DNA of bacteria. The Golgi "
                "apparatus and lysosomes are parts of the endomembrane system and contain no DNA.",
                ["(a), (b), (d): DNA present", "(c), (e): no DNA"],
                why="(c) and (e) are endomembrane components without DNA; (a) and (d) alone leave out the chloroplast.",
                ncert=ref("CELL", "Mitochondria; Plastids; Prokaryotic Cells"), secs=45)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "A gland cell synthesises and secretes large amounts of protein. Which pair of features would you expect to be "
       "prominent in it?",
       "Abundant rough endoplasmic reticulum and larger, more numerous nucleoli",
       ["Abundant smooth endoplasmic reticulum and few, small nucleoli",
        "Many microbodies and a large central vacuole",
        "Abundant smooth endoplasmic reticulum and many chromoplasts"], "C",
       "Organelles of a protein-secreting cell",
       "The rough ER is frequently observed in cells actively involved in protein synthesis and secretion, because its "
       "ribosomes make the proteins. The nucleolus is the site of active ribosomal RNA synthesis, and larger and more "
       "numerous nucleoli are present in cells actively carrying out protein synthesis.",
       ["Protein synthesis + secretion → RER", "Active protein synthesis → large, numerous nucleoli"],
       why="Smooth ER is the major site of lipid (and, in animals, steroid hormone) synthesis. Microbodies, vacuoles "
           "and chromoplasts are not features of protein-secreting cells.",
       ncert=ref("CELL", "Endomembrane System; Nucleus"), secs=40)

match_list(T_CELL, "Cell envelope and membrane", "Intermediate", "structure", "chemical composition given in NCERT",
           ["Middle lamella", "Cell wall of a higher plant", "Cell wall of an alga", "Peripheral fibrils of a "
            "centriole"],
           ["Cellulose, galactans, mannans and minerals like calcium carbonate", "The protein tubulin",
            "Mainly calcium pectate", "Cellulose, hemicellulose, pectins and proteins"],
           "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "D",
           "Composition of cell structures",
           "The middle lamella, which holds neighbouring cells together, is mainly made of calcium pectate. The cell wall "
           "of algae is made of cellulose, galactans, mannans and minerals like calcium carbonate, while in other plants "
           "it consists of cellulose, hemicellulose, pectins and proteins. The peripheral fibrils of a centriole are made "
           "of the protein tubulin.",
           ["Middle lamella → calcium pectate", "Higher plant wall → cellulose, hemicellulose, pectins, proteins",
            "Algal wall → cellulose, galactans, mannans, CaCO3", "Centriole fibrils → tubulin"],
           why="The wrong codes swap the middle lamella and higher-plant wall, the two kinds of cell wall, or the algal "
               "wall and the centriole.",
           ncert=ref("CELL", "Cell Wall; Centrosome and Centrioles"), secs=40)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "In the membrane of human red blood cells, proteins (about 52 per cent) make up a larger share than "
               "lipids (about 40 per cent).",
               "In the plasma membrane, the lipids are arranged with their hydrophobic tails towards the outer sides "
               "and their polar heads towards the inner part.",
               True, False, "C",
               "Composition and arrangement of the cell membrane",
               "Biochemical investigation showed that the membrane of the human erythrocyte has approximately 52 per "
               "cent protein and 40 per cent lipids. The lipids are arranged within the membrane with the polar head "
               "towards the outer sides and the hydrophobic tails towards the inner part, which protects the non-polar "
               "tails from the aqueous environment.",
               ["Statement I: true (52% protein, 40% lipid)", "Statement II: false; it reverses heads and tails"],
               ncert=ref("CELL", "Cell Membrane"), secs=40)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "Which of the following statements about membrane extensions and infoldings are correct?",
                [("The inner membrane of the mitochondrion forms infoldings called cristae.", True),
                 ("Mesosomes are formed by extensions of the plasma membrane into the cell, in the form of vesicles, "
                  "tubules and lamellae.", True),
                 ("The outer membrane of the mitochondrion forms the cristae.", False),
                 ("The tonoplast folds to form the grana of the vacuole.", False),
                 ("In cyanobacteria, membranous extensions into the cytoplasm called chromatophores contain "
                  "pigments.", True)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "e")], "B",
                "Membrane extensions in cells",
                "The inner mitochondrial membrane forms a number of infoldings called cristae towards the matrix, which "
                "increase the surface area; the outer membrane forms the continuous limiting boundary. In prokaryotes, "
                "mesosomes are extensions of the plasma membrane into the cell as vesicles, tubules and lamellae; they "
                "also increase the surface area of the plasma membrane and its enzymatic content. In some prokaryotes "
                "such as cyanobacteria, other membranous extensions into the cytoplasm, the chromatophores, contain "
                "pigments. Grana are stacks of thylakoids in chloroplasts; the tonoplast is the vacuole membrane.",
                ["(a), (b), (e) true", "(c) false: inner membrane", "(d) false: grana belong to chloroplasts"],
                why="(c) and (d) are false; (a) and (e) alone leave out the mesosomes.",
                ncert=ref("CELL", "Prokaryotic Cells; Mitochondria"), secs=60)

assertion_reason(T_CELL, "Endomembrane system", "Advanced",
                 "Lysosomes are formed by the process of packaging in the Golgi apparatus.",
                 "The Golgi apparatus receives no materials from the endoplasmic reticulum.",
                 True, False, False, "C",
                 "Golgi apparatus and lysosomes",
                 "Lysosomes are membrane-bound vesicular structures formed by the process of packaging in the Golgi "
                 "apparatus. The Golgi apparatus is closely associated with the ER: a number of proteins synthesised by "
                 "ribosomes on the endoplasmic reticulum are modified in the cisternae of the Golgi apparatus before "
                 "they are released from its trans face. So R is false.",
                 ["A: true", "R: false; ER proteins are modified in the Golgi cisternae"],
                 ncert=ref("CELL", "Endomembrane System (Golgi apparatus, lysosomes)"), secs=40)

direct(T_CELL, "Endomembrane system", "Advanced",
       "Which of the following is NOT a function of the Golgi apparatus described in NCERT?",
       "Synthesis of lipid-like steroidal hormones in animal cells",
       ["Packaging materials to be delivered to intracellular targets or secreted outside the cell",
        "Modifying proteins synthesised by ribosomes on the endoplasmic reticulum",
        "Formation of glycoproteins and glycolipids"], "A",
       "Functions of the Golgi apparatus and smooth ER",
       "The Golgi apparatus principally packages materials to be delivered either to intracellular targets or "
       "secreted outside the cell. Proteins synthesised by ribosomes on the ER are modified in its cisternae before "
       "release from the trans face, and it is the important site of formation of glycoproteins and glycolipids. "
       "The smooth ER is the major site of lipid synthesis; in animal cells lipid-like steroidal hormones are "
       "synthesised in the SER.",
       ["Golgi: packaging, modification, glycoproteins and glycolipids", "Steroid hormones: smooth ER"],
       why="The three other options are all Golgi functions listed by NCERT.",
       ncert=ref("CELL", "Endomembrane System"), secs=40)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "Mesosomes help in respiration and secretion processes in a bacterial cell, which has no mitochondria.",
               "The pili of bacteria are made of the protein tubulin, like the microtubules of cilia.",
               True, False, "C",
               "Prokaryotic structures",
               "Prokaryotic cells have no membrane-bound organelles such as mitochondria. Mesosomes, extensions of the "
               "plasma membrane, help in cell wall formation, DNA replication and distribution to daughter cells, and "
               "also in respiration and secretion processes. Pili are elongated tubular structures made of a special "
               "protein; NCERT does not say they are made of tubulin, which forms the microtubules and centriole "
               "fibrils of eukaryotic cells.",
               ["Statement I: true", "Statement II: false; pili are made of a special protein, not tubulin"],
               ncert=ref("CELL", "Prokaryotic Cells; Cilia and Flagella"), secs=45)

direct(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
       "Which pair consists of two structures that are both NOT part of the endomembrane system and that both lack "
       "DNA?",
       "Microbodies and centrioles",
       ["Mitochondria and chloroplasts", "Lysosomes and vacuoles", "Golgi apparatus and endoplasmic reticulum"], "D",
       "Endomembrane system and organelle DNA",
       "The endomembrane system comprises the ER, Golgi complex, lysosomes and vacuoles, whose functions are "
       "coordinated. Mitochondria, chloroplasts and peroxisomes are not part of it, and mitochondria and chloroplasts "
       "contain their own circular DNA. Microbodies (membrane-bound vesicles of enzymes) and centrioles (cylinders of "
       "tubulin fibrils) are outside the endomembrane system and contain no DNA.",
       ["Endomembrane: ER, Golgi, lysosomes, vacuoles", "Mitochondria, chloroplasts: have DNA",
        "Microbodies, centrioles: neither"],
       why="Mitochondria and chloroplasts contain DNA; lysosomes, vacuoles, the Golgi apparatus and the ER are all "
           "part of the endomembrane system.",
       ncert=ref("CELL", "Endomembrane System; Microbodies; Centrosome and Centrioles"), secs=50)


# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "Which of the following does NOT take place during interphase?",
       "Condensation of chromatin into compact chromosomes",
       ["Replication of DNA", "Duplication of the centriole in the cytoplasm of an animal cell",
        "Synthesis of proteins in preparation for mitosis"], "B",
       "Events of interphase and M phase",
       "Interphase consists of G1, S and G2. DNA replicates in the S phase, and in animal cells the centriole "
       "duplicates in the cytoplasm during the S phase. In G2, proteins are synthesised in preparation for mitosis "
       "while cell growth continues. Condensation of the chromosomal material into compact mitotic chromosomes marks "
       "prophase, the first stage of the M phase.",
       ["S: DNA replication, centriole duplication", "G2: proteins for mitosis", "Chromosome condensation: prophase"],
       why="DNA replication, centriole duplication and protein synthesis for mitosis all occur in interphase.",
       ncert=ref("CC", "Cell Cycle (phases of cell cycle); M Phase (prophase)"), secs=25)

direct(T_CC, "Significance", "Basic",
       "Which of the following is NOT brought about by mitosis?",
       "Formation of haploid gametes from diploid cells in animals",
       ["Replacement of the cells of the upper layer of the epidermis and the lining of the gut",
        "Continuous growth of plants by the apical and lateral cambium",
        "Increase in the number of cells in a growing multicellular organism"], "D",
       "Significance of mitosis",
       "Mitosis results in diploid daughter cells with identical genetic complement. It brings about the growth of "
       "multicellular organisms, cell repair (cells of the upper layer of the epidermis, the cells of the lining of the "
       "gut and blood cells are constantly replaced) and the continuous growth of plants through divisions in the "
       "apical and lateral cambium. Haploid gametes of animals are formed from diploid cells by meiosis, during "
       "gametogenesis.",
       ["Mitosis: growth, repair, meristem activity", "Gametes from diploid cells in animals: meiosis"],
       why="The other three options are the roles of mitosis listed in NCERT.",
       ncert=ref("CC", "Significance of Mitosis; Meiosis"), secs=25)

statement_pair(T_CC, "Meiosis", "Basic",
               "Electron micrographs of zygotene show that chromosome synapsis is accompanied by the formation of a "
               "complex structure called the synaptonemal complex.",
               "The complex formed by a pair of synapsed homologous chromosomes is called a bivalent.",
               True, True, "A",
               "Zygotene",
               "During zygotene, chromosomes start pairing together; this association is synapsis, and the paired "
               "chromosomes are homologous chromosomes. Electron micrographs of this stage indicate that synapsis is "
               "accompanied by the formation of a complex structure called the synaptonemal complex. The complex formed "
               "by a pair of synapsed homologous chromosomes is called a bivalent or a tetrad.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Meiosis I (prophase I: zygotene)"), secs=30)

match_list(T_CC, "Significance", "Basic", "process", "result",
           ["Mitosis in a diploid cell, followed by cytokinesis", "Meiosis I, followed by cytokinesis",
            "Meiosis II, followed by cytokinesis", "Karyokinesis not followed by cytokinesis"],
           ["A tetrad of four haploid cells", "A multinucleate condition (syncytium)",
            "Two cells with the same chromosome number as the parent", "A dyad of cells"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A",
           "Outcomes of cell division",
           "Mitosis is an equational division: the daughter cells have the same chromosome number as the parent. "
           "Telophase I is followed by cytokinesis, giving a dyad of cells. At the end of meiosis II cytokinesis forms a "
           "tetrad of cells, i.e. four haploid daughter cells. When karyokinesis is not followed by cytokinesis, a "
           "multinucleate condition arises, leading to a syncytium (e.g. the liquid endosperm of coconut).",
           ["Mitosis → 2 cells, same number", "Meiosis I → dyad", "Meiosis II → tetrad",
            "No cytokinesis → syncytium"],
           why="The wrong codes swap the dyad and the tetrad, or the syncytium with a product of meiosis.",
           ncert=ref("CC", "M Phase (cytokinesis); Meiosis I; Meiosis II"), secs=35)

numerical(T_CC, "Meiosis", "Intermediate",
          "A diploid plant cell contains 6 pg of DNA in its G1 phase. It replicates its DNA and then completes "
          "meiosis. How much DNA will be present in each of the four cells formed at the end of meiosis?",
          "3 pg", ["6 pg", "1.5 pg", "12 pg"], "C", Fraction(6 * 2, 4) == 3,
          "DNA content through meiosis",
          "In the S phase the DNA content doubles (6 → 12 pg) while the chromosome number stays the same. Meiosis "
          "involves two sequential cycles of nuclear and cell division but only a single cycle of DNA replication. "
          "Meiosis I halves it to 6 pg per cell, and meiosis II, in which sister chromatids separate, halves it again "
          "to 3 pg per cell.",
          ["G1: 6 pg → after S: 12 pg", "After meiosis I: 6 pg per cell", "After meiosis II: 3 pg per cell"],
          why="6 pg ignores the second division (or the replication); 1.5 pg halves twice without first doubling; "
              "12 pg is the content after the S phase, before any division.",
          ncert=ref("CC", "Cell Cycle (S phase); Meiosis"), secs=60,
          short="Each gamete-like product has half the G1 (2C) content: C = 6/2 = 3 pg.")

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "In anaphase of mitosis, as the chromatids move towards the poles, the centromere of each chromosome "
                 "leads, with the arms trailing behind.",
                 "The chromatids are moved towards the poles by the lengthening of the microtubules attached to their "
                 "kinetochores.",
                 True, False, False, "C",
                 "Movement of chromosomes in anaphase",
                 "At anaphase, centromeres split and the chromatids separate and move to opposite poles. As each "
                 "chromosome moves away from the equatorial plate, its centromere remains directed towards the pole, "
                 "at the leading edge, with the arms trailing behind. NCERT describes the sister chromatids moving "
                 "towards opposite poles by the shortening, not lengthening, of the microtubules attached to the "
                 "kinetochores.",
                 ["A: true", "R: false; kinetochore microtubules shorten"],
                 ncert=ref("CC", "M Phase (anaphase); Meiosis II (anaphase II)"), secs=40)

direct(T_CC, "Mitosis", "Intermediate",
       "In a dividing cell, the chromosomes have reached the two poles, the nuclear envelope is reassembling around "
       "each group, and a new wall is forming as a cell plate that grows from the centre outwards. This is:",
       "a plant cell at the end of telophase, undergoing cytokinesis",
       ["an animal cell at the end of telophase, undergoing cytokinesis", "a plant cell at anaphase",
        "an animal cell at metaphase"], "B",
       "Telophase and cytokinesis in plant cells",
       "At telophase, chromosomes cluster at opposite spindle poles and the nuclear envelope assembles around each "
       "cluster. In plant cells, enclosed by a relatively inextensible cell wall, cytokinesis takes place by cell wall "
       "formation that starts in the centre of the cell and grows outward to meet the existing lateral walls; it "
       "begins as a simple precursor, the cell plate. Animal cells divide their cytoplasm by a furrow in the plasma "
       "membrane.",
       ["Nuclear envelope reforming → telophase", "Cell plate from the centre → plant cell"],
       why="Animal cells do not form a cell plate; at anaphase and metaphase the nuclear envelope is not being "
           "reassembled.",
       ncert=ref("CC", "M Phase (telophase, cytokinesis)"), secs=40)

multi_statement(T_CC, "Meiosis", "Intermediate",
                "Which of the following take place in meiosis II but NOT in meiosis I?",
                [("Splitting of the centromere of each chromosome", True),
                 ("Separation of sister chromatids towards opposite poles", True),
                 ("Pairing of homologous chromosomes", False),
                 ("Crossing over between non-sister chromatids", False),
                 ("Attachment of microtubules from opposite poles to the kinetochores of sister chromatids", True)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "e")], "D",
                "Meiosis I and meiosis II compared",
                "In metaphase I, microtubules from opposite poles attach to the pair of homologous chromosomes, and in "
                "anaphase I the homologues separate while sister chromatids remain associated at their centromeres. In "
                "metaphase II, microtubules from opposite poles attach to the kinetochores of sister chromatids, and "
                "anaphase II begins with the simultaneous splitting of the centromere of each chromosome, so the sister "
                "chromatids move to opposite poles. Pairing (synapsis) and crossing over occur in prophase I only.",
                ["(a), (b), (e): meiosis II only", "(c), (d): meiosis I only"],
                why="(c) and (d) happen in meiosis I, not meiosis II; (a) and (e) alone leave out (b).",
                ncert=ref("CC", "Meiosis I; Meiosis II"), secs=55)

match_list(T_CC, "Meiosis", "Intermediate", "stage of prophase I", "feature",
           ["Leptotene", "Zygotene", "Pachytene", "Diplotene"],
           ["Can last for months or years in the oocytes of some vertebrates",
            "Compaction of chromosomes continues throughout this stage",
            "Longer-lived than the two stages before it; recombination nodules appear",
            "Chromosomes start pairing together (synapsis)"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "C",
           "Stages of prophase I",
           "In leptotene the chromosomes become gradually visible and their compaction continues throughout the stage. "
           "During zygotene chromosomes start pairing together (synapsis). The first two stages are relatively "
           "short-lived compared with pachytene, in which recombination nodules appear and crossing over occurs. In "
           "the oocytes of some vertebrates, diplotene can last for months or years.",
           ["Leptotene → compaction", "Zygotene → synapsis", "Pachytene → long, recombination nodules",
            "Diplotene → may last months/years"],
           why="The wrong codes swap leptotene and zygotene, pachytene and diplotene, or leptotene and pachytene.",
           ncert=ref("CC", "Meiosis I (prophase I)"), secs=40)

statement_pair(T_CC, "Meiosis", "Advanced",
               "Both mitosis and meiosis are preceded by a phase in which the DNA of the cell replicates.",
               "Sister chromatids separate at anaphase of mitosis and also at anaphase I of meiosis.",
               True, False, "C",
               "DNA replication and chromatid separation",
               "Mitosis follows interphase, in which DNA replicates during the S phase. Meiosis I is initiated after the "
               "parental chromosomes have replicated to produce identical sister chromatids at the S phase; meiosis has "
               "only a single cycle of DNA replication. At anaphase of mitosis the sister chromatids separate, but at "
               "anaphase I the homologous chromosomes separate while the sister chromatids remain associated at their "
               "centromeres; sister chromatids separate only at anaphase II.",
               ["Statement I: true", "Statement II: false; anaphase I separates homologues"],
               ncert=ref("CC", "Cell Cycle; Meiosis I"), secs=45)

numerical(T_CC, "Cell cycle phases", "Advanced",
          "In a culture of human cells, each cell divides about once in 24 hours, and the M phase lasts about 1 hour. "
          "Assume the cells are dividing independently and are spread evenly over all stages of the cycle. In a "
          "sample of 960 cells, about how many would be expected to be in the M phase at any moment?",
          "40", ["24", "920", "96"], "A", 960 * 1 // 24 == 40 and 960 % 24 == 0,
          "Duration of M phase and fraction of dividing cells",
          "A typical human cell in culture divides about once every 24 hours, and the actual cell division (M phase) "
          "lasts only about an hour; interphase takes the rest. If cells are spread evenly over the cycle, the "
          "fraction found in M phase equals the fraction of time spent in it: 1/24. So 960 × 1/24 = 40 cells.",
          ["Fraction of cycle in M = 1/24", "960 × 1/24 = 40"],
          why="24 confuses the number of hours with the number of cells; 920 is the number in interphase; 96 uses 1/10 "
              "instead of 1/24.",
          ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=60,
          short="Cells in M ∝ time in M: 960/24 = 40.")

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements comparing telophase of mitosis with telophase I of meiosis are "
                "correct?",
                [("The nuclear membrane and nucleolus reappear in both.", True),
                 ("Each nucleus formed at telophase I has half the chromosome number of the parent meiocyte.", True),
                 ("Each chromosome in a telophase I nucleus still consists of two chromatids.", True),
                 ("At the end of telophase I, the chromosomes always reach the extremely extended state of an "
                  "interphase nucleus.", False),
                 ("Cytokinesis after telophase I produces a tetrad of cells.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "B",
                "Telophase of mitosis and telophase I",
                "At telophase of mitosis the nuclear envelope assembles around each chromosome cluster and the "
                "nucleolus reappears. In telophase I the nuclear membrane and nucleolus reappear and cytokinesis follows, "
                "giving a dyad of cells. Since anaphase I separated homologous chromosomes while sister chromatids "
                "stayed together, each nucleus has half the chromosome number, and each chromosome still has two "
                "chromatids. Although the chromosomes undergo some dispersion, they do not reach the extremely "
                "extended state of the interphase nucleus. A tetrad of cells forms only after meiosis II.",
                ["(a), (b), (c) true", "(d) false: not fully extended", "(e) false: a dyad forms"],
                why="(d) and (e) are false; (a) and (c) alone leave out (b).",
                ncert=ref("CC", "M Phase (telophase); Meiosis I (telophase I)"), secs=60)

assertion_reason(T_CC, "Mitosis", "Advanced",
                 "Each daughter chromosome that moves towards a pole at anaphase of mitosis consists of a single "
                 "chromatid.",
                 "At anaphase, the centromere of each chromosome splits and the two sister chromatids separate and move "
                 "to opposite poles.",
                 True, True, True, "A",
                 "Daughter chromosomes at anaphase",
                 "At metaphase each chromosome is made of two sister chromatids held together by the centromere. At "
                 "anaphase, centromeres split and the chromatids separate; each chromatid, now a daughter chromosome, "
                 "moves to the opposite pole. Because the two chromatids of every chromosome are separated, each moving "
                 "daughter chromosome has only one chromatid.",
                 ["A: true", "R: true; splitting of centromeres and separation of chromatids is why each has one"],
                 ncert=ref("CC", "M Phase (metaphase, anaphase)"), secs=40)


# =============================================================== 7. Photosynthesis (4/6/4)
direct(T_PS, "Site and pigments", "Basic",
       "A graph showing the ability of chlorophyll a, chlorophyll b and the carotenoids to absorb light of different "
       "wavelengths is called the:",
       "absorption spectrum",
       ["action spectrum", "Z scheme", "light saturation curve"], "D",
       "Absorption and action spectra",
       "NCERT shows two graphs: one showing the absorption spectrum of chlorophyll a, b and the carotenoids (how much "
       "light of each wavelength each pigment absorbs), and another showing the action spectrum of photosynthesis "
       "(the rate of photosynthesis at different wavelengths). Comparing them shows that most photosynthesis takes "
       "place in the blue and red regions, where chlorophyll a absorbs most.",
       ["Absorption of light by pigments vs wavelength = absorption spectrum",
        "Rate of photosynthesis vs wavelength = action spectrum"],
       why="The action spectrum plots the rate of photosynthesis, not absorption. The Z scheme shows electron carriers "
           "on a redox scale. A light saturation curve plots rate against light intensity.",
       ncert=ref("PS", "How many Types of Pigments are Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Since the first product of CO₂ fixation found by Calvin was a 3-carbon acid, scientists at first searched for "
       "a CO₂ acceptor with two carbons. The acceptor they finally discovered was:",
       "a 5-carbon ketose sugar, ribulose bisphosphate (RuBP)",
       ["a 2-carbon compound, as predicted", "a 3-carbon compound, phosphoenol pyruvate (PEP)",
        "a 4-carbon acid, oxaloacetic acid (OAA)"], "C",
       "The primary acceptor of the Calvin cycle",
       "Because the first product was a C3 acid, the scientists reasoned that the primary acceptor would be a "
       "2-carbon molecule, and they spent many years trying to identify it. Surprisingly, the acceptor molecule was a "
       "5-carbon ketose sugar, ribulose bisphosphate (RuBP); CO₂ (1 C) + RuBP (5 C) gives two molecules of 3-PGA.",
       ["Expected: 2-carbon acceptor", "Found: RuBP, a 5-carbon ketose sugar"],
       why="No 2-carbon acceptor was found. PEP is the primary acceptor of the C4 pathway in mesophyll cells, and OAA "
           "is the first product of the C4 pathway.",
       ncert=ref("PS", "The Primary Acceptor of CO₂"), secs=25)

match_list(T_PS, "Light reactions and photophosphorylation", "Basic", "process", "product(s)",
           ["Non-cyclic photophosphorylation", "Cyclic photophosphorylation", "Carboxylation of RuBP by RuBisCO "
            "with CO₂", "Combination of RuBP with O₂"],
           ["Two molecules of 3-PGA", "One molecule of PGA and one of phosphoglycolate", "ATP, NADPH + H⁺ and O₂",
            "ATP only"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D",
           "Products of the reactions of photosynthesis",
           "In non-cyclic photophosphorylation both ATP and NADPH + H⁺ are synthesised, and O₂ is released by the "
           "splitting of water. Cyclic photophosphorylation results in the synthesis of ATP only, not NADPH + H⁺. "
           "RuBisCO carboxylates RuBP with CO₂ to form two molecules of 3-PGA. In photorespiration, RuBP combines with "
           "O₂ to form one molecule of PGA and phosphoglycolate.",
           ["Non-cyclic → ATP, NADPH, O₂", "Cyclic → ATP only", "Carboxylation → 2 PGA",
            "Oxygenation → PGA + phosphoglycolate"],
           why="The wrong codes swap the two kinds of photophosphorylation, or the carboxylation and oxygenation "
               "products.",
           ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation; The Calvin Cycle; Photorespiration"),
           secs=40)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "The splitting of water associated with Photosystem II releases:",
       "protons (H⁺), electrons and O₂",
       ["CO₂ and electrons", "ATP and NADPH", "O₂ and NADPH only"], "B",
       "Splitting of water",
       "Electrons removed from PS II are replaced by electrons available from the splitting of water: "
       "2H₂O → 4H⁺ + O₂ + 4e⁻. The water-splitting complex is associated with PS II. The electrons replace those "
       "lost by PS II, the protons accumulate in the lumen, and oxygen is released as a by-product.",
       ["2H₂O → 4H⁺ + O₂ + 4e⁻"],
       why="CO₂ is not produced by the light reaction. ATP is made by ATP synthase and NADPH by NADP reductase, not "
           "directly by water splitting.",
       ncert=ref("PS", "The Electron Transport (splitting of water)"), secs=20)

numerical(T_PS, "Light reactions and photophosphorylation", "Intermediate",
          "Water is split in the light reaction as 2H₂O → 4H⁺ + O₂ + 4e⁻. The electrons are finally passed to NADP⁺, "
          "each molecule of NADP⁺ accepting two electrons to form NADPH + H⁺. If 6 molecules of water are split, how "
          "many molecules of NADPH can be formed?",
          "6", ["3", "12", "24"], "D", (6 * 4 // 2) // 2 == 6,
          "Electrons from water to NADP⁺",
          "Every 2 molecules of water give 4 electrons, so 6 molecules give 12 electrons (and 3 O₂). Each NADP⁺ needs "
          "two electrons to be reduced to NADPH + H⁺, so 12 electrons reduce 6 NADP⁺. In other words, one NADPH is "
          "formed for every molecule of water split.",
          ["6 H₂O → 12 e⁻ (and 3 O₂)", "12 e⁻ ÷ 2 e⁻ per NADPH = 6 NADPH"],
          why="3 is the number of O₂ molecules; 12 is the number of electrons (or protons); 24 multiplies the "
              "electrons by two instead of dividing.",
          ncert=ref("PS", "The Electron Transport (splitting of water; NADP⁺ reduction)"), secs=60,
          short="One NADPH per water molecule split.")

assertion_reason(T_PS, "Site and pigments", "Intermediate",
                 "Chlorophyll a is the chief pigment associated with photosynthesis.",
                 "On a paper chromatogram of leaf pigments, xanthophylls appear yellow.",
                 True, True, False, "B",
                 "Leaf pigments",
                 "Chlorophyll a (bright or blue-green on a chromatogram) is the chief pigment associated with "
                 "photosynthesis; it forms the reaction centres of both photosystems. Chlorophyll b (yellow-green), "
                 "xanthophylls (yellow) and carotenoids (yellow to yellow-orange) are accessory pigments. The colour of "
                 "xanthophylls on a chromatogram has nothing to do with why chlorophyll a is the chief pigment.",
                 ["A: true", "R: true", "R is about a different pigment's colour"],
                 ncert=ref("PS", "How many Types of Pigments are Involved in Photosynthesis?"), secs=35)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                 "The regeneration of RuBP in the Calvin cycle requires ATP.",
                 "The regeneration of RuBP in the Calvin cycle requires NADPH.",
                 True, False, False, "C",
                 "Energy needs of the stages of the Calvin cycle",
                 "The reduction stage uses 2 molecules of ATP for phosphorylation and 2 of NADPH for reduction per CO₂ "
                 "fixed. The regeneration of the CO₂ acceptor RuBP requires one ATP for phosphorylation to form RuBP; "
                 "it does not use NADPH.",
                 ["A: true (1 ATP per CO₂)", "R: false; NADPH is used only in reduction"],
                 ncert=ref("PS", "The Calvin Cycle (regeneration)"), secs=35)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following take place in the stroma of the chloroplast?",
                [("Carboxylation of RuBP by RuBisCO", True),
                 ("Reduction of PGA to carbohydrate using ATP and NADPH", True),
                 ("Regeneration of RuBP", True),
                 ("Splitting of water", False),
                 ("Diffusion of protons through the CF₀ channel of ATP synthase", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "B",
                "Sites of reactions in the chloroplast",
                "The membrane system (thylakoids) traps light energy and synthesises ATP and NADPH; the enzymatic "
                "reactions that incorporate CO₂ into sugar take place in the stroma. So carboxylation, reduction and "
                "regeneration of the Calvin cycle occur in the stroma. Water is split on the inner (lumen) side of the "
                "thylakoid membrane, and protons pass through the CF₀ channel, which is embedded in the thylakoid "
                "membrane.",
                ["(a), (b), (c): Calvin cycle in stroma", "(d): lumen side of thylakoid membrane",
                 "(e): channel in thylakoid membrane"],
                why="(d) and (e) are thylakoid membrane events; (a) and (c) alone leave out reduction.",
                ncert=ref("PS", "Where does Photosynthesis take place?; The Calvin Cycle; The Chemiosmotic Hypothesis"),
                secs=50)

match_list(T_PS, "Limiting factors", "Intermediate", "factor", "NCERT's statement about it",
           ["Light", "Carbon dioxide", "Temperature", "Water"],
           ["The dark reactions, being enzymatic, are controlled by it",
            "Its stress causes stomata to close and leaves to wilt",
            "Saturation occurs at about 10 per cent of full sunlight",
            "The major limiting factor; present in the atmosphere at 0.03–0.04 per cent"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A",
           "Factors affecting photosynthesis",
           "Light saturation occurs at about 10 per cent of full sunlight, so light is rarely limiting except in shade "
           "or dense forests. Carbon dioxide is the major limiting factor; its atmospheric concentration is very low, "
           "0.03–0.04 per cent. The dark reactions, being enzymatic, are temperature controlled. Water stress causes "
           "the stomata to close, reducing CO₂ availability, and makes leaves wilt.",
           ["Light → 10% saturation", "CO₂ → major limiting factor", "Temperature → enzymatic dark reactions",
            "Water → stomatal closure, wilting"],
           why="The wrong codes swap light and CO₂, temperature and water, or CO₂ and temperature.",
           ncert=ref("PS", "Factors affecting Photosynthesis"), secs=40)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
               "The Calvin cycle operates in C4 plants as well as in C3 plants.",
               "In C4 plants, the Calvin cycle takes place in the mesophyll cells.",
               True, False, "C",
               "Calvin cycle in C3 and C4 plants",
               "The Calvin pathway occurs in all photosynthetic plants, whether they have the C3 or the C4 pathway. In "
               "C4 plants, the mesophyll cells carry out the initial fixation by PEP carboxylase and lack RuBisCO; the "
               "Calvin pathway takes place in the bundle sheath cells, which are rich in RuBisCO.",
               ["Statement I: true", "Statement II: false; it runs in the bundle sheath cells"],
               ncert=ref("PS", "The C4 Pathway"), secs=35)

multi_statement(T_PS, "Photorespiration", "Advanced",
                "In a C3 leaf, the concentration of O₂ around RuBisCO rises greatly relative to that of CO₂. Which of "
                "the following changes are expected?",
                [("A larger share of RuBP combines with O₂.", True),
                 ("More phosphoglycolate is formed.", True),
                 ("More CO₂ is released in a pathway that uses up ATP.", True),
                 ("The synthesis of sugars increases.", False),
                 ("More ATP is generated by photorespiration.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "b")], "C",
                "Applying the conditions for photorespiration",
                "The active site of RuBisCO can bind both CO₂ and O₂, and the relative concentration of O₂ and CO₂ "
                "determines which binds. When O₂ is relatively high, more RuBP is oxygenated, forming one PGA and one "
                "phosphoglycolate. This pathway, photorespiration, releases CO₂ with the utilisation of ATP; there is "
                "neither synthesis of sugars nor of ATP or NADPH.",
                ["(a), (b), (c) follow from more oxygenation", "(d) false: less carboxylation, no sugar from "
                 "photorespiration", "(e) false: photorespiration uses ATP"],
                why="(d) and (e) are false; (a) and (b) alone leave out the release of CO₂.",
                ncert=ref("PS", "Photorespiration"), secs=60)

direct(T_PS, "Chemiosmosis", "Advanced",
       "In an illuminated chloroplast, the CF₀ channel of ATP synthase is blocked so that protons cannot pass through "
       "it, while electron transport continues. What is the immediate result?",
       "ATP synthesis stops, though the proton gradient across the thylakoid membrane can still build up",
       ["ATP synthesis continues, because the proton gradient keeps increasing",
        "Water splitting stops at once, because PS II needs ATP",
        "The proton concentration in the lumen falls, because protons leak to the stroma"], "D",
       "Chemiosmotic synthesis of ATP",
       "Electron transport and water splitting build a proton gradient: protons accumulate in the lumen. ATP synthase "
       "has two parts: CF₀, embedded in the membrane, forms a transmembrane channel for facilitated diffusion of "
       "protons across the membrane, and CF₁ protrudes into the stroma. The breakdown of the gradient by protons moving "
       "through CF₀ provides the energy for a conformational change in CF₁ that synthesises ATP. If CF₀ is blocked, "
       "the gradient cannot be broken down, so ATP is not made even though the gradient may remain or grow.",
       ["Gradient made by electron transport", "ATP needs protons flowing through CF₀ → CF₁",
        "Blocked CF₀ → no ATP"],
       why="A larger gradient is useless without proton flow through CF₀. Water splitting does not need ATP. Protons "
           "cannot flow back through the blocked channel, so the lumen does not lose them this way.",
       ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=60)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "In C4 plants, the first stable product of CO₂ fixation, formed in the mesophyll cells, is 3-PGA.",
                 "In the mesophyll cells of C4 plants, PEP carboxylase fixes CO₂ with phosphoenol pyruvate.",
                 False, True, False, "D",
                 "First product of the C4 pathway",
                 "In C4 plants the primary CO₂ acceptor in the mesophyll cells is the 3-carbon phosphoenol pyruvate "
                 "(PEP), and the fixation is carried out by PEP carboxylase. The first stable product is the 4-carbon "
                 "oxaloacetic acid (OAA), hence the name C4. 3-PGA is formed later, when the CO₂ released in the bundle "
                 "sheath cells is fixed by RuBisCO.",
                 ["A: false; the first product is OAA (C4)", "R: true"],
                 ncert=ref("PS", "The C4 Pathway"), secs=40)

numerical(T_PS, "Calvin cycle and C4 pathway", "Advanced",
          "In a C4 plant, each molecule of atmospheric CO₂ is first fixed by PEP carboxylase in a mesophyll cell, then "
          "released in a bundle sheath cell and fixed again by RuBisCO. Making one molecule of glucose needs six "
          "molecules of CO₂ to enter the Calvin cycle. How many carboxylation reactions in all (by both enzymes "
          "together) are needed for one glucose?",
          "12", ["6", "18", "24"], "A", 6 * 2 == 12,
          "Double carboxylation in C4 plants",
          "In the C4 pathway, CO₂ is fixed by PEPcase into OAA in the mesophyll; the C4 acid is carried to the bundle "
          "sheath, where it is broken down to release CO₂, which RuBisCO fixes again into PGA in the Calvin cycle. "
          "Glucose needs 6 CO₂ through the Calvin cycle, and each of these 6 molecules is fixed twice: 6 × 2 = 12 "
          "carboxylations.",
          ["6 CO₂ per glucose", "Each CO₂ fixed by PEPcase and then by RuBisCO", "6 × 2 = 12"],
          why="6 counts only one enzyme; 18 confuses carboxylations with the ATP used per glucose; 24 counts each "
              "CO₂ four times.",
          ncert=ref("PS", "The C4 Pathway; The Calvin Cycle"), secs=60)


# =============================================================== 8. Respiration in Plants (4/4/4)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "In glycolysis, fructose 1,6-bisphosphate is split into:",
       "dihydroxyacetone phosphate and 3-phosphoglyceraldehyde (PGAL)",
       ["two molecules of pyruvic acid", "glucose-6-phosphate and fructose-6-phosphate",
        "1,3-bisphosphoglyceric acid and phosphoenolpyruvate"], "D",
       "Splitting step of glycolysis",
       "In glycolysis, glucose is phosphorylated to glucose-6-phosphate, which is isomerised to fructose-6-phosphate. "
       "This is phosphorylated again (using ATP) to fructose 1,6-bisphosphate, which is split into dihydroxyacetone "
       "phosphate and 3-phosphoglyceraldehyde (PGAL). PGAL is then oxidised to BPGA, and the pathway goes on to "
       "pyruvic acid.",
       ["Fructose 1,6-bisphosphate (6C) → DHAP (3C) + PGAL (3C)"],
       why="Pyruvic acid is the end product of glycolysis; glucose-6-phosphate and fructose-6-phosphate come before "
           "this step; BPGA and PEP come after it.",
       ncert=ref("RES", "Glycolysis"), secs=20)

statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "During respiration, oxygen is utilised, and carbon dioxide, water and energy are released as products.",
               "The combustion reaction of respiration requires oxygen, but some cells live where oxygen may or may "
               "not be available.",
               True, True, "A",
               "Respiration and the availability of oxygen",
               "NCERT states that during the process of respiration oxygen is utilised, and carbon dioxide, water and "
               "energy are released as products. The combustion reaction requires oxygen, but some cells live where "
               "oxygen may or may not be available; this is why organisms also retain pathways, such as glycolysis "
               "and fermentation, that partially oxidise glucose without oxygen.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Introduction; Glycolysis"), secs=30)

match_list(T_RES, "Glycolysis and fermentation", "Basic", "compound", "how it is formed",
           ["Pyruvic acid", "Citric acid", "Lactic acid", "Water"],
           ["When oxygen accepts electrons and hydrogen at the end of the electron transport system",
            "As the end product of glycolysis in the cytoplasm",
            "By reduction of pyruvic acid in muscle when oxygen is inadequate",
            "By condensation of the acetyl group with oxaloacetic acid and water"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "Formation of compounds in respiration",
           "Glycolysis in the cytoplasm ends with pyruvic acid. In the TCA cycle, the acetyl group condenses with "
           "oxaloacetic acid and water to form citric acid (citrate synthase). In animal muscle, when oxygen is "
           "inadequate, pyruvic acid is reduced to lactic acid by lactate dehydrogenase. At the end of the electron "
           "transport system, oxygen acts as the final hydrogen acceptor, and water is formed.",
           ["Pyruvic acid → glycolysis", "Citric acid → condensation in TCA", "Lactic acid → anaerobic muscle",
            "Water → O₂ at end of ETS"],
           why="The wrong codes swap pyruvic and citric acids, lactic acid and water, or pyruvic and lactic acids.",
           ncert=ref("RES", "Glycolysis; Fermentation; Tricarboxylic Acid Cycle; Electron Transport System"), secs=40)

assertion_reason(T_RES, "Glycolysis and fermentation", "Basic",
                 "Fermentation yields far less energy from a molecule of glucose than aerobic respiration does.",
                 "In fermentation, glucose is only partially broken down, whereas in aerobic respiration it is "
                 "completely degraded to CO₂ and H₂O.",
                 True, True, True, "A",
                 "Fermentation and aerobic respiration",
                 "Fermentation accounts for only a partial breakdown of glucose, and less than seven per cent of the "
                 "energy in glucose is released (not all of it trapped as ATP). In aerobic respiration glucose is "
                 "completely degraded to CO₂ and H₂O, releasing much more energy. The low yield of fermentation follows "
                 "directly from the incomplete breakdown.",
                 ["A: true", "R: true; partial breakdown is why little energy is released"],
                 ncert=ref("RES", "Fermentation"), secs=35)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "Glycolysis is present in all living organisms.",
                 "In glycolysis, ATP is used when fructose-6-phosphate is converted to fructose 1,6-bisphosphate.",
                 True, True, False, "B",
                 "Universality of glycolysis",
                 "Glycolysis is the partial oxidation of glucose to pyruvic acid; it is present in all living organisms "
                 "and is the only process of respiration in anaerobic organisms, reflecting that the first cells lived "
                 "in an atmosphere without oxygen. Separately, one of its steps uses ATP to phosphorylate "
                 "fructose-6-phosphate. That ATP-using step does not explain why the pathway is universal.",
                 ["A: true", "R: true", "R is a detail of one step, unrelated to A"],
                 ncert=ref("RES", "Glycolysis"), secs=35)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "In which of the following conversions is NAD⁺ reduced to NADH + H⁺?",
                [("PGAL → 1,3-bisphosphoglyceric acid (BPGA)", True),
                 ("Pyruvic acid → acetyl CoA", True),
                 ("Succinyl CoA → succinic acid", False),
                 ("Pyruvic acid → lactic acid", False),
                 ("Pyruvic acid → CO₂ and ethanol", False)],
                [("a", "b", "c"), ("b", "d"), ("a", "d", "e")], "D",
                "Steps that form NADH",
                "In glycolysis, PGAL is oxidised to BPGA, and two redox equivalents are removed and transferred to NAD⁺, "
                "forming NADH + H⁺. The oxidative decarboxylation of pyruvic acid to acetyl CoA by pyruvic "
                "dehydrogenase also produces NADH + H⁺. The conversion of succinyl CoA to succinic acid gives GTP. In "
                "both kinds of fermentation, NADH + H⁺ is reoxidised to NAD⁺, not formed.",
                ["(a), (b): NADH formed", "(c): GTP formed", "(d), (e): NADH used up"],
                why="Options with (c), (d) or (e) include steps that make GTP or consume NADH.",
                ncert=ref("RES", "Glycolysis; Aerobic Respiration; Fermentation"), secs=50)

direct(T_RES, "Electron transport system", "Intermediate",
       "Which of the following steps of aerobic respiration takes place in the inner mitochondrial membrane?",
       "Oxidation of NADH by NADH dehydrogenase (complex I)",
       ["Oxidative decarboxylation of pyruvic acid to acetyl CoA",
        "Condensation of acetyl CoA with oxaloacetic acid to form citric acid",
        "Isomerisation of glucose-6-phosphate to fructose-6-phosphate"], "C",
       "Sites of the steps of respiration",
       "Glycolysis takes place in the cytoplasm. The oxidative decarboxylation of pyruvic acid and the TCA cycle "
       "take place in the matrix of the mitochondria. The electron transport system, including NADH dehydrogenase "
       "(complex I), is present in the inner mitochondrial membrane, where electrons are passed to O₂ and ATP is "
       "synthesised.",
       ["Cytoplasm: glycolysis", "Matrix: link reaction, TCA cycle", "Inner membrane: ETS and ATP synthase"],
       why="Pyruvate decarboxylation and citrate formation are matrix reactions; the isomerisation is a glycolytic "
           "step in the cytoplasm.",
       ncert=ref("RES", "Aerobic Respiration; Electron Transport System"), secs=35)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
               "In the aerobic respiration of one molecule of glucose, two molecules of GTP (equivalent to ATP) are "
               "formed by substrate-level phosphorylation in the TCA cycle.",
               "In glycolysis, ATP is synthesised directly at two steps: the conversion of BPGA to PGA and the "
               "conversion of PEP to pyruvic acid.",
               True, True, "A",
               "ATP formed without the ETS",
               "In the TCA cycle, the conversion of succinyl CoA to succinic acid is accompanied by the synthesis of one "
               "GTP (a substrate-level phosphorylation; GTP can give ATP in a coupled reaction). One glucose gives two "
               "pyruvic acids and so two acetyl CoA, i.e. two turns of the cycle and two GTP. In glycolysis, ATP is "
               "formed when BPGA is converted to PGA and when PEP is converted to pyruvic acid.",
               ["Statement I: one GTP per turn × 2 turns = 2: true", "Statement II: true"],
               ncert=ref("RES", "Glycolysis; Tricarboxylic Acid Cycle"), secs=45)

numerical(T_RES, "Electron transport system", "Advanced",
          "Complete aerobic oxidation of one molecule of glucose produces 10 NADH + H⁺ and 2 FADH₂. Each of these "
          "passes two electrons into the electron transport system, and four electrons are needed to reduce one "
          "molecule of O₂ to two molecules of water. How many molecules of O₂ are needed to accept all these "
          "electrons?",
          "6", ["12", "3", "5"], "C", (10 + 2) * 2 // 4 == 6,
          "Oxygen as the final hydrogen acceptor",
          "The reducing equivalents formed in glycolysis, the link reaction and the TCA cycle are oxidised in the "
          "electron transport system, with oxygen as the final hydrogen acceptor, forming water. 12 carriers × 2 "
          "electrons = 24 electrons; 24 ÷ 4 = 6 O₂. This matches the 6 O₂ in the overall equation "
          "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O.",
          ["10 NADH + 2 FADH₂ = 12 carriers", "12 × 2 e⁻ = 24 e⁻", "24 ÷ 4 = 6 O₂"],
          why="12 counts one O₂ per carrier; 3 divides by 8; 5 counts only the NADH (10 × 2 ÷ 4) and leaves out "
              "FADH₂.",
          ncert=ref("RES", "Electron Transport System and Oxidative Phosphorylation"), secs=70,
          short="One O₂ per two carriers: 12/2 = 6.")

multi_statement(T_RES, "Glycolysis and fermentation", "Advanced",
                "In a yeast cell, the electron transport system stops working completely. Which of the following can "
                "still continue?",
                [("Glycolysis", True),
                 ("Conversion of pyruvic acid to CO₂ and ethanol", True),
                 ("The TCA cycle", False),
                 ("Oxidative phosphorylation", False),
                 ("Reoxidation of the NADH of glycolysis to NAD⁺ by alcohol dehydrogenase", True)],
                [("a", "c", "e"), ("a", "b", "d"), ("b", "e")], "B",
                "Fermentation when the ETS stops",
                "Yeast can obtain energy anaerobically. Glycolysis continues in the cytoplasm, and pyruvic acid is "
                "converted to CO₂ and ethanol by pyruvic acid decarboxylase and alcohol dehydrogenase, which reoxidises "
                "NADH + H⁺ to NAD⁺ and so lets glycolysis go on. The TCA cycle needs continued regeneration of NAD⁺ and "
                "FAD⁺ by the ETS, and oxidative phosphorylation depends on the ETS, so both stop.",
                ["(a), (b), (e): fermentation continues", "(c): needs NAD⁺/FAD⁺ from the ETS", "(d): needs the ETS"],
                why="(c) and (d) cannot continue without the ETS; (b) and (e) alone leave out glycolysis.",
                ncert=ref("RES", "Fermentation; Tricarboxylic Acid Cycle; Electron Transport System"), secs=60)

assertion_reason(T_RES, "Glycolysis and fermentation", "Advanced",
                 "CO₂ is released in lactic acid fermentation.",
                 "In alcoholic fermentation, pyruvic acid decarboxylase removes CO₂ from pyruvic acid.",
                 False, True, False, "D",
                 "Two kinds of fermentation",
                 "In alcoholic fermentation (yeast), pyruvic acid is converted to CO₂ and ethanol by pyruvic acid "
                 "decarboxylase and alcohol dehydrogenase. In lactic acid fermentation (some bacteria; animal muscle "
                 "when oxygen is inadequate), pyruvic acid is reduced to lactic acid by lactate dehydrogenase, and no "
                 "CO₂ is released.",
                 ["A: false; pyruvic acid → lactic acid releases no CO₂", "R: true"],
                 ncert=ref("RES", "Fermentation"), secs=40)

direct(T_RES, "Electron transport system", "Advanced",
       "Which of the following gives the correct path of electrons from NADH to oxygen in the mitochondrial electron "
       "transport system?",
       "NADH → complex I → ubiquinone → complex III → cytochrome c → complex IV → O₂",
       ["NADH → complex I → cytochrome c → complex III → ubiquinone → complex IV → O₂",
        "NADH → complex II → ubiquinone → complex IV → cytochrome c → complex III → O₂",
        "NADH → ubiquinone → complex I → complex III → complex IV → cytochrome c → O₂"], "D",
       "Sequence of the electron transport system",
       "Electrons from NADH are oxidised by NADH dehydrogenase (complex I) and transferred to ubiquinone in the inner "
       "membrane. Reduced ubiquinone (ubiquinol) is oxidised with transfer of electrons to cytochrome c via the "
       "cytochrome bc₁ complex (complex III). Cytochrome c, a small mobile protein on the outer surface of the inner "
       "membrane, carries electrons between complex III and complex IV (cytochrome c oxidase), which passes them to "
       "oxygen. FADH₂ enters through complex II to ubiquinone.",
       ["NADH → I → UQ → III → cyt c → IV → O₂"],
       why="Ubiquinone lies between complexes I and III, and cytochrome c between III and IV; complex II receives "
           "FADH₂, not NADH.",
       ncert=ref("RES", "Electron Transport System and Oxidative Phosphorylation"), secs=50)


# =============================================================== 9. Plant Growth and Development (4/4/4)
direct(T_PGD, "Growth rate", "Basic",
       "Plant growth can be measured by a variety of parameters. Which of the following is NOT one of the parameters "
       "listed by NCERT?",
       "Colour of the leaves",
       ["Dry weight", "Cell number", "Volume"], "A",
       "Measuring growth",
       "Growth at the cellular level is principally a consequence of an increase in the amount of protoplasm; as this "
       "is difficult to measure directly, a quantity more or less proportional to it is measured. Growth is therefore "
       "measured by parameters such as increase in fresh weight, dry weight, length, area, volume and cell number.",
       ["Parameters: fresh weight, dry weight, length, area, volume, cell number"],
       why="Dry weight, cell number and volume are all listed parameters; colour is not a measure of growth.",
       ncert=ref("PGD", "Growth (plant growth is measurable)"), secs=20)

match_list(T_PGD, "Plant growth regulators", "Basic", "plant growth regulator", "source from which it was first "
           "isolated or identified",
           ["Auxin", "Kinetin", "Zeatin", "Gibberellic acid"],
           ["Corn kernels and coconut milk", "Human urine", "The fungus Gibberella fujikuroi",
            "Autoclaved herring sperm DNA"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "B",
           "Discovery of plant growth regulators",
           "Auxin was first isolated from human urine. Skoog and Miller crystallised the cytokinesis-promoting substance "
           "kinetin, identified as a modified form of adenine in autoclaved herring sperm DNA. Zeatin was later isolated "
           "from corn kernels and coconut milk. Kurosawa showed that bakanae disease of rice was caused by the fungus "
           "Gibberella fujikuroi; its active substance was later identified as gibberellic acid.",
           ["Auxin → human urine", "Kinetin → herring sperm DNA", "Zeatin → corn kernels, coconut milk",
            "Gibberellic acid → Gibberella fujikuroi"],
           why="The wrong codes swap auxin and kinetin, zeatin and gibberellic acid, or kinetin and zeatin.",
           ncert=ref("PGD", "Plant Growth Regulators (discovery; auxins; gibberellins; cytokinins)"), secs=40)

statement_pair(T_PGD, "Plant growth regulators", "Basic",
               "Chemically, kinetin is an adenine derivative.",
               "Chemically, ethylene is a terpene.",
               True, False, "C",
               "Chemical nature of PGRs",
               "PGRs are small, simple molecules of diverse chemical composition: indole compounds (indole-3-acetic "
               "acid, IAA), adenine derivatives (N6-furfurylamino purine, kinetin), derivatives of carotenoids "
               "(abscisic acid, ABA), terpenes (gibberellic acid, GA₃) or gases (ethylene, C₂H₄).",
               ["Statement I: true", "Statement II: false; ethylene is a gas; GA₃ is the terpene"],
               ncert=ref("PGD", "Plant Growth Regulators (characteristics)"), secs=30)

assertion_reason(T_PGD, "Plant growth regulators", "Basic",
                 "Auxins help to initiate rooting in stem cuttings.",
                 "The auxin 2,4-D is widely used to kill dicotyledonous weeds.",
                 True, True, False, "B",
                 "Uses of auxins",
                 "Auxins help to initiate rooting in stem cuttings, an application widely used for plant propagation. "
                 "Separately, auxins are widely used as herbicides: 2,4-D kills dicotyledonous weeds without affecting "
                 "mature monocotyledonous plants. The herbicide use of 2,4-D is a different application and does not "
                 "explain rooting in cuttings.",
                 ["A: true", "R: true", "R is a different use of auxins"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (auxins)"), secs=30)

assertion_reason(T_PGD, "Plant growth regulators", "Intermediate",
                 "Zeatin is a synthetic cytokinin.",
                 "Kinetin does not occur naturally in plants.",
                 False, True, False, "D",
                 "Natural and synthetic cytokinins",
                 "Kinetin, a modified form of adenine, does not occur naturally in plants. The search for natural "
                 "substances with cytokinin-like activity led to the isolation of zeatin from corn kernels and coconut "
                 "milk, so zeatin is a naturally occurring cytokinin. Several naturally occurring cytokinins and some "
                 "synthetic compounds with cell-division-promoting activity have since been identified.",
                 ["A: false; zeatin is natural", "R: true"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (cytokinins)"), secs=35)

direct(T_PGD, "Plant growth regulators", "Intermediate",
       "Which pair of plant growth regulators, in that order, initiates germination in peanut seeds and inhibits "
       "seed germination?",
       "Ethylene and abscisic acid",
       ["Abscisic acid and ethylene", "Cytokinin and auxin", "Auxin and gibberellin"], "C",
       "PGRs and seed germination",
       "Ethylene breaks seed and bud dormancy and initiates germination in peanut seeds and sprouting of potato tubers. "
       "Abscisic acid acts as a general plant growth inhibitor; it inhibits seed germination and plays an important "
       "role in seed development, maturation and dormancy.",
       ["Initiates germination in peanut: ethylene", "Inhibits seed germination: ABA"],
       why="The second option reverses the roles. NCERT does not describe cytokinins, auxins or gibberellins with "
           "these two effects.",
       ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (ethylene, abscisic acid)"), secs=35)

match_list(T_PGD, "Plant growth regulators", "Intermediate", "plant growth regulator", "effect",
           ["Ethylene", "Abscisic acid", "Auxin", "Cytokinin"],
           ["Helps to produce new chloroplasts in leaves", "Promotes horizontal growth of seedlings and swelling "
            "of the axis", "Controls xylem differentiation", "Increases the tolerance of plants to various stresses"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "D",
           "Effects of plant growth regulators",
           "Ethylene influences horizontal growth of seedlings, swelling of the axis and apical hook formation in dicot "
           "seedlings. ABA increases the tolerance of plants to various kinds of stresses and is therefore called the "
           "stress hormone. Auxins control xylem differentiation and help in cell division. Cytokinins help to produce "
           "new leaves, chloroplasts in leaves, lateral shoot growth and adventitious shoot formation.",
           ["Ethylene → horizontal growth, swelling", "ABA → stress tolerance", "Auxin → xylem differentiation",
            "Cytokinin → new chloroplasts"],
           why="The wrong codes swap ethylene and ABA, auxin and cytokinin, or ethylene and auxin.",
           ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=40)

statement_pair(T_PGD, "Germination and growth phases", "Intermediate",
               "In a root, the phase of maturation lies further away from the apex than the phase of elongation.",
               "Cells in the meristematic phase are large, with large vacuoles and thick secondary walls.",
               True, False, "C",
               "Phases of growth",
               "Moving away from the root apex, one meets the meristematic phase, then the phase of elongation and then "
               "the phase of maturation. Cells in the meristematic phase are rich in protoplasm, possess large "
               "conspicuous nuclei, and have thin, primary, cellulosic walls with abundant plasmodesmatal connections. "
               "Increased vacuolation and cell enlargement characterise the phase of elongation.",
               ["Statement I: true", "Statement II: false; meristematic cells are protoplasm-rich and thin-walled"],
               ncert=ref("PGD", "Growth (phases of growth)"), secs=35)

direct(T_PGD, "Plant growth regulators", "Advanced",
       "Skoog observed that callus from internodal segments of tobacco stems proliferated only if, in addition to "
       "auxins, the medium was supplemented with extracts such as yeast extract, coconut milk or DNA. If such callus is "
       "grown on a medium with auxin alone, the expected result and its explanation are:",
       "the callus fails to proliferate, because a cytokinesis-promoting substance (a cytokinin) is missing",
       ["the callus proliferates normally, because auxin alone promotes cell division in callus",
        "the callus proliferates faster, because coconut milk contains an inhibitor",
        "the callus forms roots at once, because auxins initiate rooting in stem cuttings"], "B",
       "Cytokinins and cell division",
       "F. Skoog and co-workers observed that tobacco callus proliferated only if, in addition to auxins, the medium "
       "contained extracts of vascular tissues, yeast extract, coconut milk or DNA. Skoog and Miller later identified "
       "and crystallised the cytokinesis-promoting active substance, kinetin. Cytokinins have specific effects on "
       "cytokinesis; zeatin, a natural cytokinin, was isolated from coconut milk. Without this factor the callus does "
       "not proliferate.",
       ["Auxin alone → no proliferation", "Extracts supply a cytokinin that promotes cytokinesis"],
       why="Skoog's observation is that auxin alone is not enough. Coconut milk supplies a cytokinin, not an inhibitor. "
           "Rooting of stem cuttings is a different auxin effect and is not what Skoog's callus experiment showed.",
       ncert=ref("PGD", "Plant Growth Regulators (discovery of cytokinins)"), secs=60)

assertion_reason(T_PGD, "Plant growth regulators", "Advanced",
                 "Ethylene promotes senescence and abscission of plant organs, especially of leaves and flowers.",
                 "Ethylene is synthesised only by young, actively dividing tissues.",
                 True, False, False, "C",
                 "Ethylene: source and effects",
                 "Ethylene is a simple gaseous PGR. It is synthesised in large amounts by tissues undergoing senescence "
                 "and by ripening fruits. It promotes senescence and abscission of plant organs, especially of leaves "
                 "and flowers, and is highly effective in fruit ripening.",
                 ["A: true", "R: false; senescing tissues and ripening fruits make it in large amounts"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (ethylene)"), secs=40)

statement_pair(T_PGD, "Plant growth regulators", "Advanced",
               "Auxins and cytokinins have opposite effects on apical dominance.",
               "In most situations, abscisic acid acts as an antagonist to gibberellins.",
               True, True, "A",
               "Interactions between PGRs",
               "The growing apical bud inhibits the growth of lateral buds (apical dominance), a phenomenon NCERT "
               "attributes to auxins; cytokinins help to overcome apical dominance. So the two have opposite effects on "
               "it. In most situations, ABA acts as an antagonist to GAs. NCERT notes that the roles of PGRs in an event "
               "can be complementary or antagonistic.",
               ["Statement I: true (auxin causes, cytokinin overcomes)", "Statement II: true"],
               ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=45)

direct(T_PGD, "Germination and growth phases", "Advanced",
       "Seeds given water and a suitable temperature are kept in a sealed container in which all the air has been "
       "replaced by nitrogen. They fail to grow. Which condition for growth described in NCERT best explains this?",
       "Oxygen helps in releasing the metabolic energy essential for growth activities",
       ["Water provides the turgidity needed for extension growth",
        "Every plant has an optimum temperature range for growth",
        "Light and gravity affect certain phases of growth"], "A",
       "Conditions for growth",
       "NCERT lists water, oxygen and nutrients as very essential elements for growth, along with an optimum "
       "temperature and environmental signals such as light and gravity. Oxygen helps in releasing metabolic energy "
       "essential for growth activities. Here water and temperature are adequate, so the missing oxygen explains the "
       "failure.",
       ["Water and temperature supplied", "No oxygen → no release of metabolic energy → no growth"],
       why="Water and a suitable temperature were provided, and light or gravity is not the variable changed in this "
           "set-up.",
       ncert=ref("PGD", "Growth (conditions for growth)"), secs=45)

# =============================================================== assembly and checks
def check_plan(questions):
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if s["subject"] == BOT)
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    topics = {t["topic"]: t for t in subj["topics"]}
    want = Counter({(t, d): n for t in pkg["topics"] for d, n in topics[t]["quota"].items() if n})
    have = Counter((q["topic"], q["difficulty"]) for q in questions)
    assert have == want, (sorted((want - have).items()), sorted((have - want).items()))
    order = [q["topic"] for q in questions]
    assert order == sorted(order, key=pkg["topics"].index), "topics out of plan order"
    for q in questions:
        assert q["subtopic"] in topics[q["topic"]]["subtopics"], (q["topic"], q["subtopic"])
    lo, hi = (int(x.rsplit("_", 1)[1]) for x in pkg["question_ids"])
    assert hi - lo + 1 == len(questions) == pkg["count"]
    for i, q in enumerate(questions):
        q["question_id"] = f"NEET_BOT_{lo + i:06d}"
    assert pkg["output"] == "batches/parts/BATCH_008_BOT_p1.json"


if __name__ == "__main__":
    check_plan(QUESTIONS)
    n = len(QUESTIONS)
    keys = Counter(q["correct_answer"] for q in QUESTIONS)
    fmts = Counter(q["format"] for q in QUESTIONS)
    assert max(keys.values()) - min(keys.values()) <= 3, keys  # positions are hand-chosen; this only checks them
    for f in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f] >= 0.08 * n, (f, fmts[f])
    assert 0.03 * n <= fmts["numerical"] <= 0.08 * n, fmts["numerical"]
    assert all(q["solution"]["ncert_reference"] for q in QUESTIONS)
    assert len({q["question_text"] for q in QUESTIONS}) == n
    doc = {"schema_version": "1.0", "batch_id": BATCH, "created_at": TODAY,
           "notes": "Package BOT_008_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration, Plant Growth. 130 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
