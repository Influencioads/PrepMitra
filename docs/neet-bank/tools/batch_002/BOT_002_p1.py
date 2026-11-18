"""Writes batches/parts/BATCH_002_BOT_p1.json: package BOT_002_p1 of batch 2 (Botany, 125 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_000251 .. NEET_BOT_000375.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_002/BOT_002_p1.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_002_BOT_p1.json"
PACKAGE = "BOT_002_p1"
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


def match_list(topic, sub, diff, head1, head2, list1, list2, correct, wrongs, at, concept, expl, steps, why=None,
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
    _fix(rec, _place(_code(correct), [_code(w) for w in wrongs], at), at)
    QUESTIONS.append(rec)


# =============================================================== 1. The Living World and Classification (5/7/5)
direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Based on their shape, bacteria are grouped into four categories. Comma-shaped bacteria are called:",
       "Vibrio", ["Bacillus", "Coccus", "Spirillum"], "B",
       "Shapes of bacteria",
       "Bacteria are grouped by shape into spherical coccus, rod-shaped bacillus, comma-shaped vibrio and spiral "
       "spirillum forms.",
       ["Coccus: spherical", "Bacillus: rod-shaped", "Vibrio: comma-shaped", "Spirillum: spiral"],
       why="Bacillus is rod-shaped, coccus is spherical and spirillum is spiral.",
       ncert=ref("BC", "Kingdom Monera"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "In the NCERT table of organisms with their taxonomic categories, the housefly (Musca domestica) is placed in "
       "the order:",
       "Diptera", ["Primata", "Poales", "Sapindales"], "C",
       "Taxonomic hierarchy of the housefly",
       "The housefly belongs to genus Musca, family Muscidae, order Diptera, class Insecta and phylum Arthropoda.",
       ["Musca → Muscidae → Diptera → Insecta → Arthropoda"],
       why="Primata is the order of man. Poales (wheat) and Sapindales (mango) are plant orders.",
       ncert=ref("LW", "Taxonomic categories (Table: organisms with their taxonomic categories)"), secs=25)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Which organisms completely lack a cell wall, are the smallest living cells known and can survive without "
       "oxygen?",
       "Mycoplasma", ["Cyanobacteria", "Methanogens", "Diatoms"], "D",
       "Mycoplasma",
       "Mycoplasma are organisms that completely lack a cell wall. They are the smallest living cells known and can "
       "survive without oxygen. Many are pathogenic in animals and plants.",
       ["No cell wall + smallest living cells + survive without oxygen → Mycoplasma"],
       why="Cyanobacteria and methanogens are bacteria with a cell wall. Diatoms are protists with silica-embedded "
           "walls.",
       ncert=ref("BC", "Kingdom Monera (Mycoplasma)"), secs=25)

direct(T_LIV, "Lichens, viruses and viroids", "Basic",
       "Who showed that the extract of infected tobacco plants could infect healthy plants and called the fluid "
       "'Contagium vivum fluidum' (infectious living fluid)?",
       "M.W. Beijerinek", ["W.M. Stanley", "Dmitri Ivanowsky", "T.O. Diener"], "A",
       "Discovery of viruses",
       "M.W. Beijerinek (1898) demonstrated that the extract of infected tobacco plants could cause infection in "
       "healthy plants and called the fluid Contagium vivum fluidum.",
       ["Ivanowsky (1892): causal organism of tobacco mosaic smaller than bacteria",
        "Beijerinek (1898): Contagium vivum fluidum", "Stanley (1935): viruses can be crystallised"],
       why="Stanley crystallised viruses, Ivanowsky first recognised the tobacco mosaic agent, and Diener discovered "
           "viroids.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=25)

statement_pair(T_LIV, "Five kingdom classification", "Basic",
               "In Whittaker's five kingdom classification, mode of nutrition was the only criterion used.",
               "The two kingdom classification did not distinguish between eukaryotes and prokaryotes.",
               False, True, "D",
               "Criteria of the five kingdom system; limits of the two kingdom system",
               "Whittaker used several criteria: cell structure, body organisation, mode of nutrition, reproduction "
               "and phylogenetic relationships. The two kingdom system (Plantae and Animalia) did not distinguish "
               "between eukaryotes and prokaryotes, unicellular and multicellular organisms, or photosynthetic and "
               "non-photosynthetic organisms.",
               ["Statement I: false, nutrition was one of five criteria",
                "Statement II: true, a stated limitation of the two kingdom system"],
               ncert=ref("BC", "introduction (two kingdom and five kingdom classification)"), secs=35)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate",
           "group of protozoans", "example",
           ["Amoeboid protozoans", "Flagellated protozoans", "Ciliated protozoans", "Sporozoans"],
           ["Paramoecium", "Plasmodium", "Amoeba", "Trypanosoma"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "I", "B": "IV", "C": "III", "D": "II"},
            {"A": "III", "B": "II", "C": "I", "D": "IV"}], "B",
           "The four groups of protozoans",
           "Amoeboid protozoans (Amoeba) move by pseudopodia; flagellated protozoans include the parasite "
           "Trypanosoma that causes sleeping sickness; ciliated protozoans (Paramoecium) move by cilia; sporozoans "
           "include Plasmodium, the malarial parasite.",
           ["Amoeboid → Amoeba (III)", "Flagellated → Trypanosoma (IV)", "Ciliated → Paramoecium (I)",
            "Sporozoans → Plasmodium (II)"],
           why="The wrong codes swap Paramoecium with Trypanosoma, Amoeba with Paramoecium, or Plasmodium with "
               "Trypanosoma.",
           ncert=ref("BC", "Kingdom Protista (Protozoans)"), secs=40)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about bacteria are correct?",
                [("Cyanobacteria often form blooms in polluted water bodies.", True),
                 ("Chemosynthetic autotrophic bacteria oxidise inorganic substances such as nitrates, nitrites and "
                  "ammonia and use the released energy for ATP production.", True),
                 ("Bacteria never show any form of transfer of DNA from one bacterium to another.", False),
                 ("Heterotrophic bacteria are the most abundant in nature.", True),
                 ("Bacteria reproduce mainly by budding.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "b", "d", "e")], "C",
                "Kingdom Monera: eubacteria",
                "Cyanobacteria form blooms in polluted water. Chemosynthetic bacteria oxidise nitrates, nitrites and "
                "ammonia to make ATP. Heterotrophic bacteria are the most abundant in nature. Bacteria reproduce "
                "mainly by fission, and they also show a primitive type of DNA transfer from one bacterium to "
                "another.",
                ["(a) true", "(b) true", "(c) false: a primitive type of DNA transfer occurs", "(d) true",
                 "(e) false: mainly by fission"],
                why="Any option with (c) or (e) is wrong; (a), (b) and (c) also leaves out the true statement (d).",
                ncert=ref("BC", "Kingdom Monera (Eubacteria)"), secs=60)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Intermediate",
               "Albugo, the parasitic fungus on mustard, is a member of Phycomycetes.",
               "In ascomycetes and basidiomycetes, an intervening dikaryotic stage (n + n) may occur between "
               "plasmogamy and karyogamy.",
               True, True, "A",
               "Phycomycetes; the dikaryotic stage in fungi",
               "Phycomycetes include Mucor, Rhizopus and Albugo (the parasitic fungus on mustard). In ascomycetes and "
               "basidiomycetes, fusion of two haploid hyphae may not be followed at once by fusion of nuclei, giving "
               "a dikaryon (n + n) that later undergoes karyogamy.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("BC", "Kingdom Fungi (Phycomycetes; sexual cycle)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Euglenoids are photosynthetic in sunlight, but when deprived of sunlight they behave like "
                 "heterotrophs by predating on other smaller organisms.",
                 "Euglena has two flagella, a short one and a long one.",
                 True, True, False, "B",
                 "Euglenoids",
                 "Both statements are NCERT facts about euglenoids. A describes their switch in mode of nutrition; R "
                 "describes their flagella, a different feature. Having flagella does not explain why they become "
                 "heterotrophic in the dark.",
                 ["A: true", "R: true", "R is about locomotion, not nutrition → not the explanation"],
                 ncert=ref("BC", "Kingdom Protista (Euglenoids)"), secs=40)

direct(T_LIV, "Taxonomy and hierarchy", "Intermediate",
       "In the NCERT table of taxonomic categories, mango (Mangifera indica) and wheat (Triticum aestivum) are placed "
       "in the same:",
       "division Angiospermae", ["class Dicotyledonae", "order Poales", "family Anacardiaceae"], "D",
       "Comparing two hierarchies",
       "Mango: Anacardiaceae, Sapindales, Dicotyledonae, Angiospermae. Wheat: Poaceae, Poales, Monocotyledonae, "
       "Angiospermae. They first come together at the division level.",
       ["Family, order and class all differ", "Both are in division Angiospermae"],
       why="Wheat is a monocot (class Monocotyledonae); Poales is the order of wheat only; Anacardiaceae is the "
           "family of mango only.",
       ncert=ref("LW", "Taxonomic categories (Table: organisms with their taxonomic categories)"), secs=35)

statement_pair(T_LIV, "Lichens, viruses and viroids", "Intermediate",
               "Dmitri Ivanowsky found that the organisms causing tobacco mosaic disease were smaller than bacteria, "
               "because they passed through bacteria-proof filters.",
               "W.M. Stanley showed that viruses could be crystallised and that the crystals consist largely of "
               "lipids.",
               True, False, "C",
               "History of virus discovery",
               "Ivanowsky (1892) recognised the causal organisms of tobacco mosaic disease as smaller than bacteria "
               "since they passed through bacteria-proof filters. Stanley (1935) crystallised viruses; the crystals "
               "consist largely of proteins, not lipids.",
               ["Statement I: true", "Statement II: false, the crystals are largely proteins"],
               ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)

assertion_reason(T_LIV, "Five kingdom classification", "Intermediate",
                 "In the earlier two kingdom classification, fungi were placed in the same kingdom as green plants.",
                 "The character that unified the plant kingdom of that system was that all the organisms included "
                 "had a cell wall in their cells.",
                 True, True, True, "A",
                 "Why the two kingdom system grouped unlike organisms",
                 "Earlier systems put bacteria, blue-green algae, fungi, mosses, ferns, gymnosperms and angiosperms "
                 "under 'Plants' because all had a cell wall. That is exactly why heterotrophic fungi (chitin walls) "
                 "were grouped with autotrophic green plants (cellulose walls).",
                 ["A: true", "R: true, and the cell wall was the very basis of the grouping → R explains A"],
                 ncert=ref("BC", "introduction (limitations of the two kingdom system)"), secs=45)

match_list(T_LIV, "Monera, Protista and Fungi", "Advanced",
           "class of fungi", "feature",
           ["Phycomycetes", "Ascomycetes", "Basidiomycetes", "Deuteromycetes"],
           ["Sex organs absent; basidiospores produced exogenously on the basidium",
            "Many members are decomposers of litter and help in mineral cycling",
            "Aseptate, coenocytic mycelium; found in aquatic habitats and on decaying wood",
            "Ascospores produced endogenously in sac-like asci; mostly multicellular, rarely unicellular"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
            {"A": "II", "B": "IV", "C": "I", "D": "III"}], "B",
           "Classes of fungi",
           "Phycomycetes have aseptate, coenocytic mycelium and live in water or on decaying wood. Ascomycetes form "
           "ascospores inside asci and are mostly multicellular (yeast is unicellular). Basidiomycetes lack sex "
           "organs and bear four basidiospores outside the basidium. Many deuteromycetes are decomposers of litter "
           "that help in mineral cycling.",
           ["Phycomycetes → III", "Ascomycetes → IV", "Basidiomycetes → I", "Deuteromycetes → II"],
           why="The wrong codes swap the aseptate mycelium with the asci, the asci with the basidium, or the "
               "decomposers with the aquatic phycomycetes.",
           ncert=ref("BC", "Kingdom Fungi"), secs=60)

multi_statement(T_LIV, "Lichens, viruses and viroids", "Advanced",
                "Which of the following statements about lichens and viruses are correct?",
                [("In a lichen, the algal component prepares food for the fungus.", True),
                 ("In a lichen, the fungus provides shelter and absorbs mineral nutrients and water for its "
                  "partner.", True),
                 ("The capsid of a virus is made of small subunits called capsomeres and protects the nucleic "
                  "acid.", True),
                 ("Mumps, small pox, herpes and influenza are diseases caused by viruses.", True),
                 ("Viruses are cellular organisms that have a protein coat.", False)],
                [("a", "b", "c", "e"), ("a", "c", "d"), ("b", "c", "d", "e")], "C",
                "Lichens and viruses",
                "Lichens are mutually useful associations: the alga makes food for the fungus, and the fungus gives "
                "shelter and absorbs water and minerals. A virus has a capsid of capsomeres around its nucleic acid. "
                "Viruses cause mumps, small pox, herpes and influenza. Viruses are non-cellular, so (e) is false.",
                ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: viruses are non-cellular"],
                why="Every other option either includes the false statement (e) or leaves out a true one.",
                ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=60)

statement_pair(T_LIV, "Taxonomy and hierarchy", "Advanced",
               "Potato and brinjal belong to two different genera.",
               "Solanum, Petunia and Datura are placed in the family Solanaceae on the basis of vegetative "
               "characters alone.",
               False, False, "B",
               "Genus and family",
               "Potato and brinjal are two different species of the same genus, Solanum. Solanum, Petunia and Datura "
               "are placed in Solanaceae; a family is characterised on the basis of both vegetative and reproductive "
               "features, not vegetative characters alone.",
               ["Statement I: false, both are species of Solanum",
                "Statement II: false, families use both vegetative and reproductive features"],
               ncert=ref("LW", "Taxonomic categories (genus, family)"), secs=45)

direct(T_LIV, "Monera, Protista and Fungi", "Advanced",
       "How are the two flagella of most dinoflagellates arranged?",
       "One lies longitudinally and the other transversely in a furrow between the wall plates",
       ["Both arise from the anterior end and are of equal length",
        "One is short and the other long, both arising from a gullet",
        "Both lie transversely in the same furrow"], "D",
       "Dinoflagellates",
       "Dinoflagellates are mostly marine, photosynthetic protists with stiff cellulose plates on the outer surface "
       "of the wall. Most have two flagella: one lies longitudinally and the other transversely in a furrow between "
       "the wall plates.",
       ["Cell wall: stiff cellulose plates", "Flagella: one longitudinal, one transverse in a furrow"],
       why="Two unequal flagella (a short and a long one) describe Euglena, not dinoflagellates. The other two "
           "arrangements are not described for dinoflagellates.",
       ncert=ref("BC", "Kingdom Protista (Dinoflagellates)"), secs=40)

direct(T_LIV, "Five kingdom classification", "Advanced",
       "In Whittaker's five kingdom system, which kingdom has the following combination of features: eukaryotic "
       "cells, a cell wall present only in some members, unicellular body organisation, and both photosynthetic and "
       "heterotrophic modes of nutrition?",
       "Protista", ["Monera", "Fungi", "Plantae"], "A",
       "Comparing the five kingdoms",
       "Monera are prokaryotic. Fungi always have a cell wall (without cellulose) and are heterotrophic. Plantae have "
       "a cellulose wall, tissue/organ level body and are autotrophic. Only Protista are eukaryotic, unicellular, "
       "have a cell wall in some members, and show both photosynthetic and heterotrophic nutrition.",
       ["Eukaryotic → not Monera", "Wall in some only + some photosynthetic → not Fungi",
        "Unicellular + some heterotrophic → not Plantae", "→ Protista"],
       why="Monera are prokaryotic; Fungi have a cell wall in all members and are only heterotrophic; Plantae are "
           "multicellular autotrophs with a cellulose wall.",
       ncert=ref("BC", "Table: Characteristics of the five kingdoms"), secs=50)

# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "The stored food of members of Rhodophyceae (red algae) is:",
       "floridean starch", ["mannitol and laminarin", "starch", "glycogen"], "B",
       "Stored food in the classes of algae",
       "Chlorophyceae store starch, Phaeophyceae store mannitol and laminarin, and Rhodophyceae store floridean "
       "starch, which is very similar to amylopectin and glycogen in structure.",
       ["Chlorophyceae → starch", "Phaeophyceae → mannitol, laminarin", "Rhodophyceae → floridean starch"],
       why="Mannitol and laminarin are stored by brown algae; starch by green algae. Glycogen is not listed as the "
           "stored food of any algal class.",
       ncert=ref("PK", "Algae (Table: divisions of algae and their main characteristics)"), secs=25)

direct(T_PK, "Algae", "Basic",
       "Brown algae vary in colour from olive green to various shades of brown. The colour depends upon the amount "
       "of the pigment:",
       "fucoxanthin", ["phycoerythrin", "chlorophyll b", "phycocyanin"], "C",
       "Pigments of Phaeophyceae",
       "Brown algae contain chlorophyll a, c, carotenoids and xanthophylls. Their colour varies with the amount of "
       "the xanthophyll pigment fucoxanthin.",
       ["Colour of brown algae ∝ amount of fucoxanthin"],
       why="Phycoerythrin is the red pigment of red algae. Chlorophyll b is found in green algae, not brown algae. "
           "Phycocyanin is not the pigment NCERT names for brown algae.",
       ncert=ref("PK", "Algae (Phaeophyceae)"), secs=25)

direct(T_PK, "Bryophytes", "Basic",
       "Which of the following is a moss?",
       "Funaria", ["Marchantia", "Selaginella", "Salvinia"], "D",
       "Examples of bryophytes",
       "Common mosses are Funaria, Polytrichum and Sphagnum. Marchantia is a liverwort. Selaginella and Salvinia are "
       "pteridophytes.",
       ["Funaria → moss"],
       why="Marchantia is a liverwort; Selaginella and Salvinia are pteridophytes.",
       ncert=ref("PK", "Bryophytes (Mosses)"), secs=20)

direct(T_PK, "Gymnosperms", "Basic",
       "The giant redwood tree Sequoia, one of the tallest tree species, is a:",
       "gymnosperm", ["pteridophyte", "bryophyte", "monocotyledonous angiosperm"], "A",
       "Gymnosperms",
       "Gymnosperms include medium-sized trees, tall trees and shrubs. The giant redwood tree Sequoia, one of the "
       "tallest tree species, is a gymnosperm.",
       ["Sequoia → gymnosperm"],
       why="Sequoia bears naked seeds; it is not a fern ally, a moss or a monocot.",
       ncert=ref("PK", "Gymnosperms"), secs=20)

direct(T_PK, "Pteridophytes", "Basic",
       "In pteridophytes, small leaves such as those of Selaginella are called:",
       "microphylls", ["macrophylls", "sporophylls", "stipules"], "B",
       "Leaves of pteridophytes",
       "The leaves of pteridophytes are small (microphylls) as in Selaginella, or large (macrophylls) as in ferns.",
       ["Small leaves → microphylls (Selaginella)", "Large leaves → macrophylls (ferns)"],
       why="Macrophylls are the large leaves of ferns. Sporophylls are leaves that bear sporangia, a function and "
           "not a size class. Stipules are leaf-like outgrowths of the leaf base in flowering plants.",
       ncert=ref("PK", "Pteridophytes"), secs=20)

match_list(T_PK, "Pteridophytes", "Intermediate",
           "plant", "group",
           ["Dictyota", "Marchantia", "Salvinia", "Ginkgo"],
           ["Gymnosperm", "Heterosporous pteridophyte", "Brown alga", "Liverwort"],
           {"A": "III", "B": "IV", "C": "II", "D": "I"},
           [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
            {"A": "III", "B": "II", "C": "IV", "D": "I"}], "C",
           "Examples across the plant kingdom",
           "Dictyota is a brown alga (Phaeophyceae). Marchantia is a liverwort. Salvinia, like Selaginella, is a "
           "heterosporous pteridophyte. Ginkgo, like Cycas and Pinus, is a gymnosperm.",
           ["Dictyota → brown alga (III)", "Marchantia → liverwort (IV)", "Salvinia → heterosporous pteridophyte (II)",
            "Ginkgo → gymnosperm (I)"],
           why="The wrong codes treat Dictyota as a liverwort, Salvinia as a gymnosperm, or Marchantia as a "
               "pteridophyte.",
           ncert=ref("PK", "Algae; Bryophytes; Pteridophytes; Gymnosperms (examples)"), secs=40)

multi_statement(T_PK, "Algae", "Intermediate",
                "Which of the following statements about algae are correct?",
                [("Vegetative reproduction in algae takes place by fragmentation.", True),
                 ("The zoospores formed during asexual reproduction in algae are non-motile.", False),
                 ("At least half of the total carbon dioxide fixation on earth is carried out by algae through "
                  "photosynthesis.", True),
                 ("Many species of Porphyra, Laminaria and Sargassum are used as food.", True),
                 ("All algae are multicellular.", False)],
                [("a", "b", "c"), ("c", "d", "e"), ("a", "c", "d", "e")], "D",
                "Reproduction and uses of algae",
                "Algae reproduce vegetatively by fragmentation and asexually by spores, most commonly zoospores, "
                "which are flagellated (motile). Algae carry out at least half of all CO₂ fixation on earth. "
                "Porphyra, Laminaria and Sargassum are among the marine algae used as food. Algae may be "
                "unicellular (Chlamydomonas), colonial or filamentous.",
                ["(a) true", "(b) false: zoospores are flagellated", "(c) true", "(d) true",
                 "(e) false: Chlamydomonas is unicellular"],
                why="Options with (b) or (e) contain a false statement.",
                ncert=ref("PK", "Algae"), secs=55)

statement_pair(T_PK, "Bryophytes", "Intermediate",
               "The rhizoids of bryophytes are always unicellular.",
               "In bryophytes, the zygote undergoes reduction division immediately to form haploid spores.",
               False, False, "B",
               "Rhizoids and the zygote of bryophytes",
               "Bryophytes are attached to the substratum by unicellular or multicellular rhizoids. Their zygotes do "
               "not undergo reduction division immediately; they produce a multicellular sporophyte, some cells of "
               "which later undergo meiosis to form spores.",
               ["Statement I: false, rhizoids may be unicellular or multicellular",
                "Statement II: false, the zygote first forms a multicellular sporophyte"],
               ncert=ref("PK", "Bryophytes"), secs=40)

assertion_reason(T_PK, "Pteridophytes", "Intermediate",
                 "In the majority of pteridophytes, all the spores are of similar kinds.",
                 "Pteridophyte spores germinate to give rise to small, multicellular, free-living, mostly "
                 "photosynthetic thalloid gametophytes called prothallus.",
                 True, True, False, "B",
                 "Homospory and the prothallus",
                 "Most pteridophytes are homosporous: their spores are of one kind. R correctly describes what the "
                 "spores grow into, the prothallus. But the nature of the gametophyte does not explain why the spores "
                 "are all alike; the two statements describe different features.",
                 ["A: true (homosporous majority)", "R: true (prothallus)", "R does not explain A"],
                 ncert=ref("PK", "Pteridophytes"), secs=45)

direct(T_PK, "Gymnosperms", "Intermediate",
       "In gymnosperms, the megaspore mother cell is differentiated from one of the cells of the:",
       "nucellus", ["integument", "microsporangium", "pollen grain"], "B",
       "Ovule of gymnosperms",
       "Each megasporophyll bears ovules. The megaspore mother cell is differentiated from one of the cells of the "
       "nucellus. The nucellus, protected by envelopes, forms the ovule.",
       ["Ovule = nucellus + protective envelopes", "Megaspore mother cell ← a nucellus cell"],
       why="The integument is the protective envelope, not the source of the mother cell. The microsporangium and "
           "pollen grain belong to the male side.",
       ncert=ref("PK", "Gymnosperms"), secs=35)

statement_pair(T_PK, "Gymnosperms", "Intermediate",
               "Gymnosperms are heterosporous; they produce haploid microspores and megaspores.",
               "In gymnosperms, the male gametophyte is highly reduced and is confined to only a limited number of "
               "cells.",
               True, True, "A",
               "Spores and male gametophyte of gymnosperms",
               "Gymnosperms produce two kinds of haploid spores, microspores and megaspores, in sporangia on "
               "sporophylls. Microspores develop into a highly reduced male gametophyte of a few cells, the pollen "
               "grain.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Gymnosperms"), secs=35)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Red algae occur in well-lighted regions close to the surface of water and also at great depths in "
                 "oceans where relatively little light penetrates.",
                 "The majority of red algae are fresh-water forms.",
                 True, False, False, "C",
                 "Habitat of Rhodophyceae",
                 "Red algae are found both near the surface and at great depths where little light reaches. The "
                 "majority of red algae are marine, with greater concentrations in the warmer areas, so R is false.",
                 ["A: true", "R: false, the majority are marine"],
                 ncert=ref("PK", "Algae (Rhodophyceae)"), secs=40)

multi_statement(T_PK, "Pteridophytes", "Advanced",
                "Which of the following statements about pteridophytes are correct?",
                [("The sporangia are borne on leaf-like appendages called sporophylls.", True),
                 ("The gametophyte bears the male and female sex organs, antheridia and archegonia.", True),
                 ("Water is required for the transfer of antherozoids to the mouth of the archegonium.", True),
                 ("The spores are produced by mitosis in the sporangia.", False),
                 ("Pteridophytes are used as soil-binders and ornamentals, but never for medicinal purposes.",
                  False)],
                [("a", "b", "d"), ("a", "c", "d", "e"), ("b", "c", "e")], "C",
                "Reproduction and uses of pteridophytes",
                "Sporangia are borne on sporophylls, and spore mother cells in them undergo meiosis to form spores. "
                "The gametophyte bears antheridia and archegonia, and water carries the antherozoids to the "
                "archegonium. Pteridophytes are used for medicinal purposes, as soil-binders and as ornamentals.",
                ["(a) true", "(b) true", "(c) true", "(d) false: spores form by meiosis",
                 "(e) false: they are used medicinally too"],
                why="Options with (d) or (e) contain a false statement.",
                ncert=ref("PK", "Pteridophytes"), secs=60)

multi_statement(T_PK, "Bryophytes", "Advanced",
                "Which of the following statements about mosses and liverworts are correct?",
                [("The sporophyte of a moss is differentiated into foot, seta and capsule.", True),
                 ("The sporophyte of a liverwort is free-living and independent of the gametophyte.", False),
                 ("The leafy stage of a moss develops directly from the germinating spore.", False),
                 ("Vegetative reproduction in mosses is by fragmentation and budding in the secondary protonema.",
                  True),
                 ("In mosses, the antheridia and archegonia are produced at the apex of the leafy shoots.", True)],
                [("a", "b", "e"), ("a", "c", "d"), ("c", "d", "e")], "D",
                "Life of mosses and liverworts",
                "The moss sporophyte has foot, seta and capsule. Bryophyte sporophytes are not free-living; they are "
                "attached to the gametophyte. A moss spore first forms the protonema; the leafy stage develops from "
                "the secondary protonema as a lateral bud. Mosses reproduce vegetatively by fragmentation and "
                "budding in the secondary protonema, and bear sex organs at the apex of leafy shoots.",
                ["(a) true", "(b) false: the sporophyte depends on the gametophyte",
                 "(c) false: spore → protonema → leafy stage", "(d) true", "(e) true"],
                why="Options with (b) or (c) contain a false statement.",
                ncert=ref("PK", "Bryophytes (Liverworts; Mosses)"), secs=60)

match_list(T_PK, "Algae", "Advanced",
           "structure", "group in which it is found",
           ["Protonema", "Prothallus", "Holdfast, stipe and frond", "Pyrenoids containing protein besides starch"],
           ["Pteridophytes", "Green algae", "Mosses", "Brown algae"],
           {"A": "III", "B": "I", "C": "IV", "D": "II"},
           [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
            {"A": "IV", "B": "I", "C": "III", "D": "II"}], "A",
           "Characteristic structures of plant groups",
           "The protonema is the first, creeping stage of the moss gametophyte. The prothallus is the small thalloid "
           "gametophyte of pteridophytes. The body of brown algae is differentiated into holdfast, stipe and frond. "
           "Green algae have pyrenoids in their chloroplasts, which contain protein besides starch.",
           ["Protonema → mosses (III)", "Prothallus → pteridophytes (I)", "Holdfast, stipe, frond → brown algae (IV)",
            "Pyrenoids → green algae (II)"],
           why="The wrong codes swap the two gametophyte stages, or the brown and green algal features.",
           ncert=ref("PK", "Algae; Bryophytes; Pteridophytes"), secs=50)

# moss: gametophyte (leaf cell) is haploid, the sporophyte (seta) diploid, spores formed by meiosis are haploid
n_leaf = 12
seta, spore = 2 * n_leaf, (2 * n_leaf) // 2
assert (seta, spore) == (24, 12)
numerical(T_PK, "Bryophytes", "Advanced",
          "The cells of the leafy stage of a moss plant have 12 chromosomes each. How many chromosomes will be "
          "present in a cell of the seta and in a spore of this moss, respectively?",
          "24 and 12", ["12 and 6", "12 and 12", "24 and 24"], "B", (seta, spore) == (24, 12),
          "Ploidy of the moss gametophyte, sporophyte and spores",
          "The leafy plant is the gametophyte, which is haploid (n = 12). The zygote formed by fertilisation grows "
          "into the sporophyte (foot, seta, capsule), which is diploid (2n = 24). Some sporophyte cells undergo "
          "meiosis to form haploid spores (n = 12).",
          ["Leafy stage = gametophyte: n = 12", "Seta is part of the sporophyte: 2n = 24",
           "Spores form by meiosis: n = 12"],
          "12 and 6 takes the leafy stage as diploid. 12 and 12 forgets that the sporophyte is diploid. 24 and 24 "
          "forgets that spores form by meiosis.",
          ref("PK", "Bryophytes"), secs=50)

direct(T_PK, "Gymnosperms", "Advanced",
       "Which statement about the bearing of cones in gymnosperms is correct?",
       "In Pinus, male and female cones are borne on the same tree, whereas in Cycas male cones and megasporophylls "
       "are borne on different trees",
       ["In Pinus, male and female cones are borne on different trees, whereas in Cycas they are on the same tree",
        "In both Pinus and Cycas, male and female structures are borne on the same tree",
        "In both Pinus and Cycas, male and female structures are borne on different trees"], "C",
       "Distribution of male and female strobili",
       "The male or female cones (strobili) may be borne on the same tree, as in Pinus. In Cycas, however, male "
       "cones and megasporophylls are borne on different trees.",
       ["Pinus → both kinds of cones on one tree", "Cycas → male cones and megasporophylls on separate trees"],
       why="The other options reverse the condition or treat both genera alike.",
       ncert=ref("PK", "Gymnosperms"), secs=40)

# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Root, stem and leaf", "Basic",
       "In which of the following plants do swollen adventitious roots store food?",
       "Sweet potato", ["Carrot", "Turnip", "Potato"], "D",
       "Roots modified for storage",
       "Tap roots of carrot and turnip and adventitious roots of sweet potato get swollen and store food. Potato is "
       "an underground stem, not a root.",
       ["Carrot, turnip → swollen tap roots", "Sweet potato → swollen adventitious roots", "Potato → stem"],
       why="Carrot and turnip store food in tap roots; potato stores food in an underground stem.",
       ncert=ref("MOR", "The Root (Modifications of root)"), secs=25)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "When the veinlets in the lamina of a leaf form a network, the venation is termed:",
       "reticulate", ["parallel", "pinnate compound", "whorled"], "A",
       "Venation",
       "The arrangement of veins and veinlets in the lamina is venation. When the veinlets form a network, it is "
       "reticulate (typical of dicots); when veins run parallel within the lamina, it is parallel (most monocots).",
       ["Network of veinlets → reticulate venation"],
       why="Parallel venation has no network. Pinnately compound describes a leaf with leaflets, and whorled "
           "describes phyllotaxy, not venation.",
       ncert=ref("MOR", "The Leaf (Venation)"), secs=20)

direct(T_MOR, "Flower", "Basic",
       "When the sepals or petals in a whorl just touch one another at the margins without overlapping, as in "
       "Calotropis, the aestivation is:",
       "valvate", ["twisted", "imbricate", "vexillary"], "B",
       "Aestivation",
       "In valvate aestivation, sepals or petals of a whorl just touch one another at the margin without "
       "overlapping, as in Calotropis.",
       ["Margins touch, no overlap → valvate (Calotropis)"],
       why="Twisted and imbricate aestivation involve overlapping margins; vexillary is the pea-type arrangement of "
           "petals.",
       ncert=ref("MOR", "The Flower (Aestivation)"), secs=20)

direct(T_MOR, "Fruit and seed", "Basic",
       "Coconut, like mango, is a drupe. In coconut, the mesocarp is:",
       "fibrous", ["fleshy and edible", "hard and stony", "thin and papery"], "C",
       "The drupe",
       "Mango and coconut fruits are drupes developing from monocarpellary superior ovaries and are one-seeded. In "
       "coconut, the mesocarp is fibrous.",
       ["Coconut drupe → fibrous mesocarp"],
       why="A fleshy edible mesocarp is the mango condition; the hard stony layer is the endocarp; a thin papery "
           "mesocarp is not the coconut condition.",
       ncert=ref("MOR", "The Fruit"), secs=25)

direct(T_MOR, "Plant families", "Basic",
       "Which of the following ornamental plants belongs to the family Liliaceae?",
       "Gloriosa", ["Petunia", "Lupin", "Sweet pea"], "D",
       "Economic importance of Liliaceae",
       "Many members of Liliaceae are good ornamentals (tulip, Gloriosa), sources of medicine (Aloe), vegetables "
       "(Asparagus) and colchicine (Colchicum autumnale).",
       ["Gloriosa → Liliaceae"],
       why="Petunia is an ornamental of Solanaceae; lupin and sweet pea are ornamentals of Fabaceae.",
       ncert=ref("MOR", "Description of Some Important Families (Liliaceae)"), secs=25)

match_list(T_MOR, "Root, stem and leaf", "Intermediate",
           "plant", "modified organ",
           ["Euphorbia", "Chrysanthemum", "Ginger", "Turnip"],
           ["Swollen tap root that stores food",
            "Fleshy, cylindrical green stem of an arid-region plant that photosynthesises",
            "Underground stem that stores food and acts as an organ of perennation",
            "Lateral branches from the underground base of the stem that grow horizontally beneath the soil and "
            "then come up obliquely as leafy shoots"],
           {"A": "II", "B": "IV", "C": "III", "D": "I"},
           [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
            {"A": "II", "B": "IV", "C": "I", "D": "III"}], "B",
           "Modifications of stem and root",
           "Some plants of arid regions have fleshy cylindrical stems that photosynthesise (Euphorbia). In "
           "Chrysanthemum, banana and pineapple, lateral branches from the underground base grow beneath the soil "
           "and then come out obliquely. Ginger is an underground stem storing food and acting as a perennating "
           "organ. Turnip is a swollen tap root.",
           ["Euphorbia → II", "Chrysanthemum → IV", "Ginger → III", "Turnip → I (a root, not a stem)"],
           why="The commonest error is to swap ginger (an underground stem) with turnip (a tap root); the other "
               "wrong codes swap the two stem modifications.",
           ncert=ref("MOR", "The Root (Modifications); The Stem (Modifications of stem)"), secs=50)

direct(T_MOR, "Root, stem and leaf", "Intermediate",
       "In monocotyledons, the leaf base:",
       "expands into a sheath covering the stem partially or wholly",
       ["becomes swollen to form a pulvinus", "is modified into a tendril",
        "is modified into a spine"], "C",
       "Leaf base",
       "The leaf is attached to the stem by the leaf base, which may bear two lateral small leaf-like stipules. In "
       "monocotyledons, the leaf base expands into a sheath covering the stem partially or wholly. In some "
       "leguminous plants, the leaf base becomes swollen and is called the pulvinus.",
       ["Monocots → sheathing leaf base", "Some legumes → pulvinus"],
       why="The pulvinus is found in some leguminous plants. Tendrils and spines are leaf modifications of other "
           "plants (pea, cacti), not the monocot leaf-base feature.",
       ncert=ref("MOR", "The Leaf"), secs=30)

statement_pair(T_MOR, "Flower", "Intermediate",
               "A flower is a modified shoot in which the shoot apical meristem changes to a floral meristem.",
               "In a flower, the internodes elongate and the axis gets lengthened.",
               True, False, "C",
               "The flower as a modified shoot",
               "The flower is a modified shoot wherein the shoot apical meristem changes to a floral meristem. "
               "Internodes do not elongate and the axis gets condensed; the apex produces different floral "
               "appendages laterally at successive nodes instead of leaves.",
               ["Statement I: true", "Statement II: false, internodes do not elongate; the axis is condensed"],
               ncert=ref("MOR", "Inflorescence"), secs=35)

assertion_reason(T_MOR, "Fruit and seed", "Intermediate",
                 "The embryo of a maize grain has one large, shield-shaped cotyledon called the scutellum.",
                 "In the maize embryo, the plumule and radicle are enclosed in sheaths called the coleoptile and "
                 "coleorhiza, respectively.",
                 True, True, False, "B",
                 "Structure of a monocotyledonous seed",
                 "Both are NCERT facts about the maize embryo. A names the single cotyledon; R describes the sheaths "
                 "around the plumule and radicle. The sheaths have nothing to do with why the cotyledon is called the "
                 "scutellum, so R does not explain A.",
                 ["A: true", "R: true", "R describes another part of the embryo → not the explanation"],
                 ncert=ref("MOR", "The Seed (Structure of a monocotyledonous seed)"), secs=40)

direct(T_MOR, "Root, stem and leaf", "Intermediate",
       "In a pinnately compound leaf, the leaflets are present on a common axis, the rachis. The rachis represents "
       "the:",
       "midrib of the leaf", ["petiole of the leaf", "axillary bud", "stem"], "D",
       "Pinnately compound leaf",
       "In a pinnately compound leaf, a number of leaflets are present on a common axis, the rachis, which "
       "represents the midrib of the leaf, as in neem.",
       ["Rachis = midrib of a pinnately compound leaf"],
       why="The petiole is below the rachis and attaches it to the stem; a whole compound leaf (not its rachis) has "
           "a bud in its axil; the rachis is part of the leaf, not the stem.",
       ncert=ref("MOR", "The Leaf (Types of leaves)"), secs=30)

direct(T_MOR, "Flower", "Intermediate",
       "In which group are all three flowers hypogynous?",
       "Mustard, china rose and brinjal",
       ["Mustard, guava and plum", "Plum, rose and peach", "Guava, cucumber and ray florets of sunflower"], "A",
       "Position of floral parts on the thalamus",
       "In hypogynous flowers the gynoecium occupies the highest position and the ovary is superior: mustard, china "
       "rose and brinjal. Plum, rose and peach are perigynous; guava, cucumber and ray florets of sunflower are "
       "epigynous.",
       ["Hypogynous: mustard, china rose, brinjal", "Perigynous: plum, rose, peach",
        "Epigynous: guava, cucumber, ray florets of sunflower"],
       why="Each wrong option contains perigynous or epigynous flowers.",
       ncert=ref("MOR", "The Flower (position of floral parts on the thalamus)"), secs=35)

match_list(T_MOR, "Fruit and seed", "Intermediate",
           "part of a dicotyledonous seed", "description",
           ["Hilum", "Micropyle", "Testa", "Tegmen"],
           ["Inner layer of the seed coat", "Small pore above the hilum",
            "Scar through which the developing seed was attached to the fruit", "Outer layer of the seed coat"],
           {"A": "III", "B": "II", "C": "IV", "D": "I"},
           [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
            {"A": "II", "B": "III", "C": "I", "D": "IV"}], "B",
           "Structure of a dicotyledonous seed",
           "The seed coat has an outer testa and an inner tegmen. The hilum is a scar on the seed coat through which "
           "the developing seed was attached to the fruit. Above the hilum is a small pore, the micropyle.",
           ["Hilum → III", "Micropyle → II", "Testa → IV", "Tegmen → I"],
           why="The wrong codes swap hilum with micropyle, testa with tegmen, or both.",
           ncert=ref("MOR", "The Seed (Structure of a dicotyledonous seed)"), secs=35)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements about the family Fabaceae are correct?",
                [("The leaves are pinnately compound or simple, with a pulvinate leaf base, and are stipulate.",
                  True),
                 ("The inflorescence is cymose.", False),
                 ("The ovary is superior, monocarpellary and unilocular, with many ovules.", True),
                 ("The corolla is papilionaceous, with a posterior standard, two lateral wings and two anterior "
                  "petals forming a keel.", True),
                 ("The fruit is a berry.", False)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("c", "d", "e")], "C",
                "Family Fabaceae",
                "Fabaceae: leaves pinnately compound or simple, leaf base pulvinate, stipulate; inflorescence "
                "racemose; corolla papilionaceous (standard, wings, keel) with vexillary aestivation; ovary superior, "
                "monocarpellary, unilocular with many ovules; fruit a legume; seeds non-endospermic.",
                ["(a) true", "(b) false: racemose", "(c) true", "(d) true", "(e) false: the fruit is a legume"],
                why="Options with (b) or (e) contain a false statement.",
                ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=60)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements about the family Liliaceae are correct?",
                [("Its members are mostly perennial herbs with underground bulbs, corms or rhizomes.", True),
                 ("The leaves are mostly basal, alternate, linear and exstipulate, with parallel venation.", True),
                 ("The ovary is inferior and unilocular.", False),
                 ("The fruit is a capsule, rarely a berry.", True),
                 ("The seeds are non-endospermous.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "b", "d", "e")], "D",
                "Family Liliaceae",
                "Liliaceae (a monocot family): perennial herbs with bulbs, corms or rhizomes; leaves mostly basal, "
                "alternate, linear, exstipulate with parallel venation; gynoecium tricarpellary, syncarpous, ovary "
                "superior and trilocular with axile placentation; fruit a capsule, rarely a berry; seeds "
                "endospermous.",
                ["(a) true", "(b) true", "(c) false: superior and trilocular", "(d) true",
                 "(e) false: seeds are endospermous"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("MOR", "Description of Some Important Families (Liliaceae)"), secs=60)

statement_pair(T_MOR, "Plant families", "Advanced",
               "In Solanaceae, the calyx falls off soon after the flower opens; it is not persistent.",
               "In Solanaceae, the leaves are exstipulate and show reticulate venation.",
               False, True, "D",
               "Family Solanaceae",
               "In Solanaceae, the calyx has five united sepals, is persistent and shows valvate aestivation. The "
               "leaves are alternate, simple (rarely pinnately compound), exstipulate, with reticulate venation.",
               ["Statement I: false, the calyx is persistent", "Statement II: true"],
               ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=40)

multi_statement(T_MOR, "Root, stem and leaf", "Advanced",
                "Which of the following statements about roots are correct?",
                [("In most dicotyledonous plants, such as mustard, the primary root and its branches form the tap "
                  "root system.", True),
                 ("In monocotyledonous plants, such as wheat, the primary root is short-lived and is replaced by a "
                  "large number of roots arising from the base of the stem.", True),
                 ("Root hairs arise from the region of meristematic activity.", False),
                 ("The root cap protects the tender apex of the root as it makes its way through the soil.", True),
                 ("The cells of the region of meristematic activity are large, with thick walls and sparse "
                  "cytoplasm.", False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "d")], "A",
                "Root systems and regions of the root",
                "Dicots such as mustard have a tap root system; monocots such as wheat have a fibrous root system. "
                "The root cap protects the tender apex. The cells of the region of meristematic activity are very "
                "small, thin-walled, with dense protoplasm. Root hairs arise from epidermal cells of the region of "
                "maturation.",
                ["(a) true", "(b) true", "(c) false: root hairs arise in the region of maturation", "(d) true",
                 "(e) false: the meristematic cells are small, thin-walled, with dense protoplasm"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("MOR", "The Root (Regions of the root)"), secs=60)

match_list(T_MOR, "Root, stem and leaf", "Advanced",
           "plant", "modification",
           ["Pea", "Cactus", "Australian acacia", "Bougainvillea"],
           ["Small, short-lived leaves; the petioles expand, become green and synthesise food",
            "Axillary buds modified into woody, straight, pointed structures",
            "Leaves modified into spines for defence",
            "Leaves modified into tendrils for climbing"],
           {"A": "IV", "B": "III", "C": "I", "D": "II"},
           [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
            {"A": "IV", "B": "III", "C": "II", "D": "I"}], "B",
           "Leaf and stem modifications compared",
           "In pea, leaves are modified into tendrils for climbing; in cacti, into spines for defence. In Australian "
           "acacia, leaves are small and short-lived and the petioles expand, turn green and make food. The thorns of "
           "Bougainvillea are axillary buds of the stem modified into woody, straight, pointed structures, so they "
           "are stem modifications, unlike the leaf spines of cacti.",
           ["Pea → IV", "Cactus → III", "Australian acacia → I", "Bougainvillea → II (stem thorn)"],
           why="The main trap is to treat the Bougainvillea thorn and the cactus spine as the same; one comes from an "
               "axillary bud (stem), the other from a leaf.",
           ncert=ref("MOR", "The Stem (Modifications); The Leaf (Modifications of leaves)"), secs=50)

# =============================================================== 4. Anatomy of Flowering Plants (4/6/4)
direct(T_ANA, "Plant tissues", "Basic",
       "Sclerenchyma fibres are:",
       "thick-walled, elongated and pointed cells, generally occurring in groups",
       ["thin-walled, isodiametric living cells with large intercellular spaces",
        "living cells thickened at the corners with cellulose, hemicellulose and pectin",
        "spherical or oval cells with highly thickened walls and very narrow lumen, found in fruit walls of nuts"],
       "C",
       "Sclerenchyma",
       "Sclerenchyma consists of long, narrow cells with thick, lignified walls having a few or numerous pits; it "
       "is usually dead. Fibres are thick-walled, elongated and pointed cells, generally occurring in groups. "
       "Sclereids are spherical, oval or cylindrical, highly thickened dead cells with very narrow cavities.",
       ["Fibres: elongated, pointed, thick-walled, in groups"],
       why="The first wrong option describes parenchyma, the second collenchyma and the third sclereids.",
       ncert=ref("ANA", "The Tissues (Simple tissues: sclerenchyma)"), secs=30)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "In a dorsiventral (dicotyledonous) leaf, the stomata are generally:",
       "more numerous on the abaxial (lower) epidermis than on the adaxial (upper) epidermis",
       ["more numerous on the adaxial epidermis than on the abaxial epidermis",
        "equal in number on both surfaces",
        "present only in the mesophyll, below the epidermis"], "D",
       "Dorsiventral leaf",
       "In a dorsiventral leaf, the abaxial epidermis generally bears more stomata than the adaxial epidermis; the "
       "adaxial epidermis may even lack stomata. An isobilateral (monocot) leaf has stomata on both surfaces.",
       ["Dicot leaf: abaxial (lower) epidermis > adaxial (upper) for stomata"],
       why="More stomata on the upper surface is the reverse of the NCERT statement; stomata on both surfaces is the "
           "isobilateral condition; stomata are pores in the epidermis, not in the mesophyll.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dorsiventral leaf)"), secs=30)

direct(T_ANA, "Plant tissues", "Basic",
       "The radial conduction of water in the xylem takes place through the:",
       "ray parenchymatous cells", ["vessels", "tracheids", "xylem fibres"], "B",
       "Xylem parenchyma",
       "Xylem parenchyma cells are living and thin-walled; they store food (starch or fat) and substances like "
       "tannins. The radial conduction of water takes place by the ray parenchymatous cells.",
       ["Radial conduction of water → ray parenchyma"],
       why="Vessels and tracheids conduct water mainly along the length of the organ; xylem fibres are supportive.",
       ncert=ref("ANA", "The Tissues (Complex tissues: xylem)"), secs=25)

statement_pair(T_ANA, "Plant tissues", "Basic",
               "Phloem fibres are generally present in the primary phloem but absent in the secondary phloem.",
               "Phloem parenchyma is made of dead cells with lignified walls.",
               False, False, "B",
               "Phloem fibres and phloem parenchyma",
               "Phloem fibres (bast fibres) are generally absent in the primary phloem and are found in the "
               "secondary phloem. Phloem parenchyma is made of elongated, tapering, living cells with dense "
               "cytoplasm and a nucleus; the walls are of cellulose and have pits with plasmodesmata.",
               ["Statement I: false, reversed", "Statement II: false, phloem parenchyma is living with cellulose walls"],
               ncert=ref("ANA", "The Tissues (Complex tissues: phloem)"), secs=35)

match_list(T_ANA, "Tissue systems", "Intermediate",
           "part of the epidermal tissue system", "feature",
           ["Epidermis", "Cuticle", "Root hairs", "Trichomes"],
           ["Usually multicellular, branched or unbranched, and may be secretory",
            "Usually a single layer of elongated, compactly arranged cells",
            "Unicellular elongations of epidermal cells that absorb water and minerals",
            "Waxy thick layer that prevents loss of water and is absent in roots"],
           {"A": "II", "B": "IV", "C": "III", "D": "I"},
           [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
            {"A": "II", "B": "III", "C": "IV", "D": "I"}], "C",
           "Epidermal tissue system",
           "The epidermis is usually single-layered, of elongated, compactly arranged cells. Outside it lies the "
           "waxy cuticle, which prevents water loss and is absent in roots. Root hairs are unicellular elongations "
           "of epidermal cells; trichomes on the shoot are usually multicellular, branched or unbranched, soft or "
           "stiff, and may be secretory.",
           ["Epidermis → II", "Cuticle → IV", "Root hairs → III", "Trichomes → I"],
           why="The wrong codes swap epidermis with cuticle, root hairs with trichomes, or cuticle with root hairs.",
           ncert=ref("ANA", "The Tissue System (Epidermal tissue system)"), secs=45)

multi_statement(T_ANA, "Plant tissues", "Intermediate",
                "Which of the following statements about meristems are correct?",
                [("Apical meristems occur at the tips of roots and shoots and produce primary tissues.", True),
                 ("Intercalary meristems are secondary meristems because they occur between mature tissues.",
                  False),
                 ("Some cells 'left behind' from the shoot apical meristem during leaf formation constitute the "
                  "axillary bud.", True),
                 ("Fascicular vascular cambium, interfascicular cambium and cork cambium are examples of lateral "
                  "meristems.", True),
                 ("Lateral meristems are responsible for producing the primary tissues.", False)],
                [("a", "b", "c"), ("a", "d", "e"), ("b", "c", "d", "e")], "D",
                "Meristematic tissues",
                "Apical meristems at root and shoot tips produce primary tissues. Intercalary meristems also appear "
                "early in life and form the primary plant body, so they are primary meristems. Cells left behind by "
                "the shoot apical meristem form axillary buds. Lateral (secondary) meristems, such as the vascular "
                "cambia and cork cambium, are cylindrical and produce secondary tissues.",
                ["(a) true", "(b) false: intercalary meristems are primary meristems", "(c) true", "(d) true",
                 "(e) false: lateral meristems produce secondary tissues"],
                why="Options with (b) or (e) contain a false statement.",
                ncert=ref("ANA", "The Tissues (Meristematic tissues)"), secs=60)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "The cell walls of parenchyma are thick and lignified.",
                 "Parenchyma performs various functions such as photosynthesis, storage and secretion.",
                 False, True, False, "D",
                 "Parenchyma",
                 "Parenchyma cells are generally isodiametric; their walls are thin and made of cellulose, so A is "
                 "false. Parenchyma performs functions like photosynthesis, storage and secretion, so R is true.",
                 ["A: false, walls are thin and cellulosic", "R: true"],
                 ncert=ref("ANA", "The Tissues (Simple tissues: parenchyma)"), secs=35)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "In a dicot root, the initiation of lateral roots takes place in the pericycle.",
               "In a dicot root, the parenchymatous cells that lie between the xylem and the phloem are called "
               "conjunctive tissue.",
               True, True, "A",
               "Pericycle and conjunctive tissue of the dicot root",
               "Next to the endodermis lies the pericycle, a few layers of thick-walled parenchymatous cells. "
               "Initiation of lateral roots (and of the vascular cambium during secondary growth) takes place in "
               "these cells. The parenchymatous cells between the xylem and phloem are called conjunctive tissue.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous root)"),
               secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "In a dicot stem, the hypodermis consists of a few layers of:",
       "collenchymatous cells", ["sclerenchymatous cells", "chlorenchymatous spongy cells",
                                 "starch-filled endodermal cells"], "A",
       "Cortex of the dicot stem",
       "The cortex of a dicot stem has three sub-zones. The outer hypodermis consists of a few layers of "
       "collenchymatous cells just below the epidermis, which provide mechanical strength to the young stem. "
       "(The monocot stem has a sclerenchymatous hypodermis.)",
       ["Dicot stem: hypodermis = collenchyma", "Monocot stem: hypodermis = sclerenchyma"],
       why="A sclerenchymatous hypodermis is the monocot condition. Spongy cells belong to leaf mesophyll, and the "
           "starch-rich layer is the endodermis (starch sheath), the innermost layer of the cortex.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous stem)"), secs=30)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "In a dorsiventral leaf, the palisade parenchyma is placed adaxially and is made of elongated cells "
               "arranged vertically and parallel to each other.",
               "In a dorsiventral leaf, the spongy parenchyma lies above the palisade parenchyma, towards the "
               "adaxial side.",
               True, False, "C",
               "Mesophyll of a dorsiventral leaf",
               "The mesophyll of a dorsiventral leaf has adaxially placed palisade parenchyma of elongated, "
               "vertically arranged cells. The oval or round, loosely arranged spongy parenchyma lies below the "
               "palisade cells and extends to the lower epidermis.",
               ["Statement I: true", "Statement II: false, spongy parenchyma lies below the palisade"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dorsiventral leaf)"),
               secs=35)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "Which of the following statements about the internal structure of a dicot root are correct?",
                [("The endodermis is a single layer of barrel-shaped cells without any intercellular spaces.",
                  True),
                 ("The pith is large and well developed.", False),
                 ("Many cells of the epiblema protrude as unicellular root hairs.", True),
                 ("The cortex has several layers of thin-walled parenchyma cells with intercellular spaces.", True),
                 ("The pericycle is made of a few layers of thick-walled sclerenchyma cells.", False)],
                [("a", "b", "c", "d"), ("a", "c", "d", "e"), ("c", "d", "e")], "B",
                "Dicotyledonous root",
                "Epiblema with unicellular root hairs; cortex of thin-walled parenchyma with intercellular spaces; "
                "endodermis a single layer of barrel-shaped cells without intercellular spaces; pericycle a few "
                "layers of thick-walled parenchymatous cells; the pith is small or inconspicuous.",
                ["(a) true", "(b) false: pith is small or inconspicuous", "(c) true", "(d) true",
                 "(e) false: the pericycle is parenchymatous"],
                why="Options with (b) or (e) contain a false statement.",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous root)"),
                secs=60)

assertion_reason(T_ANA, "Tissue systems", "Advanced",
                 "The vascular bundles of dicotyledonous stems are described as open.",
                 "In dicotyledonous stems, cambium is present between the phloem and the xylem.",
                 True, True, True, "A",
                 "Open and closed vascular bundles",
                 "Vascular bundles with cambium between phloem and xylem can form secondary xylem and phloem, and "
                 "hence are called open. Dicot stems have such cambium, which is exactly why their bundles are "
                 "open. Monocot bundles lack cambium and are closed.",
                 ["A: true", "R: true", "Presence of cambium is the defining reason for 'open' → R explains A"],
                 ncert=ref("ANA", "The Tissue System (Vascular tissue system)"), secs=40)

match_list(T_ANA, "Plant tissues", "Advanced",
           "element of xylem", "feature",
           ["Tracheids", "Vessels", "Xylem fibres", "Xylem parenchyma"],
           ["Living, thin-walled cells that store starch or fat and substances like tannins",
            "Elongated, tube-like dead cells with thick, lignified walls and tapering ends",
            "Highly thickened walls and obliterated central lumen; may be septate or aseptate",
            "Long cylindrical structure of many cells, interconnected through perforations in their common walls"],
           {"A": "II", "B": "IV", "C": "III", "D": "I"},
           [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
            {"A": "II", "B": "III", "C": "IV", "D": "I"}], "C",
           "Elements of xylem",
           "Tracheids are single elongated dead cells with tapering ends. Vessels are long tubes made of many vessel "
           "members joined through perforations in their common walls. Xylem fibres have highly thickened walls and "
           "obliterated lumens and may be septate or aseptate. Xylem parenchyma is living and stores food.",
           ["Tracheids → II", "Vessels → IV", "Xylem fibres → III", "Xylem parenchyma → I"],
           why="The commonest error swaps tracheids (single cells) with vessels (many cells joined end to end).",
           ncert=ref("ANA", "The Tissues (Complex tissues: xylem)"), secs=50)

statement_pair(T_ANA, "Tissue systems", "Advanced",
               "In dicots, the outer walls of the guard cells (away from the stomatal pore) are thick and the inner "
               "walls (towards the pore) are thin.",
               "Guard cells possess chloroplasts and regulate the opening and closing of stomata.",
               False, True, "D",
               "Guard cells",
               "In dicots the guard cells are bean-shaped; their outer walls (away from the pore) are thin and the "
               "inner walls (towards the pore) are highly thickened. Guard cells have chloroplasts and regulate the "
               "opening and closing of stomata.",
               ["Statement I: false, the inner walls are thick and the outer walls thin", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System (Epidermal tissue system: stomata)"), secs=40)

# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Cell theory", "Basic",
       "Robert Brown is credited with the discovery of the:",
       "nucleus", ["cell wall", "Golgi apparatus", "ribosome"], "D",
       "History of the cell",
       "Anton von Leeuwenhoek first saw and described a live cell. Robert Brown later discovered the nucleus.",
       ["Robert Brown → nucleus"],
       why="The Golgi apparatus is named after Camillo Golgi; ribosomes were first observed by George Palade; the "
           "cell wall is not credited to Robert Brown.",
       ncert=ref("CELL", "What is a Cell?"), secs=20)

direct(T_CELL, "Cell theory", "Basic",
       "Which of the following is cited by NCERT as the largest isolated single cell?",
       "The egg of an ostrich", ["A human red blood cell", "A nerve cell", "A Mycoplasma cell"], "A",
       "Cell size",
       "Cells differ greatly in size. Mycoplasma (0.3 µm) are the smallest cells; the largest isolated single cell "
       "is the egg of an ostrich. Nerve cells are among the longest cells.",
       ["Largest isolated single cell → ostrich egg"],
       why="Mycoplasma are the smallest cells; nerve cells are among the longest, not the largest isolated cell; a "
           "human red blood cell is only about 7.0 µm across.",
       ncert=ref("CELL", "An Overview of Cell"), secs=20)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "Bacteria that take up the Gram stain are called:",
       "Gram positive", ["Gram negative", "Mycoplasma", "Archaebacteria"], "B",
       "Gram staining",
       "Based on differences in the cell envelope and in their response to the staining procedure developed by "
       "Gram, bacteria are classified into two groups: those that take up the Gram stain are Gram positive and the "
       "others that do not are Gram negative.",
       ["Takes up the stain → Gram positive"],
       why="Gram negative bacteria do not take up the stain. Mycoplasma and archaebacteria are not names of Gram "
           "staining groups.",
       ncert=ref("CELL", "Prokaryotic Cells (Cell envelope and its modifications)"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "Ribosomes were first observed under the electron microscope as dense particles by:",
       "George Palade", ["Camillo Golgi", "Robert Brown", "Rudolf Virchow"], "C",
       "Ribosomes",
       "Ribosomes are granular structures first observed under the electron microscope as dense particles by George "
       "Palade (1953). They are composed of RNA and proteins and are not surrounded by any membrane.",
       ["Ribosomes → George Palade (1953)"],
       why="Golgi described the Golgi apparatus; Brown discovered the nucleus; Virchow explained that cells arise "
           "from pre-existing cells.",
       ncert=ref("CELL", "Eukaryotic Cells (Ribosomes)"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "Besides plant cells, plastids are found in:",
       "euglenoids", ["fungi", "bacteria", "animal cells"], "D",
       "Plastids",
       "Plastids are found in all plant cells and in euglenoids. They are easily observed under the microscope as "
       "they are large, and they bear specific pigments.",
       ["Plastids: all plant cells + euglenoids"],
       why="Fungi are heterotrophs without plastids; bacteria are prokaryotes without membrane-bound organelles; "
           "animal cells lack plastids.",
       ncert=ref("CELL", "Eukaryotic Cells (Plastids)"), secs=20)

match_list(T_CELL, "Cell theory", "Intermediate",
           "cell or organelle", "size given in NCERT",
           ["Mycoplasma", "Typical bacterium", "Human red blood cell", "Mitochondrion (diameter)"],
           ["About 7.0 µm", "0.2–1.0 µm (average 0.5 µm)", "0.3 µm", "3–5 µm"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
            {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B",
           "Sizes of cells and organelles",
           "Mycoplasma, the smallest cells, are only 0.3 µm in length; bacteria are 3 to 5 µm; a human red blood "
           "cell is about 7.0 µm in diameter. A mitochondrion is 0.2–1.0 µm (average 0.5 µm) in diameter and "
           "1.0–4.1 µm long.",
           ["Mycoplasma → 0.3 µm (III)", "Bacterium → 3–5 µm (IV)", "RBC → about 7.0 µm (I)",
            "Mitochondrion → 0.2–1.0 µm diameter (II)"],
           why="The wrong codes swap Mycoplasma with the mitochondrion, the bacterium with the RBC, or Mycoplasma "
               "with the bacterium.",
           ncert=ref("CELL", "An Overview of Cell; Eukaryotic Cells (Mitochondria)"), secs=45)

multi_statement(T_CELL, "Cell envelope and membrane", "Intermediate",
                "Which of the following statements about transport across the plasma membrane are correct?",
                [("The plasma membrane is selectively permeable to some molecules present on either side of it.",
                  True),
                 ("Movement of water by diffusion is called osmosis.", True),
                 ("Passive transport across the membrane requires energy from ATP.", False),
                 ("The Na⁺/K⁺ pump is an example of active transport.", True),
                 ("Polar molecules pass freely through the non-polar lipid bilayer without any carrier protein.",
                  False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "b", "c", "d")], "C",
                "Membrane transport",
                "The membrane is selectively permeable. Many molecules cross it without using energy (passive "
                "transport); neutral solutes and water move down their concentration gradient, and the diffusion "
                "of water is osmosis. Polar molecules cannot pass the non-polar lipid bilayer and need carrier "
                "proteins. Transport against a gradient uses ATP (active transport), e.g., the Na⁺/K⁺ pump.",
                ["(a) true", "(b) true", "(c) false: passive transport needs no energy", "(d) true",
                 "(e) false: polar molecules need a carrier protein"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("CELL", "Eukaryotic Cells (Cell membrane)"), secs=55)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "The cell wall of algae is made of cellulose, galactans, mannans and minerals like calcium carbonate.",
               "The primary wall of a young plant cell is incapable of growth.",
               True, False, "C",
               "Cell wall",
               "Algal cell walls contain cellulose, galactans, mannans and minerals such as calcium carbonate; other "
               "plants have cellulose, hemicellulose, pectins and proteins. The primary wall of a young plant cell "
               "is capable of growth, which gradually diminishes as the cell matures.",
               ["Statement I: true", "Statement II: false, the primary wall can grow"],
               ncert=ref("CELL", "Eukaryotic Cells (Cell wall)"), secs=35)

assertion_reason(T_CELL, "Endomembrane system", "Intermediate",
                 "The rough endoplasmic reticulum (RER) is frequently observed in cells actively involved in protein "
                 "synthesis and secretion.",
                 "The RER bears ribosomes, the sites of protein synthesis, on its outer surface.",
                 True, True, True, "A",
                 "Rough endoplasmic reticulum",
                 "ER that bears ribosomes on its surface is the RER. Ribosomes make proteins, so cells that "
                 "synthesise and secrete much protein have extensive RER. R gives the reason for A.",
                 ["A: true", "R: true", "Ribosomes on RER make protein → explains its abundance in such cells"],
                 ncert=ref("CELL", "Eukaryotic Cells (Endoplasmic reticulum)"), secs=40)

direct(T_CELL, "Prokaryotic cell", "Intermediate",
       "Gas vacuoles are found in:",
       "blue-green and purple and green photosynthetic bacteria",
       ["Mycoplasma only", "yeast and other fungi", "animal cells"], "D",
       "Inclusion bodies of prokaryotes",
       "Reserve material in prokaryotic cells is stored in the cytoplasm as inclusion bodies (phosphate granules, "
       "cyanophycean granules, glycogen granules). Gas vacuoles are found in blue-green and purple and green "
       "photosynthetic bacteria.",
       ["Gas vacuoles → blue-green, purple and green photosynthetic bacteria"],
       why="NCERT names gas vacuoles only for these photosynthetic prokaryotes, not for Mycoplasma, fungi or animal "
           "cells.",
       ncert=ref("CELL", "Prokaryotic Cells (Inclusion bodies)"), secs=30)

direct(T_CELL, "Prokaryotic cell", "Intermediate",
       "A bacterial flagellum is composed of:",
       "filament, hook and basal body",
       ["an axoneme with a 9 + 2 arrangement of microtubules", "nine triplet microtubules and a central hub",
        "filament, central sheath and radial spokes"], "A",
       "Bacterial flagellum",
       "Motile bacterial cells have thin filamentous extensions called flagella. A bacterial flagellum has three "
       "parts: filament, hook and basal body. The filament is the longest portion and extends from the cell surface "
       "to the outside.",
       ["Bacterial flagellum = filament + hook + basal body"],
       why="The 9 + 2 axoneme, triplets with a hub, and the central sheath with radial spokes are features of "
           "eukaryotic cilia, flagella and centrioles.",
       ncert=ref("CELL", "Prokaryotic Cells (Cell envelope and its modifications)"), secs=30)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate",
               "The cytoskeleton is involved in mechanical support, motility and maintenance of the shape of the cell.",
               "The central part of the proximal region of a centriole, called the hub, is proteinaceous and is "
               "connected with the tubules of the peripheral triplets by radial spokes made of protein.",
               True, True, "A",
               "Cytoskeleton and centriole structure",
               "The cytoskeleton (microtubules, microfilaments and intermediate filaments) gives mechanical support, "
               "motility and shape. A centriole has nine evenly spaced peripheral triplet fibrils; its proximal "
               "central part, the hub, is proteinaceous and is joined to the triplets by protein radial spokes.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (Cytoskeleton; Centrosome and centrioles)"), secs=40)

multi_statement(T_CELL, "Cell envelope and membrane", "Advanced",
                "Which of the following statements about the cell membrane are correct?",
                [("The lipids are arranged with their polar heads towards the outer sides and their hydrophobic "
                  "tails towards the inner part.", True),
                 ("The ratio of protein to lipid is the same in all cell types.", False),
                 ("Peripheral proteins lie on the surface of the membrane, while integral proteins are partially or "
                  "totally buried in it.", True),
                 ("Besides lipids and proteins, cell membranes also possess carbohydrates.", True),
                 ("The fluid nature of the membrane is important for functions like cell growth, formation of "
                  "intercellular junctions, secretion, endocytosis and cell division.", True)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d", "e")], "B",
                "Structure of the cell membrane",
                "Membrane lipids form a bilayer with polar heads outwards and hydrophobic tails inwards. Membranes "
                "also contain proteins and carbohydrates, and the protein:lipid ratio varies considerably between "
                "cell types. Proteins are peripheral or integral. The fluid nature of the membrane is important for "
                "growth, junction formation, secretion, endocytosis and division.",
                ["(a) true", "(b) false: the ratio varies considerably", "(c) true", "(d) true", "(e) true"],
                why="Options with (b) are wrong; (a), (c) and (e) only leaves out the true statement (d).",
                ncert=ref("CELL", "Eukaryotic Cells (Cell membrane)"), secs=60)

assertion_reason(T_CELL, "Prokaryotic cell", "Advanced",
                 "In some bacteria the glycocalyx is a loose sheath called the slime layer, while in others it is "
                 "thick and tough and is called the capsule.",
                 "In the prokaryotic cell envelope, the plasma membrane is the outermost layer.",
                 True, False, False, "C",
                 "Prokaryotic cell envelope",
                 "The cell envelope of most prokaryotes has three tightly bound layers: the outermost glycocalyx, "
                 "then the cell wall, then the plasma membrane. The glycocalyx varies in composition and thickness: "
                 "a loose slime layer in some, a thick tough capsule in others. R is false because the plasma "
                 "membrane is the innermost layer of the envelope.",
                 ["A: true", "R: false, the glycocalyx is outermost and the plasma membrane innermost"],
                 ncert=ref("CELL", "Prokaryotic Cells (Cell envelope and its modifications)"), secs=40)

match_list(T_CELL, "Nucleus", "Advanced",
           "term", "description",
           ["Chromatin", "Satellite", "Nuclear pores", "Perinuclear space"],
           ["Passages for movement of RNA and protein molecules in both directions between the nucleus and the "
            "cytoplasm",
            "Loose, indistinct network of nucleoprotein fibres in the interphase nucleus",
            "Space of 10 to 50 nm between the two parallel membranes of the nuclear envelope",
            "Small fragment of a chromosome formed by a non-staining secondary constriction"],
           {"A": "II", "B": "IV", "C": "I", "D": "III"},
           [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
            {"A": "II", "B": "I", "C": "IV", "D": "III"}], "C",
           "The nucleus",
           "The interphase nucleus has a loose network of nucleoprotein fibres, the chromatin. A few chromosomes have "
           "non-staining secondary constrictions at a constant location, giving a small fragment, the satellite. "
           "The nuclear envelope has two membranes with a perinuclear space of 10–50 nm, which forms a barrier "
           "between nucleus and cytoplasm; nuclear pores allow RNA and proteins to move in both directions.",
           ["Chromatin → II", "Satellite → IV", "Nuclear pores → I", "Perinuclear space → III"],
           why="The wrong codes swap chromatin with satellite, nuclear pores with perinuclear space, or satellite "
               "with nuclear pores.",
           ncert=ref("CELL", "Eukaryotic Cells (Nucleus)"), secs=50)

direct(T_CELL, "Prokaryotic cell", "Advanced",
       "Which pair of structures is found alike in a bacterial cell, a plant cell and an animal cell?",
       "Plasma membrane and ribosomes",
       ["Cell wall and ribosomes", "Nuclear envelope and plasma membrane", "Mitochondria and ribosomes"], "D",
       "Features common to all cells",
       "Every cell has a plasma membrane, cytoplasm and ribosomes (70S in prokaryotes, 80S in the eukaryotic "
       "cytoplasm). Prokaryotes lack a nuclear envelope and membrane-bound organelles such as mitochondria, and "
       "animal cells lack a cell wall.",
       ["Bacterium: no nuclear envelope, no mitochondria", "Animal cell: no cell wall",
        "All three: plasma membrane and ribosomes"],
       why="Animal cells lack a cell wall; bacteria lack a nuclear envelope and mitochondria.",
       ncert=ref("CELL", "An Overview of Cell; Prokaryotic Cells"), secs=40)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
               "In a chloroplast, the stroma lamellae are stacked like piles of coins to form the grana.",
               "The membrane of the thylakoids encloses a space called the stroma.",
               False, False, "B",
               "Structure of the chloroplast",
               "The thylakoids are stacked like piles of coins to form the grana. The stroma lamellae are flat "
               "membranous tubules that connect the thylakoids of different grana. The thylakoid membrane encloses "
               "a space called the lumen; the stroma is the space enclosed by the inner membrane of the "
               "chloroplast.",
               ["Statement I: false, grana are stacks of thylakoids; stroma lamellae connect grana",
                "Statement II: false, the thylakoid membrane encloses the lumen"],
               ncert=ref("CELL", "Eukaryotic Cells (Plastids)"), secs=45)

# =============================================================== 6. Cell Cycle and Cell Division (4/6/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "A typical human cell in culture divides about once every 24 hours. Of this, the M phase (actual cell "
       "division) lasts for only about:",
       "an hour", ["12 hours", "90 minutes", "23 hours"], "A",
       "Duration of the phases of the cell cycle",
       "For a human cell in culture with a 24-hour cycle, the cell division proper (M phase) lasts only about an "
       "hour; the interphase lasts more than 95% of the cycle.",
       ["24-hour cycle: M phase ≈ 1 hour; interphase ≈ the rest"],
       why="90 minutes is the duration of the whole yeast cell cycle; 23 hours is roughly the interphase; 12 hours "
           "has no basis.",
       ncert=ref("CC", "Cell Cycle (Phases of cell cycle)"), secs=25)

direct(T_CC, "Cell cycle phases", "Basic",
       "In animal cells, the centriole duplicates during:",
       "the S phase, in the cytoplasm", ["the G1 phase, in the nucleus", "prophase, in the nucleus",
                                         "the G2 phase, in the nucleus"], "B",
       "Events of the S phase",
       "During the S phase, DNA replication begins in the nucleus, and in animal cells the centriole duplicates in "
       "the cytoplasm.",
       ["S phase: DNA replicates in the nucleus; centriole duplicates in the cytoplasm"],
       why="Centrioles lie in the cytoplasm, not the nucleus, and NCERT places their duplication in the S phase.",
       ncert=ref("CC", "Cell Cycle (Phases of cell cycle: S phase)"), secs=25)

direct(T_CC, "Meiosis", "Basic",
       "Diakinesis, the final stage of meiotic prophase I, is marked by:",
       "terminalisation of chiasmata",
       ["formation of the synaptonemal complex", "crossing over between non-sister chromatids",
        "splitting of the centromere"], "C",
       "Diakinesis",
       "During diakinesis, chiasmata are terminalised, chromosomes are fully condensed, the meiotic spindle is "
       "assembled, and by its end the nucleolus disappears and the nuclear envelope breaks down.",
       ["Diakinesis → terminalisation of chiasmata"],
       why="The synaptonemal complex forms in zygotene; crossing over occurs in pachytene; centromeres split in "
           "anaphase II.",
       ncert=ref("CC", "Meiosis (Meiosis I: prophase I)"), secs=25)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "During the G2 phase, proteins are synthesised in preparation for mitosis while cell growth continues.",
               "During the G1 phase, the cell is metabolically active and continuously grows, but does not "
               "replicate its DNA.",
               True, True, "A",
               "G1 and G2 phases",
               "G1 is the interval between mitosis and the start of DNA replication; the cell is metabolically "
               "active and grows but does not replicate DNA. In G2, proteins are synthesised in preparation for "
               "mitosis while growth continues.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Cell Cycle (Phases of cell cycle)"), secs=30)

# meiosis I in a meiocyte with 2n = 24: bivalents = n; each bivalent (tetrad) = 2 chromosomes x 2 chromatids
two_n = 24
bivalents, chromatids_per_bivalent = two_n // 2, 2 * 2
assert (bivalents, chromatids_per_bivalent) == (12, 4)
numerical(T_CC, "Meiosis", "Intermediate",
          "A meiocyte of a plant with 2n = 24 enters meiosis. How many bivalents are formed, and how many chromatids "
          "does each bivalent show at pachytene?",
          "12 bivalents, each with 4 chromatids",
          ["24 bivalents, each with 2 chromatids", "12 bivalents, each with 2 chromatids",
           "6 bivalents, each with 4 chromatids"], "D", (bivalents, chromatids_per_bivalent) == (12, 4),
          "Bivalents and tetrads",
          "In zygotene, homologous chromosomes pair (synapsis); each pair is a bivalent, so there are n = 12 "
          "bivalents. The chromosomes replicated in the S phase, so each homologue has two sister chromatids. At "
          "pachytene, the four chromatids of each bivalent become distinct and clearly appear as tetrads.",
          ["Bivalents = 2n / 2 = 12", "Chromatids per bivalent = 2 homologues × 2 chromatids = 4"],
          "24 bivalents counts each chromosome as a bivalent. Two chromatids per bivalent forgets that each "
          "homologue has already replicated. 6 bivalents halves the number twice.",
          ref("CC", "Meiosis (Meiosis I: prophase I)"), secs=45)

match_list(T_CC, "Meiosis", "Intermediate",
           "stage of meiosis", "event",
           ["Metaphase I", "Telophase I", "Prophase II", "Anaphase II"],
           ["The centromere of each chromosome splits and the sister chromatids move towards opposite poles",
            "The nuclear membrane and nucleolus reappear; cytokinesis follows to form a dyad of cells",
            "The bivalent chromosomes align on the equatorial plate",
            "The nuclear membrane disappears by the end of this stage and the chromosomes again become compact"],
           {"A": "III", "B": "II", "C": "IV", "D": "I"},
           [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "I", "B": "II", "C": "IV", "D": "III"},
            {"A": "II", "B": "III", "C": "IV", "D": "I"}], "B",
           "Stages of meiosis I and II",
           "In metaphase I the bivalents align on the equatorial plate. In telophase I the nuclear membrane and "
           "nucleolus reappear and cytokinesis gives a dyad of cells. In prophase II the nuclear membrane "
           "disappears by the end and chromosomes compact again. Anaphase II begins with simultaneous splitting of "
           "the centromere of each chromosome, so sister chromatids move to opposite poles.",
           ["Metaphase I → III", "Telophase I → II", "Prophase II → IV", "Anaphase II → I"],
           why="The wrong codes swap telophase I with prophase II, metaphase I with anaphase II, or metaphase I with "
               "telophase I.",
           ncert=ref("CC", "Meiosis (Meiosis I; Meiosis II)"), secs=50)

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "Mitosis is also called equational division.",
                 "In mitosis, the number of chromosomes in the parent cell and in the progeny cells is the same.",
                 True, True, True, "A",
                 "Equational division",
                 "Since the number of chromosomes in the parent and progeny cells is the same, mitosis is called "
                 "equational division. R is the very reason for the name.",
                 ["A: true", "R: true and is the reason for the name → A"],
                 ncert=ref("CC", "M Phase"), secs=30)

multi_statement(T_CC, "Cell cycle phases", "Intermediate",
                "Which of the following statements about the cell cycle are correct?",
                [("Interphase lasts more than 95 per cent of the duration of the cell cycle.", True),
                 ("Some cells in adult animals, such as heart cells, do not appear to divide.", True),
                 ("Interphase is divided into the G1, S and M phases.", False),
                 ("The G1 phase is the interval between mitosis and the initiation of DNA replication.", True),
                 ("The G2 phase is the interval between the S phase and the G1 phase.", False)],
                [("a", "b", "c"), ("b", "c", "d"), ("a", "d", "e")], "C",
                "Interphase",
                "Interphase lasts more than 95% of the cycle and is divided into G1, S and G2. G1 lies between "
                "mitosis and the start of DNA replication; G2 lies between S and the M phase. Some adult animal "
                "cells, e.g., heart cells, do not appear to divide.",
                ["(a) true", "(b) true", "(c) false: G1, S and G2", "(d) true",
                 "(e) false: G2 lies between S and M"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("CC", "Cell Cycle (Phases of cell cycle)"), secs=55)

direct(T_CC, "Mitosis", "Intermediate",
       "At metaphase of mitosis, the two sister chromatids of a chromosome are attached by their kinetochores to "
       "spindle fibres:",
       "from opposite poles", ["from the same pole", "at their arms rather than at the kinetochores",
                               "only one chromatid is attached; the other is free"], "D",
       "Metaphase",
       "At metaphase, all chromosomes lie at the equator. One chromatid of each chromosome is connected by its "
       "kinetochore to spindle fibres from one pole, and its sister chromatid by its kinetochore to spindle fibres "
       "from the opposite pole.",
       ["Kinetochore of one chromatid → one pole; kinetochore of the sister → opposite pole"],
       why="Attachment to the same pole could not separate the chromatids; spindle fibres attach at kinetochores; "
           "both chromatids are attached.",
       ncert=ref("CC", "M Phase (Metaphase)"), secs=30)

assertion_reason(T_CC, "Significance", "Intermediate",
                 "Cell repair by mitosis is seen only in plants; in animals, cells such as those of the upper layer "
                 "of the epidermis and the lining of the gut are never replaced.",
                 "Mitotic divisions in the meristematic tissues, the apical and the lateral cambium, result in a "
                 "continuous growth of plants throughout their life.",
                 False, True, False, "D",
                 "Significance of mitosis",
                 "Mitosis also repairs and replaces cells in animals: cells of the upper layer of the epidermis, "
                 "cells of the lining of the gut and blood cells are constantly replaced. So A is false. R is true: "
                 "mitosis in the apical and lateral cambium gives continuous growth of plants.",
                 ["A: false, such animal cells are constantly replaced", "R: true"],
                 ncert=ref("CC", "Significance of Mitosis"), secs=40)

# 2n = 18; at metaphase II each cell has n chromosomes, each still with two chromatids
two_n = 18
mII_chromosomes = two_n // 2
mII_chromatids = 2 * mII_chromosomes
assert (mII_chromosomes, mII_chromatids) == (9, 18)
numerical(T_CC, "Meiosis", "Advanced",
          "A plant has 2n = 18. How many chromosomes and how many chromatids are present in each cell at metaphase "
          "II of meiosis?",
          "9 chromosomes and 18 chromatids",
          ["18 chromosomes and 36 chromatids", "9 chromosomes and 9 chromatids", "18 chromosomes and 18 chromatids"],
          "A", (mII_chromosomes, mII_chromatids) == (9, 18),
          "Chromosome and chromatid number in meiosis II",
          "Anaphase I separates homologous chromosomes, so each cell after meiosis I has n = 9 chromosomes. The "
          "sister chromatids stay joined at the centromere until anaphase II, so at metaphase II each of the 9 "
          "chromosomes still has two chromatids.",
          ["After meiosis I: n = 9 chromosomes", "Each chromosome = 2 sister chromatids until anaphase II",
           "Chromatids = 9 × 2 = 18"],
          "18 and 36 is the count at metaphase of mitosis. 9 and 9 assumes the chromatids have already separated. "
          "18 and 18 forgets the reduction in meiosis I.",
          ref("CC", "Meiosis (Meiosis II)"), secs=50)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements about meiosis are correct?",
                [("Meiosis involves two sequential cycles of nuclear and cell division but only a single cycle of "
                  "DNA replication.", True),
                 ("Meiosis I is initiated before the parental chromosomes replicate.", False),
                 ("Meiosis involves pairing of homologous chromosomes and recombination between non-sister "
                  "chromatids of homologous chromosomes.", True),
                 ("Four haploid cells are formed at the end of meiosis II.", True),
                 ("The prophase of mitosis is typically longer and more complex than prophase I of meiosis.",
                  False)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("c", "d", "e")], "B",
                "Key features of meiosis",
                "Meiosis has two cycles of division with one round of DNA replication. Meiosis I starts after the "
                "chromosomes have replicated in the S phase. Homologues pair and recombine, and meiosis II ends "
                "with four haploid cells. Prophase I is typically longer and more complex than the prophase of "
                "mitosis.",
                ["(a) true", "(b) false: meiosis I starts after replication", "(c) true", "(d) true",
                 "(e) false: prophase I is the longer and more complex one"],
                why="Options with (b) or (e) contain a false statement.",
                ncert=ref("CC", "Meiosis"), secs=55)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "Each of the two cells formed at the end of meiosis I has half the number of chromosomes of the "
                 "parent meiocyte.",
                 "In anaphase I, the homologous chromosomes separate, while the sister chromatids remain associated "
                 "at their centromeres.",
                 True, True, True, "A",
                 "Why meiosis I is reductional",
                 "In anaphase I, whole homologous chromosomes (each with two chromatids) move to opposite poles. "
                 "Each pole therefore receives one member of each pair, so the chromosome number is halved. R is "
                 "the explanation of A.",
                 ["A: true", "R: true", "Separation of homologues halves the chromosome number → R explains A"],
                 ncert=ref("CC", "Meiosis (Meiosis I: anaphase I)"), secs=45)

statement_pair(T_CC, "Cell cycle phases", "Advanced",
               "Yeast can progress through the cell cycle in only about 90 minutes.",
               "Although cell growth (in terms of cytoplasmic increase) is a continuous process, DNA synthesis "
               "occurs only during one specific stage of the cell cycle.",
               True, True, "A",
               "Duration of the cell cycle; growth versus DNA synthesis",
               "The duration of the cell cycle varies between organisms and cell types: yeast completes it in about "
               "90 minutes. Cytoplasmic growth is continuous, but DNA is synthesised only in the S phase.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Cell Cycle"), secs=35)

# =============================================================== 7. Photosynthesis (5/6/5)
direct(T_PS, "Site and pigments", "Basic",
       "Within the chloroplast, the enzymatic reactions that synthesise sugar take place in the:",
       "stroma", ["grana", "thylakoid lumen", "outer membrane"], "C",
       "Division of labour in the chloroplast",
       "The membrane system (grana and stroma lamellae) traps light energy and makes ATP and NADPH. In the stroma, "
       "enzymatic reactions incorporate CO₂ into the plant, leading to the synthesis of sugar, which in turn forms "
       "starch.",
       ["Light trapping, ATP, NADPH → membrane system", "Sugar synthesis → stroma"],
       why="The grana carry out the light reactions; the lumen is where protons accumulate; the outer membrane has "
           "no role in sugar synthesis.",
       ncert=ref("PS", "Where does Photosynthesis take place?"), secs=25)

direct(T_PS, "Site and pigments", "Basic",
       "Besides enabling a wider range of wavelengths of incoming light to be used for photosynthesis, the accessory "
       "pigments also:",
       "protect chlorophyll a from photo-oxidation",
       ["act as the reaction centre of both photosystems", "split water to release oxygen",
        "fix CO₂ in the stroma"], "D",
       "Accessory pigments",
       "Chlorophyll b, xanthophylls and carotenoids are accessory pigments. They absorb light and transfer the "
       "energy to chlorophyll a, and they also protect chlorophyll a from photo-oxidation.",
       ["Accessory pigments: widen the usable spectrum + protect chlorophyll a"],
       why="The reaction centre is a chlorophyll a molecule; water splitting is linked to PS II; CO₂ is fixed by "
           "RuBisCO, an enzyme.",
       ncert=ref("PS", "How many types of pigments are involved in photosynthesis?"), secs=25)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "The reaction centre of Photosystem II has an absorption peak at:",
       "680 nm", ["700 nm", "660 nm", "720 nm"], "A",
       "Reaction centres",
       "In PS I the reaction-centre chlorophyll a has an absorption peak at 700 nm (P700); in PS II it has an "
       "absorption peak at 680 nm (P680).",
       ["PS II → P680", "PS I → P700"],
       why="700 nm is the peak of PS I. 660 nm and 720 nm are not reaction-centre peaks given by NCERT.",
       ncert=ref("PS", "What is Light Reaction?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Which enzyme is described by NCERT as the most abundant enzyme in the world?",
       "RuBisCO", ["PEP carboxylase", "ATP synthase", "NADP reductase"], "B",
       "RuBisCO",
       "RuBP carboxylase-oxygenase (RuBisCO), which catalyses the carboxylation of RuBP, is the most abundant enzyme "
       "in the world.",
       ["Most abundant enzyme in the world → RuBisCO"],
       why="PEP carboxylase fixes CO₂ in the mesophyll of C4 plants, ATP synthase makes ATP and NADP reductase "
           "reduces NADP⁺; none of these is described as the most abundant enzyme.",
       ncert=ref("PS", "Photorespiration"), secs=20)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Basic",
               "The Calvin cycle occurs only in plants that have the C3 pathway.",
               "The Calvin cycle can be described under three stages: carboxylation, reduction and regeneration.",
               False, True, "D",
               "The Calvin cycle",
               "The Calvin pathway occurs in all photosynthetic plants, whether they have C3 or C4 pathways. It has "
               "three stages: carboxylation of RuBP, reduction to carbohydrate, and regeneration of RuBP.",
               ["Statement I: false, it occurs in all photosynthetic plants", "Statement II: true"],
               ncert=ref("PS", "The Calvin Cycle"), secs=30)

# Calvin cycle: each CO2 carboxylates one RuBP and gives two 3-PGA
co2 = 6
rubp_used, pga_formed = co2 * 1, co2 * 2
assert (rubp_used, pga_formed) == (6, 12)
numerical(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
          "In the carboxylation step of the Calvin cycle, how many molecules of RuBP are used and how many molecules "
          "of 3-PGA are formed when six molecules of CO₂ are fixed?",
          "6 RuBP and 12 PGA", ["6 RuBP and 6 PGA", "12 RuBP and 12 PGA", "3 RuBP and 6 PGA"], "C",
          (rubp_used, pga_formed) == (6, 12),
          "Carboxylation of RuBP",
          "Carboxylation is the fixation of CO₂ into RuBP, catalysed by RuBisCO; each carboxylation gives two "
          "molecules of 3-PGA. So each CO₂ uses one RuBP and forms two PGA.",
          ["1 CO₂ + 1 RuBP → 2 PGA", "6 CO₂ → 6 RuBP used, 12 PGA formed"],
          "6 PGA forgets that each carboxylation yields two PGA. 12 RuBP doubles the RuBP instead of the PGA. "
          "3 RuBP and 6 PGA halves both, as if two CO₂ were fixed per RuBP.",
          ref("PS", "The Calvin Cycle (Carboxylation)"), secs=45)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following statements about C4 plants are correct?",
                [("'Kranz' means 'wreath' and reflects the arrangement of cells around the vascular bundles.",
                  True),
                 ("C4 plants tolerate higher temperatures.", True),
                 ("Maize and sorghum are examples of C3 plants.", False),
                 ("The C4 acid formed in the mesophyll is converted to malic acid or aspartic acid, which is "
                  "transported to the bundle sheath cells.", True),
                 ("C4 plants show a poor response to high light intensities.", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "b", "d", "e")], "D",
                "C4 plants and Kranz anatomy",
                "C4 plants such as maize and sorghum have Kranz anatomy ('wreath' of bundle sheath cells). They "
                "tolerate higher temperatures and respond to high light intensities. OAA formed in the mesophyll is "
                "converted to malic or aspartic acid, which moves to the bundle sheath.",
                ["(a) true", "(b) true", "(c) false: they are C4 plants", "(d) true",
                 "(e) false: they respond to high light intensities"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("PS", "The C4 Pathway"), secs=55)

assertion_reason(T_PS, "Photorespiration", "Intermediate",
                 "When CO₂ and O₂ are present in nearly equal concentrations, RuBisCO has a greater affinity for O₂ "
                 "than for CO₂.",
                 "The active site of RuBisCO can bind both CO₂ and O₂, and the relative concentration of O₂ and CO₂ "
                 "determines which of the two will bind to the enzyme.",
                 False, True, False, "D",
                 "Dual nature of RuBisCO",
                 "RuBisCO's active site binds both gases competitively, and their relative concentrations decide "
                 "which binds. RuBisCO has a much greater affinity for CO₂ than for O₂ when the CO₂:O₂ ratio is "
                 "nearly equal, so A is false.",
                 ["A: false, the affinity is greater for CO₂", "R: true"],
                 ncert=ref("PS", "Photorespiration"), secs=40)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Intermediate",
               "The membranes of the stroma lamellae contain both PS I and PS II.",
               "Cyclic photophosphorylation possibly takes place in the stroma lamellae, as they lack PS II and the "
               "enzyme NADP reductase.",
               False, True, "D",
               "Site of cyclic photophosphorylation",
               "The membranes of the grana have both PS I and PS II, but the stroma lamellae lack PS II as well as "
               "NADP reductase. With only PS I working, the excited electron is cycled back, so the stroma lamellae "
               "are a likely site of cyclic photophosphorylation.",
               ["Statement I: false, stroma lamellae lack PS II", "Statement II: true"],
               ncert=ref("PS", "The Electron Transport (Cyclic and non-cyclic photo-phosphorylation)"), secs=40)

direct(T_PS, "Chemiosmosis", "Intermediate",
       "Which of the following does NOT help to build up the proton gradient across the thylakoid membrane?",
       "Flow of protons from the lumen to the stroma through the CF₀ channel of ATP synthase",
       ["Splitting of water on the inner (lumen) side of the membrane",
        "Transfer of protons across the membrane as electrons move through the photosystems",
        "Removal of protons from the stroma by NADP reductase during reduction of NADP⁺"], "B",
       "Building and using the proton gradient",
       "Three events raise the proton concentration in the lumen relative to the stroma: water splitting on the "
       "lumen side, proton transport across the membrane by an H carrier as electrons pass, and removal of stroma "
       "protons by NADP reductase. The flow of protons back through CF₀ to the stroma breaks down the gradient; its "
       "energy is used by CF₁ to make ATP.",
       ["Gradient built by: water splitting, H-carrier transport, NADP reductase",
        "Gradient used by: proton flow through CF₀ → ATP"],
       why="The other three are the NCERT list of events that create the gradient.",
       ncert=ref("PS", "Where are the ATP and NADPH used? / The Chemiosmotic Hypothesis"), secs=45)

direct(T_PS, "Limiting factors", "Intermediate",
       "Which statement about the effect of temperature on photosynthesis is correct?",
       "The dark reactions, being enzymatic, are temperature controlled; the light reactions are affected to a much "
       "lesser extent",
       ["The light reactions are much more temperature sensitive than the dark reactions",
        "C3 plants have a higher temperature optimum than C4 plants",
        "All plants have the same temperature optimum, whatever their habitat"], "C",
       "Temperature as a factor",
       "The dark reactions are enzymatic and so are temperature controlled; the light reactions are also "
       "temperature sensitive but much less so. C4 plants respond to higher temperatures and have a higher optimum "
       "than C3 plants, and the optimum depends on the habitat (tropical plants have a higher optimum than "
       "temperate ones).",
       ["Enzymatic dark reactions → strongly temperature dependent", "C4 optimum > C3 optimum",
        "Optimum depends on habitat"],
       why="The other options reverse the NCERT statements on light reactions, on C3 versus C4 plants, and on "
           "habitat.",
       ncert=ref("PS", "Factors affecting Photosynthesis (Temperature)"), secs=40)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Advanced",
                "Which of the following statements about the electron transport in the light reaction are correct?",
                [("Electrons excited in the reaction centre of PS II are picked up by an electron acceptor that "
                  "passes them to an electron transport system consisting of cytochromes.", True),
                 ("The electrons move uphill, in terms of the redox potential scale, from PS II to PS I.", False),
                 ("The Z scheme gets its name from the shape formed when all the carriers are placed in sequence "
                  "on a redox potential scale.", True),
                 ("The oxygen evolved in photosynthesis comes from carbon dioxide.", False),
                 ("The reaction centre is a single chlorophyll a molecule, and it is different in the two "
                  "photosystems.", True)],
                [("a", "b", "c"), ("c", "d", "e"), ("a", "b", "c", "e")], "D",
                "Electron transport and the Z scheme",
                "Excited electrons from PS II pass to an acceptor and then through cytochromes to PS I; this "
                "movement is downhill on the redox potential scale. Plotted on that scale, the carriers form a Z. "
                "Oxygen comes from the splitting of water, not CO₂. Each photosystem has a different chlorophyll a "
                "reaction centre (P680, P700).",
                ["(a) true", "(b) false: the movement is downhill", "(c) true",
                 "(d) false: O₂ comes from water", "(e) true"],
                why="Options with (b) or (d) contain a false statement.",
                ncert=ref("PS", "The Electron Transport; Splitting of Water"), secs=60)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "The productivity and yields of C4 plants are better than those of C3 plants.",
                 "C4 plants have a mechanism that increases the concentration of CO₂ at the site of RuBisCO, so "
                 "photorespiration does not occur in them.",
                 True, True, True, "A",
                 "Why C4 plants are more productive",
                 "In C4 plants, decarboxylation of the C4 acid in bundle sheath cells raises the CO₂ concentration "
                 "around RuBisCO, so the enzyme acts as a carboxylase and photorespiration does not occur. NCERT "
                 "states that this explains why productivity and yields are better in these plants.",
                 ["A: true", "R: true", "Absence of photorespiration → better productivity → R explains A"],
                 ncert=ref("PS", "Photorespiration"), secs=40)

statement_pair(T_PS, "Limiting factors", "Advanced",
               "There is a linear relationship between incident light and the rate of CO₂ fixation at high light "
               "intensities.",
               "Water stress reduces photosynthesis because it causes the stomata to close, reducing CO₂ "
               "availability, and makes leaves wilt, reducing their surface area and metabolic activity.",
               False, True, "D",
               "Light and water as factors",
               "The relationship between incident light and CO₂ fixation is linear at low light intensities; at "
               "higher intensities the rate stops rising as other factors become limiting. Water affects "
               "photosynthesis mostly indirectly: water stress closes stomata (less CO₂) and makes leaves wilt.",
               ["Statement I: false, linear only at low light", "Statement II: true"],
               ncert=ref("PS", "Factors affecting Photosynthesis (Light; Water)"), secs=45)

direct(T_PS, "Calvin cycle and C4 pathway", "Advanced",
       "In the C4 pathway, the C4 acid is broken down in the bundle sheath cells to release CO₂ and a 3-carbon "
       "molecule. In the mesophyll cells, this 3-carbon molecule is converted back to:",
       "phosphoenol pyruvate (PEP)", ["ribulose bisphosphate (RuBP)", "oxaloacetic acid (OAA)",
                                      "3-phosphoglyceric acid (PGA)"], "A",
       "Completing the C4 cycle",
       "In the bundle sheath, the C4 acid is decarboxylated; the CO₂ enters the Calvin cycle and the 3-carbon "
       "molecule returns to the mesophyll, where it is converted to PEP again, ready to accept CO₂.",
       ["Mesophyll: PEP + CO₂ → OAA (C4)", "Bundle sheath: C4 acid → CO₂ + C3 molecule",
        "Mesophyll: C3 molecule → PEP (cycle complete)"],
       why="RuBP is regenerated in the Calvin cycle of the bundle sheath; OAA is the first product of fixation, not "
           "the regenerated acceptor; PGA is the product of RuBP carboxylation.",
       ncert=ref("PS", "The C4 Pathway"), secs=45)

direct(T_PS, "Limiting factors", "Advanced",
       "A plant growing in deep shade on a dense forest floor is supplied with extra CO₂, but its rate of "
       "photosynthesis does not change. When the light falling on it is increased, the rate rises. Which conclusion "
       "is correct?",
       "Light was the limiting factor, because the rate is set by the factor nearest to its minimal value",
       ["CO₂ was the limiting factor, because CO₂ always limits photosynthesis",
        "Light was the limiting factor, because light is limiting for all plants in nature",
        "Neither factor was limiting; the rise was due to stomatal opening alone"], "B",
       "Blackman's law of limiting factors",
       "If a process is affected by more than one factor, its rate is determined by the factor nearest to its "
       "minimal value. Extra CO₂ had no effect, but more light raised the rate, so light was nearest its minimum. "
       "Light is rarely limiting in nature, except for plants in shade or in dense forests, which is the situation "
       "here.",
       ["Raising CO₂: no change → CO₂ was not limiting", "Raising light: rate rises → light was limiting"],
       why="Extra CO₂ had no effect, so CO₂ was not limiting here. Light is not limiting for all plants (light "
           "saturation occurs at about 10% of full sunlight); it limits here because the plant is in deep shade. "
           "The observed response to light shows a limiting factor was acting.",
       ncert=ref("PS", "Factors affecting Photosynthesis (Law of limiting factors; Light)"), secs=60)

# =============================================================== 8. Respiration in Plants (4/5/4)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "Glycolysis takes place in the:",
       "cytoplasm of the cell", ["mitochondrial matrix", "inner mitochondrial membrane", "stroma of chloroplasts"],
       "C",
       "Site of glycolysis",
       "Glycolysis, the partial oxidation of glucose to two molecules of pyruvic acid, takes place in the cytoplasm "
       "and is present in all living organisms.",
       ["Glycolysis → cytoplasm", "TCA cycle → matrix", "ETS → inner mitochondrial membrane"],
       why="The matrix is the site of the TCA cycle, the inner membrane of the ETS, and the stroma of the Calvin "
           "cycle.",
       ncert=ref("RES", "Glycolysis"), secs=20)

direct(T_RES, "Glycolysis and fermentation", "Basic",
       "In yeast, under anaerobic conditions, pyruvic acid is converted to:",
       "CO₂ and ethanol", ["lactic acid", "acetyl CoA and CO₂", "citric acid"], "D",
       "Alcoholic fermentation",
       "In fermentation, say by yeast, incomplete oxidation of glucose under anaerobic conditions converts pyruvic "
       "acid to CO₂ and ethanol. The enzymes pyruvic acid decarboxylase and alcohol dehydrogenase catalyse these "
       "reactions.",
       ["Yeast, anaerobic: pyruvic acid → CO₂ + ethanol"],
       why="Lactic acid is formed by some bacteria and by muscle cells when oxygen is inadequate. Acetyl CoA is "
           "formed aerobically in mitochondria. Citric acid is a TCA cycle intermediate.",
       ncert=ref("RES", "Fermentation"), secs=20)

direct(T_RES, "TCA cycle", "Basic",
       "The oxidative decarboxylation of pyruvic acid to acetyl CoA in the mitochondrial matrix is catalysed by:",
       "pyruvic dehydrogenase", ["pyruvic acid decarboxylase", "lactate dehydrogenase", "hexokinase"], "A",
       "Link reaction",
       "Pyruvate enters the mitochondrial matrix and undergoes oxidative decarboxylation by a complex set of "
       "reactions catalysed by pyruvic dehydrogenase, which needs several coenzymes including NAD⁺ and coenzyme A. "
       "Acetyl CoA, CO₂ and NADH are formed.",
       ["Pyruvic acid + CoA + NAD⁺ → acetyl CoA + CO₂ + NADH + H⁺ (pyruvic dehydrogenase)"],
       why="Pyruvic acid decarboxylase acts in alcoholic fermentation; lactate dehydrogenase forms lactic acid; "
           "hexokinase phosphorylates glucose in glycolysis.",
       ncert=ref("RES", "Aerobic Respiration"), secs=25)

statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "Yeasts poison themselves to death when the concentration of alcohol reaches about 13 per cent.",
               "In plants, sucrose is converted into glucose and fructose by the enzyme hexokinase.",
               True, False, "C",
               "Fermentation; sources of glucose",
               "Yeasts die when the alcohol they produce reaches about 13 per cent. In plants, glucose comes from "
               "sucrose (the end product of photosynthesis) or storage carbohydrates; sucrose is converted into "
               "glucose and fructose by invertase. Hexokinase phosphorylates glucose.",
               ["Statement I: true", "Statement II: false, the enzyme is invertase"],
               ncert=ref("RES", "Glycolysis; Fermentation"), secs=35)

# glycolysis per glucose: ATP used at 2 steps; ATP made at BPGA->PGA and PEP->pyruvate, each for 2 trioses
atp_used = 2
atp_formed = 2 * 2
assert (atp_formed, atp_formed - atp_used) == (4, 2)
numerical(T_RES, "Glycolysis and fermentation", "Intermediate",
          "During glycolysis of one molecule of glucose, ATP is used at two steps and is formed when BPGA is "
          "converted to PGA and when PEP is converted to pyruvic acid. How many ATP molecules are formed directly, "
          "and what is the net gain of ATP?",
          "4 formed; net gain 2", ["2 formed; net gain 2", "4 formed; net gain 4", "2 formed; net gain 0"], "B",
          (atp_formed, atp_formed - atp_used) == (4, 2),
          "ATP balance of glycolysis",
          "One glucose splits into two triose phosphates, so each ATP-forming step occurs twice: BPGA → PGA gives 2 "
          "ATP and PEP → pyruvic acid gives 2 ATP, 4 in all. Two ATP are used (glucose → glucose-6-phosphate and "
          "fructose-6-phosphate → fructose 1,6-bisphosphate). Net gain = 4 − 2 = 2.",
          ["ATP formed = 2 steps × 2 trioses = 4", "ATP used = 2", "Net = 4 − 2 = 2"],
          "2 formed counts each step only once (forgetting the two trioses). Net gain 4 ignores the two ATP used. "
          "2 formed with net 0 makes both mistakes together.",
          ref("RES", "Glycolysis"), secs=50)

match_list(T_RES, "TCA cycle", "Intermediate",
           "compound", "number of carbon atoms",
           ["Pyruvic acid", "Citric acid", "α-Ketoglutaric acid", "Malic acid"],
           ["Four", "Five", "Three", "Six"],
           {"A": "III", "B": "IV", "C": "II", "D": "I"},
           [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "I", "B": "IV", "C": "II", "D": "III"},
            {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C",
           "Carbon skeletons in respiration",
           "Glycolysis gives the 3-carbon pyruvic acid. In the TCA cycle, the 2-carbon acetyl group joins the "
           "4-carbon OAA to give 6-carbon citric acid; two decarboxylations give 5-carbon α-ketoglutaric acid and "
           "then the 4-carbon succinyl CoA; malic acid is a 4-carbon acid that is oxidised to OAA.",
           ["Pyruvic acid → 3 (III)", "Citric acid → 6 (IV)", "α-Ketoglutaric acid → 5 (II)", "Malic acid → 4 (I)"],
           why="The wrong codes swap the 6- and 5-carbon acids, the 3- and 4-carbon acids, or α-ketoglutaric and "
               "malic acid.",
           ncert=ref("RES", "Tricarboxylic Acid Cycle (Figure: the Citric acid cycle)"), secs=45)

assertion_reason(T_RES, "Electron transport system", "Intermediate",
                 "Plants can get along without specialised respiratory organs.",
                 "Each plant part takes care of its own gas-exchange needs, and there is very little transport of "
                 "gases from one plant part to another.",
                 True, True, True, "A",
                 "Gas exchange in plants",
                 "NCERT gives this as the first reason plants manage without respiratory organs: each part meets its "
                 "own gas-exchange needs with very little transport of gases between parts. (Plants also have low "
                 "demands for gas exchange, and most living cells lie close to the surface.)",
                 ["A: true", "R: true and is a stated reason → R explains A"],
                 ncert=ref("RES", "Do Plants Breathe?"), secs=40)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "Which of the following statements about the TCA cycle are correct?",
                [("During the conversion of succinyl CoA to succinic acid, a molecule of GTP is synthesised.", True),
                 ("The TCA cycle takes place in the cytoplasm.", False),
                 ("There are three points in the cycle where NAD⁺ is reduced to NADH + H⁺ and one point where FAD⁺ "
                  "is reduced to FADH₂.", True),
                 ("Two successive decarboxylations lead to the formation of α-ketoglutaric acid and then succinyl "
                  "CoA.", True),
                 ("Citric acid is isomerised to malic acid.", False)],
                [("a", "b", "c"), ("c", "d", "e"), ("a", "b", "d", "e")], "D",
                "Tricarboxylic acid cycle",
                "The TCA cycle runs in the mitochondrial matrix. Citrate is isomerised to isocitrate; two successive "
                "decarboxylations give α-ketoglutaric acid and then succinyl CoA. Succinyl CoA → succinic acid "
                "makes a GTP (substrate-level phosphorylation). NAD⁺ is reduced at three points and FAD⁺ at one.",
                ["(a) true", "(b) false: mitochondrial matrix", "(c) true", "(d) true",
                 "(e) false: citrate is isomerised to isocitrate"],
                why="Options with (b) or (e) contain a false statement.",
                ncert=ref("RES", "Tricarboxylic Acid Cycle"), secs=55)

statement_pair(T_RES, "Respiratory quotient", "Intermediate",
               "When fats are used as the respiratory substrate, the RQ is less than 1.",
               "When proteins are used as the respiratory substrate, the RQ is about 0.9.",
               True, True, "A",
               "RQ of different substrates",
               "RQ depends on the substrate. For carbohydrates it is 1; for fats it is less than 1 (tripalmitin "
               "gives about 0.7); for proteins it is about 0.9.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Respiratory Quotient"), secs=30)

# one glucose -> 2 pyruvate; link reaction 1 CO2 per pyruvate; TCA 2 CO2 per acetyl CoA
pyruvates = 2
co2_link, co2_tca = pyruvates * 1, pyruvates * 2
assert (co2_link + co2_tca, co2_tca) == (6, 4)
numerical(T_RES, "TCA cycle", "Advanced",
          "One molecule of glucose is completely oxidised by aerobic respiration. How many molecules of CO₂ are "
          "released in all by the conversion of pyruvic acid to acetyl CoA and the TCA cycle together, and how many "
          "of these are released in the TCA cycle itself?",
          "6 in all; 4 in the TCA cycle", ["6 in all; 6 in the TCA cycle", "3 in all; 2 in the TCA cycle",
                                           "4 in all; 2 in the TCA cycle"], "B",
          (co2_link + co2_tca, co2_tca) == (6, 4),
          "Where the six CO₂ of glucose are released",
          "Glycolysis releases no CO₂ and gives 2 pyruvic acid. Each pyruvic acid loses one CO₂ when it becomes "
          "acetyl CoA (2 in all). Each acetyl CoA loses two CO₂ in the two decarboxylations of the TCA cycle (4 in "
          "all). Total 6, matching the 6 carbons of glucose.",
          ["Link reaction: 2 pyruvate × 1 = 2 CO₂", "TCA cycle: 2 acetyl CoA × 2 = 4 CO₂", "Total = 6 CO₂"],
          "6 in the TCA cycle forgets the CO₂ of the link reaction. 3 and 2 counts one pyruvic acid instead of two. "
          "4 and 2 counts the TCA cycle for only one acetyl CoA.",
          ref("RES", "Aerobic Respiration; Tricarboxylic Acid Cycle"), secs=60)

multi_statement(T_RES, "ATP yield and amphibolic pathway", "Advanced",
                "Which of the following statements about the respiratory balance sheet are correct?",
                [("It assumes a sequential, orderly pathway, with one substrate forming the next and glycolysis, the "
                  "TCA cycle and the ETS following one after another.", True),
                 ("It assumes that the NADH synthesised in glycolysis is oxidised in the cytoplasm without entering "
                  "the mitochondria.", False),
                 ("It assumes that none of the intermediates in the pathway is used to synthesise any other "
                  "compound.", True),
                 ("Its assumptions are fully valid in a living system.", False),
                 ("On these assumptions, there can be a net gain of 38 ATP molecules during aerobic respiration of "
                  "one molecule of glucose.", True)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("b", "c", "e")], "C",
                "The respiratory balance sheet",
                "The calculation assumes an orderly sequential pathway, that glycolytic NADH is transferred into "
                "the mitochondria for oxidative phosphorylation, that no intermediates are withdrawn, and that only "
                "glucose is respired. On these assumptions the net gain is 38 ATP per glucose. These assumptions "
                "are not really valid in a living system, where all pathways work simultaneously and substrates "
                "enter and leave as needed.",
                ["(a) true", "(b) false: glycolytic NADH is assumed to enter the mitochondria", "(c) true",
                 "(d) false: the assumptions are not really valid in a living system", "(e) true"],
                why="Options with (b) or (d) contain a false statement.",
                ncert=ref("RES", "The Respiratory Balance Sheet"), secs=60)

assertion_reason(T_RES, "Electron transport system", "Advanced",
                 "Although the role of oxygen is limited to the terminal stage of aerobic respiration, its presence "
                 "is vital.",
                 "Oxygen acts as the first hydrogen acceptor, receiving hydrogen during glycolysis.",
                 True, False, False, "C",
                 "Role of oxygen",
                 "Oxygen acts only at the terminal stage, yet it is vital because it drives the whole process by "
                 "removing hydrogen from the system; it is the final hydrogen acceptor. In glycolysis, hydrogen is "
                 "accepted by NAD⁺, not oxygen, so R is false.",
                 ["A: true", "R: false, oxygen is the final hydrogen acceptor; NAD⁺ accepts hydrogen in glycolysis"],
                 ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=40)

statement_pair(T_RES, "Glycolysis and fermentation", "Advanced",
               "In glycolysis, glucose undergoes partial oxidation to form two molecules of pyruvic acid.",
               "In both lactic acid and alcoholic fermentation, the reducing agent is NADH + H⁺, which is reoxidised "
               "to NAD⁺.",
               True, True, "A",
               "Glycolysis and fermentation",
               "Glycolysis partially oxidises glucose to two pyruvic acid. In both lactic acid and alcohol "
               "fermentation, not much energy is released; the reducing agent NADH + H⁺ is reoxidised to NAD⁺, "
               "which keeps glycolysis going.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Glycolysis; Fermentation"), secs=35)


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
    assert pkg["output"] == "batches/parts/BATCH_002_BOT_p1.json"


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "Package BOT_002_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 125 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
