
# ================================================================ Organic Compounds Containing Oxygen (1945-1964)
# 1945: hydroboration-oxidation: propene (4.2 g) -> propan-1-ol
v_1945 = "Propan-1-ol, " + g(F(42, 10) / mm(C=3, H=6) * mm(C=3, H=8, O=1))
assert v_1945 == "Propan-1-ol, 6.0 g"
# 1946: CH3CHO + H2 -> CH3CH2OH ; 4.4 g ethanal
v_1946 = f"{float(F(44, 10) / mm(C=2, H=4, O=1) * F(224, 10)):.2f} L"
assert v_1946 == "2.24 L"
# 1951: esters from {ethanoic, propanoic} x {methanol, ethanol}
acids, alcohols = ["ethanoic", "propanoic"], ["methyl", "ethyl"]
esters = {f"{al} {ac[:-2]}ate" for ac in acids for al in alcohols}
v_1951 = str(len(esters))
assert v_1951 == "4"
# 1952: (CH3)2CO + H2NCONHNH2 -> (CH3)2C=NNHCONH2 + H2O ; 5.8 g propanone
semi = mm(C=4, H=9, N=3, O=1)
assert semi == mm(C=3, H=6, O=1) + mm(C=1, H=5, N=3, O=1) - mm(H=2, O=1) == 115
v_1952 = g(F(58, 10) / mm(C=3, H=6, O=1) * semi)
assert v_1952 == "11.5 g"
# 1953: Rosenmund: C6H5COCl (140.5) -> C6H5CHO ; 7.025 g
n_1953 = F(7025, 1000) / mm(C=7, H=5, O=1, Cl=1)
assert n_1953 == F(5, 100)
v_1953 = g(n_1953 * mm(C=7, H=6, O=1))
assert v_1953 == "5.3 g"
# 1959: C2H5OH -> CH3CHO -> (CH3MgBr) CH3CH(OH)CH3 -> CH3COCH3 -> CHI3 ; 2.3 g ethanol, 1 : 1 throughout
n_1959 = F(23, 10) / mm(C=2, H=6, O=1)
v_1959 = g(n_1959 * mm(C=1, H=1, I=3))
assert v_1959 == "19.7 g" and g(n_1959 * 3 * 127) == "19.1 g"

QUESTIONS += [
    N(T_OX, "Alcohols", "Basic",
      "4.2 g of propene is treated with diborane and the product is oxidised with alkaline hydrogen peroxide "
      "(hydroboration–oxidation). Assuming complete conversion, the alcohol formed and its mass are (C = 12, H = 1, "
      "O = 16):",
      ["Propan-2-ol, 6.0 g", "Propan-1-ol, 3.0 g", "Propan-1-ol, 6.0 g", "Propan-2-ol, 4.2 g"], "C", v_1945,
      "Hydroboration–oxidation gives the anti-Markovnikov alcohol",
      "In hydroboration–oxidation, water is effectively added so that –OH ends up on the less substituted carbon: "
      "propene gives propan-1-ol. One mole of propene gives one mole of alcohol.",
      ["n(C₃H₆) = 4.2/42 = 0.10 mol", "Product: CH₃CH₂CH₂OH (M = 60)", "Mass = 0.10 × 60 = 6.0 g"],
      why_others_wrong="Propan-2-ol is the product of acid-catalysed hydration (Markovnikov); 3.0 g halves the mole "
                       "ratio; 4.2 g simply repeats the mass of propene and ignores the added H₂O.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols: hydroboration–oxidation", seconds=40),

    N(T_OX, "Aldehydes and ketones", "Basic",
      "4.4 g of ethanal is reduced completely to ethanol by catalytic hydrogenation over nickel. The volume of "
      "hydrogen consumed, measured at STP, is (C = 12, H = 1, O = 16; molar volume at STP = 22.4 L mol⁻¹):",
      ["4.48 L", "2.24 L", "1.12 L", "22.4 L"], "B", v_1946,
      "Reduction of aldehydes to primary alcohols",
      "CH₃CHO + H₂ → CH₃CH₂OH: one mole of H₂ per mole of aldehyde.",
      ["n(CH₃CHO) = 4.4/44 = 0.10 mol", "n(H₂) = 0.10 mol", "V = 0.10 × 22.4 = 2.24 L"],
      why_others_wrong="4.48 L assumes two moles of H₂ per mole of ethanal; 1.12 L halves the ratio; 22.4 L is for "
                       "one whole mole.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols by reduction of aldehydes", seconds=30),

    Q(T_OX, "Carboxylic acids", "Basic", "direct",
      "Methanoic acid (formic acid) gets its common name from the source from which it was first obtained. This "
      "source is:",
      ["Vinegar", "Rancid butter", "Goat fat", "Red ants"], "D",
      "Common names of carboxylic acids",
      "Methanoic acid was first obtained from red ants; its common name comes from the Latin formica, meaning ant.",
      ["formica (Latin) = ant → formic acid"],
      why_others_wrong="Vinegar gives acetic acid (acetum); rancid butter gives butyric acid (butyrum); goat fat gives "
                       "caproic acid.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nomenclature of carboxylic acids", seconds=20),

    Q(T_OX, "Ethers", "Basic", "assertion_reason",
      *ar("Ethanol has a much higher boiling point than its isomer methoxymethane.", True,
          "Ethanol molecules are associated through intermolecular hydrogen bonds, which are absent in "
          "methoxymethane.", True, explains=True),
      "Hydrogen bonding and boiling points of alcohols and ethers",
      "Both have M = 46 g mol⁻¹, but ethanol has an O–H group and forms intermolecular hydrogen bonds; an ether has no "
      "hydrogen on oxygen. Extra energy is needed to break the hydrogen bonds, so ethanol boils much higher. R "
      "explains A.",
      ["Same molar mass", "Ethanol: O–H → intermolecular H-bonds", "Ether: no O–H → only dipole interactions"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties of ethers", seconds=30),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("A primary alcohol can be oxidised to an aldehyde by CrO₃ in an anhydrous medium.", True,
          "Tertiary alcohols are readily oxidised to ketones by CrO₃.", False),
      "Oxidation of alcohols",
      "Using CrO₃ in an anhydrous medium (or PCC) stops the oxidation of a primary alcohol at the aldehyde stage "
      "(Statement I true). Tertiary alcohols have no hydrogen on the carbinol carbon and are not oxidised to "
      "carbonyl compounds by such reagents (Statement II false).",
      ["RCH₂OH → RCHO (CrO₃, anhydrous)", "R₃C–OH: no H on the C–OH carbon → no ketone"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols: oxidation", seconds=30),

    Q(T_OX, "Phenols", "Basic", "multi_statement",
      *ms("Which of the following methods can be used to prepare phenol?",
          [("Heating chlorobenzene with NaOH at 623 K and 300 atm, followed by acidification", True),
           ("Fusing sodium benzenesulphonate with NaOH, followed by acidification", True),
           ("Warming an aqueous solution of benzenediazonium chloride", True),
           ("Air oxidation of cumene to cumene hydroperoxide, followed by treatment with dilute acid", True),
           ("Heating benzene with dilute aqueous NaOH", False)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "d"]], "A"),
      "Preparation of phenols",
      "Phenol is obtained from haloarenes, from benzenesulphonic acid, from diazonium salts and from cumene. Benzene "
      "itself does not react with aqueous NaOH.",
      ["(a) from haloarene: true", "(b) from sulphonic acid: true", "(c) from diazonium salt: true",
       "(d) from cumene: true", "(e) false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of phenols", seconds=45),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "A mixture of ethanoic acid and propanoic acid is heated with a mixture of methanol and ethanol in the presence "
      "of a few drops of concentrated sulphuric acid. How many different esters can be formed?",
      ["2", "4", "3", "6"], "B", v_1951,
      "Esterification: each acid can combine with each alcohol",
      "An ester R–COO–R′ takes its acyl part from the acid and its alkyl part from the alcohol. Two acids × two "
      "alcohols give four combinations.",
      ["Methyl ethanoate", "Ethyl ethanoate", "Methyl propanoate", "Ethyl propanoate", "Total = 4"],
      why_others_wrong="2 pairs each acid with only one alcohol; 3 treats ethyl ethanoate and methyl propanoate (which "
                       "are isomers) as the same compound; 6 counts acid–acid or alcohol–alcohol products as esters.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esterification", seconds=40),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "5.8 g of propanone reacts completely with semicarbazide, H₂N–CO–NH–NH₂, in weakly acidic solution to form "
      "propanone semicarbazone. The mass of the semicarbazone formed is (C = 12, H = 1, N = 14, O = 16):",
      ["13.3 g", "7.2 g", "5.8 g", "11.5 g"], "D", v_1952,
      "Reaction of carbonyl compounds with ammonia derivatives",
      ">C=O + H₂N–Z → >C=N–Z + H₂O. Propanone gives (CH₃)₂C=N–NH–CO–NH₂, C₄H₉N₃O (M = 115).",
      ["n(propanone) = 5.8/58 = 0.10 mol", "M(semicarbazone) = 58 + 75 − 18 = 115 g mol⁻¹",
       "Mass = 0.10 × 115 = 11.5 g"],
      why_others_wrong="13.3 g forgets that water is eliminated; 7.2 g is for the hydrazone (C₃H₈N₂); 5.8 g just "
                       "repeats the mass of propanone.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions with ammonia derivatives", seconds=50),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "7.025 g of benzoyl chloride is hydrogenated over palladium on barium sulphate (Rosenmund reduction). Assuming "
      "complete conversion, the mass of benzaldehyde formed is (C = 12, H = 1, O = 16, Cl = 35.5):",
      ["5.3 g", "5.4 g", "6.1 g", "10.6 g"], "A", v_1953,
      "Rosenmund reduction of acyl chlorides",
      "C₆H₅COCl + H₂ → C₆H₅CHO + HCl. The poisoned catalyst stops the reduction at the aldehyde.",
      ["M(C₆H₅COCl) = 140.5 g mol⁻¹ → n = 0.05 mol", "n(C₆H₅CHO) = 0.05 mol", "Mass = 0.05 × 106 = 5.3 g"],
      why_others_wrong="5.4 g is benzyl alcohol (over-reduction, which the Pd–BaSO₄ catalyst prevents); 6.1 g is "
                       "benzoic acid (hydrolysis); 10.6 g takes 0.10 mol.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes from acyl chlorides",
      seconds=45),

    Q(T_OX, "Ethers", "Intermediate", "direct",
      "Ethyl methyl ether (methoxyethane), CH₃–O–CH₂CH₃, is heated with one equivalent of concentrated HI. The main "
      "products are:",
      ["CH₃CH₂I and CH₃OH", "CH₃I and CH₃I", "CH₃I and CH₃CH₂OH", "CH₃CH₂I and CH₃CH₂OH"], "C",
      "Cleavage of unsymmetrical ethers by HI",
      "The ether oxygen is first protonated. The iodide ion then attacks by SN2, choosing the less hindered (smaller) "
      "alkyl group, so iodomethane and ethanol are formed.",
      ["CH₃–O⁺(H)–C₂H₅ formed", "I⁻ attacks the less hindered CH₃ (SN2)", "→ CH₃I + C₂H₅OH"],
      why_others_wrong="CH₃CH₂I + CH₃OH would need I⁻ to attack the more hindered ethyl group; the other two options "
                       "are not balanced products of a single cleavage.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of ethers: cleavage of the C–O bond", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("Methanal undergoes the Cannizzaro reaction with concentrated alkali.", True,
          "Methanal is a gas at room temperature.", True, explains=False),
      "Cannizzaro reaction",
      "The Cannizzaro reaction is shown by aldehydes that have no α-hydrogen; methanal has none, so it disproportionates "
      "into methanol and methanoate. R is a true physical property of methanal, but it has nothing to do with the "
      "reaction.",
      ["Methanal: no α-H → Cannizzaro (A true)", "Methanal is a gas (R true)", "R does not explain A"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Cannizzaro reaction; physical properties", seconds=30),

    Q(T_OX, "Alcohols", "Intermediate", "statement_pair",
      *sp("Alcohols can act both as Brönsted acids and as Brönsted bases.", True,
          "Sodium ethoxide is a stronger base than sodium hydroxide.", True),
      "Acidic and basic character of alcohols",
      "An alcohol donates the O–H proton (acid) and its oxygen lone pairs accept a proton (base). Alcohols are weaker "
      "acids than water, so the alkoxide ion is a better proton acceptor than hydroxide: sodium ethoxide is a stronger "
      "base than NaOH. Both statements are true.",
      ["R–OH → R–O⁻ + H⁺ (acid)", "R–OH + H⁺ → R–OH₂⁺ (base)", "ROH weaker acid than H₂O → RO⁻ stronger base than OH⁻"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of alcohols", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with its name in List-II.",
          ["An alkyl halide is heated with a sodium alkoxide",
           "An aldehyde having α-hydrogen is treated with dilute NaOH",
           "An aldehyde having no α-hydrogen is heated with concentrated NaOH",
           "A carboxylic acid having α-hydrogen is treated with Cl₂ and a little red phosphorus"],
          ["Cannizzaro reaction", "Hell–Volhard–Zelinsky reaction", "Williamson synthesis", "Aldol reaction"],
          "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "D"),
      "Named reactions of oxygen compounds",
      "Alkoxide + alkyl halide → ether (Williamson); α-H aldehyde + dilute alkali → β-hydroxy aldehyde (aldol); "
      "no α-H aldehyde + concentrated alkali → alcohol + carboxylate (Cannizzaro); α-halogenation of acids with "
      "X₂/red P → HVZ reaction.",
      ["A → Williamson (III)", "B → aldol (IV)", "C → Cannizzaro (I)", "D → HVZ (II)"],
      why_others_wrong="The other codes interchange the aldol and Cannizzaro reactions (which depend on the presence "
                       "or absence of α-H) or the Williamson and HVZ reactions.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers'; 'Aldehydes, Ketones and Carboxylic Acids', named reactions",
      seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Propanal undergoes aldol condensation in the presence of dilute alkali.", True),
           ("2,2-Dimethylpropanal undergoes the Cannizzaro reaction with concentrated alkali.", True),
           ("Benzaldehyde undergoes self aldol condensation with dilute alkali.", False),
           ("The aldol formed from two molecules of propanal is 3-hydroxy-2-methylpentanal.", True),
           ("Ethanal undergoes the Cannizzaro reaction with concentrated alkali.", False)],
          [["a", "b"], ["b", "d", "e"], ["a", "c", "d"]], "C"),
      "α-Hydrogen decides between aldol and Cannizzaro reactions",
      "Aldehydes with α-H (propanal, ethanal) undergo aldol reactions; those without α-H (2,2-dimethylpropanal, "
      "benzaldehyde, methanal) undergo the Cannizzaro reaction. In propanal's aldol, the α-carbanion CH₃CH⁻–CHO adds "
      "to the C=O of a second molecule: CH₃CH₂CH(OH)–CH(CH₃)–CHO, 3-hydroxy-2-methylpentanal.",
      ["(a) true", "(b) true: no α-H", "(c) false: no α-H", "(d) true", "(e) false: has α-H"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol and Cannizzaro reactions", seconds=60),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "2.3 g of ethanol is oxidised with PCC to X. X is treated with CH₃MgBr and the product is hydrolysed to give Y. "
      "Y is oxidised with acidified K₂Cr₂O₇ to Z, and Z is warmed with iodine and aqueous NaOH. Assuming every step "
      "is complete, the mass of iodoform formed is (C = 12, H = 1, O = 16, I = 127):",
      ["39.4 g", "19.7 g", "9.85 g", "19.1 g"], "B", v_1959,
      "Multi-step conversion: aldehyde → secondary alcohol → methyl ketone → iodoform",
      "X = ethanal; Y = propan-2-ol; Z = propanone. Each step is 1 : 1, and one mole of propanone gives one mole of "
      "CHI₃.",
      ["n(C₂H₅OH) = 2.3/46 = 0.05 mol", "→ 0.05 mol CH₃CHO → 0.05 mol CH₃CH(OH)CH₃ → 0.05 mol CH₃COCH₃",
       "n(CHI₃) = 0.05 mol; M(CHI₃) = 394", "Mass = 0.05 × 394 = 19.7 g"],
      why_others_wrong="39.4 g doubles the amount; 9.85 g halves it; 19.1 g uses only the mass of three iodine atoms "
                       "(381) as the molar mass of iodoform.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Grignard addition and haloform reaction", seconds=90),

    Q(T_OX, "Alcohols", "Advanced", "direct",
      "A compound X, C₇H₈O, contains a benzene ring. It does not dissolve in aqueous NaOH, but it liberates hydrogen "
      "with sodium metal. On vigorous oxidation with alkaline KMnO₄ followed by acidification, it gives benzoic acid. "
      "X is:",
      ["Benzyl alcohol", "Anisole (methoxybenzene)", "o-Cresol", "p-Cresol"], "A",
      "Distinguishing an aromatic alcohol from phenols and ethers",
      "Insolubility in NaOH rules out the acidic cresols (phenols). Reaction with sodium shows an O–H group, which "
      "rules out anisole. Oxidation of the side chain –CH₂OH to –COOH gives benzoic acid. X is C₆H₅CH₂OH.",
      ["Not soluble in NaOH → not a phenol", "H₂ with Na → has O–H → not an ether", "Side chain → –COOH → benzyl alcohol"],
      why_others_wrong="Anisole has no O–H and does not liberate H₂ with Na; o- and p-cresol are phenols and dissolve "
                       "in aqueous NaOH.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of alcohols and phenols", seconds=60),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "assertion_reason",
      *ar("Ketones are generally more reactive than aldehydes in nucleophilic addition reactions.", False,
          "The two relatively large substituents in a ketone hinder the approach of a nucleophile to the carbonyl "
          "carbon more than the single substituent and hydrogen of an aldehyde do.", True),
      "Relative reactivity of aldehydes and ketones",
      "Aldehydes are more reactive than ketones for both steric and electronic reasons: the two alkyl groups of a "
      "ketone hinder the nucleophile and also reduce the electrophilicity of the carbonyl carbon. A is false; R is a "
      "true statement (and in fact explains why ketones are less reactive).",
      ["Aldehydes > ketones in nucleophilic addition → A false", "Steric hindrance by two groups in ketones → R true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition reactions", seconds=35),

    Q(T_OX, "Carboxylic acids", "Advanced", "statement_pair",
      *sp("Esterification of a carboxylic acid with an alcohol in the presence of concentrated H₂SO₄ is an "
          "irreversible reaction.", False,
          "Esterification of a carboxylic acid with an alcohol is catalysed by a small amount of concentrated "
          "sulphuric acid or HCl gas.", True),
      "Equilibrium nature of esterification",
      "Esterification is reversible; the equilibrium is shifted towards the ester by removing water or ester as it "
      "forms. A mineral acid such as concentrated H₂SO₄ or HCl gas catalyses it. Statement I is false and Statement II "
      "is true.",
      ["RCOOH + R′OH ⇌ RCOOR′ + H₂O (reversible)", "H⁺ catalyst (conc. H₂SO₄ or HCl gas)"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esterification", seconds=35),

    Q(T_OX, "Phenols", "Advanced", "match_list",
      *ml("Match the compound in List-I with its approximate pKa in List-II.",
          ["Ethanol", "Phenol", "4-Nitrophenol", "2,4,6-Trinitrophenol"],
          ["≈ 0.5", "≈ 7.1", "≈ 10.0", "≈ 15.9"],
          "IV III II I", ["III IV II I", "IV II III I", "IV III I II"], "C"),
      "Acid strength of alcohols and phenols",
      "The lower the pKa, the stronger the acid. Ethanol is a weaker acid than phenol (no resonance stabilisation of "
      "ethoxide). Each nitro group at an ortho or para position withdraws electrons and stabilises the phenoxide ion, "
      "so 4-nitrophenol is stronger than phenol and 2,4,6-trinitrophenol is very strong.",
      ["Acid strength: picric acid > 4-nitrophenol > phenol > ethanol", "pKa: ≈0.5 < ≈7.1 < ≈10.0 < ≈15.9",
       "A-IV, B-III, C-II, D-I"],
      why_others_wrong="The other codes make phenol weaker than ethanol, or 4-nitrophenol weaker than phenol, or give "
                       "the trinitro compound a higher pKa than 4-nitrophenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols (pKa table)", seconds=55),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following are shown by BOTH ethanal and propanone?",
          [("A yellow precipitate of iodoform when warmed with iodine and aqueous NaOH", True),
           ("An orange-yellow precipitate with 2,4-dinitrophenylhydrazine", True),
           ("A silver mirror with Tollens' reagent", False),
           ("A red-brown precipitate with Fehling's solution", False),
           ("Addition of HCN to form a cyanohydrin", True)],
          [["a", "b", "c"], ["b", "e"], ["a", "c", "d", "e"]], "B"),
      "Common and distinguishing reactions of an aldehyde and a ketone",
      "Both contain a CH₃–CO– group (iodoform positive) and a carbonyl group (2,4-DNP derivative, cyanohydrin). Only "
      "the aldehyde is oxidised by the mild oxidants in Tollens' and Fehling's reagents.",
      ["(a) both: CH₃CO– group", "(b) both: C=O", "(c) only ethanal", "(d) only ethanal", "(e) both"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions", seconds=50),
]
