"""Writes batches/parts/BATCH_006_BOT_p1.json: package BOT_006_p1 of batch 6 (Botany, 122 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_001251 .. NEET_BOT_001372.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books (secondary growth, taxonomical aids, plant life cycles and alternation of generations, early
experiments on photosynthesis) is not used. Facts already tested in batches 1-5 were listed with
`merge_batch.py stems 006 BOT_006_p1` and avoided. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_006/BOT_006_p1.py
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
PLAN = ROOT / "batches" / "plans" / "BATCH_006_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_006_BOT_p1.json"
PACKAGE = "BOT_006_p1"
BATCH = "BATCH_006"
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

CHAPTER = {
    "LW": "The Living World", "BC": "Biological Classification", "PK": "Plant Kingdom",
    "MOR": "Morphology of Flowering Plants", "ANA": "Anatomy of Flowering Plants", "CELL": "Cell: The Unit of Life",
    "CC": "Cell Cycle and Cell Division", "PS": "Photosynthesis in Higher Plants", "RES": "Respiration in Plants",
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


# =============================================================== 1. The Living World and Classification (6/7/6)
direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "NCERT lists four processes that are basic to taxonomy. Which of the following is NOT one of them?",
       "Hybridisation",
       ["Characterisation", "Identification", "Nomenclature"], "C",
       "Processes basic to taxonomy",
       "Based on characteristics, all living organisms can be classified into different taxa; this process is "
       "taxonomy. External and internal structure, the structure of cells, the development process and the "
       "ecological information of organisms are essential and form the basis of modern taxonomic studies. Hence "
       "characterisation, identification, classification and nomenclature are the processes that are basic to "
       "taxonomy. Hybridisation (crossing of organisms) is not one of them.",
       ["Basic processes: characterisation, identification, classification, nomenclature",
        "Hybridisation is not listed"],
       why="Characterisation, identification and nomenclature are all named by NCERT, along with classification, as "
           "processes basic to taxonomy.",
       ncert=ref("LW", "Diversity in the Living World (taxonomy)"), secs=25)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "The order Primata, comprising monkey, gorilla and gibbon, is placed along with the order Carnivora in the "
       "same:",
       "class Mammalia",
       ["family Hominidae", "order Diptera", "phylum Arthropoda"], "A",
       "Order and class",
       "Class includes related orders. NCERT gives the example that the order Primata, comprising animals like "
       "monkey, gorilla and gibbon, is placed in class Mammalia along with the order Carnivora, which includes "
       "animals like tiger, cat and dog. Class Mammalia has other orders also.",
       ["Primata + Carnivora → class Mammalia"],
       why="Hominidae is a family (of man), below the level of order. Diptera is the order of the housefly. "
           "Arthropoda is the phylum of the housefly, not of primates.",
       ncert=ref("LW", "Taxonomic Categories (class)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Amoeboid protozoans live in fresh water, sea water or moist soil. Which of the following is cited by NCERT "
       "as an amoeboid protozoan that is a parasite?",
       "Entamoeba",
       ["Paramoecium", "Euglena", "Gonyaulax"], "D",
       "Amoeboid protozoans",
       "Amoeboid protozoans move and capture their prey by putting out pseudopodia (false feet), as in Amoeba. "
       "Marine forms have silica shells on their surface. Some of them, such as Entamoeba, are parasites.",
       ["Amoeboid protozoans: pseudopodia", "Parasitic example: Entamoeba"],
       why="Paramoecium is a ciliated protozoan. Euglena is a euglenoid and Gonyaulax a dinoflagellate; neither is "
           "an amoeboid protozoan.",
       ncert=ref("BC", "Kingdom Protista (Protozoans)"), secs=20)

direct(T_LIV, "Lichens, viruses and viroids", "Basic",
       "In addition to proteins, viruses contain genetic material. NCERT states that viruses which infect animals "
       "have:",
       "either single- or double-stranded RNA, or double-stranded DNA",
       ["only single-stranded RNA", "both DNA and RNA in the same virus particle",
        "only double-stranded DNA"], "B",
       "Genetic material of viruses",
       "Viruses contain either RNA or DNA; no virus contains both. Viruses that infect plants generally have "
       "single-stranded RNA, and bacteriophages usually have double-stranded DNA. Viruses that infect animals have "
       "either single- or double-stranded RNA or double-stranded DNA.",
       ["Plant viruses → usually ssRNA", "Bacteriophages → usually dsDNA",
        "Animal viruses → ssRNA, dsRNA or dsDNA"],
       why="Only single-stranded RNA describes the viruses that generally infect plants. No virus contains both DNA "
           "and RNA. Animal viruses are not restricted to double-stranded DNA.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=25)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "NCERT explains that 'insects' is a recognisable group that can be given a rank, because its members share "
       "common features such as:",
       "three pairs of jointed legs",
       ["a dorsal hollow neural system", "four pairs of jointed legs", "a body covering of silica plates"], "C",
       "Taxon as a rank",
       "Insects represent a group of organisms sharing common features like three pairs of jointed legs. Such a "
       "group is a recognisable concrete object that can be classified, and it is therefore given a rank or "
       "category.",
       ["Common feature of insects → three pairs of jointed legs"],
       why="A dorsal hollow neural system is a feature of chordates. Insects have three, not four, pairs of legs. "
           "Silica plates are not a feature of insects.",
       ncert=ref("LW", "Taxonomic Categories"), secs=20)

statement_pair(T_LIV, "Taxonomy and hierarchy", "Basic",
               "Nomenclature, or naming, is possible only when an organism is described correctly and we know to "
               "what organism the name is attached; this is identification.",
               "Systematics ignores evolutionary relationships between organisms and is based only on their "
               "external structure.",
               True, False, "C",
               "Identification and systematics",
               "NCERT states that nomenclature or naming is only possible when the organism is described correctly "
               "and we know to what organism the name is attached to; this is identification. Systematics deals "
               "with the kinds of organisms and their diversities and also takes into account the evolutionary "
               "relationships between organisms.",
               ["Statement I: true", "Statement II: false, systematics takes evolutionary relationships into "
                                     "account"],
               ncert=ref("LW", "Diversity in the Living World (identification, systematics)"), secs=35)

match_list(T_LIV, "Taxonomy and hierarchy", "Intermediate", "organism", "family",
           ["Homo sapiens (man)", "Musca domestica (housefly)", "Triticum aestivum (wheat)", "Panthera leo (lion)"],
           ["Poaceae", "Felidae", "Hominidae", "Muscidae"],
           "III IV I II", ["III I IV II", "IV III I II", "III IV II I"], "D",
           "Families in NCERT's examples",
           "In NCERT's table of organisms with their taxonomic categories, man belongs to the family Hominidae, the "
           "housefly to Muscidae and wheat to Poaceae. The genus Panthera, which includes the lion (Panthera leo), "
           "is placed with the genus Felis in the family Felidae.",
           ["Man → Hominidae", "Housefly → Muscidae", "Wheat → Poaceae", "Lion → Felidae"],
           why="Each wrong code swaps at least two families; for example, Poaceae is a plant family and cannot "
               "hold man or the housefly.",
           ncert=ref("LW", "Taxonomic Categories (Table 1.1, family)"), secs=45)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Intermediate",
               "Bacteria are the most abundant micro-organisms, and hundreds of bacteria are present in a handful "
               "of soil.",
               "Mycoplasma includes many forms that are pathogenic in animals and plants.",
               True, True, "A",
               "Bacteria and mycoplasma",
               "NCERT states that bacteria are the most abundant micro-organisms; they occur almost everywhere, and "
               "hundreds of bacteria are present in a handful of soil. Mycoplasma are organisms that completely "
               "lack a cell wall; they are the smallest living cells known, can survive without oxygen, and many "
               "are pathogenic in animals and plants.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("BC", "Kingdom Monera"), secs=35)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "A fungus had long been placed in Deuteromycetes because only its asexual stage was known. Later, it is found "
       "to produce ascospores in asci. Following the practice described in NCERT, this fungus would now be:",
       "moved to Ascomycetes",
       ["kept in Deuteromycetes, because its mycelium is septate", "moved to Phycomycetes",
        "moved to Basidiomycetes"], "A",
       "Imperfect fungi",
       "Deuteromycetes are called imperfect fungi because only their asexual or vegetative phases are known. When "
       "the sexual (perfect) stages of these fungi are discovered, they are often moved to Ascomycetes and "
       "Basidiomycetes. A fungus forming ascospores in asci has the sexual stage of an ascomycete, so it is moved "
       "to Ascomycetes.",
       ["Perfect stage discovered → moved out of Deuteromycetes", "Ascospores in asci → Ascomycetes"],
       why="Once its perfect stage is known the fungus is no longer 'imperfect', so it is not kept in "
           "Deuteromycetes. Phycomycetes form zygospores and Basidiomycetes form basidiospores, not ascospores.",
       ncert=ref("BC", "Kingdom Fungi (Deuteromycetes)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Compared with many other organisms, bacteria as a group show the most extensive metabolic "
                 "diversity.",
                 "The bacteria include photosynthetic autotrophs, chemosynthetic autotrophs and heterotrophs.",
                 True, True, True, "A",
                 "Metabolic diversity of bacteria",
                 "Though the bacterial structure is very simple, bacteria are very complex in behaviour; as a group "
                 "they show the most extensive metabolic diversity. Some bacteria are autotrophic: they are "
                 "photosynthetic (like cyanobacteria) or chemosynthetic (oxidising inorganic substances such as "
                 "nitrates, nitrites and ammonia). The vast majority are heterotrophs. This range of modes of "
                 "nutrition is what their metabolic diversity consists of, so R explains A.",
                 ["A: true", "R: true", "Photosynthetic, chemosynthetic and heterotrophic modes → metabolic "
                                         "diversity → R explains A"],
                 ncert=ref("BC", "Kingdom Monera"), secs=45)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about protozoans are correct?",
                [("All protozoans are heterotrophs and live as predators or parasites.", True),
                 ("Amoeboid protozoans live in fresh water, sea water or moist soil.", True),
                 ("Ciliated protozoans are actively moving organisms because of the presence of thousands of "
                  "cilia.", True),
                 ("Sporozoans have an infectious spore-like stage in their life cycle.", True),
                 ("All flagellated protozoans are free-living.", False)],
                ["abd", "bcde", "ace"], "B",
                "Groups of protozoans",
                "All protozoans are heterotrophs and live as predators or parasites; they are believed to be "
                "primitive relatives of animals. Amoeboid protozoans live in fresh water, sea water or moist soil. "
                "Ciliated protozoans are aquatic, actively moving organisms because of the presence of thousands of "
                "cilia. Sporozoans include diverse organisms that have an infectious spore-like stage in their life "
                "cycle. Flagellated protozoans are either free-living or parasitic, e.g., Trypanosoma, the parasite "
                "that causes sleeping sickness.",
                ["(a), (b), (c), (d): true", "(e): false, flagellates are free-living or parasitic"],
                why="Every wrong combination either leaves out a true statement or includes (e).",
                ncert=ref("BC", "Kingdom Protista (Protozoans)"), secs=60)

assertion_reason(T_LIV, "Binomial nomenclature", "Intermediate",
                 "When a biological name is handwritten, the generic name and the specific epithet are underlined "
                 "separately.",
                 "The separate underlining (or printing in italics) indicates the Latin origin of the two words.",
                 True, True, True, "A",
                 "Writing scientific names",
                 "Biological names are generally in Latin and written in italics; they are Latinised or derived "
                 "from Latin irrespective of their origin. Both the words in a biological name, when handwritten, "
                 "are separately underlined, or printed in italics, to indicate their Latin origin. So the purpose "
                 "stated in R is the reason for the practice in A.",
                 ["A: true", "R: true", "Underlining/italics shows Latin origin → R explains A"],
                 ncert=ref("LW", "Diversity in the Living World (binomial nomenclature)"), secs=40)

direct(T_LIV, "What is living", "Intermediate",
       "According to NCERT, the twin characteristics of growth are:",
       "increase in mass and increase in number of individuals",
       ["increase in mass and accumulation of material on the surface",
        "cell division and response to stimuli",
        "increase in height and metabolism"], "C",
       "Growth as a feature of living organisms",
       "All living organisms grow. Increase in mass and increase in number of individuals are the twin "
       "characteristics of growth. A multicellular organism grows by cell division; in unicellular organisms "
       "growth by cell division also increases the number of individuals.",
       ["Twin characteristics: increase in mass + increase in number of individuals"],
       why="Accumulation of material on the surface is how non-living objects such as sand mounds 'grow'. Response "
           "to stimuli and metabolism are separate features of living organisms, not the characteristics of growth.",
       ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=25)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following statements about systems of classification are correct?",
                [("The main criteria used by Whittaker include cell structure, body organisation, mode of "
                  "nutrition, reproduction and phylogenetic relationships.", True),
                 ("The three-domain system divides kingdom Monera into two domains.", True),
                 ("In the three-domain system, the remaining eukaryotic kingdoms are placed in the third domain.",
                  True),
                 ("The three-domain system reduces the number of kingdoms to three.", False),
                 ("Fungi were given a separate kingdom by Whittaker mainly because they are prokaryotic.", False)],
                ["abd", "abcd", "bce"], "C",
                "Five kingdom and three-domain systems",
                "Whittaker's main criteria for classification include cell structure, body organisation, mode of "
                "nutrition, reproduction and phylogenetic relationships. The three-domain system divides kingdom "
                "Monera into two domains, leaving the remaining eukaryotic kingdoms in the third domain, thereby "
                "giving a six kingdom classification. Fungi are eukaryotic; Monera is the only prokaryotic kingdom.",
                ["(a), (b), (c): true", "(d): false, the three-domain system gives six kingdoms",
                 "(e): false, fungi are eukaryotes"],
                why="Any combination containing (d) or (e) is wrong, and one leaving out (c) is incomplete.",
                ncert=ref("BC", "Introduction (five kingdom and three-domain systems)"), secs=60)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Methanogens are responsible for the production of methane (biogas) from the dung of ruminant "
                 "animals.",
                 "Methanogens are photosynthetic archaebacteria that live mainly in hot springs.",
                 True, False, False, "C",
                 "Methanogens",
                 "Methanogens are archaebacteria present in marshy areas and in the gut of several ruminant animals "
                 "such as cows and buffaloes, and they are responsible for the production of methane (biogas) from "
                 "the dung of these animals. Hot springs are the habitat of thermoacidophiles, and methanogens are "
                 "not photosynthetic.",
                 ["A: true", "R: false, methanogens live in marshes and the ruminant gut; thermoacidophiles live in "
                             "hot springs"],
                 ncert=ref("BC", "Kingdom Monera (Archaebacteria)"), secs=40)

match_list(T_LIV, "Taxonomy and hierarchy", "Advanced", "taxonomic category", "description in NCERT",
           ["Genus", "Family", "Order", "Phylum"],
           ["An assemblage of families that exhibit a few similar characters",
            "Characterised on the basis of both vegetative and reproductive features of plant species",
            "A group of related species with more characters in common than with species of other genera",
            "Classes comprising animals like fishes, amphibians, reptiles, birds and mammals"],
           "III II I IV", ["II III I IV", "III I II IV", "I II III IV"], "B",
           "Definitions of taxonomic categories",
           "Genus comprises a group of related species which has more characters in common in comparison to species "
           "of other genera. Family has a group of related genera with still less number of similarities as compared "
           "to genus and species; families are characterised on the basis of both vegetative and reproductive "
           "features of plant species. Order is an assemblage of families which exhibit a few similar characters. "
           "Classes comprising animals like fishes, amphibians, reptiles, birds along with mammals constitute the "
           "next higher category, phylum.",
           ["Genus → related species", "Family → vegetative and reproductive features",
            "Order → assemblage of families", "Phylum → group of classes (fishes ... mammals)"],
           why="The wrong codes interchange genus, family and order, whose descriptions differ in the rank of the "
               "units grouped.",
           ncert=ref("LW", "Taxonomic Categories"), secs=60)

direct(T_LIV, "Five kingdom classification", "Advanced",
       "In Whittaker's table of the characteristics of the five kingdoms, the body organisation described as "
       "'multicellular/loose tissue' belongs to kingdom:",
       "Fungi",
       ["Protista", "Plantae", "Animalia"], "D",
       "Body organisation in the five kingdoms",
       "In the table of characteristics of the five kingdoms, the body organisation is cellular in Monera and "
       "Protista, multicellular/loose tissue in Fungi, tissue/organ in Plantae and tissue/organ/organ system in "
       "Animalia.",
       ["Monera, Protista → cellular", "Fungi → multicellular/loose tissue", "Plantae → tissue/organ",
        "Animalia → tissue/organ/organ system"],
       why="Protista is cellular, Plantae tissue/organ and Animalia tissue/organ/organ system in the table.",
       ncert=ref("BC", "Introduction (Table 2.1, characteristics of the five kingdoms)"), secs=40)

statement_pair(T_LIV, "Lichens, viruses and viroids", "Advanced",
               "Viruses are nucleoproteins, and their genetic material is infectious.",
               "The infectious agent discovered by T.O. Diener in 1971 was a protein that lacked any nucleic acid.",
               True, False, "C",
               "Viruses and viroids",
               "NCERT states that viruses are nucleoproteins and the genetic material is infectious. In 1971, T.O. "
               "Diener discovered a new infectious agent that was smaller than viruses and caused potato spindle "
               "tuber disease. It was found to be a free RNA, lacking the protein coat seen in viruses, and was "
               "named viroid. An infectious agent made of abnormally folded protein is a prion, not Diener's viroid.",
               ["Statement I: true", "Statement II: false, Diener's viroid is a free RNA without a protein coat"],
               ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=45)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Fungi grow best in cold and dry places, which is why food is stored in a refrigerator.",
                 "Food is kept in a refrigerator to prevent it from going bad due to bacterial or fungal infections.",
                 False, True, False, "D",
                 "Conditions for fungal growth",
                 "Fungi prefer to grow in warm and humid places. NCERT asks why we keep food in the refrigerator and "
                 "answers that it is to prevent food from going bad due to bacterial or fungal infections; the cold "
                 "slows their growth. A is false because fungi grow best in warm, humid conditions, not cold, dry "
                 "ones.",
                 ["A: false, fungi prefer warm and humid places", "R: true"],
                 ncert=ref("BC", "Kingdom Fungi"), secs=40)


# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "Which of the following descriptions of algae is given by NCERT?",
       "Chlorophyll-bearing, simple, thalloid, autotrophic and largely aquatic organisms",
       ["Chlorophyll-bearing, vascular, autotrophic and largely terrestrial organisms",
        "Simple, thalloid, heterotrophic organisms with a cell wall of chitin",
        "Plants whose main body is a sporophyte differentiated into root, stem and leaves"], "A",
       "Characteristics of algae",
       "Algae are chlorophyll-bearing, simple, thalloid, autotrophic and largely aquatic (both fresh water and "
       "marine) organisms. They also occur in a variety of other habitats such as moist stones, soils and wood.",
       ["Algae: chlorophyll-bearing, simple, thalloid, autotrophic, largely aquatic"],
       why="Algae have no vascular tissue and are largely aquatic. A heterotrophic body with a chitin wall describes "
           "fungi. A sporophyte with root, stem and leaves describes pteridophytes.",
       ncert=ref("PK", "Algae"), secs=20)

direct(T_PK, "Algae", "Basic",
       "In isogamous sexual reproduction, the fusing gametes are similar in size. In which alga are such gametes "
       "flagellated, according to NCERT?",
       "Chlamydomonas",
       ["Spirogyra", "Volvox", "Fucus"], "B",
       "Isogamy in algae",
       "Fusion of two gametes similar in size is called isogamous. Such gametes can be flagellated and similar in "
       "size, as in Chlamydomonas, or non-flagellated (non-motile) but similar in size, as in Spirogyra. Volvox and "
       "Fucus are oogamous.",
       ["Isogamy with flagellated gametes → Chlamydomonas", "Isogamy with non-motile gametes → Spirogyra"],
       why="Spirogyra shows isogamy with non-flagellated gametes. Volvox and Fucus show oogamy, a large non-motile "
           "female gamete fusing with a smaller motile male gamete.",
       ncert=ref("PK", "Algae (sexual reproduction)"), secs=25)

direct(T_PK, "Bryophytes", "Basic",
       "Compared with the algae, the plant body of bryophytes is described by NCERT as:",
       "more differentiated, thallus-like and prostrate or erect, attached to the substratum by rhizoids",
       ["differentiated into true roots, stem and leaves with vascular tissue",
        "a diploid sporophyte bearing sporangia on sporophylls",
        "always unicellular or colonial and free-floating"], "D",
       "Plant body of bryophytes",
       "The plant body of bryophytes is more differentiated than that of algae. It is thallus-like and prostrate or "
       "erect, and attached to the substratum by unicellular or multicellular rhizoids. Bryophytes lack true roots, "
       "stem or leaves, though they may possess root-like, leaf-like or stem-like structures.",
       ["More differentiated than algae", "Thallus-like; prostrate or erect; rhizoids"],
       why="True roots, stem and leaves with vascular tissue and sporangia on sporophylls belong to the sporophyte "
           "of pteridophytes. A unicellular or colonial free-floating body describes some algae.",
       ncert=ref("PK", "Bryophytes"), secs=25)

direct(T_PK, "Bryophytes", "Basic",
       "In mosses, the leafy stage of the gametophyte develops:",
       "from the secondary protonema as a lateral bud",
       ["from the capsule of the sporophyte after meiosis", "directly from the zygote",
        "from gemmae formed in gemma cups"], "C",
       "Gametophyte of mosses",
       "The predominant stage of the life cycle of a moss is the gametophyte, which consists of two stages. The "
       "first stage is the protonema, which develops directly from a spore. The second stage is the leafy stage, "
       "which develops from the secondary protonema as a lateral bud and bears the sex organs.",
       ["Spore → protonema", "Secondary protonema → lateral bud → leafy stage"],
       why="The capsule produces spores, not leafy shoots. The zygote forms the sporophyte. Gemmae in gemma cups are "
           "the asexual buds of liverworts.",
       ncert=ref("PK", "Bryophytes (mosses)"), secs=25)

statement_pair(T_PK, "Gymnosperms", "Basic",
               "Gymnosperms include medium-sized trees or tall trees and shrubs.",
               "The roots of gymnosperms are generally adventitious roots.",
               True, False, "C",
               "Gymnosperm habit and roots",
               "The gymnosperms include medium-sized trees or tall trees and shrubs; the giant redwood tree Sequoia "
               "is one of the tallest tree species. The roots are generally tap roots. Roots in some genera have a "
               "fungal association (mycorrhiza), as in Pinus, while some, like those of Cycas, have small "
               "specialised coralloid roots.",
               ["Statement I: true", "Statement II: false, gymnosperms generally have tap roots"],
               ncert=ref("PK", "Gymnosperms"), secs=30)

match_list(T_PK, "Algae", "Intermediate", "feature", "group",
           ["Stored food is floridean starch", "Stored food is mannitol or laminarin",
            "Two to eight equal, apical flagella", "Antheridium produces biflagellate antherozoids"],
           ["Bryophytes", "Chlorophyceae", "Phaeophyceae", "Rhodophyceae"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "A",
           "Distinguishing features of plant groups",
           "From NCERT's table of the classes of algae: Rhodophyceae store floridean starch; Phaeophyceae store "
           "mannitol and laminarin; Chlorophyceae have 2-8 equal, apical flagella (Phaeophyceae have 2 unequal "
           "lateral flagella and Rhodophyceae have none). In bryophytes, the male sex organ, the antheridium, "
           "produces biflagellate antherozoids.",
           ["Floridean starch → Rhodophyceae", "Mannitol/laminarin → Phaeophyceae",
            "2–8 equal apical flagella → Chlorophyceae", "Biflagellate antherozoids → bryophytes"],
           why="The wrong codes swap the stored foods of red and brown algae or give the green-algal flagella to "
               "bryophytes.",
           ncert=ref("PK", "Algae (Table 3.1); Bryophytes"), secs=45)

assertion_reason(T_PK, "Bryophytes", "Intermediate",
                 "The sporophyte of a bryophyte is not free-living.",
                 "The sporophyte remains attached to the photosynthetic gametophyte and derives nourishment from it.",
                 True, True, True, "A",
                 "Sporophyte of bryophytes",
                 "In bryophytes the zygote produces a multicellular body called a sporophyte. The sporophyte is not "
                 "free-living but attached to the photosynthetic gametophyte and derives nourishment from it. "
                 "Because it depends on the gametophyte for its nourishment, it cannot live independently: R "
                 "explains A.",
                 ["A: true", "R: true", "Dependence on the gametophyte for nourishment → not free-living"],
                 ncert=ref("PK", "Bryophytes"), secs=40)

multi_statement(T_PK, "Pteridophytes", "Intermediate",
                "Which of the following structures are haploid?",
                [("The protonema of a moss", True),
                 ("The prothallus of a fern", True),
                 ("The capsule of a moss", False),
                 ("The pollen grain of a gymnosperm", True),
                 ("The nucellus of a gymnosperm ovule", False)],
                ["abc", "bde", "ade"], "B",
                "Gametophytic and sporophytic structures",
                "The protonema develops directly from a haploid spore and is part of the moss gametophyte. The "
                "prothallus of pteridophytes develops from a spore and is the gametophyte. The pollen grain of a "
                "gymnosperm is the highly reduced male gametophyte. The capsule is part of the moss sporophyte "
                "(foot, seta and capsule) and is diploid; meiosis occurs in it to form spores. The nucellus is part "
                "of the ovule of the diploid sporophyte, and its megaspore mother cell divides by meiosis.",
                ["Haploid (gametophytic): protonema, prothallus, pollen grain",
                 "Diploid (sporophytic): moss capsule, nucellus"],
                why="Any combination containing (c) or (e) includes a sporophytic, diploid structure.",
                ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

assertion_reason(T_PK, "Bryophytes", "Intermediate",
                 "In liverworts, gemmae are formed by meiosis.",
                 "Gemmae become detached from the parent body and germinate to form new individuals.",
                 False, True, False, "D",
                 "Gemmae",
                 "Liverworts reproduce asexually by fragmentation of thalli or by the formation of specialised "
                 "structures called gemmae. Gemmae are green, multicellular, asexual buds that develop in small "
                 "receptacles called gemma cups on the thalli. Being asexual buds, they are not formed by meiosis. "
                 "They become detached from the parent body and germinate to form new individuals.",
                 ["A: false, gemmae are asexual buds", "R: true"],
                 ncert=ref("PK", "Bryophytes (liverworts)"), secs=40)

statement_pair(T_PK, "Pteridophytes", "Intermediate",
               "Unlike in bryophytes, the main plant body in pteridophytes is a sporophyte.",
               "Unlike in bryophytes, the gametophyte of pteridophytes is not free-living.",
               True, False, "C",
               "Bryophytes versus pteridophytes",
               "In bryophytes the main plant body is the haploid gametophyte, while in pteridophytes the main plant "
               "body is a sporophyte differentiated into true root, stem and leaves. In both groups the gametophyte "
               "is free-living: the pteridophyte spores germinate to give inconspicuous, small but multicellular, "
               "free-living, mostly photosynthetic thalloid gametophytes called prothallus.",
               ["Statement I: true", "Statement II: false, the prothallus is free-living"],
               ncert=ref("PK", "Bryophytes; Pteridophytes"), secs=35)

direct(T_PK, "Gymnosperms", "Intermediate",
       "A plant has true roots, stem and leaves with vascular tissue. Its ovules are borne on megasporophylls and are "
       "not enclosed in an ovary, its stem is unbranched, and some of its roots are coralloid roots associated with "
       "nitrogen-fixing cyanobacteria. The plant is most likely:",
       "Cycas",
       ["Pinus", "Selaginella", "Cedrus"], "B",
       "Identifying a gymnosperm",
       "Naked ovules on megasporophylls mark a gymnosperm. Among gymnosperms, Cycas has an unbranched stem and "
       "small specialised coralloid roots associated with nitrogen-fixing cyanobacteria, whereas Pinus and Cedrus "
       "have branched stems.",
       ["Naked ovules → gymnosperm", "Unbranched stem + coralloid roots → Cycas"],
       why="Pinus and Cedrus are gymnosperms with branched stems; Pinus roots have mycorrhiza. Selaginella is a "
           "pteridophyte and has no ovules.",
       ncert=ref("PK", "Gymnosperms"), secs=40)

direct(T_PK, "Algae", "Intermediate",
       "Asexual reproduction in most brown algae takes place by:",
       "biflagellate zoospores that are pear-shaped and have two unequal, laterally attached flagella",
       ["non-motile spores and non-motile gametes", "zoospores with two to eight equal, apical flagella",
        "fragmentation alone, since spores are never formed"], "D",
       "Asexual reproduction in Phaeophyceae",
       "Vegetative reproduction in brown algae takes place by fragmentation. Asexual reproduction in most brown "
       "algae is by biflagellate zoospores that are pear-shaped and have two unequal, laterally attached flagella.",
       ["Brown algae: zoospores pyriform, two unequal lateral flagella"],
       why="Non-motile spores and gametes are typical of red algae. Two to eight equal apical flagella are typical "
           "of green algae. Brown algae do form zoospores.",
       ncert=ref("PK", "Algae (Phaeophyceae)"), secs=30)

multi_statement(T_PK, "Gymnosperms", "Advanced",
                "Which of the following statements comparing pteridophytes and gymnosperms are correct?",
                [("In both groups the main plant body is a sporophyte.", True),
                 ("Compact strobili (cones) are formed in some pteridophytes as well as in gymnosperms.", True),
                 ("Heterospory is found in gymnosperms and in some pteridophytes.", True),
                 ("Like pteridophytes, gymnosperms have a free-living gametophyte.", False),
                 ("Archegonia are formed in pteridophytes but not in gymnosperms.", False)],
                ["abd", "bce", "abcd"], "D",
                "Pteridophytes and gymnosperms compared",
                "In both groups the main plant body is a sporophyte. In some pteridophytes (Selaginella, Equisetum) "
                "the sporophylls form compact strobili or cones, and in gymnosperms the sporophylls are arranged "
                "spirally to form lax or compact cones. Gymnosperms are heterosporous, as are some pteridophytes "
                "such as Selaginella and Salvinia. The gymnosperm gametophytes are not free-living; they remain "
                "within the sporangia on the sporophyte. The female gametophyte of gymnosperms bears two or more "
                "archegonia.",
                ["(a), (b), (c): true", "(d): false, gymnosperm gametophytes are not free-living",
                 "(e): false, gymnosperms also have archegonia"],
                why="Each wrong combination contains (d) or (e), or leaves out a true statement.",
                ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=60)

assertion_reason(T_PK, "Pteridophytes", "Advanced",
                 "Selaginella is a heterosporous pteridophyte.",
                 "In Selaginella, the sporophylls are compactly arranged to form strobili.",
                 True, True, False, "B",
                 "Heterospory and strobili",
                 "Selaginella produces two kinds of spores, macro (large) and micro (small) spores, so it is "
                 "heterosporous. Separately, its sporophylls form distinct compact structures called strobili or "
                 "cones. Equisetum also forms strobili but is not cited as heterosporous, so the arrangement of "
                 "sporophylls into strobili is not the reason for heterospory.",
                 ["A: true", "R: true", "Strobilus formation does not explain the production of two kinds of "
                                        "spores"],
                 ncert=ref("PK", "Pteridophytes"), secs=45)

statement_pair(T_PK, "Algae", "Advanced",
               "Chlorophyll a is present in members of both Chlorophyceae and Rhodophyceae.",
               "Chlorophyll d is present in members of both Phaeophyceae and Rhodophyceae.",
               True, False, "C",
               "Pigments of algae",
               "From NCERT's table: Chlorophyceae have chlorophyll a and b; Phaeophyceae have chlorophyll a and c and "
               "fucoxanthin; Rhodophyceae have chlorophyll a and d and phycoerythrin. Chlorophyll a is common to all "
               "three classes, but chlorophyll d is found only in Rhodophyceae.",
               ["Statement I: true", "Statement II: false, Phaeophyceae have chlorophyll c, not d"],
               ncert=ref("PK", "Algae (Table 3.1)"), secs=40)

direct(T_PK, "Algae", "Advanced",
       "An alga has chlorophyll a and d with a predominance of phycoerythrin, stores floridean starch, lacks "
       "flagella and reproduces asexually by non-motile spores. The alga is:",
       "Porphyra",
       ["Laminaria", "Chara", "Ectocarpus"], "A",
       "Identifying a red alga",
       "Chlorophyll a and d, phycoerythrin, floridean starch, absence of flagella and non-motile spores are features "
       "of Rhodophyceae. Porphyra is one of NCERT's examples of red algae (with Polysiphonia, Gracilaria and "
       "Gelidium).",
       ["Features → Rhodophyceae", "Red alga among options → Porphyra"],
       why="Laminaria and Ectocarpus are brown algae (chlorophyll a and c, fucoxanthin, mannitol/laminarin, "
           "flagellated zoospores). Chara is a green alga.",
       ncert=ref("PK", "Algae (Rhodophyceae)"), secs=40)

match_list(T_PK, "Gymnosperms", "Advanced", "plant", "feature",
           ["Pinus", "Cycas", "Selaginella", "Marchantia"],
           ["Asexual reproduction by gemmae formed in gemma cups",
            "Roots with a fungal association in the form of mycorrhiza",
            "Female gametophyte retained on the parent sporophyte for a variable period",
            "Small specialised coralloid roots associated with nitrogen-fixing cyanobacteria"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "Features of plants of different groups",
           "In Pinus the roots have a fungal association (mycorrhiza), while Cycas has coralloid roots associated "
           "with nitrogen-fixing cyanobacteria. In heterosporous Selaginella the female gametophyte is retained on "
           "the parent sporophyte for a variable period. Marchantia, a liverwort, reproduces asexually by gemmae "
           "formed in gemma cups.",
           ["Pinus → mycorrhiza", "Cycas → coralloid roots", "Selaginella → retained female gametophyte",
            "Marchantia → gemmae"],
           why="The wrong codes swap the roots of Pinus and Cycas, or give gemmae to a vascular plant.",
           ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=50)


# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Inflorescence", "Basic",
       "When a shoot tip transforms into a flower, the flower is always:",
       "solitary",
       ["borne in a racemose inflorescence", "borne in a cymose inflorescence", "unisexual"], "D",
       "Inflorescence and solitary flowers",
       "A flower is a modified shoot in which the shoot apical meristem changes to a floral meristem. The "
       "arrangement of flowers on the floral axis is the inflorescence. NCERT states that when a shoot tip "
       "transforms into a flower, it is always solitary.",
       ["Shoot tip becomes a flower → solitary flower"],
       why="Racemose and cymose are kinds of inflorescence, i.e., arrangements of many flowers on a floral axis. A "
           "solitary flower may be bisexual or unisexual; nothing makes it always unisexual.",
       ncert=ref("MOR", "The Inflorescence"), secs=20)

direct(T_MOR, "Plant families", "Basic",
       "In the floral diagram of a flower, the position of the mother axis with respect to the flower is "
       "represented by:",
       "a dot on the top of the floral diagram",
       ["a line drawn above the symbol of the ovary", "the symbol ⊕ at the centre of the diagram",
        "brackets drawn around the outermost whorl"], "A",
       "Floral diagram",
       "A floral diagram provides information about the number of parts of a flower, their arrangement and the "
       "relation they have with one another. The position of the mother axis with respect to the flower is "
       "represented by a dot on the top of the floral diagram. Calyx, corolla, androecium and gynoecium are drawn "
       "in successive whorls, calyx being the outermost and gynoecium in the centre.",
       ["Mother axis → dot at the top of the floral diagram"],
       why="Lines over the ovary symbol and brackets belong to the floral formula (position of ovary, fusion). ⊕ is "
           "the floral-formula symbol for an actinomorphic flower.",
       ncert=ref("MOR", "Description of Some Important Families (floral diagram)"), secs=25)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "The veins of a leaf:",
       "provide rigidity to the leaf blade and act as channels of transport for water, minerals and food",
       ["arise directly from the root apical meristem and store food",
        "are found only in compound leaves",
        "carry out gaseous exchange through their open ends"], "B",
       "Veins of the leaf",
       "The lamina, or leaf blade, is the green expanded part of the leaf with veins and veinlets. There is usually "
       "a middle prominent vein, the midrib. Veins provide rigidity to the leaf blade and act as channels of "
       "transport for water, minerals and food materials.",
       ["Veins: rigidity + transport of water, minerals and food"],
       why="Leaves arise from the shoot apical meristem, not the root apex. Veins are present in simple leaves too. "
           "Gaseous exchange takes place through stomata, not through veins.",
       ncert=ref("MOR", "The Leaf"), secs=20)

direct(T_MOR, "Fruit and seed", "Basic",
       "Generally, monocotyledonous seeds are endospermic. NCERT names which of the following as monocots whose "
       "seeds are non-endospermic?",
       "Orchids",
       ["Maize", "Wheat", "Onion"], "C",
       "Endosperm in monocot seeds",
       "Generally monocotyledonous seeds are endospermic, but some, as in orchids, are non-endospermic. In cereals "
       "such as maize the endosperm is bulky and stores food.",
       ["Monocot seeds: generally endospermic", "Exception named: orchids"],
       why="Maize and wheat are cereals with a bulky endosperm. Onion belongs to Liliaceae, whose seeds are "
           "endospermous.",
       ncert=ref("MOR", "The Seed (structure of a monocotyledonous seed)"), secs=20)

statement_pair(T_MOR, "Root, stem and leaf", "Basic",
               "In jasmine, a slender lateral branch arises from the base of the main axis, grows aerially for some "
               "time and then arches downwards to touch the ground.",
               "The tendrils of pea are modified stems.",
               True, False, "C",
               "Stem and leaf modifications",
               "In some plants such as mint and jasmine, a slender lateral branch arises from the base of the main "
               "axis and, after growing aerially for some time, arches downwards to touch the ground. The tendrils "
               "of pea are modified leaves (leaves modified into tendrils for climbing); stem tendrils, which "
               "develop from axillary buds, are found in gourds and grapevines.",
               ["Statement I: true", "Statement II: false, pea tendrils are modified leaves"],
               ncert=ref("MOR", "The Stem (modifications); The Leaf (modifications)"), secs=30)

match_list(T_MOR, "Flower", "Intermediate", "plant", "type of placentation",
           ["Tomato", "Primrose", "Sunflower", "Mustard"],
           ["Parietal", "Axile", "Free central", "Basal"],
           "II III IV I", ["III II IV I", "II III I IV", "II IV III I"], "B",
           "Placentation",
           "In axile placentation the placenta is axial and the ovules are attached to it in a multilocular ovary, "
           "as in china rose, tomato and lemon. In free central placentation the ovules are borne on a central axis "
           "and septa are absent, as in Dianthus and Primrose. In basal placentation the placenta develops at the "
           "base of the ovary and a single ovule is attached to it, as in sunflower and marigold. In parietal "
           "placentation the ovules develop on the inner wall of the ovary, as in mustard and Argemone.",
           ["Tomato → axile", "Primrose → free central", "Sunflower → basal", "Mustard → parietal"],
           why="The wrong codes interchange axile with free central, or basal with parietal.",
           ncert=ref("MOR", "The Flower (gynoecium, placentation)"), secs=45)

assertion_reason(T_MOR, "Inflorescence", "Intermediate",
                 "In a cymose inflorescence, the flowers are borne in a basipetal order, with the oldest flower at "
                 "the tip of the main axis.",
                 "In a cymose inflorescence, the main axis first ends in a flower and so cannot grow further; every "
                 "later flower can therefore arise only below that terminal flower.",
                 True, True, True, "A",
                 "Cymose inflorescence",
                 "In the cymose type of inflorescence the main axis terminates in a flower, hence it is limited in "
                 "growth, and the flowers are borne in a basipetal order. Because the apex of the axis is used up "
                 "by the first (terminal) flower, each later flower has to develop lower down the axis. So the "
                 "oldest flower is at the tip and younger ones lie below it: R gives the cause of A.",
                 ["A: true", "R: true", "Apex used up by the first flower → later flowers only below → basipetal"],
                 ncert=ref("MOR", "The Inflorescence"), secs=40)

statement_pair(T_MOR, "Flower", "Intermediate",
               "A calyx in which the sepals are free from one another is called gamosepalous.",
               "The petals of a corolla may be free (polypetalous) or united (gamopetalous).",
               False, True, "D",
               "Calyx and corolla",
               "The calyx may be gamosepalous (sepals united) or polysepalous (sepals free). Similarly, the corolla "
               "may be gamopetalous (petals united) or polypetalous (petals free).",
               ["Statement I: false, free sepals = polysepalous", "Statement II: true"],
               ncert=ref("MOR", "The Flower (calyx, corolla)"), secs=30)

direct(T_MOR, "Plant families", "Intermediate",
       "The floral formula ⊕ ⚥ K(5) C(5) A5 G(2), in which the corolla and androecium are joined by a line "
       "(epipetalous stamens) and the ovary is superior, represents a flower of the family:",
       "Solanaceae",
       ["Liliaceae", "Fabaceae", "Poaceae"], "D",
       "Floral formula of Solanaceae",
       "Solanaceae flowers are bisexual and actinomorphic, with five united sepals, five united petals, five "
       "epipetalous stamens and a bicarpellary, syncarpous, superior ovary: ⊕ ⚥ K(5) C(5) A5 G(2).",
       ["⊕ ⚥, K(5) C(5), epipetalous A5, G(2) → Solanaceae"],
       why="Liliaceae has a perianth P(3+3), A3+3 and G(3). Fabaceae is zygomorphic with A(9)+1 and G1. Poaceae is "
           "not described by this formula.",
       ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=35)

multi_statement(T_MOR, "Root, stem and leaf", "Intermediate",
                "Which of the following statements about modifications of the stem and leaf are correct?",
                [("The underground stems of potato, ginger, turmeric, zaminkand and Colocasia are modified to store "
                  "food.", True),
                 ("These underground stems also act as organs of perennation to tide over conditions unfavourable "
                  "for growth.", True),
                 ("Banana and pineapple propagate vegetatively by suckers.", True),
                 ("In Opuntia, the leaves are modified into flattened green structures that photosynthesise.",
                  False),
                 ("In Australian acacia, the stem is modified into a flattened, green, leaf-like structure.",
                  False)],
                ["abd", "bce", "acde"], "D",
                "Modifications of stem and leaf",
                "Underground stems of potato, ginger, turmeric, zaminkand and Colocasia are modified to store food; "
                "they also act as organs of perennation. Sub-aerial suckers, lateral branches from the basal and "
                "underground portion of the main stem, occur in banana, pineapple and Chrysanthemum. Opuntia has a "
                "flattened green stem (its leaves are spines). In Australian acacia the leaves are small and "
                "short-lived and the petioles expand, become green and synthesise food.",
                ["(a), (b), (c): true", "(d): false, Opuntia's flattened organ is the stem",
                 "(e): false, in Australian acacia the petiole is modified"],
                why="Every wrong combination contains (d) or (e), or leaves out a true statement.",
                ncert=ref("MOR", "The Stem (modifications); The Leaf (modifications)"), secs=60)

direct(T_MOR, "Root, stem and leaf", "Intermediate",
       "In a root, the region of meristematic activity is located:",
       "a few millimetres above the root cap",
       ["at the base of the root, near the stem", "within the region of maturation, among the root hairs",
        "above the region of elongation"], "D",
       "Regions of the root",
       "The apex of the root is covered by a thimble-like structure, the root cap. A few millimetres above the root "
       "cap is the region of meristematic activity, whose small, thin-walled cells with dense protoplasm divide "
       "repeatedly. Proximal to it lies the region of elongation, and further proximal, the region of maturation, "
       "from some of whose epidermal cells the root hairs arise.",
       ["Root cap → meristematic region → elongation → maturation"],
       why="The meristematic region is near the tip, below (distal to) the region of elongation; the region of "
           "maturation with root hairs lies further back.",
       ncert=ref("MOR", "The Root (regions of the root)"), secs=30)

assertion_reason(T_MOR, "Root, stem and leaf", "Intermediate",
                 "Gourds such as cucumber, pumpkins and watermelon climb with the help of tendrils.",
                 "In Citrus and Bougainvillea, axillary buds of stems are modified into woody, straight and pointed "
                 "thorns that protect the plants from browsing animals.",
                 True, True, False, "B",
                 "Stem modifications",
                 "Stem tendrils, which develop from axillary buds, are slender and spirally coiled and help plants "
                 "to climb, as in gourds (cucumber, pumpkins, watermelon) and grapevines. Separately, in Citrus and "
                 "Bougainvillea the axillary buds of stems are modified into woody, straight and pointed thorns that "
                 "protect the plants from browsing animals. R is true but concerns thorns of other plants and a "
                 "protective function, so it does not explain why gourds climb.",
                 ["A: true", "R: true", "R is about thorns (protection) in other plants → not the explanation of A"],
                 ncert=ref("MOR", "The Stem (modifications)"), secs=40)

statement_pair(T_MOR, "Flower", "Advanced",
               "Stamens of a flower may be united with other members, such as petals, or among themselves.",
               "In the family Solanaceae, the stamens are united among themselves into one bundle (monoadelphous).",
               True, False, "C",
               "Union of stamens",
               "The stamens of a flower may be united with other members such as petals (epipetalous, as in brinjal) "
               "or among themselves (into one bundle, monoadelphous as in china rose; two bundles, diadelphous as in "
               "pea; or more, polyadelphous as in citrus). In Solanaceae the five stamens are epipetalous, attached "
               "to the petals, not united among themselves.",
               ["Statement I: true", "Statement II: false, Solanaceae stamens are epipetalous"],
               ncert=ref("MOR", "The Flower (androecium); Solanaceae"), secs=40)

multi_statement(T_MOR, "Plant families", "Advanced",
                "A flower has the floral formula Br ⊕ ⚥ P(3+3) A3+3 G(3), with the ovary superior and the stamens "
                "joined to the perianth. Which conclusions about this flower are correct?",
                [("The flower is bracteate.", True),
                 ("The flower is actinomorphic and bisexual.", True),
                 ("Its calyx and corolla are not distinct, and the six tepals are united.", True),
                 ("The gynoecium is tricarpellary and syncarpous.", True),
                 ("The six stamens are united among themselves into one bundle.", False)],
                ["abce", "bcd", "acd"], "A",
                "Reading a floral formula",
                "Br means bracteate; ⊕ means actinomorphic and ⚥ bisexual. P(3+3) shows a perianth of six tepals in "
                "two whorls of three, the brackets showing fusion. A3+3 has no brackets, so the six stamens are free "
                "from one another (the line joining them to P shows that they are epiphyllous). G(3) is a "
                "tricarpellary, syncarpous gynoecium. This is the formula of Liliaceae.",
                ["Br → bracteate; ⊕ ⚥ → actinomorphic, bisexual", "P(3+3) → united tepals",
                 "A3+3 without brackets → stamens free", "G(3) → tricarpellary, syncarpous"],
                why="(e) is false because A3+3 is not enclosed in brackets; the other wrong options leave out true "
                    "conclusions.",
                ncert=ref("MOR", "Description of Some Important Families (Liliaceae; floral formula)"), secs=75)

assertion_reason(T_MOR, "Flower", "Advanced",
                 "The flower of pea is zygomorphic.",
                 "The flower of pea can be divided into two similar halves only in one particular vertical plane.",
                 True, True, True, "A",
                 "Symmetry of the pea flower",
                 "When a flower can be divided into two similar halves only in one particular vertical plane, it is "
                 "zygomorphic. The pea flower (Fabaceae), with its papilionaceous corolla of a standard, two wings "
                 "and a keel, can be halved only along one vertical plane, so it is zygomorphic. R states the "
                 "defining property that makes A true.",
                 ["A: true", "R: true", "One plane of symmetry → zygomorphic"],
                 ncert=ref("MOR", "The Flower; Fabaceae"), secs=40)

match_list(T_MOR, "Root, stem and leaf", "Advanced", "region of the root", "feature",
           ["Root cap", "Region of meristematic activity", "Region of elongation", "Region of maturation"],
           ["Cells undergo rapid elongation and enlargement and are responsible for growth in length",
            "Thimble-like structure that protects the tender apex",
            "Cells gradually differentiate and mature; some epidermal cells form root hairs",
            "Very small, thin-walled cells with dense protoplasm that divide repeatedly"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "B",
           "Regions of the root",
           "The root apex is covered by the root cap, a thimble-like structure that protects the tender apex as it "
           "makes its way through the soil. The cells of the meristematic region are very small, thin-walled, with "
           "dense protoplasm, and divide repeatedly. Cells proximal to it undergo rapid elongation and enlargement "
           "and are responsible for growth of the root in length. Proximal to this, the cells of the region of "
           "maturation differentiate and mature, and some epidermal cells form root hairs.",
           ["Root cap → II", "Meristematic → IV", "Elongation → I", "Maturation → III"],
           why="The wrong codes give the description of dividing cells to the root cap, or root hairs to the region "
               "of elongation.",
           ncert=ref("MOR", "The Root (regions of the root)"), secs=50)

direct(T_MOR, "Flower", "Advanced",
       "A flower has epipetalous stamens and a bicarpellary, syncarpous ovary with axile placentation. Which of the "
       "following could it be?",
       "Brinjal",
       ["Lily", "Pea", "Mustard"], "C",
       "Linking androecium and placentation",
       "Stamens attached to the petals are epipetalous, as in brinjal. Brinjal belongs to Solanaceae, whose ovary is "
       "bicarpellary, syncarpous and superior, with axile placentation on a swollen placenta.",
       ["Epipetalous + bicarpellary axile → Solanaceae → brinjal"],
       why="Lily has epiphyllous stamens (attached to the perianth) and a tricarpellary ovary. Pea has diadelphous "
           "stamens and a monocarpellary ovary with marginal placentation. Mustard has parietal placentation and "
           "stamens that are not epipetalous.",
       ncert=ref("MOR", "The Flower (androecium, placentation); Solanaceae"), secs=45)


# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
direct(T_ANA, "Plant tissues", "Basic",
       "The cells of collenchyma may be:",
       "oval, spherical or polygonal",
       ["long and narrow with tapering, needle-like ends", "tube-like, joined end to end through sieve plates",
        "barrel-shaped, with Casparian strips on their walls"], "D",
       "Shape of collenchyma cells",
       "Collenchyma occurs in layers below the epidermis in dicotyledonous plants, either as a homogeneous layer or "
       "in patches. Its cells are thickened at the corners due to deposition of cellulose, hemicellulose and "
       "pectin, and they may be oval, spherical or polygonal and often contain chloroplasts.",
       ["Collenchyma cells: oval, spherical or polygonal"],
       why="Long, narrow cells with pointed ends describe fibres. Tube-like cells joined through sieve plates are "
           "sieve tube elements. Barrel-shaped cells with Casparian strips form the endodermis of roots.",
       ncert=ref("ANA", "The Tissues (simple tissues, collenchyma)"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "Axillary buds, formed from cells 'left behind' by the shoot apical meristem, are present in the axils of "
       "leaves. They are capable of forming:",
       "a branch or a flower",
       ["only lateral roots", "only the cork cambium", "the vascular bundles of the leaf"], "C",
       "Axillary buds",
       "During the formation of leaves and the elongation of the stem, some cells 'left behind' from the shoot "
       "apical meristem constitute the axillary bud. Such buds are present in the axils of leaves and are capable "
       "of forming a branch or a flower.",
       ["Axillary bud → branch or flower"],
       why="Lateral roots arise from the pericycle of roots. Cork cambium is a lateral meristem. The vascular "
           "bundles of the leaf are not formed by the axillary bud.",
       ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "Sclerenchyma consists of long, narrow cells with thick and lignified cell walls having:",
       "a few or numerous pits",
       ["plasmodesmata in sieve plates", "Casparian strips of suberin", "thickenings only at the corners"], "A",
       "Walls of sclerenchyma",
       "Sclerenchyma consists of long, narrow cells with thick and lignified cell walls having a few or numerous "
       "pits. The cells are usually dead and without protoplasts.",
       ["Sclerenchyma walls: thick, lignified, a few or numerous pits"],
       why="Sieve plates belong to sieve tube elements, Casparian strips to the root endodermis, and corner "
           "thickenings to collenchyma.",
       ncert=ref("ANA", "The Tissues (simple tissues, sclerenchyma)"), secs=20)

statement_pair(T_ANA, "Plant tissues", "Basic",
               "Parenchyma cells may be closely packed or have small intercellular spaces.",
               "Sclereids are spherical, oval or cylindrical, highly thickened dead cells.",
               True, True, "A",
               "Parenchyma and sclereids",
               "Parenchyma cells are generally isodiametric; their walls are thin and made of cellulose, and they may "
               "be closely packed or have small intercellular spaces. Sclereids are spherical, oval or cylindrical, "
               "highly thickened dead cells with very narrow cavities (lumen).",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (simple tissues)"), secs=30)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Sclerenchyma provides mechanical support to organs.",
                 "The cells of sclerenchyma have thick and lignified cell walls.",
                 True, True, True, "A",
                 "Function of sclerenchyma",
                 "Sclerenchyma consists of long, narrow cells with thick and lignified walls, usually dead and "
                 "without protoplasts. Such thick, rigid, lignified walls give strength, which is why sclerenchyma "
                 "provides mechanical support to organs. R explains A.",
                 ["A: true", "R: true", "Thick lignified walls → rigidity → mechanical support"],
                 ncert=ref("ANA", "The Tissues (simple tissues, sclerenchyma)"), secs=35)

match_list(T_ANA, "Plant tissues", "Intermediate", "cell type", "condition at maturity",
           ["Sclereids", "Sieve tube elements", "Companion cells", "Collenchyma"],
           ["Living, with walls thickened at the corners",
            "Dead, highly thickened, with very narrow lumen",
            "Living, with a nucleus that controls the functions of neighbouring sieve tubes",
            "Living, with peripheral cytoplasm and a large vacuole but lacking a nucleus"],
           "II IV III I", ["IV II III I", "II III IV I", "II IV I III"], "B",
           "Living and dead cells of plant tissues",
           "Sclereids are highly thickened dead cells with very narrow lumen. A mature sieve element possesses a "
           "peripheral cytoplasm and a large vacuole but lacks a nucleus. Companion cells are specialised "
           "parenchymatous cells whose nucleus controls the functions of the sieve tubes. Collenchyma cells are "
           "living and thickened at the corners.",
           ["Sclereids → II", "Sieve tube elements → IV", "Companion cells → III", "Collenchyma → I"],
           why="The wrong codes interchange the sieve tube element and the companion cell, or the sclereid and "
               "collenchyma.",
           ncert=ref("ANA", "The Tissues (simple and complex tissues)"), secs=45)

multi_statement(T_ANA, "Tissue systems", "Intermediate",
                "Which of the following statements about the ground tissue system are correct?",
                [("All tissues except the epidermis and vascular bundles constitute the ground tissue.", True),
                 ("The ground tissue consists of simple tissues such as parenchyma, collenchyma and sclerenchyma.",
                  True),
                 ("In primary stems and roots, parenchymatous cells are usually present in the cortex, pericycle, "
                  "pith and medullary rays.", True),
                 ("The endodermis belongs to the epidermal tissue system.", False),
                 ("Leaves have no ground tissue.", False)],
                ["abd", "bce", "abcd"], "B",
                "Ground tissue system",
                "All tissues except epidermis and vascular bundles constitute the ground tissue; it consists of "
                "simple tissues such as parenchyma, collenchyma and sclerenchyma. Parenchymatous cells are usually "
                "present in the cortex, pericycle, pith and medullary rays in primary stems and roots. The "
                "endodermis, the innermost layer of the cortex, is part of the ground tissue. In leaves, the ground "
                "tissue consists of thin-walled, chloroplast-containing cells and is called mesophyll.",
                ["(a), (b), (c): true", "(d): false, endodermis is part of the cortex (ground tissue)",
                 "(e): false, the mesophyll is the ground tissue of leaves"],
                why="Each wrong combination includes (d) or (e), or omits (c).",
                ncert=ref("ANA", "The Tissue System (ground tissue system)"), secs=55)

statement_pair(T_ANA, "Plant tissues", "Intermediate",
               "The first-formed primary phloem consists of narrow sieve tubes and is called protophloem, while the "
               "later-formed phloem, with bigger sieve tubes, is called metaphloem.",
               "Phloem transports food materials, usually from the leaves to other parts of the plant.",
               True, True, "A",
               "Primary phloem",
               "Phloem transports food materials, usually from leaves to other parts of the plant. The first-formed "
               "primary phloem consists of narrow sieve tubes and is referred to as protophloem, and the later-formed "
               "phloem has bigger sieve tubes and is referred to as metaphloem.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (complex tissues, phloem)"), secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "In the transverse section of a dicot root, the few layers of thick-walled parenchymatous cells that lie "
       "immediately inside the endodermis, next to the vascular bundles, form the:",
       "pericycle",
       ["conjunctive tissue", "cortex", "pith"], "B",
       "Layers of the dicot root",
       "From outside inwards, the dicot root shows the epiblema, the cortex, the endodermis and then the pericycle, "
       "a few layers of thick-walled parenchymatous cells. Inside the pericycle lie the radial vascular bundles, "
       "the conjunctive tissue between xylem and phloem, and a small, inconspicuous pith.",
       ["Endodermis → pericycle → vascular bundles"],
       why="Conjunctive tissue lies between the xylem and phloem patches. The cortex lies outside the endodermis. "
           "The pith is central.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicot root)"), secs=30)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "Which of the following statements comparing the primary structure of roots and stems are correct?",
                [("An endodermis is present in both the dicot root and the dicot stem.", True),
                 ("The epidermis of a dicot stem is covered with a thin cuticle, while a cuticle is absent in "
                  "roots.", True),
                 ("The primary xylem is endarch in stems and exarch in roots.", True),
                 ("Both dicot and monocot roots have conjoint vascular bundles.", False),
                 ("The pith of a dicot root is large and well developed.", False)],
                ["abd", "acde", "bce"], "C",
                "Roots and stems compared",
                "Both the dicot root and the dicot stem have an endodermis as the innermost layer of the cortex (in "
                "the stem its cells are rich in starch, the starch sheath). The dicot stem epidermis is covered with "
                "a thin cuticle, which is absent in roots. The primary xylem is endarch in stems and exarch in "
                "roots. Roots have radial vascular bundles, and the pith of the dicot root is small or "
                "inconspicuous (it is large in the monocot root).",
                ["(a), (b), (c): true", "(d): false, roots have radial bundles",
                 "(e): false, the dicot root pith is small"],
                why="Each wrong combination includes (d) or (e), or leaves out a true statement.",
                ncert=ref("ANA", "The Tissue System; Anatomy of Dicotyledonous and Monocotyledonous Plants"),
                secs=60)

assertion_reason(T_ANA, "Plant tissues", "Advanced",
                 "Tracheids are living, thin-walled cells that store starch or fat.",
                 "Xylem parenchyma cells are living and thin-walled, and they store food materials in the form of "
                 "starch or fat.",
                 False, True, False, "D",
                 "Living and dead elements of xylem",
                 "Tracheids are elongated, tube-like cells with thick, lignified walls and tapering ends; they are "
                 "dead and without protoplasm. Xylem parenchyma cells are living and thin-walled, with cellulose "
                 "walls; they store food materials in the form of starch or fat, and other substances like "
                 "tannins.",
                 ["A: false, tracheids are dead", "R: true (describes xylem parenchyma)"],
                 ncert=ref("ANA", "The Tissues (complex tissues, xylem)"), secs=40)

match_list(T_ANA, "Dicot and monocot anatomy", "Advanced", "feature", "where or what",
           ["Radial vascular bundles", "Conjoint, open vascular bundles", "Conjoint, closed vascular bundles",
            "Endarch primary xylem"],
           ["Protoxylem towards the centre (pith) and metaxylem towards the periphery",
            "Roots", "Monocot stems and leaves", "Dicot stems"],
           "II IV III I", ["IV II III I", "II III IV I", "I IV III II"], "B",
           "Types of vascular bundles",
           "In roots, the xylem and phloem lie on different radii, i.e., the bundles are radial. In dicot stems the "
           "conjoint bundles have cambium between phloem and xylem and are open. In monocot stems and leaves, "
           "cambium is absent, so the conjoint bundles are closed. In stems the protoxylem lies towards the centre "
           "and the metaxylem towards the periphery: the primary xylem is endarch.",
           ["Radial → roots", "Conjoint open → dicot stems", "Conjoint closed → monocot stems and leaves",
            "Endarch → protoxylem towards the centre"],
           why="The wrong codes give open bundles to monocots or the exarch arrangement of roots to stems.",
           ncert=ref("ANA", "The Tissue System (vascular tissue system)"), secs=50)

direct(T_ANA, "Plant tissues", "Advanced",
       "Which pair of cells or tissues BOTH store food materials, according to NCERT?",
       "Xylem parenchyma and phloem parenchyma",
       ["Tracheids and sieve tube elements", "Xylem fibres and phloem fibres", "Sclereids and vessels"], "D",
       "Storage function in complex tissues",
       "Xylem parenchyma cells are living and store food materials as starch or fat, and substances like tannins. "
       "Phloem parenchyma stores food material and other substances like resins, latex and mucilage. Tracheids, "
       "vessels, sclereids and fibres are thick-walled conducting or supporting elements; sieve tube elements "
       "conduct food rather than store it.",
       ["Storage in xylem → xylem parenchyma", "Storage in phloem → phloem parenchyma"],
       why="Tracheids and vessels conduct water and are dead; sieve tube elements conduct food. Fibres and "
           "sclereids are mechanical (supporting) elements.",
       ncert=ref("ANA", "The Tissues (complex tissues)"), secs=40)


# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Cell theory", "Basic",
       "Which of the following states the cell theory as it is understood today?",
       "All living organisms are composed of cells and products of cells, and all cells arise from pre-existing "
       "cells",
       ["All living organisms are composed of cells, and new cells arise spontaneously from non-living matter",
        "Only plants are composed of cells, and the presence of a cell wall is unique to living cells",
        "All cells contain a nucleus, and all cells arise by meiosis"], "B",
       "Modern cell theory",
       "Schleiden and Schwann together formulated the cell theory, but it did not explain how new cells were "
       "formed. Rudolf Virchow (1855) explained that cells divide and new cells are formed from pre-existing "
       "cells. The cell theory as understood today is: (i) all living organisms are composed of cells and products "
       "of cells; (ii) all cells arise from pre-existing cells.",
       ["Cells and products of cells make up organisms", "Cells arise from pre-existing cells"],
       why="Spontaneous origin of cells contradicts Virchow's modification. Animals are also made of cells. "
           "Prokaryotic cells and some mature cells lack a nucleus, and most cells arise by mitosis.",
       ncert=ref("CELL", "Cell Theory"), secs=25)

direct(T_CELL, "Endomembrane system", "Basic",
       "The Golgi apparatus consists of many:",
       "flat, disc-shaped sacs or cisternae stacked parallel to each other",
       ["tubular structures scattered throughout the cytoplasm", "spherical membrane-less particles",
        "double-membrane sacs whose inner membrane forms cristae"], "D",
       "Structure of the Golgi apparatus",
       "The Golgi apparatus consists of many flat, disc-shaped sacs or cisternae of 0.5 µm to 1.0 µm diameter, "
       "stacked parallel to each other. A varied number of cisternae are present in a Golgi complex, concentrically "
       "arranged near the nucleus with distinct convex cis (forming) and concave trans (maturing) faces.",
       ["Golgi = stacks of flat, disc-shaped cisternae"],
       why="A network of tubular structures scattered in the cytoplasm is the endoplasmic reticulum. Membrane-less "
           "particles are ribosomes. A double membrane with cristae describes the mitochondrion.",
       ncert=ref("CELL", "Eukaryotic Cells (Golgi apparatus)"), secs=20)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "Bacteria are classified as Gram positive or Gram negative on the basis of:",
       "differences in their cell envelopes and the way they respond to the staining procedure developed by Gram",
       ["the number of flagella they possess", "whether or not they contain plasmids",
        "the shape of the cell, spherical or rod-shaped"], "C",
       "Gram staining",
       "Based on the differences in the cell envelopes and the manner in which they respond to the staining "
       "procedure developed by Gram, bacteria are classified into two groups: those that take up the Gram stain "
       "are Gram positive, and those that do not are Gram negative.",
       ["Basis: cell envelope differences + response to Gram's stain"],
       why="Flagella, plasmids and cell shape are not the basis of the Gram classification.",
       ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "Besides an organised nucleus with a nuclear envelope and a variety of locomotory and cytoskeletal "
       "structures, eukaryotic cells have their genetic material organised into:",
       "chromosomes",
       ["plasmids", "mesosomes", "inclusion bodies"], "B",
       "Features of eukaryotic cells",
       "Eukaryotic cells possess an organised nucleus with a nuclear envelope, and a variety of complex locomotory "
       "and cytoskeletal structures. Their genetic material is organised into chromosomes.",
       ["Eukaryotic genetic material → chromosomes"],
       why="Plasmids, mesosomes and inclusion bodies are features of prokaryotic cells.",
       ncert=ref("CELL", "Eukaryotic Cells"), secs=20)

statement_pair(T_CELL, "Cell envelope and membrane", "Basic",
               "The cell wall and middle lamellae may be traversed by plasmodesmata, which connect the cytoplasm of "
               "neighbouring cells.",
               "Animal cells lack a cell wall.",
               True, True, "A",
               "Cell wall and plasmodesmata",
               "A non-living rigid structure called the cell wall forms an outer covering for the plasma membrane of "
               "fungi and plants. The cell wall and middle lamellae may be traversed by plasmodesmata, which "
               "connect the cytoplasm of neighbouring cells. Animal cells lack a cell wall; their outer boundary is "
               "the plasma membrane.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (cell wall)"), secs=30)

match_list(T_CELL, "Cell theory", "Intermediate", "scientist", "contribution",
           ["Anton Von Leeuwenhoek", "Robert Brown", "Matthias Schleiden", "Rudolf Virchow"],
           ["Observed that all plants are composed of different kinds of cells which form the tissues of the plant",
            "Explained that new cells are formed from pre-existing cells",
            "Later discovered the nucleus", "First saw and described a live cell"],
           "IV III I II", ["III IV I II", "IV III II I", "IV I III II"], "D",
           "History of the cell theory",
           "Anton Von Leeuwenhoek first saw and described a live cell. Robert Brown later discovered the nucleus. "
           "Matthias Schleiden, a German botanist, examined a large number of plants and observed that all plants "
           "are composed of different kinds of cells which form the tissues of the plant. Rudolf Virchow (1855) "
           "explained that cells divide and new cells are formed from pre-existing cells (Omnis cellula-e "
           "cellula).",
           ["Leeuwenhoek → live cell", "Brown → nucleus", "Schleiden → plants made of cells",
            "Virchow → cells from pre-existing cells"],
           why="The wrong codes interchange Leeuwenhoek and Brown, or Schleiden and Virchow.",
           ncert=ref("CELL", "What is a Cell?; Cell Theory"), secs=45)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                 "Chromoplasts give parts of a plant a yellow, orange or red colour.",
                 "Chromoplasts contain fat-soluble carotenoid pigments such as carotene and xanthophylls.",
                 True, True, True, "A",
                 "Chromoplasts",
                 "Based on the type of pigments, plastids are chloroplasts, chromoplasts or leucoplasts. The "
                 "chromoplasts contain fat-soluble carotenoid pigments like carotene, xanthophylls and others, and "
                 "these give the part of the plant a yellow, orange or red colour. R explains A.",
                 ["A: true", "R: true", "Carotenoid pigments → yellow/orange/red colour"],
                 ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=35)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                "Which of the following statements about ribosomes are correct?",
                [("Eukaryotic ribosomes are of the 80S type and prokaryotic ribosomes are of the 70S type.", True),
                 ("Each ribosome has two subunits, a larger and a smaller one.", True),
                 ("The two subunits of the 80S ribosome are 60S and 40S.", True),
                 ("The 'S' in 80S stands for the diameter of the ribosome in nanometres.", False),
                 ("Ribosomes occur in chloroplasts but never in mitochondria.", False)],
                ["abd", "bce", "abcd"], "C",
                "Ribosomes",
                "Eukaryotic ribosomes are 80S while prokaryotic ribosomes are 70S. Each ribosome has two subunits, a "
                "larger and a smaller one; the two subunits of 80S ribosomes are 60S and 40S, while those of 70S "
                "ribosomes are 50S and 30S. 'S' (Svedberg's unit) stands for the sedimentation coefficient, which "
                "indirectly is a measure of density and size. Ribosomes (70S) are found in the matrix of "
                "mitochondria as well as in the stroma of chloroplasts.",
                ["(a), (b), (c): true", "(d): false, S = sedimentation coefficient",
                 "(e): false, the mitochondrial matrix also has 70S ribosomes"],
                why="Each wrong combination includes (d) or (e), or omits (c).",
                ncert=ref("CELL", "Eukaryotic Cells (ribosomes, mitochondria, plastids)"), secs=55)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
               "Both mitochondria and chloroplasts contain their own circular DNA and 70S ribosomes.",
               "Both mitochondria and chloroplasts are bounded by a single membrane.",
               True, False, "C",
               "Mitochondria and chloroplasts compared",
               "The mitochondrial matrix possesses a single circular DNA molecule, a few RNA molecules and 70S "
               "ribosomes; the chloroplast stroma contains small, double-stranded circular DNA molecules and 70S "
               "ribosomes. Each mitochondrion is a double membrane-bound structure, and chloroplasts are also "
               "double membrane-bound.",
               ["Statement I: true", "Statement II: false, both are double membrane-bound"],
               ncert=ref("CELL", "Eukaryotic Cells (mitochondria, plastids)"), secs=35)

direct(T_CELL, "Prokaryotic cell", "Intermediate",
       "The cell envelope of a bacterium consists of the glycocalyx, the cell wall and the plasma membrane. NCERT "
       "describes these three layers as:",
       "performing distinct functions, but acting together as a single protective unit",
       ["performing identical functions, so that any one of them can be lost without effect",
        "loosely associated layers, each acting as a separate protective unit",
        "layers of which only the outermost has any function"], "B",
       "Bacterial cell envelope",
       "Most prokaryotic cells, particularly bacterial cells, have a chemically complex cell envelope consisting of "
       "a tightly bound three-layered structure: the outermost glycocalyx, followed by the cell wall and then the "
       "plasma membrane. Although each layer of the envelope performs a distinct function, they act together as a "
       "single protective unit.",
       ["Three tightly bound layers", "Distinct functions; one protective unit"],
       why="The layers do not perform identical functions, they are tightly bound rather than loose, and the inner "
           "layers (cell wall, plasma membrane) have important functions.",
       ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=30)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "Which of the following is present in a plant cell but absent in a bacterial cell, and is NOT a part of the "
       "endomembrane system?",
       "Mitochondrion",
       ["Golgi apparatus", "Lysosome", "Ribosome"], "D",
       "Endomembrane system and prokaryotes",
       "The endomembrane system includes the endoplasmic reticulum, Golgi complex, lysosomes and vacuoles. "
       "Mitochondria, chloroplasts and peroxisomes are membrane-bound but are not part of it, since their "
       "functions are not coordinated with those components. Bacteria have no membrane-bound organelles such as "
       "mitochondria, but they do have ribosomes.",
       ["Absent in bacteria + not endomembrane → mitochondrion"],
       why="The Golgi apparatus and lysosomes are absent in bacteria but belong to the endomembrane system. "
           "Ribosomes are present in bacteria too.",
       ncert=ref("CELL", "Eukaryotic Cells (endomembrane system, mitochondria)"), secs=35)

multi_statement(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate",
                "Which of the following statements about cilia and flagella are correct?",
                [("Cilia and flagella are hair-like outgrowths of the cell membrane.", True),
                 ("Their core, the axoneme, possesses a number of microtubules running parallel to the long axis.",
                  True),
                 ("The peripheral doublets of the axoneme are interconnected by linkers.", True),
                 ("Cilia are comparatively longer than flagella.", False),
                 ("Bacterial flagella have the same structure as eukaryotic flagella.", False)],
                ["abcd", "bce", "acd"], "A",
                "Cilia and flagella",
                "Cilia and flagella are hair-like outgrowths of the cell membrane and are covered with plasma "
                "membrane. Their core, the axoneme, possesses a number of microtubules running parallel to the long "
                "axis: nine pairs of peripheral doublets and a central pair. The peripheral doublets are "
                "interconnected by linkers. Cilia are small structures that work like oars, while flagella are "
                "comparatively longer. Prokaryotic bacteria also possess flagella, but these are structurally "
                "different from eukaryotic flagella.",
                ["(a), (b), (c): true", "(d): false, flagella are longer", "(e): false, they differ in structure"],
                why="Each wrong combination includes (d) or (e), or omits a true statement.",
                ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella)"), secs=55)

assertion_reason(T_CELL, "Endomembrane system", "Advanced",
                 "Microbodies are found only in plant cells.",
                 "Microbodies are membrane-bound minute vesicles that contain various enzymes.",
                 False, True, False, "D",
                 "Microbodies",
                 "Many membrane-bound minute vesicles called microbodies, which contain various enzymes, are present "
                 "in both plant and animal cells. So A is false and R is true.",
                 ["A: false, microbodies occur in both plant and animal cells", "R: true"],
                 ncert=ref("CELL", "Eukaryotic Cells (microbodies)"), secs=35)

multi_statement(T_CELL, "Endomembrane system", "Advanced",
                "Which of the following structures are bounded by two membranes (a double membrane)?",
                [("Nucleus", True), ("Mitochondrion", True), ("Chloroplast", True), ("Lysosome", False),
                 ("Golgi cisterna", False)],
                ["abd", "bce", "acde"], "B",
                "Membrane covering of organelles",
                "The nucleus is bounded by a nuclear envelope of two parallel membranes with a perinuclear space "
                "between them. Each mitochondrion is a double membrane-bound structure, and chloroplasts too are "
                "double membrane-bound. Lysosomes are membrane-bound vesicles formed by packaging in the Golgi, and "
                "Golgi cisternae are flat, disc-shaped sacs; each is bounded by a single membrane.",
                ["Double membrane: nucleus, mitochondrion, chloroplast",
                 "Single membrane: lysosome, Golgi cisterna"],
                why="Each wrong combination either includes the single-membrane lysosome or Golgi cisterna, or leaves "
                    "out one of the double-membrane organelles.",
                ncert=ref("CELL", "Eukaryotic Cells"), secs=50)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "Mitochondria are the sites of aerobic respiration.",
                 "The mitochondrial matrix contains 70S ribosomes.",
                 True, True, False, "B",
                 "Mitochondria",
                 "Mitochondria are the sites of aerobic respiration; they produce cellular energy in the form of ATP, "
                 "and the matrix and inner membrane carry the enzymes for it. The matrix also possesses a single "
                 "circular DNA molecule, a few RNA molecules and 70S ribosomes, which are concerned with protein "
                 "synthesis, not with respiration itself. R is true but does not explain A.",
                 ["A: true", "R: true", "Ribosomes make proteins; they do not explain why respiration occurs there"],
                 ncert=ref("CELL", "Eukaryotic Cells (mitochondria)"), secs=40)

match_list(T_CELL, "Endomembrane system", "Advanced", "cell component", "function",
           ["Lysosome", "Smooth endoplasmic reticulum", "Nucleolus", "Centriole"],
           ["Active synthesis of ribosomal RNA",
            "Forms the basal body of cilia or flagella",
            "Digestion of carbohydrates, proteins, lipids and nucleic acids by hydrolases",
            "Major site for the synthesis of lipids"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "C",
           "Functions of cell components",
           "Lysosomes are rich in hydrolytic enzymes (lipases, proteases, carbohydrases) that digest carbohydrates, "
           "proteins, lipids and nucleic acids. The smooth ER is the major site for synthesis of lipids. The "
           "nucleolus is a site for active ribosomal RNA synthesis. Centrioles form the basal bodies of cilia or "
           "flagella and, in animal cells, the spindle fibres.",
           ["Lysosome → III", "SER → IV", "Nucleolus → I", "Centriole → II"],
           why="The wrong codes interchange lysosomes and the smooth ER, or the nucleolus and the centriole.",
           ncert=ref("CELL", "Eukaryotic Cells"), secs=45)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
       "In which of the following locations would 80S ribosomes be found rather than 70S ribosomes?",
       "The cytoplasm of an onion root cell",
       ["The cytoplasm of a bacterium", "The matrix of a mitochondrion",
        "The stroma of a chloroplast"], "A",
       "Location of 70S and 80S ribosomes",
       "Eukaryotic cytoplasmic ribosomes are 80S. Prokaryotic ribosomes are 70S, and the ribosomes in the "
       "mitochondrial matrix and in the chloroplast stroma are also 70S. An onion root cell is eukaryotic, so its "
       "cytoplasmic ribosomes are 80S.",
       ["Eukaryotic cytoplasm → 80S", "Bacteria, mitochondria, chloroplasts → 70S"],
       why="Bacteria, mitochondria and chloroplasts all have 70S ribosomes.",
       ncert=ref("CELL", "Eukaryotic Cells (ribosomes, mitochondria, plastids)"), secs=35)


# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Mitosis", "Basic",
       "During prophase of mitosis, each centrosome radiates out microtubules called asters. The two asters, "
       "together with the spindle fibres, form the:",
       "mitotic apparatus",
       ["synaptonemal complex", "kinetochore", "cell plate"], "C",
       "Mitotic apparatus",
       "In prophase, the centrosome, which had undergone duplication during the S phase of interphase, begins to "
       "move towards opposite poles of the cell. Each centrosome radiates out microtubules called asters. The two "
       "asters together with the spindle fibres form the mitotic apparatus.",
       ["Asters + spindle fibres = mitotic apparatus"],
       why="The synaptonemal complex forms between synapsed homologues in zygotene of meiosis. A kinetochore is a "
           "disc-shaped structure on the centromere. The cell plate forms during cytokinesis in plant cells.",
       ncert=ref("CC", "M Phase (prophase)"), secs=20)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "Interphase is also called the resting phase, although during it the cell prepares for division by "
               "undergoing both cell growth and DNA replication in an orderly manner.",
               "The M phase represents the most dramatic period of the cell cycle, involving a major reorganisation "
               "of virtually all components of the cell.",
               True, True, "A",
               "Interphase and M phase",
               "Interphase, though called the resting phase, is the time during which the cell is preparing for "
               "division by undergoing both cell growth and DNA replication in an orderly manner. The M phase "
               "represents the most dramatic period of the cell cycle, involving a major reorganisation of "
               "virtually all components of the cell.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Cell Cycle (phases of cell cycle); M Phase"), secs=30)

match_list(T_CC, "Mitosis", "Basic", "term", "description",
           ["Aster", "Kinetochore", "Synaptonemal complex", "Chiasma"],
           ["Complex formed between a pair of synapsed homologous chromosomes",
            "Microtubules radiating out from each centrosome",
            "X-shaped structure at a site of crossing over",
            "Small disc-shaped structure at the surface of the centromere"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "B",
           "Terms of cell division",
           "Each centrosome radiates out microtubules called asters (prophase). Kinetochores are small disc-shaped "
           "structures at the surface of the centromeres that serve as sites of attachment of spindle fibres. "
           "Synapsis in zygotene is accompanied by the formation of a complex structure called the synaptonemal "
           "complex. In diplotene the homologues remain attached at the sites of crossovers, the X-shaped "
           "structures called chiasmata.",
           ["Aster → II", "Kinetochore → IV", "Synaptonemal complex → I", "Chiasma → III"],
           why="The wrong codes interchange the aster and the kinetochore, or the synaptonemal complex and the "
               "chiasma.",
           ncert=ref("CC", "M Phase; Meiosis"), secs=40)

direct(T_CC, "Cell cycle phases", "Basic",
       "The M phase starts with karyokinesis. Karyokinesis corresponds to the:",
       "separation of daughter chromosomes, i.e., nuclear division",
       ["division of the cytoplasm", "replication of DNA",
        "duplication of the centriole in the cytoplasm"], "D",
       "Karyokinesis and cytokinesis",
       "The M phase starts with the nuclear division, corresponding to the separation of daughter chromosomes "
       "(karyokinesis), and usually ends with the division of the cytoplasm (cytokinesis).",
       ["Karyokinesis = nuclear division (separation of daughter chromosomes)",
        "Cytokinesis = division of cytoplasm"],
       why="Division of the cytoplasm is cytokinesis. DNA replication and centriole duplication take place in the "
           "S phase of interphase.",
       ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=20)

numerical(T_CC, "Significance", "Intermediate",
          "A cell with 2n = 20 divides once by mitosis. Another cell of the same plant, with 2n = 20, completes "
          "meiosis. What is the total number of chromosomes present in all the daughter cells taken together, in "
          "each case?",
          "40 after mitosis and 40 after meiosis",
          ["40 after mitosis and 20 after meiosis", "20 after mitosis and 40 after meiosis",
           "40 after mitosis and 80 after meiosis"], "A",
          (2 * 20 == 40) and (4 * (20 // 2) == 40),
          "Chromosome number after mitosis and meiosis",
          "Mitosis is an equational division: one cell with 2n = 20 forms two cells, each with 20 chromosomes. "
          "Meiosis forms four haploid cells, each with n = 10 chromosomes. Totals: 2 × 20 = 40 and 4 × 10 = 40. The "
          "total is the same because the parent cell's chromosomes were replicated once before division in both "
          "cases.",
          ["Mitosis: 2 cells × 20 = 40", "Meiosis: 4 cells × 10 = 40"],
          why="20 after meiosis counts only two of the four products. 20 after mitosis counts one daughter cell. 80 "
              "after meiosis wrongly gives each of the four cells the diploid number.",
          ncert=ref("CC", "Mitosis; Meiosis"), secs=60,
          short="One round of DNA replication → total chromosomes double, however many cells share them.")

assertion_reason(T_CC, "Meiosis", "Intermediate",
                 "The X-shaped structures called chiasmata are the sites of crossing over.",
                 "Chiasmata first become visible during leptotene.",
                 True, False, False, "C",
                 "Chiasmata",
                 "Diplotene is recognised by the dissolution of the synaptonemal complex and the tendency of the "
                 "recombined homologous chromosomes of the bivalents to separate from each other except at the "
                 "sites of crossovers. These X-shaped structures are called chiasmata. They become visible in "
                 "diplotene, not leptotene, when the chromosomes have only just started to become visible.",
                 ["A: true", "R: false, chiasmata are seen in diplotene"],
                 ncert=ref("CC", "Meiosis (prophase I)"), secs=35)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following statements about the stages of mitosis are correct?",
                [("In prophase, the centrosome, which had duplicated during the S phase, begins to move towards "
                  "opposite poles.", True),
                 ("At metaphase, each chromosome is made of two sister chromatids held together by the "
                  "centromere.", True),
                 ("At metaphase, the spindle fibres attach to the kinetochores of the chromosomes.", True),
                 ("In anaphase, the centromere of each chromosome remains directed towards the pole, at the "
                  "leading edge.", True),
                 ("At telophase, the chromosomes condense further and become more distinct.", False)],
                ["abc", "bcde", "acd"], "C",
                "Events of mitosis",
                "In prophase the duplicated centrosomes begin to move towards opposite poles. At metaphase, "
                "chromosomes are made up of two sister chromatids held together by the centromere, and spindle "
                "fibres attach to their kinetochores. In anaphase, as each chromosome moves away from the "
                "equatorial plate, the centromere remains directed towards the pole at the leading edge, with the "
                "arms trailing. At telophase the chromosomes decondense and lose their individuality.",
                ["(a)–(d): true", "(e): false, chromosomes decondense at telophase"],
                why="Combinations with (e) are wrong; those without (d) or (b) leave out a true statement.",
                ncert=ref("CC", "M Phase"), secs=55)

match_list(T_CC, "Significance", "Intermediate", "phenomenon", "example given in NCERT",
           ["Mitosis in haploid cells", "Cell repair by mitosis",
            "Continuous growth throughout life by mitosis", "Karyokinesis not followed by cytokinesis"],
           ["Apical and lateral cambium of plants", "Liquid endosperm of coconut",
            "Some lower plants and some social insects", "Cells of the upper layer of the epidermis and the gut "
                                                         "lining"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "B",
           "Significance of mitosis",
           "In some lower plants and in some social insects, haploid cells also divide by mitosis. Cells of the upper "
           "layer of the epidermis, the cells of the lining of the gut and blood cells are constantly replaced by "
           "mitosis (cell repair). Mitotic divisions in the meristematic tissues, the apical and lateral cambium, "
           "result in continuous growth of plants throughout their life. When karyokinesis is not followed by "
           "cytokinesis, a multinucleate condition (syncytium) arises, as in the liquid endosperm of coconut.",
           ["Haploid mitosis → lower plants, social insects", "Repair → epidermis, gut lining",
            "Continuous growth → cambium", "No cytokinesis → coconut endosperm"],
           why="The wrong codes interchange the examples of haploid mitosis and cell repair, or of cambium and "
               "coconut endosperm.",
           ncert=ref("CC", "M Phase (cytokinesis); Significance of Mitosis"), secs=45)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "The compaction of chromosomes continues throughout leptotene.",
               "During zygotene, synapsis takes place between the two sister chromatids of each chromosome.",
               True, False, "C",
               "Leptotene and zygotene",
               "During leptotene the chromosomes become gradually visible under the light microscope, and the "
               "compaction of chromosomes continues throughout leptotene. During zygotene, homologous chromosomes "
               "start pairing together; this process of association is synapsis. Synapsis is between homologous "
               "chromosomes, not between the sister chromatids of one chromosome.",
               ["Statement I: true", "Statement II: false, synapsis pairs homologous chromosomes"],
               ncert=ref("CC", "Meiosis (prophase I)"), secs=35)

numerical(T_CC, "Meiosis", "Advanced",
          "A meiocyte of a plant has 2n = 24. Every chromosome has one centromere until the centromeres split. How "
          "many centromeres are present in the meiocyte at metaphase I, and how many chromosomes are present in "
          "each nucleus at telophase II?",
          "24 centromeres; 12 chromosomes",
          ["48 centromeres; 12 chromosomes", "24 centromeres; 24 chromosomes", "12 centromeres; 6 chromosomes"], "B",
          (24 == 2 * 12) and (24 // 2 == 12),
          "Centromeres and chromosome number in meiosis",
          "At metaphase I the 24 replicated chromosomes are paired as 12 bivalents, but each chromosome still has "
          "one undivided centromere holding its two sister chromatids, so there are 24 centromeres (centromeres "
          "split only at anaphase II). Meiosis I separates the homologues, and meiosis II separates the sister "
          "chromatids, so each nucleus at telophase II has n = 12 chromosomes.",
          ["Metaphase I: 24 chromosomes in 12 bivalents → 24 centromeres",
           "Telophase II: n = 24 ÷ 2 = 12 chromosomes per nucleus"],
          why="48 counts chromatids instead of centromeres. 24 chromosomes at telophase II ignores the reduction. "
              "12 centromeres counts bivalents, and 6 halves the number twice.",
          ncert=ref("CC", "Meiosis"), secs=70)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements comparing mitosis and meiosis are correct?",
                [("Bivalents are formed in meiosis I but not in mitosis.", True),
                 ("Sister chromatids separate at anaphase of mitosis and at anaphase II of meiosis.", True),
                 ("Crossing over takes place during pachytene of meiosis I.", True),
                 ("The two cells formed at the end of meiosis I are diploid.", False),
                 ("DNA replicates again before meiosis II begins.", False)],
                ["abd", "bce", "abcd"], "D",
                "Mitosis versus meiosis",
                "Homologous chromosomes pair to form bivalents only in zygotene of meiosis I. Sister chromatids "
                "separate when centromeres split at anaphase of mitosis and anaphase II of meiosis. Crossing over "
                "occurs in pachytene. Meiosis I halves the chromosome number, so its products are haploid, and there "
                "is no DNA replication during interkinesis.",
                ["(a), (b), (c): true", "(d): false, meiosis I products are haploid",
                 "(e): false, no replication in interkinesis"],
                why="Each wrong combination contains (d) or (e), or omits (c).",
                ncert=ref("CC", "Mitosis; Meiosis"), secs=60)

assertion_reason(T_CC, "Mitosis", "Advanced",
                 "Although karyokinesis is divided into four stages, very clear-cut lines cannot be drawn between "
                 "the stages.",
                 "In animals, mitotic cell division is seen only in the diploid somatic cells.",
                 True, True, False, "B",
                 "Mitosis as a progressive process",
                 "For the sake of convenience, karyokinesis is studied in four stages (prophase, metaphase, anaphase "
                 "and telophase), but cell division is a progressive process and very clear-cut lines cannot be "
                 "drawn between the various stages. Separately, NCERT notes that in animals mitosis is seen only in "
                 "diploid somatic cells. That fact concerns where mitosis occurs, not why its stages merge into one "
                 "another, so R does not explain A.",
                 ["A: true", "R: true", "R describes where mitosis occurs; it does not explain A"],
                 ncert=ref("CC", "M Phase"), secs=45)

statement_pair(T_CC, "Meiosis", "Advanced",
               "By the end of diakinesis, the meiotic spindle is assembled while the nucleolus remains intact.",
               "In metaphase II, the chromosomes align at the equator, and microtubules from opposite poles attach "
               "to the kinetochores of sister chromatids.",
               False, True, "D",
               "Diakinesis and metaphase II",
               "During diakinesis the chromosomes are fully condensed and the meiotic spindle is assembled; by the end "
               "of diakinesis the nucleolus disappears and the nuclear envelope breaks down. At metaphase II the "
               "chromosomes align at the equator, and the microtubules from opposite poles of the spindle get "
               "attached to the kinetochores of sister chromatids.",
               ["Statement I: false, the nucleolus disappears by the end of diakinesis", "Statement II: true"],
               ncert=ref("CC", "Meiosis (prophase I, metaphase II)"), secs=40)


# =============================================================== 7. Photosynthesis (4/6/5)
direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Ribulose bisphosphate (RuBP), the primary CO₂ acceptor of the Calvin cycle, is a:",
       "5-carbon ketose sugar",
       ["3-carbon organic acid", "4-carbon dicarboxylic acid", "6-carbon aldose sugar"], "A",
       "The CO₂ acceptor of the Calvin cycle",
       "After it was found that the first product of CO₂ fixation was a 3-carbon acid (PGA), scientists looked for "
       "the acceptor molecule. Surprisingly, the acceptor molecule was a 5-carbon ketose sugar: ribulose "
       "bisphosphate (RuBP).",
       ["RuBP = 5-carbon ketose sugar"],
       why="A 3-carbon acid is PGA, the product of carboxylation. A 4-carbon acid is OAA, the first product in C4 "
           "plants. Glucose is a 6-carbon sugar, not the acceptor.",
       ncert=ref("PS", "Where are the ATP and NADPH used? (the primary acceptor of CO₂)"), secs=20)

direct(T_PS, "Site and pigments", "Basic",
       "NCERT describes photosynthesis as a process by which green plants use light energy to drive the synthesis "
       "of organic compounds. It calls this process a:",
       "physico-chemical process",
       ["purely physical process", "catabolic process", "process occurring only in darkness"], "C",
       "Nature of photosynthesis",
       "All animals, including humans, depend on plants for their food. Green plants carry out photosynthesis, a "
       "physico-chemical process by which they use light energy to drive the synthesis of organic compounds.",
       ["Photosynthesis: physico-chemical; light energy → organic compounds"],
       why="Photosynthesis involves both physical (light absorption) and chemical events. It builds organic "
           "compounds, so it is not catabolic, and its light reactions need light.",
       ncert=ref("PS", "Introduction"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "In plants with the C4 pathway, the enzyme that fixes atmospheric CO₂ with phosphoenol pyruvate in the "
       "mesophyll cells is:",
       "PEP carboxylase (PEPcase)",
       ["RuBP carboxylase-oxygenase (RuBisCO)", "NADP reductase", "ATP synthase"], "B",
       "Primary carboxylation in C4 plants",
       "In C4 plants, the primary CO₂ acceptor is a 3-carbon molecule, phosphoenol pyruvate (PEP), present in the "
       "mesophyll cells. The enzyme responsible for this fixation is PEP carboxylase or PEPcase. The mesophyll cells "
       "lack RuBisCO, which is present in the bundle sheath cells.",
       ["PEP + CO₂ → OAA, catalysed by PEPcase, in mesophyll cells"],
       why="RuBisCO fixes CO₂ with RuBP in the bundle sheath cells. NADP reductase reduces NADP⁺, and ATP synthase "
           "makes ATP; neither fixes CO₂.",
       ncert=ref("PS", "The C4 Pathway"), secs=20)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Basic",
               "Regeneration of the CO₂ acceptor molecule, RuBP, is crucial if the Calvin cycle is to continue "
               "uninterrupted.",
               "The reduction steps of the Calvin cycle use NADPH but no ATP.",
               True, False, "C",
               "Stages of the Calvin cycle",
               "The Calvin cycle has three stages: carboxylation, reduction and regeneration. Reduction is a series "
               "of reactions that lead to the formation of glucose; it involves the utilisation of 2 molecules of "
               "ATP for phosphorylation and 2 of NADPH for reduction per CO₂ molecule fixed. Regeneration of the "
               "CO₂ acceptor RuBP is crucial if the cycle is to continue uninterrupted; it needs one ATP.",
               ["Statement I: true", "Statement II: false, reduction uses 2 ATP and 2 NADPH per CO₂"],
               ncert=ref("PS", "The Calvin Cycle"), secs=30)

numerical(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
          "The Calvin cycle uses 3 ATP and 2 NADPH for every molecule of CO₂ fixed. The light reactions of a "
          "chloroplast have supplied 45 molecules of ATP and 40 molecules of NADPH to the stroma, and no more are "
          "made. How many molecules of CO₂ can be fixed, and which product runs out first?",
          "15 molecules of CO₂; ATP runs out first",
          ["20 molecules of CO₂; NADPH runs out first", "17 molecules of CO₂; both run out together",
           "45 molecules of CO₂; NADPH runs out first"], "D",
          (min(45 // 3, 40 // 2) == 15 and 45 // 3 < 40 // 2 and 40 - 15 * 2 == 10),
          "ATP and NADPH requirement of the Calvin cycle",
          "Each CO₂ fixed needs 3 ATP and 2 NADPH. 45 ATP are enough for 45 ÷ 3 = 15 CO₂, while 40 NADPH would be "
          "enough for 40 ÷ 2 = 20 CO₂. Fixation stops when the ATP is used up, after 15 CO₂; at that point 15 × 2 = "
          "30 NADPH have been used and 10 NADPH remain.",
          ["ATP allows 45 ÷ 3 = 15 CO₂", "NADPH allows 40 ÷ 2 = 20 CO₂", "Smaller value → 15 CO₂; ATP limiting"],
          why="20 CO₂ uses the NADPH figure and ignores that ATP is exhausted first. 17 comes from dividing the total "
              "85 molecules by 5 (3 + 2), which treats ATP and NADPH as interchangeable. 45 counts one ATP per CO₂.",
          ncert=ref("PS", "The Calvin Cycle"), secs=60,
          short="Divide each supply by its per-CO₂ need; the smaller quotient is the answer.")

match_list(T_PS, "Light reactions and photophosphorylation", "Intermediate", "enzyme", "reaction catalysed",
           ["RuBisCO", "PEP carboxylase", "ATP synthase", "NADP reductase"],
           ["Reduction of NADP⁺ to NADPH + H⁺ on the stroma side of the thylakoid membrane",
            "Combination of RuBP with CO₂ (or with O₂)",
            "Synthesis of ATP as protons diffuse through its CF₀ channel",
            "Fixation of CO₂ with phosphoenol pyruvate to form oxaloacetic acid"],
           "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "A",
           "Enzymes of photosynthesis",
           "RuBisCO carboxylates RuBP (its active site can also bind O₂, which leads to photorespiration). PEP "
           "carboxylase fixes CO₂ with PEP in the mesophyll of C4 plants to form OAA. ATP synthase (CF₀–CF₁) makes "
           "ATP as protons move across the membrane through CF₀. NADP reductase, located on the stroma side of the "
           "membrane, reduces NADP⁺ to NADPH + H⁺.",
           ["RuBisCO → II", "PEPcase → IV", "ATP synthase → III", "NADP reductase → I"],
           why="The wrong codes interchange the two carboxylases, or ATP synthase and NADP reductase.",
           ncert=ref("PS", "The Electron Transport; The Calvin Cycle; The C4 Pathway; Photorespiration"), secs=45)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                 "In C4 plants, the Calvin pathway takes place in the bundle sheath cells.",
                 "The mesophyll cells of C4 plants are rich in RuBisCO.",
                 True, False, False, "C",
                 "Division of labour in C4 plants",
                 "In C4 plants, the CO₂ released by the C4 acid in the bundle sheath cells enters the C3 or Calvin "
                 "pathway, which is common to all plants. The bundle sheath cells are rich in RuBisCO but lack "
                 "PEPcase, while the mesophyll cells lack RuBisCO. So R is false.",
                 ["A: true", "R: false, mesophyll cells of C4 plants lack RuBisCO"],
                 ncert=ref("PS", "The C4 Pathway"), secs=35)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following statements about the Calvin cycle are correct?",
                [("Carboxylation is the fixation of CO₂ into a stable organic intermediate.", True),
                 ("Carboxylation is the most crucial step of the Calvin cycle.", True),
                 ("The reduction steps involve the utilisation of ATP for phosphorylation and of NADPH for "
                  "reduction.", True),
                 ("Regeneration of RuBP requires NADPH but no ATP.", False),
                 ("RuBisCO catalyses the reduction steps of the cycle.", False)],
                ["abd", "bce", "abcd"], "B",
                "Stages of the Calvin cycle",
                "Carboxylation is the fixation of CO₂ into a stable organic intermediate and is the most crucial step "
                "of the Calvin cycle, where CO₂ is used for the carboxylation of RuBP by RuBisCO to form two "
                "molecules of 3-PGA. Reduction involves the use of 2 ATP for phosphorylation and 2 NADPH for "
                "reduction per CO₂ fixed. Regeneration of RuBP requires one ATP for phosphorylation.",
                ["(a), (b), (c): true", "(d): false, regeneration uses ATP",
                 "(e): false, RuBisCO catalyses carboxylation"],
                why="Each wrong combination includes (d) or (e), or omits (c).",
                ncert=ref("PS", "The Calvin Cycle"), secs=55)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
               "In C4 plants, the bundle sheath cells may form several layers around the vascular bundles.",
               "The bundle sheath cells of C4 plants are rich in RuBisCO but lack PEPcase.",
               True, True, "A",
               "Kranz anatomy",
               "The particularly large cells around the vascular bundles of C4 plants are called bundle sheath cells, "
               "and the leaves having such anatomy are said to have Kranz anatomy. The bundle sheath cells may form "
               "several layers around the vascular bundles. They are rich in RuBisCO but lack PEPcase.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "The C4 Pathway"), secs=35)

direct(T_PS, "Light reactions and photophosphorylation", "Intermediate",
       "Which of the following is required for BOTH cyclic and non-cyclic photophosphorylation?",
       "Photosystem I",
       ["Photosystem II", "Splitting of water", "Reduction of NADP⁺ by NADP reductase"], "D",
       "Cyclic and non-cyclic photophosphorylation",
       "In non-cyclic photophosphorylation the two photosystems work in series, PS II and then PS I; water is split "
       "and NADP⁺ is reduced. In cyclic photophosphorylation only PS I is functional, and the electron is "
       "circulated within the photosystem, so there is no water splitting and no NADPH. PS I is therefore common "
       "to both.",
       ["Non-cyclic: PS II + PS I", "Cyclic: PS I only", "Common: PS I"],
       why="PS II, splitting of water and NADP reduction take place only in non-cyclic photophosphorylation.",
       ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation"), secs=30)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                "Which of the following statements comparing C3 and C4 plants are correct?",
                [("In C3 plants, the initial carboxylation takes place in the mesophyll cells.", True),
                 ("In C4 plants, the initial carboxylation takes place in the mesophyll cells.", True),
                 ("RuBisCO is present in the bundle sheath cells of C4 plants.", True),
                 ("The first stable product of CO₂ fixation is PGA in both C3 and C4 plants.", False),
                 ("Photorespiration is greater in C4 plants than in C3 plants.", False)],
                ["abcd", "bce", "acd"], "A",
                "C3 and C4 plants compared",
                "In C3 plants, RuBisCO fixes CO₂ with RuBP in the mesophyll cells. In C4 plants, the initial "
                "carboxylation is by PEPcase, also in the mesophyll cells, forming OAA, a 4-carbon acid, as the "
                "first product; the CO₂ is later released in the bundle sheath cells, which contain RuBisCO, and "
                "fixed by the Calvin cycle. C4 plants have a mechanism that raises CO₂ concentration at the enzyme "
                "site, so photorespiration does not occur in them.",
                ["(a), (b), (c): true", "(d): false, the first product in C4 plants is OAA",
                 "(e): false, photorespiration does not occur in C4 plants"],
                why="Each wrong combination contains (d) or (e), or omits a true statement.",
                ncert=ref("PS", "The C4 Pathway; Photorespiration"), secs=60)

assertion_reason(T_PS, "Chemiosmosis", "Advanced",
                 "ATP synthesis in the chloroplast requires a proton gradient across the thylakoid membrane.",
                 "The reaction centre of Photosystem II has an absorption peak at 680 nm.",
                 True, True, False, "B",
                 "Chemiosmosis",
                 "According to the chemiosmotic hypothesis, ATP synthesis is linked to the development of a proton "
                 "gradient across the thylakoid membrane: the breakdown of the gradient, as protons move through "
                 "the CF₀ channel of ATP synthase, provides the energy for ATP synthesis. The absorption peak of "
                 "the PS II reaction centre (P680) is a separate property of the photosystem and does not explain "
                 "why ATP synthesis needs a proton gradient.",
                 ["A: true", "R: true", "R is unrelated to the mechanism of ATP synthesis"],
                 ncert=ref("PS", "The Electron Transport; Where are the ATP and NADPH used?"), secs=40)

match_list(T_PS, "Chemiosmosis", "Advanced", "event", "location in the chloroplast",
           ["Splitting of water", "Reduction of NADP⁺", "Carboxylation of RuBP", "Cyclic photophosphorylation"],
           ["Stroma lamellae", "Inner (lumen) side of the thylakoid membrane",
            "Outer (stroma) side of the thylakoid membrane", "Stroma"],
           "II III IV I", ["III II IV I", "II III I IV", "II IV III I"], "D",
           "Where the events of photosynthesis occur",
           "The splitting of water takes place on the inner side of the thylakoid membrane, so its protons "
           "accumulate in the lumen. NADP reductase is located on the stroma side of the membrane, where NADP⁺ is "
           "reduced using protons from the stroma. RuBisCO carboxylates RuBP in the stroma during the Calvin cycle. "
           "Cyclic photophosphorylation possibly occurs in the stroma lamellae, which lack PS II and NADP reductase.",
           ["Water splitting → lumen side", "NADP⁺ reduction → stroma side of membrane",
            "Carboxylation → stroma", "Cyclic photophosphorylation → stroma lamellae"],
           why="The wrong codes put water splitting on the stroma side or the Calvin cycle in the stroma lamellae.",
           ncert=ref("PS", "The Electron Transport; The Calvin Cycle"), secs=50)

direct(T_PS, "Light reactions and photophosphorylation", "Advanced",
       "In an illuminated chloroplast, Photosystem II stops working, while Photosystem I and its electron carriers "
       "keep functioning. Which of the following can still take place in the thylakoids?",
       "Synthesis of ATP by cyclic photophosphorylation, without evolution of O₂ or formation of NADPH",
       ["Non-cyclic photophosphorylation with evolution of O₂",
        "Splitting of water and formation of NADPH + H⁺, but no ATP",
        "Formation of NADPH + H⁺ by electrons supplied from water"], "C",
       "Role of the two photosystems",
       "Water splitting is associated with PS II, and in non-cyclic photophosphorylation electrons flow from water "
       "through PS II to PS I and on to NADP⁺. Without PS II there is no water splitting, so no O₂ is evolved and "
       "no electrons from water reach NADP⁺. In cyclic photophosphorylation only PS I is functional: its electron "
       "is cycled back through the electron transport chain, producing ATP but not NADPH.",
       ["No PS II → no water splitting, no O₂, no NADPH", "PS I alone → cyclic flow → ATP only"],
       why="O₂ evolution and water splitting need PS II. NADPH formation from water needs electrons from PS II.",
       ncert=ref("PS", "The Electron Transport; Splitting of Water; Cyclic and Non-cyclic Photo-phosphorylation"),
       secs=50)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Advanced",
               "In C4 plants, both the initial carboxylation by PEPcase and the carboxylation by RuBisCO take place "
               "in the same cell.",
               "The primary CO₂ acceptor in the mesophyll cells of C4 plants is a 5-carbon compound.",
               False, False, "B",
               "Spatial separation in the C4 pathway",
               "In C4 plants, the primary CO₂ acceptor is the 3-carbon molecule PEP in the mesophyll cells, fixed by "
               "PEPcase to form OAA. The C4 acid moves to the bundle sheath cells, where it releases CO₂ that is "
               "fixed again by RuBisCO in the Calvin cycle. The two carboxylations therefore occur in different "
               "cells, and the primary acceptor has three carbons, not five.",
               ["Statement I: false, PEPcase acts in mesophyll and RuBisCO in bundle sheath",
                "Statement II: false, PEP is a 3-carbon compound"],
               ncert=ref("PS", "The C4 Pathway"), secs=40)


# =============================================================== 8. Respiration in Plants (3/5/3)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "In glycolysis, glucose is first phosphorylated to glucose-6-phosphate by hexokinase. Glucose-6-phosphate is "
       "then isomerised to produce:",
       "fructose-6-phosphate",
       ["fructose 1,6-bisphosphate", "3-phosphoglyceraldehyde (PGAL)", "1,3-bisphosphoglycerate (BPGA)"], "D",
       "Early steps of glycolysis",
       "Glucose is phosphorylated to give glucose-6-phosphate by the enzyme hexokinase. This is then isomerised to "
       "produce fructose-6-phosphate. Fructose-6-phosphate is phosphorylated, using ATP, to fructose "
       "1,6-bisphosphate, which is split into dihydroxyacetone phosphate and PGAL.",
       ["Glucose → G-6-P (hexokinase)", "G-6-P → (isomerisation) → F-6-P", "F-6-P → F-1,6-BP (ATP used)"],
       why="Fructose 1,6-bisphosphate needs a further phosphorylation; PGAL is formed by splitting it; BPGA is formed "
           "by oxidation of PGAL. None is the product of isomerising glucose-6-phosphate.",
       ncert=ref("RES", "Glycolysis"), secs=20)

direct(T_RES, "TCA cycle", "Basic",
       "In NCERT's equation for the oxidative decarboxylation of pyruvic acid to acetyl CoA by pyruvic "
       "dehydrogenase, which ion is shown as required?",
       "Mg²⁺",
       ["Fe²⁺", "Cu²⁺", "Ca²⁺"], "A",
       "Link reaction",
       "Pyruvic acid + CoA + NAD⁺ → Acetyl CoA + CO₂ + NADH + H⁺, catalysed by pyruvate dehydrogenase in the "
       "mitochondrial matrix; NCERT shows Mg²⁺ along with the enzyme over the arrow. The reaction also needs "
       "coenzymes including NAD⁺ and coenzyme A.",
       ["Pyruvate dehydrogenase + Mg²⁺ → acetyl CoA + CO₂ + NADH + H⁺"],
       why="Copper centres are part of complex IV (cytochrome c oxidase); Fe²⁺ and Ca²⁺ are not shown in this "
           "equation.",
       ncert=ref("RES", "Aerobic Respiration"), secs=20)

statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "Fermentation accounts for only a partial breakdown of glucose, whereas in aerobic respiration glucose "
               "is completely degraded to CO₂ and H₂O.",
               "Lactic acid fermentation releases CO₂.",
               True, False, "C",
               "Fermentation and aerobic respiration",
               "NCERT compares the two: fermentation accounts for only a partial breakdown of glucose, whereas in "
               "aerobic respiration it is completely degraded to CO₂ and H₂O. In lactic acid fermentation, pyruvic "
               "acid is reduced to lactic acid by lactate dehydrogenase, and no CO₂ is released; CO₂ is released in "
               "alcoholic fermentation.",
               ["Statement I: true", "Statement II: false, lactic acid fermentation releases no CO₂"],
               ncert=ref("RES", "Fermentation; The Respiratory Balance Sheet"), secs=30)

numerical(T_RES, "Glycolysis and fermentation", "Intermediate",
          "Yeast cells ferment 3 molecules of glucose under anaerobic conditions. Each molecule of pyruvic acid is "
          "converted by pyruvic acid decarboxylase and alcohol dehydrogenase to one molecule of CO₂ and one of "
          "ethanol. How many molecules of ethanol and of CO₂ are produced in all?",
          "6 ethanol and 6 CO₂",
          ["3 ethanol and 3 CO₂", "6 ethanol and 18 CO₂", "6 ethanol and 12 CO₂"], "D",
          (3 * 2 * 1 == 6),
          "Products of alcoholic fermentation",
          "Glycolysis splits each glucose into 2 molecules of pyruvic acid, so 3 glucose give 6 pyruvic acid. In "
          "alcoholic fermentation each pyruvic acid gives one CO₂ and one ethanol, so 6 ethanol and 6 CO₂ are formed.",
          ["3 glucose × 2 = 6 pyruvic acid", "6 pyruvic acid → 6 ethanol + 6 CO₂"],
          why="3 and 3 forgets that each glucose gives two pyruvic acid. 18 CO₂ is what complete aerobic oxidation of "
              "3 glucose would release. 12 CO₂ wrongly counts two CO₂ per pyruvic acid.",
          ncert=ref("RES", "Glycolysis; Fermentation"), secs=50)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "In alcoholic fermentation, NADH + H⁺ is produced when pyruvic acid is converted to ethanol.",
                 "In both lactic acid and alcoholic fermentation, the reducing agent NADH + H⁺ is reoxidised to "
                 "NAD⁺.",
                 False, True, False, "D",
                 "Role of NADH in fermentation",
                 "In fermentation, the NADH + H⁺ formed in glycolysis (when PGAL is oxidised to BPGA) is used as the "
                 "reducing agent and is reoxidised to NAD⁺ when pyruvic acid is converted to ethanol (or to lactic "
                 "acid). So NADH is consumed, not produced, in that step: A is false, R is true.",
                 ["A: false, NADH is oxidised when ethanol is formed", "R: true"],
                 ncert=ref("RES", "Fermentation"), secs=40)

multi_statement(T_RES, "Electron transport system", "Intermediate",
                "Which of the following statements about the sites of the steps of respiration are correct?",
                [("Glycolysis takes place in the cytoplasm.", True),
                 ("The oxidative decarboxylation of pyruvic acid takes place in the mitochondrial matrix.", True),
                 ("The TCA cycle takes place in the mitochondrial matrix.", True),
                 ("The electron transport system is located in the outer mitochondrial membrane.", False),
                 ("Fermentation takes place in the mitochondrial matrix.", False)],
                ["abd", "bce", "acde"], "A",
                "Sites of respiration",
                "Glycolysis occurs in the cytoplasm and is present in all living organisms. Pyruvic acid enters the "
                "mitochondrial matrix, where it undergoes oxidative decarboxylation and the TCA cycle. The "
                "electron transport system is present in the inner mitochondrial membrane. Fermentation, like "
                "glycolysis, takes place in the cytoplasm, without the involvement of mitochondria.",
                ["(a), (b), (c): true", "(d): false, ETS is in the inner membrane",
                 "(e): false, fermentation is cytoplasmic"],
                why="Each wrong combination contains (d) or (e), or omits a true statement.",
                ncert=ref("RES", "Glycolysis; Fermentation; Aerobic Respiration"), secs=50)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
               "Calculating the net gain of ATP for every glucose molecule oxidised remains, in reality, only a "
               "theoretical exercise.",
               "In a living system, the pathways of respiration work simultaneously and do not take place one after "
               "another.",
               True, True, "A",
               "Limits of the respiratory balance sheet",
               "The ATP balance sheet assumes a sequential, orderly pathway, oxidation of glycolytic NADH in the "
               "mitochondria and no withdrawal of intermediates. These assumptions are not really valid in a living "
               "system: all pathways work simultaneously and do not take place one after another, substrates enter "
               "and intermediates are withdrawn as necessary, and ATP is used as needed. So the calculation can "
               "remain only a theoretical exercise.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "The Respiratory Balance Sheet"), secs=35)

numerical(T_RES, "Respiratory quotient", "Intermediate",
          "Germinating seeds are respiring fat, whose respiratory quotient (RQ) is 0.7. In one hour they consume "
          "250 mL of O₂. What volume of CO₂ do they evolve in the same time?",
          "175 mL",
          ["250 mL", "357 mL", "75 mL"], "B",
          (abs(250 * 0.7 - 175) < 1e-9),
          "Using the respiratory quotient",
          "RQ = volume of CO₂ evolved / volume of O₂ consumed. So CO₂ evolved = RQ × O₂ consumed = 0.7 × 250 mL = "
          "175 mL. When fats are used in respiration the RQ is less than 1, so less CO₂ is evolved than O₂ is "
          "consumed.",
          ["RQ = CO₂ / O₂", "CO₂ = 0.7 × 250 = 175 mL"],
          why="250 mL assumes RQ = 1 (carbohydrate). 357 mL comes from dividing by 0.7 instead of multiplying. "
              "75 mL is the difference between O₂ consumed and CO₂ evolved, not the CO₂ itself.",
          ncert=ref("RES", "Respiratory Quotient"), secs=45)

match_list(T_RES, "TCA cycle", "Advanced", "step of the TCA cycle", "what happens",
           ["Acetyl CoA + oxaloacetic acid + H₂O → citric acid", "Citric acid → isocitric acid",
            "Succinyl CoA → succinic acid", "α-Ketoglutaric acid → succinyl CoA"],
           ["Synthesis of a molecule of GTP", "Isomerisation", "Condensation catalysed by citrate synthase",
            "Decarboxylation"],
           "III II I IV", ["II III I IV", "III II IV I", "III I II IV"], "A",
           "Steps of the TCA cycle",
           "The TCA cycle starts with the condensation of the acetyl group with oxaloacetic acid and water to yield "
           "citric acid, catalysed by citrate synthase. Citrate is then isomerised to isocitrate. Two successive "
           "decarboxylations follow, forming α-ketoglutaric acid and then succinyl CoA. During the conversion of "
           "succinyl CoA to succinic acid, a molecule of GTP is synthesised (substrate level phosphorylation).",
           ["Condensation → citric acid", "Isomerisation → isocitric acid", "Decarboxylation → succinyl CoA",
            "Succinyl CoA → succinic acid: GTP"],
           why="The wrong codes interchange condensation and isomerisation, or the GTP-forming step and a "
               "decarboxylation.",
           ncert=ref("RES", "Tricarboxylic Acid Cycle"), secs=50)

direct(T_RES, "TCA cycle", "Advanced",
       "Which of the following is NOT formed in the mitochondrial matrix of a plant cell during aerobic respiration?",
       "Pyruvic acid",
       ["Acetyl CoA", "α-Ketoglutaric acid", "Succinyl CoA"], "D",
       "Sites of formation of respiratory intermediates",
       "Pyruvic acid is the end product of glycolysis, which takes place in the cytoplasm; it is then transported "
       "into the mitochondria. Acetyl CoA is formed from it in the matrix by oxidative decarboxylation, and "
       "α-ketoglutaric acid and succinyl CoA are formed in the matrix during the TCA cycle.",
       ["Pyruvic acid → cytoplasm (glycolysis)", "Acetyl CoA, α-KG, succinyl CoA → matrix"],
       why="Acetyl CoA, α-ketoglutaric acid and succinyl CoA are all formed inside the mitochondrial matrix.",
       ncert=ref("RES", "Glycolysis; Aerobic Respiration; Tricarboxylic Acid Cycle"), secs=40)

multi_statement(T_RES, "Glycolysis and fermentation", "Advanced",
                "In which of the following is the NADH + H⁺ formed in glycolysis reoxidised to NAD⁺ in the cytoplasm, "
                "without the involvement of oxygen?",
                [("Yeast cells growing under anaerobic conditions", True),
                 ("Animal muscle cells during exercise when oxygen is inadequate", True),
                 ("Bacteria that produce lactic acid from pyruvic acid", True),
                 ("A well-aerated plant cell carrying out complete aerobic respiration, as assumed in the "
                  "respiratory balance sheet", False),
                 ("A cell in which pyruvic acid is converted to acetyl CoA in the mitochondrial matrix", False)],
                ["abd", "bce", "abcd"], "D",
                "Regeneration of NAD⁺",
                "In fermentation (yeast under anaerobic conditions, animal muscle with inadequate oxygen, and some "
                "bacteria producing lactic acid), the NADH + H⁺ of glycolysis is reoxidised to NAD⁺ in the cytoplasm "
                "when pyruvic acid is reduced to ethanol or lactic acid. In aerobic respiration, the balance sheet "
                "assumes that glycolytic NADH is transferred into the mitochondria and oxidised through the ETS, "
                "with oxygen as the final acceptor; acetyl CoA formation itself takes place in the matrix.",
                ["Fermenting cells: NAD⁺ regenerated in cytoplasm without O₂",
                 "Aerobic cells: NADH oxidised in mitochondria with O₂"],
                why="Statements (d) and (e) describe aerobic conditions, where NADH is oxidised in the mitochondria "
                    "with oxygen as the final acceptor.",
                ncert=ref("RES", "Fermentation; Aerobic Respiration; The Respiratory Balance Sheet"), secs=60)


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
    assert pkg["output"] == "batches/parts/BATCH_006_BOT_p1.json"


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
           "notes": "Package BOT_006_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 122 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
