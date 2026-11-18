
# ================================================================ Principles Related to Practical Chemistry (2244-2250)
# 2244: FeSO4.7H2O + (NH4)2SO4 + 6H2O -> FeSO4.(NH4)2SO4.6H2O (1 : 1)
n_2244 = F(278, 100) / mm(Fe=1, S=1, O=11, H=14)
v_2244 = g(n_2244 * 392, 2)
assert mm(Fe=1, S=1, O=11, H=14) == 278 and mm(Fe=1, S=2, O=14, N=2, H=20) == 392 and v_2244 == "3.92 g"
# 2246: 2MnO4- + 5H2C2O4 ; 20.0 mL 0.020 M KMnO4 vs 25.0 mL oxalic acid
n_ox = F(5, 2) * F(20, 1000) * F(20, 1000)
M_ox = n_ox / F(25, 1000)
v_2246 = f"{float(M_ox * mm(C=2, H=6, O=6)):.2f} g L⁻¹"
assert M_ox == F(4, 100) and mm(C=2, H=6, O=6) == 126 and v_2246 == "5.04 g L⁻¹"
assert f"{float(M_ox * 90):.2f}" == "3.60"                                               # anhydrous molar mass
# 2248: group II cations (H2S in dilute HCl)
group = {"Cu2+": 2, "Cd2+": 2, "As3+": 2, "Zn2+": 4, "Ni2+": 4, "Al3+": 3, "Ba2+": 5}
v_2248 = str(sum(1 for gr in group.values() if gr == 2))
assert v_2248 == "3"
# 2249: C2H5OH + 4I2 + 6NaOH -> CHI3 + HCOONa + 5NaI + 5H2O
n_2249 = F(23, 10) / mm(C=2, H=6, O=1)
m_i2 = n_2249 * 4 * 254
m_chi3 = n_2249 * mm(C=1, H=1, I=3)
assert n_2249 == F(1, 20) and (m_i2, m_chi3) == (F(508, 10), F(197, 10))
v_2249 = f"{float(m_i2):.1f} g and {float(m_chi3):.1f} g"
assert v_2249 == "50.8 g and 19.7 g"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O (molar mass 392 g mol⁻¹), is prepared by crystallising an equimolar solution "
      "of ferrous sulphate and ammonium sulphate. The maximum mass of Mohr's salt that can be obtained from 2.78 g of "
      "FeSO₄·7H₂O (molar mass 278 g mol⁻¹) with excess ammonium sulphate is:",
      [v_2244, "2.78 g", "1.96 g", "7.84 g"], "A", v_2244,
      "Preparation of a double salt",
      "One mole of FeSO₄·7H₂O gives one mole of the double salt, which crystallises with six molecules of water.",
      ["n(FeSO₄·7H₂O) = 2.78/278 = 0.010 mol", "n(Mohr's salt) = 0.010 mol", "Mass = 0.010 × 392 = 3.92 g"],
      why_others_wrong="2.78 g assumes equal masses; 1.96 g and 7.84 g halve or double the moles.",
      ncert=f"{LAB}, preparation of double salts: Mohr's salt", seconds=40),

    Q(T_PR, "Detection of elements and functional groups", "Basic", "direct",
      "A sample is heated with a little solid potassium hydrogensulphate, and a pungent, irritating smell of acrolein "
      "is noticed. The sample is most likely:",
      ["a protein", "a carbohydrate", "a fat or oil", "an amino acid"], "C",
      "Test for fats and oils",
      "On heating with KHSO₄ (a dehydrating agent), the glycerol part of a fat or oil is dehydrated to acrolein "
      "(propenal), which has a sharp, irritating smell. This acrolein test identifies fats and oils.",
      ["Fat/oil → glycerol part", "KHSO₄, heat: glycerol → CH₂=CH–CHO (acrolein)", "Pungent smell → fat or oil"],
      why_others_wrong="Proteins and amino acids are tested by the biuret and ninhydrin tests, carbohydrates by "
                       "Molisch's test.",
      ncert=f"{LAB}, tests for carbohydrates, fats and proteins", seconds=25),

    N(T_PR, "Titrimetric analysis", "Intermediate",
      "25.0 mL of an oxalic acid solution needs 20.0 mL of 0.020 M KMnO₄ for complete reaction in dilute H₂SO₄. The "
      "strength of the oxalic acid solution, expressed as grams of crystalline oxalic acid, H₂C₂O₄·2H₂O, per litre, "
      "is (C = 12, H = 1, O = 16):",
      ["3.60 g L⁻¹", "2.02 g L⁻¹", v_2246, "12.6 g L⁻¹"], "C", v_2246,
      "Permanganate–oxalic acid titration",
      "In acid, 2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O, so 2 mol MnO₄⁻ react with 5 mol oxalic acid.",
      ["n(MnO₄⁻) = 0.020 × 0.0200 = 4.0 × 10⁻⁴ mol", "n(oxalic acid) = 5/2 × 4.0 × 10⁻⁴ = 1.0 × 10⁻³ mol",
       "Molarity = 1.0 × 10⁻³/0.0250 = 0.040 M", "Strength = 0.040 × 126 = 5.04 g L⁻¹"],
      why_others_wrong="3.60 g L⁻¹ uses the anhydrous molar mass (90); 2.02 g L⁻¹ takes a 1 : 1 mole ratio; "
                       "12.6 g L⁻¹ takes the solution as 0.1 M.",
      ncert=f"{LAB}, titrimetric exercises: oxalic acid vs KMnO₄", seconds=75),

    Q(T_PR, "Titrimetric analysis", "Intermediate", "assertion_reason",
      *ar("In the titration of oxalic acid with KMnO₄, the first few drops of permanganate are decolourised slowly, "
          "but later drops are decolourised almost at once.", True,
          "The Mn²⁺ ions formed in the reaction catalyse the reaction between permanganate and oxalic acid "
          "(autocatalysis).", True, explains=True),
      "Autocatalysis in permanganate titrations",
      "At the start no Mn²⁺ is present and the reaction is slow even in warm solution. As soon as some Mn²⁺ forms, it "
      "catalyses the reaction, so it speeds up. R explains A.",
      ["Start: no Mn²⁺ → slow", "Mn²⁺ produced → catalyst", "Reaction becomes fast (autocatalysis)"],
      ncert=f"{LAB}, titration of oxalic acid with potassium permanganate", seconds=35),

    N(T_PR, "Qualitative salt analysis", "Intermediate",
      "In systematic salt analysis, how many of the following cations are precipitated in group II, as sulphides by "
      "H₂S in the presence of dilute HCl?\nCu²⁺, Cd²⁺, As³⁺, Zn²⁺, Ni²⁺, Al³⁺, Ba²⁺",
      ["1", "2", v_2248, "4"], "C", v_2248,
      "Group separation of cations",
      "In dilute HCl the sulphide ion concentration is kept low (common ion effect on H₂S), so only the sulphides with "
      "very low solubility products (group II) precipitate. Zn²⁺ and Ni²⁺ come down as sulphides only in ammoniacal "
      "solution (group IV); Al³⁺ is precipitated as hydroxide in group III and Ba²⁺ as carbonate in group V.",
      ["Group II: Cu²⁺, Cd²⁺, As³⁺", "Group III: Al³⁺; group IV: Zn²⁺, Ni²⁺; group V: Ba²⁺", "Count = 3"],
      why_others_wrong="4 wrongly places Zn²⁺ or Ni²⁺ in group II; 1 or 2 miss Cd²⁺ or As³⁺.",
      ncert=f"{LAB}, qualitative analysis of cations", seconds=45),

    N(T_PR, "Preparations", "Advanced",
      "Iodoform is prepared in the laboratory by warming ethanol with iodine and aqueous NaOH:\n"
      "C₂H₅OH + 4I₂ + 6NaOH → CHI₃ + HCOONa + 5NaI + 5H₂O\n"
      "For complete conversion of 2.3 g of ethanol, the minimum mass of iodine needed and the mass of iodoform "
      "formed are, respectively (C = 12, H = 1, O = 16, I = 127):",
      [v_2249, "12.7 g and 19.7 g", "50.8 g and 39.4 g", "38.1 g and 19.7 g"], "A", v_2249,
      "Stoichiometry of the iodoform reaction",
      "Ethanol is first oxidised to ethanal by the hypoiodite (one I₂), and the CH₃ group of ethanal is then "
      "tri-iodinated (three I₂) before cleavage, so 4 mol I₂ are used per mole of ethanol.",
      ["n(C₂H₅OH) = 2.3/46 = 0.050 mol", "I₂ = 4 × 0.050 = 0.20 mol × 254 = 50.8 g",
       "CHI₃ (394 g mol⁻¹) = 0.050 × 394 = 19.7 g"],
      why_others_wrong="12.7 g uses one I₂ per ethanol; 38.1 g uses three (forgets the oxidation step); 39.4 g doubles "
                       "the iodoform.",
      ncert=f"{LAB}, preparation of iodoform", seconds=90),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "multi_statement",
      *ms("Which of the following statements about the kinetics experiments in the laboratory are correct?",
          [("In the reaction of sodium thiosulphate with hydrochloric acid, the time for a cross mark under the flask to "
            "disappear is taken as inversely proportional to the rate.", True),
           ("In that reaction, the turbidity is due to colloidal sulphur formed in the reaction.", True),
           ("In the iodide–hydrogen peroxide clock reaction with starch and a little thiosulphate, the blue colour "
            "appears only after all the added thiosulphate has been used up.", True),
           ("Raising the temperature increases the time taken for the cross to disappear.", False),
           ("Starch acts as a catalyst in the iodide–hydrogen peroxide reaction.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
      "Following reaction rates by a visual end point",
      "Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S + H₂O: the sulphur makes the solution turbid, and the faster the reaction the "
      "sooner the cross is hidden, so rate ∝ 1/t. In the clock reaction, the iodine formed is reduced back to iodide "
      "by thiosulphate; only when the thiosulphate is used up does iodine remain and give the blue starch–iodine "
      "colour. Starch is only an indicator. A higher temperature speeds up the reaction and shortens the time.",
      ["(a) true", "(b) true", "(c) true", "(d) false: higher temperature → shorter time",
       "(e) false: starch is an indicator"],
      ncert=f"{LAB}, chemical kinetics experiments", seconds=55),
]
