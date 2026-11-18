"""Writes batches/parts/BATCH_009_BOT_p1.json: package BOT_009_p1 of batch 9 (Botany, 123 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis.
IDs NEET_BOT_002001 .. NEET_BOT_002123.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books or outside the NMC 2026 list (secondary growth, taxonomical aids, plant life cycles and
alternation of generations, early experiments on photosynthesis) is not used. Facts already tested in batches 1-8 were
listed with `merge_batch.py stems 009 BOT_009_p1` and avoided; where a topic is saturated, questions test new
combinations, comparisons, identifications or applications. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_009/BOT_009_p1.py
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
PLAN = ROOT / "batches" / "plans" / "BATCH_009_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_009_BOT_p1.json"
PACKAGE = "BOT_009_p1"
BATCH = "BATCH_009"
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


# =============================================================== 1. The Living World and Classification (5/7/6)
direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "In the NCERT table of some organisms with their taxonomic categories, the housefly (Musca domestica) is "
       "placed in the phylum:",
       "Arthropoda",
       ["Chordata", "Insecta", "Diptera"], "A",
       "Taxonomic categories of the housefly",
       "NCERT's table gives the housefly as: genus Musca, family Muscidae, order Diptera, class Insecta, phylum "
       "Arthropoda, kingdom Animalia.",
       ["Housefly: Musca - Muscidae - Diptera - Insecta - Arthropoda - Animalia", "Phylum = Arthropoda"],
       why="Chordata is the phylum of man in the same table. Insecta is the housefly's class and Diptera its order, "
           "not its phylum.",
       ncert=ref("LW", "Taxonomic categories (table of organisms with their taxonomic categories)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "In fungi, the body consists of long, slender, thread-like structures called hyphae. The network of hyphae is "
       "known as:",
       "mycelium",
       ["conidiophore", "basidiocarp", "ascocarp"], "B",
       "Body of a fungus",
       "With the exception of yeasts, which are unicellular, fungi are filamentous. Their bodies consist of long, "
       "slender, thread-like structures called hyphae, and the network of hyphae is known as mycelium.",
       ["Thread-like unit = hypha", "Network of hyphae = mycelium"],
       why="A conidiophore is the special mycelium on which conidia are produced. Basidiocarps and ascocarps are "
           "fruiting bodies of basidiomycetes and ascomycetes.",
       ncert=ref("BC", "Kingdom Fungi"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "NCERT credits chemosynthetic autotrophic bacteria with playing a great role in:",
       "recycling nutrients such as nitrogen, phosphorus, iron and sulphur",
       ["producing methane (biogas) from the dung of ruminant animals",
        "fixing atmospheric nitrogen in specialised cells called heterocysts",
        "making curd from milk"], "B",
       "Role of chemosynthetic bacteria",
       "Chemosynthetic autotrophic bacteria oxidise various inorganic substances such as nitrates, nitrites and "
       "ammonia and use the released energy for their ATP production. They play a great role in recycling nutrients "
       "like nitrogen, phosphorus, iron and sulphur.",
       ["Chemosynthetic bacteria: energy from oxidising inorganic substances", "Role: recycling of N, P, Fe and S"],
       why="Methane is produced by methanogens (archaebacteria). Heterocysts are found in cyanobacteria such as "
           "Nostoc and Anabaena. Curd is made by heterotrophic bacteria.",
       ncert=ref("BC", "Kingdom Monera (eubacteria)"), secs=25)

statement_pair(T_LIV, "What is living", "Basic",
               "Plants respond to external factors such as light, water, temperature, other organisms and pollutants.",
               "If increase in body mass is taken as the criterion for growth, non-living objects cannot be said to "
               "grow.",
               True, False, "C",
               "Response to stimuli; growth as a criterion",
               "All organisms can sense and respond to environmental cues; plants respond to external factors like "
               "light, water, temperature, other organisms and pollutants. NCERT points out that non-living objects "
               "also grow if increase in body mass is taken as the criterion: mountains, boulders and sand mounds "
               "grow, though by accumulation of material on the surface.",
               ["Statement I: true", "Statement II: false; by the body-mass criterion, non-living objects also grow"],
               ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=30)

direct(T_LIV, "Five kingdom classification", "Basic",
       "According to NCERT, members of kingdom Animalia store their food reserves as:",
       "glycogen or fat",
       ["starch", "cellulose", "chitin"], "D",
       "Food reserves of animals",
       "Members of Animalia are heterotrophic, eukaryotic, multicellular organisms whose cells lack cell walls. They "
       "directly or indirectly depend on plants for food, digest their food in an internal cavity and store food "
       "reserves as glycogen or fat.",
       ["Animalia: holozoic nutrition", "Food reserve: glycogen or fat"],
       why="Starch is the food reserve of plants. Cellulose is a plant cell-wall material and chitin is found in fungal "
           "cell walls; neither is the stored food of animals.",
       ncert=ref("BC", "Kingdom Animalia"), secs=20)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate", "fungus", "kind of sexual spore",
           ["Rhizopus", "Claviceps", "Puccinia", "Alternaria"],
           ["Basidiospores", "Sexual stage not known", "Zygospores", "Ascospores"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A",
           "Classes of fungi and their sexual spores",
           "Rhizopus (the bread mould) is a phycomycete, in which a zygospore is formed by the fusion of two gametes. "
           "Claviceps is an ascomycete; its sexual spores, ascospores, are produced endogenously in asci. Puccinia "
           "(wheat rust) is a basidiomycete, which forms basidiospores on the basidium. Alternaria is a "
           "deuteromycete, a group in which only the asexual or vegetative phases are known.",
           ["Rhizopus: phycomycete -> zygospore", "Claviceps: ascomycete -> ascospores",
            "Puccinia: basidiomycete -> basidiospores", "Alternaria: deuteromycete -> no known sexual stage"],
           why="The wrong codes swap the phycomycete and the ascomycete, the basidiomycete and the deuteromycete, or "
               "the ascomycete and the basidiomycete.",
           ncert=ref("BC", "Kingdom Fungi (Phycomycetes, Ascomycetes, Basidiomycetes, Deuteromycetes)"), secs=45)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Yeast is a unicellular fungus.",
                 "All members of the class Ascomycetes are unicellular.",
                 True, False, False, "C",
                 "Unicellular and multicellular ascomycetes",
                 "With the exception of yeasts, which are unicellular, fungi are filamentous. The ascomycetes are "
                 "mostly multicellular (e.g. Penicillium) and only rarely unicellular (e.g. yeast, Saccharomyces).",
                 ["A: true", "R: false; ascomycetes are mostly multicellular, rarely unicellular"],
                 ncert=ref("BC", "Kingdom Fungi (Ascomycetes)"), secs=35)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about archaebacteria are correct?",
                [("They differ from other bacteria in having a different cell wall structure.", True),
                 ("Methanogens among them are present in the guts of several ruminant animals such as cows and "
                  "buffaloes.", True),
                 ("The halophiles among them live in hot springs.", False),
                 ("The cyanobacteria (blue-green algae) belong to this group.", False)],
                [("a", "b", "c"), ("b", "d"), ("a", "c", "d")], "B",
                "Archaebacteria",
                "Archaebacteria live in some of the harshest habitats: extreme salty areas (halophiles), hot springs "
                "(thermoacidophiles) and marshy areas (methanogens). They differ from other bacteria in having a "
                "different cell wall structure, which is responsible for their survival in extreme conditions. "
                "Methanogens are present in the guts of several ruminant animals such as cows and buffaloes and are "
                "responsible for the production of methane (biogas) from their dung. Cyanobacteria are described by "
                "NCERT under the eubacteria ('true bacteria').",
                ["(a) true", "(b) true", "(c) false; hot springs = thermoacidophiles; halophiles = salty areas",
                 "(d) false; cyanobacteria are eubacteria"],
                ncert=ref("BC", "Kingdom Monera (archaebacteria, eubacteria)"), secs=50)

statement_pair(T_LIV, "Five kingdom classification", "Intermediate",
               "The cell body of a protist contains a well-defined nucleus and other membrane-bound organelles.",
               "Some protists have flagella or cilia.",
               True, True, "A",
               "Protistan cells",
               "All members of Protista are eukaryotes. The protistan cell body contains a well-defined nucleus and other "
               "membrane-bound organelles, and some have flagella or cilia.",
               ["Statement I: true (protists are eukaryotes)", "Statement II: true"],
               ncert=ref("BC", "Kingdom Protista"), secs=30)

direct(T_LIV, "Lichens, viruses and viroids", "Intermediate",
       "Which of the following is true of both viruses and viroids, but NOT of prions?",
       "They contain nucleic acid as their genetic material.",
       ["They have a protein coat around the nucleic acid.", "They consist of abnormally folded protein.",
        "They contain both DNA and RNA."], "D",
       "Comparing viruses, viroids and prions",
       "Viruses contain genetic material that is either RNA or DNA, within a protein capsid. A viroid is a free RNA "
       "that lacks the protein coat found in viruses. Prions are infectious agents consisting of abnormally folded "
       "protein. So only viruses and viroids carry nucleic acid as genetic material.",
       ["Virus: RNA or DNA + protein coat", "Viroid: free RNA, no protein coat", "Prion: abnormally folded protein"],
       why="Viroids lack the protein coat. Abnormally folded protein describes prions. No virus contains both DNA and "
           "RNA, and a viroid has only RNA.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)

direct(T_LIV, "What is living", "Intermediate",
       "Taking all the properties of life together, NCERT describes living organisms as:",
       "self-replicating, evolving and self-regulating interactive systems capable of responding to external stimuli",
       ["isolated metabolic reactions that can be demonstrated in a test tube",
        "systems that grow only by the accumulation of material on their surface",
        "systems defined by reproduction, so that a non-reproducing organism is non-living"], "D",
       "What is living",
       "NCERT concludes that living organisms are self-replicating, evolving and self-regulating interactive systems "
       "capable of responding to external stimuli. Isolated metabolic reactions in vitro are not living things, "
       "though they are surely living reactions. Growth by accumulation on the surface is how non-living objects "
       "grow. Reproduction is not an all-inclusive defining feature, since many organisms (mules, sterile worker bees, "
       "infertile couples) do not reproduce.",
       ["Living organisms = self-replicating, evolving, self-regulating interactive systems",
        "They respond to external stimuli"],
       why="In vitro reactions are not living things; surface accumulation is non-living growth; reproduction cannot "
           "be an all-inclusive defining characteristic.",
       ncert=ref("LW", "Diversity in the Living World (what is living)"), secs=35)

_mango = ["Mangifera", "Anacardiaceae", "Sapindales", "Dicotyledonae", "Angiospermae"]
numerical(T_LIV, "Taxonomy and hierarchy", "Intermediate",
          "In the NCERT table of organisms with their taxonomic categories, how many taxonomic categories of mango "
          "lie between its genus Mangifera and its division Angiospermae (both excluded)?",
          "3", ["2", "4", "5"], "A",
          len(_mango[1:-1]) == 3,
          "Taxonomic hierarchy of mango",
          "Mango: genus Mangifera, family Anacardiaceae, order Sapindales, class Dicotyledonae, division Angiospermae. "
          "Between the genus and the division (both excluded) lie the family, the order and the class.",
          ["Hierarchy: genus - family - order - class - division", "Between genus and division: family, order, class",
           "Count = 3"],
          why="2 leaves out one category (usually the class); 4 counts the genus or the division as well; 5 counts the "
              "whole list including both ends.",
          ncert=ref("LW", "Taxonomic categories (table of organisms with their taxonomic categories)"), secs=40)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following organisms are eukaryotic and can carry out photosynthesis?",
                [("Chlamydomonas", True), ("Nostoc", False), ("Chlorella", True),
                 ("Euglena (in the presence of sunlight)", True), ("Mucor", False)],
                [("a", "b", "c", "d"), ("b", "c", "d"), ("a", "d", "e")], "C",
                "Eukaryotic photosynthetic organisms",
                "Chlamydomonas and Chlorella are green algae (placed in Protista in the five kingdom system) and are "
                "photosynthetic eukaryotes. Euglena is a protist that is photosynthetic in the presence of sunlight. "
                "Nostoc is a cyanobacterium: photosynthetic but prokaryotic (Monera). Mucor is a fungus: eukaryotic but "
                "heterotrophic.",
                ["(a) eukaryote, photosynthetic", "(b) prokaryote", "(c) eukaryote, photosynthetic",
                 "(d) eukaryote, photosynthetic in sunlight", "(e) heterotrophic fungus"],
                why="Any option with (b) includes a prokaryote; an option with (e) includes a heterotrophic fungus.",
                ncert=ref("BC", "Kingdom Monera; Kingdom Protista; Kingdom Fungi"), secs=60)

assertion_reason(T_LIV, "Five kingdom classification", "Advanced",
                 "Nostoc and Chlamydomonas, though both photosynthetic, are placed in different kingdoms in the five "
                 "kingdom classification.",
                 "Cell structure (prokaryotic or eukaryotic) is one of the main criteria used by Whittaker to "
                 "separate kingdoms.",
                 True, True, True, "A",
                 "Criteria of the five kingdom system",
                 "Whittaker's main criteria were cell structure, body organisation, mode of nutrition, reproduction and "
                 "phylogenetic relationships. Nostoc is prokaryotic and goes to Monera; Chlamydomonas is a eukaryote "
                 "and goes to Protista. The same mode of nutrition does not keep them together because they differ in "
                 "cell structure.",
                 ["A: true (Monera vs Protista)", "R: true", "The prokaryotic/eukaryotic difference is why they are "
                  "separated, so R explains A"],
                 ncert=ref("BC", "Introduction (five kingdom classification); Kingdom Monera; Kingdom Protista"),
                 secs=45)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Advanced",
               "In ascomycetes, both the asexual spores (conidia) and the sexual spores (ascospores) are produced "
               "exogenously.",
               "In deuteromycetes, the mycelium is septate and branched.",
               False, True, "D",
               "Spore formation in ascomycetes; mycelium of deuteromycetes",
               "In ascomycetes the asexual spores, conidia, are produced exogenously on special mycelium called "
               "conidiophores, but the sexual spores, ascospores, are produced endogenously in sac-like asci. "
               "Deuteromycetes reproduce only by asexual spores (conidia), and their mycelium is septate and branched.",
               ["Statement I: false; ascospores are endogenous", "Statement II: true"],
               ncert=ref("BC", "Kingdom Fungi (Ascomycetes, Deuteromycetes)"), secs=40)

direct(T_LIV, "Monera, Protista and Fungi", "Advanced",
       "In some fungi, an intervening dikaryotic stage (n + n) occurs between plasmogamy and karyogamy. In which of the "
       "following pairs can BOTH fungi show this stage?",
       "Claviceps and Agaricus",
       ["Mucor and Albugo", "Alternaria and Trichoderma", "Rhizopus and Puccinia"], "B",
       "Dikaryophase in fungi",
       "The dikaryotic stage occurs in ascomycetes and basidiomycetes. Claviceps is an ascomycete and Agaricus a "
       "basidiomycete, so both can show it. Mucor, Albugo and Rhizopus are phycomycetes; Alternaria and Trichoderma "
       "are deuteromycetes, whose sexual stages are not known.",
       ["Dikaryon: ascomycetes and basidiomycetes", "Claviceps = ascomycete; Agaricus = basidiomycete"],
       why="Mucor and Albugo are both phycomycetes; Alternaria and Trichoderma are deuteromycetes with no known sexual "
           "stage; in the last pair Rhizopus is a phycomycete.",
       ncert=ref("BC", "Kingdom Fungi"), secs=50)

match_list(T_LIV, "Monera, Protista and Fungi", "Advanced", "group", "asexual reproduction as described in NCERT",
           ["Phycomycetes", "Ascomycetes", "Basidiomycetes", "Bacteria"],
           ["Mainly by fission; spores may form under unfavourable conditions",
            "Motile zoospores or non-motile aplanospores formed endogenously in a sporangium",
            "Asexual spores generally not found; fragmentation common",
            "Conidia produced exogenously on conidiophores"],
           "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "D",
           "Asexual reproduction in fungi and bacteria",
           "Phycomycetes reproduce asexually by zoospores (motile) or aplanospores (non-motile), produced endogenously "
           "in a sporangium. Ascomycetes form conidia exogenously on conidiophores. In basidiomycetes asexual spores are "
           "generally not found, but vegetative reproduction by fragmentation is common. Bacteria reproduce mainly by "
           "fission; under unfavourable conditions they may produce spores.",
           ["Phycomycetes -> II", "Ascomycetes -> IV", "Basidiomycetes -> III", "Bacteria -> I"],
           why="The wrong codes exchange the endogenous and exogenous spores of phycomycetes and ascomycetes, give "
               "basidiomycetes the bacterial mode, or give them conidia.",
           ncert=ref("BC", "Kingdom Monera; Kingdom Fungi"), secs=60)

assertion_reason(T_LIV, "Lichens, viruses and viroids", "Advanced",
                 "Viroids are larger than viruses.",
                 "The RNA of a viroid is of low molecular weight.",
                 False, True, False, "D",
                 "Size of viroids",
                 "In 1971, T.O. Diener discovered a new infectious agent that was smaller than viruses and caused "
                 "potato spindle tuber disease. It was a free RNA lacking the protein coat found in viruses, hence the "
                 "name viroid. The RNA of the viroid was of low molecular weight.",
                 ["A: false; viroids are smaller than viruses", "R: true"],
                 ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)

# =============================================================== 2. Plant Kingdom (6/7/6)
direct(T_PK, "Algae", "Basic",
       "The plant body of a brown alga is usually attached to the substratum by a holdfast and has a stalk, the stipe. "
       "Its leaf-like photosynthetic organ is called the:",
       "frond",
       ["thallus", "rhizoid", "sporophyll"], "B",
       "Plant body of brown algae",
       "In Phaeophyceae the plant body is usually attached to the substratum by a holdfast, and has a stalk, the stipe, "
       "and a leaf-like photosynthetic organ, the frond.",
       ["Holdfast = attachment", "Stipe = stalk", "Frond = leaf-like photosynthetic organ"],
       why="Thallus is the general term for an undifferentiated plant body. Rhizoids attach bryophytes, not brown "
           "algae. A sporophyll is a leaf-like appendage bearing sporangia in pteridophytes and gymnosperms.",
       ncert=ref("PK", "Algae (Phaeophyceae)"), secs=20)

direct(T_PK, "Algae", "Basic",
       "NCERT divides algae into three main classes. Which of the following is NOT one of them?",
       "Chrysophyceae",
       ["Chlorophyceae", "Phaeophyceae", "Rhodophyceae"], "B",
       "Classes of algae",
       "Algae are divided into three main classes: Chlorophyceae (green algae), Phaeophyceae (brown algae) and "
       "Rhodophyceae (red algae). Chrysophytes (diatoms and golden algae) are placed by NCERT in kingdom Protista, "
       "not among these classes.",
       ["Three classes: Chlorophyceae, Phaeophyceae, Rhodophyceae"],
       why="The other three options are exactly the three main classes of algae named in NCERT.",
       ncert=ref("PK", "Algae"), secs=20)

direct(T_PK, "Pteridophytes", "Basic",
       "In a pteridophyte, the zygote formed after fusion of the male gamete with the egg in the archegonium develops "
       "into:",
       "a multicellular, well-differentiated sporophyte, which is the dominant phase",
       ["a prothallus, which is the dominant phase", "a protonema, from which leafy shoots arise",
        "a female gametophyte retained within the megasporangium"], "B",
       "Fate of the zygote in pteridophytes",
       "The gametophytes bear antheridia and archegonia. Water carries the antherozoids to the mouth of the "
       "archegonium, and fusion of a male gamete with the egg forms the zygote. The zygote then produces a "
       "multicellular, well-differentiated sporophyte, which is the dominant phase of pteridophytes.",
       ["Male gamete + egg -> zygote", "Zygote -> sporophyte (dominant phase)"],
       why="The prothallus is the gametophyte, formed from a spore and not the dominant phase. The protonema belongs to "
           "mosses. A female gametophyte develops from a megaspore, not from the zygote.",
       ncert=ref("PK", "Pteridophytes"), secs=25)

statement_pair(T_PK, "Gymnosperms", "Basic",
               "The leaves of gymnosperms may be simple or compound.",
               "In gymnosperms, the male and female gametophytes remain within the sporangia retained on the "
               "sporophytes.",
               True, True, "A",
               "Leaves and gametophytes of gymnosperms",
               "In gymnosperms the leaves may be simple or compound; in Cycas the pinnate leaves persist for a few "
               "years. Unlike bryophytes and pteridophytes, the male and female gametophytes of gymnosperms do not "
               "have an independent free-living existence; they remain within the sporangia retained on the "
               "sporophytes.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Gymnosperms"), secs=30)

match_list(T_PK, "Pteridophytes", "Basic", "term", "meaning in pteridophytes",
           ["Sporophyll", "Strobilus", "Prothallus", "Microphyll"],
           ["Small leaf, as in Selaginella", "Leaf-like appendage that subtends sporangia",
            "Compact structure formed by sporophylls", "Small, free-living, mostly photosynthetic thalloid gametophyte"],
           "II III IV I", ["III II IV I", "II III I IV", "II IV III I"], "B",
           "Terms used for pteridophytes",
           "The pteridophyte sporophyte bears sporangia subtended by leaf-like appendages called sporophylls. In some "
           "(Selaginella, Equisetum) the sporophylls form distinct compact structures called strobili or cones. The "
           "spores germinate into small, multicellular, free-living, mostly photosynthetic thalloid gametophytes "
           "called prothalli. Small leaves, as in Selaginella, are microphylls; large ones, as in ferns, are "
           "macrophylls.",
           ["Sporophyll -> II", "Strobilus -> III", "Prothallus -> IV", "Microphyll -> I"],
           why="The wrong codes exchange sporophyll and strobilus, prothallus and microphyll, or strobilus and "
               "prothallus.",
           ncert=ref("PK", "Pteridophytes"), secs=35)

direct(T_PK, "Algae", "Basic",
       "Which of the following is a green alga (Chlorophyceae)?",
       "Chara",
       ["Dictyota", "Polysiphonia", "Gracilaria"], "D",
       "Examples of green algae",
       "NCERT's examples of Chlorophyceae are Chlamydomonas, Volvox, Ulothrix, Spirogyra and Chara. Dictyota is a brown "
       "alga, while Polysiphonia and Gracilaria are red algae.",
       ["Green algae: Chlamydomonas, Volvox, Ulothrix, Spirogyra, Chara"],
       why="Dictyota belongs to Phaeophyceae; Polysiphonia and Gracilaria belong to Rhodophyceae.",
       ncert=ref("PK", "Algae (Chlorophyceae)"), secs=20)

multi_statement(T_PK, "Algae", "Intermediate",
                "Which of the following statements are true of BOTH brown algae (Phaeophyceae) and red algae "
                "(Rhodophyceae)?",
                [("The majority of members are marine.", True),
                 ("Some members produce hydrocolloids (water-holding substances) that are used commercially.", True),
                 ("Their motile cells bear two unequal, lateral flagella.", False),
                 ("Chlorophyll a is present.", True),
                 ("Food is stored as floridean starch.", False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "d")], "A",
                "Comparing brown and red algae",
                "Brown algae are found primarily in marine habitats, and the majority of red algae are marine. Certain "
                "marine brown and red algae produce large amounts of hydrocolloids: algin (brown algae) and carrageen "
                "(red algae), used commercially. Chlorophyll a is present in both. Two unequal lateral flagella occur "
                "only in brown algae; red algae have no flagella. Floridean starch is the food of red algae only; "
                "brown algae store mannitol or laminarin.",
                ["(a) true for both", "(b) true for both (algin; carrageen)", "(c) brown only",
                 "(d) true for both", "(e) red only"],
                ncert=ref("PK", "Algae (Phaeophyceae, Rhodophyceae; table of divisions of algae)"), secs=60)

statement_pair(T_PK, "Algae", "Intermediate",
               "In Chlorophyceae, sexual reproduction may be isogamous, anisogamous or oogamous.",
               "In Rhodophyceae, sexual reproduction may be isogamous, anisogamous or oogamous.",
               True, False, "C",
               "Sexual reproduction in green and red algae",
               "In green algae, sexual reproduction shows considerable variation in the type and formation of sex "
               "cells, and it may be isogamous, anisogamous or oogamous. In red algae, sexual reproduction (by "
               "non-motile gametes) is oogamous and is accompanied by complex post-fertilisation developments.",
               ["Statement I: true", "Statement II: false; red algae are oogamous"],
               ncert=ref("PK", "Algae (Chlorophyceae, Rhodophyceae)"), secs=35)

direct(T_PK, "Bryophytes", "Intermediate",
       "According to NCERT, which of the following is a feature of mosses that is NOT described for liverworts?",
       "A protonema stage of the gametophyte that develops directly from a spore",
       ["Asexual reproduction by gemmae formed in gemma cups", "A sporophyte differentiated into foot, seta and capsule",
        "Multicellular sex organs"], "C",
       "Mosses compared with liverworts",
       "The moss gametophyte has two stages: the protonema, a creeping, green, branched, frequently filamentous stage "
       "that develops directly from a spore, and the leafy stage, which develops from the secondary protonema as a "
       "lateral bud. Liverworts have a thalloid or leafy gametophyte with no protonema stage described. Gemmae in "
       "gemma cups are a liverwort feature; a sporophyte with foot, seta and capsule and multicellular sex organs "
       "are found in both.",
       ["Protonema: mosses", "Gemma cups: liverworts", "Foot-seta-capsule and multicellular sex organs: both"],
       why="Gemmae in gemma cups are described for liverworts. The liverwort sporophyte is also differentiated into "
           "foot, seta and capsule. All bryophytes have multicellular sex organs.",
       ncert=ref("PK", "Bryophytes (liverworts, mosses)"), secs=40)

match_list(T_PK, "Algae", "Intermediate", "plant", "use described in NCERT",
           ["Sphagnum", "Gelidium", "Chlorella", "Porphyra"],
           ["Marine alga used as food", "Source of agar", "Peat, used as fuel",
            "Protein-rich food supplement, used even by space travellers"],
           "III II IV I", ["II III IV I", "III II I IV", "III IV II I"], "D",
           "Economic importance of algae and bryophytes",
           "Species of the moss Sphagnum provide peat, which has long been used as fuel. Agar, used to grow microbes and "
           "in ice-creams and jellies, is obtained from Gelidium and Gracilaria. Chlorella, a unicellular alga rich in "
           "proteins, is used as a food supplement even by space travellers. Porphyra is one of the marine algae "
           "used as food.",
           ["Sphagnum -> peat", "Gelidium -> agar", "Chlorella -> food supplement", "Porphyra -> food"],
           why="The wrong codes swap Sphagnum and Gelidium, Chlorella and Porphyra, or Gelidium and Chlorella.",
           ncert=ref("PK", "Algae; Bryophytes"), secs=40)

assertion_reason(T_PK, "Bryophytes", "Intermediate",
                 "In liverworts, the male and female sex organs are produced either on the same thallus or on "
                 "different thalli.",
                 "The sporophyte of a liverwort is free-living and independent of the gametophyte.",
                 True, False, False, "C",
                 "Sex organs and sporophyte of liverworts",
                 "During sexual reproduction in liverworts, male and female sex organs are produced either on the same "
                 "or on different thalli. The sporophyte, differentiated into foot, seta and capsule, is not "
                 "free-living: in bryophytes it remains attached to the photosynthetic gametophyte and derives "
                 "nourishment from it.",
                 ["A: true", "R: false; the bryophyte sporophyte depends on the gametophyte"],
                 ncert=ref("PK", "Bryophytes (liverworts)"), secs=35)

_mmc = 6
numerical(T_PK, "Gymnosperms", "Intermediate",
          "In a gymnosperm, each ovule has one megaspore mother cell. If the megaspore mother cells of 6 ovules "
          "complete their division, how many megaspores are formed in all, and how many of these develop into female "
          "gametophytes?",
          "24 megaspores; 6 female gametophytes",
          ["24 megaspores; 24 female gametophytes", "12 megaspores; 6 female gametophytes",
           "6 megaspores; 6 female gametophytes"], "A",
          _mmc * 4 == 24 and _mmc * 1 == 6,
          "Megasporogenesis in gymnosperms",
          "The megaspore mother cell is differentiated from one of the cells of the nucellus and divides meiotically to "
          "form four megaspores. One of the megaspores enclosed within the megasporangium develops into a "
          "multicellular female gametophyte bearing two or more archegonia.",
          ["Megaspores = 6 x 4 = 24 (meiosis gives four)", "Female gametophytes = 6 x 1 = 6 (one megaspore each)"],
          why="24 gametophytes assumes every megaspore develops; 12 treats the division as giving two cells; 6 "
              "megaspores ignores that meiosis gives four.",
          ncert=ref("PK", "Gymnosperms"), secs=50)

direct(T_PK, "Pteridophytes", "Intermediate",
       "Which of the following pairs of pteridophytes belong to the same class?",
       "Selaginella and Lycopodium",
       ["Psilotum and Equisetum", "Equisetum and Adiantum", "Selaginella and Dryopteris"], "B",
       "Classes of pteridophytes",
       "NCERT divides pteridophytes into four classes: Psilopsida (Psilotum), Lycopsida (Selaginella, Lycopodium), "
       "Sphenopsida (Equisetum) and Pteropsida (Dryopteris, Pteris, Adiantum). Selaginella and Lycopodium are both "
       "Lycopsida.",
       ["Lycopsida: Selaginella, Lycopodium"],
       why="Psilotum (Psilopsida) and Equisetum (Sphenopsida) differ; Equisetum and Adiantum (Pteropsida) differ; "
           "Selaginella (Lycopsida) and Dryopteris (Pteropsida) differ.",
       ncert=ref("PK", "Pteridophytes"), secs=35)

statement_pair(T_PK, "Algae", "Advanced",
               "Members of both Chlorophyceae and Phaeophyceae have motile cells, but their flagella differ: 2-8, equal "
               "and apical in the former, and 2, unequal and lateral in the latter.",
               "Like the red algae, members of Phaeophyceae store their food as floridean starch.",
               True, False, "C",
               "Flagella and stored food in algae",
               "NCERT's table of the divisions of algae gives Chlorophyceae 2-8 equal, apical flagella and "
               "Phaeophyceae 2 unequal, lateral flagella; Rhodophyceae have none. Stored food is starch in "
               "Chlorophyceae, mannitol or laminarin in Phaeophyceae and floridean starch in Rhodophyceae.",
               ["Statement I: true", "Statement II: false; brown algae store mannitol or laminarin"],
               ncert=ref("PK", "Algae (table of divisions of algae and their main characteristics)"), secs=40)

match_list(T_PK, "Gymnosperms", "Advanced", "feature", "plant group",
           ["Naked seeds", "First terrestrial plants with xylem and phloem",
            "Sporophyte attached to, and nourished by, the gametophyte",
            "Flagellated zoospores as the most common asexual spores"],
           ["Algae", "Bryophytes", "Pteridophytes", "Gymnosperms"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "C",
           "Distinguishing features of plant groups",
           "Gymnosperms have ovules not enclosed by an ovary wall, so the seeds are naked. Pteridophytes are, "
           "evolutionarily, the first terrestrial plants to possess vascular tissues, xylem and phloem. In bryophytes "
           "the sporophyte is not free-living; it is attached to the photosynthetic gametophyte and derives "
           "nourishment from it. In algae the most common asexual spores are the flagellated zoospores.",
           ["Naked seeds -> gymnosperms", "First vascular land plants -> pteridophytes",
            "Dependent sporophyte -> bryophytes", "Zoospores -> algae"],
           why="The wrong codes swap the gymnosperms and pteridophytes, the bryophytes and algae, or the pteridophytes "
               "and bryophytes.",
           ncert=ref("PK", "Algae; Bryophytes; Pteridophytes; Gymnosperms"), secs=50)

assertion_reason(T_PK, "Gymnosperms", "Advanced",
                 "Since gymnosperms are heterosporous, their megaspores are shed and germinate in the soil into "
                 "free-living female gametophytes.",
                 "In gymnosperms, the megaspore mother cell divides meiotically to form four megaspores.",
                 False, True, False, "D",
                 "Female gametophyte of gymnosperms",
                 "Gymnosperms are heterosporous. The megaspore mother cell, differentiated from a nucellus cell, divides "
                 "meiotically to form four megaspores. One megaspore, enclosed within the megasporangium, develops into "
                 "the multicellular female gametophyte, which is retained within the megasporangium; it is not shed "
                 "and is not free-living.",
                 ["A: false; the female gametophyte develops within the megasporangium", "R: true"],
                 ncert=ref("PK", "Gymnosperms"), secs=45)

direct(T_PK, "Bryophytes", "Advanced",
       "Which sequence correctly shows the development of a moss from a spore up to the formation of sex organs?",
       "Spore -> protonema -> lateral bud on the secondary protonema -> leafy stage -> antheridia and archegonia at the "
       "apex of the leafy shoots",
       ["Spore -> leafy stage -> protonema -> antheridia and archegonia on the protonema",
        "Spore -> prothallus -> leafy stage -> antheridia and archegonia on the prothallus",
        "Spore -> protonema -> capsule -> leafy stage -> antheridia and archegonia on the capsule"], "D",
       "Gametophyte of mosses",
       "The protonema develops directly from a spore; it is a creeping, green, branched, frequently filamentous stage. "
       "The leafy stage develops from the secondary protonema as a lateral bud and bears spirally arranged leaves. "
       "The sex organs, antheridia and archegonia, are produced at the apex of the leafy shoots.",
       ["Spore -> protonema", "Secondary protonema -> lateral bud -> leafy stage", "Sex organs at the shoot apex"],
       why="The leafy stage comes after, not before, the protonema. A prothallus is a pteridophyte gametophyte. The "
           "capsule is part of the sporophyte, formed after fertilisation.",
       ncert=ref("PK", "Bryophytes (mosses)"), secs=50)

direct(T_PK, "Algae", "Advanced",
       "Which of the following alga - stored food pairs is INCORRECT?",
       "Fucus - floridean starch",
       ["Porphyra - floridean starch", "Laminaria - mannitol or laminarin", "Chara - starch"], "A",
       "Stored food of the classes of algae",
       "Stored food: Chlorophyceae, starch; Phaeophyceae, mannitol or laminarin; Rhodophyceae, floridean starch. "
       "Porphyra is a red alga, Laminaria and Fucus are brown algae, and Chara is a green alga. Fucus, being brown, "
       "stores mannitol or laminarin, not floridean starch.",
       ["Identify each alga's class", "Apply the class's stored food", "Fucus (brown) - floridean starch is wrong"],
       why="Porphyra (red) does store floridean starch; Laminaria (brown) stores mannitol or laminarin; Chara (green) "
           "stores starch.",
       ncert=ref("PK", "Algae (table of divisions of algae and their main characteristics)"), secs=45)

assertion_reason(T_PK, "Pteridophytes", "Advanced",
                 "In Equisetum, the sporophylls are compactly arranged to form strobili.",
                 "Equisetum belongs to the class Lycopsida.",
                 True, False, False, "C",
                 "Strobili and classes of pteridophytes",
                 "In some pteridophytes the sporophylls form distinct compact structures called strobili or cones, as "
                 "in Selaginella and Equisetum. Equisetum belongs to Sphenopsida; Lycopsida includes Selaginella and "
                 "Lycopodium.",
                 ["A: true", "R: false; Equisetum is in Sphenopsida"],
                 ncert=ref("PK", "Pteridophytes"), secs=35)

# =============================================================== 3. Morphology of Flowering Plants (6/7/6)
direct(T_MOR, "Flower", "Basic",
       "Of the four whorls of a typical flower, which are described by NCERT as the reproductive organs?",
       "Androecium and gynoecium",
       ["Calyx and corolla", "Calyx and androecium", "Corolla and gynoecium"], "B",
       "Accessory and reproductive whorls",
       "A typical flower has four whorls: calyx, corolla, androecium and gynoecium. Calyx and corolla are accessory "
       "organs, while androecium and gynoecium are reproductive organs.",
       ["Accessory organs: calyx, corolla", "Reproductive organs: androecium, gynoecium"],
       why="Calyx and corolla are accessory organs; each of the other wrong pairs contains one accessory whorl.",
       ncert=ref("MOR", "The Flower"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "According to NCERT, the main function of the stem is:",
       "spreading out branches bearing leaves, flowers and fruits",
       ["absorption of water and minerals from the soil", "protecting the flower in the bud stage",
        "anchoring the plant parts firmly in the soil"], "B",
       "Functions of the stem",
       "The main function of the stem is spreading out branches bearing leaves, flowers and fruits. It conducts water, "
       "minerals and photosynthates. Some stems also store food, give support and protection, and help in vegetative "
       "propagation.",
       ["Main function: bearing and spreading out branches with leaves, flowers and fruits",
        "Also: conduction of water, minerals and photosynthates"],
       why="Absorption and anchorage are functions of the root system; protecting the flower in the bud is the "
           "function of the sepals.",
       ncert=ref("MOR", "The Stem"), secs=20)

statement_pair(T_MOR, "Plant families", "Basic",
               "In the family Fabaceae, the stem may be erect or a climber.",
               "Members of the family Solanaceae are mostly herbs and shrubs, and rarely small trees.",
               True, True, "A",
               "Habit in Fabaceae and Solanaceae",
               "In NCERT's description of Fabaceae, the stem is erect or climber. Solanaceae plants are mostly herbs, "
               "shrubs and rarely small trees; the stem is herbaceous, rarely woody.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "Description of Some Important Families (Fabaceae, Solanaceae)"), secs=30)

direct(T_MOR, "Inflorescence", "Basic",
       "The arrangement of flowers on the floral axis is termed:",
       "inflorescence",
       ["aestivation", "placentation", "phyllotaxy"], "D",
       "Inflorescence",
       "A flower is a modified shoot. The arrangement of flowers on the floral axis is termed inflorescence; depending "
       "on whether the apex grows into a flower or continues to grow, it is cymose or racemose.",
       ["Arrangement of flowers on the floral axis = inflorescence"],
       why="Aestivation is the arrangement of sepals or petals in a bud; placentation is the arrangement of ovules in "
           "the ovary; phyllotaxy is the arrangement of leaves on the stem or branch.",
       ncert=ref("MOR", "Inflorescence"), secs=20)

match_list(T_MOR, "Flower", "Basic", "term", "meaning",
           ["Pedicel", "Thalamus", "Bract", "Perianth"],
           ["Reduced leaf found at the base of the pedicel", "Calyx and corolla when they are not distinct",
            "Stalk of the flower", "Swollen end of the stalk on which the floral whorls are borne"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A",
           "Parts of a flower",
           "The four whorls of a typical flower are arranged successively on the swollen end of the stalk or pedicel, "
           "called the thalamus or receptacle. Flowers with a bract, a reduced leaf found at the base of the pedicel, "
           "are bracteate. When calyx and corolla are not distinct, as in lily, they are termed the perianth.",
           ["Pedicel -> stalk", "Thalamus -> swollen end bearing the whorls", "Bract -> reduced leaf at the pedicel base",
            "Perianth -> undifferentiated calyx and corolla"],
           why="The wrong codes swap pedicel and thalamus, bract and perianth, or pedicel and bract.",
           ncert=ref("MOR", "The Flower; Parts of a Flower"), secs=30)

direct(T_MOR, "Flower", "Basic",
       "Each carpel of the gynoecium is made up of:",
       "stigma, style and ovary",
       ["filament and anther", "stigma, style and placenta only", "ovary and pedicel"], "B",
       "Parts of a carpel",
       "The gynoecium is the female reproductive part of the flower and is made up of one or more carpels. A carpel "
       "consists of three parts, namely stigma, style and ovary. The ovary bears one or more ovules attached to a "
       "flattened, cushion-like placenta.",
       ["Carpel = stigma + style + ovary"],
       why="Filament and anther make a stamen. The placenta lies inside the ovary and is not a separate part replacing "
           "it. The pedicel is the stalk of the flower.",
       ncert=ref("MOR", "Parts of a Flower (gynoecium)"), secs=20)

match_list(T_MOR, "Flower", "Intermediate", "plant", "condition of the stamens",
           ["Pea", "Brinjal", "Lily", "China rose"],
           ["Epiphyllous", "Monoadelphous", "Diadelphous", "Epipetalous"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "C",
           "Union and attachment of stamens",
           "Stamens may be united among themselves or attached to other floral members. In pea they are in two bundles "
           "(diadelphous). In brinjal they are attached to the petals (epipetalous). In lily they are attached to the "
           "perianth (epiphyllous). In china rose they are united into one bundle (monoadelphous).",
           ["Pea -> diadelphous", "Brinjal -> epipetalous", "Lily -> epiphyllous", "China rose -> monoadelphous"],
           why="The wrong codes swap pea and brinjal, lily and china rose, or brinjal and lily.",
           ncert=ref("MOR", "Parts of a Flower (androecium)"), secs=40)

assertion_reason(T_MOR, "Plant families", "Intermediate",
                 "In the family Fabaceae, the fruit is a legume.",
                 "In the family Fabaceae, the leaf base is pulvinate.",
                 True, True, False, "B",
                 "Fruit and leaf base in Fabaceae",
                 "NCERT's description of Fabaceae gives the fruit as a legume and the seeds as one to many, "
                 "non-endospermic. Among the vegetative characters, the leaves are pinnately compound or simple, the "
                 "leaf base is pulvinate and stipulate. The swollen leaf base is a feature of the leaf and has nothing "
                 "to do with the kind of fruit formed from the ovary.",
                 ["A: true", "R: true", "R is a vegetative feature, unrelated to the fruit type"],
                 ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=35)

multi_statement(T_MOR, "Plant families", "Intermediate",
                "Which of the following plants belong to the family Solanaceae?",
                [("Belladonna", True), ("Muliathi", False), ("Petunia", True), ("Gloriosa", False),
                 ("Ashwagandha", True)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("c", "e")], "D",
                "Members of Solanaceae",
                "NCERT lists as Solanaceae: tomato, brinjal and potato (food), chilli (spice), belladonna and ashwagandha "
                "(medicine), tobacco (fumigatory) and petunia (ornamental). Muliathi is a medicinal plant of Fabaceae, "
                "and Gloriosa is an ornamental of Liliaceae.",
                ["(a) Solanaceae", "(b) Fabaceae", "(c) Solanaceae", "(d) Liliaceae", "(e) Solanaceae"],
                ncert=ref("MOR", "Description of Some Important Families (economic importance)"), secs=45)

statement_pair(T_MOR, "Plant families", "Intermediate",
               "In the family Liliaceae, the perianth shows valvate aestivation.",
               "In the family Fabaceae, the calyx shows valvate aestivation.",
               True, False, "C",
               "Aestivation in Liliaceae and Fabaceae",
               "In Liliaceae, the perianth has six tepals (3 + 3), often united into a tube, with valvate aestivation. In "
               "Fabaceae, the calyx has five gamosepalous sepals with imbricate aestivation, and the corolla shows "
               "vexillary aestivation.",
               ["Statement I: true", "Statement II: false; the Fabaceae calyx is imbricate"],
               ncert=ref("MOR", "Description of Some Important Families (Liliaceae, Fabaceae)"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "A plant has root nodules, stipulate pinnately compound leaves with a pulvinate leaf base, a racemose "
       "inflorescence and zygomorphic flowers with a papilionaceous corolla. Its seeds are expected to be:",
       "non-endospermic",
       ["endospermous, many in a berry or capsule", "endospermous, in a trilocular capsule",
        "endospermous, with a bulky endosperm separated from the embryo by an aleurone layer"], "A",
       "Identifying Fabaceae and its seed",
       "Root nodules, pulvinate stipulate leaves, racemose inflorescence and a papilionaceous corolla are the "
       "characters of Fabaceae. In Fabaceae the fruit is a legume and the seeds are one to many and non-endospermic.",
       ["Characters -> family Fabaceae", "Fabaceae seeds: non-endospermic"],
       why="Many endospermous seeds in a berry or capsule describe Solanaceae; endospermous seeds in a trilocular "
           "capsule describe Liliaceae; a bulky endosperm with an aleurone layer describes a cereal grain such as "
           "maize.",
       ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=40)

assertion_reason(T_MOR, "Flower", "Intermediate",
                 "In lotus and rose, the gynoecium is syncarpous.",
                 "In mustard and tomato, the carpels of the gynoecium are fused together.",
                 False, True, False, "D",
                 "Apocarpous and syncarpous gynoecium",
                 "When more than one carpel is present, they may be free, as in lotus and rose (apocarpous), or fused "
                 "together, as in mustard and tomato (syncarpous).",
                 ["A: false; lotus and rose are apocarpous", "R: true"],
                 ncert=ref("MOR", "Parts of a Flower (gynoecium)"), secs=30)

direct(T_MOR, "Flower", "Intermediate",
       "In a floral diagram, the calyx, corolla, androecium and gynoecium are drawn in successive whorls. Which whorl "
       "is drawn outermost and which in the centre?",
       "Calyx outermost; gynoecium in the centre",
       ["Gynoecium outermost; calyx in the centre", "Corolla outermost; androecium in the centre",
        "Androecium outermost; gynoecium in the centre"], "D",
       "Floral diagram",
       "A floral diagram gives information about the number of parts of a flower, their arrangement and their "
       "relation to one another. The position of the mother axis is shown by a dot on top of the diagram. Calyx, "
       "corolla, androecium and gynoecium are drawn in successive whorls, calyx being the outermost and gynoecium "
       "being in the centre.",
       ["Order from outside: calyx, corolla, androecium, gynoecium"],
       why="The other options reverse or misplace the order of the whorls.",
       ncert=ref("MOR", "Semi-technical Description of a Typical Flowering Plant"), secs=30)

multi_statement(T_MOR, "Plant families", "Advanced",
                "The floral formula of a family is % ⚥ K(5) C1+2+(2) A(9)+1 G1. Which of the following conclusions "
                "drawn from it are correct?",
                [("The flower is zygomorphic and bisexual.", True),
                 ("The calyx is gamosepalous.", True),
                 ("Two of the petals are united with each other.", True),
                 ("The gynoecium is syncarpous.", False),
                 ("All ten stamens are united into one bundle.", False)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d")], "B",
                "Reading the floral formula of Fabaceae",
                "% stands for a zygomorphic flower and ⚥ for bisexual. K(5): five united sepals (gamosepalous). "
                "C1+2+(2): one standard, two wings and two anterior petals united (the keel). A(9)+1: nine stamens "
                "united and one free (diadelphous). G1: a single carpel, so the gynoecium is monocarpellary, not "
                "syncarpous.",
                ["(a) true: % and ⚥", "(b) true: K(5)", "(c) true: (2) in the corolla",
                 "(d) false: G1 is a single carpel", "(e) false: (9) + 1 means nine united, one free"],
                ncert=ref("MOR", "Description of Some Important Families (Fabaceae); Semi-technical Description"),
                secs=70)

match_list(T_MOR, "Plant families", "Advanced", "family or plant", "gynoecium",
           ["Fabaceae", "Solanaceae", "Liliaceae", "Rose"],
           ["Tricarpellary, syncarpous, trilocular ovary with axile placentation",
            "Monocarpellary, unilocular ovary with many ovules",
            "Bicarpellary, obliquely placed, syncarpous, bilocular ovary with a swollen placenta",
            "Carpels free (apocarpous)"],
           "II III I IV", ["III II I IV", "II III IV I", "II I III IV"], "A",
           "Gynoecium of the families",
           "Fabaceae: ovary superior, monocarpellary, unilocular with many ovules, style single. Solanaceae: "
           "bicarpellary, obliquely placed, syncarpous; ovary superior, bilocular, placenta swollen with many ovules, "
           "axile. Liliaceae: tricarpellary, syncarpous, ovary superior, trilocular with many ovules, axile "
           "placentation. In rose the carpels are free (apocarpous).",
           ["Fabaceae -> II", "Solanaceae -> III", "Liliaceae -> I", "Rose -> IV"],
           why="The wrong codes swap Fabaceae and Solanaceae, Liliaceae and rose, or Solanaceae and Liliaceae.",
           ncert=ref("MOR", "Description of Some Important Families; Parts of a Flower (gynoecium)"), secs=60)

assertion_reason(T_MOR, "Plant families", "Advanced",
                 "In the floral formula of Solanaceae, a line is drawn above the symbols C and A, joining them.",
                 "In Solanaceae the stamens are epipetalous, and adhesion of floral parts is shown in a floral formula "
                 "by a line drawn above the symbols of those parts.",
                 True, True, True, "A",
                 "Adhesion in a floral formula",
                 "In a floral formula, fusion is indicated by enclosing the figure within brackets and adhesion by a "
                 "line drawn above the symbols of the floral parts. The five stamens of Solanaceae are epipetalous, "
                 "that is, adhered to the petals, so the C and A symbols in its formula are joined by such a line.",
                 ["A: true", "R: true", "Epipetaly is adhesion of A to C, which is drawn as the line; R explains A"],
                 ncert=ref("MOR", "Semi-technical Description; Description of Some Important Families (Solanaceae)"),
                 secs=45)

direct(T_MOR, "Flower", "Advanced",
       "In which of the following pairs do BOTH plants show the same type of placentation?",
       "Tomato and lemon",
       ["Pea and mustard", "Dianthus and sunflower", "Argemone and primrose"], "D",
       "Types of placentation",
       "Axile placentation, with ovules attached to a central placenta in a multilocular ovary, is seen in china "
       "rose, tomato and lemon. Pea has marginal placentation; mustard and Argemone parietal; Dianthus and primrose "
       "free central; sunflower and marigold basal.",
       ["Tomato = axile; lemon = axile"],
       why="Pea (marginal) and mustard (parietal) differ; Dianthus (free central) and sunflower (basal) differ; "
           "Argemone (parietal) and primrose (free central) differ.",
       ncert=ref("MOR", "Parts of a Flower (placentation)"), secs=45)

statement_pair(T_MOR, "Plant families", "Advanced",
               "In both Solanaceae and Liliaceae, the fruit may be a berry.",
               "In both Fabaceae and Solanaceae, the seeds are endospermous.",
               True, False, "C",
               "Fruits and seeds of the three families",
               "Solanaceae fruits are berries or capsules, and Liliaceae fruits are capsules, rarely berries, so a berry "
               "is possible in both. Seeds are endospermous in Solanaceae and Liliaceae, but non-endospermic in "
               "Fabaceae.",
               ["Statement I: true", "Statement II: false; Fabaceae seeds are non-endospermic"],
               ncert=ref("MOR", "Description of Some Important Families"), secs=45)

multi_statement(T_MOR, "Inflorescence", "Advanced",
                "Which of the following statements about the cymose type of inflorescence are correct?",
                [("The main axis terminates in a flower.", True),
                 ("The main axis is limited in growth.", True),
                 ("The flowers are borne in a basipetal order.", True),
                 ("It is the inflorescence of the family Fabaceae.", False),
                 ("In Liliaceae, the inflorescence may be cymose, often in umbellate clusters.", True)],
                [("a", "b", "c", "d"), ("a", "c", "d", "e"), ("b", "c", "e")], "D",
                "Cymose inflorescence",
                "In cymose inflorescence the main axis terminates in a flower and is therefore limited in growth; the "
                "flowers are borne in a basipetal order. Fabaceae has a racemose inflorescence. In Liliaceae the "
                "inflorescence is solitary or cymose, often in umbellate clusters.",
                ["(a), (b), (c) true", "(d) false; Fabaceae is racemose", "(e) true"],
                ncert=ref("MOR", "Inflorescence; Description of Some Important Families"), secs=55)

# =============================================================== 4. Anatomy of Flowering Plants (5/6/5)
direct(T_ANA, "Plant tissues", "Basic",
       "In the phloem of angiosperms, companion cells are:",
       "specialised parenchymatous cells closely associated with the sieve tube elements",
       ["dead sclerenchymatous cells with very thick, lignified walls",
        "the sieve cells found in the phloem of gymnosperms",
        "thin-walled xylem cells that store tannins"], "B",
       "Companion cells",
       "Companion cells are specialised parenchymatous cells closely associated with the sieve tube elements. The "
       "sieve tube elements and companion cells are connected by pit fields in their common longitudinal walls, and "
       "the nucleus of the companion cell controls the functions of the sieve tube, which lacks a nucleus at "
       "maturity.",
       ["Companion cell = specialised parenchyma cell beside a sieve tube element"],
       why="Dead, thick-walled lignified cells describe sclerenchyma (such as phloem fibres). Gymnosperms have sieve "
           "cells and albuminous cells and lack companion cells. Tannin-storing thin-walled xylem cells are xylem "
           "parenchyma.",
       ncert=ref("ANA", "The Tissues (phloem)"), secs=25)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "In a dorsiventral (dicotyledonous) leaf, the vascular bundles are surrounded by a layer of:",
       "thick-walled bundle sheath cells",
       ["thin-walled bulliform cells", "Casparian strips of suberin", "semi-lunar patches of sclerenchyma"], "D",
       "Vascular bundles of a dorsiventral leaf",
       "The vascular system of a dorsiventral leaf includes the vascular bundles seen in the veins and the midrib. "
       "The vascular bundles are surrounded by a layer of thick-walled bundle sheath cells.",
       ["Dorsiventral leaf: bundles in veins and midrib", "Each surrounded by thick-walled bundle sheath cells"],
       why="Bulliform cells are large epidermal cells of grass leaves. Casparian strips belong to the endodermis of "
           "the root. Semi-lunar sclerenchyma patches are the pericycle of the dicot stem.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dorsiventral leaf)"), secs=25)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "Root hairs and trichomes both belong to the epidermal tissue system.",
               "Root hairs are usually multicellular, whereas the trichomes of the shoot system are unicellular.",
               True, False, "C",
               "Epidermal appendages",
               "The epidermal tissue system is made of epidermal cells, stomata and the epidermal appendages, the "
               "trichomes and hairs. Root hairs are unicellular elongations of the epidermal cells that absorb water "
               "and minerals. The trichomes of the shoot system are usually multicellular; they may be branched or "
               "unbranched, soft or stiff, and even secretory.",
               ["Statement I: true", "Statement II: false; root hairs are unicellular, trichomes usually multicellular"],
               ncert=ref("ANA", "The Tissue System (epidermal tissue system)"), secs=30)

direct(T_ANA, "Plant tissues", "Basic",
       "A simple permanent tissue has oval, spherical or polygonal cells whose walls are thickened at the corners "
       "by deposition of cellulose, hemicellulose and pectin. The cells often contain chloroplasts, and intercellular "
       "spaces are absent. The tissue is:",
       "collenchyma",
       ["parenchyma", "sclerenchyma", "xylem parenchyma"], "A",
       "Identifying collenchyma",
       "Collenchyma cells are thickened at the corners due to a deposition of cellulose, hemicellulose and pectin. "
       "They may be oval, spherical or polygonal, often contain chloroplasts and assimilate food when chloroplasts are "
       "present. Intercellular spaces are absent. Collenchyma gives mechanical support to growing parts such as the "
       "young stem and the petiole.",
       ["Corner thickening of cellulose, hemicellulose, pectin = collenchyma"],
       why="Parenchyma has thin cellulose walls; sclerenchyma has thick lignified walls; xylem parenchyma is a "
           "thin-walled storage tissue of the xylem, a complex tissue.",
       ncert=ref("ANA", "The Tissues (simple tissues: collenchyma)"), secs=25)

match_list(T_ANA, "Plant tissues", "Basic", "meristem or bud", "role described in NCERT",
           ["Apical meristem", "Intercalary meristem", "Lateral meristem", "Axillary bud"],
           ["Can form a branch or a flower", "Produces the secondary tissues",
            "Produces the primary tissues at the tips of roots and shoots",
            "Regenerates parts removed by grazing herbivores in grasses"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "B",
           "Meristems and their roles",
           "Apical meristems occur at the tips of roots and shoots and produce primary tissues. Intercalary meristems "
           "occur in grasses and regenerate parts removed by grazing herbivores. Lateral meristems, in the mature "
           "regions of roots and shoots, are responsible for producing the secondary tissues. Axillary buds, formed "
           "from cells left behind by the shoot apical meristem, are capable of forming a branch or a flower.",
           ["Apical -> III", "Intercalary -> IV", "Lateral -> II", "Axillary bud -> I"],
           why="The wrong codes swap apical and intercalary, lateral and axillary bud, or intercalary and lateral.",
           ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=35)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Sclereids are commonly found in the seed coats of legumes.",
                 "Sclereids are living cells with thin cellulose walls.",
                 True, False, False, "C",
                 "Sclereids",
                 "Sclereids are spherical, oval or cylindrical, highly thickened dead cells with very narrow cavities "
                 "(lumen). They are commonly found in the fruit walls of nuts, the pulp of fruits like guava, pear and "
                 "sapota, the seed coats of legumes and the leaves of tea.",
                 ["A: true", "R: false; sclereids are dead and highly thickened"],
                 ncert=ref("ANA", "The Tissues (simple tissues: sclerenchyma)"), secs=30)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "The section of a leaf shows a mesophyll differentiated into palisade parenchyma on the adaxial side and "
                "spongy parenchyma below it, with more stomata on the lower epidermis than on the upper. Which of the "
                "following conclusions are correct?",
                [("It is a dorsiventral (dicotyledonous) leaf.", True),
                 ("Its vascular bundles vary in size, depending on the size of the veins.", True),
                 ("Large, empty, colourless bulliform cells are present along its veins in the adaxial epidermis.",
                  False),
                 ("Each stoma is bounded by two bean-shaped guard cells.", True),
                 ("Its spongy parenchyma cells are loosely arranged, with large spaces and air cavities.", True)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("b", "d", "e")], "A",
                "Interpreting a dorsiventral leaf section",
                "A mesophyll with adaxial palisade and abaxial spongy parenchyma, and more stomata on the abaxial "
                "epidermis, marks a dorsiventral (dicot) leaf. The size of its vascular bundles depends on the size of "
                "the veins, which vary in thickness in the reticulate venation of dicot leaves. Dicot guard cells are "
                "bean-shaped. The spongy parenchyma cells are oval or round, loosely arranged, with large spaces and "
                "air cavities. Bulliform cells are a feature of grass (isobilateral) leaves.",
                ["(a), (b), (d), (e) true", "(c) false; bulliform cells occur in grasses"],
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (leaves); The Tissue System"),
                secs=60)

match_list(T_ANA, "Plant tissues", "Intermediate", "tissue", "function described in NCERT",
           ["Xylem", "Phloem", "Collenchyma", "Sclerenchyma"],
           ["Mechanical support to organs", "Transport of food materials, usually from the leaves to other parts",
            "Mechanical support to growing parts such as the young stem and the petiole",
            "Conduction of water and minerals from the roots to the stem and leaves"],
           "IV II III I", ["II IV III I", "IV II I III", "III II IV I"], "C",
           "Functions of plant tissues",
           "Xylem conducts water and minerals from the roots to the stem and leaves (and gives mechanical strength). "
           "Phloem transports food materials, usually from the leaves to other parts of the plant. Collenchyma gives "
           "mechanical support to the growing parts, such as the young stem and the petiole of a leaf. Sclerenchyma "
           "provides mechanical support to organs.",
           ["Xylem -> IV", "Phloem -> II", "Collenchyma -> III", "Sclerenchyma -> I"],
           why="The wrong codes swap xylem and phloem, collenchyma and sclerenchyma, or xylem and collenchyma.",
           ncert=ref("ANA", "The Tissues"), secs=35)

statement_pair(T_ANA, "Plant tissues", "Intermediate",
               "Both tracheids and vessel members are devoid of protoplasm at maturity.",
               "Xylem fibres have thin walls and a wide central lumen.",
               True, False, "C",
               "Elements of xylem",
               "Tracheids are elongated, tube-like cells with thick, lignified walls and tapering ends; they are dead "
               "and without protoplasm. Vessel members, with lignified walls and a large central cavity, are also "
               "devoid of protoplasm. Xylem fibres have highly thickened walls and obliterated central lumens.",
               ["Statement I: true", "Statement II: false; xylem fibres have very thick walls and obliterated lumens"],
               ncert=ref("ANA", "The Tissues (complex tissues: xylem)"), secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "A transverse section of a young root shows radial vascular bundles with two to four xylem and phloem patches, "
       "a small pith and an endodermis with Casparian strips. In this organ, lateral roots are initiated in the:",
       "pericycle",
       ["endodermis", "epiblema", "conjunctive tissue"], "B",
       "Dicot root: origin of lateral roots",
       "Two to four xylem and phloem patches and a small or inconspicuous pith identify a dicot root. Next to the "
       "endodermis, towards the inside, lie a few layers of thick-walled parenchymatous cells, the pericycle. "
       "Initiation of lateral roots takes place in these cells.",
       ["Features -> dicot root", "Lateral roots arise in the pericycle"],
       why="The endodermis is the innermost cortical layer with Casparian strips; the epiblema is the outermost layer "
           "bearing root hairs; conjunctive tissue is the parenchyma between xylem and phloem.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicotyledonous root)"), secs=40)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Axillary buds are capable of forming a branch or a flower.",
                 "Axillary buds arise from the activity of the lateral meristem.",
                 True, False, False, "C",
                 "Origin of axillary buds",
                 "During the formation of leaves and elongation of the stem, some cells 'left behind' from the shoot "
                 "apical meristem constitute the axillary bud. Such buds are present in the axils of leaves and are "
                 "capable of forming a branch or a flower. The lateral meristem is a cylindrical meristem in the mature "
                 "regions of roots and shoots.",
                 ["A: true", "R: false; axillary buds come from cells left behind by the shoot apical meristem"],
                 ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=35)

assertion_reason(T_ANA, "Tissue systems", "Advanced",
                 "In a dicot root, the conjunctive tissue is a part of the stele.",
                 "All tissues on the inner side of the endodermis constitute the stele, and the conjunctive tissue "
                 "lies between the xylem and the phloem, inside the endodermis.",
                 True, True, True, "A",
                 "Stele of the dicot root",
                 "In the dicot root, all tissues on the inner side of the endodermis, such as the pericycle, vascular "
                 "bundles and pith, constitute the stele. The conjunctive tissue is the parenchyma lying between the "
                 "xylem and the phloem, which are within the endodermis; so it falls within the stele.",
                 ["A: true", "R: true", "Being inside the endodermis is exactly what makes a tissue part of the stele"],
                 ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicotyledonous root)"),
                 secs=45)

match_list(T_ANA, "Dicot and monocot anatomy", "Advanced", "feature seen in a section", "organ",
           ["Water-containing cavities within the vascular bundles", "Semi-lunar patches of sclerenchyma above the phloem",
            "Large, well-developed pith with usually more than six xylem bundles",
            "Stomata on both surfaces and an undifferentiated mesophyll"],
           ["Isobilateral leaf", "Monocot root", "Dicot stem", "Monocot stem"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D",
           "Diagnostic features in sections",
           "Water-containing cavities in the bundles are a feature of the monocot stem. Semi-lunar sclerenchyma patches "
           "above the phloem form the pericycle of the dicot stem. A monocot root has a large, well-developed pith and "
           "usually more than six (polyarch) xylem bundles. An isobilateral leaf has stomata on both surfaces and a "
           "mesophyll not differentiated into palisade and spongy parenchyma.",
           ["A -> monocot stem", "B -> dicot stem", "C -> monocot root", "D -> isobilateral leaf"],
           why="The wrong codes swap the two stems, the monocot root and the isobilateral leaf, or the dicot stem and the "
               "monocot root.",
           ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=50)

statement_pair(T_ANA, "Plant tissues", "Advanced",
               "Phloem fibres (bast fibres) are generally absent in the primary phloem but are found in the secondary "
               "phloem.",
               "Phloem fibres are much elongated and unbranched, with pointed, needle-like apices and quite thick "
               "walls.",
               True, True, "A",
               "Phloem fibres",
               "Phloem fibres (bast fibres) are made up of sclerenchymatous cells. They are generally absent in the "
               "primary phloem but are found in the secondary phloem. They are much elongated, unbranched and have "
               "pointed, needle-like apices, and their cell wall is quite thick. At maturity they lose their "
               "protoplasm and become dead.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (complex tissues: phloem)"), secs=40)

direct(T_ANA, "Plant tissues", "Advanced",
       "In which of the following pairs do BOTH cells lack a nucleus at maturity?",
       "Tracheid and sieve tube element",
       ["Companion cell and sieve tube element", "Collenchyma cell and tracheid",
        "Xylem parenchyma cell and vessel member"], "A",
       "Cells without a nucleus at maturity",
       "Tracheids are dead and without protoplasm, so they have no nucleus. A mature sieve tube element is living but "
       "possesses only peripheral cytoplasm and a large vacuole and lacks a nucleus; its functions are controlled by "
       "the nucleus of the companion cell. Companion cells, collenchyma cells and xylem parenchyma cells are living "
       "cells with nuclei.",
       ["Tracheid: dead, no protoplasm", "Sieve tube element: living but no nucleus"],
       why="Each wrong pair includes a living, nucleated cell: the companion cell, the collenchyma cell or the xylem "
           "parenchyma cell.",
       ncert=ref("ANA", "The Tissues (xylem and phloem)"), secs=45)

multi_statement(T_ANA, "Tissue systems", "Advanced",
                "Which of the following lie on the inner side of the endodermis in a dicot stem?",
                [("Pericycle", True), ("Medullary rays", True), ("Hypodermis", False), ("Vascular bundles", True),
                 ("Pith", True)],
                [("a", "d", "e"), ("b", "c", "e"), ("a", "b", "c", "d")], "D",
                "Arrangement of tissues in the dicot stem",
                "In the dicot stem, the cortex has three sub-zones: the outer collenchymatous hypodermis, the cortical "
                "layers and the innermost endodermis. Inside the endodermis lie the pericycle (semi-lunar sclerenchyma "
                "patches above the phloem), the ring of vascular bundles, the medullary rays between the bundles and "
                "the central pith.",
                ["Outside the endodermis: epidermis, hypodermis, cortical layers",
                 "Inside: pericycle, vascular bundles, medullary rays, pith"],
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicotyledonous stem)"),
                secs=50)

# =============================================================== 5. Cell: The Unit of Life (5/7/6)
direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In a chloroplast, the flat membranous tubules that connect the thylakoids of different grana are called:",
       "stroma lamellae",
       ["cristae", "mesosomes", "chromatophores"], "D",
       "Internal membranes of the chloroplast",
       "The space limited by the inner membrane of the chloroplast is the stroma. A number of organised, flattened "
       "membranous sacs, the thylakoids, are present in the stroma and are arranged in stacks like piles of coins "
       "called grana. Flat membranous tubules called stroma lamellae connect the thylakoids of the different grana.",
       ["Thylakoids stack into grana", "Stroma lamellae connect thylakoids of different grana"],
       why="Cristae are infoldings of the inner mitochondrial membrane. Mesosomes and chromatophores are membrane "
           "extensions of prokaryotic cells.",
       ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=20)

direct(T_CELL, "Cell envelope and membrane", "Basic",
       "The quasi-fluid nature of lipid enables lateral movement of proteins within the overall bilayer of the cell "
       "membrane. This ability to move within the membrane is measured as its:",
       "fluidity",
       ["selective permeability", "osmosis", "active transport"], "B",
       "Fluidity of the membrane",
       "In the fluid mosaic model of Singer and Nicolson (1972), the quasi-fluid nature of the lipid enables lateral "
       "movement of proteins within the overall bilayer. This ability to move within the membrane is measured as its "
       "fluidity. The fluid nature is important for functions like cell growth, formation of intercellular junctions, "
       "secretion, endocytosis and cell division.",
       ["Lateral movement within the membrane is measured as fluidity"],
       why="Selective permeability refers to which molecules can cross the membrane. Osmosis is diffusion of water. "
           "Active transport is energy-dependent movement against a concentration gradient.",
       ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "Every chromosome has a primary constriction, the centromere. The disc-shaped structures present on the sides "
       "of the centromere are called:",
       "kinetochores",
       ["satellites", "centrioles", "nucleoli"], "B",
       "Centromere and kinetochores",
       "Every chromosome essentially has a primary constriction, the centromere, on the sides of which disc-shaped "
       "structures called kinetochores are present.",
       ["Primary constriction = centromere", "Disc-shaped structures on its sides = kinetochores"],
       why="A satellite is a small chromosome fragment set off by a non-staining secondary constriction. Centrioles lie "
           "in the centrosome of animal cells, and nucleoli are bodies in the nucleoplasm.",
       ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=20)

statement_pair(T_CELL, "Nucleus", "Basic",
               "Normally there is only one nucleus per cell, although variations in the number of nuclei are also "
               "frequently observed.",
               "The nucleus contains one or more spherical structures called nucleoli in the nucleoplasm.",
               True, True, "A",
               "Number of nuclei and nucleoli",
               "NCERT states that normally there is only one nucleus per cell, though variations in the number of "
               "nuclei are also frequently observed. The nuclear matrix or nucleoplasm contains the nucleolus and "
               "chromatin; the nucleoli are spherical structures present in the nucleoplasm.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=25)

match_list(T_CELL, "Mitochondria, plastids and ribosomes", "Basic", "plastid", "content",
           ["Amyloplasts", "Elaioplasts", "Aleuroplasts", "Chromoplasts"],
           ["Fat-soluble carotenoid pigments", "Proteins", "Starch (carbohydrates)", "Oils and fats"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C",
           "Kinds of plastids",
           "Leucoplasts are colourless plastids of varied shapes and sizes with stored nutrients: amyloplasts store "
           "carbohydrates (starch), elaioplasts store oils and fats, and aleuroplasts store proteins. Chromoplasts "
           "contain fat-soluble carotenoid pigments such as carotene and xanthophylls.",
           ["Amyloplast -> starch", "Elaioplast -> oils and fats", "Aleuroplast -> proteins",
            "Chromoplast -> carotenoids"],
           why="The wrong codes swap amyloplasts and elaioplasts, aleuroplasts and chromoplasts, or elaioplasts and "
               "aleuroplasts.",
           ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=30)

assertion_reason(T_CELL, "Endomembrane system", "Intermediate",
                 "In animal cells, lipid-like steroidal hormones are synthesised in the smooth endoplasmic reticulum.",
                 "The smooth endoplasmic reticulum is the major site for the synthesis of lipids.",
                 True, True, True, "A",
                 "Functions of the smooth ER",
                 "The endoplasmic reticulum that does not bear ribosomes appears smooth (SER). The SER is the major site "
                 "for the synthesis of lipid; accordingly, in animal cells, lipid-like steroidal hormones are "
                 "synthesised in the SER.",
                 ["A: true", "R: true", "Steroidal hormones are lipid-like, so they are made where lipids are made"],
                 ncert=ref("CELL", "Eukaryotic Cells (endoplasmic reticulum)"), secs=35)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                "In which of the following locations would you expect 70S ribosomes?",
                [("The cytoplasm of a bacterium", True), ("The stroma of a chloroplast", True),
                 ("The matrix of a mitochondrion", True), ("The cytoplasm of an onion root cell", False),
                 ("The rough endoplasmic reticulum of a liver cell", False)],
                [("a", "b"), ("a", "b", "c", "e"), ("b", "c", "d")], "B",
                "70S and 80S ribosomes",
                "Prokaryotic ribosomes are of the 70S type. The chloroplast stroma contains ribosomes smaller (70S) than "
                "the cytoplasmic ones (80S), and the mitochondrial matrix contains 70S ribosomes. The cytoplasm of an "
                "eukaryotic cell, including ribosomes on the RER, has 80S ribosomes.",
                ["(a), (b), (c): 70S", "(d), (e): eukaryotic cytoplasmic ribosomes, 80S"],
                ncert=ref("CELL", "Prokaryotic Cells (ribosomes); Eukaryotic Cells (mitochondria, plastids, ribosomes)"),
                secs=45)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "Transport of a few ions or molecules across the membrane from lower to higher concentration is an "
               "energy-dependent process that uses ATP, as in the Na+/K+ pump.",
               "Neutral solutes move across the membrane by simple diffusion against their concentration gradient.",
               True, False, "C",
               "Passive and active transport",
               "Neutral solutes may move across the membrane by simple diffusion along the concentration gradient, "
               "from higher to lower concentration. A few ions or molecules are transported against their "
               "concentration gradient, from lower to higher concentration; this is an energy-dependent process using "
               "ATP, called active transport, e.g. the Na+/K+ pump.",
               ["Statement I: true (active transport)", "Statement II: false; simple diffusion is along the gradient"],
               ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=35)

match_list(T_CELL, "Endomembrane system", "Intermediate", "cell activity", "structure chiefly concerned",
           ["A gland cell synthesising and secreting much protein", "Formation of glycoproteins and glycolipids",
            "Osmoregulation and excretion in Amoeba",
            "Accumulating ions in the vacuole above their cytoplasmic concentration"],
           ["Contractile vacuole", "Tonoplast", "Rough endoplasmic reticulum", "Golgi apparatus"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A",
           "Endomembrane components and their roles",
           "The RER is frequently observed in cells actively involved in protein synthesis and secretion. The Golgi "
           "apparatus is the important site of formation of glycoproteins and glycolipids. In Amoeba the contractile "
           "vacuole is important for osmoregulation and excretion. The tonoplast facilitates the transport of a number "
           "of ions and other materials against concentration gradients into the vacuole, so their concentration is "
           "significantly higher in the vacuole than in the cytoplasm.",
           ["Protein secretion -> RER", "Glycoproteins and glycolipids -> Golgi",
            "Amoeba osmoregulation -> contractile vacuole", "Ion accumulation -> tonoplast"],
           why="The wrong codes swap RER and Golgi, the contractile vacuole and tonoplast, or Golgi and the contractile "
               "vacuole.",
           ncert=ref("CELL", "Eukaryotic Cells (endomembrane system)"), secs=45)

_dna_cm = 200 / 46
numerical(T_CELL, "Nucleus", "Intermediate",
          "According to NCERT, a single human cell has an approximately two-metre-long thread of DNA distributed among "
          "its forty-six chromosomes. On average, about how long is the DNA of one chromosome?",
          "About 4.3 cm", ["About 8.7 cm", "About 43 cm", "About 0.43 cm"], "D",
          abs(_dna_cm - 4.35) < 0.01 and abs(200 / 23 - 8.70) < 0.01,
          "Length of DNA in human chromosomes",
          "The DNA of a human cell, about 2 m long, is distributed among 46 chromosomes (23 pairs). The average length "
          "per chromosome is 2 m / 46 = 200 cm / 46, about 4.3 cm.",
          ["2 m = 200 cm", "200 cm / 46 = 4.35 cm, about 4.3 cm"],
          why="8.7 cm divides by the 23 pairs instead of the 46 chromosomes; 43 cm and 0.43 cm are errors of a factor of "
              "10 in converting metres to centimetres.",
          ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=45)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "Mesosomes increase the surface area of the plasma membrane and its enzymatic content.",
                 "Mesosomes are double-membrane-bound organelles, like mitochondria.",
                 True, False, False, "C",
                 "Mesosomes",
                 "Mesosomes are a special membranous structure formed by extensions of the plasma membrane into the cell, "
                 "in the form of vesicles, tubules and lamellae. They help in cell wall formation, DNA replication and "
                 "its distribution to daughter cells, respiration and secretion, and increase the surface area of the "
                 "plasma membrane and its enzymatic content. Prokaryotes have no membrane-bound organelles such as "
                 "mitochondria.",
                 ["A: true", "R: false; mesosomes are extensions of the plasma membrane, not organelles"],
                 ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=35)

match_list(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate", "structure", "organisation",
           ["Axoneme of a cilium", "Centriole", "Bacterial flagellum", "Basal body"],
           ["Filament, hook and basal body", "Centriole-like structure from which a cilium or flagellum emerges",
            "Nine peripheral doublets around a central pair of microtubules",
            "Nine evenly spaced peripheral triplet fibrils of tubulin, like a cartwheel"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B",
           "Microtubular structures",
           "The axoneme of a cilium or flagellum has nine pairs of doublets of radially arranged peripheral microtubules "
           "and a pair of centrally located microtubules (9 + 2). A centriole has an organisation like a cartwheel, made "
           "of nine evenly spaced peripheral fibrils of tubulin, each a triplet. A bacterial flagellum has a filament, a "
           "hook and a basal body. Cilia and flagella emerge from centriole-like structures called basal bodies.",
           ["Axoneme -> 9 + 2 doublets", "Centriole -> 9 triplets", "Bacterial flagellum -> filament, hook, basal body",
            "Basal body -> centriole-like base"],
           why="The wrong codes swap the axoneme and centriole, the bacterial flagellum and basal body, or the axoneme "
               "and bacterial flagellum.",
           ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella; centrosome); Prokaryotic Cells"), secs=45)

multi_statement(T_CELL, "Cell theory", "Advanced",
                "A cell has a nucleus with a nuclear envelope and a centrosome with two centrioles, but no cell wall and "
                "no plastids. Which of the following conclusions about it are correct?",
                [("It is a eukaryotic cell.", True),
                 ("Its outer boundary is the plasma membrane.", True),
                 ("It has a large central vacuole.", False),
                 ("Its centrioles can give rise to the spindle fibres during cell division.", True),
                 ("All its ribosomes are of the 70S type.", False)],
                [("a", "b", "c", "d"), ("a", "d", "e"), ("b", "c", "d")], "C",
                "Recognising an animal cell",
                "A nucleus bounded by a nuclear envelope marks a eukaryotic cell; centrioles with no cell wall or "
                "plastids mark an animal cell. Its delimiting outer structure is the cell membrane. Plant cells, not "
                "animal cells, have a large central vacuole. In animal cells the centrioles give rise to the spindle "
                "fibres of the spindle apparatus. The cytoplasmic ribosomes of eukaryotes are 80S.",
                ["(a), (b), (d) true", "(c) false: large central vacuole is a plant-cell feature",
                 "(e) false: cytoplasmic ribosomes are 80S"],
                ncert=ref("CELL", "Eukaryotic Cells"), secs=60)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "The stroma of a chloroplast can carry out protein synthesis.",
                 "The chloroplast stroma contains small, double-stranded circular DNA molecules and ribosomes, along "
                 "with enzymes required for the synthesis of proteins.",
                 True, True, True, "A",
                 "Chloroplast stroma",
                 "The stroma of the chloroplast contains enzymes required for the synthesis of carbohydrates and "
                 "proteins. It also contains small, double-stranded circular DNA molecules and ribosomes (70S). "
                 "Ribosomes are the sites of protein synthesis, so the stroma has the machinery for it.",
                 ["A: true", "R: true", "DNA, ribosomes and enzymes in the stroma explain its protein synthesis"],
                 ncert=ref("CELL", "Eukaryotic Cells (plastids; ribosomes)"), secs=45)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "The chromatophores of cyanobacteria and the thylakoids of chloroplasts both contain pigments.",
               "Chromatophores, like thylakoids, lie inside a double-membrane-bound plastid.",
               True, False, "C",
               "Chromatophores and thylakoids",
               "In some prokaryotes such as cyanobacteria, there are other membranous extensions into the cytoplasm "
               "called chromatophores, which contain pigments. Thylakoids lie in the stroma of the chloroplast, a "
               "double-membrane-bound plastid, and contain the chlorophyll pigments. Prokaryotes have no "
               "membrane-bound organelles, so chromatophores do not lie inside any plastid.",
               ["Statement I: true", "Statement II: false; chromatophores are extensions into the prokaryotic cytoplasm"],
               ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells (plastids)"), secs=45)

match_list(T_CELL, "Endomembrane system", "Advanced", "structure", "origin or nature",
           ["Tonoplast", "Cristae", "Grana", "Nuclear pores"],
           ["Formed by the fusion of the two membranes of the nuclear envelope", "Stacks of thylakoids",
            "Infoldings of the inner mitochondrial membrane", "Single membrane bounding the vacuole"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D",
           "Membranes and membrane-derived structures",
           "The vacuole is bound by a single membrane called the tonoplast. The inner mitochondrial membrane forms a "
           "number of infoldings, the cristae. In the chloroplast stroma, thylakoids are arranged in stacks like piles "
           "of coins called grana. The nuclear envelope is interrupted at places by minute pores formed by the fusion "
           "of its two membranes.",
           ["Tonoplast -> IV", "Cristae -> III", "Grana -> II", "Nuclear pores -> I"],
           why="The wrong codes swap the tonoplast and cristae, the grana and nuclear pores, or the cristae and grana.",
           ncert=ref("CELL", "Eukaryotic Cells (vacuoles, mitochondria, plastids, nucleus)"), secs=50)

direct(T_CELL, "Cell envelope and membrane", "Advanced",
       "Two neighbouring mature plant cells each have a primary and a secondary wall. Which sequence correctly shows "
       "the layers met in going from the plasma membrane of one cell to the plasma membrane of the other?",
       "Secondary wall -> primary wall -> middle lamella -> primary wall -> secondary wall",
       ["Primary wall -> secondary wall -> middle lamella -> secondary wall -> primary wall",
        "Middle lamella -> primary wall -> secondary wall -> primary wall -> middle lamella",
        "Secondary wall -> middle lamella -> primary wall -> middle lamella -> secondary wall"], "D",
       "Layers of the plant cell wall",
       "The cell wall of a young plant cell, the primary wall, is capable of growth. Secondary wall is formed on the "
       "inner (towards the membrane) side of the cell. The middle lamella, mainly calcium pectate, holds or glues "
       "the different neighbouring cells together. So from one plasma membrane outward: secondary wall, primary wall, "
       "then the shared middle lamella, then the other cell's primary and secondary walls.",
       ["Secondary wall lies inside the primary wall", "Middle lamella lies between the walls of neighbouring cells"],
       why="The first wrong sequence puts the secondary wall outside the primary wall. The others put a middle lamella "
           "next to the plasma membrane or between the primary and secondary walls of the same cell.",
       ncert=ref("CELL", "Eukaryotic Cells (cell wall)"), secs=50)

direct(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
       "NCERT describes radial spokes as protein connections in microtubular structures. Radial spokes are found in:",
       "both the axoneme of a cilium and a centriole",
       ["the axoneme of a cilium only", "a centriole only", "the bacterial flagellum only"], "A",
       "Radial spokes in axonemes and centrioles",
       "In the axoneme of cilia and flagella, the central sheath is connected to one of the tubules of each peripheral "
       "doublet by a radial spoke. In a centriole, the central part of the proximal region, the hub, is connected with "
       "the tubules of the peripheral triplets by radial spokes made of protein. So both have radial spokes.",
       ["Axoneme: central sheath -> radial spokes -> peripheral doublets",
        "Centriole: hub -> radial spokes -> peripheral triplets"],
       why="Restricting radial spokes to only one of the two ignores the other description. The bacterial flagellum "
           "has a filament, hook and basal body, not a 9 + 2 or cartwheel structure.",
       ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella; centrosome and centrioles)"), secs=45)

# =============================================================== 6. Cell Cycle and Cell Division (5/6/5)
direct(T_CC, "Mitosis", "Basic",
       "Prophase of mitosis is marked by the initiation of condensation of the chromosomal material. The chromosomal "
       "material becomes untangled during the process of:",
       "chromatin condensation",
       ["DNA replication", "synapsis", "crossing over"], "B",
       "Prophase of mitosis",
       "In the S and G2 phases the new DNA molecules are not distinct but intertwined. Prophase is marked by the "
       "initiation of condensation of the chromosomal material, and the chromosomal material becomes untangled during "
       "the process of chromatin condensation.",
       ["S and G2: DNA molecules intertwined", "Prophase: untangled during chromatin condensation"],
       why="DNA replication takes place in the S phase, not prophase. Synapsis and crossing over are events of "
           "prophase I of meiosis.",
       ncert=ref("CC", "M Phase (prophase)"), secs=20)

match_list(T_CC, "Cell cycle phases", "Basic", "item", "value given in NCERT",
           ["Duration of the cell cycle of a typical human cell in culture", "Duration of the M phase of that cell",
            "Duration of the cell cycle of yeast", "Share of interphase in the duration of a cell cycle"],
           ["About 90 minutes", "More than 95 per cent", "About 24 hours", "About an hour"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D",
           "Timing of the cell cycle",
           "A typical eukaryotic cell, such as a human cell in culture, divides about once every 24 hours. Of this, the "
           "actual division (M phase) lasts only about an hour, and interphase lasts more than 95 per cent of the "
           "cycle. Yeast can progress through the cell cycle in only about 90 minutes.",
           ["Human cell: ~24 h", "M phase: ~1 h", "Yeast: ~90 min", "Interphase: >95 per cent"],
           why="The wrong codes swap the human cycle and the M phase, yeast and interphase, or the human and yeast "
               "cycles.",
           ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=30)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "All organisms, even the largest, start their life from a single cell.",
               "Like cell growth, DNA synthesis continues throughout the cell cycle.",
               True, False, "C",
               "Cell division and the cell cycle",
               "All organisms, even the largest, start their life from a single cell. Although cell growth (in terms "
               "of cytoplasmic increase) is a continuous process, DNA synthesis occurs only during one specific stage "
               "of the cell cycle, the S phase.",
               ["Statement I: true", "Statement II: false; DNA is synthesised only in the S phase"],
               ncert=ref("CC", "Cell Cycle"), secs=25)

direct(T_CC, "Mitosis", "Basic",
       "Karyokinesis of mitosis is divided into four stages. Which sequence is correct?",
       "Prophase -> metaphase -> anaphase -> telophase",
       ["Prophase -> anaphase -> metaphase -> telophase", "Metaphase -> prophase -> anaphase -> telophase",
        "Prophase -> metaphase -> telophase -> anaphase"], "D",
       "Stages of karyokinesis",
       "Mitosis (karyokinesis) is divided into four stages: prophase, metaphase, anaphase and telophase. Cytokinesis, "
       "the division of the cytoplasm, follows.",
       ["Order: prophase, metaphase, anaphase, telophase"],
       why="Each wrong sequence changes the order of two stages.",
       ncert=ref("CC", "M Phase"), secs=20)

multi_statement(T_CC, "Mitosis", "Basic",
                "Which of the following take place during prophase of mitosis?",
                [("Initiation of condensation of the chromosomal material", True),
                 ("The centrosomes begin to move towards opposite poles of the cell.", True),
                 ("The chromosomes align on the metaphase plate.", False),
                 ("The centromeres split and the chromatids separate.", False),
                 ("Each centrosome radiates out microtubules called asters.", True)],
                [("a", "b", "c"), ("a", "c", "d"), ("b", "d", "e")], "B",
                "Events of prophase",
                "Prophase is marked by the initiation of condensation of the chromosomal material. The centrosome, which "
                "had duplicated during interphase, now begins to move towards opposite poles, and each centrosome "
                "radiates out microtubules called asters. Alignment on the metaphase plate happens in metaphase, and "
                "splitting of centromeres in anaphase.",
                ["(a), (b), (e): prophase", "(c): metaphase", "(d): anaphase"],
                ncert=ref("CC", "M Phase (prophase)"), secs=40)

direct(T_CC, "Mitosis", "Intermediate",
       "In a dividing cell, the nuclear envelope has completely disintegrated, the condensation of chromosomes is "
       "complete, the chromosomes are spread through the cytoplasm, and spindle fibres are attaching to their "
       "kinetochores as they move to the spindle equator. The cell is in:",
       "metaphase of mitosis",
       ["prophase of mitosis", "anaphase of mitosis", "pachytene of meiosis I"], "B",
       "Recognising metaphase",
       "The complete disintegration of the nuclear envelope marks the start of metaphase. By this stage, condensation "
       "of chromosomes is complete and their morphology can be studied. Spindle fibres attach to the kinetochores of "
       "the chromosomes, which are moved to the spindle equator and aligned on the metaphase plate.",
       ["Nuclear envelope fully gone + condensation complete + kinetochore attachment = metaphase"],
       why="In prophase the chromosomes are only beginning to condense and the envelope is still breaking down. In "
           "anaphase the centromeres split and chromatids move apart. Pachytene is a stage of prophase I, before "
           "the nuclear envelope breaks down.",
       ncert=ref("CC", "M Phase (metaphase)"), secs=40)

assertion_reason(T_CC, "Meiosis", "Intermediate",
                 "Pachytene is relatively long-lived compared with leptotene and zygotene.",
                 "Recombination nodules first appear during zygotene.",
                 True, False, False, "C",
                 "Stages of prophase I",
                 "The first two stages of prophase I are relatively short-lived compared with the next stage, pachytene. "
                 "Pachytene is characterised by the appearance of recombination nodules, the sites at which crossing "
                 "over occurs between non-sister chromatids of the homologous chromosomes. Zygotene is the stage of "
                 "synapsis and formation of the synaptonemal complex.",
                 ["A: true", "R: false; recombination nodules appear in pachytene"],
                 ncert=ref("CC", "Meiosis (prophase I)"), secs=35)

match_list(T_CC, "Meiosis", "Intermediate", "event", "stage",
           ["Terminalisation of chiasmata", "Appearance of recombination nodules", "Formation of a dyad of cells",
            "Formation of a tetrad of four haploid cells"],
           ["Telophase II and cytokinesis", "Pachytene", "Telophase I and cytokinesis", "Diakinesis"],
           "IV II III I", ["II IV III I", "IV II I III", "IV III II I"], "A",
           "Events across meiosis",
           "Diakinesis is marked by terminalisation of chiasmata. Pachytene is characterised by the appearance of "
           "recombination nodules. In telophase I the nuclear membrane and nucleolus reappear and cytokinesis follows, "
           "giving a dyad of cells. At the end of meiosis II, cytokinesis follows telophase II, giving a tetrad of four "
           "haploid daughter cells.",
           ["Terminalisation -> diakinesis", "Recombination nodules -> pachytene", "Dyad -> telophase I",
            "Tetrad -> telophase II"],
           why="The wrong codes swap diakinesis and pachytene, the dyad and tetrad, or pachytene and telophase I.",
           ncert=ref("CC", "Meiosis"), secs=40)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Meiosis I is initiated after the parental chromosomes have replicated to produce identical sister "
               "chromatids in the S phase.",
               "In meiosis, recombination takes place between the sister chromatids of the same chromosome.",
               True, False, "C",
               "Key features of meiosis",
               "Meiosis I is initiated after the parental chromosomes have replicated to produce identical sister "
               "chromatids at the S phase. Meiosis involves pairing of homologous chromosomes and recombination "
               "between non-sister chromatids of homologous chromosomes.",
               ["Statement I: true", "Statement II: false; recombination is between non-sister chromatids of "
                "homologues"],
               ncert=ref("CC", "Meiosis"), secs=35)

multi_statement(T_CC, "Significance", "Intermediate",
                "Which of the following are described in NCERT as brought about by mitosis?",
                [("Growth of multicellular organisms", True),
                 ("Restoration of the nucleo-cytoplasmic ratio disturbed by cell growth", True),
                 ("Replacement of cells of the upper layer of the epidermis, the gut lining and blood cells", True),
                 ("Formation of gametes in animals", False),
                 ("Continuous growth of plants through divisions in the apical and lateral cambium", True)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d", "e")], "C",
                "Significance of mitosis",
                "Growth of multicellular organisms is due to mitosis. Cell growth disturbs the ratio between the nucleus "
                "and the cytoplasm, so the cell divides to restore the nucleo-cytoplasmic ratio. Mitosis brings about "
                "cell repair: cells of the upper layer of the epidermis, the gut lining and blood cells are constantly "
                "replaced. Mitotic divisions in the apical and lateral cambium give continuous growth of plants "
                "throughout their life. Gametes in animals are formed through meiosis (gametogenesis).",
                ["(a), (b), (c), (e) true", "(d) false; gametogenesis involves meiosis"],
                ncert=ref("CC", "Significance of Mitosis; Meiosis"), secs=50)

direct(T_CC, "Meiosis", "Intermediate",
       "Which of the following is seen at metaphase of mitosis and also at metaphase II of meiosis?",
       "Microtubules from opposite poles attach to the kinetochores of the two sister chromatids of each chromosome.",
       ["Bivalents align on the equatorial plate.",
        "Microtubules from opposite poles attach to the two members of a pair of homologous chromosomes.",
        "Chiasmata hold the homologous chromosomes together."], "D",
       "Metaphase of mitosis compared with metaphase II",
       "At metaphase of mitosis, spindle fibres from one pole attach to the kinetochore of one chromatid and fibres "
       "from the opposite pole to its sister chromatid. At metaphase II the chromosomes align at the equator and "
       "microtubules from opposite poles attach to the kinetochores of sister chromatids. In metaphase I, by contrast, "
       "bivalents align and microtubules from opposite poles attach to the pair of homologous chromosomes.",
       ["Mitosis metaphase and metaphase II: sister chromatids attached to opposite poles"],
       why="Alignment of bivalents and attachment to homologous pairs belong to metaphase I; chiasmata belong to "
           "prophase I and metaphase I, not to mitosis or meiosis II.",
       ncert=ref("CC", "M Phase (metaphase); Meiosis (metaphase I, metaphase II)"), secs=45)

assertion_reason(T_CC, "Significance", "Advanced",
                 "Meiosis is important for the process of evolution.",
                 "Meiosis increases the genetic variability in the population of organisms from one generation to the "
                 "next, and such variations are very important for evolution.",
                 True, True, True, "A",
                 "Significance of meiosis",
                 "Meiosis conserves the specific chromosome number of each species across generations in sexually "
                 "reproducing organisms. It also increases the genetic variability in the population from one "
                 "generation to the next. Variations are very important for the process of evolution; this is why "
                 "meiosis matters for evolution.",
                 ["A: true", "R: true", "Variability produced by meiosis is the reason it matters for evolution"],
                 ncert=ref("CC", "Significance of Meiosis"), secs=40)

direct(T_CC, "Meiosis", "Advanced",
       "Consider these events of meiosis: (i) separation of homologous chromosomes; (ii) terminalisation of chiasmata; "
       "(iii) splitting of the centromeres; (iv) formation of a dyad of cells; (v) alignment of bivalents on the "
       "equatorial plate. Which is the correct order?",
       "(ii) -> (v) -> (i) -> (iv) -> (iii)",
       ["(v) -> (ii) -> (i) -> (iv) -> (iii)", "(ii) -> (v) -> (iii) -> (iv) -> (i)",
        "(ii) -> (i) -> (v) -> (iii) -> (iv)"], "D",
       "Sequence of events in meiosis",
       "Terminalisation of chiasmata marks diakinesis, the end of prophase I. In metaphase I the bivalents align on "
       "the equatorial plate. In anaphase I the homologous chromosomes separate. Telophase I with cytokinesis gives a "
       "dyad of cells. In anaphase II the centromere of each chromosome splits.",
       ["Diakinesis (ii)", "Metaphase I (v)", "Anaphase I (i)", "Telophase I and cytokinesis (iv)", "Anaphase II (iii)"],
       why="The first wrong order puts metaphase I before diakinesis; the second splits centromeres in meiosis I; the "
           "third separates homologues before they align and splits centromeres before the dyad forms.",
       ncert=ref("CC", "Meiosis"), secs=60)

statement_pair(T_CC, "Cell cycle phases", "Advanced",
               "A cell in G2 phase and a cell at metaphase of mitosis of the same diploid plant have the same number of "
               "chromosomes and the same DNA content.",
               "Each nucleus at telophase I and a cell in G1 phase of the same plant have the same DNA content, though "
               "the telophase I nucleus has half as many chromosomes.",
               True, True, "A",
               "DNA content and chromosome number through division",
               "If the G1 cell has 2n chromosomes and 2C DNA, the S phase doubles the DNA to 4C without changing the "
               "chromosome number. So a G2 cell and a mitotic metaphase cell both have 2n chromosomes and 4C DNA. In "
               "meiosis I, homologous chromosomes separate while sister chromatids stay together, so each telophase I "
               "nucleus has n chromosomes of two chromatids each: 2C DNA, the same as a G1 cell.",
               ["G2 = metaphase: 2n, 4C", "Telophase I nucleus: n chromosomes x 2 chromatids = 2C = G1 DNA content"],
               ncert=ref("CC", "Cell Cycle (phases); Meiosis"), secs=60)

match_list(T_CC, "Meiosis", "Advanced", "event in meiosis", "stage in which it occurs",
           ["Nucleolus disappears and nuclear envelope breaks down", "Chiasmata first become visible",
            "Sister chromatids separate", "Homologous chromosomes separate"],
           ["Anaphase I", "Diplotene", "Anaphase II", "Diakinesis"],
           "IV II III I", ["II IV III I", "IV II I III", "IV III II I"], "B",
           "Timing of meiotic events",
           "By the end of diakinesis the nucleolus disappears and the nuclear envelope breaks down. In diplotene the "
           "bivalents tend to separate except at the sites of crossovers; these X-shaped structures are the chiasmata. "
           "In anaphase I homologous chromosomes separate while sister chromatids remain associated at their "
           "centromeres. In anaphase II the centromeres split and sister chromatids separate.",
           ["A -> diakinesis", "B -> diplotene", "C -> anaphase II", "D -> anaphase I"],
           why="The wrong codes swap diakinesis and diplotene, the two anaphases, or diplotene and anaphase II.",
           ncert=ref("CC", "Meiosis"), secs=45)

direct(T_CC, "Meiosis", "Advanced",
       "In a dividing cell of a diploid organism, a group of chromosomes has reached each pole, the nuclear membrane and "
       "nucleolus are reappearing, each group has half the chromosome number of the parent cell, and each chromosome "
       "still consists of two chromatids. The cell is in:",
       "telophase I of meiosis",
       ["telophase of mitosis", "telophase II of meiosis", "anaphase I of meiosis"], "D",
       "Recognising telophase I",
       "In telophase I the nuclear membrane and nucleolus reappear. Because homologous chromosomes separated in "
       "anaphase I while sister chromatids stayed together, each nucleus has half the parental chromosome number, each "
       "chromosome still having two chromatids.",
       ["Half the chromosome number -> meiosis", "Chromosomes still with two chromatids -> after meiosis I, not II",
        "Nuclear membrane reappearing -> telophase"],
       why="Telophase of mitosis keeps the parental (2n) number of single-chromatid chromosomes. In telophase II the "
           "chromosomes have single chromatids. In anaphase I the chromosomes are still moving and no nuclear "
           "membrane is forming.",
       ncert=ref("CC", "Meiosis (telophase I)"), secs=50)

# =============================================================== 7. Photosynthesis (5/7/5)
direct(T_PS, "Limiting factors", "Basic",
       "The plant (internal) factors affecting photosynthesis include the number, size, age and orientation of leaves "
       "and the amount of chlorophyll. According to NCERT, these internal factors depend on:",
       "the genetic predisposition and the growth of the plant",
       ["the concentration of CO2 in the atmosphere", "the temperature of the surroundings",
        "the availability of sunlight alone"], "B",
       "Internal factors of photosynthesis",
       "The plant factors include the number, size, age and orientation of leaves, mesophyll cells and chloroplasts, "
       "internal CO2 concentration and the amount of chlorophyll. These plant or internal factors are dependent on the "
       "genetic predisposition and the growth of the plant. Sunlight, temperature, CO2 concentration and water are "
       "external factors.",
       ["Internal factors depend on genetic predisposition and growth of the plant"],
       why="Atmospheric CO2, temperature and sunlight are the external factors themselves; they do not determine the "
           "plant's internal factors.",
       ncert=ref("PS", "Factors affecting Photosynthesis"), secs=25)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Plants in which the first product of CO2 fixation is a C4 acid, oxaloacetic acid (OAA), are said to follow "
       "the:",
       "C4 pathway",
       ["C3 pathway", "photorespiratory pathway", "cyclic photophosphorylation pathway"], "D",
       "C3 and C4 pathways",
       "Work on CO2 fixation showed two main groups of plants: those in which the first product of CO2 fixation is a "
       "C3 acid (PGA), following the C3 pathway, and those in which the first product is a C4 acid (OAA), following "
       "the C4 pathway.",
       ["First product PGA (C3 acid) -> C3 pathway", "First product OAA (C4 acid) -> C4 pathway"],
       why="In the C3 pathway the first product is 3-PGA. Photorespiration forms PGA and phosphoglycolate, and cyclic "
           "photophosphorylation is a light reaction that makes ATP; neither forms OAA.",
       ncert=ref("PS", "Where are the ATP and NADPH used? (the primary acceptor of CO2)"), secs=20)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Basic",
               "The Calvin pathway occurs in all photosynthetic plants, whether they have the C3 or the C4 pathway.",
               "Plants with the C4 pathway are adapted to cold, temperate regions.",
               True, False, "C",
               "Calvin cycle and C4 plants",
               "The Calvin pathway occurs in all photosynthetic plants; it does not matter whether they have C3 or C4 "
               "(or any other) pathways. Plants that are adapted to dry tropical regions have the C4 pathway; though "
               "their first CO2 fixation product is the C4 acid OAA, they use the Calvin cycle as the main "
               "biosynthetic pathway.",
               ["Statement I: true", "Statement II: false; C4 plants are adapted to dry tropical regions"],
               ncert=ref("PS", "The Calvin Cycle; The C4 Pathway"), secs=25)

match_list(T_PS, "Site and pigments", "Basic", "description", "term",
           ["Graph of the rate of photosynthesis at different wavelengths of light",
            "Graph of the light absorbed by a pigment at different wavelengths",
            "All the pigments of a photosystem except one molecule of chlorophyll a",
            "Synthesis of ATP from ADP and inorganic phosphate in the presence of light"],
           ["Photophosphorylation", "Antennae (light-harvesting system)", "Action spectrum", "Absorption spectrum"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "A",
           "Terms of the light reaction",
           "An action spectrum shows the rate of photosynthesis at different wavelengths; an absorption spectrum shows "
           "the ability of pigments to absorb light of different wavelengths. In each photosystem all the pigments "
           "except one molecule of chlorophyll a form a light-harvesting system called the antennae. The synthesis of "
           "ATP from ADP and inorganic phosphate in the presence of light is photophosphorylation.",
           ["Rate vs wavelength -> action spectrum", "Absorption vs wavelength -> absorption spectrum",
            "Light-harvesting pigments -> antennae", "Light-driven ATP synthesis -> photophosphorylation"],
           why="The wrong codes swap the two spectra, the antennae and photophosphorylation, or the absorption spectrum "
               "and antennae.",
           ncert=ref("PS", "How many Pigments are involved in Photosynthesis?; What is Light Reaction?"), secs=35)

multi_statement(T_PS, "Limiting factors", "Basic",
                "Which of the following are external factors affecting photosynthesis?",
                [("Availability of sunlight", True), ("Temperature", True), ("CO2 concentration", True),
                 ("Water", True), ("Amount of chlorophyll", False)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("b", "c", "d", "e")], "B",
                "External factors",
                "Photosynthesis is affected by both internal (plant) and external factors. The external factors include "
                "the availability of sunlight, temperature, CO2 concentration and water. The amount of chlorophyll is "
                "an internal (plant) factor.",
                ["(a)-(d): external", "(e): internal"],
                ncert=ref("PS", "Factors affecting Photosynthesis"), secs=30)

assertion_reason(T_PS, "Chemiosmosis", "Intermediate",
                 "During the light reaction, the pH in the lumen of the thylakoid decreases.",
                 "Protons accumulate in the lumen, both from the splitting of water and from the H carrier that "
                 "releases into the lumen the protons it removed from the stroma.",
                 True, True, True, "A",
                 "Proton gradient in the chloroplast",
                 "The splitting of water occurs on the inner side of the thylakoid membrane, so its protons accumulate in "
                 "the lumen. The primary acceptor passes electrons to an H carrier, which removes a proton from the "
                 "stroma and releases it into the lumen. NADP reductase on the stroma side also removes protons from the "
                 "stroma. These create a proton gradient across the thylakoid membrane and a measurable decrease in pH "
                 "in the lumen.",
                 ["A: true", "R: true", "More protons in the lumen means a lower pH there; R explains A"],
                 ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=45)

direct(T_PS, "Chemiosmosis", "Intermediate",
       "NCERT lists the requirements of chemiosmosis. Which of the following is NOT one of them?",
       "RuBisCO",
       ["A membrane", "A proton pump", "A proton gradient"], "B",
       "Requirements of chemiosmosis",
       "Chemiosmosis requires a membrane, a proton pump, a proton gradient and ATPase (ATP synthase). RuBisCO is the "
       "Calvin cycle enzyme of the stroma that combines RuBP with CO2; it has no role in making ATP.",
       ["Chemiosmosis: membrane + proton pump + proton gradient + ATPase"],
       why="A membrane, a proton pump and a proton gradient are all among the four requirements listed in NCERT.",
       ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=30)

_atp_need, _nadph_need, _atp_noncyclic = 6 * 3, 6 * 2, 12
numerical(T_PS, "Light reactions and photophosphorylation", "Intermediate",
          "The Calvin cycle uses 3 ATP and 2 NADPH for every CO2 fixed. In a chloroplast fixing 6 molecules of CO2, "
          "suppose non-cyclic photophosphorylation supplies exactly the NADPH needed together with 12 ATP. How many "
          "more ATP molecules must come from another route, such as cyclic photophosphorylation, which makes ATP but "
          "no NADPH?",
          "6", ["12", "18", "0"], "A",
          _nadph_need == 12 and _atp_need - _atp_noncyclic == 6,
          "Balancing ATP and NADPH for the Calvin cycle",
          "For 6 CO2 the Calvin cycle needs 6 x 3 = 18 ATP and 6 x 2 = 12 NADPH. Non-cyclic flow here supplies the 12 "
          "NADPH and 12 ATP, so 18 - 12 = 6 ATP are still needed. NCERT notes that the cycle needs 3 ATP but only 2 "
          "NADPH per CO2, and cyclic photophosphorylation (ATP without NADPH) probably meets this difference.",
          ["ATP needed = 6 x 3 = 18; NADPH needed = 6 x 2 = 12", "Supplied: 12 ATP", "Extra ATP = 18 - 12 = 6"],
          why="12 repeats the ATP already supplied; 18 is the total need, ignoring the non-cyclic ATP; 0 assumes ATP and "
              "NADPH are needed in equal numbers.",
          ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation; The Calvin Cycle"), secs=60)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following take place in non-cyclic photophosphorylation but NOT in cyclic "
                "photophosphorylation?",
                [("Splitting of water", True), ("Evolution of O2", True), ("Formation of NADPH + H+", True),
                 ("Synthesis of ATP", False), ("Participation of photosystem I", False)],
                [("a", "b", "c", "d"), ("a", "b"), ("c", "d", "e")], "D",
                "Cyclic and non-cyclic photophosphorylation compared",
                "In non-cyclic photophosphorylation PS II and PS I work in series; the water-splitting complex is "
                "associated with PS II, so water is split and O2 evolved, and the electrons finally reduce NADP+ to "
                "NADPH + H+. In cyclic photophosphorylation only PS I is functional and the electron circulates within "
                "the photosystem, so only ATP is synthesised. ATP synthesis and PS I occur in both.",
                ["(a), (b), (c): only non-cyclic", "(d), (e): both"],
                ncert=ref("PS", "The Electron Transport; Cyclic and Non-cyclic Photo-phosphorylation"), secs=45)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Intermediate",
               "In the Z scheme, the movement of electrons from photosystem II to photosystem I is downhill in terms of "
               "the redox potential scale.",
               "The electrons are used up as they pass through the electron transport chain.",
               True, False, "C",
               "Electron transport",
               "Electrons excited in PS II are picked up by an electron acceptor and passed to an electron transport "
               "system of cytochromes. This movement of electrons is downhill on the redox potential scale. The "
               "electrons are not used up as they pass through the chain but are passed on to the pigments of PS I.",
               ["Statement I: true", "Statement II: false; the electrons are passed on to PS I"],
               ncert=ref("PS", "The Electron Transport"), secs=35)

match_list(T_PS, "Limiting factors", "Intermediate", "observation", "factor limiting photosynthesis",
           ["A plant on a dense forest floor photosynthesises faster when more light reaches it",
            "Tomato yields rise in a greenhouse enriched with CO2",
            "A green leaf with optimal light and CO2 does not photosynthesise at a very low temperature",
            "During drought, the stomata of a plant close and its leaves wilt"],
           ["Water", "Temperature", "Carbon dioxide", "Light"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "B",
           "Identifying the limiting factor",
           "By Blackman's law, the rate of a process affected by several factors is set by the factor nearest to its "
           "minimal value. On a shaded forest floor light limits. C3 crops such as tomatoes respond to higher CO2 with "
           "higher yields. NCERT's example: despite a green leaf and optimal light and CO2, a plant may not "
           "photosynthesise if the temperature is very low. Water stress closes stomata (reducing CO2 availability) "
           "and wilts leaves.",
           ["A -> light", "B -> carbon dioxide", "C -> temperature", "D -> water"],
           why="The wrong codes swap light and CO2, temperature and water, or CO2 and temperature.",
           ncert=ref("PS", "Factors affecting Photosynthesis"), secs=45)

direct(T_PS, "Site and pigments", "Intermediate",
       "When the action spectrum of photosynthesis is compared with the absorption spectrum of chlorophyll a, the two "
       "closely overlap. From this NCERT concludes that:",
       "most photosynthesis takes place in the blue and red regions, though some takes place at other wavelengths of "
       "the visible spectrum",
       ["photosynthesis takes place only in red light", "photosynthesis is highest in the green region of the spectrum",
        "no photosynthesis at all takes place outside the blue and red regions"], "D",
       "Action and absorption spectra",
       "The wavelengths at which chlorophyll a shows maximum absorption (blue and red) also show a higher rate of "
       "photosynthesis, so chlorophyll a is the chief pigment. Taken together, the graphs show that most "
       "photosynthesis takes place in the blue and red regions of the spectrum; some photosynthesis does take place "
       "at the other wavelengths of the visible spectrum.",
       ["Action spectrum overlaps the absorption spectrum of chlorophyll a",
        "Most photosynthesis in blue and red; some at other visible wavelengths"],
       why="Blue light also drives much photosynthesis, so it is not red alone. The green region shows low absorption "
           "and a low rate. NCERT notes that some photosynthesis does occur at other visible wavelengths.",
       ncert=ref("PS", "How many Pigments are involved in Photosynthesis?"), secs=35)

multi_statement(T_PS, "Limiting factors", "Advanced",
                "Which of the following statements about the response of C3 and C4 plants to CO2 concentration are "
                "correct?",
                [("C4 plants show saturation at about 360 µL L⁻¹ of CO2.", True),
                 ("In C3 plants, saturation is seen only beyond 450 µL L⁻¹ of CO2.", True),
                 ("At low light conditions, neither C3 nor C4 plants respond to high CO2 conditions.", True),
                 ("At high light intensities, only C4 plants show an increase in the rate of photosynthesis.", False),
                 ("The current availability of CO2 is limiting to C3 plants.", True)],
                [("a", "b", "c", "d"), ("a", "b", "e"), ("b", "c", "d", "e")], "C",
                "CO2 as a limiting factor",
                "C3 and C4 plants respond differently to CO2. At low light neither responds to high CO2. At high light "
                "intensities both C3 and C4 plants show an increase in the rate of photosynthesis. C4 plants show "
                "saturation at about 360 µL L⁻¹, while C3 plants respond to increased CO2 and saturate only beyond "
                "450 µL L⁻¹. Thus the current availability of CO2 is limiting to C3 plants.",
                ["(a), (b), (c), (e) true", "(d) false; at high light both C3 and C4 plants respond"],
                ncert=ref("PS", "Factors affecting Photosynthesis (carbon dioxide concentration)"), secs=60)

assertion_reason(T_PS, "Chemiosmosis", "Advanced",
                 "ATP is synthesised as protons move from the thylakoid lumen to the stroma through the CF0 channel of "
                 "ATP synthase.",
                 "The breakdown of the proton gradient releases enough energy to cause a conformational change in the "
                 "CF1 particle, which makes the enzyme synthesise ATP.",
                 True, True, True, "A",
                 "Coupling the proton gradient to ATP synthesis",
                 "The proton gradient is broken down by the movement of protons across the membrane to the stroma "
                 "through the transmembrane channel of the CF0 of ATP synthase. This breakdown provides enough energy to "
                 "cause a conformational change in the CF1 particle, which makes the enzyme synthesise several "
                 "molecules of energy-packed ATP.",
                 ["A: true", "R: true", "R gives the mechanism by which proton flow yields ATP"],
                 ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=45)

direct(T_PS, "Light reactions and photophosphorylation", "Advanced",
       "An illuminated chloroplast receives only light of wavelengths beyond 680 nm. Which of the following is "
       "expected?",
       "ATP is formed by cyclic photophosphorylation, but no NADPH + H+ is formed and no O2 is evolved.",
       ["ATP, NADPH + H+ and O2 are all formed by non-cyclic photophosphorylation.",
        "NADPH + H+ is formed, but no ATP.", "No photophosphorylation of any kind takes place."], "B",
       "Light beyond 680 nm",
       "Cyclic photophosphorylation also occurs when only light of wavelengths beyond 680 nm is available for "
       "excitation. In it only PS I is functional and the electron circulates within the photosystem, giving ATP but "
       "no NADPH + H+. The water-splitting complex is associated with PS II, which does not take part, so no O2 is "
       "evolved.",
       ["Light > 680 nm -> cyclic photophosphorylation", "Cyclic: only PS I; ATP only; no water splitting"],
       why="Non-cyclic flow needs PS II working in series with PS I. Cyclic flow makes ATP, not NADPH. "
           "Photophosphorylation does continue, by the cyclic route.",
       ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation"), secs=50)

statement_pair(T_PS, "Site and pigments", "Advanced",
               "A single chlorophyll a molecule forms the reaction centre of each photosystem, and the reaction centres "
               "of the two photosystems are different.",
               "The antennae (light-harvesting system) of a photosystem contain no chlorophyll a.",
               True, False, "C",
               "Reaction centre and antennae",
               "The pigments are organised into light-harvesting complexes within PS I and PS II. In each photosystem "
               "all the pigments except one molecule of chlorophyll a form the light-harvesting system or antennae. "
               "The single chlorophyll a molecule forms the reaction centre, which differs between the two "
               "photosystems (P700 in PS I, P680 in PS II). Since only one chlorophyll a molecule is left out of the "
               "antennae, the other chlorophyll a molecules are part of it.",
               ["Statement I: true",
                "Statement II: false; all pigments except one chlorophyll a molecule form the antennae"],
               ncert=ref("PS", "What is Light Reaction?"), secs=50)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "In C4 plants, the Calvin cycle in the bundle sheath cells is supplied with CO2 released from a C4 "
                 "acid.",
                 "The bundle sheath cells of C4 plants have many intercellular spaces through which atmospheric CO2 "
                 "reaches RuBisCO directly.",
                 True, False, False, "C",
                 "CO2 supply in the bundle sheath",
                 "In C4 plants, atmospheric CO2 is fixed by PEPcase in the mesophyll cells into OAA, which forms malic or "
                 "aspartic acid that is transported to the bundle sheath cells. There the C4 acid is broken down to "
                 "release CO2, which enters the Calvin cycle. The bundle sheath cells have thick walls impervious to "
                 "gaseous exchange and no intercellular spaces.",
                 ["A: true", "R: false; bundle sheath cells lack intercellular spaces and are impervious to gases"],
                 ncert=ref("PS", "The C4 Pathway"), secs=45)
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
    assert pkg["output"] == "batches/parts/BATCH_009_BOT_p1.json"


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
           "notes": "Package BOT_009_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, "
                    "Anatomy, Cell, Cell Cycle, Photosynthesis. 123 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
