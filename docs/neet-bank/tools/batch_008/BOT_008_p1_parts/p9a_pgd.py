
# =============================================================== 9. Plant Growth and Development (4/4/4)
direct(T_PGD, "Growth rate", "Basic",
       "Plant growth can be measured by a variety of parameters. Which of the following is NOT one of the parameters "
       "listed by NCERT?",
       "Colour of the leaves",
       ["Dry weight", "Cell number", "Volume"], "A",
       "Measuring growth",
       "Growth at the cellular level is principally a consequence of an increase in the amount of protoplasm; as this "
       "is difficult to measure directly, a quantity more or less proportional to it is measured. Growth is therefore "
       "measured by parameters such as increase in fresh weight, dry weight, length, area, volume and cell number.",
       ["Parameters: fresh weight, dry weight, length, area, volume, cell number"],
       why="Dry weight, cell number and volume are all listed parameters; colour is not a measure of growth.",
       ncert=ref("PGD", "Growth (plant growth is measurable)"), secs=20)

match_list(T_PGD, "Plant growth regulators", "Basic", "plant growth regulator", "source from which it was first "
           "isolated or identified",
           ["Auxin", "Kinetin", "Zeatin", "Gibberellic acid"],
           ["Corn kernels and coconut milk", "Human urine", "The fungus Gibberella fujikuroi",
            "Autoclaved herring sperm DNA"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "B",
           "Discovery of plant growth regulators",
           "Auxin was first isolated from human urine. Skoog and Miller crystallised the cytokinesis-promoting substance "
           "kinetin, identified as a modified form of adenine in autoclaved herring sperm DNA. Zeatin was later isolated "
           "from corn kernels and coconut milk. Kurosawa showed that bakanae disease of rice was caused by the fungus "
           "Gibberella fujikuroi; its active substance was later identified as gibberellic acid.",
           ["Auxin → human urine", "Kinetin → herring sperm DNA", "Zeatin → corn kernels, coconut milk",
            "Gibberellic acid → Gibberella fujikuroi"],
           why="The wrong codes swap auxin and kinetin, zeatin and gibberellic acid, or kinetin and zeatin.",
           ncert=ref("PGD", "Plant Growth Regulators (discovery; auxins; gibberellins; cytokinins)"), secs=40)

statement_pair(T_PGD, "Plant growth regulators", "Basic",
               "Chemically, kinetin is an adenine derivative.",
               "Chemically, ethylene is a terpene.",
               True, False, "C",
               "Chemical nature of PGRs",
               "PGRs are small, simple molecules of diverse chemical composition: indole compounds (indole-3-acetic "
               "acid, IAA), adenine derivatives (N6-furfurylamino purine, kinetin), derivatives of carotenoids "
               "(abscisic acid, ABA), terpenes (gibberellic acid, GA₃) or gases (ethylene, C₂H₄).",
               ["Statement I: true", "Statement II: false; ethylene is a gas; GA₃ is the terpene"],
               ncert=ref("PGD", "Plant Growth Regulators (characteristics)"), secs=30)

assertion_reason(T_PGD, "Plant growth regulators", "Basic",
                 "Auxins help to initiate rooting in stem cuttings.",
                 "The auxin 2,4-D is widely used to kill dicotyledonous weeds.",
                 True, True, False, "B",
                 "Uses of auxins",
                 "Auxins help to initiate rooting in stem cuttings, an application widely used for plant propagation. "
                 "Separately, auxins are widely used as herbicides: 2,4-D kills dicotyledonous weeds without affecting "
                 "mature monocotyledonous plants. The herbicide use of 2,4-D is a different application and does not "
                 "explain rooting in cuttings.",
                 ["A: true", "R: true", "R is a different use of auxins"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (auxins)"), secs=30)

assertion_reason(T_PGD, "Plant growth regulators", "Intermediate",
                 "Zeatin is a synthetic cytokinin.",
                 "Kinetin does not occur naturally in plants.",
                 False, True, False, "D",
                 "Natural and synthetic cytokinins",
                 "Kinetin, a modified form of adenine, does not occur naturally in plants. The search for natural "
                 "substances with cytokinin-like activity led to the isolation of zeatin from corn kernels and coconut "
                 "milk, so zeatin is a naturally occurring cytokinin. Several naturally occurring cytokinins and some "
                 "synthetic compounds with cell-division-promoting activity have since been identified.",
                 ["A: false; zeatin is natural", "R: true"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (cytokinins)"), secs=35)

direct(T_PGD, "Plant growth regulators", "Intermediate",
       "Which pair of plant growth regulators, in that order, initiates germination in peanut seeds and inhibits "
       "seed germination?",
       "Ethylene and abscisic acid",
       ["Abscisic acid and ethylene", "Cytokinin and auxin", "Auxin and gibberellin"], "C",
       "PGRs and seed germination",
       "Ethylene breaks seed and bud dormancy and initiates germination in peanut seeds and sprouting of potato tubers. "
       "Abscisic acid acts as a general plant growth inhibitor; it inhibits seed germination and plays an important "
       "role in seed development, maturation and dormancy.",
       ["Initiates germination in peanut: ethylene", "Inhibits seed germination: ABA"],
       why="The second option reverses the roles. NCERT does not describe cytokinins, auxins or gibberellins with "
           "these two effects.",
       ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (ethylene, abscisic acid)"), secs=35)

match_list(T_PGD, "Plant growth regulators", "Intermediate", "plant growth regulator", "effect",
           ["Ethylene", "Abscisic acid", "Auxin", "Cytokinin"],
           ["Helps to produce new chloroplasts in leaves", "Promotes horizontal growth of seedlings and swelling "
            "of the axis", "Controls xylem differentiation", "Increases the tolerance of plants to various stresses"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "D",
           "Effects of plant growth regulators",
           "Ethylene influences horizontal growth of seedlings, swelling of the axis and apical hook formation in dicot "
           "seedlings. ABA increases the tolerance of plants to various kinds of stresses and is therefore called the "
           "stress hormone. Auxins control xylem differentiation and help in cell division. Cytokinins help to produce "
           "new leaves, chloroplasts in leaves, lateral shoot growth and adventitious shoot formation.",
           ["Ethylene → horizontal growth, swelling", "ABA → stress tolerance", "Auxin → xylem differentiation",
            "Cytokinin → new chloroplasts"],
           why="The wrong codes swap ethylene and ABA, auxin and cytokinin, or ethylene and auxin.",
           ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=40)

statement_pair(T_PGD, "Germination and growth phases", "Intermediate",
               "In a root, the phase of maturation lies further away from the apex than the phase of elongation.",
               "Cells in the meristematic phase are large, with large vacuoles and thick secondary walls.",
               True, False, "C",
               "Phases of growth",
               "Moving away from the root apex, one meets the meristematic phase, then the phase of elongation and then "
               "the phase of maturation. Cells in the meristematic phase are rich in protoplasm, possess large "
               "conspicuous nuclei, and have thin, primary, cellulosic walls with abundant plasmodesmatal connections. "
               "Increased vacuolation and cell enlargement characterise the phase of elongation.",
               ["Statement I: true", "Statement II: false; meristematic cells are protoplasm-rich and thin-walled"],
               ncert=ref("PGD", "Growth (phases of growth)"), secs=35)

direct(T_PGD, "Plant growth regulators", "Advanced",
       "Skoog observed that callus from internodal segments of tobacco stems proliferated only if, in addition to "
       "auxins, the medium was supplemented with extracts such as yeast extract, coconut milk or DNA. If such callus is "
       "grown on a medium with auxin alone, the expected result and its explanation are:",
       "the callus fails to proliferate, because a cytokinesis-promoting substance (a cytokinin) is missing",
       ["the callus proliferates normally, because auxin alone promotes cell division in callus",
        "the callus proliferates faster, because coconut milk contains an inhibitor",
        "the callus forms roots at once, because auxins initiate rooting in stem cuttings"], "B",
       "Cytokinins and cell division",
       "F. Skoog and co-workers observed that tobacco callus proliferated only if, in addition to auxins, the medium "
       "contained extracts of vascular tissues, yeast extract, coconut milk or DNA. Skoog and Miller later identified "
       "and crystallised the cytokinesis-promoting active substance, kinetin. Cytokinins have specific effects on "
       "cytokinesis; zeatin, a natural cytokinin, was isolated from coconut milk. Without this factor the callus does "
       "not proliferate.",
       ["Auxin alone → no proliferation", "Extracts supply a cytokinin that promotes cytokinesis"],
       why="Skoog's observation is that auxin alone is not enough. Coconut milk supplies a cytokinin, not an inhibitor. "
           "Rooting of stem cuttings is a different auxin effect and is not what Skoog's callus experiment showed.",
       ncert=ref("PGD", "Plant Growth Regulators (discovery of cytokinins)"), secs=60)

assertion_reason(T_PGD, "Plant growth regulators", "Advanced",
                 "Ethylene promotes senescence and abscission of plant organs, especially of leaves and flowers.",
                 "Ethylene is synthesised only by young, actively dividing tissues.",
                 True, False, False, "C",
                 "Ethylene: source and effects",
                 "Ethylene is a simple gaseous PGR. It is synthesised in large amounts by tissues undergoing senescence "
                 "and by ripening fruits. It promotes senescence and abscission of plant organs, especially of leaves "
                 "and flowers, and is highly effective in fruit ripening.",
                 ["A: true", "R: false; senescing tissues and ripening fruits make it in large amounts"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (ethylene)"), secs=40)

statement_pair(T_PGD, "Plant growth regulators", "Advanced",
               "Auxins and cytokinins have opposite effects on apical dominance.",
               "In most situations, abscisic acid acts as an antagonist to gibberellins.",
               True, True, "A",
               "Interactions between PGRs",
               "The growing apical bud inhibits the growth of lateral buds (apical dominance), a phenomenon NCERT "
               "attributes to auxins; cytokinins help to overcome apical dominance. So the two have opposite effects on "
               "it. In most situations, ABA acts as an antagonist to GAs. NCERT notes that the roles of PGRs in an event "
               "can be complementary or antagonistic.",
               ["Statement I: true (auxin causes, cytokinin overcomes)", "Statement II: true"],
               ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=45)

direct(T_PGD, "Germination and growth phases", "Advanced",
       "Seeds given water and a suitable temperature are kept in a sealed container in which all the air has been "
       "replaced by nitrogen. They fail to grow. Which condition for growth described in NCERT best explains this?",
       "Oxygen helps in releasing the metabolic energy essential for growth activities",
       ["Water provides the turgidity needed for extension growth",
        "Every plant has an optimum temperature range for growth",
        "Light and gravity affect certain phases of growth"], "A",
       "Conditions for growth",
       "NCERT lists water, oxygen and nutrients as very essential elements for growth, along with an optimum "
       "temperature and environmental signals such as light and gravity. Oxygen helps in releasing metabolic energy "
       "essential for growth activities. Here water and temperature are adequate, so the missing oxygen explains the "
       "failure.",
       ["Water and temperature supplied", "No oxygen → no release of metabolic energy → no growth"],
       why="Water and a suitable temperature were provided, and light or gravity is not the variable changed in this "
           "set-up.",
       ncert=ref("PGD", "Growth (conditions for growth)"), secs=45)
