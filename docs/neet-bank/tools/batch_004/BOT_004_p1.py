"""Writes batches/parts/BATCH_004_BOT_p1.json: package BOT_004_p1 of batch 4 (Botany, 123 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_000751 .. NEET_BOT_000873.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books (secondary growth, taxonomical aids, plant life cycles and alternation of generations, early
experiments on photosynthesis) is not used. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_004/BOT_004_p1.py
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
PLAN = ROOT / "batches" / "plans" / "BATCH_004_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_004_BOT_p1.json"
PACKAGE = "BOT_004_p1"
BATCH = "BATCH_004"
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


# =============================================================== 1. The Living World and Classification (5/7/5)
direct(T_LIV, "Binomial nomenclature", "Basic",
       "The scientific names of animals are given according to the principles and criteria laid down in the:",
       "International Code of Zoological Nomenclature (ICZN)",
       ["International Code for Botanical Nomenclature (ICBN)", "Five kingdom classification of Whittaker",
        "Two kingdom classification of Linnaeus"], "B",
       "Codes of nomenclature",
       "Names of plants follow the International Code for Botanical Nomenclature (ICBN). Animal taxonomists have "
       "evolved the International Code of Zoological Nomenclature (ICZN), which ensures that each animal has a "
       "distinct name recognised the world over.",
       ["Plants → ICBN", "Animals → ICZN"],
       why="ICBN applies to plants, not animals. The five kingdom and two kingdom systems are schemes of "
           "classification, not codes for naming.",
       ncert=ref("LW", "Nomenclature"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "In taxonomy, each category, referred to as a unit of classification, represents a rank and is commonly "
       "termed a:",
       "taxon", ["specific epithet", "binomial", "phylum"], "D",
       "Taxonomic categories",
       "Classification involves a hierarchy of steps in which each step represents a rank or category. Each "
       "category, referred to as a unit of classification, represents a rank and is commonly termed a taxon "
       "(plural: taxa).",
       ["Unit of classification representing a rank = taxon"],
       why="The specific epithet is the second word of a scientific name. A binomial is the two-word name itself. "
           "A phylum is only one particular category, not the general term for every category.",
       ncert=ref("LW", "Taxonomic Categories"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Which of the following plant diseases is named by NCERT as a disease caused by bacteria?",
       "Citrus canker",
       ["Wheat rust", "White rust of mustard", "Potato spindle tuber disease"], "A",
       "Bacteria as pathogens",
       "Some bacteria are pathogens of human beings, crops, farm animals and pets. Cholera, typhoid, tetanus and "
       "citrus canker are well-known diseases caused by different bacteria.",
       ["Citrus canker → bacterium"],
       why="Wheat rust is caused by the fungus Puccinia. White rust of mustard is caused by the fungus Albugo. "
           "Potato spindle tuber disease is caused by a viroid.",
       ncert=ref("BC", "Kingdom Monera (Eubacteria)"), secs=25)

direct(T_LIV, "Lichens, viruses and viroids", "Basic",
       "The name 'virus', given to the infectious agents that pass through bacteria-proof filters, means:",
       "venom or poisonous fluid",
       ["infectious living fluid", "small living cell", "crystalline protein"], "C",
       "Meaning of the term virus",
       "NCERT states that the name virus, which means venom or poisonous fluid, was given to these agents.",
       ["virus = venom or poisonous fluid"],
       why="'Infectious living fluid' is Beijerinek's term 'Contagium vivum fluidum', not the meaning of 'virus'. "
           "Viruses are not cells. Crystals of virus are largely protein, but that is not what the name means.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=20)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Basic",
               "The parasitic flagellated protozoan Trypanosoma causes sleeping sickness.",
               "Marine forms of amoeboid protozoans have silica shells on their surface.",
               True, True, "A",
               "Protozoans",
               "Flagellated protozoans are free-living or parasitic; the parasitic forms cause diseases such as "
               "sleeping sickness, e.g., Trypanosoma. Amoeboid protozoans live in fresh water, sea water or moist "
               "soil and move by pseudopodia; marine forms have silica shells on their surface.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("BC", "Kingdom Protista (Protozoans)"), secs=30)

match_list(T_LIV, "Taxonomy and hierarchy", "Intermediate", "taxon to which mango belongs", "taxonomic category",
           ["Mangifera", "Anacardiaceae", "Sapindales", "Dicotyledonae"],
           ["Order", "Class", "Genus", "Family"],
           "III IV I II", ["III I IV II", "IV III I II", "III IV II I"], "C",
           "Taxonomic hierarchy of mango",
           "In the NCERT table of organisms with their taxonomic categories, mango (Mangifera indica) is placed in "
           "genus Mangifera, family Anacardiaceae, order Sapindales and class Dicotyledonae (division "
           "Angiospermae).",
           ["Mangifera → genus", "Anacardiaceae → family (-aceae)", "Sapindales → order (-ales)",
            "Dicotyledonae → class"],
           why="The wrong codes swap family and order, genus and family, or order and class. The endings help: "
               "plant families end in -aceae and orders in -ales.",
           ncert=ref("LW", "Taxonomic Categories (Table 1.1)"), secs=40,
           )

match_list(T_LIV, "Five kingdom classification", "Intermediate", "kingdom", "mode of nutrition",
           ["Monera", "Fungi", "Plantae", "Animalia"],
           ["Heterotrophic (holozoic, saprophytic, etc.)", "Autotrophic (photosynthetic)",
            "Heterotrophic (saprophytic or parasitic)",
            "Autotrophic (chemosynthetic and photosynthetic) and heterotrophic"],
           "IV III II I", ["II III IV I", "IV I II III", "IV III I II"], "A",
           "Characteristics of the five kingdoms",
           "Whittaker's table of the five kingdoms gives the mode of nutrition of Monera as autotrophic "
           "(chemosynthetic and photosynthetic) and heterotrophic; of Fungi as heterotrophic (saprophytic or "
           "parasitic); of Plantae as autotrophic (photosynthetic); and of Animalia as heterotrophic (holozoic, "
           "saprophytic, etc.).",
           ["Monera → IV", "Fungi → III", "Plantae → II", "Animalia → I"],
           why="Plants are photosynthetic, not chemosynthetic. Fungi absorb food (saprophytic or parasitic) rather "
               "than ingest it (holozoic). Only Monera includes chemosynthetic autotrophs.",
           ncert=ref("BC", "Introduction (Table 2.1: Characteristics of the Five Kingdoms)"), secs=45)

statement_pair(T_LIV, "What is living", "Intermediate",
               "In the majority of higher animals and plants, growth and reproduction are mutually exclusive events.",
               "In unicellular organisms such as bacteria and Amoeba, growth and reproduction are clearly separate, "
               "mutually exclusive events.",
               True, False, "C",
               "Growth and reproduction",
               "In the majority of higher animals and plants, growth and reproduction are mutually exclusive events. "
               "In unicellular organisms such as bacteria, unicellular algae or Amoeba, reproduction is synonymous "
               "with growth, i.e., increase in the number of cells, so the two terms are not clearly separable.",
               ["Statement I: true", "Statement II: false, in unicellular organisms reproduction is synonymous "
                                     "with growth"],
               ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=40)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "In phycomycetes, asexual reproduction may take place by non-motile spores produced endogenously in a "
       "sporangium. These spores are called:",
       "aplanospores", ["zoospores", "conidia", "ascospores"], "B",
       "Asexual spores of phycomycetes",
       "In phycomycetes, asexual reproduction takes place by zoospores (motile) or by aplanospores (non-motile). "
       "These spores are produced endogenously in a sporangium.",
       ["Motile → zoospores", "Non-motile → aplanospores"],
       why="Zoospores are the motile spores. Conidia are asexual spores produced exogenously on conidiophores "
           "(ascomycetes, deuteromycetes). Ascospores are the sexual spores of ascomycetes.",
       ncert=ref("BC", "Kingdom Fungi (Phycomycetes)"), secs=30)

direct(T_LIV, "Taxonomy and hierarchy", "Intermediate",
       "In the NCERT table of organisms with their taxonomic categories, man (Homo sapiens) and the housefly "
       "(Musca domestica) are placed together in the same:",
       "kingdom Animalia", ["phylum Chordata", "class Insecta", "order Primata"], "D",
       "Taxonomic hierarchy",
       "Man: family Hominidae, order Primata, class Mammalia, phylum Chordata. Housefly: family Muscidae, order "
       "Diptera, class Insecta, phylum Arthropoda. The two share only the kingdom, Animalia.",
       ["Man: Chordata, Mammalia, Primata", "Housefly: Arthropoda, Insecta, Diptera",
        "Common category: kingdom Animalia"],
       why="Chordata and Primata hold man but not the housefly. Insecta holds the housefly but not man.",
       ncert=ref("LW", "Taxonomic Categories (Table 1.1)"), secs=35)

assertion_reason(T_LIV, "Lichens, viruses and viroids", "Intermediate",
                 "Acellular organisms such as viruses and viroids find no mention in Whittaker's five kingdom "
                 "classification.",
                 "Whittaker's kingdoms are defined using characters such as cell structure, body organisation and "
                 "mode of nutrition, which acellular particles do not possess.",
                 True, True, True, "A",
                 "Viruses and classification",
                 "NCERT notes that the five kingdom classification does not mention lichens and some acellular "
                 "organisms such as viruses, viroids and prions. Viruses did not find a place in classification "
                 "because they are not considered truly 'living' if we understand living as having a cell "
                 "structure. R gives the reason for A.",
                 ["A: true", "R: true", "Lack of cell structure → no place in the classification → R explains A"],
                 ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "Mushrooms, bracket fungi and puffballs are commonly known forms of:",
       "basidiomycetes", ["ascomycetes", "phycomycetes", "deuteromycetes"], "B",
       "Basidiomycetes",
       "NCERT states that the commonly known forms of basidiomycetes are mushrooms, bracket fungi or puffballs. "
       "They grow in soil, on logs and tree stumps, and in living plant bodies as parasites (rusts and smuts).",
       ["Mushrooms, bracket fungi, puffballs → basidiomycetes"],
       why="Ascomycetes include yeast, Penicillium, Aspergillus, Claviceps, Neurospora, morels and truffles. "
           "Phycomycetes include Mucor, Rhizopus and Albugo. Deuteromycetes include Alternaria, Colletotrichum "
           "and Trichoderma.",
       ncert=ref("BC", "Kingdom Fungi (Basidiomycetes)"), secs=30)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Advanced",
                "Which of the following statements about fungi are correct?",
                [("Some ascomycetes are coprophilous, that is, they grow on dung.", True),
                 ("In ascomycetes, the asci are arranged in different types of fruiting bodies called ascocarps.",
                  True),
                 ("Claviceps and Aspergillus are members of ascomycetes.", True),
                 ("Ustilago, the smut fungus, is a member of phycomycetes.", False),
                 ("Trichoderma is a member of deuteromycetes.", True)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("b", "c", "d", "e")], "C",
                "Classes of fungi",
                "Ascomycetes are saprophytic, decomposers, parasitic or coprophilous (growing on dung); their asci "
                "are arranged in fruiting bodies called ascocarps; examples include Aspergillus, Claviceps and "
                "Neurospora. Ustilago (smut) is a basidiomycete, as are Agaricus and Puccinia. Trichoderma, with "
                "Alternaria and Colletotrichum, is a deuteromycete.",
                ["(a) true", "(b) true", "(c) true", "(d) false: Ustilago is a basidiomycete", "(e) true"],
                why="Options with (d) contain the false statement. (a), (b) and (c) only leaves out the true "
                    "statement (e).",
                ncert=ref("BC", "Kingdom Fungi"), secs=60)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Advanced",
                "Which of the following statements about kingdom Protista are correct?",
                [("Members of Protista are primarily aquatic.", True),
                 ("The kingdom forms a link with the kingdoms dealing with plants, animals and fungi.", True),
                 ("Protists reproduce asexually and sexually by a process involving cell fusion and zygote "
                  "formation.", True),
                 ("The pigments of euglenoids are identical to those present in higher plants.", True),
                 ("Protozoans are believed to be primitive relatives of plants.", False)],
                [("a", "b", "d", "e"), ("a", "c", "d"), ("b", "c", "d", "e")], "B",
                "Kingdom Protista",
                "All single-celled eukaryotes are placed under Protista. Its members are primarily aquatic, and the "
                "kingdom forms a link with plants, animals and fungi. Protists reproduce asexually and sexually by "
                "cell fusion and zygote formation. The pigments of euglenoids are identical to those of higher "
                "plants. Protozoans are heterotrophs and are believed to be primitive relatives of animals, not "
                "plants.",
                ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: primitive relatives of animals"],
                why="Options with (e) contain the false statement. (a), (c) and (d) only leaves out the true "
                    "statement (b).",
                ncert=ref("BC", "Kingdom Protista"), secs=60)

direct(T_LIV, "Monera, Protista and Fungi", "Advanced",
       "A fungus has a septate, branched mycelium. It reproduces only by asexual spores called conidia, and its "
       "sexual stage is not known. Which of the following fungi fits this description?",
       "Colletotrichum", ["Claviceps", "Agaricus", "Mucor"], "D",
       "Deuteromycetes",
       "Fungi in which only the asexual or vegetative phases are known are placed in deuteromycetes. They "
       "reproduce only by asexual spores known as conidia, and their mycelium is septate and branched. NCERT "
       "examples are Alternaria, Colletotrichum and Trichoderma.",
       ["Only asexual phase known + conidia + septate mycelium → deuteromycete",
        "Colletotrichum is a deuteromycete"],
       why="Claviceps is an ascomycete, with a known sexual stage (ascospores). Agaricus is a basidiomycete "
           "(basidiospores). Mucor is a phycomycete with an aseptate, coenocytic mycelium.",
       ncert=ref("BC", "Kingdom Fungi (Deuteromycetes)"), secs=45)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "All members of kingdom Monera are heterotrophic.",
                 "Bacteria are the sole members of kingdom Monera.",
                 False, True, False, "D",
                 "Kingdom Monera",
                 "Bacteria are the sole members of kingdom Monera, so R is true. But Monera includes autotrophs "
                 "as well: cyanobacteria are photosynthetic autotrophs and some bacteria are chemosynthetic "
                 "autotrophs. Table 2.1 gives the nutrition of Monera as autotrophic (chemosynthetic and "
                 "photosynthetic) and heterotrophic. So A is false.",
                 ["A: false (cyanobacteria and chemosynthetic bacteria are autotrophs)", "R: true"],
                 ncert=ref("BC", "Kingdom Monera"), secs=40)

statement_pair(T_LIV, "Five kingdom classification", "Advanced",
               "Kingdom Plantae includes all eukaryotic, chlorophyll-containing organisms, a few of which are "
               "partially heterotrophic, such as insectivorous plants and parasites.",
               "Bladderwort and Venus fly trap are, like Cuscuta, parasitic plants.",
               True, False, "C",
               "Kingdom Plantae",
               "Kingdom Plantae includes all eukaryotic chlorophyll-containing organisms commonly called plants. A "
               "few members are partially heterotrophic: bladderwort and Venus fly trap are insectivorous plants, "
               "while Cuscuta is a parasite.",
               ["Statement I: true", "Statement II: false, bladderwort and Venus fly trap are insectivorous"],
               ncert=ref("BC", "Kingdom Plantae"), secs=40)

# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "Besides water, algae occur in other habitats, and some occur in association with fungi or animals. NCERT "
       "gives which of the following as an example of algae growing in association with an animal?",
       "Algae on the sloth bear",
       ["Algae in the coralloid roots of Cycas", "Algae in the gut of ruminants", "Algae on the roots of Pinus"],
       "A",
       "Habitats of algae",
       "Algae are largely aquatic, but they also occur on moist stones, soils and wood. Some occur in association "
       "with fungi (lichen) and animals (e.g., on sloth bear).",
       ["Association with animals → on the sloth bear"],
       why="Coralloid roots of Cycas hold N₂-fixing cyanobacteria, and Cycas is not an animal. The gut of "
           "ruminants holds methanogens (archaebacteria). Pinus roots have fungal mycorrhiza.",
       ncert=ref("PK", "Algae"), secs=25)

direct(T_PK, "Bryophytes", "Basic",
       "Bryophytes, which include mosses and liverworts, are found commonly growing in:",
       "moist, shaded areas in the hills",
       ["dry, sandy deserts", "the open sea", "hot springs"], "C",
       "Habitat of bryophytes",
       "NCERT describes bryophytes as including the various mosses and liverworts that are found commonly growing "
       "in moist shaded areas in the hills.",
       ["Bryophytes → moist, shaded areas in the hills"],
       why="Bryophytes need water for fertilisation and are not desert or marine plants. Hot springs are a habitat "
           "of thermoacidophile archaebacteria.",
       ncert=ref("PK", "Bryophytes"), secs=20)

direct(T_PK, "Pteridophytes", "Basic",
       "In heterosporous pteridophytes, the megaspores germinate to give rise to:",
       "female gametophytes",
       ["male gametophytes", "sporophytes directly", "strobili"], "B",
       "Heterospory in pteridophytes",
       "Genera like Selaginella and Salvinia produce two kinds of spores, macro (large) and micro (small) "
       "spores. The megaspores and microspores germinate and give rise to female and male gametophytes, "
       "respectively.",
       ["Megaspore → female gametophyte", "Microspore → male gametophyte"],
       why="Male gametophytes come from microspores. Spores give gametophytes, not sporophytes. Strobili are "
           "compact groups of sporophylls on the sporophyte.",
       ncert=ref("PK", "Pteridophytes"), secs=20)

direct(T_PK, "Gymnosperms", "Basic",
       "In gymnosperms, the cones bearing megasporophylls with ovules (megasporangia) are called:",
       "macrosporangiate or female strobili",
       ["microsporangiate or male strobili", "gemma cups", "coralloid roots"], "D",
       "Strobili of gymnosperms",
       "Gymnosperms are heterosporous. The strobili bearing microsporophylls and microsporangia are called "
       "microsporangiate or male strobili. The cones bearing megasporophylls with ovules or megasporangia are "
       "called macrosporangiate or female strobili.",
       ["Megasporophylls with ovules → macrosporangiate (female) strobili"],
       why="Male strobili bear microsporophylls. Gemma cups are receptacles of gemmae on liverwort thalli. "
           "Coralloid roots of Cycas hold cyanobacteria.",
       ncert=ref("PK", "Gymnosperms"), secs=20)

statement_pair(T_PK, "Algae", "Basic",
               "Being photosynthetic, algae increase the level of dissolved oxygen in their immediate environment.",
               "Algae also occur on moist stones, soils and wood.",
               True, True, "A",
               "Algae",
               "Algae carry out photosynthesis, so they increase the dissolved oxygen in their immediate "
               "environment. Though largely aquatic (fresh water and marine), they also occur in other habitats "
               "such as moist stones, soils and wood.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Algae"), secs=30)

match_list(T_PK, "Algae", "Intermediate", "plant", "description",
           ["Fucus", "Lycopodium", "Cedrus", "Chlamydomonas"],
           ["Gymnosperm with a branched stem", "Unicellular green alga", "Brown alga",
            "Pteridophyte of the class Lycopsida"],
           "III IV I II", ["II IV I III", "III I IV II", "IV III I II"], "B",
           "Examples of plant groups",
           "Fucus is a member of Phaeophyceae (brown algae). Lycopodium, with Selaginella, belongs to Lycopsida. "
           "Cedrus, like Pinus, is a gymnosperm with a branched stem (Cycas is unbranched). Chlamydomonas is a "
           "unicellular green alga (Chlorophyceae).",
           ["Fucus → brown alga", "Lycopodium → Lycopsida", "Cedrus → gymnosperm, branched stem",
            "Chlamydomonas → unicellular green alga"],
           why="The wrong codes treat Fucus as a green alga, Lycopodium as a gymnosperm, or Cedrus as a "
               "pteridophyte.",
           ncert=ref("PK", "Algae; Pteridophytes; Gymnosperms"), secs=40)

statement_pair(T_PK, "Bryophytes", "Intermediate",
               "The protonema of a moss is a creeping, green, branched and frequently filamentous stage.",
               "The leafy stage of a moss consists of upright, slender axes bearing leaves arranged in two rows.",
               True, False, "C",
               "Gametophyte of mosses",
               "The first stage of the moss gametophyte, the protonema, develops directly from a spore and is a "
               "creeping, green, branched and frequently filamentous stage. The leafy stage consists of upright, "
               "slender axes bearing spirally arranged leaves. (Leaf-like appendages in two rows are found in "
               "leafy liverworts.)",
               ["Statement I: true", "Statement II: false, the leaves of the moss leafy stage are spirally "
                                     "arranged"],
               ncert=ref("PK", "Bryophytes (Mosses)"), secs=40)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Members of Phaeophyceae are only rarely found in fresh water.",
                 "In brown algae, the protoplast contains, in addition to plastids, a centrally located vacuole "
                 "and nucleus.",
                 True, True, False, "B",
                 "Phaeophyceae",
                 "NCERT's table of algal classes gives the habitat of Phaeophyceae as fresh water (rare), brackish "
                 "water and salt water, so A is true. R is also true: the protoplast of brown algae contains, "
                 "besides plastids, a centrally located vacuole and nucleus. R describes the structure of the "
                 "cell and says nothing about where the algae live, so it does not explain A.",
                 ["A: true", "R: true", "R is about cell structure, A about habitat → R does not explain A"],
                 ncert=ref("PK", "Algae (Phaeophyceae; Table 3.1)"), secs=45)

direct(T_PK, "Gymnosperms", "Intermediate",
       "In gymnosperms, the nucellus together with the envelopes that protect it forms a composite structure "
       "called:",
       "an ovule", ["a megasporophyll", "a female strobilus", "an archegonium"], "C",
       "Ovule of gymnosperms",
       "The megaspore mother cell is differentiated from one of the cells of the nucellus. The nucellus is "
       "protected by envelopes, and the composite structure is called an ovule. Ovules are borne on "
       "megasporophylls, which may be clustered to form female cones.",
       ["Nucellus + protective envelopes = ovule"],
       why="A megasporophyll is the structure that bears ovules. A female strobilus is a cluster of "
           "megasporophylls. An archegonium is a female sex organ borne on the female gametophyte.",
       ncert=ref("PK", "Gymnosperms"), secs=30)

direct(T_PK, "Algae", "Intermediate",
       "In members of Chlorophyceae, pyrenoids in the chloroplasts contain protein besides starch. In addition, "
       "some green algae may store food in the form of:",
       "oil droplets", ["laminarin", "floridean starch", "mannitol"], "A",
       "Stored food in green algae",
       "Most green algae have one or more storage bodies called pyrenoids located in the chloroplasts; "
       "pyrenoids contain protein besides starch. Some algae may store food in the form of oil droplets.",
       ["Green algae: starch (pyrenoids) and, in some, oil droplets"],
       why="Laminarin and mannitol are stored by brown algae (Phaeophyceae). Floridean starch is stored by red "
           "algae (Rhodophyceae).",
       ncert=ref("PK", "Algae (Chlorophyceae)"), secs=30)

multi_statement(T_PK, "Gymnosperms", "Intermediate",
                "Which of the following statements about gymnosperms are correct?",
                [("The roots are generally tap roots.", True),
                 ("The stem is unbranched in Cycas but branched in Pinus and Cedrus.", True),
                 ("The sporophylls are arranged spirally along an axis to form lax or compact cones (strobili).",
                  True),
                 ("The seeds formed after fertilisation are enclosed within a fruit.", False),
                 ("The leaves are always compound.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "e")], "D",
                "Gymnosperms",
                "Gymnosperm roots are generally tap roots. The stem is unbranched (Cycas) or branched (Pinus, "
                "Cedrus). The sporophylls are arranged spirally along an axis to form lax or compact cones. The "
                "ovules are not enclosed by an ovary wall, so the seeds are not covered (no fruit forms). The "
                "leaves may be simple or compound.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the seeds are naked", "(e) false: simple or "
                                                                                       "compound"],
                why="Every wrong option includes (d) or (e), which are false.",
                ncert=ref("PK", "Gymnosperms"), secs=55)

statement_pair(T_PK, "Algae", "Intermediate",
               "Members of Rhodophyceae reproduce sexually by non-motile gametes.",
               "Brown algae range from simple, branched, filamentous forms such as Ectocarpus to profusely branched "
               "forms such as kelps.",
               True, True, "A",
               "Red and brown algae",
               "Red algae reproduce vegetatively by fragmentation, asexually by non-motile spores and sexually by "
               "non-motile gametes. Brown algae show great variation in size and form, from simple branched "
               "filamentous forms (Ectocarpus) to profusely branched forms represented by kelps.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Algae (Phaeophyceae; Rhodophyceae)"), secs=40)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following statements about the pigments and flagella of algae are correct?",
                [("Members of Phaeophyceae contain chlorophyll a and c, carotenoids and xanthophylls.", True),
                 ("Members of Chlorophyceae have 2–8 equal, apical flagella.", True),
                 ("Chlorophyll b is present in members of Phaeophyceae.", False),
                 ("Chlorophyll a is present in members of all three classes, Chlorophyceae, Phaeophyceae and "
                  "Rhodophyceae.", True),
                 ("Members of Phaeophyceae have 2–8 equal, apical flagella.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "c", "d", "e")], "B",
                "Divisions of algae and their main characteristics",
                "NCERT's table of algae: Chlorophyceae have chlorophyll a and b and 2–8 equal, apical flagella; "
                "Phaeophyceae have chlorophyll a and c and fucoxanthin, with 2 unequal, lateral flagella; "
                "Rhodophyceae have chlorophyll a and d and phycoerythrin, and no flagella. Chlorophyll a is common "
                "to all three. Brown algae have chlorophyll a and c, not b.",
                ["(a) true", "(b) true", "(c) false: chlorophyll b belongs to green algae",
                 "(d) true", "(e) false: brown algae have 2 unequal, lateral flagella"],
                why="Options with (c) or (e) include a false statement; the remaining combination must contain "
                    "(a), (b) and (d).",
                ncert=ref("PK", "Algae (Table 3.1: Divisions of Algae and their Main Characteristics)"), secs=70)

assertion_reason(T_PK, "Algae", "Advanced",
                 "Algae form the basis of the food cycles of all aquatic animals.",
                 "Algae are photosynthetic and are primary producers of energy-rich compounds.",
                 True, True, True, "A",
                 "Importance of algae",
                 "NCERT states that algae are of paramount importance as primary producers of energy-rich "
                 "compounds which form the basis of the food cycles of all aquatic animals. Because they make "
                 "these compounds by photosynthesis, they stand at the base of aquatic food cycles; R explains A.",
                 ["A: true", "R: true", "Primary producers → base of food cycles → R explains A"],
                 ncert=ref("PK", "Algae"), secs=40)

direct(T_PK, "Pteridophytes", "Advanced",
       "Which feature is shared by bryophytes and pteridophytes but is NOT found in gymnosperms?",
       "A gametophyte with an independent, free-living existence",
       ["A dominant sporophyte with true roots, stems and leaves", "Vascular tissues, xylem and phloem",
        "Spores produced by meiosis in sporangia"], "C",
       "Comparing the gametophytes of the plant groups",
       "In bryophytes the gametophyte is the main plant body, and in pteridophytes the gametophyte (prothallus) "
       "is small, multicellular and free-living. Unlike bryophytes and pteridophytes, in gymnosperms the male and "
       "female gametophytes do not have an independent free-living existence; they remain within the sporangia "
       "retained on the sporophytes.",
       ["Bryophytes: free-living gametophyte (main plant body)", "Pteridophytes: free-living prothallus",
        "Gymnosperms: gametophytes retained within sporangia"],
       why="A dominant sporophyte with true organs and vascular tissues is found in pteridophytes and gymnosperms "
           "but not in bryophytes. Spores formed by meiosis in sporangia occur in all three groups.",
       ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=50)

statement_pair(T_PK, "Gymnosperms", "Advanced",
               "In gymnosperms, following fertilisation, the zygote develops into an embryo and the ovules into "
               "seeds.",
               "In gymnosperms, the ovules are borne on microsporophylls.",
               True, False, "C",
               "Gymnosperm reproduction",
               "Following fertilisation, the zygote develops into an embryo and the ovules into seeds, which are not "
               "covered. The ovules are borne on megasporophylls, which may be clustered to form female cones; "
               "microsporophylls bear microsporangia.",
               ["Statement I: true", "Statement II: false, ovules are borne on megasporophylls"],
               ncert=ref("PK", "Gymnosperms"), secs=40)

direct(T_PK, "Gymnosperms", "Advanced",
       "Which sequence correctly shows the development of the female gametophyte in a gymnosperm?",
       "Nucellus cell → megaspore mother cell → four megaspores by meiosis → one megaspore forms a multicellular "
       "female gametophyte bearing archegonia",
       ["Nucellus cell → four megaspores by mitosis → megaspore mother cell → female gametophyte bearing "
        "antheridia",
        "Megasporophyll → pollen grain → megaspore mother cell → female gametophyte shed from the ovule",
        "Megaspore mother cell → two megaspores by meiosis → both form free-living female gametophytes"], "D",
       "Megasporogenesis in gymnosperms",
       "The megaspore mother cell is differentiated from one of the cells of the nucellus. It divides "
       "meiotically to form four megaspores. One of the megaspores, enclosed within the megasporangium, develops "
       "into a multicellular female gametophyte that bears two or more archegonia. The female gametophyte is "
       "retained within the megasporangium.",
       ["Nucellus → MMC", "MMC → 4 megaspores (meiosis)", "1 megaspore → female gametophyte with 2 or more "
                                                          "archegonia"],
       why="The megaspores are formed by meiosis, not mitosis, and the female gametophyte bears archegonia, not "
           "antheridia. Pollen grains are male gametophytes and the female gametophyte is retained, not shed. "
           "Meiosis gives four megaspores, and gymnosperm gametophytes are not free-living.",
       ncert=ref("PK", "Gymnosperms"), secs=50)

# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Root, stem and leaf", "Basic",
       "In plants such as grass, Monstera and the banyan tree, roots arise from parts of the plant other than the "
       "radicle. Such roots are called:",
       "adventitious roots", ["tap roots", "lateral roots", "root hairs"], "D",
       "Adventitious roots",
       "In some plants, like grass, Monstera and the banyan tree, roots arise from parts of the plant other than "
       "the radicle and are called adventitious roots.",
       ["Roots not from the radicle → adventitious"],
       why="A tap root is the direct elongation of the radicle, and lateral roots are its branches. Root hairs are "
           "unicellular outgrowths of the epidermis, not roots.",
       ncert=ref("MOR", "The Root"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In which of the following plants does a slender lateral branch arise from the base of the main axis, "
       "grow aerially for some time and then arch downwards to touch the ground?",
       "Mint", ["Pistia", "Opuntia", "Ginger"], "B",
       "Stem modifications for vegetative propagation",
       "In plants like mint and jasmine, a slender lateral branch arises from the base of the main axis and, "
       "after growing aerially for some time, arches downwards to touch the ground.",
       ["Mint and jasmine → lateral branch arching down to the ground"],
       why="In Pistia, a lateral branch with short internodes bears a rosette of leaves and a tuft of roots at "
           "each node. Opuntia has a flattened green photosynthetic stem. Ginger has an underground stem that "
           "stores food.",
       ncert=ref("MOR", "The Stem (Modifications of Stem)"), secs=25)

statement_pair(T_MOR, "Root, stem and leaf", "Basic",
               "The fleshy leaves of onion and garlic store food.",
               "Leaves originate from the shoot apical meristem and are arranged in an acropetal order.",
               True, True, "A",
               "The leaf",
               "Leaves are often modified; the fleshy leaves of onion and garlic store food. A leaf is a lateral, "
               "generally flattened structure borne on the stem; leaves originate from shoot apical meristems and "
               "are arranged in an acropetal order.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Leaf"), secs=30)

direct(T_MOR, "Flower", "Basic",
       "The sepals of a flower are green and leaf-like. Their main function is to:",
       "protect the flower in the bud stage",
       ["attract insects for pollination", "produce pollen grains", "develop into the fruit wall"], "C",
       "Calyx",
       "The calyx is the outermost whorl of the flower and its members are called sepals. Generally, sepals are "
       "green, leaf-like and protect the flower in the bud stage.",
       ["Sepals → protection in the bud stage"],
       why="Attracting insects is the role of the usually brightly coloured corolla. Pollen grains are produced in "
           "the anthers. The fruit wall develops from the ovary wall.",
       ncert=ref("MOR", "Parts of a Flower (Calyx)"), secs=20)

assertion_reason(T_MOR, "Flower", "Basic",
                 "The corolla of a flower is usually brightly coloured.",
                 "Bright colours of the corolla attract insects for pollination.",
                 True, True, True, "A",
                 "Corolla",
                 "The corolla is composed of petals, which are usually brightly coloured to attract insects for "
                 "pollination. R gives the purpose that the bright colour serves.",
                 ["A: true", "R: true", "Colour attracts pollinating insects → R explains A"],
                 ncert=ref("MOR", "Parts of a Flower (Corolla)"), secs=30)

statement_pair(T_MOR, "Flower", "Intermediate",
               "Stamens united into two bundles, as in pea, are described as diadelphous.",
               "In mustard and tomato, the carpels of the gynoecium are free, so the gynoecium is apocarpous.",
               True, False, "C",
               "Androecium and gynoecium",
               "Stamens may be united into one bundle (monoadelphous, china rose), two bundles (diadelphous, pea) or "
               "more than two bundles (polyadelphous, citrus). Carpels are free (apocarpous) in lotus and rose, but "
               "fused (syncarpous) in mustard and tomato.",
               ["Statement I: true", "Statement II: false, mustard and tomato are syncarpous"],
               ncert=ref("MOR", "Parts of a Flower (Androecium; Gynoecium)"), secs=40)

match_list(T_MOR, "Flower", "Intermediate", "type of placentation", "description",
           ["Marginal", "Parietal", "Free central", "Basal"],
           ["Placenta develops at the base of the ovary and a single ovule is attached to it",
            "Ovules are borne on the central axis and septa are absent",
            "Ovules develop on the inner wall of the ovary or on its peripheral part",
            "Placenta forms a ridge along the ventral suture and the ovules form two rows on it"],
           "IV III II I", ["IV II III I", "I III II IV", "III IV I II"], "D",
           "Placentation",
           "Marginal: the placenta forms a ridge along the ventral suture of the ovary and the ovules are borne on "
           "it in two rows (pea). Parietal: ovules develop on the inner wall of the ovary or on its "
           "peripheral part (mustard, Argemone). Free central: ovules on a central axis, septa "
           "absent (Dianthus, Primrose). Basal: placenta at the base of the ovary with a single ovule (sunflower, "
           "marigold).",
           ["Marginal → IV", "Parietal → III", "Free central → II", "Basal → I"],
           why="The wrong codes swap parietal with free central (ovules on the ovary wall versus on a central axis) "
               "or marginal with basal.",
           ncert=ref("MOR", "Parts of a Flower (Gynoecium: placentation)"), secs=50)

direct(T_MOR, "Fruit and seed", "Intermediate",
       "Mango and coconut fruits are drupes. Drupes develop from:",
       "monocarpellary superior ovaries and are one-seeded",
       ["bicarpellary superior ovaries and are many-seeded", "monocarpellary inferior ovaries and are one-seeded",
        "multicarpellary superior ovaries and are one-seeded"], "B",
       "Drupe",
       "In mango and coconut, the fruit is known as a drupe. Drupes develop from monocarpellary superior ovaries "
       "and are one-seeded.",
       ["Drupe: monocarpellary + superior ovary + one seed"],
       why="Each wrong option changes one of the three features NCERT gives: the number of carpels, the position "
           "of the ovary or the number of seeds.",
       ncert=ref("MOR", "The Fruit"), secs=30)

direct(T_MOR, "Plant families", "Intermediate",
       "Gram, arhar, sem and moong are members of the family Fabaceae that are important as sources of:",
       "pulses", ["edible oil", "fibre", "fodder"], "B",
       "Economic importance of Fabaceae",
       "Many plants of Fabaceae are sources of pulses (gram, arhar, sem, moong, soyabean); edible oil (soyabean, "
       "groundnut); dye (Indigofera); fibres (sunhemp); fodder (Sesbania, Trifolium); ornamentals (lupin, sweet "
       "pea); and medicine (muliathi).",
       ["Gram, arhar, sem, moong → pulses"],
       why="Edible oil comes from soyabean and groundnut, fibre from sunhemp, and fodder from Sesbania and "
           "Trifolium.",
       ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=25)

direct(T_MOR, "Fruit and seed", "Intermediate",
       "In a maize grain, the embryo is small and is situated:",
       "in a groove at one end of the endosperm",
       ["at the centre of the endosperm, surrounded by it on all sides", "outside the fruit wall",
        "between two large, fleshy cotyledons"], "D",
       "Structure of a monocotyledonous seed",
       "In cereals such as maize, the endosperm is bulky and stores food. The embryo is small and situated in a "
       "groove at one end of the endosperm. It has one large, shield-shaped cotyledon (scutellum) and a short "
       "axis with a plumule and a radicle.",
       ["Maize embryo: small, in a groove at one end of the endosperm"],
       why="The embryo is not embedded at the centre, and it lies inside the grain, not outside the fruit wall. "
           "Two fleshy cotyledons are found in dicotyledonous seeds; maize has a single cotyledon.",
       ncert=ref("MOR", "The Seed (Structure of a Monocotyledonous Seed)"), secs=30)

statement_pair(T_MOR, "Root, stem and leaf", "Intermediate",
               "Underground stems of some plants, such as grass and strawberry, spread to new niches, and when the "
               "older parts die new plants are formed.",
               "In Eichhornia, a lateral branch with short internodes bears at each node a rosette of leaves and a "
               "tuft of roots.",
               True, True, "A",
               "Stem modifications",
               "Underground stems of grass and strawberry spread to new niches, and new plants form when older parts "
               "die. A lateral branch with short internodes, each node bearing a rosette of leaves and a tuft of "
               "roots, is found in aquatic plants like Pistia and Eichhornia.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Stem (Modifications of Stem)"), secs=40)

statement_pair(T_MOR, "Flower", "Intermediate",
               "The corolla may be tubular, bell-shaped, funnel-shaped or wheel-shaped.",
               "The stigma is usually at the base of the style and is the receptive surface for pollen grains.",
               True, False, "C",
               "Corolla and gynoecium",
               "The shape and colour of the corolla vary greatly; it may be tubular, bell-shaped, funnel-shaped or "
               "wheel-shaped. Each carpel has a stigma, style and ovary; the stigma is usually at the tip of the "
               "style and is the receptive surface for pollen grains. The ovary is the enlarged basal part.",
               ["Statement I: true", "Statement II: false, the stigma is at the tip of the style"],
               ncert=ref("MOR", "Parts of a Flower (Corolla; Gynoecium)"), secs=35)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements about the family Liliaceae are correct?",
                [("The inflorescence is solitary or cymose, often in umbellate clusters.", True),
                 ("The perianth has six tepals (3 + 3), often united into a tube, with valvate aestivation.", True),
                 ("The androecium has six stamens, arranged as 3 + 3.", True),
                 ("The ovary is trilocular, with many ovules on axile placentation.", True),
                 ("The fruit is a legume.", False)],
                [("a", "b", "c", "e"), ("b", "c", "d"), ("a", "c", "d", "e")], "C",
                "Liliaceae",
                "Liliaceae ('lily family') is a characteristic monocot family. Inflorescence solitary/cymose, often "
                "umbellate clusters. Perianth: tepals six (3+3), often united into a tube, valvate aestivation. "
                "Androecium: stamens six, 3+3. Gynoecium: tricarpellary, syncarpous, superior ovary, trilocular with "
                "many ovules, axile placentation. Fruit: capsule, rarely berry. A legume is the fruit of Fabaceae.",
                ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: capsule, rarely berry"],
                why="Options with (e) contain the false statement. (b), (c) and (d) only leaves out the true "
                    "statement (a).",
                ncert=ref("MOR", "Description of Some Important Families (Liliaceae)"), secs=60)

direct(T_MOR, "Flower", "Advanced",
       "A flower has its stamens united into a single bundle and a multilocular ovary in which the ovules are "
       "attached to an axial placenta. Among the following, this description fits the flower of:",
       "china rose", ["pea", "mustard", "Dianthus"], "A",
       "Linking androecium and placentation",
       "China rose has monoadelphous stamens (united into one bundle) and axile placentation (placenta axial, "
       "ovules attached to it in a multilocular ovary).",
       ["One bundle of stamens → monoadelphous → china rose",
        "Axial placenta in a multilocular ovary → axile → china rose, tomato, lemon"],
       why="Pea has diadelphous stamens and marginal placentation. Mustard has parietal placentation. Dianthus has "
           "free central placentation in an ovary without septa.",
       ncert=ref("MOR", "Parts of a Flower (Androecium; Gynoecium)"), secs=50)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements about the families Fabaceae and Solanaceae are correct?",
                [("In Fabaceae, the calyx has five sepals and is gamosepalous.", True),
                 ("In Fabaceae, the androecium has ten stamens, which are diadelphous, and the anthers are "
                  "dithecous.", True),
                 ("Solanaceae is widely distributed in the tropics, the subtropics and even the temperate zones.",
                  True),
                 ("In Fabaceae, the ovary is inferior.", False),
                 ("In Solanaceae, the inflorescence is solitary, axillary or cymose, as in Solanum.", True)],
                [("a", "b", "c"), ("a", "b", "d", "e"), ("b", "c", "d", "e")], "B",
                "Fabaceae and Solanaceae",
                "Fabaceae: sepals five, gamosepalous; stamens ten, diadelphous, anthers dithecous; ovary superior, "
                "monocarpellary, unilocular. Solanaceae ('potato family') is widely distributed in tropics, "
                "subtropics and even temperate zones; its inflorescence is solitary, axillary or cymose as in "
                "Solanum.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the ovary of Fabaceae is superior", "(e) true"],
                why="Options with (d) contain the false statement. (a), (b) and (c) only leaves out the true "
                    "statement (e).",
                ncert=ref("MOR", "Description of Some Important Families (Fabaceae; Solanaceae)"), secs=60)

assertion_reason(T_MOR, "Plant families", "Advanced",
                 "In the family Solanaceae, the leaves are always pinnately compound.",
                 "In the family Solanaceae, the flowers are bisexual and actinomorphic.",
                 False, True, False, "D",
                 "Solanaceae",
                 "In Solanaceae the leaves are alternate, simple, rarely pinnately compound, exstipulate, with "
                 "reticulate venation; so 'always pinnately compound' is false. The flowers are bisexual and "
                 "actinomorphic, so R is true.",
                 ["A: false (leaves simple, rarely pinnately compound)", "R: true"],
                 ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=40)

match_list(T_MOR, "Fruit and seed", "Advanced", "family, plant or condition", "type of fruit",
           ["Fabaceae", "Solanaceae", "Mango", "A fruit formed without fertilisation of the ovary"],
           ["Parthenocarpic fruit", "Drupe", "Berry or capsule", "Legume"],
           "IV III II I", ["IV II III I", "I III II IV", "III IV II I"], "B",
           "Types of fruit",
           "NCERT's family descriptions give the fruit of Fabaceae as a legume and of Solanaceae as a berry or "
           "capsule. Mango is a drupe, developing from a monocarpellary superior ovary. A fruit formed without "
           "fertilisation of the ovary is called a parthenocarpic fruit.",
           ["Fabaceae → legume", "Solanaceae → berry or capsule", "Mango → drupe",
            "No fertilisation → parthenocarpic fruit"],
           why="The wrong codes give Solanaceae a drupe, treat the legume as a parthenocarpic fruit, or give "
               "Fabaceae the berry or capsule of Solanaceae.",
           ncert=ref("MOR", "The Fruit; Description of Some Important Families"), secs=45)

# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
direct(T_ANA, "Plant tissues", "Basic",
       "Besides the pulp of fruits such as guava, pear and sapota, sclereids are commonly found in:",
       "the fruit walls of nuts, the seed coats of legumes and the leaves of tea",
       ["the root hairs of grasses", "the guard cells of stomata", "the companion cells of the phloem"], "D",
       "Sclereids",
       "Sclereids are spherical, oval or cylindrical, highly thickened dead cells with very narrow cavities. They "
       "are commonly found in the fruit walls of nuts; the pulp of fruits like guava, pear and sapota; the seed "
       "coats of legumes; and the leaves of tea.",
       ["Sclereids: fruit walls of nuts, pulp of guava/pear/sapota, seed coats of legumes, tea leaves"],
       why="Root hairs, guard cells and companion cells are living cells; sclereids are dead, highly thickened "
           "cells.",
       ncert=ref("ANA", "The Tissues (Sclerenchyma)"), secs=25)

direct(T_ANA, "Tissue systems", "Basic",
       "The stomatal aperture, the guard cells and the surrounding subsidiary cells are together called the:",
       "stomatal apparatus", ["epidermal appendage", "stele", "bulliform cells"], "D",
       "Stomatal apparatus",
       "Stomata are structures in the epidermis of leaves. Each stoma has two guard cells enclosing the stomatal "
       "pore; a few specialised epidermal cells near the guard cells are subsidiary cells. The stomatal aperture, "
       "guard cells and surrounding subsidiary cells together are called the stomatal apparatus.",
       ["Aperture + guard cells + subsidiary cells = stomatal apparatus"],
       why="Epidermal appendages are trichomes and hairs. The stele is all the tissue inside the endodermis. "
           "Bulliform cells are large empty cells in the adaxial epidermis of grass leaves.",
       ncert=ref("ANA", "The Tissue System (Epidermal Tissue System)"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "Cells formed by the divisions of primary and secondary meristems become structurally and functionally "
       "specialised and lose the ability to divide. Such cells constitute the:",
       "permanent tissues", ["intercalary meristems", "lateral meristems", "apical meristems"], "B",
       "Permanent tissues",
       "Following divisions of cells in both primary and secondary meristems, the newly formed cells become "
       "structurally and functionally specialised and lose the ability to divide. Such cells are termed permanent "
       "or mature cells and constitute the permanent tissues.",
       ["Specialised cells that no longer divide → permanent tissues"],
       why="Intercalary, lateral and apical meristems are all meristematic tissues, whose cells keep the ability "
           "to divide.",
       ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=20)

statement_pair(T_ANA, "Plant tissues", "Basic",
               "Permanent tissues having all cells similar in structure and function are called simple tissues.",
               "In flowering plants, xylem fibres are the main water-transporting elements.",
               True, False, "C",
               "Simple tissues; xylem",
               "Permanent tissues having all cells similar in structure and function are called simple tissues; "
               "those with many different types of cells are complex tissues. In flowering plants, tracheids and "
               "vessels are the main water-transporting elements. Xylem fibres have highly thickened walls and "
               "obliterated central lumens.",
               ["Statement I: true", "Statement II: false, tracheids and vessels are the main water-transporting "
                                     "elements"],
               ncert=ref("ANA", "The Tissues (Permanent Tissues; Xylem)"), secs=35)

statement_pair(T_ANA, "Plant tissues", "Intermediate",
               "The sieve tube elements and companion cells are connected by pit fields present between their "
               "common longitudinal walls.",
               "Phloem parenchyma is made up of elongated, tapering, cylindrical cells that have dense cytoplasm and "
               "a nucleus.",
               True, True, "A",
               "Phloem",
               "Companion cells are specialised parenchymatous cells closely associated with sieve tube elements; "
               "the two are connected by pit fields present between their common longitudinal walls. Phloem "
               "parenchyma is made up of elongated, tapering cylindrical cells which have dense cytoplasm and a "
               "nucleus.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (Phloem)"), secs=40)

multi_statement(T_ANA, "Tissue systems", "Intermediate",
                "Which of the following belong to the ground tissue system of primary stems and roots?",
                [("Cortex", True), ("Pericycle", True), ("Pith", True), ("Phloem", False), ("Epidermis", False)],
                [("a", "c", "e"), ("b", "c", "d"), ("a", "b", "c", "d")], "B",
                "Ground tissue system",
                "All tissues except the epidermis and the vascular bundles constitute the ground tissue. "
                "Parenchymatous cells of the ground tissue are usually present in the cortex, pericycle, pith and "
                "medullary rays in primary stems and roots. Phloem belongs to the vascular tissue system and the "
                "epidermis to the epidermal tissue system.",
                ["(a) cortex: ground", "(b) pericycle: ground", "(c) pith: ground", "(d) phloem: vascular",
                 "(e) epidermis: epidermal"],
                why="Options with (d) or (e) include a tissue of another tissue system.",
                ncert=ref("ANA", "The Tissue System (The Ground Tissue System)"), secs=40)

match_list(T_ANA, "Plant tissues", "Intermediate", "meristem", "position",
           ["Root apical meristem", "Shoot apical meristem", "Intercalary meristem", "Lateral meristem"],
           ["Cylindrical meristem in the mature regions of roots and shoots, lateral in position",
            "Between mature tissues, as in grasses", "Distant-most region of the stem axis", "Tip of the root"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "C",
           "Meristems",
           "The root apical meristem occupies the tip of a root, while the shoot apical meristem occupies the "
           "distant-most region of the stem axis. Intercalary meristems occur between mature tissues, as in "
           "grasses. Lateral meristems appear later, in the mature regions of roots and shoots of many plants, "
           "particularly those that produce woody axes, and are lateral and cylindrical.",
           ["Root apical → IV", "Shoot apical → III", "Intercalary → II", "Lateral → I"],
           why="The wrong codes interchange the two apical meristems, or the intercalary and lateral meristems.",
           ncert=ref("ANA", "The Tissues (Meristematic Tissues)"), secs=45)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Xylem and phloem are described as complex tissues.",
                 "Each is made up of more than one type of cell, and these cells work together as a unit.",
                 True, True, True, "A",
                 "Complex tissues",
                 "Complex tissues are made of more than one type of cells that work together as a unit. Xylem "
                 "(tracheids, vessels, xylem fibres, xylem parenchyma) and phloem (sieve tube elements, companion "
                 "cells, phloem parenchyma, phloem fibres) are the complex tissues in plants. R is the defining "
                 "reason.",
                 ["A: true", "R: true", "More than one cell type working as a unit → complex tissue → R explains "
                                       "A"],
                 ncert=ref("ANA", "The Tissues (Complex Tissues)"), secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "The cortex of a dicot stem consists of three sub-zones. Which of the following gives them in the correct "
       "order from outside inwards?",
       "Hypodermis, cortical layers, endodermis",
       ["Endodermis, cortical layers, hypodermis", "Hypodermis, endodermis, cortical layers",
        "Cortical layers, hypodermis, pericycle"], "D",
       "Cortex of a dicot stem",
       "The outer hypodermis has a few layers of collenchymatous cells just below the epidermis. Below it are the "
       "cortical layers of rounded, thin-walled parenchyma with conspicuous intercellular spaces. The innermost "
       "layer of the cortex is the endodermis (starch sheath). The pericycle lies inside the endodermis and is "
       "not part of the cortex.",
       ["Outer: hypodermis", "Middle: cortical layers", "Innermost: endodermis"],
       why="The first option is the reverse order. The second places the endodermis in the middle, but it is the "
           "innermost layer. The third includes the pericycle, which lies inside the endodermis.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous Stem)"), secs=35)

multi_statement(T_ANA, "Plant tissues", "Advanced",
                "Which of the following statements about xylem are correct?",
                [("Tracheids are dead and without protoplasm; the inner layers of their walls have thickenings that "
                  "vary in form.", True),
                 ("Vessel members are devoid of protoplasm.", True),
                 ("Xylem conducts water and minerals from the leaves to the stem and roots.", False),
                 ("Besides conduction, xylem provides mechanical strength to plant parts.", True),
                 ("A vessel member has lignified walls and a large central cavity.", True)],
                [("a", "b", "c", "e"), ("b", "c", "d"), ("a", "c", "d", "e")], "B",
                "Xylem",
                "Xylem functions as a conducting tissue for water and minerals from the roots to the stem and "
                "leaves, and also provides mechanical strength. Tracheids are elongated, dead cells without "
                "protoplasm, with thick lignified walls whose inner layers bear thickenings of various forms. A "
                "vessel is a long cylindrical tube of many vessel members, each with lignified walls and a large "
                "central cavity; vessel members are devoid of protoplasm.",
                ["(a) true", "(b) true", "(c) false: from roots to stem and leaves", "(d) true", "(e) true"],
                why="Every wrong option includes (c), which reverses the direction of conduction.",
                ncert=ref("ANA", "The Tissues (Xylem)"), secs=55)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Advanced",
               "In a dicot root, both the tangential and the radial walls of the endodermal cells have a deposition "
               "of a water-impermeable, waxy material in the form of Casparian strips.",
               "In a dicot stem, the cortical layers below the hypodermis consist of rounded, thin-walled "
               "parenchymatous cells with conspicuous intercellular spaces.",
               True, True, "A",
               "Dicot root and stem",
               "In the dicot root, the tangential as well as radial walls of the endodermal cells have a deposition "
               "of water-impermeable, waxy suberin as Casparian strips. In the dicot stem, the cortical layers "
               "below the hypodermis are rounded, thin-walled parenchymatous cells with conspicuous intercellular "
               "spaces.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous Root; "
                                "Dicotyledonous Stem)"), secs=45)

assertion_reason(T_ANA, "Dicot and monocot anatomy", "Advanced",
                 "In a dorsiventral (dicot) leaf, the vascular bundles are all of nearly similar size.",
                 "The size of a vascular bundle depends on the size of the vein, and the veins vary in thickness in "
                 "the reticulate venation of dicot leaves.",
                 False, True, False, "D",
                 "Vascular bundles in leaves",
                 "In a dorsiventral leaf, the size of the vascular bundles depends on the size of the veins, and "
                 "the veins vary in thickness in the reticulate venation of dicot leaves; so the bundles vary in "
                 "size and A is false. Vascular bundles of nearly similar size (except the main veins) are a "
                 "feature of the isobilateral (monocot) leaf with parallel venation.",
                 ["A: false (bundles vary in size)", "R: true"],
                 ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dorsiventral (Dicot) "
                                  "Leaf)"), secs=45)

direct(T_ANA, "Dicot and monocot anatomy", "Advanced",
       "Which statement correctly describes collenchyma in relation to the dicot stem?",
       "It occurs in layers below the epidermis, as a homogeneous layer or in patches, and the collenchymatous "
       "hypodermis gives mechanical strength to the young stem",
       ["It forms semi-lunar patches above the phloem as part of the pericycle",
        "It forms the sclerenchymatous hypodermis found in monocot stems",
        "It consists of dead cells with lignified walls that lack intercellular spaces"], "C",
       "Collenchyma in the dicot stem",
       "Collenchyma occurs in layers below the epidermis in dicotyledonous plants, either as a homogeneous layer "
       "or in patches. In the dicot stem, the hypodermis consists of a few layers of collenchymatous cells just "
       "below the epidermis, which provide mechanical strength to the young stem.",
       ["Collenchyma: below epidermis in dicots, homogeneous layer or patches",
        "Dicot stem hypodermis = collenchyma → strength to young stem"],
       why="The semi-lunar patches of the pericycle are sclerenchyma. The hypodermis of the monocot stem is "
           "sclerenchymatous, not collenchymatous. Collenchyma cells are living, with walls thickened at the "
           "corners by cellulose, hemicellulose and pectin, not lignin.",
       ncert=ref("ANA", "The Tissues (Collenchyma); Dicotyledonous Stem"), secs=50)

# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Prokaryotic cell", "Basic",
       "According to NCERT, prokaryotic cells are represented by bacteria, blue-green algae and:",
       "mycoplasma and PPLO (pleuro pneumonia like organisms)",
       ["yeast and Amoeba", "Euglena and Chlamydomonas", "diatoms and desmids"], "C",
       "Prokaryotic cells",
       "The prokaryotic cells are represented by bacteria, blue-green algae, mycoplasma and PPLO (Pleuro "
       "Pneumonia Like Organisms).",
       ["Prokaryotes: bacteria, blue-green algae, mycoplasma, PPLO"],
       why="Yeast (a fungus), Amoeba, Euglena, Chlamydomonas, diatoms and desmids are all eukaryotes.",
       ncert=ref("CELL", "Prokaryotic Cells"), secs=20)

direct(T_CELL, "Cell theory", "Basic",
       "In both plant and animal cells, the main arena of cellular activities, where various chemical reactions "
       "keep the cell in the 'living state', is the:",
       "cytoplasm", ["nucleus", "cell wall", "vacuole"], "A",
       "Cytoplasm",
       "The cytoplasm is the main arena of cellular activities in both plant and animal cells. Various chemical "
       "reactions occur in it to keep the cell in the 'living state'.",
       ["Main arena of cellular activities → cytoplasm"],
       why="The nucleus holds the genetic material, the cell wall gives shape and protection, and the vacuole "
           "stores water, sap and materials not useful for the cell.",
       ncert=ref("CELL", "An Overview of Cell"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "Ribosomes are:",
       "composed of RNA and proteins, and not surrounded by any membrane",
       ["composed of DNA and proteins, and surrounded by a single membrane",
        "composed of lipids and proteins, and surrounded by a double membrane",
        "composed of RNA and lipids, and surrounded by a single membrane"], "B",
       "Ribosomes",
       "Ribosomes are granular structures first observed under the electron microscope by George Palade (1953). "
       "They are composed of ribonucleic acid (RNA) and proteins and are not surrounded by any membrane.",
       ["Ribosome: RNA + protein, no membrane"],
       why="Ribosomes contain RNA, not DNA, and are not membrane-bound; every wrong option adds a membrane or a "
           "wrong component.",
       ncert=ref("CELL", "Eukaryotic Cells (Ribosomes)"), secs=20)

direct(T_CELL, "Cytoskeleton, cilia and centrioles", "Basic",
       "The elaborate network of filamentous proteinaceous structures in the cytoplasm, collectively called the "
       "cytoskeleton, consists of:",
       "microtubules, microfilaments and intermediate filaments",
       ["cisternae, tubules and vesicles", "cristae, matrix and the outer membrane",
        "grana, stroma lamellae and stroma"], "D",
       "Cytoskeleton",
       "An elaborate network of filamentous proteinaceous structures consisting of microtubules, microfilaments "
       "and intermediate filaments present in the cytoplasm is collectively referred to as the cytoskeleton. It "
       "is involved in mechanical support, motility and maintenance of cell shape.",
       ["Cytoskeleton = microtubules + microfilaments + intermediate filaments"],
       why="Cisternae and vesicles describe the Golgi apparatus and ER, cristae and matrix the mitochondrion, and "
           "grana and stroma the chloroplast.",
       ncert=ref("CELL", "Eukaryotic Cells (Cytoskeleton)"), secs=20)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Basic",
               "Animal cells have centrioles, which are absent in almost all plant cells.",
               "Plant cells possess cell walls, plastids and a large central vacuole, which are absent in animal "
               "cells.",
               True, True, "A",
               "Plant and animal cells",
               "NCERT's comparison of plant and animal cells: plant cells possess cell walls, plastids and a large "
               "central vacuole, which are absent in animal cells; animal cells have centrioles, which are absent "
               "in almost all plant cells.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells"), secs=30)

direct(T_CELL, "Nucleus", "Intermediate",
       "Normally there is one nucleus per cell. Which of the following are cited by NCERT as mature cells that "
       "lack a nucleus?",
       "Erythrocytes of many mammals and sieve tube cells of vascular plants",
       ["Companion cells and guard cells", "Nerve cells and white blood cells",
        "Mesophyll cells and root hair cells"], "C",
       "Cells without a nucleus",
       "Normally there is only one nucleus per cell, though variations in the number of nuclei are frequently "
       "observed. Some mature cells even lack a nucleus, e.g., erythrocytes of many mammals and sieve tube cells "
       "of vascular plants.",
       ["Mature cells without nucleus: mammalian erythrocytes, sieve tube cells"],
       why="Companion cells, guard cells, nerve cells, white blood cells, mesophyll cells and root hair cells all "
           "have a nucleus. (The functions of sieve tubes are controlled by the nucleus of the companion cell.)",
       ncert=ref("CELL", "Eukaryotic Cells (Nucleus)"), secs=30)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "Plasmodesmata are pores in the nuclear envelope through which RNA moves into the cytoplasm.",
               "The cell wall helps in cell-to-cell interaction and provides a barrier to undesirable "
               "macromolecules.",
               False, True, "D",
               "Cell wall",
               "The cell wall and middle lamellae may be traversed by plasmodesmata, which connect the cytoplasm of "
               "neighbouring cells; the passages for RNA in the nuclear envelope are nuclear pores. Besides giving "
               "shape and protecting the cell from mechanical damage and infection, the cell wall helps in "
               "cell-to-cell interaction and provides a barrier to undesirable macromolecules.",
               ["Statement I: false, plasmodesmata connect the cytoplasm of neighbouring cells",
                "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (Cell Wall)"), secs=40)

match_list(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate", "part of the cell", "what it contains",
           ["Mitochondrial matrix", "Thylakoids", "Chloroplast stroma", "Vacuole"],
           ["Water, sap, excretory products and other materials not useful for the cell",
            "Single circular DNA molecule, a few RNA molecules and 70S ribosomes",
            "Enzymes required for the synthesis of carbohydrates and proteins",
            "Chlorophyll pigments"],
           "II IV III I", ["III IV II I", "II III IV I", "II IV I III"], "B",
           "Contents of organelles",
           "The mitochondrial matrix possesses a single circular DNA molecule, a few RNA molecules, ribosomes (70S) "
           "and components for protein synthesis. The chlorophyll pigments are present in the thylakoids. The "
           "stroma of the chloroplast contains enzymes required for the synthesis of carbohydrates and proteins. "
           "The vacuole contains water, sap, excretory products and other materials not useful for the cell.",
           ["Matrix → II", "Thylakoids → IV", "Stroma → III", "Vacuole → I"],
           why="The wrong codes swap the matrix with the stroma, the thylakoids with the stroma, or the stroma with "
               "the vacuole.",
           ncert=ref("CELL", "Eukaryotic Cells (Mitochondria; Plastids; Vacuoles)"), secs=45)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                 "The number of mitochondria per cell is variable.",
                 "The number of mitochondria in a cell depends on the physiological activity of the cell.",
                 True, True, True, "A",
                 "Mitochondria",
                 "NCERT states that the number of mitochondria per cell is variable depending on the "
                 "physiological activity of the cells. R states the cause of the variation in A.",
                 ["A: true", "R: true", "Number depends on activity → R explains A"],
                 ncert=ref("CELL", "Eukaryotic Cells (Mitochondria)"), secs=30)

multi_statement(T_CELL, "Cell envelope and membrane", "Intermediate",
                "Which of the following statements about the cell membrane are correct?",
                [("The lipid component of the membrane mainly consists of phosphoglycerides.", True),
                 ("Neutral solutes may move across the membrane by simple diffusion along the concentration "
                  "gradient.", True),
                 ("Chemical studies on human red blood cells enabled scientists to deduce the possible structure "
                  "of the plasma membrane.", True),
                 ("The detailed structure of the membrane was worked out with the light microscope, long before "
                  "the electron microscope came into use.", False)],
                [("a", "b", "d"), ("b", "c", "d"), ("a", "c", "d")], "D",
                "Cell membrane",
                "The detailed structure of the membrane was studied only after the advent of the electron "
                "microscope in the 1950s. Chemical studies on the cell membrane, especially in human RBCs, enabled "
                "scientists to deduce its possible structure. The lipid component mainly consists of "
                "phosphoglycerides. Neutral solutes may move across the membrane by simple diffusion along the "
                "concentration gradient.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the electron microscope was needed"],
                why="Every wrong option includes the false statement (d).",
                ncert=ref("CELL", "Eukaryotic Cells (Cell Membrane)"), secs=50)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
       "Compared with the ribosomes in the cytoplasm of a plant cell, the ribosomes of its chloroplasts are:",
       "smaller, of the 70S type, while the cytoplasmic ones are 80S",
       ["larger, of the 80S type, while the cytoplasmic ones are 70S", "of the same 80S type",
        "absent, since chloroplasts import all their proteins"], "B",
       "Ribosomes of chloroplasts",
       "The stroma of the chloroplast contains small, double-stranded circular DNA molecules and ribosomes. The "
       "ribosomes of the chloroplasts are smaller (70S) than the cytoplasmic ribosomes (80S).",
       ["Chloroplast: 70S", "Cytoplasm of eukaryotic cell: 80S"],
       why="The second option reverses the two types. Chloroplast ribosomes are not 80S, and they are not absent: "
           "the stroma contains ribosomes.",
       ncert=ref("CELL", "Eukaryotic Cells (Plastids)"), secs=30)

statement_pair(T_CELL, "Cell theory", "Intermediate",
               "From his studies on plant tissues, Schwann concluded that the presence of a cell wall is a unique "
               "character of plant cells.",
               "The cell theory as formulated by Schleiden and Schwann explained how new cells are formed.",
               True, False, "C",
               "Cell theory",
               "Schwann concluded, based on his studies on plant tissues, that the presence of a cell wall is a "
               "unique character of plant cells. Schleiden and Schwann together formulated the cell theory, but it "
               "did not explain how new cells were formed. Rudolf Virchow later explained that new cells arise from "
               "pre-existing cells.",
               ["Statement I: true", "Statement II: false, the theory did not explain how new cells are formed"],
               ncert=ref("CELL", "Cell Theory"), secs=40)

multi_statement(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
                "Which of the following statements about centrioles, cilia and flagella are correct?",
                [("Centrioles form the basal bodies of cilia and flagella.", True),
                 ("In animal cells, centrioles give rise to the spindle fibres that form the spindle apparatus "
                  "during cell division.", True),
                 ("The peripheral fibrils of a centriole are made of the protein tubulin.", True),
                 ("The adjacent peripheral triplets of a centriole are not linked to one another.", False),
                 ("Cilia and flagella are covered with plasma membrane.", True)],
                [("a", "b", "c"), ("a", "b", "d", "e"), ("b", "c", "d", "e")], "A",
                "Centrioles, cilia and flagella",
                "A centriole has an organisation like a cartwheel: nine evenly spaced peripheral fibrils of tubulin "
                "protein, each a triplet, and the adjacent triplets are also linked. Centrioles form the basal body "
                "of cilia or flagella, and the spindle fibres that give rise to the spindle apparatus during cell "
                "division in animal cells. Cilia and flagella are covered with plasma membrane.",
                ["(a) true", "(b) true", "(c) true", "(d) false: adjacent triplets are linked", "(e) true"],
                why="Options with (d) contain the false statement. (a), (b) and (c) only leaves out the true "
                    "statement (e).",
                ncert=ref("CELL", "Eukaryotic Cells (Cilia and Flagella; Centrosome and Centrioles)"), secs=60)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "The lumen of a mitochondrion is divided into two aqueous compartments, the outer compartment and "
                 "the matrix.",
                 "The outer membrane of a mitochondrion forms a number of infoldings called cristae.",
                 True, False, False, "C",
                 "Structure of mitochondria",
                 "Each mitochondrion is bound by two membranes, which divide its lumen into two aqueous "
                 "compartments: the outer compartment and the inner compartment, the matrix. The outer membrane "
                 "forms the continuous limiting boundary; it is the inner membrane that forms the infoldings "
                 "called cristae towards the matrix.",
                 ["A: true", "R: false (cristae are infoldings of the inner membrane)"],
                 ncert=ref("CELL", "Eukaryotic Cells (Mitochondria)"), secs=40)

assertion_reason(T_CELL, "Endomembrane system", "Advanced",
                 "Mitochondria and chloroplasts are parts of the endomembrane system, because their functions are "
                 "coordinated with those of the ER and the Golgi complex.",
                 "The functions of the endoplasmic reticulum, Golgi complex, lysosomes and vacuoles are coordinated, "
                 "so these are considered together as the endomembrane system.",
                 False, True, False, "D",
                 "Endomembrane system",
                 "The ER, Golgi complex, lysosomes and vacuoles are considered together as the endomembrane system "
                 "because their functions are coordinated. The functions of mitochondria, chloroplasts and "
                 "peroxisomes are not coordinated with these components, so they are not considered part of the "
                 "endomembrane system.",
                 ["A: false", "R: true"],
                 ncert=ref("CELL", "Eukaryotic Cells (Endomembrane System)"), secs=40)

direct(T_CELL, "Cell theory", "Advanced",
       "Which observation best supports the view that the cell is the fundamental structural and functional unit "
       "of all living organisms?",
       "Unicellular organisms can exist independently and perform the essential functions of life, while "
       "anything less than a complete cell does not ensure independent living",
       ["Every cell has a cell wall, a nucleus and chloroplasts",
        "All cells are of the same size and shape, whatever their function",
        "Cells can be seen only with the electron microscope"], "B",
       "Cell as the unit of life",
       "Unicellular organisms are capable of (i) independent existence and (ii) performing the essential "
       "functions of life. Anything less than a complete structure of a cell does not ensure independent living. "
       "Hence the cell is the fundamental structural and functional unit of all living organisms.",
       ["Independent existence of unicellular organisms", "Nothing less than a cell lives independently",
        "→ cell = fundamental unit of life"],
       why="Animal cells lack a cell wall and chloroplasts, and some mature cells lack a nucleus. Cells vary "
           "greatly in size and shape with function. Anton Von Leeuwenhoek first saw and described a live cell, "
           "long before the electron microscope existed.",
       ncert=ref("CELL", "What is a Cell?"), secs=45)

match_list(T_CELL, "Endomembrane system", "Advanced", "structure", "membrane covering",
           ["Ribosome", "Vacuole", "Mitochondrion", "Nucleus"],
           ["Double-membrane envelope with pores", "Not surrounded by any membrane",
            "Two membranes, the inner one folded into cristae", "A single membrane, the tonoplast"],
           "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "D",
           "Membranes of cell structures",
           "Ribosomes are not surrounded by any membrane. The vacuole is bound by a single membrane, the "
           "tonoplast. A mitochondrion has two membranes, the inner one forming infoldings called cristae. The "
           "nucleus has a nuclear envelope of two parallel membranes, interrupted by nuclear pores.",
           ["Ribosome → II", "Vacuole → IV", "Mitochondrion → III", "Nucleus → I"],
           why="The wrong codes give the ribosome a membrane, or swap the two double-membrane structures, or give "
               "the vacuole two membranes.",
           ncert=ref("CELL", "Eukaryotic Cells"), secs=45)

# =============================================================== 6. Cell Cycle and Cell Division (4/6/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "Cells that do not divide further enter an inactive stage called the quiescent stage (G0). They enter it by "
       "exiting which phase of the cell cycle?",
       "G1 phase", ["S phase", "G2 phase", "M phase"], "B",
       "Quiescent stage",
       "Cells that do not divide further exit the G1 phase to enter an inactive stage called the quiescent stage "
       "(G0) of the cell cycle.",
       ["Non-dividing cells: G1 → G0"],
       why="A cell that has passed into S or G2 has begun preparing for division; NCERT describes the exit to G0 "
           "from G1. M phase is the division itself.",
       ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=20)

direct(T_CC, "Meiosis", "Basic",
       "During zygotene of meiotic prophase I, the complex formed by a pair of synapsed homologous chromosomes is "
       "called a:",
       "bivalent or tetrad", ["chiasma", "kinetochore", "dyad of cells"], "A",
       "Bivalent",
       "During zygotene, homologous chromosomes start pairing (synapsis). The complex formed by a pair of "
       "synapsed homologous chromosomes is called a bivalent or a tetrad; these are more clearly visible at the "
       "next stage, pachytene.",
       ["Pair of synapsed homologues = bivalent (tetrad)"],
       why="A chiasma is the X-shaped site of crossing over seen in diplotene. A kinetochore is the disc-shaped "
           "structure on the centromere. A dyad of cells is formed after telophase I.",
       ncert=ref("CC", "Meiosis (Meiosis I: Prophase I)"), secs=20)

direct(T_CC, "Cell cycle phases", "Basic",
       "The sequence of events by which a cell duplicates its genome, synthesises the other constituents of the "
       "cell and eventually divides into two daughter cells is called the:",
       "cell cycle", ["cytokinesis", "karyokinesis", "interkinesis"], "C",
       "Cell cycle",
       "The sequence of events by which a cell duplicates its genome, synthesises the other constituents of the "
       "cell and eventually divides into two daughter cells is termed the cell cycle.",
       ["Genome duplication + synthesis of constituents + division = cell cycle"],
       why="Cytokinesis is division of the cytoplasm and karyokinesis division of the nucleus; both are only parts "
           "of M phase. Interkinesis is the short stage between meiosis I and meiosis II.",
       ncert=ref("CC", "Cell Cycle"), secs=20)

# each meiocyte gives 4 haploid cells
_cc_meiocytes = 400 // 4
numerical(T_CC, "Meiosis", "Basic",
          "Each meiocyte that completes meiosis forms four haploid cells. How many meiocytes must complete meiosis "
          "to produce 400 haploid cells?",
          "100", ["400", "200", "1600"], "C",
          _cc_meiocytes == 100 and _cc_meiocytes * 4 == 400,
          "Products of meiosis",
          "Meiosis involves two sequential nuclear and cell divisions, and four haploid cells are formed at the end "
          "of meiosis II. So the number of meiocytes needed is 400 ÷ 4 = 100.",
          ["Cells per meiocyte = 4", "Meiocytes = 400 ÷ 4 = 100"],
          "400 assumes one cell per meiocyte. 200 stops after meiosis I (two cells per meiocyte). 1600 multiplies "
          "by 4 instead of dividing.",
          ref("CC", "Meiosis"), secs=40)

# n cells from one cell need n - 1 divisions (each division adds exactly one cell)
_cc_cells = 64
_cc_divisions = _cc_cells - 1
_cc_rounds = 6
assert 2 ** _cc_rounds == _cc_cells and sum(2 ** r for r in range(_cc_rounds)) == _cc_divisions
numerical(T_CC, "Mitosis", "Intermediate",
          "A single cell divides repeatedly by mitosis until 64 cells are formed. Each division of a cell produces "
          "two cells. How many individual cell divisions take place in all?",
          "63", ["6", "32", "64"], "D",
          _cc_divisions == 63,
          "Counting mitotic divisions",
          "Each division turns one cell into two, so it adds exactly one cell to the total. Going from 1 cell to 64 "
          "cells therefore needs 64 − 1 = 63 divisions. Check by rounds: 1 + 2 + 4 + 8 + 16 + 32 = 63 divisions "
          "in 6 rounds.",
          ["Each division adds one cell", "Divisions = 64 − 1 = 63",
           "Check: 1 + 2 + 4 + 8 + 16 + 32 = 63"],
          "6 is the number of rounds (generations) of division, not the number of divisions. 32 counts only the "
          "divisions of the last round. 64 is the number of cells formed.",
          ref("CC", "Mitosis (Significance of Mitosis)"), secs=60,
          short="Cells formed − 1 = number of divisions.")

statement_pair(T_CC, "Cell cycle phases", "Intermediate",
               "In the S and G2 phases, the new DNA molecules formed are not distinct but intertwined.",
               "In an animal cell, cytokinesis is achieved by a furrow in the plasma membrane that gradually deepens "
               "and ultimately joins in the centre, dividing the cytoplasm into two.",
               True, True, "A",
               "Interphase and cytokinesis",
               "In the S and G2 phases the new DNA molecules formed are not distinct but intertwined; they condense "
               "into mitotic chromosomes in prophase. In an animal cell, cytokinesis is achieved by the appearance of "
               "a furrow in the plasma membrane, which gradually deepens and ultimately joins in the centre.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "M Phase (Prophase; Cytokinesis)"), secs=40)

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "In plant cells, cytokinesis takes place by the appearance of a furrow in the plasma membrane.",
                 "Plant cells are enclosed by a relatively inextensible cell wall.",
                 False, True, False, "D",
                 "Cytokinesis in plant cells",
                 "Plant cells are enclosed by a relatively inextensible cell wall, so they undergo cytokinesis by a "
                 "different mechanism: wall formation starts in the centre of the cell and grows outward to meet "
                 "the existing lateral walls (cell plate). The furrow is the method of animal cells. A is false, R "
                 "is true.",
                 ["A: false (plant cells form a cell plate)", "R: true"],
                 ncert=ref("CC", "M Phase (Cytokinesis)"), secs=40)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following statements about prophase of mitosis are correct?",
                [("The chromosomal material condenses to form compact mitotic chromosomes.", True),
                 ("Chromosomes are seen to be composed of two chromatids attached together at the centromere.",
                  True),
                 ("Prophase follows the S and G2 phases of interphase.", True),
                 ("The complete disintegration of the nuclear envelope marks the start of prophase.", False)],
                [("a", "b", "d"), ("b", "c", "d"), ("a", "c", "d")], "B",
                "Prophase",
                "Prophase follows the S and G2 phases. It is marked by the initiation of condensation of the "
                "chromosomal material into compact mitotic chromosomes, each composed of two chromatids attached at "
                "the centromere. The complete disintegration of the nuclear envelope marks the start of the second "
                "phase, metaphase.",
                ["(a) true", "(b) true", "(c) true", "(d) false: it marks the start of metaphase"],
                why="Every wrong option includes the false statement (d).",
                ncert=ref("CC", "M Phase (Prophase; Metaphase)"), secs=45)

direct(T_CC, "Meiosis", "Intermediate",
       "In metaphase I of meiosis, the microtubules from the opposite poles of the spindle attach to:",
       "the pair of homologous chromosomes",
       ["the two sister chromatids of each chromosome", "the nuclear envelope", "the nucleolus"], "C",
       "Metaphase I",
       "In metaphase I, the bivalent chromosomes align on the equatorial plate, and the microtubules from the "
       "opposite poles of the spindle attach to the pair of homologous chromosomes. (In mitotic metaphase and "
       "metaphase II they attach to the kinetochores of sister chromatids.)",
       ["Metaphase I: spindle fibres from opposite poles → the two homologues of each bivalent"],
       why="Attachment to sister chromatids from opposite poles happens in mitosis and in metaphase II. The "
           "nuclear envelope and nucleolus have disappeared by the end of diakinesis.",
       ncert=ref("CC", "Meiosis (Metaphase I)"), secs=35)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Meiosis produces the diploid phase in the life cycle of sexually reproducing organisms, while "
               "fertilisation restores the haploid phase.",
               "The first two stages of prophase I are relatively short-lived compared with pachytene.",
               False, True, "D",
               "Meiosis",
               "Meiosis ensures the production of the haploid phase in the life cycle of sexually reproducing "
               "organisms, whereas fertilisation restores the diploid phase; Statement I reverses them. The first "
               "two stages of prophase I (leptotene and zygotene) are relatively short-lived compared with the next "
               "stage, pachytene.",
               ["Statement I: false (meiosis → haploid; fertilisation → diploid)", "Statement II: true"],
               ncert=ref("CC", "Meiosis"), secs=40)

match_list(T_CC, "Meiosis", "Advanced", "stage of meiosis", "event",
           ["Pachytene", "Diplotene", "Diakinesis", "Telophase II"],
           ["Chromosomes are fully condensed and the meiotic spindle is assembled to prepare the homologues for "
            "separation",
            "The two groups of chromosomes are again enclosed by a nuclear envelope, and cytokinesis gives a tetrad "
            "of four haploid cells",
            "Bivalent chromosomes now clearly appear as tetrads",
            "The recombined homologous chromosomes of the bivalents tend to separate from each other, except at the "
            "sites of crossovers"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A",
           "Stages of meiosis",
           "Pachytene: bivalents clearly appear as tetrads, and recombination nodules appear. Diplotene: the "
           "synaptonemal complex dissolves and the recombined homologues tend to separate except at the crossovers "
           "(chiasmata). Diakinesis: chromosomes are fully condensed and the meiotic spindle is assembled. "
           "Telophase II: the two groups of chromosomes are enclosed by nuclear envelopes and cytokinesis gives a "
           "tetrad of cells, i.e., four haploid daughter cells.",
           ["Pachytene → III", "Diplotene → IV", "Diakinesis → I", "Telophase II → II"],
           why="The wrong codes swap pachytene with diplotene, diakinesis with telophase II, or pachytene with "
               "diakinesis.",
           ncert=ref("CC", "Meiosis (Meiosis I; Meiosis II)"), secs=60)

direct(T_CC, "Meiosis", "Advanced",
       "Consider these events of meiotic prophase I: (i) terminalisation of chiasmata; (ii) appearance of "
       "recombination nodules; (iii) dissolution of the synaptonemal complex; (iv) formation of the synaptonemal "
       "complex. Which is the correct order in which they occur?",
       "(iv) → (ii) → (iii) → (i)",
       ["(ii) → (iv) → (iii) → (i)", "(iv) → (iii) → (ii) → (i)", "(i) → (iv) → (ii) → (iii)"], "B",
       "Sequence of prophase I",
       "Zygotene: synapsis with formation of the synaptonemal complex (iv). Pachytene: recombination nodules "
       "appear, marking the sites of crossing over (ii). Diplotene: the synaptonemal complex dissolves and "
       "chiasmata become visible (iii). Diakinesis: terminalisation of chiasmata (i).",
       ["Zygotene (iv)", "Pachytene (ii)", "Diplotene (iii)", "Diakinesis (i)"],
       why="Nodules cannot appear before synapsis; the synaptonemal complex dissolves only after crossing over; "
           "terminalisation of chiasmata is the last event, in diakinesis.",
       ncert=ref("CC", "Meiosis (Meiosis I: Prophase I)"), secs=60)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "The nucleolus and the nuclear envelope are not seen in a cell at metaphase I.",
                 "By the end of diakinesis, the nucleolus disappears and the nuclear envelope breaks down.",
                 True, True, True, "A",
                 "Transition from prophase I to metaphase I",
                 "During diakinesis the chromosomes are fully condensed and the meiotic spindle is assembled. By the "
                 "end of diakinesis the nucleolus disappears and the nuclear envelope breaks down; diakinesis "
                 "represents the transition to metaphase. Hence they are absent at metaphase I, and R explains A.",
                 ["A: true", "R: true", "Lost at the end of diakinesis → absent in the next stage → R explains A"],
                 ncert=ref("CC", "Meiosis (Meiosis I: Prophase I)"), secs=45)

direct(T_CC, "Meiosis", "Advanced",
       "Which event occurs in anaphase of mitosis and in anaphase II of meiosis, but NOT in anaphase I of "
       "meiosis?",
       "Splitting of the centromeres and separation of sister chromatids",
       ["Separation of homologous chromosomes", "Crossing over between non-sister chromatids",
        "Reappearance of the nuclear envelope and nucleolus"], "D",
       "Comparing anaphases",
       "In mitotic anaphase, centromeres split and chromatids separate. Anaphase II is similar: the centromere of "
       "each chromosome splits and sister chromatids move to opposite poles. In anaphase I, the homologous "
       "chromosomes separate, while the sister chromatids remain associated at their centromeres.",
       ["Mitotic anaphase and anaphase II: centromeres split", "Anaphase I: homologues separate, centromeres "
                                                               "intact"],
       why="Separation of homologues happens only in anaphase I. Crossing over occurs in pachytene. The nuclear "
           "envelope and nucleolus reappear in telophase, not anaphase.",
       ncert=ref("CC", "M Phase (Anaphase); Meiosis (Anaphase I; Anaphase II)"), secs=50)

# =============================================================== 7. Photosynthesis (5/6/4)
match_list(T_PS, "Site and pigments", "Basic", "leaf pigment", "colour on a paper chromatogram",
           ["Chlorophyll a", "Chlorophyll b", "Xanthophylls", "Carotenoids"],
           ["Yellow to yellow-orange", "Bright or blue green", "Yellow", "Yellow green"],
           "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "B",
           "Photosynthetic pigments",
           "A chromatographic separation of leaf pigments shows chlorophyll a (bright or blue green), chlorophyll "
           "b (yellow green), xanthophylls (yellow) and carotenoids (yellow to yellow-orange).",
           ["Chlorophyll a → II", "Chlorophyll b → IV", "Xanthophylls → III", "Carotenoids → I"],
           why="The wrong codes swap the two chlorophylls, the xanthophylls and carotenoids, or chlorophyll b and "
               "xanthophylls.",
           ncert=ref("PS", "How Many Types of Pigments are Involved in Photosynthesis?"), secs=35)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "The C4 pathway, a cyclic process that operates in plants with Kranz anatomy, has been named the:",
       "Hatch and Slack pathway", ["EMP pathway", "Krebs cycle", "Z scheme"], "A",
       "C4 pathway",
       "Plants adapted to dry tropical regions have the C4 pathway. This pathway, which has been named the Hatch "
       "and Slack pathway, is again a cyclic process.",
       ["C4 pathway = Hatch and Slack pathway"],
       why="The EMP pathway is glycolysis and the Krebs cycle is the TCA cycle of respiration. The Z scheme is "
           "the pathway of electron transport in the light reaction.",
       ncert=ref("PS", "The C4 Pathway"), secs=20)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "The light reactions (photochemical phase) include all of the following EXCEPT:",
       "fixation of CO₂ into 3-phosphoglyceric acid",
       ["light absorption and water splitting", "oxygen release",
        "formation of ATP and NADPH"], "D",
       "Light reaction",
       "The light reactions or the 'photochemical' phase include light absorption, water splitting, oxygen "
       "release, and the formation of high-energy chemical intermediates, ATP and NADPH. Fixation of CO₂ into "
       "PGA is the carboxylation step of the Calvin cycle, in the biosynthetic phase.",
       ["Light reaction: absorption, water splitting, O₂ release, ATP + NADPH",
        "CO₂ fixation → biosynthetic phase"],
       why="The other three are all listed by NCERT as parts of the light reaction.",
       ncert=ref("PS", "What is Light Reaction?"), secs=25)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Basic",
               "In non-cyclic photophosphorylation, the two photosystems work in series, first PS II and then PS I.",
               "Both ATP and NADPH + H⁺ are synthesised by non-cyclic electron flow.",
               True, True, "A",
               "Non-cyclic photophosphorylation",
               "When the two photosystems work in a series, first PS II and then PS I, non-cyclic "
               "photophosphorylation occurs. The two photosystems are connected through an electron transport "
               "chain, and both ATP and NADPH + H⁺ are synthesised by this kind of electron flow.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "The Electron Transport (Cyclic and Non-cyclic Photo-phosphorylation)"), secs=30)

_ps_percent = Fraction(36, 1000)  # 0.036 per cent by volume
_ps_ul_per_l = _ps_percent / 100 * 10 ** 6
numerical(T_PS, "Limiting factors", "Basic",
          "The CO₂ content of the air is 0.036 per cent by volume. Expressed in microlitres of CO₂ per litre of air "
          "(µL L⁻¹), this concentration is (1 L = 10⁶ µL):",
          "360 µL L⁻¹", ["36 µL L⁻¹", "3600 µL L⁻¹", "0.36 µL L⁻¹"], "B",
          _ps_ul_per_l == 360,
          "CO₂ concentration as a limiting factor",
          "0.036 per cent means 0.036 L of CO₂ in 100 L of air, i.e., 0.00036 L per litre. Multiplying by 10⁶ "
          "µL per litre gives 360 µL L⁻¹. This is the concentration at which NCERT says C4 plants show "
          "saturation, while C3 plants are saturated only beyond 450 µL L⁻¹.",
          ["0.036 % = 0.036 / 100 = 3.6 × 10⁻⁴ L per L", "3.6 × 10⁻⁴ × 10⁶ µL = 360 µL L⁻¹"],
          "36 and 3600 come from a slip of one power of ten. 0.36 forgets to multiply by 10⁶ for the litre to "
          "microlitre conversion.",
          ref("PS", "Factors affecting Photosynthesis (Carbon dioxide Concentration)"), secs=50)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                 "Immediately after light becomes unavailable, the biosynthetic phase of photosynthesis continues "
                 "for some time and then stops.",
                 "The biosynthetic phase does not directly depend on light, but depends on the products of the light "
                 "reaction, ATP and NADPH.",
                 True, True, True, "A",
                 "Light-independent biosynthetic phase",
                 "The biosynthetic phase is not directly light-driven; it uses the ATP and NADPH made in the light "
                 "reaction. So when light is cut off, it goes on for some time, using up the ATP and NADPH already "
                 "made, and then stops; when light is given again, synthesis starts again. R explains A.",
                 ["A: true", "R: true", "Runs on stored ATP/NADPH until they are used up → R explains A"],
                 ncert=ref("PS", "Where are the ATP and NADPH Used?"), secs=45)

multi_statement(T_PS, "Limiting factors", "Intermediate",
                "Which of the following are internal (plant) factors that affect photosynthesis?",
                [("The number, size, age and orientation of leaves", True),
                 ("The internal CO₂ concentration", True),
                 ("The amount of chlorophyll", True),
                 ("The availability of sunlight", False),
                 ("Temperature", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "C",
                "Internal and external factors",
                "The plant (internal) factors include the number, size, age and orientation of leaves, mesophyll "
                "cells and chloroplasts, the internal CO₂ concentration and the amount of chlorophyll. The external "
                "factors include the availability of sunlight, temperature, CO₂ concentration and water.",
                ["(a), (b), (c): internal", "(d), (e): external"],
                why="Every wrong option includes sunlight or temperature, which are external factors.",
                ncert=ref("PS", "Factors affecting Photosynthesis"), secs=45)

direct(T_PS, "Light reactions and photophosphorylation", "Intermediate",
       "In the Z scheme, the electrons that were moved out of photosystem II must be replaced. They are replaced by "
       "electrons:",
       "made available by the splitting of water",
       ["returned from photosystem I by cyclic flow", "donated by NADPH formed in the stroma",
        "released when ATP is broken down"], "B",
       "Splitting of water",
       "The electrons moved from photosystem II must be replaced; this is achieved by electrons available from "
       "the splitting of water, which is associated with PS II. Water is split into 2H⁺, [O] and electrons. The "
       "electrons needed to replace those removed from PS I are provided by PS II.",
       ["Electrons lost from PS II ← water splitting", "Electrons lost from PS I ← PS II"],
       why="Cyclic flow returns electrons to PS I, not PS II. NADPH is the final product that receives electrons, "
           "not a donor to PS II. ATP breakdown does not supply electrons.",
       ncert=ref("PS", "The Electron Transport (Splitting of Water)"), secs=35)

statement_pair(T_PS, "Site and pigments", "Intermediate",
               "Chlorophyll a absorbs maximally in the blue and red regions of the spectrum, and these wavelengths "
               "also show a higher rate of photosynthesis.",
               "The rate of photosynthesis is highest in the green region of the spectrum, where chlorophyll absorbs "
               "most strongly.",
               True, False, "C",
               "Absorption and action",
               "The wavelengths at which chlorophyll a absorbs maximally, the blue and red regions, also show a "
               "higher rate of photosynthesis; hence chlorophyll a is the chief pigment of photosynthesis. Green "
               "light is not where chlorophyll absorbs most strongly, and it does not give the highest rate.",
               ["Statement I: true", "Statement II: false, maximum absorption and rate are in the blue and red "
                                     "regions"],
               ncert=ref("PS", "How Many Types of Pigments are Involved in Photosynthesis?"), secs=40)

statement_pair(T_PS, "Chemiosmosis", "Intermediate",
               "The proton gradient across the thylakoid membrane is broken down by the movement of protons from "
               "the stroma into the lumen through the CF₀ channel.",
               "A conformational change in the CF₁ particle of ATP synthase makes the enzyme synthesise ATP.",
               False, True, "D",
               "Chemiosmotic hypothesis",
               "Protons accumulate in the lumen. The gradient is broken down by the movement of protons across the "
               "membrane from the lumen to the stroma through the transmembrane channel of CF₀. This releases "
               "enough energy to cause a conformational change in the CF₁ particle of the ATP synthase, which makes "
               "the enzyme synthesise ATP.",
               ["Statement I: false, protons move from the lumen to the stroma", "Statement II: true"],
               ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=40)

direct(T_PS, "Site and pigments", "Intermediate",
       "Chlorophyll b, xanthophylls and carotenoids are called accessory pigments because they:",
       "also absorb light and transfer the energy to chlorophyll a",
       ["form the reaction centres of both photosystems", "split water and release oxygen",
        "fix CO₂ in the stroma"], "D",
       "Accessory pigments",
       "Though chlorophyll is the major pigment responsible for trapping light, other thylakoid pigments like "
       "chlorophyll b, xanthophylls and carotenoids, called accessory pigments, also absorb light and transfer "
       "the energy to chlorophyll a. This lets a wider range of wavelengths be used.",
       ["Accessory pigments: absorb light → pass energy to chlorophyll a"],
       why="The reaction centre of each photosystem is a chlorophyll a molecule. Water splitting is associated "
           "with PS II, and CO₂ fixation is done by RuBisCO in the stroma.",
       ncert=ref("PS", "How Many Types of Pigments are Involved in Photosynthesis?"), secs=30)

# RuBP + CO2 -> 2 PGA ; RuBP + O2 -> 1 PGA (phosphoglycerate) + 1 phosphoglycolate
_ps_carbox, _ps_oxy = 8, 2
_ps_pga = _ps_carbox * 2 + _ps_oxy * 1
numerical(T_PS, "Photorespiration", "Advanced",
          "In a C3 leaf, ten molecules of RuBP react with RuBisCO: eight combine with CO₂ and two combine with O₂. "
          "Each carboxylation gives two molecules of PGA, and each oxygenation gives one molecule of PGA and one "
          "of phosphoglycolate. How many molecules of PGA are formed in all?",
          "18", ["20", "16", "14"], "C",
          _ps_pga == 18,
          "Photorespiration lowers PGA output",
          "Carboxylation: 8 × 2 = 16 PGA. Oxygenation (photorespiration): 2 × 1 = 2 PGA, plus 2 phosphoglycolate. "
          "Total PGA = 16 + 2 = 18. Had all ten RuBP been carboxylated, 20 PGA would have formed; photorespiration "
          "reduces the yield.",
          ["Carboxylation: 8 × 2 = 16", "Oxygenation: 2 × 1 = 2", "Total = 18 PGA"],
          "20 treats all ten RuBP as carboxylated. 16 ignores the PGA formed in oxygenation. 14 subtracts the "
          "oxygenation products instead of adding them.",
          ref("PS", "Photorespiration"), secs=75)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Advanced",
                 "Cyclic photophosphorylation, which makes ATP but no NADPH, takes place in chloroplasts besides "
                 "non-cyclic photophosphorylation.",
                 "The Calvin cycle uses 3 ATP but only 2 NADPH for every CO₂ fixed, and cyclic photophosphorylation "
                 "probably takes place to meet this difference.",
                 True, True, True, "A",
                 "Why cyclic photophosphorylation",
                 "For every CO₂ molecule entering the Calvin cycle, 3 molecules of ATP and 2 of NADPH are required. "
                 "NCERT notes that it is probably to meet this difference in the numbers of ATP and NADPH used in "
                 "the dark reaction that cyclic phosphorylation takes place. R gives the reason for A.",
                 ["A: true", "R: true", "Extra ATP need → cyclic flow → R explains A"],
                 ncert=ref("PS", "The Calvin Cycle"), secs=55)

statement_pair(T_PS, "Limiting factors", "Advanced",
               "Even though water is one of the reactants in the light reaction, its effect as a factor is more "
               "through its effect on the plant than directly on photosynthesis.",
               "C3 plants have a much higher temperature optimum for photosynthesis than C4 plants.",
               True, False, "C",
               "Water and temperature as factors",
               "NCERT states that the effect of water as a factor is more through its effect on the plant (stomatal "
               "closure, wilting) than directly on photosynthesis. C4 plants respond to higher temperatures and show "
               "a higher rate of photosynthesis, while C3 plants have a much lower temperature optimum.",
               ["Statement I: true", "Statement II: false, C3 plants have the lower temperature optimum"],
               ncert=ref("PS", "Factors affecting Photosynthesis (Temperature; Water)"), secs=45)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Advanced",
                "Which of the following statements are correct?",
                [("Within the chloroplast, the membrane system is responsible for trapping light energy and for "
                  "the synthesis of ATP and NADPH.", True),
                 ("RuBisCO is named RuBP carboxylase-oxygenase because its active site can bind both CO₂ and O₂.",
                  True),
                 ("While discussing light as a factor, light quality, light intensity and the duration of exposure "
                  "to light have to be distinguished.", True),
                 ("When light is abundant, the rate of photosynthesis is decided by light alone, and other factors "
                  "have no effect.", False),
                 ("Photosynthesis takes place in all parts of the plant, including the roots.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "D",
                "Site, enzyme and factors of photosynthesis",
                "In the chloroplast, the membrane system traps light energy and synthesises ATP and NADPH, while the "
                "stroma holds the enzymes that make sugar. RuBisCO is RuBP carboxylase-oxygenase; its active site "
                "binds both CO₂ and O₂. Light quality, intensity and duration must be distinguished. Photosynthesis "
                "is affected by several factors simultaneously, and the rate is set by the factor nearest its "
                "minimal value. It takes place only in the green parts of the plant, mostly the leaves.",
                ["(a) true", "(b) true", "(c) true", "(d) false: several factors act together",
                 "(e) false: only green parts"],
                why="Every wrong option includes (d) or (e), which are false.",
                ncert=ref("PS", "Where does Photosynthesis take place?; Photorespiration; Factors affecting "
                                "Photosynthesis"), secs=60)

# =============================================================== 8. Respiration in Plants (4/5/4)
direct(T_RES, "ATP yield and amphibolic pathway", "Basic",
       "ATP is called the energy currency of the cell because:",
       "the energy released by oxidation in respiration is used to synthesise ATP, which is broken down whenever "
       "and wherever energy needs to be utilised",
       ["the energy of respiration is used directly by the cell without being stored in any molecule",
        "ATP is the main respiratory substrate oxidised in the mitochondria",
        "ATP stores the energy of glucose permanently and is never broken down"], "D",
       "ATP as energy currency",
       "The energy released by oxidation in respiration is not (or rather cannot be) used directly; it is used to "
       "synthesise ATP, which is broken down whenever and wherever energy needs to be utilised. Hence ATP acts as "
       "the energy currency of the cell.",
       ["Respiration → ATP made", "ATP broken down where energy is needed → energy currency"],
       why="The energy of respiration cannot be used directly. The respiratory substrates are carbohydrates and, "
           "under some conditions, fats, proteins and organic acids, not ATP. ATP is broken down whenever energy "
           "is needed.",
       ncert=ref("RES", "Introduction"), secs=30)

direct(T_RES, "Glycolysis and fermentation", "Basic",
       "Plants have no specialised organs for gaseous exchange. For this purpose they have:",
       "stomata and lenticels",
       ["lungs and air sacs", "root hairs only", "gills on the leaves"], "B",
       "Gaseous exchange in plants",
       "Plants, unlike animals, have no specialised organs for gaseous exchange, but they have stomata and "
       "lenticels for this purpose.",
       ["Plants: stomata (leaves) and lenticels (stems)"],
       why="Lungs, air sacs and gills are animal organs. Root hairs absorb water and minerals; they are not the "
           "structures NCERT names for gaseous exchange.",
       ncert=ref("RES", "Do Plants Breathe?"), secs=20)

direct(T_RES, "Glycolysis and fermentation", "Basic",
       "The term glycolysis has originated from two Greek words, which mean:",
       "sugar and splitting", ["sugar and making", "air and breathing", "glucose and burning"], "B",
       "Meaning of glycolysis",
       "The term glycolysis has originated from the Greek words glycos, for sugar, and lysis, for splitting.",
       ["glycos = sugar; lysis = splitting"],
       why="The other pairs do not match the Greek roots glycos and lysis.",
       ncert=ref("RES", "Glycolysis"), secs=20)

statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "In glycolysis, a chain of ten reactions, under the control of different enzymes, takes place to "
               "produce pyruvate from glucose.",
               "Pyruvic acid is the key product of glycolysis.",
               True, True, "A",
               "Glycolysis",
               "In glycolysis, a chain of ten reactions under the control of different enzymes produces pyruvate "
               "from glucose. Pyruvic acid is the key product of glycolysis; its metabolic fate depends on the "
               "cellular need.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Glycolysis"), secs=30)

# RQ = volume of CO2 evolved / volume of O2 consumed
_res_rq = Fraction(35, 50)
numerical(T_RES, "Respiratory quotient", "Intermediate",
          "Germinating seeds in a respirometer consume 50 mL of O₂ and give out 35 mL of CO₂ in the same time. What "
          "is the respiratory quotient (RQ), and which type of respiratory substrate is mainly being used?",
          "0.7; fat", ["1.43; an organic acid", "0.7; a carbohydrate", "1.0; a carbohydrate"], "B",
          _res_rq == Fraction(7, 10),
          "Respiratory quotient",
          "RQ = volume of CO₂ evolved ÷ volume of O₂ consumed = 35 ÷ 50 = 0.7. For carbohydrates completely "
          "oxidised, RQ = 1; for fats RQ is less than 1 (tripalmitin gives about 0.7). An RQ of 0.7 therefore "
          "points to fat as the substrate.",
          ["RQ = CO₂ / O₂ = 35 / 50 = 0.7", "Carbohydrate: 1; fat: less than 1 (about 0.7)", "→ fat"],
          "1.43 inverts the ratio (O₂ ÷ CO₂). A carbohydrate gives an RQ of 1, not 0.7. 1.0 does not follow from "
          "the volumes given.",
          ref("RES", "Respiratory Quotient"), secs=60)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "Plants do not present great demands for gas exchange.",
                 "Roots, stems and leaves respire at rates far lower than animals do.",
                 True, True, True, "A",
                 "Why plants need no respiratory organs",
                 "NCERT gives three reasons why plants can get along without respiratory organs. The second is that "
                 "plants do not present great demands for gas exchange, because roots, stems and leaves respire at "
                 "rates far lower than animals do; only during photosynthesis are large volumes of gases exchanged. "
                 "R explains A.",
                 ["A: true", "R: true", "Low respiratory rate → low demand for gas exchange → R explains A"],
                 ncert=ref("RES", "Do Plants Breathe?"), secs=40)

multi_statement(T_RES, "Glycolysis and fermentation", "Intermediate",
                "Which of the following statements about the fate of pyruvic acid are correct?",
                [("The three major ways in which cells handle pyruvic acid are lactic acid fermentation, "
                  "alcoholic fermentation and aerobic respiration.", True),
                 ("Fermentation takes place under anaerobic conditions in many prokaryotes and unicellular "
                  "eukaryotes.", True),
                 ("Some bacteria produce lactic acid from pyruvic acid.", True),
                 ("In fermentation, glucose is completely degraded to CO₂ and H₂O.", False)],
                [("a", "b", "d"), ("a", "c", "d"), ("b", "c", "d")], "B",
                "Fates of pyruvic acid",
                "Pyruvic acid formed in glycolysis is handled in three major ways: lactic acid fermentation, "
                "alcoholic fermentation and aerobic respiration. Fermentation occurs under anaerobic conditions in "
                "many prokaryotes and unicellular eukaryotes; some bacteria produce lactic acid from pyruvic acid. "
                "Fermentation accounts for only a partial breakdown of glucose; complete degradation to CO₂ and "
                "H₂O happens in aerobic respiration.",
                ["(a) true", "(b) true", "(c) true", "(d) false: fermentation is a partial breakdown"],
                why="Every wrong option includes the false statement (d).",
                ncert=ref("RES", "Fermentation"), secs=45)

match_list(T_RES, "Electron transport system", "Intermediate", "enzyme or complex", "role",
           ["Citrate synthase", "NADH dehydrogenase (complex I)", "Cytochrome bc₁ complex (complex III)",
            "F₁ headpiece of ATP synthase"],
           ["Contains the site for the synthesis of ATP from ADP and inorganic phosphate",
            "Transfers electrons from reduced ubiquinone (ubiquinol) to cytochrome c",
            "Condenses the acetyl group with oxaloacetic acid and water to form citric acid",
            "Oxidises NADH and passes the electrons to ubiquinone"],
           "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "C",
           "TCA cycle and ETS enzymes",
           "The TCA cycle starts with the condensation of the acetyl group with OAA and water to give citric acid, "
           "catalysed by citrate synthase. In the ETS, NADH dehydrogenase (complex I) oxidises NADH and transfers "
           "the electrons to ubiquinone. Reduced ubiquinone (ubiquinol) is oxidised with the transfer of electrons "
           "to cytochrome c via the cytochrome bc₁ complex (complex III). The F₁ headpiece of ATP synthase is a "
           "peripheral membrane protein complex that contains the site for ATP synthesis.",
           ["Citrate synthase → III", "Complex I → IV", "Complex III → II", "F₁ → I"],
           why="The wrong codes swap citrate synthase with complex I, complex I with complex III, or complex III "
               "with the F₁ headpiece.",
           ncert=ref("RES", "Tricarboxylic Acid Cycle; Electron Transport System (ETS) and Oxidative "
                            "Phosphorylation"), secs=50)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
               "Glycerol enters the respiratory pathway after being converted to PGAL.",
               "Fatty acids enter the respiratory pathway after being converted to pyruvic acid.",
               True, False, "C",
               "Fats in the respiratory pathway",
               "Fats are first broken down into glycerol and fatty acids. Glycerol enters the pathway after being "
               "converted to PGAL (3-phosphoglyceraldehyde). Fatty acids are degraded to acetyl CoA and enter the "
               "pathway at that point, not as pyruvic acid.",
               ["Statement I: true", "Statement II: false, fatty acids enter as acetyl CoA"],
               ncert=ref("RES", "Amphibolic Pathway"), secs=40)

# Balance sheet: 10 NADH x 3 + 2 FADH2 x 2 = 34 ATP via ETS (through F0); substrate level: 2 (net, glycolysis)
# + 2 (GTP in TCA) = 4; total 38. Each ATP made by ATP synthase needs 2 H+ through F0.
_res_ets_atp = 10 * 3 + 2 * 2
_res_substrate = 2 + 2
_res_protons = _res_ets_atp * 2
numerical(T_RES, "Electron transport system", "Advanced",
          "Use the assumptions of the respiratory balance sheet: complete oxidation of one glucose gives 10 NADH "
          "and 2 FADH₂ in all; every NADH (including that of glycolysis) is oxidised in the ETS, giving 3 ATP, and "
          "every FADH₂ gives 2 ATP; and 2 H⁺ pass through F₀ for each ATP made by ATP synthase. The remaining ATP "
          "(net 2 in glycolysis and 2 from GTP in the TCA cycle) is made directly. How many protons pass through "
          "F₀ for the oxidation of one glucose?",
          "68", ["76", "60", "72"], "D",
          _res_ets_atp == 34 and _res_ets_atp + _res_substrate == 38 and _res_protons == 68,
          "Oxidative phosphorylation and proton flow",
          "ATP made by ATP synthase (oxidative phosphorylation) = 10 × 3 + 2 × 2 = 34. The other 4 of the 38 ATP "
          "are made directly in glycolysis and the TCA cycle and need no proton flow. Protons through F₀ = 34 × 2 "
          "= 68.",
          ["ETS ATP = 10 × 3 + 2 × 2 = 34", "Direct ATP = 2 + 2 = 4 (total 38)", "Protons = 34 × 2 = 68"],
          "76 counts all 38 ATP as made by ATP synthase. 60 counts only the ATP from NADH. 72 removes only the 2 ATP "
          "formed via GTP and forgets the net 2 ATP made directly in glycolysis.",
          ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation; The Respiratory Balance Sheet"),
          secs=120)

multi_statement(T_RES, "Electron transport system", "Advanced",
                "Which of the following statements about the electron transport system are correct?",
                [("The number of ATP molecules synthesised depends on the nature of the electron donor.", True),
                 ("The electron transport system is present in the inner mitochondrial membrane.", True),
                 ("As electrons pass from complex I to complex IV, the flow is coupled to ATP synthase (complex V) "
                  "for the production of ATP.", True),
                 ("Complex IV transfers electrons to ubiquinone.", False),
                 ("Oxygen is the first acceptor of the electrons removed from NADH.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "D",
                "Electron transport system",
                "The ETS is present in the inner mitochondrial membrane. Electrons from NADH pass to ubiquinone via "
                "complex I, then through complex III and cytochrome c to complex IV (cytochrome c oxidase), and "
                "finally to oxygen, the final acceptor. Their passage from complex I to IV is coupled to ATP "
                "synthase (complex V). The number of ATP molecules synthesised depends on the nature of the electron "
                "donor: 3 per NADH and 2 per FADH₂.",
                ["(a) true", "(b) true", "(c) true", "(d) false: complex I passes electrons to ubiquinone",
                 "(e) false: oxygen is the final acceptor"],
                why="Every wrong option includes (d) or (e), which are false.",
                ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=60)

assertion_reason(T_RES, "ATP yield and amphibolic pathway", "Advanced",
                 "Cells oxidise glucose not in one step but in several small steps.",
                 "In stepwise oxidation, some steps release just enough energy to be coupled to ATP synthesis, so "
                 "not all the liberated energy goes out as heat.",
                 True, True, True, "A",
                 "Stepwise release of energy",
                 "If glucose were burnt in one step, as in complete combustion, most of the energy would be given "
                 "out as heat and could not be trapped. Plant cells catabolise glucose in several small steps, some "
                 "just large enough for the released energy to be coupled to ATP synthesis. R explains why cells "
                 "use the stepwise route.",
                 ["A: true", "R: true", "Stepwise release lets energy be trapped as ATP → R explains A"],
                 ncert=ref("RES", "Introduction"), secs=45)

statement_pair(T_RES, "TCA cycle", "Advanced",
               "Two molecules of NADH are produced when the two molecules of pyruvic acid formed from one glucose "
               "are converted to acetyl CoA.",
               "Two molecules of FADH₂ are produced when the two molecules of pyruvic acid formed from one glucose "
               "are converted to acetyl CoA.",
               True, False, "C",
               "Link reaction",
               "Pyruvate entering the mitochondrial matrix undergoes oxidative decarboxylation by pyruvic "
               "dehydrogenase, with NAD⁺ and coenzyme A. During this process two molecules of NADH are produced from "
               "the two molecules of pyruvic acid derived from one glucose. FADH₂ is not formed here; it is formed "
               "in the TCA cycle (one per acetyl CoA).",
               ["Statement I: true", "Statement II: false, FADH₂ is formed in the TCA cycle, not in the link "
                                     "reaction"],
               ncert=ref("RES", "Aerobic Respiration"), secs=40)


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
    assert pkg["output"] == "batches/parts/BATCH_004_BOT_p1.json"


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
           "notes": "Package BOT_004_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 123 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
