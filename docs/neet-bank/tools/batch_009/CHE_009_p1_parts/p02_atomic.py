

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"
R_H = 1.097e7
M_E = 9.11e-31

nu0 = 3.313e-19 / H_PLANCK
assert close(nu0, 5.0e14)
add("Dual nature and uncertainty", B, "numerical",
    "The work function (minimum energy needed to eject an electron) of a metal is 3.313 × 10⁻¹⁹ J. The threshold "
    "frequency of the metal is (h = 6.626 × 10⁻³⁴ J s):",
    Opts("B", "5.0 × 10¹⁴ Hz", ["5.0 × 10¹³ Hz", "2.0 × 10⁻¹⁵ Hz", "5.0 × 10¹⁵ Hz"]),
    "Threshold frequency in the photoelectric effect: W₀ = hν₀",
    "A photon can just eject an electron when its energy equals the work function, so ν₀ = W₀/h.",
    ["ν₀ = W₀/h = 3.313 × 10⁻¹⁹ / 6.626 × 10⁻³⁴", "ν₀ = 0.5 × 10¹⁵ = 5.0 × 10¹⁴ Hz"],
    why="5.0 × 10¹³ Hz and 5.0 × 10¹⁵ Hz are slips in the power of ten. 2.0 × 10⁻¹⁵ Hz inverts the ratio (h/W₀).",
    ncert=f"{REF2}, photoelectric effect", seconds=30, checked=True)

add("Electronic configuration", B, "direct",
    "The ground-state electronic configuration of gallium (Z = 31) is:",
    Opts("C", "[Ar] 3d¹⁰ 4s² 4p¹", ["[Ar] 4s² 4p¹", "[Ar] 3d⁹ 4s² 4p²", "[Ar] 3d¹⁰ 4s¹ 4p²"]),
    "Aufbau order: 4s, then 3d, then 4p",
    "After argon (18 electrons), 13 electrons remain. Following the Aufbau order they fill 4s (2), then 3d (10), "
    "and the last one enters 4p.",
    ["Z = 31 → 31 − 18 = 13 electrons beyond [Ar]", "4s² (2) + 3d¹⁰ (10) + 4p¹ (1) = 13",
     "[Ar] 3d¹⁰ 4s² 4p¹"],
    why="[Ar] 4s² 4p¹ leaves out the ten 3d electrons (it has only 21 electrons). The other two move electrons "
        "out of filled 3d or 4s orbitals into 4p, which is not the ground state.",
    ncert=f"{REF2}, electronic configuration of atoms", seconds=30)

add("Dual nature and uncertainty", B, "statement_pair",
    sp("A photon of red light has more energy than a photon of violet light.",
       "As the temperature of a black body is raised, the wavelength at which the intensity of the emitted "
       "radiation is maximum shifts to shorter wavelengths."),
    SP_, "Photon energy and black-body radiation",
    "E = hν = hc/λ. Red light has a longer wavelength (lower frequency) than violet light, so a red photon has "
    "LESS energy: Statement I is false. NCERT notes that as the temperature of a black body rises, the maximum of "
    "the intensity–wavelength curve moves to shorter wavelengths (a heated iron rod glows dull red, then orange, "
    "then white): Statement II is true.",
    ["I: λ(red) > λ(violet) → E(red) < E(violet) → false", "II: higher T → peak at shorter λ → true"],
    answer="D",
    why="Statement I reverses the relation between wavelength and photon energy; Statement II is the NCERT "
        "description of black-body radiation.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation: Planck's quantum theory", seconds=35)

add("Quantum numbers and orbitals", B, "match_list",
    lists("Match List-I (quantum number) with List-II (what it describes).",
          ["Principal quantum number, n", "Azimuthal quantum number, l", "Magnetic quantum number, mₗ",
           "Spin quantum number, mₛ"],
          ["Orientation of the orbital in space", "Three-dimensional shape of the orbital (the subshell)",
           "The shell; the size and, largely, the energy of the orbital", "Orientation of the spin of the electron"]),
    match("A", M("III II I IV"), [M("II III I IV"), M("III I II IV"), M("III II IV I")]),
    "Meaning of the four quantum numbers",
    "n identifies the shell and fixes the size and (largely) the energy; l identifies the subshell and the shape; "
    "mₗ gives the orientation of the orbital; mₛ gives the orientation of the electron's spin.",
    ["A → III", "B → II", "C → I", "D → IV"],
    why="The other codes swap shell with shape, shape with orbital orientation, or orbital orientation with spin "
        "orientation.",
    ncert=f"{REF2}, quantum numbers", seconds=30)

lam_53 = 1 / (R_H * (1 / 9 - 1 / 25)) * 1e9
lam_52 = 1 / (R_H * (1 / 4 - 1 / 25)) * 1e9
lam_bad = 1 / (R_H * (1 / 3 - 1 / 5)) * 1e9
assert round(lam_53) == 1282 and round(lam_52) == 434 and round(lam_bad) == 684
add("Bohr model and hydrogen spectrum", I, "numerical",
    "The electron of a hydrogen atom falls from the n = 5 orbit to the n = 3 orbit. The wavelength of the "
    "radiation emitted, and the region of the spectrum in which it lies, are (R_H = 1.097 × 10⁷ m⁻¹; "
    "1/λ = R_H (1/n₁² − 1/n₂²)):",
    Opts("D", "1282 nm, infrared", ["1282 nm, visible", "434 nm, visible", "684 nm, visible"]),
    "Rydberg formula for the hydrogen spectrum; the Paschen series",
    "Put n₁ = 3 and n₂ = 5 in the Rydberg formula. A transition ending at n = 3 belongs to the Paschen series, "
    "whose lines lie in the infrared.",
    ["1/λ = 1.097 × 10⁷ × (1/9 − 1/25) = 1.097 × 10⁷ × 16/225 = 7.80 × 10⁵ m⁻¹",
     "λ = 1.282 × 10⁻⁶ m = 1282 nm", "Ends at n = 3 → Paschen series → infrared (beyond 700 nm)"],
    why="'1282 nm, visible' has the right wavelength but the wrong region (visible light is about 400–750 nm). "
        "434 nm is the 5 → 2 Balmer line. 684 nm uses 1/n instead of 1/n².",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=70, checked=True)

e_bond = 242e3 / NA
lam_cl = H_PLANCK * C_LIGHT / e_bond
assert round(lam_cl * 1e9) == 495 and round(2 * lam_cl * 1e9) == 989 and round(lam_cl / 2 * 1e9) == 247
add("Dual nature and uncertainty", I, "numerical",
    "The energy needed to break the Cl–Cl bond is 242 kJ mol⁻¹. The longest wavelength of light whose photons "
    "can each break one Cl₂ molecule into atoms is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, "
    "Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("A", "495 nm", ["989 nm", "247 nm", "4.95 × 10⁻⁴ m"]),
    "Energy of a photon, E = hc/λ, related to the energy per molecule",
    "One photon breaks one molecule, so the photon energy must be at least the bond energy per molecule. "
    "The longest wavelength corresponds to exactly that energy.",
    ["Energy per molecule = 242 000 / 6.022 × 10²³ = 4.02 × 10⁻¹⁹ J",
     "λ = hc/E = (6.626 × 10⁻³⁴ × 3.0 × 10⁸) / 4.02 × 10⁻¹⁹ = 4.95 × 10⁻⁷ m = 495 nm"],
    why="989 nm uses half the energy (energy per Cl atom). 247 nm uses twice the energy. 4.95 × 10⁻⁴ m leaves "
        "the energy in kJ instead of converting it to J.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation", seconds=70, checked=True)

add("Bohr model and hydrogen spectrum", I, "assertion_reason",
    ar("A hydrogen atom has only one electron, yet the emission spectrum of a sample of atomic hydrogen contains "
       "many lines.",
       "A sample contains a very large number of atoms, and the electrons in different atoms fall between "
       "different pairs of energy levels, each such transition giving a line of its own frequency."),
    AR_, "Origin of the many lines of the hydrogen spectrum",
    "Each line corresponds to one transition between two quantised energy levels, ν = ΔE/h. In a sample of "
    "hydrogen, excited atoms make many different transitions at the same time (for example 3 → 2, 4 → 2, 2 → 1), "
    "so the spectrum shows many lines. R explains A.",
    ["A: many lines observed → true", "R: different atoms, different transitions, each with its own ΔE → true",
     "R is why one-electron atoms give a many-line spectrum → option A"],
    answer="A",
    why="Both are true and R directly accounts for A. A is not false: the many-line spectrum is observed.",
    ncert=f"{REF2}, Bohr's model and the line spectrum of hydrogen", seconds=40)

e_tr = {"4→1": 13.6 * (1 - 1 / 16), "2→1": 13.6 * (1 - 1 / 4), "∞→2": 13.6 / 4, "6→3": 13.6 * (1 / 9 - 1 / 36)}
assert max(e_tr, key=e_tr.get) == "4→1"
add("Bohr model and hydrogen spectrum", I, "direct",
    "In a hydrogen atom, which of the following electron transitions emits the photon of the HIGHEST energy?",
    Opts("B", "n = 4 → n = 1", ["n = 2 → n = 1", "n = ∞ → n = 2", "n = 6 → n = 3"]),
    "Energy of emitted photons in the hydrogen atom, ΔE = 13.6 (1/n₁² − 1/n₂²) eV",
    "The energy levels crowd together at high n, so the largest gaps are those that end in n = 1. Of the two "
    "transitions ending at n = 1, the one starting higher (n = 4) releases more energy.",
    ["4 → 1: 13.6 × 15/16 = 12.75 eV", "2 → 1: 13.6 × 3/4 = 10.2 eV", "∞ → 2: 13.6/4 = 3.4 eV",
     "6 → 3: 13.6 × (1/9 − 1/36) = 1.13 eV"],
    why="Starting at n = ∞ does not make ∞ → 2 the largest; it ends at n = 2, so it releases only 3.4 eV. "
        "2 → 1 and 6 → 3 are smaller gaps than 4 → 1.",
    ncert=f"{REF2}, Bohr's model: energy of the electron and line spectrum", seconds=45)

add("Quantum numbers and orbitals", I, "statement_pair",
    sp("In an isolated atom, the 2pₓ, 2p_y and 2p_z orbitals differ in their orientation in space but have the "
       "same energy.",
       "The 3p orbitals are larger than the 2p orbitals and have a higher energy than them."),
    SP_, "Orientation, size and energy of p orbitals",
    "The three p orbitals of a shell are identical in size, shape and energy and differ only in orientation "
    "(they are degenerate). NCERT also states that p orbitals increase in size and energy with n: 4p > 3p > 2p. "
    "Both statements are true.",
    ["I: three p orbitals → different orientation, same energy → true", "II: size and energy 3p > 2p → true"],
    answer="A",
    why="Neither statement is false: degeneracy is within a subshell, while size and energy rise from one shell "
        "to the next.",
    ncert=f"{REF2}, shapes of atomic orbitals (p orbitals)", seconds=35)

e_ph = H_PLANCK * C_LIGHT / 150e-9
ke = e_ph - 3.61e-19


def lam_db(energy):
    return H_PLANCK / math.sqrt(2 * M_E * energy) * 1e9


assert close(lam_db(ke), 0.500) and close(lam_db(e_ph), 0.426) and close(lam_db(e_ph + 3.61e-19), 0.378) \
    and close(H_PLANCK / math.sqrt(M_E * ke) * 1e9, 0.707)
add("Dual nature and uncertainty", A, "numerical",
    "Light of wavelength 150 nm falls on a metal whose work function is 3.61 × 10⁻¹⁹ J. The de Broglie "
    "wavelength of the fastest photoelectrons emitted is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, mass of "
    "electron = 9.11 × 10⁻³¹ kg; for a particle, momentum p = √(2m × kinetic energy)):",
    Opts("C", "0.500 nm", ["0.426 nm", "0.707 nm", "0.378 nm"]),
    "Photoelectric equation combined with the de Broglie relation",
    "The kinetic energy of the fastest electrons is the photon energy minus the work function. Convert it into "
    "momentum and use λ = h/p.",
    ["E(photon) = hc/λ = 6.626 × 10⁻³⁴ × 3.0 × 10⁸ / 1.50 × 10⁻⁷ = 1.325 × 10⁻¹⁸ J",
     "Kinetic energy = 1.325 × 10⁻¹⁸ − 0.361 × 10⁻¹⁸ = 9.64 × 10⁻¹⁹ J",
     "p = √(2 × 9.11 × 10⁻³¹ × 9.64 × 10⁻¹⁹) = 1.325 × 10⁻²⁴ kg m s⁻¹",
     "λ = h/p = 6.626 × 10⁻³⁴ / 1.325 × 10⁻²⁴ = 5.00 × 10⁻¹⁰ m = 0.500 nm"],
    why="0.426 nm takes the whole photon energy as kinetic energy (forgets the work function). 0.378 nm adds the "
        "work function instead of subtracting it. 0.707 nm leaves out the factor 2 in p = √(2mE).",
    ncert=f"{REF2}, photoelectric effect; dual behaviour of matter", seconds=150, checked=True)

add("Bohr model and hydrogen spectrum", A, "assertion_reason",
    ar("Every line of the Lyman series of hydrogen has a shorter wavelength than every line of the Balmer series.",
       "The smallest energy released in a transition ending at n = 1 is larger than the largest energy released "
       "in a transition ending at n = 2."),
    AR_, "Comparing the Lyman and Balmer series",
    "The least energetic Lyman line (2 → 1) carries 13.6 × 3/4 = 10.2 eV; the most energetic Balmer photon "
    "(∞ → 2) carries only 13.6/4 = 3.4 eV. So every Lyman photon has more energy, and since λ = hc/E, a shorter "
    "wavelength (Lyman lines lie between about 91 and 122 nm; Balmer lines between about 365 and 656 nm). R is "
    "the reason for A.",
    ["Smallest Lyman energy: 10.2 eV; largest Balmer energy: 3.4 eV → R true",
     "Higher energy → shorter wavelength → A true", "R explains A → option A"],
    answer="A",
    why="Both are true and the energy comparison in R, through λ = hc/E, is exactly why A holds.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=60)

cfg = {"Mn_d": 5, "Fe_shell3": 2 + 6 + 6, "Cr_s": 2 + 2 + 2 + 1, "Mn_p": 6 + 6, "Cu_3d4s": (10, 1)}
truth2 = {"a": cfg["Mn_d"] == 5, "b": cfg["Fe_shell3"] == 8, "c": cfg["Cr_s"] == 7, "d": cfg["Mn_p"] == 12,
          "e": cfg["Cu_3d4s"] == (10, 2)}
assert truth2 == {"a": True, "b": False, "c": True, "d": True, "e": False}
add("Electronic configuration", A, "multi_statement",
    ms("Which of the following statements about ground-state atoms are correct? (Z: Cr = 24, Mn = 25, Fe = 26, "
       "Cu = 29)",
       ["A manganese atom has five electrons in d orbitals.",
        "An iron atom has eight electrons in its third shell (n = 3).",
        "A chromium atom has seven electrons in s orbitals.",
        "A manganese atom has twelve electrons in p orbitals.",
        "A copper atom has ten electrons in its 3d orbitals and two in its 4s orbital."]),
    multi("D", truth2, ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a) and (c) only"]),
    "Ground-state configurations, including the exceptions Cr and Cu",
    "Mn: [Ar] 3d⁵ 4s²; Fe: [Ar] 3d⁶ 4s²; Cr: [Ar] 3d⁵ 4s¹; Cu: [Ar] 3d¹⁰ 4s¹.",
    ["(a) Mn 3d⁵ → 5 d electrons ✓", "(b) Fe n = 3: 3s² 3p⁶ 3d⁶ = 14, not 8 ✗",
     "(c) Cr: 1s² 2s² 3s² 4s¹ = 7 s electrons ✓", "(d) Mn: 2p⁶ + 3p⁶ = 12 p electrons ✓",
     "(e) Cu is 3d¹⁰ 4s¹, not 3d¹⁰ 4s² ✗"],
    why="(b) forgets the 3d electrons in the third shell; (e) ignores the extra stability of the filled 3d "
        "subshell in copper. '(a) and (c) only' misses (d).",
    ncert=f"{REF2}, electronic configuration of atoms; stability of half-filled and completely filled orbitals",
    seconds=90, checked=True)

n_he = math.sqrt(423.2 * 2 / 52.9)
assert close(n_he, 4)
e_he = -13.6 * 2 ** 2 / 4 ** 2
assert close(e_he, -3.40) and close(-13.6 / 16, -0.85) and close(-13.6 * 2 / 16, -1.70) \
    and close(-13.6 * 4 / 4, -13.6)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "For a hydrogen-like species, Bohr's model gives the radius of the nth orbit as rₙ = 52.9 (n²/Z) pm and the "
    "energy of the electron in it as Eₙ = −13.6 (Z²/n²) eV. The energy of the electron of a He⁺ ion (Z = 2) "
    "moving in an orbit of radius 423.2 pm is:",
    Opts("B", "−3.40 eV", ["−0.85 eV", "−1.70 eV", "−13.6 eV"]),
    "Bohr model of hydrogen-like species: find n from the radius, then the energy",
    "First find the orbit number from the radius (with Z = 2), then substitute n and Z into the energy "
    "expression.",
    ["n² = r Z / 52.9 = 423.2 × 2 / 52.9 = 16 → n = 4", "E₄ = −13.6 × 2²/4² = −13.6 × 4/16 = −3.40 eV"],
    why="−0.85 eV leaves out Z² in the energy. −1.70 eV uses Z instead of Z². −13.6 eV divides by n instead of n².",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=80, checked=True)
