
# ================================================================ Coordination Compounds (1874-1888)
# 1875: [CoF6]3-: Co3+ = 3d6, weak field -> t2g4 eg2 -> 4 unpaired
v_1875 = f"{bm(4):.2f} BM"
assert v_1875 == "4.90 BM" and f"{bm(3):.2f}" == "3.87" and f"{bm(5):.2f}" == "5.92"
# 1878: chiral species among six (True = chiral)
chiral = {"cis-[CrCl2(ox)2]3-": True, "trans-[CrCl2(ox)2]3-": False, "[Fe(ox)3]3-": True,
          "cis-[Pt(NH3)2Cl2]": False, "fac-[Co(NH3)3Cl3]": False, "cis-[Co(NH3)2(en)2]3+": True}
v_1878 = str(sum(chiral.values()))
assert v_1878 == "3"
# 1884: octahedral complexes with eg empty: (d electrons, strong field?)
def octa(d, strong):
    """(t2g, eg) occupation of an octahedral d^n ion."""
    if strong:
        t = min(d, 6)
        return t, d - t
    order = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1]  # 0 = t2g, 1 = eg (Hund filling, high spin)
    eg = sum(order[:d])
    return d - eg, eg
cpx = {"[Co(NH3)6]3+": (6, True), "[Fe(CN)6]4-": (6, True), "[Cr(H2O)6]3+": (3, False), "[Fe(H2O)6]3+": (5, False),
       "[CoF6]3-": (6, False), "[Ti(H2O)6]3+": (1, False), "[Ni(NH3)6]2+": (8, True), "[Mn(CN)6]3-": (4, True)}
v_1884 = str(sum(1 for d, s in cpx.values() if octa(d, s)[1] == 0))
assert v_1884 == "5" and octa(8, True) == (6, 2) and octa(5, False) == (3, 2) and octa(6, False) == (4, 2)
# 1885: ions per formula unit: potash alum K2SO4.Al2(SO4)3.24H2O -> 2K+ + 2Al3+ + 4SO4 2- ; K3[Al(C2O4)3] -> 3K+ + 1
alum_ions, cpx_ions = 2 + 2 + (1 + 3), 3 + 1
v_1885 = f"{alum_ions} and {cpx_ions}"
assert v_1885 == "8 and 4"
# 1886: CFT configurations
assert octa(1, False) == (1, 0) and octa(3, True) == (3, 0) and octa(5, False) == (3, 2) and octa(6, True) == (6, 0)

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of [Ni(NH₃)₆]Cl₂ is:",
      ["Hexaamminenickelate(II) chloride", "Hexaamminenickel(II) chloride", "Hexaammonianickel(II) chloride",
       "Hexaamminenickel(IV) chloride"], "B",
      "Naming a complex cation",
      "The complex is a cation, so the metal keeps its ordinary name (no -ate ending). NH₃ as a ligand is 'ammine'. "
      "Two Cl⁻ counter ions balance the charge, so the complex ion is [Ni(NH₃)₆]²⁺ and nickel is +2.",
      ["Charge of complex ion = +2 (two Cl⁻ outside)", "x + 6(0) = +2 → Ni(II)",
       "NH₃ → ammine; cationic complex → 'nickel'", "Name: hexaamminenickel(II) chloride"],
      why_others_wrong="'-ate' is used only for anionic complexes; 'ammonia' is not the ligand name for NH₃; the "
                       "oxidation state of Ni is +2, not +4.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=25),

    N(T_CC, "Crystal field theory", "Basic",
      "[CoF₆]³⁻ is a high-spin octahedral complex (atomic number of Co = 27). Its spin-only magnetic moment is about:",
      ["3.87 BM", "0 BM", "5.92 BM", "4.90 BM"], "D", v_1875,
      "Spin-only magnetic moment μ = √(n(n + 2)) BM",
      "Co³⁺ is 3d⁶. F⁻ is a weak field ligand (Δo < P), so the configuration is t₂g⁴ eg², with four unpaired electrons.",
      ["Co (27): [Ar] 3d⁷ 4s² → Co³⁺: 3d⁶", "Weak field: t₂g⁴ eg² → n = 4", "μ = √(4 × 6) = √24 ≈ 4.90 BM"],
      why_others_wrong="0 BM is the low-spin t₂g⁶ case (as in [Co(NH₃)₆]³⁺); 3.87 BM is for three unpaired electrons "
                       "and 5.92 BM for five.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory: octahedral complexes", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Basic", "match_list",
      *ml("For the compound K₃[Fe(C₂O₄)₃], match each term in List-I with the corresponding species or value in "
          "List-II.",
          ["Central ion", "Ligand", "Coordination number", "Counter ion"],
          ["K⁺", "Fe³⁺", "C₂O₄²⁻", "6"],
          "II III IV I", ["II IV III I", "III II IV I", "I III IV II"], "C"),
      "Terms used for coordination compounds",
      "Fe³⁺ is the central ion; each oxalate ion, C₂O₄²⁻, is a didentate ligand, so three of them give a coordination "
      "number of 6; the three K⁺ ions outside the square brackets are the counter ions.",
      ["Central ion: Fe³⁺ (II)", "Ligand: C₂O₄²⁻ (III)", "Coordination number: 3 × 2 = 6 (IV)", "Counter ion: K⁺ (I)"],
      why_others_wrong="Taking the coordination number as 3 (number of ligands) confuses it with the oxalate entry; "
                       "K⁺ is outside the coordination sphere and is not the central ion.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=40),

    Q(T_CC, "Crystal field theory", "Basic", "assertion_reason",
      *ar("Aqueous solutions containing [Sc(H₂O)₆]³⁺ are colourless.", True,
          "Sc³⁺ has no d electron, so no d–d transition can take place.", True, explains=True),
      "Origin of colour in complexes",
      "In crystal field theory the colour of a complex comes from excitation of a d electron from a lower to a higher "
      "set of d orbitals (d–d transition). Sc³⁺ is 3d⁰, so no such transition is possible and visible light is not "
      "absorbed. R explains A.",
      ["Sc (21): [Ar] 3d¹ 4s² → Sc³⁺: 3d⁰", "No d electron → no d–d transition", "No absorption in the visible → colourless"],
      ncert=f"{NC12}, 'Coordination Compounds', colour in coordination compounds", seconds=30),

    N(T_CC, "Isomerism", "Intermediate",
      "How many of the following species are optically active (ox = oxalate, C₂O₄²⁻; en = ethane-1,2-diamine)?\n"
      "cis-[CrCl₂(ox)₂]³⁻, trans-[CrCl₂(ox)₂]³⁻, [Fe(ox)₃]³⁻, cis-[Pt(NH₃)₂Cl₂] (square planar), "
      "fac-[Co(NH₃)₃Cl₃], cis-[Co(NH₃)₂(en)₂]³⁺",
      ["2", "3", "4", "5"], "B", v_1878,
      "Optical isomerism in octahedral complexes with didentate ligands",
      "Octahedral complexes with two or three didentate ligands in a cis arrangement have no plane of symmetry and "
      "are chiral. A trans arrangement, a square planar complex and the fac isomer of [MA₃B₃] all have a mirror plane.",
      ["cis-[CrCl₂(ox)₂]³⁻: chiral", "trans-[CrCl₂(ox)₂]³⁻: mirror plane → inactive", "[Fe(ox)₃]³⁻: chiral (like [Co(en)₃]³⁺)",
       "cis-[Pt(NH₃)₂Cl₂]: planar → inactive", "fac-[Co(NH₃)₃Cl₃]: mirror plane → inactive",
       "cis-[Co(NH₃)₂(en)₂]³⁺: chiral", "Total = 3"],
      why_others_wrong="2 misses the tris(oxalato) complex; 4 counts the trans isomer; 5 also counts a planar or fac "
                       "species, which have mirror planes.",
      ncert=f"{NC12}, 'Coordination Compounds', stereoisomerism: optical isomerism", seconds=75),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "direct",
      "Which of the following contains a complex ion that is both homoleptic and anionic?",
      ["[Co(NH₃)₆]Cl₃", "[Co(NH₃)₄Cl₂]Cl", "K[Cr(H₂O)₂(C₂O₄)₂]", "K₃[Fe(CN)₆]"], "D",
      "Homoleptic and heteroleptic complexes; cationic and anionic complexes",
      "A homoleptic complex has only one kind of ligand. [Fe(CN)₆]³⁻ has only CN⁻ ligands and carries a negative "
      "charge, so it is homoleptic and anionic.",
      ["[Co(NH₃)₆]³⁺: homoleptic but cationic", "[Co(NH₃)₄Cl₂]⁺: heteroleptic, cationic",
       "[Cr(H₂O)₂(C₂O₄)₂]⁻: anionic but heteroleptic", "[Fe(CN)₆]³⁻: homoleptic and anionic"],
      why_others_wrong="Each of the other complex ions fails one of the two conditions, as shown in the steps.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=40),

    Q(T_CC, "Crystal field theory", "Intermediate", "statement_pair",
      *sp("In the spectrochemical series, OH⁻ is a weaker field ligand than H₂O.", True,
          "Thiocyanate bonded through sulphur (SCN⁻) produces a larger crystal field splitting than thiocyanate "
          "bonded through nitrogen (NCS⁻).", False),
      "Spectrochemical series",
      "NCERT's series runs I⁻ < Br⁻ < SCN⁻ < Cl⁻ < S²⁻ < F⁻ < OH⁻ < C₂O₄²⁻ < H₂O < NCS⁻ < edta⁴⁻ < NH₃ < en < CN⁻ < CO. "
      "OH⁻ comes before H₂O, so it is the weaker field ligand (Statement I true). S-bonded SCN⁻ lies near the weak end "
      "and N-bonded NCS⁻ after H₂O, so NCS⁻ gives the larger splitting (Statement II false).",
      ["OH⁻ < C₂O₄²⁻ < H₂O → Statement I true", "SCN⁻ (weak end) < NCS⁻ → Statement II false"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory: spectrochemical series", seconds=45),

    Q(T_CC, "Valence bond theory", "Intermediate", "multi_statement",
      *ms("Which of the following statements about [Co(NH₃)₆]³⁺ and [CoF₆]³⁻ are correct (atomic number of Co = 27)?",
          [("In both complexes cobalt is in the +3 oxidation state with a 3d⁶ configuration.", True),
           ("[CoF₆]³⁻ is an outer orbital complex in which cobalt uses sp³d² hybrid orbitals.", True),
           ("[Co(NH₃)₆]³⁺ has four unpaired electrons.", False),
           ("Both complexes are octahedral.", True),
           ("F⁻ is a stronger field ligand than NH₃.", False)],
          [["a", "b"], ["a", "c", "d"], ["b", "d", "e"]], "B"),
      "Inner and outer orbital octahedral complexes of Co(III)",
      "Both are Co³⁺ (3d⁶), six-coordinate and octahedral. NH₃ pairs the 3d electrons, leaving two 3d orbitals free for "
      "d²sp³ hybridisation (inner orbital, diamagnetic). F⁻ is weak field, so the 4d orbitals are used (sp³d², outer "
      "orbital, four unpaired electrons).",
      ["(a) true", "(b) true: sp³d², outer orbital", "(c) false: [Co(NH₃)₆]³⁺ is diamagnetic", "(d) true",
       "(e) false: F⁻ is a weaker field ligand than NH₃"],
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=60),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Match the ligand in List-I with its description in List-II.",
          ["Ethane-1,2-diamine", "Oxalate ion", "Ethylenediaminetetraacetate ion", "Pyridine"],
          ["Anionic, didentate", "Neutral, unidentate", "Anionic, hexadentate", "Neutral, didentate"],
          "IV I III II", ["I IV III II", "IV I II III", "IV III I II"], "D"),
      "Charge and denticity of ligands",
      "en, H₂N–CH₂–CH₂–NH₂, is neutral and binds through both N atoms. C₂O₄²⁻ is a dianion that binds through two O "
      "atoms. EDTA⁴⁻ binds through two N and four O atoms. Pyridine, C₅H₅N, is neutral and binds only through N.",
      ["en → neutral, didentate (IV)", "C₂O₄²⁻ → anionic, didentate (I)", "EDTA⁴⁻ → anionic, hexadentate (III)",
       "Pyridine → neutral, unidentate (II)"],
      why_others_wrong="The other codes swap the neutral en and the anionic oxalate, or mix up the denticities of EDTA "
                       "and pyridine.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms: ligands", seconds=40),

    Q(T_CC, "Crystal field theory", "Intermediate", "assertion_reason",
      *ar("The crystal field splitting Δo of [CrCl₆]³⁻ is smaller than that of [Cr(NH₃)₆]³⁺.", True,
          "Cl⁻ lies before NH₃ in the spectrochemical series, i.e. it is a weaker field ligand.", True, explains=True),
      "Dependence of Δo on the ligand",
      "For the same metal ion in the same oxidation state (Cr³⁺) and the same geometry, Δo depends on the field "
      "strength of the ligand. Cl⁻ is a weaker field ligand than NH₃, so the splitting is smaller. R explains A.",
      ["Same metal, oxidation state and geometry", "Cl⁻ < NH₃ in the spectrochemical series", "→ Δo(CrCl₆³⁻) < Δo(Cr(NH₃)₆³⁺)"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory", seconds=35),

    N(T_CC, "Crystal field theory", "Advanced",
      "According to crystal field theory, in how many of the following octahedral complexes are the eg orbitals "
      "completely empty? (Atomic numbers: Ti 22, Cr 24, Mn 25, Fe 26, Co 27, Ni 28; [Mn(CN)₆]³⁻ is low spin.)\n"
      "[Co(NH₃)₆]³⁺, [Fe(CN)₆]⁴⁻, [Cr(H₂O)₆]³⁺, [Fe(H₂O)₆]³⁺, [CoF₆]³⁻, [Ti(H₂O)₆]³⁺, [Ni(NH₃)₆]²⁺, [Mn(CN)₆]³⁻",
      ["4", "6", "5", "3"], "C", v_1884,
      "Filling of t₂g and eg orbitals in octahedral complexes",
      "d¹–d³ ions always have empty eg orbitals. A d⁴–d⁶ ion keeps eg empty only with strong field ligands (low spin). "
      "A d⁸ ion must place two electrons in eg whatever the ligand, because t₂g holds only six.",
      ["[Co(NH₃)₆]³⁺ d⁶ LS: t₂g⁶ → empty", "[Fe(CN)₆]⁴⁻ d⁶ LS: t₂g⁶ → empty", "[Cr(H₂O)₆]³⁺ d³: t₂g³ → empty",
       "[Fe(H₂O)₆]³⁺ d⁵ HS: t₂g³ eg² → not empty", "[CoF₆]³⁻ d⁶ HS: t₂g⁴ eg² → not empty",
       "[Ti(H₂O)₆]³⁺ d¹ → empty", "[Ni(NH₃)₆]²⁺ d⁸: t₂g⁶ eg² → not empty", "[Mn(CN)₆]³⁻ d⁴ LS: t₂g⁴ → empty",
       "Total = 5"],
      why_others_wrong="6 assumes the strong field NH₃ empties eg in the d⁸ nickel complex; 4 misses the low-spin "
                       "manganese complex; 3 counts only the d¹ and d³ ions and one d⁶ ion.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=110),

    N(T_CC, "Werner's theory and ligands", "Advanced",
      "Potash alum, K₂SO₄·Al₂(SO₄)₃·24H₂O, is a double salt, whereas K₃[Al(C₂O₄)₃] is a coordination compound. "
      "Assuming complete dissociation of each in dilute aqueous solution, the numbers of ions given by one formula "
      "unit of potash alum and of K₃[Al(C₂O₄)₃] are, respectively:",
      ["8 and 4", "3 and 4", "8 and 7", "4 and 4"], "A", v_1885,
      "Double salts versus complexes in solution",
      "A double salt dissociates completely into simple ions in water. A complex ion keeps its identity, so only the "
      "counter ions separate from it.",
      ["Alum: 2K⁺ + 2Al³⁺ + 4SO₄²⁻ = 8 ions", "K₃[Al(C₂O₄)₃]: 3K⁺ + [Al(C₂O₄)₃]³⁻ = 4 ions"],
      why_others_wrong="'3 and 4' treats alum as a complex ion with two K⁺; '8 and 7' breaks the oxalato complex into "
                       "Al³⁺ and three C₂O₄²⁻; '4 and 4' uses the half formula KAl(SO₄)₂·12H₂O instead of the formula "
                       "unit given.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory: double salts and complexes", seconds=70),

    Q(T_CC, "Crystal field theory", "Advanced", "match_list",
      *ml("Match the octahedral complex ion in List-I with its d-electron configuration according to crystal field "
          "theory in List-II (atomic numbers: Ti 22, Cr 24, Fe 26, Co 27).",
          ["[Ti(H₂O)₆]³⁺", "[Cr(NH₃)₆]³⁺", "[Fe(H₂O)₆]³⁺", "[Co(NH₃)₆]³⁺"],
          ["t₂g⁶ eg⁰", "t₂g³ eg²", "t₂g¹ eg⁰", "t₂g³ eg⁰"],
          "III IV II I", ["III II IV I", "IV III II I", "III IV I II"], "B"),
      "Writing t₂g/eg configurations from oxidation state and ligand strength",
      "Find the d-electron count from the oxidation state, then fill t₂g first; for d⁴–d⁷ use the ligand strength to "
      "decide between high and low spin.",
      ["Ti³⁺ d¹ → t₂g¹ (III)", "Cr³⁺ d³ → t₂g³ (IV)", "Fe³⁺ d⁵ with weak field H₂O → t₂g³ eg² (II)",
       "Co³⁺ d⁶ with NH₃ (Δo > P, diamagnetic) → t₂g⁶ (I)"],
      why_others_wrong="'A-III, B-II, C-IV, D-I' gives Cr³⁺ five d electrons and Fe³⁺ three; 'A-IV, B-III, ...' swaps "
                       "the d¹ and d³ ions; 'A-III, B-IV, C-I, D-II' swaps the Fe³⁺ (d⁵) and Co³⁺ (d⁶) "
                       "configurations.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=80),

    Q(T_CC, "Valence bond theory", "Advanced", "statement_pair",
      *sp("[Ni(CN)₄]²⁻ and [Ni(CO)₄] are both diamagnetic, although nickel is in different oxidation states in them.",
          True,
          "[NiCl₄]²⁻ is square planar, because Cl⁻ is a strong field ligand that forces the 3d electrons to pair up.",
          False),
      "Four-coordinate nickel complexes in valence bond theory",
      "In [Ni(CN)₄]²⁻ (Ni²⁺, 3d⁸) the strong field CN⁻ pairs the d electrons, giving dsp², square planar and "
      "diamagnetic. In [Ni(CO)₄] (Ni⁰) all ten electrons pair in 3d, giving sp³, tetrahedral and diamagnetic. So "
      "Statement I is true. Cl⁻ is a weak field ligand: [NiCl₄]²⁻ is sp³, tetrahedral and paramagnetic with two "
      "unpaired electrons, so Statement II is false.",
      ["[Ni(CN)₄]²⁻: Ni(II), dsp², 0 unpaired", "[Ni(CO)₄]: Ni(0), sp³, 0 unpaired → Statement I true",
       "[NiCl₄]²⁻: weak field, sp³, tetrahedral, 2 unpaired → Statement II false"],
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory: tetrahedral and square planar complexes",
      seconds=55),

    Q(T_CC, "Isomerism", "Advanced", "multi_statement",
      *ms("Consider the complex K₃[Cr(C₂O₄)₃] (atomic number of Cr = 24). Which of the following statements are "
          "correct?",
          [("The oxidation state of chromium is +3.", True),
           ("The coordination number of chromium is 6.", True),
           ("The complex ion exists as a pair of enantiomers.", True),
           ("The complex ion has three unpaired electrons.", True),
           ("Its IUPAC name is potassium trioxalatochromium(III).", False)],
          [["a", "b", "c"], ["a", "b", "d", "e"], ["b", "c", "d"]], "D"),
      "Oxidation state, coordination number, optical isomerism and magnetism of a tris(chelate) complex",
      "x + 3(−2) = −3 gives Cr(III), 3d³. Three didentate oxalate ions give coordination number 6. Like [Co(en)₃]³⁺, "
      "a tris(didentate) octahedral ion is chiral. A d³ ion has t₂g³, three unpaired electrons. As the complex is an "
      "anion, the metal name ends in -ate: potassium trioxalatochromate(III).",
      ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: 'chromate(III)' for an anionic complex"],
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature and isomerism", seconds=70),
]
