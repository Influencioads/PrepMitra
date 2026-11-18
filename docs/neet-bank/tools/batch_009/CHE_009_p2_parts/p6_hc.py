
# ================================================================ Hydrocarbons (2183-2196)
# 2184: C2H5Cl + H2 (Zn, H+) -> C2H6 + HCl
n_2184 = F(645, 100) / mm(C=2, H=5, Cl=1)
assert n_2184 == F(1, 10)
v_2184 = g(n_2184 * mm(C=2, H=6))
assert v_2184 == "3.0 g"
# 2187: CH3C=CH + 2HBr -> CH3CBr2CH3
n_2187 = F(4) / mm(C=3, H=4)
v_2187 = g(2 * n_2187 * mm(H=1, Br=1))
assert n_2187 == F(1, 10) and v_2187 == "16.2 g"
# 2188: terminal alkynes (acidic H on sp carbon)
alkynes = {"ethyne": True, "propyne": True, "but-1-yne": True, "but-2-yne": False, "pent-2-yne": False,
           "3-methylbut-1-yne": True}
v_2188 = str(sum(alkynes.values()))
assert v_2188 == "4"
# 2193: (CH3)2C=CH-CH3 + [O] (KMnO4/H+) -> (CH3)2CO + CH3COOH
n_2193 = F(7) / mm(C=5, H=10)
v_2193 = g(n_2193 * mm(C=3, H=6, O=1))
assert n_2193 == F(1, 10) and v_2193 == "5.8 g" and g(n_2193 * mm(C=2, H=4, O=2)) == "6.0 g"

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "In the conformations of ethane, the repulsive interaction between the electron clouds of the C–H bonds on the "
      "two carbon atoms, which affects the stability of a conformation, is called:",
      ["Torsional strain", "Angle strain", "Steric inhibition of resonance", "Hyperconjugation"], "A",
      "Torsional strain in ethane",
      "When the C–H bonds of the two carbons face each other (eclipsed form) their electron clouds repel most. NCERT "
      "calls this repulsion torsional strain; it is least in the staggered form, which is therefore more stable.",
      ["Eclipsed: maximum torsional strain", "Staggered: minimum torsional strain",
       "Energy difference about 12.5 kJ mol⁻¹"],
      why_others_wrong="Angle strain arises from distorted bond angles in small rings; steric inhibition of resonance "
                       "and hyperconjugation are electronic effects, not this repulsion.",
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane", seconds=25),

    N(T_HC, "Alkanes and conformations", "Basic",
      "Alkyl halides (other than fluorides) are reduced to alkanes by zinc and dilute hydrochloric acid. The mass of "
      "ethane obtained from 6.45 g of chloroethane, assuming complete conversion, is (C = 12, H = 1, Cl = 35.5):",
      ["1.5 g", v_2184, "6.0 g", "2.8 g"], "B", v_2184,
      "Preparation of alkanes by reduction of alkyl halides",
      "Each chloroethane molecule gives one ethane molecule: CH₃CH₂Cl + H₂ (Zn, H⁺) → CH₃CH₃ + HCl.",
      ["Molar mass of C₂H₅Cl = 64.5 g mol⁻¹; n = 6.45/64.5 = 0.10 mol", "n(C₂H₆) = 0.10 mol",
       "Mass = 0.10 × 30 = 3.0 g"],
      why_others_wrong="1.5 g and 6.0 g use a 1 : 2 or 2 : 1 ratio, as in the Wurtz reaction; 2.8 g is the mass of "
                       "ethene, not ethane.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes from alkyl halides", seconds=40),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "assertion_reason",
      *ar("Propene reacts with cold, dilute, aqueous alkaline KMnO₄ (Baeyer's reagent) to give propane-1,2-diol.", True,
          "Propene is a gas at room temperature.", True),
      "Oxidation of alkenes by Baeyer's reagent",
      "Cold dilute alkaline KMnO₄ adds two –OH groups across the C=C bond (the purple colour is discharged), giving "
      "the vicinal glycol CH₃CH(OH)CH₂OH. R is a correct physical fact about propene, but its being a gas has nothing "
      "to do with this reaction.",
      ["CH₃–CH=CH₂ + H₂O + [O] → CH₃–CH(OH)–CH₂OH", "R: true, unrelated to the reaction"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: oxidation", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "statement_pair",
      *sp("Among the alkenes, the first three members are gases, the next fourteen are liquids and the higher members "
          "are solids.", True,
          "Alkenes are highly soluble in water.", False),
      "Physical properties of alkenes",
      "NCERT describes the physical state of alkenes exactly as in Statement I. Alkenes, like alkanes, are non-polar "
      "or weakly polar and are insoluble in water but soluble in non-polar organic solvents.",
      ["Statement I: true", "Statement II: false; alkenes are insoluble in water"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: physical properties", seconds=25),

    N(T_HC, "Alkynes", "Intermediate",
      "Propyne reacts with an excess of HBr (no peroxide) to give 2,2-dibromopropane. The minimum mass of HBr needed "
      "for 4.0 g of propyne is (C = 12, H = 1, Br = 80):",
      ["8.1 g", "32.4 g", "16.0 g", v_2187], "D", v_2187,
      "Addition of two molecules of HX to an alkyne",
      "The triple bond takes up two molecules of HBr, both following Markovnikov's rule: CH₃C≡CH → CH₃CBr=CH₂ → "
      "CH₃CBr₂CH₃.",
      ["Molar mass of propyne = 40 g mol⁻¹; n = 4.0/40 = 0.10 mol", "HBr needed = 2 × 0.10 = 0.20 mol",
       "Mass = 0.20 × 81 = 16.2 g"],
      why_others_wrong="8.1 g adds only one HBr; 32.4 g adds four; 16.0 g is the mass of Br₂ for one addition, not HBr.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of hydrogen halides", seconds=45),

    N(T_HC, "Alkynes", "Intermediate",
      "How many of the following react with sodamide (NaNH₂) to form a sodium salt?\n"
      "Ethyne, propyne, but-1-yne, but-2-yne, pent-2-yne, 3-methylbut-1-yne",
      ["2", "3", v_2188, "5"], "C", v_2188,
      "Acidic character of terminal alkynes",
      "Only a hydrogen attached to a triply bonded carbon is acidic enough to be removed by NaNH₂. The sp carbon has "
      "50% s character and holds the bonding pair close to itself. Internal alkynes have no such hydrogen.",
      ["Terminal (≡C–H present): ethyne, propyne, but-1-yne, 3-methylbut-1-yne",
       "Internal: but-2-yne, pent-2-yne", "Count = 4"],
      why_others_wrong="2 or 3 leave out ethyne or the branched terminal alkyne; 5 counts an internal alkyne.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: acidic character", seconds=40),

    Q(T_HC, "Alkynes", "Intermediate", "direct",
      "Which of the following is the correct order of acidic character?",
      ["CH₃–C≡CH > HC≡CH > CH₃–C≡C–CH₃", "CH₃–C≡C–CH₃ > CH₃–C≡CH > HC≡CH", "HC≡CH > CH₃–C≡C–CH₃ > CH₃–C≡CH",
       "HC≡CH > CH₃–C≡CH ≫ CH₃–C≡C–CH₃"], "D",
      "Acidity of alkynes",
      "Acidity comes from H attached to the sp carbon. Ethyne has two such hydrogens; in propyne the electron-releasing "
      "methyl group lowers the acidity; but-2-yne has no acetylenic hydrogen and is far less acidic.",
      ["Ethyne: two ≡C–H, no alkyl group", "Propyne: one ≡C–H, +I methyl group", "But-2-yne: no ≡C–H"],
      why_others_wrong="Placing propyne above ethyne ignores the +I effect of CH₃; placing but-2-yne high ignores that it "
                       "has no hydrogen on an sp carbon.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: acidic character of alkyne", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with the type of reaction it is in List-II.",
          ["CH₄ + Cl₂ in diffused sunlight → CH₃Cl + HCl", "C₆H₆ + CH₃Cl (anhydrous AlCl₃) → C₆H₅CH₃ + HCl",
           "CH₂=CH₂ + HBr → CH₃CH₂Br", "CH₃CH=CH₂ + HBr (benzoyl peroxide) → CH₃CH₂CH₂Br"],
          ["Free radical addition", "Electrophilic addition", "Electrophilic substitution",
           "Free radical substitution"],
          "IV III II I", ["IV II III I", "III IV I II", "IV III I II"], "A"),
      "Classifying reactions of hydrocarbons by mechanism",
      "Halogenation of alkanes in light is a free radical chain substitution. Friedel–Crafts alkylation substitutes an "
      "H of benzene through the electrophile formed with AlCl₃. HBr adds to ethene through a carbocation (electrophilic "
      "addition), whereas in the presence of a peroxide it adds to propene through bromine free radicals.",
      ["Chlorination of methane: free radical substitution (IV)", "Friedel–Crafts: electrophilic substitution (III)",
       "HBr + ethene: electrophilic addition (II)", "HBr + propene with peroxide: free radical addition (I)"],
      why_others_wrong="Codes that call Friedel–Crafts an addition, or that treat the peroxide reaction as ionic, mix "
                       "up the mechanisms.",
      ncert=f"{NC11}, 'Hydrocarbons', reactions of alkanes, alkenes and arenes", seconds=45),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "multi_statement",
      *ms("Which of the following give benzene or a benzene derivative as stated?",
          [("Ethyne passed through a red-hot iron tube at 873 K gives benzene.", True),
           ("Sodium benzoate heated with soda lime gives benzene.", True),
           ("Phenol vapour passed over heated zinc dust gives benzene.", True),
           ("Benzene treated with CH₃Cl and anhydrous AlCl₃ gives toluene.", True),
           ("Benzene treated with chlorine in ultraviolet light gives chlorobenzene by substitution.", False)],
          [["a", "b", "e"], ["b", "c", "d", "e"], ["a", "c", "e"]], "D"),
      "Preparation and reactions of benzene",
      "Benzene is made by cyclic polymerisation of ethyne, by decarboxylation of sodium benzoate with soda lime, and by "
      "reduction of phenol with zinc dust. Friedel–Crafts alkylation with CH₃Cl gives toluene. In ultraviolet light, "
      "however, benzene adds three molecules of chlorine to give benzene hexachloride, C₆H₆Cl₆; this is addition, "
      "not substitution.",
      ["(a) 3HC≡CH → C₆H₆: true", "(b) C₆H₅COONa + NaOH (CaO) → C₆H₆ + Na₂CO₃: true",
       "(c) C₆H₅OH + Zn → C₆H₆ + ZnO: true", "(d) Friedel–Crafts alkylation: true",
       "(e) false: UV light gives addition (C₆H₆Cl₆)"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: preparation and chemical properties", seconds=55),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "statement_pair",
      *sp("Aromatic hydrocarbons burn with a sooty flame.", True,
          "Aromatic hydrocarbons are immiscible with water but are readily miscible with organic solvents.", True),
      "Physical properties of arenes",
      "NCERT lists both properties: arenes are non-polar, usually colourless liquids or solids with a characteristic "
      "aroma, immiscible with water and miscible with organic solvents, and they burn with a sooty flame.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: physical properties", seconds=25),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "An open-chain alkene X, C₅H₁₀, is oxidised by acidic potassium permanganate to give a mixture of propanone and "
      "ethanoic acid only. The mass of propanone obtained from 7.0 g of X, assuming complete reaction, is "
      "(C = 12, H = 1, O = 16):",
      [v_2193, "6.0 g", "2.9 g", "11.6 g"], "A", v_2193,
      "Oxidative cleavage of alkenes by acidic KMnO₄",
      "Acidic KMnO₄ breaks the C=C bond: a carbon carrying two alkyl groups ends up as a ketone, and a carbon carrying "
      "one alkyl group and one H ends up as a carboxylic acid. Propanone plus ethanoic acid points to "
      "(CH₃)₂C=CH–CH₃, 2-methylbut-2-ene.",
      ["(CH₃)₂C= → (CH₃)₂C=O (propanone); =CH–CH₃ → CH₃COOH", "X = 2-methylbut-2-ene, M = 70 g mol⁻¹",
       "n(X) = 7.0/70 = 0.10 mol → 0.10 mol propanone", "Mass = 0.10 × 58 = 5.8 g"],
      why_others_wrong="6.0 g is the mass of ethanoic acid; 2.9 g halves the moles; 11.6 g assumes two propanone units "
                       "per molecule, as for 2,3-dimethylbut-2-ene (C₆H₁₂).",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: oxidation with acidic KMnO₄", seconds=90),

    Q(T_HC, "Alkanes and conformations", "Advanced", "assertion_reason",
      *ar("The staggered and eclipsed conformations of ethane cannot be separated and isolated at room temperature.",
          True,
          "The energy barrier to rotation about the C–C single bond of ethane is only about 12.5 kJ mol⁻¹, so the "
          "conformations change into one another rapidly.", True, explains=True),
      "Interconversion of conformations",
      "Conformations differ only by rotation about a σ bond. For ethane the difference in energy between the staggered "
      "and eclipsed forms is so small that ordinary thermal energy keeps them interconverting, so they cannot be "
      "separated. R gives the reason.",
      ["Rotation barrier ≈ 12.5 kJ mol⁻¹ (small)", "Rapid interconversion at room temperature",
       "→ not separable"],
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane: relative stability", seconds=35),

    Q(T_HC, "Alkynes", "Advanced", "direct",
      "An alkyne X, C₄H₆, does not react with sodamide. X is hydrogenated with H₂ over palladium on charcoal partly "
      "deactivated with quinoline, giving Y, which shows geometrical isomerism. Y is subjected to ozonolysis (O₃, then "
      "Zn/H₂O). The product is:",
      ["Propanal and methanal", "Butan-2-one", "Ethanal only", "Butanal"], "C",
      "Identifying an internal alkyne and following it through reduction and ozonolysis",
      "An alkyne C₄H₆ with no acidic hydrogen must be the internal alkyne but-2-yne. Lindlar-type hydrogenation stops "
      "at the alkene and gives cis-but-2-ene (which has cis and trans forms). Ozonolysis cleaves CH₃CH=CHCH₃ into two "
      "molecules of ethanal.",
      ["X: CH₃–C≡C–CH₃ (no ≡C–H)", "Y: cis-CH₃CH=CHCH₃", "Ozonolysis: 2 CH₃CHO"],
      why_others_wrong="Propanal and methanal come from but-1-ene, which would arise from but-1-yne (which reacts with "
                       "NaNH₂); butan-2-one and butanal come from hydration, not ozonolysis.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes and alkenes: reactions", seconds=60),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "match_list",
      *ml("Match the reaction in List-I with its main product in List-II.",
          ["Ethyne + H₂ (Pd/charcoal deactivated with quinoline)", "But-2-yne + sodium in liquid ammonia",
           "Ethene + H₂ (finely divided Ni)", "Benzene + H₂ (Ni, high temperature and pressure)"],
          ["Cyclohexane", "Ethane", "trans-But-2-ene", "Ethene"],
          "IV III II I", ["II III IV I", "IV I II III", "II I IV III"], "D"),
      "Controlled and complete hydrogenation",
      "The deactivated (Lindlar-type) catalyst stops the reduction of an alkyne at the alkene. Sodium in liquid "
      "ammonia also stops at the alkene but gives the trans isomer. Ordinary metal catalysts saturate C=C fully, and "
      "benzene adds three H₂ only under vigorous conditions.",
      ["Ethyne → ethene (IV)", "But-2-yne → trans-but-2-ene (III)", "Ethene → ethane (II)",
       "Benzene → cyclohexane (I)"],
      why_others_wrong="Codes giving ethane from the deactivated catalyst ignore that the catalyst is poisoned to stop "
                       "at the alkene; cyclohexane does not come from an alkene of two or four carbons.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of hydrogen; arenes: addition reactions", seconds=45),
]
