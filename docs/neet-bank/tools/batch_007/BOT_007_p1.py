"""Writes batches/parts/BATCH_007_BOT_p1.json: package BOT_007_p1 of batch 7 (Botany, 125 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_001501 .. NEET_BOT_001625.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books (secondary growth, taxonomical aids, plant life cycles and alternation of generations, early
experiments on photosynthesis) is not used. Facts already tested in batches 1-6 were listed with
`merge_batch.py stems 007 BOT_007_p1` and avoided; where a topic is saturated, questions test new combinations,
comparisons or applications. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_007/BOT_007_p1.py
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
PLAN = ROOT / "batches" / "plans" / "BATCH_007_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_007_BOT_p1.json"
PACKAGE = "BOT_007_p1"
BATCH = "BATCH_007"
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
       "The naming system in which every organism is given a name with two components, a generic name and a "
       "specific epithet, was given by:",
       "Carolus Linnaeus",
       ["R.H. Whittaker", "Aristotle", "M.W. Beijerinek"], "B",
       "Origin of binomial nomenclature",
       "Each scientific name has two components, the generic name and the specific epithet. This system of providing "
       "a name with two components is called binomial nomenclature. It was given by Carolus Linnaeus and is practised "
       "by biologists all over the world.",
       ["Two-component naming = binomial nomenclature", "Given by Carolus Linnaeus"],
       why="Whittaker proposed the five kingdom classification; Aristotle made the earliest attempt at a scientific "
           "basis of classification (trees, shrubs, herbs); Beijerinek worked on the tobacco mosaic virus.",
       ncert=ref("LW", "Diversity in the Living World (binomial nomenclature)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Some fungi live as symbionts. The symbiotic association of a fungus with the roots of higher plants is "
       "called:",
       "mycorrhiza",
       ["a lichen", "a root nodule", "a basidiocarp"], "C",
       "Fungi as symbionts",
       "Fungi are heterotrophic. Most are saprophytes and some are parasites. They can also live as symbionts: in "
       "association with algae as lichens, and with the roots of higher plants as mycorrhiza.",
       ["Fungus + alga = lichen", "Fungus + roots of higher plants = mycorrhiza"],
       why="A lichen is a fungus-alga association. Root nodules of legumes contain nitrogen-fixing bacteria. A "
           "basidiocarp is a fruiting body of basidiomycetes, not an association.",
       ncert=ref("BC", "Kingdom Fungi"), secs=20)

match_list(T_LIV, "Lichens, viruses and viroids", "Basic", "disease", "kind of causal agent",
           ["Citrus canker", "Potato spindle tuber disease", "Bovine spongiform encephalopathy (mad cow disease)",
            "Herpes"],
           ["Virus", "Prion", "Bacterium", "Viroid"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "D",
           "Causal agents of diseases",
           "Citrus canker is named by NCERT as a bacterial disease. The viroid discovered by T.O. Diener was found to "
           "be the causal agent of potato spindle tuber disease. Bovine spongiform encephalopathy (mad cow disease) "
           "in cattle is caused by a prion. Herpes, like mumps, small pox and influenza, is caused by a virus.",
           ["Citrus canker → bacterium", "Potato spindle tuber → viroid", "BSE → prion", "Herpes → virus"],
           why="The wrong codes swap the bacterium and the viroid, the prion and the virus, or the viroid and the "
               "prion.",
           ncert=ref("BC", "Kingdom Monera; Viruses, Viroids, Prions and Lichens"), secs=35)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "The genus Panthera (lion, tiger, leopard) and the genus Felis (cats) are placed together in the family:",
       "Felidae",
       ["Canidae", "Hominidae", "Muscidae"], "A",
       "Family as a taxonomic category",
       "A family is a group of related genera with still fewer similarities than genus and species. Among animals, "
       "the genus Panthera (lion, tiger, leopard) and the genus Felis (cats) are put in the family Felidae. The cat "
       "family Felidae is distinguished from the dog family Canidae on the basis of vegetative and reproductive "
       "features.",
       ["Panthera + Felis → family Felidae"],
       why="Canidae is the dog family. Hominidae is the family of man and Muscidae that of the housefly.",
       ncert=ref("LW", "Taxonomic Categories (family)"), secs=20)

statement_pair(T_LIV, "What is living", "Basic",
               "In plants, growth by cell division occurs continuously throughout their life span.",
               "Unicellular organisms also grow by cell division.",
               True, True, "A",
               "Growth by cell division",
               "Increase in mass and increase in number of individuals are twin characteristics of growth. A "
               "multicellular organism grows by cell division. In plants this growth by cell division occurs "
               "continuously throughout their life span; in animals it is seen only up to a certain age. "
               "Unicellular organisms also grow by cell division.",
               ["Statement I: true, plant growth by cell division is lifelong",
                "Statement II: true"],
               ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=30)

direct(T_LIV, "Taxonomy and hierarchy", "Intermediate",
       "In the NCERT table of organisms with their taxonomic categories, which organism is placed in the order "
       "Poales?",
       "Wheat",
       ["Mango", "Housefly", "Man"], "D",
       "Order of organisms in NCERT's table",
       "NCERT's table places wheat (Triticum aestivum) in family Poaceae, order Poales, class Monocotyledonae and "
       "division Angiospermae. Mango is in order Sapindales, the housefly in order Diptera and man in order "
       "Primata.",
       ["Wheat: Poaceae → Poales", "Mango: Sapindales; housefly: Diptera; man: Primata"],
       why="Mango (Sapindales), housefly (Diptera) and man (Primata) are in other orders.",
       ncert=ref("LW", "Taxonomic Categories (Table 1.1)"), secs=25)

match_list(T_LIV, "Taxonomy and hierarchy", "Intermediate", "organism", "class in NCERT's table",
           ["Man", "Housefly", "Mango", "Wheat"],
           ["Insecta", "Monocotyledonae", "Mammalia", "Dicotyledonae"],
           "III I IV II", ["III I II IV", "I III IV II", "IV I III II"], "B",
           "Classes in NCERT's table of taxonomic categories",
           "In the NCERT table, man (Homo sapiens) is in class Mammalia, the housefly (Musca domestica) in class "
           "Insecta, mango (Mangifera indica) in class Dicotyledonae and wheat (Triticum aestivum) in class "
           "Monocotyledonae.",
           ["Man → Mammalia", "Housefly → Insecta", "Mango → Dicotyledonae", "Wheat → Monocotyledonae"],
           why="The wrong codes interchange the two plant classes, or man and the housefly, or a plant and an "
               "animal class.",
           ncert=ref("LW", "Taxonomic Categories (Table 1.1)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "When red dinoflagellates such as Gonyaulax multiply very rapidly, other marine animals such as "
                 "fishes may be killed.",
                 "Toxins are released by the dinoflagellates present in such large numbers.",
                 True, True, True, "A",
                 "Red tides and their effect",
                 "Some dinoflagellates, e.g. Gonyaulax, undergo such rapid multiplication that they make the sea "
                 "appear red (red tides). Toxins released by such large numbers may even kill other marine animals "
                 "such as fishes. So the toxins are the direct cause of the death of fishes.",
                 ["A: true", "R: true, and the toxins are what kill the fishes"],
                 ncert=ref("BC", "Kingdom Protista (Dinoflagellates)"), secs=35)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "A group of fungi grows in soil, on logs and tree stumps, and in living plant bodies as parasites. Asexual "
       "spores are generally not found, but vegetative reproduction by fragmentation is common. Sex organs are "
       "absent, and plasmogamy takes place by fusion of two somatic cells of different strains. Which pair consists "
       "only of fungi of this group?",
       "Ustilago and Puccinia",
       ["Neurospora and Claviceps", "Mucor and Albugo", "Alternaria and Trichoderma"], "C",
       "Identifying basidiomycetes",
       "The features listed are those of basidiomycetes: they grow in soil, on logs and tree stumps and in living "
       "plant bodies as parasites (rusts and smuts); asexual spores are generally not found but fragmentation is "
       "common; sex organs are absent and plasmogamy is by fusion of somatic cells of different strains. Agaricus "
       "(mushroom), Ustilago (smut) and Puccinia (rust fungus) are examples.",
       ["No asexual spores, no sex organs, somatic plasmogamy → basidiomycetes",
        "Examples: Agaricus, Ustilago, Puccinia"],
       why="Neurospora and Claviceps are ascomycetes; Mucor and Albugo are phycomycetes; Alternaria and Trichoderma "
           "are deuteromycetes.",
       ncert=ref("BC", "Kingdom Fungi (Basidiomycetes)"), secs=45)

numerical(T_LIV, "Five kingdom classification", "Intermediate",
          "In Whittaker's table of the characteristics of the five kingdoms, in how many kingdoms is a cell wall "
          "present in at least some members?",
          "4",
          ["3", "5", "2"], "B",
          (sum(1 for k, wall in {"Monera": "present", "Protista": "present in some", "Fungi": "present",
                                  "Plantae": "present", "Animalia": "absent"}.items() if wall != "absent") == 4),
          "Cell wall across the five kingdoms",
          "In Whittaker's table, the cell wall is non-cellulosic (polysaccharide + amino acid) in Monera, present in "
          "some Protista, present without cellulose in Fungi and present (cellulose) in Plantae. Only Animalia has "
          "no cell wall. So 4 kingdoms have a cell wall in at least some members.",
          ["Monera: present", "Protista: present in some", "Fungi: present", "Plantae: present",
           "Animalia: absent → 4"],
          why="3 leaves out Protista, where only some members have a cell wall. 5 forgets that animal cells lack a "
              "cell wall. 2 counts only the kingdoms with a cellulose or chitin wall and drops Monera too.",
          ncert=ref("BC", "Introduction (Table 2.1, characteristics of the five kingdoms)"), secs=40)

statement_pair(T_LIV, "Five kingdom classification", "Intermediate",
               "Aristotle divided animals into two groups: those which had red blood and those that did not.",
               "The two kingdom system of Linnaeus's time distinguished between unicellular and multicellular "
               "organisms.",
               True, False, "C",
               "Early systems of classification",
               "Aristotle classified plants into trees, shrubs and herbs, and divided animals into two groups, those "
               "with red blood and those without. In Linnaeus's time a two kingdom system (Plantae and Animalia) was "
               "developed; it did not distinguish between eukaryotes and prokaryotes, between unicellular and "
               "multicellular organisms, or between photosynthetic and non-photosynthetic organisms.",
               ["Statement I: true", "Statement II: false, the two kingdom system did not make this distinction"],
               ncert=ref("BC", "Introduction"), secs=35)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following organisms are placed in kingdom Protista in Whittaker's five kingdom "
                "classification?",
                [("Gonyaulax", True), ("Plasmodium", True), ("Mycoplasma", False), ("Trypanosoma", True),
                 ("Penicillium", False)],
                ["abc", "bde", "ad"], "C",
                "Members of Protista",
                "Kingdom Protista includes chrysophytes, dinoflagellates (e.g. Gonyaulax), euglenoids, slime moulds "
                "and protozoans; Plasmodium is a sporozoan and Trypanosoma a flagellated protozoan. Mycoplasma is a "
                "wall-less bacterium (Monera), and Penicillium is an ascomycete fungus (Fungi).",
                ["(a), (b), (d): protists", "(c) Mycoplasma → Monera", "(e) Penicillium → Fungi"],
                why="Each wrong combination includes Mycoplasma or Penicillium, or leaves out a protist.",
                ncert=ref("BC", "Kingdom Protista; Kingdom Monera; Kingdom Fungi"), secs=45)

direct(T_LIV, "Monera, Protista and Fungi", "Advanced",
       "An organism is prokaryotic and autotrophic, has a non-cellulosic cell wall, and may be unicellular, colonial "
       "or filamentous; its colonies are surrounded by a gelatinous sheath, some members fix nitrogen in "
       "specialised cells, and it often forms blooms in polluted water bodies. It is:",
       "a cyanobacterium, placed in kingdom Monera",
       ["a dinoflagellate, placed in kingdom Protista", "a green alga, placed in kingdom Plantae",
        "a chrysophyte, placed in kingdom Protista"], "B",
       "Identifying cyanobacteria",
       "Cyanobacteria (blue-green algae) are photosynthetic autotrophs with chlorophyll a. They are unicellular, "
       "colonial or filamentous, freshwater, marine or terrestrial; the colonies are generally surrounded by a "
       "gelatinous sheath; some, like Nostoc and Anabaena, fix atmospheric nitrogen in heterocysts; and they often "
       "form blooms in polluted water bodies. Being prokaryotes, they belong to kingdom Monera.",
       ["Prokaryotic → Monera", "Gelatinous sheath, heterocysts, blooms → cyanobacteria"],
       why="Dinoflagellates, chrysophytes and green algae are eukaryotes; a prokaryotic cell rules all three out.",
       ncert=ref("BC", "Kingdom Monera (Eubacteria)"), secs=45)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Bacteria that live in extreme salty areas belong to the eubacteria.",
                 "Eubacteria are characterised by the presence of a rigid cell wall and, if motile, a flagellum.",
                 False, True, False, "D",
                 "Archaebacteria and eubacteria",
                 "Bacteria of extreme salty areas are halophiles, which are archaebacteria, along with "
                 "thermoacidophiles (hot springs) and methanogens (marshy areas). Their differently structured cell "
                 "wall helps them survive in harsh habitats. So A is false. R is true: the true bacteria or "
                 "eubacteria are characterised by a rigid cell wall and, if motile, a flagellum.",
                 ["A: false, halophiles are archaebacteria", "R: true"],
                 ncert=ref("BC", "Kingdom Monera (Archaebacteria; Eubacteria)"), secs=40)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following organisms obtain at least part of their nutrition heterotrophically, as "
                "described in NCERT?",
                [("Euglena kept in the dark", True),
                 ("Cuscuta", True),
                 ("Nostoc", False),
                 ("A slime mould", True),
                 ("Gonyaulax", False)],
                ["abc", "bde", "ade"], "D",
                "Heterotrophy across kingdoms",
                "Euglenoids are photosynthetic in sunlight but, when deprived of sunlight, behave like heterotrophs by "
                "predating on smaller organisms. Kingdom Plantae includes a few partially heterotrophic members, such "
                "as the parasite Cuscuta. Slime moulds are saprophytic protists. Nostoc is a photosynthetic "
                "cyanobacterium, and dinoflagellates such as Gonyaulax are mostly marine and photosynthetic.",
                ["(a) Euglena in dark: heterotroph", "(b) Cuscuta: parasite", "(d) slime mould: saprophyte",
                 "(c), (e): photosynthetic"],
                why="Each wrong combination includes Nostoc or Gonyaulax, which are photosynthetic, or leaves out one "
                    "of the heterotrophs.",
                ncert=ref("BC", "Kingdom Monera; Kingdom Protista; Kingdom Plantae"), secs=60)

statement_pair(T_LIV, "Five kingdom classification", "Advanced",
               "Kingdom Plantae includes algae, bryophytes, pteridophytes, gymnosperms and angiosperms.",
               "Whittaker's five kingdom classification places lichens in kingdom Fungi.",
               True, False, "C",
               "Plantae and the place of lichens",
               "Kingdom Plantae includes all eukaryotic chlorophyll-containing organisms commonly called plants: "
               "algae, bryophytes, pteridophytes, gymnosperms and angiosperms. In Whittaker's five kingdom "
               "classification there is no mention of lichens or of acellular organisms like viruses, viroids and "
               "prions, so lichens are not placed in kingdom Fungi.",
               ["Statement I: true", "Statement II: false, lichens find no mention in the five kingdoms"],
               ncert=ref("BC", "Kingdom Plantae; Viruses, Viroids, Prions and Lichens"), secs=35)

direct(T_LIV, "Lichens, viruses and viroids", "Advanced",
       "Which of the following correctly distinguishes a prion from a viroid?",
       "A prion consists of abnormally folded protein, whereas a viroid is a free RNA that lacks a protein coat",
       ["A prion is a free RNA, whereas a viroid consists of abnormally folded protein",
        "Both consist of a nucleic acid enclosed in a protein capsid",
        "A prion contains DNA in a capsid, whereas a viroid contains RNA of high molecular weight"], "A",
       "Prions and viroids",
       "A viroid, discovered by T.O. Diener in 1971, is a free RNA that lacks the protein coat found in viruses, and "
       "its RNA is of low molecular weight. Prions are infectious agents consisting of abnormally folded protein, "
       "similar in size to viruses; they cause diseases such as bovine spongiform encephalopathy in cattle.",
       ["Viroid: free low molecular weight RNA, no protein coat", "Prion: abnormally folded protein"],
       why="The second option reverses the two. A capsid around nucleic acid describes a virus, not either of these. "
           "Viroid RNA is of low, not high, molecular weight.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)

# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "NCERT states that many species of Porphyra, Laminaria and Sargassum are among the marine algae used as food. "
       "How many species of marine algae used as food does NCERT mention?",
       "70",
       ["7", "700", "7000"], "C",
       "Algae as food",
       "Algae are useful to man in a variety of ways. Many species of Porphyra, Laminaria and Sargassum are among "
       "the 70 species of marine algae used as food.",
       ["Marine algae used as food: 70 species (e.g. Porphyra, Laminaria, Sargassum)"],
       why="7, 700 and 7000 are not the figure NCERT gives.",
       ncert=ref("PK", "Algae"), secs=20)

statement_pair(T_PK, "Bryophytes", "Basic",
               "Bryophytes, in general, are of little economic importance.",
               "The plant body of bryophytes is attached to the substratum by true roots.",
               True, False, "C",
               "General features of bryophytes",
               "NCERT states that bryophytes in general are of little economic importance, though some mosses "
               "provide food for animals and Sphagnum provides peat. Their plant body lacks true roots, stem and "
               "leaves; it is attached to the substratum by unicellular or multicellular rhizoids.",
               ["Statement I: true", "Statement II: false, attachment is by rhizoids, not true roots"],
               ncert=ref("PK", "Bryophytes"), secs=30)

direct(T_PK, "Gymnosperms", "Basic",
       "In gymnosperms, the cones bearing microsporophylls with microsporangia are called:",
       "microsporangiate or male strobili",
       ["macrosporangiate or female strobili", "sori", "gemma cups"], "A",
       "Male cones of gymnosperms",
       "Gymnosperms are heterosporous. The microsporophylls bearing microsporangia are arranged spirally along an "
       "axis to form lax or compact cones; the cones bearing microsporophylls are called microsporangiate or male "
       "strobili. Pollen grains develop within the microsporangia.",
       ["Microsporophylls + microsporangia → male (microsporangiate) strobili"],
       why="Macrosporangiate or female strobili bear megasporophylls with ovules. Gemma cups are found on liverwort "
           "thalli. Sori are not the cones of gymnosperms.",
       ncert=ref("PK", "Gymnosperms"), secs=20)

direct(T_PK, "Algae", "Basic",
       "Members of Rhodophyceae (red algae) usually reproduce vegetatively by:",
       "fragmentation",
       ["biflagellate zoospores", "gemmae", "budding in the secondary protonema"], "D",
       "Reproduction in red algae",
       "The red algae usually reproduce vegetatively by fragmentation. They reproduce asexually by non-motile "
       "spores and sexually by non-motile gametes; sexual reproduction is oogamous and followed by complex "
       "post-fertilisation developments.",
       ["Vegetative: fragmentation", "Asexual: non-motile spores", "Sexual: non-motile gametes, oogamous"],
       why="Red algae have no flagellated stages, so no zoospores. Gemmae are formed by liverworts, and budding in "
           "the secondary protonema is seen in mosses.",
       ncert=ref("PK", "Algae (Rhodophyceae)"), secs=25)

match_list(T_PK, "Pteridophytes", "Basic", "plant", "leaves",
           ["Pteris", "Selaginella", "Cycas", "Pinus"],
           ["Needle-like leaves with a thick cuticle and sunken stomata", "Large leaves (macrophylls)",
            "Small leaves (microphylls)", "Pinnate leaves that persist for a few years"],
           "II III IV I", ["III II IV I", "II III I IV", "IV III II I"], "B",
           "Leaves of pteridophytes and gymnosperms",
           "In pteridophytes the leaves may be small (microphylls), as in Selaginella, or large (macrophylls), as in "
           "ferns such as Pteris. In gymnosperms the leaves may be simple or compound; in Cycas the pinnate leaves "
           "persist for a few years, and in conifers such as Pinus the needle-like leaves reduce the surface area, "
           "with a thick cuticle and sunken stomata.",
           ["Pteris → macrophylls", "Selaginella → microphylls", "Cycas → pinnate, persist a few years",
            "Pinus → needles"],
           why="The wrong codes swap the two pteridophyte leaf types, or the two gymnosperms, or a fern with a "
               "gymnosperm.",
           ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=35)

direct(T_PK, "Algae", "Intermediate",
       "Which of the following features is found in members of Chlorophyceae and of Phaeophyceae, but NOT in members "
       "of Rhodophyceae?",
       "Flagellated motile cells",
       ["Chlorophyll d", "Floridean starch as the stored food", "Chlorophyll b"], "A",
       "Comparing the three classes of algae",
       "In NCERT's table, Chlorophyceae have 2–8 equal, apical flagella and Phaeophyceae have 2 unequal, lateral "
       "flagella, whereas flagella are absent in Rhodophyceae. Chlorophyll d and floridean starch occur only in "
       "red algae, and chlorophyll b only in green algae.",
       ["Chlorophyceae: 2–8 equal apical flagella", "Phaeophyceae: 2 unequal lateral flagella",
        "Rhodophyceae: flagella absent"],
       why="Chlorophyll d and floridean starch are found only in Rhodophyceae. Chlorophyll b is found only in "
           "Chlorophyceae, not in brown algae.",
       ncert=ref("PK", "Algae (Table 3.1)"), secs=40)

assertion_reason(T_PK, "Gymnosperms", "Intermediate",
                 "The seeds of gymnosperms are not covered by a fruit.",
                 "In gymnosperms the ovules are not enclosed by any ovary wall and remain exposed, both before and "
                 "after fertilisation.",
                 True, True, True, "A",
                 "Naked seeds",
                 "In gymnosperms (gymnos = naked, sperma = seeds) the ovules are not enclosed by an ovary wall and "
                 "remain exposed before and after fertilisation. After fertilisation the ovules develop into seeds, "
                 "and since there is no ovary to form a fruit, the seeds remain uncovered. R directly explains A.",
                 ["A: true", "R: true, the absence of an ovary is why the seeds are naked"],
                 ncert=ref("PK", "Gymnosperms"), secs=35)

multi_statement(T_PK, "Pteridophytes", "Intermediate",
                "Which of the following plants are pteridophytes?",
                [("Lycopodium", True), ("Salvinia", True), ("Ginkgo", False), ("Psilotum", True),
                 ("Polytrichum", False)],
                ["abc", "bde", "ade"], "B",
                "Identifying pteridophytes",
                "NCERT's examples of pteridophytes include Selaginella, Equisetum, Psilotum, Lycopodium, Salvinia, "
                "Pteris, Dryopteris and Adiantum. Ginkgo is a gymnosperm and Polytrichum a moss.",
                ["(a), (b), (d): pteridophytes", "(c) Ginkgo: gymnosperm", "(e) Polytrichum: moss"],
                why="Each wrong combination includes Ginkgo or Polytrichum, or leaves out a pteridophyte.",
                ncert=ref("PK", "Pteridophytes; Gymnosperms; Bryophytes"), secs=35)

direct(T_PK, "Pteridophytes", "Intermediate",
       "In a fern such as Dryopteris, the antheridia that release antherozoids are borne on:",
       "the prothallus, a small free-living gametophyte",
       ["the sporophylls of the leafy sporophyte", "the strobili of the sporophyte",
        "the capsule of the sporophyte"], "C",
       "Sex organs of pteridophytes",
       "In pteridophytes the main plant body is a sporophyte that bears sporangia on sporophylls. The spores "
       "germinate into small, multicellular, free-living, mostly photosynthetic thalloid gametophytes called "
       "prothallus. The gametophytes bear the male and female sex organs, the antheridia and archegonia, and water "
       "is needed for transfer of antherozoids to the archegonium.",
       ["Sporophyte → sporangia → spores", "Spore → prothallus (gametophyte) → antheridia and archegonia"],
       why="Sporophylls and strobili of the sporophyte bear sporangia, which produce spores, not antherozoids. A "
           "capsule is part of a bryophyte sporophyte.",
       ncert=ref("PK", "Pteridophytes"), secs=35)

statement_pair(T_PK, "Gymnosperms", "Intermediate",
               "The sporophyte is the dominant phase in pteridophytes, whereas the gametophyte is the dominant phase "
               "in gymnosperms.",
               "In both pteridophytes and gymnosperms, the sporangia are borne on sporophylls.",
               False, True, "D",
               "Pteridophytes and gymnosperms compared",
               "In both pteridophytes and gymnosperms the main plant body is the sporophyte. In gymnosperms the male "
               "and female gametophytes have no independent free-living existence; they remain within the "
               "sporangia retained on the sporophyte. In pteridophytes sporangia are borne on leaf-like sporophylls, "
               "and in gymnosperms on microsporophylls and megasporophylls.",
               ["Statement I: false, the sporophyte is dominant in both", "Statement II: true"],
               ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=40)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "In members of Chlorophyceae, the pigments are localised in definite chloroplasts.",
                 "Members of Chlorophyceae lack pyrenoids in their chloroplasts.",
                 True, False, False, "C",
                 "Chloroplasts of green algae",
                 "In green algae the pigments, chiefly chlorophyll a and b, are localised in definite chloroplasts, "
                 "which may be discoid, plate-like, reticulate, cup-shaped, spiral or ribbon-shaped. Most members "
                 "have one or more storage bodies called pyrenoids located in the chloroplasts; pyrenoids contain "
                 "protein besides starch. So R is false.",
                 ["A: true", "R: false, most green algae have pyrenoids in the chloroplasts"],
                 ncert=ref("PK", "Algae (Chlorophyceae)"), secs=35)

direct(T_PK, "Bryophytes", "Intermediate",
       "Which of the following pairs consists of a liverwort and a moss, in that order?",
       "Marchantia and Sphagnum",
       ["Funaria and Marchantia", "Polytrichum and Funaria", "Marchantia and Salvinia"], "D",
       "Liverworts and mosses",
       "Bryophytes include liverworts and mosses. Marchantia is a liverwort. Funaria, Polytrichum and Sphagnum are "
       "mosses. Salvinia is a heterosporous pteridophyte.",
       ["Liverwort: Marchantia", "Mosses: Funaria, Polytrichum, Sphagnum"],
       why="Funaria and Marchantia is the reverse order. Polytrichum and Funaria are both mosses. Salvinia is a "
           "pteridophyte, not a moss.",
       ncert=ref("PK", "Bryophytes"), secs=30)

direct(T_PK, "Bryophytes", "Advanced",
       "A plant has a dominant gametophyte with two stages: a creeping, green, branched, frequently filamentous "
       "stage, and an upright stage of slender axes bearing spirally arranged leaves, attached to the soil by "
       "multicellular, branched rhizoids. Its sporophyte has a foot, seta and capsule. The plant is most likely:",
       "Polytrichum",
       ["Marchantia", "Selaginella", "Spirogyra"], "B",
       "Identifying a moss",
       "In mosses the gametophyte has two stages: the protonema (creeping, green, branched, frequently filamentous) "
       "and the leafy stage, which develops from the secondary protonema and has upright, slender axes with "
       "spirally arranged leaves, attached by multicellular, branched rhizoids. The moss sporophyte is "
       "differentiated into foot, seta and capsule. Funaria, Polytrichum and Sphagnum are mosses.",
       ["Protonema + leafy stage → moss", "Polytrichum is a moss"],
       why="Marchantia is a thalloid liverwort without a protonema stage. Selaginella is a pteridophyte whose "
           "dominant plant body is a sporophyte. Spirogyra is a filamentous green alga.",
       ncert=ref("PK", "Bryophytes (Mosses)"), secs=45)

multi_statement(T_PK, "Gymnosperms", "Advanced",
                "A seed plant bears naked ovules on megasporophylls, and its pollen grains are carried by air "
                "currents to the opening of the ovules. Which of the following statements about this plant are "
                "correct?",
                [("Its seeds are not covered by a fruit.", True),
                 ("It produces haploid microspores and megaspores.", True),
                 ("Its gametophytes have an independent, free-living existence.", False),
                 ("Its main plant body is a sporophyte with true roots, stem and leaves.", True),
                 ("Its ovules are borne on the microsporophylls.", False)],
                ["abc", "ade", "bcd"], "C",
                "Features of gymnosperms",
                "The plant described is a gymnosperm. Gymnosperms are heterosporous (haploid microspores and "
                "megaspores); the main plant body is a sporophyte with roots, stem and leaves; the ovules borne on "
                "megasporophylls are not enclosed by an ovary, so the seeds are naked. The male and female "
                "gametophytes do not have an independent free-living existence, and the microsporophylls bear "
                "microsporangia, not ovules.",
                ["(a), (b), (d): true", "(c): false, gametophytes are retained on the sporophyte",
                 "(e): false, ovules are on megasporophylls"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("PK", "Gymnosperms"), secs=60)

statement_pair(T_PK, "Bryophytes", "Advanced",
               "In Marchantia, the gemma cups are borne on the sporophyte.",
               "In mosses, the spores are formed within the capsule after meiosis.",
               False, True, "D",
               "Gemmae and spore formation in bryophytes",
               "In liverworts such as Marchantia, asexual reproduction is by gemmae, which develop in small "
               "receptacles called gemma cups located on the thalli, i.e. on the gametophyte. The bryophyte "
               "sporophyte (foot, seta, capsule) is attached to the gametophyte; in the capsule, spores are formed "
               "after meiosis.",
               ["Statement I: false, gemma cups are on the gametophyte thallus", "Statement II: true"],
               ncert=ref("PK", "Bryophytes (Liverworts; Mosses)"), secs=40)

multi_statement(T_PK, "Gymnosperms", "Advanced",
                "In which of the following is one generation NOT free-living, but remains attached to or retained "
                "on the other generation?",
                [("The sporophyte of a moss", True),
                 ("The sporophyte of a liverwort", True),
                 ("The prothallus of a fern", False),
                 ("The female gametophyte of a gymnosperm", True),
                 ("The mature sporophyte of a fern", False)],
                ["abc", "bde", "ade"], "A",
                "Dependence between generations",
                "In bryophytes the sporophyte is not free-living but attached to the photosynthetic gametophyte, "
                "from which it derives nourishment. In gymnosperms the gametophytes remain within the sporangia "
                "retained on the sporophyte. In pteridophytes both generations are free-living: the prothallus is a "
                "small free-living gametophyte and the main plant body is an independent sporophyte.",
                ["(a), (b): bryophyte sporophyte attached to gametophyte",
                 "(d): gymnosperm gametophyte retained on sporophyte",
                 "(c), (e): fern generations are both free-living"],
                why="Each wrong combination includes a fern generation, which is free-living, or leaves out one of "
                    "the dependent generations.",
                ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

assertion_reason(T_PK, "Gymnosperms", "Advanced",
                 "In gymnosperms, water is required for the antherozoids to swim to the archegonia.",
                 "In gymnosperms, the pollen tube carrying the male gametes grows towards the archegonia in the "
                 "ovules.",
                 False, True, False, "D",
                 "Fertilisation in gymnosperms",
                 "Gymnosperm pollen grains are carried by air currents to the opening of the ovules. The pollen tube "
                 "carrying the male gametes grows towards the archegonia and discharges the gametes near the mouth "
                 "of the archegonia. So fertilisation does not depend on water for swimming antherozoids, as it "
                 "does in bryophytes and pteridophytes. A is false, R is true.",
                 ["A: false, male gametes reach the archegonia through the pollen tube", "R: true"],
                 ncert=ref("PK", "Gymnosperms"), secs=40)

# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Flower", "Basic",
       "Each stamen, which represents the male reproductive organ of a flower, consists of:",
       "a stalk or filament and an anther",
       ["a style and a stigma", "an ovary and ovules", "a pedicel and a thalamus"], "B",
       "Parts of a stamen",
       "The androecium is composed of stamens. Each stamen consists of a stalk or filament and an anther. Each "
       "anther is usually bilobed and each lobe has two chambers, the pollen sacs, in which pollen grains are "
       "produced.",
       ["Stamen = filament + anther"],
       why="Stigma, style and ovary are parts of a carpel; the pedicel and thalamus are the flower stalk and its "
           "swollen end.",
       ncert=ref("MOR", "The Flower (Androecium)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "NCERT lists the main functions of the root system. Which of the following is NOT one of them?",
       "Photosynthesis",
       ["Synthesis of plant growth regulators", "Storing reserve food material",
        "Providing a proper anchorage to the plant parts"], "C",
       "Functions of the root system",
       "The main functions of the root system are absorption of water and minerals from the soil, providing a "
       "proper anchorage to the plant parts, storing reserve food material and synthesis of plant growth "
       "regulators. Photosynthesis is a function of leaves (and of green stems in some plants), not of the root "
       "system.",
       ["Root: absorption, anchorage, food storage, synthesis of plant growth regulators"],
       why="The other three are all listed by NCERT as functions of the root system.",
       ncert=ref("MOR", "The Root"), secs=25)

direct(T_MOR, "Flower", "Basic",
       "The arrangement of ovules within the ovary is known as:",
       "placentation",
       ["aestivation", "phyllotaxy", "venation"], "D",
       "Definition of placentation",
       "The arrangement of ovules within the ovary is known as placentation; its main types are marginal, axile, "
       "parietal, basal, central and free central.",
       ["Ovules in ovary → placentation"],
       why="Aestivation is the arrangement of sepals or petals in a bud, phyllotaxy the arrangement of leaves on "
           "the stem, and venation the arrangement of veins in the lamina.",
       ncert=ref("MOR", "The Flower (Gynoecium)"), secs=20)

direct(T_MOR, "Flower", "Basic",
       "The mode of arrangement of sepals or petals in a floral bud with respect to the other members of the same "
       "whorl is known as:",
       "aestivation",
       ["placentation", "inflorescence", "phyllotaxy"], "A",
       "Definition of aestivation",
       "The mode of arrangement of sepals or petals in a floral bud with respect to the other members of the same "
       "whorl is known as aestivation. Its main types are valvate, twisted, imbricate and vexillary.",
       ["Arrangement of sepals or petals in bud → aestivation"],
       why="Placentation refers to ovules in the ovary, inflorescence to flowers on the floral axis, and phyllotaxy "
           "to leaves on the stem.",
       ncert=ref("MOR", "The Flower (Aestivation)"), secs=20)

statement_pair(T_MOR, "Fruit and seed", "Basic",
               "The fruit is a characteristic feature of the flowering plants.",
               "Leaves are the most important vegetative organs for photosynthesis.",
               True, True, "A",
               "Fruit and leaf",
               "NCERT states that the fruit is a characteristic feature of the flowering plants; it is a mature or "
               "ripened ovary developed after fertilisation. It also states that leaves are the most important "
               "vegetative organs for photosynthesis.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Leaf; The Fruit"), secs=25)

match_list(T_MOR, "Root, stem and leaf", "Intermediate", "plant", "storage organ",
           ["Sweet potato", "Carrot", "Zaminkand", "Garlic"],
           ["Fleshy leaves", "Swollen adventitious roots", "Swollen tap root", "Underground stem"],
           "II III IV I", ["III II IV I", "II III I IV", "IV III II I"], "B",
           "Organs that store food",
           "Food is stored in swollen adventitious roots in sweet potato and in the swollen tap root in carrot. "
           "Underground stems of potato, ginger, turmeric, zaminkand and Colocasia store food. The fleshy leaves of "
           "onion and garlic store food.",
           ["Sweet potato → adventitious root", "Carrot → tap root", "Zaminkand → underground stem",
            "Garlic → fleshy leaves"],
           why="The wrong codes swap the two kinds of storage root, or swap the stem and the leaves.",
           ncert=ref("MOR", "The Root; The Stem; The Leaf (modifications)"), secs=45)

direct(T_MOR, "Plant families", "Intermediate",
       "In the floral formula of the family Fabaceae, the androecium is written as A(9)+1. This means that the "
       "flower has:",
       "ten stamens, nine of which are united into one bundle while one is free (diadelphous)",
       ["nine stamens united with the petals and one sterile stamen (staminode)",
        "ten free stamens arranged in two whorls",
        "nine stamens and one carpel"], "B",
       "Reading the androecium in a floral formula",
       "In a floral formula, fusion is shown by enclosing the figure within brackets. In Fabaceae the androecium "
       "has ten stamens and is diadelphous: nine are united into one bundle, written (9), and one is free, written "
       "+1. The anthers are dithecous.",
       ["Brackets = fusion", "(9)+1 = nine fused + one free = diadelphous"],
       why="Union with petals (epipetaly) is shown by a line joining C and A, not by brackets. 'Free in two whorls' "
           "ignores the brackets. The carpel is shown separately by G1.",
       ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=40)

assertion_reason(T_MOR, "Root, stem and leaf", "Intermediate",
                 "Mustard plants have a tap root system.",
                 "In mustard, the primary root formed by direct elongation of the radicle grows inside the soil and "
                 "bears lateral roots of several orders.",
                 True, True, True, "A",
                 "Tap root system",
                 "In majority of dicotyledonous plants the direct elongation of the radicle leads to the formation of "
                 "the primary root, which grows inside the soil and bears lateral roots of several orders (secondary, "
                 "tertiary roots). The primary root and its branches constitute the tap root system, as seen in "
                 "mustard. R describes exactly what makes it a tap root system.",
                 ["A: true", "R: true and explains A"],
                 ncert=ref("MOR", "The Root"), secs=35)

multi_statement(T_MOR, "Root, stem and leaf", "Intermediate",
                "Which of the following statements about the leaf are correct?",
                [("A typical leaf consists of three main parts: the leaf base, the petiole and the lamina.", True),
                 ("The leaf base may bear two lateral small leaf-like structures called stipules.", True),
                 ("The petiole helps hold the blade to light.", True),
                 ("In a pinnately compound leaf, the leaflets are attached at a common point, the tip of the "
                  "petiole.", False),
                 ("The lamina has a prominent middle vein called the midrib.", True)],
                ["abcd", "bce", "acde"], "B",
                "Parts of a leaf",
                "A typical leaf has a leaf base, petiole and lamina. The leaf is attached to the stem by the leaf "
                "base, which may bear two lateral small leaf-like stipules. The petiole helps hold the blade to "
                "light. The lamina is the green expanded part with veins and veinlets, and the middle prominent vein "
                "is the midrib. In a pinnately compound leaf the leaflets lie on a common axis, the rachis; leaflets "
                "attached at the tip of the petiole make a palmately compound leaf.",
                ["(a), (b), (c), (e): true", "(d): false, this describes a palmately compound leaf"],
                why="Each wrong combination includes (d) or leaves out a true statement.",
                ncert=ref("MOR", "The Leaf"), secs=50)

statement_pair(T_MOR, "Fruit and seed", "Intermediate",
               "In a dicotyledonous seed, the embryo consists of an embryonal axis and two cotyledons.",
               "In the embryo of maize, the coleoptile encloses the radicle.",
               True, False, "C",
               "Embryos of dicot and monocot seeds",
               "The embryo of a dicotyledonous seed consists of an embryonal axis and two cotyledons; the radicle "
               "and plumule are at the two ends of the axis. In the maize embryo there is one shield-shaped "
               "cotyledon, the scutellum; the plumule is enclosed in a sheath called the coleoptile and the "
               "radicle in a sheath called the coleorhiza.",
               ["Statement I: true", "Statement II: false, the coleoptile encloses the plumule"],
               ncert=ref("MOR", "The Seed"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "A flower is bisexual and actinomorphic, with six tepals in two whorls, six stamens attached to the perianth, "
       "and a superior, tricarpellary, syncarpous ovary. Which of the following plants could bear this flower?",
       "Tulip",
       ["Petunia", "Lupin", "China rose"], "A",
       "Identifying a flower of Liliaceae",
       "The features are those of Liliaceae: perianth of six tepals (3 + 3), six epiphyllous stamens (3 + 3) and "
       "a superior, tricarpellary, syncarpous ovary. Tulip and Gloriosa are ornamental plants of Liliaceae.",
       ["P(3+3), A3+3 epiphyllous, G(3) superior → Liliaceae", "Tulip belongs to Liliaceae"],
       why="Petunia (Solanaceae) has a pentamerous flower with bicarpellary ovary. Lupin (Fabaceae) has a "
           "zygomorphic flower with one carpel. China rose has monoadelphous stamens, a distinct calyx and corolla.",
       ncert=ref("MOR", "Description of Some Important Families (Liliaceae)"), secs=40)

direct(T_MOR, "Root, stem and leaf", "Intermediate",
       "Which of the following is NOT a modification of the stem?",
       "Spines of cactus",
       ["Tendrils of watermelon", "Thorns of Bougainvillea", "Flattened green structures of Opuntia"], "D",
       "Stem and leaf modifications",
       "Stem tendrils develop from axillary buds in gourds such as cucumber, pumpkin and watermelon. Axillary buds "
       "of stems are modified into thorns in Citrus and Bougainvillea. In Opuntia the stem is modified into "
       "flattened green structures that photosynthesise. In cacti, the leaves are modified into spines.",
       ["Watermelon tendril, Bougainvillea thorn, Opuntia flattened stem → stem",
        "Cactus spines → leaf"],
       why="Tendrils of watermelon, thorns of Bougainvillea and the flattened structures of Opuntia are all "
           "modified stems.",
       ncert=ref("MOR", "The Stem; The Leaf (modifications)"), secs=35)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements correctly compare the families Solanaceae and Liliaceae?",
                [("Both have a bilocular ovary.", False),
                 ("Both have axile placentation.", True),
                 ("The stamens are epipetalous in Solanaceae and epiphyllous in Liliaceae.", True),
                 ("Both have endospermous seeds.", True),
                 ("Both have a persistent calyx.", False)],
                ["abc", "bcde", "cde"], "B",
                "Solanaceae and Liliaceae compared",
                "Solanaceae: bicarpellary, syncarpous, bilocular ovary with axile placentation; five epipetalous "
                "stamens; calyx persistent; seeds many, endospermous. Liliaceae: tricarpellary, syncarpous, "
                "trilocular ovary with axile placentation; six tepals, six epiphyllous stamens; seeds endospermous. "
                "Liliaceae has a perianth, not a separate calyx, so it cannot have a persistent calyx.",
                ["(b), (c), (d): true", "(a): false, Liliaceae ovary is trilocular",
                 "(e): false, Liliaceae has tepals, not a calyx"],
                why="Each wrong combination includes (a) or (e), or leaves out a true statement.",
                ncert=ref("MOR", "Description of Some Important Families (Solanaceae; Liliaceae)"), secs=60)

multi_statement(T_MOR, "Inflorescence", "Advanced",
                "In the inflorescence of a plant, the older flowers are at the base and the younger flowers towards "
                "the apex of the main axis. Which of the following statements about it are correct?",
                [("The inflorescence is racemose.", True),
                 ("The main axis has terminated in a flower.", False),
                 ("Plants of the family Fabaceae have this type of inflorescence.", True),
                 ("The inflorescence of Liliaceae, often in umbellate clusters, is of this type.", False),
                 ("The flowers are borne in acropetal succession.", True)],
                ["abe", "acd", "ce"], "A",
                "Recognising a racemose inflorescence",
                "In racemose inflorescences the main axis continues to grow and the flowers are borne laterally in "
                "acropetal succession, so older flowers are lower and younger flowers nearer the apex. In cymose "
                "inflorescences the main axis terminates in a flower and flowers are borne in basipetal order. "
                "Fabaceae has a racemose inflorescence; Liliaceae has a solitary or cymose inflorescence, often in "
                "umbellate clusters.",
                ["Older below, younger above → acropetal → racemose", "Fabaceae: racemose",
                 "Liliaceae: solitary or cymose"],
                why="Each wrong combination includes (b) or (d), which describe cymose features, or omits a true "
                    "statement.",
                ncert=ref("MOR", "The Inflorescence; Description of Some Important Families"), secs=60)

numerical(T_MOR, "Plant families", "Advanced",
          "The floral formula of Fabaceae is % ⚥ K(5) C1+2+(2) A(9)+1 G1. Counting every individual sepal, petal, "
          "stamen and carpel separately, how many floral members does one such flower have?",
          "21",
          ["17", "13", "20"], "D",
          (5 + (1 + 2 + 2) + (9 + 1) + 1 == 21),
          "Counting floral members from a formula",
          "Brackets show fusion, not a single member. K(5) = 5 united sepals; C1+2+(2) = 1 standard + 2 wings + 2 "
          "united keel petals = 5; A(9)+1 = 10 stamens; G1 = 1 carpel. Total = 5 + 5 + 10 + 1 = 21.",
          ["K: 5", "C: 1 + 2 + 2 = 5", "A: 9 + 1 = 10", "G: 1", "Total = 21"],
          why="17 counts the five fused sepals as one member. 13 counts the stamens as two units (one bundle + one "
              "free). 20 counts the two fused keel petals as a single petal.",
          ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=60)

statement_pair(T_MOR, "Flower", "Advanced",
               "On the basis of its floral formula, a flower of Liliaceae is trimerous.",
               "On the basis of its floral formula, a flower of Solanaceae is tetramerous.",
               True, False, "C",
               "Merous condition from floral formulae",
               "A flower is trimerous, tetramerous or pentamerous when its floral appendages are in multiples of 3, 4 "
               "or 5. Liliaceae: P(3+3) A3+3 G(3), all in threes, so trimerous. Solanaceae: K(5) C(5) A5 G(2), the "
               "perianth whorls and stamens in fives, so pentamerous, not tetramerous.",
               ["Liliaceae: 3 + 3, 3 + 3, 3 → trimerous", "Solanaceae: 5, 5, 5 → pentamerous"],
               ncert=ref("MOR", "The Flower; Description of Some Important Families"), secs=45)

assertion_reason(T_MOR, "Flower", "Advanced",
                 "In epigynous flowers, the ovary is superior.",
                 "In hypogynous flowers, the gynoecium occupies the highest position and the other parts are situated "
                 "below it.",
                 False, True, False, "D",
                 "Position of the ovary",
                 "In hypogynous flowers the gynoecium occupies the highest position and the other parts lie below it; "
                 "the ovary is superior (mustard, china rose, brinjal). In epigynous flowers the margin of the "
                 "thalamus grows upward, encloses the ovary completely and fuses with it, and the other parts arise "
                 "above the ovary, so the ovary is inferior (guava, cucumber, ray florets of sunflower). A is false, "
                 "R is true.",
                 ["A: false, an epigynous flower has an inferior ovary", "R: true"],
                 ncert=ref("MOR", "The Flower (position of floral parts on the thalamus)"), secs=40)

# =============================================================== 4. Anatomy of Flowering Plants (4/6/4)
direct(T_ANA, "Plant tissues", "Basic",
       "Growth in plants is largely restricted to specialised regions of active cell division. These regions are "
       "called:",
       "meristems",
       ["permanent tissues", "complex tissues", "stele"], "A",
       "Meristems",
       "Growth in plants is largely restricted to specialised regions of active cell division called meristems "
       "(Gk. meristos: divided). Plants have apical, intercalary and lateral meristems.",
       ["Regions of active cell division → meristems"],
       why="Permanent tissues are cells that have lost the ability to divide. Complex tissues (xylem, phloem) are "
           "made of more than one cell type. The stele is all the tissue inside the endodermis.",
       ncert=ref("ANA", "The Tissues (Meristematic Tissues)"), secs=20)

direct(T_ANA, "Tissue systems", "Basic",
       "On the basis of their structure and location, the tissues of a plant are grouped into three tissue "
       "systems. These are the:",
       "epidermal, ground (fundamental) and vascular (conducting) tissue systems",
       ["meristematic, permanent and secretory tissue systems",
        "simple, complex and secretory tissue systems",
        "apical, intercalary and lateral tissue systems"], "C",
       "The three tissue systems",
       "The structure of tissues varies with their location in the plant body. On this basis there are three "
       "tissue systems: the epidermal tissue system, the ground or fundamental tissue system and the vascular or "
       "conducting tissue system.",
       ["Epidermal + ground + vascular tissue systems"],
       why="Meristematic and permanent, and simple and complex, are kinds of tissues, not tissue systems. Apical, "
           "intercalary and lateral are kinds of meristems.",
       ncert=ref("ANA", "The Tissue System"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "Which of the following pairs consists only of simple permanent tissues?",
       "Collenchyma and sclerenchyma",
       ["Xylem and phloem", "Parenchyma and phloem", "Xylem and sclerenchyma"], "B",
       "Simple and complex tissues",
       "A simple tissue is made of only one type of cell; the simple permanent tissues are parenchyma, collenchyma "
       "and sclerenchyma. Complex tissues are made of more than one type of cell working together as a unit; xylem "
       "and phloem are complex tissues.",
       ["Simple: parenchyma, collenchyma, sclerenchyma", "Complex: xylem, phloem"],
       why="Each wrong pair contains xylem or phloem, which are complex tissues.",
       ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=20)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "The epidermal tissue system forms the outermost covering of the whole plant body.",
               "The vascular system consists of complex tissues, the phloem and the xylem.",
               True, True, "A",
               "Epidermal and vascular tissue systems",
               "The epidermal tissue system forms the outer-most covering of the whole plant body and comprises "
               "epidermal cells, stomata and the epidermal appendages (trichomes and hairs). The vascular system "
               "consists of the complex tissues phloem and xylem, which together form the vascular bundles.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System"), secs=25)

numerical(T_ANA, "Plant tissues", "Intermediate",
          "How many of the following are dead at maturity, according to NCERT?\n"
          "Tracheids, vessel members, sclereids, phloem fibres, xylem parenchyma, companion cells, sieve tube "
          "elements, collenchyma cells",
          "4",
          ["5", "3", "6"], "B",
          (sum({"tracheids": 1, "vessel members": 1, "sclereids": 1, "phloem fibres": 1, "xylem parenchyma": 0,
                "companion cells": 0, "sieve tube elements": 0, "collenchyma": 0}.values()) == 4),
          "Living and dead cells of plant tissues",
          "Dead at maturity: tracheids (dead, without protoplasm), vessel members (devoid of protoplasm), sclereids "
          "(highly thickened dead cells) and phloem fibres (lose their protoplasm and become dead at maturity). "
          "Living: xylem parenchyma, companion cells, sieve tube elements (living, with peripheral cytoplasm, though "
          "without a nucleus) and collenchyma. So 4 are dead.",
          ["Dead: tracheids, vessels, sclereids, phloem fibres = 4",
           "Living: xylem parenchyma, companion cells, sieve tube elements, collenchyma"],
          why="5 wrongly counts sieve tube elements as dead because they lack a nucleus. 3 forgets that phloem fibres "
              "die at maturity. 6 counts both sieve tube elements and companion cells as dead.",
          ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=60)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Apical meristems and intercalary meristems are called primary meristems.",
                 "They appear early in the life of a plant and contribute to the formation of the primary plant "
                 "body.",
                 True, True, True, "A",
                 "Primary meristems",
                 "NCERT explains that apical and intercalary meristems are primary meristems because they appear "
                 "early in the life of a plant and contribute to the formation of the primary plant body. Lateral "
                 "meristems, which appear later, are secondary meristems.",
                 ["A: true", "R: true, and it is the reason for the name"],
                 ncert=ref("ANA", "The Tissues (Meristematic Tissues)"), secs=35)

match_list(T_ANA, "Plant tissues", "Intermediate", "cell or tissue", "nature of the cell wall",
           ["Parenchyma", "Collenchyma", "Sclerenchyma", "Endodermis of a dicot root"],
           ["Thin walls made of cellulose",
            "Thickened at the corners by deposition of cellulose, hemicellulose and pectin",
            "Thick and lignified walls with a few or numerous pits",
            "Tangential and radial walls with a deposit of suberin as Casparian strips"],
           "I II III IV", ["II I III IV", "I II IV III", "I III II IV"], "D",
           "Cell walls of plant tissues",
           "Parenchyma cells have thin cell walls made of cellulose. Collenchyma cells are thickened at the corners "
           "due to deposition of cellulose, hemicellulose and pectin. Sclerenchyma has long, narrow cells with thick "
           "and lignified walls with a few or numerous pits. The endodermal cells of the root have a deposition of "
           "water-impermeable, waxy suberin on their tangential and radial walls in the form of Casparian strips.",
           ["Parenchyma → thin cellulose", "Collenchyma → corner thickening", "Sclerenchyma → lignified",
            "Root endodermis → suberin (Casparian strips)"],
           why="The wrong codes swap parenchyma and collenchyma, sclerenchyma and endodermis, or collenchyma and "
               "sclerenchyma.",
           ncert=ref("ANA", "The Tissues; Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=45)

multi_statement(T_ANA, "Plant tissues", "Intermediate",
                "Which of the following statements comparing collenchyma and sclerenchyma are correct?",
                [("Both provide mechanical support.", True),
                 ("Collenchyma cells may contain chloroplasts, in which case they assimilate food.", True),
                 ("Both have lignified cell walls.", False),
                 ("The walls of sclerenchyma cells have a few or numerous pits.", True),
                 ("Collenchyma cells have large intercellular spaces between them.", False)],
                ["abc", "abde", "bd"], "A",
                "Collenchyma and sclerenchyma compared",
                "Collenchyma provides mechanical support to growing parts such as the young stem and petiole; its "
                "cells often contain chloroplasts and then assimilate food; its walls are thickened at the corners "
                "with cellulose, hemicellulose and pectin, and intercellular spaces are absent. Sclerenchyma "
                "provides mechanical support to organs; its cells have thick, lignified walls with a few or "
                "numerous pits.",
                ["(a), (b), (d): true", "(c): false, collenchyma is not lignified",
                 "(e): false, collenchyma has no intercellular spaces"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=50)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "The hypodermis is sclerenchymatous in a monocot stem but collenchymatous in a dicot stem.",
               "The vascular bundles are conjoint and closed in both dicot and monocot stems.",
               True, False, "C",
               "Dicot and monocot stems compared",
               "In a dicot stem the hypodermis consists of a few layers of collenchymatous cells; the monocot stem "
               "has a sclerenchymatous hypodermis. The vascular bundles of a dicot stem are conjoint and open (with "
               "cambium); those of a monocot stem are conjoint and closed.",
               ["Statement I: true", "Statement II: false, dicot stem bundles are open"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "In the transverse section of a dicot root, which of the following is NOT a part of the stele?",
       "Endodermis",
       ["Pericycle", "Conjunctive tissue", "Pith"], "C",
       "Extent of the stele",
       "All tissues on the inner side of the endodermis, such as the pericycle, vascular bundles and pith, "
       "constitute the stele. In the dicot root this includes the conjunctive tissue (parenchyma between xylem and "
       "phloem). The endodermis is the innermost layer of the cortex and lies outside the stele.",
       ["Stele = everything inside the endodermis", "Endodermis = innermost layer of cortex"],
       why="Pericycle, conjunctive tissue and pith all lie inside the endodermis and so belong to the stele.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous Root)"), secs=35)

assertion_reason(T_ANA, "Tissue systems", "Advanced",
                 "In grasses, the guard cells of the stomata are dumb-bell shaped.",
                 "In grass leaves, some adaxial epidermal cells along the veins are modified into large, empty, "
                 "colourless bulliform cells.",
                 True, True, False, "B",
                 "Two features of grass leaves",
                 "Both are true features of grass leaves. The dumb-bell shape describes the guard cells that enclose "
                 "the stomatal pore. Bulliform cells are a separate set of epidermal cells along the veins that help "
                 "in rolling the leaf when they lose water. The existence of bulliform cells has nothing to do with "
                 "the shape of the guard cells, so R does not explain A.",
                 ["A: true", "R: true", "R concerns other epidermal cells, not the shape of guard cells"],
                 ncert=ref("ANA", "The Tissue System (Epidermal Tissue System); Monocotyledonous Leaf"), secs=45)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "In the transverse section of a plant organ, the xylem and phloem lie on different radii, the "
                "endodermis has Casparian strips, and the pith is large and well developed. Which of the following "
                "conclusions are correct?",
                [("The section is of a monocot root.", True),
                 ("The protoxylem lies towards the periphery of the organ.", True),
                 ("Cambium is present between the xylem and the phloem, so the bundles are open.", False),
                 ("There are usually more than six xylem bundles.", True),
                 ("The xylem and phloem lie together on the same radius.", False)],
                ["abc", "bde", "ade"], "C",
                "Interpreting a transverse section",
                "Xylem and phloem on different radii means radial vascular bundles, found in roots; a Casparian "
                "endodermis confirms a root. A large, well-developed pith is a feature of the monocot root, which "
                "usually has more than six xylem bundles (polyarch). In roots the primary xylem is exarch, with "
                "protoxylem towards the periphery. Radial bundles have no cambium between xylem and phloem in the "
                "primary structure, and monocot roots do not undergo secondary growth.",
                ["Radial bundles + Casparian strips → root", "Large pith → monocot root (polyarch, exarch)"],
                why="Each wrong combination includes (c) or (e), which contradict the radial arrangement, or leaves "
                    "out a correct conclusion.",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Monocotyledonous Root)"),
                secs=60)

direct(T_ANA, "Tissue systems", "Advanced",
       "Which of the following pairs consists only of tissues that belong to the ground tissue system of a dicot "
       "stem?",
       "Hypodermis and medullary rays",
       ["Pericycle and protoxylem", "Epidermis and pith", "Companion cells and medullary rays"], "B",
       "Extent of the ground tissue system",
       "All tissues except the epidermis and the vascular bundles constitute the ground tissue. In a dicot stem "
       "this includes the hypodermis, cortical layers, endodermis, pericycle, medullary rays and pith. Protoxylem "
       "and companion cells are parts of the vascular bundles, and the epidermis belongs to the epidermal tissue "
       "system.",
       ["Ground tissue = all except epidermis and vascular bundles",
        "Hypodermis and medullary rays → ground tissue"],
       why="Protoxylem and companion cells belong to the vascular tissue system, and the epidermis to the epidermal "
           "tissue system.",
       ncert=ref("ANA", "The Tissue System (Ground Tissue System); Dicotyledonous Stem"), secs=45)

multi_statement(T_ANA, "Plant tissues", "Advanced",
                "Which of the following plant cells have lignified cell walls?",
                [("Tracheids", True), ("Vessel members", True), ("Sclerenchyma cells", True),
                 ("Collenchyma cells", False), ("Companion cells", False)],
                ["abcd", "bce", "acd"], "D",
                "Lignified walls",
                "Tracheids are elongated, tube-like cells with thick and lignified walls and tapering ends. A vessel "
                "member has lignified walls and a large central cavity. Sclerenchyma consists of long, narrow cells "
                "with thick and lignified cell walls. Collenchyma walls are thickened at the corners with cellulose, "
                "hemicellulose and pectin, not lignin, and companion cells are specialised parenchymatous cells.",
                ["(a), (b), (c): lignified", "(d) collenchyma: cellulose, hemicellulose, pectin",
                 "(e) companion cells: parenchymatous"],
                why="Each wrong combination includes collenchyma or companion cells, or leaves out a lignified "
                    "element.",
                ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=50)

# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Prokaryotic cell", "Basic",
       "The 70S ribosome of a prokaryotic cell is made of two subunits. These are:",
       "50S and 30S",
       ["60S and 40S", "40S and 30S", "60S and 10S"], "D",
       "Subunits of the prokaryotic ribosome",
       "In prokaryotes, ribosomes are about 15 nm by 20 nm in size and are made of two subunits, 50S and 30S, which "
       "together form the 70S prokaryotic ribosome. The eukaryotic 80S ribosome has 60S and 40S subunits.",
       ["70S = 50S + 30S (prokaryotes)", "80S = 60S + 40S (eukaryotes)"],
       why="60S and 40S are the subunits of the eukaryotic 80S ribosome. S values are sedimentation coefficients and "
           "are not simply added, so pairs chosen to add up to 70 are wrong.",
       ncert=ref("CELL", "Prokaryotic Cells (Ribosomes and Inclusion Bodies)"), secs=20)

match_list(T_CELL, "Cell theory", "Basic", "cell", "NCERT's description",
           ["Egg of an ostrich", "Nerve cell", "Human red blood cell", "White blood cell"],
           ["Amoeboid", "The largest isolated single cell", "Round and biconcave", "Some of the longest cells"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "Cells differ in size and shape",
           "Cells differ greatly in size, shape and activities. The largest isolated single cell is the egg of an "
           "ostrich. Nerve cells are some of the longest cells. Red blood cells are round and biconcave, while white "
           "blood cells are amoeboid.",
           ["Ostrich egg → largest isolated cell", "Nerve cell → among the longest", "RBC → round, biconcave",
            "WBC → amoeboid"],
           why="The wrong codes swap the ostrich egg and the nerve cell, the two blood cells, or the ostrich egg and "
               "the red blood cell.",
           ncert=ref("CELL", "An Overview of Cell"), secs=30)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "In prokaryotic cells, the ribosomes are associated with the:",
       "plasma membrane",
       ["endoplasmic reticulum", "nuclear envelope", "Golgi apparatus"], "A",
       "Location of ribosomes in prokaryotes",
       "No organelles like those of eukaryotes are found in prokaryotic cells, except ribosomes. NCERT states that "
       "in prokaryotes the ribosomes are associated with the plasma membrane of the cell.",
       ["Prokaryotes have no ER, nuclear envelope or Golgi", "Ribosomes → associated with plasma membrane"],
       why="The endoplasmic reticulum, nuclear envelope and Golgi apparatus are all absent in prokaryotic cells.",
       ncert=ref("CELL", "Prokaryotic Cells (Ribosomes and Inclusion Bodies)"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "Which cell organelle is described by NCERT as a double membrane-bound structure that is sausage-shaped or "
       "cylindrical, with a diameter of 0.2–1.0 µm?",
       "Mitochondrion",
       ["Lysosome", "Golgi apparatus", "Ribosome"], "C",
       "Shape of mitochondria",
       "Mitochondria are sausage-shaped or cylindrical, with a diameter of 0.2–1.0 µm (average 0.5 µm) and a "
       "length of 1.0–4.1 µm. Each is a double membrane-bound structure, with the inner membrane forming cristae.",
       ["Sausage-shaped or cylindrical, double membrane → mitochondrion"],
       why="Lysosomes are single membrane-bound vesicles. The Golgi apparatus is made of flat, disc-shaped "
           "cisternae. Ribosomes have no membrane at all.",
       ncert=ref("CELL", "Mitochondria"), secs=20)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
               "Chloroplasts may be lens-shaped, oval, spherical, discoid or even ribbon-like organelles.",
               "The space limited by the inner membrane of the chloroplast is called the stroma.",
               True, True, "A",
               "Chloroplast shape and stroma",
               "The chloroplasts in green plants are lens-shaped, oval, spherical, discoid or even ribbon-like, with "
               "a length of 5–10 µm and a width of 2–4 µm. They are double membrane-bound, and the space limited by "
               "the inner membrane is called the stroma, in which the thylakoids lie.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Plastids"), secs=25)

numerical(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate",
          "How many individual microtubules are present in the 9 + 2 axoneme of a cilium, and in the nine "
          "peripheral fibrils of a centriole, respectively?",
          "20 and 27",
          ["11 and 9", "20 and 18", "18 and 27"], "C",
          (9 * 2 + 2 == 20 and 9 * 3 == 27),
          "Counting microtubules",
          "The axoneme has nine doublets of radially arranged peripheral microtubules and a pair of centrally "
          "located microtubules: 9 × 2 + 2 = 20. A centriole has nine evenly spaced peripheral fibrils of tubulin, "
          "each of which is a triplet: 9 × 3 = 27.",
          ["Axoneme: 9 doublets + 2 central = 18 + 2 = 20", "Centriole: 9 triplets = 27"],
          why="11 and 9 count fibrils, not individual microtubules. 20 and 18 treats the centriole fibrils as "
              "doublets. 18 and 27 forgets the central pair of the axoneme.",
          ncert=ref("CELL", "Cilia and Flagella; Centrosome and Centrioles"), secs=50)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "A protein synthesised by ribosomes on the endoplasmic reticulum is to be secreted from the cell. Which route "
       "does it most likely follow?",
       "Rough ER → cis face of the Golgi apparatus → trans face of the Golgi apparatus → outside the cell",
       ["Trans face of the Golgi apparatus → cis face → rough ER → outside the cell",
        "Smooth ER → lysosome → nucleus → outside the cell",
        "Rough ER → trans face of the Golgi apparatus → cis face → outside the cell"], "B",
       "Route of secretory proteins",
       "The Golgi cisternae have a convex cis (forming) face and a concave trans (maturing) face. Materials to be "
       "packaged come from the ER, fuse with the cis face and move towards the trans face. Many proteins "
       "synthesised by ribosomes on the ER are modified in the Golgi cisternae before they are released from its "
       "trans face; the Golgi apparatus packages materials to be secreted outside the cell.",
       ["RER ribosomes make the protein", "Enters Golgi at cis face", "Leaves from trans face for secretion"],
       why="The cis face receives and the trans face releases, so routes that go trans → cis are reversed. Lysosomes "
           "and the nucleus are not on the secretory route.",
       ncert=ref("CELL", "Endomembrane System (Golgi Apparatus)"), secs=40)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "The genomic DNA of a prokaryotic cell is described as 'naked'.",
                 "In prokaryotes, the genetic material is not enveloped by a nuclear membrane.",
                 True, True, True, "A",
                 "Naked genetic material of prokaryotes",
                 "Prokaryotes have no well-defined nucleus. Their genetic material is basically naked, i.e. not "
                 "enveloped by a nuclear membrane; the genomic DNA is a single chromosome or circular DNA lying in "
                 "the cytoplasm. The absence of the envelope is exactly what 'naked' means, so R explains A.",
                 ["A: true", "R: true and explains A"],
                 ncert=ref("CELL", "Prokaryotic Cells"), secs=30)

multi_statement(T_CELL, "Nucleus", "Intermediate",
                "In which of the following does NCERT describe RNA as a component?",
                [("Ribosomes", True), ("Chromatin", True), ("The mitochondrial matrix", True),
                 ("The middle lamella", False), ("The cell wall of a higher plant", False)],
                ["abcd", "bce", "ac"], "D",
                "Where RNA is found",
                "Ribosomes are composed of ribonucleic acid and proteins. Chromatin contains DNA, histones, some "
                "non-histone proteins and also RNA. The mitochondrial matrix has a single circular DNA molecule, a "
                "few RNA molecules and ribosomes. The middle lamella is mainly calcium pectate, and the cell wall of "
                "higher plants consists of cellulose, hemicellulose, pectins and proteins.",
                ["(a), (b), (c): contain RNA", "(d), (e): no RNA"],
                why="Each wrong combination includes the middle lamella or the cell wall, or leaves out one of the "
                    "RNA-containing structures.",
                ncert=ref("CELL", "Ribosomes; Mitochondria; Nucleus; Cell Wall"), secs=50)

match_list(T_CELL, "Endomembrane system", "Intermediate", "scientist", "contribution",
           ["George Palade", "Camillo Golgi", "Flemming", "Singer and Nicolson"],
           ["Proposed the fluid mosaic model of the cell membrane (1972)",
            "First observed ribosomes under the electron microscope as dense particles (1953)",
            "Named the material of the nucleus stained by basic dyes 'chromatin'",
            "First observed densely stained reticular structures near the nucleus (1898)"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "D",
           "Discoverers of cell components",
           "Ribosomes were first observed by George Palade (1953). Camillo Golgi (1898) first observed densely "
           "stained reticular structures near the nucleus, later named the Golgi bodies. Flemming named the material "
           "of the nucleus stained by basic dyes chromatin. Singer and Nicolson (1972) proposed the fluid mosaic "
           "model.",
           ["Palade → ribosomes", "Golgi → Golgi bodies", "Flemming → chromatin", "Singer-Nicolson → fluid mosaic"],
           why="The wrong codes swap Palade and Golgi, Flemming and Singer-Nicolson, or Palade and Flemming.",
           ncert=ref("CELL", "Cell Membrane; Golgi Apparatus; Ribosomes; Nucleus"), secs=45)

statement_pair(T_CELL, "Prokaryotic cell", "Intermediate",
               "All prokaryotes have a cell wall surrounding the cell membrane, except Mycoplasma.",
               "In motile bacteria, the thin filamentous extensions that bring about movement are called pili.",
               True, False, "C",
               "Cell wall and motility structures of prokaryotes",
               "NCERT states that all prokaryotes have a cell wall surrounding the cell membrane, except in "
               "mycoplasma. Motile bacteria have thin filamentous extensions from their cell wall called flagella. "
               "Pili and fimbriae are surface structures that do not play a role in motility.",
               ["Statement I: true", "Statement II: false, movement is by flagella; pili do not help in motility"],
               ncert=ref("CELL", "Prokaryotic Cells (Cell Envelope and its Modifications)"), secs=35)

assertion_reason(T_CELL, "Endomembrane system", "Intermediate",
                 "The endoplasmic reticulum divides the intracellular space into two distinct compartments, the "
                 "luminal (inside ER) and the extra-luminal (cytoplasm) compartments.",
                 "The smooth endoplasmic reticulum is the major site for the synthesis of lipids.",
                 True, True, False, "B",
                 "Structure and function of the ER",
                 "Both statements are true. A describes how the network of the ER divides the space inside the cell. "
                 "R describes a function of the smooth ER (lipid synthesis, and steroidal hormones in animal cells). "
                 "Lipid synthesis has nothing to do with how the ER compartmentalises the cell, so R does not explain "
                 "A.",
                 ["A: true", "R: true", "R is a function, unrelated to compartmentalisation"],
                 ncert=ref("CELL", "Endomembrane System (The Endoplasmic Reticulum)"), secs=40)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "Which of the following statements comparing prokaryotic and eukaryotic cells are correct?",
                [("Both have a plasma membrane and ribosomes.", True),
                 ("Mesosomes, formed by extensions of the plasma membrane into the cell, are characteristic of "
                  "prokaryotes.", True),
                 ("The inclusion bodies of prokaryotes are not bounded by any membrane system.", True),
                 ("Prokaryotic cells have membrane-bound organelles such as mitochondria.", False),
                 ("The genomic DNA of both is enclosed in a nuclear envelope.", False)],
                ["abcd", "bce", "ace"], "A",
                "Prokaryotic and eukaryotic cells compared",
                "Plasma membrane and ribosomes are common to all cells. Mesosomes, a specialised differentiated "
                "form of the cell membrane, are characteristic of prokaryotes. Reserve material in prokaryotes is "
                "stored as inclusion bodies, not bounded by any membrane. Prokaryotes lack membrane-bound organelles "
                "and a nuclear envelope; these are features of eukaryotic cells.",
                ["(a), (b), (c): true", "(d), (e): false"],
                why="Each wrong combination includes (d) or (e), or leaves out a true statement.",
                ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells"), secs=55)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
       "An organelle is bounded by two membranes, of which the inner one is relatively less permeable. Inside it "
       "are flattened membranous sacs stacked like piles of coins, and its matrix contains small double-stranded "
       "circular DNA and 70S ribosomes. The organelle is the:",
       "chloroplast",
       ["mitochondrion", "Golgi apparatus", "nucleus"], "C",
       "Identifying the chloroplast",
       "The chloroplast is double membrane-bound, and its inner membrane is relatively less permeable. The "
       "thylakoids are arranged in stacks like piles of coins called grana. The stroma contains small, "
       "double-stranded circular DNA molecules and 70S ribosomes, and enzymes for synthesis of carbohydrates and "
       "proteins.",
       ["Double membrane + DNA + 70S ribosomes → mitochondrion or chloroplast",
        "Stacks of sacs like piles of coins (grana) → chloroplast"],
       why="A mitochondrion also has two membranes, DNA and 70S ribosomes, but its inner membrane forms cristae, not "
           "stacked sacs. The Golgi apparatus has single-membrane cisternae and no DNA. The nucleus has a double "
           "envelope with pores, but no grana-like stacks and no 70S ribosomes.",
       ncert=ref("CELL", "Plastids; Mitochondria"), secs=45)

assertion_reason(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
                 "Centrioles are present in almost all plant cells.",
                 "Centrioles form the basal bodies of cilia or flagella, and in animal cells they give rise to the "
                 "spindle fibres of the spindle apparatus during cell division.",
                 False, True, False, "D",
                 "Centrioles",
                 "Animal cells have centrioles, which are absent in almost all plant cells, so A is false. R is "
                 "true: centrioles form the basal body of cilia or flagella, and spindle fibres that give rise to the "
                 "spindle apparatus during cell division in animal cells.",
                 ["A: false, centrioles are absent in almost all plant cells", "R: true"],
                 ncert=ref("CELL", "Centrosome and Centrioles; Eukaryotic Cells"), secs=40)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "Both the bacterial flagellum and the eukaryotic flagellum have a 9 + 2 axoneme.",
               "Fimbriae help some bacteria attach to rocks in streams and also to the host tissues.",
               False, True, "D",
               "Surface structures of bacteria",
               "The bacterial flagellum is composed of three parts, the filament, hook and basal body; NCERT notes that "
               "prokaryotic bacteria have flagella that are structurally different from those of eukaryotes, which "
               "have a 9 + 2 axoneme. Fimbriae are small bristle-like fibres; in some bacteria they help attach the "
               "cell to rocks in streams and to host tissues.",
               ["Statement I: false, bacterial flagellum = filament, hook, basal body", "Statement II: true"],
               ncert=ref("CELL", "Prokaryotic Cells; Cilia and Flagella"), secs=40)

direct(T_CELL, "Prokaryotic cell", "Advanced",
       "A prokaryotic 70S ribosome is about 15 nm by 20 nm. Which of the following arranges these in increasing "
       "order of size?",
       "Prokaryotic 70S ribosome < Mycoplasma < typical bacterium < human red blood cell",
       ["Mycoplasma < prokaryotic 70S ribosome < typical bacterium < human red blood cell",
        "Prokaryotic 70S ribosome < Mycoplasma < human red blood cell < typical bacterium",
        "Typical bacterium < Mycoplasma < prokaryotic 70S ribosome < human red blood cell"], "B",
       "Comparing sizes",
       "The stem gives the ribosome as about 15 nm by 20 nm (0.015–0.02 µm). NCERT gives Mycoplasma as about 0.3 µm, "
       "a typical bacterium as 3–5 µm and a human red blood cell as about 7.0 µm in diameter. So the order is ribosome < "
       "Mycoplasma < bacterium < red blood cell.",
       ["Ribosome ≈ 0.02 µm", "Mycoplasma 0.3 µm", "Bacterium 3–5 µm", "RBC ≈ 7 µm"],
       why="Mycoplasma (0.3 µm) is larger than a ribosome (20 nm). A typical bacterium (3–5 µm) is smaller than a "
           "red blood cell (7 µm). The last option reverses the first three.",
       ncert=ref("CELL", "An Overview of Cell; Prokaryotic Cells"), secs=50)

# =============================================================== 6. Cell Cycle and Cell Division (4/6/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "In the cell cycle, the replicated chromosomes (DNA) are distributed to the daughter nuclei by a complex "
       "series of events during cell division. According to NCERT, these events are themselves:",
       "under genetic control",
       ["random and uncontrolled", "controlled only by temperature", "controlled only by light"], "A",
       "Control of the cell cycle",
       "The cell cycle is the sequence of events by which a cell duplicates its genome, synthesises the other "
       "constituents of the cell and eventually divides. The replicated chromosomes are distributed to the "
       "daughter nuclei by a complex series of events, and these events are themselves under genetic control.",
       ["Events of cell division → under genetic control"],
       why="NCERT describes the events as genetically controlled, not random or governed only by an external "
           "factor.",
       ncert=ref("CC", "Cell Cycle"), secs=20)

direct(T_CC, "Meiosis", "Basic",
       "Which division reduces the number of chromosomes to half, so that the two cells formed have half the "
       "chromosome number of the parent cell?",
       "Meiosis I",
       ["Meiosis II", "Mitosis", "Interkinesis"], "D",
       "Reductional division",
       "In anaphase I the homologous chromosomes separate while sister chromatids remain together, so each of the "
       "two cells formed at the end of meiosis I has half the number of chromosomes of the parent meiocyte. "
       "Meiosis II separates sister chromatids and does not change the chromosome number, like mitosis.",
       ["Meiosis I: homologues separate → chromosome number halved"],
       why="Meiosis II and mitosis keep the chromosome number unchanged. Interkinesis is the short stage between the "
           "two meiotic divisions, not a division.",
       ncert=ref("CC", "Meiosis (Meiosis I)"), secs=20)

match_list(T_CC, "Mitosis", "Basic", "term", "meaning",
           ["Karyokinesis", "Cytokinesis", "Interkinesis", "Syncytium"],
           ["Stage between the two meiotic divisions", "Division of the cytoplasm",
            "Multinucleate condition formed when karyokinesis is not followed by cytokinesis",
            "Separation of daughter chromosomes, i.e. nuclear division"],
           "IV II I III", ["II IV I III", "IV II III I", "I II IV III"], "B",
           "Terms used in cell division",
           "The M phase starts with karyokinesis, the nuclear division (separation of daughter chromosomes), and ends "
           "with cytokinesis, the division of the cytoplasm. When karyokinesis is not followed by cytokinesis, a "
           "multinucleate condition arises, leading to a syncytium (e.g. the liquid endosperm of coconut). The stage "
           "between the two meiotic divisions is interkinesis.",
           ["Karyokinesis → nuclear division", "Cytokinesis → cytoplasmic division", "Interkinesis → between meiosis "
            "I and II", "Syncytium → multinucleate"],
           why="The wrong codes swap karyokinesis and cytokinesis, interkinesis and syncytium, or karyokinesis and "
               "interkinesis.",
           ncert=ref("CC", "M Phase; Meiosis"), secs=35)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "Interphase is divided into three further phases: G1, S and G2.",
               "In the S phase, the DNA content doubles from 2C to 4C and the number of chromosomes also doubles.",
               True, False, "C",
               "Sub-phases of interphase and the S phase",
               "Interphase consists of the G1 phase (Gap 1), the S phase (synthesis) and the G2 phase (Gap 2). In the "
               "S phase the amount of DNA per cell doubles (2C → 4C), but there is no increase in the chromosome "
               "number; a cell with 2n chromosomes in G1 still has 2n after the S phase.",
               ["Statement I: true", "Statement II: false, chromosome number does not change in S phase"],
               ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=30)

numerical(T_CC, "Cell cycle phases", "Intermediate",
          "Yeast can progress through the cell cycle in about 90 minutes. Starting from a single yeast cell, and "
          "assuming every cell completes a cycle and divides into two every 90 minutes, how many cells will be "
          "present after 6 hours?",
          "16",
          ["4", "8", "32"], "B",
          (2 ** ((6 * 60) // 90) == 16),
          "Cell number after repeated cycles",
          "6 hours = 360 minutes. Number of cycles = 360 / 90 = 4. Each cycle doubles the number of cells, so the "
          "number of cells = 2⁴ = 16.",
          ["Cycles = 360 / 90 = 4", "Cells = 2⁴ = 16"],
          why="4 is the number of cycles, not cells. 8 counts only three doublings. 32 counts five doublings.",
          ncert=ref("CC", "Cell Cycle"), secs=45)

assertion_reason(T_CC, "Meiosis", "Intermediate",
                 "Meiosis produces four haploid cells from one diploid meiocyte.",
                 "Meiosis involves two sequential cycles of nuclear and cell division but only a single cycle of DNA "
                 "replication.",
                 True, True, True, "A",
                 "Why meiosis gives four haploid cells",
                 "The DNA of the meiocyte replicates once (in the preceding S phase), and the cell then divides twice, "
                 "in meiosis I and meiosis II. Two divisions give four cells, and because there is only one round of "
                 "replication for two divisions, each cell receives half the chromosome number. So R explains A.",
                 ["A: true", "R: true; one replication + two divisions → four haploid cells"],
                 ncert=ref("CC", "Meiosis"), secs=35)

direct(T_CC, "Cell cycle phases", "Intermediate",
       "A cell of a diploid plant has 2n chromosomes and 4C DNA. Its chromosomes have not yet condensed, and its "
       "nuclear envelope and nucleolus are intact. The cell is most likely in the:",
       "G2 phase",
       ["G1 phase", "telophase II", "G0 phase"], "B",
       "Identifying a phase from DNA content",
       "DNA doubles from 2C to 4C in the S phase while the chromosome number stays 2n. A cell with 4C DNA whose "
       "chromosomes are still uncondensed, with an intact nucleus, has completed S but not begun prophase, so it is "
       "in G2, when proteins are synthesised in preparation for mitosis.",
       ["4C + 2n + intact nucleus → after S, before prophase → G2"],
       why="G1 and G0 cells have 2C DNA. A nucleus at telophase II has n chromosomes and 1C DNA.",
       ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=40)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following statements about cytokinesis in a plant cell are correct?",
                [("The new cell wall begins as a simple precursor called the cell plate.", True),
                 ("Wall formation starts in the centre of the cell and grows outward to meet the existing lateral "
                  "walls.", True),
                 ("Cytokinesis takes place by a furrow in the plasma membrane that deepens towards the centre.",
                  False),
                 ("Organelles such as mitochondria and plastids get distributed between the two daughter cells.",
                  True),
                 ("The cell plate later becomes the secondary wall.", False)],
                ["abc", "bde", "ade"], "D",
                "Cytokinesis in plant cells",
                "Plant cells are enclosed by a relatively inextensible cell wall, so cytokinesis is by cell plate "
                "formation, not furrowing. Wall formation starts in the centre and grows outward to meet the lateral "
                "walls. The cell plate represents the middle lamella between the walls of two adjacent cells. At "
                "cytokinesis, organelles like mitochondria and plastids are distributed between the daughter cells.",
                ["(a), (b), (d): true", "(c): false, furrowing is seen in animal cells",
                 "(e): false, the cell plate represents the middle lamella"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("CC", "M Phase (Cytokinesis)"), secs=50)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Interkinesis is generally long-lived, and DNA replicates during it.",
               "Anaphase I separates homologous chromosomes, while anaphase II separates sister chromatids.",
               False, True, "D",
               "Interkinesis and the two anaphases",
               "The stage between the two meiotic divisions, interkinesis, is generally short-lived, and there is no "
               "replication of DNA during it. In anaphase I the homologous chromosomes separate while the sister "
               "chromatids stay associated at their centromeres; in anaphase II the centromere of each chromosome "
               "splits and the sister chromatids move to opposite poles.",
               ["Statement I: false, interkinesis is short and has no DNA replication", "Statement II: true"],
               ncert=ref("CC", "Meiosis (Meiosis I; Meiosis II)"), secs=35)

assertion_reason(T_CC, "Cell cycle phases", "Intermediate",
                 "Cells in the quiescent stage (G0) remain metabolically active.",
                 "Cells in G0 keep proliferating continuously, whatever the requirement of the organism.",
                 True, False, False, "C",
                 "The quiescent stage",
                 "Cells that do not divide further exit G1 and enter G0. Cells in this stage remain metabolically "
                 "active but no longer proliferate unless called on to do so, depending on the requirement of the "
                 "organism. So A is true and R is false.",
                 ["A: true", "R: false, G0 cells do not proliferate unless called on to do so"],
                 ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=35)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements about a cell at metaphase II of meiosis in a diploid (2n) "
                "organism are correct?",
                [("The cell has n chromosomes.", True),
                 ("Each chromosome has two chromatids.", True),
                 ("The homologous chromosomes are paired as bivalents.", False),
                 ("Microtubules from opposite poles attach to the kinetochores of the sister chromatids.", True),
                 ("The cell has 4C DNA.", False)],
                ["abcd", "bde", "ad"], "C",
                "A cell at metaphase II",
                "Meiosis I separates homologous chromosomes, so each cell entering meiosis II has n chromosomes, each "
                "still made of two sister chromatids (2C DNA, half of the 4C of the meiocyte after S phase). At "
                "metaphase II the chromosomes align at the equator and microtubules from opposite poles attach to "
                "the kinetochores of sister chromatids. Bivalents exist only in prophase I and metaphase I.",
                ["n chromosomes × 2 chromatids → 2C DNA", "No bivalents in meiosis II"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("CC", "Meiosis (Meiosis II)"), secs=60)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "In the oocytes of some vertebrates, diplotene can last for months or years.",
                 "Diakinesis is marked by terminalisation of chiasmata.",
                 True, True, False, "B",
                 "Diplotene and diakinesis",
                 "Both statements are true. A concerns the duration of diplotene in vertebrate oocytes. R describes the "
                 "next stage, diakinesis, in which chiasmata terminalise. The terminalisation of chiasmata in a later "
                 "stage does not explain why diplotene is prolonged, so R is not the explanation of A.",
                 ["A: true", "R: true", "R describes a different stage; it does not explain A"],
                 ncert=ref("CC", "Meiosis (Prophase I)"), secs=40)

direct(T_CC, "Meiosis", "Advanced",
       "Which of the following takes place in anaphase I of meiosis, but in neither the anaphase of mitosis nor "
       "anaphase II of meiosis?",
       "Separation of homologous chromosomes, while sister chromatids remain associated at their centromeres",
       ["Splitting of the centromeres", "Movement of chromosomes towards the opposite poles",
        "Shortening of the microtubules attached to the kinetochores"], "A",
       "Anaphases compared",
       "In anaphase I the homologous chromosomes separate, while the sister chromatids remain associated at their "
       "centromeres. In the anaphase of mitosis and in anaphase II the centromeres split and sister chromatids "
       "separate. Movement towards the poles occurs in all three anaphases.",
       ["Anaphase I: homologues separate, centromeres intact",
        "Mitotic anaphase and anaphase II: centromeres split, chromatids separate"],
       why="Splitting of the centromere occurs in mitotic anaphase and anaphase II, not anaphase I. Poleward movement "
           "and the shortening of kinetochore microtubules are not unique to anaphase I.",
       ncert=ref("CC", "M Phase (Anaphase); Meiosis"), secs=45)

statement_pair(T_CC, "Cell cycle phases", "Advanced",
               "Cell growth, in terms of cytoplasmic increase, continues through the cell cycle, but DNA is "
               "synthesised in only one specific stage.",
               "In animal cells, DNA replication begins in the nucleus during the S phase, while the centriole "
               "duplicates in the cytoplasm.",
               True, True, "A",
               "Growth and DNA synthesis in the cell cycle",
               "NCERT states that although cell growth (in terms of cytoplasmic increase) is a continuous process, "
               "DNA synthesis occurs only during one specific stage, the S phase. In animal cells, during the S "
               "phase, DNA replication begins in the nucleus and the centriole duplicates in the cytoplasm.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=35)

# =============================================================== 7. Photosynthesis (5/6/5)
direct(T_PS, "Site and pigments", "Basic",
       "A graph that shows the rate of photosynthesis at different wavelengths of light is called the:",
       "action spectrum",
       ["absorption spectrum", "Z scheme", "chromatogram"], "C",
       "Action spectrum",
       "A graph of the absorption of light of different wavelengths by a pigment is its absorption spectrum. A graph "
       "of the rate of photosynthesis against wavelength is the action spectrum. NCERT superimposes the two to show "
       "that most photosynthesis takes place in the blue and red regions, where chlorophyll a absorbs most.",
       ["Rate of photosynthesis vs wavelength → action spectrum"],
       why="The absorption spectrum plots light absorbed by a pigment, not the rate of photosynthesis. The Z scheme "
           "shows electron carriers on a redox scale. A chromatogram separates pigments.",
       ncert=ref("PS", "What is our Understanding of the Pigments Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Site and pigments", "Basic",
       "Which of the following leaf pigments is NOT an accessory pigment?",
       "Chlorophyll a",
       ["Chlorophyll b", "Xanthophylls", "Carotenoids"], "D",
       "Chief and accessory pigments",
       "Chlorophyll a is the chief pigment associated with photosynthesis and forms the reaction centre. Chlorophyll "
       "b, xanthophylls and carotenoids are called accessory pigments: they also absorb light and transfer the "
       "energy to chlorophyll a.",
       ["Chief pigment: chlorophyll a", "Accessory: chlorophyll b, xanthophylls, carotenoids"],
       why="Chlorophyll b, xanthophylls and carotenoids are the accessory pigments named by NCERT.",
       ncert=ref("PS", "What is our Understanding of the Pigments Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "In the leaves of a plant, large bundle sheath cells with many chloroplasts, thick walls and no intercellular "
       "spaces form a wreath around the vascular bundles. Which of the following plants shows this anatomy?",
       "Maize",
       ["Tomato", "Bell pepper", "Chlamydomonas"], "A",
       "Kranz anatomy of C4 plants",
       "This is Kranz ('wreath') anatomy, a characteristic of C4 plants such as maize and sorghum. The bundle sheath "
       "cells have a large number of chloroplasts, thick walls impervious to gaseous exchange and no intercellular "
       "spaces. Tomato and bell pepper are named by NCERT as C3 plants grown in CO₂-enriched greenhouses.",
       ["Wreath of bundle sheath cells → Kranz anatomy → C4 plant (maize)"],
       why="Tomato and bell pepper are C3 plants. Chlamydomonas is a unicellular green alga with no leaves or "
           "vascular bundles.",
       ncert=ref("PS", "The C4 Pathway"), secs=25)

statement_pair(T_PS, "Site and pigments", "Basic",
               "In photosynthesis, green plants use light energy to drive the synthesis of organic compounds.",
               "The oxygen released in photosynthesis comes from the splitting of water.",
               True, True, "A",
               "Nature of photosynthesis",
               "Photosynthesis is a physico-chemical process by which green plants use light energy to drive the "
               "synthesis of organic compounds. In the light reaction, water is split into H⁺, [O] and electrons on "
               "the inner side of the thylakoid membrane, and the oxygen evolved comes from this splitting of "
               "water.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Introduction; The Electron Transport (Splitting of Water)"), secs=25)

direct(T_PS, "Site and pigments", "Basic",
       "The light-harvesting complexes (LHC) of Photosystem I and Photosystem II are located in the:",
       "thylakoid membranes of the chloroplast",
       ["stroma of the chloroplast", "outer membrane of the chloroplast envelope",
        "inner membrane of the mitochondrion"], "B",
       "Location of the photosystems",
       "Within the chloroplast, the membrane system (grana and stroma lamellae) is responsible for trapping light "
       "energy. The pigments are organised into two discrete light-harvesting complexes within PS I and PS II, "
       "located in the thylakoid membranes. The stroma carries out the enzymatic reactions that synthesise sugar.",
       ["Light trapping → membrane system (thylakoids)", "Stroma → enzymatic (sugar-forming) reactions"],
       why="The stroma is the site of the biosynthetic phase. The chloroplast envelope and the mitochondrial "
           "membrane do not contain the photosystems.",
       ncert=ref("PS", "Where does Photosynthesis Take Place?; What is Light Reaction?"), secs=25)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                 "Oxygen is evolved in non-cyclic photophosphorylation but not in cyclic photophosphorylation.",
                 "The water splitting complex is associated with PS II, which does not take part in cyclic "
                 "photophosphorylation.",
                 True, True, True, "A",
                 "Why cyclic photophosphorylation releases no oxygen",
                 "Water is split by the water splitting complex associated with PS II, and this is the source of the "
                 "oxygen evolved. In non-cyclic photophosphorylation PS II and PS I work in series, so water is split "
                 "and O₂ released. In cyclic photophosphorylation only PS I is functional and the electron is "
                 "circulated within it, so no water is split and no O₂ is evolved. R directly explains A.",
                 ["A: true", "R: true; no PS II in the cyclic flow → no water splitting → no O₂"],
                 ncert=ref("PS", "Splitting of Water; Cyclic and Non-cyclic Photo-phosphorylation"), secs=40)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following are listed by NCERT as special features of C4 plants?",
                [("A special type of leaf anatomy", True),
                 ("Tolerance of higher temperatures", True),
                 ("A response to high light intensities", True),
                 ("Lack of photorespiration", True),
                 ("A lower productivity of biomass than C3 plants", False)],
                ["abce", "bcd", "acde"], "B",
                "Features of C4 plants",
                "NCERT states that C4 plants are special: they have a special type of leaf anatomy (Kranz anatomy), "
                "they tolerate higher temperatures, they show a response to high light intensities, they lack a "
                "process called photorespiration, and they have greater productivity of biomass.",
                ["(a)–(d): true", "(e): false, C4 plants have greater productivity of biomass"],
                why="Each wrong combination includes (e) or leaves out one of the true features.",
                ncert=ref("PS", "The C4 Pathway"), secs=45)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following are consumed in the Calvin cycle?",
                [("CO₂", True), ("ATP", True), ("NADPH", True), ("O₂", False), ("Phosphoenol pyruvate (PEP)", False)],
                ["abcd", "bce", "ac"], "C",
                "Inputs of the Calvin cycle",
                "The Calvin cycle fixes CO₂ (carboxylation), uses ATP for phosphorylation and NADPH for reduction "
                "(reduction stage), and uses ATP to regenerate RuBP. O₂ is a product of the light reaction, not an "
                "input of the Calvin cycle, and PEP is the CO₂ acceptor of the C4 pathway in mesophyll cells.",
                ["Inputs: CO₂, ATP, NADPH", "O₂: product of light reaction; PEP: C4 pathway"],
                why="Each wrong combination includes O₂ or PEP, or leaves out one of the inputs.",
                ncert=ref("PS", "The Calvin Cycle"), secs=40)

assertion_reason(T_PS, "Photorespiration", "Intermediate",
                 "Photorespiration results in the synthesis of sugars and ATP.",
                 "In photorespiration, RuBP combines with O₂ to form one molecule of PGA and one of "
                 "phosphoglycolate.",
                 False, True, False, "D",
                 "Photorespiration",
                 "In the photorespiratory pathway, RuBP binds O₂ instead of CO₂ and forms one molecule of PGA and "
                 "phosphoglycolate. There is neither synthesis of sugars nor of ATP and NADPH; rather, CO₂ is released "
                 "with the utilisation of ATP. So A is false and R is true.",
                 ["A: false, no sugar or ATP is synthesised", "R: true"],
                 ncert=ref("PS", "Photorespiration"), secs=35)

match_list(T_PS, "Calvin cycle and C4 pathway", "Intermediate", "quantity in the Calvin cycle", "number",
           ["ATP used for every CO₂ fixed", "NADPH used for every CO₂ fixed",
            "Turns of the cycle needed to make one glucose", "ATP used to make one glucose"],
           ["18", "2", "6", "3"],
           "IV II III I", ["II IV III I", "IV II I III", "III II IV I"], "C",
           "Energy accounting of the Calvin cycle",
           "For every CO₂ molecule entering the Calvin cycle, 3 molecules of ATP and 2 of NADPH are required. Six "
           "turns of the cycle are needed to make one molecule of glucose, so one glucose uses 6 × 3 = 18 ATP and "
           "6 × 2 = 12 NADPH.",
           ["Per CO₂: 3 ATP, 2 NADPH", "Per glucose: 6 turns, 18 ATP (12 NADPH)"],
           why="The wrong codes swap ATP and NADPH per CO₂, swap turns and total ATP, or confuse ATP per CO₂ with "
               "the number of turns.",
           ncert=ref("PS", "The Calvin Cycle"), secs=45)

direct(T_PS, "Light reactions and photophosphorylation", "Intermediate",
       "Which sequence correctly shows the path of electrons in non-cyclic photophosphorylation?",
       "H₂O → PS II → electron transport chain (cytochromes) → PS I → NADP⁺",
       ["H₂O → PS I → electron transport chain → PS II → NADP⁺",
        "NADP⁺ → PS I → electron transport chain → PS II → H₂O",
        "H₂O → PS II → NADP⁺ → PS I → electron transport chain"], "A",
       "The Z scheme",
       "Electrons lost by PS II are replaced by electrons from the splitting of water. Electrons excited in PS II "
       "pass through an electron transport system of cytochromes to PS I, not being used up on the way. Electrons "
       "excited in PS I are passed through another chain to NADP⁺, reducing it to NADPH + H⁺.",
       ["Water → PS II", "PS II → cytochromes → PS I", "PS I → NADP⁺"],
       why="The second option begins at PS I, the third runs backwards, and the fourth places NADP⁺ before PS I.",
       ncert=ref("PS", "The Electron Transport"), secs=40)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "The bundle sheath cells of C4 plants have a large number of chloroplasts.",
                 "Within the mesophyll cells, the chloroplasts align themselves along the walls so that they get the "
                 "optimum quantity of incident light.",
                 True, True, False, "B",
                 "Chloroplasts in two kinds of cells",
                 "Both statements are true. A describes the bundle sheath cells of C4 plants (Kranz anatomy). R "
                 "describes how chloroplasts are positioned within mesophyll cells in response to light. The "
                 "positioning of chloroplasts in mesophyll cells says nothing about why bundle sheath cells of C4 "
                 "plants are rich in chloroplasts, so R does not explain A.",
                 ["A: true", "R: true", "R concerns a different cell type and a different feature"],
                 ncert=ref("PS", "Where does Photosynthesis Take Place?; The C4 Pathway"), secs=45)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                "A plant that has been in bright light is suddenly placed in darkness. Which of the following can "
                "continue for some time before stopping?",
                [("Carboxylation of RuBP by RuBisCO", True),
                 ("Splitting of water", False),
                 ("Photophosphorylation", False),
                 ("Reduction of PGA using NADPH", True),
                 ("Regeneration of RuBP", True)],
                ["abe", "cde", "ad"], "D",
                "Dependence of the biosynthetic phase on light",
                "The biosynthetic (Calvin) reactions do not directly depend on light; they depend on the ATP and "
                "NADPH made in the light reaction. So, immediately after light becomes unavailable, carboxylation, "
                "reduction and regeneration continue for some time, using the ATP and NADPH already formed, and then "
                "stop. Splitting of water and photophosphorylation are parts of the light reaction and stop when "
                "light is withdrawn.",
                ["Calvin cycle steps: continue briefly", "Light reaction steps: stop"],
                why="Each wrong combination includes a light reaction step or leaves out one of the Calvin cycle "
                    "steps.",
                ncert=ref("PS", "Where are the ATP and NADPH Used?"), secs=55)

direct(T_PS, "Limiting factors", "Advanced",
       "A maize plant and a tomato plant are grown side by side on a hot, brightly lit day. Which outcome is "
       "expected, and why?",
       "Maize shows the higher rate of photosynthesis, because C4 plants have a higher temperature optimum, respond "
       "to high light intensities and lack photorespiration",
       ["Tomato shows the higher rate, because C3 plants have a higher temperature optimum than C4 plants",
        "Both show equal rates, because light is never a limiting factor",
        "Maize stops photosynthesis, because high temperature denatures PEP carboxylase in C4 plants"], "D",
       "C3 and C4 plants under heat and strong light",
       "C4 plants respond to higher temperatures and show a higher rate of photosynthesis, while C3 plants have a "
       "much lower temperature optimum. C4 plants also respond to high light intensities and lack photorespiration, "
       "which decreases CO₂ fixation in C3 plants.",
       ["Maize: C4 → higher temperature optimum, no photorespiration", "Tomato: C3 → lower optimum"],
       why="C3 plants have a lower, not higher, temperature optimum. NCERT does not say light is never limiting "
           "(it limits shade plants), and C4 plants are tolerant of high temperatures.",
       ncert=ref("PS", "The C4 Pathway; Factors Affecting Photosynthesis (Temperature)"), secs=50)

statement_pair(T_PS, "Chemiosmosis", "Advanced",
               "The splitting of water and the reduction of NADP⁺ take place on the same side of the thylakoid "
               "membrane.",
               "The protons needed to reduce NADP⁺ to NADPH + H⁺ are removed from the stroma.",
               False, True, "D",
               "Sides of the thylakoid membrane",
               "The splitting of water takes place on the inner (lumen) side of the thylakoid membrane, so its "
               "protons accumulate in the lumen. NADP reductase is located on the stroma side, and the protons "
               "needed to reduce NADP⁺ are removed from the stroma. The two events are on opposite sides, which "
               "helps build the proton gradient.",
               ["Statement I: false, water splitting = lumen side, NADP⁺ reduction = stroma side",
                "Statement II: true"],
               ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=40)

direct(T_PS, "Calvin cycle and C4 pathway", "Advanced",
       "Which sequence correctly traces atmospheric CO₂ through the C4 pathway?",
       "CO₂ + PEP → OAA in mesophyll cells → malic or aspartic acid → transported to bundle sheath cells → CO₂ "
       "released → fixed by RuBisCO into PGA",
       ["CO₂ + RuBP → PGA in mesophyll cells → OAA → transported to bundle sheath cells → PEP",
        "CO₂ + PEP → OAA in bundle sheath cells → malic acid → transported to mesophyll cells → CO₂ fixed by "
        "RuBisCO",
        "CO₂ + PEP → PGA in mesophyll cells → OAA in bundle sheath cells → RuBP"], "C",
       "Path of carbon in the C4 pathway",
       "In the mesophyll cells, PEPcase fixes CO₂ with PEP to form OAA, a C4 acid. OAA is converted to malic or "
       "aspartic acid, which is transported to the bundle sheath cells. There the C4 acid is broken down to release "
       "CO₂ and a 3-carbon molecule; the CO₂ enters the Calvin cycle, where RuBisCO fixes it with RuBP to form PGA.",
       ["Mesophyll: PEP + CO₂ → OAA → malic/aspartic acid", "Bundle sheath: decarboxylation → CO₂ → Calvin cycle"],
       why="The first option uses RuBisCO in the mesophyll, which lacks it. The third places PEPcase in the bundle "
           "sheath and RuBisCO in the mesophyll. The fourth makes PGA the product of PEP carboxylation.",
       ncert=ref("PS", "The C4 Pathway"), secs=50)

# =============================================================== 8. Respiration in Plants (4/5/4)
direct(T_RES, "Electron transport system", "Basic",
       "In ATP synthase (complex V), the part that is an integral membrane protein complex forming the channel "
       "through which protons cross the inner mitochondrial membrane is:",
       "F₀",
       ["the F₁ headpiece", "cytochrome c", "ubiquinone"], "C",
       "Parts of ATP synthase",
       "ATP synthase has two major components, F₁ and F₀. The F₁ headpiece is a peripheral membrane protein complex "
       "and contains the site for synthesis of ATP from ADP and inorganic phosphate. F₀ is an integral membrane "
       "protein complex that forms the channel through which protons cross the inner membrane.",
       ["F₀: integral, proton channel", "F₁: peripheral headpiece, site of ATP synthesis"],
       why="The F₁ headpiece contains the ATP-synthesising site, not the channel. Cytochrome c and ubiquinone are "
           "electron carriers, not parts of ATP synthase.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=25)

direct(T_RES, "Glycolysis and fermentation", "Basic",
       "Which of the following processes is common to aerobic respiration, alcoholic fermentation and lactic acid "
       "fermentation?",
       "Glycolysis",
       ["The TCA cycle", "Oxidative decarboxylation of pyruvic acid to acetyl CoA",
        "The electron transport system"], "B",
       "Glycolysis as the common first stage",
       "In all three, glucose is first broken down to pyruvic acid by glycolysis in the cytoplasm. The fate of "
       "pyruvic acid then differs: it is reduced to ethanol and CO₂ or to lactic acid in fermentation, or enters "
       "the mitochondria for the link reaction, the TCA cycle and the ETS in aerobic respiration.",
       ["Glycolysis → common", "Link reaction, TCA cycle, ETS → aerobic respiration only"],
       why="The link reaction, the TCA cycle and the ETS occur only in aerobic respiration.",
       ncert=ref("RES", "Glycolysis; Fermentation; Aerobic Respiration"), secs=25)

assertion_reason(T_RES, "Glycolysis and fermentation", "Basic",
                 "Anaerobic organisms can obtain energy from glucose without using oxygen.",
                 "All living organisms retain the enzymatic machinery to partially oxidise glucose without the help "
                 "of oxygen.",
                 True, True, True, "A",
                 "Respiration without oxygen",
                 "The breakdown of glucose to pyruvic acid (glycolysis) does not need oxygen, and all living organisms "
                 "retain the enzymes for it. In anaerobic organisms glycolysis is the only process of respiration, "
                 "and it releases some energy as ATP. So R explains A.",
                 ["A: true", "R: true; this machinery (glycolysis) is what lets them obtain energy"],
                 ncert=ref("RES", "Glycolysis"), secs=30)

direct(T_RES, "Electron transport system", "Basic",
       "In the electron transport system, electrons from NADH are oxidised by NADH dehydrogenase (complex I) and "
       "transferred to ubiquinone. Ubiquinone is located:",
       "within the inner mitochondrial membrane",
       ["in the outer mitochondrial membrane", "free in the cytoplasm", "in the thylakoid lumen"], "D",
       "Location of ubiquinone",
       "The ETS is present in the inner mitochondrial membrane. Electrons from NADH produced in the matrix are "
       "oxidised by complex I and transferred to ubiquinone located within the inner membrane. Ubiquinone also "
       "receives reducing equivalents from FADH₂ through complex II.",
       ["ETS → inner mitochondrial membrane", "Ubiquinone → within the inner membrane"],
       why="The outer membrane and the cytoplasm do not carry the ETS. The thylakoid lumen belongs to the "
           "chloroplast.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=25)

match_list(T_RES, "Glycolysis and fermentation", "Intermediate", "step of glycolysis", "what happens",
           ["Glucose → glucose-6-phosphate", "Glucose-6-phosphate → fructose-6-phosphate",
            "PGAL → 1,3-bisphosphoglyceric acid (BPGA)", "Phosphoenolpyruvate → pyruvic acid"],
           ["Synthesis of ATP", "Oxidation, with formation of NADH + H⁺", "Isomerisation",
            "Phosphorylation catalysed by hexokinase"],
           "IV III II I", ["IV II III I", "III IV II I", "IV III I II"], "B",
           "Steps of glycolysis",
           "Glucose is phosphorylated to glucose-6-phosphate by hexokinase, which is then isomerised to "
           "fructose-6-phosphate. Later, PGAL is oxidised (two redox equivalents are removed and transferred to NAD⁺, "
           "forming NADH + H⁺) and combined with inorganic phosphate to form BPGA. ATP is synthesised when BPGA forms "
           "PGA and again when PEP is converted to pyruvic acid.",
           ["Glucose → G6P: hexokinase", "G6P → F6P: isomerisation", "PGAL → BPGA: NADH", "PEP → pyruvate: ATP"],
           why="The wrong codes swap isomerisation with oxidation, phosphorylation with isomerisation, or the "
               "NADH-forming step with the ATP-forming step.",
           ncert=ref("RES", "Glycolysis"), secs=45)

assertion_reason(T_RES, "TCA cycle", "Intermediate",
                 "CO₂ is released when pyruvic acid is converted to acetyl CoA.",
                 "The conversion of pyruvic acid to acetyl CoA takes place in the cytoplasm.",
                 True, False, False, "C",
                 "The link reaction",
                 "Pyruvic acid formed in glycolysis enters the mitochondrial matrix, where it undergoes oxidative "
                 "decarboxylation by pyruvic dehydrogenase: pyruvic acid + CoA + NAD⁺ → acetyl CoA + CO₂ + NADH + H⁺. "
                 "So CO₂ is released, but the reaction occurs in the mitochondrial matrix, not the cytoplasm.",
                 ["A: true", "R: false, the reaction is in the mitochondrial matrix"],
                 ncert=ref("RES", "Aerobic Respiration"), secs=35)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "In which of the following conversions is CO₂ released?",
                [("Pyruvic acid → acetyl CoA", True),
                 ("Formation of α-ketoglutaric acid in the TCA cycle", True),
                 ("α-Ketoglutaric acid → succinyl CoA", True),
                 ("Succinyl CoA → succinic acid", False),
                 ("Pyruvic acid → lactic acid", False)],
                ["abcd", "bce", "ac"], "D",
                "Decarboxylation steps",
                "CO₂ is released in the oxidative decarboxylation of pyruvic acid to acetyl CoA, and in the two "
                "successive decarboxylations of the TCA cycle, which form α-ketoglutaric acid and then succinyl CoA. "
                "The conversion of succinyl CoA to succinic acid synthesises GTP, without decarboxylation, and the "
                "reduction of pyruvic acid to lactic acid releases no CO₂.",
                ["(a), (b), (c): decarboxylations", "(d): GTP synthesis", "(e): reduction, no CO₂"],
                why="Each wrong combination includes (d) or (e), or leaves out a decarboxylation.",
                ncert=ref("RES", "Aerobic Respiration; Tricarboxylic Acid Cycle; Fermentation"), secs=45)

statement_pair(T_RES, "Electron transport system", "Intermediate",
               "Cytochrome c acts as a mobile carrier for the transfer of electrons between complex I and complex III.",
               "Ubiquinone receives reducing equivalents from NADH through complex I and from FADH₂ through complex "
               "II.",
               False, True, "D",
               "Carriers of the ETS",
               "Cytochrome c is a small protein attached to the outer surface of the inner membrane; it acts as a "
               "mobile carrier between complex III (cytochrome bc₁ complex) and complex IV (cytochrome c oxidase). "
               "Ubiquinone receives reducing equivalents from NADH via complex I and from FADH₂ via complex II; "
               "reduced ubiquinone (ubiquinol) is then oxidised by complex III.",
               ["Statement I: false, cytochrome c links complex III and complex IV", "Statement II: true"],
               ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=35)

direct(T_RES, "Glycolysis and fermentation", "Intermediate",
       "Which of the following is true of both lactic acid fermentation and alcoholic fermentation?",
       "Both reoxidise the NADH + H⁺ formed in glycolysis to NAD⁺",
       ["Both release CO₂", "Both take place in the mitochondrial matrix",
        "Both release more energy per glucose than aerobic respiration"], "A",
       "Comparing the two fermentations",
       "In both lactic acid and alcoholic fermentation the reducing agent is NADH + H⁺, which is reoxidised to "
       "NAD⁺ as pyruvic acid is reduced. Alcoholic fermentation releases CO₂ (pyruvic acid → CO₂ + ethanol) but "
       "lactic acid fermentation does not. Both occur in the cytoplasm, and both release less than seven per cent "
       "of the energy in glucose.",
       ["Common: NADH → NAD⁺", "CO₂ only in alcoholic fermentation"],
       why="Lactic acid fermentation releases no CO₂. Fermentation is cytoplasmic. It releases far less energy than "
           "aerobic respiration.",
       ncert=ref("RES", "Fermentation"), secs=35)

multi_statement(T_RES, "Electron transport system", "Advanced",
                "The oxygen supply to a respiring plant cell is completely cut off. Which of the following will stop "
                "or decrease?",
                [("The flow of electrons through the electron transport system", True),
                 ("The continued oxidation of acetyl CoA in the TCA cycle", True),
                 ("Glycolysis", False),
                 ("The ATP yield per molecule of glucose", True),
                 ("The conversion of pyruvic acid to ethanol", False)],
                ["abc", "bde", "ade"], "D",
                "Consequences of the absence of oxygen",
                "Oxygen is the final hydrogen acceptor of the ETS, so without it electron flow stops. The TCA cycle "
                "needs continued regeneration of NAD⁺ and FAD⁺ from NADH and FADH₂ in the ETS, so it also stops. "
                "Glycolysis does not need oxygen and continues, with NAD⁺ regenerated by fermentation, so pyruvic "
                "acid is converted to products such as ethanol. Since only glycolysis yields ATP, the ATP yield per "
                "glucose falls.",
                ["(a), (b), (d): stop or decrease", "(c), (e): continue or start"],
                why="Each wrong combination includes glycolysis or ethanol formation, which continue without oxygen, "
                    "or leaves out a step that stops.",
                ncert=ref("RES", "Fermentation; Electron Transport System (ETS) and Oxidative Phosphorylation"),
                secs=60)

assertion_reason(T_RES, "Electron transport system", "Advanced",
                 "Complex IV, cytochrome c oxidase, contains cytochromes a and a₃ and two copper centres.",
                 "The F₁ headpiece of ATP synthase is a peripheral membrane protein complex that contains the site for "
                 "the synthesis of ATP.",
                 True, True, False, "B",
                 "Two components of the inner mitochondrial membrane",
                 "Both statements are true. A describes the composition of complex IV, which passes electrons to "
                 "oxygen. R describes the F₁ part of ATP synthase (complex V). The structure of ATP synthase has "
                 "nothing to do with the cytochromes and copper centres of complex IV, so R does not explain A.",
                 ["A: true", "R: true", "R describes a different complex"],
                 ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=40)

direct(T_RES, "Electron transport system", "Advanced",
       "Which of the following correctly distinguishes oxidative phosphorylation in mitochondria from "
       "photophosphorylation in chloroplasts?",
       "In oxidative phosphorylation the energy of oxidation-reduction is used to create the proton gradient, "
       "whereas in photophosphorylation light energy is used",
       ["In oxidative phosphorylation light energy creates the proton gradient, whereas in photophosphorylation "
        "the energy of oxidation-reduction is used",
        "Only photophosphorylation uses an ATP synthase to make ATP",
        "Only oxidative phosphorylation requires a proton gradient across a membrane"], "C",
       "Oxidative phosphorylation and photophosphorylation",
       "NCERT points out that in photophosphorylation light energy is used to produce the proton gradient needed for "
       "phosphorylation, while in respiration the energy of oxidation-reduction is used for the same purpose; hence "
       "the name oxidative phosphorylation. Both use a proton gradient across a membrane and an ATP synthase.",
       ["Source of energy for the gradient: redox (mitochondria) vs light (chloroplasts)",
        "Both: proton gradient + ATP synthase"],
       why="The second option reverses the two. Both processes use ATP synthase and both need a proton gradient.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=45)

assertion_reason(T_RES, "ATP yield and amphibolic pathway", "Advanced",
                 "The number of ATP molecules synthesised in the electron transport system depends on the nature of "
                 "the electron donor.",
                 "Oxidation of one molecule of NADH gives rise to 3 molecules of ATP, while that of one molecule of "
                 "FADH₂ produces 2 molecules of ATP.",
                 True, True, True, "A",
                 "ATP yield from different electron donors",
                 "NCERT states that the number of ATP molecules synthesised depends on the nature of the electron "
                 "donor: one NADH gives 3 ATP and one FADH₂ gives 2 ATP. The different yields from the two donors are "
                 "exactly what A states, so R explains A.",
                 ["A: true", "R: true; NADH (3 ATP) and FADH₂ (2 ATP) differ in yield"],
                 ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=40)
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
    assert pkg["output"] == "batches/parts/BATCH_007_BOT_p1.json"


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
           "notes": "Package BOT_007_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 125 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
