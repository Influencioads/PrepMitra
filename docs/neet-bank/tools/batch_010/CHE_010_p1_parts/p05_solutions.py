

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

solute = 100 * 0.10 + 50 * 0.40
pct = solute / 150 * 100
assert close(pct, 20) and close((10 + 40) / 2, 25) and close(solute, 30)
add("Concentration terms", B, "numerical",
    "100 g of a 10% (by mass) aqueous solution of a salt is mixed with 50 g of a 40% (by mass) aqueous solution "
    "of the same salt. The mass percentage of the salt in the resulting solution is:",
    Opts("D", "20%", ["25%", "50%", "30%"]),
    "Mass percentage = (mass of solute ÷ total mass of solution) × 100",
    "Add the masses of salt from both solutions and divide by the total mass of the mixture.",
    ["Salt from first solution = 10% of 100 g = 10 g", "Salt from second solution = 40% of 50 g = 20 g",
     "Total salt = 30 g in 150 g of solution", "Mass % = 30/150 × 100 = 20%"],
    why="25% is the simple average of 10% and 40%, which ignores the different masses mixed. 50% adds the two "
        "percentages. 30% takes the 30 g of salt per 100 g, forgetting that the mixture weighs 150 g.",
    ncert=f"{REF5}, expressing concentration of solutions (mass percentage)", seconds=40, checked=True)

add("Raoult's law and ideal solutions", B, "statement_pair",
    sp("According to Raoult's law, for a solution of two volatile liquids the partial vapour pressure of each "
       "component is directly proportional to its mole fraction in the solution.",
       "According to Dalton's law of partial pressures, the total vapour pressure over such a solution is the "
       "sum of the partial vapour pressures of the components."),
    SP_, "Vapour pressure of a solution of two volatile liquids",
    "Raoult's law: p₁ = p₁° x₁ and p₂ = p₂° x₂. Dalton's law of partial pressures: p_total = p₁ + p₂. Together "
    "they give p_total = p₁° x₁ + p₂° x₂ for an ideal solution.",
    ["I: p_i ∝ x_i (Raoult's law) → true", "II: p_total = p₁ + p₂ (Dalton's law) → true"],
    answer="A",
    why="Both statements are used together in NCERT to derive the total vapour pressure of an ideal solution.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions", seconds=30)

add("Colligative properties", B, "assertion_reason",
    ar("Osmotic pressure of a dilute solution is a colligative property.",
       "The osmotic pressure of a solution can be measured at around room temperature."),
    AR_, "Osmotic pressure: a colligative property; why it suits biomolecules",
    "A is true: π = CRT depends only on the molar concentration of solute particles, not on what they are. R is "
    "also true: NCERT notes that osmotic pressure is measured at about room temperature, which is why the method "
    "suits heat-sensitive biomolecules. But the temperature at which it can be measured has nothing to do with "
    "why it depends only on the number of particles.",
    ["A: π = CRT → depends on the number of particles → true",
     "R: measured near room temperature → true (an advantage of the method)",
     "R is a practical advantage, not the reason π is colligative → option B"],
    answer="B",
    why="R explains why the osmotic-pressure method is preferred for proteins, not why osmotic pressure is a "
        "colligative property, so option A does not apply.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=40)

n_b, n_t = 39 / 78, 46 / 92
p_tot = n_b / (n_b + n_t) * 75 + n_t / (n_b + n_t) * 22
w_b = 39 / 85
assert close(p_tot, 48.5) and close(w_b * 75 + (1 - w_b) * 22, 46.3, 0.002) and close(0.5 * 75, 37.5)
add("Raoult's law and ideal solutions", I, "numerical",
    "39 g of benzene (C₆H₆) is mixed with 46 g of toluene (C₇H₈), and the two form an ideal solution. At the "
    "temperature of the experiment the vapour pressures of pure benzene and pure toluene are 75 mm Hg and "
    "22 mm Hg. The total vapour pressure of the solution is (C = 12, H = 1):",
    Opts("C", "48.5 mm Hg", ["97.0 mm Hg", "46.3 mm Hg", "37.5 mm Hg"]),
    "Raoult's law for two volatile liquids: p_total = x_A p_A° + x_B p_B°",
    "Convert the masses to moles, find the mole fractions, and add the two partial pressures.",
    ["n(benzene) = 39/78 = 0.50 mol; n(toluene) = 46/92 = 0.50 mol", "x(benzene) = x(toluene) = 0.50",
     "p_total = 0.50 × 75 + 0.50 × 22 = 37.5 + 11.0 = 48.5 mm Hg"],
    why="97.0 mm Hg adds the two pure-liquid vapour pressures without the mole fractions. 46.3 mm Hg uses mass "
        "fractions instead of mole fractions. 37.5 mm Hg is only the partial pressure of benzene.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions (Raoult's law)", seconds=60, checked=True)

add("Concentration terms", I, "assertion_reason",
    ar("The molarity and the molality of any aqueous solution are always numerically equal.",
       "Molarity is the number of moles of solute per litre of solution, whereas molality is the number of "
       "moles of solute per kilogram of solvent."),
    AR_, "Molarity versus molality",
    "R is the correct pair of definitions. Because one is per litre of SOLUTION and the other per kilogram of "
    "SOLVENT, the two are generally different (for example 2.0 M NaOH of density 1.12 g mL⁻¹ is about 1.9 m). "
    "They are close only for very dilute aqueous solutions. So A is false.",
    ["A: different bases (litre of solution vs kg of solvent) → not always equal → false",
     "R: correct definitions → true"],
    answer="D",
    why="A would need the volume of solution in litres always to equal the mass of solvent in kilograms, which "
        "is true only approximately for very dilute aqueous solutions.",
    ncert=f"{REF5}, expressing concentration of solutions (molarity, molality)", seconds=35)

pis = {"A": 0.1 * 1 * 0.082 * 300, "B": 0.1 * 2 * 0.082 * 300, "C": 0.1 * 3 * 0.082 * 300,
       "D": 0.05 * 1 * 0.082 * 300}
assert all(close(pis[k], v) for k, v in {"A": 2.46, "B": 4.92, "C": 7.38, "D": 1.23}.items())
add("van't Hoff factor", I, "match_list",
    lists("Match List-I (aqueous solution at 300 K, electrolytes completely dissociated) with List-II (its "
          "osmotic pressure). (R = 0.082 L atm K⁻¹ mol⁻¹)",
          ["0.10 M urea", "0.10 M NaCl", "0.10 M CaCl₂", "0.05 M glucose"],
          ["7.38 atm", "1.23 atm", "4.92 atm", "2.46 atm"]),
    match("B", M("IV III I II"), [M("IV I III II"), M("II III I IV"), M("IV III II I")]),
    "Osmotic pressure with the van't Hoff factor: π = iCRT",
    "CRT = 0.10 × 0.082 × 300 = 2.46 atm for a 0.10 M solution of a non-electrolyte. Multiply by i for "
    "electrolytes.",
    ["A: i = 1 → 2.46 atm → IV", "B: NaCl → 2 ions → 4.92 atm → III", "C: CaCl₂ → 3 ions → 7.38 atm → I",
     "D: 0.05 × 0.082 × 300 = 1.23 atm → II"],
    why="B-I/C-III swaps NaCl and CaCl₂ (wrong numbers of ions). A-II/D-IV ignores the factor of two between "
        "0.10 M and 0.05 M. C-II/D-I gives glucose the CaCl₂ value.",
    ncert=f"{REF5}, osmosis and osmotic pressure; abnormal molar masses", seconds=70, checked=True)

truth_t = {"a": True, "b": True, "c": False, "d": True, "e": False}
add("Concentration terms", I, "multi_statement",
    ms("Which of the following ways of expressing the concentration of a solution do NOT change when the "
       "temperature of the solution changes?",
       ["Mass percentage (w/w)", "Parts per million by mass", "Molarity", "Molality",
        "Mass by volume percentage (w/V)"]),
    multi("A", truth_t, ["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a) and (d) only"]),
    "Temperature dependence of concentration terms",
    "Volume changes with temperature, masses do not. Terms based only on masses (or amounts) are independent "
    "of temperature; terms that use the volume of the solution change with temperature.",
    ["(a) mass/mass → independent ✓", "(b) ppm by mass → mass/mass → independent ✓",
     "(c) molarity → mol per litre of solution → changes ✗", "(d) molality → mol per kg of solvent → independent ✓",
     "(e) w/V → uses volume → changes ✗"],
    why="Molarity and mass-by-volume percentage both contain the volume of the solution, which expands on "
        "warming; '(a) and (d) only' leaves out ppm by mass, which is also mass-based.",
    ncert=f"{REF5}, expressing concentration of solutions", seconds=50)

i_obs = 0.2232 / (1.86 * 0.1)
alpha = i_obs - 1
ka = 0.1 * alpha ** 2 / (1 - alpha)
assert close(i_obs, 1.2) and close(alpha, 0.2) and close(ka, 5.0e-3) and close(0.1 * alpha ** 2, 4.0e-3) \
    and close(0.1 * alpha, 2.0e-2) and close(0.1 * 0.1 ** 2 / 0.9, 1.1e-3, 0.02)
add("van't Hoff factor", A, "numerical",
    "A 0.10 m aqueous solution of a weak monobasic acid HA (HA ⇌ H⁺ + A⁻) freezes at −0.2232 °C. Taking the "
    "molarity of this dilute solution to be equal to its molality, the dissociation constant Kₐ of the acid is "
    "(K_f of water = 1.86 K kg mol⁻¹; freezing point of water = 0 °C):",
    Opts("B", "5.0 × 10⁻³", ["4.0 × 10⁻³", "2.0 × 10⁻²", "1.1 × 10⁻³"]),
    "van't Hoff factor from a colligative property, then the degree of dissociation and Kₐ",
    "From ΔT_f = i K_f m find i. For HA ⇌ H⁺ + A⁻, i = 1 + α. Then Kₐ = cα²/(1 − α).",
    ["i = ΔT_f/(K_f m) = 0.2232/(1.86 × 0.10) = 1.2", "α = i − 1 = 0.20",
     "Kₐ = cα²/(1 − α) = 0.10 × 0.04/0.80 = 5.0 × 10⁻³"],
    why="4.0 × 10⁻³ uses Kₐ ≈ cα², which is not valid when α = 0.2. 2.0 × 10⁻² takes Kₐ = cα. 1.1 × 10⁻³ "
        "divides (i − 1) by 2, as if each HA gave three particles.",
    ncert=f"{REF5}, abnormal molar masses (van't Hoff factor)", seconds=110, checked=True)

i_dimer = 1 - 0.5 + 0.5 / 2
i_ab = 1 + 0.5
assert close(1 / i_dimer, 4 / 3) and close(1 / i_ab, 2 / 3)
add("van't Hoff factor", A, "statement_pair",
    sp("If 50% of the molecules of a solute X dimerise in solution (2X ⇌ X₂), the molar mass of X found from a "
       "colligative property is twice its true molar mass.",
       "If a salt AB is 50% dissociated into A⁺ and B⁻ in solution, the molar mass found from a colligative "
       "property is two-thirds of its true molar mass."),
    SP_, "van't Hoff factor and abnormal molar masses",
    "Observed molar mass = true molar mass ÷ i. For 50% dimerisation, i = (1 − 0.5) + 0.5/2 = 0.75, so the "
    "observed value is 4/3 of the true one (twice the true value needs COMPLETE dimerisation, i = 0.5). For AB "
    "50% dissociated, i = 1 + 0.5 = 1.5, so the observed value is 1/1.5 = 2/3 of the true one.",
    ["I: i = 0.75 → M_obs = M/0.75 = 1.33 M, not 2M → false",
     "II: i = 1.5 → M_obs = M/1.5 = 0.67 M → true"],
    answer="D",
    why="Statement I applies the result for complete association to a solute that is only half associated.",
    ncert=f"{REF5}, abnormal molar masses", seconds=70, checked=True)

particles = {"right": (0.10 * 3, 0.15 * 2), "w1": (0.10 * 2, 0.10 * 1), "w2": (0.10 * 3, 0.20 * 2),
             "w3": (0.05 * 3, 0.10 * 1)}
assert [k for k, (x, y) in particles.items() if close(x, y)] == ["right"]
add("Colligative properties", A, "direct",
    "Assuming complete dissociation of the electrolytes, which of the following pairs of aqueous solutions are "
    "ISOTONIC with each other at the same temperature?",
    Opts("C", "0.10 M Na₂SO₄ and 0.15 M KCl",
         ["0.10 M NaCl and 0.10 M glucose", "0.10 M CaCl₂ and 0.20 M NaCl", "0.05 M K₂SO₄ and 0.10 M urea"]),
    "Isotonic solutions have equal osmotic pressure, i.e. equal iC at the same temperature",
    "Compare the total molar concentration of solute particles, iC, for each pair.",
    ["Na₂SO₄: 3 × 0.10 = 0.30 M; KCl: 2 × 0.15 = 0.30 M → equal ✓",
     "NaCl 0.20 M vs glucose 0.10 M", "CaCl₂ 0.30 M vs NaCl 0.40 M", "K₂SO₄ 0.15 M vs urea 0.10 M"],
    why="Each of the other pairs has unequal particle concentrations; they look equal only if the van't Hoff "
        "factor is ignored or applied to one solution of the pair only.",
    ncert=f"{REF5}, osmosis and osmotic pressure (isotonic solutions)", seconds=60, checked=True)
