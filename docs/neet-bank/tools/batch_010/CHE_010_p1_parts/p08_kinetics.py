

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

k_s = 3.6 / 3600
t_half = 0.693 / k_s
assert close(k_s, 1.0e-3) and close(t_half, 693) and close(0.693 / 3.6, 0.1925) and close(0.693 / (3.6 / 60), 11.55)
add("Half-life", B, "numerical",
    "The rate constant of a first-order reaction is 3.6 h⁻¹. Its half-life, in seconds, is (ln 2 = 0.693):",
    Opts("D", "693 s", ["0.19 s", "11.6 s", "1.0 × 10³ s"]),
    "Half-life of a first-order reaction, t½ = 0.693/k, with consistent units",
    "Convert k into s⁻¹ first (1 h = 3600 s), then apply t½ = 0.693/k.",
    ["k = 3.6 h⁻¹ = 3.6/3600 s⁻¹ = 1.0 × 10⁻³ s⁻¹", "t½ = 0.693 / 1.0 × 10⁻³ s⁻¹ = 693 s"],
    why="0.19 s is 0.693/3.6, which is in hours, not seconds. 11.6 s converts k only to min⁻¹ and reports "
        "minutes as seconds. 1.0 × 10³ s is 1/k, leaving out ln 2.",
    ncert=f"{REF8}, half-life of a reaction", seconds=35, checked=True)

add("Half-life", B, "assertion_reason",
    ar("The half-life of a first-order reaction does not depend on the initial concentration of the reactant.",
       "A catalyst lowers the activation energy of a reaction."),
    AR_, "Half-life of a first-order reaction",
    "A is true: t½ = 0.693/k contains no concentration term. R is also true, but it describes the effect of a catalyst "
    "on the energy barrier, which has nothing to do with why t½ is independent of [R]₀. The explanation lies "
    "in the integrated rate law.",
    ["A: t½ = 0.693/k → independent of [R]₀ → true", "R: catalyst lowers Eₐ → true",
     "R is an unrelated fact about catalysts → option B"],
    answer="B",
    why="R concerns catalysis, not the concentration dependence of t½, so it cannot explain A. Both "
        "statements are true, so C and D are wrong.",
    ncert=f"{REF8}, half-life of a reaction; effect of catalyst", seconds=35)

truth_f = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Rate law and order", B, "multi_statement",
    ms("Which of the following are factors that influence the rate of a chemical reaction?",
       ["Concentration of the reactants (pressure, in the case of gases)",
        "Temperature",
        "Presence of a catalyst",
        "The magnitude of the standard Gibbs energy change, ΔG°, of the reaction",
        "The value of the equilibrium constant of the reaction"]),
    multi("C", truth_f, ["(a), (b), (c) and (d) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"]),
    "Factors influencing the rate of a reaction",
    "NCERT lists the concentration of reactants (pressure for gases), temperature and catalyst as the factors "
    "that influence the rate. ΔG° and K tell us how far a reaction will go, not how fast.",
    ["(a), (b), (c): NCERT's factors ✓", "(d) ΔG° decides feasibility, not speed ✗",
     "(e) K describes the equilibrium position, not the rate ✗"],
    why="Thermodynamic quantities (ΔG°, K) do not fix the rate; a reaction with a very negative ΔG° can still be "
        "very slow. Options containing (d) or (e) are wrong.",
    ncert=f"{REF8}, factors influencing rate of a reaction", seconds=35)

ea = 2.303 * R_J * 1200
t2 = 1 / (1 / 300 - 2.303 * R_J / ea)
t2_ln = 1 / (1 / 300 - R_J / ea)
t2_sign = 1 / (1 / 300 + 2.303 * R_J / ea)
assert close(ea, 22977, 0.002) and close(t2, 400) and close(t2_ln, 337, 0.003) and close(t2_sign, 240)
add("Arrhenius equation and activation energy", I, "numerical",
    "A reaction has an activation energy of 22.98 kJ mol⁻¹, and its pre-exponential factor does not change "
    "with temperature. Its rate constant at 300 K is k₁. The temperature at which its rate constant becomes 10k₁ "
    "is (2.303R = 19.15 J K⁻¹ mol⁻¹):",
    Opts("A", "400 K", ["337 K", "333 K", "240 K"]),
    "Arrhenius equation for two temperatures: log(k₂/k₁) = [Eₐ/(2.303R)](1/T₁ − 1/T₂)",
    "Put log(k₂/k₁) = log 10 = 1 and solve for 1/T₂.",
    ["1 = (22 980 / 19.15)(1/300 − 1/T₂) = 1200 (1/300 − 1/T₂)",
     "1/300 − 1/T₂ = 1/1200", "1/T₂ = 4/1200 − 1/1200 = 3/1200 → T₂ = 400 K"],
    why="337 K uses R instead of 2.303R (natural log with log 10 = 1). 333 K assumes the rate constant doubles "
        "for every 10 K rise, a rough rule that does not apply here. 240 K adds 1/1200 instead of subtracting, "
        "which would make k smaller, not larger.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction (Arrhenius equation)", seconds=90,
    checked=True)

remain = 0.5 ** (50 / 10) * 100
assert close(remain, 3.125) and close(0.5 ** 4 * 100, 6.25)
add("Zero and first order reactions", I, "numerical",
    "In a first-order reaction, 25% of the reactant remains unreacted after 20 minutes. The percentage of the "
    "reactant that remains unreacted after 50 minutes is:",
    Opts("B", "3.125%", ["6.25%", "0%", "10%"]),
    "For a first-order reaction the half-life is constant",
    "25% remaining = two half-lives, so t½ = 10 min. 50 min is then five half-lives.",
    ["100% → 50% → 25% in 20 min → t½ = 10 min", "50 min = 5 half-lives",
     "Remaining = 100% × (½)⁵ = 3.125%"],
    why="6.25% counts four half-lives. 0% extrapolates the fall in concentration linearly, as for a zero-order "
        "reaction. 10% divides 25% by 50/20 instead of using half-lives.",
    ncert=f"{REF8}, integrated rate equations (first order); half-life", seconds=50, checked=True)

k_slope = 2.303 * 0.0050
t_half_slope = 0.693 / k_slope
assert close(t_half_slope, 60.2, 0.002) and close(0.693 / 0.0050, 138.6) and close(0.693 / (0.0050 / 2.303), 319, 0.002) \
    and close(1 / k_slope, 86.8, 0.002)
add("Half-life", I, "numerical",
    "For a first-order reaction, a plot of log[R] (common logarithm) against time is a straight line with a "
    "slope of −0.0050 min⁻¹. The half-life of the reaction is about (ln 2 = 0.693):",
    Opts("D", "60 min", ["139 min", "319 min", "87 min"]),
    "First-order integrated rate law in common logarithms: log[R] = log[R]₀ − kt/2.303",
    "The slope of log[R] against t is −k/2.303, so k = 2.303 × 0.0050 min⁻¹. Then t½ = 0.693/k.",
    ["k = 2.303 × 0.0050 = 0.0115 min⁻¹", "t½ = 0.693/0.0115 ≈ 60 min"],
    why="139 min takes k equal to the magnitude of the slope (the slope of ln[R], not log[R]). 319 min divides "
        "the slope by 2.303 instead of multiplying. 87 min is 1/k, leaving out ln 2.",
    ncert=f"{REF8}, first order reactions (graphical form)", seconds=60, checked=True)

add("Arrhenius equation and activation energy", I, "statement_pair",
    sp("In the collision theory of chemical reactions, the reactant molecules are assumed to be hard spheres, and "
       "reaction is postulated to occur when they collide with one another.",
       "The collision frequency, Z, is the number of collisions per second per unit volume of the reaction "
       "mixture."),
    SP_, "Collision theory of chemical reactions",
    "Both statements are taken from NCERT's account of collision theory: molecules are treated as hard spheres "
    "that react on colliding, and Z is the number of collisions per second per unit volume. Only effective "
    "collisions (enough energy and proper orientation) lead to products.",
    ["I: hard-sphere model; reaction on collision → true", "II: definition of collision frequency → true"],
    answer="A",
    why="Both are NCERT statements, so any option calling one of them false is wrong.",
    ncert=f"{REF8}, collision theory of chemical reactions", seconds=35)

ea_b_cat = (150 - 50) - 50
assert ea_b_cat == 50 and 150 - 50 == 100
add("Arrhenius equation and activation energy", A, "numerical",
    "For an endothermic elementary reaction, ΔH = +50 kJ mol⁻¹ and the activation energy of the forward "
    "reaction is 150 kJ mol⁻¹. A catalyst lowers the activation energy of the forward reaction to "
    "100 kJ mol⁻¹. The activation energy of the BACKWARD reaction in the presence of the catalyst is:",
    Opts("C", "50 kJ mol⁻¹", ["100 kJ mol⁻¹", "150 kJ mol⁻¹", "0 kJ mol⁻¹"]),
    "Energy profile: Eₐ(forward) − Eₐ(backward) = ΔH; a catalyst lowers both barriers by the same amount",
    "A catalyst does not change ΔH; it lowers the energy of the activated complex. So for the catalysed path, "
    "Eₐ(backward) = Eₐ(forward, catalysed) − ΔH.",
    ["Uncatalysed: Eₐ(b) = 150 − 50 = 100 kJ mol⁻¹", "Catalyst lowers both barriers by 150 − 100 = 50 kJ mol⁻¹",
     "Catalysed: Eₐ(b) = 100 − 50 = 50 kJ mol⁻¹"],
    why="100 kJ mol⁻¹ is the uncatalysed backward barrier, as if the catalyst did not affect the reverse "
        "reaction. 150 kJ mol⁻¹ adds ΔH instead of subtracting it. 0 kJ mol⁻¹ subtracts the 50 kJ mol⁻¹ "
        "twice.",
    ncert=f"{REF8}, effect of catalyst; activation energy", seconds=70, checked=True)

assert 0.004 * (0.4 / 0.2) ** 0 == 0.004
add("Rate law and order", A, "numerical",
    "For a reaction A → products at a fixed temperature, doubling the initial concentration of A doubles the "
    "half-life. When [A] = 0.20 mol L⁻¹ the rate is 4.0 × 10⁻³ mol L⁻¹ s⁻¹. At the same temperature, the rate "
    "when [A] = 0.40 mol L⁻¹ is:",
    Opts("D", "4.0 × 10⁻³ mol L⁻¹ s⁻¹",
         ["8.0 × 10⁻³ mol L⁻¹ s⁻¹", "1.6 × 10⁻² mol L⁻¹ s⁻¹", "2.0 × 10⁻³ mol L⁻¹ s⁻¹"]),
    "Order from the dependence of half-life on initial concentration; rate law of a zero-order reaction",
    "t½ ∝ [A]₀ is the signature of a zero-order reaction (t½ = [A]₀/2k). For zero order, rate = k, independent "
    "of [A], so the rate is unchanged.",
    ["t½ ∝ [A]₀ → zero order", "Rate = k[A]⁰ = k", "Rate at 0.40 M = 4.0 × 10⁻³ mol L⁻¹ s⁻¹ (unchanged)"],
    why="8.0 × 10⁻³ assumes first order and 1.6 × 10⁻² second order. 2.0 × 10⁻³ reads the longer half-life as "
        "a slower rate; but a longer t½ here comes from more reactant to use up at the same rate.",
    ncert=f"{REF8}, zero order reactions; half-life of a reaction", seconds=60, checked=True)

truth_r = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Rate law and order", A, "multi_statement",
    ms("For the reaction 4NH₃(g) + 5O₂(g) → 4NO(g) + 6H₂O(g), which of the following statements are correct?",
       ["Rate = −¼ d[NH₃]/dt = ⅙ d[H₂O]/dt.",
        "The rate of formation of NO equals the rate of disappearance of NH₃.",
        "The rate of disappearance of O₂ is 5/4 times the rate of disappearance of NH₃.",
        "The rate of formation of H₂O is 2/3 times the rate of disappearance of NH₃.",
        "The reaction must be of fifth order with respect to O₂."]),
    multi("B", truth_r, ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only"]),
    "Expressing the rate in terms of different species; order is found by experiment",
    "Rate = −¼ d[NH₃]/dt = −⅕ d[O₂]/dt = ¼ d[NO]/dt = ⅙ d[H₂O]/dt. The rates of individual species are in the "
    "ratio of their coefficients. Orders cannot be read from the balanced equation.",
    ["(a) ✓", "(b) NH₃ : NO = 4 : 4 → equal ✓", "(c) O₂ : NH₃ = 5 : 4 ✓",
     "(d) H₂O : NH₃ = 6 : 4 = 3/2, not 2/3 ✗", "(e) order must be found experimentally ✗"],
    why="(d) inverts the ratio of the coefficients and (e) wrongly takes the coefficient of O₂ as its order; "
        "options containing either are wrong.",
    ncert=f"{REF8}, rate of a chemical reaction; order of a reaction", seconds=80)
