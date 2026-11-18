

# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"
G_ = 6.67e-11

assert close(1000 * g * 6.4e6, 6.4e10)
add(T, "Escape and orbital velocity", "Basic", "numerical",
    "Taking the Earth's radius as 6400 km and g = 10 m/s² at its surface, and neglecting air resistance and the "
    "Earth's rotation, the minimum energy that must be given to a body of mass 1000 kg at the Earth's surface so "
    "that it escapes from the Earth's gravity is:",
    place("6.4 × 10¹⁰ J", ["3.2 × 10¹⁰ J", "1.28 × 10¹¹ J", "6.4 × 10⁷ J"], "B"),
    "Energy needed for escape",
    "With the zero of potential energy at infinity, the body at the surface has U = −GMm/R. To escape it needs at "
    "least enough kinetic energy to bring its total energy to zero: K = GMm/R = mgR, since GM = gR².",
    ["E = GMm/R = mgR", "= 1000 × 10 × 6.4 × 10⁶ = 6.4 × 10¹⁰ J"],
    why="3.2 × 10¹⁰ J is mgR/2, the energy to raise the body only to a height R; 1.28 × 10¹¹ J doubles mgR; "
        "6.4 × 10⁷ J uses R in kilometres.",
    ncert="Class 11 Physics, 'Gravitation', escape speed", seconds=35, recomputed=True)

V_ = -G_ * 45 / 3
assert close(V_, -1.0e-9, rel=2e-3)
add(T, "Gravitational potential and energy", "Basic", "numerical",
    "Taking G = 6.67 × 10⁻¹¹ N m² kg⁻² and the gravitational potential to be zero at infinity, the gravitational "
    "potential at a distance of 3 m from a point mass of 45 kg is about:",
    place("−1.0 × 10⁻⁹ J kg⁻¹", ["−3.3 × 10⁻¹⁰ J kg⁻¹", "+1.0 × 10⁻⁹ J kg⁻¹", "−3.0 × 10⁻⁹ J kg⁻¹"], "A"),
    "Gravitational potential of a point mass",
    "The gravitational potential at distance r from a point mass M is V = −GM/r: the work done per unit mass by an "
    "external agent in bringing a test mass slowly from infinity. It is negative because gravity is attractive.",
    ["V = −GM/r = −(6.67 × 10⁻¹¹ × 45)/3", "= −1.0 × 10⁻⁹ J kg⁻¹"],
    why="−3.3 × 10⁻¹⁰ divides by r² (that is the field strength, in N kg⁻¹); +1.0 × 10⁻⁹ has the wrong sign; "
        "−3.0 × 10⁻⁹ forgets to divide by r.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy (gravitational potential)",
    seconds=35, recomputed=True)

add(T, "Kepler's laws", "Basic", "match_list",
    match_stem("Match List-I (scientist) with List-II (contribution described in NCERT's account of gravitation).",
               ["Ptolemy", "Tycho Brahe", "Johannes Kepler", "Galileo Galilei"],
               ["Recognised that all bodies, irrespective of their masses, are accelerated towards the Earth with a "
                "constant acceleration", "Proposed a geocentric model in which the planets move round the Earth",
                "Made detailed observations of the positions of the planets with the naked eye",
                "Analysed these observations and arrived at three laws of planetary motion"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "D"),
    "History of the study of gravitation",
    "NCERT's introduction to gravitation: Ptolemy's geocentric model; Tycho Brahe's naked-eye observations of "
    "planetary positions; Kepler's three laws drawn from Brahe's data; Galileo's finding that all bodies fall with "
    "the same constant acceleration.",
    ["Ptolemy → geocentric model (II)", "Tycho Brahe → planetary observations (III)",
     "Kepler → three laws of planetary motion (IV)", "Galileo → equal acceleration of falling bodies (I)"],
    why="The wrong codes exchange the observer (Brahe) with the analyst (Kepler), or give Galileo's result on "
        "falling bodies to Kepler.",
    ncert="Class 11 Physics, 'Gravitation', introduction and Kepler's laws", seconds=40)

assert close((2 ** 3) ** 2 / 2 ** 2, 16)
add(T, "Law of gravitation", "Intermediate", "numerical",
    "Two identical uniform solid spheres of the same material are placed in contact. If each sphere is replaced by "
    "one of the same material but twice the radius, again placed in contact, the gravitational force between them "
    "becomes:",
    place("16 times", ["4 times", "64 times", "1/4 times"], "C"),
    "Scaling of the gravitational force with size",
    "For a uniform sphere M = (4/3)πR³ρ, so doubling R makes each mass 8 times. The distance between the centres of "
    "touching spheres is 2R, so it doubles. Each sphere attracts as a point mass at its centre.",
    ["F = GM²/(2R)² with M ∝ R³ → F ∝ R⁶/R² = R⁴", "Doubling R → F becomes 2⁴ = 16 times"],
    why="4 times treats the mass as proportional to R; 64 times ignores the larger separation; 1/4 times keeps the "
        "masses fixed and only doubles the separation.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=60, recomputed=True)

V_c, V_x = -1.0, -1 / math.sqrt(1 + 3)          # in units of GM/R
assert close(V_x - V_c, 0.5)
add(T, "Gravitational potential and energy", "Intermediate", "numerical",
    "A thin uniform ring has mass M and radius R. Taking the gravitational potential to be zero at infinity, the "
    "minimum work needed to move a particle of mass m slowly from the centre of the ring to a point on its axis at "
    "a distance √3R from the centre is (G is the universal gravitational constant):",
    place("GMm/(2R)", ["−GMm/(2R)", "GMm/R", "(GMm/R)(1 − 1/√3)"], "A"),
    "Gravitational potential by superposition",
    "Potential is a scalar, so add the contributions −G dM/s of all mass elements. Every element of the ring is the "
    "same distance s from a point on the axis: s = R at the centre and s = √(R² + 3R²) = 2R at the second point. The "
    "work done by an external agent is m(V_final − V_initial).",
    ["V(centre) = −GM/R", "V(axis, √3R) = −GM/(2R)", "W = m[−GM/(2R) − (−GM/R)] = GMm/(2R)"],
    why="−GMm/(2R) has the sign reversed (the agent must do positive work to pull m away from the ring); GMm/R "
        "assumes the far point is at zero potential; (GMm/R)(1 − 1/√3) takes the distance from the ring as √3R "
        "instead of 2R.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=80, recomputed=True)

add(T, "Gravitational potential and energy", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a height h much smaller than the Earth's radius R, the gain in gravitational potential energy when a "
          "body of mass m is raised from the surface to the height h may be taken as mgh.",
        r="The exact gain is GMm/R − GMm/(R + h) = GMmh/[R(R + h)], which is nearly GMmh/R² = mgh when h ≪ R."),
    ar("A"),
    "mgh as an approximation to −GMm/r",
    "The general expression for gravitational potential energy is −GMm/r. The difference between r = R + h and "
    "r = R reduces to GMmh/R² when R + h ≈ R, and GM/R² = g. So R is exactly the derivation of A.",
    ["ΔU = GMm[1/R − 1/(R + h)] = GMmh/[R(R + h)]", "h ≪ R → ΔU ≈ GMmh/R² = mgh",
     "Both true; R explains A → option A"],
    why="R is the reason, not a separate fact, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=50)

add(T, "Escape and orbital velocity", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If the mass of the Earth were doubled with its radius unchanged, the escape speed from its surface "
           "would become √2 times its present value.",
        s2="If both the mass and the radius of the Earth were doubled, the acceleration due to gravity at its "
           "surface would remain unchanged."),
    sp("C"),
    "Dependence of escape speed and g on mass and radius",
    "v_e = √(2GM/R): doubling M alone multiplies it by √2, so Statement I is true. g = GM/R²: doubling both M and R "
    "gives 2/4 = 1/2, so g would halve, and Statement II is false. (It is the escape speed, ∝ √(M/R), that would "
    "stay unchanged.)",
    ["Statement I: v_e ∝ √M at fixed R → √2 times → true",
     "Statement II: g ∝ M/R² → 2/2² = 1/2 → false"],
    why="Statement II applies the M/R ratio, which governs escape speed, to g, which depends on M/R².",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the earth; escape speed", seconds=45)

# binary: masses M and 2M, separation d; M orbits at 2d/3 from the CM
w2 = (G_ * 2 * 1.0 / 1.0 ** 2) / (2 / 3)        # G M (2M)/d^2 = M w^2 (2d/3) with M = d = 1
assert close(w2, 3 * G_)
add(T, "Law of gravitation", "Advanced", "numerical",
    "Two stars of masses M and 2M, a distance d apart, revolve in circles about their common centre of mass under "
    "their mutual gravitational attraction alone. Their common period of revolution is (G is the universal "
    "gravitational constant):",
    place("2π√(d³/(3GM))", ["2π√(d³/(GM))", "2π√(d³/(2GM))", "2π√(d³/(4GM))"], "D"),
    "Gravitation with the centre of mass: a binary system",
    "Each star moves on a circle about the centre of mass, not about the other star. The star of mass M is at "
    "2d/3 from the centre of mass. The gravitational force between the stars, G(M)(2M)/d², supplies its centripetal "
    "force Mω²(2d/3).",
    ["r(M) = 2M·d/(3M) = 2d/3", "G·2M²/d² = Mω²(2d/3) → ω² = 3GM/d³", "T = 2π/ω = 2π√(d³/(3GM))"],
    shortcut="For two bodies, ω² = G(m₁ + m₂)/d³: here G(3M)/d³.",
    why="2π√(d³/(GM)) treats the star M as orbiting a fixed mass M at distance d; 2π√(d³/(2GM)) has M orbit the "
        "fixed 2M star at distance d; 2π√(d³/(4GM)) takes the centre of mass at the midpoint d/2.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation; 'System of Particles and Rotational "
          "Motion', centre of mass", seconds=120, recomputed=True)

E1 = F(1) - F(1, 2)                       # GMm/R units: reach height R and stop
E2 = (-F(1, 2 * 2)) - (-F(1))            # orbit at radius 2R: E = -GMm/(2r)
assert E1 / E2 == F(2, 3)
add(T, "Satellite energy and period", "Advanced", "numerical",
    "A body at rest on the Earth's surface needs a minimum energy E₁ to be thrown vertically up to a height equal "
    "to the Earth's radius R, and a minimum energy E₂ to be placed in a circular orbit at a height R above the "
    "surface. Neglecting air resistance and the Earth's rotation, E₁ : E₂ is:",
    place("2 : 3", ["3 : 2", "1 : 1", "1 : 2"], "B"),
    "Energy of a body at a height versus energy of a satellite",
    "To just reach height R the body only needs the rise in potential energy. To orbit at radius 2R it must also have "
    "the orbital kinetic energy GMm/(2·2R); its total energy there is −GMm/(4R).",
    ["E₁ = −GMm/(2R) − (−GMm/R) = GMm/(2R)", "E₂ = −GMm/(4R) − (−GMm/R) = 3GMm/(4R)",
     "E₁ : E₂ = (1/2) : (3/4) = 2 : 3"],
    why="3 : 2 inverts the ratio; 1 : 1 forgets the satellite's kinetic energy; 1 : 2 adds the kinetic energy of an "
        "orbit at the SURFACE, GMm/(2R), instead of at radius 2R.",
    ncert="Class 11 Physics, 'Gravitation', energy of an orbiting satellite", seconds=110, recomputed=True)

truth = [True, False, True, True, False]
multi_key(truth, "acd")
assert close(math.sqrt(2), (2 / 1) ** 0.5) and close((1 / 2) ** 1.5, 1 / (2 * math.sqrt(2)))
add(T, "Satellite energy and period", "Advanced", "multi_statement",
    multi("A satellite in a circular orbit of radius 2r round the Earth is shifted to a circular orbit of radius r. "
          "Taking the potential energy to be zero at infinity, which of the following statements are correct?",
          ["Its kinetic energy becomes twice as large.",
           "Its gravitational potential energy increases.",
           "Its total mechanical energy decreases.",
           "Its orbital speed becomes √2 times as large.",
           "Its period of revolution becomes half as large."]),
    place("(a), (c) and (d) only", ["(a), (b) and (d) only", "(c), (d) and (e) only",
                                    "(a), (c), (d) and (e) only"], "C"),
    "Dependence of satellite energies, speed and period on orbit radius",
    "K = GMm/(2r), U = −GMm/r and E = −GMm/(2r); v = √(GM/r) and T ∝ r^(3/2). Halving the radius doubles K, doubles "
    "the magnitude of both U and E (making them more negative), raises v by √2 and reduces T by a factor 2√2.",
    ["(a) K ∝ 1/r → 2K, true", "(b) U = −GMm/r becomes more negative → it decreases → false",
     "(c) E = −GMm/(2r) becomes more negative → decreases, true", "(d) v ∝ r^(−1/2) → √2 times, true",
     "(e) T ∝ r^(3/2) → (1/2)^(3/2) = 1/(2√2) times, not 1/2 → false"],
    why="(b) confuses a larger magnitude with a larger value: −2x is less than −x. (e) uses T ∝ r instead of "
        "Kepler's T² ∝ r³.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites; energy of an orbiting satellite", seconds=100,
    recomputed=True)
