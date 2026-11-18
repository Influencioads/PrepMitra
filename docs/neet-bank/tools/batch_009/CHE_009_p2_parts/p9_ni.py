
# ================================================================ Organic Compounds Containing Nitrogen (2224-2233)
# 2225: primary amines (one carbon on N)
amine_class = {"(CH3)3CNH2": 1, "CH3NHCH3": 2, "C6H5NH2": 1, "C6H5CH2NH2": 1, "(C2H5)3N": 3, "CH3CH2NH2": 1}
v_2225 = str(sum(1 for c in amine_class.values() if c == 1))
assert v_2225 == "4"
# 2227: Gabriel synthesis gives only primary amines from alkyl (not aryl) halides
gabriel = {"ethanamine": True, "propan-1-amine": True, "benzylamine": True, "aniline": False,
           "N-methylethanamine": False, "triethylamine": False}
v_2227 = str(sum(gabriel.values()))
assert v_2227 == "3"

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "The IUPAC name of benzylamine, C₆H₅–CH₂–NH₂, is:",
      ["Benzenamine", "N-Phenylmethanamine", "Phenylmethanamine", "2-Phenylethanamine"], "C",
      "Naming amines",
      "The –NH₂ group is on the CH₂ carbon, so the parent is methanamine and the phenyl group is a substituent on that "
      "carbon: phenylmethanamine. Benzenamine is aniline, where –NH₂ is on the ring.",
      ["Parent chain: CH₂–NH₂ → methanamine", "Substituent on carbon: phenyl", "Name: phenylmethanamine"],
      why_others_wrong="Benzenamine is C₆H₅NH₂; 'N-phenyl' would put the phenyl group on nitrogen (C₆H₅NHCH₃); "
                       "2-phenylethanamine has two CH₂ groups.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=25),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "How many of the following are primary amines?\n"
      "(CH₃)₃C–NH₂, CH₃–NH–CH₃, C₆H₅NH₂, C₆H₅CH₂NH₂, (C₂H₅)₃N, CH₃CH₂NH₂",
      ["3", v_2225, "5", "6"], "B", v_2225,
      "Classification of amines",
      "An amine is primary, secondary or tertiary according to the number of hydrogen atoms of ammonia replaced by "
      "alkyl or aryl groups (one, two or three), not according to the kind of carbon atom attached to nitrogen.",
      ["Primary (–NH₂): (CH₃)₃CNH₂, C₆H₅NH₂, C₆H₅CH₂NH₂, CH₃CH₂NH₂", "Secondary: CH₃NHCH₃",
       "Tertiary: (C₂H₅)₃N", "Count = 4"],
      why_others_wrong="3 usually treats (CH₃)₃CNH₂ as tertiary because its carbon is tertiary; 5 or 6 count the "
                       "secondary or tertiary amine.",
      ncert=f"{NC12}, 'Amines', structure and classification", seconds=30),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("The lower aliphatic amines are gases with a fishy odour, and primary amines with three or more carbon atoms "
          "are liquids.", True,
          "The higher amines are highly soluble in water.", False),
      "Physical properties of amines",
      "NCERT describes the lower aliphatic amines as gases with a fishy smell; primary amines with three or more carbon "
      "atoms are liquids and still higher ones solids. Solubility in water falls as the hydrophobic alkyl part grows, "
      "so the higher amines are essentially insoluble.",
      ["Statement I: true", "Statement II: false; solubility decreases with increasing molar mass"],
      ncert=f"{NC12}, 'Amines', physical properties", seconds=25),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "How many of the following amines can be prepared by Gabriel phthalimide synthesis?\n"
      "Ethanamine, propan-1-amine, benzylamine, aniline, N-methylethanamine, triethylamine",
      ["2", v_2227, "4", "5"], "B", v_2227,
      "Scope of Gabriel phthalimide synthesis",
      "Potassium phthalimide is alkylated by an alkyl halide and the product is hydrolysed, so only primary amines are "
      "obtained. Aromatic primary amines cannot be made this way because aryl halides do not undergo nucleophilic "
      "substitution with the phthalimide anion. Benzyl chloride is an alkyl-type halide and reacts normally.",
      ["Yes: ethanamine, propan-1-amine, benzylamine (primary, from alkyl or benzyl halides)",
       "No: aniline (aryl halide unreactive), N-methylethanamine (2°), triethylamine (3°)", "Count = 3"],
      why_others_wrong="2 wrongly excludes benzylamine; 4 or 5 include aniline or a secondary/tertiary amine.",
      ncert=f"{NC12}, 'Amines', preparation: Gabriel phthalimide synthesis", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Aniline does not undergo the Friedel–Crafts reaction.", True,
          "Aniline forms a salt with the Lewis acid AlCl₃; the nitrogen then carries a positive charge and acts as a "
          "strongly deactivating group.", True, explains=True),
      "Why aniline fails in Friedel–Crafts reactions",
      "The basic –NH₂ group donates its lone pair to AlCl₃. The resulting positively charged nitrogen withdraws "
      "electrons from the ring, so the ring is deactivated and no alkylation or acylation occurs. R explains A.",
      ["C₆H₅NH₂ + AlCl₃ → C₆H₅NH₂⁺–AlCl₃⁻", "Positive N deactivates the ring", "→ no Friedel–Crafts reaction"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution in aromatic amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "direct",
      "In the gaseous phase, where solvation is absent, the basic strength of the methyl-substituted amines and ammonia "
      "follows the order:",
      ["(CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃", "NH₃ > CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N", "CH₃NH₂ > (CH₃)₂NH > (CH₃)₃N > NH₃",
       "(CH₃)₃N > (CH₃)₂NH > CH₃NH₂ > NH₃"], "D",
      "Basicity of amines in the gas phase",
      "In the gas phase only the +I effect of the alkyl groups matters: each methyl group pushes electron density onto "
      "nitrogen, so tertiary > secondary > primary > NH₃. In water, solvation of the ammonium ions and steric "
      "factors change the order to (CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃.",
      ["Gas phase: +I effect only", "More alkyl groups → more basic", "3° > 2° > 1° > NH₃"],
      why_others_wrong="(CH₃)₂NH > CH₃NH₂ > (CH₃)₃N > NH₃ is the order in aqueous solution; the other two orders ignore "
                       "the +I effect.",
      ncert=f"{NC12}, 'Amines', basic character of amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the test in List-I with the observation in List-II.",
          ["A primary amine warmed with chloroform and ethanolic KOH",
           "Aniline treated with NaNO₂ and HCl at 273–278 K, then with phenol in mildly alkaline solution",
           "N-Methylethanamine shaken with benzenesulphonyl chloride",
           "Aniline treated with bromine water at room temperature"],
          ["White precipitate", "Foul-smelling product", "Orange dye", "Product insoluble in aqueous alkali"],
          "II III IV I", ["II I IV III", "III II IV I", "II III I IV"], "A"),
      "Tests for amines",
      "Primary amines give foul-smelling isocyanides (carbylamine test). Aniline is diazotised and the diazonium salt "
      "couples with phenol to give orange p-hydroxyazobenzene. A secondary amine gives an N,N-dialkylsulphonamide, "
      "which has no acidic H on nitrogen and is insoluble in alkali. Aniline and bromine water give a white precipitate "
      "of 2,4,6-tribromoaniline.",
      ["Carbylamine: foul smell (II)", "Diazotisation + coupling: orange dye (III)",
       "Hinsberg with 2° amine: alkali-insoluble product (IV)", "Bromine water: white precipitate (I)"],
      why_others_wrong="Codes that give the secondary amine a white precipitate or the coupling reaction a foul smell "
                       "mix up the tests.",
      ncert=f"{NC12}, 'Amines', chemical reactions and tests", seconds=45),

    Q(T_NI, "Diazonium salts", "Advanced", "multi_statement",
      *ms("1,3,5-Tribromobenzene cannot be made by direct bromination of benzene, but it can be made from aniline. "
          "Which of the following statements about this conversion are correct?",
          [("Aniline reacts with bromine water at room temperature to give 2,4,6-tribromoaniline.", True),
           ("2,4,6-Tribromoaniline is diazotised with NaNO₂ and HCl at 273–278 K.", True),
           ("The diazonium group is then replaced by hydrogen using hypophosphorous acid (H₃PO₂).", True),
           ("Direct bromination of benzene with excess Br₂ and FeBr₃ gives 1,3,5-tribromobenzene, because bromine is "
            "a meta-directing group.", False),
           ("In bromine water, the –NH₂ group directs bromine mainly to the meta positions.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
      "Using the –NH₂ group as a temporary directing group",
      "Bromine on a benzene ring is ortho/para directing, so direct bromination cannot give the 1,3,5 pattern. The "
      "strongly activating, ortho/para-directing –NH₂ group places three Br atoms at 2, 4 and 6, which are mutually "
      "meta. The –NH₂ group is then removed: diazotisation followed by H₃PO₂ replaces –N₂⁺ by –H.",
      ["(a) true", "(b) true", "(c) true: ArN₂⁺ + H₃PO₂ + H₂O → ArH + N₂ + H₃PO₃ + H⁺",
       "(d) false: Br is ortho/para directing", "(e) false: –NH₂ is ortho/para directing"],
      ncert=f"{NC12}, 'Amines', diazonium salts: replacement by hydrogen; bromination of aniline", seconds=70),

    Q(T_NI, "Diazonium salts", "Advanced", "assertion_reason",
      *ar("Benzenediazonium chloride is prepared at 273–278 K and used immediately after preparation.", True,
          "Benzenediazonium chloride couples with phenol to give an orange azo dye.", True),
      "Stability and reactions of diazonium salts",
      "Arenediazonium salts are stable only for a short time and only at low temperature, so they are made in ice-cold "
      "solution and used at once. R states a true reaction of the salt (coupling), but coupling has nothing to do "
      "with why the salt must be kept cold and used immediately.",
      ["A: true (low stability)", "R: true (coupling reaction), not the reason for A"],
      ncert=f"{NC12}, 'Amines', diazonium salts: preparation and properties", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "Benzamide is reduced with lithium aluminium hydride to give X. X is treated with NaNO₂ and dilute HCl. The main "
      "organic product is:",
      ["Phenol", "Benzenediazonium chloride", "Aniline", "Benzyl alcohol"], "D",
      "Reduction of amides; nitrous acid and primary amines",
      "LiAlH₄ reduces the amide C=O to CH₂ without losing carbon, so benzamide gives benzylamine, C₆H₅CH₂NH₂, a "
      "primary amine with –NH₂ on an sp³ carbon. Like aliphatic primary amines, it reacts with nitrous acid with loss "
      "of N₂ to give the alcohol. (Hofmann degradation with Br₂/NaOH would instead give aniline, which forms a stable "
      "diazonium salt.)",
      ["C₆H₅CONH₂ + 4[H] (LiAlH₄) → C₆H₅CH₂NH₂ + H₂O", "C₆H₅CH₂NH₂ + HNO₂ → C₆H₅CH₂OH + N₂ + H₂O",
       "Product: benzyl alcohol"],
      why_others_wrong="Aniline, its diazonium salt and phenol all come from the Hofmann route, which removes the "
                       "carbonyl carbon; LiAlH₄ keeps it.",
      ncert=f"{NC12}, 'Amines', preparation by reduction of amides; reaction with nitrous acid", seconds=60),
]
