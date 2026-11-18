

# =====================================================================================================================
# Thermodynamics (B3 I4 A3)  -- no heat engines, Carnot, efficiency or COP
# =====================================================================================================================
T = "Thermodynamics"
R_ = 8.3

add(T, "Zeroth and first law", "Basic", "direct",
    "A gas enclosed in a cylinder is said to be in thermodynamic equilibrium when:",
    place("Its macroscopic variables, such as pressure, volume, temperature, mass and composition, do not change "
          "with time",
          ["Its molecules have stopped moving", "Its temperature is 0 °C and its pressure is 1 atm",
           "Its internal energy is zero"], "C"),
    "Thermodynamic equilibrium",
    "NCERT: a system is in thermodynamic equilibrium if the macroscopic variables that characterise it do not "
    "change in time. Its molecules keep moving randomly; equilibrium is a property of the macroscopic state, not of "
    "any particular values of P and T.",
    ["Equilibrium → P, V, T, mass and composition constant in time",
     "Molecular motion continues in equilibrium"],
    why="Molecular motion never stops in a gas at any real temperature; equilibrium can occur at any pressure and "
        "temperature; the internal energy of a gas in equilibrium is not zero.",
    ncert="Class 11 Physics, 'Thermodynamics', thermal equilibrium", seconds=25)

add(T, "Zeroth and first law", "Basic", "match_list",
    match_stem("Match List-I (term used in thermodynamics) with List-II (its meaning).",
               ["Diathermic wall", "Adiabatic wall", "Heat reservoir", "Cyclic process"],
               ["A body so large that its temperature does not change appreciably when heat flows into or out of it",
                "A process in which the system returns to its initial state",
                "A conducting wall that allows heat to flow through it",
                "An insulating wall that does not allow heat to flow through it"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Basic terms of thermodynamics",
    "A diathermic (conducting) wall lets heat pass; an adiabatic (insulating) wall does not. A heat reservoir is so "
    "large that its temperature stays fixed while it exchanges heat. In a cyclic process the system comes back to "
    "its initial state.",
    ["Diathermic → conducting (III)", "Adiabatic → insulating (IV)", "Heat reservoir → constant temperature (I)",
     "Cyclic process → returns to initial state (II)"],
    why="The wrong codes exchange the two kinds of wall, or the reservoir with the cyclic process.",
    ncert="Class 11 Physics, 'Thermodynamics', thermal equilibrium; thermodynamic processes", seconds=40)

add(T, "Isothermal and adiabatic processes", "Basic", "assertion_reason",
    AR_STEM.format(
        a="No work is done by or on an ideal gas in an isochoric process.",
        r="In an isochoric process, the temperature of the gas remains constant."),
    ar("C"),
    "Isochoric process",
    "In an isochoric process the volume is constant, so W = ∫P dV = 0: A is true. The heat supplied changes the "
    "internal energy and therefore the temperature; it is the isothermal process, not the isochoric one, in which "
    "the temperature stays constant. So R is false.",
    ["A: ΔV = 0 → W = 0 → true", "R: Q = ΔU = nC_vΔT ≠ 0 in general → T changes → false"],
    why="R describes an isothermal process, so options A and B are wrong; A is true, so D is wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isochoric process)", seconds=30)

W1, W2 = 2e5 * 1e-3, 1e5 * 1e-3
assert close(W1 - W2, 100)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "An ideal gas is taken from state A (pressure 1 × 10⁵ Pa, volume 1 L) to state B (pressure 2 × 10⁵ Pa, volume "
    "2 L) by two different paths. Path 1: first at constant volume to 2 × 10⁵ Pa, then at constant pressure to 2 L. "
    "Path 2: first at constant pressure to 2 L, then at constant volume to 2 × 10⁵ Pa. The heat absorbed along "
    "path 1 exceeds that absorbed along path 2 by:",
    place("100 J", ["Zero", "200 J", "300 J"], "B"),
    "Heat depends on the path; internal energy does not",
    "Both paths join the same two states, so ΔU is the same. By the first law Q = ΔU + W, so the difference in heat "
    "equals the difference in the work done by the gas, which is the area under each path on the P–V diagram.",
    ["Path 1: W₁ = (2 × 10⁵)(1 × 10⁻³) = 200 J (expansion at the higher pressure)",
     "Path 2: W₂ = (1 × 10⁵)(1 × 10⁻³) = 100 J", "Q₁ − Q₂ = W₁ − W₂ = 100 J"],
    why="Zero assumes heat is a state function like U; 200 J and 300 J give the work along path 1 alone or the sum "
        "of the two works.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; state variables", seconds=70,
    recomputed=True)

assert close(1 / 0.693, 1.443, rel=1e-3)
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "Two identical samples of an ideal gas start from the same state (P, V, T). One expands reversibly at constant "
    "pressure to volume 2V; the other expands reversibly and isothermally to volume 2V. Taking ln 2 = 0.693, the "
    "ratio of the work done by the gas at constant pressure to that done isothermally is about:",
    place("1.44", ["0.69", "1", "2"], "D"),
    "Work in isobaric and isothermal expansions",
    "At constant pressure W₁ = P(2V − V) = PV. Isothermally W₂ = nRT ln(2V/V) = PV ln 2, since nRT = PV at the "
    "start. The ratio is 1/ln 2.",
    ["W_isobaric = PV", "W_isothermal = PV ln 2 = 0.693 PV", "Ratio = 1/0.693 ≈ 1.44"],
    why="0.69 is the inverse ratio; 1 assumes equal work for the same change of volume; 2 compares the final "
        "volumes instead of the work.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isothermal and isobaric)", seconds=60,
    recomputed=True)

add(T, "Zeroth and first law", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The molar specific heat of a gas at constant pressure is greater than that at constant volume because, at "
           "constant pressure, part of the heat supplied is used in doing work as the gas expands.",
        s2="The specific heat capacity of a gas is not unique: it depends on the process by which heat is supplied "
           "to it."),
    sp("A"),
    "Specific heat capacities of a gas",
    "At constant volume all the heat raises the internal energy. At constant pressure the gas also expands and "
    "does work, so more heat is needed for the same rise in temperature: C_p > C_v (C_p − C_v = R for an ideal "
    "gas). Statement I is true. Because the heat needed depends on how much work is done, the specific heat "
    "depends on the process: Statement II is true.",
    ["Statement I: Q_p = ΔU + PΔV > Q_v = ΔU → true", "Statement II: heat for a given ΔT depends on the process → true"],
    why="Both statements are true. Statement II is the general point, Statement I a particular case of it.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity", seconds=45)

n_, dT_ = 3, 20
dU_ = 1.5 * R_ * n_ * dT_
assert close(dU_, 747) and close(2.5 * R_ * n_ * dT_, 1245) and F(320, 300) == F(16, 15)
truth = [True, True, True, True, False]
multi_key(truth, "abcd")
add(T, "Zeroth and first law", "Intermediate", "multi_statement",
    multi("Three moles of a monatomic ideal gas in a closed rigid vessel are heated from 300 K to 320 K. Taking "
          "R = 8.3 J mol⁻¹ K⁻¹, which of the following statements are correct?",
          ["No work is done by the gas.",
           "The internal energy of the gas increases by 747 J.",
           "The heat supplied to the gas is 747 J.",
           "The final pressure of the gas is 16/15 of its initial pressure.",
           "If the same gas were heated at constant pressure through the same 20 K, it would also need 747 J of "
           "heat."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c) and (d) only",
                                         "(a), (c), (d) and (e) only"], "B"),
    "First law in an isochoric process",
    "A rigid vessel keeps the volume fixed, so W = 0 and Q = ΔU = nC_vΔT. At constant volume P ∝ T. At constant "
    "pressure the gas would also do work, so more heat, nC_pΔT, would be needed.",
    ["(a) ΔV = 0 → W = 0, true", "(b) ΔU = 3 × (3/2)(8.3)(20) = 747 J, true", "(c) Q = ΔU + 0 = 747 J, true",
     "(d) P₂/P₁ = 320/300 = 16/15, true", "(e) Q_p = 3 × (5/2)(8.3)(20) = 1245 J, not 747 J → false"],
    why="(e) forgets the work done during expansion at constant pressure. Options leaving out (a) or (d), or "
        "including (e), are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; specific heat capacity", seconds=100,
    recomputed=True)

P_gas = 1.0e5 + 10 * g / 0.01
W_ = P_gas * 0.01 * 0.2
Q_ = 3.5 * W_
assert close(P_gas, 1.1e5) and close(W_, 220) and close(Q_, 770) and close(2.5 * W_, 550)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A diatomic ideal gas (rigid molecules) is enclosed in a vertical cylinder by a smooth piston of mass 10 kg and "
    "area 0.01 m². The atmospheric pressure is 1.0 × 10⁵ Pa and g = 10 m/s². The gas is heated slowly, and the "
    "piston rises through 0.2 m. The heat supplied to the gas is:",
    place("770 J", ["220 J", "550 J", "700 J"], "C"),
    "First law with a constant-pressure expansion against a loaded piston",
    "The piston moves slowly, so the gas pressure stays equal to atmospheric pressure plus the piston's weight per "
    "unit area: an isobaric process. For a diatomic gas at constant pressure, Q = nC_pΔT = (7/2)nRΔT = (7/2)PΔV.",
    ["P = 1.0 × 10⁵ + (10 × 10)/0.01 = 1.1 × 10⁵ Pa", "ΔV = 0.01 × 0.2 = 2 × 10⁻³ m³ → W = PΔV = 220 J",
     "ΔU = (5/2)PΔV = 550 J", "Q = ΔU + W = (7/2) × 220 = 770 J"],
    why="220 J is only the work done by the gas; 550 J is only the rise in internal energy; 700 J leaves out the "
        "piston's weight in the pressure.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; isobaric process", seconds=120,
    recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Real thermodynamic processes can at best approximate a reversible process, which is an idealisation.",
        r="In real processes there are dissipative effects, such as friction and viscosity, and heat flows across "
          "finite temperature differences, so the system and surroundings cannot both be restored exactly."),
    ar("A"),
    "Reversible and irreversible processes",
    "A reversible process must be quasi-static and free of dissipative effects; only then can it be retraced with "
    "both system and surroundings returning to their original states. Every real process involves some friction, "
    "viscosity or finite-rate heat flow, which is why it is irreversible and why the reversible process is only an "
    "idealisation. R gives exactly this reason.",
    ["Reversible ⇔ quasi-static and no dissipation", "Real processes always have dissipation → irreversible",
     "R explains A → option A"],
    why="R is the cause of A, not an unrelated fact, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', reversible and irreversible processes", seconds=50)

n_, dT_ = 2, 100
W_ = n_ * R_ * dT_
assert close(W_, 1660) and close(3.5 * W_, 5810) and close(2.5 * W_, 4150)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Isothermal and adiabatic processes", "Advanced", "multi_statement",
    multi("Two moles of a diatomic ideal gas (rigid molecules) are taken from 300 K to 400 K along a process that is a "
          "straight line passing through the origin on a volume–temperature (V–T) graph. Taking R = "
          "8.3 J mol⁻¹ K⁻¹, which of the following statements are correct?",
          ["The pressure of the gas stays constant.",
           "The work done by the gas is 1660 J.",
           "The heat absorbed by the gas is 5810 J.",
           "The internal energy of the gas increases by 1660 J.",
           "The density of the gas increases during the process."]),
    place("(a), (b) and (c) only", ["(a), (b) and (d) only", "(b), (c) and (e) only",
                                    "(a), (c), (d) and (e) only"], "D"),
    "Reading a process from a V–T graph",
    "V ∝ T means V/T is constant, which by PV = nRT means P is constant: an isobaric process. Then W = PΔV = nRΔT, "
    "ΔU = nC_vΔT with C_v = (5/2)R, and Q = nC_pΔT with C_p = (7/2)R.",
    ["(a) V/T constant → P constant, true", "(b) W = nRΔT = 2 × 8.3 × 100 = 1660 J, true",
     "(c) Q = (7/2)nRΔT = 5810 J, true", "(d) ΔU = (5/2)nRΔT = 4150 J, not 1660 J → false",
     "(e) volume increases at fixed mass → density decreases → false"],
    why="(d) gives the work done instead of the change in internal energy; (e) has the wrong direction, since the "
        "gas expands as it is heated at constant pressure.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; isobaric process", seconds=110,
    recomputed=True)
