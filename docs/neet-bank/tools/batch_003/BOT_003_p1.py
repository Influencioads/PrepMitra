"""Writes batches/parts/BATCH_003_BOT_p1.json: package BOT_003_p1 of batch 3 (Botany, 122 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis, Respiration in
Plants. IDs NEET_BOT_000501 .. NEET_BOT_000622.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_003/BOT_003_p1.py
"""

import json
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
PLAN = ROOT / "batches" / "plans" / "BATCH_003_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_003_BOT_p1.json"
PACKAGE = "BOT_003_p1"
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
direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "The phylum Chordata of animals is characterised by the presence of:",
       "a notochord and a dorsal hollow neural system",
       ["a cell wall made of chitin", "jointed appendages and an exoskeleton", "red blood in all members"], "B",
       "Characters of the phylum Chordata",
       "NCERT gives the phylum Chordata as an example of a taxonomic category: it includes animals that possess a "
       "notochord and a dorsal hollow neural system.",
       ["Phylum Chordata: notochord + dorsal hollow neural system"],
       why="A chitinous wall is a feature of fungi, not animals. Jointed appendages are not the defining feature "
           "named for Chordata. Red blood was Aristotle's basis for dividing animals, not the feature of Chordata.",
       ncert=ref("LW", "Taxonomic Categories (Phylum)"), secs=25)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "NCERT cites which fungus as an important example of a fungus that causes wheat rust?",
       "Puccinia", ["Penicillium", "Albugo", "Trichoderma"], "C",
       "Fungi as plant pathogens",
       "Some fungi cause diseases in plants and animals; the wheat rust-causing Puccinia is an important example.",
       ["Wheat rust → Puccinia"],
       why="Penicillium is a source of antibiotics. Albugo is a phycomycete parasite on mustard. Trichoderma is a "
           "deuteromycete.",
       ncert=ref("BC", "Kingdom Fungi"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Diatoms have left large amounts of cell wall deposits in their habitat over billions of years. This gritty "
       "accumulation, used in polishing and in the filtration of oils and syrups, is called:",
       "diatomaceous earth", ["pellicle", "plasmodium", "peat"], "D",
       "Diatomaceous earth",
       "Diatom cell walls are embedded with silica and are indestructible. Their deposits, accumulated over billions "
       "of years, form diatomaceous earth. Being gritty, it is used in polishing and in filtration of oils and "
       "syrups.",
       ["Silica walls of diatoms accumulate → diatomaceous earth → polishing, filtration of oils and syrups"],
       why="The pellicle is the protein-rich layer of euglenoids. A plasmodium is the aggregation formed by slime "
           "moulds. Peat is obtained from the moss Sphagnum.",
       ncert=ref("BC", "Kingdom Protista (Chrysophytes)"), secs=25)

direct(T_LIV, "What is living", "Basic",
       "In which organism does NCERT describe true regeneration, in which a fragmented organism regenerates the lost "
       "part of its body and becomes a new organism?",
       "Planaria", ["Yeast", "Hydra", "Mule"], "A",
       "Regeneration as a mode of reproduction",
       "In Planaria (flat worms), true regeneration is seen: a fragmented organism regenerates the lost part of its "
       "body and becomes a new organism.",
       ["Yeast and Hydra: budding", "Planaria: true regeneration", "Mule: does not reproduce"],
       why="Yeast and Hydra reproduce by budding. A mule is sterile and does not reproduce at all.",
       ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=25)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Basic",
                 "Cyanobacteria (blue-green algae) are photosynthetic autotrophs.",
                 "Cyanobacteria have chlorophyll a similar to that of green plants.",
                 True, True, True, "A",
                 "Cyanobacteria",
                 "Cyanobacteria have chlorophyll a similar to green plants, and this pigment lets them carry out "
                 "photosynthesis, so they are photosynthetic autotrophs. R explains A.",
                 ["A: true", "R: true", "Chlorophyll a enables photosynthesis → R explains A"],
                 ncert=ref("BC", "Kingdom Monera (Eubacteria)"), secs=35)

statement_pair(T_LIV, "Five kingdom classification", "Intermediate",
               "Aristotle used simple morphological characters to classify plants into trees, shrubs and herbs.",
               "Aristotle divided animals into two groups on the basis of whether or not their cells had a cell wall.",
               True, False, "C",
               "Aristotle's classification",
               "Aristotle made the earliest attempt at a more scientific basis for classification. He classified plants "
               "into trees, shrubs and herbs using simple morphological characters, and divided animals into those "
               "which had red blood and those that did not.",
               ["Statement I: true", "Statement II: false, the basis was presence or absence of red blood"],
               ncert=ref("BC", "Introduction"), secs=35)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Slime moulds are saprophytic protists.",
                 "Under unfavourable conditions, the plasmodium of a slime mould differentiates and forms fruiting "
                 "bodies bearing spores at their tips.",
                 True, True, False, "B",
                 "Slime moulds",
                 "Slime moulds are saprophytic: the body moves along decaying twigs and leaves, engulfing organic "
                 "material. R is a true statement about their reproduction under unfavourable conditions; it says "
                 "nothing about their mode of nutrition, so it does not explain A.",
                 ["A: true (they feed on decaying organic material)", "R: true (spore formation)",
                  "R concerns reproduction, not nutrition → not the explanation"],
                 ncert=ref("BC", "Kingdom Protista (Slime moulds)"), secs=40)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate", "fungus", "use or feature",
           ["Penicillium", "Neurospora", "Yeast", "Rhizopus"],
           ["The bread mould", "Used extensively in biochemical and genetic work",
            "Source of antibiotics", "Unicellular fungus used to make bread and beer"],
           {"A": "III", "B": "II", "C": "IV", "D": "I"},
           [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
            {"A": "II", "B": "III", "C": "I", "D": "IV"}], "B",
           "Fungi of importance",
           "Penicillium is a source of antibiotics. Neurospora is used extensively in biochemical and genetic work. "
           "Yeast is a unicellular fungus used to make bread and beer. Rhizopus is the bread mould.",
           ["Penicillium → antibiotics (III)", "Neurospora → biochemical and genetic work (II)",
            "Yeast → bread and beer (IV)", "Rhizopus → bread mould (I)"],
           why="Do not confuse yeast (used to make bread) with Rhizopus (the bread mould that grows on bread).",
           ncert=ref("BC", "Kingdom Fungi"), secs=45)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about members of kingdom Protista are correct?",
                [("The cell walls of diatoms form two thin overlapping shells, which fit together as in a soap box.",
                  True),
                 ("Diatoms are the chief 'producers' in the oceans.", True),
                 ("Most chrysophytes are large, actively swimming organisms.", False),
                 ("Ciliated protozoans have a cavity (gullet) that opens to the outside of the cell surface.", True)],
                [("a", "b", "c"), ("b", "c", "d"), ("a", "d")], "C",
                "Chrysophytes and ciliated protozoans",
                "Diatom walls form two thin overlapping shells that fit together like a soap box, and diatoms are the "
                "chief producers in the oceans. Chrysophytes are microscopic and float passively in water currents "
                "(plankton). Ciliated protozoans have a gullet that opens to the outside; rows of cilia steer "
                "water laden with food into it.",
                ["(a) true", "(b) true", "(c) false: they are microscopic and float passively (plankton)",
                 "(d) true"],
                why="Any option containing (c) includes a false statement; (a) and (d) only leaves out the true "
                    "statement (b).",
                ncert=ref("BC", "Kingdom Protista"), secs=55)

direct(T_LIV, "Lichens, viruses and viroids", "Intermediate",
       "Which of the following is NOT one of the symptoms of viral infection in plants listed by NCERT?",
       "Formation of conidia on the leaf surface",
       ["Mosaic formation", "Leaf rolling and curling", "Yellowing and vein clearing"], "D",
       "Symptoms of viral diseases in plants",
       "Viruses cause plant symptoms such as mosaic formation, leaf rolling and curling, yellowing and vein "
       "clearing, dwarfing and stunted growth. Conidia are asexual spores of fungi, not a symptom of viral "
       "infection.",
       ["Viral symptoms: mosaic, leaf rolling/curling, yellowing, vein clearing, dwarfing, stunting",
        "Conidia → fungal spores"],
       why="Mosaic formation, leaf rolling and curling, and yellowing with vein clearing are all listed viral "
           "symptoms.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=30)

statement_pair(T_LIV, "Lichens, viruses and viroids", "Intermediate",
               "Viroids were discovered as the causal agents of tobacco mosaic disease.",
               "The RNA of a viroid is of high molecular weight.",
               False, False, "B",
               "Viroids",
               "T.O. Diener (1971) discovered the viroid as the agent causing potato spindle tuber disease. A viroid "
               "is a free RNA of low molecular weight.",
               ["Statement I: false, viroids were found to cause potato spindle tuber disease",
                "Statement II: false, viroid RNA is of low molecular weight"],
               ncert=ref("BC", "Viruses, Viroids, Prions and Lichens (Viroids)"), secs=35)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate", "group of protists", "feature",
           ["Chrysophytes", "Dinoflagellates", "Euglenoids", "Slime moulds"],
           ["Stiff cellulose plates on the outer surface of the cell wall",
            "A protein-rich layer called the pellicle, which makes the body flexible",
            "An aggregation called a plasmodium, which may grow and spread over several feet",
            "Include diatoms and golden algae (desmids)"],
           {"A": "IV", "B": "I", "C": "II", "D": "III"},
           [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
            {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C",
           "Groups of Protista",
           "Chrysophytes include diatoms and golden algae (desmids). Dinoflagellates have stiff cellulose plates on "
           "the outer surface of the cell wall. Euglenoids have no cell wall; a protein-rich pellicle makes their "
           "body flexible. Slime moulds form a plasmodium that may spread over several feet.",
           ["Chrysophytes → IV", "Dinoflagellates → I", "Euglenoids → II", "Slime moulds → III"],
           ncert=ref("BC", "Kingdom Protista"), secs=45)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Advanced",
                "Which of the following statements about fungi are correct?",
                [("Fungi prefer to grow in warm and humid places.", True),
                 ("In some fungi, the hyphae are continuous tubes filled with multinucleated cytoplasm; these are "
                  "called coenocytic hyphae.", True),
                 ("In phycomycetes, the asexual spores are produced exogenously on special mycelium called "
                  "conidiophores.", False),
                 ("Morels and truffles are edible ascomycetes and are considered delicacies.", True),
                 ("Asexual spores are commonly produced by members of basidiomycetes.", False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")], "A",
                "General features and classes of fungi",
                "Fungi prefer warm, humid places. Coenocytic hyphae are continuous tubes with multinucleate "
                "cytoplasm. In phycomycetes, asexual spores (zoospores or aplanospores) are produced endogenously in "
                "a sporangium; conidia formed exogenously on conidiophores belong to ascomycetes. Morels and truffles "
                "are edible ascomycetes. In basidiomycetes, asexual spores are generally not found.",
                ["(a) true", "(b) true", "(c) false: phycomycete spores are endogenous, in sporangia",
                 "(d) true", "(e) false: asexual spores are generally not found in basidiomycetes"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("BC", "Kingdom Fungi"), secs=70)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Advanced",
               "In basidiomycetes, plasmogamy takes place by the fusion of two vegetative or somatic cells of "
               "different strains or genotypes.",
               "In basidiomycetes, karyogamy and meiosis take place in the basidium, producing four basidiospores.",
               True, True, "A",
               "Sexual reproduction in basidiomycetes",
               "Sex organs are absent in basidiomycetes, but plasmogamy occurs by fusion of two vegetative or somatic "
               "cells of different strains. The resulting dikaryon gives rise to the basidium, in which karyogamy "
               "and meiosis take place to produce four basidiospores.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("BC", "Kingdom Fungi (Basidiomycetes)"), secs=40)

assertion_reason(T_LIV, "Five kingdom classification", "Advanced",
                 "Chlamydomonas and Chlorella, placed among the algae within plants in the two kingdom system, are "
                 "placed in kingdom Protista in the five kingdom system.",
                 "Chlamydomonas and Chlorella lack a cell wall.",
                 True, False, False, "C",
                 "Regrouping of organisms in the five kingdom system",
                 "The five kingdom system brought together Chlamydomonas and Chlorella (earlier placed in algae within "
                 "plants) with Paramoecium and Amoeba (earlier placed in the animal kingdom) in Protista. NCERT notes "
                 "that Chlamydomonas and Chlorella have cell walls, whereas Paramoecium and Amoeba lack them, so R is "
                 "false.",
                 ["A: true", "R: false, both have cell walls"],
                 ncert=ref("BC", "Introduction (five kingdom classification)"), secs=45)

match_list(T_LIV, "Five kingdom classification", "Advanced", "organism", "kingdom in Whittaker's system",
           ["Nostoc", "Paramoecium", "Yeast", "Cuscuta"],
           ["Fungi", "Plantae", "Monera", "Protista"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "III", "B": "II", "C": "I", "D": "IV"}], "D",
           "Placing organisms in the five kingdoms",
           "Nostoc is a cyanobacterium (Monera). Paramoecium, earlier placed among animals, is a protist. Yeast is a "
           "unicellular fungus. Cuscuta is a parasite, yet it is a member of Plantae, which also includes a few "
           "partially heterotrophic members.",
           ["Nostoc → Monera (III)", "Paramoecium → Protista (IV)", "Yeast → Fungi (I)",
            "Cuscuta → Plantae (II)"],
           why="Being unicellular does not make yeast a protist, and being parasitic does not remove Cuscuta from "
               "Plantae.",
           ncert=ref("BC", "Kingdom Monera; Kingdom Protista; Kingdom Fungi; Kingdom Plantae"), secs=50)

multi_statement(T_LIV, "What is living", "Advanced",
                "Which of the following statements about living organisms are correct?",
                [("Living organisms grow from inside, whereas non-living objects such as mountains and sand mounds "
                  "grow by accumulation of material on their surface.", True),
                 ("Growth is a defining property of living organisms, without any exception.", False),
                 ("Fungi, filamentous algae and the protonema of mosses easily multiply by fragmentation.", True),
                 ("The number of species that are known and described ranges between 1.7 and 1.8 million.", True),
                 ("All organisms, from prokaryotes to the most complex eukaryotes, can sense and respond to "
                  "environmental cues.", True)],
                [("a", "b", "c", "d"), ("c", "d", "e"), ("a", "b", "e")], "B",
                "Characteristics of living organisms",
                "Growth in living organisms is from inside, unlike the surface accumulation by which mountains and "
                "sand mounds grow. Because non-living objects also grow in mass, growth cannot be taken as a defining "
                "property of living organisms. Fungi, filamentous algae and moss protonema multiply by fragmentation. "
                "About 1.7–1.8 million species are known and described. All organisms sense and respond to "
                "environmental cues.",
                ["(a) true", "(b) false: growth is not a defining property", "(c) true", "(d) true", "(e) true"],
                why="Options with (b) contain a false statement; (c), (d) and (e) only leaves out the true statement "
                    "(a).",
                ncert=ref("LW", "Diversity in the Living World"), secs=60)

# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "Green algae may have discoid, plate-like, reticulate, cup-shaped, spiral or ribbon-shaped chloroplasts. The "
       "major pigments localised in these chloroplasts are:",
       "chlorophyll a and b",
       ["chlorophyll a and c with fucoxanthin", "chlorophyll a and d with phycoerythrin",
        "phycoerythrin and floridean starch"], "A",
       "Pigments of Chlorophyceae",
       "Members of Chlorophyceae are grass green because chlorophyll a and b dominate; these pigments are localised "
       "in definite chloroplasts of varied shapes.",
       ["Chlorophyceae: chlorophyll a, b", "Phaeophyceae: chlorophyll a, c, fucoxanthin",
        "Rhodophyceae: chlorophyll a, d, phycoerythrin"],
       why="Chlorophyll a and c with fucoxanthin is the brown-algal set; chlorophyll a and d with phycoerythrin is the "
           "red-algal set; floridean starch is a stored food, not a pigment.",
       ncert=ref("PK", "Algae (Chlorophyceae)"), secs=25)

direct(T_PK, "Bryophytes", "Basic",
       "Mosses, along with lichens, are the first organisms to colonise:",
       "rocks", ["fresh-water ponds", "the deep sea floor", "tree canopies in rain forests"], "C",
       "Ecological importance of mosses",
       "Mosses, along with lichens, are the first organisms to colonise rocks and are therefore of great ecological "
       "importance. They decompose rocks, making the substrate suitable for the growth of higher plants.",
       ["Pioneers on rocks: lichens and mosses"],
       why="The other habitats are not the ones NCERT names for these pioneer organisms.",
       ncert=ref("PK", "Bryophytes"), secs=20)

direct(T_PK, "Pteridophytes", "Basic",
       "Horsetails and ferns belong to the group:",
       "Pteridophyta", ["Bryophyta", "Gymnospermae", "Phaeophyceae"], "B",
       "Members of pteridophytes",
       "The pteridophytes include horsetails and ferns. They are used for medicinal purposes and as soil-binders, "
       "and many are grown as ornamentals.",
       ["Horsetails (Equisetum) and ferns → pteridophytes"],
       why="Bryophytes are liverworts and mosses; gymnosperms bear naked seeds; Phaeophyceae are brown algae.",
       ncert=ref("PK", "Pteridophytes"), secs=20)

direct(T_PK, "Gymnosperms", "Basic",
       "In Cycas, the pinnate leaves:",
       "persist for a few years",
       ["are shed within a few weeks", "are reduced to scales without chlorophyll",
        "are produced only on underground stems"], "D",
       "Leaves of gymnosperms",
       "Gymnosperm leaves may be simple or compound. In Cycas, the pinnate leaves persist for a few years.",
       ["Cycas: pinnate leaves that persist for a few years"],
       why="None of the other descriptions is given for Cycas leaves; its stem is unbranched and aerial, bearing a "
           "crown of pinnate leaves.",
       ncert=ref("PK", "Gymnosperms"), secs=20)

match_list(T_PK, "Algae", "Basic", "plant", "group",
           ["Polysiphonia", "Chara", "Ectocarpus", "Polytrichum"],
           ["Red alga", "Brown alga", "Green alga", "Moss"],
           {"A": "I", "B": "III", "C": "II", "D": "IV"},
           [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "I", "B": "II", "C": "III", "D": "IV"},
            {"A": "III", "B": "I", "C": "II", "D": "IV"}], "A",
           "Examples of plant groups",
           "Polysiphonia is a red alga (Rhodophyceae), Chara a green alga (Chlorophyceae), Ectocarpus a brown alga "
           "(Phaeophyceae) and Polytrichum a moss.",
           ["Polysiphonia → I", "Chara → III", "Ectocarpus → II", "Polytrichum → IV"],
           ncert=ref("PK", "Algae; Bryophytes"), secs=35)

statement_pair(T_PK, "Algae", "Intermediate",
               "The majority of red algae are marine, with greater concentrations found in the warmer areas.",
               "Floridean starch, the stored food of red algae, is very similar to amylopectin and glycogen in "
               "structure.",
               True, True, "A",
               "Rhodophyceae",
               "Most red algae are marine, with greater concentrations in warmer areas. Their food is stored as "
               "floridean starch, which is very similar to amylopectin and glycogen in structure.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Algae (Rhodophyceae)"), secs=35)

assertion_reason(T_PK, "Bryophytes", "Intermediate",
                 "Mosses play an important role in preventing soil erosion.",
                 "Mosses form dense mats on the soil, which reduce the impact of falling rain.",
                 True, True, True, "A",
                 "Mosses and soil erosion",
                 "Since mosses form dense mats on the soil, they reduce the impact of falling rain and so prevent soil "
                 "erosion. R gives the reason for A.",
                 ["A: true", "R: true", "Dense mats soften the impact of rain → less erosion → R explains A"],
                 ncert=ref("PK", "Bryophytes"), secs=35)

multi_statement(T_PK, "Gymnosperms", "Intermediate",
                "Which of the following statements about gymnosperms are correct?",
                [("Their leaves are well adapted to withstand extremes of temperature, humidity and wind.", True),
                 ("The pollen grains develop within the microsporangia.", True),
                 ("The megaspore mother cell divides mitotically to form four megaspores.", False),
                 ("The pollen tube carrying the male gametes grows towards the archegonia in the ovules.", True),
                 ("The multicellular female gametophyte is shed from the megasporangium before fertilisation.",
                  False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "d")], "B",
                "Reproduction in gymnosperms",
                "Gymnosperm leaves withstand extremes of temperature, humidity and wind. Microspores develop into "
                "reduced male gametophytes, the pollen grains, within the microsporangia. The megaspore mother cell "
                "divides meiotically to form four megaspores. The female gametophyte is retained within the "
                "megasporangium, and the pollen tube carries the male gametes towards its archegonia.",
                ["(a) true", "(b) true", "(c) false: the division is meiotic", "(d) true",
                 "(e) false: the female gametophyte is retained within the megasporangium"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("PK", "Gymnosperms"), secs=60)

statement_pair(T_PK, "Pteridophytes", "Intermediate",
               "Pteridophytes are found in cool, damp, shady places, and none of them can grow in sandy soil.",
               "The leaves of all pteridophytes are large macrophylls.",
               False, False, "B",
               "Habitat and leaves of pteridophytes",
               "Pteridophytes are found in cool, damp, shady places, though some may flourish well in sandy-soil "
               "conditions. Their leaves are small (microphylls, as in Selaginella) or large (macrophylls, as in "
               "ferns).",
               ["Statement I: false, some flourish in sandy soil",
                "Statement II: false, some have microphylls"],
               ncert=ref("PK", "Pteridophytes"), secs=35)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Members of Rhodophyceae owe their red colour to the pigment fucoxanthin.",
                 "Members of Rhodophyceae have a predominance of the red pigment r-phycoerythrin in their body.",
                 False, True, False, "D",
                 "Colour of red algae",
                 "Red algae are red because of the predominance of r-phycoerythrin. Fucoxanthin is the pigment whose "
                 "amount decides the colour of brown algae, so A is false.",
                 ["A: false, fucoxanthin is the brown-algal pigment", "R: true"],
                 ncert=ref("PK", "Algae (Rhodophyceae)"), secs=35)

direct(T_PK, "Bryophytes", "Intermediate",
       "In leafy liverworts, the tiny leaf-like appendages are:",
       "arranged in two rows on the stem-like structures",
       ["arranged spirally on upright, slender axes", "borne in whorls at each node",
        "borne as a rosette on a creeping protonema"], "C",
       "Plant body of liverworts",
       "The thallus of liverworts such as Marchantia is dorsiventral and closely appressed to the substrate. The "
       "leafy members have tiny leaf-like appendages in two rows on the stem-like structures.",
       ["Leafy liverworts: two rows of leaf-like appendages", "Mosses: spirally arranged leaves on upright axes"],
       why="Spirally arranged leaves on upright, slender axes describe the leafy stage of mosses. Whorls and a "
           "rosette on a protonema are not described for liverworts.",
       ncert=ref("PK", "Bryophytes (Liverworts)"), secs=30)

match_list(T_PK, "Gymnosperms", "Intermediate", "structure in a gymnosperm", "description",
           ["Microsporophyll", "Megasporophyll", "Archegonium", "Pollen grain"],
           ["Represents the highly reduced male gametophyte", "Bears the microsporangia", "Bears the ovules",
            "Two or more of these are borne by the multicellular female gametophyte"],
           {"A": "II", "B": "III", "C": "IV", "D": "I"},
           [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
            {"A": "IV", "B": "III", "C": "II", "D": "I"}], "B",
           "Reproductive structures of gymnosperms",
           "Microsporophylls bear microsporangia, in which the microspores develop into the reduced male "
           "gametophyte, the pollen grain. Ovules are borne on megasporophylls. The female gametophyte, retained "
           "inside the megasporangium, bears two or more archegonia.",
           ["Microsporophyll → II", "Megasporophyll → III", "Archegonium → IV", "Pollen grain → I"],
           ncert=ref("PK", "Gymnosperms"), secs=45)

match_list(T_PK, "Algae", "Advanced", "plant group", "feature",
           ["Chlorophyceae", "Phaeophyceae", "Rhodophyceae", "Mosses"],
           ["Cell wall of cellulose, pectin and polysulphate esters",
            "Rigid cell wall with an inner layer of cellulose and an outer layer of pectose",
            "Cellulosic cell wall usually covered on the outside by a gelatinous coating of algin",
            "Multicellular, branched rhizoids"],
           {"A": "II", "B": "III", "C": "I", "D": "IV"},
           [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "I", "B": "III", "C": "II", "D": "IV"},
            {"A": "II", "B": "I", "C": "III", "D": "IV"}], "D",
           "Cell walls of algae",
           "Green algae have a rigid wall with an inner cellulose layer and an outer pectose layer. Brown algae have "
           "a cellulosic wall usually covered on the outside by algin. Red algae have walls of cellulose, pectin and "
           "polysulphate esters. Mosses are attached to the substratum by multicellular, branched rhizoids.",
           ["Chlorophyceae → II", "Phaeophyceae → III", "Rhodophyceae → I", "Mosses → IV"],
           why="Algin belongs with brown algae and polysulphate esters with red algae; the options that swap them are "
               "wrong.",
           ncert=ref("PK", "Algae (Table: Divisions of Algae and their main characteristics); Bryophytes"), secs=50)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following statements about reproduction in algae are correct?",
                [("In Ulothrix, fusion takes place between flagellated gametes that are similar in size.", True),
                 ("The gametes of brown algae are pyriform (pear-shaped) and bear two laterally attached flagella.",
                  True),
                 ("In red algae, sexual reproduction is oogamous and is accompanied by complex post-fertilisation "
                  "developments.", True),
                 ("In red algae, asexual reproduction takes place by motile zoospores.", False),
                 ("In brown algae, the union of gametes may take place in water or within the oogonium.", True)],
                [("a", "b", "c"), ("b", "c", "d", "e"), ("a", "c", "d", "e")], "C",
                "Reproduction in algae",
                "Ulothrix is isogamous with flagellated gametes. Brown-algal gametes are pear-shaped with two laterally "
                "attached flagella, and they unite in water or within the oogonium. Red algae reproduce asexually by "
                "non-motile spores and sexually by non-motile gametes; sexual reproduction is oogamous with complex "
                "post-fertilisation developments.",
                ["(a) true", "(b) true", "(c) true", "(d) false: red algae form non-motile spores", "(e) true"],
                why="Options with (d) contain a false statement; (a), (b) and (c) only leaves out the true statement "
                    "(e).",
                ncert=ref("PK", "Algae"), secs=65)

statement_pair(T_PK, "Bryophytes", "Advanced",
               "In liverworts, the male and female sex organs are always produced on different thalli.",
               "In liverworts, the sporophyte is differentiated into a foot, seta and capsule, and spores are "
               "produced within the capsule after meiosis.",
               False, True, "D",
               "Sexual reproduction in liverworts",
               "In liverworts, the male and female sex organs are produced either on the same or on different thalli. "
               "The sporophyte has a foot, seta and capsule, and spores are produced in the capsule after meiosis.",
               ["Statement I: false, they may be on the same or different thalli", "Statement II: true"],
               ncert=ref("PK", "Bryophytes (Liverworts)"), secs=40)

assertion_reason(T_PK, "Bryophytes", "Advanced",
                 "Sphagnum provides peat that has long been used as fuel.",
                 "Sphagnum is a liverwort.",
                 True, False, False, "C",
                 "Economic importance of Sphagnum",
                 "Some mosses like Sphagnum provide peat that has long been used as fuel. Sphagnum is a moss, like "
                 "Funaria and Polytrichum, not a liverwort, so R is false.",
                 ["A: true", "R: false, Sphagnum is a moss"],
                 ncert=ref("PK", "Bryophytes"), secs=35)

multi_statement(T_PK, "Bryophytes", "Advanced",
                "Which of the following statements about bryophytes are correct?",
                [("They lack true roots, stem or leaves, though they may possess root-like, leaf-like or stem-like "
                  "structures.", True),
                 ("Some mosses provide food for herbaceous mammals and birds.", True),
                 ("Liverworts grow in moist, shady habitats such as banks of streams, marshy ground, damp soil and "
                  "the bark of trees.", True),
                 ("The thallus of Marchantia is erect and radially symmetrical.", False),
                 ("The zygote develops into a multicellular body called the sporophyte.", True)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d", "e")], "D",
                "General features of bryophytes",
                "Bryophytes lack true roots, stems and leaves. Some mosses are food for herbaceous mammals and birds. "
                "Liverworts grow in moist, shady habitats. The thallus of Marchantia is dorsiventral and closely "
                "appressed to the substrate. The zygote develops into a multicellular sporophyte.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the thallus is dorsiventral and appressed",
                 "(e) true"],
                why="Options with (d) contain a false statement; (a), (c) and (e) only leaves out the true statement "
                    "(b).",
                ncert=ref("PK", "Bryophytes"), secs=60)

# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Root, stem and leaf", "Basic",
       "Which region of the root is responsible for the growth of the root in length?",
       "Region of elongation",
       ["Root cap", "Region of maturation", "Region of meristematic activity"], "C",
       "Regions of the root",
       "The cells just proximal to the region of meristematic activity undergo rapid elongation and enlargement and "
       "are responsible for the growth of the root in length; this is the region of elongation.",
       ["Root cap: protects the apex", "Meristematic region: small, dividing cells",
        "Elongation region: rapid elongation → growth in length", "Maturation region: differentiation, root hairs"],
       why="The root cap protects the root apex. The meristematic region produces new cells but NCERT attributes "
           "growth in length to the region of elongation. Root hairs arise in the region of maturation.",
       ncert=ref("MOR", "The Root (Regions of the root)"), secs=25)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "Long, thin, flexible petioles allow leaf blades to flutter in the wind. This:",
       "cools the leaf and brings fresh air to the leaf surface",
       ["stores reserve food in the petiole", "helps the plant climb a support", "protects the axillary bud from "
        "grazing animals"], "A",
       "Role of the petiole",
       "The petiole helps hold the blade to light. Long, thin, flexible petioles allow leaf blades to flutter in the "
       "wind, thereby cooling the leaf and bringing fresh air to the leaf surface.",
       ["Fluttering blade → cooling + fresh air at the leaf surface"],
       why="None of the other functions is attributed to fluttering petioles.",
       ncert=ref("MOR", "The Leaf"), secs=25)

direct(T_MOR, "Flower", "Basic",
       "A flower that can be divided into two similar halves only in one particular vertical plane is described as:",
       "zygomorphic", ["actinomorphic", "asymmetric", "radially symmetrical"], "D",
       "Symmetry of flowers",
       "When a flower can be divided into two equal radial halves in any radial plane through the centre, it is "
       "actinomorphic (radial symmetry). When it can be divided into two similar halves only in one particular "
       "vertical plane, it is zygomorphic (bilateral symmetry). A flower that cannot be divided into similar halves "
       "by any vertical plane is asymmetric.",
       ["One plane only → zygomorphic (e.g. pea, gulmohur, bean, Cassia)"],
       why="Actinomorphic (radially symmetrical) flowers can be halved in any radial plane; asymmetric flowers cannot "
           "be halved in any plane.",
       ncert=ref("MOR", "The Flower"), secs=20)

direct(T_MOR, "Fruit and seed", "Basic",
       "A fruit formed without fertilisation of the ovary is called a:",
       "parthenocarpic fruit", ["drupe", "legume", "berry"], "B",
       "Parthenocarpic fruit",
       "The fruit is a mature or ripened ovary developed after fertilisation. If a fruit is formed without "
       "fertilisation of the ovary, it is called a parthenocarpic fruit.",
       ["No fertilisation → parthenocarpic fruit"],
       why="Drupe, legume and berry are fruit types named for their structure, not for fruit formation without "
           "fertilisation.",
       ncert=ref("MOR", "The Fruit"), secs=20)

direct(T_MOR, "Plant families", "Basic",
       "Which pair of plants of the family Fabaceae is a source of edible oil?",
       "Soyabean and groundnut",
       ["Sesbania and Trifolium", "Lupin and sweet pea", "Indigofera and sunhemp"], "C",
       "Economic importance of Fabaceae",
       "Many Fabaceae plants are sources of pulses, and soyabean and groundnut are sources of edible oil. Sesbania "
       "and Trifolium give fodder, lupin and sweet pea are ornamentals, Indigofera gives a dye and sunhemp gives "
       "fibre.",
       ["Edible oil: soyabean, groundnut"],
       why="Sesbania and Trifolium are fodder plants; lupin and sweet pea are ornamentals; Indigofera is a dye and "
           "sunhemp a fibre plant.",
       ncert=ref("MOR", "Description of Some Important Families (Fabaceae: economic importance)"), secs=25)

statement_pair(T_MOR, "Flower", "Intermediate",
               "In flowers such as Salvia and mustard, the stamens of the same flower vary in the length of their "
               "filaments.",
               "In lotus and rose, the carpels of the gynoecium are free (apocarpous).",
               True, True, "A",
               "Androecium and gynoecium",
               "Stamens of a flower may vary in filament length, as in Salvia and mustard. When the carpels are free, "
               "as in lotus and rose, the gynoecium is apocarpous; when fused, as in mustard and tomato, it is "
               "syncarpous.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Flower (Androecium; Gynoecium)"), secs=35)

assertion_reason(T_MOR, "Root, stem and leaf", "Intermediate",
                 "In a compound leaf, a bud is present in the axil of each leaflet.",
                 "In both simple and compound leaves, a bud is present in the axil of the petiole.",
                 False, True, False, "D",
                 "Simple and compound leaves",
                 "A bud is present in the axil of the petiole in both simple and compound leaves, but not in the axil "
                 "of the leaflets of a compound leaf. This is how a compound leaf is told apart from a branch bearing "
                 "leaves.",
                 ["A: false, leaflets have no axillary buds", "R: true"],
                 ncert=ref("MOR", "The Leaf (Types of leaves)"), secs=35)

match_list(T_MOR, "Flower", "Intermediate", "term", "meaning",
           ["Bracteate", "Trimerous", "Staminode", "Polyandrous"],
           ["Floral appendages in multiples of three", "A sterile stamen", "Stamens free from one another",
            "Flowers with a reduced leaf found at the base of the pedicel"],
           {"A": "IV", "B": "I", "C": "II", "D": "III"},
           [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "IV", "B": "I", "C": "III", "D": "II"},
            {"A": "II", "B": "I", "C": "IV", "D": "III"}], "A",
           "Floral terms",
           "Flowers with bracts (reduced leaves at the base of the pedicel) are bracteate. A trimerous flower has its "
           "floral appendages in multiples of three. A sterile stamen is a staminode. Stamens that are free are "
           "called polyandrous.",
           ["Bracteate → IV", "Trimerous → I", "Staminode → II", "Polyandrous → III"],
           ncert=ref("MOR", "The Flower"), secs=40)

multi_statement(T_MOR, "Fruit and seed", "Intermediate",
                "Which of the following statements about seeds are correct?",
                [("In castor, the endosperm formed as a result of double fertilisation is a food-storing tissue.",
                  True),
                 ("In cereals such as maize, the endosperm is bulky and stores food.", True),
                 ("In cereals, the seed coat is membranous and generally fused with the fruit wall.", True),
                 ("The cotyledons of a dicotyledonous seed are thin and papery and contain no reserve food.", False)],
                [("a", "c", "d"), ("b", "c", "d"), ("a", "b")], "B",
                "Structure of seeds",
                "In castor, the endosperm formed by double fertilisation stores food. In cereals such as maize, the "
                "seed coat is membranous and fused with the fruit wall, and the endosperm is bulky and stores food. "
                "In dicot seeds, the cotyledons are often fleshy and full of reserve food.",
                ["(a) true", "(b) true", "(c) true", "(d) false: cotyledons are often fleshy, with reserve food"],
                why="Options with (d) contain a false statement; (a) and (b) only leaves out the true statement (c).",
                ncert=ref("MOR", "The Seed (Structure of a dicotyledonous seed; Structure of a monocotyledonous "
                                 "seed)"), secs=50)

statement_pair(T_MOR, "Root, stem and leaf", "Intermediate",
               "In a simple leaf, the incisions of the lamina, if any, do not touch the midrib.",
               "The leaves of the pitcher plant and Venus fly trap are modified to store water.",
               True, False, "C",
               "Types and modifications of leaves",
               "A leaf is simple when its lamina is entire or, when incised, the incisions do not touch the midrib. "
               "The leaves of insectivorous plants such as the pitcher plant and Venus fly trap are modified to trap "
               "insects, not to store water.",
               ["Statement I: true", "Statement II: false, they are modified leaves of insectivorous plants"],
               ncert=ref("MOR", "The Leaf (Types of leaves; Modifications of leaves)"), secs=35)

assertion_reason(T_MOR, "Plant families", "Intermediate",
                 "The family Fabaceae was earlier called Papilionoideae, a subfamily of the family Leguminosae.",
                 "Plants of the family Fabaceae have roots with root nodules.",
                 True, True, False, "B",
                 "Fabaceae",
                 "Both statements are true. A is about the history of the family's name, while R is a vegetative "
                 "character of its members; root nodules do not explain why the family was once called "
                 "Papilionoideae.",
                 ["A: true", "R: true", "R is an unrelated character → not the explanation"],
                 ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=35)

match_list(T_MOR, "Plant families", "Intermediate", "plant of Liliaceae", "use",
           ["Tulip", "Aloe", "Asparagus", "Colchicum autumnale"],
           ["Vegetable", "Source of colchicine", "Ornamental", "Medicine"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "I", "B": "IV", "C": "III", "D": "II"}], "D",
           "Economic importance of Liliaceae",
           "Many Liliaceae plants are ornamentals (tulip, Gloriosa), sources of medicine (Aloe) and vegetables "
           "(Asparagus); colchicine is obtained from Colchicum autumnale.",
           ["Tulip → ornamental (III)", "Aloe → medicine (IV)", "Asparagus → vegetable (I)",
            "Colchicum autumnale → colchicine (II)"],
           ncert=ref("MOR", "Description of Some Important Families (Liliaceae: economic importance)"), secs=40)

multi_statement(T_MOR, "Flower", "Advanced",
                "Which of the following statements about flowers are correct?",
                [("In vexillary aestivation, the largest petal (standard) overlaps the two lateral petals (wings), "
                  "which in turn overlap the two smallest anterior petals (keel).", True),
                 ("Vexillary aestivation is found in pea and bean flowers.", True),
                 ("The ray florets of sunflower are epigynous.", True),
                 ("Each anther lobe usually has four chambers, the pollen sacs.", False),
                 ("Lemon shows parietal placentation.", False)],
                [("a", "b", "c", "d"), ("b", "c", "e"), ("a", "c", "d")], "A",
                "Aestivation, androecium and placentation",
                "In pea and bean, the standard overlaps the wings, which overlap the keel: vexillary (papilionaceous) "
                "aestivation. The ray florets of sunflower are epigynous. A typical anther is bilobed, and each lobe "
                "has two chambers (pollen sacs). Lemon, like china rose and tomato, has axile placentation.",
                ["(a) true", "(b) true", "(c) true", "(d) false: each lobe has two chambers",
                 "(e) false: lemon has axile placentation"],
                why="Options with (d) or (e) contain a false statement.",
                ncert=ref("MOR", "The Flower"), secs=65)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements about the symbols used in a floral formula are correct?",
                [("Br stands for bracteate.", True),
                 ("⊕ indicates an actinomorphic flower and % a zygomorphic flower.", True),
                 ("A superior ovary is indicated by a line drawn above the symbol G.", False),
                 ("Fusion of parts is indicated by enclosing the figure within brackets.", True),
                 ("Adhesion is indicated by a line drawn above the symbols of the floral parts.", True)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")], "D",
                "Semi-technical description of a flowering plant",
                "In a floral formula, Br stands for bracteate, K for calyx, C for corolla, P for perianth, A for "
                "androecium and G for gynoecium. G with a line below it shows a superior ovary and G with a line above "
                "it an inferior ovary. ⊕ shows an actinomorphic flower and % a zygomorphic one. Fusion is shown by "
                "brackets and adhesion by a line drawn above the symbols of the floral parts.",
                ["(a) true", "(b) true", "(c) false: a line above G means an inferior ovary", "(d) true",
                 "(e) true"],
                why="Options with (c) contain a false statement; (b), (d) and (e) only leaves out the true statement "
                    "(a).",
                ncert=ref("MOR", "Semi-technical Description of a Typical Flowering Plant"), secs=60)

match_list(T_MOR, "Plant families", "Advanced", "plant", "family and use",
           ["Lupin", "Petunia", "Trifolium", "Tobacco"],
           ["Fodder plant of Fabaceae", "Fumigatory of Solanaceae", "Ornamental of Fabaceae",
            "Ornamental of Solanaceae"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C",
           "Economic importance of Fabaceae and Solanaceae",
           "Lupin and sweet pea are ornamental Fabaceae; Sesbania and Trifolium are Fabaceae fodder plants. Petunia "
           "is an ornamental of Solanaceae and tobacco is its fumigatory.",
           ["Lupin → ornamental, Fabaceae (III)", "Petunia → ornamental, Solanaceae (IV)",
            "Trifolium → fodder, Fabaceae (I)", "Tobacco → fumigatory, Solanaceae (II)"],
           why="Each row needs both the family and the use; lupin and petunia are both ornamentals, but from different "
               "families.",
           ncert=ref("MOR", "Description of Some Important Families (Fabaceae; Solanaceae)"), secs=50)

assertion_reason(T_MOR, "Plant families", "Advanced",
                 "In the family Solanaceae, the stem is always woody.",
                 "In potato (Solanum tuberosum), a member of Solanaceae, the stem is underground.",
                 False, True, False, "D",
                 "Vegetative characters of Solanaceae",
                 "Solanaceae plants are mostly herbs and shrubs; the stem is herbaceous, rarely woody, and in potato "
                 "it is underground. So A is false and R is true.",
                 ["A: false, the stem is herbaceous, rarely woody", "R: true"],
                 ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=35)

statement_pair(T_MOR, "Root, stem and leaf", "Advanced",
               "Colocasia stores food in swollen roots.",
               "Carrot stores food in a swollen tap root.",
               False, True, "D",
               "Storage organs",
               "The underground stems of potato, ginger, turmeric, zaminkand and Colocasia are modified to store food. "
               "The tap roots of carrot and turnip, and the adventitious roots of sweet potato, get swollen and store "
               "food.",
               ["Statement I: false, Colocasia stores food in an underground stem", "Statement II: true"],
               ncert=ref("MOR", "The Root (Modifications of root); The Stem (Modifications of stem)"), secs=40)

# =============================================================== 4. Anatomy of Flowering Plants (4/6/4)
direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "The innermost layer of the cortex in a dicot root is the:",
       "endodermis", ["pericycle", "epiblema", "hypodermis"], "B",
       "Layers of the dicot root",
       "In a dicot root, the cortex consists of several layers of thin-walled parenchyma cells, and its innermost "
       "layer is the endodermis. The pericycle lies next to the endodermis, on its inner side.",
       ["Epiblema → cortex → endodermis (innermost cortex) → pericycle → vascular tissue"],
       why="The pericycle lies inside the endodermis and is not part of the cortex. The epiblema is the outermost "
           "layer. Hypodermis is described for stems, below the epidermis.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous root)"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "Phloem fibres are also called:",
       "bast fibres", ["tracheids", "sclereids", "companion cells"], "D",
       "Phloem fibres",
       "Phloem fibres (bast fibres) are made up of sclerenchymatous cells. They are much elongated and unbranched, "
       "with pointed, needle-like apices.",
       ["Phloem fibres = bast fibres"],
       why="Tracheids are xylem elements, sclereids are short sclerenchyma cells, and companion cells are living "
           "parenchymatous cells of phloem.",
       ncert=ref("ANA", "The Tissues (Phloem)"), secs=20)

direct(T_ANA, "Tissue systems", "Basic",
       "In the conjoint vascular bundles of stems and leaves, the phloem is usually located:",
       "only on the outer side of the xylem",
       ["only on the inner side of the xylem", "on alternate radii with the xylem",
        "in the centre, surrounded by the xylem"], "C",
       "Conjoint vascular bundles",
       "In conjoint vascular bundles, xylem and phloem are jointly situated on the same radius. They are common in "
       "stems and leaves, and the phloem is usually located only on the outer side of the xylem.",
       ["Conjoint: same radius; phloem usually outside the xylem"],
       why="Xylem and phloem on alternate radii describes radial bundles of roots. The other positions are not "
           "described for conjoint bundles.",
       ncert=ref("ANA", "The Tissue System (Vascular tissue system)"), secs=25)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "Xylem and phloem together constitute the vascular bundles.",
               "All tissues on the inner side of the endodermis, such as the pericycle, vascular bundles and pith, "
               "constitute the stele.",
               True, True, "A",
               "Vascular bundles and stele",
               "The vascular system consists of complex tissues, phloem and xylem, which together form vascular "
               "bundles. All tissues on the inner side of the endodermis (pericycle, vascular bundles and pith) form "
               "the stele.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System; Anatomy of Dicotyledonous Root"), secs=30)

direct(T_ANA, "Plant tissues", "Intermediate",
       "Collenchyma provides mechanical support mainly to:",
       "growing parts of the plant, such as the young stem and the petiole of a leaf",
       ["the hard seed coats of legumes", "the fruit walls of nuts", "the dead, central wood of old tree trunks"],
       "A",
       "Collenchyma",
       "Collenchyma occurs in layers below the epidermis in dicotyledonous plants. Its cells are thickened at the "
       "corners with cellulose, hemicellulose and pectin, often contain chloroplasts, and provide mechanical support "
       "to growing parts such as the young stem and petiole of a leaf.",
       ["Collenchyma: living, corner-thickened → support to growing parts"],
       why="Seed coats of legumes and fruit walls of nuts are sites of sclereids. Old wood is not supported by "
           "collenchyma.",
       ncert=ref("ANA", "The Tissues (Collenchyma)"), secs=30)

assertion_reason(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                 "Except for the main veins, the vascular bundles of an isobilateral (monocot) leaf are of nearly "
                 "similar size.",
                 "Monocot leaves have parallel venation.",
                 True, True, True, "A",
                 "Isobilateral leaf",
                 "NCERT explains that the parallel venation in monocot leaves is reflected in the near similar sizes "
                 "of vascular bundles (except in main veins), whereas in dicot leaves the veins vary in thickness. R "
                 "explains A.",
                 ["A: true", "R: true", "Parallel venation → bundles of similar size → R explains A"],
                 ncert=ref("ANA", "Monocotyledonous (Isobilateral) Leaf"), secs=35)

match_list(T_ANA, "Dicot and monocot anatomy", "Intermediate", "part of a dicot stem", "description",
           ["Pericycle", "Medullary rays", "Pith", "Epidermis"],
           ["A few layers of radially placed parenchymatous cells between the vascular bundles",
            "Covered with a thin cuticle; may bear trichomes and a few stomata",
            "Semi-lunar patches of sclerenchyma above the phloem",
            "Rounded parenchymatous cells with large intercellular spaces in the central portion"],
           {"A": "III", "B": "I", "C": "IV", "D": "II"},
           [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
            {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C",
           "Internal structure of a dicot stem",
           "In a dicot stem the epidermis is covered with a thin cuticle and may bear trichomes and a few stomata. "
           "The pericycle lies on the inner side of the endodermis and above the phloem as semi-lunar patches of "
           "sclerenchyma. Radially placed parenchyma cells between bundles form medullary rays. The central pith has "
           "rounded parenchyma cells with large intercellular spaces.",
           ["Pericycle → III", "Medullary rays → I", "Pith → IV", "Epidermis → II"],
           ncert=ref("ANA", "Dicotyledonous Stem"), secs=45)

multi_statement(T_ANA, "Plant tissues", "Intermediate",
                "Which of the following statements about simple permanent tissues are correct?",
                [("Parenchyma cells may be spherical, oval, round, polygonal or elongated in shape.", True),
                 ("Collenchyma cells often contain chloroplasts.", True),
                 ("Intercellular spaces are absent in collenchyma.", True),
                 ("Sclereids have very wide cavities (lumen).", False),
                 ("Collenchyma is found in layers below the epidermis in monocotyledonous plants.", False)],
                [("a", "b", "c", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "A",
                "Parenchyma, collenchyma and sclerenchyma",
                "Parenchyma cells are generally isodiametric but may be spherical, oval, round, polygonal or "
                "elongated. Collenchyma cells often contain chloroplasts and have no intercellular spaces; the tissue "
                "lies below the epidermis in dicotyledonous plants. Sclereids are highly thickened dead cells with "
                "very narrow cavities.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the lumen is very narrow",
                 "(e) false: collenchyma is described below the epidermis in dicots"],
                why="Options with (d) or (e) contain a false statement.",
                ncert=ref("ANA", "The Tissues (Permanent tissues)"), secs=55)

statement_pair(T_ANA, "Tissue systems", "Intermediate",
               "Subsidiary cells are the two bean-shaped cells that directly enclose the stomatal pore.",
               "Epidermal cells are parenchymatous, with a large amount of cytoplasm and a small vacuole.",
               False, False, "B",
               "Epidermal tissue system",
               "Each stoma has two bean-shaped guard cells enclosing the pore; subsidiary cells are specialised "
               "epidermal cells in the vicinity of the guard cells. Epidermal cells are parenchymatous with a small "
               "amount of cytoplasm lining the cell wall and a large vacuole.",
               ["Statement I: false, these are the guard cells",
                "Statement II: false, a small amount of cytoplasm and a large vacuole"],
               ncert=ref("ANA", "The Tissue System (Epidermal tissue system)"), secs=35)

multi_statement(T_ANA, "Plant tissues", "Intermediate",
                "Which of the following statements about phloem are correct?",
                [("The end walls of sieve tube elements are perforated in a sieve-like manner to form sieve plates.",
                  True),
                 ("Phloem fibres have pointed, needle-like apices.", True),
                 ("The walls of phloem parenchyma cells have pits through which plasmodesmatal connections exist "
                  "between cells.", True),
                 ("Phloem fibres remain living at maturity.", False),
                 ("A mature sieve element possesses a peripheral cytoplasm and a large vacuole.", True)],
                [("a", "b", "c"), ("b", "c", "d", "e"), ("a", "c", "d", "e")], "D",
                "Elements of phloem",
                "Sieve tube elements have sieve plates in their end walls; a mature element has peripheral cytoplasm "
                "and a large vacuole but no nucleus. Phloem parenchyma has cellulose walls with pits carrying "
                "plasmodesmatal connections. Phloem fibres are elongated with needle-like apices and, at maturity, "
                "lose their protoplasm and become dead.",
                ["(a) true", "(b) true", "(c) true", "(d) false: phloem fibres become dead at maturity", "(e) true"],
                why="Options with (d) contain a false statement; (a), (b) and (c) only leaves out the true statement "
                    "(e).",
                ncert=ref("ANA", "The Tissues (Phloem)"), secs=55)

assertion_reason(T_ANA, "Dicot and monocot anatomy", "Advanced",
                 "The vascular bundles of a monocot stem are described as closed.",
                 "In a monocot stem, the peripheral vascular bundles are generally smaller than the centrally "
                 "located ones.",
                 True, True, False, "B",
                 "Monocot stem",
                 "Vascular bundles are closed when there is no cambium between xylem and phloem, as in monocots. The "
                 "smaller size of the peripheral bundles is a true but separate feature; it does not explain why the "
                 "bundles are closed.",
                 ["A: true (no cambium)", "R: true", "Bundle size has nothing to do with the absence of cambium"],
                 ncert=ref("ANA", "Monocotyledonous Stem; The Tissue System (Vascular tissue system)"), secs=40)

match_list(T_ANA, "Plant tissues", "Advanced", "tissue or cell", "feature",
           ["Xylem parenchyma", "Phloem parenchyma", "Companion cells", "Spongy parenchyma"],
           ["Help in maintaining the pressure gradient in the sieve tubes",
            "Stores food materials and substances such as resins, latex and mucilage",
            "Stores food as starch or fat, and substances such as tannins",
            "Oval or round, loosely arranged cells with large air cavities, extending to the lower epidermis"],
           {"A": "III", "B": "II", "C": "I", "D": "IV"},
           [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
            {"A": "III", "B": "II", "C": "IV", "D": "I"}], "B",
           "Living cells of vascular and ground tissues",
           "Xylem parenchyma stores food as starch or fat and substances like tannins. Phloem parenchyma stores food "
           "and substances like resins, latex and mucilage. Companion cells help maintain the pressure gradient in "
           "sieve tubes. Spongy parenchyma in a dorsiventral leaf has loosely arranged oval or round cells with large "
           "spaces and air cavities.",
           ["Xylem parenchyma → III", "Phloem parenchyma → II", "Companion cells → I", "Spongy parenchyma → IV"],
           why="Tannins are linked with xylem parenchyma, and resins, latex and mucilage with phloem parenchyma; the "
               "options that swap them are wrong.",
           ncert=ref("ANA", "The Tissues (Xylem; Phloem); Dicotyledonous (Dorsiventral) Leaf"), secs=50)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "Which of the following statements about the anatomy of roots, stems and leaves are correct?",
                [("Both dicot and monocot roots have an endodermis and a pericycle.", True),
                 ("A monocot stem has a large, conspicuous parenchymatous ground tissue.", True),
                 ("Monocot roots do not undergo any secondary growth.", True),
                 ("In a dorsiventral leaf, the vascular bundles are surrounded by a layer of thin-walled bundle "
                  "sheath cells.", False)],
                [("a", "b", "c", "d"), ("b", "c"), ("a", "c", "d")], "C",
                "Comparative anatomy",
                "Monocot roots, like dicot roots, have epidermis, cortex, endodermis, pericycle, vascular bundles and "
                "pith, and they do not undergo any secondary growth. A monocot stem has scattered bundles in a large, "
                "conspicuous parenchymatous ground tissue. In a dorsiventral leaf, the vascular bundles are "
                "surrounded by a layer of thick-walled bundle sheath cells.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the bundle sheath cells are thick-walled"],
                why="Options with (d) contain a false statement; (b) and (c) only leaves out the true statement (a).",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=55)

statement_pair(T_ANA, "Tissue systems", "Advanced",
               "Medullary rays are a part of the vascular tissue system.",
               "In leaves, the ground tissue consists of thin-walled, chloroplast-containing cells called mesophyll.",
               False, True, "D",
               "Ground tissue system",
               "All tissues except the epidermis and vascular bundles constitute the ground tissue. In primary stems "
               "and roots it includes the cortex, pericycle, pith and medullary rays. In leaves, the ground tissue is "
               "the mesophyll.",
               ["Statement I: false, medullary rays belong to the ground tissue system", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System (Ground tissue system)"), secs=40)

# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Cell theory", "Basic",
       "Who first saw and described a live cell?",
       "Anton Von Leeuwenhoek", ["Robert Brown", "Matthias Schleiden", "Rudolf Virchow"], "C",
       "History of the cell",
       "Anton Von Leeuwenhoek first saw and described a live cell. Robert Brown later discovered the nucleus.",
       ["First live cell seen and described → Leeuwenhoek"],
       why="Robert Brown discovered the nucleus. Schleiden contributed to the cell theory. Virchow explained that "
           "new cells arise from pre-existing cells.",
       ncert=ref("CELL", "What is a Cell?"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In green plants, the majority of the chloroplasts are found in the:",
       "mesophyll cells of the leaves",
       ["epidermal cells of the roots", "xylem vessels of the stem", "cells of the root cap"], "A",
       "Location of chloroplasts",
       "The majority of the chloroplasts of green plants are found in the mesophyll cells of the leaves. They are "
       "lens-shaped, oval, spherical, discoid or even ribbon-like organelles.",
       ["Most chloroplasts → leaf mesophyll"],
       why="Root cells and root caps are not the main photosynthetic cells, and vessels are dead conducting elements.",
       ncert=ref("CELL", "Plastids"), secs=20)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "In a prokaryotic cell, several ribosomes may attach to a single mRNA and form a chain. This chain is called a:",
       "polysome (polyribosome)", ["mesosome", "nucleoid", "plasmid"], "B",
       "Polysomes",
       "Several ribosomes may attach to a single mRNA and form a chain called polyribosomes or a polysome. The "
       "ribosomes of a polysome translate the mRNA into proteins.",
       ["Many ribosomes on one mRNA → polysome"],
       why="A mesosome is an infolding of the plasma membrane, the nucleoid is the naked genomic DNA region and a "
           "plasmid is a small circular DNA outside the genomic DNA.",
       ncert=ref("CELL", "Prokaryotic Cells (Ribosomes and inclusion bodies)"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "A single human cell contains a thread of DNA, distributed among its 46 chromosomes, that is approximately:",
       "two metre long", ["two millimetre long", "two micrometre long", "twenty metre long"], "D",
       "Length of DNA in a human cell",
       "A single human cell has approximately two metre long thread of DNA distributed among its 46 chromosomes "
       "(23 pairs).",
       ["Human cell: about 2 m of DNA in 46 chromosomes"],
       why="The other lengths are not the NCERT value; they differ by factors of a thousand or more, or by ten.",
       ncert=ref("CELL", "Nucleus"), secs=20)

match_list(T_CELL, "Cell theory", "Basic", "cell", "shape",
           ["Red blood cell", "White blood cell", "Mesophyll cell", "Nerve cell"],
           ["Round and oval", "Branched and long", "Round and biconcave", "Amoeboid"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A",
           "Shapes of cells",
           "Cells vary greatly in shape. In the NCERT figure, red blood cells are round and biconcave, white blood "
           "cells amoeboid, mesophyll cells round and oval, and nerve cells branched and long.",
           ["RBC → III", "WBC → IV", "Mesophyll cell → I", "Nerve cell → II"],
           ncert=ref("CELL", "An Overview of Cell (Figure: different shapes of cells)"), secs=35)

statement_pair(T_CELL, "Cell theory", "Intermediate",
               "Matthias Schleiden, who examined a large number of plants, was a British zoologist.",
               "Theodore Schwann reported that cells have a thin outer layer, known today as the plasma membrane.",
               False, True, "D",
               "Cell theory",
               "Matthias Schleiden (1838) was a German botanist, and Theodore Schwann (1839) a British zoologist. "
               "Schwann reported that cells have a thin outer layer, today known as the plasma membrane, and "
               "concluded that the cell wall is a unique character of plant cells.",
               ["Statement I: false, Schleiden was a German botanist", "Statement II: true"],
               ncert=ref("CELL", "Cell Theory"), secs=35)

assertion_reason(T_CELL, "Cell envelope and membrane", "Intermediate",
                 "The cell wall prevents a bacterium from bursting or collapsing.",
                 "The bacterial cell wall determines the shape of the cell and provides a strong structural support.",
                 True, True, True, "A",
                 "Bacterial cell wall",
                 "The cell wall determines the shape of the cell and provides a strong structural support to prevent "
                 "the bacterium from bursting or collapsing. R explains A.",
                 ["A: true", "R: true", "Strong structural support → no bursting or collapse → R explains A"],
                 ncert=ref("CELL", "Prokaryotic Cells (Cell envelope and its modifications)"), secs=35)

match_list(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate", "structure", "description",
           ["Cilia", "Flagella", "Centrosome", "Microbodies"],
           ["Comparatively longer and responsible for cell movement",
            "Membrane-bound minute vesicles containing various enzymes, in both plant and animal cells",
            "Small structures that work like oars, moving the cell or the surrounding fluid",
            "Usually contains two cylindrical centrioles surrounded by amorphous pericentriolar material"],
           {"A": "III", "B": "I", "C": "IV", "D": "II"},
           [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
            {"A": "III", "B": "IV", "C": "I", "D": "II"}], "D",
           "Cilia, flagella, centrosome and microbodies",
           "Cilia are small structures that work like oars, moving the cell or the surrounding fluid; flagella are "
           "comparatively longer and responsible for cell movement. The centrosome usually contains two cylindrical "
           "centrioles surrounded by amorphous pericentriolar material. Microbodies are membrane-bound minute "
           "vesicles containing enzymes, present in plant and animal cells.",
           ["Cilia → III", "Flagella → I", "Centrosome → IV", "Microbodies → II"],
           ncert=ref("CELL", "Cilia and Flagella; Centrosome and Centrioles; Microbodies"), secs=45)

multi_statement(T_CELL, "Endomembrane system", "Intermediate",
                "Which of the following statements about the endomembrane system are correct?",
                [("Camillo Golgi (1898) first observed densely stained reticular structures near the nucleus.",
                  True),
                 ("The cis face of the Golgi apparatus is convex and the trans face is concave.", True),
                 ("Proteins synthesised by ribosomes on the endoplasmic reticulum are modified in the cisternae of "
                  "the Golgi apparatus before they are released from its trans face.", True),
                 ("The cis and trans faces of the Golgi apparatus are entirely different and are not "
                  "interconnected.", False),
                 ("The endoplasmic reticulum divides the intracellular space into luminal and extra-luminal "
                  "compartments.", True)],
                [("a", "b", "c"), ("b", "c", "d", "e"), ("a", "c", "d", "e")], "C",
                "Golgi apparatus and ER",
                "Camillo Golgi observed the Golgi bodies in 1898. The cisternae have a convex cis (forming) face and a "
                "concave trans (maturing) face; the two faces are entirely different but interconnected. Proteins "
                "made on the ER are modified in the Golgi cisternae before release from the trans face. The ER "
                "divides the intracellular space into luminal (inside ER) and extra-luminal (cytoplasm) "
                "compartments.",
                ["(a) true", "(b) true", "(c) true", "(d) false: the faces are interconnected", "(e) true"],
                why="Options with (d) contain a false statement; (a), (b) and (c) only leaves out the true statement "
                    "(e).",
                ncert=ref("CELL", "Endomembrane System"), secs=60)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
       "The number of chloroplasts per cell varies from one per cell in Chlamydomonas, a green alga, to about how "
       "many per cell in the mesophyll?",
       "20 to 40", ["2 to 4", "200 to 400", "2000 to 4000"], "C",
       "Number of chloroplasts",
       "The number of chloroplasts varies from 1 per cell of Chlamydomonas to 20–40 per cell in the mesophyll.",
       ["Chlamydomonas: 1", "Mesophyll cell: 20–40"],
       why="The other ranges are not given by NCERT; they are ten times too small or ten to a hundred times too "
           "large.",
       ncert=ref("CELL", "Plastids"), secs=25)

statement_pair(T_CELL, "Endomembrane system", "Intermediate",
               "In many cells, as in protists, food vacuoles are formed by engulfing food particles.",
               "Lysosomes are rich in hydrolases such as lipases, proteases and carbohydrases, and can digest "
               "carbohydrates, proteins, lipids and nucleic acids.",
               True, True, "A",
               "Vacuoles and lysosomes",
               "In many cells, as in protists, food vacuoles form by engulfing food particles. Lysosomes contain "
               "hydrolytic enzymes (lipases, proteases, carbohydrases) capable of digesting carbohydrates, proteins, "
               "lipids and nucleic acids.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Endomembrane System (Lysosomes; Vacuoles)"), secs=35)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                 "Mitochondria are easily visible under the light microscope even without specific staining.",
                 "Mitochondria are the sites of aerobic respiration and produce cellular energy in the form of ATP.",
                 False, True, False, "D",
                 "Mitochondria",
                 "Mitochondria are not easily visible under the microscope unless specifically stained. They are the "
                 "sites of aerobic respiration and produce ATP, hence they are called the power houses of the cell.",
                 ["A: false, they need specific staining to be seen", "R: true"],
                 ncert=ref("CELL", "Mitochondria"), secs=35)

match_list(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced", "structure", "size given in NCERT",
           ["Golgi cisterna (diameter)", "Chloroplast (length)", "Prokaryotic ribosome", "Mitochondrion (length)"],
           ["15 nm by 20 nm", "1.0–4.1 µm", "0.5 µm to 1.0 µm", "5–10 µm"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
            {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B",
           "Sizes of cell organelles",
           "Golgi cisternae are 0.5 µm to 1.0 µm in diameter. Chloroplasts are 5–10 µm long and 2–4 µm wide. "
           "Prokaryotic ribosomes are about 15 nm by 20 nm. Mitochondria are 0.2–1.0 µm in diameter and 1.0–4.1 µm "
           "long.",
           ["Golgi cisterna → III", "Chloroplast → IV", "Prokaryotic ribosome → I", "Mitochondrion → II"],
           why="Mitochondria (1.0–4.1 µm long) are shorter than chloroplasts (5–10 µm), and 0.5–1.0 µm is the "
               "diameter of a Golgi cisterna; options that swap these values are wrong.",
           ncert=ref("CELL", "Prokaryotic Cells; Golgi apparatus; Mitochondria; Plastids"), secs=55)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "Which of the following statements about prokaryotic cells are correct?",
                [("They are generally smaller and multiply more rapidly than eukaryotic cells.", True),
                 ("Plasmid DNA is used to monitor bacterial transformation with foreign DNA.", True),
                 ("Their inclusion bodies include phosphate granules, cyanophycean granules and glycogen granules.",
                  True),
                 ("Pili are elongated tubular structures made of a special protein.", True),
                 ("The bacterial flagellum has the same structure as the eukaryotic flagellum.", False)],
                [("a", "b", "d"), ("a", "c", "d", "e"), ("b", "c", "d")], "B",
                "Features of prokaryotic cells",
                "Prokaryotic cells are generally smaller and multiply faster than eukaryotic cells. Plasmid DNA is used "
                "to monitor bacterial transformation with foreign DNA. Inclusion bodies include phosphate, "
                "cyanophycean and glycogen granules. Pili are elongated tubular structures of a special protein. "
                "Bacterial flagella are structurally different from eukaryotic flagella.",
                ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: the structures differ"],
                why="(a), (c), (d) and (e) only includes the false statement (e); the three-statement options leave "
                    "out a true statement.",
                ncert=ref("CELL", "Prokaryotic Cells; Cilia and Flagella"), secs=60)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "The cristae increase the surface area of the inner mitochondrial membrane.",
                 "Mitochondria divide by fission.",
                 True, True, False, "B",
                 "Mitochondria",
                 "The inner membrane forms infoldings called cristae towards the matrix, which increase its surface "
                 "area. Mitochondria also divide by fission. R is a true but separate fact about how mitochondria "
                 "multiply; it does not explain the role of the cristae.",
                 ["A: true", "R: true", "Division by fission is unrelated to the cristae → not the explanation"],
                 ncert=ref("CELL", "Mitochondria"), secs=35)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
               "The inner membrane of the chloroplast is relatively less permeable than the outer membrane.",
               "Chromoplasts are colourless plastids that store nutrients.",
               True, False, "C",
               "Plastids",
               "The chloroplast has a double membrane, of which the inner one is relatively less permeable. "
               "Chromoplasts contain fat-soluble carotenoid pigments giving yellow, orange or red colours; the "
               "colourless plastids that store nutrients are the leucoplasts.",
               ["Statement I: true", "Statement II: false, these are leucoplasts"],
               ncert=ref("CELL", "Plastids"), secs=40)

multi_statement(T_CELL, "Nucleus", "Advanced",
                "Which of the following statements about the nucleus are correct?",
                [("The outer membrane of the nuclear envelope usually remains continuous with the endoplasmic "
                  "reticulum and also bears ribosomes.", True),
                 ("The nuclear pores are formed by the fusion of the two membranes of the nuclear envelope.", True),
                 ("Every chromosome has a primary constriction, the centromere, on the sides of which lie "
                  "disc-shaped kinetochores.", True),
                 ("Histones, the proteins present in chromatin, are acidic proteins.", False),
                 ("The interphase nucleus contains highly condensed chromosomes that are seen as distinct "
                  "structures.", False)],
                [("a", "b", "c", "d"), ("b", "c", "e"), ("a", "d", "e")], "A",
                "Structure of the nucleus",
                "The outer nuclear membrane is continuous with the ER and bears ribosomes. The nuclear envelope is "
                "interrupted by pores formed by fusion of its two membranes. Each chromosome has a centromere with "
                "disc-shaped kinetochores on its sides. Chromatin contains DNA and basic proteins called histones. "
                "The interphase nucleus has highly extended, elaborate nucleoprotein fibres (chromatin), not condensed "
                "chromosomes.",
                ["(a) true", "(b) true", "(c) true", "(d) false: histones are basic proteins",
                 "(e) false: interphase chromatin is extended"],
                why="Options with (d) or (e) contain a false statement.",
                ncert=ref("CELL", "Nucleus"), secs=60)

# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Mitosis", "Basic",
       "During prophase of mitosis, each centrosome radiates out microtubules called:",
       "asters", ["kinetochores", "chiasmata", "synaptonemal complexes"], "D",
       "Prophase",
       "The centrosome, which had duplicated during the S phase, begins to move towards opposite poles in prophase. "
       "Each centrosome radiates out microtubules called asters; the two asters together with spindle fibres form "
       "the mitotic apparatus.",
       ["Centrosome → asters; asters + spindle fibres → mitotic apparatus"],
       why="Kinetochores are disc-shaped structures on the centromere. Chiasmata and the synaptonemal complex belong "
           "to prophase I of meiosis.",
       ncert=ref("CC", "M Phase (Prophase)"), secs=20)

direct(T_CC, "Mitosis", "Basic",
       "The plane of alignment of the chromosomes at metaphase is called the:",
       "metaphase plate", ["cell plate", "equatorial furrow", "middle lamella"], "A",
       "Metaphase",
       "At metaphase, the chromosomes are moved to the spindle equator and aligned there. The plane of alignment of "
       "the chromosomes at metaphase is referred to as the metaphase plate.",
       ["Plane of alignment at metaphase → metaphase plate"],
       why="The cell plate forms during plant cytokinesis and represents the middle lamella. A furrow forms during "
           "animal cytokinesis.",
       ncert=ref("CC", "M Phase (Metaphase)"), secs=20)

direct(T_CC, "Mitosis", "Basic",
       "At the time of cytoplasmic division (cytokinesis), which organelles get distributed between the two daughter "
       "cells?",
       "Mitochondria and plastids",
       ["Nucleolus and nuclear envelope", "Centromeres and kinetochores", "Asters and spindle fibres"], "C",
       "Cytokinesis",
       "At the time of cytoplasmic division, organelles like mitochondria and plastids get distributed between the "
       "two daughter cells.",
       ["Cytokinesis: cytoplasm and organelles such as mitochondria and plastids are shared"],
       why="The nucleolus and nuclear envelope reform in telophase; centromeres and kinetochores are parts of "
           "chromosomes; asters and spindle fibres form the mitotic apparatus.",
       ncert=ref("CC", "M Phase (Cytokinesis)"), secs=25)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "Interphase is a period of rest in which the cell neither grows nor replicates its DNA.",
               "The M phase starts with cytokinesis and ends with karyokinesis.",
               False, False, "B",
               "Phases of the cell cycle",
               "Interphase, though called the resting phase, is the time when the cell prepares for division by "
               "undergoing both cell growth and DNA replication in an orderly manner. The M phase starts with nuclear "
               "division (karyokinesis) and usually ends with division of the cytoplasm (cytokinesis).",
               ["Statement I: false, the cell grows and replicates DNA in interphase",
                "Statement II: false, karyokinesis comes first, cytokinesis last"],
               ncert=ref("CC", "Cell Cycle (Phases of cell cycle)"), secs=30)

direct(T_CC, "Mitosis", "Intermediate",
       "In plant cells, the new cell wall formed during cytokinesis begins as a simple precursor called the cell "
       "plate. The cell plate represents the:",
       "middle lamella between the walls of two adjacent cells",
       ["secondary wall of the daughter cells", "plasma membrane of the daughter cells",
        "nuclear envelope of the daughter nuclei"], "B",
       "Cytokinesis in plant cells",
       "In plant cells, wall formation starts in the centre and grows outward to meet the lateral walls. It begins "
       "with a simple precursor, the cell plate, which represents the middle lamella between the walls of two "
       "adjacent cells.",
       ["Cell plate → middle lamella"],
       why="The secondary wall forms later on the inner side of the primary wall; the plasma membrane and nuclear "
           "envelope are not formed from the cell plate.",
       ncert=ref("CC", "M Phase (Cytokinesis)"), secs=30)

assertion_reason(T_CC, "Significance", "Intermediate",
                 "A growing cell has to divide to keep its nucleo-cytoplasmic ratio.",
                 "Cell growth disturbs the ratio between the nucleus and the cytoplasm.",
                 True, True, True, "A",
                 "Significance of mitosis",
                 "Cell growth disturbs the ratio between the nucleus and the cytoplasm, so it becomes essential for "
                 "the cell to divide to restore the nucleo-cytoplasmic ratio. R explains A.",
                 ["A: true", "R: true", "Growth disturbs the ratio → division restores it → R explains A"],
                 ncert=ref("CC", "Significance of Mitosis"), secs=35)

match_list(T_CC, "Mitosis", "Intermediate", "stage of mitosis", "event",
           ["Prophase", "Metaphase", "Anaphase", "Telophase"],
           ["Centromeres split and the chromatids separate",
            "The nuclear envelope assembles around the chromosome clusters, and the nucleolus, Golgi complex and "
            "ER reform",
            "The centrosomes begin to move towards opposite poles of the cell",
            "Its start is marked by the complete disintegration of the nuclear envelope"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
            {"A": "III", "B": "I", "C": "IV", "D": "II"}], "A",
           "Stages of mitosis",
           "In prophase the duplicated centrosomes begin moving to opposite poles. The complete disintegration of the "
           "nuclear envelope marks the start of metaphase. In anaphase, centromeres split and chromatids separate. "
           "In telophase, the nuclear envelope develops around each chromosome cluster and the nucleolus, Golgi "
           "complex and ER reform.",
           ["Prophase → III", "Metaphase → IV", "Anaphase → I", "Telophase → II"],
           ncert=ref("CC", "M Phase"), secs=45)

multi_statement(T_CC, "Meiosis", "Intermediate",
                "Which of the following statements about the later stages of meiosis are correct?",
                [("Prophase II is a much simpler prophase than prophase I.", True),
                 ("Interkinesis is generally short-lived.", True),
                 ("At the end of telophase I, the chromosomes reach the extremely extended state of the interphase "
                  "nucleus.", False),
                 ("In metaphase II, microtubules from opposite poles attach to the kinetochores of sister "
                  "chromatids.", True),
                 ("In anaphase II, sister chromatids move towards opposite poles by shortening of the microtubules "
                  "attached to their kinetochores.", True)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")], "D",
                "Interkinesis and meiosis II",
                "After telophase I, the chromosomes undergo some dispersion but do not reach the extremely extended "
                "state of the interphase nucleus. Interkinesis is generally short-lived and is followed by prophase "
                "II, a much simpler prophase. In metaphase II, microtubules from opposite poles attach to the "
                "kinetochores of sister chromatids; in anaphase II, the centromeres split and the chromatids move "
                "apart as the attached microtubules shorten.",
                ["(a) true", "(b) true", "(c) false: they do not reach the extended interphase state", "(d) true",
                 "(e) true"],
                why="Options with (c) contain a false statement; (b), (d) and (e) only leaves out the true statement "
                    "(a).",
                ncert=ref("CC", "Meiosis (Meiosis I: Telophase I; Meiosis II)"), secs=60)

# 2n = 14, G1 nucleus = 2C; S phase doubles DNA (2C -> 4C) without changing the chromosome number
_cc_2n, _cc_c_g1 = 14, 2
_cc_c_g2 = 2 * _cc_c_g1
numerical(T_CC, "Cell cycle phases", "Intermediate",
          "A plant cell has 2n = 14 chromosomes, and its nucleus contains 2C DNA in the G1 phase. What are the number "
          "of chromosomes and the DNA content of this cell in the G2 phase?",
          "14 chromosomes and 4C DNA", ["28 chromosomes and 4C DNA", "14 chromosomes and 2C DNA",
                                        "7 chromosomes and 2C DNA"], "C",
          _cc_2n == 14 and _cc_c_g2 == 4,
          "DNA content and chromosome number through the cell cycle",
          "During the S phase, the amount of DNA per cell doubles from 2C to 4C, but there is no increase in the "
          "chromosome number: each chromosome now has two sister chromatids. In G2 the cell therefore still has 2n = "
          "14 chromosomes, with 4C DNA.",
          ["G1: 14 chromosomes, 2C", "S phase: DNA doubles, chromosome number unchanged", "G2: 14 chromosomes, 4C"],
          "28 chromosomes doubles the chromosome number, which does not happen in S phase. 2C ignores DNA "
          "replication. 7 chromosomes and 2C describes a cell after meiosis I, not a cell in G2.",
          ref("CC", "Cell Cycle (Phases of cell cycle: S phase)"), secs=50)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "Crossing over leads to recombination of genetic material on the two chromosomes.",
                 "Crossing over takes place at recombination nodules between the sister chromatids of a chromosome.",
                 True, False, False, "C",
                 "Crossing over",
                 "In pachytene, recombination nodules appear at the sites where crossing over occurs between "
                 "non-sister chromatids of the homologous chromosomes. Crossing over is the exchange of genetic "
                 "material between two homologous chromosomes and leads to recombination. R wrongly says sister "
                 "chromatids.",
                 ["A: true", "R: false, crossing over is between non-sister chromatids of homologous chromosomes"],
                 ncert=ref("CC", "Meiosis I (Prophase I: Pachytene)"), secs=40)

statement_pair(T_CC, "Meiosis", "Advanced",
               "In diplotene, the X-shaped structures formed at the sites of crossing over are called recombination "
               "nodules.",
               "By the end of pachytene, recombination between homologous chromosomes is completed, leaving the "
               "chromosomes linked at the sites of crossing over.",
               False, True, "D",
               "Pachytene and diplotene",
               "Recombination nodules appear in pachytene at the sites of crossing over, and by the end of pachytene "
               "recombination is complete. In diplotene the synaptonemal complex dissolves and the homologues separate "
               "except at the sites of crossovers; these X-shaped structures are called chiasmata.",
               ["Statement I: false, the X-shaped structures are chiasmata", "Statement II: true"],
               ncert=ref("CC", "Meiosis I (Prophase I)"), secs=40)

# two rounds of mitosis: 1 -> 2 -> 4 cells; each cell then undergoes meiosis -> 4 haploid cells each
_cc_mit = 2 ** 2
_cc_cells = _cc_mit * 4
_cc_n = 10 // 2
numerical(T_CC, "Significance", "Advanced",
          "A cell with 2n = 10 divides twice by mitosis, every cell dividing once in each round. Each of the cells "
          "formed then undergoes meiosis. How many cells are finally formed, and how many chromosomes does each of "
          "them have?",
          "16 cells, each with 5 chromosomes",
          ["8 cells, each with 5 chromosomes", "16 cells, each with 10 chromosomes",
           "32 cells, each with 5 chromosomes"], "A",
          _cc_mit == 4 and _cc_cells == 16 and _cc_n == 5,
          "Products of mitosis and meiosis",
          "Two rounds of mitosis give 2 × 2 = 4 diploid cells (2n = 10). Each meiosis gives four haploid cells, so "
          "4 × 4 = 16 cells are formed, each with n = 5 chromosomes.",
          ["Mitosis × 2: 1 → 2 → 4 cells, each 2n = 10", "Meiosis of each: 4 × 4 = 16 cells", "Each cell: n = 5"],
          "8 cells counts only two products per meiosis. 10 chromosomes forgets that meiosis halves the chromosome "
          "number. 32 cells adds an extra doubling.",
          ref("CC", "Mitosis; Meiosis"), secs=60)

multi_statement(T_CC, "Significance", "Advanced",
                "Which of the following statements about the significance of mitosis and meiosis are correct?",
                [("In some lower plants and in some social insects, haploid cells also divide by mitosis.", True),
                 ("Meiosis conserves the specific chromosome number of each species across generations in sexually "
                  "reproducing organisms.", True),
                 ("Meiosis takes place during gametogenesis in plants and animals.", True),
                 ("Blood cells, which are constantly replaced, arise by meiosis.", False),
                 ("Mitosis increases the genetic variability in the population from one generation to the next.",
                  False)],
                [("a", "b", "c", "d"), ("b", "c", "e"), ("a", "c", "d")], "B",
                "Significance of cell division",
                "Mitosis is usually restricted to diploid cells, but in some lower plants and some social insects "
                "haploid cells also divide mitotically. Mitosis gives genetically identical cells and is used in "
                "growth and repair, for example in replacing blood cells. Meiosis occurs during gametogenesis, "
                "conserves the chromosome number of the species across generations and increases genetic "
                "variability.",
                ["(a) true", "(b) true", "(c) true", "(d) false: cell replacement is by mitosis",
                 "(e) false: meiosis, not mitosis, increases variability"],
                why="Options with (d) or (e) contain a false statement.",
                ncert=ref("CC", "Significance of Mitosis; Significance of Meiosis"), secs=60)

# =============================================================== 7. Photosynthesis (5/6/5)
direct(T_PS, "Site and pigments", "Basic",
       "Within the mesophyll cells, the chloroplasts align themselves along the walls of the cells so that they:",
       "get the optimum quantity of the incident light",
       ["avoid all contact with light", "store the maximum amount of starch",
        "come close to the xylem vessels for water"], "B",
       "Site of photosynthesis",
       "Photosynthesis takes place in the green parts of the plant, mostly the leaves. Within the mesophyll cells, "
       "the chloroplasts generally align themselves along the walls so that they get the optimum quantity of "
       "incident light.",
       ["Chloroplasts line the mesophyll cell walls → optimum light"],
       why="The alignment is described in relation to light, not to starch storage or water supply.",
       ncert=ref("PS", "Where does Photosynthesis take place?"), secs=25)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "In each photosystem, all the pigments except one molecule of chlorophyll a form a light-harvesting system. "
       "This system is called the:",
       "antennae", ["reaction centre", "Z scheme", "ATP synthase complex"], "D",
       "Light-harvesting complexes",
       "The pigments are organised into two discrete light-harvesting complexes (LHC) within PS I and PS II. In each "
       "photosystem, all the pigments except one molecule of chlorophyll a form a light-harvesting system called the "
       "antennae. The single chlorophyll a molecule forms the reaction centre.",
       ["Antennae: all pigments except one chlorophyll a", "Reaction centre: one chlorophyll a"],
       why="The reaction centre is the single chlorophyll a molecule. The Z scheme is the shape of the electron "
           "carrier sequence. ATP synthase makes ATP.",
       ncert=ref("PS", "What is Light Reaction?"), secs=25)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Melvin Calvin found that the first product of CO₂ fixation was a 3-carbon organic acid. His studies used:",
       "radioactive ¹⁴C in algal photosynthesis",
       ["radioactive ³²P in bacterial photosynthesis", "¹⁸O-labelled water in leaf discs",
        "¹⁵N-labelled ammonia in pea roots"], "A",
       "Discovery of the C3 pathway",
       "The use of radioactive ¹⁴C by Melvin Calvin in algal photosynthesis studies led to the discovery that the "
       "first CO₂ fixation product was a 3-carbon organic acid (PGA).",
       ["Calvin: ¹⁴C, algae → first product PGA (3C)"],
       why="NCERT links Calvin's discovery with radioactive carbon, the element being fixed, used in algae.",
       ncert=ref("PS", "The Primary Acceptor of CO₂"), secs=25)

direct(T_PS, "Limiting factors", "Basic",
       "The concentration of carbon dioxide in the atmosphere is very low, between:",
       "0.03 and 0.04 per cent", ["3 and 4 per cent", "0.3 and 0.4 per cent", "21 and 22 per cent"], "C",
       "CO₂ as a factor in photosynthesis",
       "Carbon dioxide is the major limiting factor for photosynthesis. Its concentration in the atmosphere is very "
       "low, between 0.03 and 0.04 per cent.",
       ["Atmospheric CO₂: 0.03–0.04%"],
       why="The other values are ten to a hundred times too high; about 21 per cent is the oxygen content of air.",
       ncert=ref("PS", "Factors affecting Photosynthesis (Carbon dioxide concentration)"), secs=20)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Basic",
               "The products of the light reaction are ATP, NADPH and O₂.",
               "The O₂ produced in the light reaction is used in the Calvin cycle in the stroma.",
               True, False, "C",
               "Products of the light reaction",
               "The products of the light reaction are ATP, NADPH and O₂. O₂ diffuses out of the chloroplast, while "
               "ATP and NADPH are used to drive the processes leading to the synthesis of food (sugars).",
               ["Statement I: true", "Statement II: false, ATP and NADPH (not O₂) are used in the biosynthetic phase"],
               ncert=ref("PS", "Where are the ATP and NADPH used?"), secs=30)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                 "The bundle sheath cells of C4 plants have thick walls that are impervious to gaseous exchange and "
                 "have no intercellular spaces.",
                 "The bundle sheath cells of C4 plants are rich in the enzyme RuBisCO.",
                 True, True, False, "B",
                 "Bundle sheath cells of C4 plants",
                 "Bundle sheath cells have a large number of chloroplasts, thick walls impervious to gaseous exchange "
                 "and no intercellular spaces. They are also rich in RuBisCO, but this enzyme content says nothing "
                 "about why their walls are thick or why they lack intercellular spaces.",
                 ["A: true", "R: true", "Enzyme content does not explain wall structure → not the explanation"],
                 ncert=ref("PS", "The C4 Pathway"), secs=40)

match_list(T_PS, "Calvin cycle and C4 pathway", "Intermediate", "process", "event",
           ["Carboxylation", "Reduction", "Regeneration", "Photorespiration"],
           ["One ATP is used for phosphorylation to form RuBP",
            "RuBP combines with O₂ to form one molecule of PGA and phosphoglycolate",
            "RuBisCO fixes CO₂ with RuBP to form two molecules of 3-PGA",
            "Two ATP for phosphorylation and two NADPH for reduction are used per CO₂ fixed"],
           {"A": "III", "B": "IV", "C": "I", "D": "II"},
           [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
            {"A": "II", "B": "IV", "C": "I", "D": "III"}], "D",
           "Stages of the Calvin cycle and photorespiration",
           "In carboxylation, RuBisCO fixes CO₂ with RuBP to give two 3-PGA. Reduction uses 2 ATP and 2 NADPH per "
           "CO₂ fixed. Regeneration of RuBP uses one ATP. In photorespiration, RuBP binds O₂ to give one PGA and "
           "phosphoglycolate.",
           ["Carboxylation → III", "Reduction → IV", "Regeneration → I", "Photorespiration → II"],
           why="The 3 ATP needed per CO₂ are split as 2 in reduction and 1 in regeneration; options that swap them "
               "are wrong.",
           ncert=ref("PS", "The Calvin Cycle; Photorespiration"), secs=50)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following statements about the light reaction are correct?",
                [("The pigments are organised into two discrete photochemical light-harvesting complexes (LHC) "
                  "within Photosystem I and Photosystem II.", True),
                 ("Each LHC is made up of hundreds of pigment molecules bound to proteins.", True),
                 ("The reaction centre of each photosystem is made up of several chlorophyll b molecules.", False),
                 ("Photophosphorylation is the synthesis of ATP from ADP and inorganic phosphate in the presence of "
                  "light.", True),
                 ("Only Photosystem I takes part in non-cyclic photophosphorylation.", False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")], "C",
                "Photosystems and photophosphorylation",
                "The pigments are organised into LHCs within PS I and PS II, each made of hundreds of pigment "
                "molecules bound to proteins. The reaction centre is a single chlorophyll a molecule. Photo"
                "phosphorylation is ATP synthesis from ADP and Pi in light. Both photosystems work in non-cyclic "
                "photophosphorylation; only PS I works in cyclic photophosphorylation.",
                ["(a) true", "(b) true", "(c) false: the reaction centre is one chlorophyll a molecule", "(d) true",
                 "(e) false: both photosystems take part in non-cyclic photophosphorylation"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("PS", "What is Light Reaction?; Cyclic and Non-cyclic Photo-phosphorylation"), secs=60)

# 6CO2 + 12H2O -> C6H12O6 + 6H2O + 6O2 ; 2H2O -> 4H+ + O2 + 4e-  (each O2 needs two H2O split)
_ps_glucose = 2
_ps_o2 = 6 * _ps_glucose
_ps_h2o_split = 2 * _ps_o2
numerical(T_PS, "Light reactions and photophosphorylation", "Intermediate",
          "The overall equation of photosynthesis is\n6CO₂ + 12H₂O → C₆H₁₂O₆ + 6H₂O + 6O₂\nand the splitting of water "
          "in the light reaction is 2H₂O → 4H⁺ + O₂ + 4e⁻. All the O₂ released comes from water. When two molecules "
          "of glucose are made, how many molecules of O₂ are released, and how many molecules of water must be split "
          "to release them?",
          "12 O₂; 24 H₂O split", ["6 O₂; 12 H₂O split", "12 O₂; 12 H₂O split", "24 O₂; 24 H₂O split"], "A",
          _ps_o2 == 12 and _ps_h2o_split == 24,
          "Source of oxygen in photosynthesis",
          "Each glucose is accompanied by the release of 6 O₂, so two glucose release 12 O₂. Splitting two water "
          "molecules gives one O₂, so 12 O₂ require 24 water molecules to be split, which matches 2 × 12 H₂O in the "
          "overall equation.",
          ["O₂ released = 6 × 2 = 12", "H₂O split = 2 × O₂ = 24"],
          "6 O₂ and 12 H₂O is the answer for one glucose. 12 H₂O split assumes one water gives one O₂. 24 O₂ "
          "doubles the oxygen released.",
          ref("PS", "Splitting of Water (Light reaction)"), secs=70)

statement_pair(T_PS, "Limiting factors", "Intermediate",
               "The temperature optimum for photosynthesis depends on the habitat a plant is adapted to; tropical "
               "plants have a higher temperature optimum than plants adapted to temperate climates.",
               "An increase in CO₂ concentration up to 0.05 per cent can cause an increase in CO₂ fixation rates, "
               "but levels beyond this can become damaging over longer periods.",
               True, True, "A",
               "Temperature and CO₂ as factors",
               "The temperature optimum depends on the habitat; tropical plants have a higher optimum than temperate "
               "plants. Increasing CO₂ up to 0.05 per cent can increase CO₂ fixation, but higher levels can become "
               "damaging over longer periods.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Factors affecting Photosynthesis (Temperature; Carbon dioxide concentration)"),
               secs=40)

match_list(T_PS, "Calvin cycle and C4 pathway", "Intermediate", "molecule", "number of carbon atoms",
           ["Ribulose bisphosphate (RuBP)", "Phosphoglyceric acid (PGA)", "Oxaloacetic acid (OAA)", "Glucose"],
           ["Six", "Three", "Four", "Five"],
           {"A": "IV", "B": "II", "C": "III", "D": "I"},
           [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
            {"A": "III", "B": "II", "C": "IV", "D": "I"}], "A",
           "Carbon compounds of photosynthesis",
           "RuBP, the CO₂ acceptor of the Calvin cycle, is a 5-carbon ketose sugar. PGA, the first product in C3 "
           "plants, has three carbons. OAA, the first product in C4 plants, has four. Glucose has six.",
           ["RuBP → 5 (IV)", "PGA → 3 (II)", "OAA → 4 (III)", "Glucose → 6 (I)"],
           ncert=ref("PS", "The Primary Acceptor of CO₂; The Calvin Cycle"), secs=40)

assertion_reason(T_PS, "Photorespiration", "Advanced",
                 "Photorespiration is a wasteful process.",
                 "In photorespiration, CO₂ is released and ATP is used up.",
                 True, True, True, "A",
                 "Photorespiration",
                 "In the photorespiratory pathway there is neither synthesis of sugars nor of ATP; instead CO₂ is "
                 "released and ATP is utilised. Because fixed carbon is lost and energy is spent with no gain, the "
                 "process is wasteful. R explains A.",
                 ["A: true", "R: true", "Carbon lost + ATP spent → wasteful → R explains A"],
                 ncert=ref("PS", "Photorespiration"), secs=40)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "Six turns of the Calvin cycle are required for the removal of one molecule of glucose from the "
                 "pathway.",
                 "Each turn of the Calvin cycle fixes six molecules of CO₂.",
                 True, False, False, "C",
                 "Turns of the Calvin cycle",
                 "Each turn of the Calvin cycle fixes one molecule of CO₂. A glucose molecule has six carbons, so the "
                 "fixation of six CO₂ molecules, that is six turns, is needed to remove one glucose. R is false.",
                 ["A: true", "R: false, each turn fixes one CO₂"],
                 ncert=ref("PS", "The Calvin Cycle"), secs=40)

multi_statement(T_PS, "Chemiosmosis", "Advanced",
                "Which of the following statements about the development of the proton gradient in chloroplasts are "
                "correct?",
                [("The primary electron acceptor, located towards the outer side of the thylakoid membrane, transfers "
                  "its electron to an H carrier, which removes a proton from the stroma.", True),
                 ("When the H carrier passes its electron to a carrier on the inner side of the membrane, the proton "
                  "is released into the lumen.", True),
                 ("The protons needed to reduce NADP⁺ to NADPH + H⁺ are taken from the lumen.", False),
                 ("As a result of these events, the pH in the lumen decreases.", True),
                 ("Chemiosmosis requires a membrane, a proton pump, a proton gradient and ATP synthase.", True)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")], "B",
                "Chemiosmotic hypothesis",
                "Protons accumulate in the lumen because (i) water is split on the inner side, (ii) the H carrier "
                "removes protons from the stroma and releases them into the lumen, and (iii) NADP reductase on the "
                "stroma side uses protons from the stroma. The lumen pH therefore falls. Chemiosmosis needs a "
                "membrane, a proton pump, a proton gradient and ATP synthase.",
                ["(a) true", "(b) true", "(c) false: these protons are removed from the stroma", "(d) true",
                 "(e) true"],
                why="Options with (c) contain a false statement; (b), (d) and (e) only leaves out the true statement "
                    "(a).",
                ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=65)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                "Which of the following statements about C4 plants are correct?",
                [("They are adapted to dry tropical regions.", True),
                 ("They use the Calvin cycle as the main biosynthetic pathway.", True),
                 ("In them, the C4 acid is broken down in the mesophyll cells to release CO₂.", False),
                 ("Their bundle sheath cells have a large number of chloroplasts.", True),
                 ("In their mesophyll cells, the first stable product of CO₂ fixation is a 3-carbon acid.", False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "c", "e")], "D",
                "The C4 pathway",
                "C4 plants are adapted to dry tropical regions. In the mesophyll, PEP is carboxylated to the 4-carbon "
                "OAA. The C4 acid moves to the bundle sheath cells, which have many chloroplasts; there it is broken "
                "down to release CO₂, which enters the Calvin cycle, the main biosynthetic pathway.",
                ["(a) true", "(b) true", "(c) false: the C4 acid is broken down in the bundle sheath cells",
                 "(d) true", "(e) false: the first product is the 4-carbon OAA"],
                why="Options with (c) or (e) contain a false statement.",
                ncert=ref("PS", "The C4 Pathway"), secs=60)

direct(T_PS, "Limiting factors", "Advanced",
       "A C3 plant and a C4 plant are kept under high light intensity. The CO₂ concentration around them is raised "
       "from about 360 µL L⁻¹ to 450 µL L⁻¹. What is expected?",
       "The rate of photosynthesis of the C3 plant rises, while that of the C4 plant changes little because it is "
       "already near saturation",
       ["The rate of photosynthesis of the C4 plant rises, while that of the C3 plant changes little because it is "
        "already saturated",
        "Neither plant responds, because at high light intensity CO₂ is never limiting",
        "Both plants show a sharp fall in photosynthesis, because any rise above 360 µL L⁻¹ is damaging"], "B",
       "Response of C3 and C4 plants to CO₂",
       "At high light intensities both C3 and C4 plants show an increase in photosynthesis with higher CO₂. C4 "
       "plants show saturation at about 360 µL L⁻¹, whereas C3 plants respond to increased CO₂ and saturation is "
       "seen only beyond 450 µL L⁻¹. Current CO₂ levels are therefore limiting to C3 plants.",
       ["C4 saturates at about 360 µL L⁻¹", "C3 saturates only beyond 450 µL L⁻¹",
        "360 → 450 µL L⁻¹: C3 rises, C4 nearly saturated"],
       why="The first option reverses the saturation values. At low, not high, light intensity neither group "
           "responds to high CO₂. Damage is described only for levels beyond about 0.05 per cent over long periods.",
       ncert=ref("PS", "Factors affecting Photosynthesis (Carbon dioxide concentration)"), secs=60)

# =============================================================== 8. Respiration in Plants (3/5/3)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "In alcoholic fermentation, pyruvic acid is converted to CO₂ and ethanol by the enzymes:",
       "pyruvic acid decarboxylase and alcohol dehydrogenase",
       ["lactate dehydrogenase and hexokinase", "pyruvic dehydrogenase and citrate synthase",
        "invertase and phosphofructokinase"], "B",
       "Alcoholic fermentation",
       "In fermentation, say by yeast, the incomplete oxidation of glucose is achieved under anaerobic conditions; "
       "pyruvic acid is converted to CO₂ and ethanol. The enzymes pyruvic acid decarboxylase and alcohol "
       "dehydrogenase catalyse these reactions.",
       ["Pyruvic acid → (pyruvic acid decarboxylase) → acetaldehyde + CO₂ → (alcohol dehydrogenase) → ethanol"],
       why="Lactate dehydrogenase makes lactic acid. Pyruvic dehydrogenase and citrate synthase work in aerobic "
           "respiration in the mitochondria. Invertase acts on sucrose, before glycolysis.",
       ncert=ref("RES", "Fermentation"), secs=25)

direct(T_RES, "Electron transport system", "Basic",
       "In respiration, ATP synthesis linked to the electron transport system is called oxidative phosphorylation "
       "because the energy used to create the proton gradient comes from:",
       "oxidation-reduction reactions", ["light absorbed by chlorophyll", "the hydrolysis of GTP",
                                         "the splitting of water"], "D",
       "Oxidative phosphorylation",
       "Unlike photophosphorylation, where light energy is used to create the proton gradient, in respiration the "
       "energy of oxidation-reduction is used for the same process. That is why it is called oxidative "
       "phosphorylation.",
       ["Photophosphorylation: light energy", "Oxidative phosphorylation: energy of oxidation-reduction"],
       why="Light energy drives photophosphorylation. GTP hydrolysis and water splitting are not the source of the "
           "respiratory proton gradient.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=25)

# fermentation: net 2 ATP per glucose; aerobic: net 38 ATP per glucose (NCERT balance sheet)
_res_ferm, _res_aer = 2, 38
_res_glucose_needed = _res_aer // _res_ferm
numerical(T_RES, "ATP yield and amphibolic pathway", "Basic",
          "Fermentation gives a net gain of 2 ATP per molecule of glucose, while complete aerobic respiration can give "
          "a net gain of 38 ATP per molecule of glucose. How many molecules of glucose must be fermented to obtain "
          "as much ATP as the aerobic respiration of one molecule of glucose?",
          "19", ["38", "76", "36"], "C",
          _res_glucose_needed == 19 and _res_glucose_needed * _res_ferm == _res_aer,
          "ATP yield of fermentation and aerobic respiration",
          "Fermentation gives a net 2 ATP per glucose; aerobic respiration can give a net 38 ATP. Glucose needed = "
          "38 ÷ 2 = 19.",
          ["38 ÷ 2 = 19 molecules of glucose"],
          "38 forgets that each fermented glucose gives 2 ATP. 76 multiplies instead of dividing. 36 subtracts the "
          "2 ATP of glycolysis instead of dividing.",
          ref("RES", "Fermentation; The Respiratory Balance Sheet"), secs=40)

statement_pair(T_RES, "TCA cycle", "Intermediate",
               "In aerobic respiration, the complete oxidation of pyruvate takes place in the matrix of the "
               "mitochondria, while the passing of electrons to O₂ with the synthesis of ATP takes place on the "
               "inner mitochondrial membrane.",
               "The oxidative decarboxylation of pyruvic acid requires the participation of several coenzymes, "
               "including NAD⁺ and coenzyme A.",
               True, True, "A",
               "Aerobic respiration",
               "The complete oxidation of pyruvate by stepwise removal of hydrogen atoms takes place in the matrix, "
               "and the transfer of electrons to O₂ with ATP synthesis takes place on the inner membrane. Pyruvic "
               "dehydrogenase needs coenzymes including NAD⁺ and coenzyme A.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Aerobic Respiration"), secs=40)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "Glycolysis is the only process of respiration in anaerobic organisms.",
                 "In glycolysis, fructose 1,6-bisphosphate is split into dihydroxyacetone phosphate and "
                 "3-phosphoglyceraldehyde (PGAL).",
                 True, True, False, "B",
                 "Glycolysis",
                 "Glycolysis occurs in all living organisms, and in anaerobic organisms it is the only process in "
                 "respiration. Splitting of fructose 1,6-bisphosphate into DHAP and PGAL is a true step of the "
                 "pathway, but it does not explain why anaerobic organisms depend on glycolysis alone.",
                 ["A: true", "R: true", "R is a step of glycolysis, not the reason for A"],
                 ncert=ref("RES", "Glycolysis"), secs=40)

# glycolysis per glucose: net 2 ATP (substrate level) + 2 NADH; each NADH -> 3 ATP in the ETS
_res_gly_atp, _res_gly_nadh = 2, 2
_res_gly_total = _res_gly_atp + 3 * _res_gly_nadh
numerical(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
          "Glycolysis of one molecule of glucose gives a net gain of 2 ATP and forms 2 NADH + H⁺. Assume that this "
          "NADH is oxidised through the mitochondrial electron transport system and that each NADH gives 3 ATP. How "
          "many ATP are obtained in all from the glycolysis of one molecule of glucose?",
          "8", ["2", "6", "10"], "D",
          _res_gly_total == 8,
          "ATP from glycolysis under aerobic conditions",
          "Net ATP made directly in glycolysis = 2. The 2 NADH give 2 × 3 = 6 ATP in the ETS. Total = 2 + 6 = 8.",
          ["Direct (net) ATP = 2", "From NADH = 2 × 3 = 6", "Total = 8"],
          "2 counts only the direct ATP. 6 counts only the NADH. 10 adds the 4 ATP formed directly instead of the "
          "net 2 (the 2 ATP used up in glycolysis are not subtracted).",
          ref("RES", "Glycolysis; Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=60)

multi_statement(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
                "Which of the following statements about respiration are correct?",
                [("Respiration is the breaking of C–C bonds of complex compounds through oxidation within the cells, "
                  "leading to the release of considerable energy.", True),
                 ("The energy released by oxidation in respiration is used directly by the cell and is not used to "
                  "synthesise ATP.", False),
                 ("Under certain conditions, organic acids can be used as respiratory substrates in some plants.",
                  True),
                 ("The carbon skeletons produced during respiration are used as precursors for the biosynthesis of "
                  "other molecules in the cell.", True),
                 ("In the complete combustion of glucose, most of the energy is given out as heat.", True)],
                [("a", "b", "c", "d"), ("c", "d", "e"), ("a", "b", "e")], "C",
                "Respiration and respiratory substrates",
                "Respiration breaks C–C bonds of complex compounds by oxidation, releasing considerable energy. This "
                "energy is not used directly; it is used to synthesise ATP, which is broken down whenever energy is "
                "needed. Carbohydrates are the usual substrates, but proteins, fats and even organic acids can be "
                "used in some plants under certain conditions. Carbon skeletons from respiration are precursors for "
                "biosynthesis. When glucose is burnt completely, most of the energy is given out as heat.",
                ["(a) true", "(b) false: the energy is used to synthesise ATP", "(c) true", "(d) true", "(e) true"],
                why="Options with (b) contain a false statement; (c), (d) and (e) only leaves out the true statement "
                    "(a).",
                ncert=ref("RES", "Introduction; Do Plants Breathe?"), secs=60)

multi_statement(T_RES, "Respiratory quotient", "Intermediate",
                "Which of the following statements about the respiratory quotient (RQ) are correct?",
                [("The RQ depends upon the type of respiratory substrate used during respiration.", True),
                 ("For tripalmitin, 2(C₅₁H₉₈O₆) + 145O₂ → 102CO₂ + 98H₂O + energy, so its RQ is about 0.7.", True),
                 ("In living organisms, pure proteins or fats are never used as respiratory substrates.", True),
                 ("The RQ of tripalmitin is higher than that of a carbohydrate that is completely oxidised.", False)],
                [("a", "b", "c", "d"), ("b", "c"), ("a", "c", "d")], "A",
                "Respiratory quotient",
                "The RQ (volume of CO₂ evolved ÷ volume of O₂ consumed) depends on the substrate. For tripalmitin it "
                "is 102 ÷ 145 ≈ 0.7, which is lower than the RQ of 1 for a completely oxidised carbohydrate. In "
                "living organisms the respiratory substrates are often more than one; pure proteins or fats are never "
                "used.",
                ["(a) true", "(b) true: 102/145 = 0.70", "(c) true",
                 "(d) false: 0.7 is lower than 1"],
                why="Options with (d) contain a false statement; (b) and (c) only leaves out the true statement (a).",
                ncert=ref("RES", "Respiratory Quotient"), secs=55)

# per pyruvate (NCERT summary): 4 NADH, 1 FADH2, 1 ATP; NADH -> 3 ATP, FADH2 -> 2 ATP; two pyruvate per glucose
_res_per_pyr = 4 * 3 + 1 * 2 + 1
_res_two_pyr = 2 * _res_per_pyr
numerical(T_RES, "ATP yield and amphibolic pathway", "Advanced",
          "The oxidation of one molecule of pyruvic acid in the mitochondrial matrix (link reaction plus TCA cycle) "
          "is summarised as\nPyruvic acid + 4NAD⁺ + FAD⁺ + 2H₂O + ADP + Pi → 3CO₂ + 4NADH + 4H⁺ + FADH₂ + ATP\n"
          "Taking 3 ATP per NADH and 2 ATP per FADH₂ in the electron transport system, how many ATP are obtained in "
          "all from the complete oxidation of the two molecules of pyruvic acid formed from one glucose?",
          "30", ["15", "28", "38"], "B",
          _res_per_pyr == 15 and _res_two_pyr == 30,
          "ATP yield from pyruvate oxidation",
          "Per pyruvic acid: 4 NADH × 3 = 12 ATP, 1 FADH₂ × 2 = 2 ATP, and 1 ATP directly (via GTP); total 15. One "
          "glucose gives two pyruvic acid molecules, so 2 × 15 = 30 ATP.",
          ["Per pyruvate: 12 + 2 + 1 = 15", "Two pyruvate: 2 × 15 = 30"],
          "15 is the yield of one pyruvic acid only. 28 leaves out the 2 ATP made directly in the cycle. 38 is the "
          "total for the whole glucose, including the 8 ATP of glycolysis.",
          ref("RES", "Tricarboxylic Acid Cycle; Electron Transport System (ETS) and Oxidative Phosphorylation"),
          secs=90)

multi_statement(T_RES, "TCA cycle", "Advanced",
                "Which of the following statements about the TCA cycle and the electron transport system are "
                "correct?",
                [("Continued oxidation of acetyl CoA via the TCA cycle requires the continued replenishment of "
                  "oxaloacetic acid.", True),
                 ("It also requires the regeneration of NAD⁺ and FAD⁺ from NADH and FADH₂.", True),
                 ("Oxidation of one molecule of NADH in the electron transport system gives rise to 2 ATP, and of "
                  "one molecule of FADH₂ to 3 ATP.", False),
                 ("In a coupled reaction, GTP is converted to GDP with the simultaneous synthesis of ATP from ADP.",
                  True),
                 ("The TCA cycle was elucidated by Hans Krebs.", True)],
                [("a", "b", "c"), ("b", "c", "d", "e"), ("a", "c", "d", "e")], "D",
                "TCA cycle and ETS",
                "The cycle needs continued replenishment of OAA and regeneration of NAD⁺ and FAD⁺. GTP formed during "
                "the conversion of succinyl CoA to succinic acid is converted to GDP with the synthesis of ATP. One "
                "NADH gives 3 ATP and one FADH₂ gives 2 ATP. The cycle is also called the Krebs cycle after Hans "
                "Krebs, who elucidated it.",
                ["(a) true", "(b) true", "(c) false: NADH gives 3 ATP and FADH₂ gives 2 ATP", "(d) true",
                 "(e) true"],
                why="Every option except the correct one contains the false statement (c).",
                ncert=ref("RES", "Tricarboxylic Acid Cycle; Electron Transport System (ETS) and Oxidative "
                                 "Phosphorylation"), secs=60)

statement_pair(T_RES, "Glycolysis and fermentation", "Advanced",
               "The first cells on the earth probably lived in an atmosphere that was rich in oxygen.",
               "All living organisms retain the enzymatic machinery to partially oxidise glucose without the help of "
               "oxygen.",
               False, True, "D",
               "Anaerobic beginnings of respiration",
               "The first cells on this planet lived in an atmosphere that lacked oxygen. Even among present-day "
               "organisms, all retain the enzymatic machinery to partially oxidise glucose without oxygen; this "
               "breakdown of glucose to pyruvic acid is glycolysis.",
               ["Statement I: false, the early atmosphere lacked oxygen", "Statement II: true"],
               ncert=ref("RES", "Glycolysis"), secs=40)

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
    assert pkg["output"] == "batches/parts/BATCH_003_BOT_p1.json"


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "Package BOT_003_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis, Respiration. 122 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
