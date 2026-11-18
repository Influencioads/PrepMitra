

# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

assert close(5 * 4 * 2 * math.pi, 40 * math.pi)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A constant torque of 5 N m acts on a wheel about its fixed axle while the wheel turns through 4 complete "
    "revolutions. The work done by the torque is:",
    place("40π J", ["20 J", "20π J", "40 J"], "A"),
    "Work done by a torque",
    "For rotation about a fixed axis, the work done by a constant torque is W = τθ, with θ in radians, just as "
    "W = Fs in linear motion.",
    ["θ = 4 × 2π = 8π rad", "W = τθ = 5 × 8π = 40π J"],
    why="20 J multiplies the torque by the number of revolutions; 20π J uses π rad per revolution; 40 J uses 2 rad "
        "per revolution, dropping π.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', work done by a torque", seconds=30,
    recomputed=True)

assert close(20 * 10, 200)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "The engine of a machine applies a constant torque of 20 N m to a shaft rotating steadily at 10 rad/s about its "
    "axis. The power delivered to the shaft is:",
    place("200 W", ["2 W", "20 W", "100 W"], "C"),
    "Power in rotational motion",
    "Instantaneous power in rotation is P = τω, the analogue of P = Fv.",
    ["P = τω = 20 × 10 = 200 W"],
    why="2 W divides the torque by ω; 20 W ignores ω; 100 W takes half the product, confusing P with a kinetic "
        "energy expression.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', power in rotational motion", seconds=20,
    recomputed=True)

assert close(math.sqrt(0.18 / 2), 0.3)
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "The moment of inertia of a body of mass 2 kg about a certain axis is 0.18 kg m². Its radius of gyration about "
    "this axis is:",
    place("0.3 m", ["0.09 m", "0.36 m", "0.6 m"], "D"),
    "Radius of gyration",
    "The radius of gyration k about an axis is defined by I = Mk²: it is the distance from the axis at which the "
    "whole mass, placed as a point, would have the same moment of inertia.",
    ["k = √(I/M) = √(0.18/2) = √0.09", "k = 0.3 m"],
    why="0.09 m forgets the square root; 0.36 m multiplies I by M; 0.6 m doubles the correct value.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia (radius of gyration)",
    seconds=25, recomputed=True)

add(T, "Torque and angular momentum", "Basic", "direct",
    "The SI unit of angular momentum can also be written as:",
    place("J s", ["N m", "kg m² s⁻²", "W s"], "B"),
    "Units of angular momentum",
    "Angular momentum L = r × p has unit m × kg m s⁻¹ = kg m² s⁻¹. Since 1 J = 1 kg m² s⁻², this is the same as "
    "J s (also the unit of Planck's constant).",
    ["L = mvr → kg m² s⁻¹", "J s = kg m² s⁻² × s = kg m² s⁻¹"],
    why="N m (= kg m² s⁻²) is the unit of torque; kg m² s⁻² is the same unit written in base units; W s is the joule, "
        "a unit of energy.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a particle",
    seconds=25)

I_t = (F(2, 3) + 1) * 3 * F(2, 10) ** 2
assert I_t == F(1, 5)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin spherical shell has mass 3 kg and radius 0.2 m. Its moment of inertia about a diameter is (2/3)MR². Its "
    "moment of inertia about a tangent to its surface is:",
    place("0.2 kg m²", ["0.08 kg m²", "0.168 kg m²", "0.12 kg m²"], "B"),
    "Theorem of parallel axes",
    "A tangent is parallel to a diameter at a distance R from it. By the parallel axis theorem, "
    "I = I_cm + MR² = (2/3 + 1)MR² = (5/3)MR².",
    ["MR² = 3 × 0.04 = 0.12 kg m²", "I = (5/3) × 0.12 = 0.2 kg m²"],
    why="0.08 kg m² is the moment of inertia about a diameter; 0.168 kg m² uses (7/5)MR², the result for a SOLID "
        "sphere; 0.12 kg m² is MR² alone, leaving out I_cm.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of parallel axes", seconds=45,
    recomputed=True)

L_ = F(3)
x_cm = (L_ ** 3 / 3) / (L_ ** 2 / 2)
assert x_cm == 2
add(T, "Centre of mass", "Intermediate", "numerical",
    "A thin rod 3 m long lies along the x-axis from x = 0 to x = 3 m. Its mass per unit length increases with x as "
    "λ = kx, where k is a constant. The position of its centre of mass is:",
    place("x = 2 m", ["x = 1.5 m", "x = 1 m", "x = 2.25 m"], "D"),
    "Centre of mass of a continuous body",
    "For a continuous body, X = ∫x dm / ∫dm with dm = λ dx. Because the rod is heavier towards x = 3 m, the centre "
    "of mass lies beyond the midpoint.",
    ["M = ∫₀³ kx dx = 9k/2", "∫₀³ x·kx dx = 9k", "X = 9k/(9k/2) = 2 m (= 2L/3)"],
    why="1.5 m treats the rod as uniform; 1 m is L/3, measured from the wrong end; 2.25 m uses ∫x³/∫x² "
        "(as if λ ∝ x²).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass of a continuous body",
    seconds=70, recomputed=True)

ratio = (F(1, 4)) / F(1, 12)          # (L/2pi)^2 / (L^2/12) without pi^2 -> 3/pi^2
assert ratio == 3
assert close(1 / (4 * math.pi ** 2) / (1 / 12), 3 / math.pi ** 2)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin uniform straight wire of mass M and length L has moment of inertia I₁ about an axis perpendicular to it "
    "through its midpoint. The same wire is bent into a circular ring, whose moment of inertia about the axis "
    "through its centre perpendicular to its plane is I₂. The ratio I₂/I₁ is:",
    place("3/π²", ["π²/3", "12/π²", "3/(2π²)"], "A"),
    "Moment of inertia of a rod and a ring",
    "For the straight wire I₁ = ML²/12. Bent into a ring, the circumference is L, so R = L/(2π) and "
    "I₂ = MR² = ML²/(4π²).",
    ["I₁ = ML²/12", "R = L/(2π) → I₂ = ML²/(4π²)", "I₂/I₁ = 12/(4π²) = 3/π²"],
    why="π²/3 is the inverse ratio; 12/π² takes R = L/π (forgetting the 2 in 2πR); 3/(2π²) uses MR²/2, the moment "
        "of inertia of a ring about a diameter.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moments of inertia of some regular "
          "shaped bodies", seconds=60, recomputed=True)

r_ = (2, 0, 0)
Ls = {k_: cross(r_, v) for k_, v in {"A": (0, 3, 0), "B": (3, 0, 0), "C": (0, -3, 0), "D": (0, 0, 3)}.items()}
assert Ls == {"A": (0, 0, 6), "B": (0, 0, 0), "C": (0, 0, -6), "D": (0, -6, 0)}
add(T, "Torque and angular momentum", "Intermediate", "match_list",
    match_stem("A particle of mass 1 kg is at the point r = 2î m. Match List-I (its velocity, in m/s) with List-II "
               "(its angular momentum about the origin, in kg m² s⁻¹).",
               ["v = 3ĵ", "v = 3î", "v = −3ĵ", "v = 3k̂"],
               ["Zero", "−6ĵ", "6k̂", "−6k̂"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C"),
    "Angular momentum as a vector product, l = r × p",
    "l = r × p = m(r × v). Use î × ĵ = k̂, ĵ × î = −k̂, î × î = 0 and î × k̂ = −ĵ.",
    ["A: 2î × 3ĵ = 6k̂ (III)", "B: 2î × 3î = 0, since r ∥ v (I)", "C: 2î × (−3ĵ) = −6k̂ (IV)",
     "D: 2î × 3k̂ = 6(î × k̂) = −6ĵ (II)"],
    why="The wrong codes reverse the sign for v = ±3ĵ, take î × k̂ = +ĵ, or give a non-zero angular momentum when "
        "the velocity is along r.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a particle",
    seconds=70, recomputed=True)

add(T, "Torque and angular momentum", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If no external torque acts on a body rotating about a fixed axis, its angular velocity must remain "
           "constant.",
        s2="The kinetic energy of a rigid body rotating about a fixed axis with angular velocity ω is ½Iω², where I "
           "is its moment of inertia about that axis."),
    sp("D"),
    "Conservation of angular momentum versus constant angular velocity",
    "With no external torque the angular momentum Iω is conserved, not ω itself. If the body changes shape and its "
    "moment of inertia changes (a skater pulling in her arms, a diver tucking), ω changes. So Statement I is false. "
    "Statement II is the standard result K = Σ½mᵢ(rᵢω)² = ½Iω², true.",
    ["Statement I: τ = 0 → Iω constant; I can change → ω can change → false",
     "Statement II: K = ½Iω² → true"],
    why="Statement I would hold only for a body whose moment of inertia cannot change, such as a rigid wheel.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum; "
          "kinematics of rotational motion", seconds=40)

a2 = F(1)
I_corner = (a2 / 12 + a2 / 12) + a2 / 2           # in units of M a^2
assert I_corner == F(2, 3)
add(T, "Moment of inertia and axis theorems", "Advanced", "numerical",
    "A thin uniform square plate has mass M and side a. Its moment of inertia about an axis in its plane, passing "
    "through its centre and parallel to one side, is Ma²/12. Its moment of inertia about an axis perpendicular to "
    "the plate and passing through one corner is:",
    place("2Ma²/3", ["Ma²/3", "7Ma²/12", "7Ma²/6"], "A"),
    "Perpendicular and parallel axes theorems together",
    "First use the perpendicular axes theorem at the centre: the axis perpendicular to the plate through the "
    "centre has I = Ma²/12 + Ma²/12 = Ma²/6. Then shift it parallel to the corner, a distance a/√2 away.",
    ["I_z(centre) = Ma²/12 + Ma²/12 = Ma²/6", "d = half-diagonal = a/√2 → Md² = Ma²/2",
     "I_corner = Ma²/6 + Ma²/2 = 2Ma²/3"],
    why="Ma²/3 is the moment of inertia about a side (in the plane); 7Ma²/12 starts from Ma²/12 instead of using "
        "the perpendicular axes theorem; 7Ma²/6 takes the shift distance as a instead of a/√2.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorems of perpendicular and parallel "
          "axes", seconds=100, recomputed=True)

I_ratio = F(1, 2) ** 2
w_ratio = 1 / I_ratio
assert w_ratio == 4 and 24 / w_ratio == 6
assert w_ratio ** 2 * I_ratio == 4                  # K = I w^2 / 2
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "Treat the Earth as a uniform solid sphere spinning about its axis once in 24 h. Suppose it contracted, with no "
    "external torque and no change of mass, until its radius was half its present value. The new length of the day "
    "and the factor by which its rotational kinetic energy would change are:",
    place("6 h; rotational kinetic energy becomes 4 times",
          ["12 h; rotational kinetic energy becomes 2 times", "6 h; rotational kinetic energy is unchanged",
           "96 h; rotational kinetic energy becomes 1/4 times"], "C"),
    "Conservation of angular momentum and the energy that goes with it",
    "With no external torque, L = Iω is constant. For a uniform sphere I = (2/5)MR², so halving R makes I one "
    "quarter, and ω four times as large. Rotational KE = L²/(2I), so with L fixed it rises four times; the extra "
    "energy comes from the work done by the internal forces during contraction.",
    ["I' = I/4", "ω' = 4ω → T' = 24/4 = 6 h", "K' = L²/(2I') = 4K"],
    why="12 h and 2 times assume I ∝ R instead of R²; 'unchanged' wrongly assumes rotational KE is conserved along "
        "with L; 96 h inverts the change in ω.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=100, recomputed=True)

add(T, "Equilibrium of rigid bodies", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="A rigid body cannot be in rotational equilibrium while a non-zero net external force acts on it.",
        r="Translational equilibrium requires the net external force to be zero and rotational equilibrium requires "
          "the net external torque to be zero; the two conditions are independent of each other."),
    ar("D"),
    "Conditions of translational and rotational equilibrium",
    "R is true: the two conditions of mechanical equilibrium are separate. A body can satisfy one without the "
    "other. For example, a single force acting through the centre of mass of a free body accelerates it but gives "
    "zero torque about the centre of mass, so the body is in rotational equilibrium while the net force is not "
    "zero. So A is false.",
    ["R: ΣF = 0 and Στ = 0 are independent conditions → true",
     "A: net force ≠ 0 with net torque = 0 is possible → false"],
    why="Because A is false, options A, B and C are wrong. A couple shows the converse: zero net force with a "
        "non-zero torque.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body",
    seconds=55)

X0 = F(2 * 0 + 1 * 6, 3)
Vcm = F(2 * 3 + 1 * (-3), 3)
t_c = F(6, 3 + 3)
x_c = 0 + 3 * t_c
K_i, K_f = F(1, 2) * 2 * 9 + F(1, 2) * 1 * 9, F(1, 2) * 3 * Vcm ** 2
assert X0 == 2 and Vcm == 1 and x_c == 3 and X0 + Vcm * t_c == 3 and K_i - K_f == 12
truth = [True, False, True, True, False]
multi_key(truth, "acd")
add(T, "Centre of mass", "Advanced", "multi_statement",
    multi("On a smooth horizontal surface, a particle of mass 2 kg is at x = 0 moving at 3 m/s in the +x direction "
          "and, at the same instant, a particle of mass 1 kg is at x = 6 m moving at 3 m/s in the −x direction. "
          "They move along the x-axis, collide and stick together. Which of the following statements are correct?",
          ["At the initial instant the centre of mass of the two particles is at x = 2 m.",
           "The velocity of the centre of mass is 2 m/s in the +x direction.",
           "After the collision the combined body moves at 1 m/s in the +x direction.",
           "The particles collide at x = 3 m, which is also where the centre of mass is at that instant.",
           "The total kinetic energy of the particles is the same after the collision as before it."]),
    place("(a), (c) and (d) only", ["(a), (b) and (d) only", "(c), (d) and (e) only",
                                    "(a), (b), (c) and (d) only"], "B"),
    "Motion of the centre of mass of an isolated system",
    "No external horizontal force acts, so the centre of mass moves with a constant velocity, before and after the "
    "collision. The combined body after sticking moves with the velocity of the centre of mass.",
    ["(a) X = (2 × 0 + 1 × 6)/3 = 2 m, true", "(b) V = (2 × 3 − 1 × 3)/3 = 1 m/s, not 2 m/s → false",
     "(c) the stuck pair moves with V = 1 m/s, true",
     "(d) closing speed 6 m/s, gap 6 m → t = 1 s; x = 3 m; X(1 s) = 2 + 1 = 3 m, true",
     "(e) K before = 9 + 4.5 = 13.5 J, after = ½ × 3 × 1² = 1.5 J → false"],
    why="(b) adds speeds without the signs of the velocities; (e) ignores that a sticking (perfectly inelastic) "
        "collision always loses kinetic energy, here 12 J.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass; linear "
          "momentum of a system of particles", seconds=120, recomputed=True)
