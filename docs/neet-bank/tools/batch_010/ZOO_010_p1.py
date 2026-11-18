"""Writes batches/parts/BATCH_010_ZOO_p1.json: package ZOO_010_p1 of BATCH_010 (Zoology, 131 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement; Neural Control and Coordination;
Chemical Coordination and Integration. IDs NEET_ZOO_002251 .. NEET_ZOO_002381. Every numerical answer is re-derived
below before the file is written, and the plan quota, ID range, subtopics, key balance and format mix are asserted.
Facts follow the rationalised NCERT Class 11 Biology textbook; for the frog only the digestive, circulatory,
respiratory, nervous and reproductive systems, and no earthworm or cockroach anatomy. Facts already tested in
BATCH_000 to BATCH_009 (see `merge_batch.py stems 10 ZOO_010_p1`) are not asked again in the same way; most items are
application, identification, counting or comparison questions that combine NCERT statements in new ways.

    python docs/neet-bank/tools/batch_010/ZOO_010_p1.py
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
PACKAGE = "ZOO_010_p1"
BATCH = "BATCH_010"
FIRST_ID, LAST_ID = 2251, 2381
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
CCI = "Chemical Coordination and Integration"


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


def count_check(items: dict, options: list, answer: str):
    """For 'how many of the following' items: asserts the keyed option is the number of items marked True."""
    n = sum(1 for v in items.values() if v)
    assert options[LETTERS.index(answer)] == str(n) or options[LETTERS.index(answer)].startswith(f"{n} "), (n, options)


# ---------------------------------------------------------------- questions
# ================================================================ Animal Kingdom (B6 I8 A6)
R_AK = lambda s: ref("Animal Kingdom", s)

Z(AK, "Chordate classes", "Basic", "direct",
  "In which of the following fishes are the gill slits separate and NOT covered by an operculum?",
  ["Labeo", "Pristis", "Catla", "Exocoetus"], "B",
  "Gill slits of cartilaginous and bony fishes",
  "NCERT: in Chondrichthyes the gill slits are separate and without an operculum (gill cover); Pristis (saw fish) "
  "is a cartilaginous fish. In Osteichthyes – Labeo (Rohu), Catla (Katla) and Exocoetus (flying fish) – there are "
  "four pairs of gills covered by an operculum on each side.",
  ["Pristis → Chondrichthyes → separate gill slits, no operculum",
   "Labeo, Catla, Exocoetus → Osteichthyes → gills covered by an operculum"],
  R_AK("class Chondrichthyes; class Osteichthyes"),
  why_others_wrong="A, C and D are bony fishes, whose gills are covered by an operculum.",
  seconds=25)

Z(AK, "Chordate classes", "Basic", "direct",
  "NCERT notes that in one vertebrate class the eyes have eyelids and a tympanum represents the ear. Which of the "
  "following animals belongs to that class?",
  ["Labeo", "Petromyzon", "Hippocampus", "Bufo"], "D",
  "Eyes and ear of amphibians",
  "In its account of class Amphibia NCERT states that the eyes have eyelids and a tympanum represents the ear. Bufo "
  "(toad) is an amphibian. Labeo and Hippocampus are bony fishes and Petromyzon is a cyclostome.",
  ["Eyelids + tympanum → described for Amphibia", "Bufo → Amphibia"],
  R_AK("class Amphibia"),
  why_others_wrong="A and C are bony fishes and B is a jawless cyclostome; none belongs to class Amphibia.",
  seconds=25)

Z(AK, "Chordate classes", "Basic", "direct",
  "In amphibians, the alimentary canal, the urinary tract and the reproductive tract all open into a common chamber "
  "that opens to the exterior. NCERT calls this chamber the:",
  ["Mantle cavity", "Spongocoel", "Cloaca", "Gastro-vascular cavity"], "C",
  "Cloaca of amphibians",
  "NCERT: in amphibians the alimentary canal, urinary and reproductive tracts open into a common chamber called the "
  "cloaca, which opens to the exterior. The mantle cavity belongs to molluscs, the spongocoel to sponges and the "
  "gastro-vascular cavity to coelenterates.",
  ["Common chamber for gut, urinary and reproductive tracts → cloaca"],
  R_AK("class Amphibia"),
  why_others_wrong="A is the space between the visceral hump and the mantle of molluscs; B is the central cavity of "
                   "sponges; D is the single-opening digestive cavity of coelenterates.",
  seconds=20)

Z(AK, "Chordate classes", "Basic", "statement_pair",
  sp("In cartilaginous fishes, the skin is tough and contains minute placoid scales.",
     "In bony fishes, the skin is covered with cycloid or ctenoid scales."),
  STATEMENT_PAIR, "A",
  "Body covering of the two classes of fishes",
  "NCERT: in Chondrichthyes the skin is tough, containing minute placoid scales (the teeth are modified placoid "
  "scales). In Osteichthyes the skin is covered with cycloid/ctenoid scales.",
  ["Statement I → true (Chondrichthyes)", "Statement II → true (Osteichthyes)"],
  R_AK("class Chondrichthyes; class Osteichthyes"),
  why_others_wrong="B, C and D each reject at least one of two correct NCERT descriptions.",
  seconds=30)

Z(AK, "Basis of classification", "Basic", "assertion_reason",
  ar("Aschelminthes such as Ascaris are called pseudocoelomates.",
     "In them the body cavity is not lined by mesoderm; instead, the mesoderm is present as scattered pouches in "
     "between the ectoderm and the endoderm."),
  ASSERTION_REASON, "A",
  "Pseudocoelom",
  "NCERT: in some animals the body cavity is not lined by mesoderm; instead the mesoderm is present as scattered "
  "pouches in between the ectoderm and endoderm. Such a body cavity is called a pseudocoelom and these animals are "
  "called pseudocoelomates, e.g., aschelminthes. R gives the very feature that defines a pseudocoelom, so it "
  "explains A.",
  ["A → true (aschelminthes are pseudocoelomates)", "R → true (definition of pseudocoelom)",
   "The name follows from the unlined body cavity → R explains A"],
  R_AK("basis of classification – coelom"),
  why_others_wrong="B denies the defining link; C and D reject statements that NCERT makes.",
  seconds=30)

Z(AK, "Chordate classes", "Basic", "match_list",
  ml(("animal", "body covering"), ["Scoliodon", "Catla", "Calotes", "Columba"],
     ["Feathers", "Dry, cornified skin with epidermal scales or scutes", "Tough skin with minute placoid scales",
      "Cycloid or ctenoid scales"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "D"), "D",
  "Body coverings across vertebrate classes",
  "Scoliodon (dog fish) is a cartilaginous fish – tough skin with minute placoid scales. Catla is a bony fish – "
  "cycloid/ctenoid scales. Calotes (garden lizard) is a reptile – dry, cornified skin with epidermal scales or "
  "scutes. Columba (pigeon) is a bird – feathers.",
  ["Scoliodon → III", "Catla → IV", "Calotes → II", "Columba → I"],
  R_AK("classes Chondrichthyes, Osteichthyes, Reptilia and Aves"),
  why_others_wrong="A swaps the two fishes; B swaps the reptile and the bird; C swaps the bony fish and the reptile.",
  seconds=35)

_opts = ["(a), (b), (c) and (e) only", "(a), (b) and (c) only", "(a) and (d) only", "(b), (c) and (d) only"]
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements are true of BOTH Echinodermata (e.g., Asterias) and Chordata, according to "
     "NCERT?",
     ["They are triploblastic.", "They are coelomate.", "They show the organ-system level of organisation.",
      "They possess a water vascular system.", "The adults are bilaterally symmetrical."]),
  _opts, "B",
  "Echinoderms compared with chordates",
  "NCERT: echinoderms are triploblastic and coelomate animals with the organ-system level of organisation; the "
  "adults are radially symmetrical (larvae bilateral), and the water vascular system is their most distinctive "
  "feature. Chordates are bilaterally symmetrical, triploblastic, coelomate, with organ-system level of organisation, "
  "and have no water vascular system.",
  ["(a) true for both", "(b) true for both", "(c) true for both",
   "(d) false – only echinoderms have a water vascular system",
   "(e) false – adult echinoderms are radially symmetrical"],
  R_AK("phylum Echinodermata; phylum Chordata"),
  why_others_wrong="A adds (e); C and D add (d), which is unique to echinoderms.",
  seconds=50)
ms_check("abc", _opts, "B")

Z(AK, "Non-chordate phyla", "Intermediate", "assertion_reason",
  ar("Pila and Octopus are both placed in phylum Mollusca.",
     "Mollusca is the second largest animal phylum."),
  ASSERTION_REASON, "B",
  "Members of Mollusca",
  "NCERT lists Pila (apple snail) and Octopus (devil fish) among its examples of molluscs, so A is true. NCERT also "
  "calls Mollusca the second largest animal phylum, so R is true. But the size of the phylum has nothing to do with "
  "why these two animals belong to it; that depends on their features (calcareous shell, mantle, muscular foot, "
  "visceral hump, radula). R does not explain A.",
  ["A → true", "R → true", "Size of the phylum is not the basis for placing an animal in it → R does not explain A"],
  R_AK("phylum Mollusca"),
  why_others_wrong="A treats a statement about phylum size as the reason for classification; C and D reject true "
                   "statements.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("In arthropods, the body is covered by a chitinous exoskeleton.",
     "In arthropods, excretion takes place through nephridia."),
  STATEMENT_PAIR, "C",
  "Exoskeleton and excretory organs of arthropods",
  "NCERT: the body of arthropods is covered by a chitinous exoskeleton, and excretion takes place through Malpighian "
  "tubules. Nephridia are the excretory organs of annelids.",
  ["Statement I → true", "Statement II → false: arthropods excrete through Malpighian tubules"],
  R_AK("phylum Arthropoda; phylum Annelida"),
  why_others_wrong="A and D give arthropods the annelid excretory organ; B rejects the true Statement I.",
  seconds=30)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("animal", "development as described by NCERT for its phylum"), ["Sycon", "Taenia", "Asterias", "Locusta"],
     ["Development may be direct or indirect", "Indirect, with a free-swimming larva",
      "Indirect, with a larval stage morphologically distinct from the adult", "Through many larval stages"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("II", "IV", "III", "I")], "C"), "C",
  "Patterns of development in non-chordates",
  "NCERT: in sponges (Sycon) development is indirect, having a larval stage that is morphologically distinct from the "
  "adult; in Platyhelminthes (Taenia) development is through many larval stages; in echinoderms (Asterias) "
  "development is indirect with a free-swimming larva; in arthropods (Locusta) development may be direct or indirect.",
  ["Sycon → III", "Taenia → IV", "Asterias → II", "Locusta → I"],
  R_AK("phyla Porifera, Platyhelminthes, Echinodermata and Arthropoda"),
  why_others_wrong="A swaps the sponge and the flatworm; B swaps the echinoderm and the arthropod; D swaps the sponge "
                   "and the echinoderm.",
  seconds=45)

Z(AK, "Chordate classes", "Intermediate", "direct",
  "Which of the following animals has, according to NCERT's description of its class, a three-chambered heart, "
  "internal fertilisation and direct development?",
  ["Chameleon", "Hyla", "Crocodilus", "Bufo"], "A",
  "Reptiles compared with amphibians and crocodiles",
  "Chameleon (tree lizard) is a reptile: the heart is usually three-chambered, fertilisation is internal and "
  "development is direct. Crocodilus is also a reptile but NCERT notes its heart is four-chambered. Hyla (tree frog) "
  "and Bufo (toad) are amphibians with a three-chambered heart but external fertilisation and indirect development.",
  ["Reptilia → 3-chambered heart (except crocodiles), internal fertilisation, direct development",
   "Amphibia → external fertilisation, indirect development", "→ Chameleon"],
  R_AK("class Amphibia; class Reptilia"),
  why_others_wrong="B and D are amphibians (external fertilisation, indirect development); C has a four-chambered "
                   "heart.",
  seconds=40)

_opts = ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only", "(a), (b) and (c) only"]
Z(AK, "Chordate classes", "Intermediate", "multi_statement",
  ms("Which of the following statements are true of BOTH class Reptilia and class Aves, according to NCERT?",
     ["The sexes are separate.", "Fertilisation is internal.", "They are oviparous and development is direct.",
      "They are homoiothermous (warm-blooded).", "The heart is completely four-chambered in all members."]),
  _opts, "D",
  "Reptiles compared with birds",
  "NCERT: in reptiles the sexes are separate, fertilisation is internal, they are oviparous and development is direct; "
  "they are poikilotherms and the heart is usually three-chambered (four-chambered in crocodiles). In birds the "
  "sexes are separate, fertilisation is internal, they are oviparous and development is direct; they are "
  "warm-blooded and the heart is completely four-chambered.",
  ["(a) true for both", "(b) true for both", "(c) true for both", "(d) false – reptiles are poikilotherms",
   "(e) false – most reptiles have a three-chambered heart"],
  R_AK("class Reptilia; class Aves"),
  why_others_wrong="A, B and C include (d) or (e), which hold for birds but not for reptiles in general.",
  seconds=50)
ms_check("abc", _opts, "D")

_items = {"Ancylostoma": False, "Hirudinaria": True, "Pila": True, "Taenia": False, "Asterias": True,
          "Balanoglossus": True, "Wuchereria": False, "Branchiostoma": True}
_opts = ["3", "4", "5", "6"]
Z(AK, "Basis of classification", "Intermediate", "direct",
  "How many of the following animals are coelomates, i.e. have a body cavity lined by mesoderm?\n\n"
  + ", ".join(_items),
  _opts, "C",
  "Coelomates, pseudocoelomates and acoelomates",
  "NCERT: annelids, molluscs, arthropods, echinoderms, hemichordates and chordates are coelomates; aschelminthes are "
  "pseudocoelomates; platyhelminthes are acoelomates. Hirudinaria (annelid), Pila (mollusc), Asterias (echinoderm), "
  "Balanoglossus (hemichordate) and Branchiostoma (chordate) are coelomates. Ancylostoma and Wuchereria "
  "(aschelminthes) are pseudocoelomates, and Taenia (platyhelminth) is acoelomate.",
  ["Coelomates → Hirudinaria, Pila, Asterias, Balanoglossus, Branchiostoma = 5",
   "Pseudocoelomates → Ancylostoma, Wuchereria", "Acoelomate → Taenia"],
  R_AK("basis of classification – coelom"),
  why_others_wrong="A and B leave out some coelomates (often the hemichordate or the cephalochordate); D counts a "
                   "pseudocoelomate roundworm as coelomate.",
  seconds=50)
count_check(_items, _opts, "C")

Z(AK, "Chordate classes", "Intermediate", "statement_pair",
  sp("In birds, the forelimbs are modified into wings, and the hind limbs generally have scales.",
     "In birds, the skin is rich in glands."),
  STATEMENT_PAIR, "C",
  "Limbs and skin of birds",
  "NCERT: in class Aves the forelimbs are modified into wings, and the hind limbs generally have scales and are "
  "modified for walking, swimming or clasping the tree branches. The skin is dry and without glands except the oil "
  "gland at the base of the tail.",
  ["Statement I → true", "Statement II → false: the skin is dry and has no glands except the oil gland"],
  R_AK("class Aves"),
  why_others_wrong="A and D accept a glandular skin in birds; B rejects the true Statement I.",
  seconds=30)

_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (c), (d) and (e) only",
         "(a), (c) and (e) only"]
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("Which of the following correctly contrast a cartilaginous fish (first) with a bony fish (second), according to "
     "NCERT?",
     ["Mouth located ventrally – mouth mostly terminal",
      "Gill slits separate and without operculum – four pairs of gills covered by an operculum on each side",
      "Air bladder absent – air bladder present",
      "Cartilaginous endoskeleton – bony endoskeleton",
      "Two-chambered heart – three-chambered heart"]),
  _opts, "A",
  "Chondrichthyes contrasted with Osteichthyes",
  "NCERT: Chondrichthyes have a ventral mouth, separate gill slits without an operculum, no air bladder (so they "
  "swim constantly to avoid sinking) and a cartilaginous endoskeleton. Osteichthyes have a mostly terminal mouth, "
  "four pairs of gills covered by an operculum, an air bladder that regulates buoyancy and a bony endoskeleton. In "
  "both classes the heart is two-chambered (one auricle and one ventricle), so (e) is wrong.",
  ["(a) correct", "(b) correct", "(c) correct", "(d) correct", "(e) wrong – both have a two-chambered heart"],
  R_AK("class Chondrichthyes; class Osteichthyes"),
  why_others_wrong="B leaves out the correct (d); C and D include (e).",
  seconds=60)
ms_check("abcd", _opts, "A")

Z(AK, "Basis of classification", "Advanced", "assertion_reason",
  ar("Neither Sycon nor Hydra has organs, i.e. tissues grouped together to form organs.",
     "In both Sycon and Hydra, the cells are arranged as loose cell aggregates."),
  ASSERTION_REASON, "C",
  "Cellular and tissue levels of organisation",
  "NCERT: sponges (Sycon) show the cellular level of organisation, the cells being arranged as loose cell aggregates. "
  "Coelenterates (Hydra) show the tissue level: cells performing the same function are arranged into tissues. The "
  "organ level begins with Platyhelminthes. So A is true – neither has organs – but R is false, because Hydra's cells "
  "are organised into tissues, not loose aggregates.",
  ["Sycon → cellular level (no tissues, no organs)", "Hydra → tissue level (no organs)", "A → true",
   "R → false for Hydra"],
  R_AK("basis of classification – levels of organisation"),
  why_others_wrong="A and B accept R, which holds only for the sponge; D rejects A, which is true for both animals.",
  seconds=45)

Z(AK, "Non-chordate phyla", "Advanced", "match_list",
  ml(("animal", "pair of features"), ["Ctenoplana", "Obelia", "Planaria", "Ancylostoma"],
     ["Triploblastic and pseudocoelomate; an excretory tube removes body wastes through the excretory pore",
      "Triploblastic and acoelomate; flame cells help in osmoregulation and excretion",
      "Diploblastic; polyp and medusa forms alternate (metagenesis)",
      "Diploblastic; eight external rows of ciliated comb plates, and reproduction only by sexual means"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Combining two diagnostic features per phylum",
  "Ctenoplana is a ctenophore: diploblastic, with eight external rows of ciliated comb plates, and only sexual "
  "reproduction. Obelia is a coelenterate showing metagenesis (polyps produce medusae asexually and medusae form "
  "polyps sexually). Planaria is a flatworm: triploblastic, acoelomate, with flame cells. Ancylostoma (hookworm) is an "
  "aschelminth: triploblastic, pseudocoelomate, with an excretory tube opening through an excretory pore.",
  ["Ctenoplana → IV", "Obelia → III", "Planaria → II", "Ancylostoma → I"],
  R_AK("phyla Coelenterata, Ctenophora, Platyhelminthes and Aschelminthes"),
  why_others_wrong="A swaps the two diploblastic animals; C swaps the two triploblastic worms; D swaps Obelia and "
                   "Planaria.",
  seconds=60)

_items = {"Chelone": True, "Columba": True, "Pteropus": False, "Bufo": False, "Ornithorhynchus": True,
          "Asterias": False, "Naja": True, "Pavo": True}
_opts = ["2", "3", "4", "5"]
Z(AK, "Chordate classes", "Advanced", "direct",
  "Going by NCERT's description of each animal's class (and NCERT's note on egg-laying mammals), how many of the "
  "following animals are oviparous AND show direct development?\n\n" + ", ".join(_items),
  _opts, "D",
  "Oviparity and type of development across classes",
  "Reptiles (Chelone, Naja) and birds (Columba, Pavo) are oviparous with direct development. Mammals are viviparous "
  "with a few exceptions and development is direct; NCERT gives Ornithorhynchus as the oviparous mammal, so it too "
  "lays eggs with direct development. Pteropus is a viviparous mammal. Bufo (amphibian) and Asterias (echinoderm) show "
  "indirect development.",
  ["Oviparous + direct → Chelone, Naja, Columba, Pavo, Ornithorhynchus = 5",
   "Pteropus → viviparous", "Bufo, Asterias → indirect development"],
  R_AK("classes Reptilia, Aves and Mammalia; phylum Echinodermata; class Amphibia"),
  why_others_wrong="A, B and C each miss egg-laying animals – most often Ornithorhynchus, the oviparous mammal.",
  seconds=60)
count_check(_items, _opts, "D")

Z(AK, "Chordate classes", "Advanced", "statement_pair",
  sp("Every member of division Agnatha has a bony cranium.",
     "Every member of super class Pisces has a bony endoskeleton."),
  STATEMENT_PAIR, "B",
  "Skeleton in Agnatha and Pisces",
  "NCERT: division Agnatha is represented by class Cyclostomata, whose cranium and vertebral column are "
  "cartilaginous – so Statement I is false. Super class Pisces includes Chondrichthyes, whose endoskeleton is "
  "cartilaginous, as well as Osteichthyes with a bony endoskeleton – so Statement II is false too.",
  ["Statement I → false (cyclostome cranium is cartilaginous)",
   "Statement II → false (Chondrichthyes in Pisces have a cartilaginous endoskeleton)"],
  R_AK("subphylum Vertebrata; classes Cyclostomata, Chondrichthyes and Osteichthyes"),
  why_others_wrong="A accepts both errors; C forgets that cyclostomes are cartilaginous; D forgets the cartilaginous "
                   "fishes inside Pisces.",
  seconds=45)

Z(AK, "Chordate classes", "Advanced", "assertion_reason",
  ar("Branchiostoma is a chordate but not a vertebrate.",
     "In Branchiostoma the notochord extends from head to tail and persists throughout life; it is not replaced by a "
     "vertebral column."),
  ASSERTION_REASON, "A",
  "Chordates versus vertebrates",
  "NCERT: in vertebrates the notochord is replaced by a cartilaginous or bony vertebral column in the adult, which is "
  "why all vertebrates are chordates but not all chordates are vertebrates. Branchiostoma (a cephalochordate) has a "
  "notochord from head to tail that persists throughout life and is never replaced by a vertebral column. It is "
  "therefore a chordate (it has a notochord) but not a vertebrate – R explains A.",
  ["A → true", "R → true", "No vertebral column replaces the notochord → not a vertebrate → R explains A"],
  R_AK("phylum Chordata – subphyla Cephalochordata and Vertebrata"),
  why_others_wrong="B misses the direct link; C and D reject statements that NCERT makes.",
  seconds=40)


# ================================================================ Structural Organisation in Animals (B4 I5 A4)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Frog: morphology and anatomy", "Basic", "direct",
  "In the brain of the frog, the fore-brain includes the olfactory lobes, the paired cerebral hemispheres and an "
  "unpaired:",
  ["Optic lobe", "Diencephalon", "Cerebellum", "Medulla oblongata"], "B",
  "Divisions of the frog brain",
  "NCERT: the frog brain is divided into fore-brain, mid-brain and hind-brain. The fore-brain includes the olfactory "
  "lobes, the paired cerebral hemispheres and the unpaired diencephalon. The mid-brain is characterised by a pair of "
  "optic lobes; the hind-brain consists of the cerebellum and the medulla oblongata.",
  ["Fore-brain → olfactory lobes + paired cerebral hemispheres + unpaired diencephalon"],
  R_SOA("frogs – neural system"),
  why_others_wrong="A belongs to the mid-brain (and is paired); C and D form the hind-brain.",
  seconds=25)

Z(SOA, "Animal tissues", "Basic", "statement_pair",
  sp("Smooth muscle fibres are held together by cell junctions and are bundled together in a connective tissue "
     "sheath.",
     "The walls of blood vessels contain smooth muscle tissue."),
  STATEMENT_PAIR, "A",
  "Smooth muscle",
  "NCERT: the smooth muscle fibres taper at both ends (fusiform) and do not show striations. Cell junctions hold them "
  "together and they are bundled together in a connective tissue sheath. The wall of internal organs such as the "
  "blood vessels, stomach and intestine contains this type of muscle tissue.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("animal tissues – muscle tissue"),
  why_others_wrong="B, C and D reject at least one of two correct NCERT statements.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Basic", "assertion_reason",
  ar("In the frog, fats are emulsified in the duodenum.",
     "The duodenum receives bile from the gall bladder through a common bile duct, and bile emulsifies fat."),
  ASSERTION_REASON, "A",
  "Fat digestion in the frog",
  "NCERT: the duodenum receives bile from the gall bladder and pancreatic juices from the pancreas through a common "
  "bile duct. Bile emulsifies fat and pancreatic juices digest carbohydrates and proteins. Fat is emulsified in the "
  "duodenum precisely because bile arrives there – R explains A.",
  ["A → true", "R → true", "Bile reaches the duodenum and emulsifies fat → R explains A"],
  R_SOA("frogs – digestive system"),
  why_others_wrong="B misses the direct link; C and D reject statements that NCERT makes.",
  seconds=30)

Z(SOA, "Animal tissues", "Basic", "match_list",
  ml(("cell", "tissue in which NCERT describes it"), ["Mast cells", "Chondrocytes", "Osteocytes", "Neuroglia"],
     ["Neural tissue", "Bone", "Areolar tissue", "Cartilage"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "II", "IV", "I"),
                                            M("III", "IV", "I", "II")], "C"), "C",
  "Cells of different tissues",
  "NCERT: areolar tissue contains fibroblasts, macrophages and mast cells; cartilage cells (chondrocytes) are enclosed "
  "in small cavities within the matrix; bone cells (osteocytes) lie in spaces called lacunae; neuroglial cells protect "
  "and support the neurons of neural tissue.",
  ["Mast cells → areolar tissue (III)", "Chondrocytes → cartilage (IV)", "Osteocytes → bone (II)",
   "Neuroglia → neural tissue (I)"],
  R_SOA("animal tissues – connective tissue; neural tissue"),
  why_others_wrong="A swaps areolar tissue and cartilage; B swaps cartilage and bone; D swaps bone and neural tissue.",
  seconds=30)

_opts = ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (d) only", "(a), (b) and (d) only"]
Z(SOA, "Frog: morphology and anatomy", "Intermediate", "multi_statement",
  ms("Which of the following statements about the lungs and heart of the frog are correct, according to NCERT?",
     ["The lungs are a pair of elongated, pink-coloured, sac-like structures in the upper part of the trunk region "
      "(thorax).",
      "The heart is a muscular structure situated in the upper part of the body cavity.",
      "The heart has two atria and two ventricles.",
      "The ventricle opens into a sac-like conus arteriosus on the ventral side of the heart.",
      "The sinus venosus joins the left atrium."]),
  _opts, "D",
  "Lungs and heart of the frog",
  "NCERT: the lungs are a pair of elongated, pink-coloured sac-like structures in the upper part of the trunk region "
  "(thorax). The heart is a muscular structure in the upper part of the body cavity with three chambers – two atria "
  "and one ventricle. A triangular sinus venosus joins the RIGHT atrium, and the ventricle opens into a sac-like "
  "conus arteriosus on the ventral side of the heart.",
  ["(a) true", "(b) true", "(c) false – one ventricle", "(d) true", "(e) false – sinus venosus joins the right atrium"],
  R_SOA("frogs – respiratory and circulatory systems"),
  why_others_wrong="A includes (c); B includes (e); C leaves out the correct (b).",
  seconds=50)
ms_check("abd", _opts, "D")

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "According to NCERT, glandular epithelium is formed when some of the cells of which kinds of epithelium become "
  "specialised for secretion?",
  ["Squamous or compound epithelium", "Columnar or cuboidal epithelium", "Squamous epithelium only",
   "Compound epithelium only"], "B",
  "Origin of glandular epithelium",
  "NCERT: some of the columnar or cuboidal cells get specialised for secretion and are called glandular epithelium. "
  "Such glands may be unicellular (goblet cells of the alimentary canal) or multicellular (salivary gland). Squamous "
  "epithelium forms a diffusion boundary, and compound epithelium has only a limited role in secretion.",
  ["Glandular epithelium ← specialised columnar or cuboidal cells"],
  R_SOA("animal tissues – epithelial tissue"),
  why_others_wrong="A, C and D name squamous or compound epithelium, which NCERT describes as a diffusion boundary or "
                   "as protective, not as the source of glandular cells.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "statement_pair",
  sp("In the male frog, the cloaca is used to pass faecal matter, urine and sperms to the exterior.",
     "In the female frog, the oviducts arising from the ovaries open into the cloaca separately."),
  STATEMENT_PAIR, "A",
  "Cloaca and genital ducts of the frog",
  "NCERT: the cloaca is a small, median chamber that is used to pass faecal matter, urine and sperms to the exterior "
  "(male). In the female, the ovaries have no functional connection with the kidneys, and a pair of oviducts arising "
  "from the ovaries opens into the cloaca separately.",
  ["Statement I → true", "Statement II → true"],
  R_SOA("frogs – reproductive system"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("The lymph of the frog differs from its blood in lacking RBCs.",
     "The RBCs of the frog are nucleated and contain a red-coloured pigment, haemoglobin."),
  ASSERTION_REASON, "B",
  "Blood and lymph of the frog",
  "NCERT: the lymph is different from blood – it lacks a few proteins and the RBCs. Separately, NCERT states that the "
  "frog's RBCs are nucleated and contain the red pigment haemoglobin. Whether RBCs have a nucleus has nothing to do "
  "with their absence from lymph, so R does not explain A.",
  ["A → true", "R → true", "A nucleus in the RBC is unrelated to the RBC's absence from lymph → R does not explain A"],
  R_SOA("frogs – circulatory system"),
  why_others_wrong="A forges a link NCERT does not make; C and D reject true statements.",
  seconds=35)

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("structure", "description in NCERT"), ["Goblet cell", "Salivary gland", "Ciliated epithelium",
                                             "Compound epithelium"],
     ["Main function is protection against chemical and mechanical stresses",
      "Unicellular glandular epithelium",
      "Moves particles or mucus in a specific direction",
      "Multicellular gland"]),
  match_options(M("II", "IV", "III", "I"), [M("IV", "II", "III", "I"), M("II", "IV", "I", "III"),
                                            M("II", "III", "IV", "I")], "D"), "D",
  "Glandular, ciliated and compound epithelia",
  "NCERT: glandular epithelium may be unicellular, consisting of isolated glandular cells (goblet cells of the "
  "alimentary canal), or multicellular, consisting of clusters of cells (salivary gland). Ciliated epithelium moves "
  "particles or mucus in a specific direction. The main function of compound epithelium is protection against "
  "chemical and mechanical stresses.",
  ["Goblet cell → II", "Salivary gland → IV", "Ciliated epithelium → III", "Compound epithelium → I"],
  R_SOA("animal tissues – epithelial tissue"),
  why_others_wrong="A swaps the unicellular and multicellular glands; B swaps the ciliated and compound epithelia; C "
                   "swaps the salivary gland and ciliated epithelium.",
  seconds=40)

_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
Z(SOA, "Frog: morphology and anatomy", "Advanced", "multi_statement",
  ms("A frog swallows an insect. Which of the following statements about what happens to the insect are correct, "
     "according to NCERT?",
     ["It is captured by the bilobed tongue.",
      "In the stomach, it is digested by the action of HCl and gastric juices.",
      "The partially digested food (chyme) passes from the stomach into the duodenum.",
      "Its fats are emulsified by pancreatic juice.",
      "Its final digestion takes place in the rectum."]),
  _opts, "B",
  "Path of digestion in the frog",
  "NCERT: food is captured by the bilobed tongue; digestion takes place by the action of HCl and gastric juices "
  "secreted from the walls of the stomach; partially digested food called chyme passes from the stomach to the "
  "duodenum. Bile (not pancreatic juice) emulsifies fat, pancreatic juices digest carbohydrates and proteins, and "
  "the final digestion takes place in the intestine. The rectum only passes undigested solid waste to the cloaca.",
  ["(a) true", "(b) true", "(c) true", "(d) false – bile emulsifies fat", "(e) false – final digestion is in the "
   "intestine"],
  R_SOA("frogs – digestive system"),
  why_others_wrong="A includes (d); C and D include (e) and drop correct statements.",
  seconds=60)
ms_check("abc", _opts, "B")

_items = {"Tip of the nose": True, "Outer ear joints": True, "Between adjacent bones of the vertebral column": True,
          "Limbs": True, "Hands": True, "Walls of the stomach": False, "Walls of blood vessels": False,
          "Air sacs of the lungs": False}
_opts = ["2", "3", "4", "5"]
Z(SOA, "Animal tissues", "Advanced", "direct",
  "NCERT lists the sites where cartilage is present in the body of an adult human. How many of the following sites "
  "are in that list?\n\n" + "; ".join(_items),
  _opts, "D",
  "Sites of cartilage in adults",
  "NCERT: most of the cartilages in vertebrate embryos are replaced by bones in adults. Cartilage is present in our "
  "body at the tip of the nose, outer ear joints, between adjacent bones of the vertebral column, limbs and hands in "
  "adults. The walls of the stomach and of blood vessels contain smooth muscle, and the air sacs of the lungs are "
  "made of squamous epithelium.",
  ["Listed → tip of nose, outer ear joints, between vertebrae, limbs, hands = 5",
   "Not listed → stomach wall, blood-vessel walls, air sacs"],
  R_SOA("animal tissues – connective tissue (cartilage)"),
  why_others_wrong="A, B and C leave out some of NCERT's listed sites, usually the limbs and hands.",
  seconds=50)
count_check(_items, _opts, "D")

Z(SOA, "Frog: morphology and anatomy", "Advanced", "assertion_reason",
  ar("In the frog, the renal portal system carries blood from the intestine to the liver.",
     "Frogs have special venous connections between the liver and the intestine as well as between the kidney and "
     "the lower parts of the body."),
  ASSERTION_REASON, "D",
  "Portal systems of the frog",
  "NCERT: special venous connections between the liver and intestine, and between the kidney and lower parts of the "
  "body, are present in frogs. The former is the hepatic portal system and the latter the renal portal system. So R "
  "is true, but A is false: blood from the intestine to the liver travels in the HEPATIC portal system.",
  ["R → true (two portal connections)", "Liver–intestine → hepatic portal system",
   "Kidney–lower body → renal portal system", "A → false"],
  R_SOA("frogs – circulatory system"),
  why_others_wrong="A and B accept the mislabelled portal system; C rejects NCERT's true statement R.",
  seconds=40)

Z(SOA, "Animal tissues", "Advanced", "statement_pair",
  sp("Of the three types of muscle tissue, skeletal muscle is the one closely attached to skeletal bones.",
     "Both smooth muscle fibres and cardiac muscle fibres show striations."),
  STATEMENT_PAIR, "C",
  "Comparing the three types of muscle tissue",
  "NCERT: skeletal muscle tissue is closely attached to skeletal bones (e.g. the biceps), and its fibres are striated. "
  "Smooth muscle fibres do not show striations; cardiac muscle is striated. Statement II is therefore false because "
  "of smooth muscle.",
  ["Statement I → true", "Statement II → false: smooth muscle is non-striated"],
  R_SOA("animal tissues – muscle tissue"),
  why_others_wrong="A and D accept striated smooth muscle; B rejects the true Statement I.",
  seconds=35)


# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "An amino acid is a substituted methane whose α-carbon carries a hydrogen, an amino group, a carboxyl group and a "
  "variable group R. If R is a methyl (–CH₃) group, the amino acid is:",
  ["Glycine", "Serine", "Alanine", "Lysine"], "C",
  "R groups of amino acids",
  "NCERT: the R group in the proteinaceous amino acids could be a hydrogen (glycine), a methyl group (alanine), a "
  "hydroxy methyl (serine), etc.",
  ["Glycine → H", "Alanine → methyl", "Serine → hydroxy methyl"],
  R_BIO("analysis of chemical composition – amino acids"),
  why_others_wrong="A has hydrogen as its R group and B a hydroxy methyl group; D is a basic amino acid, not one "
                   "with a methyl R group.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Basic", "statement_pair",
  sp("Trypsin and insulin are both proteins.",
     "Trypsin acts as a hormone, whereas insulin acts as an enzyme."),
  STATEMENT_PAIR, "C",
  "Functions of proteins",
  "NCERT's table of proteins lists trypsin as an enzyme and insulin as a hormone; both are proteins. Statement II "
  "reverses their functions.",
  ["Statement I → true", "Statement II → false: trypsin is the enzyme and insulin the hormone"],
  R_BIO("proteins"),
  why_others_wrong="A and D accept the reversed functions; B rejects the true Statement I.",
  seconds=25)

Z(BIO, "Carbohydrates and lipids", "Basic", "assertion_reason",
  ar("Gingelly oil remains as an oil (liquid) in winter.",
     "Oils have a lower melting point than fats."),
  ASSERTION_REASON, "A",
  "Fats and oils",
  "NCERT: triglycerides are called fats or oils on the basis of melting point. Oils have a lower melting point "
  "(e.g., gingelly oil) and hence remain as oil in winters. The low melting point is exactly why the oil stays liquid "
  "in the cold – R explains A.",
  ["A → true", "R → true", "Low melting point → stays liquid in winter → R explains A"],
  R_BIO("analysis of chemical composition – lipids"),
  why_others_wrong="B misses NCERT's direct 'hence'; C and D reject true statements.",
  seconds=25)

Z(BIO, "Nucleic acids", "Basic", "match_list",
  ml(("compound", "category"), ["Alanine", "Ribose", "Guanine", "Palmitic acid"],
     ["Fatty acid", "Nitrogen base (a substituted purine)", "Amino acid", "Sugar (a pentose)"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "B"), "B",
  "Small organic molecules of the acid-soluble pool",
  "NCERT: alanine is an amino acid; ribose is a sugar (a pentose; glucose is a hexose); guanine, like adenine, is a "
  "substituted purine; palmitic acid is a fatty acid with 16 carbon atoms including the carboxyl carbon.",
  ["Alanine → III", "Ribose → IV", "Guanine → II", "Palmitic acid → I"],
  R_BIO("analysis of chemical composition"),
  why_others_wrong="A swaps the amino acid and the sugar; C swaps the base and the fatty acid; D swaps the sugar and "
                   "the base.",
  seconds=30)

_ratio = 18.5 / 0.03
assert abs(_ratio - 617) < 1
Z(BIO, "Carbohydrates and lipids", "Basic", "numerical",
  "NCERT compares the percentage by weight of elements in the earth's crust and in the human body. Take carbon as "
  "0.03 per cent of the earth's crust and 18.5 per cent of the human body. By about what factor is the relative "
  "abundance of carbon greater in the human body than in the earth's crust?",
  ["About 61.7", "About 6170", "About 1.6 × 10⁻³", "About 617"], "D",
  "Relative abundance of carbon in living matter",
  "NCERT points out that the relative abundance of carbon and hydrogen with respect to other elements is higher in "
  "any living organism than in the earth's crust. Using the given values, the factor is 18.5 / 0.03 ≈ 617.",
  ["Factor = % in body / % in crust", "= 18.5 / 0.03", "≈ 617"],
  R_BIO("analysis of chemical composition – Table: comparison of elements in earth's crust and human body"),
  shortcut="18.5 / 0.03 = 1850 / 3 ≈ 617.",
  why_others_wrong="A and B misplace the decimal point by a factor of 10; C inverts the ratio (crust / body).",
  seconds=40, verified_by=RECOMPUTED)

Z(BIO, "Nucleic acids", "Intermediate", "direct",
  "Which of the following is a nucleoside whose nitrogenous base is a substituted pyrimidine?",
  ["Thymidine", "Adenosine", "Guanosine", "Cytidylic acid"], "A",
  "Nucleosides and nucleotides",
  "NCERT: adenine and guanine are substituted purines; uracil, cytosine and thymine are substituted pyrimidines. A "
  "base attached to a sugar is a nucleoside (adenosine, guanosine, thymidine, uridine, cytidine); if a phosphate is "
  "also esterified to the sugar, it is a nucleotide (adenylic acid, thymidylic acid, guanylic acid, uridylic acid, "
  "cytidylic acid). Thymidine is a nucleoside with the pyrimidine thymine.",
  ["Nucleoside = base + sugar", "Pyrimidine bases → C, T, U", "Thymidine → nucleoside with thymine ✓",
   "Cytidylic acid → pyrimidine, but a nucleotide"],
  R_BIO("analysis of chemical composition – nucleic acids"),
  why_others_wrong="B and C are nucleosides of purines; D has a pyrimidine but carries a phosphate, so it is a "
                   "nucleotide.",
  seconds=35)

_opts = ["(a) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (e) only", "(a), (b) and (c) only"]
Z(BIO, "Enzymes: properties and action", "Intermediate", "multi_statement",
  ms("A human enzyme has an optimum temperature of 37 °C and an optimum pH of 7. Which of the following statements "
     "about it are correct, according to NCERT?",
     ["At 25 °C its activity is lower than at 37 °C.",
      "Kept at 4 °C, it is preserved in a temporarily inactive state.",
      "Heated to 70 °C, it loses its activity because the protein is denatured by heat.",
      "At pH 9 its activity is higher than at pH 7.",
      "Once its maximum velocity (Vmax) is reached, a further rise in substrate concentration raises the velocity "
      "further."]),
  _opts, "D",
  "Temperature, pH and substrate concentration",
  "NCERT: each enzyme shows its highest activity at its optimum temperature and pH, and activity declines both below "
  "and above the optimum. Low temperature preserves the enzyme in a temporarily inactive state, whereas high "
  "temperature destroys enzymatic activity because proteins are denatured by heat. The velocity of the reaction "
  "reaches a maximum (Vmax) that is not exceeded by any further rise in substrate concentration.",
  ["(a) true – below optimum", "(b) true", "(c) true", "(d) false – activity falls above the optimum pH",
   "(e) false – Vmax is not exceeded"],
  R_BIO("enzymes – factors affecting enzyme activity"),
  why_others_wrong="A includes (d); B and C include (e).",
  seconds=50)
ms_check("abc", _opts, "D")

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("Prosthetic groups and co-enzymes are both organic compounds.",
     "Zinc, the co-factor of the proteolytic enzyme carboxypeptidase, is a prosthetic group."),
  STATEMENT_PAIR, "C",
  "Kinds of co-factors",
  "NCERT: co-factors are of three kinds – prosthetic groups (organic compounds tightly bound to the apoenzyme, e.g. "
  "haem in peroxidase and catalase), co-enzymes (organic compounds transiently associated, e.g. NAD, NADP) and metal "
  "ions (e.g. zinc for carboxypeptidase). Zinc is a metal-ion co-factor, not a prosthetic group.",
  ["Statement I → true", "Statement II → false: zinc is a metal ion co-factor"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="A and D call a metal ion a prosthetic group; B rejects the true Statement I.",
  seconds=35)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Starch gives a blue colour when treated with iodine.",
     "Starch is a store of energy in plant tissues."),
  ASSERTION_REASON, "B",
  "Starch–iodine reaction",
  "NCERT: starch forms helical secondary structures and can hold I₂ molecules in the helical portion; the starch–I₂ "
  "complex is blue. NCERT also states that starch is a store of energy in plant tissues. Being an energy store is a "
  "different property of starch and does not explain the blue colour, which comes from the helices holding iodine.",
  ["A → true (starch–I₂ is blue)", "R → true (energy store in plants)",
   "Colour depends on helices holding I₂, not on storage role → R does not explain A"],
  R_BIO("polysaccharides"),
  why_others_wrong="A gives the wrong reason for the colour; C and D reject true statements.",
  seconds=30)

Z(BIO, "Nucleic acids", "Intermediate", "match_list",
  ml(("term", "description"), ["Homopolymer", "Heteropolymer", "Nucleoside", "Nucleotide"],
     ["Built from only one type of monomer repeated 'n' times, e.g. cellulose",
      "Built from different monomers, e.g. a protein",
      "A nitrogenous base attached to a sugar, e.g. uridine",
      "A phosphate esterified to the sugar of a nucleoside, e.g. guanylic acid"]),
  match_options(M("I", "II", "III", "IV"), [M("II", "I", "III", "IV"), M("I", "II", "IV", "III"),
                                            M("II", "I", "IV", "III")], "A"), "A",
  "Polymers and nucleic-acid building blocks",
  "NCERT: a homopolymer has only one type of monomer repeating 'n' times (cellulose is a homopolymer of glucose), "
  "while proteins are heteropolymers. A nitrogenous base attached to a sugar is a nucleoside (e.g. uridine); if a "
  "phosphate group is also esterified to the sugar, it is a nucleotide (e.g. guanylic acid).",
  ["Homopolymer → I", "Heteropolymer → II", "Nucleoside → III", "Nucleotide → IV"],
  R_BIO("proteins; polysaccharides; nucleic acids"),
  why_others_wrong="B swaps the two kinds of polymer; C swaps nucleoside and nucleotide; D swaps both pairs.",
  seconds=35)

Z(BIO, "Enzyme classification", "Intermediate", "direct",
  "An enzyme links two compounds together by forming a C–S bond between them. In NCERT's classification of enzymes, "
  "it belongs to the class:",
  ["Lyases", "Transferases", "Ligases", "Isomerases"], "C",
  "Ligases",
  "NCERT: ligases catalyse the linking together of two compounds, e.g. enzymes which catalyse the joining of C–O, "
  "C–S, C–N, P–O, etc. bonds. Lyases remove groups leaving double bonds, transferases move a group G (other than "
  "hydrogen) between substrates, and isomerases inter-convert isomers.",
  ["Joining two compounds (C–S bond) → ligase"],
  R_BIO("enzymes – classification and nomenclature"),
  why_others_wrong="A removes groups rather than joining compounds; B transfers a group between two substrates; D "
                   "rearranges a single compound.",
  seconds=30)

_opts = ["(a), (b) and (c) only", "(a), (c) and (d) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"]
Z(BIO, "Proteins and amino acids", "Intermediate", "multi_statement",
  ms("NCERT gives a table of some proteins and their functions. Which of the following protein–function pairs are "
     "correct?",
     ["Collagen – intercellular ground substance", "GLUT-4 – enzyme", "Antibody – fights infectious agents",
      "Receptor – sensory reception (smell, taste, hormone, etc.)", "Trypsin – hormone"]),
  _opts, "B",
  "Functions of some proteins",
  "NCERT's table: collagen – intercellular ground substance; trypsin – enzyme; insulin – hormone; antibody – fights "
  "infectious agents; receptor – sensory reception (smell, taste, hormone, etc.); GLUT-4 – enables glucose transport "
  "into cells.",
  ["(a) correct", "(b) wrong – GLUT-4 enables glucose transport into cells", "(c) correct", "(d) correct",
   "(e) wrong – trypsin is an enzyme"],
  R_BIO("proteins – Table: some proteins and their functions"),
  why_others_wrong="A includes (b); C includes (e); D includes both wrong pairs.",
  seconds=45)
ms_check("acd", _opts, "B")

_items = {"Proteins": True, "Nucleic acids": True, "Polysaccharides": True, "Lipids": False, "Glucose": False,
          "Amino acids": False, "Nucleotides": False}
_opts = ["2", "3", "4", "5"]
Z(BIO, "Carbohydrates and lipids", "Advanced", "direct",
  "A living tissue is ground in trichloroacetic acid and strained. How many of the following would be found in the "
  "acid-insoluble fraction AND have molecular weights in the range of ten thousand daltons and above?\n\n"
  + ", ".join(_items),
  _opts, "B",
  "Acid-soluble and acid-insoluble fractions",
  "NCERT: the acid-insoluble fraction contains proteins, nucleic acids, polysaccharides and lipids. Except lipids, "
  "these have molecular weights of ten thousand daltons and above. Lipids have molecular weights not exceeding about "
  "800 Da; they come into the acid-insoluble fraction only because membranes break into water-insoluble vesicles. "
  "Glucose, amino acids and nucleotides are in the acid-soluble pool (molecular weights about 18 to 800).",
  ["Acid-insoluble → proteins, nucleic acids, polysaccharides, lipids",
   "≥ 10,000 Da → proteins, nucleic acids, polysaccharides (not lipids) = 3"],
  R_BIO("biomacromolecules"),
  why_others_wrong="A drops a macromolecule; C counts the lipids; D also counts a small molecule of the acid-soluble "
                   "pool.",
  seconds=50)
count_check(_items, _opts, "B")

Z(BIO, "Nucleic acids", "Advanced", "statement_pair",
  sp("Removing the phosphate group from adenylic acid leaves adenine.",
     "Thymidine contains a substituted purine."),
  STATEMENT_PAIR, "B",
  "Nucleotide → nucleoside → base",
  "Adenylic acid is a nucleotide (adenine + sugar + phosphate); removing the phosphate leaves the nucleoside "
  "adenosine (adenine + sugar), not the free base adenine. Thymidine is the nucleoside of thymine, which NCERT lists "
  "among the substituted pyrimidines. Both statements are false.",
  ["Statement I → false (gives adenosine)", "Statement II → false (thymine is a pyrimidine)"],
  R_BIO("analysis of chemical composition – nucleic acids"),
  why_others_wrong="A, C and D accept at least one false statement.",
  seconds=40)

Z(BIO, "Carbohydrates and lipids", "Advanced", "match_list",
  ml(("compound", "products of its complete hydrolysis"), ["Lecithin", "A triglyceride", "Cytidylic acid",
                                                           "Cellulose"],
     ["Glucose only", "Cytosine, a pentose sugar and phosphoric acid", "One glycerol and three fatty acids",
      "Glycerol, fatty acids, phosphoric acid and a phosphorylated organic compound"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Building blocks of biomolecules",
  "Lecithin is a phospholipid: besides glycerol and fatty acids it contains phosphorus and a phosphorylated organic "
  "compound. A triglyceride has three fatty acids esterified with one glycerol. Cytidylic acid is a nucleotide – "
  "cytosine, a pentose sugar and phosphate. Cellulose is a homopolymer of glucose.",
  ["Lecithin → IV", "Triglyceride → III", "Cytidylic acid → II", "Cellulose → I"],
  R_BIO("analysis of chemical composition – lipids, nucleotides; polysaccharides"),
  why_others_wrong="A swaps the two lipids; B swaps the nucleotide and cellulose; C swaps the triglyceride and the "
                   "nucleotide.",
  seconds=45)

_opts = ["(a), (b), (c) and (e) only", "(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"]
Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("Removing a small organic molecule from an enzyme abolishes its activity. NCERT would describe this molecule's "
     "association with the protein as only transient, usually occurring during the course of catalysis. Which of the "
     "following statements are correct?",
     ["The small molecule is a co-enzyme.",
      "It may serve as a co-factor in a number of different enzyme-catalysed reactions.",
      "NAD could be an example of such a molecule.",
      "Haem in peroxidase is another example of this kind of co-factor.",
      "The protein portion left behind is called the apoenzyme."]),
  _opts, "A",
  "Co-enzymes versus prosthetic groups",
  "NCERT: co-enzymes are organic compounds whose association with the apoenzyme is only transient, usually during "
  "catalysis; they serve as co-factors in a number of different enzyme-catalysed reactions; NAD and NADP contain the "
  "vitamin niacin. Prosthetic groups such as haem (in peroxidase and catalase) are tightly bound. The protein portion "
  "of such an enzyme is the apoenzyme, and catalytic activity is lost when the co-factor is removed.",
  ["(a) true", "(b) true", "(c) true", "(d) false – haem is a tightly bound prosthetic group", "(e) true"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="B and C include (d); D leaves out the correct (b).",
  seconds=55)
ms_check("abce", _opts, "A")

Z(BIO, "Carbohydrates and lipids", "Advanced", "assertion_reason",
  ar("Like cellulose, chitin is a homopolymer of glucose.",
     "Complex polysaccharides, such as chitin of the arthropod exoskeleton, have amino-sugars and chemically modified "
     "sugars as building blocks."),
  ASSERTION_REASON, "D",
  "Chitin compared with cellulose",
  "NCERT: cellulose is a homopolymer of glucose. Complex polysaccharides such as chitin have as building blocks "
  "amino-sugars and chemically modified sugars (e.g. glucosamine, N-acetyl galactosamine). So R is true, while A is "
  "false: chitin is not built of glucose.",
  ["R → true (amino-sugars and modified sugars)", "A → false (chitin's monomer is not glucose)"],
  R_BIO("polysaccharides"),
  why_others_wrong="A and B accept that chitin is made of glucose; C rejects NCERT's statement R.",
  seconds=40)


# ================================================================ Breathing and Exchange of Gases (B3 I5 A3)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Regulation and disorders", "Basic", "direct",
  "According to NCERT, the role of oxygen in the regulation of the respiratory rhythm is:",
  ["Quite insignificant", "The main stimulus that activates the respiratory rhythm centre",
   "Exerted mainly through the pneumotaxic centre", "Exerted mainly through the chemosensitive area"], "A",
  "Chemical regulation of respiration",
  "NCERT: a chemosensitive area adjacent to the rhythm centre is highly sensitive to CO₂ and hydrogen ions; receptors "
  "associated with the aortic arch and carotid artery also recognise changes in CO₂ and H⁺ concentration. The role of "
  "oxygen in the regulation of the respiratory rhythm is quite insignificant.",
  ["Main chemical signals → CO₂ and H⁺", "O₂ → quite insignificant"],
  R_BRE("regulation of respiration"),
  why_others_wrong="B, C and D give oxygen a major regulatory role; the chemosensitive area responds to CO₂ and H⁺, "
                   "and the pneumotaxic centre moderates the rhythm centre.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Basic", "statement_pair",
  sp("In humans, the alveoli are the primary sites of exchange of gases.",
     "The partial pressure of CO₂ in deoxygenated blood is about 45 mm Hg."),
  STATEMENT_PAIR, "A",
  "Site of exchange and a partial pressure value",
  "NCERT: alveoli are the primary sites of exchange of gases; exchange also occurs between blood and tissues. In "
  "NCERT's table of partial pressures, deoxygenated blood has pO₂ about 40 mm Hg and pCO₂ about 45 mm Hg.",
  ["Statement I → true", "Statement II → true"],
  R_BRE("exchange of gases"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(BRE, "Respiratory system", "Basic", "match_list",
  ml(("animal group", "means of gas exchange given in NCERT"),
     ["Insects", "Aquatic arthropods and molluscs", "Birds", "Coelenterates"],
     ["Gills", "Lungs", "Simple diffusion over the entire body surface", "A network of tubes (tracheal tubes)"]),
  match_options(M("IV", "I", "II", "III"), [M("I", "IV", "II", "III"), M("IV", "I", "III", "II"),
                                            M("IV", "II", "I", "III")], "C"), "C",
  "Respiratory organs in different animals",
  "NCERT: lower invertebrates like sponges, coelenterates and flatworms exchange O₂ with CO₂ by simple diffusion over "
  "their entire body surface. Insects have a network of tubes (tracheal tubes). Special vascularised structures called "
  "gills are used by most aquatic arthropods and molluscs. Reptiles, birds and mammals respire through lungs.",
  ["Insects → IV", "Aquatic arthropods and molluscs → I", "Birds → II", "Coelenterates → III"],
  R_BRE("respiratory organs"),
  why_others_wrong="A swaps the insects and aquatic arthropods; B swaps birds and coelenterates; D swaps gills and "
                   "lungs.",
  seconds=30)

_tv, _irv, _erv, _rv = 500, 3000, 1000, 1200
_vc = _tv + _irv + _erv
assert _vc == 4500 and round(100 * _tv / _vc, 1) == 11.1
assert round(100 * _tv / (_vc + _rv), 1) == 8.8 and round(100 * _tv / (_tv + _irv), 1) == 14.3
assert round(100 * _tv / (_tv + _erv), 1) == 33.3
Z(BRE, "Respiratory volumes", "Intermediate", "numerical",
  "Spirometry of a healthy adult gives a tidal volume of 500 mL, an inspiratory reserve volume of 3000 mL, an "
  "expiratory reserve volume of 1000 mL and a residual volume of 1200 mL. During quiet breathing, what percentage of "
  "his vital capacity is used in each breath (take one breath as the tidal volume)?",
  ["8.8%", "11.1%", "14.3%", "33.3%"], "B",
  "Tidal volume as a part of vital capacity",
  "NCERT: vital capacity is the maximum volume of air a person can breathe in after a forced expiration, i.e. "
  "ERV + TV + IRV. It does not include the residual volume. Here VC = 1000 + 500 + 3000 = 4500 mL, and the tidal "
  "volume is 500/4500 × 100 ≈ 11.1% of it.",
  ["VC = ERV + TV + IRV = 1000 + 500 + 3000 = 4500 mL", "TV / VC = 500 / 4500", "≈ 11.1%"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="VC is 9 tidal volumes here, so one breath is 1/9 ≈ 11.1% of it.",
  why_others_wrong="A divides by the total lung capacity (adds the residual volume); C divides by the inspiratory "
                   "capacity (TV + IRV); D divides by the expiratory capacity (TV + ERV).",
  seconds=60, verified_by=RECOMPUTED)

Z(BRE, "Respiratory system", "Intermediate", "assertion_reason",
  ar("The larynx is called the sound box.",
     "During swallowing, the glottis can be covered by the epiglottis, which prevents the entry of food into the "
     "larynx."),
  ASSERTION_REASON, "B",
  "Larynx and epiglottis",
  "NCERT: the larynx is a cartilaginous box which helps in sound production and hence is called the sound box. "
  "NCERT also states that during swallowing the glottis can be covered by a thin, elastic, cartilaginous flap, the "
  "epiglottis, to prevent the entry of food into the larynx. The name 'sound box' comes from the role in sound "
  "production; closing the glottis during swallowing is an unrelated function.",
  ["A → true (helps in sound production)", "R → true (epiglottis guards the glottis)",
   "R concerns swallowing, not sound production → R does not explain A"],
  R_BRE("human respiratory system"),
  why_others_wrong="A links an unrelated protective function to the name; C and D reject true statements.",
  seconds=30)

_opts = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b) and (c) only", "(a), (c), (d) and (e) only"]
Z(BRE, "Mechanism of breathing", "Intermediate", "multi_statement",
  ms("Which of the following take place during a normal inspiration in a human, according to NCERT?",
     ["The diaphragm contracts, increasing the volume of the thoracic chamber in the antero-posterior axis.",
      "The external inter-costal muscles contract and lift up the ribs and the sternum.",
      "The volume of the thoracic chamber increases in the dorso-ventral axis.",
      "The intra-pulmonary pressure becomes greater than the atmospheric pressure.",
      "The diaphragm relaxes and returns to its normal position."]),
  _opts, "C",
  "Events of inspiration",
  "NCERT: inspiration is initiated by contraction of the diaphragm, which increases the thoracic volume in the "
  "antero-posterior axis. Contraction of the external inter-costal muscles lifts up the ribs and the sternum, "
  "increasing the volume in the dorso-ventral axis. The overall increase in thoracic volume increases pulmonary "
  "volume, so the intra-pulmonary pressure falls BELOW atmospheric pressure and air moves in. Relaxation of the "
  "diaphragm belongs to expiration.",
  ["(a) true", "(b) true", "(c) true", "(d) false – pressure falls below atmospheric", "(e) false – that is "
   "expiration"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and D include (d); B includes (e) and drops (a).",
  seconds=45)
ms_check("abc", _opts, "C")

Z(BRE, "Exchange and transport of gases", "Intermediate", "statement_pair",
  sp("The diffusion membrane in the lungs is made of only two layers: the squamous epithelium of the alveoli and the "
     "endothelium of the alveolar capillaries.",
     "The total thickness of the diffusion membrane is much less than a millimetre."),
  STATEMENT_PAIR, "D",
  "The diffusion membrane",
  "NCERT: the diffusion membrane is made up of three major layers – the thin squamous epithelium of the alveoli, the "
  "endothelium of the alveolar capillaries and the basement substance (composed of a thin basement membrane "
  "supporting the squamous epithelium and that surrounding the single-layer endothelial cells) between them. Its "
  "total thickness is much less than a millimetre, which favours diffusion.",
  ["Statement I → false (three layers – the basement substance is left out)", "Statement II → true"],
  R_BRE("exchange of gases"),
  why_others_wrong="A and C accept a two-layered membrane; B rejects the true Statement II.",
  seconds=35)

Z(BRE, "Respiratory system", "Intermediate", "direct",
  "Which of the following parts of the human respiratory tract is NOT among those that NCERT describes as supported "
  "by incomplete cartilaginous rings?",
  ["Trachea", "Primary bronchi", "Tertiary bronchi", "Terminal bronchioles"], "D",
  "Cartilaginous support of the airways",
  "NCERT: the trachea, the primary, secondary and tertiary bronchi, and the initial bronchioles are supported by "
  "incomplete cartilaginous rings. Repeated divisions of the tertiary bronchi end in very thin terminal bronchioles, "
  "which are not in this list.",
  ["Supported → trachea, primary, secondary, tertiary bronchi, initial bronchioles",
   "Terminal bronchioles → not listed"],
  R_BRE("human respiratory system"),
  why_others_wrong="A, B and C are all named by NCERT as supported by incomplete cartilaginous rings.",
  seconds=30)

_opts = ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only", "(a), (b), (c) and (d) only"]
Z(BRE, "Exchange and transport of gases", "Advanced", "multi_statement",
  ms("Using NCERT's table of partial pressures (in mm Hg) of O₂ and CO₂, which of the following comparisons are "
     "correct?",
     ["The pO₂ of alveolar air is lower than that of atmospheric air.",
      "The pCO₂ of alveolar air is higher than that of atmospheric air.",
      "The pO₂ of alveolar air is higher than that of oxygenated blood.",
      "The pCO₂ of alveolar air is equal to that of oxygenated blood.",
      "The pCO₂ of the tissues is lower than that of deoxygenated blood."]),
  _opts, "D",
  "Reading the table of partial pressures",
  "NCERT's values (O₂, CO₂): atmospheric air 159, 0.3; alveoli 104, 40; deoxygenated blood 40, 45; oxygenated blood "
  "95, 40; tissues 40, 45. So alveolar pO₂ (104) < atmospheric (159); alveolar pCO₂ (40) > atmospheric (0.3); "
  "alveolar pO₂ (104) > oxygenated blood (95); alveolar pCO₂ (40) = oxygenated blood (40); tissue pCO₂ (45) = "
  "deoxygenated blood (45), not lower.",
  ["(a) 104 < 159 → true", "(b) 40 > 0.3 → true", "(c) 104 > 95 → true", "(d) 40 = 40 → true",
   "(e) 45 = 45 → false"],
  R_BRE("exchange of gases – Table: partial pressures of oxygen and carbon dioxide"),
  why_others_wrong="A leaves out the correct (d); B and C include (e).",
  seconds=60)
ms_check("abcd", _opts, "D")

Z(BRE, "Mechanism of breathing", "Advanced", "assertion_reason",
  ar("Additional muscles in the abdomen can increase the strength of expiration.",
     "Normal (quiet) expiration is brought about by the contraction of the diaphragm."),
  ASSERTION_REASON, "C",
  "Normal and forceful expiration",
  "NCERT: we have the ability to increase the strength of inspiration and expiration with the help of additional "
  "muscles in the abdomen – A is true. Normal expiration takes place when the diaphragm and the inter-costal muscles "
  "RELAX, returning the diaphragm and sternum to their normal positions and reducing the thoracic volume; contraction "
  "of the diaphragm initiates inspiration. R is false.",
  ["A → true", "Diaphragm contraction → inspiration", "Diaphragm relaxation → expiration", "R → false"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and B accept that diaphragm contraction causes expiration; D rejects NCERT's statement about "
                   "the abdominal muscles.",
  seconds=40)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "A sample has a pO₂ of about 40 mm Hg and a pCO₂ of about 45 mm Hg. Using only NCERT's table of partial pressures, "
  "the sample could be:",
  ["Alveolar air or oxygenated blood", "Deoxygenated blood or the tissues", "Atmospheric air",
   "Oxygenated blood only"], "B",
  "Identifying a sample from partial pressures",
  "NCERT's table gives pO₂ 40 and pCO₂ 45 mm Hg for BOTH deoxygenated blood and the tissues, so the table alone "
  "cannot tell these two apart. Alveolar air (104, 40), oxygenated blood (95, 40) and atmospheric air (159, 0.3) do "
  "not match.",
  ["Deoxygenated blood → 40, 45", "Tissues → 40, 45", "Both match → either is possible"],
  R_BRE("exchange of gases – Table: partial pressures of oxygen and carbon dioxide"),
  why_others_wrong="A, C and D name samples whose pO₂ is far higher (95–159 mm Hg) and pCO₂ lower (0.3–40 mm Hg).",
  seconds=40)


# ================================================================ Body Fluids and Circulation (B4 I6 A4)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Human heart", "Basic", "statement_pair",
  sp("In the human heart, the atria are two relatively small upper chambers and the ventricles are two larger lower "
     "chambers.",
     "The right and left atria are separated by a thick-walled, fibrous inter-atrial septum."),
  STATEMENT_PAIR, "C",
  "Chambers and septa of the human heart",
  "NCERT: the heart has four chambers – two relatively small upper chambers called atria and two larger lower "
  "chambers called ventricles. A thin, muscular wall called the inter-atrial septum separates the right and left "
  "atria; it is the inter-ventricular septum that is thick-walled, and the atrio-ventricular septum that is a thick "
  "fibrous tissue.",
  ["Statement I → true", "Statement II → false: the inter-atrial septum is thin and muscular"],
  R_BFC("circulatory pathways – human circulatory system"),
  why_others_wrong="A and D accept a thick, fibrous inter-atrial septum; B rejects the true Statement I.",
  seconds=30)

Z(BFC, "Human heart", "Basic", "direct",
  "In the human heart, the atrium and the ventricle of the same side are separated by a thick fibrous tissue called "
  "the:",
  ["Inter-atrial septum", "Inter-ventricular septum", "Pericardium", "Atrio-ventricular septum"], "D",
  "Septa of the heart",
  "NCERT: the atrium and the ventricle of the same side are separated by a thick fibrous tissue called the "
  "atrio-ventricular septum; each of these septa has an opening that connects the two chambers of the same side. "
  "The inter-atrial septum (thin, muscular) separates the two atria and the inter-ventricular septum (thick-walled) "
  "separates the two ventricles. The pericardium is the double-walled membranous bag around the heart.",
  ["Atrium ↔ ventricle of the same side → atrio-ventricular septum"],
  R_BFC("circulatory pathways – human circulatory system"),
  why_others_wrong="A separates the two atria and B the two ventricles; C is the protective covering of the heart.",
  seconds=20)

Z(BFC, "Circulatory disorders", "Basic", "direct",
  "According to NCERT, coronary artery disease (CAD) is often referred to as:",
  ["Atherosclerosis", "Angina", "Heart failure", "Hypertension"], "A",
  "Coronary artery disease",
  "NCERT: coronary artery disease, often referred to as atherosclerosis, affects the vessels that supply blood to the "
  "heart muscle. It is caused by deposits of calcium, fat, cholesterol and fibrous tissues, which make the lumen of "
  "the arteries narrower. Angina, heart failure and hypertension are described as separate disorders.",
  ["CAD ↔ atherosclerosis"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="B is acute chest pain when not enough O₂ reaches the heart muscle; C is ineffective pumping; D is "
                   "blood pressure persistently above normal.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Basic", "assertion_reason",
  ar("Neutrophils are phagocytic cells.",
     "Neutrophils are the most abundant cells (60–65 per cent) of the total WBCs."),
  ASSERTION_REASON, "B",
  "Neutrophils",
  "NCERT: neutrophils are the most abundant cells (60–65 per cent) of the total WBCs; neutrophils and monocytes "
  "(6–8 per cent) are phagocytic cells which destroy foreign organisms entering the body. Both statements are true, "
  "but being numerous is not why a cell is phagocytic – monocytes are phagocytic too while forming only 6–8 per cent. "
  "R does not explain A.",
  ["A → true", "R → true", "Abundance ≠ phagocytic ability (monocytes are few yet phagocytic) → R does not explain A"],
  R_BFC("blood – formed elements"),
  why_others_wrong="A links a count to a function; C and D reject true statements.",
  seconds=30)

_rbc_per_mm3, _blood_mm3, _life = 4.8e6, 5 * 1e6, 120
_total = _rbc_per_mm3 * _blood_mm3
_per_day = _total / _life
assert abs(_total - 2.4e13) < 1e9 and abs(_per_day - 2.0e11) < 1e7
assert abs(_rbc_per_mm3 * 5 * 1e3 / _life - 2.0e8) < 1e4 and abs(_per_day / 24 - 8.3e9) < 0.05e9
Z(BFC, "Blood and blood groups", "Intermediate", "numerical",
  "A man has 5 L of blood containing 4.8 million RBCs per mm³. RBCs have an average life span of 120 days. Assuming "
  "that his RBC count stays constant and that every RBC lives exactly 120 days, about how many RBCs are destroyed "
  "(and replaced) in his body each day? (Take 1 L = 10⁶ mm³.)",
  ["2.0 × 10⁸", "8.3 × 10⁹", "2.0 × 10¹¹", "2.4 × 10¹³"], "C",
  "Life span of RBCs",
  "NCERT: RBCs have an average life span of 120 days, after which they are destroyed in the spleen (graveyard of "
  "RBCs). With a constant count, the number destroyed each day equals the total number divided by the life span.",
  ["Blood volume = 5 L = 5 × 10⁶ mm³", "Total RBCs = 4.8 × 10⁶ × 5 × 10⁶ = 2.4 × 10¹³",
   "Per day = 2.4 × 10¹³ / 120 = 2.0 × 10¹¹"],
  R_BFC("blood – formed elements (erythrocytes)"),
  shortcut="4.8 × 5 = 24, and 24/120 = 0.2; powers: 10⁶ × 10⁶ = 10¹² → 0.2 × 10¹² = 2 × 10¹¹.",
  why_others_wrong="A takes 1 L as 1000 mm³; B gives the number per hour; D is the total number of RBCs, not the "
                   "number per day.",
  seconds=75, verified_by=RECOMPUTED)

Z(BFC, "Circulatory disorders", "Intermediate", "statement_pair",
  sp("Heart failure is sometimes called congestive heart failure because congestion of the lungs is one of its main "
     "symptoms.",
     "Cardiac arrest is the condition in which the heart muscle is suddenly damaged by an inadequate blood supply."),
  STATEMENT_PAIR, "C",
  "Heart failure, cardiac arrest and heart attack",
  "NCERT: heart failure means the state of the heart when it is not pumping blood effectively enough to meet the "
  "needs of the body; it is sometimes called congestive heart failure because congestion of the lungs is one of its "
  "main symptoms. Heart failure is not the same as cardiac arrest (when the heart stops beating) or a heart attack "
  "(when the heart muscle is suddenly damaged by an inadequate blood supply). Statement II describes a heart attack.",
  ["Statement I → true", "Statement II → false: that is a heart attack, not cardiac arrest"],
  R_BFC("disorders of circulatory system"),
  why_others_wrong="A and D accept the definition of heart attack as cardiac arrest; B rejects the true Statement I.",
  seconds=35)

Z(BFC, "Coagulation and lymph", "Intermediate", "assertion_reason",
  ar("Interstitial (tissue) fluid lacks the larger proteins and most of the formed elements of blood.",
     "Interstitial fluid has a mineral distribution different from that of plasma."),
  ASSERTION_REASON, "C",
  "Composition of interstitial fluid",
  "NCERT: as blood passes through the capillaries in tissues, some water along with many small water-soluble "
  "substances moves out into the spaces between the cells, leaving the larger proteins and most of the formed "
  "elements in the blood vessels. This interstitial fluid has the SAME mineral distribution as that in plasma. So A "
  "is true but R is false.",
  ["A → true", "R → false (same mineral distribution as plasma)"],
  R_BFC("lymph (tissue fluid)"),
  why_others_wrong="A and B accept a false R; D rejects the true A.",
  seconds=35)

_opts = ["(a), (b), (c) and (e) only", "(a), (b) and (c) only", "(a) and (d) only", "(b), (c) and (d) only"]
Z(BFC, "Double circulation and regulation", "Intermediate", "multi_statement",
  ms("Which of the following statements about the hepatic portal system and the coronary system are correct, "
     "according to NCERT?",
     ["The hepatic portal vein carries blood from the intestine to the liver before it is delivered to the systemic "
      "circulation.",
      "The hepatic portal system is a unique vascular connection between the digestive tract and the liver.",
      "The coronary system circulates blood exclusively to and from the cardiac musculature.",
      "The hepatic portal vein carries blood from the liver to the intestine.",
      "The coronary system is a part of the pulmonary circulation."]),
  _opts, "B",
  "Special vascular connections",
  "NCERT: a unique vascular connection exists between the digestive tract and liver, called the hepatic portal "
  "system; the hepatic portal vein carries blood from the intestine to the liver before it is delivered to the "
  "systemic circulation. A special coronary system of blood vessels is present in our body exclusively for the "
  "circulation of blood to and from the cardiac musculature. Pulmonary circulation is the path between the right "
  "ventricle, the lungs and the left atrium.",
  ["(a) true", "(b) true", "(c) true", "(d) false – direction reversed", "(e) false – it serves the heart muscle, not "
   "the lungs"],
  R_BFC("double circulation"),
  why_others_wrong="A includes (e); C and D include the reversed direction in (d).",
  seconds=45)
ms_check("abc", _opts, "B")

Z(BFC, "Blood and blood groups", "Intermediate", "direct",
  "Which of the following leucocytes is phagocytic but is NOT a granulocyte?",
  ["Monocyte", "Neutrophil", "Lymphocyte", "Basophil"], "A",
  "Granulocytes, agranulocytes and phagocytes",
  "NCERT: neutrophils, eosinophils and basophils are granulocytes; lymphocytes and monocytes are agranulocytes. "
  "Neutrophils and monocytes are phagocytic cells. The only cell that is both phagocytic and an agranulocyte is the "
  "monocyte.",
  ["Phagocytic → neutrophils, monocytes", "Agranulocytes → lymphocytes, monocytes", "Common to both → monocyte"],
  R_BFC("blood – formed elements (leucocytes)"),
  why_others_wrong="B is phagocytic but a granulocyte; C is an agranulocyte but responsible for immune responses, not "
                   "described as phagocytic; D is a granulocyte that secretes histamine, serotonin and heparin.",
  seconds=35)

Z(BFC, "Cardiac cycle and ECG", "Intermediate", "match_list",
  ml(("event", "record of it"),
     ["Closure of the tricuspid and bicuspid valves", "Closure of the semilunar valves",
      "Depolarisation of the atria", "Return of the ventricles from the excited to the normal state"],
     ["T-wave of the ECG", "P-wave of the ECG", "Second heart sound, 'dub'", "First heart sound, 'lub'"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("III", "IV", "I", "II")], "D"), "D",
  "Heart sounds and ECG waves",
  "NCERT: the first heart sound (lub) is associated with the closure of the tricuspid and bicuspid valves, and the "
  "second (dub) with the closure of the semilunar valves. In the ECG, the P-wave represents the electrical "
  "excitation (depolarisation) of the atria, and the T-wave represents the return of the ventricles from the excited "
  "to the normal state (repolarisation).",
  ["AV valves close → lub (IV)", "Semilunar valves close → dub (III)", "Atrial depolarisation → P (II)",
   "Ventricular repolarisation → T (I)"],
  R_BFC("cardiac cycle; electrocardiograph (ECG)"),
  why_others_wrong="A swaps the two heart sounds; B swaps the P- and T-waves; C swaps both pairs.",
  seconds=40)

Z(BFC, "Double circulation and regulation", "Advanced", "direct",
  "An RBC enters the right atrium through the vena cava and travels by the shortest route until it leaves the heart "
  "in the aorta. In which order does it pass the valves of the heart?",
  ["Bicuspid → semilunar valve of the pulmonary artery → tricuspid → semilunar valve of the aorta",
   "Tricuspid → semilunar valve of the pulmonary artery → bicuspid → semilunar valve of the aorta",
   "Tricuspid → bicuspid → semilunar valve of the pulmonary artery → semilunar valve of the aorta",
   "Semilunar valve of the pulmonary artery → tricuspid → semilunar valve of the aorta → bicuspid"], "B",
  "Valves met in double circulation",
  "Right atrium → (tricuspid valve) → right ventricle → (semilunar valve) → pulmonary artery → lungs → pulmonary "
  "veins → left atrium → (bicuspid/mitral valve) → left ventricle → (semilunar valve) → aorta. NCERT: the tricuspid "
  "valve guards the opening between the right atrium and right ventricle, the bicuspid between the left atrium and "
  "left ventricle, and semilunar valves guard the openings of the right and left ventricles into the pulmonary artery "
  "and the aorta.",
  ["RA → tricuspid → RV", "RV → semilunar → pulmonary artery → lungs", "Pulmonary veins → LA → bicuspid → LV",
   "LV → semilunar → aorta"],
  R_BFC("human circulatory system; double circulation"),
  why_others_wrong="A starts on the left side; C skips the pulmonary circuit between the two atrio-ventricular "
                   "valves; D puts a semilunar valve before the tricuspid.",
  seconds=50)

Z(BFC, "Cardiac cycle and ECG", "Advanced", "assertion_reason",
  ar("In a standard ECG, the QRS complex represents the contraction of the atria.",
     "The contraction of the ventricles starts shortly after Q and marks the beginning of the systole."),
  ASSERTION_REASON, "D",
  "Meaning of the QRS complex",
  "NCERT: the P-wave represents depolarisation of the atria, which leads to the contraction of both the atria. The "
  "QRS complex represents the depolarisation of the ventricles, which initiates ventricular contraction; the "
  "contraction starts shortly after Q and marks the beginning of the systole. A is false; R is true.",
  ["QRS → ventricular depolarisation (not atrial)", "A → false", "R → true"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="A and B accept a false A; C rejects the true R.",
  seconds=35)

Z(BFC, "Double circulation and regulation", "Advanced", "statement_pair",
  sp("In fishes, the heart pumps out oxygenated blood, which then goes to the gills.",
     "In birds and mammals, the oxygenated and deoxygenated blood received by the left and right atria respectively "
     "pass on to the ventricles of the same sides."),
  STATEMENT_PAIR, "D",
  "Single and double circulation",
  "NCERT: in fishes the heart pumps out deoxygenated blood, which is oxygenated by the gills and supplied to the body "
  "parts, from where deoxygenated blood is carried back to the heart (single circulation). In birds and mammals, "
  "oxygenated and deoxygenated blood received by the left and right atria respectively pass on to the ventricles of "
  "the same sides; the ventricles pump it out without any mixing (double circulation).",
  ["Statement I → false (fish heart pumps deoxygenated blood)", "Statement II → true"],
  R_BFC("circulatory pathways"),
  why_others_wrong="A and C accept that the fish heart pumps oxygenated blood; B rejects the true Statement II.",
  seconds=40)

_hr, _sv = 75, 70
assert 60 / _hr == 0.8 and _hr * _sv == 5250 and 2 * _hr == 150 and 2 * _hr * _sv == 10500
_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]
Z(BFC, "Cardiac cycle and ECG", "Advanced", "multi_statement",
  ms("A person's heart beats 75 times per minute, and each ventricle pumps out 70 mL of blood in each cardiac cycle. "
     "Which of the following statements are correct?",
     ["The duration of each cardiac cycle is 0.8 s.",
      "His cardiac output is 5250 mL per minute.",
      "His heart produces 150 prominent heart sounds ('lub' and 'dub') per minute.",
      "His left ventricle pumps out 70 mL of blood into the aorta in each cardiac cycle.",
      "His two ventricles together pump out a total of 5250 mL of blood per minute."]),
  _opts, "A",
  "Stroke volume, cardiac output and heart sounds",
  "NCERT: the stroke volume is the volume of blood pumped out by each ventricle during a cardiac cycle (about 70 mL), "
  "and cardiac output = stroke volume × heart rate is the volume pumped out by EACH ventricle per minute. Two "
  "prominent sounds (lub and dub) are produced in each cycle. Here: cycle = 60/75 = 0.8 s; cardiac output = 70 × 75 = "
  "5250 mL/min; sounds = 2 × 75 = 150 per minute; the two ventricles together pump 2 × 5250 = 10500 mL/min.",
  ["(a) 60/75 = 0.8 s → true", "(b) 70 × 75 = 5250 mL/min → true", "(c) 2 × 75 = 150 → true",
   "(d) stroke volume of each ventricle → true", "(e) both ventricles → 10500 mL/min → false"],
  R_BFC("cardiac cycle"),
  why_others_wrong="B and D include (e), which forgets that cardiac output is per ventricle; C leaves out the correct "
                   "(a).",
  seconds=75)
ms_check("abcd", _opts, "A")


# ================================================================ Excretory Products and their Elimination (B4 I5 A4)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Urine formation", "Basic", "direct",
  "Which part of the nephron reabsorbs nearly all of the essential nutrients and 70–80 per cent of the electrolytes "
  "and water of the filtrate?",
  ["Distal convoluted tubule", "Proximal convoluted tubule", "Ascending limb of Henle's loop", "Collecting duct"],
  "B",
  "Reabsorption in the PCT",
  "NCERT: the PCT is lined by simple cuboidal brush border epithelium, which increases the surface area for "
  "reabsorption. Nearly all of the essential nutrients, and 70–80 per cent of electrolytes and water, are reabsorbed "
  "by this segment.",
  ["Maximum reabsorption, incl. nearly all nutrients → PCT"],
  R_EXC("function of the tubules"),
  why_others_wrong="A carries out conditional reabsorption of Na⁺ and water; C is impermeable to water; D reabsorbs "
                   "large amounts of water mainly to concentrate urine.",
  seconds=25)

Z(EXC, "Nephron structure", "Basic", "statement_pair",
  sp("The kidneys are situated close to the dorsal inner wall of the abdominal cavity.",
     "Each ureter carries urine from a kidney directly into the urethra."),
  STATEMENT_PAIR, "C",
  "Organs of the human excretory system",
  "NCERT: the kidneys are reddish-brown, bean-shaped structures situated between the levels of the last thoracic and "
  "third lumbar vertebra close to the dorsal inner wall of the abdominal cavity. The ureters open into the urinary "
  "bladder, which stores urine until it is released through the urethra.",
  ["Statement I → true", "Statement II → false: ureters open into the urinary bladder"],
  R_EXC("human excretory system"),
  why_others_wrong="A and D accept that the ureters lead straight to the urethra; B rejects the true Statement I.",
  seconds=25)

Z(EXC, "Urine formation", "Basic", "assertion_reason",
  ar("The urine of a healthy adult human is slightly acidic.",
     "On an average, 25–30 g of urea is excreted out per day."),
  ASSERTION_REASON, "B",
  "Characteristics of urine",
  "NCERT: the urine formed is a light yellow coloured watery fluid which is slightly acidic (pH 6.0) and has a "
  "characteristic odour; on an average, 25–30 g of urea is excreted out per day. Both are true, but the daily amount "
  "of urea is a separate fact and does not explain the pH of urine.",
  ["A → true (pH about 6.0)", "R → true (25–30 g urea/day)", "R does not explain A"],
  R_EXC("micturition"),
  why_others_wrong="A forges a link NCERT does not make; C and D reject true statements.",
  seconds=25)

Z(EXC, "Urine formation", "Basic", "direct",
  "Conditional reabsorption of Na⁺ and water takes place in which part of the nephron?",
  ["Proximal convoluted tubule", "Descending limb of Henle's loop", "Collecting duct",
   "Distal convoluted tubule"], "D",
  "Functions of the DCT",
  "NCERT: in the DCT, conditional reabsorption of Na⁺ and water takes place. The DCT is also capable of reabsorption "
  "of HCO₃⁻ and selective secretion of hydrogen and potassium ions and NH₃ to maintain the pH and sodium–potassium "
  "balance in blood.",
  ["Conditional reabsorption of Na⁺ and water → DCT"],
  R_EXC("function of the tubules"),
  why_others_wrong="A reabsorbs nutrients, electrolytes and water in bulk; B is permeable to water but almost "
                   "impermeable to electrolytes; C is the site of large-scale water reabsorption for concentrated urine.",
  seconds=25)

_gfr = 125  # mL per minute
_day = _gfr * 60 * 24 / 1000  # litres per day
assert _day == 180 and _day / 3 == 60 and _day / 5 == 36 and _day / 24 / 3 == 2.5 and _day / 3000 == 0.06
Z(EXC, "Urine formation", "Intermediate", "numerical",
  "A person has 5 L of blood, of which 3 L is plasma, and a glomerular filtration rate (GFR) of 125 mL per minute. "
  "In one day, the kidneys filter a volume equal to the person's whole plasma volume about how many times?",
  ["60", "36", "2.5", "0.06"], "A",
  "Scale of glomerular filtration",
  "NCERT: a GFR of 125 mL per minute means about 180 litres of filtrate per day. Filtration takes place from the "
  "plasma (blood cells and plasma proteins stay behind), so the daily filtrate is compared with the plasma volume.",
  ["Filtrate per day = 125 mL/min × 1440 min = 180,000 mL = 180 L", "Plasma = 3 L",
   "180 / 3 = 60 times"],
  R_EXC("urine formation – glomerular filtration"),
  shortcut="NCERT's 180 L/day ÷ 3 L = 60.",
  why_others_wrong="B divides by the whole blood volume; C gives the number per hour; D divides litres by "
                   "millilitres.",
  seconds=60, verified_by=RECOMPUTED)

_glucose_g_per_L = 100 / 1000 * 10  # 100 mg per 100 mL = 1 g per L
_filtered = _day * _glucose_g_per_L
assert _glucose_g_per_L == 1 and _filtered == 180
Z(EXC, "Urine formation", "Intermediate", "numerical",
  "A healthy person has a plasma glucose concentration of 100 mg per 100 mL and a GFR of 125 mL per minute. Glucose "
  "passes freely into the glomerular filtrate, and the person's urine contains no glucose. About how much glucose do "
  "the renal tubules reabsorb in one day?",
  ["1.8 g", "125 g", "0 g", "180 g"], "D",
  "Filtered load and reabsorption of glucose",
  "NCERT: almost all constituents of the plasma except the proteins pass into the filtrate, and substances like "
  "glucose are reabsorbed actively by the tubules (glucose in urine, glycosuria, indicates diabetes mellitus). If none "
  "appears in the urine, all the glucose filtered must have been reabsorbed.",
  ["Filtrate per day = 125 × 1440 mL = 180 L", "Glucose = 100 mg/100 mL = 1 g/L",
   "Filtered = 180 L × 1 g/L = 180 g", "Urine glucose = 0 → reabsorbed = 180 g"],
  R_EXC("urine formation – reabsorption"),
  shortcut="180 L/day × 1 g/L = 180 g, all of it reabsorbed.",
  why_others_wrong="A uses the daily urine volume instead of the filtrate; B mixes up the GFR value with grams; C "
                   "assumes glucose is not filtered at all.",
  seconds=70, verified_by=RECOMPUTED)

_opts = ["(a), (b), (c) and (d) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (c) only"]
Z(EXC, "Regulation of kidney function", "Intermediate", "multi_statement",
  ms("Which of the following can lead to an increase in blood pressure and GFR, according to NCERT?",
     ["Angiotensin II, being a powerful vasoconstrictor",
      "ADH, through its constrictory effects on blood vessels",
      "Aldosterone, which causes reabsorption of Na⁺ and water from the distal parts of the tubule",
      "Atrial natriuretic factor (ANF)",
      "Dilation of blood vessels (vasodilation)"]),
  _opts, "B",
  "Hormones raising blood pressure and GFR",
  "NCERT: angiotensin II, a powerful vasoconstrictor, increases the glomerular blood pressure and thereby GFR; ADH's "
  "constrictory effect on blood vessels increases blood pressure, which can increase glomerular blood flow and GFR; "
  "aldosterone causes reabsorption of Na⁺ and water from the distal parts of the tubule, which also leads to an "
  "increase in blood pressure and GFR. ANF causes vasodilation and decreases blood pressure, acting as a check on "
  "the renin–angiotensin mechanism.",
  ["(a) raises", "(b) raises", "(c) raises", "(d) lowers", "(e) lowers"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A includes ANF; C includes ANF and vasodilation; D leaves out ADH.",
  seconds=50)
ms_check("abc", _opts, "B")

Z(EXC, "Nephron structure", "Intermediate", "assertion_reason",
  ar("In cortical nephrons, the loop of Henle is too short and extends only very little into the medulla.",
     "The vasa recta is well developed in cortical nephrons."),
  ASSERTION_REASON, "C",
  "Cortical and juxtamedullary nephrons",
  "NCERT: in the majority of nephrons the loop of Henle is too short and extends only very little into the medulla; "
  "these are cortical nephrons. In some nephrons the loop is very long and runs deep into the medulla – the "
  "juxtamedullary nephrons. The vasa recta is absent or highly reduced in cortical nephrons. So A is true and R is "
  "false.",
  ["A → true", "R → false (vasa recta absent or highly reduced in cortical nephrons)"],
  R_EXC("human excretory system – nephron"),
  why_others_wrong="A and B accept a well-developed vasa recta in cortical nephrons; D rejects the true A.",
  seconds=35)

Z(EXC, "Urine formation", "Intermediate", "statement_pair",
  sp("The counter-current mechanism helps to maintain an increasing osmolarity towards the inner medullary "
     "interstitium, from about 300 mOsmol L⁻¹ in the cortex to about 1200 mOsmol L⁻¹ in the inner medulla.",
     "This gradient is mainly caused by NaCl and urea."),
  STATEMENT_PAIR, "A",
  "Medullary osmolarity gradient",
  "NCERT: the proximity between Henle's loop and the vasa recta, and the counter current in them, help in "
  "maintaining an increasing osmolarity towards the inner medullary interstitium, i.e. from 300 mOsmol L⁻¹ in the "
  "cortex to about 1200 mOsmol L⁻¹ in the inner medulla. This gradient is mainly caused by NaCl and urea.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("mechanism of concentration of the filtrate"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=35)

_opts = ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (b), (c) and (e) only", "(a), (c) and (e) only"]
Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("Trace a molecule of water from the blood in a glomerulus until it is either reabsorbed or reaches the urine. "
     "Which of the following statements are correct according to NCERT?",
     ["It leaves the glomerular blood across the endothelium of the glomerular blood vessels, the basement membrane "
      "and the epithelium of Bowman's capsule.",
      "In the initial segments of the nephron, it can be reabsorbed passively.",
      "It can leave the filtrate in the descending limb of Henle's loop.",
      "It can leave the filtrate in the ascending limb of Henle's loop.",
      "Large amounts of it can be reabsorbed from the collecting duct."]),
  _opts, "C",
  "Handling of water along the nephron",
  "NCERT: filtration takes place through the endothelium of the glomerular blood vessels, the epithelium of Bowman's "
  "capsule and a basement membrane between them. Reabsorption of water is passive in the initial segments of the "
  "nephron. The descending limb of Henle's loop is permeable to water but almost impermeable to electrolytes; the "
  "ascending limb is impermeable to water. Large amounts of water can be reabsorbed from the collecting duct to "
  "produce concentrated urine.",
  ["(a) true", "(b) true", "(c) true", "(d) false – ascending limb impermeable to water", "(e) true"],
  R_EXC("urine formation; function of the tubules"),
  why_others_wrong="A and B include (d); D leaves out the correct (b).",
  seconds=60)
ms_check("abce", _opts, "C")

_items = {"Reptiles": True, "Birds": True, "Land snails": True, "Marine fishes": False, "Mammals": False,
          "Aquatic amphibians": False, "Bony fishes": False, "Terrestrial amphibians": False}
_opts = ["3", "4", "5", "6"]
Z(EXC, "Modes of excretion", "Advanced", "direct",
  "How many of the following groups does NCERT describe as excreting their nitrogenous wastes mainly as uric acid "
  "(uricotelic)?\n\n" + ", ".join(_items),
  _opts, "A",
  "Ammonotelic, ureotelic and uricotelic animals",
  "NCERT: many bony fishes, aquatic amphibians and aquatic insects are ammonotelic; mammals, many terrestrial "
  "amphibians and marine fishes are ureotelic; reptiles, birds, land snails and insects are uricotelic. From the "
  "list, reptiles, birds and land snails are uricotelic.",
  ["Uricotelic → reptiles, birds, land snails = 3", "Ureotelic → marine fishes, mammals, terrestrial amphibians",
   "Ammonotelic → aquatic amphibians, bony fishes"],
  R_EXC("introduction – modes of excretion"),
  why_others_wrong="B, C and D add ureotelic or ammonotelic groups – often the terrestrial amphibians, which are "
                   "ureotelic.",
  seconds=45)
count_check(_items, _opts, "A")

Z(EXC, "Urine formation", "Advanced", "assertion_reason",
  ar("In a healthy person, the urine contains every constituent of the glomerular filtrate in the same proportion as "
     "the filtrate.",
     "Nearly 99 per cent of the filtrate has to be reabsorbed by the renal tubules."),
  ASSERTION_REASON, "D",
  "Selective reabsorption",
  "NCERT: comparing the filtrate formed per day (180 L) with the urine released (1.5 L) shows that nearly 99 per cent "
  "of the filtrate has to be reabsorbed by the renal tubules. Reabsorption is selective – glucose, amino acids and Na⁺ "
  "are reabsorbed actively, nitrogenous wastes passively – and substances like H⁺, K⁺ and ammonia are secreted. So the "
  "urine does not have the same proportions as the filtrate; A is false and R is true.",
  ["R → true (≈99% reabsorbed)", "Selective reabsorption and secretion change the proportions", "A → false"],
  R_EXC("urine formation – reabsorption and secretion"),
  why_others_wrong="A and B accept a false A; C rejects NCERT's true statement R.",
  seconds=40)

Z(EXC, "Regulation of kidney function", "Advanced", "statement_pair",
  sp("Both atrial natriuretic factor (ANF) and the renin–angiotensin mechanism tend to raise the blood pressure.",
     "ANF can cause vasodilation and thereby decrease the blood pressure, acting as a check on the renin–angiotensin "
     "mechanism."),
  STATEMENT_PAIR, "D",
  "ANF versus the renin–angiotensin mechanism",
  "NCERT: an increase in blood flow to the atria of the heart can cause the release of ANF. ANF can cause "
  "vasodilation (dilation of blood vessels) and thereby decrease the blood pressure; the ANF mechanism therefore acts "
  "as a check on the renin–angiotensin mechanism, which raises blood pressure. Statement I is false because ANF "
  "lowers blood pressure.",
  ["Statement I → false", "Statement II → true"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A and C accept that ANF raises blood pressure; B rejects the true Statement II.",
  seconds=35)


# ================================================================ Locomotion and Movement (B4 I5 A4)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Muscle contraction", "Basic", "direct",
  "Each meromyosin of a thick filament has a globular head with a short arm and a tail. NCERT calls the tail the:",
  ["Heavy meromyosin (HMM)", "Tropomyosin", "Light meromyosin (LMM)", "Troponin"], "C",
  "Structure of meromyosin",
  "NCERT: each myosin (thick) filament is a polymerised protein of many monomeric proteins called meromyosins. Each "
  "meromyosin has two important parts – a globular head with a short arm, called heavy meromyosin (HMM), and a tail, "
  "called light meromyosin (LMM). Tropomyosin and troponin are proteins of the thin (actin) filament.",
  ["Head + short arm → HMM", "Tail → LMM"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="A is the head with its short arm; B and D belong to the actin filament.",
  seconds=25)

Z(LOC, "Muscle contraction", "Basic", "statement_pair",
  sp("The light bands of a myofibril contain actin and are called I-bands or isotropic bands.",
     "The dark bands of a myofibril contain myosin and are called A-bands or anisotropic bands."),
  STATEMENT_PAIR, "A",
  "Bands of a myofibril",
  "NCERT: each myofibril has alternate dark and light bands. The light bands contain actin and are called I-band or "
  "isotropic band, whereas the dark band, called 'A' or anisotropic band, contains myosin.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("skeletal muscle"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(LOC, "Skeletal system", "Basic", "assertion_reason",
  ar("Each rib is called bicephalic.",
     "The first seven pairs of ribs are called true ribs."),
  ASSERTION_REASON, "B",
  "Ribs",
  "NCERT: each rib is a thin flat bone connected dorsally to the vertebral column and ventrally to the sternum; it has "
  "two articulation surfaces on its dorsal end and is hence called bicephalic. NCERT also states that the first seven "
  "pairs are true ribs, attached dorsally to the thoracic vertebrae and ventrally to the sternum. The ventral "
  "attachment of the true ribs has nothing to do with the two dorsal articulation surfaces that make every rib "
  "bicephalic.",
  ["A → true (two dorsal articulation surfaces)", "R → true", "R concerns ventral attachment → does not explain A"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A links two unrelated features of ribs; C and D reject true statements.",
  seconds=30)

Z(LOC, "Skeletal system", "Basic", "match_list",
  ml(("bone", "description in NCERT"), ["Clavicle", "Femur", "Patella", "Hyoid"],
     ["Single U-shaped bone present at the base of the buccal cavity", "Cup-shaped bone that covers the knee "
      "ventrally", "Longest bone of the body", "Long slender bone with two curvatures, commonly called the collar "
      "bone"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "II", "III", "I"),
                                            M("IV", "III", "I", "II")], "D"), "D",
  "Identifying individual bones",
  "NCERT: each clavicle is a long slender bone with two curvatures, commonly called the collar bone; the femur (thigh "
  "bone) is the longest bone of the body; the patella is a cup-shaped bone that covers the knee ventrally (knee cap); "
  "a single U-shaped bone called the hyoid is present at the base of the buccal cavity.",
  ["Clavicle → IV", "Femur → III", "Patella → II", "Hyoid → I"],
  R_LOC("skeletal system"),
  why_others_wrong="A swaps the clavicle and the femur; B swaps the femur and the patella; C swaps the patella and "
                   "the hyoid.",
  seconds=30)

_limbs, _pectoral, _pelvic = 4 * 30, 2 * 2, 2
_appendicular = _limbs + _pectoral + _pelvic
_phalanges = 4 * 14
assert _appendicular == 126 and _appendicular - _phalanges == 70
assert _limbs - _phalanges == 64 and (_limbs + _pectoral + 6) - _phalanges == 74
Z(LOC, "Skeletal system", "Intermediate", "numerical",
  "Each upper limb and each lower limb has 30 bones, of which 14 are phalanges. Each half of the pectoral girdle has "
  "a clavicle and a scapula, and the pelvic girdle consists of two coxal bones. How many bones of the appendicular "
  "skeleton (limbs plus girdles) are NOT phalanges?",
  ["56", "70", "64", "74"], "B",
  "Counting bones of the appendicular skeleton",
  "NCERT: the appendicular skeleton is made of the bones of the limbs along with their girdles. Four limbs × 30 = "
  "120 bones; pectoral girdle 2 × 2 = 4; pelvic girdle = 2 coxal bones. Total = 126. Phalanges = 4 × 14 = 56. "
  "Non-phalangeal bones = 126 − 56 = 70.",
  ["Limbs = 4 × 30 = 120", "Girdles = 4 + 2 = 6", "Appendicular = 126", "Phalanges = 4 × 14 = 56",
   "126 − 56 = 70"],
  R_LOC("skeletal system – appendicular skeleton"),
  why_others_wrong="A is the number of phalanges itself; C forgets the girdles; D counts each coxal bone as its three "
                   "fused bones (ilium, ischium, pubis).",
  seconds=70, verified_by=RECOMPUTED)

_opts = ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only", "(a), (b), (c) and (d) only"]
Z(LOC, "Skeletal system", "Intermediate", "multi_statement",
  ms("Which of the following statements about the human skull are correct, according to NCERT?",
     ["The cranium is made of 8 bones that form a hard protective outer covering for the brain.",
      "The facial region is made up of 14 skeletal elements which form the front part of the skull.",
      "The hyoid, a single U-shaped bone at the base of the buccal cavity, is included in the skull.",
      "The skull articulates with the vertebral column with the help of two occipital condyles (dicondylic skull).",
      "Each middle ear contains two tiny bones, the ear ossicles."]),
  _opts, "D",
  "The human skull",
  "NCERT: the skull is composed of cranial and facial bones totalling 22 – the cranium has 8 bones and the facial "
  "region 14 skeletal elements. A single U-shaped hyoid at the base of the buccal cavity is also included in the "
  "skull. Each middle ear contains THREE tiny bones – malleus, incus and stapes – collectively called ear ossicles. "
  "The skull articulates with the superior region of the vertebral column with the help of two occipital condyles "
  "(dicondylic skull).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – three ossicles in each middle ear"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A leaves out the correct (d); B and C include (e).",
  seconds=50)
ms_check("abcd", _opts, "D")

Z(LOC, "Muscle contraction", "Intermediate", "assertion_reason",
  ar("During muscle contraction, the Z-lines of a sarcomere are pulled closer to each other.",
     "The myosin cross bridges pull the attached actin filaments towards the centre of the A-band, and the Z-lines "
     "are attached to these actin filaments."),
  ASSERTION_REASON, "A",
  "Sliding filament mechanism",
  "NCERT: the myosin head binds to the exposed active sites on actin to form a cross bridge, which pulls the attached "
  "actin filaments towards the centre of the 'A' band. The 'Z' line attached to these actins is also pulled inwards, "
  "thereby causing a shortening of the sarcomere, i.e. contraction. R is the mechanism by which the Z-lines come "
  "closer – it explains A.",
  ["A → true", "R → true", "Actins pulled to the A-band centre drag the Z-lines with them → R explains A"],
  R_LOC("mechanism of muscle contraction"),
  why_others_wrong="B misses the direct cause; C and D reject statements that NCERT makes.",
  seconds=35)

Z(LOC, "Skeletal system", "Intermediate", "statement_pair",
  sp("The number of cervical vertebrae is seven in almost all mammals, including human beings.",
     "The vertebral column is dorsally placed and extends from the base of the skull."),
  STATEMENT_PAIR, "A",
  "The vertebral column",
  "NCERT: the vertebral column is formed by 26 serially arranged units called vertebrae and is dorsally placed. It "
  "extends from the base of the skull and constitutes the main framework of the trunk. The number of cervical "
  "vertebrae is seven in almost all mammals including human beings.",
  ["Statement I → true", "Statement II → true"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=30)

Z(LOC, "Joints", "Intermediate", "match_list",
  ml(("structure", "what articulates with it"), ["Glenoid cavity", "Acetabulum", "Acromion", "Occipital condyles"],
     ["Clavicle", "Atlas (first vertebra)", "Head of the humerus", "Thigh bone (femur)"]),
  match_options(M("III", "IV", "I", "II"), [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"),
                                            M("I", "IV", "III", "II")], "C"), "C",
  "Articulations of the skeleton",
  "NCERT: below the acromion of the scapula is a depression called the glenoid cavity, which articulates with the "
  "head of the humerus to form the shoulder joint; the clavicle articulates with the acromion. At the point of "
  "fusion of the ilium, ischium and pubis is a cavity called the acetabulum, to which the thigh bone articulates. The "
  "first vertebra, the atlas, articulates with the occipital condyles of the skull.",
  ["Glenoid cavity → humerus (III)", "Acetabulum → femur (IV)", "Acromion → clavicle (I)",
   "Occipital condyles → atlas (II)"],
  R_LOC("skeletal system – appendicular and axial skeleton"),
  why_others_wrong="A swaps the glenoid cavity and the acetabulum; B swaps the acromion and the occipital condyles; D "
                   "swaps the glenoid cavity and the acromion.",
  seconds=45)

_items = {"Knee joint": True, "Joint between the humerus and the pectoral girdle": True,
          "Joint between the atlas and the axis": True, "Joint between the carpals": True,
          "Joint between the carpal and the metacarpal of the thumb": True,
          "Joints between adjacent vertebrae": False, "Sutures between the flat bones of the skull": False}
_opts = ["4", "5", "6", "7"]
Z(LOC, "Joints", "Advanced", "direct",
  "How many of the following are synovial joints, according to NCERT?\n\n" + "; ".join(_items),
  _opts, "B",
  "Fibrous, cartilaginous and synovial joints",
  "NCERT: synovial joints have a fluid-filled synovial cavity between the articulating surfaces. Examples: ball and "
  "socket (humerus and pectoral girdle), hinge (knee), pivot (atlas and axis), gliding (between the carpals) and "
  "saddle (carpal and metacarpal of the thumb). The joint between adjacent vertebrae is cartilaginous, and the "
  "sutures of the cranium are fibrous joints.",
  ["Synovial → knee, shoulder, atlas–axis, carpals, thumb = 5", "Cartilaginous → adjacent vertebrae",
   "Fibrous → skull sutures"],
  R_LOC("joints"),
  why_others_wrong="A misses one synovial joint; C counts the vertebral joints; D counts every joint listed.",
  seconds=50)
count_check(_items, _opts, "B")

_opts = ["(a), (c) and (e) only", "(c), (d) and (e) only", "(a), (b) and (e) only", "(a), (b), (c) and (e) only"]
Z(LOC, "Skeletal system", "Advanced", "multi_statement",
  ms("Which of the following bones are present as a pair (one on each side of the body), rather than as a single "
     "median bone?",
     ["Clavicle", "Sternum", "Patella", "Hyoid", "Scapula"]),
  _opts, "A",
  "Paired and median bones",
  "NCERT: each half of the pectoral girdle consists of a clavicle and a scapula, so both are paired; each lower limb "
  "has a patella, so there are two. The sternum is a flat bone on the ventral midline of the thorax, and the hyoid is "
  "a single U-shaped bone at the base of the buccal cavity – both are single median bones.",
  ["(a) paired – one clavicle in each half of the pectoral girdle", "(b) single – ventral midline",
   "(c) paired – one in each lower limb", "(d) single – U-shaped bone", "(e) paired"],
  R_LOC("skeletal system"),
  why_others_wrong="B includes the hyoid and drops the clavicle; C and D include the sternum.",
  seconds=45)
ms_check("ace", _opts, "A")

Z(LOC, "Muscle contraction", "Advanced", "assertion_reason",
  ar("White muscle fibres depend on anaerobic processes for energy.",
     "White muscle fibres contain plenty of mitochondria."),
  ASSERTION_REASON, "C",
  "Red and white muscle fibres",
  "NCERT: some muscles possess very little myoglobin and appear pale or whitish – the white fibres. The number of "
  "mitochondria is also few in them, but the amount of sarcoplasmic reticulum is high, and they depend on anaerobic "
  "processes for energy. Plenty of mitochondria is a feature of red (aerobic) fibres. A is true, R is false.",
  ["A → true", "R → false (white fibres have few mitochondria)"],
  R_LOC("skeletal muscle – red and white fibres"),
  why_others_wrong="A and B accept many mitochondria in white fibres; D rejects the true A.",
  seconds=35)

Z(LOC, "Skeletal system", "Advanced", "statement_pair",
  sp("The 8th, 9th and 10th pairs of ribs do not articulate directly with the sternum but join the seventh rib with "
     "the help of hyaline cartilage.",
     "The 11th and 12th pairs of ribs are not connected dorsally to the vertebral column."),
  STATEMENT_PAIR, "C",
  "True, false and floating ribs",
  "NCERT: there are 12 pairs of ribs, each connected dorsally to the vertebral column. The first seven pairs are true "
  "ribs. The 8th, 9th and 10th pairs do not articulate directly with the sternum but join the seventh rib with the "
  "help of hyaline cartilage – the vertebrochondral (false) ribs. The last two pairs (11th and 12th) are not "
  "connected VENTRALLY and are therefore called floating ribs; dorsally they are attached to the vertebral column "
  "like every other rib.",
  ["Statement I → true", "Statement II → false: floating ribs are free ventrally, not dorsally"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="A and D accept that floating ribs are free dorsally; B rejects the true Statement I.",
  seconds=40)


# ================================================================ Neural Control and Coordination (B4 I5 A4)
R_NEU = lambda s: ref("Neural Control and Coordination", s)

Z(NEU, "Nervous system divisions", "Basic", "direct",
  "The whole complex of nerves, fibres, ganglia and plexuses by which impulses travel from the CNS to the viscera "
  "and from the viscera to the CNS is the visceral nervous system. According to NCERT, it is a part of the:",
  ["Central neural system", "Spinal cord", "Peripheral neural system", "Forebrain"],
  "C",
  "Divisions of the human neural system",
  "NCERT: the human neural system is divided into the central neural system (brain and spinal cord) and the "
  "peripheral neural system (all the nerves associated with the CNS). The visceral nervous system is the part of the "
  "peripheral nervous system that comprises the whole complex of nerves, fibres, ganglia and plexuses by which "
  "impulses travel from the CNS to the viscera and from the viscera to the CNS.",
  ["CNS → brain + spinal cord", "Visceral nervous system → nerves, fibres, ganglia, plexuses → PNS"],
  R_NEU("human neural system"),
  why_others_wrong="A, B and D name the CNS or parts of it, whereas nerves, ganglia and plexuses outside the brain "
                   "and spinal cord form the PNS.",
  seconds=25)

Z(NEU, "Neuron and nerves", "Basic", "statement_pair",
  sp("In a myelinated nerve fibre, the myelin sheath around the axon is formed by Schwann cells.",
     "The gaps between two adjacent myelin sheaths are called nodes of Ranvier."),
  STATEMENT_PAIR, "A",
  "Myelinated nerve fibres",
  "NCERT: the myelinated nerve fibres are enveloped with Schwann cells, which form a myelin sheath around the axon. "
  "The gaps between two adjacent myelin sheaths are called nodes of Ranvier. Myelinated fibres are found in spinal "
  "and cranial nerves.",
  ["Statement I → true", "Statement II → true"],
  R_NEU("structure of neuron"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(NEU, "Nervous system divisions", "Basic", "assertion_reason",
  ar("The cerebral cortex is referred to as the grey matter.",
     "The cerebral cortex contains motor areas, sensory areas and large regions that are neither clearly sensory nor "
     "motor in function."),
  ASSERTION_REASON, "B",
  "Cerebral cortex",
  "NCERT: the layer of cells covering the cerebral hemisphere is the cerebral cortex; it is referred to as the grey "
  "matter due to its greyish appearance, the neuron cell bodies being concentrated there. NCERT also states that the "
  "cortex contains motor areas, sensory areas and association areas. The kinds of functional areas present have "
  "nothing to do with the grey colour, so R does not explain A.",
  ["A → true (concentrated cell bodies give a grey look)", "R → true (functional areas)",
   "Functional areas do not explain the colour → R does not explain A"],
  R_NEU("central neural system – forebrain"),
  why_others_wrong="A gives a functional reason for a structural feature; C and D reject true statements.",
  seconds=30)

Z(NEU, "Neuron and nerves", "Basic", "match_list",
  ml(("structure", "description in NCERT"), ["Cerebral aqueduct", "Arachnoid", "Nissl's granules", "Dendrites"],
     ["Short fibres that branch repeatedly and transmit impulses towards the cell body",
      "Very thin middle layer of the cranial meninges",
      "Granular bodies in the cytoplasm of the cell body and dendrites",
      "Canal that passes through the midbrain"]),
  match_options(M("IV", "II", "III", "I"), [M("II", "IV", "III", "I"), M("IV", "II", "I", "III"),
                                            M("IV", "III", "II", "I")], "B"), "B",
  "Structures of the neural system",
  "NCERT: a canal called the cerebral aqueduct passes through the midbrain; the cranial meninges are an outer dura "
  "mater, a very thin middle arachnoid and an inner pia mater; the cell body and dendrites contain certain granular "
  "bodies called Nissl's granules; dendrites are short fibres which branch repeatedly, project out of the cell body "
  "and transmit impulses towards the cell body.",
  ["Cerebral aqueduct → IV", "Arachnoid → II", "Nissl's granules → III", "Dendrites → I"],
  R_NEU("structure of neuron; central neural system"),
  why_others_wrong="A swaps the cerebral aqueduct and the arachnoid; C swaps Nissl's granules and dendrites; D swaps "
                   "the arachnoid and Nissl's granules.",
  seconds=35)

_opts = ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only"]
Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "multi_statement",
  ms("A stimulus applied at a site on a polarised axonal membrane makes the membrane at that site freely permeable "
     "to Na⁺. Which of the following statements about that site, shortly afterwards, are correct according to NCERT?",
     ["Na⁺ rushes in rapidly.",
      "The inner surface of the membrane becomes positively charged with respect to the outer surface.",
      "The membrane at the site is said to be depolarised.",
      "The electrical potential difference across the membrane at the site is the action potential, which is termed "
      "a nerve impulse.",
      "The resting potential can never be restored at this site."]),
  _opts, "C",
  "Generation of an action potential",
  "NCERT: when a stimulus is applied at a site on the polarised membrane, the membrane there becomes freely permeable "
  "to Na⁺, leading to a rapid influx of Na⁺ followed by the reversal of polarity – the outer surface becomes "
  "negatively charged and the inner positively charged. The polarity is reversed and the membrane is depolarised; "
  "the potential difference at the site is called the action potential, which is in fact termed a nerve impulse. The "
  "rise in Na⁺ permeability is extremely short-lived; it is quickly followed by a rise in K⁺ permeability, and K⁺ "
  "diffuses outside, restoring the resting potential.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – K⁺ outflow restores the resting potential"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A and D include (e); B leaves out the Na⁺ influx in (a).",
  seconds=50)
ms_check("abcd", _opts, "C")

_items = {"Voluntary movements": True, "Balance of the body": True, "Thermoregulation": True,
          "Hunger and thirst": True, "Circadian (24-hour) rhythms of the body": True,
          "Processing of vision and hearing": True, "Ultrafiltration of blood": False,
          "Production of red blood cells": False}
_opts = ["3", "4", "5", "6"]
Z(NEU, "Nervous system divisions", "Intermediate", "direct",
  "NCERT lists the functions that the human brain controls or for which it is the site of processing. How many of "
  "the following are in that list?\n\n" + "; ".join(_items),
  _opts, "D",
  "Functions of the brain",
  "NCERT: the brain is the central information processing organ and acts as the command and control system. It "
  "controls voluntary movements, balance of the body, functioning of vital involuntary organs (e.g. lungs, heart, "
  "kidneys), thermoregulation, hunger and thirst, circadian (24-hour) rhythms, activities of several endocrine glands "
  "and human behaviour. It is also the site for processing of vision, hearing, speech, memory, intelligence, emotions "
  "and thoughts. Ultrafiltration of blood takes place in the glomeruli of the kidney, and RBCs are produced in the "
  "red bone marrow.",
  ["In NCERT's list → voluntary movements, balance, thermoregulation, hunger and thirst, circadian rhythms, "
   "vision and hearing = 6", "Not in the list → ultrafiltration, RBC production"],
  R_NEU("central neural system – human brain"),
  why_others_wrong="A, B and C leave out functions NCERT lists, most often thermoregulation or the circadian rhythms.",
  seconds=45)
count_check(_items, _opts, "D")

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "assertion_reason",
  ar("In a resting neuron, the fluid outside the axon contains a high concentration of Na⁺ and a low concentration "
     "of K⁺.",
     "The sodium-potassium pump transports 3 Na⁺ outwards for 2 K⁺ into the cell."),
  ASSERTION_REASON, "A",
  "Ionic gradients across the resting axonal membrane",
  "NCERT: the axoplasm contains a high concentration of K⁺ and negatively charged proteins and a low concentration of "
  "Na⁺, while the fluid outside the axon contains a low concentration of K⁺ and a high concentration of Na⁺. NCERT "
  "states that these ionic gradients across the resting membrane are maintained by the active transport of ions by "
  "the sodium-potassium pump, which transports 3 Na⁺ outwards for 2 K⁺ into the cell. R therefore explains A.",
  ["A → true", "R → true", "NCERT: the pump maintains these ionic gradients → R explains A"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="B ignores NCERT's statement that the pump maintains the gradients; C and D reject true "
                   "statements.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Intermediate", "statement_pair",
  sp("The hypothalamus is the major coordinating centre for sensory and motor signalling.",
     "The cerebrum wraps around a structure called the thalamus."),
  STATEMENT_PAIR, "D",
  "Thalamus and hypothalamus",
  "NCERT: the cerebrum wraps around a structure called the thalamus, which is a major coordinating centre for "
  "sensory and motor signalling. The hypothalamus lies at the base of the thalamus and contains centres that control "
  "body temperature and the urge for eating and drinking, as well as neurosecretory cells. Statement I gives the "
  "thalamus's role to the hypothalamus.",
  ["Statement I → false (that is the thalamus)", "Statement II → true"],
  R_NEU("central neural system – forebrain"),
  why_others_wrong="A and C accept the hypothalamus as the sensory–motor coordinating centre; B rejects the true "
                   "Statement II.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Intermediate", "match_list",
  ml(("event in impulse transmission", "where it takes place"),
     ["Synaptic vesicles fuse with the membrane and release neurotransmitters",
      "Neurotransmitters bind to specific receptors and ion channels open",
      "Released neurotransmitters cross the fluid-filled space between the two neurons",
      "Electric current flows directly from one neuron into the other"],
     ["Electrical synapse", "Post-synaptic membrane", "Synaptic cleft",
      "Plasma membrane of the synaptic knob (pre-synaptic membrane)"]),
  match_options(M("IV", "II", "III", "I"), [M("II", "IV", "III", "I"), M("IV", "III", "II", "I"),
                                            M("IV", "II", "I", "III")], "C"), "C",
  "Steps of synaptic transmission",
  "NCERT: when an impulse arrives at the axon terminal, it stimulates the movement of synaptic vesicles towards the "
  "membrane, where they fuse with the plasma membrane and release their neurotransmitters into the synaptic cleft "
  "(the fluid-filled space separating the pre- and post-synaptic membranes of a chemical synapse). The released "
  "neurotransmitters bind to their specific receptors present on the post-synaptic membrane, and ion channels open. "
  "At electrical synapses the membranes are in very close proximity and electric current can flow directly from one "
  "neuron into the other.",
  ["Vesicle fusion → pre-synaptic membrane (IV)", "Receptor binding → post-synaptic membrane (II)",
   "Crossing the gap → synaptic cleft (III)", "Direct current flow → electrical synapse (I)"],
  R_NEU("transmission of impulses"),
  why_others_wrong="A swaps the pre- and post-synaptic membranes; B swaps receptor binding and the synaptic cleft; D "
                   "swaps the synaptic cleft and the electrical synapse.",
  seconds=45)

_opts = ["(a), (b), (c) and (d) only", "(a), (b), (d) and (e) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
Z(NEU, "Nervous system divisions", "Advanced", "multi_statement",
  ms("Which of the following statements about the human hindbrain are correct, according to NCERT?",
     ["It comprises the pons, the cerebellum and the medulla (medulla oblongata).",
      "The pons consists of fibre tracts that interconnect different regions of the brain.",
      "It contains the corpora quadrigemina.",
      "The medulla of the brain is connected to the spinal cord.",
      "The cerebellum has a very convoluted surface, which provides additional space for many more neurons."]),
  _opts, "B",
  "Structure of the hindbrain",
  "NCERT: the hindbrain comprises the pons, cerebellum and medulla (also called the medulla oblongata). The pons "
  "consists of fibre tracts that interconnect different regions of the brain. The cerebellum has a very convoluted "
  "surface in order to provide the additional space for many more neurons. The medulla of the brain is connected to "
  "the spinal cord. The corpora quadrigemina are four round swellings on the dorsal portion of the midbrain.",
  ["(a) true", "(b) true", "(c) false – corpora quadrigemina are in the midbrain", "(d) true", "(e) true"],
  R_NEU("central neural system – hindbrain"),
  why_others_wrong="A and C include (c); D leaves out the correct (b).",
  seconds=50)
ms_check("abde", _opts, "B")

Z(NEU, "Neuron and nerves", "Advanced", "assertion_reason",
  ar("Afferent nerve fibres carry regulatory impulses from the CNS to the muscles.",
     "Efferent nerve fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues and "
     "organs."),
  ASSERTION_REASON, "D",
  "Afferent and efferent fibres",
  "NCERT: the nerve fibres of the PNS are of two types – afferent fibres transmit impulses from tissues/organs to the "
  "CNS, and efferent fibres transmit regulatory impulses from the CNS to the concerned peripheral tissues/organs. A "
  "describes efferent fibres but names them afferent, so A is false; R is true.",
  ["Afferent → towards the CNS", "Efferent → away from the CNS", "A → false", "R → true"],
  R_NEU("human neural system"),
  why_others_wrong="A and B accept the reversed direction for afferent fibres; C rejects the true R.",
  seconds=30)

Z(NEU, "Nerve impulse generation and conduction", "Advanced", "statement_pair",
  sp("In the resting state, the axonal membrane is impermeable to the negatively charged proteins present in the "
     "axoplasm.",
     "In the resting state, the outer surface of the axonal membrane possesses a negative charge, while its inner "
     "surface is positively charged."),
  STATEMENT_PAIR, "C",
  "The polarised membrane",
  "NCERT: the axonal membrane is comparatively more permeable to K⁺ and nearly impermeable to Na⁺; similarly, the "
  "membrane is impermeable to the negatively charged proteins present in the axoplasm. In the resting state, the "
  "outer surface of the axonal membrane possesses a POSITIVE charge while its inner surface becomes negatively "
  "charged – it is polarised. The charges in Statement II describe a depolarised site, not a resting one.",
  ["Statement I → true", "Statement II → false: at rest the outside is positive and the inside negative"],
  R_NEU("generation and conduction of nerve impulse"),
  why_others_wrong="A and D accept the reversed resting charges; B rejects the true Statement I.",
  seconds=35)

Z(NEU, "Nervous system divisions", "Advanced", "match_list",
  ml(("effect of damage", "structure most likely damaged"),
     ["Loss of communication between the two cerebral hemispheres",
      "Disturbed control of body temperature and of the urge for eating and drinking",
      "Failure of the centres that control respiration, cardiovascular reflexes and gastric secretions",
      "Disturbed regulation of sexual behaviour and of emotional reactions such as excitement, pleasure, rage and "
      "fear, together with the hypothalamus"],
     ["Limbic system (amygdala and hippocampus)", "Medulla oblongata", "Hypothalamus", "Corpus callosum"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "I", "II", "III"), M("III", "IV", "II", "I"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Functions localised to brain regions",
  "NCERT: the two cerebral hemispheres are connected by a tract of nerve fibres, the corpus callosum. The "
  "hypothalamus contains centres which control body temperature and the urge for eating and drinking. The medulla "
  "contains centres which control respiration, cardiovascular reflexes and gastric secretions. The limbic system "
  "(with the amygdala and hippocampus), along with the hypothalamus, is involved in the regulation of sexual "
  "behaviour and the expression of emotional reactions.",
  ["A → corpus callosum (IV)", "B → hypothalamus (III)", "C → medulla (II)", "D → limbic system (I)"],
  R_NEU("central neural system – forebrain and hindbrain"),
  why_others_wrong="A swaps the hypothalamus and the limbic system; B swaps the corpus callosum and the hypothalamus; "
                   "C swaps the hypothalamus and the medulla.",
  seconds=55)


# ================================================================ Chemical Coordination and Integration (B5 I7 A5)
R_CCI = lambda s: ref("Chemical Coordination and Integration", s)

Z(CCI, "Hypothalamus and pituitary", "Basic", "direct",
  "The pituitary gland is located in a bony cavity called the:",
  ["Foramen magnum", "Acetabulum", "Glenoid cavity", "Sella turcica"], "D",
  "Location of the pituitary",
  "NCERT: the pituitary gland is located in a bony cavity called the sella turcica and is attached to the "
  "hypothalamus by a stalk. The foramen magnum is the opening in the skull through which the medulla continues into "
  "the spinal cord; the acetabulum and glenoid cavity are sockets of the girdles.",
  ["Pituitary → sella turcica, attached to the hypothalamus by a stalk"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="A is an opening of the skull; B is a socket of the pelvic girdle and C of the scapula.",
  seconds=20)

Z(CCI, "Adrenal, pancreas and gonads", "Basic", "direct",
  "The corticoids that are involved in regulating the balance of water and electrolytes in our body are called:",
  ["Glucocorticoids", "Mineralocorticoids", "Catecholamines", "Iodothyronines"], "B",
  "Classes of corticoids",
  "NCERT: the adrenal cortex secretes many hormones, commonly called corticoids. Corticoids involved in carbohydrate "
  "metabolism are glucocorticoids (mainly cortisol); those which regulate the balance of water and electrolytes are "
  "mineralocorticoids (mainly aldosterone). Catecholamines come from the adrenal medulla and iodothyronines from the "
  "thyroid.",
  ["Water and electrolyte balance → mineralocorticoids (aldosterone)"],
  R_CCI("human endocrine system – adrenal gland"),
  why_others_wrong="A regulate carbohydrate metabolism; C are adrenal medullary hormones; D are thyroid hormones.",
  seconds=20)

Z(CCI, "Thyroid, parathyroid and pineal", "Basic", "statement_pair",
  sp("Thyroid hormones control the metabolism of carbohydrates, proteins and fats.",
     "Maintenance of water and electrolyte balance is also influenced by thyroid hormones."),
  STATEMENT_PAIR, "A",
  "Actions of thyroid hormones",
  "NCERT: thyroid hormones play an important role in the regulation of the basal metabolic rate, support RBC "
  "formation, control the metabolism of carbohydrates, proteins and fats, and also influence the maintenance of water "
  "and electrolyte balance.",
  ["Statement I → true", "Statement II → true"],
  R_CCI("human endocrine system – thyroid gland"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(CCI, "Thyroid, parathyroid and pineal", "Basic", "assertion_reason",
  ar("The pineal gland secretes the hormone melatonin.",
     "The pineal gland is located on the dorsal side of the forebrain."),
  ASSERTION_REASON, "B",
  "The pineal gland",
  "NCERT: the pineal gland is located on the dorsal side of the forebrain and secretes a hormone called melatonin. "
  "Both statements are true, but the position of a gland does not explain which hormone it secretes; R does not "
  "explain A.",
  ["A → true", "R → true", "Location does not determine the secretion → R does not explain A"],
  R_CCI("human endocrine system – pineal gland"),
  why_others_wrong="A treats the location as the reason for the secretion; C and D reject true statements.",
  seconds=25)

Z(CCI, "Adrenal, pancreas and gonads", "Basic", "match_list",
  ml(("hormone", "description in NCERT"), ["Insulin", "Glucagon", "Parathyroid hormone", "Melatonin"],
     ["Hypercalcemic hormone", "Regulates the 24-hour (diurnal) rhythm of the body",
      "Hyperglycemic hormone", "Moves glucose rapidly from blood into hepatocytes and adipocytes, lowering blood "
      "glucose (hypoglycemia)"]),
  match_options(M("IV", "III", "I", "II"), [M("III", "IV", "I", "II"), M("IV", "III", "II", "I"),
                                            M("IV", "I", "III", "II")], "C"), "C",
  "Hormones and their effects on blood constituents",
  "NCERT: insulin enhances cellular glucose uptake and utilisation, so glucose moves rapidly from blood to hepatocytes "
  "and adipocytes, resulting in decreased blood glucose (hypoglycemia). Glucagon is a hyperglycemic hormone. "
  "Parathyroid hormone increases the Ca²⁺ level in blood and is a hypercalcemic hormone. Melatonin plays an important "
  "role in the regulation of the 24-hour (diurnal) rhythm of our body.",
  ["Insulin → IV", "Glucagon → III", "PTH → I", "Melatonin → II"],
  R_CCI("human endocrine system – pancreas, parathyroid gland and pineal gland"),
  why_others_wrong="A swaps insulin and glucagon; B swaps PTH and melatonin; D swaps glucagon and PTH.",
  seconds=30)

_opts = ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (b) only", "(a), (b) and (c) only"]
Z(CCI, "Adrenal, pancreas and gonads", "Intermediate", "multi_statement",
  ms("Which of the following are secreted by the adrenal cortex, according to NCERT?",
     ["Cortisol", "Aldosterone", "Small amounts of androgenic steroids", "Adrenaline", "Noradrenaline"]),
  _opts, "D",
  "Secretions of the adrenal cortex and medulla",
  "NCERT: the adrenal cortex secretes corticoids – glucocorticoids (mainly cortisol), mineralocorticoids (mainly "
  "aldosterone) – and small amounts of androgenic steroids, which play a role in the growth of axial, pubic and "
  "facial hair during puberty. Adrenaline (epinephrine) and noradrenaline (norepinephrine), the catecholamines, are "
  "secreted by the adrenal medulla.",
  ["(a) cortex", "(b) cortex", "(c) cortex", "(d) medulla", "(e) medulla"],
  R_CCI("human endocrine system – adrenal gland"),
  why_others_wrong="A and B include medullary catecholamines; C leaves out the androgenic steroids.",
  seconds=40)
ms_check("abc", _opts, "D")

Z(CCI, "Adrenal, pancreas and gonads", "Intermediate", "direct",
  "Which hormone does NCERT describe as producing anti-inflammatory reactions and suppressing the immune response?",
  ["Cortisol", "Aldosterone", "Thymosin", "Adrenaline"], "A",
  "Actions of cortisol",
  "NCERT: glucocorticoids, particularly cortisol, produce anti-inflammatory reactions and suppress the immune "
  "response. Aldosterone acts on the renal tubules; thymosins promote immunity (differentiation of T-lymphocytes and "
  "antibody production); adrenaline is an emergency hormone.",
  ["Anti-inflammatory + immunosuppressive → cortisol (a glucocorticoid)"],
  R_CCI("human endocrine system – adrenal gland"),
  why_others_wrong="B regulates water and electrolyte balance; C promotes rather than suppresses immunity; D prepares "
                   "the body for fight or flight.",
  seconds=30)

Z(CCI, "Hormonal disorders", "Intermediate", "assertion_reason",
  ar("A person with pituitary dwarfism shows stunted growth.",
     "Pituitary dwarfism results from low secretion of growth hormone."),
  ASSERTION_REASON, "A",
  "Growth hormone deficiency",
  "NCERT: low secretion of GH results in stunted growth, resulting in pituitary dwarfism. Stunted growth is the direct "
  "consequence of too little growth hormone, so R explains A.",
  ["A → true", "R → true", "Too little GH → stunted growth → R explains A"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="B misses the direct cause; C and D reject statements that NCERT makes.",
  seconds=25)

Z(CCI, "Hypothalamus and pituitary", "Intermediate", "statement_pair",
  sp("In females, LH induces ovulation of fully mature follicles (Graafian follicles) and maintains the corpus "
     "luteum.",
     "In females, FSH stimulates the growth and development of the ovarian follicles."),
  STATEMENT_PAIR, "A",
  "Gonadotrophins in females",
  "NCERT: in females, LH induces ovulation of fully mature follicles (Graafian follicles) and maintains the corpus "
  "luteum formed from the remnants of the Graafian follicles after ovulation. FSH stimulates the growth and "
  "development of the ovarian follicles in females.",
  ["Statement I → true", "Statement II → true"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=30)

Z(CCI, "Adrenal, pancreas and gonads", "Intermediate", "match_list",
  ml(("hormone", "one effect described in NCERT"), ["Catecholamines", "Androgens", "Estrogens", "Cortisol"],
     ["Stimulates RBC production", "High pitch of voice, among the female secondary sex characters",
      "Pupillary dilation and piloerection (raising of hairs)", "Muscular growth and a low pitch of voice"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "B"), "B",
  "Effects of adrenal and gonadal hormones",
  "NCERT: adrenaline and noradrenaline increase alertness, pupillary dilation, piloerection and sweating. Androgens "
  "stimulate muscular growth, growth of facial and axillary hair, aggressiveness and a low pitch of voice. Estrogens "
  "stimulate the appearance of female secondary sex characters, e.g. a high pitch of voice. Cortisol stimulates RBC "
  "production.",
  ["Catecholamines → III", "Androgens → IV", "Estrogens → II", "Cortisol → I"],
  R_CCI("human endocrine system – adrenal gland; testis; ovary"),
  why_others_wrong="A swaps catecholamines and androgens; C swaps estrogens and cortisol; D swaps androgens and "
                   "estrogens.",
  seconds=40)

Z(CCI, "Hormonal disorders", "Intermediate", "direct",
  "According to NCERT, hypothyroidism in adult women may cause:",
  ["Protruding eyeballs", "Vigorous contraction of the uterus", "Excessive pigmentation of the skin",
   "The menstrual cycle to become irregular"], "D",
  "Effect of hypothyroidism in adult women",
  "NCERT: in adult women, hypothyroidism may cause the menstrual cycle to become irregular. Protruding eyeballs are a "
  "feature of exophthalmic goitre, a form of HYPERthyroidism; vigorous uterine contraction at child birth is caused "
  "by oxytocin; pigmentation is regulated by MSH.",
  ["Hypothyroidism in adult women → irregular menstrual cycle"],
  R_CCI("human endocrine system – thyroid gland"),
  why_others_wrong="A belongs to hyperthyroidism; B is an action of oxytocin; C relates to MSH, not the thyroid.",
  seconds=25)

_opts = ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only", "(a), (b) and (c) only"]
Z(CCI, "Thyroid, parathyroid and pineal", "Intermediate", "multi_statement",
  ms("Which of the following statements about the thymus are correct, according to NCERT?",
     ["It is a lobular structure.",
      "It is located between the lungs behind the sternum on the ventral side of the aorta.",
      "Its hormones, thymosins, play a major role in the differentiation of T-lymphocytes, which provide "
      "cell-mediated immunity.",
      "Thymosins also promote the production of antibodies to provide humoral immunity.",
      "The thymus enlarges in old individuals, increasing the production of thymosins."]),
  _opts, "A",
  "The thymus",
  "NCERT: the thymus gland is a lobular structure located between the lungs behind the sternum on the ventral side "
  "of the aorta. It secretes peptide hormones called thymosins, which play a major role in the differentiation of "
  "T-lymphocytes (cell-mediated immunity) and also promote the production of antibodies (humoral immunity). The "
  "thymus is degenerated in old individuals, resulting in decreased production of thymosins, so their immune "
  "responses become weak.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – the thymus degenerates with age"],
  R_CCI("human endocrine system – thymus"),
  why_others_wrong="B and C include (e); D leaves out the correct (d).",
  seconds=50)
ms_check("abcd", _opts, "A")

_opts = ["(a), (b) and (e) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"]
Z(CCI, "Mechanism of hormone action", "Advanced", "multi_statement",
  ms("Compare the action of FSH (a pituitary protein hormone) with that of estradiol (a steroid) on their target "
     "cells. Which of the following statements are correct according to NCERT?",
     ["FSH binds to membrane-bound receptors and does not normally enter the target cell.",
      "Binding of FSH generates second messengers such as cyclic AMP, which regulate cellular metabolism.",
      "Estradiol interacts with intracellular receptors.",
      "The estradiol–receptor complex mostly regulates gene expression or chromosome function by interacting with "
      "the genome.",
      "FSH acts mainly by entering the nucleus and binding to the genome."]),
  _opts, "B",
  "Two mechanisms of hormone action",
  "NCERT: hormones which interact with membrane-bound receptors (peptide, polypeptide and protein hormones, such as "
  "the pituitary hormones) normally do not enter the target cell, but generate second messengers (e.g. cyclic AMP, "
  "IP₃, Ca²⁺) which in turn regulate cellular metabolism. Hormones which interact with intracellular receptors (e.g. "
  "steroid hormones such as estradiol, and iodothyronines) mostly regulate gene expression or chromosome function by "
  "the interaction of the hormone–receptor complex with the genome.",
  ["FSH → protein → membrane receptor → second messenger: (a), (b) true", "Estradiol → steroid → intracellular "
   "receptor → genome: (c), (d) true", "(e) false"],
  R_CCI("mechanism of hormone action"),
  why_others_wrong="A, C and D include (e), which gives FSH the mechanism of a steroid hormone.",
  seconds=60)
ms_check("abcd", _opts, "B")

Z(CCI, "Hormonal disorders", "Advanced", "assertion_reason",
  ar("Hypothyroidism during pregnancy can cause stunted growth (cretinism) of the growing baby.",
     "Hypothyroidism increases the basal metabolic rate."),
  ASSERTION_REASON, "C",
  "Hypothyroidism and hyperthyroidism",
  "NCERT: hypothyroidism during pregnancy causes defective development and maturation of the growing baby, leading to "
  "stunted growth (cretinism), mental retardation, low intelligence quotient, abnormal skin, deaf-mutism, etc. – A is "
  "true. An increased basal metabolic rate is NCERT's description of exophthalmic goitre, a form of HYPERthyroidism; "
  "R is false.",
  ["A → true", "Raised BMR → hyperthyroidism (exophthalmic goitre)", "R → false"],
  R_CCI("human endocrine system – thyroid gland"),
  why_others_wrong="A and B accept a raised BMR in hypothyroidism; D rejects the true A.",
  seconds=40)

Z(CCI, "Hypothalamus and pituitary", "Advanced", "statement_pair",
  sp("Both the pars distalis and the pars intermedia are parts of the adenohypophysis.",
     "In humans, the pars intermedia is almost merged with the pars distalis."),
  STATEMENT_PAIR, "A",
  "Parts of the pituitary",
  "NCERT: the pituitary is divided anatomically into an adenohypophysis and a neurohypophysis. The adenohypophysis "
  "consists of two portions, the pars distalis and the pars intermedia. The pars intermedia secretes only one "
  "hormone, MSH; however, in humans, the pars intermedia is almost merged with the pars distalis.",
  ["Statement I → true", "Statement II → true"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=35)

Z(CCI, "Hypothalamus and pituitary", "Advanced", "match_list",
  ml(("pair of hormones", "common feature"),
     ["Oxytocin and vasopressin", "LH and FSH", "Adrenaline and noradrenaline", "Estrogen and progesterone"],
     ["Steroid hormones produced by the ovary", "Catecholamines secreted by the adrenal medulla",
      "Gonadotrophins secreted by the pars distalis",
      "Synthesised by the hypothalamus and released from the neurohypophysis"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Grouping hormones by origin and nature",
  "NCERT: oxytocin and vasopressin are synthesised by the hypothalamus and transported axonally to the "
  "neurohypophysis, which stores and releases them. LH and FSH, secreted by the pars distalis, stimulate gonadal "
  "activity and are called gonadotrophins. Adrenaline and noradrenaline, from the adrenal medulla, are commonly "
  "called catecholamines. The ovary produces two groups of steroid hormones, estrogen and progesterone.",
  ["Oxytocin, vasopressin → IV", "LH, FSH → III", "Adrenaline, noradrenaline → II", "Estrogen, progesterone → I"],
  R_CCI("human endocrine system"),
  why_others_wrong="A swaps the neurohypophysial hormones and the gonadotrophins; B swaps the catecholamines and the "
                   "ovarian steroids; C swaps the gonadotrophins and the catecholamines.",
  seconds=45)

Z(CCI, "Adrenal, pancreas and gonads", "Advanced", "direct",
  "In a man, the Leydig (interstitial) cells of both testes are destroyed, while the seminiferous tubules and the "
  "pituitary remain intact. Based on NCERT's account of androgens, which outcome is expected?",
  ["Androgen secretion falls, and the functions of the male accessory sex organs, the secondary sex characters and "
   "spermatogenesis are affected",
   "Androgen secretion stays normal, but spermatogenesis stops",
   "Androgen secretion falls, but spermatogenesis is not affected because it does not depend on androgens",
   "The pituitary stops secreting LH and FSH"], "A",
  "Role of androgens",
  "NCERT: the Leydig cells in the intertubular spaces produce androgens, mainly testosterone. Androgens regulate the "
  "development, maturation and functions of the male accessory sex organs (epididymis, vas deferens, seminal "
  "vesicles, prostate gland, urethra, etc.), stimulate muscular growth, facial and axillary hair, aggressiveness and "
  "a low pitch of voice, and play a major stimulatory role in spermatogenesis. Destroying the Leydig cells removes "
  "this source of androgens. Nothing in the stem stops the pituitary from secreting gonadotrophins.",
  ["Leydig cells → androgens", "Androgens → accessory organs, secondary sex characters, spermatogenesis",
   "Loss of Leydig cells → all three affected"],
  R_CCI("human endocrine system – testis"),
  why_others_wrong="B keeps androgens normal although their source is lost; C denies NCERT's stimulatory role of "
                   "androgens in spermatogenesis; D blames the pituitary, which is intact.",
  seconds=50)


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
           "notes": "BATCH_010 package ZOO_010_p1: 131 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, Locomotion and Movement, Neural Control "
                    "and Coordination, and Chemical Coordination and Integration. Facts from the rationalised NCERT "
                    "Class 11 Biology textbook, avoiding questions already asked in BATCH_000-BATCH_009 (many items "
                    "are counting, comparison or scenario questions that combine NCERT statements); every numerical "
                    "answer re-derived by tools/batch_010/ZOO_010_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
