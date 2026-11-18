

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Valence and reactivity", B, "direct",
    "Using the usual valences of the elements (magnesium 2, nitrogen 3), the formula of the simplest compound "
    "formed between magnesium and nitrogen is predicted to be:",
    Opts("B", "Mg₃N₂", ["Mg₂N₃", "MgN", "MgN₂"]),
    "Predicting formulae from the valences of elements",
    "The valence of a group 2 element is 2 and that of a group 15 element towards a metal is 3 (8 − 5). Cross the "
    "valences: Mg₃N₂ (3 × 2 = 2 × 3).",
    ["Mg: valence 2; N: valence 8 − 5 = 3", "Lowest common multiple 6 → 3 Mg and 2 N → Mg₃N₂"],
    why="Mg₂N₃ swaps the valences. MgN and MgN₂ do not balance the valences of the two elements.",
    ncert=f"{REF9}, periodic trends in chemical properties: periodicity of valence", seconds=25)

add("Modern periodic table", B, "direct",
    "In the modern periodic table, the lanthanoid series consists of the elements with atomic numbers:",
    Opts("A", "58 to 71 (cerium to lutetium)", ["57 to 70", "90 to 103 (thorium to lawrencium)",
                                               "21 to 30 (scandium to zinc)"]),
    "Position of the f-block elements",
    "The lanthanoids are the fourteen elements that follow lanthanum, from cerium (Z = 58) to lutetium "
    "(Z = 71); they are placed separately at the bottom of the table, with the actinoids, thorium (Z = 90) to "
    "lawrencium (Z = 103).",
    ["Lanthanoids: Ce (58) – Lu (71)", "Actinoids: Th (90) – Lr (103)"],
    why="57 to 70 starts at lanthanum and stops before lutetium. 90 to 103 is the actinoid series. 21 to 30 is "
        "the first transition (3d) series.",
    ncert=f"{REF9}, the f-block elements (inner-transition elements)", seconds=25)

add("Modern periodic table", B, "match_list",
    lists("Match List-I (group of the periodic table) with List-II (family name of its elements).",
          ["Group 1", "Group 2", "Group 16", "Group 17"],
          ["Chalcogens", "Halogens", "Alkali metals", "Alkaline earth metals"]),
    match("B", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("III I IV II")]),
    "Family names of groups in the periodic table",
    "Group 1: alkali metals; group 2: alkaline earth metals; group 16: chalcogens; group 17: halogens; group 18: "
    "noble gases.",
    ["A → III", "B → IV", "C → I", "D → II"],
    why="The wrong codes interchange the alkali and alkaline earth metals, or the chalcogens and halogens.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=20)

add("Modern periodic table", I, "statement_pair",
    sp("The elements of group 18 have completely filled valence shells, ns² np⁶ (helium: 1s²).",
       "All the p-block elements are non-metals."),
    SP_, "The p-block and group 18",
    "Group 18 (noble gases) have filled valence shells: Statement I is true. The p-block contains metals (such "
    "as aluminium, tin and lead), metalloids (such as silicon and germanium) and non-metals; non-metallic "
    "character increases from left to right and decreases down a group. Statement II is false.",
    ["I: noble gases ns² np⁶ (He 1s²) → true", "II: p-block has metals, metalloids and non-metals → false"],
    answer="C",
    why="Statement II ignores the metals of the lower left part of the p-block.",
    ncert=f"{REF9}, p-block elements; metals, non-metals and metalloids", seconds=30)

add("Valence and reactivity", I, "assertion_reason",
    ar("Carbon and nitrogen form multiple bonds to themselves (C=C, C≡C, N≡N) much more readily than silicon and "
       "phosphorus do.",
       "Because of their small size, the second-period elements show a greater ability to form pπ–pπ multiple "
       "bonds to themselves and to other second-period elements."),
    AR_, "Anomalous behaviour of the first member of a group",
    "NCERT notes that the first member of each p-block group, being small (with only four valence orbitals and "
    "high electronegativity), differs from the rest of its group; in particular it forms pπ–pπ multiple bonds "
    "with itself (C=C, C≡C, N=N, N≡N) and with other second-period elements (C=O, C≡N, N=O) far more readily "
    "than the later members. R gives this reason for A.",
    ["A: C and N form strong multiple bonds; Si and P much less → true",
     "R: small size → effective sideways p–p overlap → pπ–pπ bonds → true and explains A"],
    answer="A",
    why="Both are true, and the greater pπ–pπ bonding ability of the small second-period atoms is exactly the "
        "cause of A.",
    ncert=f"{REF9}, anomalous properties of second period elements", seconds=45)

truth9 = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Atomic and ionic radii", I, "multi_statement",
    ms("Which of the following comparisons of size are correct?",
       ["Atomic radius: Be > B", "Ionic radius: Li⁺ < Na⁺", "Radius: S²⁻ > S", "Atomic radius: C < N",
        "Ionic radius: Fe²⁺ < Fe³⁺"]),
    multi("D", truth9, ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (d) only"]),
    "Trends in atomic and ionic radii",
    "Atomic radius falls across a period (Be > B; C > N) and rises down a group (Li⁺ < Na⁺). An anion is larger "
    "than its atom (S²⁻ > S). Removing more electrons from the same atom gives a smaller ion (Fe³⁺ < Fe²⁺).",
    ["(a) across period 2 the radius falls → Be > B ✓", "(b) down group 1 → Li⁺ < Na⁺ ✓", "(c) anion > atom ✓",
     "(d) C (77 pm) > N (74 pm) ✗", "(e) Fe³⁺ < Fe²⁺ ✗"],
    why="(d) reverses the trend across a period and (e) reverses the effect of the ionic charge.",
    ncert=f"{REF9}, atomic radius; ionic radius", seconds=50)

egh = {"Li": -60, "Na": -53, "K": -48}
assert sorted(egh, key=egh.get) == ["Li", "Na", "K"]
add("Ionisation and electron gain enthalpy", I, "direct",
    "Which of the following arranges lithium, sodium and potassium in order from the MOST negative to the LEAST "
    "negative electron gain enthalpy?",
    Opts("B", "Li > Na > K", ["K > Na > Li", "Na > Li > K", "Na > K > Li"]),
    "Variation of electron gain enthalpy down a group",
    "Down a group the size increases and the added electron is farther from the nucleus, so less energy is "
    "released. NCERT's values (kJ mol⁻¹): Li −60, Na −53, K −48.",
    ["Li −60 (most negative) → Na −53 → K −48 (least negative)"],
    why="The other orders place a larger atom before a smaller one, against the trend (and the NCERT values) "
        "for the alkali metals.",
    ncert=f"{REF9}, electron gain enthalpy", seconds=30)

add("Valence and reactivity", A, "assertion_reason",
    ar("The highest valence shown by chlorine in its compounds with oxygen is 1.",
       "Chlorine shows a valence of 1 in its hydride, HCl."),
    AR_, "Periodicity of valence: valence towards hydrogen and towards oxygen",
    "Towards hydrogen a group 17 element shows valence 8 − 7 = 1 (HCl), so R is true. Towards oxygen, however, "
    "chlorine can use all seven valence electrons: its highest valence is 7, as in Cl₂O₇. A is false.",
    ["R: HCl → valence 1 → true", "A: Cl₂O₇ → valence 7 → highest valence is 7, not 1 → false"],
    answer="D",
    why="The valence towards hydrogen (8 − group electrons) and the highest valence towards oxygen (equal to the "
        "number of valence electrons) differ for the p-block non-metals.",
    ncert=f"{REF9}, periodic trends in chemical properties: periodicity of valence", seconds=45)

truth9a = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Valence and reactivity", A, "multi_statement",
    ms("Which of the following pairs of elements show a diagonal relationship?",
       ["Lithium and magnesium", "Beryllium and aluminium", "Boron and silicon", "Lithium and sodium",
        "Magnesium and aluminium"]),
    multi("A", truth9a, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (b) only"]),
    "Diagonal relationship of second-period elements",
    "The first members of groups 1, 2 and 13 (Li, Be, B) show many similarities with the SECOND member of the "
    "NEXT group (Mg, Al, Si), lying diagonally below and to the right. Li and Na are in the same group; Mg and "
    "Al are neighbours in the same period.",
    ["(a) Li ↘ Mg ✓", "(b) Be ↘ Al ✓", "(c) B ↘ Si ✓", "(d) same group ✗", "(e) same period ✗"],
    why="Pairs in the same group or the same period are not diagonal pairs; '(a) and (b) only' misses B and Si.",
    ncert=f"{REF9}, anomalous properties of second period elements (diagonal relationship)", seconds=40)

add("Atomic and ionic radii", A, "assertion_reason",
    ar("The Mg²⁺ ion is smaller than the Na⁺ ion.",
       "The Mg²⁺ ion has more electrons than the Na⁺ ion."),
    AR_, "Radii of isoelectronic ions",
    "Na⁺ and Mg²⁺ both have 10 electrons (they are isoelectronic), so R is false. Mg²⁺ has the greater nuclear "
    "charge (+12 against +11) acting on the same number of electrons, so it pulls them closer and is smaller: "
    "A is true.",
    ["Na⁺: 11 − 1 = 10 e⁻; Mg²⁺: 12 − 2 = 10 e⁻ → R false",
     "Same electrons, larger nuclear charge → smaller ion → A true"],
    answer="C",
    why="R is false because the two ions are isoelectronic; the size difference comes from the nuclear charge, "
        "not from the number of electrons.",
    ncert=f"{REF9}, ionic radius (isoelectronic species)", seconds=40)
