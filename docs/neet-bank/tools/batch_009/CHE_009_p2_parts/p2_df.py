
# ================================================================ d- and f-Block Elements (2137-2147)
# 2137: 3d metals whose atoms have a 4s1 configuration (aufbau exceptions Cr and Cu)
conf_3d = {"Sc": (1, 2), "Ti": (2, 2), "V": (3, 2), "Cr": (5, 1), "Mn": (5, 2), "Fe": (6, 2), "Co": (7, 2),
           "Ni": (8, 2), "Cu": (10, 1), "Zn": (10, 2)}
assert all(d + s == z - 18 for (d, s), z in zip(conf_3d.values(), range(21, 31)))
v_2137 = str(sum(1 for d, s in conf_3d.values() if s == 1))
assert v_2137 == "2"
# 2141: Cr(VI) in dichromate is d0; Cr3+ is d3
v_2141 = f"{bm(0):.0f} BM to {bm(3):.2f} BM"
assert v_2141 == "0 BM to 3.87 BM"
# 2142: electrons accepted: Cr2O7(2-) -> 2Cr3+ : 2 x 3 = 6; MnO4- -> Mn2+ : 5
v_2142 = f"{float(F(2 * (6 - 3), 7 - 2)):.1f} mol"
assert v_2142 == "1.2 mol"
# 2145: I- per MnO4-: acidic (I- -> 1/2 I2, 1 e; MnO4- 5 e) = 5; neutral (I- -> IO3-, 6 e; MnO4- -> MnO2, 3 e) = 1/2
acid, neutral = F(5, 1), F(3, 6)
r_2145 = acid / neutral
assert r_2145 == 10
v_2145 = f"{r_2145} : 1"

QUESTIONS += [
    N(T_DF, "Transition element trends", "Basic",
      "How many elements of the first transition series (scandium to zinc) have only one electron in the 4s orbital "
      "in the ground state of the atom?",
      ["1", "2", "3", "4"], "B", v_2137,
      "Electronic configurations of the 3d series",
      "The 3d and 4s energies are close. Chromium and copper take one 4s electron into the 3d subshell to reach the "
      "more stable half-filled (3d⁵) and completely filled (3d¹⁰) arrangements: Cr [Ar] 3d⁵ 4s¹, Cu [Ar] 3d¹⁰ 4s¹. "
      "All the other 3d metals are 4s².",
      ["Sc to Zn: (n−1)d¹⁻¹⁰ ns², except", "Cr: 3d⁵ 4s¹", "Cu: 3d¹⁰ 4s¹", "Count = 2"],
      why_others_wrong="1 misses one of the two exceptions; 3 or 4 wrongly add manganese or zinc, which are 4s².",
      ncert=f"{NC12}, 'The d- and f-Block Elements', electronic configurations of the d-block elements", seconds=30),

    Q(T_DF, "Transition element trends", "Basic", "direct",
      "The metals of the second (4d) and third (5d) transition series have greater enthalpies of atomisation than the "
      "corresponding metals of the first (3d) series. According to NCERT, this is an important factor in accounting "
      "for:",
      ["the lanthanoid contraction", "the colour of their compounds", "the lower densities of the heavier metals",
       "the much more frequent metal–metal bonding in compounds of the heavy transition metals"], "D",
      "Enthalpy of atomisation of the 4d and 5d metals",
      "A greater enthalpy of atomisation means stronger metal–metal interaction. This is why metal–metal bonds occur "
      "much more often in compounds of the heavy (4d and 5d) transition metals than in those of the 3d metals.",
      ["4d, 5d metals: higher ΔaH than 3d", "Stronger M–M bonding", "→ metal–metal bonds common in their compounds"],
      why_others_wrong="The lanthanoid contraction comes from poor shielding by 4f electrons; colour comes from d–d "
                       "transitions; the 4d and 5d metals are denser, not less dense, than the 3d metals.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', physical properties of the transition elements", seconds=30),

    Q(T_DF, "Transition element trends", "Basic", "assertion_reason",
      *ar("Scandium (Z = 21) is regarded as a transition element, although its only common ion, Sc³⁺, has no d "
          "electron.", True,
          "In its ground state, the scandium atom has an incompletely filled 3d subshell (3d¹).", True, explains=True),
      "Definition of a transition element",
      "A transition element is one that has an incompletely filled d subshell in its ground state or in any of its "
      "common oxidation states. The scandium atom is [Ar] 3d¹ 4s², so it qualifies through its atom even though Sc³⁺ "
      "is 3d⁰. R gives the reason for A.",
      ["Sc: [Ar] 3d¹ 4s²", "Incomplete d subshell in the atom", "→ transition element"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', position in the periodic table and definition", seconds=30),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "statement_pair",
      *sp("Across the actinoid series, the maximum oxidation state first increases, from +4 for thorium to +5, +6 and "
          "+7 for protactinium, uranium and neptunium, and then decreases in the later elements.", True,
          "The ground-state electronic configuration of cerium (Z = 58) is [Xe] 4f² 6s².", False),
      "Oxidation states of actinoids; configuration of cerium",
      "NCERT notes that the maximum oxidation state of the actinoids rises up to the middle of the series and then "
      "falls. Cerium, the first lanthanoid, has the configuration [Xe] 4f¹ 5d¹ 6s², not 4f² 6s².",
      ["Statement I: true (Th +4, Pa +5, U +6, Np +7, then decrease)",
       "Statement II: false; Ce is [Xe] 4f¹ 5d¹ 6s²"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids and the actinoids", seconds=40),

    N(T_DF, "Magnetic and colour properties", "Intermediate",
      "When acidified potassium dichromate acts as an oxidising agent, chromium changes from the dichromate ion to "
      "Cr³⁺. The spin-only magnetic moment of the chromium species changes from (Z of Cr = 24):",
      ["0 BM to 2.83 BM", v_2141, "1.73 BM to 3.87 BM", "3.87 BM to 0 BM"], "B", v_2141,
      "Spin-only magnetic moment and oxidation state",
      "In Cr₂O₇²⁻ chromium is +6, which is 3d⁰: no unpaired electron. Cr³⁺ is 3d³ with three unpaired electrons.",
      ["Cr: [Ar] 3d⁵ 4s¹", "Cr(VI): 3d⁰ → n = 0 → μ = 0", "Cr³⁺: 3d³ → n = 3 → μ = √(3 × 5) = √15 ≈ 3.87 BM"],
      why_others_wrong="2.83 BM is for two unpaired electrons; 1.73 BM would need one unpaired electron in the "
                       "dichromate ion; the last option reverses the direction of the change.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', magnetic properties; potassium dichromate", seconds=45),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "In acidic solution, the dichromate ion is reduced to Cr³⁺ and the permanganate ion to Mn²⁺. How many moles of "
      "KMnO₄ have the same oxidising capacity (accept the same number of electrons) as 1 mol of K₂Cr₂O₇?",
      ["0.83 mol", "1.0 mol", "2.4 mol", v_2142], "D", v_2142,
      "Electrons accepted by dichromate and permanganate",
      "Each Cr goes from +6 to +3, so one Cr₂O₇²⁻ ion accepts 2 × 3 = 6 electrons. Each MnO₄⁻ goes from +7 to +2 and "
      "accepts 5 electrons.",
      ["Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O", "MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O",
       "Moles of KMnO₄ = 6/5 = 1.2 mol"],
      why_others_wrong="0.83 mol inverts the ratio (5/6); 1.0 mol ignores the different electron counts; 2.4 mol counts "
                       "6 electrons per chromium atom.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxidising action of K₂Cr₂O₇ and KMnO₄", seconds=45),

    Q(T_DF, "Lanthanoids and actinoids", "Intermediate", "match_list",
      *ml("Match the actinoid in List-I with its ground-state electronic configuration in List-II (Rn = radon core).",
          ["Thorium (Z = 90)", "Uranium (Z = 92)", "Plutonium (Z = 94)", "Curium (Z = 96)"],
          ["[Rn] 5f⁶ 7s²", "[Rn] 6d² 7s²", "[Rn] 5f⁷ 6d¹ 7s²", "[Rn] 5f³ 6d¹ 7s²"],
          "II IV I III", ["II III I IV", "IV II I III", "II IV III I"], "C"),
      "Electronic configurations of actinoids",
      "Thorium has no 5f electron in its ground state (6d² 7s²). Uranium is 5f³ 6d¹ 7s². Plutonium places all its "
      "electrons beyond the 7s² pair in 5f (5f⁶ 7s²), while curium keeps a half-filled 5f⁷ and puts the next "
      "electron in 6d (5f⁷ 6d¹ 7s²).",
      ["Th (90): [Rn] 6d² 7s² (II)", "U (92): [Rn] 5f³ 6d¹ 7s² (IV)", "Pu (94): [Rn] 5f⁶ 7s² (I)",
       "Cm (96): [Rn] 5f⁷ 6d¹ 7s² (III)"],
      shortcut="Count electrons beyond the radon core (Z − 86): Th 4, U 6, Pu 8, Cm 10; each configuration in "
               "List-II adds up to one of these.",
      why_others_wrong="Codes that swap uranium and curium, or plutonium and curium, give a configuration whose "
                       "electron count does not match Z − 86.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the actinoids: electronic configurations", seconds=50),

    Q(T_DF, "Transition element trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the oxidation states of the d-block elements are correct?",
          [("The elements showing the greatest number of oxidation states occur in or near the middle of the 3d "
            "series.", True),
           ("Scandium and zinc show few oxidation states, scandium because it has few electrons to lose and zinc "
            "because it has a full d subshell.", True),
           ("In the d-block, higher oxidation states are favoured by the heavier members of a group, the opposite of "
            "the trend in the p-block.", True),
           ("Cr(VI) compounds are weaker oxidising agents than Mo(VI) and W(VI) compounds.", False)],
          [["a", "d"], ["b", "c", "d"], ["a", "b", "c", "d"]], "B"),
      "Trends in oxidation states of the transition elements",
      "Manganese, near the middle of the 3d series, shows every state from +2 to +7. Near the ends there are either "
      "too few electrons to lose or share (Sc, Ti) or too many d electrons and hence fewer orbitals available (Cu, "
      "Zn). In group 6, Mo(VI) and W(VI) are more stable than Cr(VI); so dichromate (Cr(VI)) in acid is a strong "
      "oxidising agent, whereas MoO₃ and WO₃ are not.",
      ["(a) true", "(b) true", "(c) true", "(d) false: Cr(VI) is the stronger oxidising agent"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', variation in oxidation states", seconds=55),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "Permanganate oxidises iodide to iodine in acidic solution (MnO₄⁻ → Mn²⁺), but to iodate, IO₃⁻, in neutral or "
      "faintly alkaline solution (MnO₄⁻ → MnO₂). For the same amount of KMnO₄, the ratio of the moles of iodide "
      "oxidised in acidic solution to that in neutral solution is:",
      ["1 : 10", "5 : 3", v_2145, "5 : 1"], "C", v_2145,
      "Electron balance in permanganate oxidations",
      "Count electrons per MnO₄⁻ and per I⁻ in each medium. In acid each MnO₄⁻ takes 5 electrons and each I⁻ gives "
      "1 (to ½I₂). In neutral solution each MnO₄⁻ takes 3 electrons and each I⁻ gives 6 (from −1 to +5 in IO₃⁻).",
      ["Acidic: 2MnO₄⁻ + 10I⁻ + 16H⁺ → 2Mn²⁺ + 5I₂ + 8H₂O → 5 mol I⁻ per mol MnO₄⁻",
       "Neutral: 2MnO₄⁻ + I⁻ + H₂O → 2MnO₂ + IO₃⁻ + 2OH⁻ → 0.5 mol I⁻ per mol MnO₄⁻",
       "Ratio = 5 : 0.5 = 10 : 1"],
      why_others_wrong="1 : 10 inverts the ratio; 5 : 3 compares only the electrons taken by MnO₄⁻ and ignores the "
                       "change in the iodide product; 5 : 1 assumes iodide gives one electron in both media.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate: oxidising properties", seconds=90),

    Q(T_DF, "Transition element trends", "Advanced", "assertion_reason",
      *ar("Iron(III) ions catalyse the reaction between iodide and persulphate ions, 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻.", True,
          "Fe³⁺ oxidises I⁻ to I₂ and is itself reduced to Fe²⁺, which is then oxidised back to Fe³⁺ by S₂O₈²⁻; this "
          "is possible because iron changes readily between the +2 and +3 oxidation states.", True, explains=True),
      "Catalytic action of transition metal ions",
      "Transition metal ions catalyse reactions largely because they can change their oxidation state. Here the "
      "catalyst is used up in the first step (2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂) and regenerated in the second "
      "(2Fe²⁺ + S₂O₈²⁻ → 2Fe³⁺ + 2SO₄²⁻). R describes exactly how the catalysis occurs.",
      ["Step 1: 2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂", "Step 2: 2Fe²⁺ + S₂O₈²⁻ → 2Fe³⁺ + 2SO₄²⁻",
       "Net: 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻, Fe³⁺ regenerated"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', catalytic properties", seconds=45),

    Q(T_DF, "Transition element trends", "Advanced", "direct",
      "The standard electrode potentials E°(M³⁺/M²⁺) of some 3d metals are: Cr −0.41 V, Mn +1.57 V, Fe +0.77 V, "
      "Co +1.97 V. Which of the following conclusions is correct?",
      ["Mn³⁺ is a weaker oxidising agent than Fe³⁺.",
       "Co²⁺ is oxidised to Co³⁺ more easily than Fe²⁺ is oxidised to Fe³⁺.",
       "Fe³⁺ is the strongest oxidising agent among the four M³⁺ ions.",
       "Cr²⁺ is the strongest reducing agent among the four M²⁺ ions."], "D",
      "Using E°(M³⁺/M²⁺) to compare oxidising and reducing power",
      "The more positive E°(M³⁺/M²⁺), the more readily M³⁺ is reduced (strong oxidising agent) and the harder it is "
      "to oxidise M²⁺. The most negative value, for chromium, means Cr²⁺ is the most easily oxidised, i.e. the "
      "strongest reducing agent (Cr²⁺ d⁴ → Cr³⁺ d³, a half-filled t₂g level).",
      ["Order of oxidising power of M³⁺: Co³⁺ > Mn³⁺ > Fe³⁺ > Cr³⁺",
       "Order of reducing power of M²⁺: Cr²⁺ > Fe²⁺ > Mn²⁺ > Co²⁺", "Strongest reducing agent: Cr²⁺"],
      why_others_wrong="Mn³⁺ (+1.57 V) is a stronger oxidising agent than Fe³⁺ (+0.77 V); Co²⁺ is harder to oxidise "
                       "than Fe²⁺ because its E° is more positive; Co³⁺, not Fe³⁺, is the strongest oxidising agent.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', trends in the M³⁺/M²⁺ standard electrode potentials",
      seconds=60),
]
