

# ==================================================================== 11. d- and f-Block Elements
topic("d- and f-Block Elements")
REF11 = f"{C12}, 'The d- and f-Block Elements'"

cr_o = 2 * 4
assert cr_o == 8 and 7 == 4 + 4 - 1
add("K2Cr2O7 and KMnO4", B, "numerical",
    "In the dichromate ion, Cr₂O₇²⁻, two CrO₄ tetrahedra share one corner (one oxygen atom). The total number "
    "of chromium–oxygen linkages in the ion (counting each Cr–O connection once, whatever its bond order) is:",
    Opts("C", "8", ["7", "6", "4"]),
    "Structure of the dichromate ion",
    "Each chromium atom sits at the centre of a tetrahedron and is linked to four oxygen atoms. The shared "
    "(bridging) oxygen is linked to both chromium atoms, so it accounts for two Cr–O linkages.",
    ["Each Cr: 4 Cr–O linkages", "Two Cr atoms: 2 × 4 = 8",
     "Check: 6 terminal O (one link each) + 1 bridging O (two links) = 8"],
    why="7 counts oxygen atoms instead of linkages. 6 counts only the terminal oxygens. 4 counts the linkages of "
        "one chromium atom only.",
    ncert=f"{REF11}, potassium dichromate (structures of chromate and dichromate ions)", seconds=35,
    checked=True)

add("Transition element trends", B, "direct",
    "In each transition series, the melting points of the metals rise to a maximum at about which d-electron "
    "configuration (apart from the anomalous values of Mn and Tc), and then fall?",
    Opts("B", "d⁵", ["d¹⁰", "d¹", "d⁸"]),
    "Melting points of the transition metals",
    "Strong metallic bonding involves the (n − 1)d as well as the ns electrons. The number of unpaired d "
    "electrons available for bonding is greatest around the middle of the series, so the melting points rise "
    "to a maximum at about d⁵ and then fall as the d electrons pair up.",
    ["Unpaired d electrons peak at d⁵", "More electrons in metallic bonding → higher melting point"],
    why="d¹⁰ metals (Zn, Cd, Hg) have the lowest melting points; d¹ is at the start of the rise; d⁸ lies on the "
        "falling side.",
    ncert=f"{REF11}, physical properties of the transition elements", seconds=30)

add("Transition element trends", B, "statement_pair",
    sp("With the exceptions of Zn, Cd and Hg, the transition metals are very hard and have low volatility.",
       "Across the 3d series, the enthalpy of atomisation increases steadily from scandium to zinc."),
    SP_, "Hardness, volatility and enthalpy of atomisation of transition metals",
    "NCERT notes that, apart from Zn, Cd and Hg, the transition metals are very hard and have low volatility. "
    "Their enthalpies of atomisation are high and pass through a maximum around the middle of each series "
    "(many unpaired d electrons in metallic bonding); zinc, with a full 3d¹⁰ subshell, has the lowest value in "
    "the 3d series.",
    ["I: NCERT statement → true", "II: maximum near the middle, minimum at Zn → not a steady increase → false"],
    answer="C",
    why="Statement II ignores the maximum in the middle of the series and the very low value for zinc.",
    ncert=f"{REF11}, physical properties of the transition elements", seconds=40)

e_lost = 1 + 2 * 3
assert e_lost == 7 and 4 * e_lost == 7 * 4
add("K2Cr2O7 and KMnO4", I, "numerical",
    "In the first step of the manufacture of potassium dichromate, chromite ore is fused with sodium carbonate "
    "in free access of air: 4FeCr₂O₄ + 8Na₂CO₃ + 7O₂ → 8Na₂CrO₄ + 2Fe₂O₃ + 8CO₂. The number of electrons lost "
    "by ONE formula unit of FeCr₂O₄ in this reaction is:",
    Opts("D", "7", ["6", "3", "1.75"]),
    "Electron count from changes in oxidation number",
    "In FeCr₂O₄ iron is +2 and chromium is +3. Iron ends as Fe₂O₃ (+3) and chromium as Na₂CrO₄ (+6).",
    ["Fe: +2 → +3 → 1 electron", "Cr: +3 → +6 → 3 electrons each × 2 = 6", "Total = 1 + 6 = 7 electrons",
     "Check: 4 FeCr₂O₄ lose 28 e⁻; 7 O₂ gain 7 × 4 = 28 e⁻"],
    why="6 forgets that iron is also oxidised. 3 counts only one chromium atom. 1.75 is the number of O₂ "
        "molecules used per formula unit, not the number of electrons.",
    ncert=f"{REF11}, preparation of potassium dichromate", seconds=50, checked=True)

add("K2Cr2O7 and KMnO4", I, "match_list",
    lists("Match List-I (reaction) with List-II (the oxidation product formed from the reducing agent).",
          ["KMnO₄ and KI in acidic solution", "KMnO₄ and KI in neutral or faintly alkaline solution",
           "K₂Cr₂O₇ and H₂S in acidic solution", "KMnO₄ and Na₂S₂O₃ in neutral or faintly alkaline solution"],
          ["SO₄²⁻", "I₂", "S", "IO₃⁻"]),
    match("C", M("II IV III I"), [M("IV II III I"), M("II IV I III"), M("II III IV I")]),
    "Oxidising reactions of permanganate and dichromate",
    "In acid, permanganate oxidises iodide to iodine; in neutral or faintly alkaline solution it oxidises "
    "iodide further, to iodate, and thiosulphate to sulphate. Acidified dichromate oxidises H₂S, precipitating "
    "sulphur.",
    ["A: I⁻ → I₂ → II", "B: I⁻ → IO₃⁻ → IV", "C: H₂S → S → III", "D: S₂O₃²⁻ → SO₄²⁻ → I"],
    why="A-IV/B-II swaps the products of iodide in acidic and neutral solution. C-I/D-III swaps the sulphur "
        "products. B-III/C-IV gives iodide the sulphur product.",
    ncert=f"{REF11}, oxidising properties of KMnO₄ and K₂Cr₂O₇", seconds=60)

add("Transition element trends", I, "assertion_reason",
    ar("Manganese shows the largest number of oxidation states among the elements of the first transition "
       "series.",
       "Manganese has an anomalously low melting point compared with the neighbouring 3d metals."),
    AR_, "Oxidation states and melting points of the 3d metals",
    "A is true: manganese (3d⁵ 4s²) shows every oxidation state from +2 to +7, because all seven 4s and 3d "
    "electrons can take part in bonding. R is also true (NCERT notes the anomalous melting point of Mn), but "
    "the melting point of the metal has nothing to do with the number of oxidation states it shows.",
    ["A: Mn shows +2 to +7 → true", "R: anomalous (low) melting point of Mn → true",
     "R is an unrelated physical property → option B"],
    answer="B",
    why="The range of oxidation states comes from the seven 3d and 4s electrons available for bonding, not from "
        "the melting point; both statements are true, so C and D are wrong.",
    ncert=f"{REF11}, general properties of the transition elements (melting points; oxidation states)",
    seconds=40)

truth_int = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Transition element trends", I, "multi_statement",
    ms("Interstitial compounds are formed when small atoms such as H, C or N are trapped inside the crystal "
       "lattices of transition metals. Which of the following statements about them are correct?",
       ["They have high melting points, higher than those of the pure metals.",
        "They are very hard.",
        "They retain metallic conductivity.",
        "Their formulae, such as TiC or Mn₄N, correspond to normal oxidation states of the metal.",
        "They are typical ionic compounds."]),
    multi("D", truth_int, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (c) only"]),
    "Characteristics of interstitial compounds",
    "NCERT: interstitial compounds have high melting points (higher than the pure metals), are very hard, "
    "retain metallic conductivity and are chemically inert. They are usually non-stoichiometric, their "
    "formulae do not correspond to any normal oxidation state of the metal, and they are neither typically "
    "ionic nor covalent.",
    ["(a) ✓", "(b) ✓", "(c) ✓", "(d) ✗: formulae do not match normal oxidation states",
     "(e) ✗: neither typically ionic nor covalent"],
    why="(d) and (e) describe ordinary ionic compounds, which interstitial compounds are not; '(a) and (c) "
        "only' leaves out their hardness.",
    ncert=f"{REF11}, interstitial compounds", seconds=50)

d_counts = {"Ti²⁺": 2, "Cr²⁺": 4, "Mn²⁺": 5, "Ni²⁺": 8}
unp = {k: (v if v <= 5 else 10 - v) for k, v in d_counts.items()}
assert max(unp, key=unp.get) == "Mn²⁺" and unp == {"Ti²⁺": 2, "Cr²⁺": 4, "Mn²⁺": 5, "Ni²⁺": 2}
add("Magnetic and colour properties", I, "direct",
    "Which of the following gaseous ions has the HIGHEST spin-only magnetic moment? (Z: Ti = 22, Cr = 24, "
    "Mn = 25, Ni = 28)",
    Opts("A", "Mn²⁺", ["Ti²⁺", "Cr²⁺", "Ni²⁺"]),
    "Spin-only magnetic moment μ = √[n(n + 2)] BM rises with the number of unpaired electrons n",
    "Write the 3d configuration of each M²⁺ ion (the 4s electrons are lost first) and count unpaired electrons "
    "by Hund's rule.",
    ["Ti²⁺: 3d² → 2 unpaired", "Cr²⁺: 3d⁴ → 4 unpaired", "Mn²⁺: 3d⁵ → 5 unpaired (largest)",
     "Ni²⁺: 3d⁸ → 2 unpaired"],
    why="Cr²⁺ has four unpaired electrons, Ti²⁺ and Ni²⁺ two each; Mn²⁺ (3d⁵) has the maximum of five.",
    ncert=f"{REF11}, magnetic properties", seconds=40, checked=True)

mu = {n: math.sqrt(n * (n + 2)) for n in (3, 4, 5, 6)}
assert close(mu[5], 5.92, 0.002) and close(mu[4], 4.90, 0.002) and close(mu[3], 3.87, 0.002) \
    and close(mu[6], 6.93, 0.002)
add("Magnetic and colour properties", A, "numerical",
    "A gaseous M²⁺ ion of a first-row transition metal has a spin-only magnetic moment of 5.92 BM. The "
    "spin-only magnetic moment of the M³⁺ ion of the same metal is (√15 = 3.87, √24 = 4.90, √35 = 5.92, "
    "√48 = 6.93):",
    Opts("C", "4.90 BM", ["5.92 BM", "6.93 BM", "3.87 BM"]),
    "Spin-only magnetic moment μ = √[n(n + 2)] BM; identifying the ion from μ",
    "5.92 BM = √35 means n(n + 2) = 35, so n = 5 unpaired electrons: M²⁺ is 3d⁵, i.e. Mn²⁺. Then Mn³⁺ is 3d⁴ "
    "with four unpaired electrons.",
    ["√[n(n + 2)] = 5.92 → n = 5 → M²⁺ = 3d⁵ → Mn²⁺", "Mn³⁺ = 3d⁴ → n = 4",
     "μ = √(4 × 6) = √24 = 4.90 BM"],
    why="5.92 BM assumes the moment does not change on oxidation. 6.93 BM adds an electron instead of removing "
        "one. 3.87 BM removes two d electrons.",
    ncert=f"{REF11}, magnetic properties", seconds=80, checked=True)

add("Lanthanoids and actinoids", A, "match_list",
    lists("Match List-I (element) with List-II (its ground-state electronic configuration). (Z: La = 57, "
          "Gd = 64, Yb = 70, Lu = 71; Xe = 54)",
          ["Lanthanum", "Gadolinium", "Ytterbium", "Lutetium"],
          ["[Xe] 4f¹⁴ 6s²", "[Xe] 5d¹ 6s²", "[Xe] 4f¹⁴ 5d¹ 6s²", "[Xe] 4f⁷ 5d¹ 6s²"]),
    match("B", M("II IV I III"), [M("II IV III I"), M("IV II I III"), M("II I IV III")]),
    "Electronic configurations of the lanthanoids",
    "The general configuration is [Xe] 4f¹⁻¹⁴ 5d⁰⁻¹ 6s². A 5d electron appears in La (no 4f electrons), in Gd "
    "(after the half-filled 4f⁷) and in Lu (after the full 4f¹⁴); Yb has a full 4f¹⁴ with no 5d electron.",
    ["A: La (57) = [Xe] 5d¹ 6s² → II", "B: Gd (64) = [Xe] 4f⁷ 5d¹ 6s² → IV", "C: Yb (70) = [Xe] 4f¹⁴ 6s² → I",
     "D: Lu (71) = [Xe] 4f¹⁴ 5d¹ 6s² → III"],
    why="C-III/D-I swaps ytterbium and lutetium (Lu has the extra 5d electron). A-IV/B-II swaps lanthanum and "
        "gadolinium. B-I/C-IV gives gadolinium a full 4f subshell.",
    ncert=f"{REF11}, the lanthanoids: electronic configurations", seconds=60, checked=False)

truth_para = {"a": True, "b": False, "c": True, "d": False, "e": True}
add("Magnetic and colour properties", A, "multi_statement",
    ms("Which of the following gaseous ions are paramagnetic? (Z: Sc = 21, Ti = 22, Cr = 24, Co = 27, Cu = 29)",
       ["Ti³⁺", "Cu⁺", "Cr³⁺", "Sc³⁺", "Co²⁺"]),
    multi("D", truth_para, ["(a), (b) and (c) only", "(c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Paramagnetism arises from unpaired electrons",
    "Write the 3d configuration of each ion. Ions with no unpaired electrons (3d⁰ or 3d¹⁰) are diamagnetic.",
    ["(a) Ti³⁺: 3d¹ → 1 unpaired ✓", "(b) Cu⁺: 3d¹⁰ → diamagnetic ✗", "(c) Cr³⁺: 3d³ → 3 unpaired ✓",
     "(d) Sc³⁺: 3d⁰ → diamagnetic ✗", "(e) Co²⁺: 3d⁷ → 3 unpaired ✓"],
    why="Cu⁺ (3d¹⁰) and Sc³⁺ (3d⁰) have no unpaired electrons; options including either are wrong, and "
        "'(c) and (e) only' misses Ti³⁺.",
    ncert=f"{REF11}, magnetic properties", seconds=60)

truth_act = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Lanthanoids and actinoids", A, "multi_statement",
    ms("Which of the following statements about the electronic configurations and oxidation states of the "
       "actinoids are correct?",
       ["The actinoids show a greater range of oxidation states than the lanthanoids.",
        "The +3 oxidation state is common to the actinoids.",
        "Thorium (Z = 90) has no 5f electron in its ground-state configuration.",
        "The maximum oxidation state shown by uranium is +7.",
        "The general electronic configuration of the actinoids is [Rn] 5f¹⁻¹⁴ 6d⁰⁻¹ 7s¹."]),
    multi("C", truth_act, ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (e) only"]),
    "Actinoids: electronic configurations and oxidation states",
    "The 5f, 6d and 7s levels have comparable energies, so the actinoids show a wide range of oxidation states, "
    "with +3 common to the series. Thorium is [Rn] 6d² 7s². Uranium's maximum is +6 (+7 is reached by Np and "
    "Pu). The general configuration ends in 7s².",
    ["(a) ✓", "(b) ✓", "(c) Th = [Rn] 6d² 7s² → no 5f electron ✓", "(d) ✗: U maximum is +6",
     "(e) ✗: 7s², not 7s¹"],
    why="(d) gives uranium neptunium's maximum oxidation state and (e) has the wrong 7s occupancy; options "
        "containing either are wrong.",
    ncert=f"{REF11}, the actinoids: electronic configurations and oxidation states", seconds=70)
