"""Writes batches/parts/BATCH_001_ZOO_p1.json: package ZOO_001_p1 of BATCH_001 (Zoology, 122 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_000006 .. NEET_ZOO_000127. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11 Biology
textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion).

    python docs/neet-bank/tools/batch_001/ZOO_001_p1.py
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
TODAY = "2026-11-16"
LETTERS = "ABCD"
ZOO = "Zoology"
FIRST_ID, LAST_ID = 6, 127
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
    import re
    sets = []
    for o in options:
        letters = re.findall(r"\(([a-e])\)", o)
        sets.append("".join(sorted(letters)))
    assert sets[LETTERS.index(answer)] == "".join(sorted(truth)), (sets, truth)
    assert sets.count("".join(sorted(truth))) == 1


# ---------------------------------------------------------------- verification of computable answers
# Biomolecules: carbonic anhydrase. Uncatalysed 200 H2CO3 per hour; catalysed 600,000 per second.
CA_FOLD = F(600_000 * 3600, 200)
assert CA_FOLD == 10_800_000                      # 1.08 x 10^7, "about 10 million times"
assert F(600_000, 200) == 3000                    # distractor: hour not converted to seconds
assert F(600_000 * 60, 200) == 180_000            # distractor: hour taken as 60 s

# Breathing: volumes TV 500, IRV 3000, ERV 1100, RV 1200 (mL). Expiratory capacity = TV + ERV.
TV, IRV, ERV, RV = 500, 3000, 1100, 1200
assert TV + ERV == 1600                           # EC
assert ERV + RV == 2300 and TV + IRV == 3500 and TV + IRV + ERV == 4600   # FRC, IC, VC distractors

# Breathing: 5 mL O2 delivered per 100 mL blood; 5 L of blood through the tissues per minute.
O2_PER_MIN = F(5000, 100) * 5
assert O2_PER_MIN == 250
assert F(5000, 100) * 4 == 200                    # distractor: the 4 mL CO2 figure used instead

# Body fluids: cardiac cycle duration at 75 beats per minute.
assert F(60, 75) == F(4, 5)                       # 0.8 s
assert F(75, 60) == F(5, 4)                       # distractor: inverted ratio, 1.25 s

# Body fluids: rise in cardiac output from rest (70 mL x 72/min) to exercise (80 mL x 90/min).
CO_REST, CO_EX = 70 * 72, 80 * 90
assert (CO_REST, CO_EX, CO_EX - CO_REST) == (5040, 7200, 2160)
assert (90 - 72) * 70 == 1260                     # distractor: stroke-volume change ignored

# Excretion: GFR 125 mL/min, 99% of the filtrate reabsorbed -> urine per day.
FILTRATE_L = F(125 * 60 * 24, 1000)
assert FILTRATE_L == 180
URINE_L = FILTRATE_L * F(1, 100)
assert URINE_L == F(9, 5)                         # 1.8 L

# Locomotion: appendicular skeleton = 4 limbs x 30 + pectoral girdles (2 x 2) + pelvic girdle (2 coxal bones).
APPENDICULAR = 4 * 30 + 2 * 2 + 2
assert APPENDICULAR == 126
assert 4 * 30 + 2 * 2 + 2 * 3 == 130              # distractor: ilium, ischium, pubis counted separately

# Neural: Na-K pump, 3 Na+ out and 2 K+ in per cycle; net positive charges moved out in 150 cycles.
assert 150 * (3 - 2) == 150 and 150 * 3 == 450 and 150 * (3 + 2) == 750 and 150 * 2 == 300

# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Basis of classification", "Basic", "direct",
  "Animals whose cells are arranged as loose cell aggregates, showing the cellular level of organisation, belong to:",
  ["Porifera", "Coelenterata", "Platyhelminthes", "Annelida"], "A",
  "Levels of organisation",
  "Sponges (Porifera) show the cellular level: their cells form loose aggregates and do not form true tissues. "
  "Coelenterates show the tissue level, and Platyhelminthes and higher groups show organ and organ-system levels.",
  ["Cellular level → sponges (Porifera)", "Tissue level → coelenterates",
   "Organ / organ-system level → Platyhelminthes, annelids and higher phyla"],
  R_AK("basis of classification: levels of organisation"),
  why_others_wrong="Coelenterates already have tissues; flatworms and annelids have organs and organ systems.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Eight external rows of ciliated comb plates that help in locomotion are characteristic of:",
  ["Coelenterata", "Ctenophora", "Porifera", "Echinodermata"], "B",
  "Diagnostic feature of Ctenophora",
  "Ctenophores (comb jellies or sea walnuts, e.g. Pleurobrachia, Ctenoplana) swim with eight external rows of "
  "ciliated comb plates. They also show bioluminescence.",
  ["Comb plates → Ctenophora", "Cnidoblasts → Coelenterata", "Water canal system → Porifera",
   "Water vascular system → Echinodermata"],
  R_AK("Phylum Ctenophora"), seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Which of the following animals is a pseudocoelomate?",
  ["Taenia", "Pheretima", "Ancylostoma", "Pila"], "C",
  "Body cavity in different phyla",
  "Aschelminthes (roundworms) have a body cavity not lined by mesoderm; mesoderm is present as scattered pouches "
  "between ectoderm and endoderm. Ancylostoma (hookworm) is an aschelminth.",
  ["Ancylostoma → Aschelminthes → pseudocoelomate", "Taenia → Platyhelminthes → acoelomate",
   "Pheretima (Annelida) and Pila (Mollusca) → true coelomates"],
  R_AK("basis of classification: coelom; Phylum Aschelminthes"), seconds=30)

Z(AK, "Chordate classes", "Basic", "direct",
  "Air sacs connected to the lungs supplement respiration in members of class:",
  ["Reptilia", "Mammalia", "Amphibia", "Aves"], "D",
  "Respiratory features of birds",
  "In birds, respiration is by lungs, and air sacs connected to the lungs supplement it.",
  ["Aves → lungs plus air sacs", "Mammals, reptiles → lungs only", "Amphibians → gills, lungs and skin"],
  R_AK("Class Aves"), seconds=25)

Z(AK, "Chordate classes", "Basic", "statement_pair",
  sp("In cartilaginous fishes, the teeth are modified placoid scales which are backwardly directed.",
     "In cartilaginous fishes, the gill slits are covered by an operculum."),
  STATEMENT_PAIR, "C",
  "Features of Chondrichthyes",
  "Chondrichthyes have placoid scales, and their teeth are modified placoid scales pointing backwards: Statement I "
  "is true. Their gill slits are separate and without an operculum (gill cover); the operculum is a feature of bony "
  "fishes (Osteichthyes): Statement II is false.",
  ["Teeth = modified placoid scales, backwardly directed → I true",
   "Gill slits separate, no operculum in Chondrichthyes → II false"],
  R_AK("Class Chondrichthyes"), seconds=35)

Z(AK, "Chordate classes", "Basic", "direct",
  "Mammals are viviparous with a few exceptions. Which of the following mammals lays eggs?",
  ["Macropus", "Pteropus", "Delphinus", "Ornithorhynchus"], "D",
  "Oviparous mammal",
  "Ornithorhynchus (platypus) is the oviparous (egg-laying) mammal that NCERT lists. Macropus (kangaroo), Pteropus "
  "(flying fox) and Delphinus (common dolphin) are viviparous.",
  ["Mammals: viviparous with few exceptions", "Exception (oviparous) → Ornithorhynchus, the platypus"],
  R_AK("Class Mammalia"), seconds=25)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("mollusc", "common name"), ["Pinctada", "Aplysia", "Dentalium", "Chaetopleura"],
     ["Chiton", "Tusk shell", "Sea hare", "Pearl oyster"]),
  match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                 {"A": "II", "B": "III", "C": "IV", "D": "I"}], at="A"),
  "A",
  "Examples of Mollusca",
  "NCERT lists these molluscs with their common names.",
  ["Pinctada → pearl oyster (IV)", "Aplysia → sea hare (III)", "Dentalium → tusk shell (II)",
   "Chaetopleura → chiton (I)"],
  R_AK("Phylum Mollusca"),
  why_others_wrong="The other codes swap pearl oyster with sea hare or tusk shell with chiton.", seconds=40)

Z(AK, "Chordate classes", "Intermediate", "assertion_reason",
  ar("Sharks have an air bladder that keeps them afloat without swimming.",
     "The endoskeleton of members of Chondrichthyes is cartilaginous."),
  ASSERTION_REASON, "D",
  "Buoyancy in cartilaginous fishes",
  "Chondrichthyes such as sharks have no air bladder, so they have to swim constantly to avoid sinking: A is false. "
  "Their endoskeleton is cartilaginous: R is true.",
  ["Air bladder absent in Chondrichthyes (present in Osteichthyes) → A false",
   "Cartilaginous endoskeleton → R true"],
  R_AK("Class Chondrichthyes"),
  why_others_wrong="Options A and B need A to be true; the air bladder belongs to bony fishes.", seconds=40)

_o = ["(a), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"]
ms_check("abd", _o, "B")
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements about Echinodermata are correct?",
     ["They have an endoskeleton of calcareous ossicles.",
      "They have a water vascular system that helps in locomotion, capture and transport of food, and respiration.",
      "Adult echinoderms are bilaterally symmetrical.",
      "Their larvae are bilaterally symmetrical.",
      "Most of them live in fresh water."]),
  _o, "B",
  "Characters of Echinodermata",
  "Echinoderms are spiny-bodied animals with an endoskeleton of calcareous ossicles and a water vascular system. "
  "All are marine. The adult is radially symmetrical while the larva is bilaterally symmetrical.",
  ["(a) True: calcareous ossicles", "(b) True: water vascular system", "(c) False: adults are radially symmetrical",
   "(d) True: larvae are bilaterally symmetrical", "(e) False: all echinoderms are marine"],
  R_AK("Phylum Echinodermata"), seconds=50)

Z(AK, "Basis of classification", "Intermediate", "direct",
  "Animals that are triploblastic but have no body cavity between the body wall and the gut wall are found in "
  "phylum:",
  ["Aschelminthes", "Annelida", "Platyhelminthes", "Ctenophora"], "C",
  "Germ layers and coelom together",
  "Two criteria must both fit: three germ layers (triploblastic) and no body cavity (acoelomate). Platyhelminthes "
  "are triploblastic acoelomates.",
  ["Ctenophora → diploblastic, so ruled out", "Aschelminthes → triploblastic but pseudocoelomate",
   "Annelida → triploblastic, true coelom", "Platyhelminthes → triploblastic and acoelomate"],
  R_AK("basis of classification: diploblastic and triploblastic organisation; coelom"),
  why_others_wrong="Aschelminthes have a pseudocoelom and annelids a true coelom; ctenophores are diploblastic.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("In Urochordata, the notochord is present only in the larval tail.",
     "In Cephalochordata, the notochord extends from head to tail and persists throughout life."),
  STATEMENT_PAIR, "A",
  "Protochordates: position and persistence of the notochord",
  "Urochordates (e.g. Ascidia, Salpa, Doliolum) have a notochord only in the larval tail. Cephalochordates (e.g. "
  "Branchiostoma, Amphioxus) have it from head to tail throughout life. Both statements are true.",
  ["Urochordata → notochord only in larval tail → I true",
   "Cephalochordata → head to tail, throughout life → II true"],
  R_AK("Phylum Chordata: Urochordata and Cephalochordata"), seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "In Balanoglossus, a worm-like marine animal with a body of proboscis, collar and trunk, the excretory organ is "
  "the:",
  ["Flame cell", "Proboscis gland", "Nephridium", "Malpighian tubule"], "B",
  "Excretion in Hemichordata",
  "Hemichordates such as Balanoglossus and Saccoglossus excrete through the proboscis gland. They respire through "
  "gills and have an open circulatory system.",
  ["Balanoglossus → Hemichordata", "Excretory organ of hemichordates → proboscis gland"],
  R_AK("Phylum Hemichordata"),
  why_others_wrong="Flame cells belong to flatworms, nephridia to annelids and Malpighian tubules to insects.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("insect genus", "description"), ["Apis", "Bombyx", "Laccifer", "Locusta"],
     ["Gregarious pest", "Lac insect", "Honey bee", "Silkworm"]),
  match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                 {"A": "III", "B": "IV", "C": "I", "D": "II"}], at="D"),
  "D",
  "Economically important arthropods",
  "NCERT groups arthropods by importance: economically important insects (Apis, Bombyx, Laccifer), vectors "
  "(Anopheles, Culex, Aedes) and a gregarious pest (Locusta).",
  ["Apis → honey bee (III)", "Bombyx → silkworm (IV)", "Laccifer → lac insect (II)",
   "Locusta → gregarious pest (I)"],
  R_AK("Phylum Arthropoda"), seconds=40)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("Aschelminthes are called roundworms because they are circular in cross-section.",
     "The body cavity of aschelminths is a true coelom lined by mesoderm."),
  ASSERTION_REASON, "C",
  "Body form and body cavity of Aschelminthes",
  "The body of aschelminths is circular in cross-section, hence the name roundworms: A is true. Their body cavity "
  "is a pseudocoelom, not lined by mesoderm (mesoderm lies as scattered pouches): R is false.",
  ["Circular in cross-section → roundworms → A true", "Pseudocoelomate, not coelomate → R false"],
  R_AK("Phylum Aschelminthes; basis of classification: coelom"), seconds=40)

_o = ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only", "(a), (b) and (d) only"]
ms_check("abd", _o, "D")
Z(AK, "Non-chordate phyla", "Advanced", "multi_statement",
  ms("Which of the following animals are correctly matched with their phylum?",
     ["Pleurobrachia – Ctenophora", "Gorgonia – Coelenterata", "Ophiura – Mollusca", "Limulus – Arthropoda",
      "Saccoglossus – Chordata"]),
  _o, "D",
  "Examples of animal phyla",
  "Pleurobrachia (a comb jelly) is a ctenophore, Gorgonia (sea-fan) a coelenterate and Limulus (king crab, a living "
  "fossil) an arthropod. Ophiura (brittle star) is an echinoderm, and Saccoglossus is a hemichordate, which is now "
  "placed as a separate phylum under non-chordates.",
  ["(a) True", "(b) True: sea-fan", "(c) False: brittle star → Echinodermata", "(d) True: king crab",
   "(e) False: Saccoglossus → Hemichordata"],
  R_AK("examples under each phylum"),
  why_others_wrong="Options with (c) or (e) fall for the brittle star (spiny skin, not a shell) or for hemichordates, "
                   "which were once a sub-phylum of Chordata.", seconds=60)

Z(AK, "Chordate classes", "Advanced", "statement_pair",
  sp("Cyclostomes have a sucking and circular mouth without jaws.",
     "Cyclostomes are freshwater animals that migrate to the sea for spawning."),
  STATEMENT_PAIR, "C",
  "Class Cyclostomata",
  "Cyclostomes (Petromyzon, Myxine) have a jawless, sucking, circular mouth: Statement I is true. They are marine "
  "but migrate to fresh water for spawning; they die after spawning, and the larvae return to the ocean after "
  "metamorphosis. Statement II reverses the direction, so it is false.",
  ["Jawless circular sucking mouth → I true", "Marine animals that spawn in fresh water → II false"],
  R_AK("Class Cyclostomata"),
  why_others_wrong="Students who remember 'migration for spawning' but not its direction mark both true.",
  seconds=45)

Z(AK, "Chordate classes", "Advanced", "direct",
  "Which of the following characters is shared by birds (Aves) and mammals?",
  ["Pneumatic long bones", "A four-chambered heart and homoiothermy", "Oviparity in all members",
   "Mammary glands"], "B",
  "Comparing chordate classes",
  "Both birds and mammals have a completely four-chambered heart and are warm-blooded (homoiothermous), able to "
  "maintain a constant body temperature.",
  ["Pneumatic bones → birds only", "Four-chambered heart + homoiothermy → both",
   "Oviparity in all → birds only (mammals are mostly viviparous)", "Mammary glands → mammals only"],
  R_AK("Class Aves; Class Mammalia"), seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "assertion_reason",
  ar("Hemichordata is now placed as a separate phylum under non-chordates.",
     "Hemichordates have an open circulatory system, and their excretory organ is the proboscis gland."),
  ASSERTION_REASON, "B",
  "Position of Hemichordata",
  "Hemichordata was earlier treated as a sub-phylum of Chordata and is now a separate phylum under non-chordates: A "
  "is true. Their circulation is open and the proboscis gland is the excretory organ: R is true. But these are "
  "general features of the phylum and say nothing about why it was moved out of Chordata.",
  ["A: earlier a chordate sub-phylum, now a non-chordate phylum → true",
   "R: open circulatory system, proboscis gland for excretion → true",
   "R does not address the classification change → R does not explain A"],
  R_AK("Phylum Hemichordata"),
  why_others_wrong="Option A is the trap: both statements are true, but R describes the animals, not their placement.",
  seconds=50)

Z(AK, "Chordate classes", "Advanced", "match_list",
  ml(("reptile genus", "common name"), ["Chelone", "Testudo", "Hemidactylus", "Calotes"],
     ["Garden lizard", "Tortoise", "Wall lizard", "Turtle"]),
  match_options({"A": "IV", "B": "II", "C": "III", "D": "I"},
                [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                 {"A": "II", "B": "IV", "C": "I", "D": "III"}], at="C"),
  "C",
  "Examples of Reptilia",
  "The trap is the two similar pairs: turtle vs tortoise and wall lizard vs garden lizard.",
  ["Chelone → turtle (IV)", "Testudo → tortoise (II)", "Hemidactylus → wall lizard (III)",
   "Calotes → garden lizard (I)"],
  R_AK("Class Reptilia"),
  why_others_wrong="Each wrong code swaps turtle with tortoise, wall lizard with garden lizard, or both.", seconds=45)

_o = ["(a), (c) and (d) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]
ms_check("acd", _o, "A")
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["Mammals have external ears or pinnae.",
      "In mammals, all the teeth in the jaw are of one type.",
      "In birds, the skin is dry and without glands except the oil gland at the base of the tail.",
      "Snakes and lizards shed their scales as skin cast.",
      "The skin of amphibians is covered with epidermal scales."]),
  _o, "A",
  "Skin and body-covering features of chordate classes",
  "Pinnae are a mammalian feature, and the only skin gland of birds is the oil gland at the base of the tail. Snakes "
  "and lizards shed scales as skin cast. Mammals have different types of teeth in the jaw, and amphibian skin is "
  "moist and without scales.",
  ["(a) True", "(b) False: different types of teeth are present in the mammalian jaw",
   "(c) True: oil gland at the base of the tail", "(d) True: skin cast",
   "(e) False: amphibians have moist skin without scales"],
  R_AK("Classes Amphibia, Reptilia, Aves and Mammalia"),
  why_others_wrong="(e) is the usual trap: scales belong to reptiles (epidermal scales or scutes) and fishes, not "
                   "to amphibians.", seconds=60)

# ================================================================ Structural Organisation in Animals (B4 I6 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Simple squamous epithelium, made of a single thin layer of flattened cells, is found in:",
  ["The lining of the stomach", "The walls of blood vessels and air sacs of lungs", "The ducts of glands",
   "The inner surface of bronchioles"], "B",
  "Types of simple epithelium",
  "Squamous epithelium has flattened cells with irregular boundaries and forms thin linings where diffusion is "
  "important, such as the walls of blood vessels and the air sacs (alveoli) of lungs.",
  ["Squamous → walls of blood vessels, air sacs of lungs", "Columnar → lining of stomach and intestine",
   "Cuboidal → ducts of glands, tubular parts of nephrons", "Ciliated → bronchioles, fallopian tubes"],
  R_SOA("animal tissues: epithelial tissue"), seconds=25)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Goblet cells of the alimentary canal are an example of:",
  ["A multicellular exocrine gland", "Unicellular glandular epithelium", "An endocrine gland",
   "Compound epithelium"], "B",
  "Glandular epithelium",
  "Some columnar or cuboidal cells become specialised for secretion (glandular epithelium). A gland may be "
  "unicellular, made of isolated glandular cells such as the goblet cells of the alimentary canal, or multicellular, "
  "such as the salivary gland.",
  ["Goblet cell = single secretory cell → unicellular gland", "Salivary gland → multicellular example"],
  R_SOA("animal tissues: glandular epithelium"), seconds=25)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "Which features help to distinguish a male frog from a female frog?",
  ["Vocal sacs and a copulatory pad on the first digit of the forelimbs",
   "Webbed hind limbs and a nictitating membrane",
   "A tympanum on each side of the head and bulged eyes",
   "Moist slimy skin and dorsal green colour"], "A",
  "Sexual dimorphism in frog",
  "Male frogs have sound-producing vocal sacs and a copulatory pad on the first digit of the forelimbs. These are "
  "absent in female frogs.",
  ["Male only → vocal sacs, copulatory pad", "The other features are present in both sexes"],
  R_SOA("frog: morphology"), seconds=25)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Tendons attach skeletal muscles to bones.", "Ligaments attach one bone to another bone."),
  STATEMENT_PAIR, "A",
  "Dense regular connective tissue",
  "Tendons and ligaments are dense regular connective tissue, with collagen fibres in rows between parallel bundles "
  "of fibres. Tendons attach skeletal muscles to bones and ligaments attach one bone to another. Both are true.",
  ["Tendon: muscle → bone (I true)", "Ligament: bone → bone (II true)"],
  R_SOA("animal tissues: dense connective tissue"), seconds=25)

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("epithelium", "location"),
     ["Ciliated epithelium", "Compound epithelium", "Cuboidal epithelium", "Columnar epithelium"],
     ["Lining of stomach and intestine", "Inner surface of fallopian tubes", "Tubular parts of nephrons",
      "Moist surface of buccal cavity"]),
  match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "I", "B": "IV", "C": "III", "D": "II"},
                 {"A": "IV", "B": "II", "C": "I", "D": "III"}], at="B"),
  "B",
  "Location of epithelia",
  "Each epithelium lines the surface whose function it suits.",
  ["Ciliated → inner surface of bronchioles and fallopian tubes (II)",
   "Compound → moist surface of buccal cavity, pharynx, dry surface of skin (IV)",
   "Cuboidal → ducts of glands and tubular parts of nephrons (III)",
   "Columnar → lining of stomach and intestine (I)"],
  R_SOA("animal tissues: epithelial tissue"), seconds=40)

Z(SOA, "Animal tissues", "Intermediate", "assertion_reason",
  ar("Compound epithelium has a limited role in secretion and absorption.",
     "Compound epithelium is made of more than one layer of cells."),
  ASSERTION_REASON, "A",
  "Structure decides function in compound epithelium",
  "Because compound epithelium is multi-layered, substances cannot easily pass across it, so it has only a limited "
  "role in secretion and absorption. Its main function is protection against chemical and mechanical stresses. R is "
  "the reason for A.",
  ["Multi-layered → R true", "Multi-layered → poor secretion/absorption → A true and explained by R"],
  R_SOA("animal tissues: compound epithelium"), seconds=40)

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "Exocrine glands secrete all of the following EXCEPT:",
  ["Mucus", "Earwax", "Hormones", "Milk"], "C",
  "Exocrine versus endocrine glands",
  "Exocrine glands release mucus, saliva, earwax, oil, milk, digestive enzymes and other cell products through ducts. "
  "Endocrine glands have no ducts and secrete hormones directly into the fluid bathing the gland.",
  ["Mucus, earwax, milk → exocrine (through ducts)", "Hormones → endocrine (ductless)"],
  R_SOA("animal tissues: glandular epithelium"), seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "statement_pair",
  sp("Cartilage cells (chondrocytes) are enclosed in small cavities within the matrix secreted by them.",
     "Bone has a soft and pliable ground substance that is poor in calcium salts."),
  STATEMENT_PAIR, "C",
  "Cartilage and bone",
  "In cartilage, the chondrocytes lie in small cavities in the matrix they secrete: Statement I is true. Bone has a "
  "hard and non-pliable ground substance rich in calcium salts and collagen fibres, which gives it strength: "
  "Statement II is false. (Cartilage, not bone, has a pliable matrix.)",
  ["Chondrocytes in cavities (lacunae) → I true", "Bone matrix hard, non-pliable, rich in calcium salts → II false"],
  R_SOA("animal tissues: specialised connective tissue"), seconds=35)

_o = ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (d) only", "(a), (c), (d) and (e) only"]
ms_check("acd", _o, "C")
Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the frog are correct?",
     ["Frogs never drink water but absorb it through the skin.",
      "A frog has a distinct neck and a short tail.",
      "The forelimbs end in four digits and the hind limbs end in five digits.",
      "In water, the skin acts as an aquatic respiratory organ.",
      "The frog is a warm-blooded animal."]),
  _o, "C",
  "Morphology and physiology of frog",
  "The frog absorbs water through its skin and uses the skin for respiration in water (cutaneous respiration). Its "
  "forelimbs end in four digits and the larger hind limbs in five. Its body is divided into head and trunk only, and "
  "it is cold-blooded (poikilotherm).",
  ["(a) True", "(b) False: neck and tail are absent", "(c) True", "(d) True: cutaneous respiration",
   "(e) False: frogs are cold-blooded"],
  R_SOA("frog: morphology and anatomy"), seconds=50)

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "Adipose tissue, which stores fats and is located mainly beneath the skin, is a type of:",
  ["Dense regular connective tissue", "Dense irregular connective tissue", "Specialised connective tissue",
   "Loose connective tissue"], "D",
  "Classification of connective tissue",
  "NCERT classifies connective tissue as loose, dense and specialised. Loose connective tissue includes areolar "
  "tissue and adipose tissue. Adipose cells store fats; excess nutrients are converted into fat and stored here.",
  ["Loose connective tissue → areolar and adipose", "Dense regular → tendons, ligaments; dense irregular → skin",
   "Specialised → cartilage, bone, blood"],
  R_SOA("animal tissues: loose connective tissue"), seconds=30)

_o = ["(a) and (c) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only", "(a), (b) and (d) only"]
ms_check("abd", _o, "D")
Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("Which of the following statements about muscle tissue are correct?",
     ["Smooth muscle fibres taper at both ends and do not show striations.",
      "Cardiac muscle cells have communication junctions (intercalated discs) that allow the cells to contract as "
      "a unit.",
      "Skeletal muscle fibres are involuntary.",
      "Smooth muscle is found in the walls of blood vessels, stomach and intestine.",
      "Cardiac muscle tissue is found in the heart and in the walls of large arteries."]),
  _o, "D",
  "Three types of muscle tissue",
  "Smooth muscle fibres are fusiform and unstriated, and line the walls of internal organs such as blood vessels, "
  "stomach and intestine. Cardiac muscle is present only in the heart; intercalated discs let its cells contract as "
  "a unit. Skeletal muscle is attached to bones and is voluntary.",
  ["(a) True", "(b) True", "(c) False: skeletal muscle is voluntary", "(d) True",
   "(e) False: cardiac muscle is present only in the heart; artery walls have smooth muscle"],
  R_SOA("animal tissues: muscle tissue"), seconds=55)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "assertion_reason",
  ar("In female frogs, the ureters act as urinogenital ducts.",
     "In male frogs, the vasa efferentia from the testes enter the kidneys and communicate with the urinogenital "
     "duct that opens into the cloaca."),
  ASSERTION_REASON, "D",
  "Urinogenital system of frog",
  "In male frogs, the ureters carry both urine and sperms (urinogenital ducts), because the 10–12 vasa efferentia "
  "from the testes enter the kidneys and reach the urinogenital duct. In female frogs, the ureters and oviducts open "
  "separately into the cloaca. So A is false and R is true.",
  ["Female frog: ureters and oviducts separate → A false",
   "Male frog: vasa efferentia → kidney → urinogenital duct → cloaca → R true"],
  R_SOA("frog: anatomy, excretory and reproductive systems"),
  why_others_wrong="A applies the male arrangement to the female, which is the trap.", seconds=50)

Z(SOA, "Animal tissues", "Advanced", "statement_pair",
  sp("Tight junctions help to stop substances from leaking across a tissue.",
     "Gap junctions perform cementing to keep neighbouring cells together."),
  STATEMENT_PAIR, "C",
  "Cell junctions in epithelium",
  "Tight junctions stop substances from leaking across a tissue: Statement I is true. Cementing that keeps "
  "neighbouring cells together is done by adhering junctions; gap junctions connect the cytoplasm of adjoining cells "
  "for rapid transfer of ions, small molecules and sometimes big molecules: Statement II is false.",
  ["Tight → prevent leakage (I true)", "Adhering → cementing; gap → cytoplasmic communication (II false)"],
  R_SOA("animal tissues: cell junctions"),
  why_others_wrong="Statement II gives the gap junction the function of the adhering junction.", seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "direct",
  "Which of the following statements about the frog is correct?",
  ["Its RBCs are nucleated and contain haemoglobin.", "Twelve pairs of cranial nerves arise from its brain.",
   "Its heart has two atria and two ventricles.", "It excretes nitrogenous wastes mainly as uric acid."], "A",
  "Anatomy of frog",
  "Frog blood has nucleated RBCs containing the red pigment haemoglobin. Ten pairs of cranial nerves arise from its "
  "brain. The heart has three chambers (two atria and one ventricle), and the frog is ureotelic.",
  ["RBCs nucleated → correct", "Cranial nerves: 10 pairs, not 12", "Heart: 2 atria + 1 ventricle",
   "Frog is ureotelic, excreting urea"],
  R_SOA("frog: anatomy (circulatory, neural and excretory systems)"),
  why_others_wrong="The frog has ten pairs of cranial nerves, a three-chambered heart and is ureotelic; the other "
                   "options change one of these numbers or terms.", seconds=40)

# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "The most abundant protein in the animal world is:",
  ["RuBisCO", "Haemoglobin", "Collagen", "Insulin"], "C",
  "Abundant proteins",
  "Collagen is the most abundant protein in the animal world. RuBisCO (ribulose bisphosphate "
  "carboxylase-oxygenase) is the most abundant protein in the whole biosphere.",
  ["Animal world → collagen", "Whole biosphere → RuBisCO"],
  R_BIO("proteins"),
  why_others_wrong="RuBisCO is the trap: it is the most abundant in the biosphere, not in the animal world.",
  seconds=20)

Z(BIO, "Carbohydrates and lipids", "Basic", "direct",
  "Inulin is a polysaccharide made up of units of:",
  ["Glucose", "Galactose", "Ribose", "Fructose"], "D",
  "Homopolymers of monosaccharides",
  "Cellulose, starch and glycogen are polymers of glucose, while inulin is a polymer of fructose.",
  ["Inulin → fructose", "Cellulose, starch, glycogen → glucose"],
  R_BIO("polysaccharides"), seconds=20)

Z(BIO, "Nucleic acids", "Basic", "direct",
  "A nucleoside differs from a nucleotide in lacking a:",
  ["Pentose sugar", "Nitrogen base", "Phosphate group", "Pentose sugar and a phosphate group"], "C",
  "Nucleosides and nucleotides",
  "A nitrogen base attached to a sugar is a nucleoside (e.g. adenosine). When a phosphate group is also esterified "
  "to the sugar, it becomes a nucleotide (e.g. adenylic acid).",
  ["Nucleoside = base + sugar", "Nucleotide = base + sugar + phosphate", "Difference → phosphate group"],
  R_BIO("biomacromolecules: nucleic acids and their building blocks"), seconds=25)

Z(BIO, "Enzyme classification", "Basic", "statement_pair",
  sp("Isomerases catalyse the linking together of two compounds.",
     "Hydrolases catalyse the hydrolysis of ester, ether, peptide, glycosidic, C–C, C–halide or P–N bonds."),
  STATEMENT_PAIR, "D",
  "Classes of enzymes",
  "Isomerases catalyse inter-conversion of optical, geometric or positional isomers; linking two compounds together "
  "is done by ligases: Statement I is false. Statement II is the NCERT description of hydrolases: true.",
  ["Joining two compounds → ligases, not isomerases (I false)", "Hydrolases → hydrolysis of these bonds (II true)"],
  R_BIO("enzymes: classification and nomenclature"), seconds=30)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "Some nucleic acids behave like enzymes. These are called:",
  ["Coenzymes", "Ribozymes", "Apoenzymes", "Cofactors"], "B",
  "Nature of enzymes",
  "Almost all enzymes are proteins, but some nucleic acids act as catalysts. These catalytic nucleic acids are "
  "called ribozymes.",
  ["Enzymes → mostly proteins", "Catalytic nucleic acids → ribozymes"],
  R_BIO("enzymes"), seconds=20)

Z(BIO, "Proteins and amino acids", "Intermediate", "match_list",
  ml(("protein", "function"), ["Collagen", "Trypsin", "GLUT-4", "Antibody"],
     ["Fights infectious agents", "Intercellular ground substance", "Enables glucose transport into cells",
      "Enzyme"]),
  match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
                 {"A": "II", "B": "III", "C": "IV", "D": "I"}], at="C"),
  "C",
  "Functions of proteins",
  "Proteins carry out many functions: some transport nutrients across membranes, some fight infections, some are "
  "hormones and some are enzymes. NCERT tabulates these examples.",
  ["Collagen → intercellular ground substance (II)", "Trypsin → enzyme (IV)",
   "GLUT-4 → enables glucose transport into cells (III)", "Antibody → fights infectious agents (I)"],
  R_BIO("proteins: some proteins and their functions"),
  why_others_wrong="Wrong codes give collagen the enzyme role or swap GLUT-4 with antibody.", seconds=40)

Z(BIO, "Proteins and amino acids", "Intermediate", "assertion_reason",
  ar("Haemoglobin shows a quaternary structure.",
     "Adult human haemoglobin consists of four subunits: two of α type and two of β type."),
  ASSERTION_REASON, "A",
  "Levels of protein structure",
  "A protein has quaternary structure when it is an assembly of more than one polypeptide (subunit). Adult human "
  "haemoglobin has four subunits, 2α and 2β, so R is exactly why A is true.",
  ["Quaternary structure = arrangement of several polypeptide subunits",
   "Hb = 2α + 2β subunits → quaternary → R explains A"],
  R_BIO("structure of proteins"), seconds=35)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "direct",
  "Lipids have molecular weights below 800 Da, yet they appear in the acid-insoluble fraction when a tissue is "
  "ground in trichloroacetic acid. This is because:",
  ["Their molecular weight exceeds 10,000 Da once they bind glycerol",
   "On grinding, cell membranes break into pieces and form vesicles that are not water-soluble",
   "They are polymers of fatty acids linked by peptide bonds",
   "Trichloroacetic acid converts them into proteins"], "B",
  "Acid-soluble and acid-insoluble pools",
  "Lipids are not strictly macromolecules. They come into the acid-insoluble fraction because, when the tissue is "
  "ground, the membranes (made largely of lipids) break into pieces and form vesicles that are not water-soluble, so "
  "they separate with the macromolecules.",
  ["Lipids: molecular weight < 800 Da → not macromolecules",
   "Grinding → membranes → water-insoluble vesicles → retained in the acid-insoluble fraction"],
  R_BIO("biomacromolecules: acid-insoluble fraction"), seconds=40)

_o = ["(a), (b) and (c) only", "(a), (b), (d) and (e) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]
ms_check("abde", _o, "B")
Z(BIO, "Carbohydrates and lipids", "Intermediate", "multi_statement",
  ms("Which of the following statements about polysaccharides are correct?",
     ["Cellulose is a homopolymer of glucose.",
      "Starch can hold I₂ molecules in its helical portion and gives a blue colour.",
      "Cellulose gives a blue colour with iodine.",
      "In a polysaccharide chain such as glycogen, the right end is the reducing end and the left end is the "
      "non-reducing end.",
      "The exoskeleton of arthropods contains the complex polysaccharide chitin."]),
  _o, "B",
  "Structure of polysaccharides",
  "Starch forms helical secondary structures that hold I₂ (starch–I₂ is blue). Cellulose lacks such complex helices, "
  "so it cannot hold I₂. Chitin, found in arthropod exoskeletons, is a complex polysaccharide.",
  ["(a) True", "(b) True", "(c) False: cellulose has no complex helices to hold I₂", "(d) True", "(e) True"],
  R_BIO("polysaccharides"), seconds=50)

Z(BIO, "Proteins and amino acids", "Intermediate", "statement_pair",
  sp("Amino acids are substituted methanes.", "In glycine, the R group is a methyl group."),
  STATEMENT_PAIR, "C",
  "Structure of amino acids",
  "In an amino acid, the α-carbon carries four substituents: hydrogen, a carboxyl group, an amino group and a "
  "variable R group, so amino acids are substituted methanes: Statement I is true. In glycine the R group is a "
  "hydrogen; a methyl group is the R group of alanine: Statement II is false.",
  ["α-carbon with H, –COOH, –NH₂ and R → substituted methane (I true)",
   "Glycine: R = H; alanine: R = CH₃; serine: R = hydroxymethyl (II false)"],
  R_BIO("biomacromolecules: amino acids"), seconds=30)

Z(BIO, "Enzymes: properties and action", "Intermediate", "direct",
  "Malonate inhibits the enzyme succinic dehydrogenase because malonate:",
  ["Closely resembles the substrate succinate in structure and competes for the substrate-binding site",
   "Denatures the enzyme protein permanently",
   "Removes the metal ion cofactor of the enzyme",
   "Raises the activation energy of the uncatalysed reaction"], "A",
  "Competitive inhibition",
  "A competitive inhibitor closely resembles the substrate in molecular structure. It competes with the substrate "
  "for the substrate-binding site, so the substrate cannot bind and enzyme action declines. Malonate inhibiting "
  "succinic dehydrogenase is the NCERT example.",
  ["Inhibitor resembles substrate → binds the active site", "Substrate blocked → reaction slows"],
  R_BIO("enzymes: factors affecting enzyme activity (inhibitors)"), seconds=35)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("Low temperature preserves an enzyme in a temporarily inactive state.",
     "High temperature destroys enzymatic activity because proteins are denatured by heat."),
  STATEMENT_PAIR, "A",
  "Effect of temperature on enzymes",
  "Each enzyme works best at its optimum temperature. Below it the enzyme is only temporarily inactive and recovers "
  "on warming; well above it the protein is denatured and activity is destroyed. Both statements are true.",
  ["Low temperature → reversible inactivity (I true)", "High temperature → denaturation (II true)"],
  R_BIO("enzymes: factors affecting enzyme activity"), seconds=30)

Z(BIO, "Enzymes: properties and action", "Advanced", "numerical",
  "Without an enzyme, about 200 molecules of H₂CO₃ are formed from CO₂ and H₂O in one hour. In the presence of "
  "carbonic anhydrase, about 600,000 molecules are formed every second. By roughly what factor has the enzyme "
  "increased the rate of the reaction?",
  ["3.0 × 10³", "1.8 × 10⁵", "0.83", "1.08 × 10⁷"], "D",
  "Rate enhancement by enzymes",
  "Compare both rates in the same unit of time before dividing.",
  ["Uncatalysed: 200 molecules per hour",
   "Catalysed: 600,000 per second × 3600 s = 2.16 × 10⁹ molecules per hour",
   "Factor = 2.16 × 10⁹ / 200 = 1.08 × 10⁷ (NCERT: about 10 million times)"],
  R_BIO("enzymes: chemical reactions and carbonic anhydrase"),
  shortcut="600,000 / 200 = 3000 per unit time; × 3600 for hours → seconds = 1.08 × 10⁷.",
  why_others_wrong="3.0 × 10³ divides without converting the hour into seconds. 1.8 × 10⁵ takes an hour as 60 "
                   "seconds. 0.83 divides the rates the wrong way round.",
  seconds=75, verified_by=RECOMPUTED)

Z(BIO, "Enzyme classification", "Advanced", "match_list",
  ml(("class of enzyme", "reaction catalysed"), ["Oxidoreductases", "Transferases", "Lyases", "Ligases"],
     ["Removal of groups from substrates by mechanisms other than hydrolysis, leaving double bonds",
      "Linking together of two compounds, e.g. joining C–O, C–S, C–N or P–O bonds",
      "Transfer of a group G (other than hydrogen) between a pair of substrates",
      "Oxidation-reduction between two substrates"]),
  match_options({"A": "IV", "B": "III", "C": "I", "D": "II"},
                [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                 {"A": "IV", "B": "I", "C": "III", "D": "II"}], at="A"),
  "A",
  "Six classes of enzymes",
  "Read each List-II description for its key words: 'oxidation-reduction', 'transfer of a group', 'removal ... "
  "leaving double bonds', 'linking together of two compounds'.",
  ["Oxidoreductases/dehydrogenases → oxidation-reduction (IV)", "Transferases → group transfer (III)",
   "Lyases → removal of groups leaving double bonds (I)", "Ligases → joining two compounds (II)"],
  R_BIO("enzymes: classification and nomenclature"),
  why_others_wrong="The usual error is to swap lyases (which remove groups) with ligases (which join compounds).",
  seconds=55)

_o = ["(a), (b) and (c) only", "(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"]
ms_check("abc", _o, "A")
Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("Which of the following statements about co-factors are correct?",
     ["Haem is the prosthetic group in the enzymes peroxidase and catalase.",
      "The co-enzymes NAD and NADP contain the vitamin niacin.",
      "Zinc is a co-factor for the proteolytic enzyme carboxypeptidase.",
      "Co-enzymes are permanently and tightly bound to the apoenzyme.",
      "Removal of the co-factor does not affect the catalytic activity of the enzyme."]),
  _o, "A",
  "Co-factors: prosthetic groups, co-enzymes and metal ions",
  "Prosthetic groups (such as haem) are tightly bound to the apoenzyme. Co-enzymes are bound only transiently, "
  "usually during catalysis, and many contain vitamins. Some enzymes need metal ions (e.g. zinc for "
  "carboxypeptidase). When the co-factor is removed, catalytic activity is lost.",
  ["(a) True", "(b) True", "(c) True", "(d) False: co-enzyme binding is transient",
   "(e) False: activity is lost without the co-factor"],
  R_BIO("enzymes: co-factors"),
  why_others_wrong="(d) gives co-enzymes the tight binding that defines prosthetic groups.", seconds=55)

Z(BIO, "Proteins and amino acids", "Advanced", "assertion_reason",
  ar("In proteins, only right-handed helices are observed.",
     "The primary structure of a protein is the sequence of amino acids in it."),
  ASSERTION_REASON, "B",
  "Primary and secondary structure of proteins",
  "NCERT states that the protein thread may be folded as a helix and that only right-handed helices are seen in "
  "proteins: A is true. The primary structure is the amino acid sequence: R is true. But the definition of primary "
  "structure says nothing about the handedness of the helix, so R does not explain A.",
  ["A: secondary structure, right-handed helices only → true",
   "R: primary structure = amino acid sequence → true", "R is about a different level of structure → not the reason"],
  R_BIO("structure of proteins"), seconds=40)

Z(BIO, "Proteins and amino acids", "Advanced", "direct",
  "Which of the following amino acids is correctly matched with its nature?",
  ["Glutamic acid – basic", "Lysine – basic", "Valine – aromatic", "Tryptophan – acidic"], "B",
  "Classification of amino acids by the R group",
  "The R group decides the nature of an amino acid. NCERT gives: acidic – glutamic acid; basic – lysine; neutral – "
  "valine; aromatic – tyrosine, phenylalanine, tryptophan.",
  ["Glutamic acid → acidic", "Lysine → basic ✓", "Valine → neutral", "Tryptophan → aromatic"],
  R_BIO("biomacromolecules: amino acids"),
  why_others_wrong="Each wrong pair gives the amino acid the nature of another one in the NCERT list.", seconds=35)

# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Respiratory system", "Basic", "direct",
  "In humans, the trachea divides into the right and left primary bronchi at the level of the:",
  ["3rd cervical vertebra", "5th thoracic vertebra", "9th thoracic vertebra", "1st lumbar vertebra"], "B",
  "Human respiratory tract",
  "The trachea is a straight tube extending up to the mid-thoracic cavity, where it divides at the level of the 5th "
  "thoracic vertebra into the right and left primary bronchi.",
  ["Trachea → mid-thoracic cavity", "Division into primary bronchi → level of 5th thoracic vertebra"],
  R_BRE("human respiratory system"), seconds=25)

Z(BRE, "Respiratory system", "Basic", "direct",
  "Insects exchange gases with the atmosphere through:",
  ["Gills", "A network of tracheal tubes", "Book lungs", "Moist skin only"], "B",
  "Respiratory organs in different animals",
  "Lower invertebrates such as sponges, coelenterates and flatworms use simple diffusion over the body surface; "
  "earthworms use their moist cuticle; insects have a network of tubes (tracheal tubes) that carry air into the "
  "body.",
  ["Insects → tracheal tubes", "Aquatic arthropods and molluscs → gills", "Earthworm → moist cuticle"],
  R_BRE("respiratory organs"), seconds=20)

Z(BRE, "Respiratory system", "Basic", "statement_pair",
  sp("The conducting part of the human respiratory system extends from the external nostrils up to the terminal "
     "bronchioles.",
     "The alveoli and their ducts form the respiratory or exchange part of the system."),
  STATEMENT_PAIR, "A",
  "Conducting and exchange parts",
  "Both statements are the NCERT division of the respiratory system. The conducting part transports air to the "
  "alveoli, clears it of foreign particles, humidifies it and brings it to body temperature. The exchange part is "
  "where O₂ and CO₂ actually diffuse between blood and air.",
  ["External nostrils → terminal bronchioles = conducting part (I true)",
   "Alveoli and their ducts = exchange part (II true)"],
  R_BRE("human respiratory system"), seconds=30)

Z(BRE, "Regulation and disorders", "Basic", "direct",
  "The respiratory rhythm centre, which is primarily responsible for regulating breathing, is located in the:",
  ["Pons", "Cerebellum", "Hypothalamus", "Medulla region of the brain"], "D",
  "Neural regulation of respiration",
  "A specialised centre in the medulla region of the brain, the respiratory rhythm centre, is primarily responsible "
  "for this regulation. The pneumotaxic centre in the pons can moderate it.",
  ["Rhythm centre → medulla", "Pneumotaxic centre → pons"],
  R_BRE("regulation of respiration"),
  why_others_wrong="The pons holds the pneumotaxic centre, which only moderates the rhythm centre.", seconds=20)

Z(BRE, "Respiratory volumes", "Intermediate", "numerical",
  "A healthy man has a tidal volume of 500 mL, an inspiratory reserve volume of 3000 mL, an expiratory reserve volume "
  "of 1100 mL and a residual volume of 1200 mL. His expiratory capacity is:",
  ["2300 mL", "3500 mL", "1600 mL", "4600 mL"], "C",
  "Respiratory capacities",
  "Expiratory capacity (EC) is the total volume of air a person can expire after a normal inspiration: the tidal "
  "volume plus the expiratory reserve volume.",
  ["EC = TV + ERV", "EC = 500 + 1100 = 1600 mL"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="2300 mL is ERV + RV, the functional residual capacity. 3500 mL is TV + IRV, the inspiratory "
                   "capacity. 4600 mL is TV + IRV + ERV, the vital capacity.",
  seconds=45, verified_by=RECOMPUTED)

Z(BRE, "Mechanism of breathing", "Intermediate", "assertion_reason",
  ar("Inspiration takes place when the intra-pulmonary pressure is less than the atmospheric pressure.",
     "During inspiration, the external inter-costal muscles relax."),
  ASSERTION_REASON, "C",
  "Pressure gradient and muscles of breathing",
  "Air moves in when there is a negative pressure in the lungs relative to the atmosphere: A is true. Inspiration "
  "starts with contraction of the diaphragm, and contraction (not relaxation) of the external inter-costal muscles "
  "lifts the ribs and sternum, enlarging the thoracic chamber: R is false.",
  ["Intra-pulmonary pressure < atmospheric → air rushes in → A true",
   "External inter-costals contract during inspiration → R false"],
  R_BRE("mechanism of breathing"), seconds=40)

_o = ["(a), (b), (c) and (e) only", "(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only"]
ms_check("abce", _o, "A")
Z(BRE, "Exchange and transport of gases", "Intermediate", "multi_statement",
  ms("Which of the following statements about transport of gases in humans are correct?",
     ["About 97 per cent of O₂ is transported by RBCs in the blood.",
      "About 70 per cent of CO₂ is carried as bicarbonate.",
      "About 20–25 per cent of CO₂ is carried by haemoglobin as carbamino-haemoglobin.",
      "Each haemoglobin molecule can carry a maximum of two molecules of O₂.",
      "About 7 per cent of CO₂ is carried in a dissolved state through plasma."]),
  _o, "A",
  "Transport of O₂ and CO₂",
  "About 97% of O₂ travels with RBCs and 3% dissolved in plasma. Of CO₂, 20–25% is carried as "
  "carbamino-haemoglobin, about 70% as bicarbonate and about 7% dissolved in plasma. Each haemoglobin molecule can "
  "carry up to four O₂ molecules.",
  ["(a) True", "(b) True", "(c) True", "(d) False: maximum four O₂ per haemoglobin", "(e) True"],
  R_BRE("transport of gases"), seconds=50)

Z(BRE, "Exchange and transport of gases", "Intermediate", "direct",
  "Compared with oxygen, the solubility of carbon dioxide is about:",
  ["2–3 times higher", "20–25 times higher", "200–250 times higher", "The same"], "B",
  "Factors affecting diffusion of gases",
  "Solubility of the gases and the thickness of the membranes also affect diffusion. CO₂ is 20–25 times more "
  "soluble than O₂, so the amount of CO₂ that can diffuse per unit difference in partial pressure is much higher "
  "than that of O₂.",
  ["Solubility of CO₂ ≈ 20–25 × that of O₂"],
  R_BRE("exchange of gases"), seconds=25)

Z(BRE, "Regulation and disorders", "Intermediate", "statement_pair",
  sp("Emphysema is a chronic disorder in which alveolar walls are damaged, so the respiratory surface decreases.",
     "Asthma is a difficulty in breathing, causing wheezing, due to inflammation of bronchi and bronchioles."),
  STATEMENT_PAIR, "A",
  "Disorders of the respiratory system",
  "Both statements match NCERT. In emphysema the damaged alveolar walls reduce the respiratory surface; cigarette "
  "smoking is a major cause. In asthma, inflamed bronchi and bronchioles make breathing difficult and cause wheezing.",
  ["Emphysema → alveolar walls damaged (I true)", "Asthma → inflamed bronchi and bronchioles (II true)"],
  R_BRE("disorders of the respiratory system"), seconds=30)

Z(BRE, "Exchange and transport of gases", "Advanced", "numerical",
  "Under normal physiological conditions, every 100 mL of oxygenated blood delivers about 5 mL of O₂ to the tissues. "
  "If 5 L of blood flows through the tissues every minute, the volume of O₂ delivered to the tissues per minute is "
  "about:",
  ["25 mL", "200 mL", "2500 mL", "250 mL"], "D",
  "O₂ delivery to tissues",
  "Find how many 100 mL portions are in 5 L of blood, then multiply by the 5 mL of O₂ each portion delivers.",
  ["5 L = 5000 mL = 50 portions of 100 mL", "O₂ delivered = 50 × 5 mL = 250 mL per minute"],
  R_BRE("transport of oxygen"),
  why_others_wrong="200 mL uses the 4 mL figure, which is for CO₂ delivered to the alveoli. 25 mL and 2500 mL come "
                   "from slipping a factor of 10 while converting litres to 100 mL portions.",
  seconds=60, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Advanced", "assertion_reason",
  ar("More CO₂ binds to haemoglobin in the tissues than in the alveoli.",
     "In the tissues pCO₂ is high and pO₂ is low, which favours the binding of CO₂ to haemoglobin."),
  ASSERTION_REASON, "A",
  "Conditions for carbamino-haemoglobin formation",
  "CO₂ binding to haemoglobin depends on partial pressures. Where pCO₂ is high and pO₂ is low (tissues), more CO₂ "
  "binds; where pCO₂ is low and pO₂ is high (alveoli), CO₂ is released. So R is the reason for A.",
  ["Tissues: high pCO₂, low pO₂ → binding favoured", "Alveoli: low pCO₂, high pO₂ → dissociation",
   "R explains A"],
  R_BRE("transport of carbon dioxide"), seconds=45)

_o = ["(a) and (d) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)"]
ms_check("abc", _o, "B")
Z(BRE, "Regulation and disorders", "Advanced", "multi_statement",
  ms("Which of the following statements about the regulation of respiration are correct?",
     ["The pneumotaxic centre in the pons can reduce the duration of inspiration and thereby alter the respiratory "
      "rate.",
      "A chemosensitive area adjacent to the rhythm centre is highly sensitive to CO₂ and hydrogen ions.",
      "Receptors associated with the aortic arch and carotid artery can recognise changes in CO₂ and H⁺ "
      "concentration.",
      "Oxygen plays a major role in the regulation of the respiratory rhythm."]),
  _o, "B",
  "Chemical and neural control of breathing",
  "The pneumotaxic centre moderates the rhythm centre. Rising CO₂ and H⁺ activate the chemosensitive area and the "
  "receptors in the aortic arch and carotid artery, which signal the rhythm centre to adjust breathing. NCERT states "
  "that the role of oxygen in regulating the respiratory rhythm is quite insignificant.",
  ["(a) True", "(b) True", "(c) True", "(d) False: the role of O₂ is quite insignificant"],
  R_BRE("regulation of respiration"),
  why_others_wrong="(d) is the trap: breathing is driven mainly by CO₂ and H⁺, not by O₂.", seconds=50)

Z(BRE, "Exchange and transport of gases", "Advanced", "match_list",
  ml(("partial pressure", "value in mm Hg"),
     ["pO₂ in atmospheric air", "pO₂ in oxygenated blood", "pCO₂ in deoxygenated blood", "pCO₂ in atmospheric air"],
     ["0.3", "45", "95", "159"]),
  match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                 {"A": "IV", "B": "III", "C": "I", "D": "II"}], at="C"),
  "C",
  "Partial pressures of respiratory gases",
  "NCERT tabulates partial pressures (mm Hg) at different sites. O₂ falls from the atmosphere to the tissues; CO₂ "
  "is almost absent in atmospheric air and highest in tissues and deoxygenated blood.",
  ["pO₂ atmospheric air = 159 (IV)", "pO₂ oxygenated blood = 95 (III)", "pCO₂ deoxygenated blood = 45 (II)",
   "pCO₂ atmospheric air = 0.3 (I)"],
  R_BRE("exchange of gases: partial pressures of O₂ and CO₂"), seconds=50)

# ================================================================ Body Fluids and Circulation (B5 I7 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "The most abundant type of white blood cell (leucocyte) in human blood is the:",
  ["Lymphocyte", "Monocyte", "Neutrophil", "Eosinophil"], "C",
  "Differential count of leucocytes",
  "Neutrophils are the most abundant leucocytes (60–65% of total WBCs). Basophils are the least (0.5–1%).",
  ["Neutrophils 60–65%", "Lymphocytes 20–25%", "Monocytes 6–8%", "Eosinophils 2–3%"],
  R_BFC("blood: formed elements"), seconds=20)

Z(BFC, "Human heart", "Basic", "direct",
  "Which part of the human heart initiates and maintains its rhythmic contractile activity and is therefore called "
  "the pacemaker?",
  ["Atrio-ventricular node", "Bundle of His", "Purkinje fibres", "Sino-atrial node"], "D",
  "Nodal tissue of the heart",
  "The sino-atrial node (SAN) generates the maximum number of action potentials (70–75 per minute), so it starts "
  "and maintains the rhythm of the heart. It is called the pacemaker.",
  ["SAN → highest rate of action potentials → pacemaker"],
  R_BFC("human circulatory system: nodal tissue"), seconds=20)

Z(BFC, "Cardiac cycle and ECG", "Basic", "numerical",
  "If a person's heart beats 75 times per minute, the duration of one cardiac cycle is:",
  ["0.8 s", "1.25 s", "0.75 s", "0.08 s"], "A",
  "Duration of the cardiac cycle",
  "One heartbeat is one cardiac cycle, so the duration of a cycle is 60 seconds divided by the number of beats per "
  "minute.",
  ["Duration = 60 s / 75 = 0.8 s"],
  R_BFC("cardiac cycle"),
  why_others_wrong="1.25 s divides the wrong way (75/60). 0.75 s divides 75 by 100 instead of 60 by 75. 0.08 s is a "
                   "decimal slip.",
  seconds=30, verified_by=RECOMPUTED)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Plasma proteins constitute about 20–25 per cent of plasma.", "Albumins help in osmotic balance."),
  STATEMENT_PAIR, "D",
  "Composition of plasma",
  "Plasma is 90–92% water and proteins make up only 6–8% of it: Statement I is false. Of the plasma proteins, "
  "fibrinogen is needed for clotting, globulins for defence and albumins for osmotic balance: Statement II is true.",
  ["Plasma proteins 6–8% → I false", "Albumins → osmotic balance → II true"],
  R_BFC("blood: plasma"), seconds=30)

Z(BFC, "Double circulation and regulation", "Basic", "direct",
  "A closed circulatory system, in which blood always flows through a closed network of vessels, is found in:",
  ["Arthropods", "Annelids", "Molluscs", "Insects"], "B",
  "Open and closed circulation",
  "Arthropods (including insects) and molluscs have an open circulatory system: blood is pumped into open spaces "
  "or sinuses. Annelids and chordates have a closed circulatory system.",
  ["Open → arthropods, molluscs", "Closed → annelids, chordates"],
  R_BFC("circulatory pathways"), seconds=20)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "match_list",
  ml(("feature of a standard ECG", "event"), ["P-wave", "QRS complex", "T-wave", "End of the T-wave"],
     ["End of systole", "Depolarisation of the atria", "Return of the ventricles from excited to normal state",
      "Depolarisation of the ventricles"]),
  match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
                 {"A": "II", "B": "IV", "C": "I", "D": "III"}], at="B"),
  "B",
  "Electrocardiogram",
  "Each peak of the ECG matches an electrical event in the heart.",
  ["P-wave → depolarisation of the atria, which causes atrial contraction (II)",
   "QRS complex → depolarisation of the ventricles, which starts ventricular contraction (IV)",
   "T-wave → return of the ventricles from excited to normal state, i.e. repolarisation (III)",
   "End of the T-wave → end of systole (I)"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="The common mistake gives the P-wave to the ventricles or the T-wave to depolarisation.",
  seconds=45)

Z(BFC, "Blood and blood groups", "Intermediate", "assertion_reason",
  ar("An Rh-ve mother carrying an Rh+ve foetus in a subsequent pregnancy may have a baby with erythroblastosis "
     "foetalis.",
     "During the delivery of her first Rh+ve child, the mother may be exposed to small amounts of foetal Rh+ve "
     "blood and start preparing antibodies against the Rh antigen."),
  ASSERTION_REASON, "A",
  "Rh incompatibility",
  "In the first pregnancy the placenta keeps the two bloods apart. At the first delivery, some foetal Rh+ve blood "
  "may reach the mother, who then makes anti-Rh antibodies. In later pregnancies these antibodies can leak into the "
  "Rh+ve foetus and destroy its RBCs (erythroblastosis foetalis). R explains A.",
  ["First delivery → maternal sensitisation (R true)",
   "Next Rh+ve foetus → maternal antibodies destroy foetal RBCs (A true)", "R is the cause of A"],
  R_BFC("blood groups: Rh grouping"), seconds=45)

_o = ["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only", "(a), (b), (c) and (d) only"]
ms_check("abcd", _o, "D")
Z(BFC, "Coagulation and lymph", "Intermediate", "multi_statement",
  ms("Which of the following statements about coagulation of blood are correct?",
     ["An enzyme complex, thrombokinase, is required for the formation of thrombin from prothrombin.",
      "Thrombin converts inactive fibrinogen in the plasma into fibrin.",
      "Calcium ions play a very important role in clotting.",
      "An injury stimulates the platelets to release certain factors that activate the mechanism of coagulation.",
      "Serum is plasma that still contains the clotting factors."]),
  _o, "D",
  "Coagulation cascade",
  "The clot is a network of fibrin threads in which formed elements are trapped. Fibrin forms from fibrinogen under "
  "thrombin, and thrombin forms from prothrombin with the help of thrombokinase. Platelets release factors after an "
  "injury, and Ca²⁺ is essential. Plasma without the clotting factors is called serum.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: serum is plasma without clotting factors"],
  R_BFC("coagulation of blood; plasma"), seconds=50)

Z(BFC, "Human heart", "Intermediate", "direct",
  "The atrio-ventricular node (AVN) of the human heart is located in the:",
  ["Upper right corner of the right atrium", "Lower left corner of the right atrium, close to the atrio-ventricular "
   "septum", "Wall of the left ventricle near the apex", "Upper part of the inter-ventricular septum"], "B",
  "Position of the nodal tissue",
  "The SAN lies in the upper right corner of the right atrium. The AVN lies in the lower left corner of the right "
  "atrium, close to the atrio-ventricular septum. From the AVN, the bundle of His passes through the "
  "atrio-ventricular septum to the top of the inter-ventricular septum.",
  ["SAN → upper right corner of right atrium", "AVN → lower left corner of right atrium, near AV septum"],
  R_BFC("human circulatory system: nodal tissue"),
  why_others_wrong="The first option is the position of the SAN; the inter-ventricular septum carries the bundle of "
                   "His and its branches.", seconds=30)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "statement_pair",
  sp("The first heart sound, 'lub', is associated with the closure of the tricuspid and bicuspid valves.",
     "The second heart sound, 'dub', is associated with the closure of the semilunar valves."),
  STATEMENT_PAIR, "A",
  "Heart sounds",
  "During each cardiac cycle two prominent sounds are heard. The first (lub) comes from closure of the "
  "atrio-ventricular valves (tricuspid and bicuspid) at the start of ventricular systole; the second (dub) from "
  "closure of the semilunar valves at the start of ventricular diastole. Both statements are true.",
  ["Lub → AV valves close (I true)", "Dub → semilunar valves close (II true)"],
  R_BFC("cardiac cycle"), seconds=30)

Z(BFC, "Double circulation and regulation", "Intermediate", "direct",
  "In the hepatic portal system, the hepatic portal vein carries blood from the:",
  ["Liver to the intestine", "Liver to the heart", "Intestine to the liver", "Heart to the liver"], "C",
  "Portal circulation",
  "A unique vascular connection exists between the digestive tract and the liver. The hepatic portal vein carries "
  "blood from the intestine to the liver before it is delivered to the systemic circulation.",
  ["Intestine → hepatic portal vein → liver → systemic circulation"],
  R_BFC("double circulation: hepatic portal system"), seconds=25)

Z(BFC, "Double circulation and regulation", "Intermediate", "direct",
  "Parasympathetic neural signals to the heart:",
  ["Increase the rate of heartbeat", "Increase the strength of ventricular contraction",
   "Have no effect, because the heart is myogenic",
   "Decrease the rate of heartbeat and the speed of conduction of action potential, and thereby the cardiac "
   "output"], "D",
  "Neural regulation of cardiac activity",
  "The heart is myogenic (auto-regulated by nodal tissue), but a centre in the medulla oblongata can moderate it "
  "through the ANS. Sympathetic signals increase heart rate, strength of ventricular contraction and cardiac output; "
  "parasympathetic signals decrease heart rate, conduction speed and cardiac output.",
  ["Sympathetic → increases rate and strength", "Parasympathetic → decreases rate, conduction speed, output"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="The first two are sympathetic effects. Being myogenic does not stop the ANS from moderating the "
                   "heart.", seconds=35)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "numerical",
  "At rest, a person's stroke volume is 70 mL and heart rate 72 beats per minute. During exercise, the stroke volume "
  "rises to 80 mL and the heart rate to 90 beats per minute. By how much does the cardiac output increase?",
  ["7200 mL per minute", "1260 mL per minute", "2160 mL per minute", "5040 mL per minute"], "C",
  "Cardiac output = stroke volume × heart rate",
  "Work out the cardiac output in each state and subtract.",
  ["At rest: 70 mL × 72 = 5040 mL per minute", "During exercise: 80 mL × 90 = 7200 mL per minute",
   "Increase = 7200 − 5040 = 2160 mL per minute"],
  R_BFC("cardiac cycle: stroke volume and cardiac output"),
  why_others_wrong="7200 and 5040 mL are the two outputs themselves, not the increase. 1260 mL multiplies only the "
                   "rise in heart rate (18) by the resting stroke volume and ignores the larger stroke volume.",
  seconds=75, verified_by=RECOMPUTED)

Z(BFC, "Blood and blood groups", "Advanced", "match_list",
  ml(("leucocyte", "feature"), ["Basophils", "Eosinophils", "Monocytes", "Lymphocytes"],
     ["Occur as B and T forms responsible for immune responses", "Phagocytic cells forming 6–8 per cent of WBCs",
      "Secrete histamine, serotonin and heparin", "Resist infections and are associated with allergic reactions"]),
  match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                 {"A": "II", "B": "IV", "C": "III", "D": "I"}], at="D"),
  "D",
  "Functions of leucocytes",
  "Granulocytes (neutrophils, eosinophils, basophils) and agranulocytes (lymphocytes, monocytes) have distinct "
  "roles.",
  ["Basophils → histamine, serotonin, heparin; inflammatory reactions (III)",
   "Eosinophils → resist infections, allergic reactions (IV)", "Monocytes → phagocytic, 6–8% (II)",
   "Lymphocytes → B and T forms, immune responses (I)"],
  R_BFC("blood: formed elements"),
  why_others_wrong="Swapping basophils and eosinophils is the classic error; both are granulocytes linked with "
                   "allergy and inflammation.", seconds=50)

Z(BFC, "Double circulation and regulation", "Advanced", "assertion_reason",
  ar("Amphibians and most reptiles show incomplete double circulation.",
     "Their heart has a single ventricle into which both oxygenated and deoxygenated blood flow and get mixed."),
  ASSERTION_REASON, "A",
  "Evolution of circulation in vertebrates",
  "Amphibians and reptiles (except crocodiles) have a three-chambered heart. The left atrium receives oxygenated "
  "blood and the right atrium deoxygenated blood, but both empty into the single ventricle, which pumps out mixed "
  "blood. That mixing is why the double circulation is incomplete, so R explains A.",
  ["Two atria, one ventricle → mixing in the ventricle", "Mixed blood pumped out → incomplete double circulation"],
  R_BFC("circulatory pathways"), seconds=45)

_o = ["(a), (b), (c) and (e) only", "(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c), (d) and (e)"]
ms_check("abce", _o, "A")
Z(BFC, "Circulatory disorders", "Advanced", "multi_statement",
  ms("Which of the following statements about disorders of the circulatory system are correct?",
     ["Repeated blood pressure readings of 140/90 mm Hg or higher indicate hypertension.",
      "In coronary artery disease, deposits of calcium, fat, cholesterol and fibrous tissue narrow the lumen of the "
      "arteries supplying the heart muscle.",
      "Angina occurs when not enough oxygen reaches the heart muscle.",
      "Heart failure is the same as cardiac arrest.",
      "Heart failure is sometimes called congestive heart failure because congestion of the lungs is one of its "
      "main symptoms."]),
  _o, "A",
  "Disorders of the circulatory system",
  "Normal blood pressure is 120/80 mm Hg; repeated readings of 140/90 or higher indicate hypertension. CAD "
  "(atherosclerosis) narrows the coronary arteries. Angina is acute chest pain when too little oxygen reaches the "
  "heart muscle. Heart failure means the heart does not pump blood effectively enough; it is not the same as cardiac "
  "arrest (heart stops beating) or a heart attack (heart muscle suddenly damaged by inadequate blood supply).",
  ["(a) True", "(b) True", "(c) True", "(d) False: heart failure ≠ cardiac arrest", "(e) True"],
  R_BFC("disorders of circulatory system"), seconds=60)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "statement_pair",
  sp("During joint diastole, all four chambers are relaxed and the tricuspid and bicuspid valves are open.",
     "Atrial systole accounts for about 70 per cent of the filling of the ventricles."),
  STATEMENT_PAIR, "C",
  "Events of the cardiac cycle",
  "At the start of the cycle all four chambers are in joint diastole: the AV valves are open, blood flows from the "
  "atria into the ventricles, and the semilunar valves are closed. Statement I is true. Most ventricular filling "
  "takes place in this phase; atrial systole then increases the flow of blood into the ventricles by only about 30 "
  "per cent. Statement II is false.",
  ["Joint diastole: AV valves open, semilunar valves closed → I true",
   "Atrial systole adds about 30% of ventricular filling, not 70% → II false"],
  R_BFC("cardiac cycle"),
  why_others_wrong="NCERT gives about 30 per cent for the increase due to atrial systole; Statement II inflates it, "
                   "so options A and B fail.", seconds=45)

# ================================================================ Excretory Products and their Elimination (B4 I6 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Which of the following groups of animals is uricotelic?",
  ["Bony fishes and aquatic amphibians", "Mammals and marine fishes", "Reptiles, birds, land snails and insects",
   "Aquatic insects and bony fishes"], "C",
  "Ammonotelism, ureotelism and uricotelism",
  "Uricotelic animals excrete nitrogenous wastes as uric acid in pellet or paste form with minimum loss of water: "
  "reptiles, birds, land snails and insects.",
  ["Ammonotelic → bony fishes, aquatic amphibians, aquatic insects",
   "Ureotelic → mammals, many terrestrial amphibians, marine fishes",
   "Uricotelic → reptiles, birds, land snails, insects"],
  R_EXC("introduction: modes of excretion"), seconds=25)

Z(EXC, "Nephron structure", "Basic", "direct",
  "The notch at the centre of the inner concave surface of the kidney, through which the ureter, blood vessels and "
  "nerves enter, is called the:",
  ["Renal pelvis", "Calyx", "Medullary pyramid", "Hilum"], "D",
  "External structure of the kidney",
  "Towards the centre of the inner concave surface of each kidney is a notch called the hilum. Inner to the hilum is "
  "a broad funnel-shaped space, the renal pelvis, with projections called calyces.",
  ["Notch on inner concave surface → hilum", "Funnel-shaped space inside → renal pelvis"],
  R_EXC("human excretory system"), seconds=20)

Z(EXC, "Nephron structure", "Basic", "direct",
  "In the human kidney, the columns of Bertini are:",
  ["Projections of the renal pelvis", "Extensions of the cortex between the medullary pyramids",
   "Conical masses of the medulla", "Bundles of collecting ducts in the renal papillae"], "B",
  "Internal structure of the kidney",
  "The medulla is divided into a few conical masses, the medullary pyramids, which project into the calyces. The "
  "cortex extends in between the medullary pyramids as renal columns called columns of Bertini.",
  ["Medullary pyramids → conical masses of medulla", "Columns of Bertini → cortex extending between pyramids"],
  R_EXC("human excretory system"), seconds=25)

Z(EXC, "Nephron structure", "Basic", "statement_pair",
  sp("The Malpighian corpuscle, PCT and DCT of the nephron are situated in the cortical region of the kidney.",
     "Each human kidney has nearly one million nephrons."),
  STATEMENT_PAIR, "A",
  "Organisation of nephrons",
  "Both statements are NCERT facts. Each kidney has nearly one million nephrons, the functional units. The "
  "Malpighian corpuscle, PCT and DCT lie in the cortex, while the loop of Henle dips into the medulla.",
  ["Corpuscle, PCT, DCT → cortex (I true)", "About one million nephrons per kidney (II true)"],
  R_EXC("human excretory system: nephron"), seconds=30)

Z(EXC, "Urine formation", "Intermediate", "numerical",
  "The glomerular filtration rate of a healthy person is 125 mL per minute. If exactly 99 per cent of the filtrate is "
  "reabsorbed by the renal tubules, the volume of urine formed in one day is:",
  ["180 L", "1.8 L", "18 L", "0.18 L"], "B",
  "GFR and tubular reabsorption",
  "Convert the GFR to a daily volume, then keep only the 1 per cent that is not reabsorbed.",
  ["Filtrate per day = 125 mL × 60 × 24 = 180,000 mL = 180 L",
   "Not reabsorbed = 1% of 180 L = 1.8 L"],
  R_EXC("urine formation"),
  shortcut="NCERT's 180 L of filtrate per day is worth remembering; 1% of it is 1.8 L.",
  why_others_wrong="180 L is the filtrate, before reabsorption. 18 L keeps 10% instead of 1%. 0.18 L keeps 0.1%.",
  seconds=50, verified_by=RECOMPUTED)

Z(EXC, "Urine formation", "Intermediate", "assertion_reason",
  ar("The ascending limb of Henle's loop is impermeable to water.",
     "The ascending limb of Henle's loop allows transport of electrolytes actively or passively."),
  ASSERTION_REASON, "B",
  "Function of the ascending limb",
  "Both are NCERT statements about the ascending limb, so both are true. But transport of electrolytes does not "
  "explain why the limb is impermeable to water; these are two separate properties. Together they make the filtrate "
  "dilute as it moves up into the cortex.",
  ["A: impermeable to water → true", "R: electrolytes move out actively or passively → true",
   "R does not explain the water impermeability"],
  R_EXC("function of the tubules"),
  why_others_wrong="Option A wrongly treats one property of the ascending limb as the cause of the other.",
  seconds=40)

Z(EXC, "Urine formation", "Intermediate", "match_list",
  ml(("part of the nephron", "function"),
     ["Proximal convoluted tubule", "Descending limb of loop of Henle", "Distal convoluted tubule",
      "Collecting duct"],
     ["Allows passage of small amounts of urea into the medullary interstitium",
      "Conditional reabsorption of Na⁺ and water",
      "Permeable to water but almost impermeable to electrolytes",
      "Reabsorbs nearly all essential nutrients and 70–80 per cent of electrolytes and water"]),
  match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                 {"A": "IV", "B": "III", "C": "I", "D": "II"}], at="D"),
  "D",
  "Function of the tubules",
  "Each segment of the nephron handles water and solutes differently.",
  ["PCT → nearly all nutrients, 70–80% of electrolytes and water (IV)",
   "Descending limb → permeable to water, almost impermeable to electrolytes (III)",
   "DCT → conditional reabsorption of Na⁺ and water (II)",
   "Collecting duct → passes small amounts of urea into the medullary interstitium (I)"],
  R_EXC("function of the tubules"), seconds=50)

Z(EXC, "Regulation of kidney function", "Intermediate", "direct",
  "An increase in blood flow to the atria of the heart causes the release of atrial natriuretic factor (ANF). ANF "
  "causes:",
  ["Vasoconstriction and a rise in blood pressure", "Release of renin from the JG cells",
   "Vasodilation and a fall in blood pressure", "Increased secretion of aldosterone"], "C",
  "ANF as a check on the renin-angiotensin mechanism",
  "ANF causes vasodilation (dilation of blood vessels) and thereby decreases blood pressure. So the ANF mechanism "
  "acts as a check on the renin-angiotensin mechanism.",
  ["More blood to atria → ANF released", "ANF → vasodilation → blood pressure falls"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="The other options describe the renin-angiotensin-aldosterone mechanism, which ANF opposes.",
  seconds=30)

_o = ["(a) and (d) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)"]
ms_check("abc", _o, "B")
Z(EXC, "Urine formation", "Intermediate", "multi_statement",
  ms("Which of the following statements about glomerular filtration are correct?",
     ["The glomerular capillary blood pressure causes filtration of blood.",
      "Blood is filtered through three layers: the endothelium of the glomerular blood vessels, the epithelium of "
      "Bowman's capsule and a basement membrane between them.",
      "The podocytes of Bowman's capsule leave minute spaces called filtration slits.",
      "Plasma proteins pass freely into the lumen of Bowman's capsule."]),
  _o, "B",
  "Ultrafiltration in the glomerulus",
  "Blood pressure in the glomerular capillaries forces fluid through the three-layered filtration membrane. The "
  "podocytes are arranged to leave filtration slits. Filtration is so fine that almost all constituents of plasma "
  "except the proteins pass into Bowman's capsule, so it is called ultrafiltration.",
  ["(a) True", "(b) True", "(c) True", "(d) False: proteins are held back (ultrafiltration)"],
  R_EXC("urine formation"), seconds=45)

Z(EXC, "Disorders and dialysis", "Intermediate", "statement_pair",
  sp("In haemodialysis, an anticoagulant such as heparin is added to the blood before it is pumped into the "
     "dialysing unit.",
     "Glomerulonephritis is the formation of stones or insoluble masses of crystallised salts in the kidney."),
  STATEMENT_PAIR, "C",
  "Disorders of the excretory system",
  "During haemodialysis, blood drained from an artery is mixed with heparin and pumped through the dialysing unit; "
  "anti-heparin is added before it is returned: Statement I is true. Glomerulonephritis is inflammation of the "
  "glomeruli; stone formation is renal calculi: Statement II is false.",
  ["Heparin added before dialysis → I true", "Glomerulonephritis = inflamed glomeruli; stones = renal calculi → II false"],
  R_EXC("disorders of the excretory system"), seconds=35)

Z(EXC, "Urine formation", "Advanced", "assertion_reason",
  ar("Human kidneys can produce urine nearly four times as concentrated as the initial filtrate.",
     "The counter-current mechanism maintains an osmolarity gradient in the medullary interstitium, from about "
     "300 mOsmol L⁻¹ in the cortex to about 1200 mOsmol L⁻¹ in the inner medulla."),
  ASSERTION_REASON, "A",
  "Counter-current mechanism",
  "The flow of filtrate in the two limbs of Henle's loop and of blood in the two limbs of the vasa recta is in "
  "opposite directions. This keeps the medullary interstitium increasingly concentrated towards the inner medulla. "
  "Water then passes easily out of the collecting tubule into this hyperosmotic interstitium, concentrating the "
  "urine. R explains A (1200/300 = 4).",
  ["Counter-current flow → gradient 300 → 1200 mOsmol L⁻¹", "Water leaves collecting duct → urine concentrated",
   "Maximum concentration ≈ 4 × filtrate → R explains A"],
  R_EXC("mechanism of concentration of the filtrate"), seconds=50)

_o = ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only", "(a), (b), (c), (d) and (e)"]
ms_check("abde", _o, "C")
Z(EXC, "Regulation of kidney function", "Advanced", "multi_statement",
  ms("Which of the following statements about the renin-angiotensin mechanism are correct?",
     ["A fall in glomerular blood flow or GFR can activate the JG cells to release renin.",
      "Renin converts angiotensinogen in blood to angiotensin I and further to angiotensin II.",
      "Angiotensin II is a powerful vasodilator.",
      "Angiotensin II activates the adrenal cortex to release aldosterone.",
      "Aldosterone causes reabsorption of Na⁺ and water from the distal parts of the tubule."]),
  _o, "C",
  "Renin-angiotensin-aldosterone mechanism",
  "When GFR falls, the juxtaglomerular apparatus releases renin. The resulting angiotensin II is a powerful "
  "vasoconstrictor: it raises glomerular blood pressure and thereby GFR. It also makes the adrenal cortex release "
  "aldosterone, which increases Na⁺ and water reabsorption, raising blood pressure and GFR.",
  ["(a) True", "(b) True", "(c) False: angiotensin II is a vasoconstrictor", "(d) True", "(e) True"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="(c) is the trap: vasodilation is the effect of ANF, which works against this mechanism.",
  seconds=60)

Z(EXC, "Modes of excretion", "Advanced", "match_list",
  ml(("excretory structure", "animal"),
     ["Antennal glands", "Malpighian tubules", "Nephridia", "Protonephridia"],
     ["Earthworm", "Amphioxus", "Prawn", "Cockroach"]),
  match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                 {"A": "II", "B": "IV", "C": "I", "D": "III"}], at="A"),
  "A",
  "Excretory structures in animals",
  "NCERT names the excretory structure of each group. The trap is Amphioxus, a cephalochordate that, like flatworms, "
  "has protonephridia.",
  ["Antennal (green) glands → crustaceans such as prawn (III)",
   "Malpighian tubules → most insects including cockroach (IV)",
   "Nephridia → earthworm and other annelids (I)",
   "Protonephridia (flame cells) → flatworms, rotifers, some annelids and Amphioxus (II)"],
  R_EXC("introduction: excretory structures"), seconds=45)

Z(EXC, "Nephron structure", "Advanced", "direct",
  "Which of the following is present in juxtamedullary nephrons but is absent or highly reduced in cortical "
  "nephrons?",
  ["A short loop of Henle and a well-developed vasa recta", "A glomerulus and Bowman's capsule",
   "A proximal convoluted tubule with a brush border",
   "A long loop of Henle running deep into the medulla, with a well-developed vasa recta"], "D",
  "Cortical and juxtamedullary nephrons",
  "In most nephrons (cortical nephrons) the loop of Henle is short and extends only a little into the medulla, and "
  "the vasa recta is absent or highly reduced. Juxtamedullary nephrons have a very long loop of Henle that runs deep "
  "into the medulla and a prominent vasa recta, a U-shaped vessel parallel to the loop.",
  ["Cortical nephron → short loop, vasa recta absent or reduced",
   "Juxtamedullary nephron → long loop, vasa recta well developed",
   "Glomerulus and PCT → present in all nephrons"],
  R_EXC("human excretory system: nephron"),
  why_others_wrong="The first option pairs a short loop (a cortical feature) with a juxtamedullary feature. The "
                   "glomerulus and PCT are common to all nephrons.", seconds=45)

# ================================================================ Locomotion and Movement (B4 I6 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Types of movement", "Basic", "direct",
  "In humans, ciliary movement is responsible for:",
  ["The movement of macrophages and leucocytes", "The movement of the jaws", "The beating of the heart",
   "The passage of ova through the female reproductive tract"], "D",
  "Amoeboid, ciliary and muscular movement",
  "Ciliary movement occurs in internal tubular organs lined by ciliated epithelium. Coordinated cilia in the trachea "
  "remove dust particles, and ciliary movement helps the passage of ova through the female reproductive tract.",
  ["Ciliary → trachea, female reproductive tract", "Amoeboid → macrophages, leucocytes",
   "Muscular → limbs, jaws, heart"],
  R_LOC("types of movement"),
  why_others_wrong="Macrophages and leucocytes show amoeboid movement; jaws and heart move by muscular movement.",
  seconds=25)

Z(LOC, "Skeletal system", "Basic", "direct",
  "The total number of bones in the human skull, including the cranial and facial bones, is:",
  ["8", "14", "26", "22"], "D",
  "Axial skeleton: skull",
  "The skull has two sets of bones, cranial and facial, totalling 22. The 8 cranial bones form the hard protective "
  "outer covering of the brain; the 14 facial bones form the front part of the skull.",
  ["Cranial 8 + facial 14 = 22"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="8 and 14 are the cranial and facial bones alone; 26 is the number of vertebrae.", seconds=20)

Z(LOC, "Joints", "Basic", "direct",
  "The joint between the atlas and the axis vertebrae is a:",
  ["Pivot joint", "Hinge joint", "Gliding joint", "Saddle joint"], "A",
  "Types of synovial joints",
  "Synovial joints allow considerable movement. NCERT examples: ball and socket (humerus–pectoral girdle), hinge "
  "(knee), pivot (atlas–axis), gliding (between carpals), saddle (carpal–metacarpal of thumb).",
  ["Atlas–axis → pivot joint"],
  R_LOC("joints"), seconds=20)

Z(LOC, "Muscular and skeletal disorders", "Basic", "direct",
  "Gout is caused by:",
  ["Low Ca²⁺ in body fluids", "Accumulation of uric acid crystals in the joints",
   "An auto-immune disorder affecting the neuromuscular junction", "An age-related decrease in bone mass"], "B",
  "Disorders of muscular and skeletal system",
  "Gout is inflammation of joints due to accumulation of uric acid crystals.",
  ["Gout → uric acid crystals in joints", "Tetany → low Ca²⁺", "Myasthenia gravis → auto-immune, neuromuscular "
   "junction", "Osteoporosis → decreased bone mass"],
  R_LOC("disorders of muscular and skeletal system"), seconds=20)

Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "Each upper limb and each lower limb of a human contains 30 bones. Each half of the pectoral girdle is made of a "
  "clavicle and a scapula, and the pelvic girdle is made of two coxal bones (each formed by the fusion of ilium, "
  "ischium and pubis). The total number of bones in the appendicular skeleton is:",
  ["120", "124", "130", "126"], "D",
  "Appendicular skeleton = limbs + girdles",
  "Add the bones of the four limbs and of the two girdles, counting each fused coxal bone as one bone.",
  ["Limbs: 4 × 30 = 120", "Pectoral girdle: 2 × (clavicle + scapula) = 4", "Pelvic girdle: 2 coxal bones = 2",
   "Total = 120 + 4 + 2 = 126"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="120 counts the limbs only. 124 leaves out the pelvic girdle. 130 counts ilium, ischium and pubis "
                   "as separate bones although each coxal bone is a single fused bone.",
  seconds=60, verified_by=RECOMPUTED)

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("During contraction of a skeletal muscle fibre, the A-band shortens.",
     "Muscle contraction takes place by the sliding of thin filaments over thick filaments."),
  ASSERTION_REASON, "D",
  "Sliding filament theory",
  "When the thin (actin) filaments slide over the thick (myosin) filaments, the Z-lines are pulled closer and the "
  "sarcomere shortens. The I-bands get reduced, but the A-bands, which correspond to the thick filaments, retain "
  "their length: A is false. R is the sliding filament theory: true.",
  ["Sliding filaments → sarcomere shortens", "I-band reduces; A-band retains its length → A false",
   "R is the NCERT mechanism → true"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="Students often think every band shortens; NCERT states that the I-bands get reduced while the "
                   "A-bands retain their length.", seconds=45)

Z(LOC, "Muscle contraction", "Intermediate", "match_list",
  ml(("part of a sarcomere", "description"), ["I-band", "A-band", "Z-line", "M-line"],
     ["Thin fibrous membrane holding the thick filaments together in the middle of the A-band",
      "Elastic fibre that bisects the I-band; thin filaments are firmly attached to it",
      "Light band containing actin (isotropic band)",
      "Dark band containing myosin (anisotropic band)"]),
  match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                 {"A": "IV", "B": "III", "C": "I", "D": "II"}], at="C"),
  "C",
  "Structure of a myofibril",
  "Alternate light and dark bands give skeletal muscle its striated look.",
  ["I-band → light, actin, isotropic (III)", "A-band → dark, myosin, anisotropic (IV)",
   "Z-line → bisects I-band, anchors thin filaments (II)", "M-line → holds thick filaments in middle of A-band (I)"],
  R_LOC("skeletal muscle: structure of the myofibril"), seconds=45)

_o = ["(a), (c) and (e) only", "(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c), (d) and (e)"]
ms_check("abcd", _o, "B")
Z(LOC, "Muscle contraction", "Intermediate", "multi_statement",
  ms("Which of the following statements about the mechanism of muscle contraction are correct?",
     ["Acetylcholine released at the neuromuscular junction generates an action potential in the sarcolemma.",
      "The action potential spreads through the muscle fibre and causes the release of Ca²⁺ into the sarcoplasm.",
      "The myosin head binds to the exposed active sites on actin to form a cross bridge.",
      "During relaxation, Ca²⁺ is pumped back into the sarcoplasmic cisternae.",
      "The Ca²⁺ that triggers contraction is released from the mitochondria of the muscle fibre."]),
  _o, "B",
  "Excitation–contraction coupling",
  "A neural signal releases acetylcholine at the motor end plate, generating an action potential in the "
  "sarcolemma. Ca²⁺ is released from the sarcoplasmic reticulum, the store of calcium ions, and binds troponin, "
  "exposing the active sites on actin for myosin heads. Cross bridges form and pull actin. During relaxation Ca²⁺ is "
  "pumped back into the sarcoplasmic cisternae.",
  ["(a) True", "(b) True", "(c) True", "(d) True",
   "(e) False: the Ca²⁺ comes from the sarcoplasmic reticulum, not mitochondria"],
  R_LOC("mechanism of muscle contraction"), seconds=55)

Z(LOC, "Skeletal system", "Intermediate", "statement_pair",
  sp("The first seven pairs of ribs are called true ribs.",
     "The 11th and 12th pairs of ribs are called vertebrochondral (false) ribs."),
  STATEMENT_PAIR, "C",
  "Types of ribs",
  "The first seven pairs join the sternum ventrally through hyaline cartilage: true ribs. The 8th, 9th and 10th "
  "pairs join the seventh rib through hyaline cartilage instead: vertebrochondral (false) ribs. The 11th and 12th "
  "pairs are not connected ventrally: floating ribs. So Statement I is true and Statement II is false.",
  ["Ribs 1–7 → true ribs (I true)", "Ribs 8–10 → vertebrochondral (false) ribs",
   "Ribs 11–12 → floating ribs (II false)"],
  R_LOC("skeletal system: rib cage"), seconds=35)

Z(LOC, "Skeletal system", "Intermediate", "direct",
  "Which of the following statements about the human vertebral column is correct?",
  ["It is formed by 33 separate vertebrae in the adult", "It has 12 cervical vertebrae",
   "Its lumbar region has 7 vertebrae", "It is formed by 26 serially arranged units called vertebrae"], "D",
  "Vertebral column",
  "The vertebral column is formed by 26 serially arranged vertebrae and is dorsally placed. The vertebral formula "
  "is cervical 7, thoracic 12, lumbar 5, sacral 1 (fused) and coccygeal 1 (fused).",
  ["7 + 12 + 5 + 1 + 1 = 26 vertebrae"],
  R_LOC("skeletal system: vertebral column"),
  why_others_wrong="12 is the thoracic count and 7 the cervical count; the sacral and coccygeal vertebrae are fused, "
                   "so NCERT counts 26 units.", seconds=30)

Z(LOC, "Muscular and skeletal disorders", "Advanced", "assertion_reason",
  ar("Tetany is characterised by rapid spasms (wild contractions) in muscle.",
     "Tetany is caused by a high level of Ca²⁺ in body fluids."),
  ASSERTION_REASON, "C",
  "Tetany",
  "Tetany is rapid spasms (wild contractions) in muscle: A is true. It is due to low, not high, Ca²⁺ in body fluid: "
  "R is false.",
  ["A matches the NCERT definition → true", "Cause is low Ca²⁺ → R false"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="Linking Ca²⁺ with contraction tempts students to accept 'high Ca²⁺' as the cause.", seconds=35)

Z(LOC, "Joints", "Advanced", "match_list",
  ml(("type of synovial joint", "example"), ["Ball and socket joint", "Hinge joint", "Gliding joint", "Saddle joint"],
     ["Knee joint", "Between humerus and pectoral girdle", "Between carpal and metacarpal of thumb",
      "Between the carpals"]),
  match_options({"A": "II", "B": "I", "C": "IV", "D": "III"},
                [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                 {"A": "I", "B": "II", "C": "III", "D": "IV"}], at="A"),
  "A",
  "Synovial joints",
  "Gliding and saddle joints are both in the hand, which is the trap: gliding joints are between the carpals; the "
  "saddle joint is between the carpal and metacarpal of the thumb.",
  ["Ball and socket → humerus and pectoral girdle (II)", "Hinge → knee (I)", "Gliding → between carpals (IV)",
   "Saddle → carpal–metacarpal of thumb (III)"],
  R_LOC("joints"), seconds=40)

_o = ["(b), (c) and (e) only", "(a), (d) and (e) only", "(a), (b), (c), (d) and (e)", "(a), (b), (c) and (d) only"]
ms_check("abcd", _o, "D")
Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("Which of the following statements about contractile proteins are correct?",
     ["Each actin (thin) filament is made of two F-actins helically wound to each other.",
      "Each F-actin is a polymer of monomeric G-actins.",
      "In the resting state, a subunit of troponin masks the active binding sites for myosin on the actin "
      "filaments.",
      "Each myosin (thick) filament is a polymer of monomeric proteins called meromyosins.",
      "The tail of the meromyosin, the light meromyosin (LMM), has ATPase activity."]),
  _o, "D",
  "Actin and myosin",
  "Thin filaments are two helically wound F-actins (polymers of G-actin) with tropomyosin running along them and "
  "troponin at intervals. Thick filaments are polymers of meromyosin. Each meromyosin has a globular head with a "
  "short arm (heavy meromyosin, HMM) and a tail (light meromyosin, LMM). The globular head is the active ATPase and "
  "has binding sites for ATP and actin.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: ATPase activity is in the globular head (HMM part)"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="(e) moves the ATPase from the head to the tail; the head is what binds actin and ATP.",
  seconds=60)

Z(LOC, "Skeletal system", "Advanced", "statement_pair",
  sp("The scapula is situated in the dorsal part of the thorax between the fourth and the tenth ribs.",
     "The clavicle articulates with the acromion, a flat expanded process of the spine of the scapula."),
  STATEMENT_PAIR, "D",
  "Pectoral girdle",
  "Each scapula is a large triangular flat bone in the dorsal part of the thorax between the second and the seventh "
  "ribs: Statement I is false. Its spine projects as a flat, expanded process, the acromion, with which the clavicle "
  "articulates: Statement II is true.",
  ["Scapula lies between the 2nd and 7th ribs → I false", "Clavicle articulates with the acromion → II true"],
  R_LOC("skeletal system: pectoral girdle"), seconds=40)

# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Neuron and nerves", "Basic", "direct",
  "In a neuron, Nissl's granules are found in the:",
  ["Axon only", "Cell body and dendrites", "Synaptic knobs", "Myelin sheath"], "B",
  "Structure of a neuron",
  "The cell body contains cytoplasm with typical organelles and granular bodies called Nissl's granules. The short, "
  "repeatedly branching dendrites also contain Nissl's granules. The axon does not.",
  ["Cell body → Nissl's granules", "Dendrites → Nissl's granules", "Axon → long fibre ending in synaptic knobs"],
  R_NEU("neuron as structural and functional unit of neural system"), seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The neural system of Hydra is composed of:",
  ["A brain with a number of ganglia", "A network of neurons",
   "A central neural system of brain and spinal cord", "A dorsal hollow nerve cord"], "B",
  "Neural organisation in animals",
  "Neural organisation is very simple in lower invertebrates; in Hydra it is a network of neurons. Insects have a "
  "brain with a number of ganglia, and vertebrates have a more developed neural system.",
  ["Hydra → network of neurons", "Insects → brain + ganglia", "Vertebrates → more developed system"],
  R_NEU("neural system"), seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The hindbrain of humans comprises the:",
  ["Pons, cerebellum and medulla oblongata", "Thalamus, hypothalamus and cerebrum",
   "Corpora quadrigemina and cerebral aqueduct", "Cerebrum, pons and medulla oblongata"], "A",
  "Divisions of the human brain",
  "The forebrain consists of the cerebrum, thalamus and hypothalamus. The midbrain carries the corpora quadrigemina "
  "and the cerebral aqueduct. The hindbrain comprises the pons, cerebellum and medulla oblongata.",
  ["Forebrain → cerebrum, thalamus, hypothalamus", "Midbrain → corpora quadrigemina, cerebral aqueduct",
   "Hindbrain → pons, cerebellum, medulla"],
  R_NEU("central neural system"), seconds=25)

Z(NEU, "Nervous system divisions", "Basic", "statement_pair",
  sp("The autonomic neural system is further classified into the sympathetic and the parasympathetic neural "
     "systems.",
     "Afferent nerve fibres transmit impulses from the CNS to the peripheral tissues and organs."),
  STATEMENT_PAIR, "C",
  "Divisions of the peripheral neural system",
  "The PNS has afferent and efferent fibres. Afferent fibres carry impulses from tissues and organs to the CNS; "
  "efferent fibres carry regulatory impulses from the CNS to the tissues. So Statement II is false. The autonomic "
  "neural system is classified into sympathetic and parasympathetic systems: Statement I is true.",
  ["ANS → sympathetic + parasympathetic (I true)", "Afferent = towards CNS; efferent = away from CNS (II false)"],
  R_NEU("human neural system"), seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "numerical",
  "In each cycle, the sodium-potassium pump transports 3 Na⁺ out of the axon and 2 K⁺ into it. After 150 cycles, the "
  "net number of positive charges moved from inside to outside the axon is:",
  ["450", "300", "150", "750"], "C",
  "Electrogenic nature of the Na⁺–K⁺ pump",
  "Each cycle moves 3 positive charges out and 2 in, a net outward movement of one positive charge. This helps make "
  "the outer surface of the resting membrane positive and the inner surface negative.",
  ["Net per cycle = 3 − 2 = 1 positive charge outward", "150 cycles × 1 = 150"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="450 counts only the Na⁺ moved out; 300 counts only the K⁺ moved in; 750 adds both instead of "
                   "taking the difference.", seconds=45, verified_by=RECOMPUTED)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("In a resting neuron, the inner surface of the axonal membrane is negatively charged with respect to the outer "
     "surface.",
     "The resting axonal membrane is more permeable to Na⁺ than to K⁺."),
  ASSERTION_REASON, "C",
  "Resting membrane potential",
  "The resting membrane is polarised: inside negative, outside positive. A is true. The resting axonal membrane is "
  "comparatively more permeable to K⁺ and nearly impermeable to Na⁺, and the Na⁺–K⁺ pump maintains the ionic "
  "gradients. R reverses the permeabilities, so R is false.",
  ["Polarised membrane: inside negative → A true", "Resting membrane: more permeable to K⁺, not Na⁺ → R false"],
  R_NEU("generation and conduction of nerve impulse"), seconds=40)

Z(NEU, "Nervous system divisions", "Intermediate", "match_list",
  ml(("part of the brain", "feature"), ["Corpora quadrigemina", "Medulla oblongata", "Corpus callosum", "Thalamus"],
     ["Tract of nerve fibres connecting the two cerebral hemispheres",
      "Four round swellings on the dorsal portion of the midbrain",
      "Major coordinating centre for sensory and motor signalling",
      "Centres controlling respiration, cardiovascular reflexes and gastric secretions"]),
  match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "I", "B": "IV", "C": "II", "D": "III"},
                 {"A": "IV", "B": "II", "C": "I", "D": "III"}], at="B"),
  "B",
  "Parts of the human brain and their roles",
  "Locate each part first (forebrain, midbrain or hindbrain), then recall its feature.",
  ["Corpora quadrigemina → four lobes on dorsal midbrain (II)", "Medulla → respiration, cardiovascular reflexes, "
   "gastric secretions (IV)", "Corpus callosum → connects cerebral hemispheres (I)",
   "Thalamus → coordinating centre for sensory and motor signalling (III)"],
  R_NEU("central neural system"), seconds=45)

_o = ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c), (d) and (e)", "(a), (b), (c) and (d) only"]
ms_check("abcd", _o, "D")
Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "multi_statement",
  ms("Which of the following statements about synapses are correct?",
     ["Electrical synapses are rare in our neural system.",
      "Impulse transmission across an electrical synapse is faster than across a chemical synapse.",
      "At a chemical synapse, the pre- and post-synaptic membranes are separated by a fluid-filled synaptic cleft.",
      "Neurotransmitters bind to specific receptors present on the post-synaptic membrane.",
      "Impulse transmission across an electrical synapse requires the release of neurotransmitters."]),
  _o, "D",
  "Transmission of impulses",
  "At electrical synapses the membranes are in very close proximity and current flows directly from one neuron to "
  "the next, so transmission is faster; such synapses are rare. At chemical synapses neurotransmitters cross the "
  "synaptic cleft and bind receptors on the post-synaptic membrane.",
  ["(a) True", "(b) True", "(c) True", "(d) True",
   "(e) False: current flows directly across an electrical synapse; neurotransmitters are used at chemical synapses"],
  R_NEU("transmission of impulses"), seconds=50)

Z(NEU, "Neuron and nerves", "Intermediate", "statement_pair",
  sp("Myelinated nerve fibres are enveloped by Schwann cells, which form a myelin sheath around the axon.",
     "Unmyelinated nerve fibres are commonly found in the spinal and cranial nerves."),
  STATEMENT_PAIR, "C",
  "Myelinated and unmyelinated fibres",
  "In myelinated fibres, Schwann cells form a myelin sheath with gaps called nodes of Ranvier: Statement I is true. "
  "Myelinated fibres are the ones found in spinal and cranial nerves; unmyelinated fibres are commonly found in the "
  "autonomous and the somatic neural systems: Statement II is false.",
  ["Schwann cells form myelin sheath → I true",
   "Spinal and cranial nerves → myelinated, not unmyelinated → II false"],
  R_NEU("neuron as structural and functional unit of neural system"), seconds=35)

Z(NEU, "Nervous system divisions", "Advanced", "assertion_reason",
  ar("The hypothalamus contains several groups of neurosecretory cells, which secrete hypothalamic hormones.",
     "The hypothalamus contains a number of centres that control body temperature and the urge for eating and "
     "drinking."),
  ASSERTION_REASON, "B",
  "Functions of the hypothalamus",
  "Both statements are NCERT facts about the hypothalamus, which lies at the base of the thalamus. But controlling "
  "body temperature and appetite is a separate function from secreting hormones; R does not explain why the "
  "hypothalamus has neurosecretory cells.",
  ["A: neurosecretory cells → hypothalamic hormones → true",
   "R: centres for body temperature, eating, drinking → true", "Two independent functions → R does not explain A"],
  R_NEU("central neural system: forebrain"), seconds=40)

_o = ["(a), (b) and (c) only", "(a) and (d) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)"]
ms_check("abc", _o, "A")
Z(NEU, "Nervous system divisions", "Advanced", "multi_statement",
  ms("Which of the following statements about the human brain are correct?",
     ["The cranial meninges consist of an outer dura mater, a very thin middle arachnoid and an inner pia mater in "
      "contact with the brain tissue.",
      "The cerebral cortex is referred to as the grey matter due to its greyish appearance.",
      "The cerebral cortex has large association areas that are neither clearly sensory nor motor in function.",
      "The cerebellum has a smooth surface with relatively few neurons."]),
  _o, "A",
  "Structure of the brain",
  "The brain is protected by three meninges. The cerebral cortex (grey matter) contains motor areas, sensory areas "
  "and large association areas responsible for complex functions such as intersensory associations, memory and "
  "communication. The cerebellum has a very convoluted surface to provide additional space for many more neurons.",
  ["(a) True", "(b) True", "(c) True", "(d) False: the cerebellum is highly convoluted, with many neurons"],
  R_NEU("central neural system"), seconds=50)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "direct",
  "When a stimulus is applied at a site on a polarised axonal membrane, which sequence of events is correct?",
  ["Rise in permeability to K⁺ → K⁺ diffuses out → inside becomes positive → Na⁺ influx restores the resting "
   "potential",
   "Membrane becomes freely permeable to Na⁺ → rapid efflux of Na⁺ → inside becomes more negative → K⁺ moves in",
   "K⁺ rushes into the axon → inside becomes positive → Na⁺ diffuses out → resting potential restored",
   "Membrane becomes freely permeable to Na⁺ → rapid influx of Na⁺ → reversal of polarity (inside positive) → rise "
   "in permeability to K⁺ → K⁺ diffuses out and the resting potential is restored"], "D",
  "Action potential: depolarisation and repolarisation",
  "At the stimulated site the membrane becomes freely permeable to Na⁺, leading to a rapid influx of Na⁺ and a "
  "reversal of polarity: the outer surface becomes negative and the inner surface positive (depolarised). This rise "
  "in Na⁺ permeability is short-lived and is quickly followed by a rise in permeability to K⁺. K⁺ diffuses out and "
  "restores the resting potential.",
  ["Na⁺ channels open → Na⁺ influx", "Polarity reverses → action potential",
   "K⁺ permeability rises → K⁺ efflux → resting potential restored"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="The other sequences reverse the direction of Na⁺ or K⁺ movement or put K⁺ first.", seconds=60)

Z(NEU, "Neuron and nerves", "Advanced", "statement_pair",
  sp("The branches of an axon end in bulb-like synaptic knobs that contain synaptic vesicles filled with "
     "neurotransmitters.",
     "Unipolar neurons, with a cell body and one axon only, are usually found in the embryonic stage."),
  STATEMENT_PAIR, "A",
  "Structure and types of neurons",
  "Both statements are NCERT facts. The axon's distal end branches, and each branch ends in a synaptic knob with "
  "synaptic vesicles holding neurotransmitters. By number of axons and dendrites, neurons are multipolar (cerebral "
  "cortex), bipolar (retina) or unipolar (usually in the embryonic stage).",
  ["Synaptic knobs with vesicles of neurotransmitters → I true", "Unipolar → embryonic stage → II true"],
  R_NEU("neuron as structural and functional unit of neural system"), seconds=40)


# ---------------------------------------------------------------- checks and output
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_001_ZOO_p1.json"


def check_plan():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if s["subject"] == ZOO)
    pkg = next(p for p in subj["packages"] if p["package"] == "ZOO_001_p1")
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, (have - planned, planned - have)
    assert len(QUESTIONS) == pkg["count"] == LAST_ID - FIRST_ID + 1
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_ZOO_{n:06d}" for n in range(FIRST_ID, LAST_ID + 1)]
    assert pkg["question_ids"] == [QUESTIONS[0]["question_id"], QUESTIONS[-1]["question_id"]]
    assert pkg["output"] == "batches/parts/BATCH_001_ZOO_p1.json"
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "BATCH_001 package ZOO_001_p1: 122 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook; every "
                    "numerical answer re-derived by tools/batch_001/ZOO_001_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
