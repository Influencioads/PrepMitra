

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

period_sizes = [2, 8, 8, 18, 18]
assert sum(period_sizes) == 54 and sum(period_sizes[:4]) == 36 and sum([2, 8, 18, 18, 32]) == 78
add("Modern periodic table", B, "numerical",
    "The total number of elements in the first five periods of the long form of the periodic table is:",
    Opts("C", "54", ["36", "78", "50"]),
    "Number of elements in each period of the modern periodic table",
    "Periods 1 to 5 contain 2, 8, 8, 18 and 18 elements respectively. The fifth period ends with xenon, "
    "Z = 54.",
    ["2 + 8 + 8 + 18 + 18 = 54", "Check: the fifth period ends at Xe (Z = 54)"],
    why="36 stops at the end of the fourth period (krypton). 78 takes the third period as 18 and the fifth as 32 "
        "elements (2 + 8 + 18 + 18 + 32). 50 is the sum 2 + 8 + 8 + 18 + 14, mixing in the 14 f-block elements.",
    ncert=f"{REF9}, modern periodic law and the present form of the periodic table", seconds=30, checked=True)

add("Modern periodic table", B, "direct",
    "Which of the following pairs of atomic numbers belongs to elements of the SAME group?",
    Opts("A", "12 and 38", ["11 and 21", "17 and 25", "6 and 22"]),
    "Group from the electronic configuration",
    "Z = 12 is magnesium ([Ne] 3s²) and Z = 38 is strontium ([Kr] 5s²); both are group 2 elements.",
    ["12: [Ne] 3s² → group 2", "38: [Kr] 5s² → group 2 ✓", "11 (group 1) and 21 (Sc, group 3)",
     "17 (group 17) and 25 (Mn, group 7)", "6 (group 14) and 22 (Ti, group 4)"],
    why="The other pairs have similar numbers of outer electrons, but one member of each is a d-block element "
        "(Sc, Mn, Ti) whose group number counts its (n − 1)d electrons as well, so it is in a different group.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=40)

add("Modern periodic table", I, "statement_pair",
    sp("The number of elements in each period of the periodic table is twice the number of atomic orbitals "
       "available in the energy level that is being filled.",
       "The fifth period begins with the filling of the 5s orbital and, after the 4d orbitals, ends with the "
       "filling of the 5p orbitals, so it contains 18 elements."),
    SP_, "Electronic configurations and the lengths of the periods",
    "Each orbital holds two electrons, so the number of elements in a period equals 2 × (number of orbitals "
    "being filled). In period 5 the orbitals filled are 5s (1), 4d (5) and 5p (3): 9 orbitals → 18 elements.",
    ["I: NCERT statement → true", "II: 5s + 4d + 5p = 1 + 5 + 3 = 9 orbitals → 18 elements → true"],
    answer="A",
    why="Both statements are correct, so any option that marks one of them false is wrong.",
    ncert=f"{REF9}, electronic configurations of elements and the periodic table", seconds=45, checked=True)

add("Modern periodic table", I, "match_list",
    lists("Match List-I (atomic number) with List-II (position of the element in the periodic table).",
          ["Z = 16", "Z = 30", "Z = 53", "Z = 56"],
          ["Period 5, group 17", "Period 6, group 2", "Period 3, group 16", "Period 4, group 12"]),
    match("C", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "Locating an element from its atomic number",
    "Write the configuration and read the period from the highest n and the group from the outer electrons.",
    ["16: [Ne] 3s² 3p⁴ → period 3, group 16 → III", "30: [Ar] 3d¹⁰ 4s² → period 4, group 12 → IV",
     "53: [Kr] 4d¹⁰ 5s² 5p⁵ → period 5, group 17 → I", "56: [Xe] 6s² → period 6, group 2 → II"],
    why="B-I/C-IV swaps zinc and iodine. A-IV/B-III swaps sulphur and zinc. C-II/D-I swaps iodine and barium.",
    ncert=f"{REF9}, electronic configurations and types of elements", seconds=60)

truth_cmp = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Atomic and ionic radii", I, "multi_statement",
    ms("Which of the following comparisons are correct?",
       ["Atomic radius: Ca > Mg",
        "Electronegativity: P > Si",
        "First ionisation enthalpy: Be > Li",
        "Ionic radius: Na⁺ > F⁻",
        "Atomic radius: O > N"]),
    multi("D", truth_cmp, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Periodic trends in radius, electronegativity and ionisation enthalpy",
    "Radius increases down a group and decreases across a period; electronegativity and (generally) "
    "ionisation enthalpy increase across a period. Among isoelectronic ions, the one with the larger nuclear "
    "charge is smaller.",
    ["(a) Ca is below Mg in group 2 → larger ✓", "(b) P is to the right of Si → more electronegative ✓",
     "(c) Be (2s²) holds its electrons more tightly than Li (2s¹) ✓",
     "(d) Na⁺ (Z = 11) and F⁻ (Z = 9) are isoelectronic; F⁻ is larger ✗",
     "(e) O is to the right of N → smaller ✗"],
    why="(d) reverses the isoelectronic order and (e) reverses the trend across a period; options containing "
        "either are wrong.",
    ncert=f"{REF9}, periodic trends in physical properties", seconds=60)

add("Ionisation and electron gain enthalpy", A, "assertion_reason",
    ar("The second ionisation enthalpy of sodium is many times larger than its first ionisation enthalpy.",
       "After the first electron is lost, Na⁺ has the stable neon configuration, and the next electron has to "
       "be removed from the inner 2p subshell, which is much closer to the nucleus."),
    AR_, "Successive ionisation enthalpies",
    "Na is [Ne] 3s¹. Removing the 3s electron is easy. The second electron must come out of the compact, "
    "noble-gas 2p⁶ core, which is nearer the nucleus and less shielded, so far more energy is needed. R is the "
    "reason for A.",
    ["Na → Na⁺: remove 3s¹ (easy)", "Na⁺ → Na²⁺: remove a 2p electron from the [Ne] core (very hard)",
     "Hence ΔiH₂ ≫ ΔiH₁ → R explains A"],
    answer="A",
    why="R gives exactly why the jump occurs after the first electron for a group 1 element, so it is the "
        "correct explanation.",
    ncert=f"{REF9}, ionization enthalpy", seconds=40)

ies = {"A": [520, 7298, 11815], "B": [899, 1757, 14848], "C": [801, 2427, 3660, 25025],
       "D": [1086, 2352, 4620, 6223, 37831]}


def jump_after(v):
    return max(range(len(v) - 1), key=lambda i: v[i + 1] / v[i]) + 1


assert {k: jump_after(v) for k, v in ies.items()} == {"A": 1, "B": 2, "C": 3, "D": 4}
add("Valence and reactivity", A, "match_list",
    lists("Match List-I (successive ionisation enthalpies of an element, in kJ mol⁻¹, starting from the first) "
          "with List-II (the group to which the element belongs).",
          ["520, 7298, 11815", "899, 1757, 14848", "801, 2427, 3660, 25025",
           "1086, 2352, 4620, 6223, 37831"],
          ["Group 13", "Group 1", "Group 14", "Group 2"]),
    match("B", M("II IV I III"), [M("IV II I III"), M("II IV III I"), M("II I IV III")]),
    "Valence electrons from the jump in successive ionisation enthalpies",
    "A very large jump appears when the first electron is taken from the inner noble-gas core. The number of "
    "ionisation enthalpies before the jump equals the number of valence electrons.",
    ["A: jump after the 1st → 1 valence electron → group 1 → II",
     "B: jump after the 2nd → 2 valence electrons → group 2 → IV",
     "C: jump after the 3rd → 3 valence electrons → group 13 → I",
     "D: jump after the 4th → 4 valence electrons → group 14 → III"],
    why="A-IV/B-II swaps the group 1 and group 2 patterns. C-III/D-I swaps the group 13 and 14 "
        "patterns. B-I/C-IV puts the jump one place too late for B.",
    ncert=f"{REF9}, ionization enthalpy; valence", seconds=90, checked=True)
