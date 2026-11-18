

# ================================================================ Magnetic Effects of Current and Magnetism (B5 I7 A5)
MCC = NC + "'Moving Charges and Magnetism', "
MMC = NC + "'Magnetism and Matter', "

# ---- Basic
chi = F(-2, 100000)
assert 1 + chi == F(99998, 100000)
q(MAG, "Magnetic materials", "Basic", "numerical",
  "The magnetic susceptibility of a material is −2.0 × 10⁻⁵. Its relative magnetic permeability and the class of "
  "magnetic material it belongs to are:",
  *opt("0.99998; diamagnetic", ["1.00002; paramagnetic", "−2.0 × 10⁻⁵; diamagnetic", "0.99998; paramagnetic"], "B"),
  "Relative permeability μ_r = 1 + χ; a small negative χ (μ_r slightly less than 1) marks a diamagnetic material",
  "Susceptibility and relative permeability are related by μ_r = 1 + χ. A small negative susceptibility means the "
  "material is magnetised weakly opposite to the applied field, which is diamagnetism.",
  ["μ_r = 1 + (−2.0 × 10⁻⁵) = 0.99998", "χ small and negative (μ_r < 1) → diamagnetic"],
  why="1.00002 adds the magnitude of χ and would describe a paramagnetic material. −2.0 × 10⁻⁵ is χ itself, not "
      "μ_r. A paramagnetic material has μ_r slightly greater than 1.",
  ncert=MMC + "magnetic properties of materials", seconds=35, rc=True)

Fmax = 0.20 * 5 * 0.4
close(Fmax, 0.40)
close(20 * 5 * 0.4, 40)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A straight wire 20 cm long carries a current of 5 A in a uniform magnetic field of 0.4 T. As the orientation of "
  "the wire in the field is changed, the largest and the smallest possible magnitudes of the magnetic force on it "
  "are, respectively:",
  *opt("0.40 N and zero", ["0.40 N and 0.20 N", "40 N and zero", "0.20 N and zero"], "A"),
  "Force on a straight current-carrying conductor: F = I l B sin θ",
  "The force is largest when the wire is perpendicular to the field (sin θ = 1) and zero when the wire lies along the "
  "field (sin θ = 0).",
  ["F_max = I l B = 5 × 0.20 × 0.4 = 0.40 N", "F_min = 0 (wire parallel to B)"],
  why="0.20 N is the force at 30° (sin 30° = ½); it is not a minimum. 40 N keeps the length in centimetres. "
      "0.20 N as the maximum halves the correct value.",
  ncert=MCC + "magnetic force on a current-carrying conductor", seconds=30, rc=True)

q(MAG, "Magnetic materials", "Basic", "statement_pair",
  sp("A ferromagnetic material consists of domains; a typical domain is about 1 mm across and contains about 10¹¹ "
     "atoms whose magnetic moments are aligned in the same direction.",
     "When a paramagnetic sample is kept in a fixed weak magnetic field and its temperature is raised, its "
     "magnetisation increases."),
  SP, sp_key(True, False),
  "Domains in ferromagnets; effect of temperature on paramagnets",
  "Statement I is NCERT's description of domains. Statement II is false: in a paramagnet, thermal agitation "
  "randomises the atomic dipoles, so at higher temperature fewer of them line up with the field and the "
  "magnetisation decreases (Curie's law, M ∝ B/T).",
  ["I: domain ≈ 1 mm, ≈ 10¹¹ atoms → true", "II: M ∝ 1/T for a paramagnet → false"],
  why="Statement II reverses the effect of temperature on a paramagnet.",
  ncert=MMC + "ferromagnetism; paramagnetism", seconds=40)

q(MAG, "Magnetic dipole and bar magnet", "Basic", "direct",
  "A square loop of wire lies in the x–y plane and carries a steady current that circulates anticlockwise when "
  "viewed from a point on the positive z-axis. The magnetic dipole moment of the loop is directed along:",
  *opt("the +z axis", ["the −z axis", "the +x axis", "the diagonal of the square, in the plane of the loop"], "D"),
  "Magnetic moment of a current loop: m = I A, with A along the normal given by the right-hand rule",
  "The magnetic moment is perpendicular to the plane of the loop. Curling the fingers of the right hand in the "
  "direction of the current, the thumb points along m. An anticlockwise current seen from +z gives m along +z.",
  ["m ⊥ plane of loop", "Right-hand rule: anticlockwise seen from +z → m along +z"],
  why="−z would correspond to a clockwise current seen from +z. A magnetic moment never lies in the plane of a "
      "plane loop, so +x and the diagonal are both wrong.",
  ncert=MCC + "the current loop as a magnetic dipole", seconds=30)

q(MAG, "Magnetic materials", "Basic", "assertion_reason",
  ar("The magnetic field inside a long current-carrying solenoid becomes much stronger when a soft iron core is "
     "placed inside it.",
     "Soft iron is ferromagnetic, with a relative permeability very much larger than 1, so it is strongly magnetised "
     "along the field of the solenoid."),
  AR, ar_key(True, True, True),
  "Field in a solenoid filled with a material: B = μ₀μ_r n I",
  "With the core in place, the field is μ_r times the field of the empty solenoid. For soft iron μ_r is very large "
  "(its domains line up readily with the applied field), so the field increases greatly. R is the cause of A.",
  ["Empty solenoid: B₀ = μ₀ n I", "With core: B = μ_r B₀, μ_r ≫ 1 for soft iron", "R explains A"],
  why="R is not a separate property of iron; the strong magnetisation of the core is exactly why the field grows.",
  ncert=MMC + "ferromagnetism", seconds=35)

# ---- Intermediate
B0, chi_p = 2.5e-3, 2.0e-4
dB = chi_p * B0
close(dB, 5.0e-7)
close((1 + chi_p) * B0, 2.5005e-3)
close(chi_p * 100 * B0, 5.0e-5)
q(MAG, "Magnetic materials", "Intermediate", "numerical",
  "The magnetic field well inside a long, air-filled solenoid carrying a steady current is 2.5 mT. The solenoid is "
  "completely filled with a paramagnetic material of magnetic susceptibility 2.0 × 10⁻⁴, the current being kept "
  "the same. The magnetic field inside the solenoid:",
  *opt("increases by 5.0 × 10⁻⁷ T", ["decreases by 5.0 × 10⁻⁷ T", "becomes 5.0 × 10⁻⁷ T",
                                     "increases by 5.0 × 10⁻⁵ T"], "C"),
  "Field in a material: B = µ₀µ_r H with µ_r = 1 + χ; a paramagnetic material has a small positive χ",
  "With the current unchanged, the field inside becomes µ_r = 1 + χ times the field of the empty solenoid. For a "
  "paramagnetic material χ is small and positive, so the field increases slightly; the increase is χ times the "
  "original field.",
  ["B = (1 + χ)B₀", "Increase = χB₀ = 2.0 × 10⁻⁴ × 2.5 × 10⁻³ T = 5.0 × 10⁻⁷ T"],
  why="'Decreases' is what a diamagnetic material (χ < 0) would do. 'Becomes 5.0 × 10⁻⁷ T' multiplies B₀ by χ "
      "instead of by 1 + χ, leaving almost no field. 5.0 × 10⁻⁵ T treats χ as a percentage (×100).",
  ncert=MMC + "magnetisation and magnetic intensity; paramagnetism", seconds=50, rc=True)

G_, Ig, Ir = F(60), F(3, 100), F(3)
S_ = Ig * G_ / (Ir - Ig)
RA = G_ * S_ / (G_ + S_)
assert RA == F(6, 10) and RA == Ig * G_ / Ir and round(float(S_), 3) == 0.606 and round(float(G_ + S_), 1) == 60.6
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A galvanometer of resistance 60 Ω gives full-scale deflection for a current of 30 mA. It is converted into an "
  "ammeter of range 0–3 A by connecting a suitable shunt. The resistance of the ammeter so formed (galvanometer and "
  "shunt together) is:",
  *opt("0.60 Ω", ["0.606 Ω", "60.6 Ω", "60 Ω"], "D"),
  "Conversion of a galvanometer into an ammeter: a low resistance shunt S in parallel",
  "At full scale, 30 mA flows through the galvanometer and the remaining 2.97 A through the shunt, both having the "
  "same potential difference I_g G across them. The ammeter's resistance is the parallel combination of G and S, "
  "which is also (I_g G)/I.",
  ["PD at full scale = 0.030 × 60 = 1.8 V", "S = 1.8/2.97 ≈ 0.606 Ω",
   "R_ammeter = G S/(G + S) = 1.8 V / 3 A = 0.60 Ω"],
  shortcut="R_ammeter = (full-scale PD)/(full-scale current) = 1.8/3 = 0.60 Ω.",
  why="0.606 Ω is the shunt alone. 60.6 Ω adds G and S as if they were in series. 60 Ω ignores the shunt.",
  ncert=MCC + "moving coil galvanometer", seconds=60, rc=True)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "match_list",
  ml("Match List-I (physical quantity) with List-II (an SI unit in which it can be expressed).",
     ["Magnetisation (magnetic moment per unit volume)", "Magnetic susceptibility",
      "Magnetic dipole moment", "Current sensitivity of a moving-coil galvanometer"],
     ["A m⁻¹", "no unit (a pure number)", "J T⁻¹", "rad A⁻¹"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-III, B-II, C-I, D-IV", "A-I, B-IV, C-III, D-II", "A-II, B-I, C-III, D-IV"], "B"),
  "Units from definitions: M = m/V, χ = M/H, U = −m·B, current sensitivity φ/I",
  "Magnetisation is magnetic moment (A m²) per unit volume (m³): A m⁻¹. Susceptibility is the ratio of two "
  "quantities with the same unit (M and H), so it has none. From U = −m·B, m has the unit J T⁻¹ (equivalent to "
  "A m²). Current sensitivity is deflection per unit current: rad A⁻¹.",
  ["A → I", "B → II", "C → III", "D → IV"],
  why="The other codes exchange magnetisation with magnetic moment (they differ by a factor of volume), or give "
      "susceptibility a unit although it is a ratio.",
  ncert=MMC + "magnetisation and magnetic intensity", seconds=50)

m_, g_, qq, BB = 1e-3, 10, 1e-6, 0.5
v_lev = m_ * g_ / (qq * BB)
close(v_lev, 2e4)
close(m_ / (qq * BB), 2e3)
close(qq * BB / (m_ * g_), 5e-5)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A small particle of mass 1.0 g carrying a charge of +1.0 μC is projected horizontally, at right angles to a "
  "uniform horizontal magnetic field of 0.50 T, in a direction such that the magnetic force on it is vertically "
  "upwards. Taking g = 10 m/s², the speed with which it must be projected so that it moves along a horizontal straight "
  "line is:",
  *opt("2.0 × 10⁴ m/s", ["2.0 × 10³ m/s", "2.0 × 10⁷ m/s", "5.0 × 10⁻⁵ m/s"], "A"),
  "Magnetic force qvB balancing the weight mg",
  "For straight-line motion the upward magnetic force must cancel the weight exactly. Since v is perpendicular to B, "
  "the force is qvB, and it stays vertical as long as the particle moves horizontally.",
  ["qvB = mg", "v = mg/(qB) = (1.0 × 10⁻³ × 10)/(1.0 × 10⁻⁶ × 0.50)", "v = 2.0 × 10⁴ m/s"],
  why="2.0 × 10³ m/s leaves out g. 2.0 × 10⁷ m/s keeps the mass in grams. 5.0 × 10⁻⁵ m/s inverts the expression.",
  ncert=MCC + "magnetic force", seconds=50, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "multi_statement",
  ms("An electron (charge −e, mass mₑ) revolves with speed v in a circular orbit of radius r round the nucleus, as in "
     "the Bohr model of the hydrogen atom. Its orbital angular momentum is l. Which of the following statements are "
     "correct?",
     ["The magnitude of its orbital magnetic moment is evr/2.",
      "The ratio of the magnitude of its orbital magnetic moment to that of its orbital angular momentum is "
      "e/(2mₑ).",
      "Its orbital magnetic moment points in the same direction as its orbital angular momentum.",
      "The smallest value of the orbital magnetic moment, the Bohr magneton, is about 9.27 × 10⁻²⁴ A m².",
      "The equivalent current of the revolving electron is ev/r."]),
  *mso(truth, "abd", ["abc", "ade", "bcd"], "C"),
  "Magnetic dipole moment of a revolving electron",
  "The revolving electron is a current loop with I = e/T = ev/(2πr), so μ = Iπr² = evr/2. Since l = mₑvr, "
  "μ/l = e/(2mₑ). Because the electron's charge is negative, its magnetic moment is opposite to its angular "
  "momentum: μ = −(e/2mₑ) l. Using Bohr's l = h/2π gives the least value eh/(4πmₑ) ≈ 9.27 × 10⁻²⁴ A m², the Bohr "
  "magneton.",
  ["(a) true", "(b) true", "(c) false: opposite, as the charge is negative", "(d) true",
   "(e) false: I = ev/(2πr)"],
  why="Options with (c) forget the negative charge of the electron; options with (e) leave out the 2π in the period "
      "2πr/v.",
  ncert=MCC + "magnetic dipole moment of a revolving electron", seconds=70)

q(MAG, "Force on charges and conductors", "Intermediate", "statement_pair",
  sp("A charged particle moving along a helix in a uniform magnetic field (no other force acting) has a constant "
     "velocity.",
     "The kinetic energy of such a particle remains constant."),
  SP, sp_key(False, True),
  "Magnetic force is perpendicular to velocity: it changes direction, not speed",
  "The magnetic force q(v × B) is always perpendicular to the velocity, so it does no work: the speed and the kinetic "
  "energy stay constant (Statement II true). But the direction of motion keeps changing round the helix, so the "
  "velocity, a vector, is not constant (Statement I false).",
  ["I: direction changes → velocity not constant → false", "II: F ⊥ v → no work → KE constant → true"],
  why="Statement I confuses constant speed with constant velocity.",
  ncert=MCC + "motion in a magnetic field", seconds=40)

q(MAG, "Biot-Savart law", "Intermediate", "direct",
  "Two identical circular loops of wire are placed coaxially, a short distance apart, in parallel planes. They carry "
  "steady currents circulating in the same sense when viewed along the common axis. The loops will:",
  *opt("attract each other", ["repel each other", "exert no force on each other, since their fields are parallel",
                              "rotate so that their planes become perpendicular"], "B"),
  "Force between parallel currents; a current loop as a magnetic dipole",
  "Facing portions of the two loops carry currents in the same direction, and parallel currents in the same "
  "direction attract. Equivalently, each loop is a magnetic dipole and the two moments point the same way along the "
  "common axis, so the north face of one faces the south face of the other.",
  ["Adjacent segments carry parallel currents → attraction",
   "Dipole picture: moments aligned along the axis, N of one facing S of the other → attraction"],
  why="Repulsion would need opposite senses of circulation. The loops do exert forces on each other. Coaxial loops "
      "with aligned moments are already in equilibrium as far as torque is concerned, so they do not turn.",
  ncert=MCC + "force between two parallel currents; the current loop as a magnetic dipole", seconds=40)

# ---- Advanced
Bt, It, Rt_ = 0.5, 4, 0.10
T_loop = Bt * It * Rt_
close(T_loop, 0.2)
close(2 * Bt * It * Rt_, 0.4)
close(2 * math.pi * Rt_ * Bt * It, 1.2566)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A thin flexible circular loop of wire of radius 10 cm lies in a plane perpendicular to a uniform magnetic field of "
  "0.50 T and carries a current of 4.0 A, in the sense for which the magnetic forces on it act outwards (away from "
  "its centre) everywhere. The tension in the wire is:",
  *opt("0.20 N", ["0.40 N", "1.3 N", "zero, because the net force on the loop is zero"], "D"),
  "Force on a curved conductor in a uniform field; equilibrium of half the loop",
  "Consider one half of the loop. The magnetic force on a semicircle in a uniform field equals the force on the "
  "straight diameter joining its ends: B I (2R), directed outwards. This half is held in equilibrium by the tension "
  "T acting at each of its two cut ends, both pulling towards the other half: 2T = 2BIR.",
  ["Force on a semicircle = B I × 2R = 0.50 × 4.0 × 0.20 = 0.40 N", "2T = 0.40 N", "T = BIR = 0.20 N"],
  why="0.40 N is the net magnetic force on half the loop, which is shared by two ends. 1.3 N multiplies B I by the "
      "whole circumference, adding force magnitudes that point in different directions. The net force on the whole "
      "loop is zero, but each part is still stretched.",
  ncert=MCC + "magnetic force on a current-carrying conductor", seconds=110, rc=True)

Bw = 2e-7 * 10 / 0.05
Fp = 1.6e-19 * 2e6 * Bw
close(Bw, 4e-5)
close(Fp, 1.28e-17)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A long straight wire carries a steady current of 10 A. At an instant when a proton is 5.0 cm from the wire, it is "
  "moving with a speed of 2.0 × 10⁶ m/s directly towards the wire (along the perpendicular from it to the wire). "
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹ and e = 1.6 × 10⁻¹⁹ C, the magnetic force on the proton at that instant is:",
  *opt("1.28 × 10⁻¹⁷ N, parallel to the wire and opposite to the current",
       ["1.28 × 10⁻¹⁷ N, parallel to the wire and in the direction of the current",
        "1.28 × 10⁻¹⁷ N, directed away from the wire",
        "6.4 × 10⁻¹⁸ N, parallel to the wire and opposite to the current"], "C"),
  "Field of a long straight wire; Lorentz force F = q v × B",
  "Take the wire along the z-axis with the current along +z, and the proton on the +x axis moving in the −x "
  "direction. At that point the field is along +y (right-hand rule). Then v × B = (−v x̂) × (B ŷ) = −vB ẑ, so the "
  "force is parallel to the wire and opposite to the current.",
  ["B = µ₀I/(2πd) = 2 × 10⁻⁷ × 10/0.05 = 4.0 × 10⁻⁵ T", "|F| = evB = 1.6 × 10⁻¹⁹ × 2.0 × 10⁶ × 4.0 × 10⁻⁵ "
   "= 1.28 × 10⁻¹⁷ N", "Direction: (−x̂) × ŷ = −ẑ → opposite to the current"],
  why="'In the direction of the current' reverses the cross product. 'Away from the wire' is the direction for a "
      "proton moving parallel to the current in the opposite direction, not one moving towards the wire. "
      "6.4 × 10⁻¹⁸ N uses µ₀I/(4πd) for the field, half the correct value.",
  ncert=MCC + "Ampere's circuital law (field of a straight wire); magnetic force",
  seconds=120, rc=True)

Gv, Igv = F(50), F(2, 1000)
R1v = 5 / Igv - Gv
R2v = 20 / Igv - Gv - R1v
assert R1v == 2450 and R2v == 7500 and 20 / Igv - Gv == 9950
q(MAG, "Torque on loop and galvanometer", "Advanced", "numerical",
  "A galvanometer of resistance 50 Ω gives full-scale deflection for a current of 2.0 mA. It is made into a "
  "two-range voltmeter: a resistor R₁ in series with the galvanometer gives the 0–5 V range, and a further resistor "
  "R₂ added in series with R₁ (between R₁ and a second terminal) gives the 0–20 V range. The values of R₁ and R₂ "
  "are:",
  *opt("2450 Ω and 7500 Ω", ["2500 Ω and 10 000 Ω", "2450 Ω and 9950 Ω", "2500 Ω and 7500 Ω"], "A"),
  "Galvanometer as a voltmeter: total resistance = range ÷ full-scale current",
  "On the 5 V range the total resistance must be 5/0.002 = 2500 Ω, which includes the 50 Ω galvanometer. On the "
  "20 V range the total must be 20/0.002 = 10 000 Ω, which includes both the galvanometer and R₁.",
  ["R₁ = 5/0.002 − 50 = 2450 Ω", "R₁ + R₂ + 50 = 10 000 Ω", "R₂ = 10 000 − 2500 = 7500 Ω"],
  why="2500 Ω and 10 000 Ω are the total resistances of the two ranges, not the added resistors. 9950 Ω is the "
      "resistor needed for 20 V on its own, forgetting that R₁ is already in the circuit. 2500 Ω for R₁ ignores the "
      "galvanometer's own resistance.",
  ncert=MCC + "moving coil galvanometer", seconds=100, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": True}
q(MAG, "Force on charges and conductors", "Advanced", "multi_statement",
  ms("In a region there are a uniform electric field E and a uniform magnetic field B, both directed along the +z "
     "axis. A positively charged particle is introduced into the region (gravity negligible). Which of the following "
     "statements are correct?",
     ["If it is released from rest, it moves along a straight line parallel to the z-axis with uniform "
      "acceleration.",
      "If its initial velocity is perpendicular to the z-axis, it moves along a helix about an axis parallel to z, "
      "advancing a greater distance along z in each successive turn.",
      "Its speed remains constant whatever its initial velocity.",
      "The magnetic force on it does no work.",
      "The time it takes for each turn round the z-direction is 2πm/(qB), the same for every turn."]),
  *mso(truth, "abde", ["abcd", "ade", "bcde"], "B"),
  "Superposition of the motions due to E and B when the fields are parallel",
  "The electric force qE is along z and changes only the z-component of velocity, uniformly. The magnetic force acts "
  "only on the velocity component perpendicular to B (which E does not change), giving uniform circular motion in "
  "the x–y projection with period 2πm/(qB). Released from rest, there is no perpendicular velocity and the particle "
  "simply accelerates along z. With a perpendicular initial velocity the path is a helix whose step along z grows "
  "each turn, because v_z keeps increasing. The magnetic force is always perpendicular to the velocity and does no "
  "work, but the electric force does work, so the speed is not constant.",
  ["(a) true", "(b) true", "(c) false: E does work", "(d) true", "(e) true: period independent of speed"],
  why="Options with (c) forget that the electric field does work on the charge; the options leaving out (b) or (e) "
      "miss that the circular part of the motion depends only on B.",
  ncert=MCC + "motion in a magnetic field; motion in combined electric and magnetic fields", seconds=100)

KE_e, B_e = 100 * 1.6e-19, 1.0e-3
mu_e = KE_e / B_e
close(mu_e, 1.6e-14)
m_e = 9.1e-31
v_e = math.sqrt(2 * KE_e / m_e)
r_e = m_e * v_e / (1.6e-19 * B_e)
close(1.6e-19 * v_e * r_e / 2, mu_e, 1e-9)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "An electron with a kinetic energy of 100 eV moves in a circle in a plane perpendicular to a uniform magnetic field "
  "of 1.0 mT (1 eV = 1.6 × 10⁻¹⁹ J). Treating the circulating electron as a current loop, the magnitude of its "
  "magnetic dipole moment and its direction relative to the field are:",
  *opt("1.6 × 10⁻¹⁴ A m², opposite to the field",
       ["1.6 × 10⁻¹⁴ A m², along the field", "3.2 × 10⁻¹⁴ A m², opposite to the field",
        "1.6 × 10⁻²⁰ A m², opposite to the field"], "D"),
  "Magnetic moment of a circulating charge, μ = IA with I = q/T; radius r = mv/(qB)",
  "For a charge circulating in a field B: I = e/T = e²B/(2πm) and A = πr² with r = mv/(eB). Then "
  "μ = IA = e²B r²/(2m) = (½mv²)/B, the kinetic energy divided by the field. The sense of circulation is such that "
  "the moment opposes the applied field (for either sign of charge), the same tendency that underlies diamagnetism.",
  ["μ = evr/2 with r = mv/(eB) → μ = mv²/(2B) = KE/B", "KE = 100 × 1.6 × 10⁻¹⁹ = 1.6 × 10⁻¹⁷ J",
   "μ = 1.6 × 10⁻¹⁷/1.0 × 10⁻³ = 1.6 × 10⁻¹⁴ A m², opposite to B"],
  why="'Along the field' gets the sense of circulation wrong: an electron in a field B along +z circulates "
      "anticlockwise seen from +z, so the conventional current is clockwise and the moment points along −z. "
      "3.2 × 10⁻¹⁴ A m² uses mv²/B, dropping the ½. 1.6 × 10⁻²⁰ A m² multiplies KE by B instead of dividing.",
  ncert=MCC + "motion in a magnetic field; magnetic dipole moment of a revolving electron", seconds=140, rc=True)
