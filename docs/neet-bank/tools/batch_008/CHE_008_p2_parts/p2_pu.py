
# ================================================================ Purification and Characterisation (1889-1895)
# 1890: C 40.0 %, H 6.67 %, O 53.33 % -> CH2O
mol_ratio = [F(4000, 100) / 12, F(667, 100) / 1, F(5333, 100) / 16]
small = min(mol_ratio)
assert [round(float(x / small), 2) for x in mol_ratio] == [1.0, 2.0, 1.0]
v_1890 = "CH₂O"
# 1891: M from vapour: 0.88 g occupies 224 mL at STP -> 88 g/mol; C 54.55 %, H 9.09 %, O rest
M_1891 = F(88, 100) / F(224, 22400)
assert M_1891 == 88
nC, nH = round(88 * 0.5455 / 12), round(88 * 0.0909 / 1)
nO = (88 - 12 * nC - nH) // 16
assert (nC, nH, nO) == (4, 8, 2) and 12 * nC + nH + 16 * nO == 88
v_1891 = "C₄H₈O₂"
# 1894: Dumas 56 mL N2 at STP -> mol N atoms; Kjeldahl NH3 = mol N; 2NH3 + H2SO4 -> 1 : 2
nN = 2 * F(56, 22400)
v_mL = nN / 2 / F(1, 10) * 1000
assert v_mL == 25
v_1894 = "25 mL"

QUESTIONS += [
    Q(T_PU, "Qualitative analysis", "Basic", "direct",
      "The sodium fusion extract of an organic compound is acidified with acetic acid and lead acetate solution is "
      "added. A black precipitate forms. This shows the presence of:",
      ["Nitrogen", "Chlorine", "Sulphur", "Phosphorus"], "C",
      "Test for sulphur in Lassaigne's extract",
      "During sodium fusion, sulphur of the compound is converted into sodium sulphide. With lead acetate, sulphide "
      "ions give black lead sulphide: S²⁻ + Pb²⁺ → PbS (black).",
      ["Na + S (from compound) → Na₂S", "Na₂S + (CH₃COO)₂Pb → PbS↓ (black)"],
      why_others_wrong="Nitrogen is shown by Prussian blue, chlorine by a white AgCl precipitate, and phosphorus by "
                       "the yellow ammonium molybdate test.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis: test for "
            f"sulphur", seconds=25),

    N(T_PU, "Quantitative analysis and formulae", "Basic",
      "An organic compound contains 40.0% carbon, 6.67% hydrogen and 53.33% oxygen by mass. Its empirical formula is "
      "(C = 12, H = 1, O = 16):",
      ["CH₂O", "CHO", "C₂H₄O", "CH₃O"], "A", v_1890,
      "Empirical formula from percentage composition",
      "Divide each percentage by the atomic mass and then by the smallest quotient.",
      ["C: 40.0/12 = 3.33", "H: 6.67/1 = 6.67", "O: 53.33/16 = 3.33", "Ratio C : H : O = 1 : 2 : 1 → CH₂O"],
      why_others_wrong="CHO ignores the factor 2 for hydrogen; C₂H₄O doubles C and H but not O; CH₃O misreads the "
                       "hydrogen ratio.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=40),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "An organic compound containing only C, H and O has 54.55% carbon and 9.09% hydrogen by mass. 0.88 g of its "
      "vapour occupies 224 mL at STP. Its molecular formula is (C = 12, H = 1, O = 16; molar volume at STP = "
      "22400 mL):",
      ["C₂H₄O", "C₃H₄O₃", "C₅H₁₂O", "C₄H₈O₂"], "D", v_1891,
      "Molecular formula from percentage composition and molar mass",
      "Molar mass = mass / moles of vapour. Oxygen is found by difference. Then each element's share of the molar "
      "mass gives the number of atoms.",
      ["n = 224/22400 = 0.01 mol → M = 0.88/0.01 = 88 g mol⁻¹", "%O = 100 − 54.55 − 9.09 = 36.36",
       "C: 0.5455 × 88/12 = 4; H: 0.0909 × 88 = 8; O: 0.3636 × 88/16 = 2", "Molecular formula C₄H₈O₂"],
      why_others_wrong="C₂H₄O is only the empirical formula (M = 44); C₃H₄O₃ and C₅H₁₂O have M = 88 but the wrong "
                       "percentages of C and H.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=75),

    Q(T_PU, "Qualitative analysis", "Intermediate", "assertion_reason",
      *ar("Nitrogen, sulphur and halogens present in an organic compound cannot be detected directly with the usual "
          "reagents for their ions, so the compound is first fused with sodium.", True,
          "These elements are covalently bonded in organic compounds; fusion with sodium converts them into ionic "
          "compounds such as NaCN, Na₂S and NaX.", True, explains=True),
      "Purpose of sodium fusion (Lassaigne's test)",
      "Ionic tests (Prussian blue, nitroprusside, AgNO₃) need the elements as ions. Because they are covalently "
      "bonded in the compound, fusion with sodium is used to convert them into ionic salts, which are extracted "
      "with water. R explains A.",
      ["Elements covalently bonded → no ions to test", "Na fusion → NaCN, Na₂S, NaX", "Extract tested for ions"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis", seconds=40),

    Q(T_PU, "Qualitative analysis", "Intermediate", "statement_pair",
      *sp("In the test for nitrogen, the sodium fusion extract is boiled with iron(II) sulphate and then acidified "
          "with concentrated sulphuric acid; on heating, some iron(II) ions are oxidised to iron(III) ions, which "
          "react with the hexacyanidoferrate(II) formed.", True,
          "The Prussian blue precipitate obtained in this test is iron(III) hexacyanidoferrate(II), "
          "Fe₄[Fe(CN)₆]₃·xH₂O.", True),
      "Chemistry of the Prussian blue test",
      "NaCN in the extract gives Na₄[Fe(CN)₆] with iron(II) sulphate. On heating with concentrated H₂SO₄, some Fe²⁺ "
      "is oxidised to Fe³⁺, "
      "which with [Fe(CN)₆]⁴⁻ gives Prussian blue, Fe₄[Fe(CN)₆]₃·xH₂O. Both statements are true.",
      ["6CN⁻ + Fe²⁺ → [Fe(CN)₆]⁴⁻", "Some Fe²⁺ → Fe³⁺ on heating", "3[Fe(CN)₆]⁴⁻ + 4Fe³⁺ → Fe₄[Fe(CN)₆]₃·xH₂O"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', test for nitrogen", seconds=45),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "In a Dumas determination, 0.30 g of an organic compound gave 56 mL of nitrogen gas, corrected to STP. If "
      "another 0.30 g of the same compound were analysed by Kjeldahl's method (assume the method is applicable), the "
      "ammonia evolved would exactly neutralise what volume of 0.10 M H₂SO₄? (Molar volume at STP = 22400 mL)",
      ["50 mL", "25 mL", "12.5 mL", "250 mL"], "B", v_1894,
      "Linking the Dumas and Kjeldahl methods through the moles of nitrogen atoms",
      "Each N₂ molecule carries two N atoms, and each N atom gives one NH₃ in Kjeldahl's method. Two NH₃ "
      "neutralise one H₂SO₄.",
      ["n(N₂) = 56/22400 = 0.0025 mol → n(N) = 0.0050 mol", "n(NH₃) = 0.0050 mol",
       "n(H₂SO₄) = 0.0050/2 = 0.0025 mol", "V = 0.0025/0.10 L = 25 mL"],
      why_others_wrong="50 mL treats H₂SO₄ as monobasic; 12.5 mL takes one N atom per N₂ molecule; 250 mL "
                       "divides 0.0025 mol by 0.010 M instead of 0.10 M (a slip of one decimal place).",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of nitrogen", seconds=90),

    Q(T_PU, "Quantitative analysis and formulae", "Advanced", "multi_statement",
      *ms("Which of the following statements about the quantitative analysis of organic compounds are correct?",
          [("In the Carius method, the halogen of the compound is finally weighed as a silver halide.", True),
           ("Kjeldahl's method is suitable for estimating nitrogen in azo compounds.", False),
           ("In the estimation of sulphur, the sulphuric acid formed is precipitated as barium sulphate.", True),
           ("In the estimation of carbon and hydrogen, the carbon dioxide formed is absorbed in concentrated "
            "potassium hydroxide solution.", True),
           ("The percentage of oxygen is usually found by direct weighing of the oxygen set free from the "
            "compound.", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "c", "d", "e"]], "C"),
      "Methods of quantitative elemental analysis",
      "Halogen is weighed as AgX (Carius) and sulphur as BaSO₄. CO₂ is absorbed in KOH and water in anhydrous CaCl₂. "
      "Kjeldahl's method fails for nitro and azo compounds and for nitrogen in a ring (e.g. pyridine), because their "
      "nitrogen is not converted into ammonium sulphate. Oxygen is usually estimated by difference.",
      ["(a) true", "(b) false: azo nitrogen is not converted to (NH₄)₂SO₄", "(c) true", "(d) true",
       "(e) false: %O = 100 − sum of the other percentages"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=70),
]
