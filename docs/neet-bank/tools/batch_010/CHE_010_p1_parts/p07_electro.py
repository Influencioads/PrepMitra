

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7 = f"{C12}, 'Electrochemistry'"
REF7R = f"{C11}, 'Redox Reactions'"

e_m = 0.0 - 0.44
assert close(e_m, -0.44) and close(e_m / 2, -0.22)
add("Electrode potential and cells", B, "numerical",
    "The standard emf of the cell M(s) | M²⁺(aq, 1 M) || H⁺(aq, 1 M) | H₂(g, 1 bar) | Pt(s) is +0.44 V at "
    "298 K, the metal electrode M being the anode. The standard electrode (reduction) potential of the M²⁺/M "
    "couple is:",
    Opts("C", "−0.44 V", ["+0.44 V", "−0.22 V", "+0.22 V"]),
    "E°cell = E°(cathode) − E°(anode), with the standard hydrogen electrode taken as 0 V",
    "The hydrogen electrode on the right is the cathode with E° = 0. Rearranging, E°(anode) = E°(cathode) − "
    "E°cell.",
    ["E°cell = E°(H⁺/H₂) − E°(M²⁺/M)", "0.44 = 0 − E°(M²⁺/M)", "E°(M²⁺/M) = −0.44 V"],
    why="+0.44 V forgets that the anode couple has the LOWER reduction potential. −0.22 V and +0.22 V divide by "
        "the number of electrons, but E° does not depend on n.",
    ncert=f"{REF7}, measurement of electrode potential (standard hydrogen electrode)", seconds=35, checked=True)

lam = 6.0e-3 * 1000 / 0.050
assert close(lam, 120) and close(6.0e-3 / 0.050, 0.12) and close(6.0e-3 * 1000 * 0.050, 0.30) \
    and close(6.0e-3 * 0.050, 3.0e-4)
add("Conductance and Kohlrausch's law", B, "numerical",
    "The conductivity of a 0.050 mol L⁻¹ solution of an electrolyte is 6.0 × 10⁻³ S cm⁻¹. Its molar "
    "conductivity, in S cm² mol⁻¹, is:",
    Opts("D", "120", ["0.12", "0.30", "3.0 × 10⁻⁴"]),
    "Λm = κ × 1000 / c (κ in S cm⁻¹, c in mol L⁻¹, Λm in S cm² mol⁻¹)",
    "Molar conductivity is conductivity divided by molar concentration; the factor 1000 converts litres into "
    "cm³.",
    ["Λm = (6.0 × 10⁻³ S cm⁻¹ × 1000 cm³ L⁻¹) / 0.050 mol L⁻¹", "Λm = 120 S cm² mol⁻¹"],
    why="0.12 forgets the factor 1000 cm³ L⁻¹. 0.30 multiplies by the concentration instead of dividing. "
        "3.0 × 10⁻⁴ multiplies κ by c and omits the factor 1000.",
    ncert=f"{REF7}, conductance of electrolytic solutions (molar conductivity)", seconds=35, checked=True)

add("Oxidation number and balancing", B, "direct",
    "Which of the following species can act ONLY as a reducing agent in redox reactions?",
    Opts("A", "S²⁻", ["SO₂", "H₂O₂", "NO₂⁻"]),
    "An element in its lowest possible oxidation state can only be oxidised",
    "A species acts only as a reducing agent when its key element is already in its lowest oxidation state and "
    "can only increase it. Sulphur is −2 in S²⁻, its lowest state. In SO₂ (S = +4), H₂O₂ (O = −1) and NO₂⁻ "
    "(N = +3) the element is in an intermediate state, so these can be oxidised or reduced.",
    ["S²⁻: S = −2 (lowest) → only reducing ✓", "SO₂: S = +4 → both", "H₂O₂: O = −1 → both",
     "NO₂⁻: N = +3 → both"],
    why="SO₂, H₂O₂ and NO₂⁻ each contain an element in an intermediate oxidation state and can act as either an "
        "oxidising or a reducing agent.",
    ncert=f"{REF7R}, oxidation number; redox reactions", seconds=35)

add("Oxidation number and balancing", B, "match_list",
    lists("Match List-I (term) with List-II (its meaning in terms of electron transfer).",
          ["Oxidation", "Oxidising agent", "Reducing agent", "Disproportionation"],
          ["A species that donates electrons and is itself oxidised",
           "The same element in one species is simultaneously oxidised and reduced",
           "Loss of electrons by a species",
           "A species that accepts electrons and is itself reduced"]),
    match("B", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "Electronic concept of oxidation and reduction",
    "Oxidation is loss of electrons and reduction is gain. An oxidising agent takes electrons (and is reduced); "
    "a reducing agent gives electrons (and is oxidised). In disproportionation one element is both oxidised and "
    "reduced.",
    ["A: loss of electrons → III", "B: electron acceptor, itself reduced → IV",
     "C: electron donor, itself oxidised → I", "D: same element oxidised and reduced → II"],
    why="B-I/C-IV swaps the oxidising and reducing agents. A-IV/B-III confuses oxidation with an oxidising "
        "agent. C-II/D-I swaps reducing agent and disproportionation.",
    ncert=f"{REF7R}, redox reactions in terms of electron transfer", seconds=40)

e_disp = 0.52 - 0.15
assert close(e_disp, 0.37) and close(0.52 + 0.15, 0.67)
add("Electrode potential and cells", I, "numerical",
    "Given the standard reduction potentials E°(Cu²⁺/Cu⁺) = +0.15 V and E°(Cu⁺/Cu) = +0.52 V at 298 K, the "
    "standard emf for the reaction 2Cu⁺(aq) → Cu²⁺(aq) + Cu(s), and the conclusion about Cu⁺ in aqueous "
    "solution, are:",
    Opts("A", "+0.37 V; Cu⁺ disproportionates",
         ["−0.37 V; Cu⁺ is stable", "+0.67 V; Cu⁺ disproportionates", "+0.37 V; Cu⁺ is stable"]),
    "Feasibility of a disproportionation from standard potentials",
    "Split the reaction into a reduction (Cu⁺ → Cu, the cathode) and an oxidation (Cu⁺ → Cu²⁺, the anode). "
    "E° = E°(cathode) − E°(anode). A positive E° means ΔG° < 0, so the reaction is spontaneous.",
    ["Cathode: Cu⁺ + e⁻ → Cu, E° = +0.52 V", "Anode: Cu⁺ → Cu²⁺ + e⁻ (couple Cu²⁺/Cu⁺, E° = +0.15 V)",
     "E° = 0.52 − 0.15 = +0.37 V > 0 → ΔG° < 0 → Cu⁺ disproportionates"],
    why="−0.37 V subtracts the potentials the wrong way round. +0.67 V adds them. '+0.37 V; Cu⁺ is stable' gets "
        "the value right but misreads a positive E° as non-spontaneous.",
    ncert=f"{REF7}, electrochemical cells and Gibbs energy of reaction", seconds=60, checked=True)

g_star = 100 * 129 * 0.10 / 1000
kappa2 = 141 * 0.010 / 1000
r2 = g_star / kappa2
assert close(g_star, 1.29) and close(r2, 915, 0.002) and close(100 * 10 * 141 / 129, 1093, 0.002)
add("Conductance and Kohlrausch's law", I, "numerical",
    "A conductivity cell filled with 0.10 M KCl solution (molar conductivity 129 S cm² mol⁻¹) shows a "
    "resistance of 100 Ω. The same cell is then filled with 0.010 M KCl solution, whose molar conductivity is "
    "141 S cm² mol⁻¹. The resistance it now shows is about:",
    Opts("C", "915 Ω", ["1000 Ω", "1093 Ω", "91.5 Ω"]),
    "Cell constant G* = R × κ is fixed for a cell; κ = Λm × c / 1000",
    "Find the cell constant from the first measurement, then the conductivity of the dilute solution, and "
    "R = G*/κ.",
    ["κ₁ = 129 × 0.10/1000 = 0.0129 S cm⁻¹; G* = 100 × 0.0129 = 1.29 cm⁻¹",
     "κ₂ = 141 × 0.010/1000 = 1.41 × 10⁻³ S cm⁻¹", "R₂ = 1.29 / 1.41 × 10⁻³ ≈ 915 Ω"],
    why="1000 Ω assumes the molar conductivity stays the same on dilution, so that R grows tenfold. 1093 Ω "
        "uses the ratio of molar conductivities upside down. 91.5 Ω slips a power of ten.",
    ncert=f"{REF7}, measurement of the conductivity; variation of molar conductivity with concentration",
    seconds=90, checked=True)

add("Electrode potential and cells", I, "assertion_reason",
    ar("In a galvanic cell, the anode is the negative electrode.",
       "The salt bridge of a galvanic cell usually contains a solution of an inert electrolyte such as KCl set "
       "in agar–agar gel."),
    AR_, "Polarity of electrodes; the salt bridge",
    "A is true: oxidation at the anode releases electrons into it, so the anode carries a negative charge "
    "relative to the cathode. R is also true, but the composition of the salt bridge has nothing to do with "
    "which electrode is negative; the salt bridge only completes the circuit and keeps the solutions neutral.",
    ["A: oxidation at the anode leaves electrons there → negative → true",
     "R: KCl/NH₄NO₃ in agar gel → true", "Salt-bridge contents do not decide polarity → option B"],
    answer="B",
    why="Option A would need R to account for the anode being negative; it does not. Both statements are true, "
        "so C and D are wrong.",
    ncert=f"{REF7}, electrochemical cells; galvanic cells", seconds=35)

add("Nernst equation and Gibbs energy", I, "statement_pair",
    sp("At 298 K, the reduction potential of a Cu²⁺/Cu electrode becomes more positive when the concentration "
       "of Cu²⁺ ions in its solution is increased.",
       "The standard electrode potential of the Cu²⁺/Cu electrode increases when the concentration of Cu²⁺ ions "
       "in its solution is increased."),
    SP_, "Electrode potential versus standard electrode potential",
    "Nernst: E = E° − (0.059/2) log(1/[Cu²⁺]) = E° + 0.0295 log[Cu²⁺]. Raising [Cu²⁺] raises E. But E° is "
    "defined for unit concentration and is a fixed value at a given temperature; it does not change with the "
    "concentration actually used.",
    ["I: E = E° + 0.0295 log[Cu²⁺] → rises with [Cu²⁺] → true",
     "II: E° refers to 1 M by definition → does not change → false"],
    answer="C",
    why="Statement II confuses the electrode potential E with the standard electrode potential E°.",
    ncert=f"{REF7}, Nernst equation", seconds=40)

truth_hno3 = {"a": True, "b": True, "c": True, "d": False, "e": False}
assert 3 * 2 == 2 * 3 and 8 - 2 == 6
add("Oxidation number and balancing", I, "multi_statement",
    ms("For the balanced reaction 3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO + 4H₂O, which of the following statements are "
       "correct?",
       ["Copper is oxidised from 0 to +2.",
        "Only two of the eight HNO₃ molecules are reduced; the other six supply the nitrate ions of Cu(NO₃)₂.",
        "The oxidation number of the nitrogen that is reduced changes from +5 to +2.",
        "A total of eight electrons is transferred in the reaction as written.",
        "HNO₃ acts as the reducing agent."]),
    multi("D", truth_hno3, ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"]),
    "Oxidation numbers, electron count and the roles of the reactants",
    "Cu: 0 → +2 (oxidised). N in NO: +5 → +2 (reduced). Electrons lost by 3 Cu = 3 × 2 = 6 = electrons gained "
    "by 2 N (2 × 3), so only 2 HNO₃ are reduced; 6 NO₃⁻ stay unchanged in Cu(NO₃)₂.",
    ["(a) ✓", "(b) 2 NO formed → 2 HNO₃ reduced; 6 remain as NO₃⁻ ✓", "(c) +5 → +2 ✓",
     "(d) electrons transferred = 6, not 8 ✗", "(e) HNO₃ is the oxidising agent ✗"],
    why="(d) counts one electron per HNO₃ molecule, and (e) swaps the roles of the reagents; options containing "
        "either are wrong.",
    ncert=f"{REF7R}, oxidation number; balancing of redox reactions", seconds=90, checked=True)

h_plus = math.sqrt(1.0e-6 * 0.010)
e_h = -0.059 * (-math.log10(h_plus))
assert close(h_plus, 1.0e-4) and close(e_h, -0.236)
add("Nernst equation and Gibbs energy", A, "numerical",
    "A hydrogen electrode (H₂ gas at 1 bar, platinum) is dipped in a 0.010 M solution of a weak monobasic acid "
    "HA (Kₐ = 1.0 × 10⁻⁶) at 298 K. Taking [H⁺] ≈ √(Kₐc), the reduction potential of this electrode is "
    "(2.303RT/F = 0.059 V):",
    Opts("B", "−0.236 V", ["−0.118 V", "−0.354 V", "+0.236 V"]),
    "pH of a weak acid, then the Nernst equation for the hydrogen electrode: E = −0.059 pH (p(H₂) = 1 bar)",
    "Find [H⁺] of the weak acid, convert to pH, and use E = −(0.059/1) log(1/[H⁺]) = −0.059 pH.",
    ["[H⁺] = √(1.0 × 10⁻⁶ × 0.010) = 1.0 × 10⁻⁴ M → pH = 4", "E = −0.059 × 4 = −0.236 V"],
    why="−0.118 V takes [H⁺] equal to the acid concentration (pH 2), as for a strong acid. −0.354 V takes "
        "[H⁺] = Kₐ (pH 6). +0.236 V has the wrong sign; a lower [H⁺] than 1 M makes E negative.",
    ncert=f"{REF7}, Nernst equation (hydrogen electrode)", seconds=80, checked=True)

add("Nernst equation and Gibbs energy", A, "match_list",
    lists("Match List-I (electrode, at 298 K) with List-II (its reduction potential from the Nernst equation, "
          "2.303RT/F = 0.059 V).",
          ["Pt | H₂(g, 1 bar) | H⁺(aq)", "Cu²⁺(aq) | Cu(s)", "Ag⁺(aq) | Ag(s)", "Pt | Fe³⁺(aq), Fe²⁺(aq)"],
          ["E = E° − 0.059 log(1/[Ag⁺])", "E = −0.059 pH",
           "E = E° − 0.059 log([Fe²⁺]/[Fe³⁺])", "E = E° − (0.059/2) log(1/[Cu²⁺])"]),
    match("D", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "Nernst equation for different types of electrode",
    "For Mⁿ⁺ + ne⁻ → M, E = E° − (0.059/n) log(1/[Mⁿ⁺]) (the pure metal has unit activity). For the hydrogen "
    "electrode E° = 0 and p(H₂) = 1 bar, so E = −0.059 pH. For the redox couple Fe³⁺ + e⁻ → Fe²⁺, "
    "E = E° − 0.059 log([Fe²⁺]/[Fe³⁺]).",
    ["A: H⁺ + e⁻ → ½H₂ → E = −0.059 pH → II", "B: n = 2 → (0.059/2) log(1/[Cu²⁺]) → IV",
     "C: n = 1 → 0.059 log(1/[Ag⁺]) → I", "D: Fe³⁺/Fe²⁺, n = 1 → III"],
    why="B-I/C-IV swaps the one- and two-electron metal electrodes. A-IV/B-II gives the copper electrode the "
        "pH expression. C-III/D-I swaps the silver and iron electrodes.",
    ncert=f"{REF7}, Nernst equation", seconds=80)

add("Nernst equation and Gibbs energy", A, "direct",
    "At 298 K, the reduction potential of which of the following electrodes does NOT depend on the pH of the "
    "solution (all other concentrations being fixed)?",
    Opts("A", "Cu²⁺(aq) | Cu(s)",
         ["MnO₄⁻, Mn²⁺ | Pt in acid (MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O)",
          "Cr₂O₇²⁻, Cr³⁺ | Pt in acid (Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O)",
          "Pt | H₂(g, 1 bar) | H⁺(aq)"]),
    "Which electrode reactions involve H⁺ ions",
    "The Nernst equation contains [H⁺] only if H⁺ appears in the electrode reaction. Cu²⁺ + 2e⁻ → Cu involves "
    "no H⁺, so its potential is independent of pH. The other three reactions consume H⁺.",
    ["Cu²⁺/Cu: no H⁺ in the half-reaction → pH-independent ✓", "MnO₄⁻/Mn²⁺: [H⁺]⁸ in Q",
     "Cr₂O₇²⁻/Cr³⁺: [H⁺]¹⁴ in Q", "H⁺/H₂: E = −0.059 pH"],
    why="The permanganate, dichromate and hydrogen electrodes all have H⁺ in their half-reactions, so their "
        "potentials change with pH.",
    ncert=f"{REF7}, Nernst equation", seconds=45)

add("Electrode potential and cells", A, "assertion_reason",
    ar("In a galvanic cell made of two half-cells, the electrode of the couple with the lower standard reduction "
       "potential acts as the anode.",
       "E°cell = E°(anode) − E°(cathode), where both are standard reduction potentials."),
    AR_, "Choosing the anode; calculating E°cell",
    "A is true: the couple with the lower reduction potential has the greater tendency to be oxidised, so it "
    "is the anode. R is false: the correct relation is E°cell = E°(cathode) − E°(anode) (E°right − E°left), "
    "which is positive for a working cell.",
    ["A: lower E° → oxidation → anode → true", "R: sign reversed; correct is E°(cathode) − E°(anode) → false"],
    answer="C",
    why="With R as written, every working galvanic cell would have a negative standard emf, which contradicts "
        "E°cell > 0 for a spontaneous cell reaction.",
    ncert=f"{REF7}, electrode potential; galvanic cells", seconds=40)
