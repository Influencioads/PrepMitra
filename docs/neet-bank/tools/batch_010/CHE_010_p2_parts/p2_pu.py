
# ================================================================ Purification and Characterisation (2389-2395)
# 2389: Kjeldahl works for urea, ethanamide, aniline; not for nitro, ring N (pyridine), azo
kj_2389 = {"urea": True, "ethanamide": True, "aniline": True, "nitrobenzene": False, "pyridine": False,
           "azobenzene": False}
v_2389 = str(sum(kj_2389.values()))
assert v_2389 == "3"
# 2391: Dumas on 0.30 g urea, CO(NH2)2: 1 mol urea -> 1 mol N2 -> 22400 mL at STP
M_urea = mm(C=1, H=4, N=2, O=1)
assert M_urea == 60
v_2391_n = F(30, 100) / M_urea * 22400
assert v_2391_n == 112
v_2391 = "112 mL"
# 2392: Carius on 0.239 g CHCl3 (119.5) -> 3 AgCl (143.5) per molecule
M_chcl3 = mm(C=1, H=1, Cl=3)
M_agcl = AM["Ag"] + AM["Cl"]
assert M_chcl3 == F(1195, 10) and M_agcl == F(1435, 10)
m_2392 = F(239, 1000) / M_chcl3 * 3 * M_agcl
assert m_2392 == F(861, 1000)
v_2392 = "0.861 g"
# 2394: Carius on 0.259 g CH2BrCl (129.5) -> AgCl + AgBr
M_cbc = mm(C=1, H=2, Br=1, Cl=1)
assert M_cbc == F(1295, 10)
n_2394 = F(259, 1000) / M_cbc
m_2394 = n_2394 * (M_agcl + AM["Ag"] + AM["Br"])
assert n_2394 == F(2, 1000) and m_2394 == F(663, 1000)
v_2394 = "0.663 g"

QUESTIONS += [
    N(T_PU, "Quantitative analysis and formulae", "Basic",
      "Kjeldahl's method is to be used to estimate nitrogen. For how many of the following compounds is the method "
      "applicable?\nUrea, ethanamide (CH₃CONH₂), aniline, nitrobenzene, pyridine, azobenzene (C₆H₅–N=N–C₆H₅)",
      ["2", v_2389, "4", "6"], "B", v_2389,
      "Limitation of Kjeldahl's method",
      "In Kjeldahl's method the nitrogen is converted into ammonium sulphate by heating with concentrated H₂SO₄. "
      "The method is not applicable to compounds containing nitrogen in nitro and azo groups or in a ring (such as "
      "pyridine), because their nitrogen does not change to ammonium sulphate under these conditions.",
      ["Applicable: urea, ethanamide, aniline (3)", "Not applicable: nitrobenzene (nitro), pyridine (ring N), "
       "azobenzene (azo)"],
      why_others_wrong="2 usually leaves out aniline, whose –NH₂ nitrogen is converted normally; 4 or 6 forget the "
                       "NCERT exclusions for nitro, azo and ring nitrogen.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of nitrogen: "
            "Kjeldahl's method", seconds=40),

    Q(T_PU, "Purification methods", "Basic", "direct",
      "In differential extraction, if the organic compound is only slightly soluble in the organic solvent, a very "
      "large quantity of solvent would be needed to extract even a small quantity of the compound. The technique "
      "used in such cases, in which the same solvent is used repeatedly for extraction, is:",
      ["Simple distillation", "Steam distillation", "Sublimation", "Continuous extraction"], "D",
      "Differential extraction",
      "NCERT: when the compound is less soluble in the organic solvent, the technique of continuous extraction is "
      "employed, in which the same solvent is repeatedly used for extraction of the compound.",
      ["Low solubility in the organic solvent → large volume needed",
       "Solution: re-use the same solvent repeatedly → continuous extraction"],
      why_others_wrong="Simple and steam distillation separate liquids by volatility; sublimation separates a "
                       "sublimable solid from a non-sublimable one. None of them reuses an extracting solvent.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', differential extraction",
      seconds=30),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "If 0.30 g of urea, CO(NH₂)₂, were analysed by Dumas' method, the volume of nitrogen gas collected, corrected "
      "to STP, would be (C = 12, H = 1, N = 14, O = 16; molar volume at STP = 22400 mL):",
      ["56 mL", v_2391, "224 mL", "448 mL"], "B", v_2391,
      "Dumas' method: all nitrogen is collected as N₂",
      "In Dumas' method the nitrogen of the compound is set free as N₂ gas. One molecule of urea has two nitrogen "
      "atoms, which give one molecule of N₂.",
      ["Urea: 0.30 / 60 = 0.0050 mol", "N₂ formed = 0.0050 mol (2 N per urea → 1 N₂)",
       "Volume = 0.0050 × 22400 = 112 mL"],
      why_others_wrong="56 mL treats urea as having one nitrogen atom; 224 mL counts one N₂ per nitrogen atom; "
                       "448 mL also doubles the moles of urea.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of nitrogen: Dumas "
            "method", seconds=50),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "0.239 g of chloroform, CHCl₃, is analysed by the Carius method. Assuming that all its chlorine is converted "
      "into silver chloride, the mass of AgCl obtained is (C = 12, H = 1, Cl = 35.5, Ag = 108):",
      ["0.287 g", "0.574 g", v_2392, "1.148 g"], "C", v_2392,
      "Carius method: halogen → silver halide",
      "In the Carius method the halogen of the compound is converted into silver halide. Each molecule of CHCl₃ "
      "gives three molecules of AgCl.",
      ["CHCl₃: 0.239 / 119.5 = 0.0020 mol", "AgCl: 3 × 0.0020 = 0.0060 mol",
       "Mass = 0.0060 × 143.5 = 0.861 g"],
      why_others_wrong="0.287 g counts one chlorine atom per molecule and 0.574 g two; 1.148 g counts four, as for "
                       "CCl₄.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of halogens: Carius "
            "method", seconds=50),

    Q(T_PU, "Quantitative analysis and formulae", "Intermediate", "match_list",
      *ml("Match the method of quantitative estimation in List-I with the quantity that is finally measured in "
          "List-II.",
          ["Dumas' method for nitrogen", "Kjeldahl's method for nitrogen", "Carius method for halogens",
           "Carius method for sulphur"],
          ["Volume of nitrogen gas collected over aqueous KOH", "Mass of barium sulphate",
           "Amount of ammonia absorbed in a known volume of standard acid", "Mass of silver halide"],
          "I III IV II", ["III I IV II", "I III II IV", "IV III I II"], "A"),
      "Principles of quantitative estimation",
      "Dumas: nitrogen is collected as N₂ gas over KOH solution. Kjeldahl: nitrogen is converted to ammonium "
      "sulphate, the ammonia set free by alkali is absorbed in standard acid, and the unused acid is titrated. "
      "Carius: halogen is weighed as silver halide; sulphur is oxidised to sulphuric acid and weighed as barium "
      "sulphate.",
      ["Dumas → N₂ volume", "Kjeldahl → NH₃ in standard acid", "Carius (X) → AgX mass", "Carius (S) → BaSO₄ mass"],
      why_others_wrong="Codes that swap Dumas and Kjeldahl confuse gas collection with acid absorption; codes that "
                       "swap the two Carius estimations give sulphur as the silver salt.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=45),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "0.259 g of bromochloromethane, CH₂BrCl, is heated with fuming nitric acid and silver nitrate in a Carius "
      "tube. Assuming complete conversion of both halogens, the total mass of the silver halide precipitate is "
      "(C = 12, H = 1, Cl = 35.5, Br = 80, Ag = 108):",
      ["0.574 g", v_2394, "0.752 g", "1.326 g"], "B", v_2394,
      "Carius method with two halogens",
      "Each molecule of CH₂BrCl gives one AgCl and one AgBr. The precipitate is a mixture of the two silver halides.",
      ["CH₂BrCl: 0.259 / 129.5 = 0.0020 mol", "AgCl: 0.0020 × 143.5 = 0.287 g",
       "AgBr: 0.0020 × 188 = 0.376 g", "Total = 0.663 g"],
      why_others_wrong="0.574 g treats both halogens as chlorine and 0.752 g both as bromine; 1.326 g doubles the "
                       "moles of compound.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of halogens: Carius "
            "method", seconds=80),

    Q(T_PU, "Purification methods", "Advanced", "assertion_reason",
      *ar("In fractional distillation, the vapour that reaches the top of the fractionating column is richer in the "
          "more volatile component.", True,
          "The fractionating column provides many surfaces for heat exchange between the ascending vapours and the "
          "descending condensed liquid, so at each stage part of the less volatile component condenses and returns "
          "towards the flask.", True, explains=True),
      "Fractional distillation",
      "NCERT: the fractionating column provides many surfaces for heat exchange between the ascending vapours and "
      "the descending condensed liquid. Some of the condensing liquid takes heat from the rising vapours and "
      "vaporises, so the vapours become richer in the low-boiling component. Each such condensation and "
      "vaporisation unit is a theoretical plate. R is the reason for A.",
      ["Repeated condensation and vaporisation along the column",
       "Less volatile component condenses and runs back; vapour at the top is enriched in the more volatile one"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fractional distillation",
      seconds=50),
]
