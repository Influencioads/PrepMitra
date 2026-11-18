

# =====================================================================================================================
# Kinetic Theory of Gases (B2 I3 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

assert 2 ** 2 == 4
add(T, "Pressure and rms speed", "Basic", "numerical",
    "An ideal gas is kept in a closed rigid container. If the speed of every one of its molecules were doubled, the "
    "pressure of the gas would become:",
    place("4 times", ["2 times", "√2 times", "8 times"], "C"),
    "Kinetic-theory expression for pressure",
    "P = (1/3)nm⟨v²⟩. In a rigid closed container n (molecules per unit volume) and m are fixed, so P ∝ ⟨v²⟩. "
    "Doubling every speed makes ⟨v²⟩ four times. (Each collision transfers twice the momentum, and collisions "
    "happen twice as often.)",
    ["P = (1/3)nm⟨v²⟩", "v → 2v ⇒ ⟨v²⟩ → 4⟨v²⟩", "P → 4P"],
    why="2 times counts only the larger momentum per collision (or takes P ∝ v); √2 times confuses the result with "
        "the rms speed when T doubles; 8 times uses P ∝ v³.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=30, recomputed=True)

add(T, "Pressure and rms speed", "Basic", "direct",
    "According to the kinetic theory of gases, the absolute temperature of an ideal gas is directly proportional "
    "to:",
    place("The average translational kinetic energy of its molecules",
          ["The rms speed of its molecules", "The total linear momentum of its molecules",
           "The number of molecules in the gas"], "A"),
    "Kinetic interpretation of temperature",
    "Kinetic theory gives the average translational kinetic energy of a molecule as (3/2)k_BT, so T is directly "
    "proportional to it. The rms speed is proportional to √T, not to T.",
    ["⟨½mv²⟩ = (3/2)k_BT → T ∝ average KE", "v_rms = √(3k_BT/m) ∝ √T"],
    why="The rms speed varies as √T; the total momentum of a gas at rest in its container is zero on average; "
        "temperature does not depend on how many molecules there are.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=25)

P_f = F(2 * 2 + 3 * 1, 2 + 3)
assert P_f == F(7, 5)
add(T, "Ideal gas equation", "Intermediate", "numerical",
    "A vessel of volume 2 L contains a gas at a pressure of 2 atm and another vessel of volume 3 L contains the same "
    "gas at 1 atm, both at the same temperature. The vessels are connected by a narrow tube of negligible volume and "
    "the temperature is kept the same. Treating the gas as ideal, the final common pressure is:",
    place("1.4 atm", ["1.5 atm", "3 atm", "1.6 atm"], "D"),
    "Ideal gas equation: conservation of the number of moles",
    "At a fixed temperature, the number of moles in each vessel is proportional to PV. The total number of moles "
    "does not change when the vessels are joined, so P_f(V₁ + V₂) = P₁V₁ + P₂V₂.",
    ["P₁V₁ + P₂V₂ = 2 × 2 + 1 × 3 = 7 atm L", "P_f = 7/(2 + 3) = 1.4 atm"],
    why="1.5 atm is the simple average of the pressures; 3 atm adds the pressures; 1.6 atm weights each pressure by "
        "the wrong volume (2 × 3 + 1 × 2)/5.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (ideal gas equation)", seconds=50, recomputed=True)

cv_kg = 1.5 * 8.3 / 0.004
assert close(cv_kg, 3112.5)
add(T, "Degrees of freedom and equipartition", "Intermediate", "numerical",
    "Helium is a monatomic gas of molar mass 4 g/mol. Using the law of equipartition of energy and taking "
    "R = 8.3 J mol⁻¹ K⁻¹, the specific heat capacity of helium at constant volume (per unit mass) is about:",
    place("3.1 × 10³ J kg⁻¹ K⁻¹", ["12.5 J kg⁻¹ K⁻¹", "5.2 × 10³ J kg⁻¹ K⁻¹", "3.1 J kg⁻¹ K⁻¹"], "B"),
    "From molar specific heat to specific heat per unit mass",
    "A monatomic molecule has 3 translational degrees of freedom, so U = (3/2)RT per mole and C_v = (3/2)R per "
    "mole. Dividing by the molar mass in kg/mol gives the value per kilogram.",
    ["Molar C_v = (3/2)R = 12.45 J mol⁻¹ K⁻¹", "c_v = 12.45 / 0.004 kg mol⁻¹ ≈ 3.1 × 10³ J kg⁻¹ K⁻¹"],
    why="12.5 J kg⁻¹ K⁻¹ is the MOLAR value with the wrong unit; 5.2 × 10³ J kg⁻¹ K⁻¹ is c_p, from (5/2)R; "
        "3.1 J kg⁻¹ K⁻¹ divides by 4 instead of 0.004 kg/mol.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy; specific heat capacity",
    seconds=50, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Intermediate", "match_list",
    match_stem("Match List-I (gas molecule) with List-II (number of quadratic terms in its energy that share the "
               "energy, each contributing ½k_BT on average, according to the law of equipartition of energy).",
               ["Helium (monatomic)", "Nitrogen (N₂) with rigid molecules",
                "Nitrogen (N₂) whose molecules also vibrate in one mode", "A rigid non-linear polyatomic molecule"],
               ["6", "3", "7", "5"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
    "Equipartition of energy and degrees of freedom",
    "Translational motion gives 3 terms; a rigid diatomic (linear) molecule adds 2 rotational terms; a rigid "
    "non-linear molecule adds 3. A vibrational mode adds 2 terms (kinetic and potential energy), i.e. k_BT.",
    ["He: 3 translational → 3 (II)", "Rigid N₂: 3 + 2 → 5 (IV)", "Vibrating N₂: 5 + 2 → 7 (III)",
     "Rigid non-linear polyatomic: 3 + 3 → 6 (I)"],
    why="The wrong codes count a vibrational mode as one term instead of two, or give a linear molecule three "
        "rotational terms.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=50)

T_ratio = 32 ** (F(7, 5) - 1)
assert close(float(T_ratio), 4.0) and close(math.sqrt(float(T_ratio)), 2.0)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "An ideal gas of rigid diatomic molecules (γ = 7/5) has an rms molecular speed v. It is compressed reversibly "
    "and adiabatically to 1/32 of its volume. The rms speed of its molecules becomes:",
    place("2v", ["4v", "√2 v", "32v"], "A"),
    "Adiabatic compression and the rms speed",
    "In a reversible adiabatic process TV^(γ−1) is constant, so the temperature rises by 32^(2/5). The rms speed is "
    "proportional to √T.",
    ["T₂/T₁ = (V₁/V₂)^(γ−1) = 32^(2/5) = 4", "v_rms ∝ √T → v₂ = √4 v = 2v"],
    why="4v gives the factor for the temperature, not the speed; √2 v uses the exponent 1/5 instead of 2/5, so T only doubles; "
        "32v treats the speed as proportional to the compression ratio.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature; 'Thermodynamics', adiabatic "
          "process", seconds=80, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Equal masses of hydrogen (H₂) and oxygen (O₂), both treated as ideal gases of rigid diatomic molecules, "
          "have equal internal energies at the same temperature.",
        r="At a given temperature, the average energy of a rigid diatomic molecule is (5/2)k_BT, the same for H₂ and "
          "O₂."),
    ar("D"),
    "Internal energy depends on the number of molecules",
    "R is true by the law of equipartition (3 translational + 2 rotational terms). But equal masses contain very "
    "different numbers of molecules: with molar masses 2 g/mol and 32 g/mol, the hydrogen sample has 16 times as "
    "many molecules, so 16 times the internal energy. So A is false.",
    ["R: energy per molecule = (5/2)k_BT for both → true",
     "A: N(H₂)/N(O₂) = 32/2 = 16 → U(H₂) = 16 U(O₂) → false"],
    why="A is false, so options A, B and C are wrong. Equal energy per molecule does not mean equal energy per unit "
        "mass.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=50)
