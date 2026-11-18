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
