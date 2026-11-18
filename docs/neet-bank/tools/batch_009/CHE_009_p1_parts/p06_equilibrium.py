

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

add("Physical equilibria and Henry's law", B, "direct",
    "Bottles of soda water and soft drinks are sealed under high pressure in order to:",
    Opts("C", "increase the solubility of carbon dioxide in the drink",
         ["decrease the solubility of carbon dioxide in the drink", "raise the boiling point of the drink",
          "stop carbon dioxide from reacting with water"]),
    "Henry's law: the solubility of a gas in a liquid increases with its pressure",
    "By Henry's law, the mass of a gas dissolved in a given mass of liquid at a given temperature is "
    "proportional to the pressure of the gas above it. Sealing under high pressure keeps more CO₂ dissolved; "
    "when the bottle is opened the pressure falls and gas escapes as bubbles.",
    ["Solubility of a gas ∝ its partial pressure (Henry's law)", "High pressure → more CO₂ dissolved"],
    why="Higher pressure raises, not lowers, the solubility of a gas. The purpose is not to change the boiling "
        "point or to prevent a reaction.",
    ncert=f"{REF6}, equilibrium in physical processes: dissolution of gases in liquids", seconds=20)

add("Physical equilibria and Henry's law", B, "direct",
    "Which of the following substances can set up a solid ⇌ vapour equilibrium (it sublimes) when kept in a "
    "closed vessel and warmed gently?",
    Opts("A", "Camphor", ["Sodium chloride", "Sugar", "Copper sulphate"]),
    "Solid–vapour equilibrium (sublimation)",
    "NCERT gives iodine, camphor and ammonium chloride as substances that pass directly from the solid to the "
    "vapour; in a closed vessel the solid and its vapour reach a dynamic equilibrium.",
    ["Camphor(solid) ⇌ camphor(vapour)"],
    why="Sodium chloride, sugar and copper sulphate do not sublime on gentle warming.",
    ncert=f"{REF6}, equilibrium in physical processes: solid–vapour equilibrium", seconds=20)

ph_b3 = -math.log10(2.0e-3)
assert close(ph_b3, 2.70, 0.002)
add("Acids, bases and pH", B, "numerical",
    "The pH of a 2.0 × 10⁻³ M aqueous solution of hydrochloric acid at 298 K, assuming complete ionisation, is "
    "(log 2 = 0.30):",
    Opts("B", "2.70", ["3.30", "11.30", "2.30"]),
    "pH of a strong acid, pH = −log[H₃O⁺]",
    "HCl ionises completely, so [H₃O⁺] equals the concentration of the acid.",
    ["[H₃O⁺] = 2.0 × 10⁻³ M", "pH = −log(2.0 × 10⁻³) = 3 − log 2 = 3 − 0.30 = 2.70"],
    why="3.30 adds log 2 instead of subtracting it. 11.30 is 14 − 2.70, the pOH. 2.30 uses log 5 instead of "
        "log 2.",
    ncert=f"{REF6}, the pH scale", seconds=30, checked=True)

kp_b4 = 0.6 ** 2 / 0.4
assert close(kp_b4, 0.90) and close(0.6 / 0.4, 1.5) and close(0.4 / 0.36, 1.11, 0.01)
add("Kp, Kc and Le Chatelier", B, "numerical",
    "At equilibrium at a certain temperature, the partial pressures in the reaction N₂O₄(g) ⇌ 2NO₂(g) are "
    "p(N₂O₄) = 0.40 bar and p(NO₂) = 0.60 bar. K_p for the reaction at this temperature is:",
    Opts("A", "0.90 bar", ["1.5 bar", "1.11 bar⁻¹", "0.90 bar⁻¹"]),
    "Writing and evaluating K_p",
    "K_p = p²(NO₂)/p(N₂O₄); the coefficient 2 becomes a power, and the unit is bar²/bar = bar.",
    ["K_p = (0.60)² / 0.40 = 0.36/0.40 = 0.90 bar"],
    why="1.5 bar forgets to square p(NO₂). 1.11 bar⁻¹ inverts the expression. 0.90 bar⁻¹ has the right number "
        "but the wrong unit (Δn = +1, so the unit is bar).",
    ncert=f"{REF6}, equilibrium constant in gaseous systems", seconds=35, checked=True)

add("Acids, bases and pH", B, "direct",
    "Which of the following species can act as a Lewis acid?",
    Opts("D", "Mg²⁺", ["NH₃", "OH⁻", "H₂O"]),
    "Lewis acids are electron-pair acceptors",
    "Metal cations such as Mg²⁺ and Co³⁺ can accept electron pairs (from water molecules or other ligands) and "
    "so are Lewis acids. NH₃, OH⁻ and H₂O have lone pairs that they donate: they are Lewis bases.",
    ["Mg²⁺: electron-deficient cation → accepts electron pairs → Lewis acid",
     "NH₃, OH⁻, H₂O: lone-pair donors → Lewis bases"],
    why="NH₃, OH⁻ and H₂O are given in NCERT as examples of Lewis bases.",
    ncert=f"{REF6}, Lewis acids and bases", seconds=25)

alpha_p = math.sqrt(0.45 / (0.45 + 0.8))
assert close(alpha_p, 0.6) and close(alpha_p ** 2, 0.36) and close(math.sqrt(0.45 / 0.8), 0.75)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "For PCl₅(g) ⇌ PCl₃(g) + Cl₂(g), K_p = 0.45 atm at a certain temperature. Pure PCl₅ is allowed to reach "
    "equilibrium at this temperature, and the total pressure at equilibrium is 0.80 atm. The degree of "
    "dissociation of PCl₅ is:",
    Opts("C", "0.60", ["0.36", "0.75", "0.40"]),
    "Relating K_p to the degree of dissociation and the total pressure",
    "Start with 1 mol PCl₅; at equilibrium there are (1 − α) mol PCl₅, α mol PCl₃ and α mol Cl₂, total (1 + α). "
    "Partial pressures are mole fractions × P.",
    ["p(PCl₃) = p(Cl₂) = αP/(1 + α); p(PCl₅) = (1 − α)P/(1 + α)", "K_p = α²P/(1 − α²)",
     "0.45 = 0.80 α²/(1 − α²) → α² = 0.45/(0.45 + 0.80) = 0.36", "α = 0.60"],
    why="0.36 is α², not α. 0.75 uses K_p = α²P (forgets the 1 − α² term). 0.40 is 1 − α, the fraction left "
        "undissociated.",
    ncert=f"{REF6}, equilibrium constant in gaseous systems; applications of equilibrium constants",
    seconds=90, checked=True)

n_h = 1e-13 * 1e-3
assert close(n_h * NA, 6.022e7) and close(1e-13 * NA, 6.022e10) and close(0.1 * 1e-3 * NA, 6.022e19)
add("Acids, bases and pH", I, "numerical",
    "The number of H₃O⁺ ions present in 1.0 mL of an aqueous solution of pH 13 at 298 K is "
    "(Nₐ = 6.0 × 10²³ mol⁻¹):",
    Opts("A", "6.0 × 10⁷", ["6.0 × 10¹⁰", "6.0 × 10¹⁹", "1.0 × 10⁻¹⁶"]),
    "From pH to concentration to number of ions",
    "pH 13 means [H₃O⁺] = 10⁻¹³ mol L⁻¹. Convert the volume to litres, find the moles and multiply by Nₐ.",
    ["[H₃O⁺] = 10⁻¹³ mol L⁻¹", "In 1.0 mL = 10⁻³ L: 10⁻¹³ × 10⁻³ = 10⁻¹⁶ mol",
     "Number = 10⁻¹⁶ × 6.0 × 10²³ = 6.0 × 10⁷"],
    why="6.0 × 10¹⁰ is the number in one litre (mL not converted). 6.0 × 10¹⁹ counts OH⁻ ions (0.1 M) instead "
        "of H₃O⁺. 1.0 × 10⁻¹⁶ is the amount in moles, not the number of ions.",
    ncert=f"{REF6}, the pH scale", seconds=50, checked=True)

add("Solubility product", I, "assertion_reason",
    ar("Calcium phosphate, a salt of a weak acid, is more soluble in an acidic solution than in pure water.",
       "In acid, phosphate ions are protonated, which lowers their concentration, so more of the salt dissolves "
       "before the ionic product again equals K_sp."),
    AR_, "Effect of pH on the solubility of salts of weak acids",
    "NCERT notes that the solubility of salts of weak acids such as phosphates increases at lower pH: the anion "
    "is protonated, its concentration falls, the ionic product drops below K_sp and more salt dissolves until "
    "Q_sp = K_sp again. R is the reason for A.",
    ["A: phosphate salt dissolves more at low pH → true",
     "R: PO₄³⁻ + H⁺ → HPO₄²⁻ … lowers [PO₄³⁻] → more dissolves → true and explains A"],
    answer="A",
    why="Both statements are true and the protonation of the anion described in R is exactly why the solubility "
        "rises in acid.",
    ncert=f"{REF6}, solubility equilibria: common ion effect and effect of pH on solubility", seconds=40)

truth6 = {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Acids, bases and pH", I, "multi_statement",
    ms("Which of the following statements are correct at 298 K?",
       ["In aqueous solution, the proton exists as the hydronium ion, H₃O⁺, and not as a bare H⁺ ion.",
        "Human blood is slightly basic, with a pH of about 7.4.",
        "Gastric juice is basic.",
        "Milk of magnesia is acidic.",
        "Lemon juice is more acidic than black coffee."]),
    multi("B", truth6, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (b) only"]),
    "The hydronium ion and the pH of some common fluids",
    "A bare proton is very reactive and attaches to a water molecule, giving H₃O⁺. Blood has pH about 7.4 "
    "(slightly basic); gastric juice is strongly acidic (pH about 1.2); milk of magnesia is basic (pH about "
    "10); lemon juice (pH about 2.2) is more acidic than black coffee (pH about 5).",
    ["(a) ✓", "(b) ✓", "(c) ✗ strongly acidic", "(d) ✗ basic", "(e) ✓"],
    why="(c) and (d) reverse the nature of gastric juice and milk of magnesia; '(a) and (b) only' misses (e).",
    ncert=f"{REF6}, Arrhenius concept (hydronium ion); the pH scale (pH of some common substances)", seconds=50)

oh = {"A": 1e-14 / 1e-3, "B": 1e-14 / 1e-9, "C": 1e-4, "D": 1e-14 / 1e-7}
assert all(close(v, w) for v, w in zip(oh.values(), (1e-11, 1e-5, 1e-4, 1e-7)))
add("Acids, bases and pH", I, "match_list",
    lists("Match List-I (aqueous solution at 298 K) with List-II (its hydroxide ion concentration). "
          "(K_w = 1.0 × 10⁻¹⁴)",
          ["A solution of pH 3", "A solution of pH 9", "A solution of pOH 4",
           "A solution in which [H₃O⁺] = 1.0 × 10⁻⁷ M"],
          ["1.0 × 10⁻⁴ M", "1.0 × 10⁻⁷ M", "1.0 × 10⁻¹¹ M", "1.0 × 10⁻⁵ M"]),
    match("B", M("III IV I II"), [M("IV III I II"), M("III I IV II"), M("III IV II I")]),
    "pH, pOH and K_w",
    "At 298 K, pH + pOH = 14 and [OH⁻] = 10^(−pOH).",
    ["pH 3 → pOH 11 → 10⁻¹¹ M → III", "pH 9 → pOH 5 → 10⁻⁵ M → IV", "pOH 4 → 10⁻⁴ M → I",
     "[H₃O⁺] = 10⁻⁷ → [OH⁻] = 10⁻⁷ M → II"],
    why="The wrong codes give [H₃O⁺] instead of [OH⁻] for one of the solutions, or swap pH 9 with pOH 4.",
    ncert=f"{REF6}, ionisation constant of water and the pH scale", seconds=50, checked=True)

add("Physical equilibria and Henry's law", I, "statement_pair",
    sp("At high altitudes, water boils at a higher temperature than at sea level.",
       "At a given temperature, of two liquids the one with the higher vapour pressure has the lower boiling "
       "point."),
    SP_, "Liquid–vapour equilibrium and boiling point",
    "A liquid boils when its vapour pressure equals the external pressure. At high altitude the atmospheric "
    "pressure is lower, so this happens at a LOWER temperature: Statement I is false. A liquid that already has "
    "a higher vapour pressure at a given temperature reaches the external pressure sooner on heating, so it "
    "boils at a lower temperature: Statement II is true.",
    ["I: lower atmospheric pressure → lower boiling point → false",
     "II: higher vapour pressure → more volatile → lower boiling point → true"],
    answer="D",
    why="Statement I reverses the effect of pressure on the boiling point.",
    ncert=f"{REF6}, equilibrium in physical processes: liquid–vapour equilibrium", seconds=35)

add("Kp, Kc and Le Chatelier", I, "assertion_reason",
    ar("For the equilibrium N₂(g) + O₂(g) ⇌ 2NO(g), ΔH > 0, raising the temperature increases the amount of NO "
       "at equilibrium.",
       "Raising the temperature increases the equilibrium constant of every reaction."),
    AR_, "Effect of temperature on equilibrium (Le Chatelier's principle)",
    "For an endothermic reaction, a rise in temperature is absorbed by shifting the equilibrium forward, so K "
    "increases and more NO forms: A is true. But for an exothermic reaction K DECREASES with rise in "
    "temperature, so R, which claims this for every reaction, is false.",
    ["A: endothermic → higher T favours products → true", "R: K falls with T for exothermic reactions → false"],
    answer="C",
    why="R is a false generalisation, so options A and B are wrong; A itself is true, so option D is wrong.",
    ncert=f"{REF6}, factors affecting equilibria: effect of temperature", seconds=40)

kp_carb = 2.0 ** 2 * 1.0
assert kp_carb == 4.0 and 2.0 * 1.0 == 2.0 and close(1.5 ** 3, 3.375)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "Solid ammonium carbamate is placed in an evacuated vessel and allowed to reach equilibrium at a certain "
    "temperature: NH₂COONH₄(s) ⇌ 2NH₃(g) + CO₂(g). The total pressure at equilibrium is 3.0 atm. K_p for the "
    "equilibrium is:",
    Opts("D", "4.0 atm³", ["2.0 atm³", "3.375 atm³", "27 atm³"]),
    "K_p for a heterogeneous equilibrium in which the gases come only from the solid",
    "The solid does not appear in K_p. Because the gases are formed in the ratio 2 : 1, p(NH₃) = 2p(CO₂); the "
    "two partial pressures add up to the total pressure.",
    ["p(NH₃) + p(CO₂) = 3p(CO₂) = 3.0 atm → p(CO₂) = 1.0 atm, p(NH₃) = 2.0 atm",
     "K_p = p²(NH₃) × p(CO₂) = (2.0)² × 1.0 = 4.0 atm³"],
    why="2.0 atm³ forgets to square p(NH₃). 3.375 atm³ shares the pressure equally (1.5 atm each), ignoring "
        "the 2 : 1 ratio. 27 atm³ cubes the total pressure.",
    ncert=f"{REF6}, heterogeneous equilibria", seconds=70, checked=True)

ka_a2 = 1e-5
c_new = (1e-4) ** 2 / ka_a2
assert close(math.sqrt(ka_a2 * 0.1), 1e-3) and close(c_new, 1e-3) and close(0.1 / c_new, 100)
add("Acids, bases and pH", A, "numerical",
    "A 0.10 M aqueous solution of a weak monobasic acid HA (K_a = 1.0 × 10⁻⁵) is diluted with water at 298 K. "
    "Using [H₃O⁺] ≈ √(K_a c), by what factor must the solution be diluted to raise its pH by exactly one unit?",
    Opts("C", "100 times", ["10 times", "1000 times", "√10 ≈ 3.2 times"]),
    "Dilution of a weak acid: [H₃O⁺] varies as √c",
    "Raising the pH by one unit means lowering [H₃O⁺] ten times. For a weak acid [H₃O⁺] ∝ √c, so the "
    "concentration must fall 10² = 100 times.",
    ["Initially [H₃O⁺] = √(10⁻⁵ × 0.1) = 10⁻³ M (pH 3)", "Target pH 4: [H₃O⁺] = 10⁻⁴ M",
     "c = [H₃O⁺]²/K_a = 10⁻⁸/10⁻⁵ = 10⁻³ M", "Dilution factor = 0.1/10⁻³ = 100"],
    why="10 times would be enough for a STRONG acid, whose [H₃O⁺] is proportional to c. 1000 times overshoots "
        "(pH would rise by 1.5). √10 times raises the pH by only 0.25.",
    ncert=f"{REF6}, ionisation of weak acids", seconds=90, checked=True)

truth6a = {"a": True, "b": True, "c": False, "d": True, "e": False}
add("Kp, Kc and Le Chatelier", A, "multi_statement",
    ms("For the equilibrium CO(g) + 2H₂(g) ⇌ CH₃OH(g), ΔH < 0, set up in a closed vessel, which of the "
       "following statements are correct?",
       ["K_p = K_c (RT)⁻².",
        "Compressing the mixture to a smaller volume at constant temperature increases the amount of CH₃OH at "
        "equilibrium.",
        "Raising the temperature increases the equilibrium constant.",
        "The unit of K_c is L² mol⁻².",
        "Adding a catalyst increases the amount of CH₃OH at equilibrium."]),
    multi("A", truth6a, ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "K_p–K_c relation, units of K and Le Chatelier's principle",
    "Δn(gas) = 1 − 3 = −2, so K_p = K_c(RT)⁻² and K_c = [CH₃OH]/([CO][H₂]²) has the unit (mol L⁻¹)⁻² = "
    "L² mol⁻². Compression favours the side with fewer gas molecules (CH₃OH). The reaction is exothermic, so K "
    "falls when the temperature rises. A catalyst only helps the system reach equilibrium faster.",
    ["(a) Δn = −2 ✓", "(b) 3 mol gas → 1 mol gas favoured at higher pressure ✓", "(c) exothermic → K falls ✗",
     "(d) ✓", "(e) catalyst does not shift equilibrium ✗"],
    why="Options containing (c) or (e) are wrong; '(a) and (d) only' leaves out the pressure effect (b).",
    ncert=f"{REF6}, relationship between K_p and K_c; factors affecting equilibria", seconds=80)

s_ba = 1.0e-10 / 0.01
assert close(s_ba * 233, 2.33e-6) and close(math.sqrt(1.0e-10) * 233, 2.33e-3) \
    and close(1.0e-10 / 0.01 ** 2 * 233, 2.33e-4)
add("Solubility product", A, "numerical",
    "K_sp of BaSO₄ at 298 K is 1.0 × 10⁻¹⁰. The mass of BaSO₄ that can dissolve in 1.0 L of a 0.010 M Na₂SO₄ "
    "solution at 298 K is (molar mass of BaSO₄ = 233 g mol⁻¹; Na₂SO₄ is completely dissociated):",
    Opts("B", "2.33 × 10⁻⁶ g", ["2.33 × 10⁻³ g", "1.0 × 10⁻⁸ g", "2.33 × 10⁻⁴ g"]),
    "Common ion effect on solubility",
    "The sulphate from Na₂SO₄ (0.010 M) swamps the tiny amount from BaSO₄, so [SO₄²⁻] ≈ 0.010 M and the "
    "solubility s = [Ba²⁺] = K_sp/0.010.",
    ["K_sp = [Ba²⁺][SO₄²⁻] = s × 0.010", "s = 1.0 × 10⁻¹⁰ / 0.010 = 1.0 × 10⁻⁸ mol L⁻¹",
     "Mass in 1.0 L = 1.0 × 10⁻⁸ × 233 = 2.33 × 10⁻⁶ g"],
    why="2.33 × 10⁻³ g is the solubility in pure water (s = √K_sp), ignoring the common ion. 1.0 × 10⁻⁸ g is "
        "the amount in moles written as grams. 2.33 × 10⁻⁴ g divides K_sp by (0.010)².",
    ncert=f"{REF6}, common ion effect in the ionisation of salts", seconds=80, checked=True)

ph_buf = 4.74 + math.log10(0.095 / 0.105)
assert close(4.74 - ph_buf, 0.0435, 0.02) and 4.74 - ph_buf < 0.05 and close(-math.log10(0.005), 2.30, 0.002)
add("Hydrolysis and buffers", A, "statement_pair",
    sp("Adding 0.005 mol of HCl to 1 L of a buffer containing 0.10 mol of CH₃COOH and 0.10 mol of CH₃COONa "
       "(pK_a = 4.74) lowers its pH by less than 0.05 unit (log (19/21) = −0.043).",
       "Adding 0.005 mol of HCl to 1 L of pure water at 298 K lowers its pH from 7 to about 2.3 "
       "(log 5 = 0.70)."),
    SP_, "Buffer action compared with unbuffered water",
    "In the buffer, the added H⁺ converts 0.005 mol CH₃COO⁻ into CH₃COOH: the ratio becomes 0.095/0.105 = 19/21 "
    "and pH = 4.74 − 0.043 = 4.70, a drop of only 0.043. Statement I is true. In water, [H₃O⁺] becomes "
    "5 × 10⁻³ M and pH = 3 − 0.70 = 2.30, a drop of nearly 5 units. Statement II is true.",
    ["I: pH = 4.74 + log(0.095/0.105) = 4.74 − 0.043 = 4.70 → drop < 0.05 → true",
     "II: [H₃O⁺] = 0.005 M → pH 2.30 → true"],
    answer="A",
    why="Both statements hold; together they show how strongly the buffer resists the change in pH.",
    ncert=f"{REF6}, buffer solutions (Henderson–Hasselbalch equation)", seconds=90, checked=True)
