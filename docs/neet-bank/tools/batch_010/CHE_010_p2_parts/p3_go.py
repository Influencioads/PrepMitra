
# ================================================================ Some Basic Principles of Organic Chemistry (2396-2415)
# 2396: benzenoid aromatic compounds (contain a benzene ring)
bz_2396 = {"benzene": True, "toluene": True, "naphthalene": True, "pyridine": False, "furan": False,
           "cyclohexane": False, "tropolone": False}
v_2396 = str(sum(bz_2396.values()))
assert v_2396 == "3"
# 2411: functional group isomers of propanoic acid (C3H6O2) = same formula, different functional group
f_2411 = {"methyl ethanoate": (mm(C=3, H=6, O=2), True), "ethyl methanoate": (mm(C=3, H=6, O=2), True),
          "propanal": (mm(C=3, H=6, O=1), False), "2-hydroxypropanal": (mm(C=3, H=6, O=2), True),
          "ethanoic acid": (mm(C=2, H=4, O=2), False), "propan-1-ol": (mm(C=3, H=8, O=1), False),
          "propane-1,2-diol": (mm(C=3, H=8, O=2), False)}
target = mm(C=3, H=6, O=2)
assert all((m == target) == iso for m, iso in f_2411.values())  # every C3H6O2 compound listed is not an acid
v_2411 = str(sum(1 for m, iso in f_2411.values() if iso))
assert v_2411 == "3"

QUESTIONS += [
    N(T_GO, "Hybridisation and functional groups", "Basic",
      "Aromatic compounds that contain one or more benzene rings are called benzenoid aromatic compounds. How many of "
      "the following are benzenoid aromatic compounds?\n"
      "Benzene, toluene, naphthalene, pyridine, furan, cyclohexane, tropolone",
      ["2", v_2396, "4", "5"], "B", v_2396,
      "Classification of cyclic compounds",
      "Benzenoid aromatic compounds contain a benzene ring: benzene, toluene and naphthalene (two fused benzene "
      "rings). Pyridine and furan are heterocyclic aromatic compounds, tropolone is a non-benzenoid aromatic "
      "compound and cyclohexane is alicyclic.",
      ["Benzenoid: benzene, toluene, naphthalene → 3",
       "Not benzenoid: pyridine, furan (heterocyclic), tropolone (non-benzenoid), cyclohexane (alicyclic)"],
      why_others_wrong="2 leaves out naphthalene, whose fused rings are both benzene rings; 4 or 5 count pyridine or "
                       "tropolone, which are aromatic but not benzenoid.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "direct",
      "In ketene, CH₂=C=O, the hybridisation states of the CH₂ carbon and of the central carbon are, respectively:",
      ["sp and sp²", "sp² and sp²", "sp³ and sp", "sp² and sp"], "D",
      "Hybridisation from the number of σ bonds and π bonds",
      "The CH₂ carbon forms three σ bonds (two C–H, one C–C) and one π bond: sp². The central carbon forms two "
      "double bonds (two σ and two π bonds): sp, like the central carbon of an allene.",
      ["CH₂ carbon: 3 σ + 1 π → sp²", "Central carbon: 2 σ + 2 π → sp"],
      why_others_wrong="sp and sp² reverses the two carbons; sp² for the central carbon ignores its second π bond; "
                       "sp³ would need four σ bonds and no π bond.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', shapes of carbon compounds",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of CH₃–C(CH₃)=CH–CH₂–CH₃ is:",
      ["4-Methylpent-3-ene", "2-Methylpent-2-ene", "2-Methylpent-3-ene", "4-Methylpent-2-ene"], "B",
      "Naming an alkene",
      "The longest chain containing the double bond has five carbons. It is numbered from the end nearer the double "
      "bond, so the double bond starts at C-2 and the methyl group is on C-2.",
      ["Parent: pentene; number from the left: C1–C2(=C3)", "Double bond at 2, methyl at 2 → 2-methylpent-2-ene"],
      why_others_wrong="4-Methylpent-3-ene and 2-methylpent-3-ene number the chain from the wrong end, giving the "
                       "double bond a higher locant; 4-methylpent-2-ene is a different compound, "
                       "CH₃–CH=CH–CH(CH₃)–CH₃.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', IUPAC nomenclature", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "statement_pair",
      *sp("The members of a homologous series can be represented by a general formula, and successive members "
          "differ from each other by a –CH₂– unit.", True,
          "Alicyclic compounds, such as cyclohexane, show some properties similar to those of aliphatic compounds.",
          True),
      "Homologous series; alicyclic compounds",
      "A homologous series is a group of compounds with the same functional group, represented by a general "
      "formula, in which successive members differ by –CH₂–. NCERT notes that alicyclic (closed-chain, non-aromatic) "
      "compounds exhibit some properties similar to those of aliphatic compounds.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=30),

    Q(T_GO, "Reactive intermediates", "Basic", "assertion_reason",
      *ar("Alkyl free radicals are highly reactive species.", True,
          "The carbon atom of an alkyl free radical carries an unpaired electron and has only seven electrons in its "
          "valence shell, so it readily reacts to pair up this electron.", True, explains=True),
      "Free radicals as reactive intermediates",
      "Homolytic cleavage gives free radicals, in which a carbon atom carries an unpaired electron. With an "
      "incomplete octet, the radical reacts at once (for example with Cl₂ or another radical) to pair the "
      "electron, so free radicals are short-lived, highly reactive intermediates. R explains A.",
      ["A: true (reactive intermediate)", "R: true; the unpaired electron/incomplete octet is the cause"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', homolytic cleavage; free radicals",
      seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "match_list",
      *ml("Match the compound in List-I with its next higher homologue in List-II.",
          ["Methanal, HCHO", "Propanone, CH₃COCH₃", "Methanoic acid, HCOOH", "Methanamine, CH₃NH₂"],
          ["CH₃CH₂NH₂", "CH₃COOH", "CH₃COCH₂CH₃", "CH₃CHO"],
          "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D"),
      "Homologous series",
      "The next higher homologue has the same functional group and one more –CH₂– unit.",
      ["HCHO → CH₃CHO", "CH₃COCH₃ → CH₃COCH₂CH₃", "HCOOH → CH₃COOH", "CH₃NH₂ → CH₃CH₂NH₂"],
      why_others_wrong="The other codes pair a compound with a member of a different series (for example an "
                       "aldehyde with a ketone), which has a different functional group.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', homologous series", seconds=30),

    Q(T_GO, "Isomerism", "Intermediate", "direct",
      "Which of the following shows geometrical (cis–trans) isomerism?",
      ["1-Chloroprop-1-ene, ClCH=CH–CH₃", "2-Chloroprop-1-ene, CH₂=CCl–CH₃", "3-Chloroprop-1-ene, CH₂=CH–CH₂Cl",
       "1,1-Dichloroprop-1-ene, Cl₂C=CH–CH₃"], "A",
      "Condition for geometrical isomerism",
      "Geometrical isomerism about a C=C bond needs each doubly bonded carbon to carry two different groups. In "
      "ClCH=CH–CH₃, C-1 has H and Cl and C-2 has H and CH₃.",
      ["ClCH=CHCH₃: both carbons carry two different groups → cis and trans",
       "Other three: one doubly bonded carbon carries two identical groups"],
      why_others_wrong="2-Chloro- and 3-chloroprop-1-ene have a =CH₂ end (two H atoms); 1,1-dichloroprop-1-ene has "
                       "two Cl atoms on the same carbon.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', stereoisomerism", seconds=40),

    Q(T_GO, "Reactive intermediates", "Intermediate", "direct",
      "In which of the following does heterolytic cleavage of the indicated bond normally leave the shared pair of "
      "electrons on carbon, giving a carbanion?",
      ["The C–Br bond of CH₃CH₂Br", "The C–O bond of protonated ethanol, CH₃CH₂–OH₂⁺",
       "The C–Mg bond of CH₃CH₂MgBr", "The C–Cl bond of (CH₃)₃C–Cl"], "C",
      "Direction of heterolysis",
      "In heterolysis the shared pair goes to the more electronegative atom. Carbon is more electronegative than "
      "magnesium, so in a Grignard reagent the polar C–Mg bond leaves the electron pair on carbon (carbanion "
      "character). With Br, O or Cl, the more electronegative atom takes the pair and a carbocation forms.",
      ["C–Mg: carbon is the more electronegative atom → carbanion",
       "C–Br, C–O, C–Cl: the heteroatom takes the pair → carbocation"],
      why_others_wrong="Bromoethane, protonated ethanol and tert-butyl chloride all lose an electronegative leaving "
                       "group with the bonding pair, leaving a positively charged carbon.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', heterolytic cleavage", seconds=45),

    Q(T_GO, "Electronic effects", "Intermediate", "assertion_reason",
      *ar("The C–O bond in CH₃–OH is more polar than the C–S bond in CH₃–SH.", True,
          "Sulphur is more electronegative than oxygen.", False),
      "Bond polarity and electronegativity",
      "Oxygen is more electronegative than sulphur, so the electronegativity difference, and hence the polarity, is "
      "greater for the C–O bond. A is true; R is false.",
      ["A: true", "R: false; electronegativity O > S"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect; polarity of "
            "bonds", seconds=35),

    Q(T_GO, "Electronic effects", "Intermediate", "statement_pair",
      *sp("Hyperconjugation is possible in the methyl cation, CH₃⁺.", False,
          "Hyperconjugation is also possible in alkenes and alkylarenes.", True),
      "Hyperconjugation",
      "Hyperconjugation is the delocalisation of the σ electrons of a C–H bond of an alkyl group directly attached "
      "to an atom of an unsaturated system or to an atom with an unshared p orbital. CH₃⁺ has no alkyl group on the "
      "positive carbon (its own C–H bonds lie in the nodal plane of the empty p orbital), so it cannot be "
      "stabilised by hyperconjugation. NCERT notes hyperconjugation in alkenes (propene) and alkylarenes.",
      ["Statement I: false; no C–H bond adjacent to the cationic carbon", "Statement II: true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hyperconjugation", seconds=40),

    Q(T_GO, "Isomerism", "Intermediate", "match_list",
      *ml("Match the compound in List-I with the type of stereoisomerism it shows in List-II.",
          ["2-Chlorobutane", "Pent-2-ene", "4-Chloropent-2-ene, CH₃–CH=CH–CHCl–CH₃", "Propan-2-ol"],
          ["Both geometrical and optical isomerism", "Optical isomerism only", "Neither", "Geometrical isomerism only"],
          "II IV I III", ["IV II I III", "II IV III I", "I IV II III"], "B"),
      "Geometrical and optical isomerism",
      "Optical isomerism needs a carbon bonded to four different groups; geometrical isomerism needs two different "
      "groups on each doubly bonded carbon.",
      ["2-Chlorobutane: C-2 chiral, no C=C → optical only", "Pent-2-ene: cis/trans, no chiral carbon → geometrical only",
       "4-Chloropent-2-ene: cis/trans and chiral C-4 → both", "Propan-2-ol: C-2 has two CH₃ groups, no C=C → neither"],
      why_others_wrong="Codes that give pent-2-ene optical isomerism look for a chiral carbon that is not there; "
                       "codes that give propan-2-ol any isomerism overlook its two identical methyl groups.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', stereoisomerism", seconds=60),

    Q(T_GO, "Isomerism", "Intermediate", "multi_statement",
      *ms("Which of the following statements about structural isomerism are correct?",
          [("Butan-1-ol and 2-methylpropan-1-ol are chain isomers.", True),
           ("Propan-1-ol and propan-2-ol are position isomers.", True),
           ("Propanal and prop-2-en-1-ol (CH₂=CH–CH₂OH) are functional group isomers.", True),
           ("But-1-ene and 2-methylpropene are position isomers.", False),
           ("Methoxyethane and propan-2-ol are metamers.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "B"),
      "Chain, position and functional isomers; metamers",
      "Chain isomers differ in the carbon skeleton; position isomers differ in the position of the substituent or "
      "functional group on the same skeleton; functional isomers have different functional groups. Metamerism arises "
      "from different alkyl groups on either side of the same functional group.",
      ["(a) C₄H₁₀O, straight vs branched chain → true", "(b) –OH on C-1 vs C-2 → true",
       "(c) both C₃H₆O; aldehyde vs alcohol (with C=C) → true",
       "(d) straight vs branched skeleton → chain isomers, false",
       "(e) ether vs alcohol → functional isomers, not metamers, false"],
      why_others_wrong="Options with (d) mistake a change of skeleton for a change of position; the option with (e) "
                       "calls an ether–alcohol pair metamers, although metamers must share the functional group.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=75),

    Q(T_GO, "Types of organic reactions", "Intermediate", "multi_statement",
      *ms("For the reaction CH₃CH₂Br + HS⁻ → CH₃CH₂SH + Br⁻, which of the following statements are correct?",
          [("HS⁻ acts as the nucleophile.", True),
           ("CH₃CH₂Br is the substrate.", True),
           ("Br⁻ is the leaving group.", True),
           ("The carbon atom attacked by HS⁻ carries a partial negative charge.", False),
           ("The reaction is a substitution reaction.", True)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d", "e"]], "D"),
      "Substrate, reagent and reaction type",
      "The substrate supplies the carbon to the new bond: here CH₃CH₂Br. The reagent HS⁻ brings an electron pair, "
      "so it is a nucleophile, and it attacks the carbon bonded to bromine, which carries a partial positive charge "
      "because Br is more electronegative. Br⁻ leaves, and one group replaces another: a substitution.",
      ["(a), (b), (c), (e) true", "(d) false: the C–Br carbon is δ+"],
      why_others_wrong="Options containing (d) reverse the polarity of the C–Br bond; (a), (b) and (c) only leaves out "
                       "the correct classification as substitution.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', substrate and reagent; types of "
            "organic reactions", seconds=60),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "multi_statement",
      *ms("Which of the following statements about hybridisation and shape are correct?",
          [("In CH₃–C≡N, the carbon of the CH₃ group is sp³ and the nitrile carbon is sp hybridised.", True),
           ("In benzene, all six carbon atoms are sp² hybridised.", True),
           ("An sp² hybridised carbon is more electronegative than an sp³ hybridised carbon.", True),
           ("In propyne, CH₃–C≡CH, the C–C≡C bond angle is 120°.", False),
           ("In the carbocation (CH₃)₃C⁺, the positively charged carbon is sp³ hybridised.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Hybridisation, electronegativity and bond angles",
      "A carbon with four σ bonds is sp³, with one π bond sp², and with two π bonds sp. Greater s character makes "
      "the carbon more electronegative (sp > sp² > sp³). The sp carbons of an alkyne are linear (180°). The positive "
      "carbon of a carbocation uses three sp² orbitals and has an empty p orbital.",
      ["(a) true", "(b) true", "(c) true (33% vs 25% s character)", "(d) false: 180°", "(e) false: sp²"],
      why_others_wrong="(d) uses the sp² angle for sp carbons; (e) gives a carbocation the hybridisation of a "
                       "carbanion; options containing either are wrong.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation; carbocations",
      seconds=60),

    N(T_GO, "Isomerism", "Advanced",
      "How many of the following are functional group isomers of propanoic acid, CH₃CH₂COOH?\n"
      "Methyl ethanoate, ethyl methanoate, propanal, 2-hydroxypropanal (CH₃CH(OH)CHO), ethanoic acid, propan-1-ol, "
      "propane-1,2-diol",
      ["0", "1", "2", v_2411], "D", v_2411,
      "Functional group isomers: same molecular formula, different functional group",
      "Propanoic acid is C₃H₆O₂. A functional group isomer must have the same molecular formula but a different "
      "functional group. Check the formula of each compound first.",
      ["C₃H₆O₂: methyl ethanoate, ethyl methanoate (esters), 2-hydroxypropanal (aldehyde + alcohol) → isomers",
       "Propanal C₃H₆O, ethanoic acid C₂H₄O₂, propan-1-ol C₃H₈O, propane-1,2-diol C₃H₈O₂ → not isomers",
       "Count = 3"],
      why_others_wrong="2 counts only the two esters and misses the hydroxy aldehyde; lower counts also judge by "
                       "functional group alone without checking the molecular formula.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', functional group isomerism",
      seconds=75),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of HOOC–CH₂–CH(OH)–CH₂–C≡N is:",
      ["3-Hydroxy-4-cyanobutanoic acid", "4-Cyano-3-hydroxybutanoic acid", "4-Cyano-3-hydroxypentanoic acid",
       "4-Carboxy-3-hydroxybutanenitrile"], "B",
      "Principal functional group, prefixes and alphabetical order",
      "–COOH ranks above –CN, so the compound is named as a butanoic acid (C-1 = COOH, chain of four carbons). The "
      "–C≡N group, cited as a prefix (cyano), is not counted in the parent chain. Prefixes are cited "
      "alphabetically: cyano before hydroxy.",
      ["Principal group –COOH → '-oic acid'; parent chain C1–C4 = butanoic acid",
       "Substituents: OH on C-3, CN on C-4", "Alphabetical: 4-cyano-3-hydroxybutanoic acid"],
      why_others_wrong="'3-Hydroxy-4-cyano' breaks the alphabetical order; 'pentanoic acid' counts the nitrile carbon "
                       "both in the chain and in the prefix; naming it as a nitrile ignores the higher priority of "
                       "–COOH.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=60),

    Q(T_GO, "Reactive intermediates", "Advanced", "assertion_reason",
      *ar("In the tert-butyl cation, (CH₃)₃C⁺, the positively charged carbon and the three carbon atoms attached to "
          "it lie in one plane.", True,
          "The tert-butyl cation is more stable than the isopropyl cation, (CH₃)₂CH⁺.", True, explains=False),
      "Shape and stability of carbocations",
      "The planarity comes from the sp² hybridisation of the positive carbon: its three σ bonds lie in one plane "
      "at 120°, with the vacant p orbital perpendicular to it. R is a true but separate property: tert-butyl is more "
      "stable than isopropyl because of more hyperconjugation and +I effect of three methyl groups. Stability does "
      "not decide the shape (the isopropyl cation is planar too).",
      ["A: true (sp², trigonal planar)", "R: true (3° > 2°)", "R does not explain the planar shape"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', carbocations", seconds=50),

    Q(T_GO, "Isomerism", "Advanced", "statement_pair",
      *sp("2,3-Dimethylbutane and 2,2-dimethylbutane are chain isomers.", True,
          "Pentan-2-one and 3-methylbutan-2-one are position isomers.", False),
      "Chain versus position isomers",
      "Both pairs are C₆H₁₄ and C₅H₁₀O isomers respectively. 2,3- and 2,2-dimethylbutane differ in the carbon "
      "skeleton, so they are chain isomers. Pentan-2-one (straight chain) and 3-methylbutan-2-one (branched chain) "
      "also differ in the skeleton, with the C=O at C-2 in both; they are chain isomers, not position isomers.",
      ["Statement I: true", "Statement II: false; different skeletons → chain isomers"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "match_list",
      *ml("Match the structure in List-I with its IUPAC name in List-II.",
          ["CH₂=CH–CH₂–C≡N", "HC≡C–CH₂–CH₂–OH", "CH₃–CO–CH₂–CHO", "HO–CH₂–CH₂–COO–CH₃"],
          ["Methyl 3-hydroxypropanoate", "3-Oxobutanal", "But-3-enenitrile", "But-3-yn-1-ol"],
          "III IV II I", ["III IV I II", "IV III II I", "II IV III I"], "A"),
      "Naming polyfunctional compounds",
      "The principal group decides the suffix and gets the lowest locant; the nitrile carbon is C-1 of the chain; "
      "the –CHO carbon is C-1 and a ketonic C=O is cited as 'oxo'; esters are named alkyl alkanoate.",
      ["CH₂=CH–CH₂–CN: C1 = CN, C=C at 3 → but-3-enenitrile",
       "HC≡C–CH₂–CH₂OH: C1 bears OH, C≡C at 3 → but-3-yn-1-ol",
       "CH₃COCH₂CHO: C1 = CHO, C=O at 3 → 3-oxobutanal",
       "HOCH₂CH₂COOCH₃: methyl ester of 3-hydroxypropanoic acid"],
      why_others_wrong="Codes that swap the ester and the oxo-aldehyde mistake a –COO– group for a ketone; codes "
                       "that swap the nitrile and the alkynol ignore which group carries C-1.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', IUPAC nomenclature", seconds=75),

    Q(T_GO, "Reactive intermediates", "Advanced", "multi_statement",
      *ms("Which of the following statements about carbocations are correct?",
          [("In CH₃CH₂⁺, the C–H bonds of the CH₃ group, not those on the positively charged carbon, take part in "
            "hyperconjugation.", True),
           ("The benzyl cation, C₆H₅CH₂⁺, is stabilised by delocalisation of its positive charge over the benzene "
            "ring.", True),
           ("The isopropyl cation, (CH₃)₂CH⁺, has six C–H bonds that can take part in hyperconjugation.", True),
           ("Carbocations behave as nucleophiles because they carry a positive charge.", False),
           ("The order of stability of carbocations is CH₃⁺ > CH₃CH₂⁺ > (CH₃)₂CH⁺.", False)],
          [["a", "b", "d"], ["c", "d", "e"], ["a", "b", "c", "e"]], "B"),
      "Stability and reactivity of carbocations",
      "Hyperconjugation uses C–H bonds on carbons adjacent to the positive carbon: three in CH₃CH₂⁺ and six in "
      "(CH₃)₂CH⁺. Benzylic and allylic carbocations are stabilised by resonance. Carbocations are electron "
      "deficient and act as electrophiles; their stability order is 3° > 2° > 1° > CH₃⁺.",
      ["(a) true", "(b) true", "(c) true: two CH₃ groups × 3 C–H", "(d) false: electrophiles",
       "(e) false: the order is reversed"],
      why_others_wrong="Options with (d) confuse electron-deficient species with nucleophiles; the option with (e) "
                       "reverses the stability order.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', carbocations; hyperconjugation; "
            "resonance", seconds=70),
]
