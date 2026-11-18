
# =============================================================== 8. Respiration in Plants (3/4/3)
statement_pair(T_RES, "Glycolysis and fermentation", "Basic",
               "Glycolysis takes place in the matrix of the mitochondria.",
               "In aerobic respiration, NAD⁺ is the final acceptor of electrons in the electron transport system.",
               False, False, "B",
               "Site of glycolysis; final electron acceptor",
               "Glycolysis occurs in the cytoplasm of the cell and is present in all living organisms. In aerobic "
               "respiration, electrons from NADH and FADH₂ pass through the electron transport system and are "
               "finally accepted by oxygen, which is reduced to water; NAD⁺ is the acceptor that is reduced to NADH "
               "in glycolysis and the TCA cycle.",
               ["Statement I: false; glycolysis is in the cytoplasm",
                "Statement II: false; oxygen is the final acceptor"],
               ncert=ref("RES", "Glycolysis; Electron Transport System (ETS) and Oxidative Phosphorylation"),
               secs=25)

direct(T_RES, "ATP yield and amphibolic pathway", "Basic",
       "NCERT suggests that the respiratory pathway is better considered an amphibolic pathway rather than a "
       "catabolic one, because it:",
       "is involved in both anabolism and catabolism",
       ["occurs in both the cytoplasm and the mitochondria", "can run both with and without oxygen",
        "produces both ATP and GTP"], "C",
       "Amphibolic nature of respiration",
       "Substrates such as fatty acids are broken down to acetyl CoA before entering the pathway, and when the "
       "organism needs to synthesise fatty acids, acetyl CoA is withdrawn from it. Because the respiratory pathway "
       "is involved in both anabolism and catabolism, NCERT considers it an amphibolic pathway.",
       ["Breakdown (catabolism) + withdrawal of intermediates for synthesis (anabolism)",
        "-> amphibolic pathway"],
       why="The pathway does occur in two compartments, has anaerobic and aerobic variants and forms ATP and GTP, "
           "but none of these is NCERT's reason for calling it amphibolic.",
       ncert=ref("RES", "Amphibolic Pathway"), secs=25)

assertion_reason(T_RES, "Glycolysis and fermentation", "Basic",
                 "In lactic acid fermentation, CO₂ is removed from pyruvic acid.",
                 "In lactic acid fermentation, pyruvic acid is reduced to lactic acid by lactate dehydrogenase.",
                 False, True, False, "D",
                 "Lactic acid fermentation",
                 "In some bacteria, and in animal muscle when oxygen is inadequate during exercise, pyruvic acid is "
                 "reduced to lactic acid by lactate dehydrogenase, with NADH + H⁺ as the reducing agent. No CO₂ is "
                 "released; CO₂ is released in alcoholic fermentation, where pyruvic acid forms CO₂ and ethanol.",
                 ["A: false - no CO₂ is released in lactic acid fermentation", "R: true"],
                 ncert=ref("RES", "Fermentation"), secs=30)

match_list(T_RES, "ATP yield and amphibolic pathway", "Intermediate", "respiratory substrate",
           "how it enters the respiratory pathway",
           ["Glycerol (from fats)", "Fatty acids", "Amino acids (after deamination)", "Sucrose"],
           ["After being converted to PGAL",
            "As glucose and fructose formed by the enzyme invertase, which enter glycolysis",
            "At some stage within the Krebs cycle, or as pyruvate or acetyl CoA, depending on structure",
            "After being degraded to acetyl CoA"],
           "I IV III II", ["IV I III II", "I IV II III", "III IV I II"], "A",
           "Entry of different substrates into respiration",
           "NCERT: fats are first broken down into glycerol and fatty acids. Glycerol enters the pathway after being "
           "converted to PGAL, and fatty acids are degraded to acetyl CoA before entering. Proteins are degraded by "
           "proteases, and the amino acids (after deamination) enter at some stage within the Krebs cycle or as "
           "pyruvate or acetyl CoA. Sucrose is converted into glucose and fructose by invertase, and these enter "
           "glycolysis.",
           ["Glycerol -> I (PGAL)", "Fatty acids -> IV (acetyl CoA)", "Amino acids -> III",
            "Sucrose -> II (invertase)"],
           why="The wrong codes swap glycerol with fatty acids, amino acids with sucrose, or glycerol with amino "
               "acids.",
           ncert=ref("RES", "Glycolysis; Amphibolic Pathway"), secs=50)

assertion_reason(T_RES, "Glycolysis and fermentation", "Intermediate",
                 "In alcoholic fermentation by yeast, CO₂ is released.",
                 "In alcoholic fermentation, the CO₂ is released by the enzyme alcohol dehydrogenase.",
                 True, False, False, "C",
                 "Enzymes of alcoholic fermentation",
                 "In yeast, under anaerobic conditions, pyruvic acid is converted to CO₂ and ethanol by two enzymes: "
                 "pyruvic acid decarboxylase, which removes CO₂ from pyruvic acid, and alcohol dehydrogenase, which "
                 "forms ethanol using NADH + H⁺ as the reducing agent. Alcohol dehydrogenase does not release CO₂.",
                 ["A: true", "R: false - the decarboxylase, not alcohol dehydrogenase, removes CO₂"],
                 ncert=ref("RES", "Fermentation"), secs=35)

multi_statement(T_RES, "TCA cycle", "Intermediate",
                "In which of the following steps of aerobic respiration is ATP (or GTP) formed directly, without the "
                "electron transport system?",
                [("Glucose -> glucose-6-phosphate", False),
                 ("1,3-Bisphosphoglyceric acid (BPGA) -> 3-phosphoglyceric acid (PGA)", True),
                 ("Fructose-6-phosphate -> fructose 1,6-bisphosphate", False),
                 ("Phosphoenolpyruvate (PEP) -> pyruvic acid", True),
                 ("Succinyl CoA -> succinic acid", True)],
                [("b", "d"), ("a", "b", "d"), ("c", "d", "e")], "B",
                "Direct synthesis of ATP and GTP",
                "In glycolysis, ATP is used at two steps (glucose to glucose-6-phosphate, and fructose-6-phosphate to "
                "fructose 1,6-bisphosphate) and formed directly at two steps (BPGA to PGA, and PEP to pyruvic acid). "
                "In the TCA cycle, a molecule of GTP is synthesised when succinyl CoA is converted to succinic acid "
                "(substrate level phosphorylation).",
                ["(a), (c): ATP is used", "(b), (d): ATP formed directly", "(e): GTP formed"],
                why="(b) and (d) only leaves out the GTP step of the TCA cycle. The other combinations include a step "
                    "that uses ATP rather than forming it.",
                ncert=ref("RES", "Glycolysis; Tricarboxylic Acid Cycle"), secs=55)

statement_pair(T_RES, "TCA cycle", "Intermediate",
               "In the TCA cycle, citric acid is isomerised to isocitrate.",
               "In the TCA cycle, α-ketoglutaric acid is formed by the condensation of the acetyl group with "
               "oxaloacetic acid.",
               True, False, "C",
               "Early steps of the TCA cycle",
               "The TCA cycle starts with the condensation of the acetyl group with oxaloacetic acid (OAA) and water "
               "to yield citric acid, catalysed by citrate synthase. Citrate is then isomerised to isocitrate, which "
               "is followed by two successive decarboxylations leading to α-ketoglutaric acid and then succinyl CoA.",
               ["Statement I: true", "Statement II: false; the condensation forms citric acid, and α-ketoglutaric "
                "acid comes later by decarboxylation"],
               ncert=ref("RES", "Tricarboxylic Acid Cycle"), secs=35)

multi_statement(T_RES, "Electron transport system", "Advanced",
                "Which of the following are true of BOTH oxidative phosphorylation in mitochondria and "
                "photophosphorylation in chloroplasts?",
                [("ATP synthase has an integral membrane part forming a proton channel and a headpiece where ATP is "
                  "made.", True),
                 ("The energy used to build the proton gradient comes from light.", False),
                 ("ATP is synthesised as protons move through the channel down their gradient.", True),
                 ("Oxygen is the final acceptor of the electrons.", False),
                 ("Electrons pass along a chain of electron carriers.", True)],
                [("a", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Comparing the two kinds of phosphorylation",
                "Both use a chemiosmotic mechanism: electron transport through a chain of carriers builds a proton "
                "gradient, and ATP synthase (F₀/F₁ in mitochondria, CF₀/CF₁ in chloroplasts) makes ATP as protons "
                "flow through its channel. In oxidative phosphorylation the energy comes from oxidation-reduction "
                "and oxygen is the final electron acceptor; in photophosphorylation the energy comes from light and "
                "the electrons finally reduce NADP⁺.",
                ["(a), (c), (e): common to both", "(b): only photophosphorylation",
                 "(d): only oxidative phosphorylation"],
                why="(a) and (c) only leaves out the electron transport chain. The other combinations include (b) or "
                    "(d), each true of only one process.",
                ncert=ref("RES", "Electron Transport System (ETS) and Oxidative Phosphorylation"), secs=60)

direct(T_RES, "ATP yield and amphibolic pathway", "Advanced",
       "Which compound is formed BOTH by the degradation of fatty acids and by the oxidative decarboxylation of "
       "pyruvic acid, before entering the TCA cycle?",
       "Acetyl CoA",
       ["PGAL", "Oxaloacetic acid", "Citric acid"], "B",
       "Meeting point of fat and carbohydrate breakdown",
       "Pyruvic acid from glycolysis undergoes oxidative decarboxylation by pyruvic dehydrogenase to form acetyl "
       "CoA. Fatty acids are also degraded to acetyl CoA before entering the respiratory pathway. Acetyl CoA then "
       "condenses with OAA to form citric acid in the TCA cycle.",
       ["Pyruvic acid -> acetyl CoA", "Fatty acids -> acetyl CoA", "Common product = acetyl CoA"],
       why="PGAL is the entry point of glycerol, not of fatty acids. OAA and citric acid are TCA-cycle "
           "intermediates, not products of fatty-acid degradation before the cycle.",
       ncert=ref("RES", "Aerobic Respiration; Amphibolic Pathway"), secs=40)

assertion_reason(T_RES, "Electron transport system", "Advanced",
                 "If oxygen is absent, the TCA cycle continues normally, because no step of the cycle itself uses "
                 "oxygen.",
                 "Oxygen acts as the final hydrogen acceptor in the electron transport system.",
                 False, True, False, "D",
                 "Dependence of the TCA cycle on oxygen",
                 "The continued oxidation of acetyl CoA in the TCA cycle requires the continued regeneration of NAD⁺ "
                 "and FAD⁺ from NADH and FADH₂, which are oxidised in the electron transport system. Oxygen is the "
                 "final hydrogen acceptor of that system; NCERT stresses that, though its role is limited to the "
                 "terminal stage, the presence of oxygen is vital, as it drives the whole process. So the cycle "
                 "cannot continue normally without oxygen.",
                 ["A: false - without O₂ the ETS stops, NAD⁺/FAD⁺ are not regenerated and the cycle cannot continue",
                  "R: true"],
                 ncert=ref("RES", "Tricarboxylic Acid Cycle; Electron Transport System"), secs=50)
