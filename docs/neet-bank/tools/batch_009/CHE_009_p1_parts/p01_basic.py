

# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"

m_nh3 = 1.204e22 / NA * 17
assert close(m_nh3, 0.34) and close(1.204e22 / NA * 14, 0.28) and close(1.204e22 / NA * 4 * 17, 1.36)
add("Mole concept", B, "numerical",
    "The mass of 1.204 × 10²² molecules of ammonia is (N = 14, H = 1, Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("C", "0.34 g", ["0.28 g", "3.4 g", "1.36 g"]),
    "Converting a number of molecules into a mass through the mole",
    "Divide the number of molecules by the Avogadro constant to get moles, then multiply by the molar mass of NH₃.",
    ["n = 1.204 × 10²² / 6.022 × 10²³ = 0.020 mol", "M(NH₃) = 14 + 3 = 17 g mol⁻¹",
     "Mass = 0.020 × 17 = 0.34 g"],
    why="0.28 g uses the molar mass of nitrogen alone (14 g mol⁻¹). 3.4 g misplaces the power of ten (0.2 mol). "
        "1.36 g counts four atoms per molecule as if they were four molecules.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=35, checked=True)

masses = {"H₂": 2, "N₂": 28, "O₂": 32, "CO₂": 44}
assert min(masses, key=masses.get) == "H₂"
add("Mole concept", B, "direct",
    "Which of the following samples contains the LARGEST number of molecules? (H = 1, C = 12, N = 14, O = 16)",
    Opts("A", "1 g of H₂", ["1 g of N₂", "1 g of O₂", "1 g of CO₂"]),
    "For equal masses, the number of molecules is inversely proportional to the molar mass",
    "Number of molecules = (mass/molar mass) × Nₐ. With the mass fixed at 1 g, the gas with the smallest molar "
    "mass (H₂, 2 g mol⁻¹) has the most moles and so the most molecules.",
    ["n = 1/M: H₂ 0.5 mol; N₂ 0.036 mol; O₂ 0.031 mol; CO₂ 0.023 mol", "Largest n → H₂"],
    why="N₂, O₂ and CO₂ have larger molar masses, so 1 g of each contains fewer moles and fewer molecules.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=25)

p_mol, o_mol = 43.66 / 31, 56.34 / 16
assert close(o_mol / p_mol, 2.5)
add("Empirical and molecular formulae", I, "numerical",
    "An oxide of phosphorus contains 43.66% phosphorus and 56.34% oxygen by mass. Its empirical formula is "
    "(P = 31, O = 16):",
    Opts("D", "P₂O₅", ["PO₂", "P₂O₃", "PO₃"]),
    "Empirical formula from percentage composition",
    "Convert the mass per cent of each element into moles, divide by the smaller value, and multiply by a whole "
    "number if the ratio is not a whole-number ratio.",
    ["P: 43.66/31 = 1.408 mol; O: 56.34/16 = 3.521 mol", "O : P = 3.521/1.408 = 2.5",
     "P : O = 1 : 2.5 = 2 : 5 → P₂O₅"],
    why="PO₂ rounds 2.5 down to 2 instead of doubling the ratio. P₂O₃ is a different oxide (P : O = 1 : 1.5). "
        "PO₃ rounds 2.5 up to 3.",
    ncert=f"{REF1}, empirical formula for molecular formula", seconds=60, checked=True)

n_mg = 2.4 / 24
v_acid = n_mg / 0.25 * 1000
assert close(v_acid, 400) and close(n_mg / 2 / 0.25 * 1000, 200) and close(2 * n_mg / 0.25 * 1000, 800)
add("Stoichiometry", I, "numerical",
    "The volume of 0.25 M sulphuric acid needed to react completely with 2.4 g of magnesium, "
    "Mg(s) + H₂SO₄(aq) → MgSO₄(aq) + H₂(g), is (Mg = 24):",
    Opts("B", "400 mL", ["200 mL", "800 mL", "40 mL"]),
    "Stoichiometry with a solution: moles = molarity × volume",
    "Find the moles of Mg, use the 1 : 1 mole ratio with H₂SO₄, and divide by the molarity to get the volume.",
    ["n(Mg) = 2.4/24 = 0.10 mol", "n(H₂SO₄) = 0.10 mol (1 : 1)", "V = 0.10/0.25 = 0.40 L = 400 mL"],
    why="200 mL takes two Mg per H₂SO₄. 800 mL takes two H₂SO₄ per Mg (confusing it with HCl, which needs 2 mol "
        "per mol Mg). 40 mL is a slip of a power of ten in the litre-to-millilitre conversion.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=50, checked=True)

add("Empirical and molecular formulae", I, "assertion_reason",
    ar("Two different compounds can have exactly the same percentage composition by mass.",
       "Percentage composition fixes only the simplest whole-number ratio of atoms (the empirical formula), "
       "not the actual number of atoms in a molecule."),
    AR_, "Empirical formula versus molecular formula",
    "Compounds such as ethyne (C₂H₂) and benzene (C₆H₆) share the empirical formula CH and therefore the same "
    "mass per cent of each element, though their molecular formulae differ. This is possible precisely because "
    "percentage composition determines only the atom ratio, not the molecular formula. R explains A.",
    ["A: same empirical formula → same percentage composition → true",
     "R: % composition → empirical formula only → true", "R is the reason A can happen → option A"],
    answer="A",
    why="Both statements are true, and R is exactly why compounds with different molecular formulae can share a "
        "composition, so the 'not the explanation' option does not apply.",
    ncert=f"{REF1}, empirical formula for molecular formula", seconds=40)

add("Stoichiometry", I, "statement_pair",
    sp("In a balanced chemical equation, the coefficients give the ratio of the amounts (in moles) of the "
       "reactants and products.",
       "For a reaction between gases, the coefficients of a balanced equation also give the ratio of the masses "
       "of the reacting gases."),
    SP_, "What the coefficients of a balanced equation mean",
    "The coefficients are mole (and molecule) ratios; for gases at the same temperature and pressure they are "
    "also volume ratios. They are not mass ratios: in 2H₂ + O₂ → 2H₂O, 2 mol (4 g) of H₂ reacts with 1 mol "
    "(32 g) of O₂, a mass ratio of 1 : 8, not 2 : 1.",
    ["I: coefficients = mole ratio → true", "II: masses depend on molar masses; 2 : 1 by moles is 4 g : 32 g → false"],
    answer="C",
    why="Statement II confuses the mole (or volume) ratio with the mass ratio.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=35)

n_na2co3_total = 0.53 / 106
n_aliquot = n_na2co3_total * 20 / 100
m_hcl = 2 * n_aliquot / 0.025
assert close(m_hcl, 0.08) and close(n_aliquot / 0.025, 0.04) and close(2 * n_na2co3_total / 0.025, 0.4) \
    and close(2 * n_aliquot / 0.020, 0.10)
add("Stoichiometry", A, "numerical",
    "0.53 g of anhydrous sodium carbonate is dissolved in water and the solution is made up to 100 mL. 20.0 mL of "
    "this solution reacts completely with 25.0 mL of a hydrochloric acid solution: "
    "Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂. The molarity of the hydrochloric acid is (Na = 23, C = 12, O = 16):",
    Opts("A", "0.080 M", ["0.040 M", "0.40 M", "0.10 M"]),
    "Stoichiometry of a titration with an aliquot of a standard solution",
    "Find the moles of Na₂CO₃ in the 20 mL portion that was titrated, double it for HCl (1 : 2), and divide by "
    "the volume of acid used.",
    ["n(Na₂CO₃) in 100 mL = 0.53/106 = 0.0050 mol", "In 20.0 mL: 0.0050 × 20/100 = 0.0010 mol",
     "n(HCl) = 2 × 0.0010 = 0.0020 mol", "M = 0.0020/0.0250 = 0.080 M"],
    why="0.040 M ignores the 1 : 2 ratio. 0.40 M uses all the Na₂CO₃ in 100 mL instead of the 20 mL portion. "
        "0.10 M divides by the 20.0 mL of carbonate solution instead of the 25.0 mL of acid.",
    ncert=f"{REF1}, reactions in solutions (molarity)", seconds=100, checked=True)

n_salt = 0.5 * 0.2
truth1 = {"a": close(n_salt * 142, 14.2), "b": close(2 * n_salt, 0.2), "c": close(3 * n_salt, 0.2),
          "d": close(2 * 0.2, 0.4), "e": close(n_salt * 32, 6.4)}
assert truth1 == {"a": True, "b": True, "c": False, "d": True, "e": False}
add("Mole concept", A, "multi_statement",
    ms("500 mL of a 0.20 M aqueous solution of sodium sulphate, Na₂SO₄, is prepared. Assuming complete "
       "dissociation, which of the following statements are correct? (Na = 23, S = 32, O = 16)",
       ["The solution contains 14.2 g of Na₂SO₄.",
        "The solution contains 0.20 mol of Na⁺ ions.",
        "The solution contains 0.20 mol of ions in all.",
        "The concentration of Na⁺ ions in the solution is 0.40 M.",
        "The mass of sulphur in the solution is 6.4 g."]),
    multi("B", truth1, ["(a), (b), (c) and (d) only", "(a) and (e) only", "(b), (d) and (e) only"]),
    "Moles of a solute and of its ions from molarity and volume",
    "n(Na₂SO₄) = 0.20 × 0.500 = 0.10 mol. Each formula unit gives 2 Na⁺ and 1 SO₄²⁻.",
    ["(a) 0.10 × 142 = 14.2 g ✓", "(b) 2 × 0.10 = 0.20 mol Na⁺ ✓", "(c) 3 × 0.10 = 0.30 mol of ions ✗",
     "(d) [Na⁺] = 2 × 0.20 = 0.40 M ✓", "(e) 0.10 × 32 = 3.2 g of S ✗"],
    why="(c) forgets that each formula unit gives three ions; (e) doubles the amount of sulphur. Every option "
        "containing (c) or (e) is wrong, and the remaining option omitting (a) is incomplete.",
    ncert=f"{REF1}, mole concept; reactions in solutions", seconds=90, checked=True)

o2 = {"A": 3 / 12 * 1 * 32, "B": 4 / 16 * 2 * 32, "C": 4 / 2 * 0.5 * 32, "D": 15 / 30 * 3.5 * 32}
assert {k: round(v) for k, v in o2.items()} == {"A": 8, "B": 16, "C": 32, "D": 56}
add("Stoichiometry", A, "match_list",
    lists("Match List-I (substance burnt completely in an excess of oxygen) with List-II (mass of O₂ consumed). "
          "(H = 1, C = 12, O = 16)",
          ["3 g of carbon (C + O₂ → CO₂)", "4 g of methane (CH₄ + 2O₂ → CO₂ + 2H₂O)",
           "4 g of hydrogen (2H₂ + O₂ → 2H₂O)", "15 g of ethane (2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O)"],
          ["16 g", "32 g", "56 g", "8 g"]),
    match("D", M("IV I II III"), [M("I IV II III"), M("IV I III II"), M("IV II I III")]),
    "Mass–mole–mass stoichiometry",
    "Convert each mass to moles, use the mole ratio with O₂ from the equation, and convert O₂ to grams.",
    ["A: 0.25 mol C × 1 = 0.25 mol O₂ = 8 g → IV", "B: 0.25 mol CH₄ × 2 = 0.5 mol O₂ = 16 g → I",
     "C: 2 mol H₂ × ½ = 1 mol O₂ = 32 g → II", "D: 0.5 mol C₂H₆ × 3.5 = 1.75 mol O₂ = 56 g → III"],
    why="A-I/B-IV swaps carbon and methane; C-III/D-II forgets the factor 3.5 for ethane; B-II/C-I ignores that "
        "two H₂ need only one O₂.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=100, checked=True)
