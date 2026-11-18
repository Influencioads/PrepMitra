
NC = "Class 12 Physics, "
rad, deg = math.radians, math.degrees
K9 = 9e9

# ================================================================ Electrostatics (B5 I7 A5)
ESC = NC + "'Electric Charges and Fields', "
ESP = NC + "'Electrostatic Potential and Capacitance', "

# ---- Basic
C_ = F(240, 60)
assert C_ == 4 and C_ * 90 == 360 and F(240 * 60, 90) == 160 and F(240) * F(90, 60) ** 2 == 540
q(ES, "Capacitors and dielectrics", "Basic", "numerical",
  "A capacitor holds a charge of 240 μC when a potential difference of 60 V is applied across it. If the potential "
  "difference is raised to 90 V, the charge it holds becomes:",
  *opt("360 μC", ["160 μC", "240 μC", "540 μC"], "A"),
  "Capacitance C = Q/V is fixed by the geometry and the medium, so Q is proportional to V",
  "The capacitance found from the first reading stays the same when the voltage changes; only the charge changes.",
  ["C = 240 μC / 60 V = 4 μF", "New charge Q = CV = 4 μF × 90 V = 360 μC"],
  shortcut="Q ∝ V: Q = 240 × 90/60 = 360 μC.",
  why="160 μC scales the charge by 60/90 instead of 90/60. 240 μC assumes the charge stays fixed. 540 μC scales the "
      "charge with V², which is how the stored energy (not the charge) changes.",
  ncert=ESP + "capacitors and capacitance", seconds=30, rc=True)

n_ = 10
assert F(n_) / F(1, n_) == 100
q(ES, "Capacitors and dielectrics", "Basic", "numerical",
  "Ten identical capacitors are first connected all in parallel and then all in series. The ratio of the equivalent "
  "capacitance of the parallel combination to that of the series combination is:",
  *opt("100", ["1/100", "10", "1"], "B"),
  "Parallel: C_p = sum of capacitances; series: 1/C_s = sum of reciprocals",
  "For n identical capacitors C, the parallel combination is nC and the series combination is C/n.",
  ["C_p = 10C", "C_s = C/10", "C_p/C_s = 10C ÷ (C/10) = 100"],
  shortcut="For n identical capacitors the ratio is n².",
  why="1/100 is the series-to-parallel ratio, inverted. 10 compares only one of the combinations with a single "
      "capacitor. 1 assumes the arrangement does not matter.",
  ncert=ESP + "combination of capacitors", seconds=30, rc=True)

q(ES, "Gauss's law", "Basic", "direct",
  "A student applies Gauss's law to a system of discrete point charges. Which of the following is a correct "
  "guideline for choosing the Gaussian surface?",
  *opt("It must not pass through any of the discrete point charges",
       ["It must be a sphere centred on one of the charges",
        "It must be the surface of a real conductor",
        "It must enclose all the charges, because charges outside change the total flux through it"], "C"),
  "Gauss's law and the Gaussian surface",
  "Any closed surface may be used as a Gaussian surface, of any shape or size, real or imaginary. The one caution "
  "NCERT gives is that the surface should not pass through a discrete charge, because the electric field of a system "
  "of point charges is not well defined at the location of a charge.",
  ["Gaussian surface: any closed surface", "Field undefined at a point charge → surface must not pass through one"],
  why="The sphere is only a convenient choice when there is spherical symmetry; Gauss's law holds for any shape. The "
      "surface may be imaginary. Charges outside the surface contribute zero total flux (they change the field on the "
      "surface, but not the net flux).",
  ncert=ESC + "Gauss's law", seconds=35)

q(ES, "Electric field and dipole", "Basic", "assertion_reason",
  ar("To find the electric field produced by a source charge, the force is measured on a test charge that is made "
     "vanishingly small.",
     "A test charge that is not small could push or pull the source charges and disturb their arrangement, so the "
     "field measured would not be the field of the original arrangement."),
  AR, ar_key(True, True, True),
  "Definition of the electric field using a test charge",
  "The field at a point is E = F/q for a test charge q placed there. If q were large, the force it exerts on the "
  "source charges could move them (or, on a conductor, redistribute them), so the field being measured would be "
  "changed by the act of measuring it. Making q negligibly small avoids this. R is exactly why A is done.",
  ["A: test charge made vanishingly small → true", "R: a large test charge disturbs the source arrangement → true",
   "R gives the reason for A"],
  why="R is not an unrelated fact: it is the very reason the test charge must be small, so the 'NOT the correct "
      "explanation' option fails.",
  ncert=ESC + "electric field", seconds=40)

W_ = 1.6e-19 * (70 - 20)
close(W_, 8.0e-18)
close(1.6e-19 * 90, 1.44e-17)
q(ES, "Electric potential and energy", "Basic", "numerical",
  "An electron moves from a point where the electrostatic potential is 20 V to a point where it is 70 V. Taking "
  "e = 1.6 × 10⁻¹⁹ C, the work done on the electron by the electric field is:",
  *opt("+8.0 × 10⁻¹⁸ J", ["−8.0 × 10⁻¹⁸ J", "+1.12 × 10⁻¹⁷ J", "+1.44 × 10⁻¹⁷ J"], "D"),
  "Work done by the field = −(change in potential energy) = −q(V_final − V_initial)",
  "The potential energy of a charge q at potential V is qV. For the electron q = −e, so moving to a higher potential "
  "lowers its potential energy, and the field does positive work on it.",
  ["ΔU = q ΔV = (−1.6 × 10⁻¹⁹ C)(70 V − 20 V) = −8.0 × 10⁻¹⁸ J",
   "Work by the field = −ΔU = +8.0 × 10⁻¹⁸ J"],
  shortcut="A negative charge moving towards higher potential gains kinetic energy: |W| = e × 50 V = 50 eV, positive.",
  why="−8.0 × 10⁻¹⁸ J treats the electron as a positive charge (or gives the work of an external agent). "
      "+1.12 × 10⁻¹⁷ J uses the final potential (70 V) alone. +1.44 × 10⁻¹⁷ J adds the two potentials instead of "
      "taking their difference.",
  ncert=ESP + "potential energy of a charge in an external field", seconds=40, rc=True)

# ---- Intermediate
E_hex = K9 * 2e-6 / 0.3 ** 2
close(E_hex, 2e5)
close(5 * E_hex, 1e6)
q(ES, "Coulomb's law and superposition", "Intermediate", "numerical",
  "Point charges, each of +2 μC, are placed at five of the six corners of a regular hexagon of side 30 cm, in air; "
  "the sixth corner is empty. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electric field at the centre of the hexagon "
  "is:",
  *opt("2 × 10⁵ N/C, directed towards the empty corner",
       ["2 × 10⁵ N/C, directed away from the empty corner", "1 × 10⁶ N/C, directed towards the empty corner",
        "zero"], "A"),
  "Superposition principle; symmetry",
  "If all six corners carried +2 μC, the fields at the centre would cancel in pairs (opposite corners). So the field "
  "of the five charges equals minus the field that the missing sixth charge would produce. A +2 μC charge at the "
  "empty corner would give a field at the centre pointing away from that corner; the actual field therefore points "
  "towards the empty corner. In a regular hexagon each corner is at a distance equal to the side from the centre.",
  ["Distance of each corner from the centre = side = 0.30 m",
   "Field of one charge there = 9 × 10⁹ × 2 × 10⁻⁶ / 0.09 = 2 × 10⁵ N/C",
   "Five charges = six charges (zero) − one charge → 2 × 10⁵ N/C towards the empty corner"],
  shortcut="Field of the gap = field of a −2 μC charge placed at the empty corner.",
  why="'Away from the empty corner' gets the magnitude right but reverses the direction. 1 × 10⁶ N/C adds the five "
      "magnitudes as if all the fields were parallel. Zero assumes the five charges are still symmetric.",
  seconds=75, rc=True)

kk, e_, G_, mp = 9e9, 1.6e-19, 6.67e-11, 1.67e-27
ratio = kk * e_ ** 2 / (G_ * mp ** 2)
close(ratio, 1.24e36, 1e-2)
close(kk * e_ ** 2 / (G_ * mp), 2.07e9, 1e-2)
close(1 / ratio, 8.07e-37, 1e-2)
q(ES, "Coulomb's law and superposition", "Intermediate", "numerical",
  "Two protons are a distance r apart in vacuum. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², G = 6.67 × 10⁻¹¹ N m² kg⁻², "
  "e = 1.6 × 10⁻¹⁹ C and the proton mass as 1.67 × 10⁻²⁷ kg, the ratio of the electrostatic force between them to "
  "the gravitational force between them is about:",
  *opt("1.2 × 10³⁶, whatever the value of r",
       ["8.1 × 10⁻³⁷, whatever the value of r", "2.1 × 10⁹, whatever the value of r",
        "1.2 × 10³⁶ at r = 1 m, and larger at smaller r"], "C"),
  "Coulomb's law and Newton's law of gravitation are both inverse-square laws",
  "Both forces vary as 1/r², so r cancels in the ratio: F_e/F_G = ke²/(Gm²).",
  ["ke² = 9 × 10⁹ × (1.6 × 10⁻¹⁹)² = 2.30 × 10⁻²⁸ N m²",
   "Gm² = 6.67 × 10⁻¹¹ × (1.67 × 10⁻²⁷)² = 1.86 × 10⁻⁶⁴ N m²",
   "Ratio = 2.30 × 10⁻²⁸ / 1.86 × 10⁻⁶⁴ ≈ 1.2 × 10³⁶"],
  why="8.1 × 10⁻³⁷ is the gravitational-to-electrostatic ratio. 2.1 × 10⁹ forgets to square the mass. The last "
      "option wrongly makes the ratio depend on r, although both forces fall off as 1/r².",
  ncert=ESC + "Coulomb's law", seconds=75, rc=True)

Qf, Kd = F(40), 5
Qp = Qf * (1 - F(1, Kd))
assert Qp == 32 and Qf / Kd == 8
q(ES, "Capacitors and dielectrics", "Intermediate", "numerical",
  "An isolated parallel plate capacitor carries charges +40 μC and −40 μC on its plates. A slab of dielectric "
  "constant 5 is slid in so that it completely fills the space between the plates. The magnitude of the charge "
  "induced (by polarisation) on each face of the slab is:",
  *opt("32 μC", ["8 μC", "200 μC", "40 μC"], "D"),
  "Polarisation of a dielectric: induced surface charge reduces the field to E₀/K",
  "The free charge Q on the plates stays 40 μC (the capacitor is isolated). The face of the slab next to the "
  "positive plate acquires a charge −Q_p and the other face +Q_p. The field inside the slab is due to the net "
  "charge Q − Q_p, and it must be 1/K of the field without the slab.",
  ["(Q − Q_p) = Q/K", "Q_p = Q(1 − 1/K) = 40 × (1 − 1/5)", "Q_p = 32 μC"],
  why="8 μC is Q/K, the net (free minus induced) charge, not the induced charge. 200 μC multiplies by K; the induced "
      "charge can never exceed the free charge. 40 μC would cancel the field inside completely, which happens in a "
      "conductor, not a dielectric.",
  ncert=ESP + "dielectrics and polarisation", seconds=60, rc=True)

Cc, Vv = 20e-12, 100
Ui = 0.5 * Cc * Vv ** 2
Uf = (Cc * Vv) ** 2 / (2 * (Cc / 2))
close(Ui, 1e-7)
close(Uf - Ui, 1e-7)
close(Uf, 2e-7)
q(ES, "Capacitors and dielectrics", "Intermediate", "numerical",
  "A 20 pF parallel plate capacitor with air between its plates is charged to 100 V and then disconnected from the "
  "battery. Its plates are now slowly pulled apart until their separation is doubled. The work done by the agent "
  "pulling the plates apart is:",
  *opt("1 × 10⁻⁷ J", ["2 × 10⁻⁷ J", "−5 × 10⁻⁸ J", "zero"], "B"),
  "With the battery disconnected the charge stays constant; U = Q²/(2C)",
  "Doubling the separation halves the capacitance. With Q fixed, the stored energy Q²/(2C) doubles. The plates "
  "attract each other, so the agent does positive work, equal to the increase in stored energy.",
  ["Initial energy U = ½CV² = ½ × 20 × 10⁻¹² × 100² = 1 × 10⁻⁷ J",
   "C → C/2 with Q fixed → U → 2U = 2 × 10⁻⁷ J", "Work done = 2 × 10⁻⁷ − 1 × 10⁻⁷ = 1 × 10⁻⁷ J"],
  why="2 × 10⁻⁷ J is the final stored energy, not the increase. −5 × 10⁻⁸ J treats the voltage as fixed (as if the "
      "battery stayed connected), which would halve the energy. The work is not zero: the attracting plates must be "
      "pulled apart.",
  ncert=ESP + "energy stored in a capacitor", seconds=75, rc=True)

q(ES, "Electric potential and energy", "Intermediate", "match_list",
  ml("Match List-I (physical quantity) with List-II (its dimensional formula). A stands for the dimension of "
     "electric current.",
     ["Electric field", "Electric potential", "Capacitance", "Permittivity of free space, ε₀"],
     ["[M⁻¹ L⁻³ T⁴ A²]", "[M L T⁻³ A⁻¹]", "[M⁻¹ L⁻² T⁴ A²]", "[M L² T⁻³ A⁻¹]"]),
  *mlo("A-II, B-IV, C-III, D-I", ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-IV, B-II, C-I, D-III"], "C"),
  "Dimensions from defining relations: E = F/q, V = W/q, C = Q/V, ε₀ = C d/A",
  "Charge has dimensions [A T]. E = F/q = [M L T⁻²]/[A T] = [M L T⁻³ A⁻¹]. V = W/q = [M L² T⁻²]/[A T] = "
  "[M L² T⁻³ A⁻¹]. C = Q/V = [A T]/[M L² T⁻³ A⁻¹] = [M⁻¹ L⁻² T⁴ A²]. ε₀ = Cd/A has one more L⁻¹ than C: "
  "[M⁻¹ L⁻³ T⁴ A²] (its unit is F/m).",
  ["E → II", "V → IV", "C → III", "ε₀ → I"],
  why="Swapping E and V confuses N/C with J/C (they differ by one power of length). Swapping C and ε₀ forgets that "
      "ε₀ is capacitance per unit length (F/m).",
  seconds=60)

q(ES, "Gauss's law", "Intermediate", "statement_pair",
  sp("Two large, thin, parallel plane sheets carry the same uniform surface charge density +σ. In the region "
     "between the sheets (away from the edges), the electric field is zero.",
     "For the same two sheets, the electric field in the region outside them (away from the edges) has magnitude "
     "σ/(2ε₀)."),
  SP, sp_key(True, False),
  "Field of a large plane sheet, σ/(2ε₀), and superposition",
  "Each sheet produces a field of magnitude σ/(2ε₀) directed away from it on both sides. Between the sheets the two "
  "fields are opposite and cancel, so Statement I is true. Outside, both fields point the same way and add to "
  "σ/ε₀, so Statement II is false.",
  ["Between: σ/(2ε₀) − σ/(2ε₀) = 0 → I true", "Outside: σ/(2ε₀) + σ/(2ε₀) = σ/ε₀ → II false"],
  why="σ/(2ε₀) is the field of a single sheet; outside two like sheets the fields add.",
  ncert=ESC + "applications of Gauss's law: field due to a uniformly charged infinite plane sheet", seconds=50)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(ES, "Electric field and dipole", "Intermediate", "multi_statement",
  ms("An electric dipole of dipole moment p is placed in a non-uniform electric field E. Which of the following "
     "statements are correct?",
     ["In general, the dipole experiences both a net force and a torque.",
      "If p is parallel to E, the net force on the dipole is in the direction of increasing field.",
      "If p is antiparallel to E, the net force on the dipole is in the direction of decreasing field.",
      "If p is parallel to E, the torque on the dipole is maximum.",
      "If p is antiparallel to E, the torque on the dipole is maximum."]),
  *mso(truth, "abc", ["abd", "bce", "ad"], "B"),
  "Dipole in a non-uniform field: torque p × E and a net force that depends on how E varies",
  "In a non-uniform field the forces qE on the two charges are unequal, so there is in general a net force as well "
  "as a torque. With p parallel to E the dipole is pulled towards the stronger field; with p antiparallel it is "
  "pushed towards the weaker field (NCERT states both). The torque p × E has magnitude pE sin θ, which is zero (not "
  "maximum) when p is parallel or antiparallel to E.",
  ["(a) true", "(b) true", "(c) true", "(d) false: sin 0° = 0, torque zero", "(e) false: sin 180° = 0, torque zero"],
  why="Any option containing (d) or (e) treats the aligned positions as positions of maximum torque; the torque is "
      "maximum when p is perpendicular to E.",
  ncert=ESC + "dipole in a uniform external field", seconds=70)

# ---- Advanced
Q_end = F(8)
q_mid = -Q_end / 4
assert Q_end * Q_end / 4 + Q_end * q_mid == 0 and q_mid == -2
q(ES, "Coulomb's law and superposition", "Advanced", "numerical",
  "Two point charges, each of +8 μC, are fixed at x = 0 and x = 2a on the x-axis. A third point charge q is placed "
  "at x = a. For all three charges to be in equilibrium under their mutual electrostatic forces alone, q must be:",
  *opt("−2 μC", ["+2 μC", "−8 μC", "−4 μC"], "D"),
  "Equilibrium of a system of charges: net Coulomb force on each charge zero",
  "The middle charge is in equilibrium for any q, by symmetry. For the charge at x = 0, the repulsion from the "
  "other +8 μC charge (distance 2a) must be balanced by an attraction towards the middle charge (distance a), so q "
  "must be negative.",
  ["Force on the end charge from the other end: k(8)(8)/(2a)² = 16k/a² (away)",
   "Force from q: k(8)|q|/a² (towards q, if q is negative)", "8|q| = 16 → |q| = 2 μC, negative"],
  shortcut="q = −Q/4 for equal charges Q at the ends.",
  why="+2 μC has the right size but would repel the end charges. −8 μC ignores that the middle charge is at half "
      "the distance. −4 μC uses distances a and 2a without squaring them.",
  ncert=ESC + "forces between multiple charges", seconds=75, rc=True)

r1, r2, Qt = F(1, 10), F(2, 10), F(5)
Q1 = Qt * r1 ** 2 / (r1 ** 2 + r2 ** 2)
Q2 = Qt - Q1
assert Q1 == 1 and Q2 == 4 and Q1 / (4 * r1 ** 2) == Q2 / (4 * r2 ** 2)
Vc = 9 * (Q1 / r1 + Q2 / r2)       # k × 1e-9 = 9
assert Vc == 270 and 9 * Qt / r1 == 450 and 9 * (4 / r1 + 1 / r2) == 405 and 9 * Qt / r2 == 225
q(ES, "Electric potential and energy", "Advanced", "numerical",
  "A total charge of 5 nC is shared between two thin concentric conducting spherical shells of radii 10 cm and "
  "20 cm (kept insulated from each other) so that the two shells have equal surface charge densities. Taking "
  "1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electric potential at the common centre is:",
  *opt("270 V", ["450 V", "405 V", "225 V"], "A"),
  "Potential due to a charged spherical shell; superposition of potentials",
  "Equal surface densities mean the charges are in the ratio of the areas, r₁² : r₂² = 1 : 4, so the shells carry "
  "1 nC and 4 nC. Inside a shell its potential is constant and equal to kQ/R, so at the centre each shell "
  "contributes kQ/R.",
  ["Q₁ : Q₂ = 10² : 20² = 1 : 4 → Q₁ = 1 nC, Q₂ = 4 nC",
   "V = k(Q₁/r₁ + Q₂/r₂) = 9 × 10⁹ × (10⁻⁹/0.1 + 4 × 10⁻⁹/0.2)", "V = 9 × (10 + 20) = 270 V"],
  why="450 V puts the whole 5 nC on the inner shell. 405 V divides the charge in the inverse ratio (4 nC on the "
      "inner shell). 225 V puts all the charge on the outer shell.",
  ncert=ESP + "potential due to a system of charges", seconds=100, rc=True)

C1, V1, Vc2 = F(5), F(200), F(40)
Ctot = C1 * V1 / Vc2
C2 = Ctot - C1
heat = F(1, 2) * C1 * V1 ** 2 - F(1, 2) * Ctot * Vc2 ** 2      # in μJ
assert C2 == 20 and heat == 80000 and F(1, 2) * Ctot * Vc2 ** 2 == 20000 and F(1, 2) * C2 * Vc2 ** 2 == 16000
assert heat == F(1, 2) * C1 * C2 / (C1 + C2) * V1 ** 2
q(ES, "Capacitors and dielectrics", "Advanced", "numerical",
  "A 5 μF capacitor charged to 200 V is disconnected from the battery and connected across an uncharged capacitor "
  "of unknown capacitance. The common potential difference across the two capacitors settles at 40 V. The energy "
  "dissipated (as heat and radiation) during the redistribution of charge is:",
  *opt("0.08 J", ["0.02 J", "0.1 J", "0.016 J"], "C"),
  "Conservation of charge when capacitors are connected; stored energy ½CV²",
  "Charge is conserved: 5 μF × 200 V = 1000 μC is shared between the two capacitors at 40 V, so the total "
  "capacitance is 25 μF and the unknown capacitor is 20 μF. The energy lost is the initial stored energy minus the "
  "final stored energy.",
  ["Q = 5 μF × 200 V = 1000 μC; total C = 1000/40 = 25 μF → unknown C = 20 μF",
   "Initial energy = ½ × 5 × 10⁻⁶ × 200² = 0.1 J", "Final energy = ½ × 25 × 10⁻⁶ × 40² = 0.02 J",
   "Energy dissipated = 0.1 − 0.02 = 0.08 J"],
  shortcut="Loss = ½ [C₁C₂/(C₁ + C₂)] V₁² = ½ × 4 μF × (200 V)² = 0.08 J.",
  why="0.02 J is the energy finally stored. 0.1 J is the energy initially stored. 0.016 J is the energy finally "
      "stored in the 20 μF capacitor alone.",
  ncert=ESP + "energy stored in a capacitor", seconds=110, rc=True)

q(ES, "Capacitors and dielectrics", "Advanced", "assertion_reason",
  ar("When a dielectric slab that completely fills the space between the plates is inserted into an air-filled "
     "parallel plate capacitor that remains connected to a battery, the electric field between the plates does not "
     "change.",
     "With the battery connected, the potential difference V between the plates and the plate separation d both "
     "stay the same, and the uniform field between the plates is E = V/d."),
  AR, ar_key(True, True, True),
  "Capacitor with a dielectric: which quantity is held fixed",
  "The familiar result that a dielectric reduces the field to E₀/K applies when the charge is fixed (isolated "
  "capacitor). With the battery connected, V is fixed; the field in the filled gap is V/d, so it cannot change. The "
  "battery supplies extra charge (K times the original) so that the field of the free charges, reduced by the "
  "polarisation charges, is again V/d. R states exactly why A holds.",
  ["A: V fixed, d fixed → E = V/d unchanged → true", "R: true, and it is the reason for A"],
  why="Students who apply E₀/K regardless of the battery would mark A false; that rule needs the charge to be "
      "fixed. R is not an unrelated fact; it is the derivation of A.",
  ncert=ESP + "effect of dielectric on capacitance", seconds=60)

Cb = F(50, 10 ** 6)
Wb = Cb * (12 - 4) * 12
dU = F(1, 2) * Cb * (12 ** 2 - 4 ** 2)
assert Wb == F(48, 10 ** 4) and dU == F(32, 10 ** 4) and Wb - dU == F(16, 10 ** 4) == F(1, 2) * Cb * 8 ** 2
q(ES, "Capacitors and dielectrics", "Advanced", "numerical",
  "A 50 μF capacitor already charged to 4 V is connected, through a resistor and with like terminals joined, to a "
  "12 V battery of negligible internal resistance, and is left until it is fully charged to 12 V. The heat produced "
  "in the resistor during this process is:",
  *opt("1.6 mJ", ["3.2 mJ", "4.8 mJ", "2.4 mJ"], "B"),
  "Energy balance in charging: work done by the battery = increase in stored energy + heat",
  "The battery moves the extra charge ΔQ = C(12 − 4) through its emf of 12 V, so it does work ΔQ × 12 V. Only part of "
  "this goes into the capacitor's stored energy; the rest is dissipated in the resistor.",
  ["ΔQ = 50 μF × 8 V = 400 μC; battery work = 400 μC × 12 V = 4.8 mJ",
   "Increase in stored energy = ½ × 50 μF × (12² − 4²) V² = 3.2 mJ", "Heat = 4.8 − 3.2 = 1.6 mJ"],
  shortcut="Heat = ½C(ΔV)² = ½ × 50 μF × 8² = 1.6 mJ when a battery tops up a capacitor through a resistor.",
  why="3.2 mJ is the increase in stored energy. 4.8 mJ is the work done by the battery. 2.4 mJ assumes that half of "
      "the battery's work always becomes heat, which is true only when the capacitor starts uncharged.",
  ncert=ESP + "energy stored in a capacitor", seconds=110, rc=True)
