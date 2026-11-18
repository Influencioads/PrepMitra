
# =============================================================== 7. Photosynthesis (4/6/4)
direct(T_PS, "Site and pigments", "Basic",
       "A graph showing the ability of chlorophyll a, chlorophyll b and the carotenoids to absorb light of different "
       "wavelengths is called the:",
       "absorption spectrum",
       ["action spectrum", "Z scheme", "light saturation curve"], "D",
       "Absorption and action spectra",
       "NCERT shows two graphs: one showing the absorption spectrum of chlorophyll a, b and the carotenoids (how much "
       "light of each wavelength each pigment absorbs), and another showing the action spectrum of photosynthesis "
       "(the rate of photosynthesis at different wavelengths). Comparing them shows that most photosynthesis takes "
       "place in the blue and red regions, where chlorophyll a absorbs most.",
       ["Absorption of light by pigments vs wavelength = absorption spectrum",
        "Rate of photosynthesis vs wavelength = action spectrum"],
       why="The action spectrum plots the rate of photosynthesis, not absorption. The Z scheme shows electron carriers "
           "on a redox scale. A light saturation curve plots rate against light intensity.",
       ncert=ref("PS", "How many Types of Pigments are Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Since the first product of CO₂ fixation found by Calvin was a 3-carbon acid, scientists at first searched for "
       "a CO₂ acceptor with two carbons. The acceptor they finally discovered was:",
       "a 5-carbon ketose sugar, ribulose bisphosphate (RuBP)",
       ["a 2-carbon compound, as predicted", "a 3-carbon compound, phosphoenol pyruvate (PEP)",
        "a 4-carbon acid, oxaloacetic acid (OAA)"], "C",
       "The primary acceptor of the Calvin cycle",
       "Because the first product was a C3 acid, the scientists reasoned that the primary acceptor would be a "
       "2-carbon molecule, and they spent many years trying to identify it. Surprisingly, the acceptor molecule was a "
       "5-carbon ketose sugar, ribulose bisphosphate (RuBP); CO₂ (1 C) + RuBP (5 C) gives two molecules of 3-PGA.",
       ["Expected: 2-carbon acceptor", "Found: RuBP, a 5-carbon ketose sugar"],
       why="No 2-carbon acceptor was found. PEP is the primary acceptor of the C4 pathway in mesophyll cells, and OAA "
           "is the first product of the C4 pathway.",
       ncert=ref("PS", "The Primary Acceptor of CO₂"), secs=25)

match_list(T_PS, "Light reactions and photophosphorylation", "Basic", "process", "product(s)",
           ["Non-cyclic photophosphorylation", "Cyclic photophosphorylation", "Carboxylation of RuBP by RuBisCO "
            "with CO₂", "Combination of RuBP with O₂"],
           ["Two molecules of 3-PGA", "One molecule of PGA and one of phosphoglycolate", "ATP, NADPH + H⁺ and O₂",
            "ATP only"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D",
           "Products of the reactions of photosynthesis",
           "In non-cyclic photophosphorylation both ATP and NADPH + H⁺ are synthesised, and O₂ is released by the "
           "splitting of water. Cyclic photophosphorylation results in the synthesis of ATP only, not NADPH + H⁺. "
           "RuBisCO carboxylates RuBP with CO₂ to form two molecules of 3-PGA. In photorespiration, RuBP combines with "
           "O₂ to form one molecule of PGA and phosphoglycolate.",
           ["Non-cyclic → ATP, NADPH, O₂", "Cyclic → ATP only", "Carboxylation → 2 PGA",
            "Oxygenation → PGA + phosphoglycolate"],
           why="The wrong codes swap the two kinds of photophosphorylation, or the carboxylation and oxygenation "
               "products.",
           ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation; The Calvin Cycle; Photorespiration"),
           secs=40)

direct(T_PS, "Light reactions and photophosphorylation", "Basic",
       "The splitting of water associated with Photosystem II releases:",
       "protons (H⁺), electrons and O₂",
       ["CO₂ and electrons", "ATP and NADPH", "O₂ and NADPH only"], "B",
       "Splitting of water",
       "Electrons removed from PS II are replaced by electrons available from the splitting of water: "
       "2H₂O → 4H⁺ + O₂ + 4e⁻. The water-splitting complex is associated with PS II. The electrons replace those "
       "lost by PS II, the protons accumulate in the lumen, and oxygen is released as a by-product.",
       ["2H₂O → 4H⁺ + O₂ + 4e⁻"],
       why="CO₂ is not produced by the light reaction. ATP is made by ATP synthase and NADPH by NADP reductase, not "
           "directly by water splitting.",
       ncert=ref("PS", "The Electron Transport (splitting of water)"), secs=20)

numerical(T_PS, "Light reactions and photophosphorylation", "Intermediate",
          "Water is split in the light reaction as 2H₂O → 4H⁺ + O₂ + 4e⁻. The electrons are finally passed to NADP⁺, "
          "each molecule of NADP⁺ accepting two electrons to form NADPH + H⁺. If 6 molecules of water are split, how "
          "many molecules of NADPH can be formed?",
          "6", ["3", "12", "24"], "D", (6 * 4 // 2) // 2 == 6,
          "Electrons from water to NADP⁺",
          "Every 2 molecules of water give 4 electrons, so 6 molecules give 12 electrons (and 3 O₂). Each NADP⁺ needs "
          "two electrons to be reduced to NADPH + H⁺, so 12 electrons reduce 6 NADP⁺. In other words, one NADPH is "
          "formed for every molecule of water split.",
          ["6 H₂O → 12 e⁻ (and 3 O₂)", "12 e⁻ ÷ 2 e⁻ per NADPH = 6 NADPH"],
          why="3 is the number of O₂ molecules; 12 is the number of electrons (or protons); 24 multiplies the "
              "electrons by two instead of dividing.",
          ncert=ref("PS", "The Electron Transport (splitting of water; NADP⁺ reduction)"), secs=60,
          short="One NADPH per water molecule split.")

assertion_reason(T_PS, "Site and pigments", "Intermediate",
                 "Chlorophyll a is the chief pigment associated with photosynthesis.",
                 "On a paper chromatogram of leaf pigments, xanthophylls appear yellow.",
                 True, True, False, "B",
                 "Leaf pigments",
                 "Chlorophyll a (bright or blue-green on a chromatogram) is the chief pigment associated with "
                 "photosynthesis; it forms the reaction centres of both photosystems. Chlorophyll b (yellow-green), "
                 "xanthophylls (yellow) and carotenoids (yellow to yellow-orange) are accessory pigments. The colour of "
                 "xanthophylls on a chromatogram has nothing to do with why chlorophyll a is the chief pigment.",
                 ["A: true", "R: true", "R is about a different pigment's colour"],
                 ncert=ref("PS", "How many Types of Pigments are Involved in Photosynthesis?"), secs=35)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                 "The regeneration of RuBP in the Calvin cycle requires ATP.",
                 "The regeneration of RuBP in the Calvin cycle requires NADPH.",
                 True, False, False, "C",
                 "Energy needs of the stages of the Calvin cycle",
                 "The reduction stage uses 2 molecules of ATP for phosphorylation and 2 of NADPH for reduction per CO₂ "
                 "fixed. The regeneration of the CO₂ acceptor RuBP requires one ATP for phosphorylation to form RuBP; "
                 "it does not use NADPH.",
                 ["A: true (1 ATP per CO₂)", "R: false; NADPH is used only in reduction"],
                 ncert=ref("PS", "The Calvin Cycle (regeneration)"), secs=35)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following take place in the stroma of the chloroplast?",
                [("Carboxylation of RuBP by RuBisCO", True),
                 ("Reduction of PGA to carbohydrate using ATP and NADPH", True),
                 ("Regeneration of RuBP", True),
                 ("Splitting of water", False),
                 ("Diffusion of protons through the CF₀ channel of ATP synthase", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "B",
                "Sites of reactions in the chloroplast",
                "The membrane system (thylakoids) traps light energy and synthesises ATP and NADPH; the enzymatic "
                "reactions that incorporate CO₂ into sugar take place in the stroma. So carboxylation, reduction and "
                "regeneration of the Calvin cycle occur in the stroma. Water is split on the inner (lumen) side of the "
                "thylakoid membrane, and protons pass through the CF₀ channel, which is embedded in the thylakoid "
                "membrane.",
                ["(a), (b), (c): Calvin cycle in stroma", "(d): lumen side of thylakoid membrane",
                 "(e): channel in thylakoid membrane"],
                why="(d) and (e) are thylakoid membrane events; (a) and (c) alone leave out reduction.",
                ncert=ref("PS", "Where does Photosynthesis take place?; The Calvin Cycle; The Chemiosmotic Hypothesis"),
                secs=50)

match_list(T_PS, "Limiting factors", "Intermediate", "factor", "NCERT's statement about it",
           ["Light", "Carbon dioxide", "Temperature", "Water"],
           ["The dark reactions, being enzymatic, are controlled by it",
            "Its stress causes stomata to close and leaves to wilt",
            "Saturation occurs at about 10 per cent of full sunlight",
            "The major limiting factor; present in the atmosphere at 0.03–0.04 per cent"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A",
           "Factors affecting photosynthesis",
           "Light saturation occurs at about 10 per cent of full sunlight, so light is rarely limiting except in shade "
           "or dense forests. Carbon dioxide is the major limiting factor; its atmospheric concentration is very low, "
           "0.03–0.04 per cent. The dark reactions, being enzymatic, are temperature controlled. Water stress causes "
           "the stomata to close, reducing CO₂ availability, and makes leaves wilt.",
           ["Light → 10% saturation", "CO₂ → major limiting factor", "Temperature → enzymatic dark reactions",
            "Water → stomatal closure, wilting"],
           why="The wrong codes swap light and CO₂, temperature and water, or CO₂ and temperature.",
           ncert=ref("PS", "Factors affecting Photosynthesis"), secs=40)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
               "The Calvin cycle operates in C4 plants as well as in C3 plants.",
               "In C4 plants, the Calvin cycle takes place in the mesophyll cells.",
               True, False, "C",
               "Calvin cycle in C3 and C4 plants",
               "The Calvin pathway occurs in all photosynthetic plants, whether they have the C3 or the C4 pathway. In "
               "C4 plants, the mesophyll cells carry out the initial fixation by PEP carboxylase and lack RuBisCO; the "
               "Calvin pathway takes place in the bundle sheath cells, which are rich in RuBisCO.",
               ["Statement I: true", "Statement II: false; it runs in the bundle sheath cells"],
               ncert=ref("PS", "The C4 Pathway"), secs=35)

multi_statement(T_PS, "Photorespiration", "Advanced",
                "In a C3 leaf, the concentration of O₂ around RuBisCO rises greatly relative to that of CO₂. Which of "
                "the following changes are expected?",
                [("A larger share of RuBP combines with O₂.", True),
                 ("More phosphoglycolate is formed.", True),
                 ("More CO₂ is released in a pathway that uses up ATP.", True),
                 ("The synthesis of sugars increases.", False),
                 ("More ATP is generated by photorespiration.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "b")], "C",
                "Applying the conditions for photorespiration",
                "The active site of RuBisCO can bind both CO₂ and O₂, and the relative concentration of O₂ and CO₂ "
                "determines which binds. When O₂ is relatively high, more RuBP is oxygenated, forming one PGA and one "
                "phosphoglycolate. This pathway, photorespiration, releases CO₂ with the utilisation of ATP; there is "
                "neither synthesis of sugars nor of ATP or NADPH.",
                ["(a), (b), (c) follow from more oxygenation", "(d) false: less carboxylation, no sugar from "
                 "photorespiration", "(e) false: photorespiration uses ATP"],
                why="(d) and (e) are false; (a) and (b) alone leave out the release of CO₂.",
                ncert=ref("PS", "Photorespiration"), secs=60)

direct(T_PS, "Chemiosmosis", "Advanced",
       "In an illuminated chloroplast, the CF₀ channel of ATP synthase is blocked so that protons cannot pass through "
       "it, while electron transport continues. What is the immediate result?",
       "ATP synthesis stops, though the proton gradient across the thylakoid membrane can still build up",
       ["ATP synthesis continues, because the proton gradient keeps increasing",
        "Water splitting stops at once, because PS II needs ATP",
        "The proton concentration in the lumen falls, because protons leak to the stroma"], "D",
       "Chemiosmotic synthesis of ATP",
       "Electron transport and water splitting build a proton gradient: protons accumulate in the lumen. ATP synthase "
       "has two parts: CF₀, embedded in the membrane, forms a transmembrane channel for facilitated diffusion of "
       "protons across the membrane, and CF₁ protrudes into the stroma. The breakdown of the gradient by protons moving "
       "through CF₀ provides the energy for a conformational change in CF₁ that synthesises ATP. If CF₀ is blocked, "
       "the gradient cannot be broken down, so ATP is not made even though the gradient may remain or grow.",
       ["Gradient made by electron transport", "ATP needs protons flowing through CF₀ → CF₁",
        "Blocked CF₀ → no ATP"],
       why="A larger gradient is useless without proton flow through CF₀. Water splitting does not need ATP. Protons "
           "cannot flow back through the blocked channel, so the lumen does not lose them this way.",
       ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=60)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "In C4 plants, the first stable product of CO₂ fixation, formed in the mesophyll cells, is 3-PGA.",
                 "In the mesophyll cells of C4 plants, PEP carboxylase fixes CO₂ with phosphoenol pyruvate.",
                 False, True, False, "D",
                 "First product of the C4 pathway",
                 "In C4 plants the primary CO₂ acceptor in the mesophyll cells is the 3-carbon phosphoenol pyruvate "
                 "(PEP), and the fixation is carried out by PEP carboxylase. The first stable product is the 4-carbon "
                 "oxaloacetic acid (OAA), hence the name C4. 3-PGA is formed later, when the CO₂ released in the bundle "
                 "sheath cells is fixed by RuBisCO.",
                 ["A: false; the first product is OAA (C4)", "R: true"],
                 ncert=ref("PS", "The C4 Pathway"), secs=40)

numerical(T_PS, "Calvin cycle and C4 pathway", "Advanced",
          "In a C4 plant, each molecule of atmospheric CO₂ is first fixed by PEP carboxylase in a mesophyll cell, then "
          "released in a bundle sheath cell and fixed again by RuBisCO. Making one molecule of glucose needs six "
          "molecules of CO₂ to enter the Calvin cycle. How many carboxylation reactions in all (by both enzymes "
          "together) are needed for one glucose?",
          "12", ["6", "18", "24"], "A", 6 * 2 == 12,
          "Double carboxylation in C4 plants",
          "In the C4 pathway, CO₂ is fixed by PEPcase into OAA in the mesophyll; the C4 acid is carried to the bundle "
          "sheath, where it is broken down to release CO₂, which RuBisCO fixes again into PGA in the Calvin cycle. "
          "Glucose needs 6 CO₂ through the Calvin cycle, and each of these 6 molecules is fixed twice: 6 × 2 = 12 "
          "carboxylations.",
          ["6 CO₂ per glucose", "Each CO₂ fixed by PEPcase and then by RuBisCO", "6 × 2 = 12"],
          why="6 counts only one enzyme; 18 confuses carboxylations with the ATP used per glucose; 24 counts each "
              "CO₂ four times.",
          ncert=ref("PS", "The C4 Pathway; The Calvin Cycle"), secs=60)
