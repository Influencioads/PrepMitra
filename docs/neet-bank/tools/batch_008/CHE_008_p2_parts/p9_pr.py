
# ================================================================ Principles Related to Practical Chemistry (1991-2000)
# 1991: % Fe in Mohr's salt FeSO4.(NH4)2SO4.6H2O (M 392)
mohr = mm(Fe=1, S=2, O=8, N=2, H=8) + 6 * mm(H=2, O=1)
assert mohr == 392
v_1991 = pct(F(56, mohr))
assert v_1991 == "14.3%"
# 1994: KNO3 dissolution: 10.1 g (0.1 mol) in water, solution 100 g, c 4.2 J/g/K, temperature falls 8.0 K
q_1994 = 100 * F(42, 10) * 8
n_1994 = F(101, 10) / mm(K=1, N=1, O=3)
assert n_1994 == F(1, 10)
v_1994 = f"+{float(q_1994 / n_1994 / 1000):.1f} kJ mol⁻¹"
assert v_1994 == "+33.6 kJ mol⁻¹" and f"{float(F(1101, 10) * F(42, 10) * 8 / n_1994 / 1000):.1f}" == "37.0"
# 1995: dissociation enthalpy of CH3COOH = dH_neut(weak) - dH_neut(strong)
v_1995 = f"+{-55.8 - (-57.1):.1f} kJ mol⁻¹"
assert v_1995 == "+1.3 kJ mol⁻¹"
# 1998: 50 mL 0.5 M H2SO4 + 50 mL 1.0 M NaOH -> 0.05 mol water; 100 g solution
n_h = F(50, 1000) * F(5, 10) * 2
n_oh = F(50, 1000) * 1
assert n_h == n_oh == F(5, 100)
dT = n_h * F(571, 10) * 1000 / (100 * F(42, 10))
v_1998 = f"{float(dT):.2f} K"
assert v_1998 == "6.80 K"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O, is prepared in the laboratory and used as a primary standard. The "
      "percentage of iron by mass in Mohr's salt is (Fe = 56, S = 32, O = 16, N = 14, H = 1):",
      ["36.8%", "20.1%", "14.3%", "28.6%"], "C", v_1991,
      "Percentage composition of a double salt",
      "Mohr's salt has one iron atom per formula unit and a molar mass of 392 g mol⁻¹.",
      ["M = 152 (FeSO₄) + 132 ((NH₄)₂SO₄) + 108 (6H₂O) = 392", "%Fe = 56/392 × 100 = 14.3%"],
      why_others_wrong="36.8% is iron in anhydrous FeSO₄; 20.1% is iron in FeSO₄·7H₂O; 28.6% counts two iron atoms.",
      ncert=f"{LAB}, preparation of double salts: ferrous ammonium sulphate", seconds=40),

    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In the flame test, a salt gives a lilac (pale violet) colour to the flame, best seen through blue (cobalt) "
      "glass. The cation present is:",
      ["Na⁺", "K⁺", "Ca²⁺", "Sr²⁺"], "B",
      "Flame colours of cations",
      "Potassium salts give a lilac flame; the blue glass absorbs any yellow sodium light that would mask it.",
      ["Lilac through blue glass → K⁺"],
      why_others_wrong="Na⁺ gives a persistent golden-yellow flame, Ca²⁺ brick red and Sr²⁺ crimson red.",
      ncert=f"{LAB}, qualitative analysis: flame test", seconds=20),

    Q(T_PR, "Titrimetric analysis", "Basic", "match_list",
      *ml("Match the titration or experiment in List-I with the indicator used to detect its end point in List-II.",
          ["Oxalic acid against sodium hydroxide", "Sodium carbonate against hydrochloric acid",
           "Oxalic acid against acidified potassium permanganate",
           "Iodine clock reaction of H₂O₂ with iodide (with a little thiosulphate)"],
          ["KMnO₄ itself (self-indicator)", "Starch solution", "Phenolphthalein", "Methyl orange"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A"),
      "Choice of indicator",
      "A weak acid–strong base titration needs phenolphthalein (end point in the alkaline range); the carbonate–strong "
      "acid titration uses methyl orange (end point in the acidic range); permanganate is its own indicator (first "
      "permanent pink); free iodine is detected with starch (blue).",
      ["A → phenolphthalein (III)", "B → methyl orange (IV)", "C → self-indicator (I)", "D → starch (II)"],
      why_others_wrong="The other codes swap phenolphthalein and methyl orange, or the starch and permanganate entries.",
      ncert=f"{LAB}, titrimetric analysis and chemical kinetics experiments", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "10.1 g of potassium nitrate (molar mass 101 g mol⁻¹) is dissolved in water in a calorimeter, and the "
      "temperature falls by 8.0 K. Take the mass of the solution as 100 g and its specific heat as 4.2 J g⁻¹ K⁻¹, and "
      "ignore the heat capacity of the calorimeter. The enthalpy of solution of KNO₃ is:",
      ["−33.6 kJ mol⁻¹", "+3.4 kJ mol⁻¹", "+37.0 kJ mol⁻¹", "+33.6 kJ mol⁻¹"], "D", v_1994,
      "Enthalpy of solution from a calorimetric experiment",
      "A fall in temperature means heat is absorbed from the surroundings: the dissolution is endothermic. "
      "q = m c ΔT, divided by the moles of salt.",
      ["q = 100 × 4.2 × 8.0 = 3360 J absorbed", "n(KNO₃) = 10.1/101 = 0.10 mol",
       "ΔsolH = +3360/0.10 = +33 600 J mol⁻¹ = +33.6 kJ mol⁻¹"],
      why_others_wrong="−33.6 kJ mol⁻¹ has the wrong sign for a temperature fall; +3.4 kJ mol⁻¹ does not divide by "
                       "the number of moles correctly; +37.0 kJ mol⁻¹ uses 110.1 g (water + salt) instead of the "
                       "100 g stated.",
      ncert=f"{LAB}, thermochemistry: enthalpy of dissolution", seconds=60),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "In two calorimetric experiments, the enthalpy of neutralisation of hydrochloric acid by NaOH is found to be "
      "−57.1 kJ mol⁻¹ and that of ethanoic acid by NaOH −55.8 kJ mol⁻¹. On this basis, the enthalpy of ionisation "
      "(dissociation) of ethanoic acid is:",
      ["−1.3 kJ mol⁻¹", "+1.3 kJ mol⁻¹", "+112.9 kJ mol⁻¹", "−55.8 kJ mol⁻¹"], "B", v_1995,
      "Neutralisation of a weak acid includes its ionisation",
      "For a strong acid only H⁺ + OH⁻ → H₂O occurs. For ethanoic acid, some of the heat released is used to ionise "
      "the weak acid, so less heat is given out. ΔH(ionisation) = ΔH(neut, weak) − ΔH(neut, strong).",
      ["ΔH(ion) = (−55.8) − (−57.1)", "= +1.3 kJ mol⁻¹ (endothermic)"],
      why_others_wrong="−1.3 kJ mol⁻¹ subtracts in the wrong order; +112.9 kJ mol⁻¹ adds the two magnitudes; −55.8 "
                       "kJ mol⁻¹ is simply the enthalpy of neutralisation of ethanoic acid.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation of strong and weak acids", seconds=45),

    Q(T_PR, "Detection of elements and functional groups", "Intermediate", "assertion_reason",
      *ar("Carboxylic acids give brisk effervescence with aqueous sodium hydrogencarbonate, but phenols generally "
          "do not.", True,
          "Carboxylic acids are stronger acids than carbonic acid, whereas phenol is a weaker acid than carbonic "
          "acid.", True, explains=True),
      "Sodium hydrogencarbonate test for the carboxyl group",
      "An acid displaces CO₂ from HCO₃⁻ only if it is stronger than carbonic acid. Carboxylic acids are, so CO₂ is "
      "evolved; phenol is weaker, so no effervescence occurs. R explains A.",
      ["RCOOH + NaHCO₃ → RCOONa + H₂O + CO₂↑", "Phenol (weaker than H₂CO₃): no reaction"],
      ncert=f"{LAB}, tests for functional groups: carboxyl group", seconds=35),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the precipitate obtained in systematic salt analysis (List-I) with its colour (List-II).",
          ["Fe(OH)₃ (group III)", "Al(OH)₃ (group III)", "CuS (group II)", "MnS (group IV)"],
          ["Black", "Buff (flesh-coloured)", "Reddish-brown", "White, gelatinous"],
          "III IV I II", ["IV III I II", "III IV II I", "II IV I III"], "C"),
      "Colours of group precipitates",
      "Iron(III) hydroxide is reddish-brown and aluminium hydroxide white and gelatinous; copper(II) sulphide is "
      "black; manganese(II) sulphide is buff (flesh) coloured.",
      ["Fe(OH)₃ → III", "Al(OH)₃ → IV", "CuS → I", "MnS → II"],
      why_others_wrong="The other codes swap the two hydroxides, or the two sulphides.",
      ncert=f"{LAB}, systematic analysis of cations", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "50 mL of 0.50 M H₂SO₄ is mixed with 50 mL of 1.0 M NaOH in a calorimeter. Take the enthalpy of neutralisation "
      "as −57.1 kJ per mole of water formed, the mass of the solution as 100 g and its specific heat as "
      "4.2 J g⁻¹ K⁻¹, and ignore the heat capacity of the calorimeter. The rise in temperature is:",
      ["3.40 K", "6.80 K", "13.60 K", "0.68 K"], "B", v_1998,
      "Neutralisation of a dibasic acid",
      "H₂SO₄ is dibasic: 0.025 mol of acid supplies 0.050 mol H⁺, which exactly neutralises 0.050 mol OH⁻ to give "
      "0.050 mol water.",
      ["n(H⁺) = 2 × 0.050 × 0.50 = 0.050 mol; n(OH⁻) = 0.050 mol", "q = 0.050 × 57 100 = 2855 J",
       "ΔT = 2855 / (100 × 4.2) = 6.80 K"],
      why_others_wrong="3.40 K treats H₂SO₄ as monobasic (0.025 mol water); 13.60 K counts 0.10 mol water; 0.68 K "
                       "slips a factor of 10 in the heat capacity of the solution.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation", seconds=75),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "statement_pair",
      *sp("Zn²⁺ and Mn²⁺ are precipitated in group IV as their sulphides when H₂S is passed through the ammoniacal "
          "solution.", True,
          "Ni²⁺ and Co²⁺ are precipitated in group III as hydroxides by NH₄OH in the presence of NH₄Cl.", False),
      "Group III and group IV cations",
      "Group III (Fe³⁺, Al³⁺, Cr³⁺) is precipitated as hydroxides by NH₄OH/NH₄Cl. Ni²⁺, Co²⁺, Mn²⁺ and Zn²⁺ stay in "
      "solution and are precipitated in group IV as sulphides by H₂S in ammoniacal medium (NiS and CoS black, MnS "
      "buff, ZnS white). Statement I is true and Statement II false.",
      ["Group IV: Ni²⁺, Co²⁺, Mn²⁺, Zn²⁺ as sulphides", "Ni²⁺ and Co²⁺ are not group III → Statement II false"],
      ncert=f"{LAB}, systematic analysis of cations: groups III and IV", seconds=40),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about systematic analysis of cations are correct?",
          [("Group I cations are precipitated as chlorides by dilute HCl.", True),
           ("Lead chloride is appreciably soluble in water, so Pb²⁺ may also appear in group II.", True),
           ("Group V cations are precipitated as carbonates by ammonium carbonate in the presence of NH₄OH.", True),
           ("Mg²⁺ is precipitated in group V as magnesium carbonate.", False),
           ("The test for NH₄⁺ is performed on the original salt, because ammonium salts are added as reagents during "
            "the analysis.", True)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "c", "d"]], "A"),
      "Principles of group separation",
      "Pb²⁺ is precipitated incompletely as PbCl₂ in group I and the rest as PbS in group II. Group V (Ba²⁺, Sr²⁺, "
      "Ca²⁺) comes down as carbonates; Mg²⁺ is not precipitated in the presence of NH₄Cl and is tested in group VI. "
      "Because NH₄Cl, NH₄OH and (NH₄)₂CO₃ are added during the scheme, NH₄⁺ (zero group) must be tested in the "
      "original salt.",
      ["(a) true", "(b) true", "(c) true", "(d) false: Mg²⁺ is group VI", "(e) true"],
      ncert=f"{LAB}, systematic qualitative analysis of cations", seconds=55),
]
