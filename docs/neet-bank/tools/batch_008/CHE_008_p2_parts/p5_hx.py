
# ================================================================ Organic Compounds Containing Halogens (1932-1944)
# 1933: C6H5Cl + CH3Cl + 2Na -> C6H5CH3 ; 11.25 g chlorobenzene
n_1933 = F(1125, 100) / mm(C=6, H=5, Cl=1)
assert n_1933 == F(1, 10)
v_1933 = g(n_1933 * mm(C=7, H=8))
assert v_1933 == "9.2 g" and g(n_1933 / 2 * mm(C=12, H=10)) == "7.7 g"
# 1936: 3CCl4 + 2SbF3 -> 3CCl2F2 + 2SbCl3 ; 15.4 g CCl4
n_1936 = F(154, 10) / mm(C=1, Cl=4)
assert n_1936 == F(1, 10)
v_1936 = g(n_1936 * mm(C=1, Cl=2) + n_1936 * 2 * 19)
assert v_1936 == "12.1 g"
# 1941: SN1 first order, k = 6.93e-4 s^-1, ln2 = 0.693 -> t1/2 = 1000 s; 25 % left after 2 half-lives
t_half = 0.693 / 6.93e-4
assert abs(t_half - 1000) < 1e-6
v_1941 = f"{round(2 * t_half)} s"
assert v_1941 == "2000 s"
# 1942: C6H5Br -> C6H5MgBr -> (CO2, H3O+) C6H5COOH ; 7.85 g bromobenzene
n_1942 = F(785, 100) / mm(C=6, H=5, Br=1)
assert n_1942 == F(5, 100)
v_1942 = g(n_1942 * mm(C=7, H=6, O=2))
assert v_1942 == "6.1 g" and g(n_1942 * mm(C=6, H=6)) == "3.9 g"

QUESTIONS += [
    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "Primary and secondary alcohols are converted into alkyl chlorides by heating with concentrated hydrochloric "
      "acid in the presence of:",
      ["Anhydrous ZnCl₂", "Red phosphorus", "Aqueous NaOH", "Dry ether"], "A",
      "Preparation of haloalkanes from alcohols",
      "Anhydrous zinc chloride is used with concentrated HCl to replace the –OH group of primary and secondary "
      "alcohols by –Cl; tertiary alcohols react with concentrated HCl simply by shaking at room temperature.",
      ["R–OH + HCl (ZnCl₂) → R–Cl + H₂O"],
      why_others_wrong="Red phosphorus is used with bromine or iodine (to give PBr₃/PI₃ in situ); aqueous NaOH would "
                       "hydrolyse an alkyl halide back to the alcohol; dry ether is the solvent for Grignard and Wurtz "
                       "reactions.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=25),

    N(T_HX, "C-X bond and preparation", "Basic",
      "Chlorobenzene is treated with chloromethane and sodium in dry ether (Wurtz–Fittig reaction):\n"
      "C₆H₅Cl + CH₃Cl + 2Na → C₆H₅CH₃ + 2NaCl\n"
      "The mass of toluene formed from 11.25 g of chlorobenzene, assuming complete conversion, is (C = 12, H = 1, "
      "Cl = 35.5):",
      ["7.7 g", "18.4 g", "4.6 g", "9.2 g"], "D", v_1933,
      "Wurtz–Fittig reaction",
      "One mole of chlorobenzene gives one mole of toluene.",
      ["M(C₆H₅Cl) = 112.5 g mol⁻¹ → n = 0.10 mol", "n(toluene) = 0.10 mol", "Mass = 0.10 × 92 = 9.2 g"],
      why_others_wrong="7.7 g is the biphenyl that the Fittig reaction (two aryl halides) would give; 18.4 g and 4.6 g "
                       "double or halve the 1 : 1 ratio.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes with metals", seconds=40),

    Q(T_HX, "C-X bond and preparation", "Basic", "statement_pair",
      *sp("Free-radical halogenation of alkanes is not a good method for preparing a particular haloalkane, because it "
          "gives a mixture of isomeric mono- and polyhaloalkanes.", True,
          "Ethene reacts with hydrogen chloride to give chloroethane.", True),
      "Preparation of haloalkanes from hydrocarbons",
      "Chlorination of an alkane such as butane gives several monochloro isomers and polychloro products that are "
      "hard to separate, so the method is unsuitable for a pure product (Statement I true). Hydrogen halides add to "
      "alkenes: CH₂=CH₂ + HCl → CH₃CH₂Cl (Statement II true).",
      ["Alkane + Cl₂ (light) → mixture", "CH₂=CH₂ + HCl → CH₃CH₂Cl"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes", seconds=30),

    Q(T_HX, "SN1 and SN2", "Basic", "multi_statement",
      *ms("Which of the following statements about optical activity are correct?",
          [("A racemic mixture shows zero optical rotation.", True),
           ("The two enantiomers of a compound rotate plane-polarised light by equal amounts but in opposite "
            "directions.", True),
           ("Butan-2-ol is a chiral molecule.", True),
           ("A laevorotatory compound is indicated by the sign (+) before its name.", False),
           ("Propan-2-ol is a chiral molecule.", False)],
          [["a", "b"], ["a", "c", "e"], ["b", "c", "d"]], "B"),
      "Chirality and optical rotation",
      "In a racemic mixture the rotation due to one enantiomer is cancelled by the other. Butan-2-ol has a carbon "
      "bonded to H, OH, CH₃ and C₂H₅, so it is chiral; propan-2-ol's C-2 carries two CH₃ groups. Laevorotatory "
      "compounds carry the sign (−); dextrorotatory ones (+).",
      ["(a) true", "(b) true", "(c) true", "(d) false: (−) for laevo", "(e) false: two identical CH₃ groups"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', optical isomerism", seconds=40),

    N(T_HX, "Polyhalogen compounds", "Intermediate",
      "Freon-12 is made from tetrachloromethane by the Swarts reaction:\n"
      "3CCl₄ + 2SbF₃ → 3CCl₂F₂ + 2SbCl₃\n"
      "The mass of CCl₂F₂ obtained from 15.4 g of CCl₄, assuming complete conversion, is (C = 12, Cl = 35.5, "
      "F = 19):",
      ["13.8 g", "10.5 g", "12.1 g", "8.1 g"], "C", v_1936,
      "Stoichiometry of the Swarts reaction",
      "CCl₄ and CCl₂F₂ are in the mole ratio 3 : 3, i.e. 1 : 1.",
      ["n(CCl₄) = 15.4/154 = 0.10 mol", "n(CCl₂F₂) = 0.10 mol", "M(CCl₂F₂) = 12 + 71 + 38 = 121 g mol⁻¹",
       "Mass = 12.1 g"],
      why_others_wrong="13.8 g is for CCl₃F (one F only); 10.5 g is for CClF₃ (three F); 8.1 g wrongly uses the "
                       "2 : 3 ratio of SbF₃ to CCl₂F₂ for CCl₄.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds: freons", seconds=50),

    Q(T_HX, "SN1 and SN2", "Intermediate", "assertion_reason",
      *ar("An SN2 reaction at a chiral carbon atom gives a product with the inverted configuration.", True,
          "In an SN2 reaction the nucleophile attacks the carbon atom from the side opposite to the leaving group.",
          True, explains=True),
      "Stereochemistry of SN2 reactions",
      "Because the nucleophile approaches from the back, the other three groups are pushed over to the other side as "
      "the leaving group departs, like an umbrella turning inside out. This backside attack is why the configuration "
      "is inverted. R explains A.",
      ["Backside attack", "Transition state: Nu···C···X", "Three groups flip → inversion"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN2 mechanism and stereochemistry", seconds=30),

    Q(T_HX, "SN1 and SN2", "Intermediate", "match_list",
      *ml("Match the reaction of haloalkanes in List-I with its feature in List-II.",
          ["SN2 reaction", "SN1 reaction", "β-Elimination (dehydrohalogenation)", "Reaction with magnesium in dry ether"],
          ["Carbocation intermediate; racemisation of a chiral substrate",
           "Organometallic product with a polar carbon–magnesium bond",
           "Alkene formed by loss of HX from adjacent carbon atoms",
           "Single step with inversion of configuration"],
          "IV I III II", ["I IV III II", "IV III I II", "IV I II III"], "D"),
      "Reactions of haloalkanes",
      "SN2 is concerted with inversion; SN1 goes through a planar carbocation and racemises a chiral substrate; "
      "β-elimination removes H from the β-carbon and X from the α-carbon to give an alkene; Mg in dry ether gives "
      "the Grignard reagent R–MgX.",
      ["SN2 → IV", "SN1 → I", "β-Elimination → III", "Mg/dry ether → II"],
      why_others_wrong="The other codes swap SN1 and SN2, or the elimination and Grignard entries.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', chemical reactions of haloalkanes", seconds=40),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "statement_pair",
      *sp("Iodoform was used earlier as an antiseptic, but because of its objectionable smell it has been replaced by "
          "other formulations containing iodine.", True,
          "Freons are extremely stable, unreactive, non-toxic, non-corrosive and easily liquefiable gases.", True),
      "Polyhalogen compounds",
      "Both statements follow NCERT's account: iodoform's antiseptic action comes from free iodine, but its smell led "
      "to its replacement; freons (chlorofluorocarbons) are stable, non-toxic, non-corrosive, easily liquefied gases, "
      "which is why they were used in refrigeration and aerosol propellants.",
      ["Iodoform: antiseptic, replaced due to smell → true", "Freons: stable, unreactive, easily liquefied → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=35),

    Q(T_HX, "SN1 and SN2", "Intermediate", "multi_statement",
      *ms("Which of the following statements about 2-bromo-2-methylpropane, (CH₃)₃C–Br, are correct?",
          [("It is a secondary alkyl halide.", False),
           ("Its hydrolysis in water takes place mainly by the SN1 mechanism.", True),
           ("The rate of its SN1 hydrolysis does not depend on the concentration of the nucleophile.", True),
           ("When heated with alcoholic KOH it gives 2-methylpropene.", True),
           ("Its hydrolysis by SN2 gives a product with inverted configuration at a chiral carbon.", False)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["c", "d"]], "B"),
      "Behaviour of a tertiary alkyl halide",
      "The C–Br carbon is bonded to three carbons, so the halide is tertiary. Tertiary halides react by SN1, whose "
      "rate depends only on [RX]. With alcoholic KOH they undergo β-elimination to (CH₃)₂C=CH₂. The molecule has no "
      "chiral carbon (three identical CH₃ groups) and is too hindered for SN2.",
      ["(a) false: tertiary", "(b) true", "(c) true", "(d) true", "(e) false: no chiral carbon; SN2 is hindered"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism and elimination", seconds=55),

    N(T_HX, "SN1 and SN2", "Advanced",
      "The hydrolysis of 2-bromo-2-methylpropane in a large excess of water follows the SN1 mechanism, with "
      "rate = k[(CH₃)₃CBr] and k = 6.93 × 10⁻⁴ s⁻¹ at a certain temperature. The time taken for 75% of the alkyl "
      "bromide to react is (ln 2 = 0.693):",
      ["1000 s", "2000 s", "4000 s", "500 s"], "B", v_1941,
      "First-order kinetics of an SN1 reaction",
      "An SN1 reaction is first order in the alkyl halide, so its half-life is constant: t½ = 0.693/k. 75% reaction "
      "means 25% left, i.e. two half-lives.",
      ["t½ = 0.693 / (6.93 × 10⁻⁴) = 1000 s", "100% → 50% → 25%: two half-lives", "t = 2 × 1000 = 2000 s"],
      why_others_wrong="1000 s is one half-life (50% reaction); 4000 s is four half-lives; 500 s halves t½.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism (first-order rate)", seconds=60),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "7.85 g of bromobenzene is converted completely into phenylmagnesium bromide in dry ether. The Grignard reagent "
      "is treated with dry ice (solid CO₂) and the product is hydrolysed with dilute acid. Assuming every step is "
      "complete, the mass of the organic acid obtained is (C = 12, H = 1, O = 16, Br = 80):",
      ["12.2 g", "3.9 g", "6.8 g", "6.1 g"], "D", v_1942,
      "Grignard reagent + CO₂ → carboxylic acid",
      "C₆H₅Br → C₆H₅MgBr → (CO₂) C₆H₅COOMgBr → (H₃O⁺) C₆H₅COOH. One mole of bromobenzene gives one mole of benzoic "
      "acid.",
      ["n(C₆H₅Br) = 7.85/157 = 0.05 mol", "n(C₆H₅COOH) = 0.05 mol", "Mass = 0.05 × 122 = 6.1 g"],
      why_others_wrong="12.2 g takes 0.10 mol; 3.9 g is the benzene formed if the Grignard reagent were hydrolysed by "
                       "water before reacting with CO₂; 6.8 g is the mass of phenylethanoic acid (M = 136), which would "
                       "need one more carbon atom than CO₂ supplies.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', Grignard reagents; 'Aldehydes, Ketones and Carboxylic Acids', "
            f"preparation of carboxylic acids", seconds=60),

    Q(T_HX, "C-X bond and preparation", "Advanced", "direct",
      "Propene is treated with HBr in the presence of benzoyl peroxide to give X. X is heated with ethanolic KCN to "
      "give Y, and Y is reduced with lithium aluminium hydride to give Z. Z is:",
      ["Propan-1-amine", "2-Methylpropan-1-amine", "Butan-1-amine", "N-Propylmethanamine"], "C",
      "Anti-Markovnikov addition, nucleophilic substitution by CN⁻ and reduction of nitriles",
      "With peroxide, HBr adds anti-Markovnikov: X = CH₃CH₂CH₂Br. KCN gives the nitrile Y = CH₃CH₂CH₂CN (one carbon "
      "added). LiAlH₄ reduces –C≡N to –CH₂NH₂: Z = CH₃CH₂CH₂CH₂NH₂.",
      ["X: 1-bromopropane", "Y: butanenitrile", "Z: butan-1-amine"],
      why_others_wrong="2-Methylpropan-1-amine would come from 2-bromopropane (no peroxide); propan-1-amine forgets the "
                       "carbon added by cyanide; N-propylmethanamine would come from an isocyanide, which forms with "
                       "AgCN, not KCN.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution; 'Amines', reduction of nitriles",
      seconds=60),

    Q(T_HX, "SN1 and SN2", "Advanced", "assertion_reason",
      *ar("Tertiary alkyl halides undergo SN1 reactions faster than primary alkyl halides.", True,
          "An SN1 reaction takes place in a single step without forming any intermediate.", False),
      "SN1 mechanism and carbocation stability",
      "SN1 takes place in two steps: slow ionisation of R–X to a carbocation, then fast attack of the nucleophile. "
      "The more stable the carbocation (3° > 2° > 1°), the faster the reaction, so A is true. R describes an SN2 "
      "reaction and is false.",
      ["Step 1 (slow): R–X → R⁺ + X⁻", "Step 2 (fast): R⁺ + Nu⁻ → R–Nu", "3° carbocation most stable → A true",
       "R false: SN1 has a carbocation intermediate"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=35),
]
