"""Writes batches/parts/BATCH_005_ZOO_p1.json: package ZOO_005_p1 of BATCH_005 (Zoology, 129 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_001001 .. NEET_ZOO_001129. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, subtopics, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11
Biology textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion and absorption). Facts
already tested in BATCH_000 to BATCH_004 (see `merge_batch.py stems 005 ZOO_005_p1`) are not tested again.

    python docs/neet-bank/tools/batch_005/ZOO_005_p1.py
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
PACKAGE = "ZOO_005_p1"
BATCH = "BATCH_005"
FIRST_ID, LAST_ID = 1001, 1129
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
# Breathing: FRC = ERV + RV, so ERV = FRC - RV; VC = ERV + TV + IRV, so IRV = VC - ERV - TV.
FRC, RV, VC, TV = 2300, 1200, 4600, 500
ERV5 = FRC - RV
IRV5 = VC - ERV5 - TV
assert (ERV5, IRV5) == (1100, 3000)
assert VC - TV == 4100 and VC - FRC - TV == 1800 and VC - ERV5 == 3500          # forgot ERV; used FRC; gave IC

# Body fluids: 7000 WBC per mm3; lymphocytes 25 %, monocytes 7 % (both agranulocytes).
WBC = 7000
AGRAN = WBC * F(25, 100) + WBC * F(7, 100)
assert AGRAN == 2240
assert WBC * F(25, 100) == 1750 and WBC - AGRAN == 4760 and WBC * F(7, 100) == 490  # lymphocytes only; granulocytes

# Body fluids: 5 L blood, plasma 55 % of blood, water taken as 90 % of plasma.
PLASMA = 5000 * F(55, 100)
PLASMA_WATER = PLASMA * F(90, 100)
assert (PLASMA, PLASMA_WATER) == (2750, 2475)
assert 5000 * F(90, 100) == 4500 and 5000 * F(45, 100) * F(90, 100) == 2025         # water of whole blood; used 45 %

# Excretion: 27 g of urea in 1.5 L of urine per day.
UREA_CONC = F(27) / F(3, 2)
assert UREA_CONC == 18
assert 27 * F(3, 2) == F(81, 2) and F(27, 15) == F(9, 5)                          # multiplied; per 15 L slip

# Excretion: GFR 125 mL/min shared by 2 kidneys x 1 million nephrons; 1 mL = 10^6 nL.
PER_NEPHRON_NL = F(125 * 10 ** 6, 2 * 10 ** 6)
assert PER_NEPHRON_NL == F(125, 2)                                                  # 62.5 nL per minute
assert F(125 * 10 ** 6, 10 ** 6) == 125 and F(125 * 10 ** 6, 2 * 10 ** 7) == F(25, 4)  # one kidney; 10^7 slip

# Locomotion: each foot has 5 metatarsals and 14 phalanges; both feet.
FEET = 2 * (5 + 14)
assert FEET == 38
assert 5 + 14 == 19 and 2 * (7 + 5 + 14) == 52 and 2 * 14 + 5 == 33                 # one foot; tarsals added; slip


# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "In sponges, water enters through minute pores (ostia) in the body wall into a central cavity, the spongocoel. "
  "From the spongocoel, the water goes out through the:",
  ["Osculum", "Hypostome", "Excretory pore", "Cloaca"], "A",
  "Water canal system of sponges",
  "NCERT: sponges have a water transport or canal system. Water enters through minute pores (ostia) in the body "
  "wall into a central cavity, the spongocoel, from where it goes out through the osculum.",
  ["Ostia → spongocoel → osculum"],
  R_AK("phylum Porifera"),
  why_others_wrong="The hypostome bears the mouth of coelenterates; the excretory pore belongs to aschelminths; a "
                   "cloaca is a common chamber found in vertebrates such as amphibians, reptiles and birds.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Among cartilaginous fishes, some possess electric organs while some possess a poison sting. Which of the following "
  "is cited by NCERT as having a poison sting?",
  ["Scoliodon", "Trygon", "Pristis", "Carcharodon"], "B",
  "Examples of Chondrichthyes",
  "NCERT: some cartilaginous fishes have electric organs (e.g. Torpedo) and some possess a poison sting (e.g. "
  "Trygon, the sting ray). Scoliodon is the dog fish, Pristis the saw fish and Carcharodon the great white shark.",
  ["Poison sting → Trygon (sting ray)", "Electric organ → Torpedo"],
  R_AK("class Chondrichthyes"),
  why_others_wrong="Scoliodon (dog fish), Pristis (saw fish) and Carcharodon (great white shark) are cartilaginous "
                   "fishes, but NCERT does not cite them for a poison sting.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Branchiostoma, commonly called Amphioxus or lancelet, is placed in the subphylum:",
  ["Urochordata", "Vertebrata", "Cephalochordata", "Hemichordata"], "C",
  "Subphyla of Chordata",
  "NCERT gives Branchiostoma (Amphioxus or Lancelet) as the example of Cephalochordata, in which the notochord "
  "extends from head to tail. Ascidia, Salpa and Doliolum are urochordates.",
  ["Branchiostoma → Cephalochordata"],
  R_AK("phylum Chordata"),
  why_others_wrong="Urochordates are Ascidia, Salpa and Doliolum; Branchiostoma has no vertebral column, so it is not "
                   "a vertebrate; Hemichordata is now a separate non-chordate phylum (Balanoglossus, Saccoglossus).",
  seconds=20)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Which phylum does NCERT describe as the second largest animal phylum?",
  ["Arthropoda", "Annelida", "Chordata", "Mollusca"], "D",
  "Phylum Mollusca",
  "NCERT opens its description of phylum Mollusca by calling it the second largest animal phylum. Arthropoda is the "
  "largest phylum, containing over two-thirds of all named species.",
  ["Largest phylum → Arthropoda", "Second largest → Mollusca"],
  R_AK("phylum Mollusca"),
  why_others_wrong="Arthropoda is the largest phylum, not the second largest; NCERT does not rank Annelida or "
                   "Chordata in this way.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Respiration by gills, by lungs and through the skin is described by NCERT for members of class:",
  ["Reptilia", "Amphibia", "Aves", "Osteichthyes"], "B",
  "Features of Amphibia",
  "NCERT: in amphibians, respiration is by gills, lungs and through the skin. Their skin is moist and without scales. "
  "Reptiles and birds respire by lungs, and bony fishes respire by gills.",
  ["Amphibia → gills, lungs and skin"],
  R_AK("class Amphibia"),
  why_others_wrong="Reptiles have dry, cornified skin and respire by lungs; birds respire by lungs supplemented by air "
                   "sacs; bony fishes respire by gills.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "match_list",
  ml(("genus", "common name"),
     ["Chameleon", "Vipera", "Bufo", "Macaca"],
     ["Toad", "Tree lizard", "Monkey", "Viper"]),
  match_options(M("II", "IV", "I", "III"),
                [M("IV", "II", "I", "III"), M("II", "IV", "III", "I"), M("III", "IV", "I", "II")], "A"),
  "A",
  "Examples of reptiles, amphibians and mammals",
  "From the NCERT examples: Chameleon is the tree lizard and Vipera the viper (both reptiles); Bufo is the toad (an "
  "amphibian); Macaca is the monkey (a mammal).",
  ["Chameleon → tree lizard (II)", "Vipera → viper (IV)", "Bufo → toad (I)", "Macaca → monkey (III)"],
  R_AK("classes Amphibia, Reptilia and Mammalia (examples)"),
  why_others_wrong="Each wrong code swaps one pair: the chameleon is not a viper, and Bufo is a toad, not a monkey.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "Which of the following features does NCERT describe for parasitic forms of Platyhelminthes such as Taenia?",
  ["Parapodia and nephridia that help in swimming and excretion",
   "Cnidoblasts used for anchorage and capture of prey",
   "Hooks and suckers, and some absorb nutrients from the host directly through their body surface",
   "Comb plates and a well-marked bioluminescence"], "C",
  "Parasitic adaptations of flatworms",
  "NCERT: flatworms are mostly endoparasites. Hooks and suckers are present in the parasitic forms, and some of them "
  "absorb nutrients from the host directly through their body surface.",
  ["Platyhelminthes (parasitic) → hooks and suckers", "Some absorb nutrients directly through the body surface"],
  R_AK("phylum Platyhelminthes"),
  why_others_wrong="Parapodia belong to aquatic annelids such as Nereis; cnidoblasts belong to cnidarians; comb plates "
                   "and bioluminescence are features of ctenophores.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "According to NCERT, the water transport or canal system of sponges helps in:",
  ["Locomotion alone, the sponges being free-swimming",
   "Capture of prey with stinging cells",
   "Osmoregulation by flame cells",
   "Food gathering, respiratory exchange and removal of waste"], "D",
  "Functions of the canal system in Porifera",
  "NCERT: the water transport system of sponges is helpful in food gathering, respiratory exchange and removal of "
  "waste. Sponges are mostly marine, mostly asymmetrical, primitive multicellular animals.",
  ["Canal system → food gathering + respiratory exchange + removal of waste"],
  R_AK("phylum Porifera"),
  why_others_wrong="NCERT does not describe sponges as free-swimming; stinging cells (cnidoblasts) belong to "
                   "cnidarians; flame cells are found in flatworms.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("In sponges, digestion is intracellular.",
     "Sponges have a complete alimentary canal with a separate mouth and anus."),
  ASSERTION_REASON, "C",
  "Digestion in Porifera",
  "NCERT states that digestion in sponges is intracellular, so A is true. Sponges show only the cellular level of "
  "organisation; their cells are loose aggregates and they have a water canal system, not an alimentary canal with "
  "a mouth and an anus. R is false.",
  ["A → true (digestion intracellular)", "R → false (no alimentary canal; cellular level of organisation)"],
  R_AK("phylum Porifera"),
  why_others_wrong="A and B treat R as true; D calls the NCERT statement on intracellular digestion false.",
  seconds=30)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("Subphyla Urochordata and Cephalochordata are often referred to as protochordates and are exclusively marine.",
     "Vertebrates have a ventral muscular heart with two, three or four chambers, and their kidneys serve for "
     "excretion and osmoregulation."),
  STATEMENT_PAIR, "A",
  "Protochordates and vertebrate features",
  "NCERT: Urochordata and Cephalochordata are often referred to as protochordates and are exclusively marine. "
  "Vertebrates have a ventral muscular heart with two, three or four chambers, kidneys for excretion and "
  "osmoregulation, and paired appendages which may be fins or limbs.",
  ["Statement I → true", "Statement II → true"],
  R_AK("phylum Chordata; subphylum Vertebrata"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("phylum", "basis of its name given in NCERT"),
     ["Arthropoda", "Annelida", "Cnidaria", "Echinodermata"],
     ["Spiny body", "Cells containing stinging capsules", "Little ring", "Jointed appendages"]),
  match_options(M("IV", "III", "II", "I"),
                [M("IV", "II", "III", "I"), M("I", "III", "II", "IV"), M("III", "IV", "II", "I")], "B"),
  "B",
  "Meaning of phylum names",
  "NCERT: Arthropoda – arthros, joint; poda, appendages. Annelida – Latin annulus, little ring, because the body "
  "surface is marked into segments or metameres. Cnidaria – from the cnidoblasts or cnidocytes, which contain the "
  "stinging capsules or nematocysts. Echinodermata – spiny bodied, from the endoskeleton of calcareous ossicles.",
  ["Arthropoda → jointed appendages (IV)", "Annelida → little ring (III)", "Cnidaria → stinging capsules (II)",
   "Echinodermata → spiny body (I)"],
  R_AK("phyla Coelenterata, Annelida, Arthropoda and Echinodermata"),
  why_others_wrong="The other codes interchange 'little ring' with 'stinging capsules' or 'jointed appendages', or "
                   "give the spiny body to arthropods.",
  seconds=40)

Z(AK, "Chordate classes", "Intermediate", "multi_statement",
  ms("Which of the following statements are correct?",
     ["In birds, the endoskeleton is fully ossified (bony).",
      "The skin of mammals is unique in possessing hair.",
      "The most unique mammalian characteristic is the presence of mammary glands, by which the young ones are "
      "nourished.",
      "Birds are poikilothermous (cold-blooded) animals.",
      "The skin of reptiles is moist and without scales."]),
  ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only", "(a), (b) and (c) only"], "D",
  "Features of Aves, Mammalia and Reptilia",
  "NCERT: in birds the endoskeleton is fully ossified (bones) and they are warm-blooded (homoiothermous). Mammals "
  "are unique in possessing hair on the skin, and their most unique characteristic is the presence of mammary glands. "
  "Reptiles have dry, cornified skin with epidermal scales or scutes.",
  ["(a) true", "(b) true", "(c) true", "(d) false – birds are homoiothermous",
   "(e) false – reptilian skin is dry and cornified, with scales"],
  R_AK("classes Reptilia, Aves and Mammalia"),
  why_others_wrong="Any option containing (d) or (e) is wrong; B also leaves out the true statement (a).",
  seconds=50)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("Hemichordates show direct development.",
     "In hemichordates, fertilisation is external."),
  ASSERTION_REASON, "D",
  "Reproduction in Hemichordata",
  "NCERT: in hemichordates, sexes are separate, fertilisation is external and development is indirect. A is false "
  "because development is indirect; R is true.",
  ["A → false (development is indirect)", "R → true (fertilisation external)"],
  R_AK("phylum Hemichordata"),
  why_others_wrong="A, B and C all treat the assertion as true, but NCERT states that development in hemichordates "
                   "is indirect.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("In molluscs, the anterior head region has sensory tentacles.",
     "The body of molluscs is segmented, with a distinct head, a muscular foot and a visceral hump."),
  STATEMENT_PAIR, "C",
  "Body plan of Mollusca",
  "NCERT: the body of molluscs is covered by a calcareous shell and is unsegmented, with a distinct head, a muscular "
  "foot and a visceral hump. The anterior head region has sensory tentacles. Statement II wrongly calls the body "
  "segmented.",
  ["Statement I → true", "Statement II → false (body unsegmented)"],
  R_AK("phylum Mollusca"),
  why_others_wrong="A and D accept a segmented molluscan body; B rejects the true NCERT line about sensory tentacles.",
  seconds=30)

Z(AK, "Chordate classes", "Advanced", "direct",
  "An animal has dry, cornified skin with epidermal scales, two pairs of limbs and a tympanum that represents the "
  "ear. It is cold-blooded, fertilisation is internal and development is "
  "direct. To which class does it belong?",
  ["Reptilia", "Amphibia", "Aves", "Mammalia"], "A",
  "Identifying a vertebrate class from combined features",
  "NCERT (Reptilia): the body is covered by dry, cornified skin with epidermal scales or scutes; the tympanum "
  "represents the ear; limbs, when present, are two pairs; they are "
  "poikilotherms; fertilisation is internal and they are oviparous with direct development.",
  ["Dry cornified skin + scales → not Amphibia (moist skin, no scales)",
   "Cold-blooded → not Aves or Mammalia (homoiothermous)",
   "Scales, tympanum as ear, direct development → Reptilia"],
  R_AK("class Reptilia"),
  why_others_wrong="Amphibians have moist skin without scales and indirect development; birds and mammals are "
                   "warm-blooded, and mammals have external ears (pinnae).",
  seconds=50)

Z(AK, "Chordate classes", "Advanced", "match_list",
  ml(("animal", "class"),
     ["Myxine", "Carcharodon", "Hippocampus", "Alligator"],
     ["Osteichthyes", "Cyclostomata", "Reptilia", "Chondrichthyes"]),
  match_options(M("II", "IV", "I", "III"),
                [M("II", "I", "IV", "III"), M("IV", "II", "I", "III"), M("II", "IV", "III", "I")], "C"),
  "C",
  "Placing NCERT examples in their classes",
  "Myxine (hagfish) is a cyclostome; Carcharodon (great white shark) is a cartilaginous fish; Hippocampus (sea "
  "horse) is a marine bony fish despite its unusual shape; Alligator is a reptile.",
  ["Myxine → Cyclostomata (II)", "Carcharodon → Chondrichthyes (IV)", "Hippocampus → Osteichthyes (I)",
   "Alligator → Reptilia (III)"],
  R_AK("classes Cyclostomata, Chondrichthyes, Osteichthyes and Reptilia (examples)"),
  why_others_wrong="A makes the great white shark a bony fish and the sea horse cartilaginous; B makes the hagfish a "
                   "shark; D treats the sea horse as a reptile.",
  seconds=45)

Z(AK, "Basis of classification", "Advanced", "multi_statement",
  ms("Which of the following statements about phylum Chordata are correct?",
     ["A pharynx perforated by gill slits is present in chordates and absent in non-chordates.",
      "Chordates are fundamentally characterised by the presence of a notochord, a dorsal hollow nerve cord and "
      "paired pharyngeal gill slits.",
      "Chordates are bilaterally symmetrical, triploblastic and coelomate, with the organ-system level of "
      "organisation.",
      "In chordates, a post-anal part (tail) is absent.",
      "Chordates lack a closed circulatory system."]),
  ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (b) only", "(a), (b) and (c) only"], "D",
  "Fundamental features of chordates",
  "NCERT: chordates are fundamentally characterised by a notochord, a dorsal hollow nerve cord and paired "
  "pharyngeal gill slits. They are bilaterally symmetrical, triploblastic, coelomate with organ-system level of "
  "organisation, and they possess a post-anal tail and a closed circulatory system. In the comparison table, the "
  "pharynx is perforated by gill slits in chordates but gill slits are absent in non-chordates.",
  ["(a) true", "(b) true", "(c) true", "(d) false – a post-anal tail is present",
   "(e) false – circulation is closed"],
  R_AK("phylum Chordata"),
  why_others_wrong="A includes (d), B includes (e), and C leaves out the true statement (c).",
  seconds=60)

Z(AK, "Non-chordate phyla", "Advanced", "assertion_reason",
  ar("Members of phylum Coelenterata are also called cnidarians.",
     "They possess cnidoblasts or cnidocytes, which contain the stinging capsules or nematocysts."),
  ASSERTION_REASON, "A",
  "Origin of the name Cnidaria",
  "NCERT: the name Cnidaria is derived from the cnidoblasts or cnidocytes (which contain the stinging capsules or "
  "nematocysts) present on the tentacles and the body. So coelenterates are called cnidarians because they possess "
  "cnidoblasts – R gives the very reason for the name in A.",
  ["A → true", "R → true", "Name Cnidaria comes from cnidoblasts → R explains A"],
  R_AK("phylum Coelenterata (Cnidaria)"),
  why_others_wrong="B denies the link that NCERT states directly; C and D call a true statement false.",
  seconds=35)

Z(AK, "Chordate classes", "Advanced", "direct",
  "Which statement correctly describes the life history of cyclostomes as given in NCERT?",
  ["They live in fresh water and migrate to the sea for spawning, after which the adults return to fresh water",
   "They are marine but migrate to fresh water for spawning; after spawning, within a few days, they die, and their "
   "larvae, after metamorphosis, return to the ocean",
   "They are marine and spawn in the sea; their larvae migrate to fresh water and remain there throughout life",
   "They are viviparous, and the young ones are nourished by mammary glands"], "B",
  "Spawning migration in Cyclostomata",
  "NCERT: cyclostomes are marine but migrate for spawning to fresh water. After spawning, within a few days, they "
  "die. Their larvae, after metamorphosis, return to the ocean.",
  ["Adults: sea → fresh water for spawning", "Die within a few days of spawning",
   "Larvae metamorphose and return to the ocean"],
  R_AK("class Cyclostomata"),
  why_others_wrong="A reverses the direction of migration and lets adults survive; C keeps the larvae in fresh water; "
                   "D describes mammals.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "statement_pair",
  sp("Ctenophores, commonly known as sea walnuts or comb jellies, show both extracellular and intracellular "
     "digestion.",
     "In ctenophores, locomotion is brought about by cnidoblasts present on the tentacles and body."),
  STATEMENT_PAIR, "C",
  "Features of Ctenophora",
  "NCERT: in ctenophores (sea walnuts or comb jellies) digestion is both extracellular and intracellular. The body "
  "bears eight external rows of ciliated comb plates, which help in locomotion. Cnidoblasts (stinging cells) are "
  "the feature of cnidarians (coelenterates), not of ctenophores, so Statement II is false.",
  ["Statement I → true", "Statement II → false (comb plates, not cnidoblasts, help in locomotion)"],
  R_AK("phylum Ctenophora"),
  why_others_wrong="A and D give ctenophores the cnidoblasts of cnidarians and miss the comb plates; B rejects the "
                   "true NCERT description of their digestion.",
  seconds=35)

# ================================================================ Structural Organisation in Animals (B5 I6 A5)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Animal tissues", "Basic", "direct",
  "The epithelium of the proximal convoluted tubule (PCT) of the nephron is cuboidal. According to NCERT, its free "
  "surface bears:",
  ["Cilia", "Microvilli", "Flagella", "Several layers of flattened cells"], "B",
  "Cuboidal epithelium of the PCT",
  "NCERT: cuboidal epithelium is commonly found in the ducts of glands and the tubular parts of nephrons, and its "
  "main functions are secretion and absorption. The epithelium of the proximal convoluted tubule (PCT) of the nephron "
  "in the kidney has microvilli.",
  ["PCT epithelium → cuboidal with microvilli"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="Cilia are borne by ciliated epithelium (bronchioles, fallopian tubes); flagella are not described "
                   "for this epithelium; several cell layers describe compound epithelium.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "direct",
  "In connective tissues (other than blood), the cells secrete fibres of the structural proteins collagen or elastin. "
  "According to NCERT, these fibres provide the tissue with:",
  ["The ability to conduct impulses", "The ability to contract on stimulation",
   "Strength, elasticity and flexibility", "A free surface facing a body fluid"], "C",
  "Role of connective tissue fibres",
  "NCERT: in all connective tissues except blood, the cells secrete fibres of structural proteins called collagen or "
  "elastin. The fibres provide strength, elasticity and flexibility to the tissue.",
  ["Collagen/elastin fibres → strength, elasticity and flexibility"],
  R_SOA("animal tissues: connective tissue"),
  why_others_wrong="Conducting impulses is a property of neural tissue, contraction of muscle tissue, and a free "
                   "surface is a feature of epithelial tissue.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "The skin of the frog is smooth and slippery. According to NCERT, this is due to the presence of:",
  ["Keratinised scales", "Feathers", "Hair", "Mucus"], "D",
  "Skin of the frog",
  "NCERT: the skin of the frog is smooth and slippery due to the presence of mucus. The skin is always maintained in "
  "a moist condition.",
  ["Smooth, slippery skin → mucus"],
  R_SOA("frog: morphology"),
  why_others_wrong="Frogs have no scales, feathers or hair; scales cover reptiles and fishes, feathers birds and hair "
                   "mammals.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "In the frog, the digested food is absorbed by numerous finger-like folds in the inner wall of the intestine, "
  "called:",
  ["Villi and microvilli", "Rugae", "Calyces", "Nephrons"], "A",
  "Absorption of food in the frog",
  "NCERT: in the frog, digested food is absorbed by the numerous finger-like folds in the inner wall of the "
  "intestine called villi and microvilli. Undigested solid waste moves into the rectum and passes out through the "
  "cloaca.",
  ["Absorption → villi and microvilli of the intestine"],
  R_SOA("frog: anatomy (digestive system)"),
  why_others_wrong="Calyces are projections of the renal pelvis and nephrons are kidney units; NCERT does not use "
                   "'rugae' for the frog intestine.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "match_list",
  ml(("tissue", "role described in NCERT"),
     ["Epithelial tissue", "Connective tissue", "Muscle tissue", "Neural tissue"],
     ["Link and support other tissues or organs", "Greatest control over the body's responsiveness to changing "
      "conditions", "Covering or lining for some part of the body", "Contraction and relaxation that move the body"]),
  match_options(M("III", "I", "IV", "II"),
                [M("I", "III", "IV", "II"), M("III", "I", "II", "IV"), M("IV", "I", "III", "II")], "B"),
  "B",
  "The four basic animal tissues",
  "NCERT: epithelial tissue provides a covering or a lining for some part of the body; connective tissues link and "
  "support other tissues or organs; muscle fibres contract and relax and their action moves the body; neural tissue "
  "exerts the greatest control over the body's responsiveness to changing conditions.",
  ["Epithelial → covering/lining (III)", "Connective → link and support (I)", "Muscle → contraction (IV)",
   "Neural → control of responsiveness (II)"],
  R_SOA("animal tissues"),
  why_others_wrong="The other codes swap epithelial with connective tissue, muscle with neural tissue, or epithelial "
                   "with muscle tissue.",
  seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "assertion_reason",
  ar("Ciliated epithelium moves particles or mucus in a specific direction over the epithelium.",
     "The columnar or cuboidal cells of this epithelium bear cilia on their free surface."),
  ASSERTION_REASON, "A",
  "Ciliated epithelium",
  "NCERT: if the columnar or cuboidal cells bear cilia on their free surface they are called ciliated epithelium; "
  "their function is to move particles or mucus in a specific direction over the epithelium. The beating cilia on "
  "the free surface are what move the mucus, so R explains A.",
  ["A → true", "R → true", "Cilia on the free surface → movement of mucus → R explains A"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="B ignores that the cilia themselves do the moving; C and D call true statements false.",
  seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "statement_pair",
  sp("Cuboidal epithelium is commonly found in the ducts of glands, and its main functions are secretion and "
     "absorption.",
     "Simple epithelium is composed of several layers of cells and its main function is protection against "
     "mechanical stress."),
  STATEMENT_PAIR, "C",
  "Simple versus compound epithelium",
  "NCERT: simple epithelium is composed of a single layer of cells and functions as a lining for body cavities, ducts "
  "and tubes; compound epithelium has two or more cell layers and a protective function. Cuboidal epithelium is "
  "found in the ducts of glands and tubular parts of nephrons, mainly for secretion and absorption.",
  ["Statement I → true", "Statement II → false (that describes compound epithelium)"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="A and D accept a multilayered simple epithelium; B rejects a correct NCERT line on cuboidal "
                   "epithelium.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the frog are correct?",
     ["The hind limbs are larger and more muscular than the forelimbs.",
      "The muscular legs of the frog are used as food by man in some countries.",
      "The cloaca is a large chamber into which the stomach opens directly.",
      "Each kidney is composed of several structural and functional units called uriniferous tubules or nephrons."]),
  ["(a) and (b) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)"], "B",
  "Morphology and anatomy of the frog",
  "NCERT: the hind limbs end in five digits and are larger and muscular than the forelimbs; in some countries the "
  "muscular legs of the frog are used as food by man; each kidney is composed of several uriniferous tubules or "
  "nephrons. The cloaca is a small median chamber; food passes from the stomach through the intestine and rectum "
  "before reaching it.",
  ["(a) true", "(b) true", "(c) false – the stomach opens into the intestine, not the cloaca", "(d) true"],
  R_SOA("frog: morphology and anatomy"),
  why_others_wrong="A omits the true statement (d); C and D include the false statement (c).",
  seconds=45)

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "Besides fibres, the cells of connective tissues secrete a substance that accumulates between the cells and fibres "
  "and acts as the matrix (ground substance). According to NCERT, this substance consists of:",
  ["Keratin", "Actin and myosin", "Modified polysaccharides", "Haemoglobin"], "C",
  "Ground substance of connective tissue",
  "NCERT: the cells of connective tissues also secrete modified polysaccharides, which accumulate between cells and "
  "fibres and act as the matrix (ground substance).",
  ["Matrix (ground substance) → modified polysaccharides"],
  R_SOA("animal tissues: connective tissue"),
  why_others_wrong="Actin and myosin are contractile proteins of muscle; haemoglobin is the pigment of RBCs; keratin "
                   "is not named by NCERT as the matrix of connective tissue.",
  seconds=30)

Z(SOA, "Animal tissues", "Intermediate", "assertion_reason",
  ar("Cardiac muscle cells stick together.",
     "Cell junctions fuse the plasma membranes of cardiac muscle cells."),
  ASSERTION_REASON, "A",
  "Cell junctions in cardiac muscle",
  "NCERT: cell junctions fuse the plasma membranes of cardiac muscle cells and make them stick together. So the "
  "fusion of membranes by cell junctions (R) is the reason the cells stick together (A).",
  ["A → true", "R → true", "Membranes fused by junctions → cells stick together → R explains A"],
  R_SOA("animal tissues: muscle tissue"),
  why_others_wrong="B denies a cause that NCERT states in the same sentence; C and D call true statements false.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("Above the mouth, the frog has a pair of nostrils.",
     "The male reproductive organs of the frog include a pair of yellowish, ovoid testes."),
  STATEMENT_PAIR, "A",
  "External features and male reproductive organs of the frog",
  "NCERT: above the mouth of the frog, a pair of nostrils is present. The male reproductive organs consist of a pair "
  "of yellowish ovoid testes, found adhered to the upper part of the kidneys by a double fold of peritoneum called "
  "mesorchium.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("frog: morphology; reproductive system"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("Which of the following statements about muscle tissue are correct?",
     ["Muscle fibres contract (shorten) in response to stimulation, then relax (lengthen) and return to the "
      "uncontracted state in a coordinated fashion.",
      "The action of muscles moves the body to adjust to changes in the environment and to maintain the positions of "
      "the various body parts.",
      "Skeletal muscle tissue is closely attached to skeletal bones.",
      "Smooth muscle cells show a branching pattern.",
      "Skeletal muscle forms the walls of internal organs such as the blood vessels."]),
  ["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (c) only", "(a) and (c) only"], "C",
  "Muscle tissue: function and types",
  "NCERT: muscle fibres contract in response to stimulation, then relax and return to the uncontracted state in a "
  "coordinated fashion; their action moves the body to adjust to environmental changes and to maintain the positions "
  "of body parts. Skeletal muscle is closely attached to skeletal bones. Smooth muscle fibres taper at both ends; the "
  "branching pattern is described for cardiac muscle. The walls of internal organs such as blood vessels, stomach "
  "and intestine contain smooth muscle.",
  ["(a) true", "(b) true", "(c) true", "(d) false – branching is a feature of cardiac muscle cells",
   "(e) false – these walls have smooth muscle"],
  R_SOA("animal tissues: muscle tissue"),
  why_others_wrong="A includes (d); B includes (d) and (e) and leaves out (a) and (b); D omits the true statement (b).",
  seconds=60)

Z(SOA, "Animal tissues", "Advanced", "assertion_reason",
  ar("Cardiac muscles are involuntary in nature.",
     "Cardiac muscle tissue is a contractile tissue present only in the heart."),
  ASSERTION_REASON, "B",
  "Cardiac muscle",
  "Both statements are NCERT lines: cardiac muscle tissue is a contractile tissue present only in the heart, and "
  "cardiac muscles are involuntary because the nervous system does not control their activities directly. Being "
  "located only in the heart (R) is a statement about where the tissue occurs; it does not explain why its activity "
  "is involuntary (A). The explanation is the lack of direct nervous control.",
  ["A → true", "R → true", "Location in the heart ≠ reason for involuntary nature → R does not explain A"],
  R_SOA("animal tissues: muscle tissue") + "; Class 11 Biology, 'Locomotion and Movement', types of muscles",
  why_others_wrong="A treats the location of the tissue as the cause; C and D call true statements false.",
  seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "statement_pair",
  sp("In the male frog, the vasa efferentia enter the kidneys on their side and open into Bidder's canal.",
     "In the male frog, sperms are carried to the exterior by a separate vas deferens that opens to the outside "
     "independently of the ureter."),
  STATEMENT_PAIR, "C",
  "Male urinogenital system of the frog",
  "NCERT: in the male frog, the vasa efferentia enter the kidneys on their side and open into Bidder's canal, which "
  "finally communicates with the urinogenital duct that comes out of the kidneys and opens into the cloaca. Sperms "
  "and urine therefore share the urinogenital duct and the cloaca; there is no separate vas deferens opening to the "
  "outside.",
  ["Statement I → true", "Statement II → false (sperms pass through the urinogenital duct into the cloaca)"],
  R_SOA("frog: anatomy (reproductive system)"),
  why_others_wrong="A and D accept a separate sperm duct; B rejects the true NCERT line about Bidder's canal.",
  seconds=40)

Z(SOA, "Animal tissues", "Advanced", "match_list",
  ml(("epithelium", "function"),
     ["Ciliated epithelium", "Compound epithelium", "Glandular epithelium", "Squamous epithelium"],
     ["Specialised for secretion", "Forming a diffusion boundary", "Moving particles or mucus in a specific direction",
      "Protection against chemical and mechanical stresses"]),
  match_options(M("III", "IV", "I", "II"),
                [M("III", "II", "I", "IV"), M("IV", "III", "I", "II"), M("III", "IV", "II", "I")], "D"),
  "D",
  "Functions of different epithelia",
  "NCERT: ciliated epithelium moves particles or mucus in a specific direction; the main function of compound "
  "epithelium is protection against chemical and mechanical stresses; some columnar or cuboidal cells get "
  "specialised for secretion and are called glandular epithelium; squamous epithelium is involved in functions like "
  "forming a diffusion boundary.",
  ["Ciliated → moving mucus (III)", "Compound → protection (IV)", "Glandular → secretion (I)",
   "Squamous → diffusion boundary (II)"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="A gives the diffusion boundary to compound epithelium; B swaps ciliated and compound epithelia; "
                   "C swaps glandular and squamous epithelia.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "direct",
  "Which of the following correctly matches an epithelium with a site where NCERT says it is found and its main "
  "function there?",
  ["Squamous epithelium – inner surface of fallopian tubes – moving the ovum along the tube",
   "Columnar epithelium – walls of blood vessels – forming a diffusion boundary",
   "Compound epithelium – lining of the intestine – absorption of digested food",
   "Cuboidal epithelium – ducts of glands – secretion and absorption"], "D",
  "Site and function of epithelia",
  "NCERT: cuboidal epithelium is commonly found in the ducts of glands and the tubular parts of nephrons, and its "
  "main functions are secretion and absorption. Squamous epithelium lines the walls of blood vessels and air sacs "
  "and forms a diffusion boundary; columnar epithelium lines the stomach and intestine; the inner surface of "
  "fallopian tubes bears ciliated epithelium; compound epithelium has a limited role in secretion and absorption.",
  ["Check site and function together", "Only cuboidal – ducts of glands – secretion and absorption fits both"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="A gives the fallopian tube lining to squamous epithelium; B gives the blood-vessel wall and "
                   "diffusion to columnar epithelium; C gives absorption in the intestine to compound epithelium.",
  seconds=50)

# ================================================================ Biomolecules (B6 I8 A6)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Carbohydrates and lipids", "Basic", "assertion_reason",
  ar("Elemental analysis of a living tissue tells us the kinds of organic compounds present in it.",
     "Analysis for compounds gives an idea of the kind of organic and inorganic constituents present in living "
     "tissues."),
  ASSERTION_REASON, "D",
  "Elemental analysis versus analysis for compounds",
  "NCERT: elemental analysis gives the elemental composition of living tissues in the form of hydrogen, oxygen, "
  "chlorine, carbon, etc., while analysis for compounds gives an idea of the kind of organic and inorganic "
  "constituents present in living tissues. A is false (elemental analysis lists elements, not compounds); R is true.",
  ["A → false (elemental analysis gives elements only)", "R → true"],
  R_BIO("how to analyse chemical composition"),
  why_others_wrong="A, B and C all accept the assertion, but identifying compounds needs analysis for compounds, not "
                   "elemental analysis.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "According to NCERT, co-factors of enzymes are of three kinds. Which of the following is NOT one of them?",
  ["Prosthetic groups", "Co-enzymes", "Apoenzymes", "Metal ions"], "C",
  "Kinds of co-factors",
  "NCERT: co-factors are non-protein constituents bound to the enzyme to make it catalytically active. Three kinds "
  "of co-factors may be identified: prosthetic groups, co-enzymes and metal ions. The protein portion of such an "
  "enzyme is the apoenzyme, which is not a co-factor.",
  ["Co-factors → prosthetic groups, co-enzymes, metal ions", "Apoenzyme → protein part, not a co-factor"],
  R_BIO("co-factors"),
  why_others_wrong="Prosthetic groups, co-enzymes and metal ions are exactly the three kinds NCERT lists.",
  seconds=20)

Z(BIO, "Carbohydrates and lipids", "Basic", "match_list",
  ml(("biomolecule", "building block"),
     ["Protein", "Cellulose", "Triglyceride", "Nucleic acid"],
     ["Nucleotides", "Glucose", "Amino acids", "Glycerol and fatty acids"]),
  match_options(M("III", "II", "IV", "I"),
                [M("III", "IV", "II", "I"), M("I", "II", "IV", "III"), M("II", "III", "IV", "I")], "D"),
  "D",
  "Monomers of biomolecules",
  "NCERT: proteins are polypeptides, linear chains of amino acids; cellulose is a polymeric polysaccharide of only "
  "one type of monosaccharide, glucose; in triglycerides, fatty acids are esterified with glycerol; nucleic acids "
  "are polynucleotides, whose building block is a nucleotide.",
  ["Protein → amino acids (III)", "Cellulose → glucose (II)", "Triglyceride → glycerol + fatty acids (IV)",
   "Nucleic acid → nucleotides (I)"],
  R_BIO("proteins; polysaccharides; lipids; nucleic acids"),
  why_others_wrong="The other codes give cellulose glycerol and fatty acids, give proteins nucleotides, or give "
                   "proteins glucose.",
  seconds=25)

Z(BIO, "Enzymes: properties and action", "Basic", "statement_pair",
  sp("If the product P of a reaction is at a lower energy level than the substrate S, the reaction is an exothermic "
     "reaction.",
     "The transition state between the substrate and the product is a stable structural state."),
  STATEMENT_PAIR, "C",
  "Energy changes in a reaction",
  "NCERT: if P is at a lower level than S, the reaction is exothermic. Between the stable substrate and the product "
  "there are many 'altered structural states', and all these intermediate states, including the transition state, "
  "are unstable. Statement II is therefore false.",
  ["Statement I → true", "Statement II → false (transition state is unstable)"],
  R_BIO("how do enzymes bring about such high rates of chemical conversions?"),
  why_others_wrong="A and D call the transition state stable; B rejects the NCERT definition of an exothermic "
                   "reaction.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "When the binding of a chemical to an enzyme shuts off the enzyme's activity, the process and the chemical are "
  "respectively called:",
  ["Denaturation and denaturant", "Inhibition and inhibitor", "Activation and activator", "Catalysis and co-factor"],
  "B",
  "Inhibition of enzyme activity",
  "NCERT: the activity of an enzyme is sensitive to the presence of specific chemicals that bind to it. When the "
  "binding of the chemical shuts off enzyme activity, the process is called inhibition and the chemical is called "
  "an inhibitor.",
  ["Activity shut off by a bound chemical → inhibition; chemical → inhibitor"],
  R_BIO("factors affecting enzyme activity: presence of inhibitors"),
  why_others_wrong="Denaturation is the destruction of protein structure, for example by heat; activators and "
                   "co-factors increase or permit activity rather than shut it off.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "In the potential-energy diagram of a reaction, the difference in the average energy content of the substrate S "
  "from that of the transition state is called the:",
  ["Activation energy", "Maximum velocity (Vmax)", "Optimum energy", "Energy of the product"], "A",
  "Activation energy",
  "NCERT: the y-axis of the diagram represents the potential energy content and the x-axis the progression of the "
  "reaction. The difference in average energy content of S from that of this transition state is called the "
  "activation energy. Enzymes bring down this energy barrier.",
  ["Energy of transition state − average energy of S = activation energy"],
  R_BIO("how do enzymes bring about such high rates of chemical conversions?"),
  why_others_wrong="Vmax is the maximum velocity reached at high substrate concentration; 'optimum' is used for "
                   "temperature and pH; the energy of the product is a different level on the diagram.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("Co-factors are non-protein constituents bound to an enzyme to make the enzyme catalytically active.",
     "Co-enzymes serve as co-factors in a number of different enzyme-catalysed reactions."),
  STATEMENT_PAIR, "A",
  "Co-factors and co-enzymes",
  "NCERT: enzymes may be composed of one or several polypeptide chains, and in a number of cases non-protein "
  "constituents called co-factors are bound to the enzyme to make it catalytically active. Co-enzymes are organic "
  "compounds whose association with the apoenzyme is transient; furthermore, co-enzymes serve as co-factors in a "
  "number of different enzyme-catalysed reactions.",
  ["Statement I → true", "Statement II → true"],
  R_BIO("co-factors"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Triglycerides are called fats or oils on the basis of their melting point.",
     "Oils have a higher melting point than fats and therefore remain solid in winter."),
  ASSERTION_REASON, "C",
  "Fats and oils",
  "NCERT: fatty acids esterified with glycerol form mono-, di- and triglycerides, which are also called fats and "
  "oils based on melting point. Oils have a lower melting point (e.g. gingelly oil) and hence remain as oil in "
  "winter. A is true; R reverses the melting-point relation and is false.",
  ["A → true", "R → false (oils have the lower melting point)"],
  R_BIO("lipids"),
  why_others_wrong="A and B accept a false reason; D rejects the NCERT basis for naming fats and oils.",
  seconds=30)

Z(BIO, "Proteins and amino acids", "Intermediate", "assertion_reason",
  ar("A protein is a heteropolymer and not a homopolymer.",
     "A homopolymer has only one type of monomer repeating 'n' number of times, whereas a protein is built from "
     "different types of amino acids."),
  ASSERTION_REASON, "A",
  "Proteins as heteropolymers",
  "NCERT: a protein is a heteropolymer and not a homopolymer; a homopolymer has only one type of monomer repeating "
  "'n' number of times. Proteins are made of different types of amino acids (twenty types occur in proteins), so "
  "the definition given in R is exactly why a protein is called a heteropolymer.",
  ["A → true", "R → true", "Different monomers ≠ homopolymer → R explains A"],
  R_BIO("proteins"),
  why_others_wrong="B denies the definitional link; C and D call true statements false.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("Unlike other proteins, enzymes have no primary structure.",
     "In the tertiary structure of an enzyme, the backbone of the protein chain folds upon itself and criss-crosses "
     "itself, creating many crevices or pockets."),
  STATEMENT_PAIR, "D",
  "Structure of enzymes",
  "NCERT: enzymes are generally proteins and, like any protein, an enzyme has a primary structure, i.e. an amino "
  "acid sequence, as well as secondary and tertiary structures. In the tertiary structure the backbone folds upon "
  "itself, the chain criss-crosses itself and many crevices or pockets are made; one such pocket is the active site.",
  ["Statement I → false (enzymes have a primary structure)", "Statement II → true"],
  R_BIO("enzymes"),
  why_others_wrong="A and C accept that enzymes lack a primary structure; B rejects the NCERT description of the "
                   "tertiary structure.",
  seconds=30)

Z(BIO, "Enzyme classification", "Intermediate", "direct",
  "Succinic dehydrogenase removes hydrogen from its substrate succinate (oxidising it) while another substrate is "
  "reduced. In the NCERT classification of enzymes, it belongs to the class:",
  ["Transferases", "Hydrolases", "Oxidoreductases", "Lyases"], "C",
  "Classifying an enzyme",
  "NCERT names the first class 'Oxidoreductases/dehydrogenases': enzymes that catalyse oxidoreduction between two "
  "substrates, S reduced + S' oxidised → S oxidised + S' reduced. A dehydrogenase such as succinic dehydrogenase "
  "removes hydrogen from (oxidises) its substrate and therefore belongs to this class.",
  ["Removal of hydrogen = oxidation of one substrate, reduction of another", "→ Oxidoreductases/dehydrogenases"],
  R_BIO("classification and nomenclature of enzymes"),
  why_others_wrong="Transferases move a group other than hydrogen; hydrolases break bonds by adding water; lyases "
                   "remove groups leaving double bonds.",
  seconds=30)

Z(BIO, "Enzyme classification", "Intermediate", "direct",
  "An enzyme transfers a phosphate group from ATP to glucose. In the NCERT classification of enzymes, it is a:",
  ["Ligase", "Transferase", "Isomerase", "Hydrolase"], "B",
  "Classifying an enzyme",
  "NCERT: transferases catalyse the transfer of a group G (other than hydrogen) between a pair of substrates S and "
  "S': S – G + S' → S + S' – G. Moving a phosphate group from ATP to glucose is such a group transfer.",
  ["Group (phosphate, not hydrogen) moved between two substrates → transferase"],
  R_BIO("classification and nomenclature of enzymes"),
  why_others_wrong="Ligases link two compounds together; isomerases interconvert isomers of one compound; hydrolases "
                   "break bonds by hydrolysis.",
  seconds=30)

Z(BIO, "Enzyme classification", "Intermediate", "match_list",
  ml(("reaction", "class of enzyme"),
     ["Trypsin hydrolysing the peptide bonds of a protein",
      "Removal of a water molecule from a substrate, leaving a double bond",
      "Conversion of a cis isomer of a compound into its trans isomer",
      "Linking two compounds together by a C–N bond"],
     ["Ligases", "Isomerases", "Hydrolases", "Lyases"]),
  match_options(M("III", "IV", "II", "I"),
                [M("III", "II", "IV", "I"), M("IV", "III", "II", "I"), M("III", "IV", "I", "II")], "D"),
  "D",
  "Applying the enzyme classes",
  "NCERT: hydrolases catalyse hydrolysis of ester, ether, peptide, glycosidic and other bonds (trypsin is an enzyme "
  "that breaks peptide bonds); lyases remove groups from substrates by mechanisms other than hydrolysis, leaving "
  "double bonds; isomerases interconvert optical, geometric or positional isomers (cis–trans is geometric "
  "isomerism); ligases link two compounds together, e.g. by C–O, C–S, C–N or P–O bonds.",
  ["Peptide-bond hydrolysis → Hydrolases (III)", "Removal leaving double bond → Lyases (IV)",
   "cis → trans → Isomerases (II)", "Joining by C–N bond → Ligases (I)"],
  R_BIO("classification and nomenclature of enzymes"),
  why_others_wrong="A swaps lyases and isomerases; B calls trypsin a lyase; C swaps isomerases and ligases.",
  seconds=45)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "direct",
  "NCERT compares the elemental composition of the human body with that of the earth's crust. Which element is a "
  "major constituent of the earth's crust but is shown as negligible in the human body?",
  ["Carbon", "Silicon", "Nitrogen", "Oxygen"], "B",
  "Elements in living and non-living matter",
  "In the NCERT table comparing elements in the earth's crust and the human body (per cent weight), silicon is a "
  "large component of the earth's crust but is negligible in the human body. Carbon is far more abundant in the body "
  "than in the crust, nitrogen is present in the body but very little in the crust, and oxygen is abundant in both.",
  ["Silicon → large share of crust, negligible in body"],
  R_BIO("how to analyse chemical composition (comparison of elements in the earth's crust and human body)"),
  why_others_wrong="Carbon and nitrogen are relatively more abundant in the body than in the crust; oxygen is a major "
                   "element of both.",
  seconds=25)

Z(BIO, "Enzymes: properties and action", "Advanced", "direct",
  "A purified enzyme preparation is dialysed to remove small non-protein molecules, and it loses its catalytic "
  "activity. When the small molecules removed are added back, the activity is restored. The best conclusion is:",
  ["The enzyme was denatured by dialysis and has been renatured",
   "The enzyme requires a non-protein co-factor; the protein part (apoenzyme) alone is catalytically inactive",
   "The small molecules were competitive inhibitors of the enzyme",
   "The enzyme is a ribozyme made of nucleic acid"], "B",
  "Role of co-factors",
  "NCERT: in many enzymes, non-protein co-factors are bound to the enzyme to make it catalytically active, the "
  "protein portion being the apoenzyme; catalytic activity is lost when the co-factor is removed from the enzyme, "
  "which shows that co-factors play a crucial role. Loss of activity on removing small molecules and its return on "
  "adding them back fits exactly this.",
  ["Remove small non-protein molecules → activity lost", "Add them back → activity restored",
   "→ co-factor needed; apoenzyme alone inactive"],
  R_BIO("co-factors"),
  why_others_wrong="Heat denaturation is not what dialysis does, and denaturation would not be reversed by adding the "
                   "small molecules; inhibitors would raise activity when removed, not lower it; a purified enzyme "
                   "that needs small molecules to work need not be a nucleic acid.",
  seconds=50)

Z(BIO, "Carbohydrates and lipids", "Advanced", "direct",
  "A tissue containing glucose, free amino acids, nucleotides, cellulose and membrane lipids is ground in "
  "trichloroacetic acid and strained through cheesecloth. Which two of these will be found in the acid-insoluble "
  "(retentate) fraction?",
  ["Cellulose and the membrane lipids", "Glucose and the free amino acids", "Nucleotides and glucose",
   "Free amino acids and the membrane lipids"], "A",
  "Acid-soluble and acid-insoluble fractions",
  "NCERT: the acid-insoluble fraction contains proteins, nucleic acids, polysaccharides and lipids. Cellulose is a "
  "polysaccharide (a macromolecule). Lipids are small (below 800 Da) but appear in the insoluble fraction because, "
  "on grinding, cell membranes break into vesicles that are not water-soluble. Glucose, amino acids and nucleotides "
  "are small molecules of the acid-soluble pool (molecular weight about 18 to 800 Da).",
  ["Polysaccharide (cellulose) → acid-insoluble", "Membrane lipids → vesicles → acid-insoluble",
   "Sugars, amino acids, nucleotides → acid-soluble"],
  R_BIO("how to analyse chemical composition"),
  why_others_wrong="B, C and D each place at least one small, acid-soluble molecule (glucose, amino acids or "
                   "nucleotides) in the insoluble fraction.",
  seconds=50)

Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("Which of the following statements about enzyme action are correct?",
     ["The chemical which is converted into a product is called the substrate.",
      "The substrate has to diffuse towards the active site of the enzyme.",
      "An enzyme molecule is used up after it converts one substrate molecule.",
      "Enzymes are proteins with three-dimensional structures that include an active site.",
      "An enzyme raises the activation energy of the reaction it catalyses."]),
  ["(a), (b) and (c) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"], "B",
  "Enzyme–substrate interaction",
  "NCERT: the chemical converted into a product is the substrate; enzymes, i.e. proteins with three-dimensional "
  "structures including an active site, convert a substrate into a product; the substrate has to diffuse towards "
  "the active site. After the products are released, the free enzyme is ready to bind another substrate molecule, so "
  "it is not used up. Enzymes bring down the energy barrier (activation energy).",
  ["(a) true", "(b) true", "(c) false – enzyme is released free after each cycle", "(d) true",
   "(e) false – enzymes lower the activation energy"],
  R_BIO("how do enzymes bring about such high rates of chemical conversions?; nature of enzyme action"),
  why_others_wrong="A includes (c); C and D include (e), and C also leaves out (a).",
  seconds=60)

Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("Which of the following statements are correct according to NCERT?",
     ["A physical change refers to a change in shape without the breaking of bonds.",
      "Ba(OH)₂ + H₂SO₄ → BaSO₄ + 2H₂O is an example of an inorganic chemical reaction.",
      "The hydrolysis of starch into glucose is a physical change.",
      "Enzymes are inorganic catalysts."]),
  ["(a), (b) and (c) only", "(b) and (c) only", "(a), (b) and (d) only", "(a) and (b) only"], "D",
  "Physical and chemical changes",
  "NCERT: a physical change refers to a change in shape without breaking of bonds. Chemical reactions involve "
  "breaking of bonds and formation of new bonds; Ba(OH)₂ + H₂SO₄ → BaSO₄ + 2H₂O is given as an inorganic chemical "
  "reaction, and hydrolysis of starch into glucose as an organic chemical reaction. Almost all enzymes are proteins, "
  "i.e. biological catalysts, not inorganic catalysts.",
  ["(a) true", "(b) true", "(c) false – it is an organic chemical reaction", "(d) false – enzymes are mostly proteins"],
  R_BIO("chemical reactions"),
  why_others_wrong="A and B include (c); C includes (d).",
  seconds=50)

Z(BIO, "Carbohydrates and lipids", "Advanced", "statement_pair",
  sp("The relative abundance of carbon and hydrogen with respect to other elements is higher in any living organism "
     "than in the earth's crust.",
     "All the elements present in a sample of the earth's crust are also present in a sample of living tissue."),
  STATEMENT_PAIR, "A",
  "Living versus non-living matter",
  "NCERT: if elemental analysis is performed on a living tissue and on a piece of the earth's crust, a similar list is "
  "obtained; in absolute terms no differences can be made out, and all the elements present in a sample of the "
  "earth's crust are also present in a sample of living tissue. A closer examination shows that the relative "
  "abundance of carbon and hydrogen with respect to other elements is higher in any living organism.",
  ["Statement I → true", "Statement II → true"],
  R_BIO("how to analyse chemical composition"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=40)

Z(BIO, "Carbohydrates and lipids", "Advanced", "direct",
  "Which of the following pairs consists of two homopolymers?",
  ["Glycogen and haemoglobin", "Starch and collagen", "Cellulose and glycogen", "Inulin and trypsin"], "C",
  "Homopolymers and heteropolymers",
  "NCERT: a homopolymer has only one type of monomer repeating 'n' times. Cellulose is a polymeric polysaccharide of "
  "only one type of monosaccharide, glucose, and glycogen (the animal variant of starch) is also a polymer of "
  "glucose. Proteins such as haemoglobin, collagen and trypsin are heteropolymers of different amino acids.",
  ["Cellulose → glucose only; glycogen → glucose only → both homopolymers",
   "Haemoglobin, collagen, trypsin → proteins → heteropolymers"],
  R_BIO("polysaccharides; proteins"),
  why_others_wrong="Each of the other pairs contains a protein (haemoglobin, collagen or trypsin), which is a "
                   "heteropolymer.",
  seconds=40)

# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Respiratory system", "Basic", "direct",
  "In humans, a pair of external nostrils opening out above the upper lips leads through the nasal passage into "
  "the:",
  ["Larynx", "Nasal chamber", "Trachea", "Primary bronchi"], "B",
  "Path of air in the human respiratory system",
  "NCERT: we have a pair of external nostrils opening out above the upper lips. They lead to a nasal chamber through "
  "the nasal passage. The nasal chamber opens into the pharynx.",
  ["External nostrils → nasal passage → nasal chamber → pharynx"],
  R_BRE("human respiratory system"),
  why_others_wrong="The larynx, trachea and bronchi lie further along the path, after the pharynx.",
  seconds=20)

Z(BRE, "Respiratory system", "Basic", "statement_pair",
  sp("Oxygen is utilised by organisms to indirectly break down nutrient molecules like glucose and to derive energy "
     "for performing various activities.",
     "Carbon dioxide released during these catabolic reactions is harmless and need not be removed from the body."),
  STATEMENT_PAIR, "C",
  "Why we breathe",
  "NCERT: oxygen is utilised by organisms to indirectly break down simple molecules like glucose, amino acids and "
  "fatty acids to derive energy. Carbon dioxide, which is harmful, is also released during these catabolic "
  "reactions; it must therefore be released from the cells, which is why O₂ has to be continuously provided and CO₂ "
  "released.",
  ["Statement I → true", "Statement II → false (CO₂ is harmful and must be released)"],
  R_BRE("introduction"),
  why_others_wrong="A and D call CO₂ harmless; B rejects the true NCERT line on the use of oxygen.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Basic", "direct",
  "According to NCERT, the partial pressure of oxygen (pO₂) in the alveoli is about:",
  ["159 mm Hg", "95 mm Hg", "104 mm Hg", "40 mm Hg"], "C",
  "Partial pressure of O₂ in alveolar air",
  "In the NCERT table of partial pressures, pO₂ is 159 mm Hg in atmospheric air, 104 mm Hg in the alveoli, 95 mm Hg "
  "in oxygenated blood and 40 mm Hg in deoxygenated blood and in the tissues.",
  ["Alveoli → pO₂ about 104 mm Hg"],
  R_BRE("exchange of gases (table of partial pressures)"),
  why_others_wrong="159 mm Hg is atmospheric air, 95 mm Hg oxygenated blood and 40 mm Hg deoxygenated blood or "
                   "tissues.",
  seconds=20)

Z(BRE, "Exchange and transport of gases", "Basic", "direct",
  "NCERT lists the steps of respiration in order. Which step immediately follows the transport of gases by the "
  "blood?",
  ["Diffusion of O₂ and CO₂ between the blood and the tissues",
   "Diffusion of gases across the alveolar membrane",
   "Pulmonary ventilation (breathing)",
   "Utilisation of O₂ by the cells for catabolic reactions"], "A",
  "Steps of respiration",
  "NCERT: the steps are (i) breathing or pulmonary ventilation; (ii) diffusion of gases across the alveolar "
  "membrane; (iii) transport of gases by the blood; (iv) diffusion of O₂ and CO₂ between blood and tissues; (v) "
  "utilisation of O₂ by the cells for catabolic reactions and resultant release of CO₂ (cellular respiration).",
  ["Step (iii) transport → step (iv) diffusion between blood and tissues"],
  R_BRE("respiratory organs: steps of respiration"),
  why_others_wrong="Alveolar diffusion and breathing come before transport; utilisation by cells is the step after "
                   "diffusion into the tissues.",
  seconds=25)

Z(BRE, "Respiratory system", "Intermediate", "match_list",
  ml(("term", "meaning"),
     ["Branchial respiration", "Pulmonary respiration", "Cutaneous respiration", "Cellular respiration"],
     ["Exchange of gases through the moist skin", "Utilisation of O₂ by cells for catabolic reactions and release "
      "of CO₂", "Exchange of gases through gills", "Exchange of gases through lungs"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("I", "IV", "III", "II")], "D"),
  "D",
  "Kinds of respiration",
  "NCERT: aquatic arthropods and molluscs use gills (branchial respiration); terrestrial forms use lungs (pulmonary "
  "respiration); amphibians like frogs can respire through their moist skin (cutaneous respiration). Utilisation of "
  "O₂ by the cells for catabolic reactions and the resultant release of CO₂ is cellular respiration.",
  ["Branchial → gills (III)", "Pulmonary → lungs (IV)", "Cutaneous → skin (I)", "Cellular → use of O₂ by cells (II)"],
  R_BRE("respiratory organs; steps of respiration"),
  why_others_wrong="A swaps gills and lungs; B swaps skin and cellular respiration; C gives the skin to branchial "
                   "respiration.",
  seconds=35)

Z(BRE, "Exchange and transport of gases", "Intermediate", "multi_statement",
  ms("Using the NCERT values of partial pressures, which of the following statements are correct?",
     ["O₂ diffuses from the alveoli (pO₂ about 104 mm Hg) into the deoxygenated blood (pO₂ about 40 mm Hg).",
      "O₂ diffuses from the oxygenated blood (pO₂ about 95 mm Hg) into the tissues (pO₂ about 40 mm Hg).",
      "O₂ and CO₂ cross the diffusion membrane by active transport against the gradient.",
      "CO₂ diffuses from the alveoli into the deoxygenated blood."]),
  ["(a), (b) and (d) only", "(a) and (b) only", "(b) and (c) only", "(a), (b) and (c) only"], "B",
  "Direction of gas diffusion",
  "NCERT: O₂ and CO₂ are exchanged by simple diffusion, mainly based on the pressure or concentration gradient. pO₂ "
  "falls from alveoli (104) to deoxygenated blood (40), and from oxygenated blood (95) to tissues (40), so O₂ moves "
  "in both these directions. pCO₂ is higher in deoxygenated blood (45) than in the alveoli (40), so CO₂ moves from "
  "blood to alveoli, not the reverse.",
  ["(a) true", "(b) true", "(c) false – simple diffusion along gradients", "(d) false – CO₂ moves from blood to alveoli"],
  R_BRE("exchange of gases"),
  why_others_wrong="A includes (d); C and D include (c), and C also omits (a).",
  seconds=50)

Z(BRE, "Respiratory system", "Intermediate", "direct",
  "According to NCERT, the mechanisms of breathing vary among different groups of animals depending mainly on their:",
  ["Body size and colour", "Habitats and levels of organisation", "Diet and mode of reproduction",
   "Life span and body temperature"], "B",
  "Diversity of respiratory organs",
  "NCERT: mechanisms of breathing vary among different groups of animals depending mainly on their habitats and "
  "levels of organisation. For example, lower invertebrates exchange gases by simple diffusion over the body "
  "surface, insects use tracheal tubes, aquatic forms use gills and terrestrial forms use lungs.",
  ["Breathing mechanism ← habitat + level of organisation"],
  R_BRE("respiratory organs"),
  why_others_wrong="NCERT names habitat and level of organisation, not size, colour, diet, reproduction or life span.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Intermediate", "statement_pair",
  sp("The partial pressure of CO₂ in alveolar air is about 40 mm Hg.",
     "The partial pressure of O₂ in deoxygenated blood is about 95 mm Hg."),
  STATEMENT_PAIR, "C",
  "Partial pressures of respiratory gases",
  "NCERT table: pCO₂ is about 40 mm Hg in the alveoli; pO₂ is about 40 mm Hg in deoxygenated blood and about 95 mm "
  "Hg in oxygenated blood. Statement II gives the value for oxygenated blood.",
  ["Statement I → true", "Statement II → false (deoxygenated blood pO₂ ≈ 40 mm Hg)"],
  R_BRE("exchange of gases (table of partial pressures)"),
  why_others_wrong="A and D accept 95 mm Hg for deoxygenated blood; B rejects the correct alveolar pCO₂.",
  seconds=30)

Z(BRE, "Respiratory system", "Intermediate", "multi_statement",
  ms("Which of the following statements about respiratory organs are correct?",
     ["Lower invertebrates like sponges, coelenterates and flatworms exchange O₂ with CO₂ by simple diffusion over "
      "their entire body surface.",
      "Aquatic arthropods and molluscs use gills for the exchange of gases.",
      "Among vertebrates, fishes use gills, whereas reptiles, birds and mammals respire through lungs.",
      "Insects exchange gases through a moist cuticle.",
      "Earthworms use a network of tracheal tubes for respiration."]),
  ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (c) only", "(a), (b) and (c) only"], "D",
  "Respiratory organs in animals",
  "NCERT: sponges, coelenterates and flatworms exchange gases by simple diffusion over the entire body surface; "
  "earthworms use their moist cuticle and insects have a network of tubes (tracheal tubes); aquatic arthropods and "
  "molluscs use gills, terrestrial forms use lungs; among vertebrates, fishes use gills while reptiles, birds and "
  "mammals respire through lungs.",
  ["(a) true", "(b) true", "(c) true", "(d) false – insects use tracheal tubes",
   "(e) false – earthworms use the moist cuticle"],
  R_BRE("respiratory organs"),
  why_others_wrong="A includes (d); B includes (e); C omits the true statement (b).",
  seconds=45)

Z(BRE, "Respiratory volumes", "Advanced", "numerical",
  "For a healthy adult, the functional residual capacity is 2300 mL, the residual volume 1200 mL, the vital capacity "
  "4600 mL and the tidal volume 500 mL. What is the inspiratory reserve volume?",
  ["4100 mL", "1800 mL", "3500 mL", "3000 mL"], "D",
  "Respiratory volumes and capacities",
  "NCERT: functional residual capacity (FRC) = ERV + RV, and vital capacity (VC) = ERV + TV + IRV. So ERV = FRC − RV "
  "= 2300 − 1200 = 1100 mL, and IRV = VC − ERV − TV = 4600 − 1100 − 500 = 3000 mL, which lies in the NCERT range of "
  "2500–3000 mL.",
  ["ERV = FRC − RV = 2300 − 1200 = 1100 mL", "IRV = VC − ERV − TV = 4600 − 1100 − 500 = 3000 mL"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="VC − TV − (FRC − RV) = 4600 − 500 − 1100 = 3000 mL.",
  why_others_wrong="4100 mL forgets to subtract ERV; 1800 mL subtracts the whole FRC instead of ERV; 3500 mL is "
                   "VC − ERV, i.e. the inspiratory capacity (TV + IRV), not IRV.",
  seconds=75, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "NCERT names the pressure (concentration) gradient, the solubility of the gases and the thickness of the membranes "
  "as factors affecting the rate of diffusion. Other things remaining the same, which change would INCREASE the rate "
  "of diffusion of O₂ from the alveoli into the blood?",
  ["A thickening of the diffusion membrane", "A fall in the pO₂ of alveolar air",
   "A rise in the pO₂ of the deoxygenated blood reaching the alveoli",
   "A decrease in the thickness of the diffusion membrane"], "D",
  "Factors affecting diffusion",
  "NCERT: the pressure or concentration gradient, the solubility of gases and the thickness of the membranes involved "
  "in diffusion affect the rate of diffusion. A thinner membrane allows faster diffusion. A thicker membrane, a lower "
  "alveolar pO₂ or a higher pO₂ in the incoming blood all reduce the rate, the last two by reducing the gradient.",
  ["Thinner membrane → faster diffusion",
   "Lower alveolar pO₂ or higher blood pO₂ → smaller gradient → slower diffusion"],
  R_BRE("exchange of gases"),
  why_others_wrong="A thickens the barrier; B and C reduce the O₂ gradient between alveoli and blood.",
  seconds=45)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "A sample has a pO₂ of about 95 mm Hg and a pCO₂ of about 40 mm Hg. Using the NCERT table of partial pressures, "
  "the sample is most likely:",
  ["Oxygenated blood", "Alveolar air", "Deoxygenated blood", "Fluid from a body tissue"], "A",
  "Reading the partial-pressure table",
  "NCERT values (mm Hg): alveoli – pO₂ 104, pCO₂ 40; deoxygenated blood – pO₂ 40, pCO₂ 45; oxygenated blood – pO₂ "
  "95, pCO₂ 40; tissues – pO₂ 40, pCO₂ 45. Only oxygenated blood has the pair 95 and 40.",
  ["pCO₂ 40 → alveoli or oxygenated blood", "pO₂ 95 (not 104) → oxygenated blood"],
  R_BRE("exchange of gases (table of partial pressures)"),
  why_others_wrong="Alveolar air has the same pCO₂ but a pO₂ of 104 mm Hg; deoxygenated blood and tissues have pO₂ "
                   "40 and pCO₂ 45 mm Hg.",
  seconds=40)

Z(BRE, "Exchange and transport of gases", "Advanced", "assertion_reason",
  ar("At the tissues, CO₂ diffuses from the tissue cells into the blood.",
     "The pCO₂ in the tissues (about 45 mm Hg) is higher than that in the oxygenated blood reaching them (about 40 "
     "mm Hg)."),
  ASSERTION_REASON, "A",
  "Diffusion of CO₂ at the tissues",
  "NCERT: gases are exchanged by simple diffusion along the partial-pressure gradient. In the tissues, pCO₂ is about "
  "45 mm Hg because of catabolism, while the arriving oxygenated blood has pCO₂ about 40 mm Hg. CO₂ therefore "
  "diffuses from the tissues into the blood; the gradient in R is the cause of the movement in A.",
  ["A → true", "R → true (45 > 40 mm Hg)", "Gradient drives diffusion → R explains A"],
  R_BRE("exchange of gases"),
  why_others_wrong="B ignores that diffusion follows this gradient; C and D call true statements false.",
  seconds=35)

# ================================================================ Body Fluids and Circulation (B5 I7 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "Which two types of leucocytes are described by NCERT as phagocytic cells that destroy foreign organisms entering "
  "the body?",
  ["Basophils and eosinophils", "Neutrophils and monocytes", "Lymphocytes and basophils", "Eosinophils and lymphocytes"],
  "B",
  "Phagocytic leucocytes",
  "NCERT: neutrophils and monocytes (6–8 per cent) are phagocytic cells which destroy foreign organisms entering the "
  "body. Basophils secrete histamine, serotonin, heparin, etc.; eosinophils resist infections and are associated "
  "with allergic reactions; lymphocytes (B and T) are responsible for immune responses.",
  ["Phagocytes → neutrophils and monocytes"],
  R_BFC("blood: formed elements"),
  why_others_wrong="Basophils, eosinophils and lymphocytes are given other roles by NCERT, not phagocytosis.",
  seconds=20)

Z(BFC, "Coagulation and lymph", "Basic", "direct",
  "Platelets, also called thrombocytes, are cell fragments produced from:",
  ["Erythroblasts in the spleen", "Lymphocytes in the lymph nodes", "Monocytes in the liver",
   "Megakaryocytes, special cells in the bone marrow"], "D",
  "Origin of platelets",
  "NCERT: platelets, also called thrombocytes, are cell fragments produced from megakaryocytes (special cells in the "
  "bone marrow). Blood normally contains 1,50,000–3,50,000 platelets per mm³, and they are involved in coagulation.",
  ["Platelets (thrombocytes) ← megakaryocytes of the bone marrow"],
  R_BFC("blood: formed elements"),
  why_others_wrong="The spleen is the graveyard of RBCs, and lymphocytes and monocytes are whole leucocytes, not "
                   "the source of platelets.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "The Rh antigen found on the surface of RBCs of most humans is so named because it is similar to an antigen present "
  "in:",
  ["Rhesus monkeys", "Rats", "Rabbits", "Horses"], "A",
  "Rh grouping",
  "NCERT: another antigen, the Rh antigen, similar to one present in Rhesus monkeys (hence Rh), is also observed on "
  "the surface of RBCs of the majority of humans.",
  ["Rh → Rhesus monkey"],
  R_BFC("blood groups: Rh grouping"),
  why_others_wrong="NCERT links the name only to the Rhesus monkey.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Leucocytes are nucleated and are relatively fewer in number than erythrocytes.",
     "Leucocytes are generally long-lived cells."),
  STATEMENT_PAIR, "C",
  "Features of leucocytes",
  "NCERT: leucocytes are also known as white blood cells as they are colourless due to the lack of haemoglobin. They "
  "are nucleated and are relatively lesser in number, averaging 6000–8000 per mm³ of blood (against 5–5.5 million "
  "RBCs per mm³). Leucocytes are generally short-lived.",
  ["Statement I → true", "Statement II → false (generally short-lived)"],
  R_BFC("blood: formed elements"),
  why_others_wrong="A and D call leucocytes long-lived; B rejects the true statement about their nucleus and number.",
  seconds=25)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Blood is the most commonly used body fluid for transport by most of the higher organisms, including humans.",
     "Erythrocytes, leucocytes and platelets are collectively called formed elements."),
  STATEMENT_PAIR, "A",
  "Blood and its formed elements",
  "NCERT: blood is the most commonly used body fluid by most of the higher organisms, including humans, for moving "
  "substances; lymph also helps in the transport of certain substances. Erythrocytes, leucocytes and platelets are "
  "collectively called formed elements.",
  ["Statement I → true", "Statement II → true"],
  R_BFC("blood"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=25)

Z(BFC, "Blood and blood groups", "Intermediate", "numerical",
  "A person has 5 L of blood. Plasma forms 55 per cent of the blood, and water makes up 90 per cent of the plasma. "
  "About how much water is present in the plasma of this person?",
  ["2750 mL", "2475 mL", "4500 mL", "2025 mL"], "B",
  "Composition of blood and plasma",
  "NCERT: plasma constitutes nearly 55 per cent of the blood, and water forms 90–92 per cent of plasma. Plasma = 55 % "
  "of 5000 mL = 2750 mL; water = 90 % of 2750 mL = 2475 mL.",
  ["Plasma = 0.55 × 5000 = 2750 mL", "Water = 0.90 × 2750 = 2475 mL"],
  R_BFC("blood: plasma"),
  shortcut="5000 × 0.55 × 0.9 = 2475 mL.",
  why_others_wrong="2750 mL is the whole plasma; 4500 mL takes 90 per cent of the whole blood; 2025 mL uses the 45 "
                   "per cent formed-element share instead of plasma.",
  seconds=45, verified_by=RECOMPUTED)

Z(BFC, "Blood and blood groups", "Intermediate", "assertion_reason",
  ar("An Rh+ve foetus of a sensitised Rh-ve mother may suffer severe anaemia and jaundice, which could even be fatal.",
     "The Rh antibodies of the mother can leak into the blood of the foetus and destroy the foetal RBCs."),
  ASSERTION_REASON, "A",
  "Erythroblastosis foetalis: how the foetus is harmed",
  "NCERT: in subsequent pregnancies, the Rh antibodies from the mother (Rh-ve) can leak into the blood of the foetus "
  "(Rh+ve) and destroy the foetal RBCs. This could be fatal to the foetus or could cause severe anaemia and jaundice "
  "to the baby. The destruction of foetal RBCs described in R is the cause of the effects in A.",
  ["A → true", "R → true", "Destruction of foetal RBCs → anaemia and jaundice → R explains A"],
  R_BFC("blood groups: Rh grouping"),
  why_others_wrong="B denies the causal chain NCERT gives; C and D call true statements false.",
  seconds=35)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "multi_statement",
  ms("Which of the following statements about the cardiac cycle are correct?",
     ["The SAN generates an action potential which stimulates both the atria to undergo a simultaneous contraction "
      "(atrial systole).",
      "The action potential is conducted to the ventricular side by the AVN and the AV bundle, from where the bundle "
      "of His transmits it through the entire ventricular musculature.",
      "During joint diastole, blood from the pulmonary veins and the vena cava flows into the left and the right "
      "ventricle respectively through the left and right atria.",
      "In each cycle, the ventricles contract before the atria."]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(a), (b) and (c) only"], "D",
  "Events of the cardiac cycle",
  "NCERT: in joint diastole the tricuspid and bicuspid valves are open, so blood from the pulmonary veins and vena "
  "cava flows into the left and right ventricles through the atria. The SAN then generates an action potential that "
  "makes both atria contract simultaneously; the impulse is conducted by the AVN and AV bundle and transmitted by the "
  "bundle of His through the ventricular musculature, causing ventricular systole. So the atria contract first.",
  ["(a) true", "(b) true", "(c) true", "(d) false – atrial systole precedes ventricular systole"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A omits the true statement (c); B and C include the false statement (d).",
  seconds=50)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "statement_pair",
  sp("The ECG is a graphical representation of the electrical activity of the heart during a cardiac cycle.",
     "Any deviation from the normal shape of the ECG indicates a possible abnormality or disease, so the ECG is of "
     "great clinical significance."),
  STATEMENT_PAIR, "A",
  "Electrocardiograph",
  "NCERT: the ECG is a graphical representation of the electrical activity of the heart during a cardiac cycle. Any "
  "deviation from the shape of this graph indicates a possible abnormality or disease; hence it is of great clinical "
  "significance.",
  ["Statement I → true", "Statement II → true"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

Z(BFC, "Blood and blood groups", "Intermediate", "multi_statement",
  ms("Which of the following statements about the ABO blood groups are correct?",
     ["ABO grouping is based on the presence or absence of two surface antigens, A and B, on the RBCs.",
      "The plasma of different individuals contains two natural antibodies.",
      "Antibodies are proteins produced in response to antigens.",
      "The RBCs of persons with blood group O carry both the A and the B antigens."]),
  ["(a), (b) and (d) only", "(a) and (b) only", "(a), (b) and (c) only", "(b), (c) and (d) only"], "C",
  "Basis of ABO grouping",
  "NCERT: ABO grouping is based on the presence or absence of two surface antigens (chemicals that can induce an "
  "immune response), A and B, on the RBCs. Similarly, the plasma of different individuals contains two natural "
  "antibodies (proteins produced in response to antigens). Group O RBCs carry neither antigen; it is group AB that "
  "carries both.",
  ["(a) true", "(b) true", "(c) true", "(d) false – group O has no A or B antigen"],
  R_BFC("blood groups: ABO grouping"),
  why_others_wrong="A and D include (d); B leaves out the true statement (c).",
  seconds=40)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "statement_pair",
  sp("During each cardiac cycle two prominent sounds are produced, which can be easily heard through a stethoscope.",
     "The heart sounds are produced by the contraction of the atrial muscles."),
  STATEMENT_PAIR, "C",
  "Heart sounds",
  "NCERT: during each cardiac cycle two prominent sounds are produced which can be easily heard through a "
  "stethoscope. The first sound (lub) is associated with the closure of the tricuspid and bicuspid valves, and the "
  "second (dub) with the closure of the semilunar valves – not with atrial contraction.",
  ["Statement I → true", "Statement II → false (sounds are linked to closure of valves)"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A and D link the sounds to atrial contraction; B rejects the true NCERT line about the stethoscope.",
  seconds=30)

Z(BFC, "Coagulation and lymph", "Intermediate", "direct",
  "A dark reddish-brown scum formed at the site of a cut or an injury over a period of time is:",
  ["A clot or coagulum, formed mainly of a network of fibrin threads in which dead and damaged formed elements are "
   "trapped",
   "A mass of lymph rich in lymphocytes",
   "Serum, which is plasma without the clotting factors",
   "A mass of fresh RBCs produced at the site by the bone marrow"], "A",
  "Coagulation of blood",
  "NCERT: you would have observed a dark reddish-brown scum formed at the site of a cut or an injury over a period of "
  "time. It is a clot or coagulum, formed mainly of a network of threads called fibrins in which dead and damaged "
  "formed elements of blood are trapped. This mechanism prevents excessive loss of blood.",
  ["Dark reddish-brown scum at an injury → clot (coagulum) of fibrin threads"],
  R_BFC("coagulation of blood"),
  why_others_wrong="Lymph is a colourless fluid; serum is a fluid, not a scum; RBCs are not produced at a wound.",
  seconds=30)

Z(BFC, "Blood and blood groups", "Advanced", "numerical",
  "A blood report shows a total WBC count of 7000 per mm³, with neutrophils 64.5 per cent, eosinophils 3 per cent, "
  "basophils 0.5 per cent, lymphocytes 25 per cent and monocytes 7 per cent. What is the total number of "
  "agranulocytes per mm³ of this blood?",
  ["1750", "4760", "490", "2240"], "D",
  "Granulocytes and agranulocytes",
  "NCERT: leucocytes are of two main categories – granulocytes (neutrophils, eosinophils, basophils) and "
  "agranulocytes (lymphocytes and monocytes). Agranulocytes = (25 + 7) % of 7000 = 32 % of 7000 = 2240 per mm³.",
  ["Agranulocytes → lymphocytes + monocytes = 25 % + 7 % = 32 %", "32 % of 7000 = 2240 per mm³"],
  R_BFC("blood: formed elements"),
  shortcut="7000 × 0.32 = 2240.",
  why_others_wrong="1750 counts only lymphocytes; 490 counts only monocytes; 4760 is the number of granulocytes (68 "
                   "per cent).",
  seconds=60, verified_by=RECOMPUTED)

Z(BFC, "Blood and blood groups", "Advanced", "direct",
  "A patient with blood group O, Rh-ve needs a blood transfusion. Considering both the ABO and the Rh systems, which "
  "donor's blood is the safe choice?",
  ["A, Rh-ve", "O, Rh+ve", "AB, Rh-ve", "O, Rh-ve"], "D",
  "Matching ABO and Rh groups in transfusion",
  "NCERT: a group O person has both anti-A and anti-B antibodies in the plasma and can receive blood only from group "
  "O. An Rh-ve person, if exposed to Rh+ve blood, will form specific antibodies against the Rh antigens, so Rh groups "
  "must also be matched. Only O, Rh-ve blood satisfies both conditions.",
  ["Recipient O → anti-A and anti-B present → donor must be O", "Recipient Rh-ve → donor must be Rh-ve",
   "→ O, Rh-ve"],
  R_BFC("blood groups"),
  why_others_wrong="A and C carry A and/or B antigens, which the recipient's anti-A/anti-B would attack; O, Rh+ve "
                   "would expose the Rh-ve recipient to Rh antigens.",
  seconds=45)

Z(BFC, "Blood and blood groups", "Advanced", "assertion_reason",
  ar("Erythroblastosis foetalis usually does not affect the first Rh+ve foetus of an Rh-ve mother.",
     "In the first pregnancy, the Rh antigens of the foetus do not get exposed to the Rh-ve blood of the mother, as "
     "the two bloods are well separated by the placenta."),
  ASSERTION_REASON, "A",
  "Why the first pregnancy is spared",
  "NCERT: the Rh antigens of the foetus do not get exposed to the Rh-ve blood of the mother in the first pregnancy, "
  "as the two bloods are well separated by the placenta. The mother is sensitised only at the delivery of the first "
  "child, so the antibodies that harm the foetus are made only for subsequent pregnancies. The separation in R is "
  "why the first foetus is usually spared.",
  ["A → true", "R → true", "No exposure in the first pregnancy → no antibodies yet → R explains A"],
  R_BFC("blood groups: Rh grouping"),
  why_others_wrong="B ignores the direct cause; C and D call true statements false.",
  seconds=40)

Z(BFC, "Human heart", "Advanced", "statement_pair",
  sp("The nodal musculature of the heart can generate action potentials without any external stimuli, i.e. it is "
     "autoexcitable.",
     "The number of action potentials that can be generated in a minute is the same in all parts of the nodal "
     "system."),
  STATEMENT_PAIR, "C",
  "Autoexcitability of nodal tissue",
  "NCERT: the nodal musculature has the ability to generate action potentials without any external stimuli, i.e. it "
  "is autoexcitable. However, the number of action potentials that could be generated in a minute varies at "
  "different parts of the nodal system; the SAN can generate the maximum (70–75 per minute) and therefore acts as the "
  "pacemaker.",
  ["Statement I → true", "Statement II → false (the rate varies; SAN is highest)"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="A and D accept equal rates in all nodal parts, which would leave no reason for the SAN to be the "
                   "pacemaker; B rejects the true NCERT line on autoexcitability.",
  seconds=40)

Z(BFC, "Human heart", "Advanced", "multi_statement",
  ms("Which of the following statements about the conducting system of the human heart are correct?",
     ["The atrio-ventricular bundle emerges on the top of the inter-ventricular septum and immediately divides into "
      "a right and a left bundle.",
      "The Purkinje fibres, along with the right and left bundles, are known as the bundle of His.",
      "The bundle of His lies in the wall of the right atrium.",
      "The atrio-ventricular bundle arises directly from the SAN, bypassing the AVN."]),
  ["(a), (b) and (c) only", "(a) and (b) only", "(b) and (d) only", "(a), (c) and (d) only"], "B",
  "Bundle of His",
  "NCERT: a bundle of nodal fibres, the atrio-ventricular bundle (AV bundle), continues from the AVN, passes through "
  "the atrio-ventricular septa to emerge on the top of the inter-ventricular septum, and immediately divides into a "
  "right and left bundle. These branches give rise to minute fibres throughout the ventricular musculature of the "
  "respective sides, the Purkinje fibres. These fibres along with the right and left bundles are known as the bundle "
  "of His – a ventricular, not atrial, structure.",
  ["(a) true", "(b) true", "(c) false – it runs in the ventricular musculature",
   "(d) false – the AV bundle continues from the AVN"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="A includes (c); C includes (d) and omits (a); D includes (c) and (d).",
  seconds=55)

# ================================================================ Excretory Products and their Elimination (B5 I6 A5)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "In crustaceans like prawns, the excretory structures called antennal glands are also known as:",
  ["Flame cells", "Malpighian tubules", "Green glands", "Nephridia"], "C",
  "Excretory structures of invertebrates",
  "NCERT: antennal glands or green glands perform the excretory function in crustaceans like prawns. Flame cells "
  "(protonephridia) occur in flatworms, nephridia in earthworms and Malpighian tubules in insects.",
  ["Prawn → antennal glands = green glands"],
  R_EXC("introduction (excretory structures in animals)"),
  why_others_wrong="Flame cells, Malpighian tubules and nephridia are different excretory structures of flatworms, "
                   "insects and annelids.",
  seconds=20)

Z(EXC, "Modes of excretion", "Basic", "assertion_reason",
  ar("In ammonotelic animals, the kidneys play a significant role in the removal of ammonia.",
     "Ammonia, being readily soluble, is generally excreted by diffusion across body surfaces or through gill "
     "surfaces (in fish) as ammonium ions."),
  ASSERTION_REASON, "D",
  "Removal of ammonia",
  "NCERT: ammonia, as it is readily soluble, is generally excreted by diffusion across body surfaces or through gill "
  "surfaces (in fish) as ammonium ions. Kidneys do not play any significant role in its removal. A is false; R is "
  "true.",
  ["A → false (kidneys play no significant role)", "R → true"],
  R_EXC("introduction (ammonotelism)"),
  why_others_wrong="A, B and C accept the assertion, but NCERT states that kidneys do not play any significant role "
                   "in ammonia removal.",
  seconds=30)

Z(EXC, "Urine formation", "Basic", "numerical",
  "NCERT states that a healthy adult excretes 1 to 1.5 L of urine and 25–30 g of urea per day. If a person excretes "
  "27 g of urea in 1.5 L of urine in a day, what is the average concentration of urea in the urine?",
  ["18 g per litre", "40.5 g per litre", "1.8 g per litre", "27 g per litre"], "A",
  "Composition of urine",
  "Concentration = mass of urea / volume of urine = 27 g / 1.5 L = 18 g per litre.",
  ["Concentration = 27 g ÷ 1.5 L", "= 18 g L⁻¹"],
  R_EXC("micturition (characteristics of urine)"),
  why_others_wrong="40.5 g multiplies instead of dividing; 1.8 g divides by 15 instead of 1.5; 27 g ignores the volume "
                   "of urine.",
  seconds=30, verified_by=RECOMPUTED)

Z(EXC, "Nephron structure", "Basic", "match_list",
  ml(("organ of the human excretory system", "role"),
     ["Kidneys", "Ureters", "Urinary bladder", "Urethra"],
     ["Stores urine until a voluntary signal is given by the CNS", "Carries urine out of the body",
      "Form urine", "Carry urine from the kidneys to the urinary bladder"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("I", "IV", "III", "II")], "B"),
  "B",
  "Human excretory system",
  "NCERT: the human excretory system consists of a pair of kidneys, one pair of ureters, a urinary bladder and a "
  "urethra. Urine formed by the nephrons of the kidneys is carried by the ureters to the urinary bladder, where it is "
  "stored till a voluntary signal is given by the CNS, and is released out through the urethra (micturition).",
  ["Kidneys → form urine (III)", "Ureters → kidneys to bladder (IV)", "Bladder → stores urine (I)",
   "Urethra → releases urine (II)"],
  R_EXC("human excretory system; micturition"),
  why_others_wrong="The other codes swap the kidneys with the ureters, the bladder with the urethra, or the kidneys "
                   "with the bladder.",
  seconds=25)

Z(EXC, "Modes of excretion", "Basic", "match_list",
  ml(("term", "meaning"),
     ["Ammonotelism", "Ureotelism", "Uricotelism", "Ketonuria"],
     ["Excretion of nitrogenous waste mainly as uric acid", "Presence of ketone bodies in urine",
      "Excretion of nitrogenous waste mainly as ammonia", "Excretion of nitrogenous waste mainly as urea"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "I", "IV", "II"), M("III", "IV", "II", "I")], "A"),
  "A",
  "Terms related to excretion",
  "NCERT: the process of excreting ammonia is ammonotelism, of urea ureotelism and of uric acid uricotelism. The "
  "presence of ketone bodies in urine is ketonuria, which with glycosuria indicates diabetes mellitus.",
  ["Ammonotelism → ammonia (III)", "Ureotelism → urea (IV)", "Uricotelism → uric acid (I)",
   "Ketonuria → ketone bodies (II)"],
  R_EXC("introduction; micturition"),
  why_others_wrong="The other codes interchange urea and ammonia, urea and uric acid, or uric acid and ketone bodies.",
  seconds=25)

Z(EXC, "Modes of excretion", "Intermediate", "direct",
  "Besides many bony fishes, which of the following does NCERT cite as ammonotelic animals?",
  ["Aquatic amphibians and aquatic insects", "Land snails and reptiles", "Marine fishes and mammals",
   "Birds and insects living on land"], "A",
  "Ammonotelic animals",
  "NCERT: many bony fishes, aquatic amphibians and aquatic insects are ammonotelic in nature. Mammals, many "
  "terrestrial amphibians and marine fishes are ureotelic; reptiles, birds, land snails and insects are uricotelic.",
  ["Ammonotelic → bony fishes, aquatic amphibians, aquatic insects"],
  R_EXC("introduction (ammonotelism)"),
  why_others_wrong="Land snails, reptiles and birds are uricotelic; marine fishes and mammals are ureotelic.",
  seconds=25)

Z(EXC, "Modes of excretion", "Intermediate", "multi_statement",
  ms("Which of the following statements about excretory structures are correct?",
     ["Most invertebrates have simple tubular excretory structures, whereas vertebrates have complex tubular organs "
      "called kidneys.",
      "Nephridia help earthworms and other annelids to remove nitrogenous wastes and maintain fluid and ionic balance.",
      "Malpighian tubules help most insects in the removal of nitrogenous wastes and in osmoregulation.",
      "Antennal glands are the excretory structures of insects such as cockroaches.",
      "Flame cells are the excretory structures of earthworms."]),
  ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a) and (c) only"], "C",
  "Excretory structures across the animal kingdom",
  "NCERT: animals have simple tubular forms (most invertebrates) or complex tubular organs called kidneys "
  "(vertebrates). Nephridia of earthworms and other annelids remove nitrogenous wastes and maintain fluid and ionic "
  "balance; Malpighian tubules of most insects including cockroaches remove nitrogenous wastes and help in "
  "osmoregulation. Antennal (green) glands are found in crustaceans like prawns, and flame cells (protonephridia) in "
  "flatworms.",
  ["(a) true", "(b) true", "(c) true", "(d) false – antennal glands occur in crustaceans",
   "(e) false – flame cells occur in flatworms"],
  R_EXC("introduction (excretory structures)"),
  why_others_wrong="A includes (d); B includes (e) and omits (a); D omits the true statement (b).",
  seconds=45)

Z(EXC, "Nephron structure", "Intermediate", "direct",
  "Which sequence correctly traces the path of the glomerular filtrate in a human nephron until it leaves the "
  "kidney?",
  ["Bowman's capsule → DCT → Henle's loop → PCT → collecting duct → renal pelvis",
   "Bowman's capsule → PCT → collecting duct → Henle's loop → DCT → renal pelvis",
   "Bowman's capsule → Henle's loop → PCT → DCT → renal pelvis → collecting duct",
   "Bowman's capsule → PCT → Henle's loop → DCT → collecting duct → renal pelvis"], "D",
  "Course of the renal tubule",
  "NCERT: the renal tubule begins with the double-walled Bowman's capsule, continues as the highly coiled PCT, then "
  "the hairpin-shaped Henle's loop (descending and ascending limbs), which continues as the highly coiled DCT. The "
  "DCTs of many nephrons open into a straight collecting duct; many collecting ducts converge and open into the renal "
  "pelvis through the medullary pyramids in the calyces.",
  ["Bowman's capsule → PCT → Henle's loop → DCT → collecting duct → renal pelvis"],
  R_EXC("human excretory system (nephron)"),
  why_others_wrong="A reverses the PCT and DCT; B places the collecting duct before Henle's loop; C skips from the "
                   "capsule to Henle's loop and puts the pelvis before the collecting duct.",
  seconds=35)

Z(EXC, "Urine formation", "Intermediate", "direct",
  "In a patient, substantial amounts of plasma proteins are found in the glomerular filtrate. The structure most "
  "likely to be damaged is the:",
  ["Filtration membrane of the glomerulus (endothelium, basement membrane and epithelium of Bowman's capsule)",
   "Brush border of the proximal convoluted tubule",
   "Ascending limb of Henle's loop",
   "Collecting duct"], "A",
  "Glomerular filtration barrier",
  "NCERT: blood is filtered through three layers – the endothelium of the glomerular blood vessels, the epithelium of "
  "Bowman's capsule (with podocytes leaving filtration slits) and a basement membrane between them. The filtration is "
  "so fine that almost all constituents of plasma except the proteins pass into the lumen of Bowman's capsule. "
  "Proteins in the filtrate point to damage of this barrier, which lies before the tubule.",
  ["Proteins are normally held back at filtration", "Protein in the filtrate → filtration membrane damaged"],
  R_EXC("urine formation (glomerular filtration)"),
  why_others_wrong="The PCT, Henle's loop and collecting duct act on the filtrate only after it has formed; they "
                   "cannot let proteins into Bowman's capsule.",
  seconds=40)

Z(EXC, "Disorders and dialysis", "Intermediate", "statement_pair",
  sp("Accumulation of urea in the blood (uremia) is highly harmful and may lead to kidney failure.",
     "In patients with uremia, urea can be removed from the blood by a process called haemodialysis."),
  STATEMENT_PAIR, "A",
  "Uremia and haemodialysis",
  "NCERT: malfunctioning of the kidneys can lead to the accumulation of urea in the blood, a condition called uremia, "
  "which is highly harmful and may lead to kidney failure. In such patients, urea can be removed by a process called "
  "haemodialysis, which is a boon for thousands of uremic patients all over the world.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("disorders of the excretory system"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

Z(EXC, "Regulation of kidney function", "Intermediate", "multi_statement",
  ms("A healthy person drinks a large volume of water in a short time. Which of the following responses are expected?",
     ["The rise in body fluid volume switches off the osmoreceptors.",
      "Release of ADH from the neurohypophysis is suppressed.",
      "Less water is reabsorbed from the latter parts of the tubule, so a larger volume of dilute urine is formed.",
      "The JG cells release more renin.",
      "Aldosterone secretion rises and more Na⁺ is reabsorbed from the distal parts of the tubule."]),
  ["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(b) and (c) only", "(a), (b) and (c) only"], "D",
  "Regulation by ADH in excess water intake",
  "NCERT: osmoreceptors respond to changes in blood volume, body fluid volume and ionic concentration. An increase in "
  "body fluid volume can switch off the osmoreceptors and suppress ADH release, completing the feedback. ADH "
  "normally facilitates water reabsorption from the latter parts of the tubule, so with less ADH more dilute urine "
  "is passed. Renin and aldosterone respond to a fall in glomerular blood flow or GFR, which is not the situation "
  "here.",
  ["(a) true", "(b) true", "(c) true", "(d) false – renin is released when GFR falls",
   "(e) false – not triggered by excess water"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A includes (d); B includes (d) and (e); C omits the first step (a) of the response.",
  seconds=55)

Z(EXC, "Nephron structure", "Advanced", "numerical",
  "The GFR of a healthy person is 125 mL per minute. Each kidney has nearly one million nephrons; take exactly "
  "10⁶ nephrons per kidney and assume all nephrons filter equally. About how much filtrate does one nephron form per "
  "minute? (1 mL = 10⁶ nL)",
  ["125 nL", "6.25 nL", "62.5 nL", "62.5 µL"], "C",
  "GFR and number of nephrons",
  "NCERT: GFR in a healthy individual is approximately 125 mL per minute, and each kidney has nearly one million "
  "nephrons. Two kidneys → 2 × 10⁶ nephrons. Filtrate per nephron = 125 mL ÷ (2 × 10⁶) = 125 × 10⁶ nL ÷ (2 × 10⁶) "
  "= 62.5 nL per minute.",
  ["Total nephrons = 2 × 10⁶", "125 mL = 1.25 × 10⁸ nL", "1.25 × 10⁸ ÷ 2 × 10⁶ = 62.5 nL per minute"],
  R_EXC("human excretory system; urine formation"),
  why_others_wrong="125 nL counts the nephrons of only one kidney; 6.25 nL is a slip of a power of ten; 62.5 µL "
                   "confuses nanolitres with microlitres (1000 times too large).",
  seconds=75, verified_by=RECOMPUTED)

Z(EXC, "Regulation of kidney function", "Advanced", "multi_statement",
  ms("After a severe loss of blood, a person's blood pressure and GFR fall. Which of the following responses are "
     "expected according to the regulatory mechanisms described in NCERT?",
     ["The JG cells release renin.",
      "Angiotensin II constricts blood vessels, raising the glomerular blood pressure and thereby the GFR.",
      "Aldosterone causes reabsorption of Na⁺ and water from the distal parts of the tubule.",
      "ANF release increases and causes vasodilation."]),
  ["(a), (b), (c) and (d)", "(a), (b) and (c) only", "(a) and (d) only", "(b), (c) and (d) only"], "B",
  "Responses to a fall in blood pressure",
  "NCERT: a fall in glomerular blood flow, glomerular blood pressure or GFR activates the JG cells to release renin, "
  "which converts angiotensinogen to angiotensin I and II. Angiotensin II, a powerful vasoconstrictor, raises the "
  "glomerular blood pressure and GFR, and activates the adrenal cortex to release aldosterone, which causes "
  "reabsorption of Na⁺ and water from the distal tubule, raising BP and GFR. ANF is released when blood flow to the "
  "atria increases and causes vasodilation – the opposite of what is needed after blood loss.",
  ["(a) true", "(b) true", "(c) true", "(d) false – ANF is a check on this mechanism, released on increased atrial "
   "blood flow"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A, C and D include (d); C also leaves out (b) and (c).",
  seconds=60)

Z(EXC, "Urine formation", "Advanced", "direct",
  "Damage to which of the following would most directly impair the ability of the human kidney to produce "
  "concentrated urine?",
  ["The podocytes of Bowman's capsule", "The brush border of the PCT",
   "Henle's loop and the vasa recta", "The urinary bladder"], "C",
  "Counter-current mechanism",
  "NCERT: mammals have the ability to produce concentrated urine; Henle's loop and the vasa recta play a significant "
  "role in this. The flow in their two limbs is counter-current, which maintains an increasing osmolarity towards the "
  "inner medulla (300 to about 1200 mOsmol L⁻¹); this gradient allows water to be reabsorbed from the collecting "
  "tubule to concentrate the filtrate.",
  ["Concentrated urine depends on the medullary osmotic gradient",
   "Gradient is built and kept by Henle's loop and vasa recta"],
  R_EXC("mechanism of concentration of the filtrate"),
  why_others_wrong="Podocytes form filtration slits; the PCT brush border reabsorbs most nutrients, electrolytes and "
                   "water; the bladder only stores urine – none of these builds the medullary gradient.",
  seconds=40)

Z(EXC, "Regulation of kidney function", "Advanced", "assertion_reason",
  ar("If the latter parts of the renal tubule (DCT and collecting duct) stop responding to ADH, a large volume of "
     "dilute urine will be passed.",
     "ADH facilitates water reabsorption from the latter parts of the tubule, thereby preventing diuresis."),
  ASSERTION_REASON, "A",
  "Action of ADH",
  "NCERT: ADH (vasopressin) facilitates water reabsorption from the latter parts of the tubule, thereby preventing "
  "diuresis. If these parts cannot respond to ADH, this water is not reabsorbed and excess dilute urine is "
  "passed. R gives the very mechanism whose failure produces A.",
  ["A → true (no ADH action → less water reabsorbed)", "R → true", "Loss of ADH action → diuresis → R explains A"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="B ignores that A follows directly from the role in R; C and D call true statements false.",
  seconds=40)

Z(EXC, "Urine formation", "Advanced", "direct",
  "In a juxtamedullary nephron, how does the filtrate at the hairpin bend of Henle's loop (deep in the medulla) "
  "compare with the filtrate that has just passed up the ascending limb?",
  ["Both are isotonic to plasma",
   "Filtrate at the bend is dilute, and filtrate after the ascending limb is more concentrated",
   "Filtrate after the ascending limb is still more concentrated than at the bend",
   "Filtrate at the bend is highly concentrated, and it gets diluted as it passes up the ascending limb"], "D",
  "Changes in the filtrate along Henle's loop",
  "NCERT: the descending limb is permeable to water but almost impermeable to electrolytes, so the filtrate gets "
  "concentrated as it moves down towards the inner medulla, where the interstitium reaches about 1200 mOsmol L⁻¹. The "
  "ascending limb is impermeable to water but allows transport of electrolytes to the medullary fluid, so the "
  "concentrated filtrate gets diluted as it moves up.",
  ["Descending limb: water leaves → filtrate concentrated at the bend",
   "Ascending limb: electrolytes leave, water cannot → filtrate diluted"],
  R_EXC("function of the tubules; mechanism of concentration of the filtrate"),
  why_others_wrong="A ignores the medullary gradient; B reverses the changes; C forgets that the ascending limb "
                   "removes electrolytes without water.",
  seconds=50)

# ================================================================ Locomotion and Movement (B4 I6 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Types of movement", "Basic", "direct",
  "Amoeboid movement is effected by pseudopodia formed by the streaming of protoplasm. According to NCERT, which "
  "cytoskeletal elements are also involved in amoeboid movement?",
  ["Myosin heads", "Microfilaments", "Cilia", "Intercalated discs"], "B",
  "Amoeboid movement",
  "NCERT: some specialised cells in our body like macrophages and leucocytes in blood exhibit amoeboid movement. It is "
  "effected by pseudopodia formed by the streaming of protoplasm (as in Amoeba). Cytoskeletal elements like "
  "microfilaments are also involved in amoeboid movement.",
  ["Amoeboid movement → pseudopodia + microfilaments"],
  R_LOC("types of movement"),
  why_others_wrong="Myosin heads form cross bridges in muscle; cilia bring about ciliary movement; intercalated discs "
                   "are junctions of cardiac muscle.",
  seconds=20)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "In a myofibril, the actin filaments are called thin filaments because:",
  ["They contain the protein myoglobin", "They are made of meromyosin monomers",
   "They are thinner compared with the myosin filaments", "They form the dark A-band"], "C",
  "Thin and thick filaments",
  "NCERT: the actin filaments are thinner as compared to the myosin filaments, hence they are commonly called thin "
  "filaments and thick filaments respectively.",
  ["Actin thinner than myosin → thin filaments; myosin → thick filaments"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="Myoglobin is an oxygen-storing pigment, meromyosins build the thick (myosin) filament, and the "
                   "dark A-band contains myosin.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "match_list",
  ml(("bones", "number"),
     ["Carpals in one wrist", "Metacarpals in one palm", "Phalanges in one hand", "Coxal bones in the pelvic girdle"],
     ["14", "2", "8", "5"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("III", "I", "IV", "II")], "B"),
  "B",
  "Bones of the hand and the pelvic girdle",
  "NCERT: each fore limb has carpals (wrist bones – 8 in number), metacarpals (palm bones – 5 in number) and "
  "phalanges (digits – 14 in number). The pelvic girdle consists of two coxal bones.",
  ["Carpals → 8 (III)", "Metacarpals → 5 (IV)", "Phalanges → 14 (I)", "Coxal bones → 2 (II)"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="The other codes swap the carpal and metacarpal counts, the phalanges and coxal bones, or the "
                   "metacarpal and phalanx counts.",
  seconds=25)

Z(LOC, "Muscular and skeletal disorders", "Basic", "direct",
  "Myasthenia gravis is an auto-immune disorder affecting the neuromuscular junction. According to NCERT, it leads to:",
  ["Rapid spasms (wild contractions) in muscle due to low Ca²⁺ in body fluids",
   "Inflammation of joints",
   "Decreased bone mass and increased chances of fractures",
   "Fatigue, weakening and paralysis of skeletal muscle"], "D",
  "Myasthenia gravis",
  "NCERT: myasthenia gravis is an auto-immune disorder affecting the neuromuscular junction, leading to fatigue, "
  "weakening and paralysis of skeletal muscle.",
  ["Myasthenia gravis → fatigue, weakening and paralysis of skeletal muscle"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="Rapid spasms due to low Ca²⁺ describe tetany, inflammation of joints is arthritis, and decreased "
                   "bone mass is osteoporosis.",
  seconds=20)

Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "Each human foot has 7 tarsals, 5 metatarsals and 14 phalanges. How many metatarsals and phalanges are there in "
  "total in both feet?",
  ["19", "38", "52", "33"], "B",
  "Bones of the foot",
  "NCERT: each hind limb has tarsals (ankle bones – 7), metatarsals (5) and phalanges (digits – 14). Metatarsals + "
  "phalanges per foot = 5 + 14 = 19; for both feet = 2 × 19 = 38.",
  ["Per foot: 5 + 14 = 19", "Both feet: 2 × 19 = 38"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="19 counts one foot only; 52 wrongly adds the tarsals as well (2 × 26); 33 doubles only the "
                   "phalanges.",
  seconds=40, verified_by=RECOMPUTED)

Z(LOC, "Muscle contraction", "Intermediate", "statement_pair",
  sp("White muscle fibres possess very little myoglobin and therefore appear pale or whitish.",
     "White muscle fibres have few mitochondria but a high amount of sarcoplasmic reticulum."),
  STATEMENT_PAIR, "A",
  "White muscle fibres",
  "NCERT: some muscles possess very little myoglobin and therefore appear pale or whitish; these are the white "
  "fibres. The number of mitochondria is also few in them, but the amount of sarcoplasmic reticulum is high. They "
  "depend on anaerobic processes for energy.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("mechanism of muscle contraction (red and white fibres)"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=30)

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("Some skeletal muscles have a red appearance.",
     "These muscles possess a high quantity of myoglobin, a red-coloured oxygen-storing pigment."),
  ASSERTION_REASON, "A",
  "Red muscle fibres",
  "NCERT: myoglobin is a red-coloured oxygen-storing pigment. Some muscles possess a high quantity of myoglobin, "
  "which gives them a reddish appearance; such muscles are called red fibres. The pigment in R is the cause of the "
  "colour in A.",
  ["A → true", "R → true", "Red pigment myoglobin in high amount → red appearance → R explains A"],
  R_LOC("mechanism of muscle contraction (red and white fibres)"),
  why_others_wrong="B denies the obvious pigment–colour link; C and D call true statements false.",
  seconds=30)

Z(LOC, "Types of movement", "Intermediate", "multi_statement",
  ms("Which of the following statements are correct according to NCERT?",
     ["Locomotion requires a perfectly coordinated activity of the muscular, skeletal and neural systems.",
      "Movement of the limbs, jaws, tongue, etc. requires muscular movement.",
      "The contractile property of muscles is effectively used for locomotion and other movements by human beings "
      "and the majority of multicellular organisms.",
      "Locomotion can take place without any role of the neural system."]),
  ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (b), (c) and (d)"], "C",
  "Muscular movement and locomotion",
  "NCERT: movement of our limbs, jaws, tongue, etc. requires muscular movement. The contractile property of muscles "
  "is effectively used for locomotion and other movements by human beings and the majority of multicellular "
  "organisms. Locomotion requires a perfect coordinated activity of muscular, skeletal and neural systems, so it "
  "cannot occur without the neural system.",
  ["(a) true", "(b) true", "(c) true", "(d) false – the neural system is essential"],
  R_LOC("types of movement"),
  why_others_wrong="A omits the true statement (c); B and D include (d).",
  seconds=40)

Z(LOC, "Skeletal system", "Intermediate", "match_list",
  ml(("bone(s) of the fore limb", "bone(s) occupying the corresponding position in the hind limb"),
     ["Humerus", "Radius and ulna", "Carpals", "Metacarpals"],
     ["Metatarsals", "Tarsals", "Tibia and fibula", "Femur"]),
  match_options(M("IV", "III", "II", "I"),
                [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"), M("IV", "III", "I", "II")], "D"),
  "D",
  "Comparing the bones of the limbs",
  "NCERT lists the bones of each fore limb as humerus, radius and ulna, carpals (wrist bones), metacarpals (palm "
  "bones) and phalanges, and of each hind limb as femur (thigh bone), tibia and fibula, tarsals (ankle bones), "
  "metatarsals, phalanges and patella. Taken in the same order: humerus ↔ femur, radius and ulna ↔ tibia and "
  "fibula, carpals ↔ tarsals, metacarpals ↔ metatarsals.",
  ["Humerus → femur (IV)", "Radius and ulna → tibia and fibula (III)", "Carpals → tarsals (II)",
   "Metacarpals → metatarsals (I)"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="The other codes swap the wrist and leg bones, the upper-arm and leg bones, or the wrist and palm "
                   "equivalents.",
  seconds=40)

Z(LOC, "Muscle contraction", "Intermediate", "direct",
  "According to NCERT, skeletal muscles are primarily involved in:",
  ["The transportation of food through the digestive tract",
   "Locomotory actions and changes of body postures",
   "Pumping blood through the blood vessels",
   "Removing dust particles from the trachea"], "B",
  "Role of skeletal muscle",
  "NCERT: skeletal muscles are closely associated with the skeletal components of the body; they have a striped "
  "appearance and are primarily involved in locomotory actions and changes of body postures. Visceral (smooth) "
  "muscles move food and gametes, cardiac muscle pumps blood, and cilia of the trachea remove dust.",
  ["Skeletal muscle → locomotion and changes of posture"],
  R_LOC("muscle"),
  why_others_wrong="Transport of food is by visceral muscles, pumping blood by cardiac muscle and removal of dust by "
                   "ciliary movement.",
  seconds=25)

Z(LOC, "Muscle contraction", "Advanced", "direct",
  "A muscle fibre is found to have very little myoglobin, few mitochondria and a large amount of sarcoplasmic "
  "reticulum. Which description of this fibre is correct?",
  ["A red fibre that depends mainly on aerobic ATP production",
   "A white fibre that depends on anaerobic processes for energy",
   "A red fibre that depends on anaerobic processes for energy",
   "A white fibre that uses large amounts of oxygen stored in it"], "B",
  "Identifying red and white fibres",
  "NCERT: muscles with very little myoglobin appear pale or whitish (white fibres); they have few mitochondria but a "
  "high amount of sarcoplasmic reticulum, and depend on anaerobic processes for energy. Red fibres, with plenty of "
  "myoglobin and mitochondria, use the large amount of stored oxygen for ATP production and are called aerobic "
  "muscles.",
  ["Little myoglobin → pale → white fibre", "Few mitochondria → anaerobic energy"],
  R_LOC("mechanism of muscle contraction (red and white fibres)"),
  why_others_wrong="Red fibres have much myoglobin and many mitochondria; a fibre with little myoglobin cannot store "
                   "much oxygen.",
  seconds=40)

Z(LOC, "Skeletal system", "Advanced", "statement_pair",
  sp("Each hind limb consists of the femur, tibia and fibula, tarsals, metatarsals, phalanges and a cup-shaped "
     "patella.",
     "The tarsals are eight in number in each foot."),
  STATEMENT_PAIR, "C",
  "Bones of the hind limb",
  "NCERT: the bones of each leg are the femur (thigh bone, the longest bone), tibia and fibula, tarsals (ankle bones – "
  "7 in number), metatarsals (5) and phalanges (digits – 14); a cup-shaped bone called patella covers the knee "
  "ventrally. Eight is the number of carpals in the wrist, not of tarsals.",
  ["Statement I → true", "Statement II → false (tarsals are 7; carpals are 8)"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="A and D confuse the 7 tarsals with the 8 carpals; B rejects the correct list of hind-limb bones.",
  seconds=35)

Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("Which of the following statements about the structure of skeletal muscle are correct?",
     ["In a myofibril, actin and myosin are arranged as rod-like structures, parallel to each other and to the "
      "longitudinal axis of the myofibril.",
      "A skeletal muscle fibre is a syncitium, as its sarcoplasm contains many nuclei.",
      "In a resting sarcomere, the thin filaments are firmly attached to the M-line.",
      "The A-band is called the isotropic band."]),
  ["(a), (b) and (c) only", "(b) and (d) only", "(a) and (c) only", "(a) and (b) only"], "D",
  "Organisation of a skeletal muscle fibre",
  "NCERT: each muscle fibre is lined by the sarcolemma enclosing the sarcoplasm; the fibre is a syncitium because "
  "the sarcoplasm contains many nuclei. Actin and myosin are arranged as rod-like structures, parallel to each other "
  "and to the longitudinal axis of the myofibrils. Thin filaments are firmly attached to the Z-line, while the M-line "
  "holds the thick filaments together. The dark A-band is anisotropic; the light I-band is isotropic.",
  ["(a) true", "(b) true", "(c) false – thin filaments attach to the Z-line", "(d) false – A-band is anisotropic"],
  R_LOC("skeletal muscle"),
  why_others_wrong="A includes (c); B includes (d) and leaves out (a); C includes (c) and leaves out (b).",
  seconds=50)

Z(LOC, "Types of movement", "Advanced", "assertion_reason",
  ar("Skeletal muscles assist in the transportation of food through the digestive tract.",
     "Visceral muscles assist in the transportation of food through the digestive tract and of gametes through the "
     "genital tract."),
  ASSERTION_REASON, "D",
  "Skeletal versus visceral muscle",
  "NCERT: visceral muscles, located in the inner walls of hollow visceral organs, are smooth and involuntary, and "
  "assist, for example, in the transportation of food through the digestive tract and gametes through the genital "
  "tract. Skeletal muscles are primarily involved in locomotory actions and changes of body posture. A is false; R "
  "is true.",
  ["A → false (food is moved by visceral muscles)", "R → true"],
  R_LOC("muscle"),
  why_others_wrong="A, B and C treat the assertion as true, giving skeletal muscle a role NCERT assigns to visceral "
                   "muscle.",
  seconds=35)

# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "According to NCERT, the neural system provides:",
  ["Chemical integration through hormones", "An organised network of point-to-point connections for a quick "
   "coordination", "Slow coordination that acts only through the blood", "Only the processing of vision and hearing"],
  "B",
  "Role of the neural system",
  "NCERT: the neural system provides an organised network of point-to-point connections for a quick coordination. "
  "The endocrine system provides chemical integration through hormones.",
  ["Neural system → point-to-point network → quick coordination"],
  R_NEU("introduction; neural system"),
  why_others_wrong="Chemical integration through hormones is the role of the endocrine system; the neural system is "
                   "quick, not slow, and does far more than process vision and hearing.",
  seconds=20)

Z(NEU, "Nerve impulse generation and conduction", "Basic", "direct",
  "Different types of ion channels are present on the neural membrane. According to NCERT, these ion channels are:",
  ["Freely permeable to all ions at all times", "Selectively permeable to different ions",
   "Permeable only to proteins", "Absent from the membrane of a resting neuron"], "B",
  "Ion channels of the neural membrane",
  "NCERT: neurons are excitable cells because their membranes are in a polarised state. Different types of ion "
  "channels are present on the neural membrane, and these ion channels are selectively permeable to different ions.",
  ["Ion channels → selectively permeable to different ions"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="The channels are selective, not freely permeable; the resting membrane is impermeable to the "
                   "negatively charged proteins of the axoplasm; the channels are present at rest too.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "statement_pair",
  sp("The neural system and the endocrine system jointly coordinate and integrate all the activities of the organs so "
     "that they function in a synchronised fashion.",
     "Coordination is the process through which two or more organs interact and complement the functions of one "
     "another."),
  STATEMENT_PAIR, "A",
  "Coordination and integration",
  "NCERT: coordination is the process through which two or more organs interact and complement the functions of one "
  "another. In our body, the neural system and the endocrine system jointly coordinate and integrate all the "
  "activities of the organs so that they function in a synchronised fashion.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("introduction"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "During physical exercise, the energy demand for increased muscular activity rises. According to NCERT, the "
  "increased supply of oxygen needed is met by a coordinated:",
  ["Decrease in heart rate and increase in rate of respiration",
   "Reduction of blood flow to the muscles",
   "Increase in the rate of respiration, heart beat and blood flow via the blood vessels",
   "Stoppage of kidney function until the exercise ends"], "C",
  "Example of coordination",
  "NCERT: when we do physical exercise, the energy demand increases for maintaining increased muscular activity, and "
  "the supply of oxygen also increases, necessitating an increase in the rate of respiration, heart beat and "
  "increased blood flow via blood vessels. When the exercise stops, the activities of nerves, lungs, heart and kidney "
  "gradually return to normal.",
  ["More O₂ needed → faster respiration + faster heart beat + more blood flow"],
  R_NEU("introduction"),
  why_others_wrong="The heart rate rises, not falls; blood flow to the muscles increases; NCERT describes the kidneys "
                   "returning to normal after exercise, not stopping.",
  seconds=25)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("A nerve impulse, once generated at a site, is conducted along the length of the axon.",
     "The impulse at one site causes a reversal of polarity at the adjacent site, and this sequence is repeated along "
     "the length of the axon."),
  ASSERTION_REASON, "A",
  "Conduction of a nerve impulse",
  "NCERT: current flow between the stimulated site and the next site reverses the polarity at the next site, so the "
  "action potential is generated there; the impulse at site A arrives at site B. The sequence is repeated along the "
  "length of the axon and consequently the impulse is conducted. R is the mechanism of A.",
  ["A → true", "R → true", "Repeated reversal of polarity at successive sites → conduction → R explains A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="B denies the mechanism NCERT gives; C and D call true statements false.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Intermediate", "assertion_reason",
  ar("The cerebral cortex is referred to as the grey matter.",
     "The neuron cell bodies are concentrated in the cerebral cortex, giving it its greyish colour."),
  ASSERTION_REASON, "A",
  "Grey matter of the cerebrum",
  "NCERT: the layer of cells covering the cerebral hemispheres is the cerebral cortex. It is referred to as the grey "
  "matter due to its greyish appearance; the neuron cell bodies are concentrated here, giving the colour. So R "
  "explains A.",
  ["A → true", "R → true", "Cell bodies concentrated → grey colour → R explains A"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="B denies the cause NCERT states; C and D call true statements false.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "direct",
  "Which sequence correctly describes transmission of an impulse across a chemical synapse?",
  ["Neurotransmitters bind receptors on the pre-synaptic membrane → synaptic vesicles fuse with the post-synaptic "
   "membrane → new potential in the pre-synaptic neuron",
   "Ion channels open on the post-synaptic membrane → impulse arrives at the axon terminal → synaptic vesicles release "
   "neurotransmitters",
   "Electrical current flows directly from the pre-synaptic to the post-synaptic membrane → neurotransmitters are "
   "released afterwards",
   "Impulse arrives at the axon terminal → synaptic vesicles move to and fuse with the plasma membrane → "
   "neurotransmitters are released into the synaptic cleft → they bind specific receptors on the post-synaptic "
   "membrane → ion channels open and a new potential may be generated"], "D",
  "Steps at a chemical synapse",
  "NCERT: when an impulse arrives at the axon terminal, it stimulates the movement of synaptic vesicles towards the "
  "membrane, where they fuse with the plasma membrane and release their neurotransmitters into the synaptic cleft. "
  "The neurotransmitters bind to specific receptors on the post-synaptic membrane; this opens ion channels, allowing "
  "the entry of ions which can generate a new potential in the post-synaptic neuron.",
  ["Arrival of impulse → vesicles fuse → release into cleft → binding to post-synaptic receptors → ion channels open "
   "→ new potential"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A places receptors on the pre-synaptic side; B starts with channel opening before the impulse "
                   "arrives; C describes an electrical synapse.",
  seconds=40)

Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human brain are correct?",
     ["The brain controls voluntary movements.", "The brain controls the balance of the body.",
      "The brain controls human behaviour.",
      "Vision, hearing and speech are processed in the spinal cord rather than in the brain."]),
  ["(a), (b), (c) and (d)", "(a), (b) and (c) only", "(a) and (d) only", "(b) and (c) only"], "B",
  "Functions of the brain",
  "NCERT: the brain controls voluntary movements, balance of the body, functioning of vital involuntary organs, "
  "thermoregulation, hunger and thirst, circadian rhythms, the activities of several endocrine glands and human "
  "behaviour. It is also the site for processing of vision, hearing, speech, memory, intelligence, emotions and "
  "thoughts – the brain, not the spinal cord.",
  ["(a) true", "(b) true", "(c) true", "(d) false – these are processed in the brain"],
  R_NEU("central neural system"),
  why_others_wrong="A and C include (d); D leaves out the true statement (a).",
  seconds=40)

Z(NEU, "Nervous system divisions", "Intermediate", "statement_pair",
  sp("Along with the hypothalamus, the limbic system is involved in the expression of emotional reactions such as "
     "excitement, pleasure, rage and fear.",
     "The limbic system is formed by the corpus callosum and the corpora quadrigemina."),
  STATEMENT_PAIR, "C",
  "Limbic system",
  "NCERT: the inner parts of the cerebral hemispheres and a group of associated deep structures like the amygdala and "
  "hippocampus form the limbic lobe or limbic system. Along with the hypothalamus, it is involved in the regulation of "
  "sexual behaviour, expression of emotional reactions (e.g. excitement, pleasure, rage and fear) and motivation. The "
  "corpus callosum is a tract connecting the two hemispheres, and the corpora quadrigemina are swellings of the "
  "midbrain.",
  ["Statement I → true", "Statement II → false (amygdala, hippocampus and inner parts of the hemispheres)"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="A and D accept a wrong composition of the limbic system; B rejects its NCERT functions.",
  seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "multi_statement",
  ms("A drug prevents the axonal membrane from becoming permeable to Na⁺ when it is stimulated, but does not affect "
     "the resting membrane. Which of the following would be expected?",
     ["The resting potential of the axon can still exist.",
      "On stimulation, the rapid influx of Na⁺ cannot occur.",
      "The inner surface at the stimulated site does not become positively charged, so no action potential arises.",
      "The membrane at the stimulated site undergoes a reversal of polarity as usual."]),
  ["(a) and (d) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(c) only"], "B",
  "Role of Na⁺ influx in the action potential",
  "NCERT: the resting potential depends on the ionic gradients maintained by the sodium–potassium pump and on the "
  "resting membrane being more permeable to K⁺ and nearly impermeable to Na⁺, so it is unaffected. When a stimulus "
  "is applied, the membrane normally becomes freely permeable to Na⁺, leading to a rapid influx of Na⁺ and a "
  "reversal of polarity (inner surface positive) – the action potential. Without that rise in Na⁺ permeability, no "
  "influx, no reversal and no action potential occur.",
  ["(a) true – resting state untouched", "(b) true", "(c) true", "(d) false – reversal needs Na⁺ influx"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A and C include (d); D leaves out the true statements (a) and (b).",
  seconds=60)

Z(NEU, "Neuron and nerves", "Advanced", "direct",
  "An injury destroys all the afferent nerve fibres coming from a limb but leaves its efferent nerve fibres intact. "
  "Which outcome is expected?",
  ["Neither impulses from the limb to the CNS nor regulatory impulses from the CNS to the limb can pass",
   "Impulses from the limb reach the CNS, but regulatory impulses from the CNS cannot reach the limb",
   "Both kinds of impulses pass normally, because the PNS has only one type of fibre",
   "Impulses from the limb can no longer reach the CNS, but regulatory impulses from the CNS can still reach the "
   "limb"], "D",
  "Afferent and efferent fibres",
  "NCERT: the nerve fibres of the PNS are of two types – afferent fibres transmit impulses from tissues and organs to "
  "the CNS, and efferent fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues and "
  "organs. Losing only the afferent fibres blocks the limb-to-CNS route while the CNS-to-limb route remains.",
  ["Afferent → towards CNS (destroyed)", "Efferent → from CNS (intact)"],
  R_NEU("human neural system"),
  why_others_wrong="A also blocks the intact efferent route; B reverses the roles of afferent and efferent fibres; C "
                   "ignores that the PNS has two kinds of fibres.",
  seconds=45)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "multi_statement",
  ms("A toxin prevents synaptic vesicles from fusing with the pre-synaptic membrane at chemical synapses only. Which "
     "of the following would be expected?",
     ["Neurotransmitters are not released into the synaptic cleft.",
      "No new potential is generated in the post-synaptic neuron across these synapses.",
      "The pre-synaptic neuron itself loses its resting potential.",
      "Transmission at electrical synapses, where current flows directly from one neuron into the other, continues."]),
  ["(a) and (b) only", "(a), (b), (c) and (d)", "(a), (b) and (d) only", "(b) and (c) only"], "C",
  "Chemical versus electrical synapses",
  "NCERT: at a chemical synapse, the arriving impulse makes synaptic vesicles fuse with the plasma membrane and "
  "release neurotransmitters into the cleft; these bind post-synaptic receptors, open ion channels and can generate a "
  "new potential. If fusion fails, nothing is released and no post-synaptic potential arises. The pre-synaptic "
  "neuron's own resting potential depends on its ionic gradients, not on transmitter release. At electrical "
  "synapses, current flows directly from one neuron into the other, without neurotransmitters.",
  ["(a) true", "(b) true", "(c) false – the resting potential is unaffected", "(d) true – no vesicles needed"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A leaves out (d); B and D include (c), and D also leaves out (a).",
  seconds=60)

Z(NEU, "Nervous system divisions", "Advanced", "direct",
  "If the corpus callosum of a person were cut, which function would be most directly affected?",
  ["Control of respiration and cardiovascular reflexes",
   "Communication between the left and right cerebral hemispheres",
   "Passage of the cerebral aqueduct through the midbrain",
   "Connection of the brain with the spinal cord through the medulla"], "B",
  "Corpus callosum",
  "NCERT: a deep cleft divides the cerebrum longitudinally into two halves, the left and right cerebral hemispheres, "
  "which are connected by a tract of nerve fibres called the corpus callosum. Cutting it would most directly affect "
  "communication between the two hemispheres.",
  ["Corpus callosum = fibre tract joining the two hemispheres", "Cut → hemispheres disconnected"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="Respiratory and cardiovascular centres are in the medulla; the cerebral aqueduct passes through "
                   "the midbrain; the medulla connects the brain to the spinal cord.",
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
           "notes": "BATCH_005 package ZOO_005_p1: 129 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "facts already tested in BATCH_000-BATCH_004; every numerical answer re-derived by "
                    "tools/batch_005/ZOO_005_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
