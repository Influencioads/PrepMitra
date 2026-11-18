

# ================================================================ Electromagnetic Induction and AC (B4 I5 A4)
EMC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
U_, I_l = F(4, 10), F(2)
L_ = 2 * U_ / I_l ** 2
assert L_ == F(1, 5) and U_ / I_l ** 2 == F(1, 10) and 2 * U_ / I_l == F(2, 5) and U_ / (2 * I_l ** 2) == F(1, 20)
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "When a steady current of 2.0 A flows through a coil, the energy stored in its magnetic field is 0.40 J. The "
  "self-inductance of the coil is:",
  *opt("0.20 H", ["0.10 H", "0.40 H", "0.05 H"], "C"),
  "Magnetic energy stored in an inductor: U = ½ L I²",
  "Rearranging U = ½LI² gives L = 2U/I².",
  ["L = 2U/I² = 2 × 0.40/2.0²", "L = 0.80/4.0 = 0.20 H"],
  why="0.10 H drops the factor ½ from U = ½LI². 0.40 H divides by I instead of I². 0.05 H puts the ½ on the wrong "
      "side of the equation.",
  ncert=EMC + "self-inductance", seconds=30, rc=True)

q(EMI, "Self and mutual inductance", "Basic", "direct",
  "For a coil of self-inductance L and resistance R, the ratio L/R has the dimensions of:",
  *opt("time", ["frequency", "resistance", "a pure number (it is dimensionless)"], "A"),
  "Dimensional analysis using ε = L dI/dt and V = IR",
  "From ε = L (dI/dt), the unit of L is V s A⁻¹ = Ω s. Dividing by the unit of R (Ω) leaves seconds, so L/R has the "
  "dimensions of time. (It is the time constant of an L–R circuit.)",
  ["[L] = V s A⁻¹ = Ω s", "[L/R] = Ω s / Ω = s → time"],
  why="Frequency would be R/L, the inverse. L/R is not a resistance and it is not dimensionless, since the henry "
      "is an ohm-second.",
  ncert=EMC + "self-inductance", seconds=30)

assert F(1, 2) ** 2 == F(1, 4)
q(EMI, "LCR resonance and power", "Basic", "numerical",
  "A series LCR circuit is in resonance at a frequency f₀. Keeping L and R unchanged, the capacitance C must be "
  "changed to which value so that the resonant frequency becomes 2f₀?",
  *opt("C/4", ["C/2", "2C", "4C"], "D"),
  "Resonant frequency f₀ = 1/(2π√(LC))",
  "The resonant frequency varies inversely as the square root of C. To double it with L fixed, √C must be halved, "
  "so C must become one quarter.",
  ["f ∝ 1/√C", "2f₀ → √C' = √C/2 → C' = C/4"],
  why="C/2 treats f as inversely proportional to C, not to √C. 2C and 4C change C in the wrong direction; they "
      "would lower the resonant frequency.",
  ncert=ACC + "series LCR circuit: resonance", seconds=30, rc=True)

q(EMI, "Self and mutual inductance", "Basic", "statement_pair",
  sp("For a pair of coils, the flux linked with the second coil per unit current in the first equals the flux linked "
     "with the first coil per unit current in the second; that is, M₁₂ = M₂₁.",
     "Self-inductance and mutual inductance are both measured in the same SI unit, the henry."),
  SP, sp_key(True, True),
  "Mutual inductance and its unit",
  "NCERT shows for two long coaxial solenoids that M₁₂ = M₂₁ and states that the relation holds in general, so "
  "Statement I is true. Both inductances are flux linkage per unit current (Wb A⁻¹), the henry, so Statement II is "
  "true.",
  ["I: M₁₂ = M₂₁ → true", "II: unit of both = henry = Wb A⁻¹ → true"],
  why="Both statements are true; neither is a trap.",
  ncert=EMC + "mutual inductance", seconds=35)

# ---- Intermediate
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "direct",
  "A closed coil B (not connected to any battery) is placed close to a coil A, the two being coaxial. A steady "
  "battery is connected to A through a switch. When the switch is closed, coil B is:",
  *opt("repelled from A, but only while the current in A is growing",
       ["attracted towards A, but only while the current in A is growing",
        "repelled from A for as long as the current in A flows",
        "not acted on by any force, since no battery drives a current in B"], "B"),
  "Lenz's law: the induced current opposes the change of flux that produces it",
  "While the current in A grows, the flux through B increases, so the induced current in B circulates in the "
  "opposite sense to the current in A, opposing the increase. Antiparallel currents repel (equivalently, like poles "
  "face each other), so B is pushed away. Once the current in A is steady, the flux through B no longer changes, "
  "the induced current stops and so does the force.",
  ["Growing current in A → increasing flux through B", "Induced current in B opposite to that in A → repulsion",
   "Steady current in A → no induced current → no force"],
  why="Attraction would occur while the current in A is decreasing (for example when the switch is opened). A "
      "steady current induces nothing, so the force does not last. B needs no battery: the changing flux induces a "
      "current in it.",
  ncert=EMC + "Lenz's law and conservation of energy", seconds=45)

Lc, Ic, dIdt = 0.5, 2, 4
P_store = Lc * Ic * dIdt
close(P_store, 4)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "The current in an ideal coil of self-inductance 0.50 H is increasing at a steady rate of 4.0 A/s. At the instant "
  "when the current is 2.0 A, the rate at which energy is being stored in the magnetic field of the coil is:",
  *opt("4.0 W", ["2.0 W", "1.0 W", "8.0 W"], "C"),
  "Energy stored U = ½LI², so dU/dt = L I (dI/dt) = (self-induced emf) × current",
  "The source must push the current against the self-induced emf L dI/dt = 0.50 × 4.0 = 2.0 V. The power it delivers "
  "to the coil, all of which is stored in the field of an ideal coil, is this emf times the current.",
  ["Self-induced emf = L dI/dt = 2.0 V", "dU/dt = emf × I = 2.0 V × 2.0 A = 4.0 W"],
  shortcut="dU/dt = d(½LI²)/dt = LI dI/dt = 0.5 × 2 × 4 = 4 W.",
  why="2.0 W keeps an extra ½ when differentiating ½LI². 1.0 W is the stored energy ½LI² = 1.0 J at that instant, "
      "not its rate of increase. 8.0 W multiplies L by I² and dI/dt.",
  ncert=EMC + "self-inductance", seconds=60, rc=True)

mu0 = 4 * math.pi * 1e-7
Ls = mu0 * 1000 ** 2 * 1e-3 / 0.5
Us = 0.5 * Ls * 2 ** 2
close(Ls, 2.513e-3)
close(Us, 5.03e-3)
close(0.5 * Ls * 2, 2.51e-3)
close(0.5 * mu0 * 1000 ** 2 * 1e-3 * 0.5 * 4, 1.257e-3)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "A long air-cored solenoid is 50 cm long, has 1000 turns and a cross-sectional area of 10 cm², and carries a "
  "steady current of 2.0 A. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the energy stored in its magnetic field is about:",
  *opt("5.0 mJ", ["2.5 mJ", "10 mJ", "1.3 mJ"], "D"),
  "Self-inductance of a long solenoid L = µ₀N²A/l; energy U = ½LI²",
  "First find the self-inductance from the dimensions of the solenoid, then the energy for a current of 2.0 A.",
  ["L = µ₀N²A/l = 4π × 10⁻⁷ × 10⁶ × 10 × 10⁻⁴/0.50 ≈ 2.5 × 10⁻³ H",
   "U = ½LI² = ½ × 2.5 × 10⁻³ × 2.0² ≈ 5.0 × 10⁻³ J = 5.0 mJ"],
  why="2.5 mJ uses ½LI instead of ½LI². 10 mJ drops the ½. 1.3 mJ uses µ₀N²Al, putting the total number of turns N "
      "in place of n = N/l in L = µ₀n²Al.",
  ncert=EMC + "self-inductance", seconds=75, rc=True)

q(EMI, "AC generator and transformer", "Intermediate", "match_list",
  ml("Match each device or effect in List-I with the phenomenon on which it is based in List-II.",
     ["Transformer", "AC generator", "Induction furnace",
      "A spark across the switch when a circuit containing a large coil is suddenly broken"],
     ["Mutual induction", "Self-induction", "Heating by eddy currents",
      "Change of flux linkage of a coil rotated in a magnetic field"]),
  *mlo("A-I, B-IV, C-III, D-II", ["A-II, B-IV, C-III, D-I", "A-I, B-III, C-IV, D-II", "A-IV, B-I, C-III, D-II"], "A"),
  "Applications of electromagnetic induction",
  "A transformer transfers energy from the primary to the secondary through their mutual inductance. An AC "
  "generator produces an emf because the flux linkage of its rotating coil changes continuously. An induction "
  "furnace melts metal using the heat produced by large eddy currents. When a current in a coil of large "
  "self-inductance is cut off quickly, the large self-induced emf can make a spark jump across the switch.",
  ["A → I", "B → IV", "C → III", "D → II"],
  why="The other codes swap self- and mutual induction between the transformer and the spark, or attribute the "
      "generator to eddy currents; eddy currents are a loss in a generator, not its working principle.",
  ncert=EMC + "self-inductance; mutual inductance; eddy currents; AC generator", seconds=50)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "assertion_reason",
  ar("An ideal inductor, which has no resistance, limits the alternating current through it, although it lets a "
     "steady direct current pass without any opposition once the current has become steady.",
     "The emf self-induced in the inductor opposes every change of current in it, giving it a reactance "
     "X_L = ωL, which is zero for a steady current (ω = 0)."),
  AR, ar_key(True, True, True),
  "Inductive reactance X_L = ωL",
  "For an alternating current the current is always changing, so the self-induced emf L(di/dt) always opposes it; "
  "this opposition is the reactance ωL, which limits the rms current to V/(ωL). For a steady current di/dt = 0, the "
  "self-induced emf is zero and an ideal inductor offers no opposition. R gives exactly this reason.",
  ["AC: X_L = ωL > 0 → current limited", "Steady DC: ω = 0 → X_L = 0", "R explains A"],
  why="R is not a separate fact about inductors; the self-induced emf is the cause of the reactance.",
  ncert=ACC + "AC voltage applied to an inductor", seconds=40)

# ---- Advanced
m_r, v0, Rr, Br, lr = F(1, 10), F(2), F(1), F(1, 2), F(4, 10)
X_stop = m_r * v0 * Rr / (Br ** 2 * lr ** 2)
a0 = Br ** 2 * lr ** 2 * v0 / (m_r * Rr)
assert X_stop == 5 and v0 ** 2 / (2 * a0) == F(5, 2)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A metal rod of mass 0.10 kg lies across two smooth, horizontal, parallel conducting rails 0.40 m apart, which are "
  "joined at one end through a 1.0 Ω resistor; the rod and rails have negligible resistance. A uniform vertical "
  "magnetic field of 0.50 T acts on the region. The rod is given a velocity of 2.0 m/s along the rails, away from the "
  "resistor, and is then left to itself. The total distance it moves before coming to rest is:",
  *opt("5.0 m", ["2.5 m", "10 m", "infinite, because the rod never stops completely"], "B"),
  "Motional emf, induced current and the retarding force; charge through the circuit = change of flux / R",
  "The induced current I = Blv/R gives a retarding force BIl. Over the whole motion, the impulse of this force equals "
  "the momentum lost: Bl × (total charge Q) = mv₀. The total charge is the change of flux divided by R: "
  "Q = BlX/R, where X is the distance moved.",
  ["Impulse: Bl Q = m v₀", "Q = ΔΦ/R = BlX/R", "B²l²X/R = m v₀ → X = m v₀ R/(B²l²)",
   "X = 0.10 × 2.0 × 1.0/(0.25 × 0.16) = 5.0 m"],
  why="2.5 m treats the initial retarding force as constant (uniform deceleration), though it falls as the rod slows. "
      "10 m is twice the correct value. The speed decays exponentially, so the rod takes an infinite time to stop, "
      "but the distance covered is finite.",
  ncert=EMC + "motional electromotive force", seconds=150, rc=True)

lw, xw, Bw_, kw, vw = 0.5, 0.4, 0.5, 0.1, 2.0
emf_tot = lw * (xw * kw + Bw_ * vw)
close(emf_tot, 0.52)
close(lw * Bw_ * vw, 0.50)
close(lw * xw * kw, 0.02)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A metal rod slides with a constant speed of 2.0 m/s along two parallel conducting rails 0.50 m apart that are "
  "joined at one end, forming a rectangular circuit whose area grows as the rod moves away from the joined end. A "
  "uniform magnetic field perpendicular to the plane of the rails is increasing at a steady rate of 0.10 T/s. At the "
  "instant when the field is 0.50 T and the rod is 0.40 m from the joined end, the magnitude of the emf induced in the "
  "circuit is:",
  *opt("0.52 V", ["0.50 V", "0.02 V", "0.48 V"], "C"),
  "Faraday's law with both the field and the area changing: Φ = B l x, dΦ/dt = l x (dB/dt) + B l (dx/dt)",
  "Both changes increase the flux through the circuit (the area grows and the field grows), so their contributions "
  "add.",
  ["Flux Φ = B l x", "Term from changing field: l x dB/dt = 0.50 × 0.40 × 0.10 = 0.02 V",
   "Term from moving rod: B l v = 0.50 × 0.50 × 2.0 = 0.50 V", "Total emf = 0.52 V"],
  why="0.50 V keeps only the motional emf. 0.02 V keeps only the part due to the changing field. 0.48 V subtracts "
      "the two parts, although both increase the flux.",
  ncert=EMC + "Faraday's law of induction; motional electromotive force", seconds=110, rc=True)

truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(EMI, "AC: rms, reactance and impedance", "Advanced", "multi_statement",
  ms("A coil of large inductance and small resistance is connected in series with a bulb across an AC supply of "
     "fixed voltage and frequency. A soft-iron rod is then pushed into the coil. Which of the following statements "
     "are correct?",
     ["The self-inductance of the coil increases.",
      "The bulb becomes dimmer.",
      "The power factor of the circuit decreases.",
      "The current in the circuit starts to lead the supply voltage.",
      "If the same arrangement were connected to a steady DC supply instead, pushing the rod in would not change "
      "the steady brightness of the bulb."]),
  *mso(truth, "abce", ["abd", "acde", "bce"], "D"),
  "Inductive reactance X_L = ωL; impedance and power factor of an R–L circuit",
  "Soft iron has a large permeability, so the inductance of the coil increases (a). Then X_L = ωL increases, the "
  "impedance √(R² + X_L²) increases and the current falls, so the bulb dims (b). The power factor R/Z falls (c). In "
  "an R–L circuit the current always lags the voltage (d is false). With steady DC, an inductor offers no opposition "
  "once the current is steady, so the steady current depends only on the resistances (e).",
  ["(a) true", "(b) true", "(c) true: cos φ = R/Z", "(d) false: current lags in an R–L circuit",
   "(e) true: X_L = 0 for steady DC"],
  why="Any option containing (d) makes the inductive circuit capacitive. The options leaving out (c) or (a) miss "
      "the effect of the larger inductance on the power factor or the inductance itself.",
  ncert=ACC + "AC voltage applied to an inductor; power factor", seconds=90)

q(EMI, "Faraday's and Lenz's laws", "Advanced", "direct",
  "A flexible circular loop of wire lies in the plane of the page in a uniform magnetic field directed into the page. "
  "The field is steadily increasing. Because of the current induced in it, the loop tends to:",
  *opt("contract (its area tends to decrease)",
       ["expand (its area tends to increase)", "rotate about one of its diameters",
        "stay unchanged, since the net force on a closed loop in a uniform field is zero"], "B"),
  "Lenz's law; force on the induced current, F = I dl × B",
  "The induced current opposes the increase of the inward flux, so it produces an outward field inside the loop: it "
  "flows anticlockwise as seen by the reader. On each element the force I dl × B (dl anticlockwise, B into the page) "
  "points towards the centre. These inward forces squeeze the loop, tending to reduce its area and hence the flux, as "
  "Lenz's law requires.",
  ["Inward flux increasing → induced current anticlockwise", "F = I dl × B on each element points inwards",
   "Loop tends to contract, reducing the flux"],
  why="Expansion would increase the flux, which is the opposite of what Lenz's law demands (it would happen if the "
      "field were decreasing). There is no torque about a diameter in a uniform field when the moment is along B. The "
      "net force is zero, but the inward forces on the different parts still tend to change the shape.",
  ncert=EMC + "Lenz's law and conservation of energy", seconds=70)
