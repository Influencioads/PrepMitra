
# ================================================================ Some Basic Principles of Organic Chemistry (2166-2182)
# 2167: carbonyl compounds C4H8O: butanal, 2-methylpropanal, butan-2-one
carbonyl_c4h8o = ["CH3CH2CH2CHO", "(CH3)2CHCHO", "CH3COCH2CH3"]
v_2167 = str(len(carbonyl_c4h8o))
assert v_2167 == "3"
# 2171: 2-methylbutane (CH3)2CH-CH2-CH3: H on 1 deg, 2 deg, 3 deg carbons
h1, h2, h3 = 3 + 3 + 3, 2, 1
assert h1 + h2 + h3 == 12                                                                 # C5H12
v_2171 = f"{h1} : {h2} : {h3}"
assert v_2171 == "9 : 2 : 1"
# 2172: acids stronger than ethanoic acid (EWG or H in place of CH3: stronger; extra alkyl: weaker)
stronger = {"HCOOH": True, "ClCH2COOH": True, "CH3CH2COOH": False, "FCH2COOH": True, "Cl2CHCOOH": True,
            "(CH3)3CCOOH": False}
v_2172 = str(sum(stronger.values()))
assert v_2172 == "4"
# 2178: cycloalkanes C5H10 (structural isomers only)
rings = {5: ["cyclopentane"], 4: ["methylcyclobutane"],
         3: ["ethylcyclopropane", "1,1-dimethylcyclopropane", "1,2-dimethylcyclopropane"]}
v_2178 = str(sum(len(v) for v in rings.values()))
assert v_2178 == "5"

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of (CH₃)₂CH–CH₂–C≡N is:",
      ["2-Methylbutanenitrile", "4-Methylbutanenitrile", "1-Cyano-2-methylpropane", "3-Methylbutanenitrile"], "D",
      "Naming nitriles",
      "For a nitrile, the carbon of the –C≡N group is part of the parent chain and is numbered C-1; the suffix is "
      "'-nitrile' added to the name of the alkane.",
      ["Chain including the CN carbon: N≡C1–C2H₂–C3H(CH₃)–C4H₃", "Four carbons → butanenitrile",
       "Methyl on C-3 → 3-methylbutanenitrile"],
      why_others_wrong="2-methyl numbers the chain from the wrong end; 4-methylbutane would make the chain longer; "
                       "'cyano' is used as a prefix only when a higher-priority group is present.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of compounds with "
            f"functional groups", seconds=35),

    N(T_GO, "Isomerism", "Basic",
      "How many structural isomers with the molecular formula C₄H₈O are aldehydes or ketones?",
      ["2", "3", "4", "5"], "B", v_2167,
      "Counting carbonyl isomers",
      "C₄H₈O fits CₙH₂ₙO, the formula of saturated open-chain aldehydes and ketones.",
      ["Aldehydes: butanal, CH₃CH₂CH₂CHO; 2-methylpropanal, (CH₃)₂CHCHO",
       "Ketone: butan-2-one, CH₃COCH₂CH₃ (a ketone needs C=O inside the chain)", "Total = 3"],
      why_others_wrong="2 forgets the branched aldehyde or the ketone; 4 or 5 count 'butan-1-one' or repeat butan-2-one "
                       "numbered from the other end, which is the same compound.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', isomerism", seconds=40),

    Q(T_GO, "Types of organic reactions", "Basic", "statement_pair",
      *sp("Organic reactions that proceed by homolytic fission of bonds are called free radical, homopolar or non-polar "
          "reactions.", True,
          "Organic reactions that proceed by heterolytic fission of bonds are called ionic, heteropolar or polar "
          "reactions.", True),
      "Classifying reactions by the type of bond fission",
      "In homolytic fission each atom keeps one electron of the shared pair and neutral free radicals are formed; the "
      "reactions are called free radical (homopolar, non-polar) reactions. Heterolytic fission gives ions such as "
      "carbocations and carbanions, and these reactions are called ionic (heteropolar, polar) reactions.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fission of a covalent bond",
      seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "match_list",
      *ml("Match the carbon–carbon bond in List-I with its bond length in List-II.",
          ["C–C bond in ethane", "C=C bond in ethene", "C≡C bond in ethyne", "Carbon–carbon bond in benzene"],
          ["139 pm", "154 pm", "120 pm", "134 pm"],
          "II IV III I", ["II I III IV", "IV II III I", "II IV I III"], "C"),
      "Bond length and bond order",
      "The more bonds between two carbon atoms (and the greater the s character of the hybrid orbitals), the shorter "
      "the bond: C–C 154 pm > C=C 134 pm > C≡C 120 pm. All six C–C bonds of benzene have the same length, 139 pm, "
      "between the single and double bond values, because of resonance.",
      ["Ethane C–C: 154 pm (II)", "Ethene C=C: 134 pm (IV)", "Ethyne C≡C: 120 pm (III)", "Benzene: 139 pm (I)"],
      why_others_wrong="Codes that give benzene 134 pm treat it as having isolated double bonds (Kekulé); giving "
                       "ethyne 139 pm ignores that the triple bond is the shortest.",
      ncert=f"{NC11}, 'Hydrocarbons', structure of ethene, ethyne and benzene", seconds=40),

    Q(T_GO, "Types of organic reactions", "Basic", "assertion_reason",
      *ar("The reaction of ethene with bromine to give 1,2-dibromoethane is an addition reaction.", True,
          "Ethene is a planar molecule in which all six atoms lie in the same plane.", True),
      "Addition reactions",
      "Ethene adds Br₂ across its C=C double bond, so the two reactants combine into one product: an addition "
      "reaction, made possible by the π bond. R is a correct statement about the shape of ethene, but the planar shape "
      "is not why the reaction is an addition; R does not explain A.",
      ["CH₂=CH₂ + Br₂ → BrCH₂–CH₂Br: two molecules give one → addition",
       "R: true (sp² carbons, planar) but about geometry, not reaction type"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', types of organic reactions",
      seconds=30),

    N(T_GO, "Hybridisation and functional groups", "Intermediate",
      "In 2-methylbutane, (CH₃)₂CH–CH₂–CH₃, the ratio of the numbers of hydrogen atoms attached to primary, "
      "secondary and tertiary carbon atoms is:",
      ["6 : 2 : 1", "9 : 1 : 2", "3 : 2 : 1", v_2171], "D", v_2171,
      "Primary, secondary and tertiary hydrogens",
      "A hydrogen is called primary, secondary or tertiary according to the carbon it is attached to (bonded to one, "
      "two or three other carbons).",
      ["Three CH₃ groups (primary carbons): 3 × 3 = 9 H", "One CH₂ (secondary carbon): 2 H",
       "One CH (tertiary carbon): 1 H", "Ratio 9 : 2 : 1 (total 12 H, C₅H₁₂)"],
      why_others_wrong="6 : 2 : 1 misses the CH₃ of the ethyl group; 9 : 1 : 2 swaps secondary and tertiary; 3 : 2 : 1 "
                       "counts primary carbons, not hydrogens.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', classification of carbon atoms",
      seconds=40),

    N(T_GO, "Electronic effects", "Intermediate",
      "How many of the following acids are stronger than ethanoic acid, CH₃COOH?\n"
      "HCOOH, ClCH₂COOH, CH₃CH₂COOH, FCH₂COOH, Cl₂CHCOOH, (CH₃)₃CCOOH",
      ["2", "3", v_2172, "5"], "C", v_2172,
      "Inductive effect and acid strength",
      "Electron-withdrawing (−I) groups stabilise the carboxylate ion and increase acid strength; electron-releasing "
      "(+I) alkyl groups do the opposite. Methanoic acid lacks the +I methyl group of ethanoic acid, so it is the "
      "stronger acid.",
      ["Stronger: HCOOH (no +I alkyl group), ClCH₂COOH, FCH₂COOH, Cl₂CHCOOH (−I halogens)",
       "Weaker: CH₃CH₂COOH and (CH₃)₃CCOOH (more +I alkyl)", "Count = 4"],
      why_others_wrong="2 or 3 usually leave out HCOOH or the dichloro acid; 5 wrongly counts propanoic acid, whose "
                       "ethyl group releases electrons.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', effect of substituents on acidity", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of OHC–CH₂–CH₂–C≡N is:",
      ["4-Oxobutanenitrile", "3-Cyanopropanal", "3-Formylpropanenitrile", "4-Cyanobutanal"], "A",
      "Priority of functional groups",
      "The nitrile group ranks above the aldehyde group, so –CN is the principal group (suffix '-nitrile') and the "
      "–CHO carbon, which is a chain carbon, is shown by the prefix 'oxo'.",
      ["Principal group: –C≡N; its carbon is C-1", "Chain: N≡C1–C2–C3–C4HO → butanenitrile",
       "C-4 carries =O → 4-oxobutanenitrile"],
      why_others_wrong="'3-Cyanopropanal' makes the lower-priority aldehyde the suffix; 'formyl' is used only when the "
                       "CHO carbon is outside the parent chain; '4-cyanobutanal' counts one carbon too many.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature: polyfunctional "
            f"compounds", seconds=45),

    Q(T_GO, "Reactive intermediates", "Intermediate", "assertion_reason",
      *ar("Anhydrous AlCl₃ acts as a nucleophile.", False,
          "The aluminium atom in AlCl₃ has only six electrons in its valence shell.", True),
      "Electrophiles and nucleophiles",
      "A nucleophile donates an electron pair; an electrophile accepts one. Aluminium in AlCl₃ has an incomplete "
      "octet and accepts an electron pair, so AlCl₃ is an electrophile (as in Friedel–Crafts reactions). A is false; "
      "R is true.",
      ["Al in AlCl₃: 3 bonds, 6 valence electrons", "Electron-pair acceptor → electrophile, not nucleophile"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "multi_statement",
      *ms("Which of the following structures are correctly named?",
          [("CH₃–O–CH₂–CH₂–CH₃: 1-methoxypropane", True),
           ("Br–CH₂–CH₂–COOH: 3-bromopropanoic acid", True),
           ("(CH₃)₃C–COOH: 2,2-dimethylpropanoic acid", True),
           ("CH₃–CH(CH₃)–CO–CH₃: 2-methylbutan-3-one", False),
           ("Cl–CH₂–CH₂–CHO: 3-chloropropanal", True)],
          [["a", "b", "d"], ["b", "c", "d", "e"], ["a", "c", "e"]], "B"),
      "IUPAC names of compounds with functional groups",
      "The chain is numbered so that the principal functional group gets the lowest locant. In (d) the carbonyl must "
      "be at C-2, so the name is 3-methylbutan-2-one.",
      ["(a) true", "(b) true: COOH carbon is C-1", "(c) true", "(d) false: 3-methylbutan-2-one",
       "(e) true: CHO carbon is C-1"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature", seconds=55),

    Q(T_GO, "Isomerism", "Intermediate", "statement_pair",
      *sp("1-Chloropropane, CH₃CH₂CH₂Cl, and 2-chloropropane, CH₃CHClCH₃, differ only in where the chlorine atom "
          "sits on the same three-carbon chain.", True,
          "Hexane and 2-methylpentane, which have different carbon skeletons, are classified as position isomers.",
          False),
      "Position and chain isomerism",
      "Compounds with the same carbon skeleton but a substituent or functional group at a different position are "
      "position isomers, as the two chloropropanes are. Hexane (unbranched) and 2-methylpentane (branched) have "
      "different carbon skeletons, so they are chain isomers, not position isomers.",
      ["Statement I: same chain, Cl on C-1 vs C-2: true",
       "Statement II: different skeletons → chain isomers, so the classification is false"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "match_list",
      *ml("Match the compound in List-I with the kinds of hybridised carbon atoms present in it (List-II).",
          ["Propyne, CH₃–C≡CH", "Propenenitrile, CH₂=CH–C≡N", "Propanal, CH₃CH₂CHO", "Benzene"],
          ["sp² only", "sp³ and sp²", "sp² and sp", "sp³ and sp"],
          "IV III II I", ["IV II III I", "III IV II I", "IV III I II"], "D"),
      "Hybridisation of carbon in different functional groups",
      "A carbon with four σ bonds is sp³, a carbon in a double bond is sp², and a carbon in a triple bond is sp.",
      ["Propyne: CH₃ sp³; both C≡C carbons sp → sp³ and sp (IV)",
       "Propenenitrile: CH₂=CH sp², C≡N carbon sp → sp² and sp (III)",
       "Propanal: CH₃, CH₂ sp³; CHO sp² → sp³ and sp² (II)", "Benzene: all sp² (I)"],
      why_others_wrong="Treating the nitrile carbon as sp² or the CHO carbon as sp³ gives the wrong pairings.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', shapes of carbon compounds",
      seconds=45),

    N(T_GO, "Isomerism", "Advanced",
      "How many structural isomers with the molecular formula C₅H₁₀ are cycloalkanes (saturated ring compounds)? "
      "Do not count stereoisomers separately.",
      ["3", "4", v_2178, "6"], "C", v_2178,
      "Ring-size and position isomers of cycloalkanes",
      "C₅H₁₀ fits CₙH₂ₙ, the formula of cycloalkanes as well as alkenes. Work through the possible ring sizes and place "
      "the remaining carbons as substituents.",
      ["Five-membered ring: cyclopentane", "Four-membered ring: methylcyclobutane",
       "Three-membered ring: ethylcyclopropane, 1,1-dimethylcyclopropane, 1,2-dimethylcyclopropane",
       "Total = 1 + 1 + 3 = 5"],
      why_others_wrong="3 or 4 miss the dimethylcyclopropanes or methylcyclobutane; 6 counts cis- and "
                       "trans-1,2-dimethylcyclopropane separately, which the question excludes.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=70),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₃–CH(CH₃)–CH(CH₃)–CH₂–CH(CH₂CH₃)–CH₃ is:",
      ["5-Ethyl-2,3-dimethylhexane", "3,5,6-Trimethylheptane", "2-Ethyl-4,5-dimethylhexane",
       "2,3,5-Trimethylheptane"], "D",
      "Choosing the longest chain and the lowest locants",
      "The longest chain runs through the ethyl group and has seven carbons. Numbering from the end nearer the first "
      "branch gives the methyl groups the locants 2, 3 and 5, lower at the first point of difference than 3, 5, 6.",
      ["Longest chain: CH₃–CH–CH–CH₂–CH–CH₂–CH₃ (7 C, heptane)",
       "Substituents: CH₃ on three carbons", "Left to right: 2, 3, 5; right to left: 3, 5, 6",
       "Name: 2,3,5-trimethylheptane"],
      why_others_wrong="'Hexane' names miss the longer chain through the ethyl group (and an ethyl at C-2 is never "
                       "correct); 3,5,6 numbers from the wrong end.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of branched alkanes",
      seconds=60),

    Q(T_GO, "Types of organic reactions", "Advanced", "multi_statement",
      *ms("For the base-catalysed reaction CH₃CHO + HCN → CH₃CH(OH)CN, which of the following statements are correct?",
          [("The cyanide ion acts as the nucleophile.", True),
           ("The carbonyl carbon is the electrophilic centre that is attacked.", True),
           ("The carbonyl carbon changes from sp² to sp³ hybridisation.", True),
           ("The reaction is a nucleophilic substitution.", False),
           ("The product contains a carbon atom bonded to four different groups.", True)],
          [["a", "b", "d"], ["a", "c", "d", "e"], ["b", "c", "e"]], "B"),
      "Nucleophilic addition to the carbonyl group",
      "The base produces CN⁻, which attacks the electron-deficient carbonyl carbon; the oxygen then takes up H⁺. Two "
      "molecules combine into one, so it is a nucleophilic addition. The carbonyl carbon goes from trigonal (sp²) to "
      "tetrahedral (sp³) and carries CH₃, H, OH and CN, four different groups.",
      ["(a) true", "(b) true", "(c) true", "(d) false: addition, not substitution",
       "(e) true: C bonded to CH₃, H, OH, CN"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition reactions", seconds=60),

    Q(T_GO, "Isomerism", "Advanced", "assertion_reason",
      *ar("2-Methylbut-2-ene, (CH₃)₂C=CH–CH₃, does not show geometrical isomerism, although both of its doubly bonded "
          "carbon atoms carry alkyl groups.", True,
          "One of its doubly bonded carbon atoms carries two identical groups (two methyl groups).", True,
          explains=True),
      "Condition for geometrical isomerism",
      "Cis and trans forms exist only when each carbon of the double bond carries two different groups. In "
      "2-methylbut-2-ene, C-2 bears two CH₃ groups, so interchanging them gives the same molecule. R is exactly why "
      "A holds.",
      ["C-2: CH₃ and CH₃ (identical)", "C-3: H and CH₃", "One carbon with identical groups → no cis/trans"],
      ncert=f"{NC11}, 'Hydrocarbons', geometrical isomerism in alkenes", seconds=40),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("In propene, CH₃–CH=CH₂, the three C–H bonds of the methyl group can take part in hyperconjugation with the "
          "π bond.", True,
          "As a result of this hyperconjugation, the =CH₂ carbon of propene acquires some negative charge.",
          True),
      "Hyperconjugation in alkenes",
      "The σ electrons of the C–H bonds of an alkyl group attached to a C=C bond are partly delocalised into the π "
      "system. In the hyperconjugation structures of propene, H⁺ is shown separated from the methyl carbon, the "
      "double bond shifts to C2–C3, and the negative charge appears on the terminal CH₂ carbon (C-1).",
      ["Statement I: three α C–H bonds → true",
       "Statement II: structure H⁺ ⁻CH₂–CH=CH₂ (old methyl carbon now double bonded), charge on the former =CH₂ carbon → true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hyperconjugation", seconds=50),
]
