
# =============================================================== 3. Morphology of Flowering Plants (5/6/5)
direct(T_MOR, "Flower", "Basic",
       "In twisted aestivation, one margin of each petal overlaps that of the next one. Which of the following plants "
       "shows twisted aestivation?",
       "Lady's finger",
       ["Calotropis", "Pea", "Gulmohur"], "A",
       "Types of aestivation",
       "If one margin of an appendage overlaps that of the next one and so on, the aestivation is twisted, as in "
       "china rose, lady's finger and cotton. Calotropis shows valvate aestivation, Cassia and gulmohur imbricate, and "
       "pea and bean vexillary aestivation.",
       ["Twisted: china rose, lady's finger, cotton"],
       why="Calotropis is valvate, pea is vexillary and gulmohur is imbricate.",
       ncert=ref("MOR", "The Flower (aestivation)"), secs=20)

direct(T_MOR, "Flower", "Basic",
       "Each ovary bears one or more ovules attached to a flattened, cushion-like:",
       "placenta",
       ["thalamus", "style", "stigma"], "B",
       "Parts of the gynoecium",
       "Each carpel consists of three parts: stigma, style and ovary. The ovary is the enlarged basal part, on which "
       "lies the elongated style connecting the ovary to the stigma. Each ovary bears one or more ovules attached to "
       "a flattened, cushion-like placenta.",
       ["Ovules are attached to the placenta inside the ovary"],
       why="The thalamus is the swollen end of the pedicel bearing the floral whorls; the style connects the ovary to "
           "the stigma; the stigma receives pollen.",
       ncert=ref("MOR", "The Flower (gynoecium)"), secs=20)

direct(T_MOR, "Root, stem and leaf", "Basic",
       "In the alternate type of phyllotaxy:",
       "a single leaf arises at each node in an alternate manner",
       ["a pair of leaves arises at each node, opposite each other",
        "more than two leaves arise at a node and form a whorl",
        "all the leaves arise from the base of the stem"], "D",
       "Phyllotaxy",
       "Phyllotaxy is the pattern of arrangement of leaves on the stem or branch, usually of three types: alternate, "
       "opposite and whorled. In the alternate type, a single leaf arises at each node in an alternate manner, as in "
       "china rose, mustard and sunflower. In the opposite type, a pair of leaves arises at each node opposite each "
       "other (Calotropis, guava). If more than two leaves arise at a node and form a whorl, it is whorled (Alstonia).",
       ["Alternate: one leaf per node", "Opposite: two per node", "Whorled: more than two per node"],
       why="The other options describe opposite and whorled phyllotaxy, or a basal arrangement that is not a type of "
           "phyllotaxy named by NCERT.",
       ncert=ref("MOR", "The Leaf (phyllotaxy)"), secs=20)

statement_pair(T_MOR, "Root, stem and leaf", "Basic",
               "A leaf develops at the node and bears a bud in its axil.",
               "The buds borne by a stem may be terminal or axillary.",
               True, True, "A",
               "Nodes, buds and leaves",
               "The stem bears nodes and internodes; the region where leaves are born is the node. The stem bears "
               "buds, which may be terminal or axillary. A leaf is a lateral, generally flattened structure borne on the "
               "stem; it develops at the node and bears a bud in its axil, which later develops into a branch.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("MOR", "The Stem; The Leaf"), secs=25)

match_list(T_MOR, "Root, stem and leaf", "Basic", "plant", "root modification",
           ["Banyan", "Sugarcane", "Rhizophora", "Sweet potato"],
           ["Swollen adventitious roots that store food", "Stilt roots arising from the lower nodes of the stem",
            "Hanging prop roots from the branches", "Roots that grow vertically upwards to get oxygen for respiration"],
           "III II IV I", ["II III IV I", "III II I IV", "IV II III I"], "D",
           "Modifications of roots",
           "In the banyan tree, hanging structures from the branches (prop roots) support the tree. The supporting roots "
           "coming out of the lower nodes of the stem in maize and sugarcane are stilt roots. In Rhizophora growing in "
           "swampy areas, many roots come out of the ground and grow vertically upwards (pneumatophores) to get oxygen "
           "for respiration. Sweet potato stores food in swollen adventitious roots.",
           ["Banyan → prop roots; sugarcane → stilt roots", "Rhizophora → pneumatophores; sweet potato → storage"],
           why="The wrong codes swap the prop and stilt roots, the respiratory and storage roots, or the banyan and "
               "Rhizophora roots.",
           ncert=ref("MOR", "The Root (modifications of root)"), secs=35)

assertion_reason(T_MOR, "Plant families", "Intermediate",
                 "The seeds of members of the family Solanaceae are endospermous.",
                 "In members of the family Solanaceae, the calyx is persistent.",
                 True, True, False, "B",
                 "Features of Solanaceae",
                 "In the family Solanaceae the seeds are many and endospermous. Separately, the calyx has five united "
                 "sepals, is persistent and shows valvate aestivation. Whether the calyx persists has no bearing on "
                 "whether the seed keeps an endosperm.",
                 ["A: true", "R: true", "The calyx and the seed are unrelated features"],
                 ncert=ref("MOR", "Description of Some Important Families (Solanaceae)"), secs=35)

assertion_reason(T_MOR, "Flower", "Intermediate",
                 "In a perigynous flower such as rose, the ovary is inferior.",
                 "In a perigynous flower, the gynoecium is situated in the centre and the other parts of the flower are "
                 "located on the rim of the thalamus almost at the same level.",
                 False, True, False, "D",
                 "Position of the ovary",
                 "If the gynoecium is situated in the centre and the other parts of the flower are located on the rim of "
                 "the thalamus almost at the same level, the flower is perigynous; the ovary here is said to be half "
                 "inferior (plum, rose, peach). An inferior ovary is found in epigynous flowers such as guava and "
                 "cucumber.",
                 ["A: false; the ovary of a perigynous flower is half inferior", "R: true"],
                 ncert=ref("MOR", "The Flower (position of floral parts on the thalamus)"), secs=40)

direct(T_MOR, "Plant families", "Intermediate",
       "Which pair of plants both bear zygomorphic flowers with a monocarpellary ovary?",
       "Pea and bean",
       ["Mustard and datura", "Canna and pea", "Chilli and bean"], "A",
       "Symmetry and gynoecium of Fabaceae",
       "Pea and bean belong to Fabaceae, whose flowers are bisexual and zygomorphic, with a superior, monocarpellary, "
       "unilocular ovary. NCERT names pea, gulmohur, bean and Cassia as having zygomorphic flowers. Mustard, datura "
       "and chilli have actinomorphic flowers, and canna has an asymmetric flower.",
       ["Zygomorphic: pea, bean, gulmohur, Cassia", "Fabaceae: monocarpellary ovary"],
       why="Mustard, datura and chilli are actinomorphic; canna is asymmetric (irregular).",
       ncert=ref("MOR", "The Flower (symmetry); Fabaceae"), secs=40)

multi_statement(T_MOR, "Plant families", "Intermediate",
                "In which of the following plants are the stamens epipetalous, that is, attached to the petals?",
                [("Brinjal", True), ("Tomato", True), ("Petunia", True), ("Pea", False), ("Lily", False)],
                [("a", "b", "e"), ("a", "d"), ("b", "c", "d", "e")], "C",
                "Epipetalous stamens",
                "Stamens attached to the petals are epipetalous, as in brinjal. In the family Solanaceae (brinjal, "
                "tomato, petunia, potato), the androecium has five epipetalous stamens. In pea (Fabaceae) the ten "
                "stamens are diadelphous, not attached to the petals, and in lily the stamens are attached to the "
                "perianth (epiphyllous).",
                ["Solanaceae → epipetalous: brinjal, tomato, Petunia", "Pea: diadelphous", "Lily: epiphyllous"],
                why="Pea and lily do not have epipetalous stamens, so options with (d) or (e) are wrong; (a) and (d) "
                    "alone also leave out tomato and Petunia.",
                ncert=ref("MOR", "The Flower (androecium); Solanaceae"), secs=45)

match_list(T_MOR, "Flower", "Intermediate", "term", "meaning",
           ["Apocarpous", "Syncarpous", "Epipetalous", "Polyadelphous"],
           ["Stamens attached to the petals", "Carpels fused", "Stamens united into more than two bundles",
            "Carpels free"],
           "IV II I III", ["II IV I III", "IV II III I", "II IV III I"], "B",
           "Terms for the androecium and gynoecium",
           "When more than one carpel is present, they may be free (apocarpous, as in lotus and rose) or fused "
           "(syncarpous, as in mustard and tomato). Stamens attached to the petals are epipetalous (brinjal). Stamens "
           "united into more than two bundles are polyadelphous (citrus).",
           ["Apocarpous = free carpels; syncarpous = fused carpels",
            "Epipetalous = on petals; polyadelphous = more than two bundles"],
           why="The wrong codes swap free and fused carpels, or the epipetalous and polyadelphous conditions.",
           ncert=ref("MOR", "The Flower (androecium, gynoecium)"), secs=35)

direct(T_MOR, "Plant families", "Intermediate",
       "In the semi-technical description of a flowering plant, the description is given in which sequence?",
       "Habit → vegetative characters (roots, stem, leaves) → floral characters (inflorescence, flower parts)",
       ["Floral characters → vegetative characters → habit",
        "Inflorescence → habit → roots, stem and leaves → flower parts",
        "Vegetative characters → habit → floral characters"], "C",
       "Semi-technical description of a plant",
       "A flowering plant is described in simple, scientific language and in a proper sequence. The description begins "
       "with the habit and the vegetative characters (roots, stem and leaves), and then the floral characters "
       "(inflorescence and flower parts). The floral diagram and floral formula are presented after this.",
       ["Habit first", "Then roots, stem, leaves", "Then inflorescence and flower"],
       why="Each wrong sequence moves the habit or the floral characters out of their NCERT position.",
       ncert=ref("MOR", "Semi-technical Description of a Typical Flowering Plant"), secs=30)

multi_statement(T_MOR, "Plant families", "Advanced",
                "A flower has the floral formula ⊕ ⚥ K(5) C(5) A5 G(2), with the stamens joined to the corolla "
                "(epipetalous) and the ovary superior. Which of the following conclusions about it are correct?",
                [("The calyx is gamosepalous.", True),
                 ("The corolla is gamopetalous.", True),
                 ("The stamens are not united with one another, though they are attached to the petals.", True),
                 ("The flower is zygomorphic.", False),
                 ("The gynoecium is bicarpellary and apocarpous.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "D",
                "Reading a floral formula",
                "In a floral formula, ⊕ shows an actinomorphic flower and ⚥ a bisexual one. Fusion is shown by "
                "enclosing the figure in brackets, and adhesion by a line drawn above the symbols of the floral parts. "
                "K(5) means five united sepals and C(5) five united petals. A5 has no bracket, so the five stamens are "
                "free from one another; the line joining C and A shows they are attached to the petals. G(2) means two "
                "fused carpels (syncarpous). This is the floral formula of Solanaceae.",
                ["(a) K(5): true", "(b) C(5): true", "(c) A5 + line to C: true", "(d) ⊕ = actinomorphic: false",
                 "(e) G(2) = syncarpous: false"],
                why="Options with (d) or (e) include a false conclusion; (a) and (c) alone leave out (b).",
                ncert=ref("MOR", "Semi-technical Description (floral formula); Solanaceae"), secs=75)

assertion_reason(T_MOR, "Fruit and seed", "Advanced",
                 "In a mango fruit, the seed lies enclosed within a hard, stony layer.",
                 "Mango is a drupe, a fruit in which the endocarp is stony and hard.",
                 True, True, True, "A",
                 "Pericarp of a drupe",
                 "When the pericarp is thick and fleshy, it is differentiated into the outer epicarp, the middle "
                 "mesocarp and the inner endocarp. In mango, a drupe developing from a monocarpellary superior ovary and "
                 "one-seeded, the pericarp is differentiated into a thin epicarp, a fleshy edible mesocarp and an inner "
                 "stony, hard endocarp. The hard layer around the seed is this endocarp, so R explains A.",
                 ["A: true", "R: true; the stony layer enclosing the seed is the endocarp"],
                 ncert=ref("MOR", "The Fruit"), secs=45)

statement_pair(T_MOR, "Root, stem and leaf", "Advanced",
               "The tendrils of both cucumber and pea help the plant to climb.",
               "The tendrils of both cucumber and pea develop from axillary buds.",
               True, False, "C",
               "Stem tendrils and leaf tendrils",
               "Tendrils that develop from axillary buds are stem tendrils; they are slender and spirally coiled and "
               "help plants to climb, as in gourds (cucumber, pumpkins, watermelon) and grapevines. In pea, leaves are "
               "modified into tendrils for climbing. So both help in climbing, but only the cucumber tendril develops "
               "from an axillary bud.",
               ["Statement I: true", "Statement II: false; the pea tendril is a modified leaf"],
               ncert=ref("MOR", "The Stem (modifications); The Leaf (modifications)"), secs=45)

multi_statement(T_MOR, "Fruit and seed", "Advanced",
                "Which of the following statements correctly compare the seed of bean with the grain of maize?",
                [("Both have cotyledons in the embryo: two in bean and one (the scutellum) in maize.", True),
                 ("The mature bean seed lacks an endosperm, whereas in maize the endosperm is bulky and stores food.",
                  True),
                 ("In both, the seed coat is fused with the fruit wall.", False),
                 ("In both, the plumule is enclosed in a sheath called the coleoptile.", False),
                 ("In both, an aleurone layer separates the endosperm from the embryo.", False)],
                [("a", "b", "c"), ("b", "d"), ("a", "e")], "B",
                "Dicotyledonous and monocotyledonous seeds compared",
                "The embryo of a dicot seed such as bean has an embryonal axis and two cotyledons; bean, gram and pea "
                "seeds have no endosperm at maturity (non-endospermous). In a maize grain, the seed coat is membranous "
                "and fused with the fruit wall; the endosperm is bulky and is separated from the embryo by the "
                "proteinaceous aleurone layer; the embryo has one large, shield-shaped cotyledon, the scutellum, and "
                "its plumule and radicle are enclosed in the coleoptile and coleorhiza.",
                ["(a) true", "(b) true", "(c), (d), (e) are features of maize only"],
                why="Statements (c), (d) and (e) describe cereal (maize) features that the bean seed does not have.",
                ncert=ref("MOR", "The Seed (dicotyledonous and monocotyledonous seeds)"), secs=70)

direct(T_MOR, "Plant families", "Advanced",
       "Which of the following features is common to the flowers of the families Fabaceae, Solanaceae and "
       "Liliaceae?",
       "Bisexual flowers with a superior ovary",
       ["Actinomorphic flowers with axile placentation", "Endospermous seeds",
        "A gamosepalous calyx with valvate aestivation"], "A",
       "Comparing three families",
       "In all three families the flowers are bisexual and the ovary is superior. Fabaceae flowers are zygomorphic "
       "with a monocarpellary, unilocular ovary and non-endospermous seeds, and the calyx shows imbricate "
       "aestivation. Solanaceae and Liliaceae flowers are actinomorphic with axile placentation and endospermous "
       "seeds. Liliaceae has a perianth of tepals rather than a separate calyx.",
       ["Fabaceae, Solanaceae, Liliaceae: all bisexual, ovary superior",
        "Fabaceae differs: zygomorphic, non-endospermous, imbricate calyx"],
       why="Fabaceae is zygomorphic and monocarpellary (no axile placentation), has non-endospermous seeds and an "
           "imbricate calyx; Liliaceae has no distinct calyx.",
       ncert=ref("MOR", "Description of Some Important Families"), secs=60)
