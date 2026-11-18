"""Writes batches/parts/BATCH_010_BOT_p1.json: package BOT_010_p1 of batch 10 (Botany, 125 questions).

Topics (in plan order): The Living World and Classification, Plant Kingdom, Morphology of Flowering Plants,
Anatomy of Flowering Plants, Cell: The Unit of Life, Cell Cycle and Cell Division, Photosynthesis,
Respiration in Plants, Plant Growth and Development. IDs NEET_BOT_002251 .. NEET_BOT_002375.

Every fact is from the rationalised NCERT Class 11 Biology textbook (reference on every question). Content removed in
the rationalised books or outside the NMC 2026 list (secondary growth, taxonomical aids, plant life cycles and
alternation of generations, early experiments on photosynthesis) is not used. Facts already tested in batches 1-9 were
listed with `merge_batch.py stems 10 BOT_010_p1` and avoided; where a topic is saturated, questions test new
combinations, comparisons, identifications or applications. Before writing:
  * numerical answers are recomputed here (assert);
  * assertion-reason and two-statement keys are derived from the truth values given for each statement;
  * multi-statement keys are derived from the truth value of each statement and must sit at the chosen position;
  * the quota per (topic, difficulty), the ID range, the format shares and the answer-key balance are checked.
The correct position of every direct, numerical, match-list and multi-statement question is written by hand in its
call (argument `at`) and never moved by code. If any check fails, nothing is written.

    python docs/neet-bank/tools/batch_010/BOT_010_p1.py
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
PLAN = ROOT / "batches" / "plans" / "BATCH_010_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_010_BOT_p1.json"
PACKAGE = "BOT_010_p1"
BATCH = "BATCH_010"
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


# =============================================================== 1. The Living World and Classification (5/6/5)
direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "Linnaeus used the term 'Systema' in the title of his publication, from which the word 'systematics' is "
       "derived. The title of that publication, as given in NCERT, is:",
       "Systema Naturae",
       ["Species Plantarum", "Genera Plantarum", "Origin of Species"], "A",
       "Origin of the word systematics",
       "The word systematics is derived from the Latin word 'systema', which means systematic arrangement of "
       "organisms. NCERT notes that Linnaeus used Systema Naturae as the title of his publication.",
       ["Systematics <- Latin 'systema'", "Linnaeus's publication: Systema Naturae"],
       why="NCERT names only Systema Naturae as Linnaeus's publication in this context. Origin of Species is "
           "Darwin's book; the other two titles are not the one NCERT cites.",
       ncert=ref("LW", "Diversity in the Living World (systematics)"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "NCERT states that plant families like Convolvulaceae and Solanaceae are included in one order, mainly on the "
       "basis of floral characters. That order is:",
       "Polymoniales",
       ["Sapindales", "Poales", "Primata"], "C",
       "Order as an assemblage of families",
       "An order is an assemblage of families that exhibit a few similar characters. NCERT's example: plant "
       "families like Convolvulaceae and Solanaceae are included in the order Polymoniales, mainly based on floral "
       "characters.",
       ["Order = assemblage of families with a few similar characters",
        "Convolvulaceae + Solanaceae -> order Polymoniales"],
       why="Sapindales is the order of mango and Poales the order of wheat in NCERT's table. Primata is an animal "
           "order (monkey, gorilla, gibbon).",
       ncert=ref("LW", "Taxonomic categories (order)"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "In taxonomic studies, a group of individual organisms with fundamental similarities, which can be "
       "distinguished from other closely related groups on the basis of distinct morphological differences, is "
       "considered a:",
       "species",
       ["genus", "family", "order"], "B",
       "Species as the basic taxonomic category",
       "NCERT: taxonomic studies consider a group of individual organisms with fundamental similarities as a "
       "species. One should be able to distinguish one species from the other closely related species on the basis "
       "of the distinct morphological differences.",
       ["Group of individuals with fundamental similarities = species",
        "Species are told apart by distinct morphological differences"],
       why="A genus is a group of related species, a family a group of related genera and an order an assemblage "
           "of families; none of these is a group of individuals with fundamental similarities.",
       ncert=ref("LW", "Taxonomic categories (species)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Amoeboid protozoans such as Amoeba move and capture their prey by putting out:",
       "pseudopodia (false feet)",
       ["cilia arranged in rows", "two flagella of unequal length", "a protein-rich pellicle"], "D",
       "Locomotion in amoeboid protozoans",
       "Amoeboid protozoans live in fresh water, sea water or moist soil. They move and capture their prey by "
       "putting out pseudopodia (false feet), as in Amoeba.",
       ["Amoeboid protozoans: pseudopodia", "Used both for movement and for capturing prey"],
       why="Rows of cilia are found in ciliated protozoans such as Paramoecium. Two unequal flagella and a "
           "pellicle are features of euglenoids such as Euglena.",
       ncert=ref("BC", "Kingdom Protista (protozoans)"), secs=20)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Basic",
               "Rod-shaped bacteria are called bacilli (singular: bacillus).",
               "Spherical bacteria are called cocci (singular: coccus).",
               True, True, "A",
               "Shapes of bacteria",
               "NCERT groups bacteria into four categories by shape: spherical coccus (pl. cocci), rod-shaped "
               "bacillus (pl. bacilli), comma-shaped vibrium (pl. vibrio) and spiral spirillum (pl. spirilla).",
               ["Statement I: rod-shaped = bacillus, true", "Statement II: spherical = coccus, true"],
               ncert=ref("BC", "Kingdom Monera"), secs=25)

direct(T_LIV, "Five kingdom classification", "Intermediate",
       "In NCERT's table of the characteristics of the five kingdoms, the body organisation described as "
       "'tissue/organ/organ system' belongs to kingdom:",
       "Animalia",
       ["Plantae", "Fungi", "Protista"], "B",
       "Body organisation in the five kingdoms",
       "In Whittaker's table, body organisation is: Monera and Protista - cellular; Fungi - multicellular/loose "
       "tissue; Plantae - tissue/organ; Animalia - tissue/organ/organ system. Only the animal kingdom is credited "
       "with the organ-system level.",
       ["Plantae: tissue/organ", "Animalia: tissue/organ/organ system", "Organ-system level -> Animalia"],
       why="Plantae is given only 'tissue/organ'. Fungi have 'multicellular/loose tissue' and Protista 'cellular' "
           "body organisation.",
       ncert=ref("BC", "Introduction (table: characteristics of the five kingdoms)"), secs=30)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "The spores of slime moulds can survive for many years, even under adverse conditions.",
                 "The spores of slime moulds possess true walls and are extremely resistant.",
                 True, True, True, "A",
                 "Survival of slime-mould spores",
                 "Under unfavourable conditions the plasmodium of a slime mould forms fruiting bodies bearing spores "
                 "at their tips. NCERT states that the spores possess true walls; they are extremely resistant and "
                 "survive for many years, even under adverse conditions. The resistant, true-walled spore is what "
                 "lets it survive so long.",
                 ["A: true", "R: true", "True walls make the spores extremely resistant, which is why they survive "
                  "for years -> R explains A"],
                 ncert=ref("BC", "Kingdom Protista (slime moulds)"), secs=40)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Intermediate",
               "In basidiomycetes, the dikaryotic structure formed after plasmogamy ultimately gives rise to the "
               "basidium.",
               "In basidiomycetes, the basidia are arranged in fruiting bodies called ascocarps.",
               True, False, "C",
               "Sexual cycle of basidiomycetes",
               "In basidiomycetes, plasmogamy is by fusion of two somatic cells of different strains. The resulting "
               "structure is dikaryotic, which ultimately gives rise to the basidium. Karyogamy and meiosis take "
               "place in the basidium, producing four basidiospores. The basidia are arranged in fruiting bodies "
               "called basidiocarps; ascocarps are the fruiting bodies of ascomycetes.",
               ["Statement I: dikaryon -> basidium, true", "Statement II: basidia lie in basidiocarps, not "
                "ascocarps; false"],
               ncert=ref("BC", "Kingdom Fungi (Basidiomycetes)"), secs=35)

match_list(T_LIV, "Taxonomy and hierarchy", "Intermediate", "term", "meaning as given in NCERT",
           ["Identification", "Nomenclature", "Classification", "Systematics"],
           ["Grouping into convenient categories based on some easily observable characters",
            "Describing an organism correctly so that we know to what organism a name is attached",
            "A study that takes into account evolutionary relationships between organisms",
            "Naming of an organism according to standardised rules and criteria"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "A",
           "Basic terms of taxonomy",
           "Nomenclature (naming) is possible only when the organism is described correctly and we know to what "
           "organism the name is attached - this is identification. Nomenclature gives scientific names according "
           "to agreed principles and criteria. Classification is the process by which anything is grouped into "
           "convenient categories based on some easily observable characters. Systematics deals with the "
           "classification of organisms and takes into account evolutionary relationships between them.",
           ["Identification -> II", "Nomenclature -> IV", "Classification -> I", "Systematics -> III"],
           why="The wrong codes swap identification with nomenclature, classification with systematics, or "
               "nomenclature with classification.",
           ncert=ref("LW", "Diversity in the Living World"), secs=50)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about fungi are correct?",
                [("In ascomycetes, conidia on germination produce mycelium.", True),
                 ("Penicillium is a multicellular ascomycete, whereas yeast (Saccharomyces) is a unicellular one.",
                  True),
                 ("In basidiomycetes, vegetative reproduction by fragmentation is common.", True),
                 ("Phycomycetes are found only in aquatic habitats.", False),
                 ("In ascomycetes, the conidiophores bear ascospores.", False)],
                [("a", "b"), ("a", "b", "c", "e"), ("b", "c", "d")], "C",
                "Features of classes of fungi",
                "Ascomycetes are mostly multicellular (Penicillium) or rarely unicellular (yeast, Saccharomyces). "
                "Their asexual spores, conidia, are produced exogenously on conidiophores and on germination "
                "produce mycelium; the sexual spores, ascospores, are produced endogenously in asci. In "
                "basidiomycetes asexual spores are generally not found, but vegetative reproduction by "
                "fragmentation is common. Phycomycetes occur in aquatic habitats, on decaying wood in moist and "
                "damp places, or as obligate parasites on plants.",
                ["(a) true", "(b) true", "(c) true", "(d) false: also on decaying wood and as obligate parasites "
                 "on plants", "(e) false: conidiophores bear conidia; ascospores form in asci"],
                why="(a) and (b) only leaves out the true statement (c). The other combinations include (d) or (e).",
                ncert=ref("BC", "Kingdom Fungi"), secs=60)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "In ciliated protozoans such as Paramoecium, the coordinated movement of rows of cilia causes the water laden "
       "with food to be steered into the:",
       "gullet",
       ["contractile vacuole", "pseudopodium", "spore-like infectious stage"], "A",
       "Feeding in ciliated protozoans",
       "Ciliated protozoans are aquatic, actively moving organisms because of the presence of thousands of cilia. "
       "They have a cavity (gullet) that opens to the outside of the cell surface. The coordinated movement of rows "
       "of cilia causes the water laden with food to be steered into the gullet.",
       ["Ciliated protozoans: thousands of cilia and a gullet", "Rows of cilia steer food-laden water into the "
        "gullet"],
       why="Pseudopodia are put out by amoeboid protozoans; an infectious spore-like stage is a feature of "
           "sporozoans. NCERT does not describe the cilia as steering food into a contractile vacuole.",
       ncert=ref("BC", "Kingdom Protista (protozoans)"), secs=30)

numerical(T_LIV, "Monera, Protista and Fungi", "Advanced",
          "NCERT lists the spores by which fungi reproduce. How many of the following are listed as SEXUAL spores "
          "of fungi?\n\nconidia, sporangiospores, zoospores, oospores, ascospores, basidiospores",
          "3", ["2", "4", "6"], "B",
          len([s for s, sexual in [("conidia", False), ("sporangiospores", False), ("zoospores", False),
                                   ("oospores", True), ("ascospores", True), ("basidiospores", True)]
               if sexual]) == 3,
          "Asexual and sexual spores of fungi",
          "NCERT: in fungi, asexual reproduction is by spores called conidia or sporangiospores or zoospores, and "
          "sexual reproduction is by oospores, ascospores and basidiospores.",
          ["Asexual: conidia, sporangiospores, zoospores", "Sexual: oospores, ascospores, basidiospores",
           "Count of sexual spores = 3"],
          why="2 leaves out the oospore, which is often forgotten. 4 wrongly counts zoospores as sexual because they "
              "are motile. 6 counts every spore as sexual.",
          ncert=ref("BC", "Kingdom Fungi"), secs=45)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "According to NCERT's table of the characteristics of the five kingdoms, which of the following are "
                "true of BOTH kingdom Monera and kingdom Fungi?",
                [("A cell wall is present, and it is not made of cellulose.", True),
                 ("A nuclear membrane is present.", False),
                 ("Heterotrophic nutrition (saprophytic or parasitic) is found among their members.", True),
                 ("Body organisation is multicellular/loose tissue.", False),
                 ("The cell type is eukaryotic.", False)],
                [("a", "b", "c"), ("c", "d"), ("a", "c", "e")], "D",
                "Comparing Monera and Fungi",
                "In the table, Monera: prokaryotic, cell wall non-cellulosic (polysaccharide + amino acid), nuclear "
                "membrane absent, cellular body organisation, nutrition autotrophic (chemosynthetic and "
                "photosynthetic) and heterotrophic (saprophytic/parasitic). Fungi: eukaryotic, cell wall present "
                "(without cellulose), nuclear membrane present, multicellular/loose tissue, heterotrophic "
                "(saprophytic/parasitic).",
                ["(a) both have non-cellulosic walls: true", "(b) Monera lack a nuclear membrane: false",
                 "(c) both include saprophytic/parasitic heterotrophs: true",
                 "(d) Monera are cellular: false", "(e) Monera are prokaryotic: false"],
                why="The other combinations include (b), (d) or (e), each of which holds only for Fungi.",
                ncert=ref("BC", "Introduction (table: characteristics of the five kingdoms)"), secs=70)

assertion_reason(T_LIV, "Taxonomy and hierarchy", "Advanced",
                 "The higher the taxonomic category, the greater is the difficulty of determining its relationship "
                 "to other taxa at the same level.",
                 "As we go higher from species to kingdom, the number of common characteristics goes on decreasing.",
                 True, True, True, "A",
                 "Characters shared at different levels of the hierarchy",
                 "NCERT: as we go higher from species to kingdom, the number of common characteristics goes on "
                 "decreasing; the lower the taxon, the more characteristics its members share. Because members of a "
                 "higher category share fewer characters, it becomes harder to determine its relationship to other "
                 "taxa at the same level, and the problem of classification becomes more complex.",
                 ["A: true", "R: true", "Fewer shared characters at higher levels is why relationships are harder "
                  "to judge -> R explains A"],
                 ncert=ref("LW", "Taxonomic categories"), secs=45)

statement_pair(T_LIV, "Binomial nomenclature", "Advanced",
               "In the name Panthera tigris, 'Panthera' is the generic name and 'tigris' is the specific epithet.",
               "Lion (Panthera leo), leopard (P. pardus) and tiger (P. tigris) have different specific epithets and "
               "therefore belong to three different genera.",
               True, False, "C",
               "Genus and specific epithet",
               "In a binomial, the first word is the genus and the second the specific epithet. NCERT notes that "
               "lion (Panthera leo), leopard (P. pardus) and tiger (P. tigris), with several common features, are "
               "all species of the same genus Panthera. A different specific epithet marks a different species, "
               "not a different genus.",
               ["Statement I: true", "Statement II: false; one genus (Panthera), three species"],
               ncert=ref("LW", "Taxonomic categories (genus)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Deuteromycetes are placed in a separate class because their mycelium is aseptate and coenocytic.",
                 "When the sexual forms of deuteromycetes are discovered, they are moved to ascomycetes and "
                 "basidiomycetes.",
                 False, True, False, "D",
                 "Why the deuteromycetes form a separate class",
                 "Deuteromycetes (imperfect fungi) are grouped together because only their asexual or vegetative "
                 "phases are known; their mycelium is septate and branched, not aseptate. NCERT adds that when the "
                 "sexual forms of these fungi are discovered, they are moved into the classes they rightly belong "
                 "to, ascomycetes and basidiomycetes.",
                 ["A: false - the mycelium is septate and branched; the grouping rests on the unknown sexual stage",
                  "R: true"],
                 ncert=ref("BC", "Kingdom Fungi (Deuteromycetes)"), secs=40)

# =============================================================== 2. Plant Kingdom (5/6/5)
direct(T_PK, "Gymnosperms", "Basic",
       "In gymnosperms, the pollen tube carrying the male gametes grows towards the archegonia in the ovules. "
       "According to NCERT, it discharges its contents:",
       "near the mouth of the archegonia",
       ["inside the microsporangium", "on the surface of the megasporophyll, outside the ovule",
        "into the soil, where the gametes swim to the ovule"], "B",
       "Fertilisation in gymnosperms",
       "Pollen grains released from the microsporangium are carried by air currents to the opening of the ovules "
       "borne on megasporophylls. The pollen tube carrying the male gametes grows towards the archegonia in the "
       "ovules and discharges its contents near the mouth of the archegonia.",
       ["Pollen reaches the opening of the ovule", "Pollen tube grows to the archegonia",
        "Contents discharged near the mouth of the archegonia"],
       why="The microsporangium is where pollen grains develop, not where they discharge gametes. The tube grows "
           "inside the ovule, not on the megasporophyll surface, and gymnosperm gametes are not released into the "
           "soil.",
       ncert=ref("PK", "Gymnosperms"), secs=25)

direct(T_PK, "Algae", "Basic",
       "NCERT notes that, besides living in water, some algae occur in association with fungi and some with "
       "animals. The association of algae with fungi is seen in:",
       "lichens",
       ["mycorrhiza", "the coralloid roots of Cycas", "the fur of the sloth bear"], "C",
       "Habitats and associations of algae",
       "Algae are largely aquatic, but also occur on moist stones, soils and wood. Some of them also occur in "
       "association with fungi (lichen) and animals (e.g., on sloth bear).",
       ["Algae + fungi -> lichen", "Algae + animal -> e.g., on sloth bear"],
       why="Mycorrhiza is a fungus associated with the roots of higher plants (e.g., Pinus). The coralloid roots of "
           "Cycas are associated with nitrogen-fixing cyanobacteria, and algae on the sloth bear are NCERT's example "
           "of association with an animal.",
       ncert=ref("PK", "Algae"), secs=20)

direct(T_PK, "Gymnosperms", "Basic",
       "Which of the following is NOT a gymnosperm?",
       "Salvinia",
       ["Ginkgo", "Cedrus", "Sequoia"], "D",
       "Identifying gymnosperms",
       "Ginkgo, Cedrus and Sequoia (the giant redwood, one of the tallest tree species) are gymnosperms. Salvinia is "
       "a heterosporous pteridophyte.",
       ["Ginkgo, Cedrus, Sequoia: gymnosperms", "Salvinia: heterosporous pteridophyte"],
       why="Ginkgo and Cedrus are gymnosperm examples in NCERT, and Sequoia is named as a gymnosperm that is one "
           "of the tallest tree species.",
       ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=20)

statement_pair(T_PK, "Pteridophytes", "Basic",
               "Pteridophytes are used for medicinal purposes and as soil-binders, and are frequently grown as "
               "ornamentals.",
               "Although pteridophytes are found in cool, damp, shady places, some may flourish well in sandy-soil "
               "conditions.",
               True, True, "A",
               "Uses and habitat of pteridophytes",
               "NCERT: pteridophytes include horsetails and ferns. They are used for medicinal purposes and as "
               "soil-binders, and are frequently grown as ornamentals. They are found in cool, damp, shady places, "
               "though some may flourish well in sandy-soil conditions.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Pteridophytes"), secs=25)

direct(T_PK, "Algae", "Basic",
       "In members of Chlorophyceae (green algae), the plant body may be:",
       "unicellular, colonial or filamentous",
       ["only unicellular", "always filamentous and attached by rhizoids",
        "always massive, with a holdfast, a stipe and a frond"], "A",
       "Body form of green algae",
       "NCERT: in Chlorophyceae the plant body may be unicellular, colonial or filamentous (e.g., Chlamydomonas, "
       "Volvox, Ulothrix). They are usually grass green because chlorophyll a and b dominate.",
       ["Green algae: unicellular, colonial or filamentous"],
       why="Green algae are not restricted to one body form. Rhizoids attach bryophytes, and a holdfast, stipe and "
           "frond describe the body of brown algae.",
       ncert=ref("PK", "Algae (Chlorophyceae)"), secs=20)

multi_statement(T_PK, "Bryophytes", "Intermediate",
                "Which of the following structures are diploid?",
                [("The seta of a moss", True),
                 ("The megaspore mother cell in the ovule of a gymnosperm", True),
                 ("A leaf of a fern", True),
                 ("The protonema of a moss", False),
                 ("An antherozoid of a fern", False)],
                [("a", "b"), ("b", "c", "e"), ("a", "c", "d")], "B",
                "Haploid and diploid structures in plant groups",
                "In mosses the zygote develops into the sporophyte (foot, seta and capsule), which is diploid; the "
                "spores formed in it by meiosis give the haploid protonema. In gymnosperms the megaspore mother "
                "cell, differentiated from a cell of the nucellus, is diploid and divides meiotically. In ferns the "
                "main plant body, with its leaves, is the diploid sporophyte, while the antherozoids are produced on "
                "the haploid gametophyte.",
                ["(a) seta: part of the sporophyte -> 2n", "(b) megaspore mother cell -> 2n (divides by meiosis)",
                 "(c) fern leaf: sporophyte -> 2n", "(d) protonema: gametophyte -> n",
                 "(e) antherozoid: male gamete -> n"],
                why="(a) and (b) only leaves out the fern leaf. The other combinations include the haploid "
                    "antherozoid or the haploid protonema.",
                ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Members of Phaeophyceae vary in colour from olive green to various shades of brown.",
                 "In members of Phaeophyceae, chlorophyll b is the main pigment.",
                 True, False, False, "C",
                 "Pigments of brown algae",
                 "Brown algae possess chlorophyll a and c, carotenoids and xanthophylls. They vary in colour from "
                 "olive green to various shades of brown depending upon the amount of the xanthophyll pigment "
                 "fucoxanthin. Chlorophyll b is the pigment of green algae (with chlorophyll a); it is not present "
                 "in brown algae.",
                 ["A: true", "R: false - brown algae have chlorophyll a and c; their colour depends on fucoxanthin"],
                 ncert=ref("PK", "Algae (Phaeophyceae)"), secs=35)

statement_pair(T_PK, "Gymnosperms", "Intermediate",
               "In gymnosperms, the ovules are borne on megasporophylls, which may be clustered to form the female "
               "cones.",
               "In gymnosperms, the multicellular female gametophyte bears only a single archegonium.",
               True, False, "C",
               "Ovules and female gametophyte of gymnosperms",
               "NCERT: the ovules are borne on megasporophylls, which may be clustered to form the female cones. The "
               "megaspore mother cell divides meiotically to form four megaspores; one of them develops into a "
               "multicellular female gametophyte that bears two or more archegonia (female sex organs).",
               ["Statement I: true", "Statement II: false; the female gametophyte bears two or more archegonia"],
               ncert=ref("PK", "Gymnosperms"), secs=35)

match_list(T_PK, "Bryophytes", "Intermediate", "structure in bryophytes", "description",
           ["Archegonium", "Antheridium", "Gemma", "Protonema"],
           ["Creeping, green, branched and frequently filamentous stage that develops directly from a spore",
            "Green, multicellular, asexual bud that develops in a small receptacle on the thallus",
            "Flask-shaped sex organ that produces a single egg",
            "Sex organ that produces biflagellate antherozoids"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C",
           "Structures of bryophytes",
           "The archegonium (female sex organ) is flask-shaped and produces a single egg; the antheridium (male sex "
           "organ) produces biflagellate antherozoids. Gemmae are green, multicellular, asexual buds that develop in "
           "small receptacles called gemma cups on liverwort thalli. The protonema is the first stage of the moss "
           "gametophyte: creeping, green, branched and frequently filamentous, developing directly from a spore.",
           ["Archegonium -> III", "Antheridium -> IV", "Gemma -> II", "Protonema -> I"],
           why="The wrong codes swap the two sex organs, the gemma and the protonema, or the antheridium and the "
               "gemma.",
           ncert=ref("PK", "Bryophytes"), secs=45)

multi_statement(T_PK, "Pteridophytes", "Intermediate",
                "Which of the following statements are correct for a fern such as Dryopteris?",
                [("Its main plant body is a sporophyte differentiated into true root, stem and leaves.", True),
                 ("Its leaves are large (macrophylls).", True),
                 ("Its gametophyte needs cool, damp, shady places to grow.", True),
                 ("Its sporophyte remains attached to and nourished by the gametophyte throughout life.", False),
                 ("Its ovules are not enclosed by an ovary wall.", False)],
                [("a", "b", "c", "e"), ("a", "c"), ("b", "c", "d")], "D",
                "Features of ferns",
                "In pteridophytes the main plant body is a sporophyte with true root, stem and leaves; the leaves "
                "are small (microphylls) as in Selaginella or large (macrophylls) as in ferns. The spores give rise "
                "to a small, free-living, mostly photosynthetic gametophyte (prothallus), which needs cool, damp, "
                "shady places to grow. The sporophyte is the dominant, independent phase, and pteridophytes form no "
                "ovules or seeds.",
                ["(a) true", "(b) true: macrophylls as in ferns", "(c) true", "(d) false: that is the bryophyte "
                 "condition", "(e) false: ferns have no ovules"],
                why="The other combinations either add (d) or (e), or leave out the true statement (b).",
                ncert=ref("PK", "Pteridophytes"), secs=55)

direct(T_PK, "Bryophytes", "Intermediate",
       "In which of the following plants is the dominant, independent, photosynthetic phase haploid?",
       "Polytrichum",
       ["Pteris", "Cycas", "Selaginella"], "A",
       "Dominant phase in different plant groups",
       "In bryophytes such as the moss Polytrichum, the main plant body is haploid; it produces gametes and is "
       "called a gametophyte. In pteridophytes (Pteris, Selaginella) and gymnosperms (Cycas), the main plant body "
       "is the diploid sporophyte.",
       ["Moss: dominant phase = gametophyte (n)", "Fern, Selaginella, Cycas: dominant phase = sporophyte (2n)"],
       why="Pteris and Selaginella are pteridophytes and Cycas is a gymnosperm; in all three the dominant, "
           "independent plant is the diploid sporophyte.",
       ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=30)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following are true of members of Chlorophyceae but NOT of members of Phaeophyceae, "
                "according to NCERT's table of the divisions of algae?",
                [("Chlorophyll b is present.", True),
                 ("The stored food is starch.", True),
                 ("The motile cells bear 2-8 equal, apical flagella.", True),
                 ("Cellulose is a component of the cell wall.", False),
                 ("Members occur in brackish water and salt water.", False)],
                [("a", "b"), ("a", "c", "d"), ("b", "c", "e")], "C",
                "Comparing green and brown algae",
                "Chlorophyceae: chlorophyll a and b; stored food starch; cell wall of cellulose; 2-8 equal, apical "
                "flagella; fresh, brackish and salt water. Phaeophyceae: chlorophyll a and c with fucoxanthin; "
                "stored food mannitol and laminarin; cell wall of cellulose and algin; 2 unequal, lateral flagella; "
                "fresh water (rare), brackish and salt water.",
                ["(a), (b), (c) hold only for green algae", "(d) both have cellulose in the wall",
                 "(e) both occur in brackish and salt water"],
                why="(a) and (b) only misses the flagellar difference. The other combinations include (d) or (e), "
                    "which are shared by both classes.",
                ncert=ref("PK", "Algae (table: divisions of algae and their main characteristics)"), secs=70)

numerical(T_PK, "Pteridophytes", "Advanced",
          "How many of the following are formed by meiosis?\n\n(i) Spores in the capsule of a moss\n(ii) The four "
          "megaspores in a gymnosperm ovule\n(iii) Gemmae of Marchantia\n(iv) Microspores of Selaginella\n"
          "(v) Antherozoids of a fern\n(vi) The zygote of a moss",
          "3", ["2", "4", "5"], "C",
          sum([True, True, False, True, False, False]) == 3,
          "Where meiosis occurs in plant groups",
          "Meiosis produces spores: in mosses the spores are formed within the capsule after meiosis; in gymnosperms "
          "the megaspore mother cell divides meiotically to form four megaspores; in pteridophytes, including the "
          "heterosporous Selaginella, the sporangia produce spores by meiosis in spore mother cells. Gemmae are "
          "asexual buds of the haploid thallus, antherozoids are produced in antheridia on the haploid gametophyte, "
          "and a zygote is formed by fusion of gametes - none of these by meiosis.",
          ["By meiosis: (i), (ii), (iv)", "Not by meiosis: (iii) gemmae, (v) antherozoids, (vi) zygote",
           "Count = 3"],
          why="2 leaves out the Selaginella microspores, forgetting that heterosporous spores also arise by meiosis. "
              "4 counts gemmae as meiotic products, and 5 also counts the antherozoids.",
          ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

direct(T_PK, "Gymnosperms", "Advanced",
       "Which of the following is true of the female gametophyte of BOTH Selaginella and Pinus?",
       "It is retained on the parent sporophyte: for variable periods in Selaginella, and within the "
       "megasporangium in Pinus.",
       ["It develops from a microspore.", "It is enclosed within an ovary wall.",
        "It is the dominant, long-lived phase of the plant."], "B",
       "Retention of the female gametophyte",
       "In heterosporous pteridophytes such as Selaginella, the female gametophyte is retained on the parent "
       "sporophyte for variable periods, an event regarded as a precursor to the seed habit. In gymnosperms such "
       "as Pinus, the multicellular female gametophyte is retained within the megasporangium on the sporophyte.",
       ["Selaginella: female gametophyte retained on parent sporophyte",
        "Pinus: female gametophyte retained within megasporangium", "Common feature: retention"],
       why="Female gametophytes develop from megaspores, not microspores. Neither plant has an ovary, and in both "
           "the dominant phase is the sporophyte.",
       ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=45)

statement_pair(T_PK, "Pteridophytes", "Advanced",
               "In both Selaginella and Pinus, the sporophylls are arranged to form strobili (cones).",
               "In both Salvinia and Cycas, the ovules develop into naked seeds after fertilisation.",
               True, False, "C",
               "Strobili and seeds compared",
               "In some pteridophytes, such as Selaginella and Equisetum, the sporophylls form compact strobili. In "
               "gymnosperms such as Pinus, sporophylls are arranged spirally along an axis to form lax or compact "
               "strobili or cones. Salvinia, however, is a heterosporous pteridophyte; it forms no ovules or seeds. "
               "Only gymnosperms such as Cycas have naked seeds.",
               ["Statement I: true", "Statement II: false; Salvinia is a pteridophyte and has no seeds"],
               ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=45)

match_list(T_PK, "Gymnosperms", "Advanced", "structure in a gymnosperm", "origin or composition",
           ["Pollen grain", "Ovule", "Female gametophyte", "Seed"],
           ["Develops from one of the four megaspores", "Develops from the ovule after fertilisation",
            "Highly reduced male gametophyte developing from a microspore within the microsporangium",
            "Nucellus together with the envelopes that protect it"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D",
           "Origin of gymnosperm structures",
           "Microspores develop into a highly reduced male gametophyte, the pollen grain, within the microsporangia. "
           "The nucellus, protected by envelopes, forms the ovule. The megaspore mother cell in the nucellus forms "
           "four megaspores by meiosis, and one of them develops into the multicellular female gametophyte. After "
           "fertilisation the zygote forms the embryo and the ovules develop into seeds.",
           ["Pollen grain -> III", "Ovule -> IV", "Female gametophyte -> I", "Seed -> II"],
           why="The wrong codes swap the pollen grain and the ovule, the female gametophyte and the seed, or the ovule "
               "and the female gametophyte.",
           ncert=ref("PK", "Gymnosperms"), secs=55)

# =============================================================== 3. Morphology of Flowering Plants (5/6/5)
direct(T_MOR, "Flower", "Basic",
       "After fertilisation in a flower, according to NCERT:",
       "the ovules develop into seeds and the ovary matures into a fruit",
       ["the ovary develops into a seed and the ovules into the fruit wall",
        "the stigma and style develop into the fruit",
        "the thalamus develops into the seed coat and the ovules disappear"], "D",
       "Fate of the ovary and ovules",
       "NCERT (gynoecium): after fertilisation, the ovules develop into seeds and the ovary matures into a fruit. "
       "The fruit is thus a mature or ripened ovary.",
       ["Ovules -> seeds", "Ovary -> fruit"],
       why="The other options reverse or misplace the fate of the ovary and ovules; NCERT gives the ovules as "
           "forming seeds and the ovary as forming the fruit.",
       ncert=ref("MOR", "The Flower (gynoecium)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In insectivorous plants such as the pitcher plant and the Venus fly trap, the structures that trap insects "
       "are modified:",
       "leaves",
       ["roots", "stems", "inflorescence axes"], "B",
       "Leaf modifications",
       "Leaves are often modified to perform functions other than photosynthesis. NCERT states that the leaves of "
       "certain insectivorous plants, such as the pitcher plant and the Venus fly trap, are also modified leaves.",
       ["Pitcher and Venus fly trap: modified leaves"],
       why="NCERT lists these structures among leaf modifications, along with leaf tendrils (pea), spines (cactus) "
           "and fleshy leaves (onion, garlic); they are not roots, stems or inflorescence axes.",
       ncert=ref("MOR", "The Leaf (modifications of leaves)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In some plants such as Rhizophora growing in swampy areas, many roots come out of the ground and grow "
       "vertically upwards. These roots are called:",
       "pneumatophores",
       ["prop roots", "stilt roots", "fibrous roots"], "A",
       "Pneumatophores",
       "NCERT: in some plants such as Rhizophora growing in swampy areas, many roots come out of the ground and grow "
       "vertically upwards. Such roots, called pneumatophores, help to get oxygen for respiration.",
       ["Upward-growing roots of swamp plants = pneumatophores", "Function: oxygen for respiration"],
       why="Prop roots are the hanging supporting roots of the banyan tree, and stilt roots arise from the lower "
           "nodes of maize and sugarcane. Fibrous roots form the root system of monocots such as wheat.",
       ncert=ref("MOR", "The Root (modifications of root)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In the region of maturation of a root, some epidermal cells form very fine, delicate, thread-like root "
       "hairs. According to NCERT, these root hairs:",
       "absorb water and minerals from the soil",
       ["protect the tender apex of the root", "divide repeatedly to add new cells",
        "elongate rapidly and are responsible for growth in length"], "C",
       "Function of root hairs",
       "Proximal to the region of elongation, cells gradually differentiate and mature (region of maturation). From "
       "this region some epidermal cells form very fine, delicate, thread-like root hairs, which absorb water and "
       "minerals from the soil.",
       ["Root hairs arise in the region of maturation", "They absorb water and minerals"],
       why="Protection of the apex is the job of the root cap. Repeated division is the work of the region of "
           "meristematic activity, and growth in length that of the region of elongation.",
       ncert=ref("MOR", "The Root (regions of the root)"), secs=20)

statement_pair(T_MOR, "Flower", "Basic",
               "The ovary is the enlarged basal part of a carpel.",
               "The style is the elongated tube that connects the ovary to the stigma.",
               True, True, "A",
               "Parts of a carpel",
               "Each carpel is made up of stigma, style and ovary. The ovary is the enlarged basal part, on which lies "
               "the elongated tube, the style. The style connects the ovary to the stigma, which is usually at the "
               "tip of the style and is the receptive surface for pollen grains.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Flower (gynoecium)"), secs=25)

match_list(T_MOR, "Fruit and seed", "Intermediate", "part of a maize grain", "description",
           ["Scutellum", "Coleoptile", "Coleorhiza", "Aleurone layer"],
           ["Sheath enclosing the radicle", "Proteinaceous layer separating the endosperm from the embryo",
            "One large, shield-shaped cotyledon", "Sheath enclosing the plumule"],
           "III IV I II", ["III I IV II", "IV III I II", "III IV II I"], "B",
           "Structure of a monocotyledonous seed",
           "In maize, the embryo is small and lies in a groove at one end of the endosperm. It has one large, "
           "shield-shaped cotyledon called the scutellum and a short axis with a plumule and a radicle. The plumule "
           "and radicle are enclosed in sheaths called the coleoptile and coleorhiza respectively. The outer "
           "covering of the endosperm separates the embryo by a proteinaceous aleurone layer.",
           ["Scutellum -> III", "Coleoptile -> IV (plumule)", "Coleorhiza -> I (radicle)", "Aleurone layer -> II"],
           why="The wrong codes swap the two sheaths, the scutellum and the coleoptile, or the coleorhiza and the "
               "aleurone layer.",
           ncert=ref("MOR", "The Seed (structure of a monocotyledonous seed)"), secs=40)

assertion_reason(T_MOR, "Root, stem and leaf", "Intermediate",
                 "The wheat plant has a fibrous root system.",
                 "In wheat, the primary root is short-lived and is replaced by a large number of roots that "
                 "originate from the base of the stem.",
                 True, True, True, "A",
                 "Fibrous root system",
                 "In most dicots the primary root persists as the tap root. NCERT: in monocotyledonous plants, the "
                 "primary root is short-lived and is replaced by a large number of roots. These roots originate from "
                 "the base of the stem and constitute the fibrous root system, as seen in the wheat plant.",
                 ["A: true", "R: true", "Replacement of the short-lived primary root by many roots from the stem "
                  "base is what forms a fibrous root system -> R explains A"],
                 ncert=ref("MOR", "The Root"), secs=35)

direct(T_MOR, "Root, stem and leaf", "Intermediate",
       "In which of the following pairs are BOTH structures modified leaves?",
       "Tendrils of pea and fleshy storage leaves of onion",
       ["Tendrils of pea and tendrils of cucumber", "Spines of cactus and thorns of Citrus",
        "Green expanded petioles of Australian acacia and the flattened green structure of Opuntia"], "C",
       "Distinguishing leaf and stem modifications",
       "Leaves are modified into tendrils for climbing (pea), spines for defence (cactus) and fleshy storage "
       "organs (onion, garlic). Stem tendrils of cucumber and pumpkin develop from axillary buds; thorns of Citrus "
       "and Bougainvillea are modified axillary buds; Opuntia has a flattened green stem.",
       ["Pea tendril: leaf; onion fleshy leaf: leaf -> both leaves",
        "Cucumber tendril, Citrus thorn and Opuntia's flattened structure: stems"],
       why="Each wrong pair contains one stem modification: cucumber tendrils, Citrus thorns and the flattened "
           "green structure of Opuntia are all modified stems.",
       ncert=ref("MOR", "The Stem; The Leaf (modifications)"), secs=40)

multi_statement(T_MOR, "Plant families", "Intermediate",
                "Which of the following features are common to BOTH the families Fabaceae and Solanaceae, as "
                "described in NCERT?",
                [("The leaves show reticulate venation.", True),
                 ("The calyx has five united sepals (gamosepalous).", True),
                 ("The leaves are stipulate.", False),
                 ("The seeds are endospermous.", False),
                 ("The inflorescence is racemose.", False)],
                [("a", "b", "c"), ("a", "d"), ("b", "e")], "A",
                "Comparing Fabaceae and Solanaceae",
                "Fabaceae: leaves pinnately compound or simple, pulvinate leaf base, stipulate, reticulate venation; "
                "racemose inflorescence; calyx of five gamosepalous sepals; seeds non-endospermic. Solanaceae: "
                "leaves simple (rarely pinnately compound), exstipulate, reticulate venation; inflorescence "
                "solitary, axillary or cymose; calyx of five united, persistent sepals; seeds endospermous.",
                ["(a) both reticulate: true", "(b) both have five united sepals: true",
                 "(c) Solanaceae is exstipulate: false", "(d) Fabaceae seeds are non-endospermic: false",
                 "(e) Solanaceae inflorescence is not racemose: false"],
                why="The other combinations include (c), (d) or (e), each of which holds for only one of the two "
                    "families.",
                ncert=ref("MOR", "Description of Some Important Families (Fabaceae, Solanaceae)"), secs=60)

statement_pair(T_MOR, "Plant families", "Intermediate",
               "In Liliaceae the leaves are mostly basal, linear and show parallel venation, whereas in Solanaceae "
               "the leaves show reticulate venation.",
               "In Fabaceae, the corolla shows valvate aestivation.",
               True, False, "C",
               "Leaves and aestivation in three families",
               "Liliaceae: leaves mostly basal, alternate, linear, exstipulate with parallel venation. Solanaceae: "
               "leaves alternate, simple, exstipulate, with reticulate venation. In Fabaceae the calyx shows "
               "imbricate aestivation and the papilionaceous corolla shows vexillary aestivation.",
               ["Statement I: true", "Statement II: false; the corolla of Fabaceae is vexillary"],
               ncert=ref("MOR", "Description of Some Important Families"), secs=35)

direct(T_MOR, "Flower", "Intermediate",
       "A flower has floral appendages in multiples of five, and its gynoecium occupies the highest position on the "
       "thalamus with the other parts situated below it. Such a flower is described as:",
       "pentamerous and hypogynous",
       ["pentamerous and epigynous", "tetramerous and hypogynous", "trimerous and perigynous"], "B",
       "Merosity and position of floral parts",
       "A flower is trimerous, tetramerous or pentamerous when its floral appendages are in multiples of 3, 4 or 5. "
       "When the gynoecium occupies the highest position and the other parts are situated below it, the flower is "
       "hypogynous and the ovary is superior.",
       ["Multiples of five -> pentamerous", "Gynoecium highest, other parts below -> hypogynous"],
       why="In an epigynous flower the other parts arise above the ovary (inferior ovary). Tetramerous means "
           "multiples of four and trimerous multiples of three; perigynous means the other parts arise on the rim "
           "of the thalamus at about the level of the ovary.",
       ncert=ref("MOR", "The Flower"), secs=35)

multi_statement(T_MOR, "Plant families", "Advanced",
                "A flower has the floral formula ⊕ ⚥ K(5) C(5) A5 G(2), with the stamens epipetalous and the ovary "
                "superior. From NCERT's description of the family to which it belongs, which of the following "
                "would you also expect in this plant?",
                [("The calyx is persistent.", True),
                 ("The fruit is a berry or a capsule.", True),
                 ("The seeds are endospermous.", True),
                 ("The leaf base is pulvinate.", False),
                 ("The leaves show parallel venation.", False)],
                [("a", "b"), ("b", "c", "d"), ("a", "c", "e")], "D",
                "Inferring family characters from a floral formula",
                "⊕ ⚥ K(5) C(5) A5 G(2) with epipetalous stamens and a superior ovary is the floral formula NCERT gives "
                "for Solanaceae. In that family the calyx is persistent, the fruit is a berry or capsule, the seeds "
                "are many and endospermous, and the leaves are simple, exstipulate and reticulately veined. A "
                "pulvinate leaf base belongs to Fabaceae; parallel venation to monocots such as Liliaceae.",
                ["Formula -> Solanaceae", "(a), (b), (c): Solanaceae characters", "(d) Fabaceae character",
                 "(e) monocot character"],
                why="(a) and (b) only leaves out the endospermous seeds. The other combinations include (d) or (e), "
                    "which are not characters of Solanaceae.",
                ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=75)

assertion_reason(T_MOR, "Flower", "Advanced",
                 "In the flower of pea, the stamens are diadelphous.",
                 "The flower of pea is zygomorphic.",
                 True, True, False, "B",
                 "Two independent features of the pea flower",
                 "Stamens united into two bundles, as in pea, are diadelphous (nine united and one free, A(9)+1). The "
                 "pea flower is also zygomorphic: it can be divided into two similar halves only in one vertical "
                 "plane. Symmetry describes how the whole flower can be divided; it says nothing about how the "
                 "filaments of the stamens are united. The two statements are separate features.",
                 ["A: true", "R: true", "Symmetry of the flower does not explain the fusion of stamens into two "
                  "bundles -> R is not the explanation"],
                 ncert=ref("MOR", "The Flower (symmetry; androecium)"), secs=45)

statement_pair(T_MOR, "Flower", "Advanced",
               "The flowers of both pea and brinjal are hypogynous.",
               "The gynoecium of both pea and brinjal is syncarpous.",
               True, False, "C",
               "Comparing the gynoecium of pea and brinjal",
               "In Fabaceae (pea) the ovary is superior, monocarpellary and unilocular; in Solanaceae (brinjal) it is "
               "bicarpellary, syncarpous and superior. A superior ovary means a hypogynous flower in both. Pea, with "
               "a single carpel, cannot have a syncarpous (fused carpels) gynoecium.",
               ["Statement I: both have superior ovaries -> hypogynous; true",
                "Statement II: pea is monocarpellary; false"],
               ncert=ref("MOR", "The Flower; Description of Some Important Families"), secs=45)

match_list(T_MOR, "Plant families", "Advanced", "character described in NCERT", "family or families",
           ["Placenta swollen, bearing many ovules", "Leaf base pulvinate",
            "Perianth of six tepals, often united into a tube", "Flowers bisexual with a superior ovary"],
           ["Liliaceae only", "Fabaceae, Solanaceae and Liliaceae", "Solanaceae only", "Fabaceae only"],
           "III IV I II", ["IV III I II", "III IV II I", "III II I IV"], "A",
           "Characters of Fabaceae, Solanaceae and Liliaceae",
           "Solanaceae: bicarpellary, syncarpous ovary with a swollen placenta bearing many ovules (axile). "
           "Fabaceae: leaf base pulvinate, stipulate. Liliaceae: perianth of six tepals (3 + 3), often united into a "
           "tube. In all three families the flowers are bisexual and the ovary is superior.",
           ["Swollen placenta -> Solanaceae only", "Pulvinate leaf base -> Fabaceae only",
            "Six tepals united into a tube -> Liliaceae only", "Bisexual, superior ovary -> all three"],
           why="The wrong codes swap Solanaceae and Fabaceae, Liliaceae and 'all three', or wrongly treat a "
               "shared character as belonging to one family.",
           ncert=ref("MOR", "Description of Some Important Families"), secs=60)

direct(T_MOR, "Root, stem and leaf", "Advanced",
       "In Opuntia and in Australian acacia, food is synthesised largely by green structures other than a typical "
       "leaf lamina. Which statement about these structures is correct?",
       "In Opuntia the green structure is a modified stem, whereas in Australian acacia it is the expanded petiole "
       "of the leaf.",
       ["In both plants the green structure is a modified stem.",
        "In both plants the green structure is a modified stipule.",
        "In Opuntia it is the expanded petiole, whereas in Australian acacia it is a modified stem."], "D",
       "Photosynthetic organs other than the lamina",
       "NCERT: some plants of arid regions modify their stems into flattened (Opuntia) or fleshy cylindrical "
       "(Euphorbia) structures that contain chlorophyll and carry out photosynthesis. In Australian acacia the "
       "leaves are small and short-lived; the petioles expand, become green and synthesise food.",
       ["Opuntia: flattened green stem", "Australian acacia: green, expanded petiole (part of the leaf)"],
       why="Only Opuntia uses a modified stem; the acacia structure is a leaf petiole. Neither is a stipule, and "
           "the last option reverses the two plants.",
       ncert=ref("MOR", "The Stem; The Leaf (modifications)"), secs=45)

# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
direct(T_ANA, "Plant tissues", "Basic",
       "According to NCERT, the secondary or lateral meristem occurs in the mature regions of roots and shoots of "
       "many plants, particularly those that:",
       "produce a woody axis",
       ["are grasses regenerating after grazing", "are aquatic and lack vascular tissue",
        "have no apical meristem"], "D",
       "Where lateral meristems occur",
       "NCERT: the meristem that occurs in the mature regions of roots and shoots of many plants, particularly those "
       "that produce a woody axis, and appears later than the primary meristem is called the secondary or lateral "
       "meristem. It is cylindrical; fascicular vascular cambium, interfascicular cambium and cork cambium are "
       "examples.",
       ["Lateral meristem: mature regions of roots and shoots", "Particularly in plants producing a woody axis"],
       why="Regeneration after grazing in grasses is due to intercalary meristems. Flowering plants are not "
           "without vascular tissue, and all have apical meristems at root and shoot tips.",
       ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=20)

numerical(T_ANA, "Plant tissues", "Basic",
          "In angiosperms, how many different kinds of elements make up the xylem and the phloem taken together, as "
          "listed in NCERT?",
          "8", ["4", "6", "7"], "A",
          len(["tracheids", "vessels", "xylem fibres", "xylem parenchyma"]
              + ["sieve tube elements", "companion cells", "phloem parenchyma", "phloem fibres"]) == 8,
          "Elements of xylem and phloem",
          "Xylem is composed of four elements: tracheids, vessels, xylem fibres and xylem parenchyma. Phloem in "
          "angiosperms is composed of sieve tube elements, companion cells, phloem parenchyma and phloem fibres.",
          ["Xylem: 4 elements", "Angiosperm phloem: 4 elements", "Total = 4 + 4 = 8"],
          why="4 counts only one of the two tissues. 6 leaves out the fibres of both tissues. 7 leaves out one "
              "element, such as the phloem fibres.",
          ncert=ref("ANA", "The Tissues (xylem; phloem)"), secs=30)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "The trichomes of the shoot system may be branched or unbranched, and soft or stiff.",
               "The waxy cuticle that covers the epidermis is absent in roots.",
               True, True, "A",
               "Trichomes and cuticle",
               "On the stem, the epidermal hairs are called trichomes. They are usually multicellular, may be branched "
               "or unbranched, soft or stiff, and may even be secretory; they help prevent water loss due to "
               "transpiration. The outside of the epidermis is often covered with a waxy, thick cuticle that "
               "prevents loss of water; the cuticle is absent in roots.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System (epidermal tissue system)"), secs=25)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "Which of the following is found in a monocot stem but NOT in a dicot stem?",
       "Scattered vascular bundles, each surrounded by a sclerenchymatous bundle sheath",
       ["Conjoint vascular bundles", "An epidermis forming the outermost layer",
        "A hypodermis of a few layers of collenchymatous cells"], "B",
       "Monocot stem compared with dicot stem",
       "The monocot stem has a sclerenchymatous hypodermis, a large number of scattered vascular bundles, each "
       "surrounded by a sclerenchymatous bundle sheath, and a large, conspicuous parenchymatous ground tissue. The "
       "dicot stem has a collenchymatous hypodermis and conjoint, open bundles arranged in a ring.",
       ["Monocot stem: scattered bundles with sclerenchymatous sheaths", "Dicot stem: bundles in a ring"],
       why="Conjoint bundles and an epidermis are found in both stems. A collenchymatous hypodermis is a feature "
           "of the dicot stem, not the monocot stem.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (monocot stem)"), secs=30)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Xylem parenchyma is a living component of the xylem.",
                 "All components of the xylem except xylem parenchyma are living cells.",
                 True, False, False, "C",
                 "Living and dead elements of xylem",
                 "Xylem parenchyma cells are living and thin-walled, with cellulose walls, and store starch or fat and "
                 "substances like tannins. The other xylem elements are not living: tracheids are dead and without "
                 "protoplasm, vessel members are devoid of protoplasm, and xylem fibres have highly thickened walls "
                 "with an obliterated lumen.",
                 ["A: true", "R: false - tracheids, vessel members and xylem fibres are not living"],
                 ncert=ref("ANA", "The Tissues (xylem)"), secs=35)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "Which of the following features are common to the vascular bundles of BOTH the dicot stem and the "
                "monocot stem?",
                [("The bundles are conjoint.", True),
                 ("The primary xylem is endarch.", True),
                 ("The bundles are open, with cambium between the xylem and the phloem.", False),
                 ("The bundles are arranged in a ring.", False),
                 ("Water-containing cavities are present within the bundles.", False)],
                [("a", "b", "c"), ("a", "d"), ("b", "e")], "C",
                "Vascular bundles of dicot and monocot stems",
                "In both stems the xylem and phloem lie together on the same radius (conjoint), and, as in all stems, "
                "the protoxylem lies towards the centre and the metaxylem towards the periphery (endarch). The dicot "
                "stem's bundles are open and arranged in a ring; the monocot stem's bundles are closed, scattered, "
                "lack phloem parenchyma and have water-containing cavities.",
                ["(a) both conjoint: true", "(b) both stems endarch: true", "(c) open only in dicot stem: false",
                 "(d) ring only in dicot stem: false", "(e) cavities only in monocot stem: false"],
                why="The other combinations include (c), (d) or (e), each of which belongs to only one of the two "
                    "stems.",
                ncert=ref("ANA", "The Tissues (xylem); Anatomy of Dicotyledonous and Monocotyledonous Plants"),
                secs=60)

direct(T_ANA, "Plant tissues", "Intermediate",
       "Which of the following is true of BOTH sclereids and phloem fibres, but NOT of companion cells?",
       "They are dead at maturity and have thick cell walls.",
       ["They are living at maturity and have a nucleus.",
        "They help in maintaining the pressure gradient in the sieve tubes.",
        "They store resins, latex and mucilage."], "D",
       "Comparing sclerenchymatous cells with companion cells",
       "Sclereids are spherical, oval or cylindrical, highly thickened dead cells with very narrow lumen. Phloem "
       "fibres are sclerenchymatous, with quite thick walls, and lose their protoplasm at maturity to become dead. "
       "Companion cells are specialised, living parenchymatous cells whose nucleus controls the sieve tubes and "
       "which help maintain the pressure gradient in them.",
       ["Sclereids: dead, thick-walled", "Phloem fibres: dead at maturity, thick-walled",
        "Companion cells: living, with nucleus"],
       why="Being living with a nucleus, and maintaining the pressure gradient, describe companion cells only. "
           "Storing resins, latex and mucilage is a function of phloem parenchyma.",
       ncert=ref("ANA", "The Tissues (sclerenchyma; phloem)"), secs=40)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "In a monocot stem, the peripheral vascular bundles are generally smaller than the centrally located "
               "ones.",
               "In a monocot stem, the parenchymatous ground tissue is small and inconspicuous.",
               True, False, "C",
               "Monocot stem",
               "NCERT: the monocot stem has a sclerenchymatous hypodermis, a large number of scattered vascular "
               "bundles, each surrounded by a sclerenchymatous bundle sheath, and a large, conspicuous parenchymatous "
               "ground tissue. Its vascular bundles are conjoint and closed, and the peripheral ones are generally "
               "smaller than the centrally located ones.",
               ["Statement I: true", "Statement II: false; the ground tissue is large and conspicuous"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (monocot stem)"), secs=35)

match_list(T_ANA, "Plant tissues", "Intermediate", "term", "meaning",
           ["Protoxylem", "Metaxylem", "Protophloem", "Metaphloem"],
           ["Later-formed primary phloem with bigger sieve tubes", "First-formed primary xylem elements",
            "First-formed primary phloem with narrow sieve tubes", "Later-formed primary xylem elements"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "First- and later-formed primary vascular tissues",
           "Primary xylem is of two types: the first-formed elements are protoxylem and the later-formed ones "
           "metaxylem. Likewise, the first-formed primary phloem consists of narrow sieve tubes and is called "
           "protophloem; the later-formed phloem has bigger sieve tubes and is called metaphloem.",
           ["Protoxylem -> II", "Metaxylem -> IV", "Protophloem -> III", "Metaphloem -> I"],
           why="The wrong codes swap the two kinds of xylem, the two kinds of phloem, or protoxylem with protophloem.",
           ncert=ref("ANA", "The Tissues (xylem; phloem)"), secs=35)

numerical(T_ANA, "Dicot and monocot anatomy", "Advanced",
          "In the transverse section of a dicot root, how many of the following lie OUTSIDE the stele?\n\n"
          "epiblema, root hairs, cortex, endodermis, pericycle, conjunctive tissue, xylem, pith",
          "4", ["3", "5", "6"], "B",
          len([p for p, inside in [("epiblema", False), ("root hairs", False), ("cortex", False),
                                   ("endodermis", False), ("pericycle", True), ("conjunctive tissue", True),
                                   ("xylem", True), ("pith", True)] if not inside]) == 4,
          "Extent of the stele in a dicot root",
          "All tissues on the inner side of the endodermis - the pericycle, the vascular bundles (with the "
          "conjunctive tissue between xylem and phloem) and the pith - constitute the stele. The epiblema with its "
          "root hairs, the cortex and the endodermis itself lie outside it.",
          ["Stele = everything inside the endodermis", "Outside: epiblema, root hairs, cortex, endodermis",
           "Count = 4"],
          why="3 wrongly places the endodermis inside the stele. 5 wrongly places the pericycle outside it. 6 also "
              "puts the conjunctive tissue outside, forgetting that it lies between the xylem and phloem.",
          ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicot root)"), secs=60)

assertion_reason(T_ANA, "Dicot and monocot anatomy", "Advanced",
                 "The vascular bundles of a monocot stem do not form secondary xylem and secondary phloem.",
                 "In the vascular bundles of monocots, no cambium is present between the xylem and the phloem.",
                 True, True, True, "A",
                 "Closed vascular bundles",
                 "In dicot stems, cambium between phloem and xylem gives the bundles the ability to form secondary "
                 "xylem and phloem, so they are open. NCERT: in monocotyledons the vascular bundles have no cambium "
                 "in them; hence they do not form secondary tissues and are referred to as closed. The absence of "
                 "cambium is the reason no secondary tissues form.",
                 ["A: true", "R: true", "No cambium -> no secondary xylem or phloem -> R explains A"],
                 ncert=ref("ANA", "The Tissue System (vascular tissue system)"), secs=45)

statement_pair(T_ANA, "Plant tissues", "Advanced",
               "Companion cells and phloem parenchyma cells are both living cells with a nucleus.",
               "Xylem fibres and phloem fibres are both living at maturity.",
               True, False, "C",
               "Living cells of the vascular tissues",
               "Companion cells are specialised parenchymatous cells whose nucleus controls the functions of the "
               "sieve tubes. Phloem parenchyma is made of elongated cells with dense cytoplasm and a nucleus. Xylem "
               "fibres have highly thickened walls and obliterated lumens, and phloem fibres lose their protoplasm "
               "and become dead at maturity.",
               ["Statement I: true", "Statement II: false; both kinds of fibre are dead at maturity"],
               ncert=ref("ANA", "The Tissues (xylem; phloem)"), secs=45)

direct(T_ANA, "Dicot and monocot anatomy", "Advanced",
       "A transverse section of a young plant organ shows a collenchymatous hypodermis, an endodermis whose cells "
       "are rich in starch grains, and semi-lunar patches of sclerenchyma above the phloem. The vascular bundles of "
       "this organ are expected to be:",
       "conjoint, open and endarch, arranged in a ring",
       ["radial, with exarch xylem and two to four xylem patches",
        "conjoint and closed, scattered, each with a sclerenchymatous bundle sheath",
        "conjoint and closed, all of nearly similar size except in the main veins"], "A",
       "Identifying a dicot stem from its section",
       "A collenchymatous hypodermis, a starch sheath (endodermis rich in starch grains) and a pericycle of "
       "semi-lunar sclerenchyma patches above the phloem identify a dicot stem. Its many vascular bundles are "
       "arranged in a ring; each is conjoint, open and has endarch protoxylem.",
       ["Features -> dicot stem", "Dicot stem bundles: conjoint, open, endarch, in a ring"],
       why="Radial bundles with exarch xylem and 2-4 patches describe a dicot root. Scattered, closed bundles with "
           "sclerenchymatous sheaths describe a monocot stem, and bundles of nearly similar size describe an "
           "isobilateral (monocot) leaf.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicot stem)"), secs=50)

# =============================================================== 5. Cell: The Unit of Life (5/6/5)
direct(T_CELL, "Cell envelope and membrane", "Basic",
       "Membrane proteins are classified as integral or peripheral. According to NCERT, this classification is "
       "based on their:",
       "ease of extraction from the membrane",
       ["molecular weight", "content of carbohydrates", "ability to act as enzymes"], "D",
       "Integral and peripheral proteins",
       "NCERT: depending on the ease of extraction, membrane proteins can be classified as integral or peripheral. "
       "Peripheral proteins lie on the surface of the membrane, while integral proteins are partially or totally "
       "buried in it.",
       ["Basis of classification = ease of extraction"],
       why="NCERT does not classify membrane proteins by molecular weight, carbohydrate content or enzyme "
           "activity.",
       ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "According to NCERT, the nucleus as a cell organelle was first described by Robert Brown as early as:",
       "1831",
       ["1838", "1855", "1898"], "B",
       "Discovery of the nucleus",
       "NCERT: the nucleus as a cell organelle was first described by Robert Brown as early as 1831. Later the "
       "material of the nucleus stained by basic dyes was named chromatin by Flemming.",
       ["Robert Brown described the nucleus in 1831"],
       why="1838 is the year of Schleiden's work on plant cells, 1855 that of Virchow's 'Omnis cellula-e cellula', "
           "and 1898 that of Camillo Golgi's observation of the Golgi apparatus.",
       ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In a chloroplast, the membrane of each thylakoid encloses a space called the:",
       "lumen",
       ["stroma", "matrix", "perinuclear space"], "C",
       "Compartments of the chloroplast",
       "The space limited by the inner membrane of the chloroplast is the stroma, in which flattened membranous "
       "sacs, the thylakoids, are present. NCERT: the membrane of the thylakoids encloses a space called a lumen.",
       ["Inside the inner membrane: stroma", "Inside each thylakoid: lumen"],
       why="The stroma surrounds the thylakoids. The matrix is the inner compartment of a mitochondrion, and the "
           "perinuclear space lies between the two membranes of the nuclear envelope.",
       ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=20)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "According to NCERT, the plasma membrane of a prokaryotic cell is:",
       "semi-permeable and structurally similar to that of eukaryotes",
       ["freely permeable and structurally unlike that of eukaryotes",
        "the outermost layer of the cell envelope",
        "absent in Mycoplasma, which lacks a cell wall"], "A",
       "Plasma membrane of prokaryotes",
       "NCERT: in prokaryotes, the plasma membrane is semi-permeable in nature and interacts with the outside world. "
       "This membrane is similar structurally to that of the eukaryotes. The cell envelope consists of the outermost "
       "glycocalyx, then the cell wall and then the plasma membrane.",
       ["Prokaryotic plasma membrane: semi-permeable", "Structure similar to the eukaryotic membrane"],
       why="The membrane is not freely permeable, and it is the innermost, not the outermost, layer of the "
           "envelope. Mycoplasma lacks a cell wall, not a plasma membrane.",
       ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=25)

statement_pair(T_CELL, "Prokaryotic cell", "Basic",
               "Plastids can be seen only with the electron microscope because they are very small.",
               "Motile bacteria show a range in the number and arrangement of their flagella.",
               False, True, "D",
               "Plastids; bacterial flagella",
               "NCERT: plastids are found in all plant cells and in euglenoids; they are easily observed under the "
               "microscope as they are large. Bacterial cells may be motile or non-motile; motile ones have thin "
               "filamentous extensions called flagella, and bacteria show a range in the number and arrangement of "
               "flagella.",
               ["Statement I: false; plastids are large and easily seen under the microscope", "Statement II: true"],
               ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells (plastids)"), secs=30)

match_list(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate", "cell structure",
           "shape or organisation described in NCERT",
           ["Mitochondrion", "Chloroplast", "Golgi apparatus", "Centriole"],
           ["Flat, disc-shaped sacs (cisternae) stacked parallel to each other",
            "Cartwheel-like organisation of nine evenly spaced peripheral fibrils",
            "Sausage-shaped or cylindrical",
            "Lens-shaped, oval, spherical, discoid or even ribbon-like"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D",
           "Shapes of cell organelles",
           "NCERT: mitochondria are sausage-shaped or cylindrical (diameter 0.2-1.0 µm). Chloroplasts may be "
           "lens-shaped, oval, spherical, discoid or even ribbon-like. The Golgi apparatus consists of many flat, "
           "disc-shaped sacs or cisternae stacked parallel to each other. A centriole has an organisation like a "
           "cartwheel, made of nine evenly spaced peripheral fibrils of tubulin.",
           ["Mitochondrion -> III", "Chloroplast -> IV", "Golgi apparatus -> I", "Centriole -> II"],
           why="The wrong codes swap the mitochondrion and the chloroplast, the Golgi apparatus and the centriole, or "
               "the chloroplast and the Golgi apparatus.",
           ncert=ref("CELL", "Eukaryotic Cells"), secs=45)

assertion_reason(T_CELL, "Cell envelope and membrane", "Intermediate",
                 "Peripheral proteins are totally buried in the lipid bilayer of the cell membrane.",
                 "Integral proteins are partially or totally buried in the cell membrane.",
                 False, True, False, "D",
                 "Peripheral and integral proteins",
                 "Peripheral proteins lie on the surface of the membrane, while integral proteins are partially or "
                 "totally buried in the membrane.",
                 ["A: false - peripheral proteins lie on the surface", "R: true"],
                 ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=35)

statement_pair(T_CELL, "Endomembrane system", "Intermediate",
               "Microbodies, membrane-bound minute vesicles containing various enzymes, are present in both plant "
               "and animal cells.",
               "Microbodies are counted by NCERT as part of the endomembrane system.",
               True, False, "C",
               "Microbodies and the endomembrane system",
               "NCERT: many membrane-bound minute vesicles called microbodies, containing various enzymes, are present "
               "in both plant and animal cells. The endomembrane system includes the endoplasmic reticulum, Golgi "
               "complex, lysosomes and vacuoles, whose functions are coordinated; microbodies are not listed in it.",
               ["Statement I: true", "Statement II: false; endomembrane system = ER, Golgi, lysosomes, vacuoles"],
               ncert=ref("CELL", "Eukaryotic Cells (endomembrane system; microbodies)"), secs=35)

multi_statement(T_CELL, "Prokaryotic cell", "Intermediate",
                "Which of the following statements about bacterial flagella are correct?",
                [("A bacterial flagellum is composed of three parts: filament, hook and basal body.", True),
                 ("The filament is the longest portion and extends from the cell surface to the outside.", True),
                 ("Fimbriae form the longest part of the bacterial flagellum.", False),
                 ("Bacterial flagella are structurally identical to eukaryotic flagella.", False),
                 ("Motile bacteria have thin filamentous extensions called flagella.", True)],
                [("a", "b"), ("a", "c", "e"), ("b", "d", "e")], "B",
                "Structure of the bacterial flagellum",
                "Motile bacteria have thin filamentous extensions called flagella. A bacterial flagellum has three "
                "parts - filament, hook and basal body; the filament is the longest portion and extends from the "
                "cell surface to the outside. Fimbriae are separate small bristle-like fibres used for attachment, "
                "and prokaryotic flagella are structurally different from eukaryotic ones.",
                ["(a) true", "(b) true", "(c) false: fimbriae are not part of the flagellum",
                 "(d) false: they are structurally different", "(e) true"],
                why="(a) and (b) only leaves out (e). The other combinations include the false statement (c) or (d).",
                ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=55)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "Which of the following pairs consists of two structures that are NOT bounded by any membrane?",
       "Ribosome and nucleolus",
       ["Lysosome and vacuole", "Ribosome and microbody", "Nucleolus and mitochondrion"], "C",
       "Non-membranous structures of the cell",
       "Ribosomes are composed of RNA and proteins and are not surrounded by any membrane. The nucleolus is not a "
       "membrane-bound structure; its content is continuous with the rest of the nucleoplasm. Lysosomes, vacuoles "
       "and microbodies are membrane-bound, and mitochondria have two membranes.",
       ["Ribosome: no membrane", "Nucleolus: no membrane", "Lysosome, vacuole, microbody, mitochondrion: "
        "membrane-bound"],
       why="Each wrong pair contains at least one membrane-bound structure: lysosome, vacuole (tonoplast), "
           "microbody or mitochondrion (double membrane).",
       ncert=ref("CELL", "Eukaryotic Cells (ribosomes; nucleus)"), secs=35)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
       "Which of the following is found in both plant and animal cells and also contains its own DNA?",
       "Mitochondrion",
       ["Chloroplast", "Centriole", "Lysosome"], "A",
       "Organelles with their own DNA",
       "Mitochondria occur in plant and animal cells, and the mitochondrial matrix possesses a single circular DNA "
       "molecule, a few RNA molecules and 70S ribosomes. Chloroplasts also have DNA but are found in plant cells "
       "(and euglenoids), not in animal cells. Centrioles and lysosomes do not contain DNA.",
       ["Mitochondrion: both cell types + own DNA", "Chloroplast: own DNA but not in animal cells"],
       why="Chloroplasts are absent from animal cells. Centrioles are absent from almost all plant cells and, like "
           "lysosomes, have no DNA.",
       ncert=ref("CELL", "Eukaryotic Cells (mitochondria; plastids)"), secs=30)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "Unless specifically stained, mitochondria are not easily visible under the microscope.",
                 "The number of mitochondria per cell is variable, depending on the physiological activity of the "
                 "cell.",
                 True, True, False, "B",
                 "Two separate features of mitochondria",
                 "NCERT: mitochondria, unless specifically stained, are not easily visible under the microscope. The "
                 "number of mitochondria per cell is variable depending on the physiological activity of the cells. "
                 "How many mitochondria a cell has does not decide whether each one can be seen without staining; "
                 "the two statements describe different properties.",
                 ["A: true", "R: true", "The number per cell has nothing to do with visibility -> R does not "
                  "explain A"],
                 ncert=ref("CELL", "Eukaryotic Cells (mitochondria)"), secs=40)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
               "In a centriole the peripheral fibrils are doublets of microtubules, whereas in the axoneme of a "
               "cilium the peripheral fibrils are triplets.",
               "The central part of the proximal region of a centriole is called the hub, and it is proteinaceous.",
               False, True, "D",
               "Comparing centrioles and axonemes",
               "The axoneme of a cilium or flagellum has nine pairs of doublets of radially arranged peripheral "
               "microtubules and a pair of centrally located microtubules (9 + 2). A centriole has nine evenly spaced "
               "peripheral fibrils, each a triplet; the central part of its proximal region, the hub, is "
               "proteinaceous and is connected to the peripheral triplets by radial spokes.",
               ["Statement I: false; the doublet and triplet are reversed", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella; centrosome and centrioles)"), secs=45)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "An organism completely lacks a cell wall, is among the smallest living cells known and can survive "
                "without oxygen. Which of the following statements about its cell are correct?",
                [("It is a prokaryotic cell.", True),
                 ("Its ribosomes are associated with the plasma membrane.", True),
                 ("Its genetic material is naked, not enveloped by a nuclear membrane.", True),
                 ("Its cell envelope consists of a glycocalyx, a cell wall and a plasma membrane.", False),
                 ("Its ribosomes are of the 80S type.", False)],
                [("a", "c"), ("a", "b", "d"), ("b", "c", "e")], "A",
                "Applying prokaryotic features to Mycoplasma",
                "The organism described is Mycoplasma, the smallest living cell known (about 0.3 µm), which lacks a "
                "cell wall and can survive without oxygen. NCERT places mycoplasma with bacteria, blue-green algae "
                "and PPLO among prokaryotes. In prokaryotes the genetic material is naked, the ribosomes are 70S "
                "and are associated with the plasma membrane. Lacking a wall, Mycoplasma cannot have the usual "
                "three-layered envelope.",
                ["Organism = Mycoplasma (prokaryote)", "(a), (b), (c): prokaryotic features -> true",
                 "(d) false: it has no cell wall", "(e) false: prokaryotic ribosomes are 70S"],
                why="(a) and (c) only leaves out the true statement (b). The other combinations include (d) or (e).",
                ncert=ref("CELL", "Prokaryotic Cells; Biological Classification (Mycoplasma)"), secs=60)

match_list(T_CELL, "Endomembrane system", "Advanced", "structure", "enzymes or contents described in NCERT",
           ["Lysosome", "Chloroplast stroma", "Mitochondrial membranes", "Microbodies"],
           ["Each of the two membranes has its own specific enzymes associated with the organelle's function",
            "Minute membrane-bound vesicles containing various enzymes, present in both plant and animal cells",
            "Hydrolytic enzymes such as lipases, proteases and carbohydrases, optimally active at acidic pH",
            "Enzymes required for the synthesis of carbohydrates and proteins"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "C",
           "Enzymes of cell compartments",
           "Isolated lysosomal vesicles are very rich in almost all types of hydrolytic enzymes (lipases, proteases, "
           "carbohydrases), optimally active at acidic pH. The chloroplast stroma contains enzymes required for the "
           "synthesis of carbohydrates and proteins. The two mitochondrial membranes have their own specific "
           "enzymes associated with mitochondrial function. Microbodies are membrane-bound minute vesicles that "
           "contain various enzymes and occur in both plant and animal cells.",
           ["Lysosome -> III", "Chloroplast stroma -> IV", "Mitochondrial membranes -> I", "Microbodies -> II"],
           why="The wrong codes swap the lysosome with the stroma, the mitochondrial membranes with microbodies, or "
               "the stroma with the mitochondrial membranes.",
           ncert=ref("CELL", "Eukaryotic Cells"), secs=55)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
       "Which of the following possesses plastids but has no cell wall, according to NCERT?",
       "Euglena",
       ["A mesophyll cell of a leaf", "Nostoc", "Amoeba"], "B",
       "Plastids without a cell wall",
       "NCERT states that plastids are found in all plant cells and in euglenoids. Euglenoids such as Euglena have "
       "no cell wall; instead they have a protein-rich layer called the pellicle. A mesophyll cell has both "
       "plastids and a cell wall. Nostoc, a cyanobacterium, has pigment-containing chromatophores, not plastids, "
       "and Amoeba has neither plastids nor a wall.",
       ["Plastids: plant cells and euglenoids", "Euglenoids: pellicle instead of a cell wall"],
       why="A mesophyll cell has a cell wall. Nostoc is a prokaryote without plastids (it has a cell wall too). "
           "Amoeba has no plastids.",
       ncert=ref("CELL", "Eukaryotic Cells (plastids); Biological Classification (euglenoids)"), secs=45)

# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "According to NCERT, the cell cycle is divided into two basic phases. These are:",
       "interphase and M phase",
       ["G1 phase and G2 phase", "karyokinesis and cytokinesis", "S phase and G0 phase"], "B",
       "Two basic phases of the cell cycle",
       "The cell cycle is divided into two basic phases: interphase, the period of preparation for division (G1, S "
       "and G2), and the M phase (mitosis phase), when the actual cell division takes place.",
       ["Basic phases: interphase + M phase", "Interphase = G1 + S + G2"],
       why="G1 and G2 are sub-phases of interphase. Karyokinesis and cytokinesis are the two parts of the M phase. "
           "G0 is a quiescent stage outside the active cycle, and S is a sub-phase of interphase.",
       ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=20)

direct(T_CC, "Mitosis", "Basic",
       "Which of the following is NOT one of the four stages into which karyokinesis of mitosis is divided?",
       "Interkinesis",
       ["Prophase", "Metaphase", "Telophase"], "D",
       "Stages of karyokinesis",
       "Karyokinesis of mitosis is divided into four stages: prophase, metaphase, anaphase and telophase. "
       "Interkinesis is the stage between the two meiotic divisions, not a stage of mitosis.",
       ["Mitotic stages: prophase, metaphase, anaphase, telophase", "Interkinesis: between meiosis I and II"],
       why="Prophase, metaphase and telophase are three of the four stages of karyokinesis.",
       ncert=ref("CC", "M Phase"), secs=20)

statement_pair(T_CC, "Meiosis", "Basic",
               "Meiosis II is initiated immediately after cytokinesis, usually before the chromosomes have fully "
               "elongated.",
               "Prophase II is a much simpler prophase than prophase I.",
               True, True, "A",
               "Start of meiosis II",
               "NCERT: meiosis II is initiated immediately after cytokinesis, usually before the chromosomes have "
               "fully elongated. Interkinesis is followed by prophase II, a much simpler prophase than prophase I.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Meiosis (meiosis II)"), secs=25)

direct(T_CC, "Significance", "Basic",
       "Meiosis ensures that the specific chromosome number of each species is conserved across generations in "
       "sexually reproducing organisms, even though the process itself, paradoxically, results in:",
       "reduction of the chromosome number by half",
       ["doubling of the chromosome number", "no change in the chromosome number of the daughter cells",
        "the formation of diploid gametes"], "D",
       "The paradox of meiosis",
       "NCERT: the conservation of the specific chromosome number of each species across generations is achieved "
       "through meiosis, even though the process, per se, paradoxically, results in reduction of chromosome number "
       "by half. Fertilisation later restores the diploid number.",
       ["Meiosis halves the chromosome number", "Fertilisation restores it -> number conserved across generations"],
       why="Meiosis does not double or keep the chromosome number; it halves it, and the gametes it forms are "
           "haploid, not diploid.",
       ncert=ref("CC", "Significance of Meiosis"), secs=25)

numerical(T_CC, "Cell cycle phases", "Intermediate",
          "How many of the following take place during the M phase of the cell cycle?\n\n(i) Replication of DNA\n"
          "(ii) Duplication of the centriole in an animal cell\n(iii) Condensation of chromosomes\n"
          "(iv) Disintegration of the nuclear envelope\n(v) Cytokinesis\n"
          "(vi) Synthesis of proteins in preparation for mitosis",
          "3", ["2", "4", "5"], "B",
          sum([False, False, True, True, True, False]) == 3,
          "Events of interphase and M phase",
          "DNA replication and centriole duplication take place in the S phase, and proteins are synthesised in "
          "preparation for mitosis in G2 - all parts of interphase. The M phase starts with karyokinesis "
          "(condensation of chromosomes in prophase; complete disintegration of the nuclear envelope marks the start "
          "of metaphase) and usually ends with cytokinesis.",
          ["Interphase: (i), (ii) in S; (vi) in G2", "M phase: (iii), (iv), (v)", "Count = 3"],
          why="2 leaves out cytokinesis, which is part of the M phase. 4 adds G2 protein synthesis or centriole "
              "duplication, and 5 adds both, though they belong to interphase.",
          ncert=ref("CC", "Cell Cycle; M Phase"), secs=50)

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "Mitosis is also called equational division.",
                 "In plant cells, cytokinesis begins with a cell plate that forms in the centre of the cell and "
                 "grows outwards.",
                 True, True, False, "B",
                 "Equational division; cytokinesis in plants",
                 "Mitosis is called equational division because the number of chromosomes in the parent and progeny "
                 "cells is the same. Separately, in plant cells the new wall begins as a cell plate formed in the "
                 "centre and growing outward to meet the lateral walls. The way the cytoplasm is divided in plants "
                 "has nothing to do with why mitosis keeps the chromosome number equal.",
                 ["A: true (same chromosome number in parent and progeny)", "R: true", "R is about cytokinesis in "
                  "plants, not about the chromosome number -> not the explanation"],
                 ncert=ref("CC", "M Phase (cytokinesis)"), secs=35)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following take place during telophase of mitosis?",
                [("The centromere of each chromosome splits.", False),
                 ("A nuclear envelope develops around each chromosome cluster at the poles.", True),
                 ("The nucleolus, Golgi complex and ER reform.", True),
                 ("The chromosomes decondense and lose their individuality.", True),
                 ("The chromosomes align on the metaphase plate.", False)],
                [("b", "c"), ("a", "b", "d"), ("c", "d", "e")], "D",
                "Events of telophase",
                "At telophase the chromosomes that have reached their poles decondense and lose their "
                "individuality; the chromatin collects in a mass at each pole. A nuclear envelope develops around "
                "the chromosome clusters at each pole, forming two daughter nuclei, and the nucleolus, Golgi complex "
                "and ER reform. Centromeres split at anaphase, and chromosomes align on the metaphase plate at "
                "metaphase.",
                ["(a) anaphase event: false", "(b) true", "(c) true", "(d) true", "(e) metaphase event: false"],
                why="(b) and (c) only leaves out the decondensation of chromosomes. The other combinations include "
                    "(a) or (e), which belong to anaphase and metaphase.",
                ncert=ref("CC", "M Phase (telophase)"), secs=50)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Diakinesis is marked by the formation of the synaptonemal complex.",
               "During diakinesis, the chromosomes are fully condensed and the meiotic spindle is assembled to "
               "prepare the homologous chromosomes for separation.",
               False, True, "D",
               "Diakinesis",
               "The synaptonemal complex forms in zygotene and dissolves in diplotene. Diakinesis is marked by "
               "terminalisation of chiasmata; during this phase the chromosomes are fully condensed and the meiotic "
               "spindle is assembled to prepare the homologous chromosomes for separation. By its end the nucleolus "
               "disappears and the nuclear envelope breaks down.",
               ["Statement I: false; synaptonemal complex forms in zygotene", "Statement II: true"],
               ncert=ref("CC", "Meiosis (prophase I)"), secs=35)

direct(T_CC, "Meiosis", "Intermediate",
       "A dividing cell of a diploid organism has n chromosomes, each made of two chromatids. The chromosomes are "
       "becoming compact again, and the nuclear membrane disappears by the end of the stage. The cell is in:",
       "prophase II",
       ["prophase I", "metaphase II", "telophase I"], "B",
       "Recognising prophase II",
       "After meiosis I each cell has n chromosomes, each still with two chromatids. Meiosis II begins immediately; "
       "in prophase II the nuclear membrane disappears by the end of the stage and the chromosomes again become "
       "compact. In metaphase II the chromosomes align at the equator.",
       ["n chromosomes with two chromatids -> after meiosis I", "Chromosomes compacting, nuclear membrane "
        "disappearing -> prophase II"],
       why="A cell in prophase I has 2n chromosomes forming bivalents. In metaphase II the chromosomes are already "
           "aligned at the equator. In telophase I the nuclear membrane and nucleolus reappear rather than "
           "disappear.",
       ncert=ref("CC", "Meiosis (meiosis II)"), secs=40)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements correctly compare prophase I of meiosis with prophase of "
                "mitosis?",
                [("Prophase I is typically longer and more complex than prophase of mitosis.", True),
                 ("Crossing over between non-sister chromatids occurs in both.", False),
                 ("Synapsis of homologous chromosomes takes place only in prophase I.", True),
                 ("The nuclear envelope remains intact after both of them are over.", False),
                 ("Condensation of the chromosomal material takes place in both.", True)],
                [("a", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Prophase I versus mitotic prophase",
                "NCERT: prophase of the first meiotic division is typically longer and more complex than prophase of "
                "mitosis and is subdivided into leptotene, zygotene, pachytene, diplotene and diakinesis. "
                "Chromosomes condense in both. Synapsis (zygotene) and crossing over between non-sister chromatids "
                "(pachytene) happen only in meiosis I. The nuclear envelope breaks down at the end of mitotic "
                "prophase (its complete disintegration marks the start of metaphase) and by the end of diakinesis.",
                ["(a) true", "(b) false: no crossing over in mitosis", "(c) true",
                 "(d) false: the nuclear envelope breaks down in both", "(e) true"],
                why="(a) and (c) only leaves out the condensation of chromosomes. The other combinations include (b) "
                    "or (d).",
                ncert=ref("CC", "M Phase (prophase); Meiosis (prophase I)"), secs=60)

direct(T_CC, "Meiosis", "Advanced",
       "Which of the following would NOT be seen in a cell at anaphase II of meiosis?",
       "Homologous chromosomes paired as bivalents",
       ["Splitting of the centromere of each chromosome",
        "Sister chromatids moving towards opposite poles",
        "Shortening of the microtubules attached to the kinetochores"], "A",
       "Events of anaphase II",
       "Anaphase II begins with the simultaneous splitting of the centromere of each chromosome, allowing the sister "
       "chromatids to move towards opposite poles by shortening of the microtubules attached to the kinetochores. "
       "The homologous chromosomes had already separated in anaphase I, so no bivalents remain.",
       ["Anaphase II: centromeres split, sister chromatids move apart, microtubules shorten",
        "Homologues separated in anaphase I -> no bivalents"],
       why="Splitting of centromeres, movement of sister chromatids to opposite poles and shortening of "
           "kinetochore microtubules all happen in anaphase II.",
       ncert=ref("CC", "Meiosis (meiosis II)"), secs=40)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "Interkinesis is followed by a prophase that is more complex than prophase I.",
                 "Interkinesis, the stage between the two meiotic divisions, is generally short-lived.",
                 False, True, False, "D",
                 "Interkinesis and prophase II",
                 "The stage between the two meiotic divisions is called interkinesis and is generally short-lived. "
                 "Interkinesis is followed by prophase II, which NCERT describes as a much simpler prophase than "
                 "prophase I.",
                 ["A: false - prophase II is much simpler than prophase I", "R: true"],
                 ncert=ref("CC", "Meiosis (meiosis I; meiosis II)"), secs=40)

statement_pair(T_CC, "Meiosis", "Advanced",
               "At metaphase I, the chromosomes align on the equatorial plate as single, unpaired chromosomes.",
               "At metaphase of mitosis, both sister chromatids of a chromosome are attached to spindle fibres from "
               "the same pole.",
               False, False, "B",
               "Metaphase of mitosis and metaphase I",
               "At metaphase I, the bivalent chromosomes align on the equatorial plate, and microtubules from the "
               "opposite poles attach to the pair of homologous chromosomes. At metaphase of mitosis, one chromatid "
               "of each chromosome is connected by its kinetochore to spindle fibres from one pole and its sister "
               "chromatid to spindle fibres from the opposite pole.",
               ["Statement I: false; bivalents align at metaphase I",
                "Statement II: false; sister chromatids attach to opposite poles"],
               ncert=ref("CC", "M Phase (metaphase); Meiosis (metaphase I)"), secs=45)

# =============================================================== 7. Photosynthesis (4/6/4)
direct(T_PS, "Site and pigments", "Basic",
       "NCERT shows that the colour of a green leaf is due to four different pigments rather than one. The "
       "technique used to separate these leaf pigments is:",
       "paper chromatography",
       ["centrifugation", "gel electrophoresis", "staining with basic dyes"], "C",
       "Separating leaf pigments",
       "A chromatographic separation of the leaf pigments shows that the colour of leaves is due to four pigments: "
       "chlorophyll a (bright or blue green), chlorophyll b (yellow green), xanthophylls (yellow) and carotenoids "
       "(yellow to yellow-orange). NCERT describes this separation by paper chromatography.",
       ["Technique: paper chromatography", "Result: four pigment bands"],
       why="NCERT uses paper chromatography, not centrifugation or electrophoresis, to separate the pigments; "
           "staining with basic dyes is how chromatin was named, not how pigments are separated.",
       ncert=ref("PS", "What is the Photosynthetic Pigment Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Phosphoenol pyruvate (PEP), the primary CO₂ acceptor in the mesophyll cells of C4 plants, is a:",
       "3-carbon molecule",
       ["4-carbon molecule", "5-carbon ketose sugar", "6-carbon sugar"], "D",
       "Primary CO₂ acceptor of the C4 pathway",
       "NCERT: in the C4 pathway, the primary CO₂ acceptor is a 3-carbon molecule, phosphoenol pyruvate (PEP), "
       "present in the mesophyll cells; the enzyme is PEP carboxylase. The product is the 4-carbon oxaloacetic acid "
       "(OAA).",
       ["PEP: 3 carbons", "PEP + CO₂ -> OAA (4 carbons)"],
       why="The 4-carbon molecule is OAA, the product. The 5-carbon ketose sugar is RuBP, the acceptor of the "
           "Calvin cycle, and glucose is the 6-carbon sugar.",
       ncert=ref("PS", "The C4 Pathway"), secs=20)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Basic",
               "Photosystem I and Photosystem II are named in the sequence in which they function during the light "
               "reaction.",
               "Each light-harvesting complex (LHC) is made up of hundreds of pigment molecules bound to proteins.",
               False, True, "D",
               "Photosystems and light-harvesting complexes",
               "The pigments are organised into two discrete photochemical light-harvesting complexes within PS I and "
               "PS II. These are named in the sequence of their discovery, not in the sequence in which they "
               "function during the light reaction. Each LHC is made up of hundreds of pigment molecules bound to "
               "proteins.",
               ["Statement I: false; named in order of discovery", "Statement II: true"],
               ncert=ref("PS", "What is Light Reaction?"), secs=25)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Basic",
                 "Photosynthesis is responsible for the release of oxygen into the atmosphere.",
                 "In the light reaction, water is split, and oxygen is released as one of the products.",
                 True, True, True, "A",
                 "Source of atmospheric oxygen from photosynthesis",
                 "NCERT notes that photosynthesis is important because it is the primary source of all food on earth "
                 "and is responsible for the release of oxygen into the atmosphere. This oxygen comes from the "
                 "splitting of water (2H₂O -> 4H⁺ + O₂ + 4e⁻) associated with PS II in the light reaction.",
                 ["A: true", "R: true", "The O₂ that photosynthesis releases is produced by water splitting -> R "
                  "explains A"],
                 ncert=ref("PS", "Introduction; The Splitting of Water"), secs=30)

match_list(T_PS, "Chemiosmosis", "Intermediate", "component", "location or role",
           ["CF₀ of ATP synthase", "CF₁ of ATP synthase", "NADP reductase", "Water-splitting complex"],
           ["Forms a transmembrane channel for facilitated diffusion of protons",
            "Located on the stroma side of the membrane; the protons it needs are removed from the stroma",
            "Protrudes on the outer surface facing the stroma; its conformational change makes the enzyme "
            "synthesise ATP",
            "Associated with PS II and located on the inner side of the membrane"],
           "I III II IV", ["III I II IV", "I III IV II", "II III I IV"], "B",
           "Parts of the chemiosmotic machinery",
           "ATP synthase has two parts: CF₀, embedded in the thylakoid membrane, forms a transmembrane channel for "
           "facilitated diffusion of protons; CF₁ protrudes on the outer surface facing the stroma, and the energy "
           "of proton movement causes a conformational change in it that makes the enzyme synthesise ATP. NADP "
           "reductase is on the stroma side, and the protons for NADPH + H⁺ are removed from the stroma. The "
           "water-splitting complex is associated with PS II on the inner side of the membrane.",
           ["CF₀ -> I", "CF₁ -> III", "NADP reductase -> II", "Water-splitting complex -> IV"],
           why="The wrong codes swap the two parts of ATP synthase, the NADP reductase with the water-splitting "
               "complex, or CF₀ with NADP reductase.",
           ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=50)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following are true of BOTH Photosystem I and Photosystem II?",
                [("It is associated with the water-splitting complex.", False),
                 ("Its reaction centre is a single chlorophyll a molecule.", True),
                 ("Its light-harvesting complex has hundreds of pigment molecules bound to proteins.", True),
                 ("It takes part in cyclic photophosphorylation.", False),
                 ("It is located in the thylakoid membranes.", True)],
                [("b", "c"), ("a", "b", "e"), ("c", "d", "e")], "C",
                "Common features of the two photosystems",
                "Each photosystem has a light-harvesting complex of hundreds of pigment molecules bound to proteins, "
                "with a single chlorophyll a molecule as the reaction centre (different in the two photosystems). "
                "The LHCs are located in the thylakoid membranes. Only PS II is associated with water splitting, "
                "and only PS I is functional in cyclic photophosphorylation.",
                ["(a) PS II only: false", "(b) true", "(c) true", "(d) PS I only: false", "(e) true"],
                why="(b) and (c) only leaves out the location in the thylakoid membranes. The other combinations "
                    "include (a) or (d), each true of only one photosystem.",
                ncert=ref("PS", "What is Light Reaction?; Cyclic and Non-cyclic Photo-phosphorylation"), secs=55)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
               "The reduction steps of the Calvin cycle are catalysed by RuBisCO.",
               "The oxygen evolved during photosynthesis comes from carbon dioxide.",
               False, False, "B",
               "RuBisCO's step; source of O₂",
               "RuBisCO catalyses carboxylation, the fixation of CO₂ with RuBP to form two molecules of 3-PGA. The "
               "reduction steps that follow use ATP for phosphorylation and NADPH for reduction. The O₂ evolved in "
               "photosynthesis comes from the splitting of water, not from CO₂.",
               ["Statement I: false; RuBisCO catalyses carboxylation", "Statement II: false; O₂ comes from water"],
               ncert=ref("PS", "The Calvin Cycle; The Splitting of Water"), secs=35)

direct(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
       "In a C4 plant, which option correctly pairs each carboxylating enzyme with the cells in which it fixes CO₂?",
       "PEP carboxylase in the mesophyll cells; RuBisCO in the bundle sheath cells",
       ["RuBisCO in the mesophyll cells; PEP carboxylase in the bundle sheath cells",
        "Both PEP carboxylase and RuBisCO in the mesophyll cells",
        "Both PEP carboxylase and RuBisCO in the bundle sheath cells"], "A",
       "Division of labour in C4 leaves",
       "In C4 plants the primary CO₂ acceptor PEP is carboxylated by PEP carboxylase in the mesophyll cells, which "
       "lack RuBisCO. The C4 acid is moved to the bundle sheath cells, broken down to release CO₂, and the CO₂ "
       "enters the Calvin cycle there. The bundle sheath cells are rich in RuBisCO but lack PEPcase.",
       ["Mesophyll: PEPcase (no RuBisCO)", "Bundle sheath: RuBisCO (no PEPcase)"],
       why="The first option reverses the two cell types. Each cell type has only one of the two enzymes, so "
           "neither 'both in one cell' option is correct.",
       ncert=ref("PS", "The C4 Pathway"), secs=35)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following are part of the light reactions (photochemical phase) of photosynthesis?",
                [("Splitting of water", True),
                 ("Carboxylation of RuBP", False),
                 ("Formation of NADPH", True),
                 ("Regeneration of RuBP", False),
                 ("Release of oxygen", True)],
                [("a", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Light reactions versus the biosynthetic phase",
                "The light reactions (photochemical phase) include light absorption, water splitting, oxygen release "
                "and the formation of the high-energy intermediates ATP and NADPH. Carboxylation, reduction and "
                "regeneration of RuBP make up the Calvin cycle of the biosynthetic phase in the stroma.",
                ["(a), (c), (e): light reactions", "(b), (d): Calvin cycle (biosynthetic phase)"],
                why="(a) and (c) only leaves out the release of oxygen. The other combinations include a stage of the "
                    "Calvin cycle.",
                ncert=ref("PS", "What is Light Reaction?; Where are the ATP and NADPH used?"), secs=45)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                 "In a C4 plant, the CO₂ fixed in the mesophyll cells is ultimately released in the bundle sheath "
                 "cells.",
                 "The C4 acids (malic acid or aspartic acid) formed in the mesophyll cells are transported to the "
                 "bundle sheath cells and broken down there to release CO₂ and a 3-carbon molecule.",
                 True, True, True, "A",
                 "Transport of fixed CO₂ in the C4 pathway",
                 "OAA formed in the mesophyll forms other 4-carbon compounds like malic acid or aspartic acid, which "
                 "are transported to the bundle sheath cells. There these C4 acids are broken down to release CO₂ "
                 "and a 3-carbon molecule; the CO₂ then enters the Calvin cycle. The transport and breakdown of the "
                 "C4 acid is how the CO₂ reaches the bundle sheath.",
                 ["A: true", "R: true", "The C4 acid carries the fixed carbon to the bundle sheath and releases it "
                  "-> R explains A"],
                 ncert=ref("PS", "The C4 Pathway"), secs=40)

match_list(T_PS, "Calvin cycle and C4 pathway", "Advanced", "feature", "plants in which NCERT describes it",
           ["The Calvin cycle as the main biosynthetic pathway",
            "Initial fixation of atmospheric CO₂ by PEP carboxylase",
            "3-PGA as the first stable product of CO₂ fixation",
            "Release of O₂ derived from the splitting of CO₂"],
           ["C3 plants only", "C4 plants only", "Both C3 and C4 plants", "Neither C3 nor C4 plants"],
           "III II I IV", ["II III I IV", "III II IV I", "III I II IV"], "D",
           "Comparing C3 and C4 plants",
           "The Calvin pathway occurs in all photosynthetic plants, whether they have the C3 or the C4 pathway. Only "
           "C4 plants fix atmospheric CO₂ first by PEP carboxylase (first product OAA); in C3 plants the first stable "
           "product is 3-PGA. In no plant is the O₂ released derived from CO₂: it comes from the splitting of water.",
           ["Calvin cycle -> both", "PEPcase as first fixer -> C4 only", "3-PGA first product -> C3 only",
            "O₂ from CO₂ -> neither"],
           why="The wrong codes swap 'both' with 'C4 only', 'C3 only' with 'neither', or 'C3 only' with 'C4 only'.",
           ncert=ref("PS", "The Calvin Cycle; The C4 Pathway; The Splitting of Water"), secs=60)

direct(T_PS, "Calvin cycle and C4 pathway", "Advanced",
       "Which of the following does NOT take place in the bundle sheath cells of a C4 plant such as maize?",
       "Fixation of atmospheric CO₂ with phosphoenol pyruvate",
       ["Breakdown of the C4 acid to release CO₂", "Carboxylation of RuBP by RuBisCO",
        "Reduction of PGA using ATP and NADPH"], "B",
       "Events in the bundle sheath cells",
       "In C4 plants, the bundle sheath cells receive the C4 acid, break it down to release CO₂, and carry out the "
       "Calvin cycle: carboxylation of RuBP by RuBisCO, reduction using ATP and NADPH, and regeneration of RuBP. "
       "The bundle sheath cells lack PEP carboxylase, so the fixation of atmospheric CO₂ with PEP happens only in "
       "the mesophyll cells.",
       ["Bundle sheath: decarboxylation + whole Calvin cycle", "No PEPcase in bundle sheath -> PEP fixation only "
        "in mesophyll"],
       why="Breakdown of the C4 acid, carboxylation of RuBP and reduction of PGA all take place in the bundle "
           "sheath cells.",
       ncert=ref("PS", "The C4 Pathway"), secs=45)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Advanced",
               "In the Z scheme, electrons from PS II pass downhill through the electron transport chain to the "
               "pigments of PS I, and electrons excited in the reaction centre of PS I are finally passed to NADP⁺.",
               "NADP reductase is located on the lumen side of the thylakoid membrane, so the protons used to reduce "
               "NADP⁺ are taken from the lumen.",
               True, False, "C",
               "Electron flow and NADP⁺ reduction",
               "In non-cyclic flow, electrons excited in PS II are passed through the electron transport chain "
               "(downhill on the redox scale) to PS I; electrons excited in PS I are passed through another chain to "
               "NADP⁺, reducing it to NADPH + H⁺. NADP reductase is located on the stroma side of the membrane, and "
               "the protons needed for the reduction are removed from the stroma, which adds to the proton gradient.",
               ["Statement I: true", "Statement II: false; NADP reductase is on the stroma side"],
               ncert=ref("PS", "Electron Transport; The Chemiosmotic Hypothesis"), secs=50)

assertion_reason(T_PS, "Limiting factors", "Advanced",
                 "When the CO₂ concentration rises above about 360 µL L⁻¹, the rate of photosynthesis of C3 plants "
                 "increases.",
                 "C3 plants show saturation of photosynthesis at about 360 µL L⁻¹ of CO₂.",
                 True, False, False, "C",
                 "CO₂ response of C3 and C4 plants",
                 "NCERT: C4 plants show saturation at about 360 µL L⁻¹, while C3 plants respond to increased CO₂ "
                 "concentration and saturation is seen only beyond 450 µL L⁻¹. So raising CO₂ above 360 µL L⁻¹ still "
                 "increases photosynthesis in C3 plants; it is the C4 plants that are saturated at that level.",
                 ["A: true", "R: false - saturation at about 360 µL L⁻¹ is for C4 plants; C3 plants saturate only "
                  "beyond 450 µL L⁻¹"],
                 ncert=ref("PS", "Factors affecting Photosynthesis (carbon dioxide concentration)"), secs=45)

# =============================================================== 8. Respiration in Plants (3/4/3)
statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "Glycolysis takes place in the matrix of the mitochondria.",
               "In aerobic respiration, NAD⁺ is the final acceptor of electrons in the electron transport system.",
               False, False, "B",
               "Site of glycolysis; final electron acceptor",
               "Glycolysis occurs in the cytoplasm of the cell and is present in all living organisms. In aerobic "
               "respiration, electrons from NADH and FADH₂ pass through the electron transport system and are "
               "finally accepted by oxygen, which is reduced to water; NAD⁺ is the acceptor that is reduced to NADH "
               "in glycolysis and the TCA cycle.",
               ["Statement I: false; glycolysis is in the cytoplasm",
                "Statement II: false; oxygen is the final acceptor"],
               ncert=ref("RES", "Glycolysis; Electron Transport System (ETS) and Oxidative Phosphorylation"),
               secs=25)

direct(T_RES, "ATP yield and amphibolic pathway", "Basic",
       "NCERT suggests that the respiratory pathway is better considered an amphibolic pathway rather than a "
       "catabolic one, because it:",
       "is involved in both anabolism and catabolism",
       ["occurs in both the cytoplasm and the mitochondria", "can run both with and without oxygen",
        "produces both ATP and GTP"], "C",
       "Amphibolic nature of respiration",
       "Substrates such as fatty acids are broken down to acetyl CoA before entering the pathway, and when the "
       "organism needs to synthesise fatty acids, acetyl CoA is withdrawn from it. Because the respiratory pathway "
       "is involved in both anabolism and catabolism, NCERT considers it an amphibolic pathway.",
       ["Breakdown (catabolism) + withdrawal of intermediates for synthesis (anabolism)",
        "-> amphibolic pathway"],
       why="The pathway does occur in two compartments, has anaerobic and aerobic variants and forms ATP and GTP, "
           "but none of these is NCERT's reason for calling it amphibolic.",
       ncert=ref("RES", "Amphibolic Pathway"), secs=25)

assertion_reason(T_RES, "Glycolysis and fermentation", "Basic",
                 "In lactic acid fermentation, CO₂ is removed from pyruvic acid.",
                 "In lactic acid fermentation, pyruvic acid is reduced to lactic acid by lactate dehydrogenase.",
                 False, True, False, "D",
                 "Lactic acid fermentation",
                 "In some bacteria, and in animal muscle when oxygen is inadequate during exercise, pyruvic acid is "
                 "reduced to lactic acid by lactate dehydrogenase, with NADH + H⁺ as the reducing agent. No CO₂ is "
                 "released; CO₂ is released in alcoholic fermentation, where pyruvic acid forms CO₂ and ethanol.",
                 ["A: false - no CO₂ is released in lactic acid fermentation", "R: true"],
                 ncert=ref("RES", "Fermentation"), secs=30)

match_list(T_RES, "ATP yield and amphibolic pathway", "Intermediate", "respiratory substrate",
           "how it enters the respiratory pathway",
           ["Glycerol (from fats)", "Fatty acids", "Amino acids (after deamination)", "Sucrose"],
           ["After being converted to PGAL",
            "As glucose and fructose formed by the enzyme invertase, which enter glycolysis",
            "At some stage within the Krebs cycle, or as pyruvate or acetyl CoA, depending on structure",
            "After being degraded to acetyl CoA"],
           "I IV III II", ["IV I III II", "I IV II III", "III IV I II"], "A",
           "Entry of different substrates into respiration",
           "NCERT: fats are first broken down into glycerol and fatty acids. Glycerol enters the pathway after being "
           "converted to PGAL, and fatty acids are degraded to acetyl CoA before entering. Proteins are degraded by "
           "proteases, and the amino acids (after deamination) enter at some stage within the Krebs cycle or as "
           "pyruvate or acetyl CoA. Sucrose is converted into glucose and fructose by invertase, and these enter "
           "glycolysis.",
           ["Glycerol -> I (PGAL)", "Fatty acids -> IV (acetyl CoA)", "Amino acids -> III",
            "Sucrose -> II (invertase)"],
           why="The wrong codes swap glycerol with fatty acids, amino acids with sucrose, or glycerol with amino "
               "acids.",
           ncert=ref("RES", "Glycolysis; Amphibolic Pathway"), secs=50)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "In alcoholic fermentation by yeast, CO₂ is released.",
                 "In alcoholic fermentation, the CO₂ is released by the enzyme alcohol dehydrogenase.",
                 True, False, False, "C",
                 "Enzymes of alcoholic fermentation",
                 "In yeast, under anaerobic conditions, pyruvic acid is converted to CO₂ and ethanol by two enzymes: "
                 "pyruvic acid decarboxylase, which removes CO₂ from pyruvic acid, and alcohol dehydrogenase, which "
                 "forms ethanol using NADH + H⁺ as the reducing agent. Alcohol dehydrogenase does not release CO₂.",
                 ["A: true", "R: false - the decarboxylase, not alcohol dehydrogenase, removes CO₂"],
                 ncert=ref("RES", "Fermentation"), secs=35)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "In which of the following steps of aerobic respiration is ATP (or GTP) formed directly, without the "
                "electron transport system?",
                [("Glucose -> glucose-6-phosphate", False),
                 ("1,3-Bisphosphoglyceric acid (BPGA) -> 3-phosphoglyceric acid (PGA)", True),
                 ("Fructose-6-phosphate -> fructose 1,6-bisphosphate", False),
                 ("Phosphoenolpyruvate (PEP) -> pyruvic acid", True),
                 ("Succinyl CoA -> succinic acid", True)],
                [("b", "d"), ("a", "b", "d"), ("c", "d", "e")], "B",
                "Direct synthesis of ATP and GTP",
                "In glycolysis, ATP is used at two steps (glucose to glucose-6-phosphate, and fructose-6-phosphate to "
                "fructose 1,6-bisphosphate) and formed directly at two steps (BPGA to PGA, and PEP to pyruvic acid). "
                "In the TCA cycle, a molecule of GTP is synthesised when succinyl CoA is converted to succinic acid "
                "(substrate level phosphorylation).",
                ["(a), (c): ATP is used", "(b), (d): ATP formed directly", "(e): GTP formed"],
                why="(b) and (d) only leaves out the GTP step of the TCA cycle. The other combinations include a step "
                    "that uses ATP rather than forming it.",
                ncert=ref("RES", "Glycolysis; Tricarboxylic Acid Cycle"), secs=55)

statement_pair(T_RES, "TCA cycle", "Intermediate",
               "In the TCA cycle, citric acid is isomerised to isocitrate.",
               "In the TCA cycle, α-ketoglutaric acid is formed by the condensation of the acetyl group with "
               "oxaloacetic acid.",
               True, False, "C",
               "Early steps of the TCA cycle",
               "The TCA cycle starts with the condensation of the acetyl group with oxaloacetic acid (OAA) and water "
               "to yield citric acid, catalysed by citrate synthase. Citrate is then isomerised to isocitrate, which "
               "is followed by two successive decarboxylations leading to α-ketoglutaric acid and then succinyl CoA.",
               ["Statement I: true", "Statement II: false; the condensation forms citric acid, and α-ketoglutaric "
                "acid comes later by decarboxylation"],
               ncert=ref("RES", "Tricarboxylic Acid Cycle"), secs=35)

multi_statement(T_RES, "Electron transport system", "Advanced",
                "Which of the following are true of BOTH oxidative phosphorylation in mitochondria and "
                "photophosphorylation in chloroplasts?",
                [("ATP synthase has an integral membrane part forming a proton channel and a headpiece where ATP is "
                  "made.", True),
                 ("The energy used to build the proton gradient comes from light.", False),
                 ("ATP is synthesised as protons move through the channel down their gradient.", True),
                 ("Oxygen is the final acceptor of the electrons.", False),
                 ("Electrons pass along a chain of electron carriers.", True)],
                [("a", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Comparing the two kinds of phosphorylation",
                "Both use a chemiosmotic mechanism: electron transport through a chain of carriers builds a proton "
                "gradient, and ATP synthase (F₀/F₁ in mitochondria, CF₀/CF₁ in chloroplasts) makes ATP as protons "
                "flow through its channel. In oxidative phosphorylation the energy comes from oxidation-reduction "
                "and oxygen is the final electron acceptor; in photophosphorylation the energy comes from light and "
                "the electrons finally reduce NADP⁺.",
                ["(a), (c), (e): common to both", "(b): only photophosphorylation",
                 "(d): only oxidative phosphorylation"],
                why="(a) and (c) only leaves out the electron transport chain. The other combinations include (b) or "
                    "(d), each true of only one process.",
                ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=60)

direct(T_RES, "ATP yield and amphibolic pathway", "Advanced",
       "Which compound is formed BOTH by the degradation of fatty acids and by the oxidative decarboxylation of "
       "pyruvic acid, before entering the TCA cycle?",
       "Acetyl CoA",
       ["PGAL", "Oxaloacetic acid", "Citric acid"], "B",
       "Meeting point of fat and carbohydrate breakdown",
       "Pyruvic acid from glycolysis undergoes oxidative decarboxylation by pyruvic dehydrogenase to form acetyl "
       "CoA. Fatty acids are also degraded to acetyl CoA before entering the respiratory pathway. Acetyl CoA then "
       "condenses with OAA to form citric acid in the TCA cycle.",
       ["Pyruvic acid -> acetyl CoA", "Fatty acids -> acetyl CoA", "Common product = acetyl CoA"],
       why="PGAL is the entry point of glycerol, not of fatty acids. OAA and citric acid are TCA-cycle "
           "intermediates, not products of fatty-acid degradation before the cycle.",
       ncert=ref("RES", "Aerobic Respiration; Amphibolic Pathway"), secs=40)

assertion_reason(T_RES, "Electron transport system", "Advanced",
                 "If oxygen is absent, the TCA cycle continues normally, because no step of the cycle itself uses "
                 "oxygen.",
                 "Oxygen acts as the final hydrogen acceptor in the electron transport system.",
                 False, True, False, "D",
                 "Dependence of the TCA cycle on oxygen",
                 "The continued oxidation of acetyl CoA in the TCA cycle requires the continued regeneration of NAD⁺ "
                 "and FAD⁺ from NADH and FADH₂, which are oxidised in the electron transport system. Oxygen is the "
                 "final hydrogen acceptor of that system; NCERT stresses that, though its role is limited to the "
                 "terminal stage, the presence of oxygen is vital, as it drives the whole process. So the cycle "
                 "cannot continue normally without oxygen.",
                 ["A: false - without O₂ the ETS stops, NAD⁺/FAD⁺ are not regenerated and the cycle cannot continue",
                  "R: true"],
                 ncert=ref("RES", "Tricarboxylic Acid Cycle; Electron Transport System"), secs=50)

# =============================================================== 9. Plant Growth and Development (3/5/3)
_promoters = {"IAA": True, "IBA": True, "GA3": True, "kinetin": True, "zeatin": True, "ABA": False}
numerical(T_PGD, "Plant growth regulators", "Basic",
          "NCERT broadly divides plant growth regulators into growth promoters and growth inhibitors. How many of "
          "the following belong to the growth-promoting group?\n\nindole-3-acetic acid (IAA), indole butyric acid "
          "(IBA), gibberellic acid (GA₃), kinetin, zeatin, abscisic acid (ABA)",
          "5", ["3", "4", "6"], "A",
          sum(_promoters.values()) == 5,
          "Promoters and inhibitors among PGRs",
          "NCERT: one group of PGRs is involved in growth-promoting activities such as cell division, cell "
          "enlargement, pattern formation, tropic growth, flowering, fruiting and seed formation - the auxins, "
          "gibberellins and cytokinins. The other group, which includes abscisic acid, plays an important role in "
          "responses to wounds and stresses and in dormancy and abscission. IAA and IBA are auxins, GA₃ is a "
          "gibberellin, and kinetin and zeatin are cytokinins.",
          ["Auxins: IAA, IBA", "Gibberellin: GA₃", "Cytokinins: kinetin, zeatin", "Inhibitor: ABA",
           "Promoters = 5"],
          why="3 counts only one member of each promoter group. 4 leaves out one of the two cytokinins or one of "
              "the two auxins. 6 wrongly counts ABA, a growth inhibitor.",
          ncert=ref("PGD", "Plant Growth Regulators (characteristics)"), secs=40)

direct(T_PGD, "Plant growth regulators", "Basic",
       "Which of the following is NOT an auxin?",
       "Zeatin",
       ["Indole-3-acetic acid (IAA)", "Indole butyric acid (IBA)", "Naphthalene acetic acid (NAA)"], "D",
       "Identifying auxins",
       "IAA and IBA are natural auxins isolated from plants, and NAA (with 2,4-D) is a synthetic auxin. Zeatin is a "
       "naturally occurring cytokinin isolated from corn kernels and coconut milk.",
       ["Auxins: IAA, IBA (natural), NAA, 2,4-D (synthetic)", "Zeatin: cytokinin"],
       why="IAA, IBA and NAA are all auxins named in NCERT.",
       ncert=ref("PGD", "Plant Growth Regulators (auxins; cytokinins)"), secs=20)

statement_pair(T_PGD, "Plant growth regulators", "Basic",
               "Abscisic acid was discovered for its role in regulating abscission and dormancy.",
               "Ethylene is used to initiate flowering and to synchronise fruit-set in pineapples.",
               True, True, "A",
               "Abscisic acid; ethylene in pineapple",
               "NCERT: abscisic acid was discovered for its role in regulating abscission and dormancy. Ethylene is "
               "used to initiate flowering and to synchronise fruit-set in pineapples, and it also induces flowering "
               "in mango.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=25)

match_list(T_PGD, "Plant growth regulators", "Intermediate", "plant growth regulator",
           "site of production or source described in NCERT",
           ["Auxins (natural)", "Cytokinins (natural)", "Ethylene", "Kinetin"],
           ["Tissues undergoing senescence and ripening fruits, in large amounts",
            "Growing apices of the stems and roots",
            "Autoclaved herring sperm DNA",
            "Regions of rapid cell division, such as root apices, developing shoot buds and young fruits"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "A",
           "Where PGRs come from",
           "Auxins are generally produced by the growing apices of the stems and roots, from where they migrate to "
           "their regions of action. Natural cytokinins are synthesised in regions where rapid cell division occurs, "
           "such as root apices, developing shoot buds and young fruits. Ethylene is synthesised in large amounts by "
           "tissues undergoing senescence and by ripening fruits. Kinetin was discovered as a modified form of "
           "adenine in autoclaved herring sperm DNA.",
           ["Auxins -> II", "Cytokinins -> IV", "Ethylene -> I", "Kinetin -> III"],
           why="The wrong codes swap auxins with cytokinins, ethylene with kinetin, or cytokinins with ethylene.",
           ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=50)

assertion_reason(T_PGD, "Plant growth regulators", "Intermediate",
                 "Abscisic acid stimulates the closure of stomata.",
                 "Chemically, abscisic acid is a derivative of carotenoids.",
                 True, True, False, "B",
                 "Two separate facts about ABA",
                 "Abscisic acid acts as a general plant growth inhibitor and an inhibitor of plant metabolism; it "
                 "inhibits seed germination, stimulates the closure of stomata and increases tolerance to stresses. "
                 "Separately, NCERT classifies ABA chemically as a derivative of carotenoids. Its chemical origin is "
                 "not given as the reason for its effect on stomata.",
                 ["A: true", "R: true", "The chemical class of ABA does not explain stomatal closure -> R is not "
                  "the explanation"],
                 ncert=ref("PGD", "Plant Growth Regulators (characteristics; abscisic acid)"), secs=35)

multi_statement(T_PGD, "Plant growth regulators", "Intermediate",
                "Which of the following effects are attributed to abscisic acid in NCERT?",
                [("It promotes female flowers in cucumbers.", False),
                 ("It inhibits seed germination.", True),
                 ("It stimulates the closure of stomata.", True),
                 ("It helps to overcome apical dominance.", False),
                 ("It increases the tolerance of plants to various kinds of stresses.", True)],
                [("b", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Effects of abscisic acid",
                "ABA regulates abscission and dormancy, inhibits seed germination, stimulates the closure of stomata "
                "and increases tolerance to various stresses (hence 'stress hormone'). Promotion of female flowers "
                "in cucumbers is an effect of ethylene, and overcoming apical dominance is an effect of cytokinins.",
                ["(b), (c), (e): ABA", "(a): ethylene", "(d): cytokinins"],
                why="(b) and (c) only leaves out the stress tolerance that gives ABA the name stress hormone. The other "
                    "combinations include an effect of ethylene or of cytokinins.",
                ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (abscisic acid)"), secs=50)

direct(T_PGD, "Plant growth regulators", "Intermediate",
       "Which plant growth regulator BOTH promotes root growth and root hair formation and promotes the senescence "
       "and abscission of plant organs, especially of leaves and flowers?",
       "Ethylene",
       ["Cytokinin", "Gibberellin", "Abscisic acid"], "A",
       "Effects of ethylene",
       "NCERT: ethylene promotes senescence and abscission of plant organs, especially of leaves and flowers. It "
       "also promotes root growth and root hair formation, thus helping plants to increase their absorption "
       "surface.",
       ["Root growth and root hairs: ethylene", "Senescence and abscission of leaves and flowers: ethylene"],
       why="Cytokinins delay leaf senescence. Gibberellins delay senescence and are not linked with root hairs. "
           "ABA regulates abscission and dormancy, but NCERT does not credit it with promoting root hairs.",
       ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (ethylene)"), secs=35)

statement_pair(T_PGD, "Growth rate", "Intermediate",
               "In geometric growth, the initial growth is slow (lag phase), and it increases rapidly thereafter at "
               "an exponential rate (log phase).",
               "In arithmetic growth, a plot of length against time gives a sigmoid curve.",
               True, False, "C",
               "Geometric and arithmetic growth curves",
               "In geometric growth the initial growth is slow (lag phase) and then rises rapidly at an exponential "
               "rate (log or exponential phase); with limited nutrients it slows down to a stationary phase, giving "
               "a sigmoid curve. In arithmetic growth, only one daughter cell continues to divide, and a plot of "
               "length against time gives a linear curve.",
               ["Statement I: true", "Statement II: false; arithmetic growth gives a straight line"],
               ncert=ref("PGD", "Growth (growth rates)"), secs=35)

direct(T_PGD, "Differentiation and redifferentiation", "Advanced",
       "In a woody dicot, a parenchyma cell formed from a meristem matures and loses the ability to divide. Later it "
       "regains that ability and becomes part of the cork cambium, which cuts off cork cells that again lose the "
       "capacity to divide. Which sequence of processes does this show?",
       "Differentiation -> dedifferentiation -> redifferentiation",
       ["Dedifferentiation -> differentiation -> redifferentiation",
        "Differentiation -> redifferentiation -> dedifferentiation",
        "Redifferentiation -> dedifferentiation -> differentiation"], "A",
       "Differentiation, dedifferentiation and redifferentiation",
       "Cells derived from meristems mature to perform specific functions - differentiation. Living differentiated "
       "cells that have lost the capacity to divide can regain it, as when the cork cambium forms from fully "
       "differentiated parenchyma cells - dedifferentiation. The cells produced by such a dedifferentiated "
       "meristem again lose the capacity to divide and mature to perform specific functions - redifferentiation.",
       ["Meristem cell -> parenchyma: differentiation", "Parenchyma -> cork cambium: dedifferentiation",
        "Cork cambium -> cork cells: redifferentiation"],
       why="The other options put the steps in the wrong order: dedifferentiation can only act on a cell that has "
           "already differentiated, and redifferentiation needs a dedifferentiated meristem.",
       ncert=ref("PGD", "Differentiation, Dedifferentiation and Redifferentiation"), secs=50)

assertion_reason(T_PGD, "Plant growth regulators", "Advanced",
                 "Auxins promote the abscission of older, mature leaves and fruits.",
                 "Auxins prevent fruit and leaf drop at all stages of development.",
                 True, False, False, "C",
                 "Dual effect of auxins on abscission",
                 "NCERT: auxins prevent fruit and leaf drop at early stages but promote the abscission of older, "
                 "mature leaves and fruits. The prevention of drop is limited to early stages, so R overstates it.",
                 ["A: true", "R: false - auxins prevent drop only at early stages"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (auxins)"), secs=40)

statement_pair(T_PGD, "Plant growth regulators", "Advanced",
               "Both ethylene and abscisic acid promote seed germination.",
               "Both gibberellins and cytokinins strengthen apical dominance.",
               False, False, "B",
               "Opposing and shared effects of PGRs",
               "Ethylene breaks seed and bud dormancy and initiates germination in peanut seeds, but abscisic acid "
               "inhibits seed germination. Auxins cause apical dominance, while cytokinins help to overcome it; NCERT "
               "does not credit gibberellins with strengthening apical dominance.",
               ["Statement I: false; ABA inhibits seed germination",
                "Statement II: false; cytokinins overcome apical dominance"],
               ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=45)
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
    assert pkg["output"] == "batches/parts/BATCH_010_BOT_p1.json"


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
           "notes": "Package BOT_010_p1 (Botany): Living World and Classification, Plant Kingdom, Morphology, Anatomy, "
                    "Cell, Cell Cycle, Photosynthesis, Respiration, Plant Growth. 125 original questions, NCERT "
                    "referenced; numerical answers recomputed by the builder; answer positions chosen by hand.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; keys {dict(sorted(keys.items()))}; formats {dict(fmts)}; "
          f"difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}")
