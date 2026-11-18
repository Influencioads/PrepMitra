
# =============================================================== 7. Photosynthesis (5/6/5)
direct(T_PS, "Site and pigments", "Basic",
       "A graph that shows the rate of photosynthesis at different wavelengths of light is called the:",
       "action spectrum",
       ["absorption spectrum", "Z scheme", "chromatogram"], "C",
       "Action spectrum",
       "A graph of the absorption of light of different wavelengths by a pigment is its absorption spectrum. A graph "
       "of the rate of photosynthesis against wavelength is the action spectrum. NCERT superimposes the two to show "
       "that most photosynthesis takes place in the blue and red regions, where chlorophyll a absorbs most.",
       ["Rate of photosynthesis vs wavelength → action spectrum"],
       why="The absorption spectrum plots light absorbed by a pigment, not the rate of photosynthesis. The Z scheme "
           "shows electron carriers on a redox scale. A chromatogram separates pigments.",
       ncert=ref("PS", "What is our Understanding of the Pigments Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Site and pigments", "Basic",
       "Which of the following leaf pigments is NOT an accessory pigment?",
       "Chlorophyll a",
       ["Chlorophyll b", "Xanthophylls", "Carotenoids"], "D",
       "Chief and accessory pigments",
       "Chlorophyll a is the chief pigment associated with photosynthesis and forms the reaction centre. Chlorophyll "
       "b, xanthophylls and carotenoids are called accessory pigments: they also absorb light and transfer the "
       "energy to chlorophyll a.",
       ["Chief pigment: chlorophyll a", "Accessory: chlorophyll b, xanthophylls, carotenoids"],
       why="Chlorophyll b, xanthophylls and carotenoids are the accessory pigments named by NCERT.",
       ncert=ref("PS", "What is our Understanding of the Pigments Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "In the leaves of a plant, large bundle sheath cells with many chloroplasts, thick walls and no intercellular "
       "spaces form a wreath around the vascular bundles. Which of the following plants shows this anatomy?",
       "Maize",
       ["Tomato", "Bell pepper", "Chlamydomonas"], "A",
       "Kranz anatomy of C4 plants",
       "This is Kranz ('wreath') anatomy, a characteristic of C4 plants such as maize and sorghum. The bundle sheath "
       "cells have a large number of chloroplasts, thick walls impervious to gaseous exchange and no intercellular "
       "spaces. Tomato and bell pepper are named by NCERT as C3 plants grown in CO₂-enriched greenhouses.",
       ["Wreath of bundle sheath cells → Kranz anatomy → C4 plant (maize)"],
       why="Tomato and bell pepper are C3 plants. Chlamydomonas is a unicellular green alga with no leaves or "
           "vascular bundles.",
       ncert=ref("PS", "The C4 Pathway"), secs=25)

statement_pair(T_PS, "Site and pigments", "Basic",
               "In photosynthesis, green plants use light energy to drive the synthesis of organic compounds.",
               "The oxygen released in photosynthesis comes from the splitting of water.",
               True, True, "A",
               "Nature of photosynthesis",
               "Photosynthesis is a physico-chemical process by which green plants use light energy to drive the "
               "synthesis of organic compounds. In the light reaction, water is split into H⁺, [O] and electrons on "
               "the inner side of the thylakoid membrane, and the oxygen evolved comes from this splitting of "
               "water.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PS", "Introduction; The Electron Transport (Splitting of Water)"), secs=25)

direct(T_PS, "Site and pigments", "Basic",
       "The light-harvesting complexes (LHC) of Photosystem I and Photosystem II are located in the:",
       "thylakoid membranes of the chloroplast",
       ["stroma of the chloroplast", "outer membrane of the chloroplast envelope",
        "inner membrane of the mitochondrion"], "B",
       "Location of the photosystems",
       "Within the chloroplast, the membrane system (grana and stroma lamellae) is responsible for trapping light "
       "energy. The pigments are organised into two discrete light-harvesting complexes within PS I and PS II, "
       "located in the thylakoid membranes. The stroma carries out the enzymatic reactions that synthesise sugar.",
       ["Light trapping → membrane system (thylakoids)", "Stroma → enzymatic (sugar-forming) reactions"],
       why="The stroma is the site of the biosynthetic phase. The chloroplast envelope and the mitochondrial "
           "membrane do not contain the photosystems.",
       ncert=ref("PS", "Where does Photosynthesis Take Place?; What is Light Reaction?"), secs=25)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                 "Oxygen is evolved in non-cyclic photophosphorylation but not in cyclic photophosphorylation.",
                 "The water splitting complex is associated with PS II, which does not take part in cyclic "
                 "photophosphorylation.",
                 True, True, True, "A",
                 "Why cyclic photophosphorylation releases no oxygen",
                 "Water is split by the water splitting complex associated with PS II, and this is the source of the "
                 "oxygen evolved. In non-cyclic photophosphorylation PS II and PS I work in series, so water is split "
                 "and O₂ released. In cyclic photophosphorylation only PS I is functional and the electron is "
                 "circulated within it, so no water is split and no O₂ is evolved. R directly explains A.",
                 ["A: true", "R: true; no PS II in the cyclic flow → no water splitting → no O₂"],
                 ncert=ref("PS", "Splitting of Water; Cyclic and Non-cyclic Photo-phosphorylation"), secs=40)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following are listed by NCERT as special features of C4 plants?",
                [("A special type of leaf anatomy", True),
                 ("Tolerance of higher temperatures", True),
                 ("A response to high light intensities", True),
                 ("Lack of photorespiration", True),
                 ("A lower productivity of biomass than C3 plants", False)],
                ["abce", "bcd", "acde"], "B",
                "Features of C4 plants",
                "NCERT states that C4 plants are special: they have a special type of leaf anatomy (Kranz anatomy), "
                "they tolerate higher temperatures, they show a response to high light intensities, they lack a "
                "process called photorespiration, and they have greater productivity of biomass.",
                ["(a)–(d): true", "(e): false, C4 plants have greater productivity of biomass"],
                why="Each wrong combination includes (e) or leaves out one of the true features.",
                ncert=ref("PS", "The C4 Pathway"), secs=45)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                "Which of the following are consumed in the Calvin cycle?",
                [("CO₂", True), ("ATP", True), ("NADPH", True), ("O₂", False), ("Phosphoenol pyruvate (PEP)", False)],
                ["abcd", "bce", "ac"], "C",
                "Inputs of the Calvin cycle",
                "The Calvin cycle fixes CO₂ (carboxylation), uses ATP for phosphorylation and NADPH for reduction "
                "(reduction stage), and uses ATP to regenerate RuBP. O₂ is a product of the light reaction, not an "
                "input of the Calvin cycle, and PEP is the CO₂ acceptor of the C4 pathway in mesophyll cells.",
                ["Inputs: CO₂, ATP, NADPH", "O₂: product of light reaction; PEP: C4 pathway"],
                why="Each wrong combination includes O₂ or PEP, or leaves out one of the inputs.",
                ncert=ref("PS", "The Calvin Cycle"), secs=40)

assertion_reason(T_PS, "Photorespiration", "Intermediate",
                 "Photorespiration results in the synthesis of sugars and ATP.",
                 "In photorespiration, RuBP combines with O₂ to form one molecule of PGA and one of "
                 "phosphoglycolate.",
                 False, True, False, "D",
                 "Photorespiration",
                 "In the photorespiratory pathway, RuBP binds O₂ instead of CO₂ and forms one molecule of PGA and "
                 "phosphoglycolate. There is neither synthesis of sugars nor of ATP and NADPH; rather, CO₂ is released "
                 "with the utilisation of ATP. So A is false and R is true.",
                 ["A: false, no sugar or ATP is synthesised", "R: true"],
                 ncert=ref("PS", "Photorespiration"), secs=35)

match_list(T_PS, "Calvin cycle and C4 pathway", "Intermediate", "quantity in the Calvin cycle", "number",
           ["ATP used for every CO₂ fixed", "NADPH used for every CO₂ fixed",
            "Turns of the cycle needed to make one glucose", "ATP used to make one glucose"],
           ["18", "2", "6", "3"],
           "IV II III I", ["II IV III I", "IV II I III", "III II IV I"], "C",
           "Energy accounting of the Calvin cycle",
           "For every CO₂ molecule entering the Calvin cycle, 3 molecules of ATP and 2 of NADPH are required. Six "
           "turns of the cycle are needed to make one molecule of glucose, so one glucose uses 6 × 3 = 18 ATP and "
           "6 × 2 = 12 NADPH.",
           ["Per CO₂: 3 ATP, 2 NADPH", "Per glucose: 6 turns, 18 ATP (12 NADPH)"],
           why="The wrong codes swap ATP and NADPH per CO₂, swap turns and total ATP, or confuse ATP per CO₂ with "
               "the number of turns.",
           ncert=ref("PS", "The Calvin Cycle"), secs=45)

direct(T_PS, "Light reactions and photophosphorylation", "Intermediate",
       "Which sequence correctly shows the path of electrons in non-cyclic photophosphorylation?",
       "H₂O → PS II → electron transport chain (cytochromes) → PS I → NADP⁺",
       ["H₂O → PS I → electron transport chain → PS II → NADP⁺",
        "NADP⁺ → PS I → electron transport chain → PS II → H₂O",
        "H₂O → PS II → NADP⁺ → PS I → electron transport chain"], "A",
       "The Z scheme",
       "Electrons lost by PS II are replaced by electrons from the splitting of water. Electrons excited in PS II "
       "pass through an electron transport system of cytochromes to PS I, not being used up on the way. Electrons "
       "excited in PS I are passed through another chain to NADP⁺, reducing it to NADPH + H⁺.",
       ["Water → PS II", "PS II → cytochromes → PS I", "PS I → NADP⁺"],
       why="The second option begins at PS I, the third runs backwards, and the fourth places NADP⁺ before PS I.",
       ncert=ref("PS", "The Electron Transport"), secs=40)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                 "The bundle sheath cells of C4 plants have a large number of chloroplasts.",
                 "Within the mesophyll cells, the chloroplasts align themselves along the walls so that they get the "
                 "optimum quantity of incident light.",
                 True, True, False, "B",
                 "Chloroplasts in two kinds of cells",
                 "Both statements are true. A describes the bundle sheath cells of C4 plants (Kranz anatomy). R "
                 "describes how chloroplasts are positioned within mesophyll cells in response to light. The "
                 "positioning of chloroplasts in mesophyll cells says nothing about why bundle sheath cells of C4 "
                 "plants are rich in chloroplasts, so R does not explain A.",
                 ["A: true", "R: true", "R concerns a different cell type and a different feature"],
                 ncert=ref("PS", "Where does Photosynthesis Take Place?; The C4 Pathway"), secs=45)

multi_statement(T_PS, "Calvin cycle and C4 pathway", "Advanced",
                "A plant that has been in bright light is suddenly placed in darkness. Which of the following can "
                "continue for some time before stopping?",
                [("Carboxylation of RuBP by RuBisCO", True),
                 ("Splitting of water", False),
                 ("Photophosphorylation", False),
                 ("Reduction of PGA using NADPH", True),
                 ("Regeneration of RuBP", True)],
                ["abe", "cde", "ad"], "D",
                "Dependence of the biosynthetic phase on light",
                "The biosynthetic (Calvin) reactions do not directly depend on light; they depend on the ATP and "
                "NADPH made in the light reaction. So, immediately after light becomes unavailable, carboxylation, "
                "reduction and regeneration continue for some time, using the ATP and NADPH already formed, and then "
                "stop. Splitting of water and photophosphorylation are parts of the light reaction and stop when "
                "light is withdrawn.",
                ["Calvin cycle steps: continue briefly", "Light reaction steps: stop"],
                why="Each wrong combination includes a light reaction step or leaves out one of the Calvin cycle "
                    "steps.",
                ncert=ref("PS", "Where are the ATP and NADPH Used?"), secs=55)

direct(T_PS, "Limiting factors", "Advanced",
       "A maize plant and a tomato plant are grown side by side on a hot, brightly lit day. Which outcome is "
       "expected, and why?",
       "Maize shows the higher rate of photosynthesis, because C4 plants have a higher temperature optimum, respond "
       "to high light intensities and lack photorespiration",
       ["Tomato shows the higher rate, because C3 plants have a higher temperature optimum than C4 plants",
        "Both show equal rates, because light is never a limiting factor",
        "Maize stops photosynthesis, because high temperature denatures PEP carboxylase in C4 plants"], "D",
       "C3 and C4 plants under heat and strong light",
       "C4 plants respond to higher temperatures and show a higher rate of photosynthesis, while C3 plants have a "
       "much lower temperature optimum. C4 plants also respond to high light intensities and lack photorespiration, "
       "which decreases CO₂ fixation in C3 plants.",
       ["Maize: C4 → higher temperature optimum, no photorespiration", "Tomato: C3 → lower optimum"],
       why="C3 plants have a lower, not higher, temperature optimum. NCERT does not say light is never limiting "
           "(it limits shade plants), and C4 plants are tolerant of high temperatures.",
       ncert=ref("PS", "The C4 Pathway; Factors Affecting Photosynthesis (Temperature)"), secs=50)

statement_pair(T_PS, "Chemiosmosis", "Advanced",
               "The splitting of water and the reduction of NADP⁺ take place on the same side of the thylakoid "
               "membrane.",
               "The protons needed to reduce NADP⁺ to NADPH + H⁺ are removed from the stroma.",
               False, True, "D",
               "Sides of the thylakoid membrane",
               "The splitting of water takes place on the inner (lumen) side of the thylakoid membrane, so its "
               "protons accumulate in the lumen. NADP reductase is located on the stroma side, and the protons "
               "needed to reduce NADP⁺ are removed from the stroma. The two events are on opposite sides, which "
               "helps build the proton gradient.",
               ["Statement I: false, water splitting = lumen side, NADP⁺ reduction = stroma side",
                "Statement II: true"],
               ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=40)

direct(T_PS, "Calvin cycle and C4 pathway", "Advanced",
       "Which sequence correctly traces atmospheric CO₂ through the C4 pathway?",
       "CO₂ + PEP → OAA in mesophyll cells → malic or aspartic acid → transported to bundle sheath cells → CO₂ "
       "released → fixed by RuBisCO into PGA",
       ["CO₂ + RuBP → PGA in mesophyll cells → OAA → transported to bundle sheath cells → PEP",
        "CO₂ + PEP → OAA in bundle sheath cells → malic acid → transported to mesophyll cells → CO₂ fixed by "
        "RuBisCO",
        "CO₂ + PEP → PGA in mesophyll cells → OAA in bundle sheath cells → RuBP"], "C",
       "Path of carbon in the C4 pathway",
       "In the mesophyll cells, PEPcase fixes CO₂ with PEP to form OAA, a C4 acid. OAA is converted to malic or "
       "aspartic acid, which is transported to the bundle sheath cells. There the C4 acid is broken down to release "
       "CO₂ and a 3-carbon molecule; the CO₂ enters the Calvin cycle, where RuBisCO fixes it with RuBP to form PGA.",
       ["Mesophyll: PEP + CO₂ → OAA → malic/aspartic acid", "Bundle sheath: decarboxylation → CO₂ → Calvin cycle"],
       why="The first option uses RuBisCO in the mesophyll, which lacks it. The third places PEPcase in the bundle "
           "sheath and RuBisCO in the mesophyll. The fourth makes PGA the product of PEP carboxylation.",
       ncert=ref("PS", "The C4 Pathway"), secs=50)
