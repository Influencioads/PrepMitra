

# =====================================================================================================================
# Properties of Solids and Liquids (B5 I7 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

assert close(0.5 * (1e-3 / (1e-2 * 1)), 0.05)        # 0.5 g cm^-1 s^-1 -> kg m^-1 s^-1
add(T, "Viscosity and Stokes' law", "Basic", "numerical",
    "The coefficient of viscosity of a liquid is 0.5 poise, where 1 poise = 1 g cm⁻¹ s⁻¹ (the CGS unit). Its value "
    "in SI units is:",
    place("0.05 Pa s", ["5 Pa s", "0.5 Pa s", "0.005 Pa s"], "C"),
    "Conversion between CGS and SI units of viscosity",
    "1 g cm⁻¹ s⁻¹ = 10⁻³ kg / (10⁻² m × 1 s) = 0.1 kg m⁻¹ s⁻¹ = 0.1 Pa s. So 1 poise = 0.1 Pa s.",
    ["1 poise = 10⁻³ kg × 10² m⁻¹ s⁻¹ = 0.1 Pa s", "0.5 poise = 0.05 Pa s"],
    why="5 Pa s multiplies by 10 instead of dividing; 0.5 Pa s assumes the two units are equal; 0.005 Pa s divides "
        "by 100 instead of 10, treating 1 poise as 10⁻² Pa s.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity", seconds=30, recomputed=True)

assert close(math.sqrt(2 * g * 5), 10)
add(T, "Bernoulli's principle", "Basic", "numerical",
    "Water flows out of a small hole in the side of a wide open tank, 5 m below the free surface of the water. "
    "Taking g = 10 m/s², the speed of efflux is:",
    place("10 m/s", ["100 m/s", "5√2 m/s", "50 m/s"], "A"),
    "Torricelli's law",
    "Applying Bernoulli's principle between the free surface (speed ≈ 0, pressure Pₐ) and the hole (pressure Pₐ), "
    "the speed of efflux is √(2gh), the speed a body gains in falling freely through h.",
    ["v = √(2gh) = √(2 × 10 × 5)", "= √100 = 10 m/s"],
    why="100 m/s forgets the square root; 5√2 m/s uses √(gh); 50 m/s uses gh.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle (speed of efflux: "
          "Torricelli's law)", seconds=25, recomputed=True)

X_ = 20 + (220 - 20) / 100 * 50
assert close(X_, 120)
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "On a new temperature scale X, the melting point of ice is 20 °X and the boiling point of water is 220 °X, both "
    "at standard pressure, and the scale is linear. A temperature of 50 °C on this scale is:",
    place("120 °X", ["100 °X", "70 °X", "110 °X"], "D"),
    "Relation between linear temperature scales",
    "For any two linear scales, (reading − ice point)/(steam point − ice point) is the same. So "
    "(X − 20)/(220 − 20) = (C − 0)/(100 − 0).",
    ["(X − 20)/200 = 50/100", "X − 20 = 100", "X = 120 °X"],
    why="100 °X forgets to add the ice-point offset of 20; 70 °X just adds 20 to 50; 110 °X multiplies 50 by "
        "220/100 without the offset.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', temperature and heat; measurement of temperature",
    seconds=35, recomputed=True)

add(T, "Heat transfer", "Basic", "direct",
    "Cooking pots are often given a copper coating on the bottom mainly because copper:",
    place("Is a good conductor of heat, so it spreads the heat over the bottom of the pot",
          ["Is a poor conductor of heat, so it keeps the heat inside the food",
           "Has a very high specific heat capacity, so it stores a large amount of heat",
           "Reflects heat radiation back into the pot"], "B"),
    "Thermal conductivity and its uses",
    "Copper has a high thermal conductivity. A copper-coated bottom conducts heat quickly and spreads it evenly "
    "over the base, so the food is heated uniformly.",
    ["Copper → high thermal conductivity", "Good conductor → faster, more uniform heating of the pot's base"],
    why="Copper is a good, not a poor, conductor; its specific heat capacity is low, not high; reflection of "
        "radiation is not why it is used on the bottom of a pot heated by a flame.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction)", seconds=25)

add(T, "Elasticity and moduli", "Basic", "direct",
    "The ropes of cranes used to lift heavy loads are made of a large number of thin wires braided together, rather "
    "than of a single thick wire of the same total cross-section. The main reason is that the braided rope:",
    place("Is easier to manufacture and more flexible, while giving the required strength",
          ["Has a much larger Young's modulus than a single wire of the same material",
           "Is lighter for the same cross-sectional area of metal",
           "Stretches more under the load, so it stores more energy"], "A"),
    "Application of elastic behaviour: design of crane ropes",
    "The required radius of the rope is fixed by the load and the yield strength of steel (with a safety factor). "
    "A single thick wire of that radius would be practically a rigid rod; braiding many thin wires gives the same "
    "strength with ease of manufacture, flexibility and strength.",
    ["Required cross-section is set by load and yield strength", "Many thin braided wires → flexible, easy to make"],
    why="Young's modulus is a property of the material, not of how the wires are arranged; the mass of metal for "
        "the same cross-section is the same; extra stretching is not the aim.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', applications of elastic behaviour of materials",
    seconds=30)

assert close(2 ** 2 * 0.5 ** 4, 0.25)
add(T, "Heat transfer", "Intermediate", "numerical",
    "A sphere radiates energy at the rate P as a black body at absolute temperature T. Another black-body sphere has "
    "twice the radius and is at an absolute temperature T/2. The rate at which it radiates energy is:",
    place("P/4", ["P/2", "4P", "P/8"], "B"),
    "Stefan-Boltzmann law",
    "The power radiated by a black body is P = σAT⁴, with A = 4πr² for a sphere. So P ∝ r²T⁴.",
    ["P'/P = (r'/r)² × (T'/T)⁴", "= 2² × (1/2)⁴ = 4/16 = 1/4"],
    why="P/2 uses T² instead of T⁴; 4P ignores the change in temperature; P/8 takes the area as proportional to r "
        "instead of r².",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation (Stefan-Boltzmann law)", seconds=40,
    recomputed=True)

P_in = 1.0e5 + 1000 * g * 0.10 + 2 * 0.07 / 1e-4
assert close(P_in, 1.024e5)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "An air bubble of radius 0.1 mm is formed 10 cm below the surface of water in an open vessel. The surface "
    "tension of water is 0.07 N/m, its density is 1000 kg/m³, the atmospheric pressure is 1.0 × 10⁵ Pa and "
    "g = 10 m/s². The pressure inside the bubble is:",
    place("1.024 × 10⁵ Pa", ["1.014 × 10⁵ Pa", "1.010 × 10⁵ Pa", "1.038 × 10⁵ Pa"], "D"),
    "Pressure inside an air bubble in a liquid",
    "The water just outside the bubble is at Pₐ + ρgh. An air bubble in a liquid has one liquid surface, so the "
    "pressure inside exceeds this by 2S/r.",
    ["Pressure outside = 1.0 × 10⁵ + 1000 × 10 × 0.10 = 1.010 × 10⁵ Pa", "2S/r = 0.14/10⁻⁴ = 1400 Pa",
     "P_inside = 1.010 × 10⁵ + 1400 = 1.024 × 10⁵ Pa"],
    why="1.014 × 10⁵ Pa leaves out the hydrostatic pressure ρgh; 1.010 × 10⁵ Pa leaves out the surface-tension "
        "term; 1.038 × 10⁵ Pa uses 4S/r, which applies to a soap bubble with two surfaces.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension (excess pressure inside a drop and "
          "a bubble)", seconds=60, recomputed=True)

assert close(5e-4 * 40 * 100, 2.0)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "The coefficient of volume expansion of a liquid is 5 × 10⁻⁴ K⁻¹. When the liquid is heated through 40 K, its "
    "density decreases by about:",
    place("2%", ["0.67%", "6%", "0.02%"], "C"),
    "Change of density with temperature",
    "The mass stays fixed while the volume grows by the factor (1 + γΔT), so ρ' = ρ/(1 + γΔT) ≈ ρ(1 − γΔT) when "
    "γΔT ≪ 1. The fractional decrease in density is γΔT.",
    ["Δρ/ρ ≈ γΔT = 5 × 10⁻⁴ × 40 = 0.02", "Percentage decrease ≈ 2%"],
    why="0.67% treats 5 × 10⁻⁴ as a volume coefficient and divides by 3; 6% multiplies by 3, treating the given value "
        "as a linear coefficient; 0.02% leaves out the factor 100.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=40, recomputed=True)

H_ = 0.021 * 1.0 * 40 / 0.05
m_ice = H_ * 3600 / 3.36e5
assert close(H_, 16.8) and close(m_ice, 0.18)
add(T, "Heat transfer", "Intermediate", "numerical",
    "The walls of an ice box have a total area of 1.0 m² and a thickness of 5 cm, and are made of a material of "
    "thermal conductivity 0.021 W m⁻¹ K⁻¹. The ice box contains ice at 0 °C and the outside temperature is 40 °C. "
    "Taking the latent heat of fusion of ice as 3.36 × 10⁵ J kg⁻¹ and neglecting heat flow other than by conduction "
    "through the walls, the mass of ice that melts in one hour is:",
    place("180 g", ["3 g", "1.8 g", "0.18 g"], "A"),
    "Steady-state conduction combined with latent heat",
    "In the steady state the heat current through the walls is H = KAΔT/d. All this heat melts ice at 0 °C.",
    ["H = 0.021 × 1.0 × 40 / 0.05 = 16.8 W", "Heat in 1 h = 16.8 × 3600 = 60480 J",
     "m = 60480 / 3.36 × 10⁵ = 0.18 kg = 180 g"],
    why="3 g is the mass melted in one minute; 1.8 g puts the thickness as 5 m instead of 0.05 m (a factor 100); "
        "0.18 g leaves the answer in the wrong unit (0.18 kg read as grams).",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction; latent heat", seconds=80, recomputed=True)

Q = {"A": 1 * 4200 * 10, "B": 1 * 3.36e5, "C": 0.1 * 2.26e6, "D": 1 * 2100 * 10}
assert [round(Q[k] / 1000) for k in "ABCD"] == [42, 336, 226, 21]
add(T, "Thermal expansion and calorimetry", "Intermediate", "match_list",
    match_stem("Take the specific heat capacity of water as 4200 J kg⁻¹ K⁻¹, that of ice as 2100 J kg⁻¹ K⁻¹, the "
               "latent heat of fusion of ice as 3.36 × 10⁵ J kg⁻¹ and the latent heat of vaporisation of water as "
               "2.26 × 10⁶ J kg⁻¹. Match List-I (process, at standard pressure) with List-II (heat needed).",
               ["Warming 1 kg of water from 20 °C to 30 °C", "Melting 1 kg of ice at 0 °C into water at 0 °C",
                "Turning 0.1 kg of water at 100 °C into steam at 100 °C",
                "Warming 1 kg of ice from −10 °C to 0 °C (without melting it)"],
               ["226 kJ", "21 kJ", "42 kJ", "336 kJ"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Sensible heat (mcΔT) and latent heat (mL)",
    "A change of temperature needs Q = mcΔT; a change of state at constant temperature needs Q = mL.",
    ["A: 1 × 4200 × 10 = 42 kJ (III)", "B: 1 × 3.36 × 10⁵ = 336 kJ (IV)", "C: 0.1 × 2.26 × 10⁶ = 226 kJ (I)",
     "D: 1 × 2100 × 10 = 21 kJ (II)"],
    why="The wrong codes swap the specific heats of ice and water, or the two latent heats (forgetting that only "
        "0.1 kg is vaporised).",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', specific heat capacity; change of state (latent heat)",
    seconds=70, recomputed=True)

add(T, "Elasticity and moduli", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Within the elastic limit, the elastic potential energy stored per unit volume of a stretched wire is "
           "½ × stress × strain.",
        s2="For the same tensile stress, a wire of a material with a larger Young's modulus stores more elastic "
           "energy per unit volume."),
    sp("C"),
    "Elastic potential energy density",
    "The work done in stretching a wire is ½Fl, so the energy per unit volume is ½(F/A)(l/L) = ½ × stress × strain: "
    "Statement I is true. With strain = stress/Y, the energy density is stress²/(2Y), so at the same stress a "
    "larger Y gives LESS stored energy per unit volume: Statement II is false.",
    ["u = ½ σ ε (Statement I, true)", "u = σ²/(2Y) → larger Y, smaller u at fixed σ (Statement II, false)"],
    why="Statement II would be right for the same STRAIN (u = ½Yε²), not for the same stress.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', elastic potential energy in a stretched wire",
    seconds=50)

add(T, "Heat transfer", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Newton's law of cooling, that the rate of loss of heat is proportional to the temperature difference "
           "between a body and its surroundings, holds for small temperature differences.",
        s2="A body cooling according to Newton's law takes longer to cool through 10 °C when its temperature is "
           "closer to that of the surroundings."),
    sp("A"),
    "Newton's law of cooling",
    "NCERT states the law for a small temperature difference between the body and its surroundings, so Statement I "
    "is true. Since −dT/dt = k(T − T₀), the rate of cooling is smaller when T is closer to T₀, so the same 10 °C "
    "drop takes more time near the surrounding temperature. Statement II is true.",
    ["Statement I: law valid for small (T − T₀) → true",
     "Statement II: rate ∝ (T − T₀) → slower cooling near T₀ → more time → true"],
    why="Both statements are true; Statement II follows from the law, since the cooling rate falls as the "
        "temperature difference falls.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', Newton's law of cooling", seconds=45)

assert 2 ** 5 == 32
add(T, "Viscosity and Stokes' law", "Advanced", "numerical",
    "A small metal sphere falls through a viscous liquid with its terminal velocity, and the viscous force on it "
    "dissipates energy at the rate P. A sphere of the same metal with twice the radius falls through the same liquid "
    "with its terminal velocity. Assuming Stokes' law holds, the rate at which the viscous force dissipates energy "
    "on the second sphere is:",
    place("32P", ["16P", "8P", "4P"], "D"),
    "Terminal velocity and viscous power",
    "At terminal velocity v = 2r²(ρ − σ)g/(9η), so v ∝ r². The viscous force equals the weight minus the buoyancy, "
    "6πηrv ∝ r³. The power dissipated is F v ∝ r³ × r² = r⁵.",
    ["v_t ∝ r² → 4 times", "F = 6πηrv_t ∝ r³ → 8 times", "P = Fv_t ∝ r⁵ → 2⁵ = 32 times"],
    why="16P takes F ∝ r²; 8P gives only the change in the force; 4P gives only the change in the terminal velocity.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Stokes' law and terminal velocity", seconds=90,
    recomputed=True)

v2 = math.sqrt(1 ** 2 + 2 * g * 0.15)
r2 = 1.0 * math.sqrt(1 / v2)
assert close(v2, 2) and close(r2, 1 / math.sqrt(2))
add(T, "Bernoulli's principle", "Advanced", "numerical",
    "A steady, smooth stream of water comes vertically down out of a tap whose opening has a radius of 1 cm, with a "
    "speed of 1 m/s at the opening. Taking g = 10 m/s² and neglecting viscosity, air resistance and surface tension, "
    "the radius of the stream 15 cm below the opening is:",
    place("1/√2 cm", ["1/2 cm", "1/4 cm", "√2 cm"], "C"),
    "Free fall combined with the equation of continuity",
    "Each element of water falls freely, so its speed grows as v² = v₀² + 2gh. The same volume flows through every "
    "cross-section per second, so Av is constant and the stream narrows.",
    ["v² = 1 + 2 × 10 × 0.15 = 4 → v = 2 m/s", "πr²v = constant → r² = (1 cm)² × (1/2)",
     "r = 1/√2 cm ≈ 0.71 cm"],
    why="1/2 cm takes r ∝ 1/v instead of A ∝ 1/v; 1/4 cm uses the ratio of v² for the radius; √2 cm assumes the "
        "stream widens as it speeds up.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow (equation of continuity)",
    seconds=100, recomputed=True)

add(T, "Heat transfer", "Advanced", "numerical",
    "Two solid spheres of the same material, with radii in the ratio 1 : 2, have the same surface finish and are at "
    "the same temperature, in the same surroundings, losing heat only by radiation. The ratio of their initial "
    "rates of fall of temperature (smaller sphere : larger sphere) is:",
    place("2 : 1", ["1 : 2", "4 : 1", "1 : 1"], "B"),
    "Rate of cooling by radiation depends on area/heat capacity",
    "The rate of heat loss by radiation is proportional to the surface area (same T, same surroundings, same "
    "surface). The fall of temperature is this rate divided by the heat capacity mc, which is proportional to the "
    "volume. So dT/dt ∝ r²/r³ = 1/r.",
    ["Heat loss rate ∝ 4πr²", "Heat capacity ∝ (4/3)πr³ρc", "dT/dt ∝ 1/r → (1/1) : (1/2) = 2 : 1"],
    why="1 : 2 inverts the ratio; 4 : 1 uses only the ratio of the areas inverted (1/r²); 1 : 1 assumes that the "
        "same temperature means the same rate of cooling.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation; specific heat capacity", seconds=80,
    recomputed=True)
assert close((1 / 1) / (1 / 2), 2)

add(T, "Thermal expansion and calorimetry", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="During a long spell of very cold weather, a deep lake freezes at its surface while the water near its "
          "bottom stays liquid, at about 4 °C.",
        r="Water has its maximum density at about 4 °C, so as the lake cools, water at 4 °C sinks to the bottom "
          "while the colder, less dense water stays at the top and freezes there."),
    ar("A"),
    "Anomalous expansion of water",
    "Most liquids become denser as they cool, but water contracts only down to about 4 °C and expands on further "
    "cooling. As a lake cools, surface water sinks until the whole lake is near 4 °C; after that, colder water is "
    "lighter and stays on top, where it freezes. The ice and the cold surface layer insulate the water below, which "
    "stays liquid near 4 °C, allowing aquatic life to survive. R is the reason for A.",
    ["Water: maximum density at about 4 °C", "Water at 4 °C collects at the bottom; colder water stays on top",
     "Freezing starts at the surface; the bottom stays near 4 °C → A true, R explains it"],
    why="R is the cause of A, not a separate fact, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion (anomalous expansion of water)",
    seconds=50)

stress, strain = 50 / 0.5e-6, 50 / 0.5e-6 / 1e11
ext = strain * 1.5
U_ = 0.5 * 50 * ext
assert close(stress, 1e8) and close(strain, 1e-3) and close(ext, 1.5e-3) and close(U_, 0.0375)
assert close(ext / 4, 0.375e-3)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Elasticity and moduli", "Advanced", "multi_statement",
    multi("A wire 1.5 m long, of cross-sectional area 0.5 mm² and Young's modulus 1 × 10¹¹ N/m², hangs from a rigid "
          "support and carries a load that exerts a force of 50 N on it. Within the elastic limit, which of the "
          "following statements are correct?",
          ["The tensile stress in the wire is 1 × 10⁸ N/m².",
           "The longitudinal strain is 1 × 10⁻³.",
           "The extension of the wire is 1.5 mm.",
           "The elastic potential energy stored in the wire is 75 mJ.",
           "A wire of the same material and length but twice the diameter, carrying the same load, would extend "
           "by 0.75 mm."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only",
                                    "(b), (d) and (e) only"], "D"),
    "Stress, strain, extension and stored energy of a wire",
    "Stress = F/A, strain = stress/Y, extension = strain × L, and the energy stored = ½ × F × extension. Doubling "
    "the diameter makes the area 4 times, so the extension falls to one quarter.",
    ["(a) 50 / (0.5 × 10⁻⁶) = 1 × 10⁸ N/m², true", "(b) 10⁸ / 10¹¹ = 10⁻³, true",
     "(c) 10⁻³ × 1.5 m = 1.5 mm, true", "(d) U = ½ × 50 × 1.5 × 10⁻³ = 37.5 mJ, not 75 mJ → false",
     "(e) area × 4 → extension 1.5/4 = 0.375 mm, not 0.75 mm → false"],
    why="(d) forgets the ½ in U = ½F·Δl; (e) treats the area as proportional to the diameter instead of its "
        "square.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus; elastic potential energy in a "
          "stretched wire", seconds=110, recomputed=True)
