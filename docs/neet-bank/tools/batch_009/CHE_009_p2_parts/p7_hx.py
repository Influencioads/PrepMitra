
# ================================================================ Organic Compounds Containing Halogens (2197-2206)
# 2197: geminal dihalides (both X on one carbon) in the list
dihal = {"CH3CHCl2": "gem", "ClCH2CH2Cl": "vic", "CH3CBr2CH3": "gem", "CH3CHBrCH2Br": "vic",
         "ClCH2CH2CH2Cl": "neither"}
v_2197 = str(sum(1 for t in dihal.values() if t == "gem"))
assert v_2197 == "2"
# 2200: 1.09 g C2H5Br -> Br- -> AgBr with 0.1 M AgNO3
n_2200 = F(109, 100) / mm(C=2, H=5, Br=1)
v_2200 = f"{float(n_2200 / F(1, 10) * 1000):.0f} mL"
assert n_2200 == F(1, 100) and v_2200 == "100 mL"
# 2206: C4H9Cl isomers, enantiomers counted separately
c4h9cl = {"1-chlorobutane": 1, "2-chlorobutane": 2, "1-chloro-2-methylpropane": 1, "2-chloro-2-methylpropane": 1}
v_2206 = str(sum(c4h9cl.values()))
assert v_2206 == "5" and len(c4h9cl) == 4

QUESTIONS += [
    N(T_HX, "C-X bond and preparation", "Basic",
      "Dihalogen derivatives with both halogen atoms on the same carbon are called geminal (gem) dihalides. How many of "
      "the following are gem-dihalides?\nCH₃CHCl₂, ClCH₂–CH₂Cl, CH₃CBr₂CH₃, CH₃CHBr–CH₂Br, ClCH₂–CH₂–CH₂Cl",
      ["1", v_2197, "3", "4"], "B", v_2197,
      "Classification of dihalogen compounds",
      "Gem-dihalides (alkylidene halides) have both halogens on one carbon; vicinal dihalides (alkylene dihalides) have "
      "them on adjacent carbons.",
      ["CH₃CHCl₂ (ethylidene chloride): gem", "ClCH₂CH₂Cl (ethylene dichloride): vic", "CH₃CBr₂CH₃: gem",
       "CH₃CHBrCH₂Br: vic", "ClCH₂CH₂CH₂Cl: halogens on C-1 and C-3, neither", "Count = 2"],
      why_others_wrong="Counting the vicinal compounds or the 1,3-dichloride as gem-dihalides gives 3 or 4.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification", seconds=30),

    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "Which of the following has the highest boiling point?",
      ["CH₃CH₂Cl", "CH₃CH₂F", "CH₃CH₂I", "CH₃CH₂Br"], "C",
      "Boiling points of haloalkanes",
      "For the same alkyl group, the boiling point rises with the size and mass of the halogen, because larger, more "
      "polarisable halogen atoms give stronger van der Waals forces: RI > RBr > RCl > RF.",
      ["Same alkyl group, different halogen", "Molar mass and van der Waals forces: I > Br > Cl > F",
       "Highest boiling point: CH₃CH₂I"],
      why_others_wrong="The C–F bond is the most polar, but polarity is not the deciding factor here; the heavier "
                       "halides have the stronger intermolecular forces.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties: boiling points", seconds=25),

    Q(T_HX, "Polyhalogen compounds", "Basic", "match_list",
      *ml("Match the polyhalogen compound in List-I with its use in List-II.",
          ["Dichloromethane", "Iodoform", "Freons", "DDT"],
          ["Refrigeration and air conditioning", "Paint remover", "Insecticide",
           "Antiseptic (formerly), acting through the free iodine it liberates"],
          "II IV I III", ["IV II I III", "II I IV III", "II IV III I"], "B"),
      "Uses of polyhalogen compounds",
      "Dichloromethane is a solvent used as a paint remover and in drug manufacture. Iodoform was used as an "
      "antiseptic because it liberates free iodine. Freons (chlorofluorocarbons) are used in refrigeration, air "
      "conditioning and as aerosol propellants. DDT was the first chlorinated organic insecticide.",
      ["Dichloromethane: paint remover (II)", "Iodoform: antiseptic (IV)", "Freons: refrigeration (I)",
       "DDT: insecticide (III)"],
      why_others_wrong="Swapping dichloromethane and iodoform, or freons and DDT, mismatches a solvent with an "
                       "antiseptic or a refrigerant with an insecticide.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=35),

    N(T_HX, "SN1 and SN2", "Intermediate",
      "1.09 g of bromoethane is boiled with excess aqueous NaOH until it is completely hydrolysed. The solution is "
      "acidified with dilute nitric acid and then titrated with 0.10 M AgNO₃. The volume of AgNO₃ solution needed to "
      "precipitate all the bromide is (C = 12, H = 1, Br = 80):",
      [v_2200, "50 mL", "200 mL", "10 mL"], "A", v_2200,
      "Nucleophilic substitution releases the halide ion",
      "The C–Br bond is covalent, so bromoethane itself gives no precipitate with AgNO₃. Hydrolysis "
      "(C₂H₅Br + OH⁻ → C₂H₅OH + Br⁻) frees bromide ions; nitric acid removes the excess OH⁻, which would otherwise "
      "precipitate silver oxide.",
      ["Molar mass of C₂H₅Br = 109 g mol⁻¹; n = 1.09/109 = 0.010 mol", "n(Br⁻) = 0.010 mol = n(Ag⁺) needed",
       "V = 0.010/0.10 = 0.10 L = 100 mL"],
      why_others_wrong="50 mL and 200 mL use a 1 : 2 or 2 : 1 ratio; 10 mL is a tenfold slip in the conversion to mL.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions", seconds=60),

    Q(T_HX, "SN1 and SN2", "Intermediate", "assertion_reason",
      *ar("Allylic and benzylic halides show high reactivity towards the SN1 reaction.", True,
          "The allylic or benzylic carbocation formed in the slow step is stabilised by resonance.", True,
          explains=True),
      "Reactivity of allylic and benzylic halides in SN1",
      "The rate of an SN1 reaction depends on how easily the carbocation forms. In CH₂=CH–CH₂⁺ and C₆H₅–CH₂⁺ the "
      "positive charge is delocalised over the double bond or the benzene ring, so these carbocations form readily. "
      "R explains A.",
      ["SN1: rate-determining ionisation to a carbocation", "Allyl and benzyl cations: resonance stabilised",
       "→ faster SN1"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the physical properties of haloalkanes are correct?",
          [("Bromo, iodo and polychloro derivatives of hydrocarbons are heavier than water.", True),
           ("The density of haloalkanes increases with the number of carbon atoms, the number of halogen atoms and "
            "the atomic mass of the halogen.", True),
           ("Methyl bromide is a liquid at room temperature.", False),
           ("Haloalkanes dissolve in organic solvents.", True),
           ("Among isomeric haloalkanes, the boiling point increases with branching.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d", "e"]], "C"),
      "Density, state and solubility of haloalkanes",
      "NCERT notes that bromo, iodo and polychloro compounds are denser than water and that density rises with more "
      "carbon atoms, more halogen atoms and heavier halogens. Methyl chloride, methyl bromide, ethyl chloride and some "
      "chlorofluoromethanes are gases at room temperature. Haloalkanes dissolve in organic solvents. Branching lowers "
      "the surface area and hence the boiling point.",
      ["(a) true", "(b) true", "(c) false: CH₃Br is a gas", "(d) true", "(e) false: branching lowers the boiling point"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties", seconds=50),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "statement_pair",
      *sp("In the preparation of iodoarenes by electrophilic substitution, an oxidising agent such as HNO₃ or HIO₄ is "
          "needed, because the reaction is reversible and the HI formed must be oxidised.", True,
          "Fluoroarenes are not prepared by direct electrophilic fluorination, because fluorine is far too reactive.",
          True),
      "Preparation of haloarenes by electrophilic substitution",
      "Chlorination and bromination of arenes with a Lewis acid catalyst work well. Iodination is reversible, so HI is "
      "removed by oxidation. Fluorine reacts too violently for controlled substitution.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloarenes from hydrocarbons", seconds=35),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "Bromoethane is heated with silver nitrite to give X as the main product. X is reduced with tin and hydrochloric "
      "acid to give Y. Y is:",
      ["Ethanol", "Ethanenitrile", "Ethyl nitrite", "Ethanamine"], "D",
      "Ambident nucleophiles and reduction of nitro compounds",
      "Silver nitrite is covalent, so the nitrite ion attacks through nitrogen and gives the nitroalkane (KNO₂, which "
      "is ionic, gives the alkyl nitrite through oxygen). A nitro group is reduced to –NH₂ by a metal and acid.",
      ["C₂H₅Br + AgNO₂ → C₂H₅–NO₂ (nitroethane) + AgBr", "C₂H₅NO₂ + 6[H] (Sn/HCl) → C₂H₅NH₂ + 2H₂O",
       "Y = ethanamine"],
      why_others_wrong="Ethyl nitrite would be the product with KNO₂ and gives no amine on reduction; ethanol and "
                       "ethanenitrile need OH⁻ and CN⁻ respectively.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution; 'Amines', reduction of nitro "
            f"compounds", seconds=50),

    Q(T_HX, "SN1 and SN2", "Advanced", "match_list",
      *ml("Nitro groups ortho and para to the halogen make aryl halides much more reactive towards nucleophiles. Match "
          "the aryl chloride in List-I with the condition needed to convert it into the corresponding phenol (List-II).",
          ["Chlorobenzene", "1-Chloro-4-nitrobenzene", "1-Chloro-2,4-dinitrobenzene", "2,4,6-Trinitrochlorobenzene"],
          ["Warm water, 323 K", "Aqueous NaOH, 443 K, then H⁺", "Aqueous NaOH, 623 K and 300 atm, then H⁺",
           "Aqueous NaOH, 368 K, then H⁺"],
          "III II IV I", ["III IV II I", "I II IV III", "III II I IV"], "C"),
      "Effect of electron-withdrawing groups on haloarenes",
      "An –NO₂ group at the ortho or para position withdraws electron density from the ring and stabilises the "
      "negatively charged intermediate (the charge can reach the nitro group by resonance). The more such groups, the "
      "milder the conditions.",
      ["No NO₂: 623 K, 300 atm (III)", "One p-NO₂: 443 K (II)", "Two (o, p): 368 K (IV)", "Three (o, o, p): warm "
       "water, 323 K (I)"],
      why_others_wrong="Any code that gives a more nitrated compound a harsher condition than a less nitrated one "
                       "reverses the activating effect of the nitro groups.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes: effect of substituents", seconds=50),

    N(T_HX, "SN1 and SN2", "Advanced",
      "Counting the two enantiomers of a chiral compound separately, how many isomers have the molecular formula "
      "C₄H₉Cl?",
      ["4", v_2206, "6", "7"], "B", v_2206,
      "Structural isomers and enantiomers of chlorobutanes",
      "First list the structural isomers, then look for a carbon bonded to four different groups.",
      ["1-Chlorobutane: achiral", "2-Chlorobutane: C-2 has H, Cl, CH₃, C₂H₅ → chiral, two enantiomers",
       "1-Chloro-2-methylpropane: achiral", "2-Chloro-2-methylpropane: achiral", "Total = 1 + 2 + 1 + 1 = 5"],
      why_others_wrong="4 counts structures only; 6 or 7 wrongly treat 1-chloro-2-methylpropane (C-2 has two CH₃) or "
                       "2-chloro-2-methylpropane as chiral.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', optical isomerism", seconds=60),
]
