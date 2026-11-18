"""Writes batches/parts/BATCH_003_ZOO_p1.json: package ZOO_003_p1 of BATCH_003 (Zoology, 128 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_000501 .. NEET_ZOO_000628. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11 Biology
textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion). Facts already tested in
BATCH_000, BATCH_001 and BATCH_002 (see `merge_batch.py stems 003 ZOO_003_p1`) are not tested again.

    python docs/neet-bank/tools/batch_003/ZOO_003_p1.py
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
PACKAGE = "ZOO_003_p1"
BATCH = "BATCH_003"
FIRST_ID, LAST_ID = 501, 628
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
# Biomolecules: rule of thumb, rate doubles for every 10 degC rise; 20 degC -> 50 degC is three 10-degree steps.
RATE_FACTOR = 2 ** ((50 - 20) // 10)
assert RATE_FACTOR == 8
assert (50 - 20) // 10 == 3 and 2 * 3 == 6 and F(50, 20) == F(5, 2)   # distractors: 3R, 6R, 2.5R

# Biomolecules: fatty acids esterified in 3 monoglycerides, 4 diglycerides and 2 triglycerides.
FATTY = 3 * 1 + 4 * 2 + 2 * 3
assert FATTY == 17
assert 3 + 4 + 2 == 9 and (3 + 4 + 2) * 3 == 27 and FATTY + 9 == 26    # distractors: molecules; all tri; + glycerol

# Body fluids: nearly 80 per cent of humans are Rh positive; Rh-negative persons expected among 650.
RH_NEG = 650 * F(20, 100)
assert RH_NEG == 130
assert 650 * F(80, 100) == 520 and 650 * F(10, 100) == 65 and 650 * F(1, 2) == 325   # distractors

# Locomotion: wrist + palm + digits of both hands = 2 x (8 carpals + 5 metacarpals + 14 phalanges).
HAND = 2 * (8 + 5 + 14)
assert HAND == 54
assert 8 + 5 + 14 == 27 and 2 * (7 + 5 + 14) == 52 and 2 * 30 == 60      # distractors: one hand; feet; whole limbs

# Locomotion: ribs reaching the sternum directly (true ribs, 7 pairs) or via the 7th rib's cartilage (8th-10th pairs).
STERNAL = 2 * 7 + 2 * 3
assert STERNAL == 20
assert 2 * 7 == 14 and 7 + 3 == 10 and 2 * 12 == 24                     # distractors: true only; pairs; all ribs

# Locomotion: vertebrae between the last cervical and the sacral vertebra = thoracic 12 + lumbar 5.
BETWEEN = 12 + 5
assert BETWEEN == 17 and 7 + 12 + 5 + 1 + 1 == 26
assert 26 - 7 == 19 and 26 - 2 == 24                                    # distractors: only cervical removed; fused


# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Basis of classification", "Basic", "direct",
  "In which of the following groups are cells performing the same function arranged into tissues, without "
  "tissues being grouped into organs (tissue level of organisation)?",
  ["Porifera", "Platyhelminthes", "Coelenterata", "Annelida"], "C",
  "Levels of organisation",
  "NCERT: in sponges the cells are loose aggregates (cellular level). In coelenterates the arrangement is more "
  "complex: cells performing the same function are arranged into tissues (tissue level). From Platyhelminthes "
  "onwards tissues are grouped into organs (organ level), and in annelids, arthropods, molluscs, echinoderms and "
  "chordates organs associate to form organ systems (organ-system level).",
  ["Porifera → cellular level", "Coelenterata → tissue level", "Platyhelminthes → organ level",
   "Annelida → organ-system level"],
  R_AK("basis of classification: levels of organisation"),
  why_others_wrong="Porifera stop at the cellular level; flatworms form organs; annelids form organ systems.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Over two-thirds of all named species on earth belong to the phylum:",
  ["Arthropoda", "Mollusca", "Chordata", "Annelida"], "A",
  "Arthropoda, the largest phylum",
  "NCERT: Arthropoda is the largest phylum of Animalia; over two-thirds of all named species on earth are "
  "arthropods. Mollusca is the second largest animal phylum.",
  ["Largest phylum → Arthropoda (over two-thirds of named species)", "Second largest → Mollusca"],
  R_AK("classification of animals: phylum Arthropoda"),
  why_others_wrong="Mollusca is the second largest phylum; chordates and annelids are far fewer in species.",
  seconds=20)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "A file-like rasping organ for feeding, called the radula, is present in the mouth of:",
  ["Annelids", "Molluscs", "Echinoderms", "Hemichordates"], "B",
  "Features of Mollusca",
  "In molluscs the body has a distinct head, a muscular foot and a visceral hump, and the mouth contains a "
  "file-like rasping organ for feeding called the radula.",
  ["Radula → file-like rasping feeding organ", "Present in the mouth of molluscs"],
  R_AK("phylum Mollusca"),
  why_others_wrong="Annelids, echinoderms and hemichordates have no radula.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Some cartilaginous fishes possess electric organs. An example is:",
  ["Trygon", "Pristis", "Scoliodon", "Torpedo"], "D",
  "Features of Chondrichthyes",
  "NCERT: some members of Chondrichthyes have electric organs (e.g. Torpedo) and some possess a poison sting "
  "(e.g. Trygon, the sting ray). Pristis is the saw fish and Scoliodon the dog fish.",
  ["Electric organs → Torpedo", "Poison sting → Trygon"],
  R_AK("class Chondrichthyes"),
  why_others_wrong="Trygon has a poison sting, not an electric organ; Pristis (saw fish) and Scoliodon (dog fish) "
                   "are not cited for electric organs.",
  seconds=20)

Z(AK, "Non-chordate phyla", "Basic", "match_list",
  ml(("echinoderm", "common name"), ["Asterias", "Echinus", "Antedon", "Cucumaria"],
     ["Sea cucumber", "Sea lily", "Sea urchin", "Star fish"]),
  match_options(M("IV", "III", "II", "I"),
                [M("IV", "II", "III", "I"), M("III", "IV", "I", "II"), M("I", "III", "II", "IV")], at="A"),
  "A",
  "Examples of Echinodermata",
  "NCERT examples of echinoderms: Asterias (star fish), Echinus (sea urchin), Antedon (sea lily), Cucumaria (sea "
  "cucumber) and Ophiura (brittle star).",
  ["Asterias → star fish (IV)", "Echinus → sea urchin (III)", "Antedon → sea lily (II)",
   "Cucumaria → sea cucumber (I)"],
  R_AK("phylum Echinodermata"),
  why_others_wrong="The other codes swap the sea urchin with the sea lily, or the star fish with the sea cucumber.",
  seconds=35)

Z(AK, "Chordate classes", "Basic", "direct",
  "Which of the following reptiles is a poisonous snake?",
  ["Chameleon", "Alligator", "Testudo", "Bangarus"], "D",
  "Examples of Reptilia",
  "NCERT lists Naja (cobra), Bangarus (krait) and Vipera (viper) as poisonous snakes. Chameleon is the tree lizard, "
  "Alligator is an alligator and Testudo is the tortoise.",
  ["Poisonous snakes → Naja, Bangarus, Vipera", "Bangarus → krait"],
  R_AK("class Reptilia"),
  why_others_wrong="Chameleon is a tree lizard, Alligator a crocodilian and Testudo a tortoise; none is a snake.",
  seconds=20)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "Bioluminescence, the property of a living organism to emit light, is well-marked in:",
  ["Coelenterates", "Ctenophores", "Echinoderms", "Hemichordates"], "B",
  "Features of Ctenophora",
  "Ctenophores (sea walnuts or comb jellies) are exclusively marine, radially symmetrical and diploblastic. NCERT "
  "states that bioluminescence (the property of a living organism to emit light) is well-marked in ctenophores.",
  ["Ctenophora → sea walnuts / comb jellies", "Bioluminescence well-marked"],
  R_AK("phylum Ctenophora"),
  why_others_wrong="NCERT does not cite bioluminescence for coelenterates, echinoderms or hemichordates.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "Planaria, which possesses a high regeneration capacity, belongs to the same phylum as:",
  ["Taenia", "Ascaris", "Hirudinaria", "Pila"], "A",
  "Platyhelminthes",
  "NCERT: some members of Platyhelminthes, like Planaria, possess a high regeneration capacity. Taenia (tapeworm) "
  "and Fasciola (liver fluke) are the other examples of this phylum.",
  ["Planaria → Platyhelminthes", "Taenia (tapeworm) → Platyhelminthes"],
  R_AK("phylum Platyhelminthes"),
  why_others_wrong="Ascaris is an aschelminth, Hirudinaria (blood-sucking leech) an annelid and Pila (apple snail) "
                   "a mollusc.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("Sponges are hermaphrodite: eggs and sperms are produced by the same individual.",
     "Sponges reproduce asexually by fragmentation."),
  ASSERTION_REASON, "B",
  "Reproduction in Porifera",
  "Both are NCERT statements about sponges. Sexes are not separate (hermaphrodite), i.e. eggs and sperms are "
  "produced by the same individual. Asexual reproduction is by fragmentation, and sexual reproduction by the "
  "formation of gametes. The ability to fragment says nothing about why one individual makes both gametes, so R "
  "does not explain A.",
  ["A: hermaphrodite → true", "R: asexual reproduction by fragmentation → true",
   "Asexual fragmentation is unrelated to the sexual condition → R does not explain A"],
  R_AK("phylum Porifera"),
  why_others_wrong="A claims a causal link that does not exist; C and D call a true statement false.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("Aschelminthes are dioecious, and often the females are longer than the males.",
     "In aschelminths, the alimentary canal is complete with a well-developed muscular pharynx."),
  STATEMENT_PAIR, "A",
  "Features of Aschelminthes",
  "NCERT: in roundworms sexes are separate (dioecious), males and females are distinct, and often females are "
  "longer than males. The alimentary canal is complete with a well-developed muscular pharynx. Both statements "
  "are true.",
  ["Dioecious; females often longer → I true", "Complete gut with muscular pharynx → II true"],
  R_AK("phylum Aschelminthes"), seconds=30)

Z(AK, "Chordate classes", "Intermediate", "match_list",
  ml(("mammal", "common name"), ["Pteropus", "Macropus", "Delphinus", "Balaenoptera"],
     ["Blue whale", "Kangaroo", "Flying fox", "Common dolphin"]),
  match_options(M("III", "II", "IV", "I"),
                [M("II", "III", "IV", "I"), M("III", "II", "I", "IV"), M("IV", "II", "III", "I")], at="C"),
  "C",
  "Examples of Mammalia",
  "NCERT examples of viviparous mammals include Macropus (kangaroo), Pteropus (flying fox), Delphinus (common "
  "dolphin) and Balaenoptera (blue whale).",
  ["Pteropus → flying fox (III)", "Macropus → kangaroo (II)", "Delphinus → common dolphin (IV)",
   "Balaenoptera → blue whale (I)"],
  R_AK("class Mammalia"),
  why_others_wrong="The other codes swap the flying fox with the kangaroo, the dolphin with the whale, or the "
                   "flying fox with the dolphin.",
  seconds=35)

_o = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only", "(a), (b) and (c) only"]
ms_check("abc", _o, "D")
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements about phylum Arthropoda are correct?",
     ["Arthropods show the organ-system level of organisation.",
      "The body of arthropods is covered by a chitinous exoskeleton.",
      "Respiratory organs are gills, book gills, book lungs or a tracheal system.",
      "Statocysts are the organs of vision.",
      "Fertilisation is usually external."]),
  _o, "D",
  "Features of Arthropoda",
  "Arthropods are bilaterally symmetrical, triploblastic, segmented, coelomate animals with organ-system level of "
  "organisation and a chitinous exoskeleton. Respiration is by gills, book gills, book lungs or tracheal system. "
  "Sensory organs include antennae, eyes (compound and simple) and statocysts, which are balancing organs. "
  "Fertilisation is usually internal.",
  ["(a) True", "(b) True", "(c) True", "(d) False: statocysts are balancing organs",
   "(e) False: fertilisation is usually internal"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="A includes (d); B and C include (e) and leave out true statements.",
  seconds=50)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("mollusc", "common name"), ["Pila", "Sepia", "Loligo", "Octopus"],
     ["Devil fish", "Squid", "Apple snail", "Cuttlefish"]),
  match_options(M("III", "IV", "II", "I"),
                [M("III", "II", "IV", "I"), M("IV", "III", "II", "I"), M("III", "IV", "I", "II")], at="C"),
  "C",
  "Examples of Mollusca",
  "NCERT examples of molluscs: Pila (apple snail), Pinctada (pearl oyster), Sepia (cuttlefish), Loligo (squid), "
  "Octopus (devil fish), Aplysia (sea hare), Dentalium (tusk shell) and Chaetopleura (chiton).",
  ["Pila → apple snail (III)", "Sepia → cuttlefish (IV)", "Loligo → squid (II)", "Octopus → devil fish (I)"],
  R_AK("phylum Mollusca"),
  why_others_wrong="The other codes swap Sepia with Loligo, Pila with Sepia, or Loligo with Octopus.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("Cyclostomes bear scales and paired fins.",
     "In cyclostomes, the cranium and the vertebral column are bony."),
  STATEMENT_PAIR, "B",
  "Features of Cyclostomata",
  "NCERT: cyclostomes have an elongated body bearing 6–15 pairs of gill slits for respiration; scales and paired "
  "fins are absent; the cranium and vertebral column are cartilaginous. Both statements are false.",
  ["Scales and paired fins absent → I false", "Cranium and vertebral column cartilaginous → II false"],
  R_AK("class Cyclostomata"), seconds=30)

Z(AK, "Chordate classes", "Advanced", "assertion_reason",
  ar("All chordates are vertebrates.",
     "In vertebrates, the notochord is replaced by a cartilaginous or bony vertebral column in the adult."),
  ASSERTION_REASON, "D",
  "Chordates and vertebrates",
  "Members of subphylum Vertebrata possess a notochord during the embryonic period, which is replaced by a "
  "cartilaginous or bony vertebral column in the adult. Urochordates and cephalochordates are chordates without a "
  "vertebral column. Hence all vertebrates are chordates, but all chordates are not vertebrates. A is false; R is "
  "true.",
  ["Urochordata and Cephalochordata lack a vertebral column → A false",
   "Notochord replaced by vertebral column in adult vertebrates → R true"],
  R_AK("phylum Chordata: subphylum Vertebrata"),
  why_others_wrong="A and B treat a false assertion as true; C calls the true reason false.",
  seconds=35)

_o = ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (e) only", "(a), (c) and (e) only"]
ms_check("abce", _o, "C")
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following statements about the classification of chordates are correct?",
     ["Petromyzon and Myxine belong to the division Agnatha.",
      "Chondrichthyes and Osteichthyes are placed in the super class Pisces of the division Gnathostomata.",
      "Amphibia, Reptilia, Aves and Mammalia form the super class Tetrapoda.",
      "Cephalochordates possess a vertebral column.",
      "Ascidia, Salpa and Doliolum are urochordates."]),
  _o, "C",
  "Classification of Chordata",
  "Vertebrata is divided into Agnatha (lacking jaws; class Cyclostomata, e.g. Petromyzon and Myxine) and "
  "Gnathostomata (bearing jaws). Gnathostomata has super class Pisces (Chondrichthyes, Osteichthyes) and "
  "super class Tetrapoda (Amphibia, Reptilia, Aves, Mammalia). Urochordates (Ascidia, Salpa, Doliolum) and "
  "cephalochordates (Branchiostoma) are protochordates without a vertebral column.",
  ["(a) True", "(b) True", "(c) True", "(d) False: cephalochordates have a notochord, no vertebral column",
   "(e) True"],
  R_AK("phylum Chordata: classification"),
  why_others_wrong="A and B include the false statement (d); D leaves out the true statement (b).",
  seconds=60)

Z(AK, "Chordate classes", "Advanced", "match_list",
  ml(("animal", "class"), ["Ichthyophis", "Exocoetus", "Pristis", "Neophron"],
     ["Aves", "Chondrichthyes", "Osteichthyes", "Amphibia"]),
  match_options(M("IV", "III", "II", "I"),
                [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"), M("IV", "III", "I", "II")], at="D"),
  "D",
  "Vertebrate classes and examples",
  "Ichthyophis is the limbless amphibian; Exocoetus (flying fish) is a marine bony fish; Pristis (saw fish) is a "
  "cartilaginous fish; Neophron (vulture) is a bird. The names 'fish' in flying fish and saw fish do not decide "
  "which fish class they belong to: their endoskeletons do.",
  ["Ichthyophis → Amphibia (IV)", "Exocoetus → Osteichthyes (III)", "Pristis → Chondrichthyes (II)",
   "Neophron → Aves (I)"],
  R_AK("vertebrate classes"),
  why_others_wrong="The other codes swap the two fish classes, the amphibian with the bony fish, or the saw fish "
                   "with the vulture.",
  seconds=45)

Z(AK, "Non-chordate phyla", "Advanced", "direct",
  "Which of the following features is shared by Mollusca and Echinodermata?",
  ["Sexes are usually separate and development is indirect",
   "A water vascular system helps in locomotion and capture of food",
   "A soft spongy mantle covers the visceral hump",
   "The adults are radially symmetrical"], "A",
  "Comparing Mollusca and Echinodermata",
  "Molluscs are usually dioecious and oviparous with indirect development. In echinoderms, sexes are separate and "
  "development is indirect with a free-swimming larva. The water vascular system and adult radial symmetry are "
  "echinoderm features; the mantle over the visceral hump is a mollusc feature.",
  ["Mollusca: usually dioecious, indirect development", "Echinodermata: sexes separate, indirect development",
   "Water vascular system, radial adults → echinoderms only; mantle → molluscs only"],
  R_AK("phyla Mollusca and Echinodermata"),
  why_others_wrong="B and D are found only in echinoderms; C is found only in molluscs.",
  seconds=45)

Z(AK, "Chordate classes", "Advanced", "statement_pair",
  sp("In bony fishes, fertilisation is usually external, they are mostly oviparous, and development is direct.",
     "In bony fishes, the mouth is mostly ventral."),
  STATEMENT_PAIR, "C",
  "Osteichthyes compared with Chondrichthyes",
  "NCERT on Osteichthyes: the mouth is mostly terminal; sexes are separate, fertilisation is usually external, "
  "they are mostly oviparous and development is direct. A ventral mouth is a feature of cartilaginous fishes. So "
  "Statement I is true and Statement II is false.",
  ["Bony fish: external fertilisation, oviparous, direct development → I true",
   "Mouth mostly terminal (ventral in Chondrichthyes) → II false"],
  R_AK("class Osteichthyes"), seconds=35)

Z(AK, "Non-chordate phyla", "Advanced", "assertion_reason",
  ar("Corals have a skeleton composed of calcium carbonate.",
     "Cnidoblasts present on the tentacles and the body of cnidarians are used for anchorage, defence and the "
     "capture of prey."),
  ASSERTION_REASON, "B",
  "Features of Coelenterata",
  "Both are NCERT statements on coelenterates. Cnidarians that form corals have a skeleton of calcium carbonate. "
  "Cnidoblasts (cnidocytes), stinging cells on the tentacles and body, serve in anchorage, defence and capture of "
  "prey. The stinging cells have nothing to do with the composition of the coral skeleton, so R does not explain A.",
  ["A: coral skeleton of CaCO₃ → true", "R: cnidoblasts for anchorage, defence, prey capture → true",
   "Stinging cells do not explain skeletal composition → R does not explain A"],
  R_AK("phylum Coelenterata (Cnidaria)"),
  why_others_wrong="A claims a causal link that does not exist; C and D call a true statement false.",
  seconds=35)

# ================================================================ Structural Organisation in Animals (B4 I6 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Areolar tissue, a loose connective tissue present beneath the skin, contains:",
  ["Chondrocytes and osteocytes", "Neurons and neuroglial cells", "Only adipocytes",
   "Fibroblasts, macrophages and mast cells"], "D",
  "Loose connective tissue",
  "NCERT: areolar tissue present beneath the skin often serves as a support framework for epithelium. It contains "
  "fibroblasts (cells that produce and secrete fibres), macrophages and mast cells.",
  ["Areolar tissue → fibroblasts, macrophages, mast cells"],
  R_SOA("connective tissue: loose connective tissue"),
  why_others_wrong="Chondrocytes and osteocytes belong to cartilage and bone; neurons and neuroglia to neural "
                   "tissue; fat-storing cells dominate adipose tissue, not areolar tissue.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "In the male frog, the testes are found adhered to the upper part of the kidneys by a double fold of "
  "peritoneum called the:",
  ["Pericardium", "Mesorchium", "Mesentery", "Cloaca"], "B",
  "Male reproductive organs of the frog",
  "The male frog has a pair of yellowish, ovoid testes found adhered to the upper part of the kidneys by a double "
  "fold of peritoneum called the mesorchium.",
  ["Testes → yellowish, ovoid", "Attached to upper part of kidneys by mesorchium"],
  R_SOA("frog: reproductive system"),
  why_others_wrong="The pericardium covers the heart; the mesentery is not named by NCERT here; the cloaca is the "
                   "common chamber opening to the exterior.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "Frogs can change their colour to hide from their enemies (camouflage). NCERT calls this protective coloration:",
  ["Aestivation", "Hibernation", "Mimicry", "Metamorphosis"], "C",
  "Morphology of the frog",
  "NCERT: frogs have the ability to change colour to hide them from their enemies (camouflage); this protective "
  "coloration is called mimicry.",
  ["Colour change to hide → camouflage", "Protective coloration → mimicry"],
  R_SOA("frog: morphology"),
  why_others_wrong="Aestivation and hibernation are summer and winter sleep; metamorphosis is the change of a "
                   "tadpole into an adult.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Compound epithelium covers the dry surface of the skin and lines the ducts of salivary glands and the "
     "pancreatic ducts.",
     "The main function of compound epithelium is to provide protection against chemical and mechanical stresses."),
  STATEMENT_PAIR, "A",
  "Compound epithelium",
  "NCERT: compound epithelium covers the dry surface of the skin, the moist surface of the buccal cavity and "
  "pharynx, the inner lining of the ducts of salivary glands and of pancreatic ducts. Its main function is to "
  "provide protection against chemical and mechanical stresses. Both statements are true.",
  ["Locations: skin, buccal cavity, pharynx, salivary and pancreatic ducts → I true",
   "Function: protection against chemical and mechanical stresses → II true"],
  R_SOA("epithelial tissue: compound epithelium"), seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "In the frog, a special venous connection between the liver and the intestine forms the hepatic portal system. "
  "A similar special venous connection, the renal portal system, exists between the:",
  ["Lungs and the heart", "Brain and the spinal cord", "Skin and the lungs",
   "Kidneys and the lower parts of the body"], "D",
  "Circulatory system of the frog",
  "NCERT: in the frog, a special venous connection between the liver and intestine is the hepatic portal system, "
  "and that between the kidney and the lower parts of the body is the renal portal system.",
  ["Liver–intestine → hepatic portal system", "Kidney–lower parts of body → renal portal system"],
  R_SOA("frog: circulatory system"),
  why_others_wrong="NCERT describes no portal system between the lungs and heart, brain and spinal cord, or skin "
                   "and lungs.",
  seconds=25)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "During aestivation and hibernation, gaseous exchange in the frog takes place through the:",
  ["Lungs", "Buccal cavity", "Skin", "Gills"], "C",
  "Respiration in the frog",
  "NCERT: during aestivation and hibernation, gaseous exchange in the frog takes place through the skin.",
  ["Aestivation / hibernation → cutaneous gas exchange"],
  R_SOA("frog: respiratory system"),
  why_others_wrong="Lungs and the buccal cavity work on land in the active frog; the adult frog has no gills.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("The alimentary canal of the frog is short.",
     "Frogs are carnivores, and hence the length of their intestine is reduced."),
  ASSERTION_REASON, "A",
  "Alimentary canal of the frog",
  "NCERT: the alimentary canal of the frog is short because frogs are carnivores and hence the length of the "
  "intestine is reduced. R gives the reason for A.",
  ["A: short alimentary canal → true", "R: carnivorous, intestine reduced → true", "NCERT links them with 'because'"],
  R_SOA("frog: anatomy, digestive system"),
  why_others_wrong="B denies the causal link NCERT states; C and D call a true statement false.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("Ten pairs of cranial nerves arise from the brain of the frog.",
     "In the frog, the peripheral neural system consists of the brain and the spinal cord."),
  STATEMENT_PAIR, "C",
  "Neural system of the frog",
  "The frog's neural system has a central neural system (brain and spinal cord), a peripheral neural system "
  "(cranial and spinal nerves) and an autonomic neural system (sympathetic and parasympathetic). Ten pairs of "
  "cranial nerves arise from the brain. Statement I is true; Statement II describes the central neural system, so "
  "it is false.",
  ["Ten pairs of cranial nerves → I true", "Brain and spinal cord = CNS; PNS = cranial and spinal nerves → II false"],
  R_SOA("frog: control and coordination"), seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "match_list",
  ml(("part", "feature in the frog"), ["Fore-brain", "Mid-brain", "Hind-brain", "Cranium"],
     ["Bony brain box enclosing the brain", "Cerebellum and medulla oblongata", "A pair of optic lobes",
      "Olfactory lobes, paired cerebral hemispheres and unpaired diencephalon"]),
  match_options(M("IV", "III", "II", "I"),
                [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"), M("IV", "III", "I", "II")], at="B"),
  "B",
  "Brain of the frog",
  "The frog's brain is enclosed in a bony structure called the brain box (cranium). It is divided into the "
  "fore-brain (olfactory lobes, paired cerebral hemispheres and unpaired diencephalon), the mid-brain (a pair of "
  "optic lobes) and the hind-brain (cerebellum and medulla oblongata).",
  ["Fore-brain → IV", "Mid-brain → III", "Hind-brain → II", "Cranium → I"],
  R_SOA("frog: neural system"),
  why_others_wrong="The other codes swap the fore- and mid-brain, the mid- and hind-brain, or the hind-brain with "
                   "the cranium.",
  seconds=40)

_o = ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only", "(a), (b), (c) and (d) only"]
ms_check("abcd", _o, "D")
Z(SOA, "Animal tissues", "Intermediate", "multi_statement",
  ms("Which of the following statements about muscle tissue are correct?",
     ["Each muscle is made of many long, cylindrical fibres arranged in parallel arrays.",
      "Muscle fibres are composed of numerous fine fibrils called myofibrils.",
      "In a typical skeletal muscle such as the biceps, a sheath of tough connective tissue encloses several "
      "bundles of muscle fibres.",
      "Smooth muscle fibres are held together by cell junctions and bundled together in a connective tissue sheath.",
      "Cardiac muscle is a voluntary muscle."]),
  _o, "D",
  "Muscle tissue",
  "NCERT: each muscle is made of many long cylindrical fibres arranged in parallel arrays, composed of fine "
  "myofibrils. In the biceps, striated fibres are bundled in parallel and a sheath of tough connective tissue "
  "encloses several bundles. Smooth muscle fibres are held together by cell junctions and bundled in a connective "
  "tissue sheath. Cardiac muscle, found only in the heart, is involuntary.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: cardiac muscle is involuntary"],
  R_SOA("muscle tissue"),
  why_others_wrong="A and C include the false statement (e); B leaves out the true statement (a).",
  seconds=50)

_o = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
ms_check("abc", _o, "B")
Z(SOA, "Frog: morphology and anatomy", "Advanced", "multi_statement",
  ms("Which of the following statements about the frog are correct?",
     ["Frogs eat insects and thus protect the crop.",
      "Frogs maintain ecological balance because they serve as an important link of the food chain and food web.",
      "The frog has a thin-walled urinary bladder, ventral to the rectum, which also opens into the cloaca.",
      "The lymph of the frog contains more proteins and RBCs than its blood.",
      "The frog captures its food with a single-lobed tongue."]),
  _o, "B",
  "Anatomy and importance of the frog",
  "Frogs are beneficial: they eat insects and protect the crop, and maintain ecological balance as an important "
  "link of the food chain and food web. A thin-walled urinary bladder lies ventral to the rectum and opens into "
  "the cloaca. Lymph differs from blood: it lacks a few proteins and RBCs. Food is captured by the bilobed tongue.",
  ["(a) True", "(b) True", "(c) True", "(d) False: lymph lacks a few proteins and RBCs",
   "(e) False: the tongue is bilobed"],
  R_SOA("frog: anatomy"),
  why_others_wrong="A includes (d); C and D include (e) and/or (d) and leave out true statements.",
  seconds=55)

Z(SOA, "Animal tissues", "Advanced", "assertion_reason",
  ar("Connective tissues are the most abundant and widely distributed tissues in the body of complex animals.",
     "In all connective tissues, including blood, the cells secrete fibres of structural proteins called collagen "
     "or elastin."),
  ASSERTION_REASON, "C",
  "Connective tissue",
  "NCERT: connective tissues are the most abundant and widely distributed in the body of complex animals. In all "
  "connective tissues except blood, the cells secrete fibres of collagen or elastin. Blood, a fluid connective "
  "tissue, is the exception, so R (which includes blood) is false.",
  ["A: most abundant and widely distributed → true", "R: blood is the exception → false"],
  R_SOA("connective tissue"),
  why_others_wrong="A and B accept the false reason; D calls the true assertion false.",
  seconds=35)

Z(SOA, "Animal tissues", "Advanced", "statement_pair",
  sp("Squamous epithelium is made of a single thin layer of flattened cells with regular boundaries.",
     "Columnar epithelium is composed of a single layer of tall and slender cells whose nuclei are located at the "
     "base, and their free surface may have microvilli."),
  STATEMENT_PAIR, "D",
  "Simple epithelia",
  "NCERT: squamous epithelium is a single thin layer of flattened cells with irregular boundaries, so Statement I "
  "is false. Columnar epithelium is a single layer of tall, slender cells with basal nuclei; the free surface may "
  "have microvilli. Statement II is true.",
  ["Squamous cells have irregular boundaries → I false", "Columnar: tall, basal nuclei, may have microvilli → II true"],
  R_SOA("epithelial tissue: simple epithelium"), seconds=35)

_o = ["(a), (b), (c) and (e) only", "(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only"]
ms_check("abce", _o, "A")
Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("Which of the following statements about glands are correct?",
     ["The salivary gland is an example of a multicellular gland.",
      "Endocrine glands do not have ducts, and their products, called hormones, are secreted directly into the "
      "fluid bathing the gland.",
      "Exocrine glands release their products through ducts or tubes.",
      "Exocrine glands secrete hormones directly into the blood.",
      "Some columnar or cuboidal cells get specialised for secretion and are called glandular epithelium."]),
  _o, "A",
  "Glandular epithelium",
  "Some columnar or cuboidal cells specialise for secretion as glandular epithelium. Glands may be unicellular "
  "(goblet cells) or multicellular (salivary gland). Exocrine glands release their products (mucus, saliva, "
  "earwax, oil, milk, digestive enzymes) through ducts; endocrine glands lack ducts and secrete hormones directly "
  "into the fluid bathing the gland.",
  ["(a) True", "(b) True", "(c) True", "(d) False: that describes endocrine glands", "(e) True"],
  R_SOA("epithelial tissue: glandular epithelium"),
  why_others_wrong="B, C and D include the false statement (d); B and D also leave out true statements.",
  seconds=55)

# ================================================================ Biomolecules (B6 I7 A6)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "The most abundant protein in the whole of the biosphere is:",
  ["Collagen", "RuBisCO", "Haemoglobin", "Insulin"], "B",
  "Abundant proteins",
  "NCERT: collagen is the most abundant protein in the animal world, while ribulose bisphosphate carboxylase-"
  "oxygenase (RuBisCO) is the most abundant protein in the whole of the biosphere.",
  ["Animal world → collagen", "Whole biosphere → RuBisCO"],
  R_BIO("proteins"),
  why_others_wrong="Collagen is the most abundant only in the animal world; haemoglobin and insulin are not cited "
                   "as the most abundant.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "Amino acids differ in their R group. In serine, the R group is a:",
  ["Hydrogen atom", "Methyl group", "Hydroxy methyl group", "Phenyl group"], "C",
  "R groups of amino acids",
  "Amino acids are substituted methanes. The R group gives each amino acid its identity: hydrogen in glycine, a "
  "methyl group in alanine and a hydroxy methyl group in serine.",
  ["Glycine → H", "Alanine → –CH₃", "Serine → –CH₂OH (hydroxy methyl)"],
  R_BIO("how to analyse chemical composition?: amino acids"),
  why_others_wrong="Hydrogen is the R group of glycine and methyl that of alanine; a phenyl group is not the R "
                   "group of serine.",
  seconds=20)

Z(BIO, "Nucleic acids", "Basic", "match_list",
  ml(("component of the cell", "approximate per cent of the total cellular mass"),
     ["Water", "Proteins", "Nucleic acids", "Lipids"], ["2", "5–7", "10–15", "70–90"]),
  match_options(M("IV", "III", "II", "I"),
                [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"), M("IV", "III", "I", "II")], at="A"),
  "A",
  "Average composition of cells",
  "NCERT gives the average composition of cells as a per cent of total cellular mass: water 70–90, proteins 10–15, "
  "nucleic acids 5–7, carbohydrates 3, lipids 2 and ions 1. Water is the most abundant chemical in living "
  "organisms.",
  ["Water → 70–90 (IV)", "Proteins → 10–15 (III)", "Nucleic acids → 5–7 (II)", "Lipids → 2 (I)"],
  R_BIO("biomacromolecules: average composition of cells"),
  why_others_wrong="The other codes swap proteins with nucleic acids, water with proteins, or nucleic acids with "
                   "lipids.",
  seconds=35)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "The hydrolysis of starch into glucose is an example of a/an:",
  ["Physical change involving only a change in shape", "Change in the state of matter",
   "Inorganic chemical reaction", "Organic chemical reaction"], "D",
  "Types of changes in chemical compounds",
  "NCERT: a physical change is a change in shape without breaking of bonds; melting of ice is a change in state. "
  "When bonds are broken and new bonds formed, it is a chemical reaction. Ba(OH)₂ + H₂SO₄ → BaSO₄ + 2H₂O is an "
  "inorganic chemical reaction, while hydrolysis of starch into glucose is an organic chemical reaction.",
  ["Bonds broken and formed → chemical reaction", "Starch → glucose → organic chemical reaction"],
  R_BIO("enzymes: chemical reactions"),
  why_others_wrong="Hydrolysis breaks glycosidic bonds, so it is not a physical change or a change of state; NCERT "
                   "gives the barium hydroxide–sulphuric acid reaction as the inorganic example.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Basic", "statement_pair",
  sp("Some proteins are involved in transporting nutrients across the cell membrane.",
     "Receptors are proteins involved in sensory reception, for example of smell, taste and hormones."),
  STATEMENT_PAIR, "A",
  "Functions of proteins",
  "NCERT: proteins carry out many functions; some transport nutrients across the cell membrane, some fight "
  "infectious organisms, some are hormones and some are enzymes. In the table of proteins, receptors are listed "
  "for sensory reception (smell, taste, hormone, etc.). Both statements are true.",
  ["Transport across membranes → I true", "Receptor → sensory reception → II true"],
  R_BIO("proteins"), seconds=25)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "Although many amino acids exist, the amino acids occurring in proteins are only of:",
  ["Ten types", "Twenty types", "Twenty-two types", "Sixty-four types"], "B",
  "Amino acids in proteins",
  "NCERT: based on the nature of the R group there are many amino acids; however, those occurring in proteins are "
  "only of twenty types. A protein is therefore a heteropolymer of these twenty kinds of amino acids.",
  ["Amino acids in proteins → 20 types"],
  R_BIO("how to analyse chemical composition?: amino acids"),
  why_others_wrong="Ten and twenty-two are not the NCERT number; sixty-four is the number of codons, not amino "
                   "acids.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Intermediate", "numerical",
  "As a rule of thumb, the rate of a physical or chemical process doubles for every 10 °C rise in temperature (and "
  "decreases by half for every 10 °C fall). A non-enzymatic reaction proceeds at a rate R at 20 °C. Assuming the "
  "rule holds over this range, its rate at 50 °C will be about:",
  ["3R", "6R", "8R", "2.5R"], "C",
  "Effect of temperature on reaction rate",
  "NCERT: the rate of a physical or chemical process doubles or decreases by half for every 10 °C change in either "
  "direction. From 20 °C to 50 °C there are three 10 °C steps, and the rate doubles at each step.",
  ["Rise = 50 − 20 = 30 °C = 3 steps of 10 °C", "Rate = R × 2 × 2 × 2 = 2³R = 8R"],
  R_BIO("enzymes: chemical reactions"),
  shortcut="Rate factor = 2^(ΔT/10) = 2³ = 8.",
  why_others_wrong="3R counts the steps instead of doubling; 6R adds a doubling per step (2 × 3); 2.5R simply "
                   "divides the two temperatures.",
  seconds=50, verified_by=RECOMPUTED)

Z(BIO, "Enzymes: properties and action", "Intermediate", "direct",
  "In skeletal muscle under anaerobic conditions the pathway from glucose ends in lactic acid, and in yeast during "
  "fermentation it leads to ethanol. According to NCERT, glucose is converted into pyruvic acid through:",
  ["A single enzyme-catalysed reaction", "Ten different enzyme-catalysed metabolic reactions",
   "Two non-enzymatic steps", "About twenty reactions catalysed by ribozymes"], "B",
  "Metabolic pathways",
  "NCERT: glucose → 2 pyruvic acid is a metabolic pathway in which glucose becomes pyruvic acid through ten "
  "different enzyme-catalysed metabolic reactions. In skeletal muscle under anaerobic conditions lactic acid is "
  "formed; under normal aerobic conditions pyruvic acid is formed; in yeast during fermentation the same pathway "
  "leads to ethanol.",
  ["Glucose → pyruvic acid: ten enzyme-catalysed reactions", "Muscle (anaerobic) → lactic acid; yeast → ethanol"],
  R_BIO("enzymes: how do enzymes bring about such high rates of chemical conversions?"),
  why_others_wrong="The pathway is neither a single reaction nor non-enzymatic, and NCERT does not attribute it to "
                   "ribozymes.",
  seconds=35)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Paper made from plant pulp and cotton fibre is made of starch.", "Plant cell walls are made of cellulose."),
  ASSERTION_REASON, "D",
  "Cellulose",
  "NCERT: plant cell walls are made of cellulose, and paper made from plant pulp and cotton fibre is cellulosic. "
  "Starch is the energy store of plant tissues, not the material of paper or cotton. A is false; R is true.",
  ["A: paper and cotton are cellulosic, not starch → false", "R: plant cell walls are cellulose → true"],
  R_BIO("polysaccharides"),
  why_others_wrong="A and B accept a false assertion; C calls the true reason false.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("The rate of a physical or chemical process refers to the amount of product formed per unit time.",
     "Rate can also be called velocity if the direction is specified."),
  STATEMENT_PAIR, "A",
  "Rate of a reaction",
  "NCERT: rate of a physical or chemical process refers to the amount of product formed per unit time, expressed "
  "as rate = δP/δt. Rate can also be called velocity if the direction is specified. Both statements are true.",
  ["Rate = product formed per unit time → I true", "Velocity = rate with direction → II true"],
  R_BIO("enzymes: chemical reactions"), seconds=25)

_o = ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only", "(a), (b) and (c) only"]
ms_check("abc", _o, "D")
Z(BIO, "Carbohydrates and lipids", "Intermediate", "multi_statement",
  ms("Which of the following statements about lipids are correct?",
     ["Lipids are generally water insoluble.",
      "The R group of a fatty acid could be a methyl, an ethyl or a higher number of –CH₂ groups (1 carbon to 19 "
      "carbons).",
      "Some tissues, especially the neural tissues, have lipids with more complex structures.",
      "Glycerol is a fatty acid.",
      "Lecithin is a lipid that does not contain phosphorus."]),
  _o, "D",
  "Lipids",
  "Lipids are generally water insoluble. A fatty acid has a carboxyl group attached to an R group, which could be "
  "a methyl, ethyl or higher number of –CH₂ groups (1 to 19 carbons). Glycerol is trihydroxy propane, not a fatty "
  "acid (it has no carboxyl group). Lecithin is a phospholipid, so it contains phosphorus. Neural tissues have "
  "lipids with more complex structures.",
  ["(a) True", "(b) True", "(c) True", "(d) False: glycerol is trihydroxy propane",
   "(e) False: lecithin is a phospholipid"],
  R_BIO("how to analyse chemical composition?: lipids"),
  why_others_wrong="A includes (d); B and C include (e) or (d) and leave out true statements.",
  seconds=50)

Z(BIO, "Enzymes: properties and action", "Intermediate", "direct",
  "Metal ions act as co-factors for a number of enzymes. They work by:",
  ["Remaining tightly bound to the apoenzyme as organic prosthetic groups",
   "Associating with the apoenzyme only transiently, as organic co-enzymes do",
   "Forming coordination bonds with side chains at the active site and, at the same time, one or more coordination "
   "bonds with the substrate",
   "Supplying the vitamin component of the co-enzyme"], "C",
  "Co-factors: metal ions",
  "NCERT: co-factors are of three kinds: prosthetic groups (organic, tightly bound), co-enzymes (organic, "
  "transient association, often containing vitamins) and metal ions. Metal ions form coordination bonds with side "
  "chains at the active site and at the same time form one or more coordination bonds with the substrate.",
  ["Prosthetic group → organic, tightly bound", "Co-enzyme → organic, transient", "Metal ion → coordination bonds "
   "with active-site side chains and with substrate"],
  R_BIO("enzymes: co-factors"),
  why_others_wrong="A describes prosthetic groups and B co-enzymes, both organic; vitamins are components of "
                   "co-enzymes, not of metal ions.",
  seconds=35)

Z(BIO, "Proteins and amino acids", "Intermediate", "direct",
  "At which level of protein structure is the long protein chain folded upon itself like a hollow woollen ball, "
  "giving a three-dimensional view of the protein?",
  ["Primary", "Tertiary", "Secondary", "Quaternary"], "B",
  "Levels of protein structure",
  "NCERT: the primary structure is the amino acid sequence; in the secondary structure the chain is folded as a "
  "helix; the long protein chain is further folded upon itself like a hollow woollen ball, giving the tertiary "
  "structure (a 3-D view). The quaternary structure is the arrangement of more than one polypeptide (subunits).",
  ["Hollow woollen ball, 3-D view → tertiary structure"],
  R_BIO("structure of proteins"),
  why_others_wrong="Primary is only the sequence; secondary is the helix; quaternary involves subunits.",
  seconds=25)

Z(BIO, "Carbohydrates and lipids", "Advanced", "numerical",
  "In lipids, fatty acids are found esterified with glycerol as monoglycerides, diglycerides or triglycerides. A "
  "sample contains 3 molecules of a monoglyceride, 4 molecules of a diglyceride and 2 molecules of a triglyceride. "
  "How many fatty acid residues in all are esterified with glycerol in this sample?",
  ["17", "9", "27", "26"], "A",
  "Glycerides",
  "A monoglyceride has one fatty acid esterified with glycerol, a diglyceride two and a triglyceride three. Add the "
  "fatty acid residues of each kind of molecule.",
  ["Monoglycerides: 3 × 1 = 3", "Diglycerides: 4 × 2 = 8", "Triglycerides: 2 × 3 = 6", "Total = 3 + 8 + 6 = 17"],
  R_BIO("how to analyse chemical composition?: lipids"),
  why_others_wrong="9 counts molecules (or glycerol units); 27 treats every molecule as a triglyceride; 26 adds "
                   "the 9 glycerol units to the fatty acids.",
  seconds=50, verified_by=RECOMPUTED)

_o = ["(a), (b), (c) and (d) only", "(a), (c), (d) and (e) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
ms_check("acde", _o, "B")
Z(BIO, "Proteins and amino acids", "Advanced", "multi_statement",
  ms("Which of the following statements about the chemical analysis of a living tissue are correct?",
     ["The tissue is ground in trichloroacetic acid using a mortar and pestle to obtain a thick slurry.",
      "The filtrate obtained after straining the slurry through cheesecloth is the acid-insoluble fraction.",
      "The chemicals in the acid-soluble pool have molecular weights ranging from 18 to around 800 daltons.",
      "The acid-soluble pool represents roughly the cytoplasmic composition.",
      "Inorganic compounds like sulphate and phosphate are also seen in the acid-soluble fraction."]),
  _o, "B",
  "Analysis of chemical composition",
  "A living tissue is ground in trichloroacetic acid (Cl₃CCOOH) to a slurry and strained through cheesecloth. The "
  "filtrate is the acid-soluble pool and the retentate is the acid-insoluble fraction. Acid-soluble chemicals have "
  "molecular weights of about 18–800 Da; the pool represents roughly the cytoplasmic composition, and inorganic "
  "compounds such as sulphate and phosphate are seen in it.",
  ["(a) True", "(b) False: filtrate = acid-soluble pool; retentate = acid-insoluble", "(c) True", "(d) True",
   "(e) True"],
  R_BIO("how to analyse chemical composition?; biomacromolecules"),
  why_others_wrong="A and C include the false statement (b); D leaves out the true statement (c).",
  seconds=60)

Z(BIO, "Enzymes: properties and action", "Advanced", "assertion_reason",
  ar("The activity of an enzyme can be affected by changes in temperature and pH.",
     "Such changes in conditions can alter the tertiary structure of the enzyme protein."),
  ASSERTION_REASON, "A",
  "Factors affecting enzyme activity",
  "NCERT: the activity of an enzyme can be affected by a change in the conditions which can alter the tertiary "
  "structure of the protein; these include temperature and pH. Since the active site lies in the tertiary "
  "structure, altering that structure changes activity. R explains A.",
  ["A: temperature and pH affect enzyme activity → true", "R: they can alter the tertiary structure → true",
   "Activity depends on the tertiary structure → R explains A"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="B denies the link NCERT states; C and D call a true statement false.",
  seconds=40)

Z(BIO, "Enzymes: properties and action", "Advanced", "statement_pair",
  sp("The formation of an enzyme–substrate (ES) complex is obligatory for catalysis, and this complex formation is "
     "a transient phenomenon.",
     "In an exothermic reaction, the substrate does not have to pass through a higher-energy transition state "
     "because the product is at a lower energy level than the substrate."),
  STATEMENT_PAIR, "C",
  "ES complex and transition state",
  "NCERT: the substrate must diffuse to the active site, so ES complex formation is obligatory, and it is "
  "transient (Statement I true). Whether the reaction is exothermic or endothermic, the substrate has to go "
  "through a much higher energy state, the transition state; the energy difference is the activation energy, "
  "which enzymes bring down (Statement II false).",
  ["ES complex: obligatory and transient → I true", "Exothermic reactions also pass a transition state → II false"],
  R_BIO("enzymes: nature of enzyme action"), seconds=40)

Z(BIO, "Enzymes: properties and action", "Advanced", "direct",
  "A competitive inhibitor closely resembles the substrate in its molecular structure and shuts off enzyme "
  "activity. According to NCERT, competitive inhibitors are often used in:",
  ["Raising the optimum temperature of enzymes", "Preserving enzymes in a temporarily inactive state",
   "Converting apoenzymes into co-enzymes", "The control of bacterial pathogens"], "D",
  "Uses of competitive inhibitors",
  "When the binding of a chemical shuts off enzyme activity, the process is called inhibition. NCERT states that "
  "competitive inhibitors are often used in the control of bacterial pathogens.",
  ["Inhibitor resembling substrate → competitive inhibitor", "Use → control of bacterial pathogens"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="Low temperature, not an inhibitor, keeps enzymes temporarily inactive; inhibitors do not shift "
                   "the optimum or convert apoenzymes into co-enzymes.",
  seconds=30)

Z(BIO, "Proteins and amino acids", "Advanced", "statement_pair",
  sp("Glutamic acid is an acidic amino acid, and valine is a neutral amino acid.",
     "Tyrosine, phenylalanine and tryptophan are basic amino acids."),
  STATEMENT_PAIR, "C",
  "Classes of amino acids",
  "NCERT: based on the number of amino and carboxyl groups there are acidic (e.g. glutamic acid), basic (e.g. "
  "lysine) and neutral (e.g. valine) amino acids. Tyrosine, phenylalanine and tryptophan are aromatic amino "
  "acids, not basic ones. Statement I is true; Statement II is false.",
  ["Glutamic acid acidic, valine neutral → I true", "Tyrosine, phenylalanine, tryptophan → aromatic → II false"],
  R_BIO("how to analyse chemical composition?: amino acids"), seconds=35)

# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Respiratory system", "Basic", "direct",
  "In humans, the trachea, the primary, secondary and tertiary bronchi, and the initial bronchioles are supported "
  "by:",
  ["Incomplete cartilaginous rings", "Complete bony rings", "Complete cartilaginous rings",
   "Elastic fibres alone, without any cartilage"], "A",
  "Human respiratory tract",
  "NCERT: the tracheae, primary, secondary and tertiary bronchi, and initial bronchioles are supported by "
  "incomplete cartilaginous rings.",
  ["Trachea to initial bronchioles → incomplete cartilaginous rings"],
  R_BRE("human respiratory system"),
  why_others_wrong="The rings are cartilaginous, not bony, and they are incomplete, not complete.",
  seconds=20)

Z(BRE, "Respiratory system", "Basic", "direct",
  "The lungs lie in the thoracic chamber. This chamber is formed:",
  ["Dorsally by the sternum, ventrally by the vertebral column, laterally by the ribs and on the lower side by the "
   "diaphragm",
   "Dorsally by the vertebral column, ventrally by the sternum, laterally by the diaphragm and on the lower side by "
   "the ribs",
   "Dorsally by the vertebral column, ventrally by the sternum, laterally by the ribs and on the lower side by the "
   "dome-shaped diaphragm",
   "Dorsally by the ribs, ventrally by the diaphragm, laterally by the sternum and on the lower side by the "
   "vertebral column"], "C",
  "Thoracic chamber",
  "NCERT: the thoracic chamber is formed dorsally by the vertebral column, ventrally by the sternum, laterally by "
  "the ribs and on the lower side by the dome-shaped diaphragm.",
  ["Dorsal → vertebral column", "Ventral → sternum", "Lateral → ribs", "Floor → dome-shaped diaphragm"],
  R_BRE("human respiratory system"),
  why_others_wrong="A swaps the dorsal and ventral boundaries; B swaps the lateral and lower boundaries; D jumbles "
                   "all four.",
  seconds=30)

Z(BRE, "Respiratory volumes", "Basic", "direct",
  "The volume of air involved in breathing movements can be estimated, for the clinical assessment of pulmonary "
  "functions, by using a:",
  ["Sphygmomanometer", "Spirometer", "Electrocardiograph", "Dialysing unit"], "B",
  "Measuring respiratory volumes",
  "NCERT: the volume of air involved in breathing movements can be estimated by using a spirometer, which helps in "
  "the clinical assessment of pulmonary functions.",
  ["Spirometer → respiratory volumes and capacities"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="A sphygmomanometer measures blood pressure, an electrocardiograph records the ECG and a "
                   "dialysing unit is used in haemodialysis.",
  seconds=20)

Z(BRE, "Respiratory system", "Basic", "statement_pair",
  sp("Each terminal bronchiole gives rise to a number of very thin, irregular-walled and vascularised bag-like "
     "structures called alveoli.",
     "The branching network of bronchi, bronchioles and alveoli comprises the lungs."),
  STATEMENT_PAIR, "A",
  "Alveoli and lungs",
  "NCERT: each terminal bronchiole gives rise to a number of very thin, irregular-walled and vascularised bag-like "
  "structures called alveoli. The branching network of bronchi, bronchioles and alveoli comprises the lungs. Both "
  "statements are true.",
  ["Terminal bronchiole → alveoli → I true", "Bronchi + bronchioles + alveoli = lungs → II true"],
  R_BRE("human respiratory system"), seconds=25)

Z(BRE, "Exchange and transport of gases", "Intermediate", "direct",
  "Under normal physiological conditions, every 100 mL of deoxygenated blood delivers approximately how much CO₂ "
  "to the alveoli?",
  ["5 mL", "20 mL", "45 mL", "4 mL"], "D",
  "Transport of carbon dioxide",
  "NCERT: every 100 mL of deoxygenated blood delivers approximately 4 mL of CO₂ to the alveoli. (The corresponding "
  "figure for oxygen is about 5 mL of O₂ delivered to the tissues by every 100 mL of oxygenated blood.)",
  ["CO₂ to alveoli → about 4 mL per 100 mL deoxygenated blood"],
  R_BRE("transport of carbon dioxide"),
  why_others_wrong="5 mL is the O₂ delivered to tissues per 100 mL of oxygenated blood; 45 mm Hg is the pCO₂ of "
                   "deoxygenated blood (a pressure, not a volume); 20 mL is not an NCERT value.",
  seconds=25)

Z(BRE, "Mechanism of breathing", "Intermediate", "assertion_reason",
  ar("Any change in the volume of the thoracic cavity is reflected in the lung (pulmonary) cavity.",
     "The lungs are situated in the thoracic chamber, which is anatomically an air-tight chamber."),
  ASSERTION_REASON, "A",
  "Air-tight thoracic chamber",
  "NCERT: the lungs are situated in the thoracic chamber, which is anatomically an air-tight chamber. Such an "
  "arrangement is essential for breathing, as we cannot directly alter the pulmonary volume: any change in the "
  "volume of the thoracic cavity is reflected in the lung cavity. The air-tight arrangement is why the change is "
  "passed on, so R explains A.",
  ["A: thoracic volume change reflected in lung cavity → true", "R: air-tight thoracic chamber → true",
   "Air-tightness transmits the change → R explains A"],
  R_BRE("human respiratory system; mechanism of breathing"),
  why_others_wrong="B denies the explanation NCERT gives; C and D call a true statement false.",
  seconds=35)

Z(BRE, "Mechanism of breathing", "Intermediate", "match_list",
  ml(("term", "description"), ["Breathing (pulmonary ventilation)", "Cellular respiration", "Partial pressure",
                               "Expiration"],
     ["Pressure contributed by an individual gas in a mixture of gases",
      "Utilisation of O₂ by the cells for catabolic reactions and resultant release of CO₂",
      "Release of the alveolar air out of the body",
      "Drawing in atmospheric air and releasing CO₂-rich alveolar air"]),
  match_options(M("IV", "II", "I", "III"),
                [M("IV", "I", "II", "III"), M("III", "II", "I", "IV"), M("IV", "II", "III", "I")], at="B"),
  "B",
  "Steps of respiration",
  "NCERT lists the steps of respiration as breathing or pulmonary ventilation (atmospheric air drawn in and "
  "CO₂-rich alveolar air released out), diffusion across the alveolar membrane, transport by blood, diffusion "
  "between blood and tissues, and utilisation of O₂ by cells for catabolic reactions with release of CO₂ "
  "(cellular respiration). Breathing has two stages: inspiration and expiration (alveolar air released out). The "
  "pressure contributed by an individual gas in a mixture is its partial pressure.",
  ["Breathing → IV", "Cellular respiration → II", "Partial pressure → I", "Expiration → III"],
  R_BRE("respiration: steps; mechanism of breathing; exchange of gases"),
  why_others_wrong="The other codes swap cellular respiration with partial pressure, breathing with expiration, or "
                   "partial pressure with expiration.",
  seconds=45)

_o = ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (d) only", "(a), (c) and (e) only"]
ms_check("abd", _o, "C")
Z(BRE, "Respiratory system", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human respiratory system are correct?",
     ["Apart from transporting atmospheric air to the alveoli, the conducting part clears it of foreign particles, "
      "humidifies it and brings it to body temperature.",
      "The outer pleural membrane is in close contact with the thoracic lining, whereas the inner pleural membrane "
      "is in contact with the lung surface.",
      "The larynx is the common passage for food and air.",
      "The trachea is a straight tube extending up to the mid-thoracic cavity.",
      "The external nostrils open out below the lower lip."]),
  _o, "C",
  "Organisation of the respiratory system",
  "The conducting part transports air to the alveoli and also clears, humidifies and warms it. The outer pleural "
  "membrane lies against the thoracic lining and the inner one against the lung surface. A portion of the pharynx "
  "(not the larynx) is the common passage for food and air; the larynx is the sound box. The trachea is a straight "
  "tube extending up to the mid-thoracic cavity. The external nostrils open out above the upper lips.",
  ["(a) True", "(b) True", "(c) False: the pharynx is the common passage", "(d) True",
   "(e) False: nostrils open above the upper lips"],
  R_BRE("human respiratory system"),
  why_others_wrong="A includes (c); B and D include (e) and leave out true statements.",
  seconds=55)

Z(BRE, "Mechanism of breathing", "Intermediate", "statement_pair",
  sp("Additional muscles in the abdomen have the ability to increase the strength of inspiration and expiration.",
     "On average, a healthy human breathes 30–40 times per minute."),
  STATEMENT_PAIR, "C",
  "Mechanism of breathing",
  "NCERT: with additional muscles in the abdomen, we can increase the strength of inspiration and expiration "
  "(Statement I true). On average, a healthy human breathes 12–16 times per minute (Statement II false).",
  ["Abdominal muscles strengthen breathing → I true", "Normal rate is 12–16 per minute → II false"],
  R_BRE("mechanism of breathing"), seconds=25)

Z(BRE, "Respiratory volumes", "Advanced", "match_list",
  ml(("respiratory volume", "average value"),
     ["Tidal volume", "Inspiratory reserve volume", "Expiratory reserve volume", "Residual volume"],
     ["1100–1200 mL", "1000–1100 mL", "2500–3000 mL", "About 500 mL"]),
  match_options(M("IV", "III", "II", "I"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("IV", "II", "III", "I")], at="B"),
  "B",
  "Respiratory volumes",
  "NCERT values: tidal volume about 500 mL; inspiratory reserve volume 2500–3000 mL; expiratory reserve volume "
  "1000–1100 mL; residual volume 1100–1200 mL. The ERV and RV ranges are close: the residual volume is the "
  "slightly larger one.",
  ["TV → ~500 mL (IV)", "IRV → 2500–3000 mL (III)", "ERV → 1000–1100 mL (II)", "RV → 1100–1200 mL (I)"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="IRV is by far the largest volume; of the two ~1 L volumes, RV is the larger.",
  why_others_wrong="The first wrong code swaps ERV and RV; the others swap TV with IRV, or IRV with ERV.",
  seconds=45)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "Which statement about the oxygen dissociation curve is correct?",
  ["It is obtained by plotting pCO₂ against the percentage saturation of haemoglobin with CO₂",
   "It is a straight line, showing that O₂ binding rises evenly with pO₂",
   "It is obtained by plotting pO₂ against the pH of blood",
   "It is a sigmoid curve of the percentage saturation of haemoglobin with O₂ against pO₂, useful in studying the "
   "effect of factors like pCO₂ and H⁺ concentration on the binding of O₂ with haemoglobin"], "D",
  "Oxygen dissociation curve",
  "NCERT: a sigmoid curve is obtained when the percentage saturation of haemoglobin with O₂ is plotted against "
  "pO₂. This oxygen dissociation curve is highly useful in studying the effect of factors like pCO₂ and H⁺ "
  "concentration on the binding of O₂ with haemoglobin.",
  ["Axes: pO₂ (x) vs % saturation of Hb with O₂ (y)", "Shape: sigmoid", "Use: effect of pCO₂, H⁺, etc."],
  R_BRE("transport of oxygen"),
  why_others_wrong="The curve concerns O₂, not CO₂ or pH, and it is sigmoid, not a straight line.",
  seconds=40)

Z(BRE, "Exchange and transport of gases", "Advanced", "assertion_reason",
  ar("The pO₂ in body tissues is higher than that in oxygenated blood.",
     "The pCO₂ in body tissues is about 45 mm Hg."),
  ASSERTION_REASON, "D",
  "Partial pressures in the tissues",
  "NCERT's table of partial pressures gives, for tissues, pO₂ 40 mm Hg and pCO₂ 45 mm Hg; for oxygenated blood, "
  "pO₂ 95 mm Hg and pCO₂ 40 mm Hg. Tissue pO₂ (40) is lower than that of oxygenated blood (95), which is why O₂ "
  "diffuses from blood into tissues. A is false; R is true.",
  ["Tissue pO₂ 40 < oxygenated blood pO₂ 95 → A false", "Tissue pCO₂ 45 mm Hg → R true"],
  R_BRE("exchange of gases: partial pressures"),
  why_others_wrong="A and B accept a false assertion; C calls the true reason false.",
  seconds=35)

_o = ["(a), (b), (c) and (d) only", "(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"]
ms_check("abce", _o, "B")
Z(BRE, "Exchange and transport of gases", "Advanced", "multi_statement",
  ms("Which of the following statements about the exchange and transport of gases are correct?",
     ["Alveoli are the primary sites of exchange of gases.",
      "Exchange of gases also occurs between blood and tissues.",
      "O₂ and CO₂ are exchanged at these sites by simple diffusion, mainly based on the pressure or concentration "
      "gradient.",
      "The binding of oxygen with haemoglobin is primarily related to temperature.",
      "Haemoglobin is a red-coloured, iron-containing pigment present in the RBCs."]),
  _o, "B",
  "Exchange and transport of gases",
  "Alveoli are the primary sites of gas exchange; exchange also occurs between blood and tissues, by simple "
  "diffusion based mainly on pressure or concentration gradients. Haemoglobin is a red, iron-containing pigment "
  "in RBCs. Binding of O₂ with haemoglobin is primarily related to the partial pressure of O₂; pCO₂, H⁺ "
  "concentration and temperature are other factors that can interfere with it.",
  ["(a) True", "(b) True", "(c) True", "(d) False: binding is primarily related to pO₂", "(e) True"],
  R_BRE("exchange of gases; transport of oxygen"),
  why_others_wrong="A, C and D include the false statement (d); C and D also leave out true statements.",
  seconds=50)

# ================================================================ Body Fluids and Circulation (B5 I7 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "Leucocytes are of two main categories, granulocytes and agranulocytes. Which of the following are "
  "agranulocytes?",
  ["Neutrophils and eosinophils", "Basophils and neutrophils", "Lymphocytes and monocytes",
   "Eosinophils and basophils"], "C",
  "Classification of leucocytes",
  "NCERT: WBCs are of two main categories: granulocytes (neutrophils, eosinophils and basophils) and agranulocytes "
  "(lymphocytes and monocytes).",
  ["Granulocytes → neutrophils, eosinophils, basophils", "Agranulocytes → lymphocytes, monocytes"],
  R_BFC("blood: formed elements"),
  why_others_wrong="Neutrophils, eosinophils and basophils are all granulocytes.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "Plasma is a straw-coloured, viscous fluid. Water constitutes about what proportion of plasma?",
  ["55 per cent", "90–92 per cent", "6–8 per cent", "45 per cent"], "B",
  "Composition of plasma",
  "NCERT: plasma constitutes nearly 55 per cent of the blood. 90–92 per cent of plasma is water and proteins "
  "contribute 6–8 per cent of it. Formed elements make up nearly 45 per cent of the blood.",
  ["Water → 90–92 % of plasma", "Proteins → 6–8 % of plasma"],
  R_BFC("blood: plasma"),
  why_others_wrong="55 % is the share of plasma in blood, 45 % that of formed elements, and 6–8 % that of proteins "
                   "in plasma.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "numerical",
  "The Rh antigen is observed on the surface of the RBCs of nearly 80 per cent of humans. In a group of 650 "
  "people, about how many would be expected to be Rh negative?",
  ["520", "65", "325", "130"], "D",
  "Rh grouping",
  "Individuals with the Rh antigen are Rh positive (nearly 80 %); those without it are Rh negative (about 20 %).",
  ["Rh negative ≈ 100 − 80 = 20 %", "20 % of 650 = 0.2 × 650 = 130"],
  R_BFC("blood groups: Rh grouping"),
  why_others_wrong="520 is the expected number of Rh-positive people; 65 takes 10 %; 325 takes half the group.",
  seconds=30, verified_by=RECOMPUTED)

Z(BFC, "Human heart", "Basic", "direct",
  "The opening between the right atrium and the right ventricle is guarded by the:",
  ["Mitral valve", "Tricuspid valve", "Semilunar valve", "Bicuspid valve"], "B",
  "Valves of the heart",
  "NCERT: the opening between the right atrium and the right ventricle is guarded by a valve formed of three "
  "muscular flaps or cusps, the tricuspid valve; the bicuspid or mitral valve guards the opening between the left "
  "atrium and the left ventricle. Semilunar valves guard the openings of the ventricles into the pulmonary artery "
  "and the aorta.",
  ["Right AV opening → tricuspid", "Left AV opening → bicuspid (mitral)", "Ventricles to arteries → semilunar"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="The mitral and bicuspid valve (the same valve) guards the left side; semilunar valves guard "
                   "the arterial openings.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Group O blood can be donated to persons with any other ABO blood group, so group O individuals are called "
     "universal donors.",
     "Persons with the AB group can accept blood from persons with AB as well as the other groups, so they are "
     "called universal recipients."),
  STATEMENT_PAIR, "A",
  "Universal donors and recipients",
  "From NCERT's table of ABO groups: group O blood can be donated to persons of any other group (universal donors), "
  "and AB persons can accept blood from AB as well as the other groups (universal recipients). Both statements "
  "are true.",
  ["O → universal donor → I true", "AB → universal recipient → II true"],
  R_BFC("blood groups: ABO grouping"), seconds=25)

Z(BFC, "Double circulation and regulation", "Intermediate", "direct",
  "A special neural centre that can moderate cardiac function through the autonomic neural system is located in "
  "the:",
  ["Medulla oblongata", "Cerebellum", "Cerebral cortex", "Corpus callosum"], "A",
  "Regulation of cardiac activity",
  "NCERT: normal activities of the heart are regulated intrinsically (myogenic), but a special neural centre in "
  "the medulla oblongata can moderate cardiac function through the autonomic neural system.",
  ["Cardiac moderating centre → medulla oblongata", "Acts through the ANS"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="The cerebellum, cerebral cortex and corpus callosum are not the cardiac regulating centre.",
  seconds=20)

Z(BFC, "Double circulation and regulation", "Intermediate", "assertion_reason",
  ar("A closed circulatory system is considered more advantageous than an open circulatory system.",
     "In a closed circulatory system, the flow of fluid can be more precisely regulated."),
  ASSERTION_REASON, "A",
  "Open and closed circulation",
  "NCERT: the closed circulatory system is considered to be more advantageous as the flow of fluid can be more "
  "precisely regulated. R is the stated reason for A.",
  ["A: closed system more advantageous → true", "R: flow more precisely regulated → true",
   "NCERT links them with 'as' → R explains A"],
  R_BFC("circulatory pathways"),
  why_others_wrong="B denies the explanation NCERT gives; C and D call a true statement false.",
  seconds=30)

Z(BFC, "Human heart", "Intermediate", "match_list",
  ml(("part of the nodal tissue", "location or course"),
     ["Sino-atrial node", "Atrio-ventricular node", "Atrio-ventricular bundle", "Purkinje fibres"],
     ["Minute fibres spread throughout the ventricular musculature of the respective sides",
      "Right upper corner of the right atrium",
      "Passes through the atrio-ventricular septa and emerges on the top of the inter-ventricular septum",
      "Lower left corner of the right atrium, close to the atrio-ventricular septum"]),
  match_options(M("II", "IV", "III", "I"),
                [M("IV", "II", "III", "I"), M("II", "IV", "I", "III"), M("II", "III", "IV", "I")], at="D"),
  "D",
  "Nodal tissue of the heart",
  "The SAN lies in the right upper corner of the right atrium and the AVN in the lower left corner of the right "
  "atrium close to the AV septum. The AV bundle continues from the AVN, passes through the AV septa, emerges on "
  "top of the inter-ventricular septum and divides into right and left bundles, which give rise to minute fibres "
  "throughout the ventricular musculature: the Purkinje fibres.",
  ["SAN → II", "AVN → IV", "AV bundle → III", "Purkinje fibres → I"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="The other codes swap the SAN with the AVN, the AV bundle with the Purkinje fibres, or the AVN "
                   "with the AV bundle.",
  seconds=45)

_o = ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (d) only", "(a), (b), (c) and (e) only"]
ms_check("abce", _o, "D")
Z(BFC, "Coagulation and lymph", "Intermediate", "multi_statement",
  ms("Which of the following statements about the coagulation of blood are correct?",
     ["A clot is formed mainly of a network of threads called fibrins, in which dead and damaged formed elements "
      "of blood are trapped.",
      "Thrombokinase is formed by a series of linked enzymic reactions (a cascade process) involving a number of "
      "factors present in the plasma in an inactive state.",
      "Certain factors released by the tissues at the site of injury can also initiate coagulation.",
      "The clotting factors are present in the plasma in an active form at all times.",
      "Fibrinogens are plasma proteins needed for the clotting or coagulation of blood."]),
  _o, "D",
  "Coagulation of blood",
  "A clot (coagulum) is mainly a network of fibrin threads trapping dead and damaged formed elements. Fibrins are "
  "formed from fibrinogens by thrombin; thrombin forms from prothrombin with the help of thrombokinase, which is "
  "formed by a cascade of linked enzymic reactions involving factors present in plasma in an inactive state. "
  "Factors released by tissues at the site of injury can also initiate coagulation.",
  ["(a) True", "(b) True", "(c) True", "(d) False: the factors are present in an inactive state", "(e) True"],
  R_BFC("coagulation of blood; blood: plasma"),
  why_others_wrong="A, B and C include the false statement (d); B and C also leave out true statements.",
  seconds=55)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "direct",
  "To obtain a standard ECG, a patient is connected to the machine with three electrical leads attached to:",
  ["Each ankle and the right wrist", "Multiple points on the chest only", "Both wrists and the right ankle",
   "Each wrist and the left ankle"], "D",
  "Recording an ECG",
  "NCERT: to obtain a standard ECG, a patient is connected to the machine with three electrical leads (one to each "
  "wrist and to the left ankle) that continuously monitor the heart activity. For a detailed evaluation, multiple "
  "leads are attached to the chest region.",
  ["Standard ECG → one lead on each wrist + one on the left ankle", "Detailed evaluation → multiple chest leads"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="Chest leads are used for a detailed evaluation, not the standard ECG; the ankle lead goes on "
                   "the left ankle, with one lead on each wrist.",
  seconds=25)

Z(BFC, "Double circulation and regulation", "Intermediate", "statement_pair",
  sp("The pulmonary veins carry oxygenated blood from the lungs into the left atrium.",
     "In systemic circulation, deoxygenated blood from the tissues is collected by venules, veins and the vena cava "
     "and emptied into the left atrium."),
  STATEMENT_PAIR, "C",
  "Pulmonary and systemic circulation",
  "NCERT: oxygenated blood from the lungs is carried by the pulmonary veins into the left atrium (Statement I "
  "true). Deoxygenated blood from the tissues is collected by venules, veins and the vena cava and emptied into "
  "the right atrium (Statement II false).",
  ["Pulmonary veins → left atrium → I true", "Vena cava → right atrium, not left → II false"],
  R_BFC("double circulation"), seconds=30)

Z(BFC, "Blood and blood groups", "Intermediate", "direct",
  "Erythroblastosis foetalis in a second Rh-positive foetus of an Rh-negative mother can be avoided by:",
  ["Giving Rh-positive blood to the mother during her first pregnancy",
   "Administering anti-Rh antibodies to the mother immediately after the delivery of the first child",
   "Administering Rh antigens to the foetus before the second delivery",
   "Transfusing group O blood to the mother before the first delivery"], "B",
  "Prevention of erythroblastosis foetalis",
  "NCERT: the situation (erythroblastosis foetalis) can be avoided by administering anti-Rh antibodies to the "
  "mother immediately after the delivery of the first child.",
  ["Prevention → anti-Rh antibodies to the mother", "Timing → immediately after the first delivery"],
  R_BFC("blood groups: Rh grouping"),
  why_others_wrong="Exposure to Rh-positive blood or antigens would sensitise rather than protect; ABO group O "
                   "blood has nothing to do with Rh incompatibility.",
  seconds=30)

Z(BFC, "Double circulation and regulation", "Advanced", "assertion_reason",
  ar("In fishes, the heart pumps out deoxygenated blood, which is oxygenated by the gills and supplied to the body "
     "parts.",
     "In fishes, oxygenated and deoxygenated blood are received by separate left and right atria and are pumped "
     "out by separate ventricles."),
  ASSERTION_REASON, "C",
  "Circulation in fishes",
  "NCERT: fishes have a two-chambered heart with an atrium and a ventricle. The heart pumps out deoxygenated blood, "
  "which is oxygenated by the gills and supplied to the body parts, from where deoxygenated blood returns to the "
  "heart. Separate left and right atria and ventricles occur in birds and mammals (double circulation), not in "
  "fishes. A is true; R is false.",
  ["A: fish heart pumps deoxygenated blood to the gills → true",
   "R: fishes have one atrium and one ventricle → false"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A and B accept the false reason; D calls the true assertion false.",
  seconds=35)

_o = ["(a), (b), (c) and (e) only", "(a), (c) and (d) only", "(b), (c), (d) and (e) only", "(a), (b) and (d) only"]
ms_check("abce", _o, "A")
Z(BFC, "Circulatory disorders", "Advanced", "multi_statement",
  ms("Which of the following statements about disorders of the circulatory system are correct?",
     ["In a normal blood pressure of 120/80 mm Hg, 120 mm Hg is the systolic (pumping) pressure and 80 mm Hg is the "
      "diastolic (resting) pressure.",
      "High blood pressure leads to heart diseases and also affects vital organs like the brain and kidney.",
      "Coronary artery disease is often referred to as atherosclerosis.",
      "Angina occurs only in elderly men.",
      "A heart attack is when the heart muscle is suddenly damaged by an inadequate blood supply."]),
  _o, "A",
  "Circulatory disorders",
  "Normal blood pressure is 120/80 mm Hg: 120 is the systolic (pumping) and 80 the diastolic (resting) pressure. "
  "High blood pressure leads to heart diseases and also affects the brain and kidney. CAD is often referred to as "
  "atherosclerosis. Angina can occur in men and women of any age but is more common among the middle-aged and "
  "elderly. A heart attack is sudden damage to heart muscle by an inadequate blood supply.",
  ["(a) True", "(b) True", "(c) True", "(d) False: any age, men and women; more common in middle-aged and elderly",
   "(e) True"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="B, C and D include the false statement (d); B and D also leave out true statements.",
  seconds=55)

Z(BFC, "Double circulation and regulation", "Advanced", "direct",
  "Which of the following correctly pairs an animal group with its pattern of circulation?",
  ["Molluscs: closed circulation, so that blood flow can be precisely regulated",
   "Arthropods: open circulation, in which blood pumped by the heart passes through large vessels into open spaces "
   "or body cavities called sinuses",
   "Annelids: open circulation, with blood flowing into sinuses",
   "Fishes: double circulation, with separate pulmonary and systemic pathways"], "B",
  "Circulatory pathways",
  "NCERT: the open circulatory system is present in arthropods and molluscs; blood pumped by the heart passes "
  "through large vessels into open spaces or body cavities called sinuses. Annelids and chordates have a closed "
  "circulatory system. Double circulation, with separate pulmonary and systemic pathways, is seen in birds and "
  "mammals; fishes have a two-chambered heart.",
  ["Open (sinuses) → arthropods, molluscs", "Closed → annelids, chordates", "Double circulation → birds, mammals"],
  R_BFC("circulatory pathways"),
  why_others_wrong="Molluscs have an open system; annelids a closed one; fishes do not have double circulation.",
  seconds=45)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "statement_pair",
  sp("During the cardiac cycle, atrial systole coincides with ventricular systole.",
     "The contraction of the ventricles starts shortly after the Q wave of the ECG and marks the beginning of "
     "systole."),
  STATEMENT_PAIR, "D",
  "Timing of the cardiac cycle and ECG",
  "NCERT: during ventricular systole the atria undergo relaxation (diastole), so atrial diastole, not atrial "
  "systole, coincides with ventricular systole (Statement I false). The QRS complex represents depolarisation of "
  "the ventricles, which initiates ventricular contraction; the contraction starts shortly after Q and marks the "
  "beginning of systole (Statement II true).",
  ["Atrial diastole coincides with ventricular systole → I false",
   "Ventricular contraction begins shortly after Q → II true"],
  R_BFC("cardiac cycle; electrocardiograph (ECG)"), seconds=35)

_o = ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only", "(a), (d) and (e) only"]
ms_check("abde", _o, "C")
Z(BFC, "Human heart", "Advanced", "multi_statement",
  ms("Which of the following statements about the human heart are correct?",
     ["The heart is mesodermally derived and is situated in the thoracic cavity between the two lungs, slightly "
      "tilted to the left.",
      "It has the size of a clenched fist.",
      "The inter-atrial septum is a thick-walled muscular partition.",
      "The atrium and the ventricle of the same side are separated by a thick fibrous tissue called the "
      "atrio-ventricular septum.",
      "The valves allow the flow of blood in only one direction."]),
  _o, "C",
  "Structure of the human heart",
  "NCERT: the heart, a mesodermally derived organ, lies in the thoracic cavity between the two lungs, slightly "
  "tilted to the left, and is the size of a clenched fist. A thin muscular wall, the inter-atrial septum, "
  "separates the atria, while a thick-walled inter-ventricular septum separates the ventricles. A thick fibrous "
  "atrio-ventricular septum separates the atrium and ventricle of the same side. Valves allow flow in only one "
  "direction.",
  ["(a) True", "(b) True", "(c) False: the inter-atrial septum is thin", "(d) True", "(e) True"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="A and B include the false statement (c); D leaves out the true statement (b).",
  seconds=55)

# ================================================================ Excretory Products and their Elimination (B5 I6 A5)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Mammals, many terrestrial amphibians and marine fishes mainly excrete their nitrogenous wastes as:",
  ["Ammonia", "Urea", "Uric acid", "Ammonium ions through the gills"], "B",
  "Ureotelism",
  "NCERT: mammals, many terrestrial amphibians and marine fishes mainly excrete urea and are called ureotelic "
  "animals. Many bony fishes, aquatic amphibians and aquatic insects are ammonotelic, and reptiles, birds, land "
  "snails and insects are uricotelic.",
  ["Mammals, terrestrial amphibians, marine fishes → urea (ureotelic)"],
  R_EXC("introduction: modes of excretion"),
  why_others_wrong="Ammonia (including ammonium ions through gills) is excreted by ammonotelic animals such as "
                   "many bony fishes; uric acid by reptiles, birds, land snails and insects.",
  seconds=20)

Z(EXC, "Disorders and dialysis", "Basic", "direct",
  "The presence of glucose (glycosuria) and ketone bodies (ketonuria) in urine is indicative of:",
  ["Diabetes insipidus", "Uremia", "Diabetes mellitus", "Renal calculi"], "C",
  "Abnormal constituents of urine",
  "NCERT: analysis of urine helps in the clinical diagnosis of many metabolic disorders as well as malfunctioning "
  "of the kidney. The presence of glucose (glycosuria) and ketone bodies (ketonuria) in urine is indicative of "
  "diabetes mellitus.",
  ["Glycosuria + ketonuria → diabetes mellitus"],
  R_EXC("micturition: composition of urine"),
  why_others_wrong="Uremia is urea in the blood, renal calculi are kidney stones, and NCERT does not link "
                   "glycosuria and ketonuria to diabetes insipidus.",
  seconds=20)

Z(EXC, "Disorders and dialysis", "Basic", "direct",
  "Kidney transplantation is the ultimate method in the correction of acute renal failure. A functioning kidney is "
  "taken from a donor, preferably a close relative, in order to:",
  ["Increase the glomerular filtration rate", "Avoid the use of anticoagulants",
   "Minimise the chances of rejection by the immune system of the host", "Prevent the formation of renal calculi"],
  "C",
  "Kidney transplantation",
  "NCERT: in kidney transplantation a functioning kidney is used from a donor, preferably a close relative, to "
  "minimise its chances of rejection by the immune system of the host. Modern clinical procedures have increased "
  "the success rate of such a complicated technique.",
  ["Close relative as donor → less chance of immune rejection"],
  R_EXC("disorders of the excretory system"),
  why_others_wrong="The choice of a related donor is about immune rejection, not GFR, anticoagulants or stones.",
  seconds=20)

Z(EXC, "Nephron structure", "Basic", "statement_pair",
  sp("Each kidney of an adult human measures about 10–12 cm in length, 5–7 cm in width and 2–3 cm in thickness.",
     "The kidneys are reddish-brown, bean-shaped structures."),
  STATEMENT_PAIR, "A",
  "Human kidney",
  "NCERT: kidneys are reddish-brown, bean-shaped structures. Each kidney of an adult human measures 10–12 cm in "
  "length, 5–7 cm in width and 2–3 cm in thickness. Both statements are true.",
  ["Size 10–12 × 5–7 × 2–3 cm → I true", "Reddish-brown, bean-shaped → II true"],
  R_EXC("human excretory system"), seconds=25)

Z(EXC, "Nephron structure", "Basic", "direct",
  "The glomerulus along with Bowman's capsule is called the:",
  ["Juxtaglomerular apparatus", "Medullary pyramid", "Renal pelvis", "Malpighian body or renal corpuscle"], "D",
  "Parts of a nephron",
  "NCERT: each nephron has a glomerulus and a renal tubule. The tubule begins with the double-walled, cup-like "
  "Bowman's capsule enclosing the glomerulus. The glomerulus along with Bowman's capsule is called the Malpighian "
  "body or renal corpuscle.",
  ["Glomerulus + Bowman's capsule → Malpighian body (renal corpuscle)"],
  R_EXC("human excretory system: nephron"),
  why_others_wrong="The JGA is formed by the DCT and afferent arteriole; medullary pyramids and the renal pelvis "
                   "are regions of the kidney, not parts of a nephron.",
  seconds=20)

Z(EXC, "Regulation of kidney function", "Intermediate", "direct",
  "The juxtaglomerular apparatus (JGA) is a special sensitive region formed by cellular modifications in the:",
  ["Proximal convoluted tubule and the efferent arteriole",
   "Distal convoluted tubule and the afferent arteriole, at the location of their contact",
   "Collecting duct and the vasa recta", "Henle's loop and the peritubular capillaries"], "B",
  "Juxtaglomerular apparatus",
  "NCERT: the JGA is a special sensitive region formed by cellular modifications in the distal convoluted tubule "
  "and the afferent arteriole at the location of their contact. A fall in GFR can activate the JG cells to "
  "release renin, which helps bring GFR back to normal.",
  ["JGA = modified DCT + afferent arteriole at their contact"],
  R_EXC("urine formation: regulation of GFR"),
  why_others_wrong="The JGA involves the DCT and the afferent arteriole, not the PCT, efferent arteriole, collecting "
                   "duct, vasa recta or Henle's loop.",
  seconds=25)

Z(EXC, "Modes of excretion", "Intermediate", "assertion_reason",
  ar("Ammonia is generally excreted by diffusion across body surfaces or through gill surfaces (in fish) as "
     "ammonium ions.",
     "Ammonia is readily soluble."),
  ASSERTION_REASON, "A",
  "Ammonotelism",
  "NCERT: ammonia, as it is readily soluble, is generally excreted by diffusion across body surfaces or through "
  "gill surfaces (in fish) as ammonium ions; kidneys do not play any significant role in its removal. High "
  "solubility is why simple diffusion works, so R explains A.",
  ["A: ammonia leaves by diffusion across body or gill surfaces → true", "R: ammonia is readily soluble → true",
   "NCERT links them with 'as it is readily soluble' → R explains A"],
  R_EXC("introduction: modes of excretion"),
  why_others_wrong="B denies the link NCERT states; C and D call a true statement false.",
  seconds=30)

Z(EXC, "Urine formation", "Intermediate", "match_list",
  ml(("term", "meaning"), ["Uremia", "Micturition reflex", "Ultrafiltration", "Renal calculi"],
     ["Stone or insoluble mass of crystallised salts (oxalates, etc.) formed within the kidney",
      "Accumulation of urea in the blood due to malfunctioning of the kidneys",
      "Neural mechanisms causing the release of urine",
      "Glomerular filtration in which almost all the constituents of plasma except proteins pass into Bowman's "
      "capsule"]),
  match_options(M("II", "III", "IV", "I"),
                [M("III", "II", "IV", "I"), M("II", "IV", "III", "I"), M("II", "III", "I", "IV")], at="C"),
  "C",
  "Terms related to excretion",
  "Accumulation of urea in blood is uremia. The neural mechanisms causing release of urine form the micturition "
  "reflex. Almost all plasma constituents except proteins pass into Bowman's capsule, so glomerular filtration is "
  "considered a process of ultrafiltration. Renal calculi are stones of crystallised salts (oxalates, etc.) "
  "formed within the kidney.",
  ["Uremia → II", "Micturition reflex → III", "Ultrafiltration → IV", "Renal calculi → I"],
  R_EXC("urine formation; micturition; disorders of the excretory system"),
  why_others_wrong="The other codes swap uremia with the micturition reflex, the reflex with ultrafiltration, or "
                   "ultrafiltration with renal calculi.",
  seconds=40)

_o = ["(a), (b) and (e) only", "(a), (b), (c) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (d) only"]
ms_check("abcd", _o, "B")
Z(EXC, "Regulation of kidney function", "Intermediate", "multi_statement",
  ms("Which of the following statements about the regulation of kidney function are correct?",
     ["Osmoreceptors in the body are activated by changes in blood volume, body fluid volume and ionic "
      "concentration.",
      "Antidiuretic hormone (ADH) is also called vasopressin.",
      "ADH facilitates water reabsorption from the latter parts of the tubule, thereby preventing diuresis.",
      "An increase in body fluid volume can switch off the osmoreceptors and suppress ADH release.",
      "A decrease in body fluid volume suppresses ADH release."]),
  _o, "B",
  "Hormonal feedback in kidney function",
  "Osmoreceptors respond to changes in blood volume, body fluid volume and ionic concentration. Excessive loss of "
  "fluid activates them, and the hypothalamus releases ADH (vasopressin) from the neurohypophysis. ADH increases "
  "water reabsorption from the latter parts of the tubule, preventing diuresis. An increase in body fluid volume "
  "switches off the osmoreceptors and suppresses ADH release, completing the feedback. A fall in fluid volume "
  "stimulates, not suppresses, ADH release.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: fluid loss stimulates ADH release"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A and C include the false statement (e); D leaves out the true statement (b).",
  seconds=50)

Z(EXC, "Modes of excretion", "Intermediate", "statement_pair",
  sp("In ureotelic animals, ammonia produced by metabolism is converted into urea in the liver and released into "
     "the blood.",
     "Some amount of urea may be retained in the kidney matrix of some animals to maintain a desired osmolarity."),
  STATEMENT_PAIR, "A",
  "Formation and retention of urea",
  "NCERT: in ureotelic animals, ammonia produced by metabolism is converted into urea in the liver and released "
  "into the blood, which is filtered and excreted by the kidneys. Some amount of urea may be retained in the kidney "
  "matrix of some animals to maintain a desired osmolarity. Both statements are true.",
  ["Urea made in the liver → I true", "Urea retained in kidney matrix for osmolarity → II true"],
  R_EXC("introduction: modes of excretion"), seconds=30)

Z(EXC, "Regulation of kidney function", "Intermediate", "direct",
  "The signal that finally leads to micturition is initiated by:",
  ["The release of ADH from the neurohypophysis", "Contraction of the urethral sphincter",
   "The release of renin by the JG cells",
   "Stretching of the urinary bladder as it fills with urine, which makes stretch receptors on its walls send "
   "signals to the CNS"], "D",
  "Micturition",
  "NCERT: the signal is initiated by the stretching of the urinary bladder as it gets filled with urine. In "
  "response, the stretch receptors on the walls of the bladder send signals to the CNS, which passes on motor "
  "messages to contract the smooth muscles of the bladder and relax the urethral sphincter, releasing urine.",
  ["Bladder fills → stretch receptors → signals to CNS", "CNS → bladder muscles contract, urethral sphincter relaxes"],
  R_EXC("micturition"),
  why_others_wrong="ADH and renin regulate water and GFR, not micturition; the urethral sphincter relaxes, not "
                   "contracts, when urine is released.",
  seconds=30)

Z(EXC, "Modes of excretion", "Advanced", "assertion_reason",
  ar("Reptiles, birds, land snails and insects excrete nitrogenous wastes as uric acid in the form of a pellet or "
     "paste.",
     "Uric acid, being the least toxic, can be removed with a minimum loss of water."),
  ASSERTION_REASON, "A",
  "Uricotelism",
  "NCERT: ammonia is the most toxic and needs a large amount of water for elimination, whereas uric acid, being "
  "the least toxic, can be removed with a minimum loss of water. Uricotelic animals (reptiles, birds, land snails, "
  "insects) therefore excrete uric acid as a pellet or paste with a minimum loss of water. R explains A.",
  ["A: uric acid as pellet or paste → true", "R: least toxic, removable with minimum water → true",
   "Low toxicity allows near-dry excretion → R explains A"],
  R_EXC("introduction: modes of excretion"),
  why_others_wrong="B denies the link; C and D call a true statement false.",
  seconds=35)

_o = ["(a), (b), (c) and (d)", "(b), (c) and (d) only", "(a) and (c) only", "(a), (b) and (d) only"]
ms_check("abd", _o, "D")
Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("Which of the following statements about tubular reabsorption and secretion are correct?",
     ["Amino acids and Na⁺ in the filtrate are reabsorbed actively.",
      "Nitrogenous wastes are absorbed by passive transport.",
      "Water is reabsorbed actively in the initial segments of the nephron.",
      "Secretion of H⁺, K⁺ and ammonia into the filtrate helps in the maintenance of the ionic and acid-base "
      "balance of body fluids."]),
  _o, "D",
  "Reabsorption and secretion",
  "NCERT: the tubular epithelial cells reabsorb by active or passive mechanisms. Substances like glucose, amino "
  "acids and Na⁺ are reabsorbed actively, whereas nitrogenous wastes are absorbed by passive transport. "
  "Reabsorption of water also occurs passively in the initial segments of the nephron. Tubular cells secrete H⁺, "
  "K⁺ and ammonia into the filtrate, which helps maintain the ionic and acid-base balance of body fluids.",
  ["(a) True", "(b) True", "(c) False: water is reabsorbed passively", "(d) True"],
  R_EXC("urine formation: reabsorption and secretion"),
  why_others_wrong="A, B and C include the false statement (c); B and C also leave out true statements.",
  seconds=50)

Z(EXC, "Urine formation", "Advanced", "direct",
  "Which of the following is a function of the distal convoluted tubule (DCT)?",
  ["Reabsorption of nearly all the essential nutrients and 70–80 per cent of electrolytes and water",
   "Reabsorption of HCO₃⁻ and selective secretion of H⁺, K⁺ and NH₃ to maintain the pH and sodium-potassium "
   "balance in blood",
   "Being permeable to water but almost impermeable to electrolytes",
   "Allowing small amounts of urea to pass into the medullary interstitium"], "B",
  "Function of the DCT",
  "NCERT: in the DCT, conditional reabsorption of Na⁺ and water takes place. The DCT is also capable of "
  "reabsorption of HCO₃⁻ and selective secretion of hydrogen and potassium ions and NH₃ to maintain the pH and "
  "sodium-potassium balance in blood.",
  ["DCT → conditional Na⁺/water reabsorption", "DCT → HCO₃⁻ reabsorption; H⁺, K⁺, NH₃ secretion"],
  R_EXC("function of the tubules"),
  why_others_wrong="A describes the PCT, C the descending limb of Henle's loop and D the collecting duct.",
  seconds=35)

Z(EXC, "Disorders and dialysis", "Advanced", "statement_pair",
  sp("In haemodialysis, the dialysing unit contains a coiled cellophane tube surrounded by dialysing fluid, and "
     "nitrogenous wastes move out of the blood across the porous membrane according to the concentration "
     "gradient.",
     "In the majority of nephrons, the loop of Henle is very long and runs deep into the medulla."),
  STATEMENT_PAIR, "C",
  "Haemodialysis and types of nephrons",
  "NCERT: the dialysing unit contains a coiled cellophane tube surrounded by dialysing fluid; its porous membrane "
  "allows passage of molecules based on concentration gradient, and since nitrogenous wastes are absent in the "
  "fluid they move out of the blood (Statement I true). In the majority of nephrons the loop of Henle is too short "
  "and extends only very little into the medulla (cortical nephrons); only some, the juxtamedullary nephrons, have "
  "very long loops (Statement II false).",
  ["Cellophane tube, concentration gradient → I true", "Majority are cortical nephrons with short loops → II false"],
  R_EXC("disorders of the excretory system; human excretory system: nephron"), seconds=40)

Z(EXC, "Urine formation", "Advanced", "direct",
  "Which statement about the collecting duct of the human nephron is correct?",
  ["It is impermeable to water and plays no part in concentrating urine",
   "It lies only in the cortex of the kidney",
   "It receives the filtrate directly from the proximal convoluted tubule",
   "It extends from the cortex of the kidney to the inner parts of the medulla, and large amounts of water can be "
   "reabsorbed from it to produce concentrated urine"], "D",
  "Collecting duct",
  "NCERT: the DCTs of many nephrons open into a straight tube called the collecting duct. This long duct extends "
  "from the cortex of the kidney to the inner parts of the medulla. Large amounts of water could be reabsorbed from "
  "this region to produce a concentrated urine.",
  ["DCT → collecting duct", "Cortex to inner medulla", "Large water reabsorption → concentrated urine"],
  R_EXC("human excretory system: nephron; function of the tubules"),
  why_others_wrong="The duct reabsorbs much water, runs into the inner medulla, and receives filtrate from the DCT "
                   "rather than the PCT.",
  seconds=35)

# ================================================================ Locomotion and Movement (B5 I6 A5)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Skeletal system", "Basic", "direct",
  "Bone has a very hard matrix because of calcium salts. The matrix of cartilage is slightly pliable because of:",
  ["Calcium salts", "Chondroitin salts", "Collagen fibres alone", "Sodium chloride"], "B",
  "Bone and cartilage",
  "NCERT: bone has a very hard matrix due to calcium salts, and cartilage has a slightly pliable matrix due to "
  "chondroitin salts.",
  ["Bone → calcium salts → very hard", "Cartilage → chondroitin salts → slightly pliable"],
  R_LOC("skeletal system"),
  why_others_wrong="Calcium salts make bone hard; collagen alone or sodium chloride is not what NCERT gives.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "direct",
  "The human skeletal system consists of a framework of bones and a few cartilages. The total number of bones is:",
  ["80", "126", "206", "213"], "C",
  "Number of bones",
  "NCERT: the skeletal system consists of a framework of bones and a few cartilages; it is made up of 206 bones, "
  "grouped into the axial skeleton (80 bones) and the appendicular skeleton (126 bones).",
  ["Total = 206 = 80 (axial) + 126 (appendicular)"],
  R_LOC("skeletal system"),
  why_others_wrong="80 is the axial and 126 the appendicular skeleton alone; 213 is not an NCERT figure.",
  seconds=20)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "A motor neuron along with the muscle fibres connected to it constitutes a:",
  ["Motor unit", "Motor-end plate", "Sarcomere", "Myofibril"], "A",
  "Motor unit",
  "NCERT: muscle contraction is initiated by a signal sent by the CNS via a motor neuron. A motor neuron along with "
  "the muscle fibres connected to it constitutes a motor unit. The junction between a motor neuron and the "
  "sarcolemma is the neuromuscular junction or motor-end plate.",
  ["Motor neuron + its muscle fibres → motor unit", "Their junction → motor-end plate"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="The motor-end plate is only the junction; a sarcomere is a contractile unit of a myofibril; a "
                   "myofibril is a fibril within a muscle fibre.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "statement_pair",
  sp("Each clavicle is a long slender bone with two curvatures and is commonly called the collar bone.",
     "The two halves of the pelvic girdle meet dorsally to form the pubic symphysis, which contains hyaline "
     "cartilage."),
  STATEMENT_PAIR, "C",
  "Pectoral and pelvic girdles",
  "NCERT: each clavicle is a long slender bone with two curvatures, commonly called the collar bone (Statement I "
  "true). The two halves of the pelvic girdle meet ventrally to form the pubic symphysis containing fibrous "
  "cartilage (Statement II false on two counts).",
  ["Clavicle: two curvatures, collar bone → I true", "Pubic symphysis: ventral, fibrous cartilage → II false"],
  R_LOC("appendicular skeleton"), seconds=30)

Z(LOC, "Muscular and skeletal disorders", "Basic", "direct",
  "Osteoporosis is an age-related disorder with decreased bone mass and increased chances of fractures. A common "
  "cause of it is:",
  ["Accumulation of uric acid crystals in the joints", "A low level of Ca²⁺ in body fluids",
   "Autoimmune damage at the neuromuscular junction", "Decreased levels of estrogen"], "D",
  "Osteoporosis",
  "NCERT: osteoporosis is an age-related disorder characterised by decreased bone mass and increased chances of "
  "fractures. Decreased levels of estrogen is a common cause.",
  ["Osteoporosis → common cause: decreased estrogen"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="Uric acid crystals cause gout; low Ca²⁺ causes tetany; autoimmune damage at the NMJ is "
                   "myasthenia gravis.",
  seconds=20)

Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "How many bones in all are present in the wrists, palms and digits of both hands of a human being?",
  ["27", "52", "60", "54"], "D",
  "Bones of the fore limb",
  "Each fore limb has the humerus, radius, ulna, 8 carpals (wrist bones), 5 metacarpals (palm bones) and 14 "
  "phalanges (digits).",
  ["One hand: 8 + 5 + 14 = 27", "Both hands: 2 × 27 = 54"],
  R_LOC("appendicular skeleton"),
  why_others_wrong="27 is one hand only; 52 uses the 7 tarsals of the foot instead of the 8 carpals; 60 counts all "
                   "30 bones of each fore limb.",
  seconds=40, verified_by=RECOMPUTED)

Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "How many individual ribs in a human are connected ventrally to the sternum, either directly or by joining the "
  "seventh rib with the help of hyaline cartilage?",
  ["14", "20", "10", "24"], "B",
  "Ribs",
  "There are 12 pairs of ribs. The first seven pairs (true ribs) are connected ventrally to the sternum with the "
  "help of hyaline cartilage. The 8th, 9th and 10th pairs (vertebrochondral or false ribs) do not articulate "
  "directly with the sternum but join the seventh rib with the help of hyaline cartilage. The 11th and 12th pairs "
  "(floating ribs) are not connected ventrally.",
  ["True ribs: 7 pairs = 14", "Vertebrochondral ribs: 3 pairs = 6", "Total = 14 + 6 = 20"],
  R_LOC("axial skeleton: ribs"),
  shortcut="All 24 ribs minus the 4 floating ribs = 20.",
  why_others_wrong="14 counts only the true ribs; 10 counts pairs instead of ribs; 24 includes the floating ribs.",
  seconds=45, verified_by=RECOMPUTED)

Z(LOC, "Muscle contraction", "Intermediate", "direct",
  "In a resting sarcomere, the central part of the thick filaments that is not overlapped by the thin filaments is "
  "called the:",
  ["I-band", "Z-line", "H-zone", "M-line"], "C",
  "Structure of a sarcomere",
  "NCERT: in the resting state, the edges of thin filaments on either side of the thick filaments partially "
  "overlap the free ends of the thick filaments, leaving the central part of the thick filaments. This central "
  "part of the thick filament, not overlapped by thin filaments, is called the H-zone.",
  ["Central part of A-band not overlapped by actin → H-zone"],
  R_LOC("skeletal muscle"),
  why_others_wrong="The I-band contains thin filaments; the Z-line bisects the I-band; the M-line is the fibrous "
                   "membrane holding the thick filaments together in the middle of the A-band.",
  seconds=25)

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("Repeated activation of muscles can lead to fatigue.",
     "Repeated activation leads to the accumulation of lactic acid in muscles due to the anaerobic breakdown of "
     "glycogen in them."),
  ASSERTION_REASON, "A",
  "Muscle fatigue",
  "NCERT: repeated activation of the muscles can lead to the accumulation of lactic acid due to anaerobic "
  "breakdown of glycogen in them, causing fatigue. R gives the cause of A.",
  ["A: repeated activation → fatigue → true", "R: lactic acid from anaerobic glycogen breakdown → true",
   "Lactic acid accumulation causes the fatigue → R explains A"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="B denies the causal link; C and D call a true statement false.",
  seconds=30)

Z(LOC, "Muscle contraction", "Intermediate", "match_list",
  ml(("structure", "feature or role"),
     ["Visceral muscles", "Tropomyosin", "Heavy meromyosin (HMM)", "Cilia of the trachea"],
     ["Remove dust particles and some foreign substances inhaled with atmospheric air",
      "Globular head with a short arm that projects outwards from the myosin filament as a cross arm",
      "Protein that runs close to the F-actins throughout their length",
      "Assist in the transportation of food through the digestive tract and gametes through the genital tract"]),
  match_options(M("IV", "III", "II", "I"),
                [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"), M("IV", "III", "I", "II")], at="B"),
  "B",
  "Muscles, contractile proteins and ciliary movement",
  "Visceral (smooth) muscles in the walls of hollow organs assist in moving food through the digestive tract and "
  "gametes through the genital tract. Two filaments of tropomyosin run close to the F-actins throughout their "
  "length. Each meromyosin has a globular head with a short arm (HMM) and a tail (LMM); the HMM projects outwards "
  "as the cross arm. Coordinated movements of tracheal cilia remove dust and foreign particles from inhaled air.",
  ["Visceral muscles → IV", "Tropomyosin → III", "HMM → II", "Tracheal cilia → I"],
  R_LOC("types of movement; muscle; structure of contractile proteins"),
  why_others_wrong="The other codes swap visceral muscle with tropomyosin, tropomyosin with HMM, or HMM with the "
                   "cilia.",
  seconds=45)

Z(LOC, "Types of movement", "Intermediate", "statement_pair",
  sp("All movements are locomotions.",
     "In Paramecium, cilia help in the movement of food through the cytopharynx and in locomotion."),
  STATEMENT_PAIR, "D",
  "Movement and locomotion",
  "NCERT: all locomotions are movements, but all movements are not locomotions (Statement I false). In "
  "Paramecium, cilia help in the movement of food through the cytopharynx and in locomotion (Statement II true).",
  ["All locomotions are movements, not the reverse → I false", "Paramecium cilia: food movement + locomotion → II true"],
  R_LOC("introduction: movement and locomotion"), seconds=25)

Z(LOC, "Skeletal system", "Advanced", "numerical",
  "In the human vertebral column, how many vertebrae lie between the last cervical vertebra and the sacral "
  "vertebra?",
  ["19", "17", "12", "24"], "B",
  "Regions of the vertebral column",
  "The vertebral column of 26 vertebrae is differentiated into cervical (7), thoracic (12), lumbar (5), sacral "
  "(1, fused) and coccygeal (1, fused) regions, from the skull downwards. Between the last cervical and the sacral "
  "vertebra lie the thoracic and lumbar vertebrae.",
  ["Thoracic = 12", "Lumbar = 5", "Between cervical and sacral = 12 + 5 = 17"],
  R_LOC("axial skeleton: vertebral column"),
  why_others_wrong="19 removes only the 7 cervical vertebrae from 26; 12 counts only the thoracic vertebrae; 24 "
                   "removes only the two fused vertebrae.",
  seconds=40, verified_by=RECOMPUTED)

_o = ["(a), (b), (c) and (d)", "(b) and (d) only", "(a), (c) and (d) only", "(a), (b) and (c) only"]
ms_check("abc", _o, "D")
Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("Which of the following statements about the mechanism of muscle contraction are correct?",
     ["Ca²⁺ binds with a subunit of troponin on the actin filaments and thereby removes the masking of the active "
      "sites for myosin.",
      "Muscle contraction is initiated by a signal sent by the CNS via a motor neuron.",
      "The junction between a motor neuron and the sarcolemma of a muscle fibre is called the neuromuscular "
      "junction or motor-end plate.",
      "The reaction time of the muscle fibres is the same in all muscles."]),
  _o, "D",
  "Mechanism of muscle contraction",
  "Contraction is initiated by a CNS signal via a motor neuron; the motor neuron meets the sarcolemma at the "
  "neuromuscular junction (motor-end plate). The rise in Ca²⁺ leads to binding of calcium with a subunit of "
  "troponin, removing the masking of the active sites for myosin. NCERT notes that the reaction time of the fibres "
  "can vary in different muscles.",
  ["(a) True", "(b) True", "(c) True", "(d) False: reaction time can vary in different muscles"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A, B and C include the false statement (d); B and C also leave out true statements.",
  seconds=45)

Z(LOC, "Muscle contraction", "Advanced", "assertion_reason",
  ar("Red muscle fibres can also be called aerobic muscles.",
     "Red muscle fibres contain plenty of mitochondria, which can utilise the large amount of oxygen stored in them "
     "for ATP production."),
  ASSERTION_REASON, "A",
  "Red and white muscle fibres",
  "NCERT: muscles with high myoglobin (a red, oxygen-storing pigment) look reddish and are called red fibres. They "
  "contain plenty of mitochondria which can utilise the large amount of oxygen stored in them for ATP production; "
  "these muscles, therefore, can also be called aerobic muscles. White fibres have little myoglobin, few "
  "mitochondria and much sarcoplasmic reticulum, and depend on anaerobic processes. R explains A.",
  ["A: red fibres = aerobic muscles → true", "R: many mitochondria using stored O₂ for ATP → true",
   "NCERT links them with 'therefore' → R explains A"],
  R_LOC("mechanism of muscle contraction: red and white fibres"),
  why_others_wrong="B denies the link NCERT states; C and D call a true statement false.",
  seconds=35)

Z(LOC, "Skeletal system", "Advanced", "direct",
  "Which statement about the human skull is correct?",
  ["The cranium is made of 14 bones and the facial region of 8 skeletal elements",
   "The skull articulates with the vertebral column through a single occipital condyle",
   "The cranium has 8 bones forming a hard protective outer covering for the brain, the facial region has 14 "
   "skeletal elements, and the skull articulates with the vertebral column by two occipital condyles",
   "The first vertebra, the axis, articulates with the occipital condyles"], "C",
  "Skull",
  "NCERT: the cranium has 8 bones forming the hard protective outer covering of the brain; the facial region is "
  "made of 14 skeletal elements. The skull articulates with the superior region of the vertebral column with the "
  "help of two occipital condyles (dicondylic skull). The first vertebra, the atlas, articulates with the occipital "
  "condyles.",
  ["Cranium 8 + facial 14 = 22", "Two occipital condyles → dicondylic", "Atlas (not axis) meets the condyles"],
  R_LOC("axial skeleton: skull"),
  why_others_wrong="A swaps the cranial and facial counts; B gives one condyle instead of two; D names the axis "
                   "instead of the atlas.",
  seconds=40)

Z(LOC, "Joints", "Advanced", "statement_pair",
  sp("The thoracic vertebrae, ribs and sternum together form the rib cage.",
     "The force generated by the muscles is used to carry out movement through joints, where the joint acts as a "
     "fulcrum."),
  STATEMENT_PAIR, "A",
  "Rib cage and joints",
  "NCERT: the thoracic vertebrae, ribs and sternum together form the rib cage (Statement I true). Joints are "
  "essential for all types of movements involving the bony parts of the body; force generated by the muscles is "
  "used to carry out movement through joints, where the joint acts as a fulcrum (Statement II true).",
  ["Thoracic vertebrae + ribs + sternum = rib cage → I true", "Joint acts as a fulcrum → II true"],
  R_LOC("axial skeleton: ribs; joints"), seconds=35)

# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The major part of the human brain is formed by the:",
  ["Cerebellum", "Cerebrum", "Medulla oblongata", "Thalamus"], "B",
  "Forebrain: cerebrum",
  "NCERT: the forebrain consists of the cerebrum, thalamus and hypothalamus, and the cerebrum forms the major part "
  "of the human brain.",
  ["Cerebrum → major part of the human brain"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="The cerebellum and medulla belong to the hindbrain and the thalamus is a forebrain structure "
                   "that the cerebrum wraps around; none forms the major part.",
  seconds=20)

Z(NEU, "Nerve impulse generation and conduction", "Basic", "direct",
  "The electrical potential difference across the resting plasma membrane of a neuron is called the:",
  ["Action potential", "Depolarisation", "Resting potential", "Nerve impulse"], "C",
  "Resting potential",
  "NCERT: in the resting state, the outer surface of the axonal membrane is positive and the inner surface "
  "negative (polarised). The electrical potential difference across the resting plasma membrane is called the "
  "resting potential.",
  ["Resting membrane potential difference → resting potential"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="The action potential (nerve impulse) is the potential difference at a depolarised site; "
                   "depolarisation is the reversal of polarity, not the resting state.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The midbrain is located between the:",
  ["Cerebrum and the thalamus", "Pons and the medulla oblongata", "Medulla oblongata and the spinal cord",
   "Thalamus/hypothalamus of the forebrain and the pons of the hindbrain"], "D",
  "Midbrain",
  "NCERT: the midbrain is located between the thalamus/hypothalamus of the forebrain and the pons of the "
  "hindbrain. A canal called the cerebral aqueduct passes through it.",
  ["Midbrain: between thalamus/hypothalamus (forebrain) and pons (hindbrain)"],
  R_NEU("central neural system: midbrain"),
  why_others_wrong="The cerebrum and thalamus are both forebrain; the pons and medulla are both hindbrain; the "
                   "medulla continues into the spinal cord.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "statement_pair",
  sp("A deep cleft divides the cerebrum longitudinally into two halves, the left and right cerebral hemispheres.",
     "The layer of cells covering the cerebral hemispheres, the cerebral cortex, is thrown into prominent folds."),
  STATEMENT_PAIR, "A",
  "Cerebrum",
  "NCERT: a deep cleft divides the cerebrum longitudinally into the left and right cerebral hemispheres, which are "
  "connected by the corpus callosum. The layer of cells covering the hemispheres is the cerebral cortex, and it is "
  "thrown into prominent folds. Both statements are true.",
  ["Longitudinal cleft → two hemispheres → I true", "Cortex thrown into prominent folds → II true"],
  R_NEU("central neural system: forebrain"), seconds=25)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("Transmission of an impulse across an electrical synapse is very similar to impulse conduction along a single "
     "axon.",
     "At electrical synapses, the membranes of the pre- and post-synaptic neurons are in very close proximity, and "
     "electrical current can flow directly from one neuron into the other."),
  ASSERTION_REASON, "A",
  "Electrical synapses",
  "NCERT: at electrical synapses, the membranes of pre- and post-synaptic neurons are in very close proximity, and "
  "electrical current can flow directly from one neuron into the other across these synapses. Transmission of an "
  "impulse across them is therefore very similar to conduction along a single axon. R explains A.",
  ["A: similar to conduction along one axon → true", "R: close membranes, direct current flow → true",
   "Direct current flow makes it like axonal conduction → R explains A"],
  R_NEU("transmission of impulses"),
  why_others_wrong="B denies the explanation; C and D call a true statement false.",
  seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "direct",
  "At a chemical synapse, the arrival of an impulse at the axon terminal stimulates:",
  ["The synthesis of neurotransmitters in the post-synaptic membrane",
   "The movement of synaptic vesicles towards the membrane, where they fuse with the plasma membrane and release "
   "neurotransmitters into the synaptic cleft",
   "The fusion of the pre- and post-synaptic neurons, closing the synaptic cleft",
   "The direct flow of electrical current into the post-synaptic neuron without any chemical"], "B",
  "Chemical synapse",
  "NCERT: when an impulse arrives at the axon terminal, it stimulates the movement of the synaptic vesicles "
  "towards the membrane, where they fuse with the plasma membrane and release their neurotransmitters into the "
  "synaptic cleft. These bind to specific receptors on the post-synaptic membrane.",
  ["Impulse at terminal → vesicles move and fuse → neurotransmitters released into cleft"],
  R_NEU("transmission of impulses"),
  why_others_wrong="Neurotransmitters are stored in pre-synaptic vesicles; the cleft is not closed; direct current "
                   "flow describes an electrical synapse.",
  seconds=30)

_o = ["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (d) only", "(a), (c) and (d) only"]
ms_check("abcd", _o, "C")
Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following statements about the functions of the human brain are correct?",
     ["The brain controls the circadian (24-hour) rhythms of our body.",
      "The brain controls the activities of several endocrine glands.",
      "The brain is the site for processing of vision, hearing, speech, memory, intelligence, emotions and "
      "thoughts.",
      "Thermoregulation, hunger and thirst are controlled by the brain.",
      "The brain does not control the functioning of vital involuntary organs such as the lungs, heart and "
      "kidneys."]),
  _o, "C",
  "Functions of the brain",
  "NCERT: the brain is the central information processing organ and acts as the command and control system. It "
  "controls voluntary movements, balance, the functioning of vital involuntary organs (lungs, heart, kidneys), "
  "thermoregulation, hunger and thirst, circadian rhythms, activities of several endocrine glands and human "
  "behaviour, and is the site for processing vision, hearing, speech, memory, intelligence, emotions and thoughts.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: it controls vital involuntary organs"],
  R_NEU("central neural system"),
  why_others_wrong="A and B include the false statement (e); D leaves out the true statement (b).",
  seconds=45)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "statement_pair",
  sp("The rise in stimulus-induced permeability to Na⁺ is long-lived and is not followed by any change in the "
     "permeability to K⁺.",
     "The electrical potential difference across the plasma membrane at a depolarised site is called the action "
     "potential, which is in fact termed a nerve impulse."),
  STATEMENT_PAIR, "D",
  "Action potential",
  "NCERT: the rise in stimulus-induced permeability to Na⁺ is extremely short-lived; it is quickly followed by a "
  "rise in permeability to K⁺, and K⁺ diffuses out to restore the resting potential (Statement I false). The "
  "potential difference at the depolarised site is the action potential, termed a nerve impulse (Statement II "
  "true).",
  ["Na⁺ permeability rise is extremely short-lived, then K⁺ permeability rises → I false",
   "Action potential = nerve impulse → II true"],
  R_NEU("generation and conduction of nerve impulse"), seconds=35)

Z(NEU, "Nervous system divisions", "Intermediate", "direct",
  "The association areas of the cerebral cortex, which are neither clearly sensory nor motor in function, are "
  "responsible for:",
  ["Complex functions like intersensory associations, memory and communication",
   "Controlling respiration, cardiovascular reflexes and gastric secretions",
   "Relaying impulses from the CNS to involuntary organs and smooth muscles",
   "Connecting the two cerebral hemispheres"], "A",
  "Association areas",
  "NCERT: the cerebral cortex contains motor areas, sensory areas and large regions that are neither clearly "
  "sensory nor motor in function. These regions, called the association areas, are responsible for complex "
  "functions like intersensory associations, memory and communication.",
  ["Association areas → intersensory associations, memory, communication"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="B is the medulla oblongata, C the autonomic neural system and D the corpus callosum.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Advanced", "assertion_reason",
  ar("The brain stem forms the connections between the brain and the spinal cord.",
     "The brain stem consists of the cerebrum, thalamus and hypothalamus."),
  ASSERTION_REASON, "C",
  "Brain stem",
  "NCERT: the brain stem, formed by the midbrain, pons and medulla oblongata, "
  "forms the connections between the brain and the spinal cord. The cerebrum, thalamus and "
  "hypothalamus make up the forebrain. A is true; R is false.",
  ["A: brain stem links brain and spinal cord → true",
   "R: cerebrum, thalamus, hypothalamus = forebrain, not brain stem → false"],
  R_NEU("central neural system: hindbrain"),
  why_others_wrong="A and B accept the false reason; D calls the true assertion false.",
  seconds=35)

_o = ["(a), (c) and (e) only", "(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c), (d) and (e)"]
ms_check("abcd", _o, "B")
Z(NEU, "Neuron and nerves", "Advanced", "multi_statement",
  ms("Which of the following statements about neurons and nerve fibres are correct?",
     ["Afferent nerve fibres transmit impulses from tissues and organs to the CNS.",
      "Efferent nerve fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues and "
      "organs.",
      "An unmyelinated nerve fibre is enclosed by a Schwann cell that does not form a myelin sheath around the axon.",
      "The cell body of a neuron contains cytoplasm with typical cell organelles.",
      "The distal end of the axon is unbranched."]),
  _o, "B",
  "Neuron and nerve fibres",
  "The PNS has afferent fibres (tissues/organs → CNS) and efferent fibres (CNS → peripheral tissues/organs). An "
  "unmyelinated fibre is enclosed by a Schwann cell that does not form a myelin sheath. The cell body contains "
  "cytoplasm with typical cell organelles and Nissl's granules. The axon is a long fibre whose distal end is "
  "branched, each branch ending in a synaptic knob.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: the distal end of the axon is branched"],
  R_NEU("human neural system; neuron as structural and functional unit"),
  why_others_wrong="A, C and D include the false statement (e); A and C also leave out true statements.",
  seconds=50)

Z(NEU, "Nervous system divisions", "Advanced", "assertion_reason",
  ar("The neural system provides chemical integration through hormones.",
     "The endocrine system provides chemical integration through hormones."),
  ASSERTION_REASON, "D",
  "Neural and chemical coordination",
  "NCERT: the neural system provides an organised network of point-to-point connections for quick coordination, "
  "while the endocrine system provides chemical integration through hormones. A wrongly assigns hormonal "
  "integration to the neural system, so A is false; R is true.",
  ["Neural system → point-to-point, quick coordination → A false", "Endocrine system → hormones → R true"],
  R_NEU("introduction: neural system"),
  why_others_wrong="A and B accept a false assertion; C calls the true reason false.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "direct",
  "At a site of excitation on an axon, K⁺ diffuses out after the brief rise in Na⁺ permeability and the resting "
  "potential is restored within a fraction of a second. The fibre then:",
  ["Remains depolarised, with its inner surface positive",
   "Becomes permanently impermeable to Na⁺",
   "Becomes once more responsive to further stimulation",
   "Releases neurotransmitters along its entire length"], "C",
  "Recovery after an action potential",
  "NCERT: the rise in Na⁺ permeability is quickly followed by a rise in K⁺ permeability. Within a fraction of a "
  "second, K⁺ diffuses outside the membrane and restores the resting potential at the site of excitation, and the "
  "fibre becomes once more responsive to further stimulation.",
  ["Na⁺ in (brief) → K⁺ out → resting potential restored", "Fibre responsive to further stimulation"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="Restoring the resting potential ends depolarisation; the membrane can again become permeable "
                   "to Na⁺; neurotransmitters are released only at axon terminals.",
  seconds=35)


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
           "notes": "BATCH_003 package ZOO_003_p1: 128 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "facts already tested in BATCH_000-BATCH_002; every numerical answer re-derived by "
                    "tools/batch_003/ZOO_003_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
