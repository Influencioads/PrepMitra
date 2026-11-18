"""Writes batches/parts/BATCH_009_ZOO_p1.json: package ZOO_009_p1 of BATCH_009 (Zoology, 119 questions).

Topics: Animal Kingdom; Structural Organisation in Animals; Biomolecules; Breathing and Exchange of Gases; Body Fluids
and Circulation; Excretory Products and their Elimination; Locomotion and Movement. IDs NEET_ZOO_002001 ..
NEET_ZOO_002119. Every numerical answer is re-derived below before the file is written, and the plan quota, ID range,
subtopics, key balance and format mix are asserted. Facts follow the rationalised NCERT Class 11 Biology textbook; for
the frog only the systems the NMC 2026 text lists, and no earthworm or cockroach anatomy. Facts already tested in
BATCH_000 to BATCH_008 (see `merge_batch.py stems 9 ZOO_009_p1`) are not asked again in the same way; most items are
application, identification or comparison questions on NCERT content.

    python docs/neet-bank/tools/batch_009/ZOO_009_p1.py
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
PACKAGE = "ZOO_009_p1"
BATCH = "BATCH_009"
FIRST_ID, LAST_ID = 2001, 2119
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
  ml(("bony fish genus", "common name"), ["Hippocampus", "Labeo", "Clarias", "Betta"],
     ["Fighting fish", "Magur", "Sea horse", "Rohu"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "B"), "B",
  "Examples of class Osteichthyes",
  "NCERT lists bony fishes as marine – Exocoetus (Flying fish), Hippocampus (Sea horse); freshwater – Labeo (Rohu), "
  "Catla (Katla), Clarias (Magur); and aquarium – Betta (Fighting fish), Pterophyllum (Angel fish).",
  ["Hippocampus → Sea horse (III)", "Labeo → Rohu (IV)", "Clarias → Magur (II)", "Betta → Fighting fish (I)"],
  R_AK("class Osteichthyes"),
  why_others_wrong="A swaps Hippocampus and Labeo; C swaps Clarias and Betta; D swaps Labeo and Clarias.",
  seconds=30)

Z(AK, "Chordate classes", "Basic", "direct",
  "Besides a ventral muscular heart and kidneys, NCERT lists paired appendages among the features of vertebrates. "
  "These paired appendages may be:",
  ["Parapodia or tube feet", "Jointed appendages only", "Fins or limbs", "Wings only"], "C",
  "Features of subphylum Vertebrata",
  "NCERT: in addition to the basic chordate characters, vertebrates have a ventral muscular heart with two, three or "
  "four chambers, kidneys for excretion and osmoregulation, and paired appendages which may be fins or limbs.",
  ["Vertebrate paired appendages → fins (fishes) or limbs (tetrapods)"],
  R_AK("subphylum Vertebrata"),
  why_others_wrong="A names annelid and echinoderm structures; B describes arthropods; D covers only the forelimbs of "
                   "birds.",
  seconds=25)

Z(AK, "Chordate classes", "Basic", "direct",
  "According to NCERT, the body of reptiles is covered by dry and cornified skin bearing epidermal scales or:",
  ["Placoid scales", "Cycloid scales", "Feathers", "Scutes"], "D",
  "Body covering of reptiles",
  "NCERT: in class Reptilia the body is covered by dry and cornified skin, epidermal scales or scutes. Placoid scales "
  "belong to cartilaginous fishes, cycloid scales to bony fishes and feathers to birds.",
  ["Reptile skin → dry, cornified, epidermal scales or scutes"],
  R_AK("class Reptilia"),
  why_others_wrong="A is the scale type of Chondrichthyes, B of Osteichthyes, and C is the covering of Aves.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "direct",
  "Which of the following correctly describes development in arthropods, as given in NCERT?",
  ["Development may be direct or indirect", "Development is always direct",
   "Development is always indirect with a free-swimming larva", "Development occurs only through many larval stages"],
  "A",
  "Reproduction in Arthropoda",
  "NCERT: arthropods are mostly dioecious, fertilisation is usually internal, they are mostly oviparous, and "
  "development may be direct or indirect.",
  ["Arthropoda → mostly oviparous; development direct or indirect"],
  R_AK("phylum Arthropoda"),
  why_others_wrong="B and C each allow only one route; D is NCERT's description for Platyhelminthes.",
  seconds=25)

Z(AK, "Non-chordate phyla", "Basic", "statement_pair",
  sp("Annelids may be aquatic (marine and fresh water) or terrestrial; they are free-living, and sometimes parasitic.",
     "Annelids reproduce only asexually, by fragmentation."),
  STATEMENT_PAIR, "C",
  "Habitat and reproduction of annelids",
  "NCERT: annelids may be aquatic (marine and fresh water) or terrestrial; free-living, and sometimes parasitic. "
  "Reproduction in annelids is sexual. Fragmentation is NCERT's asexual method for sponges.",
  ["Statement I → true", "Statement II → false: reproduction in annelids is sexual"],
  R_AK("phylum Annelida"),
  why_others_wrong="A and D accept the false Statement II; B rejects NCERT's description of annelid habitats.",
  seconds=30)

Z(AK, "Basis of classification", "Basic", "assertion_reason",
  ar("Platyhelminthes are acoelomate animals.",
     "Platyhelminthes have an incomplete digestive system with a single opening that serves as both mouth and anus."),
  ASSERTION_REASON, "B",
  "Body cavity versus type of gut",
  "NCERT: animals in which the body cavity is absent are called acoelomates, e.g., Platyhelminthes. Separately, "
  "Platyhelminthes are NCERT's example of an incomplete digestive system with a single opening. Whether there is a "
  "cavity between the body wall and the gut wall has nothing to do with how many openings the gut has, so R does not "
  "explain A.",
  ["A → true (no body cavity)", "R → true (single opening to the gut)",
   "Body cavity and gut openings are independent features → R does not explain A"],
  R_AK("basis of classification – digestive system; coelom"),
  why_others_wrong="A wrongly links the gut openings to the absence of a coelom; C and D reject true statements.",
  seconds=35)

Z(AK, "Chordate classes", "Intermediate", "direct",
  "In which of the following animals does the notochord persist throughout life?",
  ["Ascidia", "Branchiostoma", "Balanoglossus", "Labeo"], "B",
  "Fate of the notochord in different groups",
  "NCERT: in Cephalochordata (e.g., Branchiostoma) the notochord extends from head to tail and persists throughout "
  "life. In Urochordata (Ascidia) it is present only in the larval tail. Hemichordates (Balanoglossus) have only a "
  "stomochord, a structure similar to the notochord. In vertebrates such as Labeo the notochord is replaced by a "
  "vertebral column in the adult.",
  ["Cephalochordate → notochord head to tail, lifelong", "Urochordate → larval tail only",
   "Hemichordate → stomochord, not a notochord", "Vertebrate → replaced by vertebral column"],
  R_AK("phylum Hemichordata; phylum Chordata"),
  why_others_wrong="A keeps it only in the larva; C has a stomochord; D replaces it by a bony vertebral column.",
  seconds=40)

_opts_rc = ["(a), (b) and (e) only", "(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only"]
Z(AK, "Chordate classes", "Intermediate", "multi_statement",
  ms("Compare Rana (an amphibian) with Calotes (a reptile). Which of the following statements are correct for BOTH "
     "of them, according to NCERT?",
     ["Both are cold-blooded (poikilothermous) animals.",
      "In both, a tympanum represents the ear.",
      "In both, fertilisation is internal.",
      "Both have a moist skin without scales.",
      "In both, the sexes are separate."]),
  _opts_rc, "A",
  "Amphibia compared with Reptilia",
  "NCERT: amphibians are cold-blooded, have a tympanum representing the ear, separate sexes, external fertilisation "
  "and a moist skin without scales. Reptiles are poikilotherms with a tympanum representing the ear, separate sexes, "
  "internal fertilisation and dry, cornified skin with epidermal scales or scutes.",
  ["(a) true for both", "(b) true for both", "(c) false – fertilisation is external in amphibians",
   "(d) false – reptile skin is dry and scaly", "(e) true for both"],
  R_AK("class Amphibia and class Reptilia"),
  why_others_wrong="B, C and D each include (c) or (d), which hold for only one of the two classes.",
  seconds=50)
ms_check("abe", _opts_rc, "A")

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("structure", "animal that possesses it"), ["Water vascular system", "Radula", "Parapodia", "Proboscis gland"],
     ["Nereis", "Saccoglossus", "Antedon", "Aplysia"]),
  match_options(M("III", "IV", "I", "II"), [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"),
                                            M("III", "I", "IV", "II")], "D"), "D",
  "Diagnostic structures of non-chordate phyla",
  "Water vascular system → Echinodermata (Antedon, the sea lily). Radula → Mollusca (Aplysia, the sea hare). "
  "Parapodia → aquatic annelids such as Nereis. Proboscis gland, the excretory organ → Hemichordata (Saccoglossus).",
  ["Identify the phylum of each animal", "Water vascular system → Antedon (III)", "Radula → Aplysia (IV)",
   "Parapodia → Nereis (I)", "Proboscis gland → Saccoglossus (II)"],
  R_AK("phyla Annelida, Mollusca, Echinodermata and Hemichordata"),
  why_others_wrong="A swaps the echinoderm and the mollusc; B swaps Nereis and Saccoglossus; C gives the radula to "
                   "Nereis.",
  seconds=45)

Z(AK, "Non-chordate phyla", "Intermediate", "statement_pair",
  sp("Coelenterates and ctenophores are both exclusively marine.",
     "In both coelenterates and ctenophores, digestion is both extracellular and intracellular."),
  STATEMENT_PAIR, "D",
  "Coelenterata compared with Ctenophora",
  "NCERT: coelenterates are aquatic, mostly marine, sessile or free-swimming (Hydra is NOT marine), whereas "
  "ctenophores are exclusively marine. In coelenterates, digestion in the gastro-vascular cavity is extracellular and "
  "intracellular; in ctenophores too, digestion is both extracellular and intracellular.",
  ["Statement I → false: coelenterates are only 'mostly' marine", "Statement II → true for both phyla"],
  R_AK("phyla Coelenterata and Ctenophora"),
  why_others_wrong="A and C accept Statement I, which is true only of ctenophores; B rejects the shared digestion "
                   "pattern.",
  seconds=40)

Z(AK, "Chordate classes", "Intermediate", "assertion_reason",
  ar("Scoliodon and Exocoetus are both cold-blooded (poikilothermous) animals.",
     "Both Scoliodon and Exocoetus possess an air bladder that regulates buoyancy."),
  ASSERTION_REASON, "C",
  "Cartilaginous and bony fishes compared",
  "NCERT describes both Chondrichthyes (Scoliodon, the dog fish) and Osteichthyes (Exocoetus, the flying fish) as "
  "cold-blooded. The air bladder that regulates buoyancy is found only in bony fishes; cartilaginous fishes lack it "
  "and have to swim constantly to avoid sinking.",
  ["A → true (both poikilothermous)", "R → false: Scoliodon has no air bladder"],
  R_AK("class Chondrichthyes and class Osteichthyes"),
  why_others_wrong="A and B accept R, which fails for the shark; D rejects the true Assertion.",
  seconds=35)

Z(AK, "Non-chordate phyla", "Intermediate", "match_list",
  ml(("animal", "fertilisation and development as given in NCERT"), ["Asterias", "Fasciola", "Pavo", "Bufo"],
     ["Internal fertilisation; development through many larval stages",
      "Usually external fertilisation; indirect development with a free-swimming larva",
      "Internal fertilisation; oviparous with direct development",
      "External fertilisation; oviparous with indirect development"]),
  match_options(M("II", "I", "III", "IV"), [M("I", "II", "III", "IV"), M("II", "I", "IV", "III"),
                                            M("IV", "I", "III", "II")], "A"), "A",
  "Reproductive patterns across phyla and classes",
  "NCERT: echinoderms (Asterias) – fertilisation usually external, development indirect with a free-swimming larva; "
  "Platyhelminthes (Fasciola) – internal fertilisation, development through many larval stages; birds (Pavo) – "
  "internal fertilisation, oviparous, direct development; amphibians (Bufo) – external fertilisation, oviparous, "
  "indirect development.",
  ["Asterias → II", "Fasciola → I", "Pavo → III", "Bufo → IV"],
  R_AK("phyla Platyhelminthes and Echinodermata; classes Amphibia and Aves"),
  why_others_wrong="B swaps the starfish and the liver fluke; C swaps the bird and the toad; D gives the toad's "
                   "pattern to Asterias.",
  seconds=50)

_opts_eh = ["(a), (b) and (c) only", "(b), (d) and (e) only", "(b), (c) and (e) only", "(a), (c) and (d) only"]
Z(AK, "Non-chordate phyla", "Intermediate", "multi_statement",
  ms("Which of the following statements are true for BOTH Echinodermata and Hemichordata, according to NCERT?",
     ["The adults are radially symmetrical.",
      "They are triploblastic and coelomate.",
      "The sexes are separate.",
      "A proboscis gland serves for excretion.",
      "Development is indirect."]),
  _opts_eh, "C",
  "Echinoderms compared with hemichordates",
  "NCERT: echinoderm adults are radially symmetrical (larvae bilateral) while hemichordates are bilaterally "
  "symmetrical; both are triploblastic and coelomate; sexes are separate in both; development is indirect in both. "
  "The proboscis gland is the excretory organ of hemichordates only – echinoderms have no excretory system.",
  ["(a) false – hemichordates are bilaterally symmetrical", "(b) true", "(c) true",
   "(d) false – echinoderms lack an excretory system", "(e) true"],
  R_AK("phyla Echinodermata and Hemichordata"),
  why_others_wrong="A includes (a); B includes (d); D includes both (a) and (d).",
  seconds=50)
ms_check("bce", _opts_eh, "C")

Z(AK, "Non-chordate phyla", "Intermediate", "direct",
  "Which one of the following animals does NOT belong to phylum Coelenterata (Cnidaria)?",
  ["Ctenoplana", "Physalia", "Gorgonia", "Meandrina"], "A",
  "Identifying coelenterates",
  "NCERT gives Physalia (Portuguese man-of-war), Gorgonia (sea-fan) and Meandrina (brain coral) as coelenterates. "
  "Ctenoplana, with Pleurobrachia, is NCERT's example of phylum Ctenophora (comb jellies).",
  ["Physalia, Gorgonia, Meandrina → Coelenterata", "Ctenoplana → Ctenophora"],
  R_AK("phyla Coelenterata and Ctenophora"),
  why_others_wrong="B, C and D are all listed by NCERT as examples of Coelenterata.",
  seconds=30)

_opts_egg = ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only", "(a), (c) and (e) only"]
Z(AK, "Chordate classes", "Advanced", "multi_statement",
  ms("A vertebrate is homoiothermous, has a four-chambered heart and lays eggs. Without knowing its class, which of "
     "the following can you say must be true of it, according to NCERT?",
     ["It respires by lungs.",
      "Its body is covered with feathers.",
      "Fertilisation is internal.",
      "It has mammary glands.",
      "The sexes are separate."]),
  _opts_egg, "D",
  "Reasoning from a combination of characters",
  "Among vertebrates, only birds and mammals are homoiothermous with a four-chambered heart. Birds lay eggs, and so "
  "does the mammal Ornithorhynchus (platypus), so the animal could be either. NCERT gives for both classes: "
  "respiration by lungs, internal fertilisation and separate sexes. Feathers are found only in birds and mammary "
  "glands only in mammals, so neither can be stated with certainty.",
  ["Homoiothermy + 4-chambered heart → bird or mammal", "Egg-laying → bird or Ornithorhynchus",
   "(a), (c), (e) hold for both classes", "(b) only birds; (d) only mammals"],
  R_AK("class Aves and class Mammalia"),
  why_others_wrong="A and B include (b) or (d), each true of only one possible class; C includes (d).",
  seconds=70)
ms_check("ace", _opts_egg, "D")

Z(AK, "Chordate classes", "Advanced", "assertion_reason",
  ar("An adult Ascidia does not have a notochord.",
     "In Urochordata, the notochord is present only in the larval tail."),
  ASSERTION_REASON, "A",
  "Notochord in urochordates",
  "NCERT: in Urochordata (e.g., Ascidia, Salpa, Doliolum) the notochord is present only in the larval tail. "
  "Since it is restricted to the larva, the adult has none – R directly explains A. Ascidia is still a chordate "
  "because a notochord is present at one stage of its life.",
  ["R → notochord only in the larval tail", "Adult stage → no notochord", "R explains A"],
  R_AK("phylum Chordata – subphylum Urochordata"),
  why_others_wrong="B denies the direct link; C and D reject true statements.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "match_list",
  ml(("animal", "reproductive feature"), ["Sycon", "Hirudinaria", "Nereis", "Ascaris"],
     ["Dioecious; bears parapodia that help in swimming",
      "Dioecious; females often longer than males",
      "Monoecious annelid",
      "Hermaphrodite; internal fertilisation and indirect development"]),
  match_options(M("IV", "III", "I", "II"), [M("IV", "I", "III", "II"), M("III", "IV", "I", "II"),
                                            M("IV", "III", "II", "I")], "C"), "C",
  "Sexuality across non-chordates",
  "NCERT: sponges (Sycon) are hermaphrodite, with internal fertilisation and indirect development; earthworms and "
  "leeches (Hirudinaria) are monoecious; Nereis is dioecious and its parapodia help in swimming; aschelminths "
  "(Ascaris) are dioecious, and often the females are longer than the males.",
  ["Sycon → IV", "Hirudinaria → III", "Nereis → I", "Ascaris → II"],
  R_AK("phyla Porifera, Aschelminthes and Annelida"),
  why_others_wrong="A swaps the two annelids; B swaps the sponge and the leech; D swaps Nereis and Ascaris.",
  seconds=50)

Z(AK, "Chordate classes", "Advanced", "statement_pair",
  sp("Cyclostomes, like cartilaginous fishes, have a cartilaginous cranium and vertebral column.",
     "Cyclostomes, like cartilaginous fishes, are placed in the super class Pisces."),
  STATEMENT_PAIR, "C",
  "Agnatha versus Gnathostomata",
  "NCERT: in cyclostomes the cranium and vertebral column are cartilaginous, and Chondrichthyes have a cartilaginous "
  "endoskeleton. But cyclostomes lack jaws and form the division Agnatha; Chondrichthyes and Osteichthyes form the "
  "super class Pisces under the division Gnathostomata.",
  ["Statement I → true", "Statement II → false: cyclostomes are Agnatha, not Pisces"],
  R_AK("subphylum Vertebrata – class Cyclostomata"),
  why_others_wrong="A and D accept Statement II; B rejects the shared cartilaginous skeleton.",
  seconds=40)

Z(AK, "Non-chordate phyla", "Advanced", "direct",
  "Which of the following correctly distinguishes Pleurobrachia from Obelia, as described in NCERT?",
  ["Pleurobrachia is diploblastic, whereas Obelia is triploblastic",
   "Pleurobrachia bears eight external rows of ciliated comb plates and reproduces only sexually, whereas Obelia "
   "bears cnidoblasts and shows alternation between polyp and medusa forms",
   "Pleurobrachia bears cnidoblasts on its tentacles, whereas Obelia bears comb plates",
   "Pleurobrachia shows only intracellular digestion, whereas Obelia shows only extracellular digestion"], "B",
  "Ctenophora versus Coelenterata",
  "NCERT: ctenophores (Pleurobrachia) bear eight external rows of ciliated comb plates and reproduce only by sexual "
  "means. Coelenterates possess cnidoblasts, and those existing in both body forms, like Obelia, show metagenesis – "
  "polyps produce medusae asexually and medusae form polyps sexually. Both phyla are diploblastic, and both show "
  "extracellular as well as intracellular digestion.",
  ["Comb plates, only sexual reproduction → Ctenophora", "Cnidoblasts, metagenesis → Obelia (Coelenterata)",
   "Both diploblastic; both extra- and intracellular digestion"],
  R_AK("phyla Coelenterata and Ctenophora"),
  why_others_wrong="A is wrong because both phyla are diploblastic; C reverses the two diagnostic structures; D "
                   "ignores that both show extracellular and intracellular digestion.",
  seconds=55)

Z(AK, "Non-chordate phyla", "Advanced", "assertion_reason",
  ar("Like coelenterates, echinoderms are radially symmetrical at every stage of their life.",
     "Echinoderms are triploblastic and coelomate animals."),
  ASSERTION_REASON, "D",
  "Symmetry of larval and adult echinoderms",
  "NCERT: adult echinoderms are radially symmetrical but their larvae are bilaterally symmetrical, so the symmetry "
  "is not radial at every stage. They are triploblastic and coelomate animals, so R is true.",
  ["A → false: larvae are bilaterally symmetrical", "R → true"],
  R_AK("phylum Echinodermata"),
  why_others_wrong="A and B accept the false Assertion; C rejects the true Reason.",
  seconds=40)

# ================================================================ Structural Organisation in Animals (B5 I6 A5)
R_SOA = lambda s: ref("Structural Organisation in Animals", s)

Z(SOA, "Animal tissues", "Basic", "direct",
  "Tendons and ligaments are given in NCERT as examples of which type of connective tissue?",
  ["Areolar (loose) connective tissue", "Dense irregular connective tissue", "Dense regular connective tissue",
   "Specialised connective tissue"], "C",
  "Dense regular connective tissue",
  "NCERT: in dense regular connective tissue the collagen fibres are present in rows between many parallel bundles of "
  "fibres. Tendons, which attach skeletal muscles to bones, and ligaments, which attach one bone to another, are "
  "examples of this tissue. Dense irregular tissue (fibres oriented differently) is present in the skin.",
  ["Parallel collagen bundles → dense regular", "Examples → tendons and ligaments"],
  R_SOA("animal tissues – connective tissue"),
  why_others_wrong="A is loose tissue beneath the skin; B is the tissue of the skin; D covers cartilage, bone and "
                   "blood.",
  seconds=25)

Z(SOA, "Animal tissues", "Basic", "direct",
  "According to NCERT, the discernible trend shown by the increasing complexity of organs and organ systems across "
  "animal groups is called the:",
  ["Evolutionary trend", "Division of labour", "Level of organisation", "Metamerism"], "A",
  "Organs and organ systems",
  "NCERT: tissues organise to form organs, which in turn associate to form organ systems. Complexity in organ and "
  "organ systems displays a certain discernible trend, and this discernible trend is called the evolutionary trend.",
  ["Increasing complexity of organs/organ systems → evolutionary trend"],
  R_SOA("introduction – organ and organ system"),
  why_others_wrong="B is the sharing of work among cells, tissues and organs; C is a basis of classification; D is "
                   "segmentation of the body.",
  seconds=25)

Z(SOA, "Frog: morphology and anatomy", "Basic", "match_list",
  ml(("part of the frog's digestive system", "role"), ["Tongue", "Stomach", "Intestine", "Liver"],
     ["Secretes bile", "Site of the final digestion of food", "Bilobed; captures the food",
      "Digests food by the action of HCl and gastric juices"]),
  match_options(M("III", "IV", "II", "I"), [M("III", "II", "IV", "I"), M("IV", "III", "II", "I"),
                                            M("III", "IV", "I", "II")], "D"), "D",
  "Digestive system of the frog",
  "NCERT: food is captured by the bilobed tongue; in the stomach it is digested by the action of HCl and gastric "
  "juices; the liver secretes bile, which is stored in the gall bladder; final digestion takes place in the "
  "intestine.",
  ["Tongue → III", "Stomach → IV", "Intestine → II", "Liver → I"],
  R_SOA("frog – anatomy (digestive system)"),
  why_others_wrong="A swaps stomach and intestine; B swaps tongue and stomach; C swaps intestine and liver.",
  seconds=35)

Z(SOA, "Frog: morphology and anatomy", "Basic", "statement_pair",
  sp("In the frog, blood carries nutrients, gases and water to the respective sites during circulation.",
     "In the frog, the ventricle opens into the sinus venosus."),
  STATEMENT_PAIR, "C",
  "Circulation in the frog",
  "NCERT: the blood of the frog carries nutrients, gases and water to the respective sites during circulation. The "
  "ventricle opens into a sac-like conus arteriosus on the ventral side of the heart; the sinus venosus is the "
  "triangular structure that joins the right atrium and receives blood through the vena cava.",
  ["Statement I → true", "Statement II → false: the ventricle opens into the conus arteriosus"],
  R_SOA("frog – anatomy (circulatory system)"),
  why_others_wrong="A and D accept Statement II; B rejects NCERT's statement on what frog blood carries.",
  seconds=30)

Z(SOA, "Animal tissues", "Basic", "assertion_reason",
  ar("In multicellular animals, tissues are organised into organs, which in turn associate to form organ systems.",
     "Such an organisation is essential for more efficient and better coordinated activities of the millions of cells "
     "that make up an organism."),
  ASSERTION_REASON, "A",
  "Why tissues form organs and organ systems",
  "NCERT: the basic tissues organise to form organs, which in turn associate to form organ systems in multicellular "
  "organisms, and such an organisation is essential for more efficient and better coordinated activities of the "
  "millions of cells constituting an organism. R gives NCERT's own reason for A.",
  ["A → true", "R → true; NCERT gives it as the reason for this organisation"],
  R_SOA("introduction – organ and organ system"),
  why_others_wrong="B denies the link NCERT states; C and D reject true statements.",
  seconds=30)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "direct",
  "Which sequence correctly traces blood returning from the body through the heart of the frog?",
  ["Vena cava → sinus venosus → right atrium → ventricle → conus arteriosus",
   "Vena cava → right atrium → sinus venosus → ventricle → conus arteriosus",
   "Vena cava → sinus venosus → left atrium → ventricle → conus arteriosus",
   "Vena cava → conus arteriosus → right atrium → ventricle → sinus venosus"], "A",
  "Chambers of the frog heart",
  "NCERT: the frog heart has two atria and one ventricle. The sinus venosus, a triangular structure, joins the right atrium and receives blood through the vena cava. The ventricle opens into a sac-like conus "
  "arteriosus on the ventral side of the heart, from which arteries carry blood to the body.",
  ["Vena cava → sinus venosus (receives it)", "Sinus venosus → right atrium (joins it)",
   "Atrium → ventricle", "Ventricle → conus arteriosus"],
  R_SOA("frog – anatomy (circulatory system)"),
  why_others_wrong="B puts the sinus venosus after the atrium; C connects it to the left atrium; D reverses the "
                   "positions of the sinus venosus and the conus arteriosus.",
  seconds=40)

Z(SOA, "Animal tissues", "Intermediate", "match_list",
  ml(("tissue", "cellular feature described in NCERT"), ["Cartilage", "Bone", "Areolar tissue", "Cardiac muscle"],
     ["Contains fibroblasts, macrophages and mast cells",
      "Communication junctions (intercalated discs) at the fusion points of cells",
      "Cells enclosed in small cavities within the matrix secreted by them",
      "Osteocytes present in spaces called lacunae within a hard matrix"]),
  match_options(M("III", "IV", "I", "II"), [M("IV", "III", "I", "II"), M("III", "IV", "II", "I"),
                                            M("I", "IV", "III", "II")], "B"), "B",
  "Cells of connective and muscle tissues",
  "NCERT: cartilage cells (chondrocytes) are enclosed in small cavities within the matrix secreted by them; bone "
  "cells (osteocytes) are present in spaces called lacunae; areolar tissue contains fibroblasts, macrophages and mast "
  "cells; cardiac muscle cells have communication junctions (intercalated discs) at some fusion points.",
  ["Cartilage → III", "Bone → IV", "Areolar → I", "Cardiac muscle → II"],
  R_SOA("animal tissues – connective tissue and muscle tissue"),
  why_others_wrong="A swaps cartilage and bone; C swaps areolar tissue and cardiac muscle; D swaps cartilage and "
                   "areolar tissue.",
  seconds=40)

Z(SOA, "Animal tissues", "Intermediate", "statement_pair",
  sp("Tendons and the connective tissue of the skin are both dense connective tissues, but they differ in the "
     "orientation of their collagen fibres.",
     "Adipose tissue and areolar tissue are both specialised connective tissues."),
  STATEMENT_PAIR, "C",
  "Categories of connective tissue",
  "NCERT: in dense connective tissue fibres and fibroblasts are compactly packed, and the orientation of the fibres "
  "is regular (tendons, ligaments – fibres in rows between parallel bundles) or irregular (skin – fibres oriented "
  "differently). Areolar and adipose tissues are loose connective tissues; cartilage, bone and blood are the "
  "specialised connective tissues.",
  ["Statement I → true: dense regular vs dense irregular", "Statement II → false: both are loose connective tissues"],
  R_SOA("animal tissues – connective tissue"),
  why_others_wrong="A and D call adipose and areolar tissue specialised; B rejects the regular/irregular distinction.",
  seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Intermediate", "assertion_reason",
  ar("In the frog, the final digestion of food takes place in the stomach.",
     "In the stomach of the frog, food is digested by the action of HCl and gastric juices."),
  ASSERTION_REASON, "D",
  "Sites of digestion in the frog",
  "NCERT: in the frog's stomach, food is digested by HCl and gastric juices and the partially digested food (chyme) "
  "passes to the duodenum, which receives bile and pancreatic juices. Final digestion takes place in the intestine. "
  "So digestion begins in the stomach but is not completed there.",
  ["A → false: final digestion is in the intestine", "R → true: gastric digestion by HCl and gastric juices"],
  R_SOA("frog – anatomy (digestive system)"),
  why_others_wrong="A and B accept the false Assertion; C rejects the true Reason.",
  seconds=35)

_opts_cb = ["(a) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (c) only"]
Z(SOA, "Animal tissues", "Intermediate", "multi_statement",
  ms("Which of the following statements correctly compare cartilage and bone, according to NCERT?",
     ["Both are specialised connective tissues.",
      "In both, the cells lie in small cavities or spaces within the matrix.",
      "The intercellular material of cartilage is solid and pliable, whereas the ground substance of bone is hard and "
      "non-pliable.",
      "The ground substance of both is rich in calcium salts.",
      "In adults, cartilage is the main tissue that provides the structural frame to the body."]),
  _opts_cb, "D",
  "Cartilage compared with bone",
  "NCERT: cartilage, bones and blood are specialised connective tissues. Chondrocytes are enclosed in small cavities "
  "within the matrix they secrete; osteocytes are present in spaces called lacunae. Cartilage has a solid, pliable "
  "matrix that resists compression; bone has a very hard, non-pliable ground substance rich in calcium salts and "
  "collagen fibres, and bone is the main tissue that provides the structural frame to the body.",
  ["(a) true", "(b) true – cavities (cartilage), lacunae (bone)", "(c) true",
   "(d) false – only bone is rich in calcium salts", "(e) false – bone provides the frame"],
  R_SOA("animal tissues – specialised connective tissue"),
  why_others_wrong="A leaves out the true (b); B includes (d); C includes (d) and (e) and omits (a) and (c).",
  seconds=50)
ms_check("abc", _opts_cb, "D")

Z(SOA, "Animal tissues", "Intermediate", "direct",
  "Suppose the tight junctions between the cells of an epithelium were disrupted while its adhering junctions and "
  "gap junctions remained intact. According to NCERT, which function would be lost?",
  ["Cementing neighbouring cells together", "Stopping substances from leaking across the tissue",
   "Rapid transfer of ions and small molecules between adjoining cells",
   "Production and secretion of collagen fibres"], "B",
  "Roles of the three cell junctions",
  "NCERT: tight junctions help to stop substances from leaking across a tissue; adhering junctions perform cementing "
  "to keep neighbouring cells together; gap junctions connect the cytoplasm of adjoining cells for rapid transfer of "
  "ions, small molecules and sometimes big molecules. Fibres are produced by fibroblasts of connective tissue.",
  ["Tight junction lost → leakage across the tissue no longer prevented",
   "Adhering and gap junctions intact → cementing and communication continue"],
  R_SOA("animal tissues – epithelial tissue (cell junctions)"),
  why_others_wrong="A is the job of the intact adhering junctions; C of the intact gap junctions; D is done by "
                   "fibroblasts, not by an epithelial junction.",
  seconds=40)

_opts_fr = ["(a), (b), (c) and (d) only", "(a), (b) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]
Z(SOA, "Frog: morphology and anatomy", "Advanced", "multi_statement",
  ms("A frog spends part of its life in a pond, part on land, and the winter hibernating in a deep burrow. Which of "
     "the following statements about its respiration are correct?",
     ["In the pond, dissolved oxygen is exchanged through the skin by diffusion.",
      "On land, the buccal cavity, the skin and the lungs all act as respiratory organs.",
      "During hibernation in the burrow, gaseous exchange takes place mainly through the lungs.",
      "On land, air entering through the nostrils passes into the buccal cavity and then to the lungs.",
      "Respiration by the lungs is called cutaneous respiration."]),
  _opts_fr, "B",
  "Respiration of the frog in different conditions",
  "NCERT: in water, the skin acts as the aquatic respiratory organ and dissolved oxygen is exchanged through the skin "
  "by diffusion (cutaneous respiration). On land, the buccal cavity, skin and lungs act as respiratory organs; air "
  "enters through the nostrils into the buccal cavity and then to the lungs (pulmonary respiration). During "
  "aestivation and hibernation, gaseous exchange takes place through the skin.",
  ["(a) true", "(b) true", "(c) false – through the skin during hibernation", "(d) true",
   "(e) false – lung respiration is pulmonary; skin respiration is cutaneous"],
  R_SOA("frog – anatomy (respiratory system)"),
  why_others_wrong="A includes (c); C includes (e) and omits (a); D includes both (c) and (e).",
  seconds=60)
ms_check("abd", _opts_fr, "B")

Z(SOA, "Animal tissues", "Advanced", "match_list",
  ml(("function", "structure that performs it"),
     ["Cementing to keep neighbouring cells together", "Allowing cardiac muscle cells to contract as a unit",
      "Production of blood cells", "Forming a diffusion boundary"],
     ["Squamous epithelium", "Bone marrow", "Adhering junctions", "Intercalated discs"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "A"), "A",
  "Structure–function links across tissues",
  "NCERT: adhering junctions perform cementing to keep neighbouring cells together; communication junctions "
  "(intercalated discs) at fusion points allow cardiac muscle cells to contract as a unit; bone marrow in some bones "
  "is the site of production of blood cells; squamous epithelium (walls of blood vessels, air sacs of lungs) is "
  "involved in forming a diffusion boundary.",
  ["Cementing → adhering junctions (III)", "Contract as a unit → intercalated discs (IV)",
   "Blood cells → bone marrow (II)", "Diffusion boundary → squamous epithelium (I)"],
  R_SOA("animal tissues – epithelial, connective and muscle tissue"),
  why_others_wrong="B swaps the two junction types; C swaps bone marrow and squamous epithelium; D swaps bone marrow "
                   "and intercalated discs.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "direct",
  "Which of the following tissue–location pairs is INCORRECTLY matched according to NCERT?",
  ["Compound epithelium – inner lining of the pancreatic ducts",
   "Dense irregular connective tissue – skin",
   "Cartilage – between adjacent bones of the vertebral column",
   "Cuboidal epithelium – walls of blood vessels"], "D",
  "Locating tissues in the body",
  "NCERT: compound epithelium covers the dry surface of the skin and the moist surface of the buccal cavity and "
  "pharynx, and lines the ducts of salivary glands and the pancreatic ducts. Dense irregular connective tissue is "
  "present in the skin. Cartilage is present between adjacent bones of the vertebral column. The walls of blood "
  "vessels are made of squamous epithelium; cuboidal epithelium is found in the ducts of glands and the tubular parts "
  "of nephrons.",
  ["A, B, C → as stated in NCERT", "Walls of blood vessels → squamous, not cuboidal"],
  R_SOA("animal tissues – epithelial and connective tissue"),
  why_others_wrong="A is correct even though ducts of glands in general have cuboidal epithelium; B and C are NCERT's "
                   "own locations.",
  seconds=45)

Z(SOA, "Animal tissues", "Advanced", "statement_pair",
  sp("Blood is a connective tissue even though its cells do not secrete fibres of collagen or elastin.",
     "Bone marrow in all bones is the site of production of blood cells."),
  STATEMENT_PAIR, "C",
  "Exceptions within connective tissues",
  "NCERT: in all connective tissues except blood, the cells secrete fibres of structural proteins called collagen or "
  "elastin; blood is still classed as a (specialised, fluid) connective tissue. NCERT says the bone marrow in SOME "
  "bones is the site of production of blood cells – not in all bones.",
  ["Statement I → true: blood is the stated exception for fibre secretion",
   "Statement II → false: 'some bones', not all bones"],
  R_SOA("animal tissues – connective tissue"),
  why_others_wrong="A and D miss the qualifier 'some' in Statement II; B rejects the true Statement I.",
  seconds=40)

Z(SOA, "Frog: morphology and anatomy", "Advanced", "assertion_reason",
  ar("In the male frog, sperms pass through the kidneys on their way to the cloaca.",
     "In the female frog, too, the oviducts open into the kidneys."),
  ASSERTION_REASON, "C",
  "Reproductive ducts of the frog",
  "NCERT: in the male frog, 10–12 vasa efferentia arising from the testes enter the kidneys on their side and open "
  "into Bidder's canal, which communicates with the urinogenital duct that opens into the cloaca – so sperms pass "
  "through the kidneys. In the female, the ovaries have no functional connection with the kidneys, and the oviducts "
  "open into the cloaca separately.",
  ["A → true (vasa efferentia → Bidder's canal → urinogenital duct)",
   "R → false: oviducts open into the cloaca separately"],
  R_SOA("frog – anatomy (reproductive system)"),
  why_others_wrong="A and B accept the false Reason; D rejects the true Assertion.",
  seconds=40)

# ================================================================ Biomolecules (B6 I8 A6)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Carbohydrates and lipids", "Basic", "direct",
  "Which of the following is NOT a polysaccharide?",
  ["Chitin", "Inulin", "Glycogen", "Collagen"], "D",
  "Identifying polysaccharides",
  "NCERT: chitin (a complex polysaccharide of the arthropod exoskeleton), inulin (a polymer of fructose) and glycogen "
  "(the animal variant of starch) are polysaccharides. Collagen is a protein – the most abundant protein in the animal "
  "world – and is a polymer of amino acids.",
  ["Chitin, inulin, glycogen → polysaccharides", "Collagen → protein"],
  R_BIO("polysaccharides; proteins"),
  why_others_wrong="A, B and C are all polysaccharides named in NCERT.",
  seconds=20)

Z(BIO, "Nucleic acids", "Basic", "direct",
  "When the nitrogenous base cytosine is attached to a sugar, the compound formed is:",
  ["Cytidylic acid", "Cytidine", "Cytosine monophosphate ester of glycerol", "A substituted purine"], "B",
  "Nucleosides",
  "NCERT: a nitrogenous base attached to a sugar is called a nucleoside; adenosine, guanosine, thymidine, uridine and "
  "cytidine are nucleosides. If a phosphate group is also esterified to the sugar, the compound is a nucleotide – "
  "cytidylic acid. Cytosine is a substituted pyrimidine.",
  ["Base + sugar → nucleoside", "Cytosine + sugar → cytidine"],
  R_BIO("nucleic acids"),
  why_others_wrong="A is the nucleotide (it also needs a phosphate); C is not a nucleic-acid component; D is wrong "
                   "because cytosine is a substituted pyrimidine.",
  seconds=25)

_n_nt, _n_pur = 30, 12
_n_pyr = _n_nt - _n_pur
assert _n_pyr == 18
Z(BIO, "Nucleic acids", "Basic", "numerical",
  f"A polynucleotide chain is made of {_n_nt} nucleotides. Of these, {_n_pur} carry adenine or guanine as their "
  "nitrogenous base. On complete hydrolysis, how many molecules of substituted pyrimidines will the chain yield?",
  ["12", "30", "18", "42"], "C",
  "Purines and pyrimidines in nucleotides",
  "NCERT: each nucleotide has one heterocyclic nitrogenous base. Adenine and guanine are substituted purines; "
  "cytosine, uracil and thymine are substituted pyrimidines. So every nucleotide that does not carry a purine carries "
  "a pyrimidine.",
  [f"Total bases = {_n_nt} (one per nucleotide)", f"Purines (A + G) = {_n_pur}",
   f"Pyrimidines = {_n_nt} − {_n_pur} = {_n_pyr}"],
  R_BIO("nucleic acids"),
  shortcut="Pyrimidines = nucleotides − purines.",
  why_others_wrong="A counts the purines; B counts all the bases; D adds purines to the total instead of subtracting.",
  seconds=40, verified_by=RECOMPUTED)

Z(BIO, "Enzyme classification", "Basic", "statement_pair",
  sp("Lyases catalyse the removal of groups from substrates by hydrolysis.",
     "Ligases catalyse the linking together of two compounds."),
  STATEMENT_PAIR, "D",
  "Lyases and ligases",
  "NCERT: lyases are enzymes that catalyse the removal of groups from substrates by mechanisms OTHER than hydrolysis, "
  "leaving double bonds. Ligases catalyse the linking together of two compounds, e.g., enzymes that catalyse the "
  "joining of C–O, C–S, C–N, P–O etc. bonds.",
  ["Statement I → false: 'other than hydrolysis'", "Statement II → true"],
  R_BIO("enzymes – classification and nomenclature"),
  why_others_wrong="A and C accept Statement I, which describes hydrolases; B rejects NCERT's definition of ligases.",
  seconds=30)

Z(BIO, "Enzymes: properties and action", "Basic", "assertion_reason",
  ar("Trypsin is a protein that acts as an enzyme.",
     "Trypsin is a ribozyme, i.e., a nucleic acid that behaves like an enzyme."),
  ASSERTION_REASON, "C",
  "Proteins and ribozymes as enzymes",
  "NCERT's table of proteins lists trypsin with the function 'enzyme', so trypsin is a protein enzyme. NCERT states "
  "that almost all enzymes are proteins, and that there are some nucleic acids that behave like enzymes – these are "
  "called ribozymes. Trypsin, being a protein, is not a ribozyme.",
  ["A → true (NCERT table: trypsin – enzyme)", "R → false: ribozymes are nucleic acids; trypsin is a protein"],
  R_BIO("proteins; enzymes"),
  why_others_wrong="A and B accept the false Reason; D rejects the true Assertion.",
  seconds=30)

Z(BIO, "Nucleic acids", "Basic", "match_list",
  ml(("compound", "category"), ["Lecithin", "Adenylic acid", "Insulin", "Uridine"],
     ["Phospholipid", "Nucleotide", "Protein hormone", "Nucleoside"]),
  match_options(M("I", "II", "III", "IV"), [M("I", "IV", "III", "II"), M("III", "II", "I", "IV"),
                                            M("II", "I", "III", "IV")], "A"), "A",
  "Classes of biomolecules",
  "NCERT: lecithin is a phospholipid found in the cell membrane; adenylic acid is a nucleotide (base + sugar + "
  "phosphate); insulin is a protein that functions as a hormone; uridine is a nucleoside (base + sugar).",
  ["Lecithin → I", "Adenylic acid → II", "Insulin → III", "Uridine → IV"],
  R_BIO("lipids; nucleic acids; proteins"),
  why_others_wrong="B swaps the nucleotide and the nucleoside; C swaps lecithin and insulin; D swaps lecithin and "
                   "adenylic acid.",
  seconds=30)

Z(BIO, "Proteins and amino acids", "Intermediate", "direct",
  "NCERT names three aromatic amino acids. Which of the following is NOT one of them?",
  ["Lysine", "Tyrosine", "Phenylalanine", "Tryptophan"], "A",
  "Aromatic amino acids",
  "NCERT: tyrosine, phenylalanine and tryptophan are aromatic amino acids. Lysine is a basic amino acid (more amino "
  "groups than carboxyl groups).",
  ["Aromatic → tyrosine, phenylalanine, tryptophan", "Lysine → basic"],
  R_BIO("proteins – amino acids"),
  why_others_wrong="B, C and D are exactly NCERT's three aromatic amino acids.",
  seconds=25)

_cell_mass = 400
_pct = {"carbohydrates": 3, "lipids": 2, "ions": 1}
_mass = _cell_mass * sum(_pct.values()) / 100
assert _mass == 24
Z(BIO, "Carbohydrates and lipids", "Intermediate", "numerical",
  f"A cell has a total mass of {_cell_mass} pg. Using the average percentages of the total cellular mass given in "
  "NCERT (carbohydrates 3%, lipids 2%, ions 1%), what is the combined mass of the carbohydrates, lipids and ions in "
  "this cell?",
  ["12 pg", "24 pg", "60 pg", "6 pg"], "B",
  "Average composition of cells",
  "NCERT's table of the average composition of cells gives water 70–90%, proteins 10–15%, carbohydrates 3%, lipids "
  "2%, nucleic acids 5–7% and ions 1% of the total cellular mass.",
  ["Carbohydrates + lipids + ions = 3 + 2 + 1 = 6%", f"6% of {_cell_mass} pg = {_mass:g} pg"],
  R_BIO("biomacromolecules – average composition of cells (table)"),
  why_others_wrong="A uses only carbohydrates (3%); C takes 15%, the upper value for proteins; D gives the percentage "
                   "instead of the mass.",
  seconds=45, verified_by=RECOMPUTED)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "match_list",
  ml(("polysaccharide", "feature described in NCERT"), ["Starch", "Cellulose", "Glycogen", "Inulin"],
     ["Polymer of fructose", "Store of energy in animals; a variant of starch",
      "Forms helical secondary structures that can hold I₂, giving a blue colour",
      "Forms plant cell walls and does not give a blue colour with iodine"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "B"), "B",
  "Features of common polysaccharides",
  "NCERT: starch forms helical secondary structures and can hold I₂ molecules in the helical portion (blue colour); "
  "cellulose, of plant cell walls, has no complex helices and gives no blue colour; animals have glycogen, a variant "
  "of starch, as their energy store; inulin is a polymer of fructose.",
  ["Starch → III", "Cellulose → IV", "Glycogen → II", "Inulin → I"],
  R_BIO("polysaccharides"),
  why_others_wrong="A swaps starch and cellulose; C swaps glycogen and inulin; D swaps cellulose and glycogen.",
  seconds=40)

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("The activity of an enzyme declines both below and above its optimum pH.",
     "Low temperature permanently destroys the activity of an enzyme by denaturing it."),
  STATEMENT_PAIR, "C",
  "Effect of pH and temperature on enzymes",
  "NCERT: each enzyme shows its highest activity at a particular temperature and pH (optimum), and activity declines "
  "both below and above the optimum value. Low temperature preserves the enzyme in a temporarily inactive state, "
  "whereas high temperature destroys enzymatic activity because proteins are denatured by heat.",
  ["Statement I → true", "Statement II → false: low temperature only inactivates temporarily"],
  R_BIO("enzymes – factors affecting enzyme activity"),
  why_others_wrong="A and D accept Statement II, which describes high, not low, temperature; B rejects the optimum-"
                   "pH behaviour.",
  seconds=35)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Some lipids, such as lecithin, contain phosphorus and a phosphorylated organic compound.",
     "Fatty acids may be saturated (without a double bond) or unsaturated (with one or more C=C double bonds)."),
  ASSERTION_REASON, "B",
  "Phospholipids and fatty acids",
  "NCERT: some lipids have phosphorous and a phosphorylated organic compound in them; these are phospholipids, found "
  "in the cell membrane, e.g., lecithin. Separately, NCERT classifies fatty acids as saturated or unsaturated by the "
  "presence of C=C double bonds. Saturation of fatty acids has nothing to do with whether a lipid contains phosphorus, "
  "so R does not explain A.",
  ["A → true (phospholipid)", "R → true (saturated/unsaturated fatty acids)",
   "R describes the fatty-acid chains, not the phosphate part → no explanation"],
  R_BIO("lipids"),
  why_others_wrong="A links two unrelated features; C and D reject true statements.",
  seconds=35)

_opts_nt = ["(a), (b) and (d) only", "(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"]
Z(BIO, "Nucleic acids", "Intermediate", "multi_statement",
  ms("Which of the following compounds are nucleotides, according to NCERT?",
     ["Adenylic acid", "Thymidylic acid", "Uridine", "Cytidylic acid", "Guanosine"]),
  _opts_nt, "A",
  "Nucleotides versus nucleosides",
  "NCERT: a nitrogenous base attached to a sugar is a nucleoside (adenosine, guanosine, thymidine, uridine, cytidine). "
  "If a phosphate group is also esterified to the 5'-OH of the nucleoside, it is a nucleotide (adenylic acid, "
  "thymidylic acid, guanylic acid, uridylic acid, cytidylic acid).",
  ["'-ylic acid' names → nucleotides: (a), (b), (d)", "'-idine/-osine' names → nucleosides: (c), (e)"],
  R_BIO("nucleic acids"),
  why_others_wrong="B, C and D each include uridine or guanosine, which are nucleosides.",
  seconds=35)
ms_check("abd", _opts_nt, "A")

Z(BIO, "Enzyme classification", "Intermediate", "direct",
  "An enzyme breaks a carbon–halide (C–halide) bond in its substrate by adding water across it. In NCERT's "
  "classification of enzymes, it belongs to the class:",
  ["Lyases", "Hydrolases", "Transferases", "Ligases"], "B",
  "Hydrolases",
  "NCERT: hydrolases catalyse the hydrolysis of ester, ether, peptide, glycosidic, C–C, C–halide or P–N bonds. "
  "Lyases remove groups by mechanisms other than hydrolysis, leaving double bonds.",
  ["Bond broken by adding water → hydrolysis", "C–halide is in NCERT's list for hydrolases"],
  R_BIO("enzymes – classification and nomenclature"),
  why_others_wrong="A works by mechanisms other than hydrolysis; C moves a group between two substrates; D joins two "
                   "compounds.",
  seconds=30)

_c_total = 20
_c_r = _c_total - 1
assert _c_r == 19
Z(BIO, "Carbohydrates and lipids", "Intermediate", "numerical",
  "A fatty acid has a carboxyl group attached to an R group. NCERT states that arachidonic acid has 20 carbon atoms "
  "including the carboxyl carbon. How many carbon atoms are present in its R group?",
  ["20", "19", "18", "21"], "B",
  "Structure of a fatty acid",
  "A fatty acid = R–COOH. The carboxyl group contributes one carbon, so the R group has one carbon fewer than the "
  "total. NCERT's range for the R group (1 to 19 carbons) has arachidonic acid at its upper end.",
  [f"Total carbons = {_c_total} (includes the carboxyl carbon)", f"R group = {_c_total} − 1 = {_c_r}"],
  R_BIO("lipids"),
  why_others_wrong="A counts the carboxyl carbon in the R group; C subtracts two carbons; D adds one instead of "
                   "subtracting.",
  seconds=30, verified_by=RECOMPUTED)

_gly, _fa = 40, 90
_tri = _fa - 2 * _gly
_di = _gly - _tri
assert (_di, _tri) == (30, 10) and 2 * _di + 3 * _tri == _fa and _di + _tri == _gly
Z(BIO, "Carbohydrates and lipids", "Advanced", "numerical",
  f"A fat sample contains only diglycerides and triglycerides. On complete hydrolysis it yields {_gly} molecules of "
  f"glycerol and {_fa} molecules of fatty acids. How many triglyceride molecules did the sample contain?",
  ["10", "30", "20", "45"], "A",
  "Glycerides as esters of glycerol",
  "NCERT: fatty acids are found esterified with glycerol as monoglycerides, diglycerides and triglycerides. Each "
  "glyceride molecule contains one glycerol; a diglyceride carries two fatty acids and a triglyceride three.",
  [f"Let d diglycerides and t triglycerides: d + t = {_gly} (one glycerol each)",
   f"2d + 3t = {_fa} (fatty acids)", f"Subtract 2 × first equation: t = {_fa} − {2 * _gly} = {_tri}",
   f"d = {_gly} − {_tri} = {_di}"],
  R_BIO("lipids"),
  shortcut="If all 40 were diglycerides there would be 80 fatty acids; each of the 10 extra fatty acids marks one "
           "triglyceride.",
  why_others_wrong="B is the number of diglycerides; C splits the glycerol equally; D halves the fatty acids as if "
                   "every glyceride carried two.",
  seconds=75, verified_by=RECOMPUTED)

_opts_pr = ["(a), (b) and (d) only", "(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
Z(BIO, "Proteins and amino acids", "Advanced", "multi_statement",
  ms("A protein consists of a single polypeptide chain of 120 amino acids. Parts of the chain are arranged as "
     "helices, and the whole chain is folded upon itself like a hollow woollen ball. Which of the following "
     "statements about this protein are correct?",
     ["It shows primary, secondary and tertiary structures.",
      "It does not show a quaternary structure.",
      "Its helical portions are right-handed helices.",
      "It has two N-terminal amino acids.",
      "Its amino acids are joined by 120 peptide bonds."]),
  _opts_pr, "B",
  "Levels of protein structure in a single-chain protein",
  "NCERT: the sequence of amino acids is the primary structure; portions of the thread arranged as a helix form the "
  "secondary structure, and in proteins only right-handed helices are observed; folding of the long chain upon "
  "itself like a hollow woollen ball gives the tertiary structure. Quaternary structure needs more than one subunit. "
  "A single linear chain has one N-terminal and one C-terminal amino acid, and n amino acids in a linear chain are "
  "joined by n − 1 peptide bonds.",
  ["(a) true", "(b) true – only one polypeptide, no subunits", "(c) true",
   "(d) false – one chain has one N-terminal end", "(e) false – 120 amino acids need 119 peptide bonds"],
  R_BIO("proteins – structure of proteins"),
  why_others_wrong="A includes (d); C includes (e) and leaves out (a); D includes both (d) and (e).",
  seconds=65)
ms_check("abc", _opts_pr, "B")

Z(BIO, "Enzyme classification", "Advanced", "assertion_reason",
  ar("An enzyme that hydrolyses the ester bonds of a fat is a lyase, because it removes groups from its substrate.",
     "Lyases catalyse the removal of groups from substrates by mechanisms other than hydrolysis, leaving double "
     "bonds."),
  ASSERTION_REASON, "D",
  "Hydrolases versus lyases",
  "NCERT: hydrolases catalyse the hydrolysis of ester, ether, peptide, glycosidic, C–C, C–halide or P–N bonds. "
  "Lyases remove groups by mechanisms other than hydrolysis, leaving double bonds. An ester-hydrolysing enzyme is "
  "therefore a hydrolase – the very definition in R rules out calling it a lyase.",
  ["A → false: ester hydrolysis → hydrolase", "R → true (NCERT definition of lyases)"],
  R_BIO("enzymes – classification and nomenclature"),
  why_others_wrong="A and B accept the false Assertion; C rejects NCERT's definition of lyases.",
  seconds=40)

Z(BIO, "Enzymes: properties and action", "Advanced", "match_list",
  ml(("enzyme property", "NCERT example"),
     ["Thermal stability", "Competitive inhibition", "Metal-ion co-factor", "Prosthetic group"],
     ["Haem in peroxidase and catalase", "Zinc in carboxypeptidase",
      "Enzymes of organisms living in hot vents and sulphur springs", "Malonate acting on succinic dehydrogenase"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("II", "IV", "III", "I")], "A"), "A",
  "NCERT's worked examples of enzyme properties",
  "NCERT: enzymes isolated from organisms that normally live in extremely high temperatures (hot vents, sulphur "
  "springs) are stable and retain catalytic power even at 80–90 °C; malonate closely resembles succinate and "
  "inhibits succinic dehydrogenase competitively; zinc is a co-factor for the proteolytic enzyme carboxypeptidase; "
  "haem is the prosthetic group in peroxidase and catalase.",
  ["Thermal stability → III", "Competitive inhibition → IV", "Metal ion → II", "Prosthetic group → I"],
  R_BIO("enzymes – properties; factors affecting enzyme activity; co-factors"),
  why_others_wrong="B swaps thermal stability and inhibition; C swaps the two kinds of co-factor; D swaps thermal "
                   "stability and the metal ion.",
  seconds=45)

Z(BIO, "Enzymes: properties and action", "Advanced", "statement_pair",
  sp("An enzyme loses its catalytic activity when its co-factor is removed, whether that co-factor is a prosthetic "
     "group or a co-enzyme.",
     "Like prosthetic groups, co-enzymes remain tightly bound to the apoenzyme at all times."),
  STATEMENT_PAIR, "C",
  "Prosthetic groups compared with co-enzymes",
  "NCERT: co-factors (prosthetic groups, co-enzymes and metal ions) are non-protein constituents bound to the enzyme "
  "to make it catalytically active, and catalytic activity is lost when the co-factor is removed. Prosthetic groups "
  "are tightly bound to the apoenzyme, but the association of a co-enzyme with the apoenzyme is only transient, "
  "usually occurring during the course of catalysis.",
  ["Statement I → true for every kind of co-factor", "Statement II → false: co-enzyme binding is transient"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="A and D accept Statement II; B rejects the true Statement I.",
  seconds=40)

Z(BIO, "Proteins and amino acids", "Advanced", "direct",
  "A tripeptide is written with its N-terminal amino acid on the left as glycine–alanine–serine. Which of the "
  "following statements about it is correct?",
  ["The R group of its C-terminal amino acid is a hydroxy methyl group",
   "The R group of its N-terminal amino acid is a methyl group",
   "It contains three peptide bonds",
   "The R group of its C-terminal amino acid is a hydrogen atom"], "A",
  "R groups and the ends of a polypeptide",
  "NCERT: the first amino acid of a polypeptide is the N-terminal amino acid and the last is the C-terminal amino "
  "acid. The R group is a hydrogen in glycine, a methyl group in alanine and a hydroxy methyl group in serine. Three "
  "amino acids in a linear chain are joined by two peptide bonds.",
  ["N-terminal = glycine (R = H)", "C-terminal = serine (R = –CH₂OH)", "3 amino acids → 2 peptide bonds"],
  R_BIO("proteins – amino acids and primary structure"),
  why_others_wrong="B gives alanine's R group to glycine; C counts one bond per amino acid; D gives glycine's R group "
                   "to the C-terminal serine.",
  seconds=50)

# ================================================================ Breathing and Exchange of Gases (B4 I6 A4)
R_BRE = lambda s: ref("Breathing and Exchange of Gases", s)

Z(BRE, "Mechanism of breathing", "Basic", "direct",
  "According to NCERT, inspiration in humans is initiated by the:",
  ["Relaxation of the diaphragm", "Relaxation of the external inter-costal muscles",
   "Contraction of the muscles of the abdomen", "Contraction of the diaphragm"], "D",
  "Initiation of inspiration",
  "NCERT: inspiration is initiated by the contraction of the diaphragm, which increases the volume of the thoracic "
  "chamber in the antero-posterior axis. Contraction of the external inter-costal muscles adds to it in the "
  "dorso-ventral axis. Relaxation of these muscles brings about expiration; abdominal muscles only add strength to "
  "inspiration and expiration.",
  ["Diaphragm contracts → thoracic volume ↑ (antero-posterior) → inspiration begins"],
  R_BRE("mechanism of breathing"),
  why_others_wrong="A and B are the relaxations that bring about expiration; C only increases the strength of "
                   "breathing.",
  seconds=20)

Z(BRE, "Respiratory system", "Basic", "match_list",
  ml(("part of the human respiratory system", "feature"), ["Pharynx", "Larynx", "Trachea", "Alveoli"],
     ["Very thin, irregular-walled and vascularised bag-like structures",
      "Straight tube that divides at the level of the 5th thoracic vertebra",
      "Cartilaginous box that helps in sound production",
      "A portion of it is the common passage for food and air"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Parts of the human respiratory system",
  "NCERT: the nasal chamber opens into the pharynx, a portion of which is the common passage for food and air; the "
  "larynx is a cartilaginous box (sound box) that helps in sound production; the trachea is a straight tube extending "
  "up to the mid-thoracic cavity, which divides at the level of the 5th thoracic vertebra into the primary bronchi; "
  "each terminal bronchiole gives rise to very thin, irregular-walled and vascularised bag-like alveoli.",
  ["Pharynx → IV", "Larynx → III", "Trachea → II", "Alveoli → I"],
  R_BRE("human respiratory system"),
  why_others_wrong="A swaps pharynx and larynx; C swaps trachea and alveoli; D swaps larynx and trachea.",
  seconds=35)

Z(BRE, "Exchange and transport of gases", "Basic", "statement_pair",
  sp("About 3 per cent of O₂ is carried in a dissolved state through the plasma.",
     "About 7 per cent of O₂ is carried by the RBCs."),
  STATEMENT_PAIR, "C",
  "Forms of oxygen transport",
  "NCERT: about 97 per cent of O₂ is transported by RBCs in the blood, and the remaining 3 per cent is carried in a "
  "dissolved state through the plasma. The figure of 7 per cent belongs to CO₂ carried dissolved in plasma.",
  ["Statement I → true (3% dissolved)", "Statement II → false: RBCs carry about 97%"],
  R_BRE("transport of gases"),
  why_others_wrong="A and D accept Statement II, which borrows the CO₂ figure; B rejects the true Statement I.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Basic", "assertion_reason",
  ar("Each haemoglobin molecule can carry a maximum of two molecules of O₂.",
     "Haemoglobin is a red-coloured, iron-containing pigment present in the RBCs."),
  ASSERTION_REASON, "D",
  "Haemoglobin and oxygen",
  "NCERT: haemoglobin is a red-coloured, iron-containing pigment present in the RBCs. O₂ binds with haemoglobin in a "
  "reversible manner to form oxyhaemoglobin, and each haemoglobin molecule can carry a maximum of FOUR molecules of "
  "O₂.",
  ["A → false: maximum four O₂ per haemoglobin", "R → true"],
  R_BRE("transport of oxygen"),
  why_others_wrong="A and B accept the false Assertion; C rejects NCERT's description of haemoglobin.",
  seconds=25)

Z(BRE, "Exchange and transport of gases", "Intermediate", "direct",
  "Using the partial pressures of oxygen given in NCERT, which sequence correctly ranks the pO₂ from highest to "
  "lowest?",
  ["Alveoli > atmospheric air > oxygenated blood > deoxygenated blood = tissues",
   "Atmospheric air > alveoli > oxygenated blood > deoxygenated blood = tissues",
   "Atmospheric air > oxygenated blood > alveoli > tissues > deoxygenated blood",
   "Atmospheric air > alveoli > deoxygenated blood > oxygenated blood = tissues"], "B",
  "Partial pressure of O₂ along the respiratory path",
  "NCERT's table gives pO₂ (mm Hg): atmospheric air 159, alveoli 104, deoxygenated blood 40, oxygenated blood 95, "
  "tissues 40. Oxygen therefore always moves down its gradient: air → alveoli → blood → tissues.",
  ["159 (air) > 104 (alveoli) > 95 (oxygenated blood) > 40 (deoxygenated blood) = 40 (tissues)"],
  R_BRE("exchange of gases (table of partial pressures)"),
  why_others_wrong="A puts the alveoli above atmospheric air; C puts oxygenated blood above the alveoli and separates "
                   "two equal values; D puts deoxygenated blood above oxygenated blood.",
  seconds=45)

_opts_dis = ["(a), (b) and (c) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]
Z(BRE, "Regulation and disorders", "Intermediate", "multi_statement",
  ms("Which of the following statements about respiratory disorders are correct, according to NCERT?",
     ["Asthma is a difficulty in breathing, causing wheezing, due to inflammation of the bronchi and bronchioles.",
      "Emphysema is a chronic disorder in which alveolar walls are damaged, and cigarette smoking is one of its "
      "major causes.",
      "Long exposure to dust in some industries can give rise to inflammation leading to fibrosis.",
      "In emphysema, the respiratory surface increases.",
      "Asthma is caused mainly by damage to the alveolar walls."]),
  _opts_dis, "A",
  "Asthma, emphysema and occupational disorders",
  "NCERT: asthma is a difficulty in breathing causing wheezing due to inflammation of bronchi and bronchioles. "
  "Emphysema is a chronic disorder in which alveolar walls are damaged, due to which the respiratory surface is "
  "decreased; cigarette smoking is one of its major causes. In industries involving grinding or stone-breaking, long "
  "exposure to dust can give rise to inflammation leading to fibrosis.",
  ["(a) true", "(b) true", "(c) true", "(d) false – the respiratory surface decreases",
   "(e) false – that is emphysema; asthma involves bronchi and bronchioles"],
  R_BRE("disorders of the respiratory system"),
  why_others_wrong="B includes (d); C includes (e) and omits (a); D includes both false statements.",
  seconds=45)
ms_check("abc", _opts_dis, "A")

Z(BRE, "Respiratory system", "Intermediate", "assertion_reason",
  ar("In humans, the trachea divides into the right and left primary bronchi at the level of the 5th thoracic "
     "vertebra.",
     "The trachea, the primary, secondary and tertiary bronchi and the initial bronchioles are supported by "
     "incomplete cartilaginous rings."),
  ASSERTION_REASON, "B",
  "Trachea and bronchi",
  "NCERT: the trachea is a straight tube extending up to the mid-thoracic cavity, which divides at the level of the "
  "5th thoracic vertebra into a right and a left primary bronchus. Separately, the trachea, primary, secondary and "
  "tertiary bronchi and initial bronchioles are supported by incomplete cartilaginous rings. The supporting rings "
  "have nothing to do with the level at which the trachea branches, so R does not explain A.",
  ["A → true", "R → true", "Level of branching ≠ supporting rings → R does not explain A"],
  R_BRE("human respiratory system"),
  why_others_wrong="A links two unrelated features; C and D reject true statements.",
  seconds=35)

Z(BRE, "Regulation and disorders", "Intermediate", "statement_pair",
  sp("The respiratory rhythm centre is located in the medulla region of the brain, and the pneumotaxic centre in the "
     "pons region.",
     "Receptors associated with the aortic arch and carotid artery recognise changes in CO₂ and H⁺ concentration and "
     "send signals to the pneumotaxic centre for remedial action."),
  STATEMENT_PAIR, "C",
  "Centres and receptors regulating respiration",
  "NCERT: a specialised centre in the medulla, the respiratory rhythm centre, is primarily responsible for this "
  "regulation; the pneumotaxic centre in the pons can moderate it. Receptors associated with the aortic arch and "
  "carotid artery recognise changes in CO₂ and H⁺ concentration and send the necessary signals to the RHYTHM centre "
  "for remedial actions.",
  ["Statement I → true", "Statement II → false: the signals go to the rhythm centre"],
  R_BRE("regulation of respiration"),
  why_others_wrong="A and D accept the wrong destination in Statement II; B rejects the correct locations of the "
                   "centres.",
  seconds=40)

Z(BRE, "Respiratory system", "Intermediate", "direct",
  "Which of the following is NOT a function of the conducting part of the human respiratory system?",
  ["Transporting atmospheric air to the alveoli", "Clearing the inhaled air of foreign particles",
   "Humidifying the air and bringing it to body temperature",
   "Diffusion of O₂ and CO₂ between blood and atmospheric air"], "D",
  "Conducting part versus exchange part",
  "NCERT: the conducting part (external nostrils up to the terminal bronchioles) transports atmospheric air to the "
  "alveoli, clears it of foreign particles, humidifies it and brings it to body temperature. The exchange or "
  "respiratory part (alveoli and their ducts) is the site of actual diffusion of O₂ and CO₂ between blood and "
  "atmospheric air.",
  ["A, B, C → conducting part", "D → exchange (respiratory) part"],
  R_BRE("human respiratory system"),
  why_others_wrong="A, B and C are exactly the functions NCERT gives for the conducting part.",
  seconds=30)

_opts_ts = ["(a), (b) and (c) only", "(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"]
Z(BRE, "Exchange and transport of gases", "Intermediate", "multi_statement",
  ms("Which of the following events take place as blood flows through the capillaries of a body tissue, according to "
     "NCERT?",
     ["CO₂ diffuses into the blood and, with the help of carbonic anhydrase, forms HCO₃⁻ and H⁺.",
      "More CO₂ binds to haemoglobin, forming carbamino-haemoglobin.",
      "O₂ dissociates from oxyhaemoglobin.",
      "The pO₂ of the tissue is higher than that of the oxygenated blood reaching it.",
      "HCO₃⁻ is converted back into CO₂ and H₂O, and the CO₂ is released."]),
  _opts_ts, "A",
  "Events at the tissue site",
  "NCERT: at the tissue site, where pCO₂ is high due to catabolism, CO₂ diffuses into blood (RBCs and plasma) and "
  "forms HCO₃⁻ and H⁺ with the help of carbonic anhydrase; high pCO₂ and low pO₂ favour more binding of CO₂ to "
  "haemoglobin; low pO₂, high pCO₂, high H⁺ and higher temperature favour dissociation of O₂ from oxyhaemoglobin. "
  "Tissue pO₂ (40 mm Hg) is lower than that of oxygenated blood (95 mm Hg). The reverse reaction releasing CO₂ from "
  "bicarbonate occurs at the alveoli, where pCO₂ is low.",
  ["(a) true", "(b) true", "(c) true", "(d) false – tissue pO₂ is lower", "(e) false – this happens at the alveoli"],
  R_BRE("exchange of gases; transport of gases"),
  why_others_wrong="B and D include (e); C includes (d) and (e) and omits (a) and (c).",
  seconds=50)
ms_check("abc", _opts_ts, "A")

_ic, _erv, _tv = 3600, 1100, 500
_irv = _ic - _tv
_vc = _tv + _irv + _erv
assert (_irv, _vc) == (3100, 4700) and _ic + _erv == _vc
assert _vc + _tv == 5200 and _vc - _tv == 4200
Z(BRE, "Respiratory volumes", "Advanced", "numerical",
  f"Spirometry of a healthy adult gives an inspiratory capacity (IC) of {_ic} mL, a tidal volume (TV) of {_tv} mL "
  f"and an expiratory reserve volume (ERV) of {_erv} mL. What is his vital capacity?",
  ["4700 mL", "5200 mL", "4200 mL", "3600 mL"], "A",
  "Building vital capacity from a capacity and a volume",
  "NCERT: inspiratory capacity (IC) = TV + IRV, the total volume a person can inspire after a normal expiration; "
  "vital capacity (VC) = ERV + TV + IRV, the maximum volume a person can breathe in after a forced expiration. Since "
  "IC already contains TV, VC = IC + ERV; adding TV again counts it twice.",
  [f"IRV = IC − TV = {_ic} − {_tv} = {_irv} mL",
   f"VC = TV + IRV + ERV = {_tv} + {_irv} + {_erv} = {_vc} mL"],
  R_BRE("respiratory volumes and capacities"),
  shortcut="VC = IC + ERV = 3600 + 1100 = 4700 mL.",
  why_others_wrong="B adds TV again although IC already contains it; C subtracts TV from IC + ERV; D gives the "
                   "inspiratory capacity alone, leaving out ERV.",
  seconds=70, verified_by=RECOMPUTED)

Z(BRE, "Exchange and transport of gases", "Advanced", "assertion_reason",
  ar("Carbonic anhydrase takes part in the transport of CO₂ both at the tissues and at the alveoli.",
     "Most of the CO₂ in blood is carried in a dissolved state through the plasma."),
  ASSERTION_REASON, "C",
  "Role of carbonic anhydrase",
  "NCERT: at the tissues, where pCO₂ is high, carbonic anhydrase helps convert CO₂ and H₂O into HCO₃⁻ and H⁺; at the "
  "alveoli, where pCO₂ is low, the reaction proceeds in the opposite direction, forming CO₂ and H₂O. About 70 per "
  "cent of CO₂ is carried as bicarbonate, 20–25 per cent as carbamino-haemoglobin and only about 7 per cent "
  "dissolved in plasma.",
  ["A → true (forward at tissues, reverse at alveoli)", "R → false: only about 7% is dissolved; most is bicarbonate"],
  R_BRE("transport of carbon dioxide"),
  why_others_wrong="A and B accept the false Reason; D rejects the two-way role NCERT describes.",
  seconds=40)

Z(BRE, "Exchange and transport of gases", "Advanced", "statement_pair",
  sp("Under normal physiological conditions, every 100 mL of oxygenated blood delivers about 5 mL of O₂ to the "
     "tissues, and every 100 mL of deoxygenated blood delivers about 4 mL of CO₂ to the alveoli.",
     "O₂ diffuses more readily than CO₂ across the diffusion membrane because O₂ is 20–25 times more soluble."),
  STATEMENT_PAIR, "C",
  "Gas delivery and solubility",
  "NCERT gives both delivery figures in Statement I. NCERT also states that the solubility of CO₂ is 20–25 times "
  "higher than that of O₂, so the amount of CO₂ that can diffuse through the diffusion membrane per unit difference "
  "in partial pressure is much higher than that of O₂. Statement II reverses this.",
  ["Statement I → true (5 mL O₂ and 4 mL CO₂ per 100 mL)", "Statement II → false: CO₂ is the more soluble gas"],
  R_BRE("exchange of gases; transport of gases"),
  why_others_wrong="A and D accept the reversed solubility; B rejects NCERT's delivery figures.",
  seconds=45)

Z(BRE, "Exchange and transport of gases", "Advanced", "direct",
  "An O₂ molecule diffuses from the alveolar air into the blood across the diffusion membrane. In which order does "
  "it cross the three layers of this membrane described in NCERT?",
  ["Endothelium of the alveolar capillary → basement substance → squamous epithelium of the alveolus",
   "Squamous epithelium of the alveolus → basement substance → endothelium of the alveolar capillary",
   "Basement substance → squamous epithelium of the alveolus → endothelium of the alveolar capillary",
   "Squamous epithelium of the alveolus → endothelium of the alveolar capillary → basement substance"], "B",
  "Layers of the diffusion membrane",
  "NCERT: the diffusion membrane is made up of three major layers – the thin squamous epithelium of the alveoli, the "
  "endothelium of the alveolar capillaries and the basement substance in between them. Moving from the alveolar air "
  "to the blood, O₂ meets the alveolar epithelium first, then the basement substance, then the capillary endothelium.",
  ["Alveolar side → squamous epithelium", "Middle → basement substance", "Blood side → capillary endothelium"],
  R_BRE("exchange of gases (diffusion membrane)"),
  why_others_wrong="A is the route of CO₂ leaving the blood, not O₂ entering it; C and D misplace the basement "
                   "substance, which lies between the two cell layers.",
  seconds=45)

# ================================================================ Body Fluids and Circulation (B5 I7 A5)
R_BFC = lambda s: ref("Body Fluids and Circulation", s)

Z(BFC, "Blood and blood groups", "Basic", "direct",
  "According to NCERT, why should the Rh group also be matched before a blood transfusion?",
  ["Because the Rh antigen is found only in Rhesus monkeys",
   "Because Rh-ve blood lacks haemoglobin",
   "Because the Rh antigen is present on the RBCs of only about 20 per cent of humans",
   "Because an Rh-ve person exposed to Rh+ve blood forms specific antibodies against the Rh antigen"], "D",
  "Rh grouping and transfusion",
  "NCERT: the Rh antigen, similar to one present in Rhesus monkeys, is observed on the RBCs of nearly 80 per cent of "
  "humans (Rh+ve). An Rh-ve person, if exposed to Rh+ve blood, will form specific antibodies against the Rh antigens. "
  "Therefore, the Rh group should also be matched before transfusions.",
  ["Rh-ve + Rh+ve blood → anti-Rh antibodies formed", "Hence Rh must be matched as well as ABO"],
  R_BFC("blood groups – Rh grouping"),
  why_others_wrong="A is wrong because about 80 per cent of humans carry the antigen; B is irrelevant – Rh-ve RBCs "
                   "have haemoglobin; C reverses the figure (about 80 per cent are Rh+ve).",
  seconds=25)

Z(BFC, "Blood and blood groups", "Basic", "assertion_reason",
  ar("Erythrocytes are called red blood cells.",
     "Erythrocytes contain a red-coloured, iron-containing complex protein called haemoglobin."),
  ASSERTION_REASON, "A",
  "Colour and name of erythrocytes",
  "NCERT: RBCs have a red coloured, iron containing complex protein called haemoglobin, hence the colour and name of "
  "these cells. R is the reason NCERT itself gives for A.",
  ["A → true", "R → true; haemoglobin gives the cells their colour and their name"],
  R_BFC("blood – formed elements"),
  why_others_wrong="B denies the 'hence' that NCERT states; C and D reject true statements.",
  seconds=25)

Z(BFC, "Cardiac cycle and ECG", "Basic", "match_list",
  ml(("term", "meaning"), ["Stroke volume", "Cardiac output", "Cardiac cycle", "Joint diastole"],
     ["Volume of blood pumped out by each ventricle per minute",
      "Volume of blood pumped out by each ventricle in each cardiac cycle",
      "Sequential events in the heart that are cyclically repeated, consisting of systole and diastole of the atria "
      "and ventricles",
      "State in which all four chambers of the heart are relaxed"]),
  match_options(M("II", "I", "III", "IV"), [M("I", "II", "III", "IV"), M("II", "I", "IV", "III"),
                                            M("III", "I", "II", "IV")], "C"), "C",
  "Terms of the cardiac cycle",
  "NCERT: each ventricle pumps out about 70 mL of blood in each cardiac cycle – the stroke volume; stroke volume × "
  "heart rate gives the cardiac output, the volume pumped out by each ventricle per minute; the cardiac cycle is the "
  "sequential event in the heart, cyclically repeated, consisting of systole and diastole of both the atria and the "
  "ventricles; when all four chambers are relaxed, the heart is in joint diastole.",
  ["Stroke volume → II", "Cardiac output → I", "Cardiac cycle → III", "Joint diastole → IV"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A swaps stroke volume and cardiac output; B swaps cardiac cycle and joint diastole; D swaps "
                   "stroke volume and cardiac cycle.",
  seconds=35)

Z(BFC, "Blood and blood groups", "Basic", "statement_pair",
  sp("Blood is a special connective tissue consisting of a fluid matrix, plasma, and formed elements.",
     "Basophils are the most abundant of the leucocytes."),
  STATEMENT_PAIR, "C",
  "Blood and its leucocytes",
  "NCERT: blood is a special connective tissue consisting of a fluid matrix, plasma, and formed elements. Neutrophils "
  "are the most abundant leucocytes (60–65 per cent of the total WBCs), while basophils are the least (0.5–1 per "
  "cent).",
  ["Statement I → true", "Statement II → false: basophils are the least abundant; neutrophils the most"],
  R_BFC("blood"),
  why_others_wrong="A and D accept Statement II; B rejects NCERT's definition of blood.",
  seconds=25)

Z(BFC, "Cardiac cycle and ECG", "Basic", "direct",
  "According to NCERT, the cardiac output of a healthy individual averages about:",
  ["70 mL", "5000 mL (5 litres) per minute", "1,20,000 mL per minute", "500 mL per minute"], "B",
  "Average cardiac output",
  "NCERT: the cardiac output, the volume of blood pumped out by each ventricle per minute, averages 5000 mL or 5 "
  "litres in a healthy individual. About 70 mL is the stroke volume – the volume pumped out by each ventricle in one "
  "cardiac cycle.",
  ["Cardiac output = stroke volume × heart rate ≈ 5000 mL per minute"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A is the stroke volume, not the output per minute; C and D are far from NCERT's average.",
  seconds=20)

Z(BFC, "Blood and blood groups", "Intermediate", "assertion_reason",
  ar("Glucose, amino acids and lipids are present in the plasma.",
     "These substances are always in transit in the body."),
  ASSERTION_REASON, "A",
  "Organic solutes of plasma",
  "NCERT: glucose, amino acids, lipids, etc., are also present in the plasma as they are always in transit in the "
  "body. R is the reason NCERT gives for their presence in the plasma.",
  ["A → true", "R → true; NCERT links the two with 'as'"],
  R_BFC("blood – plasma"),
  why_others_wrong="B denies the link NCERT states; C and D reject true statements.",
  seconds=30)

Z(BFC, "Human heart", "Intermediate", "direct",
  "Suppose the bicuspid (mitral) valve of a person failed to close properly during ventricular systole. In which "
  "direction would blood leak?",
  ["From the aorta into the left ventricle", "From the right ventricle into the right atrium",
   "From the left atrium into the pulmonary veins", "From the left ventricle into the left atrium"], "D",
  "Function of the bicuspid valve",
  "NCERT: the opening between the left atrium and the left ventricle is guarded by the bicuspid (mitral) valve. During "
  "ventricular systole the rising ventricular pressure normally closes the tricuspid and bicuspid valves because of "
  "the attempted backflow of blood into the atria. If the bicuspid valve did not close, blood would flow back from "
  "the left ventricle into the left atrium.",
  ["Bicuspid valve → between left atrium and left ventricle",
   "Ventricular systole → attempted backflow into the atrium", "Faulty valve → leak into the left atrium"],
  R_BFC("human circulatory system – heart; cardiac cycle"),
  why_others_wrong="A is the leak through a faulty aortic semilunar valve; B is through a faulty tricuspid valve; C is "
                   "not guarded by the bicuspid valve.",
  seconds=40)

Z(BFC, "Blood and blood groups", "Intermediate", "match_list",
  ml(("formed element", "feature described in NCERT"), ["Erythrocytes", "Platelets", "Neutrophils", "Lymphocytes"],
     ["Occur as two major types, B and T", "Most abundant leucocytes; phagocytic",
      "Cell fragments produced from megakaryocytes", "Average life span of 120 days; destroyed in the spleen"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "B"), "B",
  "Formed elements of blood",
  "NCERT: RBCs have an average life span of 120 days, after which they are destroyed in the spleen; platelets are "
  "cell fragments produced from megakaryocytes; neutrophils are the most abundant WBCs (60–65 per cent) and are "
  "phagocytic; lymphocytes are of two major types, B and T, responsible for immune responses.",
  ["Erythrocytes → IV", "Platelets → III", "Neutrophils → II", "Lymphocytes → I"],
  R_BFC("blood – formed elements"),
  why_others_wrong="A swaps erythrocytes and platelets; C swaps the two leucocytes; D swaps platelets and neutrophils.",
  seconds=40)

Z(BFC, "Double circulation and regulation", "Intermediate", "statement_pair",
  sp("A special neural centre in the medulla oblongata can moderate cardiac function through the autonomic neural "
     "system.",
     "Parasympathetic neural signals increase the speed of conduction of the action potential in the heart."),
  STATEMENT_PAIR, "C",
  "Neural regulation of the heart",
  "NCERT: normal activities of the heart are regulated intrinsically, but a special neural centre in the medulla "
  "oblongata can moderate cardiac function through the ANS. Sympathetic signals can increase the rate of heart beat "
  "and the strength of ventricular contraction; parasympathetic signals DECREASE the rate of heart beat and the speed "
  "of conduction of the action potential, and thereby the cardiac output.",
  ["Statement I → true", "Statement II → false: parasympathetic signals slow conduction"],
  R_BFC("regulation of cardiac activity"),
  why_others_wrong="A and D accept Statement II; B rejects the role of the medulla oblongata.",
  seconds=35)

_opts_pl = ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only", "(a), (b), (c) and (e) only"]
Z(BFC, "Blood and blood groups", "Intermediate", "multi_statement",
  ms("Which of the following statements about human plasma are correct, according to NCERT?",
     ["It is a straw-coloured, viscous fluid.",
      "Water forms 90–92 per cent of it.",
      "Proteins form 6–8 per cent of it.",
      "Its albumins are primarily involved in the defence mechanisms of the body.",
      "It contains small amounts of minerals such as Na⁺, Ca⁺⁺, Mg⁺⁺, HCO₃⁻ and Cl⁻."]),
  _opts_pl, "D",
  "Composition of plasma",
  "NCERT: plasma is a straw-coloured, viscous fluid constituting nearly 55 per cent of the blood; 90–92 per cent of "
  "plasma is water and proteins contribute 6–8 per cent. Fibrinogen is needed for clotting, globulins are primarily "
  "involved in defence, and albumins help in osmotic balance. Plasma also contains small amounts of minerals such as "
  "Na⁺, Ca⁺⁺, Mg⁺⁺, HCO₃⁻ and Cl⁻.",
  ["(a) true", "(b) true", "(c) true", "(d) false – globulins serve defence; albumins help osmotic balance",
   "(e) true"],
  R_BFC("blood – plasma"),
  why_others_wrong="A and C include (d); B leaves out the true statement (a) about the appearance of plasma.",
  seconds=45)
ms_check("abce", _opts_pl, "D")

_hr, _co = 75, 5250
_sv = _co // _hr
assert _sv * _hr == _co and _sv == 70
Z(BFC, "Cardiac cycle and ECG", "Intermediate", "numerical",
  f"A person's heart beats {_hr} times per minute and his cardiac output is {_co} mL per minute. What is his stroke "
  "volume?",
  ["70 mL", "35 mL", "5175 mL", "7 mL"], "A",
  "Stroke volume from cardiac output",
  "NCERT: the stroke volume (blood pumped out by each ventricle in each cardiac cycle) multiplied by the heart rate "
  "gives the cardiac output, the volume pumped out by each ventricle per minute. So stroke volume = cardiac output ÷ "
  "heart rate.",
  [f"Stroke volume = {_co} ÷ {_hr}", f"= {_sv} mL"],
  R_BFC("cardiac cycle"),
  why_others_wrong="B halves the answer as if the output were shared by two ventricles – cardiac output is already "
                   "per ventricle; C subtracts instead of dividing; D misplaces the decimal point.",
  seconds=35, verified_by=RECOMPUTED)

_opts_fl = ["(a), (c) and (d) only", "(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"]
Z(BFC, "Coagulation and lymph", "Intermediate", "multi_statement",
  ms("Which of the following statements about the body fluids of humans are correct, according to NCERT?",
     ["Serum is plasma without the clotting factors.",
      "Interstitial (tissue) fluid has the same mineral distribution as plasma.",
      "Lymph is a colourless fluid containing specialised lymphocytes.",
      "The larger proteins and most of the formed elements pass out of the capillaries into the interstitial fluid.",
      "Lymph is red because it carries haemoglobin-containing RBCs."]),
  _opts_fl, "B",
  "Plasma, serum, tissue fluid and lymph",
  "NCERT: plasma without the clotting factors is called serum. As blood passes through the capillaries, some water "
  "and water-soluble substances move out into the spaces between the cells, forming interstitial or tissue fluid, "
  "which has the same mineral distribution as plasma; the larger proteins and most of the formed elements remain in "
  "the blood vessels. Lymph is a colourless fluid containing specialised lymphocytes.",
  ["(a) true", "(b) true", "(c) true", "(d) false – they stay in the blood vessels", "(e) false – lymph is colourless"],
  R_BFC("blood – plasma; lymph (tissue fluid)"),
  why_others_wrong="A and C include (d); D includes (e).",
  seconds=45)
ms_check("abc", _opts_fl, "B")

Z(BFC, "Cardiac cycle and ECG", "Advanced", "direct",
  "Which sequence correctly orders the events of a cardiac cycle that begin with an action potential from the SAN, "
  "as described in NCERT?",
  ["SAN action potential → AVN and AV bundle conduct it → ventricles contract → atria contract → semilunar valves "
   "open",
   "AVN generates the action potential → SAN relays it → atria contract → bundle of His → ventricles contract",
   "SAN action potential → bundle of His spreads it in the atria → atria contract → AVN → ventricles contract",
   "SAN action potential → both atria contract → AVN and AV bundle conduct it → bundle of His spreads it through the "
   "ventricles → ventricles contract and tricuspid and bicuspid valves close → semilunar valves open"], "D",
  "Sequence of the cardiac cycle",
  "NCERT: the SAN generates an action potential which stimulates both atria to contract simultaneously (atrial "
  "systole). The action potential is conducted to the ventricular side by the AVN and the AV bundle, from where the "
  "bundle of His transmits it through the entire ventricular musculature, causing ventricular systole. Rising "
  "ventricular pressure closes the tricuspid and bicuspid valves; as it rises further, the semilunar valves are "
  "forced open.",
  ["SAN → atrial systole", "AVN + AV bundle → ventricular side", "Bundle of His → ventricular musculature",
   "Ventricular systole → AV valves close → semilunar valves open"],
  R_BFC("cardiac cycle"),
  why_others_wrong="A makes the ventricles contract before the atria; B makes the AVN the initiator; C places the "
                   "bundle of His in the atria, before the AVN.",
  seconds=60)

Z(BFC, "Human heart", "Advanced", "assertion_reason",
  ar("The SAN is called the pacemaker of the human heart.",
     "The SAN is present in the right upper corner of the right atrium."),
  ASSERTION_REASON, "B",
  "Why the SAN is the pacemaker",
  "NCERT: the SAN is present in the right upper corner of the right atrium. It is the pacemaker because it can "
  "generate the maximum number of action potentials (70–75 per minute) and is responsible for initiating and "
  "maintaining the rhythmic contractile activity of the heart. Its position in the atrium is a separate fact and is "
  "not the reason it sets the pace.",
  ["A → true", "R → true (location)", "Pacemaker role comes from generating the most action potentials, not from "
   "its location → R does not explain A"],
  R_BFC("human circulatory system – heart (nodal tissue)"),
  why_others_wrong="A treats the location as the cause; C and D reject true statements.",
  seconds=40)

Z(BFC, "Blood and blood groups", "Advanced", "statement_pair",
  sp("Both monocytes and neutrophils are phagocytic, but only neutrophils are granulocytes.",
     "Both basophils and eosinophils are granulocytes, and both secrete histamine, serotonin and heparin."),
  STATEMENT_PAIR, "C",
  "Comparing leucocytes",
  "NCERT: neutrophils, eosinophils and basophils are granulocytes; lymphocytes and monocytes are agranulocytes. "
  "Neutrophils and monocytes are phagocytic cells which destroy foreign organisms. Basophils secrete histamine, "
  "serotonin, heparin, etc., and are involved in inflammatory reactions; eosinophils resist infections and are "
  "associated with allergic reactions – NCERT gives the secretion of histamine, serotonin and heparin only for "
  "basophils.",
  ["Statement I → true", "Statement II → false: only basophils are described as secreting these substances"],
  R_BFC("blood – formed elements (leucocytes)"),
  why_others_wrong="A and D accept Statement II; B rejects the true comparison in Statement I.",
  seconds=45)

_opts_ecg = ["(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (c) and (e) only", "(a), (b), (c) and (e) only"]
Z(BFC, "Cardiac cycle and ECG", "Advanced", "multi_statement",
  ms("Which of the following statements correctly relate the waves of a standard ECG to events of the cardiac cycle?",
     ["The P-wave represents the electrical excitation (depolarisation) of the atria, which leads to the contraction "
      "of both the atria.",
      "The QRS complex represents the depolarisation of the ventricles, which initiates ventricular contraction.",
      "The T-wave represents the return of the ventricles from the excited to the normal state.",
      "The end of the T-wave marks the beginning of systole.",
      "The contraction of the ventricles starts shortly after Q."]),
  _opts_ecg, "D",
  "ECG and the cardiac cycle",
  "NCERT: the P-wave represents the electrical excitation (depolarisation) of the atria, which leads to the "
  "contraction of both atria; the QRS complex represents depolarisation of the ventricles, which initiates "
  "ventricular contraction, and the contraction starts shortly after Q, marking the beginning of systole; the T-wave "
  "represents the return of the ventricles from the excited to the normal state (repolarisation), and the end of the "
  "T-wave marks the END of systole.",
  ["(a) true", "(b) true", "(c) true", "(d) false – the end of T marks the end of systole", "(e) true"],
  R_BFC("electrocardiograph (ECG)"),
  why_others_wrong="A and B include (d); C leaves out the true statement (b).",
  seconds=55)
ms_check("abce", _opts_ecg, "D")

Z(BFC, "Cardiac cycle and ECG", "Advanced", "match_list",
  ml(("event in the cardiac cycle", "effect on the valves"),
     ["Ventricular systole begins and ventricular pressure rises",
      "Ventricular pressure increases further",
      "Ventricles relax and ventricular pressure falls",
      "Ventricular pressure declines further while the veins keep emptying blood into the atria"],
     ["Tricuspid and bicuspid valves are pushed open", "Semilunar valves close",
      "Semilunar valves are forced open", "Tricuspid and bicuspid valves close"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "A"), "A",
  "Pressure changes and valve movements",
  "NCERT: ventricular systole increases the ventricular pressure, causing closure of the tricuspid and bicuspid "
  "valves due to attempted backflow into the atria; as the pressure increases further, the semilunar valves guarding "
  "the pulmonary artery and the aorta are forced open; when the ventricles relax, the pressure falls and the "
  "semilunar valves close; as the ventricular pressure declines further, the tricuspid and bicuspid valves are pushed "
  "open by the pressure in the atria exerted by the blood emptied into them by the veins.",
  ["Start of ventricular systole → IV", "Further rise → III", "Relaxation → II", "Further decline → I"],
  R_BFC("cardiac cycle"),
  why_others_wrong="B reverses the first two events; C reverses the last two; D swaps the second and third events.",
  seconds=55)

# ================================================================ Excretory Products and their Elimination (B5 I6 A5)
R_EXC = lambda s: ref("Excretory Products and their Elimination", s)

Z(EXC, "Nephron structure", "Basic", "direct",
  "The glomerulus of a nephron is a tuft of capillaries formed by the:",
  ["Efferent arteriole", "Peritubular capillaries", "Afferent arteriole", "Vasa recta"], "C",
  "Blood supply of the nephron",
  "NCERT: the glomerulus is a tuft of capillaries formed by the afferent arteriole – a fine branch of the renal "
  "artery. Blood from the glomerulus is carried away by the efferent arteriole, which forms the peritubular "
  "capillaries around the renal tubule; a minute vessel of this network runs parallel to Henle's loop as the vasa "
  "recta.",
  ["Renal artery → afferent arteriole → glomerulus (tuft of capillaries)"],
  R_EXC("human excretory system – nephron"),
  why_others_wrong="A carries blood away from the glomerulus; B and D are formed downstream from the efferent "
                   "arteriole.",
  seconds=20)

Z(EXC, "Urine formation", "Basic", "direct",
  "During urine formation, the tubular cells add substances such as H⁺, K⁺ and ammonia to the filtrate. NCERT "
  "describes this step as important for maintaining the ionic and acid-base balance of body fluids. The step is "
  "called:",
  ["Tubular secretion", "Glomerular filtration", "Micturition", "Ultrafiltration"], "A",
  "Tubular secretion",
  "NCERT: urine formation involves glomerular filtration, reabsorption and secretion. During urine formation the "
  "tubular cells secrete substances like H⁺, K⁺ and ammonia into the filtrate; tubular secretion is an important step "
  "because it helps in the maintenance of ionic and acid-base balance of body fluids.",
  ["Substances moved from tubular cells into the filtrate → secretion",
   "Role → ionic and acid-base balance"],
  R_EXC("urine formation"),
  why_others_wrong="B and D (ultrafiltration is NCERT's name for glomerular filtration) move plasma constituents from "
                   "the glomerular blood into Bowman's capsule; C is the release of urine from the bladder.",
  seconds=25)

Z(EXC, "Nephron structure", "Basic", "statement_pair",
  sp("Henle's loop is a hairpin-shaped part of the renal tubule whose ascending limb continues as the distal "
     "convoluted tubule.",
     "The efferent arteriole carries blood to the glomerulus."),
  STATEMENT_PAIR, "C",
  "Parts of the nephron",
  "NCERT: the tubule continues from the PCT as a hairpin-shaped Henle's loop with a descending and an ascending limb; "
  "the ascending limb continues as another highly coiled tubular region, the DCT. The efferent arteriole carries "
  "blood AWAY from the glomerulus; blood reaches it through the afferent arteriole.",
  ["Statement I → true", "Statement II → false: the efferent arteriole leaves the glomerulus"],
  R_EXC("human excretory system – nephron"),
  why_others_wrong="A and D accept Statement II; B rejects NCERT's description of Henle's loop.",
  seconds=25)

Z(EXC, "Nephron structure", "Basic", "assertion_reason",
  ar("Cortical nephrons form a minority of the nephrons of the human kidney.",
     "In juxtamedullary nephrons, the loop of Henle is very long and runs deep into the medulla."),
  ASSERTION_REASON, "D",
  "Cortical and juxtamedullary nephrons",
  "NCERT: in the MAJORITY of nephrons, the loop of Henle is too short and extends only very little into the medulla; "
  "these are cortical nephrons. In some nephrons the loop of Henle is very long and runs deep into the medulla; "
  "these are juxtamedullary nephrons.",
  ["A → false: cortical nephrons are the majority", "R → true"],
  R_EXC("human excretory system – nephron"),
  why_others_wrong="A and B accept the false Assertion; C rejects the true Reason.",
  seconds=25)

Z(EXC, "Disorders and dialysis", "Basic", "match_list",
  ml(("term", "meaning"), ["Glycosuria", "Ketonuria", "Uremia", "Renal calculi"],
     ["Presence of ketone bodies in urine", "Presence of glucose in urine",
      "Stone or insoluble mass of crystallised salts formed within the kidney",
      "Accumulation of urea in the blood"]),
  match_options(M("II", "I", "IV", "III"), [M("I", "II", "IV", "III"), M("II", "I", "III", "IV"),
                                            M("IV", "I", "II", "III")], "B"), "B",
  "Terms related to urine and kidney disorders",
  "NCERT: presence of glucose (glycosuria) and ketone bodies (ketonuria) in urine are indicative of diabetes "
  "mellitus; malfunctioning of the kidneys can lead to accumulation of urea in the blood (uremia); renal calculi are "
  "stones or insoluble masses of crystallised salts (oxalates, etc.) formed within the kidney.",
  ["Glycosuria → II", "Ketonuria → I", "Uremia → IV", "Renal calculi → III"],
  R_EXC("disorders of the excretory system"),
  why_others_wrong="A swaps glycosuria and ketonuria; C swaps uremia and renal calculi; D swaps glycosuria and "
                   "uremia.",
  seconds=30)

Z(EXC, "Urine formation", "Intermediate", "direct",
  "Which pair of substances does NCERT describe as being reabsorbed from the filtrate passively?",
  ["Glucose and amino acids", "Na⁺ and glucose", "H⁺ and K⁺",
   "Nitrogenous wastes, and water in the initial segments of the nephron"], "D",
  "Active and passive reabsorption",
  "NCERT: substances like glucose, amino acids, Na⁺, etc., in the filtrate are reabsorbed actively, whereas the "
  "nitrogenous wastes are absorbed by passive transport; reabsorption of water also occurs passively in the initial "
  "segments of the nephron. H⁺, K⁺ and ammonia are secreted into the filtrate by the tubular cells.",
  ["Active → glucose, amino acids, Na⁺", "Passive → nitrogenous wastes; water (initial segments)",
   "Secreted → H⁺, K⁺, ammonia"],
  R_EXC("urine formation"),
  why_others_wrong="A and B are reabsorbed actively; C are secreted into the filtrate, not reabsorbed.",
  seconds=35)

_opts_hd = ["(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only", "(a), (b) and (c) only"]
Z(EXC, "Disorders and dialysis", "Intermediate", "multi_statement",
  ms("Which of the following statements about haemodialysis are correct, according to NCERT?",
     ["Blood drained from a convenient artery is pumped into the dialysing unit after adding an anticoagulant like "
      "heparin.",
      "The unit contains a coiled cellophane tube surrounded by a dialysing fluid having the same composition as "
      "plasma except the nitrogenous wastes.",
      "The cleared blood is pumped back into the body through a vein after adding anti-heparin to it.",
      "Nitrogenous wastes cross the cellophane membrane by active transport.",
      "The dialysing fluid contains more nitrogenous wastes than the patient's plasma."]),
  _opts_hd, "D",
  "Steps of haemodialysis",
  "NCERT: blood drained from a convenient artery is pumped into a dialysing unit after adding an anticoagulant like "
  "heparin. The unit contains a coiled cellophane tube surrounded by dialysing fluid having the same composition as "
  "plasma except the nitrogenous wastes. The porous cellophane membrane allows the passage of molecules based on the "
  "concentration gradient; since the dialysing fluid lacks nitrogenous wastes, they move freely out of the blood. "
  "The cleared blood is pumped back through a vein after adding anti-heparin.",
  ["(a) true", "(b) true", "(c) true", "(d) false – movement is along the concentration gradient",
   "(e) false – the fluid lacks nitrogenous wastes"],
  R_EXC("disorders of the excretory system – haemodialysis"),
  why_others_wrong="A, B and C each include (d) or (e).",
  seconds=45)
ms_check("abc", _opts_hd, "D")

Z(EXC, "Nephron structure", "Intermediate", "assertion_reason",
  ar("The kidneys are situated between the levels of the last thoracic and the third lumbar vertebra, close to the "
     "dorsal inner wall of the abdominal cavity.",
     "Each kidney of an adult human has an average weight of 120–170 g."),
  ASSERTION_REASON, "B",
  "Position and size of the kidneys",
  "NCERT gives both facts: the kidneys lie between the levels of the last thoracic and the third lumbar vertebra "
  "close to the dorsal inner wall of the abdominal cavity, and each adult kidney measures 10–12 cm × 5–7 cm × 2–3 cm "
  "with an average weight of 120–170 g. The weight of the kidney does not determine where it lies, so R does not "
  "explain A.",
  ["A → true (position)", "R → true (weight)", "Weight and position are independent facts → no explanation"],
  R_EXC("human excretory system"),
  why_others_wrong="A links two unrelated facts; C and D reject true statements.",
  seconds=30)

Z(EXC, "Urine formation", "Intermediate", "statement_pair",
  sp("Large amounts of water can be reabsorbed from the collecting duct to produce a concentrated urine.",
     "The collecting duct allows passage of small amounts of urea into the medullary interstitium to keep up the "
     "osmolarity."),
  STATEMENT_PAIR, "A",
  "Roles of the collecting duct",
  "NCERT: the long collecting duct extends from the cortex of the kidney to the inner parts of the medulla. Large "
  "amounts of water could be reabsorbed from this region to produce a concentrated urine. This segment allows passage "
  "of small amounts of urea into the medullary interstitium to keep up the osmolarity, and it also helps maintain the "
  "pH and ionic balance of blood by the selective secretion of H⁺ and K⁺.",
  ["Statement I → true", "Statement II → true"],
  R_EXC("urine formation – function of the tubules"),
  why_others_wrong="B, C and D each reject a role NCERT assigns to the collecting duct.",
  seconds=30)

Z(EXC, "Modes of excretion", "Intermediate", "match_list",
  ml(("substance", "description in NCERT"), ["Ammonia", "Urea", "Uric acid", "Bilirubin"],
     ["Least toxic; removed as pellet or paste with a minimum loss of water",
      "Most toxic; its elimination requires large amounts of water",
      "Formed from ammonia in the liver of ureotelic animals",
      "Passed out with the bile secreted by the liver"]),
  match_options(M("II", "III", "I", "IV"), [M("I", "III", "II", "IV"), M("II", "IV", "I", "III"),
                                            M("III", "II", "I", "IV")], "B"), "B",
  "Forms of nitrogenous and other wastes",
  "NCERT: ammonia is the most toxic form and requires large amounts of water for its elimination; in ureotelic "
  "animals ammonia is converted into urea in the liver; uric acid, being the least toxic, can be removed with a "
  "minimum loss of water as pellet or paste; the liver secretes bile containing bilirubin, biliverdin, cholesterol, "
  "degraded steroid hormones, vitamins and drugs, which pass out with digestive wastes.",
  ["Ammonia → II", "Urea → III", "Uric acid → I", "Bilirubin → IV"],
  R_EXC("introduction; role of other organs in excretion"),
  why_others_wrong="A swaps ammonia and uric acid; C swaps urea and bilirubin; D swaps ammonia and urea.",
  seconds=40)

Z(EXC, "Urine formation", "Intermediate", "direct",
  "Which of the following correctly compares the PCT and the DCT of a human nephron?",
  ["Both lie in the cortex; the PCT reabsorbs nearly all the essential nutrients and 70–80 per cent of the "
   "electrolytes and water, whereas the DCT carries out conditional reabsorption of Na⁺ and water",
   "Both lie in the medulla; the PCT carries out conditional reabsorption of Na⁺ and water, whereas the DCT "
   "reabsorbs nearly all the essential nutrients",
   "Both lie in the cortex; the PCT carries out conditional reabsorption of Na⁺ and water, whereas the DCT reabsorbs "
   "nearly all the essential nutrients",
   "The PCT lies in the cortex and the DCT in the medulla; only the PCT secretes H⁺ and K⁺"], "A",
  "PCT compared with DCT",
  "NCERT: the Malpighian corpuscle, PCT and DCT are situated in the cortical region of the kidney. Nearly all the "
  "essential nutrients and 70–80 per cent of electrolytes and water are reabsorbed by the PCT. Conditional "
  "reabsorption of Na⁺ and water takes place in the DCT. Both secrete H⁺ and K⁺ (the PCT also ammonia, the DCT also "
  "NH₃) to maintain pH and ionic balance.",
  ["Location → both cortical", "PCT → bulk reabsorption", "DCT → conditional reabsorption of Na⁺ and water"],
  R_EXC("human excretory system – nephron; urine formation – function of the tubules"),
  why_others_wrong="B puts both in the medulla and swaps their roles; C swaps their roles; D puts the DCT in the "
                   "medulla and denies its secretion of H⁺ and K⁺.",
  seconds=45)

_opts_sec = ["(a) and (b) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (b) and (c) only"]
Z(EXC, "Urine formation", "Advanced", "multi_statement",
  ms("NCERT describes certain parts of the nephron as helping to maintain the pH and ionic balance of the body fluids "
     "or blood by the selective secretion of H⁺ and K⁺. Which of the following are such parts?",
     ["Proximal convoluted tubule",
      "Distal convoluted tubule",
      "Collecting duct",
      "Descending limb of Henle's loop",
      "Bowman's capsule"]),
  _opts_sec, "D",
  "Tubular secretion along the nephron",
  "NCERT: the PCT helps maintain the pH and ionic balance of the body fluids by selective secretion of H⁺, ammonia and "
  "K⁺ into the filtrate and absorption of HCO₃⁻; the DCT is capable of reabsorbing HCO₃⁻ and selectively secreting "
  "H⁺, K⁺ and NH₃ to maintain pH and sodium-potassium balance in blood; the collecting duct plays a role in "
  "maintaining pH and ionic balance of blood by selective secretion of H⁺ and K⁺. The descending limb is permeable to "
  "water but almost impermeable to electrolytes, and Bowman's capsule receives the filtrate.",
  ["(a) PCT – yes", "(b) DCT – yes", "(c) collecting duct – yes", "(d) descending limb – no", "(e) Bowman's capsule – no"],
  R_EXC("urine formation – function of the tubules"),
  why_others_wrong="A leaves out the collecting duct; B adds Bowman's capsule; C adds the descending limb and leaves "
                   "out the PCT.",
  seconds=50)
ms_check("abc", _opts_sec, "D")

Z(EXC, "Urine formation", "Advanced", "assertion_reason",
  ar("Henle's loop plays a significant role in the maintenance of a high osmolarity of the medullary interstitial "
     "fluid.",
     "Reabsorption in Henle's loop is the maximum of all the segments of the renal tubule."),
  ASSERTION_REASON, "C",
  "Role of Henle's loop",
  "NCERT: reabsorption in Henle's loop is MINIMUM, but this segment plays a significant role in the maintenance of "
  "high osmolarity of the medullary interstitial fluid. The maximum reabsorption occurs in the PCT (nearly all "
  "essential nutrients and 70–80 per cent of electrolytes and water).",
  ["A → true", "R → false: reabsorption in Henle's loop is minimum; the PCT reabsorbs the most"],
  R_EXC("urine formation – function of the tubules"),
  why_others_wrong="A and B accept the false Reason; D rejects the true Assertion.",
  seconds=40)

Z(EXC, "Regulation of kidney function", "Advanced", "statement_pair",
  sp("Both ADH and angiotensin II, through their constrictory effects on blood vessels, can increase the glomerular "
     "filtration rate.",
     "Both ADH and aldosterone are released into the blood from the neurohypophysis."),
  STATEMENT_PAIR, "C",
  "Comparing the hormones that regulate the kidney",
  "NCERT: ADH can affect kidney function by its constrictory effects on blood vessels, which increases blood pressure "
  "and can increase the glomerular blood flow and thereby the GFR. Angiotensin II, a powerful vasoconstrictor, "
  "increases the glomerular blood pressure and thereby the GFR. ADH is released from the neurohypophysis, but "
  "aldosterone is released by the adrenal cortex (activated by angiotensin II).",
  ["Statement I → true for both hormones", "Statement II → false: aldosterone comes from the adrenal cortex"],
  R_EXC("regulation of kidney function"),
  why_others_wrong="A and D accept the wrong source of aldosterone; B rejects the vasoconstrictor effect of both "
                   "hormones.",
  seconds=45)

Z(EXC, "Regulation of kidney function", "Advanced", "match_list",
  ml(("condition", "expected consequence according to NCERT"),
     ["Deficiency of ADH", "Diabetes mellitus", "Destruction of the JG cells", "Excess of atrial natriuretic factor"],
     ["Vasodilation and a fall in blood pressure", "No renin is released when the glomerular blood flow falls",
      "Glucose and ketone bodies appear in the urine",
      "Water reabsorption from the latter parts of the tubule falls, so diuresis is not prevented"]),
  match_options(M("IV", "III", "II", "I"), [M("IV", "II", "III", "I"), M("III", "IV", "II", "I"),
                                            M("IV", "III", "I", "II")], "B"), "B",
  "Linking conditions to their effects",
  "NCERT: ADH facilitates water reabsorption from the latter parts of the tubule, thereby preventing diuresis – its "
  "deficiency removes this; glycosuria and ketonuria are indicative of diabetes mellitus; a fall in glomerular blood "
  "flow activates the JG cells to release renin – without JG cells this cannot happen; ANF causes vasodilation and "
  "thereby decreases blood pressure.",
  ["ADH deficiency → IV", "Diabetes mellitus → III", "JG cells destroyed → II", "Excess ANF → I"],
  R_EXC("regulation of kidney function; disorders of the excretory system"),
  why_others_wrong="A swaps diabetes mellitus and the JG cells; C swaps ADH deficiency and diabetes mellitus; D swaps "
                   "the JG cells and ANF.",
  seconds=50)

Z(EXC, "Urine formation", "Advanced", "direct",
  "Suppose the collecting duct of a person's nephrons no longer allowed urea to pass into the medullary interstitium, "
  "while every other part of the kidney worked normally. Using NCERT's account, which effect is expected?",
  ["It would be harder to keep up the osmolarity of the medullary interstitium, so the ability to form concentrated "
   "urine would fall",
   "Glucose would begin to appear in the urine",
   "The glomerular filtration rate would rise sharply",
   "The ascending limb of Henle's loop would become permeable to water"], "A",
  "Urea and the medullary osmolarity gradient",
  "NCERT: the collecting duct allows passage of small amounts of urea into the medullary interstitium to keep up the "
  "osmolarity. Together with the counter-current mechanism, this maintains the concentration gradient in the "
  "medullary interstitium, and the gradient helps the easy passage of water from the collecting tubule, concentrating "
  "the filtrate. Without the urea contribution, the gradient – and hence urine concentration – would suffer.",
  ["Urea into interstitium → keeps up medullary osmolarity",
   "Gradient → water leaves the collecting duct → concentrated urine", "No urea entry → weaker concentrating ability"],
  R_EXC("urine formation – function of the tubules; mechanism of concentration of the filtrate"),
  why_others_wrong="B depends on glucose reabsorption in the PCT; C depends on glomerular blood pressure; D is "
                   "unrelated – the ascending limb stays impermeable to water.",
  seconds=55)

# ================================================================ Locomotion and Movement (B5 I6 A5)
R_LOC = lambda s: ref("Locomotion and Movement", s)

Z(LOC, "Skeletal system", "Basic", "direct",
  "According to NCERT, the bones of the pectoral and pelvic girdles help in the:",
  ["Protection of the brain and the spinal cord", "Production of blood cells", "Formation of the rib cage",
   "Articulation of the upper and the lower limbs, respectively, with the axial skeleton"], "D",
  "Role of the girdles",
  "NCERT: the appendicular skeleton is composed of the bones of the limbs along with their girdles; the pectoral and "
  "pelvic girdle bones help in the articulation of the upper and the lower limbs, respectively, with the axial "
  "skeleton. The rib cage is formed by the thoracic vertebrae, ribs and sternum.",
  ["Pectoral girdle → links upper limb to axial skeleton", "Pelvic girdle → links lower limb to axial skeleton"],
  R_LOC("skeletal system – appendicular skeleton"),
  why_others_wrong="A is a role of the skull and vertebral column; B is not the role NCERT gives the girdles; C is "
                   "formed by the thoracic vertebrae, ribs and sternum.",
  seconds=25)

Z(LOC, "Types of movement", "Basic", "direct",
  "Voluntary movements that result in a change of place or location are called:",
  ["Ciliary movements", "Locomotion", "Amoeboid movements", "Muscle tone"], "B",
  "Movement and locomotion",
  "NCERT: voluntary movements which result in a change of place or location are called locomotion; walking, running, "
  "climbing, flying and swimming are some forms of locomotory movements. Not every movement is locomotion.",
  ["Change of place + voluntary → locomotion"],
  R_LOC("introduction"),
  why_others_wrong="A and C are types of movement shown by cells and need not change the organism's location; D is "
                   "not a term NCERT uses for movement from place to place.",
  seconds=20)

Z(LOC, "Skeletal system", "Basic", "match_list",
  ml(("part of the human skeleton", "number"), ["Cranial bones", "Facial bones", "Vertebrae", "Pairs of ribs"],
     ["12", "26", "14", "8"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "A"), "A",
  "Counting the axial skeleton",
  "NCERT: the skull is composed of cranial and facial bones totalling 22 – the cranium has 8 bones and the facial "
  "region is made up of 14 skeletal elements; the vertebral column is formed by 26 serially arranged vertebrae; there "
  "are 12 pairs of ribs.",
  ["Cranial → 8 (IV)", "Facial → 14 (III)", "Vertebrae → 26 (II)", "Pairs of ribs → 12 (I)"],
  R_LOC("skeletal system – axial skeleton"),
  why_others_wrong="B swaps the cranial and facial counts; C swaps vertebrae and ribs; D swaps facial bones and "
                   "vertebrae.",
  seconds=30)

Z(LOC, "Muscular and skeletal disorders", "Basic", "statement_pair",
  sp("Arthritis is inflammation of joints.",
     "Myasthenia gravis is caused by the accumulation of uric acid crystals in the joints."),
  STATEMENT_PAIR, "C",
  "Disorders of the muscular and skeletal system",
  "NCERT: arthritis is inflammation of joints. Myasthenia gravis is an auto-immune disorder affecting the "
  "neuromuscular junction, leading to fatigue, weakening and paralysis of skeletal muscle. Inflammation of joints due "
  "to accumulation of uric acid crystals is gout.",
  ["Statement I → true", "Statement II → false: that describes gout"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="A and D accept Statement II; B rejects NCERT's definition of arthritis.",
  seconds=25)

Z(LOC, "Skeletal system", "Basic", "assertion_reason",
  ar("The sternum is a part of the axial skeleton.",
     "The sternum is one of the bones of the pectoral girdle."),
  ASSERTION_REASON, "C",
  "Axial and appendicular skeleton",
  "NCERT: the axial skeleton comprises 80 bones distributed along the main axis of the body – the skull, vertebral "
  "column, sternum and ribs. The pectoral girdle belongs to the appendicular skeleton; each half of it consists of a "
  "clavicle and a scapula.",
  ["A → true", "R → false: the pectoral girdle is clavicle + scapula"],
  R_LOC("skeletal system"),
  why_others_wrong="A and B accept the false Reason; D rejects the true Assertion.",
  seconds=25)

_opts_rw = ["(a), (d) and (e) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only", "(a), (b) and (c) only"]
Z(LOC, "Muscle contraction", "Intermediate", "multi_statement",
  ms("Which of the following statements about red and white muscle fibres are correct, according to NCERT?",
     ["Red fibres have a high content of myoglobin.",
      "Red fibres contain plenty of mitochondria.",
      "White fibres have a high amount of sarcoplasmic reticulum.",
      "White fibres depend on aerobic processes for energy.",
      "Red fibres appear pale or whitish."]),
  _opts_rw, "D",
  "Red versus white muscle fibres",
  "NCERT: myoglobin content is high in some muscles, giving them a reddish appearance (red fibres); they contain "
  "plenty of mitochondria, which can utilise the large amount of oxygen stored in them for ATP production, so they "
  "can be called aerobic muscles. Other muscles possess very little myoglobin and appear pale or whitish (white "
  "fibres); they have few mitochondria but a high amount of sarcoplasmic reticulum, and they depend on anaerobic "
  "processes for energy.",
  ["(a) true", "(b) true", "(c) true", "(d) false – white fibres depend on anaerobic processes",
   "(e) false – white fibres are the pale ones"],
  R_LOC("muscle – red and white fibres"),
  why_others_wrong="A, B and C each include (d) or (e).",
  seconds=40)
ms_check("abc", _opts_rw, "D")

Z(LOC, "Muscular and skeletal disorders", "Intermediate", "assertion_reason",
  ar("Gout is an inflammation of joints.",
     "In gout, uric acid crystals accumulate in the joints."),
  ASSERTION_REASON, "A",
  "Cause of gout",
  "NCERT: gout is inflammation of joints due to accumulation of uric acid crystals. R states the cause that NCERT "
  "gives for the inflammation in A.",
  ["A → true", "R → true; 'due to' links them in NCERT"],
  R_LOC("disorders of muscular and skeletal system"),
  why_others_wrong="B denies the cause NCERT gives; C and D reject true statements.",
  seconds=25)

Z(LOC, "Joints", "Intermediate", "statement_pair",
  sp("Synovial joints allow considerable movement and play a significant role in locomotion and many other "
     "movements.",
     "The joint between the carpals is a pivot joint."),
  STATEMENT_PAIR, "C",
  "Synovial joints",
  "NCERT: synovial joints are characterised by a fluid-filled synovial cavity between the articulating surfaces of "
  "the two bones; such an arrangement allows considerable movement, and these joints play a significant role in "
  "locomotion and many other movements. The joint between the carpals is a gliding joint; the pivot joint is between "
  "the atlas and the axis.",
  ["Statement I → true", "Statement II → false: carpals form gliding joints"],
  R_LOC("joints"),
  why_others_wrong="A and D accept Statement II; B rejects the role of synovial joints in movement.",
  seconds=30)

Z(LOC, "Types of movement", "Intermediate", "match_list",
  ml(("type of movement", "example in the human body"), ["Amoeboid", "Ciliary", "Flagellar", "Muscular"],
     ["Swimming of spermatozoa", "Macrophages and leucocytes in blood",
      "Movement of the limbs, jaws and tongue", "Passage of ova through the female reproductive tract"]),
  match_options(M("II", "IV", "I", "III"), [M("II", "I", "IV", "III"), M("IV", "II", "I", "III"),
                                            M("II", "IV", "III", "I")], "B"), "B",
  "Types of movement in human cells and organs",
  "NCERT: some specialised cells in our body like macrophages and leucocytes in blood exhibit amoeboid movement; "
  "ciliary movement helps the passage of ova through the female reproductive tract; flagellar movement helps in the "
  "swimming of spermatozoa; movement of our limbs, jaws, tongue, etc., requires muscular movement.",
  ["Amoeboid → II", "Ciliary → IV", "Flagellar → I", "Muscular → III"],
  R_LOC("types of movement"),
  why_others_wrong="A swaps the ciliary and flagellar examples; C swaps amoeboid and ciliary; D swaps flagellar and "
                   "muscular.",
  seconds=35)

Z(LOC, "Muscle contraction", "Intermediate", "direct",
  "Which sequence correctly arranges the organisation of a skeletal muscle from the largest unit to the smallest?",
  ["Muscle → muscle fibres → fascicles → myofibrils → actin and myosin filaments",
   "Muscle → myofibrils → muscle fibres → fascicles → actin and myosin filaments",
   "Fascicles → muscle → muscle fibres → myofibrils → actin and myosin filaments",
   "Muscle → fascicles (muscle bundles) → muscle fibres → myofibrils → actin and myosin filaments"], "D",
  "Organisation of a skeletal muscle",
  "NCERT: each organised skeletal muscle is made of a number of muscle bundles or fascicles held together by a common "
  "collagenous connective tissue layer called fascia. Each muscle bundle contains a number of muscle fibres. Each "
  "muscle fibre has many parallelly arranged myofibrils, and each myofibril has many serially arranged units "
  "(sarcomeres) made of actin and myosin filaments.",
  ["Muscle → fascicles", "Fascicle → muscle fibres", "Muscle fibre → myofibrils", "Myofibril → actin and myosin"],
  R_LOC("structure of contractile proteins / skeletal muscle"),
  why_others_wrong="A places fibres above fascicles; B places myofibrils above fibres; C puts fascicles above the "
                   "whole muscle.",
  seconds=35)

Z(LOC, "Muscle contraction", "Intermediate", "direct",
  "Which feature is shared by skeletal and cardiac muscles but NOT by visceral muscles?",
  ["Involuntary nature", "Striated appearance", "Location in the inner walls of hollow visceral organs",
   "Voluntary control by the nervous system"], "B",
  "Comparing the three types of muscle",
  "NCERT: skeletal muscles are striped (striated) and under voluntary control; visceral muscles are smooth "
  "(non-striated) and involuntary; cardiac muscles are striated and involuntary. Striation is therefore the feature "
  "common to skeletal and cardiac muscle only.",
  ["Skeletal → striated, voluntary", "Visceral → non-striated, involuntary", "Cardiac → striated, involuntary"],
  R_LOC("muscle – types of muscles"),
  why_others_wrong="A is shared by cardiac and visceral muscle; C is true only of visceral muscle; D is true only of "
                   "skeletal muscle.",
  seconds=30)

_opts_gd = ["(a) and (b) only", "(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (b) and (c) only"]
Z(LOC, "Skeletal system", "Advanced", "multi_statement",
  ms("Which of the following statements correctly describe the human pectoral and pelvic girdles?",
     ["Each half of the pectoral girdle consists of a clavicle and a scapula.",
      "Each coxal bone of the pelvic girdle is formed by the fusion of three bones – ilium, ischium and pubis.",
      "The glenoid cavity of the scapula articulates with the head of the humerus, and the acetabulum of the coxal "
      "bone articulates with the thigh bone.",
      "The two halves of the pectoral girdle meet ventrally to form a symphysis.",
      "The pubic symphysis contains hyaline cartilage."]),
  _opts_gd, "D",
  "Pectoral and pelvic girdles compared",
  "NCERT: each half of the pectoral girdle consists of a clavicle and a scapula; the glenoid cavity below the acromion "
  "articulates with the head of the humerus. The pelvic girdle consists of two coxal bones, each formed by the fusion "
  "of ilium, ischium and pubis; at their point of fusion is the acetabulum, to which the thigh bone articulates. The "
  "two halves of the PELVIC girdle meet ventrally to form the pubic symphysis, which contains fibrous cartilage.",
  ["(a) true", "(b) true", "(c) true", "(d) false – the symphysis belongs to the pelvic girdle",
   "(e) false – the pubic symphysis has fibrous cartilage"],
  R_LOC("skeletal system – appendicular skeleton"),
  why_others_wrong="A leaves out the true (c); B adds (e); C adds (d) and (e) and leaves out (a) and (c).",
  seconds=55)
ms_check("abc", _opts_gd, "D")

Z(LOC, "Muscle contraction", "Advanced", "assertion_reason",
  ar("A skeletal muscle fibre is described as a syncytium.",
     "The sarcoplasm of a skeletal muscle fibre contains many nuclei."),
  ASSERTION_REASON, "A",
  "Multinucleate muscle fibres",
  "NCERT: each muscle fibre is lined by the plasma membrane called the sarcolemma enclosing the sarcoplasm, and the "
  "muscle fibre is a syncitium as the sarcoplasm contains many nuclei. R is exactly the reason NCERT gives for A.",
  ["A → true", "R → true; 'as' links them in NCERT"],
  R_LOC("skeletal muscle"),
  why_others_wrong="B denies the stated link; C and D reject true statements.",
  seconds=30)

Z(LOC, "Skeletal system", "Advanced", "statement_pair",
  sp("The appendicular skeleton of a human contains more bones than the axial skeleton.",
     "The hyoid and the ear ossicles are counted in the axial skeleton."),
  STATEMENT_PAIR, "A",
  "Dividing the 206 bones",
  "NCERT: the axial skeleton comprises 80 bones – the skull (22 cranial and facial bones, the hyoid and the three ear "
  "ossicles in each middle ear), the 26 vertebrae, the sternum and 12 pairs of ribs. The appendicular skeleton – "
  "limbs (30 bones each) and girdles (two clavicles, two scapulae, two coxal bones) – has 126 bones.",
  ["Axial: 22 + 1 + 6 + 26 + 1 + 24 = 80", "Appendicular: 4 × 30 + 2 + 2 + 2 = 126 > 80",
   "Hyoid and ossicles are part of the skull → axial"],
  R_LOC("skeletal system"),
  why_others_wrong="B, C and D each reject a true statement; the hyoid and ossicles are part of the skull's count.",
  seconds=50)

Z(LOC, "Muscle contraction", "Advanced", "match_list",
  ml(("structure in a myofibril", "description"),
     ["H-zone", "Z-line", "M-line", "Sarcomere"],
     ["Portion of the myofibril between two successive Z-lines",
      "Thin fibrous membrane holding the thick filaments together in the middle of the A-band",
      "Central part of the thick filaments not overlapped by the thin filaments in the resting state",
      "Elastic fibre that bisects the I-band and to which the thin filaments are firmly attached"]),
  match_options(M("III", "IV", "II", "I"), [M("III", "II", "IV", "I"), M("II", "IV", "III", "I"),
                                            M("III", "IV", "I", "II")], "B"), "B",
  "Landmarks of the sarcomere",
  "NCERT: in the centre of each I-band is an elastic fibre called the Z-line, which bisects it, and the thin filaments "
  "are firmly attached to it; the thick filaments in the A-band are held together in the middle by a thin fibrous "
  "membrane called the M-line; the portion of the myofibril between two successive Z-lines is the sarcomere; in the "
  "resting state the central part of the thick filaments not overlapped by the thin filaments is the H-zone.",
  ["H-zone → III", "Z-line → IV", "M-line → II", "Sarcomere → I"],
  R_LOC("structure of contractile proteins"),
  why_others_wrong="A swaps the Z-line and the M-line; C swaps the H-zone and the M-line; D swaps the M-line and the "
                   "sarcomere.",
  seconds=45)

Z(LOC, "Skeletal system", "Advanced", "direct",
  "Which of the following pairs DIFFER in number between one human hand (with its wrist) and one foot (with its "
  "ankle)?",
  ["Metacarpals and metatarsals", "Phalanges of the hand and phalanges of the foot",
   "All the bones of one upper limb and all the bones of one lower limb", "Carpals and tarsals"], "D",
  "Comparing the bones of the fore and hind limbs",
  "NCERT: each upper limb has 8 carpals, 5 metacarpals and 14 phalanges; each lower limb has 7 tarsals, 5 metatarsals "
  "and 14 phalanges. Each limb – upper or lower – is made of 30 bones (the lower limb includes the patella).",
  ["Carpals 8 vs tarsals 7 → differ", "Metacarpals 5 = metatarsals 5", "Phalanges 14 = 14",
   "Upper limb 30 = lower limb 30"],
  R_LOC("skeletal system – appendicular skeleton"),
  why_others_wrong="A, B and C are equal pairs (5 and 5, 14 and 14, 30 and 30).",
  seconds=45)

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
           "notes": "BATCH_009 package ZOO_009_p1: 119 original Zoology questions on Animal Kingdom, Structural "
                    "Organisation in Animals, Biomolecules, Breathing and Exchange of Gases, Body Fluids and "
                    "Circulation, Excretory Products and their Elimination, and Locomotion and Movement. Facts from the rationalised NCERT Class 11 Biology textbook, avoiding "
                    "questions already asked in BATCH_000-BATCH_008 (many items are application, comparison or "
                    "scenario questions on NCERT mechanisms); every numerical answer re-derived by "
                    "tools/batch_009/ZOO_009_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, difficulty {dict(Counter(x['difficulty'] for x in QUESTIONS))}, "
          f"keys {dict(sorted(keys.items()))}, formats {dict(fmts)}")
