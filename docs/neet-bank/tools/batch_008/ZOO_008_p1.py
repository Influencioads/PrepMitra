"""Writes batches/parts/BATCH_008_ZOO_p1.json: package ZOO_008_p1 of BATCH_008 (Zoology, 117 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_001751 .. NEET_ZOO_001867. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, subtopics, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11
Biology textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion and absorption), and
for the frog only the systems the NMC text lists. Facts already tested in BATCH_000 to BATCH_007 (see
`merge_batch.py stems 008 ZOO_008_p1`) are not asked again in the same way; many items are application or scenario
questions on NCERT mechanisms.

    python docs/neet-bank/tools/batch_008/ZOO_008_p1.py
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
PACKAGE = "ZOO_008_p1"
BATCH = "BATCH_008"
FIRST_ID, LAST_ID = 1751, 1867
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

Z(AK, "Chordate classes", "Basic", "match_list",
  ml(("fish genus", "common name"), ["Petromyzon", "Myxine", "Catla", "Pterophyllum"],
     ["Angel fish", "Katla", "Hagfish", "Lamprey"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "C"), "C",
  "Examples of cyclostomes and bony fishes",
  "NCERT examples: class Cyclostomata – Petromyzon (Lamprey) and Myxine (Hagfish); class Osteichthyes – freshwater "
  "Catla (Katla) and the aquarium fish Pterophyllum (Angel fish).",
  ["Petromyzon → Lamprey (IV)", "Myxine → Hagfish (III)", "Catla → Katla (II)", "Pterophyllum → Angel fish (I)"],
  R_AK("class Cyclostomata and class Osteichthyes"),
  why_others_wrong="A swaps the two cyclostomes; B swaps Catla and Pterophyllum; D swaps Myxine and Catla.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "According to NCERT, which structures of annelids help them in locomotion?",
  ["Longitudinal and circular muscles", "Jointed appendages", "A muscular foot", "Tube feet of a water vascular "
   "system"], "A",
  "Locomotion in annelids",
  "NCERT: annelids possess longitudinal and circular muscles which help in locomotion. Aquatic annelids like Nereis "
  "also possess lateral appendages, parapodia, which help in swimming.",
  ["Annelida → longitudinal + circular muscles help in locomotion"],
  R_AK("phylum Annelida"),
  why_others_wrong="Jointed appendages belong to arthropods, the muscular foot to molluscs and tube feet of the water "
                   "vascular system to echinoderms.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "The class name Amphibia (Greek amphi: dual, bios: life) indicates that its members:",
  ["Have both gills and lungs throughout life", "Can live in aquatic as well as terrestrial habitats",
   "Possess both an endoskeleton and an exoskeleton", "Reproduce both sexually and asexually"], "B",
  "Meaning of the name Amphibia",
  "NCERT: as the name indicates (Gr., Amphi: dual, bios: life), amphibians can live in aquatic as well as "
  "terrestrial habitats. The 'dual life' refers to the two habitats.",
  ["amphi = dual, bios = life → life in water as well as on land"],
  R_AK("class Amphibia"),
  why_others_wrong="The name does not refer to two respiratory organs, two skeletons or two modes of reproduction; "
                   "NCERT explains it by the two habitats.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "direct",
  "Neophron, one of NCERT's examples of class Aves, is commonly known as the:",
  ["Crow", "Penguin", "Parrot", "Vulture"], "D",
  "Examples of Aves",
  "NCERT examples of Aves: Corvus (Crow), Columba (Pigeon), Psittacula (Parrot), Struthio (Ostrich), Pavo (Peacock), "
  "Aptenodytes (Penguin) and Neophron (Vulture).",
  ["Neophron → vulture"],
  R_AK("class Aves"),
  why_others_wrong="The crow is Corvus, the penguin Aptenodytes and the parrot Psittacula.",
  seconds=20)

Z(AK, "Basis of classification", "Basic", "statement_pair",
  sp("Animals like annelids and arthropods, whose body can be divided into identical left and right halves in only "
     "one plane, exhibit bilateral symmetry.",
     "Sponges are mostly asymmetrical, i.e. any plane that passes through the centre does not divide them into equal "
     "halves."),
  STATEMENT_PAIR, "A",
  "Body symmetry",
  "NCERT: sponges are mostly asymmetrical – any plane that passes through the centre does not divide them into equal "
  "halves. Animals like annelids, arthropods, etc., where the body can be divided into identical left and right "
  "halves in only one plane, exhibit bilateral symmetry.",
  ["Statement I → true (bilateral symmetry)", "Statement II → true (sponges mostly asymmetrical)"],
  R_AK("basis of classification: symmetry"),
  why_others_wrong="Both lines restate NCERT's definitions, so any option calling either statement false is wrong.",
  seconds=30)

Z(AK, "Chordate classes", "Basic", "direct",
  "NCERT groups its examples of bony fishes as marine, freshwater and aquarium fishes. Which of the following is "
  "listed as a marine bony fish?",
  ["Labeo", "Clarias", "Hippocampus", "Catla"], "C",
  "Examples of Osteichthyes",
  "NCERT: marine – Exocoetus (Flying fish), Hippocampus (Sea horse); freshwater – Labeo (Rohu), Catla (Katla), "
  "Clarias (Magur); aquarium – Betta (Fighting fish), Pterophyllum (Angel fish).",
  ["Hippocampus (sea horse) → marine bony fish"],
  R_AK("class Osteichthyes"),
  why_others_wrong="Labeo (Rohu), Clarias (Magur) and Catla (Katla) are NCERT's freshwater examples.",
  seconds=20)

_opts_ind = ["(b), (c) and (d) only", "(a), (b), (c) and (e) only", "(a) and (d) only", "(a), (b) and (c) only"]
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("In which of the following animals is development indirect, according to NCERT's description of their phylum "
     "or class?",
     ["Pila", "Asterias", "Balanoglossus", "Labeo", "Columba"]),
  _opts_ind, "D",
  "Direct and indirect development across groups",
  "NCERT: molluscs are usually dioecious and oviparous with indirect development; in echinoderms development is "
  "indirect with a free-swimming larva; in hemichordates fertilisation is external and development is indirect. "
  "Bony fishes (Labeo) are mostly oviparous and development is direct; birds (Columba) are oviparous and development "
  "is direct.",
  ["(a) Pila – Mollusca → indirect", "(b) Asterias – Echinodermata → indirect",
   "(c) Balanoglossus – Hemichordata → indirect", "(d) Labeo – Osteichthyes → direct",
   "(e) Columba – Aves → direct"],
  R_AK("phyla Mollusca, Echinodermata and Hemichordata; classes Osteichthyes and Aves"),
  why_others_wrong="A and C include Labeo and B includes Columba, both of which have direct development; A and C also "
                   "leave out animals with indirect development.",
  seconds=50)
ms_check("abc", _opts_ind, "D")

Z(AK, "Chordate classes", "Intermediate", "assertion_reason",
  ar("Unlike in a shark, separate gill slits are not seen on the sides of the head of a bony fish such as Labeo.",
     "In bony fishes, the four pairs of gills are covered by an operculum on each side, whereas in cartilaginous "
     "fishes the gill slits are separate and without an operculum."),
  ASSERTION_REASON, "A",
  "Gill cover of bony fishes",
  "NCERT: in Chondrichthyes the gill slits are separate and without operculum (gill cover); in Osteichthyes there are "
  "four pairs of gills which are covered by an operculum on each side. Because an operculum covers the gills of a bony "
  "fish, its individual gill slits are hidden, while a shark's separate, uncovered slits are visible. R is therefore "
  "the direct cause of A.",
  ["R: bony fish – gills under an operculum; shark – separate gill slits, no operculum",
   "A follows: the operculum hides the gills of Labeo"],
  R_AK("class Chondrichthyes and class Osteichthyes"),
  why_others_wrong="Both statements are true and R explains A, so B, C and D are wrong.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("animal", "structure that NCERT gives for its excretion"), ["Planaria", "Nereis", "Locusta", "Saccoglossus"],
     ["Proboscis gland", "Malpighian tubules", "Nephridia", "Flame cells"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Excretory structures of non-chordates",
  "Work out each animal's phylum first: Planaria – Platyhelminthes (flame cells help in osmoregulation and "
  "excretion); Nereis – Annelida (nephridia); Locusta – Arthropoda (excretion through Malpighian tubules); "
  "Saccoglossus – Hemichordata (the excretory organ is the proboscis gland).",
  ["Planaria → flame cells (IV)", "Nereis → nephridia (III)", "Locusta → Malpighian tubules (II)",
   "Saccoglossus → proboscis gland (I)"],
  R_AK("phyla Platyhelminthes, Annelida, Arthropoda and Hemichordata"),
  why_others_wrong="A swaps Planaria and Nereis; C swaps Locusta and Saccoglossus; D swaps Nereis and Locusta.",
  seconds=40)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("In cartilaginous fishes, the mouth is located ventrally.",
     "Unlike cartilaginous fishes, bony fishes are warm-blooded (homoiothermous) animals."),
  STATEMENT_PAIR, "C",
  "Comparing the two fish classes",
  "NCERT: in Chondrichthyes the mouth is located ventrally, and they are cold-blooded (poikilothermous). NCERT also "
  "describes Osteichthyes as cold-blooded animals. Among vertebrates, only birds and mammals are homoiothermous.",
  ["Statement I → true", "Statement II → false: both fish classes are cold-blooded"],
  R_AK("class Chondrichthyes and class Osteichthyes"),
  why_others_wrong="A and D accept Statement II, but bony fishes are cold-blooded; B rejects the ventral mouth of "
                   "sharks, which NCERT states.",
  seconds=35)

Z(AK, "Basis of classification", "Intermediate", "direct",
  "A student examines Pila, Asterias and Ascaris. Which feature do all three share?",
  ["All three are coelomates", "All three are triploblastic", "All three are bilaterally symmetrical as adults",
   "All three are monoecious (hermaphrodite)"], "B",
  "Germ layers, coelom and symmetry",
  "Pila (Mollusca), Asterias (Echinodermata) and Ascaris (Aschelminthes) are all triploblastic. But Ascaris is a "
  "pseudocoelomate, adult Asterias is radially symmetrical, and NCERT describes molluscs as usually dioecious, "
  "aschelminths as dioecious and echinoderms as having separate sexes.",
  ["Pila, Asterias, Ascaris → all triploblastic", "Ascaris → pseudocoelom", "Adult Asterias → radial",
   "All three → sexes separate"],
  R_AK("basis of classification; phyla Aschelminthes, Mollusca and Echinodermata"),
  why_others_wrong="A fails for Ascaris (pseudocoelomate), C fails for adult Asterias (radial) and D fails for all "
                   "three, which have separate sexes.",
  seconds=40)

Z(AK, "Chordate classes", "Intermediate", "match_list",
  ml(("class", "respiratory organs described in NCERT"), ["Cyclostomata", "Osteichthyes", "Amphibia", "Aves"],
     ["Gills, lungs and skin", "6–15 pairs of gill slits", "Lungs, supplemented by air sacs",
      "Four pairs of gills covered by an operculum on each side"]),
  match_options(M("II", "IV", "I", "III"), [M("IV", "II", "I", "III"), M("II", "IV", "III", "I"),
                                            M("II", "I", "IV", "III")], "D"), "D",
  "Respiratory organs of vertebrate classes",
  "NCERT: cyclostomes have 6–15 pairs of gill slits for respiration; bony fishes have four pairs of gills covered by "
  "an operculum on each side; in amphibians respiration is by gills, lungs and through skin; in birds respiration is "
  "by lungs, and air sacs connected to the lungs supplement respiration.",
  ["Cyclostomata → 6–15 pairs of gill slits (II)", "Osteichthyes → four pairs of gills + operculum (IV)",
   "Amphibia → gills, lungs, skin (I)", "Aves → lungs + air sacs (III)"],
  R_AK("classes Cyclostomata, Osteichthyes, Amphibia and Aves"),
  why_others_wrong="A swaps the two fish-like classes; B swaps Amphibia and Aves; C swaps Osteichthyes and Amphibia.",
  seconds=40)

Z(AK, "Chordate classes", "Intermediate", "assertion_reason",
  ar("Cyclostomes such as Petromyzon are placed in the division Agnatha of the vertebrates.",
     "Cyclostomes have a sucking and circular mouth without jaws."),
  ASSERTION_REASON, "A",
  "Agnatha – the jawless vertebrates",
  "NCERT divides vertebrates into the division Agnatha (lacks jaw) and Gnathostomata (bears jaw); Agnatha contains "
  "class Cyclostomata. Cyclostomes have a sucking and circular mouth without jaws. Lacking jaws is exactly what puts "
  "them in Agnatha, so R explains A.",
  ["Agnatha = lacks jaw", "Cyclostomes: circular sucking mouth without jaws → Agnatha"],
  R_AK("subphylum Vertebrata; class Cyclostomata"),
  why_others_wrong="Both statements are true and the jawless mouth is the basis of the grouping, so B, C and D are "
                   "wrong.",
  seconds=35)

Z(AK, "Basis of classification", "Intermediate", "direct",
  "Which of the following features is shared by Coelenterata and Ctenophora but NOT by Platyhelminthes?",
  ["Bioluminescence", "Metagenesis", "A diploblastic body with the tissue level of organisation",
   "Hermaphroditism"], "C",
  "Diploblastic phyla",
  "NCERT: coelenterates and ctenophores are diploblastic and show the tissue level of organisation, while "
  "Platyhelminthes are triploblastic with the organ level. Bioluminescence is well-marked in ctenophores only, "
  "metagenesis is shown by some cnidarians such as Obelia, and hermaphroditism is shared by ctenophores and "
  "flatworms.",
  ["Coelenterata, Ctenophora → diploblastic, tissue level", "Platyhelminthes → triploblastic"],
  R_AK("basis of classification; phyla Coelenterata, Ctenophora and Platyhelminthes"),
  why_others_wrong="A belongs to ctenophores alone, B to some cnidarians alone, and D is also true of Platyhelminthes, "
                   "so it does not separate them.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "match_list",
  ml(("animal", "fertilisation and development as described in NCERT"),
     ["Sycon", "Pleurobrachia", "Labeo", "Calotes"],
     ["Internal fertilisation; direct development", "Usually external fertilisation; direct development",
      "External fertilisation; indirect development", "Internal fertilisation; indirect development"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("I", "III", "II", "IV")], "B"), "B",
  "Fertilisation and development across groups",
  "Identify the group, then recall NCERT: sponges (Sycon) – fertilisation internal and development indirect; "
  "ctenophores (Pleurobrachia) – fertilisation external with indirect development; bony fishes (Labeo) – "
  "fertilisation usually external, mostly oviparous and development direct; reptiles (Calotes) – fertilisation "
  "internal, oviparous and development direct.",
  ["Sycon → internal, indirect (IV)", "Pleurobrachia → external, indirect (III)",
   "Labeo → usually external, direct (II)", "Calotes → internal, direct (I)"],
  R_AK("phyla Porifera and Ctenophora; classes Osteichthyes and Reptilia"),
  why_others_wrong="A swaps Sycon and Pleurobrachia (fertilisation site); C swaps Labeo and Calotes; D swaps Sycon "
                   "and Calotes (development type).",
  seconds=60)

_opts_ost = ["(a), (b) and (d) only", "(a), (b), (c) and (d) only", "(a), (d) and (e) only", "(b), (c) and (e) only"]
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Struthio (ostrich) cannot fly. Which of the following would NCERT's account of class Aves still lead you to "
     "expect in it?",
     ["Its body bears feathers.", "It possesses a beak.", "It is poikilothermous.",
      "Air sacs connected to its lungs supplement respiration.", "It is viviparous."]),
  _opts_ost, "A",
  "Class characters apply to flightless birds",
  "NCERT names Struthio as a flightless bird of class Aves. Class characters still apply: feathers, a beak, lungs "
  "with air sacs that supplement respiration, a four-chambered heart and warm-bloodedness (homoiothermy), and birds "
  "are oviparous. Being unable to fly does not change these.",
  ["(a) true", "(b) true", "(c) false – birds are homoiothermous", "(d) true", "(e) false – birds are oviparous"],
  R_AK("class Aves"),
  why_others_wrong="B and D include poikilothermy (c); C and D include viviparity (e); C also drops the beak.",
  seconds=50)
ms_check("abd", _opts_ost, "A")

Z(AK, "Chordate classes", "Advanced", "statement_pair",
  sp("Since the adult frog has no tail, no member of class Amphibia possesses a tail.",
     "Most amphibians have two pairs of limbs, and their body is divisible into head and trunk."),
  STATEMENT_PAIR, "D",
  "Body plan of amphibians",
  "NCERT, class Amphibia: most of them have two pairs of limbs; the body is divisible into head and trunk; a tail "
  "may be present in some. The adult frog lacks a tail, but that is one amphibian, not the whole class – so the "
  "generalisation in Statement I is false, while Statement II is NCERT's description.",
  ["Statement I → false: NCERT says a tail may be present in some amphibians", "Statement II → true"],
  R_AK("class Amphibia"),
  why_others_wrong="A and C accept Statement I, which over-generalises from the frog; B rejects Statement II, which "
                   "NCERT states for the class.",
  seconds=45)

_opts_pl = ["(a), (b) and (c) only", "(b), (c) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]
Z(AK, "Non-chordate phyla", "Advanced", "multi_statement",
  ms("Compare Pheretima (earthworm) with Locusta. Which of the following statements are correct?",
     ["Both have a closed circulatory system.",
      "Both are bilaterally symmetrical, triploblastic and coelomate.",
      "Locusta excretes through Malpighian tubules, while Pheretima uses nephridia.",
      "Pheretima is monoecious, whereas arthropods like Locusta are mostly dioecious.",
      "Both have a chitinous exoskeleton."]),
  _opts_pl, "C",
  "Annelida versus Arthropoda",
  "NCERT: annelids have a closed circulatory system, arthropods an open one. Both phyla are bilaterally symmetrical, "
  "triploblastic and coelomate. Annelids excrete through nephridia and arthropods through Malpighian tubules. "
  "Earthworms are monoecious, while arthropods are mostly dioecious. Only arthropods have a chitinous exoskeleton.",
  ["(a) false – Locusta has an open circulatory system", "(b) true", "(c) true", "(d) true",
   "(e) false – the chitinous exoskeleton is an arthropod feature"],
  R_AK("phyla Annelida and Arthropoda"),
  why_others_wrong="A includes (a); B includes (e); D includes both (a) and (e) and leaves out (b).",
  seconds=55)
ms_check("bcd", _opts_pl, "C")

_opts_bf = ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (b), (d) and (e) only"]
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("A fish has its gills covered by an operculum on each side and its skin covered with cycloid scales. Which of "
     "the following would you also expect in it, according to NCERT?",
     ["An air bladder that regulates buoyancy", "A mouth that is mostly terminal",
      "Claspers on the pelvic fins of males", "A two-chambered heart",
      "It is mostly oviparous with direct development"]),
  _opts_bf, "D",
  "Identifying a bony fish from its features",
  "An operculum and cycloid scales identify a bony fish (Osteichthyes). NCERT: bony fishes have an air bladder which "
  "regulates buoyancy, the mouth is mostly terminal, the heart is two-chambered (one auricle and one ventricle), "
  "fertilisation is usually external, they are mostly oviparous and development is direct. Claspers on the pelvic "
  "fins of males are a feature of cartilaginous fishes.",
  ["Operculum + cycloid scales → Osteichthyes", "(a), (b), (d), (e) true", "(c) false – claspers are in "
   "Chondrichthyes"],
  R_AK("class Osteichthyes"),
  why_others_wrong="A, B and C all include claspers (c), a cartilaginous-fish feature, and leave out true features.",
  seconds=50)
ms_check("abde", _opts_bf, "D")

Z(AK, "Non-chordate phyla", "Advanced", "direct",
  "Which of the following statements correctly compares Hirudinaria with Balanoglossus?",
  ["Both are dioecious and excrete through a proboscis gland",
   "Both are coelomates, but Hirudinaria has a closed and Balanoglossus an open circulatory system",
   "Both have open circulatory systems, but only Balanoglossus is a coelomate",
   "Both are hermaphrodite, but only Hirudinaria has nephridia"], "B",
  "Annelida versus Hemichordata",
  "Hirudinaria (Annelida) is a coelomate with a closed circulatory system, nephridia, and – like earthworms – is "
  "monoecious. Balanoglossus (Hemichordata) is also a triploblastic coelomate, but its circulatory system is open, "
  "its excretory organ is the proboscis gland, and its sexes are separate.",
  ["Both phyla → coelomate", "Annelida → closed circulation; Hemichordata → open circulation"],
  R_AK("phyla Annelida and Hemichordata"),
  why_others_wrong="A gives the leech a proboscis gland and separate sexes; C gives the leech an open system and "
                   "denies it a coelom; D makes the hemichordate hermaphrodite.",
  seconds=45)

# ================================================================ Structural Organisation in Animals (B4 I5 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "When a frog is in water, dissolved oxygen is exchanged through its skin by diffusion. NCERT calls this:",
  ["Pulmonary respiration", "Cutaneous respiration", "Buccal respiration", "Branchial respiration"], "B",
  "Respiration in the frog",
  "NCERT: in water, the skin of the frog acts as an aquatic respiratory organ (cutaneous respiration); dissolved "
  "oxygen in the water is exchanged through the skin by diffusion. On land, the buccal cavity, skin and lungs act as "
  "respiratory organs, and respiration by the lungs is called pulmonary respiration.",
  ["Gas exchange through skin → cutaneous respiration"],
  R_SOA("frog: anatomy – respiratory system"),
  why_others_wrong="Pulmonary respiration is by the lungs; buccal respiration and branchial (gill) respiration are not "
                   "NCERT's name for exchange through the skin.",
  seconds=20)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "In the frog, partially digested food (chyme) leaves the stomach and passes into the:",
  ["Rectum", "Cloaca", "Oesophagus", "Duodenum"], "D",
  "Digestive system of the frog",
  "NCERT: partially digested food, called chyme, is passed from the stomach to the first part of the intestine, the "
  "duodenum. The duodenum receives bile from the gall bladder and pancreatic juices from the pancreas through a "
  "common bile duct.",
  ["Stomach → chyme → duodenum (first part of the intestine)"],
  R_SOA("frog: anatomy – digestive system"),
  why_others_wrong="The rectum and cloaca come at the end of the canal and receive undigested waste; the oesophagus "
                   "lies before the stomach.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "direct",
  "In a typical skeletal muscle such as the biceps, the muscle fibres are:",
  ["Unstriated, and they taper at both ends", "Striated, and bundled together in a parallel fashion",
   "Branched, and joined by intercalated discs", "Loosely arranged in a semi-fluid ground substance"], "B",
  "Skeletal muscle",
  "NCERT: skeletal muscle tissue is closely attached to skeletal bones. In a typical muscle such as the biceps, "
  "striated (striped) skeletal muscle fibres are bundled together in a parallel fashion, and a sheath of tough "
  "connective tissue encloses several bundles of muscle fibres.",
  ["Biceps → striated skeletal fibres in parallel bundles"],
  R_SOA("animal tissue – muscle tissue"),
  why_others_wrong="A describes smooth muscle fibres; C describes cardiac muscle junctions; D describes loose "
                   "connective tissue.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Blood is a fluid connective tissue containing plasma, red blood cells, white blood cells and platelets.",
     "Blood is the main circulating fluid that helps in the transport of various substances."),
  STATEMENT_PAIR, "A",
  "Blood as a specialised connective tissue",
  "NCERT: blood is a fluid connective tissue containing plasma, red blood cells (RBC), white blood cells (WBC) and "
  "platelets. It is the main circulating fluid that helps in the transport of various substances.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("animal tissue – specialised connective tissue"),
  why_others_wrong="Both statements are NCERT's description of blood, so options calling either false are wrong.",
  seconds=25)

Z(SOA, "Animal tissues", "Intermediate", "assertion_reason",
  ar("Gases diffuse readily across the walls of the air sacs of the lungs.",
     "The walls of the air sacs are made of squamous epithelium, a single thin layer of flattened cells that forms a "
     "diffusion boundary."),
  ASSERTION_REASON, "A",
  "Structure suits function in squamous epithelium",
  "NCERT: squamous epithelium is made of a single thin layer of flattened cells with irregular boundaries. It is "
  "found in the walls of blood vessels and air sacs of lungs and is involved in functions like forming a diffusion "
  "boundary. The thin single layer is exactly why diffusion across the air-sac wall is easy, so R explains A.",
  ["R: air-sac wall = squamous epithelium = diffusion boundary", "A follows from R"],
  R_SOA("animal tissue – epithelial tissue"),
  why_others_wrong="Both statements are true and R gives the structural reason for A, so B, C and D are wrong.",
  seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "match_list",
  ml(("structure in the male frog", "description"), ["Mesorchium", "Vasa efferentia", "Bidder's canal", "Cloaca"],
     ["Small median chamber that passes faecal matter, urine and sperms to the exterior",
      "Canal in the kidney into which the vasa efferentia open",
      "Double fold of peritoneum attaching the testes to the upper part of the kidneys",
      "10–12 ducts that arise from the testes and enter the kidneys"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "II", "IV", "I"),
                                            M("III", "IV", "I", "II")], "C"), "C",
  "Male reproductive system of the frog",
  "NCERT: the yellowish ovoid testes adhere to the upper part of the kidneys by a double fold of peritoneum called "
  "the mesorchium. Vasa efferentia, 10–12 in number, arise from the testes, enter the kidneys on their side and open "
  "into Bidder's canal, which communicates with the urinogenital duct. The cloaca is a small, median chamber used to "
  "pass faecal matter, urine and sperms to the exterior.",
  ["Mesorchium → III", "Vasa efferentia → IV", "Bidder's canal → II", "Cloaca → I"],
  R_SOA("frog: anatomy – reproductive system"),
  why_others_wrong="A swaps the mesorchium and the vasa efferentia; B swaps the vasa efferentia and Bidder's canal; "
                   "D swaps Bidder's canal and the cloaca.",
  seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "Which sequence correctly traces the path of food through the alimentary canal of the frog?",
  ["Mouth → buccal cavity → oesophagus → pharynx → stomach → intestine → cloaca → rectum",
   "Mouth → pharynx → buccal cavity → oesophagus → stomach → rectum → intestine → cloaca",
   "Mouth → buccal cavity → pharynx → stomach → oesophagus → intestine → rectum → cloaca",
   "Mouth → buccal cavity → pharynx → oesophagus → stomach → intestine → rectum → cloaca"], "D",
  "Alimentary canal of the frog",
  "NCERT: the mouth opens into the buccal cavity, which leads to the oesophagus through the pharynx. The oesophagus is "
  "a short tube that opens into the stomach, which in turn continues as the intestine, the rectum, and finally opens "
  "outside by the cloaca.",
  ["Buccal cavity → pharynx → oesophagus", "Stomach → intestine → rectum → cloaca"],
  R_SOA("frog: anatomy – digestive system"),
  why_others_wrong="A puts the oesophagus before the pharynx and the cloaca before the rectum; B puts the pharynx "
                   "before the buccal cavity and the rectum before the intestine; C puts the stomach before the "
                   "oesophagus.",
  seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("In the frog, the veins collect blood from different parts of the body and carry it to the heart, forming the "
     "venous system.",
     "In the frog, the special venous connection between the kidneys and the lower parts of the body is called the "
     "hepatic portal system."),
  STATEMENT_PAIR, "C",
  "Venous system and portal systems of the frog",
  "NCERT: the veins collect blood from different parts of the body to the heart and form the venous system. Special "
  "venous connections are present between the liver and intestine as well as between the kidney and the lower parts "
  "of the body; the former is called the hepatic portal system and the latter the renal portal system.",
  ["Statement I → true", "Statement II → false: kidney–lower body connection is the renal portal system"],
  R_SOA("frog: anatomy – circulatory system"),
  why_others_wrong="A and D accept Statement II, which names the wrong portal system; B rejects Statement I, which is "
                   "NCERT's description of the venous system.",
  seconds=35)

_opts_frep = ["(a), (b) and (e) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]
Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about reproduction in the frog are correct?",
     ["Fertilisation is external and takes place in water.",
      "Development involves a larval stage called the tadpole.",
      "A mature female lays only a single ovum at a time.",
      "In the male, the testes are attached to the upper part of the kidneys by the mesorchium.",
      "In the female, the oviducts open into the urinogenital duct of the kidneys."]),
  _opts_frep, "B",
  "Reproduction in the frog",
  "NCERT: fertilisation is external and takes place in water; development involves a larval stage called the tadpole, "
  "which undergoes metamorphosis to form the adult. A mature female can lay 2500 to 3000 ova at a time. The testes "
  "adhere to the upper part of the kidneys by the mesorchium. In the female, the ovaries have no functional "
  "connection with the kidneys, and the oviducts open into the cloaca separately.",
  ["(a) true", "(b) true", "(c) false – 2500–3000 ova at a time", "(d) true",
   "(e) false – oviducts open into the cloaca separately"],
  R_SOA("frog: anatomy – reproductive system"),
  why_others_wrong="A and D include (e); C and D include (c); C also leaves out external fertilisation (a).",
  seconds=45)
ms_check("abd", _opts_frep, "B")

Z(SOA, "Frog: morphology and anatomy", "Advanced", "direct",
  "Suppose both ureters of a male frog and of a female frog were tied off just after they leave the kidneys. "
  "Release of which of the following to the exterior would be blocked?",
  ["Urine in the male only; gametes in both frogs",
   "Urine in both frogs; gametes in neither frog",
   "Urine in both frogs; sperms in the male, but not ova in the female",
   "Urine in the female only; gametes in the male only"], "C",
  "Urinogenital ducts of male and female frogs",
  "NCERT: in male frogs the ureters act as urinogenital ducts – the vasa efferentia open into Bidder's canal in the "
  "kidney, which communicates with the urinogenital duct coming out of the kidney. In the female, the ovaries have no "
  "functional connection with the kidneys and the oviducts open into the cloaca separately. Tying the ureters "
  "therefore blocks urine in both sexes, and sperms in the male, but the ova of the female still leave through the "
  "oviducts.",
  ["Male: ureter = urinogenital duct → urine + sperms blocked",
   "Female: ureter carries urine only; oviducts separate → ova still released"],
  R_SOA("frog: anatomy – reproductive system"),
  why_others_wrong="A and D forget that both frogs' ureters carry urine; A also blocks ova; B forgets that the male's "
                   "sperms travel through the urinogenital duct.",
  seconds=60)

_opts_cart = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c) and (d) only", "(a), (b), (d) and (e) only"]
Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("A tissue has cells enclosed in small cavities within a solid and pliable matrix that resists compression. Which "
     "of the following statements about this tissue are correct?",
     ["It is cartilage, a specialised connective tissue.",
      "In adults, it is present at the tip of the nose, the outer ear joints and between adjacent bones of the "
      "vertebral column.",
      "Its ground substance is hard, non-pliable and rich in calcium salts.",
      "Its cells secrete the matrix that surrounds them.",
      "In vertebrate embryos, most of this tissue is later replaced by bone in the adult."]),
  _opts_cart, "D",
  "Identifying cartilage from its matrix",
  "A solid, pliable matrix that resists compression is NCERT's description of cartilage. Its cells (chondrocytes) are "
  "enclosed in small cavities within the matrix secreted by them. In adults cartilage is present in the tip of the "
  "nose, outer ear joints, between adjacent bones of the vertebral column, limbs and hands. Most of the cartilages "
  "in vertebrate embryos are replaced by bones in adults. A hard, non-pliable matrix rich in calcium salts describes "
  "bone.",
  ["(a) true", "(b) true", "(c) false – that is bone", "(d) true", "(e) true"],
  R_SOA("animal tissue – specialised connective tissue"),
  why_others_wrong="B and C include (c), the bone matrix; A leaves out the embryonic replacement by bone (e).",
  seconds=50)
ms_check("abde", _opts_cart, "D")

Z(SOA, "Animal tissues", "Advanced", "direct",
  "Suppose the cilia of the epithelium lining a person's bronchioles stopped beating, though the cells remained "
  "alive. According to NCERT, which function of this epithelium would be lost?",
  ["Moving particles or mucus in a specific direction over the epithelium",
   "Forming a diffusion boundary for gases",
   "Providing protection against chemical and mechanical stresses",
   "Secreting hormones directly into the fluid bathing the tissue"], "A",
  "Function of ciliated epithelium",
  "NCERT: columnar or cuboidal cells bearing cilia on their free surface form ciliated epithelium, mainly present in "
  "the inner surface of hollow organs like bronchioles and fallopian tubes. Their function is to move particles or "
  "mucus in a specific direction over the epithelium – a job done by the beating cilia.",
  ["Bronchioles → ciliated epithelium", "Cilia beat → move particles/mucus in one direction"],
  R_SOA("animal tissue – epithelial tissue"),
  why_others_wrong="B is the role of squamous epithelium, C of compound epithelium and D of endocrine glands.",
  seconds=45)

_opts_ct = ["(a), (c) and (e) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"]
Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("NCERT classifies connective tissues as loose, dense and specialised. In which of the following pairs do BOTH "
     "tissues fall in the same category?",
     ["Areolar tissue and adipose tissue", "Tendon and ligament", "Cartilage and blood",
      "Connective tissue of the skin and areolar tissue", "Bone and adipose tissue"]),
  _opts_ct, "B",
  "Categories of connective tissue",
  "NCERT: areolar and adipose tissues are both loose connective tissues; tendons and ligaments are both dense regular "
  "connective tissues; cartilage, bones and blood are specialised connective tissues. The connective tissue of the skin is "
  "dense (irregular), unlike loose areolar tissue, and bone (specialised) differs from adipose tissue (loose).",
  ["(a) loose + loose", "(b) dense regular + dense regular", "(c) specialised + specialised",
   "(d) dense (irregular) vs loose", "(e) specialised vs loose"],
  R_SOA("animal tissue – connective tissue"),
  why_others_wrong="A and C include (e); C and D include (d), where the skin's tissue is dense but areolar "
                   "tissue loose.",
  seconds=50)
ms_check("abc", _opts_ct, "B")

# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "Amino acids are substituted methanes. The four substituent groups that occupy the four valency positions of the "
  "α-carbon are:",
  ["Hydrogen, a hydroxyl group, an amino group and a variable R group",
   "Two amino groups, a carboxyl group and hydrogen",
   "Hydrogen, a carboxyl group, an amino group and a variable R group",
   "A carboxyl group, a phosphate group, an amino group and an R group"], "C",
  "Structure of amino acids",
  "NCERT: amino acids are substituted methanes. There are four substituent groups occupying the four valency "
  "positions – hydrogen, carboxyl group, amino group and a variable group designated as the R group. The amino and "
  "acidic groups sit on the same (α) carbon.",
  ["α-carbon: H + COOH + NH₂ + R"],
  R_BIO("analysing chemical composition – amino acids"),
  why_others_wrong="A drops the carboxyl group; B has two amino groups and no R group; D adds a phosphate group, which "
                   "belongs to nucleotides.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "NCERT compares the percentage by weight of elements in the earth's crust and in the human body. Which element "
  "has the highest percentage by weight in BOTH?",
  ["Oxygen", "Carbon", "Silicon", "Hydrogen"], "A",
  "Elemental composition of living and non-living matter",
  "NCERT's table: oxygen is 46.6% of the earth's crust and 65.0% of the human body – the largest share in both. "
  "Carbon is 18.5% of the body but only 0.03% of the crust; silicon is 27.7% of the crust but negligible in the body; "
  "hydrogen is 0.14% of the crust and 0.5% of the body.",
  ["Crust: O 46.6% > Si 27.7%", "Human body: O 65.0% > C 18.5%"],
  R_BIO("how to analyse chemical composition (Table: comparison of elements)"),
  why_others_wrong="Carbon leads only among the non-oxygen elements of the body and is scarce in the crust; silicon is "
                   "negligible in the body; hydrogen is small in both.",
  seconds=25)

Z(BIO, "Proteins and amino acids", "Basic", "statement_pair",
  sp("Proteins are polypeptides, i.e. linear chains of amino acids linked by peptide bonds.",
     "In a polypeptide, the last amino acid of the chain is called the N-terminal amino acid."),
  STATEMENT_PAIR, "C",
  "Proteins as polypeptides",
  "NCERT: proteins are polypeptides – linear chains of amino acids linked by peptide bonds. In the primary structure, "
  "the left end is represented by the first amino acid, called the N-terminal amino acid, and the right end by the "
  "last amino acid, called the C-terminal amino acid.",
  ["Statement I → true", "Statement II → false: the last amino acid is C-terminal"],
  R_BIO("proteins; structure of proteins"),
  why_others_wrong="A and D accept Statement II, which swaps the terminal names; B rejects Statement I, NCERT's "
                   "definition of proteins.",
  seconds=25)

Z(BIO, "Enzymes: properties and action", "Basic", "match_list",
  ml(("item", "description in NCERT"), ["Haem", "Zinc", "NAD", "Apoenzyme"],
     ["Protein portion of an enzyme that needs a co-factor", "Co-enzyme containing the vitamin niacin",
      "Metal-ion co-factor of carboxypeptidase", "Prosthetic group of peroxidase and catalase"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Co-factors and apoenzyme",
  "NCERT: the protein portion of such an enzyme is the apoenzyme. Co-factors are of three kinds: prosthetic groups "
  "(e.g. haem in peroxidase and catalase), co-enzymes (e.g. NAD and NADP, which contain the vitamin niacin) and metal "
  "ions (e.g. zinc for the proteolytic enzyme carboxypeptidase).",
  ["Haem → prosthetic group (IV)", "Zinc → metal ion (III)", "NAD → co-enzyme (II)", "Apoenzyme → protein part (I)"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="A swaps haem and zinc; B swaps zinc and NAD; C swaps NAD and the apoenzyme.",
  seconds=30)

_hb_molecules, _hb_subunits = 5, 4
_hb_n_terminal = _hb_molecules * _hb_subunits
assert _hb_n_terminal == 20
Z(BIO, "Proteins and amino acids", "Basic", "numerical",
  "Adult human haemoglobin consists of four subunits (two of α type and two of β type), each a polypeptide chain. "
  "How many N-terminal amino acids are present in total in 5 molecules of adult human haemoglobin?",
  ["5", "20", "10", "40"], "B",
  "Subunits of haemoglobin",
  "Each polypeptide chain has one N-terminal (first) amino acid. One haemoglobin molecule has four subunits, i.e. "
  "four chains, so it has four N-terminal amino acids; 5 molecules have 5 × 4 = 20.",
  ["Chains per haemoglobin = 4", "N-terminal amino acids = 1 per chain", "Total = 5 × 4 = 20"],
  R_BIO("structure of proteins (quaternary structure of haemoglobin)"),
  shortcut="Count chains, not molecules: 5 × 4.",
  why_others_wrong="5 counts one per molecule; 10 counts only the α (or only the β) chains; 40 counts both the N- and "
                   "C-terminal ends.",
  seconds=30, verified_by=RECOMPUTED)

Z(BIO, "Proteins and amino acids", "Intermediate", "direct",
  "NCERT gives a list of representative inorganic constituents of living tissues. Which of the following belongs to "
  "that list?",
  ["Glucose", "Amino acids", "Nucleotides", "Calcium carbonate (CaCO₃)"], "D",
  "Inorganic constituents of living tissues",
  "NCERT's table of representative inorganic constituents of living tissues lists sodium, potassium, calcium, "
  "magnesium, water and compounds such as NaCl, CaCO₃, PO₄³⁻ and SO₄²⁻. Glucose, amino acids and nucleotides are "
  "carbon compounds – organic constituents of the acid-soluble pool.",
  ["Inorganic: Na⁺, K⁺, Ca²⁺, Mg²⁺, water, NaCl, CaCO₃, PO₄³⁻, SO₄²⁻", "Glucose, amino acids, nucleotides → organic"],
  R_BIO("how to analyse chemical composition (table of inorganic constituents)"),
  why_others_wrong="A, B and C are organic compounds, which NCERT discusses separately from the inorganic "
                   "constituents.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Intermediate", "match_list",
  ml(("term", "meaning"), ["Active site", "Transition state", "Activation energy", "Enzyme–substrate complex"],
     ["Difference in average energy content between the substrate and the transition state",
      "Pocket in the enzyme into which the substrate fits",
      "Obligatory, transient complex formed before the products appear",
      "Unstable, higher-energy structural state between substrate and product"]),
  match_options(M("II", "IV", "I", "III"), [M("IV", "II", "I", "III"), M("II", "I", "IV", "III"),
                                            M("II", "IV", "III", "I")], "A"), "A",
  "Terms of enzyme action",
  "NCERT: the backbone of the enzyme folds to create crevices or pockets; one such pocket is the active site into "
  "which the substrate fits. The substrate must pass through a much higher-energy, unstable transition state to form "
  "the product. The difference in average energy content of S from that of this transition state is the activation "
  "energy. Formation of the ES complex is essential (obligatory) for catalysis and is a transient phenomenon.",
  ["Active site → II", "Transition state → IV", "Activation energy → I", "ES complex → III"],
  R_BIO("enzymes – how do enzymes bring about high rates; nature of enzyme action"),
  why_others_wrong="B swaps the active site and the transition state; C swaps the transition state and activation "
                   "energy; D swaps activation energy and the ES complex.",
  seconds=40)

Z(BIO, "Enzymes: properties and action", "Intermediate", "direct",
  "NCERT notes that the essential chemical components of many co-enzymes are vitamins. A severe deficiency of the "
  "vitamin niacin would most directly impair enzymes that depend on:",
  ["The haem prosthetic group", "Zinc ions", "The co-enzymes NAD and NADP",
   "Metal ions held by coordination bonds"], "C",
  "Vitamins as co-enzyme components",
  "NCERT: the co-enzyme nicotinamide adenine dinucleotide (NAD) and NADP contain the vitamin niacin. Without niacin "
  "these co-enzymes cannot be made, so the enzymes that need them lose activity – catalytic activity is lost when "
  "the co-factor is removed from the enzyme.",
  ["Niacin → part of NAD and NADP", "No co-enzyme → no catalytic activity"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="Haem is a prosthetic group and zinc a metal-ion co-factor; neither is built from niacin.",
  seconds=35)

Z(BIO, "Proteins and amino acids", "Intermediate", "direct",
  "An amino acid has two carboxyl groups and one amino group. Based on NCERT's grouping of amino acids by the number "
  "of amino and carboxyl groups, it is:",
  ["A neutral amino acid, like valine", "An acidic amino acid, like glutamic acid",
   "A basic amino acid, like lysine", "An aromatic amino acid, like tryptophan"], "B",
  "Acidic, basic and neutral amino acids",
  "NCERT: based on the number of amino and carboxyl groups, there are acidic (e.g. glutamic acid), basic (lysine) "
  "and neutral (valine) amino acids. An extra carboxyl (acidic) group makes the amino acid acidic.",
  ["2 COOH > 1 NH₂ → acidic", "Example: glutamic acid"],
  R_BIO("analysing chemical composition – amino acids"),
  why_others_wrong="A neutral amino acid has equal numbers of the two groups; a basic one has the extra amino group; "
                   "'aromatic' refers to the ring in the R group, not to the count of these groups.",
  seconds=35)

Z(BIO, "Proteins and amino acids", "Intermediate", "direct",
  "NCERT lists several functions of proteins. Which of the following is NOT one of them?",
  ["Transporting nutrients across the cell membrane", "Storing hereditary information as a nucleotide sequence",
   "Fighting infectious organisms", "Acting as hormones and as enzymes"], "B",
  "Functions of proteins",
  "NCERT: proteins perform many functions – some transport nutrients across the cell membrane, some fight infectious "
  "organisms, some are hormones and some are enzymes. Nucleotide sequences belong to nucleic acids, which are "
  "polynucleotides, not proteins.",
  ["Transport, defence, hormones, enzymes → protein roles", "Nucleotide sequence → nucleic acids"],
  R_BIO("proteins"),
  why_others_wrong="A, C and D are all in NCERT's list of protein functions.",
  seconds=30)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Cellulose is a homopolymer.",
     "Cellulose is built of only one type of monosaccharide, glucose, repeated many times."),
  ASSERTION_REASON, "A",
  "Homopolymers",
  "NCERT: cellulose is a polymeric polysaccharide consisting of only one type of monosaccharide, i.e. glucose; "
  "cellulose is a homopolymer. A homopolymer is one in which a single type of monomer repeats, so R is exactly why "
  "A holds.",
  ["Homopolymer = one type of monomer repeated", "Cellulose: glucose only → homopolymer"],
  R_BIO("polysaccharides"),
  why_others_wrong="Both statements are true and R defines why cellulose is a homopolymer, so B, C and D are wrong.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("When a tissue is ground in trichloroacetic acid, its enzymes, being proteins, are found in the acid-insoluble "
     "fraction.",
     "Like any other protein, an enzyme has a primary structure, i.e. an amino acid sequence."),
  STATEMENT_PAIR, "A",
  "Enzymes are proteins",
  "Almost all enzymes are proteins. NCERT places proteins in the acid-insoluble (retentate) fraction, which holds the "
  "macromolecules, and states that an enzyme, like any protein, has a primary structure (amino acid sequence) and "
  "also secondary and tertiary structures.",
  ["Statement I → true (proteins are in the acid-insoluble fraction)", "Statement II → true"],
  R_BIO("how to analyse chemical composition; enzymes"),
  why_others_wrong="Both statements hold, so options calling either false are wrong.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Advanced", "match_list",
  ml(("observation on an enzyme", "best explanation"),
     ["Activity is lost on dialysis and restored when the small molecules removed are added back",
      "Activity is lost after heating, though no peptide bond is broken",
      "Activity falls when a chemical closely resembling the substrate is added",
      "Activity falls when the pH is moved away from one particular value"],
     ["Each enzyme has an optimum pH", "Competitive inhibition",
      "The three-dimensional (tertiary) structure has been altered",
      "The enzyme needs a non-protein co-factor"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Interpreting experiments on enzymes",
  "NCERT: co-factors are non-protein constituents whose removal makes the enzyme inactive; heat denatures proteins, "
  "and changes in temperature or pH alter the tertiary structure; a competitive inhibitor closely resembles the "
  "substrate and competes for its binding site; each enzyme shows its highest activity at an optimum pH, with "
  "activity declining on either side.",
  ["Dialysis → co-factor (IV)", "Heating → tertiary structure altered (III)", "Substrate look-alike → competitive "
   "inhibition (II)", "pH away from one value → optimum pH (I)"],
  R_BIO("enzymes – factors affecting enzyme activity; co-factors"),
  why_others_wrong="A swaps the dialysis and heating results; B swaps heating and the substrate look-alike; C swaps "
                   "the inhibitor and the pH results.",
  seconds=55)

Z(BIO, "Proteins and amino acids", "Advanced", "statement_pair",
  sp("Every protein that shows a quaternary structure also has a tertiary structure.",
     "In adult human haemoglobin, all four subunits are identical to one another."),
  STATEMENT_PAIR, "C",
  "Levels of protein structure",
  "NCERT: some proteins are an assembly of more than one polypeptide or subunit, and the manner in which these "
  "individually folded polypeptides (each with its own tertiary structure) are arranged with respect to each other "
  "is the quaternary structure – so quaternary structure presupposes tertiary structure. Adult human haemoglobin has "
  "4 subunits, of which two are identical to each other: two subunits of α type and two of β type.",
  ["Statement I → true (subunits are individually folded)", "Statement II → false (2 α + 2 β)"],
  R_BIO("structure of proteins"),
  why_others_wrong="A and D accept four identical subunits; B rejects Statement I, though the subunits of a "
                   "quaternary structure are themselves folded chains.",
  seconds=45)

Z(BIO, "Enzyme classification", "Advanced", "direct",
  "Succinic dehydrogenase oxidises succinate by removing hydrogen, which is passed to another substrate. Malonate "
  "reduces its activity. Which option correctly gives the class of the enzyme and the nature of the inhibition?",
  ["Transferase; competitive inhibition", "Hydrolase; competitive inhibition",
   "Oxidoreductase; inhibition by heat denaturation of the enzyme", "Oxidoreductase; competitive inhibition"], "D",
  "Classifying an enzyme and its inhibitor",
  "Moving hydrogen from one substrate to another is an oxidation-reduction between two substrates, so the enzyme is "
  "an oxidoreductase (NCERT excludes hydrogen transfer from the transferases). NCERT gives malonate as the example of "
  "a competitive inhibitor: it closely resembles succinate in structure and competes with it for the "
  "substrate-binding site of succinic dehydrogenase.",
  ["H removed from S, passed to S′ → oxidoreductase", "Malonate ~ succinate → competitive inhibition"],
  R_BIO("enzymes – classification and nomenclature; inhibition"),
  why_others_wrong="A uses transferase, which NCERT keeps for groups other than hydrogen; B uses hydrolase, which needs "
                   "water to break bonds; C gives the wrong kind of inhibition.",
  seconds=45)

_opts_nt = ["(a) and (d) only", "(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"]
Z(BIO, "Nucleic acids", "Advanced", "multi_statement",
  ms("On complete hydrolysis, one molecule of a compound gives one molecule each of adenine, ribose and phosphoric "
     "acid. Which of the following statements about the compound are correct?",
     ["It is a nucleotide, adenylic acid.",
      "Removing its phosphate would leave the nucleoside adenosine.",
      "Its nitrogenous base is a substituted purine.",
      "It is a nucleoside, because it contains a sugar.",
      "Its sugar is a hexose."]),
  _opts_nt, "B",
  "Nucleosides and nucleotides",
  "NCERT: a nitrogenous base attached to a sugar is a nucleoside (e.g. adenosine); when a phosphate group is also "
  "esterified to the sugar, it is a nucleotide (e.g. adenylic acid). Adenine is a substituted purine. Ribose is a "
  "pentose. A compound with base + sugar + phosphate is therefore a nucleotide, not a nucleoside.",
  ["Base + sugar + phosphate → nucleotide (adenylic acid)", "Base + sugar → nucleoside (adenosine)",
   "(d) false – phosphate makes it a nucleotide", "(e) false – ribose is a pentose"],
  R_BIO("analysing chemical composition – nitrogen bases, nucleosides and nucleotides"),
  why_others_wrong="A and D include (d), which ignores the phosphate; C includes (e) and leaves out (a).",
  seconds=50)
ms_check("abc", _opts_nt, "B")

_opts_en = ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b) and (d) only", "(a), (b), (c) and (d) only"]
Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("For a reaction S → P whose product lies at a lower energy level than the substrate, which of the following "
     "statements are correct according to NCERT?",
     ["The substrate must pass through a much higher-energy transition state to form the product.",
      "The reaction is an exothermic reaction.",
      "Being exothermic, the reaction does not need to pass through a transition state.",
      "An enzyme catalysing it brings down this energy barrier, making the transition of S to P easier.",
      "The transition state is a stable structural state."]),
  _opts_en, "C",
  "Energy barrier of reactions",
  "NCERT: if P is at a lower level than S, the reaction is exothermic. Whether exothermic or endothermic, S has to go "
  "through a much higher-energy, unstable transition state to form P. Enzymes bring down this energy barrier, making "
  "the transition of S to P easier.",
  ["(a) true", "(b) true", "(c) false – every reaction passes through the transition state", "(d) true",
   "(e) false – it is unstable"],
  R_BIO("enzymes – how do enzymes bring about such high rates of chemical conversions"),
  why_others_wrong="A and D include (c); A and B include (e); B also leaves out (a).",
  seconds=50)
ms_check("abd", _opts_en, "C")

# ================================================================ Breathing and Exchange of Gases (B3 I5 A3)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Respiratory system", "Basic", "direct",
  "NCERT lists the steps involved in respiration. Which of the following is NOT one of them?",
  ["Breathing or pulmonary ventilation", "Diffusion of gases across the alveolar membrane",
   "Transport of gases by the blood", "Synthesis of haemoglobin in the red bone marrow"], "D",
  "Steps of respiration",
  "NCERT: respiration involves (i) breathing or pulmonary ventilation, (ii) diffusion of gases (O₂ and CO₂) across "
  "the alveolar membrane, (iii) transport of gases by the blood, (iv) diffusion of O₂ and CO₂ between blood and "
  "tissues, and (v) utilisation of O₂ by the cells for catabolic reactions and resultant release of CO₂ (cellular "
  "respiration). Making haemoglobin is not one of these steps.",
  ["Five steps: ventilation → alveolar diffusion → transport → tissue diffusion → cellular respiration"],
  R_BRE("respiratory organs – human respiratory system (steps of respiration)"),
  why_others_wrong="A, B and C are the first three steps in NCERT's list.",
  seconds=20)

_po2_atm, _p_total = 159, 760
_o2_percent = _po2_atm / _p_total * 100
assert abs(_o2_percent - 20.9) < 0.05
Z(BRE, "Exchange and transport of gases", "Basic", "numerical",
  "Partial pressure is the pressure contributed by an individual gas in a mixture of gases. The pO₂ of atmospheric "
  "air is about 159 mm Hg. If the total atmospheric pressure is 760 mm Hg, oxygen makes up about what percentage of "
  "atmospheric air?",
  ["79%", "21%", "15.9%", "4.8%"], "B",
  "Partial pressure",
  "The partial pressure of a gas is its share of the total pressure, so the fraction of O₂ = pO₂ / total pressure = "
  "159 / 760 ≈ 0.209, i.e. about 21%.",
  ["Fraction = 159 / 760 ≈ 0.209", "≈ 21%"],
  R_BRE("exchange of gases (partial pressures)"),
  shortcut="160/760 is a little over 1/5, so about 21%.",
  why_others_wrong="79% is the share of the rest of the air, not O₂; 15.9% divides 159 by 1000 instead of 760; 4.8 is "
                   "the inverted ratio 760/159.",
  seconds=30, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Basic", "statement_pair",
  sp("Besides the partial pressure of O₂, the partial pressure of CO₂, the hydrogen ion concentration and the "
     "temperature can interfere with the binding of O₂ to haemoglobin.",
     "Oxygen is carried by haemoglobin in the form of carbamino-haemoglobin."),
  STATEMENT_PAIR, "C",
  "Factors affecting oxygen binding",
  "NCERT: the binding of oxygen with haemoglobin is primarily related to the partial pressure of O₂; the partial "
  "pressure of CO₂, hydrogen ion concentration and temperature are the other factors which can interfere with this "
  "binding. Oxygen is carried as oxyhaemoglobin; carbamino-haemoglobin is the form in which haemoglobin carries CO₂.",
  ["Statement I → true", "Statement II → false: O₂ forms oxyhaemoglobin; CO₂ forms carbamino-haemoglobin"],
  R_BRE("transport of gases – transport of oxygen and carbon dioxide"),
  why_others_wrong="A and D accept Statement II, which confuses the two complexes; B rejects Statement I, which is "
                   "NCERT's text.",
  seconds=30)

Z(BRE, "Exchange and transport of gases", "Intermediate", "direct",
  "In a vigorously working muscle, the pO₂ is low, the pCO₂ and hydrogen ion concentration are high and the "
  "temperature is higher. For the blood flowing through this muscle, these conditions:",
  ["Favour dissociation of oxygen from oxyhaemoglobin, releasing O₂ to the muscle",
   "Favour the formation of oxyhaemoglobin, so less O₂ reaches the muscle",
   "Prevent CO₂ from diffusing from the muscle into the blood",
   "Have no effect, because O₂ binding to haemoglobin depends only on temperature"], "A",
  "Unloading of oxygen at the tissues",
  "NCERT: in the tissues, where low pO₂, high pCO₂, high H⁺ concentration and higher temperature exist, the "
  "conditions are favourable for dissociation of oxygen from oxyhaemoglobin. A working muscle has these conditions "
  "in stronger form, so oxygen is released to it. High pCO₂ in the muscle also drives CO₂ into the blood.",
  ["Low pO₂ + high pCO₂ + high H⁺ + higher temperature → O₂ dissociates from oxyhaemoglobin"],
  R_BRE("transport of gases – transport of oxygen"),
  why_others_wrong="B describes the alveolar conditions (high pO₂, low pCO₂, less H⁺, lower temperature); C is the "
                   "reverse of what high muscle pCO₂ does; D ignores that binding depends primarily on pO₂.",
  seconds=40)

_opts_cond = ["(a), (b) and (c) only", "(c), (d) and (e) only", "(b), (c), (d) and (e) only",
              "(a), (b), (c) and (d) only"]
Z(BRE, "Respiratory system", "Intermediate", "multi_statement",
  ms("Which of the following belong to the conducting part of the human respiratory system?",
     ["External nostrils", "Larynx", "Trachea", "Terminal bronchioles", "Alveolar ducts"]),
  _opts_cond, "D",
  "Conducting and exchange parts",
  "NCERT: the part starting with the external nostrils up to the terminal bronchioles constitutes the conducting "
  "part, whereas the alveoli and their ducts form the respiratory or exchange part. The larynx and trachea lie "
  "between the nostrils and the terminal bronchioles, so they are conducting structures.",
  ["(a)–(d): nostrils to terminal bronchioles → conducting", "(e) alveolar ducts → exchange part"],
  R_BRE("respiratory organs – human respiratory system"),
  why_others_wrong="A leaves out the terminal bronchioles, the last conducting structure; B and C include the "
                   "alveolar ducts, which belong to the exchange part.",
  seconds=35)
ms_check("abcd", _opts_cond, "D")

Z(BRE, "Exchange and transport of gases", "Intermediate", "assertion_reason",
  ar("At the alveoli, CO₂ is released from the bicarbonate carried in the blood.",
     "Where pCO₂ is low, as at the alveoli, the reaction catalysed by carbonic anhydrase proceeds in the opposite "
     "direction, forming CO₂ and H₂O."),
  ASSERTION_REASON, "A",
  "Carbonic anhydrase works in both directions",
  "NCERT: at the tissue site, where pCO₂ is high, CO₂ diffuses into blood and forms HCO₃⁻ and H⁺. At the alveolar "
  "site, where pCO₂ is low, the reaction proceeds in the opposite direction, leading to the formation of CO₂ and H₂O. "
  "Thus CO₂ trapped as bicarbonate at the tissue level is released at the alveoli – R explains A.",
  ["Tissues: CO₂ + H₂O → H₂CO₃ → HCO₃⁻ + H⁺", "Alveoli (low pCO₂): reaction reverses → CO₂ released"],
  R_BRE("transport of gases – transport of carbon dioxide"),
  why_others_wrong="Both statements are true and the reversed reaction is how bicarbonate yields CO₂, so B, C and D "
                   "are wrong.",
  seconds=35)

Z(BRE, "Respiratory volumes", "Intermediate", "match_list",
  ml(("respiratory capacity", "NCERT definition"),
     ["Inspiratory capacity", "Expiratory capacity", "Functional residual capacity", "Total lung capacity"],
     ["Volume of air remaining in the lungs after a normal expiration",
      "Total volume of air accommodated in the lungs at the end of a forced inspiration",
      "Total volume of air a person can inspire after a normal expiration",
      "Total volume of air a person can expire after a normal inspiration"]),
  match_options(M("III", "IV", "I", "II"), [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"),
                                            M("III", "I", "IV", "II")], "C"), "C",
  "Respiratory capacities",
  "NCERT: inspiratory capacity – total volume of air a person can inspire after a normal expiration (TV + IRV); "
  "expiratory capacity – total volume a person can expire after a normal inspiration (TV + ERV); functional residual "
  "capacity – volume that remains in the lungs after a normal expiration (ERV + RV); total lung capacity – total "
  "volume accommodated in the lungs at the end of a forced inspiration (RV + ERV + TV + IRV).",
  ["IC → III", "EC → IV", "FRC → I", "TLC → II"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="A swaps the inspiratory and expiratory capacities; B swaps FRC and TLC; D swaps the expiratory "
                   "capacity and FRC.",
  seconds=45)

Z(BRE, "Respiratory system", "Intermediate", "statement_pair",
  sp("The exchange part of the respiratory system is the site of actual diffusion of O₂ and CO₂ between blood and "
     "atmospheric air.",
     "The primary, secondary and tertiary bronchi belong to the exchange part of the respiratory system."),
  STATEMENT_PAIR, "C",
  "Exchange part of the respiratory system",
  "NCERT: the alveoli and their ducts form the respiratory or exchange part, which is the site of actual diffusion "
  "of O₂ and CO₂ between blood and atmospheric air. The bronchi lie between the nostrils and the terminal "
  "bronchioles, i.e. in the conducting part.",
  ["Statement I → true", "Statement II → false: bronchi are conducting"],
  R_BRE("respiratory organs – human respiratory system"),
  why_others_wrong="A and D accept Statement II; B rejects Statement I, which is NCERT's description of the exchange "
                   "part.",
  seconds=30)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "Suppose all the haemoglobin in a person's RBCs were prevented from binding respiratory gases, while carbonic "
  "anhydrase and plasma remained normal. Using NCERT's percentages, roughly what share of O₂ transport and of CO₂ "
  "transport would be lost?",
  ["About 3% of O₂ transport and about 70% of CO₂ transport",
   "About 97% of O₂ transport and about 20–25% of CO₂ transport",
   "About 97% of O₂ transport and about 70% of CO₂ transport",
   "All O₂ transport and only about 7% of CO₂ transport"], "B",
  "Share of haemoglobin in gas transport",
  "NCERT: about 97% of O₂ is transported by RBCs (as oxyhaemoglobin) and the remaining 3% dissolved in plasma. About "
  "20–25% of CO₂ is carried by haemoglobin as carbamino-haemoglobin, about 70% as bicarbonate (formed with the help "
  "of carbonic anhydrase) and about 7% dissolved in plasma. Blocking haemoglobin removes the oxyhaemoglobin and "
  "carbamino-haemoglobin routes only.",
  ["O₂ lost: 97% (only the dissolved 3% remains)", "CO₂ lost: carbamino share, 20–25%",
   "Bicarbonate (70%) and dissolved (7%) CO₂ unaffected"],
  R_BRE("transport of gases"),
  why_others_wrong="A gives the dissolved O₂ share and the bicarbonate share; C wrongly blocks bicarbonate transport, "
                   "which needs carbonic anhydrase, not haemoglobin; D ignores the 3% of O₂ dissolved in plasma and "
                   "gives the dissolved CO₂ share.",
  seconds=55)

_opts_co2 = ["(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c) and (e) only",
             "(a), (b), (c) and (e) only"]
Z(BRE, "Exchange and transport of gases", "Advanced", "multi_statement",
  ms("Trace a CO₂ molecule produced in a tissue cell until it leaves the body. Which of the following statements are "
     "correct according to NCERT?",
     ["It diffuses from the tissue into the blood, because the pCO₂ of the tissue (about 45 mm Hg) is higher than "
      "that of the oxygenated blood reaching it (about 40 mm Hg).",
      "In the blood it is likely to be converted, with the help of carbonic anhydrase, into HCO₃⁻ and H⁺.",
      "At the alveoli, where pCO₂ is low, the reaction reverses and CO₂ is formed again.",
      "At the alveoli, it diffuses from the alveolar air into the blood.",
      "It finally leaves through the conducting part of the respiratory system during expiration."]),
  _opts_co2, "D",
  "The journey of carbon dioxide",
  "NCERT: CO₂ diffuses from tissues (pCO₂ 45 mm Hg) into blood (40 mm Hg). About 70% of CO₂ is carried as "
  "bicarbonate formed with the help of carbonic anhydrase. At the alveolar site, where pCO₂ is low, the reaction "
  "reverses, forming CO₂ and H₂O; CO₂ then diffuses from blood (45 mm Hg) into the alveoli (40 mm Hg), not the other "
  "way. The alveolar air is released out by expiration through the conducting passages.",
  ["(a) true", "(b) true (the major route, about 70%)", "(c) true", "(d) false – CO₂ moves from blood to alveoli",
   "(e) true"],
  R_BRE("exchange of gases; transport of carbon dioxide"),
  why_others_wrong="A and B include (d), the reversed direction; C leaves out the bicarbonate step (b).",
  seconds=60)
ms_check("abce", _opts_co2, "D")

Z(BRE, "Respiratory volumes", "Advanced", "statement_pair",
  sp("Vital capacity equals the inspiratory capacity plus the expiratory reserve volume.",
     "Vital capacity also equals the expiratory capacity plus the inspiratory reserve volume."),
  STATEMENT_PAIR, "A",
  "Combining respiratory volumes",
  "NCERT: vital capacity = ERV + TV + IRV. Inspiratory capacity = TV + IRV, so IC + ERV = ERV + TV + IRV = VC. "
  "Expiratory capacity = TV + ERV, so EC + IRV = TV + ERV + IRV = VC. Both statements hold.",
  ["VC = ERV + TV + IRV", "IC + ERV = (TV + IRV) + ERV = VC", "EC + IRV = (TV + ERV) + IRV = VC"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="Both sums contain each of TV, IRV and ERV exactly once and no RV, so both equal VC.",
  why_others_wrong="Any option calling either statement false misses that each sum contains TV, IRV and ERV once.",
  seconds=50)

# ================================================================ Body Fluids and Circulation (B4 I6 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Coagulation and lymph", "Basic", "match_list",
  ml(("substance in plasma", "role described in NCERT"), ["Fibrinogen", "Globulins", "Albumins", "Thrombokinase"],
     ["Help in osmotic balance", "Enzyme complex required to form thrombin from prothrombin",
      "Primarily involved in the defence mechanisms of the body", "Needed for clotting or coagulation of blood"]),
  match_options(M("IV", "III", "I", "II"), [M("II", "III", "I", "IV"), M("IV", "I", "III", "II"),
                                            M("III", "IV", "I", "II")], "A"), "A",
  "Plasma proteins and clotting",
  "NCERT: fibrinogen, globulins and albumins are the major plasma proteins. Fibrinogens are needed for clotting or "
  "coagulation of blood, globulins are primarily involved in defence mechanisms and albumins help in osmotic "
  "balance. An enzyme complex, thrombokinase, is required for the formation of thrombin from prothrombin.",
  ["Fibrinogen → IV", "Globulins → III", "Albumins → I", "Thrombokinase → II"],
  R_BFC("blood – plasma; coagulation of blood"),
  why_others_wrong="B swaps fibrinogen and thrombokinase; C swaps globulins and albumins; D swaps fibrinogen and "
                   "globulins.",
  seconds=30)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "Leucocytes are grouped into granulocytes and agranulocytes. Which option lists only granulocytes?",
  ["Lymphocytes and monocytes", "Neutrophils, eosinophils and basophils", "Neutrophils and monocytes",
   "Basophils and lymphocytes"], "B",
  "Granulocytes and agranulocytes",
  "NCERT: neutrophils, eosinophils and basophils are different types of granulocytes, while lymphocytes and monocytes "
  "are agranulocytes.",
  ["Granulocytes: neutrophils, eosinophils, basophils", "Agranulocytes: lymphocytes, monocytes"],
  R_BFC("blood – formed elements: leucocytes"),
  why_others_wrong="A lists the two agranulocytes; C and D each mix one granulocyte with one agranulocyte.",
  seconds=20)

_beats_per_min, _sounds_per_cycle = 72, 2
_sounds_per_min = _beats_per_min * _sounds_per_cycle
assert _sounds_per_min == 144
Z(BFC, "Cardiac cycle and ECG", "Basic", "numerical",
  "NCERT states that during each cardiac cycle two prominent sounds ('lub' and 'dub') are produced. If a person's "
  "heart beats 72 times per minute, how many heart sounds are produced in one minute?",
  ["72", "36", "288", "144"], "D",
  "Heart sounds per cardiac cycle",
  "Each heartbeat is one cardiac cycle, and each cycle produces two prominent sounds – the first ('lub') with closure "
  "of the tricuspid and bicuspid valves and the second ('dub') with closure of the semilunar valves. So 72 cycles "
  "give 72 × 2 = 144 sounds.",
  ["Cycles per minute = 72", "Sounds per cycle = 2", "Sounds per minute = 72 × 2 = 144"],
  R_BFC("cardiac cycle (heart sounds)"),
  why_others_wrong="72 counts one sound per beat; 36 halves the beats instead of doubling them; 288 counts four sounds "
                   "per cycle.",
  seconds=25, verified_by=RECOMPUTED)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Neutrophils and monocytes are phagocytic cells which destroy foreign organisms entering the body.",
     "Lymphocytes are of two major types, B and T, and both are responsible for the immune responses of the body."),
  STATEMENT_PAIR, "A",
  "Roles of leucocytes",
  "NCERT: neutrophils and monocytes (6–8 per cent) are phagocytic cells which destroy foreign organisms entering the "
  "body. Lymphocytes are of two major types – B and T forms – and both B and T lymphocytes are responsible for the "
  "immune responses of the body.",
  ["Statement I → true", "Statement II → true"],
  R_BFC("blood – formed elements: leucocytes"),
  why_others_wrong="Both statements are NCERT's own lines, so options calling either false are wrong.",
  seconds=25)

Z(BFC, "Coagulation and lymph", "Intermediate", "direct",
  "Plasma and serum are compared. Which of the following is present in plasma but absent from serum?",
  ["Albumins", "Glucose", "Fibrinogen", "Globulins"], "C",
  "Plasma versus serum",
  "NCERT: plasma without the clotting factors is called serum. Fibrinogen, the plasma protein needed for clotting, "
  "is used up when blood clots (it is converted into fibrin threads), so serum lacks it. Albumins, globulins and "
  "glucose remain in serum.",
  ["Serum = plasma − clotting factors", "Fibrinogen → needed for clotting → absent from serum"],
  R_BFC("blood – plasma; coagulation of blood"),
  why_others_wrong="Albumins (osmotic balance), globulins (defence) and glucose are not clotting factors, so they "
                   "remain in serum.",
  seconds=30)

Z(BFC, "Blood and blood groups", "Intermediate", "direct",
  "A blood report of a person suffering from an allergy shows that one type of leucocyte is above its usual share. "
  "Going by NCERT's description of leucocytes, which type is it most likely to be?",
  ["Eosinophils", "Neutrophils", "Monocytes", "Erythrocytes"], "A",
  "Eosinophils and allergy",
  "NCERT: eosinophils (2–3 per cent) resist infections and are also associated with allergic reactions. Neutrophils "
  "and monocytes are described as phagocytes, and erythrocytes are not leucocytes at all.",
  ["Allergy → eosinophils (associated with allergic reactions)"],
  R_BFC("blood – formed elements: leucocytes"),
  why_others_wrong="Neutrophils and monocytes are described as phagocytic cells; erythrocytes are red blood cells, not "
                   "leucocytes.",
  seconds=30)

Z(BFC, "Double circulation and regulation", "Intermediate", "match_list",
  ml(("blood vessel", "blood it carries"), ["Pulmonary artery", "Pulmonary veins", "Aorta", "Vena cava"],
     ["Deoxygenated blood from the body to the right atrium",
      "Oxygenated blood from the left ventricle to the body tissues",
      "Oxygenated blood from the lungs to the left atrium",
      "Deoxygenated blood from the right ventricle to the lungs"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Vessels of double circulation",
  "NCERT: deoxygenated blood pumped by the right ventricle enters the pulmonary artery, which carries it to the "
  "lungs; oxygenated blood is carried by the pulmonary veins into the left atrium (pulmonary circulation). "
  "Oxygenated blood entering the aorta from the left ventricle is carried to the tissues, and deoxygenated blood is "
  "collected by the veins and vena cava and emptied into the right atrium (systemic circulation).",
  ["Pulmonary artery → IV", "Pulmonary veins → III", "Aorta → II", "Vena cava → I"],
  R_BFC("double circulation"),
  why_others_wrong="A swaps the pulmonary artery and veins; C swaps the aorta and vena cava; D swaps the pulmonary "
                   "veins and the aorta.",
  seconds=40)

Z(BFC, "Coagulation and lymph", "Intermediate", "assertion_reason",
  ar("Platelets are involved in the coagulation or clotting of blood.",
     "Platelets are nucleated cells that are formed in the spleen."),
  ASSERTION_REASON, "C",
  "Platelets",
  "NCERT: platelets, also called thrombocytes, are cell fragments produced from megakaryocytes (special cells in the "
  "bone marrow). Blood normally contains 1,50,000–3,50,000 platelets per mm³. Platelets can release a variety of "
  "substances, most of which are involved in the coagulation or clotting of blood. A is true; R is false on both "
  "counts – they are cell fragments, and they come from the bone marrow.",
  ["A → true", "R → false: cell fragments from megakaryocytes of the bone marrow"],
  R_BFC("blood – formed elements: platelets"),
  why_others_wrong="A and B treat R as true; D denies the clotting role NCERT gives platelets.",
  seconds=30)

Z(BFC, "Double circulation and regulation", "Intermediate", "statement_pair",
  sp("In amphibians, the left atrium receives oxygenated blood from the gills, lungs or skin, and the right atrium "
     "receives deoxygenated blood from the other body parts.",
     "In fishes, the heart has two atria and one ventricle."),
  STATEMENT_PAIR, "C",
  "Hearts of fishes and amphibians",
  "NCERT: amphibians and reptiles (except crocodiles) have a 3-chambered heart; in amphibians the left atrium "
  "receives oxygenated blood from the gills/lungs/skin and the right atrium gets deoxygenated blood from other body "
  "parts. Fishes have a 2-chambered heart with an atrium and a ventricle.",
  ["Statement I → true", "Statement II → false: fish heart = one atrium + one ventricle"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A and D accept a three-chambered fish heart; B rejects Statement I, which is NCERT's description "
                   "of the amphibian heart.",
  seconds=35)

_opts_as = ["(a), (b) and (d) only", "(b), (d) and (e) only", "(c), (d) and (e) only", "(a), (b) and (c) only"]
Z(BFC, "Cardiac cycle and ECG", "Intermediate", "multi_statement",
  ms("Which of the following statements correctly describe the phase of atrial systole in the cardiac cycle?",
     ["It is started by an action potential from the SAN that stimulates both atria to contract simultaneously.",
      "It increases the flow of blood into the ventricles by about 30 per cent.",
      "The tricuspid and bicuspid valves are open during this phase.",
      "The semilunar valves are open during this phase.",
      "The ventricles are also in systole during this phase."]),
  _opts_as, "D",
  "Atrial systole",
  "NCERT: the SAN generates an action potential which stimulates both atria to undergo a simultaneous contraction – "
  "the atrial systole. This increases the flow of blood into the ventricles by about 30 per cent; blood can enter "
  "the ventricles because the tricuspid and bicuspid valves are open, while the semilunar valves stay closed. "
  "Ventricular systole begins only after the impulse is conducted to the ventricles, by which time the atria relax.",
  ["(a) true", "(b) true", "(c) true", "(d) false – semilunar valves open only in ventricular systole",
   "(e) false – atria and ventricles do not contract together"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A, B and C each include (d) or (e), which describe ventricular systole, not atrial systole.",
  seconds=45)
ms_check("abc", _opts_as, "D")

_opts_tr = ["(b), (c) and (e) only", "(a), (b) and (c) only", "(b) and (c) only", "(a), (c), (d) and (e) only"]
Z(BFC, "Blood and blood groups", "Advanced", "multi_statement",
  ms("A donor has blood group B, Rh-ve. Considering both the ABO and the Rh systems, which of the following "
     "recipients can safely receive this blood?",
     ["A, Rh+ve", "B, Rh+ve", "AB, Rh+ve", "O, Rh+ve", "AB, Rh-ve"]),
  _opts_tr, "A",
  "Combining ABO and Rh compatibility",
  "ABO: group B blood carries antigen B, so it can go only to recipients without anti-B antibodies – groups B and AB "
  "(group A has anti-B, group O has both anti-A and anti-B). Rh: the donor's blood is Rh-ve, i.e. it carries no Rh "
  "antigen, so it does not expose any recipient to Rh antigen; it is safe for both Rh+ve and Rh-ve recipients of "
  "groups B and AB.",
  ["ABO: B blood → B or AB recipients only", "Rh-ve donor → no Rh antigen → fine for Rh+ve and Rh-ve",
   "Safe: (b), (c), (e)"],
  R_BFC("blood groups – ABO grouping and Rh grouping"),
  why_others_wrong="B and D include group A (anti-B) or group O (anti-A and anti-B) recipients; C leaves out the AB, "
                   "Rh-ve recipient.",
  seconds=60)
ms_check("bce", _opts_tr, "A")

Z(BFC, "Blood and blood groups", "Advanced", "statement_pair",
  sp("A person with blood group O has both anti-A and anti-B antibodies in his plasma, so he can receive blood only "
     "from group O donors.",
     "A person with blood group AB has neither anti-A nor anti-B antibodies, so his blood can be given to persons "
     "of any ABO group."),
  STATEMENT_PAIR, "C",
  "Antigens decide donation, antibodies decide reception",
  "NCERT's table: group O has no antigens but both anti-A and anti-B antibodies, and can receive only from O. Group "
  "AB has both A and B antigens and no antibodies – which is why AB persons can accept blood from any group "
  "(universal recipients). But AB blood carries both antigens, so it can be given only to AB persons. Lacking "
  "antibodies makes AB a universal recipient, not a universal donor.",
  ["Statement I → true", "Statement II → false: AB blood has A and B antigens → donor to AB only"],
  R_BFC("blood groups – ABO grouping"),
  why_others_wrong="A and D accept Statement II, confusing the recipient's antibodies with the donor's antigens; B "
                   "rejects Statement I, which matches NCERT's table.",
  seconds=50)

Z(BFC, "Human heart", "Advanced", "direct",
  "Which sequence correctly traces oxygenated blood from the lungs to a capillary in the hand?",
  ["Pulmonary artery → left atrium → bicuspid valve → left ventricle → aorta → arteries → capillary",
   "Pulmonary veins → left atrium → bicuspid valve → left ventricle → semilunar valve → aorta → arteries → capillary",
   "Pulmonary veins → right atrium → tricuspid valve → right ventricle → aorta → arteries → capillary",
   "Pulmonary veins → left ventricle → bicuspid valve → left atrium → aorta → arteries → capillary"], "B",
  "Path of oxygenated blood",
  "NCERT: oxygenated blood from the lungs is carried by the pulmonary veins into the left atrium; it passes through "
  "the opening guarded by the bicuspid (mitral) valve into the left ventricle, and is pumped through the semilunar "
  "valve at the opening of the aorta into the aorta, which carries it through arteries, arterioles and capillaries "
  "to the tissues (systemic circulation).",
  ["Lungs → pulmonary veins → left atrium", "→ bicuspid valve → left ventricle", "→ semilunar valve → aorta → "
   "systemic arteries → capillaries"],
  R_BFC("human circulatory system; double circulation"),
  why_others_wrong="A starts with the pulmonary artery, which carries blood to the lungs; C sends oxygenated blood "
                   "through the right side of the heart; D reverses the atrium and the ventricle.",
  seconds=45)

Z(BFC, "Circulatory disorders", "Advanced", "match_list",
  ml(("disorder", "description in NCERT"),
     ["Hypertension", "Coronary artery disease", "Angina", "Heart failure"],
     ["The heart is not pumping blood effectively enough to meet the needs of the body",
      "Acute chest pain appearing when not enough oxygen reaches the heart muscle",
      "Deposits of calcium, fat, cholesterol and fibrous tissue narrow the lumen of the vessels supplying the heart "
      "muscle",
      "Repeated blood pressure readings of 140/90 mm Hg or higher"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Disorders of the circulatory system",
  "NCERT: hypertension is blood pressure higher than normal (repeated checks of 140/90 mm Hg or higher); coronary "
  "artery disease (atherosclerosis) is caused by deposits of calcium, fat, cholesterol and fibrous tissue that "
  "narrow the lumen of the arteries supplying the heart muscle; angina is acute chest pain when not enough oxygen "
  "reaches the heart muscle; heart failure is the state in which the heart is not pumping blood effectively enough "
  "to meet the needs of the body.",
  ["Hypertension → IV", "CAD → III", "Angina → II", "Heart failure → I"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="A swaps hypertension and CAD; B swaps CAD and angina; C swaps angina and heart failure.",
  seconds=45)

Z(BFC, "Blood and blood groups", "Advanced", "direct",
  "In erythroblastosis foetalis, anti-Rh antibodies made by a sensitised Rh-ve mother destroy the RBCs of her Rh+ve "
  "foetus. Why do these antibodies not destroy the mother's own RBCs?",
  ["Her RBCs are Rh-ve, so they lack the Rh antigen against which the antibodies act",
   "The antibodies are made only after delivery and are removed from her blood immediately",
   "Her RBCs carry both A and B antigens, which block the antibodies",
   "The placenta prevents the antibodies from entering the mother's circulation"], "A",
  "Rh antigen and anti-Rh antibodies",
  "NCERT: Rh+ve persons have the Rh antigen on their RBCs, Rh-ve persons do not. An Rh-ve mother exposed to the Rh "
  "antigen of her Rh+ve foetus makes antibodies against the Rh antigen; in a later pregnancy these can leak into the "
  "foetal blood and destroy the foetal RBCs. Antibodies act only on cells carrying their antigen, and the mother's "
  "own RBCs carry no Rh antigen.",
  ["Antibody acts against Rh antigen", "Mother Rh-ve → no Rh antigen on her RBCs → unaffected"],
  R_BFC("blood groups – Rh grouping"),
  why_others_wrong="B is wrong because the antibodies persist and affect the next pregnancy; C confuses the ABO and "
                   "Rh systems; D is wrong because the antibodies are made in the mother's own body.",
  seconds=45)

# ================================================================ Excretory Products and their Elimination (B4 I5 A5)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

_co2_ml_per_min = 200
_co2_l_per_day = _co2_ml_per_min * 60 * 24 / 1000
assert _co2_l_per_day == 288
Z(EXC, "Modes of excretion", "Basic", "numerical",
  "According to NCERT, our lungs remove large amounts of CO₂, about 200 mL per minute. At this rate, about how much "
  "CO₂ do the lungs remove in one day?",
  ["12 L", "288 L", "28.8 L", "2.88 L"], "B",
  "Lungs as accessory excretory organs",
  "200 mL per minute × 60 minutes × 24 hours = 288,000 mL = 288 L per day.",
  ["Per hour: 200 × 60 = 12,000 mL", "Per day: 12,000 × 24 = 288,000 mL = 288 L"],
  R_EXC("role of other organs in excretion"),
  why_others_wrong="12 L is the amount per hour only; 28.8 L and 2.88 L slip the decimal point by factors of 10 and "
                   "100 in the mL-to-L conversion.",
  seconds=30, verified_by=RECOMPUTED)

Z(EXC, "Nephron structure", "Basic", "direct",
  "In a nephron, the Malpighian corpuscle, the PCT and the DCT are situated in the cortical region of the kidney. "
  "Which part dips into the medulla?",
  ["Bowman's capsule", "Glomerulus", "Loop of Henle", "Proximal convoluted tubule"], "C",
  "Position of nephron parts",
  "NCERT: the Malpighian corpuscle (glomerulus + Bowman's capsule), PCT and DCT of the nephron are situated in the "
  "cortical region of the kidney, whereas the loop of Henle dips into the medulla.",
  ["Cortex: Malpighian corpuscle, PCT, DCT", "Medulla: loop of Henle"],
  R_EXC("human excretory system (nephron)"),
  why_others_wrong="Bowman's capsule and the glomerulus make up the Malpighian corpuscle, and the PCT is cortical too.",
  seconds=20)

Z(EXC, "Nephron structure", "Basic", "statement_pair",
  sp("A minute vessel of the peritubular capillary network runs parallel to Henle's loop, forming the U-shaped vasa "
     "recta.",
     "The vasa recta is absent or highly reduced in cortical nephrons."),
  STATEMENT_PAIR, "A",
  "Vasa recta",
  "NCERT: the efferent arteriole emerging from the glomerulus forms a fine capillary network around the renal tubule "
  "called the peritubular capillaries; a minute vessel of this network runs parallel to Henle's loop, forming a "
  "'U'-shaped vasa recta. The vasa recta is absent or highly reduced in cortical nephrons.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("human excretory system (nephron)"),
  why_others_wrong="Both lines are NCERT's description of the vasa recta, so options calling either false are wrong.",
  seconds=25)

Z(EXC, "Urine formation", "Basic", "statement_pair",
  sp("Glomerular filtration, in which almost all the constituents of the plasma except the proteins pass into the "
     "lumen of Bowman's capsule, is called ultrafiltration.",
     "Glomerular filtration is caused by the glomerular capillary blood pressure."),
  STATEMENT_PAIR, "A",
  "Glomerular filtration",
  "NCERT: the first step in urine formation is the filtration of blood, carried out by the glomerulus. On average "
  "1100–1200 mL of blood is filtered per minute; the glomerular capillary blood pressure causes filtration through "
  "three layers, and the blood is filtered so finely that almost all the constituents of the plasma except the "
  "proteins pass onto the lumen of Bowman's capsule. Hence it is considered a process of ultrafiltration.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("urine formation"),
  why_others_wrong="Both statements are from NCERT's account of filtration, so options calling either false are wrong.",
  seconds=25)

Z(EXC, "Modes of excretion", "Intermediate", "match_list",
  ml(("organ or secretion", "what it eliminates, according to NCERT"),
     ["Liver (bile)", "Sweat glands", "Sebaceous glands", "Saliva"],
     ["Sterols, hydrocarbons and waxes", "Small amounts of nitrogenous wastes",
      "A watery fluid containing NaCl, small amounts of urea and lactic acid",
      "Bilirubin, biliverdin, cholesterol, degraded steroid hormones, vitamins and drugs"]),
  match_options(M("IV", "III", "I", "II"), [M("III", "IV", "I", "II"), M("IV", "I", "III", "II"),
                                            M("IV", "III", "II", "I")], "B"), "B",
  "Role of other organs in excretion",
  "NCERT: the liver secretes bile containing bilirubin, biliverdin, cholesterol, degraded steroid hormones, vitamins "
  "and drugs, which pass out with digestive wastes. Sweat is a watery fluid containing NaCl, small amounts of urea, "
  "lactic acid, etc. Sebaceous glands eliminate sterols, hydrocarbons and waxes through sebum. Small amounts of "
  "nitrogenous wastes can be eliminated through saliva too.",
  ["Liver → IV", "Sweat glands → III", "Sebaceous glands → I", "Saliva → II"],
  R_EXC("role of other organs in excretion"),
  why_others_wrong="A swaps the liver and sweat glands; C swaps sweat and sebum; D swaps sebum and saliva.",
  seconds=40)

Z(EXC, "Modes of excretion", "Intermediate", "assertion_reason",
  ar("Protonephridia are the excretory structures of insects such as cockroaches.",
     "Protonephridia or flame cells are primarily concerned with ionic and fluid volume regulation, i.e. "
     "osmoregulation."),
  ASSERTION_REASON, "D",
  "Excretory structures of invertebrates",
  "NCERT: protonephridia or flame cells are the excretory structures in Platyhelminthes (e.g. Planaria), rotifers, "
  "some annelids and the cephalochordate Amphioxus; they are primarily concerned with osmoregulation. Insects, "
  "including cockroaches, use Malpighian tubules. So A is false and R is true.",
  ["A → false: insects have Malpighian tubules", "R → true"],
  R_EXC("excretory structures in animals"),
  why_others_wrong="A and B accept the false assertion; C rejects R, which is NCERT's statement about flame cells.",
  seconds=30)

_opts_kid = ["(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only",
             "(a), (b), (d) and (e) only"]
Z(EXC, "Nephron structure", "Intermediate", "multi_statement",
  ms("Which of the following statements about the structure of the human kidney are correct?",
     ["The outer layer of the kidney is a tough capsule.",
      "The medulla is divided into a few conical masses, the medullary pyramids, projecting into the calyces.",
      "The columns of Bertini are extensions of the medulla into the cortex.",
      "Inner to the hilum is a broad, funnel-shaped renal pelvis with projections called calyces.",
      "The ureter, blood vessels and nerves enter the kidney through the hilum."]),
  _opts_kid, "D",
  "Internal structure of the kidney",
  "NCERT: the outer layer of the kidney is a tough capsule; inside are the outer cortex and inner medulla. The "
  "medulla is divided into a few conical masses (medullary pyramids) projecting into the calyces. The cortex extends "
  "in between the medullary pyramids as renal columns called columns of Bertini. Towards the centre of the inner "
  "concave surface is the hilum, through which the ureter, blood vessels and nerves enter; inner to it is the renal "
  "pelvis with projections called calyces.",
  ["(a) true", "(b) true", "(c) false – they are extensions of the cortex", "(d) true", "(e) true"],
  R_EXC("human excretory system"),
  why_others_wrong="A, B and C all include (c), which reverses cortex and medulla.",
  seconds=45)
ms_check("abde", _opts_kid, "D")

Z(EXC, "Disorders and dialysis", "Intermediate", "direct",
  "In haemodialysis, heparin is added to the blood drained from the patient before it is pumped into the dialysing "
  "unit, and anti-heparin is added before the cleared blood is returned to the body. Anti-heparin is added so that:",
  ["Nitrogenous wastes leave the blood faster", "The blood regains its normal ability to clot once back in the body",
   "The blood does not clot inside the dialysing unit", "The dialysing fluid matches the composition of plasma"], "B",
  "Anticoagulant and its reversal in haemodialysis",
  "NCERT: blood drained from a convenient artery is pumped into the dialysing unit after adding an anticoagulant like "
  "heparin, and the cleared blood is pumped back to the body through a vein after adding anti-heparin. Heparin keeps "
  "blood from clotting in the machine; anti-heparin counteracts it, so the returned blood can clot normally again.",
  ["Heparin = anticoagulant (no clotting in the unit)", "Anti-heparin → reverses it before return"],
  R_EXC("disorders of the excretory system (haemodialysis)"),
  why_others_wrong="A is the job of the concentration gradient; C is the role of heparin, not anti-heparin; D describes "
                   "how the dialysing fluid is prepared.",
  seconds=35)

Z(EXC, "Urine formation", "Intermediate", "direct",
  "In the counter-current mechanism, NaCl transported out by the ascending limb of Henle's loop is exchanged with the "
  "descending limb of the vasa recta. What happens to this NaCl next, according to NCERT?",
  ["It is excreted at once in the urine", "It is carried straight back to the glomerulus",
   "It is returned to the interstitium by the ascending portion of the vasa recta",
   "It is converted into urea within the vasa recta"], "C",
  "Recycling of NaCl in the medulla",
  "NCERT: NaCl is transported by the ascending limb of Henle's loop and exchanged with the descending limb of the "
  "vasa recta; NaCl is returned to the interstitium by the ascending portion of the vasa recta. Together with urea "
  "from the collecting tubule, this keeps up the increasing osmolarity towards the inner medulla.",
  ["Ascending limb of loop → NaCl out", "→ descending vasa recta", "→ ascending vasa recta → back to interstitium"],
  R_EXC("mechanism of concentration of the filtrate"),
  why_others_wrong="A, B and D are not described by NCERT; NaCl is not converted into urea, and recycling it keeps it "
                   "in the medulla rather than sending it away.",
  seconds=35)

_opts_dm = ["(a), (b), (c) and (d) only", "(a), (b) and (e) only", "(b), (c) and (d) only",
            "(a), (c), (d) and (e) only"]
Z(EXC, "Disorders and dialysis", "Advanced", "multi_statement",
  ms("Urine analysis of a patient shows glucose and ketone bodies. Which of the following statements are correct?",
     ["The patient shows glycosuria.", "The patient shows ketonuria.",
      "These findings are indicative of diabetes mellitus.",
      "Glucose is normally absent from urine because the renal tubules reabsorb it actively.",
      "These findings indicate diabetes insipidus caused by a deficiency of ADH."]),
  _opts_dm, "A",
  "Urine analysis",
  "NCERT: presence of glucose (glycosuria) and ketone bodies (ketonuria) in urine are indicative of diabetes "
  "mellitus. Normally, substances like glucose are reabsorbed actively from the filtrate. Diabetes insipidus, caused "
  "by impaired ADH synthesis or release, leads to loss of water (diuresis), not to glucose in the urine.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – that is diabetes mellitus, not insipidus"],
  R_EXC("micturition (analysis of urine); regulation of kidney function"),
  why_others_wrong="B and D include diabetes insipidus (e); C leaves out glycosuria (a), which the glucose shows.",
  seconds=45)
ms_check("abcd", _opts_dm, "A")

Z(EXC, "Regulation of kidney function", "Advanced", "match_list",
  ml(("regulatory factor", "main effect described in NCERT"),
     ["ADH", "Angiotensin II", "Aldosterone", "Atrial natriuretic factor"],
     ["Vasodilation and a fall in blood pressure, acting as a check on the renin–angiotensin mechanism",
      "Reabsorption of Na⁺ and water from the distal parts of the tubule",
      "Powerful vasoconstriction, and activation of the adrenal cortex",
      "Water reabsorption from the latter parts of the tubule, preventing diuresis"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Hormonal regulation of the kidney",
  "NCERT: ADH facilitates water reabsorption from the latter parts of the tubule, preventing diuresis. Angiotensin II, "
  "being a powerful vasoconstrictor, raises glomerular blood pressure and GFR, and activates the adrenal cortex to "
  "release aldosterone. Aldosterone causes reabsorption of Na⁺ and water from the distal parts of the tubule. ANF "
  "causes vasodilation and decreases blood pressure, acting as a check on the renin–angiotensin mechanism.",
  ["ADH → IV", "Angiotensin II → III", "Aldosterone → II", "ANF → I"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A swaps ADH and angiotensin II; B swaps angiotensin II and aldosterone; C swaps aldosterone and "
                   "ANF.",
  seconds=50)

Z(EXC, "Urine formation", "Advanced", "direct",
  "During glomerular filtration, fluid leaves the glomerular blood and enters the lumen of Bowman's capsule. In what "
  "order does it cross the three layers that NCERT describes?",
  ["Epithelium of Bowman's capsule → basement membrane → endothelium of glomerular blood vessels",
   "Endothelium of glomerular blood vessels → basement membrane → epithelium of Bowman's capsule",
   "Endothelium of glomerular blood vessels → epithelium of Bowman's capsule → basement membrane",
   "Basement membrane → endothelium of glomerular blood vessels → epithelium of Bowman's capsule"], "B",
  "Layers of the filtration membrane",
  "NCERT: blood is filtered through three layers – the endothelium of the glomerular blood vessels, the epithelium of "
  "Bowman's capsule, and a basement membrane between these two. The epithelial cells of Bowman's capsule (podocytes) "
  "leave filtration slits. Fluid leaving the blood therefore crosses the capillary endothelium first, then the "
  "basement membrane lying between, and finally the capsule's epithelium, entering the capsule lumen.",
  ["Blood side: endothelium", "Middle: basement membrane", "Capsule side: epithelium (podocytes)"],
  R_EXC("urine formation"),
  why_others_wrong="A gives the reverse direction; C and D misplace the basement membrane, which lies between the "
                   "other two layers.",
  seconds=45)

_opts_nep = ["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (d) only",
             "(a), (c) and (d) only"]
Z(EXC, "Nephron structure", "Advanced", "multi_statement",
  ms("Compare cortical and juxtamedullary nephrons. Which of the following statements are correct?",
     ["In both types, the Malpighian corpuscle lies in the cortex.",
      "In juxtamedullary nephrons, Henle's loop is very long and runs deep into the medulla.",
      "Cortical nephrons form the majority of the nephrons.",
      "The DCTs of many nephrons open into a common collecting duct.",
      "Only juxtamedullary nephrons have peritubular capillaries around their tubules."]),
  _opts_nep, "C",
  "Cortical and juxtamedullary nephrons",
  "NCERT: the Malpighian corpuscle, PCT and DCT of every nephron are situated in the cortex. In the majority of "
  "nephrons, the loop of Henle is too short and extends only very little into the medulla (cortical nephrons); in "
  "some, the loop is very long and runs deep into the medulla (juxtamedullary nephrons). The DCTs of many nephrons "
  "open into a straight collecting duct. The efferent arteriole of every nephron forms peritubular capillaries; it is "
  "the vasa recta that is absent or highly reduced in cortical nephrons.",
  ["(a) true", "(b) true", "(c) true", "(d) true",
   "(e) false – peritubular capillaries surround all tubules; only the vasa recta is reduced in cortical nephrons"],
  R_EXC("human excretory system (nephron)"),
  why_others_wrong="A and B include (e), which confuses peritubular capillaries with the vasa recta; D leaves out "
                   "the deep loop of juxtamedullary nephrons (b).",
  seconds=55)
ms_check("abcd", _opts_nep, "C")

Z(EXC, "Nephron structure", "Advanced", "direct",
  "Which sequence correctly traces the flow of blood through the vessels of a nephron?",
  ["Renal artery → efferent arteriole → glomerulus → afferent arteriole → peritubular capillaries",
   "Renal artery → afferent arteriole → peritubular capillaries → glomerulus → efferent arteriole",
   "Renal artery → glomerulus → afferent arteriole → efferent arteriole → vasa recta",
   "Renal artery → afferent arteriole → glomerulus → efferent arteriole → peritubular capillaries and vasa recta"],
  "D",
  "Blood supply of the nephron",
  "NCERT: the glomerulus is a tuft of capillaries formed by the afferent arteriole, a fine branch of the renal artery. "
  "Blood from the glomerulus is carried away by an efferent arteriole, which forms a fine capillary network around "
  "the renal tubule called the peritubular capillaries; a minute vessel of this network runs parallel to Henle's loop "
  "as the vasa recta.",
  ["Renal artery → afferent arteriole", "→ glomerulus → efferent arteriole", "→ peritubular capillaries (+ vasa "
   "recta)"],
  R_EXC("human excretory system (nephron)"),
  why_others_wrong="A swaps the afferent and efferent arterioles; B sends blood to the peritubular capillaries before "
                   "the glomerulus; C puts the glomerulus before the afferent arteriole that forms it.",
  seconds=45)

# ================================================================ Locomotion and Movement (B5 I6 A5)
R_LOC = lambda s: ref("Locomotion and Movement", s)

_body_kg = 60
_muscle_low, _muscle_high = _body_kg * 40 / 100, _body_kg * 50 / 100
assert (_muscle_low, _muscle_high) == (24, 30)
Z(LOC, "Muscle contraction", "Basic", "numerical",
  "According to NCERT, muscles contribute about 40–50 per cent of the body weight of a human adult. For an adult "
  "weighing 60 kg, the mass of the muscles would be about:",
  ["24–30 kg", "42–48 kg", "12–15 kg", "4–5 kg"], "A",
  "Share of muscle in body weight",
  "40% of 60 kg = 24 kg and 50% of 60 kg = 30 kg, so muscles weigh about 24–30 kg.",
  ["0.40 × 60 = 24 kg", "0.50 × 60 = 30 kg"],
  R_LOC("muscle"),
  why_others_wrong="42–48 kg uses 70–80 per cent; 12–15 kg uses 20–25 per cent (halving the share); 4–5 kg treats the "
                   "percentage as a fraction of 10 kg.",
  seconds=25, verified_by=RECOMPUTED)

Z(LOC, "Skeletal system", "Basic", "match_list",
  ml(("bone", "part of the skeleton it belongs to"), ["Femur", "Scapula", "Ilium", "Sternum"],
     ["Axial skeleton", "Pelvic girdle", "Pectoral girdle", "Hind limb"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "B"), "B",
  "Divisions of the skeleton",
  "NCERT: the femur (thigh bone) is a bone of the hind limb; each half of the pectoral girdle consists of a clavicle "
  "and a scapula; each coxal bone of the pelvic girdle is formed by the fusion of the ilium, ischium and pubis; the "
  "sternum, ribs, vertebral column and skull form the axial skeleton.",
  ["Femur → hind limb (IV)", "Scapula → pectoral girdle (III)", "Ilium → pelvic girdle (II)",
   "Sternum → axial skeleton (I)"],
  R_LOC("skeletal system"),
  why_others_wrong="A swaps the femur and the scapula; C swaps the scapula and the ilium; D swaps the ilium and the "
                   "sternum.",
  seconds=30)

Z(LOC, "Muscle contraction", "Basic", "statement_pair",
  sp("The portion of a myofibril between two successive Z-lines is considered the functional unit of contraction and "
     "is called a sarcomere.",
     "In a resting state, the edges of the thin filaments on either side of the thick filaments partially overlap the "
     "free ends of the thick filaments, leaving the central part of the thick filaments not overlapped."),
  STATEMENT_PAIR, "A",
  "The sarcomere",
  "NCERT: the portion of the myofibril between two successive 'Z' lines is the functional unit of contraction, the "
  "sarcomere. In a resting state, the edges of thin filaments on either side of the thick filaments partially overlap "
  "the free ends of the thick filaments, leaving the central part of the thick filaments; this central part, not "
  "overlapped by thin filaments, is the 'H' zone.",
  ["Statement I → true", "Statement II → true (the non-overlapped part is the H-zone)"],
  R_LOC("structure of contractile proteins / skeletal muscle"),
  why_others_wrong="Both statements are NCERT's own description, so options calling either false are wrong.",
  seconds=30)

Z(LOC, "Skeletal system", "Basic", "statement_pair",
  sp("Each upper limb is made of 30 bones.",
     "Each lower limb (hind limb) – femur, tibia, fibula, tarsals, metatarsals, phalanges and the patella – is also "
     "made of 30 bones."),
  STATEMENT_PAIR, "A",
  "Bones of the limbs",
  "NCERT: each limb is made of 30 bones. Upper limb: humerus 1 + radius and ulna 2 + carpals 8 + metacarpals 5 + "
  "phalanges 14 = 30. Hind limb: femur 1 + tibia and fibula 2 + tarsals 7 + metatarsals 5 + phalanges 14 + patella 1 "
  "= 30.",
  ["Upper limb: 1 + 2 + 8 + 5 + 14 = 30", "Hind limb: 1 + 2 + 7 + 5 + 14 + 1 = 30"],
  R_LOC("skeletal system – appendicular skeleton"),
  why_others_wrong="Both statements hold, since the patella makes up for the hind limb's one fewer tarsal.",
  seconds=30)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "The junction between a motor neuron and the sarcolemma of a muscle fibre is called the:",
  ["Synapse between two neurons", "Z-line", "Sarcomere", "Neuromuscular junction or motor-end plate"], "D",
  "Neuromuscular junction",
  "NCERT: a motor neuron along with the muscle fibres connected to it constitutes a motor unit; the junction between "
  "a motor neuron and the sarcolemma of the muscle fibre is called the neuromuscular junction or motor-end plate.",
  ["Motor neuron + sarcolemma junction → neuromuscular junction (motor-end plate)"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A synapse in NCERT's neural chapter joins two neurons; the Z-line and sarcomere are parts of a "
                   "myofibril.",
  seconds=20)

Z(LOC, "Skeletal system", "Intermediate", "match_list",
  ml(("ribs", "description in NCERT"), ["True ribs", "Vertebrochondral (false) ribs", "Floating ribs", "Every rib"],
     ["Has two articulation surfaces on its dorsal end (bicephalic)",
      "11th and 12th pairs, not connected ventrally",
      "8th, 9th and 10th pairs, joined to the seventh rib with the help of hyaline cartilage",
      "First seven pairs, attached directly to the sternum"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "C"), "C",
  "Types of ribs",
  "NCERT: there are 12 pairs of ribs. Each rib is a thin flat bone connected dorsally to the vertebral column and "
  "ventrally to the sternum, with two articulation surfaces on its dorsal end (bicephalic). The first seven pairs are "
  "true ribs, attached dorsally to the thoracic vertebrae and ventrally to the sternum. The 8th, 9th and 10th pairs "
  "do not articulate directly with the sternum but join the seventh rib with hyaline cartilage (vertebrochondral or "
  "false ribs). The last two pairs (11th and 12th) are not connected ventrally (floating ribs).",
  ["True → IV", "Vertebrochondral → III", "Floating → II", "Every rib → I"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A swaps true and vertebrochondral ribs; B swaps vertebrochondral and floating ribs; D swaps "
                   "floating ribs with the feature common to all ribs.",
  seconds=40)

Z(LOC, "Joints", "Intermediate", "direct",
  "The vertebral column can bend a little because of the joints between adjacent vertebrae. These joints are:",
  ["Fibrous joints, which allow no movement at all", "Synovial ball and socket joints, which allow movement in all "
   "directions", "Cartilaginous joints, which permit limited movement", "Synovial pivot joints, which allow rotation "
   "only"], "C",
  "Cartilaginous joints",
  "NCERT: in cartilaginous joints the bones involved are joined together with the help of cartilages; the joint "
  "between the adjacent vertebrae in the vertebral column is of this pattern and it permits limited movements. "
  "Fibrous joints (skull sutures) allow no movement, and synovial joints allow considerable movement.",
  ["Adjacent vertebrae → joined by cartilage → cartilaginous joint → limited movement"],
  R_LOC("joints"),
  why_others_wrong="A describes the skull sutures; B describes the shoulder joint; D describes the joint between the "
                   "atlas and axis.",
  seconds=30)

Z(LOC, "Types of movement", "Intermediate", "assertion_reason",
  ar("Coordinated movement of the cilia in the trachea helps us remove dust particles and some foreign substances "
     "inhaled with atmospheric air.",
     "Macrophages and leucocytes in the blood show amoeboid movement, effected by pseudopodia formed by the streaming "
     "of protoplasm."),
  ASSERTION_REASON, "B",
  "Ciliary and amoeboid movement",
  "Both are NCERT statements, but about two different kinds of movement. The trachea's cleaning action is ciliary "
  "movement of its ciliated epithelium; the amoeboid movement of macrophages and leucocytes is a separate process "
  "that has nothing to do with clearing the airway. R is true but does not explain A.",
  ["A → true (ciliary movement)", "R → true (amoeboid movement)", "R describes a different movement → no "
   "explanation"],
  R_LOC("types of movement"),
  why_others_wrong="A treats an unrelated statement as the explanation; C and D reject statements that NCERT makes.",
  seconds=30)

_opts_rel = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only", "(a), (b) and (c) only"]
Z(LOC, "Muscle contraction", "Intermediate", "multi_statement",
  ms("Which of the following happen when a skeletal muscle fibre relaxes after contraction?",
     ["Ca²⁺ ions are pumped back into the sarcoplasmic cisternae.",
      "The active sites on the actin filaments are masked again.",
      "The Z-lines return to their original positions.",
      "The A-bands lengthen.",
      "New cross bridges keep forming between myosin heads and actin."]),
  _opts_rel, "D",
  "Relaxation of a muscle fibre",
  "NCERT: the cross-bridge cycle continues till the Ca²⁺ ions are pumped back to the sarcoplasmic cisternae, "
  "resulting in the masking of actin filaments. This causes the Z-lines to return to their original position, i.e. "
  "relaxation. The A-bands keep their length throughout, and with the active sites masked no new cross bridges form.",
  ["(a) true", "(b) true", "(c) true", "(d) false – A-band length does not change",
   "(e) false – masked sites block cross bridges"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A and C include the A-band change (d); B and C include continued cross-bridge formation (e).",
  seconds=40)
ms_check("abc", _opts_rel, "D")

Z(LOC, "Muscular and skeletal disorders", "Intermediate", "match_list",
  ml(("disorder", "cause or nature"), ["Tetany", "Gout", "Myasthenia gravis", "Osteoporosis"],
     ["Decreased levels of estrogen are a common cause", "Auto-immune disorder affecting the neuromuscular junction",
      "Accumulation of uric acid crystals in the joints", "Low Ca²⁺ in body fluids"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "A"), "A",
  "Disorders of muscular and skeletal system",
  "NCERT: tetany – rapid spasms (wild contractions) in muscle due to low Ca²⁺ in body fluid; gout – inflammation of "
  "joints due to accumulation of uric acid crystals; myasthenia gravis – auto-immune disorder affecting the "
  "neuromuscular junction; osteoporosis – age-related decrease in bone mass, with decreased levels of estrogen a "
  "common cause.",
  ["Tetany → IV", "Gout → III", "Myasthenia gravis → II", "Osteoporosis → I"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="B swaps tetany and gout; C swaps gout and myasthenia gravis; D swaps myasthenia gravis and "
                   "osteoporosis.",
  seconds=40)

Z(LOC, "Muscle contraction", "Intermediate", "statement_pair",
  sp("During contraction of a muscle, the I-bands get reduced, whereas the A-bands retain their length.",
     "During contraction, the thick filaments slide over the thin filaments towards the Z-lines."),
  STATEMENT_PAIR, "C",
  "Sliding filament theory",
  "NCERT: muscle contraction is explained by the sliding filament theory, which states that contraction takes place "
  "by the sliding of the thin filaments over the thick filaments. The cross bridges pull the actin filaments towards "
  "the centre of the A-band, and the Z-lines attached to them are pulled inwards. The I-bands get reduced while the "
  "A-bands retain their length.",
  ["Statement I → true", "Statement II → false: thin filaments slide over thick filaments, towards the centre"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A and D accept Statement II, which reverses which filament slides and the direction; B rejects "
                   "Statement I, which is NCERT's observation.",
  seconds=35)

_opts_ach = ["(a), (b) and (e) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(b), (c) and (d) only"]
Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("A toxin blocks the release of acetylcholine at the neuromuscular junctions of a skeletal muscle, while the "
     "motor neuron still carries signals from the CNS. Which of the following are expected?",
     ["No action potential is generated in the sarcolemma of the muscle fibres.",
      "Ca²⁺ is not released from the sarcoplasmic reticulum into the sarcoplasm.",
      "Troponin continues to mask the active sites for myosin on the actin filaments.",
      "The muscle fails to contract in response to the nerve signals.",
      "The muscle fibres stay permanently contracted."]),
  _opts_ach, "B",
  "Excitation–contraction coupling",
  "NCERT: a neural signal reaching the neuromuscular junction releases acetylcholine, which generates an action "
  "potential in the sarcolemma; this spreads through the fibre and causes the release of Ca²⁺ into the sarcoplasm. "
  "Ca²⁺ binds a subunit of troponin, removing the masking of active sites on actin so that myosin can bind. Without "
  "acetylcholine, none of these steps begins, so the fibre stays relaxed rather than contracted.",
  ["No ACh → no action potential", "→ no Ca²⁺ release → active sites stay masked", "→ no cross bridges → no "
   "contraction"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A and C include (e), but without the trigger the fibre cannot contract at all; D leaves out (a), "
                   "the first step that fails.",
  seconds=55)
ms_check("abcd", _opts_ach, "B")

Z(LOC, "Muscle contraction", "Advanced", "statement_pair",
  sp("In a resting sarcomere, a thin cross-section cut through the H-zone would show thick filaments but no thin "
     "filaments.",
     "In a resting sarcomere, a cross-section cut through the I-band would show both thick and thin filaments."),
  STATEMENT_PAIR, "C",
  "Filament arrangement in the sarcomere",
  "NCERT: the light I-band contains actin (thin filaments); the dark A-band contains myosin (thick filaments). The "
  "central part of the thick filaments not overlapped by thin filaments is the H-zone. So a cut through the H-zone "
  "meets only thick filaments, and a cut through the I-band meets only thin filaments.",
  ["H-zone: thick only → Statement I true", "I-band: thin only → Statement II false"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="A and D place thick filaments in the I-band; B rejects Statement I, which follows from the "
                   "definition of the H-zone.",
  seconds=50)

_opts_mov = ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only",
             "(a), (b), (c) and (d) only"]
Z(LOC, "Types of movement", "Advanced", "multi_statement",
  ms("Which of the following statements about movement in different organisms are correct according to NCERT?",
     ["In Paramecium, cilia help in the movement of food through the cytopharynx and in locomotion.",
      "Hydra uses its tentacles for capturing its prey and also for locomotion.",
      "Protozoans like Euglena move by flagellar movement.",
      "The water current in the canal system of sponges is maintained by flagellar movement.",
      "Amoeba moves by ciliary movement."]),
  _opts_mov, "D",
  "Movement in living organisms",
  "NCERT: in Paramecium, cilia help in the movement of food through the cytopharynx and in locomotion; Hydra uses its "
  "tentacles for capturing prey and also for locomotion. Flagellar movement helps in the swimming of spermatozoa, "
  "the maintenance of the water current in the canal system of sponges and the locomotion of protozoans like "
  "Euglena. Amoeba moves by streaming of protoplasm forming pseudopodia (amoeboid movement).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – Amoeba shows amoeboid movement"],
  R_LOC("types of movement"),
  why_others_wrong="A and C include (e); B leaves out Paramecium (a), which NCERT describes.",
  seconds=45)
ms_check("abcd", _opts_mov, "D")

Z(LOC, "Muscle contraction", "Advanced", "direct",
  "Which sequence correctly orders the events that lead to the sliding of filaments in a skeletal muscle fibre?",
  ["ACh release → Ca²⁺ release into sarcoplasm → action potential in sarcolemma → troponin unmasks actin → cross "
   "bridge forms → actin pulled to the centre of the A-band",
   "ACh release at the neuromuscular junction → action potential in sarcolemma → Ca²⁺ released into sarcoplasm → "
   "Ca²⁺ binds troponin, unmasking active sites on actin → myosin head binds actin (cross bridge) → actin pulled to "
   "the centre of the A-band",
   "Action potential in sarcolemma → ACh release → myosin head binds actin → Ca²⁺ released → troponin unmasks "
   "actin → sliding",
   "ACh release → action potential in sarcolemma → myosin head binds actin → Ca²⁺ binds troponin → sliding"], "B",
  "Order of events in muscle contraction",
  "NCERT: a neural signal reaching the neuromuscular junction releases acetylcholine, which generates an action "
  "potential in the sarcolemma. This spreads through the fibre and causes the release of Ca²⁺ into the sarcoplasm. "
  "Ca²⁺ binds a subunit of troponin, removing the masking of active sites on actin; utilising energy from ATP "
  "hydrolysis, the myosin head binds the exposed sites to form a cross bridge, which pulls the attached actin "
  "filaments towards the centre of the A-band.",
  ["ACh → action potential → Ca²⁺ release → troponin unmasks sites → cross bridge → sliding"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="A releases Ca²⁺ before the action potential that triggers it; C puts the action potential before "
                   "ACh and binding before unmasking; D lets myosin bind before Ca²⁺ has unmasked the active sites.",
  seconds=50)

Z(LOC, "Skeletal system", "Advanced", "direct",
  "Which pair correctly names the parts of the scapula that articulate with the clavicle and with the head of the "
  "humerus, respectively?",
  ["Acromion; glenoid cavity", "Glenoid cavity; acromion", "Acetabulum; glenoid cavity", "Acromion; acetabulum"], "A",
  "Pectoral girdle",
  "NCERT: the scapula has a slightly elevated ridge called the spine, which projects as a flat, expanded process, the "
  "acromion; the clavicle articulates with it. Below the acromion is a depression, the glenoid cavity, which "
  "articulates with the head of the humerus to form the shoulder joint. The acetabulum is a cavity of the coxal bone "
  "(pelvic girdle), where the thigh bone articulates.",
  ["Clavicle ↔ acromion", "Humerus head ↔ glenoid cavity", "Acetabulum belongs to the pelvic girdle"],
  R_LOC("skeletal system – appendicular skeleton (girdles)"),
  why_others_wrong="B reverses the two; C and D use the acetabulum, which is part of the pelvic girdle, not the "
                   "scapula.",
  seconds=40)

# ================================================================ Neural Control and Coordination (B3 I5 A3)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nerve impulse generation and conduction", "Basic", "direct",
  "At a stimulated site of an axon, the brief rise in Na⁺ permeability is quickly followed by a rise in permeability "
  "to another ion. Diffusion of which ion out of the axon restores the resting potential at that site?",
  ["Na⁺", "Ca²⁺", "Cl⁻", "K⁺"], "D",
  "Repolarisation of the axonal membrane",
  "NCERT: the rise in stimulus-induced permeability to Na⁺ is extremely short-lived. It is quickly followed by a rise "
  "in permeability to K⁺. Within a fraction of a second, K⁺ diffuses outside the membrane and restores the resting "
  "potential of the membrane at the site of excitation, and the fibre becomes once more responsive to further "
  "stimulation.",
  ["Na⁺ in → depolarisation", "K⁺ out → resting potential restored"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="Na⁺ enters during depolarisation; NCERT does not involve Ca²⁺ or Cl⁻ in restoring the axon's "
                   "resting potential.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "match_list",
  ml(("component of the neural system", "role"),
     ["Afferent nerve fibres", "Efferent nerve fibres", "Somatic neural system", "Autonomic neural system"],
     ["Relays impulses from the CNS to the involuntary organs and smooth muscles",
      "Relays impulses from the CNS to the skeletal muscles",
      "Transmit regulatory impulses from the CNS to the concerned peripheral tissues and organs",
      "Transmit impulses from tissues and organs to the CNS"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Divisions of the peripheral neural system",
  "NCERT: the nerve fibres of the PNS are of two types – afferent fibres transmit impulses from tissues/organs to the "
  "CNS, and efferent fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues/organs. The "
  "somatic neural system relays impulses from the CNS to skeletal muscles, while the autonomic neural system "
  "transmits impulses from the CNS to the involuntary organs and smooth muscles.",
  ["Afferent → IV", "Efferent → III", "Somatic → II", "Autonomic → I"],
  R_NEU("human neural system"),
  why_others_wrong="A swaps afferent and efferent fibres; C swaps the somatic and autonomic systems; D swaps efferent "
                   "fibres and the somatic system.",
  seconds=30)

Z(NEU, "Nervous system divisions", "Basic", "statement_pair",
  sp("Inside the skull, the human brain is covered by cranial meninges.",
     "The innermost of the cranial meninges, the pia mater, is in contact with the brain tissue."),
  STATEMENT_PAIR, "A",
  "Cranial meninges",
  "NCERT: the human brain is well protected by the skull. Inside the skull, the brain is covered by cranial meninges "
  "consisting of an outer layer called the dura mater, a very thin middle layer called the arachnoid and an inner "
  "layer, the pia mater, which is in contact with the brain tissue.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("central neural system – human brain"),
  why_others_wrong="Both statements are NCERT's own lines, so options calling either false are wrong.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Intermediate", "direct",
  "A disease damages the amygdala and hippocampus of a person's brain. Using NCERT's account of the limbic system, "
  "which functions are most likely to be disturbed?",
  ["Regulation of sexual behaviour, expression of emotional reactions such as excitement, pleasure, rage and fear, "
   "and motivation",
   "Control of respiration, cardiovascular reflexes and gastric secretions",
   "Communication between the left and right cerebral hemispheres",
   "Conduction of impulses from the skin to the spinal cord"], "A",
  "The limbic system",
  "NCERT: the inner parts of the cerebral hemispheres and a group of associated deep structures like the amygdala and "
  "hippocampus form the limbic lobe or limbic system. Along with the hypothalamus, it is involved in the regulation "
  "of sexual behaviour, expression of emotional reactions (e.g. excitement, pleasure, rage and fear) and motivation.",
  ["Amygdala + hippocampus → limbic system", "Limbic system + hypothalamus → sexual behaviour, emotions, "
   "motivation"],
  R_NEU("central neural system – forebrain"),
  why_others_wrong="B is the role of the medulla oblongata, C of the corpus callosum, and D of afferent fibres of the "
                   "PNS.",
  seconds=35)

Z(NEU, "Neuron and nerves", "Intermediate", "assertion_reason",
  ar("Bipolar neurons are found in the retina of the eye.",
     "Bipolar neurons have one axon and two or more dendrites."),
  ASSERTION_REASON, "C",
  "Types of neurons",
  "NCERT: based on the number of axons and dendrites, neurons are multipolar (one axon and two or more dendrites; "
  "found in the cerebral cortex), bipolar (one axon and one dendrite; found in the retina of the eye) and unipolar "
  "(cell body with one axon only; found usually in the embryonic stage). A is true, but R describes a multipolar "
  "neuron.",
  ["A → true", "R → false: two or more dendrites = multipolar; bipolar = one dendrite"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="A and B accept R, which describes multipolar neurons; D rejects A, which NCERT states.",
  seconds=30)

_opts_fb = ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (d) only",
            "(a), (b), (c) and (e) only"]
Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following structures belong to the forebrain?",
     ["Cerebrum", "Thalamus", "Hypothalamus", "Pons", "Amygdala and hippocampus of the limbic system"]),
  _opts_fb, "D",
  "Parts of the forebrain",
  "NCERT: the forebrain consists of the cerebrum, thalamus and hypothalamus. The inner parts of the cerebral "
  "hemispheres and a group of associated deep structures like the amygdala and hippocampus form the limbic system, "
  "so they too lie in the forebrain. The pons belongs to the hindbrain.",
  ["(a), (b), (c) → forebrain", "(e) → deep parts of the cerebral hemispheres → forebrain", "(d) pons → hindbrain"],
  R_NEU("central neural system – forebrain"),
  why_others_wrong="A, B and C all include the pons, a hindbrain structure; A also leaves out the hypothalamus.",
  seconds=40)
ms_check("abce", _opts_fb, "D")

Z(NEU, "Nervous system divisions", "Intermediate", "assertion_reason",
  ar("A canal called the cerebral aqueduct passes through the midbrain.",
     "The dorsal portion of the midbrain consists mainly of four round swellings called the corpora quadrigemina."),
  ASSERTION_REASON, "B",
  "The midbrain",
  "NCERT: the midbrain is located between the thalamus/hypothalamus of the forebrain and the pons of the hindbrain. A "
  "canal called the cerebral aqueduct passes through it, and its dorsal portion consists mainly of four round "
  "swellings (lobes) called the corpora quadrigemina. Both are true, but the swellings on its dorsal side do not "
  "explain why a canal runs through it – they are two separate features of the midbrain.",
  ["A → true", "R → true", "R is a different feature of the midbrain → not the explanation"],
  R_NEU("central neural system – midbrain"),
  why_others_wrong="A treats an unrelated feature as the cause; C and D reject statements NCERT makes about the "
                   "midbrain.",
  seconds=30)

Z(NEU, "Neuron and nerves", "Intermediate", "direct",
  "Impulses pass along an unmyelinated nerve fibre of the autonomic neural system to the smooth muscle of the gut. "
  "Which statement about this fibre is correct?",
  ["It is enclosed by a Schwann cell that does not form a myelin sheath around the axon",
   "It bears nodes of Ranvier between adjacent myelin sheaths",
   "It belongs to the somatic neural system, which supplies smooth muscles",
   "It is a part of the central neural system"], "A",
  "Unmyelinated fibres",
  "NCERT: an unmyelinated nerve fibre is enclosed by a Schwann cell that does not form a myelin sheath around the "
  "axon, and it is commonly found in the autonomous and somatic neural systems. Nodes of Ranvier are gaps between "
  "adjacent myelin sheaths, so they occur on myelinated fibres. The autonomic neural system, part of the PNS, relays "
  "impulses from the CNS to the involuntary organs and smooth muscles.",
  ["Unmyelinated → Schwann cell, no myelin sheath", "No myelin → no nodes of Ranvier",
   "Smooth muscle → autonomic (PNS)"],
  R_NEU("neuron as structural and functional unit; human neural system"),
  why_others_wrong="B needs myelin sheaths; C is wrong because the somatic system supplies skeletal muscles; D is "
                   "wrong because nerve fibres to the gut belong to the PNS.",
  seconds=40)

_opts_path = ["(a), (b) and (d) only", "(a), (b), (c) and (e) only", "(b), (c), (d) and (e) only",
              "(a), (c) and (d) only"]
Z(NEU, "Nervous system divisions", "Advanced", "multi_statement",
  ms("Impulses from the skin of the hand reach the brain, and the brain then sends a command that makes a skeletal "
     "muscle of the hand contract. Which of the following statements about this pathway are correct?",
     ["Impulses from the skin travel to the CNS along afferent nerve fibres.",
      "The information is processed in the CNS, the site of information processing and control.",
      "The command is carried to the muscle by efferent fibres of the somatic neural system.",
      "The autonomic neural system relays the command to the skeletal muscle.",
      "Wherever the impulse passes from one neuron to the next across a chemical synapse, neurotransmitters carry it "
      "across the synaptic cleft."]),
  _opts_path, "B",
  "Afferent, central and efferent links",
  "NCERT: afferent fibres transmit impulses from tissues/organs to the CNS; the CNS is the site of information "
  "processing and control; efferent fibres carry regulatory impulses from the CNS to the peripheral tissues, and the "
  "somatic neural system relays impulses from the CNS to the skeletal muscles. The autonomic neural system serves the "
  "involuntary organs and smooth muscles. At a chemical synapse, neurotransmitters released into the synaptic cleft "
  "bind receptors on the post-synaptic membrane.",
  ["(a) true", "(b) true", "(c) true", "(d) false – skeletal muscle is served by the somatic system", "(e) true"],
  R_NEU("human neural system; transmission of impulses"),
  why_others_wrong="A, C and D include (d); A and D also leave out true statements.",
  seconds=55)
ms_check("abce", _opts_path, "B")

_opts_br = ["(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only",
            "(a), (b), (c) and (e) only"]
Z(NEU, "Nervous system divisions", "Advanced", "multi_statement",
  ms("Which of the following statements about the human brain are correct?",
     ["The association areas of the cerebral cortex are responsible for complex functions like intersensory "
      "associations, memory and communication.",
      "The inner part of the cerebral hemisphere looks white because the fibres of its tracts are covered with a "
      "myelin sheath.",
      "A tract of nerve fibres called the corpus callosum connects the two cerebral hemispheres.",
      "The thalamus is a part of the midbrain.",
      "The medulla oblongata of the brain is connected to the spinal cord."]),
  _opts_br, "D",
  "Organisation of the brain",
  "NCERT: the large association areas of the cortex are responsible for intersensory associations, memory and "
  "communication. Fibres of the tracts are covered with myelin, which gives the inner part of the cerebral hemisphere "
  "an opaque white appearance (white matter). The two hemispheres are connected by the corpus callosum. The cerebrum "
  "wraps around the thalamus, a forebrain structure. The medulla of the brain is connected to the spinal cord.",
  ["(a) true", "(b) true", "(c) true", "(d) false – the thalamus is in the forebrain", "(e) true"],
  R_NEU("central neural system – forebrain and hindbrain"),
  why_others_wrong="A, B and C all include (d), which places the thalamus in the midbrain.",
  seconds=50)
ms_check("abce", _opts_br, "D")

Z(NEU, "Nervous system divisions", "Advanced", "statement_pair",
  sp("In the visceral nervous system, impulses travel from the CNS to the viscera and also from the viscera to the "
     "CNS.",
     "The visceral nervous system is a part of the central neural system."),
  STATEMENT_PAIR, "C",
  "The visceral nervous system",
  "NCERT: the visceral nervous system is the part of the peripheral nervous system that comprises the whole complex "
  "of nerves, fibres, ganglia and plexuses by which impulses travel from the CNS to the viscera and from the viscera "
  "to the CNS. The CNS itself is only the brain and the spinal cord.",
  ["Statement I → true (two-way traffic)", "Statement II → false: it is part of the PNS"],
  R_NEU("human neural system"),
  why_others_wrong="A and D place the visceral system in the CNS; B rejects the two-way traffic NCERT describes.",
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
           "notes": "BATCH_008 package ZOO_008_p1: 117 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "questions already asked in BATCH_000-BATCH_007 (many items are application, comparison or "
                    "scenario questions on NCERT mechanisms); every numerical answer re-derived by "
                    "tools/batch_008/ZOO_008_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
