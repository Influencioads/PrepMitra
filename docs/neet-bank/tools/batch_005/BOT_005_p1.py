"""Writes batches/parts/BATCH_005_BOT_p1.json: package BOT_005_p1 of batch 5 (Botany, 125 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_001001 .. NEET_BOT_001125.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books (secondary growth, taxonomical aids, plant life cycles and alternation of generations, early
experiments on photosynthesis) is not used. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_005/BOT_005_p1.py
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
PLAN = ROOT / "batches" / "plans" / "BATCH_005_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_005_BOT_p1.json"
PACKAGE = "BOT_005_p1"
BATCH = "BATCH_005"
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
direct(T_LIV, "What is living", "Basic",
       "In which of the following pairs of organisms does NCERT describe asexual reproduction by budding?",
       "Yeast and Hydra",
       ["Planaria and Hydra", "Fungi and filamentous algae", "Mosses and Planaria"], "B",
       "Reproduction as a feature of living organisms",
       "NCERT notes that organisms reproduce asexually in different ways: in yeast and Hydra we observe budding, "
       "while in Planaria (flatworms) we observe true regeneration. Fungi, filamentous algae and the protonema of "
       "mosses multiply by fragmentation.",
       ["Budding → yeast and Hydra", "True regeneration → Planaria", "Fragmentation → fungi, filamentous algae, "
                                                                      "protonema of mosses"],
       why="Planaria is NCERT's example of true regeneration, not budding. Fungi, filamentous algae and the moss "
           "protonema are its examples of fragmentation.",
       ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=25)

direct(T_LIV, "Lichens, viruses and viroids", "Basic",
       "The capsid of a virus is made of small subunits called capsomeres. NCERT states that the capsomeres are "
       "arranged in:",
       "helical or polyhedral geometric forms",
       ["two thin overlapping shells that fit like a soap box", "stiff cellulose plates on the outer surface",
        "a flexible protein-rich layer called the pellicle"], "C",
       "Structure of a virus",
       "A virus has a protein coat, the capsid, made of small subunits called capsomeres, which protects the "
       "nucleic acid. The capsomeres are arranged in helical or polyhedral geometric forms.",
       ["Capsid = capsomeres", "Arrangement: helical or polyhedral"],
       why="Two overlapping shells describe the diatom wall, cellulose plates the wall of dinoflagellates, and the "
           "pellicle the body covering of euglenoids.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=25)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "The word 'systematics' is derived from the Latin word 'systema', which means:",
       "systematic arrangement of organisms",
       ["naming of organisms with two words", "grouping of organisms by their mode of nutrition",
        "the study of the evolutionary history of organisms"], "B",
       "Systematics",
       "The word systematics is derived from the Latin word 'systema', which means systematic arrangement of "
       "organisms. Linnaeus used 'Systema Naturae' as the title of his publication.",
       ["systema = systematic arrangement of organisms"],
       why="Two-word naming is binomial nomenclature. Mode of nutrition is only one criterion of Whittaker's "
           "classification. Systematics takes evolutionary relationships into account, but that is not the meaning "
           "of 'systema'.",
       ncert=ref("LW", "Diversity in the Living World (systematics)"), secs=20)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Basic",
               "Fungi are cosmopolitan and occur in air, water, soil and on animals and plants.",
               "Fungi that absorb soluble organic matter from dead substrates are called parasites.",
               True, False, "C",
               "Nutrition in fungi",
               "Fungi are cosmopolitan and occur in air, water, soil and on animals and plants. Most fungi are "
               "heterotrophic and absorb soluble organic matter from dead substrates; these are called saprophytes. "
               "Those that depend on living plants and animals are called parasites.",
               ["Statement I: true", "Statement II: false, fungi living on dead substrates are saprophytes"],
               ncert=ref("BC", "Kingdom Fungi"), secs=30)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Which class of fungi is commonly known as the sac-fungi?",
       "Ascomycetes", ["Phycomycetes", "Basidiomycetes", "Deuteromycetes"], "D",
       "Classes of fungi",
       "Commonly known as sac-fungi, the ascomycetes are mostly multicellular, e.g., Penicillium, or rarely "
       "unicellular, e.g., yeast (Saccharomyces). Their sexual spores, ascospores, are produced in sac-like asci.",
       ["Sac-like asci → sac-fungi → Ascomycetes"],
       why="Phycomycetes are the algal fungi with aseptate mycelium. Basidiomycetes are the mushrooms, bracket fungi "
           "and puffballs. Deuteromycetes are the imperfect fungi.",
       ncert=ref("BC", "Kingdom Fungi (Ascomycetes)"), secs=20)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate", "group of protists", "habitat or habit",
           ["Chrysophytes", "Dinoflagellates", "Euglenoids", "Slime moulds"],
           ["Mostly marine and photosynthetic; appear yellow, green, brown, blue or red",
            "Majority are fresh-water organisms found in stagnant water",
            "Body moves along decaying twigs and leaves, engulfing organic material",
            "Found in fresh water as well as marine environments; float passively in water currents (plankton)"],
           "IV I II III", ["I IV II III", "IV I III II", "IV II I III"], "B",
           "Habitats of protists",
           "Chrysophytes (diatoms and desmids) occur in fresh water as well as marine environments and float "
           "passively as plankton. Dinoflagellates are mostly marine and photosynthetic, and appear yellow, green, "
           "brown, blue or red depending on their pigments. The majority of euglenoids are fresh-water organisms of "
           "stagnant water. Slime moulds are saprophytic protists whose body moves along decaying twigs and leaves, "
           "engulfing organic material.",
           ["Chrysophytes → IV", "Dinoflagellates → I", "Euglenoids → II", "Slime moulds → III"],
           why="The wrong codes swap chrysophytes with dinoflagellates (both photosynthetic, but only dinoflagellates "
               "are mostly marine), or euglenoids with slime moulds (only slime moulds engulf decaying organic "
               "matter).",
           ncert=ref("BC", "Kingdom Protista"), secs=45)

assertion_reason(T_LIV, "Lichens, viruses and viroids", "Intermediate",
                 "Viruses are obligate parasites.",
                 "Viruses replicate with their own cellular machinery, without needing a host cell.",
                 True, False, False, "C",
                 "Viruses as obligate parasites",
                 "NCERT describes viruses as obligate parasites: once they infect a cell, they take over the "
                 "machinery of the host cell to replicate themselves, killing the host. Viruses are not cells and "
                 "have no machinery of their own, so R is false.",
                 ["A: true", "R: false, viruses use the host cell's machinery to replicate"],
                 ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=35)

statement_pair(T_LIV, "Five kingdom classification", "Intermediate",
               "In Whittaker's table of the five kingdoms, the nuclear envelope is absent only in kingdom Monera.",
               "In the same table, the body organisation of kingdom Protista is described as cellular.",
               True, True, "A",
               "Characteristics of the five kingdoms",
               "Table 2.1 of NCERT gives the nuclear envelope as absent in Monera and present in Protista, Fungi, "
               "Plantae and Animalia. The body organisation is cellular in Monera and Protista, multicellular/loose "
               "tissue in Fungi, tissue/organ in Plantae and tissue/organ/organ system in Animalia.",
               ["Statement I: true (Monera is the only prokaryotic kingdom)",
                "Statement II: true (Monera and Protista are both cellular)"],
               ncert=ref("BC", "Introduction (Table 2.1: Characteristics of the Five Kingdoms)"), secs=40)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "The fruiting bodies of slime moulds bear spores at their tips. These spores are dispersed by:",
       "air currents",
       ["water currents", "the flagella of the spores themselves", "insects that visit the fruiting bodies"], "D",
       "Slime moulds",
       "Under unfavourable conditions the plasmodium of a slime mould differentiates and forms fruiting bodies "
       "bearing spores at their tips. The spores possess true walls, are extremely resistant, and are dispersed by "
       "air currents.",
       ["Slime mould spores → dispersed by air currents"],
       why="NCERT names only air currents as the agent of dispersal. The spores are walled and do not swim, and "
           "insects are not mentioned.",
       ncert=ref("BC", "Kingdom Protista (Slime Moulds)"), secs=25)

direct(T_LIV, "Taxonomy and hierarchy", "Intermediate",
       "The process by which anything is grouped into convenient categories based on some easily observable "
       "characters is called:",
       "classification", ["identification", "nomenclature", "characterisation"], "A",
       "Basic processes of taxonomy",
       "Classification is the process by which anything is grouped into convenient categories based on some easily "
       "observable characters. Characterisation, identification, classification and nomenclature together are the "
       "processes basic to taxonomy.",
       ["Grouping into convenient categories = classification"],
       why="Identification is recognising an organism correctly, nomenclature is giving it its correct scientific "
           "name, and characterisation is describing its characters. None of these is the grouping into "
           "categories.",
       ncert=ref("LW", "Taxonomic Categories"), secs=30)

statement_pair(T_LIV, "Lichens, viruses and viroids", "Intermediate",
               "Prions are infectious agents consisting of abnormally folded protein, and they are similar in size "
               "to viruses.",
               "Bovine spongiform encephalopathy (BSE), commonly called mad cow disease, is a prion disease of "
               "humans.",
               True, False, "C",
               "Prions",
               "Certain infectious neurological diseases are transmitted by an agent consisting of abnormally folded "
               "protein, similar in size to viruses; these agents are called prions. BSE (mad cow disease) is a "
               "prion disease of cattle; its analogous variant in humans is Creutzfeldt–Jakob disease (CJD).",
               ["Statement I: true", "Statement II: false, BSE occurs in cattle; the human disease is CJD"],
               ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=35)

assertion_reason(T_LIV, "Binomial nomenclature", "Intermediate",
                 "There is a need to standardise the naming of living organisms so that a particular organism is "
                 "known by the same name all over the world.",
                 "The local names of plants and animals vary from place to place, even within a country.",
                 True, True, True, "A",
                 "Need for nomenclature",
                 "We know plants and animals of our own area by their local names, and these names vary from place "
                 "to place, even within a country. This creates confusion, so a standardised naming system is needed "
                 "in which a particular organism has the same name all over the world. R is the reason given for A.",
                 ["A: true", "R: true", "Varying local names cause confusion → need for one standard name → R "
                                        "explains A"],
                 ncert=ref("LW", "Diversity in the Living World (nomenclature)"), secs=35)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Advanced",
                "Which of the following statements about reproduction in fungi are correct?",
                [("The sexual cycle involves plasmogamy, then karyogamy, and then meiosis in the zygote resulting in "
                  "haploid spores.", True),
                 ("In phycomycetes, zygospores are formed by the fusion of two gametes, which may be isogamous, "
                  "anisogamous or oogamous.", True),
                 ("Conidia are the sexual spores of ascomycetes.", False),
                 ("Vegetative reproduction in fungi takes place by fragmentation, fission and budding.", True),
                 ("Basidiocarps are the fruiting bodies of ascomycetes.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "d")], "B",
                "Reproduction in fungi",
                "Fungi reproduce vegetatively by fragmentation, fission and budding; asexually by conidia, "
                "sporangiospores or zoospores; and sexually by oospores, ascospores and basidiospores. The sexual "
                "cycle has three steps: plasmogamy, karyogamy and meiosis in the zygote giving haploid spores. In "
                "phycomycetes, zygospores form by fusion of two gametes that are isogamous, anisogamous or oogamous. "
                "Conidia are asexual spores; the sexual spores of ascomycetes are ascospores. Basidiocarps are the "
                "fruiting bodies of basidiomycetes; those of ascomycetes are ascocarps.",
                ["(a) true", "(b) true", "(c) false: conidia are asexual spores", "(d) true",
                 "(e) false: basidiocarps belong to basidiomycetes"],
                why="(a, b, c) and (b, d, e) include a false statement. (a, d) leaves out the true statement (b).",
                ncert=ref("BC", "Kingdom Fungi"), secs=60)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following statements about members of kingdom Animalia are correct?",
                [("They are heterotrophic, eukaryotic, multicellular organisms whose cells lack cell walls.", True),
                 ("Their mode of nutrition is holozoic, that is, by ingestion of food.", True),
                 ("They follow a definite growth pattern and grow into adults of definite shape and size.", True),
                 ("Sexual reproduction is by copulation of male and female followed by embryological "
                  "development.", True),
                 ("They store food reserves mainly as starch.", False)],
                [("a", "b", "c", "e"), ("b", "c", "d", "e"), ("a", "b", "d")], "D",
                "Kingdom Animalia",
                "Animals are heterotrophic, eukaryotic and multicellular, and their cells lack cell walls. They "
                "depend directly or indirectly on plants for food, digest food in an internal cavity and store food "
                "reserves as glycogen or fat. Nutrition is holozoic. They follow a definite growth pattern, and "
                "sexual reproduction is by copulation of male and female followed by embryological development.",
                ["(a), (b), (c), (d) true", "(e) false: animals store glycogen or fat, not starch"],
                why="Options with (e) include a false statement. (a, b, d) leaves out the true statement (c).",
                ncert=ref("BC", "Kingdom Animalia"), secs=50)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Advanced",
                "Which of the following statements about kingdom Monera are correct?",
                [("Cyanobacteria may be unicellular, colonial or filamentous, and may be freshwater, marine or "
                  "terrestrial.", True),
                 ("The colonies of cyanobacteria are generally surrounded by a gelatinous sheath.", True),
                 ("Bacteria reproduce mainly by fission and, under unfavourable conditions, may produce spores.",
                  True),
                 ("Heterotrophic bacteria are helpful in making curd from milk and in fixing nitrogen in legume "
                  "roots.", True),
                 ("Eubacteria are characterised by the absence of a rigid cell wall.", False)],
                [("a", "b", "c", "e"), ("a", "c", "d", "e"), ("b", "c", "d")], "B",
                "Bacteria and cyanobacteria",
                "Cyanobacteria are unicellular, colonial or filamentous, freshwater, marine or terrestrial algae; "
                "their colonies are generally surrounded by a gelatinous sheath. Heterotrophic bacteria help in "
                "making curd from milk, producing antibiotics and fixing nitrogen in legume roots. Bacteria reproduce "
                "mainly by fission and sometimes form spores under unfavourable conditions. True bacteria "
                "(eubacteria) are characterised by the presence of a rigid cell wall and, if motile, a flagellum.",
                ["(a)–(d) true", "(e) false: eubacteria have a rigid cell wall"],
                why="Options with (e) include a false statement. (b, c, d) leaves out the true statement (a).",
                ncert=ref("BC", "Kingdom Monera"), secs=60)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "All fungi are multicellular and filamentous.",
                 "Fungi show a great diversity in morphology and habitat.",
                 False, True, False, "D",
                 "Body form of fungi",
                 "NCERT states that, with the exception of yeasts, which are unicellular, fungi are filamentous. "
                 "So A is false. R is true: the fungi form a unique kingdom of heterotrophic organisms that show a "
                 "great diversity in morphology and habitat.",
                 ["A: false (yeasts are unicellular)", "R: true"],
                 ncert=ref("BC", "Kingdom Fungi"), secs=35)

statement_pair(T_LIV, "Five kingdom classification", "Advanced",
               "Before the five kingdom system, bacteria, blue-green algae, fungi, mosses, ferns, gymnosperms and "
               "angiosperms were all placed under 'Plants'.",
               "Paramoecium and Amoeba, now placed in kingdom Protista, were earlier placed in the animal kingdom "
               "and lack a cell wall.",
               True, True, "A",
               "Two kingdom versus five kingdom classification",
               "The earlier classification placed bacteria, blue-green algae, fungi, mosses, ferns, gymnosperms and "
               "angiosperms under 'Plants', the unifying character being a cell wall. Kingdom Protista brought "
               "together Chlamydomonas and Chlorella (earlier algae within plants, both with cell walls) with "
               "Paramoecium and Amoeba (earlier in the animal kingdom, which lack a cell wall).",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("BC", "Introduction"), secs=45)


# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Gymnosperms", "Basic",
       "The name 'gymnosperm' (Greek gymnos, sperma) refers to plants in which the:",
       "seeds are naked, that is, not covered",
       ["seeds are enclosed within a fruit", "male gametes are naked and swim in water",
        "spores are produced in naked cones without sporophylls"], "C",
       "Gymnosperms",
       "Gymnosperms (gymnos: naked, sperma: seeds) are plants in which the ovules are not enclosed by any ovary "
       "wall and remain exposed, both before and after fertilisation. The seeds that develop after fertilisation are "
       "not covered, that is, they are naked.",
       ["gymnos = naked, sperma = seeds", "Ovules not enclosed by an ovary wall → naked seeds"],
       why="Seeds enclosed in a fruit describe angiosperms. The name refers to seeds, not to male gametes, and the "
           "cones of gymnosperms are made of sporophylls.",
       ncert=ref("PK", "Gymnosperms"), secs=20)

direct(T_PK, "Algae", "Basic",
       "Which of the following is a filamentous alga?",
       "Spirogyra", ["Volvox", "Chlamydomonas", "Chlorella"], "D",
       "Form of algae",
       "The form and size of algae are highly variable, ranging from colonial forms like Volvox to filamentous forms "
       "like Ulothrix and Spirogyra. Chlamydomonas and Chlorella are unicellular green algae.",
       ["Filamentous: Ulothrix, Spirogyra", "Colonial: Volvox", "Unicellular: Chlamydomonas, Chlorella"],
       why="Volvox is NCERT's example of a colonial alga, and Chlamydomonas and Chlorella are unicellular.",
       ncert=ref("PK", "Algae"), secs=20)

statement_pair(T_PK, "Bryophytes", "Basic",
               "In bryophytes, the antherozoids are released into water, where they come in contact with the "
               "archegonium.",
               "In bryophytes, an antherozoid fuses with the egg to produce the zygote.",
               True, True, "A",
               "Fertilisation in bryophytes",
               "The antheridium of a bryophyte produces biflagellate antherozoids. These are released into water, "
               "where they come in contact with the archegonium. An antherozoid fuses with the egg to produce the "
               "zygote, which develops into the sporophyte.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Bryophytes"), secs=30)

direct(T_PK, "Pteridophytes", "Basic",
       "Which of the following is a pteridophyte?",
       "Dryopteris", ["Sphagnum", "Gracilaria", "Cedrus"], "B",
       "Examples of pteridophytes",
       "NCERT lists Selaginella and Lycopodium (Lycopsida), Equisetum (Sphenopsida), and the ferns Dryopteris, Pteris "
       "and Adiantum (Pteropsida) as pteridophytes.",
       ["Dryopteris → fern → pteridophyte"],
       why="Sphagnum is a moss, Gracilaria a red alga and Cedrus a gymnosperm.",
       ncert=ref("PK", "Pteridophytes"), secs=20)

direct(T_PK, "Bryophytes", "Basic",
       "The female sex organ of bryophytes, the archegonium, is:",
       "flask-shaped and produces a single egg",
       ["pear-shaped and produces many biflagellate gametes", "cup-shaped and produces gemmae",
        "sac-like and produces many spores"], "D",
       "Sex organs of bryophytes",
       "The sex organs of bryophytes are multicellular. The male sex organ, the antheridium, produces biflagellate "
       "antherozoids. The female sex organ, the archegonium, is flask-shaped and produces a single egg.",
       ["Antheridium → biflagellate antherozoids", "Archegonium → flask-shaped, single egg"],
       why="Pear-shaped biflagellate cells are the gametes of brown algae. Gemma cups are asexual structures of "
           "liverworts. A sac producing spores is a spore-bearing structure, not a sex organ.",
       ncert=ref("PK", "Bryophytes"), secs=25)

_pk_cells = 24
_pk_mmc, _pk_fg, _pk_embryo = _pk_cells, _pk_cells // 2, _pk_cells
numerical(T_PK, "Gymnosperms", "Intermediate",
          "The cells of the nucellus in the ovule of a gymnosperm have 24 chromosomes each. How many chromosomes will "
          "be present in the megaspore mother cell, in a cell of the female gametophyte and in a cell of the "
          "embryo, respectively?",
          "24, 12 and 24", ["12, 12 and 24", "24, 24 and 24", "24, 12 and 12"], "C",
          (_pk_mmc, _pk_fg, _pk_embryo) == (24, 12, 24),
          "Ploidy in the gymnosperm ovule",
          "The megaspore mother cell is differentiated from one of the cells of the nucellus, so it is diploid (24). "
          "It divides meiotically to form four haploid megaspores; one of them develops into the multicellular "
          "female gametophyte, whose cells are haploid (12). The zygote formed after fertilisation is diploid and "
          "develops into the embryo (24).",
          ["Nucellus cell (2n) = 24 → megaspore mother cell = 24", "Meiosis → megaspore and female gametophyte = 12",
           "Fertilisation → zygote → embryo = 24"],
          "12, 12 and 24 treats the megaspore mother cell as already haploid. 24, 24 and 24 forgets that meiosis "
          "precedes the female gametophyte. 24, 12 and 12 forgets that fertilisation restores the diploid number "
          "in the embryo.",
          ref("PK", "Gymnosperms"), secs=50)

assertion_reason(T_PK, "Gymnosperms", "Intermediate",
                 "The needle-like leaves of conifers help to reduce water loss.",
                 "Needle-like leaves have a reduced surface area.",
                 True, True, True, "A",
                 "Leaves of gymnosperms",
                 "The leaves of gymnosperms are well adapted to withstand extremes of temperature, humidity and wind. "
                 "In conifers, the needle-like leaves reduce the surface area, and their thick cuticle and sunken "
                 "stomata also help to reduce water loss. A smaller surface area directly means less surface for "
                 "water loss, so R explains A.",
                 ["A: true", "R: true", "Less surface area → less water lost → R explains A"],
                 ncert=ref("PK", "Gymnosperms"), secs=35)

statement_pair(T_PK, "Algae", "Intermediate",
               "In Chlorophyceae, asexual reproduction is by flagellated zoospores produced in zoosporangia.",
               "In most members of Chlorophyceae, the storage bodies called pyrenoids are located in the cell wall.",
               True, False, "C",
               "Chlorophyceae",
               "In green algae, asexual reproduction is by flagellated zoospores produced in zoosporangia. Most "
               "members have one or more storage bodies called pyrenoids, located in the chloroplasts; pyrenoids "
               "contain protein besides starch.",
               ["Statement I: true", "Statement II: false, pyrenoids are located in the chloroplasts"],
               ncert=ref("PK", "Algae (Chlorophyceae)"), secs=35)

direct(T_PK, "Gymnosperms", "Intermediate",
       "Which of the following features is shared by pteridophytes and gymnosperms but NOT by bryophytes?",
       "The main plant body is a sporophyte with vascular tissues (xylem and phloem)",
       ["Water is required for the transfer of male gametes to the archegonium",
        "The gametophyte has an independent, free-living existence",
        "Seeds are formed after fertilisation"], "B",
       "Comparison of plant groups",
       "In bryophytes the main plant body is the haploid gametophyte and vascular tissue is absent. Pteridophytes "
       "are the first terrestrial plants to possess xylem and phloem, and in them, as in gymnosperms, the main "
       "plant body is the sporophyte.",
       ["Bryophytes: gametophyte dominant, no vascular tissue", "Pteridophytes and gymnosperms: sporophyte dominant, "
                                                                "vascular tissue present"],
       why="Water for fertilisation and a free-living gametophyte are shared by bryophytes and pteridophytes, not "
           "gymnosperms. Seeds are formed by gymnosperms but not by pteridophytes.",
       ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=40)

statement_pair(T_PK, "Algae", "Intermediate",
               "The cell wall contains cellulose in members of both Phaeophyceae and Rhodophyceae.",
               "Algin and carrageen are hydrocolloids, that is, water-holding substances.",
               True, True, "A",
               "Cell walls and products of algae",
               "Table 3.1 gives the cell wall of Phaeophyceae as cellulose and algin, and that of Rhodophyceae as "
               "cellulose, pectin and polysulphate esters. Certain marine brown and red algae produce large amounts "
               "of hydrocolloids (water-holding substances), e.g., algin (brown algae) and carrageen (red algae), "
               "which are used commercially.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Algae (Table 3.1)"), secs=40)

direct(T_PK, "Algae", "Intermediate",
       "Which of the following is NOT a brown alga?",
       "Gracilaria", ["Dictyota", "Laminaria", "Sargassum"], "D",
       "Examples of algae",
       "NCERT gives Ectocarpus, Dictyota, Laminaria, Sargassum and Fucus as examples of brown algae "
       "(Phaeophyceae). Gracilaria, with Gelidium, is a red alga from which agar is obtained.",
       ["Brown algae: Ectocarpus, Dictyota, Laminaria, Sargassum, Fucus", "Gracilaria → red alga"],
       why="Dictyota, Laminaria and Sargassum are all listed by NCERT as members of Phaeophyceae.",
       ncert=ref("PK", "Algae (Phaeophyceae; Rhodophyceae)"), secs=25)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Members of Chlorophyceae are usually grass green in colour.",
                 "In members of Chlorophyceae, the pigments chlorophyll a and b are dominant.",
                 True, True, True, "A",
                 "Colour of green algae",
                 "NCERT states that members of Chlorophyceae are usually grass green due to the dominance of the "
                 "pigments chlorophyll a and b. The dominant pigments decide the colour, so R explains A.",
                 ["A: true", "R: true", "Dominant chlorophyll a and b → grass green → R explains A"],
                 ncert=ref("PK", "Algae (Chlorophyceae)"), secs=30)

multi_statement(T_PK, "Gymnosperms", "Advanced",
                "Which of the following statements comparing bryophytes, pteridophytes and gymnosperms are "
                "correct?",
                [("Archegonia are formed in all three groups.", True),
                 ("Vascular tissues are present in pteridophytes and gymnosperms but absent in bryophytes.", True),
                 ("Water is required for fertilisation in both bryophytes and pteridophytes.", True),
                 ("A free-living gametophyte is found in all three groups.", False),
                 ("Seeds are formed in both pteridophytes and gymnosperms.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "D",
                "Comparison of bryophytes, pteridophytes and gymnosperms",
                "Archegonia occur in bryophytes, on the prothallus of pteridophytes, and on the female gametophyte "
                "of gymnosperms (two or more per gametophyte). Vascular tissue first appears in pteridophytes. In "
                "bryophytes the antherozoids are released into water, and in pteridophytes water is required to "
                "carry antherozoids to the archegonium. The gametophytes of gymnosperms are not free-living, and "
                "seeds are formed only in gymnosperms.",
                ["(a) true", "(b) true", "(c) true", "(d) false: gymnosperm gametophytes are not free-living",
                 "(e) false: pteridophytes do not form seeds"],
                why="(a, b, d) and (b, c, e) contain a false statement. (a, c) leaves out the true statement (b).",
                ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following algae are correctly matched with their class?",
                [("Laminaria – Phaeophyceae", True),
                 ("Gelidium – Rhodophyceae", True),
                 ("Chara – Chlorophyceae", True),
                 ("Fucus – Rhodophyceae", False),
                 ("Volvox – Phaeophyceae", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c", "d")], "B",
                "Classes of algae",
                "Laminaria and Fucus are brown algae (Phaeophyceae). Gelidium is a red alga (Rhodophyceae). Chara "
                "and Volvox are green algae (Chlorophyceae).",
                ["(a), (b), (c) correct", "(d) wrong: Fucus is a brown alga", "(e) wrong: Volvox is a green alga"],
                why="Every wrong option includes (d) or (e).",
                ncert=ref("PK", "Algae"), secs=45)

assertion_reason(T_PK, "Bryophytes", "Advanced",
                 "Mosses, along with lichens, are of great ecological importance in the colonisation of rocks.",
                 "Mosses decompose rocks, making the substrate suitable for the growth of higher plants.",
                 True, True, True, "A",
                 "Ecological importance of mosses",
                 "Mosses along with lichens are the first organisms to colonise rocks and hence are of great "
                 "ecological importance. They decompose rocks, making the substrate suitable for the growth of "
                 "higher plants. Preparing the rock surface for later plants is the reason for their ecological "
                 "importance, so R explains A.",
                 ["A: true", "R: true", "Rock decomposition prepares the substrate → ecological importance → R "
                                        "explains A"],
                 ncert=ref("PK", "Bryophytes"), secs=40)

statement_pair(T_PK, "Algae", "Advanced",
               "In algae, the most common asexual spores are zoospores, which are flagellated and on germination give "
               "rise to new plants.",
               "Sargassum, a seaweed used as food, belongs to Rhodophyceae.",
               True, False, "C",
               "Reproduction and examples of algae",
               "Algae reproduce asexually by different types of spores, the most common being zoospores, which are "
               "flagellated (motile) and on germination give rise to new plants. Sargassum, like Laminaria, is a "
               "brown alga (Phaeophyceae); many species of Porphyra, Laminaria and Sargassum are used as food.",
               ["Statement I: true", "Statement II: false, Sargassum is a brown alga"],
               ncert=ref("PK", "Algae"), secs=40)

direct(T_PK, "Pteridophytes", "Advanced",
       "In which of the following pairs is the main plant body a sporophyte with true roots, stem and leaves, while "
       "the gametophyte is a small, free-living, photosynthetic thallus?",
       "Adiantum and Equisetum",
       ["Funaria and Marchantia", "Cycas and Pinus", "Chara and Volvox"], "B",
       "Pteridophytes",
       "In pteridophytes the main plant body is a sporophyte differentiated into true root, stem and leaves. Their "
       "spores germinate to give rise to small, multicellular, free-living, mostly photosynthetic thalloid "
       "gametophytes called prothallus. Adiantum (a fern) and Equisetum are pteridophytes.",
       ["Dominant sporophyte + free-living thalloid gametophyte → pteridophytes",
        "Adiantum (Pteropsida) and Equisetum (Sphenopsida)"],
       why="Funaria and Marchantia are bryophytes, whose main plant body is the gametophyte. Cycas and Pinus are "
           "gymnosperms, whose gametophytes are not free-living. Chara and Volvox are green algae.",
       ncert=ref("PK", "Pteridophytes"), secs=40)


# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Flower", "Basic",
       "A flower that cannot be divided into two similar halves by any vertical plane passing through the centre is "
       "called asymmetric (irregular). NCERT's example of such a flower is:",
       "canna", ["mustard", "pea", "datura"], "D",
       "Symmetry of flowers",
       "A flower is actinomorphic when any radial plane through the centre divides it into two similar halves (e.g., "
       "mustard, datura, chilli), zygomorphic when only one particular vertical plane does so (e.g., pea, gulmohur, "
       "bean, Cassia), and asymmetric (irregular) when no vertical plane through the centre does so, as in canna.",
       ["No plane of symmetry → asymmetric → canna"],
       why="Mustard and datura are actinomorphic, and pea is zygomorphic.",
       ncert=ref("MOR", "The Flower"), secs=25)

match_list(T_MOR, "Plant families", "Basic", "member of Solanaceae", "use",
           ["Chilli", "Ashwagandha", "Brinjal", "Petunia"],
           ["Ornamental", "Food", "Spice", "Medicine"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C",
           "Economic importance of Solanaceae",
           "Many plants of Solanaceae are sources of food (tomato, brinjal, potato), spice (chilli), medicine "
           "(belladonna, ashwagandha), fumigatory (tobacco) and ornamentals (petunia).",
           ["Chilli → spice", "Ashwagandha → medicine", "Brinjal → food", "Petunia → ornamental"],
           why="The wrong codes swap chilli with ashwagandha, brinjal with petunia, or ashwagandha with brinjal.",
           ncert=ref("MOR", "Solanaceae (Economic importance)"), secs=30)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In some leguminous plants the leaf base becomes swollen. This swollen leaf base is called the:",
       "pulvinus", ["stipule", "sheath", "rachis"], "B",
       "Parts of a leaf",
       "A typical leaf has a leaf base, a petiole and a lamina. The leaf base may bear two lateral small leaf-like "
       "structures called stipules. In monocotyledons the leaf base expands into a sheath, and in some leguminous "
       "plants the leaf base may become swollen; this is called the pulvinus.",
       ["Swollen leaf base (legumes) → pulvinus"],
       why="Stipules are small leaf-like outgrowths of the leaf base. A sheath is the expanded leaf base of "
           "monocots. The rachis is the common axis of a pinnately compound leaf.",
       ncert=ref("MOR", "The Leaf"), secs=20)

statement_pair(T_MOR, "Root, stem and leaf", "Basic",
               "In parallel venation, the veins run parallel to each other within the lamina.",
               "Leaves of most monocotyledons have reticulate venation.",
               True, False, "C",
               "Venation",
               "The arrangement of veins and veinlets in the lamina is venation. When the veinlets form a network, "
               "the venation is reticulate; when the veins run parallel to each other within the lamina, it is "
               "parallel. Leaves of dicotyledons generally possess reticulate venation, while parallel venation is "
               "characteristic of most monocotyledons.",
               ["Statement I: true", "Statement II: false, most monocots have parallel venation"],
               ncert=ref("MOR", "The Leaf (Venation)"), secs=30)

direct(T_MOR, "Flower", "Basic",
       "The four whorls of a typical flower are arranged successively on the swollen end of the stalk or pedicel. "
       "This swollen end is called the:",
       "thalamus or receptacle", ["placenta", "pulvinus", "peduncle"], "D",
       "Parts of a flower",
       "A typical flower has four whorls, calyx, corolla, androecium and gynoecium, arranged successively on the "
       "swollen end of the stalk or pedicel, called the thalamus or receptacle.",
       ["Swollen end of the pedicel = thalamus (receptacle)"],
       why="The placenta is the cushion-like tissue in the ovary bearing ovules. The pulvinus is a swollen leaf "
           "base. The peduncle is the axis of an inflorescence, not the swollen end of the pedicel.",
       ncert=ref("MOR", "The Flower"), secs=20)

match_list(T_MOR, "Flower", "Intermediate", "type of aestivation", "example",
           ["Valvate", "Twisted", "Imbricate", "Vexillary"],
           ["Bean", "Gulmohur", "Calotropis", "Cotton"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "B",
           "Aestivation",
           "In valvate aestivation, sepals or petals just touch one another at the margins (Calotropis). In twisted "
           "aestivation, one margin of each appendage overlaps the next (china rose, lady's finger, cotton). In "
           "imbricate aestivation, the margins overlap but not in any particular direction (Cassia, gulmohur). In "
           "vexillary aestivation, the large standard overlaps the two wings, which overlap the keel (pea, bean).",
           ["Valvate → Calotropis", "Twisted → cotton", "Imbricate → gulmohur", "Vexillary → bean"],
           why="The wrong codes swap Calotropis with cotton, bean with gulmohur, or cotton with gulmohur.",
           ncert=ref("MOR", "The Flower (Aestivation)"), secs=40)

assertion_reason(T_MOR, "Plant families", "Intermediate",
                 "The family Liliaceae is a characteristic representative of monocotyledonous plants.",
                 "Members of Liliaceae have leaves with reticulate venation.",
                 True, False, False, "C",
                 "Liliaceae",
                 "Liliaceae, commonly called the lily family, is a characteristic representative of monocotyledonous "
                 "plants. Its leaves are mostly basal, alternate, linear and exstipulate, with parallel venation, not "
                 "reticulate.",
                 ["A: true", "R: false, Liliaceae leaves have parallel venation"],
                 ncert=ref("MOR", "Liliaceae"), secs=30)

statement_pair(T_MOR, "Plant families", "Intermediate",
               "In Solanaceae, the corolla has five united petals with valvate aestivation.",
               "In Solanaceae, the placenta is swollen and bears many ovules.",
               True, True, "A",
               "Floral features of Solanaceae",
               "In Solanaceae, the corolla has five united petals with valvate aestivation. The gynoecium is "
               "bicarpellary, obliquely placed and syncarpous; the ovary is superior and bilocular, and the placenta "
               "is swollen with many ovules (axile placentation).",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "Solanaceae (Floral characters)"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "Which of the following members of Fabaceae is named by NCERT as an ornamental plant?",
       "Sweet pea", ["Muliathi", "Sunhemp", "Indigofera"], "B",
       "Economic importance of Fabaceae",
       "Fabaceae members are sources of pulses, edible oil (soyabean, groundnut), dye (Indigofera), fibres "
       "(sunhemp), fodder (Sesbania, Trifolium), ornamentals (lupin, sweet pea) and medicine (muliathi).",
       ["Ornamentals → lupin, sweet pea"],
       why="Muliathi is medicinal, sunhemp gives fibre and Indigofera gives dye.",
       ncert=ref("MOR", "Fabaceae (Economic importance)"), secs=25)

multi_statement(T_MOR, "Flower", "Intermediate",
                "Which of the following statements about flowers are correct?",
                [("A flower having both androecium and gynoecium is bisexual.", True),
                 ("A flower having either only stamens or only carpels is unisexual.", True),
                 ("Mustard and datura have actinomorphic flowers.", True),
                 ("Chilli has zygomorphic flowers.", False),
                 ("Gulmohur and Cassia have zygomorphic flowers.", True)],
                [("a", "b", "c", "d"), ("b", "c", "d", "e"), ("a", "c", "e")], "D",
                "Sex and symmetry of flowers",
                "A flower with both androecium and gynoecium is bisexual; one with either only stamens or only "
                "carpels is unisexual. NCERT gives mustard, datura and chilli as actinomorphic flowers, and pea, "
                "gulmohur, bean and Cassia as zygomorphic flowers.",
                ["(a), (b), (c), (e) true", "(d) false: chilli is actinomorphic"],
                why="Options with (d) include a false statement. (a, c, e) leaves out the true statement (b).",
                ncert=ref("MOR", "The Flower"), secs=45)

statement_pair(T_MOR, "Root, stem and leaf", "Intermediate",
               "The stem is generally green when young and later often becomes woody and dark brown.",
               "The region of the stem where leaves are borne is called the internode.",
               True, False, "C",
               "The stem",
               "The stem bears nodes and internodes. The region of the stem where leaves are borne is the node; the "
               "portion between two nodes is the internode. The stem is generally green when young and later often "
               "becomes woody and dark brown.",
               ["Statement I: true", "Statement II: false, leaves are borne at the nodes"],
               ncert=ref("MOR", "The Stem"), secs=30)

direct(T_MOR, "Fruit and seed", "Intermediate",
       "In the embryo of a dicotyledonous seed, the radicle and the plumule are present at the two ends of the:",
       "embryonal axis", ["cotyledon", "endosperm", "hilum"], "A",
       "Structure of a dicotyledonous seed",
       "The outermost covering of a dicot seed is the seed coat. Within it is the embryo, which consists of an "
       "embryonal axis and two cotyledons. The cotyledons are often fleshy and full of reserve food. At the two ends "
       "of the embryonal axis are present the radicle and the plumule.",
       ["Embryo = embryonal axis + two cotyledons", "Radicle and plumule → two ends of the embryonal axis"],
       why="Cotyledons are attached to the embryonal axis and store food. The endosperm is a separate food-storing "
           "tissue, absent in mature bean, gram and pea seeds. The hilum is a scar on the seed coat.",
       ncert=ref("MOR", "The Seed (Structure of a Dicotyledonous Seed)"), secs=30)

direct(T_MOR, "Root, stem and leaf", "Advanced",
       "In which of the following pairs are BOTH structures modified stems?",
       "Thorns of Citrus and tendrils of grapevine",
       ["Spines of cactus and thorns of Bougainvillea", "Tendrils of pea and tendrils of cucumber",
        "Swollen roots of sweet potato and the underground food-storing organ of ginger"], "D",
       "Homologous modifications of stem",
       "Axillary buds of stems are modified into woody, straight, pointed thorns in Citrus and Bougainvillea. Stem "
       "tendrils, which develop from axillary buds, help gourds (cucumber, pumpkin, watermelon) and grapevines to "
       "climb. In pea the leaves are modified into tendrils, and in cacti the leaves are modified into spines. "
       "Sweet potato stores food in swollen adventitious roots, whereas ginger has an underground stem.",
       ["Citrus thorn → axillary bud (stem)", "Grapevine tendril → stem", "Cactus spine and pea tendril → leaf",
        "Sweet potato → root"],
       why="Cactus spines are leaves (Bougainvillea thorns are stems). Pea tendrils are leaves (cucumber tendrils "
           "are stems). Sweet potato stores food in roots (ginger in a stem).",
       ncert=ref("MOR", "The Stem (Modifications of stem); The Leaf (Modifications of leaves)"), secs=50)

multi_statement(T_MOR, "Root, stem and leaf", "Advanced",
                "Which of the following statements about the stem and the leaf are correct?",
                [("The axillary bud of a leaf later develops into a branch.", True),
                 ("The stem develops from the plumule of the embryo of a germinating seed.", True),
                 ("The primary root develops from the elongation of the plumule.", False),
                 ("Stems of some plants also perform the functions of food storage, support, protection and "
                  "vegetative propagation.", True),
                 ("Leaves originate from the root apical meristem.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "d")], "B",
                "Stem and leaf",
                "A leaf develops at the node and bears a bud in its axil; the axillary bud later develops into a "
                "branch. The stem is the ascending part of the axis and develops from the plumule of the embryo, "
                "while the primary root develops from the elongation of the radicle. Besides spreading out branches "
                "and conducting water and food, some stems store food, give support and protection, and help in "
                "vegetative propagation. Leaves originate from the shoot apical meristem.",
                ["(a) true", "(b) true", "(c) false: the primary root comes from the radicle", "(d) true",
                 "(e) false: leaves come from the shoot apical meristem"],
                why="(a, b, c) and (b, d, e) include a false statement. (a, d) leaves out the true statement (b).",
                ncert=ref("MOR", "The Root; The Stem; The Leaf"), secs=60)

assertion_reason(T_MOR, "Root, stem and leaf", "Advanced",
                 "The thorns of Citrus protect the plant from browsing animals.",
                 "Thorns are hard, woody and sharp-pointed, so browsing animals avoid feeding on the plants that "
                 "bear them.",
                 True, True, True, "A",
                 "Thorns",
                 "Axillary buds of stems may be modified into woody, straight and pointed thorns, as in Citrus and "
                 "Bougainvillea. NCERT states that they protect the plants from browsing animals. Their hard, "
                 "sharp form is what keeps the animals away, so R explains A.",
                 ["A: true", "R: true", "Woody, pointed structures deter browsing → R explains A"],
                 ncert=ref("MOR", "The Stem (Modifications of stem)"), secs=40)

statement_pair(T_MOR, "Plant families", "Advanced",
               "In Fabaceae, the calyx shows imbricate aestivation, whereas the corolla shows vexillary aestivation.",
               "In Fabaceae, the style is single and the seeds are endospermous.",
               True, False, "C",
               "Floral characters of Fabaceae",
               "In Fabaceae the calyx has five gamosepalous sepals with imbricate aestivation, and the corolla has "
               "five polypetalous, papilionaceous petals with vexillary aestivation. The ovary is superior, "
               "monocarpellary and unilocular with many ovules, and the style is single. The fruit is a legume and "
               "the seeds are one to many and non-endospermic.",
               ["Statement I: true", "Statement II: false, Fabaceae seeds are non-endospermic"],
               ncert=ref("MOR", "Fabaceae"), secs=45)

multi_statement(T_MOR, "Fruit and seed", "Advanced",
                "Which of the following statements about fruits and seeds are correct?",
                [("The fruit is a mature or ripened ovary, developed after fertilisation.", True),
                 ("When the pericarp is fleshy, it is differentiated into epicarp, mesocarp and endocarp.", True),
                 ("In mango, the endocarp is stony and hard.", True),
                 ("The pericarp of a fruit is always fleshy.", False),
                 ("The seed is formed after fertilisation and is made up of a seed coat and an embryo.", True)],
                [("a", "b", "c", "d"), ("b", "c", "d", "e"), ("a", "b", "e")], "D",
                "Fruit and seed",
                "The fruit is a characteristic feature of flowering plants: a mature or ripened ovary developed "
                "after fertilisation. It consists of a wall or pericarp and seeds; the pericarp may be dry or "
                "fleshy, and when fleshy it is differentiated into epicarp, mesocarp and endocarp. In mango the "
                "endocarp is stony and hard. The ovules after fertilisation develop into seeds, each made up of a "
                "seed coat and an embryo.",
                ["(a), (b), (c), (e) true", "(d) false: the pericarp may be dry or fleshy"],
                why="Options with (d) include a false statement. (a, b, e) leaves out the true statement (c).",
                ncert=ref("MOR", "The Fruit; The Seed"), secs=50)


# =============================================================== 4. Anatomy of Flowering Plants (4/6/4)
direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "In the transverse section of a dicot root, the outermost layer, many of whose cells protrude as unicellular "
       "root hairs, is the:",
       "epiblema", ["cuticle", "hypodermis", "pericycle"], "B",
       "Dicot root",
       "The outermost layer of a dicot root is the epiblema. Many of its cells protrude in the form of unicellular "
       "root hairs. Inside it lie the cortex, the endodermis, the pericycle and the vascular tissue.",
       ["Outermost layer of the root = epiblema (with root hairs)"],
       why="A cuticle is absent in roots. A hypodermis is described for stems, not roots. The pericycle lies inside "
           "the endodermis.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous Root)"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "The first-formed primary xylem elements are called:",
       "protoxylem", ["metaxylem", "xylem parenchyma", "xylem fibres"], "D",
       "Primary xylem",
       "Primary xylem is of two types. The first-formed primary xylem elements are called protoxylem, and the "
       "later-formed primary xylem is called metaxylem.",
       ["First formed → protoxylem", "Later formed → metaxylem"],
       why="Metaxylem forms later. Xylem parenchyma and xylem fibres are kinds of xylem cells, not names for the "
           "first-formed elements.",
       ncert=ref("ANA", "The Tissues (Xylem)"), secs=20)

statement_pair(T_ANA, "Plant tissues", "Basic",
               "Sclerenchyma cells are usually dead and without protoplasts.",
               "On the basis of variation in form, structure, origin and development, sclerenchyma may be either "
               "fibres or sclereids.",
               True, True, "A",
               "Sclerenchyma",
               "Sclerenchyma consists of long, narrow cells with thick, lignified cell walls having a few or numerous "
               "pits. They are usually dead and without protoplasts. On the basis of variation in form, structure, "
               "origin and development, sclerenchyma may be either fibres or sclereids.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (Simple tissues: Sclerenchyma)"), secs=30)

direct(T_ANA, "Tissue systems", "Basic",
       "Stomata are structures present in the epidermis of leaves. They regulate the process of:",
       "transpiration and gaseous exchange",
       ["conduction of water from roots to leaves", "storage of food and tannins", "secretion of resins and latex"],
       "C",
       "Stomata",
       "Stomata are present in the epidermis of leaves and regulate the process of transpiration and gaseous "
       "exchange. Each stoma is composed of two bean-shaped guard cells that enclose the stomatal pore.",
       ["Stomata → transpiration and gaseous exchange"],
       why="Water is conducted by xylem. Storage of food and tannins is done by parenchyma (e.g., xylem "
           "parenchyma). Resins and latex are stored by phloem parenchyma.",
       ncert=ref("ANA", "The Tissue System (Epidermal Tissue System)"), secs=20)

assertion_reason(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                 "The mesophyll of a leaf carries out photosynthesis.",
                 "Mesophyll cells possess chloroplasts.",
                 True, True, True, "A",
                 "Mesophyll",
                 "The mesophyll, which possesses chloroplasts and carries out photosynthesis, is made up of "
                 "parenchyma. In a dorsiventral leaf it has two types of cells, palisade and spongy parenchyma. "
                 "Photosynthesis takes place in chloroplasts, so their presence explains the photosynthetic role.",
                 ["A: true", "R: true", "Chloroplasts are the site of photosynthesis → R explains A"],
                 ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dorsiventral Leaf)"),
                 secs=30)

direct(T_ANA, "Plant tissues", "Intermediate",
       "Which simple permanent tissue forms the major component within organs?",
       "Parenchyma", ["Collenchyma", "Sclerenchyma", "Xylem"], "D",
       "Parenchyma",
       "The parenchyma forms the major component within organs. Its cells are generally isodiametric, with thin "
       "cellulose walls, and may be closely packed or have small intercellular spaces. It performs functions such "
       "as photosynthesis, storage and secretion.",
       ["Major component within organs → parenchyma"],
       why="Collenchyma occurs in layers below the epidermis of dicots, and sclerenchyma gives mechanical support; "
           "neither is the major component. Xylem is a complex tissue, not a simple one.",
       ncert=ref("ANA", "The Tissues (Simple tissues: Parenchyma)"), secs=25)

match_list(T_ANA, "Dicot and monocot anatomy", "Intermediate", "organ", "feature seen in transverse section",
           ["Dicot root", "Monocot root", "Dicot stem", "Monocot stem"],
           ["Vascular bundles arranged in a ring",
            "Pith large and well developed; usually more than six xylem bundles",
            "Scattered vascular bundles, each surrounded by a sclerenchymatous bundle sheath",
            "Pith small or inconspicuous; two to four xylem and phloem patches"],
           "IV II I III", ["II IV I III", "IV II III I", "I II IV III"], "C",
           "Comparison of roots and stems",
           "In the dicot root the pith is small or inconspicuous and there are two to four xylem and phloem patches. "
           "The monocot root has usually more than six (polyarch) xylem bundles and a large, well-developed pith. In "
           "the dicot stem the vascular bundles are arranged in a ring, which is characteristic. The monocot stem "
           "has a large number of scattered vascular bundles, each surrounded by a sclerenchymatous bundle sheath.",
           ["Dicot root → IV", "Monocot root → II", "Dicot stem → I", "Monocot stem → III"],
           why="The wrong codes swap the two roots (small versus large pith), the two stems (ring versus scattered "
               "bundles), or a root with a stem.",
           ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=45)

statement_pair(T_ANA, "Plant tissues", "Intermediate",
               "In angiosperms, phloem is composed of sieve tube elements, companion cells, phloem parenchyma and "
               "phloem fibres.",
               "Sieve tube elements are long, tube-like structures, arranged longitudinally, and are associated with "
               "the companion cells.",
               True, True, "A",
               "Phloem",
               "Phloem transports food materials, usually from leaves to other parts of the plant. In angiosperms it "
               "is composed of sieve tube elements, companion cells, phloem parenchyma and phloem fibres. Sieve tube "
               "elements are long, tube-like structures, arranged longitudinally and associated with the companion "
               "cells; their end walls form sieve plates.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (Phloem)"), secs=35)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "Which of the following statements about the primary structure of a dicot stem are correct?",
                [("The arrangement of vascular bundles in a ring is characteristic of the dicot stem.", True),
                 ("Each vascular bundle is conjoint and open, with endarch protoxylem.", True),
                 ("The hypodermis consists of a few layers of sclerenchymatous cells.", False),
                 ("The vascular bundles are of the radial type.", False),
                 ("A pith is absent.", False)],
                [("a", "b", "c"), ("a", "d"), ("b", "e")], "C",
                "Dicot stem",
                "In a dicot stem a large number of vascular bundles are arranged in a ring, which is characteristic. "
                "Each bundle is conjoint, open and has endarch protoxylem. The hypodermis is collenchymatous, and a "
                "large central pith of rounded parenchymatous cells with intercellular spaces is present. Radial "
                "bundles are found in roots.",
                ["(a) true", "(b) true", "(c) false: the hypodermis is collenchymatous",
                 "(d) false: radial bundles occur in roots", "(e) false: the pith occupies the centre"],
                why="(a, b, c) includes the false (c). (a, d) and (b, e) each include a false statement and leave out "
                    "a true one.",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous Stem)"),
                secs=45)

direct(T_ANA, "Plant tissues", "Intermediate",
       "According to NCERT, a tissue is a group of cells having:",
       "a common origin and usually performing a common function",
       ["a common function but always a different origin", "the same shape, whatever their origin",
        "the ability to divide throughout the life of the plant"], "B",
       "Definition of a tissue",
       "A tissue is a group of cells having a common origin and usually performing a common function. A plant is "
       "made up of different kinds of tissues, classified as meristematic or permanent according to whether the "
       "cells can divide.",
       ["Tissue = common origin + usually a common function"],
       why="Origin, not shape, defines a tissue, and complex tissues such as xylem contain cells of different "
           "shapes. The ability to divide distinguishes meristematic tissue only.",
       ncert=ref("ANA", "The Tissues"), secs=25)

multi_statement(T_ANA, "Tissue systems", "Advanced",
                "Which of the following are parts of the epidermal tissue system?",
                [("Stomata", True), ("Trichomes", True), ("Root hairs", True), ("Pericycle", False),
                 ("Medullary rays", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c", "d")], "D",
                "Epidermal tissue system",
                "The epidermal tissue system forms the outermost covering of the plant body and comprises the "
                "epidermal cells, stomata and epidermal appendages, the trichomes and hairs. Root hairs are "
                "unicellular elongations of epidermal cells. The pericycle and medullary rays are parenchymatous "
                "parts of the ground tissue system.",
                ["Epidermal: stomata, trichomes, root hairs", "Ground tissue: pericycle, medullary rays"],
                why="Every wrong option includes the pericycle or the medullary rays, which belong to the ground "
                    "tissue system.",
                ncert=ref("ANA", "The Tissue System"), secs=45)

statement_pair(T_ANA, "Plant tissues", "Advanced",
               "When the protoxylem lies towards the centre (pith) and the metaxylem towards the periphery of the "
               "organ, the primary xylem is called endarch, as in stems.",
               "In roots the primary xylem is exarch, with the metaxylem towards the periphery and the protoxylem "
               "towards the centre.",
               True, False, "C",
               "Endarch and exarch xylem",
               "In stems, the protoxylem lies towards the centre (pith) and the metaxylem towards the periphery; this "
               "primary xylem is called endarch. In roots, the protoxylem lies towards the periphery and the "
               "metaxylem towards the centre; this arrangement is called exarch.",
               ["Statement I: true", "Statement II: false, in exarch xylem the protoxylem is towards the periphery"],
               ncert=ref("ANA", "The Tissues (Xylem)"), secs=40)

match_list(T_ANA, "Tissue systems", "Advanced", "cell or tissue", "where it is found",
           ["Albuminous cells", "Bulliform cells", "Subsidiary cells", "Conjunctive tissue"],
           ["Adaxial epidermis of grass leaves, along the veins", "Phloem of gymnosperms",
            "Parenchyma between the xylem and phloem of roots",
            "Epidermal cells in the vicinity of the guard cells"],
           "II I IV III", ["I II IV III", "II I III IV", "II IV I III"], "B",
           "Specialised cells and tissues",
           "Gymnosperms have albuminous cells and sieve cells in their phloem in place of companion cells and sieve "
           "tubes. In grasses, certain adaxial epidermal cells along the veins become large, empty, colourless "
           "bulliform cells. Epidermal cells in the vicinity of the guard cells may become specialised in shape and "
           "size as subsidiary cells. In roots, the parenchymatous cells between the xylem and the phloem are "
           "called conjunctive tissue.",
           ["Albuminous cells → II", "Bulliform cells → I", "Subsidiary cells → IV", "Conjunctive tissue → III"],
           why="The wrong codes interchange albuminous and bulliform cells, subsidiary cells and conjunctive tissue, "
               "or bulliform and subsidiary cells (both epidermal, but only bulliform cells lie along the veins of "
               "grass leaves).",
           ncert=ref("ANA", "The Tissues; The Tissue System; Anatomy of Dicotyledonous and Monocotyledonous Plants"),
           secs=50)

direct(T_ANA, "Plant tissues", "Advanced",
       "In which of the following pairs are BOTH kinds of cells dead at maturity?",
       "Tracheids and phloem fibres",
       ["Xylem parenchyma and vessel members", "Phloem fibres and companion cells", "Tracheids and xylem parenchyma"],
       "B",
       "Living and dead elements of xylem and phloem",
       "Tracheids are dead and without protoplasm, and vessel members are also devoid of protoplasm. Phloem fibres "
       "lose their protoplasm at maturity and become dead. Xylem parenchyma cells are living and thin-walled, and "
       "companion cells are specialised parenchymatous cells with a nucleus that controls the sieve tubes.",
       ["Dead: tracheids, vessel members, xylem fibres, phloem fibres",
        "Living: xylem parenchyma, phloem parenchyma, companion cells"],
       why="Each wrong pair contains a living cell: xylem parenchyma or companion cells.",
       ncert=ref("ANA", "The Tissues (Xylem; Phloem)"), secs=45)


# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Cell envelope and membrane", "Basic",
       "In plants other than algae, the cell wall consists of:",
       "cellulose, hemicellulose, pectins and proteins",
       ["chitin and polysaccharides", "cellulose, galactans, mannans and calcium carbonate",
        "phospholipids and cholesterol only"], "B",
       "Composition of the cell wall",
       "The cell wall of algae is made of cellulose, galactans, mannans and minerals like calcium carbonate, while "
       "in other plants it consists of cellulose, hemicellulose, pectins and proteins.",
       ["Algae: cellulose, galactans, mannans, CaCO₃", "Other plants: cellulose, hemicellulose, pectins, proteins"],
       why="Chitin and polysaccharides make the wall of fungi. Galactans, mannans and calcium carbonate occur in the "
           "algal wall. Lipids are components of membranes, not of the cell wall.",
       ncert=ref("CELL", "Eukaryotic Cells (Cell Wall)"), secs=25)

direct(T_CELL, "Nucleus", "Basic",
       "The nucleolus is a site for the active synthesis of:",
       "ribosomal RNA", ["messenger RNA only", "histone proteins", "lipids"], "C",
       "Nucleolus",
       "The nucleoli are spherical structures present in the nucleoplasm. Their content is continuous with the rest "
       "of the nucleoplasm, as the nucleolus is not membrane-bound. It is a site for active ribosomal RNA synthesis.",
       ["Nucleolus → rRNA synthesis"],
       why="NCERT links the nucleolus only with ribosomal RNA synthesis. Proteins are made on ribosomes, and lipids "
           "mainly in the smooth endoplasmic reticulum.",
       ncert=ref("CELL", "Eukaryotic Cells (Nucleus)"), secs=20)

direct(T_CELL, "Cell theory", "Basic",
       "An onion cell has a distinct cell wall as its outer boundary. What forms the delimiting outer structure of a "
       "cell of the human cheek?",
       "The cell membrane", ["A cell wall", "A glycocalyx and capsule", "The nuclear envelope"], "B",
       "Plant and animal cells",
       "An onion cell, a typical plant cell, has a distinct cell wall as its outer boundary, and just within it is "
       "the cell membrane. The cells of the human cheek have an outer membrane as the delimiting structure of the "
       "cell.",
       ["Onion cell: cell wall outside the cell membrane", "Cheek cell: cell membrane is the outer boundary"],
       why="Animal cells lack a cell wall. The glycocalyx and capsule belong to the bacterial cell envelope. The "
           "nuclear envelope surrounds only the nucleus.",
       ncert=ref("CELL", "An Overview of Cell"), secs=20)

statement_pair(T_CELL, "Cell theory", "Basic",
               "The eukaryotes include all the protists, plants, animals and fungi.",
               "In eukaryotic cells there is an extensive compartmentalisation of the cytoplasm through membrane-"
               "bound organelles.",
               True, True, "A",
               "Eukaryotic cells",
               "The eukaryotes include all the protists, plants, animals and fungi. In eukaryotic cells there is an "
               "extensive compartmentalisation of the cytoplasm through the presence of membrane-bound organelles, "
               "and they possess an organised nucleus with a nuclear envelope.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells"), secs=30)

match_list(T_CELL, "Endomembrane system", "Basic", "component of the endomembrane system", "feature",
           ["Golgi apparatus", "Smooth endoplasmic reticulum", "Rough endoplasmic reticulum", "Lysosome"],
           ["Membrane-bound vesicle rich in hydrolytic enzymes, formed by packaging in the Golgi apparatus",
            "Bears ribosomes on its outer surface", "Major site for the synthesis of lipids",
            "Packages materials to be delivered to intracellular targets or secreted outside the cell"],
           "IV III II I", ["III IV II I", "IV II III I", "IV III I II"], "D",
           "Endomembrane system",
           "The Golgi apparatus principally performs the function of packaging materials, to be delivered either to "
           "intracellular targets or secreted outside the cell. The ER bearing ribosomes on its outer surface is the "
           "rough ER; the smooth ER is the major site for synthesis of lipids. Lysosomes are membrane-bound "
           "vesicles formed by packaging in the Golgi apparatus and are rich in hydrolytic enzymes.",
           ["Golgi → IV", "SER → III", "RER → II", "Lysosome → I"],
           why="The wrong codes swap the Golgi apparatus with the smooth ER, the two kinds of ER, or the rough ER "
               "with the lysosome.",
           ncert=ref("CELL", "Eukaryotic Cells (Endomembrane System)"), secs=35)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                 "Mitochondria are called the 'power houses' of the cell.",
                 "Mitochondria are the sites of aerobic respiration and produce cellular energy in the form of ATP.",
                 True, True, True, "A",
                 "Mitochondria",
                 "NCERT states that mitochondria are the sites of aerobic respiration; they produce cellular energy in "
                 "the form of ATP, hence they are called the 'power houses' of the cell. R gives the reason for the "
                 "name.",
                 ["A: true", "R: true", "ATP production → 'power house' → R explains A"],
                 ncert=ref("CELL", "Eukaryotic Cells (Mitochondria)"), secs=30)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "The cell wall gives shape to the plant cell and protects it from mechanical damage and infection.",
               "The cell wall is a living, flexible structure.",
               True, False, "C",
               "Cell wall",
               "A non-living rigid structure called the cell wall forms an outer covering for the plasma membrane of "
               "fungi and plants. It gives shape to the cell, protects it from mechanical damage and infection, "
               "helps in cell-to-cell interaction and provides a barrier to undesirable macromolecules.",
               ["Statement I: true", "Statement II: false, the cell wall is non-living and rigid"],
               ncert=ref("CELL", "Eukaryotic Cells (Cell Wall)"), secs=30)

direct(T_CELL, "Prokaryotic cell", "Intermediate",
       "Which surface structures of bacteria do NOT play a role in motility?",
       "Pili and fimbriae", ["Flagella", "The filament and hook", "The basal body of the flagellum"], "D",
       "Surface structures of bacteria",
       "Motile bacterial cells have thin filamentous extensions called flagella, each made of a filament, a hook "
       "and a basal body. Besides flagella, pili and fimbriae are also surface structures of bacteria, but they do "
       "not play a role in motility.",
       ["Flagellum (filament, hook, basal body) → motility", "Pili and fimbriae → not for motility"],
       why="The filament, hook and basal body are the three parts of the bacterial flagellum, the organ of motility.",
       ncert=ref("CELL", "Prokaryotic Cells (Cell Envelope and its Modifications)"), secs=25)

multi_statement(T_CELL, "Nucleus", "Intermediate",
                "Which of the following statements about the nucleus are correct?",
                [("The nuclear matrix (nucleoplasm) contains the nucleolus and the chromatin.", True),
                 ("Chromatin contains DNA, basic proteins called histones, some non-histone proteins and also RNA.",
                  True),
                 ("The nuclear envelope forms a barrier between the materials inside the nucleus and those of the "
                  "cytoplasm.", True),
                 ("The nucleolus is bounded by a double membrane.", False),
                 ("Molecules move through the nuclear pores only from the nucleus to the cytoplasm.", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c")], "B",
                "Structure of the nucleus",
                "The nuclear envelope of two parallel membranes forms a barrier between the nucleus and the "
                "cytoplasm; its pores allow movement of RNA and protein molecules in both directions. The nuclear "
                "matrix contains the nucleolus and chromatin. The nucleolus is not membrane-bound. Chromatin contains "
                "DNA, histones, some non-histone proteins and RNA.",
                ["(a), (b), (c) true", "(d) false: the nucleolus has no membrane",
                 "(e) false: movement through pores is in both directions"],
                why="(a, b, d) and (a, c, e) include a false statement. (b, c) leaves out the true statement (a).",
                ncert=ref("CELL", "Eukaryotic Cells (Nucleus)"), secs=50)

statement_pair(T_CELL, "Prokaryotic cell", "Intermediate",
               "In prokaryotes, the genetic material is basically naked, not enveloped by a nuclear membrane.",
               "Besides helping in cell wall formation and DNA replication, mesosomes help in respiration and "
               "secretion and increase the surface area of the plasma membrane and its enzymatic content.",
               True, True, "A",
               "Prokaryotic cells",
               "In prokaryotes the genetic material is basically naked, not enveloped by a nuclear membrane. "
               "Mesosomes, formed by extensions of the plasma membrane into the cell as vesicles, tubules and "
               "lamellae, help in cell wall formation, DNA replication and distribution to daughter cells, "
               "respiration and secretion, and increase the surface area of the plasma membrane and its enzymatic "
               "content.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Prokaryotic Cells"), secs=40)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
               "The outer membrane of a mitochondrion forms the continuous limiting boundary of the organelle.",
               "The outer and inner membranes of a mitochondrion carry identical sets of enzymes.",
               True, False, "C",
               "Mitochondrial membranes",
               "Each mitochondrion is a double-membrane-bound structure. The outer membrane forms the continuous "
               "limiting boundary of the organelle, and the inner membrane forms infoldings called cristae towards "
               "the matrix. The two membranes have their own specific enzymes associated with mitochondrial "
               "function.",
               ["Statement I: true", "Statement II: false, each membrane has its own specific enzymes"],
               ncert=ref("CELL", "Eukaryotic Cells (Mitochondria)"), secs=35)

direct(T_CELL, "Prokaryotic cell", "Intermediate",
       "The bacterial cell envelope is a tightly bound three-layered structure. Which option gives its layers in "
       "order from the outside inwards?",
       "Glycocalyx, cell wall, plasma membrane",
       ["Cell wall, glycocalyx, plasma membrane", "Plasma membrane, cell wall, glycocalyx",
        "Glycocalyx, plasma membrane, cell wall"], "B",
       "Prokaryotic cell envelope",
       "Most prokaryotic cells, particularly bacteria, have a chemically complex cell envelope made of a tightly "
       "bound three-layered structure: the outermost glycocalyx, followed by the cell wall and then the plasma "
       "membrane. Each layer has a distinct function, but together they act as a single protective unit.",
       ["Outside → inside: glycocalyx → cell wall → plasma membrane"],
       why="The glycocalyx is the outermost layer and the plasma membrane the innermost; every other order "
           "misplaces one of them.",
       ncert=ref("CELL", "Prokaryotic Cells (Cell Envelope and its Modifications)"), secs=25)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                "Which of the following are found in a eukaryotic plant cell but NOT in a prokaryotic cell?",
                [("Nuclear envelope", True), ("Mitochondria", True), ("Golgi apparatus", True),
                 ("Ribosomes", False), ("Plasma membrane", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "D",
                "Prokaryotic and eukaryotic cells",
                "Prokaryotic cells have no well-defined nucleus and no membrane-bound organelles; eukaryotic cells "
                "have a nuclear envelope and organelles such as mitochondria and the Golgi apparatus. The plasma "
                "membrane and ribosomes (70S in prokaryotes, 80S in the eukaryotic cytoplasm) are found in both.",
                ["Only in eukaryotes: nuclear envelope, mitochondria, Golgi apparatus",
                 "In both: ribosomes, plasma membrane"],
                why="Every wrong option includes ribosomes or the plasma membrane, which prokaryotes also have.",
                ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells"), secs=45)

assertion_reason(T_CELL, "Cell envelope and membrane", "Advanced",
                 "Polar molecules need a carrier protein of the membrane to be transported across the plasma "
                 "membrane.",
                 "Polar molecules cannot pass through the non-polar lipid bilayer.",
                 True, True, True, "A",
                 "Transport of polar molecules",
                 "NCERT states that, as polar molecules cannot pass through the non-polar lipid bilayer, they require "
                 "a carrier protein of the membrane to facilitate their transport across the membrane. R is the "
                 "cause of A.",
                 ["A: true", "R: true", "Non-polar bilayer blocks polar molecules → carrier protein needed → R "
                                        "explains A"],
                 ncert=ref("CELL", "Eukaryotic Cells (Cell Membrane)"), secs=40)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
               "Both chloroplasts and chromoplasts contain carotenoid pigments.",
               "Leucoplasts are colourless plastids that may store starch (amyloplasts), oils and fats "
               "(elaioplasts) or proteins (aleuroplasts).",
               True, True, "A",
               "Types of plastids",
               "Chloroplasts contain chlorophyll and carotenoid pigments, which trap light energy for photosynthesis. "
               "In chromoplasts, fat-soluble carotenoid pigments such as carotene and xanthophylls give the plastid "
               "a yellow, orange or red colour. Leucoplasts are colourless plastids of varied shapes and sizes with "
               "stored nutrients: amyloplasts store starch, elaioplasts oils and fats, and aleuroplasts proteins.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (Plastids)"), secs=45)

direct(T_CELL, "Prokaryotic cell", "Advanced",
       "A cell has a cell wall, 70S ribosomes, naked genomic DNA without a nuclear membrane, membranous "
       "chromatophores containing pigments, and cyanophycean granules as inclusion bodies. This cell most likely "
       "belongs to:",
       "a cyanobacterium", ["Chlamydomonas", "yeast", "Mycoplasma"], "C",
       "Identifying a prokaryotic cell",
       "Naked DNA without a nuclear membrane and 70S ribosomes mark a prokaryote. Membranous extensions with "
       "pigments (chromatophores) are found in prokaryotes such as cyanobacteria, and cyanophycean granules are "
       "among the inclusion bodies of prokaryotic cells. A cell wall rules out Mycoplasma.",
       ["Naked DNA + 70S ribosomes → prokaryote", "Chromatophores → cyanobacteria",
        "Cell wall present → not Mycoplasma"],
       why="Chlamydomonas and yeast are eukaryotes with a nucleus and 80S cytoplasmic ribosomes. Mycoplasma is a "
           "prokaryote that completely lacks a cell wall.",
       ncert=ref("CELL", "Prokaryotic Cells"), secs=45)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
       "Which structure has no surrounding membrane, is present in both prokaryotic and eukaryotic cells, and in a "
       "plant cell occurs in the cytoplasm as well as inside chloroplasts and mitochondria?",
       "Ribosome", ["Nucleolus", "Centriole", "Mesosome"], "D",
       "Ribosomes",
       "Ribosomes are composed of RNA and proteins and are not surrounded by any membrane. They occur in "
       "prokaryotes (70S) and in the eukaryotic cytoplasm (80S), and 70S ribosomes are also found in the stroma of "
       "chloroplasts and the matrix of mitochondria.",
       ["Non-membranous + in prokaryotes + in chloroplasts and mitochondria → ribosome"],
       why="The nucleolus has no membrane but is absent in prokaryotes. Centrioles are absent in prokaryotes and in "
           "almost all plant cells. Mesosomes are infoldings of the prokaryotic plasma membrane, not found in "
           "plant cells.",
       ncert=ref("CELL", "Eukaryotic Cells (Ribosomes; Mitochondria; Plastids)"), secs=40)


# =============================================================== 6. Cell Cycle and Cell Division (4/6/4)
direct(T_CC, "Mitosis", "Basic",
       "When karyokinesis is not followed by cytokinesis, a multinucleate condition arises, as in the liquid "
       "endosperm of coconut. This leads to the formation of a:",
       "syncytium", ["dyad of cells", "bivalent", "cell plate"], "D",
       "Cytokinesis",
       "In some organisms karyokinesis is not followed by cytokinesis, so a multinucleate condition arises, leading "
       "to the formation of a syncytium (e.g., the liquid endosperm in coconut).",
       ["Nuclear division without cytoplasmic division → multinucleate → syncytium"],
       why="A dyad is the pair of cells formed at the end of meiosis I. A bivalent is a pair of synapsed homologous "
           "chromosomes. The cell plate is the precursor of the new wall in plant cytokinesis.",
       ncert=ref("CC", "M Phase (Cytokinesis)"), secs=20)

direct(T_CC, "Meiosis", "Basic",
       "The stage between the two meiotic divisions is called:",
       "interkinesis", ["interphase", "diakinesis", "cytokinesis"], "C",
       "Stages of meiosis",
       "After telophase I, cytokinesis forms a dyad of cells. The stage between the two meiotic divisions is called "
       "interkinesis; it is generally short-lived and is followed by prophase II.",
       ["Between meiosis I and meiosis II → interkinesis"],
       why="Interphase is the preparatory phase before a division. Diakinesis is the last stage of prophase I. "
           "Cytokinesis is division of the cytoplasm.",
       ncert=ref("CC", "Meiosis (Meiosis I: Telophase I)"), secs=20)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "The duration of the cell cycle can vary from organism to organism and also from cell type to cell "
               "type.",
               "During the division of a cell, DNA replication and cell growth also take place.",
               True, True, "A",
               "The cell cycle",
               "Cell division is a very important process in all living organisms. During the division of a cell, DNA "
               "replication and cell growth also take place, and these processes must be coordinated. The duration "
               "of the cell cycle can vary from organism to organism and also from cell type to cell type; for "
               "example, yeast takes about 90 minutes and a human cell in culture about 24 hours.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Cell Cycle"), secs=30)

direct(T_CC, "Meiosis", "Basic",
       "Which stage of meiotic prophase I represents the transition to metaphase I?",
       "Diakinesis", ["Pachytene", "Zygotene", "Diplotene"], "B",
       "Prophase I",
       "Diakinesis is marked by terminalisation of chiasmata. The chromosomes are fully condensed and the meiotic "
       "spindle is assembled; by the end of diakinesis the nucleolus disappears and the nuclear envelope breaks "
       "down. Diakinesis represents the transition to metaphase.",
       ["Order: leptotene → zygotene → pachytene → diplotene → diakinesis → metaphase I"],
       why="Zygotene, pachytene and diplotene come before diakinesis, so none of them leads directly into "
           "metaphase I.",
       ncert=ref("CC", "Meiosis (Prophase I)"), secs=20)

_cc_2n = 16
_cc_centromeres, _cc_kinetochores = _cc_2n, 2 * _cc_2n
numerical(T_CC, "Mitosis", "Intermediate",
          "A plant cell with 2n = 16 is at metaphase of mitosis. Every chromosome has one centromere, and on its "
          "sides lie the disc-shaped kinetochores by which the two sister chromatids attach to spindle fibres from "
          "opposite poles. How many centromeres and how many kinetochores are present in the cell?",
          "16 centromeres and 32 kinetochores",
          ["16 centromeres and 16 kinetochores", "32 centromeres and 32 kinetochores",
           "8 centromeres and 16 kinetochores"], "D",
          (_cc_centromeres, _cc_kinetochores) == (16, 32),
          "Centromeres and kinetochores at metaphase",
          "At metaphase each of the 16 chromosomes consists of two sister chromatids held together by one "
          "centromere. Kinetochores lie on the sides of the centromere, one for each sister chromatid, so that the "
          "chromatids attach to spindle fibres from opposite poles. Centromeres = 16; kinetochores = 16 × 2 = 32.",
          ["Centromeres = number of chromosomes = 16", "Kinetochores = 2 per chromosome = 32"],
          "16 kinetochores ignores that each sister chromatid has its own kinetochore. 32 centromeres counts "
          "chromatids as chromosomes (the centromeres split only in anaphase). 8 and 16 halves the number as if the "
          "cell were in meiosis II.",
          ref("CC", "M Phase (Metaphase)"), secs=60)

_cc_cycle_h, _cc_m_h = 24, 1
_cc_inter_h = _cc_cycle_h - _cc_m_h
numerical(T_CC, "Cell cycle phases", "Intermediate",
          "A human cell in culture divides once in about 24 hours, and its M phase lasts about 1 hour. How long does "
          "its interphase last, and roughly what percentage of the cell cycle is this?",
          "23 hours, about 96 per cent",
          ["1 hour, about 4 per cent", "22 hours, about 92 per cent", "24 hours, 100 per cent"], "B",
          _cc_inter_h == 23 and round(100 * _cc_inter_h / _cc_cycle_h) == 96,
          "Duration of interphase",
          "The cell cycle has two basic phases, interphase and M phase. Interphase = 24 − 1 = 23 hours, which is "
          "23/24 ≈ 96 per cent of the cycle, consistent with NCERT's statement that interphase lasts more than 95 "
          "per cent of the duration of the cell cycle.",
          ["Interphase = 24 − 1 = 23 h", "23/24 × 100 ≈ 95.8 ≈ 96 per cent"],
          "1 hour (4 per cent) is the M phase, not interphase. 22 hours subtracts 2 hours instead of 1. 24 hours "
          "ignores the M phase altogether.",
          ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=45)

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "At metaphase of mitosis, the chromosomes come to lie aligned on the metaphase plate.",
                 "The nuclear envelope remains intact throughout metaphase.",
                 True, False, False, "C",
                 "Metaphase",
                 "The complete disintegration of the nuclear envelope marks the start of metaphase, so the chromosomes "
                 "are spread through the cytoplasm. Spindle fibres attach to the kinetochores, and the chromosomes are "
                 "moved to the spindle equator and aligned along the metaphase plate. R is false.",
                 ["A: true", "R: false, the nuclear envelope has disintegrated by the start of metaphase"],
                 ncert=ref("CC", "M Phase (Metaphase)"), secs=35)

multi_statement(T_CC, "Meiosis", "Intermediate",
                "Which of the following events take place both in mitosis and in meiosis I?",
                [("Condensation of chromosomes", True),
                 ("Breakdown of the nuclear envelope", True),
                 ("Assembly of the spindle", True),
                 ("Synapsis of homologous chromosomes", False),
                 ("Splitting of centromeres and separation of sister chromatids", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c", "d", "e")], "B",
                "Comparison of mitosis and meiosis I",
                "In both divisions the chromosomes condense, the nuclear envelope breaks down and a spindle is "
                "assembled. Synapsis of homologous chromosomes (zygotene) occurs only in meiosis I. In anaphase I "
                "the homologues separate while the sister chromatids remain associated at their centromeres; the "
                "centromeres split only in mitotic anaphase and anaphase II.",
                ["(a), (b), (c) common", "(d) only meiosis I", "(e) mitosis and meiosis II, not meiosis I"],
                why="Every wrong option includes (d) or (e).",
                ncert=ref("CC", "M Phase; Meiosis"), secs=50)

match_list(T_CC, "Cell cycle phases", "Intermediate", "phase", "feature",
           ["G0", "G1", "S", "G2"],
           ["Cell is metabolically active and grows continuously but does not replicate its DNA",
            "DNA replication takes place; in animal cells the centriole duplicates in the cytoplasm",
            "Proteins are synthesised in preparation for mitosis while cell growth continues",
            "Cell remains metabolically active but no longer proliferates unless called on to do so"],
           "IV I II III", ["I IV II III", "IV I III II", "IV II I III"], "C",
           "Phases of the cell cycle",
           "G1 is the interval between mitosis and initiation of DNA replication; the cell is metabolically active "
           "and grows but does not replicate DNA. In S phase DNA is replicated, and in animal cells the centriole "
           "duplicates in the cytoplasm. In G2, proteins are synthesised in preparation for mitosis while growth "
           "continues. Cells that exit G1 enter the quiescent G0 stage, where they remain metabolically active but "
           "do not proliferate unless called on.",
           ["G0 → IV", "G1 → I", "S → II", "G2 → III"],
           why="The wrong codes swap G0 with G1 (both lack DNA synthesis, but only G1 cells grow towards division), "
               "S with G2, or G1 with S.",
           ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=45)

statement_pair(T_CC, "Mitosis", "Intermediate",
               "In prophase, the initiation of the assembly of the mitotic spindle takes place, with the help of "
               "microtubules, the proteinaceous components of the cytoplasm.",
               "At metaphase, the chromosomes are spread through the cytoplasm, and their condensation is complete.",
               True, True, "A",
               "Prophase and metaphase",
               "Prophase is marked by condensation of chromosomes and the initiation of the assembly of the mitotic "
               "spindle, helped by microtubules. With the complete disintegration of the nuclear envelope at the "
               "start of metaphase, the chromosomes are spread through the cytoplasm; by this stage their "
               "condensation is completed and they can be observed clearly.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "M Phase (Prophase; Metaphase)"), secs=40)

_cc2_2n = 20
_ai_chr, _ai_cht = _cc2_2n // 2, _cc2_2n
_aii_chr, _aii_cht = _cc2_2n // 2, _cc2_2n // 2
numerical(T_CC, "Meiosis", "Advanced",
          "A meiocyte of a plant with 2n = 20 undergoes meiosis. How many chromosomes, and how many chromatids, move "
          "to each pole at anaphase I and at anaphase II?",
          "Anaphase I: 10 chromosomes with 20 chromatids; anaphase II: 10 chromosomes with 10 chromatids",
          ["Anaphase I: 20 chromosomes with 20 chromatids; anaphase II: 10 chromosomes with 10 chromatids",
           "Anaphase I: 10 chromosomes with 10 chromatids; anaphase II: 5 chromosomes with 5 chromatids",
           "Anaphase I: 10 chromosomes with 20 chromatids; anaphase II: 5 chromosomes with 10 chromatids"], "D",
          (_ai_chr, _ai_cht, _aii_chr, _aii_cht) == (10, 20, 10, 10),
          "Chromosome movement in meiosis",
          "In anaphase I the homologous chromosomes separate while sister chromatids stay together, so 10 "
          "chromosomes, each with two chromatids (20 chromatids), go to each pole. In anaphase II the centromeres "
          "split and the sister chromatids of these 10 chromosomes separate, so 10 chromosomes, each a single "
          "chromatid, go to each pole.",
          ["Anaphase I: 20 ÷ 2 = 10 chromosomes × 2 chromatids = 20", "Anaphase II: centromeres split → 10 "
                                                                       "single-chromatid chromosomes per pole"],
          "20 chromosomes at anaphase I assumes sister chromatids separate in meiosis I. Halving again to 5 at "
          "anaphase II treats meiosis II as a second reduction; it separates chromatids, not homologues.",
          ref("CC", "Meiosis (Anaphase I; Anaphase II)"), secs=90)

statement_pair(T_CC, "Significance", "Advanced",
               "Many cells in adult animals divide only occasionally, as needed to replace cells lost because of "
               "injury or cell death.",
               "In adult animals, heart cells divide continuously to replace damaged cells.",
               True, False, "C",
               "Cell division in adult animals",
               "Some cells in adult animals do not appear to exhibit division (e.g., heart cells), and many other "
               "cells divide only occasionally, as needed to replace cells that have been lost because of injury or "
               "cell death. Such non-dividing cells exit G1 and enter the quiescent G0 stage.",
               ["Statement I: true", "Statement II: false, heart cells do not appear to divide"],
               ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=40)

multi_statement(T_CC, "Cell cycle phases", "Advanced",
                "Which of the following take place during the S phase of the cell cycle?",
                [("Replication of DNA", True),
                 ("Increase in the DNA content of the cell from 2C to 4C", True),
                 ("Doubling of the number of chromosomes", False),
                 ("Duplication of the centriole in the cytoplasm of animal cells", True),
                 ("Breakdown of the nuclear envelope", False)],
                [("a", "b", "c"), ("a", "b", "d", "e"), ("b", "c", "d")], "D",
                "S phase",
                "S (synthesis) phase marks the period of DNA synthesis or replication. The amount of DNA per cell "
                "doubles from 2C to 4C, but there is no increase in the chromosome number. In animal cells, the "
                "centriole duplicates in the cytoplasm during S phase. The nuclear envelope breaks down later, in M "
                "phase.",
                ["(a), (b), (d) true", "(c) false: chromosome number does not change",
                 "(e) false: the nuclear envelope breaks down in M phase"],
                why="Every wrong option includes (c) or (e).",
                ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=50)

match_list(T_CC, "Meiosis", "Advanced", "cell or nucleus of a diploid organism", "chromosome condition",
           ["Cell in G1 phase", "Cell in G2 phase", "Cell at metaphase II", "Nucleus at telophase II"],
           ["n chromosomes, each with one chromatid", "2n chromosomes, each with two chromatids",
            "2n chromosomes, each with one chromatid", "n chromosomes, each with two chromatids"],
           "III II IV I", ["II III IV I", "III II I IV", "I II IV III"], "A",
           "Chromosome number and chromatids through the cycle",
           "In G1 a diploid cell has 2n single-chromatid chromosomes. After DNA replication in S phase, the G2 cell "
           "still has 2n chromosomes, each now with two chromatids. Meiosis I halves the number, so at metaphase II "
           "each cell has n chromosomes, each still with two chromatids. Anaphase II separates the chromatids, so a "
           "telophase II nucleus has n single-chromatid chromosomes.",
           ["G1 → III", "G2 → II", "Metaphase II → IV", "Telophase II → I"],
           why="The wrong codes swap G1 with G2 (chromosome number does not change in S phase, only the chromatids), "
               "metaphase II with telophase II, or G1 with telophase II.",
           ncert=ref("CC", "Cell Cycle; Meiosis"), secs=60)


# =============================================================== 7. Photosynthesis (5/6/5)
direct(T_PS, "Site and pigments", "Basic",
       "In the stroma of the chloroplast, enzymatic reactions incorporate CO₂ and lead to the synthesis of sugar. "
       "This sugar in turn forms:",
       "starch", ["cellulose", "glycogen", "protein"], "A",
       "Division of labour in the chloroplast",
       "Within the chloroplast there is a clear division of labour. The membrane system traps light energy and "
       "synthesises ATP and NADPH. In the stroma, enzymatic reactions synthesise sugar, which in turn forms starch.",
       ["Membrane system → ATP and NADPH", "Stroma → sugar → starch"],
       why="NCERT names starch as the product formed from the sugar in the stroma. Glycogen is the storage form in "
           "animals, and cellulose and protein are not what the sugar is described as forming.",
       ncert=ref("PS", "Where does Photosynthesis take place?"), secs=20)

direct(T_PS, "Site and pigments", "Basic",
       "NCERT gives two reasons why photosynthesis is important. They are that it is:",
       "the primary source of all food on earth, and responsible for the release of oxygen into the atmosphere",
       ["the only process that releases CO₂, and the only source of water for plants",
        "the main source of ATP for roots, and the process that breaks down glucose",
        "the source of nitrogen for proteins, and the process that fixes oxygen"], "B",
       "Importance of photosynthesis",
       "Photosynthesis is important for two reasons: it is the primary source of all food on earth, and it is "
       "responsible for the release of oxygen into the atmosphere by green plants.",
       ["Food for all life + atmospheric O₂"],
       why="Photosynthesis consumes CO₂ and water rather than supplying them. Breakdown of glucose to make ATP is "
           "respiration. Nitrogen is not obtained through photosynthesis.",
       ncert=ref("PS", "Introduction"), secs=25)

statement_pair(T_PS, "Site and pigments", "Basic",
               "Photosynthesis takes place in green leaves and also in other green parts of the plant.",
               "The mesophyll cells of leaves have a large number of chloroplasts.",
               True, True, "A",
               "Site of photosynthesis",
               "Photosynthesis takes place in the green leaves of plants, but also in other green parts of the "
               "plant. The mesophyll cells in the leaves have a large number of chloroplasts, which usually align "
               "themselves along the walls of the mesophyll cells.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Where does Photosynthesis take place?"), secs=25)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "The large cells around the vascular bundles of plants with the C4 pathway are called:",
       "bundle sheath cells", ["mesophyll cells", "guard cells", "companion cells"], "B",
       "Kranz anatomy",
       "The large cells around the vascular bundles of C4 plants are called bundle sheath cells, and leaves with "
       "such anatomy are said to have 'Kranz' anatomy. Bundle sheath cells may form several layers around the "
       "vascular bundles.",
       ["Large cells around vascular bundles of C4 leaves → bundle sheath cells → Kranz anatomy"],
       why="Mesophyll cells lie outside the bundle sheath. Guard cells surround the stomatal pore, and companion "
           "cells are part of the phloem.",
       ncert=ref("PS", "The C4 Pathway"), secs=20)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "In the Z scheme, what happens to the electrons as they pass from photosystem II through the electron "
       "transport chain?",
       "They are not used up but are passed on to the pigments of photosystem I",
       ["They are used up in splitting water", "They are passed directly to NADP⁺ without reaching PS I",
        "They are returned to the reaction centre of PS II"], "D",
       "Electron transport in the light reaction",
       "Electrons excited in the reaction centre of PS II are picked up by an acceptor and passed through an "
       "electron transport system of cytochromes. They are not used up as they pass through the chain, but are "
       "passed on to the pigments of PS I, whose excited electrons finally reduce NADP⁺.",
       ["PS II → ETS (cytochromes) → PS I → NADP⁺"],
       why="Water splitting supplies electrons to PS II; it does not consume them. NADP⁺ is reduced by electrons "
           "from PS I. Return of electrons to the same photosystem is the cyclic flow around PS I, not PS II.",
       ncert=ref("PS", "The Electron Transport"), secs=30)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Intermediate",
               "The sugar-synthesising reactions of the stroma are not directly light driven but depend on the "
               "products of the light reactions.",
               "Because they are called dark reactions, these reactions occur only in darkness.",
               True, False, "C",
               "Light and dark reactions",
               "The reactions in the stroma are not directly light driven but depend on ATP and NADPH from the light "
               "reactions. By convention they are called dark reactions (carbon reactions) to distinguish them. "
               "NCERT cautions that this should not be construed to mean that they occur in darkness or that they "
               "are not light-dependent.",
               ["Statement I: true", "Statement II: false, the name does not mean they occur in darkness"],
               ncert=ref("PS", "Where does Photosynthesis take place?"), secs=35)

statement_pair(T_PS, "Limiting factors", "Intermediate",
               "At low light intensities, there is a linear relationship between incident light and the rate of "
               "CO₂ fixation.",
               "At higher light intensities, the rate gradually stops increasing because other factors become "
               "limiting.",
               True, True, "A",
               "Light as a factor",
               "There is a linear relationship between incident light and CO₂ fixation rates at low light "
               "intensities. At higher light intensities, the rate gradually does not show further increase as "
               "other factors become limiting.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Factors affecting Photosynthesis (Light)"), secs=35)

assertion_reason(T_PS, "Chemiosmosis", "Intermediate",
                 "The protons produced by the splitting of water accumulate within the lumen of the thylakoids.",
                 "The splitting of water takes place on the inner side of the thylakoid membrane.",
                 True, True, True, "A",
                 "Proton gradient in chloroplasts",
                 "The water-splitting complex is associated with PS II, which is physically located on the inner side "
                 "of the thylakoid membrane. Since water is split on the inner side, the protons (hydrogen ions) "
                 "produced accumulate within the lumen. This is one of the causes of the proton gradient across the "
                 "thylakoid membrane.",
                 ["A: true", "R: true", "Water split on the lumen side → protons released into the lumen → R "
                                        "explains A"],
                 ncert=ref("PS", "The Electron Transport (Splitting of Water); Where are the ATP and NADPH Used? "
                              "(Chemiosmotic Hypothesis)"), secs=40)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following statements about the products of the light reaction are correct?",
                [("ATP is formed in the light reaction and used in the biosynthetic phase.", True),
                 ("NADPH is formed in the light reaction and used in the biosynthetic phase.", True),
                 ("O₂ formed in the light reaction diffuses out of the chloroplast.", True),
                 ("CO₂ is one of the products of the light reaction.", False),
                 ("RuBP is consumed in the light reaction.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "D",
                "Products of the light reaction",
                "ATP, NADPH and O₂ are the products of the light reaction. O₂ diffuses out of the chloroplast, while "
                "ATP and NADPH are used to drive the processes leading to the synthesis of food (the biosynthetic "
                "phase). CO₂ is a reactant fixed in the stroma, and RuBP is used in the Calvin cycle.",
                ["(a), (b), (c) true", "(d) false: CO₂ is fixed, not produced", "(e) false: RuBP belongs to the "
                                                                               "Calvin cycle"],
                why="Every wrong option includes (d) or (e).",
                ncert=ref("PS", "Where are the ATP and NADPH Used?"), secs=45)

direct(T_PS, "Chemiosmosis", "Intermediate",
       "According to the chemiosmotic hypothesis, the energy released during electron transport in the chloroplast "
       "is used to:",
       "pump protons across the membrane, creating a high concentration of protons in the thylakoid lumen",
       ["directly phosphorylate ADP without any proton gradient", "split water molecules in the stroma",
        "reduce CO₂ to sugar inside the lumen"], "D",
       "Chemiosmosis",
       "Chemiosmosis requires a membrane, a proton pump, a proton gradient and ATP synthase. Energy is used to pump "
       "protons across the membrane to create a gradient, a high concentration of protons within the thylakoid "
       "lumen. Protons then diffuse back across the membrane through the ATP synthase, releasing enough energy to "
       "activate the enzyme that catalyses ATP formation.",
       ["Electron transport energy → proton pumping → gradient", "Gradient breakdown through ATP synthase → ATP"],
       why="ATP synthesis in chloroplasts is linked to the proton gradient. Water is split on the inner (lumen) "
           "side. CO₂ is reduced in the stroma by the Calvin cycle.",
       ncert=ref("PS", "Where are the ATP and NADPH Used? (Chemiosmotic Hypothesis)"), secs=35)

direct(T_PS, "Light reactions and photophosphorylation", "Intermediate",
       "Which of the following takes place in both cyclic and non-cyclic photophosphorylation?",
       "Synthesis of ATP",
       ["Splitting of water", "Release of oxygen", "Reduction of NADP⁺ to NADPH + H⁺"], "B",
       "Cyclic and non-cyclic photophosphorylation",
       "In non-cyclic photophosphorylation, PS II and PS I work in series; water is split, O₂ is released, and both "
       "ATP and NADPH + H⁺ are made. In cyclic photophosphorylation only PS I works; the electron is cycled back to "
       "PS I, and only ATP is synthesised.",
       ["Cyclic → ATP only", "Non-cyclic → ATP + NADPH + O₂", "Common → ATP"],
       why="Water splitting, O₂ release and NADP⁺ reduction happen only in the non-cyclic flow.",
       ncert=ref("PS", "The Electron Transport (Cyclic and Non-cyclic Photo-phosphorylation)"), secs=30)

_ps_co2 = 6
_ps_red_atp, _ps_reg_atp, _ps_nadph = 2 * _ps_co2, 1 * _ps_co2, 2 * _ps_co2
numerical(T_PS, "Calvin cycle and C4 pathway", "Advanced",
          "In the Calvin cycle, for every CO₂ fixed, the reduction stage uses 2 ATP and 2 NADPH, and the "
          "regeneration of RuBP uses 1 ATP. For the synthesis of one molecule of glucose, how many ATP molecules are "
          "used in the reduction stage and how many in the regeneration stage?",
          "12 ATP in reduction and 6 ATP in regeneration",
          ["6 ATP in reduction and 12 ATP in regeneration", "12 ATP in reduction and 12 ATP in regeneration",
           "2 ATP in reduction and 1 ATP in regeneration"], "C",
          (_ps_red_atp, _ps_reg_atp) == (12, 6) and _ps_red_atp + _ps_reg_atp == 18 and _ps_nadph == 12,
          "ATP use in the stages of the Calvin cycle",
          "One glucose needs six CO₂ fixed, that is, six turns of the cycle. Reduction uses 2 ATP per CO₂ → 2 × 6 = 12 "
          "ATP (with 2 × 6 = 12 NADPH). Regeneration uses 1 ATP per CO₂ → 6 ATP. Total 18 ATP, matching NCERT's 18 "
          "ATP and 12 NADPH per glucose.",
          ["CO₂ per glucose = 6", "Reduction: 2 × 6 = 12 ATP", "Regeneration: 1 × 6 = 6 ATP (total 18)"],
          "6 and 12 swaps the two stages. 12 and 12 confuses the regeneration ATP with the 12 NADPH. 2 and 1 gives "
          "the cost per CO₂, not per glucose.",
          ref("PS", "The Calvin Cycle"), secs=60)

assertion_reason(T_PS, "Photorespiration", "Advanced",
                 "In C3 plants, the rate of CO₂ fixation is decreased in the presence of oxygen.",
                 "In C3 plants some O₂ binds to RuBisCO, so some RuBP is oxygenated instead of being carboxylated.",
                 True, True, True, "A",
                 "Photorespiration",
                 "The active site of RuBisCO can bind both CO₂ and O₂. NCERT states that in C3 plants some O₂ does "
                 "bind to RuBisCO, and hence CO₂ fixation is decreased: RuBP that binds O₂ forms one molecule of PGA "
                 "and phosphoglycolate instead of two molecules of PGA. R is the direct cause of A.",
                 ["A: true", "R: true", "O₂ competes for RuBisCO → less RuBP carboxylated → R explains A"],
                 ncert=ref("PS", "Photorespiration"), secs=40)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Advanced",
               "In cyclic photophosphorylation, only PS I is functional and the electron is circulated within the "
               "photosystem.",
               "In cyclic photophosphorylation, water is split by PS I, releasing oxygen.",
               True, False, "C",
               "Cyclic photophosphorylation",
               "In cyclic photophosphorylation only PS I is functional; the excited electron is cycled back to the "
               "PS I complex through the electron transport chain, and only ATP is formed. The water-splitting "
               "complex is associated with PS II, so water is not split and no oxygen is released in the cyclic "
               "flow.",
               ["Statement I: true", "Statement II: false, water splitting is associated with PS II"],
               ncert=ref("PS", "The Electron Transport (Cyclic and Non-cyclic Photo-phosphorylation; Splitting of "
                               "Water)"), secs=45)

match_list(T_PS, "Chemiosmosis", "Advanced", "event", "location",
           ["Fixation of CO₂ by PEP carboxylase in a C4 plant",
            "Release of CO₂ from the C4 acid in a C4 plant",
            "Accumulation of protons from the splitting of water",
            "Probable site of cyclic photophosphorylation"],
           ["Stroma lamellae", "Thylakoid lumen", "Bundle sheath cells", "Mesophyll cells"],
           "IV III II I", ["III IV II I", "IV III I II", "II III IV I"], "D",
           "Where the events of photosynthesis occur",
           "In C4 plants, PEP carboxylase in the mesophyll cells fixes CO₂ into OAA; the C4 acid is carried to the "
           "bundle sheath cells, where it is broken down to release CO₂ for the Calvin cycle. Water is split on the "
           "inner side of the thylakoid membrane, so its protons accumulate in the lumen. The stroma lamellae lack "
           "PS II and NADP reductase and are the probable site of cyclic photophosphorylation.",
           ["PEPcase fixation → mesophyll (IV)", "C4 acid breakdown → bundle sheath (III)",
            "Protons from water → lumen (II)", "Cyclic photophosphorylation → stroma lamellae (I)"],
           why="The wrong codes swap the two C4 cell types, the lumen with the stroma lamellae, or the mesophyll "
               "with the lumen.",
           ncert=ref("PS", "The C4 Pathway; The Electron Transport; Where are the ATP and NADPH Used?"), secs=55)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                "Which of the following statements about the C4 pathway are correct?",
                [("Atmospheric CO₂ is first fixed by PEP carboxylase in the mesophyll cells, and the CO₂ later "
                  "released in the bundle sheath cells is fixed again by RuBisCO.", True),
                 ("The 3-carbon molecule left after decarboxylation is converted back to PEP in the bundle sheath "
                  "cells.", False),
                 ("The C4 acid is converted to malic acid or aspartic acid, which is transported to the bundle "
                  "sheath cells.", True),
                 ("The bundle sheath cells lack PEP carboxylase.", True),
                 ("The mesophyll cells carry out the Calvin cycle.", False)],
                [("a", "b", "c"), ("a", "d", "e"), ("b", "c", "d")], "B",
                "The C4 pathway",
                "In the mesophyll cells PEP carboxylase fixes CO₂ into OAA, which forms malic or aspartic acid that "
                "is transported to the bundle sheath cells. There it is broken down to release CO₂ and a 3-carbon "
                "molecule; the CO₂ enters the Calvin pathway, catalysed by RuBisCO, which is abundant in the bundle "
                "sheath. The 3-carbon molecule is transported back to the mesophyll and converted to PEP there. "
                "Bundle sheath cells lack PEPcase, and mesophyll cells lack RuBisCO, so they do not run the Calvin "
                "cycle.",
                ["(a) true", "(b) false: PEP is regenerated in the mesophyll", "(c) true", "(d) true",
                 "(e) false: the Calvin cycle runs in the bundle sheath"],
                why="Every wrong option includes (b) or (e).",
                ncert=ref("PS", "The C4 Pathway"), secs=60)


# =============================================================== 8. Respiration in Plants (4/5/4)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "In plants, sucrose, the end product of photosynthesis, is converted into glucose and fructose before "
       "glycolysis. The enzyme that brings about this conversion is:",
       "invertase", ["hexokinase", "pyruvic dehydrogenase", "citrate synthase"], "C",
       "Entry of sucrose into glycolysis",
       "In plants, glucose for glycolysis is derived from sucrose or from storage carbohydrates. Sucrose is "
       "converted into glucose and fructose by the enzyme invertase, and these two monosaccharides readily enter "
       "the glycolytic pathway, where hexokinase phosphorylates them.",
       ["Sucrose → glucose + fructose (invertase)", "Glucose → glucose-6-phosphate (hexokinase)"],
       why="Hexokinase phosphorylates glucose; it does not split sucrose. Pyruvic dehydrogenase converts pyruvate to "
           "acetyl CoA, and citrate synthase forms citric acid in the TCA cycle.",
       ncert=ref("RES", "Glycolysis"), secs=20)

direct(T_RES, "Glycolysis and fermentation", "Basic",
       "Most cells of a plant have at least a part of their surface in contact with air. NCERT says this is also "
       "facilitated by:",
       "the loose packing of parenchyma cells, which provides an interconnected network of air spaces",
       ["specialised respiratory organs in the roots", "transport of oxygen from the leaves to other parts through "
                                                       "the xylem",
        "the thick cuticle that covers the roots"], "B",
       "Gas exchange in plants",
       "In large, bulky plants the living cells are located close to the surface; in stems they are organised in "
       "thin layers inside and beneath the bark, which has openings called lenticels. Most cells thus have part of "
       "their surface in contact with air, and this is facilitated by the loose packing of parenchyma cells in "
       "leaves, stems and roots, which provide an interconnected network of air spaces.",
       ["Living cells near the surface + lenticels + loosely packed parenchyma with air spaces"],
       why="Plants have no specialised respiratory organs, there is very little transport of gases from one part "
           "to another, and roots have no cuticle.",
       ncert=ref("RES", "Do Plants Breathe?"), secs=25)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Basic",
               "Glucose is the favoured substrate for respiration.",
               "Fats have to be broken down into glycerol and fatty acids before they can be used as respiratory "
               "substrates.",
               True, True, "A",
               "Respiratory substrates",
               "Glucose is the favoured substrate for respiration, and all carbohydrates are usually first converted "
               "into glucose. Other substrates can also be respired, but not through the first step: fats would need "
               "to be broken down into glycerol and fatty acids first.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Amphibolic Pathway"), secs=25)

direct(T_RES, "TCA cycle", "Basic",
       "In the TCA cycle, the conversion of succinyl CoA to succinic acid is accompanied by the synthesis of a "
       "molecule of GTP. This mode of synthesis of a high-energy phosphate is called:",
       "substrate level phosphorylation",
       ["oxidative phosphorylation", "photophosphorylation", "oxidative decarboxylation"], "D",
       "Substrate level phosphorylation",
       "During the conversion of succinyl CoA to succinic acid a molecule of GTP is synthesised; this is a "
       "substrate level phosphorylation. In a coupled reaction, GTP is converted to GDP with the simultaneous "
       "synthesis of ATP from ADP.",
       ["Succinyl CoA → succinic acid + GTP → substrate level phosphorylation"],
       why="Oxidative phosphorylation uses the proton gradient made by the ETS. Photophosphorylation uses light. "
           "Oxidative decarboxylation removes CO₂ and does not form GTP.",
       ncert=ref("RES", "Tricarboxylic Acid Cycle"), secs=25)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "When cells are photosynthesising, the availability of oxygen for their respiration is not a "
                 "problem.",
                 "Oxygen is released within these cells during photosynthesis.",
                 True, True, True, "A",
                 "Oxygen supply in photosynthesising cells",
                 "During photosynthesis large volumes of gases are exchanged, and the leaf is well adapted for these "
                 "periods. NCERT notes that when cells photosynthesise, availability of O₂ is not a problem in these "
                 "cells since O₂ is released within the cell. R is the reason for A.",
                 ["A: true", "R: true", "O₂ produced inside the cell → no shortage → R explains A"],
                 ncert=ref("RES", "Do Plants Breathe?"), secs=35)

assertion_reason(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
                 "The respiratory pathway comes into the picture both during the breakdown and during the synthesis "
                 "of fatty acids.",
                 "Fatty acids are degraded to acetyl CoA before entering the pathway, and acetyl CoA is withdrawn "
                 "from the pathway when the organism needs to synthesise fatty acids.",
                 True, True, True, "A",
                 "Amphibolic pathway",
                 "Fatty acids used as respiratory substrates are degraded to acetyl CoA and enter the pathway. When "
                 "the organism needs to synthesise fatty acids, acetyl CoA is withdrawn from the respiratory pathway. "
                 "Acetyl CoA links both processes, so R explains why the pathway takes part in both breakdown "
                 "(catabolism) and synthesis (anabolism); hence it is called amphibolic.",
                 ["A: true", "R: true", "Acetyl CoA used in both directions → R explains A"],
                 ncert=ref("RES", "Amphibolic Pathway"), secs=40)

multi_statement(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
                "Which of the following statements about the entry of substrates other than glucose into the "
                "respiratory pathway are correct?",
                [("Fatty acids are degraded to acetyl CoA and then enter the pathway.", True),
                 ("Proteins are first degraded by proteases into individual amino acids.", True),
                 ("After deamination, amino acids enter the pathway at some stage within the Krebs cycle or as "
                  "pyruvate or acetyl CoA, depending on their structure.", True),
                 ("Amino acids enter the pathway without any deamination.", False),
                 ("Fats enter the pathway directly, without being broken down.", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c", "d", "e")], "D",
                "Entry of other substrates",
                "Fats are first broken down into glycerol and fatty acids; fatty acids are degraded to acetyl CoA, "
                "and glycerol enters after conversion to PGAL. Proteins are degraded by proteases, and the individual "
                "amino acids, after deamination, enter at some stage within the Krebs cycle or as pyruvate or acetyl "
                "CoA, depending on their structure.",
                ["(a), (b), (c) true", "(d) false: amino acids are deaminated first",
                 "(e) false: fats are broken down first"],
                why="Every wrong option includes (d) or (e).",
                ncert=ref("RES", "Amphibolic Pathway"), secs=50)

match_list(T_RES, "Glycolysis and fermentation", "Intermediate", "conversion of pyruvic acid or acetyl CoA",
           "enzyme(s)",
           ["Pyruvic acid to lactic acid", "Pyruvic acid to CO₂ and ethanol", "Pyruvic acid to acetyl CoA",
            "Acetyl CoA and oxaloacetic acid to citric acid"],
           ["Citrate synthase", "Pyruvic dehydrogenase", "Lactate dehydrogenase",
            "Pyruvic acid decarboxylase and alcohol dehydrogenase"],
           "III IV II I", ["IV III II I", "III IV I II", "II IV III I"], "B",
           "Fates of pyruvic acid",
           "Under anaerobic conditions in muscle and some bacteria, pyruvic acid is reduced to lactic acid by lactate "
           "dehydrogenase. In yeast, pyruvic acid decarboxylase and alcohol dehydrogenase convert it to CO₂ and "
           "ethanol. In aerobic respiration, pyruvic dehydrogenase carries out its oxidative decarboxylation to "
           "acetyl CoA, and citrate synthase condenses the acetyl group with oxaloacetic acid and water to form "
           "citric acid.",
           ["Lactic acid → lactate dehydrogenase", "Ethanol → pyruvic acid decarboxylase + alcohol dehydrogenase",
            "Acetyl CoA → pyruvic dehydrogenase", "Citric acid → citrate synthase"],
           why="The wrong codes swap the two fermentation enzymes, the link-reaction enzyme with citrate synthase, or "
               "lactate dehydrogenase with pyruvic dehydrogenase.",
           ncert=ref("RES", "Fermentation; Aerobic Respiration; Tricarboxylic Acid Cycle"), secs=45)

statement_pair(T_RES, "Glycolysis and fermentation", "Intermediate",
               "Both lactic acid fermentation and alcoholic fermentation are hazardous processes, since either acid "
               "or alcohol is produced.",
               "In fermentation, all the energy released from glucose is trapped as high-energy bonds of ATP.",
               True, False, "C",
               "Fermentation",
               "In both lactic acid and alcohol fermentation not much energy is released; less than seven per cent of "
               "the energy in glucose is released, and not all of it is trapped as high-energy bonds of ATP. The "
               "processes are also hazardous, since either acid or alcohol is produced.",
               ["Statement I: true", "Statement II: false, not all of the released energy is trapped as ATP"],
               ncert=ref("RES", "Fermentation"), secs=35)

multi_statement(T_RES, "Glycolysis and fermentation", "Advanced",
                "Which of the following statements about gas exchange in plants are correct?",
                [("In large, bulky plants, the living cells are located close to the surface of the plant.", True),
                 ("Cells in the interior of thick, woody stems are dead and provide only mechanical support.",
                  True),
                 ("Large volumes of gases are exchanged only during photosynthesis, and the leaf is well adapted to "
                  "take care of the needs during these periods.", True),
                 ("Plants transport large volumes of oxygen from the leaves to the roots through the xylem.", False),
                 ("Roots, stems and leaves respire at rates much higher than those of animals.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "D",
                "Do plants breathe?",
                "Plants have no specialised organs for gaseous exchange. Each plant part takes care of its own needs, "
                "and there is very little transport of gases from one part to another. Roots, stems and leaves respire "
                "at rates far lower than animals do; only during photosynthesis are large volumes of gases "
                "exchanged, and the leaf is well adapted for this. In bulky plants the living cells are near the "
                "surface, and the cells in the interior are dead and provide only mechanical support.",
                ["(a), (b), (c) true", "(d) false: very little gas is transported between plant parts",
                 "(e) false: plants respire at far lower rates"],
                why="Every wrong option includes (d) or (e).",
                ncert=ref("RES", "Do Plants Breathe?"), secs=50)

assertion_reason(T_RES, "Electron transport system", "Advanced",
                 "The continued oxidation of acetyl CoA in the TCA cycle depends on the working of the electron "
                 "transport system.",
                 "The TCA cycle requires the continued regeneration of NAD⁺ and FAD⁺ from NADH and FADH₂, and they "
                 "are oxidised back in the electron transport system.",
                 True, True, True, "A",
                 "Link between the TCA cycle and the ETS",
                 "The continued oxidation of acetyl CoA via the TCA cycle requires the continued replenishment of "
                 "oxaloacetic acid and the regeneration of NAD⁺ and FAD⁺ from NADH and FADH₂. NADH and FADH₂ are "
                 "oxidised through the electron transport system, which passes the electrons to O₂. Without the ETS "
                 "there would be no NAD⁺ and FAD⁺ for the cycle, so R explains A.",
                 ["A: true", "R: true", "ETS regenerates NAD⁺ and FAD⁺ needed by the cycle → R explains A"],
                 ncert=ref("RES", "Tricarboxylic Acid Cycle; Electron Transport System (ETS) and Oxidative "
                                  "Phosphorylation"), secs=45)

statement_pair(T_RES, "TCA cycle", "Advanced",
               "In eukaryotic plant cells, photosynthesis takes place within the chloroplasts, whereas the breakdown "
               "of complex molecules to yield energy takes place in the cytoplasm and in the mitochondria.",
               "In aerobic respiration, the pyruvic acid formed in glycolysis is oxidised completely in the "
               "cytoplasm.",
               True, False, "C",
               "Sites of respiration",
               "Photosynthesis takes place within the chloroplasts of eukaryotic cells, whereas the breakdown of "
               "complex molecules to yield energy takes place in the cytoplasm and in the mitochondria. Glycolysis "
               "occurs in the cytoplasm, but for aerobic respiration the pyruvate is transported from the cytoplasm "
               "into the mitochondria, where its complete oxidation takes place in the matrix.",
               ["Statement I: true", "Statement II: false, pyruvate is oxidised in the mitochondrial matrix"],
               ncert=ref("RES", "Introduction; Aerobic Respiration"), secs=40)

direct(T_RES, "TCA cycle", "Advanced",
       "Which of the following steps takes place in aerobic respiration but NOT in alcoholic fermentation?",
       "Oxidative decarboxylation of pyruvic acid to acetyl CoA by pyruvic dehydrogenase",
       ["Phosphorylation of glucose to glucose-6-phosphate by hexokinase",
        "Formation of NADH + H⁺ when PGAL is oxidised to BPGA",
        "Formation of ATP when PEP is converted to pyruvic acid"], "B",
       "Aerobic respiration versus fermentation",
       "Glycolysis is common to aerobic respiration and fermentation: hexokinase phosphorylates glucose, NADH is "
       "formed when PGAL is oxidised to BPGA, and ATP is formed when PEP becomes pyruvic acid. Only in aerobic "
       "respiration does pyruvic acid enter the mitochondrial matrix and undergo oxidative decarboxylation to "
       "acetyl CoA by pyruvic dehydrogenase. In alcoholic fermentation, pyruvic acid decarboxylase and alcohol "
       "dehydrogenase form CO₂ and ethanol instead.",
       ["Glycolytic steps → common", "Pyruvic dehydrogenase (link reaction) → aerobic only"],
       why="The other three steps belong to glycolysis, which occurs in both aerobic respiration and fermentation.",
       ncert=ref("RES", "Glycolysis; Fermentation; Aerobic Respiration"), secs=45)

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
    assert pkg["output"] == "batches/parts/BATCH_005_BOT_p1.json"


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
           "notes": "Package BOT_005_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 125 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
