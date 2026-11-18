
# =============================================================== 3. Morphology of Flowering Plants (6/7/6)
direct(T_MOR, "Flower", "Basic",
       "Of the four whorls of a typical flower, which are described by NCERT as the reproductive organs?",
       "Androecium and gynoecium",
       ["Calyx and corolla", "Calyx and androecium", "Corolla and gynoecium"], "B",
       "Accessory and reproductive whorls",
       "A typical flower has four whorls: calyx, corolla, androecium and gynoecium. Calyx and corolla are accessory "
       "organs, while androecium and gynoecium are reproductive organs.",
       ["Accessory organs: calyx, corolla", "Reproductive organs: androecium, gynoecium"],
       why="Calyx and corolla are accessory organs; each of the other wrong pairs contains one accessory whorl.",
       ncert=ref("MOR", "The Flower"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "According to NCERT, the main function of the stem is:",
       "spreading out branches bearing leaves, flowers and fruits",
       ["absorption of water and minerals from the soil", "protecting the flower in the bud stage",
        "anchoring the plant parts firmly in the soil"], "B",
       "Functions of the stem",
       "The main function of the stem is spreading out branches bearing leaves, flowers and fruits. It conducts water, "
       "minerals and photosynthates. Some stems also store food, give support and protection, and help in vegetative "
       "propagation.",
       ["Main function: bearing and spreading out branches with leaves, flowers and fruits",
        "Also: conduction of water, minerals and photosynthates"],
       why="Absorption and anchorage are functions of the root system; protecting the flower in the bud is the "
           "function of the sepals.",
       ncert=ref("MOR", "The Stem"), secs=20)

statement_pair(T_MOR, "Plant families", "Basic",
               "In the family Fabaceae, the stem may be erect or a climber.",
               "Members of the family Solanaceae are mostly herbs and shrubs, and rarely small trees.",
               True, True, "A",
               "Habit in Fabaceae and Solanaceae",
               "In NCERT's description of Fabaceae, the stem is erect or climber. Solanaceae plants are mostly herbs, "
               "shrubs and rarely small trees; the stem is herbaceous, rarely woody.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "Description of Some Important Families (Fabaceae, Solanaceae)"), secs=30)

direct(T_MOR, "Inflorescence", "Basic",
       "The arrangement of flowers on the floral axis is termed:",
       "inflorescence",
       ["aestivation", "placentation", "phyllotaxy"], "D",
       "Inflorescence",
       "A flower is a modified shoot. The arrangement of flowers on the floral axis is termed inflorescence; depending "
       "on whether the apex grows into a flower or continues to grow, it is cymose or racemose.",
       ["Arrangement of flowers on the floral axis = inflorescence"],
       why="Aestivation is the arrangement of sepals or petals in a bud; placentation is the arrangement of ovules in "
           "the ovary; phyllotaxy is the arrangement of leaves on the stem or branch.",
       ncert=ref("MOR", "Inflorescence"), secs=20)

match_list(T_MOR, "Flower", "Basic", "term", "meaning",
           ["Pedicel", "Thalamus", "Bract", "Perianth"],
           ["Reduced leaf found at the base of the pedicel", "Calyx and corolla when they are not distinct",
            "Stalk of the flower", "Swollen end of the stalk on which the floral whorls are borne"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A",
           "Parts of a flower",
           "The four whorls of a typical flower are arranged successively on the swollen end of the stalk or pedicel, "
           "called the thalamus or receptacle. Flowers with a bract, a reduced leaf found at the base of the pedicel, "
           "are bracteate. When calyx and corolla are not distinct, as in lily, they are termed the perianth.",
           ["Pedicel -> stalk", "Thalamus -> swollen end bearing the whorls", "Bract -> reduced leaf at the pedicel base",
            "Perianth -> undifferentiated calyx and corolla"],
           why="The wrong codes swap pedicel and thalamus, bract and perianth, or pedicel and bract.",
           ncert=ref("MOR", "The Flower; Parts of a Flower"), secs=30)

direct(T_MOR, "Flower", "Basic",
       "Each carpel of the gynoecium is made up of:",
       "stigma, style and ovary",
       ["filament and anther", "stigma, style and placenta only", "ovary and pedicel"], "B",
       "Parts of a carpel",
       "The gynoecium is the female reproductive part of the flower and is made up of one or more carpels. A carpel "
       "consists of three parts, namely stigma, style and ovary. The ovary bears one or more ovules attached to a "
       "flattened, cushion-like placenta.",
       ["Carpel = stigma + style + ovary"],
       why="Filament and anther make a stamen. The placenta lies inside the ovary and is not a separate part replacing "
           "it. The pedicel is the stalk of the flower.",
       ncert=ref("MOR", "Parts of a Flower (gynoecium)"), secs=20)

match_list(T_MOR, "Flower", "Intermediate", "plant", "condition of the stamens",
           ["Pea", "Brinjal", "Lily", "China rose"],
           ["Epiphyllous", "Monoadelphous", "Diadelphous", "Epipetalous"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "C",
           "Union and attachment of stamens",
           "Stamens may be united among themselves or attached to other floral members. In pea they are in two bundles "
           "(diadelphous). In brinjal they are attached to the petals (epipetalous). In lily they are attached to the "
           "perianth (epiphyllous). In china rose they are united into one bundle (monoadelphous).",
           ["Pea -> diadelphous", "Brinjal -> epipetalous", "Lily -> epiphyllous", "China rose -> monoadelphous"],
           why="The wrong codes swap pea and brinjal, lily and china rose, or brinjal and lily.",
           ncert=ref("MOR", "Parts of a Flower (androecium)"), secs=40)

assertion_reason(T_MOR, "Plant families", "Intermediate",
                 "In the family Fabaceae, the fruit is a legume.",
                 "In the family Fabaceae, the leaf base is pulvinate.",
                 True, True, False, "B",
                 "Fruit and leaf base in Fabaceae",
                 "NCERT's description of Fabaceae gives the fruit as a legume and the seeds as one to many, "
                 "non-endospermic. Among the vegetative characters, the leaves are pinnately compound or simple, the "
                 "leaf base is pulvinate and stipulate. The swollen leaf base is a feature of the leaf and has nothing "
                 "to do with the kind of fruit formed from the ovary.",
                 ["A: true", "R: true", "R is a vegetative feature, unrelated to the fruit type"],
                 ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=35)

multi_statement(T_MOR, "Plant families", "Intermediate",
                "Which of the following plants belong to the family Solanaceae?",
                [("Belladonna", True), ("Muliathi", False), ("Petunia", True), ("Gloriosa", False),
                 ("Ashwagandha", True)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("c", "e")], "D",
                "Members of Solanaceae",
                "NCERT lists as Solanaceae: tomato, brinjal and potato (food), chilli (spice), belladonna and ashwagandha "
                "(medicine), tobacco (fumigatory) and petunia (ornamental). Muliathi is a medicinal plant of Fabaceae, "
                "and Gloriosa is an ornamental of Liliaceae.",
                ["(a) Solanaceae", "(b) Fabaceae", "(c) Solanaceae", "(d) Liliaceae", "(e) Solanaceae"],
                ncert=ref("MOR", "Description of Some Important Families (economic importance)"), secs=45)

statement_pair(T_MOR, "Plant families", "Intermediate",
               "In the family Liliaceae, the perianth shows valvate aestivation.",
               "In the family Fabaceae, the calyx shows valvate aestivation.",
               True, False, "C",
               "Aestivation in Liliaceae and Fabaceae",
               "In Liliaceae, the perianth has six tepals (3 + 3), often united into a tube, with valvate aestivation. In "
               "Fabaceae, the calyx has five gamosepalous sepals with imbricate aestivation, and the corolla shows "
               "vexillary aestivation.",
               ["Statement I: true", "Statement II: false; the Fabaceae calyx is imbricate"],
               ncert=ref("MOR", "Description of Some Important Families (Liliaceae, Fabaceae)"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "A plant has root nodules, stipulate pinnately compound leaves with a pulvinate leaf base, a racemose "
       "inflorescence and zygomorphic flowers with a papilionaceous corolla. Its seeds are expected to be:",
       "non-endospermic",
       ["endospermous, many in a berry or capsule", "endospermous, in a trilocular capsule",
        "endospermous, with a bulky endosperm separated from the embryo by an aleurone layer"], "A",
       "Identifying Fabaceae and its seed",
       "Root nodules, pulvinate stipulate leaves, racemose inflorescence and a papilionaceous corolla are the "
       "characters of Fabaceae. In Fabaceae the fruit is a legume and the seeds are one to many and non-endospermic.",
       ["Characters -> family Fabaceae", "Fabaceae seeds: non-endospermic"],
       why="Many endospermous seeds in a berry or capsule describe Solanaceae; endospermous seeds in a trilocular "
           "capsule describe Liliaceae; a bulky endosperm with an aleurone layer describes a cereal grain such as "
           "maize.",
       ncert=ref("MOR", "Description of Some Important Families (Fabaceae)"), secs=40)

assertion_reason(T_MOR, "Flower", "Intermediate",
                 "In lotus and rose, the gynoecium is syncarpous.",
                 "In mustard and tomato, the carpels of the gynoecium are fused together.",
                 False, True, False, "D",
                 "Apocarpous and syncarpous gynoecium",
                 "When more than one carpel is present, they may be free, as in lotus and rose (apocarpous), or fused "
                 "together, as in mustard and tomato (syncarpous).",
                 ["A: false; lotus and rose are apocarpous", "R: true"],
                 ncert=ref("MOR", "Parts of a Flower (gynoecium)"), secs=30)

direct(T_MOR, "Flower", "Intermediate",
       "In a floral diagram, the calyx, corolla, androecium and gynoecium are drawn in successive whorls. Which whorl "
       "is drawn outermost and which in the centre?",
       "Calyx outermost; gynoecium in the centre",
       ["Gynoecium outermost; calyx in the centre", "Corolla outermost; androecium in the centre",
        "Androecium outermost; gynoecium in the centre"], "D",
       "Floral diagram",
       "A floral diagram gives information about the number of parts of a flower, their arrangement and their "
       "relation to one another. The position of the mother axis is shown by a dot on top of the diagram. Calyx, "
       "corolla, androecium and gynoecium are drawn in successive whorls, calyx being the outermost and gynoecium "
       "being in the centre.",
       ["Order from outside: calyx, corolla, androecium, gynoecium"],
       why="The other options reverse or misplace the order of the whorls.",
       ncert=ref("MOR", "Semi-technical Description of a Typical Flowering Plant"), secs=30)

multi_statement(T_MOR, "Plant families", "Advanced",
                "The floral formula of a family is % ⚥ K(5) C1+2+(2) A(9)+1 G1. Which of the following conclusions "
                "drawn from it are correct?",
                [("The flower is zygomorphic and bisexual.", True),
                 ("The calyx is gamosepalous.", True),
                 ("Two of the petals are united with each other.", True),
                 ("The gynoecium is syncarpous.", False),
                 ("All ten stamens are united into one bundle.", False)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d")], "B",
                "Reading the floral formula of Fabaceae",
                "% stands for a zygomorphic flower and ⚥ for bisexual. K(5): five united sepals (gamosepalous). "
                "C1+2+(2): one standard, two wings and two anterior petals united (the keel). A(9)+1: nine stamens "
                "united and one free (diadelphous). G1: a single carpel, so the gynoecium is monocarpellary, not "
                "syncarpous.",
                ["(a) true: % and ⚥", "(b) true: K(5)", "(c) true: (2) in the corolla",
                 "(d) false: G1 is a single carpel", "(e) false: (9) + 1 means nine united, one free"],
                ncert=ref("MOR", "Description of Some Important Families (Fabaceae); Semi-technical Description"),
                secs=70)

match_list(T_MOR, "Plant families", "Advanced", "family or plant", "gynoecium",
           ["Fabaceae", "Solanaceae", "Liliaceae", "Rose"],
           ["Tricarpellary, syncarpous, trilocular ovary with axile placentation",
            "Monocarpellary, unilocular ovary with many ovules",
            "Bicarpellary, obliquely placed, syncarpous, bilocular ovary with a swollen placenta",
            "Carpels free (apocarpous)"],
           "II III I IV", ["III II I IV", "II III IV I", "II I III IV"], "A",
           "Gynoecium of the families",
           "Fabaceae: ovary superior, monocarpellary, unilocular with many ovules, style single. Solanaceae: "
           "bicarpellary, obliquely placed, syncarpous; ovary superior, bilocular, placenta swollen with many ovules, "
           "axile. Liliaceae: tricarpellary, syncarpous, ovary superior, trilocular with many ovules, axile "
           "placentation. In rose the carpels are free (apocarpous).",
           ["Fabaceae -> II", "Solanaceae -> III", "Liliaceae -> I", "Rose -> IV"],
           why="The wrong codes swap Fabaceae and Solanaceae, Liliaceae and rose, or Solanaceae and Liliaceae.",
           ncert=ref("MOR", "Description of Some Important Families; Parts of a Flower (gynoecium)"), secs=60)

assertion_reason(T_MOR, "Plant families", "Advanced",
                 "In the floral formula of Solanaceae, a line is drawn above the symbols C and A, joining them.",
                 "In Solanaceae the stamens are epipetalous, and adhesion of floral parts is shown in a floral formula "
                 "by a line drawn above the symbols of those parts.",
                 True, True, True, "A",
                 "Adhesion in a floral formula",
                 "In a floral formula, fusion is indicated by enclosing the figure within brackets and adhesion by a "
                 "line drawn above the symbols of the floral parts. The five stamens of Solanaceae are epipetalous, "
                 "that is, adhered to the petals, so the C and A symbols in its formula are joined by such a line.",
                 ["A: true", "R: true", "Epipetaly is adhesion of A to C, which is drawn as the line; R explains A"],
                 ncert=ref("MOR", "Semi-technical Description; Description of Some Important Families (Solanaceae)"),
                 secs=45)

direct(T_MOR, "Flower", "Advanced",
       "In which of the following pairs do BOTH plants show the same type of placentation?",
       "Tomato and lemon",
       ["Pea and mustard", "Dianthus and sunflower", "Argemone and primrose"], "D",
       "Types of placentation",
       "Axile placentation, with ovules attached to a central placenta in a multilocular ovary, is seen in china "
       "rose, tomato and lemon. Pea has marginal placentation; mustard and Argemone parietal; Dianthus and primrose "
       "free central; sunflower and marigold basal.",
       ["Tomato = axile; lemon = axile"],
       why="Pea (marginal) and mustard (parietal) differ; Dianthus (free central) and sunflower (basal) differ; "
           "Argemone (parietal) and primrose (free central) differ.",
       ncert=ref("MOR", "Parts of a Flower (placentation)"), secs=45)

statement_pair(T_MOR, "Plant families", "Advanced",
               "In both Solanaceae and Liliaceae, the fruit may be a berry.",
               "In both Fabaceae and Solanaceae, the seeds are endospermous.",
               True, False, "C",
               "Fruits and seeds of the three families",
               "Solanaceae fruits are berries or capsules, and Liliaceae fruits are capsules, rarely berries, so a berry "
               "is possible in both. Seeds are endospermous in Solanaceae and Liliaceae, but non-endospermic in "
               "Fabaceae.",
               ["Statement I: true", "Statement II: false; Fabaceae seeds are non-endospermic"],
               ncert=ref("MOR", "Description of Some Important Families"), secs=45)

multi_statement(T_MOR, "Inflorescence", "Advanced",
                "Which of the following statements about the cymose type of inflorescence are correct?",
                [("The main axis terminates in a flower.", True),
                 ("The main axis is limited in growth.", True),
                 ("The flowers are borne in a basipetal order.", True),
                 ("It is the inflorescence of the family Fabaceae.", False),
                 ("In Liliaceae, the inflorescence may be cymose, often in umbellate clusters.", True)],
                [("a", "b", "c", "d"), ("a", "c", "d", "e"), ("b", "c", "e")], "D",
                "Cymose inflorescence",
                "In cymose inflorescence the main axis terminates in a flower and is therefore limited in growth; the "
                "flowers are borne in a basipetal order. Fabaceae has a racemose inflorescence. In Liliaceae the "
                "inflorescence is solitary or cymose, often in umbellate clusters.",
                ["(a), (b), (c) true", "(d) false; Fabaceae is racemose", "(e) true"],
                ncert=ref("MOR", "Inflorescence; Description of Some Important Families"), secs=55)
