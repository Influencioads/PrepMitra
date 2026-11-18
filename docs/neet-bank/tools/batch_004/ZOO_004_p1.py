"""Writes batches/parts/BATCH_004_ZOO_p1.json: package ZOO_004_p1 of BATCH_004 (Zoology, 121 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_000751 .. NEET_ZOO_000871. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, subtopics, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11
Biology textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion and absorption). Facts
already tested in BATCH_000 to BATCH_003 (see `merge_batch.py stems 004 ZOO_004_p1`) are not tested again.

    python docs/neet-bank/tools/batch_004/ZOO_004_p1.py
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
PACKAGE = "ZOO_004_p1"
BATCH = "BATCH_004"
FIRST_ID, LAST_ID = 751, 871
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


# ---------------------------------------------------------------- verification of computable answers
# Breathing: TLC = RV + ERV + TV + IRV and IC = TV + IRV, so ERV = TLC - RV - IC.
TLC, RV, IC = 5800, 1200, 3500
ERV = TLC - RV - IC
assert ERV == 1100
assert TLC - IC == 2300 and TLC - RV == 4600 and TLC - RV - IC - 500 == 600   # distractors: FRC; VC; TV removed twice

# Breathing: of 200 mL CO2 carried per minute, about 70 % as bicarbonate and about 7 % dissolved in plasma.
CO2_BICARB, CO2_DISSOLVED = 200 * F(70, 100), 200 * F(7, 100)
assert (CO2_BICARB, CO2_DISSOLVED) == (140, 14)
assert 200 * F(25, 100) == 50 and 200 * F(97, 100) == 194 and 200 * F(3, 100) == 6   # carbamino share; O2 split

# Body fluids: 14 g haemoglobin per 100 mL of blood, 5 L (5000 mL) of blood.
HB_TOTAL = F(14, 100) * 5000
assert HB_TOTAL == 700
assert 14 * 5 == 70 and 14 * 10 == 140 and F(14, 10) * 5000 == 7000                 # per-litre slip; per-10-mL slip

# Body fluids: 5 million RBCs per mm3; 1 L = 1000 mL = 1000 cm3 = 10^6 mm3.
RBC_PER_L = 5 * 10 ** 6 * 10 ** 6
assert RBC_PER_L == 5 * 10 ** 12
assert 5 * 10 ** 6 * 10 ** 3 == 5 * 10 ** 9                                           # per mL, not per L

# Body fluids: recipients of group A blood are groups A and AB (anti-A absent from their plasma).
WARD = {"A": 12, "B": 9, "AB": 4, "O": 15}
CAN_RECEIVE_A = WARD["A"] + WARD["AB"]
assert CAN_RECEIVE_A == 16
assert WARD["A"] + WARD["O"] == 27 and WARD["A"] == 12 and WARD["A"] + WARD["AB"] + WARD["O"] == 31

# Excretion: GFR 125 mL/min -> filtrate per day; PCT taken to reabsorb 75 % of it.
FILTRATE_L = F(125 * 60 * 24, 1000)
assert FILTRATE_L == 180
LEAVES_PCT = FILTRATE_L * F(25, 100)
assert LEAVES_PCT == 45
assert FILTRATE_L * F(75, 100) == 135 and F(125 * 60, 1000) == F(15, 2)             # reabsorbed; per hour only
assert FILTRATE_L * F(1, 100) == F(18, 10)                                            # urine at 99 % reabsorption


# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "The body of sponges is supported by a skeleton made up of:",
  ["Calcareous ossicles", "Spicules or spongin fibres", "A chitinous exoskeleton",
   "A calcareous shell secreted by the mantle"], "B",
  "Features of Porifera",
  "NCERT: in sponges (phylum Porifera) the body is supported by a skeleton made up of spicules or spongin fibres. "
  "Calcareous ossicles form the endoskeleton of echinoderms, a chitinous exoskeleton covers arthropods, and molluscs "
  "are covered by a calcareous shell.",
  ["Porifera → skeleton of spicules or spongin fibres", "Ossicles → Echinodermata; chitin → Arthropoda; shell → Mollusca"],
  R_AK("phylum Porifera"),
  why_others_wrong="Calcareous ossicles belong to echinoderms, the chitinous exoskeleton to arthropods and the "
                   "calcareous shell to molluscs.",
  seconds=20)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Coelenterates have a central gastro-vascular cavity with a single opening, the mouth on the hypostome. In them, "
  "digestion is:",
  ["Only intracellular", "Only extracellular", "Absent, nutrients being absorbed through the body surface",
   "Both extracellular and intracellular"], "D",
  "Digestion in Coelenterata",
  "NCERT: coelenterates have a central gastro-vascular cavity with a single opening, the mouth on the hypostome, and "
  "digestion is extracellular and intracellular.",
  ["Gastro-vascular cavity with one opening (mouth on hypostome)", "Digestion → extracellular and intracellular"],
  R_AK("phylum Coelenterata (Cnidaria)"),
  why_others_wrong="Digestion is neither only intracellular nor only extracellular; absorption through the body "
                   "surface without digestion is described for some parasitic flatworms, not coelenterates.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Which of the following arthropods is cited by NCERT as a 'living fossil'?",
  ["Anopheles", "Culex", "Limulus", "Aedes"], "C",
  "Examples of Arthropoda",
  "Among the NCERT examples of Arthropoda, Limulus (king crab) is the living fossil. Anopheles, Culex and Aedes are "
  "vectors (mosquitoes).",
  ["Limulus (king crab) → living fossil", "Anopheles, Culex, Aedes → vectors"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="Anopheles, Culex and Aedes are listed as vectors, not as a living fossil.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Most birds can fly, but some are flightless. Which of the following is a flightless bird?",
  ["Struthio", "Pavo", "Neophron", "Columba"], "A",
  "Features and examples of Aves",
  "NCERT: the characteristic features of Aves are feathers and the ability to fly, except in flightless birds such as "
  "the ostrich (Struthio). Pavo is the peacock, Neophron the vulture and Columba the pigeon; all of them fly.",
  ["Flightless bird → ostrich (Struthio)", "Pavo, Neophron, Columba → flying birds"],
  R_AK("class Aves"),
  why_others_wrong="Pavo (peacock), Neophron (vulture) and Columba (pigeon) are flying birds.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "match_list",
  ml(("bird genus", "common name"), ["Corvus", "Columba", "Psittacula", "Pavo"],
     ["Peacock", "Parrot", "Crow", "Pigeon"]),
  match_options(M("III", "IV", "II", "I"),
                [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"), M("II", "IV", "III", "I")], at="B"),
  "B",
  "Examples of Aves",
  "NCERT examples of birds: Corvus (crow), Columba (pigeon), Psittacula (parrot), Struthio (ostrich), Pavo "
  "(peacock), Aptenodytes (penguin) and Neophron (vulture).",
  ["Corvus → crow (III)", "Columba → pigeon (IV)", "Psittacula → parrot (II)", "Pavo → peacock (I)"],
  R_AK("class Aves"),
  why_others_wrong="The other codes swap the crow with the pigeon, the parrot with the peacock, or the crow with "
                   "the parrot.",
  seconds=30)

Z(AK, "Basis of classification", "Basic", "statement_pair",
  sp("In diploblastic animals, an undifferentiated layer called mesoglea is present between the ectoderm and the "
     "endoderm.",
     "Coelenterates and ctenophores are diploblastic animals."),
  STATEMENT_PAIR, "A",
  "Diploblastic and triploblastic organisation",
  "NCERT: animals whose cells are arranged in two embryonic layers, an external ectoderm and an internal endoderm, "
  "are diploblastic, e.g. coelenterates; an undifferentiated layer, mesoglea, is present between them. Ctenophores "
  "too are described as diploblastic. Animals with a third (middle) layer, the mesoderm, are triploblastic "
  "(platyhelminthes to chordates).",
  ["Statement I: mesoglea lies between ectoderm and endoderm → true",
   "Statement II: coelenterates and ctenophores are diploblastic → true"],
  R_AK("basis of classification: diploblastic and triploblastic organisation"),
  why_others_wrong="Both statements are NCERT lines, so any option calling one of them false is wrong.",
  seconds=30)

Z(AK, "Basis of classification", "Advanced", "direct",
  "An animal is triploblastic and bilaterally symmetrical, and has a complete alimentary canal with a muscular "
  "pharynx. Its body cavity is not lined by mesoderm; instead, the mesoderm is present as scattered pouches between "
  "the ectoderm and the endoderm. The animal belongs to the phylum:",
  ["Platyhelminthes", "Annelida", "Aschelminthes", "Ctenophora"], "C",
  "Pseudocoelom and the digestive system",
  "A body cavity not lined by mesoderm, with mesoderm in scattered pouches, is a pseudocoelom; such animals are "
  "pseudocoelomates, e.g. aschelminthes. Aschelminthes are also triploblastic, bilaterally symmetrical and have a "
  "complete alimentary canal with a well-developed muscular pharynx. Flatworms are acoelomate with an incomplete gut; "
  "annelids are coelomates; ctenophores are diploblastic.",
  ["Mesoderm as scattered pouches → pseudocoelom", "Pseudocoelomate + complete gut with muscular pharynx → "
   "Aschelminthes"],
  R_AK("basis of classification: coelom; phylum Aschelminthes"),
  why_others_wrong="Platyhelminthes have no body cavity and an incomplete digestive system; Annelida have a true "
                   "coelom; Ctenophora are diploblastic.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("Echinoderms have no excretory system.",
     "In echinoderms, the digestive system is complete, with the mouth on the lower (ventral) side and the anus on "
     "the upper (dorsal) side."),
  ASSERTION_REASON, "B",
  "Features of Echinodermata",
  "Both are NCERT statements about echinoderms: the digestive system is complete with a ventral mouth and a dorsal "
  "anus, and an excretory system is absent. The position of the mouth and anus says nothing about why an excretory "
  "system is lacking, so R does not explain A.",
  ["A: excretory system absent → true", "R: complete gut, mouth ventral, anus dorsal → true",
   "R describes the gut, a different organ system → not the explanation"],
  R_AK("phylum Echinodermata"),
  why_others_wrong="A wrongly links the two facts; C and D call a true statement false.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("In hemichordates, a rudimentary structure in the collar region, called the stomochord, is similar to the "
     "notochord.",
     "Hemichordates are exclusively freshwater animals."),
  STATEMENT_PAIR, "C",
  "Features of Hemichordata",
  "NCERT: Hemichordata consists of a small group of worm-like marine animals. They have a rudimentary structure in "
  "the collar region called the stomochord, a structure similar to the notochord. Statement II is false because "
  "hemichordates are marine.",
  ["Statement I: stomochord in the collar region, similar to notochord → true",
   "Statement II: hemichordates are marine, not freshwater → false"],
  R_AK("phylum Hemichordata"),
  why_others_wrong="A and D accept the false habitat; B rejects the true stomochord statement.",
  seconds=30)

Z(AK, "Chordate classes", "Intermediate", "direct",
  "In one class of vertebrates the forelimbs are modified into wings, while the hind limbs generally have scales and "
  "are modified for walking, swimming or clasping tree branches. The class is:",
  ["Reptilia", "Mammalia", "Amphibia", "Aves"], "D",
  "Limbs of birds",
  "NCERT (Aves): the forelimbs are modified into wings, and the hind limbs generally have scales and are modified "
  "for walking, swimming or clasping the tree branches.",
  ["Forelimbs → wings", "Hind limbs scaly, for walking, swimming or clasping → Aves"],
  R_AK("class Aves"),
  why_others_wrong="No reptile, mammal or amphibian has forelimbs modified into feathered wings described this way.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("animal", "common name"), ["Spongilla", "Euspongia", "Ancylostoma", "Hirudinaria"],
     ["Hookworm", "Blood-sucking leech", "Bath sponge", "Fresh water sponge"]),
  match_options(M("IV", "III", "I", "II"),
                [M("III", "IV", "I", "II"), M("IV", "III", "II", "I"), M("III", "IV", "II", "I")], at="A"),
  "A",
  "Examples of Porifera, Aschelminthes and Annelida",
  "NCERT examples: Spongilla (fresh water sponge) and Euspongia (bath sponge) are poriferans; Ancylostoma (hookworm) "
  "is an aschelminth; Hirudinaria (blood-sucking leech) is an annelid.",
  ["Spongilla → fresh water sponge (IV)", "Euspongia → bath sponge (III)", "Ancylostoma → hookworm (I)",
   "Hirudinaria → blood-sucking leech (II)"],
  R_AK("phyla Porifera, Aschelminthes and Annelida"),
  why_others_wrong="The other codes swap the two sponges, or the hookworm with the leech.",
  seconds=35)

_o = ["(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (b) and (d) only", "(a), (d) and (e) only"]
ms_check("abd", _o, "C")
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements are correct?",
     ["In annelids, the neural system consists of paired ganglia connected by lateral nerves to a double ventral "
      "nerve cord.",
      "Aschelminthes have an excretory tube that removes body wastes from the body cavity through the excretory "
      "pore.",
      "Molluscs have a segmented body covered by a chitinous exoskeleton.",
      "In arthropods, excretion takes place through Malpighian tubules.",
      "Platyhelminthes are triploblastic and coelomate."]),
  _o, "C",
  "Organ systems of non-chordates",
  "NCERT: the annelid neural system has paired ganglia connected by lateral nerves to a double ventral nerve cord; "
  "in aschelminthes an excretory tube removes body wastes from the body cavity through the excretory pore; arthropods "
  "excrete through Malpighian tubules. Molluscs are unsegmented and covered by a calcareous shell (a chitinous "
  "exoskeleton belongs to arthropods). Flatworms are triploblastic but acoelomate.",
  ["(a) True", "(b) True", "(c) False: molluscs are unsegmented with a calcareous shell", "(d) True",
   "(e) False: flatworms are acoelomate"],
  R_AK("phyla Platyhelminthes to Mollusca"),
  why_others_wrong="A leaves out (d) and includes the false (c); B and D include false statements (c) or (e).",
  seconds=55)

Z(AK, "Chordate classes", "Intermediate", "assertion_reason",
  ar("The class name Reptilia refers to the mode of locomotion of its members.",
     "Reptiles have a creeping or crawling mode of locomotion (Latin repere or reptum, to creep or crawl)."),
  ASSERTION_REASON, "A",
  "Reptilia: origin of the name",
  "NCERT: the class name Reptilia refers to their creeping or crawling mode of locomotion (Latin, repere or reptum, "
  "to creep or crawl). The creeping locomotion described in R is exactly why the class carries this name.",
  ["A: name refers to locomotion → true", "R: creeping or crawling locomotion → true", "R gives the basis of the name "
   "→ correct explanation"],
  R_AK("class Reptilia"),
  why_others_wrong="B denies the direct link given by NCERT; C and D call a true statement false.",
  seconds=25)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("Members of Chondrichthyes are cold-blooded (poikilothermous), i.e. they lack the capacity to regulate their "
     "body temperature.",
     "In Chondrichthyes, the notochord is persistent throughout life."),
  STATEMENT_PAIR, "A",
  "Features of Chondrichthyes",
  "NCERT lists both for cartilaginous fishes: the notochord is persistent throughout life, and they are cold-blooded "
  "(poikilothermous) animals, i.e. they lack the capacity to regulate their body temperature.",
  ["Statement I: poikilothermous → true", "Statement II: notochord persists throughout life → true"],
  R_AK("class Chondrichthyes"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "Ctenophores reproduce only by sexual means. In them, fertilisation and development are:",
  ["Internal fertilisation with direct development", "External fertilisation with indirect development",
   "Internal fertilisation with indirect development", "External fertilisation with direct development"], "B",
  "Reproduction in Ctenophora",
  "NCERT (Ctenophora): sexes are not separate, reproduction takes place only by sexual means, and fertilisation is "
  "external with indirect development.",
  ["Fertilisation → external", "Development → indirect"],
  R_AK("phylum Ctenophora"),
  why_others_wrong="Fertilisation in ctenophores is not internal, and development is not direct.",
  seconds=25)

_o = ["(a), (b), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]
ms_check("abd", _o, "B")
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following statements about reproduction and development in vertebrates are correct?",
     ["Reptiles are oviparous and development is direct.",
      "Amphibians are oviparous and development is indirect.",
      "In birds, fertilisation is external.",
      "In mammals, development is direct.",
      "Birds show indirect development with a free-living larval stage."]),
  _o, "B",
  "Reproduction across vertebrate classes",
  "NCERT: Reptilia - fertilisation internal, oviparous, development direct. Amphibia - fertilisation external, "
  "oviparous, development indirect. Aves - fertilisation internal, oviparous, development direct. Mammalia - "
  "fertilisation internal, viviparous with a few exceptions, development direct.",
  ["(a) True", "(b) True", "(c) False: fertilisation is internal in birds", "(d) True",
   "(e) False: development is direct in birds"],
  R_AK("classes Amphibia, Reptilia, Aves and Mammalia"),
  why_others_wrong="A, C and D include (c) or (e), both false for birds.",
  seconds=55)

Z(AK, "Basis of classification", "Advanced", "match_list",
  ml(("animal", "body plan"), ["Sycon", "Pleurobrachia", "Fasciola", "Asterias (adult)"],
     ["Bilaterally symmetrical, triploblastic and acoelomate",
      "Cellular level of organisation",
      "Radially symmetrical, triploblastic and coelomate",
      "Radially symmetrical, diploblastic, with tissue level of organisation"]),
  match_options(M("II", "IV", "I", "III"),
                [M("II", "III", "I", "IV"), M("IV", "II", "I", "III"), M("II", "IV", "III", "I")], at="C"),
  "C",
  "Applying the basis of classification",
  "Sycon is a sponge (cellular level). Pleurobrachia is a ctenophore: radially symmetrical, diploblastic, tissue "
  "level. Fasciola (liver fluke) is a flatworm: bilaterally symmetrical, triploblastic and acoelomate. Adult "
  "echinoderms such as Asterias are radially symmetrical, triploblastic and coelomate (their larvae are bilateral).",
  ["Sycon → II", "Pleurobrachia → IV", "Fasciola → I", "Asterias (adult) → III"],
  R_AK("basis of classification; phyla Porifera, Ctenophora, Platyhelminthes and Echinodermata"),
  why_others_wrong="The other codes give the starfish a diploblastic plan, call the sponge diploblastic, or give the "
                   "fluke a coelom.",
  seconds=60)

Z(AK, "Non-chordate phyla", "Advanced", "assertion_reason",
  ar("In cnidarians, the polyp is a free-swimming, umbrella-shaped form.",
     "Cnidarians exhibit two basic body forms, called polyp and medusa."),
  ASSERTION_REASON, "D",
  "Polyp and medusa",
  "NCERT: cnidarians exhibit two basic body forms. The polyp is a sessile and cylindrical form like Hydra and "
  "Adamsia; the medusa is umbrella-shaped and free-swimming like Aurelia (jelly fish). A gives the polyp the "
  "features of the medusa, so A is false; R is true.",
  ["Polyp → sessile, cylindrical (Hydra, Adamsia)", "Medusa → umbrella-shaped, free-swimming (Aurelia)",
   "A false, R true"],
  R_AK("phylum Coelenterata (Cnidaria)"),
  why_others_wrong="A, B and C all treat the false assertion as true.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Advanced", "statement_pair",
  sp("In Platyhelminthes, fertilisation is internal and development is through many larval stages.",
     "In Aschelminthes, fertilisation is external and development is always direct."),
  STATEMENT_PAIR, "C",
  "Reproduction in flatworms and roundworms",
  "NCERT: in flatworms, fertilisation is internal and development is through many larval stages. In aschelminthes, "
  "fertilisation is internal and development may be direct (the young ones resemble the adult) or indirect. "
  "Statement II is wrong on both counts.",
  ["Statement I → true", "Statement II: fertilisation internal; development direct or indirect → false"],
  R_AK("phyla Platyhelminthes and Aschelminthes"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=35)

_o = ["(b), (c) and (e) only", "(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(a), (c) and (d) only"]
ms_check("abc", _o, "C")
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["In cyclostomes, the circulation is of the closed type.",
      "Cyclostomes are ectoparasites on some fishes.",
      "Cyclostomes have 6–15 pairs of gill slits for respiration.",
      "In bony fishes, the skin is covered with placoid scales.",
      "In mammals, the heart is three-chambered."]),
  _o, "C",
  "Cyclostomata compared with other vertebrates",
  "NCERT (Cyclostomata): all living members are ectoparasites on some fishes; they have 6–15 pairs of gill slits for "
  "respiration, and circulation is of the closed type. Bony fishes have cycloid or ctenoid scales (placoid scales "
  "belong to cartilaginous fishes). Mammals have a four-chambered heart.",
  ["(a) True", "(b) True", "(c) True", "(d) False: bony fishes bear cycloid/ctenoid scales",
   "(e) False: the mammalian heart is four-chambered"],
  R_AK("classes Cyclostomata, Osteichthyes and Mammalia"),
  why_others_wrong="A includes (e); B and D include (d), which is true only for cartilaginous fishes.",
  seconds=55)


# ================================================================ Structural Organisation in Animals (B4 I6 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Cartilage is present in adults at all of the following sites EXCEPT:",
  ["Tip of the nose", "Outer ear joints", "Walls of the stomach and intestine", "Limbs and hands"], "C",
  "Location of cartilage",
  "NCERT: cartilage is present in the tip of the nose, outer ear joints, between adjacent bones of the vertebral "
  "column, and limbs and hands in adults. The walls of the stomach and intestine are made of smooth muscle and are "
  "lined by columnar epithelium; they have no cartilage.",
  ["Cartilage sites: nose tip, outer ear joints, between vertebrae, limbs and hands",
   "Stomach and intestine walls → smooth muscle, columnar epithelium"],
  R_SOA("animal tissues: specialised connective tissue (cartilage)"),
  why_others_wrong="The tip of the nose, outer ear joints and the limbs and hands of adults all contain cartilage.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "The scientific name of the common Indian frog described in NCERT is:",
  ["Hyla", "Rana tigrina", "Bufo", "Ichthyophis"], "B",
  "The frog",
  "NCERT: the most common species of frog found in India is Rana tigrina. Hyla is the tree frog, Bufo the toad and "
  "Ichthyophis a limbless amphibian.",
  ["Common Indian frog → Rana tigrina"],
  R_SOA("frog"),
  why_others_wrong="Hyla (tree frog), Bufo (toad) and Ichthyophis (limbless amphibian) are other amphibians.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "Which of the following is NOT a part of the excretory system of the frog?",
  ["A pair of kidneys", "Ureters", "Urinary bladder", "Malpighian tubules"], "D",
  "Excretory system of the frog",
  "NCERT: the elimination of nitrogenous wastes in the frog is carried out by a well-developed excretory system made "
  "of a pair of kidneys, ureters, the cloaca and the urinary bladder. Malpighian tubules are the excretory organs of "
  "insects and other arthropods.",
  ["Frog excretory system → kidneys, ureters, cloaca, urinary bladder", "Malpighian tubules → arthropods"],
  R_SOA("frog: anatomy (excretory system)"),
  why_others_wrong="Kidneys, ureters and the urinary bladder are all parts of the frog's excretory system.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Epithelial tissue has a free surface, which faces either a body fluid or the outside environment.",
     "In epithelial tissue, the cells are loosely packed with a large amount of intercellular matrix."),
  STATEMENT_PAIR, "C",
  "General features of epithelium",
  "NCERT: epithelial tissue has a free surface which faces either a body fluid or the outside environment and thus "
  "provides a covering or lining for some part of the body. The cells are compactly packed with little intercellular "
  "matrix, so Statement II is false.",
  ["Statement I: free surface → true", "Statement II: cells are compactly packed, little matrix → false"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=25)

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "When a neuron is suitably stimulated, an electrical disturbance is generated which swiftly travels along its "
  "plasma membrane. The arrival of this disturbance at the neuron's endings, or output zone:",
  ["Triggers stimulation or inhibition of adjacent neurons and other cells",
   "Always makes the neuron itself contract",
   "Makes the neuron permanently non-excitable",
   "Is passed on only to the neuroglial cells, which store it"], "A",
  "Neural tissue",
  "NCERT: when a neuron is suitably stimulated, an electrical disturbance is generated which swiftly travels along "
  "its plasma membrane. Arrival of the disturbance at the neuron's endings, or output zone, triggers stimulation or "
  "inhibition of adjacent neurons and other cells.",
  ["Stimulus → electrical disturbance along the membrane", "At the output zone → stimulation or inhibition of "
   "adjacent neurons and other cells"],
  R_SOA("animal tissues: neural tissue"),
  why_others_wrong="Neurons are not contractile; they remain excitable; neuroglia protect and support neurons and "
                   "do not store impulses.",
  seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("tissue", "feature"), ["Cartilage", "Dense regular connective tissue", "Adipose tissue", "Blood"],
     ["Specialised to store fats", "Fluid connective tissue that is the main circulating fluid",
      "Collagen fibres present in rows between many parallel bundles of fibres",
      "Solid and pliable intercellular material that resists compression"]),
  match_options(M("IV", "III", "I", "II"),
                [M("III", "IV", "I", "II"), M("IV", "III", "II", "I"), M("II", "III", "I", "IV")], at="D"),
  "D",
  "Types of connective tissue",
  "NCERT: the intercellular material of cartilage is solid and pliable and resists compression. In dense regular "
  "connective tissue the collagen fibres are present in rows between many parallel bundles of fibres (tendons, "
  "ligaments). Adipose tissue, a loose connective tissue, is specialised to store fats. Blood is a fluid connective "
  "tissue and the main circulating fluid that helps in the transport of various substances.",
  ["Cartilage → IV", "Dense regular → III", "Adipose → I", "Blood → II"],
  R_SOA("animal tissues: connective tissue"),
  why_others_wrong="The other codes swap cartilage with dense regular tissue, adipose tissue with blood, or put "
                   "blood against cartilage.",
  seconds=40)

_o = ["(a), (b), (c) and (e) only", "(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c), (d) and (e)"]
ms_check("abce", _o, "A")
Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the alimentary canal of the frog are correct?",
     ["The mouth opens into the buccal cavity, which leads to the oesophagus through the pharynx.",
      "The oesophagus is a short tube that opens into the stomach.",
      "In the stomach, food is digested by the action of HCl and gastric juices.",
      "Partially digested food (chyme) passes from the stomach directly into the rectum.",
      "Undigested solid waste moves into the rectum and passes out through the cloaca."]),
  _o, "A",
  "Alimentary canal of the frog",
  "NCERT: the mouth opens into the buccal cavity that leads to the oesophagus through the pharynx. The oesophagus is "
  "a short tube that opens into the stomach, which continues as the intestine, rectum and finally opens outside by "
  "the cloaca. Food is digested in the stomach by HCl and gastric juices; the partially digested food, chyme, passes "
  "to the first part of the intestine, the duodenum. Undigested solid waste moves into the rectum and passes out "
  "through the cloaca.",
  ["(a) True", "(b) True", "(c) True", "(d) False: chyme passes to the duodenum", "(e) True"],
  R_SOA("frog: anatomy (digestive system)"),
  why_others_wrong="B, C and D include the false (d); B and C also leave out true statements.",
  seconds=50)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("The vascular system of the frog is a well-developed closed type.",
     "The frog also has a lymphatic system consisting of lymph, lymph channels and lymph nodes."),
  ASSERTION_REASON, "B",
  "Circulatory and lymphatic systems of the frog",
  "NCERT: the vascular system of the frog is a well-developed closed type. Frogs have a lymphatic system also, which "
  "consists of lymph, lymph channels and lymph nodes. The lymphatic system is a separate system; its presence does "
  "not explain why the blood vascular system is closed.",
  ["A: closed blood vascular system → true", "R: lymphatic system present → true",
   "R describes a different system → not the explanation"],
  R_SOA("frog: anatomy (circulatory system)"),
  why_others_wrong="A wrongly links two independent facts; C and D call a true statement false.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "In the female frog, the reproductive organs are related to the excretory organs in which way?",
  ["The oviducts join the ureters, which act as urinogenital ducts",
   "The oviducts pass through the kidneys and open into the urinary bladder",
   "The ovaries have no functional connection with the kidneys, and the oviducts open into the cloaca separately",
   "The ovaries open to the exterior through a genital pore separate from the cloaca"], "C",
  "Female reproductive system of the frog",
  "NCERT: the ovaries are situated near the kidneys, and there is no functional connection with the kidneys. A pair "
  "of oviducts arising from the ovaries opens into the cloaca separately. (Only in males do the ureters act as "
  "urinogenital ducts.)",
  ["Ovaries near kidneys but not functionally connected", "Oviducts open into the cloaca separately"],
  R_SOA("frog: anatomy (reproductive system)"),
  why_others_wrong="Ureters act as urinogenital ducts only in males; the oviducts neither pass through the kidneys "
                   "nor open by a separate genital pore.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("The endocrine glands found in the frog include the pituitary, thyroid, parathyroid, thymus, pineal body, "
     "pancreatic islets, adrenals and gonads.",
     "The blood of the frog is composed of plasma and cells: RBCs, WBCs and platelets."),
  STATEMENT_PAIR, "A",
  "Endocrine glands and blood of the frog",
  "NCERT: the prominent endocrine glands found in the frog are the pituitary, thyroid, parathyroid, thymus, pineal "
  "body, pancreatic islets, adrenals and gonads. Frog blood is composed of plasma and cells; the blood cells are RBCs "
  "(erythrocytes), WBCs (leucocytes) and platelets.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("frog: anatomy (endocrine and circulatory systems)"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

_o = ["(a), (b), (c) and (e) only", "(b), (c) and (e) only", "(a), (c) and (d) only", "(a), (b) and (d) only"]
ms_check("abd", _o, "D")
Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("Which of the following statements about animal tissues are correct?",
     ["Gap junctions help cells to communicate with each other by connecting the cytoplasm of adjoining cells, for "
      "rapid transfer of ions, small molecules and sometimes big molecules.",
      "In loose connective tissue, cells and fibres are loosely arranged in a semi-fluid ground substance.",
      "Blood is a loose connective tissue, like areolar tissue.",
      "Neurons, the units of the neural system, are excitable cells.",
      "Smooth muscle forms the contractile wall of the heart."]),
  _o, "D",
  "Junctions, connective, neural and muscle tissue",
  "NCERT: gap junctions connect the cytoplasm of adjoining cells for rapid transfer of ions, small molecules and "
  "sometimes big molecules. Loose connective tissue has cells and fibres loosely arranged in a semi-fluid ground "
  "substance (areolar and adipose tissue). Blood is a specialised (fluid) connective tissue, not a loose connective "
  "tissue. Neurons are excitable cells. The wall of the heart is made of cardiac muscle, which is present only in "
  "the heart.",
  ["(a) True", "(b) True", "(c) False: blood is a specialised (fluid) connective tissue", "(d) True",
   "(e) False: the heart wall is cardiac muscle"],
  R_SOA("animal tissues: cell junctions, connective, muscle and neural tissue"),
  why_others_wrong="A and C include the false (c) or (e); B leaves out true statements and includes (e).",
  seconds=55)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "match_list",
  ml(("structure in the frog", "feature"), ["Lungs", "Gall bladder", "Pancreas", "Duodenum"],
     ["Receives bile and pancreatic juice through a common bile duct",
      "Pair of elongated, pink, sac-like structures in the upper part of the trunk (thorax)",
      "Produces pancreatic juice containing digestive enzymes",
      "Stores bile secreted by the liver"]),
  match_options(M("II", "IV", "III", "I"),
                [M("II", "III", "IV", "I"), M("I", "IV", "III", "II"), M("IV", "II", "I", "III")], at="B"),
  "B",
  "Respiratory and digestive organs of the frog",
  "NCERT: the lungs of the frog are a pair of elongated, pink-coloured sac-like structures in the upper part of the "
  "trunk region (thorax). The liver secretes bile that is stored in the gall bladder. The pancreas, a digestive "
  "gland, produces pancreatic juice containing digestive enzymes. The duodenum receives bile from the gall bladder "
  "and pancreatic juice from the pancreas through a common bile duct.",
  ["Lungs → II", "Gall bladder → IV", "Pancreas → III", "Duodenum → I"],
  R_SOA("frog: anatomy (digestive and respiratory systems)"),
  why_others_wrong="The other codes swap the gall bladder with the pancreas, the lungs with the duodenum, or shift "
                   "every pair.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "assertion_reason",
  ar("Bone is the main tissue that provides the structural frame to the body.",
     "Bone has a very hard and non-pliable ground substance rich in calcium salts and collagen fibres, which give "
     "bone its strength."),
  ASSERTION_REASON, "A",
  "Bone as a specialised connective tissue",
  "NCERT: bones have a hard and non-pliable ground substance rich in calcium salts and collagen fibres which give "
  "bone its strength. It is the main tissue that provides structural frame to the body. The strength from the hard, "
  "mineral-rich matrix is what lets bone act as the body's frame.",
  ["A → true", "R → true", "Hard, strong matrix → structural frame → R explains A"],
  R_SOA("animal tissues: specialised connective tissue (bone)"),
  why_others_wrong="B ignores the link NCERT itself draws; C and D call a true statement false.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "statement_pair",
  sp("The heart of the frog is a muscular structure situated in the lower part of the body cavity.",
     "In the frog, blood from the heart is carried to all parts of the body by the arteries (arterial system)."),
  STATEMENT_PAIR, "D",
  "Circulatory system of the frog",
  "NCERT: the heart of the frog is a muscular structure situated in the upper part of the body cavity, so Statement "
  "I is false. Blood from the heart is carried to all parts of the body by the arteries (arterial system), and the "
  "veins collect blood from different parts of the body to the heart (venous system).",
  ["Statement I: heart in the upper part of the body cavity → false", "Statement II: arterial system → true"],
  R_SOA("frog: anatomy (circulatory system)"),
  why_others_wrong="A and C accept the wrong position of the heart; B rejects the true Statement II.",
  seconds=30)


# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Enzyme classification", "Basic", "direct",
  "Enzymes that catalyse the inter-conversion of optical, geometric or positional isomers are placed in the class:",
  ["Lyases", "Isomerases", "Ligases", "Transferases"], "B",
  "Classes of enzymes",
  "NCERT: isomerases include all enzymes catalysing the inter-conversion of optical, geometric or positional "
  "isomers. Lyases remove groups from substrates by mechanisms other than hydrolysis, leaving double bonds; ligases "
  "catalyse the linking together of two compounds; transferases transfer a group G (other than hydrogen) between a "
  "pair of substrates.",
  ["Inter-conversion of isomers → isomerases"],
  R_BIO("enzymes: classification and nomenclature of enzymes"),
  why_others_wrong="Lyases, ligases and transferases catalyse group removal, linking of compounds and group "
                   "transfer respectively.",
  seconds=20)

Z(BIO, "Nucleic acids", "Basic", "direct",
  "Which of the following nitrogenous bases of nucleic acids is a substituted pyrimidine?",
  ["Adenine", "Guanine", "Ribose", "Cytosine"], "D",
  "Purines and pyrimidines",
  "NCERT: the nitrogenous bases of nucleic acids are adenine, guanine, uracil, cytosine and thymine. Adenine and "
  "guanine are substituted purines; the rest (uracil, cytosine and thymine) are substituted pyrimidines. Ribose is a "
  "sugar, not a base.",
  ["Purines → adenine, guanine", "Pyrimidines → uracil, cytosine, thymine"],
  R_BIO("nucleic acids"),
  why_others_wrong="Adenine and guanine are purines; ribose is a pentose sugar.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "Inorganic catalysts work efficiently at high temperatures and high pressures. According to NCERT, enzymes of most "
  "organisms, in contrast, get damaged at high temperatures, say above:",
  ["20 °C", "40 °C", "80 °C", "100 °C"], "B",
  "Enzymes versus inorganic catalysts",
  "NCERT: inorganic catalysts work efficiently at high temperatures and high pressures, while enzymes get damaged at "
  "high temperatures (say above 40 °C). Only enzymes isolated from organisms living at extremely high temperatures "
  "(hot vents, sulphur springs) remain stable up to 80–90 °C.",
  ["Most enzymes damaged above about 40 °C", "Thermophile enzymes stable up to 80–90 °C"],
  R_BIO("enzymes"),
  why_others_wrong="20 °C is below body temperature; 80 °C and 100 °C are the range only thermostable enzymes of "
                   "thermophiles tolerate.",
  seconds=20)

Z(BIO, "Nucleic acids", "Basic", "statement_pair",
  sp("A nucleotide has three chemically distinct components: a heterocyclic compound, a monosaccharide and a "
     "phosphoric acid or phosphate.",
     "Nucleic acids are polynucleotides."),
  STATEMENT_PAIR, "A",
  "Nucleotides and nucleic acids",
  "NCERT: nucleic acids are polynucleotides; for nucleic acids the building block is a nucleotide. A nucleotide has "
  "three chemically distinct components: a heterocyclic compound (nitrogenous base), a monosaccharide (ribose or "
  "2'-deoxyribose) and a phosphoric acid or phosphate.",
  ["Statement I → true", "Statement II → true"],
  R_BIO("nucleic acids"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=25)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "Which of the following is NOT a protein?",
  ["Insulin", "GLUT-4", "Cellulose", "RuBisCO"], "C",
  "Proteins and polysaccharides",
  "Insulin (a hormone), GLUT-4 (which enables glucose transport into cells) and RuBisCO (the most abundant protein "
  "in the biosphere) are proteins. Cellulose is a polysaccharide, a homopolymer of glucose.",
  ["Insulin, GLUT-4, RuBisCO → proteins", "Cellulose → polysaccharide"],
  R_BIO("proteins; polysaccharides"),
  why_others_wrong="Insulin, GLUT-4 and RuBisCO are all named by NCERT as proteins.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Intermediate", "direct",
  "Amino acids are called α-amino acids because:",
  ["Their amino group and acidic group are substituents on the same carbon, the α-carbon",
   "They are the first (alpha) products formed when proteins are digested",
   "Their R group is always attached to an α-helix",
   "They occur only in the α-chains of haemoglobin"], "A",
  "Structure of amino acids",
  "NCERT: amino acids are organic compounds containing an amino group and an acidic group as substituents on the "
  "same carbon, the α-carbon. Hence they are called α-amino acids.",
  ["Amino group + acidic group on the same (α) carbon → α-amino acids"],
  R_BIO("analysis of chemical composition: amino acids"),
  why_others_wrong="The name refers to the α-carbon, not to digestion products, helices or haemoglobin chains.",
  seconds=25)

Z(BIO, "Enzymes: properties and action", "Intermediate", "assertion_reason",
  ar("Enzymes generally function in a narrow range of temperature and pH.",
     "All enzymes show their highest activity at the same pH."),
  ASSERTION_REASON, "C",
  "Effect of temperature and pH on enzymes",
  "NCERT: enzymes generally function in a narrow range of temperature and pH, and each enzyme shows its highest "
  "activity at a particular temperature and pH called its optimum temperature and optimum pH. The optimum differs "
  "from enzyme to enzyme, so R is false.",
  ["A → true", "R: optimum pH is particular to each enzyme → false"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="A and B accept the false reason; D rejects the true assertion.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Intermediate", "direct",
  "A multistep chemical reaction, in which each of the steps is catalysed by the same enzyme complex or by different "
  "enzymes, is called a:",
  ["Transition state", "Competitive inhibition", "Metabolic pathway", "Enzyme–substrate complex"], "C",
  "Metabolic pathway",
  "NCERT: a multistep chemical reaction, when each of the steps is catalysed by the same enzyme complex or different "
  "enzymes, is called a metabolic pathway. For example, glucose becomes pyruvic acid through ten different "
  "enzyme-catalysed metabolic reactions.",
  ["Many steps, each enzyme-catalysed → metabolic pathway"],
  R_BIO("enzymes: how do enzymes bring about such high rates of chemical conversions"),
  why_others_wrong="A transition state is a high-energy state of the substrate; competitive inhibition is blocking "
                   "by a substrate-like chemical; the ES complex is a single transient intermediate.",
  seconds=25)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "statement_pair",
  sp("A polysaccharide chain such as glycogen has branches.",
     "Complex polysaccharides, such as chitin of the arthropod exoskeleton, are mostly heteropolymers."),
  STATEMENT_PAIR, "C",
  "Polysaccharides",
  "NCERT shows glycogen as a branched polysaccharide chain with a reducing and a non-reducing end. Complex "
  "polysaccharides have amino-sugars and chemically modified sugars as building blocks, and NCERT states that these "
  "complex polysaccharides are mostly homopolymers. So Statement II is false.",
  ["Statement I: glycogen is branched → true", "Statement II: complex polysaccharides are mostly homopolymers → false"],
  R_BIO("polysaccharides"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=30)

Z(BIO, "Proteins and amino acids", "Intermediate", "statement_pair",
  sp("In the secondary structure of a protein, the entire protein thread is arranged in the form of a helix.",
     "The helix seen in the secondary structure of proteins is similar to a revolving staircase."),
  STATEMENT_PAIR, "D",
  "Secondary structure of proteins",
  "NCERT: a protein thread does not exist throughout as an extended rigid rod; it is folded in the form of a helix, "
  "similar to a revolving staircase. Of course, only some portions of the protein thread are arranged as a helix; "
  "other regions are folded into other forms in the secondary structure. So Statement I is false.",
  ["Statement I: only some portions form a helix → false", "Statement II: revolving staircase → true"],
  R_BIO("structure of proteins"),
  why_others_wrong="A and C accept the false Statement I; B rejects the true Statement II.",
  seconds=30)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "direct",
  "Which of the following correctly describes a fatty acid?",
  ["An amino group and an acidic group on the same carbon",
   "Propane carrying three hydroxyl groups",
   "A glycerol molecule esterified with a phosphorylated organic compound",
   "A carboxyl group attached to an R group"], "D",
  "Structure of fatty acids",
  "NCERT: a fatty acid has a carboxyl group attached to an R group; the R group could be a methyl, an ethyl or a "
  "higher number of –CH₂ groups. An amino and an acidic group on the same carbon describe an amino acid; glycerol "
  "is trihydroxy propane; lipids with a phosphorylated organic compound are phospholipids such as lecithin.",
  ["Fatty acid → –COOH attached to R group"],
  R_BIO("analysis of chemical composition: lipids"),
  why_others_wrong="A describes an amino acid, B glycerol and C a phospholipid.",
  seconds=25)

Z(BIO, "Enzymes: properties and action", "Intermediate", "assertion_reason",
  ar("When ice melts into water, no chemical reaction takes place.",
     "A chemical reaction is a transformation in which bonds are broken and new bonds are formed."),
  ASSERTION_REASON, "A",
  "Physical change and chemical reaction",
  "NCERT: a change in state of matter, as when ice melts into water or water becomes vapour, is a physical process. "
  "When bonds are broken and new bonds are formed during a transformation, it is called a chemical reaction. Melting "
  "breaks no covalent bonds and forms none, which is exactly why it is not a chemical reaction; R explains A.",
  ["A: melting is a change of state → physical → true", "R: definition of a chemical reaction → true",
   "No bonds broken or formed in melting → R explains A"],
  R_BIO("enzymes: chemical reactions"),
  why_others_wrong="B misses that the definition in R is the very reason; C and D call a true statement false.",
  seconds=30)

_o = ["(a), (c) and (e) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"]
ms_check("abc", _o, "B")
Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("Which of the following statements are correct according to NCERT?",
     ["There are thousands of types of enzymes, each catalysing a unique chemical or metabolic reaction.",
      "In our skeletal muscle, under normal aerobic conditions, the pathway from glucose forms pyruvic acid.",
      "In our skeletal muscle, under anaerobic conditions, lactic acid is formed.",
      "In an exothermic reaction, energy must be supplied by heating for the product to form.",
      "In yeast, during fermentation, the same glucose pathway leads to the production of lactic acid."]),
  _o, "B",
  "Enzymes and metabolic end products",
  "NCERT: there are thousands of types of enzymes, each catalysing a unique chemical or metabolic reaction. The same "
  "pathway with one or two additional reactions gives a variety of end products: in skeletal muscle, lactic acid "
  "under anaerobic conditions and pyruvic acid under normal aerobic conditions; in yeast during fermentation, ethanol. "
  "If the product is at a lower energy level than the substrate, the reaction is exothermic, and one need not supply "
  "energy (by heating) to form the product.",
  ["(a) True", "(b) True", "(c) True", "(d) False: no heating is needed for an exothermic reaction",
   "(e) False: yeast produces ethanol"],
  R_BIO("enzymes: how do enzymes bring about high rates; nature of enzyme action"),
  why_others_wrong="A includes (e); C includes (d) and (e); D includes (d).",
  seconds=60)

_o = ["(a) and (b) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a) and (d) only"]
ms_check("ab", _o, "A")
Z(BIO, "Nucleic acids", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["Nucleic acids, together with polysaccharides and polypeptides, comprise the true macromolecular fraction of "
      "any living tissue or cell.",
      "The heterocyclic compounds in nucleic acids are the nitrogenous bases adenine, guanine, uracil, cytosine and "
      "thymine.",
      "Lipids are strictly macromolecules, with molecular weights above ten thousand daltons.",
      "Polysaccharides are absent from the acid-insoluble fraction of a living tissue."]),
  _o, "A",
  "Macromolecular fraction and nucleic acids",
  "NCERT: nucleic acids (polynucleotides), together with polysaccharides and polypeptides, comprise the true "
  "macromolecular fraction of any living tissue or cell. The nitrogenous bases are adenine, guanine, uracil, cytosine "
  "and thymine. Lipids, whose molecular weights do not exceed 800 Da, come in the acid-insoluble fraction only "
  "because they form insoluble membrane vesicles; they are not strictly macromolecules. Polysaccharides are part of "
  "the acid-insoluble fraction.",
  ["(a) True", "(b) True", "(c) False: lipids are not strictly macromolecules",
   "(d) False: polysaccharides are in the acid-insoluble fraction"],
  R_BIO("biomacromolecules; nucleic acids"),
  why_others_wrong="B, C and D include (c) or (d), both false.",
  seconds=50)

Z(BIO, "Enzymes: properties and action", "Advanced", "assertion_reason",
  ar("In the presence of an enzyme, the substrate is converted into the product without passing through any "
     "transition state.",
     "An enzyme brings down the energy barrier, making the transition of the substrate into the product easier."),
  ASSERTION_REASON, "D",
  "Activation energy and the transition state",
  "NCERT: whether a reaction is exothermic or endothermic, the substrate has to go through a much higher energy "
  "state, the transition state; the difference in average energy content of S and this transition state is the "
  "activation energy. The enzyme does not remove the transition state; it brings down the energy barrier, making the "
  "transition of S to P easier. So A is false and R is true.",
  ["Transition state is always passed → A false", "Enzyme lowers the activation energy barrier → R true"],
  R_BIO("enzymes: concept of activation energy"),
  why_others_wrong="A, B and C accept the false assertion.",
  seconds=40)

Z(BIO, "Proteins and amino acids", "Advanced", "direct",
  "A protein consists of four separately folded polypeptide subunits arranged with respect to one another in a "
  "definite manner. Which levels of protein structure does this protein show?",
  ["Only the quaternary structure, since its subunits are already folded",
   "Primary and quaternary structures only",
   "Primary, secondary, tertiary and quaternary structures",
   "Primary, secondary and tertiary structures only"], "C",
  "Levels of protein structure",
  "Each polypeptide subunit has a primary structure (amino acid sequence), secondary structure (helices and other "
  "folds) and is folded upon itself into a tertiary structure. NCERT: some proteins are an assembly of more than one "
  "polypeptide or subunit, and the manner in which these individually folded subunits are arranged with respect to "
  "each other (e.g. a linear string of spheres, or spheres arranged one upon another as a cube or plate) is the "
  "quaternary structure. Such a protein therefore shows all four levels.",
  ["Each subunit → primary, secondary, tertiary", "Arrangement of folded subunits → quaternary",
   "All four levels present"],
  R_BIO("structure of proteins"),
  why_others_wrong="Quaternary structure is built on the lower levels, not instead of them; D leaves out the "
                   "arrangement of subunits, which is the quaternary level.",
  seconds=40)

_o = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
ms_check("abc", _o, "B")
Z(BIO, "Proteins and amino acids", "Advanced", "multi_statement",
  ms("Which of the following statements about amino acids are correct?",
     ["Their chemical and physical properties are essentially those of the amino, carboxyl and R functional groups.",
      "Based on the number of amino and carboxyl groups, amino acids may be acidic, basic or neutral.",
      "In alanine, the R group is a methyl group.",
      "Tyrosine is an acidic amino acid.",
      "The twenty types of amino acids found in proteins differ from one another only in their carboxyl group."]),
  _o, "B",
  "Properties of amino acids",
  "NCERT: the chemical and physical properties of amino acids are essentially of the amino, carboxyl and R "
  "functional groups. Based on the number of amino and carboxyl groups, there are acidic (glutamic acid), basic "
  "(lysine) and neutral (valine) amino acids; tyrosine, phenylalanine and tryptophan are aromatic amino acids. The R "
  "group is hydrogen in glycine, methyl in alanine and hydroxy methyl in serine; amino acids differ in their R group.",
  ["(a) True", "(b) True", "(c) True", "(d) False: tyrosine is an aromatic amino acid",
   "(e) False: amino acids differ in the R group"],
  R_BIO("analysis of chemical composition: amino acids"),
  why_others_wrong="A includes (d); C includes (e) and omits (a); D includes (d) and (e).",
  seconds=55)


# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Respiratory system", "Basic", "direct",
  "In humans, the common passage for food and air is a portion of the:",
  ["Larynx", "Trachea", "Nasal chamber", "Pharynx"], "D",
  "Human respiratory passage",
  "NCERT: the nasal chamber opens into the pharynx, a portion of which is the common passage for food and air. The "
  "pharynx opens through the larynx region into the trachea.",
  ["Nasal chamber → pharynx (common passage for food and air) → larynx → trachea"],
  R_BRE("respiratory organs: human respiratory system"),
  why_others_wrong="The larynx and trachea carry only air; the nasal chamber does not carry food.",
  seconds=20)

Z(BRE, "Mechanism of breathing", "Basic", "direct",
  "Breathing works by creating a pressure gradient between the lungs and the atmosphere. In humans, such pressure "
  "gradients are generated with the help of:",
  ["The epiglottis and the vocal cords",
   "The diaphragm and the external and internal inter-costal muscles",
   "The pleural fluid alone",
   "The smooth muscles of the alveolar walls"], "B",
  "Generation of pressure gradients",
  "NCERT: we have the ability to generate pressure gradients through the diaphragm and a specialised set of muscles, "
  "the external and internal inter-costals, between the ribs, which help in the generation of such gradients.",
  ["Pressure gradient → diaphragm + external and internal inter-costal muscles"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="The epiglottis guards the larynx, the pleural fluid reduces friction, and alveoli do not pump "
                   "air.",
  seconds=20)

Z(BRE, "Mechanism of breathing", "Basic", "statement_pair",
  sp("Breathing involves two stages: inspiration, during which atmospheric air is drawn in, and expiration, by which "
     "the alveolar air is released out.",
     "Inspiration is initiated by the relaxation of the diaphragm."),
  STATEMENT_PAIR, "C",
  "Inspiration and expiration",
  "NCERT: breathing involves inspiration, during which atmospheric air is drawn in, and expiration, by which the "
  "alveolar air is released out. Inspiration is initiated by the contraction of the diaphragm, which increases the "
  "volume of the thoracic chamber in the antero-posterior axis. Relaxation of the diaphragm belongs to expiration.",
  ["Statement I → true", "Statement II: inspiration starts with contraction of the diaphragm → false"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Basic", "direct",
  "NCERT lists the steps of respiration in order. Which step immediately follows the diffusion of gases (O₂ and CO₂) "
  "across the alveolar membrane?",
  ["Breathing or pulmonary ventilation", "Transport of gases by the blood",
   "Utilisation of O₂ by the cells for catabolic reactions",
   "Diffusion of O₂ and CO₂ between blood and tissues"], "B",
  "Steps of respiration",
  "NCERT: respiration involves (i) breathing or pulmonary ventilation, (ii) diffusion of gases across the alveolar "
  "membrane, (iii) transport of gases by the blood, (iv) diffusion of O₂ and CO₂ between blood and tissues, and (v) "
  "utilisation of O₂ by the cells for catabolic reactions and resultant release of CO₂ (cellular respiration).",
  ["Step 2 → diffusion across alveolar membrane", "Step 3 → transport of gases by the blood"],
  R_BRE("respiratory organs: steps of respiration"),
  why_others_wrong="Pulmonary ventilation comes first; diffusion between blood and tissues and the use of O₂ by "
                   "cells come after transport.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Intermediate", "numerical",
  "About 70 per cent of CO₂ is carried in the blood as bicarbonate, about 20–25 per cent as carbamino-haemoglobin and "
  "about 7 per cent dissolved in plasma. If the blood carries 200 mL of CO₂ from the tissues to the lungs in one "
  "minute, about how much of it is carried as bicarbonate and how much dissolved in plasma?",
  ["140 mL and 50 mL", "14 mL and 140 mL", "194 mL and 6 mL", "140 mL and 14 mL"], "D",
  "Transport of carbon dioxide",
  "Bicarbonate: 70 per cent of 200 mL = 140 mL. Dissolved: 7 per cent of 200 mL = 14 mL. (The remaining 20–25 per "
  "cent, about 40–50 mL, travels as carbamino-haemoglobin.)",
  ["Bicarbonate = 0.70 × 200 = 140 mL", "Dissolved = 0.07 × 200 = 14 mL"],
  R_BRE("transport of gases: transport of carbon dioxide"),
  shortcut="Bicarbonate share is ten times the dissolved share (70 : 7), so the two answers must differ by a factor of "
           "10.",
  why_others_wrong="A takes the carbamino share (25 per cent) as the dissolved part; B swaps the two; C uses the O₂ "
                   "split (97 : 3) instead of the CO₂ figures.",
  seconds=60, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Intermediate", "assertion_reason",
  ar("For the same difference in partial pressure, much more CO₂ than O₂ can diffuse through the diffusion membrane "
     "per unit time.",
     "The solubility of CO₂ is 20–25 times higher than that of O₂."),
  ASSERTION_REASON, "A",
  "Solubility and diffusion of gases",
  "NCERT: solubility of the gases and the thickness of the membranes, besides the pressure gradient, affect the rate "
  "of diffusion. As the solubility of CO₂ is 20–25 times higher than that of O₂, the amount of CO₂ that can diffuse "
  "through the diffusion membrane per unit difference in partial pressure is much higher compared to that of O₂. R "
  "is the cause NCERT gives for A.",
  ["A → true", "R → true", "Higher solubility → more diffusion per unit pressure difference → R explains A"],
  R_BRE("exchange of gases"),
  why_others_wrong="B ignores the causal link NCERT states; C and D call a true statement false.",
  seconds=30)

Z(BRE, "Exchange and transport of gases", "Intermediate", "statement_pair",
  sp("At the tissue site, where the partial pressure of CO₂ is high due to catabolism, CO₂ diffuses into the blood "
     "(RBCs and plasma) and forms HCO₃⁻ and H⁺.",
     "In the tissues, where pO₂ is low, pCO₂ is high, H⁺ concentration is high and temperature is higher, conditions "
     "favour the dissociation of oxygen from oxyhaemoglobin."),
  STATEMENT_PAIR, "A",
  "Gas transport at the tissue level",
  "NCERT: at the tissue site, where pCO₂ is high due to catabolism, CO₂ diffuses into blood (RBCs and plasma) and "
  "forms HCO₃⁻ and H⁺ (catalysed by carbonic anhydrase). In the tissues, low pO₂, high pCO₂, high H⁺ concentration "
  "and higher temperature favour dissociation of oxygen from oxyhaemoglobin; the reverse conditions in the alveoli "
  "favour its formation.",
  ["Statement I → true", "Statement II → true"],
  R_BRE("transport of gases"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=35)

Z(BRE, "Respiratory system", "Intermediate", "direct",
  "Which sequence correctly traces the path of inhaled air in humans?",
  ["External nostrils → nasal chamber → pharynx → larynx → trachea → primary bronchi → secondary and tertiary "
   "bronchi → bronchioles → terminal bronchioles → alveoli",
   "External nostrils → pharynx → nasal chamber → trachea → larynx → primary bronchi → bronchioles → tertiary "
   "bronchi → alveoli",
   "External nostrils → nasal chamber → larynx → pharynx → trachea → primary bronchi → terminal bronchioles → "
   "secondary bronchi → alveoli",
   "External nostrils → nasal chamber → pharynx → trachea → larynx → secondary bronchi → primary bronchi → "
   "bronchioles → alveoli"], "A",
  "Pathway of air",
  "NCERT: external nostrils lead through the nasal passage to the nasal chamber, which opens into the pharynx. The "
  "pharynx opens through the larynx into the trachea, which divides into the right and left primary bronchi. Each "
  "bronchus divides into secondary and tertiary bronchi and bronchioles, ending in very thin terminal bronchioles, "
  "each of which gives rise to alveoli.",
  ["Nasal chamber → pharynx → larynx → trachea", "Primary → secondary/tertiary bronchi → bronchioles → terminal "
   "bronchioles → alveoli"],
  R_BRE("respiratory organs: human respiratory system"),
  why_others_wrong="B puts the pharynx before the nasal chamber and the trachea before the larynx; C puts the larynx "
                   "before the pharynx; D puts the trachea before the larynx and secondary before primary bronchi.",
  seconds=40)

Z(BRE, "Respiratory volumes", "Intermediate", "match_list",
  ml(("respiratory volume", "definition"),
     ["Tidal volume", "Inspiratory reserve volume", "Expiratory reserve volume", "Residual volume"],
     ["Additional volume of air a person can expire by a forcible expiration",
      "Volume of air remaining in the lungs even after a forcible expiration",
      "Volume of air inspired or expired during a normal respiration",
      "Additional volume of air a person can inspire by a forcible inspiration"]),
  match_options(M("III", "IV", "I", "II"),
                [M("III", "I", "IV", "II"), M("IV", "III", "II", "I"), M("II", "IV", "I", "III")], at="B"),
  "B",
  "Respiratory volumes",
  "NCERT: tidal volume (TV) is the volume of air inspired or expired during a normal respiration; inspiratory reserve "
  "volume (IRV) is the additional volume a person can inspire by a forcible inspiration; expiratory reserve volume "
  "(ERV) is the additional volume a person can expire by a forcible expiration; residual volume (RV) is the volume "
  "remaining in the lungs even after a forcible expiration.",
  ["TV → III", "IRV → IV", "ERV → I", "RV → II"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="The other codes swap the two reserve volumes, or confuse the tidal and residual volumes.",
  seconds=40)

Z(BRE, "Respiratory volumes", "Advanced", "numerical",
  "A person's total lung capacity is 5800 mL, residual volume 1200 mL and inspiratory capacity 3500 mL. What is the "
  "expiratory reserve volume?",
  ["2300 mL", "4600 mL", "600 mL", "1100 mL"], "D",
  "Relations among volumes and capacities",
  "Total lung capacity = RV + ERV + TV + IRV, and inspiratory capacity = TV + IRV. Hence ERV = TLC − RV − IC = "
  "5800 − 1200 − 3500 = 1100 mL.",
  ["TLC = RV + ERV + (TV + IRV) = RV + ERV + IC", "ERV = 5800 − 1200 − 3500 = 1100 mL"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="TLC − IC gives the functional residual capacity (2300 mL); subtract RV to get ERV.",
  why_others_wrong="2300 mL is the functional residual capacity (RV not removed); 4600 mL is the vital capacity "
                   "(TLC − RV); 600 mL subtracts the tidal volume a second time though IC already contains it.",
  seconds=75, verified_by=RECOMPUTED)

_o = ["(a), (b), (d) and (e) only", "(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c) and (e) only"]
ms_check("abc", _o, "B")
Z(BRE, "Exchange and transport of gases", "Advanced", "multi_statement",
  ms("Which of the following statements about the transport of gases by haemoglobin are correct?",
     ["The binding of oxygen with haemoglobin is primarily related to the partial pressure of O₂.",
      "Each haemoglobin molecule can carry a maximum of four molecules of O₂.",
      "CO₂ is carried by haemoglobin as carbamino-haemoglobin.",
      "In the alveoli, where pCO₂ is low and pO₂ is high, more CO₂ binds to haemoglobin.",
      "Carbonic anhydrase is absent from RBCs."]),
  _o, "B",
  "Haemoglobin as a carrier of O₂ and CO₂",
  "NCERT: binding of O₂ with haemoglobin is primarily related to pO₂ (pCO₂, H⁺ and temperature can interfere); each "
  "haemoglobin molecule can carry a maximum of four molecules of O₂. CO₂ is carried by haemoglobin as "
  "carbamino-haemoglobin (about 20–25 per cent). When pCO₂ is low and pO₂ is high, as in the alveoli, CO₂ dissociates "
  "from carbamino-haemoglobin. RBCs contain a very high concentration of carbonic anhydrase.",
  ["(a) True", "(b) True", "(c) True", "(d) False: CO₂ dissociates in the alveoli",
   "(e) False: RBCs are rich in carbonic anhydrase"],
  R_BRE("transport of gases"),
  why_others_wrong="A, C and D include (d) or (e), both false.",
  seconds=55)

Z(BRE, "Regulation and disorders", "Advanced", "assertion_reason",
  ar("The chemosensitive area situated adjacent to the respiratory rhythm centre is highly sensitive to oxygen.",
     "An increase in CO₂ and hydrogen ions can activate this centre, which in turn signals the rhythm centre to make "
     "the adjustments in the respiratory process by which these substances can be eliminated."),
  ASSERTION_REASON, "D",
  "Chemical regulation of breathing",
  "NCERT: a chemosensitive area adjacent to the rhythm centre is highly sensitive to CO₂ and hydrogen ions. Increase "
  "in these substances activates this centre, which signals the rhythm centre to make adjustments so that they are "
  "eliminated. The role of oxygen in the regulation of respiratory rhythm is quite insignificant. So A is false, R "
  "is true.",
  ["Chemosensitive area → CO₂ and H⁺, not O₂ → A false", "R → true"],
  R_BRE("regulation of respiration"),
  why_others_wrong="A, B and C accept the false assertion.",
  seconds=35)

Z(BRE, "Respiratory volumes", "Advanced", "statement_pair",
  sp("The functional residual capacity exceeds the residual volume by an amount equal to the expiratory reserve "
     "volume.",
     "The inspiratory capacity of a person is greater than his vital capacity."),
  STATEMENT_PAIR, "C",
  "Comparing respiratory capacities",
  "FRC = ERV + RV, so FRC − RV = ERV (Statement I true). Inspiratory capacity = TV + IRV, while vital capacity = ERV "
  "+ TV + IRV; IC is smaller than VC by the ERV, so Statement II is false.",
  ["FRC − RV = ERV → true", "VC − IC = ERV > 0, so IC < VC → Statement II false"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=40)


# ================================================================ Body Fluids and Circulation (B5 I6 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "numerical",
  "A healthy adult has, on average, 12–16 g of haemoglobin in every 100 mL of blood. If a person has 14 g of "
  "haemoglobin per 100 mL and a total blood volume of 5 L, the total haemoglobin in his blood is about:",
  ["70 g", "700 g", "140 g", "7000 g"], "B",
  "Haemoglobin content of blood",
  "5 L = 5000 mL = 50 × 100 mL. Total haemoglobin = 14 g × 50 = 700 g.",
  ["5 L = 5000 mL", "5000 / 100 = 50 portions of 100 mL", "14 g × 50 = 700 g"],
  R_BFC("blood: formed elements (erythrocytes)"),
  why_others_wrong="70 g treats 14 g as the amount per litre; 140 g is the amount in one litre only; 7000 g treats "
                   "14 g as the amount in 10 mL.",
  seconds=40, verified_by=RECOMPUTED)

Z(BFC, "Circulatory disorders", "Basic", "direct",
  "Heart failure is not the same as cardiac arrest. Cardiac arrest refers to the condition in which:",
  ["Not enough oxygen reaches the heart muscle, causing acute chest pain",
   "The lumen of the coronary arteries is narrowed by deposits",
   "The heart stops beating",
   "Blood pressure stays at 140/90 mm Hg or higher"], "C",
  "Disorders of the circulatory system",
  "NCERT: heart failure means the state of the heart when it is not pumping blood effectively enough to meet the "
  "needs of the body. It is not the same as cardiac arrest (when the heart stops beating) or a heart attack (when the "
  "heart muscle is suddenly damaged by an inadequate blood supply).",
  ["Cardiac arrest → heart stops beating", "Heart failure → ineffective pumping", "Heart attack → sudden damage from "
   "inadequate blood supply"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="A describes angina, B coronary artery disease and D hypertension.",
  seconds=20)

Z(BFC, "Human heart", "Basic", "direct",
  "The human heart is protected by:",
  ["The rib cage alone, with no covering of its own",
   "A single-layered pleura enclosing pleural fluid",
   "A thick layer of adipose tissue called the myocardium",
   "A double-walled membranous bag, the pericardium, enclosing the pericardial fluid"], "D",
  "Human heart: protective covering",
  "NCERT: the heart, the mesodermally derived organ situated in the thoracic cavity, is protected by a double-walled "
  "membranous bag, the pericardium, enclosing the pericardial fluid.",
  ["Covering of the heart → double-walled pericardium with pericardial fluid"],
  R_BFC("circulatory pathways: human circulatory system"),
  why_others_wrong="The pleura covers the lungs; the heart is not covered by adipose tissue and does have its own "
                   "membranous covering.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Formed elements constitute nearly 55 per cent of the blood.",
     "Plasma contains minerals like Na⁺, Ca⁺⁺, Mg⁺⁺, HCO₃⁻ and Cl⁻, and also glucose, amino acids and lipids."),
  STATEMENT_PAIR, "D",
  "Composition of blood",
  "NCERT: plasma constitutes nearly 55 per cent of the blood; erythrocytes, leucocytes and platelets are collectively "
  "called formed elements and constitute nearly 45 per cent of the blood. Plasma contains small amounts of minerals "
  "like Na⁺, Ca⁺⁺, Mg⁺⁺, HCO₃⁻, Cl⁻ and so on, and glucose, amino acids and lipids are also present in it, as they are "
  "always in transit in the body.",
  ["Statement I: formed elements ≈ 45 per cent (plasma ≈ 55 per cent) → false", "Statement II → true"],
  R_BFC("blood: plasma and formed elements"),
  why_others_wrong="A and C accept the wrong percentage; B rejects the true Statement II.",
  seconds=25)

Z(BFC, "Blood and blood groups", "Basic", "match_list",
  ml(("ABO blood group", "antibodies in plasma"), ["A", "B", "AB", "O"],
     ["anti-A", "anti-B", "anti-A and anti-B", "nil"]),
  match_options(M("II", "I", "IV", "III"),
                [M("I", "II", "IV", "III"), M("II", "I", "III", "IV"), M("I", "II", "III", "IV")], at="B"),
  "B",
  "ABO grouping",
  "NCERT: ABO grouping is based on the presence or absence of two surface antigens, A and B, on the RBCs, and the "
  "plasma of different individuals contains two natural antibodies. As NCERT's table shows, group A has anti-B, "
  "group B has anti-A, group AB has neither (nil), and group O has both anti-A and anti-B.",
  ["A → anti-B (II)", "B → anti-A (I)", "AB → nil (IV)", "O → anti-A and anti-B (III)"],
  R_BFC("blood groups: ABO grouping"),
  why_others_wrong="The other codes give a group the antibody against its own antigen, or swap AB with O.",
  seconds=30)

Z(BFC, "Blood and blood groups", "Intermediate", "numerical",
  "A healthy adult man has about 5 million RBCs per mm³ of blood. Taking 1 L = 1000 cm³ and 1 cm³ = 1000 mm³, the "
  "number of RBCs in one litre of his blood is about:",
  ["5 × 10⁶", "5 × 10⁹", "5 × 10¹⁵", "5 × 10¹²"], "D",
  "RBC count",
  "NCERT: a healthy adult man has, on average, 5 million to 5.5 million RBCs per mm³ of blood. 1 L = 1000 cm³ = "
  "1000 × 1000 mm³ = 10⁶ mm³. Number of RBCs = 5 × 10⁶ per mm³ × 10⁶ mm³ = 5 × 10¹² per litre.",
  ["5 million = 5 × 10⁶ per mm³", "1 L = 10⁶ mm³", "5 × 10⁶ × 10⁶ = 5 × 10¹²"],
  R_BFC("blood: formed elements (erythrocytes)"),
  why_others_wrong="5 × 10⁶ is the count per mm³; 5 × 10⁹ is the count per mL (one factor of 1000 missed); "
                   "5 × 10¹⁵ applies one factor of 1000 too many.",
  seconds=60, verified_by=RECOMPUTED)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "direct",
  "The sino-atrial node (SAN) acts as the pacemaker of the human heart because it:",
  ["Receives the maximum number of nerve fibres from the medulla oblongata",
   "Can generate the maximum number of action potentials, i.e. 70–75 per minute",
   "Is the largest mass of nodal tissue, lying in the inter-ventricular septum",
   "Is the only part of the heart made of cardiac muscle"], "B",
  "Nodal tissue and the pacemaker",
  "NCERT: the nodal musculature has the ability to generate action potentials without any external stimuli, i.e. it "
  "is autoexcitable. The number of action potentials that could be generated in a minute varies at different parts "
  "of the nodal system; the SAN can generate the maximum number, i.e. 70–75 min⁻¹, and is responsible for initiating "
  "and maintaining the rhythmic contractile activity of the heart. Therefore it is called the pacemaker.",
  ["Nodal tissue is autoexcitable", "SAN → maximum rate (70–75 per min) → pacemaker"],
  R_BFC("circulatory pathways: human circulatory system"),
  why_others_wrong="The heart is auto-regulated, not driven by the medulla; the SAN lies in the right upper corner of "
                   "the right atrium; the entire heart is made of cardiac muscle.",
  seconds=30)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "assertion_reason",
  ar("The cardiac output of an athlete can be much higher than that of an ordinary man.",
     "The body has the ability to alter the stroke volume as well as the rate of heartbeat, and thereby the cardiac "
     "output."),
  ASSERTION_REASON, "A",
  "Cardiac output",
  "Cardiac output = stroke volume × heart rate (about 5000 mL per minute in a healthy person). NCERT: the body has the "
  "ability to alter the stroke volume as well as the heart rate and thereby the cardiac output; for example, the "
  "cardiac output of an athlete will be much higher than that of an ordinary man. R is the reason A is possible.",
  ["Cardiac output = SV × heart rate", "Both can be raised → higher output in athletes → R explains A"],
  R_BFC("cardiac cycle"),
  why_others_wrong="B ignores that A is NCERT's own example of R; C and D call a true statement false.",
  seconds=30)

_o = ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (b) and (d) only", "(a), (d) and (e) only"]
ms_check("abd", _o, "C")
Z(BFC, "Coagulation and lymph", "Intermediate", "multi_statement",
  ms("Which of the following statements about tissue fluid and lymph are correct?",
     ["The lymphatic system collects the interstitial fluid and drains it back to the major veins.",
      "Lymph is an important carrier of nutrients, hormones, etc.",
      "Lymph is a red fluid rich in haemoglobin-containing RBCs.",
      "Exchange of nutrients, gases, etc. between the blood and the cells always occurs through the interstitial "
      "fluid.",
      "The lymphatic system drains the interstitial fluid into the pulmonary arteries."]),
  _o, "C",
  "Lymph (tissue fluid)",
  "NCERT: an elaborate network of vessels, the lymphatic system, collects the interstitial fluid and drains it back "
  "to the major veins. The fluid in the lymphatic system is lymph, a colourless fluid with specialised lymphocytes. "
  "Exchange of nutrients, gases, etc. between the blood and the cells always occurs through this fluid. Lymph is "
  "also an important carrier for nutrients, hormones, etc.",
  ["(a) True", "(b) True", "(c) False: lymph is colourless", "(d) True",
   "(e) False: it drains into the major veins"],
  R_BFC("lymph (tissue fluid)"),
  why_others_wrong="A includes (c); B and D include (e); B also leaves out true statements.",
  seconds=50)

Z(BFC, "Human heart", "Intermediate", "match_list",
  ml(("structure", "feature"), ["Tricuspid valve", "Bicuspid (mitral) valve", "Semilunar valves",
                                "Inter-ventricular septum"],
     ["Thick-walled partition separating the left and right ventricles",
      "Guard the openings of the ventricles into the pulmonary artery and the aorta",
      "Guards the opening between the left atrium and the left ventricle",
      "Formed of three muscular flaps or cusps between the right atrium and the right ventricle"]),
  match_options(M("IV", "III", "II", "I"),
                [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"), M("II", "III", "IV", "I")], at="B"),
  "B",
  "Valves and septa of the heart",
  "NCERT: the opening between the right atrium and the right ventricle is guarded by the tricuspid valve, formed of "
  "three muscular flaps or cusps; the bicuspid or mitral valve guards the opening between the left atrium and the "
  "left ventricle. The openings of the right and left ventricles into the pulmonary artery and the aorta are "
  "provided with semilunar valves. A thick-walled inter-ventricular septum separates the left and right ventricles.",
  ["Tricuspid → IV", "Bicuspid (mitral) → III", "Semilunar → II", "Inter-ventricular septum → I"],
  R_BFC("circulatory pathways: human circulatory system"),
  why_others_wrong="The other codes swap the two atrio-ventricular valves, or the semilunar valves with the septum.",
  seconds=40)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "statement_pair",
  sp("During joint diastole, the semilunar valves are closed.",
     "As the ventricular pressure declines after ventricular systole, the tricuspid and bicuspid valves are pushed "
     "open by the pressure in the atria exerted by the blood emptied into them by the veins."),
  STATEMENT_PAIR, "A",
  "Valves during the cardiac cycle",
  "NCERT: in joint diastole the tricuspid and bicuspid valves are open and blood flows from the atria into the "
  "ventricles; the semilunar valves are closed at this stage. After ventricular systole the ventricles relax, the "
  "semilunar valves close, and as the ventricular pressure declines further the tricuspid and bicuspid valves are "
  "pushed open by the pressure in the atria, starting a new cycle.",
  ["Statement I → true", "Statement II → true"],
  R_BFC("cardiac cycle"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=35)

Z(BFC, "Blood and blood groups", "Advanced", "numerical",
  "A ward has 12 patients of blood group A, 9 of group B, 4 of group AB and 15 of group O. Considering only the ABO "
  "system, how many of these patients can safely receive blood from a group A donor?",
  ["12", "27", "31", "16"], "D",
  "Donor compatibility in the ABO system",
  "Group A blood carries antigen A on its RBCs. It can be given only to persons whose plasma lacks anti-A, i.e. "
  "groups A (anti-B only) and AB (no antibodies). Recipients = 12 + 4 = 16. Group B and group O persons have anti-A "
  "and cannot receive it.",
  ["Donor A → antigen A", "Recipients without anti-A → A and AB", "12 + 4 = 16"],
  R_BFC("blood groups: ABO grouping (donor compatibility)"),
  shortcut="A donor can give to any recipient whose group contains the letter A: A and AB.",
  why_others_wrong="27 adds group O, confusing the donors for an A recipient (A and O) with the recipients of an A "
                   "donor; 12 forgets group AB; 31 adds group O as well.",
  seconds=60, verified_by=RECOMPUTED)

_o = ["(a), (b) and (c) only", "(a) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only"]
ms_check("ac", _o, "B")
Z(BFC, "Double circulation and regulation", "Advanced", "multi_statement",
  ms("Which of the following statements about circulatory pathways are correct?",
     ["The systemic circulation provides nutrients, O₂ and other essential substances to the tissues and takes CO₂ "
      "and other harmful substances away for elimination.",
      "In the pulmonary circulation, oxygenated blood entering the pulmonary artery is carried to the lungs.",
      "Birds and mammals have two separate circulatory pathways, so oxygenated and deoxygenated blood are pumped out "
      "without mixing.",
      "In amphibians, the left atrium receives deoxygenated blood from the body parts."]),
  _o, "B",
  "Double circulation",
  "NCERT: deoxygenated blood pumped into the pulmonary artery is carried to the lungs, and oxygenated blood returns "
  "by the pulmonary veins (pulmonary circulation). Oxygenated blood entering the aorta is carried to the tissues "
  "(systemic circulation), which provides nutrients, O₂ and other essential substances and takes away CO₂ and other "
  "harmful substances. In birds and mammals the ventricles pump out blood without mixing, i.e. there are two separate "
  "pathways. In amphibians the left atrium receives oxygenated blood from the gills/lungs/skin and the right atrium "
  "gets deoxygenated blood from other body parts.",
  ["(a) True", "(b) False: the pulmonary artery carries deoxygenated blood", "(c) True",
   "(d) False: the left atrium receives oxygenated blood"],
  R_BFC("circulatory pathways; double circulation"),
  why_others_wrong="A includes (b); C includes (b) and (d); D includes (d).",
  seconds=50)

Z(BFC, "Blood and blood groups", "Advanced", "assertion_reason",
  ar("Leucocytes are known as white blood cells.",
     "Leucocytes are colourless due to the lack of haemoglobin."),
  ASSERTION_REASON, "A",
  "Leucocytes",
  "NCERT: leucocytes are also known as white blood cells (WBC) as they are colourless due to the lack of haemoglobin. "
  "They are nucleated and relatively fewer in number (6000–8000 per mm³ of blood). R gives the reason for the name "
  "in A.",
  ["A → true", "R → true", "Colourless (no haemoglobin) → called 'white' → R explains A"],
  R_BFC("blood: formed elements (leucocytes)"),
  why_others_wrong="B misses the causal link NCERT states with 'as'; C and D call a true statement false.",
  seconds=25)

Z(BFC, "Human heart", "Advanced", "statement_pair",
  sp("The entire human heart is made of cardiac muscles.",
     "The nodal tissue of the human heart is distributed only in the ventricles."),
  STATEMENT_PAIR, "C",
  "Cardiac musculature and nodal tissue",
  "NCERT: the entire heart is made of cardiac muscles. A specialised cardiac musculature called the nodal tissue is "
  "also distributed in the heart: the SAN in the right upper corner of the right atrium, the AVN in the lower left "
  "corner of the right atrium, and the AV bundle and Purkinje fibres in the ventricles. Nodal tissue is therefore not "
  "confined to the ventricles.",
  ["Statement I → true", "Statement II: SAN and AVN lie in the right atrium → false"],
  R_BFC("circulatory pathways: human circulatory system"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=35)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "direct",
  "At the start of ventricular systole, the ventricular pressure has risen above the atrial pressure but is still "
  "below the pressure in the pulmonary artery and the aorta. At this instant:",
  ["The tricuspid and bicuspid valves are closed, and the semilunar valves are also closed",
   "The tricuspid and bicuspid valves are open, and the semilunar valves are closed",
   "The tricuspid and bicuspid valves are closed, and the semilunar valves are open",
   "All four valves are open"], "A",
  "Valve positions in the cardiac cycle",
  "NCERT: as the ventricles contract, the ventricular pressure rises and the tricuspid and bicuspid valves close "
  "because of the attempted backflow into the atria. Only when the ventricular pressure increases further (above "
  "that in the arteries) are the semilunar valves forced open. In between, therefore, all four valves are closed.",
  ["Ventricular pressure > atrial pressure → AV valves close", "Ventricular pressure < arterial pressure → semilunar "
   "valves still closed", "All four valves closed"],
  R_BFC("cardiac cycle"),
  why_others_wrong="B describes joint diastole; C describes the later phase of ejection; all four valves are never "
                   "open together.",
  seconds=45)


# ================================================================ Excretory Products and their Elimination (B4 I6 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Ammonia is the most toxic form of nitrogenous waste. Its elimination requires:",
  ["Conversion into uric acid crystals in the liver", "Very little water, as a pellet or paste",
   "Active secretion by the urinary bladder", "Large amounts of water"], "D",
  "Ammonotelism",
  "NCERT: ammonia, urea and uric acid are the major forms of nitrogenous wastes. Ammonia is the most toxic form and "
  "requires a large amount of water for its elimination, whereas uric acid, being the least toxic, can be removed "
  "with a minimum loss of water.",
  ["Ammonia → most toxic → large amount of water needed"],
  R_EXC("introduction: forms of nitrogenous wastes"),
  why_others_wrong="Pellets or paste with little water describe uric acid excretion; ammonia is not converted into "
                   "uric acid for its own elimination, and the bladder only stores urine.",
  seconds=20)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Protonephridia or flame cells are primarily concerned with:",
  ["Ionic and fluid volume regulation, i.e. osmoregulation", "Digestion of food",
   "Production of uric acid", "Exchange of respiratory gases"], "A",
  "Excretory structures of animals",
  "NCERT: protonephridia or flame cells are the excretory structures in Platyhelminthes (e.g. Planaria), rotifers, "
  "some annelids and the cephalochordate Amphioxus. Protonephridia are primarily concerned with ionic and fluid "
  "volume regulation, i.e. osmoregulation.",
  ["Protonephridia → osmoregulation (ionic and fluid volume regulation)"],
  R_EXC("introduction: excretory structures"),
  why_others_wrong="Protonephridia have no role in digestion, uric acid synthesis or gas exchange.",
  seconds=20)

Z(EXC, "Urine formation", "Basic", "direct",
  "On average, a healthy adult human excretes how much urine per day?",
  ["0.1 to 0.15 L", "1 to 1.5 L", "10 to 15 L", "180 L"], "B",
  "Volume of urine",
  "NCERT: on an average, 1 to 1.5 litres of urine is excreted out per day by an adult human. About 180 litres of "
  "glomerular filtrate is formed per day, nearly 99 per cent of which is reabsorbed.",
  ["Urine → 1 to 1.5 L per day", "Filtrate → about 180 L per day"],
  R_EXC("micturition"),
  why_others_wrong="180 L is the daily glomerular filtrate; 0.1–0.15 L and 10–15 L are off by a factor of ten.",
  seconds=20)

Z(EXC, "Modes of excretion", "Basic", "statement_pair",
  sp("Protonephridia are excretory structures in rotifers and some annelids as well, besides flatworms.",
     "Nephridia are the excretory structures of most insects, including cockroaches."),
  STATEMENT_PAIR, "C",
  "Excretory structures in invertebrates",
  "NCERT: protonephridia (flame cells) are found in Platyhelminthes, rotifers, some annelids and the cephalochordate "
  "Amphioxus. Nephridia are the tubular excretory structures of earthworms and other annelids; most insects, "
  "including cockroaches, have Malpighian tubules. So Statement II is false.",
  ["Statement I → true", "Statement II: insects have Malpighian tubules; nephridia belong to annelids → false"],
  R_EXC("introduction: excretory structures"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=25)

Z(EXC, "Urine formation", "Advanced", "numerical",
  "A person's glomerular filtration rate is 125 mL per minute. If the proximal convoluted tubule reabsorbs 75 per "
  "cent of the filtrate volume (NCERT gives 70–80 per cent of electrolytes and water), what volume of filtrate leaves "
  "the PCT in one day?",
  ["135 L", "1.8 L", "7.5 L", "45 L"], "D",
  "GFR and reabsorption in the PCT",
  "Filtrate per day = 125 mL/min × 60 × 24 = 1,80,000 mL = 180 L. If 75 per cent is reabsorbed in the PCT, the "
  "remaining 25 per cent passes on: 0.25 × 180 = 45 L per day.",
  ["Filtrate/day = 125 × 1440 = 180000 mL = 180 L", "Leaves PCT = 25 per cent of 180 L = 45 L"],
  R_EXC("human excretory system; function of the tubules"),
  shortcut="180 L × 1/4 = 45 L.",
  why_others_wrong="135 L is the volume reabsorbed, not the volume left; 1.8 L is the daily urine at 99 per cent "
                   "total reabsorption; 7.5 L is the filtrate formed in one hour, not what leaves the PCT in a day.",
  seconds=75, verified_by=RECOMPUTED)

Z(EXC, "Urine formation", "Intermediate", "direct",
  "As the filtrate moves down the descending limb of Henle's loop, it:",
  ["Gets diluted, because electrolytes are added to it from the medullary fluid",
   "Gets concentrated, because the limb is permeable to water but almost impermeable to electrolytes",
   "Remains unchanged, because no transport occurs in this limb",
   "Loses all its urea to the vasa recta by active transport"], "B",
  "Henle's loop: descending limb",
  "NCERT: the descending limb of the loop of Henle is permeable to water but almost impermeable to electrolytes. "
  "This concentrates the filtrate as it moves down.",
  ["Water leaves, electrolytes stay → filtrate concentrated going down"],
  R_EXC("function of the tubules"),
  why_others_wrong="Dilution occurs in the ascending limb; water does move in the descending limb; urea movement is "
                   "linked to the collecting tubule and the thin ascending limb, not removal of all urea here.",
  seconds=30)

Z(EXC, "Urine formation", "Intermediate", "assertion_reason",
  ar("As the concentrated filtrate passes upward through the ascending limb of Henle's loop, it gets diluted.",
     "The ascending limb is impermeable to water but allows transport of electrolytes, actively or passively, to "
     "the medullary fluid."),
  ASSERTION_REASON, "A",
  "Henle's loop: ascending limb",
  "NCERT: the ascending limb is impermeable to water but allows transport of electrolytes actively or passively. "
  "Therefore, as the concentrated filtrate passes upward, it gets diluted due to the passage of electrolytes to the "
  "medullary fluid. Solutes leave while water cannot follow, which is exactly why the filtrate is diluted.",
  ["A → true", "R → true", "Electrolytes out, water retained → dilution → R explains A"],
  R_EXC("function of the tubules"),
  why_others_wrong="B misses the cause NCERT gives with 'therefore'; C and D call a true statement false.",
  seconds=30)

Z(EXC, "Nephron structure", "Intermediate", "match_list",
  ml(("structure", "description"), ["Capsule of the kidney", "Medullary pyramids", "Henle's loop",
                                    "Proximal convoluted tubule"],
     ["Highly coiled network of the tubule that follows Bowman's capsule",
      "Hairpin-shaped part of the tubule with a descending and an ascending limb",
      "Tough outer layer covering the kidney",
      "Few conical masses of the medulla projecting into the calyces"]),
  match_options(M("III", "IV", "II", "I"),
                [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"), M("I", "IV", "II", "III")], at="D"),
  "D",
  "Structure of the kidney and nephron",
  "NCERT: outside the kidney is a tough capsule. Inside are an outer cortex and an inner medulla; the medulla is "
  "divided into a few conical masses, the medullary pyramids, projecting into the calyces. The tubule continues from "
  "Bowman's capsule as a highly coiled network, the PCT; a hairpin-shaped Henle's loop, with a descending and an "
  "ascending limb, comes next.",
  ["Capsule → III", "Medullary pyramids → IV", "Henle's loop → II", "PCT → I"],
  R_EXC("human excretory system"),
  why_others_wrong="The other codes swap the capsule with the pyramids, the loop with the PCT, or the capsule with "
                   "the PCT.",
  seconds=40)

_o = ["(a), (b) and (c) only", "(a) and (c) only", "(c), (d) and (e) only", "(a), (c) and (d) only"]
ms_check("ac", _o, "B")
Z(EXC, "Regulation of kidney function", "Intermediate", "multi_statement",
  ms("Which of the following statements about the regulation of kidney function are correct?",
     ["Kidney function is monitored and regulated by hormonal feedback mechanisms involving the hypothalamus, the "
      "JGA and, to a certain extent, the heart.",
      "ADH is released into the blood from the adenohypophysis.",
      "Angiotensin II increases the glomerular blood pressure and thereby the GFR.",
      "Renin is released by the cells of the proximal convoluted tubule.",
      "Aldosterone is released by the adrenal medulla."]),
  _o, "B",
  "Hormonal regulation of the kidney",
  "NCERT: the functioning of the kidneys is efficiently monitored and regulated by hormonal feedback mechanisms "
  "involving the hypothalamus, JGA and to a certain extent the heart. ADH is released from the neurohypophysis. "
  "Renin is released by the JG cells. Angiotensin II, a powerful vasoconstrictor, increases the glomerular blood "
  "pressure and thereby GFR, and also activates the adrenal cortex to release aldosterone.",
  ["(a) True", "(b) False: neurohypophysis", "(c) True", "(d) False: JG cells release renin",
   "(e) False: adrenal cortex"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A includes (b); C includes (d) and (e); D includes (d).",
  seconds=50)

Z(EXC, "Urine formation", "Intermediate", "statement_pair",
  sp("Reabsorption in Henle's loop is minimum, but this segment plays a significant role in the maintenance of a "
     "high osmolarity of the medullary interstitial fluid.",
     "Analysis of urine helps in the clinical diagnosis of many metabolic disorders as well as malfunctioning of "
     "the kidney."),
  STATEMENT_PAIR, "A",
  "Henle's loop and urine analysis",
  "NCERT: reabsorption in Henle's loop is minimum; however, this region plays a significant role in the maintenance "
  "of high osmolarity of the medullary interstitial fluid. Analysis of urine helps in the clinical diagnosis of many "
  "metabolic disorders as well as malfunctioning of the kidney (e.g. glycosuria and ketonuria in diabetes "
  "mellitus).",
  ["Statement I → true", "Statement II → true"],
  R_EXC("function of the tubules; micturition"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=30)

Z(EXC, "Modes of excretion", "Advanced", "assertion_reason",
  ar("Small amounts of nitrogenous wastes can be eliminated through saliva.",
     "The primary function of sweat is to produce a cooling effect on the body surface."),
  ASSERTION_REASON, "B",
  "Role of other organs in excretion",
  "NCERT: small amounts of nitrogenous wastes could be eliminated through saliva too. Separately, though the primary "
  "function of sweat is to facilitate a cooling effect on the body surface, it also helps to remove some wastes. Both "
  "are true, but the cooling function of sweat has nothing to do with excretion through saliva.",
  ["A → true", "R → true", "R concerns sweat, not saliva → not the explanation"],
  R_EXC("role of other organs in excretion"),
  why_others_wrong="A links two unrelated facts; C and D call a true statement false.",
  seconds=30)

Z(EXC, "Modes of excretion", "Advanced", "assertion_reason",
  ar("Terrestrial animals excrete less toxic nitrogenous wastes such as urea and uric acid.",
     "Terrestrial adaptation necessitated the production of less toxic nitrogenous wastes for the conservation of "
     "water."),
  ASSERTION_REASON, "A",
  "Excretion and life on land",
  "NCERT: terrestrial adaptation necessitated the production of lesser toxic nitrogenous wastes like urea and uric "
  "acid for conservation of water. Ammonia needs a large amount of water for its elimination, which land animals "
  "cannot spare; R gives the reason for A.",
  ["A → true", "R → true", "Need to conserve water on land → less toxic wastes → R explains A"],
  R_EXC("introduction: forms of nitrogenous wastes"),
  why_others_wrong="B ignores the reason NCERT states; C and D call a true statement false.",
  seconds=30)

_o = ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (d) only", "(a), (c) and (e) only"]
ms_check("abd", _o, "C")
Z(EXC, "Nephron structure", "Advanced", "multi_statement",
  ms("Which of the following statements about the nephron and its blood supply are correct?",
     ["Each nephron has two parts: the glomerulus and the renal tubule.",
      "The efferent arteriole emerging from the glomerulus forms a fine capillary network around the renal tubule, "
      "the peritubular capillaries.",
      "The distal convoluted tubules of many nephrons open directly into the ureter.",
      "Many collecting ducts converge and open into the renal pelvis through the medullary pyramids in the calyces.",
      "The afferent arteriole carries blood away from the glomerulus."]),
  _o, "C",
  "Nephron and its blood vessels",
  "NCERT: each nephron has two parts, the glomerulus and the renal tubule. The glomerulus is a tuft of capillaries "
  "formed by the afferent arteriole; blood is carried away by the efferent arteriole, which forms the peritubular "
  "capillaries. The DCTs of many nephrons open into a straight collecting duct; many collecting ducts converge and "
  "open into the renal pelvis through the medullary pyramids in the calyces.",
  ["(a) True", "(b) True", "(c) False: DCTs open into collecting ducts", "(d) True",
   "(e) False: the efferent arteriole carries blood away"],
  R_EXC("human excretory system"),
  why_others_wrong="A includes (c); B and D include (e).",
  seconds=55)

Z(EXC, "Regulation of kidney function", "Intermediate", "direct",
  "Which of the following acts as a check on the renin-angiotensin mechanism?",
  ["Aldosterone", "Angiotensin II", "Antidiuretic hormone", "Atrial natriuretic factor (ANF)"], "D",
  "Atrial natriuretic factor",
  "NCERT: an increase in blood flow to the atria of the heart can cause the release of atrial natriuretic factor "
  "(ANF). ANF causes vasodilation and thereby decreases blood pressure. The ANF mechanism therefore acts as a check on "
  "the renin-angiotensin mechanism, which raises blood pressure and GFR.",
  ["Renin-angiotensin → vasoconstriction, higher BP", "ANF → vasodilation, lower BP → check on it"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="Aldosterone and angiotensin II are products of the renin-angiotensin mechanism; ADH also raises "
                   "blood pressure by constriction and does not oppose it.",
  seconds=30)


# ================================================================ Locomotion and Movement (B4 I6 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Types of movement", "Basic", "direct",
  "Hydra uses its tentacles for:",
  ["Respiration only", "Excretion and osmoregulation", "Producing water currents through its canal system",
   "Capturing its prey and also for locomotion"], "D",
  "Movement and locomotion",
  "NCERT: locomotion and movement cannot always be studied separately; the same structure may serve both. Hydra can "
  "use its tentacles for capturing its prey and also use them for locomotion.",
  ["Tentacles of Hydra → capture of prey + locomotion"],
  R_LOC("introduction"),
  why_others_wrong="Tentacles are not respiratory or excretory organs; a canal system with water currents belongs "
                   "to sponges.",
  seconds=20)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "According to NCERT, muscles have special properties such as:",
  ["Phagocytosis, secretion, absorption and excretion",
   "Excitability, contractility, extensibility and elasticity",
   "Conduction of nerve impulses, synaptic transmission and secretion of hormones",
   "Calcification, ossification, mineral storage and blood formation"], "B",
  "Properties of muscle",
  "NCERT: muscle is a specialised tissue of mesodermal origin. Muscles have special properties like excitability, "
  "contractility, extensibility and elasticity.",
  ["Muscle properties → excitability, contractility, extensibility, elasticity"],
  R_LOC("muscle"),
  why_others_wrong="Phagocytosis and secretion are features of other cells; impulse conduction and synaptic "
                   "transmission are neural functions; ossification and blood formation relate to bone.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "direct",
  "The three tiny bones, or ear ossicles, present in each middle ear are:",
  ["Hyoid, atlas and axis", "Carpals, tarsals and phalanges", "Malleus, incus and stapes",
   "Clavicle, scapula and acromion"], "C",
  "Ear ossicles",
  "NCERT: the skull includes, in addition, a single U-shaped hyoid bone at the base of the buccal cavity, and each "
  "middle ear contains three tiny bones - malleus, incus and stapes - collectively called ear ossicles.",
  ["Ear ossicles → malleus, incus, stapes (in each middle ear)"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="Hyoid, atlas and axis are other axial bones; carpals, tarsals and phalanges are limb bones; the "
                   "clavicle and scapula form the pectoral girdle and the acromion is part of the scapula.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "match_list",
  ml(("region of the vertebral column", "number of vertebrae"), ["Cervical", "Thoracic", "Lumbar", "Sacral"],
     ["1 (fused)", "5", "7", "12"]),
  match_options(M("III", "IV", "II", "I"),
                [M("IV", "III", "II", "I"), M("III", "II", "IV", "I"), M("III", "IV", "I", "II")], at="D"),
  "D",
  "Regions of the vertebral column",
  "NCERT: the vertebral column is formed by 26 serially arranged vertebrae and, starting from the skull, has cervical "
  "(7), thoracic (12), lumbar (5), sacral (1, fused) and coccygeal (1, fused) regions.",
  ["Cervical → 7 (III)", "Thoracic → 12 (IV)", "Lumbar → 5 (II)", "Sacral → 1 fused (I)"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="The other codes swap the cervical and thoracic counts, the thoracic and lumbar counts, or the "
                   "lumbar and sacral counts.",
  seconds=30)

Z(LOC, "Muscle contraction", "Intermediate", "direct",
  "The striated appearance of a skeletal muscle fibre, with alternate dark and light bands on its myofibrils, is due "
  "to:",
  ["The distribution pattern of two important proteins, actin and myosin",
   "Alternate layers of fat and protein in the sarcolemma",
   "The regular arrangement of nuclei along the fibre",
   "Bands of calcium phosphate deposited in the sarcoplasm"], "A",
  "Striations of skeletal muscle",
  "NCERT: the striated appearance of the myofibril is due to the distribution pattern of two important proteins - "
  "actin and myosin. The light bands contain actin (I-band, isotropic) and the dark bands contain myosin (A-band, "
  "anisotropic).",
  ["Striations → pattern of actin (light band) and myosin (dark band)"],
  R_LOC("structure of contractile proteins / skeletal muscle"),
  why_others_wrong="The sarcolemma is a plasma membrane, nuclei are not arranged in bands, and calcium is stored as "
                   "ions in the sarcoplasmic reticulum, not as banded deposits.",
  seconds=25)

Z(LOC, "Skeletal system", "Intermediate", "assertion_reason",
  ar("The vertebral column protects the spinal cord.",
     "Each vertebra has a central hollow portion, the neural canal, through which the spinal cord passes."),
  ASSERTION_REASON, "A",
  "Vertebra and spinal cord",
  "NCERT: each vertebra has a central hollow portion (neural canal) through which the spinal cord passes, and the "
  "vertebral column protects the spinal cord. The spinal cord lying inside the bony neural canals is what makes the "
  "column protective, so R explains A.",
  ["A → true", "R → true", "Spinal cord enclosed in neural canals → protection → R explains A"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="B misses the direct link; C and D call a true statement false.",
  seconds=30)

Z(LOC, "Muscle contraction", "Intermediate", "statement_pair",
  sp("Troponin is distributed at regular intervals on the tropomyosin of the thin filament.",
     "The globular head of the heavy meromyosin is an active ATPase enzyme and has binding sites for ATP and active "
     "sites for actin."),
  STATEMENT_PAIR, "A",
  "Contractile proteins",
  "NCERT: each actin filament has two F-actins helically wound to each other, with two filaments of tropomyosin "
  "running close to the F-actins; troponin is distributed at regular intervals on the tropomyosin. Each meromyosin "
  "has a globular head with a short arm (heavy meromyosin, HMM) and a tail (light meromyosin, LMM); the globular head "
  "is an active ATPase enzyme with binding sites for ATP and active sites for actin.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=30)

_o = ["(a), (b), (c) and (d) only", "(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
ms_check("acd", _o, "B")
Z(LOC, "Skeletal system", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human skeleton are correct?",
     ["The first vertebra, the atlas, articulates with the occipital condyles.",
      "The humerus is the bone of the thigh.",
      "The 11th and 12th pairs of ribs are not connected ventrally and are called floating ribs.",
      "Each upper limb has a humerus, a radius and an ulna.",
      "The hyoid is one of the eight bones of the cranium."]),
  _o, "B",
  "Axial and appendicular skeleton",
  "NCERT: the first vertebra is the atlas and it articulates with the occipital condyles. The last two pairs of ribs "
  "(11th and 12th) are not connected ventrally and are therefore called floating ribs. The bones of each limb include "
  "the humerus, radius and ulna (forelimb); the femur is the thigh bone. The hyoid is a single U-shaped bone at the "
  "base of the buccal cavity, included in the skull but not one of the 8 cranial bones.",
  ["(a) True", "(b) False: the femur is the thigh bone", "(c) True", "(d) True",
   "(e) False: the hyoid is not a cranial bone"],
  R_LOC("skeletal system"),
  why_others_wrong="A includes (b); C includes (b) and (e); D includes (e).",
  seconds=50)

Z(LOC, "Joints", "Intermediate", "statement_pair",
  sp("Joints are points of contact between bones, or between bones and cartilages.",
     "Cartilaginous joints, such as those between the adjacent vertebrae, do not permit any movement."),
  STATEMENT_PAIR, "C",
  "Types of joints",
  "NCERT: joints are points of contact between bones, or between bones and cartilages. In cartilaginous joints, the "
  "bones involved are joined together with the help of cartilages; the joint between the adjacent vertebrae is of "
  "this pattern and it permits limited movements. Fibrous joints are the ones that do not allow any movement.",
  ["Statement I → true", "Statement II: cartilaginous joints permit limited movement → false"],
  R_LOC("joints"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=30)

Z(LOC, "Skeletal system", "Intermediate", "direct",
  "The scapula is a large, triangular, flat bone situated in the dorsal part of the thorax between the:",
  ["Fourth and the tenth ribs", "First and the fifth ribs", "Seventh and the twelfth ribs",
   "Second and the seventh ribs"], "D",
  "Pectoral girdle",
  "NCERT: each half of the pectoral girdle consists of a clavicle and a scapula. The scapula is a large triangular "
  "flat bone situated in the dorsal part of the thorax between the second and the seventh ribs.",
  ["Scapula → dorsal thorax, between ribs 2 and 7"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="The other rib ranges do not match the NCERT description.",
  seconds=25)

Z(LOC, "Types of movement", "Advanced", "assertion_reason",
  ar("Animals generally show locomotion in search of food, shelter, a mate, suitable breeding grounds or favourable "
     "climatic conditions, or to escape from enemies or predators.",
     "Methods of locomotion performed by animals vary with their habitats and the demand of the situation."),
  ASSERTION_REASON, "B",
  "Purpose and methods of locomotion",
  "NCERT: methods of locomotion performed by animals vary with their habitats and the demand of the situation. "
  "However, locomotion is generally for search of food, shelter, mate, suitable breeding grounds, favourable climatic "
  "conditions or to escape from enemies/predators. R explains how locomotion varies, not why animals move about, so "
  "it is not the explanation of A.",
  ["A (purposes of locomotion) → true", "R (methods vary with habitat) → true",
   "R explains the variety of methods, not the purpose → not the explanation"],
  R_LOC("introduction"),
  why_others_wrong="A treats the variety of methods as the reason for locomotion; C and D call a true statement "
                   "false.",
  seconds=35)

_o = ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (b), (d) and (e) only"]
ms_check("abc", _o, "C")
Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("Which of the following statements about the three types of muscles are correct?",
     ["Visceral muscles are located in the inner walls of hollow visceral organs such as the alimentary canal and "
      "the reproductive tract.",
      "Visceral muscles are non-striated and involuntary.",
      "Cardiac muscle fibres are striated and involuntary.",
      "Skeletal muscle fibres are non-striated.",
      "Muscles contribute about 70–80 per cent of the body weight of a human adult."]),
  _o, "C",
  "Skeletal, visceral and cardiac muscles",
  "NCERT: skeletal muscles are closely associated with skeletal components and are striated and voluntary. Visceral "
  "muscles lie in the inner walls of hollow visceral organs such as the alimentary canal and reproductive tract; they "
  "are smooth (non-striated) and involuntary. Cardiac muscles are striated and involuntary. Muscles contribute about "
  "40–50 per cent of the body weight of a human adult.",
  ["(a) True", "(b) True", "(c) True", "(d) False: skeletal muscles are striated",
   "(e) False: 40–50 per cent"],
  R_LOC("muscle"),
  why_others_wrong="A includes (e); B includes (d); D includes (d) and (e).",
  seconds=50)

Z(LOC, "Muscle contraction", "Advanced", "direct",
  "A motor neuron stimulates a skeletal muscle fibre and an action potential spreads through it, but a drug blocks "
  "the release of Ca²⁺ from the sarcoplasmic reticulum. What will happen?",
  ["Myosin heads will bind actin permanently, and the fibre will stay contracted",
   "Acetylcholine will not be released at the neuromuscular junction",
   "The A-bands will shorten while the I-bands stay unchanged",
   "Troponin will continue to mask the active sites on actin, so cross bridges cannot form and the fibre will not "
   "contract"], "D",
  "Role of calcium in muscle contraction",
  "NCERT: the action potential in the sarcolemma causes the release of Ca²⁺ into the sarcoplasm. Ca²⁺ binds to a "
  "subunit of troponin on the actin filaments and removes the masking of the active sites for myosin; only then can "
  "the myosin head bind actin to form a cross bridge. Without Ca²⁺ release the active sites stay masked and no "
  "contraction occurs.",
  ["Action potential → Ca²⁺ release from sarcoplasmic reticulum", "Ca²⁺ + troponin → active sites unmasked",
   "No Ca²⁺ → sites stay masked → no cross bridge → no contraction"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="Cross bridges cannot form at all without Ca²⁺; acetylcholine release happens earlier at the "
                   "nerve ending and is unaffected; A-bands never shorten during contraction.",
  seconds=45)

Z(LOC, "Types of movement", "Advanced", "statement_pair",
  sp("Flagellar movement helps in the swimming of spermatozoa, maintenance of the water current in the canal system "
     "of sponges and locomotion of protozoans like Euglena.",
     "Amoeboid movement is brought about by flagella."),
  STATEMENT_PAIR, "C",
  "Amoeboid, ciliary and flagellar movement",
  "NCERT: flagellar movement helps in the swimming of spermatozoa, maintenance of water current in the canal system "
  "of sponges and locomotion of protozoans like Euglena. Amoeboid movement is effected by pseudopodia formed by the "
  "streaming of protoplasm (as in Amoeba); cytoskeletal elements like microfilaments are also involved. Flagella do "
  "not cause amoeboid movement.",
  ["Statement I → true", "Statement II: amoeboid movement is by pseudopodia → false"],
  R_LOC("types of movement"),
  why_others_wrong="A and D accept the false Statement II; B rejects the true Statement I.",
  seconds=30)


# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nerve impulse generation and conduction", "Basic", "direct",
  "A nerve impulse is transmitted from one neuron to another through junctions called:",
  ["Nodes of Ranvier", "Neuromuscular junctions", "Synapses", "Nissl's granules"], "C",
  "Transmission of impulses",
  "NCERT: a nerve impulse is transmitted from one neuron to another through junctions called synapses. Nodes of "
  "Ranvier are gaps between adjacent myelin sheaths, a neuromuscular junction links a motor neuron to a muscle fibre, "
  "and Nissl's granules are granular bodies in the cell body.",
  ["Neuron-to-neuron junction → synapse"],
  R_NEU("generation and conduction of nerve impulse: transmission of impulses"),
  why_others_wrong="Nodes of Ranvier lie along one fibre; a neuromuscular junction links a neuron to a muscle; "
                   "Nissl's granules are not junctions.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "In the human forebrain, the cerebrum wraps around a structure called the:",
  ["Medulla oblongata", "Cerebellum", "Pons", "Thalamus"], "D",
  "Forebrain",
  "NCERT: the forebrain consists of the cerebrum, thalamus and hypothalamus. The cerebrum wraps around a structure "
  "called the thalamus, which is a major coordinating centre for sensory and motor signalling.",
  ["Cerebrum wraps around the thalamus"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="The medulla, cerebellum and pons are parts of the hindbrain, not wrapped by the cerebrum.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The cerebellum has a very convoluted surface. This:",
  ["Reduces the number of neurons it contains",
   "Provides additional space for many more neurons",
   "Allows the cerebellum to secrete hypothalamic hormones",
   "Connects the two cerebral hemispheres"], "B",
  "Hindbrain: cerebellum",
  "NCERT: the cerebellum has a very convoluted surface in order to provide the additional space for many more "
  "neurons.",
  ["Convoluted surface → more area → space for many more neurons"],
  R_NEU("central neural system: hindbrain"),
  why_others_wrong="The folding increases, not decreases, room for neurons; hypothalamic hormones come from the "
                   "hypothalamus; the corpus callosum connects the hemispheres.",
  seconds=20)

Z(NEU, "Neuron and nerves", "Basic", "match_list",
  ml(("neuron or nerve fibre", "where commonly found"),
     ["Multipolar neurons", "Bipolar neurons", "Myelinated nerve fibres", "Unmyelinated nerve fibres"],
     ["Autonomous and somatic neural systems", "Spinal and cranial nerves", "Retina of the eye",
      "Cerebral cortex"]),
  match_options(M("IV", "III", "II", "I"),
                [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"), M("II", "III", "IV", "I")], at="C"),
  "C",
  "Types of neurons and nerve fibres",
  "NCERT: multipolar neurons (one axon, two or more dendrites) are found in the cerebral cortex; bipolar neurons (one "
  "axon, one dendrite) in the retina of the eye. Myelinated nerve fibres are found in spinal and cranial nerves; "
  "unmyelinated fibres are commonly found in the autonomous and the somatic neural systems.",
  ["Multipolar → IV", "Bipolar → III", "Myelinated → II", "Unmyelinated → I"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="The other codes swap the multipolar and bipolar sites, the myelinated and unmyelinated sites, or "
                   "multipolar neurons with myelinated fibres.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Intermediate", "direct",
  "The inner parts of the cerebral hemispheres and a group of associated deep structures form a complex structure "
  "called the limbic lobe or limbic system. These deep structures include:",
  ["Pons and medulla", "Corpora quadrigemina", "Corpus callosum and cerebral aqueduct", "Amygdala and hippocampus"],
  "D",
  "Limbic system",
  "NCERT: the inner parts of the cerebral hemispheres and a group of associated deep structures like the amygdala, "
  "hippocampus, etc. form the limbic lobe or limbic system. Along with the hypothalamus, it is involved in the "
  "regulation of sexual behaviour, expression of emotional reactions and motivation.",
  ["Limbic system → inner cerebral hemispheres + amygdala, hippocampus, etc."],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="The pons and medulla are hindbrain; corpora quadrigemina and the cerebral aqueduct belong to the "
                   "midbrain; the corpus callosum is a fibre tract joining the hemispheres.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Intermediate", "assertion_reason",
  ar("The medulla oblongata is a part of the forebrain.",
     "The medulla of the brain is connected to the spinal cord."),
  ASSERTION_REASON, "D",
  "Hindbrain: medulla",
  "NCERT: the hindbrain comprises the pons, cerebellum and medulla (also called the medulla oblongata). The medulla "
  "of the brain is connected to the spinal cord. A places the medulla in the forebrain, so A is false; R is true.",
  ["Medulla → hindbrain → A false", "Medulla connected to spinal cord → R true"],
  R_NEU("central neural system: hindbrain"),
  why_others_wrong="A, B and C accept the false assertion.",
  seconds=25)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "statement_pair",
  sp("A synapse is formed by the membranes of a pre-synaptic neuron and a post-synaptic neuron, which may or may not "
     "be separated by a gap called the synaptic cleft.",
     "At a chemical synapse, neurotransmitters are released by the post-synaptic neuron and act on receptors of the "
     "pre-synaptic membrane."),
  STATEMENT_PAIR, "C",
  "Structure of a synapse",
  "NCERT: a synapse is formed by the membranes of a pre-synaptic neuron and a post-synaptic neuron, which may or may "
  "not be separated by a gap called the synaptic cleft. At a chemical synapse, the synaptic vesicles of the axon "
  "terminal (pre-synaptic side) release neurotransmitters into the cleft, and these bind to specific receptors on "
  "the post-synaptic membrane. Statement II reverses the direction.",
  ["Statement I → true", "Statement II: release is pre-synaptic, receptors are post-synaptic → false"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A and D accept the reversed Statement II; B rejects the true Statement I.",
  seconds=30)

_o = ["(a), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"]
ms_check("abd", _o, "B")
Z(NEU, "Neuron and nerves", "Intermediate", "multi_statement",
  ms("Which of the following statements about the structure of a neuron are correct?",
     ["A neuron is a microscopic structure composed of three major parts: the cell body, dendrites and axon.",
      "Axons transmit nerve impulses away from the cell body to a synapse or to a neuromuscular junction.",
      "The cell body of a neuron lacks typical cell organelles.",
      "Each branch of the axon terminates as a bulb-like structure called a synaptic knob.",
      "Dendrites transmit impulses away from the cell body."]),
  _o, "B",
  "Structure of a neuron",
  "NCERT: a neuron is a microscopic structure composed of three major parts: cell body, dendrites and axon. The cell "
  "body contains cytoplasm with typical cell organelles and Nissl's granules. Dendrites transmit impulses towards the "
  "cell body; the axon transmits impulses away from the cell body to a synapse or a neuromuscular junction. The "
  "distal end of the axon is branched, and each branch terminates as a bulb-like synaptic knob.",
  ["(a) True", "(b) True", "(c) False: typical organelles are present", "(d) True",
   "(e) False: dendrites carry impulses towards the cell body"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="A includes (c); C and D include (e).",
  seconds=50)

_o = ["(a), (b) and (c) only", "(b), (c) and (d) only", "(a) and (b) only", "(a) and (d) only"]
ms_check("ab", _o, "C")
Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human brain are correct?",
     ["The brain is the central information processing organ of the body and acts as the 'command and control "
      "system'.",
      "The human brain is well protected by the skull.",
      "The forebrain consists of the cerebrum, thalamus and medulla oblongata.",
      "The brain stem is formed by the cerebrum, pons and medulla oblongata."]),
  _o, "C",
  "Organisation of the brain",
  "NCERT: the brain is the central information processing organ of our body and acts as the 'command and control "
  "system'. The human brain is well protected by the skull. The forebrain consists of the cerebrum, thalamus and "
  "hypothalamus; the midbrain, pons and medulla oblongata form the brain stem.",
  ["(a) True", "(b) True", "(c) False: hypothalamus, not medulla", "(d) False: midbrain, not cerebrum"],
  R_NEU("central neural system"),
  why_others_wrong="A, B and D include the false (c) or (d).",
  seconds=40)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "direct",
  "In a resting neuron, the axoplasm has a high K⁺ and low Na⁺ concentration, while the outside fluid has a low K⁺ "
  "and high Na⁺ concentration. If the sodium-potassium pump of the axonal membrane were blocked, which would be the "
  "most direct consequence?",
  ["The membrane would become freely permeable to the negatively charged proteins of the axoplasm",
   "Na⁺ would start being pumped into the axoplasm in exchange for K⁺",
   "More K⁺ would be pumped in, making the inside of the membrane more negative",
   "These ionic gradients across the resting membrane would no longer be maintained"], "D",
  "Role of the sodium-potassium pump",
  "NCERT: the ionic gradients across the resting membrane are maintained by the active transport of ions by the "
  "sodium-potassium pump, which transports 3 Na⁺ outwards for 2 K⁺ into the cell. If the pump is blocked, the "
  "gradients it maintains can no longer be kept up.",
  ["Gradients are maintained by active transport through the Na⁺–K⁺ pump", "Pump blocked → gradients not maintained"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="The membrane stays impermeable to the axoplasmic proteins; a blocked pump transports nothing, so "
                   "it neither reverses nor speeds up.",
  seconds=40)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "assertion_reason",
  ar("When a stimulus is applied at a site on a polarised axonal membrane, the inner surface of the membrane at that "
     "site becomes positively charged with respect to the outer surface.",
     "At the site of stimulation, the membrane becomes freely permeable to Na⁺, which leads to a rapid influx of "
     "Na⁺."),
  ASSERTION_REASON, "A",
  "Depolarisation",
  "NCERT: when a stimulus is applied at a site on the polarised membrane, the membrane at that site becomes freely "
  "permeable to Na⁺. This leads to a rapid influx of Na⁺ followed by the reversal of the polarity at that site: the "
  "outer surface becomes negatively charged and the inner side positively charged. The Na⁺ influx causes the "
  "reversal, so R explains A.",
  ["A → true", "R → true", "Na⁺ influx → inside becomes positive → R explains A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="B ignores the causal sequence NCERT gives; C and D call a true statement false.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Advanced", "statement_pair",
  sp("The autonomic neural system relays impulses from the CNS to the involuntary organs and the smooth muscles of "
     "the body.",
     "The peripheral neural system is divided into two divisions: the somatic neural system and the autonomic "
     "neural system."),
  STATEMENT_PAIR, "A",
  "Divisions of the PNS",
  "NCERT: the PNS is divided into the somatic neural system and the autonomic neural system. The somatic system "
  "relays impulses from the CNS to the skeletal muscles, while the autonomic system transmits impulses from the CNS "
  "to the involuntary organs and smooth muscles of the body. The autonomic system is further divided into "
  "sympathetic and parasympathetic systems.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("human neural system"),
  why_others_wrong="Both statements are true, so B, C and D are wrong.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "direct",
  "At a chemical synapse, a drug blocks the specific receptors on the post-synaptic membrane. An impulse arriving at "
  "the axon terminal still causes neurotransmitters to be released into the synaptic cleft. What will follow?",
  ["The neurotransmitters cannot bind and open ion channels, so no new potential is generated in the post-synaptic "
   "neuron",
   "The impulse will cross the cleft as an electrical current instead",
   "The pre-synaptic neuron will stop being excitable",
   "The post-synaptic neuron will generate an excitatory potential more quickly"], "A",
  "Chemical transmission across a synapse",
  "NCERT: the released neurotransmitters bind to their specific receptors on the post-synaptic membrane. This binding "
  "opens ion channels allowing the entry of ions, which can generate a new potential in the post-synaptic neuron. If "
  "the receptors are blocked, binding cannot occur, the channels do not open and no new potential arises.",
  ["Transmitter release → binding to post-synaptic receptors → ion channels open → new potential",
   "Receptors blocked → chain stops at binding"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A chemical synapse cannot switch to electrical transmission; the pre-synaptic neuron is "
                   "unaffected; with receptors blocked no potential, excitatory or inhibitory, is produced.",
  seconds=40)


# ---------------------------------------------------------------- checks and output
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
           "notes": "BATCH_004 package ZOO_004_p1: 121 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "facts already tested in BATCH_000-BATCH_003; every numerical answer re-derived by "
                    "tools/batch_004/ZOO_004_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
