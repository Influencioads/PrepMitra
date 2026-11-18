

# ================================================================ Electromagnetic Waves (B1 I1 A1)
EWC = NC + "'Electromagnetic Waves', "

c_ = 1 / math.sqrt(4 * math.pi * 1e-7 * 8.85e-12)
close(c_, 3.0e8, 2e-3)
close(1 / (4 * math.pi * 1e-7 * 8.85e-12), 9.0e16, 2e-3)
close(math.sqrt(4 * math.pi * 1e-7 * 8.85e-12), 3.3e-9, 2e-2)
q(EMW, "EM wave properties", "Basic", "numerical",
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹ and ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the speed of electromagnetic waves in vacuum "
  "predicted by Maxwell's equations is about:",
  *opt("3.0 × 10⁸ m/s", ["9.0 × 10¹⁶ m/s", "3.3 × 10⁻⁹ m/s", "1.1 × 10⁻¹⁷ m/s"], "B"),
  "Speed of electromagnetic waves in vacuum c = 1/√(µ₀ε₀)",
  "Maxwell found that his equations give waves travelling with speed 1/√(µ₀ε₀), which agrees with the measured "
  "speed of light.",
  ["µ₀ε₀ = 4π × 10⁻⁷ × 8.85 × 10⁻¹² ≈ 1.11 × 10⁻¹⁷ s² m⁻²", "c = 1/√(1.11 × 10⁻¹⁷) ≈ 3.0 × 10⁸ m/s"],
  why="9.0 × 10¹⁶ m/s forgets the square root (it is c², in m² s⁻²). 3.3 × 10⁻⁹ m/s is √(µ₀ε₀), the reciprocal of c. "
      "1.1 × 10⁻¹⁷ is µ₀ε₀ itself.",
  ncert=EWC + "electromagnetic waves: sources and nature", seconds=35, rc=True)

q(EMW, "EM wave properties", "Intermediate", "match_list",
  ml("Match each scientist in List-I with the contribution to the study of electromagnetic waves (List-II) that NCERT "
     "describes.",
     ["J. C. Maxwell", "H. Hertz", "J. C. Bose", "G. Marconi"],
     ["Transmitted electromagnetic waves over distances of many kilometres",
      "Produced and observed electromagnetic waves of much shorter wavelength, 25 mm to 5 mm",
      "Introduced the displacement current and predicted the existence of electromagnetic waves",
      "First demonstrated electromagnetic waves experimentally, in 1887"]),
  *mlo("A-III, B-IV, C-II, D-I", ["A-IV, B-III, C-II, D-I", "A-III, B-IV, C-I, D-II", "A-III, B-II, C-IV, D-I"], "C"),
  "History of electromagnetic waves (NCERT introduction to the chapter)",
  "Maxwell added the displacement current to Ampere's law and showed that the equations predict electromagnetic "
  "waves. Hertz demonstrated such waves experimentally in 1887. J. C. Bose, working in Calcutta, produced and "
  "observed waves of much shorter wavelength (25 mm to 5 mm). Marconi transmitted electromagnetic waves over "
  "distances of many kilometres.",
  ["Maxwell → III", "Hertz → IV", "Bose → II", "Marconi → I"],
  why="The other codes swap the theoretical prediction (Maxwell) with the first experiment (Hertz), or swap the "
      "short-wavelength work of Bose with Marconi's long-distance transmission.",
  ncert=EWC + "introduction", seconds=45)

r_in, r_out = F(1, 2), F(3)          # in units of the plate radius R
B_in = r_in                           # µ₀ i r/(2πR²), in units of µ₀i/(2πR)
B_out = 1 / r_out                     # µ₀ i/(2πr), same units
assert B_in / B_out == F(3, 2) and r_in / r_out == F(1, 6) and (1 / r_in) / (1 / r_out) == 6
q(EMW, "Displacement current", "Advanced", "numerical",
  "A parallel-plate capacitor with circular plates of radius R is being charged by a steady current. Neglect edge "
  "effects, so that the uniform, changing electric field exists only in the cylindrical region between the plates. "
  "In the plane midway between the plates, the ratio of the magnitude of the magnetic field at a distance R/2 from "
  "the axis to that at a distance 3R from the axis is:",
  *opt("3 : 2", ["1 : 6", "6 : 1", "2 : 3"], "D"),
  "Ampere–Maxwell law: ∮B·dl = µ₀ i_d, where i_d = ε₀ dΦ_E/dt is the displacement current enclosed by the loop",
  "Take circular loops coaxial with the plates. The displacement current, equal to the charging current i, is spread "
  "uniformly over the plate area. A loop of radius r < R encloses the fraction r²/R² of it; a loop of radius r > R "
  "encloses all of it.",
  ["r = R/2: B × 2π(R/2) = µ₀ i (1/4) → B = µ₀i/(4πR)", "r = 3R: B × 2π(3R) = µ₀ i → B = µ₀i/(6πR)",
   "Ratio = (1/4)/(1/6) = 3 : 2"],
  why="1 : 6 assumes B ∝ r at both points, as if the changing field filled the whole plane. 6 : 1 assumes B ∝ 1/r "
      "at both points, as if all of the displacement current were enclosed even at R/2. 2 : 3 inverts the answer.",
  ncert=EWC + "displacement current", seconds=100, rc=True)
