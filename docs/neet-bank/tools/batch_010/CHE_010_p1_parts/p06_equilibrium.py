

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

ratio_h = 10 ** -5 / 10 ** -8
assert close(ratio_h, 1000)
add("Acids, bases and pH", B, "numerical",
    "At 298 K, solution P has pH 5 and solution Q has pH 8. The hydronium ion concentration of P is how many "
    "times that of Q?",
    Opts("B", "1000 times", ["3 times", "1.6 times", "10⁻³ times"]),
    "pH = −log[H₃O⁺]; each unit of pH is a factor of 10 in [H₃O⁺]",
    "[H₃O⁺] = 10⁻ᵖᴴ. The ratio is 10⁻⁵/10⁻⁸ = 10³.",
    ["P: [H₃O⁺] = 10⁻⁵ M", "Q: [H₃O⁺] = 10⁻⁸ M", "Ratio = 10⁻⁵/10⁻⁸ = 1000"],
    why="3 times treats the difference in pH as a ratio of concentrations. 1.6 times divides the pH values "
        "(8/5). 10⁻³ inverts the ratio: the solution with the lower pH has the HIGHER [H₃O⁺].",
    ncert=f"{REF6}, the pH scale", seconds=25, checked=True)

ksp_agbr = (7.0e-7) ** 2
assert close(ksp_agbr, 4.9e-13) and close((2 * 7.0e-7) ** 2, 1.96e-12)
add("Solubility product", B, "numerical",
    "The molar solubility of silver bromide, AgBr, in water at 298 K is 7.0 × 10⁻⁷ mol L⁻¹. Its solubility "
    "product at 298 K is:",
    Opts("A", "4.9 × 10⁻¹³", ["7.0 × 10⁻⁷", "1.4 × 10⁻⁶", "1.96 × 10⁻¹²"]),
    "K_sp of a 1 : 1 salt: AgBr(s) ⇌ Ag⁺(aq) + Br⁻(aq); K_sp = s²",
    "Each mole of AgBr that dissolves gives one mole of Ag⁺ and one mole of Br⁻, so both ion concentrations "
    "equal s.",
    ["[Ag⁺] = [Br⁻] = s = 7.0 × 10⁻⁷ M", "K_sp = s² = (7.0 × 10⁻⁷)² = 4.9 × 10⁻¹³"],
    why="7.0 × 10⁻⁷ is the solubility itself, not K_sp. 1.4 × 10⁻⁶ adds the two ion concentrations. "
        "1.96 × 10⁻¹² squares 2s, as if AgBr gave two of each ion.",
    ncert=f"{REF6}, solubility equilibria of sparingly soluble salts", seconds=30, checked=True)

add("Kp, Kc and Le Chatelier", B, "assertion_reason",
    ar("The equilibrium constant of a reaction changes when the temperature is changed.",
       "Adding a catalyst does not change the equilibrium constant of a reaction."),
    AR_, "Factors that do and do not change K",
    "A is true: K depends on temperature (it rises with temperature for an endothermic reaction and falls for "
    "an exothermic one). R is also true: a catalyst speeds up the forward and backward reactions equally and "
    "leaves K unchanged. But the behaviour of a catalyst says nothing about why temperature changes K; R is a "
    "separate fact.",
    ["A: K = f(T) → true", "R: catalyst → equilibrium reached faster, K unchanged → true",
     "R does not explain the temperature dependence in A → option B"],
    answer="B",
    why="R is about a catalyst, a different factor from temperature, so it cannot be the explanation of A; both "
        "statements are true, so C and D are wrong.",
    ncert=f"{REF6}, factors affecting equilibria (temperature; catalyst)", seconds=35)

add("Acids, bases and pH", B, "direct",
    "Which of the following is NOT a conjugate acid–base pair?",
    Opts("D", "H₃PO₄ and HPO₄²⁻", ["H₂O and OH⁻", "NH₄⁺ and NH₃", "HSO₄⁻ and SO₄²⁻"]),
    "Brønsted–Lowry conjugate acid–base pairs differ by exactly one proton",
    "An acid and its conjugate base differ by one H⁺. H₃PO₄ and HPO₄²⁻ differ by two protons; the conjugate base "
    "of H₃PO₄ is H₂PO₄⁻.",
    ["H₂O/OH⁻: differ by one H⁺ ✓", "NH₄⁺/NH₃: one H⁺ ✓", "HSO₄⁻/SO₄²⁻: one H⁺ ✓",
     "H₃PO₄/HPO₄²⁻: two H⁺ → not a conjugate pair"],
    why="Each of the other three pairs differs by exactly one proton, so each is a genuine conjugate pair.",
    ncert=f"{REF6}, Brönsted–Lowry acids and bases", seconds=25)

add("Physical equilibria and Henry's law", B, "match_list",
    lists("Match List-I (equilibrium in a closed vessel at constant temperature) with List-II (its type).",
          ["H₂O(l) ⇌ H₂O(g)", "N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", "CaCO₃(s) ⇌ CaO(s) + CO₂(g)", "I₂(s) ⇌ I₂(g)"],
          ["Physical equilibrium: solid ⇌ vapour", "Homogeneous chemical equilibrium",
           "Physical equilibrium: liquid ⇌ vapour", "Heterogeneous chemical equilibrium"]),
    match("C", M("III II IV I"), [M("I II IV III"), M("III IV II I"), M("III II I IV")]),
    "Physical versus chemical equilibria; homogeneous versus heterogeneous",
    "A physical equilibrium involves only a change of state; a chemical equilibrium involves a reaction. A "
    "chemical equilibrium is homogeneous when all species are in one phase and heterogeneous when more than one "
    "phase is present.",
    ["A: evaporation ⇌ condensation of water → III", "B: all gases, chemical change → homogeneous → II",
     "C: two solids and a gas → heterogeneous → IV", "D: sublimation of iodine → solid ⇌ vapour → I"],
    why="A-I/D-III swaps the two physical equilibria. B-IV/C-II swaps the homogeneous and heterogeneous "
        "reactions. C-I/D-IV calls the decomposition of CaCO₃ a physical change.",
    ncert=f"{REF6}, equilibrium in physical processes; homogeneous and heterogeneous equilibria", seconds=45)

poh = 4.74 + math.log10(0.10 / 0.20)
ph_buf = 14 - poh
assert close(ph_buf, 9.56, 0.001) and close(14 - (4.74 + math.log10(2)), 8.96, 0.001)
add("Hydrolysis and buffers", I, "numerical",
    "A buffer solution at 298 K contains 0.20 M aqueous ammonia (NH₄OH) and 0.10 M ammonium chloride. Its pH is "
    "(pK_b of NH₄OH = 4.74; pK_w = 14; log 2 = 0.30):",
    Opts("A", "9.56", ["8.96", "4.44", "9.26"]),
    "Basic buffer: pOH = pK_b + log([salt]/[base])",
    "Find the pOH of the basic buffer from the Henderson–Hasselbalch form for bases, then pH = 14 − pOH.",
    ["pOH = 4.74 + log(0.10/0.20) = 4.74 − 0.30 = 4.44", "pH = 14 − 4.44 = 9.56"],
    why="8.96 inverts the ratio (base/salt instead of salt/base). 4.44 reports the pOH as the pH. 9.26 is "
        "14 − pK_b, the pH only when the salt and base concentrations are equal.",
    ncert=f"{REF6}, buffer solutions", seconds=50, checked=True)

s_common = 4.0e-11 / 0.10 ** 2
assert close(s_common, 4.0e-9) and close(4.0e-11 / 0.10, 4.0e-10) and close(4.0e-11 / 0.20 ** 2, 1.0e-9) \
    and close((4.0e-11 / 4) ** (1 / 3), 2.15e-4, 0.005)
add("Solubility product", I, "numerical",
    "A sparingly soluble fluoride MF₂ dissolves as MF₂(s) ⇌ M²⁺(aq) + 2F⁻(aq); its K_sp at 298 K is "
    "4.0 × 10⁻¹¹. Its molar solubility in a 0.10 M NaF solution at 298 K is (NaF completely dissociated; "
    "∛10 = 2.15):",
    Opts("C", "4.0 × 10⁻⁹ M", ["4.0 × 10⁻¹⁰ M", "1.0 × 10⁻⁹ M", "2.2 × 10⁻⁴ M"]),
    "Common ion effect on solubility: K_sp = [M²⁺][F⁻]² with [F⁻] fixed by the added salt",
    "The F⁻ from NaF (0.10 M) is far greater than the F⁻ from the dissolved MF₂, so [F⁻] ≈ 0.10 M and "
    "s = [M²⁺] = K_sp/[F⁻]².",
    ["[F⁻] ≈ 0.10 M", "s = 4.0 × 10⁻¹¹ / (0.10)² = 4.0 × 10⁻⁹ M"],
    why="4.0 × 10⁻¹⁰ M forgets to square [F⁻]. 1.0 × 10⁻⁹ M doubles the fluoride from NaF (takes 0.20 M). "
        "2.2 × 10⁻⁴ M is the solubility in pure water, ∛(K_sp/4), with the common ion ignored.",
    ncert=f"{REF6}, common ion effect in the ionisation of sparingly soluble salts", seconds=60, checked=True)

p_n2 = 0.80 * 2.5
x_n2 = p_n2 / 100e3
assert close(x_n2, 2.0e-5) and close(2.5 / 100e3, 2.5e-5) and close(p_n2 / 100, 2.0e-2) and close(0.80 / 100e3, 8.0e-6)
add("Physical equilibria and Henry's law", I, "numerical",
    "Air containing 80% nitrogen by moles is kept over water at a total pressure of 2.5 bar at a temperature "
    "at which the Henry's law constant of N₂ in water is K_H = 100 kbar. The mole fraction of nitrogen "
    "dissolved in the water is:",
    Opts("D", "2.0 × 10⁻⁵", ["2.5 × 10⁻⁵", "2.0 × 10⁻²", "8.0 × 10⁻⁶"]),
    "Henry's law with Dalton's law of partial pressures: p = K_H x, where p is the PARTIAL pressure",
    "First find the partial pressure of N₂ (mole fraction in air × total pressure), then x = p/K_H with both "
    "pressures in the same unit.",
    ["p(N₂) = 0.80 × 2.5 bar = 2.0 bar", "K_H = 100 kbar = 1.0 × 10⁵ bar",
     "x(N₂) = 2.0 / 1.0 × 10⁵ = 2.0 × 10⁻⁵"],
    why="2.5 × 10⁻⁵ uses the total pressure instead of the partial pressure of N₂. 2.0 × 10⁻² leaves K_H in "
        "kbar. 8.0 × 10⁻⁶ uses the mole fraction 0.80 as if it were the pressure.",
    ncert=f"{C12}, 'Solutions', Henry's law", seconds=55, checked=True)

pkw_323 = -math.log10(5.5e-14)
assert close(pkw_323, 13.26, 0.001)
add("Acids, bases and pH", I, "statement_pair",
    sp("At 323 K, where K_w = 5.5 × 10⁻¹⁴, the pH and pOH of any aqueous solution add up to 14.",
       "At 298 K, where K_w = 1.0 × 10⁻¹⁴, the pH and pOH of any aqueous solution add up to 14."),
    SP_, "pH + pOH = pK_w, which depends on temperature",
    "Taking −log of K_w = [H₃O⁺][OH⁻] gives pH + pOH = pK_w. At 298 K, pK_w = 14. At 323 K, "
    "pK_w = −log(5.5 × 10⁻¹⁴) = 14 − 0.74 = 13.26, so pH + pOH = 13.26, not 14.",
    ["pH + pOH = pK_w", "323 K: pK_w = 13.26 → I false", "298 K: pK_w = 14 → II true"],
    answer="D",
    why="Statement I uses the 298 K value of pK_w at a temperature where K_w is larger.",
    ncert=f"{REF6}, ionization constant of water and its ionic product; the pH scale", seconds=45, checked=True)

add("Acids, bases and pH", I, "assertion_reason",
    ar("Acetic acid is a weak electrolyte.",
       "Acetic acid is only slightly soluble in water."),
    AR_, "Strong and weak electrolytes",
    "A weak electrolyte is one that is only partially ionised in solution. Acetic acid mixes with water in all "
    "proportions (it is very soluble), but only a small fraction of its molecules ionise, so it is a weak "
    "electrolyte. A is true; R is false.",
    ["A: partially ionised → weak electrolyte → true",
     "R: acetic acid is miscible with water → false",
     "Weakness is about the extent of ionisation, not solubility"],
    answer="C",
    why="R confuses the extent of ionisation with solubility; a substance can be very soluble yet weakly "
        "ionised.",
    ncert=f"{REF6}, ionic equilibrium in solution (strong and weak electrolytes)", seconds=30)

truth_h = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Physical equilibria and Henry's law", I, "multi_statement",
    ms("Which of the following statements about Henry's law and the solubility of gases in liquids are "
       "correct?",
       ["The Henry's law constant, K_H, depends on the nature of the gas.",
        "At a given partial pressure and temperature, the higher the K_H value of a gas, the lower its "
        "solubility in the liquid.",
        "The K_H value of a gas in water increases as the temperature rises.",
        "The solubility of a gas in a liquid increases as the temperature rises.",
        "At constant temperature, the mole fraction of a gas in its solution is inversely proportional to the "
        "partial pressure of the gas above the solution."]),
    multi("B", truth_h, ["(a), (b), (c) and (e) only", "(a), (c) and (d) only", "(b) and (d) only"]),
    "Henry's law: p = K_H x",
    "x = p/K_H, so the mole fraction dissolved is directly proportional to the partial pressure and inversely "
    "proportional to K_H. K_H differs from gas to gas and rises with temperature, so gases become less soluble "
    "on warming.",
    ["(a) ✓", "(b) x = p/K_H → larger K_H, smaller x ✓", "(c) ✓ (NCERT)",
     "(d) ✗: K_H rises → solubility falls with temperature",
     "(e) ✗: x is directly proportional to p"],
    why="(d) reverses the effect of temperature and (e) reverses Henry's law; any option containing either is "
        "wrong.",
    ncert=f"{C12}, 'Solutions', Henry's law", seconds=60)

x = (4.0 * 0.70 - 0.80) / 5.0
assert close(x, 0.40) and close((0.80 + x) / (0.70 - x), 4.0) and close(0.80 + x, 1.20)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "For the equilibrium A(g) ⇌ B(g), K_c = 4.0 at a certain temperature. An equilibrium mixture in a closed "
    "1.0 L vessel contains 0.20 mol of A and 0.80 mol of B. Another 0.50 mol of A is now added, the temperature "
    "and volume being kept constant. When equilibrium is re-established, the amount of B is:",
    Opts("D", "1.20 mol", ["1.30 mol", "0.80 mol", "2.80 mol"]),
    "Le Chatelier's principle made quantitative: the system re-adjusts until Q = K again",
    "After the addition, Q = 0.80/0.70 < K, so the reaction moves forward. Let x mol of A change into B and use "
    "K_c to find x.",
    ["After adding A: [A] = 0.70 M, [B] = 0.80 M; Q = 1.14 < 4.0 → forward",
     "(0.80 + x)/(0.70 − x) = 4.0 → 0.80 + x = 2.80 − 4x → x = 0.40",
     "B = 0.80 + 0.40 = 1.20 mol (A = 0.30 mol; check 1.20/0.30 = 4.0)"],
    why="1.30 mol assumes all the added A turns into B. 0.80 mol assumes the equilibrium does not shift. "
        "2.80 mol multiplies K by the new amount of A without letting A be used up.",
    ncert=f"{REF6}, effect of concentration change (Le Chatelier's principle)", seconds=100, checked=True)

kp_pcl5 = 0.5 ** 2 * 1.0 / (1 - 0.5 ** 2)
p_new = kp_pcl5 * (1 - 0.2 ** 2) / 0.2 ** 2
assert close(p_new, 8.0) and close((0.5 / 0.2) ** 2, 6.25) and close(0.5 / 0.2, 2.5)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "Pure PCl₅ is heated to a fixed temperature: PCl₅(g) ⇌ PCl₃(g) + Cl₂(g). At a total equilibrium pressure of "
    "1.0 atm it is 50% dissociated. At the same temperature, the total equilibrium pressure at which it would be "
    "only 20% dissociated is (for this equilibrium, K_p = α²P/(1 − α²), where α is the degree of dissociation "
    "and P the total pressure):",
    Opts("A", "8.0 atm", ["6.25 atm", "2.5 atm", "0.125 atm"]),
    "K_p is constant at a fixed temperature; the degree of dissociation adjusts to the total pressure",
    "Find K_p from the first set of data, then solve the same relation for P when α = 0.20.",
    ["K_p = (0.5)² × 1.0 / (1 − 0.25) = 0.25/0.75 = 1/3 atm", "At α = 0.20: 1/3 = 0.04 P / 0.96",
     "P = (1/3) × 0.96/0.04 = 8.0 atm"],
    why="6.25 atm uses the approximation K_p ≈ α²P (ignoring α² in 1 − α²), not valid at α = 0.5. 2.5 atm "
        "takes α inversely proportional to P. 0.125 atm inverts the pressure ratio; lowering α needs a "
        "HIGHER pressure.",
    ncert=f"{REF6}, equilibrium constant Kp; effect of pressure change", seconds=110, checked=True)

c_base = 0.010 / 0.200
oh = math.sqrt(2.0e-5 * c_base)
ph_mix = 14 + math.log10(oh)
assert close(c_base, 0.050) and close(ph_mix, 11.0, 0.001) \
    and close(14 + math.log10(math.sqrt(2.0e-5 * 0.10)), 11.15, 0.001) and close(14 + math.log10(0.05), 12.7, 0.001)
add("Hydrolysis and buffers", A, "numerical",
    "100 mL of 0.10 M ammonium chloride solution is mixed with 100 mL of 0.10 M sodium hydroxide solution at "
    "298 K. The pH of the resulting solution is (K_b of NH₄OH = 2.0 × 10⁻⁵; pK_w = 14; for a weak base, "
    "[OH⁻] ≈ √(K_b c)):",
    Opts("B", "11.0", ["11.15", "7.0", "12.7"]),
    "A strong base displaces a weak base from its salt; then the pH of a weak base",
    "NH₄Cl + NaOH → NH₄OH + NaCl. Equal amounts react completely, leaving only the weak base NH₄OH (NaCl is "
    "neutral), diluted into 200 mL.",
    ["n(NH₄OH) = 0.10 × 0.100 = 0.010 mol in 0.200 L → c = 0.050 M",
     "[OH⁻] = √(2.0 × 10⁻⁵ × 0.050) = √(1.0 × 10⁻⁶) = 1.0 × 10⁻³ M", "pOH = 3.0; pH = 11.0"],
    why="11.15 forgets that mixing doubles the volume (uses 0.10 M). 7.0 treats the mixture as a neutralisation "
        "that leaves only a neutral salt, overlooking the NH₄OH formed. 12.7 treats the solution as 0.05 M "
        "NaOH, as if no reaction occurred.",
    ncert=f"{REF6}, ionization of weak bases", seconds=110, checked=True)

add("Kp, Kc and Le Chatelier", A, "direct",
    "For which of the following equilibria will BOTH raising the temperature AND lowering the total pressure "
    "shift the equilibrium in the forward direction?",
    Opts("A", "PCl₅(g) ⇌ PCl₃(g) + Cl₂(g); ΔH > 0",
         ["N₂(g) + 3H₂(g) ⇌ 2NH₃(g); ΔH < 0", "N₂(g) + O₂(g) ⇌ 2NO(g); ΔH > 0",
          "2SO₂(g) + O₂(g) ⇌ 2SO₃(g); ΔH < 0"]),
    "Le Chatelier's principle for temperature and pressure",
    "Raising the temperature favours the endothermic direction, so the forward reaction must be endothermic "
    "(ΔH > 0). Lowering the pressure favours the side with more moles of gas, so the forward reaction must "
    "increase the moles of gas (Δn_g > 0).",
    ["PCl₅: ΔH > 0, Δn_g = +1 → both favour forward ✓", "NH₃ synthesis: ΔH < 0, Δn_g = −2 → both favour backward",
     "NO formation: ΔH > 0 but Δn_g = 0 → pressure has no effect", "SO₃ formation: ΔH < 0, Δn_g = −1 → both backward"],
    why="The NO equilibrium responds to temperature but not to pressure; the ammonia and SO₃ equilibria are "
        "pushed backward by both changes.",
    ncert=f"{REF6}, factors affecting equilibria", seconds=50)

add("Acids, bases and pH", A, "assertion_reason",
    ar("When a solution of a weak monobasic acid is diluted with water, its pH increases even though the degree "
       "of ionisation of the acid increases.",
       "On dilution [H₃O⁺] ≈ √(Kₐc) decreases, because the degree of ionisation (α ≈ √(Kₐ/c)) increases only as "
       "1/√c while the concentration c falls in direct proportion."),
    AR_, "Effect of dilution on the degree of ionisation and pH of a weak acid",
    "[H₃O⁺] = cα. Diluting 100 times raises α only 10 times, so cα falls 10 times and the pH rises by 1. R gives "
    "exactly this reasoning, so it explains A.",
    ["α ≈ √(Kₐ/c) → α rises on dilution", "[H₃O⁺] = cα = √(Kₐc) → falls on dilution",
     "Lower [H₃O⁺] → higher pH → R explains A"],
    answer="A",
    why="R is the quantitative reason why more ionisation still gives fewer H₃O⁺ ions per litre, so it is the "
        "correct explanation, not just a related fact.",
    ncert=f"{REF6}, ionization constants of weak acids", seconds=50)
