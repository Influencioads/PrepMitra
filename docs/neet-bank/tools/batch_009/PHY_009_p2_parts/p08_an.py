

# ================================================================ Atoms and Nuclei (B4 I5 A4)
ATC = NC + "'Atoms', "
NUC = NC + "'Nuclei', "

# ---- Basic
avg = F(2, 10) * F(1001, 100) + F(8, 10) * F(1101, 100)
assert avg == F(1081, 100) and (F(1001, 100) + F(1101, 100)) / 2 == F(1051, 100)
assert F(8, 10) * F(1001, 100) + F(2, 10) * F(1101, 100) == F(1021, 100)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "Naturally occurring boron consists of two isotopes: ¹⁰B (atomic mass 10.01 u), making up 20% of the atoms, and "
  "¹¹B (atomic mass 11.01 u), making up 80%. The average atomic mass of natural boron is:",
  *opt("10.81 u", ["10.51 u", "10.21 u", "21.02 u"], "C"),
  "Atomic mass of an element = abundance-weighted average of the masses of its isotopes",
  "The average mass is found by weighting each isotope's mass by the fraction of atoms that are of that isotope.",
  ["Average = 0.20 × 10.01 + 0.80 × 11.01", "= 2.002 + 8.808 = 10.81 u"],
  why="10.51 u is the simple average, ignoring the abundances. 10.21 u swaps the two abundances. 21.02 u adds the "
      "two masses.",
  ncert=NUC + "atomic masses and composition of nucleus", seconds=35, rc=True)

q(AN, "Rutherford scattering", "Basic", "assertion_reason",
  ar("In the alpha-particle scattering experiment, the electrons of the gold atoms have practically no effect on the "
     "paths of the alpha particles.",
     "The mass of an electron is very small compared with that of an alpha particle, so an alpha particle hardly "
     "changes its direction when it collides with an electron."),
  AR, ar_key(True, True, True),
  "Interpretation of the alpha-particle scattering experiment",
  "An alpha particle is several thousand times heavier than an electron. In a collision with such a light particle "
  "it is deflected very little, just as a heavy ball is hardly deflected by striking a much lighter one. The large "
  "deflections must therefore be due to the heavy, positively charged nucleus. R is the reason for A.",
  ["A: true", "R: true", "Light electrons cannot appreciably deflect a heavy alpha particle → R explains A"],
  why="R directly explains A; it is not an unrelated property of electrons.",
  ncert=ATC + "alpha-particle scattering and Rutherford's nuclear model of atom", seconds=35)

q(AN, "Rutherford scattering", "Basic", "statement_pair",
  sp("In the Geiger–Marsden experiment, only about 0.14% of the incident alpha particles were scattered by more "
     "than 1°, and about 1 in 8000 was deflected by more than 90°.",
     "In Thomson's model of the atom, the positive charge is spread uniformly through the volume of the atom and the "
     "electrons are embedded in it, like seeds in a watermelon."),
  SP, sp_key(True, True),
  "Early models of the atom and the results of the scattering experiment",
  "Both statements are as given in NCERT. The tiny fraction scattered through large angles could not be explained "
  "by Thomson's model, in which the positive charge is spread out, and led Rutherford to propose a small, massive "
  "nucleus.",
  ["I: NCERT's figures for the scattering → true", "II: Thomson's (plum pudding) model → true"],
  why="Both statements are correct descriptions; neither is altered.",
  ncert=ATC + "introduction; alpha-particle scattering", seconds=35)

assert F(1, 2) == F(1) / 2
q(AN, "Rutherford scattering", "Basic", "direct",
  "An alpha particle is projected head-on towards a fixed heavy nucleus and comes momentarily to rest at a distance "
  "d from it. If the kinetic energy of the alpha particle is doubled, the distance of closest approach becomes:",
  *opt("d/2", ["2d", "d/√2", "d/4"], "D"),
  "Distance of closest approach: K = (1/4πε₀)(2e)(Ze)/d",
  "At the distance of closest approach the whole initial kinetic energy has become electrostatic potential energy, "
  "which varies as 1/d. So d is inversely proportional to the kinetic energy.",
  ["K = k(2e)(Ze)/d → d ∝ 1/K", "K → 2K gives d → d/2"],
  why="2d has the dependence inverted. d/√2 would follow if d varied as 1/√K. d/4 would follow if d varied as 1/K².",
  ncert=ATC + "alpha-particle trajectory; distance of closest approach", seconds=30, rc=True)

# ---- Intermediate
Ryd = 13.6 / 1240 * 1e9
close(Ryd, 1.097e7, 1e-3)
close(1240 / 13.6 * 1e-9, 9.12e-8, 1e-3)
close(13.6 / 1240 / 4 * 1e9, 2.74e6, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model the energy levels of the hydrogen atom are E_n = −13.6/n² eV, and the wavelengths emitted obey "
  "1/λ = R(1/n_f² − 1/n_i²). Taking hc = 1240 eV nm, the value of the Rydberg constant R obtained from these is "
  "about:",
  *opt("1.1 × 10⁷ m⁻¹", ["9.1 × 10⁻⁸ m⁻¹", "1.1 × 10⁻² m⁻¹", "2.7 × 10⁶ m⁻¹"], "B"),
  "Bohr's frequency condition hc/λ = E_i − E_f = 13.6 eV (1/n_f² − 1/n_i²)",
  "Comparing hc/λ = 13.6 eV (1/n_f² − 1/n_i²) with 1/λ = R(1/n_f² − 1/n_i²) gives R = 13.6 eV/hc.",
  ["R = 13.6 eV / (1240 eV nm) = 0.01097 nm⁻¹", "1 nm⁻¹ = 10⁹ m⁻¹ → R ≈ 1.1 × 10⁷ m⁻¹"],
  why="9.1 × 10⁻⁸ m⁻¹ is the number 91.2 nm (hc/13.6 eV, the Lyman series limit) written with the wrong unit. "
      "1.1 × 10⁻² m⁻¹ leaves the answer in nm⁻¹ but labels it m⁻¹. 2.7 × 10⁶ m⁻¹ divides by an extra factor of 4.",
  ncert=ATC + "Bohr model; the line spectra of the hydrogen atom", seconds=60, rc=True)

E_e = 9.1e-31 * (3e8) ** 2 / 1.6e-13
close(E_e, 0.512, 1e-2)
q(AN, "Binding energy", "Intermediate", "numerical",
  "Taking the mass of the electron as 9.1 × 10⁻³¹ kg, c = 3 × 10⁸ m/s and 1 MeV = 1.6 × 10⁻¹³ J, the energy "
  "equivalent of the rest mass of an electron is about:",
  *opt("0.51 MeV", ["0.26 MeV", "931 MeV", "5.1 × 10⁵ MeV"], "D"),
  "Einstein's mass–energy relation E = mc²",
  "A mass m is equivalent to an energy mc². Convert joules to MeV at the end.",
  ["E = 9.1 × 10⁻³¹ × (3 × 10⁸)² = 8.19 × 10⁻¹⁴ J", "E = 8.19 × 10⁻¹⁴/1.6 × 10⁻¹³ ≈ 0.51 MeV"],
  why="0.26 MeV uses ½mc², a kinetic-energy expression. 931 MeV is the energy equivalent of 1 u, not of an electron. "
      "5.1 × 10⁵ MeV is the value in eV mislabelled as MeV.",
  ncert=NUC + "mass-energy and nuclear binding energy", seconds=45, rc=True)

a_c = (2.2e6) ** 2 / 0.53e-10
close(a_c, 9.13e22, 1e-2)
close(2.2e6 / 0.53e-10, 4.15e16, 1e-2)
close((2.2e6) ** 2 / 0.53, 9.13e12, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the ground state of the hydrogen atom in the Bohr model, the electron moves in a circle of radius "
  "0.53 × 10⁻¹⁰ m with a speed of 2.2 × 10⁶ m/s. The magnitude of its acceleration is about:",
  *opt("9.1 × 10²² m/s²", ["4.2 × 10¹⁶ m/s²", "1.8 × 10²³ m/s²", "9.1 × 10¹² m/s²"], "C"),
  "Uniform circular motion: centripetal acceleration a = v²/r",
  "The electron moves with constant speed in its orbit, so its acceleration is purely centripetal, directed towards "
  "the nucleus; it is provided by the Coulomb attraction.",
  ["a = v²/r = (2.2 × 10⁶)²/(0.53 × 10⁻¹⁰)", "a = 4.84 × 10¹²/0.53 × 10⁻¹⁰ ≈ 9.1 × 10²² m/s²"],
  why="4.2 × 10¹⁶ is v/r, which is the angular speed in rad/s, not an acceleration. 1.8 × 10²³ m/s² doubles v²/r. "
      "9.1 × 10¹² m/s² takes the radius in Å instead of metres.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=45, rc=True)

q(AN, "Nuclear size and mass defect", "Intermediate", "match_list",
  ml("Match each scientist (or pair of scientists) in List-I with the contribution described in NCERT (List-II).",
     ["H. Geiger and E. Marsden", "E. Rutherford", "N. Bohr", "J. Chadwick"],
     ["Discovered the neutron (1932)", "Proposed the nuclear model of the atom to explain the scattering results",
      "Carried out the alpha-particle scattering experiment with a thin gold foil",
      "Proposed stationary orbits in which the electron does not radiate"]),
  *mlo("A-III, B-II, C-IV, D-I", ["A-II, B-III, C-IV, D-I", "A-III, B-II, C-I, D-IV", "A-III, B-IV, C-II, D-I"], "B"),
  "History of atomic and nuclear structure",
  "Geiger and Marsden, at Rutherford's suggestion, performed the alpha-particle scattering experiment (1911). "
  "Rutherford explained the results with the nuclear model. Bohr (1913) proposed stationary, non-radiating orbits. "
  "Chadwick discovered the neutron in 1932.",
  ["A → III", "B → II", "C → IV", "D → I"],
  why="The other codes swap the experimenters with the person who interpreted the experiment, or give the neutron "
      "to Bohr.",
  ncert=ATC + "alpha-particle scattering; Bohr model; " + "'Nuclei', discovery of neutron", seconds=45)

lines = [(i, f) for i in range(2, 5) for f in range(1, i) if i <= 4]
E = lambda n: -F(136, 10) / n ** 2
dE = {(i, f): E(i) - E(f) for i, f in lines}
assert len(lines) == 6 and min(dE, key=dE.get) == (4, 3) and max(dE, key=dE.get) == (4, 1)
assert sum(1 for i, f in lines if f == 2) == 2 and dE[(4, 1)] == F(1275, 100)
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "multi_statement",
  ms("A sample of hydrogen atoms is excited to the n = 4 level (E_n = −13.6/n² eV). As the atoms return to the ground "
     "state by all possible downward transitions, which of the following statements about the emitted radiation are "
     "correct?",
     ["Six different spectral lines can appear.",
      "The line of longest wavelength comes from the transition n = 4 → n = 3 and lies in the infrared.",
      "The line of shortest wavelength comes from the transition n = 4 → n = 1.",
      "Exactly two of the lines belong to the Balmer series.",
      "The most energetic photon emitted has an energy of 13.6 eV."]),
  *mso(truth, "abcd", ["abce", "bcd", "acde"], "D"),
  "Bohr's frequency condition; spectral series of hydrogen",
  "From n = 4 the possible transitions are 4→3, 4→2, 4→1, 3→2, 3→1 and 2→1: six lines. The smallest energy gap, "
  "4→3 (0.66 eV), gives the longest wavelength, a Paschen line in the infrared; the largest, 4→1 (12.75 eV), the "
  "shortest. Transitions ending on n = 2 (4→2 and 3→2) form Balmer lines: two of them. The largest photon energy is "
  "12.75 eV, not 13.6 eV, which would need an electron from n = ∞.",
  ["(a) 4 × 3/2 = 6 → true", "(b) 4→3: 0.66 eV, Paschen (IR) → true", "(c) 4→1: 12.75 eV → true",
   "(d) 4→2 and 3→2 → true", "(e) maximum 12.75 eV → false"],
  why="Options with (e) take the ionisation energy as the largest photon energy; the options leaving out (a) or (b) "
      "miss correct statements.",
  ncert=ATC + "the line spectra of the hydrogen atom", seconds=80, rc=True)

# ---- Advanced
r_ratio = F(1, 2)
m_ratio = r_ratio ** 3
v_ratio = 1 / m_ratio
assert m_ratio == F(1, 8) and v_ratio == 8
q(AN, "Fission and fusion", "Advanced", "numerical",
  "A nucleus at rest splits into two fragments whose radii are in the ratio 1 : 2 (take R = R₀A^(1/3) for each "
  "fragment and the mass of each fragment as proportional to its mass number). The ratio of the speed of the "
  "smaller fragment to that of the larger fragment is:",
  *opt("8 : 1", ["2 : 1", "4 : 1", "1 : 8"], "C"),
  "Nuclear radius R ∝ A^(1/3); conservation of momentum",
  "Since R ∝ A^(1/3), the mass numbers (and masses) are in the ratio of the cubes of the radii, 1 : 8. The parent "
  "was at rest, so the fragments move off with equal and opposite momenta, and their speeds are in the inverse ratio "
  "of their masses.",
  ["A₁ : A₂ = 1³ : 2³ = 1 : 8", "m₁v₁ = m₂v₂ → v₁ : v₂ = m₂ : m₁ = 8 : 1"],
  why="2 : 1 takes the masses in the ratio of the radii. 4 : 1 squares the radius ratio (as for surface areas). "
      "1 : 8 inverts the speed ratio: the lighter fragment moves faster.",
  ncert=NUC + "size of the nucleus", seconds=80, rc=True)

T1 = 1.5e-16
N_rev = 1.0e-8 / (8 * T1)
close(N_rev, 8.33e6, 1e-2)
close(1.0e-8 / T1, 6.67e7, 1e-2)
close(1.0e-8 / (4 * T1), 1.67e7, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the Bohr model of the hydrogen atom, the electron takes 1.5 × 10⁻¹⁶ s to complete one revolution in the ground "
  "state, and the orbit radius and the electron's speed vary as n² and 1/n respectively. An electron remains in the "
  "n = 2 state for 1.0 × 10⁻⁸ s before returning to the ground state. The number of revolutions it makes in the "
  "n = 2 orbit in this time is about:",
  *opt("8.3 × 10⁶", ["6.7 × 10⁷", "1.7 × 10⁷", "4.2 × 10⁶"], "B"),
  "Time period of revolution T = 2πr/v ∝ n²/(1/n) = n³",
  "The period grows as n³, so in the n = 2 orbit it is 8 times the ground-state period. The number of revolutions "
  "is the time spent divided by this period.",
  ["T ∝ n³ → T₂ = 8 × 1.5 × 10⁻¹⁶ = 1.2 × 10⁻¹⁵ s", "N = 1.0 × 10⁻⁸/1.2 × 10⁻¹⁵ ≈ 8.3 × 10⁶"],
  why="6.7 × 10⁷ uses the ground-state period. 1.7 × 10⁷ takes T ∝ n² (only the larger radius). 4.2 × 10⁶ takes "
      "T ∝ n⁴.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=100, rc=True)

R_cu = 1.2 * 64 ** (1 / 3)
K_alpha = 2 * 29 * 1.44 / R_cu
close(R_cu, 4.8)
close(K_alpha, 17.4, 1e-2)
close(29 * 1.44 / R_cu, 8.7, 1e-2)
close(2 * 29 * 1.44 / (1.2 * 64), 1.09, 1e-2)
close(2 * 64 * 1.44 / R_cu, 38.4, 1e-2)
q(AN, "Rutherford scattering", "Advanced", "numerical",
  "An alpha particle is projected head-on towards a copper nucleus (Z = 29, A = 64), which may be taken as fixed. "
  "Taking the nuclear radius R = R₀A^(1/3) with R₀ = 1.2 fm and e²/(4πε₀) = 1.44 MeV fm, and treating the nucleus "
  "and the alpha particle as point charges, the least kinetic energy the alpha particle must have for its distance "
  "of closest approach to equal the radius of the copper nucleus is about:",
  *opt("17 MeV", ["8.7 MeV", "1.1 MeV", "38 MeV"], "D"),
  "Nuclear radius R = R₀A^(1/3); distance of closest approach K = k(2e)(Ze)/d",
  "At closest approach the kinetic energy has all become electrostatic potential energy. Setting the distance equal "
  "to the nuclear radius gives the required energy.",
  ["R = 1.2 × 64^(1/3) = 1.2 × 4 = 4.8 fm", "K = (2 × 29 × 1.44 MeV fm)/4.8 fm", "K = 83.5/4.8 ≈ 17.4 MeV"],
  why="8.7 MeV gives the alpha particle a charge of e instead of 2e. 1.1 MeV uses R = R₀A instead of R₀A^(1/3). "
      "38 MeV uses the mass number 64 in place of the atomic number 29.",
  ncert=ATC + "alpha-particle trajectory; " + "'Nuclei', size of the nucleus", seconds=110, rc=True)

q(AN, "Binding energy", "Advanced", "statement_pair",
  sp("The binding energy of a nucleus is the energy needed to separate it completely into its constituent protons "
     "and neutrons.",
     "Of two nuclei, the one with the larger total binding energy is always the more stable."),
  SP, sp_key(True, False),
  "Binding energy and binding energy per nucleon",
  "Statement I is the definition of binding energy (it equals the mass defect times c²). Statement II is false: the "
  "stability of a nucleus is judged by its binding energy per nucleon. A heavy nucleus such as ²³⁸U has a much larger "
  "total binding energy than ⁵⁶Fe but a smaller binding energy per nucleon, and it releases energy when it splits.",
  ["I: definition → true", "II: stability depends on BE per nucleon, not total BE → false"],
  why="Statement II ignores that the total binding energy grows with the number of nucleons; it is the value per "
      "nucleon that measures how tightly each nucleon is bound.",
  ncert=NUC + "mass-energy and nuclear binding energy", seconds=50)
