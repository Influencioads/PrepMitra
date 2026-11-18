
# ================================================================ Coordination Compounds (2373-2388)
# 2375: heteroleptic entities in the list
het_2375 = {"[Co(NH3)6]3+": 1, "[Co(NH3)4Cl2]+": 2, "[Ni(CO)4]": 1, "[Fe(CN)6]4-": 1, "[Co(en)2Cl2]+": 2,
            "[Pt(NH3)2Cl2]": 2, "[Cr(C2O4)3]3-": 1, "[Co(NH3)5(H2O)]3+": 2}  # number of kinds of ligand
v_2375 = str(sum(1 for k in het_2375.values() if k > 1))
assert v_2375 == "4"
# 2378: only [Co(NH3)5Br]SO4 releases free sulphate; 0.010 mol BaSO4
m_2378 = F(10, 1000) * (AM["Ba"] + AM["S"] + 4 * AM["O"])
assert m_2378 == F(233, 100)
v_2378 = f"{float(m_2378):.2f} g"
# 2379: Cr3+ d3, t2g3: CFSE = 3 x (-0.4 Do) = -1.2 Do; Do = 260 kJ/mol
cfse = lambda t2g, eg: F(-4, 10) * t2g + F(6, 10) * eg
e_2379 = cfse(3, 0) * 260
assert e_2379 == -312
v_2379 = "−312 kJ mol⁻¹"
assert (F(-4, 10) * 260, F(-6, 10) * 260, F(-18, 10) * 260) == (-104, -156, -468)
# 2384: 2.665 g of CrCl3.6H2O (266.5 g/mol) gives 2.87 g AgCl (143.5 g/mol) -> 2 ionisable Cl
M_2384 = AM["Cr"] + 3 * AM["Cl"] + 6 * mm(H=2, O=1)
assert M_2384 == F(2665, 10)
n_cplx = F(2665, 1000) / M_2384
n_agcl = F(287, 100) / (AM["Ag"] + AM["Cl"])
assert n_cplx == F(1, 100) and n_agcl == F(2, 100) and n_agcl / n_cplx == 2
v_2384 = "[Cr(H₂O)₅Cl]Cl₂·H₂O"
# 2385: [Cr(NH3)6]3+ (d3, 3 unpaired) + [Fe(CN)6]3- (low-spin d5, 1 unpaired)
v_2385 = str(3 + 1)
assert v_2385 == "4" and 3 + 5 == 8
# 2388: CFSE values (ignoring pairing): HS d5 = 0, d10 = 0, HS d4 = -0.6, LS d5 = -2.0
assert cfse(3, 2) == 0 and cfse(6, 4) == 0 and cfse(3, 1) == F(-6, 10) and cfse(5, 0) == -2
assert abs(cfse(3, 2)) < abs(cfse(3, 1))  # statement (e) is false

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of the complex ion [Pt(NH₃)BrCl(NO₂)]⁻, in which the nitrite ligand is bonded through "
      "nitrogen, is:",
      ["Amminebromidochloridonitrito-N-platinum(II) ion", "Amminechloridobromidonitrito-N-platinate(II) ion",
       "Amminebromidochloridonitrito-N-platinate(II) ion", "Amminebromidochloridonitrito-N-platinate(IV) ion"], "C",
      "Naming an anionic coordination entity",
      "The ligands are named in alphabetical order: ammine, bromido, chlorido, nitrito-N. The oxidation state of "
      "platinum is x + 0 − 1 − 1 − 1 = −1, so x = +2. Because the entity is an anion, the metal name takes the "
      "ending -ate: platinate(II).",
      ["Ligands alphabetically: ammine (a), bromido (b), chlorido (c), nitrito-N (n)",
       "Oxidation state: x − 3 = −1 → x = +2", "Anionic entity → platinate(II)"],
      why_others_wrong="'Platinum(II)' is used only when the entity is a cation or neutral; chlorido before bromido "
                       "breaks the alphabetical order; (IV) ignores the three anionic ligands in the charge balance.",
      ncert=f"{NC12}, 'Coordination Compounds', naming of mononuclear coordination compounds", seconds=40),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The formula of dichloridobis(ethane-1,2-diamine)platinum(IV) nitrate is:",
      ["[PtCl₂(en)₂]NO₃", "[PtCl₂(en)₂](NO₃)₄", "[Pt(en)₂]Cl₂(NO₃)₂", "[PtCl₂(en)₂](NO₃)₂"], "D",
      "Writing the formula from the name",
      "The coordination entity contains two chloride ions and two neutral en ligands around Pt⁴⁺, so its charge is "
      "+4 − 2 = +2. Two nitrate ions balance this charge.",
      ["Entity: [PtCl₂(en)₂]ˣ, x = +4 + 2(−1) + 2(0) = +2", "Two NO₃⁻ counter ions → [PtCl₂(en)₂](NO₃)₂"],
      why_others_wrong="One or four nitrate ions do not balance a +2 entity; writing the chlorides outside the square "
                       "brackets contradicts the name, which lists them as ligands (dichlorido).",
      ncert=f"{NC12}, 'Coordination Compounds', formulas of mononuclear coordination entities", seconds=30),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "How many of the following coordination entities are heteroleptic?\n"
      "[Co(NH₃)₆]³⁺, [Co(NH₃)₄Cl₂]⁺, [Ni(CO)₄], [Fe(CN)₆]⁴⁻, [Co(en)₂Cl₂]⁺, [Pt(NH₃)₂Cl₂], [Cr(C₂O₄)₃]³⁻, "
      "[Co(NH₃)₅(H₂O)]³⁺",
      ["3", v_2375, "5", "6"], "B", v_2375,
      "Homoleptic and heteroleptic complexes",
      "A complex in which the metal is bound to only one kind of donor group is homoleptic; one bound to more than "
      "one kind of donor group is heteroleptic.",
      ["Homoleptic: [Co(NH₃)₆]³⁺, [Ni(CO)₄], [Fe(CN)₆]⁴⁻, [Cr(C₂O₄)₃]³⁻",
       "Heteroleptic: [Co(NH₃)₄Cl₂]⁺, [Co(en)₂Cl₂]⁺, [Pt(NH₃)₂Cl₂], [Co(NH₃)₅(H₂O)]³⁺ → 4"],
      why_others_wrong="3 usually misses [Co(NH₃)₅(H₂O)]³⁺, where one water molecule makes the complex heteroleptic; "
                       "5 or 6 counts charged or chelate complexes such as [Fe(CN)₆]⁴⁻ or [Cr(C₂O₄)₃]³⁻, which have "
                       "only one kind of ligand.",
      ncert=f"{NC12}, 'Coordination Compounds', homoleptic and heteroleptic complexes", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Basic", "statement_pair",
      *sp("According to Werner's theory, the secondary valence of the central metal ion in a complex corresponds to "
          "its coordination number.", True,
          "In [Co(en)₃]Cl₃ (en = ethane-1,2-diamine), the secondary valence of cobalt is 3.", False),
      "Primary and secondary valences",
      "Werner's secondary valence is the coordination number. Each en is didentate, so three en ligands supply six "
      "donor nitrogen atoms: the coordination number (secondary valence) of cobalt is 6. Its primary valence "
      "(oxidation state) is 3.",
      ["Statement I: true (secondary valence = coordination number)",
       "Statement II: false; 3 en × 2 donor atoms = 6, so the secondary valence is 6"],
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory; coordination number", seconds=35),

    Q(T_CC, "Werner's theory and ligands", "Basic", "match_list",
      *ml("Match the ligand in List-I with the donor atom(s) through which it binds the metal in List-II.",
          ["Ethane-1,2-diamine (en)", "Oxalate ion, C₂O₄²⁻", "Carbonyl, CO", "Nitrite ion, bound as nitrito-O"],
          ["One oxygen atom", "Two nitrogen atoms", "One carbon atom", "Two oxygen atoms"],
          "II IV III I", ["II I III IV", "IV II III I", "II IV I III"], "D"),
      "Donor atoms of common ligands",
      "en, H₂N–CH₂–CH₂–NH₂, is didentate through its two nitrogen atoms; oxalate is didentate through two oxygen "
      "atoms; CO binds through carbon; the ambidentate nitrite ion binds through oxygen in the nitrito-O form.",
      ["en → two N", "C₂O₄²⁻ → two O", "CO → C", "–ONO → one O"],
      why_others_wrong="Codes that give oxalate a single oxygen confuse it with nitrito-O; code with CO → one O "
                       "forgets that CO donates the lone pair on carbon.",
      ncert=f"{NC12}, 'Coordination Compounds', ligands: didentate and ambidentate ligands", seconds=40),

    N(T_CC, "Isomerism", "Intermediate",
      "[Co(NH₃)₅Br]SO₄ and [Co(NH₃)₅(SO₄)]Br are ionisation isomers. 0.010 mol of each is dissolved together in "
      "water and an excess of BaCl₂ solution is added. The mass of BaSO₄ precipitated is (Ba = 137, S = 32, "
      "O = 16):",
      ["0 g", "1.17 g", v_2378, "4.66 g"], "C", v_2378,
      "Ionisation isomers give different ions in solution",
      "In [Co(NH₃)₅Br]SO₄ the sulphate is a counter ion and is free in solution, so it is precipitated by Ba²⁺. In "
      "[Co(NH₃)₅(SO₄)]Br the sulphate is coordinated to cobalt and is not available; this isomer gives free Br⁻ "
      "instead.",
      ["Free SO₄²⁻ comes only from [Co(NH₃)₅Br]SO₄: 0.010 mol", "BaSO₄ = 0.010 × 233 = 2.33 g"],
      why_others_wrong="4.66 g assumes that both isomers release sulphate; 1.17 g halves the correct amount; 0 g "
                       "assumes that sulphate is never free in a cobalt ammine complex.",
      ncert=f"{NC12}, 'Coordination Compounds', structural isomerism: ionisation isomerism", seconds=60),

    N(T_CC, "Crystal field theory", "Intermediate",
      "For the octahedral complex [Cr(NH₃)₆]³⁺ (Z of Cr = 24), the crystal field splitting energy Δo is "
      "260 kJ mol⁻¹. Taking the energy of each t₂g electron as −0.4Δo and of each eg electron as +0.6Δo, the "
      "crystal field stabilisation energy of the complex is:",
      [v_2379, "−104 kJ mol⁻¹", "−156 kJ mol⁻¹", "−468 kJ mol⁻¹"], "A", v_2379,
      "Crystal field stabilisation energy of a d³ ion",
      "Cr³⁺ is 3d³. In an octahedral field the three electrons occupy the t₂g orbitals singly (t₂g³ eg⁰), "
      "whatever the field strength, so CFSE = 3 × (−0.4Δo) = −1.2Δo.",
      ["Cr³⁺: 3d³ → t₂g³ eg⁰", "CFSE = 3 × (−0.4 × 260) = −312 kJ mol⁻¹"],
      why_others_wrong="−104 kJ mol⁻¹ counts only one electron; −156 kJ mol⁻¹ uses 0.6Δo for a single electron; "
                       "−468 kJ mol⁻¹ uses 0.6Δo for each of the three electrons, the eg value, with a minus sign.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=60),

    Q(T_CC, "Valence bond theory", "Intermediate", "assertion_reason",
      *ar("[Mn(CN)₆]³⁻ has two unpaired electrons, whereas [MnCl₆]³⁻ has four unpaired electrons (Z of Mn = 25).",
          True,
          "CN⁻ is a strong field ligand that makes two of the four 3d electrons of Mn³⁺ pair up, whereas Cl⁻ is a "
          "weak field ligand that cannot do so.", True, explains=True),
      "Magnetic behaviour of inner and outer orbital complexes",
      "Mn³⁺ is 3d⁴. With CN⁻ the electrons pair into three 3d orbitals (two unpaired), leaving two 3d orbitals for "
      "d²sp³ hybridisation. With Cl⁻ no pairing occurs, so four electrons stay unpaired and the outer 4d orbitals are "
      "used (sp³d²). The ligand field strength is exactly why the numbers differ.",
      ["Mn³⁺: 3d⁴", "CN⁻ (strong field): paired → 2 unpaired, inner orbital",
       "Cl⁻ (weak field): unpaired → 4 unpaired, outer orbital"],
      ncert=f"{NC12}, 'Coordination Compounds', magnetic properties of coordination compounds", seconds=45),

    Q(T_CC, "Valence bond theory", "Intermediate", "multi_statement",
      *ms("Which of the following statements, based on valence bond theory, are correct?",
          [("dsp² hybridisation of the central atom gives a square planar coordination entity.", True),
           ("sp³d hybridisation of the central atom gives a trigonal bipyramidal coordination entity.", True),
           ("In [CoF₆]³⁻, the six 3d electrons of Co³⁺ are paired up in three 3d orbitals.", False),
           ("An inner orbital complex uses (n−1)d orbitals in hybridisation, whereas an outer orbital complex uses "
            "nd orbitals.", True),
           ("Every inner orbital octahedral complex is diamagnetic.", False)],
          [["a", "b", "d", "e"], ["b", "c", "d"], ["a", "d"]], "B"),
      "Hybridisation, geometry and inner/outer orbital complexes",
      "dsp² → square planar and sp³d → trigonal bipyramidal. In [CoF₆]³⁻, F⁻ is a weak field ligand: the 3d⁶ "
      "electrons stay unpaired as far as possible (four unpaired) and cobalt uses sp³d² hybrid orbitals. Inner "
      "orbital complexes use (n−1)d orbitals, but they need not be diamagnetic: [Fe(CN)₆]³⁻ has one and "
      "[Cr(NH₃)₆]³⁺ three unpaired electrons.",
      ["(a) true", "(b) true", "(c) false: [CoF₆]³⁻ has four unpaired electrons (outer orbital)",
       "(d) true", "(e) false: [Fe(CN)₆]³⁻ and [Cr(NH₃)₆]³⁺ are inner orbital yet paramagnetic"],
      why_others_wrong="Options with (e) forget paramagnetic inner orbital complexes; options with (c) treat F⁻ as "
                       "a strong field ligand; (a) and (d) only leaves out the correct shape for sp³d.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory; magnetic properties", seconds=75),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Werner also studied platinum(IV) ammine chlorides. Assume that platinum has a coordination number of 6 "
          "in each compound below and that each is treated with an excess of AgNO₃ solution. Match the compound in "
          "List-I with the number of moles of AgCl precipitated per mole of compound in List-II.",
          ["PtCl₄·6NH₃", "PtCl₄·5NH₃", "PtCl₄·4NH₃", "PtCl₄·3NH₃"],
          ["1", "2", "3", "4"],
          "IV III II I", ["I II III IV", "IV III I II", "III IV II I"], "C"),
      "Werner's theory: ionisable chlorides",
      "With six positions to fill, every NH₃ is coordinated and the remaining positions are taken by chloride ions; "
      "only the chlorides outside the coordination sphere are precipitated by Ag⁺.",
      ["PtCl₄·6NH₃ = [Pt(NH₃)₆]Cl₄ → 4 AgCl", "PtCl₄·5NH₃ = [Pt(NH₃)₅Cl]Cl₃ → 3",
       "PtCl₄·4NH₃ = [Pt(NH₃)₄Cl₂]Cl₂ → 2", "PtCl₄·3NH₃ = [Pt(NH₃)₃Cl₃]Cl → 1"],
      shortcut="Ionisable Cl⁻ = 4 − (6 − number of NH₃).",
      why_others_wrong="The reversed code takes the coordinated chlorides as the ionisable ones; the other codes "
                       "pair a compound with a count that leaves the coordination number different from 6.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory of coordination compounds", seconds=60),

    Q(T_CC, "Isomerism", "Intermediate", "statement_pair",
      *sp("[Co(NH₃)₅(NO₂)]Cl₂ is obtained in a yellow form, in which the nitrite ligand is bound through nitrogen, "
          "and in a red form, in which it is bound through oxygen.", True,
          "According to Werner, the ions or groups bound to the metal by secondary linkages have characteristic "
          "spatial arrangements corresponding to different coordination numbers.", True),
      "Linkage isomerism; Werner's postulates",
      "NCERT describes the two linkage isomers of [Co(NH₃)₅(NO₂)]Cl₂: the yellow –NO₂ (nitrito-N) form and the red "
      "–ONO (nitrito-O) form. Werner's postulates include that secondary linkages give characteristic spatial "
      "arrangements, the coordination polyhedra (octahedral, tetrahedral, square planar).",
      ["Statement I: true (linkage isomers, yellow N-bound and red O-bound)", "Statement II: true"],
      ncert=f"{NC12}, 'Coordination Compounds', linkage isomerism; Werner's theory", seconds=40),

    N(T_CC, "Isomerism", "Advanced",
      "CrCl₃·6H₂O (molar mass 266.5 g mol⁻¹) exists as hydrate (solvate) isomers in which chromium has a "
      "coordination number of 6. A solution containing 2.665 g of one isomer gives 2.87 g of AgCl with an excess "
      "of AgNO₃ solution (molar mass of AgCl = 143.5 g mol⁻¹). The isomer is:",
      ["[Cr(H₂O)₆]Cl₃", "[Cr(H₂O)₄Cl₂]Cl·2H₂O", "[Cr(H₂O)₃Cl₃]·3H₂O", v_2384], "D", v_2384,
      "Identifying a hydrate isomer from the ionisable chloride",
      "Only chloride ions outside the coordination sphere are precipitated as AgCl. The mole ratio AgCl : complex "
      "tells how many chlorides are ionisable; the rest are coordinated, and water fills the remaining positions.",
      ["Complex: 2.665 / 266.5 = 0.0100 mol", "AgCl: 2.87 / 143.5 = 0.0200 mol → 2 ionisable Cl⁻",
       "One Cl⁻ coordinated + five H₂O → [Cr(H₂O)₅Cl]Cl₂·H₂O"],
      why_others_wrong="[Cr(H₂O)₆]Cl₃ would give 3 mol AgCl per mole (4.31 g); [Cr(H₂O)₄Cl₂]Cl·2H₂O would give "
                       "1.435 g; the neutral [Cr(H₂O)₃Cl₃]·3H₂O gives no precipitate.",
      ncert=f"{NC12}, 'Coordination Compounds', solvate (hydrate) isomerism", seconds=90),

    N(T_CC, "Crystal field theory", "Advanced",
      "In the compound [Cr(NH₃)₆][Fe(CN)₆], chromium is in the +3 oxidation state, and the cyanido complex of iron "
      "is low spin (atomic numbers: Cr 24, Fe 26). The total number of unpaired electrons in one formula unit is:",
      ["3", v_2385, "5", "8"], "B", v_2385,
      "Charge balance and spin state in a complex salt",
      "The cation is [Cr(NH₃)₆]³⁺, so the anion must be [Fe(CN)₆]³⁻, which contains Fe³⁺ (3d⁵). Cr³⁺ (3d³, t₂g³) "
      "has three unpaired electrons; low-spin Fe³⁺ (t₂g⁵) has one.",
      ["[Cr(NH₃)₆]³⁺ → anion [Fe(CN)₆]³⁻ → Fe³⁺", "Cr³⁺: t₂g³ → 3 unpaired", "Fe³⁺ (low spin): t₂g⁵ → 1 unpaired",
       "Total = 4"],
      why_others_wrong="3 treats the anion as [Fe(CN)₆]⁴⁻ with diamagnetic Fe²⁺ (charge does not balance); 5 counts "
                       "only a high-spin Fe³⁺; 8 adds a high-spin Fe³⁺ (5) to Cr³⁺ (3).",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory; magnetic properties", seconds=75),

    Q(T_CC, "Valence bond theory", "Advanced", "direct",
      "Which pair of complexes has the same number of unpaired electrons AND the same type of hybridisation of the "
      "central atom, according to valence bond theory? ([Fe(H₂O)₆]²⁺ is a high-spin complex; atomic numbers: Cr 24, "
      "Mn 25, Fe 26, Co 27, Ni 28.)",
      ["[Ni(CN)₄]²⁻ and [Ni(CO)₄]", "[Fe(CN)₆]³⁻ and [Mn(CN)₆]³⁻", "[CoF₆]³⁻ and [Fe(H₂O)₆]²⁺",
       "[Cr(NH₃)₆]³⁺ and [Co(NH₃)₆]³⁺"], "C",
      "Comparing hybridisation and magnetic moments",
      "Co³⁺ and Fe²⁺ are both 3d⁶. With the weak field ligands F⁻ and H₂O, both keep four unpaired electrons and "
      "use outer 4d orbitals: sp³d², octahedral, four unpaired electrons each.",
      ["[CoF₆]³⁻: 3d⁶, 4 unpaired, sp³d²", "[Fe(H₂O)₆]²⁺: 3d⁶, 4 unpaired, sp³d²",
       "Other pairs differ in one of the two properties"],
      why_others_wrong="[Ni(CN)₄]²⁻ (dsp²) and [Ni(CO)₄] (sp³) are both diamagnetic but differently hybridised; "
                       "[Fe(CN)₆]³⁻ (1 unpaired) and [Mn(CN)₆]³⁻ (2 unpaired) are both d²sp³; [Cr(NH₃)₆]³⁺ (3) and "
                       "[Co(NH₃)₆]³⁺ (0) are both d²sp³.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=90),

    Q(T_CC, "Valence bond theory", "Advanced", "assertion_reason",
      *ar("[Co(C₂O₄)₃]³⁻ is an outer orbital (sp³d²) complex with four unpaired electrons (Z of Co = 27).", False,
          "In the spectrochemical series, the oxalate ion lies before water, i.e. it is a weaker field ligand than "
          "water.", True),
      "Spin state of cobalt(III) complexes",
      "NCERT reports [Co(C₂O₄)₃]³⁻ as diamagnetic: the six 3d electrons of Co³⁺ are paired, and cobalt uses d²sp³ "
      "hybrid orbitals (inner orbital complex). So A is false. R is true: in the spectrochemical series "
      "C₂O₄²⁻ < H₂O. Even so, Co³⁺ (high charge) gives a splitting large enough for pairing with oxalate.",
      ["A: false; [Co(C₂O₄)₃]³⁻ is diamagnetic, d²sp³", "R: true (… C₂O₄²⁻ < H₂O < NCS⁻ …)"],
      ncert=f"{NC12}, 'Coordination Compounds', magnetic properties; spectrochemical series", seconds=60),

    Q(T_CC, "Crystal field theory", "Advanced", "multi_statement",
      *ms("Ignoring pairing energy, and taking the energy of each t₂g electron as −0.4Δo and of each eg electron as "
          "+0.6Δo in an octahedral field, which of the following statements are correct?",
          [("For high-spin [Fe(H₂O)₆]³⁺ (t₂g³ eg²), the crystal field stabilisation energy (CFSE) is zero.", True),
           ("A d¹⁰ ion such as Zn²⁺ has zero CFSE in an octahedral field.", True),
           ("A high-spin d⁴ octahedral complex has a CFSE of −0.6Δo.", True),
           ("A low-spin d⁵ octahedral complex has a CFSE of −2.4Δo.", False),
           ("For the same Δo, the magnitude of the CFSE of a high-spin d⁵ ion is larger than that of a high-spin d⁴ "
            "ion.", False)],
          [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "c", "d"]], "A"),
      "Calculating CFSE",
      "CFSE = −0.4Δo × (t₂g electrons) + 0.6Δo × (eg electrons).",
      ["(a) t₂g³ eg²: −1.2 + 1.2 = 0 → true", "(b) t₂g⁶ eg⁴: −2.4 + 2.4 = 0 → true",
       "(c) t₂g³ eg¹: −1.2 + 0.6 = −0.6Δo → true", "(d) t₂g⁵: −2.0Δo, not −2.4Δo → false",
       "(e) high-spin d⁵ has 0, high-spin d⁴ has −0.6Δo → false"],
      why_others_wrong="Options containing (d) use the low-spin d⁶ value for d⁵; the option with (e) reverses the "
                       "comparison; (b), (d) and (e) misses two correct statements.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=90),
]
