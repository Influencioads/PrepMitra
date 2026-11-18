

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

cp_m = 75 / (2.0 * 1.5)
assert close(cp_m, 25) and close(75 / 1.5, 50) and close(75 / 2, 37.5) and close(cp_m - R_J, 16.7, 0.002)
add("First law, work and enthalpy", B, "numerical",
    "When 75 J of heat is supplied at constant pressure to 2.0 mol of a gas, its temperature rises by 1.5 K. "
    "The molar heat capacity of the gas at constant pressure, C_p,m, is:",
    Opts("A", "25 J K⁻¹ mol⁻¹", ["50 J K⁻¹ mol⁻¹", "37.5 J K⁻¹ mol⁻¹", "16.7 J K⁻¹ mol⁻¹"]),
    "Molar heat capacity: q = n C_m ΔT",
    "At constant pressure the heat supplied is q_p = n C_p,m ΔT, so C_p,m = q/(n ΔT).",
    ["C_p,m = 75 J / (2.0 mol × 1.5 K)", "C_p,m = 25 J K⁻¹ mol⁻¹"],
    why="50 J K⁻¹ mol⁻¹ is the heat capacity of the whole 2.0 mol sample, not per mole. "
        "37.5 divides by the amount but not by ΔT. 16.7 subtracts R, which would give C_v,m for an ideal gas, "
        "not C_p,m.",
    ncert=f"{REF4}, heat capacity; molar heat capacity", seconds=30, checked=True)

add("First law, work and enthalpy", B, "direct",
    "According to NCERT, which of the following is an example of a CLOSED system?",
    Opts("C", "Reactants placed in a closed vessel made of a conducting material such as copper or steel",
         ["Reactants placed in an open beaker",
          "Reactants placed in a thermos flask or any other closed, insulated vessel",
          "A living plant growing in the open air"]),
    "Open, closed and isolated systems",
    "A closed system can exchange energy but not matter with its surroundings. A sealed vessel made of a "
    "conducting metal lets heat pass through its walls but keeps the matter in.",
    ["Closed: energy exchanged, matter not → sealed conducting vessel",
     "Open beaker / plant: matter and energy both exchanged → open",
     "Thermos flask: neither exchanged → isolated"],
    why="An open beaker and a plant exchange matter with the surroundings (open systems). A closed, insulated "
        "vessel exchanges neither matter nor energy (isolated system).",
    ncert=f"{REF4}, types of the system", seconds=25)

add("First law, work and enthalpy", B, "assertion_reason",
    ar("Enthalpy is an extensive property.",
       "Enthalpy is a state function."),
    AR_, "Extensive properties versus state functions",
    "A is true: the enthalpy of a system depends on the amount of matter in it (doubling the system doubles H). "
    "R is also true: H depends only on the state of the system, not on how that state was reached. But being a "
    "state function has nothing to do with depending on the amount of matter — temperature and pressure are "
    "state functions too, yet they are intensive. So R does not explain A.",
    ["A: H depends on the amount of matter → extensive → true",
     "R: H = U + pV depends only on the state → true",
     "Temperature is a state function but intensive → 'state function' does not imply 'extensive' → option B"],
    answer="B",
    why="Option A would need state-function behaviour to make a property extensive, which the example of "
        "temperature disproves; both statements are true, so C and D are out.",
    ncert=f"{REF4}, extensive and intensive properties; state functions", seconds=40)

heat = 0.010 * 3200
c_cal = heat / 4.0
assert close(c_cal, 8.0) and close(heat * 4.0, 128) and close(3200 / 4.0, 800)
add("First law, work and enthalpy", I, "numerical",
    "A bomb calorimeter is calibrated by burning 0.010 mol of a standard substance whose internal energy of "
    "combustion is ΔcU = −3200 kJ mol⁻¹. The temperature of the calorimeter rises by 4.0 K. The heat capacity of "
    "the calorimeter is:",
    Opts("D", "8.0 kJ K⁻¹", ["128 kJ K⁻¹", "800 kJ K⁻¹", "0.80 kJ K⁻¹"]),
    "Bomb calorimetry: heat released at constant volume = C_calorimeter × ΔT",
    "At constant volume the heat given out by the combustion is −ΔU and it all goes into the calorimeter, so "
    "C = q/ΔT.",
    ["q = 0.010 mol × 3200 kJ mol⁻¹ = 32 kJ", "C = 32 kJ / 4.0 K = 8.0 kJ K⁻¹"],
    why="128 kJ K⁻¹ multiplies the heat by ΔT instead of dividing. 800 kJ K⁻¹ uses the molar value without "
        "multiplying by 0.010 mol. 0.80 kJ K⁻¹ slips a power of ten.",
    ncert=f"{REF4}, measurement of ΔU: calorimetry", seconds=45, checked=True)

add("Entropy and Gibbs energy", I, "statement_pair",
    sp("For every reaction that involves gases, ΔH is greater than ΔU.",
       "A reaction in which the entropy of the system decreases can never be spontaneous."),
    SP_, "ΔH–ΔU relation and the criteria of spontaneity",
    "ΔH = ΔU + Δn_g RT, so ΔH > ΔU only when the number of moles of gas increases; when Δn_g = 0 they are equal "
    "and when Δn_g < 0, ΔH < ΔU. A reaction with ΔS(system) < 0 can still be spontaneous if it is exothermic "
    "enough that ΔG = ΔH − TΔS is negative (low temperature), because the surroundings gain entropy.",
    ["I: depends on the sign of Δn_g; e.g. N₂ + 3H₂ → 2NH₃ has ΔH < ΔU → false",
     "II: ΔH < 0 and ΔS < 0 → spontaneous below T = ΔH/ΔS → false"],
    answer="B",
    why="Statement I ignores reactions with Δn_g ≤ 0, and Statement II ignores the entropy gained by the "
        "surroundings from the heat released.",
    ncert=f"{REF4}, enthalpy (ΔH and ΔU); Gibbs energy and spontaneity", seconds=45)

add("Gibbs energy and K", I, "match_list",
    lists("Match List-I (situation) with List-II (thermodynamic condition that describes it).",
          ["A spontaneous process at constant temperature and pressure",
           "A spontaneous change in an isolated system",
           "A system at equilibrium at constant temperature and pressure",
           "A reaction whose standard Gibbs energy change, ΔrG°, is zero"],
          ["ΔG = 0", "K = 1", "ΔS > 0", "ΔG < 0"]),
    match("A", M("IV III I II"), [M("III IV I II"), M("IV III II I"), M("I III IV II")]),
    "Criteria for spontaneity and equilibrium",
    "At constant T and p, ΔG < 0 for a spontaneous process and ΔG = 0 at equilibrium. In an isolated system "
    "(no exchange of energy), a spontaneous change increases the entropy. ΔrG° = −2.303 RT log K, so ΔrG° = 0 "
    "means log K = 0 and K = 1.",
    ["A → ΔG < 0 → IV", "B → ΔS > 0 → III", "C → ΔG = 0 → I", "D → log K = 0 → K = 1 → II"],
    why="A-III/B-IV swaps the criteria for constant T, p and for an isolated system. C-II/D-I confuses ΔG = 0 "
        "with ΔG° = 0. A-I/C-IV swaps spontaneity and equilibrium.",
    ncert=f"{REF4}, entropy and spontaneity; Gibbs energy change and equilibrium", seconds=50)

add("Gibbs energy and K", I, "assertion_reason",
    ar("A reaction with a large positive standard Gibbs energy change, ΔrG°, has an equilibrium constant much "
       "smaller than 1.",
       "ΔrG° = −2.303 RT log K."),
    AR_, "Relation between ΔrG° and K",
    "From ΔrG° = −2.303 RT log K, log K = −ΔrG°/(2.303 RT). A large positive ΔrG° makes log K large and "
    "negative, so K ≪ 1: at equilibrium the mixture contains mostly reactants. R is the relation from which A "
    "follows.",
    ["log K = −ΔrG°/2.303RT", "ΔrG° ≫ 0 → log K ≪ 0 → K ≪ 1", "R explains A"],
    answer="A",
    why="The equation in R is the direct cause of A, so 'not the correct explanation' does not apply.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=35)

dh_gas = 436 + 498 / 2 - 2 * 464
dh_liq = dh_gas - 44
assert dh_gas == -243 and dh_liq == -287 and -243 + 44 == -199 and 436 + 498 - 928 - 44 == -38
add("Hess's law and enthalpies", A, "numerical",
    "Use the mean bond enthalpies H–H = 436, O=O = 498 and O–H = 464 kJ mol⁻¹, and the enthalpy of vaporisation "
    "of water at 298 K, 44 kJ mol⁻¹, to estimate the standard enthalpy of formation of LIQUID water, "
    "H₂(g) + ½O₂(g) → H₂O(l):",
    Opts("C", "−287 kJ mol⁻¹", ["−243 kJ mol⁻¹", "−199 kJ mol⁻¹", "−38 kJ mol⁻¹"]),
    "Reaction enthalpy from bond enthalpies (valid for gases only) plus a phase-change step (Hess's law)",
    "The bond-enthalpy relation ΔrH = Σ(bonds broken) − Σ(bonds formed) applies only when all species are "
    "gases, so it gives the formation of H₂O(g). Then add the enthalpy of condensation of water (−44 kJ mol⁻¹) "
    "to reach H₂O(l).",
    ["Bonds broken: H–H + ½ O=O = 436 + 249 = 685 kJ", "Bonds formed: 2 O–H = 2 × 464 = 928 kJ",
     "H₂(g) + ½O₂(g) → H₂O(g): 685 − 928 = −243 kJ", "H₂O(g) → H₂O(l): −44 kJ",
     "ΔfH°(H₂O, l) ≈ −243 − 44 = −287 kJ mol⁻¹"],
    why="−243 kJ mol⁻¹ stops at water vapour. −199 kJ mol⁻¹ adds the enthalpy of vaporisation with the wrong "
        "sign (condensation releases heat). −38 kJ mol⁻¹ breaks a whole O=O bond instead of half of one.",
    ncert=f"{REF4}, bond enthalpy; Hess's law; enthalpy of phase transformation", seconds=100, checked=True)

truth_so3 = {"a": True, "b": True, "c": True, "d": False, "e": False}
dng = 2 - 3
assert dng == -1
add("Entropy and Gibbs energy", A, "multi_statement",
    ms("For the exothermic reaction 2SO₂(g) + O₂(g) → 2SO₃(g), carried out at constant temperature and pressure "
       "with the gases behaving ideally, which of the following statements are correct?",
       ["ΔH is more negative than ΔU.",
        "The entropy of the system decreases.",
        "Work is done ON the system by the surroundings (w is positive).",
        "The reaction becomes more favourable (ΔG more negative) as the temperature is raised, assuming ΔH and "
        "ΔS stay constant.",
        "The heat given out at constant pressure is equal to −ΔU."]),
    multi("B", truth_so3, ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (d) only"]),
    "ΔH = ΔU + Δn_g RT; entropy, work and Gibbs energy for a gas-phase reaction",
    "Δn_g = 2 − 3 = −1. The gas volume shrinks, the entropy of the system falls, and the surroundings push the "
    "system in.",
    ["(a) ΔH = ΔU − RT → ΔH more negative ✓", "(b) 3 mol gas → 2 mol gas → ΔS < 0 ✓",
     "(c) volume decreases → w = −p ΔV > 0 ✓",
     "(d) ΔG = ΔH − TΔS with ΔH < 0, ΔS < 0: −TΔS is positive and grows with T → less favourable ✗",
     "(e) heat at constant pressure = −ΔH, not −ΔU ✗"],
    why="(d) reverses the effect of temperature when ΔS is negative, and (e) confuses q_p (ΔH) with q_v (ΔU); "
        "any option including either is wrong, and '(a) and (d) only' also misses (b) and (c).",
    ncert=f"{REF4}, enthalpy; work; Gibbs energy and spontaneity", seconds=100, checked=True)

add("Entropy and Gibbs energy", A, "direct",
    "An ideal gas in a thermally insulated, rigid container is allowed to expand from one half of the container "
    "into the other, evacuated half (the whole container being an isolated system). Which set of values is "
    "correct for this free expansion?",
    Opts("D", "w = 0, q = 0, ΔU = 0, ΔS > 0",
         ["w = 0, q = 0, ΔU = 0, ΔS = 0", "w < 0, q = 0, ΔU < 0, ΔS > 0", "w = 0, q > 0, ΔU > 0, ΔS > 0"]),
    "Free expansion of an ideal gas; entropy change in an isolated system",
    "Against zero external pressure the gas does no work (w = 0). The container is insulated (q = 0), so "
    "ΔU = q + w = 0 and the temperature of the ideal gas stays the same. The expansion is spontaneous in an "
    "isolated system, so the entropy increases.",
    ["p_ex = 0 → w = 0", "Insulated → q = 0", "ΔU = q + w = 0",
     "Spontaneous change in an isolated system → ΔS > 0"],
    why="ΔS = 0 would mean the expansion is not spontaneous, but gases spread into a vacuum on their own. w < 0 "
        "would need an external pressure to push against. q > 0 is impossible with insulated walls.",
    ncert=f"{REF4}, free expansion; entropy and spontaneity", seconds=60)
