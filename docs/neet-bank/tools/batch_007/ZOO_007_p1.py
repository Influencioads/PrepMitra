"""Writes batches/parts/BATCH_007_ZOO_p1.json: package ZOO_007_p1 of BATCH_007 (Zoology, 125 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_001501 .. NEET_ZOO_001625. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, subtopics, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11
Biology textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion and absorption), and
for the frog only the systems the NMC text lists. Facts already tested in BATCH_000 to BATCH_006 (see
`merge_batch.py stems 007 ZOO_007_p1`) are not asked again in the same way.

    python docs/neet-bank/tools/batch_007/ZOO_007_p1.py
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
ZOO = "Zoology"
PACKAGE = "ZOO_007_p1"
BATCH = "BATCH_007"
FIRST_ID, LAST_ID = 1501, 1625
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

Z(AK, "Chordate classes", "Basic", "direct",
  "Among the reptiles that NCERT lists as examples, the genus Naja is commonly known as the:",
  ["Krait", "Cobra", "Viper", "Wall lizard"], "B",
  "Examples of Reptilia",
  "NCERT examples of Reptilia include Chelone (turtle), Testudo (tortoise), Chameleon (tree lizard), Calotes (garden "
  "lizard), Crocodilus (crocodile), Alligator (alligator), Hemidactylus (wall lizard) and the poisonous snakes Naja "
  "(cobra), Bangarus (krait) and Vipera (viper).",
  ["Naja → cobra"],
  R_AK("class Reptilia"),
  why_others_wrong="The krait is Bangarus, the viper is Vipera and the wall lizard is Hemidactylus.",
  seconds=20)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "In molluscs, feather-like gills are present in the mantle cavity. According to NCERT, these gills serve for:",
  ["Locomotion only", "Respiration only", "Respiration and excretion", "Feeding and sensory reception"], "C",
  "Gills of molluscs",
  "NCERT: the space between the hump and the mantle is called the mantle cavity, in which feather-like gills are "
  "present. They have respiratory and excretory functions.",
  ["Mantle cavity gills → respiratory + excretory functions"],
  R_AK("phylum Mollusca"),
  why_others_wrong="NCERT gives the gills two roles, so 'respiration only' is incomplete; locomotion is by the "
                   "muscular foot, feeding uses the radula and sensory reception the head tentacles.",
  seconds=25)

Z(AK, "Chordate classes", "Basic", "match_list",
  ml(("mammal genus", "common name"), ["Rattus", "Canis", "Panthera tigris", "Panthera leo"],
     ["Lion", "Dog", "Tiger", "Rat"]),
  match_options(M("IV", "II", "III", "I"), [M("IV", "II", "I", "III"), M("II", "IV", "III", "I"),
                                            M("IV", "III", "II", "I")], "D"), "D",
  "Examples of Mammalia",
  "NCERT examples of viviparous mammals include Rattus (rat), Canis (dog), Panthera tigris (tiger) and Panthera leo "
  "(lion). The two big cats share the genus Panthera and differ in the species name.",
  ["Rattus → rat (IV)", "Canis → dog (II)", "Panthera tigris → tiger (III)", "Panthera leo → lion (I)"],
  R_AK("class Mammalia"),
  why_others_wrong="A swaps the tiger and the lion; B swaps Rattus and Canis; C swaps Canis and Panthera tigris.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Basic", "match_list",
  ml(("animal", "common name"), ["Gorgonia", "Ophiura", "Wuchereria", "Taenia"],
     ["Tapeworm", "Filaria worm", "Brittle star", "Sea-fan"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("I", "III", "II", "IV")], "A"), "A",
  "Examples of non-chordate phyla",
  "NCERT examples: Gorgonia (sea-fan) is a coelenterate, Ophiura (brittle star) an echinoderm, Wuchereria (filaria "
  "worm) an aschelminth and Taenia (tapeworm) a platyhelminth.",
  ["Gorgonia → sea-fan (IV)", "Ophiura → brittle star (III)", "Wuchereria → filaria worm (II)",
   "Taenia → tapeworm (I)"],
  R_AK("phyla Coelenterata, Platyhelminthes, Aschelminthes and Echinodermata"),
  why_others_wrong="B swaps Gorgonia and Ophiura; C swaps the two worms; D swaps Gorgonia and Taenia.",
  seconds=30)

Z(AK, "Chordate classes", "Basic", "direct",
  "NCERT gives an alternative name for the chordate subphylum Urochordata. It is:",
  ["Cephalochordata", "Hemichordata", "Agnatha", "Tunicata"], "D",
  "Subphyla of Chordata",
  "NCERT: phylum Chordata is divided into three subphyla – Urochordata or Tunicata, Cephalochordata and Vertebrata. "
  "Examples of urochordates are Ascidia, Salpa and Doliolum.",
  ["Urochordata = Tunicata"],
  R_AK("phylum Chordata"),
  why_others_wrong="Cephalochordata is a separate subphylum; Hemichordata is now a separate non-chordate phylum; "
                   "Agnatha is the jawless division of the vertebrates.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "statement_pair",
  sp("Mammals are found in a variety of habitats – polar ice caps, deserts, mountains, forests, grasslands and dark "
     "caves.",
     "In mammals, respiration is by lungs."),
  STATEMENT_PAIR, "A",
  "Class Mammalia",
  "Both lines are NCERT's description of class Mammalia: mammals are found in a variety of habitats (polar ice caps, "
  "deserts, mountains, forests, grasslands and dark caves), some are adapted to fly or live in water, and their "
  "respiration is by lungs.",
  ["Statement I → true", "Statement II → true"],
  R_AK("class Mammalia"),
  why_others_wrong="Neither statement is false, so B, C and D are wrong.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements about phylum Mollusca are correct?",
     ["The body is covered by a calcareous shell.",
      "A soft and spongy layer of skin forms a mantle over the visceral hump.",
      "Molluscs are exclusively marine animals.",
      "Molluscs show the tissue level of organisation."]),
  ["(b) and (d) only", "(a) and (b) only", "(a), (b) and (c) only", "(a), (c) and (d) only"], "B",
  "Phylum Mollusca",
  "NCERT: molluscs are terrestrial or aquatic (marine or fresh water) and have an organ-system level of "
  "organisation. The body is covered by a calcareous shell and is unsegmented with a distinct head, muscular foot "
  "and visceral hump. A soft and spongy layer of skin forms a mantle over the visceral hump.",
  ["(a) true", "(b) true", "(c) false – terrestrial or aquatic, marine or fresh water",
   "(d) false – organ-system level"],
  R_AK("phylum Mollusca"),
  why_others_wrong="A includes (d) and leaves out (a); C includes (c); D includes (c) and (d) and leaves out (b).",
  seconds=45)
ms_check("ab", ["(b) and (d) only", "(a) and (b) only", "(a), (b) and (c) only", "(a), (c) and (d) only"], "B")

Z(AK, "Basis of classification", "Intermediate", "assertion_reason",
  ar("Sponges are placed among the non-chordates.",
     "Animals that do not form a notochord during embryonic development are called non-chordates, and sponges do "
     "not form a notochord."),
  ASSERTION_REASON, "A",
  "Notochord as a basis of classification",
  "NCERT: the notochord is a mesodermally derived rod-like structure formed on the dorsal side during embryonic "
  "development in some animals. Animals with a notochord are called chordates and those which do not form this "
  "structure are called non-chordates, e.g. Porifera to Echinodermata. The absence of a notochord is exactly why "
  "sponges are non-chordates.",
  ["A true", "R true", "No notochord → non-chordate → R explains A"],
  R_AK("basis of classification: notochord"),
  why_others_wrong="B is wrong because the absence of a notochord is the very criterion that places sponges among the "
                   "non-chordates; C and D are wrong because both statements are true.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("Arthropods have sensory organs such as antennae, eyes (compound and simple) and statocysts or balance organs.",
     "Arthropods are mostly monoecious."),
  STATEMENT_PAIR, "C",
  "Phylum Arthropoda",
  "NCERT: in arthropods, sensory organs like antennae, eyes (compound and simple) and statocysts or balance organs "
  "are present. They are mostly dioecious, fertilisation is usually internal, they are mostly oviparous and "
  "development may be direct or indirect.",
  ["Statement I → true", "Statement II → false (mostly dioecious)"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="A and D accept 'mostly monoecious', whereas NCERT says arthropods are mostly dioecious; B "
                   "rejects NCERT's list of arthropod sense organs.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "direct",
  "Which of the following features does NCERT describe for cartilaginous fishes (Chondrichthyes) but NOT for bony "
  "fishes (Osteichthyes)?",
  ["Their heart is two-chambered", "They are cold-blooded (poikilothermous)",
   "Their jaws are very powerful and they are predaceous", "Their sexes are separate"], "C",
  "Chondrichthyes versus Osteichthyes",
  "NCERT: in Chondrichthyes the jaws are very powerful and these animals are predaceous. Both classes of fishes have "
  "a two-chambered heart (one auricle and one ventricle), both are cold-blooded and in both the sexes are separate.",
  ["Two-chambered heart → both", "Cold-blooded → both", "Separate sexes → both",
   "Very powerful jaws, predaceous → Chondrichthyes only"],
  R_AK("classes Chondrichthyes and Osteichthyes"),
  why_others_wrong="A, B and D are stated for both classes of fishes, so they do not distinguish the cartilaginous "
                   "fishes.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("In echinoderms, fertilisation is usually external.",
     "Echinoderms are monoecious, each individual producing both eggs and sperms."),
  ASSERTION_REASON, "C",
  "Reproduction in Echinodermata",
  "NCERT: in echinoderms, sexes are separate, reproduction is sexual, fertilisation is usually external and "
  "development is indirect with a free-swimming larva. So the Assertion is true, but echinoderms are not monoecious; "
  "the Reason is false.",
  ["A true", "R false – sexes are separate (dioecious)"],
  R_AK("phylum Echinodermata"),
  why_others_wrong="A and B accept a false Reason; D rejects NCERT's statement that fertilisation is usually "
                   "external.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("All members of phylum Aschelminthes are parasites.",
     "Aschelminthes may be free-living, aquatic and terrestrial, or parasitic in plants and animals."),
  ASSERTION_REASON, "D",
  "Habitat of Aschelminthes",
  "NCERT: roundworms may be free-living, aquatic and terrestrial or parasitic in plants and animals. Ascaris and "
  "Ancylostoma are parasites, but the phylum is not wholly parasitic, so the Assertion is false while the Reason is "
  "NCERT's own line.",
  ["A false – free-living forms also exist", "R true"],
  R_AK("phylum Aschelminthes"),
  why_others_wrong="A, B and C all treat the Assertion as true; the Reason itself shows that free-living members "
                   "exist.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "match_list",
  ml(("cartilaginous fish", "common name"), ["Scoliodon", "Pristis", "Carcharodon", "Trygon"],
     ["Sting ray", "Great white shark", "Saw fish", "Dog fish"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("II", "III", "IV", "I")], "B"), "B",
  "Examples of Chondrichthyes",
  "NCERT examples of Chondrichthyes: Scoliodon (dog fish), Pristis (saw fish), Carcharodon (great white shark) and "
  "Trygon (sting ray). Torpedo has electric organs and Trygon has a poison sting.",
  ["Scoliodon → dog fish (IV)", "Pristis → saw fish (III)", "Carcharodon → great white shark (II)",
   "Trygon → sting ray (I)"],
  R_AK("class Chondrichthyes"),
  why_others_wrong="A swaps Scoliodon and Pristis; C swaps Carcharodon and Trygon; D swaps Scoliodon and "
                   "Carcharodon.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "Which of the following statements about hemichordates such as Balanoglossus is correct according to NCERT?",
  ["Respiration takes place through gills", "The circulatory system is of the closed type",
   "They are found mainly in fresh water", "The body is divided into head, thorax and abdomen"], "A",
  "Phylum Hemichordata",
  "NCERT: hemichordates are a small group of worm-like marine animals with an organ-system level of organisation. The "
  "body is cylindrical and is composed of an anterior proboscis, a collar and a long trunk. The circulatory system "
  "is of open type, respiration takes place through gills and the excretory organ is the proboscis gland.",
  ["Respiration → gills", "Circulation → open", "Habitat → marine", "Body → proboscis, collar, trunk"],
  R_AK("phylum Hemichordata"),
  why_others_wrong="B is wrong because their circulation is open; C because they are marine; D because the body "
                   "parts are proboscis, collar and trunk (head, thorax and abdomen describe arthropods).",
  seconds=35)

Z(AK, "Basis of classification", "Advanced", "multi_statement",
  ms("In which of the following pairs do BOTH animals show the organ-system level of organisation, as described in "
     "NCERT?",
     ["Ascaris and Pheretima", "Hydra and Adamsia", "Pila and Asterias", "Pleurobrachia and Ctenoplana",
      "Sycon and Spongilla"]),
  ["(a), (b) and (c) only", "(c) and (e) only", "(a), (c) and (d) only", "(a) and (c) only"], "D",
  "Levels of organisation",
  "NCERT: sponges show the cellular level; coelenterates and ctenophores show the tissue level; aschelminths, "
  "annelids, arthropods, molluscs, echinoderms and chordates show the organ-system level. Ascaris (aschelminth) and "
  "Pheretima (annelid) qualify, as do Pila (mollusc) and Asterias (echinoderm). Hydra and Adamsia are coelenterates "
  "and Pleurobrachia and Ctenoplana are ctenophores (tissue level); Sycon and Spongilla are sponges (cellular level).",
  ["(a) organ-system + organ-system → yes", "(b) tissue level → no", "(c) organ-system → yes",
   "(d) tissue level → no", "(e) cellular level → no"],
  R_AK("basis of classification: levels of organisation; phylum descriptions"),
  why_others_wrong="A adds the coelenterate pair; B adds the sponges and drops (a); C adds the ctenophore pair.",
  seconds=60)
ms_check("ac", ["(a), (b) and (c) only", "(c) and (e) only", "(a), (c) and (d) only", "(a) and (c) only"], "D")

Z(AK, "Chordate classes", "Advanced", "direct",
  "Which of the following is correctly matched in all three columns (genus – class – common name)?",
  ["Hippocampus – Chondrichthyes – Sea horse", "Neophron – Aves – Penguin",
   "Exocoetus – Osteichthyes – Flying fish", "Salamandra – Reptilia – Salamander"], "C",
  "Examples of vertebrate classes",
  "NCERT: Exocoetus (flying fish) and Hippocampus (sea horse) are marine bony fishes (Osteichthyes); Neophron is the "
  "vulture (the penguin is Aptenodytes); Salamandra (salamander) is an amphibian.",
  ["Exocoetus → Osteichthyes → flying fish ✓", "Hippocampus → Osteichthyes, not Chondrichthyes",
   "Neophron → vulture", "Salamandra → Amphibia"],
  R_AK("classes Osteichthyes, Amphibia and Aves"),
  why_others_wrong="A has the wrong class (sea horse is a bony fish); B has the wrong common name (Neophron is the "
                   "vulture); D has the wrong class (the salamander is an amphibian).",
  seconds=45)

Z(AK, "Basis of classification", "Advanced", "assertion_reason",
  ar("All triploblastic animals are coelomates.",
     "In triploblastic animals, a third germinal layer, the mesoderm, is present in between the ectoderm and the "
     "endoderm of the developing embryo."),
  ASSERTION_REASON, "D",
  "Germ layers and body cavity",
  "NCERT: animals with three germ layers (Platyhelminthes to Chordates) are triploblastic. But the body cavity "
  "varies among them: Platyhelminthes are acoelomates (no body cavity) and Aschelminthes are pseudocoelomates (body "
  "cavity not lined by mesoderm). Only animals whose cavity is lined by mesoderm are coelomates. So the Assertion is "
  "false; the Reason is NCERT's definition of triploblastic animals.",
  ["A false – flatworms are acoelomate, roundworms pseudocoelomate", "R true"],
  R_AK("basis of classification: diploblastic and triploblastic organisation; coelom"),
  why_others_wrong="A, B and C treat the Assertion as true; having mesoderm does not by itself give a coelom.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "statement_pair",
  sp("NCERT describes the sexes as not separate (hermaphrodite) in members of Porifera, Ctenophora and "
     "Platyhelminthes.",
     "Hemichordates, too, are hermaphrodite."),
  STATEMENT_PAIR, "C",
  "Sexes in different phyla",
  "NCERT: in sponges the sexes are not separate (hermaphrodite), i.e. eggs and sperms are produced by the same "
  "individual; in ctenophores the sexes are not separate; in platyhelminths the sexes are not separate. In "
  "hemichordates, however, the sexes are separate, fertilisation is external and development is indirect.",
  ["Statement I → true", "Statement II → false (sexes separate in Hemichordata)"],
  R_AK("phyla Porifera, Ctenophora, Platyhelminthes and Hemichordata"),
  why_others_wrong="A and D accept that hemichordates are hermaphrodite; B rejects Statement I, though NCERT gives "
                   "'sexes not separate' for all three phyla.",
  seconds=40)

Z(AK, "Basis of classification", "Advanced", "match_list",
  ml(("animal", "level of organisation"), ["Spongilla", "Physalia", "Planaria", "Hirudinaria"],
     ["Organ-system level", "Organ level", "Tissue level", "Cellular level"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"),
                                            M("IV", "III", "I", "II")], "B"), "B",
  "Levels of organisation",
  "NCERT: sponges (Spongilla) show the cellular level; coelenterates (Physalia) the tissue level; flatworms "
  "(Planaria) are 'triploblastic and acoelomate animals with organ level of organisation'; annelids (Hirudinaria) "
  "have the organ-system level.",
  ["Spongilla → cellular (IV)", "Physalia → tissue (III)", "Planaria → organ (II)", "Hirudinaria → organ-system (I)"],
  R_AK("basis of classification: levels of organisation; phylum Platyhelminthes"),
  why_others_wrong="A swaps the coelenterate and the flatworm; C swaps the sponge and the coelenterate; D gives the "
                   "flatworm the organ-system level and the leech only the organ level.",
  seconds=45)

Z(AK, "Non-chordate phyla", "Advanced", "direct",
  "Which of the following features is shared by Annelida, Arthropoda and Mollusca as described in NCERT?",
  ["Metameric segmentation", "A chitinous exoskeleton", "A closed circulatory system",
   "Bilateral symmetry, triploblastic organisation, a true coelom and the organ-system level"], "D",
  "Comparing coelomate phyla",
  "NCERT: annelids are bilaterally symmetrical, triploblastic, metamerically segmented and coelomate with organ-system "
  "level; arthropods are bilaterally symmetrical, triploblastic, segmented and coelomate with organ-system level and a "
  "chitinous exoskeleton and open circulation; molluscs are bilaterally symmetrical, triploblastic and coelomate with "
  "organ-system level, but their body is unsegmented.",
  ["Segmentation → not molluscs", "Chitinous exoskeleton → arthropods only",
   "Closed circulation → annelids, not arthropods", "Bilateral, triploblastic, coelomate, organ-system → all three"],
  R_AK("phyla Annelida, Arthropoda and Mollusca"),
  why_others_wrong="A fails for the unsegmented molluscs; B is true only of arthropods; C fails for arthropods, whose "
                   "circulatory system is open.",
  seconds=50)

# ================================================================ Structural Organisation in Animals (B5 I6 A5)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "On land, the buccal cavity, skin and lungs act as the respiratory organs of the frog. Respiration by the lungs is "
  "called:",
  ["Cutaneous respiration", "Pulmonary respiration", "Branchial respiration", "Cellular respiration"], "B",
  "Respiration in the frog",
  "NCERT: in water, the skin acts as the aquatic respiratory organ (cutaneous respiration). On land, the buccal "
  "cavity, skin and lungs act as respiratory organs; the respiration by lungs is called pulmonary respiration.",
  ["Lungs → pulmonary respiration", "Skin → cutaneous respiration"],
  R_SOA("frog: anatomy (respiratory system)"),
  why_others_wrong="Cutaneous respiration is through the skin; branchial respiration is through gills; cellular "
                   "respiration is the use of O₂ inside cells, not gas exchange by an organ.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Earwax and milk are both secretions of which type of gland?",
  ["Endocrine glands", "Unicellular glands only", "Ductless glands", "Exocrine glands"], "D",
  "Exocrine glands",
  "NCERT: exocrine glands secrete mucus, saliva, earwax, oil, milk, digestive enzymes and other cell products, which "
  "are released through ducts or tubes. Endocrine glands are ductless and secrete hormones directly into the fluid "
  "bathing the gland.",
  ["Earwax, milk → exocrine products"],
  R_SOA("animal tissues: epithelial tissue (glands)"),
  why_others_wrong="Endocrine (ductless) glands secrete hormones, not earwax or milk; milk-secreting mammary glands are "
                   "multicellular, so 'unicellular glands only' is wrong.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "direct",
  "According to NCERT, simple epithelium, which is composed of a single layer of cells, functions as a lining for:",
  ["The dry surface of the skin", "Body cavities, ducts and tubes",
   "Areas exposed to chemical and mechanical stresses", "The moist surface of the buccal cavity"], "B",
  "Simple epithelium",
  "NCERT: simple epithelium is composed of a single layer of cells and functions as a lining for body cavities, ducts "
  "and tubes. Compound epithelium consists of two or more cell layers and has a protective function, covering the dry "
  "surface of the skin and the moist surface of the buccal cavity.",
  ["Simple epithelium → lining of body cavities, ducts, tubes"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="A, C and D describe the sites and role of compound (multi-layered) epithelium.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "During winter, frogs take shelter in deep burrows to protect themselves from extreme cold. NCERT calls this:",
  ["Aestivation (summer sleep)", "Camouflage", "Metamorphosis", "Hibernation (winter sleep)"], "D",
  "Hibernation and aestivation",
  "NCERT: during peak summer and winter, frogs take shelter in deep burrows to protect themselves from extreme heat "
  "and cold. This is called summer sleep (aestivation) and winter sleep (hibernation) respectively.",
  ["Extreme cold → burrow → hibernation"],
  R_SOA("frog: habitat"),
  why_others_wrong="Aestivation is the summer sleep against heat; camouflage is protective colour change; "
                   "metamorphosis is the change of tadpole into adult.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "statement_pair",
  sp("Frogs can live both on land and in freshwater, and they belong to class Amphibia of phylum Chordata.",
     "The forelimbs and hind limbs of the frog help in swimming, walking, leaping and burrowing."),
  STATEMENT_PAIR, "A",
  "Habitat and limbs of the frog",
  "NCERT: frogs can live both on land and in freshwater and belong to class Amphibia of phylum Chordata. The forelimbs "
  "and hind limbs help in swimming, walking, leaping and burrowing; the hind limbs end in five digits and are larger "
  "and more muscular than the forelimbs.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("frog: habitat and morphology"),
  why_others_wrong="Both statements are NCERT's own description, so B, C and D are wrong.",
  seconds=25)

Z(SOA, "Animal tissues", "Intermediate", "assertion_reason",
  ar("A person who regularly takes in more food than the body uses immediately tends to accumulate fat beneath the "
     "skin.",
     "The excess of nutrients which are not used immediately are converted into fats and stored in adipose tissue, "
     "which is located mainly beneath the skin."),
  ASSERTION_REASON, "A",
  "Adipose tissue",
  "NCERT: adipose tissue is a type of loose connective tissue located mainly beneath the skin. Its cells are "
  "specialised to store fats. The excess of nutrients which are not used immediately are converted into fats and are "
  "stored in this tissue. This directly explains why surplus food intake builds up fat beneath the skin.",
  ["A true", "R true", "Excess nutrients → fat → stored in adipose beneath skin → R explains A"],
  R_SOA("animal tissues: connective tissue (adipose tissue)"),
  why_others_wrong="B is wrong because the storage of surplus nutrients as fat in subcutaneous adipose tissue is the "
                   "cause of the Assertion; C and D are wrong because both statements are true.",
  seconds=35)

Z(SOA, "Animal tissues", "Intermediate", "statement_pair",
  sp("Cells, tissues, organs and organ systems split up the work in a way that exhibits division of labour and "
     "contribute to the survival of the body as a whole.",
     "Each organ such as the stomach, lung, heart or kidney is formed from a single type of tissue."),
  STATEMENT_PAIR, "C",
  "Organs and organ systems",
  "NCERT: tissues are organised in specific proportion and pattern to form an organ like the stomach, lung, heart "
  "and kidney – that is, an organ is built of several tissues. Cells, tissues, organs and organ systems split up the "
  "work in a way that exhibits division of labour and contribute to the survival of the body as a whole.",
  ["Statement I → true", "Statement II → false (organs contain tissues in a specific proportion and pattern)"],
  R_SOA("organ and organ system"),
  why_others_wrong="A and D accept the single-tissue claim; B rejects NCERT's statement of division of labour.",
  seconds=35)

Z(SOA, "Animal tissues", "Intermediate", "multi_statement",
  ms("A tissue taken from the wall of the intestine shows spindle-shaped fibres that taper at both ends, show no "
     "striations, are held together by cell junctions and are bundled in a connective tissue sheath. Which of the "
     "following statements about this tissue are correct?",
     ["It is smooth muscle tissue.",
      "The same type of tissue occurs in the walls of blood vessels and the stomach.",
      "Its contraction can be directly controlled by thinking about it.",
      "It is described as involuntary muscle.",
      "Its cells are joined by communication junctions (intercalated discs) like those of the heart."]),
  ["(a), (c) and (d) only", "(a), (b) and (d) only", "(a), (b), (d) and (e) only", "(b), (c) and (e) only"], "B",
  "Smooth muscle",
  "NCERT: smooth muscle fibres taper at both ends (fusiform) and do not show striations. Cell junctions hold them "
  "together and they are bundled together in a connective tissue sheath. The walls of internal organs such as the "
  "blood vessels, stomach and intestine contain this tissue. Smooth muscles are involuntary, as their functioning "
  "cannot be directly controlled. Communication junctions (intercalated discs) are described for cardiac muscle.",
  ["(a) true", "(b) true", "(c) false – involuntary", "(d) true", "(e) false – intercalated discs belong to cardiac "
   "muscle"],
  R_SOA("animal tissues: muscle tissue"),
  why_others_wrong="A includes (c) and leaves out (b); C adds the cardiac-muscle feature (e); D includes (c) and (e) "
                   "and leaves out (a) and (d).",
  seconds=55)
ms_check("abd", ["(a), (c) and (d) only", "(a), (b) and (d) only", "(a), (b), (d) and (e) only",
                 "(b), (c) and (e) only"], "B")

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("In the frog, air drawn in through the nostrils passes into the buccal cavity and then to the lungs.",
     "On land, the skin is the only respiratory organ of the frog."),
  ASSERTION_REASON, "C",
  "Respiratory pathway in the frog",
  "NCERT: the lungs of the frog are a pair of elongated, pink-coloured sac-like structures in the upper part of the "
  "trunk (thorax). Air enters through the nostrils into the buccal cavity and then to the lungs. On land, the buccal "
  "cavity, skin and lungs all act as respiratory organs, so the skin is not the only one.",
  ["A true", "R false – buccal cavity, skin and lungs on land"],
  R_SOA("frog: anatomy (respiratory system)"),
  why_others_wrong="A and B accept the false Reason; D rejects the NCERT route of air into the lungs.",
  seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "match_list",
  ml(("structure in the frog", "organ system it belongs to"),
     ["Conus arteriosus", "Optic lobes", "Gall bladder", "Lungs"],
     ["Neural system", "Respiratory system", "Digestive system", "Circulatory system"]),
  match_options(M("IV", "I", "III", "II"), [M("IV", "III", "I", "II"), M("II", "I", "III", "IV"),
                                            M("I", "IV", "III", "II")], "D"), "D",
  "Organ systems of the frog",
  "NCERT: the ventricle of the frog's heart opens into a sac-like conus arteriosus (circulatory system); the "
  "mid-brain is characterised by a pair of optic lobes (neural system); the gall bladder stores bile secreted by the "
  "liver (digestive system); the lungs are the organs of pulmonary respiration (respiratory system).",
  ["Conus arteriosus → circulatory (IV)", "Optic lobes → neural (I)", "Gall bladder → digestive (III)",
   "Lungs → respiratory (II)"],
  R_SOA("frog: anatomy"),
  why_others_wrong="A swaps the optic lobes and the gall bladder; B swaps the conus arteriosus and the lungs; C swaps "
                   "the conus arteriosus and the optic lobes.",
  seconds=35)

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "NCERT mentions microvilli on the free surface of two kinds of simple epithelium. Which pair is it?",
  ["Squamous and compound epithelium", "Cuboidal and columnar epithelium", "Squamous and cuboidal epithelium",
   "Compound and columnar epithelium"], "B",
  "Microvilli on epithelia",
  "NCERT: the cuboidal epithelium of the proximal convoluted tubule (PCT) of the nephron has microvilli, and the free "
  "surface of columnar epithelium may have microvilli. Squamous epithelium is a thin layer of flattened cells forming "
  "a diffusion boundary, and compound epithelium is protective.",
  ["Cuboidal (PCT) → microvilli", "Columnar → free surface may have microvilli"],
  R_SOA("animal tissues: epithelial tissue"),
  why_others_wrong="A, C and D each include squamous or compound epithelium, for which NCERT mentions no microvilli.",
  seconds=35)

Z(SOA, "Animal tissues", "Advanced", "statement_pair",
  sp("Of the three specialised connective tissues – cartilage, bone and blood – only bone has a hard, non-pliable "
     "ground substance rich in calcium salts.",
     "In blood, as in the other connective tissues, the cells secrete fibres of the structural proteins collagen or "
     "elastin."),
  STATEMENT_PAIR, "C",
  "Specialised connective tissues",
  "NCERT: bones have a hard and non-pliable ground substance rich in calcium salts and collagen fibres; the "
  "intercellular material of cartilage is solid and pliable; blood is a fluid connective tissue. NCERT also states "
  "that in all connective tissues except blood, the cells secrete fibres of structural proteins called collagen or "
  "elastin.",
  ["Statement I → true", "Statement II → false (blood is the exception)"],
  R_SOA("animal tissues: connective tissue"),
  why_others_wrong="A and D accept Statement II, ignoring NCERT's 'except blood'; B rejects Statement I, though "
                   "cartilage is pliable and blood is fluid.",
  seconds=40)

Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("Which of the following surfaces are covered or lined by compound epithelium, according to NCERT?",
     ["The dry surface of the skin", "The moist surface of the buccal cavity", "The inner lining of the pancreatic "
      "ducts", "The walls of the air sacs of the lungs", "The tubular parts of the nephrons"]),
  ["(a) and (b) only", "(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (b) and (c) only"], "D",
  "Compound epithelium",
  "NCERT: compound epithelium covers the dry surface of the skin, the moist surface of the buccal cavity and the "
  "pharynx, and the inner lining of the ducts of salivary glands and of pancreatic ducts. The walls of the air sacs "
  "of the lungs are lined by squamous epithelium and the tubular parts of nephrons by cuboidal epithelium.",
  ["(a) compound", "(b) compound", "(c) compound", "(d) squamous", "(e) cuboidal"],
  R_SOA("animal tissues: epithelial tissue (compound epithelium)"),
  why_others_wrong="A leaves out the pancreatic ducts; B adds the nephron tubules (cuboidal); C adds the air sacs "
                   "(squamous) and leaves out the skin.",
  seconds=50)
ms_check("abc", ["(a) and (b) only", "(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (b) and (c) only"], "D")

Z(SOA, "Frog: morphology and anatomy", "Advanced", "multi_statement",
  ms("A student compares the frog with human beings. Which of the following statements are correct according to "
     "NCERT?",
     ["Both have a closed type of blood vascular system.",
      "The heart of the frog has three chambers, whereas the human heart has four.",
      "The RBCs of the frog are nucleated, whereas human RBCs are devoid of a nucleus.",
      "Both have a hepatic portal system connecting the intestine with the liver.",
      "Like human beings, the frog maintains a constant body temperature."]),
  ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only", "(a), (b) and (d) only"],
  "A",
  "Frog and human compared",
  "NCERT: the vascular system of the frog is a well-developed closed type, the heart has three chambers (two atria "
  "and one ventricle), its RBCs are nucleated and contain haemoglobin, and it has a hepatic portal system between the "
  "liver and the intestine. Humans also have a closed circulatory system, a four-chambered heart, RBCs devoid of a "
  "nucleus (as in most mammals) and a hepatic portal vein carrying blood from the intestine to the liver. The frog, "
  "however, is cold-blooded (poikilotherm).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – the frog is cold-blooded"],
  R_SOA("frog: anatomy (circulatory system)") + "; Class 11 Biology, 'Body Fluids and Circulation', erythrocytes "
  "and double circulation",
  why_others_wrong="B and C include (e), though the frog is cold-blooded; D leaves out the correct statement (c).",
  seconds=60)
ms_check("abcd", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only",
                  "(a), (b) and (d) only"], "A")

Z(SOA, "Animal tissues", "Advanced", "match_list",
  ml(("epithelium", "sites where NCERT says it is found"),
     ["Ciliated epithelium", "Cuboidal epithelium", "Columnar epithelium", "Squamous epithelium"],
     ["Lining of the stomach and intestine", "Walls of blood vessels and air sacs of lungs",
      "Inner surface of bronchioles and fallopian tubes", "Ducts of glands and tubular parts of nephrons"]),
  match_options(M("III", "IV", "I", "II"), [M("III", "I", "IV", "II"), M("IV", "III", "I", "II"),
                                            M("II", "IV", "I", "III")], "D"), "D",
  "Simple epithelia and their sites",
  "NCERT: ciliated epithelium is mainly present on the inner surface of hollow organs like bronchioles and fallopian "
  "tubes; cuboidal epithelium is commonly found in the ducts of glands and tubular parts of nephrons; columnar "
  "epithelium lines the stomach and intestine; squamous epithelium is found in the walls of blood vessels and air "
  "sacs of lungs.",
  ["Ciliated → bronchioles, fallopian tubes (III)", "Cuboidal → glandular ducts, nephron tubules (IV)",
   "Columnar → stomach, intestine (I)", "Squamous → blood vessels, air sacs (II)"],
  R_SOA("animal tissues: epithelial tissue (simple epithelium)"),
  why_others_wrong="A swaps cuboidal and columnar; B swaps ciliated and cuboidal; C swaps ciliated and squamous.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "assertion_reason",
  ar("The cartilage at the tip of the nose can be pressed and bent without being crushed.",
     "The intercellular material of cartilage is solid and pliable and resists compression."),
  ASSERTION_REASON, "A",
  "Properties of cartilage",
  "NCERT: the intercellular material of cartilage is solid and pliable and resists compression; in adults, cartilage "
  "is present in the tip of the nose, outer ear joints, between adjacent bones of the vertebral column, limbs and "
  "hands. Pliability lets the nose tip bend, and resistance to compression keeps it from being crushed, so R explains "
  "A.",
  ["A true", "R true", "Pliable + resists compression → bends without crushing → R explains A"],
  R_SOA("animal tissues: connective tissue (cartilage)"),
  why_others_wrong="B is wrong because the pliable, compression-resistant matrix is the reason for the behaviour "
                   "described; C and D are wrong because both statements are true.",
  seconds=35)

# ================================================================ Biomolecules (B6 I8 A6)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "Amino acids differ in their R group. The amino acid whose R group is simply a hydrogen atom is:",
  ["Glycine", "Alanine", "Serine", "Valine"], "A",
  "R groups of amino acids",
  "NCERT: the R group in proteinaceous amino acids could be a hydrogen (the amino acid is called glycine), a methyl "
  "group (alanine), hydroxy methyl (serine), etc.",
  ["R = H → glycine"],
  R_BIO("amino acids"),
  why_others_wrong="Alanine has a methyl R group and serine a hydroxy methyl R group; valine is cited by NCERT as a "
                   "neutral amino acid, not one with H as its R group.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "For which kind of enzyme co-factor does NCERT say that its association with the apoenzyme is only transient, "
  "usually occurring during the course of catalysis?",
  ["Prosthetic groups", "Co-enzymes", "Metal ions", "Haem"], "B",
  "Kinds of co-factors",
  "NCERT: co-factors are of three kinds – prosthetic groups, co-enzymes and metal ions. Prosthetic groups are organic "
  "compounds distinguished from other co-factors in that they are tightly bound to the apoenzyme (e.g. haem in "
  "peroxidase and catalase). Co-enzymes are also organic compounds, but their association with the apoenzyme is only "
  "transient, usually occurring during the course of catalysis.",
  ["Tightly bound → prosthetic group", "Transient association → co-enzyme"],
  R_BIO("enzymes: co-factors"),
  why_others_wrong="Prosthetic groups, including haem, are tightly bound; metal ions act by forming coordination bonds "
                   "with side chains at the active site, and NCERT does not describe them as the transiently associated "
                   "organic co-factor.",
  seconds=25)

Z(BIO, "Nucleic acids", "Basic", "statement_pair",
  sp("A nitrogenous base attached to a sugar is called a nucleoside.",
     "Adenylic acid and guanylic acid are nucleosides."),
  STATEMENT_PAIR, "C",
  "Nucleosides and nucleotides",
  "NCERT: a nitrogenous base attached to a sugar is a nucleoside (adenosine, guanosine, thymidine, uridine, "
  "cytidine). If a phosphate group is also esterified to the 5′-OH of the sugar, it is a nucleotide; adenylic acid, "
  "thymidylic acid, guanylic acid, uridylic acid and cytidylic acid are nucleotides.",
  ["Statement I → true", "Statement II → false (they are nucleotides)"],
  R_BIO("nucleic acids"),
  why_others_wrong="A and D accept the '-ylic acids' as nucleosides, though they carry a phosphate; B rejects NCERT's "
                   "definition of a nucleoside.",
  seconds=30)

Z(BIO, "Nucleic acids", "Basic", "match_list",
  ml(("nitrogenous base", "nucleoside formed with it"), ["Adenine", "Guanine", "Thymine", "Uracil"],
     ["Uridine", "Thymidine", "Adenosine", "Guanosine"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("II", "IV", "III", "I")], "C"), "C",
  "Naming nucleosides",
  "NCERT: a nitrogenous base attached to a sugar is a nucleoside; adenosine, guanosine, thymidine, uridine and "
  "cytidine are nucleosides, formed from adenine, guanine, thymine, uracil and cytosine respectively.",
  ["Adenine → adenosine (III)", "Guanine → guanosine (IV)", "Thymine → thymidine (II)", "Uracil → uridine (I)"],
  R_BIO("nucleic acids"),
  why_others_wrong="A swaps the two purines; B swaps the two pyrimidines; D swaps adenine and thymine.",
  seconds=25)

Z(BIO, "Proteins and amino acids", "Basic", "match_list",
  ml(("amino acid", "nature as described in NCERT"), ["Glutamic acid", "Lysine", "Valine", "Phenylalanine"],
     ["Aromatic", "Neutral", "Basic", "Acidic"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Kinds of amino acids",
  "NCERT: based on the number of amino and carboxyl groups, there are acidic (e.g. glutamic acid), basic (lysine) "
  "and neutral (valine) amino acids. Similarly, there are aromatic amino acids (tyrosine, phenylalanine and "
  "tryptophan).",
  ["Glutamic acid → acidic (IV)", "Lysine → basic (III)", "Valine → neutral (II)", "Phenylalanine → aromatic (I)"],
  R_BIO("amino acids"),
  why_others_wrong="A swaps acidic and basic; B swaps lysine and valine; C swaps valine and phenylalanine.",
  seconds=25)

Z(BIO, "Enzyme classification", "Basic", "direct",
  "Carboxypeptidase is a proteolytic enzyme: it breaks peptide bonds of proteins by adding water. In NCERT's "
  "classification of enzymes, it belongs to the class:",
  ["Transferases", "Lyases", "Hydrolases", "Ligases"], "C",
  "Classifying an enzyme by its reaction",
  "NCERT: hydrolases catalyse the hydrolysis of ester, ether, peptide, glycosidic, C–C, C–halide or P–N bonds. "
  "Carboxypeptidase (for which NCERT names zinc as a co-factor) is proteolytic, i.e. it hydrolyses peptide bonds, so "
  "it is a hydrolase.",
  ["Peptide bond broken by hydrolysis → hydrolase"],
  R_BIO("enzymes: classification and nomenclature; co-factors"),
  why_others_wrong="Transferases move a group G between two substrates; lyases remove groups by mechanisms other than "
                   "hydrolysis, leaving double bonds; ligases link two compounds together.",
  seconds=30)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Cellulose does not give a blue colour when treated with iodine.",
     "Cellulose does not contain complex helices and hence cannot hold I₂ molecules."),
  ASSERTION_REASON, "A",
  "Starch, cellulose and iodine",
  "NCERT: starch forms helical secondary structures and can hold I₂ molecules in the helical portion; the starch–I₂ "
  "complex is blue. Cellulose does not contain complex helices and hence cannot hold I₂. The blue colour depends on "
  "I₂ held in the helix, so the absence of helices explains the absence of colour.",
  ["A true", "R true", "No helix → no I₂ held → no blue colour → R explains A"],
  R_BIO("polysaccharides"),
  why_others_wrong="B is wrong because inability to hold I₂ is precisely why cellulose stays uncoloured; C and D are "
                   "wrong because both statements are true.",
  seconds=35)

Z(BIO, "Enzyme classification", "Intermediate", "assertion_reason",
  ar("DNA ligase, which joins two DNA fragments by forming P–O bonds between them, is placed in the class Ligases.",
     "Ligases catalyse the linking together of two compounds, for example the joining of C–O, C–S, C–N or P–O "
     "bonds."),
  ASSERTION_REASON, "A",
  "Ligases",
  "NCERT defines ligases as enzymes catalysing the linking together of two compounds, e.g. enzymes which catalyse the "
  "joining of C–O, C–S, C–N, P–O, etc. bonds. DNA ligase links two DNA fragments by forming P–O bonds, which fits "
  "this definition exactly.",
  ["A true", "R true", "Joining two compounds via P–O bond = ligase reaction → R explains A"],
  R_BIO("enzymes: classification and nomenclature"),
  why_others_wrong="B is wrong because the class definition in R is what places DNA ligase among the ligases; C and D "
                   "are wrong because both statements are true.",
  seconds=35)

Z(BIO, "Enzymes: properties and action", "Intermediate", "assertion_reason",
  ar("An enzyme that requires a co-factor loses its catalytic activity when the co-factor is removed.",
     "Co-factors are the protein constituents of such enzymes."),
  ASSERTION_REASON, "C",
  "Co-factors and apoenzyme",
  "NCERT: enzymes may be composed of one or several polypeptide chains; in many cases non-protein constituents called "
  "co-factors are bound to the enzyme to make it catalytically active. The protein portion is called the apoenzyme. "
  "When the co-factor is removed from the enzyme, the catalytic activity of the enzyme is lost. So the Assertion is "
  "true, but co-factors are non-protein constituents.",
  ["A true", "R false – co-factors are non-protein; the protein part is the apoenzyme"],
  R_BIO("enzymes: co-factors"),
  why_others_wrong="A and B accept the false Reason; D rejects NCERT's statement that activity is lost on removing "
                   "the co-factor.",
  seconds=35)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("The activity of an enzyme declines both below and above its optimum temperature.",
     "In the presence of a competitive inhibitor, the substrate can still bind normally to the enzyme, because the "
     "inhibitor binds to a site other than the substrate-binding site."),
  STATEMENT_PAIR, "C",
  "Temperature and competitive inhibition",
  "NCERT: each enzyme shows its highest activity at a particular temperature and pH (the optimum); activity declines "
  "both below and above the optimum value. A competitive inhibitor closely resembles the substrate and, owing to this "
  "similarity, competes with the substrate for the substrate-binding site, so the substrate cannot bind and enzyme "
  "action declines.",
  ["Statement I → true", "Statement II → false (the inhibitor competes for the substrate-binding site)"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="A and D accept Statement II, which describes the opposite of competitive inhibition; B rejects "
                   "NCERT's statement about the optimum temperature.",
  seconds=40)

Z(BIO, "Enzyme classification", "Intermediate", "direct",
  "Peroxidase uses H₂O₂ to oxidise another substrate, the H₂O₂ itself being reduced to water. In NCERT's "
  "classification of enzymes, peroxidase belongs to the class:",
  ["Hydrolases", "Transferases", "Isomerases", "Oxidoreductases"], "D",
  "Oxidoreductases",
  "NCERT: oxidoreductases/dehydrogenases catalyse oxido-reduction between two substrates S and S′: S reduced + S′ "
  "oxidised → S oxidised + S′ reduced. In the peroxidase reaction one substrate is oxidised while H₂O₂ is reduced, "
  "which is exactly this pattern. (NCERT also names haem as the prosthetic group of peroxidase.)",
  ["One substrate oxidised + the other reduced → oxidoreductase"],
  R_BIO("enzymes: classification and nomenclature"),
  why_others_wrong="Hydrolases split bonds by adding water; transferases move a group other than hydrogen; isomerases "
                   "inter-convert isomers – none describes a redox reaction between two substrates.",
  seconds=35)

Z(BIO, "Proteins and amino acids", "Intermediate", "match_list",
  ml(("level of protein structure", "description in NCERT"), ["Primary", "Secondary", "Tertiary", "Quaternary"],
     ["Long chain folded upon itself like a hollow woollen ball",
      "Arrangement of individually folded subunits with respect to each other",
      "Sequence of amino acids, i.e. the positional information in a protein",
      "Portions of the thread arranged as a helix, like a revolving staircase"]),
  match_options(M("III", "IV", "I", "II"), [M("III", "I", "IV", "II"), M("IV", "III", "I", "II"),
                                            M("III", "IV", "II", "I")], "B"), "B",
  "Levels of protein structure",
  "NCERT: the primary structure is the sequence of amino acids (the positional information); in the secondary "
  "structure only some portions of the protein thread are arranged as a helix, similar to a revolving staircase; in "
  "the tertiary structure the long chain is folded upon itself like a hollow woollen ball; the quaternary structure "
  "is the manner in which individually folded polypeptides or subunits are arranged with respect to each other "
  "(e.g. adult haemoglobin).",
  ["Primary → III", "Secondary → IV", "Tertiary → I", "Quaternary → II"],
  R_BIO("proteins: structure of proteins"),
  why_others_wrong="A swaps secondary and tertiary; C swaps primary and secondary; D swaps tertiary and quaternary.",
  seconds=40)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Lecithin is a triglyceride.",
     "Lecithin is a phospholipid: besides glycerol and fatty acids, it contains phosphorus and a phosphorylated "
     "organic compound."),
  ASSERTION_REASON, "D",
  "Phospholipids",
  "NCERT: fatty acids esterified with glycerol form monoglycerides, diglycerides and triglycerides (fats and oils). "
  "Some lipids have phosphorus and a phosphorylated organic compound in them; these are phospholipids, found in cell "
  "membranes, and lecithin is one example. So lecithin is not a triglyceride; the Reason is true.",
  ["A false – lecithin is a phospholipid", "R true"],
  R_BIO("lipids"),
  why_others_wrong="A, B and C treat the Assertion as true, but a triglyceride has only glycerol esterified with "
                   "three fatty acids.",
  seconds=35)

Z(BIO, "Enzymes: properties and action", "Intermediate", "assertion_reason",
  ar("An enzyme molecule is used up when it converts one molecule of substrate into product.",
     "After the products are released from the enzyme–product complex, the free enzyme is ready to bind another "
     "molecule of substrate and run through the catalytic cycle once again."),
  ASSERTION_REASON, "D",
  "Catalytic cycle of an enzyme",
  "NCERT describes the catalytic cycle: the substrate binds the active site, the enzyme alters its shape to fit more "
  "tightly, the substrate's bonds are broken and an enzyme–product complex forms, and the products are released. The "
  "free enzyme is then ready to bind another substrate molecule and run through the cycle again. Hence the enzyme is "
  "not used up; the Assertion is false.",
  ["A false – the enzyme is regenerated", "R true"],
  R_BIO("enzymes: nature of enzyme action"),
  why_others_wrong="A, B and C accept the Assertion, which is contradicted by the catalytic cycle described in R.",
  seconds=30)

Z(BIO, "Proteins and amino acids", "Advanced", "multi_statement",
  ms("A protein is made of two identical polypeptide chains. Each chain is folded into its own three-dimensional "
     "shape, and the two folded chains are arranged with respect to each other in a definite manner. Which of the "
     "following statements about this protein are correct?",
     ["It shows a quaternary structure.",
      "It has two N-terminal amino acids, one on each chain.",
      "Its primary structure is the sequence of amino acids in its chains.",
      "It is a homopolymer, because its two chains are identical.",
      "Its helical portions are left-handed helices."]),
  ["(a), (b), (c) and (e) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (d) only"], "B",
  "Protein structure applied",
  "NCERT: a protein's left end is the first amino acid (N-terminal) and its right end the last (C-terminal), so each "
  "polypeptide chain has its own N-terminal amino acid. The primary structure is the sequence of amino acids. When "
  "individually folded polypeptides (subunits) are arranged with respect to each other, the protein has a quaternary "
  "structure. Each chain is still made of different kinds of amino acids, so the protein is a heteropolymer – "
  "identical chains do not make it a homopolymer. In proteins, only right-handed helices are observed.",
  ["(a) true", "(b) true", "(c) true", "(d) false – amino-acid chains are heteropolymers",
   "(e) false – only right-handed helices"],
  R_BIO("proteins: structure of proteins"),
  why_others_wrong="A adds left-handed helices; C and D add the homopolymer claim and leave out a true statement.",
  seconds=60)
ms_check("abc", ["(a), (b), (c) and (e) only", "(a), (b) and (c) only", "(b), (c) and (d) only",
                 "(a), (c) and (d) only"], "B")

Z(BIO, "Enzymes: properties and action", "Advanced", "assertion_reason",
  ar("A human enzyme that has been heated to 70 °C does not regain its activity when it is cooled back to 37 °C.",
     "High temperature destroys enzymatic activity because proteins are denatured by heat."),
  ASSERTION_REASON, "A",
  "Effect of high temperature on enzymes",
  "NCERT: enzymes of most organisms get damaged at high temperatures (say above 40 °C). Low temperature preserves the "
  "enzyme in a temporarily inactive state, whereas high temperature destroys enzymatic activity because proteins are "
  "denatured by heat. Denaturation destroys the enzyme's structure, so cooling does not bring the activity back – "
  "unlike the reversible effect of cold.",
  ["A true", "R true", "Heat denatures the protein → activity destroyed, not just paused → R explains A"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="B is wrong because denaturation by heat is the very reason activity is not regained; C and D are "
                   "wrong because both statements are true.",
  seconds=40)

Z(BIO, "Nucleic acids", "Advanced", "multi_statement",
  ms("A nucleic acid sample, on complete hydrolysis, gives deoxyribose, phosphoric acid and the bases adenine, "
     "guanine, cytosine and thymine. Which of the following statements are correct?",
     ["The sample is DNA.",
      "It contains two kinds of substituted purines.",
      "Thymine is a substituted pyrimidine.",
      "The sample is RNA, because it contains adenine and guanine.",
      "The sugar obtained is a hexose."]),
  ["(a) and (b) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (e) only"], "B",
  "Identifying a nucleic acid",
  "NCERT: a nucleic acid containing deoxyribose is called DNA, while one containing ribose is RNA. Adenine and guanine "
  "are substituted purines; uracil, cytosine and thymine are substituted pyrimidines. The sugar in polynucleotides is "
  "either ribose or 2′-deoxyribose, both pentoses.",
  ["(a) deoxyribose → DNA – true", "(b) adenine + guanine → two purines – true", "(c) true",
   "(d) false – the sugar, not the purines, decides DNA versus RNA", "(e) false – pentose"],
  R_BIO("nucleic acids"),
  why_others_wrong="A leaves out (c); C includes (d) and leaves out (a); D includes (e) and leaves out (b).",
  seconds=55)
ms_check("abc", ["(a) and (b) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (e) only"], "B")

Z(BIO, "Enzymes: properties and action", "Advanced", "statement_pair",
  sp("Every enzyme is a protein.",
     "Some nucleic acids that behave like enzymes are called ribozymes."),
  STATEMENT_PAIR, "D",
  "Nature of enzymes",
  "NCERT: almost all enzymes are proteins. There are some nucleic acids that behave like enzymes; these are called "
  "ribozymes. Because of ribozymes, the absolute claim 'every enzyme is a protein' is false.",
  ["Statement I → false ('almost all', not every)", "Statement II → true"],
  R_BIO("enzymes"),
  why_others_wrong="A and C accept the absolute Statement I, which the existence of ribozymes contradicts; B rejects "
                   "NCERT's statement about ribozymes.",
  seconds=30)

Z(BIO, "Carbohydrates and lipids", "Advanced", "match_list",
  ml(("biomolecule", "building blocks"), ["Inulin", "Insulin", "Chitin", "Cellulose"],
     ["Glucose", "Fructose", "Amino acids", "Amino-sugars and chemically modified sugars"]),
  match_options(M("II", "III", "IV", "I"), [M("I", "III", "IV", "II"), M("III", "II", "IV", "I"),
                                            M("II", "IV", "III", "I")], "A"), "A",
  "Monomers of biopolymers",
  "NCERT: inulin is a polymer of fructose; insulin is a protein (a hormone), i.e. a polymer of amino acids; complex "
  "polysaccharides such as chitin of the arthropod exoskeleton have amino-sugars and chemically modified sugars (e.g. "
  "glucosamine, N-acetyl galactosamine) as building blocks; cellulose is a homopolymer of glucose.",
  ["Inulin → fructose (II)", "Insulin → amino acids (III)", "Chitin → amino-sugars (IV)", "Cellulose → glucose (I)"],
  R_BIO("polysaccharides; proteins"),
  why_others_wrong="B swaps inulin and cellulose; C confuses inulin with insulin; D swaps insulin and chitin.",
  seconds=40)

Z(BIO, "Enzyme classification", "Advanced", "multi_statement",
  ms("Which of the following enzymes are placed in the correct NCERT class?",
     ["An enzyme that hydrolyses the ester bonds of a fat – Hydrolase",
      "An enzyme that transfers an amino group (not hydrogen) from one substrate to another – Transferase",
      "An enzyme that removes a water molecule from a substrate, leaving a double bond – Ligase",
      "An enzyme that converts an optical isomer of a compound into its mirror-image form – Isomerase",
      "An enzyme that moves hydrogen from one substrate to another, oxidising the first – Transferase"]),
  ["(a), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"], "B",
  "Applying the enzyme classes",
  "NCERT: hydrolases hydrolyse ester, ether, peptide, glycosidic and other bonds; transferases transfer a group G "
  "other than hydrogen between two substrates; lyases remove groups by mechanisms other than hydrolysis, leaving "
  "double bonds; isomerases inter-convert optical, geometric or positional isomers; oxido-reduction between two "
  "substrates (including transfer of hydrogen) is catalysed by oxidoreductases/dehydrogenases.",
  ["(a) true", "(b) true", "(c) false – lyase", "(d) true", "(e) false – oxidoreductase"],
  R_BIO("enzymes: classification and nomenclature"),
  why_others_wrong="A includes (c), which is a lyase reaction; C and D include (e), a redox (hydrogen-transfer) "
                   "reaction that is not a transferase reaction.",
  seconds=60)
ms_check("abd", ["(a), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only",
                 "(a), (b), (d) and (e) only"], "B")

# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

_tlc, _frc = 6000, 2400
_ic = _tlc - _frc
assert _ic == 3600
Z(BRE, "Respiratory volumes", "Basic", "numerical",
  "Spirometry of a healthy adult gives a total lung capacity of 6000 mL and a functional residual capacity of "
  "2400 mL. What is his inspiratory capacity?",
  ["8400 mL", f"{_ic} mL", "2400 mL", "4800 mL"], "B",
  "Inspiratory capacity from TLC and FRC",
  "NCERT: inspiratory capacity (IC) = TV + IRV; functional residual capacity (FRC) = ERV + RV; total lung capacity "
  "(TLC) = RV + ERV + TV + IRV. Hence TLC = IC + FRC, and IC = 6000 − 2400 = 3600 mL.",
  ["TLC = (TV + IRV) + (ERV + RV) = IC + FRC", "IC = 6000 − 2400 = 3600 mL"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="Lung capacity splits at the end of a normal expiration: below it is FRC, above it is IC.",
  why_others_wrong="8400 mL adds FRC to TLC; 2400 mL is the FRC itself; 4800 mL subtracts a residual volume of "
                   "1200 mL from TLC, which gives the vital capacity, not the inspiratory capacity.",
  seconds=40, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Basic", "direct",
  "NCERT lists the steps of respiration in order. Which step comes LAST in this list?",
  ["Diffusion of gases across the alveolar membrane",
   "Utilisation of O₂ by the cells for catabolic reactions and the resultant release of CO₂",
   "Transport of gases by the blood", "Pulmonary ventilation (breathing)"], "B",
  "Steps of respiration",
  "NCERT: respiration involves (i) breathing or pulmonary ventilation; (ii) diffusion of gases (O₂ and CO₂) across "
  "the alveolar membrane; (iii) transport of gases by the blood; (iv) diffusion of O₂ and CO₂ between blood and "
  "tissues; and (v) utilisation of O₂ by the cells for catabolic reactions and resultant release of CO₂ (cellular "
  "respiration).",
  ["Step (v), cellular respiration, is last"],
  R_BRE("mechanism of breathing (steps of respiration)"),
  why_others_wrong="Breathing is step (i), diffusion across the alveolar membrane step (ii) and transport by blood "
                   "step (iii).",
  seconds=25)

Z(BRE, "Mechanism of breathing", "Basic", "direct",
  "According to NCERT, on an average a healthy human breathes about how many times per minute?",
  ["12–16 times", "30–40 times", "70–75 times", "4–6 times"], "A",
  "Breathing rate",
  "NCERT: on an average, a healthy human breathes 12–16 times per minute. (70–75 per minute is the rate of action "
  "potentials generated by the SA node, i.e. the heart rate range.)",
  ["Breathing rate → 12–16 per minute"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="30–40 per minute is far above the NCERT figure; 70–75 per minute is the SA-node (heart) rate; "
                   "4–6 per minute is far too low.",
  seconds=20)

Z(BRE, "Respiratory volumes", "Basic", "statement_pair",
  sp("A healthy man can inspire or expire approximately 6000 to 8000 mL of air per minute.",
     "The vital capacity includes the residual volume."),
  STATEMENT_PAIR, "C",
  "Minute volume and vital capacity",
  "NCERT: tidal volume is approximately 500 mL, i.e. a healthy man can inspire or expire approximately 6000 to "
  "8000 mL of air per minute. Vital capacity is ERV + TV + IRV, the maximum volume of air a person can breathe in "
  "after a forced expiration; the residual volume, which remains even after a forcible expiration, is not part of it.",
  ["Statement I → true", "Statement II → false (VC = ERV + TV + IRV)"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="A and D accept that the vital capacity includes the residual volume; B rejects NCERT's figure of "
                   "6000–8000 mL per minute.",
  seconds=30)

_full, _half = 600, 400
_o2 = _full * 4 + _half * 2
assert _o2 == 3200
Z(BRE, "Exchange and transport of gases", "Intermediate", "numerical",
  "Each haemoglobin molecule can carry a maximum of four molecules of O₂. In a sample, 600 haemoglobin molecules are "
  "fully saturated with O₂ and another 400 are exactly half saturated. How many O₂ molecules are bound in all?",
  ["4000", f"{_o2}", "2400", "1600"], "B",
  "Oxygen binding by haemoglobin",
  "NCERT: each haemoglobin molecule can carry a maximum of four molecules of O₂. Fully saturated molecules carry 4 "
  "each and half-saturated molecules carry 2 each: 600 × 4 + 400 × 2 = 2400 + 800 = 3200.",
  ["600 × 4 = 2400", "400 × 2 = 800", "Total = 3200"],
  R_BRE("transport of oxygen"),
  why_others_wrong="4000 treats all 1000 molecules as fully saturated; 2400 counts only the fully saturated "
                   "molecules; 1600 takes the maximum load as two O₂ per haemoglobin.",
  seconds=40, verified_by=RECOMPUTED)

Z(BRE, "Mechanism of breathing", "Intermediate", "assertion_reason",
  ar("When the diaphragm and the external inter-costal muscles contract, air flows into the lungs.",
     "Their contraction increases the thoracic volume and hence the pulmonary volume, which decreases the "
     "intra-pulmonary pressure to less than the atmospheric pressure."),
  ASSERTION_REASON, "A",
  "Inspiration",
  "NCERT: contraction of the diaphragm increases the volume of the thoracic chamber in the antero-posterior axis, and "
  "contraction of the external inter-costal muscles lifts the ribs and sternum, increasing it in the dorso-ventral "
  "axis. The overall increase in thoracic volume causes a similar increase in pulmonary volume, which decreases the "
  "intra-pulmonary pressure to less than the atmospheric pressure; this forces air from outside into the lungs.",
  ["A true", "R true", "Volume ↑ → pressure falls below atmospheric → air enters → R explains A"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="B is wrong because the pressure gradient created by the volume increase is what drives air into "
                   "the lungs; C and D are wrong because both statements are true.",
  seconds=35)

Z(BRE, "Exchange and transport of gases", "Intermediate", "match_list",
  ml(("respiratory gas and its form of transport", "approximate per cent carried that way"),
     ["O₂ bound to haemoglobin in RBCs", "O₂ dissolved in plasma", "CO₂ as bicarbonate", "CO₂ dissolved in plasma"],
     ["7", "70", "3", "97"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "I", "II", "III"), M("II", "III", "IV", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Transport of O₂ and CO₂",
  "NCERT: about 97 per cent of O₂ is transported by RBCs in the blood; the remaining 3 per cent is carried in a "
  "dissolved state through the plasma. Nearly 20–25 per cent of CO₂ is transported by RBCs (as carbamino-"
  "haemoglobin), about 70 per cent is carried as bicarbonate and about 7 per cent in a dissolved state through "
  "plasma.",
  ["O₂ in RBCs → 97 (IV)", "O₂ in plasma → 3 (III)", "CO₂ as bicarbonate → 70 (II)", "CO₂ in plasma → 7 (I)"],
  R_BRE("transport of gases"),
  why_others_wrong="A swaps the two dissolved fractions; B swaps the haemoglobin-bound O₂ and the bicarbonate; C swaps "
                   "bicarbonate and dissolved CO₂.",
  seconds=35)

Z(BRE, "Exchange and transport of gases", "Intermediate", "statement_pair",
  sp("According to the NCERT table of partial pressures, the pO₂ of the tissues equals the pO₂ of deoxygenated "
     "blood.",
     "According to the same table, the pCO₂ of the tissues equals the pCO₂ of deoxygenated blood."),
  STATEMENT_PAIR, "A",
  "Reading the partial-pressure table",
  "NCERT table (mm Hg): pO₂ – atmospheric air 159, alveoli 104, deoxygenated blood 40, oxygenated blood 95, tissues "
  "40; pCO₂ – atmospheric air 0.3, alveoli 40, deoxygenated blood 45, oxygenated blood 40, tissues 45. Blood leaving "
  "the tissues has come to the same partial pressures as the tissues: pO₂ 40 and pCO₂ 45.",
  ["Tissues pO₂ 40 = deoxygenated blood pO₂ 40 → I true", "Tissues pCO₂ 45 = deoxygenated blood pCO₂ 45 → II true"],
  R_BRE("exchange of gases"),
  why_others_wrong="Both equalities are read directly from the NCERT table, so B, C and D are wrong.",
  seconds=40)

Z(BRE, "Mechanism of breathing", "Intermediate", "match_list",
  ml(("event", "effect"),
     ["Contraction of the diaphragm", "Contraction of the external inter-costal muscles",
      "Relaxation of the diaphragm and the inter-costal muscles", "Contraction of additional muscles in the abdomen"],
     ["Increases the strength of inspiration and expiration",
      "Thoracic and pulmonary volumes decrease and air is expelled",
      "Ribs and sternum are lifted, increasing the volume in the dorso-ventral axis",
      "Volume of the thoracic chamber increases in the antero-posterior axis"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("II", "III", "IV", "I")], "B"), "B",
  "Muscles of breathing",
  "NCERT: contraction of the diaphragm increases the volume of the thoracic chamber in the antero-posterior axis; "
  "contraction of the external inter-costal muscles lifts the ribs and sternum, increasing the volume in the "
  "dorso-ventral axis; relaxation of the diaphragm and inter-costal muscles reduces the thoracic and pulmonary "
  "volumes, leading to expiration; additional muscles in the abdomen can increase the strength of inspiration and "
  "expiration.",
  ["Diaphragm → antero-posterior (IV)", "External inter-costals → dorso-ventral (III)", "Relaxation → expiration (II)",
   "Abdominal muscles → strength (I)"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A swaps the two axes; C swaps relaxation and the abdominal muscles; D gives the diaphragm the "
                   "effect of relaxation.",
  seconds=40)

_tv, _irv, _erv, _rv = 500, 3000, 1000, 1200
_vals = {"IC": _tv + _irv, "VC": _erv + _tv + _irv, "FRC": _erv + _rv, "TLC": _rv + _erv + _tv + _irv,
         "EC": _tv + _erv}
assert _vals == {"IC": 3500, "VC": 4500, "FRC": 2200, "TLC": 5700, "EC": 1500}
_opts_vol = ["(a), (b), (c) and (e) only", "(a), (b) and (d) only", "(b), (c), (d) and (e) only",
             "(a), (c) and (e) only"]
Z(BRE, "Respiratory volumes", "Advanced", "multi_statement",
  ms("A healthy adult has a tidal volume of 500 mL, an inspiratory reserve volume of 3000 mL, an expiratory reserve "
     "volume of 1000 mL and a residual volume of 1200 mL. Which of the following statements are correct?",
     ["His inspiratory capacity is 3500 mL.", "His vital capacity is 4500 mL.",
      "His functional residual capacity is 2200 mL.", "His total lung capacity is 5200 mL.",
      "His expiratory capacity is 1500 mL."]),
  _opts_vol, "A",
  "Respiratory capacities",
  "NCERT definitions: IC = TV + IRV = 3500 mL; VC = ERV + TV + IRV = 4500 mL; FRC = ERV + RV = 2200 mL; TLC = RV + "
  "ERV + TV + IRV = 5700 mL (not 5200); EC = TV + ERV = 1500 mL.",
  ["IC 3500 ✓", "VC 4500 ✓", "FRC 2200 ✓", "TLC 5700, so (d) ✗", "EC 1500 ✓"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="B and C accept a TLC of 5200 mL, which leaves out the expiratory reserve volume; D leaves out the "
                   "correct vital capacity (b).",
  seconds=90)
ms_check("abce", _opts_vol, "A")

Z(BRE, "Exchange and transport of gases", "Advanced", "statement_pair",
  sp("At the alveoli, O₂ diffuses from the alveolar air into the blood while CO₂ diffuses from the blood into the "
     "alveolar air, each gas moving from a higher to a lower partial pressure.",
     "At the tissues, as at the alveoli, CO₂ diffuses out of the blood."),
  STATEMENT_PAIR, "C",
  "Direction of gas diffusion",
  "NCERT: pO₂ is 104 mm Hg in the alveoli and 40 in deoxygenated blood, while pCO₂ is 45 in deoxygenated blood and 40 "
  "in the alveoli, so at the alveoli O₂ enters and CO₂ leaves the blood. At the tissues the pCO₂ is 45 mm Hg and "
  "that of oxygenated blood 40, so CO₂ diffuses from the tissues into the blood – the opposite direction to that at "
  "the alveoli.",
  ["Statement I → true", "Statement II → false (at the tissues CO₂ enters the blood)"],
  R_BRE("exchange of gases"),
  why_others_wrong="A and D accept Statement II, which reverses the direction of CO₂ movement at the tissues; B "
                   "rejects Statement I, which follows directly from the NCERT partial pressures.",
  seconds=40)

Z(BRE, "Respiratory volumes", "Advanced", "direct",
  "Which of the following respiratory capacities includes the residual volume?",
  ["Vital capacity", "Functional residual capacity", "Inspiratory capacity", "Expiratory capacity"], "B",
  "Composition of capacities",
  "NCERT: vital capacity = ERV + TV + IRV; inspiratory capacity = TV + IRV; expiratory capacity = TV + ERV; "
  "functional residual capacity = ERV + RV. Of these, only the functional residual capacity (and, besides these, the "
  "total lung capacity) includes the residual volume.",
  ["VC, IC, EC → no RV", "FRC = ERV + RV → includes RV"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="Vital, inspiratory and expiratory capacities are all made of air that can be moved in breathing; "
                   "none of them contains the residual volume.",
  seconds=35)

Z(BRE, "Regulation and disorders", "Advanced", "assertion_reason",
  ar("In a person with emphysema, the exchange of gases in the lungs becomes less efficient.",
     "In emphysema, the alveolar walls are damaged, due to which the respiratory surface is decreased."),
  ASSERTION_REASON, "A",
  "Emphysema",
  "NCERT: emphysema is a chronic disorder in which alveolar walls are damaged, due to which the respiratory surface is "
  "decreased; cigarette smoking is one of its major causes. Since the alveoli are the primary sites of exchange of "
  "gases, a smaller respiratory surface means less gas exchange, so R explains A.",
  ["A true", "R true", "Damaged alveolar walls → less respiratory surface → less exchange → R explains A"],
  R_BRE("disorders of respiratory system"),
  why_others_wrong="B is wrong because the reduced respiratory surface is the cause of the poorer exchange; C and D "
                   "are wrong because both statements are true.",
  seconds=35)

# ================================================================ Body Fluids and Circulation (B5 I7 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "According to NCERT, the red blood cells (erythrocytes) of most mammals are:",
  ["Spherical and nucleated", "Oval and nucleated", "Biconcave and devoid of a nucleus",
   "Biconvex and multinucleate"], "C",
  "Shape of erythrocytes",
  "NCERT: erythrocytes are the most abundant of all the cells in blood. They are formed in the red bone marrow in "
  "adults, are devoid of a nucleus in most of the mammals and are biconcave in shape.",
  ["Most mammals → RBCs biconcave, without a nucleus"],
  R_BFC("formed elements: erythrocytes"),
  why_others_wrong="A and B describe nucleated RBCs, not those of most mammals; D is not a shape NCERT describes for "
                   "RBCs.",
  seconds=20)

Z(BFC, "Human heart", "Basic", "direct",
  "In the human heart, the opening between the left atrium and the left ventricle is guarded by the:",
  ["Tricuspid valve", "Semilunar valve", "Inter-atrial septum", "Bicuspid (mitral) valve"], "D",
  "Valves of the heart",
  "NCERT: the opening between the right atrium and the right ventricle is guarded by a valve formed of three muscular "
  "flaps or cusps, the tricuspid valve, whereas a bicuspid or mitral valve guards the opening between the left atrium "
  "and the left ventricle. The openings of the right and left ventricles into the pulmonary artery and the aorta are "
  "provided with semilunar valves.",
  ["Left atrio-ventricular opening → bicuspid (mitral) valve"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="The tricuspid valve is on the right side; semilunar valves guard the exits into the pulmonary "
                   "artery and aorta; the inter-atrial septum is a wall between the atria, not a valve.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "Which leucocytes, besides secreting histamine, serotonin and heparin, are described by NCERT as being involved in "
  "inflammatory reactions?",
  ["Neutrophils", "Basophils", "Lymphocytes", "Monocytes"], "B",
  "Basophils",
  "NCERT: basophils secrete histamine, serotonin, heparin, etc., and are involved in inflammatory reactions. "
  "Neutrophils and monocytes are phagocytic cells, and lymphocytes (B and T forms) are responsible for immune "
  "responses.",
  ["Histamine, serotonin, heparin + inflammatory reactions → basophils"],
  R_BFC("formed elements: leucocytes"),
  why_others_wrong="Neutrophils and monocytes are described as phagocytes; lymphocytes are responsible for immune "
                   "responses of the body.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Erythrocytes are the most abundant of all the cells in blood.",
     "Leucocytes are generally short-lived."),
  STATEMENT_PAIR, "A",
  "Erythrocytes and leucocytes",
  "NCERT: erythrocytes are the most abundant of all the cells in blood (5 to 5.5 million per mm³ in a healthy adult "
  "man). Leucocytes are colourless due to the lack of haemoglobin, are nucleated, relatively lesser in number "
  "(6000–8000 per mm³) and generally short-lived.",
  ["Statement I → true", "Statement II → true"],
  R_BFC("formed elements"),
  why_others_wrong="Both statements are NCERT's own description, so B, C and D are wrong.",
  seconds=25)

Z(BFC, "Blood and blood groups", "Basic", "match_list",
  ml(("ABO blood group", "antigens on the RBCs"), ["A", "B", "AB", "O"],
     ["Neither A nor B", "Both A and B", "B only", "A only"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("II", "III", "IV", "I")], "C"), "C",
  "Antigens of the ABO groups",
  "NCERT: ABO grouping is based on the presence or absence of two surface antigens, A and B, on the RBCs. Group A has "
  "antigen A, group B antigen B, group AB both A and B, and group O neither (nil).",
  ["A → A only (IV)", "B → B only (III)", "AB → both (II)", "O → neither (I)"],
  R_BFC("blood groups: ABO grouping"),
  why_others_wrong="A swaps groups A and B; B swaps AB and O; D swaps groups A and AB.",
  seconds=25)

_sv, _hr = 70, 72
_per_ventricle = _sv * _hr
_both = 2 * _per_ventricle
assert (_per_ventricle, _both) == (5040, 10080)
Z(BFC, "Cardiac cycle and ECG", "Intermediate", "numerical",
  "In a person, each ventricle pumps out 70 mL of blood in every cardiac cycle and the heart beats 72 times per "
  "minute. What total volume of blood do the two ventricles together pump out in one minute?",
  ["5040 mL", "2520 mL", "140 mL", f"{_both} mL"], "D",
  "Stroke volume and cardiac output",
  "NCERT: during a cardiac cycle each ventricle pumps out approximately 70 mL of blood (the stroke volume). The "
  "stroke volume multiplied by the heart rate gives the cardiac output, the volume of blood pumped out by EACH "
  "ventricle per minute: 70 × 72 = 5040 mL. Both ventricles together pump 2 × 5040 = 10080 mL per minute (one "
  "stream to the lungs, one to the body).",
  ["Per ventricle: 70 × 72 = 5040 mL min⁻¹ (cardiac output)", "Both ventricles: 2 × 5040 = 10080 mL min⁻¹"],
  R_BFC("cardiac cycle"),
  shortcut="Cardiac output is defined per ventricle; double it for the whole heart.",
  why_others_wrong="5040 mL is the cardiac output of one ventricle; 2520 mL halves instead of doubling; 140 mL is the "
                   "output of the two ventricles in a single beat.",
  seconds=45, verified_by=RECOMPUTED)

Z(BFC, "Human heart", "Intermediate", "assertion_reason",
  ar("During ventricular systole, blood is not pushed back from the right ventricle into the right atrium.",
     "The tricuspid valve guarding the opening between the right atrium and the right ventricle allows the flow of "
     "blood only in one direction, and it is closed by the attempted backflow."),
  ASSERTION_REASON, "A",
  "One-way valves",
  "NCERT: the valves in the heart allow the flow of blood only in one direction, i.e. from the atria to the "
  "ventricles and from the ventricles to the pulmonary artery or aorta, and prevent backward flow. As the ventricles "
  "contract, the rising ventricular pressure closes the tricuspid and bicuspid valves due to the attempted backflow "
  "of blood into the atria. So the closed tricuspid valve is why blood does not return to the right atrium.",
  ["A true", "R true", "Closed one-way tricuspid valve → no backflow → R explains A"],
  R_BFC("human heart; cardiac cycle"),
  why_others_wrong="B is wrong because the one-way tricuspid valve is the direct cause of the Assertion; C and D are "
                   "wrong because both statements are true.",
  seconds=35)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "statement_pair",
  sp("During joint diastole, blood from the pulmonary veins and the vena cava flows through the atria into the "
     "ventricles, because the tricuspid and bicuspid valves are open.",
     "The simultaneous contraction of the atria increases the flow of blood into the ventricles by about 30 per "
     "cent."),
  STATEMENT_PAIR, "A",
  "Filling of the ventricles",
  "NCERT: in joint diastole, all four chambers are relaxed; as the tricuspid and bicuspid valves are open, blood from "
  "the pulmonary veins and vena cava flows into the left and right ventricles respectively through the left and right "
  "atria. The SAN then stimulates both atria to contract simultaneously (atrial systole), which increases the flow of "
  "blood into the ventricles by about 30 per cent.",
  ["Statement I → true", "Statement II → true"],
  R_BFC("cardiac cycle"),
  why_others_wrong="Both are NCERT statements; most ventricular filling happens in joint diastole and atrial systole "
                   "adds about 30 per cent, so B, C and D are wrong.",
  seconds=35)

Z(BFC, "Human heart", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human heart are correct?",
     ["It has two relatively small upper chambers, the atria, and two larger lower chambers, the ventricles.",
      "The right and left atria are separated by a thin, muscular inter-atrial septum.",
      "The atrium and the ventricle of the same side are separated by a thick fibrous atrio-ventricular septum.",
      "The bicuspid valve guards the opening between the right atrium and the right ventricle.",
      "The sino-atrial node lies in the left atrium."]),
  ["(a) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only"], "C",
  "Chambers and septa of the heart",
  "NCERT: the heart has four chambers – two relatively small upper chambers called atria and two larger lower "
  "chambers called ventricles. A thin, muscular wall called the inter-atrial septum separates the right and left "
  "atria, whereas a thick-walled inter-ventricular septum separates the ventricles. The atrium and the ventricle of "
  "the same side are separated by a thick fibrous tissue, the atrio-ventricular septum. The tricuspid valve guards "
  "the right atrio-ventricular opening, and the SAN lies in the right upper corner of the right atrium.",
  ["(a) true", "(b) true", "(c) true", "(d) false – tricuspid on the right", "(e) false – right atrium"],
  R_BFC("human circulatory system: heart"),
  why_others_wrong="A includes (d); B includes (e) and leaves out (a); D includes (d).",
  seconds=50)
ms_check("abc", ["(a) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only"],
         "C")

Z(BFC, "Circulatory disorders", "Intermediate", "assertion_reason",
  ar("A heart attack is the condition in which the heart muscle is suddenly damaged by an inadequate blood supply.",
     "A heart attack and cardiac arrest are the same condition, in which the heart stops beating."),
  ASSERTION_REASON, "C",
  "Heart attack versus cardiac arrest",
  "NCERT: cardiac arrest is when the heart stops beating, whereas a heart attack is when the heart muscle is suddenly "
  "damaged by an inadequate blood supply. The two are different, so the Reason is false.",
  ["A true", "R false – cardiac arrest is a different condition"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="A and B accept the false Reason; D rejects NCERT's definition of a heart attack.",
  seconds=30)

Z(BFC, "Double circulation and regulation", "Intermediate", "assertion_reason",
  ar("During a sudden fright, the heart beats faster and more forcefully.",
     "Neural signals through the sympathetic nerves can increase the rate of heart beat and the strength of "
     "ventricular contraction, and adrenal medullary hormones can also increase the cardiac output."),
  ASSERTION_REASON, "A",
  "Neural and hormonal regulation of the heart",
  "NCERT: neural signals through the sympathetic nerves (part of the ANS) can increase the rate of heart beat, the "
  "strength of ventricular contraction and thereby the cardiac output; adrenal medullary hormones can also increase "
  "the cardiac output. In an emergency such as fright, the sympathetic system and the adrenal medullary hormones "
  "(the emergency hormones) are activated, which is why the heart beats faster and more strongly.",
  ["A true", "R true", "Sympathetic + adrenal medulla → rate and strength ↑ → R explains A"],
  R_BFC("regulation of cardiac activity") + "; Class 11 Biology, 'Chemical Coordination and Integration', adrenal "
  "gland",
  why_others_wrong="B is wrong because the sympathetic and adrenal medullary effects are what produce the faster, "
                   "stronger beat; C and D are wrong because both statements are true.",
  seconds=40)

Z(BFC, "Blood and blood groups", "Intermediate", "match_list",
  ml(("component", "approximate share given in NCERT"),
     ["Plasma, as a share of blood", "Water, as a share of plasma", "Proteins, as a share of plasma",
      "Neutrophils, as a share of total leucocytes"],
     ["60–65 per cent", "6–8 per cent", "90–92 per cent", "About 55 per cent"]),
  match_options(M("IV", "III", "II", "I"), [M("I", "III", "II", "IV"), M("IV", "II", "III", "I"),
                                            M("III", "IV", "II", "I")], "B"), "B",
  "Composition of blood",
  "NCERT: plasma is a straw-coloured, viscous fluid constituting nearly 55 per cent of the blood; 90–92 per cent of "
  "plasma is water and proteins contribute 6–8 per cent of it. Neutrophils are the most abundant leucocytes, 60–65 "
  "per cent of the total WBCs.",
  ["Plasma → ~55% of blood (IV)", "Water → 90–92% of plasma (III)", "Proteins → 6–8% of plasma (II)",
   "Neutrophils → 60–65% of WBCs (I)"],
  R_BFC("blood: plasma; formed elements"),
  why_others_wrong="A swaps plasma and neutrophils; C swaps water and proteins; D swaps plasma and water.",
  seconds=40)

_opts_rep = ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (b) and (c) only", "(a), (b), (c) and (e) only"]
Z(BFC, "Blood and blood groups", "Advanced", "multi_statement",
  ms("An adult man's blood report shows: RBCs 3.5 million per mm³, haemoglobin 9 g per 100 mL, WBCs 7000 per mm³ and "
     "platelets 2,00,000 per mm³. Comparing with the normal values given in NCERT, which of the following statements "
     "are correct?",
     ["His RBC count is below the normal value.",
      "His haemoglobin is below the normal range.",
      "His WBC count is within the normal range.",
      "His platelet count is below normal, so he is likely to have clotting disorders.",
      "His low haemoglobin can reduce the transport of respiratory gases by his blood."]),
  _opts_rep, "D",
  "Reading a blood report",
  "NCERT normal values: RBCs 5 to 5.5 million per mm³ (healthy adult man); haemoglobin 12–16 g per 100 mL; WBCs "
  "6000–8000 per mm³; platelets 1,50,000–3,50,000 per mm³. Haemoglobin molecules play a significant role in the "
  "transport of respiratory gases. So 3.5 million RBCs and 9 g haemoglobin are low, 7000 WBCs is normal, and 2,00,000 "
  "platelets is within the normal range.",
  ["(a) 3.5 < 5 million → true", "(b) 9 < 12 g → true", "(c) 7000 within 6000–8000 → true",
   "(d) 2,00,000 within 1.5–3.5 lakh → false", "(e) true"],
  R_BFC("blood: formed elements"),
  why_others_wrong="A and B include (d), though the platelet count is normal; C leaves out the true statement (e).",
  seconds=75)
ms_check("abce", _opts_rep, "D")

Z(BFC, "Double circulation and regulation", "Advanced", "assertion_reason",
  ar("Crocodiles, being reptiles, show incomplete double circulation like other reptiles.",
     "Amphibians and the reptiles, except crocodiles, have a three-chambered heart in which a single ventricle "
     "receives both oxygenated and deoxygenated blood."),
  ASSERTION_REASON, "D",
  "Crocodiles as an exception",
  "NCERT: amphibians and the reptiles (except crocodiles) have a three-chambered heart with two atria and a single "
  "ventricle, where oxygenated and deoxygenated blood get mixed, so they show incomplete double circulation. "
  "Crocodiles, birds and mammals possess a four-chambered heart. Hence the Assertion is false; the Reason, with its "
  "exception, is true.",
  ["A false – crocodiles have a four-chambered heart", "R true"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A, B and C accept the Assertion; the Reason itself excludes crocodiles from the three-chambered "
                   "group.",
  seconds=40)

_opts_reg = ["(a), (b) and (d) only", "(c) and (e) only", "(a), (b) and (e) only", "(a), (d) and (e) only"]
Z(BFC, "Double circulation and regulation", "Advanced", "multi_statement",
  ms("In a person, the parasympathetic nerve supply to the heart is blocked, and at the same time the level of "
     "adrenal medullary hormones in the blood rises. Which of the following are expected?",
     ["The rate of heart beat tends to rise.",
      "The cardiac output can increase.",
      "The SAN stops generating action potentials, because neural signals are needed to start each beat.",
      "The speed of conduction of the action potential decreases.",
      "The heart keeps beating, since its normal activities are regulated intrinsically by the nodal tissue."]),
  _opts_reg, "C",
  "Regulation of cardiac activity",
  "NCERT: normal activities of the heart are regulated intrinsically (auto-regulated) by the nodal tissue, so the "
  "heart is myogenic. Parasympathetic signals decrease the rate of heart beat, the speed of conduction of the action "
  "potential and thereby the cardiac output; removing them lets the rate rise. Adrenal medullary hormones can "
  "increase the cardiac output.",
  ["(a) true – braking influence removed", "(b) true – hormones raise output", "(c) false – nodal tissue is "
   "autoexcitable", "(d) false – it is the parasympathetic input that slows conduction", "(e) true"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="A and D include (d), which is the effect of parasympathetic stimulation, not of its blocking; B "
                   "includes (c), which contradicts the myogenic nature of the heart.",
  seconds=60)
ms_check("abe", _opts_reg, "C")

Z(BFC, "Cardiac cycle and ECG", "Advanced", "direct",
  "Suppose the atrio-ventricular node (AVN) of a person's heart failed to conduct impulses while the SAN worked "
  "normally. Which consequence follows from the NCERT account of the cardiac cycle?",
  ["The SAN would stop generating action potentials",
   "The atria would still be stimulated to contract, but the SAN's action potential would not be conducted to the "
   "ventricular side",
   "The ventricles would contract before the atria in every cycle",
   "The bundle of His would conduct the impulse directly from the SAN to the Purkinje fibres"], "B",
  "Conduction in the heart",
  "NCERT: the SAN generates an action potential which stimulates both atria to undergo simultaneous contraction "
  "(atrial systole). The action potential is conducted to the ventricular side by the AVN and the AV bundle, from "
  "where the bundle of His transmits it through the entire ventricular musculature. If the AVN fails, atrial systole "
  "still occurs, but the impulse from the SAN cannot reach the AV bundle and the ventricles.",
  ["SAN → atria (unaffected)", "AVN → AV bundle → bundle of His → ventricles (blocked at the AVN)"],
  R_BFC("cardiac cycle; human heart (nodal tissue)"),
  why_others_wrong="A is wrong because the SAN is autoexcitable and does not depend on the AVN; C reverses the order "
                   "of events; D is wrong because the AV bundle is reached only through the AVN, not directly from the "
                   "SAN.",
  seconds=50)

Z(BFC, "Double circulation and regulation", "Advanced", "match_list",
  ml(("animal", "pattern of circulation"), ["Pila", "Scoliodon", "Rana", "Columba"],
     ["Two separate circulatory pathways, so oxygenated and deoxygenated blood do not mix",
      "A single ventricle receives both oxygenated and deoxygenated blood (incomplete double circulation)",
      "Two-chambered heart pumping out deoxygenated blood, which is oxygenated by the gills",
      "Open circulatory system"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Circulatory patterns in animals",
  "NCERT: the open circulatory system is present in arthropods and molluscs (Pila is a mollusc). Fishes "
  "(Scoliodon) have a two-chambered heart that pumps out deoxygenated blood, which is oxygenated by the gills. "
  "Amphibians (Rana) have a three-chambered heart with a single ventricle, showing incomplete double circulation. "
  "Birds (Columba) and mammals have a four-chambered heart with two separate circulatory pathways (double "
  "circulation).",
  ["Pila → open (IV)", "Scoliodon → two-chambered, gills (III)", "Rana → incomplete double (II)",
   "Columba → double circulation (I)"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A swaps the mollusc and the fish; B swaps the frog and the pigeon; C swaps the fish and the frog.",
  seconds=45)

# ================================================================ Excretory Products and their Elimination (B5 I6 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Nephron structure", "Basic", "direct",
  "According to NCERT, the average weight of each kidney of an adult human is:",
  ["12–17 g", "1.2–1.7 kg", "120–170 g", "500–700 g"], "C",
  "Size of the human kidney",
  "NCERT: each kidney of an adult human measures 10–12 cm in length, 5–7 cm in width and 2–3 cm in thickness, with "
  "an average weight of 120–170 g.",
  ["Average weight → 120–170 g"],
  R_EXC("human excretory system"),
  why_others_wrong="12–17 g and 1.2–1.7 kg are the NCERT figure shifted by a factor of ten; 500–700 g is not an NCERT "
                   "figure.",
  seconds=20)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Sebaceous glands eliminate substances such as sterols, hydrocarbons and waxes through sebum. According to NCERT, "
  "this secretion also:",
  ["Provides a protective oily covering for the skin", "Produces a cooling effect on the body surface",
   "Removes most of the body's urea", "Removes large amounts of CO₂ every day"], "A",
  "Role of skin in excretion",
  "NCERT: sebaceous glands eliminate certain substances like sterols, hydrocarbons and waxes through sebum, and this "
  "secretion provides a protective oily covering for the skin. Sweat, from the sweat glands, mainly produces a "
  "cooling effect; urea is removed mainly by the kidneys; CO₂ is removed by the lungs.",
  ["Sebum → protective oily covering for the skin"],
  R_EXC("role of other organs in excretion"),
  why_others_wrong="The cooling effect is the primary function of sweat; urea is eliminated mainly in urine; CO₂ is "
                   "removed by the lungs (about 200 mL per minute).",
  seconds=25)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Animals accumulate ammonia, urea, uric acid, CO₂, water and ions as end products of metabolism. Which of these "
  "does NCERT name as the major forms of nitrogenous wastes excreted by animals?",
  ["CO₂, water and ions", "Urea and CO₂ only", "Uric acid, water and sulphate", "Ammonia, urea and uric acid"], "D",
  "Forms of nitrogenous waste",
  "NCERT: animals accumulate ammonia, urea, uric acid, carbon dioxide, water and ions like Na⁺, K⁺, Cl⁻, phosphate, "
  "sulphate, etc., which have to be removed totally or partially. Ammonia, urea and uric acid are the major forms of "
  "nitrogenous wastes excreted by the animals.",
  ["Nitrogenous wastes → ammonia, urea, uric acid"],
  R_EXC("introduction (forms of nitrogenous wastes)"),
  why_others_wrong="CO₂, water and ions such as sulphate are end products that must be removed, but they are not "
                   "nitrogenous wastes.",
  seconds=20)

Z(EXC, "Urine formation", "Basic", "statement_pair",
  sp("The urine formed is a light yellow coloured watery fluid which is slightly acidic (pH 6.0) and has a "
     "characteristic odour.",
     "On an average, 25–30 g of glucose is excreted out in the urine per day."),
  STATEMENT_PAIR, "C",
  "Characteristics of urine",
  "NCERT: an adult human excretes, on an average, 1 to 1.5 litres of urine per day. The urine is a light yellow "
  "coloured watery fluid, slightly acidic (pH 6.0), with a characteristic odour. On an average, 25–30 g of urea is "
  "excreted per day. Glucose is normally absent; its presence (glycosuria) indicates diabetes mellitus.",
  ["Statement I → true", "Statement II → false (25–30 g of urea, not glucose)"],
  R_EXC("micturition (characteristics of urine)"),
  why_others_wrong="A and D accept glucose in the place of urea; B rejects NCERT's description of urine.",
  seconds=30)

Z(EXC, "Regulation of kidney function", "Basic", "match_list",
  ml(("regulatory factor", "source"), ["ADH", "Renin", "Aldosterone", "Atrial natriuretic factor"],
     ["Atria of the heart", "Adrenal cortex", "Juxtaglomerular (JG) cells", "Released from the neurohypophysis"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Hormonal regulation of the kidney",
  "NCERT: osmoreceptors stimulate the hypothalamus to release ADH from the neurohypophysis; a fall in glomerular blood "
  "flow, blood pressure or GFR activates the JG cells to release renin; angiotensin II activates the adrenal cortex "
  "to release aldosterone; an increase in blood flow to the atria of the heart can cause the release of ANF.",
  ["ADH → neurohypophysis (IV)", "Renin → JG cells (III)", "Aldosterone → adrenal cortex (II)", "ANF → atria (I)"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A swaps ADH and renin; C swaps aldosterone and ANF; D swaps renin and aldosterone.",
  seconds=30)

_gfr, _urine = 125, 1.25
_pct = round((_gfr - _urine) / _gfr * 100, 2)
assert _pct == 99.0
Z(EXC, "Urine formation", "Intermediate", "numerical",
  "A healthy person forms glomerular filtrate at 125 mL per minute and passes urine at 1.25 mL per minute. What "
  "percentage of the filtrate is reabsorbed by the renal tubules?",
  ["1%", "90%", "98.75%", "99%"], "D",
  "Extent of tubular reabsorption",
  "Volume reabsorbed = 125 − 1.25 = 123.75 mL per minute. Percentage reabsorbed = 123.75 ÷ 125 × 100 = 99 per cent. "
  "This matches NCERT: a comparison of the volume of filtrate formed per day (180 L) with that of urine released "
  "(1.5 L) suggests that nearly 99 per cent of the filtrate has to be reabsorbed by the renal tubules.",
  ["Reabsorbed = 125 − 1.25 = 123.75 mL min⁻¹", "% = 123.75 / 125 × 100 = 99%"],
  R_EXC("urine formation"),
  why_others_wrong="1% is the fraction excreted as urine, not reabsorbed; 90% is a rough guess; 98.75% subtracts the "
                   "urine volume (1.25) from 100 instead of working out the ratio.",
  seconds=40, verified_by=RECOMPUTED)

Z(EXC, "Nephron structure", "Intermediate", "assertion_reason",
  ar("Blood that has left the glomerulus through the efferent arteriole still supplies the cells of the renal "
     "tubule.",
     "The efferent arteriole emerging from the glomerulus forms a fine capillary network around the renal tubule, "
     "called the peritubular capillaries."),
  ASSERTION_REASON, "A",
  "Blood supply of the nephron",
  "NCERT: the glomerulus is a tuft of capillaries formed by the afferent arteriole, a fine branch of the renal "
  "artery. Blood from the glomerulus is carried away by an efferent arteriole, which forms a fine capillary network "
  "around the renal tubule called the peritubular capillaries (a minute vessel of it, the vasa recta, runs parallel "
  "to Henle's loop). This network is how post-glomerular blood reaches the tubule.",
  ["A true", "R true", "Efferent arteriole → peritubular capillaries around tubule → R explains A"],
  R_EXC("human excretory system (nephron and its blood supply)"),
  why_others_wrong="B is wrong because the peritubular network is the route by which this blood reaches the tubule; "
                   "C and D are wrong because both statements are true.",
  seconds=35)

_opts_ald = ["(a), (c) and (e) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"]
Z(EXC, "Regulation of kidney function", "Intermediate", "multi_statement",
  ms("Suppose a person's adrenal cortex cannot release aldosterone, while the rest of the renin–angiotensin mechanism "
     "works normally. Which of the following are expected?",
     ["Less Na⁺ and water are reabsorbed from the distal parts of the tubule.",
      "The volume of urine tends to increase.",
      "The JG cells can no longer release renin.",
      "Angiotensin II can still act as a powerful vasoconstrictor and raise the glomerular blood pressure.",
      "ADH can no longer be released from the neurohypophysis."]),
  _opts_ald, "B",
  "Role of aldosterone",
  "NCERT: renin converts angiotensinogen into angiotensin I and then angiotensin II. Angiotensin II, a powerful "
  "vasoconstrictor, increases glomerular blood pressure and thereby GFR; it also activates the adrenal cortex to "
  "release aldosterone, which causes reabsorption of Na⁺ and water from the distal parts of the tubule. Without "
  "aldosterone, that reabsorption falls, so more water stays in the filtrate. Renin release (JG cells) and ADH release "
  "(neurohypophysis) do not depend on aldosterone.",
  ["(a) true", "(b) true – less water reabsorbed", "(c) false – JG cells are not affected",
   "(d) true – angiotensin II acts directly on vessels", "(e) false – ADH is a separate mechanism"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A and C include (c), and D includes (e): neither renin nor ADH release depends on aldosterone.",
  seconds=60)
ms_check("abd", _opts_ald, "B")

Z(EXC, "Modes of excretion", "Intermediate", "assertion_reason",
  ar("In a ureotelic animal whose liver is severely damaged, ammonia tends to accumulate in the blood.",
     "In ureotelic animals, ammonia produced by metabolism is converted into urea in the liver and released into the "
     "blood, which is filtered and excreted out by the kidneys."),
  ASSERTION_REASON, "A",
  "Formation of urea",
  "NCERT: in ureotelic animals, ammonia produced by metabolism is converted into urea in the liver of these animals "
  "and released into the blood, which is filtered and excreted out by the kidneys. If the liver cannot carry out "
  "this conversion, the highly toxic ammonia is not turned into urea and builds up.",
  ["A true", "R true", "Liver converts ammonia → urea; no conversion → ammonia accumulates → R explains A"],
  R_EXC("introduction (ureotelism)"),
  why_others_wrong="B is wrong because the liver's role in converting ammonia to urea is exactly why liver damage "
                   "leads to ammonia build-up; C and D are wrong because both statements are true.",
  seconds=35)

Z(EXC, "Urine formation", "Intermediate", "match_list",
  ml(("substance", "how the kidney handles it during urine formation"),
     ["Glucose", "Nitrogenous wastes", "Plasma proteins", "H⁺, K⁺ and ammonia"],
     ["Secreted into the filtrate by the tubular cells",
      "Not filtered into Bowman's capsule, so they do not enter the filtrate",
      "Filtered, and then absorbed from the filtrate by passive transport",
      "Filtered, and then reabsorbed from the filtrate actively"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("I", "III", "II", "IV")], "D"), "D",
  "Filtration, reabsorption and secretion",
  "NCERT: in glomerular filtration, almost all the constituents of the plasma except the proteins pass into the lumen "
  "of Bowman's capsule. Substances like glucose, amino acids and Na⁺ in the filtrate are reabsorbed actively, whereas "
  "the nitrogenous wastes are absorbed by passive transport. During urine formation, the tubular cells secrete "
  "substances like H⁺, K⁺ and ammonia into the filtrate.",
  ["Glucose → filtered, reabsorbed actively (IV)", "Nitrogenous wastes → filtered, passive transport (III)",
   "Plasma proteins → not filtered (II)", "H⁺, K⁺, NH₃ → secreted (I)"],
  R_EXC("urine formation"),
  why_others_wrong="A swaps glucose and the nitrogenous wastes (active versus passive); B treats plasma proteins as "
                   "secreted and the ions as unfiltered; C swaps glucose and the secreted ions.",
  seconds=40)

Z(EXC, "Regulation of kidney function", "Intermediate", "statement_pair",
  sp("If a person's blood carries an excess of ADH, more water is reabsorbed from the latter parts of the tubule, so a "
     "small volume of concentrated urine is formed.",
     "Excess ADH, through its constrictory effect on blood vessels, lowers the blood pressure."),
  STATEMENT_PAIR, "C",
  "Effects of ADH",
  "NCERT: ADH facilitates water reabsorption from the latter parts of the tubule, thereby preventing diuresis. ADH "
  "can also affect kidney function by its constrictory effects on blood vessels, which causes an increase in blood "
  "pressure, and this can increase glomerular blood flow and thereby the GFR. So excess ADH raises, not lowers, the "
  "blood pressure.",
  ["Statement I → true", "Statement II → false (vasoconstriction raises blood pressure)"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A and D accept that vasoconstriction lowers blood pressure; B rejects the water-conserving action "
                   "of ADH.",
  seconds=35)

_opts_mic = ["(a), (c) and (e) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (d) and (e) only"]
Z(EXC, "Regulation of kidney function", "Advanced", "multi_statement",
  ms("Suppose the stretch receptors on the wall of a person's urinary bladder are destroyed. Using the NCERT account "
     "of micturition, which of the following are expected?",
     ["Filling of the bladder would no longer send the usual signals to the CNS.",
      "The CNS would not reflexly pass on the motor messages for contraction of the bladder's smooth muscles and "
      "relaxation of the urethral sphincter.",
      "The kidneys would stop forming urine.",
      "Urine formed by the kidneys would still be carried to the bladder by the ureters.",
      "The JG cells would release renin to empty the bladder."]),
  _opts_mic, "B",
  "Micturition reflex",
  "NCERT: urine formed by the nephrons is carried to the urinary bladder, where it is stored till a voluntary signal "
  "is given by the CNS. This signal is initiated by the stretching of the urinary bladder as it gets filled with "
  "urine: stretch receptors on its walls send signals to the CNS, and the CNS passes on motor messages to initiate "
  "contraction of the smooth muscles of the bladder and simultaneous relaxation of the urethral sphincter. Urine "
  "formation and its transport through the ureters do not depend on these receptors.",
  ["(a) true", "(b) true", "(c) false – urine formation continues", "(d) true", "(e) false – renin regulates GFR, not "
   "bladder emptying"],
  R_EXC("micturition"),
  why_others_wrong="A and C include the cessation of urine formation; D includes the irrelevant renin response and "
                   "leaves out (b).",
  seconds=60)
ms_check("abd", _opts_mic, "B")

Z(EXC, "Urine formation", "Advanced", "direct",
  "Suppose a drug made the descending limb of Henle's loop impermeable to water, while all other parts worked "
  "normally. Which change would follow directly?",
  ["The ascending limb would begin to reabsorb water",
   "The filtrate would no longer get concentrated as it moves down the descending limb",
   "Glucose would begin to appear in the urine",
   "The filtrate at the hairpin bend would become more concentrated than normal"], "B",
  "Function of the descending limb",
  "NCERT: the descending limb of the loop of Henle is permeable to water but almost impermeable to electrolytes; this "
  "concentrates the filtrate as it moves down. The ascending limb is impermeable to water. If the descending limb "
  "could not lose water, the filtrate would not be concentrated on its way down. Glucose is reabsorbed earlier, in "
  "the PCT, so it is unaffected.",
  ["Descending limb concentrates the filtrate by losing water", "No water loss → no concentration on the way down"],
  R_EXC("function of the tubules"),
  why_others_wrong="A is wrong because the ascending limb is impermeable to water; C is wrong because glucose is "
                   "reabsorbed in the PCT; D is the opposite of the expected effect.",
  seconds=45)

Z(EXC, "Nephron structure", "Advanced", "statement_pair",
  sp("In a juxtamedullary nephron, the filtrate passes from the cortex into the medulla and back into the cortex before "
     "it reaches the collecting duct.",
     "The collecting duct into which such a nephron opens lies entirely within the cortex."),
  STATEMENT_PAIR, "C",
  "Course of the nephron",
  "NCERT: the Malpighian corpuscle, PCT and DCT are situated in the cortical region, whereas the loop of Henle dips "
  "into the medulla; in juxtamedullary nephrons the loop is very long and runs deep into the medulla. So the filtrate "
  "goes cortex (PCT) → medulla (loop) → cortex (DCT). The collecting duct extends from the cortex of the kidney to "
  "the inner parts of the medulla.",
  ["Statement I → true", "Statement II → false (collecting duct runs from cortex to inner medulla)"],
  R_EXC("human excretory system (nephron)"),
  why_others_wrong="A and D accept that the collecting duct is purely cortical; B rejects Statement I, though the DCT "
                   "lies in the cortex after the loop has dipped into the medulla.",
  seconds=45)

_opts_fil = ["(a), (b) and (c) only", "(c) and (e) only", "(a), (b) and (d) only", "(a) and (b) only"]
Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("In a healthy person, which of the following are present in the glomerular filtrate in Bowman's capsule but are "
     "normally absent from the final urine?",
     ["Glucose", "Amino acids", "Urea", "Plasma proteins", "Water"]),
  _opts_fil, "D",
  "Filtrate versus urine",
  "NCERT: almost all the constituents of plasma except the proteins pass into the lumen of Bowman's capsule. Nearly "
  "all the essential nutrients, such as glucose and amino acids, are reabsorbed (actively) in the PCT, so they are "
  "normally absent from urine; glucose in urine (glycosuria) indicates diabetes mellitus. Urea is excreted (25–30 g "
  "per day) and water forms the bulk of urine. Plasma proteins are not filtered in the first place.",
  ["(a) filtered, then reabsorbed → yes", "(b) filtered, then reabsorbed → yes", "(c) present in urine → no",
   "(d) not in the filtrate → no", "(e) present in urine → no"],
  R_EXC("urine formation; function of the tubules"),
  why_others_wrong="A and B include urea, which remains in urine; C includes plasma proteins, which never enter the "
                   "filtrate.",
  seconds=50)
ms_check("ab", _opts_fil, "D")

# ================================================================ Locomotion and Movement (B4 I5 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Muscle contraction", "Basic", "match_list",
  ml(("muscle", "feature described in NCERT"),
     ["Skeletal muscle", "Visceral muscle", "Cardiac muscle", "Red muscle fibres"],
     ["Plenty of mitochondria and a high content of myoglobin", "Many cells assemble in a branching pattern",
      "Located in the inner walls of hollow visceral organs", "Closely associated with the skeletal components and "
      "striped in appearance"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("II", "III", "IV", "I")], "B"), "B",
  "Types of muscles",
  "NCERT: skeletal muscles are closely associated with the skeletal components of the body and have a striped "
  "appearance (striated). Visceral muscles are located in the inner walls of hollow visceral organs such as the "
  "alimentary canal and reproductive tract. Many cardiac muscle cells assemble in a branching pattern to form a "
  "cardiac muscle. Red fibres contain a high quantity of myoglobin and plenty of mitochondria (aerobic muscles).",
  ["Skeletal → IV", "Visceral → III", "Cardiac → II", "Red fibres → I"],
  R_LOC("muscle"),
  why_others_wrong="A swaps skeletal and visceral; C swaps cardiac muscle and red fibres; D swaps skeletal and cardiac.",
  seconds=30)

_pelvic_fused = 2 * 3
assert _pelvic_fused == 6
Z(LOC, "Skeletal system", "Basic", "numerical",
  "The pelvic girdle consists of two coxal bones, and each coxal bone is formed by the fusion of three bones. How "
  "many bones in all fuse to form the human pelvic girdle?",
  ["2", "3", f"{_pelvic_fused}", "4"], "C",
  "Composition of the pelvic girdle",
  "NCERT: the pelvic girdle consists of two coxal bones; each coxal bone is formed by the fusion of three bones – "
  "ilium, ischium and pubis. So 2 × 3 = 6 bones fuse to form the girdle.",
  ["2 coxal bones × 3 (ilium, ischium, pubis) = 6"],
  R_LOC("skeletal system: appendicular skeleton (pelvic girdle)"),
  why_others_wrong="2 counts only the coxal bones; 3 counts the bones of one coxal bone; 4 is the number of bones of "
                   "the pectoral girdle (two clavicles and two scapulae).",
  seconds=25, verified_by=RECOMPUTED)

Z(LOC, "Types of movement", "Basic", "statement_pair",
  sp("Streaming of protoplasm in unicellular organisms like Amoeba is a simple form of movement.",
     "Ciliary movement occurs in most of our internal tubular organs which are lined by ciliated epithelium."),
  STATEMENT_PAIR, "A",
  "Kinds of movement",
  "NCERT: movement is one of the significant features of living beings; streaming of protoplasm in unicellular "
  "organisms like Amoeba is a simple form of movement. Ciliary movement occurs in most of our internal tubular organs "
  "which are lined by ciliated epithelium – for example, the coordinated movement of cilia in the trachea and in the "
  "female reproductive tract.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("types of movement"),
  why_others_wrong="Both statements are NCERT lines, so B, C and D are wrong.",
  seconds=25)

Z(LOC, "Skeletal system", "Basic", "direct",
  "The human vertebral column has cervical (7), thoracic (12), lumbar (5) and sacral (1, fused) regions. According to "
  "NCERT, the coccygeal region consists of:",
  ["4 free vertebrae", "5 free vertebrae", "2 fused vertebrae", "1 (fused) vertebra"], "D",
  "Regions of the vertebral column",
  "NCERT: the vertebral column is differentiated into cervical (7), thoracic (12), lumbar (5), sacral (1, fused) and "
  "coccygeal (1, fused) regions starting from the skull, giving 26 vertebrae in all: 7 + 12 + 5 + 1 + 1 = 26.",
  ["Coccygeal → 1 (fused)", "Check: 7 + 12 + 5 + 1 + 1 = 26"],
  R_LOC("skeletal system: axial skeleton (vertebral column)"),
  why_others_wrong="With 4, 5 or 2 coccygeal units, the total would not be the 26 vertebrae NCERT gives.",
  seconds=20)

Z(LOC, "Skeletal system", "Intermediate", "assertion_reason",
  ar("Bone is much harder than cartilage.",
     "Bone has a very hard matrix due to calcium salts in it, whereas cartilage has a slightly pliable matrix due to "
     "chondroitin salts."),
  ASSERTION_REASON, "A",
  "Bone and cartilage",
  "NCERT: bone and cartilage are specialised connective tissues. Bone has a very hard matrix due to calcium salts in "
  "it, and cartilage has a slightly pliable matrix due to chondroitin salts. The nature of the matrix is exactly what "
  "makes bone hard and cartilage pliable.",
  ["A true", "R true", "Calcium salts → hard matrix; chondroitin salts → pliable matrix → R explains A"],
  R_LOC("skeletal system"),
  why_others_wrong="B is wrong because the composition of the matrix is the cause of the difference in hardness; C "
                   "and D are wrong because both statements are true.",
  seconds=30)

_opts_vc = ["(a), (c) and (e) only", "(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"]
Z(LOC, "Skeletal system", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human vertebral column are correct?",
     ["It is dorsally placed and extends from the base of the skull.",
      "It constitutes the main framework of the trunk.",
      "It is formed by 26 serially arranged units called vertebrae.",
      "Its first vertebra is the axis.",
      "Its lumbar region has twelve vertebrae."]),
  _opts_vc, "B",
  "Vertebral column",
  "NCERT: the vertebral column is formed by 26 serially arranged units called vertebrae and is dorsally placed. It "
  "extends from the base of the skull and constitutes the main framework of the trunk. The first vertebra is the "
  "atlas, which articulates with the occipital condyles; the lumbar region has five vertebrae and the thoracic region "
  "twelve.",
  ["(a) true", "(b) true", "(c) true", "(d) false – atlas", "(e) false – five lumbar"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="A includes (e) and leaves out (b); C and D include (d), since the first vertebra is the atlas.",
  seconds=45)
ms_check("abc", _opts_vc, "B")

Z(LOC, "Skeletal system", "Intermediate", "statement_pair",
  sp("The two halves of the pelvic girdle meet ventrally to form the pubic symphysis, which contains fibrous "
     "cartilage.",
     "The acetabulum, at the point of fusion of the ilium, ischium and pubis, articulates with the head of the "
     "humerus."),
  STATEMENT_PAIR, "C",
  "Pelvic girdle",
  "NCERT: each coxal bone is formed by the fusion of the ilium, ischium and pubis; at the point of fusion is a cavity "
  "called the acetabulum, to which the thigh bone articulates. The two halves of the pelvic girdle meet ventrally to "
  "form the pubic symphysis containing fibrous cartilage. The humerus articulates with the glenoid cavity of the "
  "scapula.",
  ["Statement I → true", "Statement II → false (the acetabulum receives the thigh bone, the femur)"],
  R_LOC("skeletal system: appendicular skeleton (girdles)"),
  why_others_wrong="A and D accept that the humerus fits into the acetabulum; B rejects NCERT's description of the "
                   "pubic symphysis.",
  seconds=35)

Z(LOC, "Muscle contraction", "Intermediate", "match_list",
  ml(("event in a skeletal muscle fibre", "what it brings about"),
     ["Release of acetylcholine at the neuromuscular junction", "Rise in the Ca²⁺ level in the sarcoplasm",
      "Hydrolysis of ATP by the myosin head", "Binding of a new ATP molecule to the myosin head"],
     ["Breaking of the cross bridge", "Energy for the myosin head to bind the exposed active sites on actin",
      "Removal of the masking of the active sites on actin through troponin",
      "Generation of an action potential in the sarcolemma"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "C"), "C",
  "Steps of muscle contraction",
  "NCERT: a neural signal reaching the neuromuscular junction releases acetylcholine, which generates an action "
  "potential in the sarcolemma. This spreads through the fibre and causes release of Ca²⁺ into the sarcoplasm; Ca²⁺ "
  "binds a subunit of troponin, removing the masking of the active sites for myosin. Utilising the energy from ATP "
  "hydrolysis, the myosin head binds the exposed active sites on actin to form a cross bridge. A new ATP binds and "
  "the cross bridge is broken.",
  ["ACh → action potential (IV)", "Ca²⁺ → unmasking via troponin (III)", "ATP hydrolysis → energy to bind actin "
   "(II)", "New ATP → cross bridge broken (I)"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A swaps the first two events; B swaps the roles of ATP hydrolysis and new ATP binding; D swaps "
                   "the Ca²⁺ rise and ATP hydrolysis.",
  seconds=45)

_upper = 2 * 30 + 2 * 2
assert _upper == 64
Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "Each upper limb has 30 bones, and each half of the pectoral girdle consists of a clavicle and a scapula. What is "
  "the total number of bones in both upper limbs together with the complete pectoral girdle?",
  ["62", f"{_upper}", "60", "34"], "B",
  "Counting bones of the fore limbs and girdle",
  "NCERT: each of the two limbs is made of 30 bones (humerus, radius and ulna, 8 carpals, 5 metacarpals and 14 "
  "phalanges), and each half of the pectoral girdle consists of a clavicle and a scapula. Both upper limbs: 2 × 30 = "
  "60; pectoral girdle: 2 × 2 = 4; total 64.",
  ["Upper limbs: 2 × 30 = 60", "Pectoral girdle: 2 × (clavicle + scapula) = 4", "Total = 64"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="62 counts only one bone per half of the girdle; 60 leaves out the girdle; 34 counts only one limb "
                   "with the girdle.",
  seconds=40, verified_by=RECOMPUTED)

_opts_sl = ["(a) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only", "(a), (b) and (c) only"]
Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("According to the sliding filament theory, which of the following remain unchanged in length when a skeletal "
     "muscle fibre contracts?",
     ["The A-band", "The thick (myosin) filaments", "The thin (actin) filaments", "The I-band",
      "The distance between two successive Z-lines"]),
  _opts_sl, "D",
  "Sliding filament theory",
  "NCERT: muscle contraction takes place by the sliding of thin filaments over thick filaments. The Z-lines attached "
  "to the actins are pulled inwards, causing a shortening of the sarcomere; the I-bands get reduced, whereas the "
  "A-bands retain their length. Because the filaments slide rather than shorten, the thick filaments (which define "
  "the A-band) and the thin filaments keep their lengths.",
  ["(a) unchanged", "(b) unchanged", "(c) unchanged – they slide", "(d) shortens", "(e) shortens (sarcomere)"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A and C include the I-band, which gets reduced; B includes the Z-to-Z distance (sarcomere), "
                   "which shortens.",
  seconds=50)
ms_check("abc", _opts_sl, "D")

Z(LOC, "Joints", "Advanced", "match_list",
  ml(("movement", "joint at which it occurs"),
     ["Rotation of the atlas on the axis", "Bending of the leg at the knee",
      "Movement of the arm in many directions at the shoulder", "Movement between the carpal and the metacarpal of "
      "the thumb"],
     ["Saddle joint", "Ball and socket joint", "Hinge joint", "Pivot joint"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"),
                                            M("IV", "III", "I", "II")], "A"), "A",
  "Synovial joints",
  "NCERT examples of synovial joints: ball and socket joint (between humerus and pectoral girdle), hinge joint (knee "
  "joint), pivot joint (between atlas and axis), gliding joint (between the carpals) and saddle joint (between the "
  "carpal and metacarpal of the thumb).",
  ["Atlas–axis → pivot (IV)", "Knee → hinge (III)", "Shoulder → ball and socket (II)", "Thumb carpal–metacarpal → "
   "saddle (I)"],
  R_LOC("joints"),
  why_others_wrong="B swaps the knee and the shoulder; C swaps the atlas–axis and knee joints; D swaps the shoulder "
                   "and the thumb joints.",
  seconds=40)

Z(LOC, "Skeletal system", "Advanced", "statement_pair",
  sp("All 12 pairs of ribs are connected dorsally to the vertebral column.",
     "All 12 pairs of ribs are connected ventrally to the sternum, either directly or with the help of hyaline "
     "cartilage."),
  STATEMENT_PAIR, "C",
  "Ribs",
  "NCERT: there are 12 pairs of ribs; each rib is a thin flat bone connected dorsally to the vertebral column (it has "
  "two articulation surfaces on its dorsal end and is called bicephalic). The first seven pairs are attached "
  "ventrally to the sternum (true ribs); the 8th, 9th and 10th pairs join the seventh rib with the help of hyaline "
  "cartilage (vertebrochondral ribs); the 11th and 12th pairs are not connected ventrally (floating ribs).",
  ["Statement I → true", "Statement II → false (11th and 12th pairs are floating)"],
  R_LOC("skeletal system: axial skeleton (ribs)"),
  why_others_wrong="A and D overlook the floating ribs; B rejects Statement I, though every rib articulates dorsally "
                   "with the vertebral column.",
  seconds=40)

Z(LOC, "Muscle contraction", "Advanced", "assertion_reason",
  ar("Cardiac muscle is a voluntary muscle because it is striated.",
     "Based on their appearance, cardiac muscles are striated."),
  ASSERTION_REASON, "D",
  "Striation and voluntary control",
  "NCERT: cardiac muscles are striated in appearance, but they are involuntary in nature, as the nervous system does "
  "not control their activities directly. Striation does not make a muscle voluntary, so the Assertion is false "
  "while the Reason is true.",
  ["A false – cardiac muscle is involuntary", "R true"],
  R_LOC("muscle"),
  why_others_wrong="A, B and C accept the Assertion; striated cardiac muscle is involuntary, which shows that "
                   "striation and voluntary control do not go together.",
  seconds=30)

# ================================================================ Neural Control and Coordination (B3 I5 A3)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The human brain is covered by cranial meninges. Which option lists them correctly from the outermost to the "
  "innermost layer (the one in contact with the brain tissue)?",
  ["Dura mater → arachnoid → pia mater", "Pia mater → arachnoid → dura mater", "Arachnoid → dura mater → pia mater",
   "Dura mater → pia mater → arachnoid"], "A",
  "Cranial meninges",
  "NCERT: the brain is covered by cranial meninges consisting of an outer layer called the dura mater, a very thin "
  "middle layer called the arachnoid and an inner layer, in contact with the brain tissue, called the pia mater.",
  ["Outer → dura mater", "Middle (very thin) → arachnoid", "Inner, on the brain → pia mater"],
  R_NEU("central neural system: human brain"),
  why_others_wrong="B reverses the order; C and D place the arachnoid outermost or innermost, but it is the middle "
                   "layer.",
  seconds=20)

Z(NEU, "Neuron and nerves", "Basic", "direct",
  "Within a single neuron, a nerve impulse normally travels in which order?",
  ["Axon → cell body → dendrites → synaptic knob", "Synaptic knob → axon → cell body → dendrites",
   "Cell body → dendrites → axon → synaptic knob", "Dendrites → cell body → axon → synaptic knob"], "D",
  "Direction of impulse in a neuron",
  "NCERT: dendrites are short fibres that branch repeatedly and project out of the cell body; they transmit impulses "
  "towards the cell body. The axon is a long fibre whose distal end is branched; it transmits nerve impulses away "
  "from the cell body to a synapse or to a neuromuscular junction, each branch terminating as a bulb-like synaptic "
  "knob.",
  ["Dendrites → towards cell body", "Axon → away from cell body", "Ends in synaptic knobs"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="A and B run the impulse the wrong way along the axon; C sends it out along the dendrites, which "
                   "carry impulses towards the cell body.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Basic", "match_list",
  ml(("neural system", "organisation described in NCERT"),
     ["Neural system of Hydra", "Neural system of insects", "Human central neural system",
      "Human peripheral neural system"],
     ["All the nerves of the body associated with the brain and spinal cord", "Brain and spinal cord",
      "A brain along with a number of ganglia and neural tissues", "A network of neurons"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Neural systems compared",
  "NCERT: the neural organisation is very simple in lower invertebrates; for example, in Hydra it is composed of a "
  "network of neurons. In insects it is better organised, consisting of a brain along with a number of ganglia and "
  "neural tissues. In humans, the CNS includes the brain and the spinal cord, and the PNS comprises all the nerves of "
  "the body associated with the CNS.",
  ["Hydra → network (IV)", "Insects → brain + ganglia (III)", "CNS → brain + spinal cord (II)",
   "PNS → all nerves associated with CNS (I)"],
  R_NEU("neural system; human neural system"),
  why_others_wrong="A swaps Hydra and insects; C swaps CNS and PNS; D swaps the insect system and the CNS.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "statement_pair",
  sp("In the resting state, the axonal membrane is comparatively more permeable to K⁺ ions and nearly impermeable to "
     "Na⁺ ions.",
     "The sodium-potassium pump transports 2 Na⁺ outwards for every 3 K⁺ moved into the cell."),
  STATEMENT_PAIR, "C",
  "Resting membrane",
  "NCERT: in a resting state, the axonal membrane is comparatively more permeable to potassium ions (K⁺) and nearly "
  "impermeable to sodium ions (Na⁺). The ionic gradients across the resting membrane are maintained by the active "
  "transport of ions by the sodium-potassium pump, which transports 3 Na⁺ outwards for 2 K⁺ into the cell.",
  ["Statement I → true", "Statement II → false (3 Na⁺ out for 2 K⁺ in)"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A and D accept the reversed pump ratio; B rejects NCERT's description of the resting membrane's "
                   "permeability.",
  seconds=35)

_opts_pns = ["(a), (b) and (d) only", "(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"]
Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following are parts of the human peripheral neural system (PNS)?",
     ["Cranial nerves", "Spinal nerves", "Spinal cord",
      "The nerves, fibres, ganglia and plexuses of the visceral nervous system", "Thalamus"]),
  _opts_pns, "A",
  "Divisions of the neural system",
  "NCERT: the human neural system is divided into the CNS (brain and spinal cord) and the PNS, which comprises all the "
  "nerves of the body associated with the CNS. The visceral nervous system is the part of the PNS comprising the "
  "whole complex of nerves, fibres, ganglia and plexuses by which impulses travel between the CNS and the viscera. "
  "The thalamus is part of the forebrain (CNS).",
  ["(a) PNS", "(b) PNS", "(c) CNS", "(d) PNS (visceral nervous system)", "(e) CNS (forebrain)"],
  R_NEU("human neural system"),
  why_others_wrong="B, C and D each include the spinal cord, and B also the thalamus, which belong to the CNS.",
  seconds=40)
ms_check("abd", _opts_pns, "A")

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("When the axonal membrane at a site becomes freely permeable to Na⁺ on stimulation, Na⁺ rushes into the axon.",
     "In the resting state, the fluid outside the axon contains a high concentration of Na⁺ while the axoplasm "
     "contains a low concentration of Na⁺, forming a concentration gradient."),
  ASSERTION_REASON, "A",
  "Cause of sodium influx",
  "NCERT: the axoplasm contains a high concentration of K⁺ and negatively charged proteins and a low concentration of "
  "Na⁺, whereas the fluid outside the axon contains a low concentration of K⁺ and a high concentration of Na⁺, thus "
  "forming a concentration gradient. When a stimulus makes the membrane freely permeable to Na⁺, this gradient leads "
  "to a rapid influx of Na⁺, followed by reversal of polarity.",
  ["A true", "R true", "High outside, low inside → Na⁺ moves in once permeable → R explains A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="B is wrong because the concentration gradient is what drives the Na⁺ inwards; C and D are wrong "
                   "because both statements are true.",
  seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "match_list",
  ml(("event at a stimulated site of an axon", "consequence"),
     ["The membrane becomes freely permeable to Na⁺", "The inner surface becomes positive with respect to the outer",
      "Permeability to K⁺ rises", "The resting potential is restored"],
     ["The fibre becomes once more responsive to further stimulation", "K⁺ diffuses outside the membrane",
      "The membrane at that site is said to be depolarised", "Rapid influx of Na⁺"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Events of the action potential",
  "NCERT: on stimulation, the membrane at the site becomes freely permeable to Na⁺, leading to a rapid influx of Na⁺ "
  "and reversal of polarity: the outer surface becomes negative and the inner positive, and the membrane is said to "
  "be depolarised. The rise in Na⁺ permeability is extremely short-lived and is quickly followed by a rise in "
  "permeability to K⁺; K⁺ diffuses outside the membrane and restores the resting potential, and the fibre becomes "
  "once more responsive to further stimulation.",
  ["Na⁺ permeability → influx (IV)", "Inside positive → depolarised (III)", "K⁺ permeability → K⁺ out (II)",
   "Resting potential back → responsive again (I)"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A swaps the first two events; B swaps depolarisation and K⁺ efflux; C swaps the last two events.",
  seconds=40)

Z(NEU, "Nervous system divisions", "Intermediate", "statement_pair",
  sp("Impulses from the CNS to the smooth muscles of the stomach are relayed by the autonomic neural system.",
     "Impulses from the CNS to the skeletal muscles of the arm are relayed by the autonomic neural system."),
  STATEMENT_PAIR, "C",
  "Somatic and autonomic neural systems",
  "NCERT: the PNS is divided into the somatic neural system and the autonomic neural system. The somatic neural "
  "system relays impulses from the CNS to the skeletal muscles, while the autonomic neural system transmits impulses "
  "from the CNS to the involuntary organs and smooth muscles of the body.",
  ["Statement I → true (smooth muscle → autonomic)", "Statement II → false (skeletal muscle → somatic)"],
  R_NEU("human neural system"),
  why_others_wrong="A and D give skeletal muscles autonomic control; B rejects the autonomic supply of smooth muscle.",
  seconds=30)

_opts_syn = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]
Z(NEU, "Nerve impulse generation and conduction", "Advanced", "multi_statement",
  ms("An impulse passes from neuron X to neuron Y across a chemical synapse. Which of the following statements are "
     "correct?",
     ["Neurotransmitters are released into the synaptic cleft from synaptic vesicles in the synaptic knob of X.",
      "The released neurotransmitters bind to specific receptors on the post-synaptic membrane of Y.",
      "This binding opens ion channels, allowing entry of ions that can generate a new potential in Y.",
      "The same synapse can pass the impulse equally well from Y back to X, since receptors lie on both membranes.",
      "At this synapse, electrical current flows directly from X into Y."]),
  _opts_syn, "B",
  "Chemical synaptic transmission",
  "NCERT: at a chemical synapse the membranes of the pre- and post-synaptic neurons are separated by a fluid-filled "
  "synaptic cleft. An impulse arriving at the axon terminal makes synaptic vesicles fuse with the plasma membrane and "
  "release neurotransmitters into the cleft; these bind to specific receptors present on the post-synaptic membrane, "
  "opening ion channels and allowing entry of ions which can generate a new potential in the post-synaptic neuron. "
  "The receptors are on the post-synaptic membrane, and direct current flow happens only at electrical synapses.",
  ["(a) true", "(b) true", "(c) true", "(d) false – receptors are on the post-synaptic membrane",
   "(e) false – that describes an electrical synapse"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A adds the backward transmission (d); C and D include (e), which describes an electrical "
                   "synapse.",
  seconds=55)
ms_check("abc", _opts_syn, "B")

Z(NEU, "Nervous system divisions", "Advanced", "match_list",
  ml(("structure", "part of the neural system it belongs to"),
     ["Cerebral aqueduct", "Amygdala", "Pons", "Spinal nerves"],
     ["Peripheral neural system", "Hindbrain", "Forebrain (limbic system)", "Midbrain"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"),
                                            M("II", "III", "IV", "I")], "D"), "D",
  "Locating brain structures",
  "NCERT: a canal called the cerebral aqueduct passes through the midbrain. The inner parts of the cerebral "
  "hemispheres (forebrain) and a group of associated deep structures like the amygdala and hippocampus form the "
  "limbic system. The hindbrain comprises the pons, cerebellum and medulla. Spinal nerves, like cranial nerves, are "
  "part of the PNS.",
  ["Cerebral aqueduct → midbrain (IV)", "Amygdala → forebrain, limbic (III)", "Pons → hindbrain (II)",
   "Spinal nerves → PNS (I)"],
  R_NEU("central neural system: forebrain, midbrain and hindbrain"),
  why_others_wrong="A swaps the amygdala and the pons; B swaps the cerebral aqueduct and the amygdala; C swaps the "
                   "cerebral aqueduct and the pons.",
  seconds=40)

_opts_sch = ["(a), (c) and (e) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"]
Z(NEU, "Neuron and nerves", "Advanced", "multi_statement",
  ms("Suppose the Schwann cells around a myelinated axon of a spinal nerve were destroyed. Using NCERT's description "
     "of nerve fibres, which of the following statements are correct?",
     ["The myelin sheath around that axon would be lost.",
      "Nodes of Ranvier, the gaps between adjacent myelin sheaths, would no longer be present on it.",
      "The cell body of the neuron would lose all its cell organelles.",
      "In myelinated fibres of spinal and cranial nerves, it is the Schwann cells that form the myelin sheath.",
      "The axon would now become a part of the central neural system."]),
  _opts_sch, "B",
  "Myelinated nerve fibres",
  "NCERT: the myelinated nerve fibres are enveloped with Schwann cells, which form a myelin sheath around the axon; "
  "the gaps between two adjacent myelin sheaths are called nodes of Ranvier. Myelinated fibres are found in spinal "
  "and cranial nerves. Losing the Schwann cells therefore removes the sheath and its nodes, but it does not strip the "
  "cell body of its organelles or move a spinal nerve into the CNS.",
  ["(a) true", "(b) true – nodes are gaps between sheaths", "(c) false", "(d) true", "(e) false – spinal nerves are "
   "PNS"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="A and C include (c), which does not follow; D includes (e), though spinal nerves remain part of "
                   "the PNS.",
  seconds=55)
ms_check("abd", _opts_sch, "B")


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
           "notes": "BATCH_007 package ZOO_007_p1: 125 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "questions already asked in BATCH_000-BATCH_006 (many items are application or scenario "
                    "questions on NCERT mechanisms); every numerical answer re-derived by "
                    "tools/batch_007/ZOO_007_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
