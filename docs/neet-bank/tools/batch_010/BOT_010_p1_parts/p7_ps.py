
# =============================================================== 7. Photosynthesis (4/6/4)
direct(T_PS, "Site and pigments", "Basic",
       "NCERT shows that the colour of a green leaf is due to four different pigments rather than one. The "
       "technique used to separate these leaf pigments is:",
       "paper chromatography",
       ["centrifugation", "gel electrophoresis", "staining with basic dyes"], "C",
       "Separating leaf pigments",
       "A chromatographic separation of the leaf pigments shows that the colour of leaves is due to four pigments: "
       "chlorophyll a (bright or blue green), chlorophyll b (yellow green), xanthophylls (yellow) and carotenoids "
       "(yellow to yellow-orange). NCERT describes this separation by paper chromatography.",
       ["Technique: paper chromatography", "Result: four pigment bands"],
       why="NCERT uses paper chromatography, not centrifugation or electrophoresis, to separate the pigments; "
           "staining with basic dyes is how chromatin was named, not how pigments are separated.",
       ncert=ref("PS", "What is the Photosynthetic Pigment Involved in Photosynthesis?"), secs=20)

direct(T_PS, "Calvin cycle and C4 pathway", "Basic",
       "Phosphoenol pyruvate (PEP), the primary CO₂ acceptor in the mesophyll cells of C4 plants, is a:",
       "3-carbon molecule",
       ["4-carbon molecule", "5-carbon ketose sugar", "6-carbon sugar"], "D",
       "Primary CO₂ acceptor of the C4 pathway",
       "NCERT: in the C4 pathway, the primary CO₂ acceptor is a 3-carbon molecule, phosphoenol pyruvate (PEP), "
       "present in the mesophyll cells; the enzyme is PEP carboxylase. The product is the 4-carbon oxaloacetic acid "
       "(OAA).",
       ["PEP: 3 carbons", "PEP + CO₂ -> OAA (4 carbons)"],
       why="The 4-carbon molecule is OAA, the product. The 5-carbon ketose sugar is RuBP, the acceptor of the "
           "Calvin cycle, and glucose is the 6-carbon sugar.",
       ncert=ref("PS", "The C4 Pathway"), secs=20)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Basic",
               "Photosystem I and Photosystem II are named in the sequence in which they function during the light "
               "reaction.",
               "Each light-harvesting complex (LHC) is made up of hundreds of pigment molecules bound to proteins.",
               False, True, "D",
               "Photosystems and light-harvesting complexes",
               "The pigments are organised into two discrete photochemical light-harvesting complexes within PS I and "
               "PS II. These are named in the sequence of their discovery, not in the sequence in which they "
               "function during the light reaction. Each LHC is made up of hundreds of pigment molecules bound to "
               "proteins.",
               ["Statement I: false; named in order of discovery", "Statement II: true"],
               ncert=ref("PS", "What is Light Reaction?"), secs=25)

assertion_reason(T_PS, "Light reactions and photophosphorylation", "Basic",
                 "Photosynthesis is responsible for the release of oxygen into the atmosphere.",
                 "In the light reaction, water is split, and oxygen is released as one of the products.",
                 True, True, True, "A",
                 "Source of atmospheric oxygen from photosynthesis",
                 "NCERT notes that photosynthesis is important because it is the primary source of all food on earth "
                 "and is responsible for the release of oxygen into the atmosphere. This oxygen comes from the "
                 "splitting of water (2H₂O -> 4H⁺ + O₂ + 4e⁻) associated with PS II in the light reaction.",
                 ["A: true", "R: true", "The O₂ that photosynthesis releases is produced by water splitting -> R "
                  "explains A"],
                 ncert=ref("PS", "Introduction; The Splitting of Water"), secs=30)

match_list(T_PS, "Chemiosmosis", "Intermediate", "component", "location or role",
           ["CF₀ of ATP synthase", "CF₁ of ATP synthase", "NADP reductase", "Water-splitting complex"],
           ["Forms a transmembrane channel for facilitated diffusion of protons",
            "Located on the stroma side of the membrane; the protons it needs are removed from the stroma",
            "Protrudes on the outer surface facing the stroma; its conformational change makes the enzyme "
            "synthesise ATP",
            "Associated with PS II and located on the inner side of the membrane"],
           "I III II IV", ["III I II IV", "I III IV II", "II III I IV"], "B",
           "Parts of the chemiosmotic machinery",
           "ATP synthase has two parts: CF₀, embedded in the thylakoid membrane, forms a transmembrane channel for "
           "facilitated diffusion of protons; CF₁ protrudes on the outer surface facing the stroma, and the energy "
           "of proton movement causes a conformational change in it that makes the enzyme synthesise ATP. NADP "
           "reductase is on the stroma side, and the protons for NADPH + H⁺ are removed from the stroma. The "
           "water-splitting complex is associated with PS II on the inner side of the membrane.",
           ["CF₀ -> I", "CF₁ -> III", "NADP reductase -> II", "Water-splitting complex -> IV"],
           why="The wrong codes swap the two parts of ATP synthase, the NADP reductase with the water-splitting "
               "complex, or CF₀ with NADP reductase.",
           ncert=ref("PS", "The Chemiosmotic Hypothesis"), secs=50)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following are true of BOTH Photosystem I and Photosystem II?",
                [("It is associated with the water-splitting complex.", False),
                 ("Its reaction centre is a single chlorophyll a molecule.", True),
                 ("Its light-harvesting complex has hundreds of pigment molecules bound to proteins.", True),
                 ("It takes part in cyclic photophosphorylation.", False),
                 ("It is located in the thylakoid membranes.", True)],
                [("b", "c"), ("a", "b", "e"), ("c", "d", "e")], "C",
                "Common features of the two photosystems",
                "Each photosystem has a light-harvesting complex of hundreds of pigment molecules bound to proteins, "
                "with a single chlorophyll a molecule as the reaction centre (different in the two photosystems). "
                "The LHCs are located in the thylakoid membranes. Only PS II is associated with water splitting, "
                "and only PS I is functional in cyclic photophosphorylation.",
                ["(a) PS II only: false", "(b) true", "(c) true", "(d) PS I only: false", "(e) true"],
                why="(b) and (c) only leaves out the location in the thylakoid membranes. The other combinations "
                    "include (a) or (d), each true of only one photosystem.",
                ncert=ref("PS", "What is Light Reaction?; Cyclic and Non-cyclic Photo-phosphorylation"), secs=55)

statement_pair(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
               "The reduction steps of the Calvin cycle are catalysed by RuBisCO.",
               "The oxygen evolved during photosynthesis comes from carbon dioxide.",
               False, False, "B",
               "RuBisCO's step; source of O₂",
               "RuBisCO catalyses carboxylation, the fixation of CO₂ with RuBP to form two molecules of 3-PGA. The "
               "reduction steps that follow use ATP for phosphorylation and NADPH for reduction. The O₂ evolved in "
               "photosynthesis comes from the splitting of water, not from CO₂.",
               ["Statement I: false; RuBisCO catalyses carboxylation", "Statement II: false; O₂ comes from water"],
               ncert=ref("PS", "The Calvin Cycle; The Splitting of Water"), secs=35)

direct(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
       "In a C4 plant, which option correctly pairs each carboxylating enzyme with the cells in which it fixes CO₂?",
       "PEP carboxylase in the mesophyll cells; RuBisCO in the bundle sheath cells",
       ["RuBisCO in the mesophyll cells; PEP carboxylase in the bundle sheath cells",
        "Both PEP carboxylase and RuBisCO in the mesophyll cells",
        "Both PEP carboxylase and RuBisCO in the bundle sheath cells"], "A",
       "Division of labour in C4 leaves",
       "In C4 plants the primary CO₂ acceptor PEP is carboxylated by PEP carboxylase in the mesophyll cells, which "
       "lack RuBisCO. The C4 acid is moved to the bundle sheath cells, broken down to release CO₂, and the CO₂ "
       "enters the Calvin cycle there. The bundle sheath cells are rich in RuBisCO but lack PEPcase.",
       ["Mesophyll: PEPcase (no RuBisCO)", "Bundle sheath: RuBisCO (no PEPcase)"],
       why="The first option reverses the two cell types. Each cell type has only one of the two enzymes, so "
           "neither 'both in one cell' option is correct.",
       ncert=ref("PS", "The C4 Pathway"), secs=35)

multi_statement(T_PS, "Light reactions and photophosphorylation", "Intermediate",
                "Which of the following are part of the light reactions (photochemical phase) of photosynthesis?",
                [("Splitting of water", True),
                 ("Carboxylation of RuBP", False),
                 ("Formation of NADPH", True),
                 ("Regeneration of RuBP", False),
                 ("Release of oxygen", True)],
                [("a", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Light reactions versus the biosynthetic phase",
                "The light reactions (photochemical phase) include light absorption, water splitting, oxygen release "
                "and the formation of the high-energy intermediates ATP and NADPH. Carboxylation, reduction and "
                "regeneration of RuBP make up the Calvin cycle of the biosynthetic phase in the stroma.",
                ["(a), (c), (e): light reactions", "(b), (d): Calvin cycle (biosynthetic phase)"],
                why="(a) and (c) only leaves out the release of oxygen. The other combinations include a stage of the "
                    "Calvin cycle.",
                ncert=ref("PS", "What is Light Reaction?; Where are the ATP and NADPH used?"), secs=45)

assertion_reason(T_PS, "Calvin cycle and C4 pathway", "Intermediate",
                 "In a C4 plant, the CO₂ fixed in the mesophyll cells is ultimately released in the bundle sheath "
                 "cells.",
                 "The C4 acids (malic acid or aspartic acid) formed in the mesophyll cells are transported to the "
                 "bundle sheath cells and broken down there to release CO₂ and a 3-carbon molecule.",
                 True, True, True, "A",
                 "Transport of fixed CO₂ in the C4 pathway",
                 "OAA formed in the mesophyll forms other 4-carbon compounds like malic acid or aspartic acid, which "
                 "are transported to the bundle sheath cells. There these C4 acids are broken down to release CO₂ "
                 "and a 3-carbon molecule; the CO₂ then enters the Calvin cycle. The transport and breakdown of the "
                 "C4 acid is how the CO₂ reaches the bundle sheath.",
                 ["A: true", "R: true", "The C4 acid carries the fixed carbon to the bundle sheath and releases it "
                  "-> R explains A"],
                 ncert=ref("PS", "The C4 Pathway"), secs=40)

match_list(T_PS, "Calvin cycle and C4 pathway", "Advanced", "feature", "plants in which NCERT describes it",
           ["The Calvin cycle as the main biosynthetic pathway",
            "Initial fixation of atmospheric CO₂ by PEP carboxylase",
            "3-PGA as the first stable product of CO₂ fixation",
            "Release of O₂ derived from the splitting of CO₂"],
           ["C3 plants only", "C4 plants only", "Both C3 and C4 plants", "Neither C3 nor C4 plants"],
           "III II I IV", ["II III I IV", "III II IV I", "III I II IV"], "D",
           "Comparing C3 and C4 plants",
           "The Calvin pathway occurs in all photosynthetic plants, whether they have the C3 or the C4 pathway. Only "
           "C4 plants fix atmospheric CO₂ first by PEP carboxylase (first product OAA); in C3 plants the first stable "
           "product is 3-PGA. In no plant is the O₂ released derived from CO₂: it comes from the splitting of water.",
           ["Calvin cycle -> both", "PEPcase as first fixer -> C4 only", "3-PGA first product -> C3 only",
            "O₂ from CO₂ -> neither"],
           why="The wrong codes swap 'both' with 'C4 only', 'C3 only' with 'neither', or 'C3 only' with 'C4 only'.",
           ncert=ref("PS", "The Calvin Cycle; The C4 Pathway; The Splitting of Water"), secs=60)

direct(T_PS, "Calvin cycle and C4 pathway", "Advanced",
       "Which of the following does NOT take place in the bundle sheath cells of a C4 plant such as maize?",
       "Fixation of atmospheric CO₂ with phosphoenol pyruvate",
       ["Breakdown of the C4 acid to release CO₂", "Carboxylation of RuBP by RuBisCO",
        "Reduction of PGA using ATP and NADPH"], "B",
       "Events in the bundle sheath cells",
       "In C4 plants, the bundle sheath cells receive the C4 acid, break it down to release CO₂, and carry out the "
       "Calvin cycle: carboxylation of RuBP by RuBisCO, reduction using ATP and NADPH, and regeneration of RuBP. "
       "The bundle sheath cells lack PEP carboxylase, so the fixation of atmospheric CO₂ with PEP happens only in "
       "the mesophyll cells.",
       ["Bundle sheath: decarboxylation + whole Calvin cycle", "No PEPcase in bundle sheath -> PEP fixation only "
        "in mesophyll"],
       why="Breakdown of the C4 acid, carboxylation of RuBP and reduction of PGA all take place in the bundle "
           "sheath cells.",
       ncert=ref("PS", "The C4 Pathway"), secs=45)

statement_pair(T_PS, "Light reactions and photophosphorylation", "Advanced",
               "In the Z scheme, electrons from PS II pass downhill through the electron transport chain to the "
               "pigments of PS I, and electrons excited in the reaction centre of PS I are finally passed to NADP⁺.",
               "NADP reductase is located on the lumen side of the thylakoid membrane, so the protons used to reduce "
               "NADP⁺ are taken from the lumen.",
               True, False, "C",
               "Electron flow and NADP⁺ reduction",
               "In non-cyclic flow, electrons excited in PS II are passed through the electron transport chain "
               "(downhill on the redox scale) to PS I; electrons excited in PS I are passed through another chain to "
               "NADP⁺, reducing it to NADPH + H⁺. NADP reductase is located on the stroma side of the membrane, and "
               "the protons needed for the reduction are removed from the stroma, which adds to the proton gradient.",
               ["Statement I: true", "Statement II: false; NADP reductase is on the stroma side"],
               ncert=ref("PS", "Electron Transport; The Chemiosmotic Hypothesis"), secs=50)

assertion_reason(T_PS, "Limiting factors", "Advanced",
                 "When the CO₂ concentration rises above about 360 µL L⁻¹, the rate of photosynthesis of C3 plants "
                 "increases.",
                 "C3 plants show saturation of photosynthesis at about 360 µL L⁻¹ of CO₂.",
                 True, False, False, "C",
                 "CO₂ response of C3 and C4 plants",
                 "NCERT: C4 plants show saturation at about 360 µL L⁻¹, while C3 plants respond to increased CO₂ "
                 "concentration and saturation is seen only beyond 450 µL L⁻¹. So raising CO₂ above 360 µL L⁻¹ still "
                 "increases photosynthesis in C3 plants; it is the C4 plants that are saturated at that level.",
                 ["A: true", "R: false - saturation at about 360 µL L⁻¹ is for C4 plants; C3 plants saturate only "
                  "beyond 450 µL L⁻¹"],
                 ncert=ref("PS", "Factors affecting Photosynthesis (carbon dioxide concentration)"), secs=45)
