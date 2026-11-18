

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

rate_b1 = 2.0e-2 * 0.50
assert close(rate_b1, 1.0e-2) and close(2.0e-2 / 0.50, 4.0e-2) and close(2.0e-2 * 0.25, 5.0e-3)
add("Rate law and order", B, "numerical",
    "A first-order reaction A → products has a rate constant of 2.0 × 10⁻² s⁻¹. Its rate at the moment when "
    "[A] = 0.50 mol L⁻¹ is:",
    Opts("D", "1.0 × 10⁻² mol L⁻¹ s⁻¹", ["4.0 × 10⁻² mol L⁻¹ s⁻¹", "5.0 × 10⁻³ mol L⁻¹ s⁻¹",
                                         "2.0 × 10⁻² mol L⁻¹ s⁻¹"]),
    "Rate law of a first-order reaction, rate = k[A]",
    "For a first-order reaction the rate is the rate constant multiplied by the concentration of the reactant "
    "at that moment.",
    ["Rate = k[A] = 2.0 × 10⁻² s⁻¹ × 0.50 mol L⁻¹", "= 1.0 × 10⁻² mol L⁻¹ s⁻¹"],
    why="4.0 × 10⁻² divides k by [A]. 5.0 × 10⁻³ uses [A]² (second order). 2.0 × 10⁻² takes the rate equal to k, "
        "which is true only when [A] = 1 mol L⁻¹.",
    ncert=f"{REF8}, rate expression and rate constant", seconds=25, checked=True)

c_b2 = 0.10 - 2.0e-3 * 20
assert close(c_b2, 0.06) and close(0.10 * math.exp(-2.0e-3 * 20), 0.0961, 0.002)
add("Zero and first order reactions", B, "numerical",
    "A zero-order reaction R → P has a rate constant of 2.0 × 10⁻³ mol L⁻¹ s⁻¹. If the initial concentration of "
    "R is 0.10 mol L⁻¹, its concentration after 20 s is:",
    Opts("A", "0.060 mol L⁻¹", ["0.040 mol L⁻¹", "0.140 mol L⁻¹", "0.096 mol L⁻¹"]),
    "Integrated rate equation of a zero-order reaction, [R] = [R]₀ − kt",
    "For a zero-order reaction the concentration falls linearly with time at the rate k.",
    ["[R] = 0.10 − (2.0 × 10⁻³ × 20)", "= 0.10 − 0.040 = 0.060 mol L⁻¹"],
    why="0.040 mol L⁻¹ is the amount that has reacted, not the amount left. 0.140 mol L⁻¹ adds kt. "
        "0.096 mol L⁻¹ uses the first-order equation [R] = [R]₀e^(−kt).",
    ncert=f"{REF8}, integrated rate equations: zero order reactions", seconds=30, checked=True)

add("Rate law and order", B, "direct",
    "At a given temperature, the rate constant of a reaction does NOT depend on:",
    Opts("B", "the concentrations of the reactants", ["the temperature", "the presence of a catalyst",
                                                    "the nature of the reaction"]),
    "Rate versus rate constant",
    "The rate of a reaction changes as the concentrations change, but the rate constant k is fixed for a given "
    "reaction at a given temperature. It changes with temperature (Arrhenius equation) and when a catalyst "
    "provides a path of lower activation energy.",
    ["Rate = k[A]ˣ[B]ʸ: the concentration dependence is in the concentration terms, not in k",
     "k = A e^(−Ea/RT): depends on T and Ea (nature of reaction, catalyst)"],
    why="Temperature, a catalyst and the nature of the reaction all change the value of k.",
    ncert=f"{REF8}, rate expression and rate constant; temperature dependence of the rate of a reaction",
    seconds=25)

add("Arrhenius equation and activation energy", B, "match_list",
    lists("Match List-I (quantity) with List-II (its unit). (Concentrations in mol L⁻¹, time in s.)",
          ["Activation energy, Eₐ", "Pre-exponential factor, A, for a first-order reaction",
           "Rate of a reaction in solution", "Slope of the plot of ln k against 1/T"],
          ["K", "s⁻¹", "J mol⁻¹", "mol L⁻¹ s⁻¹"]),
    match("D", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("III IV II I")]),
    "Units in chemical kinetics",
    "Eₐ is an energy per mole. A has the same unit as k (s⁻¹ for first order). Rate is a change of "
    "concentration per unit time. The slope of ln k against 1/T is −Eₐ/R, whose unit is (J mol⁻¹)/(J K⁻¹ "
    "mol⁻¹) = K.",
    ["A → III", "B → II", "C → IV", "D → I"],
    why="The wrong codes swap the units of Eₐ and A, of the rate and the slope, or of A and the rate.",
    ncert=f"{REF8}, rate constant; temperature dependence (Arrhenius equation)", seconds=40)

add("Zero and first order reactions", I, "assertion_reason",
    ar("The decomposition of ammonia on a hot platinum surface at high pressure, 2NH₃(g) → N₂(g) + 3H₂(g), is a "
       "zero-order reaction.",
       "At high pressure the metal surface is saturated with ammonia molecules, so increasing the concentration "
       "of ammonia cannot increase the amount adsorbed on the surface, and the rate does not change."),
    AR_, "Zero-order surface reactions",
    "NCERT cites this reaction as zero order: the platinum surface acts as a catalyst, and at high pressure it is "
    "fully covered by gas molecules. The rate depends on the (fixed) amount on the surface, not on the "
    "ammonia concentration in the gas. R explains A.",
    ["A: rate = k[NH₃]⁰ = k → zero order → true", "R: surface saturated → rate independent of [NH₃] → true",
     "R is the cause of the zero order → option A"],
    answer="A",
    why="Both statements are true, and saturation of the catalyst surface is exactly why the order is zero.",
    ncert=f"{REF8}, zero order reactions", seconds=40)

t_i2 = 10 * math.log(1 / 0.64) / math.log(1 / 0.8)
assert close(t_i2, 20) and close(10 * math.log(0.64) / math.log(0.2), 2.77, 0.01)
add("Zero and first order reactions", I, "numerical",
    "A first-order reaction is 20% complete in 10 minutes. The time it takes to be 36% complete is:",
    Opts("C", "20 min", ["18 min", "2.8 min", "40 min"]),
    "Equal fractions react in equal times in a first-order reaction",
    "In each 10-minute interval the same fraction (20%) of the remaining reactant reacts, i.e. 80% is left. "
    "After two such intervals (0.8)² = 0.64 is left, which is 36% completion.",
    ["After 10 min: 0.80 of the reactant left", "After 20 min: 0.80 × 0.80 = 0.64 left → 36% reacted",
     "Check: t = (2.303/k) log(1/0.64) = 2 × (2.303/k) log(1/0.80)"],
    why="18 min scales the time in proportion to the percentage reacted (a zero-order assumption). 2.8 min uses "
        "the fraction reacted instead of the fraction left in the logarithm. 40 min squares the time instead of "
        "the fraction left.",
    ncert=f"{REF8}, integrated rate equations: first order reactions", seconds=70, checked=True)

truth8 = {"a": True, "b": True, "c": False, "d": False}
add("Arrhenius equation and activation energy", I, "multi_statement",
    ms("Which of the following statements about the energy profile of a reaction are correct?",
       ["The activation energy is the energy of the activated complex minus the energy of the reactants.",
        "For an exothermic reaction, the products lie lower in energy than the reactants.",
        "The activated complex is a stable species that can be isolated.",
        "A catalyst changes the enthalpy change of the reaction."]),
    multi("B", truth8, ["(a), (b) and (c) only", "(b) and (d) only", "(a) and (c) only"]),
    "Activated complex, activation energy and the effect of a catalyst",
    "The reaction passes through an unstable, short-lived activated complex at the top of the energy barrier; "
    "the height of this barrier above the reactants is Eₐ. In an exothermic reaction the products end below "
    "the reactants. A catalyst lowers the barrier (provides a new path) but leaves the energies of reactants "
    "and products, and so ΔH, unchanged.",
    ["(a) ✓", "(b) ✓", "(c) ✗ unstable, cannot be isolated", "(d) ✗ ΔH unchanged"],
    why="(c) and (d) are false; every option containing either of them is wrong.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction; effect of catalyst", seconds=45)

add("Rate law and order", I, "statement_pair",
    sp("The average rate of a reaction over a time interval equals its instantaneous rate at every moment in "
       "that interval.",
       "The rate of a reaction can be expressed as the rate of decrease of the concentration of a reactant, or "
       "the rate of increase of the concentration of a product, each divided by its stoichiometric coefficient."),
    SP_, "Average and instantaneous rates; expressing the rate of a reaction",
    "As reactants are used up the rate usually falls, so the instantaneous rate changes within an interval and "
    "the average rate equals it only at some instant (or when the rate is constant): Statement I is false. "
    "Statement II is how NCERT defines a single rate for a reaction such as 2HI → H₂ + I₂: "
    "rate = −½ d[HI]/dt = d[H₂]/dt = d[I₂]/dt.",
    ["I: instantaneous rate varies within the interval → false", "II: rate = −(1/a)d[A]/dt = (1/p)d[P]/dt → true"],
    answer="D",
    why="Statement I would be true only for a zero-order reaction, not in general.",
    ncert=f"{REF8}, rate of a chemical reaction", seconds=40)

add("Arrhenius equation and activation energy", I, "match_list",
    lists("Match List-I (change made) with List-II (its effect on the rate constant k of a reaction).",
          ["The temperature is raised", "A catalyst is added",
           "The concentration of a reactant is increased at constant temperature",
           "A second reaction with the same A but a higher Eₐ is compared at the same temperature"],
          ["k increases because the activation energy is lowered", "k does not change",
           "k increases because a larger fraction of molecules has energy ≥ Eₐ", "k is smaller"]),
    match("A", M("III I II IV"), [M("I III II IV"), M("III II I IV"), M("III I IV II")]),
    "Factors that change the rate constant",
    "k = A e^(−Eₐ/RT). Raising T increases the fraction e^(−Eₐ/RT) of molecules able to react. A catalyst "
    "provides a path of lower Eₐ. Concentration changes the rate, not k. A higher Eₐ with the same A and T "
    "gives a smaller k.",
    ["A → III", "B → I", "C → II", "D → IV"],
    why="The wrong codes give the catalyst's mechanism to temperature (and vice versa), or claim that "
        "concentration changes k.",
    ncert=f"{REF8}, temperature dependence of the rate; effect of catalyst", seconds=45)

ea_a1 = 19.15 * 1 / (1 / 300 - 1 / 320)
log_ratio = 91.9e3 / 19.15 * (1 / 300 - 1 / 320)
assert close(ea_a1, 91.9e3, 0.001) and close(10 ** log_ratio, 10, 0.01)
add("Arrhenius equation and activation energy", A, "numerical",
    "A reaction has an activation energy of 91.9 kJ mol⁻¹. Assuming the pre-exponential factor does not change, "
    "by about what factor does its rate constant increase when the temperature is raised from 300 K to 320 K? "
    "(2.303R = 19.15 J K⁻¹ mol⁻¹)",
    Opts("C", "10", ["4", "100", "2.7"]),
    "Arrhenius equation at two temperatures",
    "log(k₂/k₁) = [Eₐ/(2.303R)] × (1/T₁ − 1/T₂).",
    ["1/300 − 1/320 = 20/96 000 = 2.083 × 10⁻⁴ K⁻¹",
     "log(k₂/k₁) = (91 900/19.15) × 2.083 × 10⁻⁴ = 4799 × 2.083 × 10⁻⁴ = 1.00", "k₂/k₁ = 10"],
    why="4 applies the rough 'doubling for every 10 K' rule instead of the given Eₐ. 100 takes the logarithm as "
        "2. 2.7 treats the value 1.00 as the natural "
        "logarithm of the ratio (e¹ ≈ 2.7).",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=90, checked=True)

k_a2 = (0.80 - 0.20) / 30
t_half_a2 = 0.40 / (2 * k_a2)
assert close(k_a2, 0.020) and close(t_half_a2, 10) and close(0.20 / (2 * k_a2), 5) \
    and close(math.log(2) / (math.log(4) / 30), 15)
add("Half-life", A, "numerical",
    "For a zero-order reaction R → P at a constant temperature, the concentration of R falls from 0.80 mol L⁻¹ "
    "to 0.20 mol L⁻¹ in 30 minutes. The half-life of the same reaction when the initial concentration of R is "
    "0.40 mol L⁻¹ is:",
    Opts("B", "10 min", ["20 min", "15 min", "5 min"]),
    "Half-life of a zero-order reaction, t½ = [R]₀/2k",
    "First find k from the linear fall in concentration, then use the zero-order half-life with the NEW initial "
    "concentration.",
    ["k = (0.80 − 0.20)/30 = 0.020 mol L⁻¹ min⁻¹", "t½ = 0.40/(2 × 0.020) = 10 min"],
    why="20 min leaves out the factor 2 in t½ = [R]₀/2k. 15 min treats the reaction as first order (0.80 → 0.20 "
        "is two half-lives in 30 min). 5 min uses 0.20 mol L⁻¹ as the initial concentration.",
    ncert=f"{REF8}, zero order reactions; half-life of a reaction", seconds=80, checked=True)

add("Arrhenius equation and activation energy", A, "direct",
    "Two reactions have the same pre-exponential factor A, but the activation energy of reaction 1 is larger "
    "than that of reaction 2 (Eₐ₁ > Eₐ₂). Assuming A and Eₐ do not change with temperature, which statement "
    "about their rate constants k₁ and k₂ is correct?",
    Opts("D", "k₁ < k₂ at every temperature, and the ratio k₂/k₁ decreases as the temperature rises",
         ["k₁ < k₂ at every temperature, and the ratio k₂/k₁ increases as the temperature rises",
          "k₁ > k₂ at every temperature",
          "k₁ > k₂ at low temperatures but k₁ < k₂ at high temperatures"]),
    "Comparing rate constants with the Arrhenius equation",
    "k₂/k₁ = e^((Eₐ₁ − Eₐ₂)/RT). The exponent is positive, so k₂ > k₁ at every temperature; as T rises the "
    "exponent becomes smaller, so the ratio falls towards 1. The reaction with the larger Eₐ is the more "
    "sensitive to temperature.",
    ["k₂/k₁ = exp[(Eₐ₁ − Eₐ₂)/RT] > 1 → k₁ < k₂ always",
     "Higher T → smaller exponent → k₂/k₁ decreases (k₁ catches up)"],
    why="The ratio cannot increase with T because the exponent (Eₐ₁ − Eₐ₂)/RT shrinks as T grows. With equal A, "
        "k₁ never exceeds k₂, so the last two options are wrong.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=70)

d8 = {1: (0.1, 0.1, 2.0e-3), 2: (0.3, 0.1, 1.8e-2), 3: (0.1, 0.3, 2.0e-3)}
order_a = round(math.log(d8[2][2] / d8[1][2]) / math.log(3))
order_b = round(math.log(d8[3][2] / d8[1][2]) / math.log(3))
k_d8 = d8[1][2] / (0.1 ** order_a)
truth8a = {"a": order_a == 2, "b": order_b == 0, "c": close(k_d8, 0.20), "d": order_a + order_b == 3,
           "e": close(k_d8 * 0.2 ** 2, 8.0e-3)}
assert truth8a == {"a": True, "b": True, "c": True, "d": False, "e": True}
add("Rate law and order", A, "multi_statement",
    ms("For the reaction A + B → products, the following initial rates were measured at the same temperature:\n"
       "Experiment 1: [A] = 0.10 M, [B] = 0.10 M, rate = 2.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
       "Experiment 2: [A] = 0.30 M, [B] = 0.10 M, rate = 1.8 × 10⁻² mol L⁻¹ s⁻¹\n"
       "Experiment 3: [A] = 0.10 M, [B] = 0.30 M, rate = 2.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
       "Which of the following statements are correct?",
       ["The reaction is second order with respect to A.",
        "The reaction is zero order with respect to B.",
        "The rate constant is 0.20 L mol⁻¹ s⁻¹.",
        "The overall order of the reaction is 3.",
        "When [A] = 0.20 M and [B] = 0.50 M, the rate is 8.0 × 10⁻³ mol L⁻¹ s⁻¹."]),
    multi("C", truth8a, ["(a), (b) and (d) only", "(a), (c), (d) and (e) only", "(b), (c) and (e) only"]),
    "Rate law from initial rates (method of initial rates)",
    "Compare experiments in which only one concentration changes. Tripling [A] multiplies the rate by 9 = 3², "
    "so the order in A is 2. Tripling [B] leaves the rate unchanged, so the order in B is 0. Rate = k[A]².",
    ["(a) 1.8 × 10⁻²/2.0 × 10⁻³ = 9 = 3² → order 2 in A ✓", "(b) rate unchanged → order 0 in B ✓",
     "(c) k = 2.0 × 10⁻³/(0.10)² = 0.20 L mol⁻¹ s⁻¹ ✓", "(d) overall order = 2 + 0 = 2, not 3 ✗",
     "(e) rate = 0.20 × (0.20)² = 8.0 × 10⁻³ mol L⁻¹ s⁻¹ (B has no effect) ✓"],
    why="(d) adds an order of 1 for B, which the data rule out. Options leaving out (a) or (c) are incomplete.",
    ncert=f"{REF8}, factors influencing the rate of a reaction: order of a reaction", seconds=120, checked=True)
