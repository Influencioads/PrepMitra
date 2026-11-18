
# ================================================================ Coordination Compounds (2148-2161)
# 2149: anionic ligands in the list
lig_2149 = {"en": 0, "C2O4": -2, "py": 0, "CN": -1, "NH3": 0, "NO2": -1, "H2O": 0, "Cl": -1, "CO": 0}
v_2149 = str(sum(1 for c in lig_2149.values() if c < 0))
assert v_2149 == "4"
# 2152: [Cr(H2O)6]2+ high spin d4 (4 unpaired) vs [Cr(CN)6]4- low spin t2g4 (2 unpaired)
v_2152 = f"{bm(4) - bm(2):.2f} BM"
assert v_2152 == "2.07 BM" and f"{bm(4) - bm(3):.2f}" == "1.03"
# 2153: Ag+ + e- -> Ag from K[Ag(CN)2]; 965 C
m_2153 = F(965, 96500) * AM["Ag"]
assert m_2153 == F(108, 100)
v_2153 = f"{float(m_2153):.2f} g"
# 2158: d6, E(LS) - E(HS) = (-2.4 + 0.4) Do + 2P (two extra pairs in t2g6)
Do, Pe = 23000, 21000
cfse = lambda t2g, eg: F(-4, 10) * t2g + F(6, 10) * eg
pairs = lambda t2g, eg: max(0, t2g - 3) + max(0, eg - 2)
e_ls = cfse(6, 0) * Do + pairs(6, 0) * Pe
e_hs = cfse(4, 2) * Do + pairs(4, 2) * Pe
assert cfse(6, 0) == F(-24, 10) and cfse(4, 2) == F(-4, 10) and (pairs(6, 0), pairs(4, 2)) == (3, 1)
assert e_ls - e_hs == -4000
v_2158 = "Low spin, by 4000 cm⁻¹"

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The formula of tris(ethane-1,2-diamine)cobalt(III) sulphate is:",
      ["[Co(en)₃](SO₄)₃", "[Co(en)₃]₃(SO₄)₂", "[Co(en)₃]₂(SO₄)₃", "[Co(en)₂]₂(SO₄)₃"], "C",
      "Writing the formula from the name",
      "'Tris(ethane-1,2-diamine)' means three neutral en ligands, so the complex ion is [Co(en)₃]³⁺. Two such cations "
      "(total +6) are balanced by three sulphate ions (total −6).",
      ["Complex ion: [Co(en)₃]³⁺ (en is neutral)", "Charge balance: 2 × (+3) = 3 × (−2)", "Formula: [Co(en)₃]₂(SO₄)₃"],
      why_others_wrong="[Co(en)₃](SO₄)₃ and [Co(en)₃]₃(SO₄)₂ are not electrically neutral; [Co(en)₂]₂(SO₄)₃ has only "
                       "two en ligands, which would be 'bis'.",
      ncert=f"{NC12}, 'Coordination Compounds', formulas of mononuclear coordination entities", seconds=30),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "How many of the following ligands are anionic?\n"
      "H₂NCH₂CH₂NH₂ (en), C₂O₄²⁻, C₅H₅N (pyridine), CN⁻, NH₃, NO₂⁻, H₂O, Cl⁻, CO",
      ["1", "2", "3", "4"], "D", v_2149,
      "Classifying ligands by charge",
      "Ligands may be neutral molecules with a lone pair (en, pyridine, NH₃, H₂O, CO) or anions (C₂O₄²⁻, CN⁻, NO₂⁻, "
      "Cl⁻).",
      ["Neutral: en, pyridine, NH₃, H₂O, CO (5)", "Anionic: C₂O₄²⁻, CN⁻, NO₂⁻, Cl⁻ (4)"],
      why_others_wrong="Lower counts usually miss the oxalate or nitrite ion; en and pyridine are neutral even though "
                       "they are named as ligands without 'o' endings.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms: ligands", seconds=30),

    Q(T_CC, "Applications", "Basic", "statement_pair",
      *sp("EDTA is used in the treatment of lead poisoning.", True,
          "The coordination polyhedron of [PtCl₄]²⁻ is square planar.", True),
      "Chelate therapy; coordination polyhedra",
      "In chelate therapy, a chelating ligand binds a toxic metal so that it can be removed from the body; NCERT cites "
      "EDTA for lead poisoning. The four chloride ligands in [PtCl₄]²⁻ lie at the corners of a square around "
      "platinum, so its coordination polyhedron is square planar.",
      ["Statement I: true (chelate therapy)", "Statement II: true"],
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications; coordination polyhedron", seconds=30),

    Q(T_CC, "Werner's theory and ligands", "Basic", "assertion_reason",
      *ar("Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O, is a double salt, whereas [Co(NH₃)₆]Cl₃ is a coordination compound.",
          True,
          "In water, Mohr's salt dissociates completely into simple ions, whereas the [Co(NH₃)₆]³⁺ ion does not "
          "dissociate into Co³⁺ and NH₃.", True, explains=True),
      "Double salts and complexes",
      "Double salts such as Mohr's salt and carnallite exist only in the solid state and give all their simple ions "
      "(Fe²⁺, NH₄⁺, SO₄²⁻) in solution. A coordination compound keeps its complex ion intact in solution. That "
      "difference in behaviour in water is what classifies them, so R explains A.",
      ["Mohr's salt → Fe²⁺ + 2NH₄⁺ + 2SO₄²⁻ (all simple ions)", "[Co(NH₃)₆]Cl₃ → [Co(NH₃)₆]³⁺ + 3Cl⁻",
       "Complex ion stays intact → coordination compound"],
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory: double salts and complexes", seconds=35),

    N(T_CC, "Crystal field theory", "Intermediate",
      "[Cr(H₂O)₆]²⁺ is a high-spin complex and [Cr(CN)₆]⁴⁻ is a low-spin complex (Z of Cr = 24). The difference "
      "between their spin-only magnetic moments is about:",
      ["4.90 BM", "2.83 BM", v_2152, "1.03 BM"], "C", v_2152,
      "High-spin and low-spin d⁴ octahedral complexes",
      "Cr²⁺ is 3d⁴. With the weak field ligand H₂O (Δo < P) the fourth electron enters eg: t₂g³ eg¹, four unpaired "
      "electrons. With the strong field ligand CN⁻ (Δo > P) it pairs in t₂g: t₂g⁴ eg⁰, two unpaired electrons.",
      ["High spin: n = 4, μ = √24 ≈ 4.90 BM", "Low spin: n = 2, μ = √8 ≈ 2.83 BM", "Difference ≈ 2.07 BM"],
      why_others_wrong="4.90 BM treats the low-spin complex as diamagnetic; 2.83 BM applies the formula to the "
                       "difference in the number of unpaired electrons; 1.03 BM takes three unpaired electrons for the "
                       "low-spin complex.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=60),

    N(T_CC, "Applications", "Intermediate",
      "Articles are electroplated with silver from a solution of the complex K[Ag(CN)₂]. What mass of silver is "
      "deposited at the cathode when 965 C of charge is passed? (Ag = 108, F = 96500 C mol⁻¹)",
      ["0.54 g", "2.16 g", "10.8 g", v_2153], "D", v_2153,
      "Electroplating from a complex; Faraday's law",
      "Silver is +1 in [Ag(CN)₂]⁻. The complex keeps the concentration of free Ag⁺ low, which gives a smooth, even "
      "deposit, but each silver atom deposited still needs one electron.",
      ["Moles of electrons = 965/96500 = 0.010 mol", "Ag⁺ + e⁻ → Ag: 0.010 mol Ag", "Mass = 0.010 × 108 = 1.08 g"],
      why_others_wrong="0.54 g assumes two electrons per silver atom; 2.16 g assumes two silver atoms per electron; "
                       "10.8 g is a tenfold slip in the moles of electrons.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications", seconds=50),

    Q(T_CC, "Isomerism", "Intermediate", "multi_statement",
      *ms("Which of the following statements about structural isomerism in coordination compounds are correct?",
          [("Solvate isomerism is called hydrate isomerism when water is the solvent involved.", True),
           ("Linkage isomerism arises in a coordination compound that contains an ambidentate ligand.", True),
           ("Coordination isomerism arises from the interchange of ligands between the cationic and anionic entities "
            "of different metal ions in a complex.", True),
           ("Ionisation isomerism arises when the counter ion is itself a potential ligand and can displace a ligand, "
            "which then becomes the counter ion.", True),
           ("Stereoisomers have the same chemical bonds but different chemical formulae.", False)],
          [["a", "b", "e"], ["b", "c", "d"], ["a", "c", "d", "e"]], "C"),
      "Kinds of isomerism in coordination compounds",
      "Statements (a) to (d) are NCERT's descriptions of the four kinds of structural isomerism. Stereoisomers have the "
      "same chemical formula and the same chemical bonds but a different spatial arrangement, so (e) is false.",
      ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: same formula, different spatial arrangement"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=45),

    Q(T_CC, "Crystal field theory", "Intermediate", "direct",
      "For an octahedral complex, the number of unpaired electrons can differ between weak field (high spin) and strong "
      "field (low spin) ligands only when the metal ion has the configuration:",
      ["d¹ to d³", "d⁴ to d⁷", "d⁸ to d¹⁰", "d³ to d⁸"], "B",
      "When high-spin and low-spin arrangements are possible",
      "For d¹ to d³ the electrons simply occupy t₂g singly. From d⁴ the next electron can either enter eg (Δo < P) or "
      "pair in t₂g (Δo > P). For d⁸ to d¹⁰, t₂g is full and eg receives the rest in the same way whatever Δo is "
      "(t₂g⁶ eg², t₂g⁶ eg³, t₂g⁶ eg⁴).",
      ["d⁴: t₂g³ eg¹ or t₂g⁴", "d⁵: t₂g³ eg² or t₂g⁵", "d⁶: t₂g⁴ eg² or t₂g⁶", "d⁷: t₂g⁵ eg² or t₂g⁶ eg¹",
       "d¹–d³ and d⁸–d¹⁰: only one arrangement"],
      why_others_wrong="d¹–d³ and d⁸–d¹⁰ have only one possible arrangement; d³ to d⁸ wrongly includes d³ and d⁸.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Match the coordination compound in List-I with the description of its coordination entity in List-II.",
          ["K₄[Fe(CN)₆]", "[Co(NH₃)₅Cl]Cl₂", "[Ni(CO)₄]", "[Pt(NH₃)₂Cl₂]"],
          ["Heteroleptic, neutral", "Homoleptic, anionic", "Homoleptic, neutral", "Heteroleptic, cationic"],
          "II IV III I", ["II I III IV", "III IV II I", "IV II I III"], "D"),
      "Homoleptic and heteroleptic entities; charge of the entity",
      "A homoleptic entity has only one kind of donor group; a heteroleptic one has more than one kind. The charge of "
      "the entity is found from the metal's oxidation state and the ligand charges.",
      ["[Fe(CN)₆]⁴⁻: only CN⁻, charge −4 → homoleptic, anionic (II)",
       "[Co(NH₃)₅Cl]²⁺: NH₃ and Cl⁻, charge +2 → heteroleptic, cationic (IV)",
       "[Ni(CO)₄]: only CO, charge 0 → homoleptic, neutral (III)",
       "[Pt(NH₃)₂Cl₂]: NH₃ and Cl⁻, charge 0 → heteroleptic, neutral (I)"],
      why_others_wrong="Codes that call [Co(NH₃)₅Cl]²⁺ neutral forget that only two of the three chlorides are "
                       "counter ions; [Ni(CO)₄] has a single kind of ligand and is not heteroleptic.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=45),

    Q(T_CC, "Isomerism", "Intermediate", "assertion_reason",
      *ar("The square planar complex [Pt(NH₃)₂Cl₂] exists as cis and trans isomers.", True,
          "cis-Platin, the cis isomer of [Pt(NH₃)₂Cl₂], is used to inhibit the growth of tumours.", True),
      "Geometrical isomerism in square planar complexes",
      "In a square planar [MX₂L₂] complex the two Cl ligands can be next to each other (cis) or opposite each other "
      "(trans), so two geometrical isomers exist. R is a true statement about the medical use of the cis isomer; it "
      "says nothing about why two arrangements are possible, so it does not explain A.",
      ["Square planar MX₂L₂ → cis and trans", "R: medical use of one isomer, not the cause of isomerism"],
      ncert=f"{NC12}, 'Coordination Compounds', geometric isomerism; applications", seconds=35),

    N(T_CC, "Crystal field theory", "Advanced",
      "For a certain d⁶ metal ion in an octahedral field, Δo = 23000 cm⁻¹ and the pairing energy P = 21000 cm⁻¹. "
      "Taking into account both the crystal field stabilisation energy and the extra electron pairing, which "
      "arrangement is more stable, and by how much?",
      ["High spin, by 4000 cm⁻¹", v_2158, "Low spin, by 46000 cm⁻¹", "Low spin, by 2000 cm⁻¹"], "B", v_2158,
      "Balance between Δo and pairing energy",
      "In an octahedral field t₂g lies (2/5)Δo below and eg (3/5)Δo above the barycentre. High spin d⁶ is t₂g⁴ eg² "
      "with one pair; low spin d⁶ is t₂g⁶ with three pairs. The low-spin form gains crystal field stabilisation but "
      "must pay for two extra pairs.",
      ["High spin: CFSE = 4(−0.4Δo) + 2(0.6Δo) = −0.4Δo; 1 pair",
       "Low spin: CFSE = 6(−0.4Δo) = −2.4Δo; 3 pairs",
       "E(low) − E(high) = −2.0Δo + 2P = −46000 + 42000 = −4000 cm⁻¹",
       "Low spin is more stable by 4000 cm⁻¹ (consistent with Δo > P)"],
      why_others_wrong="'High spin' reverses the sign; 46000 cm⁻¹ ignores the pairing energy; 2000 cm⁻¹ counts only "
                       "one extra pair and half the CFSE difference.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory: octahedral complexes", seconds=110),

    Q(T_CC, "Isomerism", "Advanced", "multi_statement",
      *ms("Consider the octahedral complex [Co(NH₃)₄Cl₂]NO₂. Which of the following statements are correct?",
          [("It can exist as cis and trans isomers.", True),
           ("[Co(NH₃)₄Cl(NO₂)]Cl is an ionisation isomer of it.", True),
           ("The ionisation isomer [Co(NH₃)₄Cl(NO₂)]Cl can itself show linkage isomerism.", True),
           ("One mole of [Co(NH₃)₄Cl₂]NO₂ gives two moles of AgCl with excess AgNO₃ solution.", False),
           ("The coordination number of cobalt in it is 4.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "D"),
      "Combining geometrical, ionisation and linkage isomerism",
      "The entity [Co(NH₃)₄Cl₂]⁺ is of the type [MA₄B₂] and has cis and trans forms. Exchanging the counter ion NO₂⁻ "
      "with one coordinated Cl⁻ gives the ionisation isomer [Co(NH₃)₄Cl(NO₂)]Cl, and in that compound the ambidentate "
      "nitrite can bind through N or O. Both chlorides of the original compound are inside the coordination sphere, "
      "so it gives no AgCl. Four NH₃ and two Cl make the coordination number 6.",
      ["(a) true: [MA₄B₂]", "(b) true", "(c) true: NO₂⁻ / ONO⁻", "(d) false: Cl⁻ is coordinated, NO₂⁻ is the counter ion",
       "(e) false: CN = 6"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=80),

    Q(T_CC, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of [Pt(NH₃)₄][PtCl₄] is:",
      ["Tetraammineplatinum(II) tetrachloridoplatinum(II)", "Tetrachloridoplatinum(II) tetraammineplatinate(II)",
       "Tetraammineplatinum(II) tetrachloridoplatinate(II)", "Tetraammineplatinate(II) tetrachloridoplatinum(II)"],
      "C",
      "Naming a salt in which both ions are complex",
      "The cation is named first. [Pt(NH₃)₄]²⁺ is a cation, so platinum keeps its plain name. [PtCl₄]²⁻ is an anion, so "
      "the metal name takes the ending '-ate'. In each ion platinum is +2.",
      ["Cation [Pt(NH₃)₄]²⁺: x + 0 = +2 → Pt(II): tetraammineplatinum(II)",
       "Anion [PtCl₄]²⁻: x − 4 = −2 → Pt(II): tetrachloridoplatinate(II)",
       "Name: tetraammineplatinum(II) tetrachloridoplatinate(II)"],
      why_others_wrong="The anion needs the '-ate' ending; the cation must be named first; '-ate' is never used for a "
                       "cationic entity.",
      ncert=f"{NC12}, 'Coordination Compounds', naming of mononuclear coordination compounds", seconds=40),

    Q(T_CC, "Isomerism", "Advanced", "statement_pair",
      *sp("cis-[Co(NH₃)₄Cl₂]⁺ is optically inactive.", True,
          "cis-[Co(en)₂(NH₃)Cl]²⁺ is optically active.", True),
      "Optical activity of cis octahedral complexes",
      "cis-[Co(NH₃)₄Cl₂]⁺ has a mirror plane that contains the cobalt and both chlorine atoms, so it is superimposable "
      "on its mirror image. In cis-[Co(en)₂(NH₃)Cl]²⁺ the two didentate en rings are arranged in a propeller-like way "
      "(as in cis-[Co(en)₂Cl₂]⁺); it has no plane of symmetry and exists as a pair of enantiomers.",
      ["Statement I: unidentate ligands only, mirror plane → inactive: true",
       "Statement II: two chelate rings in cis arrangement, no mirror plane → active: true"],
      ncert=f"{NC12}, 'Coordination Compounds', optical isomerism", seconds=60),
]
