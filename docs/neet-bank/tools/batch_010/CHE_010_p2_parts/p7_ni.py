
# ================================================================ Organic Compounds Containing Nitrogen (2465-2477)
# 2465: arylamines = N bonded directly to an aromatic ring
aryl_2465 = {"aniline": True, "benzylamine": False, "N-methylaniline": True, "4-methylaniline": True,
             "cyclohexanamine": False, "N,N-dimethylaniline": True, "2-phenylethanamine": False}
v_2465 = str(sum(aryl_2465.values()))
assert v_2465 == "4"
# 2469: 2,4,6-tribromoaniline (C6H4Br3N) -> diazonium -> H3PO2 -> 1,3,5-tribromobenzene (C6H3Br3)
M_tba = mm(C=6, H=4, Br=3, N=1)
M_tbb = mm(C=6, H=3, Br=3)
assert (M_tba, M_tbb) == (330, 315)
m_2469 = F(330, 100) / M_tba * M_tbb
assert m_2469 == F(315, 100)
v_2469 = "3.15 g"
assert round(float(F(1, 100) * mm(C=6, H=4, Br=2)), 2) == 2.36
# 2470: stable arenediazonium salts at 273-278 K only from primary aromatic amines
pa_2470 = {"aniline": True, "4-methylaniline": True, "4-nitroaniline": True, "benzylamine": False,
           "ethanamine": False, "N-methylaniline": False}
v_2470 = str(sum(pa_2470.values()))
assert v_2470 == "3"
# 2474: pH of 0.10 M aniline, pKb = 9.38: pOH = (pKb - log C)/2
pOH = (9.38 + 1) / 2
pH_2474 = 14 - pOH
assert abs(pOH - 5.19) < 1e-9 and abs(pH_2474 - 8.81) < 1e-9
v_2474 = "8.81"

QUESTIONS += [
    N(T_NI, "Amines: basicity and identification", "Basic",
      "In an arylamine, the nitrogen atom is bonded directly to a carbon atom of an aromatic ring. How many of the "
      "following are arylamines?\n"
      "Aniline, benzylamine (C₆H₅CH₂NH₂), N-methylaniline, 4-methylaniline, cyclohexanamine, N,N-dimethylaniline, "
      "2-phenylethanamine (C₆H₅CH₂CH₂NH₂)",
      ["1", "2", "3", v_2465], "D", v_2465,
      "Classification of amines",
      "Only the position of nitrogen matters: it must be attached to the ring itself. Benzylamine and "
      "2-phenylethanamine have the amino group on a side-chain carbon, so they are aliphatic amines; cyclohexanamine "
      "has no aromatic ring.",
      ["Arylamines: aniline, N-methylaniline, 4-methylaniline, N,N-dimethylaniline → 4",
       "Not arylamines: benzylamine, 2-phenylethanamine, cyclohexanamine"],
      why_others_wrong="Lower counts leave out the secondary and tertiary arylamines (N-methyl and N,N-dimethyl "
                       "anilines); being 2° or 3° does not change the aryl classification.",
      ncert=f"{NC12}, 'Amines', classification of amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Ethanamine is soluble in water, whereas aniline is only sparingly soluble. The reason is that:",
      ["aniline is a stronger base than ethanamine",
       "ethanamine forms hydrogen bonds with water, whereas the large hydrophobic C₆H₅ group of aniline decreases "
       "the extent of hydrogen bonding with water",
       "ethanamine is an ionic compound", "the nitrogen atom of aniline has no lone pair of electrons"], "B",
      "Solubility of amines in water",
      "Lower aliphatic amines dissolve in water because they form hydrogen bonds with water molecules. In aniline "
      "the large hydrocarbon (phenyl) part is hydrophobic, so the extent of hydrogen bonding, and hence the "
      "solubility, decreases.",
      ["Both have –NH₂ able to hydrogen bond", "Large hydrophobic C₆H₅ part in aniline → lower solubility"],
      why_others_wrong="Aniline is a weaker base than ethanamine; ethanamine is a covalent molecule; aniline's "
                       "nitrogen does carry a lone pair, though it is partly delocalised into the ring.",
      ncert=f"{NC12}, 'Amines', physical properties", seconds=30),

    Q(T_NI, "Diazonium salts", "Basic", "statement_pair",
      *sp("In replacing the diazonium group by chlorine, the yield in the Sandmeyer reaction (CuCl/HCl) is better "
          "than in the Gattermann reaction (copper powder/HCl).", True,
          "If the temperature of a benzenediazonium chloride solution is allowed to rise up to 283 K, the salt is "
          "hydrolysed to phenol.", True),
      "Reactions of arenediazonium salts",
      "NCERT: chloro and bromo groups can be introduced either with Cu(I) halides (Sandmeyer) or with copper "
      "powder and the halogen acid (Gattermann); the yield in the Sandmeyer reaction is found to be better. A "
      "diazonium salt solution warmed up to 283 K is hydrolysed to phenol.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Basic", "match_list",
      *ml("Match the common name of the amine in List-I with its IUPAC name in List-II.",
          ["Allylamine, CH₂=CH–CH₂–NH₂", "Hexamethylenediamine, H₂N–(CH₂)₆–NH₂", "Isopropylamine, (CH₃)₂CH–NH₂",
           "Dimethylamine, (CH₃)₂NH"],
          ["N-Methylmethanamine", "Propan-2-amine", "Prop-2-en-1-amine", "Hexane-1,6-diamine"],
          "III IV II I", ["IV III II I", "III IV I II", "II IV III I"], "B"),
      "Nomenclature of amines",
      "Amines are named by replacing the 'e' of the alkane with 'amine' (keeping 'e' before 'diamine'); the position "
      "of –NH₂ is given by a locant; extra alkyl groups on nitrogen are shown with the prefix N-.",
      ["Allylamine → prop-2-en-1-amine", "Hexamethylenediamine → hexane-1,6-diamine",
       "Isopropylamine → propan-2-amine", "Dimethylamine → N-methylmethanamine"],
      why_others_wrong="Swapping isopropylamine and dimethylamine confuses a 1° amine with a 2° amine; swapping the "
                       "first two pairs a C₃ unsaturated amine with a C₆ diamine.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=35),

    N(T_NI, "Diazonium salts", "Intermediate",
      "1,3,5-Tribromobenzene cannot be made by direct bromination of benzene but can be made from aniline. 3.30 g of "
      "2,4,6-tribromoaniline is diazotised at 273–278 K, and the diazonium salt is treated with hypophosphorous "
      "acid (H₃PO₂). Assuming every step is complete, the mass of 1,3,5-tribromobenzene formed is (C = 12, H = 1, "
      "N = 14, Br = 80):",
      ["2.36 g", "3.30 g", v_2469, "6.30 g"], "C", v_2469,
      "Replacing –N₂⁺ by hydrogen",
      "Hypophosphorous acid reduces the diazonium salt and replaces –N₂⁺ by –H, so the three bromine atoms are left "
      "in the 1,3,5 positions, which direct bromination of benzene cannot give.",
      ["C₆H₂Br₃NH₂: M = 330 g mol⁻¹ → 3.30 / 330 = 0.010 mol", "C₆H₃Br₃: M = 315 g mol⁻¹",
       "Mass = 0.010 × 315 = 3.15 g"],
      why_others_wrong="3.30 g repeats the mass of the amine; 2.36 g is for a dibromobenzene; 6.30 g doubles the "
                       "moles.",
      ncert=f"{NC12}, 'Amines', importance of diazonium salts in synthesis of aromatic compounds", seconds=60),

    N(T_NI, "Diazonium salts", "Intermediate",
      "How many of the following give a diazonium salt that is stable enough to be used in solution at "
      "273–278 K when treated with NaNO₂ and dilute HCl?\n"
      "Aniline, 4-methylaniline, 4-nitroaniline, benzylamine, ethanamine, N-methylaniline",
      ["2", v_2470, "4", "5"], "B", v_2470,
      "Which amines form arenediazonium salts",
      "Only primary aromatic amines form arenediazonium salts, which are stable for a short time at low "
      "temperature. Primary aliphatic amines (including benzylamine, where –NH₂ is on a side chain) give unstable "
      "aliphatic diazonium salts that decompose at once with evolution of N₂. A secondary amine such as "
      "N-methylaniline has only one H on nitrogen and cannot form a diazonium salt.",
      ["Primary aromatic: aniline, 4-methylaniline, 4-nitroaniline → 3",
       "Benzylamine, ethanamine: primary aliphatic; N-methylaniline: secondary"],
      why_others_wrong="4 includes benzylamine, whose nitrogen is not on the ring; 2 leaves out 4-nitroaniline, "
                       "which is still a primary aromatic amine.",
      ncert=f"{NC12}, 'Amines', reaction with nitrous acid; diazonium salts", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("N,N-Dimethylaniline reacts with benzenesulphonyl chloride to give a sulphonamide that is insoluble in "
          "aqueous alkali.", False,
          "Tertiary amines have no hydrogen atom on the nitrogen atom.", True),
      "Hinsberg's test and tertiary amines",
      "Benzenesulphonyl chloride replaces a hydrogen atom on nitrogen. N,N-Dimethylaniline is a tertiary amine "
      "with no N–H, so it does not react with Hinsberg's reagent at all; an alkali-insoluble sulphonamide is "
      "characteristic of secondary amines. A is false, R is true.",
      ["A: false; no reaction", "R: true"],
      ncert=f"{NC12}, 'Amines', reaction with arylsulphonyl chloride", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "statement_pair",
      *sp("Secondary amines react with benzenesulphonyl chloride to give a sulphonamide that dissolves in aqueous "
          "alkali.", False,
          "Primary aromatic amines react with nitrous acid at 273–278 K to form arenediazonium salts.", True),
      "Identification reactions of amines",
      "The N,N-dialkylbenzenesulphonamide from a secondary amine has no hydrogen on nitrogen and so is not acidic; "
      "it is insoluble in alkali (the alkali-soluble product comes from a primary amine). Primary aromatic amines "
      "give arenediazonium salts with nitrous acid in the cold.",
      ["Statement I: false", "Statement II: true"],
      ncert=f"{NC12}, 'Amines', chemical reactions: Hinsberg's test; reaction with nitrous acid", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "direct",
      "The correct order of basic strength in aqueous solution is:",
      ["4-Methylaniline > aniline > 4-nitroaniline", "Aniline > 4-methylaniline > 4-nitroaniline",
       "4-Nitroaniline > aniline > 4-methylaniline", "Aniline > 4-nitroaniline > 4-methylaniline"], "A",
      "Effect of substituents on the basicity of aniline",
      "Electron-releasing groups such as –CH₃ increase the electron density on nitrogen and raise the basic "
      "strength; electron-withdrawing groups such as –NO₂ lower it.",
      ["–CH₃ (+I, hyperconjugation): stronger base than aniline",
       "–NO₂ (−I, −R): much weaker base than aniline"],
      why_others_wrong="The other orders either ignore the activating effect of –CH₃ or treat –NO₂ as electron "
                       "releasing.",
      ncert=f"{NC12}, 'Amines', basic character of arylamines", seconds=35),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "The pKb of aniline is 9.38. Treating aniline as a weak base that is only slightly ionised, the pH of a "
      "0.10 M aqueous solution of aniline at 298 K is (pKw = 14.00):",
      ["4.62", "5.19", "9.38", v_2474], "D", v_2474,
      "pH of a solution of a weak base",
      "For a weak base, [OH⁻] = √(Kb·C), so pOH = ½(pKb − log C).",
      ["pOH = ½(9.38 + 1.00) = 5.19", "pH = 14.00 − 5.19 = 8.81"],
      why_others_wrong="5.19 is the pOH, not the pH; 4.62 is 14 − 9.38, which treats pKb as pOH; 9.38 is simply the "
                       "pKb.",
      ncert=f"{NC12}, 'Amines', basic character of amines (pKb values)", seconds=75),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "An amine X, C₃H₉N, reacts with benzenesulphonyl chloride to give a product that is insoluble in aqueous "
      "alkali, and it does not give the carbylamine test. X is:",
      ["Propan-1-amine", "Propan-2-amine", "N-Methylethanamine", "N,N-Dimethylmethanamine"], "C",
      "Identifying an amine by Hinsberg's and carbylamine tests",
      "An alkali-insoluble Hinsberg product is given by a secondary amine. The carbylamine test is given only by "
      "primary amines, so a negative result is consistent. The only secondary amine of formula C₃H₉N is "
      "CH₃–NH–C₂H₅.",
      ["Insoluble sulphonamide → 2° amine", "No isocyanide → not 1°", "C₃H₉N, 2° → N-methylethanamine"],
      why_others_wrong="Propan-1-amine and propan-2-amine are primary (alkali-soluble product, positive carbylamine "
                       "test); trimethylamine (N,N-dimethylmethanamine) does not react with benzenesulphonyl "
                       "chloride.",
      ncert=f"{NC12}, 'Amines', identification of primary, secondary and tertiary amines", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "assertion_reason",
      *ar("4-Nitroaniline is a much weaker base than aniline.", True,
          "The –NO₂ group at the para position withdraws electron density from the nitrogen lone pair by its −R and "
          "−I effects, making the lone pair less available for protonation.", True, explains=True),
      "Electron-withdrawing groups and the basicity of arylamines",
      "In aniline the nitrogen lone pair is already partly delocalised into the ring. A para –NO₂ group pulls this "
      "electron density further, through the ring onto itself (−R) and through σ bonds (−I), so protonation is much "
      "less favourable. R gives the reason for A.",
      ["A: true", "R: true and the cause of A"],
      ncert=f"{NC12}, 'Amines', basic character of arylamines", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "multi_statement",
      *ms("Consider three amines: X = ethanamine, Y = aniline and Z = N-methylaniline. Which of the following "
          "statements are correct?",
          [("X and Y both give a foul-smelling isocyanide when warmed with chloroform and ethanolic KOH.", True),
           ("Y, after treatment with NaNO₂ and dilute HCl at 273–278 K, gives a coloured azo dye with an alkaline "
            "solution of phenol.", True),
           ("Z gives a product with benzenesulphonyl chloride that is insoluble in aqueous alkali.", True),
           ("X gives a diazonium salt that is stable in solution at 273–278 K.", False),
           ("Z gives the carbylamine test.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "e"]], "B"),
      "Distinguishing primary aliphatic, primary aromatic and secondary amines",
      "The carbylamine test is given by primary amines, aliphatic and aromatic. Only primary aromatic amines give "
      "stable diazonium salts, which couple with phenol to give azo dyes; ethanamine's diazonium salt decomposes "
      "at once, releasing N₂. N-Methylaniline, a secondary amine, gives an alkali-insoluble sulphonamide and no "
      "isocyanide.",
      ["(a) true", "(b) true", "(c) true", "(d) false", "(e) false"],
      why_others_wrong="Options with (d) forget that aliphatic diazonium salts are unstable; options with (e) apply "
                       "the carbylamine test to a secondary amine.",
      ncert=f"{NC12}, 'Amines', chemical reactions; diazonium salts", seconds=75),
]
