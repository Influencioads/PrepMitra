"""Writes batches/parts/BATCH_001_BOT_p1.json: package BOT_001_p1 of batch 1 (Botany, 121 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_000006 .. NEET_BOT_000126.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement;
  * the quota per (topic, difficulty), the ID range and the answer-key balance are checked.
If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_001/BOT_001_p1.py
"""

import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_001_BOT_p1.json"
PACKAGE = "BOT_001_p1"
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


QUESTIONS = []  # records in ID order; free-placement records get their options in place_free()


def _record(topic, sub, diff, fmt, text, concept, expl, steps, why, ncert, secs, verified_by, short=None):
    assert diff in ("Basic", "Intermediate", "Advanced") and ncert and 20 <= secs <= 180
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


def direct(topic, sub, diff, text, correct, wrong, concept, expl, steps, why=None, ncert=None, secs=30, short=None):
    """Plain MCQ; the correct option's position is chosen later to balance the answer key."""
    assert len(wrong) == 3 and correct not in wrong
    rec = _record(topic, sub, diff, "direct", text, concept, expl, steps, why, ncert, secs, AUTHORED, short)
    rec["_free"] = (correct, list(wrong))
    QUESTIONS.append(rec)


def numerical(topic, sub, diff, text, options, answer, value_check, concept, expl, steps, why, ncert, secs=60,
              short=None):
    """Numerical with fixed option order; value_check must be True (the builder's recomputation)."""
    assert value_check is True
    rec = _record(topic, sub, diff, "numerical", text, concept, expl, steps, why, ncert, secs, RECOMPUTED, short)
    _fix(rec, options, answer)
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


def multi_statement(topic, sub, diff, lead, statements, wrong_combos, concept, expl, steps, why=None, ncert=None,
                    secs=60):
    """statements: list of (text, is_true). The correct combination is derived from the truth values."""
    labels = "abcde"[:len(statements)]
    correct = tuple(labels[i] for i, (_, t) in enumerate(statements) if t)
    assert correct and len(correct) < len(statements), "need at least one true and one false statement"
    wrong = [tuple(w) for w in wrong_combos]
    assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3
    body = "\n".join(f"({labels[i]}) {s}" for i, (s, _) in enumerate(statements))
    text = f"{lead}\n\n{body}\n\nChoose the correct answer from the options given below:"
    rec = _record(topic, sub, diff, "multi_statement", text, concept, expl, steps, why, ncert, secs, AUTHORED)
    rec["_free"] = (combo_label(correct), [combo_label(w) for w in wrong])
    QUESTIONS.append(rec)


def _code(m):
    return ", ".join(f"{k}-{m[k]}" for k in "ABCD")


def match_list(topic, sub, diff, head1, head2, list1, list2, correct, wrongs, concept, expl, steps, why=None,
               ncert=None, secs=45):
    """list1: 4 items (A-D); list2: 4 items (I-IV); correct/wrongs: dicts like {'A': 'II', ...}."""
    nums = ["I", "II", "III", "IV"]
    assert len(list1) == 4 and len(list2) == 4
    for m in [correct, *wrongs]:
        assert sorted(m.values(), key=nums.index) == nums and sorted(m) == list("ABCD")
    assert len(wrongs) == 3 and len({_code(m) for m in [correct, *wrongs]}) == 4
    l1 = "\n".join(f"{k}. {t}" for k, t in zip("ABCD", list1))
    l2 = "\n".join(f"{n}. {t}" for n, t in zip(nums, list2))
    text = (f"Match List-I ({head1}) with List-II ({head2}).\n\nList-I:\n{l1}\n\nList-II:\n{l2}\n\n"
            "Choose the correct answer from the options given below:")
    rec = _record(topic, sub, diff, "match_list", text, concept, expl, steps, why, ncert, secs, AUTHORED)
    rec["_free"] = (_code(correct), [_code(w) for w in wrongs])
    QUESTIONS.append(rec)


# =============================================================== 1. The Living World and Classification (5/7/5)
direct(T_LIV, "What is living", "Basic",
       "Which of the following is a defining feature of all living organisms, without any exception?",
       "Metabolism", ["Growth", "Reproduction", "Increase in body mass"],
       "Defining features of life",
       "Growth and increase in mass are also shown by non-living things (a mountain or sand mound grows by "
       "accumulation of material on its surface), and many living organisms do not reproduce. Metabolism, the sum "
       "of all chemical reactions in the body, is found in every living organism and in no non-living object.",
       ["Growth / increase in mass: also seen in non-living objects → not defining",
        "Reproduction: absent in mules, sterile worker bees → not defining",
        "Metabolism: present in all living organisms, absent in non-living things → defining"],
       why="Growth and increase in body mass occur in non-living objects too (by accumulation on the surface); "
           "reproduction is absent in several living organisms.",
       ncert=ref("LW", "What is 'living'?"), secs=25)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "The families Felidae and Canidae are placed together in the order:",
       "Carnivora", ["Primata", "Polymoniales", "Sapindales"],
       "Taxonomic categories: family and order",
       "An order is a group of related families. Felidae (cats) and Canidae (dogs) share several features and are "
       "grouped in the animal order Carnivora.",
       ["Family Felidae (e.g. Panthera, Felis) and family Canidae → order Carnivora"],
       why="Primata is the order of monkeys, gorilla and gibbon (and man). Polymoniales and Sapindales are plant "
           "orders.",
       ncert=ref("LW", "Taxonomic categories (order)"), secs=25)

direct(T_LIV, "Binomial nomenclature", "Basic",
       "The scientific names of plants are given according to the principles and criteria laid down in:",
       "International Code for Botanical Nomenclature (ICBN)",
       ["International Code of Zoological Nomenclature (ICZN)", "Five kingdom classification of Whittaker",
        "Two kingdom classification of Linnaeus"],
       "Codes of nomenclature",
       "Names of plants follow the agreed principles of the ICBN; animal names follow the ICZN. Classification "
       "systems group organisms but do not lay down naming rules.",
       ["Plants → ICBN", "Animals → ICZN"],
       why="ICZN is for animals. The two- and five-kingdom systems are systems of classification, not codes of "
           "naming.",
       ncert=ref("LW", "Nomenclature"), secs=25)

statement_pair(T_LIV, "Five kingdom classification", "Basic",
               "R.H. Whittaker proposed the five kingdom classification in 1969.",
               "The five kingdoms are Monera, Protista, Fungi, Plantae and Animalia.",
               True, True, "A",
               "Whittaker's five kingdom system",
               "Whittaker (1969) proposed five kingdoms: Monera, Protista, Fungi, Plantae and Animalia. The main "
               "criteria were cell structure, body organisation, mode of nutrition, reproduction and phylogenetic "
               "relationships.",
               ["Statement I: Whittaker, 1969 → true", "Statement II: the five kingdoms are correctly listed → true"],
               ncert=ref("BC", "introduction (five kingdom classification)"), secs=25)

direct(T_LIV, "Lichens, viruses and viroids", "Basic",
       "A viroid differs from a virus in that a viroid:",
       "is a free RNA that lacks a protein coat",
       ["contains both DNA and RNA", "is a free DNA enclosed in a protein coat",
        "is a protein that lacks nucleic acid"],
       "Viroids",
       "T.O. Diener (1971) found that the agent of potato spindle tuber disease is a free RNA of low molecular "
       "weight. It lacks the protein coat found in viruses, hence the name viroid.",
       ["Viroid = free, low molecular weight RNA", "No protein coat (unlike a virus)"],
       why="No virus or viroid has both DNA and RNA. A viroid's nucleic acid is RNA, not DNA. A protein without "
           "nucleic acid describes a prion.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=30)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate",
           "organism", "habitat or feature",
           ["Halophiles", "Thermoacidophiles", "Methanogens", "Nostoc"],
           ["Hot springs", "Marshy areas and the gut of ruminants", "Extremely salty areas",
            "Heterocysts that fix atmospheric nitrogen"],
           {"A": "III", "B": "I", "C": "II", "D": "IV"},
           [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
            {"A": "II", "B": "I", "C": "III", "D": "IV"}],
           "Kingdom Monera: archaebacteria and cyanobacteria",
           "Archaebacteria live in harsh habitats: halophiles in extreme salty areas, thermoacidophiles in hot "
           "springs and methanogens in marshy areas (some also live in the gut of cows and buffaloes and produce "
           "methane from their dung). Cyanobacteria such as Nostoc and Anabaena fix nitrogen in heterocysts.",
           ["Halophiles → extreme salty areas (III)", "Thermoacidophiles → hot springs (I)",
            "Methanogens → marshy areas, gut of ruminants (II)", "Nostoc → heterocysts, N₂ fixation (IV)"],
           why="The wrong codes swap the habitats of the three archaebacterial groups.",
           ncert=ref("BC", "Kingdom Monera (archaebacteria, eubacteria)"), secs=40)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about members of kingdom Protista are correct?",
                [("The cell walls of diatoms are embedded with silica, which makes them indestructible.", True),
                 ("Red dinoflagellates such as Gonyaulax can multiply so rapidly that the sea appears red.", True),
                 ("Euglenoids have a cellulose cell wall.", False),
                 ("The spores of slime moulds possess true walls and are extremely resistant.", True),
                 ("Most dinoflagellates live in fresh water.", False)],
                [("a", "c", "d"), ("b", "d", "e"), ("a", "b", "c", "d")],
                "Kingdom Protista: chrysophytes, dinoflagellates, euglenoids, slime moulds",
                "Diatom walls form two thin overlapping shells embedded with silica. Red tides are caused by rapid "
                "multiplication of red dinoflagellates such as Gonyaulax. Euglenoids have no cell wall; instead they "
                "have a protein-rich pellicle. Slime mould spores have true walls and survive for many years. "
                "Dinoflagellates are mostly marine.",
                ["(a) True: silica walls, accumulate as diatomaceous earth", "(b) True: red tides",
                 "(c) False: euglenoids have a protein-rich pellicle, not a cell wall",
                 "(d) True: resistant spores dispersed by air", "(e) False: dinoflagellates are mostly marine"],
                why="Statement (c) is the usual trap: the flexible pellicle of Euglena is not a cell wall.",
                ncert=ref("BC", "Kingdom Protista"), secs=60)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate",
           "class of fungi", "example",
           ["Phycomycetes", "Ascomycetes", "Basidiomycetes", "Deuteromycetes"],
           ["Agaricus", "Mucor", "Alternaria", "Neurospora"],
           {"A": "II", "B": "IV", "C": "I", "D": "III"},
           [{"A": "II", "B": "I", "C": "IV", "D": "III"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
            {"A": "II", "B": "III", "C": "I", "D": "IV"}],
           "Classes of kingdom Fungi",
           "Phycomycetes have aseptate, coenocytic mycelium (Mucor, Rhizopus, Albugo). Ascomycetes are sac fungi "
           "(Neurospora, Aspergillus, Claviceps). Basidiomycetes include mushrooms (Agaricus), smuts and rusts. "
           "Deuteromycetes are the imperfect fungi (Alternaria, Colletotrichum, Trichoderma).",
           ["Phycomycetes → Mucor (II)", "Ascomycetes → Neurospora (IV)", "Basidiomycetes → Agaricus (I)",
            "Deuteromycetes → Alternaria (III)"],
           why="Neurospora is a sac fungus (ascomycete), not a mushroom; Alternaria has no known sexual stage, so it "
               "is a deuteromycete.",
           ncert=ref("BC", "Kingdom Fungi"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Members of Deuteromycetes are commonly called imperfect fungi.",
                 "Only the asexual or vegetative phases of these fungi are known.",
                 True, True, True, "A",
                 "Deuteromycetes (imperfect fungi)",
                 "A fungus is called 'imperfect' because its sexual stage is not known; only its asexual or "
                 "vegetative phase has been seen. When the sexual stage of such a fungus is discovered, it is moved "
                 "to the class it belongs to. So R is exactly why they are called imperfect.",
                 ["A: Deuteromycetes = imperfect fungi → true", "R: only asexual/vegetative phases known → true",
                  "The missing sexual stage is the reason for the name → R explains A"],
                 ncert=ref("BC", "Kingdom Fungi (Deuteromycetes)"), secs=35)

statement_pair(T_LIV, "Lichens, viruses and viroids", "Intermediate",
               "In a lichen, the algal partner is called the mycobiont.",
               "Lichens do not grow in polluted areas, so they are good indicators of pollution.",
               False, True, "D",
               "Lichens: a symbiotic association",
               "A lichen is a mutually useful association of an alga and a fungus. The algal component is the "
               "phycobiont and the fungal component is the mycobiont. The alga makes food; the fungus provides "
               "shelter and absorbs water and minerals. Lichens do not grow in polluted areas.",
               ["Algal partner = phycobiont, fungal partner = mycobiont → Statement I false",
                "Lichens are absent from polluted areas → Statement II true"],
               ncert=ref("BC", "Viruses, Viroids, Prions and Lichens (lichens)"), secs=30)

multi_statement(T_LIV, "Taxonomy and hierarchy", "Intermediate",
                "Which of the following statements about taxonomic categories are correct?",
                [("Lion, tiger and leopard are species of the same genus.", True),
                 ("The families Convolvulaceae and Solanaceae are placed in the same order, mainly on the basis "
                  "of floral characters.", True),
                 ("In plants, classes with a few similar characters are grouped into a higher category called "
                  "division.", True),
                 ("As we go up from species to kingdom, the number of characters common to the members of a "
                  "category increases.", False)],
                [("a", "c", "d"), ("b", "d"), ("a", "b", "c", "d")],
                "Taxonomic hierarchy",
                "Lion (Panthera leo), leopard (P. pardus) and tiger (P. tigris) belong to the genus Panthera. "
                "Convolvulaceae and Solanaceae are placed in the order Polymoniales mainly on floral characters. "
                "In plants, the category above class is called division (phylum in animals). Higher categories "
                "hold more kinds of organisms, which share fewer characters.",
                ["(a) True: genus Panthera", "(b) True: order Polymoniales, based on floral characters",
                 "(c) True: division is used for plants", "(d) False: common characters decrease going up"],
                why="Statement (d) reverses the rule: the higher the category, the broader it is and the fewer "
                    "characters its members share.",
                ncert=ref("LW", "Taxonomic categories"), secs=50)

assertion_reason(T_LIV, "What is living", "Intermediate",
                 "Reproduction cannot be taken as an all-inclusive defining characteristic of living organisms.",
                 "Many organisms, such as mules, sterile worker bees and infertile human couples, do not "
                 "reproduce.",
                 True, True, True, "A",
                 "Why reproduction is not a defining feature of life",
                 "A defining feature must be present in every living organism. NCERT points out that mules, sterile "
                 "worker bees and infertile human couples are living but do not reproduce, so reproduction cannot "
                 "define life. R states exactly these exceptions, so it explains A.",
                 ["A: true", "R: true (NCERT's own examples)",
                  "Living things that cannot reproduce show reproduction is not all-inclusive → R explains A"],
                 why="Option B is the trap: R is not a side fact here; it is the very reason NCERT gives for A.",
                 ncert=ref("LW", "What is 'living'? (reproduction)"), secs=45)

match_list(T_LIV, "Five kingdom classification", "Advanced",
           "kingdom", "cell wall",
           ["Monera", "Fungi", "Plantae", "Animalia"],
           ["Absent", "Present, made of cellulose", "Non-cellulosic, made of polysaccharide and amino acids",
            "Present, without cellulose (chitin and polysaccharides)"],
           {"A": "III", "B": "IV", "C": "II", "D": "I"},
           [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
            {"A": "I", "B": "IV", "C": "II", "D": "III"}],
           "Characteristics of the five kingdoms (cell wall)",
           "Bacteria have a non-cellulosic wall of polysaccharide and amino acids. Fungal walls lack cellulose and are "
           "made of chitin and polysaccharides. Plant cell walls are mainly cellulose. Animal cells have no cell wall.",
           ["Monera → non-cellulosic (polysaccharide + amino acid) (III)",
            "Fungi → without cellulose, chitin (IV)", "Plantae → cellulose (II)", "Animalia → absent (I)"],
           why="Swapping III and IV is the common error: chitin is the fungal wall material, while the bacterial wall "
               "is made of polysaccharide and amino acids.",
           ncert=ref("BC", "Table: characteristics of the five kingdoms; Kingdom Fungi"), secs=50)

multi_statement(T_LIV, "What is living", "Advanced",
                "Read the following statements about the features of living organisms.",
                [("Metabolic reactions demonstrated in a test tube (in vitro) are living things.", False),
                 ("Photoperiod affects reproduction in seasonal breeders, both plants and animals.", True),
                 ("Human beings are the only organisms that are aware of themselves (self-conscious).", True),
                 ("In animals, growth by cell division continues throughout the life span.", False)],
                [("b", "c", "d"), ("a", "b", "c"), ("c", "d")],
                "Properties of living organisms",
                "Isolated metabolic reactions in vitro are not living things, though they are living reactions. All "
                "organisms sense their environment; photoperiod, for example, affects reproduction in seasonal "
                "breeders. Only humans have self-consciousness. Plants grow by cell division throughout life, but "
                "animals grow only up to a certain age (cell division continues only to replace lost cells).",
                ["(a) False: in vitro reactions are not living things", "(b) True: response to photoperiod",
                 "(c) True: self-consciousness is unique to humans", "(d) False: true of plants, not animals"],
                why="(d) describes plants. In animals, growth stops at a certain age.",
                ncert=ref("LW", "What is 'living'?"), secs=60)

multi_statement(T_LIV, "Binomial nomenclature", "Advanced",
                "Which of the following are rules of binomial nomenclature?",
                [("Biological names are generally in Latin and written in italics.", True),
                 ("The first word of the name is the genus and the second is the specific epithet.", True),
                 ("Both words of the name begin with a capital letter.", False),
                 ("When handwritten, the two words are underlined separately.", True),
                 ("The author's name, in abbreviated form, is written after the specific epithet.", True)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d", "e")],
                "Binomial nomenclature (Linnaeus)",
                "Each name has a generic name and a specific epithet, Latinised and printed in italics (underlined "
                "separately when handwritten). The genus begins with a capital letter, the specific epithet with a "
                "small letter. The author's name comes at the end in abbreviated form, e.g. Mangifera indica Linn.",
                ["(a) True", "(b) True", "(c) False: the specific epithet starts with a small letter",
                 "(d) True", "(e) True: e.g. Mangifera indica Linn."],
                why="Any option containing (c) is wrong: 'Mangifera Indica' is incorrectly written.",
                ncert=ref("LW", "Nomenclature (binomial nomenclature)"), secs=50)

multi_statement(T_LIV, "Lichens, viruses and viroids", "Advanced",
                "Which of the following statements are correct?",
                [("Viruses have an inert crystalline structure outside a living cell.", True),
                 ("Some viruses contain both DNA and RNA.", False),
                 ("Viruses that infect plants generally have single-stranded RNA.", True),
                 ("Bacteriophages are usually double-stranded DNA viruses.", True),
                 ("Prions are infectious agents made of abnormally folded RNA.", False)],
                [("a", "b", "c"), ("c", "d", "e"), ("a", "c", "d", "e")],
                "Viruses and prions",
                "Viruses are non-cellular and inert outside a host cell. Their genetic material is either RNA or DNA, "
                "never both. Plant viruses generally have single-stranded RNA; animal viruses have single- or double-"
                "stranded RNA or double-stranded DNA; bacteriophages usually have double-stranded DNA. Prions are "
                "abnormally folded proteins.",
                ["(a) True", "(b) False: no virus contains both RNA and DNA", "(c) True", "(d) True",
                 "(e) False: prions consist of abnormally folded protein"],
                why="(b) and (e) are false, so only the combination (a), (c), (d) fits.",
                ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=60)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Archaebacteria can live in some of the harshest habitats, such as extreme salty areas and hot "
                 "springs.",
                 "Archaebacteria have a cell wall structure different from that of other bacteria.",
                 True, True, True, "A",
                 "Archaebacteria and extreme habitats",
                 "NCERT states that archaebacteria differ from other bacteria in having a different cell wall "
                 "structure, and that this feature is responsible for their survival in extreme conditions. So R "
                 "is the correct explanation of A.",
                 ["A: halophiles, thermoacidophiles, methanogens live in extreme habitats → true",
                  "R: different cell wall structure → true",
                  "NCERT links the two: the cell wall structure is responsible for survival → R explains A"],
                 why="Option B is the trap: students often treat the cell wall as an unrelated fact, but NCERT names it "
                     "as the cause.",
                 ncert=ref("BC", "Kingdom Monera (archaebacteria)"), secs=45)

# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "Agar, used to grow microbes and in ice-creams and jellies, is obtained commercially from:",
       "Gelidium and Gracilaria", ["Laminaria and Fucus", "Chlorella and Volvox", "Ectocarpus and Sargassum"],
       "Economic importance of algae",
       "Agar is obtained from the red algae Gelidium and Gracilaria.",
       ["Agar → red algae Gelidium and Gracilaria"],
       why="Laminaria, Fucus, Ectocarpus and Sargassum are brown algae; Chlorella and Volvox are green algae.",
       ncert=ref("PK", "Algae (uses of algae)"), secs=25)

direct(T_PK, "Bryophytes", "Basic",
       "Bryophytes are called the 'amphibians of the plant kingdom' because they:",
       "live in soil but depend on water for sexual reproduction",
       ["live partly in fresh water and partly in sea water", "have both aquatic roots and aerial leaves",
        "have a free-living sporophyte and a free-living gametophyte"],
       "Bryophytes",
       "Bryophytes grow on land, usually in damp, shaded places, but their male gametes (antherozoids) need water "
       "to swim to the archegonium.",
       ["Habitat: soil (land)", "Fertilisation: antherozoids reach the egg through water"],
       why="Bryophytes have no true roots or leaves, and their sporophyte is not free-living.",
       ncert=ref("PK", "Bryophytes"), secs=25)

direct(T_PK, "Pteridophytes", "Basic",
       "In Selaginella and Equisetum, the sporophylls are compactly arranged to form:",
       "strobili (cones)", ["sori", "gemma cups", "prothalli"],
       "Sporophylls in pteridophytes",
       "In pteridophytes, sporangia are borne on leaf-like sporophylls. In some (Selaginella, Equisetum) the "
       "sporophylls form distinct compact structures called strobili or cones.",
       ["Sporangia on sporophylls", "Compact groups of sporophylls → strobili (cones)"],
       why="Gemma cups are found on liverwort thalli; a prothallus is the pteridophyte gametophyte. Sori are not "
           "described for these two genera.",
       ncert=ref("PK", "Pteridophytes"), secs=25)

direct(T_PK, "Gymnosperms", "Basic",
       "The specialised coralloid roots of Cycas are associated with:",
       "nitrogen-fixing cyanobacteria", ["mycorrhizal fungi", "nitrogen-fixing Rhizobium", "red algae"],
       "Roots of gymnosperms",
       "Gymnosperms usually have tap roots. In Cycas, small specialised roots called coralloid roots are associated "
       "with N₂-fixing cyanobacteria. Pinus roots have fungal association (mycorrhiza).",
       ["Cycas coralloid roots → cyanobacteria", "Pinus roots → mycorrhiza"],
       why="Mycorrhiza is the association in Pinus roots. Rhizobium forms root nodules in legumes, not in Cycas.",
       ncert=ref("PK", "Gymnosperms"), secs=25)

statement_pair(T_PK, "Algae", "Basic",
               "Chlorella, a unicellular alga rich in proteins, is used as a food supplement even by space "
               "travellers.",
               "Algin is obtained from red algae and carrageen from brown algae.",
               True, False, "C",
               "Uses of algae",
               "Chlorella is used as a food supplement, even by space travellers. Hydrocolloids: algin comes from "
               "brown algae and carrageen from red algae, so Statement II has them reversed.",
               ["Statement I: true", "Statement II: false, algin → brown algae, carrageen → red algae"],
               ncert=ref("PK", "Algae (uses of algae)"), secs=30)

match_list(T_PK, "Algae", "Intermediate",
           "alga", "description",
           ["Volvox", "Ulothrix", "Kelps", "Porphyra"],
           ["A filamentous green alga", "A member of Rhodophyceae", "A colonial green alga",
            "Marine forms with massive plant bodies"],
           {"A": "III", "B": "I", "C": "IV", "D": "II"},
           [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
            {"A": "IV", "B": "I", "C": "III", "D": "II"}],
           "Forms of algae",
           "Algae range from colonial forms like Volvox and filamentous forms like Ulothrix and Spirogyra to marine "
           "kelps with massive plant bodies. Porphyra is a red alga (Rhodophyceae).",
           ["Volvox → colonial (III)", "Ulothrix → filamentous (I)", "Kelps → massive marine bodies (IV)",
            "Porphyra → Rhodophyceae (II)"],
           why="Volvox is colonial, not filamentous; Porphyra is red, not a kelp.",
           ncert=ref("PK", "Algae"), secs=40)

statement_pair(T_PK, "Algae", "Intermediate",
               "Members of Rhodophyceae contain chlorophyll a, chlorophyll d and phycoerythrin.",
               "Flagella are absent in members of Rhodophyceae.",
               True, True, "A",
               "Rhodophyceae (red algae)",
               "Red algae owe their colour to the red pigment r-phycoerythrin; their pigments are chlorophyll a, d and "
               "phycoerythrin. They have no flagella; asexual reproduction is by non-motile spores and sexual "
               "reproduction by non-motile gametes.",
               ["Pigments: chl a, d, phycoerythrin → Statement I true", "Flagella: absent → Statement II true"],
               ncert=ref("PK", "Algae (Rhodophyceae; table of algal classes)"), secs=35)

multi_statement(T_PK, "Bryophytes", "Intermediate",
                "Which of the following statements about bryophytes are correct?",
                [("The main plant body is haploid and produces gametes.", True),
                 ("The sporophyte is free-living and independent of the gametophyte.", False),
                 ("The antherozoids are biflagellate.", True),
                 ("Some cells of the sporophyte undergo meiosis to form haploid spores.", True),
                 ("Each archegonium produces many eggs.", False)],
                [("a", "b", "c"), ("c", "d", "e"), ("a", "c", "d", "e")],
                "Life features of bryophytes",
                "The dominant bryophyte plant is the haploid gametophyte. The antheridium makes biflagellate "
                "antherozoids; the flask-shaped archegonium makes a single egg. The zygote grows into a sporophyte "
                "that stays attached to the gametophyte and is nourished by it. Meiosis in the sporophyte gives "
                "haploid spores.",
                ["(a) True", "(b) False: sporophyte is attached to and nourished by the gametophyte", "(c) True",
                 "(d) True: meiosis in the capsule", "(e) False: archegonium has a single egg"],
                ncert=ref("PK", "Bryophytes"), secs=55)

assertion_reason(T_PK, "Bryophytes", "Intermediate",
                 "Sphagnum is used as packing material for the trans-shipment of living material.",
                 "Sphagnum has a very poor water-holding capacity.",
                 True, False, False, "C",
                 "Economic importance of mosses",
                 "Sphagnum is used as packing material for sending living material because it holds a lot of water. "
                 "So A is true and R is false. Sphagnum also provides peat, used as fuel.",
                 ["A: true", "R: false, Sphagnum has a great capacity to hold water"],
                 ncert=ref("PK", "Bryophytes (mosses)"), secs=35)

statement_pair(T_PK, "Pteridophytes", "Intermediate",
               "In pteridophytes, the main plant body is a gametophyte.",
               "Pteridophytes are the first terrestrial plants to possess vascular tissues, xylem and phloem.",
               False, True, "D",
               "Pteridophytes",
               "In pteridophytes the main plant body is the sporophyte, differentiated into true root, stem and "
               "leaves. The gametophyte (prothallus) is small. They were the first land plants with xylem and phloem.",
               ["Statement I: false, the dominant body is the sporophyte", "Statement II: true"],
               ncert=ref("PK", "Pteridophytes"), secs=30)

assertion_reason(T_PK, "Pteridophytes", "Intermediate",
                 "The spread of living pteridophytes is limited to narrow geographical regions.",
                 "Their gametophytes need cool, damp, shady places to grow, and water is needed for fertilisation.",
                 True, True, True, "A",
                 "Distribution of pteridophytes",
                 "The prothallus needs cool, damp, shady places, and the male gametes need water to reach the "
                 "archegonium. NCERT states that because of this restricted requirement and the need for water, "
                 "living pteridophytes are restricted to narrow geographical regions. R explains A.",
                 ["A: true", "R: true", "NCERT gives R as the cause of A → R explains A"],
                 ncert=ref("PK", "Pteridophytes"), secs=40)

multi_statement(T_PK, "Gymnosperms", "Intermediate",
                "Which of the following statements about gymnosperms are correct?",
                [("Their ovules are not enclosed by any ovary wall.", True),
                 ("The roots of Pinus have a fungal association in the form of mycorrhiza.", True),
                 ("The needle-like leaves of conifers have a thick cuticle and sunken stomata.", True),
                 ("The stem of Cycas is profusely branched.", False)],
                [("a", "c", "d"), ("b", "c", "d"), ("a", "b", "c", "d")],
                "Gymnosperms",
                "Gymnosperms have naked ovules and seeds. Pinus roots have mycorrhiza. Conifer leaves are needle-like "
                "with a thick cuticle and sunken stomata, which reduce water loss. The stem of Cycas is unbranched; "
                "Pinus and Cedrus have branched stems.",
                ["(a) True", "(b) True", "(c) True", "(d) False: Cycas stem is unbranched"],
                ncert=ref("PK", "Gymnosperms"), secs=45)

match_list(T_PK, "Pteridophytes", "Advanced",
           "class of pteridophytes", "example",
           ["Psilopsida", "Lycopsida", "Sphenopsida", "Pteropsida"],
           ["Equisetum", "Psilotum", "Adiantum", "Selaginella"],
           {"A": "II", "B": "IV", "C": "I", "D": "III"},
           [{"A": "II", "B": "I", "C": "IV", "D": "III"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
            {"A": "II", "B": "IV", "C": "III", "D": "I"}],
           "Classes of pteridophytes",
           "Pteridophytes are classified into four classes: Psilopsida (Psilotum), Lycopsida (Selaginella, "
           "Lycopodium), Sphenopsida (Equisetum) and Pteropsida (Dryopteris, Pteris, Adiantum).",
           ["Psilopsida → Psilotum (II)", "Lycopsida → Selaginella (IV)", "Sphenopsida → Equisetum (I)",
            "Pteropsida → Adiantum (III)"],
           why="Equisetum (horsetail) is the sphenopsid; Adiantum is a fern (Pteropsida).",
           ncert=ref("PK", "Pteridophytes (classes)"), secs=45)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following statements about reproduction and structure in algae are correct?",
                [("Spirogyra shows fusion of non-flagellated gametes that are similar in size.", True),
                 ("Volvox and Fucus show fusion of a large, non-motile female gamete with a smaller, motile male "
                  "gamete.", True),
                 ("Some species of Eudorina show fusion of two gametes dissimilar in size.", True),
                 ("Members of Phaeophyceae have two equal, apical flagella.", False),
                 ("Members of Chlorophyceae store food as mannitol and laminarin.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "b", "c", "d")],
                "Sexual reproduction and features of algae",
                "Isogamy with non-flagellated gametes: Spirogyra. Anisogamy: some species of Eudorina. Oogamy (large "
                "static egg, small motile male gamete): Volvox, Fucus. Brown algae have two unequal, laterally "
                "attached flagella. Green algae store starch; mannitol and laminarin are the reserves of brown algae.",
                ["(a) True: isogamy", "(b) True: oogamy", "(c) True: anisogamy",
                 "(d) False: brown algae have 2 unequal lateral flagella",
                 "(e) False: mannitol and laminarin are brown-algal reserves"],
                why="(d) and (e) swap features between classes: 2–8 equal apical flagella and starch belong to green "
                    "algae; unequal lateral flagella and laminarin to brown algae.",
                ncert=ref("PK", "Algae (reproduction; table of algal classes)"), secs=70)

assertion_reason(T_PK, "Pteridophytes", "Advanced",
                 "Heterosporous pteridophytes such as Selaginella and Salvinia show an event considered a "
                 "precursor to the seed habit.",
                 "In them, the female gametophyte is retained on the parent sporophyte for a variable period, and "
                 "the zygote develops into a young embryo within the female gametophyte.",
                 True, True, True, "A",
                 "Heterospory and the seed habit",
                 "In heterosporous pteridophytes, megaspores and microspores give rise to female and male "
                 "gametophytes. The female gametophyte is retained on the parent sporophyte, and the zygote develops "
                 "into an embryo within it. NCERT calls this event a precursor to the seed habit. R describes that "
                 "event, so it explains A.",
                 ["A: true", "R: true", "The retention of the female gametophyte and development of the embryo "
                  "within it is the event called the precursor of the seed habit → R explains A"],
                 ncert=ref("PK", "Pteridophytes (heterospory)"), secs=50)

multi_statement(T_PK, "Bryophytes", "Advanced",
                "Which of the following statements about liverworts and mosses are correct?",
                [("The gametophyte of a moss has two stages: the protonema and the leafy stage.", True),
                 ("Gemmae are green, multicellular asexual buds formed in gemma cups on liverwort thalli.", True),
                 ("Mosses have an elaborate mechanism of spore dispersal.", True),
                 ("The leafy stage of mosses bears true leaves with vascular tissue.", False),
                 ("The sporophyte of mosses is more elaborate than that of liverworts.", True)],
                [("a", "b", "c", "d"), ("b", "c", "d", "e"), ("a", "c", "e")],
                "Liverworts and mosses",
                "Moss gametophyte: a creeping, green, branched filamentous protonema and an upright leafy stage. "
                "Liverworts like Marchantia reproduce asexually by gemmae from gemma cups. Bryophytes lack true roots, "
                "stem and leaves and have no vascular tissue. The moss sporophyte (foot, seta, capsule) is more "
                "elaborate than the liverwort sporophyte, and mosses have an elaborate spore-dispersal mechanism.",
                ["(a) True", "(b) True", "(c) True", "(d) False: bryophytes lack true leaves and vascular tissue",
                 "(e) True"],
                ncert=ref("PK", "Bryophytes (liverworts, mosses)"), secs=70)

statement_pair(T_PK, "Gymnosperms", "Advanced",
               "In gymnosperms, the male and female gametophytes do not have an independent free-living existence.",
               "In gymnosperms, pollen grains are carried to the ovules by water currents.",
               True, False, "C",
               "Reproduction in gymnosperms",
               "Gymnosperm gametophytes remain within the sporangia retained on the sporophyte. Pollen grains are "
               "released from microsporangia and carried by air currents to the opening of the ovules; the pollen "
               "tube carries the male gametes to the archegonia. Water is not needed.",
               ["Statement I: true", "Statement II: false, pollen is carried by air currents"],
               why="Dependence on water for fertilisation is a feature of bryophytes and pteridophytes, not "
                   "gymnosperms.",
               ncert=ref("PK", "Gymnosperms"), secs=40)

# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Root, stem and leaf", "Basic",
       "In Rhizophora growing in swampy areas, many roots come out of the ground and grow vertically upwards. "
       "These roots help the plant to:",
       "get oxygen for respiration", ["store food", "climb a support", "absorb water from the soil"],
       "Modifications of roots: pneumatophores",
       "Swampy soil is poor in oxygen. The upward-growing roots of Rhizophora, called pneumatophores, help the "
       "plant get oxygen for respiration.",
       ["Swampy soil → little oxygen", "Pneumatophores grow above ground → obtain oxygen for respiration"],
       why="Food storage is seen in carrot, turnip and sweet potato roots; support is given by prop and stilt roots.",
       ncert=ref("MOR", "The Root (modifications of root)"), secs=25)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "The tendrils of cucumber and pumpkin develop from:",
       "axillary buds", ["leaflets", "stipules", "adventitious roots"],
       "Modifications of stem: stem tendrils",
       "Stem tendrils develop from axillary buds. They are slender, spirally coiled and help gourds (cucumber, "
       "pumpkin, watermelon) and grapevines to climb.",
       ["Tendril position: in the axil of a leaf → axillary bud → stem tendril"],
       why="In pea, tendrils are modified leaves (leaflets), not stems.",
       ncert=ref("MOR", "The Stem (modifications of stem)"), secs=25)

direct(T_MOR, "Flower", "Basic",
       "Twisted aestivation, in which one margin of each petal overlaps the next one, is found in:",
       "China rose", ["Calotropis", "Cassia", "Pea"],
       "Aestivation",
       "In twisted aestivation one margin of each appendage overlaps the next one in a regular way, as in china "
       "rose, lady's finger and cotton.",
       ["China rose → twisted", "Calotropis → valvate", "Cassia → imbricate", "Pea → vexillary"],
       why="Calotropis has valvate aestivation (margins only touch), Cassia imbricate and pea vexillary.",
       ncert=ref("MOR", "The Flower (aestivation)"), secs=25)

direct(T_MOR, "Fruit and seed", "Basic",
       "In a mango fruit, the edible part is the:",
       "fleshy mesocarp", ["stony endocarp", "thin epicarp", "fibrous mesocarp"],
       "Drupe fruit",
       "Mango is a drupe. Its pericarp has a thin epicarp, a fleshy edible mesocarp and a stony hard endocarp.",
       ["Epicarp: thin", "Mesocarp: fleshy, edible", "Endocarp: stony"],
       why="A fibrous mesocarp is found in coconut, not mango.",
       ncert=ref("MOR", "The Fruit"), secs=25)

statement_pair(T_MOR, "Plant families", "Basic",
               "Solanaceae is commonly called the 'potato family'.",
               "Liliaceae is a family of dicotyledonous plants.",
               True, False, "C",
               "Plant families",
               "Solanaceae is the potato family. Liliaceae, the lily family, is a characteristic representative of "
               "monocotyledonous plants.",
               ["Statement I: true", "Statement II: false, Liliaceae is a monocot family"],
               ncert=ref("MOR", "Description of some important families"), secs=25)

match_list(T_MOR, "Root, stem and leaf", "Intermediate",
           "plant", "modification",
           ["Banyan", "Maize", "Pistia", "Opuntia"],
           ["Flattened green stem that carries out photosynthesis",
            "Supporting roots arising from the lower nodes of the stem",
            "Hanging roots from branches that support the tree",
            "Lateral branch with short internodes, each node bearing a rosette of leaves and a tuft of roots"],
           {"A": "III", "B": "II", "C": "IV", "D": "I"},
           [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
            {"A": "III", "B": "IV", "C": "II", "D": "I"}],
           "Modifications of root and stem",
           "Banyan has prop roots hanging from its branches. Maize and sugarcane have stilt roots from the lower "
           "nodes. Aquatic plants like Pistia and Eichhornia have lateral branches with short internodes, each node "
           "bearing a rosette of leaves and a tuft of roots. Opuntia has a flattened green photosynthetic stem.",
           ["Banyan → prop roots (III)", "Maize → stilt roots (II)", "Pistia → short-internode branch (IV)",
            "Opuntia → flattened stem (I)"],
           why="Prop roots (banyan) hang from branches; stilt roots (maize) arise from the lowest nodes. Mixing the "
               "two is the usual error.",
           ncert=ref("MOR", "The Root; The Stem (modifications)"), secs=50)

assertion_reason(T_MOR, "Inflorescence", "Intermediate",
                 "In a racemose inflorescence, the flowers are borne in basipetal succession.",
                 "In a racemose inflorescence, the main axis continues to grow.",
                 False, True, False, "D",
                 "Racemose and cymose inflorescences",
                 "In a racemose inflorescence the main axis keeps growing, so new flowers keep forming at the top: "
                 "the flowers are borne laterally in acropetal succession (older below, younger above). Basipetal "
                 "order is seen in cymose inflorescence, where the main axis ends in a flower.",
                 ["A: false, racemose = acropetal", "R: true, the main axis continues to grow"],
                 why="Basipetal order belongs to cymose inflorescence, where growth of the main axis is limited.",
                 ncert=ref("MOR", "Inflorescence"), secs=35)

multi_statement(T_MOR, "Root, stem and leaf", "Intermediate",
                "Which of the following statements about leaves are correct?",
                [("China rose, mustard and sunflower show alternate phyllotaxy.", True),
                 ("Calotropis and guava show opposite phyllotaxy.", True),
                 ("Alstonia shows whorled phyllotaxy.", True),
                 ("Neem has palmately compound leaves.", False),
                 ("Silk cotton has palmately compound leaves.", True)],
                [("a", "b", "c", "d"), ("a", "c", "d", "e"), ("b", "c", "e")],
                "Phyllotaxy and compound leaves",
                "Alternate: a single leaf at each node (china rose, mustard, sunflower). Opposite: a pair at each "
                "node (Calotropis, guava). Whorled: more than two at a node (Alstonia). Neem has pinnately compound "
                "leaves (leaflets on a common rachis); silk cotton has palmately compound leaves.",
                ["(a) True", "(b) True", "(c) True", "(d) False: neem is pinnately compound", "(e) True"],
                ncert=ref("MOR", "The Leaf (types of leaves, phyllotaxy)"), secs=55)

match_list(T_MOR, "Flower", "Intermediate",
           "type of placentation", "example",
           ["Marginal", "Parietal", "Free central", "Basal"],
           ["Dianthus", "Marigold", "Pea", "Argemone"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
            {"A": "III", "B": "IV", "C": "II", "D": "I"}],
           "Placentation",
           "Marginal: placenta along the ventral suture of a one-chambered ovary (pea). Parietal: ovules on the "
           "inner wall or periphery (mustard, Argemone). Free central: ovules on a central axis without septa "
           "(Dianthus, Primrose). Basal: a single ovule at the base (sunflower, marigold).",
           ["Marginal → pea (III)", "Parietal → Argemone (IV)", "Free central → Dianthus (I)",
            "Basal → marigold (II)"],
           why="Dianthus (free central) and Argemone (parietal) are the pair most often swapped.",
           ncert=ref("MOR", "The Flower (gynoecium, placentation)"), secs=45)

statement_pair(T_MOR, "Flower", "Intermediate",
               "In perigynous flowers such as plum, rose and peach, the ovary is said to be half inferior.",
               "In epigynous flowers such as guava and cucumber, the ovary is inferior.",
               True, True, "A",
               "Position of floral parts on the thalamus",
               "Hypogynous: ovary highest, superior (mustard, china rose, brinjal). Perigynous: other parts at about "
               "the level of the ovary, which is half inferior (plum, rose, peach). Epigynous: thalamus grows round "
               "the ovary and fuses with it, other parts above it, so the ovary is inferior (guava, cucumber, ray "
               "florets of sunflower).",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Flower (position of floral parts)"), secs=35)

direct(T_MOR, "Fruit and seed", "Intermediate",
       "In a maize grain, the proteinaceous layer that separates the endosperm from the embryo is the:",
       "aleurone layer", ["scutellum", "coleoptile", "coleorhiza"],
       "Structure of a monocot seed",
       "In maize, the outer covering of the bulky endosperm separates it from the embryo by a proteinous layer "
       "called the aleurone layer. The embryo has one large shield-shaped cotyledon (scutellum) and an axis with "
       "the plumule and radicle enclosed in sheaths: coleoptile and coleorhiza.",
       ["Aleurone layer: between endosperm and embryo", "Scutellum: the cotyledon",
        "Coleoptile / coleorhiza: sheaths of plumule / radicle"],
       why="The scutellum is the cotyledon; the coleoptile and coleorhiza are sheaths of the plumule and radicle.",
       ncert=ref("MOR", "The Seed (structure of a monocotyledonous seed)"), secs=30)

direct(T_MOR, "Plant families", "Intermediate",
       "The floral formula % ⚥ K(5) C1+2+(2) A(9)+1 G1 represents a flower of the family:",
       "Fabaceae", ["Solanaceae", "Liliaceae", "Poaceae"],
       "Reading a floral formula",
       "% = zygomorphic; C1+2+(2) = papilionaceous corolla (one standard, two wings, two fused keel petals); "
       "A(9)+1 = diadelphous stamens; G1 = monocarpellary ovary. These are the features of Fabaceae (e.g. pea).",
       ["% → zygomorphic flower", "C1+2+(2) → standard, wings, keel", "A(9)+1 → diadelphous", "G1 → monocarpellary"],
       why="Solanaceae is ⊕ K(5) C(5) A5 G(2); Liliaceae is ⊕ P(3+3) A3+3 G(3).",
       ncert=ref("MOR", "Description of some important families (Fabaceae)"), secs=40)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements about the family Solanaceae are correct?",
                [("The stamens are five and epipetalous.", True),
                 ("The ovary is bicarpellary, obliquely placed, syncarpous and superior, with axile placentation.",
                  True),
                 ("The corolla has five free petals with imbricate aestivation.", False),
                 ("The seeds are non-endospermous.", False),
                 ("Belladonna and ashwagandha are medicinal plants of this family.", True)],
                [("a", "b", "c"), ("a", "b", "d", "e"), ("b", "c", "e")],
                "Family Solanaceae",
                "Solanaceae: actinomorphic flowers; calyx of five united sepals, persistent, valvate; corolla of five "
                "united petals, valvate; five epipetalous stamens; bicarpellary, obliquely placed, syncarpous, "
                "superior, bilocular ovary with axile placentation; berry or capsule; seeds many and endospermous. "
                "Belladonna and ashwagandha are medicinal members.",
                ["(a) True", "(b) True", "(c) False: the corolla is united (gamopetalous), valvate",
                 "(d) False: seeds are endospermous", "(e) True"],
                ncert=ref("MOR", "Description of some important families (Solanaceae)"), secs=60)

match_list(T_MOR, "Plant families", "Advanced",
           "member of Fabaceae", "use",
           ["Indigofera", "Sunhemp", "Sesbania", "Muliathi"],
           ["Medicine", "Fodder", "Dye", "Fibre"],
           {"A": "III", "B": "IV", "C": "II", "D": "I"},
           [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
            {"A": "III", "B": "IV", "C": "I", "D": "II"}],
           "Economic importance of Fabaceae",
           "NCERT lists Fabaceae plants as sources of pulses, edible oil, dye (Indigofera), fibres (sunhemp), "
           "fodder (Sesbania, Trifolium), ornamentals (lupin, sweet pea) and medicine (muliathi).",
           ["Indigofera → dye (III)", "Sunhemp → fibre (IV)", "Sesbania → fodder (II)", "Muliathi → medicine (I)"],
           ncert=ref("MOR", "Description of some important families (Fabaceae, economic importance)"), secs=45)

assertion_reason(T_MOR, "Plant families", "Advanced",
                 "The floral formula of Liliaceae shows P(3+3) in place of separate K and C.",
                 "In Liliaceae the calyx and corolla are not distinct, so they are together termed the perianth "
                 "(tepals).",
                 True, True, True, "A",
                 "Perianth in Liliaceae",
                 "When calyx and corolla are not distinct, they are called the perianth, as in lily. Liliaceae has six "
                 "tepals in two whorls of three, often united into a tube, written P(3+3). R is exactly why the "
                 "formula uses P.",
                 ["A: Br ⊕ ⚥ P(3+3) A3+3 G(3) → true", "R: tepals = undifferentiated calyx and corolla → true",
                  "Undistinguished calyx and corolla are written as P → R explains A"],
                 ncert=ref("MOR", "The Flower (perianth); Description of some important families (Liliaceae)"),
                 secs=40)

statement_pair(T_MOR, "Fruit and seed", "Advanced",
               "All monocotyledonous seeds are endospermic.",
               "In bean, gram and pea, the endosperm persists in the mature seed.",
               False, False, "B",
               "Endospermic and non-endospermic seeds",
               "Monocot seeds are generally endospermic, but some, as in orchids, are non-endospermic, so 'all' makes "
               "Statement I false. In bean, gram and pea the endosperm is not present in the mature seed "
               "(non-endospermous seeds), so Statement II is false.",
               ["Statement I: false (orchid seeds are non-endospermic)",
                "Statement II: false (bean, gram, pea are non-endospermous)"],
               why="Statement I is a trap based on the word 'all': NCERT says 'generally', and names orchids as the "
                   "exception.",
               ncert=ref("MOR", "The Seed"), secs=40)

multi_statement(T_MOR, "Flower", "Advanced",
                "Which of the following statements about flowers are correct?",
                [("Stamens attached to the perianth, as in lily, are called epiphyllous.", True),
                 ("The stamens of china rose are united into one bundle (monoadelphous).", True),
                 ("In Cassia and gulmohur, the margins of the petals overlap one another, but not in any particular "
                  "direction.", True),
                 ("Citrus has polyadelphous stamens.", True),
                 ("Brinjal has epiphyllous stamens.", False)],
                [("a", "b", "d", "e"), ("b", "c", "d", "e"), ("a", "c", "e")],
                "Androecium and aestivation",
                "Stamens attached to petals are epipetalous (brinjal); attached to the perianth, epiphyllous (lily). "
                "Stamens may be united in one bundle (monoadelphous, china rose), two bundles (diadelphous, pea) or "
                "more than two bundles (polyadelphous, citrus). Imbricate aestivation: margins overlap but not in a "
                "particular direction (Cassia, gulmohur).",
                ["(a) True", "(b) True", "(c) True: imbricate aestivation", "(d) True",
                 "(e) False: brinjal stamens are epipetalous"],
                ncert=ref("MOR", "The Flower (aestivation, androecium)"), secs=60)

# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
direct(T_ANA, "Plant tissues", "Basic",
       "Grasses regenerate the parts removed by grazing herbivores mainly through the activity of:",
       "intercalary meristems", ["root apical meristem", "cork cambium", "vascular cambium"],
       "Meristems",
       "Intercalary meristems occur between mature tissues. They are found in grasses and regenerate parts removed "
       "by grazing herbivores.",
       ["Meristem between mature tissues → intercalary", "Found in grasses → regrowth after grazing"],
       why="The root apical meristem adds to root length; cork cambium and vascular cambium are lateral "
           "meristems, not meristems lying between mature tissues.",
       ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=25)

direct(T_ANA, "Tissue systems", "Basic",
       "In grasses, the guard cells of the stomata are:",
       "dumb-bell shaped", ["bean shaped", "spherical", "absent"],
       "Stomata",
       "Each stoma has two guard cells. Guard cells are generally bean-shaped; in grasses they are dumb-bell "
       "shaped. The outer walls are thin and the inner walls (towards the pore) highly thickened.",
       ["Grasses → dumb-bell shaped guard cells", "Generally → bean-shaped guard cells"],
       why="Bean-shaped guard cells are the general type, not the grass type. Guard cells are present in grasses.",
       ncert=ref("ANA", "The Tissue System (epidermal tissue system)"), secs=25)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "The Casparian strips of the endodermis of a root are made of:",
       "suberin", ["lignin", "cutin", "pectin"],
       "Endodermis of the root",
       "The tangential and radial walls of root endodermal cells have water-impermeable, waxy suberin deposited as "
       "Casparian strips.",
       ["Endodermis: innermost layer of the cortex", "Casparian strips: suberin on radial and tangential walls"],
       why="Lignin thickens xylem walls, cutin forms the cuticle and pectin thickens collenchyma.",
       ncert=ref("ANA", "Anatomy of dicotyledonous and monocotyledonous plants (dicot root)"), secs=25)

statement_pair(T_ANA, "Plant tissues", "Basic",
               "Vessels are absent from the xylem of gymnosperms.",
               "Gymnosperms have albuminous cells and sieve cells instead of companion cells and sieve tubes.",
               True, True, "A",
               "Xylem and phloem of gymnosperms",
               "Vessels are a characteristic feature of angiosperms; gymnosperms lack them. Gymnosperm phloem lacks "
               "sieve tubes and companion cells; it has sieve cells and albuminous cells.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (xylem, phloem)"), secs=30)

match_list(T_ANA, "Plant tissues", "Intermediate",
           "tissue or cell", "feature",
           ["Collenchyma", "Sclereids", "Companion cells", "Phloem fibres"],
           ["Commercial fibres of jute, flax and hemp",
            "Their nucleus controls the functions of sieve tubes",
            "Walls thickened at the corners with cellulose, hemicellulose and pectin",
            "Found in the pulp of guava, pear and sapota"],
           {"A": "III", "B": "IV", "C": "II", "D": "I"},
           [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
            {"A": "III", "B": "I", "C": "II", "D": "IV"}],
           "Simple and complex permanent tissues",
           "Collenchyma has corner thickenings of cellulose, hemicellulose and pectin. Sclereids occur in the fruit "
           "walls of nuts, the pulp of guava, pear and sapota, seed coats of legumes and tea leaves. The nucleus of "
           "the companion cell controls the sieve tube. Phloem (bast) fibres of jute, flax and hemp are used "
           "commercially.",
           ["Collenchyma → III", "Sclereids → IV", "Companion cells → II", "Phloem fibres → I"],
           why="Sclereids and phloem fibres are both sclerenchyma, but only phloem fibres give commercial fibres.",
           ncert=ref("ANA", "The Tissues (permanent tissues)"), secs=45)

assertion_reason(T_ANA, "Tissue systems", "Intermediate",
                 "Grass leaves curl inwards when water is scarce.",
                 "Bulliform cells in the adaxial epidermis of grass leaves become flaccid when they lose water.",
                 True, True, True, "A",
                 "Bulliform cells",
                 "Some adaxial epidermal cells along the veins of grass leaves are large, empty and colourless "
                 "(bulliform cells). When turgid, they keep the leaf surface exposed; when flaccid under water stress, "
                 "they make the leaf curl inwards to reduce water loss. R explains A.",
                 ["A: true", "R: true", "Flaccid bulliform cells cause the inward curling → R explains A"],
                 ncert=ref("ANA", "Anatomy of dicotyledonous and monocotyledonous plants (monocot leaf)"), secs=40)

multi_statement(T_ANA, "Plant tissues", "Intermediate",
                "Which of the following statements about xylem are correct?",
                [("In stems, the protoxylem lies towards the centre and the metaxylem towards the periphery.", True),
                 ("In roots, the protoxylem lies towards the periphery and the metaxylem towards the centre.", True),
                 ("Vessels are a characteristic feature of angiosperms.", True),
                 ("Tracheids are living, thin-walled cells.", False)],
                [("a", "b", "d"), ("b", "c", "d"), ("a", "b", "c", "d")],
                "Xylem: elements and arrangement",
                "Endarch xylem (stems): protoxylem towards the centre. Exarch xylem (roots): protoxylem towards the "
                "periphery. Vessels are characteristic of angiosperms. Tracheids are dead, elongated cells with thick, "
                "lignified walls and tapering ends.",
                ["(a) True: endarch", "(b) True: exarch", "(c) True",
                 "(d) False: tracheids are dead with lignified walls"],
                ncert=ref("ANA", "The Tissues (xylem)"), secs=45)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "A monocot root usually has more than six xylem bundles (polyarch).",
               "In a monocot root, the pith is small or inconspicuous.",
               True, False, "C",
               "Monocot root",
               "A monocot root resembles a dicot root but usually has more than six xylem bundles (polyarch), while a "
               "dicot root has two to four. The pith of a monocot root is large and well developed; in a dicot root "
               "it is small or inconspicuous.",
               ["Statement I: true", "Statement II: false, the pith is large and well developed"],
               why="Statement II describes the dicot root.",
               ncert=ref("ANA", "Anatomy of dicotyledonous and monocotyledonous plants (monocot root)"), secs=35)

direct(T_ANA, "Tissue systems", "Intermediate",
       "Which of the following statements about trichomes in the shoot system is correct?",
       "They help in preventing water loss due to transpiration.",
       ["They are always unicellular.", "They are elongations of root epidermal cells.", "They are never secretory."],
       "Epidermal appendages",
       "Root hairs are unicellular elongations of root epidermal cells. Trichomes on the shoot are usually "
       "multicellular, branched or unbranched, soft or stiff, and may be secretory. They help prevent water loss "
       "due to transpiration.",
       ["Shoot trichomes: usually multicellular, may be secretory", "Function: reduce water loss"],
       why="Unicellular elongations of root epidermis are root hairs. Trichomes are usually multicellular and can "
           "be secretory.",
       ncert=ref("ANA", "The Tissue System (epidermal tissue system)"), secs=30)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "Which of the following are features of a monocot stem?",
                [("A sclerenchymatous hypodermis.", True),
                 ("Conjoint, closed vascular bundles, each surrounded by a sclerenchymatous bundle sheath.", True),
                 ("Absence of phloem parenchyma.", True),
                 ("Vascular bundles arranged in a ring.", False),
                 ("Water-containing cavities within the vascular bundles.", True)],
                [("a", "b", "c", "d"), ("b", "c", "d", "e"), ("a", "b", "e")],
                "Monocot stem anatomy",
                "A monocot stem has a sclerenchymatous hypodermis and many scattered vascular bundles, each with a "
                "sclerenchymatous bundle sheath. The bundles are conjoint and closed, the peripheral ones smaller. "
                "Phloem parenchyma is absent and water-containing cavities are present in the bundles. A ring of "
                "bundles is a dicot stem feature.",
                ["(a) True", "(b) True", "(c) True", "(d) False: bundles are scattered", "(e) True"],
                ncert=ref("ANA", "Anatomy of dicotyledonous and monocotyledonous plants (monocot stem)"), secs=60)

match_list(T_ANA, "Dicot and monocot anatomy", "Advanced",
           "anatomical feature", "organ",
           ["Endodermis rich in starch grains (starch sheath)", "Mesophyll differentiated into palisade and spongy "
            "parenchyma", "Two to four xylem patches", "Undifferentiated mesophyll with stomata on both surfaces"],
           ["Dicot root", "Isobilateral leaf", "Dicot stem", "Dorsiventral leaf"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
            {"A": "III", "B": "IV", "C": "II", "D": "I"}],
           "Identifying organs by internal structure",
           "In a dicot stem, the endodermis is rich in starch grains and called the starch sheath. A dorsiventral "
           "(dicot) leaf has palisade and spongy mesophyll. A dicot root usually has two to four xylem and phloem "
           "patches. An isobilateral (monocot) leaf has stomata on both surfaces and undifferentiated mesophyll.",
           ["Starch sheath → dicot stem (III)", "Palisade + spongy → dorsiventral leaf (IV)",
            "2–4 xylem patches → dicot root (I)", "Undifferentiated mesophyll → isobilateral leaf (II)"],
           why="The root endodermis has Casparian strips; the starch sheath is the endodermis of the dicot stem.",
           ncert=ref("ANA", "Anatomy of dicotyledonous and monocotyledonous plants"), secs=55)

assertion_reason(T_ANA, "Tissue systems", "Advanced",
                 "The vascular bundles of roots are of the radial type.",
                 "In roots, the xylem and phloem are arranged on the same radius.",
                 True, False, False, "C",
                 "Types of vascular bundles",
                 "In roots, xylem and phloem lie in an alternate manner on different radii; this arrangement is called "
                 "radial. In conjoint bundles (stems, leaves) xylem and phloem lie together on the same radius. So A is "
                 "true and R is false.",
                 ["A: true", "R: false, the same-radius arrangement defines conjoint bundles"],
                 why="R describes conjoint vascular bundles, the opposite of radial.",
                 ncert=ref("ANA", "The Tissue System (vascular tissue system)"), secs=40)

statement_pair(T_ANA, "Plant tissues", "Advanced",
               "A mature sieve tube element retains a large nucleus that controls its functions.",
               "Phloem parenchyma is absent in most monocotyledons.",
               False, True, "D",
               "Phloem elements",
               "A mature sieve element has peripheral cytoplasm and a large vacuole but lacks a nucleus; its functions "
               "are controlled by the nucleus of the companion cell. Phloem parenchyma is absent in most monocots.",
               ["Statement I: false, a mature sieve element lacks a nucleus", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (phloem)"), secs=40)

# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Cell theory", "Basic",
       "Who explained that new cells are formed from pre-existing cells (Omnis cellula-e cellula)?",
       "Rudolf Virchow", ["Matthias Schleiden", "Theodore Schwann", "Robert Brown"],
       "Cell theory",
       "Schleiden (1838) and Schwann (1839) together formulated the cell theory, but it did not explain how new "
       "cells form. Rudolf Virchow (1855) first explained that cells divide and new cells form from pre-existing "
       "cells, and he modified the hypothesis into the final form of the cell theory.",
       ["Schleiden: all plants are made of cells", "Schwann: animals; plasma membrane; cell wall unique to plants",
        "Virchow (1855): Omnis cellula-e cellula"],
       why="Schleiden and Schwann proposed the cell theory without explaining the origin of new cells; Robert "
           "Brown discovered the nucleus.",
       ncert=ref("CELL", "Cell Theory"), secs=25)

direct(T_CELL, "Endomembrane system", "Basic",
       "Which of the following is NOT a part of the endomembrane system?",
       "Peroxisome", ["Golgi complex", "Lysosome", "Vacuole"],
       "The endomembrane system",
       "The endoplasmic reticulum, Golgi complex, lysosomes and vacuoles work in coordination and form the "
       "endomembrane system. Mitochondria, chloroplasts and peroxisomes are not included because their functions "
       "are not coordinated with these components.",
       ["Endomembrane system = ER + Golgi complex + lysosomes + vacuoles",
        "Peroxisomes, mitochondria, chloroplasts are excluded"],
       ncert=ref("CELL", "Endomembrane System"), secs=25)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In which cell organelle is the inner membrane folded into infoldings called cristae?",
       "Mitochondrion", ["Chloroplast", "Golgi apparatus", "Nucleus"],
       "Structure of mitochondria",
       "A mitochondrion has two membranes. The inner membrane forms infoldings called cristae towards the matrix, "
       "which increase its surface area.",
       ["Outer membrane: continuous limiting boundary", "Inner membrane: folded into cristae"],
       why="Chloroplasts have flattened thylakoids stacked as grana, not cristae.",
       ncert=ref("CELL", "Mitochondria"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "The material of the nucleus that stains with basic dyes was named chromatin by:",
       "Flemming", ["Robert Brown", "Camillo Golgi", "George Palade"],
       "History of the nucleus",
       "Robert Brown described the nucleus as a cell organelle (1831). Later, the nuclear material stained by "
       "basic dyes was named chromatin by Flemming.",
       ["Nucleus described: Robert Brown", "Chromatin named: Flemming"],
       why="Golgi discovered the Golgi apparatus; Palade observed ribosomes as dense particles.",
       ncert=ref("CELL", "Nucleus"), secs=25)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Basic",
               "The axoneme of cilia and flagella has a 9 + 2 arrangement of microtubules.",
               "Each of the nine peripheral fibrils of a centriole is a doublet of microtubules.",
               True, False, "C",
               "Cilia, flagella and centrioles",
               "The axoneme has nine doublets of radially arranged peripheral microtubules and a pair of central "
               "microtubules (9 + 2). A centriole has a cartwheel organisation of nine evenly spaced peripheral "
               "fibrils of tubulin, each a triplet.",
               ["Statement I: true", "Statement II: false, centriole fibrils are triplets"],
               why="Doublets belong to the axoneme; centriole fibrils are triplets.",
               ncert=ref("CELL", "Cilia and Flagella; Centrosome and Centrioles"), secs=30)

match_list(T_CELL, "Prokaryotic cell", "Intermediate",
           "structure in a prokaryotic cell", "feature",
           ["Mesosome", "Plasmid", "Fimbriae", "Chromatophores"],
           ["Membranous extensions containing pigments, as in cyanobacteria",
            "Small circular DNA that can confer antibiotic resistance",
            "Infolding of the plasma membrane that helps in cell wall formation and DNA replication",
            "Small bristle-like fibres that help the cell attach to rocks in streams and to host tissues"],
           {"A": "III", "B": "II", "C": "IV", "D": "I"},
           [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "II", "B": "III", "C": "IV", "D": "I"}],
           "Structures of the prokaryotic cell",
           "Mesosomes are infoldings of the plasma membrane (vesicles, tubules, lamellae) that help in cell wall "
           "formation, DNA replication and distribution, respiration and secretion. Plasmids are small circular "
           "extra-chromosomal DNA that can give antibiotic resistance. Fimbriae help attachment. Chromatophores are "
           "pigment-containing membranous extensions in cyanobacteria.",
           ["Mesosome → III", "Plasmid → II", "Fimbriae → IV", "Chromatophores → I"],
           why="Mesosomes and chromatophores are both membranous extensions, but only chromatophores carry pigments.",
           ncert=ref("CELL", "Prokaryotic Cells"), secs=45)

assertion_reason(T_CELL, "Cell envelope and membrane", "Intermediate",
                 "Proteins can move laterally within the plasma membrane.",
                 "The lipid bilayer of the plasma membrane is quasi-fluid in nature.",
                 True, True, True, "A",
                 "Fluid mosaic model",
                 "In the fluid mosaic model (Singer and Nicolson), the quasi-fluid nature of the lipid bilayer lets "
                 "proteins move laterally within it. This fluidity is important for cell growth, intercellular "
                 "junctions, secretion, endocytosis and cell division. R is the reason for A.",
                 ["A: lateral movement of proteins → true", "R: quasi-fluid lipid → true",
                  "Fluid lipid layer allows the movement → R explains A"],
                 ncert=ref("CELL", "Cell Membrane"), secs=35)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "The middle lamella, which holds neighbouring plant cells together, is mainly made of calcium pectate.",
               "The secondary wall of a plant cell is formed on the outer side of the primary wall.",
               True, False, "C",
               "Plant cell wall",
               "The middle lamella is a layer mainly of calcium pectate that glues neighbouring cells together. The "
               "primary wall of a young cell can grow; it diminishes as the cell matures, and the secondary wall is "
               "formed on the inner side of the cell (towards the membrane).",
               ["Statement I: true", "Statement II: false, the secondary wall forms on the inner side"],
               ncert=ref("CELL", "Cell Wall"), secs=35)

multi_statement(T_CELL, "Endomembrane system", "Intermediate",
                "Which of the following statements about the Golgi apparatus and lysosomes are correct?",
                [("The cis face of the Golgi apparatus is the forming face and the trans face is the maturing face.",
                  True),
                 ("The Golgi apparatus is the important site of formation of glycoproteins and glycolipids.", True),
                 ("Lysosomal enzymes are optimally active at alkaline pH.", False),
                 ("Lysosomes are formed by the process of packaging in the Golgi apparatus.", True),
                 ("The Golgi apparatus was first observed by Robert Brown.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "c", "d", "e")],
                "Golgi apparatus and lysosomes",
                "Camillo Golgi (1898) first observed the Golgi apparatus. Its cis (forming) and trans (maturing) faces "
                "are interconnected. It packages materials and is the important site of formation of glycoproteins "
                "and glycolipids. Lysosomes are vesicles formed by packaging in the Golgi; their hydrolytic enzymes "
                "(lipases, proteases, carbohydrases) are optimally active at acidic pH.",
                ["(a) True", "(b) True", "(c) False: acidic pH", "(d) True", "(e) False: Camillo Golgi"],
                ncert=ref("CELL", "Endomembrane System (Golgi apparatus, lysosomes)"), secs=55)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
       "In the term '80S ribosome', the sedimentation coefficient indirectly indicates the ribosome's:",
       "density and size",
       ["number of RNA molecules", "number of protein molecules", "rate of protein synthesis"],
       "Ribosome nomenclature",
       "'S' (Svedberg unit) stands for the sedimentation coefficient. It is an indirect measure of density and "
       "size. Eukaryotic ribosomes are 80S (60S + 40S); prokaryotic ribosomes are 70S (50S + 30S).",
       ["S = sedimentation coefficient", "It indirectly measures density and size"],
       why="S values are not counts of molecules, and they do not measure activity. That is also why 60S + 40S "
           "gives 80S, not 100S.",
       ncert=ref("CELL", "Ribosomes"), secs=30)

assertion_reason(T_CELL, "Nucleus", "Intermediate",
                 "Larger and more numerous nucleoli are present in cells that are actively carrying out protein "
                 "synthesis.",
                 "The nucleolus is not a membrane-bound structure; its content is continuous with the rest of the "
                 "nucleoplasm.",
                 True, True, False, "B",
                 "Nucleolus",
                 "The nucleolus is the site of active ribosomal RNA synthesis, so cells making a lot of protein have "
                 "larger and more numerous nucleoli. It is not membrane-bound, so its content is continuous with the "
                 "nucleoplasm. Both statements are true, but the lack of a membrane does not explain A; rRNA "
                 "synthesis does.",
                 ["A: true", "R: true", "The explanation of A is rRNA synthesis for ribosomes, not the absence of a "
                  "membrane → R does not explain A"],
                 why="Option A is the trap; R is a true but unrelated structural fact.",
                 ncert=ref("CELL", "Nucleus (nucleolus)"), secs=45)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                "Which of the following statements about plastids are correct?",
                [("Chromoplasts contain fat-soluble carotenoid pigments such as carotene and xanthophylls.", True),
                 ("Amyloplasts store carbohydrates (starch), as in potato.", True),
                 ("Aleuroplasts store oils and fats.", False),
                 ("The stroma of a chloroplast contains small, double-stranded circular DNA and 70S ribosomes.",
                  True)],
                [("a", "c", "d"), ("b", "c"), ("a", "b", "c", "d")],
                "Plastids",
                "Chromoplasts give yellow, orange or red colours (carotenoids). Leucoplasts are colourless storage "
                "plastids: amyloplasts store starch (potato), elaioplasts store oils and fats, aleuroplasts store "
                "proteins. The chloroplast stroma has small circular dsDNA and 70S ribosomes.",
                ["(a) True", "(b) True", "(c) False: aleuroplasts store proteins; elaioplasts store oils and fats",
                 "(d) True"],
                ncert=ref("CELL", "Plastids"), secs=45)

match_list(T_CELL, "Nucleus", "Advanced",
           "type of chromosome", "position of the centromere",
           ["Metacentric", "Sub-metacentric", "Acrocentric", "Telocentric"],
           ["At the tip (terminal)", "Close to one end, giving one extremely short and one very long arm",
            "In the middle, giving two equal arms", "Slightly away from the middle, giving one shorter and one "
            "longer arm"],
           {"A": "III", "B": "IV", "C": "II", "D": "I"},
           [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
            {"A": "III", "B": "IV", "C": "I", "D": "II"}],
           "Classification of chromosomes by centromere position",
           "Metacentric: centromere in the middle, two equal arms. Sub-metacentric: slightly away from the middle, "
           "one shorter and one longer arm. Acrocentric: close to the end, one extremely short and one very long arm. "
           "Telocentric: terminal centromere.",
           ["Metacentric → III", "Sub-metacentric → IV", "Acrocentric → II", "Telocentric → I"],
           why="Acrocentric (near the end) and telocentric (at the end) are the pair most often confused.",
           ncert=ref("CELL", "Nucleus (chromosomes)"), secs=45)

multi_statement(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
                "Which of the following statements about cilia, flagella and centrioles are correct?",
                [("The central microtubules of the axoneme are connected by bridges and enclosed by a central sheath.",
                  True),
                 ("The central sheath is connected to one of the tubules of each peripheral doublet by a radial "
                  "spoke.", True),
                 ("Cilia and flagella emerge from centriole-like structures called basal bodies.", True),
                 ("The two centrioles of a centrosome lie parallel to each other.", False)],
                [("a", "b", "d"), ("b", "c", "d"), ("a", "b", "c", "d")],
                "Ultrastructure of cilia and centrioles",
                "In the axoneme the two central microtubules are joined by bridges and enclosed by a central sheath, "
                "which is linked to one tubule of each peripheral doublet by radial spokes. Cilia and flagella arise "
                "from basal bodies. The centrosome has two cylindrical centrioles lying perpendicular to each other.",
                ["(a) True", "(b) True", "(c) True", "(d) False: the centrioles lie perpendicular"],
                ncert=ref("CELL", "Cilia and Flagella; Centrosome and Centrioles"), secs=55)

assertion_reason(T_CELL, "Cell envelope and membrane", "Advanced",
                 "Lipids make up about 52 per cent of the membrane of human erythrocytes.",
                 "The fluid mosaic model of the cell membrane was proposed by Singer and Nicolson in 1972.",
                 False, True, False, "D",
                 "Composition of the plasma membrane",
                 "Biochemical study of the human RBC membrane shows about 52 per cent protein and 40 per cent lipids. "
                 "So A, which gives 52 per cent to lipids, is false. R is true: Singer and Nicolson proposed the fluid "
                 "mosaic model in 1972.",
                 ["RBC membrane: ~52% protein, ~40% lipid → A false", "Fluid mosaic model: Singer and Nicolson, 1972 → "
                  "R true"],
                 why="The trap is the swapped percentages; protein, not lipid, is about 52 per cent.",
                 ncert=ref("CELL", "Cell Membrane"), secs=40)

multi_statement(T_CELL, "Endomembrane system", "Advanced",
                "Which of the following statements are correct?",
                [("In plant cells, vacuoles can occupy up to 90 per cent of the volume of the cell.", True),
                 ("Because the tonoplast transports ions against concentration gradients, their concentration is "
                  "much higher in the vacuole than in the cytoplasm.", True),
                 ("In Amoeba, the contractile vacuole is important for osmoregulation and excretion.", True),
                 ("The smooth endoplasmic reticulum is the major site of protein synthesis.", False),
                 ("In animal cells, lipid-like steroidal hormones are synthesised in the smooth endoplasmic "
                  "reticulum.", True)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")],
                "Vacuoles and endoplasmic reticulum",
                "The plant vacuole can fill up to 90 per cent of the cell; the tonoplast pumps ions into it against "
                "the gradient. The contractile vacuole of Amoeba helps in osmoregulation and excretion. Rough ER, "
                "with ribosomes, is active in protein synthesis and secretion; smooth ER is the major site of lipid "
                "synthesis, including steroidal hormones in animal cells.",
                ["(a) True", "(b) True", "(c) True", "(d) False: RER makes proteins; SER makes lipids", "(e) True"],
                ncert=ref("CELL", "Endomembrane System (ER, vacuoles)"), secs=60)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "Prokaryotic ribosomes are of the 80S type, made of 60S and 40S subunits.",
               "Reserve material in prokaryotic cells is stored in inclusion bodies bounded by a single membrane.",
               False, False, "B",
               "Ribosomes and inclusion bodies of prokaryotes",
               "Prokaryotic ribosomes are 70S, made of 50S and 30S subunits; 80S (60S + 40S) ribosomes are "
               "eukaryotic. Inclusion bodies (phosphate granules, cyanophycean granules, glycogen granules) are not "
               "bounded by any membrane and lie free in the cytoplasm.",
               ["Statement I: false, 70S (50S + 30S)", "Statement II: false, inclusion bodies have no membrane"],
               ncert=ref("CELL", "Prokaryotic Cells (ribosomes and inclusion bodies)"), secs=40)

# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "Which change takes place during the S phase of the cell cycle?",
       "The amount of DNA doubles, but the number of chromosomes stays the same.",
       ["The number of chromosomes doubles, but the amount of DNA stays the same.",
        "Both the amount of DNA and the number of chromosomes double.",
        "Both the amount of DNA and the number of chromosomes are halved."],
       "Synthesis (S) phase",
       "DNA replicates during the S phase. If the initial amount of DNA is 2C, it becomes 4C. Each chromosome now "
       "has two chromatids joined at the centromere, so the chromosome number is unchanged (a 2n cell stays 2n).",
       ["DNA: 2C → 4C", "Chromosome number: 2n → 2n (each chromosome now has two chromatids)"],
       why="Chromosome number doubles only briefly at anaphase, when sister chromatids separate; it is halved by "
           "meiosis I.",
       ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=25)

direct(T_CC, "Mitosis", "Basic",
       "The morphology of chromosomes is most easily studied at which stage of mitosis?",
       "Metaphase", ["Prophase", "Anaphase", "Telophase"],
       "Metaphase",
       "By metaphase, condensation of chromosomes is complete and they line up at the metaphase plate. They can be "
       "observed clearly under the microscope, so this is the stage at which their morphology is most easily "
       "studied.",
       ["Condensation complete", "Chromosomes aligned at the metaphase plate"],
       why="In prophase condensation is incomplete, in anaphase the chromatids are moving apart, and in telophase "
           "the chromosomes decondense.",
       ncert=ref("CC", "M Phase (metaphase)"), secs=20)

# 128 cells from one cell by synchronous mitosis: 2**n = 128
ROUNDS = next(n for n in range(1, 20) if 2 ** n == 128)
assert ROUNDS == 7 and 128 - 1 == 127
numerical(T_CC, "Mitosis", "Basic",
          "A single cell divides repeatedly by mitosis, and in every round each cell divides once. How many rounds "
          "of division are needed to produce 128 cells?",
          ["6", "7", "64", "127"], "B", ROUNDS == 7,
          "Mitosis doubles the number of cells",
          "Each mitotic division gives two daughter cells, so the cell number doubles in every round: after n rounds "
          "there are 2ⁿ cells.",
          ["2ⁿ = 128", "128 = 2⁷", "n = 7 rounds"],
          why="6 rounds give only 64 cells; 64 is half the number of cells, not the number of rounds. 127 is the "
              "total number of individual division events (1 + 2 + 4 + ... + 64), not the number of rounds.",
          ncert=ref("CC", "M Phase; Significance of Mitosis"), secs=40)

statement_pair(T_CC, "Significance", "Basic",
               "Mitosis results in diploid daughter cells with an identical genetic complement.",
               "Meiosis increases the genetic variability in the population of organisms from one generation to the "
               "next.",
               True, True, "A",
               "Significance of mitosis and meiosis",
               "Mitosis is an equational division: daughter cells have the same chromosome number and genetic "
               "complement as the parent. Meiosis conserves the chromosome number across sexually reproducing "
               "generations and increases genetic variability, which is important for evolution.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Significance of Mitosis; Significance of Meiosis"), secs=25)

match_list(T_CC, "Meiosis", "Intermediate",
           "stage of prophase I", "event",
           ["Leptotene", "Zygotene", "Pachytene", "Diplotene"],
           ["Crossing over between non-sister chromatids of homologous chromosomes",
            "Dissolution of the synaptonemal complex; chiasmata become visible",
            "Chromosomes become gradually visible under the light microscope",
            "Synapsis of homologous chromosomes with formation of the synaptonemal complex"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "III", "B": "I", "C": "IV", "D": "II"}],
           "Sub-stages of prophase I",
           "Leptotene: chromosomes become visible as compaction continues. Zygotene: homologues pair (synapsis) "
           "with a synaptonemal complex, forming bivalents. Pachytene: crossing over. Diplotene: the synaptonemal "
           "complex dissolves and the homologues separate except at chiasmata.",
           ["Leptotene → III", "Zygotene → IV", "Pachytene → I", "Diplotene → II"],
           why="Crossing over happens in pachytene; chiasmata, its visible sign, appear in diplotene.",
           ncert=ref("CC", "Meiosis (prophase I)"), secs=45)

# DNA content: G1 = 2C = 20 pg; after S = 4C; after meiosis I each cell = 2C; after meiosis II = 1C
G1_PG = 20
AFTER_S = 2 * G1_PG
AFTER_M1 = AFTER_S // 2
AFTER_M2 = AFTER_M1 // 2
assert (AFTER_S, AFTER_M1, AFTER_M2) == (40, 20, 10)
numerical(T_CC, "Meiosis", "Intermediate",
          "A diploid cell in G1 phase contains 20 pg of DNA. It enters meiosis. How much DNA will each cell have "
          "at the end of meiosis I (before meiosis II begins)? There is no DNA replication during interkinesis.",
          ["5 pg", "10 pg", "20 pg", "40 pg"], "C", AFTER_M1 == 20,
          "DNA content through meiosis",
          "DNA doubles in the S phase before meiosis. Meiosis I separates homologous chromosomes into two cells, "
          "halving the DNA. Interkinesis has no DNA replication, and meiosis II halves it again.",
          ["G1: 2C = 20 pg", "After S phase: 4C = 40 pg", "After meiosis I: each cell 2C = 20 pg",
           "(After meiosis II: each cell 1C = 10 pg)"],
          why="10 pg is the content after meiosis II; 40 pg is the content after S phase (G2); 5 pg halves too "
              "many times.",
          ncert=ref("CC", "Cell Cycle (S phase); Meiosis"), secs=60,
          short="Meiosis I starts at 4C and ends at 2C: the G1 value again.")

assertion_reason(T_CC, "Cell cycle phases", "Intermediate",
                 "Cells in the quiescent stage (G0) are metabolically inactive.",
                 "Cells in G0 do not proliferate unless called on to do so, depending on the requirement of the "
                 "organism.",
                 False, True, False, "D",
                 "Quiescent stage (G0)",
                 "Some cells, such as heart cells in adult animals, do not divide further; others divide only "
                 "occasionally. Cells that do not divide further exit G1 and enter G0. NCERT states that cells in "
                 "this stage remain metabolically active but no longer proliferate unless called on to do so.",
                 ["A: false, G0 cells are metabolically active", "R: true"],
                 why="'Inactive' is the trap: G0 cells are non-dividing, not non-metabolising.",
                 ncert=ref("CC", "Cell Cycle (phases of cell cycle, G0)"), secs=35)

statement_pair(T_CC, "Mitosis", "Intermediate",
               "In animal cells, cytokinesis takes place by the formation of a cell plate that grows from the centre "
               "outwards.",
               "The liquid endosperm of coconut is a multinucleate condition that arises when karyokinesis is not "
               "followed by cytokinesis.",
               False, True, "D",
               "Cytokinesis and syncytium",
               "In animal cells a furrow appears in the plasma membrane and deepens until the cytoplasm divides in "
               "two. Plant cells, enclosed by a rigid wall, form a cell plate from the centre outwards. When "
               "karyokinesis is not followed by cytokinesis, a multinucleate syncytium forms, e.g. the liquid "
               "endosperm of coconut.",
               ["Statement I: false, cell plate formation is in plant cells", "Statement II: true"],
               ncert=ref("CC", "M Phase (cytokinesis)"), secs=35)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following statements about mitosis are correct?",
                [("At the end of prophase, the Golgi complex, endoplasmic reticulum, nucleolus and nuclear envelope "
                  "are no longer seen.", True),
                 ("Kinetochores are small disc-shaped structures at the surface of the centromere that serve as "
                  "attachment sites for spindle fibres.", True),
                 ("In anaphase, the arms of each chromosome lead the way to the pole and the centromere trails "
                  "behind.", False),
                 ("In telophase, chromosomes cluster at opposite poles and their identity as discrete elements is "
                  "lost.", True)],
                [("a", "b", "c"), ("b", "c", "d"), ("a", "c", "d")],
                "Stages of mitosis",
                "Late prophase: Golgi, ER, nucleolus and nuclear envelope disappear. Metaphase: spindle fibres attach "
                "to kinetochores. Anaphase: centromeres split, and the chromatids move to the poles with the "
                "centromere leading and the arms trailing. Telophase: chromosomes decondense at the poles and lose "
                "their individuality; the nuclear envelope and nucleolus reappear.",
                ["(a) True", "(b) True", "(c) False: the centromere leads, the arms trail", "(d) True"],
                ncert=ref("CC", "M Phase"), secs=50)

# Plant with 2n = 16: metaphase 16 chromosomes x 2 chromatids; anaphase sister chromatids separate
TWO_N = 16
META_CHROMATIDS = TWO_N * 2
ANA_CHROMOSOMES = TWO_N * 2
assert (META_CHROMATIDS, ANA_CHROMOSOMES) == (32, 32)
numerical(T_CC, "Mitosis", "Advanced",
          "A plant cell with 2n = 16 divides by mitosis. How many chromatids are present in the cell at metaphase, "
          "and how many chromosomes are present in the whole cell at anaphase?",
          ["16 chromatids and 16 chromosomes", "32 chromatids and 16 chromosomes",
           "16 chromatids and 32 chromosomes", "32 chromatids and 32 chromosomes"], "D",
          (META_CHROMATIDS, ANA_CHROMOSOMES) == (32, 32),
          "Chromatid and chromosome counts during mitosis",
          "After the S phase each of the 16 chromosomes has two sister chromatids, giving 32 chromatids at "
          "metaphase. At anaphase the centromeres split and each chromatid becomes a daughter chromosome, so the "
          "cell briefly holds 32 chromosomes (16 moving to each pole).",
          ["Metaphase: 16 chromosomes × 2 chromatids = 32 chromatids",
           "Anaphase: centromeres split → 32 chromosomes (16 at each pole)"],
          why="16 chromatids forgets that DNA replicated in S phase. 16 chromosomes at anaphase counts only one pole "
              "or forgets that separated chromatids are counted as chromosomes.",
          ncert=ref("CC", "M Phase (metaphase, anaphase)"), secs=60)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements about meiosis are correct?",
                [("Crossing over is an enzyme-mediated process, and the enzyme involved is recombinase.", True),
                 ("In the oocytes of some vertebrates, diplotene can last for months or years.", True),
                 ("DNA replicates during interkinesis.", False),
                 ("Sister chromatids separate from each other during anaphase I.", False)],
                [("a", "b", "d"), ("b", "c", "d"), ("a", "c")],
                "Events of meiosis",
                "Crossing over in pachytene is mediated by the enzyme recombinase. Diplotene can last for months or "
                "years in oocytes of some vertebrates. Interkinesis is generally short-lived and has no DNA "
                "replication. In anaphase I, homologous chromosomes separate while sister chromatids stay associated "
                "at their centromeres; sister chromatids separate in anaphase II.",
                ["(a) True", "(b) True", "(c) False: no DNA replication in interkinesis",
                 "(d) False: homologues separate in anaphase I"],
                why="(d) describes anaphase II (or mitotic anaphase), the commonest meiosis trap.",
                ncert=ref("CC", "Meiosis"), secs=55)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "Meiosis II resembles a normal mitosis.",
                 "Meiosis II begins immediately after cytokinesis, usually before the chromosomes have fully "
                 "elongated.",
                 True, True, False, "B",
                 "Meiosis II",
                 "In meiosis II the centromeres split and sister chromatids separate, just as in mitosis, which is why "
                 "it resembles mitosis. NCERT also states that meiosis II starts immediately after cytokinesis, "
                 "usually before the chromosomes fully elongate. That is true, but its timing does not explain the "
                 "similarity to mitosis.",
                 ["A: true", "R: true", "The resemblance comes from separation of sister chromatids, not the timing "
                  "of onset → R does not explain A"],
                 why="Option A is the trap: R describes when meiosis II begins, not why it is mitosis-like.",
                 ncert=ref("CC", "Meiosis (meiosis II)"), secs=45)

statement_pair(T_CC, "Mitosis", "Advanced",
               "In animals, mitotic cell division is seen only in diploid somatic cells.",
               "In plants, mitotic divisions occur only in diploid cells.",
               True, False, "C",
               "Where mitosis occurs",
               "NCERT: in animals, mitotic division is seen only in diploid somatic cells. Against this, plants can "
               "show mitotic divisions in both haploid and diploid cells (for example, the haploid gametophytes).",
               ["Statement I: true", "Statement II: false, plants show mitosis in haploid and diploid cells"],
               why="Treating plants like animals is the trap; haploid plant cells also divide by mitosis.",
               ncert=ref("CC", "M Phase (introduction to mitosis)"), secs=40)

# =============================================================== 7. Photosynthesis (4/6/4)
direct(T_PS, "Site and pigments", "Basic",
       "When the pigments of a green leaf are separated by paper chromatography, chlorophyll b appears:",
       "yellow green", ["bright or blue green", "yellow", "yellow to yellow-orange"],
       "Photosynthetic pigments",
       "Paper chromatography of leaf pigments shows four pigments: chlorophyll a (bright or blue green), "
       "chlorophyll b (yellow green), xanthophylls (yellow) and carotenoids (yellow to yellow-orange).",
       ["Chlorophyll a → bright/blue green", "Chlorophyll b → yellow green", "Xanthophylls → yellow",
        "Carotenoids → yellow to yellow-orange"],
       why="Each wrong option is the colour of one of the other three pigments.",
       ncert=ref("PS", "How many types of pigments are involved in photosynthesis?"), secs=25)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "The splitting of water during the light reaction is associated with:",
       "Photosystem II", ["Photosystem I", "NADP reductase", "ATP synthase"],
       "Splitting of water",
       "Electrons that leave PS II are replaced by electrons from the splitting of water: 2H₂O → 4H⁺ + O₂ + 4e⁻. "
       "The water-splitting complex is associated with PS II, which is located on the inner side of the thylakoid "
       "membrane.",
       ["PS II loses electrons to the electron transport chain", "Water splitting supplies replacement electrons → "
        "linked to PS II"],
       why="PS I receives its replacement electrons from PS II through the electron transport chain, not from water.",
       ncert=ref("PS", "The electron transport (splitting of water)"), secs=25)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "The first stable product of CO₂ fixation in the Calvin cycle is:",
       "3-phosphoglyceric acid (PGA)", ["oxaloacetic acid (OAA)", "ribulose bisphosphate (RuBP)",
                                        "phosphoenol pyruvate (PEP)"],
       "The C3 pathway",
       "Melvin Calvin, using radioactive ¹⁴C, found that the first CO₂ fixation product is a 3-carbon organic acid, "
       "3-phosphoglyceric acid (PGA); hence the name C3 pathway.",
       ["CO₂ + RuBP → 2 molecules of 3-PGA (RuBisCO)"],
       why="OAA is the first product of the C4 pathway; RuBP and PEP are CO₂ acceptors, not products.",
       ncert=ref("PS", "Where are the ATP and NADPH used? (the primary acceptor of CO₂)"), secs=25)

statement_pair(T_PS, "Limiting factors", "Basic",
               "Blackman (1905) gave the law of limiting factors.",
               "Carbon dioxide is the major limiting factor for photosynthesis.",
               True, True, "A",
               "Factors affecting photosynthesis",
               "Blackman's law (1905): if a process depends on several factors, its rate is set by the factor nearest "
               "its minimal value. NCERT states that carbon dioxide is the major limiting factor for photosynthesis, "
               "since its concentration in the atmosphere is very low (0.03 to 0.04 per cent).",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Factors affecting photosynthesis"), secs=25)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                 "Cyclic photophosphorylation produces ATP but no NADPH + H⁺.",
                 "In cyclic photophosphorylation, the electrons excited from PS I are circulated back to PS I "
                 "through the electron transport chain instead of being passed to NADP⁺.",
                 True, True, True, "A",
                 "Cyclic photophosphorylation",
                 "When only PS I works, the excited electron returns to PS I through the electron transport chain. "
                 "ATP is made during this flow, but since the electron never reaches NADP⁺, no NADPH + H⁺ forms. R "
                 "explains A.",
                 ["A: true", "R: true", "No electron reaches NADP⁺ → no NADPH → R explains A"],
                 ncert=ref("PS", "Cyclic and non-cyclic photo-phosphorylation"), secs=40)

multi_statement(T_PS, "Chemiosmosis", "Intermediate",
                "Which of the following statements about chemiosmotic ATP synthesis in chloroplasts are correct?",
                [("Protons accumulate inside the lumen of the thylakoid.", True),
                 ("NADP reductase is located on the lumen side of the thylakoid membrane.", False),
                 ("The CF₀ part of ATP synthase forms a transmembrane channel for facilitated diffusion of protons.",
                  True),
                 ("The CF₁ part of ATP synthase protrudes on the outer surface of the thylakoid membrane, facing the "
                  "stroma.", True),
                 ("The splitting of water takes place on the stroma side of the thylakoid membrane.", False)],
                [("a", "b", "c"), ("c", "d", "e"), ("a", "b", "d", "e")],
                "Chemiosmotic hypothesis",
                "A proton gradient builds up across the thylakoid membrane: water splitting releases H⁺ inside the "
                "lumen, the electron carriers move H⁺ from the stroma into the lumen, and NADP reductase on the "
                "stroma side removes H⁺ from the stroma. Protons flow back through the CF₀ channel, causing a change "
                "in CF₁ (facing the stroma) that makes ATP.",
                ["(a) True", "(b) False: NADP reductase is on the stroma side", "(c) True", "(d) True",
                 "(e) False: water is split on the inner (lumen) side"],
                ncert=ref("PS", "Chemiosmotic hypothesis"), secs=60)

match_list(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
           "molecule", "role",
           ["Phosphoenol pyruvate (PEP)", "Oxaloacetic acid (OAA)", "Ribulose bisphosphate (RuBP)", "NADP⁺"],
           ["Final acceptor of electrons in non-cyclic photophosphorylation",
            "Primary CO₂ acceptor in the mesophyll cells of C4 plants",
            "First product of CO₂ fixation in the C4 pathway",
            "CO₂ acceptor in the Calvin cycle"],
           {"A": "II", "B": "III", "C": "IV", "D": "I"},
           [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
            {"A": "III", "B": "II", "C": "IV", "D": "I"}],
           "Key molecules of photosynthesis",
           "In C4 plants, PEP (3C) in the mesophyll accepts CO₂ (enzyme PEPcase), forming the 4C OAA. In the Calvin "
           "cycle the CO₂ acceptor is the 5C RuBP. In non-cyclic photophosphorylation, electrons finally reduce "
           "NADP⁺ to NADPH + H⁺.",
           ["PEP → II", "OAA → III", "RuBP → IV", "NADP⁺ → I"],
           why="PEP and OAA are often swapped: PEP is the acceptor, OAA the product.",
           ncert=ref("PS", "The C4 pathway; The Calvin cycle; The electron transport"), secs=45)

statement_pair(T_PS, "Photorespiration", "Intermediate",
               "In photorespiration, there is no synthesis of sugars, ATP or NADPH.",
               "In photorespiration, RuBP combines with O₂ to form two molecules of PGA.",
               True, False, "C",
               "Photorespiration",
               "When RuBisCO binds O₂, RuBP forms one molecule of PGA and one of phosphoglycolate, instead of two PGA. "
               "The pathway makes no sugar, ATP or NADPH; it releases CO₂ and uses ATP.",
               ["Statement I: true", "Statement II: false, one PGA + one phosphoglycolate"],
               ncert=ref("PS", "Photorespiration"), secs=35)

direct(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
       "Which of the following is NOT a feature of the bundle sheath cells of C4 plants?",
       "Presence of PEP carboxylase",
       ["A large number of chloroplasts", "Thick walls impervious to gaseous exchange",
        "No intercellular spaces"],
       "Kranz anatomy",
       "The bundle sheath cells of C4 plants (Kranz anatomy) are large, form several layers around the vascular "
       "bundles, have many chloroplasts, thick walls impervious to gas exchange and no intercellular spaces. They "
       "are rich in RuBisCO but lack PEPcase, which is found in the mesophyll cells.",
       ["Bundle sheath: RuBisCO present, PEPcase absent", "Mesophyll: PEPcase present, RuBisCO absent"],
       ncert=ref("PS", "The C4 pathway"), secs=35)

direct(T_PS, "Limiting factors", "Intermediate",
       "Tomatoes and bell peppers are grown in carbon dioxide-enriched greenhouses because:",
       "C3 plants respond to a higher CO₂ concentration with a higher rate of photosynthesis, giving higher yields",
       ["higher CO₂ makes the stomata close and saves water",
        "C4 plants respond to a higher CO₂ concentration more than C3 plants do",
        "higher CO₂ raises the oxygenase activity of RuBisCO"],
       "CO₂ as a limiting factor",
       "C3 plants are not saturated at the present low CO₂ level; their rate of photosynthesis rises as CO₂ "
       "concentration increases. C4 plants are saturated at about 360 µl/L. So C3 crops such as tomato and bell "
       "pepper give higher yields in CO₂-enriched greenhouses.",
       ["Tomato, bell pepper → C3 plants", "C3 plants respond to higher CO₂ → more photosynthesis → higher "
        "productivity"],
       why="C4 plants saturate at lower CO₂ levels than C3 plants. Higher CO₂ favours carboxylation, not "
           "oxygenation.",
       ncert=ref("PS", "Factors affecting photosynthesis (carbon dioxide concentration)"), secs=40)

# Calvin cycle: per CO2 fixed, 3 ATP and 2 NADPH; one glucose needs 6 CO2 (6 turns)
ATP_PER_CO2, NADPH_PER_CO2 = 3, 2
GLUCOSE = 3
ATP_NEEDED = GLUCOSE * 6 * ATP_PER_CO2
NADPH_NEEDED = GLUCOSE * 6 * NADPH_PER_CO2
assert (6 * ATP_PER_CO2, 6 * NADPH_PER_CO2) == (18, 12) and (ATP_NEEDED, NADPH_NEEDED) == (54, 36)
numerical(T_PS, "Calvin cycle and C4 pathway", "Advanced",
          "In the Calvin cycle, fixing one molecule of CO₂ needs 3 ATP and 2 NADPH. How many molecules of ATP and "
          "NADPH are needed to make 3 molecules of glucose?",
          ["54 ATP and 36 NADPH", "36 ATP and 54 NADPH", "18 ATP and 12 NADPH", "54 ATP and 54 NADPH"], "A",
          (ATP_NEEDED, NADPH_NEEDED) == (54, 36),
          "Energy requirement of the Calvin cycle",
          "Glucose has six carbon atoms, so six turns of the Calvin cycle (six CO₂ fixed) make one glucose, needing "
          "18 ATP and 12 NADPH. Three glucose molecules need three times as much.",
          ["One glucose: 6 CO₂ × 3 ATP = 18 ATP; 6 × 2 NADPH = 12 NADPH",
           "Three glucose: 3 × 18 = 54 ATP; 3 × 12 = 36 NADPH"],
          why="18 ATP and 12 NADPH is for one glucose only. 36 ATP and 54 NADPH swaps the two. 54 NADPH takes 3 "
              "NADPH per CO₂.",
          ncert=ref("PS", "The Calvin cycle"), secs=60,
          short="Per glucose: 18 ATP, 12 NADPH (ratio 3 : 2); multiply by 3.")

multi_statement(T_PS, "Light reactions and photophosphorylation", "Advanced",
                "Which of the following statements about the light reaction are correct?",
                [("PS I and PS II are named in the sequence of their discovery, not in the sequence in which they "
                  "function.", True),
                 ("The reaction centre of PS I has an absorption peak at 700 nm.", True),
                 ("In the Z scheme, electrons move from PS I to PS II.", False),
                 ("Cyclic photophosphorylation also occurs when only light of wavelengths beyond 680 nm is "
                  "available for excitation.", True),
                 ("Chlorophyll b is the chief pigment associated with photosynthesis.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "c", "d", "e")],
                "Photosystems and the Z scheme",
                "PS I and PS II are numbered by order of discovery. Their reaction centres are P700 (PS I) and P680 "
                "(PS II). In non-cyclic flow (Z scheme), electrons pass from PS II through the electron transport "
                "chain to PS I and then to NADP⁺. Cyclic photophosphorylation also occurs when only light beyond "
                "680 nm is available. Chlorophyll a is the chief pigment; the others are accessory pigments.",
                ["(a) True", "(b) True: P700", "(c) False: PS II → PS I", "(d) True",
                 "(e) False: chlorophyll a is the chief pigment"],
                ncert=ref("PS", "Light reaction; The electron transport; Cyclic and non-cyclic photo-phosphorylation"),
                secs=60)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "In C4 plants, the Calvin cycle takes place in the mesophyll cells.",
                 "The mesophyll cells of C4 plants lack RuBisCO.",
                 False, True, False, "D",
                 "Division of labour in C4 leaves",
                 "Mesophyll cells of C4 plants have PEPcase but lack RuBisCO, so the Calvin cycle cannot run there. CO₂ "
                 "released from C4 acids in the bundle sheath cells enters the Calvin cycle there, where RuBisCO is "
                 "abundant. So A is false and R is true.",
                 ["A: false, the Calvin cycle runs in bundle sheath cells", "R: true"],
                 why="R is the very reason the Calvin cycle cannot run in the mesophyll, which makes A false.",
                 ncert=ref("PS", "The C4 pathway"), secs=45)

statement_pair(T_PS, "Limiting factors", "Advanced",
               "Increasing the incident light beyond a point causes breakdown of chlorophyll and a decrease in "
               "photosynthesis.",
               "Light saturation occurs at about 10 per cent of full sunlight, so, except for plants in shade or in "
               "dense forests, light is rarely a limiting factor in nature.",
               True, True, "A",
               "Light as a factor",
               "At low light intensity, the rate of CO₂ fixation rises linearly with light. Saturation is reached at "
               "about 10 per cent of full sunlight, so light seldom limits photosynthesis in nature except in shade "
               "or dense forests. Very high light causes chlorophyll breakdown and a fall in photosynthesis.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Factors affecting photosynthesis (light)"), secs=40)

# =============================================================== 8. Respiration in Plants (4/5/4)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "The scheme of glycolysis (EMP pathway) was given by:",
       "Embden, Meyerhof and Parnas", ["Hans Krebs", "Melvin Calvin", "Hatch and Slack"],
       "Glycolysis",
       "The scheme of glycolysis was given by Gustav Embden, Otto Meyerhof and J. Parnas, and is often called the "
       "EMP pathway. It occurs in the cytoplasm and is the only respiratory process in anaerobic organisms.",
       ["EMP = Embden, Meyerhof, Parnas"],
       why="Krebs described the TCA cycle; Calvin the C3 cycle; Hatch and Slack the C4 pathway.",
       ncert=ref("RES", "Glycolysis"), secs=20)

direct(T_RES, "TCA cycle", "Basic",
       "The TCA cycle begins when an acetyl group condenses with oxaloacetic acid and water to form:",
       "citric acid", ["isocitric acid", "α-ketoglutaric acid", "succinic acid"],
       "TCA (Krebs) cycle",
       "The first reaction of the TCA cycle, catalysed by citrate synthase, condenses the acetyl group of acetyl "
       "CoA with oxaloacetic acid (OAA) and water to give citric acid.",
       ["Acetyl CoA + OAA + H₂O → citric acid + CoA (citrate synthase)"],
       why="Isocitrate, α-ketoglutarate and succinate are later intermediates of the cycle.",
       ncert=ref("RES", "Tricarboxylic acid cycle"), secs=25)

direct(T_RES, "Electron transport system", "Basic",
       "In aerobic respiration, the final acceptor of electrons (hydrogen) in the electron transport system is:",
       "oxygen", ["NAD⁺", "cytochrome c", "ubiquinone"],
       "Role of oxygen",
       "Electrons passed along the electron transport chain finally reduce oxygen, which is the final hydrogen "
       "acceptor, forming water. Oxygen's role is limited to this terminal stage.",
       ["Electrons: NADH → complex I → ubiquinone → complex III → cytochrome c → complex IV → O₂",
        "O₂ + electrons + H⁺ → water"],
       why="NAD⁺, ubiquinone and cytochrome c are intermediate carriers, not the final acceptor.",
       ncert=ref("RES", "Electron transport system (ETS) and oxidative phosphorylation"), secs=20)

statement_pair(T_RES, "Respiratory quotient", "Basic",
               "The respiratory quotient (RQ) is the ratio of the volume of CO₂ evolved to the volume of O₂ consumed "
               "in respiration.",
               "When carbohydrates are used as the substrate and completely oxidised, the RQ is 1.",
               True, True, "A",
               "Respiratory quotient",
               "RQ = volume of CO₂ evolved / volume of O₂ consumed. For carbohydrates, as in C₆H₁₂O₆ + 6O₂ → 6CO₂ + "
               "6H₂O, equal volumes of CO₂ and O₂ are exchanged, so RQ = 1.",
               ["Statement I: true", "Statement II: true, 6 CO₂ / 6 O₂ = 1"],
               ncert=ref("RES", "Respiratory quotient"), secs=25)

# RQ of malic acid: C4H6O5 + 3 O2 -> 4 CO2 + 3 H2O
C, H, O = 4, 6, 5
O2_USED = F(2 * C + F(H, 2) - O, 2)
assert O2_USED == 3 and 2 * O2_USED + O == 2 * C + F(H, 2)  # oxygen atoms balance
RQ_MALIC = F(C) / O2_USED
assert RQ_MALIC == F(4, 3) and round(float(RQ_MALIC), 2) == 1.33
numerical(T_RES, "Respiratory quotient", "Intermediate",
          "Malic acid is completely oxidised according to the equation\nC₄H₆O₅ + 3O₂ → 4CO₂ + 3H₂O\n"
          "The respiratory quotient (RQ) of malic acid is about:",
          ["0.70", "0.75", "1.00", "1.33"], "D", RQ_MALIC == F(4, 3),
          "RQ from a balanced equation",
          "RQ = moles (volume) of CO₂ evolved / moles of O₂ consumed. Organic acids are already partly oxidised, so "
          "they need less O₂ than the CO₂ they release, giving RQ greater than 1.",
          ["CO₂ evolved = 4", "O₂ consumed = 3", "RQ = 4/3 ≈ 1.33"],
          why="0.75 inverts the ratio (O₂/CO₂ = 3/4). 1.00 is the RQ of carbohydrates. 0.70 is the "
              "RQ of fats such as tripalmitin.",
          ncert=ref("RES", "Respiratory quotient"), secs=45,
          short="Read the coefficients: RQ = CO₂/O₂ = 4/3.")

match_list(T_RES, "Electron transport system", "Intermediate",
           "complex of the ETS", "name",
           ["Complex I", "Complex III", "Complex IV", "Complex V"],
           ["Cytochrome c oxidase", "ATP synthase", "NADH dehydrogenase", "Cytochrome bc₁ complex"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
            {"A": "III", "B": "IV", "C": "II", "D": "I"}],
           "Complexes of the mitochondrial electron transport system",
           "Complex I (NADH dehydrogenase) oxidises NADH and passes electrons to ubiquinone. Complex II is succinate "
           "dehydrogenase. Ubiquinol is oxidised by complex III (cytochrome bc₁). Cytochrome c carries electrons to "
           "complex IV (cytochrome c oxidase). Complex V is ATP synthase.",
           ["Complex I → NADH dehydrogenase (III)", "Complex III → cytochrome bc₁ (IV)",
            "Complex IV → cytochrome c oxidase (I)", "Complex V → ATP synthase (II)"],
           ncert=ref("RES", "Electron transport system (ETS) and oxidative phosphorylation"), secs=40)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "During strenuous exercise, lactic acid accumulates in the muscles.",
                 "When oxygen is inadequate, pyruvic acid is reduced to lactic acid by lactate dehydrogenase.",
                 True, True, True, "A",
                 "Lactic acid fermentation in muscle",
                 "In muscle cells during exercise, oxygen supply falls short of demand. Pyruvic acid is then reduced "
                 "to lactic acid by lactate dehydrogenase, with NADH + H⁺ as the reducing agent, so lactic acid "
                 "builds up. R explains A.",
                 ["A: true", "R: true", "Reduction of pyruvate under low O₂ is the source of the lactic acid → R "
                  "explains A"],
                 ncert=ref("RES", "Fermentation"), secs=35)

multi_statement(T_RES, "Glycolysis and fermentation", "Intermediate",
                "Which of the following statements about glycolysis are correct?",
                [("Glucose is phosphorylated to glucose-6-phosphate by the enzyme hexokinase.", True),
                 ("ATP is used when fructose-6-phosphate is converted to fructose 1,6-bisphosphate.", True),
                 ("NADH + H⁺ is formed when 1,3-bisphosphoglycerate (BPGA) is converted to 3-phosphoglyceric acid "
                  "(PGA).", False),
                 ("ATP is formed when phosphoenolpyruvate (PEP) is converted to pyruvic acid.", True)],
                [("a", "b", "c"), ("b", "c", "d"), ("a", "b", "c", "d")],
                "Steps of glycolysis",
                "ATP is used at two steps: glucose → glucose-6-phosphate (hexokinase) and fructose-6-phosphate → "
                "fructose 1,6-bisphosphate. NADH + H⁺ forms when PGAL (3-phosphoglyceraldehyde) is oxidised to BPGA. "
                "ATP is formed at two steps: BPGA → PGA and PEP → pyruvic acid.",
                ["(a) True", "(b) True",
                 "(c) False: BPGA → PGA produces ATP; NADH forms at PGAL → BPGA", "(d) True"],
                why="(c) shifts the NADH-forming step one reaction later; that step makes ATP instead.",
                ncert=ref("RES", "Glycolysis"), secs=50)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
               "Fatty acids enter the respiratory pathway after being converted to PGAL.",
               "Amino acids enter the respiratory pathway only after conversion to acetyl CoA.",
               False, False, "B",
               "Entry of fats and proteins into respiration",
               "Fats are broken into glycerol and fatty acids. Fatty acids are degraded to acetyl CoA; glycerol is "
               "converted to PGAL. Proteins are degraded to amino acids which, after deamination, enter at "
               "different points: as pyruvate, as acetyl CoA, or within the Krebs cycle.",
               ["Statement I: false, glycerol → PGAL; fatty acids → acetyl CoA",
                "Statement II: false, amino acids enter at several points, not only as acetyl CoA"],
               ncert=ref("RES", "Amphibolic pathway"), secs=40)

# NADH formed per glucose up to the end of the Krebs cycle: glycolysis 2 + link reaction 2 + TCA 3 x 2 = 10
NADH_GLYCOLYSIS, NADH_LINK, NADH_TCA_PER_TURN, TURNS = 2, 2, 3, 2
NADH_PER_GLUCOSE = NADH_GLYCOLYSIS + NADH_LINK + NADH_TCA_PER_TURN * TURNS
assert NADH_PER_GLUCOSE == 10 and 2 * NADH_PER_GLUCOSE == 20
assert 2 * (NADH_LINK + NADH_TCA_PER_TURN * TURNS) == 16  # distractor: glycolytic NADH forgotten
assert 2 * (NADH_PER_GLUCOSE + 1 * TURNS) == 24  # distractor: FADH2 counted as NADH
numerical(T_RES, "TCA cycle", "Advanced",
          "Two molecules of glucose are completely oxidised by aerobic respiration. How many molecules of NADH + H⁺ "
          "are formed in all, from glycolysis to the end of the Krebs cycle (including the conversion of pyruvic "
          "acid to acetyl CoA)?",
          ["10", "16", "20", "24"], "C", 2 * NADH_PER_GLUCOSE == 20,
          "Counting reduced coenzymes in respiration",
          "Per glucose: glycolysis gives 2 NADH; oxidative decarboxylation of 2 pyruvic acid to 2 acetyl CoA gives "
          "2 NADH; each turn of the TCA cycle reduces NAD⁺ at three points, and the cycle turns twice per glucose. "
          "Then double the total for two glucose molecules.",
          ["Glycolysis: 2 NADH", "Pyruvic acid → acetyl CoA: 2 NADH", "TCA: 3 NADH × 2 turns = 6 NADH",
           "Per glucose = 10; for two glucose = 20"],
          why="10 is the count for one glucose. 16 leaves out the glycolytic NADH. 24 also counts the FADH₂ formed in "
              "the TCA cycle as NADH.",
          ncert=ref("RES", "Glycolysis; Aerobic respiration; Tricarboxylic acid cycle"), secs=90,
          short="Per pyruvate: 4 NADH (1 link + 3 TCA); per glucose 2 × 4 + 2 = 10.")

multi_statement(T_RES, "Electron transport system", "Advanced",
                "Which of the following statements about the mitochondrial electron transport system and ATP "
                "synthase are correct?",
                [("Cytochrome c is a small protein attached to the outer surface of the inner membrane that carries "
                  "electrons between complex III and complex IV.", True),
                 ("Complex IV contains cytochromes a and a₃ and two copper centres.", True),
                 ("The F₁ part of ATP synthase is an integral membrane protein complex that forms the proton "
                  "channel.", False),
                 ("For each ATP produced, 2H⁺ pass through F₀ from the intermembrane space to the matrix.", True),
                 ("Ubiquinone also receives reducing equivalents from FADH₂ through complex II.", True)],
                [("a", "b", "c", "d"), ("b", "c", "e"), ("a", "c", "d", "e")],
                "ETS and oxidative phosphorylation",
                "Cytochrome c is a mobile carrier between complexes III and IV. Complex IV (cytochrome c oxidase) has "
                "cytochromes a and a₃ and two copper centres. Ubiquinone receives electrons from complex I and, via "
                "complex II, from FADH₂. In ATP synthase, F₀ is the integral membrane complex forming the proton "
                "channel; F₁ is the peripheral headpiece where ATP is made. Two H⁺ pass through F₀ per ATP.",
                ["(a) True", "(b) True", "(c) False: F₀ is integral and forms the channel; F₁ is peripheral",
                 "(d) True", "(e) True"],
                why="(c) swaps the roles of F₀ and F₁.",
                ncert=ref("RES", "Electron transport system (ETS) and oxidative phosphorylation"), secs=70)

assertion_reason(T_RES, "ATP yield and amphibolic pathway", "Advanced",
                 "The respiratory pathway is better described as an amphibolic pathway than as a catabolic one.",
                 "Intermediates of the respiratory pathway are never withdrawn for the synthesis of other "
                 "substances.",
                 True, False, False, "C",
                 "Amphibolic pathway",
                 "Respiration breaks down substrates (catabolism), but its intermediates are also withdrawn to make "
                 "other molecules; for example, acetyl CoA is withdrawn for fatty acid synthesis. Because the pathway "
                 "takes part in both anabolism and catabolism, it is called amphibolic. So A is true and R is false.",
                 ["A: true", "R: false, intermediates such as acetyl CoA are withdrawn for synthesis"],
                 ncert=ref("RES", "Amphibolic pathway"), secs=40)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Advanced",
               "In fermentation, less than seven per cent of the energy in glucose is released.",
               "In fermentation, NADH is oxidised to NAD⁺ vigorously, whereas in aerobic respiration this reaction is "
               "very slow.",
               True, False, "C",
               "Fermentation versus aerobic respiration",
               "Fermentation only partly breaks down glucose and releases less than seven per cent of its energy; "
               "net gain is two ATP per glucose. In fermentation, NADH is oxidised to NAD⁺ rather slowly, whereas the "
               "reaction is very vigorous in aerobic respiration. Statement II has these reversed.",
               ["Statement I: true", "Statement II: false, slow in fermentation, vigorous in aerobic respiration"],
               ncert=ref("RES", "Fermentation; The respiratory balance sheet"), secs=40)


# =============================================================== assembly and checks
def place_free(questions):
    """Gives each free-placement question its key so that the whole package is balanced (about 25% each)."""
    fixed = Counter(q["correct_answer"] for q in questions if "_free" not in q)
    free = [q for q in questions if "_free" in q]
    total = len(questions)
    target = {L: total // 4 + (1 if i >= 4 - total % 4 else 0) for i, L in enumerate(LETTERS)}
    need = {L: target[L] - fixed[L] for L in LETTERS}
    assert all(n >= 0 for n in need.values()) and sum(need.values()) == len(free), (need, len(free))
    ptr = 0
    for q in free:
        while need[LETTERS[ptr % 4]] == 0:
            ptr += 1
        at = LETTERS[ptr % 4]
        need[at] -= 1
        ptr += 1
        correct, wrong = q.pop("_free")
        opts = list(wrong)
        opts.insert(LETTERS.index(at), correct)
        _fix(q, opts, at)


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
    assert pkg["output"] == "batches/parts/BATCH_001_BOT_p1.json"


if __name__ == "__main__":
    place_free(QUESTIONS)
    check_plan(QUESTIONS)
    keys = Counter(q["correct_answer"] for q in QUESTIONS)
    fmts = Counter(q["format"] for q in QUESTIONS)
    assert max(keys.values()) - min(keys.values()) <= 1, keys
    for f in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f] >= 0.08 * len(QUESTIONS), (f, fmts[f])
    assert all(q["solution"]["ncert_reference"] for q in QUESTIONS)
    assert len({q["question_text"] for q in QUESTIONS}) == len(QUESTIONS)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "Package BOT_001_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 121 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
