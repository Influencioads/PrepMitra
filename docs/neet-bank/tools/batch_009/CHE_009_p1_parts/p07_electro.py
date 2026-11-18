

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R = f"{C11}, 'Redox Reactions'"
REF7 = f"{C12}, 'Electrochemistry'"

x_p = -1 - 2 * 1 + 2 * 2
assert x_p == 1
add("Oxidation number and balancing", B, "numerical",
    "The oxidation number of phosphorus in barium hypophosphite, Ba(H₂PO₂)₂, is:",
    Opts("B", "+1", ["+3", "+5", "−1"]),
    "Rules for assigning oxidation numbers",
    "Ba is +2, so each H₂PO₂⁻ ion carries a charge of −1. In it, H is +1 and O is −2.",
    ["H₂PO₂⁻: 2(+1) + x + 2(−2) = −1", "2 + x − 4 = −1 → x = +1"],
    why="+3 and +5 are the oxidation numbers of P in phosphite (H₃PO₃) and phosphate. −1 treats the hydrogen "
        "atoms as hydride (−1).",
    ncert=f"{REF7R}, oxidation number", seconds=35, checked=True)

add("Electrode potential and cells", B, "direct",
    "In the cell representation Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s), the double vertical line stands for:",
    Opts("D", "a salt bridge", ["the boundary between an electrode and its solution", "the anode",
                                "the direction in which electrons flow"]),
    "Conventional representation of a galvanic cell",
    "In the cell notation, a single vertical line marks a phase boundary (metal | solution), and a double "
    "vertical line marks the salt bridge joining the two half-cells. The anode is written on the left.",
    ["| → phase boundary", "|| → salt bridge"],
    why="A phase boundary is shown by a single line; the anode and the direction of electron flow are shown by "
        "the order of writing (anode on the left), not by the double line.",
    ncert=f"{REF7}, galvanic cells: representation of a cell", seconds=20)

add("Batteries and fuel cells", B, "direct",
    "In the dry (Leclanché) cell, the ammonia produced in the cathode reaction:",
    Opts("A", "combines with Zn²⁺ ions to form the complex [Zn(NH₃)₄]²⁺",
         ["escapes as a gas through a vent in the cell", "is oxidised at the zinc anode",
          "reduces manganese dioxide to manganese metal"]),
    "Reactions in the dry cell",
    "At the cathode MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃. NCERT notes that the ammonia formed combines with the Zn²⁺ "
    "ions (produced at the anode) to give the complex [Zn(NH₃)₄]²⁺.",
    ["Anode: Zn → Zn²⁺ + 2e⁻", "Cathode: MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃",
     "NH₃ + Zn²⁺ → [Zn(NH₃)₄]²⁺"],
    why="The dry cell is sealed and the ammonia is taken up as a complex; it is not oxidised at the anode, and "
        "manganese is reduced only from +4 to +3, not to the metal.",
    ncert=f"{REF7}, batteries: primary batteries (dry cell)", seconds=30)

add("Conductance and Kohlrausch's law", B, "statement_pair",
    sp("The SI unit of conductance is the siemens (S), which is equal to Ω⁻¹.",
       "The conductivity of a solution is the reciprocal of its resistance."),
    SP_, "Conductance, resistivity and conductivity",
    "Conductance G = 1/R, measured in siemens (S = Ω⁻¹): Statement I is true. Conductivity κ is the reciprocal "
    "of RESISTIVITY (κ = 1/ρ, unit S m⁻¹), not of resistance; the reciprocal of resistance is the conductance. "
    "Statement II is false.",
    ["I: G = 1/R, unit S = Ω⁻¹ → true", "II: κ = 1/ρ (not 1/R) → false"],
    answer="C",
    why="Statement II confuses conductivity with conductance.",
    ncert=f"{REF7}, conductance of electrolytic solutions", seconds=30)

q_fc = 2 / 2 * 2 * F_CONST
assert q_fc == 193000
add("Batteries and fuel cells", B, "numerical",
    "In a hydrogen–oxygen fuel cell, the anode reaction is 2H₂(g) + 4OH⁻(aq) → 4H₂O(l) + 4e⁻. The quantity of "
    "electricity produced when 2.0 g of hydrogen is consumed is (H = 1, F = 96 500 C mol⁻¹):",
    Opts("D", "1.93 × 10⁵ C", ["9.65 × 10⁴ C", "3.86 × 10⁵ C", "4.83 × 10⁴ C"]),
    "Charge from the amount of reactant: Q = n(e⁻) × F",
    "Each H₂ molecule gives two electrons (2H₂ → 4e⁻). 2.0 g of H₂ is 1.0 mol, which gives 2.0 mol of electrons.",
    ["n(H₂) = 2.0/2 = 1.0 mol", "n(e⁻) = 2 × 1.0 = 2.0 mol", "Q = 2.0 × 96 500 = 1.93 × 10⁵ C"],
    why="9.65 × 10⁴ C takes one electron per H₂. 3.86 × 10⁵ C takes four electrons per H₂ (reading the 4e⁻ of "
        "the equation as per molecule). 4.83 × 10⁴ C takes half a mole of electrons.",
    ncert=f"{REF7}, fuel cells", seconds=40, checked=True)

add("Oxidation number and balancing", I, "direct",
    "Which of the following compounds is given an INCORRECT name in the Stock notation?",
    Opts("C", "Cr₂O₃ – chromium(II) oxide", ["MnO₂ – manganese(IV) oxide", "Hg₂Cl₂ – mercury(I) chloride",
                                             "SnCl₄ – tin(IV) chloride"]),
    "Stock notation: the oxidation number of the metal in Roman numerals",
    "Find the oxidation number of the metal in each compound: Cr₂O₃: 2x = +6 → Cr is +3, so the name should be "
    "chromium(III) oxide.",
    ["MnO₂: Mn +4 ✓", "Hg₂Cl₂: 2x = +2 → Hg +1 ✓", "SnCl₄: Sn +4 ✓", "Cr₂O₃: Cr +3, not +2 ✗"],
    why="The other three names show the correct oxidation numbers; in Hg₂Cl₂ each mercury is +1 (the Hg₂²⁺ unit).",
    ncert=f"{REF7R}, oxidation number: Stock notation", seconds=40)

e_mg = 0.80 - (-2.37) - 0.059 / 2 * math.log10(0.01 / 0.001 ** 2)
assert close(e_mg, 3.052, 0.001) and close(3.17 - 0.0295, 3.14, 0.002) and close(3.17 - 0.059 * 4, 2.93, 0.002) \
    and close(3.17 + 0.118, 3.29, 0.002)
add("Nernst equation and Gibbs energy", I, "numerical",
    "The emf at 298 K of the cell Mg(s) | Mg²⁺(0.010 M) || Ag⁺(0.0010 M) | Ag(s), whose cell reaction is "
    "Mg(s) + 2Ag⁺(aq) → Mg²⁺(aq) + 2Ag(s), is (E°(Mg²⁺/Mg) = −2.37 V, E°(Ag⁺/Ag) = +0.80 V, "
    "2.303RT/F = 0.059 V):",
    Opts("B", "3.05 V", ["3.14 V", "2.93 V", "3.29 V"]),
    "Nernst equation for a cell with unequal numbers of ions",
    "E°cell = E°(cathode) − E°(anode). The reaction quotient contains [Ag⁺]² because two Ag⁺ ions appear in the "
    "balanced equation, and n = 2.",
    ["E°cell = 0.80 − (−2.37) = 3.17 V", "Q = [Mg²⁺]/[Ag⁺]² = 0.010/(0.0010)² = 1.0 × 10⁴",
     "E = 3.17 − (0.059/2) × log 10⁴ = 3.17 − 0.118 = 3.05 V"],
    why="3.14 V forgets to square [Ag⁺] (Q = 10). 2.93 V uses n = 1. 3.29 V adds the correction term, inverting Q.",
    ncert=f"{REF7}, Nernst equation", seconds=90, checked=True)

add("Conductance and Kohlrausch's law", I, "direct",
    "Which of the following ions has the HIGHEST limiting molar conductivity in water at 298 K?",
    Opts("D", "H⁺", ["Na⁺", "K⁺", "Cl⁻"]),
    "Limiting molar conductivities of ions",
    "NCERT's table of limiting molar conductivities at 298 K shows H⁺ (349.6 S cm² mol⁻¹) far above all other "
    "ions; OH⁻ (199.1) comes next. Na⁺ (50.1), K⁺ (73.5) and Cl⁻ (76.3) are much lower.",
    ["H⁺ 349.6 > Cl⁻ 76.3 > K⁺ 73.5 > Na⁺ 50.1 (S cm² mol⁻¹)"],
    why="Na⁺, K⁺ and Cl⁻ have limiting molar conductivities between about 50 and 76 S cm² mol⁻¹.",
    ncert=f"{REF7}, variation of molar conductivity with concentration: Kohlrausch's law (table of λ°)",
    seconds=25)

add("Oxidation number and balancing", I, "assertion_reason",
    ar("In the reaction 2H₂S(g) + SO₂(g) → 3S(s) + 2H₂O(l), sulphur dioxide acts as an oxidising agent.",
       "Sulphur dioxide is a gas at room temperature."),
    AR_, "Identifying the oxidising agent from changes in oxidation number",
    "In SO₂ sulphur is +4 and it becomes 0 in S: it is reduced, so SO₂ is the oxidising agent (H₂S, with S at "
    "−2 going to 0, is the reducing agent). A is true. R is true as well, but being a gas has nothing to do with "
    "the change in oxidation number.",
    ["S in SO₂: +4 → 0 (reduced) → SO₂ is the oxidising agent → A true",
     "SO₂ is a gas at 298 K → R true", "Physical state does not decide the redox role → option B"],
    answer="B",
    why="R is a true property of SO₂ but plainly unrelated to why it oxidises H₂S.",
    ncert=f"{REF7R}, oxidising and reducing agents (oxidation number concept)", seconds=40)

add("Nernst equation and Gibbs energy", I, "match_list",
    lists("Match List-I (quantity for a cell reaction in which n electrons are transferred) with List-II (its "
          "expression). (K = equilibrium constant, Q = reaction quotient; 2.303RT/F = 0.059 V at 298 K)",
          ["Standard Gibbs energy change, ΔrG°", "Standard emf, E°cell, at 298 K",
           "Emf, E_cell, at 298 K", "Gibbs energy change under the actual conditions, ΔrG"],
          ["−nF E_cell", "E°cell − (0.059/n) log Q", "−nF E°cell", "(0.059/n) log K"]),
    match("C", M("III IV II I"), [M("III II IV I"), M("I IV II III"), M("IV III II I")]),
    "Relations between emf, Gibbs energy and the equilibrium constant",
    "ΔrG° = −nFE°cell and ΔrG = −nFE_cell. Combining ΔrG° = −2.303RT log K with the first gives "
    "E°cell = (0.059/n) log K at 298 K. The Nernst equation gives E_cell = E°cell − (0.059/n) log Q.",
    ["A → III", "B → IV", "C → II", "D → I"],
    why="The wrong codes swap the standard and actual quantities, or the Nernst equation with the E°–K relation.",
    ncert=f"{REF7}, Nernst equation; equilibrium constant from Nernst equation; electrochemical cell and "
          f"Gibbs energy of the reaction", seconds=50)

truth7 = {"a": False, "b": False, "c": True, "d": True, "e": True}
add("Electrode potential and cells", I, "multi_statement",
    ms("Which of the following statements about galvanic cells are correct?",
       ["The anode of a galvanic cell is its positive electrode.",
        "Electrons flow through the salt bridge from one half-cell to the other.",
        "E°cell = E°(cathode) − E°(anode), using standard reduction potentials.",
        "In a working Daniell cell, the zinc electrode loses mass.",
        "If an external opposing potential greater than 1.1 V is applied to a Daniell cell, zinc is deposited on "
        "the zinc electrode and copper dissolves."]),
    multi("D", truth7, ["(a), (c) and (d) only", "(b), (c) and (e) only", "(c) and (d) only"]),
    "Working of a galvanic cell",
    "Oxidation occurs at the anode, which releases electrons into the external circuit and is the NEGATIVE "
    "electrode. Electrons flow only through the external wire; the salt bridge carries ions. In the Daniell cell "
    "Zn is oxidised to Zn²⁺, so the zinc rod loses mass. When an external potential larger than 1.1 V opposes "
    "the cell, the reaction reverses: the cell works as an electrolytic cell, zinc is deposited and copper "
    "dissolves.",
    ["(a) ✗ anode is negative", "(b) ✗ ions, not electrons, move in the salt bridge", "(c) ✓", "(d) ✓", "(e) ✓"],
    why="(a) and (b) are false; '(c) and (d) only' misses the NCERT description of the reversed cell in (e).",
    ncert=f"{REF7}, electrochemical cells; galvanic cells", seconds=60)

ph_a1 = (0.517 - 0.34) / 0.059
assert close(ph_a1, 3.0) and close((0.517 - 0.34) / 0.0295, 6.0) and close((0.517 - 0.34) / 0.118, 1.5) and close(0.517 / 0.059, 8.76)
add("Nernst equation and Gibbs energy", A, "numerical",
    "The emf of the cell Pt | H₂(g, 1 bar) | H⁺(aq) || Cu²⁺(aq, 1 M) | Cu(s) at 298 K is 0.517 V. The cell "
    "reaction is H₂(g) + Cu²⁺(aq) → 2H⁺(aq) + Cu(s). The pH of the solution in the hydrogen half-cell is "
    "(E°(Cu²⁺/Cu) = +0.34 V, 2.303RT/F = 0.059 V):",
    Opts("B", "3.0", ["6.0", "1.5", "8.8"]),
    "Nernst equation used to find pH",
    "Apply the Nernst equation to the whole cell with n = 2. Since [H⁺]² appears in Q, the log term becomes "
    "−2 × 0.059/2 × log[H⁺] = 0.059 pH.",
    ["E°cell = 0.34 − 0 = 0.34 V", "E = 0.34 − (0.059/2) log([H⁺]²/[Cu²⁺]) = 0.34 + 0.059 pH",
     "0.517 = 0.34 + 0.059 pH → pH = 0.177/0.059 = 3.0"],
    why="6.0 forgets the square on [H⁺] (uses 0.0295 per pH unit). 1.5 doubles the coefficient (0.118 per pH "
        "unit). 8.8 ignores E° of the copper electrode and "
        "takes E = 0.059 pH.",
    ncert=f"{REF7}, Nernst equation", seconds=120, checked=True)

w_max = 6.54 / 65.4 * 2 * F_CONST * 1.10 / 1000
assert close(w_max, 21.23, 0.001) and close(w_max / 2, 10.6, 0.002) and close(2 * F_CONST * 1.10 / 1000, 212.3)
add("Nernst equation and Gibbs energy", A, "numerical",
    "The standard emf of the Daniell cell is 1.10 V. The maximum electrical work that can be obtained when "
    "6.54 g of zinc is used up in the cell under standard conditions is (Zn = 65.4, F = 96 500 C mol⁻¹):",
    Opts("C", "21.2 kJ", ["10.6 kJ", "212 kJ", "2.12 kJ"]),
    "Maximum electrical work = −ΔG = nFE",
    "For Zn + Cu²⁺ → Zn²⁺ + Cu, n = 2 per mole of zinc. Scale the work per mole to the amount of zinc used.",
    ["n(Zn) = 6.54/65.4 = 0.100 mol", "Charge = 0.100 × 2 × 96 500 = 19 300 C",
     "Work = 19 300 × 1.10 = 21 230 J ≈ 21.2 kJ"],
    why="10.6 kJ uses one electron per Zn atom. 212 kJ is the work per mole of zinc (the 0.1 mol is ignored). "
        "2.12 kJ is a slip of a power of ten.",
    ncert=f"{REF7}, electrochemical cell and Gibbs energy of the reaction", seconds=70, checked=True)

e7 = {"Cl2": 1.36, "Br2": 1.09, "Fe3": 0.77, "I2": 0.54}
truth7a = {"a": e7["Cl2"] > e7["Br2"], "b": e7["Br2"] > e7["I2"], "c": e7["I2"] > e7["Fe3"],
           "d": e7["Fe3"] > e7["Br2"], "e": e7["Br2"] > e7["Fe3"]}
assert truth7a == {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Electrode potential and cells", A, "multi_statement",
    ms("The standard reduction potentials at 298 K are: Cl₂/Cl⁻ +1.36 V, Br₂/Br⁻ +1.09 V, Fe³⁺/Fe²⁺ +0.77 V "
       "and I₂/I⁻ +0.54 V. Which of the following reactions are feasible under standard conditions?",
       ["Cl₂ oxidises Br⁻ to Br₂.", "Br₂ oxidises I⁻ to I₂.", "I₂ oxidises Fe²⁺ to Fe³⁺.",
        "Fe³⁺ oxidises Br⁻ to Br₂.", "Br₂ oxidises Fe²⁺ to Fe³⁺."]),
    multi("A", truth7a, ["(a), (b), (c) and (e) only", "(a), (d) and (e) only", "(b) and (e) only"]),
    "Using the electrochemical series to predict redox reactions",
    "A species can oxidise the reduced form of any couple with a LOWER reduction potential (E°cell > 0).",
    ["(a) 1.36 > 1.09 → feasible ✓", "(b) 1.09 > 0.54 ✓", "(c) 0.54 < 0.77 → not feasible ✗",
     "(d) 0.77 < 1.09 ✗", "(e) 1.09 > 0.77 ✓"],
    why="(c) and (d) would need the oxidant to have the higher reduction potential, which it does not; "
        "'(b) and (e) only' misses (a).",
    ncert=f"{REF7}, electrode potential: the electrochemical series", seconds=70, checked=True)

cr_ox = 0 + 2 + 2 * 2
s_ox = 0 - 2 * 1 + 3 * 2 + 2 * 1
assert cr_ox == 6 and s_ox == 6
add("Oxidation number and balancing", A, "statement_pair",
    sp("In CrO₅, which contains one oxide oxygen atom and two peroxide (–O–O–) groups, chromium has the "
       "oxidation number +6.",
       "In peroxomonosulphuric acid, H₂SO₅, which contains one peroxide (–O–O–) group, sulphur has the "
       "oxidation number +8."),
    SP_, "Oxidation numbers in compounds containing peroxide linkages",
    "Peroxide oxygen is −1. CrO₅: x + (−2) + 4(−1) = 0 → x = +6, so Statement I is true. H₂SO₅ has two "
    "peroxide O atoms (−1 each) and three ordinary O atoms (−2 each): 2(+1) + x + 3(−2) + 2(−1) = 0 → x = +6, "
    "not +8. Statement II is false.",
    ["I: x − 2 − 4 = 0 → +6 → true", "II: 2 + x − 6 − 2 = 0 → +6 → false"],
    answer="C",
    why="+8 is obtained for H₂SO₅ only if all five O atoms are wrongly taken as −2; sulphur cannot exceed its "
        "group oxidation state of +6.",
    ncert=f"{REF7R}, oxidation number", seconds=60, checked=True)
