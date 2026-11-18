

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10 = f"{C12}, 'The p-Block Elements'"
REF10A = f"{C11}, 'The p-Block Elements'"

add("Group 17 and 18 trends", B, "direct",
    "Which of the following INCREASES on going down group 17 from fluorine to iodine?",
    Opts("A", "Atomic radius", ["Electronegativity", "First ionisation enthalpy", "Oxidising power of the element"]),
    "Trends down group 17",
    "Down the group a new shell is added at each step, so the atomic radius increases. The outer electrons are "
    "farther from the nucleus and better shielded, so ionisation enthalpy, electronegativity and oxidising "
    "power all decrease.",
    ["Radius: F < Cl < Br < I (increases)", "Electronegativity, ionisation enthalpy, oxidising power: decrease"],
    why="Electronegativity, ionisation enthalpy and oxidising power all fall from fluorine to iodine.",
    ncert=f"{REF10}, group 17 elements: atomic and physical properties", seconds=25)

add("Group 15 and 16 trends", B, "direct",
    "Tellurium is the group 16 element of the fifth period. Its valence-shell electronic configuration in the "
    "ground state is:",
    Opts("C", "5s² 5p⁴", ["4d¹⁰ 5s² 5p²", "5s² 5p⁶", "6s² 6p⁴"]),
    "General valence-shell configuration of group 16: ns² np⁴",
    "Group 16 elements have six valence electrons, ns² np⁴. For period 5, n = 5, so tellurium (Z = 52, "
    "[Kr] 4d¹⁰ 5s² 5p⁴) has the valence shell 5s² 5p⁴.",
    ["Group 16 → ns² np⁴", "Period 5 → n = 5 → 5s² 5p⁴"],
    why="4d¹⁰ 5s² 5p² belongs to tin (group 14). 5s² 5p⁶ is xenon (group 18). 6s² 6p⁴ is the group 16 element "
        "of period 6, polonium.",
    ncert=f"{REF10}, group 16 elements: electronic configuration", seconds=25)

add("Group 15 and 16 trends", B, "match_list",
    lists("Match List-I (group 15 element) with List-II (its nature).",
          ["Bismuth", "Arsenic", "Nitrogen", "Phosphorus"],
          ["Metalloid", "Non-metal; a gas at room temperature", "Metal",
           "Non-metal; a solid at room temperature"]),
    match("D", M("III I II IV"), [M("I III II IV"), M("III I IV II"), M("III II I IV")]),
    "Increase of metallic character down group 15",
    "Down group 15, metallic character increases: nitrogen and phosphorus are non-metals, arsenic and antimony "
    "are metalloids, and bismuth is a typical metal. Of the non-metals, only nitrogen is a gas (N₂).",
    ["A: Bi → metal → III", "B: As → metalloid → I", "C: N → non-metal, gas → II", "D: P → non-metal, solid → IV"],
    why="A-I/B-III swaps bismuth and arsenic. C-IV/D-II swaps nitrogen and phosphorus. B-II/C-I calls arsenic a "
        "gas and nitrogen a metalloid.",
    ncert=f"{REF10}, group 15 elements: physical properties", seconds=40)

add("Anomalous first element", I, "match_list",
    lists("Match List-I (first element of a p-block group) with List-II (a way in which it differs from the "
          "other members of its group).",
          ["Boron", "Nitrogen", "Oxygen", "Fluorine"],
          ["Shows only the −1 oxidation state in its compounds",
           "It is a non-metal, whereas all the other members of its group are metals",
           "Exists as a diatomic molecule held by a triple bond, whereas the next member exists as tetra-atomic "
           "molecules with single bonds",
           "Its hydride is a liquid because of extensive hydrogen bonding, whereas the hydrides of the heavier "
           "members are gases"]),
    match("B", M("II III IV I"), [M("III II IV I"), M("II III I IV"), M("II IV III I")]),
    "Anomalous behaviour of the first member of each p-block group",
    "The first members are small, highly electronegative and have no d orbitals in the valence shell. Boron is "
    "the only non-metal of group 13; small size lets nitrogen form pπ–pπ multiple bonds (N≡N), makes oxygen's "
    "hydride hydrogen-bonded, and keeps fluorine at −1.",
    ["A: boron, the only non-metal of group 13 → II", "B: nitrogen, N≡N vs P₄ → III",
     "C: oxygen, H₂O liquid (hydrogen bonding) vs H₂S gas → IV", "D: fluorine, only −1 → I"],
    why="A-III/B-II swaps boron and nitrogen. C-I/D-IV swaps oxygen and fluorine. B-IV/C-III swaps nitrogen "
        "and oxygen.",
    ncert=f"{REF10}, anomalous behaviour of nitrogen, oxygen and fluorine; {REF10A}, anomalous properties of boron",
    seconds=60)

truth_18 = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Group 17 and 18 trends", I, "multi_statement",
    ms("Which of the following statements about the group 18 elements (noble gases) are correct?",
       ["Their first ionisation enthalpy decreases down the group.",
        "Their atomic radius increases down the group.",
        "Their boiling points increase from helium to radon.",
        "They have large negative electron gain enthalpies.",
        "All of them have the valence-shell configuration ns² np⁶."]),
    multi("A", truth_18, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Trends in group 18",
    "Down the group the atoms become larger, so ionisation enthalpy falls and the dispersion forces between "
    "atoms grow (boiling points rise). With completely filled valence shells, the noble gases have large "
    "POSITIVE electron gain enthalpies. Helium is 1s², not ns² np⁶.",
    ["(a) ✓", "(b) ✓", "(c) larger atoms → stronger dispersion forces ✓", "(d) ✗: large positive",
     "(e) ✗: helium is 1s²"],
    why="(d) gives the wrong sign for the electron gain enthalpy and (e) forgets helium; any option with either "
        "is wrong.",
    ncert=f"{REF10}, group 18 elements: electronic configuration, atomic and physical properties", seconds=50)

add("Group 17 and 18 trends", I, "statement_pair",
    sp("On going down group 17 from fluorine to iodine, the first ionisation enthalpy decreases.",
       "On going down group 17 from fluorine to iodine, the oxidising power of the halogens increases."),
    SP_, "Trends in ionisation enthalpy and oxidising power in group 17",
    "Down the group the atomic size increases, so the outer electrons are held less firmly and the ionisation "
    "enthalpy falls. The tendency to gain an electron also falls, and fluorine is the strongest oxidising "
    "agent; oxidising power DECREASES from F₂ to I₂.",
    ["I: larger atoms → lower ionisation enthalpy → true", "II: oxidising power F₂ > Cl₂ > Br₂ > I₂ → false"],
    answer="C",
    why="Statement II reverses the trend: oxidising power decreases down group 17.",
    ncert=f"{REF10}, group 17 elements", seconds=30)

truth_15 = {"a": True, "b": False, "c": True, "d": True, "e": False}
add("Group 15 and 16 trends", I, "multi_statement",
    ms("Which of the following trends on going down group 15 from nitrogen to bismuth are correct?",
       ["The covalent radius increases.",
        "The first ionisation enthalpy increases.",
        "The metallic character increases.",
        "The tendency to show the −3 oxidation state decreases.",
        "The electronegativity increases."]),
    multi("B", truth_15, ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Periodic trends down group 15",
    "Down the group the atoms become larger, so ionisation enthalpy and electronegativity fall and metallic "
    "character rises. With falling electronegativity, the tendency to gain electrons and show −3 falls (bismuth "
    "hardly forms compounds in −3).",
    ["(a) ✓", "(b) ✗: ionisation enthalpy decreases", "(c) ✓", "(d) ✓", "(e) ✗: electronegativity decreases"],
    why="(b) and (e) reverse the trends in ionisation enthalpy and electronegativity; options containing either "
        "are wrong.",
    ncert=f"{REF10}, group 15 elements: atomic and physical properties; oxidation states", seconds=50)

conf = {"Ga": "4s2 4p1", "As": "4s2 4p3", "Se": "4s2 4p4", "Br": "4s2 4p5"}
unpaired = {"Ga": 1, "As": 3, "Se": 2, "Br": 1}
assert 6 + 6 + 5 == 17
truth_c = {"a": unpaired["As"] == 3, "b": unpaired["Se"] == 2, "c": True, "d": unpaired["Ga"] == 3, "e": True}
assert truth_c == {"a": True, "b": True, "c": True, "d": False, "e": True}
add("Group 15 and 16 trends", A, "multi_statement",
    ms("Consider the ground-state atoms of gallium (Z = 31), arsenic (Z = 33), selenium (Z = 34) and bromine "
       "(Z = 35). Which of the following statements are correct?",
       ["An arsenic atom has three unpaired electrons.",
        "A selenium atom has two unpaired electrons.",
        "A bromine atom has 17 electrons with azimuthal quantum number l = 1.",
        "All three valence electrons of a gallium atom are unpaired.",
        "Each of the four atoms has ten electrons in its 3d subshell."]),
    multi("D", truth_c, ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Electronic configurations of the period 4 p-block elements",
    "All four have [Ar] 3d¹⁰ 4s² and then 4p¹ (Ga), 4p³ (As), 4p⁴ (Se) and 4p⁵ (Br). Apply Hund's rule to the "
    "4p electrons.",
    ["(a) As: 4p³ → three singly filled 4p orbitals → 3 unpaired ✓",
     "(b) Se: 4p⁴ → one pair + two singles → 2 unpaired ✓",
     "(c) Br: p electrons = 2p⁶ + 3p⁶ + 4p⁵ = 17 ✓",
     "(d) Ga: 4s² is paired; only the 4p¹ electron is unpaired ✗",
     "(e) all have 3d¹⁰ ✓"],
    why="Only (d) is false: the two 4s electrons of gallium share one orbital. Options that leave out a true "
        "statement or include (d) are wrong.",
    ncert=f"{REF10}, electronic configuration of groups 15–17; {REF10A}, group 13", seconds=90, checked=True)

add("Group 13 and 14 trends", A, "statement_pair",
    sp("Every p-block element of the sixth period, from thallium to radon, has a completely filled 4f subshell "
       "in its ground state.",
       "Every p-block element of the fifth period, from indium to xenon, has a completely filled 4d subshell "
       "in its ground state."),
    SP_, "Inner filled subshells of the heavier p-block elements",
    "The sixth-period p-block elements follow the lanthanoids and the 5d series: [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹⁻⁶. The "
    "fifth-period p-block elements follow the 4d series: [Kr] 4d¹⁰ 5s² 5p¹⁻⁶. These filled d and f subshells "
    "shield the nucleus poorly, which is behind several irregular trends in groups 13 to 17.",
    ["I: Tl to Rn = [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹⁻⁶ → true", "II: In to Xe = [Kr] 4d¹⁰ 5s² 5p¹⁻⁶ → true"],
    answer="A",
    why="Both statements follow from the order of filling (6s, 4f, 5d, 6p and 5s, 4d, 5p).",
    ncert=f"{REF10}, electronic configurations of p-block elements", seconds=50)

add("Group 13 and 14 trends", A, "match_list",
    lists("Match List-I (description of a p-block element in its ground state) with List-II (the element).",
          ["The period 4 element with three unpaired electrons",
           "The period 5 element whose valence shell is 5s² 5p²",
           "The period 6 element with three electrons in its 6p subshell",
           "The period 3 element with four valence p electrons"],
          ["Sulphur", "Bismuth", "Arsenic", "Tin"]),
    match("B", M("III IV II I"), [M("IV III II I"), M("III IV I II"), M("III II IV I")]),
    "Identifying p-block elements from their configurations",
    "Use the period for n and the number of valence p electrons for the group (group = 12 + number of p "
    "electrons for groups 13–18).",
    ["A: 4p³ → group 15, period 4 → As → III", "B: 5s² 5p² → group 14, period 5 → Sn → IV",
     "C: 6p³ → group 15, period 6 → Bi → II", "D: 3p⁴ → group 16, period 3 → S → I"],
    why="A-IV/B-III swaps arsenic and tin. C-I/D-II swaps bismuth and sulphur. B-II/C-IV puts tin and bismuth "
        "in each other's places.",
    ncert=f"{REF10}, electronic configurations of p-block elements", seconds=70)
