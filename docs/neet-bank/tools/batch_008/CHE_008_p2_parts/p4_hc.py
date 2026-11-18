
# ================================================================ Hydrocarbons (1916-1931)
# 1916: CH4 + 2O2 -> CO2 + 2H2O, dcH = -890 kJ/mol; 4.0 g CH4
v_1916 = f"{float(F(4, mm(C=1, H=4)) * 890):.1f} kJ"
assert v_1916 == "222.5 kJ"
# 1920: CH3CHBrCH2Br (M 202) + 2 NaNH2 -> CH3C≡CH (M 40)
n_1920 = F(202, 10) / mm(C=3, H=6, Br=2)
assert n_1920 == F(1, 10)
v_1920 = g(n_1920 * mm(C=3, H=4))
assert v_1920 == "4.0 g"
# 1921: CH4 + 4Cl2 -> CCl4 + 4HCl; 1.6 g CH4
v_1921 = g(F(16, 10) / mm(C=1, H=4) * 4 * 2 * AM["Cl"])
assert v_1921 == "28.4 g"
# 1922: alkenes giving propanone on ozonolysis (have a (CH3)2C= end)
gives_acetone = {"2-methylpropene": True, "2,3-dimethylbut-2-ene": True, "2-methylbut-2-ene": True,
                 "but-2-ene": False, "propene": False, "2-methylbut-1-ene": False, "3-methylbut-1-ene": False}
v_1922 = str(sum(gives_acetone.values()))
assert v_1922 == "3"
# 1925: equal masses of C6H6 and C2H2 -> mol CO2 per gram identical (both CH empirical formula)
co2_benz = F(78, 10) / mm(C=6, H=6) * 6
co2_ethy = F(78, 10) / mm(C=2, H=2) * 2
assert co2_benz == co2_ethy == F(6, 10)
v_1925 = "1 : 1"
# 1927: distinct mononitro derivatives of o-, m-, p-xylene
def ring_canon(labels):
    forms = []
    for r in range(6):
        for sgn in (1, -1):
            forms.append(tuple(labels[(sgn * i + r) % 6] for i in range(6)))
    return min(forms)
def mononitro(me_positions):
    out = set()
    for p in range(6):
        if p in me_positions:
            continue
        lab = ["M" if i in me_positions else ("N" if i == p else "H") for i in range(6)]
        out.add(ring_canon(lab))
    return len(out)
xyl = {"o": mononitro({0, 1}), "m": mononitro({0, 2}), "p": mononitro({0, 3})}
assert xyl == {"o": 2, "m": 3, "p": 1}
v_1927 = str(sum(xyl.values()))
assert v_1927 == "6"
# 1930: monochloro structural isomers (distinct H environments)
mono = {"2,2-dimethylpropane": 1, "n-butane": 2, "n-pentane": 3, "3-methylpentane": 4}
assert sorted(mono.values()) == [1, 2, 3, 4]

QUESTIONS += [
    N(T_HC, "Alkanes and conformations", "Basic",
      "Methane burns completely according to CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l); ΔcH = −890 kJ mol⁻¹. The heat "
      "released by the complete combustion of 4.0 g of methane is (C = 12, H = 1):",
      ["890 kJ", "55.6 kJ", "3560 kJ", "222.5 kJ"], "D", v_1916,
      "Heat of combustion of alkanes",
      "The enthalpy change is for one mole of methane, so scale it by the number of moles burnt.",
      ["M(CH₄) = 16 g mol⁻¹ → n = 4.0/16 = 0.25 mol", "q = 0.25 × 890 = 222.5 kJ released"],
      why_others_wrong="890 kJ is for one whole mole; 55.6 kJ is the heat per gram (890/16); 3560 kJ multiplies by "
                       "4 instead of dividing by the molar mass.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: combustion", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Basic", "direct",
      "In the sulphonation of benzene with fuming sulphuric acid (oleum), the electrophile that attacks the ring is:",
      ["H₃O⁺", "SO₃", "HSO₄⁻", "SO₄²⁻"], "B",
      "Electrophiles in aromatic substitution",
      "Fuming sulphuric acid contains dissolved SO₃. Sulphur in SO₃ is strongly electron-deficient, so SO₃ is the "
      "electrophile that attacks the π electrons of the ring, giving benzenesulphonic acid.",
      ["Oleum = H₂SO₄ + SO₃", "SO₃ (electron-deficient S) attacks the ring", "Product: C₆H₅SO₃H"],
      why_others_wrong="H₃O⁺ does not substitute the ring; HSO₄⁻ and SO₄²⁻ are anions (electron-rich) and cannot act "
                       "as electrophiles.",
      ncert=f"{NC11}, 'Hydrocarbons', electrophilic substitution reactions: sulphonation", seconds=25),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "match_list",
      *ml("Match the method of preparing an alkene in List-I with the name of the process in List-II.",
          ["Heating an alkyl halide with alcoholic KOH", "Heating a vicinal dihalide with zinc metal",
           "Heating an alcohol with concentrated H₂SO₄", "Hydrogenating an alkyne over Lindlar's catalyst"],
          ["Partial reduction", "Acidic dehydration", "Dehydrohalogenation", "Dehalogenation"],
          "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "C"),
      "Preparation of alkenes",
      "Alcoholic KOH removes HX (dehydrohalogenation); zinc removes two halogen atoms from adjacent carbons "
      "(dehalogenation); concentrated H₂SO₄ removes water from an alcohol (acidic dehydration); Lindlar's catalyst "
      "stops hydrogenation of an alkyne at the alkene (partial reduction).",
      ["A → dehydrohalogenation (III)", "B → dehalogenation (IV)", "C → acidic dehydration (II)",
       "D → partial reduction (I)"],
      why_others_wrong="The other codes interchange the halogen-removing processes or the dehydration and partial "
                       "reduction.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Basic", "statement_pair",
      *sp("Among isomeric alkanes, the straight-chain isomer has the highest boiling point.", True,
          "2,2-Dimethylpropane (neopentane) has a higher boiling point than 2-methylbutane (isopentane).", False),
      "Effect of branching on boiling points of alkanes",
      "Branching makes a molecule more compact (nearly spherical), reducing its surface area and therefore the van "
      "der Waals forces. So the boiling point falls as branching increases: n-pentane (309 K) > isopentane (301 K) > "
      "neopentane (282.5 K). Statement I is true and Statement II false.",
      ["More branching → smaller surface area → weaker van der Waals forces → lower b.p.",
       "n-pentane > isopentane > neopentane"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: physical properties", seconds=30),

    N(T_HC, "Alkynes", "Basic",
      "1,2-Dibromopropane, CH₃–CHBr–CH₂Br, is converted into propyne by treatment with alcoholic KOH followed by "
      "sodamide. The mass of propyne obtained from 20.2 g of 1,2-dibromopropane, assuming complete conversion, is "
      "(C = 12, H = 1, Br = 80):",
      ["8.0 g", "4.0 g", "4.2 g", "2.0 g"], "B", v_1920,
      "Preparation of alkynes from vicinal dihalides",
      "Two molecules of HBr are removed from one molecule of the vicinal dihalide, so 1 mol of dihalide gives 1 mol "
      "of propyne.",
      ["M(C₃H₆Br₂) = 36 + 6 + 160 = 202 g mol⁻¹ → n = 0.10 mol", "n(C₃H₄) = 0.10 mol",
       "Mass = 0.10 × 40 = 4.0 g"],
      why_others_wrong="4.2 g is the mass of propene (only one HBr removed); 8.0 g and 2.0 g double or halve the mole "
                       "ratio.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkynes from vicinal dihalides", seconds=45),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "Methane is chlorinated in light until it is converted completely into tetrachloromethane:\n"
      "CH₄ + 4Cl₂ → CCl₄ + 4HCl\n"
      "The minimum mass of chlorine needed for 1.6 g of methane is (C = 12, H = 1, Cl = 35.5):",
      ["7.1 g", "14.2 g", "56.8 g", "28.4 g"], "D", v_1921,
      "Stepwise free-radical chlorination of methane",
      "Each substitution replaces one H by Cl and uses one Cl₂ molecule (the other Cl atom leaves as HCl). Four "
      "hydrogens are replaced, so 4 mol Cl₂ per mol CH₄.",
      ["n(CH₄) = 1.6/16 = 0.10 mol", "n(Cl₂) = 4 × 0.10 = 0.40 mol", "Mass = 0.40 × 71 = 28.4 g"],
      why_others_wrong="7.1 g uses one Cl₂ per CH₄; 14.2 g uses Cl (35.5) instead of Cl₂ (71) for 0.40 mol; 56.8 g "
                       "counts eight Cl₂ per CH₄.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation", seconds=45),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "How many of the following alkenes give propanone as one of the products of ozonolysis (O₃, then Zn/H₂O)?\n"
      "2-Methylpropene, 2,3-dimethylbut-2-ene, 2-methylbut-2-ene, but-2-ene, propene, 2-methylbut-1-ene, "
      "3-methylbut-1-ene",
      ["2", "3", "4", "5"], "B", v_1922,
      "Ozonolysis: each doubly bonded carbon becomes a carbonyl carbon",
      "Propanone, (CH₃)₂C=O, is formed only from a doubly bonded carbon that carries two methyl groups, i.e. an "
      "alkene containing (CH₃)₂C=.",
      ["2-Methylpropene: (CH₃)₂C=CH₂ → yes", "2,3-Dimethylbut-2-ene: (CH₃)₂C=C(CH₃)₂ → yes (2 mol)",
       "2-Methylbut-2-ene: (CH₃)₂C=CHCH₃ → yes", "But-2-ene → ethanal only; propene → ethanal + methanal",
       "2-Methylbut-1-ene → butanone + methanal; 3-methylbut-1-ene → 2-methylpropanal + methanal", "Total = 3"],
      why_others_wrong="4 or 5 count 2-methylbut-1-ene or 3-methylbut-1-ene, whose (CH₃) groups are not both on a "
                       "doubly bonded carbon; 2 misses one of the three correct alkenes.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: ozonolysis", seconds=75),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "assertion_reason",
      *ar("When a single alkyl halide is used in the Wurtz reaction, the alkane formed has twice the number of carbon "
          "atoms present in the alkyl halide.", True,
          "In the Wurtz reaction, two alkyl groups from two molecules of the alkyl halide are joined by a new C–C "
          "bond when the halide is treated with sodium in dry ether.", True, explains=True),
      "Wurtz reaction",
      "2R–X + 2Na → R–R + 2NaX. Because the product joins two identical R groups, it has double the carbon atoms "
      "of R–X (e.g. CH₃Br → ethane, C₂H₅Br → butane). R is why A is true.",
      ["2R–X + 2Na → R–R + 2NaX", "Carbon count of R–R = 2 × carbon count of R"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes: Wurtz reaction", seconds=35),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "multi_statement",
      *ms("Which of the following statements about benzene are correct?",
          [("Under ordinary conditions benzene prefers electrophilic substitution to addition.", True),
           ("All six carbon atoms of benzene are sp² hybridised and the ring is planar.", True),
           ("Benzene has (4n + 2) π electrons with n = 1.", True),
           ("Benzene is hydrogenated over nickel at high temperature and pressure mainly to cyclohexene.", False),
           ("The Kekulé structure with fixed alternate single and double bonds explains the equal lengths of all "
            "the C–C bonds.", False)],
          [["a", "b"], ["b", "c", "d"], ["a", "c", "e"]], "D"),
      "Structure and stability of benzene",
      "Substitution keeps the aromatic sextet, so benzene favours it. The six sp² carbons form a planar ring whose six "
      "π electrons (n = 1 in 4n + 2) are delocalised. Hydrogenation over Ni goes on to cyclohexane. A Kekulé structure "
      "would have unequal bonds; the equal 139 pm bonds are explained by resonance.",
      ["(a) true", "(b) true", "(c) true", "(d) false: cyclohexane", "(e) false: resonance hybrid explains it"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: structure of benzene", seconds=55),

    N(T_HC, "Benzene and aromaticity", "Intermediate",
      "Equal masses (7.8 g each) of benzene, C₆H₆, and ethyne, C₂H₂, are burnt completely in oxygen. The ratio of "
      "the volumes of carbon dioxide formed from benzene and from ethyne, measured under the same conditions, is "
      "(C = 12, H = 1):",
      ["3 : 1", "1 : 3", "1 : 1", "6 : 1"], "C", v_1925,
      "Same empirical formula → same CO₂ per gram",
      "Benzene and ethyne both have the empirical formula CH. Equal masses therefore contain the same number of moles "
      "of carbon atoms, and each carbon atom gives one CO₂.",
      ["Benzene: 7.8/78 = 0.10 mol × 6 C = 0.60 mol CO₂", "Ethyne: 7.8/26 = 0.30 mol × 2 C = 0.60 mol CO₂",
       "Ratio = 1 : 1"],
      why_others_wrong="3 : 1 compares the carbon atoms per molecule (6 : 2) without using moles; 1 : 3 compares the "
                       "moles of the two hydrocarbons; 6 : 1 compares the carbon atoms per molecule with one mole of "
                       "ethyne giving one CO₂.",
      ncert=f"{NC11}, 'Hydrocarbons', combustion of hydrocarbons", seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "statement_pair",
      *sp("The addition of HBr to propene in the presence of benzoyl peroxide takes place by a free-radical "
          "mechanism.", True,
          "Addition of HBr to an unsymmetrical alkene in the presence of a peroxide is also called the peroxide effect "
          "or Kharash effect.", True),
      "Anti-Markovnikov addition of HBr",
      "Benzoyl peroxide forms free radicals that generate Br• from HBr; Br• adds to give the more stable free radical, "
      "so the product is 1-bromopropane (anti-Markovnikov). NCERT calls this the peroxide or Kharash effect. Both "
      "statements are true.",
      ["Peroxide → radicals → Br•", "Br• adds to CH₂ end → secondary radical → 1-bromopropane",
       "Named peroxide (Kharash) effect"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: anti-Markovnikov addition", seconds=35),

    N(T_HC, "Electrophilic substitution", "Advanced",
      "Each of the three xylenes (o-, m- and p-dimethylbenzene) is mononitrated on the ring. Counting only "
      "structurally different products, the total number of mononitro derivatives that can be obtained from all "
      "three xylenes together is:",
      ["5", "6", "7", "4"], "B", v_1927,
      "Counting distinct ring positions in disubstituted benzenes",
      "Use the symmetry of each xylene to find how many ring positions are different.",
      ["o-Xylene (1,2): positions 3 (=6) and 4 (=5) → 2 products",
       "m-Xylene (1,3): positions 2, 4 (=6) and 5 → 3 products",
       "p-Xylene (1,4): all four free positions equivalent → 1 product", "Total = 2 + 3 + 1 = 6"],
      why_others_wrong="5 misses position 2 of m-xylene (between the methyl groups); 7 counts positions 4 and 6 of "
                       "m-xylene separately; 4 assumes each xylene has the same number of products as toluene's o/p.",
      ncert=f"{NC11}, 'Hydrocarbons', isomerism in aromatic compounds and electrophilic substitution", seconds=90),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "direct",
      "An alkene X, C₆H₁₂, on ozonolysis (O₃, then Zn/H₂O) gives one mole of ethanal and one mole of butanone per "
      "mole of X. X is:",
      ["Hex-2-ene", "2-Methylpent-2-ene", "3-Methylpent-1-ene", "3-Methylpent-2-ene"], "D",
      "Working back from ozonolysis products",
      "Join the two carbonyl carbons by a double bond after removing the oxygen atoms: CH₃CH=O + O=C(CH₃)CH₂CH₃ → "
      "CH₃CH=C(CH₃)CH₂CH₃. The longest chain containing the double bond has five carbons, with a methyl group on C-3.",
      ["Ethanal: CH₃CH= ; butanone: =C(CH₃)CH₂CH₃", "X = CH₃–CH=C(CH₃)–CH₂–CH₃", "Name: 3-methylpent-2-ene"],
      why_others_wrong="Hex-2-ene gives ethanal and butanal; 2-methylpent-2-ene gives propanone and propanal; "
                       "3-methylpent-1-ene gives methanal and 2-methylbutanal.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: ozonolysis", seconds=60),

    Q(T_HC, "Alkynes", "Advanced", "assertion_reason",
      *ar("Hydrogenation of but-2-yne over palladium on charcoal partially deactivated with quinoline gives "
          "cis-but-2-ene.", True,
          "Reduction of but-2-yne with sodium in liquid ammonia gives trans-but-2-ene.", True, explains=False),
      "Partial reduction of alkynes to cis and trans alkenes",
      "Lindlar's catalyst stops the hydrogenation at the alkene stage and gives the cis alkene. Sodium in liquid "
      "ammonia gives the trans alkene. Both statements are true, but R describes a different reagent and a different "
      "product; it does not explain why Lindlar reduction gives the cis isomer.",
      ["Lindlar (Pd/C + quinoline) → cis-alkene: A true", "Na/liquid NH₃ → trans-alkene: R true",
       "R is about another reaction → not the explanation"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from alkynes", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Advanced", "match_list",
      *ml("Match the alkane in List-I with the number of structurally different monochloro derivatives it can give "
          "on free-radical chlorination (List-II).",
          ["2,2-Dimethylpropane", "n-Butane", "n-Pentane", "3-Methylpentane"],
          ["2", "4", "1", "3"],
          "III I IV II", ["I III IV II", "III I II IV", "III IV I II"], "D"),
      "Counting different kinds of hydrogen atoms",
      "Each set of equivalent hydrogen atoms gives one monochloro product.",
      ["Neopentane: all 12 H equivalent → 1 (III)", "n-Butane: CH₃ and CH₂ → 2 (I)",
       "n-Pentane: C1, C2, C3 → 3 (IV)", "3-Methylpentane: C1, C2, C3 and the branch CH₃ → 4 (II)"],
      why_others_wrong="The other codes miscount n-pentane (forgetting C-3) or 3-methylpentane (forgetting the "
                       "branch methyl or the tertiary C-3).",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation", seconds=70),

    Q(T_HC, "Alkanes and conformations", "Advanced", "multi_statement",
      *ms("Which of the following statements about the chemical reactions of alkanes are correct?",
          [("On pyrolysis, dodecane gives a mixture containing heptane and pentene, among other products.", True),
           ("Under normal conditions alkanes are generally inert towards acids, bases and most oxidising and "
            "reducing agents.", True),
           ("Free-radical chlorination of methane proceeds through a carbocation intermediate.", False),
           ("Heating n-alkanes with anhydrous AlCl₃ and HCl gas converts them into branched-chain isomers.", True),
           ("Complete combustion of an alkane gives carbon monoxide and hydrogen.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "d"]], "C"),
      "Reactions of alkanes",
      "Pyrolysis (cracking) breaks large alkanes into smaller alkanes and alkenes, e.g. C₁₂H₂₆ → C₇H₁₆ + C₅H₁₀ + "
      "other products. Alkanes are generally inert to most reagents under ordinary conditions. Halogenation is a "
      "free-radical chain reaction. Anhydrous AlCl₃/HCl isomerises n-alkanes. Complete combustion gives CO₂ and H₂O.",
      ["(a) true", "(b) true", "(c) false: free radicals", "(d) true", "(e) false: CO₂ and H₂O"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: chemical properties", seconds=60),
]
