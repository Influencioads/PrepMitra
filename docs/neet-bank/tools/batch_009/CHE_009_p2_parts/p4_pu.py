
# ================================================================ Purification and Characterisation (2162-2165)
# 2163: acetone-like sample: 0.29 g -> 0.66 g CO2, 0.27 g H2O; O by difference
mC = F(66, 100) * 12 / 44
mH = F(27, 100) * 2 / 18
mO = F(29, 100) - mC - mH
assert (mC, mH) == (F(18, 100), F(3, 100))
v_2163 = pct(mO / F(29, 100))
assert v_2163 == "27.6%" and pct(mC / F(29, 100)) == "62.1%"
assert pct((F(29, 100) - mC) / F(29, 100)) == "37.9%"                                   # H forgotten
assert pct((F(29, 100) - mC - F(27, 100) / 18) / F(29, 100)) == "32.8%"                 # H2O/18 slip
# 2165: C2H4Br2 from Carius + combustion + vapour density
s = F(188, 1000)
nBr = F(376, 1000) / 188
nC = F(88, 1000) / 44
nH = 2 * F(36, 1000) / 18
assert (nBr, nC, nH) == (F(2, 1000), F(2, 1000), F(4, 1000))
assert nBr * 80 + nC * 12 + nH * 1 == s                                                   # nothing else present
mn = min(nC, nH, nBr)
emp = (nC / mn, nH / mn, nBr / mn)
assert emp == (1, 2, 1)                                                                  # CH2Br
emp_mass = 12 + 2 + 80
k = 2 * 94 // emp_mass
assert emp_mass == 94 and k == 2
v_2165 = "C₂H₄Br₂"

QUESTIONS += [
    Q(T_PU, "Qualitative analysis", "Basic", "direct",
      "The sodium fusion extract of an organic compound gives a violet colour on adding sodium nitroprusside. The "
      "element shown to be present is:",
      ["Nitrogen", "Sulphur", "Chlorine", "Phosphorus"], "B",
      "Lassaigne's test for sulphur",
      "Sulphur in the compound is converted into sodium sulphide during fusion. Sulphide ions react with sodium "
      "nitroprusside to give a violet colour.",
      ["Na + S → Na₂S during fusion", "S²⁻ + [Fe(CN)₅NO]²⁻ → violet complex", "Sulphur present"],
      why_others_wrong="Nitrogen is detected by the Prussian blue test, chlorine by a white precipitate with AgNO₃ "
                       "and phosphorus by a yellow colour with ammonium molybdate.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis: test for "
            f"sulphur", seconds=20),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "0.29 g of an organic compound containing only carbon, hydrogen and oxygen gives 0.66 g of CO₂ and 0.27 g of "
      "H₂O on complete combustion. The percentage of oxygen in the compound is (C = 12, H = 1, O = 16):",
      [v_2163, "62.1%", "37.9%", "32.8%"], "A", v_2163,
      "Percentage of oxygen by difference",
      "Oxygen is usually estimated by difference: the masses of carbon and hydrogen found from CO₂ and H₂O are "
      "subtracted from the mass of the sample.",
      ["Mass of C = 0.66 × 12/44 = 0.18 g", "Mass of H = 0.27 × 2/18 = 0.03 g",
       "Mass of O = 0.29 − 0.18 − 0.03 = 0.08 g", "% O = 0.08/0.29 × 100 ≈ 27.6%"],
      why_others_wrong="62.1% is the percentage of carbon; 37.9% leaves out the hydrogen; 32.8% takes the mass of "
                       "hydrogen as 0.27/18 instead of 0.27 × 2/18.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis: oxygen",
      seconds=60),

    Q(T_PU, "Qualitative analysis", "Intermediate", "statement_pair",
      *sp("In the silver nitrate test on the sodium fusion extract, a white precipitate soluble in ammonium hydroxide "
          "shows chlorine, whereas a yellowish precipitate sparingly soluble in ammonium hydroxide shows bromine.",
          True,
          "In thin layer chromatography, the spots of the components always travel farther from the base line than the "
          "solvent front.", False),
      "Test for halogens; Rf in chromatography",
      "AgCl is white and dissolves in NH₄OH; AgBr is pale yellow and only sparingly soluble; AgI is yellow and "
      "insoluble. In TLC every component moves behind the solvent, so the distance moved by a spot is less than that "
      "of the solvent front, and the retardation factor Rf is less than 1.",
      ["Statement I: true", "Statement II: false; spots lag behind the solvent front (Rf < 1)"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', test for halogens; chromatography",
      seconds=40),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "An organic compound contains carbon, hydrogen and bromine only. In a Carius determination, 0.188 g of it gives "
      "0.376 g of AgBr. On complete combustion, 0.188 g of it gives 0.088 g of CO₂ and 0.036 g of H₂O. Its vapour "
      "density is 94. The molecular formula of the compound is (C = 12, H = 1, Br = 80, Ag = 108):",
      ["CH₂Br", v_2165, "C₂H₅Br", "C₂H₂Br₂"], "B", v_2165,
      "Molecular formula from Carius and combustion data",
      "Find the moles of each element in the same mass of sample, take the simplest ratio for the empirical formula, "
      "and scale it with the molar mass (2 × vapour density).",
      ["AgBr = 188 g mol⁻¹: n(Br) = 0.376/188 = 0.002 mol (0.160 g)",
       "n(C) = 0.088/44 = 0.002 mol (0.024 g); n(H) = 2 × 0.036/18 = 0.004 mol (0.004 g)",
       "Check: 0.160 + 0.024 + 0.004 = 0.188 g, so no other element is present",
       "C : H : Br = 0.002 : 0.004 : 0.002 = 1 : 2 : 1 → empirical formula CH₂Br (94 g mol⁻¹)",
       "Molar mass = 2 × 94 = 188 g mol⁻¹ → n = 188/94 = 2 → C₂H₄Br₂"],
      why_others_wrong="CH₂Br is only the empirical formula; C₂H₅Br (109 g mol⁻¹) and C₂H₂Br₂ (186 g mol⁻¹) do not fit "
                       "the element ratio or the vapour density.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis: halogens "
            f"(Carius method)",
      seconds=120),
]
