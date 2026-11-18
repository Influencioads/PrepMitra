
# ================================================================ Organic Compounds Containing Oxygen (2445-2464)
# 2445: C6H5OH + Zn -> C6H6 + ZnO; 9.4 g phenol
m_2445 = F(94, 10) / mm(C=6, H=6, O=1) * mm(C=6, H=6)
assert mm(C=6, H=6, O=1) == 94 and m_2445 == F(78, 10)
v_2445 = "7.8 g"
# 2446: CH3CN + 2H2O (H+) -> CH3COOH + NH4+; 4.1 g nitrile
n_2446 = F(41, 10) / mm(C=2, H=3, N=1)
m_2446 = n_2446 * mm(C=2, H=4, O=2)
assert n_2446 == F(1, 10) and m_2446 == 6 and n_2446 * mm(C=2, H=5, N=1, O=1) == F(59, 10)
v_2446 = "6.0 g"
# 2451: acids with pKa below 6.4 (carbonic acid) liberate CO2 from NaHCO3
pka_2451 = {"ethanoic acid": 4.76, "benzoic acid": 4.19, "methanoic acid": 3.75, "phenol": 10.0,
            "4-nitrophenol": 7.1, "picric acid": 0.5, "ethanol": 15.9}
v_2451 = str(sum(1 for p in pka_2451.values() if p < 6.4))
assert v_2451 == "4"
# 2452: immediate turbidity with Lucas reagent at room temperature = tertiary alcohols
deg_2452 = {"2-methylpropan-2-ol": 3, "butan-2-ol": 2, "2-methylbutan-2-ol": 3, "propan-1-ol": 1,
            "1-methylcyclohexan-1-ol": 3, "cyclohexanol": 2, "butan-1-ol": 1}
v_2452 = str(sum(1 for d in deg_2452.values() if d == 3))
assert v_2452 == "3"
# 2459: C2H5OH -> CH3COOH loses 4 e-; Cr2O7^2- gains 6 e-; K2Cr2O7 = 294 g/mol
n_e = F(46, 10) / mm(C=2, H=6, O=1) * 4
m_2459 = n_e / 6 * 294
assert n_e == F(4, 10) and m_2459 == F(196, 10)
assert F(1, 10) * 2 / 6 * 294 == F(98, 10) and F(1, 10) * 294 == F(294, 10)
v_2459 = "19.6 g"
# 2460: propene -> (B2H6; H2O2/OH-) propan-1-ol -> (PCC) propanal -> 2 Ag per CHO
n_2460 = F(42, 10) / mm(C=3, H=6)
m_2460 = n_2460 * 2 * AM["Ag"]
assert n_2460 == F(1, 10) and m_2460 == F(216, 10)
v_2460 = "21.6 g"

QUESTIONS += [
    N(T_OX, "Phenols", "Basic",
      "9.4 g of phenol is heated with zinc dust and is converted completely into benzene. The mass of benzene formed "
      "is (C = 12, H = 1, O = 16):",
      ["3.9 g", v_2445, "9.4 g", "15.6 g"], "B", v_2445,
      "Reduction of phenol by zinc dust",
      "Phenol is converted into benzene on heating with zinc dust: C₆H₅OH + Zn → C₆H₆ + ZnO. One mole of phenol "
      "gives one mole of benzene.",
      ["Phenol: 9.4 / 94 = 0.10 mol", "Benzene: 0.10 × 78 = 7.8 g"],
      why_others_wrong="9.4 g repeats the mass of phenol; 3.9 g and 15.6 g halve or double the 1 : 1 mole ratio.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of phenol with zinc dust", seconds=30),

    N(T_OX, "Carboxylic acids", "Basic",
      "4.1 g of ethanenitrile, CH₃CN, is hydrolysed completely with dilute acid. The mass of the carboxylic acid "
      "formed is (C = 12, H = 1, N = 14, O = 16):",
      ["4.1 g", "4.6 g", "5.9 g", v_2446], "D", v_2446,
      "Preparation of carboxylic acids from nitriles",
      "Nitriles are hydrolysed, through amides, to carboxylic acids in the presence of H⁺ or OH⁻ as catalyst: "
      "CH₃C≡N → CH₃CONH₂ → CH₃COOH. One mole of nitrile gives one mole of acid.",
      ["CH₃CN: 4.1 / 41 = 0.10 mol", "CH₃COOH: 0.10 × 60 = 6.0 g"],
      why_others_wrong="5.9 g stops at the amide, CH₃CONH₂; 4.6 g is the mass of 0.10 mol of ethanol; 4.1 g repeats "
                       "the mass of the nitrile.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', methods of preparation of carboxylic acids",
      seconds=30),

    Q(T_OX, "Alcohols", "Basic", "direct",
      "The IUPAC name of glycerol, HOCH₂–CH(OH)–CH₂OH, is:",
      ["Propane-1,3-diol", "1,2,3-Trihydroxypropane", "Propane-1,2,3-triol", "Propan-1,2,3-ol"], "C",
      "Naming polyhydric alcohols",
      "For a polyol the 'e' of the alkane name is kept and multiplying prefixes are added to 'ol': three –OH groups "
      "on a three-carbon chain at C-1, C-2 and C-3 give propane-1,2,3-triol.",
      ["Parent: propane", "Three –OH at 1, 2, 3 → propane-1,2,3-triol"],
      why_others_wrong="Propane-1,3-diol has only two –OH groups; 'trihydroxypropane' cites the principal group as a "
                       "prefix; 'propan-1,2,3-ol' drops the multiplying prefix 'tri' and the 'e'.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nomenclature", seconds=25),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("In the acid-catalysed dehydration of ethanol, the formation of the carbocation is the slowest, "
          "rate-determining step.", True,
          "The reaction of an alcohol with an acid chloride to give an ester is carried out in the presence of a base "
          "such as pyridine, which neutralises the HCl formed.", True),
      "Dehydration mechanism; esterification with acid chlorides",
      "Dehydration of ethanol: (1) protonation of the –OH group, (2) loss of water to form the carbocation, the "
      "slowest step, (3) loss of a proton to give ethene. In acylation by an acid chloride, HCl is formed; pyridine "
      "removes it and shifts the equilibrium forward.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols", seconds=35),

    Q(T_OX, "Phenols", "Basic", "assertion_reason",
      *ar("Sodium phenoxide reacts with carbon dioxide, a weak electrophile, and the product on acidification gives "
          "salicylic acid.", True,
          "The phenoxide ion is even more reactive than phenol towards electrophilic aromatic substitution.", True,
          explains=True),
      "Kolbe's reaction",
      "NCERT: the phenoxide ion, generated by treating phenol with NaOH, is even more reactive than phenol towards "
      "electrophilic substitution, and hence it reacts even with CO₂, a weak electrophile, giving "
      "ortho-hydroxybenzoic acid (salicylic acid) after acidification. R is the reason for A.",
      ["–O⁻ is a stronger electron donor than –OH", "Strongly activated ring attacks the weak electrophile CO₂"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Kolbe's reaction", seconds=35),

    Q(T_OX, "Alcohols", "Basic", "match_list",
      *ml("Match the common name of the alcohol in List-I with its IUPAC name in List-II.",
          ["Isobutyl alcohol", "tert-Butyl alcohol", "sec-Butyl alcohol", "Neopentyl alcohol"],
          ["Butan-2-ol", "2,2-Dimethylpropan-1-ol", "2-Methylpropan-1-ol", "2-Methylpropan-2-ol"],
          "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B"),
      "Common and IUPAC names of alcohols",
      "Isobutyl = (CH₃)₂CHCH₂–; tert-butyl = (CH₃)₃C–; sec-butyl = CH₃CH₂CH(CH₃)–; neopentyl = (CH₃)₃CCH₂–.",
      ["(CH₃)₂CHCH₂OH → 2-methylpropan-1-ol", "(CH₃)₃COH → 2-methylpropan-2-ol",
       "CH₃CH₂CH(OH)CH₃ → butan-2-ol", "(CH₃)₃CCH₂OH → 2,2-dimethylpropan-1-ol"],
      why_others_wrong="Swapping isobutyl and tert-butyl confuses a 1° alcohol with a 3° alcohol; swapping sec-butyl "
                       "and neopentyl confuses a C₄ with a C₅ alcohol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nomenclature", seconds=40),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "An acid liberates CO₂ from aqueous sodium hydrogencarbonate only if it is a stronger acid than carbonic acid "
      "(pKa = 6.4). Using the pKa values given in brackets, how many of the following liberate CO₂ from NaHCO₃?\n"
      "Ethanoic acid (4.76), benzoic acid (4.19), methanoic acid (3.75), phenol (10.0), 4-nitrophenol (7.1), "
      "picric acid, i.e. 2,4,6-trinitrophenol (0.5), ethanol (15.9)",
      ["3", v_2451, "5", "6"], "B", v_2451,
      "Acid strength and the hydrogencarbonate test",
      "A lower pKa means a stronger acid. Acids with pKa below 6.4 are stronger than carbonic acid and displace CO₂ "
      "from NaHCO₃.",
      ["pKa < 6.4: ethanoic, benzoic, methanoic acids and picric acid → 4",
       "pKa > 6.4: phenol, 4-nitrophenol, ethanol → no CO₂"],
      why_others_wrong="3 counts only the carboxylic acids and leaves out picric acid, a phenol with a pKa of 0.5; "
                       "5 includes 4-nitrophenol, which is still weaker than carbonic acid.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', acidity of carboxylic acids", seconds=50),

    N(T_OX, "Alcohols", "Intermediate",
      "How many of the following alcohols give turbidity immediately with Lucas reagent (concentrated HCl and "
      "anhydrous ZnCl₂) at room temperature?\n"
      "2-Methylpropan-2-ol, butan-2-ol, 2-methylbutan-2-ol, propan-1-ol, 1-methylcyclohexan-1-ol, cyclohexanol, "
      "butan-1-ol",
      ["1", "2", v_2452, "5"], "C", v_2452,
      "Lucas test",
      "Tertiary alcohols form the insoluble alkyl chloride at once and give turbidity immediately; primary alcohols "
      "give no turbidity at room temperature (secondary alcohols react more slowly).",
      ["Tertiary: 2-methylpropan-2-ol, 2-methylbutan-2-ol, 1-methylcyclohexan-1-ol → 3",
       "Secondary: butan-2-ol, cyclohexanol; primary: propan-1-ol, butan-1-ol"],
      why_others_wrong="1 or 2 misses the cyclic tertiary alcohol 1-methylcyclohexan-1-ol or 2-methylbutan-2-ol; 5 "
                       "adds the secondary alcohols, which do not react immediately.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', distinguishing primary, secondary and tertiary alcohols",
      seconds=45),

    Q(T_OX, "Phenols", "Intermediate", "direct",
      "In the Reimer–Tiemann reaction, phenol is treated with chloroform in the presence of aqueous sodium "
      "hydroxide, and salicylaldehyde is obtained after acidification. The intermediate that is hydrolysed by the "
      "alkali in this reaction is:",
      ["Benzoyl chloride", "Chlorobenzene", "Benzyl chloride", "A substituted benzal chloride"], "D",
      "Reimer–Tiemann reaction",
      "NCERT: a –CHO group is introduced at the ortho position of the benzene ring; an intermediate substituted "
      "benzal chloride (a –CHCl₂ group on the phenoxide ring) is hydrolysed in the presence of alkali to give "
      "salicylaldehyde.",
      ["–CHCl₂ group introduced ortho to –O⁻", "Hydrolysis of –CHCl₂ → –CHO"],
      why_others_wrong="Benzoyl chloride (C₆H₅COCl) and benzyl chloride (C₆H₅CH₂Cl) carry the wrong number of "
                       "chlorine atoms on the side chain; chlorobenzene has chlorine on the ring and cannot give an "
                       "aldehyde group.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Reimer–Tiemann reaction", seconds=40),

    Q(T_OX, "Carboxylic acids", "Intermediate", "direct",
      "Which reagent reduces carboxylic acids to primary alcohols but does not easily reduce functional groups such "
      "as ester, nitro and halo groups?",
      ["Lithium aluminium hydride", "Sodium borohydride", "Diborane", "Zinc amalgam and concentrated HCl"], "C",
      "Selective reduction of carboxylic acids",
      "NCERT: carboxylic acids are reduced to primary alcohols by lithium aluminium hydride or, better, by "
      "diborane. Diborane does not easily reduce functional groups such as ester, nitro and halo. Sodium "
      "borohydride does not reduce the carboxyl group.",
      ["Diborane: –COOH → –CH₂OH; leaves ester, nitro, halo largely untouched"],
      why_others_wrong="LiAlH₄ reduces esters as well; NaBH₄ does not reduce –COOH; Zn–Hg/HCl is used for "
                       "Clemmensen reduction of aldehydes and ketones.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reduction of carboxylic acids", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("Ketones are readily oxidised by Tollens' reagent to carboxylic acids having the same number of carbon "
          "atoms.", False,
          "In aldehydes, the hydrogen atom on the carbonyl carbon is converted into an –OH group on oxidation, "
          "without breaking any carbon–carbon bond.", True),
      "Oxidation of aldehydes versus ketones",
      "Aldehydes are oxidised easily, even by mild oxidising agents such as Tollens' reagent, because of the H on "
      "the carbonyl carbon (R). Ketones lack this hydrogen; they are oxidised only under vigorous conditions by "
      "strong oxidising agents, with cleavage of C–C bonds, giving acids with fewer carbon atoms. A is false.",
      ["A: false", "R: true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', oxidation of aldehydes and ketones", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Esters are reduced to aldehydes by diisobutylaluminium hydride (DIBAL-H).", True,
          "Propanone undergoes the Cannizzaro reaction when heated with concentrated NaOH.", False),
      "DIBAL-H reduction; Cannizzaro reaction",
      "NCERT notes that DIBAL-H reduces nitriles to imines (then aldehydes on hydrolysis) and that esters are also "
      "reduced to aldehydes with DIBAL-H. The Cannizzaro reaction is shown by aldehydes with no α-hydrogen; "
      "propanone is a ketone with six α-hydrogens and instead undergoes aldol reaction.",
      ["Statement I: true", "Statement II: false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes; Cannizzaro reaction",
      seconds=40),

    Q(T_OX, "Alcohols", "Intermediate", "match_list",
      *ml("The vapours of each alcohol in List-I are passed over heated copper at 573 K. Match it with the main "
          "organic product in List-II.",
          ["Ethanol", "Propan-2-ol", "2-Methylpropan-2-ol", "Methanol"],
          ["Methanal", "2-Methylpropene", "Propanone", "Ethanal"],
          "IV III II I", ["IV III I II", "III IV II I", "II III IV I"], "D"),
      "Dehydrogenation of alcohols",
      "Over heated copper, primary alcohols are dehydrogenated to aldehydes and secondary alcohols to ketones. A "
      "tertiary alcohol has no H on the carbinol carbon, so it is dehydrated to an alkene instead.",
      ["Ethanol → ethanal", "Propan-2-ol → propanone", "2-Methylpropan-2-ol → 2-methylpropene",
       "Methanol → methanal"],
      why_others_wrong="Codes that give the tertiary alcohol a carbonyl product ignore the missing α-hydrogen on the "
                       "carbinol carbon; codes that swap ethanol and propan-2-ol mix up aldehyde and ketone formation.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', dehydrogenation of alcohols", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "multi_statement",
      *ms("Which of the following give benzaldehyde as the main organic product?",
          [("Toluene treated with chromyl chloride in CS₂, followed by hydrolysis", True),
           ("Benzene treated with carbon monoxide and HCl in the presence of anhydrous AlCl₃ or CuCl", True),
           ("Benzoyl chloride hydrogenated over palladium on barium sulphate", True),
           ("Benzonitrile reduced with SnCl₂ and HCl, followed by hydrolysis", True),
           ("Toluene oxidised with alkaline KMnO₄, followed by acidification", False)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
      "Preparation of aromatic aldehydes",
      "Etard reaction (chromyl chloride), Gattermann–Koch reaction (CO + HCl), Rosenmund reduction (H₂, Pd–BaSO₄) "
      "and Stephen reaction (SnCl₂/HCl, then H₃O⁺) all give benzaldehyde. Strong oxidation of toluene with KMnO₄ "
      "goes on to benzoic acid.",
      ["(a) Etard → C₆H₅CHO", "(b) Gattermann–Koch → C₆H₅CHO", "(c) Rosenmund → C₆H₅CHO",
       "(d) Stephen → C₆H₅CHO", "(e) KMnO₄ → C₆H₅COOH"],
      why_others_wrong="Options with (e) forget that KMnO₄ oxidises the side chain right up to –COOH; (a), (b) and "
                       "(c) only leaves out the Stephen reaction.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes", seconds=60),

    N(T_OX, "Alcohols", "Advanced",
      "Ethanol is oxidised to ethanoic acid by acidified potassium dichromate. The half-reactions are\n"
      "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O and C₂H₅OH + H₂O → CH₃COOH + 4H⁺ + 4e⁻.\n"
      "The minimum mass of K₂Cr₂O₇ (molar mass 294 g mol⁻¹) needed to oxidise 4.6 g of ethanol completely is "
      "(C = 12, H = 1, O = 16):",
      ["9.8 g", "14.7 g", "29.4 g", v_2459], "D", v_2459,
      "Electron balance in the oxidation of an alcohol",
      "Equate the electrons lost by ethanol to the electrons gained by dichromate.",
      ["Ethanol: 4.6 / 46 = 0.10 mol → electrons lost = 0.10 × 4 = 0.40 mol",
       "K₂Cr₂O₇ = 0.40 / 6 = 0.0667 mol", "Mass = 0.0667 × 294 = 19.6 g"],
      shortcut="3C₂H₅OH needs 2Cr₂O₇²⁻ (12 electrons each side).",
      why_others_wrong="9.8 g counts only 2 electrons per ethanol (oxidation stopping at ethanal); 29.4 g takes a "
                       "1 : 1 mole ratio; 14.7 g uses 3 electrons per ethanol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', oxidation of alcohols", seconds=90),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "4.2 g of propene is converted into an alcohol by hydroboration–oxidation (B₂H₆, then H₂O₂/OH⁻). The alcohol "
      "is oxidised with pyridinium chlorochromate (PCC), and the product is warmed with an excess of Tollens' "
      "reagent. Assuming every step is complete, the mass of silver deposited is (C = 12, H = 1, Ag = 108):",
      ["0 g", v_2460, "10.8 g", "43.2 g"], "B", v_2460,
      "Regiochemistry of hydroboration and the Tollens' test",
      "Hydroboration–oxidation adds water in an anti-Markovnikov manner, giving propan-1-ol. PCC oxidises a primary "
      "alcohol only to the aldehyde, propanal, which reduces Tollens' reagent: RCHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → "
      "RCOO⁻ + 2Ag + 2H₂O + 4NH₃.",
      ["Propene: 4.2 / 42 = 0.10 mol → 0.10 mol propan-1-ol → 0.10 mol propanal",
       "Ag = 2 × 0.10 = 0.20 mol → 0.20 × 108 = 21.6 g"],
      why_others_wrong="0 g assumes Markovnikov addition (propan-2-ol → propanone, which gives no silver mirror); "
                       "10.8 g uses one Ag per aldehyde; 43.2 g uses four, as for methanal.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', hydroboration–oxidation; 'Aldehydes, Ketones and Carboxylic "
            "Acids', Tollens' test", seconds=90),

    Q(T_OX, "Ethers", "Advanced", "assertion_reason",
      *ar("When methyl tert-butyl ether, CH₃–O–C(CH₃)₃, is heated with HI, the products are methanol and "
          "2-iodo-2-methylpropane.", True,
          "In this cleavage, the iodide ion attacks the methyl carbon by the SN2 mechanism.", False),
      "Cleavage of ethers containing a tertiary alkyl group",
      "When one alkyl group is tertiary, the protonated ether ionises by the SN1 mechanism to give the stable "
      "tert-butyl carbocation, which combines with I⁻; methanol is the other product. An SN2 attack on the methyl "
      "carbon would instead give CH₃I and tert-butyl alcohol. So A is true and R is false.",
      ["A: true (tert-butyl iodide + methanol)", "R: false; the reaction follows SN1"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', cleavage of C–O bond in ethers", seconds=50),

    Q(T_OX, "Phenols", "Advanced", "statement_pair",
      *sp("Phenol reacts with dilute nitric acid at 298 K to give p-nitrophenol as the only product.", False,
          "2,4,6-Trinitrophenol is a weaker acid than phenol.", False),
      "Nitration of phenol; acidity of nitrophenols",
      "With dilute HNO₃ at low temperature (298 K), phenol gives a mixture of ortho- and para-nitrophenols, which "
      "are separated by steam distillation. Three –NO₂ groups make picric acid a much stronger acid than phenol "
      "(pKa about 0.5 against 10.0).",
      ["Statement I: false; o- and p-nitrophenols are formed", "Statement II: false; picric acid is far stronger"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nitration of phenol; acidity of phenols", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following pairs can be distinguished by the test given?",
          [("Propanal and propanone: Tollens' reagent", True),
           ("Pentan-2-one and pentan-3-one: iodoform test (I₂ and NaOH)", True),
           ("Benzaldehyde and acetophenone: Fehling's solution", False),
           ("Phenol and benzoic acid: aqueous NaHCO₃", True),
           ("Ethanol and methanol: 2,4-dinitrophenylhydrazine", False)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
      "Chemical tests that distinguish oxygen compounds",
      "Propanal reduces Tollens' reagent, propanone does not. Pentan-2-one is a methyl ketone and gives iodoform; "
      "pentan-3-one does not. Aromatic aldehydes such as benzaldehyde do not respond to Fehling's test, and "
      "acetophenone (a ketone) does not either, so Fehling's solution cannot tell them apart. Benzoic acid "
      "liberates CO₂ from NaHCO₃, phenol does not. Neither alcohol has a carbonyl group, so neither reacts with "
      "2,4-DNP.",
      ["(a) true", "(b) true", "(c) false: neither gives a positive Fehling's test", "(d) true",
       "(e) false: both negative"],
      why_others_wrong="Options containing (c) assume every aldehyde reduces Fehling's solution; options containing "
                       "(e) use a carbonyl reagent on two alcohols.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical tests to distinguish aldehydes and "
            "ketones", seconds=75),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following statements about the carbonyl group are correct?",
          [("The carbonyl carbon is sp² hybridised and lies at the centre of a trigonal planar arrangement, with "
            "bond angles of about 120°.", True),
           ("The carbonyl carbon is an electrophilic (Lewis acid) centre and the carbonyl oxygen a nucleophilic "
            "(Lewis base) centre.", True),
           ("Carbonyl compounds have substantial dipole moments and are more polar than ethers.", True),
           ("The carboxylic carbon of a carboxylic acid is more electrophilic than the carbonyl carbon of an "
            "aldehyde.", False),
           ("The C=O bond of an aldehyde is non-polar, because both atoms share the π electrons equally.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "D"),
      "Nature of the carbonyl group",
      "NCERT: the carbonyl carbon is sp² hybridised, trigonal planar, with ~120° bond angles; the C=O bond is "
      "polarised because oxygen is more electronegative, making carbon an electrophilic centre and oxygen a "
      "nucleophilic centre; carbonyl compounds have substantial dipole moments and are more polar than ethers. "
      "In carboxylic acids the carboxylic carbon is less electrophilic than the carbonyl carbon because of "
      "resonance with the –OH oxygen.",
      ["(a) true", "(b) true", "(c) true", "(d) false: resonance makes it less electrophilic",
       "(e) false: the C=O bond is polar"],
      why_others_wrong="Options containing (d) overlook the resonance of the carboxyl group; the option with (e) "
                       "ignores the electronegativity difference between carbon and oxygen.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nature of carbonyl group; structure of carboxyl "
            "group", seconds=60),
]
