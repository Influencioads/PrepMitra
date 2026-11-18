
# ================================================================ Some Basic Principles of Organic Chemistry (1896-1915)
# 1897: +I groups among eight (NCERT: alkyl groups release electrons; NO2, CN, COOH, halogen, ester withdraw)
plus_i = {"-CH3": True, "-CH2CH3": True, "-C(CH3)3": True, "-NO2": False, "-CN": False, "-COOH": False,
          "-Cl": False, "-COOR": False}
v_1897 = str(sum(plus_i.values()))
assert v_1897 == "3"
# 1902: molecules with at least one sp carbon
has_sp = {"CO2": True, "HCN": True, "CH2=C=CH2": True, "CH3CN": True, "C2H4": False, "C6H6": False,
          "CH3C≡CH": True, "CH3CHO": False}
v_1902 = str(sum(has_sp.values()))
assert v_1902 == "5"
# 1903: isomers of C6H3Cl3 = 3-subsets of ring positions up to the 12 ring symmetries
from itertools import combinations  # noqa: E402
def canon(s):
    forms = []
    for r in range(6):
        for sgn in (1, -1):
            forms.append(tuple(sorted(((sgn * p + r) % 6) for p in s)))
    return min(forms)
v_1903 = str(len({canon(c) for c in combinations(range(6), 3)}))
assert v_1903 == "3" and len({canon(c) for c in combinations(range(6), 2)}) == 3
# 1910: the eight structural isomers of C5H11Cl and whether each has a chiral carbon
c5 = {"1-chloropentane": False, "2-chloropentane": True, "3-chloropentane": False,
      "1-chloro-2-methylbutane": True, "2-chloro-2-methylbutane": False, "2-chloro-3-methylbutane": True,
      "1-chloro-3-methylbutane": False, "1-chloro-2,2-dimethylpropane": False}
assert len(c5) == 8
v_1910 = str(sum(c5.values()))
assert v_1910 == "3"
# 1911: chain of 8 C; locant sets from the two ends, first point of difference
ends = ([3, 5, 6], [3, 4, 6])
assert min(ends) == [3, 4, 6]

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of CH₃–CH₂–CH(Br)–CH₂–OH is:",
      ["3-Bromobutan-4-ol", "1-Hydroxy-2-bromobutane", "2-Bromobutan-4-ol", "2-Bromobutan-1-ol"], "D",
      "Numbering a chain that carries a principal functional group and a substituent",
      "–OH is the principal functional group (suffix -ol) and must get the lowest locant, so the carbon carrying "
      "–OH is C-1. Bromine is then on C-2. Halogens are always cited as prefixes.",
      ["Parent chain: 4 C → butane", "–OH at C-1 → butan-1-ol", "Br at C-2 → 2-bromo", "Name: 2-bromobutan-1-ol"],
      why_others_wrong="'3-Bromobutan-4-ol' and '2-Bromobutan-4-ol' number from the wrong end; '1-Hydroxy-2-bromobutane' "
                       "cites the principal group as a prefix.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of compounds having "
            f"functional groups", seconds=30),

    N(T_GO, "Electronic effects", "Basic",
      "How many of the following groups, attached to a carbon chain, show an electron-releasing (+I) inductive "
      "effect?\n–CH₃, –CH₂CH₃, –C(CH₃)₃, –NO₂, –CN, –COOH, –Cl, –COOR",
      ["4", "3", "5", "2"], "B", v_1897,
      "Electron-releasing and electron-withdrawing groups (inductive effect)",
      "Alkyl groups such as methyl and ethyl release electrons (+I). Nitro, cyano, carboxyl, ester and halogen groups "
      "withdraw electrons (−I).",
      ["+I: –CH₃, –CH₂CH₃, –C(CH₃)₃ → 3", "−I: –NO₂, –CN, –COOH, –Cl, –COOR"],
      why_others_wrong="4 or 5 wrongly add the ester or carboxyl group, whose carbonyl carbon withdraws electrons; "
                       "2 leaves out one of the alkyl groups.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "assertion_reason",
      *ar("Ethyne, HC≡CH, is a linear molecule.", True,
          "Each carbon atom of ethyne is sp hybridised, and its two sp hybrid orbitals point in opposite directions "
          "at 180°.", True, explains=True),
      "Hybridisation and shape",
      "Each carbon uses its two sp orbitals to form σ bonds to H and to the other carbon. As the two sp orbitals are "
      "at 180°, H–C–C–H lies on a straight line. R explains A.",
      ["C in ethyne: sp", "sp orbitals at 180°", "→ linear H–C≡C–H"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', shapes of carbon compounds", seconds=25),

    Q(T_GO, "Isomerism", "Basic", "statement_pair",
      *sp("Ethyl ethanoate (CH₃COOC₂H₅) and methyl propanoate (C₂H₅COOCH₃) are metamers.", True,
          "Pentan-2-ol and pentan-3-ol are chain isomers.", False),
      "Metamerism and position isomerism",
      "Metamers have the same functional group with different alkyl groups on either side of it; both esters are "
      "C₄H₈O₂ with the alkyl groups distributed differently about –COO–, so Statement I is true. Pentan-2-ol and "
      "pentan-3-ol have the same chain and differ only in the position of –OH: they are position isomers, so "
      "Statement II is false.",
      ["Esters: same group, different alkyl groups on either side → metamers", "Same chain, –OH moved → position isomers"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=35),

    Q(T_GO, "Reactive intermediates", "Basic", "match_list",
      *ml("Match the species in List-I with its description in List-II.",
          ["(CH₃)₃C⁺", "CH₃•", "CH₃⁻", "NH₃"],
          ["Has a carbon atom with six valence electrons and a vacant p orbital",
           "Has a carbon atom with an unpaired electron",
           "Has a carbon atom carrying an unshared pair, with pyramidal shape",
           "A neutral molecule that acts as a nucleophile"],
          "I II III IV", ["II I III IV", "I III II IV", "IV II III I"], "A"),
      "Carbocations, free radicals, carbanions and nucleophiles",
      "A carbocation has a sextet on the sp² carbon with an empty p orbital; a free radical has an odd (unpaired) "
      "electron; a carbanion has an unshared pair on an sp³ carbon and is pyramidal; NH₃ is a neutral molecule with "
      "a lone pair, so it acts as a nucleophile.",
      ["(CH₃)₃C⁺ → I", "CH₃• → II", "CH₃⁻ → III", "NH₃ → IV"],
      why_others_wrong="The other codes swap the carbocation and free radical, the radical and carbanion, or treat "
                       "NH₃ as the carbocation.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fission of a covalent bond", seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "multi_statement",
      *ms("Which of the following statements about the representation of organic molecules are correct?",
          [("In a bond-line formula, carbon and hydrogen atoms are not shown and the lines represent carbon–carbon "
            "bonds drawn in a zig-zag fashion.", True),
           ("In a bond-line formula, the terminals of the lines represent methyl groups unless a functional group "
            "is indicated there.", True),
           ("The condensed formula CH₃(CH₂)₃CH₃ represents hexane.", False),
           ("In a wedge-and-dash formula, a dashed wedge represents a bond projecting away from the observer.", True),
           ("In a bond-line formula, heteroatoms such as oxygen and nitrogen are not shown.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "d"]], "D"),
      "Bond-line, condensed and three-dimensional formulas",
      "In bond-line formulas only the heteroatoms and the hydrogens attached to them are written; C and H are "
      "implied, and line ends are methyl groups. CH₃(CH₂)₃CH₃ has five carbons (pentane). A dashed wedge points "
      "away from the observer, a solid wedge towards the observer.",
      ["(a) true", "(b) true", "(c) false: C₅H₁₂, pentane", "(d) true", "(e) false: heteroatoms are shown"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural representations", seconds=50),

    N(T_GO, "Hybridisation and functional groups", "Intermediate",
      "How many of the following molecules contain at least one sp-hybridised carbon atom?\n"
      "CO₂, HCN, CH₂=C=CH₂, CH₃CN, CH₂=CH₂, C₆H₆, CH₃–C≡CH, CH₃CHO",
      ["4", "6", "5", "3"], "C", v_1902,
      "Recognising sp carbon atoms",
      "A carbon with two σ bonds and two π bonds (a triple bond, or two double bonds) is sp hybridised.",
      ["CO₂: O=C=O → sp", "HCN: H–C≡N → sp", "Allene: central C=C=C → sp", "CH₃–C≡N: nitrile C → sp",
       "Propyne: both C≡ carbons → sp", "Ethene, benzene, ethanal: only sp² and sp³", "Total = 5"],
      why_others_wrong="4 usually misses the central carbon of allene or the CO₂ carbon; 6 counts the carbonyl carbon "
                       "of ethanal, which is sp²; 3 counts only the C≡C and C≡N compounds.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation", seconds=50),

    N(T_GO, "Isomerism", "Intermediate",
      "How many structural isomers are possible for trichlorobenzene, C₆H₃Cl₃ (all three chlorine atoms on the "
      "benzene ring)?",
      ["3", "4", "2", "6"], "A", v_1903,
      "Position isomerism in trisubstituted benzenes",
      "Place three identical substituents on the six ring positions and remove arrangements that are the same after "
      "rotating or turning over the ring.",
      ["Three adjacent: 1,2,3-", "Two adjacent and one apart: 1,2,4-", "Alternate: 1,3,5-", "Total = 3"],
      why_others_wrong="2 forgets the unsymmetrical 1,2,4-isomer; 4 counts 1,2,4- and 1,2,5- (the same compound) "
                       "separately; 6 counts numbering variants as different compounds.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', isomerism", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of CH₃–CH(CH₃)–CH(OH)–CH₂–CH=CH₂ is:",
      ["5-Methylhex-1-en-4-ol", "2-Methylhex-5-en-3-ol", "2-Methylhex-5-en-4-ol", "5-Methylhex-1-en-3-ol"], "B",
      "Lowest locant to the principal functional group (–OH) in preference to a double bond",
      "The parent chain has six carbons and contains both the C=C and the C bearing –OH. The suffix group –OH gets "
      "the lowest locant: numbering from the left gives –OH at C-3 (from the right it would be C-4). The double bond "
      "is then C5=C6 and the methyl group is on C-2.",
      ["Six-carbon chain with C=C and –OH", "From the left: OH at 3; from the right: OH at 4 → number from the left",
       "Double bond at 5, methyl at 2", "Name: 2-methylhex-5-en-3-ol"],
      why_others_wrong="Names with '-1-en' give the double bond the lowest locant, which is wrong when –OH is the "
                       "principal group; '2-methylhex-5-en-4-ol' mixes the two numberings.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature", seconds=55),

    Q(T_GO, "Reactive intermediates", "Intermediate", "assertion_reason",
      *ar("Carbanions behave as nucleophiles.", True,
          "The negatively charged carbon of a carbanion carries an unshared pair of electrons that it can donate to "
          "an electron-deficient centre.", True, explains=True),
      "Carbanions as electron-pair donors",
      "A nucleophile is an electron-pair donor that seeks an electron-deficient centre. The carbanion carbon has an "
      "unshared electron pair, so it acts as a nucleophile. R explains A.",
      ["Carbanion: carbon with an unshared pair and negative charge", "Electron-pair donor → nucleophile"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nucleophiles and carbanions",
      seconds=30),

    Q(T_GO, "Types of organic reactions", "Intermediate", "statement_pair",
      *sp("The conversion of ethanol into ethene by heating with concentrated sulphuric acid is an elimination "
          "reaction.", True,
          "In a rearrangement reaction, atoms or groups shift within the same molecule to give a structural isomer "
          "of it.", True),
      "Types of organic reactions",
      "Loss of H₂O from adjacent carbon atoms of ethanol to form a C=C bond is an elimination. A rearrangement "
      "reaction changes the skeleton or positions of groups within one molecule (e.g. n-hexane → 2-methylpentane), "
      "giving an isomer. Both statements are true.",
      ["CH₃CH₂OH → CH₂=CH₂ + H₂O: elimination", "Rearrangement: groups shift within the molecule → isomer"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', types of organic reactions",
      seconds=35),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "match_list",
      *ml("Match the compound in List-I with its IUPAC name in List-II.",
          ["CH₃–CH=CH–CHO", "CH₃–CO–CH=CH₂", "HC≡C–CH₂–OH", "CH₃–CH(CN)–CH₃"],
          ["Prop-2-yn-1-ol", "2-Methylpropanenitrile", "But-2-enal", "But-3-en-2-one"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D"),
      "Names of unsaturated and polyfunctional compounds",
      "In each name the principal group (–CHO, C=O, –OH, –CN) gets the lowest locant; the carbon of –CHO and of "
      "–CN is counted as C-1 of the chain.",
      ["CH₃CH=CHCHO: C-1 is CHO, C=C at 2 → but-2-enal (III)",
       "CH₃COCH=CH₂: C=O at 2, C=C at 3 → but-3-en-2-one (IV)",
       "HC≡CCH₂OH: OH at 1, C≡C at 2 → prop-2-yn-1-ol (I)",
       "(CH₃)₂CHCN: CN carbon is C-1, methyl at 2 → 2-methylpropanenitrile (II)"],
      why_others_wrong="The other codes swap the aldehyde and the ketone, or the alcohol and the nitrile.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature", seconds=55),

    Q(T_GO, "Electronic effects", "Intermediate", "multi_statement",
      *ms("Which of the following statements about electronic effects are correct?",
          [("In chloroethane, CH₃–CH₂–Cl, the carbon atom bonded to chlorine carries a partial positive charge.", True),
           ("In chloroethane, the carbon atom farther from chlorine carries a smaller partial positive charge than "
            "the carbon bonded to chlorine.", True),
           ("The inductive effect is transmitted only through π bonds.", False),
           ("The electromeric effect is a permanent effect.", False),
           ("Alkyl groups such as –CH₃ show an electron-releasing inductive (+I) effect.", True)],
          [["a", "b"], ["a", "c", "e"], ["b", "d", "e"]], "C"),
      "Inductive and electromeric effects",
      "Cl pulls the C–Cl bond electrons, making C-1 δ+; C-1 in turn pulls a little from C-2, which becomes δδ+, so "
      "the effect weakens along the chain of σ bonds. The electromeric effect is temporary, operating only when an "
      "attacking reagent is present. Alkyl groups are +I.",
      ["(a) true", "(b) true (δδ+)", "(c) false: transmitted through σ bonds", "(d) false: temporary", "(e) true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', electron movement in organic "
            f"reactions", seconds=50),

    Q(T_GO, "Electronic effects", "Intermediate", "direct",
      "Which of the following is the strongest acid?",
      ["CH₃CH₂CH₂COOH", "ClCH₂CH₂CH₂COOH", "CH₃CH(Cl)CH₂COOH", "CH₃CH₂CH(Cl)COOH"], "D",
      "Inductive effect decreases with distance",
      "The −I effect of chlorine stabilises the carboxylate ion and increases acidity, but the effect fades rapidly "
      "as the number of bonds between Cl and –COO⁻ increases. It is greatest when Cl is on the α-carbon.",
      ["Cl on α-carbon (C-2): strongest −I at –COOH", "Cl on β (C-3) or γ (C-4): weaker", "No Cl: weakest acid",
       "→ 2-chlorobutanoic acid"],
      why_others_wrong="Moving chlorine to C-3 or C-4 weakens its effect on the carboxyl group; butanoic acid has no "
                       "electron-withdrawing group.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect", seconds=35),

    N(T_GO, "Isomerism", "Advanced",
      "Among all the structural isomers of the monochloroalkane C₅H₁₁Cl, how many contain a chiral carbon atom "
      "(a carbon bonded to four different groups)?",
      ["2", "3", "4", "5"], "B", v_1910,
      "Generating structural isomers and finding chiral centres",
      "C₅H₁₁Cl has eight structural isomers (three on the pentane chain, four on the 2-methylbutane chain, one on "
      "the 2,2-dimethylpropane chain). Check each carbon bearing Cl or a branch.",
      ["Pentane: 1-Cl (no), 2-Cl (yes), 3-Cl (no)",
       "2-Methylbutane: 1-Cl (C-2: H, CH₃, C₂H₅, CH₂Cl → yes), 2-Cl (two CH₃ → no), "
       "3-Cl i.e. 2-chloro-3-methylbutane (yes), 4-Cl i.e. 1-chloro-3-methylbutane (no)",
       "2,2-Dimethylpropane: 1-Cl (no)", "Total chiral = 3"],
      why_others_wrong="2 misses 1-chloro-2-methylbutane, whose chiral carbon does not carry chlorine; 4 or 5 wrongly "
                       "count 3-chloropentane or 2-chloro-2-methylbutane, which have two identical groups.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', isomerism", seconds=120),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₃–CH(C₂H₅)–CH₂–CH(CH₃)–CH(CH₃)–CH₂–CH₃ is:",
      ["2-Ethyl-4,5-dimethylheptane", "3,5,6-Trimethyloctane", "3,4,6-Trimethyloctane", "6-Ethyl-3,4-dimethylheptane"],
      "C",
      "Longest chain and lowest locants at the first point of difference",
      "The longest chain runs from the CH₃ of the ethyl group to the far CH₃: eight carbons (octane), with methyl "
      "groups on three carbons. Numbering from the right gives {3, 4, 6}; from the left {3, 5, 6}. At the first point "
      "of difference 4 < 5, so number from the right.",
      ["Longest chain = 8 C (through the ethyl group)", "Substituents: three methyl groups",
       "Locants {3,4,6} vs {3,5,6} → {3,4,6}", "Name: 3,4,6-trimethyloctane"],
      why_others_wrong="Names ending in 'heptane' miss the longer chain that runs through the ethyl group (an ethyl "
                       "group at C-2 or C-6 always means a longer chain exists); 3,5,6- numbers from the wrong end.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of branched alkanes",
      seconds=75),

    Q(T_GO, "Hybridisation and functional groups", "Advanced", "assertion_reason",
      *ar("An sp-hybridised carbon atom attracts bonding electrons more strongly than an sp³-hybridised carbon atom.",
          True,
          "The greater the s character of a hybrid orbital, the farther its electrons lie from the nucleus.", False),
      "s character and electronegativity of carbon",
      "s orbitals are held closer to the nucleus than p orbitals, so a hybrid orbital with more s character (sp: 50%) "
      "keeps its electrons nearer the nucleus. An sp carbon is therefore more electronegative than sp² or sp³ carbon. "
      "A is true; R reverses the relationship and is false.",
      ["sp: 50% s; sp²: 33%; sp³: 25%", "More s character → electrons closer to the nucleus",
       "→ sp carbon more electronegative (A true)", "R says 'farther' → false"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation and electronegativity",
      seconds=45),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("For chloroethene, CH₂=CH–Cl, a canonical structure with a positive charge on chlorine and a negative charge "
          "on the terminal CH₂ carbon contributes to the resonance hybrid.", True,
          "As a result, the carbon–chlorine bond in chloroethene acquires partial double bond character.", True),
      "Resonance (+R) involving a halogen lone pair",
      "A lone pair of chlorine is delocalised into the C=C π bond, giving ⁻CH₂–CH=Cl⁺ as a minor canonical "
      "structure. Because a C=Cl double bond appears in one contributor, the real C–Cl bond has partial double bond "
      "character. Both statements are true.",
      ["CH₂=CH–Cl̈ ↔ ⁻CH₂–CH=Cl⁺", "Hybrid: C–Cl with partial double bond character"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', resonance effect", seconds=45),

    Q(T_GO, "Electronic effects", "Advanced", "match_list",
      *ml("Match the observation in List-I with the electronic effect mainly responsible for it in List-II.",
          ["Stabilisation of propene by delocalisation of the σ electrons of its methyl C–H bonds into the π bond",
           "Equal length of the two carbon–oxygen bonds in the methanoate ion, HCOO⁻",
           "Chloroethanoic acid is a stronger acid than ethanoic acid",
           "Complete shift of the π electrons of an alkene to one carbon when H⁺ approaches"],
          ["Inductive effect", "Electromeric effect", "Hyperconjugation", "Resonance effect"],
          "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "B"),
      "Choosing the electronic effect that explains an observation",
      "σ–π delocalisation of C–H bonds is hyperconjugation; equal C–O bonds arise because the negative charge is "
      "delocalised over both oxygens (resonance); Cl withdraws electrons through σ bonds (−I), stabilising "
      "ClCH₂COO⁻; the temporary, complete shift of a π pair on the approach of a reagent is the electromeric effect.",
      ["A → hyperconjugation (III)", "B → resonance (IV)", "C → inductive effect (I)", "D → electromeric effect (II)"],
      why_others_wrong="The other codes confuse resonance with hyperconjugation, or the permanent inductive effect "
                       "with the temporary electromeric effect.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', electronic displacements", seconds=60),

    Q(T_GO, "Electronic effects", "Advanced", "multi_statement",
      *ms("Which of the following pairs are resonance (canonical) structures of the same species, rather than "
          "different compounds?",
          [("CH₃–CO–CH₃ and CH₂=C(OH)–CH₃", False),
           ("The two Kekulé structures of benzene", True),
           ("CH₂=CH–CH₂⁺ and ⁺CH₂–CH=CH₂", True),
           ("CH₃–O–N=O and CH₃–NO₂", False),
           ("The two structures of the ethanoate ion with the negative charge on either oxygen atom", True)],
          [["a", "b", "c"], ["b", "c", "d"], ["a", "c", "e"]], "D"),
      "Rules for writing canonical structures",
      "Canonical structures differ only in the positions of electrons; the positions of all nuclei stay the same. "
      "In (a) a hydrogen atom has moved (the two are different compounds), and in (d) the atoms are connected "
      "differently (methyl nitrite and nitromethane are isomers). In (b), (c) and (e) only π electrons or charges move.",
      ["(a) H moves → different compounds", "(b) resonance", "(c) resonance (allyl cation)",
       "(d) different connectivity → isomers", "(e) resonance"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', resonance structure", seconds=60),
]
