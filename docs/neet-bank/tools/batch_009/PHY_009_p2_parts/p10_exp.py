

# ================================================================ Experimental Skills (B3 I3 A3)
LAB = "NMC syllabus, Experimental Skills: "

# ---- Basic
rel_d = F(1, 100) / F(2)
assert rel_d * 100 == F(1, 2) and 3 * rel_d * 100 == F(3, 2)
q(EXP, "Vernier calipers and screw gauge", "Basic", "numerical",
  "The diameter of a small steel sphere is measured with a vernier calipers of least count 0.01 cm and found to be "
  "2.00 cm. Taking the uncertainty in the diameter as one least count, the maximum percentage error in the volume of "
  "the sphere calculated from this measurement is:",
  *opt("1.5%", ["0.5%", "1.0%", "0.17%"], "C"),
  "Propagation of relative errors: for V ∝ d³, ΔV/V = 3 Δd/d",
  "The volume of a sphere is πd³/6, so its relative error is three times the relative error in the diameter.",
  ["Δd/d = 0.01/2.00 = 0.5%", "ΔV/V = 3 × 0.5% = 1.5%"],
  why="0.5% is the error in the diameter alone. 1.0% uses the square of d (as for an area). 0.17% divides by 3 "
      "instead of multiplying.",
  ncert=LAB + "use of vernier callipers to measure the diameter of a small spherical body", seconds=35, rc=True)

Rm = F(36)
assert Rm / 2 == 18
q(EXP, "Optics experiments", "Basic", "numerical",
  "In an experiment with a concave mirror, an object needle is moved along the principal axis until its real, "
  "inverted image coincides with it with no parallax between them. The needle is then 36.0 cm from the pole of the "
  "mirror. The focal length of the mirror is:",
  *opt("18.0 cm", ["36.0 cm", "9.0 cm", "72.0 cm"], "D"),
  "A real image coincides with the object only when the object is at the centre of curvature (u = v = R = 2f)",
  "For the reflected rays to return along their own paths and form the image on the object itself, they must strike "
  "the mirror normally, i.e. pass through the centre of curvature. So the needle is at C, 36.0 cm from the pole, and "
  "f = R/2.",
  ["Object and image coincide → needle at C", "R = 36.0 cm → f = R/2 = 18.0 cm"],
  why="36.0 cm is the radius of curvature, not the focal length. 9.0 cm halves R twice. 72.0 cm doubles R.",
  ncert=LAB + "focal length of a concave mirror", seconds=30, rc=True)

q(EXP, "Vernier calipers and screw gauge", "Basic", "assertion_reason",
  ar("The internal diameter of a beaker is measured with the upper pair of jaws of a vernier calipers, not with the "
     "lower (main) jaws.",
     "The upper jaws have their measuring edges on the outside, so they can be placed against the inner walls of the "
     "beaker and opened out until they touch them."),
  AR, ar_key(True, True, True),
  "Use of the vernier calipers: outside jaws, inside jaws and depth rod",
  "The lower jaws grip an object between their inner faces and so measure external dimensions. The small upper jaws "
  "have their measuring faces facing outwards; inserted into the beaker and opened, they press against the inner "
  "wall, giving the internal diameter. (The depth is measured with the thin strip at the end.) R explains A.",
  ["Lower jaws → external diameter", "Upper jaws (outward-facing edges) → internal diameter", "R explains A"],
  why="R gives the very reason the upper jaws are used for an internal measurement.",
  ncert=LAB + "use of vernier callipers to measure the internal diameter and depth of a given beaker", seconds=35)

# ---- Intermediate
l1, l2 = F(17), F(52)
l3 = l2 + (l2 - l1)
assert l3 == 87 and 5 * l1 == 85 and l1 + l2 == 69 and 2 * l2 == 104
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "In a resonance-tube experiment with a tuning fork, the first and second resonances are obtained at air-column "
  "lengths of 17.0 cm and 52.0 cm. If the tube is long enough, the third resonance will be obtained at an air-column "
  "length of:",
  *opt("87.0 cm", ["69.0 cm", "104.0 cm", "85.0 cm"], "B"),
  "Successive resonances of a tube closed at one end are half a wavelength apart; the end correction is the same "
  "for all of them",
  "The resonances occur at l + e = λ/4, 3λ/4, 5λ/4, ..., where e is the end correction. So the difference between "
  "successive resonance lengths is λ/2, which is 52.0 − 17.0 = 35.0 cm, and the third resonance is another 35.0 cm "
  "further on.",
  ["λ/2 = l₂ − l₁ = 35.0 cm", "l₃ = l₂ + λ/2 = 52.0 + 35.0 = 87.0 cm"],
  why="69.0 cm adds l₁ and l₂. 104.0 cm doubles l₂. 85.0 cm takes 5l₁, which assumes no end correction "
      "(l₁ = λ/4 exactly); here 3l₁ = 51 cm ≠ 52 cm shows that there is an end correction.",
  ncert=LAB + "speed of sound in air at room temperature using a resonance tube", seconds=60, rc=True)

A0, A1_ = F(8), F(4)
remaining = (A1_ / A0) ** 2
assert remaining == F(1, 4) and (1 - remaining) * 100 == 75
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "In an experiment on the dissipation of energy of a simple pendulum, the amplitude of the oscillations falls from "
  "8.0 cm to 4.0 cm in a certain time. The percentage of the initial energy of oscillation that has been dissipated "
  "in this time is:",
  *opt("75%", ["50%", "25%", "94%"], "D"),
  "Energy of a pendulum oscillating with small amplitude A is proportional to A²",
  "Halving the amplitude reduces the energy to (1/2)² = 1/4 of its initial value. The rest has been dissipated "
  "(mainly by air resistance and friction at the support).",
  ["E ∝ A²", "E_final/E_initial = (4/8)² = 1/4", "Energy dissipated = 1 − 1/4 = 75%"],
  why="50% takes the energy as proportional to the amplitude. 25% is the fraction of energy remaining, not the "
      "fraction dissipated. 94% uses A⁴.",
  ncert=LAB + "dissipation of energy of a simple pendulum by plotting a graph between square of amplitude and time",
  seconds=40, rc=True)

q(EXP, "Mechanics experiments", "Intermediate", "statement_pair",
  sp("In finding the mass of an object with a metre scale and a knife edge, the weight of the metre scale acts at its "
     "centre of gravity.",
     "If the scale is balanced on the knife edge at a point other than its centre of gravity, the moment of the "
     "scale's own weight about the knife edge must be included in the balance condition."),
  SP, sp_key(True, True),
  "Principle of moments; centre of gravity",
  "The whole weight of a uniform scale can be taken to act at its centre of gravity (its midpoint). When the knife "
  "edge is at the centre of gravity, this weight has no moment and drops out of the balance condition; when the "
  "knife edge is elsewhere, the weight has a moment about it, which must be included. Both statements are true.",
  ["I: weight acts at the centre of gravity → true",
   "II: knife edge away from the CG → weight has a moment → true"],
  why="Both statements are correct; neither is a trap.",
  ncert=LAB + "mass of a given object using a metre scale by the principle of moments", seconds=40)

# ---- Advanced
i_m, A_p = 50, 60
dm = 2 * i_m - A_p
n_p = 0.766 / math.sin(rad(A_p / 2))
assert dm == 40
close(n_p, 1.532)
close(0.766 / math.sin(rad(40)), 1.19, 1e-2)
q(EXP, "Optics experiments", "Advanced", "numerical",
  "In the experiment to draw the i–δ curve for a triangular glass prism of refracting angle 60°, the lowest point of "
  "the curve (minimum deviation) occurs at an angle of incidence of 50°. Taking sin 50° = 0.766, the angle of minimum "
  "deviation and the refractive index of the glass are, respectively:",
  *opt("40° and about 1.53", ["50° and about 1.53", "40° and about 1.19", "20° and about 1.53"], "B"),
  "At minimum deviation i = e and r₁ = r₂ = A/2, so δ_m = 2i − A and n = sin i / sin(A/2)",
  "At the minimum of the i–δ curve the ray passes symmetrically through the prism. Then i + e = A + δ with e = i "
  "gives δ_m, and Snell's law at the first face with r = A/2 gives n.",
  ["δ_m = 2i − A = 100° − 60° = 40°", "r = A/2 = 30°", "n = sin 50°/sin 30° = 0.766/0.5 ≈ 1.53"],
  why="'50°' takes the angle of incidence itself as the deviation. 'About 1.19' divides sin i by sin δ_m instead of "
      "sin(A/2). '20°' subtracts A/2 from i instead of using δ_m = 2i − A.",
  ncert=LAB + "plot a graph of angle of deviation versus angle of incidence for a triangular prism", seconds=90,
  rc=True)

q(EXP, "Thermal and fluid experiments", "Advanced", "match_list",
  ml("Match each laboratory determination in List-I with the relation used to calculate the result (List-II). "
     "(r = radius, ρ and σ = densities of ball and liquid, v = terminal velocity, h = capillary rise, M = load, "
     "L = length of wire, l = extension, f = frequency, l₁ and l₂ = first two resonance lengths.)",
     ["Coefficient of viscosity from the terminal velocity of a steel ball",
      "Surface tension from capillary rise (angle of contact zero)",
      "Young's modulus with Searle's apparatus",
      "Speed of sound with a resonance tube"],
     ["v = 2f(l₂ − l₁)", "T = rhρg/2", "Y = MgL/(πr²l)", "η = 2r²(ρ − σ)g/(9v)"]),
  *mlo("A-IV, B-II, C-III, D-I", ["A-II, B-IV, C-III, D-I", "A-IV, B-III, C-II, D-I", "A-IV, B-II, C-I, D-III"], "C"),
  "Working formulae of standard laboratory experiments",
  "At terminal velocity the viscous force 6πηrv balances the weight minus the upthrust, (4/3)πr³(ρ − σ)g, giving "
  "η = 2r²(ρ − σ)g/(9v). For capillary rise with zero contact angle, 2πrT = πr²hρg, so T = rhρg/2. Young's modulus "
  "is stress/strain = (Mg/πr²)/(l/L). Successive resonances are λ/2 apart, so v = fλ = 2f(l₂ − l₁).",
  ["A → IV", "B → II", "C → III", "D → I"],
  why="The other codes exchange the viscosity and surface-tension relations or the Young's modulus and speed-of-sound "
      "relations; each formula follows from a different balance of forces or wave condition.",
  ncert=LAB + "viscosity by terminal velocity; surface tension by capillary rise; Young's modulus; resonance tube",
  seconds=70)

truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(EXP, "Electrical experiments", "Advanced", "multi_statement",
  ms("In the experiment to find the resistance of a given wire using Ohm's law, a graph of the potential difference "
     "V across the wire (y-axis) is plotted against the current I through it (x-axis). Which of the following "
     "statements are correct?",
     ["For the wire at a constant temperature, the graph is a straight line through the origin.",
      "The slope of the graph gives the resistance of the wire.",
      "A rheostat in the circuit is used to change the current in steps.",
      "The current should be kept small and passed only while readings are taken, so that the wire does not heat up.",
      "If a wire of the same material and thickness but twice the length is used, the slope of the graph is "
      "halved."]),
  *mso(truth, "abcd", ["abce", "abd", "bcde"], "D"),
  "Ohm's law, V = IR; R = ρL/A",
  "At constant temperature V ∝ I, so the V–I graph is a straight line through the origin (a) whose slope V/I is R "
  "(b). The rheostat varies the current (c). Heating raises the resistance and spoils the straight line, so the "
  "current is kept small and switched off between readings (d). Doubling the length doubles R = ρL/A, so the slope "
  "doubles, not halves (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: R ∝ L → slope doubles"],
  why="Options with (e) invert the dependence of resistance on length; the options leaving out (c) or (a) miss "
      "correct statements about the set-up.",
  ncert=LAB + "resistivity of the material of a given wire using Ohm's law (graph of potential difference versus "
              "current)", seconds=70)
