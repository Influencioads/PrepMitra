
# =============================================================== 3. Morphology of Flowering Plants (5/7/5)
direct(T_MOR, "Flower", "Basic",
       "Each stamen, which represents the male reproductive organ of a flower, consists of:",
       "a stalk or filament and an anther",
       ["a style and a stigma", "an ovary and ovules", "a pedicel and a thalamus"], "B",
       "Parts of a stamen",
       "The androecium is composed of stamens. Each stamen consists of a stalk or filament and an anther. Each "
       "anther is usually bilobed and each lobe has two chambers, the pollen sacs, in which pollen grains are "
       "produced.",
       ["Stamen = filament + anther"],
       why="Stigma, style and ovary are parts of a carpel; the pedicel and thalamus are the flower stalk and its "
           "swollen end.",
       ncert=ref("MOR", "The Flower (Androecium)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "NCERT lists the main functions of the root system. Which of the following is NOT one of them?",
       "Photosynthesis",
       ["Synthesis of plant growth regulators", "Storing reserve food material",
        "Providing a proper anchorage to the plant parts"], "C",
       "Functions of the root system",
       "The main functions of the root system are absorption of water and minerals from the soil, providing a "
       "proper anchorage to the plant parts, storing reserve food material and synthesis of plant growth "
       "regulators. Photosynthesis is a function of leaves (and of green stems in some plants), not of the root "
       "system.",
       ["Root: absorption, anchorage, food storage, synthesis of plant growth regulators"],
       why="The other three are all listed by NCERT as functions of the root system.",
       ncert=ref("MOR", "The Root"), secs=25)

direct(T_MOR, "Flower", "Basic",
       "The arrangement of ovules within the ovary is known as:",
       "placentation",
       ["aestivation", "phyllotaxy", "venation"], "D",
       "Definition of placentation",
       "The arrangement of ovules within the ovary is known as placentation; its main types are marginal, axile, "
       "parietal, basal, central and free central.",
       ["Ovules in ovary → placentation"],
       why="Aestivation is the arrangement of sepals or petals in a bud, phyllotaxy the arrangement of leaves on "
           "the stem, and venation the arrangement of veins in the lamina.",
       ncert=ref("MOR", "The Flower (Gynoecium)"), secs=20)

direct(T_MOR, "Flower", "Basic",
       "The mode of arrangement of sepals or petals in a floral bud with respect to the other members of the same "
       "whorl is known as:",
       "aestivation",
       ["placentation", "inflorescence", "phyllotaxy"], "A",
       "Definition of aestivation",
       "The mode of arrangement of sepals or petals in a floral bud with respect to the other members of the same "
       "whorl is known as aestivation. Its main types are valvate, twisted, imbricate and vexillary.",
       ["Arrangement of sepals or petals in bud → aestivation"],
       why="Placentation refers to ovules in the ovary, inflorescence to flowers on the floral axis, and phyllotaxy "
           "to leaves on the stem.",
       ncert=ref("MOR", "The Flower (Aestivation)"), secs=20)

statement_pair(T_MOR, "Fruit and seed", "Basic",
               "The fruit is a characteristic feature of the flowering plants.",
               "Leaves are the most important vegetative organs for photosynthesis.",
               True, True, "A",
               "Fruit and leaf",
               "NCERT states that the fruit is a characteristic feature of the flowering plants; it is a mature or "
               "ripened ovary developed after fertilisation. It also states that leaves are the most important "
               "vegetative organs for photosynthesis.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Leaf; The Fruit"), secs=25)

match_list(T_MOR, "Root, stem and leaf", "Intermediate", "plant", "storage organ",
           ["Sweet potato", "Carrot", "Zaminkand", "Garlic"],
           ["Fleshy leaves", "Swollen adventitious roots", "Swollen tap root", "Underground stem"],
           "II III IV I", ["III II IV I", "II III I IV", "IV III II I"], "B",
           "Organs that store food",
           "Food is stored in swollen adventitious roots in sweet potato and in the swollen tap root in carrot. "
           "Underground stems of potato, ginger, turmeric, zaminkand and Colocasia store food. The fleshy leaves of "
           "onion and garlic store food.",
           ["Sweet potato → adventitious root", "Carrot → tap root", "Zaminkand → underground stem",
            "Garlic → fleshy leaves"],
           why="The wrong codes swap the two kinds of storage root, or swap the stem and the leaves.",
           ncert=ref("MOR", "The Root; The Stem; The Leaf (modifications)"), secs=45)

direct(T_MOR, "Plant families", "Intermediate",
       "In the floral formula of the family Fabaceae, the androecium is written as A(9)+1. This means that the "
       "flower has:",
       "ten stamens, nine of which are united into one bundle while one is free (diadelphous)",
       ["nine stamens united with the petals and one sterile stamen (staminode)",
        "ten free stamens arranged in two whorls",
        "nine stamens and one carpel"], "B",
       "Reading the androecium in a floral formula",
       "In a floral formula, fusion is shown by enclosing the figure within brackets. In Fabaceae the androecium "
       "has ten stamens and is diadelphous: nine are united into one bundle, written (9), and one is free, written "
       "+1. The anthers are dithecous.",
       ["Brackets = fusion", "(9)+1 = nine fused + one free = diadelphous"],
       why="Union with petals (epipetaly) is shown by a line joining C and A, not by brackets. 'Free in two whorls' "
           "ignores the brackets. The carpel is shown separately by G1.",
       ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=40)

assertion_reason(T_MOR, "Root, stem and leaf", "Intermediate",
                 "Mustard plants have a tap root system.",
                 "In mustard, the primary root formed by direct elongation of the radicle grows inside the soil and "
                 "bears lateral roots of several orders.",
                 True, True, True, "A",
                 "Tap root system",
                 "In majority of dicotyledonous plants the direct elongation of the radicle leads to the formation of "
                 "the primary root, which grows inside the soil and bears lateral roots of several orders (secondary, "
                 "tertiary roots). The primary root and its branches constitute the tap root system, as seen in "
                 "mustard. R describes exactly what makes it a tap root system.",
                 ["A: true", "R: true and explains A"],
                 ncert=ref("MOR", "The Root"), secs=35)

multi_statement(T_MOR, "Root, stem and leaf", "Intermediate",
                "Which of the following statements about the leaf are correct?",
                [("A typical leaf consists of three main parts: the leaf base, the petiole and the lamina.", True),
                 ("The leaf base may bear two lateral small leaf-like structures called stipules.", True),
                 ("The petiole helps hold the blade to light.", True),
                 ("In a pinnately compound leaf, the leaflets are attached at a common point, the tip of the "
                  "petiole.", False),
                 ("The lamina has a prominent middle vein called the midrib.", True)],
                ["abcd", "bce", "acde"], "B",
                "Parts of a leaf",
                "A typical leaf has a leaf base, petiole and lamina. The leaf is attached to the stem by the leaf "
                "base, which may bear two lateral small leaf-like stipules. The petiole helps hold the blade to "
                "light. The lamina is the green expanded part with veins and veinlets, and the middle prominent vein "
                "is the midrib. In a pinnately compound leaf the leaflets lie on a common axis, the rachis; leaflets "
                "attached at the tip of the petiole make a palmately compound leaf.",
                ["(a), (b), (c), (e): true", "(d): false, this describes a palmately compound leaf"],
                why="Each wrong combination includes (d) or leaves out a true statement.",
                ncert=ref("MOR", "The Leaf"), secs=50)

statement_pair(T_MOR, "Fruit and seed", "Intermediate",
               "In a dicotyledonous seed, the embryo consists of an embryonal axis and two cotyledons.",
               "In the embryo of maize, the coleoptile encloses the radicle.",
               True, False, "C",
               "Embryos of dicot and monocot seeds",
               "The embryo of a dicotyledonous seed consists of an embryonal axis and two cotyledons; the radicle "
               "and plumule are at the two ends of the axis. In the maize embryo there is one shield-shaped "
               "cotyledon, the scutellum; the plumule is enclosed in a sheath called the coleoptile and the "
               "radicle in a sheath called the coleorhiza.",
               ["Statement I: true", "Statement II: false, the coleoptile encloses the plumule"],
               ncert=ref("MOR", "The Seed"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "A flower is bisexual and actinomorphic, with six tepals in two whorls, six stamens attached to the perianth, "
       "and a superior, tricarpellary, syncarpous ovary. Which of the following plants could bear this flower?",
       "Tulip",
       ["Petunia", "Lupin", "China rose"], "A",
       "Identifying a flower of Liliaceae",
       "The features are those of Liliaceae: perianth of six tepals (3 + 3), six epiphyllous stamens (3 + 3) and "
       "a superior, tricarpellary, syncarpous ovary. Tulip and Gloriosa are ornamental plants of Liliaceae.",
       ["P(3+3), A3+3 epiphyllous, G(3) superior → Liliaceae", "Tulip belongs to Liliaceae"],
       why="Petunia (Solanaceae) has a pentamerous flower with bicarpellary ovary. Lupin (Fabaceae) has a "
           "zygomorphic flower with one carpel. China rose has monoadelphous stamens, a distinct calyx and corolla.",
       ncert=ref("MOR", "Description of Some Important Families (Liliaceae)"), secs=40)

direct(T_MOR, "Root, stem and leaf", "Intermediate",
       "Which of the following is NOT a modification of the stem?",
       "Spines of cactus",
       ["Tendrils of watermelon", "Thorns of Bougainvillea", "Flattened green structures of Opuntia"], "D",
       "Stem and leaf modifications",
       "Stem tendrils develop from axillary buds in gourds such as cucumber, pumpkin and watermelon. Axillary buds "
       "of stems are modified into thorns in Citrus and Bougainvillea. In Opuntia the stem is modified into "
       "flattened green structures that photosynthesise. In cacti, the leaves are modified into spines.",
       ["Watermelon tendril, Bougainvillea thorn, Opuntia flattened stem → stem",
        "Cactus spines → leaf"],
       why="Tendrils of watermelon, thorns of Bougainvillea and the flattened structures of Opuntia are all "
           "modified stems.",
       ncert=ref("MOR", "The Stem; The Leaf (modifications)"), secs=35)

multi_statement(T_MOR, "Plant families", "Advanced",
                "Which of the following statements correctly compare the families Solanaceae and Liliaceae?",
                [("Both have a bilocular ovary.", False),
                 ("Both have axile placentation.", True),
                 ("The stamens are epipetalous in Solanaceae and epiphyllous in Liliaceae.", True),
                 ("Both have endospermous seeds.", True),
                 ("Both have a persistent calyx.", False)],
                ["abc", "bcde", "cde"], "B",
                "Solanaceae and Liliaceae compared",
                "Solanaceae: bicarpellary, syncarpous, bilocular ovary with axile placentation; five epipetalous "
                "stamens; calyx persistent; seeds many, endospermous. Liliaceae: tricarpellary, syncarpous, "
                "trilocular ovary with axile placentation; six tepals, six epiphyllous stamens; seeds endospermous. "
                "Liliaceae has a perianth, not a separate calyx, so it cannot have a persistent calyx.",
                ["(b), (c), (d): true", "(a): false, Liliaceae ovary is trilocular",
                 "(e): false, Liliaceae has tepals, not a calyx"],
                why="Each wrong combination includes (a) or (e), or leaves out a true statement.",
                ncert=ref("MOR", "Description of Some Important Families (Solanaceae; Liliaceae)"), secs=60)

multi_statement(T_MOR, "Inflorescence", "Advanced",
                "In the inflorescence of a plant, the older flowers are at the base and the younger flowers towards "
                "the apex of the main axis. Which of the following statements about it are correct?",
                [("The inflorescence is racemose.", True),
                 ("The main axis has terminated in a flower.", False),
                 ("Plants of the family Fabaceae have this type of inflorescence.", True),
                 ("The inflorescence of Liliaceae, often in umbellate clusters, is of this type.", False),
                 ("The flowers are borne in acropetal succession.", True)],
                ["abe", "acd", "ce"], "A",
                "Recognising a racemose inflorescence",
                "In racemose inflorescences the main axis continues to grow and the flowers are borne laterally in "
                "acropetal succession, so older flowers are lower and younger flowers nearer the apex. In cymose "
                "inflorescences the main axis terminates in a flower and flowers are borne in basipetal order. "
                "Fabaceae has a racemose inflorescence; Liliaceae has a solitary or cymose inflorescence, often in "
                "umbellate clusters.",
                ["Older below, younger above → acropetal → racemose", "Fabaceae: racemose",
                 "Liliaceae: solitary or cymose"],
                why="Each wrong combination includes (b) or (d), which describe cymose features, or omits a true "
                    "statement.",
                ncert=ref("MOR", "The Inflorescence; Description of Some Important Families"), secs=60)

numerical(T_MOR, "Plant families", "Advanced",
          "The floral formula of Fabaceae is % ⚥ K(5) C1+2+(2) A(9)+1 G1. Counting every individual sepal, petal, "
          "stamen and carpel separately, how many floral members does one such flower have?",
          "21",
          ["17", "13", "20"], "D",
          (5 + (1 + 2 + 2) + (9 + 1) + 1 == 21),
          "Counting floral members from a formula",
          "Brackets show fusion, not a single member. K(5) = 5 united sepals; C1+2+(2) = 1 standard + 2 wings + 2 "
          "united keel petals = 5; A(9)+1 = 10 stamens; G1 = 1 carpel. Total = 5 + 5 + 10 + 1 = 21.",
          ["K: 5", "C: 1 + 2 + 2 = 5", "A: 9 + 1 = 10", "G: 1", "Total = 21"],
          why="17 counts the five fused sepals as one member. 13 counts the stamens as two units (one bundle + one "
              "free). 20 counts the two fused keel petals as a single petal.",
          ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=60)

statement_pair(T_MOR, "Flower", "Advanced",
               "On the basis of its floral formula, a flower of Liliaceae is trimerous.",
               "On the basis of its floral formula, a flower of Solanaceae is tetramerous.",
               True, False, "C",
               "Merous condition from floral formulae",
               "A flower is trimerous, tetramerous or pentamerous when its floral appendages are in multiples of 3, 4 "
               "or 5. Liliaceae: P(3+3) A3+3 G(3), all in threes, so trimerous. Solanaceae: K(5) C(5) A5 G(2), the "
               "perianth whorls and stamens in fives, so pentamerous, not tetramerous.",
               ["Liliaceae: 3 + 3, 3 + 3, 3 → trimerous", "Solanaceae: 5, 5, 5 → pentamerous"],
               ncert=ref("MOR", "The Flower; Description of Some Important Families"), secs=45)

assertion_reason(T_MOR, "Flower", "Advanced",
                 "In epigynous flowers, the ovary is superior.",
                 "In hypogynous flowers, the gynoecium occupies the highest position and the other parts are situated "
                 "below it.",
                 False, True, False, "D",
                 "Position of the ovary",
                 "In hypogynous flowers the gynoecium occupies the highest position and the other parts lie below it; "
                 "the ovary is superior (mustard, china rose, brinjal). In epigynous flowers the margin of the "
                 "thalamus grows upward, encloses the ovary completely and fuses with it, and the other parts arise "
                 "above the ovary, so the ovary is inferior (guava, cucumber, ray florets of sunflower). A is false, "
                 "R is true.",
                 ["A: false, an epigynous flower has an inferior ovary", "R: true"],
                 ncert=ref("MOR", "The Flower (position of floral parts on the thalamus)"), secs=40)
