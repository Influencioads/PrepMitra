

# ================================================================ Dual Nature of Matter and Radiation (B3 I4 A3)
DNC = NC + "'Dual Nature of Radiation and Matter', "

# ---- Basic
h_ = 6.6e-34
lam_ball = h_ / (0.05 * 30)
close(lam_ball, 4.4e-34)
close(h_ / (50 * 30), 4.4e-37)
close(h_ / 0.05, 1.32e-32)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "A ball of mass 50 g is thrown with a speed of 30 m/s. Taking h = 6.6 × 10⁻³⁴ J s, its de Broglie wavelength is:",
  *opt("4.4 × 10⁻³⁴ m", ["4.4 × 10⁻³⁷ m", "1.3 × 10⁻³² m", "2.3 × 10³³ m"], "B"),
  "de Broglie relation λ = h/p = h/(mv)",
  "The momentum of the ball is p = mv = 0.050 kg × 30 m/s = 1.5 kg m/s. Its de Broglie wavelength is far too small "
  "to be detected, which is why a ball shows no wave behaviour.",
  ["p = 0.050 × 30 = 1.5 kg m s⁻¹", "λ = 6.6 × 10⁻³⁴/1.5 = 4.4 × 10⁻³⁴ m"],
  why="4.4 × 10⁻³⁷ m keeps the mass in grams. 1.3 × 10⁻³² m divides h by the mass only, leaving out the speed. "
      "2.3 × 10³³ m is p/h, the inverse of the correct ratio.",
  ncert=DNC + "wave nature of matter", seconds=30, rc=True)

q(DUAL, "Photoelectric effect", "Basic", "assertion_reason",
  ar("A photon of violet light carries more momentum than a photon of red light.",
     "The momentum of a photon is p = hν/c = h/λ, and violet light has a higher frequency (shorter wavelength) than "
     "red light."),
  AR, ar_key(True, True, True),
  "Photon picture of light: energy hν and momentum hν/c",
  "Each photon of frequency ν carries momentum hν/c. Violet light has a higher frequency than red light, so each "
  "violet photon carries more momentum. R is the reason for A.",
  ["p = hν/c", "ν_violet > ν_red → p_violet > p_red", "R explains A"],
  why="R is the direct reason; it is not an unrelated statement about photons.",
  ncert=DNC + "Einstein's photoelectric equation: energy quantum of radiation; particle nature of light: the photon",
  seconds=30)

q(DUAL, "Einstein's equation", "Basic", "statement_pair",
  sp("Millikan's careful experiments on the photoelectric effect verified Einstein's photoelectric equation and gave "
     "an accurate value of Planck's constant.",
     "Einstein's photoelectric equation predicts that the maximum kinetic energy of the photoelectrons increases "
     "linearly with the intensity of the incident light."),
  SP, sp_key(True, False),
  "Einstein's photoelectric equation K_max = hν − φ₀ and its experimental verification",
  "NCERT records that Millikan's photoelectric experiments (1906–1916) verified Einstein's equation and gave an "
  "accurate value of h, so Statement I is true. The equation K_max = hν − φ₀ contains no intensity at all: K_max "
  "depends linearly on the frequency, not on the intensity. Statement II is false.",
  ["I: true", "II: K_max = hν − φ₀ depends on ν, not on intensity → false"],
  why="Statement II replaces frequency by intensity, which is the prediction of the wave picture that the photoelectric "
      "effect contradicts.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=35)

# ---- Intermediate
hc_l, phi_ = F(10), F(2)          # hc/λ = 10 units, φ = 2 units (any example)
V1 = hc_l - phi_
V2 = 2 * hc_l - phi_
assert V2 == 2 * V1 + phi_ and V2 > 2 * V1
q(DUAL, "Einstein's equation", "Intermediate", "direct",
  "Monochromatic light of wavelength λ falls on a metal surface and the stopping potential is V₀. If light of "
  "wavelength λ/2 is used instead, the stopping potential becomes:",
  *opt("more than 2V₀", ["exactly 2V₀", "more than V₀ but less than 2V₀", "V₀/2"], "C"),
  "Einstein's photoelectric equation eV₀ = hc/λ − φ₀",
  "Halving the wavelength doubles the photon energy, but the work function stays the same, so the stopping potential "
  "more than doubles.",
  ["eV₀ = hc/λ − φ₀", "eV₀' = 2hc/λ − φ₀ = 2(hc/λ − φ₀) + φ₀ = 2eV₀ + φ₀", "V₀' = 2V₀ + φ₀/e > 2V₀"],
  why="'Exactly 2V₀' assumes V₀ is proportional to the photon energy, forgetting the work function. 'Less than 2V₀' "
      "subtracts the work function twice. V₀/2 treats V₀ as proportional to λ.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=50, rc=True)

E_ph = F(136, 10) * (1 - F(1, 4))
K_ = E_ph - F(42, 10)
assert E_ph == F(102, 10) and K_ == 6 and E_ph + F(42, 10) == F(144, 10) and F(136, 10) - F(42, 10) == F(94, 10)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "The energy of the electron in the nth orbit of the hydrogen atom is −13.6/n² eV. Photons emitted when hydrogen "
  "atoms make transitions from n = 2 to n = 1 fall on a metal surface of work function 4.2 eV. The stopping potential "
  "for the photoelectrons is:",
  *opt("6.0 V", ["10.2 V", "14.4 V", "9.4 V"], "D"),
  "Photon energy from an atomic transition; Einstein's equation eV₀ = hν − φ₀",
  "The photon carries the energy difference of the two levels. The fastest photoelectron leaves with that energy minus "
  "the work function, and the stopping potential (in volts) equals that kinetic energy in eV.",
  ["hν = E₂ − E₁ = −3.4 − (−13.6) = 10.2 eV", "K_max = 10.2 − 4.2 = 6.0 eV", "V₀ = 6.0 V"],
  why="10.2 V ignores the work function. 14.4 V adds the work function instead of subtracting it. 9.4 V takes the "
      "photon energy as the full ionisation energy 13.6 eV.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=60, rc=True)

q(DUAL, "Einstein's equation", "Intermediate", "match_list",
  ml("Graphs are drawn from photoelectric data for one metal: the stopping potential V₀ against the frequency ν, and "
     "the maximum kinetic energy K_max against ν. Match each feature in List-I with what it gives in List-II.",
     ["Slope of the V₀–ν graph", "Intercept of the V₀–ν line on the ν axis",
      "Intercept of the extended K_max–ν line on the K_max axis", "Slope of the K_max–ν graph"],
     ["h", "h/e", "the threshold frequency ν₀", "−φ₀ (minus the work function)"]),
  *mlo("A-II, B-III, C-IV, D-I", ["A-I, B-III, C-IV, D-II", "A-II, B-IV, C-III, D-I", "A-II, B-III, C-I, D-IV"], "B"),
  "Einstein's equation as a straight line: K_max = hν − φ₀ and V₀ = (h/e)ν − φ₀/e",
  "K_max = hν − φ₀ is a straight line of slope h that cuts the K_max axis at −φ₀. Dividing by e, V₀ = (h/e)ν − φ₀/e has "
  "slope h/e, and V₀ = 0 at ν = φ₀/h = ν₀, the threshold frequency.",
  ["A → h/e (II)", "B → ν₀ (III)", "C → −φ₀ (IV)", "D → h (I)"],
  why="Swapping the two slopes forgets the factor e between the energy (K_max) and the potential (V₀). The other "
      "codes confuse the frequency-axis intercept (ν₀) with the energy-axis intercept (−φ₀).",
  ncert=DNC + "experimental study of photoelectric effect; Einstein's photoelectric equation", seconds=60)

Kmax_e = F(3) - F(2)
assert Kmax_e + F(3, 2) == F(5, 2) and 0 + F(3, 2) == F(3, 2)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Photons of energy 3.0 eV fall on the emitter of a photocell, whose work function is 2.0 eV. The collector is kept "
  "at a potential of +1.5 V with respect to the emitter. The kinetic energies of the photoelectrons arriving at the "
  "collector lie in the range:",
  *opt("1.5 eV to 2.5 eV", ["0 to 1.0 eV", "0 to 2.5 eV", "exactly 2.5 eV for every electron"], "C"),
  "Photoelectrons leave with kinetic energies from 0 to K_max; an accelerating potential adds eV to each",
  "Electrons leave the emitter with kinetic energies from zero up to K_max = 3.0 − 2.0 = 1.0 eV. The collector is "
  "1.5 V higher, so every electron gains 1.5 eV on the way.",
  ["K at emitter: 0 to 1.0 eV", "Gain from accelerating potential: +1.5 eV", "K at collector: 1.5 eV to 2.5 eV"],
  why="'0 to 1.0 eV' ignores the accelerating potential. '0 to 2.5 eV' adds 1.5 eV only to the fastest electrons. "
      "Photoelectrons are not all emitted with K_max, so they do not all arrive with 2.5 eV.",
  ncert=DNC + "experimental study of photoelectric effect: effect of potential on photoelectric current",
  seconds=60, rc=True)

# ---- Advanced
nu0 = F(1)
K = lambda nu: nu - nu0                     # in units of hν₀
assert K(3) == 2 * K(2) and K(4) == 3 * K(2)
truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(DUAL, "Photoelectric effect", "Advanced", "multi_statement",
  ms("Monochromatic light of frequency 2ν₀, where ν₀ is the threshold frequency of a metal, falls on it and gives a "
     "stopping potential V₀ and a saturation current I_s. Each change below is made separately, the other conditions "
     "being kept as they were. Which of the following statements are correct?",
     ["If the frequency is raised to 3ν₀ (the number of photons falling per second unchanged), the stopping potential "
      "becomes 2V₀.",
      "If the number of photons falling per second is doubled (frequency unchanged), the saturation current becomes "
      "2I_s.",
      "If the frequency is raised to 4ν₀, the maximum kinetic energy of the photoelectrons becomes three times its "
      "original value.",
      "If the number of photons falling per second is doubled (frequency unchanged), the stopping potential becomes "
      "2V₀.",
      "If the frequency is lowered to 0.9ν₀, a small photocurrent still flows provided the light is intense "
      "enough."]),
  *mso(truth, "abc", ["abd", "bce", "acd"], "B"),
  "Einstein's equation K_max = h(ν − ν₀); saturation current ∝ number of photons per second",
  "eV₀ = h(ν − ν₀). At 2ν₀: eV₀ = hν₀. At 3ν₀: 2hν₀, i.e. 2V₀ (a). At 4ν₀: 3hν₀, three times (c). Each photon can "
  "free at most one electron, so the number of photoelectrons per second, and hence the saturation current, is "
  "proportional to the number of photons per second (b), while the stopping potential does not depend on it (d "
  "false). Below the threshold frequency no photoelectrons are emitted however intense the light (e false).",
  ["(a) h(3ν₀ − ν₀) = 2hν₀ → 2V₀ → true", "(b) true", "(c) h(4ν₀ − ν₀) = 3hν₀ → true",
   "(d) V₀ independent of photon flux → false", "(e) ν < ν₀ → no emission → false"],
  why="Options with (d) let the photon flux change the stopping potential; options with (e) ignore the threshold "
      "frequency.",
  ncert=DNC + "experimental study of photoelectric effect; Einstein's photoelectric equation", seconds=100,
  rc=True)

E_J = 10.2 * 1.6e-19
v_rec = E_J / (1.67e-27 * 3e8)
close(v_rec, 3.26, 1e-2)
close(2 * v_rec, 6.5, 1e-2)
close(math.sqrt(2 * E_J / 1.67e-27), 4.42e4, 1e-2)
q(DUAL, "Photoelectric effect", "Advanced", "numerical",
  "A hydrogen atom, initially at rest, emits a photon of energy 10.2 eV. Taking the mass of the atom as "
  "1.67 × 10⁻²⁷ kg, 1 eV = 1.6 × 10⁻¹⁹ J and c = 3 × 10⁸ m/s, the speed with which the atom recoils is about:",
  *opt("3.3 m/s", ["6.5 m/s", "4.4 × 10⁴ m/s", "zero, since a photon has no mass and carries no momentum"], "D"),
  "Photon momentum p = E/c = hν/c; conservation of momentum",
  "Before the emission the total momentum is zero. The photon carries away momentum E/c, so the atom recoils with an "
  "equal and opposite momentum: m v = E/c.",
  ["E = 10.2 × 1.6 × 10⁻¹⁹ = 1.63 × 10⁻¹⁸ J", "p = E/c = 5.44 × 10⁻²⁷ kg m s⁻¹",
   "v = p/m = 5.44 × 10⁻²⁷/1.67 × 10⁻²⁷ ≈ 3.3 m/s"],
  why="6.5 m/s uses 2E/c, the momentum change on reflection of a photon, not on emission. 4.4 × 10⁴ m/s gives all "
      "the photon's energy to the atom as kinetic energy. A photon has no rest mass but does carry momentum hν/c.",
  ncert=DNC + "particle nature of light: the photon", seconds=100, rc=True)

phi_m = F(2)
K1, K2 = F(4) - phi_m, F(8) - phi_m
assert K1 == 2 and K2 == 6 and K2 / K1 == 3
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "Photons of energy 4.0 eV, and then photons of energy 8.0 eV, fall on a metal of work function 2.0 eV. The ratio "
  "of the de Broglie wavelength of the fastest photoelectrons in the first case to that in the second case is:",
  *opt("√3 : 1", ["√2 : 1", "3 : 1", "1 : √3"], "A"),
  "Einstein's equation K_max = hν − φ₀; de Broglie wavelength λ = h/√(2mK) ∝ 1/√K",
  "Doubling the photon energy does not double K_max, because the work function is subtracted each time. For "
  "non-relativistic electrons λ ∝ 1/√K.",
  ["K₁ = 4.0 − 2.0 = 2.0 eV", "K₂ = 8.0 − 2.0 = 6.0 eV", "λ₁/λ₂ = √(K₂/K₁) = √3"],
  why="√2 : 1 assumes K_max doubles when the photon energy doubles. 3 : 1 is the ratio of the kinetic energies, not "
      "of the wavelengths. 1 : √3 inverts the ratio; the slower electrons have the longer wavelength.",
  ncert=DNC + "wave nature of matter", seconds=80, rc=True)
