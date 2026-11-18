

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"
M_E = 9.11e-31

v_db = H_PLANCK / (M_E * 0.727e-9)
assert close(v_db, 1.0e6, 0.002) and close(H_PLANCK / (M_E * 0.727e-6), 1.0e3, 0.002) \
    and close(H_PLANCK / (M_E * 0.727e-12), 1.0e9, 0.002)
add("Dual nature and uncertainty", B, "numerical",
    "The de Broglie wavelength of a moving electron is 0.727 nm. Its speed is "
    "(h = 6.626 × 10⁻³⁴ J s, mass of electron = 9.11 × 10⁻³¹ kg):",
    Opts("A", "1.0 × 10⁶ m s⁻¹", ["1.0 × 10³ m s⁻¹", "5.0 × 10⁵ m s⁻¹", "1.0 × 10⁹ m s⁻¹"]),
    "de Broglie relation λ = h/mv",
    "Rearrange the de Broglie relation to v = h/(mλ) and put the wavelength in metres.",
    ["λ = 0.727 nm = 7.27 × 10⁻¹⁰ m", "v = 6.626 × 10⁻³⁴ / (9.11 × 10⁻³¹ × 7.27 × 10⁻¹⁰)",
     "v = 6.626 × 10⁻³⁴ / 6.62 × 10⁻⁴⁰ ≈ 1.0 × 10⁶ m s⁻¹"],
    why="1.0 × 10³ m s⁻¹ takes 0.727 nm as 7.27 × 10⁻⁷ m (a micrometre slip). 5.0 × 10⁵ m s⁻¹ wrongly puts a "
        "factor 2 in the relation (λ = h/2mv). 1.0 × 10⁹ m s⁻¹ takes the wavelength in picometres.",
    ncert=f"{REF2}, dual behaviour of matter", seconds=45, checked=True)

add("Quantum numbers and orbitals", B, "direct",
    "For the 2s orbital of the hydrogen atom, how does the probability density ψ² vary as the distance r from "
    "the nucleus increases?",
    Opts("B", "It falls to zero at one finite distance (a node) and then rises again before finally dying away",
         ["It is zero at the nucleus and increases steadily with r",
          "It decreases steadily with r and never becomes zero at any finite distance",
          "It becomes zero at two different finite distances from the nucleus"]),
    "Variation of ψ² with r for 1s and 2s orbitals",
    "For a 2s orbital ψ² is largest at the nucleus, decreases to zero at one value of r (the radial node, where "
    "ψ changes sign), rises again to a small maximum and then decreases towards zero at large r. A 2s orbital "
    "has n − l − 1 = 1 radial node.",
    ["2s: n = 2, l = 0 → radial nodes = 2 − 0 − 1 = 1", "ψ² → 0 once, then a second smaller maximum"],
    why="ψ² of an s orbital is not zero at the nucleus. A steady decrease without any node describes a 1s "
        "orbital. Two radial nodes belong to a 3s orbital.",
    ncert=f"{REF2}, quantum mechanical model of atom (plots of ψ and ψ² for 1s and 2s)", seconds=35)

add("Bohr model and hydrogen spectrum", B, "statement_pair",
    sp("Electromagnetic waves, unlike sound waves, do not need a medium and can travel through a vacuum.",
       "In electromagnetic radiation the oscillating electric and magnetic fields are perpendicular to each "
       "other and to the direction in which the wave travels."),
    SP_, "Nature of electromagnetic radiation",
    "NCERT describes electromagnetic radiation as oscillating electric and magnetic fields, perpendicular to "
    "each other and to the direction of propagation, which need no medium and travel through a vacuum at "
    "3.0 × 10⁸ m s⁻¹.",
    ["I: no medium needed, travels in vacuum → true", "II: E ⟂ B ⟂ direction of travel → true"],
    answer="A",
    why="Both are NCERT statements about electromagnetic waves; an option calling either false is wrong.",
    ncert=f"{REF2}, nature of electromagnetic radiation", seconds=30)

dE = 13.6 * 2 ** 2 * (1 - 1 / 2 ** 2)
assert close(dE, 40.8) and close(13.6 * (1 - 1 / 4), 10.2) and close(13.6 * 4, 54.4) and close(13.6 * 2 * 0.75, 20.4)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "In Bohr's model the energy of the electron of a hydrogen-like species is Eₙ = −13.6 (Z²/n²) eV. The energy "
    "needed to excite the electron of a He⁺ ion (Z = 2) from n = 1 to n = 2 is:",
    Opts("C", "40.8 eV", ["10.2 eV", "54.4 eV", "20.4 eV"]),
    "Energy of a transition in a hydrogen-like ion: ΔE = 13.6 Z² (1/n₁² − 1/n₂²) eV",
    "Find the energies of the two levels for Z = 2 and take their difference.",
    ["E₁ = −13.6 × 4/1 = −54.4 eV", "E₂ = −13.6 × 4/4 = −13.6 eV", "ΔE = −13.6 − (−54.4) = 40.8 eV"],
    why="10.2 eV is the value for the hydrogen atom (Z² left out). 54.4 eV is the energy to remove the electron "
        "completely (n = 1 → ∞). 20.4 eV uses Z instead of Z².",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=45, checked=True)

add("Electronic configuration", I, "assertion_reason",
    ar("In the ground state of a helium atom, the two electrons in the 1s orbital have opposite spins.",
       "No two electrons in an atom can have the same set of all four quantum numbers."),
    AR_, "Pauli exclusion principle",
    "Both helium electrons are in the 1s orbital, so they share n = 1, l = 0 and mₗ = 0. Pauli's principle "
    "forbids them from also sharing mₛ, so one has mₛ = +½ and the other −½: their spins must be opposite. R is "
    "the direct reason for A.",
    ["Same orbital → same n, l, mₗ", "Pauli: the fourth quantum number must differ → mₛ = +½ and −½",
     "Hence opposite spins → R explains A"],
    answer="A",
    why="R is not just another true statement: it is the rule that forces the two 1s electrons of helium to "
        "pair with opposite spins.",
    ncert=f"{REF2}, Pauli exclusion principle", seconds=35)

orbitals = {"A": 3 ** 2, "B": 2 * 1 + 1, "C": 1, "D": 2 * 3 + 1}
assert orbitals == {"A": 9, "B": 3, "C": 1, "D": 7}
add("Quantum numbers and orbitals", I, "match_list",
    lists("Match List-I (quantum numbers that are specified) with List-II (number of orbitals described by "
          "them).",
          ["n = 3", "n = 2, l = 1", "n = 4, l = 2, mₗ = 0", "n = 4, l = 3"],
          ["1", "3", "7", "9"]),
    match("D", M("IV II I III"), [M("IV III I II"), M("II IV I III"), M("IV II III I")]),
    "Counting orbitals from quantum numbers",
    "A shell n has n² orbitals; a subshell l has (2l + 1) orbitals; fixing n, l and mₗ picks out exactly one "
    "orbital.",
    ["A: n = 3 → 3² = 9 orbitals → IV", "B: 2p → 2(1) + 1 = 3 → II", "C: n, l and mₗ all fixed → 1 orbital → I",
     "D: 4f → 2(3) + 1 = 7 → III"],
    why="B-III/D-II gives a p subshell seven orbitals. A-II/B-IV confuses the shell with a subshell. "
        "C-III/D-I forgets that fixing mₗ leaves a single orbital.",
    ncert=f"{REF2}, quantum numbers", seconds=50, checked=True)

add("Electronic configuration", I, "statement_pair",
    sp("A ground-state chromium atom (Z = 24) has six unpaired electrons, all with parallel spins.",
       "In a ground-state iron atom (Z = 26), the two 4s electrons are unpaired."),
    SP_, "Ground-state configurations, Hund's rule and the Pauli principle",
    "Cr is [Ar] 3d⁵ 4s¹: five singly occupied 3d orbitals and one 4s electron, six unpaired electrons with "
    "parallel spins (maximum multiplicity). Fe is [Ar] 3d⁶ 4s²: the two 4s electrons share one orbital and must "
    "be paired; the four unpaired electrons are in 3d.",
    ["Cr: 3d⁵ 4s¹ → 6 unpaired, parallel → I true",
     "Fe: 4s² → one orbital, two electrons, opposite spins → II false"],
    answer="C",
    why="Two electrons in the same 4s orbital cannot both be unpaired (Pauli); Fe's unpaired electrons are the "
        "four in 3d.",
    ncert=f"{REF2}, electronic configuration of atoms; stability of half-filled subshells", seconds=40)

n_up = 1 / math.sqrt(1 - 12.75 / 13.6)
assert close(n_up, 4) and 4 * 3 // 2 == 6
add("Bohr model and hydrogen spectrum", A, "numerical",
    "A hydrogen atom in its ground state absorbs a photon of energy 12.75 eV. When the excited atoms return to "
    "the ground state, the highest level reached and the largest number of different spectral lines that a "
    "sample of such atoms can emit are, respectively (Eₙ = −13.6/n² eV):",
    Opts("A", "n = 4; 6 lines", ["n = 4; 3 lines", "n = 3; 3 lines", "n = 5; 10 lines"]),
    "Energy absorbed fixes the level reached; number of lines from level n to the ground state = n(n − 1)/2",
    "The energy of the level reached is −13.6 + 12.75 = −0.85 eV, which is −13.6/16, so n = 4. From n = 4 the "
    "electrons can fall by all possible routes, giving 4 × 3/2 = 6 different lines.",
    ["Eₙ = −13.6 + 12.75 = −0.85 eV", "13.6/n² = 0.85 → n² = 16 → n = 4",
     "Lines = n(n − 1)/2 = 4 × 3/2 = 6"],
    shortcut="12.75 eV = 13.6 × (1 − 1/16), so the jump is 1 → 4.",
    why="'n = 4; 3 lines' counts only the single cascade 4 → 3 → 2 → 1 and misses lines such as 4 → 1 and "
        "4 → 2. 'n = 3' and 'n = 5' come from solving 13.6/n² = 0.85 wrongly.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom; line spectrum of hydrogen", seconds=90, checked=True)

truth_qm = {"a": True, "b": True, "c": False, "d": False, "e": True}
assert 2 - 0 - 1 + 0 == 1 and 1 - 0 - 1 == 0
add("Quantum numbers and orbitals", A, "multi_statement",
    ms("Which of the following statements about the quantum mechanical model of the atom are correct?",
       ["The wave function ψ of an electron has no physical meaning by itself.",
        "An atomic orbital is specified by the three quantum numbers n, l and mₗ.",
        "The probability of finding the electron at a point is given by the value of ψ at that point.",
        "The total number of nodes in an orbital with principal quantum number n is n.",
        "A 1s orbital has no node."]),
    multi("C", truth_qm, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"]),
    "Wave function, probability density, orbitals and nodes",
    "ψ is a mathematical function with no physical meaning; ψ² gives the probability density. An orbital is "
    "fixed by n, l and mₗ (mₛ describes the electron's spin, not the orbital). The total number of nodes is "
    "n − 1 (radial n − l − 1 plus angular l).",
    ["(a) true", "(b) true", "(c) false: probability density is ψ², not ψ",
     "(d) false: total nodes = n − 1", "(e) 1s: n − 1 = 0 nodes → true"],
    why="Options with (c) treat ψ itself as a probability; options with (d) count n nodes instead of n − 1; the "
        "option without (a) leaves out a true statement.",
    ncert=f"{REF2}, quantum mechanical model of atom; orbitals and quantum numbers", seconds=80)

nodes = {"3p": (1, 1), "4d": (1, 2), "4p": (2, 1), "3s": (2, 0)}
assert all(nodes[o] == (int(o[0]) - "spdf".index(o[1]) - 1, "spdf".index(o[1])) for o in nodes)
assert [o for o, v in nodes.items() if v == (2, 1)] == ["4p"]
add("Quantum numbers and orbitals", A, "direct",
    "Which of the following orbitals has two radial (spherical) nodes and one angular node?",
    Opts("C", "4p", ["3p", "4d", "3s"]),
    "Radial nodes = n − l − 1; angular nodes = l",
    "One angular node means l = 1 (a p orbital). Two radial nodes then need n − 1 − 1 = 2, so n = 4.",
    ["Angular nodes = l = 1 → p orbital", "Radial nodes = n − l − 1 = 2 → n = 4", "Orbital = 4p"],
    why="3p has one radial and one angular node. 4d has one radial and two angular nodes. 3s has two radial "
        "nodes but no angular node.",
    ncert=f"{REF2}, shapes of atomic orbitals (nodes)", seconds=45, checked=True)
