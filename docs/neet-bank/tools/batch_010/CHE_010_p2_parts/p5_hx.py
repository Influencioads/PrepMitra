
# ================================================================ Organic Compounds Containing Halogens (2432-2444)
# 2432: (CH3)3COH + HCl -> (CH3)3CCl; 7.4 g alcohol
M_tbuoh = mm(C=4, H=10, O=1)
M_tbucl = mm(C=4, H=9, Cl=1)
assert M_tbuoh == 74 and M_tbucl == F(925, 10)
m_2432 = F(74, 10) / M_tbuoh * M_tbucl
assert m_2432 == F(925, 100)
v_2432 = "9.25 g"
assert F(1, 10) * mm(H=1, Cl=1) == F(365, 100) and F(1, 10) * mm(C=4, H=9, Br=1) == F(137, 10)
# 2436: C2H5OH + SOCl2 -> C2H5Cl + SO2(g) + HCl(g); 4.6 g ethanol
n_2436 = F(46, 10) / mm(C=2, H=6, O=1)
V_2436 = 2 * n_2436 * F(224, 10)
assert n_2436 == F(1, 10) and V_2436 == F(448, 100)
v_2436 = "4.48 L"
# 2437: Fittig 2 C6H5Cl + 2 Na -> C6H5-C6H5 + 2 NaCl; 11.25 g chlorobenzene
M_phcl = mm(C=6, H=5, Cl=1)
assert M_phcl == F(1125, 10)
m_2437 = F(1125, 100) / M_phcl / 2 * mm(C=12, H=10)
assert m_2437 == F(77, 10)
v_2437 = "7.7 g"
# 2441: structural isomers of C5H11Br classified as 1/2/3 degree
c5_2441 = {"1-bromopentane": 1, "2-bromopentane": 2, "3-bromopentane": 2, "1-bromo-2-methylbutane": 1,
           "2-bromo-2-methylbutane": 3, "2-bromo-3-methylbutane": 2, "1-bromo-3-methylbutane": 1,
           "1-bromo-2,2-dimethylpropane": 1}
assert len(c5_2441) == 8
v_2441 = str(sum(1 for d in c5_2441.values() if d == 2))
assert v_2441 == "3" and sum(1 for d in c5_2441.values() if d == 1) == 4

QUESTIONS += [
    N(T_HX, "C-X bond and preparation", "Basic",
      "7.4 g of 2-methylpropan-2-ol is shaken with concentrated hydrochloric acid at room temperature and is "
      "converted completely into 2-chloro-2-methylpropane. The mass of the alkyl chloride formed is (C = 12, H = 1, "
      "O = 16, Cl = 35.5):",
      ["3.65 g", "7.40 g", "13.7 g", v_2432], "D", v_2432,
      "Preparation of a tertiary alkyl chloride from an alcohol",
      "Tertiary alcohols react with concentrated HCl even at room temperature: (CH₃)₃C–OH + HCl → (CH₃)₃C–Cl + "
      "H₂O. One mole of alcohol gives one mole of alkyl chloride.",
      ["Alcohol: 7.4 / 74 = 0.10 mol", "(CH₃)₃CCl: M = 92.5 g mol⁻¹", "Mass = 0.10 × 92.5 = 9.25 g"],
      why_others_wrong="3.65 g is the mass of HCl consumed; 7.40 g repeats the mass of the alcohol; 13.7 g uses the "
                       "molar mass of the bromide, C₄H₉Br.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=40),

    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "The IUPAC name of benzyl chloride, C₆H₅CH₂Cl, is:",
      ["1-Chloro-2-methylbenzene", "(Chloromethyl)benzene", "Chlorobenzene", "1-Chloro-4-methylbenzene"], "B",
      "Naming a benzylic halide",
      "In C₆H₅CH₂Cl the chlorine is on the side-chain carbon, not on the ring. The substituent –CH₂Cl on benzene "
      "is named chloromethyl, so the compound is (chloromethyl)benzene.",
      ["Cl on the CH₂ group attached to the ring", "Substituent –CH₂Cl = chloromethyl → (chloromethyl)benzene"],
      why_others_wrong="1-Chloro-2-methylbenzene and 1-chloro-4-methylbenzene are chlorotoluenes, with chlorine on the "
                       "ring; chlorobenzene, C₆H₅Cl, has no CH₂ group.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nomenclature", seconds=25),

    Q(T_HX, "Polyhalogen compounds", "Basic", "statement_pair",
      *sp("Exposure to lower levels of dichloromethane in air can lead to slightly impaired hearing and vision.",
          True,
          "Exposure to carbon tetrachloride can make the heart beat irregularly or stop.", True),
      "Health effects of polyhalogen compounds",
      "NCERT notes that lower levels of methylene chloride in air can lead to slightly impaired hearing and vision, "
      "and that exposure to carbon tetrachloride can make the heart beat irregularly or stop (besides liver damage "
      "and effects on the nervous system).",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds: dichloromethane, tetrachloromethane",
      seconds=30),

    Q(T_HX, "SN1 and SN2", "Basic", "match_list",
      *ml("Match the reagent in List-I, reacting with a haloalkane R–X, with the main organic product in List-II.",
          ["A primary amine, R′NH₂", "Silver cyanide, AgCN", "Potassium nitrite, KNO₂",
           "Silver salt of a carboxylic acid, R′COOAg"],
          ["Alkyl nitrite, R–O–N=O", "Isocyanide, R–NC", "Ester, R′COOR", "Secondary amine, R–NH–R′"],
          "IV II I III", ["II IV I III", "IV II III I", "IV I II III"], "B"),
      "Nucleophilic substitution products of haloalkanes",
      "A primary amine attacks through nitrogen to give a secondary amine; AgCN, being mainly covalent, attacks "
      "through nitrogen to give an isocyanide; KNO₂ (ionic) attacks through oxygen to give an alkyl nitrite; the "
      "carboxylate ion of a silver salt gives an ester.",
      ["R′NH₂ → RNHR′", "AgCN → RNC", "KNO₂ → R–O–N=O", "R′COOAg → R′COOR"],
      why_others_wrong="Swapping AgCN and the amine mixes up an isocyanide and an amine; swapping KNO₂ with AgCN "
                       "or the silver carboxylate confuses the ambident nitrite attack with other reagents.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions", seconds=40),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "4.6 g of ethanol is converted completely into chloroethane by heating with thionyl chloride. The total volume "
      "of the gaseous by-products, measured at STP, is (C = 12, H = 1, O = 16; molar volume at STP = "
      "22.4 L mol⁻¹):",
      ["2.24 L", v_2436, "6.72 L", "1.12 L"], "B", v_2436,
      "Thionyl chloride method",
      "C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑. Both by-products are gases, which is why this method gives a fairly "
      "pure alkyl chloride.",
      ["Ethanol: 4.6 / 46 = 0.10 mol", "SO₂ + HCl = 0.10 + 0.10 = 0.20 mol", "Volume = 0.20 × 22.4 = 4.48 L"],
      why_others_wrong="2.24 L counts only one of the two gases; 6.72 L also counts chloroethane, which is the "
                       "product and not a by-product; 1.12 L halves one gas.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation from alcohols: thionyl chloride", seconds=45),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "11.25 g of chlorobenzene is treated with sodium in dry ether, and the Fittig reaction goes to completion. The "
      "mass of biphenyl, C₆H₅–C₆H₅, formed is (C = 12, H = 1, Cl = 35.5):",
      ["3.85 g", "15.4 g", v_2437, "11.25 g"], "C", v_2437,
      "Fittig reaction",
      "Aryl halides couple with sodium in dry ether: 2C₆H₅Cl + 2Na → C₆H₅–C₆H₅ + 2NaCl. Two moles of aryl halide "
      "give one mole of biphenyl.",
      ["C₆H₅Cl: 11.25 / 112.5 = 0.10 mol", "Biphenyl: 0.10 / 2 = 0.050 mol",
       "Mass = 0.050 × 154 = 7.7 g"],
      why_others_wrong="15.4 g forgets that two aryl groups make one biphenyl; 3.85 g halves twice; 11.25 g repeats "
                       "the mass of chlorobenzene.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes with metals: Fittig reaction",
      seconds=45),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "assertion_reason",
      *ar("Alkyl chlorides are converted into alkyl iodides by heating with NaI in dry acetone.", True,
          "The NaCl formed is precipitated in dry acetone, which drives the reaction forward according to Le "
          "Chatelier's principle.", True, explains=True),
      "Finkelstein reaction",
      "R–Cl + NaI ⇌ R–I + NaCl is an equilibrium. In dry acetone NaI is soluble but NaCl is not; as NaCl "
      "precipitates, it is removed from the equilibrium, so the reaction goes to completion. R explains A.",
      ["Halogen exchange (Finkelstein)", "Removal of NaCl as a precipitate shifts the equilibrium to the right"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', halogen exchange", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "statement_pair",
      *sp("Alkyl bromides can be prepared from alcohols using red phosphorus and bromine, which generate PBr₃ in "
          "situ.", True,
          "Primary alcohols are converted into alkyl chlorides simply by shaking with concentrated HCl at room "
          "temperature, without any catalyst.", False),
      "Preparing haloalkanes from alcohols",
      "PBr₃ and PI₃ are usually generated in situ by the reaction of red phosphorus with bromine or iodine. Only "
      "tertiary alcohols react with concentrated HCl at room temperature; primary and secondary alcohols need "
      "anhydrous ZnCl₂ as catalyst (and heating).",
      ["Statement I: true", "Statement II: false; this works only for tertiary alcohols"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=40),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "multi_statement",
      *ms("Which of the following statements about polyhalogen compounds are correct?",
          [("Chloroform is used as a solvent for fats, alkaloids and iodine.", True),
           ("In the stratosphere, freons initiate radical chain reactions that upset the natural ozone balance.",
            True),
           ("Iodoform is now widely preferred as an antiseptic because of its pleasant smell.", False),
           ("Dichloromethane is used as a propellant in aerosols and as a process solvent in the manufacture of "
            "drugs.", True),
           ("DDT has been used to kill mosquitoes that spread malaria and lice that carry typhus.", True)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "d", "e"]], "C"),
      "Uses and environmental effects of polyhalogen compounds",
      "NCERT: chloroform is a solvent for fats, alkaloids and iodine; freons that reach the stratosphere start "
      "radical chain reactions upsetting the ozone balance; dichloromethane is a paint remover, aerosol propellant "
      "and process solvent for drugs; DDT was used against malaria-spreading mosquitoes and typhus-carrying lice. "
      "Iodoform has an objectionable smell and has been replaced by other iodine formulations.",
      ["(a) true", "(b) true", "(c) false: objectionable smell", "(d) true", "(e) true"],
      why_others_wrong="Options containing (c) accept the wrong claim about iodoform; (a), (d) and (e) only leaves "
                       "out the role of freons in ozone depletion.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=60),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "Considering all the structural isomers of the monobromoalkane C₅H₁₁Br, how many of them are secondary (2°) "
      "alkyl bromides?",
      ["1", "2", v_2441, "4"], "C", v_2441,
      "Classifying isomeric haloalkanes",
      "C₅H₁₁Br has eight structural isomers. An alkyl halide is secondary when the carbon carrying the halogen is "
      "bonded to two other carbon atoms.",
      ["1°: 1-bromopentane, 1-bromo-2-methylbutane, 1-bromo-3-methylbutane, 1-bromo-2,2-dimethylpropane (4)",
       "2°: 2-bromopentane, 3-bromopentane, 2-bromo-3-methylbutane (3)", "3°: 2-bromo-2-methylbutane (1)"],
      why_others_wrong="2 usually misses the branched 2-bromo-3-methylbutane; 4 counts 2-bromo-2-methylbutane, which "
                       "is tertiary; 1 counts only the tertiary bromide.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification of haloalkanes", seconds=90),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "Which of the following reacts fastest with OH⁻ ions by the SN2 mechanism?",
      ["1-Bromo-2,2-dimethylpropane, (CH₃)₃C–CH₂Br", "2-Bromopentane", "2-Bromo-2-methylbutane", "1-Bromopentane"],
      "D",
      "Steric hindrance in SN2 reactions",
      "In SN2 the nucleophile attacks the carbon from the side opposite the leaving group, in a single step. Bulky "
      "groups on or next to that carbon hinder the attack. 1-Bromopentane is primary with an unbranched chain, so "
      "it is attacked most easily.",
      ["1-Bromopentane: 1°, unhindered → fastest", "2-Bromopentane: 2° → slower",
       "2-Bromo-2-methylbutane: 3° → very slow by SN2",
       "(CH₃)₃C–CH₂Br: 1°, but the bulky tert-butyl group next to the reacting carbon hinders attack"],
      why_others_wrong="Neopentyl bromide is primary, but the adjacent tert-butyl group blocks the back-side approach; "
                       "secondary and tertiary bromides are more crowded at the reacting carbon itself.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN2 mechanism: steric effects", seconds=60),

    Q(T_HX, "SN1 and SN2", "Advanced", "assertion_reason",
      *ar("SN1 reactions of alkyl halides are favoured by non-polar solvents.", False,
          "In SN1 reactions, polar protic solvents stabilise the carbocation and the leaving halide ion by "
          "solvation.", True),
      "Solvent effects in SN1 reactions",
      "The slow step of SN1 is the ionisation of R–X into R⁺ and X⁻. Polar protic solvents such as water, alcohols "
      "and ethanoic acid help this step by solvating both ions, so SN1 reactions are generally carried out in "
      "polar protic solvents. A is false; R is true.",
      ["A: false; SN1 needs polar protic solvents", "R: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=40),

    Q(T_HX, "SN1 and SN2", "Advanced", "multi_statement",
      *ms("Which of the following statements about dehydrohalogenation (β-elimination) are correct?",
          [("2-Bromo-2-methylbutane, heated with alcoholic KOH, gives mainly 2-methylbut-2-ene.", True),
           ("1-Bromobutane, heated with alcoholic KOH, gives but-1-ene.", True),
           ("A tertiary alkyl halide treated with a strong base mainly undergoes SN2 substitution.", False),
           ("1-Bromo-2,2-dimethylpropane, (CH₃)₃C–CH₂Br, cannot undergo β-elimination, because its β-carbon "
            "carries no hydrogen atom.", True),
           ("In dehydrohalogenation, the halogen and a hydrogen atom are removed from the same carbon atom.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "B"),
      "β-Elimination and Zaitsev's rule",
      "In β-elimination, H is lost from the β-carbon (next to the carbon bearing X). Zaitsev's rule: the alkene with "
      "more alkyl groups on the doubly bonded carbons is preferred. A tertiary halide with a strong base prefers "
      "elimination. In neopentyl bromide the only β-carbon is a quaternary carbon with no hydrogen.",
      ["(a) true (Zaitsev product)", "(b) true (only one kind of β-H)", "(c) false: elimination is preferred",
       "(d) true", "(e) false: H comes from the β-carbon"],
      why_others_wrong="Options with (c) ignore the competition that favours elimination for 3° halides; the option "
                       "with (e) describes an α-elimination, which is not dehydrohalogenation.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions", seconds=75),
]
