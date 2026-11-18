
# ================================================================ Organic Compounds Containing Nitrogen (1965-1977)
# 1966: C6H5NO2 + 3H2 -> C6H5NH2 + 2H2O ; 12.3 g nitrobenzene
n_1966 = F(123, 10) / mm(C=6, H=5, N=1, O=2)
assert n_1966 == F(1, 10)
v_1966 = f"{float(n_1966 * 3 * F(224, 10)):.2f} L"
assert v_1966 == "6.72 L"
# 1969: C6H5N2+BF4- -> C6H5F + BF3 + N2 ; 9.3 g aniline -> 0.1 mol salt -> 0.2 mol gas
n_1969 = F(93, 10) / mm(C=6, H=7, N=1)
assert n_1969 == F(1, 10)
v_1969 = f"{float(n_1969 * 2 * F(224, 10)):.2f} L"
assert v_1969 == "4.48 L"
# 1970: NCERT pKb values; ammonia 4.75; count stronger bases (smaller pKb)
pkb = {"CH3NH2": 3.38, "(CH3)2NH": 3.27, "(CH3)3N": 4.22, "C2H5NH2": 3.29, "C6H5NH2": 9.38, "C6H5NHCH3": 9.30,
       "p-nitroaniline": 13.0}
v_1970 = str(sum(1 for v in pkb.values() if v < 4.75))
assert v_1970 == "4"
# 1974: Hinsberg: secondary amines give alkali-insoluble sulphonamides; tertiary do not react
cls = {"CH3NH2": 1, "(CH3)2NH": 2, "(CH3)3N": 3, "C6H5NH2": 1, "C6H5NHCH3": 2, "(C2H5)2NH": 2, "C6H5N(CH3)2": 3}
v_1974 = str(sum(1 for c in cls.values() if c == 2))
assert v_1974 == "3"

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "The IUPAC name of CH₃–CH(NH₂)–CH₂–CH₃ is:",
      ["2-Aminobutane", "Butan-3-amine", "1-Methylpropanamine", "Butan-2-amine"], "D",
      "IUPAC names of amines",
      "The –NH₂ group is the principal group, named by replacing the final 'e' of the alkane by 'amine'. The chain "
      "is numbered so that the carbon bearing –NH₂ gets the lowest locant.",
      ["Chain: 4 C → butane", "–NH₂ on C-2 (lowest)", "Name: butan-2-amine"],
      why_others_wrong="'2-Aminobutane' cites the principal group as a prefix; 'butan-3-amine' numbers from the wrong "
                       "end; '1-methylpropanamine' does not use the longest chain.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=25),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "12.3 g of nitrobenzene is reduced completely to aniline by catalytic hydrogenation:\n"
      "C₆H₅NO₂ + 3H₂ → C₆H₅NH₂ + 2H₂O\n"
      "The volume of hydrogen consumed, measured at STP, is (C = 12, H = 1, N = 14, O = 16; molar volume at STP = "
      "22.4 L mol⁻¹):",
      ["2.24 L", "6.72 L", "4.48 L", "8.96 L"], "B", v_1966,
      "Reduction of nitro compounds to amines",
      "Three moles of H₂ are needed per mole of nitrobenzene: two to remove the oxygen atoms as water and one to "
      "supply the two hydrogens on nitrogen.",
      ["n(C₆H₅NO₂) = 12.3/123 = 0.10 mol", "n(H₂) = 3 × 0.10 = 0.30 mol", "V = 0.30 × 22.4 = 6.72 L"],
      why_others_wrong="2.24 L uses a 1 : 1 ratio; 4.48 L counts only the H₂ that forms water; 8.96 L uses four moles "
                       "of H₂.",
      ncert=f"{NC12}, 'Amines', preparation of amines by reduction of nitro compounds", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("The –NH₂ group attached to a benzene ring is a strongly activating, ortho- and para-directing group.", True,
          "The activating effect of the –NH₂ group can be controlled by first acetylating it to –NHCOCH₃.", True),
      "Electrophilic substitution in aniline and its control",
      "The lone pair on nitrogen is delocalised into the ring (+R), making the ortho and para positions very electron "
      "rich. In acetanilide the nitrogen lone pair is also delocalised onto the acetyl oxygen, so the group is less "
      "activating and monosubstitution becomes possible. Both statements are true.",
      ["–NH₂: +R → o/p, strongly activating", "–NHCOCH₃: lone pair shared with C=O → moderate activation"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution", seconds=30),

    Q(T_NI, "Amines: basicity and identification", "Basic", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Amines react with mineral acids to form ammonium salts.", True),
           ("Anilinium chloride regenerates aniline when treated with aqueous NaOH.", True),
           ("Aniline is highly soluble in water.", False),
           ("Aniline dissolves in dilute hydrochloric acid.", True),
           ("Tertiary aliphatic amines liberate nitrogen gas with nitrous acid.", False)],
          [["a", "b"], ["b", "d", "e"], ["a", "c", "d"]], "C"),
      "Salt formation by amines",
      "Amines are bases and form salts with acids: C₆H₅NH₂ + HCl → C₆H₅NH₃⁺Cl⁻, which is water soluble, so aniline "
      "dissolves in dilute HCl. A strong base sets the amine free again. Aniline itself, with its large hydrophobic "
      "phenyl group, is only sparingly soluble in water. Evolution of N₂ with nitrous acid is a reaction of primary "
      "aliphatic amines.",
      ["(a) true", "(b) true", "(c) false", "(d) true", "(e) false"],
      ncert=f"{NC12}, 'Amines', physical properties and basic character", seconds=45),

    N(T_NI, "Diazonium salts", "Intermediate",
      "9.3 g of aniline is diazotised and the diazonium salt is converted completely into benzenediazonium "
      "fluoroborate, C₆H₅N₂⁺BF₄⁻. This is heated until it decomposes completely into fluorobenzene, boron trifluoride "
      "and nitrogen. The total volume of gases released, measured at STP, is (C = 12, H = 1, N = 14; molar volume at "
      "STP = 22.4 L mol⁻¹):",
      ["2.24 L", "6.72 L", "1.12 L", "4.48 L"], "D", v_1969,
      "Balz–Schiemann reaction",
      "C₆H₅N₂⁺BF₄⁻ → C₆H₅F + BF₃↑ + N₂↑. Each mole of the salt releases two moles of gas.",
      ["n(aniline) = 9.3/93 = 0.10 mol → 0.10 mol salt", "Gas: 0.10 mol N₂ + 0.10 mol BF₃ = 0.20 mol",
       "V = 0.20 × 22.4 = 4.48 L"],
      why_others_wrong="2.24 L counts only N₂ (or only BF₃); 6.72 L adds a third gas; 1.12 L halves the amount.",
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts: replacement by fluoride", seconds=55),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "NCERT's table lists the pKb values of several amines in aqueous solution; for ammonia, pKb = 4.75. How many of "
      "the following are stronger bases than ammonia in aqueous solution?\n"
      "CH₃NH₂, (CH₃)₂NH, (CH₃)₃N, C₂H₅NH₂, C₆H₅NH₂, C₆H₅NHCH₃, p-nitroaniline",
      ["3", "4", "5", "7"], "B", v_1970,
      "Basic strength of aliphatic and aromatic amines",
      "A smaller pKb means a stronger base. All the aliphatic amines (pKb ≈ 3.3–4.2) are stronger bases than ammonia "
      "because of the +I effect of the alkyl groups. In aryl amines the lone pair is delocalised into the ring, so "
      "they are much weaker bases (pKb ≈ 9.3–9.4, even higher for p-nitroaniline).",
      ["Aliphatic: CH₃NH₂ 3.38, (CH₃)₂NH 3.27, (CH₃)₃N 4.22, C₂H₅NH₂ 3.29 → all < 4.75",
       "Aromatic: C₆H₅NH₂ 9.38, C₆H₅NHCH₃ 9.30, p-nitroaniline → all > 4.75", "Total = 4"],
      why_others_wrong="3 leaves out trimethylamine, which in water is weaker than the other methylamines but still "
                       "stronger than ammonia; 5 or 7 count aromatic amines, which are weaker than ammonia.",
      ncert=f"{NC12}, 'Amines', basic character of amines (pKb values)", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Direct nitration of aniline gives, besides the ortho and para derivatives, a significant amount of "
          "m-nitroaniline.", True,
          "In the strongly acidic nitrating mixture, aniline is protonated to the anilinium ion, which is "
          "meta-directing.", True, explains=True),
      "Nitration of aniline",
      "–NH₂ is ortho/para directing, but in concentrated acid much of the aniline exists as C₆H₅NH₃⁺. The –NH₃⁺ group "
      "has no lone pair and withdraws electrons, so it directs to the meta position. R explains A.",
      ["C₆H₅NH₂ + H⁺ → C₆H₅NH₃⁺", "–NH₃⁺: electron-withdrawing, meta-directing", "→ m-nitroaniline formed"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution: nitration", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the conversion in List-I with the reagent(s) used in List-II.",
          ["Nitrobenzene → aniline", "Benzamide → aniline", "Ethanenitrile → ethanamine",
           "Phthalimide → primary aliphatic amine"],
          ["Bromine and aqueous NaOH, warmed", "Ethanolic KOH, then an alkyl halide, then alkaline hydrolysis",
           "Iron scrap and hydrochloric acid", "Lithium aluminium hydride (or H₂ with a nickel catalyst)"],
          "III I IV II", ["I III IV II", "III IV I II", "III I II IV"], "C"),
      "Methods of preparing amines",
      "Nitro compounds are reduced by Fe/HCl. Amides lose a carbon in the Hofmann bromamide degradation (Br₂/NaOH). "
      "Nitriles are reduced to primary amines by LiAlH₄ or by catalytic hydrogenation. Gabriel synthesis converts "
      "phthalimide, via its potassium salt and an alkyl halide, into a primary amine on alkaline hydrolysis.",
      ["A → III", "B → I", "C → IV", "D → II"],
      why_others_wrong="The other codes swap the reduction of the nitro group with the Hofmann degradation, or the "
                       "nitrile reduction with the Gabriel synthesis.",
      ncert=f"{NC12}, 'Amines', preparation of amines", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Ethanamine is soluble in water.", True,
          "Ethanamine is a stronger base than ammonia in aqueous solution.", True, explains=False),
      "Solubility versus basicity of lower amines",
      "Lower aliphatic amines dissolve in water because they form hydrogen bonds with water molecules. Ethanamine's "
      "greater basicity than ammonia comes from the +I effect of the ethyl group. Both statements are true, but the "
      "basic strength is a separate property and does not explain the solubility.",
      ["Solubility: H-bonding with water (A true)", "Basicity: +I of C₂H₅ (R true)", "R does not explain A"],
      ncert=f"{NC12}, 'Amines', physical properties and basic character", seconds=30),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "Each of the following is shaken with benzenesulphonyl chloride (Hinsberg's reagent). How many of them give a "
      "product that is insoluble in aqueous alkali?\n"
      "CH₃NH₂, (CH₃)₂NH, (CH₃)₃N, C₆H₅NH₂, C₆H₅NHCH₃, (C₂H₅)₂NH, C₆H₅N(CH₃)₂",
      ["5", "2", "4", "3"], "D", v_1974,
      "Hinsberg's test",
      "Primary amines give N-substituted sulphonamides that still carry an acidic N–H, so they dissolve in alkali. "
      "Secondary amines give N,N-disubstituted sulphonamides with no N–H: insoluble in alkali. Tertiary amines do "
      "not react.",
      ["Primary (CH₃NH₂, C₆H₅NH₂): product soluble in alkali", "Secondary ((CH₃)₂NH, C₆H₅NHCH₃, (C₂H₅)₂NH): insoluble",
       "Tertiary ((CH₃)₃N, C₆H₅N(CH₃)₂): no reaction", "Count = 3"],
      why_others_wrong="5 adds the tertiary amines, which give no product at all; 2 misses N-methylaniline, an aryl "
                       "secondary amine; 4 counts aniline, a primary amine.",
      ncert=f"{NC12}, 'Amines', reaction with arylsulphonyl chloride (Hinsberg's test)", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "Benzoic acid is heated with thionyl chloride, and the product is treated with ammonia to give X. X is warmed "
      "with bromine and aqueous NaOH to give Y. Y is:",
      ["Benzylamine", "Benzonitrile", "Aniline", "Benzamide"], "C",
      "Acid → acyl chloride → amide → amine with one carbon fewer",
      "C₆H₅COOH + SOCl₂ → C₆H₅COCl; with NH₃ → X = C₆H₅CONH₂ (benzamide). Hofmann bromamide degradation removes the "
      "carbonyl carbon: Y = C₆H₅NH₂.",
      ["C₆H₅COCl → C₆H₅CONH₂ (X)", "Br₂ + NaOH → C₆H₅NH₂ (Y)"],
      why_others_wrong="Benzylamine would keep all seven carbons (reduction of the amide with LiAlH₄); benzonitrile "
                       "needs dehydration of the amide; benzamide is X, not Y.",
      ncert=f"{NC12}, 'Amines', Hofmann bromamide degradation", seconds=50),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "statement_pair",
      *sp("In the acylation of amines, a hydrogen atom of the –NH₂ or >NH group is replaced by an acyl group.", True,
          "Tertiary amines are readily acylated by ethanoyl chloride to give amides.", False),
      "Acylation of amines",
      "Acylation is nucleophilic substitution in which the amine nitrogen attacks the acyl chloride and an N–H "
      "hydrogen is lost (as HCl, removed by pyridine). Tertiary amines have no hydrogen on nitrogen, so they do not "
      "give amides. Statement I is true and Statement II false.",
      ["R–NH₂ + CH₃COCl → R–NHCOCH₃ + HCl", "R₃N: no N–H → no amide"],
      ncert=f"{NC12}, 'Amines', acylation", seconds=35),

    Q(T_NI, "Diazonium salts", "Advanced", "match_list",
      *ml("Match the reagent in List-I, used with benzenediazonium chloride, with the main organic product in List-II.",
          ["Copper powder and HCl", "Hypophosphorous acid (H₃PO₂) and water", "Phenol in mildly alkaline medium",
           "Aniline in mildly acidic medium"],
          ["p-Aminoazobenzene (yellow dye)", "Chlorobenzene", "p-Hydroxyazobenzene (orange dye)", "Benzene"],
          "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "A"),
      "Replacement and coupling reactions of diazonium salts",
      "Cu/HCl replaces –N₂⁺ by –Cl (Gattermann reaction); H₃PO₂ replaces it by H; coupling with phenoxide gives the "
      "orange p-hydroxyazobenzene and with aniline the yellow p-aminoazobenzene, both retaining –N=N–.",
      ["A → chlorobenzene (II)", "B → benzene (IV)", "C → p-hydroxyazobenzene (III)", "D → p-aminoazobenzene (I)"],
      why_others_wrong="The other codes swap the two replacement reactions or the two coupling products.",
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts", seconds=50),
]
