

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

dg = 97.9 - 2 * 51.3
assert close(dg, -4.7) and close(97.9 - 51.3, 46.6) and close(97.9 + 2 * 51.3, 200.5)
add("Gibbs energy and K", B, "numerical",
    "The standard Gibbs energies of formation at 298 K are ΔfG°(NO₂, g) = 51.3 kJ mol⁻¹ and "
    "ΔfG°(N₂O₄, g) = 97.9 kJ mol⁻¹. The standard Gibbs energy change for 2NO₂(g) → N₂O₄(g) at 298 K is:",
    Opts("D", "−4.7 kJ mol⁻¹", ["+46.6 kJ mol⁻¹", "+4.7 kJ mol⁻¹", "+200.5 kJ mol⁻¹"]),
    "ΔrG° from standard Gibbs energies of formation",
    "Like enthalpy, Gibbs energy is a state function: ΔrG° = Σ ΔfG°(products) − Σ ΔfG°(reactants), each "
    "multiplied by its coefficient.",
    ["ΔrG° = ΔfG°(N₂O₄) − 2 ΔfG°(NO₂)", "= 97.9 − 2 × 51.3 = 97.9 − 102.6 = −4.7 kJ mol⁻¹"],
    why="+46.6 kJ mol⁻¹ forgets the coefficient 2 of NO₂. +4.7 kJ mol⁻¹ subtracts products from reactants. "
        "+200.5 kJ mol⁻¹ adds the terms instead of subtracting.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=35, checked=True)

add("First law, work and enthalpy", B, "direct",
    "For a system enclosed by adiabatic walls, the change in internal energy, ΔU, in a process is equal to:",
    Opts("A", "the work done on the system", ["the heat absorbed by the system", "zero, in every process",
                                              "the enthalpy change of the system"]),
    "First law of thermodynamics for an adiabatic process",
    "ΔU = q + w. Adiabatic walls allow no heat exchange (q = 0), so ΔU = w_ad, the work done on the system.",
    ["ΔU = q + w", "Adiabatic → q = 0", "ΔU = w_ad"],
    why="The heat absorbed is zero in an adiabatic process, so ΔU cannot equal it. ΔU is zero only if no work is "
        "done either. ΔH equals the heat absorbed at constant pressure, not ΔU in an adiabatic change.",
    ncert=f"{REF4}, internal energy as a state function: work", seconds=25)

add("Entropy and Gibbs energy", B, "statement_pair",
    sp("The Gibbs energy change, ΔG, of a process at constant temperature and pressure is the net energy "
       "available to do useful work.",
       "For a spontaneous process at constant temperature and pressure, ΔG is positive."),
    SP_, "Meaning of Gibbs energy and the criterion of spontaneity",
    "NCERT describes ΔG as the net energy available to do useful work (Statement I true). A process at constant "
    "T and p is spontaneous when ΔG is NEGATIVE; a positive ΔG means the process is non-spontaneous "
    "(Statement II false).",
    ["I: ΔG = net energy available for useful work → true", "II: spontaneous ↔ ΔG < 0 → false"],
    answer="C",
    why="Statement II reverses the sign of the criterion.",
    ncert=f"{REF4}, Gibbs energy and spontaneity", seconds=30)

du = 120 + 80
assert du == 200 and 120 - 80 == 40
add("First law, work and enthalpy", B, "numerical",
    "A system absorbs 120 J of heat from its surroundings, and at the same time the surroundings do 80 J of work "
    "on it. The change in the internal energy of the system is:",
    Opts("C", "+200 J", ["+40 J", "−40 J", "−200 J"]),
    "First law of thermodynamics, ΔU = q + w (IUPAC sign convention)",
    "Heat absorbed by the system and work done on the system both increase its internal energy, so both are "
    "positive.",
    ["q = +120 J (absorbed)", "w = +80 J (done on the system)", "ΔU = 120 + 80 = +200 J"],
    why="+40 J takes the work done on the system as negative. −40 J and −200 J also use wrong signs for q or w.",
    ncert=f"{REF4}, first law of thermodynamics", seconds=25, checked=True)

dh_hyd = -1300 + 2 * (-286) - (-1560)
assert dh_hyd == -312 and (-1300 - 286 + 1560) == -26
add("Hess's law and enthalpies", I, "numerical",
    "The standard enthalpies of combustion (kJ mol⁻¹) of ethyne C₂H₂(g), hydrogen H₂(g) and ethane C₂H₆(g) are "
    "−1300, −286 and −1560 respectively (water formed as liquid). The standard enthalpy change of the reaction "
    "C₂H₂(g) + 2H₂(g) → C₂H₆(g) is:",
    Opts("A", "−312 kJ mol⁻¹", ["+312 kJ mol⁻¹", "−26 kJ mol⁻¹", "−3146 kJ mol⁻¹"]),
    "Hess's law with enthalpies of combustion",
    "Burn the reactants and 'un-burn' the product: ΔrH = Σ ΔcH(reactants) − Σ ΔcH(products), with every "
    "combustion giving the same CO₂ and H₂O on both sides.",
    ["ΔrH = [ΔcH(C₂H₂) + 2 ΔcH(H₂)] − ΔcH(C₂H₆)", "= [−1300 + 2(−286)] − (−1560)",
     "= −1872 + 1560 = −312 kJ mol⁻¹"],
    why="+312 kJ mol⁻¹ subtracts the reactant terms from the product term (the rule for enthalpies of "
        "formation). −26 kJ mol⁻¹ forgets the coefficient 2 of H₂. −3146 kJ mol⁻¹ adds all three values.",
    ncert=f"{REF4}, Hess's law of constant heat summation; enthalpy of combustion", seconds=70, checked=True)

rt = R_J * 373 / 1000
du_vap = 40.7 - rt
assert close(du_vap, 37.6) and close(40.7 + rt, 43.8) and close(40.7 - R_J * 100 / 1000, 39.87)
add("First law, work and enthalpy", I, "numerical",
    "The enthalpy of vaporisation of water at 373 K and 1 bar is 40.7 kJ mol⁻¹. Treating the vapour as an "
    "ideal gas and neglecting the volume of the liquid, the change in internal energy when 1 mol of water "
    "vaporises at 373 K is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("B", "37.6 kJ mol⁻¹", ["43.8 kJ mol⁻¹", "40.7 kJ mol⁻¹", "39.9 kJ mol⁻¹"]),
    "Relation between ΔH and ΔU: ΔH = ΔU + Δn_g RT",
    "Vaporisation creates 1 mol of gas from a liquid (Δn_g = +1). Part of the enthalpy supplied goes into "
    "pushing back the atmosphere (pΔV = RT), so ΔU is smaller than ΔH by RT.",
    ["Δn_g = 1 − 0 = 1", "RT = 8.314 × 373 = 3101 J = 3.10 kJ", "ΔU = ΔH − Δn_g RT = 40.7 − 3.10 = 37.6 kJ mol⁻¹"],
    why="43.8 kJ mol⁻¹ adds RT instead of subtracting it. 40.7 kJ mol⁻¹ ignores the expansion work. 39.9 kJ "
        "mol⁻¹ uses the temperature in °C (100) instead of kelvin.",
    ncert=f"{REF4}, enthalpy: relation between ΔH and ΔU", seconds=60, checked=True)

add("Hess's law and enthalpies", I, "assertion_reason",
    ar("The standard enthalpy of formation of O₂(g) at 298 K is zero.",
       "The O₂ molecule is paramagnetic."),
    AR_, "Standard enthalpy of formation of an element in its reference state",
    "By convention, ΔfH° of an element in its reference (most stable) state at 1 bar is zero; at 298 K oxygen's "
    "reference state is O₂(g), so A is true. R is also true (O₂ has two unpaired electrons), but it is a "
    "magnetic property that has nothing to do with the enthalpy convention.",
    ["A: element in its reference state → ΔfH° = 0 → true", "R: two unpaired electrons in π* orbitals → true",
     "R does not explain A → option B"],
    answer="B",
    why="ΔfH° of O₂(g) would be zero even if O₂ were diamagnetic, because it is the reference state of oxygen.",
    ncert=f"{REF4}, standard enthalpy of formation", seconds=35)

add("Entropy and Gibbs energy", I, "statement_pair",
    sp("The entropy of a substance decreases when it is heated.",
       "For a reversible change at temperature T, the entropy change of a system is ΔS = q_rev/T, where q_rev is "
       "the heat absorbed reversibly."),
    SP_, "Entropy and temperature",
    "Heating increases the random motion of the particles, so entropy increases with temperature: Statement I "
    "is false. The definition ΔS = q_rev/T is as given in NCERT: Statement II is true.",
    ["I: higher T → more randomness → higher entropy → false", "II: ΔS = q_rev/T → true"],
    answer="D",
    why="Statement I reverses the effect of temperature on entropy.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=30)

add("Hess's law and enthalpies", I, "match_list",
    lists("Match List-I (process) with List-II (name of its enthalpy change).",
          ["Na(g) → Na⁺(g) + e⁻", "Cl(g) + e⁻ → Cl⁻(g)", "NaCl(s) → Na⁺(g) + Cl⁻(g)", "Cl₂(g) → 2Cl(g)"],
          ["Lattice enthalpy", "Bond dissociation enthalpy", "Ionisation enthalpy", "Electron gain enthalpy"]),
    match("D", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Enthalpy changes used in a Born–Haber cycle",
    "Removing an electron from a gaseous atom is ionisation; adding one to a gaseous atom is electron gain; "
    "separating one mole of an ionic solid into gaseous ions is the lattice enthalpy; breaking the bond of a "
    "gaseous diatomic molecule into atoms is bond dissociation.",
    ["A → III", "B → IV", "C → I", "D → II"],
    why="The wrong codes swap ionisation with electron gain, lattice with bond dissociation, or ionisation with "
        "lattice enthalpy.",
    ncert=f"{REF4}, enthalpies for different types of reactions: lattice enthalpy (Born–Haber cycle)",
    seconds=35)

ds_sys = 40700 / 373
ds_surr = -40700 / 383
ds_tot = ds_sys + ds_surr
assert close(ds_tot, 2.85, 0.01) and close(ds_sys - ds_surr, 215.4, 0.01)
add("Entropy and Gibbs energy", A, "numerical",
    "Water boils at 373 K at 1 bar, and its enthalpy of vaporisation is 40.7 kJ mol⁻¹. Assuming ΔvapH and "
    "ΔvapS do not change with temperature, the TOTAL entropy change (system + surroundings) when 1 mol of "
    "liquid water vaporises at 383 K and 1 bar, and the nature of the process, are:",
    Opts("C", "+2.85 J K⁻¹; spontaneous", ["−2.85 J K⁻¹; non-spontaneous", "0; at equilibrium",
                                          "+215 J K⁻¹; spontaneous"]),
    "Total entropy change as the criterion of spontaneity",
    "At the boiling point ΔG = 0, so ΔvapS = ΔvapH/T_b. At 383 K the surroundings supply 40.7 kJ of heat, so "
    "their entropy falls by ΔH/383. The sum decides spontaneity.",
    ["ΔS(system) = 40 700/373 = +109.1 J K⁻¹", "ΔS(surroundings) = −40 700/383 = −106.3 J K⁻¹",
     "ΔS(total) = 109.1 − 106.3 = +2.85 J K⁻¹ > 0 → spontaneous (water boils above 373 K)"],
    why="−2.85 J K⁻¹ swaps the two temperatures. 'At equilibrium' applies only at 373 K. +215 J K⁻¹ adds the "
        "magnitudes, forgetting that the surroundings lose heat.",
    ncert=f"{REF4}, entropy and spontaneity; Gibbs energy", seconds=120, checked=True)

be_co = (717 + 498 + 393.5) / 2
assert close(be_co, 804.25) and close(2 * be_co, 1608.5) and close((717 + 498 - 393.5) / 2, 410.75) \
    and close((498 + 393.5) / 2, 445.75)
add("Hess's law and enthalpies", A, "numerical",
    "Use the data (kJ mol⁻¹): ΔfH°(CO₂, g) = −393.5; enthalpy of atomisation of graphite, C(graphite) → C(g), "
    "= 717; bond dissociation enthalpy of O₂ = 498. The mean C=O bond enthalpy in CO₂ is about:",
    Opts("A", "804 kJ mol⁻¹", ["1608 kJ mol⁻¹", "411 kJ mol⁻¹", "446 kJ mol⁻¹"]),
    "Bond enthalpy from a Hess's-law cycle",
    "Form CO₂ from the elements by a two-route cycle: (i) directly, ΔfH°; (ii) atomise graphite and break O₂ "
    "into atoms, then form two C=O bonds. The two routes must have the same enthalpy change.",
    ["ΔfH° = ΔaH(C) + D(O=O) − 2 × D(C=O)", "−393.5 = 717 + 498 − 2 D(C=O)",
     "2 D(C=O) = 1608.5 → D(C=O) = 804 kJ mol⁻¹"],
    why="1608 kJ mol⁻¹ is the energy of both C=O bonds together. 411 kJ mol⁻¹ uses +393.5 for ΔfH°. "
        "446 kJ mol⁻¹ leaves out the atomisation of graphite.",
    ncert=f"{REF4}, bond enthalpy; Hess's law", seconds=100, checked=True)

add("Gibbs energy and K", A, "statement_pair",
    sp("For a reaction with negative ΔH° and negative ΔS° (both independent of temperature), the equilibrium "
       "constant decreases as the temperature is raised.",
       "Raising the temperature increases the equilibrium constant of every reaction."),
    SP_, "Effect of temperature on K through ΔG° = ΔH° − TΔS° and ΔG° = −RT ln K",
    "With ΔH° < 0 and ΔS° < 0, the term −TΔS° is positive and grows with T, so ΔG° becomes less negative (or "
    "positive) as T rises, and K = e^(−ΔG°/RT) falls: Statement I is true. For an endothermic reaction K rises "
    "with temperature, but for an exothermic one it falls, so Statement II is false.",
    ["I: ΔG° = ΔH° − TΔS° rises with T when ΔS° < 0 → K falls → true",
     "II: K rises with T only when ΔH° > 0 → false"],
    answer="C",
    why="Statement II ignores the sign of ΔH°; Statement I describes an exothermic reaction correctly.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=60)

add("Entropy and Gibbs energy", A, "assertion_reason",
    ar("When an ideal gas is compressed isothermally and reversibly, its entropy decreases.",
       "During this compression heat flows out of the gas (q_rev is negative), and the entropy change of the gas "
       "is ΔS = q_rev/T."),
    AR_, "Sign of the entropy change from the heat exchanged reversibly",
    "In an isothermal change of an ideal gas ΔU = 0, so q = −w. During compression work is done on the gas "
    "(w > 0), hence q_rev < 0: heat leaves the gas. With ΔS = q_rev/T, the entropy change is negative. R gives "
    "exactly this reasoning.",
    ["Isothermal ideal gas: ΔU = 0 → q_rev = −w", "Compression: w > 0 → q_rev < 0",
     "ΔS = q_rev/T < 0 → A true, R true and explains A"],
    answer="A",
    why="Both statements are true and R is the direct cause: a negative q_rev at constant T means a negative ΔS.",
    ncert=f"{REF4}, entropy and spontaneity; isothermal work of an ideal gas", seconds=60)
