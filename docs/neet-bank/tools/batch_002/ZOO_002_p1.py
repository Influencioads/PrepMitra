"""Writes batches/parts/BATCH_002_ZOO_p1.json: package ZOO_002_p1 of BATCH_002 (Zoology, 123 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination.
IDs NEET_ZOO_000251 .. NEET_ZOO_000373. Every numerical answer is re-derived below before the file is written, and the
plan quota, ID range, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11 Biology
textbook; nothing from the parts NMC 2026 drops (reflex action, sense organs, digestion). Facts already tested in
BATCH_001 (see `merge_batch.py stems 002 ZOO_002_p1`) are not tested again.

    python docs/neet-bank/tools/batch_002/ZOO_002_p1.py
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
PACKAGE = "ZOO_002_p1"
FIRST_ID, LAST_ID = 251, 373
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
# Biomolecules: peptide bonds in a protein of two polypeptide chains of 21 and 30 amino acids.
PEPTIDE = (21 - 1) + (30 - 1)
assert PEPTIDE == 49
assert 21 + 30 == 51 and 21 + 30 - 1 == 50 and PEPTIDE - 1 == 48     # distractors

# Breathing: air moved per minute = tidal volume x breathing rate.
MINUTE_VOL = 500 * 14
assert MINUTE_VOL == 7000
assert (500 + 1100) * 14 == 22400                                     # distractor: ERV added to each breath
assert round(500 / 14, 1) == 35.7 and 500 + 14 == 514                  # distractors: divided; added

# Breathing: partial-pressure gradients (mm Hg). O2 alveoli -> deoxygenated blood; CO2 deoxygenated blood -> alveoli.
PO2_ALV, PO2_DEOXY, PCO2_ALV, PCO2_DEOXY, PO2_OXY = 104, 40, 40, 45, 95
assert (PO2_ALV - PO2_DEOXY, PCO2_DEOXY - PCO2_ALV) == (64, 5)
assert PO2_OXY - PO2_DEOXY == 55                                       # distractor: oxygenated blood taken for alveoli
assert F(PO2_ALV - PO2_DEOXY, PCO2_DEOXY - PCO2_ALV) == F(64, 5)        # 12.8 : 1

# Body fluids: heart rate from QRS complexes; 18 complexes in 15 s.
HR = F(18 * 60, 15)
assert HR == 72
assert F(15 * 60, 18) == 50 and 18 * 15 == 270 and 18 * 2 == 36       # distractors: inverted, multiplied, x2

# Excretion: descending limb permeable to water, almost impermeable to electrolytes -> solute amount conserved,
# so volume x osmolarity stays constant: 20 mL at 300 mOsmol/L -> V at 1200 mOsmol/L.
DLV = F(20 * 300, 1200)
assert DLV == 5
assert 20 * F(1200, 300) == 80 and 20 - DLV == 15                      # distractors: inverted ratio; water lost

# Locomotion: axial skeleton = skull 22 + hyoid 1 + ear ossicles 2 x 3 + vertebrae 26 + sternum 1 + ribs 12 x 2.
AXIAL = 22 + 1 + 2 * 3 + 26 + 1 + 12 * 2
assert AXIAL == 80
assert 22 + 1 + 26 + 1 + 24 == 74                                      # distractor: ear ossicles left out
assert 22 + 1 + 6 + 26 + 1 + 12 == 68                                  # distractor: 12 ribs, not 12 pairs
assert 22 + 1 + 3 + 26 + 1 + 24 == 77                                  # distractor: ossicles of one ear only


# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Basis of classification", "Basic", "direct",
  "An animal in which any plane passing through the central axis of the body divides it into two identical halves "
  "shows radial symmetry. Which of the following groups shows this body plan?",
  ["Annelids", "Arthropods", "Coelenterates", "Platyhelminthes"], "C",
  "Radial symmetry",
  "NCERT: when any plane passing through the central axis divides the organism into two identical halves, it is "
  "radial symmetry. Coelenterates, ctenophores and (adult) echinoderms have this body plan. Annelids, arthropods "
  "and flatworms are bilaterally symmetrical: only one plane gives identical left and right halves.",
  ["Radial symmetry → coelenterates, ctenophores, adult echinoderms",
   "Bilateral symmetry → annelids, arthropods, flatworms and others"],
  R_AK("basis of classification: symmetry"),
  why_others_wrong="Annelids, arthropods and flatworms can be divided into identical halves along one plane only "
                   "(bilateral symmetry).",
  seconds=25)

Z(AK, "Basis of classification", "Basic", "direct",
  "In which of the following animals is the body divided externally and internally into segments with a serial "
  "repetition of at least some organs (metamerism)?",
  ["Pheretima", "Ascaris", "Hydra", "Pila"], "A",
  "Metameric segmentation",
  "NCERT gives the earthworm (Pheretima) as the example: its body is divided externally and internally into "
  "segments with serial repetition of at least some organs. This pattern is metameric segmentation and the "
  "phenomenon is metamerism.",
  ["Metamerism → true segmentation, external and internal", "Example → earthworm (Pheretima), an annelid"],
  R_AK("basis of classification: segmentation"),
  why_others_wrong="Ascaris (roundworm), Hydra (coelenterate) and Pila (mollusc, unsegmented body) do not show "
                   "metamerism.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "assertion_reason",
  ar("In Platyhelminthes, specialised cells called flame cells help in osmoregulation and excretion.",
     "Platyhelminthes are mostly endoparasites found in animals, including human beings."),
  ASSERTION_REASON, "B",
  "Features of flatworms",
  "Both statements are NCERT facts about Platyhelminthes. Flame cells are the osmoregulatory and excretory cells. "
  "The endoparasitic habit is a separate feature: being parasites does not explain why flatworms have flame cells, "
  "so R is not the explanation of A.",
  ["A: flame cells → osmoregulation and excretion → true",
   "R: mostly endoparasites → true", "Habitat does not explain the excretory cell type → R does not explain A"],
  R_AK("Phylum Platyhelminthes"),
  why_others_wrong="Both statements are true, so options C and D are out; option A fails because the parasitic "
                   "habit is not the reason for flame cells.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "In some cnidarians, polyps produce medusae asexually and medusae form the polyps sexually (metagenesis). An "
  "example of such a cnidarian is:",
  ["Pleurobrachia", "Fasciola", "Spongilla", "Obelia"], "D",
  "Metagenesis in Coelenterata",
  "Cnidarians show two basic body forms, polyp and medusa. Those that exist in both forms show alternation of "
  "generation (metagenesis): polyps produce medusae asexually and medusae form polyps sexually, e.g. Obelia.",
  ["Polyp → medusa (asexual)", "Medusa → polyp (sexual)", "Both forms in one life cycle → Obelia"],
  R_AK("Phylum Coelenterata (Cnidaria)"),
  why_others_wrong="Pleurobrachia is a ctenophore, Fasciola a flatworm and Spongilla a sponge; none has polyp and "
                   "medusa forms.",
  seconds=25)

Z(AK, "Chordate classes", "Basic", "direct",
  "Which of the following is a bony fish (class Osteichthyes)?",
  ["Scoliodon", "Labeo", "Pristis", "Trygon"], "B",
  "Examples of bony and cartilaginous fishes",
  "Labeo (Rohu) is a freshwater bony fish. Scoliodon (dog fish), Pristis (saw fish) and Trygon (sting ray) are "
  "cartilaginous fishes (Chondrichthyes).",
  ["Osteichthyes → Labeo, Catla, Clarias, Exocoetus, Hippocampus, Betta, Pterophyllum",
   "Chondrichthyes → Scoliodon, Pristis, Carcharodon, Trygon"],
  R_AK("Class Osteichthyes; Class Chondrichthyes"),
  why_others_wrong="Scoliodon, Pristis and Trygon have a cartilaginous endoskeleton.",
  seconds=25)

Z(AK, "Chordate classes", "Basic", "statement_pair",
  sp("Hyla is a limbless amphibian.", "Salamandra is the salamander, an amphibian."),
  STATEMENT_PAIR, "D",
  "Examples of Amphibia",
  "NCERT examples: Bufo (toad), Rana (frog), Hyla (tree frog), Salamandra (salamander) and Ichthyophis (limbless "
  "amphibian). Hyla is the tree frog, not limbless, so Statement I is false. Statement II is true.",
  ["Limbless amphibian → Ichthyophis, not Hyla → I false", "Salamandra → salamander → II true"],
  R_AK("Class Amphibia"), seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("In sponges, fertilisation is internal and development is indirect, with a larval stage that is "
     "morphologically distinct from the adult.",
     "In sponges, choanocytes or collar cells line the spongocoel and the canals."),
  STATEMENT_PAIR, "A",
  "Reproduction and canal system of Porifera",
  "Sponges are hermaphrodite; fertilisation is internal and development is indirect, with a larval stage distinct "
  "from the adult (Statement I true). Water enters through ostia into the spongocoel and leaves through the "
  "osculum; choanocytes (collar cells) line the spongocoel and the canals (Statement II true).",
  ["Fertilisation internal, development indirect → I true", "Choanocytes line spongocoel and canals → II true"],
  R_AK("Phylum Porifera"), seconds=40)

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("Ctenophores are exclusively marine animals.", "Ctenophores reproduce only by sexual means."),
  ASSERTION_REASON, "B",
  "Features of Ctenophora",
  "NCERT: ctenophores (sea walnuts, comb jellies) are exclusively marine, radially symmetrical, diploblastic "
  "animals with tissue level organisation. Reproduction takes place only by sexual means, with external "
  "fertilisation and indirect development. Both are true, but the mode of reproduction has nothing to do with the "
  "marine habitat.",
  ["A: exclusively marine → true", "R: only sexual reproduction → true",
   "Mode of reproduction does not explain habitat → R is not the explanation"],
  R_AK("Phylum Ctenophora"),
  why_others_wrong="A needs both statements to be linked as cause and effect, which they are not; C and D need one "
                   "statement to be false.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("animal", "phylum"), ["Aurelia", "Fasciola", "Wuchereria", "Nereis"],
     ["Annelida", "Aschelminthes", "Coelenterata", "Platyhelminthes"]),
  match_options(M("III", "IV", "II", "I"),
                [M("III", "II", "IV", "I"), M("I", "IV", "II", "III"), M("III", "IV", "I", "II")], at="C"),
  "C",
  "Examples of non-chordate phyla",
  "Aurelia (jelly fish) is a coelenterate, Fasciola (liver fluke) a flatworm, Wuchereria (filaria worm) an "
  "aschelminth (roundworm) and Nereis an aquatic annelid.",
  ["Aurelia → Coelenterata (III)", "Fasciola → Platyhelminthes (IV)", "Wuchereria → Aschelminthes (II)",
   "Nereis → Annelida (I)"],
  R_AK("Phyla Coelenterata, Platyhelminthes, Aschelminthes and Annelida"),
  why_others_wrong="The other codes swap the two worm phyla (flatworm and roundworm) or place Nereis with the "
                   "coelenterates.",
  seconds=45)

_o = ["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c) and (e) only", "(a), (b), (c) and (e) only"]
ms_check("abce", _o, "D")
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements about Annelida are correct?",
     ["Aquatic annelids such as Nereis have lateral appendages, parapodia, which help in swimming.",
      "Annelids have a closed circulatory system.",
      "Nephridia help in osmoregulation and excretion.",
      "Nereis is monoecious.",
      "Earthworms and leeches are monoecious."]),
  _o, "D",
  "Features of annelids",
  "Nereis has parapodia for swimming; annelids have a closed circulatory system; nephridia help in osmoregulation "
  "and excretion. Nereis, an aquatic form, is dioecious, whereas earthworms and leeches are monoecious.",
  ["(a) True", "(b) True", "(c) True", "(d) False: Nereis is dioecious", "(e) True"],
  R_AK("Phylum Annelida"),
  why_others_wrong="Options A and C leave out true statements; option B includes the false statement (d).",
  seconds=55)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("In molluscs, the space between the visceral hump and the mantle is the mantle cavity, in which feather-like "
     "gills are present.",
     "Molluscs are usually monoecious and viviparous."),
  STATEMENT_PAIR, "C",
  "Features of Mollusca",
  "A soft, spongy layer of skin forms a mantle over the visceral hump; the space between hump and mantle is the "
  "mantle cavity, with feather-like gills that have respiratory and excretory functions (Statement I true). "
  "Molluscs are usually dioecious and oviparous with indirect development (Statement II false).",
  ["Mantle cavity with feather-like gills → I true", "Usually dioecious and oviparous → II false"],
  R_AK("Phylum Mollusca"), seconds=40)

Z(AK, "Basis of classification", "Intermediate", "direct",
  "Which of the following correctly compares the heart and the central nervous system of chordates with those of "
  "non-chordates?",
  ["Chordates: heart ventral, CNS dorsal, hollow and single; non-chordates: heart dorsal (if present), CNS "
   "ventral, solid and double",
   "Chordates: heart dorsal, CNS ventral, solid and double; non-chordates: heart ventral, CNS dorsal, hollow and "
   "single",
   "Chordates: heart ventral, CNS ventral, hollow and single; non-chordates: heart dorsal, CNS dorsal, solid and "
   "double",
   "Chordates: heart dorsal, CNS dorsal, hollow and single; non-chordates: heart ventral (if present), CNS "
   "ventral, solid and double"], "A",
  "Chordates versus non-chordates",
  "NCERT's comparison table: in chordates the CNS is dorsal, hollow and single and the heart is ventral; in "
  "non-chordates the CNS is ventral, solid and double and the heart, if present, is dorsal.",
  ["CNS: chordates dorsal-hollow-single; non-chordates ventral-solid-double",
   "Heart: chordates ventral; non-chordates dorsal (if present)"],
  R_AK("Phylum Chordata: comparison of chordates and non-chordates"),
  why_others_wrong="B reverses both features; C puts the chordate CNS ventrally; D places the chordate heart "
                   "dorsally.",
  seconds=45)

Z(AK, "Chordate classes", "Intermediate", "direct",
  "The heart of reptiles is usually three-chambered. In which of the following reptiles is it four-chambered?",
  ["Chameleon", "Naja", "Crocodilus", "Vipera"], "C",
  "Heart in Reptilia",
  "NCERT: the reptilian heart is usually three-chambered, but four-chambered in crocodiles. Chameleon (tree lizard), "
  "Naja (cobra) and Vipera (viper) have three-chambered hearts.",
  ["Reptiles → usually 3 chambers", "Exception → crocodiles (Crocodilus) have 4 chambers"],
  R_AK("Class Reptilia"),
  why_others_wrong="Lizards and snakes have the usual three-chambered reptilian heart.",
  seconds=30)

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("In birds, the long bones are hollow with air cavities (pneumatic).",
     "The digestive tract of birds has additional chambers, the crop and the gizzard."),
  STATEMENT_PAIR, "A",
  "Features of Aves",
  "Birds have a fully ossified endoskeleton whose long bones are hollow with air cavities (pneumatic). Their "
  "digestive tract has two additional chambers, the crop and the gizzard. Both statements are true.",
  ["Pneumatic long bones → I true", "Crop and gizzard → II true"],
  R_AK("Class Aves"), seconds=30)

_o = ["(a), (c) and (d) only", "(a) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
ms_check("ad", _o, "B")
Z(AK, "Basis of classification", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["An incomplete digestive system has a single opening to the outside that serves as both mouth and anus, "
      "as in Platyhelminthes.",
      "Sponges are mostly radially symmetrical.",
      "The notochord is a mesodermally derived rod-like structure formed on the ventral side during embryonic "
      "development.",
      "Annelids, molluscs, arthropods, echinoderms, hemichordates and chordates are coelomates.",
      "Ctenophores show the organ-system level of organisation."]),
  _o, "B",
  "Basis of classification",
  "(a) True: NCERT's example of an incomplete gut is Platyhelminthes. (b) False: sponges are mostly asymmetrical. "
  "(c) False: the notochord forms on the dorsal side. (d) True: these phyla have a body cavity lined by mesoderm. "
  "(e) False: ctenophores show the tissue level of organisation.",
  ["(a) True", "(b) False: mostly asymmetrical", "(c) False: dorsal, not ventral", "(d) True",
   "(e) False: tissue level"],
  R_AK("basis of classification; Phylum Ctenophora; Phylum Porifera"),
  why_others_wrong="Each other option includes at least one of the false statements (b), (c) or (e).",
  seconds=70)

Z(AK, "Chordate classes", "Advanced", "assertion_reason",
  ar("Bony fishes have four pairs of gills, which are covered by an operculum on each side.",
     "Bony fishes have an air bladder, which regulates buoyancy."),
  ASSERTION_REASON, "B",
  "Features of Osteichthyes",
  "Both are NCERT features of Osteichthyes. The operculum covering the four pairs of gills is a respiratory "
  "feature; the air bladder is a buoyancy organ. One does not explain the other.",
  ["A: four pairs of gills + operculum → true", "R: air bladder regulates buoyancy → true",
   "Buoyancy organ ≠ reason for a gill cover → R does not explain A"],
  R_AK("Class Osteichthyes"),
  why_others_wrong="A wrongly links two independent features; C and D wrongly call one of the true statements "
                   "false.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "match_list",
  ml(("coelenterate", "common name"), ["Physalia", "Adamsia", "Pennatula", "Meandrina"],
     ["Sea-pen", "Brain coral", "Portuguese man-of-war", "Sea anemone"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("III", "I", "IV", "II")], at="D"),
  "D",
  "Examples of Coelenterata",
  "NCERT lists Physalia (Portuguese man-of-war), Adamsia (sea anemone), Pennatula (sea-pen), Gorgonia (sea-fan) "
  "and Meandrina (brain coral).",
  ["Physalia → Portuguese man-of-war (III)", "Adamsia → sea anemone (IV)", "Pennatula → sea-pen (I)",
   "Meandrina → brain coral (II)"],
  R_AK("Phylum Coelenterata (Cnidaria)"),
  why_others_wrong="The other codes swap Physalia with Adamsia, or Pennatula with Meandrina, or Adamsia with "
                   "Pennatula.",
  seconds=50)

Z(AK, "Chordate classes", "Advanced", "direct",
  "Which of the following fishes is NOT correctly matched with its common name?",
  ["Clarias – Fighting fish", "Pristis – Saw fish", "Exocoetus – Flying fish", "Hippocampus – Sea horse"], "A",
  "Common names of fishes",
  "Clarias is Magur, a freshwater bony fish. The fighting fish is Betta, an aquarium fish. The other three pairs are "
  "correct as given in NCERT.",
  ["Clarias → Magur", "Betta → fighting fish", "Pristis → saw fish; Exocoetus → flying fish; Hippocampus → sea horse"],
  R_AK("Class Chondrichthyes; Class Osteichthyes"),
  why_others_wrong="Options B, C and D are correct pairs, so they are not the answer.",
  seconds=40)

_o = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only", "(a), (c), (d) and (e) only"]
ms_check("abde", _o, "C")
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following statements about Amphibia are correct?",
     ["The heart is three-chambered, with two auricles and one ventricle.",
      "They are cold-blooded animals.",
      "Fertilisation is internal.",
      "The alimentary canal, urinary and reproductive tracts open into a common chamber called the cloaca.",
      "The eyes have eyelids, and a tympanum represents the ear."]),
  _o, "C",
  "Features of amphibians",
  "Amphibians have a three-chambered heart (two auricles, one ventricle), are cold-blooded, have a cloaca, and have "
  "eyelids and a tympanum. Their fertilisation is external, and they are oviparous with indirect development.",
  ["(a) True", "(b) True", "(c) False: fertilisation is external", "(d) True", "(e) True"],
  R_AK("Class Amphibia"),
  why_others_wrong="A leaves out (e); B and D include the false statement (c).",
  seconds=60)

Z(AK, "Chordate classes", "Advanced", "statement_pair",
  sp("In cartilaginous fishes, the pelvic fins of males bear claspers, fertilisation is internal and many species "
     "are viviparous.",
     "The heart of cartilaginous fishes is three-chambered."),
  STATEMENT_PAIR, "C",
  "Reproduction and heart in Chondrichthyes",
  "In Chondrichthyes sexes are separate, males have claspers on the pelvic fins, fertilisation is internal and "
  "many are viviparous (Statement I true). The heart is two-chambered, with one auricle and one ventricle "
  "(Statement II false).",
  ["Claspers, internal fertilisation, many viviparous → I true",
   "Heart two-chambered (one auricle, one ventricle) → II false"],
  R_AK("Class Chondrichthyes"), seconds=40)


# ================================================================ Structural Organisation in Animals (B5 I6 A5)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Animal tissues", "Basic", "direct",
  "The cells of neural tissue that protect and support neurons, and make up more than one-half the volume of "
  "neural tissue in our body, are the:",
  ["Fibroblasts", "Neuroglial cells", "Mast cells", "Chondrocytes"], "B",
  "Neural tissue",
  "Neural tissue has neurons, the excitable units, and neuroglial cells, which form the rest of the neural system, "
  "protect and support the neurons, and make up more than half the volume of neural tissue.",
  ["Neurons → excitable units", "Neuroglia → protect and support neurons; > 1/2 the volume of neural tissue"],
  R_SOA("animal tissues: neural tissue"),
  why_others_wrong="Fibroblasts and mast cells are connective tissue cells; chondrocytes are cartilage cells.",
  seconds=25)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Which of the following is a specialised connective tissue?",
  ["Areolar tissue", "Adipose tissue", "Dense regular connective tissue", "Blood"], "D",
  "Types of connective tissue",
  "NCERT groups connective tissues into loose, dense and specialised types. Cartilage, bone and blood are the "
  "specialised connective tissues; blood is a fluid connective tissue with plasma, RBCs, WBCs and platelets.",
  ["Loose → areolar, adipose", "Dense → regular (tendons, ligaments), irregular (skin)",
   "Specialised → cartilage, bone, blood"],
  R_SOA("animal tissues: connective tissue"),
  why_others_wrong="Areolar and adipose tissue are loose connective tissues; tendons are dense regular connective "
                   "tissue.",
  seconds=25)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "During peak summer, frogs take shelter in deep burrows to protect themselves from extreme heat. This is called:",
  ["Aestivation", "Hibernation", "Metamorphosis", "Camouflage"], "A",
  "Summer and winter sleep in frogs",
  "Frogs take shelter in deep burrows during peak summer and winter. The summer sleep is aestivation and the "
  "winter sleep is hibernation.",
  ["Summer sleep → aestivation", "Winter sleep → hibernation"],
  R_SOA("frog: habit and habitat"),
  why_others_wrong="Hibernation is the winter sleep; metamorphosis is the change from tadpole to adult; camouflage "
                   "is colour change to hide from enemies.",
  seconds=20)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Areolar tissue, present beneath the skin, often serves as a support framework for epithelium.",
     "In dense regular connective tissue, the collagen fibres are oriented differently, and this tissue is present "
     "in the skin."),
  STATEMENT_PAIR, "C",
  "Loose and dense connective tissue",
  "Areolar tissue (loose connective tissue) lies beneath the skin, serves as a support framework for epithelium "
  "and contains fibroblasts, macrophages and mast cells (Statement I true). Fibres oriented differently, as in the "
  "skin, describe dense irregular connective tissue; in dense regular tissue the collagen fibres lie in rows "
  "between many parallel bundles of fibres (Statement II false).",
  ["Areolar tissue → support framework for epithelium → I true",
   "Differently oriented fibres, skin → dense irregular, not regular → II false"],
  R_SOA("animal tissues: connective tissue"), seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "How many ova can a mature female frog lay at a time?",
  ["About 25 to 30", "About 250 to 300", "About 2500 to 3000", "About 25,000 to 30,000"], "C",
  "Reproduction in the frog",
  "NCERT: a mature female frog can lay 2500 to 3000 ova at a time. Fertilisation is external and takes place in "
  "water.",
  ["Female frog → 2500–3000 ova at a time", "External fertilisation in water"],
  R_SOA("frog: reproductive system"),
  why_others_wrong="The other figures are off by factors of ten from the NCERT value.",
  seconds=20)

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("tissue", "location or role"),
     ["Dense irregular connective tissue", "Cartilage", "Bone marrow", "Areolar tissue"],
     ["Beneath the skin", "Site of production of blood cells", "Between adjacent bones of the vertebral column",
      "Skin"]),
  match_options(M("IV", "III", "II", "I"),
                [M("I", "III", "II", "IV"), M("IV", "II", "III", "I"), M("III", "IV", "II", "I")], at="B"),
  "B",
  "Connective tissues and where they occur",
  "Dense irregular connective tissue, with differently oriented fibres, is present in the skin. Cartilage is "
  "present between adjacent bones of the vertebral column (and in the tip of the nose, outer ear joints, limbs "
  "and hands in adults). The bone marrow in some bones is the site of production of blood cells. Areolar tissue is "
  "present beneath the skin.",
  ["Dense irregular → skin (IV)", "Cartilage → between vertebrae (III)", "Bone marrow → blood cells (II)",
   "Areolar → beneath the skin (I)"],
  R_SOA("animal tissues: connective tissue"),
  why_others_wrong="The other codes confuse 'skin' with 'beneath the skin', or swap cartilage and bone marrow.",
  seconds=45)

Z(SOA, "Animal tissues", "Intermediate", "assertion_reason",
  ar("Smooth muscles are called involuntary muscles.",
     "The functioning of smooth muscles cannot be directly controlled; we usually cannot make them contract merely "
     "by thinking about it."),
  ASSERTION_REASON, "A",
  "Smooth muscle",
  "NCERT: smooth muscles are 'involuntary' as their functioning cannot be directly controlled; we usually are not "
  "able to make them contract merely by thinking about it, as we can with skeletal muscles. R gives exactly the "
  "reason for the name in A.",
  ["A: smooth muscle = involuntary → true", "R: not under direct control → true", "R is why they are called "
   "involuntary → R explains A"],
  R_SOA("animal tissues: muscle tissue"),
  why_others_wrong="B denies a link that NCERT states directly; C and D wrongly call a true statement false.",
  seconds=30)

_o = ["(a), (c) and (d) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]
ms_check("acd", _o, "A")
Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the external features of the frog are correct?",
     ["The body is divisible into head and trunk.",
      "The skin is dry and rough because of keratinised scales.",
      "The eyes are bulged and covered by a nictitating membrane that protects them while in water.",
      "The feet have webbed digits that help in swimming.",
      "The dorsal side is uniformly pale yellow and the ventral side is olive green with dark irregular spots."]),
  _o, "A",
  "Morphology of the frog",
  "The frog's body has a head and a trunk (no neck or tail). The skin is smooth and slippery because of mucus, "
  "not dry and scaly. The bulged eyes have a nictitating membrane, and the webbed hind feet help in swimming. The "
  "colours in (e) are reversed: the dorsal side is olive green with dark irregular spots and the ventral side is "
  "uniformly pale yellow.",
  ["(a) True", "(b) False: smooth and slippery due to mucus", "(c) True", "(d) True",
   "(e) False: dorsal olive green with spots, ventral pale yellow"],
  R_SOA("frog: morphology"),
  why_others_wrong="B and C include (b); D includes (e).",
  seconds=55)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("The heart of the frog has three chambers, two atria and one ventricle, and is covered by a membrane called "
     "the pericardium.",
     "In the frog, a triangular structure called the sinus venosus joins the right atrium and receives blood "
     "through the vena cava."),
  STATEMENT_PAIR, "A",
  "Circulatory system of the frog",
  "The frog's heart, in the upper part of the body cavity, has two atria and one ventricle and is covered by the "
  "pericardium. A triangular sinus venosus joins the right atrium and receives blood through the major veins "
  "called vena cava. Both statements are true.",
  ["Three chambers (2 atria + 1 ventricle), pericardium → I true",
   "Sinus venosus joins right atrium, receives vena cava → II true"],
  R_SOA("frog: anatomy, circulatory system"), seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "The main nitrogenous waste excreted by the frog shows that it is:",
  ["Ammonotelic", "Uricotelic", "Aminotelic", "Ureotelic"], "D",
  "Excretion in the frog",
  "The frog's excretory system (kidneys, ureters, cloaca and urinary bladder) eliminates nitrogenous waste mainly "
  "as urea, so the frog is a ureotelic animal.",
  ["Frog excretes urea → ureotelic"],
  R_SOA("frog: excretory system"),
  why_others_wrong="Ammonotelic animals excrete ammonia and uricotelic animals uric acid; 'aminotelic' is not the "
                   "NCERT term for the frog.",
  seconds=25)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "In the frog, the medulla oblongata passes out of the cranium and continues into the spinal cord through the:",
  ["Neural canal of the atlas only", "Foramen magnum", "Cerebral aqueduct", "Cloaca"], "B",
  "Neural system of the frog",
  "The frog's brain is enclosed in a bony brain box (cranium). The hind-brain has the cerebellum and medulla "
  "oblongata; the medulla oblongata passes out through the foramen magnum and continues into the spinal cord, "
  "which is enclosed in the vertebral column.",
  ["Brain in cranium", "Medulla oblongata → foramen magnum → spinal cord in the vertebral column"],
  R_SOA("frog: nervous system"),
  why_others_wrong="The cerebral aqueduct is a canal inside the midbrain; the cloaca is part of the gut; option A "
                   "names a vertebral canal, not the opening of the cranium.",
  seconds=30)

_o = ["(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c) and (e) only", "(a), (b), (c) and (e) only"]
ms_check("abce", _o, "D")
Z(SOA, "Animal tissues", "Advanced", "multi_statement",
  ms("Which of the following statements about specialised connective tissues are correct?",
     ["Most of the cartilages in vertebrate embryos are replaced by bones in adults.",
      "Long bones of the legs serve weight-bearing functions.",
      "Bone cells (osteocytes) are present in spaces called lacunae.",
      "Blood is a dense connective tissue.",
      "Limb bones interact with the skeletal muscles attached to them to bring about movements."]),
  _o, "D",
  "Cartilage, bone and blood",
  "NCERT: most cartilages of vertebrate embryos are replaced by bones in adults; limb bones such as the long bones "
  "of the legs bear weight and, with the skeletal muscles attached to them, bring about movements; osteocytes lie "
  "in lacunae. Blood is a fluid connective tissue, not a dense one.",
  ["(a) True", "(b) True", "(c) True", "(d) False: blood is a fluid (specialised) connective tissue", "(e) True"],
  R_SOA("animal tissues: specialised connective tissue"),
  why_others_wrong="A and B include (d); C leaves out the true statement (b).",
  seconds=60)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "assertion_reason",
  ar("In the frog, a tadpole undergoes metamorphosis to form the adult.",
     "In the frog, fertilisation is internal and takes place in the female's body."),
  ASSERTION_REASON, "C",
  "Development in the frog",
  "Fertilisation in the frog is external and takes place in water. Development involves a larval stage, the "
  "tadpole, which undergoes metamorphosis to form the adult. A is true; R is false.",
  ["A: tadpole → metamorphosis → adult → true", "R: fertilisation internal → false (external, in water)"],
  R_SOA("frog: reproductive system"),
  why_others_wrong="A and B need R to be true; D wrongly calls A false.",
  seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "statement_pair",
  sp("In the frog, the cloaca receives only faecal matter, while urine and sperms leave the body through separate "
     "openings.",
     "On land, the buccal cavity, skin and lungs act as the respiratory organs of the frog."),
  STATEMENT_PAIR, "D",
  "Cloaca and respiration in the frog",
  "The cloaca is a small median chamber used to pass faecal matter, urine and sperms to the exterior, so Statement "
  "I is false. In water the skin is the respiratory organ (cutaneous respiration); on land the buccal cavity, skin "
  "and lungs act as respiratory organs, so Statement II is true.",
  ["Cloaca passes faeces, urine and sperms → I false", "On land: buccal cavity, skin, lungs → II true"],
  R_SOA("frog: digestive, respiratory and excretory systems"), seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "match_list",
  ml(("structure in the frog", "feature"), ["Sinus venosus", "Conus arteriosus", "Hepatic portal system", "Tympanum"],
     ["Receives sound signals", "Special venous connection between the liver and the intestine",
      "Triangular structure joining the right atrium", "Sac-like structure on the ventral side of the heart into "
      "which the ventricle opens"]),
  match_options(M("III", "IV", "II", "I"),
                [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"), M("III", "II", "IV", "I")], at="A"),
  "A",
  "Frog anatomy",
  "The sinus venosus is a triangular structure joining the right atrium; the ventricle opens into the sac-like "
  "conus arteriosus on the ventral side; the hepatic portal system is the special venous connection between liver "
  "and intestine; the tympanum receives sound signals.",
  ["Sinus venosus → III", "Conus arteriosus → IV", "Hepatic portal system → II", "Tympanum → I"],
  R_SOA("frog: morphology; circulatory system"),
  why_others_wrong="The other codes swap the two heart structures, or the portal system with the tympanum, or the "
                   "conus with the portal system.",
  seconds=50)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "direct",
  "Which of the following statements about the anatomy of the frog is INCORRECT?",
  ["The liver secretes bile, which is stored in the gall bladder.",
   "The ovaries are situated near the kidneys but have no functional connection with them.",
   "The kidneys are compact, dark red, bean-like structures situated a little anteriorly in the body cavity.",
   "Ten pairs of cranial nerves arise from the brain."], "C",
  "Anatomy of the frog",
  "NCERT: the frog's kidneys are compact, dark red and bean-like and are situated a little posteriorly in the body "
  "cavity, on both sides of the vertebral column. The other statements are NCERT facts.",
  ["Kidneys → a little posteriorly, not anteriorly", "Bile stored in gall bladder → correct",
   "Ovaries not functionally connected with kidneys → correct", "10 pairs of cranial nerves → correct"],
  R_SOA("frog: anatomy"),
  why_others_wrong="A, B and D are correct statements, so they are not the answer to an 'incorrect' question.",
  seconds=50)


# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "The structure of an amino acid changes in solutions of different pH because:",
  ["Its R group is always a methyl group", "Amino acids are polymers of glucose",
   "Its –NH₂ and –COOH groups are ionisable", "The α-carbon carries no hydrogen atom"], "C",
  "Ionisable nature of amino acids",
  "A particular property of amino acids is the ionisable nature of their –NH₂ and –COOH groups. Hence in solutions "
  "of different pH the structure of amino acids changes (for example, the zwitterionic form).",
  ["Amino and carboxyl groups ionise", "Degree of ionisation depends on pH → structure changes with pH"],
  R_BIO("analysis of chemical composition: amino acids"),
  why_others_wrong="The R group differs between amino acids (H in glycine, methyl in alanine); amino acids are not "
                   "glucose polymers; the α-carbon carries a hydrogen.",
  seconds=25)

Z(BIO, "Nucleic acids", "Basic", "direct",
  "Which of the following nitrogen bases are substituted purines?",
  ["Adenine and guanine", "Cytosine and thymine", "Uracil and cytosine", "Guanine and cytosine"], "A",
  "Purines and pyrimidines",
  "Of the nitrogen bases adenine, guanine, cytosine, uracil and thymine, adenine and guanine are substituted "
  "purines; the rest are substituted pyrimidines.",
  ["Purines → adenine, guanine", "Pyrimidines → cytosine, uracil, thymine"],
  R_BIO("analysis of chemical composition: nitrogen bases"),
  why_others_wrong="B and C name two pyrimidines; D pairs a purine with a pyrimidine.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "The pocket in the tertiary structure of an enzyme into which the substrate fits is called the:",
  ["Prosthetic group", "Co-enzyme", "Allosteric chain", "Active site"], "D",
  "Active site",
  "An enzyme's backbone folds upon itself to form crevices or pockets. One such pocket, into which the substrate "
  "fits, is the active site; through it the enzyme catalyses reactions at a high rate.",
  ["Tertiary structure → pockets", "Substrate-binding pocket → active site"],
  R_BIO("enzymes"),
  why_others_wrong="Prosthetic groups and co-enzymes are co-factors, not pockets of the protein; 'allosteric chain' "
                   "is not an NCERT term for the substrate pocket.",
  seconds=20)

Z(BIO, "Enzymes: properties and action", "Basic", "direct",
  "In an enzyme that needs a co-factor for its activity, the protein portion of the enzyme is called the:",
  ["Holoenzyme", "Apoenzyme", "Co-enzyme", "Ribozyme"], "B",
  "Apoenzyme and co-factor",
  "Some enzymes have non-protein constituents (co-factors) bound to them that make the enzyme catalytically "
  "active. In such enzymes, the protein portion is called the apoenzyme.",
  ["Protein part → apoenzyme", "Non-protein part → co-factor (prosthetic group, co-enzyme or metal ion)"],
  R_BIO("enzymes: co-factors"),
  why_others_wrong="A co-enzyme is a co-factor; a ribozyme is a nucleic acid with enzyme activity; the term "
                   "holoenzyme names the whole enzyme, not the protein portion alone.",
  seconds=20)

Z(BIO, "Carbohydrates and lipids", "Basic", "statement_pair",
  sp("Glycerol is trihydroxy propane.",
     "Fatty acids with one or more C=C double bonds are called saturated fatty acids."),
  STATEMENT_PAIR, "C",
  "Glycerol and fatty acids",
  "NCERT describes glycerol as trihydroxy propane (Statement I true). Fatty acids without a double bond are "
  "saturated; those with one or more C=C double bonds are unsaturated (Statement II false).",
  ["Glycerol = trihydroxy propane → I true", "Double bonds → unsaturated, not saturated → II false"],
  R_BIO("analysis of chemical composition: lipids"), seconds=30)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "statement_pair",
  sp("Starch is a store of energy in plant tissues, and animals have a variant of it called glycogen.",
     "Complex polysaccharides have amino-sugars and chemically modified sugars, such as glucosamine and N-acetyl "
     "galactosamine, as building blocks."),
  STATEMENT_PAIR, "A",
  "Polysaccharides",
  "Starch is the plant store of energy; animals store glycogen, a variant of it (Statement I true). Complex "
  "polysaccharides are built of amino-sugars and chemically modified sugars such as glucosamine and N-acetyl "
  "galactosamine (Statement II true).",
  ["Starch → plants; glycogen → animals → I true", "Amino-sugars as building blocks → II true"],
  R_BIO("polysaccharides"), seconds=35)

Z(BIO, "Nucleic acids", "Intermediate", "match_list",
  ml(("compound", "category"), ["Uracil", "Uridine", "Guanylic acid", "2'-deoxyribose"],
     ["Nucleotide", "Sugar found in DNA", "Nitrogen base", "Nucleoside"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "I", "IV", "II"), M("III", "IV", "II", "I")], at="D"),
  "D",
  "Bases, nucleosides and nucleotides",
  "A nitrogen base (uracil) attached to a sugar gives a nucleoside (uridine); with a phosphate also esterified to "
  "the sugar it becomes a nucleotide (adenylic, guanylic, uridylic acid and so on). The sugar of polynucleotides is "
  "ribose or 2'-deoxyribose; a nucleic acid with deoxyribose is DNA.",
  ["Uracil → base (III)", "Uridine → nucleoside (IV)", "Guanylic acid → nucleotide (I)",
   "2'-deoxyribose → sugar of DNA (II)"],
  R_BIO("analysis of chemical composition; nucleic acids"),
  why_others_wrong="The other codes swap base with nucleoside, nucleoside with nucleotide, or the nucleotide with "
                   "the sugar.",
  seconds=45)

Z(BIO, "Enzymes: properties and action", "Intermediate", "assertion_reason",
  ar("Enzymes isolated from organisms living at very high temperatures, as in hot vents and sulphur springs, "
     "retain their catalytic power even at 80–90 °C.",
     "Each enzyme shows its highest activity at a particular temperature and pH called the optimum temperature and "
     "optimum pH."),
  ASSERTION_REASON, "B",
  "Thermal stability and optimum conditions",
  "NCERT states both: enzymes from organisms of extremely hot habitats are stable and keep their catalytic power at "
  "80–90 °C, and every enzyme has an optimum temperature and pH. R is a general property of all enzymes; it does "
  "not explain why these particular enzymes are thermally stable.",
  ["A: thermostable enzymes from hot vents → true", "R: optimum temperature and pH → true",
   "General property ≠ cause of thermal stability → R does not explain A"],
  R_BIO("enzymes: nature of enzyme action; factors affecting enzyme activity"),
  why_others_wrong="Option A treats a general property as the cause; C and D call a true statement false.",
  seconds=40)

_o = ["(a), (b) and (d) only", "(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]
ms_check("acd", _o, "B")
Z(BIO, "Proteins and amino acids", "Intermediate", "multi_statement",
  ms("Which of the following statements about proteins are correct?",
     ["Proteins are heteropolymers of amino acids.",
      "The first amino acid of a polypeptide is called the C-terminal amino acid.",
      "Insulin is a protein that acts as a hormone.",
      "The three-dimensional tertiary structure of a protein is necessary for many of its biological activities.",
      "The secondary structure of a protein is the sequence of amino acids in it."]),
  _o, "B",
  "Proteins",
  "Proteins are linear chains of amino acids, i.e. heteropolymers. The first amino acid of a chain is the "
  "N-terminal amino acid and the last is the C-terminal. NCERT's table lists insulin as a hormone. The tertiary "
  "structure is absolutely necessary for many biological activities. The sequence of amino acids is the primary "
  "structure, not the secondary.",
  ["(a) True", "(b) False: first = N-terminal", "(c) True", "(d) True", "(e) False: sequence = primary structure"],
  R_BIO("proteins; structure of proteins"),
  why_others_wrong="A and C include (b); D includes (e).",
  seconds=55)

Z(BIO, "Enzymes: properties and action", "Intermediate", "direct",
  "As substrate concentration is raised, the velocity of an enzyme-catalysed reaction rises at first and then "
  "reaches a maximum (Vmax) that is not exceeded by any further rise in substrate concentration. This is because:",
  ["The enzyme molecules are fewer than the substrate molecules, and after they are saturated no free enzyme "
   "molecules are left to bind the extra substrate",
   "The extra substrate denatures the enzyme",
   "The extra substrate acts as a competitive inhibitor",
   "The products formed lower the activation energy further"], "A",
  "Effect of substrate concentration",
  "NCERT: the velocity rises with substrate concentration and reaches Vmax, which is not exceeded, because the "
  "enzyme molecules are fewer than the substrate molecules; once they are all saturated, there are no free enzyme "
  "molecules to bind more substrate.",
  ["Low [S] → velocity rises with [S]", "All enzyme molecules occupied → saturation → Vmax"],
  R_BIO("enzymes: factors affecting enzyme activity"),
  why_others_wrong="Substrate does not denature the enzyme or act as its own competitive inhibitor; products do not "
                   "lower the activation energy.",
  seconds=40)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("Almost all enzymes are proteins.",
     "Like inorganic catalysts, enzymes work efficiently at high temperatures and high pressures."),
  STATEMENT_PAIR, "C",
  "Enzymes versus inorganic catalysts",
  "Almost all enzymes are proteins; a few nucleic acids also act as enzymes (Statement I true). Inorganic "
  "catalysts work efficiently at high temperatures and pressures, whereas enzymes get damaged at high temperatures "
  "(say above 40 °C) (Statement II false).",
  ["Almost all enzymes are proteins → I true", "Enzymes are damaged above about 40 °C → II false"],
  R_BIO("enzymes"), seconds=30)

Z(BIO, "Proteins and amino acids", "Intermediate", "assertion_reason",
  ar("Essential amino acids have to be supplied through our diet.",
     "Our body cannot make essential amino acids, whereas it can make the non-essential ones."),
  ASSERTION_REASON, "A",
  "Essential and non-essential amino acids",
  "Dietary proteins are the source of essential amino acids. Non-essential amino acids are those our body can make; "
  "essential ones it cannot make, so they must come from food. R is exactly why A is true.",
  ["A: essential amino acids from diet → true", "R: body cannot synthesise them → true", "R explains A"],
  R_BIO("proteins"),
  why_others_wrong="B denies the direct causal link; C and D call a true statement false.",
  seconds=30)

Z(BIO, "Proteins and amino acids", "Advanced", "numerical",
  "A protein is made of two polypeptide chains, one of 21 amino acids and the other of 30 amino acids. Each chain "
  "is a linear chain of amino acids joined by peptide bonds. How many peptide bonds are present in the protein?",
  ["51", "50", "48", "49"], "D",
  "Peptide bonds in a polypeptide",
  "In a linear chain of n amino acids, n − 1 peptide bonds join neighbours. Each chain is counted separately "
  "because there is no peptide bond between the two chains.",
  ["Chain 1: 21 − 1 = 20", "Chain 2: 30 − 1 = 29", "Total = 20 + 29 = 49"],
  R_BIO("proteins"),
  shortcut="Peptide bonds = total amino acids − number of chains = 51 − 2 = 49.",
  why_others_wrong="51 counts amino acids, not bonds; 50 treats both chains as one continuous chain; 48 subtracts "
                   "one bond too many.",
  seconds=45, verified_by=RECOMPUTED)

_o = ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b) and (c) only", "(a), (b), (c) and (d) only"]
ms_check("abc", _o, "C")
Z(BIO, "Nucleic acids", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["Proteins, nucleic acids and polysaccharides are found in the acid-insoluble fraction of a living tissue.",
      "Biomolecules of the acid-insoluble fraction other than lipids have molecular weights of ten thousand "
      "daltons and above.",
      "A nucleic acid containing deoxyribose is DNA, while one containing ribose is RNA.",
      "In a protein, adjacent amino acids are joined by glycosidic bonds.",
      "The sugar found in polynucleotides is a hexose."]),
  _o, "C",
  "Macromolecules and nucleic acids",
  "Grinding a tissue in trichloroacetic acid gives an acid-insoluble fraction of proteins, nucleic acids, "
  "polysaccharides and lipids. Except lipids, these have molecular weights of ten thousand daltons and above. The "
  "sugar of polynucleotides is ribose or 2'-deoxyribose, both pentoses; deoxyribose gives DNA and ribose RNA. "
  "Amino acids in proteins are linked by peptide bonds; glycosidic bonds link sugars.",
  ["(a) True", "(b) True", "(c) True", "(d) False: peptide bonds", "(e) False: pentose sugar"],
  R_BIO("biomacromolecules; nucleic acids"),
  why_others_wrong="A includes (e); B and D include (d).",
  seconds=65)

Z(BIO, "Carbohydrates and lipids", "Advanced", "match_list",
  ml(("lipid", "feature"), ["Palmitic acid", "Arachidonic acid", "Lecithin", "Gingelly oil"],
     ["Phospholipid found in cell membranes", "Fatty acid with 20 carbon atoms including the carboxyl carbon",
      "Fatty acid with 16 carbon atoms including the carboxyl carbon",
      "Has a low melting point and remains liquid in winter"]),
  match_options(M("III", "II", "I", "IV"),
                [M("II", "III", "I", "IV"), M("III", "II", "IV", "I"), M("I", "II", "III", "IV")], at="B"),
  "B",
  "Fatty acids, phospholipids and oils",
  "Palmitic acid has 16 carbons and arachidonic acid 20 carbons, each count including the carboxyl carbon. "
  "Lecithin is a phospholipid found in cell membranes. Oils such as gingelly oil have lower melting points and stay "
  "liquid in winter.",
  ["Palmitic → 16 C (III)", "Arachidonic → 20 C (II)", "Lecithin → phospholipid (I)", "Gingelly oil → low m.p. (IV)"],
  R_BIO("analysis of chemical composition: lipids"),
  why_others_wrong="The other codes swap the two fatty acids, or lecithin with the oil, or lecithin with palmitic "
                   "acid.",
  seconds=50)

Z(BIO, "Enzymes: properties and action", "Advanced", "direct",
  "Which sequence correctly describes the catalytic cycle of an enzyme?",
  ["Products are released → substrate binds to the active site → bonds of the substrate are broken → enzyme alters "
   "its shape",
   "Enzyme alters its shape → substrate binds to a site away from the active site → products are released → "
   "enzyme–product complex forms",
   "Substrate binds to the active site → bonds of the substrate are broken → enzyme alters its shape around the "
   "products → products stay bound permanently",
   "Substrate binds to the active site → enzyme alters its shape to fit more tightly around the substrate → bonds "
   "of the substrate are broken and an enzyme–product complex forms → products are released and the free enzyme "
   "can bind another substrate molecule"], "D",
  "Catalytic cycle of an enzyme",
  "NCERT gives four steps: (1) the substrate binds to the active site; (2) binding induces the enzyme to alter its "
  "shape and fit more tightly around the substrate; (3) the active site breaks the chemical bonds of the substrate "
  "and an enzyme–product complex forms; (4) the enzyme releases the products and the free enzyme is ready for "
  "another substrate molecule.",
  ["Bind → induced fit → bond breaking (EP complex) → release and reuse"],
  R_BIO("enzymes: nature of enzyme action"),
  why_others_wrong="A and B scramble the order (release before binding, binding away from the active site); C keeps "
                   "the products bound, but the enzyme is released unchanged for reuse.",
  seconds=55)

Z(BIO, "Enzyme classification", "Advanced", "direct",
  "Which statement about the classification and naming of enzymes is correct?",
  ["Enzymes are divided into 6 classes, each with 4–13 subclasses, and each enzyme is named by a four-digit number",
   "Enzymes are divided into 4 classes, each with 6–13 subclasses, and each enzyme is named by a six-digit number",
   "Enzymes are divided into 13 classes, each with 4–6 subclasses, and each enzyme is named by a four-letter code",
   "Enzymes are divided into 6 classes, each with exactly 4 subclasses, and each enzyme is named by a two-digit "
   "number"], "A",
  "Enzyme nomenclature",
  "NCERT: enzymes are divided into 6 classes (oxidoreductases/dehydrogenases, transferases, hydrolases, lyases, "
  "isomerases and ligases), each with 4–13 subclasses, and are named accordingly by a four-digit number.",
  ["6 classes", "4–13 subclasses each", "Four-digit number for each enzyme"],
  R_BIO("enzymes: classification and nomenclature of enzymes"),
  why_others_wrong="B, C and D change the number of classes, the number of subclasses or the length of the code.",
  seconds=40)


# ================================================================ Breathing and Exchange of Gases (B4 I5 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Respiratory system", "Basic", "direct",
  "The cartilaginous box of the human respiratory tract that helps in sound production, and is therefore called "
  "the sound box, is the:",
  ["Pharynx", "Larynx", "Trachea", "Bronchiole"], "B",
  "Human respiratory tract",
  "The pharynx opens through the larynx into the trachea. The larynx is a cartilaginous box that helps in sound "
  "production and is hence called the sound box.",
  ["Nostrils → nasal chamber → pharynx → larynx (sound box) → trachea"],
  R_BRE("human respiratory system"),
  why_others_wrong="The pharynx is a common passage for food and air; the trachea and bronchioles are air tubes, "
                   "not the sound box.",
  seconds=20)

Z(BRE, "Respiratory system", "Basic", "direct",
  "During swallowing, the entry of food into the larynx is prevented by a thin, elastic, cartilaginous flap called "
  "the:",
  ["Glottis", "Pleura", "Epiglottis", "Diaphragm"], "C",
  "Epiglottis",
  "During swallowing, the glottis can be covered by a thin elastic cartilaginous flap called the epiglottis, which "
  "prevents the entry of food into the larynx.",
  ["Glottis = opening of the larynx", "Epiglottis covers the glottis during swallowing"],
  R_BRE("human respiratory system"),
  why_others_wrong="The glottis is the opening that gets covered; the pleura covers the lungs; the diaphragm "
                   "separates thorax from abdomen.",
  seconds=20)

Z(BRE, "Respiratory system", "Basic", "direct",
  "The lungs are covered by a double-layered pleura with pleural fluid between the layers. The pleural fluid:",
  ["Reduces friction on the lung surface", "Carries oxygen to the alveoli", "Produces surfactant for gas exchange",
   "Forms the exchange surface of the alveoli"], "A",
  "Pleura and pleural fluid",
  "The lungs are covered by a double-layered pleura with pleural fluid between the layers, which reduces friction "
  "on the lung surface. The outer pleural membrane is in close contact with the thoracic lining and the inner one "
  "with the lung surface.",
  ["Double-layered pleura around each lung", "Pleural fluid → reduces friction"],
  R_BRE("human respiratory system"),
  why_others_wrong="NCERT gives only one role for pleural fluid, reducing friction; gas exchange takes place across "
                   "the alveolar wall, not through the pleura.",
  seconds=20)

Z(BRE, "Respiratory volumes", "Basic", "numerical",
  "A healthy man has a tidal volume of 500 mL, an expiratory reserve volume of 1100 mL and an inspiratory reserve "
  "volume of 3000 mL, and he breathes 14 times per minute at rest. What volume of air does he inspire per minute "
  "during normal breathing?",
  ["35.7 mL", "514 mL", "22,400 mL", "7000 mL"], "D",
  "Tidal volume and breathing rate",
  "During normal breathing, the volume inspired in each breath is the tidal volume. Volume per minute = tidal "
  "volume × breathing rate. NCERT notes that a healthy man can inspire or expire about 6000 to 8000 mL of air per "
  "minute; 7000 mL lies in that range. The reserve volumes are used only in forcible breathing.",
  ["Air per breath (normal) = TV = 500 mL", "Air per minute = 500 × 14 = 7000 mL"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="35.7 mL divides instead of multiplying; 514 mL adds the rate to the volume; 22,400 mL wrongly "
                   "adds the ERV to each breath.",
  seconds=40, verified_by=RECOMPUTED)

Z(BRE, "Respiratory system", "Intermediate", "match_list",
  ml(("animal", "respiratory surface"), ["Flatworms", "Earthworms", "Fishes", "Frogs"],
     ["Gills", "Lungs and moist skin", "Simple diffusion over the entire body surface", "Moist cuticle"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("III", "I", "IV", "II")], at="C"),
  "C",
  "Respiratory organs in animals",
  "Lower invertebrates such as sponges, coelenterates and flatworms exchange gases by simple diffusion over the "
  "entire body surface. Earthworms use their moist cuticle. Fishes use gills. Amphibians such as frogs respire "
  "through lungs and can also respire through their moist skin.",
  ["Flatworms → body surface (III)", "Earthworms → moist cuticle (IV)", "Fishes → gills (I)",
   "Frogs → lungs and moist skin (II)"],
  R_BRE("respiratory organs"),
  why_others_wrong="The other codes swap flatworms with earthworms, fishes with frogs, or earthworms with fishes.",
  seconds=40)

Z(BRE, "Mechanism of breathing", "Intermediate", "assertion_reason",
  ar("Contraction of the diaphragm increases the volume of the thoracic chamber in the antero-posterior axis.",
     "Contraction of the external inter-costal muscles lifts up the ribs and the sternum, increasing the volume of "
     "the thoracic chamber in the dorso-ventral axis."),
  ASSERTION_REASON, "B",
  "Muscles of inspiration",
  "Both statements are NCERT facts about inspiration. A concerns the diaphragm (antero-posterior axis); R concerns "
  "a different set of muscles, the external inter-costals (dorso-ventral axis). R describes a separate "
  "contribution to the rise in thoracic volume and does not explain A.",
  ["A: diaphragm → antero-posterior axis → true",
   "R: external inter-costals → dorso-ventral axis → true", "Different muscles, different axes → R does not "
   "explain A"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A treats an independent muscle action as the cause; C and D call a true statement false.",
  seconds=40)

_o = ["(a), (b), (c) and (e) only", "(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]
ms_check("abce", _o, "A")
Z(BRE, "Respiratory volumes", "Intermediate", "multi_statement",
  ms("Which of the following definitions of respiratory volumes and capacities are correct?",
     ["Residual volume is the volume of air remaining in the lungs even after a forcible expiration.",
      "Vital capacity is the maximum volume of air a person can breathe in after a forced expiration.",
      "Functional residual capacity is the expiratory reserve volume plus the residual volume.",
      "Inspiratory capacity is the tidal volume plus the expiratory reserve volume.",
      "Total lung capacity is the vital capacity plus the residual volume."]),
  _o, "A",
  "Respiratory volumes and capacities",
  "RV is the air left after forcible expiration. VC (ERV + TV + IRV) is the maximum volume breathed in after a "
  "forced expiration (or out after a forced inspiration). FRC = ERV + RV. Inspiratory capacity is TV + IRV, not "
  "TV + ERV (that sum is the expiratory capacity). TLC = VC + RV.",
  ["(a) True", "(b) True", "(c) True", "(d) False: IC = TV + IRV", "(e) True"],
  R_BRE("respiratory volumes and capacities"),
  why_others_wrong="B, C and D include the false statement (d); B and C also leave out true statements.",
  seconds=55)

Z(BRE, "Exchange and transport of gases", "Intermediate", "statement_pair",
  sp("The diffusion membrane is made of three major layers: the thin squamous epithelium of the alveoli, the "
     "endothelium of the alveolar capillaries, and the basement substance between them.",
     "The total thickness of the diffusion membrane is much more than a millimetre."),
  STATEMENT_PAIR, "C",
  "Diffusion membrane",
  "The diffusion membrane has three major layers: alveolar squamous epithelium, capillary endothelium and the "
  "basement substance between them (Statement I true). Its total thickness is much less than a millimetre, which "
  "favours diffusion (Statement II false).",
  ["Three layers → I true", "Thickness much less than 1 mm → II false"],
  R_BRE("exchange of gases"), seconds=35)

Z(BRE, "Exchange and transport of gases", "Intermediate", "direct",
  "Which set of conditions, found in the alveoli, favours the formation of oxyhaemoglobin?",
  ["Low pO₂, high pCO₂, higher H⁺ concentration and higher temperature",
   "High pO₂, high pCO₂, higher H⁺ concentration and lower temperature",
   "Low pO₂, low pCO₂, lesser H⁺ concentration and higher temperature",
   "High pO₂, low pCO₂, lesser H⁺ concentration and lower temperature"], "D",
  "Factors affecting oxygen binding",
  "Binding of O₂ to haemoglobin depends mainly on pO₂; pCO₂, H⁺ concentration and temperature also interfere. In "
  "the alveoli there is high pO₂, low pCO₂, lesser H⁺ concentration and lower temperature, all favourable for "
  "oxyhaemoglobin formation. The opposite conditions in the tissues favour dissociation of O₂.",
  ["Alveoli: ↑pO₂, ↓pCO₂, ↓H⁺, ↓temperature → O₂ binds", "Tissues: the reverse → O₂ released"],
  R_BRE("transport of gases: transport of oxygen"),
  why_others_wrong="A gives the tissue conditions, which favour dissociation; B and C mix favourable and "
                   "unfavourable factors.",
  seconds=40)

Z(BRE, "Exchange and transport of gases", "Advanced", "numerical",
  "The partial pressures (in mm Hg) are: alveoli, pO₂ 104 and pCO₂ 40; deoxygenated blood, pO₂ 40 and pCO₂ 45; "
  "oxygenated blood, pO₂ 95 and pCO₂ 40. What are the partial-pressure gradients for O₂ from the alveoli to the "
  "deoxygenated blood reaching the lungs, and for CO₂ from that blood to the alveoli?",
  ["55 mm Hg for O₂ and 5 mm Hg for CO₂", "64 mm Hg for O₂ and 5 mm Hg for CO₂",
   "64 mm Hg for O₂ and 45 mm Hg for CO₂", "104 mm Hg for O₂ and 40 mm Hg for CO₂"], "B",
  "Partial-pressure gradients at the alveoli",
  "Gas moves down its partial-pressure gradient. Deoxygenated blood arrives at the alveoli, so the O₂ gradient is "
  "alveolar pO₂ minus blood pO₂, and the CO₂ gradient is blood pCO₂ minus alveolar pCO₂.",
  ["O₂: 104 − 40 = 64 mm Hg (alveoli → blood)", "CO₂: 45 − 40 = 5 mm Hg (blood → alveoli)",
   "CO₂ still diffuses readily because its solubility is 20–25 times that of O₂"],
  R_BRE("exchange of gases"),
  why_others_wrong="55 mm Hg uses the oxygenated-blood pO₂ (95) in place of the alveolar value; 45 mm Hg is the "
                   "blood pCO₂ itself, not a difference; 104 and 40 are the alveolar values, not gradients.",
  seconds=60, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Advanced", "assertion_reason",
  ar("RBCs contain a very high concentration of the enzyme carbonic anhydrase, and minute quantities of it are "
     "present in the plasma too.",
     "At the alveolar site, where pCO₂ is high, carbonic anhydrase converts CO₂ and water into HCO₃⁻ and H⁺."),
  ASSERTION_REASON, "C",
  "Carbonic anhydrase and CO₂ transport",
  "A is an NCERT statement. At the tissue site, where pCO₂ is high because of catabolism, CO₂ diffuses into blood "
  "and forms HCO₃⁻ and H⁺. At the alveolar site pCO₂ is low, and the reaction runs the opposite way, releasing CO₂ "
  "and H₂O. R puts the high pCO₂ at the alveoli and the forward reaction there, so R is false.",
  ["A: high carbonic anhydrase in RBCs, minute amount in plasma → true",
   "Tissues: high pCO₂ → HCO₃⁻ formed", "Alveoli: low pCO₂ → HCO₃⁻ → CO₂ + H₂O → R false"],
  R_BRE("transport of gases: transport of carbon dioxide"),
  why_others_wrong="A and B need R to be true; D calls the true assertion false.",
  seconds=45)

_o = ["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (d) only", "(a), (b) and (c) only"]
ms_check("abc", _o, "D")
Z(BRE, "Regulation and disorders", "Advanced", "multi_statement",
  ms("Which of the following statements about respiratory disorders are correct?",
     ["Cigarette smoking is one of the major causes of emphysema.",
      "Long exposure to the dust of grinding or stone-breaking industries can cause inflammation leading to "
      "fibrosis and serious lung damage.",
      "Workers in such industries should wear protective masks.",
      "In grinding and stone-breaking industries, the body's defence mechanism can fully cope with the dust "
      "produced."]),
  _o, "D",
  "Occupational respiratory disorders",
  "NCERT: cigarette smoking is one of the major causes of emphysema. In industries involving grinding or "
  "stone-breaking, so much dust is produced that the body's defence mechanism cannot fully cope; long exposure "
  "causes inflammation, fibrosis (proliferation of fibrous tissue) and serious lung damage, so workers should wear "
  "protective masks.",
  ["(a) True", "(b) True", "(c) True", "(d) False: the defence mechanism cannot fully cope"],
  R_BRE("disorders of respiratory system"),
  why_others_wrong="A leaves out (c); B and C include the false statement (d).",
  seconds=45)

Z(BRE, "Mechanism of breathing", "Advanced", "direct",
  "Which sequence correctly describes normal (quiet) expiration in humans?",
  ["Diaphragm and inter-costal muscles relax → diaphragm and sternum return to their normal positions → thoracic "
   "and pulmonary volumes decrease → intra-pulmonary pressure rises slightly above atmospheric pressure → air is "
   "expelled",
   "Diaphragm and external inter-costal muscles contract → thoracic volume increases → intra-pulmonary pressure "
   "rises above atmospheric pressure → air is expelled",
   "Diaphragm relaxes → thoracic volume increases → intra-pulmonary pressure falls below atmospheric pressure → "
   "air is expelled",
   "Inter-costal muscles relax → pulmonary volume increases → intra-pulmonary pressure becomes equal to "
   "atmospheric pressure → air is expelled"], "A",
  "Mechanism of expiration",
  "Relaxation of the diaphragm and the inter-costal muscles returns the diaphragm and sternum to their normal "
  "positions and reduces the thoracic volume and thereby the pulmonary volume. Intra-pulmonary pressure rises to "
  "slightly above atmospheric pressure, and air is expelled.",
  ["Muscles relax → volumes fall", "Volume falls → pressure rises above atmospheric", "Air flows out"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="B describes the muscle action of inspiration; C and D let volume rise during expiration, and "
                   "air cannot flow out when the inside pressure is lower than or equal to the outside pressure.",
  seconds=50)


# ================================================================ Body Fluids and Circulation (B5 I6 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "A healthy adult human has, on average, how much haemoglobin in every 100 mL of blood?",
  ["1.2–1.6 g", "5–5.5 g", "12–16 g", "120–160 g"], "C",
  "Haemoglobin content of blood",
  "RBCs contain the red, iron-containing protein haemoglobin. A healthy individual has 12–16 g of haemoglobin in "
  "every 100 mL of blood.",
  ["Haemoglobin → 12–16 g per 100 mL of blood"],
  R_BFC("blood: formed elements"),
  why_others_wrong="1.2–1.6 g and 120–160 g are off by a factor of ten; 5–5.5 is the RBC count in millions per "
                   "mm³, not grams of haemoglobin.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "RBCs have an average life span of 120 days, after which they are destroyed in the organ called the 'graveyard "
  "of RBCs'. This organ is the:",
  ["Spleen", "Liver", "Red bone marrow", "Kidney"], "A",
  "Life span of RBCs",
  "RBCs live on average 120 days and are then destroyed in the spleen, the graveyard of RBCs. In adults they are "
  "formed in the red bone marrow.",
  ["Formed → red bone marrow (adults)", "Destroyed after 120 days → spleen"],
  R_BFC("blood: formed elements"),
  why_others_wrong="Red bone marrow is where RBCs are formed; NCERT names the spleen, not the liver or kidney, as "
                   "the graveyard of RBCs.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "Which plasma proteins are primarily involved in the defence mechanisms of the body?",
  ["Albumins", "Fibrinogens", "Haemoglobins", "Globulins"], "D",
  "Plasma proteins",
  "Fibrinogen, globulins and albumins are the major plasma proteins. Fibrinogens are needed for clotting, globulins "
  "are primarily involved in defence mechanisms, and albumins help in osmotic balance.",
  ["Fibrinogen → clotting", "Globulins → defence", "Albumins → osmotic balance"],
  R_BFC("blood: plasma"),
  why_others_wrong="Albumins maintain osmotic balance; fibrinogens act in clotting; haemoglobin is inside RBCs, not "
                   "a plasma protein.",
  seconds=20)

Z(BFC, "Cardiac cycle and ECG", "Basic", "numerical",
  "The heart rate of a person can be found by counting the QRS complexes in an ECG over a known time. If 18 QRS "
  "complexes are recorded in 15 seconds, the heart rate is:",
  ["50 per minute", "72 per minute", "270 per minute", "36 per minute"], "B",
  "Heart rate from the ECG",
  "Each QRS complex marks one depolarisation of the ventricles, i.e. one heartbeat. NCERT notes that counting QRS "
  "complexes in a given time gives the heart rate.",
  ["Beats in 15 s = 18", "Beats per minute = 18 × (60 / 15) = 18 × 4 = 72"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="50 per minute inverts the ratio (15 × 60 / 18); 270 multiplies 18 by 15; 36 scales 15 s up to "
                   "30 s only.",
  seconds=35, verified_by=RECOMPUTED)

Z(BFC, "Double circulation and regulation", "Basic", "direct",
  "The heart of fishes has:",
  ["Three chambers: two atria and one ventricle", "Four chambers: two atria and two ventricles",
   "Three chambers: one atrium and two ventricles", "Two chambers: an atrium and a ventricle"], "D",
  "Hearts of vertebrates",
  "Fishes have a two-chambered heart with an atrium and a ventricle. Amphibians and reptiles (except crocodiles) "
  "have a three-chambered heart with two atria and one ventricle; crocodiles, birds and mammals have a "
  "four-chambered heart. In fishes the heart pumps out deoxygenated blood, which is oxygenated by the gills.",
  ["Fishes → 2 chambers", "Amphibians, most reptiles → 3 chambers", "Crocodiles, birds, mammals → 4 chambers"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A is the amphibian heart, B the bird and mammal heart; C does not occur in vertebrates.",
  seconds=20)

Z(BFC, "Coagulation and lymph", "Intermediate", "statement_pair",
  sp("Lymph is a colourless fluid containing specialised lymphocytes, which are responsible for the immune "
     "responses of the body.",
     "Fats are absorbed through lymph in the lacteals present in the intestinal villi."),
  STATEMENT_PAIR, "A",
  "Lymph",
  "Lymph is a colourless fluid with specialised lymphocytes responsible for immune responses; it is also an "
  "important carrier of nutrients and hormones. Fats are absorbed through lymph in the lacteals of the intestinal "
  "villi. Both statements are true.",
  ["Colourless, with lymphocytes → I true", "Fat absorption via lacteals → II true"],
  R_BFC("lymph (tissue fluid)"), seconds=30)

Z(BFC, "Blood and blood groups", "Intermediate", "match_list",
  ml(("component of blood", "normal value"), ["Erythrocytes", "Leucocytes", "Platelets", "Plasma"],
     ["6000–8000 per mm³ of blood", "About 55 per cent of blood", "1,50,000–3,50,000 per mm³ of blood",
      "5–5.5 million per mm³ of blood"]),
  match_options(M("IV", "I", "III", "II"),
                [M("IV", "III", "I", "II"), M("I", "IV", "III", "II"), M("IV", "I", "II", "III")], at="B"),
  "B",
  "Composition of blood",
  "A healthy adult has 5–5.5 million RBCs, 6000–8000 WBCs and 1,50,000–3,50,000 platelets per mm³ of blood. Plasma "
  "forms nearly 55 per cent of the blood; formed elements form about 45 per cent.",
  ["RBCs → 5–5.5 million (IV)", "WBCs → 6000–8000 (I)", "Platelets → 1.5–3.5 lakh (III)", "Plasma → 55% (II)"],
  R_BFC("blood: plasma and formed elements"),
  why_others_wrong="The other codes swap WBC and platelet counts, RBC and WBC counts, or platelets with plasma.",
  seconds=45)

Z(BFC, "Double circulation and regulation", "Intermediate", "assertion_reason",
  ar("The human heart is called myogenic.",
     "The normal activities of the heart are regulated intrinsically (auto-regulated) by specialised muscles, the "
     "nodal tissue."),
  ASSERTION_REASON, "A",
  "Myogenic heart",
  "NCERT: normal activities of the heart are regulated intrinsically, i.e. auto-regulated by specialised muscles "
  "(nodal tissue); hence the heart is called myogenic. R is the reason for the term in A.",
  ["A: heart is myogenic → true", "R: auto-regulated by nodal tissue → true", "'Hence' links R to A → R explains A"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="B denies the link NCERT states with 'hence'; C and D call a true statement false.",
  seconds=30)

_o = ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (d) only", "(a), (c), (d) and (e) only"]
ms_check("acd", _o, "C")
Z(BFC, "Blood and blood groups", "Intermediate", "multi_statement",
  ms("Which of the following statements about the formed elements of blood are correct?",
     ["In adults, RBCs are formed in the red bone marrow.",
      "In most mammals, RBCs are nucleated and spherical.",
      "Platelets are cell fragments produced from megakaryocytes.",
      "A reduction in the number of platelets can lead to clotting disorders and excessive loss of blood.",
      "Erythrocytes are the least abundant cells in blood."]),
  _o, "C",
  "Formed elements of blood",
  "RBCs are formed in the red bone marrow in adults; in most mammals they lack a nucleus and are biconcave. "
  "Platelets (thrombocytes) are cell fragments from megakaryocytes, and a fall in their number causes clotting "
  "disorders with excessive blood loss. Erythrocytes are the most abundant cells in blood.",
  ["(a) True", "(b) False: enucleate and biconcave", "(c) True", "(d) True", "(e) False: most abundant"],
  R_BFC("blood: formed elements"),
  why_others_wrong="A and B include (b); D includes (e).",
  seconds=50)

Z(BFC, "Double circulation and regulation", "Intermediate", "direct",
  "In human double circulation, the pulmonary artery carries:",
  ["Oxygenated blood from the left ventricle to the body",
   "Deoxygenated blood from the right ventricle to the lungs",
   "Oxygenated blood from the lungs to the left atrium",
   "Deoxygenated blood from the body to the right atrium"], "B",
  "Pulmonary circulation",
  "Deoxygenated blood pumped by the right ventricle enters the pulmonary artery and goes to the lungs. Oxygenated "
  "blood returns through the pulmonary veins to the left atrium. This is the pulmonary circulation.",
  ["Right ventricle → pulmonary artery (deoxygenated) → lungs", "Lungs → pulmonary veins (oxygenated) → left atrium"],
  R_BFC("double circulation"),
  why_others_wrong="A describes the aorta, C the pulmonary veins and D the venae cavae.",
  seconds=30)

Z(BFC, "Human heart", "Intermediate", "statement_pair",
  sp("A special coronary system of blood vessels circulates blood exclusively to and from the cardiac musculature.",
     "The walls of the ventricles are much thinner than the walls of the atria."),
  STATEMENT_PAIR, "C",
  "Coronary system and heart walls",
  "NCERT: a special coronary system of blood vessels exists exclusively for circulation of blood to and from the "
  "cardiac musculature (Statement I true). The walls of the ventricles are much thicker than those of the atria "
  "(Statement II false).",
  ["Coronary system → heart muscle only → I true", "Ventricular walls thicker → II false"],
  R_BFC("double circulation; human circulatory system"), seconds=30)

_o = ["(a), (b) and (e) only", "(a), (b), (c) and (d) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]
ms_check("abcd", _o, "B")
Z(BFC, "Cardiac cycle and ECG", "Advanced", "multi_statement",
  ms("Which of the following statements about the cardiac cycle are correct?",
     ["As the ventricles contract, ventricular pressure rises and closes the tricuspid and bicuspid valves because of "
      "the attempted backflow of blood into the atria.",
      "As ventricular pressure rises further, the semilunar valves guarding the pulmonary artery and the aorta are "
      "forced open.",
      "As the ventricles relax, ventricular pressure falls and the semilunar valves close, preventing backflow.",
      "Each ventricle pumps out about 70 mL of blood in each cardiac cycle.",
      "The atria and the ventricles contract at the same time."]),
  _o, "B",
  "Events of the cardiac cycle",
  "During ventricular systole the rising pressure first closes the atrio-ventricular valves and then forces the "
  "semilunar valves open. When the ventricles relax, their pressure falls and the semilunar valves close. The "
  "stroke volume is about 70 mL per ventricle per cycle. The atria contract first (atrial systole) and the "
  "ventricles afterwards, when the action potential reaches them through the AVN and bundle of His; the two do not "
  "contract together.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: atrial systole precedes ventricular systole"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A and D include (e); C leaves out the true statement (a).",
  seconds=65)

Z(BFC, "Double circulation and regulation", "Advanced", "assertion_reason",
  ar("Neural signals through the sympathetic nerves decrease the rate of heartbeat.",
     "Adrenal medullary hormones can increase the cardiac output."),
  ASSERTION_REASON, "D",
  "Regulation of cardiac activity",
  "Sympathetic signals increase the rate of heartbeat, the strength of ventricular contraction and thereby the "
  "cardiac output; it is parasympathetic signals that decrease them. So A is false. Adrenal medullary hormones can "
  "also increase the cardiac output, so R is true.",
  ["A: sympathetic → increases heart rate → A false", "R: adrenal medullary hormones ↑ cardiac output → true"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="A, B and C all require the assertion to be true.",
  seconds=40)

Z(BFC, "Blood and blood groups", "Advanced", "match_list",
  ml(("leucocyte", "percentage of total WBCs"), ["Neutrophils", "Eosinophils", "Basophils", "Lymphocytes"],
     ["0.5–1", "20–25", "60–65", "2–3"]),
  match_options(M("III", "IV", "I", "II"),
                [M("III", "I", "IV", "II"), M("II", "IV", "I", "III"), M("III", "II", "I", "IV")], at="D"),
  "D",
  "Differential count of leucocytes",
  "Neutrophils are the most abundant WBCs (60–65 per cent) and basophils the least (0.5–1 per cent). Eosinophils "
  "form 2–3 per cent and lymphocytes 20–25 per cent (monocytes 6–8 per cent).",
  ["Neutrophils → 60–65 (III)", "Eosinophils → 2–3 (IV)", "Basophils → 0.5–1 (I)", "Lymphocytes → 20–25 (II)"],
  R_BFC("blood: formed elements"),
  why_others_wrong="The other codes swap eosinophils with basophils, neutrophils with lymphocytes, or eosinophils "
                   "with lymphocytes.",
  seconds=50)

Z(BFC, "Blood and blood groups", "Advanced", "direct",
  "A person with blood group B needs a transfusion. Which option lists all the ABO donor groups whose blood is "
  "compatible with this person?",
  ["B and O", "B and AB", "A, B, AB and O", "B only"], "A",
  "ABO compatibility",
  "A group B person has antigen B on the RBCs and anti-A antibodies in plasma. Donor RBCs must therefore not carry "
  "antigen A. Group B (antigen B) and group O (no antigens) qualify; A and AB carry antigen A.",
  ["Recipient B → plasma has anti-A", "Donor RBCs must lack antigen A", "Compatible donors → B and O"],
  R_BFC("blood groups: ABO grouping"),
  why_others_wrong="AB and A donor cells carry antigen A, which the recipient's anti-A would attack; 'B only' leaves "
                   "out group O, which is also compatible.",
  seconds=45)

Z(BFC, "Coagulation and lymph", "Advanced", "direct",
  "As blood passes through the capillaries in tissues, some fluid moves out into the spaces between the cells. "
  "Which statement about this interstitial (tissue) fluid is correct?",
  ["It contains all the formed elements of blood but no water-soluble substances",
   "It contains the larger plasma proteins but no minerals",
   "It has the same mineral distribution as plasma, while the larger proteins and most formed elements stay in "
   "the blood vessels",
   "It is identical to plasma, including the larger proteins"], "C",
  "Formation of tissue fluid",
  "Water and many small water-soluble substances move out of the capillaries, leaving the larger proteins and most "
  "formed elements in the blood vessels. This interstitial fluid has the same mineral distribution as plasma. "
  "Exchange of nutrients and gases between blood and cells always occurs through it.",
  ["Water + small solutes leave capillaries", "Large proteins + most formed elements stay behind",
   "Minerals as in plasma"],
  R_BFC("lymph (tissue fluid)"),
  why_others_wrong="Formed elements and larger proteins mostly stay in the vessels, so A, B and D are wrong; minerals "
                   "do pass out, which also rules out B.",
  seconds=45)


# ================================================================ Excretory Products and their Elimination (B4 I6 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Modes of excretion", "Basic", "direct",
  "Which of the following groups includes many ammonotelic animals?",
  ["Birds", "Bony fishes", "Mammals", "Land snails"], "B",
  "Ammonotelism",
  "Ammonia is the most toxic nitrogenous waste and needs much water for its removal. Many bony fishes, aquatic "
  "amphibians and aquatic insects are ammonotelic; ammonia diffuses out across body surfaces or gill surfaces as "
  "ammonium ions.",
  ["Ammonotelic → many bony fishes, aquatic amphibians, aquatic insects", "Ureotelic → mammals",
   "Uricotelic → birds, land snails"],
  R_EXC("introduction: ammonotelism, ureotelism, uricotelism"),
  why_others_wrong="Mammals are ureotelic; birds and land snails are uricotelic.",
  seconds=20)

Z(EXC, "Nephron structure", "Basic", "direct",
  "The renal tubule of a nephron begins with a double-walled, cup-like structure that encloses the glomerulus. This "
  "structure is the:",
  ["Bowman's capsule", "Loop of Henle", "Renal pelvis", "Collecting duct"], "A",
  "Parts of a nephron",
  "Each nephron has a glomerulus and a renal tubule. The tubule begins with the double-walled, cup-like Bowman's "
  "capsule, which encloses the glomerulus; together they form the Malpighian body (renal corpuscle).",
  ["Glomerulus + Bowman's capsule = Malpighian body", "Then PCT → Henle's loop → DCT → collecting duct"],
  R_EXC("human excretory system: nephron"),
  why_others_wrong="Henle's loop and the collecting duct are later parts of the tubule; the renal pelvis is a "
                   "funnel-shaped space of the kidney, not part of a nephron.",
  seconds=20)

Z(EXC, "Regulation of kidney function", "Basic", "statement_pair",
  sp("Urine formed by the nephrons is stored in the urinary bladder until a voluntary signal is given by the "
     "central nervous system.",
     "During micturition, the smooth muscles of the bladder relax and the urethral sphincter contracts."),
  STATEMENT_PAIR, "C",
  "Micturition",
  "Urine is stored in the bladder until the CNS gives a voluntary signal (Statement I true). When the bladder "
  "fills, stretch receptors send signals to the CNS, which sends motor messages that contract the smooth muscles "
  "of the bladder and simultaneously relax the urethral sphincter, releasing urine (Statement II false).",
  ["Storage until voluntary CNS signal → I true", "Bladder muscles contract, sphincter relaxes → II false"],
  R_EXC("micturition"), seconds=30)

Z(EXC, "Urine formation", "Basic", "numerical",
  "Filtrate enters the descending limb of Henle's loop at an osmolarity of 300 mOsmol L⁻¹ and reaches the hairpin "
  "bend at 1200 mOsmol L⁻¹. Assume that the amount of solute in the filtrate does not change along this limb. If "
  "20 mL of filtrate enters the descending limb, what volume reaches the hairpin bend?",
  ["80 mL", "15 mL", "20 mL", "5 mL"], "D",
  "Concentration of the filtrate in the descending limb",
  "NCERT: the descending limb of the loop of Henle is permeable to water but almost impermeable to electrolytes, "
  "so the filtrate gets concentrated as it moves down by losing water, while its solutes stay in it. With the "
  "solute amount fixed, volume × osmolarity stays constant, so a four-fold rise in osmolarity means the volume "
  "falls to one-fourth.",
  ["Solute amount constant: 20 mL × 300 = V × 1200", "V = 20 × 300 / 1200 = 5 mL"],
  R_EXC("urine formation: function of the tubules (Henle's loop) and mechanism of concentration of the filtrate"),
  shortcut="Osmolarity rises 4-fold (300 → 1200), so the volume falls to 1/4 of 20 mL.",
  why_others_wrong="80 mL multiplies by the ratio instead of dividing; 15 mL is the volume of water lost, not the "
                   "volume left; 20 mL assumes the filtrate is concentrated by gaining solutes, but this limb is "
                   "almost impermeable to electrolytes.",
  seconds=40, verified_by=RECOMPUTED)

Z(EXC, "Modes of excretion", "Intermediate", "assertion_reason",
  ar("Our lungs remove large amounts of CO₂ (about 200 mL per minute) and also significant quantities of water "
     "every day.",
     "The liver secretes bile containing substances such as bilirubin, biliverdin, cholesterol, degraded steroid "
     "hormones, vitamins and drugs."),
  ASSERTION_REASON, "B",
  "Role of other organs in excretion",
  "Both are NCERT examples of organs other than the kidneys that help in excretion: the lungs remove CO₂ and water, "
  "and the liver eliminates substances through bile. The liver's bile has no bearing on what the lungs remove, so "
  "R does not explain A.",
  ["A: lungs remove ~200 mL CO₂ per minute and water → true",
   "R: bile contents → true", "Two separate organs and processes → R does not explain A"],
  R_EXC("role of other organs in excretion"),
  why_others_wrong="A links two unrelated facts; C and D call a true statement false.",
  seconds=35)

_o = ["(a) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)", "(a), (b) and (d) only"]
ms_check("abd", _o, "D")
Z(EXC, "Urine formation", "Intermediate", "multi_statement",
  ms("Which of the following statements about the functions of the renal tubule are correct?",
     ["The PCT is lined by simple cuboidal brush border epithelium, which increases the surface area for "
      "reabsorption.",
      "The PCT helps to maintain the pH and ionic balance of body fluids by selective secretion of H⁺, ammonia and "
      "K⁺ into the filtrate and absorption of HCO₃⁻ from it.",
      "Reabsorption in Henle's loop is the maximum of all segments of the tubule.",
      "The collecting duct helps to maintain the pH and ionic balance of blood by selective secretion of H⁺ and K⁺."]),
  _o, "D",
  "Function of the tubules",
  "The brush border of the PCT increases the surface for reabsorption, and the PCT secretes H⁺, NH₃ and K⁺ and "
  "absorbs HCO₃⁻. Reabsorption in Henle's loop is minimum; this region instead maintains the high osmolarity of "
  "the medullary interstitial fluid. The collecting duct also secretes H⁺ and K⁺ selectively.",
  ["(a) True", "(b) True", "(c) False: reabsorption in Henle's loop is minimum", "(d) True"],
  R_EXC("function of the tubules"),
  why_others_wrong="A leaves out (b) and (d) and includes (c); B and C include the false statement (c).",
  seconds=50)

Z(EXC, "Urine formation", "Intermediate", "direct",
  "Which of the following is reabsorbed from the glomerular filtrate by active transport?",
  ["Nitrogenous wastes", "Water in the initial segments of the nephron", "Glucose",
   "Ammonia secreted by the PCT"], "C",
  "Active and passive reabsorption",
  "Substances such as glucose, amino acids and Na⁺ are reabsorbed actively. Nitrogenous wastes are absorbed by "
  "passive transport, and water is reabsorbed passively in the initial segments of the nephron.",
  ["Active → glucose, amino acids, Na⁺", "Passive → nitrogenous wastes; water in initial segments"],
  R_EXC("urine formation: reabsorption"),
  why_others_wrong="Nitrogenous wastes and water move passively; ammonia is secreted into the filtrate, not "
                   "reabsorbed.",
  seconds=30)

Z(EXC, "Nephron structure", "Intermediate", "match_list",
  ml(("blood vessel", "description"),
     ["Afferent arteriole", "Efferent arteriole", "Peritubular capillaries", "Vasa recta"],
     ["Fine branch of the renal artery that forms the glomerulus", "U-shaped vessel running parallel to Henle's loop",
      "Carries blood away from the glomerulus", "Fine capillary network around the renal tubule"]),
  match_options(M("I", "III", "IV", "II"),
                [M("III", "I", "IV", "II"), M("I", "III", "II", "IV"), M("I", "IV", "III", "II")], at="A"),
  "A",
  "Blood supply of the nephron",
  "The glomerulus is a tuft of capillaries formed by the afferent arteriole, a fine branch of the renal artery. "
  "Blood leaves it through the efferent arteriole, which forms the peritubular capillaries around the renal tubule. "
  "A minute vessel of this network runs parallel to Henle's loop as the U-shaped vasa recta.",
  ["Afferent → forms glomerulus (I)", "Efferent → carries blood away (III)", "Peritubular → around tubule (IV)",
   "Vasa recta → U-shaped, parallel to Henle's loop (II)"],
  R_EXC("human excretory system: nephron"),
  why_others_wrong="The other codes swap the afferent and efferent arterioles, the peritubular network and vasa "
                   "recta, or the efferent arteriole and the peritubular network.",
  seconds=45)

Z(EXC, "Regulation of kidney function", "Intermediate", "direct",
  "Apart from increasing water reabsorption from the latter parts of the tubule, ADH can also increase the "
  "glomerular filtration rate. It does so by:",
  ["Dilating the afferent arteriole and lowering blood pressure",
   "Constricting blood vessels, which raises blood pressure and thereby glomerular blood flow",
   "Converting angiotensinogen into angiotensin I",
   "Stimulating the atrial walls to release ANF"], "B",
  "Effect of ADH on GFR",
  "NCERT: ADH can also affect kidney function through its constrictory effect on blood vessels. This raises blood "
  "pressure, and a rise in blood pressure can increase glomerular blood flow and thereby the GFR.",
  ["ADH → vasoconstriction → ↑ blood pressure", "↑ blood pressure → ↑ glomerular blood flow → ↑ GFR"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A gives the opposite effect; renin, not ADH, converts angiotensinogen; ANF is released by the "
                   "atria in response to increased blood flow, not by ADH.",
  seconds=35)

Z(EXC, "Modes of excretion", "Intermediate", "statement_pair",
  sp("Sweat produced by the sweat glands is a watery fluid containing NaCl, small amounts of urea, lactic acid and "
     "other substances.",
     "Sebaceous glands eliminate certain substances such as sterols, hydrocarbons and waxes through sebum."),
  STATEMENT_PAIR, "A",
  "Excretion through the skin",
  "Sweat is a watery fluid with NaCl, small amounts of urea and lactic acid; its main function is cooling, but it "
  "also removes some wastes. Sebum from sebaceous glands eliminates sterols, hydrocarbons and waxes and gives the "
  "skin a protective oily covering. Both statements are true.",
  ["Sweat composition → I true", "Sebum removes sterols, hydrocarbons, waxes → II true"],
  R_EXC("role of other organs in excretion"), seconds=30)

_o = ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (e) only", "(a), (c) and (e) only"]
ms_check("abce", _o, "C")
Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("Which of the following statements about the counter-current mechanism in the human kidney are correct?",
     ["The filtrate flows in opposite directions in the two limbs of Henle's loop.",
      "Blood flows through the two limbs of the vasa recta in a counter-current pattern.",
      "NaCl transported out by the ascending limb of Henle's loop is exchanged with the descending limb of the vasa "
      "recta.",
      "The mechanism maintains an osmolarity of the interstitium that increases towards the cortex.",
      "Small amounts of urea that enter the thin segment of the ascending limb are transported back to the "
      "interstitium by the collecting tubule."]),
  _o, "C",
  "Counter-current mechanism",
  "Henle's loop and the vasa recta each carry flows in opposite directions in their two limbs. NaCl from the "
  "ascending limb of Henle's loop is exchanged with the descending limb of the vasa recta and returned to the "
  "interstitium by its ascending portion; urea is recycled from the thin ascending segment via the collecting "
  "tubule. Together these maintain an osmolarity that increases towards the inner medulla, not the cortex.",
  ["(a) True", "(b) True", "(c) True", "(d) False: increases towards the inner medulla", "(e) True"],
  R_EXC("mechanism of concentration of the filtrate"),
  why_others_wrong="A and B include (d); D leaves out the true statement (b).",
  seconds=65)

Z(EXC, "Disorders and dialysis", "Advanced", "statement_pair",
  sp("In haemodialysis, blood drained from a convenient vein is pumped into the dialysing unit, and the cleared blood "
     "is returned to the body through an artery after adding anti-heparin.",
     "The dialysing fluid has the same composition as plasma, except for the nitrogenous wastes."),
  STATEMENT_PAIR, "D",
  "Haemodialysis",
  "In haemodialysis, blood is drained from a convenient artery, an anticoagulant such as heparin is added, and it "
  "is pumped into the dialysing unit; the cleared blood is pumped back through a vein after adding anti-heparin. "
  "Statement I reverses artery and vein, so it is false. The dialysing fluid matches plasma except that it lacks "
  "nitrogenous wastes, so these move out of the blood by concentration gradient (Statement II true).",
  ["Drained from an artery, returned through a vein → I false",
   "Dialysing fluid = plasma minus nitrogenous wastes → II true"],
  R_EXC("disorders of the excretory system: haemodialysis"), seconds=45)

Z(EXC, "Urine formation", "Advanced", "direct",
  "Which statement about the urine of a healthy adult human is correct?",
  ["It is slightly acidic (pH about 6.0), and on average 25–30 g of urea is excreted per day",
   "It is slightly alkaline (pH about 8.0), and on average 25–30 g of urea is excreted per day",
   "It is slightly acidic (pH about 6.0), and an adult excretes on average 5–6 L of it per day",
   "It normally contains glucose and ketone bodies in small amounts"], "A",
  "Composition and volume of urine",
  "An adult excretes on average 1–1.5 L of urine per day. It is a light yellow, watery, slightly acidic (pH 6.0) "
  "fluid with a characteristic odour, and on average 25–30 g of urea is excreted per day. Glucose (glycosuria) and "
  "ketone bodies (ketonuria) in urine indicate diabetes mellitus.",
  ["pH ≈ 6.0 (slightly acidic)", "Volume 1–1.5 L per day", "Urea 25–30 g per day",
   "Glucose, ketone bodies → abnormal (diabetes mellitus)"],
  R_EXC("micturition: composition of urine"),
  why_others_wrong="B gives an alkaline pH; C gives a daily volume far above 1–1.5 L; D describes the urine of a "
                   "diabetic, not a healthy person.",
  seconds=45)

_o = ["(a), (b) and (c) only", "(a) and (c) only", "(c) and (d) only", "(a), (c) and (d) only"]
ms_check("ac", _o, "B")
Z(EXC, "Nephron structure", "Advanced", "multi_statement",
  ms("Which of the following statements about the human kidney are correct?",
     ["The kidneys lie between the levels of the last thoracic and the third lumbar vertebra, close to the dorsal "
      "inner wall of the abdominal cavity.",
      "Each kidney of an adult weighs on average 1.2–1.7 kg.",
      "Inner to the hilum is a broad, funnel-shaped space called the renal pelvis, with projections called calyces.",
      "The ascending limb of Henle's loop continues as the proximal convoluted tubule."]),
  _o, "B",
  "Structure of the kidney and nephron",
  "The kidneys lie between the last thoracic and third lumbar vertebra near the dorsal inner wall of the abdominal "
  "cavity. Each adult kidney measures 10–12 cm × 5–7 cm × 2–3 cm and weighs on average 120–170 g, not kilograms. "
  "Inner to the hilum is the renal pelvis with calyces. The ascending limb of Henle's loop continues as the distal "
  "convoluted tubule (DCT); the PCT comes before Henle's loop.",
  ["(a) True", "(b) False: 120–170 g", "(c) True", "(d) False: continues as the DCT"],
  R_EXC("human excretory system"),
  why_others_wrong="A includes (b); C and D include (d).",
  seconds=55)


# ================================================================ Locomotion and Movement (B4 I6 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Types of movement", "Basic", "direct",
  "In the human body, amoeboid movement is shown by:",
  ["Skeletal muscle fibres", "Ciliated cells of the trachea", "Macrophages and leucocytes in blood",
   "Sperms"], "C",
  "Types of movement",
  "Cells of the human body show three main types of movement: amoeboid, ciliary and muscular. Specialised cells "
  "such as macrophages and leucocytes in blood show amoeboid movement, which is effected by pseudopodia formed by "
  "the streaming of protoplasm.",
  ["Amoeboid → macrophages, leucocytes", "Ciliary → trachea, female reproductive tract",
   "Muscular → limbs, jaws, tongue"],
  R_LOC("types of movement"),
  why_others_wrong="Skeletal muscle fibres show muscular movement; tracheal cilia show ciliary movement; sperms "
                   "swim with flagella.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "direct",
  "A single U-shaped bone present at the base of the buccal cavity, and included in the skull, is the:",
  ["Stapes", "Atlas", "Clavicle", "Hyoid"], "D",
  "Hyoid bone",
  "NCERT: a single U-shaped bone called the hyoid is present at the base of the buccal cavity, and it is also "
  "included in the skull.",
  ["U-shaped, base of buccal cavity → hyoid"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="The stapes is an ear ossicle, the atlas the first vertebra and the clavicle part of the "
                   "pectoral girdle.",
  seconds=20)

Z(LOC, "Joints", "Basic", "direct",
  "The flat bones of the skull fuse end-to-end with the help of dense fibrous connective tissue in the form of "
  "sutures, forming the cranium. This type of joint:",
  ["Is a fibrous joint and does not allow any movement", "Is a cartilaginous joint and permits limited movement",
   "Is a synovial joint and permits considerable movement", "Is a pivot joint and permits rotation"], "A",
  "Fibrous joints",
  "Fibrous joints do not allow any movement. The flat skull bones fuse end-to-end with dense fibrous connective "
  "tissue in the form of sutures to form the cranium.",
  ["Sutures of the cranium → fibrous joints → no movement"],
  R_LOC("joints"),
  why_others_wrong="Cartilaginous joints (between vertebrae) allow limited movement; synovial joints, including "
                   "pivot joints, allow considerable movement.",
  seconds=25)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "Muscles contribute about 40–50 per cent of the body weight of a human adult. In origin, muscle is a specialised "
  "tissue derived from the:",
  ["Ectoderm", "Mesoderm", "Endoderm", "Neural crest only"], "B",
  "Origin of muscle",
  "NCERT: muscle is a specialised tissue of mesodermal origin. About 40–50 per cent of the body weight of a human "
  "adult is contributed by muscles.",
  ["Muscle → mesodermal origin", "≈ 40–50 per cent of adult body weight"],
  R_LOC("muscle"),
  why_others_wrong="Ectoderm and endoderm give rise to other tissues; NCERT states the mesodermal origin of muscle.",
  seconds=20)

Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "The human axial skeleton consists of the skull (22 cranial and facial bones, plus the hyoid), three ear "
  "ossicles in each middle ear, 26 vertebrae, the sternum and 12 pairs of ribs. How many bones does the axial "
  "skeleton have?",
  ["74", "77", "80", "68"], "C",
  "Bones of the axial skeleton",
  "Add each group, remembering that ear ossicles occur in both ears and ribs occur in pairs.",
  ["Skull 22 + hyoid 1 = 23", "Ear ossicles: 2 × 3 = 6", "Vertebrae 26 + sternum 1 = 27", "Ribs: 12 × 2 = 24",
   "Total = 23 + 6 + 27 + 24 = 80"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="74 leaves out the ear ossicles; 77 counts the ossicles of one ear only; 68 counts 12 ribs "
                   "instead of 12 pairs.",
  seconds=50, verified_by=RECOMPUTED)

Z(LOC, "Skeletal system", "Intermediate", "statement_pair",
  sp("The sternum is a flat bone on the ventral midline of the thorax.",
     "Each rib has two articulation surfaces on its dorsal end and is therefore called bicephalic."),
  STATEMENT_PAIR, "A",
  "Sternum and ribs",
  "The sternum is a flat bone on the ventral midline of the thorax. Each rib is a thin flat bone connected dorsally "
  "to the vertebral column and ventrally to the sternum; it has two articulation surfaces on its dorsal end and is "
  "hence called bicephalic. Both statements are true.",
  ["Sternum: flat, ventral midline → I true", "Two dorsal articulation surfaces → bicephalic → II true"],
  R_LOC("skeletal system: axial skeleton"), seconds=30)

Z(LOC, "Muscular and skeletal disorders", "Intermediate", "match_list",
  ml(("disorder", "description"), ["Myasthenia gravis", "Muscular dystrophy", "Arthritis", "Osteoporosis"],
     ["Inflammation of joints", "Age-related decrease in bone mass with increased chances of fractures",
      "Autoimmune disorder affecting the neuromuscular junction",
      "Progressive degeneration of skeletal muscle, mostly due to a genetic disorder"]),
  match_options(M("III", "IV", "I", "II"),
                [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"), M("III", "I", "IV", "II")], at="D"),
  "D",
  "Disorders of the muscular and skeletal system",
  "Myasthenia gravis is an autoimmune disorder of the neuromuscular junction causing fatigue, weakening and "
  "paralysis of skeletal muscle. Muscular dystrophy is progressive degeneration of skeletal muscle, mostly genetic. "
  "Arthritis is inflammation of joints. Osteoporosis is an age-related fall in bone mass with more fractures; low "
  "oestrogen is a common cause.",
  ["Myasthenia gravis → III", "Muscular dystrophy → IV", "Arthritis → I", "Osteoporosis → II"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="The other codes swap the two muscle disorders, the two skeletal disorders, or muscular "
                   "dystrophy with arthritis.",
  seconds=45)

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("Skeletal muscles are also known as voluntary muscles.",
     "The activities of skeletal muscles are under the voluntary control of the nervous system."),
  ASSERTION_REASON, "A",
  "Skeletal muscle",
  "NCERT: skeletal muscles have a striped appearance and are called striated muscles; as their activities are under "
  "nervous system control, they are known as voluntary muscles too. R gives the reason for the name in A.",
  ["A: skeletal = voluntary → true", "R: under nervous control → true", "'As' links R to A → R explains A"],
  R_LOC("muscle"),
  why_others_wrong="B denies the stated link; C and D call a true statement false.",
  seconds=30)

_o = ["(a), (b) and (c) only", "(a), (c) and (d) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"]
ms_check("acd", _o, "B")
Z(LOC, "Muscle contraction", "Intermediate", "multi_statement",
  ms("Which of the following statements about the structure of skeletal muscle are correct?",
     ["Each muscle fibre is lined by a plasma membrane called the sarcolemma, which encloses the sarcoplasm.",
      "Each muscle fibre is uninucleate.",
      "The sarcoplasmic reticulum of muscle fibres is the store house of calcium ions.",
      "The muscle bundles (fascicles) of a skeletal muscle are held together by a common collagenous connective "
      "tissue layer called fascia.",
      "The portion of a myofibril between two successive M-lines is a sarcomere."]),
  _o, "B",
  "Structure of skeletal muscle",
  "A muscle is made of fascicles held together by fascia; each fibre is lined by the sarcolemma enclosing the "
  "sarcoplasm. The fibre is a syncytium because its sarcoplasm contains many nuclei. The sarcoplasmic reticulum "
  "stores Ca²⁺. A sarcomere is the portion of a myofibril between two successive Z-lines, not M-lines.",
  ["(a) True", "(b) False: syncytium, many nuclei", "(c) True", "(d) True", "(e) False: between two Z-lines"],
  R_LOC("muscle: structure of contractile proteins; skeletal muscle"),
  why_others_wrong="A includes (b) and leaves out (d); C and D include the false statement (e).",
  seconds=55)

Z(LOC, "Skeletal system", "Intermediate", "direct",
  "Which option correctly describes the acetabulum and the glenoid cavity?",
  ["Acetabulum: on the scapula, articulates with the head of the humerus; glenoid cavity: on the coxal bone, "
   "articulates with the thigh bone",
   "Acetabulum and glenoid cavity: both on the scapula, articulating with the clavicle",
   "Acetabulum: at the point of fusion of ilium, ischium and pubis, articulates with the humerus; glenoid cavity: "
   "below the acromion, articulates with the thigh bone",
   "Acetabulum: at the point of fusion of ilium, ischium and pubis, articulates with the thigh bone; glenoid "
   "cavity: below the acromion, articulates with the head of the humerus"], "D",
  "Girdles and their articulations",
  "Each coxal bone of the pelvic girdle is formed by the fusion of ilium, ischium and pubis; at their point of "
  "fusion is the acetabulum, to which the thigh bone articulates. Below the acromion of the scapula is a depression, "
  "the glenoid cavity, which articulates with the head of the humerus to form the shoulder joint.",
  ["Acetabulum → pelvic girdle → femur (hip)", "Glenoid cavity → scapula → humerus (shoulder joint)"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="A swaps the two cavities completely; B puts both on the scapula; C swaps the bones that "
                   "articulate.",
  seconds=45)

_o = ["(a), (c), (d) and (e) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(c), (d) and (e) only"]
ms_check("acde", _o, "A")
Z(LOC, "Muscle contraction", "Advanced", "multi_statement",
  ms("Which of the following statements about the cross-bridge cycle of muscle contraction are correct?",
     ["After the power stroke, the myosin head releases ADP and Pi and goes back to its relaxed state.",
      "During contraction, the I-bands lengthen while the A-bands shorten.",
      "The cross bridge pulls the attached actin filaments towards the centre of the A-band.",
      "The Z-lines attached to the actin filaments are pulled inwards, shortening the sarcomere.",
      "Binding of a new ATP molecule to the myosin head breaks the cross bridge."]),
  _o, "A",
  "Sliding filament mechanism",
  "The cross bridge pulls actin filaments towards the centre of the A-band; the Z-lines attached to them move "
  "inwards, so the sarcomere shortens. During shortening the I-bands get reduced while the A-bands retain their "
  "length. The myosin then releases ADP and Pi and returns to its relaxed state; a new ATP binds and the cross "
  "bridge is broken, and the cycle repeats.",
  ["(a) True", "(b) False: I-bands shorten, A-bands keep their length", "(c) True", "(d) True", "(e) True"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="B and C include (b); D leaves out the true statement (a).",
  seconds=65)

Z(LOC, "Skeletal system", "Advanced", "assertion_reason",
  ar("The vertebral column protects the spinal cord, supports the head and serves as the point of attachment for "
     "the ribs and the musculature of the back.",
     "The number of cervical vertebrae is seven in almost all mammals except human beings."),
  ASSERTION_REASON, "C",
  "Vertebral column",
  "A is an NCERT statement of the functions of the vertebral column. NCERT also states that the number of cervical "
  "vertebrae is seven in almost all mammals including human beings; R wrongly excludes humans, so R is false.",
  ["A: protects spinal cord, supports head, attachment for ribs and back muscles → true",
   "R: humans also have 7 cervical vertebrae → R false"],
  R_LOC("skeletal system: axial skeleton"),
  why_others_wrong="A and B need R to be true; D calls the true assertion false.",
  seconds=40)

Z(LOC, "Joints", "Advanced", "statement_pair",
  sp("The joint between adjacent vertebrae of the vertebral column is a fibrous joint and does not permit any "
     "movement.",
     "Synovial joints have a fluid-filled synovial cavity between the articulating surfaces of the two bones, which "
     "allows considerable movement."),
  STATEMENT_PAIR, "D",
  "Cartilaginous and synovial joints",
  "In cartilaginous joints the bones are joined by cartilage; the joint between adjacent vertebrae is of this type "
  "and permits limited movement, so Statement I is false. Synovial joints have a fluid-filled synovial cavity "
  "between the articulating surfaces and allow considerable movement, so Statement II is true.",
  ["Adjacent vertebrae → cartilaginous, limited movement → I false", "Synovial cavity → considerable movement → II "
   "true"],
  R_LOC("joints"), seconds=35)

Z(LOC, "Skeletal system", "Advanced", "direct",
  "Which statement about the bones of a human lower limb is correct?",
  ["Each lower limb has eight tarsals",
   "The femur is the longest bone of the body, and the patella is a cup-shaped bone that covers the knee ventrally",
   "The patella is a cup-shaped bone that covers the knee dorsally",
   "Each lower limb has five tarsals and seven metatarsals"], "B",
  "Bones of the lower limb",
  "Each lower limb has the femur (thigh bone, the longest bone), tibia and fibula, 7 tarsals, 5 metatarsals, 14 "
  "phalanges and the cup-shaped patella (knee cap), which covers the knee ventrally.",
  ["Femur → longest bone", "Tarsals 7, metatarsals 5, phalanges 14", "Patella → covers the knee ventrally"],
  R_LOC("skeletal system: appendicular skeleton"),
  why_others_wrong="8 is the number of carpals in the hand, not tarsals; the patella covers the knee ventrally; D "
                   "swaps the numbers of tarsals and metatarsals.",
  seconds=40)


# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "In insects, the neural system consists of:",
  ["A network of neurons only", "A brain along with a number of ganglia and neural tissues",
   "A brain and a spinal cord enclosed in a vertebral column", "A pair of cerebral ganglia without any nerves"], "B",
  "Neural system of insects",
  "NCERT: the neural organisation of lower invertebrates is very simple (e.g. Hydra, a network of neurons). In "
  "insects the neural system is better organised and consists of a brain along with a number of ganglia and neural "
  "tissues. Vertebrates have a more developed neural system.",
  ["Hydra → network of neurons", "Insects → brain + ganglia + neural tissues", "Vertebrates → brain and spinal cord"],
  R_NEU("neural system"),
  why_others_wrong="A describes Hydra; C describes vertebrates; D is not a description NCERT gives.",
  seconds=20)

Z(NEU, "Neuron and nerves", "Basic", "direct",
  "Bipolar neurons, with one axon and one dendrite, are found in the:",
  ["Cerebral cortex", "Embryonic stage", "Retina of the eye", "Neuromuscular junction"], "C",
  "Types of neurons",
  "By the number of axons and dendrites, neurons are multipolar (one axon, two or more dendrites; cerebral cortex), "
  "bipolar (one axon, one dendrite; retina of the eye) and unipolar (cell body with one axon only; usually in the "
  "embryonic stage).",
  ["Multipolar → cerebral cortex", "Bipolar → retina", "Unipolar → embryonic stage"],
  R_NEU("neuron as structural and functional unit of neural system"),
  why_others_wrong="The cerebral cortex has multipolar neurons; unipolar neurons occur in the embryonic stage; a "
                   "neuromuscular junction is a junction, not a neuron type's location in NCERT.",
  seconds=20)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The forebrain of humans consists of the:",
  ["Pons, cerebellum and medulla oblongata", "Cerebrum, thalamus and hypothalamus",
   "Corpora quadrigemina and cerebral aqueduct", "Cerebrum, pons and medulla oblongata"], "B",
  "Divisions of the brain",
  "The human brain is divided into forebrain, midbrain and hindbrain. The forebrain consists of the cerebrum, "
  "thalamus and hypothalamus.",
  ["Forebrain → cerebrum, thalamus, hypothalamus", "Midbrain → corpora quadrigemina; cerebral aqueduct passes "
   "through it", "Hindbrain → pons, cerebellum, medulla"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="A is the hindbrain; C belongs to the midbrain; D mixes forebrain and hindbrain parts.",
  seconds=20)

Z(NEU, "Neuron and nerves", "Basic", "direct",
  "Short fibres that branch repeatedly, project out of the cell body of a neuron, and transmit impulses towards the "
  "cell body are the:",
  ["Axon", "Synaptic knobs", "Myelin sheath", "Dendrites"], "D",
  "Parts of a neuron",
  "Dendrites are short, repeatedly branched fibres projecting from the cell body; they also contain Nissl's "
  "granules and transmit impulses towards the cell body. The axon is a long fibre that carries impulses away from "
  "the cell body to a synapse or a neuromuscular junction.",
  ["Dendrites → towards the cell body", "Axon → away from the cell body"],
  R_NEU("structure of a neuron"),
  why_others_wrong="The axon carries impulses away from the cell body; synaptic knobs are axon endings; the myelin "
                   "sheath is a covering, not a fibre.",
  seconds=20)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("Neurons are excitable cells.", "The membranes of neurons are in a polarised state."),
  ASSERTION_REASON, "A",
  "Excitability of neurons",
  "NCERT: neurons are excitable cells because their membranes are in a polarised state. Different types of ion "
  "channels in the membrane are selectively permeable, so a stimulus can change the polarisation. R is the stated "
  "reason for A.",
  ["A: neurons are excitable → true", "R: membranes polarised → true", "'Because' links R to A → R explains A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="B denies the link NCERT states with 'because'; C and D call a true statement false.",
  seconds=30)

_o = ["(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only", "(a), (b) and (c) only"]
ms_check("abce", _o, "C")
Z(NEU, "Nervous system divisions", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human neural system are correct?",
     ["The CNS includes the brain and the spinal cord and is the site of information processing and control.",
      "The PNS comprises all the nerves of the body associated with the CNS.",
      "The visceral nervous system is the part of the PNS through whose nerves, fibres, ganglia and plexuses "
      "impulses travel from the CNS to the viscera and from the viscera to the CNS.",
      "The autonomic neural system relays impulses from the CNS to the skeletal muscles.",
      "The somatic neural system relays impulses from the CNS to the skeletal muscles."]),
  _o, "C",
  "Divisions of the human neural system",
  "The CNS (brain and spinal cord) processes information and controls. The PNS includes all nerves associated "
  "with the CNS and has somatic and autonomic divisions. The somatic system relays impulses from the CNS to "
  "skeletal muscles; the autonomic system relays them to involuntary organs and smooth muscles. The visceral "
  "nervous system is part of the PNS linking the CNS and the viscera in both directions.",
  ["(a) True", "(b) True", "(c) True", "(d) False: autonomic → involuntary organs and smooth muscles", "(e) True"],
  R_NEU("human neural system"),
  why_others_wrong="A and B include (d); D leaves out the true statement (e).",
  seconds=55)

Z(NEU, "Nervous system divisions", "Intermediate", "statement_pair",
  sp("The cerebrum wraps around the medulla oblongata.", "The hypothalamus lies at the base of the thalamus."),
  STATEMENT_PAIR, "D",
  "Forebrain",
  "NCERT: the cerebrum wraps around a structure called the thalamus, a major coordinating centre for sensory and "
  "motor signalling; the medulla oblongata is part of the hindbrain. So Statement I is false. The hypothalamus lies "
  "at the base of the thalamus, so Statement II is true.",
  ["Cerebrum wraps around the thalamus → I false", "Hypothalamus at the base of the thalamus → II true"],
  R_NEU("central neural system: forebrain"), seconds=30)

Z(NEU, "Nervous system divisions", "Intermediate", "match_list",
  ml(("structure", "description"), ["Brain stem", "Pons", "Cerebral aqueduct", "Limbic system"],
     ["Canal passing through the midbrain", "Fibre tracts that interconnect different regions of the brain",
      "Formed by the midbrain, pons and medulla oblongata",
      "Along with the hypothalamus, regulates sexual behaviour, emotional reactions and motivation"]),
  match_options(M("III", "II", "I", "IV"),
                [M("II", "III", "I", "IV"), M("III", "I", "II", "IV"), M("III", "II", "IV", "I")], at="B"),
  "B",
  "Parts of the brain",
  "The midbrain, pons and medulla oblongata form the brain stem. The pons consists of fibre tracts that "
  "interconnect different regions of the brain. The cerebral aqueduct is a canal passing through the midbrain. The "
  "limbic system (inner parts of the cerebral hemispheres with amygdala, hippocampus and so on), along with the "
  "hypothalamus, regulates sexual behaviour, emotional reactions and motivation.",
  ["Brain stem → III", "Pons → II", "Cerebral aqueduct → I", "Limbic system → IV"],
  R_NEU("central neural system: forebrain, midbrain and hindbrain"),
  why_others_wrong="The other codes swap the brain stem with the pons, the pons with the aqueduct, or the aqueduct "
                   "with the limbic system.",
  seconds=45)

Z(NEU, "Neuron and nerves", "Intermediate", "direct",
  "In a myelinated nerve fibre, the gaps between two adjacent myelin sheaths are called:",
  ["Synaptic clefts", "Nissl's granules", "Nodes of Ranvier", "Synaptic knobs"], "C",
  "Myelinated nerve fibres",
  "Myelinated fibres are enveloped by Schwann cells, which form a myelin sheath around the axon. The gaps between "
  "two adjacent myelin sheaths are the nodes of Ranvier.",
  ["Myelin sheath from Schwann cells", "Gaps between adjacent sheaths → nodes of Ranvier"],
  R_NEU("structure of a neuron"),
  why_others_wrong="A synaptic cleft separates two neurons at a chemical synapse; Nissl's granules lie in the cell "
                   "body and dendrites; synaptic knobs are the bulb-like ends of axon branches.",
  seconds=25)

_o = ["(a) and (d) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)", "(a), (b) and (c) only"]
ms_check("abc", _o, "D")
Z(NEU, "Nerve impulse generation and conduction", "Advanced", "multi_statement",
  ms("Which of the following statements about a resting (polarised) axon are correct?",
     ["The axoplasm contains a high concentration of K⁺ and negatively charged proteins and a low concentration of "
      "Na⁺.",
      "The fluid outside the axon contains a low concentration of K⁺ and a high concentration of Na⁺.",
      "The resting axonal membrane is impermeable to the negatively charged proteins present in the axoplasm.",
      "The ionic gradients across the resting membrane are maintained by passive diffusion alone, without any use "
      "of energy."]),
  _o, "D",
  "Ionic basis of the resting potential",
  "Inside the axon, K⁺ and negatively charged proteins are high and Na⁺ is low; outside, K⁺ is low and Na⁺ is high. "
  "The membrane is impermeable to the negatively charged proteins of the axoplasm. The ionic gradients are "
  "maintained by the active transport of ions by the sodium-potassium pump (3 Na⁺ out for 2 K⁺ in), which uses "
  "energy.",
  ["(a) True", "(b) True", "(c) True", "(d) False: maintained by the Na⁺-K⁺ pump (active transport)"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A, B and C include the false statement (d); A and B also leave out true statements.",
  seconds=55)

Z(NEU, "Nervous system divisions", "Advanced", "assertion_reason",
  ar("The inner part of the cerebral hemisphere is called the white matter.",
     "The fibres of the tracts forming this part are covered with a myelin sheath, which gives the layer an opaque "
     "white appearance."),
  ASSERTION_REASON, "A",
  "Grey and white matter",
  "The cerebral cortex, with its cell bodies, is the grey matter. The inner part of the hemisphere is made of tract "
  "fibres covered with myelin sheath; this gives an opaque white appearance, hence the name white matter. R "
  "explains A.",
  ["A: inner part = white matter → true", "R: myelinated tract fibres look opaque white → true",
   "'Hence' links R to A → R explains A"],
  R_NEU("central neural system: forebrain"),
  why_others_wrong="B denies the stated link; C and D call a true statement false.",
  seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "statement_pair",
  sp("At a chemical synapse, the new potential developed in the post-synaptic neuron may be either excitatory or "
     "inhibitory.",
     "The neural system of all animals is composed of highly specialised cells called neurons, which can detect, "
     "receive and transmit different kinds of stimuli."),
  STATEMENT_PAIR, "A",
  "Synaptic transmission and neurons",
  "Neurotransmitters released at a chemical synapse bind to receptors on the post-synaptic membrane, opening ion "
  "channels; the new potential may be excitatory or inhibitory (Statement I true). NCERT also states that the "
  "neural system of all animals is made of neurons that detect, receive and transmit different kinds of stimuli "
  "(Statement II true).",
  ["Post-synaptic potential: excitatory or inhibitory → I true", "Neurons detect, receive, transmit stimuli → II true"],
  R_NEU("neural system; transmission of impulses"), seconds=35)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "direct",
  "Site A on an axon has just been stimulated, and site B, immediately ahead of it, is still at rest. Which "
  "statement about the charges and the local current between the two sites is correct?",
  ["At A the inner surface is negative and at B it is positive; current flows on the inner surface from B to A",
   "At A the inner surface is positive and at B it is negative; current flows on the inner surface from A to B and "
   "on the outer surface from B to A",
   "At A the inner surface is positive and at B it is negative; current flows on both the inner and the outer "
   "surface from A to B",
   "At A and at B the inner surface is positive; no current flows between them"], "B",
  "Conduction of the nerve impulse",
  "At the stimulated site A, Na⁺ influx reverses the polarity: the outer surface becomes negative and the inner "
  "surface positive. At site B, still at rest, the outer surface is positive and the inner negative. So current "
  "flows on the inner surface from A to B, and on the outer surface from B to A, completing the circuit. This "
  "depolarises B, and the impulse moves along the axon.",
  ["Site A (stimulated): inside +, outside −", "Site B (resting): inside −, outside +",
   "Inner current A → B; outer current B → A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A reverses the charges; C ignores that the circuit is completed in the opposite direction on "
                   "the outer surface; D treats the resting site as depolarised.",
  seconds=55)


# ---------------------------------------------------------------- checks and output
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_002_ZOO_p1.json"


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
    assert pkg["output"] == "batches/parts/BATCH_002_ZOO_p1.json"
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "BATCH_002 package ZOO_002_p1: 123 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, and Neural "
                    "Control and Coordination. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "facts already tested in BATCH_001; every numerical answer re-derived by "
                    "tools/batch_002/ZOO_002_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
