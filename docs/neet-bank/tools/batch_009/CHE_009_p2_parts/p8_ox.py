
# ================================================================ Organic Compounds Containing Oxygen (2207-2223)
# 2208: 2CH3COCl + (CH3)2Cd -> 2CH3COCH3 + CdCl2
n_2208 = F(157, 10) / mm(C=2, H=3, O=1, Cl=1)
v_2208 = g(n_2208 * mm(C=3, H=6, O=1))
assert n_2208 == F(1, 5) and v_2208 == "11.6 g"
# 2213: CH3COONH4 -> (heat) CH3CONH2 + H2O
n_2213 = F(77, 10) / mm(C=2, H=7, O=2, N=1)
v_2213 = g(n_2213 * mm(C=2, H=5, O=1, N=1))
assert n_2213 == F(1, 10) and v_2213 == "5.9 g"
# 2214: alcohols oxidised to ketones (secondary alcohols)
kind = {"propan-2-ol": 2, "butan-2-ol": 2, "cyclohexanol": 2, "2-methylpropan-2-ol": 3, "propan-1-ol": 1,
        "pentan-3-ol": 2, "benzyl alcohol": 1}
v_2214 = str(sum(1 for c in kind.values() if c == 2))
assert v_2214 == "4"
# 2219: C5H12O alcohols by class
c5_alcohols = {"pentan-1-ol": 1, "2-methylbutan-1-ol": 1, "3-methylbutan-1-ol": 1, "2,2-dimethylpropan-1-ol": 1,
               "pentan-2-ol": 2, "pentan-3-ol": 2, "3-methylbutan-2-ol": 2, "2-methylbutan-2-ol": 3}
assert len(c5_alcohols) == 8
v_2219 = str(sum(1 for c in c5_alcohols.values() if c == 1))
assert v_2219 == "4"

QUESTIONS += [
    Q(T_OX, "Aldehydes and ketones", "Basic", "direct",
      "Formalin, a 40% aqueous solution of methanal, is mainly used:",
      ["as a food preservative", "as a solvent for paints", "as a fuel in spirit lamps",
       "to preserve biological specimens"], "D",
      "Uses of methanal",
      "NCERT lists formalin (about 40% methanal in water) as the liquid used to preserve biological specimens.",
      ["Formalin = 40% HCHO(aq)", "Use: preserving biological specimens"],
      why_others_wrong="Sodium benzoate, not formalin, is the common food preservative; formalin is neither a paint "
                       "solvent nor a lamp fuel.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', uses of aldehydes and ketones", seconds=20),

    N(T_OX, "Aldehydes and ketones", "Basic",
      "Ketones are prepared by treating acyl chlorides with dialkylcadmium: 2CH₃COCl + (CH₃)₂Cd → 2CH₃COCH₃ + CdCl₂. "
      "The mass of propanone obtained from 15.7 g of ethanoyl chloride, assuming complete conversion, is "
      "(C = 12, H = 1, O = 16, Cl = 35.5):",
      ["5.8 g", v_2208, "23.2 g", "15.7 g"], "B", v_2208,
      "Preparation of ketones from acyl chlorides",
      "Each molecule of acyl chloride gives one molecule of ketone; the dialkylcadmium supplies one alkyl group to each.",
      ["Molar mass of CH₃COCl = 78.5 g mol⁻¹; n = 15.7/78.5 = 0.20 mol", "n(CH₃COCH₃) = 0.20 mol",
       "Mass = 0.20 × 58 = 11.6 g"],
      why_others_wrong="5.8 g takes the 2 : 1 ratio the wrong way; 23.2 g doubles the moles; 15.7 g assumes equal "
                       "masses.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of ketones from acyl chlorides",
      seconds=40),

    Q(T_OX, "Carboxylic acids", "Basic", "match_list",
      *ml("Match the substance in List-I with its use in List-II.",
          ["Methanoic acid", "Ethanoic acid", "Sodium benzoate", "Sodium or potassium salts of higher fatty acids"],
          ["Soaps and detergents", "Rubber, textile, dyeing, leather and electroplating industries",
           "Food preservative", "Solvent, and as vinegar in the food industry"],
          "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "D"),
      "Uses of carboxylic acids and their salts",
      "These are the uses NCERT gives: methanoic acid in rubber, textile, dyeing, leather and electroplating; "
      "ethanoic acid as a solvent and as vinegar; sodium benzoate as a food preservative; and salts of higher fatty "
      "acids as soaps.",
      ["Methanoic acid: II", "Ethanoic acid: IV", "Sodium benzoate: III", "Salts of fatty acids: I"],
      why_others_wrong="Swapping methanoic and ethanoic acids, or the preservative and soaps, mismatches the uses.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', uses of carboxylic acids", seconds=35),

    Q(T_OX, "Ethers", "Basic", "statement_pair",
      *sp("The miscibility of ethers with water resembles that of alcohols of the same molecular mass.", True,
          "Ether molecules are associated through intermolecular hydrogen bonds, as alcohol molecules are.", False),
      "Solubility and boiling points of ethers",
      "Ethers can accept hydrogen bonds from water through the lone pairs on oxygen, so ethoxyethane and butan-1-ol "
      "are miscible with water to almost the same extent. But ethers have no O–H group, so their molecules cannot "
      "hydrogen bond with one another; this is why their boiling points are much lower than those of isomeric "
      "alcohols.",
      ["Statement I: true (ethoxyethane ≈ butan-1-ol in miscibility)", "Statement II: false; no O–H in ethers"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties of ethers", seconds=30),

    Q(T_OX, "Phenols", "Basic", "assertion_reason",
      *ar("Phenol dissolves in aqueous sodium hydroxide.", True,
          "Phenol reacts with bromine water to give a white precipitate.", True),
      "Acidic character of phenol",
      "Phenol is acidic enough to react with NaOH and form the soluble salt sodium phenoxide. R is a true reaction of "
      "phenol (bromination of the activated ring to 2,4,6-tribromophenol), but it is about ring substitution, not "
      "acidity, so it does not explain A.",
      ["C₆H₅OH + NaOH → C₆H₅O⁻Na⁺ + H₂O (soluble)", "R: electrophilic substitution, unrelated to A"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols; electrophilic substitution", seconds=30),

    Q(T_OX, "Alcohols", "Intermediate", "match_list",
      *ml("Match the conversion in List-I with the conditions used for it in List-II.",
          ["Ethanol → ethene", "A secondary alcohol → alkene", "A tertiary alcohol → alkene",
           "Ethanol (in excess) → ethoxyethane"],
          ["20% H₃PO₄, 358 K", "Concentrated H₂SO₄, 443 K", "Concentrated H₂SO₄, 413 K", "85% H₃PO₄, 440 K"],
          "II IV I III", ["IV II I III", "II I IV III", "III IV I II"], "B"),
      "Ease of dehydration of alcohols",
      "The ease of dehydration is tertiary > secondary > primary, so the conditions needed become milder from primary "
      "to tertiary. With ethanol in excess and a lower temperature (413 K), intermolecular dehydration gives the ether.",
      ["Primary (ethanol): conc. H₂SO₄, 443 K (II)", "Secondary: 85% H₃PO₄, 440 K (IV)",
       "Tertiary: 20% H₃PO₄, 358 K (I)", "Ether from ethanol: conc. H₂SO₄, 413 K (III)"],
      why_others_wrong="Codes that give the tertiary alcohol the harshest conditions reverse the order of ease of "
                       "dehydration; 443 K versus 413 K decides alkene versus ether for ethanol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of alcohols: dehydration", seconds=45),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "Ethanoic acid reacts with ammonia to give ammonium ethanoate, which on strong heating loses water to give "
      "ethanamide. The mass of ethanamide obtained from 7.7 g of ammonium ethanoate, assuming complete conversion, is "
      "(C = 12, H = 1, N = 14, O = 16):",
      ["7.7 g", "6.0 g", "4.5 g", v_2213], "D", v_2213,
      "Formation of amides from carboxylic acids",
      "CH₃COOH + NH₃ ⇌ CH₃COONH₄; on heating, CH₃COONH₄ → CH₃CONH₂ + H₂O. One mole of salt gives one mole of amide.",
      ["Molar mass of CH₃COONH₄ = 77 g mol⁻¹; n = 7.7/77 = 0.10 mol", "Molar mass of CH₃CONH₂ = 59 g mol⁻¹",
       "Mass = 0.10 × 59 = 5.9 g"],
      why_others_wrong="7.7 g ignores the loss of water; 6.0 g is the mass of ethanoic acid; 4.5 g subtracts the "
                       "ammonia instead of water.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions of carboxylic acids: with ammonia",
      seconds=45),

    N(T_OX, "Alcohols", "Intermediate",
      "How many of the following alcohols give a ketone on oxidation with acidified potassium dichromate?\n"
      "Propan-2-ol, butan-2-ol, cyclohexanol, 2-methylpropan-2-ol, propan-1-ol, pentan-3-ol, benzyl alcohol",
      ["2", "3", v_2214, "5"], "C", v_2214,
      "Oxidation of primary, secondary and tertiary alcohols",
      "Secondary alcohols are oxidised to ketones. Primary alcohols give aldehydes and then carboxylic acids; tertiary "
      "alcohols resist oxidation under these conditions.",
      ["Secondary: propan-2-ol, butan-2-ol, cyclohexanol, pentan-3-ol → ketones",
       "Primary: propan-1-ol, benzyl alcohol → aldehyde/acid", "Tertiary: 2-methylpropan-2-ol → no ketone",
       "Count = 4"],
      why_others_wrong="3 usually misses cyclohexanol (a secondary ring alcohol); 5 counts benzyl alcohol or the "
                       "tertiary alcohol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', oxidation of alcohols", seconds=45),

    Q(T_OX, "Phenols", "Intermediate", "assertion_reason",
      *ar("o-Nitrophenol and p-nitrophenol can be separated by steam distillation, o-nitrophenol passing over with the "
          "steam.", True,
          "o-Nitrophenol has intramolecular hydrogen bonding, whereas p-nitrophenol molecules are associated through "
          "intermolecular hydrogen bonds.", True, explains=True),
      "Hydrogen bonding and volatility of nitrophenols",
      "Nitration of phenol with dilute nitric acid gives a mixture of o- and p-nitrophenols. In the ortho isomer the "
      "–OH and –NO₂ groups are hydrogen bonded within the molecule, so it is not associated and is steam volatile. "
      "The para isomer is held together by intermolecular hydrogen bonds and is much less volatile. R explains A.",
      ["o-Nitrophenol: intramolecular H-bond → volatile in steam", "p-Nitrophenol: intermolecular H-bonds → not",
       "Steam distillation separates them"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', electrophilic substitution in phenols: nitration", seconds=40),

    Q(T_OX, "Carboxylic acids", "Intermediate", "assertion_reason",
      *ar("Carboxylic acids do not give the characteristic nucleophilic addition reactions of aldehydes and ketones, "
          "although they contain a C=O group.", True,
          "The carbonyl carbon of a carboxylic acid is sp³ hybridised.", False),
      "Structure of the carboxyl group",
      "The carboxyl carbon is sp² hybridised and lies in a planar group, just as in aldehydes and ketones. It is less "
      "electrophilic because the lone pair on the –OH oxygen is delocalised onto the C=O group by resonance, so "
      "carboxylic acids do not show typical carbonyl reactions. A is true; R is false.",
      ["Carboxyl carbon: three σ bonds + one π bond → sp²", "Resonance lowers the electrophilic character",
       "A true, R false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', structure of the carboxyl group", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "direct",
      "Propanal is treated with dilute NaOH and the aldol formed is heated. The final product is:",
      ["Hex-2-enal", "3-Hydroxyhexanal", "2-Methylpent-3-enal", "2-Methylpent-2-enal"], "D",
      "Aldol condensation",
      "The α-carbon of one propanal molecule (C-2) adds to the carbonyl carbon of another, giving "
      "3-hydroxy-2-methylpentanal. On heating, water is lost between the α and β carbons to give the α,β-unsaturated "
      "aldehyde.",
      ["2CH₃CH₂CHO → CH₃CH₂CH(OH)–CH(CH₃)–CHO (aldol)", "−H₂O → CH₃CH₂CH=C(CH₃)–CHO",
       "Name: 2-methylpent-2-enal"],
      why_others_wrong="Hex-2-enal and 3-hydroxyhexanal would need the bond to form at the terminal CH₃, which is not "
                       "the α-carbon; in 2-methylpent-3-enal the double bond is not conjugated with C=O.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol condensation", seconds=50),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Aldehydes react with one equivalent of a monohydric alcohol in the presence of dry HCl to give a hemiacetal, "
          "which reacts with a second molecule of alcohol to give an acetal.", True,
          "Acetals and ketals are hydrolysed by aqueous mineral acids back to the corresponding aldehydes and "
          "ketones.", True),
      "Hemiacetals, acetals and ketals",
      "Dry HCl protonates the carbonyl oxygen and makes the carbonyl carbon more electrophilic, so the weak "
      "nucleophile ROH can add (hemiacetal); a second ROH replaces the –OH (acetal, a gem-dialkoxy compound). With "
      "aqueous acid the reaction runs backwards and the carbonyl compound is regenerated.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', addition of alcohols", seconds=35),

    N(T_OX, "Alcohols", "Advanced",
      "How many of the structural isomers with the molecular formula C₅H₁₂O are primary alcohols (and so can be "
      "oxidised to aldehydes)?",
      ["3", v_2219, "5", "8"], "B", v_2219,
      "Classifying the isomeric pentanols",
      "There are eight alcohols C₅H₁₁OH. An alcohol is primary when the –OH carbon is attached to only one other "
      "carbon (–CH₂OH).",
      ["Primary: pentan-1-ol, 2-methylbutan-1-ol, 3-methylbutan-1-ol, 2,2-dimethylpropan-1-ol (4)",
       "Secondary: pentan-2-ol, pentan-3-ol, 3-methylbutan-2-ol (3)", "Tertiary: 2-methylbutan-2-ol (1)"],
      why_others_wrong="3 misses 2,2-dimethylpropan-1-ol (neopentyl alcohol), which is primary although its "
                       "neighbouring carbon is quaternary; 5 adds a secondary alcohol; 8 counts all alcohols.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', classification and oxidation of alcohols", seconds=75),

    Q(T_OX, "Ethers", "Advanced", "assertion_reason",
      *ar("When (CH₃)₃C–Br is heated with sodium methoxide, the main product is 2-methylpropene and not "
          "tert-butyl methyl ether.", True,
          "Alkoxides are strong bases as well as nucleophiles, and with a tertiary alkyl halide elimination competes "
          "over substitution.", True, explains=True),
      "Limitation of Williamson synthesis",
      "Williamson synthesis works best with primary alkyl halides. A tertiary halide is crowded, so the alkoxide removes "
      "a β-hydrogen instead of attacking carbon, and an alkene is formed. tert-Butyl methyl ether is therefore made from "
      "sodium tert-butoxide and bromomethane. R explains A.",
      ["(CH₃)₃C–Br + CH₃O⁻ → CH₂=C(CH₃)₂ + CH₃OH + Br⁻", "Better route: (CH₃)₃C–O⁻Na⁺ + CH₃Br → (CH₃)₃C–O–CH₃"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of ethers: Williamson synthesis", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "match_list",
      *ml("Match each pair of compounds in List-I with the test in List-II that distinguishes them. Use each test once.",
          ["Ethanal and propanone", "Ethanol and methanol", "Phenol and ethanol", "Ethanoic acid and phenol"],
          ["Effervescence with aqueous NaHCO₃", "Tollens' reagent", "Iodoform test (I₂ and NaOH)",
           "White precipitate with bromine water"],
          "II III IV I", ["III II IV I", "II III I IV", "II IV III I"], "D"),
      "Chemical tests for oxygen compounds",
      "Tollens' reagent is reduced by ethanal but not by propanone (both give iodoform, so that test fails here). "
      "Ethanol gives iodoform and methanol does not. Phenol gives a white precipitate of 2,4,6-tribromophenol with "
      "bromine water; ethanol does not. Ethanoic acid is strong enough to liberate CO₂ from NaHCO₃; phenol is not. "
      "Once ethanol/methanol has taken the iodoform test, phenol/ethanol must take bromine water and the acid/phenol "
      "pair NaHCO₃.",
      ["Ethanal/propanone: Tollens' (II)", "Ethanol/methanol: iodoform (III)", "Phenol/ethanol: bromine water (IV)",
       "Ethanoic acid/phenol: NaHCO₃ (I)"],
      why_others_wrong="Iodoform cannot distinguish ethanal from propanone; NaHCO₃ cannot distinguish phenol from "
                       "ethanol, as neither reacts.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids' and 'Alcohols, Phenols and Ethers', chemical tests",
      seconds=80),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following compounds give BOTH a positive iodoform test and an orange-yellow precipitate with "
          "2,4-dinitrophenylhydrazine?",
          [("Ethanal", True), ("Propanal", False), ("Butan-2-one", True), ("Ethanol", False),
           ("Acetophenone (C₆H₅COCH₃)", True)],
          [["a", "b", "c"], ["a", "d", "e"], ["c", "d", "e"]], "B"),
      "Combining the iodoform and 2,4-DNP tests",
      "2,4-DNP reacts with the C=O group of aldehydes and ketones. The iodoform test needs a CH₃CO– group (or a "
      "CH₃CH(OH)– group, which is first oxidised to it).",
      ["(a) ethanal: CH₃CHO, C=O and CH₃CO– → both", "(b) propanal: no CH₃CO– → no iodoform",
       "(c) butan-2-one: CH₃COC₂H₅ → both", "(d) ethanol: iodoform yes, but no C=O → no 2,4-DNP",
       "(e) acetophenone: C₆H₅COCH₃ → both"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', haloform reaction; reactions with ammonia "
            f"derivatives", seconds=60),

    Q(T_OX, "Carboxylic acids", "Advanced", "multi_statement",
      *ms("Which of the following statements about reactions of carboxylic acids are correct?",
          [("With PCl₅, a carboxylic acid gives the acyl chloride, POCl₃ and HCl.", True),
           ("Thionyl chloride is preferred for making acyl chlorides, because the other two products are gases that "
            "escape.", True),
           ("With PCl₃, a carboxylic acid gives the acyl chloride and H₃PO₃.", True),
           ("Carboxylic acids are reduced to primary alcohols by sodium borohydride.", False),
           ("On heating with P₂O₅, a carboxylic acid gives the acid anhydride.", True)],
          [["a", "b", "d"], ["b", "c", "d", "e"], ["a", "c", "d", "e"]], "D"),
      "Reactions of the –OH part of the carboxyl group",
      "The –OH of a carboxylic acid is replaced by Cl with PCl₅, PCl₃ or SOCl₂ (SO₂ and HCl escape, leaving a pure "
      "product). Strong dehydrating agents such as P₂O₅ give anhydrides. Carboxylic acids are reduced by LiAlH₄ or "
      "diborane; NaBH₄ does not reduce the carboxyl group.",
      ["(a) RCOOH + PCl₅ → RCOCl + POCl₃ + HCl: true", "(b) RCOOH + SOCl₂ → RCOCl + SO₂ + HCl: true",
       "(c) 3RCOOH + PCl₃ → 3RCOCl + H₃PO₃: true", "(d) false: NaBH₄ does not reduce –COOH",
       "(e) true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions of carboxylic acids",
      seconds=55),
]
