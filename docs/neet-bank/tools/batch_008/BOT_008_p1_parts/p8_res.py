
# =============================================================== 8. Respiration in Plants (4/4/4)
direct(T_RES, "Glycolysis and fermentation", "Basic",
       "In glycolysis, fructose 1,6-bisphosphate is split into:",
       "dihydroxyacetone phosphate and 3-phosphoglyceraldehyde (PGAL)",
       ["two molecules of pyruvic acid", "glucose-6-phosphate and fructose-6-phosphate",
        "1,3-bisphosphoglyceric acid and phosphoenolpyruvate"], "D",
       "Splitting step of glycolysis",
       "In glycolysis, glucose is phosphorylated to glucose-6-phosphate, which is isomerised to fructose-6-phosphate. "
       "This is phosphorylated again (using ATP) to fructose 1,6-bisphosphate, which is split into dihydroxyacetone "
       "phosphate and 3-phosphoglyceraldehyde (PGAL). PGAL is then oxidised to BPGA, and the pathway goes on to "
       "pyruvic acid.",
       ["Fructose 1,6-bisphosphate (6C) → DHAP (3C) + PGAL (3C)"],
       why="Pyruvic acid is the end product of glycolysis; glucose-6-phosphate and fructose-6-phosphate come before "
           "this step; BPGA and PEP come after it.",
       ncert=ref("RES", "Glycolysis"), secs=20)

statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "During respiration, oxygen is utilised, and carbon dioxide, water and energy are released as products.",
               "The combustion reaction of respiration requires oxygen, but some cells live where oxygen may or may "
               "not be available.",
               True, True, "A",
               "Respiration and the availability of oxygen",
               "NCERT states that during the process of respiration oxygen is utilised, and carbon dioxide, water and "
               "energy are released as products. The combustion reaction requires oxygen, but some cells live where "
               "oxygen may or may not be available; this is why organisms also retain pathways, such as glycolysis "
               "and fermentation, that partially oxidise glucose without oxygen.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("RES", "Introduction; Glycolysis"), secs=30)

match_list(T_RES, "Glycolysis and fermentation", "Basic", "compound", "how it is formed",
           ["Pyruvic acid", "Citric acid", "Lactic acid", "Water"],
           ["When oxygen accepts electrons and hydrogen at the end of the electron transport system",
            "As the end product of glycolysis in the cytoplasm",
            "By reduction of pyruvic acid in muscle when oxygen is inadequate",
            "By condensation of the acetyl group with oxaloacetic acid and water"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "Formation of compounds in respiration",
           "Glycolysis in the cytoplasm ends with pyruvic acid. In the TCA cycle, the acetyl group condenses with "
           "oxaloacetic acid and water to form citric acid (citrate synthase). In animal muscle, when oxygen is "
           "inadequate, pyruvic acid is reduced to lactic acid by lactate dehydrogenase. At the end of the electron "
           "transport system, oxygen acts as the final hydrogen acceptor, and water is formed.",
           ["Pyruvic acid → glycolysis", "Citric acid → condensation in TCA", "Lactic acid → anaerobic muscle",
            "Water → O₂ at end of ETS"],
           why="The wrong codes swap pyruvic and citric acids, lactic acid and water, or pyruvic and lactic acids.",
           ncert=ref("RES", "Glycolysis; Fermentation; Tricarboxylic Acid Cycle; Electron Transport System"), secs=40)

assertion_reason(T_RES, "Glycolysis and fermentation", "Basic",
                 "Fermentation yields far less energy from a molecule of glucose than aerobic respiration does.",
                 "In fermentation, glucose is only partially broken down, whereas in aerobic respiration it is "
                 "completely degraded to CO₂ and H₂O.",
                 True, True, True, "A",
                 "Fermentation and aerobic respiration",
                 "Fermentation accounts for only a partial breakdown of glucose, and less than seven per cent of the "
                 "energy in glucose is released (not all of it trapped as ATP). In aerobic respiration glucose is "
                 "completely degraded to CO₂ and H₂O, releasing much more energy. The low yield of fermentation follows "
                 "directly from the incomplete breakdown.",
                 ["A: true", "R: true; partial breakdown is why little energy is released"],
                 ncert=ref("RES", "Fermentation"), secs=35)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "Glycolysis is present in all living organisms.",
                 "In glycolysis, ATP is used when fructose-6-phosphate is converted to fructose 1,6-bisphosphate.",
                 True, True, False, "B",
                 "Universality of glycolysis",
                 "Glycolysis is the partial oxidation of glucose to pyruvic acid; it is present in all living organisms "
                 "and is the only process of respiration in anaerobic organisms, reflecting that the first cells lived "
                 "in an atmosphere without oxygen. Separately, one of its steps uses ATP to phosphorylate "
                 "fructose-6-phosphate. That ATP-using step does not explain why the pathway is universal.",
                 ["A: true", "R: true", "R is a detail of one step, unrelated to A"],
                 ncert=ref("RES", "Glycolysis"), secs=35)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "In which of the following conversions is NAD⁺ reduced to NADH + H⁺?",
                [("PGAL → 1,3-bisphosphoglyceric acid (BPGA)", True),
                 ("Pyruvic acid → acetyl CoA", True),
                 ("Succinyl CoA → succinic acid", False),
                 ("Pyruvic acid → lactic acid", False),
                 ("Pyruvic acid → CO₂ and ethanol", False)],
                [("a", "b", "c"), ("b", "d"), ("a", "d", "e")], "D",
                "Steps that form NADH",
                "In glycolysis, PGAL is oxidised to BPGA, and two redox equivalents are removed and transferred to NAD⁺, "
                "forming NADH + H⁺. The oxidative decarboxylation of pyruvic acid to acetyl CoA by pyruvic "
                "dehydrogenase also produces NADH + H⁺. The conversion of succinyl CoA to succinic acid gives GTP. In "
                "both kinds of fermentation, NADH + H⁺ is reoxidised to NAD⁺, not formed.",
                ["(a), (b): NADH formed", "(c): GTP formed", "(d), (e): NADH used up"],
                why="Options with (c), (d) or (e) include steps that make GTP or consume NADH.",
                ncert=ref("RES", "Glycolysis; Aerobic Respiration; Fermentation"), secs=50)

direct(T_RES, "Electron transport system", "Intermediate",
       "Which of the following steps of aerobic respiration takes place in the inner mitochondrial membrane?",
       "Oxidation of NADH by NADH dehydrogenase (complex I)",
       ["Oxidative decarboxylation of pyruvic acid to acetyl CoA",
        "Condensation of acetyl CoA with oxaloacetic acid to form citric acid",
        "Isomerisation of glucose-6-phosphate to fructose-6-phosphate"], "C",
       "Sites of the steps of respiration",
       "Glycolysis takes place in the cytoplasm. The oxidative decarboxylation of pyruvic acid and the TCA cycle "
       "take place in the matrix of the mitochondria. The electron transport system, including NADH dehydrogenase "
       "(complex I), is present in the inner mitochondrial membrane, where electrons are passed to O₂ and ATP is "
       "synthesised.",
       ["Cytoplasm: glycolysis", "Matrix: link reaction, TCA cycle", "Inner membrane: ETS and ATP synthase"],
       why="Pyruvate decarboxylation and citrate formation are matrix reactions; the isomerisation is a glycolytic "
           "step in the cytoplasm.",
       ncert=ref("RES", "Aerobic Respiration; Electron Transport System"), secs=35)

statement_pair(T_RES, "ATP yield and amphibolic pathway", "Intermediate",
               "In the aerobic respiration of one molecule of glucose, two molecules of GTP (equivalent to ATP) are "
               "formed by substrate-level phosphorylation in the TCA cycle.",
               "In glycolysis, ATP is synthesised directly at two steps: the conversion of BPGA to PGA and the "
               "conversion of PEP to pyruvic acid.",
               True, True, "A",
               "ATP formed without the ETS",
               "In the TCA cycle, the conversion of succinyl CoA to succinic acid is accompanied by the synthesis of one "
               "GTP (a substrate-level phosphorylation; GTP can give ATP in a coupled reaction). One glucose gives two "
               "pyruvic acids and so two acetyl CoA, i.e. two turns of the cycle and two GTP. In glycolysis, ATP is "
               "formed when BPGA is converted to PGA and when PEP is converted to pyruvic acid.",
               ["Statement I: one GTP per turn × 2 turns = 2: true", "Statement II: true"],
               ncert=ref("RES", "Glycolysis; Tricarboxylic Acid Cycle"), secs=45)

numerical(T_RES, "Electron transport system", "Advanced",
          "Complete aerobic oxidation of one molecule of glucose produces 10 NADH + H⁺ and 2 FADH₂. Each of these "
          "passes two electrons into the electron transport system, and four electrons are needed to reduce one "
          "molecule of O₂ to two molecules of water. How many molecules of O₂ are needed to accept all these "
          "electrons?",
          "6", ["12", "3", "5"], "C", (10 + 2) * 2 // 4 == 6,
          "Oxygen as the final hydrogen acceptor",
          "The reducing equivalents formed in glycolysis, the link reaction and the TCA cycle are oxidised in the "
          "electron transport system, with oxygen as the final hydrogen acceptor, forming water. 12 carriers × 2 "
          "electrons = 24 electrons; 24 ÷ 4 = 6 O₂. This matches the 6 O₂ in the overall equation "
          "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O.",
          ["10 NADH + 2 FADH₂ = 12 carriers", "12 × 2 e⁻ = 24 e⁻", "24 ÷ 4 = 6 O₂"],
          why="12 counts one O₂ per carrier; 3 divides by 8; 5 counts only the NADH (10 × 2 ÷ 4) and leaves out "
              "FADH₂.",
          ncert=ref("RES", "Electron Transport System and Oxidative Phosphorylation"), secs=70,
          short="One O₂ per two carriers: 12/2 = 6.")

multi_statement(T_RES, "Glycolysis and fermentation", "Advanced",
                "In a yeast cell, the electron transport system stops working completely. Which of the following can "
                "still continue?",
                [("Glycolysis", True),
                 ("Conversion of pyruvic acid to CO₂ and ethanol", True),
                 ("The TCA cycle", False),
                 ("Oxidative phosphorylation", False),
                 ("Reoxidation of the NADH of glycolysis to NAD⁺ by alcohol dehydrogenase", True)],
                [("a", "c", "e"), ("a", "b", "d"), ("b", "e")], "B",
                "Fermentation when the ETS stops",
                "Yeast can obtain energy anaerobically. Glycolysis continues in the cytoplasm, and pyruvic acid is "
                "converted to CO₂ and ethanol by pyruvic acid decarboxylase and alcohol dehydrogenase, which reoxidises "
                "NADH + H⁺ to NAD⁺ and so lets glycolysis go on. The TCA cycle needs continued regeneration of NAD⁺ and "
                "FAD⁺ by the ETS, and oxidative phosphorylation depends on the ETS, so both stop.",
                ["(a), (b), (e): fermentation continues", "(c): needs NAD⁺/FAD⁺ from the ETS", "(d): needs the ETS"],
                why="(c) and (d) cannot continue without the ETS; (b) and (e) alone leave out glycolysis.",
                ncert=ref("RES", "Fermentation; Tricarboxylic Acid Cycle; Electron Transport System"), secs=60)

assertion_reason(T_RES, "Glycolysis and fermentation", "Advanced",
                 "CO₂ is released in lactic acid fermentation.",
                 "In alcoholic fermentation, pyruvic acid decarboxylase removes CO₂ from pyruvic acid.",
                 False, True, False, "D",
                 "Two kinds of fermentation",
                 "In alcoholic fermentation (yeast), pyruvic acid is converted to CO₂ and ethanol by pyruvic acid "
                 "decarboxylase and alcohol dehydrogenase. In lactic acid fermentation (some bacteria; animal muscle "
                 "when oxygen is inadequate), pyruvic acid is reduced to lactic acid by lactate dehydrogenase, and no "
                 "CO₂ is released.",
                 ["A: false; pyruvic acid → lactic acid releases no CO₂", "R: true"],
                 ncert=ref("RES", "Fermentation"), secs=40)

direct(T_RES, "Electron transport system", "Advanced",
       "Which of the following gives the correct path of electrons from NADH to oxygen in the mitochondrial electron "
       "transport system?",
       "NADH → complex I → ubiquinone → complex III → cytochrome c → complex IV → O₂",
       ["NADH → complex I → cytochrome c → complex III → ubiquinone → complex IV → O₂",
        "NADH → complex II → ubiquinone → complex IV → cytochrome c → complex III → O₂",
        "NADH → ubiquinone → complex I → complex III → complex IV → cytochrome c → O₂"], "D",
       "Sequence of the electron transport system",
       "Electrons from NADH are oxidised by NADH dehydrogenase (complex I) and transferred to ubiquinone in the inner "
       "membrane. Reduced ubiquinone (ubiquinol) is oxidised with transfer of electrons to cytochrome c via the "
       "cytochrome bc₁ complex (complex III). Cytochrome c, a small mobile protein on the outer surface of the inner "
       "membrane, carries electrons between complex III and complex IV (cytochrome c oxidase), which passes them to "
       "oxygen. FADH₂ enters through complex II to ubiquinone.",
       ["NADH → I → UQ → III → cyt c → IV → O₂"],
       why="Ubiquinone lies between complexes I and III, and cytochrome c between III and IV; complex II receives "
           "FADH₂, not NADH.",
       ncert=ref("RES", "Electron Transport System and Oxidative Phosphorylation"), secs=50)
