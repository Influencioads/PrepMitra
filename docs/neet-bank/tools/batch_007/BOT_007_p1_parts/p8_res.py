
# =============================================================== 8. Respiration in Plants (4/5/4)
direct(T_RES, "Electron transport system", "Basic",
       "In ATP synthase (complex V), the part that is an integral membrane protein complex forming the channel "
       "through which protons cross the inner mitochondrial membrane is:",
       "F₀",
       ["the F₁ headpiece", "cytochrome c", "ubiquinone"], "C",
       "Parts of ATP synthase",
       "ATP synthase has two major components, F₁ and F₀. The F₁ headpiece is a peripheral membrane protein complex "
       "and contains the site for synthesis of ATP from ADP and inorganic phosphate. F₀ is an integral membrane "
       "protein complex that forms the channel through which protons cross the inner membrane.",
       ["F₀: integral, proton channel", "F₁: peripheral headpiece, site of ATP synthesis"],
       why="The F₁ headpiece contains the ATP-synthesising site, not the channel. Cytochrome c and ubiquinone are "
           "electron carriers, not parts of ATP synthase.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=25)

direct(T_RES, "Glycolysis and fermentation", "Basic",
       "Which of the following processes is common to aerobic respiration, alcoholic fermentation and lactic acid "
       "fermentation?",
       "Glycolysis",
       ["The TCA cycle", "Oxidative decarboxylation of pyruvic acid to acetyl CoA",
        "The electron transport system"], "B",
       "Glycolysis as the common first stage",
       "In all three, glucose is first broken down to pyruvic acid by glycolysis in the cytoplasm. The fate of "
       "pyruvic acid then differs: it is reduced to ethanol and CO₂ or to lactic acid in fermentation, or enters "
       "the mitochondria for the link reaction, the TCA cycle and the ETS in aerobic respiration.",
       ["Glycolysis → common", "Link reaction, TCA cycle, ETS → aerobic respiration only"],
       why="The link reaction, the TCA cycle and the ETS occur only in aerobic respiration.",
       ncert=ref("RES", "Glycolysis; Fermentation; Aerobic Respiration"), secs=25)

assertion_reason(T_RES, "Glycolysis and fermentation", "Basic",
                 "Anaerobic organisms can obtain energy from glucose without using oxygen.",
                 "All living organisms retain the enzymatic machinery to partially oxidise glucose without the help "
                 "of oxygen.",
                 True, True, True, "A",
                 "Respiration without oxygen",
                 "The breakdown of glucose to pyruvic acid (glycolysis) does not need oxygen, and all living organisms "
                 "retain the enzymes for it. In anaerobic organisms glycolysis is the only process of respiration, "
                 "and it releases some energy as ATP. So R explains A.",
                 ["A: true", "R: true; this machinery (glycolysis) is what lets them obtain energy"],
                 ncert=ref("RES", "Glycolysis"), secs=30)

direct(T_RES, "Electron transport system", "Basic",
       "In the electron transport system, electrons from NADH are oxidised by NADH dehydrogenase (complex I) and "
       "transferred to ubiquinone. Ubiquinone is located:",
       "within the inner mitochondrial membrane",
       ["in the outer mitochondrial membrane", "free in the cytoplasm", "in the thylakoid lumen"], "D",
       "Location of ubiquinone",
       "The ETS is present in the inner mitochondrial membrane. Electrons from NADH produced in the matrix are "
       "oxidised by complex I and transferred to ubiquinone located within the inner membrane. Ubiquinone also "
       "receives reducing equivalents from FADH₂ through complex II.",
       ["ETS → inner mitochondrial membrane", "Ubiquinone → within the inner membrane"],
       why="The outer membrane and the cytoplasm do not carry the ETS. The thylakoid lumen belongs to the "
           "chloroplast.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=25)

match_list(T_RES, "Glycolysis and fermentation", "Intermediate", "step of glycolysis", "what happens",
           ["Glucose → glucose-6-phosphate", "Glucose-6-phosphate → fructose-6-phosphate",
            "PGAL → 1,3-bisphosphoglyceric acid (BPGA)", "Phosphoenolpyruvate → pyruvic acid"],
           ["Synthesis of ATP", "Oxidation, with formation of NADH + H⁺", "Isomerisation",
            "Phosphorylation catalysed by hexokinase"],
           "IV III II I", ["IV II III I", "III IV II I", "IV III I II"], "B",
           "Steps of glycolysis",
           "Glucose is phosphorylated to glucose-6-phosphate by hexokinase, which is then isomerised to "
           "fructose-6-phosphate. Later, PGAL is oxidised (two redox equivalents are removed and transferred to NAD⁺, "
           "forming NADH + H⁺) and combined with inorganic phosphate to form BPGA. ATP is synthesised when BPGA forms "
           "PGA and again when PEP is converted to pyruvic acid.",
           ["Glucose → G6P: hexokinase", "G6P → F6P: isomerisation", "PGAL → BPGA: NADH", "PEP → pyruvate: ATP"],
           why="The wrong codes swap isomerisation with oxidation, phosphorylation with isomerisation, or the "
               "NADH-forming step with the ATP-forming step.",
           ncert=ref("RES", "Glycolysis"), secs=45)

assertion_reason(T_RES, "TCA cycle", "Intermediate",
                 "CO₂ is released when pyruvic acid is converted to acetyl CoA.",
                 "The conversion of pyruvic acid to acetyl CoA takes place in the cytoplasm.",
                 True, False, False, "C",
                 "The link reaction",
                 "Pyruvic acid formed in glycolysis enters the mitochondrial matrix, where it undergoes oxidative "
                 "decarboxylation by pyruvic dehydrogenase: pyruvic acid + CoA + NAD⁺ → acetyl CoA + CO₂ + NADH + H⁺. "
                 "So CO₂ is released, but the reaction occurs in the mitochondrial matrix, not the cytoplasm.",
                 ["A: true", "R: false, the reaction is in the mitochondrial matrix"],
                 ncert=ref("RES", "Aerobic Respiration"), secs=35)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "In which of the following conversions is CO₂ released?",
                [("Pyruvic acid → acetyl CoA", True),
                 ("Formation of α-ketoglutaric acid in the TCA cycle", True),
                 ("α-Ketoglutaric acid → succinyl CoA", True),
                 ("Succinyl CoA → succinic acid", False),
                 ("Pyruvic acid → lactic acid", False)],
                ["abcd", "bce", "ac"], "D",
                "Decarboxylation steps",
                "CO₂ is released in the oxidative decarboxylation of pyruvic acid to acetyl CoA, and in the two "
                "successive decarboxylations of the TCA cycle, which form α-ketoglutaric acid and then succinyl CoA. "
                "The conversion of succinyl CoA to succinic acid synthesises GTP, without decarboxylation, and the "
                "reduction of pyruvic acid to lactic acid releases no CO₂.",
                ["(a), (b), (c): decarboxylations", "(d): GTP synthesis", "(e): reduction, no CO₂"],
                why="Each wrong combination includes (d) or (e), or leaves out a decarboxylation.",
                ncert=ref("RES", "Aerobic Respiration; Tricarboxylic Acid Cycle; Fermentation"), secs=45)

statement_pair(T_RES, "Electron transport system", "Intermediate",
               "Cytochrome c acts as a mobile carrier for the transfer of electrons between complex I and complex III.",
               "Ubiquinone receives reducing equivalents from NADH through complex I and from FADH₂ through complex "
               "II.",
               False, True, "D",
               "Carriers of the ETS",
               "Cytochrome c is a small protein attached to the outer surface of the inner membrane; it acts as a "
               "mobile carrier between complex III (cytochrome bc₁ complex) and complex IV (cytochrome c oxidase). "
               "Ubiquinone receives reducing equivalents from NADH via complex I and from FADH₂ via complex II; "
               "reduced ubiquinone (ubiquinol) is then oxidised by complex III.",
               ["Statement I: false, cytochrome c links complex III and complex IV", "Statement II: true"],
               ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=35)

direct(T_RES, "Glycolysis and fermentation", "Intermediate",
       "Which of the following is true of both lactic acid fermentation and alcoholic fermentation?",
       "Both reoxidise the NADH + H⁺ formed in glycolysis to NAD⁺",
       ["Both release CO₂", "Both take place in the mitochondrial matrix",
        "Both release more energy per glucose than aerobic respiration"], "A",
       "Comparing the two fermentations",
       "In both lactic acid and alcoholic fermentation the reducing agent is NADH + H⁺, which is reoxidised to "
       "NAD⁺ as pyruvic acid is reduced. Alcoholic fermentation releases CO₂ (pyruvic acid → CO₂ + ethanol) but "
       "lactic acid fermentation does not. Both occur in the cytoplasm, and both release less than seven per cent "
       "of the energy in glucose.",
       ["Common: NADH → NAD⁺", "CO₂ only in alcoholic fermentation"],
       why="Lactic acid fermentation releases no CO₂. Fermentation is cytoplasmic. It releases far less energy than "
           "aerobic respiration.",
       ncert=ref("RES", "Fermentation"), secs=35)

multi_statement(T_RES, "Electron transport system", "Advanced",
                "The oxygen supply to a respiring plant cell is completely cut off. Which of the following will stop "
                "or decrease?",
                [("The flow of electrons through the electron transport system", True),
                 ("The continued oxidation of acetyl CoA in the TCA cycle", True),
                 ("Glycolysis", False),
                 ("The ATP yield per molecule of glucose", True),
                 ("The conversion of pyruvic acid to ethanol", False)],
                ["abc", "bde", "ade"], "D",
                "Consequences of the absence of oxygen",
                "Oxygen is the final hydrogen acceptor of the ETS, so without it electron flow stops. The TCA cycle "
                "needs continued regeneration of NAD⁺ and FAD⁺ from NADH and FADH₂ in the ETS, so it also stops. "
                "Glycolysis does not need oxygen and continues, with NAD⁺ regenerated by fermentation, so pyruvic "
                "acid is converted to products such as ethanol. Since only glycolysis yields ATP, the ATP yield per "
                "glucose falls.",
                ["(a), (b), (d): stop or decrease", "(c), (e): continue or start"],
                why="Each wrong combination includes glycolysis or ethanol formation, which continue without oxygen, "
                    "or leaves out a step that stops.",
                ncert=ref("RES", "Fermentation; Electron Transport System (ETS) and Oxidative Phosphorylation"),
                secs=60)

assertion_reason(T_RES, "Electron transport system", "Advanced",
                 "Complex IV, cytochrome c oxidase, contains cytochromes a and a₃ and two copper centres.",
                 "The F₁ headpiece of ATP synthase is a peripheral membrane protein complex that contains the site for "
                 "the synthesis of ATP.",
                 True, True, False, "B",
                 "Two components of the inner mitochondrial membrane",
                 "Both statements are true. A describes the composition of complex IV, which passes electrons to "
                 "oxygen. R describes the F₁ part of ATP synthase (complex V). The structure of ATP synthase has "
                 "nothing to do with the cytochromes and copper centres of complex IV, so R does not explain A.",
                 ["A: true", "R: true", "R describes a different complex"],
                 ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=40)

direct(T_RES, "Electron transport system", "Advanced",
       "Which of the following correctly distinguishes oxidative phosphorylation in mitochondria from "
       "photophosphorylation in chloroplasts?",
       "In oxidative phosphorylation the energy of oxidation-reduction is used to create the proton gradient, "
       "whereas in photophosphorylation light energy is used",
       ["In oxidative phosphorylation light energy creates the proton gradient, whereas in photophosphorylation "
        "the energy of oxidation-reduction is used",
        "Only photophosphorylation uses an ATP synthase to make ATP",
        "Only oxidative phosphorylation requires a proton gradient across a membrane"], "C",
       "Oxidative phosphorylation and photophosphorylation",
       "NCERT points out that in photophosphorylation light energy is used to produce the proton gradient needed for "
       "phosphorylation, while in respiration the energy of oxidation-reduction is used for the same purpose; hence "
       "the name oxidative phosphorylation. Both use a proton gradient across a membrane and an ATP synthase.",
       ["Source of energy for the gradient: redox (mitochondria) vs light (chloroplasts)",
        "Both: proton gradient + ATP synthase"],
       why="The second option reverses the two. Both processes use ATP synthase and both need a proton gradient.",
       ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=45)

assertion_reason(T_RES, "ATP yield and amphibolic pathway", "Advanced",
                 "The number of ATP molecules synthesised in the electron transport system depends on the nature of "
                 "the electron donor.",
                 "Oxidation of one molecule of NADH gives rise to 3 molecules of ATP, while that of one molecule of "
                 "FADH₂ produces 2 molecules of ATP.",
                 True, True, True, "A",
                 "ATP yield from different electron donors",
                 "NCERT states that the number of ATP molecules synthesised depends on the nature of the electron "
                 "donor: one NADH gives 3 ATP and one FADH₂ gives 2 ATP. The different yields from the two donors are "
                 "exactly what A states, so R explains A.",
                 ["A: true", "R: true; NADH (3 ATP) and FADH₂ (2 ATP) differ in yield"],
                 ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=40)
