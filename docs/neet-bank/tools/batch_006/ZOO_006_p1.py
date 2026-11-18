"""Writes batches/parts/BATCH_006_ZOO_p1.json: package ZOO_006_p1 of BATCH_006 (Zoology, 122 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_001251 .. NEET_ZOO_001372. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, subtopics, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11
Biology textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion and absorption). Facts
already tested in BATCH_000 to BATCH_005 (see `merge_batch.py stems 006 ZOO_006_p1`) are not tested again.

    python docs/neet-bank/tools/batch_006/ZOO_006_p1.py
"""

import json
import re
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
ZOO = "Zoology"
PACKAGE = "ZOO_006_p1"
BATCH = "BATCH_006"
FIRST_ID, LAST_ID = 1251, 1372
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")

QUESTIONS = []

AK = "Animal Kingdom"
SOA = "Structural Organisation in Animals"
BIO = "Biomolecules"
BRE = "Breathing and Exchange of Gases"
BFC = "Body Fluids and Circulation"
EXC = "Excretory Products and their Elimination"
LOC = "Locomotion and Movement"
NEU = "Neural Control and Coordination"


def ref(chapter, section):
    return f"Class 11 Biology, '{chapter}', {section}"


def Z(topic, subtopic, difficulty, fmt, text, options, answer, concept, explanation, steps, ncert,
      shortcut=None, why_others_wrong=None, seconds=45, verified_by=AUTHORED):
    """Appends one Zoology question with the next ID in the package range."""
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4
    assert ncert, "every Zoology question needs an NCERT reference"
    if fmt == "assertion_reason":
        assert options == ASSERTION_REASON
    if fmt == "statement_pair":
        assert options == STATEMENT_PAIR
    if fmt == "numerical":
        assert verified_by == RECOMPUTED
    qid = f"NEET_ZOO_{FIRST_ID + len(QUESTIONS):06d}"
    QUESTIONS.append({
        "question_id": qid, "exam_mappings": default_mappings(ZOO), "subject": ZOO, "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why_others_wrong, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(verified_by), "verified_at": TODAY},
    })


def match_options(correct: dict, wrong: list, at: str) -> list:
    """Option texts for a match-the-list question with the correct code at position `at`."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    for m in [correct, *wrong]:
        assert sorted(m) == list("ABCD") and sorted(m.values()) == sorted(["I", "II", "III", "IV"])
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4
    return opts


def M(a, b, c, d):
    return {"A": a, "B": b, "C": c, "D": d}


def ar(assertion, reason):
    return ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {assertion}\nReason (R): {reason}\n\n"
            "Choose the correct answer from the options given below:")


def sp(one, two):
    return (f"Given below are two statements:\n\nStatement I: {one}\nStatement II: {two}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")


def ml(intro, list1, list2):
    l1 = "\n".join(f"{k}. {v}" for k, v in zip("ABCD", list1))
    l2 = "\n".join(f"{k}. {v}" for k, v in zip(["I", "II", "III", "IV"], list2))
    return (f"Match List-I ({intro[0]}) with List-II ({intro[1]}).\n\nList-I:\n{l1}\n\nList-II:\n{l2}\n\n"
            "Choose the correct answer from the options given below:")


def ms(lead, statements):
    body = "\n".join(f"({chr(97 + i)}) {s}" for i, s in enumerate(statements))
    return f"{lead}\n\n{body}\n\nChoose the correct answer from the options given below:"


def ms_check(truth: str, options: list, answer: str):
    """Asserts that the multi-statement option at `answer` is exactly the set of true statements, e.g. 'abd'."""
    sets = ["".join(sorted(re.findall(r"\(([a-e])\)", o))) for o in options]
    assert sets[LETTERS.index(answer)] == "".join(sorted(truth)), (sets, truth)
    assert sets.count("".join(sorted(truth))) == 1



# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "NCERT groups some arthropod examples by their importance to humans. Anopheles, Culex and Aedes are listed as:",
  ["Vectors", "Economically important insects", "Gregarious pests", "Living fossils"], "A",
  "Examples of Arthropoda",
  "NCERT lists the examples of Arthropoda as: economically important insects – Apis (honey bee), Bombyx (silkworm), "
  "Laccifer (lac insect); vectors – Anopheles, Culex and Aedes (mosquitoes); gregarious pest – Locusta (locust); "
  "living fossil – Limulus (king crab).",
  ["Anopheles, Culex, Aedes = mosquitoes = vectors"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="Economically important insects are Apis, Bombyx and Laccifer; the gregarious pest is Locusta; "
                   "the living fossil is Limulus.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Aptenodytes, one of the examples of class Aves given in NCERT, is commonly known as the:",
  ["Vulture", "Penguin", "Ostrich", "Peacock"], "B",
  "Examples of Aves",
  "NCERT examples of Aves: Corvus (crow), Columba (pigeon), Psittacula (parrot), Struthio (ostrich), Pavo "
  "(peacock), Aptenodytes (penguin) and Neophron (vulture).",
  ["Aptenodytes → penguin"],
  R_AK("class Aves"),
  why_others_wrong="The vulture is Neophron, the ostrich is Struthio and the peacock is Pavo.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "match_list",
  ml(("mammal genus", "common name"), ["Camelus", "Elephas", "Equus", "Felis"], ["Horse", "Cat", "Camel", "Elephant"]),
  match_options(M("III", "IV", "I", "II"), [M("III", "I", "IV", "II"), M("II", "IV", "I", "III"),
                                            M("IV", "III", "II", "I")], "C"), "C",
  "Examples of Mammalia",
  "NCERT examples of viviparous mammals include Camelus (camel), Elephas (elephant), Equus (horse) and Felis (cat), "
  "along with Macaca, Rattus, Canis, Delphinus, Balaenoptera and Panthera.",
  ["Camelus → camel (III)", "Elephas → elephant (IV)", "Equus → horse (I)", "Felis → cat (II)"],
  R_AK("class Mammalia"),
  why_others_wrong="A swaps Elephas and Equus; B swaps Camelus and Felis; D mismatches all four genera.",
  seconds=30)

Z(AK, "Chordate classes", "Basic", "direct",
  "Which pair of bony fishes is given in NCERT as examples of aquarium fishes?",
  ["Labeo and Catla", "Exocoetus and Hippocampus", "Scoliodon and Pristis", "Betta and Pterophyllum"], "D",
  "Examples of Osteichthyes",
  "NCERT examples of Osteichthyes: marine – Exocoetus (flying fish), Hippocampus (sea horse); fresh water – Labeo "
  "(rohu), Catla (katla), Clarias (magur); aquarium – Betta (fighting fish), Pterophyllum (angel fish).",
  ["Aquarium fishes → Betta, Pterophyllum"],
  R_AK("class Osteichthyes"),
  why_others_wrong="Labeo and Catla are freshwater food fishes; Exocoetus and Hippocampus are marine bony fishes; "
                   "Scoliodon and Pristis are cartilaginous fishes, not bony fishes.",
  seconds=20)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "NCERT describes the polyp as the sessile and cylindrical body form of cnidarians. Which pair of animals does it "
  "cite as examples of this form?",
  ["Aurelia and Hydra", "Pleurobrachia and Ctenoplana", "Hydra and Adamsia", "Adamsia and Aurelia"], "C",
  "Polyp and medusa",
  "NCERT: cnidarians exhibit two basic body forms, polyp and medusa. The polyp is a sessile and cylindrical form like "
  "Hydra and Adamsia, whereas the medusa is umbrella-shaped and free-swimming like Aurelia (jelly fish).",
  ["Polyp → Hydra, Adamsia", "Medusa → Aurelia"],
  R_AK("phylum Coelenterata (Cnidaria)"),
  why_others_wrong="A and D include Aurelia, which is the example of the medusa form; Pleurobrachia and Ctenoplana "
                   "are ctenophores, which do not have polyp and medusa forms.",
  seconds=25)

Z(AK, "Basis of classification", "Basic", "statement_pair",
  sp("In an open circulatory system, the blood is pumped out of the heart and the cells and tissues are directly "
     "bathed in it.",
     "In a closed circulatory system, the blood is circulated through a series of vessels of varying diameters – "
     "arteries, veins and capillaries."),
  STATEMENT_PAIR, "A",
  "Open and closed circulatory systems",
  "NCERT describes the circulatory system as of two types: the open type, in which blood is pumped out of the heart "
  "and the cells and tissues are directly bathed in it, and the closed type, in which blood circulates through a "
  "series of vessels of varying diameters (arteries, veins and capillaries). Both statements are correct.",
  ["Statement I → true", "Statement II → true"],
  R_AK("basis of classification: circulatory system"),
  why_others_wrong="Each statement is NCERT's own description of one type, so neither is false.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "According to NCERT, which pair of phyla both have an open type of circulatory system?",
  ["Annelida and Arthropoda", "Arthropoda and Hemichordata", "Annelida and Chordata", "Hemichordata and Chordata"],
  "B",
  "Circulatory system across phyla",
  "NCERT states that in Arthropoda the circulatory system is of open type, and that in Hemichordata the circulatory "
  "system is of open type. Annelids have a closed circulatory system, and chordates too have a closed circulatory "
  "system.",
  ["Arthropoda → open", "Hemichordata → open", "Annelida, Chordata → closed"],
  R_AK("phyla Arthropoda and Hemichordata"),
  why_others_wrong="A and C each include Annelida, whose circulation is closed; C and D include Chordata, whose "
                   "circulation is also closed.",
  seconds=35)

Z(AK, "Basis of classification", "Intermediate", "assertion_reason",
  ar("Ascaris, the roundworm, is a triploblastic animal.",
     "In its embryo, a third germinal layer, the mesoderm, is present in between the ectoderm and the endoderm."),
  ASSERTION_REASON, "A",
  "Diploblastic and triploblastic organisation",
  "NCERT: animals in which the developing embryo has a third germinal layer, mesoderm, in between the ectoderm and "
  "endoderm are called triploblastic animals (platyhelminthes to chordates). Ascaris is an aschelminth, so it is "
  "triploblastic, and the presence of the mesoderm is exactly what makes it so.",
  ["A true – aschelminths are triploblastic", "R true – mesoderm between ectoderm and endoderm",
   "R is the definition of A → R explains A"],
  R_AK("basis of classification: diploblastic and triploblastic organisation"),
  why_others_wrong="B is wrong because having three germinal layers is precisely what 'triploblastic' means; C and D "
                   "are wrong because both statements are true.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "multi_statement",
  ms("Which of the following statements about bony fishes (class Osteichthyes) are correct?",
     ["Their skin is covered with cycloid or ctenoid scales.",
      "Their heart is two-chambered, with one auricle and one ventricle.",
      "They are homoiothermous (warm-blooded).",
      "An air bladder is absent in them.",
      "Labeo and Catla are freshwater bony fishes."]),
  ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only", "(a), (b) and (e) only"], "D",
  "Features of Osteichthyes",
  "NCERT: in bony fishes the skin is covered with cycloid/ctenoid scales; the heart is two-chambered (one auricle and "
  "one ventricle); they are cold-blooded; an air bladder is present which regulates buoyancy. Labeo (rohu) and Catla "
  "(katla) are listed as freshwater bony fishes.",
  ["(a) true", "(b) true", "(c) false – cold-blooded", "(d) false – air bladder present", "(e) true"],
  R_AK("class Osteichthyes"),
  why_others_wrong="A includes (c); B and C include (d); A and B also leave out true statements.",
  seconds=50)
ms_check("abe", ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only",
                 "(a), (b) and (e) only"], "D")

Z(AK, "Chordate classes", "Intermediate", "direct",
  "NCERT notes that some mammals are adapted to fly and some to live in water. Which pair gives one mammal of each "
  "kind, in that order?",
  ["Macropus and Delphinus", "Pteropus and Macropus", "Pteropus and Balaenoptera", "Ornithorhynchus and Camelus"],
  "C",
  "Adaptations among mammals",
  "NCERT: mammals are found in a variety of habitats, and some of them have adapted to fly or live in water. Among "
  "its examples, Pteropus is the flying fox (a flying mammal) and Balaenoptera is the blue whale (an aquatic "
  "mammal).",
  ["Flying → Pteropus (flying fox)", "Aquatic → Balaenoptera (blue whale)"],
  R_AK("class Mammalia"),
  why_others_wrong="Macropus (kangaroo) does not fly; Pteropus–Macropus gives no aquatic mammal; Ornithorhynchus "
                   "(platypus) and Camelus (camel) are neither flying nor the NCERT aquatic example.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("Mammals have two pairs of limbs, adapted for walking, running, climbing, burrowing, swimming or flying.",
     "In mammals, fertilisation is external."),
  STATEMENT_PAIR, "C",
  "Features of Mammalia",
  "NCERT: mammals have two pairs of limbs, adapted for walking, running, climbing, burrowing, swimming or flying. "
  "Sexes are separate and fertilisation is internal; they are viviparous with a few exceptions and development is "
  "direct.",
  ["Statement I → true", "Statement II → false (internal fertilisation)"],
  R_AK("class Mammalia"),
  why_others_wrong="A and D accept external fertilisation; B rejects NCERT's description of mammalian limbs.",
  seconds=30)

Z(AK, "Chordate classes", "Intermediate", "match_list",
  ml(("animal", "heart"), ["Scoliodon", "Rana", "Crocodilus", "Columba"],
     ["Two-chambered heart with one auricle and one ventricle",
      "Three-chambered heart with two auricles and one ventricle",
      "Four-chambered heart in a cold-blooded (poikilothermous) animal",
      "Four-chambered heart in a warm-blooded (homoiothermous) animal"]),
  match_options(M("I", "II", "III", "IV"), [M("I", "II", "IV", "III"), M("II", "I", "III", "IV"),
                                            M("I", "III", "II", "IV")], "B"), "B",
  "Heart chambers and thermoregulation across vertebrate classes",
  "NCERT: cartilaginous fishes such as Scoliodon have a two-chambered heart (one auricle, one ventricle); amphibians "
  "such as Rana have a three-chambered heart (two auricles, one ventricle); the reptilian heart is usually "
  "three-chambered but four-chambered in crocodiles, and reptiles are poikilotherms; birds such as Columba have a "
  "four-chambered heart and are warm-blooded.",
  ["Scoliodon → I", "Rana → II", "Crocodilus → III (four chambers, but a poikilotherm)", "Columba → IV"],
  R_AK("classes Chondrichthyes, Amphibia, Reptilia and Aves"),
  why_others_wrong="A swaps the crocodile and the pigeon (the crocodile is cold-blooded); C swaps the fish and the "
                   "frog; D swaps the frog and the crocodile.",
  seconds=45)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("In arthropods, the body consists of head, thorax and abdomen.",
     "Arthropods have a closed type of circulatory system."),
  ASSERTION_REASON, "C",
  "Features of Arthropoda",
  "NCERT: the body of arthropods consists of head, thorax and abdomen, and is covered by a chitinous exoskeleton. "
  "Their circulatory system is of the open type, so the Reason is false.",
  ["A true", "R false – circulation is open"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="A and B treat R as true; D treats the correct Assertion as false.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("Platyhelminthes have a dorso-ventrally flattened body, hence they are called flatworms.",
     "Fasciola, an example of Platyhelminthes, is commonly known as the liver fluke."),
  STATEMENT_PAIR, "A",
  "Platyhelminthes",
  "NCERT: platyhelminths have a dorso-ventrally flattened body, hence are called flatworms. Its examples are Taenia "
  "(tapeworm) and Fasciola (liver fluke). Both statements are true.",
  ["Statement I → true", "Statement II → true"],
  R_AK("phylum Platyhelminthes"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

Z(AK, "Basis of classification", "Advanced", "direct",
  "Which of the following sequences lists one acoelomate, one pseudocoelomate and one coelomate animal, in that "
  "order?",
  ["Ancylostoma, Taenia, Hirudinaria", "Hirudinaria, Ancylostoma, Taenia", "Taenia, Hirudinaria, Ancylostoma",
   "Taenia, Ancylostoma, Hirudinaria"], "D",
  "Body cavity as a basis of classification",
  "NCERT: animals without a body cavity are acoelomates, e.g. platyhelminthes (Taenia, the tapeworm). In "
  "pseudocoelomates the body cavity is not lined by mesoderm, e.g. aschelminthes (Ancylostoma, the hookworm). "
  "Coelomates have a true coelom lined by mesoderm, e.g. annelids (Hirudinaria, the blood-sucking leech).",
  ["Taenia → Platyhelminthes → acoelomate", "Ancylostoma → Aschelminthes → pseudocoelomate",
   "Hirudinaria → Annelida → coelomate"],
  R_AK("basis of classification: coelom"),
  shortcut="Flat → none; round → pseudo; ringed → true coelom.",
  why_others_wrong="A swaps the flatworm and the roundworm; B puts the coelomate leech first; C swaps the leech and "
                   "the hookworm.",
  seconds=45)

Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following pairs consist of two animals belonging to the same class?",
     ["Naja and Chelone", "Aptenodytes and Struthio", "Ichthyophis and Hippocampus", "Pteropus and Neophron",
      "Petromyzon and Myxine"]),
  ["(a), (b) and (e) only", "(b), (c) and (e) only", "(a), (d) and (e) only", "(a), (b), (c) and (e) only"], "A",
  "Classes of vertebrates",
  "Naja (cobra) and Chelone (turtle) are both reptiles; Aptenodytes (penguin) and Struthio (ostrich) are both birds; "
  "Petromyzon (lamprey) and Myxine (hagfish) are both cyclostomes. Ichthyophis is a limbless amphibian while "
  "Hippocampus (sea horse) is a bony fish; Pteropus (flying fox) is a mammal while Neophron (vulture) is a bird.",
  ["(a) Reptilia + Reptilia", "(b) Aves + Aves", "(c) Amphibia + Osteichthyes ✗", "(d) Mammalia + Aves ✗",
   "(e) Cyclostomata + Cyclostomata"],
  R_AK("subphylum Vertebrata: classes"),
  why_others_wrong="B and D include (c); C includes (d); B and C also leave out a true pair.",
  seconds=60)
ms_check("abe", ["(a), (b) and (e) only", "(b), (c) and (e) only", "(a), (d) and (e) only",
                 "(a), (b), (c) and (e) only"], "A")

Z(AK, "Chordate classes", "Advanced", "assertion_reason",
  ar("Sharks such as Scoliodon have to swim constantly to avoid sinking, whereas bony fishes such as Labeo need not.",
     "Bony fishes have an air bladder that regulates buoyancy, while cartilaginous fishes do not have an air bladder."),
  ASSERTION_REASON, "A",
  "Air bladder and buoyancy in fishes",
  "NCERT: in Chondrichthyes the air bladder is absent, and due to this they have to swim constantly to avoid "
  "sinking. In Osteichthyes an air bladder is present which regulates buoyancy. The presence or absence of the air "
  "bladder is therefore the direct cause of the contrast stated in A.",
  ["A true", "R true", "Air bladder absent → must swim to stay afloat; present → buoyancy regulated"],
  R_AK("classes Chondrichthyes and Osteichthyes"),
  why_others_wrong="B is wrong because NCERT itself gives the absence of the air bladder as the reason for constant "
                   "swimming; C and D are wrong because both statements are true.",
  seconds=45)

Z(AK, "Non-chordate phyla", "Advanced", "match_list",
  ml(("animal", "feature"), ["Aurelia", "Ctenoplana", "Ascaris", "Pheretima"],
     ["Body cavity not lined by mesoderm (pseudocoelom)",
      "True coelom with metameric segmentation",
      "Umbrella-shaped, free-swimming medusa",
      "Eight external rows of ciliated comb plates"]),
  match_options(M("III", "IV", "I", "II"), [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"),
                                            M("IV", "III", "II", "I")], "D"), "D",
  "Distinguishing features of non-chordate phyla",
  "Aurelia (jelly fish) is the NCERT example of the umbrella-shaped, free-swimming medusa. Ctenoplana is a "
  "ctenophore, with eight external rows of ciliated comb plates. Ascaris is an aschelminth, a pseudocoelomate. "
  "Pheretima (earthworm) is an annelid: a coelomate showing metameric segmentation.",
  ["Aurelia → III", "Ctenoplana → IV", "Ascaris → I", "Pheretima → II"],
  R_AK("phyla Coelenterata, Ctenophora, Aschelminthes and Annelida"),
  why_others_wrong="A swaps the jelly fish and the comb jelly; B swaps the roundworm and the earthworm; C makes both "
                   "swaps.",
  seconds=50)

Z(AK, "Non-chordate phyla", "Advanced", "multi_statement",
  ms("An invertebrate has a chitinous exoskeleton, jointed appendages and Malpighian tubules for excretion. Which of "
     "the following would NCERT also lead you to expect in it?",
     ["Its body consists of head, thorax and abdomen.",
      "Statocysts or balance organs are present among its sensory organs.",
      "Nephridia help in its osmoregulation and excretion.",
      "It is mostly oviparous.",
      "Its circulatory system is of the closed type."]),
  ["(a), (b), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], "B",
  "Recognising an arthropod and its features",
  "A chitinous exoskeleton, jointed appendages and Malpighian tubules mark the animal as an arthropod. NCERT: the "
  "arthropod body consists of head, thorax and abdomen; sensory organs like antennae, eyes and statocysts (balance "
  "organs) are present; arthropods are mostly oviparous; their circulatory system is of the open type. Nephridia are "
  "the excretory organs of annelids, not arthropods.",
  ["Identify: Arthropoda", "(a) true", "(b) true", "(c) false – nephridia are annelidan", "(d) true",
   "(e) false – open circulation"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="A includes (c); C includes (e) and leaves out (a); D includes both false statements.",
  seconds=60)
ms_check("abd", ["(a), (b), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only",
                 "(a), (c) and (e) only"], "B")

Z(AK, "Basis of classification", "Advanced", "direct",
  "In which of the following pairs do the two animals show the same type of body symmetry as adults?",
  ["Spongilla and Ctenoplana", "Antedon and Aurelia", "Nereis and Echinus", "Taenia and Adamsia"], "B",
  "Symmetry as a basis of classification",
  "NCERT: sponges are mostly asymmetrical; coelenterates, ctenophores and adult echinoderms are radially symmetrical; "
  "annelids, platyhelminthes and arthropods are bilaterally symmetrical. Antedon (sea lily, an echinoderm) is radial "
  "as an adult, and Aurelia (a coelenterate) is radial too.",
  ["Antedon → adult echinoderm → radial", "Aurelia → coelenterate → radial"],
  R_AK("basis of classification: symmetry"),
  why_others_wrong="Spongilla is a sponge (mostly asymmetrical) while Ctenoplana is radial; Nereis is bilateral while "
                   "Echinus is radial as an adult; Taenia is bilateral while Adamsia is radial.",
  seconds=45)

# ================================================================ Structural Organisation in Animals (B4 I6 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "In the male frog, the vasa efferentia arise from the testes and enter the kidneys. According to NCERT, how many "
  "vasa efferentia are there?",
  ["2–4", "10–12", "25–30", "About 100"], "B",
  "Male reproductive system of the frog",
  "NCERT: vasa efferentia are 10–12 in number; they arise from the testes, enter the kidneys on their side and open "
  "into Bidder's canal, which finally communicates with the urinogenital duct opening into the cloaca.",
  ["Vasa efferentia → 10–12"],
  R_SOA("frog: reproductive system"),
  why_others_wrong="The other numbers are not given by NCERT for the vasa efferentia of the frog.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "direct",
  "In multicellular animals, a group of similar cells along with intercellular substances that performs a specific "
  "function is called a(n):",
  ["Tissue", "Organ", "Organ system", "Gland"], "A",
  "Levels of organisation in animals",
  "NCERT: a group of similar cells along with intercellular substances perform a specific function, and such an "
  "organisation is called a tissue. Tissues organised in a specific proportion and pattern form an organ, and organs "
  "with a common function form an organ system.",
  ["Similar cells + intercellular substance + one function → tissue"],
  R_SOA("animal tissues"),
  why_others_wrong="An organ is made of tissues arranged in a pattern; an organ system is a group of organs; a gland "
                   "is only one kind of specialised epithelial structure.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "Besides a closed blood vascular system, the frog has a lymphatic system. According to NCERT, the lymph of the frog "
  "differs from its blood in that lymph:",
  ["Lacks plasma", "Contains more RBCs than blood", "Lacks WBCs", "Lacks a few proteins and the RBCs"], "D",
  "Lymph of the frog",
  "NCERT: frogs have a well-developed closed type of circulatory system and also a lymphatic system. Lymph is "
  "different from blood: it lacks a few proteins and RBCs.",
  ["Lymph = blood minus a few proteins and the RBCs"],
  R_SOA("frog: circulatory system"),
  why_others_wrong="Lymph is a fluid with a plasma-like base, so it does not lack plasma; it lacks RBCs rather than "
                   "having more of them; NCERT does not say that it lacks WBCs.",
  seconds=25)

Z(SOA, "Frog: morphology and anatomy", "Basic", "statement_pair",
  sp("In the frog, bile emulsifies fat, and the pancreatic juices digest carbohydrates and proteins.",
     "In the frog, the final digestion of food takes place in the stomach."),
  STATEMENT_PAIR, "C",
  "Digestion in the frog",
  "NCERT: in the frog, food is digested in the stomach by HCl and gastric juices, and the partially digested food "
  "(chyme) passes to the duodenum. Bile emulsifies fat and pancreatic juices digest carbohydrates and proteins. Final "
  "digestion takes place in the intestine, not in the stomach.",
  ["Statement I → true", "Statement II → false (final digestion in the intestine)"],
  R_SOA("frog: digestive system"),
  why_others_wrong="A and D accept that final digestion is in the stomach; B rejects the NCERT roles of bile and "
                   "pancreatic juice.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("Frogs are cold-blooded (poikilotherm) animals, whose body temperature varies with the temperature of the "
     "environment.",
     "Frogs have the ability to change their colour to hide from their enemies."),
  ASSERTION_REASON, "B",
  "Poikilothermy and protective coloration in the frog",
  "NCERT states both: frogs are cold-blooded or poikilotherm animals, i.e. their body temperature varies with the "
  "temperature of the environment; and frogs have the ability to change colour to hide from their enemies "
  "(camouflage, a protective coloration called mimicry). Colour change is a defence against enemies; it is not why "
  "the body temperature follows the environment.",
  ["A true", "R true", "R is about protection from enemies, a different property → B"],
  R_SOA("frog: morphology"),
  why_others_wrong="A would make colour change the cause of poikilothermy, which NCERT does not say; C and D reject "
                   "statements that NCERT makes.",
  seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the neural system of the frog are correct?",
     ["It is organised into a central neural system, a peripheral neural system and an autonomic neural system.",
      "The peripheral neural system consists of the cranial nerves and the spinal nerves.",
      "The autonomic neural system consists of the sympathetic and the parasympathetic neural systems.",
      "The brain is enclosed in a cartilaginous brain box.",
      "The spinal cord is enclosed in the vertebral column."]),
  ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only", "(a), (b), (c) and (e) only"],
  "D",
  "Neural system of the frog",
  "NCERT: the frog's neural system is organised into a central neural system (brain and spinal cord), a peripheral "
  "neural system (cranial and spinal nerves) and an autonomic neural system (sympathetic and parasympathetic). The "
  "brain is enclosed in a bony structure called the brain box (cranium), and the spinal cord is enclosed in the "
  "vertebral column.",
  ["(a) true", "(b) true", "(c) true", "(d) false – bony cranium", "(e) true"],
  R_SOA("frog: neural system"),
  why_others_wrong="A and C include the false (d); B leaves out the true (a); A also leaves out (c) and (e).",
  seconds=50)
ms_check("abce", ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only",
                  "(a), (b), (c) and (e) only"], "D")

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("structure", "role"), ["Tight junctions", "Adhering junctions", "Gap junctions", "Fibroblasts"],
     ["Perform cementing to keep neighbouring cells together",
      "Produce and secrete fibres",
      "Help stop substances from leaking across a tissue",
      "Connect the cytoplasm of adjoining cells for rapid transfer of ions and small molecules"]),
  match_options(M("III", "I", "IV", "II"), [M("I", "III", "IV", "II"), M("III", "IV", "I", "II"),
                                            M("IV", "I", "III", "II")], "C"), "C",
  "Cell junctions and connective-tissue cells",
  "NCERT: tight junctions help to stop substances from leaking across a tissue; adhering junctions perform cementing "
  "to keep neighbouring cells together; gap junctions facilitate the cells to communicate by connecting the "
  "cytoplasm of adjoining cells, for rapid transfer of ions, small molecules and sometimes big molecules. Areolar "
  "tissue contains fibroblasts, the cells that produce and secrete fibres.",
  ["Tight → III", "Adhering → I", "Gap → IV", "Fibroblasts → II"],
  R_SOA("epithelial tissue: cell junctions; loose connective tissue"),
  why_others_wrong="A swaps tight and adhering junctions; B swaps adhering and gap junctions; D swaps tight and gap "
                   "junctions.",
  seconds=40)

Z(SOA, "Animal tissues", "Intermediate", "statement_pair",
  sp("Bones interact with the skeletal muscles attached to them to bring about movements.",
     "Bones support and protect the softer tissues and organs of the body."),
  STATEMENT_PAIR, "A",
  "Functions of bone",
  "NCERT: bones support and protect softer tissues and organs. Limb bones such as the long bones of the legs serve "
  "weight-bearing functions, and they also interact with the skeletal muscles attached to them to bring about "
  "movements. Both statements are true.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("connective tissue: specialised connective tissue (bone)"),
  why_others_wrong="Both statements are NCERT descriptions of bone, so B, C and D are wrong.",
  seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "statement_pair",
  sp("When two or more organs perform a common function by their physical and/or chemical interaction, they "
     "together form an organ system.",
     "In unicellular organisms, functions such as digestion, respiration and reproduction are performed by different "
     "tissues."),
  STATEMENT_PAIR, "C",
  "Organisation of the animal body",
  "NCERT: in unicellular organisms, all functions like digestion, respiration and reproduction are performed by a "
  "single cell; in multicellular animals the same functions are carried out by different groups of cells. When two "
  "or more organs perform a common function by their physical and/or chemical interaction, they together form an "
  "organ system, e.g. the digestive and respiratory systems.",
  ["Statement I → true", "Statement II → false (a single cell does everything; there are no tissues)"],
  R_SOA("introduction and animal tissues"),
  why_others_wrong="A and D accept that unicellular organisms have tissues; B rejects the NCERT definition of an "
                   "organ system.",
  seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "Which of the following is true of BOTH smooth muscle and cardiac muscle, as described in NCERT?",
  ["Both are closely attached to skeletal bones", "Both are involuntary",
   "Both are found in the walls of the stomach and intestine", "Both are the striated muscle of the biceps"], "B",
  "Comparing muscle tissues",
  "NCERT: smooth muscles are involuntary, as their functioning cannot be directly controlled; they occur in the walls "
  "of internal organs such as blood vessels, stomach and intestine. Cardiac muscle is a contractile tissue present "
  "only in the heart and is also involuntary. Skeletal muscle is closely attached to skeletal bones, as in the "
  "biceps.",
  ["Smooth → involuntary", "Cardiac → involuntary", "Common feature → involuntary"],
  R_SOA("muscle tissue"),
  why_others_wrong="Attachment to skeletal bones and the biceps describe skeletal muscle; cardiac muscle is present "
                   "only in the heart, not in the walls of the stomach and intestine.",
  seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "direct",
  "Suppose a dye injected into a testis of a male frog were carried along with the sperms. Which route would it "
  "follow to reach the outside?",
  ["Testis → vasa efferentia → Bidder's canal in the kidney → oviduct → cloaca",
   "Testis → urinogenital duct → vasa efferentia → kidney → cloaca",
   "Testis → separate vas deferens → cloacal aperture, bypassing the kidney",
   "Testis → vasa efferentia → Bidder's canal in the kidney → urinogenital duct → cloaca"], "D",
  "Route of sperms in the male frog",
  "NCERT: the vasa efferentia arise from the testes, enter the kidneys on their side and open into Bidder's canal. "
  "This finally communicates with the urinogenital duct that comes out of the kidneys and opens into the cloaca, a "
  "small median chamber used to pass faecal matter, urine and sperms to the exterior.",
  ["Testis", "Vasa efferentia", "Bidder's canal (in kidney)", "Urinogenital duct", "Cloaca"],
  R_SOA("frog: reproductive system"),
  why_others_wrong="A ends in an oviduct, which belongs to the female; B puts the urinogenital duct before the vasa "
                   "efferentia; C invents a separate vas deferens, whereas sperms pass through the kidney.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "direct",
  "A tissue has cells lying in spaces called lacunae, and a very hard, non-pliable ground substance rich in calcium "
  "salts and collagen fibres. In an adult human, at which of the following sites would this tissue be found?",
  ["Long bones of the legs", "Tip of the nose", "Tendons attaching muscles to bones", "Dermis of the skin"], "A",
  "Identifying bone and its location",
  "NCERT: bone has a very hard and non-pliable ground substance rich in calcium salts and collagen fibres, and the "
  "bone cells (osteocytes) lie in spaces called lacunae. Limb bones, such as the long bones of the legs, serve "
  "weight-bearing functions. The tip of the nose has cartilage (solid but pliable matrix), tendons are dense regular "
  "connective tissue, and the skin has dense irregular connective tissue.",
  ["Hard, calcified matrix + lacunae → bone", "Bone → long bones of the legs"],
  R_SOA("connective tissue: specialised connective tissue"),
  why_others_wrong="The tip of the nose is supported by cartilage, whose matrix is pliable; tendons and the skin have "
                   "collagen-rich dense connective tissue without calcium salts.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "direct",
  "Suppose that in a person's heart, the communication junctions (intercalated discs) at the fusion points between "
  "cardiac muscle cells failed to function, though the cells still stuck together. According to NCERT, which "
  "property would be lost?",
  ["The involuntary nature of the cardiac muscle", "The presence of cardiac muscle only in the heart",
   "The ability of the cells to contract as a unit", "The striations of skeletal muscle fibres"], "C",
  "Intercalated discs of cardiac muscle",
  "NCERT: cell junctions fuse the plasma membranes of cardiac muscle cells and make them stick together. "
  "Communication junctions (intercalated discs) at some fusion points allow the cells to contract as a unit, i.e. "
  "when one cell receives a signal to contract, its neighbours are also stimulated to contract.",
  ["Intercalated discs → signal passes to neighbouring cells", "Lost → cells cannot contract as a unit"],
  R_SOA("muscle tissue: cardiac muscle"),
  why_others_wrong="Being involuntary and being present only in the heart do not depend on the communication "
                   "junctions; skeletal muscle fibres are a different tissue altogether.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("NCERT classifies connective tissues as loose, dense and specialised. Which of the following are specialised "
     "connective tissues?",
     ["Cartilage", "Bone", "Blood", "Adipose tissue", "Tendon"]),
  ["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (c) only"], "D",
  "Types of connective tissue",
  "NCERT: connective tissues are loose (areolar and adipose tissue), dense (dense regular – tendons and ligaments; "
  "dense irregular – skin) and specialised (cartilage, bones and blood).",
  ["(a), (b), (c) → specialised", "(d) adipose → loose", "(e) tendon → dense regular"],
  R_SOA("connective tissue"),
  shortcut="Specialised connective tissues = cartilage, bone, blood.",
  why_others_wrong="A leaves out blood, a fluid specialised connective tissue; B adds adipose tissue, which is loose "
                   "connective tissue; C adds adipose tissue and tendon and leaves out cartilage and bone.",
  seconds=45)
ms_check("abc", ["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only",
                 "(a), (b) and (c) only"], "D")

# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

# Activation energy = energy of transition state - energy of substrate (hypothetical diagram values, kJ/mol).
S_E, TS_E, P_E = 40, 110, 15
EA_UNCAT = TS_E - S_E
assert EA_UNCAT == 70
assert TS_E - P_E == 95 and S_E - P_E == 25                                      # measured from P; S - P
S2_E, TS2_E, TSENZ_E, P2_E = 30, 105, 70, 10
EA2 = TS2_E - S2_E
EA2_ENZ = TSENZ_E - S2_E
assert (EA2, EA2_ENZ, EA2 - EA2_ENZ) == (75, 40, 35)
assert TSENZ_E - P2_E == 60 and (TS2_E - P2_E) - (TSENZ_E - P2_E) == 35            # new Ea measured from P

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "An enzyme shows its highest activity at pH 2. If the pH of its medium is raised to 7, keeping all other "
  "conditions the same, its activity is expected to:",
  ["Decline, because activity falls on either side of the optimum pH", "Rise, because a neutral pH suits all enzymes",
   "Remain unchanged, because pH affects only inorganic catalysts", "Rise first and then become constant at Vmax"],
  "A",
  "Optimum pH of enzymes",
  "NCERT: each enzyme shows its highest activity at a particular pH, its optimum pH, and activity declines both below "
  "and above the optimum value. Moving from pH 2 to pH 7 takes the enzyme away from its optimum, so its activity "
  "falls.",
  ["Optimum pH = 2", "pH 7 ≠ optimum → activity declines"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="Enzymes do not share one optimum pH; pH does affect enzymes (changes can alter their tertiary "
                   "structure); Vmax describes the effect of substrate concentration, not of pH.",
  seconds=25)

Z(BIO, "Carbohydrates and lipids", "Basic", "direct",
  "Glucose and ribose, two sugars found in the acid-soluble pool of living tissues, are respectively a:",
  ["Pentose and hexose", "Hexose and hexose", "Hexose and pentose", "Pentose and pentose"], "C",
  "Monosaccharides in living tissue",
  "Glucose is a six-carbon sugar (hexose); ribose is a five-carbon sugar (pentose). NCERT shows both among the sugars "
  "of the acid-soluble pool, and states that the sugar in polynucleotides is either ribose or 2′-deoxyribose.",
  ["Glucose → C₆ → hexose", "Ribose → C₅ → pentose"],
  R_BIO("how to analyse chemical composition (sugars); nucleic acids"),
  why_others_wrong="A reverses the two; B and D give both sugars the same number of carbons.",
  seconds=20)

Z(BIO, "Carbohydrates and lipids", "Basic", "direct",
  "A lipid from a cell membrane yields, on hydrolysis, glycerol, fatty acids, phosphoric acid and a phosphorylated "
  "organic compound. According to NCERT, it is a:",
  ["Triglyceride, such as gingelly oil", "Phospholipid, such as lecithin", "Saturated fatty acid, such as palmitic acid",
   "Homopolymer, such as cellulose"], "B",
  "Phospholipids",
  "NCERT: some lipids have phosphorous and a phosphorylated organic compound in them; these are phospholipids, found "
  "in the cell membrane. Lecithin is one example.",
  ["Phosphorus + phosphorylated organic compound + membrane → phospholipid"],
  R_BIO("lipids"),
  why_others_wrong="A triglyceride is glycerol esterified with three fatty acids, with no phosphorus; palmitic acid "
                   "is a single fatty acid; cellulose is a polysaccharide of glucose, not a lipid.",
  seconds=25)

Z(BIO, "Enzyme classification", "Basic", "direct",
  "An enzyme breaks the glycosidic bonds of starch by adding water, releasing glucose. In the NCERT classification of "
  "enzymes, it belongs to the class:",
  ["Lyases", "Ligases", "Isomerases", "Hydrolases"], "D",
  "Classes of enzymes",
  "NCERT: hydrolases are enzymes catalysing the hydrolysis of ester, ether, peptide, glycosidic, C–C, C–halide or "
  "P–N bonds. Breaking glycosidic bonds of starch with water is hydrolysis.",
  ["Glycosidic bond + water → hydrolysis → hydrolase"],
  R_BIO("classification and nomenclature of enzymes"),
  why_others_wrong="Lyases remove groups by mechanisms other than hydrolysis, leaving double bonds; ligases link two "
                   "compounds together; isomerases inter-convert isomers.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "Which of the following proteins would NOT show a quaternary structure?",
  ["A protein made of a single polypeptide chain", "Adult human haemoglobin",
   "A protein assembled from four separately folded subunits", "A protein made of two α and two β subunits"], "A",
  "Quaternary structure of proteins",
  "NCERT: some proteins are an assembly of more than one polypeptide or subunit, and the manner in which these "
  "individually folded polypeptides are arranged with respect to each other is the quaternary structure. A protein of "
  "a single polypeptide chain has no subunits to arrange.",
  ["Quaternary structure needs two or more subunits", "Single chain → none"],
  R_BIO("structure of proteins"),
  why_others_wrong="Haemoglobin (two α and two β subunits) and any four-subunit protein are assemblies of polypeptides, "
                   "so they show a quaternary structure.",
  seconds=25)

Z(BIO, "Proteins and amino acids", "Intermediate", "multi_statement",
  ms("A purified protein loses its biological activity after mild heating, although none of its peptide bonds is "
     "broken. Which of the following statements are correct?",
     ["Its primary structure is unchanged.",
      "Its three-dimensional (tertiary) structure has been altered.",
      "Heat can denature proteins.",
      "The sequence of its amino acids has changed.",
      "Mild heating hydrolyses the peptide bonds of every protein."]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(c), (d) and (e) only"], "C",
  "Levels of protein structure and denaturation",
  "The primary structure is the sequence of amino acids joined by peptide bonds; since no peptide bond is broken, it is "
  "intact. NCERT: the tertiary structure is absolutely necessary for many biological activities of proteins, and high "
  "temperature destroys enzymatic activity because proteins are denatured by heat. Loss of activity with intact "
  "peptide bonds means the three-dimensional folding has changed.",
  ["(a) true", "(b) true", "(c) true", "(d) false – bonds intact, sequence intact",
   "(e) false – contradicts the stem"],
  R_BIO("structure of proteins; factors affecting enzyme activity"),
  why_others_wrong="A leaves out (c); B and D include (d), which cannot be true when no peptide bond is broken; D "
                   "also includes (e).",
  seconds=50)
ms_check("abc", ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(c), (d) and (e) only"], "C")

Z(BIO, "Enzymes: properties and action", "Intermediate", "numerical",
  "In a potential-energy diagram of an uncatalysed reaction S → P, the substrate S is at 40 kJ mol⁻¹, the "
  "transition state at 110 kJ mol⁻¹ and the product P at 15 kJ mol⁻¹ (hypothetical values). Using the NCERT "
  "definition, the activation energy of this reaction is:",
  ["95 kJ mol⁻¹", "70 kJ mol⁻¹", "25 kJ mol⁻¹", "110 kJ mol⁻¹"], "B",
  "Activation energy",
  "NCERT: the difference in average energy content of S from that of the transition state is called the activation "
  "energy. Here it is 110 − 40 = 70 kJ mol⁻¹. (P lies below S, so the reaction is exothermic, but S must still pass "
  "through the higher-energy transition state.)",
  ["Ea = E(transition state) − E(S)", "= 110 − 40 = 70 kJ mol⁻¹"],
  R_BIO("enzymes: how do enzymes bring about such high rates of chemical conversions?"),
  why_others_wrong="95 measures from the product instead of the substrate; 25 is the energy difference between S and "
                   "P; 110 is the energy of the transition state itself, not a difference.",
  seconds=45, verified_by=RECOMPUTED)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("An endothermic reaction is an energy-requiring reaction.",
     "In an endothermic reaction, the product is at a lower energy level than the substrate."),
  STATEMENT_PAIR, "C",
  "Exothermic and endothermic reactions",
  "NCERT contrasts the exothermic (spontaneous) reaction with the endothermic, energy-requiring reaction. If the "
  "product P is at a lower level than the substrate S, the reaction is exothermic and energy need not be supplied to "
  "form the product. So a product below the substrate describes an exothermic, not an endothermic, reaction.",
  ["Statement I → true", "Statement II → false (that describes an exothermic reaction)"],
  R_BIO("enzymes: how do enzymes bring about such high rates of chemical conversions?"),
  why_others_wrong="A and D accept Statement II, which describes an exothermic reaction; B rejects NCERT's "
                   "description of an endothermic reaction.",
  seconds=35)

Z(BIO, "Enzymes: properties and action", "Intermediate", "assertion_reason",
  ar("A human enzyme stored at 4 °C for a day can catalyse its reaction again when it is brought back to 37 °C.",
     "Low temperature preserves an enzyme in a temporarily inactive state."),
  ASSERTION_REASON, "A",
  "Effect of low temperature on enzymes",
  "NCERT: low temperature preserves the enzyme in a temporarily inactive state, whereas high temperature destroys "
  "enzymatic activity because proteins are denatured by heat. Because the cold only inactivates the enzyme "
  "temporarily, warming it back to its working temperature restores its activity.",
  ["A true", "R true", "Inactivation is temporary → activity returns → R explains A"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="B is wrong because the temporary nature of cold inactivation is exactly why activity returns; C "
                   "and D are wrong because both statements are true.",
  seconds=40)

Z(BIO, "Nucleic acids", "Intermediate", "match_list",
  ml(("compound", "category"), ["Thymine", "Guanine", "Adenosine", "Cytidylic acid"],
     ["Nucleotide", "Nucleoside", "Substituted purine", "Substituted pyrimidine"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("III", "IV", "I", "II")], "D"), "D",
  "Building blocks of nucleic acids",
  "NCERT: adenine and guanine are substituted purines, while uracil, cytosine and thymine are substituted "
  "pyrimidines. A nitrogen base attached to a sugar is a nucleoside (adenosine, guanosine, thymidine, uridine, "
  "cytidine); when a phosphate group is also esterified to the sugar, it is a nucleotide (adenylic, thymidylic, "
  "guanylic, uridylic and cytidylic acids).",
  ["Thymine → pyrimidine (IV)", "Guanine → purine (III)", "Adenosine → nucleoside (II)",
   "Cytidylic acid → nucleotide (I)"],
  R_BIO("nucleic acids"),
  why_others_wrong="A swaps the purine and the pyrimidine; B swaps the nucleoside and the nucleotide; C makes both "
                   "swaps.",
  seconds=40)

Z(BIO, "Nucleic acids", "Intermediate", "direct",
  "A compound from the acid-insoluble fraction of a tissue yields, on complete hydrolysis, a pentose sugar, "
  "phosphoric acid and heterocyclic nitrogenous bases. The compound is most likely a:",
  ["Phospholipid", "Nucleic acid", "Nucleoside", "Protein"], "B",
  "Identifying a nucleic acid",
  "NCERT: nucleic acids are polynucleotides, found in the acid-insoluble fraction. Each nucleotide has three "
  "chemically distinct components: a heterocyclic compound (nitrogenous base), a monosaccharide (ribose or "
  "2′-deoxyribose, both pentoses) and a phosphoric acid or phosphate.",
  ["Base + pentose + phosphate → nucleotides", "Acid-insoluble polymer of nucleotides → nucleic acid"],
  R_BIO("nucleic acids"),
  why_others_wrong="A phospholipid yields glycerol and fatty acids, not heterocyclic bases and a pentose; a nucleoside "
                   "has no phosphate and is a small acid-soluble molecule; a protein yields amino acids.",
  seconds=35)

Z(BIO, "Enzyme classification", "Intermediate", "assertion_reason",
  ar("An enzyme that moves a hydrogen atom from a substrate S to another substrate S′ is not placed in the class "
     "Transferases.",
     "In NCERT's classification, transferases catalyse the transfer of a group G, other than hydrogen, between a pair "
     "of substrates S and S′."),
  ASSERTION_REASON, "A",
  "Transferases versus oxidoreductases",
  "NCERT defines transferases as enzymes catalysing the transfer of a group G (other than hydrogen) between a pair of "
  "substrates S and S′. Transfer of hydrogen between S and S′ is an oxido-reduction, catalysed by oxidoreductases "
  "(dehydrogenases). The exclusion of hydrogen in the definition is exactly why such an enzyme is not a transferase.",
  ["A true", "R true", "Hydrogen is excluded from 'group G' → R explains A"],
  R_BIO("classification and nomenclature of enzymes"),
  why_others_wrong="B is wrong because the definition in R is what excludes the enzyme; C and D are wrong because both "
                   "statements are true.",
  seconds=40)

Z(BIO, "Enzymes: properties and action", "Advanced", "numerical",
  "For a reaction S → P (hypothetical values), the substrate lies at 30 kJ mol⁻¹ and the product at 10 kJ mol⁻¹. "
  "Without an enzyme the transition state lies at 105 kJ mol⁻¹; with the enzyme it lies at 70 kJ mol⁻¹. What is "
  "the activation energy with the enzyme, and by how much has the enzyme lowered it?",
  ["Ea = 60 kJ mol⁻¹; lowered by 35 kJ mol⁻¹", "Ea = 70 kJ mol⁻¹; lowered by 35 kJ mol⁻¹",
   "Ea = 40 kJ mol⁻¹; lowered by 75 kJ mol⁻¹", "Ea = 40 kJ mol⁻¹; lowered by 35 kJ mol⁻¹"], "D",
  "Enzymes lower the activation energy",
  "NCERT: activation energy is the difference in energy between the substrate S and the transition state; an enzyme "
  "brings down this energy barrier, making the transition of S into P easier. Without the enzyme, Ea = 105 − 30 = 75 "
  "kJ mol⁻¹; with it, Ea = 70 − 30 = 40 kJ mol⁻¹. The lowering is 75 − 40 = 35 kJ mol⁻¹. The energies of S and P are "
  "not changed by the enzyme.",
  ["Ea (no enzyme) = 105 − 30 = 75", "Ea (enzyme) = 70 − 30 = 40", "Lowering = 75 − 40 = 35 kJ mol⁻¹"],
  R_BIO("enzymes: how do enzymes bring about such high rates of chemical conversions?"),
  shortcut="Lowering = difference between the two transition-state energies = 105 − 70 = 35.",
  why_others_wrong="A measures the new Ea from the product (70 − 10); B takes the transition-state energy itself as "
                   "Ea; C gives the uncatalysed Ea (75) as the lowering.",
  seconds=75, verified_by=RECOMPUTED)

Z(BIO, "Enzyme classification", "Advanced", "multi_statement",
  ms("An enzyme catalyses the reaction S reduced + S′ oxidised → S oxidised + S′ reduced, and it is catalytically "
     "active only when the co-enzyme NAD is present. Which of the following statements are correct?",
     ["The enzyme is an oxidoreductase (dehydrogenase).",
      "The co-enzyme NAD contains the vitamin niacin.",
      "NAD is the protein part (apoenzyme) of this enzyme.",
      "If NAD is removed, the enzyme loses its catalytic activity.",
      "The enzyme is a transferase, because a group moves from S to S′."]),
  ["(a), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"], "B",
  "Oxidoreductases and co-enzymes",
  "NCERT: oxidoreductases/dehydrogenases catalyse oxido-reduction between two substrates, S reduced + S′ oxidised → "
  "S oxidised + S′ reduced. Co-factors are non-protein constituents; the protein portion is the apoenzyme. The "
  "essential chemical components of many co-enzymes are vitamins – NAD and NADP contain niacin. When the co-factor is "
  "removed, the catalytic activity of the enzyme is lost. Transferases move a group other than hydrogen, so this "
  "redox enzyme is not a transferase.",
  ["(a) true", "(b) true", "(c) false – co-enzymes are non-protein; apoenzyme is the protein",
   "(d) true", "(e) false – redox transfer of hydrogen is not a transferase reaction"],
  R_BIO("classification and nomenclature of enzymes; co-factors"),
  why_others_wrong="A and D include (c); C includes (e) and leaves out (a).",
  seconds=60)
ms_check("abd", ["(a), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only",
                 "(a), (b), (c) and (d) only"], "B")

Z(BIO, "Carbohydrates and lipids", "Advanced", "multi_statement",
  ms("On complete hydrolysis, compound X gives only glucose and has a branched chain; compound Y gives only fructose; "
     "compound Z gives one glycerol and three fatty acid molecules. Which of the following statements are correct?",
     ["X could be glycogen.",
      "Y could be inulin.",
      "Z is a triglyceride.",
      "X is a heteropolymer.",
      "Z is a macromolecule of molecular weight above ten thousand daltons."]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (e) only"], "C",
  "Identifying polysaccharides and lipids",
  "Glycogen, the animal store of energy, is a branched polymer of glucose, i.e. a homopolymer. NCERT: inulin is a "
  "polymer of fructose. Glycerol esterified with three fatty acids is a triglyceride. Lipids have molecular weights "
  "not exceeding 800 Da and are not strictly macromolecules.",
  ["(a) true", "(b) true", "(c) true", "(d) false – one kind of monomer → homopolymer",
   "(e) false – lipids are below 800 Da"],
  R_BIO("polysaccharides; lipids"),
  why_others_wrong="A leaves out (c); B includes (d); D includes (e) and leaves out (b).",
  seconds=60)
ms_check("abc", ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (e) only"], "C")

Z(BIO, "Proteins and amino acids", "Advanced", "direct",
  "Two proteins contain exactly the same numbers of each kind of amino acid, yet they have different shapes and "
  "functions. In which feature must they differ at the most basic level?",
  ["The kinds of amino acids present in them", "The total number of amino acids in each",
   "The type of bond joining adjacent amino acids, peptide in one and glycosidic in the other",
   "The sequence of amino acids, i.e. their primary structure"], "D",
  "Primary structure determines the protein",
  "NCERT: proteins are linear chains of amino acids linked by peptide bonds, and the sequence of amino acids – the "
  "positional information of which amino acid is first, second and so on – is the primary structure. With the same "
  "composition, only the order can differ, and the higher levels of folding follow from the chain.",
  ["Same kinds and numbers → composition identical", "Remaining variable → order (primary structure)"],
  R_BIO("proteins; structure of proteins"),
  why_others_wrong="A and B are ruled out by the stem (same kinds and numbers); every protein's amino acids are "
                   "joined by peptide bonds, so C is wrong.",
  seconds=45)

Z(BIO, "Nucleic acids", "Advanced", "direct",
  "A tissue containing nucleotides, nucleosides, free amino acids, DNA and proteins is ground in trichloroacetic acid "
  "and strained through cheesecloth. Which set will be found in the filtrate (acid-soluble pool)?",
  ["Nucleotides, nucleosides and free amino acids", "DNA and proteins only",
   "Nucleotides, nucleosides and DNA", "Free amino acids and proteins"], "A",
  "Acid-soluble and acid-insoluble fractions",
  "NCERT: grinding a tissue in trichloroacetic acid and straining it gives an acid-soluble filtrate containing "
  "micromolecules (molecular weights below one thousand daltons) such as amino acids, sugars, nucleosides and "
  "nucleotides, and an acid-insoluble retentate containing macromolecules such as proteins, polysaccharides and "
  "nucleic acids.",
  ["Small molecules → filtrate: nucleotides, nucleosides, amino acids", "Polymers → retentate: DNA, proteins"],
  R_BIO("how to analyse chemical composition"),
  why_others_wrong="DNA and proteins are macromolecules of the acid-insoluble retentate, so B, C and D each place a "
                   "macromolecule in the filtrate or leave the small molecules out.",
  seconds=45)

# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

# Breathing: TLC = VC + RV.
VC6, RV6, TV6 = 4200, 1100, 500
TLC6 = VC6 + RV6
assert TLC6 == 5300
assert VC6 - RV6 == 3100 and VC6 + RV6 + TV6 == 5800                              # subtracted; TV added again
# Breathing: air in the lungs at the end of a normal inspiration = RV + ERV + TV (= FRC + TV).
RV7, ERV7, TV7, IRV7 = 1200, 1000, 500, 2500
END_INSP = RV7 + ERV7 + TV7
assert END_INSP == 2700
assert TV7 + ERV7 == 1500 and RV7 + ERV7 == 2200 and RV7 + ERV7 + TV7 + IRV7 == 5200  # forgot RV; FRC; TLC
# Partial-pressure gradients at the tissues (NCERT table, mm Hg).
assert 95 - 40 == 55 and 45 - 40 == 5

Z(BRE, "Regulation and disorders", "Basic", "direct",
  "A worker who spent many years in a stone-breaking unit without any protection develops serious lung damage. "
  "According to NCERT, what is the most likely cause, and how could it have been prevented?",
  ["Allergic inflammation of the bronchi and bronchioles; by avoiding pollen",
   "Inflammation due to long exposure to dust, leading to fibrosis; by wearing a protective mask",
   "Damage to the alveolar walls by cigarette smoke; by quitting smoking",
   "Failure of the respiratory rhythm centre; by keeping the body cool"], "B",
  "Occupational respiratory disorders",
  "NCERT: in industries involving grinding or stone-breaking, so much dust is produced that the defence mechanism of "
  "the body cannot fully cope. Long exposure can give rise to inflammation leading to fibrosis (proliferation of "
  "fibrous tissues) and thus serious lung damage. Workers in such industries should wear protective masks.",
  ["Dust exposure → inflammation → fibrosis", "Prevention → protective masks"],
  R_BRE("disorders of respiratory system"),
  why_others_wrong="A describes asthma; C describes emphysema, whose major cause NCERT gives as cigarette smoking; D "
                   "is not an occupational disorder at all.",
  seconds=30)

Z(BRE, "Respiratory volumes", "Basic", "numerical",
  "Spirometry of a healthy man gives a vital capacity of 4200 mL, a residual volume of 1100 mL and a tidal volume of "
  "500 mL. What is his total lung capacity?",
  ["3100 mL", "4200 mL", "5300 mL", "5800 mL"], "C",
  "Total lung capacity",
  "NCERT: total lung capacity is the total volume of air accommodated in the lungs at the end of a forced "
  "inspiration; it equals RV + ERV + TV + IRV, i.e. vital capacity + residual volume. TLC = 4200 + 1100 = 5300 mL. "
  "The tidal volume is already part of the vital capacity.",
  ["TLC = VC + RV", "= 4200 + 1100 = 5300 mL"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="3100 mL subtracts RV instead of adding it; 4200 mL leaves out the residual volume; 5800 mL adds the "
                   "tidal volume again although it is already included in the vital capacity.",
  seconds=40, verified_by=RECOMPUTED)

Z(BRE, "Respiratory system", "Basic", "direct",
  "Which of the following belongs to the respiratory or exchange part of the human respiratory system rather than to "
  "the conducting part?",
  ["Alveolar ducts", "Terminal bronchioles", "Tertiary bronchi", "Larynx"], "A",
  "Conducting and exchange parts",
  "NCERT: the part starting with the external nostrils up to the terminal bronchioles constitutes the conducting "
  "part, whereas the alveoli and their ducts form the respiratory or exchange part, the site of actual diffusion of "
  "O₂ and CO₂ between blood and atmospheric air.",
  ["Conducting → nostrils … terminal bronchioles", "Exchange → alveoli and their ducts"],
  R_BRE("human respiratory system"),
  why_others_wrong="The terminal bronchioles mark the end of the conducting part, and the tertiary bronchi and the "
                   "larynx lie within it.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Basic", "statement_pair",
  sp("At the tissues, where pO₂ is low, oxygen dissociates from oxyhaemoglobin.",
     "Under normal physiological conditions, every 100 mL of oxygenated blood delivers about 4 mL of O₂ to the "
     "tissues."),
  STATEMENT_PAIR, "C",
  "Oxygen delivery to tissues",
  "NCERT: in the tissues, where low pO₂, high pCO₂, high H⁺ concentration and higher temperature exist, conditions "
  "favour dissociation of oxygen from oxyhaemoglobin. Every 100 mL of oxygenated blood delivers about 5 mL of O₂ to "
  "the tissues; the figure of about 4 mL is for CO₂ delivered to the alveoli by 100 mL of deoxygenated blood.",
  ["Statement I → true", "Statement II → false (5 mL O₂; 4 mL is the CO₂ figure)"],
  R_BRE("transport of oxygen"),
  why_others_wrong="A and D accept the CO₂ figure for O₂; B rejects the NCERT condition for dissociation of "
                   "oxyhaemoglobin.",
  seconds=30)

Z(BRE, "Respiratory volumes", "Intermediate", "numerical",
  "A person has a residual volume of 1200 mL, an expiratory reserve volume of 1000 mL, a tidal volume of 500 mL and "
  "an inspiratory reserve volume of 2500 mL. What volume of air is present in his lungs at the end of a normal (quiet) "
  "inspiration?",
  ["1500 mL", "2200 mL", "5200 mL", "2700 mL"], "D",
  "Lung volumes during quiet breathing",
  "After a normal expiration the lungs still hold the functional residual capacity, FRC = ERV + RV = 1000 + 1200 = "
  "2200 mL. A normal inspiration adds the tidal volume of 500 mL, so the lungs then hold 2200 + 500 = 2700 mL. The "
  "IRV is not inspired in quiet breathing.",
  ["FRC = ERV + RV = 2200 mL", "End of normal inspiration = FRC + TV = 2700 mL"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="1500 mL (TV + ERV) leaves out the residual volume; 2200 mL is the FRC, the volume at the end of a "
                   "normal expiration; 5200 mL is the total lung capacity, reached only after a forced inspiration.",
  seconds=60, verified_by=RECOMPUTED)

Z(BRE, "Mechanism of breathing", "Intermediate", "direct",
  "If a person's diaphragm were paralysed but the external inter-costal muscles worked normally, inspiration could "
  "still enlarge the thoracic chamber in which axis?",
  ["Antero-posterior axis, by flattening of the diaphragm", "Dorso-ventral axis, by lifting of the ribs and sternum",
   "Antero-posterior axis, by contraction of the abdominal muscles", "No axis, because only the diaphragm can "
   "change thoracic volume"], "B",
  "Roles of the diaphragm and inter-costal muscles",
  "NCERT: contraction of the diaphragm increases the volume of the thoracic chamber in the antero-posterior axis, "
  "while contraction of the external inter-costal muscles lifts up the ribs and the sternum, increasing the volume in "
  "the dorso-ventral axis. With the diaphragm paralysed, only the dorso-ventral enlargement remains.",
  ["Diaphragm → antero-posterior (lost)", "External inter-costals → dorso-ventral (retained)"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A needs the paralysed diaphragm; abdominal muscles are not what enlarges the chamber in the "
                   "antero-posterior axis; D ignores the inter-costal muscles.",
  seconds=40)

Z(BRE, "Regulation and disorders", "Intermediate", "direct",
  "A person breathes rapidly and deeply for a minute, so that the CO₂ and H⁺ levels in his blood fall. Which effect "
  "on the regulation of breathing is expected?",
  ["The chemosensitive area next to the rhythm centre is less stimulated, so the drive to breathe decreases",
   "The chemosensitive area is more strongly stimulated, because O₂ has increased",
   "The pneumotaxic centre in the medulla takes over the rhythm completely",
   "Oxygen receptors become the main regulators, because O₂ plays the major role in respiratory rhythm"], "A",
  "Chemical regulation of breathing",
  "NCERT: a chemosensitive area adjacent to the rhythm centre is highly sensitive to CO₂ and H⁺; an increase in these "
  "activates it, and it signals the rhythm centre to make adjustments so that they are eliminated. The role of "
  "oxygen in regulating respiratory rhythm is quite insignificant. Lower CO₂ and H⁺ therefore mean less stimulation "
  "of this area and a weaker drive to breathe.",
  ["CO₂ and H⁺ ↓", "Chemosensitive area less active", "Rhythm centre less driven"],
  R_BRE("regulation of respiration"),
  why_others_wrong="B links the chemosensitive area to O₂, to which NCERT says it is not the main sensitivity; the "
                   "pneumotaxic centre is in the pons, not the medulla; NCERT calls the role of O₂ quite "
                   "insignificant.",
  seconds=45)

Z(BRE, "Respiratory volumes", "Intermediate", "match_list",
  ml(("capacity", "made up of"), ["Inspiratory capacity", "Expiratory capacity", "Functional residual capacity",
                                  "Vital capacity"],
     ["ERV + RV", "TV + IRV", "ERV + TV + IRV", "TV + ERV"]),
  match_options(M("II", "IV", "I", "III"), [M("IV", "II", "I", "III"), M("II", "IV", "III", "I"),
                                            M("II", "I", "IV", "III")], "B"), "B",
  "Respiratory capacities",
  "NCERT: inspiratory capacity = TV + IRV; expiratory capacity = TV + ERV; functional residual capacity = ERV + RV; "
  "vital capacity = ERV + TV + IRV, the maximum volume that can be breathed in after a forced expiration.",
  ["IC → II", "EC → IV", "FRC → I", "VC → III"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="A swaps the inspiratory and expiratory capacities; C swaps FRC and vital capacity; D gives the "
                   "expiratory capacity the FRC sum.",
  seconds=45)

Z(BRE, "Mechanism of breathing", "Intermediate", "assertion_reason",
  ar("During normal expiration, the intra-pulmonary pressure falls below the atmospheric pressure.",
     "Relaxation of the diaphragm and the inter-costal muscles reduces the thoracic volume and thereby the pulmonary "
     "volume."),
  ASSERTION_REASON, "D",
  "Pressure changes during expiration",
  "NCERT: relaxation of the diaphragm and the inter-costal muscles returns the diaphragm and sternum to their normal "
  "positions and reduces the thoracic volume and thereby the pulmonary volume. This raises the intra-pulmonary "
  "pressure slightly above the atmospheric pressure, causing expulsion of air. So the Assertion is false and the "
  "Reason true.",
  ["A false – pressure rises above atmospheric", "R true"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and B accept the false Assertion; C rejects the Reason, which is NCERT's account of expiration.",
  seconds=40)

Z(BRE, "Mechanism of breathing", "Advanced", "direct",
  "A stab wound makes an opening through the chest wall into the thoracic chamber on one side. Although the "
  "inspiratory muscles of that side contract normally, the lung of that side fails to fill with air. Which is the "
  "best explanation?",
  ["The diaphragm cannot contract once the chest wall is opened",
   "Oxygen can no longer diffuse across the alveolar membrane",
   "The chamber is no longer air-tight, so the enlarging thoracic volume no longer lowers the intra-pulmonary "
   "pressure below atmospheric pressure",
   "The trachea is blocked by the pleural fluid that leaks out"], "C",
  "Air-tight thoracic chamber",
  "NCERT: the thoracic chamber is anatomically air-tight, so any change in its volume is reflected in the lung "
  "(pulmonary) cavity; we cannot directly alter the pulmonary volume. Inspiration occurs only when the "
  "intra-pulmonary pressure falls below atmospheric pressure. Once the chamber is open, enlarging it no longer "
  "expands the lung, so no negative pressure develops in the lung and air does not flow in.",
  ["Air-tight chamber → thoracic volume change transmitted to lung", "Opened → not transmitted",
   "No negative intra-pulmonary pressure → no inflow"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="The stem says the inspiratory muscles still contract; diffusion across the alveoli is not the "
                   "first step that fails; pleural fluid lies between the pleural membranes, not in the trachea.",
  seconds=60)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "If the carbonic anhydrase of a person's RBCs were completely inhibited, which process would be most directly "
  "impaired?",
  ["Conversion of CO₂ into bicarbonate at the tissues, and release of CO₂ from bicarbonate at the alveoli",
   "Binding of O₂ with haemoglobin to form oxyhaemoglobin in the alveoli",
   "Transport of the small fraction of CO₂ dissolved in plasma",
   "Diffusion of O₂ from the oxygenated blood into the tissues"], "A",
  "Role of carbonic anhydrase in CO₂ transport",
  "NCERT: RBCs contain a very high concentration of carbonic anhydrase, which facilitates CO₂ + H₂O ⇌ H₂CO₃ ⇌ "
  "HCO₃⁻ + H⁺ in both directions. At the tissues, where pCO₂ is high, CO₂ forms HCO₃⁻ and H⁺; at the alveoli, where "
  "pCO₂ is low, the reaction runs the other way and releases CO₂. About 70 per cent of CO₂ is carried as "
  "bicarbonate, so this route is the one most affected.",
  ["Carbonic anhydrase → CO₂ ⇌ HCO₃⁻ in RBCs", "Inhibited → bicarbonate route (~70 % of CO₂) impaired"],
  R_BRE("transport of carbon dioxide"),
  why_others_wrong="O₂ binding and O₂ diffusion depend mainly on pO₂, not on carbonic anhydrase; dissolved CO₂ (about "
                   "7 per cent) does not need the enzyme.",
  seconds=50)

Z(BRE, "Regulation and disorders", "Advanced", "multi_statement",
  ms("A person rebreathes air from a closed bag, so that the CO₂ and H⁺ concentration of his blood rise. Which of the "
     "following statements are correct?",
     ["The chemosensitive area adjacent to the respiratory rhythm centre is activated.",
      "This area signals the rhythm centre to make adjustments by which CO₂ and H⁺ can be eliminated.",
      "Receptors associated with the aortic arch and carotid artery can also recognise these changes and send "
      "signals to the rhythm centre.",
      "The falling O₂ level is the main factor that adjusts his breathing.",
      "The pneumotaxic centre, which moderates the rhythm centre, is located in the medulla."]),
  ["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (c) only"], "D",
  "Chemical regulation of breathing",
  "NCERT: the respiratory rhythm centre is in the medulla; the pneumotaxic centre, in the pons, can moderate it. A "
  "chemosensitive area adjacent to the rhythm centre is highly sensitive to CO₂ and H⁺, and an increase in these "
  "activates it; it then signals the rhythm centre to make adjustments by which these substances are eliminated. "
  "Receptors associated with the aortic arch and carotid artery can also recognise changes in CO₂ and H⁺ and signal "
  "the rhythm centre. The role of oxygen in the regulation of respiratory rhythm is quite insignificant.",
  ["(a) true", "(b) true", "(c) true", "(d) false – O₂ role insignificant", "(e) false – pons"],
  R_BRE("regulation of respiration"),
  why_others_wrong="A leaves out (c); B includes (d); C includes (d) and (e) and leaves out (a) and (b).",
  seconds=60)
ms_check("abc", ["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only",
                 "(a), (b) and (c) only"], "D")

Z(BRE, "Exchange and transport of gases", "Advanced", "statement_pair",
  sp("Using the NCERT partial pressures, the pO₂ gradient from oxygenated blood to the tissues (about 55 mm Hg) is "
     "much larger than the pCO₂ gradient from the tissues to the oxygenated blood (about 5 mm Hg).",
     "At the tissues, O₂ diffuses from the tissue cells into the blood."),
  STATEMENT_PAIR, "C",
  "Partial-pressure gradients at the tissues",
  "NCERT values: oxygenated blood pO₂ 95, pCO₂ 40 mm Hg; tissues pO₂ 40, pCO₂ 45 mm Hg. The O₂ gradient is 95 − 40 = "
  "55 mm Hg (blood → tissues) and the CO₂ gradient is 45 − 40 = 5 mm Hg (tissues → blood). O₂ therefore diffuses "
  "from the blood into the tissues, not the reverse.",
  ["O₂: 95 − 40 = 55 mm Hg", "CO₂: 45 − 40 = 5 mm Hg", "Statement I → true",
   "Statement II → false (O₂ moves blood → tissues)"],
  R_BRE("exchange of gases"),
  why_others_wrong="A and D accept the reversed direction of O₂ diffusion; B rejects a correct calculation from NCERT "
                   "values.",
  seconds=50)

# ================================================================ Body Fluids and Circulation (B5 I6 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

# Cardiac output from the R–R (QRS-to-QRS) interval: HR = 60 / 0.75 s = 80 per minute; CO = 80 x 70 mL.
RR = F(3, 4)
HR8 = F(60) / RR
CO8 = HR8 * 70
assert (HR8, CO8) == (80, 5600)
assert 72 * 70 == 5040 and 60 * 70 == 4200 and RR * 70 * 60 == F(3150)             # NCERT 72; 1 per s; multiplied

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "A blood report shows a platelet count of 50,000 per mm³ of blood. Taking the NCERT normal range of "
  "1,50,000–3,50,000 per mm³, which problem is this person most likely to face?",
  ["Clotting disorders, leading to excessive loss of blood from injuries", "Reduced transport of oxygen by haemoglobin",
   "Failure of immune responses mediated by B and T lymphocytes", "Excess formation of clots inside blood vessels"],
  "A",
  "Role of platelets",
  "NCERT: blood normally contains 1,50,000–3,50,000 platelets per mm³. Platelets release a variety of substances "
  "involved in the coagulation or clotting of blood, and a reduction in their number can lead to clotting disorders, "
  "which will lead to excessive loss of blood from the body. 50,000 per mm³ is far below normal.",
  ["50,000 < 1,50,000 → low platelets", "Low platelets → clotting disorders → excessive blood loss"],
  R_BFC("blood: formed elements"),
  why_others_wrong="Oxygen transport depends on RBCs and haemoglobin; immune responses depend on lymphocytes; fewer "
                   "platelets lead to less clotting, not more.",
  seconds=30)

Z(BFC, "Coagulation and lymph", "Basic", "direct",
  "Fresh blood is collected into a tube containing a chemical that removes calcium ions from it. The blood does not "
  "clot. According to NCERT, the best explanation is that:",
  ["Calcium ions are needed to make RBCs biconcave", "Calcium ions are the source of fibrinogen",
   "Without calcium ions, platelets cannot be formed from megakaryocytes",
   "Calcium ions play a very important role in the clotting of blood"], "D",
  "Calcium in coagulation",
  "NCERT: coagulation involves a cascade forming thrombokinase, which converts prothrombin into thrombin; thrombin "
  "converts inactive fibrinogen into fibrin, whose threads form the clot. Calcium ions play a very important role in "
  "clotting, so removing them prevents it.",
  ["Ca²⁺ removed → clotting mechanism cannot proceed"],
  R_BFC("coagulation of blood"),
  why_others_wrong="RBC shape and platelet formation in bone marrow are not what fails in a collection tube; "
                   "fibrinogen is a plasma protein, not a product of calcium ions.",
  seconds=25)

Z(BFC, "Human heart", "Basic", "direct",
  "Which valve prevents the backflow of blood from the aorta into the left ventricle?",
  ["Bicuspid (mitral) valve", "Semilunar valve at the opening of the aorta", "Tricuspid valve",
   "Atrio-ventricular septum"], "B",
  "Valves of the human heart",
  "NCERT: the openings of the right and left ventricles into the pulmonary artery and the aorta respectively are "
  "provided with the semilunar valves; the valves in the heart allow the flow of blood only in one direction, i.e. "
  "from the atria to the ventricles and from the ventricles to the pulmonary artery or aorta.",
  ["Left ventricle → aorta opening → semilunar valve"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="The bicuspid valve guards the left atrio-ventricular opening and the tricuspid valve the right one; "
                   "the atrio-ventricular septum is a fibrous partition, not a valve.",
  seconds=20)

Z(BFC, "Cardiac cycle and ECG", "Basic", "direct",
  "In a patient's ECG, the P-waves are absent while QRS complexes are present. Which event is NOT being recorded "
  "normally in this patient?",
  ["Depolarisation of the ventricles", "Return of the ventricles from the excited to the normal state",
   "Electrical excitation (depolarisation) of the atria", "Closure of the semilunar valves"], "C",
  "Waves of a standard ECG",
  "NCERT: the P-wave represents the electrical excitation (or depolarisation) of the atria, which leads to the "
  "contraction of both the atria. The QRS complex represents depolarisation of the ventricles and the T-wave their "
  "return from the excited to the normal state (repolarisation).",
  ["P-wave = atrial depolarisation", "P absent → atrial excitation not recorded normally"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="Ventricular depolarisation is shown by the QRS complex, which is present; ventricular "
                   "repolarisation is the T-wave; valve closure is heard as a heart sound, not drawn as a P-wave.",
  seconds=25)

Z(BFC, "Circulatory disorders", "Basic", "direct",
  "Angina pectoris, the acute chest pain felt when not enough oxygen reaches the heart muscle, is described by NCERT "
  "as:",
  ["Occurring only in elderly men", "A form of cardiac arrest in which the heart stops beating",
   "Another name for congestive heart failure", "Able to occur at any age, but more common among the middle-aged and "
   "elderly"], "D",
  "Angina",
  "NCERT: angina (angina pectoris) is a symptom of acute chest pain that appears when no enough oxygen is reaching "
  "the heart muscle. It can occur in men and women of any age, but it is more common among the middle-aged and "
  "elderly; it occurs due to conditions that affect the blood flow.",
  ["Angina → any age, more common in middle-aged and elderly"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="NCERT says angina occurs in men and women of any age; cardiac arrest is when the heart stops "
                   "beating; heart failure is a different condition in which the heart does not pump blood "
                   "effectively enough.",
  seconds=25)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "numerical",
  "In a person's ECG, successive QRS complexes are 0.75 s apart. If each ventricle pumps out 70 mL of blood per beat, "
  "what is the person's cardiac output?",
  ["5040 mL per minute", "4200 mL per minute", "5600 mL per minute", "3150 mL per minute"], "C",
  "Heart rate from ECG and cardiac output",
  "Each QRS complex marks one ventricular depolarisation, so one beat occurs every 0.75 s. Heart rate = 60 ÷ 0.75 = "
  "80 beats per minute. NCERT: cardiac output = stroke volume × heart rate = 70 mL × 80 = 5600 mL per minute.",
  ["Heart rate = 60 / 0.75 = 80 per minute", "Cardiac output = 70 × 80 = 5600 mL per minute"],
  R_BFC("cardiac cycle; electrocardiograph (ECG)"),
  why_others_wrong="5040 uses the typical rate of 72 per minute instead of the given ECG; 4200 assumes one beat per "
                   "second; 3150 multiplies by the interval instead of dividing by it.",
  seconds=60, verified_by=RECOMPUTED)

Z(BFC, "Coagulation and lymph", "Intermediate", "assertion_reason",
  ar("Serum separated from clotted blood cannot form a clot again.",
     "Serum is plasma without the clotting factors."),
  ASSERTION_REASON, "A",
  "Plasma and serum",
  "NCERT: plasma without the clotting factors is called serum. The clotting factors, including fibrinogen, which "
  "thrombin converts into fibrin, are used up in forming the clot; serum lacks them and so cannot clot.",
  ["Serum = plasma − clotting factors", "No clotting factors → no clot"],
  R_BFC("blood: plasma; coagulation of blood"),
  why_others_wrong="B is wrong because the absence of clotting factors is precisely why serum cannot clot; C and D "
                   "are wrong because both statements are true.",
  seconds=35)

Z(BFC, "Blood and blood groups", "Intermediate", "multi_statement",
  ms("Which of the following statements about a person with blood group A, Rh-ve are correct?",
     ["Antigen A is present on the surface of his RBCs.",
      "His plasma contains anti-B antibodies.",
      "Considering ABO and Rh groups, his blood can be given to a recipient of group AB, Rh+ve.",
      "He can safely receive blood from a group O, Rh+ve donor.",
      "He can safely receive blood from a group AB, Rh-ve donor."]),
  ["(a) and (b) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only"], "B",
  "ABO and Rh compatibility",
  "NCERT: group A persons have antigen A on their RBCs and anti-B antibodies in their plasma. Group AB persons have no "
  "anti-A or anti-B antibodies and can accept blood of any ABO group, and an Rh+ve recipient has the Rh antigen, so "
  "Rh-ve blood is safe for them. An Rh-ve person exposed to Rh+ve blood forms antibodies against the Rh antigen, so "
  "Rh+ve blood is not safe for him. Group AB blood carries antigen B, which his anti-B antibodies would attack.",
  ["(a) true", "(b) true", "(c) true", "(d) false – Rh mismatch", "(e) false – antigen B meets anti-B"],
  R_BFC("blood groups"),
  why_others_wrong="A leaves out (c); C includes the Rh-mismatched (d); D includes (e) and leaves out (a).",
  seconds=60)
ms_check("abc", ["(a) and (b) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only",
                 "(b), (c) and (e) only"], "B")

Z(BFC, "Double circulation and regulation", "Intermediate", "match_list",
  ml(("chamber", "role in double circulation"), ["Right atrium", "Left atrium", "Right ventricle", "Left ventricle"],
     ["Pumps oxygenated blood into the aorta", "Receives oxygenated blood through the pulmonary veins",
      "Pumps deoxygenated blood into the pulmonary artery", "Receives deoxygenated blood through the vena cava"]),
  match_options(M("IV", "II", "III", "I"), [M("II", "IV", "III", "I"), M("IV", "II", "I", "III"),
                                            M("II", "IV", "I", "III")], "D"), "D",
  "Pulmonary and systemic circulation",
  "NCERT: deoxygenated blood from the body is emptied into the right atrium through the vena cava; the right "
  "ventricle pumps it into the pulmonary artery to the lungs. Oxygenated blood from the lungs returns through the "
  "pulmonary veins into the left atrium, and the left ventricle pumps it into the aorta for the systemic circulation.",
  ["RA → IV", "LA → II", "RV → III", "LV → I"],
  R_BFC("double circulation"),
  why_others_wrong="A swaps the two atria; B swaps the two ventricles; C swaps both pairs.",
  seconds=40)

Z(BFC, "Double circulation and regulation", "Intermediate", "statement_pair",
  sp("If the parasympathetic neural signals to a person's heart are blocked, the rate of his heartbeat tends to rise.",
     "Adrenal medullary hormones decrease the cardiac output."),
  STATEMENT_PAIR, "C",
  "Neural and hormonal regulation of the heart",
  "NCERT: neural signals through the sympathetic nerves increase the rate of heartbeat, the strength of ventricular "
  "contraction and thereby the cardiac output; parasympathetic signals decrease the rate of heartbeat and the speed of "
  "conduction of the action potential, and thereby the cardiac output. Blocking the slowing (parasympathetic) input "
  "lets the rate rise. Adrenal medullary hormones can also increase the cardiac output.",
  ["Statement I → true (the slowing influence is removed)", "Statement II → false (they increase it)"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="A and D accept that adrenal medullary hormones lower cardiac output; B rejects the consequence of "
                   "removing the parasympathetic brake.",
  seconds=40)

Z(BFC, "Coagulation and lymph", "Intermediate", "direct",
  "If the lymphatic vessels draining a person's leg were blocked, which change would be expected in that leg?",
  ["Interstitial fluid would collect in the tissue spaces, because it could not be drained back to the major veins",
   "RBCs would leak out of the capillaries into the tissue spaces",
   "Blood in the leg would stop clotting, because lymph carries the platelets",
   "Arterial blood would bypass the capillaries and enter the lymph vessels"], "A",
  "Lymphatic drainage of tissue fluid",
  "NCERT: as blood passes through the capillaries in tissues, some water along with many small water-soluble "
  "substances moves out into the spaces between the cells; this is the interstitial or tissue fluid. An elaborate "
  "network of vessels called the lymphatic system collects this fluid and drains it back to the major veins. If that "
  "drainage is blocked, the tissue fluid accumulates.",
  ["Capillaries → tissue fluid", "Lymph vessels → back to major veins", "Blocked → fluid accumulates"],
  R_BFC("lymph (tissue fluid)"),
  why_others_wrong="Most formed elements stay in the blood vessels; platelets are carried in blood, not lymph; "
                   "arterial blood does not enter lymph vessels.",
  seconds=40)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "multi_statement",
  ms("Consider the phase of the cardiac cycle in which blood is being ejected from the ventricles into the pulmonary "
     "artery and the aorta. Which of the following statements are correct for this phase?",
     ["The tricuspid valve is closed.",
      "The bicuspid valve is closed.",
      "The semilunar valves are open.",
      "The atria are undergoing systole.",
      "The ventricular pressure is lower than that in the aorta."]),
  ["(a), (b) and (d) only", "(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"], "B",
  "Valve positions during ventricular ejection",
  "NCERT: as the ventricles contract, ventricular pressure increases, closing the tricuspid and bicuspid valves due to "
  "attempted backflow into the atria. As ventricular pressure rises further, the semilunar valves guarding the "
  "pulmonary artery and the aorta are forced open, allowing blood to flow into these vessels. The atria undergo "
  "relaxation (diastole), coinciding with the ventricular systole.",
  ["(a) true", "(b) true", "(c) true – forced open by higher ventricular pressure", "(d) false – atria relax",
   "(e) false – ventricular pressure must exceed aortic pressure"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A and D include (d); C includes (d) and (e) and leaves out the closed AV valves.",
  seconds=60)
ms_check("abc", ["(a), (b) and (d) only", "(a), (b) and (c) only", "(c), (d) and (e) only",
                 "(a), (b), (c) and (d) only"], "B")

Z(BFC, "Double circulation and regulation", "Advanced", "multi_statement",
  ms("An RBC leaves a capillary in a person's foot and travels by the shortest route to the capillaries of the lungs. "
     "Which of the following statements about its journey are correct?",
     ["It enters the right atrium through the vena cava.",
      "It passes through the tricuspid valve.",
      "It passes through the bicuspid valve.",
      "It leaves the heart through the pulmonary artery.",
      "It passes through the left ventricle."]),
  ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (d) only", "(a), (c) and (e) only"], "C",
  "Route of blood in double circulation",
  "NCERT: deoxygenated blood from the tissues is collected by venules, veins and the vena cava and emptied into the "
  "right atrium; it passes through the tricuspid valve into the right ventricle and is pumped into the pulmonary "
  "artery to the lungs. The bicuspid valve and the left ventricle are on the return path, after the lungs.",
  ["Vena cava → right atrium", "Tricuspid → right ventricle", "Semilunar valve → pulmonary artery → lungs",
   "Bicuspid and left ventricle come only after the lungs"],
  R_BFC("double circulation"),
  why_others_wrong="A adds the bicuspid valve; B adds the left ventricle and leaves out (a); D includes both "
                   "left-side structures.",
  seconds=60)
ms_check("abd", ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (d) only",
                 "(a), (c) and (e) only"], "C")

Z(BFC, "Circulatory disorders", "Advanced", "statement_pair",
  sp("In a blood pressure reading of 150/95 mm Hg, 95 mm Hg is the diastolic (resting) pressure.",
     "If repeated checks give readings like 150/95 mm Hg, the person has hypertension, which can also affect vital "
     "organs like the brain and kidney."),
  STATEMENT_PAIR, "A",
  "Interpreting blood pressure",
  "NCERT: in a reading such as 120/80 mm Hg, the first number is the systolic (pumping) pressure and the second the "
  "diastolic (resting) pressure. If repeated checks of blood pressure show 140/90 mm Hg or higher, it shows "
  "hypertension; high blood pressure leads to heart diseases and also affects vital organs like the brain and kidney. "
  "150/95 exceeds 140/90 on both counts.",
  ["Second number → diastolic", "150 ≥ 140 and 95 ≥ 90 on repeated checks → hypertension"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="Both statements apply the NCERT definitions correctly, so B, C and D are wrong.",
  seconds=40)

Z(BFC, "Coagulation and lymph", "Advanced", "direct",
  "Which sequence correctly orders the events leading to a clot at a wound?",
  ["Prothrombin → thrombin → injury → thrombokinase → fibrin → fibrinogen",
   "Injury → fibrinogen → fibrin → thrombokinase → prothrombin → clot",
   "Injury → thrombin → thrombokinase → prothrombin → fibrinogen → clot",
   "Injury → release of factors by platelets and injured tissue → thrombokinase → prothrombin to thrombin → "
   "fibrinogen to fibrin → clot"], "D",
  "Cascade of coagulation",
  "NCERT: an injury or trauma stimulates the platelets to release certain factors which activate the mechanism of "
  "coagulation; factors released by the tissues at the site of injury can also initiate it. A cascade forms "
  "thrombokinase, which is required for the formation of thrombin from prothrombin; thrombin converts inactive "
  "fibrinogen into fibrin, and the network of fibrin threads traps formed elements to form the clot.",
  ["Injury → factors", "Thrombokinase", "Prothrombin → thrombin", "Fibrinogen → fibrin → clot"],
  R_BFC("coagulation of blood"),
  why_others_wrong="A starts with prothrombin before the injury and reverses fibrinogen and fibrin; B puts fibrin "
                   "formation before thrombokinase; C puts thrombin before thrombokinase and prothrombin.",
  seconds=45)

Z(BFC, "Double circulation and regulation", "Advanced", "direct",
  "A child is born with an opening in the inter-ventricular septum. Which consequence would be expected?",
  ["Deoxygenated blood would enter the aorta directly from the right atrium",
   "Oxygenated and deoxygenated blood would mix in the ventricles, as happens in the single ventricle of amphibians",
   "The pulmonary circulation would carry only oxygenated blood",
   "Both atria would stop receiving blood"], "B",
  "Significance of separate ventricles",
  "NCERT: the inter-ventricular septum is a thick-walled partition separating the left and right ventricles, and "
  "double circulation keeps oxygenated and deoxygenated blood apart. In amphibians and most reptiles the heart has a "
  "single ventricle in which oxygenated and deoxygenated blood mix (incomplete double circulation). An opening in the "
  "septum would likewise allow mixing in the ventricles.",
  ["Septum separates the ventricles", "Opening → mixing of oxygenated and deoxygenated blood"],
  R_BFC("human heart; double circulation"),
  why_others_wrong="The atria are separated from each other by the inter-atrial septum, which is intact; the "
                   "pulmonary artery would still carry largely deoxygenated blood; venous return to the atria is "
                   "unaffected.",
  seconds=45)

# ================================================================ Excretory Products and their Elimination (B4 I5 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

# GFR 125 mL per minute -> litres per day.
GFR_DAY_L = F(125 * 60 * 24, 1000)
assert GFR_DAY_L == 180
assert F(125 * 60, 1000) == F(15, 2) and GFR_DAY_L / 10 == 18 and GFR_DAY_L * 10 == 1800   # per hour; slips

Z(EXC, "Urine formation", "Basic", "numerical",
  "The glomerular filtration rate (GFR) of a healthy individual is about 125 mL per minute. How much glomerular "
  "filtrate do the kidneys form in a day?",
  ["7.5 L", "180 L", "18 L", "1800 L"], "B",
  "Glomerular filtration rate",
  "NCERT: the amount of filtrate formed by the kidneys per minute is the GFR, about 125 mL per minute in a healthy "
  "individual, i.e. 180 litres per day. 125 mL × 60 × 24 = 1,80,000 mL = 180 L.",
  ["125 mL/min × 60 min/h × 24 h", "= 1,80,000 mL = 180 L per day"],
  R_EXC("urine formation"),
  why_others_wrong="7.5 L is the volume formed in one hour; 18 L and 1800 L come from slipping a factor of 10 in "
                   "converting millilitres to litres.",
  seconds=30, verified_by=RECOMPUTED)

Z(EXC, "Urine formation", "Basic", "direct",
  "Urine formation in the human kidney involves three main processes. Which of the following is NOT one of them?",
  ["Glomerular filtration", "Reabsorption", "Secretion", "Micturition"], "D",
  "Processes of urine formation",
  "NCERT: urine formation involves three main processes, namely glomerular filtration, reabsorption and secretion, "
  "which take place in different parts of the nephron. Micturition is the process of release of urine from the "
  "urinary bladder, after it has been formed.",
  ["Formation → filtration, reabsorption, secretion", "Micturition → release of stored urine"],
  R_EXC("urine formation; micturition"),
  why_others_wrong="Glomerular filtration, reabsorption and secretion are the three processes NCERT names for urine "
                   "formation.",
  seconds=20)

Z(EXC, "Disorders and dialysis", "Basic", "direct",
  "Inflammation of the glomeruli of the kidney is called:",
  ["Uremia", "Renal calculi", "Glomerulonephritis", "Renal failure"], "C",
  "Disorders of the excretory system",
  "NCERT: glomerulonephritis is the inflammation of the glomeruli of the kidney. Uremia is the accumulation of urea "
  "in the blood; renal calculi are stones or insoluble masses of crystallised salts formed within the kidney; renal "
  "failure is a malfunction of the kidneys.",
  ["Glomerul(i) + nephr(itis) → inflamed glomeruli"],
  R_EXC("disorders of the excretory system"),
  why_others_wrong="Uremia, renal calculi and renal failure are other disorders, none of which is defined as "
                   "inflammation of the glomeruli.",
  seconds=20)

Z(EXC, "Urine formation", "Basic", "assertion_reason",
  ar("Glucose filtered into Bowman's capsule is normally absent from the urine of a healthy person.",
     "Glucose is reabsorbed from the filtrate by the renal tubules by active transport."),
  ASSERTION_REASON, "A",
  "Reabsorption of glucose",
  "NCERT: substances like glucose, amino acids and Na⁺ in the filtrate are reabsorbed actively. Because filtered "
  "glucose is taken back by the tubules, normal urine lacks it; glucose in urine (glycosuria) is indicative of "
  "diabetes mellitus.",
  ["A true", "R true", "Active reabsorption returns the filtered glucose → R explains A"],
  R_EXC("urine formation: reabsorption"),
  why_others_wrong="B is wrong because tubular reabsorption is precisely why glucose does not reach the urine; C and D "
                   "are wrong because both statements are true.",
  seconds=30)

Z(EXC, "Regulation of kidney function", "Intermediate", "direct",
  "If the juxtaglomerular (JG) cells of a person's kidneys were destroyed, which response to a fall in GFR would fail "
  "to begin?",
  ["Release of ADH from the neurohypophysis in response to fluid loss",
   "Release of atrial natriuretic factor from the walls of the atria",
   "Release of renin, and with it the formation of angiotensin II and the release of aldosterone that it triggers",
   "Filtration of blood through the glomerular membrane"], "C",
  "Renin–angiotensin mechanism",
  "NCERT: a fall in glomerular blood flow, glomerular blood pressure or GFR can activate the JG cells to release "
  "renin, which converts angiotensinogen into angiotensin I and further to angiotensin II. Angiotensin II, a powerful "
  "vasoconstrictor, raises the glomerular blood pressure and GFR, and activates the adrenal cortex to release "
  "aldosterone. Without JG cells, this whole chain cannot start.",
  ["JG cells → renin", "Renin → angiotensin I → angiotensin II", "Angiotensin II → aldosterone"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="ADH release is triggered through osmoreceptors and the hypothalamus; ANF comes from the atria of "
                   "the heart; filtration itself depends on glomerular capillary blood pressure, not on JG cells.",
  seconds=45)

Z(EXC, "Urine formation", "Intermediate", "match_list",
  ml(("part", "property"), ["Descending limb of Henle's loop", "Ascending limb of Henle's loop", "Collecting duct",
                            "Glomerulus"],
     ["Impermeable to water but allows transport of electrolytes",
      "Filters almost all the constituents of plasma except the proteins",
      "Permeable to water but almost impermeable to electrolytes",
      "Large amounts of water can be reabsorbed here to produce concentrated urine"]),
  match_options(M("III", "I", "IV", "II"), [M("I", "III", "IV", "II"), M("III", "I", "II", "IV"),
                                            M("I", "III", "II", "IV")], "D"), "D",
  "Functions of the parts of the nephron",
  "NCERT: the descending limb of Henle's loop is permeable to water but almost impermeable to electrolytes; the "
  "ascending limb is impermeable to water but allows transport of electrolytes actively or passively. Large amounts "
  "of water can be reabsorbed from the collecting duct to produce concentrated urine. In the glomerulus, almost all "
  "the constituents of plasma except the proteins pass into the lumen of Bowman's capsule.",
  ["Descending → III", "Ascending → I", "Collecting duct → IV", "Glomerulus → II"],
  R_EXC("function of the tubules; glomerular filtration"),
  why_others_wrong="A swaps the two limbs of Henle's loop; B swaps the collecting duct and the glomerulus; C makes "
                   "both swaps.",
  seconds=45)

Z(EXC, "Nephron structure", "Intermediate", "statement_pair",
  sp("The distal convoluted tubules of many nephrons open into a straight tube called the collecting duct.",
     "Many collecting ducts converge and open into the renal pelvis through the medullary pyramids in the calyces."),
  STATEMENT_PAIR, "A",
  "Collecting system of the kidney",
  "NCERT: the ascending limb of Henle's loop continues as another highly coiled tubular region called the distal "
  "convoluted tubule (DCT). The DCTs of many nephrons open into a straight tube called the collecting duct, many of "
  "which converge and open into the renal pelvis through the medullary pyramids in the calyces. Both statements are "
  "true.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("human excretory system"),
  why_others_wrong="Both statements are NCERT descriptions, so B, C and D are wrong.",
  seconds=30)

Z(EXC, "Modes of excretion", "Intermediate", "multi_statement",
  ms("Which of the following animals are correctly paired with the main nitrogenous waste they excrete?",
     ["Aquatic insects – ammonia", "Land snails – uric acid", "Marine fishes – urea", "Birds – urea",
      "Terrestrial amphibians – uric acid"]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (e) only"], "C",
  "Ammonotelism, ureotelism and uricotelism",
  "NCERT: many bony fishes, aquatic amphibians and aquatic insects are ammonotelic. Mammals, many terrestrial "
  "amphibians and marine fishes mainly excrete urea (ureotelic). Reptiles, birds, land snails and insects excrete "
  "uric acid (uricotelic).",
  ["(a) true", "(b) true", "(c) true", "(d) false – birds are uricotelic",
   "(e) false – terrestrial amphibians are ureotelic"],
  R_EXC("introduction: modes of excretion"),
  why_others_wrong="A leaves out (c); B includes (d); D includes (e) and leaves out (b).",
  seconds=50)
ms_check("abc", ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (e) only"], "C")

Z(EXC, "Disorders and dialysis", "Intermediate", "direct",
  "In haemodialysis, the dialysing fluid has the same composition as plasma except that it lacks the nitrogenous "
  "wastes. What is gained by keeping the other constituents the same as in plasma?",
  ["Useful plasma constituents have no concentration gradient across the membrane, so they are not lost from the "
   "blood, while nitrogenous wastes move out",
   "The cellophane membrane becomes impermeable to urea",
   "Blood cells can pass into the fluid and be cleaned",
   "Heparin is no longer needed to prevent clotting"], "A",
  "Principle of haemodialysis",
  "NCERT: in the dialysing unit, a coiled cellophane tube is surrounded by dialysing fluid having the same composition "
  "as plasma except the nitrogenous wastes. The porous membrane allows the passage of molecules based on the "
  "concentration gradient; as nitrogenous wastes are absent in the fluid, they freely move out of blood. For other "
  "constituents, equal concentrations on both sides mean no net loss.",
  ["Movement across the membrane follows concentration gradients", "Wastes: gradient blood → fluid",
   "Other constituents: no gradient → retained"],
  R_EXC("haemodialysis"),
  why_others_wrong="The membrane must let urea through for dialysis to work; blood cells are not meant to cross it; "
                   "heparin is still added as an anticoagulant before the blood enters the unit.",
  seconds=45)

Z(EXC, "Urine formation", "Advanced", "direct",
  "A drug blocks the transport of electrolytes out of the ascending limb of Henle's loop into the medullary fluid. "
  "What is the most likely effect on urine formation?",
  ["The medullary interstitium becomes more concentrated, so a smaller volume of more concentrated urine is formed",
   "Glucose starts appearing in the urine because its active reabsorption in the PCT stops",
   "The ascending limb becomes permeable to water, so the filtrate is concentrated there",
   "The osmolarity gradient of the medullary interstitium falls, so less water is reabsorbed from the collecting "
   "duct and the urine becomes more dilute"], "D",
  "Counter-current mechanism and urine concentration",
  "NCERT: the ascending limb is impermeable to water but transports electrolytes actively or passively to the "
  "medullary fluid. NaCl transported by the ascending limb is exchanged with the descending limb of the vasa recta, "
  "and with urea this maintains an increasing osmolarity towards the inner medulla (about 300 to 1200 mOsmol L⁻¹). "
  "This gradient helps the easy passage of water from the collecting tubule, concentrating the filtrate. If the "
  "ascending limb cannot deliver electrolytes, the gradient collapses and urine stays dilute.",
  ["Block electrolyte transport → medullary osmolarity falls", "Less water drawn from collecting duct",
   "More dilute urine"],
  R_EXC("mechanism of concentration of the filtrate"),
  why_others_wrong="A reverses the effect; glucose reabsorption occurs in the PCT and is not affected; the drug does "
                   "not alter the water impermeability of the ascending limb.",
  seconds=60)

Z(EXC, "Regulation of kidney function", "Advanced", "multi_statement",
  ms("A person loses a large amount of body fluid through heavy sweating on a hot day. According to NCERT, which of "
     "the following responses are expected?",
     ["Osmoreceptors are activated and stimulate the hypothalamus to release ADH from the neurohypophysis.",
      "More water is reabsorbed from the latter parts of the renal tubule.",
      "ADH, by constricting blood vessels, can raise blood pressure and thereby glomerular blood flow.",
      "A larger volume of urine is passed.",
      "Release of atrial natriuretic factor increases."]),
  ["(a) and (b) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"], "B",
  "ADH response to fluid loss",
  "NCERT: osmoreceptors are activated by changes in blood volume, body fluid volume and ionic concentration; an "
  "excessive loss of fluid activates them, and they stimulate the hypothalamus to release ADH (vasopressin) from the "
  "neurohypophysis. ADH facilitates water reabsorption from the latter parts of the tubule, preventing diuresis, and "
  "by its constrictory effect on blood vessels raises blood pressure, which can increase glomerular blood flow and "
  "GFR. ANF is released when blood flow to the atria increases, not after fluid loss.",
  ["(a) true", "(b) true", "(c) true", "(d) false – diuresis is prevented", "(e) false – ANF needs more atrial flow"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A leaves out (c); C includes (d) and leaves out (a); D includes (e).",
  seconds=60)
ms_check("abc", ["(a) and (b) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
         "B")

Z(EXC, "Nephron structure", "Advanced", "assertion_reason",
  ar("Juxtamedullary nephrons contribute more than cortical nephrons to the production of concentrated urine.",
     "In juxtamedullary nephrons, Henle's loop is very long and runs deep into the medulla alongside a "
     "well-developed vasa recta, whereas in cortical nephrons the loop is short and the vasa recta is absent or "
     "highly reduced."),
  ASSERTION_REASON, "A",
  "Cortical and juxtamedullary nephrons",
  "NCERT: in cortical nephrons the loop of Henle is too short and extends only very little into the medulla, and the "
  "vasa recta is absent or highly reduced; in juxtamedullary nephrons the loop is very long and runs deep into the "
  "medulla. The proximity between Henle's loop and the vasa recta, and the counter-current in them, maintain the "
  "increasing medullary osmolarity that allows concentrated urine to be formed. So the long loop with its vasa recta "
  "is the reason these nephrons matter more for concentration.",
  ["A true", "R true", "Long loop + vasa recta → counter-current gradient → concentration → R explains A"],
  R_EXC("human excretory system; mechanism of concentration of the filtrate"),
  why_others_wrong="B is wrong because the structural difference in R is what equips these nephrons for the "
                   "counter-current mechanism; C and D are wrong because both statements are true.",
  seconds=50)

Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("Trace a molecule of urea carried to the kidney in the blood. Which of the following statements are correct?",
     ["It can pass from the glomerular blood into the lumen of Bowman's capsule during filtration.",
      "Nitrogenous wastes such as urea are reabsorbed from the filtrate by passive transport.",
      "Small amounts of urea pass from the collecting duct into the medullary interstitium, helping to keep up its "
      "osmolarity.",
      "All the filtered urea is reabsorbed, so the urine of a healthy person contains no urea.",
      "The urea was formed from ammonia in the kidney itself."]),
  ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (d) and (e) only"], "C",
  "Handling of urea by the kidney",
  "NCERT: almost all the constituents of plasma except the proteins pass into Bowman's capsule; nitrogenous wastes "
  "are absorbed by passive transport; the collecting duct allows passage of small amounts of urea into the medullary "
  "interstitium to keep up the osmolarity. A healthy adult still excretes 25–30 g of urea per day. In ureotelic "
  "animals, ammonia is converted into urea in the liver, not in the kidney.",
  ["(a) true", "(b) true", "(c) true", "(d) false – 25–30 g urea per day in urine", "(e) false – made in the liver"],
  R_EXC("urine formation; function of the tubules"),
  why_others_wrong="A includes (d); B includes (e) and leaves out (a); D includes (d) and (e).",
  seconds=60)
ms_check("abc", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only",
                 "(a), (d) and (e) only"], "C")

# ================================================================ Locomotion and Movement (B5 I6 A5)
R_LOC = lambda s: ref("Locomotion and Movement", s)

# Sliding filaments: the A-band keeps its length; the I-band (total within one sarcomere) = sarcomere - A-band.
SARC0, A_BAND, SARC1 = F(24, 10), F(16, 10), F(2)
I0, I1 = SARC0 - A_BAND, SARC1 - A_BAND
assert (I0, I1) == (F(8, 10), F(4, 10))
PROP = SARC1 / SARC0                                                               # wrong: everything shortens
assert (A_BAND * PROP, I0 * PROP) == (F(4, 3), F(2, 3))
assert SARC1 - I0 == F(12, 10)                                                     # wrong: I fixed, A shrinks

Z(LOC, "Types of movement", "Basic", "direct",
  "Long-term smoking damages the cilia lining a person's trachea. Which function of these cilia is then impaired?",
  ["Production of sound in the larynx",
   "Removal of dust particles and some foreign substances inhaled with atmospheric air",
   "Exchange of O₂ and CO₂ across the tracheal wall",
   "Passage of food from the pharynx to the oesophagus"], "B",
  "Ciliary movement in humans",
  "NCERT: ciliary movement occurs in most of our internal tubular organs lined by ciliated epithelium. The "
  "coordinated movements of cilia in the trachea help in removing dust particles and some of the foreign substances "
  "inhaled along with the atmospheric air.",
  ["Tracheal cilia → sweep out dust and foreign particles"],
  R_LOC("types of movement"),
  why_others_wrong="Sound is produced by the larynx; gas exchange occurs at the alveoli, not the trachea; swallowing "
                   "of food is not a function of tracheal cilia.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "direct",
  "Which of the following bones belongs to the axial skeleton rather than the appendicular skeleton?",
  ["Clavicle", "Patella", "Coxal bone", "Sternum"], "D",
  "Axial and appendicular skeleton",
  "NCERT: the axial skeleton comprises 80 bones distributed along the main axis of the body – the skull, vertebral "
  "column, sternum and ribs. The appendicular skeleton comprises the bones of the limbs along with their girdles.",
  ["Sternum → rib cage → axial", "Clavicle (girdle), patella (limb), coxal bone (girdle) → appendicular"],
  R_LOC("skeletal system"),
  why_others_wrong="The clavicle is part of the pectoral girdle, the patella part of the hind limb and the coxal bone "
                   "part of the pelvic girdle – all appendicular.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "direct",
  "Which pair consists of one bone of the pectoral girdle and one bone of the pelvic girdle?",
  ["Scapula and clavicle", "Clavicle and ilium", "Ischium and pubis", "Sternum and scapula"], "B",
  "Girdles of the human skeleton",
  "NCERT: each half of the pectoral girdle consists of a clavicle and a scapula. The pelvic girdle consists of two "
  "coxal bones, each formed by the fusion of three bones – ilium, ischium and pubis.",
  ["Clavicle → pectoral girdle", "Ilium → part of the coxal bone → pelvic girdle"],
  R_LOC("appendicular skeleton"),
  why_others_wrong="Scapula and clavicle are both pectoral; ischium and pubis are both pelvic; the sternum is part of "
                   "the axial skeleton.",
  seconds=20)

Z(LOC, "Muscular and skeletal disorders", "Basic", "direct",
  "A 62-year-old woman, whose estrogen levels have fallen, fractures her wrist in a minor fall. An age-related "
  "decrease in her bone mass is found. The disorder is most likely:",
  ["Gout", "Arthritis", "Tetany", "Osteoporosis"], "D",
  "Osteoporosis",
  "NCERT: osteoporosis is an age-related disorder characterised by decreased bone mass and increased chances of "
  "fractures; decreased levels of estrogen is a common cause.",
  ["Age + low estrogen + low bone mass + fracture → osteoporosis"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="Gout is inflammation of joints due to uric acid crystals; arthritis is inflammation of joints; "
                   "tetany is rapid spasms due to low Ca²⁺.",
  seconds=20)

Z(LOC, "Joints", "Basic", "statement_pair",
  sp("The joint between the humerus and the pectoral girdle is a ball and socket joint.",
     "The knee joint is a saddle joint."),
  STATEMENT_PAIR, "C",
  "Synovial joints",
  "NCERT examples of synovial joints: ball and socket joint (between humerus and pectoral girdle), hinge joint (knee "
  "joint), pivot joint (between atlas and axis), gliding joint (between the carpals) and saddle joint (between the "
  "carpal and metacarpal of the thumb).",
  ["Statement I → true", "Statement II → false (knee = hinge joint)"],
  R_LOC("joints"),
  why_others_wrong="A and D accept the knee as a saddle joint; B rejects the correct example of a ball and socket "
                   "joint.",
  seconds=25)

Z(LOC, "Muscle contraction", "Intermediate", "numerical",
  "A resting sarcomere is 2.4 µm long and its A-band is 1.6 µm long. During contraction, the sarcomere shortens to "
  "2.0 µm. According to the sliding filament theory, what will be the length of the A-band, and the total length of "
  "the I-band within this sarcomere, after contraction?",
  ["A-band 1.2 µm; I-band 0.8 µm", "A-band 1.6 µm; I-band 0.4 µm", "A-band about 1.33 µm; I-band about 0.67 µm",
   "A-band 1.6 µm; I-band 0.8 µm"], "B",
  "Band changes in muscle contraction",
  "NCERT: during contraction the thin filaments slide over the thick filaments; the Z-lines are pulled inwards, the "
  "sarcomere shortens, the I-bands get reduced and the A-bands retain their length. So the A-band stays 1.6 µm. The "
  "I-band within one sarcomere is the sarcomere length minus the A-band: before, 2.4 − 1.6 = 0.8 µm; after, "
  "2.0 − 1.6 = 0.4 µm.",
  ["A-band unchanged = 1.6 µm", "I-band (total) = sarcomere − A-band", "= 2.0 − 1.6 = 0.4 µm"],
  R_LOC("mechanism of muscle contraction"),
  shortcut="Whatever the sarcomere loses, the I-band loses: 0.8 − 0.4 = 0.4 µm.",
  why_others_wrong="A shortens the A-band and keeps the I-band, the reverse of what happens; C shrinks every band in "
                   "proportion; D keeps both bands unchanged, which is impossible if the sarcomere shortens.",
  seconds=75, verified_by=RECOMPUTED)

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("If the ATP supply of a contracting muscle fibre is exhausted, the cross bridges between myosin heads and actin "
     "cannot be broken.",
     "Binding of a new ATP molecule to the myosin head is what breaks the cross bridge."),
  ASSERTION_REASON, "A",
  "Role of ATP in the cross-bridge cycle",
  "NCERT: after the power stroke, the myosin head releases ADP and Pi and goes back to its relaxed state; a new ATP "
  "binds and the cross bridge is broken. The ATP is again hydrolysed by the myosin head and the cycle of cross-bridge "
  "formation and breakage is repeated. Without ATP, nothing detaches the head from actin.",
  ["A true", "R true", "ATP binding detaches myosin from actin → no ATP, no detachment → R explains A"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="B is wrong because the role of ATP in R is exactly why the bridges stay attached; C and D are wrong "
                   "because both statements are true.",
  seconds=40)

Z(LOC, "Skeletal system", "Intermediate", "match_list",
  ml(("bone or part", "where it belongs"), ["Patella", "Acromion", "Atlas", "Malleus"],
     ["Middle ear", "First vertebra of the vertebral column", "Process of the scapula in the pectoral girdle",
      "Covers the knee ventrally in the hind limb"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Locating bones of the human skeleton",
  "NCERT: the patella is a cup-shaped bone which covers the knee ventrally (knee cap); the spine of the scapula "
  "projects as a flat, expanded process called the acromion; the first vertebra is the atlas, which articulates with "
  "the occipital condyles; the malleus, incus and stapes are the three ear ossicles of each middle ear.",
  ["Patella → IV", "Acromion → III", "Atlas → II", "Malleus → I"],
  R_LOC("skeletal system"),
  why_others_wrong="A swaps the patella and the acromion; B swaps the atlas and the malleus; C swaps the acromion and "
                   "the atlas.",
  seconds=40)

Z(LOC, "Types of movement", "Intermediate", "multi_statement",
  ms("Which of the following movements in the human body are brought about by muscular movement (rather than by "
     "amoeboid or ciliary movement)?",
     ["Movement of the jaws", "Passage of ova through the female reproductive tract",
      "Movement of the tongue", "Movement of macrophages", "Movement of the limbs"]),
  ["(a), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"], "B",
  "Amoeboid, ciliary and muscular movement",
  "NCERT: cells of the human body exhibit three main types of movement. Some specialised cells such as macrophages "
  "and leucocytes show amoeboid movement; passage of ova through the female reproductive tract is facilitated by "
  "ciliary movement; movement of our limbs, jaws, tongue, etc., requires muscular movement.",
  ["(a) muscular", "(b) ciliary ✗", "(c) muscular", "(d) amoeboid ✗", "(e) muscular"],
  R_LOC("types of movement"),
  why_others_wrong="A includes amoeboid movement of macrophages; C includes (b) and (d); D includes the ciliary "
                   "passage of ova.",
  seconds=45)
ms_check("ace", ["(a), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only",
                 "(a), (b), (c) and (e) only"], "B")

Z(LOC, "Joints", "Intermediate", "direct",
  "Which of the following pairs consists of two synovial joints?",
  ["Sutures between the flat bones of the skull and the knee joint",
   "Joint between adjacent vertebrae and the knee joint",
   "Sutures of the skull and the joint between adjacent vertebrae",
   "Knee joint and the joint between the carpals"], "D",
  "Types of joints",
  "NCERT: joints are classified as fibrous (e.g. sutures of the skull, no movement), cartilaginous (e.g. between "
  "adjacent vertebrae, limited movement) and synovial (fluid-filled cavity, considerable movement). The knee joint is "
  "a hinge joint and the joint between the carpals is a gliding joint – both synovial.",
  ["Knee → hinge → synovial", "Between carpals → gliding → synovial"],
  R_LOC("joints"),
  why_others_wrong="Sutures are fibrous joints and the joints between adjacent vertebrae are cartilaginous, so every "
                   "other pair includes a non-synovial joint.",
  seconds=35)

Z(LOC, "Muscular and skeletal disorders", "Intermediate", "assertion_reason",
  ar("In myasthenia gravis, skeletal muscles show fatigue and weakening, and may even be paralysed.",
     "Myasthenia gravis is caused by a low level of Ca²⁺ in body fluids."),
  ASSERTION_REASON, "C",
  "Myasthenia gravis and tetany",
  "NCERT: myasthenia gravis is an auto-immune disorder affecting the neuromuscular junction, leading to fatigue, "
  "weakening and paralysis of skeletal muscle. Low Ca²⁺ in body fluids causes tetany (rapid spasms), not myasthenia "
  "gravis.",
  ["A true", "R false – that is the cause of tetany; myasthenia gravis is auto-immune"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="A and B accept the wrong cause; D rejects NCERT's description of the disorder.",
  seconds=35)

Z(LOC, "Muscle contraction", "Advanced", "direct",
  "A toxin stops the myosin head from hydrolysing ATP, although Ca²⁺ is released normally and the active sites on "
  "actin are exposed. What will happen to the muscle fibre?",
  ["It contracts normally, because Ca²⁺ alone makes actin slide",
   "Cross bridges cannot form, because the myosin head does not get the energy of ATP hydrolysis it uses to bind "
   "actin",
   "It contracts more strongly, because unused ATP accumulates in the sarcoplasm",
   "Troponin re-masks the active sites, because Ca²⁺ is pumped back at once"], "B",
  "ATP hydrolysis and cross-bridge formation",
  "NCERT: utilising the energy from ATP hydrolysis, the myosin head now binds to the exposed active sites on actin to "
  "form a cross bridge, which pulls the actin filaments towards the centre of the A-band. If ATP cannot be "
  "hydrolysed, the head does not get this energy, so cross bridges and contraction fail even though the sites are "
  "exposed.",
  ["Ca²⁺ exposes actin sites (still happens)", "ATP hydrolysis energises myosin head (blocked)",
   "No cross bridge → no contraction"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="Ca²⁺ only unmasks the sites; it does not move actin by itself; unused ATP gives no extra force; the "
                   "stem says Ca²⁺ is released normally, so re-masking is not the cause.",
  seconds=50)

Z(LOC, "Skeletal system", "Advanced", "multi_statement",
  ms("Which of the following statements about the human skeleton are correct?",
     ["Each half of the pectoral girdle consists of two bones.",
      "The pelvic girdle consists of two coxal bones, each formed by the fusion of three bones.",
      "Of the 12 pairs of ribs, three pairs are vertebrochondral (false) ribs.",
      "The floating ribs are the 8th, 9th and 10th pairs.",
      "The hyoid is a bone of the appendicular skeleton."]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (e) only", "(a), (b) and (c) only"], "D",
  "Girdles, ribs and the axial skeleton",
  "NCERT: each half of the pectoral girdle consists of a clavicle and a scapula; the pelvic girdle consists of two "
  "coxal bones, each formed by the fusion of ilium, ischium and pubis. The 8th, 9th and 10th pairs of ribs join the "
  "seventh rib with hyaline cartilage and are vertebrochondral (false) ribs, while the 11th and 12th pairs are not "
  "connected ventrally and are floating ribs. The hyoid is included in the skull, part of the axial skeleton.",
  ["(a) true – clavicle + scapula", "(b) true – ilium, ischium, pubis", "(c) true – 8th, 9th, 10th",
   "(d) false – floating = 11th and 12th", "(e) false – hyoid is axial"],
  R_LOC("skeletal system"),
  why_others_wrong="A leaves out (c); B includes (d); C includes (e) and leaves out (b).",
  seconds=60)
ms_check("abc", ["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (e) only", "(a), (b) and (c) only"], "D")

Z(LOC, "Muscle contraction", "Advanced", "direct",
  "Suppose the sarcoplasmic reticulum of a muscle fibre could release Ca²⁺ but could not take it back after the "
  "nerve stimulus stopped. What would most likely happen?",
  ["The fibre would never contract, because Ca²⁺ is needed only for relaxation",
   "The fibre would relax at once, because troponin would immediately mask the active sites",
   "The A-band would shorten, because Ca²⁺ dissolves the myosin filaments",
   "The fibre would be unable to relax, because Ca²⁺ would keep the active sites on actin unmasked"], "D",
  "Calcium and muscle relaxation",
  "NCERT: Ca²⁺ released from the sarcoplasmic reticulum binds a subunit of troponin on the actin filaments and "
  "removes the masking of the active sites for myosin, allowing cross bridges to form. During relaxation, Ca²⁺ is "
  "pumped back into the sarcoplasmic cisternae, resulting in the masking of the actin filaments. If Ca²⁺ cannot be "
  "taken back, the sites stay exposed and the fibre cannot relax.",
  ["Ca²⁺ stays in sarcoplasm", "Actin sites stay unmasked", "Cross-bridge cycling continues → no relaxation"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A reverses the role of Ca²⁺; B needs Ca²⁺ removal, which is what fails; C is wrong because the "
                   "A-band retains its length during contraction.",
  seconds=50)

Z(LOC, "Joints", "Advanced", "direct",
  "The head of which bone fits into the glenoid cavity, and what type of joint is formed there?",
  ["Femur; ball and socket joint", "Humerus; ball and socket joint", "Humerus; hinge joint", "Femur; hinge joint"],
  "B",
  "Glenoid cavity and the shoulder joint",
  "NCERT: below the acromion of the scapula is a depression called the glenoid cavity, which articulates with the "
  "head of the humerus to form the shoulder joint. The joint between the humerus and the pectoral girdle is the NCERT "
  "example of a ball and socket joint.",
  ["Glenoid cavity → head of humerus", "Humerus–pectoral girdle → ball and socket"],
  R_LOC("appendicular skeleton; joints"),
  why_others_wrong="The femur articulates with the acetabulum of the pelvic girdle, not the glenoid cavity; the knee, "
                   "not the shoulder, is NCERT's example of a hinge joint.",
  seconds=35)

Z(LOC, "Muscle contraction", "Advanced", "assertion_reason",
  ar("If a single motor neuron is destroyed, all the skeletal muscle fibres connected to it can no longer be made to "
     "contract by nerve signals, while the muscle's other fibres still respond.",
     "A motor neuron along with the muscle fibres connected to it constitutes a motor unit."),
  ASSERTION_REASON, "A",
  "Motor unit",
  "NCERT: muscle contraction is initiated by a signal sent by the CNS via a motor neuron, and a motor neuron along "
  "with the muscle fibres connected to it constitutes a motor unit. The fibres of one motor unit receive their "
  "command only through that neuron, so losing it silences exactly that unit; fibres of other motor units, served by "
  "other neurons, still respond.",
  ["A true", "R true", "Each fibre is commanded through its own motor neuron → R explains A"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="B is wrong because the motor-unit arrangement is precisely why only that neuron's fibres are "
                   "affected; C and D are wrong because both statements are true.",
  seconds=50)

# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "A tumour damages a person's hypothalamus. Which functions are most likely to be disturbed?",
  ["Control of body temperature and the urge for eating and drinking",
   "Connection of the left and right cerebral hemispheres",
   "Passage of the cerebral aqueduct through the brain",
   "Formation of the grey matter of the cerebral cortex"], "A",
  "Functions of the hypothalamus",
  "NCERT: the hypothalamus lies at the base of the thalamus and contains a number of centres which control body "
  "temperature and the urge for eating and drinking. It also contains groups of neurosecretory cells that secrete "
  "hypothalamic hormones.",
  ["Hypothalamus → centres for body temperature, eating and drinking"],
  R_NEU("forebrain"),
  why_others_wrong="The hemispheres are connected by the corpus callosum; the cerebral aqueduct passes through the "
                   "midbrain; the grey matter is the cerebral cortex itself.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "An injury to a person's medulla oblongata is life-threatening mainly because the medulla contains centres that "
  "control:",
  ["Memory, intelligence and communication", "Vision through the optic lobes",
   "Respiration, cardiovascular reflexes and gastric secretions", "Emotional reactions such as rage and fear"], "C",
  "Functions of the medulla",
  "NCERT: the medulla is connected to the spinal cord and contains centres which control respiration, "
  "cardiovascular reflexes and gastric secretions.",
  ["Medulla → respiration, cardiovascular reflexes, gastric secretions"],
  R_NEU("hindbrain"),
  why_others_wrong="Memory and communication involve association areas of the cerebral cortex; NCERT does not "
                   "assign vision to the medulla; emotional reactions involve the limbic system with the "
                   "hypothalamus.",
  seconds=25)

Z(NEU, "Neuron and nerves", "Basic", "direct",
  "A neuron with one axon and two or more dendrites, found in the cerebral cortex, is classed as:",
  ["Unipolar", "Multipolar", "Bipolar", "Pseudounipolar"], "B",
  "Types of neurons",
  "NCERT: based on the number of axons and dendrites, neurons are multipolar (one axon and two or more dendrites; "
  "found in the cerebral cortex), bipolar (one axon and one dendrite; found in the retina of the eye) and unipolar "
  "(cell body with one axon only; found usually in the embryonic stage).",
  ["One axon + two or more dendrites → multipolar"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="Unipolar neurons have only an axon; bipolar neurons have one axon and one dendrite; "
                   "'pseudounipolar' is not one of the NCERT categories.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "statement_pair",
  sp("The cerebral cortex contains motor areas, sensory areas and large regions that are neither clearly sensory nor "
     "motor in function.",
     "The thalamus is a major coordinating centre for sensory and motor signalling."),
  STATEMENT_PAIR, "A",
  "Cerebral cortex and thalamus",
  "NCERT: the cerebral cortex contains motor areas, sensory areas and large regions that are neither clearly sensory "
  "nor motor (the association areas). The cerebrum wraps around the thalamus, which is a major coordinating centre "
  "for sensory and motor signalling. Both statements are true.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("forebrain"),
  why_others_wrong="Both statements are NCERT descriptions, so B, C and D are wrong.",
  seconds=30)

Z(NEU, "Neuron and nerves", "Intermediate", "match_list",
  ml(("part of a neuron", "feature"), ["Dendrites", "Axon", "Synaptic knob", "Nissl's granules"],
     ["Contains synaptic vesicles filled with neurotransmitters",
      "Granular bodies in the cytoplasm of the cell body and dendrites",
      "Transmits impulses away from the cell body to a synapse or neuromuscular junction",
      "Short, repeatedly branched fibres transmitting impulses towards the cell body"]),
  match_options(M("IV", "III", "I", "II"), [M("III", "IV", "I", "II"), M("IV", "III", "II", "I"),
                                            M("III", "IV", "II", "I")], "D"), "D",
  "Structure of a neuron",
  "NCERT: dendrites are short fibres which branch repeatedly and project out of the cell body; they transmit impulses "
  "towards the cell body and contain Nissl's granules. The axon is a long fibre whose distal end is branched; it "
  "transmits impulses away from the cell body to a synapse or a neuromuscular junction. Each branch ends as a "
  "bulb-like synaptic knob containing synaptic vesicles filled with neurotransmitters. The cell body contains "
  "cytoplasm with typical organelles and certain granular bodies called Nissl's granules.",
  ["Dendrites → IV", "Axon → III", "Synaptic knob → I", "Nissl's granules → II"],
  R_NEU("structure of a neuron"),
  why_others_wrong="A swaps dendrites and axon; B swaps the synaptic knob and Nissl's granules; C makes both swaps.",
  seconds=40)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("Impulse transmission across an electrical synapse is slower than across a chemical synapse.",
     "At electrical synapses, the membranes of the pre- and post-synaptic neurons are in very close proximity."),
  ASSERTION_REASON, "D",
  "Electrical and chemical synapses",
  "NCERT: at electrical synapses the membranes of the pre- and post-synaptic neurons are in very close proximity, and "
  "electrical current can flow directly from one neuron into the other across them. Impulse transmission across an "
  "electrical synapse is always faster than that across a chemical synapse, which depends on the release and binding "
  "of neurotransmitters. So the Assertion is false and the Reason true.",
  ["A false – electrical synapses are faster", "R true"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A and B accept the false Assertion; C rejects the Reason, which is NCERT's description of an "
                   "electrical synapse.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following structures are correctly matched with the division of the brain to which they belong?",
     ["Thalamus – forebrain", "Corpora quadrigemina – midbrain", "Pons – hindbrain", "Hypothalamus – midbrain",
      "Cerebellum – forebrain"]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (e) only"], "C",
  "Divisions of the human brain",
  "NCERT: the forebrain consists of the cerebrum, thalamus and hypothalamus. The dorsal portion of the midbrain "
  "consists mainly of four round swellings called corpora quadrigemina. The hindbrain comprises the pons, cerebellum "
  "and medulla oblongata.",
  ["(a) true", "(b) true", "(c) true", "(d) false – forebrain", "(e) false – hindbrain"],
  R_NEU("central neural system"),
  why_others_wrong="A leaves out (c); B includes (d) and leaves out (a); D includes (e) and leaves out (b).",
  seconds=45)
ms_check("abc", ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (e) only"], "C")

Z(NEU, "Nervous system divisions", "Intermediate", "direct",
  "Damage to the somatic neural system nerves supplying a person's arm would most directly interfere with:",
  ["Impulses from the CNS to the smooth muscles of the arm's blood vessels",
   "Impulses from the CNS to the skeletal muscles of the arm",
   "Impulses from the CNS to the involuntary organs of the thorax",
   "Transmission across synapses inside the brain"], "B",
  "Somatic and autonomic neural systems",
  "NCERT: the peripheral neural system is divided into the somatic and the autonomic neural systems. The somatic "
  "neural system relays impulses from the CNS to the skeletal muscles, while the autonomic neural system transmits "
  "impulses from the CNS to the involuntary organs and smooth muscles of the body.",
  ["Somatic → skeletal muscles", "Autonomic → involuntary organs and smooth muscles"],
  R_NEU("human neural system"),
  why_others_wrong="Smooth muscles and involuntary organs are supplied by the autonomic neural system; synapses inside "
                   "the brain are part of the CNS, not the peripheral somatic nerves.",
  seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "statement_pair",
  sp("At the site of stimulation, the inner surface of the axonal membrane becomes positive and the outer surface "
     "negative, and the membrane at that site is said to be depolarised.",
     "The rise in Na⁺ permeability at the stimulated site is extremely short-lived and is quickly followed by a rise "
     "in permeability to K⁺."),
  STATEMENT_PAIR, "A",
  "Depolarisation and recovery",
  "NCERT: when a stimulus is applied, the membrane becomes freely permeable to Na⁺; the rapid influx reverses the "
  "polarity, making the outer surface negative and the inner surface positive, and the membrane at that site is said "
  "to be depolarised. The rise in Na⁺ permeability is extremely short-lived and is quickly followed by a rise in "
  "permeability to K⁺; K⁺ diffuses out and restores the resting potential.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="Both statements are NCERT's account of the action potential, so B, C and D are wrong.",
  seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "multi_statement",
  ms("A toxin blocks the rise in K⁺ permeability that normally follows the brief rise in Na⁺ permeability at a "
     "stimulated site of an axon, but does not affect the Na⁺ channels. Which of the following would be expected at "
     "that site?",
     ["The first stimulus can still reverse the polarity of the membrane.",
      "K⁺ cannot diffuse out, so the resting potential is not promptly restored.",
      "The fibre does not promptly become responsive to further stimulation.",
      "The rapid influx of Na⁺ on stimulation is prevented.",
      "The inner surface becomes negative again within a fraction of a second, as usual."]),
  ["(a) and (b) only", "(a), (b) and (c) only", "(c), (d) and (e) only", "(b), (c) and (e) only"], "B",
  "Role of K⁺ in restoring the resting potential",
  "NCERT: on stimulation the membrane becomes freely permeable to Na⁺, and the rapid influx reverses the polarity. "
  "This rise is extremely short-lived and is quickly followed by a rise in permeability to K⁺; within a fraction of a "
  "second K⁺ diffuses outside the membrane and restores the resting potential at the site of excitation, and the "
  "fibre becomes once more responsive to further stimulation. If the K⁺ step is blocked, the reversal still occurs "
  "but its prompt recovery and renewed responsiveness do not.",
  ["(a) true – Na⁺ channels unaffected", "(b) true", "(c) true", "(d) false", "(e) false – recovery needs K⁺ outflow"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A leaves out (c); C and D include statements (d) or (e), which contradict the stem or need the "
                   "blocked K⁺ step.",
  seconds=60)
ms_check("abc", ["(a) and (b) only", "(a), (b) and (c) only", "(c), (d) and (e) only", "(b), (c) and (e) only"], "B")

Z(NEU, "Nervous system divisions", "Advanced", "direct",
  "Which sequence correctly traces a command for a voluntary movement from the brain to a skeletal muscle of the leg?",
  ["Brain → spinal cord → afferent fibres of the autonomic neural system → skeletal muscle",
   "Brain → afferent fibres → spinal cord → skeletal muscle",
   "Spinal cord → brain → efferent fibres of the autonomic neural system → skeletal muscle",
   "Brain → spinal cord (CNS) → efferent fibres of the somatic neural system → neuromuscular junction of the skeletal "
   "muscle"], "D",
  "Pathway of a voluntary command",
  "NCERT: the CNS (brain and spinal cord) is the site of information processing and control, and the brain controls "
  "voluntary movements. Efferent fibres transmit regulatory impulses from the CNS to the peripheral tissues, and the "
  "somatic neural system relays impulses from the CNS to the skeletal muscles. The axon ends at a neuromuscular "
  "junction with the muscle fibre.",
  ["Brain (CNS) → spinal cord (CNS)", "Efferent, somatic fibres", "Neuromuscular junction → skeletal muscle"],
  R_NEU("human neural system; neuron"),
  why_others_wrong="Afferent fibres carry impulses towards the CNS, not away from it (A, B); the autonomic neural "
                   "system supplies involuntary organs and smooth muscles, not skeletal muscles (A, C).",
  seconds=45)

Z(NEU, "Neuron and nerves", "Advanced", "multi_statement",
  ms("Which of the following statements about neurons and nerve fibres are correct?",
     ["Multipolar neurons have one axon and two or more dendrites and are found in the cerebral cortex.",
      "Bipolar neurons have one axon and one dendrite and are found in the retina of the eye.",
      "Unipolar neurons have a cell body with one axon only and are found usually in the embryonic stage.",
      "In myelinated nerve fibres, the myelin sheath around the axon is formed by the neuroglia of the cerebral "
      "cortex.",
      "The gaps between two adjacent myelin sheaths are called synaptic clefts."]),
  ["(a) and (c) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only"], "C",
  "Types of neurons and nerve fibres",
  "NCERT: multipolar neurons (one axon, two or more dendrites) occur in the cerebral cortex; bipolar neurons (one "
  "axon, one dendrite) in the retina; unipolar neurons (cell body with one axon only) usually in the embryonic stage. "
  "Myelinated nerve fibres are enveloped by Schwann cells, which form a myelin sheath around the axon, and are found "
  "in the spinal and cranial nerves; the gaps between two adjacent myelin sheaths are called nodes of Ranvier. A "
  "synaptic cleft is the gap that may separate the pre- and post-synaptic membranes at a synapse.",
  ["(a) true", "(b) true", "(c) true", "(d) false – Schwann cells", "(e) false – nodes of Ranvier"],
  R_NEU("structure of a neuron"),
  why_others_wrong="A leaves out (b); B includes (e) and leaves out (a); D includes (d).",
  seconds=60)
ms_check("abc", ["(a) and (c) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only"],
         "C")

Z(NEU, "Nervous system divisions", "Advanced", "assertion_reason",
  ar("Information processed in one cerebral hemisphere can be shared with the other hemisphere.",
     "The left and right cerebral hemispheres are connected to each other by the pons."),
  ASSERTION_REASON, "C",
  "Connection between the cerebral hemispheres",
  "NCERT: a deep cleft divides the cerebrum into the left and right cerebral hemispheres, which are connected by a "
  "tract of nerve fibres called the corpus callosum. The pons, part of the hindbrain, consists of fibre tracts that "
  "interconnect different regions of the brain, but it is not the connection between the two hemispheres.",
  ["A true – via the corpus callosum", "R false – the connecting tract is the corpus callosum, not the pons"],
  R_NEU("forebrain; hindbrain"),
  why_others_wrong="A and B accept the pons as the inter-hemispheric connection; D rejects the true Assertion.",
  seconds=40)


PLAN = ROOT / "batches" / "plans" / f"{BATCH}_plan.json"
OUT = ROOT / "batches" / "parts" / f"{BATCH}_ZOO_p1.json"


def check_plan():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if s["subject"] == ZOO)
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, (have - planned, planned - have)
    assert len(QUESTIONS) == pkg["count"] == LAST_ID - FIRST_ID + 1
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_ZOO_{n:06d}" for n in range(FIRST_ID, LAST_ID + 1)]
    assert pkg["question_ids"] == [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]]
    assert pkg["output"] == f"batches/parts/{BATCH}_ZOO_p1.json"
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    for x in QUESTIONS:
        assert x["subtopic"] in subtopics[x["topic"]], (x["question_id"], x["subtopic"])


if __name__ == "__main__":
    check_plan()
    n = len(QUESTIONS)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert all(0.22 * n <= keys[k] <= 0.28 * n for k in LETTERS), keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    for f in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f] >= 0.08 * n, (f, fmts)
    assert 0.04 * n <= fmts["numerical"] <= 0.08 * n, fmts
    for x in QUESTIONS:
        if x["format"] == "numerical":
            assert "script:recompute" in x["verification"]["verified_by"], x["question_id"]
        else:
            assert "script:recompute" not in x["verification"]["verified_by"], x["question_id"]
    stems = [x["question_text"] for x in QUESTIONS]
    assert len(set(stems)) == n
    doc = {"schema_version": "1.0", "batch_id": BATCH, "created_at": TODAY,
           "notes": "BATCH_006 package ZOO_006_p1: 122 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "facts already tested in BATCH_000-BATCH_005; every numerical answer re-derived by "
                    "tools/batch_006/ZOO_006_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
