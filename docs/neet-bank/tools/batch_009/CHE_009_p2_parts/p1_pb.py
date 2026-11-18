
# ================================================================ p-Block Elements (2124-2136)
# 2125: group 16, period 4: [Ar] 3d10 4s2 4p4
z_2125 = 18 + 10 + 2 + 4
assert z_2125 == 34
# 2130: decomposition of AsH3 into its elements: dH = -n * dfH
n_2130 = F(156, 10) / mm(As=1, H=3)
dh_2130 = -n_2130 * F(664, 10)
assert n_2130 == F(1, 5) and f"{float(dh_2130):.1f}" == "-13.3"
v_2130 = f"{float(dh_2130):.1f} kJ".replace("-", "−")
# 2135: energy that turns 1.08 g B(g) into B3+(g) is used for Al(g) -> Al3+(g)
ie_B, ie_Al = 801 + 2427 + 3659, 577 + 1816 + 2744
assert (ie_B, ie_Al) == (6887, 5137)
e_2135 = F(108, 100) / AM["B"] * ie_B
m_2135 = e_2135 / ie_Al * AM["Al"]
assert f"{float(m_2135):.2f}" == "3.62"
assert f"{float(F(1, 10) * ie_Al / ie_B * 27):.2f}" == "2.01"            # ratio inverted
assert f"{float(F(1, 10) * 801 / 577 * 27):.2f}" == "3.75"              # first IE only
v_2135 = f"{float(m_2135):.2f} g"

QUESTIONS += [
    Q(T_PB, "Group 13 and 14 trends", "Basic", "direct",
      "Which of the following elements of group 14 is a metalloid?",
      ["Carbon", "Germanium", "Tin", "Lead"], "B",
      "Metallic character down group 14",
      "Metallic character increases down group 14. Carbon is a non-metal, germanium is a metalloid, and tin and lead "
      "are soft metals with low melting points.",
      ["Group 14: C, Si, Ge, Sn, Pb", "Non-metal → metalloid → metals on going down", "Germanium is the metalloid"],
      why_others_wrong="Carbon is a non-metal; tin and lead are metals.",
      ncert=f"{NC11}, 'The p-Block Elements', group 14: physical and chemical properties", seconds=20),

    N(T_PB, "Group 15 and 16 trends", "Basic",
      "An element of group 16 lies in the fourth period of the periodic table. Its atomic number is:",
      ["32", "33", "34", "35"], "C", str(z_2125),
      "Locating a p-block element from its group and period",
      "A group 16 element has the valence configuration ns² np⁴. In the fourth period this is 4s² 4p⁴, which follows the "
      "argon core and the filled 3d subshell.",
      ["Configuration: [Ar] 3d¹⁰ 4s² 4p⁴", "Z = 18 + 10 + 2 + 4 = 34 (selenium)"],
      shortcut="Period 4 ends at Kr (Z = 36); group 16 is two places before group 18, so Z = 36 − 2 = 34.",
      why_others_wrong="32 is germanium (group 14), 33 is arsenic (group 15) and 35 is bromine (group 17).",
      seconds=30),

    Q(T_PB, "Group 15 and 16 trends", "Basic", "statement_pair",
      *sp("In group 16, the electron gain enthalpy becomes less negative on going down from sulphur to polonium.", True,
          "The atomic radius of tellurium is smaller than that of sulphur.", False),
      "Electron gain enthalpy and atomic size in group 16",
      "Oxygen has a less negative electron gain enthalpy than sulphur because of its compact 2p subshell, but from "
      "sulphur onwards the value again becomes less negative up to polonium, as the atoms grow larger. Atomic radius "
      "increases down the group because a new shell is added each time, so tellurium is larger than sulphur.",
      ["Statement I: S → Se → Te → Po, electron gain enthalpy less negative: true",
       "Statement II: radius increases down the group, so Te > S: false"],
      ncert=f"{NC12}, 'The p-Block Elements', group 16: atomic and physical properties", seconds=35),

    Q(T_PB, "Group 17 and 18 trends", "Basic", "match_list",
      *ml("Match the halogen in List-I with its ground-state electronic configuration in List-II.",
          ["Fluorine (Z = 9)", "Chlorine (Z = 17)", "Bromine (Z = 35)", "Iodine (Z = 53)"],
          ["[Kr] 4d¹⁰ 5s² 5p⁵", "[Ar] 3d¹⁰ 4s² 4p⁵", "[Ne] 3s² 3p⁵", "[He] 2s² 2p⁵"],
          "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D"),
      "Electronic configuration of group 17 elements",
      "All halogens have the valence configuration ns² np⁵, with n equal to the period number. From period 4 "
      "onwards the filled (n−1)d¹⁰ subshell appears before the ns² np⁵ valence shell.",
      ["F (period 2): [He] 2s² 2p⁵ (IV)", "Cl (period 3): [Ne] 3s² 3p⁵ (III)",
       "Br (period 4): [Ar] 3d¹⁰ 4s² 4p⁵ (II)", "I (period 5): [Kr] 4d¹⁰ 5s² 5p⁵ (I)"],
      shortcut="Check the electron count: core + 2 + 5 (+10 for the d subshell) must equal Z.",
      why_others_wrong="Codes that swap fluorine and chlorine, or bromine and iodine, give configurations whose "
                       "electron count does not equal the atomic number.",
      ncert=f"{NC12}, 'The p-Block Elements', group 17: electronic configuration", seconds=35),

    Q(T_PB, "Anomalous first element", "Intermediate", "assertion_reason",
      *ar("Carbon cannot show a covalency greater than four, whereas silicon and the heavier elements of group 14 "
          "can expand their covalency beyond four.", True,
          "The valence shell of carbon has only the 2s and 2p orbitals (four orbitals in all) and no d orbitals, "
          "whereas the heavier elements have vacant d orbitals in their valence shell.", True, explains=True),
      "Anomalous behaviour of carbon",
      "The first member of group 14 has only four valence orbitals (2s, 2px, 2py, 2pz), so it can form at most four "
      "covalent bonds. Silicon and the heavier members have vacant d orbitals in the valence shell and can use them to "
      "show a covalency of six. R gives the cause of A.",
      ["Carbon: n = 2, no 2d subshell → 4 valence orbitals → maximum covalency 4",
       "Si onwards: vacant d orbitals → covalency can exceed 4", "R explains A"],
      ncert=f"{NC11}, 'The p-Block Elements', group 14: anomalous behaviour of carbon", seconds=35),

    Q(T_PB, "Group 15 and 16 trends", "Intermediate", "statement_pair",
      *sp("The stability of the halides of the group 16 elements decreases in the order fluoride > chloride > "
          "bromide > iodide.", True,
          "The first ionisation enthalpy decreases down group 16 from oxygen to tellurium.", True),
      "Group 16: halides and ionisation enthalpy",
      "Group 16 elements form many halides, and their stability falls from fluorides to iodides, in line with the "
      "falling strength of the E–X bond. Ionisation enthalpy decreases down the group because atomic size increases.",
      ["Statement I: stability of halides F > Cl > Br > I: true",
       "Statement II: ionisation enthalpy falls down the group: true"],
      ncert=f"{NC12}, 'The p-Block Elements', group 16: chemical properties", seconds=35),

    N(T_PB, "Group 15 and 16 trends", "Intermediate",
      "The standard enthalpies of formation (in kJ mol⁻¹) of some group 15 hydrides are: NH₃ −46.1, PH₃ +13.4, "
      "AsH₃ +66.4. What is the enthalpy change when 15.6 g of AsH₃(g) decomposes completely into arsenic and "
      "hydrogen (As = 75, H = 1)?",
      [v_2130, v_2130.replace("−", "+"), "−66.4 kJ", "−26.6 kJ"], "A", v_2130,
      "Enthalpy of decomposition and thermal stability of hydrides",
      "Decomposition into the elements is the reverse of formation, so ΔH(decomposition) = −ΔfH per mole. The values "
      "of ΔfH become more positive from NH₃ to AsH₃, which is why thermal stability falls down the group: the heavier "
      "hydrides decompose exothermically.",
      ["Molar mass of AsH₃ = 75 + 3 = 78 g mol⁻¹; n = 15.6/78 = 0.20 mol",
       "AsH₃ → As + 3/2 H₂: ΔH = −66.4 kJ mol⁻¹", "ΔH = 0.20 × (−66.4) ≈ −13.3 kJ"],
      why_others_wrong="+13.3 kJ keeps the sign of ΔfH instead of reversing it; −66.4 kJ is for one mole, not 0.20 mol; "
                       "−26.6 kJ uses 0.40 mol (doubling for 2AsH₃).",
      seconds=60),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the p-block elements are correct?",
          [("Across a period, from group 13 to group 17, the non-metallic character of the elements generally "
            "increases.", True),
           ("The p-block contains metals, non-metals and metalloids.", True),
           ("Down a group of the p-block, the metallic character of the elements decreases.", False),
           ("The inert pair effect becomes more marked for the heavier members of groups 13 to 16.", True),
           ("Metalloids are found only in group 14.", False)],
          [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "d", "e"]], "D"),
      "General features of the p-block",
      "The p-block has metals (Al, Sn, Pb, Bi, ...), non-metals (C, N, O, halogens, ...) and metalloids. Non-metallic "
      "character increases across a period and decreases (metallic character increases) down a group. The reluctance "
      "of the ns² pair to take part in bonding increases for the heavier elements, so the oxidation state two units "
      "below the group oxidation state becomes more stable in groups 13 to 16. Metalloids occur in several groups "
      "(Ge in 14, As and Sb in 15, Se and Te in 16).",
      ["(a) true", "(b) true", "(c) false: metallic character increases down a group", "(d) true",
       "(e) false: As, Sb, Se and Te are also metalloids"],
      ncert=f"{NC12}, 'The p-Block Elements', introduction and groups 15-16", seconds=50),

    Q(T_PB, "Group 13 and 14 trends", "Intermediate", "direct",
      "Which of the following shows the p-block elements of the third period in order of DECREASING metallic "
      "character?",
      ["Cl > S > P > Si > Al", "Si > Al > P > S > Cl", "Al > P > Si > S > Cl", "Al > Si > P > S > Cl"], "D",
      "Trend in metallic character across a period",
      "Across a period the nuclear charge increases and the atomic radius decreases, so ionisation enthalpy and "
      "electronegativity rise and the tendency to lose electrons falls. Metallic character therefore decreases from "
      "left to right: aluminium (group 13) is a metal and chlorine (group 17) a typical non-metal.",
      ["Period 3 p-block, left to right: Al (13), Si (14), P (15), S (16), Cl (17)",
       "Metallic character decreases across the period", "Order: Al > Si > P > S > Cl"],
      why_others_wrong="The first option is the order of increasing metallic character; the other two break the "
                       "left-to-right sequence of the period.",
      ncert=f"{NC12}, 'The p-Block Elements', introduction: metallic and non-metallic character", seconds=30),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "assertion_reason",
      *ar("Down group 15, the stability of the +5 oxidation state decreases and that of the +3 oxidation state "
          "increases.", True,
          "The ns² electrons of the heavier elements are increasingly reluctant to take part in bond formation "
          "(inert pair effect).", True, explains=True),
      "Inert pair effect in group 15",
      "The group 15 elements show +3 and +5. Because the ns² electrons of the heavier elements hold back from bonding "
      "(inert pair effect), only three electrons are commonly used by bismuth, so +3 becomes the more stable state and "
      "Bi(V) compounds are rare. R explains A.",
      ["Valence configuration ns² np³", "Heavier elements: ns² pair reluctant to bond",
       "So +3 more stable than +5 down the group"],
      ncert=f"{NC12}, 'The p-Block Elements', group 15: oxidation states and trends in chemical reactivity",
      seconds=40),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "statement_pair",
      *sp("The E–H bond length increases from NH₃ to SbH₃ in group 15.", True,
          "Since the F–F bond is the shortest X–X bond, F₂ has the highest bond dissociation enthalpy among the "
          "halogens.", False),
      "Bond length and bond strength trends",
      "As the size of E increases down group 15, the E–H bond becomes longer (about 102 pm in NH₃ to about 171 pm in "
      "SbH₃). F₂ does have the shortest bond, but its bond dissociation enthalpy (158.8 kJ mol⁻¹) is lower than those "
      "of Cl₂ and Br₂, because of the large repulsion between the lone pairs of the small fluorine atoms. Cl₂ has the "
      "highest value.",
      ["Statement I: E–H bond length increases with size of E: true",
       "Statement II: bond dissociation enthalpy order Cl₂ > Br₂ > F₂ > I₂: false"],
      ncert=f"{NC12}, 'The p-Block Elements', groups 15 and 17", seconds=45),

    N(T_PB, "Group 13 and 14 trends", "Advanced",
      "The first three ionisation enthalpies (in kJ mol⁻¹) are: boron 801, 2427, 3659; aluminium 577, 1816, 2744. The "
      "energy needed to convert 1.08 g of gaseous boron atoms completely into B³⁺(g) ions would convert what mass of "
      "gaseous aluminium atoms into Al³⁺(g) ions? (B = 10.8, Al = 27)",
      ["2.70 g", v_2135, "2.01 g", "3.75 g"], "B", v_2135,
      "Sum of ionisation enthalpies in group 13",
      "Forming M³⁺(g) needs the sum of the first three ionisation enthalpies. This sum is much larger for boron "
      "(6887 kJ mol⁻¹) than for aluminium (5137 kJ mol⁻¹), which is one reason boron does not form B³⁺ ions.",
      ["Boron: n = 1.08/10.8 = 0.10 mol; energy = 0.10 × 6887 = 688.7 kJ",
       "Aluminium: ΣIE = 577 + 1816 + 2744 = 5137 kJ mol⁻¹", "n(Al) = 688.7/5137 = 0.134 mol",
       "Mass = 0.134 × 27 ≈ 3.62 g"],
      why_others_wrong="2.70 g assumes equal moles; 2.01 g inverts the ratio of the sums; 3.75 g uses only the first "
                       "ionisation enthalpies.",
      seconds=100),

    Q(T_PB, "Group 15 and 16 trends", "Advanced", "multi_statement",
      *ms("The electron gain enthalpies (in kJ mol⁻¹) of some elements are: O −141, S −200, Se −195, Te −190; "
          "F −333, Cl −349, Br −325, I −296. Which of the following conclusions are correct?",
          [("In both groups, the element of the second period has a less negative electron gain enthalpy than the "
            "element of the third period.", True),
           ("Each halogen has a more negative electron gain enthalpy than the group 16 element of the same period.",
            True),
           ("From the third period downwards, the electron gain enthalpy becomes less negative in both groups.", True),
           ("Oxygen has a less negative value than sulphur because the oxygen atom is larger than the sulphur atom.",
            False),
           ("Adding an electron to a gaseous oxygen atom releases more energy than adding one to a gaseous fluorine "
            "atom.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "B"),
      "Reading electron gain enthalpy data for groups 16 and 17",
      "The data show the second-period anomaly (O and F less negative than S and Cl), the steady fall from the third "
      "period downwards, and the much more negative values of the halogens, which need only one electron to reach a "
      "noble gas configuration. The anomaly arises because oxygen and fluorine are very small, so the incoming "
      "electron is strongly repelled by the electrons already in the compact 2p subshell.",
      ["(a) −141 > −200 and −333 > −349: true", "(b) −333 < −141, −349 < −200, ...: true",
       "(c) S → Se → Te and Cl → Br → I become less negative: true",
       "(d) false: oxygen is smaller, not larger", "(e) false: −141 is less negative than −333"],
      ncert=f"{NC12}, 'The p-Block Elements', groups 16 and 17: atomic properties", seconds=75),
]
