
# =============================================================== 7. Photosynthesis (5/7/5)
direct(T_PS, "Limiting factors", "Basic",
       "The plant (internal) factors affecting photosynthesis include the number, size, age and orientation of leaves "
       "and the amount of chlorophyll. According to NCERT, these internal factors depend on:",
       "the genetic predisposition and the growth of the plant",
       ["the concentration of CO2 in the atmosphere", "the temperature of the surroundings",
        "the availability of sunlight alone"], "B",
       "Internal factors of photosynthesis",
       "The plant factors include the number, size, age and orientation of leaves, mesophyll cells and chloroplasts, "
       "internal CO2 concentration and the amount of chlorophyll. These plant or internal factors are dependent on the "
       "genetic predisposition and the growth of the plant. Sunlight, temperature, CO2 concentration and water are "
       "external factors.",
       ["Internal factors depend on genetic predisposition and growth of the plant"],
       why="Atmospheric CO2, temperature and sunlight are the external factors themselves; they do not determine the "
           "plant's internal factors.",
       ncert=ref("PS", "Factors affecting Photosynthesis"), secs=25)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Plants in which the first product of CO2 fixation is a C4 acid, oxaloacetic acid (OAA), are said to follow "
       "the:",
       "C4 pathway",
       ["C3 pathway", "photorespiratory pathway", "cyclic photophosphorylation pathway"], "D",
       "C3 and C4 pathways",
       "Work on CO2 fixation showed two main groups of plants: those in which the first product of CO2 fixation is a "
       "C3 acid (PGA), following the C3 pathway, and those in which the first product is a C4 acid (OAA), following "
       "the C4 pathway.",
       ["First product PGA (C3 acid) -> C3 pathway", "First product OAA (C4 acid) -> C4 pathway"],
       why="In the C3 pathway the first product is 3-PGA. Photorespiration forms PGA and phosphoglycolate, and cyclic "
           "photophosphorylation is a light reaction that makes ATP; neither forms OAA.",
       ncert=ref("PS", "Where are the ATP and NADPH used? (the primary acceptor of CO2)"), secs=20)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Basic",
               "The Calvin pathway occurs in all photosynthetic plants, whether they have the C3 or the C4 pathway.",
               "Plants with the C4 pathway are adapted to cold, temperate regions.",
               True, False, "C",
               "Calvin cycle and C4 plants",
               "The Calvin pathway occurs in all photosynthetic plants; it does not matter whether they have C3 or C4 "
               "(or any other) pathways. Plants that are adapted to dry tropical regions have the C4 pathway; though "
               "their first CO2 fixation product is the C4 acid OAA, they use the Calvin cycle as the main "
               "biosynthetic pathway.",
               ["Statement I: true", "Statement II: false; C4 plants are adapted to dry tropical regions"],
               ncert=ref("PS", "The Calvin Cycle; The C4 Pathway"), secs=25)

match_list(T_PS, "Site and pigments", "Basic", "description", "term",
           ["Graph of the rate of photosynthesis at different wavelengths of light",
            "Graph of the light absorbed by a pigment at different wavelengths",
            "All the pigments of a photosystem except one molecule of chlorophyll a",
            "Synthesis of ATP from ADP and inorganic phosphate in the presence of light"],
           ["Photophosphorylation", "Antennae (light-harvesting system)", "Action spectrum", "Absorption spectrum"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "A",
           "Terms of the light reaction",
           "An action spectrum shows the rate of photosynthesis at different wavelengths; an absorption spectrum shows "
           "the ability of pigments to absorb light of different wavelengths. In each photosystem all the pigments "
           "except one molecule of chlorophyll a form a light-harvesting system called the antennae. The synthesis of "
           "ATP from ADP and inorganic phosphate in the presence of light is photophosphorylation.",
           ["Rate vs wavelength -> action spectrum", "Absorption vs wavelength -> absorption spectrum",
            "Light-harvesting pigments -> antennae", "Light-driven ATP synthesis -> photophosphorylation"],
           why="The wrong codes swap the two spectra, the antennae and photophosphorylation, or the absorption spectrum "
               "and antennae.",
           ncert=ref("PS", "How many Pigments are involved in Photosynthesis?; What is Light Reaction?"), secs=35)

multi_statement(T_PS, "Limiting factors", "Basic",
                "Which of the following are external factors affecting photosynthesis?",
                [("Availability of sunlight", True), ("Temperature", True), ("CO2 concentration", True),
                 ("Water", True), ("Amount of chlorophyll", False)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("b", "c", "d", "e")], "B",
                "External factors",
                "Photosynthesis is affected by both internal (plant) and external factors. The external factors include "
                "the availability of sunlight, temperature, CO2 concentration and water. The amount of chlorophyll is "
                "an internal (plant) factor.",
                ["(a)-(d): external", "(e): internal"],
                ncert=ref("PS", "Factors affecting Photosynthesis"), secs=30)

assertion_reason(T_PS, "Chemiosmosis", "Intermediate",
                 "During the light reaction, the pH in the lumen of the thylakoid decreases.",
                 "Protons accumulate in the lumen, both from the splitting of water and from the H carrier that "
                 "releases into the lumen the protons it removed from the stroma.",
                 True, True, True, "A",
                 "Proton gradient in the chloroplast",
                 "The splitting of water occurs on the inner side of the thylakoid membrane, so its protons accumulate in "
                 "the lumen. The primary acceptor passes electrons to an H carrier, which removes a proton from the "
                 "stroma and releases it into the lumen. NADP reductase on the stroma side also removes protons from the "
                 "stroma. These create a proton gradient across the thylakoid membrane and a measurable decrease in pH "
                 "in the lumen.",
                 ["A: true", "R: true", "More protons in the lumen means a lower pH there; R explains A"],
                 ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=45)

direct(T_PS, "Chemiosmosis", "Intermediate",
       "NCERT lists the requirements of chemiosmosis. Which of the following is NOT one of them?",
       "RuBisCO",
       ["A membrane", "A proton pump", "A proton gradient"], "B",
       "Requirements of chemiosmosis",
       "Chemiosmosis requires a membrane, a proton pump, a proton gradient and ATPase (ATP synthase). RuBisCO is the "
       "Calvin cycle enzyme of the stroma that combines RuBP with CO2; it has no role in making ATP.",
       ["Chemiosmosis: membrane + proton pump + proton gradient + ATPase"],
       why="A membrane, a proton pump and a proton gradient are all among the four requirements listed in NCERT.",
       ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=30)

_atp_need, _nadph_need, _atp_noncyclic = 6 * 3, 6 * 2, 12
numerical(T_PS, "Light reactions and photophosphorylation", "Intermediate",
          "The Calvin cycle uses 3 ATP and 2 NADPH for every CO2 fixed. In a chloroplast fixing 6 molecules of CO2, "
          "suppose non-cyclic photophosphorylation supplies exactly the NADPH needed together with 12 ATP. How many "
          "more ATP molecules must come from another route, such as cyclic photophosphorylation, which makes ATP but "
          "no NADPH?",
          "6", ["12", "18", "0"], "A",
          _nadph_need == 12 and _atp_need - _atp_noncyclic == 6,
          "Balancing ATP and NADPH for the Calvin cycle",
          "For 6 CO2 the Calvin cycle needs 6 x 3 = 18 ATP and 6 x 2 = 12 NADPH. Non-cyclic flow here supplies the 12 "
          "NADPH and 12 ATP, so 18 - 12 = 6 ATP are still needed. NCERT notes that the cycle needs 3 ATP but only 2 "
          "NADPH per CO2, and cyclic photophosphorylation (ATP without NADPH) probably meets this difference.",
          ["ATP needed = 6 x 3 = 18; NADPH needed = 6 x 2 = 12", "Supplied: 12 ATP", "Extra ATP = 18 - 12 = 6"],
          why="12 repeats the ATP already supplied; 18 is the total need, ignoring the non-cyclic ATP; 0 assumes ATP and "
              "NADPH are needed in equal numbers.",
          ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation; The Calvin Cycle"), secs=60)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following take place in non-cyclic photophosphorylation but NOT in cyclic "
                "photophosphorylation?",
                [("Splitting of water", True), ("Evolution of O2", True), ("Formation of NADPH + H+", True),
                 ("Synthesis of ATP", False), ("Participation of photosystem I", False)],
                [("a", "b", "c", "d"), ("a", "b"), ("c", "d", "e")], "D",
                "Cyclic and non-cyclic photophosphorylation compared",
                "In non-cyclic photophosphorylation PS II and PS I work in series; the water-splitting complex is "
                "associated with PS II, so water is split and O2 evolved, and the electrons finally reduce NADP+ to "
                "NADPH + H+. In cyclic photophosphorylation only PS I is functional and the electron circulates within "
                "the photosystem, so only ATP is synthesised. ATP synthesis and PS I occur in both.",
                ["(a), (b), (c): only non-cyclic", "(d), (e): both"],
                ncert=ref("PS", "The Electron Transport; Cyclic and Non-cyclic Photo-phosphorylation"), secs=45)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Intermediate",
               "In the Z scheme, the movement of electrons from photosystem II to photosystem I is downhill in terms of "
               "the redox potential scale.",
               "The electrons are used up as they pass through the electron transport chain.",
               True, False, "C",
               "Electron transport",
               "Electrons excited in PS II are picked up by an electron acceptor and passed to an electron transport "
               "system of cytochromes. This movement of electrons is downhill on the redox potential scale. The "
               "electrons are not used up as they pass through the chain but are passed on to the pigments of PS I.",
               ["Statement I: true", "Statement II: false; the electrons are passed on to PS I"],
               ncert=ref("PS", "The Electron Transport"), secs=35)

match_list(T_PS, "Limiting factors", "Intermediate", "observation", "factor limiting photosynthesis",
           ["A plant on a dense forest floor photosynthesises faster when more light reaches it",
            "Tomato yields rise in a greenhouse enriched with CO2",
            "A green leaf with optimal light and CO2 does not photosynthesise at a very low temperature",
            "During drought, the stomata of a plant close and its leaves wilt"],
           ["Water", "Temperature", "Carbon dioxide", "Light"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "B",
           "Identifying the limiting factor",
           "By Blackman's law, the rate of a process affected by several factors is set by the factor nearest to its "
           "minimal value. On a shaded forest floor light limits. C3 crops such as tomatoes respond to higher CO2 with "
           "higher yields. NCERT's example: despite a green leaf and optimal light and CO2, a plant may not "
           "photosynthesise if the temperature is very low. Water stress closes stomata (reducing CO2 availability) "
           "and wilts leaves.",
           ["A -> light", "B -> carbon dioxide", "C -> temperature", "D -> water"],
           why="The wrong codes swap light and CO2, temperature and water, or CO2 and temperature.",
           ncert=ref("PS", "Factors affecting Photosynthesis"), secs=45)

direct(T_PS, "Site and pigments", "Intermediate",
       "When the action spectrum of photosynthesis is compared with the absorption spectrum of chlorophyll a, the two "
       "closely overlap. From this NCERT concludes that:",
       "most photosynthesis takes place in the blue and red regions, though some takes place at other wavelengths of "
       "the visible spectrum",
       ["photosynthesis takes place only in red light", "photosynthesis is highest in the green region of the spectrum",
        "no photosynthesis at all takes place outside the blue and red regions"], "D",
       "Action and absorption spectra",
       "The wavelengths at which chlorophyll a shows maximum absorption (blue and red) also show a higher rate of "
       "photosynthesis, so chlorophyll a is the chief pigment. Taken together, the graphs show that most "
       "photosynthesis takes place in the blue and red regions of the spectrum; some photosynthesis does take place "
       "at the other wavelengths of the visible spectrum.",
       ["Action spectrum overlaps the absorption spectrum of chlorophyll a",
        "Most photosynthesis in blue and red; some at other visible wavelengths"],
       why="Blue light also drives much photosynthesis, so it is not red alone. The green region shows low absorption "
           "and a low rate. NCERT notes that some photosynthesis does occur at other visible wavelengths.",
       ncert=ref("PS", "How many Pigments are involved in Photosynthesis?"), secs=35)

multi_statement(T_PS, "Limiting factors", "Advanced",
                "Which of the following statements about the response of C3 and C4 plants to CO2 concentration are "
                "correct?",
                [("C4 plants show saturation at about 360 µL L⁻¹ of CO2.", True),
                 ("In C3 plants, saturation is seen only beyond 450 µL L⁻¹ of CO2.", True),
                 ("At low light conditions, neither C3 nor C4 plants respond to high CO2 conditions.", True),
                 ("At high light intensities, only C4 plants show an increase in the rate of photosynthesis.", False),
                 ("The current availability of CO2 is limiting to C3 plants.", True)],
                [("a", "b", "c", "d"), ("a", "b", "e"), ("b", "c", "d", "e")], "C",
                "CO2 as a limiting factor",
                "C3 and C4 plants respond differently to CO2. At low light neither responds to high CO2. At high light "
                "intensities both C3 and C4 plants show an increase in the rate of photosynthesis. C4 plants show "
                "saturation at about 360 µL L⁻¹, while C3 plants respond to increased CO2 and saturate only beyond "
                "450 µL L⁻¹. Thus the current availability of CO2 is limiting to C3 plants.",
                ["(a), (b), (c), (e) true", "(d) false; at high light both C3 and C4 plants respond"],
                ncert=ref("PS", "Factors affecting Photosynthesis (carbon dioxide concentration)"), secs=60)

assertion_reason(T_PS, "Chemiosmosis", "Advanced",
                 "ATP is synthesised as protons move from the thylakoid lumen to the stroma through the CF0 channel of "
                 "ATP synthase.",
                 "The breakdown of the proton gradient releases enough energy to cause a conformational change in the "
                 "CF1 particle, which makes the enzyme synthesise ATP.",
                 True, True, True, "A",
                 "Coupling the proton gradient to ATP synthesis",
                 "The proton gradient is broken down by the movement of protons across the membrane to the stroma "
                 "through the transmembrane channel of the CF0 of ATP synthase. This breakdown provides enough energy to "
                 "cause a conformational change in the CF1 particle, which makes the enzyme synthesise several "
                 "molecules of energy-packed ATP.",
                 ["A: true", "R: true", "R gives the mechanism by which proton flow yields ATP"],
                 ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=45)

direct(T_PS, "Light reactions and photophosphorylation", "Advanced",
       "An illuminated chloroplast receives only light of wavelengths beyond 680 nm. Which of the following is "
       "expected?",
       "ATP is formed by cyclic photophosphorylation, but no NADPH + H+ is formed and no O2 is evolved.",
       ["ATP, NADPH + H+ and O2 are all formed by non-cyclic photophosphorylation.",
        "NADPH + H+ is formed, but no ATP.", "No photophosphorylation of any kind takes place."], "B",
       "Light beyond 680 nm",
       "Cyclic photophosphorylation also occurs when only light of wavelengths beyond 680 nm is available for "
       "excitation. In it only PS I is functional and the electron circulates within the photosystem, giving ATP but "
       "no NADPH + H+. The water-splitting complex is associated with PS II, which does not take part, so no O2 is "
       "evolved.",
       ["Light > 680 nm -> cyclic photophosphorylation", "Cyclic: only PS I; ATP only; no water splitting"],
       why="Non-cyclic flow needs PS II working in series with PS I. Cyclic flow makes ATP, not NADPH. "
           "Photophosphorylation does continue, by the cyclic route.",
       ncert=ref("PS", "Cyclic and Non-cyclic Photo-phosphorylation"), secs=50)

statement_pair(T_PS, "Site and pigments", "Advanced",
               "A single chlorophyll a molecule forms the reaction centre of each photosystem, and the reaction centres "
               "of the two photosystems are different.",
               "The antennae (light-harvesting system) of a photosystem contain no chlorophyll a.",
               True, False, "C",
               "Reaction centre and antennae",
               "The pigments are organised into light-harvesting complexes within PS I and PS II. In each photosystem "
               "all the pigments except one molecule of chlorophyll a form the light-harvesting system or antennae. "
               "The single chlorophyll a molecule forms the reaction centre, which differs between the two "
               "photosystems (P700 in PS I, P680 in PS II). Since only one chlorophyll a molecule is left out of the "
               "antennae, the other chlorophyll a molecules are part of it.",
               ["Statement I: true",
                "Statement II: false; all pigments except one chlorophyll a molecule form the antennae"],
               ncert=ref("PS", "What is Light Reaction?"), secs=50)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "In C4 plants, the Calvin cycle in the bundle sheath cells is supplied with CO2 released from a C4 "
                 "acid.",
                 "The bundle sheath cells of C4 plants have many intercellular spaces through which atmospheric CO2 "
                 "reaches RuBisCO directly.",
                 True, False, False, "C",
                 "CO2 supply in the bundle sheath",
                 "In C4 plants, atmospheric CO2 is fixed by PEPcase in the mesophyll cells into OAA, which forms malic or "
                 "aspartic acid that is transported to the bundle sheath cells. There the C4 acid is broken down to "
                 "release CO2, which enters the Calvin cycle. The bundle sheath cells have thick walls impervious to "
                 "gaseous exchange and no intercellular spaces.",
                 ["A: true", "R: false; bundle sheath cells lack intercellular spaces and are impervious to gases"],
                 ncert=ref("PS", "The C4 Pathway"), secs=45)
