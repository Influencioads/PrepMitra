

# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"

n_c = 6 / 12
m_mg = n_c * 24
assert close(m_mg, 12) and close(6 * 12 / 24, 3)
add("Mole concept", B, "numerical",
    "What mass of magnesium contains the same number of atoms as 6 g of carbon? (C = 12, Mg = 24)",
    Opts("C", "12 g", ["6 g", "24 g", "3 g"]),
    "Equal numbers of atoms means equal amounts (moles) of atoms",
    "Find the moles of carbon atoms in 6 g; the same number of moles of Mg atoms is needed. Multiply by the "
    "molar mass of Mg.",
    ["n(C) = 6/12 = 0.5 mol", "n(Mg) = 0.5 mol", "m(Mg) = 0.5 × 24 = 12 g"],
    why="6 g assumes equal masses contain equal numbers of atoms. 24 g is the mass of a whole mole of Mg. "
        "3 g inverts the ratio of the molar masses (6 × 12/24).",
    ncert=f"{REF1}, mole concept and molar masses", seconds=30, checked=True)

add("Laws of chemical combination", B, "statement_pair",
    sp("Gay-Lussac's law of gaseous volumes is, in effect, the law of definite proportions applied to the "
       "volumes of reacting gases.",
       "Avogadro's hypothesis made a distinction between atoms and molecules."),
    SP_, "Gay-Lussac's law and Avogadro's law",
    "NCERT describes Gay-Lussac's law (gases combine in a simple whole-number ratio by volume at the same "
    "temperature and pressure) as the law of definite proportions by volume. Avogadro proposed that equal "
    "volumes of gases at the same temperature and pressure contain equal numbers of molecules, and in doing so "
    "distinguished atoms from molecules.",
    ["I: Gay-Lussac's law = definite proportions by volume → true",
     "II: Avogadro distinguished atoms from molecules → true"],
    answer="A",
    why="Both statements are NCERT statements, so no option that calls either of them false can be right.",
    ncert=f"{REF1}, Gay Lussac's law of gaseous volumes; Avogadro's law", seconds=35)

n_fe = 16.8 / 56
m_o2 = n_fe * 2 / 3 * 32
assert close(m_o2, 6.4) and close(n_fe * 16, 4.8) and close(n_fe / 2 * 1.5 * 32, 7.2) and close(n_fe * 32, 9.6)
add("Stoichiometry", I, "numerical",
    "The mass of oxygen gas needed to convert 16.8 g of iron completely into Fe₃O₄, "
    "3Fe(s) + 2O₂(g) → Fe₃O₄(s), is (Fe = 56, O = 16):",
    Opts("D", "6.4 g", ["4.8 g", "7.2 g", "9.6 g"]),
    "Mass–mole–mass calculation from a balanced equation",
    "Convert the mass of iron to moles, use the 3 : 2 mole ratio of Fe to O₂, and convert O₂ to grams.",
    ["n(Fe) = 16.8/56 = 0.30 mol", "n(O₂) = 0.30 × 2/3 = 0.20 mol", "m(O₂) = 0.20 × 32 = 6.4 g"],
    why="4.8 g takes one O atom per Fe atom (FeO). 7.2 g uses the Fe₂O₃ ratio (1.5 mol O₂ per 2 mol Fe). "
        "9.6 g takes one O₂ per Fe.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=50, checked=True)

o_atoms = {"A": 0.5 * 3, "B": 49 / 98 * 4, "C": 9 / 18 * 1, "D": 16 / 16}
assert o_atoms == {"A": 1.5, "B": 2.0, "C": 0.5, "D": 1.0}
add("Mole concept", I, "match_list",
    lists("Match List-I (sample) with List-II (amount of oxygen ATOMS it contains). "
          "(H = 1, C = 12, O = 16, Na = 23, S = 32)",
          ["0.5 mol of Na₂CO₃", "49 g of H₂SO₄", "9 g of H₂O", "16 g of O₃"],
          ["0.5 mol", "1.0 mol", "1.5 mol", "2.0 mol"]),
    match("B", M("III IV I II"), [M("III II I IV"), M("I IV III II"), M("III IV II I")]),
    "Moles of atoms = moles of the substance × number of those atoms in one formula unit",
    "Find the moles of each substance and multiply by the number of oxygen atoms in its formula.",
    ["A: 0.5 × 3 = 1.5 mol → III", "B: 49/98 = 0.5 mol H₂SO₄ × 4 = 2.0 mol → IV",
     "C: 9/18 = 0.5 mol H₂O × 1 = 0.5 mol → I", "D: 16/48 = 1/3 mol O₃ × 3 = 1.0 mol (or simply 16/16) → II"],
    why="B-II/D-IV counts molecules of H₂SO₄ or O₃ instead of oxygen atoms. A-I/C-III swaps the carbonate and "
        "water values. C-II/D-I takes 16 g of O₃ as 0.5 mol of atoms by using the molar mass of O₂.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=75, checked=True)

add("Laws of chemical combination", I, "assertion_reason",
    ar("The average atomic mass of chlorine, 35.5 u, is not a whole number.",
       "Naturally occurring chlorine is a mixture of isotopes of different masses, and its atomic mass is the "
       "abundance-weighted average of their masses."),
    AR_, "Average atomic mass of an element with isotopes",
    "Each chlorine isotope has a mass close to a whole number (about 35 u and 37 u), but natural chlorine "
    "contains both in a fixed ratio. The atomic mass quoted for the element is their weighted average, which "
    "lies between them and is not a whole number. R is exactly why A is true.",
    ["A: atomic mass of Cl = 35.5 u → true", "R: isotopes averaged by abundance → true",
     "The averaging in R produces the non-integral value in A → option A"],
    answer="A",
    why="R is not merely another true fact about chlorine: it is the reason the quoted atomic mass is "
        "fractional, so 'not the correct explanation' does not apply.",
    ncert=f"{REF1}, atomic and molecular masses (average atomic mass)", seconds=35)

v_co, v_o2 = 30, 20
used_o2 = v_co / 2
left = v_co + (v_o2 - used_o2)
assert left == 35 and v_o2 * 2 == 40
add("Stoichiometry", A, "numerical",
    "30 mL of carbon monoxide is mixed with 20 mL of oxygen and the mixture is ignited: "
    "2CO(g) + O₂(g) → 2CO₂(g). All volumes are measured at the same temperature and pressure. The total volume "
    "of gas left after the reaction is:",
    Opts("B", "35 mL", ["30 mL", "50 mL", "40 mL"]),
    "Gay-Lussac's law of gaseous volumes combined with a limiting reagent",
    "Volumes of gases at the same temperature and pressure react in the ratio of their coefficients. Find the "
    "limiting gas, the volume of product formed and the volume of the excess gas left over.",
    ["30 mL CO needs 15 mL O₂; 20 mL O₂ is available → CO is limiting",
     "CO₂ formed = 30 mL; O₂ left = 20 − 15 = 5 mL", "Total gas = 30 + 5 = 35 mL"],
    why="30 mL counts only the CO₂ and forgets the unused oxygen. 50 mL assumes the volume does not change "
        "on reaction. 40 mL treats O₂ as the limiting gas (20 mL O₂ → 40 mL CO₂), although that would need "
        "40 mL of CO.",
    ncert=f"{REF1}, Gay Lussac's law of gaseous volumes; limiting reagent", seconds=80, checked=True)

mol_mass, ef_mass = 84, 14
n_mult = mol_mass // ef_mass
pc_c = 72 / 84 * 100
h_atoms = 0.1 * 12
water = 0.1 * 6 * 18
truth_cx = {"a": n_mult == 6, "b": close(pc_c, 85.7), "c": close(h_atoms, 0.6), "d": True,
            "e": close(water, 21.6)}
assert truth_cx == {"a": True, "b": True, "c": False, "d": True, "e": False} and close(water, 10.8)
add("Empirical and molecular formulae", A, "multi_statement",
    ms("A hydrocarbon has the empirical formula CH₂ and a molar mass of 84 g mol⁻¹. Which of the following "
       "statements about it are correct? (C = 12, H = 1, O = 16)",
       ["Its molecular formula is C₆H₁₂.",
        "It contains about 85.7% carbon by mass.",
        "0.1 mol of it contains 0.6 mol of hydrogen atoms.",
        "It has the same percentage composition by mass as ethene (C₂H₄).",
        "Complete combustion of 8.4 g of it gives 21.6 g of water."]),
    multi("D", truth_cx, ["(a), (b), (c) and (d) only", "(a), (d) and (e) only", "(b), (c) and (e) only"]),
    "Molecular formula = n × empirical formula; composition and stoichiometry from the formula",
    "Empirical formula mass of CH₂ = 14, so n = 84/14 = 6 and the formula is C₆H₁₂. Use it to check each "
    "statement.",
    ["(a) n = 6 → C₆H₁₂ ✓", "(b) %C = 72/84 × 100 = 85.7% ✓",
     "(c) 0.1 mol × 12 H = 1.2 mol H atoms, not 0.6 ✗", "(d) C₂H₄ also has empirical formula CH₂ → same % ✓",
     "(e) 8.4 g = 0.1 mol → 0.6 mol H₂O = 10.8 g, not 21.6 g ✗"],
    why="(c) counts H₂ molecules' worth of hydrogen (half the atoms); (e) doubles the water by taking 12 mol "
        "of H₂O per mol of hydrocarbon. Any option containing (c) or (e) is wrong.",
    ncert=f"{REF1}, empirical formula for molecular formula", seconds=100, checked=True)
