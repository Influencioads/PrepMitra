
# ================================================================ Principles Related to Practical Chemistry (2491-2500)
# 2491: lyophilic sols among the listed substances
lyo_2491 = {"starch": True, "gum": True, "egg albumin": True, "ferric hydroxide": False,
            "arsenious sulphide": False, "aluminium hydroxide": False}
v_2491 = str(sum(lyo_2491.values()))
assert v_2491 == "3"
# 2494: anions that give a gas when warmed with dilute H2SO4: CO3 2- (CO2), S 2- (H2S), NO2- (NO2 fumes)
dil_2494 = {"CO3": True, "S": True, "NO2": True, "SO4": False, "NO3": False, "Cl": False, "Br": False, "I": False}
v_2494 = str(sum(dil_2494.values()))
assert v_2494 == "3"
# 2495: 0.535 g NH4Cl -> NH3 (with NaOH) -> neutralised by 0.10 M HCl
n_2495 = F(535, 1000) / mm(N=1, H=4, Cl=1)
V_2495 = n_2495 / F(1, 10) * 1000
assert mm(N=1, H=4, Cl=1) == F(535, 10) and n_2495 == F(1, 100) and V_2495 == 100
v_2495 = "100 mL"
# 2498: rate = k[H2O2]^x [I-]^y from three experiments
exps = [(F(1, 100), F(2, 100), F(2, 10**6)), (F(2, 100), F(2, 100), F(4, 10**6)), (F(2, 100), F(4, 100), F(8, 10**6))]
x = exps[1][2] / exps[0][2]  # [H2O2] doubled
y = exps[2][2] / exps[1][2]  # [I-] doubled
assert x == 2 and y == 2  # first order in each
k_2498 = exps[0][2] / (exps[0][0] * exps[0][1])
assert k_2498 == F(1, 100) and all(r / (a * b) == k_2498 for a, b, r in exps)
assert exps[0][2] / exps[0][0] == F(2, 10**4) and exps[0][2] / exps[0][1] == F(1, 10**4)
assert exps[0][2] / (exps[0][0] * exps[0][1] ** 2) == F(5, 10)
v_2498 = "1.0 × 10⁻² L mol⁻¹ s⁻¹"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "In the laboratory, sols are prepared of the following substances. How many of them form lyophilic sols?\n"
      "Starch, gum, egg albumin, ferric hydroxide, arsenious sulphide, aluminium hydroxide",
      ["1", "2", v_2491, "4"], "C", v_2491,
      "Lyophilic and lyophobic sols",
      "Lyophilic sols are formed directly by warming and stirring substances such as starch, gum and egg albumin "
      "with water. Ferric hydroxide, aluminium hydroxide and arsenious sulphide give lyophobic sols, which need "
      "special methods (hydrolysis, double decomposition).",
      ["Lyophilic: starch, gum, egg albumin → 3", "Lyophobic: Fe(OH)₃, As₂S₃, Al(OH)₃"],
      why_others_wrong="Counts of 1 or 2 miss gum or egg albumin; 4 counts a metal hydroxide sol, which is "
                       "lyophobic.",
      ncert=f"{LAB}, preparation of lyophilic and lyophobic sols", seconds=30),

    Q(T_PR, "Preparations", "Basic", "direct",
      "In the laboratory, a lyophobic sol of arsenious sulphide, As₂S₃, is prepared by:",
      ["adding iron(III) chloride solution drop by drop to boiling water",
       "passing hydrogen sulphide gas through a dilute aqueous solution of arsenious oxide",
       "warming arsenious oxide with water and stirring well",
       "adding sodium hydroxide solution to aluminium sulphate solution"], "B",
      "Preparation of a lyophobic sol by double decomposition",
      "Arsenious sulphide sol is made by a chemical reaction: H₂S is passed through a dilute solution of As₂O₃ in "
      "water, As₂O₃ + 3H₂S → As₂S₃ (sol) + 3H₂O.",
      ["As₂O₃ + 3H₂S → As₂S₃ (colloidal) + 3H₂O"],
      why_others_wrong="FeCl₃ in boiling water gives a ferric hydroxide sol; simply warming and stirring works only "
                       "for lyophilic substances; NaOH with aluminium sulphate gives a precipitate of Al(OH)₃.",
      ncert=f"{LAB}, preparation of lyophobic sols", seconds=30),

    Q(T_PR, "Titrimetric analysis", "Basic", "statement_pair",
      *sp("Phenolphthalein is colourless in acidic solution and pink in alkaline solution.", True,
          "Methyl orange is red in acidic solution and yellow in alkaline solution.", True),
      "Acid–base indicators",
      "Phenolphthalein is colourless in acid and turns pink in alkali; methyl orange is red in acid and yellow in "
      "alkali. These colour changes are used to detect the end points of acid–base titrations.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{LAB}, titrimetric analysis: indicators", seconds=25),

    N(T_PR, "Qualitative salt analysis", "Intermediate",
      "In salt analysis, a little of each salt is warmed with dilute H₂SO₄. How many of the following anions give a "
      "gas under these conditions?\nCO₃²⁻, S²⁻, NO₂⁻, SO₄²⁻, NO₃⁻, Cl⁻, Br⁻, I⁻",
      ["2", v_2494, "4", "5"], "B", v_2494,
      "Dilute sulphuric acid group of anions",
      "Carbonate gives CO₂ (turns lime water milky), sulphide gives H₂S (turns lead acetate paper black) and nitrite "
      "gives brown fumes of NO₂ with dilute H₂SO₄. Nitrate, chloride, bromide and iodide react only with "
      "concentrated H₂SO₄; sulphate does not react.",
      ["Dilute H₂SO₄ group: CO₃²⁻, S²⁻, NO₂⁻ → 3",
       "Concentrated H₂SO₄ group: NO₃⁻, Cl⁻, Br⁻, I⁻; SO₄²⁻: neither"],
      why_others_wrong="2 usually forgets the nitrite ion; 4 or 5 add halides or nitrate, which need concentrated "
                       "H₂SO₄.",
      ncert=f"{LAB}, qualitative analysis: tests for anions", seconds=40),

    N(T_PR, "Qualitative salt analysis", "Intermediate",
      "In the test for NH₄⁺, 0.535 g of ammonium chloride is heated with an excess of NaOH solution, and all the "
      "ammonia evolved is absorbed in 0.10 M HCl. The volume of the acid exactly neutralised is (N = 14, H = 1, "
      "Cl = 35.5):",
      ["10 mL", "50 mL", "200 mL", v_2495], "D", v_2495,
      "Ammonia from ammonium salts",
      "NH₄Cl + NaOH → NaCl + NH₃ + H₂O; NH₃ + HCl → NH₄Cl. One mole of ammonium chloride gives one mole of NH₃, "
      "which neutralises one mole of HCl.",
      ["NH₄Cl: 0.535 / 53.5 = 0.010 mol → 0.010 mol NH₃", "HCl: 0.010 mol / 0.10 M = 0.10 L = 100 mL"],
      why_others_wrong="50 mL halves the ammonia; 200 mL doubles it; 10 mL uses the molarity as 1.0 M.",
      ncert=f"{LAB}, qualitative analysis: test for ammonium ion", seconds=40),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Intermediate", "statement_pair",
      *sp("In the reaction of iodide ions with hydrogen peroxide in acidic solution at room temperature, the rate "
          "increases when the concentration of iodide ions is increased.", True,
          "The rate of this reaction does not depend on the concentration of hydrogen peroxide.", False),
      "Kinetics of the iodide–hydrogen peroxide reaction",
      "The reaction H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O follows the rate law rate = k[H₂O₂][I⁻] under the experimental "
      "conditions, so the rate rises with an increase in the concentration of either reactant.",
      ["Statement I: true", "Statement II: false; first order in H₂O₂"],
      ncert=f"{LAB}, chemical kinetics: reaction of iodide ions with hydrogen peroxide", seconds=35),

    Q(T_PR, "Preparations", "Intermediate", "match_list",
      *ml("Match the compound prepared in the laboratory (List-I) with the starting materials used (List-II).",
          ["Mohr's salt", "Potash alum", "p-Nitroacetanilide", "Iodoform"],
          ["Acetanilide, with a mixture of concentrated HNO₃ and concentrated H₂SO₄",
           "Ethanol or acetone, warmed with iodine and alkali",
           "Iron(II) sulphate and ammonium sulphate, with a little dilute H₂SO₄",
           "Potassium sulphate and aluminium sulphate"],
          "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A"),
      "Laboratory preparations",
      "Mohr's salt crystallises from an equimolar solution of FeSO₄ and (NH₄)₂SO₄ (dilute H₂SO₄ prevents "
      "hydrolysis); potash alum from K₂SO₄ and Al₂(SO₄)₃; p-nitroacetanilide by nitrating acetanilide; iodoform by "
      "the haloform reaction of ethanol or acetone with iodine and alkali.",
      ["A → III", "B → IV", "C → I", "D → II"],
      why_others_wrong="Swapping Mohr's salt and potash alum confuses the two double sulphates; swapping "
                       "p-nitroacetanilide and iodoform pairs a nitration with a haloform reaction.",
      ncert=f"{LAB}, preparation of inorganic and organic compounds", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "The initial rate of the reaction H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O was measured at room temperature at a fixed, "
      "excess acidity:\n"
      "Experiment 1: [H₂O₂] = 0.010 M, [I⁻] = 0.020 M, rate = 2.0 × 10⁻⁶ mol L⁻¹ s⁻¹\n"
      "Experiment 2: [H₂O₂] = 0.020 M, [I⁻] = 0.020 M, rate = 4.0 × 10⁻⁶ mol L⁻¹ s⁻¹\n"
      "Experiment 3: [H₂O₂] = 0.020 M, [I⁻] = 0.040 M, rate = 8.0 × 10⁻⁶ mol L⁻¹ s⁻¹\n"
      "The rate constant of the reaction is:",
      ["2.0 × 10⁻⁴ s⁻¹", "1.0 × 10⁻⁴ s⁻¹", v_2498, "5.0 × 10⁻¹ L² mol⁻² s⁻¹"], "C", v_2498,
      "Finding orders and the rate constant from initial rates",
      "Compare experiments in which only one concentration changes to find each order, then substitute any one "
      "experiment into the rate law.",
      ["Exp 1 → 2: [H₂O₂] doubled, rate doubled → first order in H₂O₂",
       "Exp 2 → 3: [I⁻] doubled, rate doubled → first order in I⁻",
       "k = 2.0 × 10⁻⁶ / (0.010 × 0.020) = 1.0 × 10⁻² L mol⁻¹ s⁻¹"],
      why_others_wrong="2.0 × 10⁻⁴ s⁻¹ and 1.0 × 10⁻⁴ s⁻¹ treat the reaction as first order overall in one reactant "
                       "only; 5.0 × 10⁻¹ L² mol⁻² s⁻¹ assumes second order in iodide.",
      ncert=f"{LAB}, chemical kinetics: reaction of iodide ions with hydrogen peroxide", seconds=90),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "assertion_reason",
      *ar("Zn²⁺ is precipitated as ZnS when H₂S is passed through its ammoniacal solution, but not when H₂S is passed "
          "through its solution acidified with dilute HCl.", True,
          "In ammoniacal solution the ionisation of H₂S increases, so the sulphide ion concentration becomes high "
          "enough for the ionic product of ZnS to exceed its solubility product.", True, explains=True),
      "Group separation by control of sulphide ion concentration",
      "H₂S ⇌ 2H⁺ + S²⁻. In dilute HCl the common ion H⁺ suppresses ionisation, and [S²⁻] is so low that only sulphides "
      "with very low Ksp (group II) precipitate. NH₄OH removes H⁺, increasing ionisation and [S²⁻], so ZnS (higher "
      "Ksp, group IV) precipitates. R explains A.",
      ["Acidic: low [S²⁻] → ionic product of ZnS < Ksp", "Ammoniacal: high [S²⁻] → ionic product > Ksp → ZnS"],
      ncert=f"{LAB}, qualitative analysis of cations: group IV", seconds=50),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "multi_statement",
      *ms("The enthalpy of neutralisation of hydrochloric acid by sodium hydroxide is determined by mixing equal "
          "volumes of the two solutions, of the same molarity, in a calorimeter. Which of the following statements "
          "are correct?",
          [("Using 1.0 M solutions instead of 0.5 M solutions (same volumes) gives a larger rise in temperature.",
            True),
           ("Using half the volumes of the same solutions gives about half the rise in temperature.", False),
           ("The heat capacity of the calorimeter must be taken into account to get an accurate value.", True),
           ("Per mole of water formed, about the same value is obtained if nitric acid is used instead of "
            "hydrochloric acid.", True),
           ("The enthalpy of neutralisation of ethanoic acid by NaOH is more negative than that of HCl by NaOH.",
            False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "d", "e"]], "B"),
      "Calorimetric determination of the enthalpy of neutralisation",
      "Doubling the concentrations doubles the heat released into the same mass of solution, so ΔT is larger. "
      "Halving both volumes halves both the heat released and the mass to be heated, so ΔT stays about the same "
      "(ignoring the calorimeter). Part of the heat warms the calorimeter, so its heat capacity is needed. Any strong "
      "acid with a strong base gives about −57 kJ per mole of water. A weak acid such as ethanoic acid gives a less "
      "negative value, because some heat is used to ionise it.",
      ["(a) true", "(b) false: ΔT is about the same", "(c) true", "(d) true", "(e) false: less negative"],
      why_others_wrong="Options with (b) forget that the mass of solution is halved along with the heat; options "
                       "with (e) reverse the weak-acid effect.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation", seconds=75),
]
