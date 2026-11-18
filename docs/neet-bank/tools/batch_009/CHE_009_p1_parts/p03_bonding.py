

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

add("Hybridisation and resonance", B, "statement_pair",
    sp("When two hydrogen atoms approach each other, the potential energy of the system falls to a minimum at an "
       "internuclear distance of 74 pm, which is the bond length of H₂.",
       "435.8 kJ of energy is absorbed when one mole of H₂ molecules is formed from hydrogen atoms."),
    SP_, "Valence bond picture of the formation of H₂",
    "As the atoms approach, the attraction between each nucleus and the other atom's electron outweighs the "
    "repulsions, and the energy falls to a minimum at 74 pm: Statement I is true. Because the energy falls, "
    "bond formation RELEASES energy: 435.8 kJ mol⁻¹ is given out when H₂ forms (and must be supplied to break "
    "it). Statement II is false.",
    ["I: energy minimum at 74 pm = bond length → true", "II: bond formation is exothermic (energy released) → false"],
    answer="C",
    why="Statement II reverses the sign: 435.8 kJ mol⁻¹ is the bond dissociation enthalpy, absorbed on breaking "
        "the bond, not on forming it.",
    ncert=f"{REF3}, valence bond theory: formation of the hydrogen molecule", seconds=35)

add("Fajans' rule and dipole moment", B, "direct",
    "Which of the following hydrogen halides has the LARGEST dipole moment?",
    Opts("C", "HF", ["HCl", "HBr", "HI"]),
    "Bond polarity and the electronegativity difference",
    "In a heteronuclear diatomic molecule the shared pair is displaced towards the more electronegative atom. "
    "Fluorine is the most electronegative halogen, so the H–F bond is the most polar and HF has the largest "
    "dipole moment.",
    ["Electronegativity: F > Cl > Br > I", "Largest difference from H → H–F → largest dipole moment"],
    why="HCl, HBr and HI have smaller electronegativity differences between H and the halogen, so their bonds are "
        "less polar.",
    ncert=f"{REF3}, polarity of bonds; dipole moment", seconds=25)

add("Molecular orbital theory", B, "direct",
    "Which of the following species has the same bond order as the N₂ molecule?",
    Opts("B", "NO⁺", ["O₂⁺", "N₂⁺", "O₂"]),
    "Isoelectronic species have the same bond order",
    "NO⁺ has 7 + 8 − 1 = 14 electrons, the same as N₂, and NCERT notes that isoelectronic species such as N₂, CO "
    "and NO⁺ have the same bond order, 3.",
    ["N₂: 14 electrons, bond order 3", "NO⁺: 14 electrons → bond order 3",
     "O₂⁺ 2.5; N₂⁺ 2.5; O₂ 2"],
    why="O₂⁺ and N₂⁺ both have bond order 2.5 and O₂ has bond order 2.",
    ncert=f"{REF3}, bond parameters (bond order); molecular orbital theory", seconds=30)

add("Molecular orbital theory", B, "statement_pair",
    sp("A molecular orbital can hold a maximum of four electrons.",
       "Electrons are filled into molecular orbitals in order of increasing energy, following the Pauli exclusion "
       "principle and Hund's rule, just as in atomic orbitals."),
    SP_, "Filling of molecular orbitals",
    "Like an atomic orbital, a molecular orbital holds at most two electrons of opposite spin, so Statement I is "
    "false. Molecular orbitals are filled according to the Aufbau principle, the Pauli exclusion principle and "
    "Hund's rule: Statement II is true.",
    ["I: max 2 electrons per molecular orbital → false", "II: Aufbau, Pauli and Hund apply → true"],
    answer="D",
    why="Four electrons fit into a PAIR of degenerate molecular orbitals (such as π2pₓ and π2p_y), not into one.",
    ncert=f"{REF3}, molecular orbital theory: electronic configuration of molecules", seconds=30)

add("Ionic bonding and lattice enthalpy", B, "direct",
    "In which of the following pairs do BOTH ions have the electronic configuration of argon? "
    "(Z: F = 9, Na = 11, Mg = 12, S = 16, Cl = 17, K = 19, Ca = 20)",
    Opts("B", "Ca²⁺ and S²⁻", ["Na⁺ and Cl⁻", "Mg²⁺ and Cl⁻", "K⁺ and F⁻"]),
    "Ions formed by electron transfer attain noble-gas configurations",
    "Argon has 18 electrons. Ca²⁺ has 20 − 2 = 18 and S²⁻ has 16 + 2 = 18 electrons, so both have the argon "
    "configuration.",
    ["Ca²⁺: 18 e⁻ (Ar); S²⁻: 18 e⁻ (Ar) ✓", "Na⁺ 10 (Ne), Cl⁻ 18 (Ar)", "Mg²⁺ 10 (Ne), Cl⁻ 18 (Ar)",
     "K⁺ 18 (Ar), F⁻ 10 (Ne)"],
    why="In each other pair one ion (Na⁺, Mg²⁺ or F⁻) has only 10 electrons, the configuration of neon.",
    ncert=f"{REF3}, Kössel–Lewis approach: ionic or electrovalent bond", seconds=35)

add("Hydrogen and metallic bonding", B, "assertion_reason",
    ar("The water molecule has a bent shape.",
       "In liquid water, the molecules are associated with one another through intermolecular hydrogen bonds."),
    AR_, "Shape of a molecule versus intermolecular forces",
    "The bent shape of H₂O comes from the four electron pairs on oxygen (two bond pairs and two lone pairs) "
    "arranged tetrahedrally, with the lone pairs pushing the O–H bonds closer (104.5°). Intermolecular hydrogen "
    "bonding is a different property: it acts BETWEEN molecules and does not decide the shape of a single "
    "molecule. Both statements are true, but R does not explain A.",
    ["A: 2 bond pairs + 2 lone pairs on O → bent → true", "R: O–H···O hydrogen bonds between molecules → true",
     "Shape is fixed by electron pairs on O, not by hydrogen bonding → option B"],
    answer="B",
    why="R is true but describes how molecules attract one another; an isolated water molecule in the vapour is "
        "bent too.",
    ncert=f"{REF3}, VSEPR theory; hydrogen bonding", seconds=40)

truth3 = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Hybridisation and resonance", I, "multi_statement",
    ms("Which of the following statements about the ethyne molecule, HC≡CH, are correct?",
       ["Each carbon atom is sp hybridised.",
        "The C–C σ bond is formed by the overlap of an sp hybrid orbital of each carbon atom.",
        "The two π bonds lie in mutually perpendicular planes.",
        "The H–C–C bond angle is 120°.",
        "Each carbon atom has one unhybridised 2p orbital."]),
    multi("C", truth3, ["(a), (b) and (d) only", "(a), (c) and (e) only", "(b), (c), (d) and (e) only"]),
    "sp hybridisation and the triple bond in ethyne",
    "Each carbon mixes its 2s and one 2p orbital into two sp hybrids at 180°: one overlaps the other carbon's sp "
    "orbital (C–C σ) and one overlaps the 1s orbital of H (C–H σ). The two remaining 2p orbitals of each carbon "
    "(2pₓ and 2p_y) overlap sideways to give two π bonds in perpendicular planes. The molecule is linear.",
    ["(a) ✓", "(b) ✓ sp–sp overlap", "(c) ✓", "(d) ✗ the angle is 180° (linear)",
     "(e) ✗ each carbon keeps TWO unhybridised p orbitals"],
    why="(d) is the angle for sp² carbon and (e) would allow only one π bond; any option with (d) or (e) is wrong.",
    ncert=f"{REF3}, hybridisation: formation of C₂H₂", seconds=60)

add("Molecular orbital theory", I, "direct",
    "Using the molecular orbital energy order that applies to molecules up to N₂, the electronic configuration of "
    "the valence electrons of the N₂ molecule is:",
    Opts("D", "σ2s² σ*2s² (π2pₓ² = π2p_y²) σ2p_z²",
         ["σ2s² σ*2s² σ2p_z² (π2pₓ² = π2p_y²)", "σ2s² σ*2s² (π2pₓ² = π2p_y²) (π*2pₓ¹ = π*2p_y¹)",
          "σ2s² σ2p_z² (π2pₓ² = π2p_y²) σ*2s²"]),
    "Molecular orbital configuration of N₂",
    "N₂ has 10 valence electrons. For B₂, C₂ and N₂ the π2p orbitals lie below σ2p_z, so after σ2s and σ*2s the "
    "four π electrons are placed before the last pair goes into σ2p_z.",
    ["10 valence electrons", "σ2s² σ*2s² (4) → π2pₓ² π2p_y² (8) → σ2p_z² (10)", "Bond order = (8 − 2)/2 = 3"],
    why="Placing σ2p_z below π2p is the order for O₂ and F₂. Putting electrons in π* while σ2p_z is empty breaks "
        "the Aufbau principle and would make N₂ paramagnetic. σ*2s cannot be filled after the higher-energy "
        "orbitals.",
    ncert=f"{REF3}, energy level diagram for molecular orbitals; electronic configuration of molecules",
    seconds=45)

bonds = {"C₂H₄": (5, 1), "C₂H₂": (3, 2), "HCN": (2, 2), "N₂": (1, 2)}
assert len(set(bonds.values())) == 4
add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (molecule) with List-II (numbers of σ and π bonds in one molecule).",
          ["Ethene, H₂C=CH₂", "Ethyne, HC≡CH", "Hydrogen cyanide, H–C≡N", "Nitrogen, N≡N"],
          ["1 σ and 2 π", "2 σ and 2 π", "3 σ and 2 π", "5 σ and 1 π"]),
    match("B", M("IV III II I"), [M("IV II III I"), M("III IV II I"), M("IV III I II")]),
    "Counting σ and π bonds: every single bond is σ; a double bond is 1σ + 1π; a triple bond is 1σ + 2π",
    "Count each bond once, then split multiple bonds into one σ and the rest π.",
    ["C₂H₄: 4 C–H + 1 C=C → 5 σ, 1 π → IV", "C₂H₂: 2 C–H + 1 C≡C → 3 σ, 2 π → III",
     "HCN: 1 C–H + 1 C≡N → 2 σ, 2 π → II", "N₂: N≡N → 1 σ, 2 π → I"],
    why="The other codes swap ethyne with HCN, or ethene with ethyne, or HCN with N₂, each of which miscounts "
        "the C–H σ bonds.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds (σ and π bonds)", seconds=50)

add("Hybridisation and resonance", I, "direct",
    "In which of the following pairs are the central atoms hybridised DIFFERENTLY?",
    Opts("C", "PCl₅ and SF₆", ["CH₄ and NH₄⁺", "BF₃ and NO₃⁻", "BeCl₂ and CO₂"]),
    "Hybridisation from the number of electron pairs (σ bonds + lone pairs) around the central atom",
    "Count the σ bond pairs and lone pairs on the central atom: 2 → sp, 3 → sp², 4 → sp³, 5 → sp³d, 6 → sp³d².",
    ["CH₄, NH₄⁺: 4 pairs → sp³, sp³", "BF₃, NO₃⁻: 3 σ pairs, no lone pair → sp², sp²",
     "BeCl₂, CO₂: 2 σ pairs → sp, sp", "PCl₅: 5 pairs → sp³d; SF₆: 6 pairs → sp³d² → different"],
    why="Each of the other pairs has the same number of σ pairs plus lone pairs on the central atom, and so the "
        "same hybridisation.",
    ncert=f"{REF3}, hybridisation (including s, p and d orbitals)", seconds=45)

add("Hybridisation and resonance", I, "assertion_reason",
    ar("The CO₂ molecule is linear.",
       "The carbon atom in CO₂ is sp² hybridised."),
    AR_, "Hybridisation of carbon in CO₂",
    "Carbon in CO₂ forms two σ bonds (one to each O) and has no lone pair, so it is sp hybridised and the "
    "molecule is linear (O=C=O, 180°). A is true. R is false: an sp² carbon would give a 120° arrangement.",
    ["A: O=C=O, 180° → true", "R: 2 σ pairs, no lone pair → sp, not sp² → false"],
    answer="C",
    why="R is false, so options A and B are out; A is true, so option D is out.",
    ncert=f"{REF3}, hybridisation; VSEPR shapes", seconds=35)

add("VSEPR shapes", I, "statement_pair",
    sp("Like CO₂, the SO₂ molecule is linear.",
       "The BrF₃ molecule is T-shaped."),
    SP_, "Shapes predicted by VSEPR theory",
    "In SO₂ the sulphur atom has two bonding domains and one lone pair; the lone pair bends the molecule (it is "
    "polar), so Statement I is false. In BrF₃, bromine (7 valence electrons) forms three bonds and keeps two lone "
    "pairs; the five pairs are arranged trigonal bipyramidally with both lone pairs equatorial, giving a "
    "T-shaped molecule: Statement II is true.",
    ["I: SO₂ is AB₂E → bent → false", "II: BrF₃ is AB₃E₂ → T-shaped → true"],
    answer="D",
    why="Statement I ignores the lone pair on sulphur, which CO₂'s carbon does not have.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules with lone pairs", seconds=40)

add("Ionic bonding and lattice enthalpy", I, "statement_pair",
    sp("In Kössel's approach, an electron is transferred from one atom to another to form positive and negative "
       "ions, and the bond formed by the electrostatic attraction between these ions is called an electrovalent "
       "bond.",
       "Lewis pictured an atom as a positively charged 'kernel' (the nucleus together with the inner electrons) "
       "surrounded by the outer shell, which can hold up to eight electrons."),
    SP_, "The Kössel–Lewis approach to chemical bonding",
    "Both statements are as given in NCERT. Kössel described ionic (electrovalent) bonding by electron transfer "
    "and electrostatic attraction. Lewis described the atom as a kernel plus an outer shell of at most eight "
    "electrons, and represented the valence electrons by dots in Lewis symbols.",
    ["I: Kössel → electron transfer → electrovalent bond → true", "II: Lewis → kernel + outer shell (octet) → true"],
    answer="A",
    why="Neither statement is false; they describe the two halves of the Kössel–Lewis approach.",
    ncert=f"{REF3}, Kössel–Lewis approach to chemical bonding", seconds=35)

add("VSEPR shapes", I, "direct",
    "Which of the following species has the same shape as the NH₃ molecule?",
    Opts("B", "SO₃²⁻", ["SO₃", "NO₃⁻", "BF₃"]),
    "VSEPR: three bond pairs and one lone pair give a trigonal pyramid",
    "NH₃ is AB₃E (trigonal pyramidal). In SO₃²⁻, sulphur has 6 + 2 = 8 electrons to place; three go into bonds "
    "with the three O atoms (counted as three bonding domains, any multiple bond counting as one) and one pair "
    "remains, so SO₃²⁻ is also AB₃E, trigonal pyramidal.",
    ["NH₃: 3 bp + 1 lp → trigonal pyramidal", "SO₃²⁻: 3 bonding domains + 1 lp → trigonal pyramidal",
     "SO₃, NO₃⁻, BF₃: 3 bonding domains, no lone pair → trigonal planar"],
    why="SO₃, NO₃⁻ and BF₃ have no lone pair on the central atom and are trigonal planar.",
    ncert=f"{REF3}, VSEPR theory", seconds=50)

truth3a = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("VSEPR shapes", A, "multi_statement",
    ms("In which of the following molecules is at least one bond angle around the central atom exactly 90°?",
       ["SF₆", "XeF₄", "PCl₅", "XeF₂", "BF₃"]),
    multi("B", truth3a, ["(a), (b), (c) and (d) only", "(a) and (b) only", "(b), (c) and (e) only"]),
    "Bond angles in octahedral, square planar, trigonal bipyramidal and linear molecules",
    "SF₆ (octahedral) has 90° angles between adjacent bonds. XeF₄ (square planar) has 90° between adjacent "
    "Xe–F bonds. PCl₅ (trigonal bipyramidal) has 90° between each axial and each equatorial bond. XeF₂ is "
    "linear: its only F–Xe–F angle is 180° (the 90° angles involve lone pairs, not bonds). BF₃ has only 120°.",
    ["(a) SF₆: 90°, 180° ✓", "(b) XeF₄: 90°, 180° ✓", "(c) PCl₅: 90°, 120°, 180° ✓",
     "(d) XeF₂: 180° only ✗", "(e) BF₃: 120° only ✗"],
    why="The trap is XeF₂: its electron-pair geometry is trigonal bipyramidal, but with only two bonds, both "
        "axial, the bond angle is 180°. '(a) and (b) only' misses the axial–equatorial 90° angles of PCl₅.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules", seconds=70)

add("Molecular orbital theory", A, "assertion_reason",
    ar("The Li₂ molecule has a bond order of one.",
       "In Li₂, the four 1s electrons fill σ1s and σ*1s, whose effects cancel, and the two 2s electrons occupy the "
       "bonding σ2s orbital."),
    AR_, "Bond order from the molecular orbital configuration",
    "Li₂ has 6 electrons: σ1s² σ*1s² σ2s². Bonding electrons Nb = 4, antibonding Na = 2, so bond order = "
    "(4 − 2)/2 = 1. The configuration in R is exactly what gives this bond order.",
    ["Configuration: σ1s² σ*1s² σ2s²", "Bond order = (4 − 2)/2 = 1 → A true",
     "R states this configuration → true and explains A"],
    answer="A",
    why="Both are true, and the bond order is calculated directly from the configuration stated in R.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=50)

anti = {"N₂": 2 + 2, "O₂": 2 + 2 + 2, "F₂": 2 + 2 + 4, "Ne₂": 2 + 2 + 4 + 2}
assert anti == {"N₂": 4, "O₂": 6, "F₂": 8, "Ne₂": 10}
add("Molecular orbital theory", A, "match_list",
    lists("Match List-I (species) with List-II (total number of electrons, including the 1s electrons, in "
          "antibonding molecular orbitals).",
          ["N₂", "O₂", "F₂", "Ne₂"], ["8", "10", "4", "6"]),
    match("C", M("III IV I II"), [M("III IV II I"), M("IV III I II"), M("I IV III II")]),
    "Counting antibonding electrons in homonuclear diatomic molecules",
    "Write each configuration including σ1s and σ*1s. Antibonding orbitals: σ*1s, σ*2s, π*2p and σ*2p.",
    ["N₂ (14 e): σ*1s² σ*2s² → 4 → III", "O₂ (16 e): σ*1s² σ*2s² π*2p² → 6 → IV",
     "F₂ (18 e): σ*1s² σ*2s² π*2p⁴ → 8 → I", "Ne₂ (20 e): σ*1s² σ*2s² π*2p⁴ σ*2p² → 10 → II"],
    why="The wrong codes swap neighbouring species; each of these molecules has 10 bonding electrons, so the "
        "antibonding count rises by 2 from N₂ to O₂ to F₂ to Ne₂ (bond orders 3, 2, 1, 0).",
    ncert=f"{REF3}, molecular orbital theory: bond order", seconds=70, checked=True)

add("Hybridisation and resonance", A, "statement_pair",
    sp("In the nitrate ion, NO₃⁻, all three N–O bonds are of equal length.",
       "Each N–O bond in the nitrate ion has a bond order of 1.5."),
    SP_, "Resonance in the nitrate ion",
    "NO₃⁻ is a resonance hybrid of three equivalent structures, each with one N=O and two N–O bonds, so the "
    "three bonds are identical: Statement I is true. The four bonds (one double + two single) are shared over "
    "three positions, so each has bond order 4/3 ≈ 1.33, not 1.5: Statement II is false.",
    ["I: three equivalent canonical structures → equal bonds → true",
     "II: bond order = (2 + 1 + 1)/3 = 1.33, not 1.5 → false"],
    answer="C",
    why="1.5 is the bond order for a hybrid of TWO equivalent structures (as in O₃), not three.",
    ncert=f"{REF3}, resonance structures", seconds=50)

add("Hybridisation and resonance", A, "assertion_reason",
    ar("The sulphur atom in SF₄ is sp³ hybridised.",
       "The sulphur atom in SF₄ has four bond pairs and one lone pair of electrons."),
    AR_, "Hybridisation from the number of electron pairs",
    "Five electron pairs (four bond pairs + one lone pair) around sulphur need five hybrid orbitals: S is sp³d "
    "hybridised, giving a trigonal bipyramidal arrangement and a see-saw molecule. A is false; R is true.",
    ["R: S (6 valence e⁻) uses 4 in bonds, keeps 1 lone pair → true",
     "5 pairs → sp³d, not sp³ → A false"],
    answer="D",
    why="sp³ hybridisation would accommodate only four electron pairs, so A cannot be true while R is.",
    ncert=f"{REF3}, hybridisation of elements involving d orbitals", seconds=40)

truth3b = {"a": True, "b": False, "c": True, "d": False, "e": True}
add("Fajans' rule and dipole moment", A, "multi_statement",
    ms("Which of the following molecules have a NON-ZERO dipole moment?",
       ["CHCl₃", "BCl₃", "SO₂", "XeF₂", "BrF₃"]),
    multi("D", truth3b, ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a) and (c) only"]),
    "Dipole moment from molecular shape",
    "A molecule is non-polar only when its bond dipoles (and lone-pair effects) cancel by symmetry.",
    ["(a) CHCl₃: tetrahedral but with unlike substituents → bond dipoles do not cancel ✓",
     "(b) BCl₃: trigonal planar, three identical bonds → 0 ✗", "(c) SO₂: bent → polar ✓",
     "(d) XeF₂: linear, two opposite Xe–F dipoles cancel → 0 ✗", "(e) BrF₃: T-shaped → polar ✓"],
    why="BCl₃ and XeF₂ are symmetric and have zero dipole moment even though their bonds are polar; "
        "'(a) and (c) only' misses BrF₃.",
    ncert=f"{REF3}, polarity of bonds; dipole moment", seconds=60)
