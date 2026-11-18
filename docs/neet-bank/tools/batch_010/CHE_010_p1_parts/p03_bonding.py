

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"


def formal_charge(valence, lone_electrons, bonds):
    return valence - lone_electrons - bonds


assert formal_charge(3, 0, 4) == -1 and formal_charge(7, 6, 1) == 0
add("Hybridisation and resonance", B, "numerical",
    "In the Lewis structure of the tetrafluoroborate ion, BF₄⁻, the boron atom forms four B–F single bonds and "
    "carries no lone pair. The formal charge on the boron atom is:",
    Opts("D", "−1", ["0", "+3", "−4"]),
    "Formal charge = (valence electrons) − (non-bonding electrons) − ½(bonding electrons)",
    "Boron has 3 valence electrons. In BF₄⁻ it has no non-bonding electrons and shares 8 electrons in four "
    "bonds, so it is assigned 4 electrons — one more than it brings.",
    ["V = 3, L = 0, ½S = ½ × 8 = 4", "Formal charge = 3 − 0 − 4 = −1",
     "Each F: 7 − 6 − 1 = 0, so the ion's −1 charge sits formally on B"],
    why="0 assumes the charge must be on fluorine. +3 counts boron's valence electrons without subtracting the "
        "shared ones. −4 subtracts all eight shared electrons instead of half of them.",
    ncert=f"{REF3}, formal charge", seconds=40, checked=True)

add("VSEPR shapes", B, "direct",
    "According to VSEPR theory, the shape of the sulphur dichloride molecule, SCl₂, is:",
    Opts("C", "Bent (V-shaped)", ["Linear", "T-shaped", "Trigonal planar"]),
    "VSEPR: shape from the numbers of bond pairs and lone pairs",
    "Sulphur has six valence electrons; two form S–Cl bonds and four stay as two lone pairs. Four electron pairs "
    "point to the corners of a tetrahedron, and with two of them lone pairs the molecule is bent, like H₂O.",
    ["S: 6 valence electrons → 2 bond pairs + 2 lone pairs", "Type AB₂E₂ → bent"],
    why="Linear needs no lone pairs (AB₂) or three (AB₂E₃). T-shaped is AB₃E₂. Trigonal planar is AB₃ with no "
        "lone pair.",
    ncert=f"{REF3}, VSEPR theory (shapes of molecules with lone pairs)", seconds=30)

add("Ionic bonding and lattice enthalpy", B, "statement_pair",
    sp("The van der Waals radius of chlorine is half the Cl–Cl bond length in the Cl₂ molecule.",
       "Bond enthalpy is the energy needed to break one mole of bonds of a particular type between two atoms "
       "in the gaseous state."),
    SP_, "Bond parameters: covalent and van der Waals radii; bond enthalpy",
    "Half the distance between two bonded chlorine atoms in Cl₂ is the covalent radius of chlorine. The van der "
    "Waals radius is half the distance between two similar atoms in separate (non-bonded) molecules in the "
    "solid, and is larger. Statement II is NCERT's definition of bond enthalpy.",
    ["I: half the bond length = covalent radius, not van der Waals radius → false",
     "II: definition of bond enthalpy → true"],
    answer="D",
    why="Statement I swaps the two radii; the van der Waals radius is measured between non-bonded atoms.",
    ncert=f"{REF3}, bond parameters (bond length, bond enthalpy)", seconds=35)

add("Molecular orbital theory", B, "assertion_reason",
    ar("The H₂⁺ ion is expected to be stable according to molecular orbital theory.",
       "H₂⁺ has one electron in the bonding σ1s orbital and none in the antibonding σ*1s orbital, so its bond "
       "order is ½."),
    AR_, "Bond order and stability from molecular orbital theory",
    "Bond order = ½(N_b − N_a). A positive bond order means the molecule or ion is more stable than the "
    "separated atoms. For H₂⁺, N_b = 1 and N_a = 0, so bond order = ½ > 0 and the ion is predicted to exist. R "
    "is exactly the reason for A.",
    ["H₂⁺: one electron → σ1s¹", "Bond order = ½(1 − 0) = ½", "Positive bond order → stable → R explains A"],
    answer="A",
    why="R gives the electron count and bond order on which the prediction in A rests; it is the explanation, "
        "not an unrelated fact.",
    ncert=f"{REF3}, molecular orbital theory (bond order and stability)", seconds=35)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (species) with List-II (its shape predicted by VSEPR theory).",
          ["NO₃⁻", "PCl₄⁺", "BrF₄⁻", "ICl₂⁻"],
          ["Linear", "Tetrahedral", "Square planar", "Trigonal planar"]),
    match("B", M("IV II III I"), [M("IV III II I"), M("II IV III I"), M("IV II I III")]),
    "VSEPR shapes of ions",
    "Count the electron pairs on the central atom (including the ion's charge), then decide the shape from the "
    "bond pairs and lone pairs.",
    ["NO₃⁻: three σ-bonded O, no lone pair on N → trigonal planar → IV",
     "PCl₄⁺: P has 5 − 1 = 4 electrons → 4 bond pairs → tetrahedral → II",
     "BrF₄⁻: Br has 7 + 1 = 8 electrons → 4 bond pairs + 2 lone pairs → square planar → III",
     "ICl₂⁻: I has 7 + 1 = 8 electrons → 2 bond pairs + 3 lone pairs → linear → I"],
    why="B-III/C-II treats BrF₄⁻ like a tetrahedral AB₄ and ignores its two lone pairs. A-II/B-IV swaps the "
        "planar and tetrahedral species. C-I/D-III swaps the AB₄E₂ and AB₂E₃ shapes.",
    ncert=f"{REF3}, VSEPR theory", seconds=70)

lp_clf3 = 2 + 3 * 3
assert lp_clf3 == 11
add("VSEPR shapes", I, "numerical",
    "The total number of lone pairs of electrons on ALL the atoms of the ClF₃ molecule (on chlorine and on the "
    "three fluorine atoms together) is:",
    Opts("B", "11", ["2", "9", "13"]),
    "Counting lone pairs in a Lewis structure",
    "Chlorine has 7 valence electrons; 3 are used in the three Cl–F bonds and the other 4 form two lone pairs. "
    "Each fluorine has 7 valence electrons; one is used in its bond and the other 6 form three lone pairs.",
    ["Cl: (7 − 3)/2 = 2 lone pairs", "3 F: 3 × 3 = 9 lone pairs", "Total = 2 + 9 = 11"],
    why="2 counts only the lone pairs on chlorine and 9 only those on fluorine. 13 gives chlorine four lone pairs "
        "(as if it formed no bonds).",
    ncert=f"{REF3}, Lewis structures; VSEPR theory", seconds=40, checked=True)

add("VSEPR shapes", I, "direct",
    "Which of the following is the correct order of the H–N–H bond angle in NH₄⁺, NH₃ and NH₂⁻?",
    Opts("D", "NH₄⁺ > NH₃ > NH₂⁻",
         ["NH₂⁻ > NH₃ > NH₄⁺", "NH₃ > NH₄⁺ > NH₂⁻", "NH₄⁺ = NH₃ = NH₂⁻"]),
    "Effect of lone pairs on bond angles (VSEPR)",
    "In all three species nitrogen has four electron pairs. NH₄⁺ has no lone pair (regular tetrahedron, "
    "109.5°), NH₃ has one lone pair (about 107°) and NH₂⁻ has two lone pairs. Lone pairs repel bond pairs more "
    "strongly than bond pairs do, so each extra lone pair squeezes the H–N–H angle further.",
    ["NH₄⁺: 4 bp, 0 lp → 109.5°", "NH₃: 3 bp, 1 lp → ≈107°", "NH₂⁻: 2 bp, 2 lp → smaller still (bent)"],
    why="The reversed order ignores lone-pair repulsion. NH₃ cannot exceed NH₄⁺ because it has a lone pair. "
        "Equal angles would need equal numbers of lone pairs.",
    ncert=f"{REF3}, VSEPR theory (lone pair–bond pair repulsion)", seconds=40)

add("Hybridisation and resonance", I, "statement_pair",
    sp("To explain the formation of SF₆, sulphur is pictured in an excited state that has four unpaired "
       "electrons.",
       "In SF₆, six sp³d² hybrid orbitals of sulphur overlap with singly occupied 2p orbitals of fluorine "
       "atoms to form six S–F σ bonds."),
    SP_, "sp³d² hybridisation in SF₆",
    "Ground-state S is 3s² 3p⁴. Promoting one 3s and one 3p electron into 3d orbitals gives 3s¹ 3p³ 3d², with "
    "SIX unpaired electrons. These six orbitals mix to give six sp³d² hybrids, each of which overlaps with a "
    "half-filled 2p orbital of an F atom.",
    ["Excited S: 3s¹ 3p³ 3d² → six unpaired electrons → I false",
     "Six sp³d² hybrids + six F 2p orbitals → six σ bonds → II true"],
    answer="D",
    why="Four unpaired electrons is the state used for SF₄-type bonding, not for six bonds in SF₆.",
    ncert=f"{REF3}, hybridisation involving d orbitals (sp³d², SF₆)", seconds=45)

add("Hybridisation and resonance", I, "statement_pair",
    sp("Valence bond theory explains the shapes of polyatomic molecules such as CH₄, NH₃ and H₂O in terms of "
       "the overlap and hybridisation of atomic orbitals.",
       "The four equal H–C–H angles of 109.5° in CH₄ can be explained by overlap of the hydrogen 1s orbitals "
       "with the unhybridised 2s and 2p orbitals of carbon."),
    SP_, "Directional properties of bonds and the need for hybridisation",
    "NCERT points out that simple overlap of the hydrogen 1s orbitals with carbon's 2s and three mutually "
    "perpendicular 2p orbitals would give three bonds at 90° and one different bond, not four identical bonds "
    "at 109.5°. The tetrahedral shape is explained by sp³ hybridisation.",
    ["I: VB theory + hybridisation explain shapes → true",
     "II: pure 2p orbitals are at 90°, so they cannot give 109.5° → false"],
    answer="C",
    why="Statement II describes exactly the simple-overlap picture that NCERT says fails for CH₄.",
    ncert=f"{REF3}, directional properties of bonds; hybridisation", seconds=40)

add("Molecular orbital theory", I, "assertion_reason",
    ar("The peroxide ion, O₂²⁻, is diamagnetic.",
       "The bond order of the O₂²⁻ ion is 2."),
    AR_, "MO configuration of O₂²⁻",
    "O₂²⁻ has 18 electrons: … σ2p_z² (π2p)⁴ (π*2p)⁴. All electrons are paired, so it is diamagnetic (A true). "
    "Bonding electrons in the valence MOs = 8 and antibonding = 6 (counting σ2s, σ*2s), so the bond order is "
    "½(10 − 8) = 1 overall, not 2. R is false.",
    ["O₂²⁻: π*2p fully filled (4 electrons) → no unpaired electron → A true",
     "Bond order = ½(N_b − N_a) = ½(10 − 8) = 1 → R false"],
    answer="C",
    why="A bond order of 2 belongs to O₂, whose two π* electrons are unpaired; adding two electrons fills π* and "
        "lowers the bond order to 1.",
    ncert=f"{REF3}, molecular orbital theory (bonding in O₂ and related species)", seconds=45)

add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (type of hybridisation) with List-II (angle between the hybrid orbitals).",
          ["sp", "sp²", "sp³", "sp³d²"],
          ["90°", "109°28′", "120°", "180°"]),
    match("B", M("IV III II I"), [M("III IV II I"), M("IV II III I"), M("IV III I II")]),
    "Geometry of hybrid orbitals",
    "sp hybrids are linear, sp² trigonal planar, sp³ tetrahedral and sp³d² octahedral.",
    ["sp → linear → 180° → IV", "sp² → trigonal planar → 120° → III", "sp³ → tetrahedral → 109°28′ → II",
     "sp³d² → octahedral → 90° → I"],
    why="A-III/B-IV swaps linear and trigonal planar. B-II/C-III swaps the planar and tetrahedral angles. "
        "C-I/D-II gives the octahedral angle to sp³.",
    ncert=f"{REF3}, hybridisation (types and geometry)", seconds=35)


def bond_order(nb, na):
    return (nb - na) / 2


bo = {"a": bond_order(10, 5), "b": bond_order(9, 4), "c": bond_order(10, 5), "d": bond_order(10, 7),
      "e": bond_order(8, 4)}
assert bo == {"a": 2.5, "b": 2.5, "c": 2.5, "d": 1.5, "e": 2.0}
truth_bo = {k: v == 2.5 for k, v in bo.items()}
add("Molecular orbital theory", I, "multi_statement",
    ms("According to molecular orbital theory, which of the following species have a bond order of 2.5?",
       ["O₂⁺", "N₂⁺", "N₂⁻", "O₂⁻", "C₂"]),
    multi("B", truth_bo, ["(a) and (d) only", "(a), (b), (c) and (e) only", "(b) and (c) only"]),
    "Bond order = ½(N_b − N_a)",
    "Count bonding and antibonding electrons (all electrons, including 1s) in each species using the "
    "appropriate MO energy order.",
    ["O₂⁺ (15 e⁻): N_b = 10, N_a = 5 → 2.5 ✓", "N₂⁺ (13 e⁻): N_b = 9, N_a = 4 → 2.5 ✓",
     "N₂⁻ (15 e⁻): N_b = 10, N_a = 5 → 2.5 ✓", "O₂⁻ (17 e⁻): N_b = 10, N_a = 7 → 1.5 ✗",
     "C₂ (12 e⁻): N_b = 8, N_a = 4 → 2 ✗"],
    why="O₂⁻ (superoxide) has bond order 1.5 and C₂ has bond order 2, so options containing (d) or (e) are "
        "wrong; '(b) and (c) only' misses O₂⁺.",
    ncert=f"{REF3}, molecular orbital theory (bond order)", seconds=80, checked=True)

truth_sp3 = {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Hybridisation and resonance", A, "multi_statement",
    ms("In which of the following species is the central atom sp³ hybridised?",
       ["BF₄⁻", "H₃O⁺", "SO₃", "I₃⁻", "SiCl₄"]),
    multi("D", truth_sp3, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (e) only"]),
    "Hybridisation from the number of electron pairs (σ bond pairs + lone pairs) on the central atom",
    "Four electron pairs → sp³; three → sp²; five → sp³d. Count σ bonds and lone pairs on each central atom.",
    ["(a) BF₄⁻: 4 bond pairs, 0 lone pairs → sp³ ✓", "(b) H₃O⁺: 3 bond pairs + 1 lone pair → sp³ ✓",
     "(c) SO₃: 3 σ bonds, no lone pair → sp² ✗", "(d) I₃⁻: 2 bond pairs + 3 lone pairs = 5 → sp³d ✗",
     "(e) SiCl₄: 4 bond pairs → sp³ ✓"],
    why="SO₃ is trigonal planar (sp²) and I₃⁻ has five electron pairs (sp³d), so any option with (c) or (d) is "
        "wrong; '(a) and (e) only' misses H₃O⁺, whose lone pair counts as an electron pair.",
    ncert=f"{REF3}, hybridisation; VSEPR theory", seconds=75)

add("VSEPR shapes", A, "assertion_reason",
    ar("The H–O–H bond angle in water (104.5°) is smaller than the H–N–H bond angle in ammonia (107°).",
       "Lone pair–lone pair repulsion is greater than lone pair–bond pair repulsion, which in turn is greater "
       "than bond pair–bond pair repulsion."),
    AR_, "Order of electron-pair repulsions in VSEPR theory",
    "Both molecules have four electron pairs (tetrahedral arrangement). NH₃ has one lone pair; H₂O has two, so "
    "in water there is also a lone pair–lone pair repulsion, the strongest of all, which pushes the two O–H "
    "bond pairs closer together than the N–H bond pairs in NH₃. R gives the cause of A.",
    ["NH₃: 3 bp + 1 lp; H₂O: 2 bp + 2 lp", "lp–lp > lp–bp > bp–bp", "Extra lp–lp repulsion in H₂O → smaller angle"],
    answer="A",
    why="R is the repulsion order that VSEPR uses to explain exactly this difference in bond angles.",
    ncert=f"{REF3}, VSEPR theory", seconds=45)

add("Hybridisation and resonance", A, "statement_pair",
    sp("In the nitrite ion, NO₂⁻, the two nitrogen–oxygen bonds have different lengths, one being a double "
       "bond and the other a single bond.",
       "The average bond order of a nitrogen–oxygen bond in the nitrite ion is 1.5."),
    SP_, "Resonance and average bond order",
    "NO₂⁻ is a resonance hybrid of two equivalent structures, O=N–O⁻ and ⁻O–N=O. Neither structure is real; in "
    "the hybrid both N–O bonds are identical, with a length between those of N–O and N=O. Bond order = "
    "(1 + 2)/2 = 1.5.",
    ["Two equivalent canonical structures → both bonds identical → I false",
     "Average bond order = 3 bonds shared over 2 positions = 1.5 → II true"],
    answer="D",
    why="Statement I describes one canonical structure as if it were the real ion; resonance makes the bonds "
        "equal.",
    ncert=f"{REF3}, resonance structures", seconds=45)

add("VSEPR shapes", A, "match_list",
    lists("Match List-I (molecule) with List-II (geometry of ALL the electron pairs — bond pairs and lone pairs "
          "— around the central atom, which may differ from the shape of the molecule).",
          ["H₂O", "SF₄", "XeF₄", "SO₂"],
          ["Trigonal planar", "Octahedral", "Trigonal bipyramidal", "Tetrahedral"]),
    match("C", M("IV III II I"), [M("I III II IV"), M("IV II III I"), M("IV I II III")]),
    "Electron-pair geometry versus molecular shape (VSEPR)",
    "Count σ bond pairs plus lone pairs on the central atom (a multiple bond counts as one 'super pair'). The "
    "electron pairs take up the geometry for that number; the shape then describes only the atoms.",
    ["H₂O: 2 bp + 2 lp = 4 → tetrahedral (shape bent) → IV",
     "SF₄: 4 bp + 1 lp = 5 → trigonal bipyramidal (shape see-saw) → III",
     "XeF₄: 4 bp + 2 lp = 6 → octahedral (shape square planar) → II",
     "SO₂: 2 double-bond 'pairs' + 1 lp = 3 → trigonal planar (shape bent) → I"],
    why="A-I/D-IV swaps H₂O and SO₂, judging by the bent shape that both share. B-II/C-III swaps the five- and "
        "six-pair geometries. B-I/D-III gives SF₄ three pairs and SO₂ five.",
    ncert=f"{REF3}, VSEPR theory (geometry with lone pairs)", seconds=90)

add("Hybridisation and resonance", A, "direct",
    "In which of the following pairs do the two molecules have the SAME shape although their central atoms are "
    "DIFFERENTLY hybridised?",
    Opts("B", "CO₂ and XeF₂", ["NH₃ and PCl₃", "BF₃ and NO₃⁻", "SF₆ and XeF₄"]),
    "Shape depends on the bond pairs; hybridisation depends on all electron pairs",
    "CO₂: carbon is sp hybridised and the molecule is linear. XeF₂: xenon has 2 bond pairs and 3 lone pairs "
    "(sp³d), and with the lone pairs equatorial the molecule is also linear.",
    ["CO₂: sp, linear", "XeF₂: sp³d, linear → same shape, different hybridisation ✓",
     "NH₃/PCl₃: both sp³, both pyramidal", "BF₃/NO₃⁻: both sp², both trigonal planar",
     "SF₆/XeF₄: both sp³d², octahedral vs square planar (different shape)"],
    why="NH₃/PCl₃ and BF₃/NO₃⁻ share both shape and hybridisation. SF₆/XeF₄ is the reverse case: same "
        "hybridisation, different shapes.",
    ncert=f"{REF3}, hybridisation; VSEPR theory", seconds=60)
