

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

assert close(0.9 / 100 * 500, 4.5)
add("Concentration terms", B, "numerical",
    "A saline solution used in medicine is 0.9% (mass by volume) sodium chloride. The mass of NaCl present in "
    "500 mL of this solution is:",
    Opts("B", "4.5 g", ["0.18 g", "45 g", "9.0 g"]),
    "Mass by volume percentage (w/V)",
    "0.9% (w/V) means 0.9 g of solute in every 100 mL of solution.",
    ["0.9 g per 100 mL", "500 mL → 0.9 × 500/100 = 4.5 g"],
    why="0.18 g divides 0.9 by 5 instead of multiplying. 45 g reads 0.9% as 9 g per 100 mL. 9.0 g treats the "
        "percentage as grams per 50 mL.",
    ncert=f"{REF5}, expressing concentration of solutions: mass by volume percentage", seconds=25, checked=True)

ratio_tf = (1 / 60) / (1 / 180)
assert close(ratio_tf, 3)
add("Colligative properties", B, "numerical",
    "Equal masses of urea (molar mass 60 g mol⁻¹) and glucose (molar mass 180 g mol⁻¹) are dissolved "
    "separately in equal masses of water. The ratio of the depression of freezing point of the urea solution "
    "to that of the glucose solution is:",
    Opts("C", "3 : 1", ["1 : 3", "1 : 1", "9 : 1"]),
    "Depression of freezing point is proportional to molality, ΔTf = K_f m",
    "For the same mass of solute and solvent, molality is inversely proportional to the molar mass of the "
    "solute; both are non-electrolytes, so the ratio of ΔTf is the ratio of molalities.",
    ["m ∝ 1/M", "ΔTf(urea)/ΔTf(glucose) = M(glucose)/M(urea) = 180/60 = 3"],
    why="1 : 3 inverts the ratio. 1 : 1 assumes equal masses give equal effects, ignoring that colligative "
        "properties depend on the number of particles. 9 : 1 squares the ratio.",
    ncert=f"{REF5}, depression of freezing point", seconds=30, checked=True)

add("Colligative properties", B, "assertion_reason",
    ar("Salting of meat helps to preserve it from bacterial decay.",
       "A bacterium on salted meat loses water through osmosis, shrivels and dies."),
    AR_, "Osmosis in everyday life",
    "NCERT explains that preservation of meat by salting (and of fruits by adding sugar) protects them against "
    "bacterial action: a bacterium on salted meat or candied fruit loses water by osmosis to the concentrated "
    "surroundings, shrivels and dies. R is the reason for A.",
    ["A: salted meat resists bacterial decay → true",
     "R: water moves out of the bacterium into the more concentrated salt → it dies → true and explains A"],
    answer="A",
    why="Both statements are true, and the osmotic loss of water from bacteria is exactly why salting preserves "
        "meat.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=30)

add("Concentration terms", B, "match_list",
    lists("Match List-I (concentration term) with List-II (its definition).",
          ["Mass percentage (w/w)", "Volume percentage (V/V)", "Mass by volume percentage (w/V)", "Molality"],
          ["(Volume of the component ÷ total volume of the solution) × 100",
           "(Mass of the component ÷ total mass of the solution) × 100",
           "Moles of solute ÷ mass of solvent in kilograms",
           "(Mass of solute in grams ÷ volume of the solution in mL) × 100"]),
    match("D", M("II I IV III"), [M("I II IV III"), M("II I III IV"), M("IV I II III")]),
    "Ways of expressing the concentration of a solution",
    "w/w compares masses; V/V compares volumes; w/V gives grams of solute per 100 mL of solution; molality is "
    "moles of solute per kilogram of solvent.",
    ["A → II", "B → I", "C → IV", "D → III"],
    why="The wrong codes interchange the mass and volume percentages, or w/V with molality, or w/V with w/w.",
    ncert=f"{REF5}, expressing concentration of solutions", seconds=30)

pi_k2so4 = 3 * 0.1 * 0.082 * 300
assert close(pi_k2so4, 7.38) and close(pi_k2so4 / 3, 2.46) and close(pi_k2so4 * 2 / 3, 4.92) \
    and close(pi_k2so4 * 4 / 3, 9.84)
add("van't Hoff factor", I, "numerical",
    "The osmotic pressure at 300 K of a 0.10 M aqueous solution of potassium sulphate, assuming complete "
    "dissociation, is (R = 0.082 L atm K⁻¹ mol⁻¹):",
    Opts("C", "7.38 atm", ["2.46 atm", "4.92 atm", "9.84 atm"]),
    "Osmotic pressure of an electrolyte solution, π = iCRT",
    "K₂SO₄ → 2K⁺ + SO₄²⁻ gives three ions per formula unit, so i = 3.",
    ["i = 3", "π = 3 × 0.10 × 0.082 × 300", "π = 7.38 atm"],
    why="2.46 atm ignores dissociation (i = 1). 4.92 atm takes i = 2, counting K₂ as one particle. 9.84 atm takes "
        "i = 4.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=45, checked=True)

x_hcl = 1 / (1 + 63.5 / 18)
assert close(x_hcl, 0.221) and close(1 / (63.5 / 18), 0.2835) and close(36.5 / 63.5, 0.575)
add("Concentration terms", I, "numerical",
    "Concentrated hydrochloric acid is 36.5% HCl by mass. The mole fraction of HCl in it is (H = 1, Cl = 35.5, "
    "O = 16):",
    Opts("B", "0.221", ["0.365", "0.283", "0.575"]),
    "Converting mass percentage into mole fraction",
    "Take 100 g of solution: 36.5 g is HCl and the rest is water. Convert both to moles; the mole fraction is the "
    "moles of HCl divided by the total moles.",
    ["n(HCl) = 36.5/36.5 = 1.00 mol", "n(H₂O) = 63.5/18 = 3.53 mol", "x(HCl) = 1.00/(1.00 + 3.53) = 0.221"],
    why="0.365 is the mass fraction, not the mole fraction. 0.283 divides by the moles of water only (a mole "
        "ratio). 0.575 is the ratio of the masses of HCl and water.",
    ncert=f"{REF5}, expressing concentration of solutions: mole fraction", seconds=50, checked=True)

truth5 = {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Colligative properties", I, "multi_statement",
    ms("Which of the following statements about osmosis are correct?",
       ["Wilted flowers revive when they are placed in fresh water.",
        "People who take a lot of salt may experience water retention in tissue cells and intercellular spaces, "
        "with puffiness or swelling (oedema).",
        "In the osmotic pressure method of finding molar masses, the molality of the solution is used.",
        "In osmosis, solvent molecules move from the more concentrated solution into the more dilute one.",
        "Compared with the other colligative properties, osmotic pressure has a large magnitude even for very "
        "dilute solutions."]),
    multi("D", truth5, ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a) and (d) only"]),
    "Osmosis in everyday life; the osmotic pressure method",
    "Water enters the cells of wilted flowers by osmosis, and excess salt in the body draws water into the "
    "tissues (oedema). The osmotic pressure method uses MOLARITY (π = CRT) and is measured near room "
    "temperature; its magnitude is large even for dilute solutions, which makes it suitable for macromolecules. "
    "In osmosis the solvent moves from the dilute side (or pure solvent) into the more concentrated solution.",
    ["(a) ✓", "(b) ✓", "(c) ✗ molarity, not molality", "(d) ✗ direction reversed", "(e) ✓"],
    why="(c) and (d) are false; every option containing either of them is wrong.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=60)

add("Colligative properties", I, "assertion_reason",
    ar("A 0.1 m aqueous solution of sucrose and a 0.1 m aqueous solution of urea (both non-volatile "
       "non-electrolytes) show the same depression of freezing point.",
       "A sucrose molecule (C₁₂H₂₂O₁₁) contains many more atoms than a urea molecule (CO(NH₂)₂)."),
    AR_, "Colligative properties depend on the number of solute particles, not on their nature",
    "ΔTf = K_f m for a non-electrolyte. Both solutions have the same molality and neither solute dissociates or "
    "associates, so both contain the same number of solute particles per kilogram of water and show the same "
    "ΔTf: A is true. R is also true, but the size or composition of the solute molecule plays no part in a "
    "colligative property, so R does not explain A.",
    ["A: same m, i = 1 for both → same ΔTf = 1.86 × 0.1 = 0.186 K → true",
     "R: C₁₂H₂₂O₁₁ has 45 atoms, CO(NH₂)₂ has 8 → true",
     "ΔTf does not depend on the nature of the solute particles → R is unrelated → option B"],
    answer="B",
    why="R is a true statement about the two molecules, but colligative properties depend only on the number of "
        "solute particles, so R cannot be the explanation of A (if anything it would wrongly suggest a "
        "difference).",
    ncert=f"{REF5}, colligative properties and determination of molar mass", seconds=40)

add("Raoult's law and ideal solutions", I, "statement_pair",
    sp("The components of an azeotropic mixture can be separated completely by fractional distillation.",
       "For a solution showing positive deviation from Raoult's law, the total vapour pressure at every "
       "composition lies above the straight line expected for an ideal solution."),
    SP_, "Azeotropes and vapour pressure–composition plots of non-ideal solutions",
    "Azeotropes boil at a constant temperature and the liquid and vapour have the same composition, so they "
    "cannot be separated by fractional distillation: Statement I is false. In a positive deviation the A–B "
    "attractions are weaker than A–A and B–B, molecules escape more easily, and the vapour pressure is higher "
    "than predicted by Raoult's law: Statement II is true.",
    ["I: azeotrope → same composition in liquid and vapour → cannot be separated → false",
     "II: positive deviation → vapour pressure above the ideal line → true"],
    answer="D",
    why="Statement I contradicts the definition of an azeotrope; Statement II is the meaning of a positive "
        "deviation.",
    ncert=f"{REF5}, non-ideal solutions; azeotropes", seconds=40)

kb_w = R_J * 18 * 373 ** 2 / (1000 * 40660)
assert close(kb_w, 0.512) and close(kb_w * 1000, 512) and close(R_J * 18 * 100 ** 2 / (1000 * 40660), 0.0368) \
    and close(R_J * 18 * 373 / (1000 * 40660), 1.373e-3)
add("Colligative properties", A, "numerical",
    "The molal elevation constant of a solvent is given by K_b = R M₁ T_b² / (1000 Δ_vapH), where M₁ is the "
    "molar mass of the solvent in g mol⁻¹, T_b its boiling point in kelvin and Δ_vapH its molar enthalpy of "
    "vaporisation in J mol⁻¹. For water, T_b = 373 K and Δ_vapH = 40.66 kJ mol⁻¹. K_b of water is "
    "(R = 8.314 J K⁻¹ mol⁻¹, M₁ = 18 g mol⁻¹):",
    Opts("A", "0.512 K kg mol⁻¹", ["512 K kg mol⁻¹", "0.0368 K kg mol⁻¹", "1.37 × 10⁻³ K kg mol⁻¹"]),
    "Ebullioscopic constant from the properties of the solvent",
    "Substitute the data with Δ_vapH in J mol⁻¹ and T_b in kelvin, squaring T_b.",
    ["Numerator: 8.314 × 18 × 373² = 8.314 × 18 × 139 129 = 2.082 × 10⁷",
     "Denominator: 1000 × 40 660 = 4.066 × 10⁷", "K_b = 0.512 K kg mol⁻¹"],
    why="512 leaves out the factor 1000 in the denominator. 0.0368 uses 100 (the temperature in °C) for T_b. "
        "1.37 × 10⁻³ forgets to square T_b.",
    ncert=f"{REF5}, elevation of boiling point", seconds=90, checked=True)

dtf_mix = 1.86 * (0.01 * 2 + 0.01 * 3)
assert close(dtf_mix, 0.093) and close(1.86 * 0.02, 0.0372) and close(1.86 * 0.04, 0.0744) \
    and close(1.86 * 0.03, 0.0558)
add("van't Hoff factor", A, "numerical",
    "0.010 mol of NaCl and 0.010 mol of CaCl₂ are dissolved together in 1.0 kg of water. Assuming complete "
    "dissociation of both salts, the depression of the freezing point of the solution is (K_f of water = "
    "1.86 K kg mol⁻¹):",
    Opts("D", "0.093 K", ["0.0372 K", "0.0744 K", "0.0558 K"]),
    "Colligative properties depend on the total molality of solute particles",
    "Add up the particles: NaCl gives 2 ions and CaCl₂ gives 3 ions per formula unit. The total particle "
    "molality fixes ΔTf.",
    ["Particles from NaCl: 2 × 0.010 = 0.020 mol", "Particles from CaCl₂: 3 × 0.010 = 0.030 mol",
     "Total = 0.050 mol in 1.0 kg → 0.050 mol kg⁻¹", "ΔTf = 1.86 × 0.050 = 0.093 K"],
    why="0.0372 K ignores dissociation. 0.0744 K takes i = 2 for both salts. 0.0558 K counts only the ions "
        "from CaCl₂ and leaves out the NaCl.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=70, checked=True)

m_sol = 0.93 / 1.86
pi_sol = m_sol * 0.0821 * 300
assert close(m_sol, 0.5) and close(pi_sol, 12.3, 0.01) and close(m_sol * 0.0821 * 27, 1.108) \
    and close(2 * pi_sol, 24.6, 0.01)
add("Colligative properties", A, "numerical",
    "A dilute aqueous solution of a non-volatile non-electrolyte freezes at −0.93 °C. Taking its molarity to be "
    "equal to its molality, its osmotic pressure at 27 °C is (K_f of water = 1.86 K kg mol⁻¹, "
    "R = 0.0821 L atm K⁻¹ mol⁻¹; freezing point of water = 0 °C):",
    Opts("B", "12.3 atm", ["1.11 atm", "24.6 atm", "6.16 atm"]),
    "Linking two colligative properties through the concentration",
    "Find the molality from ΔTf, take it as the molarity C, and use π = CRT with T in kelvin.",
    ["m = ΔTf/K_f = 0.93/1.86 = 0.50 mol kg⁻¹ ≈ 0.50 mol L⁻¹", "T = 27 + 273 = 300 K",
     "π = 0.50 × 0.0821 × 300 = 12.3 atm"],
    why="1.11 atm uses 27 (°C) for T. 24.6 atm doubles the concentration as if the solute dissociated into two "
        "particles. 6.16 atm halves it.",
    ncert=f"{REF5}, depression of freezing point; osmotic pressure", seconds=80, checked=True)

i_vals = {"AB": 1 + 0.5 * 1, "AB₂": 1 + 0.5 * 2, "dimer": 1 - 0.5 / 2, "AB₃": 1 + 0.5 * 3}
assert i_vals == {"AB": 1.5, "AB₂": 2.0, "dimer": 0.75, "AB₃": 2.5}
add("van't Hoff factor", A, "match_list",
    lists("Match List-I (behaviour of the solute in a dilute solution) with List-II (van't Hoff factor, i).",
          ["A salt AB that is 50% dissociated into A⁺ and B⁻",
           "A salt AB₂ that is 50% dissociated into A²⁺ and 2B⁻",
           "A solute X of which 50% of the molecules have dimerised (2X ⇌ X₂)",
           "A salt AB₃ that is 50% dissociated into A³⁺ and 3B⁻"],
          ["2.0", "0.75", "2.5", "1.5"]),
    match("A", M("IV I II III"), [M("I IV II III"), M("IV III II I"), M("IV I III II")]),
    "van't Hoff factor for partial dissociation and association",
    "For dissociation into n particles with degree α: i = 1 + (n − 1)α. For dimerisation with degree of "
    "association α: i = 1 − α/2.",
    ["AB: 1 + 0.5 × 1 = 1.5 → IV", "AB₂: 1 + 0.5 × 2 = 2.0 → I", "Dimerisation: 1 − 0.5/2 = 0.75 → II",
     "AB₃: 1 + 0.5 × 3 = 2.5 → III"],
    why="The wrong codes swap AB with AB₂, AB₂ with AB₃, or the dimer with AB₃ (association LOWERS i below 1).",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=80, checked=True)
