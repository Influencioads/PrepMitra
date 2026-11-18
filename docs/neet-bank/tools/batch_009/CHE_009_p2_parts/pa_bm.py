
# ================================================================ Biomolecules (Chemistry) (2234-2243)
# 2234: fat-soluble vitamins in the list
fat_soluble = {"A": True, "B1": False, "C": False, "D": True, "E": True, "K": True, "B12": False}
v_2234 = str(sum(fat_soluble.values()))
assert v_2234 == "4"
# 2237: moles of glucose from 1 mol each of maltose, sucrose, lactose
glucose_units = {"maltose": 2, "sucrose": 1, "lactose": 1}
v_2237 = str(sum(glucose_units.values()))
assert v_2237 == "4"

QUESTIONS += [
    N(T_BM, "Vitamins", "Basic",
      "How many of the following vitamins are fat soluble?\nA, B₁, C, D, E, K, B₁₂",
      ["3", v_2234, "5", "6"], "B", v_2234,
      "Fat-soluble and water-soluble vitamins",
      "Vitamins A, D, E and K are fat soluble and are stored in the liver and adipose tissue. The B group vitamins and "
      "vitamin C are water soluble.",
      ["Fat soluble: A, D, E, K", "Water soluble: B₁, B₁₂, C", "Count = 4"],
      why_others_wrong="3 leaves out one of A, D, E, K; 5 or 6 wrongly include vitamin B₁₂ or C.",
      ncert=f"{NC12}, 'Biomolecules', classification of vitamins", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "direct",
      "Increased blood clotting time is caused by a deficiency of:",
      ["Vitamin A", "Vitamin B₁", "Vitamin K", "Vitamin D"], "C",
      "Vitamin deficiency diseases",
      "NCERT's table of vitamins links vitamin K deficiency with an increased blood clotting time.",
      ["Vitamin K: needed for normal blood clotting", "Deficiency → increased clotting time"],
      why_others_wrong="Vitamin A deficiency causes xerophthalmia and night blindness, vitamin B₁ deficiency beri beri, "
                       "and vitamin D deficiency rickets and osteomalacia.",
      ncert=f"{NC12}, 'Biomolecules', vitamins: deficiency diseases", seconds=20),

    Q(T_BM, "Amino acids and proteins", "Basic", "statement_pair",
      *sp("In the α-helix, a polypeptide chain twists into a right-handed screw, with the –NH group of each amino acid "
          "residue hydrogen bonded to the >C=O of an adjacent turn.", True,
          "In the β-pleated sheet, the peptide chains are stretched out nearly to their maximum extension and laid side "
          "by side, held together by intermolecular hydrogen bonds.", True),
      "Secondary structure of proteins",
      "These are NCERT's descriptions of the two common secondary structures. In both, hydrogen bonds between the "
      "–NH and >C=O groups of peptide bonds hold the shape.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Biomolecules', structure of proteins: secondary structure", seconds=30),

    N(T_BM, "Carbohydrates", "Intermediate",
      "One mole each of maltose, sucrose and lactose is hydrolysed completely. The total number of moles of D-glucose "
      "formed is:",
      ["1", "2", "3", v_2237], "D", v_2237,
      "Composition of disaccharides",
      "Maltose is made of two glucose units; sucrose of one glucose and one fructose unit; lactose of one galactose and "
      "one glucose unit.",
      ["Maltose → 2 glucose", "Sucrose → 1 glucose + 1 fructose", "Lactose → 1 galactose + 1 glucose",
       "Total glucose = 2 + 1 + 1 = 4 mol"],
      why_others_wrong="3 counts maltose as giving only one glucose; 2 or 1 forget the glucose units in sucrose or "
                       "lactose.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides", seconds=40),

    Q(T_BM, "Carbohydrates", "Intermediate", "direct",
      "In the name D-(+)-glucose, the sign '(+)' indicates that glucose:",
      ["has its –OH group on the right at the lowest asymmetric carbon",
       "is dextrorotatory, rotating plane-polarised light to the right",
       "is a reducing sugar", "has a positive charge in solution"], "B",
      "D/L and (+)/(−) notation",
      "The letter D refers to the configuration (related to glyceraldehyde), while (+) or (−) gives the experimentally "
      "observed direction of optical rotation. The two are independent: D-fructose, for example, is laevorotatory.",
      ["'D': relative configuration", "'(+)': dextrorotatory"],
      why_others_wrong="The –OH on the right at the lowest asymmetric carbon is what 'D' means, not '(+)'; the sign "
                       "says nothing about reducing behaviour or charge.",
      ncert=f"{NC12}, 'Biomolecules', glucose: D- and L- configuration", seconds=30),

    Q(T_BM, "Carbohydrates", "Intermediate", "assertion_reason",
      *ar("Glucose pentaacetate does not react with hydroxylamine.", True,
          "In the pentaacetate the –OH at C-1 of the cyclic (hemiacetal) form is acetylated, so the ring cannot open "
          "to give a free –CHO group.", True, explains=True),
      "Evidence for the cyclic structure of glucose",
      "Glucose itself forms an oxime because its ring opens to the free aldehyde in solution. In the pentaacetate the "
      "anomeric –OH is converted into an acetate, the hemiacetal cannot open, and no free –CHO is available. NCERT uses "
      "this as evidence for the cyclic structure. R explains A.",
      ["Glucose ⇌ open chain (free CHO) → oxime", "Pentaacetate: C-1 –OH acetylated → ring locked",
       "→ no reaction with NH₂OH"],
      ncert=f"{NC12}, 'Biomolecules', cyclic structure of glucose", seconds=45),

    Q(T_BM, "Carbohydrates", "Intermediate", "match_list",
      *ml("Match the carbohydrate in List-I with the glycosidic linkage found in it (List-II).",
          ["Maltose", "Lactose", "Sucrose", "Amylopectin (at the branch points)"],
          ["C1 of α-D-glucose to C2 of β-D-fructose", "C1–C6 linkage between α-D-glucose units",
           "C1 of α-D-glucose to C4 of another glucose unit", "C1 of β-D-galactose to C4 of β-D-glucose"],
          "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D"),
      "Glycosidic linkages in di- and polysaccharides",
      "Maltose: two α-D-glucose units, C1–C4. Lactose: β-D-galactose and β-D-glucose, C1 of galactose to C4 of glucose. "
      "Sucrose: C1 of α-D-glucose to C2 of β-D-fructose, which uses both reducing groups. Amylopectin: C1–C4 in the "
      "chains and C1–C6 at the branches.",
      ["Maltose: III", "Lactose: IV", "Sucrose: I", "Amylopectin branches: II"],
      why_others_wrong="Swapping maltose and lactose ignores that lactose contains galactose; sucrose is the only one "
                       "with a C1–C2 linkage.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides and polysaccharides", seconds=45),

    Q(T_BM, "Carbohydrates", "Advanced", "assertion_reason",
      *ar("Sucrose is dextrorotatory, but after hydrolysis the solution becomes laevorotatory.", True,
          "Both glucose and fructose are laevorotatory.", False),
      "Inversion of cane sugar",
      "Hydrolysis gives equal amounts of D-(+)-glucose (+52.5°) and D-(−)-fructose (−92.4°). Fructose has the larger "
      "rotation, so the mixture is laevorotatory and the change in sign is called inversion. Glucose itself is "
      "dextrorotatory, so R is false.",
      ["Sucrose: +66.5°", "Glucose +52.5°, fructose −92.4°", "Mixture: net laevorotatory (invert sugar)"],
      ncert=f"{NC12}, 'Biomolecules', sucrose: invert sugar", seconds=40),

    Q(T_BM, "Nucleic acids", "Advanced", "match_list",
      *ml("Match the term in List-I with its description in List-II.",
          ["Nucleoside", "Nucleotide", "Phosphodiester linkage", "Complementary base pairing"],
          ["Joins the 5′ and 3′ carbon atoms of the pentose sugars of successive nucleotides",
           "Base + sugar + phosphoric acid (at the 5′ position of the sugar)",
           "Adenine with thymine and guanine with cytosine, through hydrogen bonds", "Base attached to C-1′ of the sugar"],
          "IV II I III", ["II IV I III", "IV II III I", "IV I II III"], "B"),
      "Structure of nucleic acids",
      "A nucleoside is a base joined at the 1′ position of the sugar; a nucleotide also has a phosphate at the 5′ "
      "position. Nucleotides are joined by phosphodiester links between C-5′ and C-3′ of the sugars, and the two "
      "strands of DNA are held together by hydrogen bonds between complementary bases.",
      ["Nucleoside: IV", "Nucleotide: II", "Phosphodiester linkage: I", "Base pairing: III"],
      why_others_wrong="Confusing nucleoside and nucleotide misses the phosphate group; the phosphodiester link joins "
                       "sugars, not bases.",
      ncert=f"{NC12}, 'Biomolecules', nucleic acids: chemical composition and structure", seconds=45),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about carbohydrates are correct?",
          [("Carbohydrates that yield two to ten monosaccharide units on hydrolysis are called oligosaccharides.", True),
           ("Glucose occurs freely in nature as well as in combined form.", True),
           ("Starch is the main storage polysaccharide of plants.", True),
           ("Sucrose is a reducing sugar.", False),
           ("Monosaccharides can be hydrolysed further into simpler polyhydroxy aldehydes or ketones.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
      "Classification and occurrence of carbohydrates",
      "Oligosaccharides give 2–10 monosaccharide units on hydrolysis. Glucose is found free (in fruits, honey) and "
      "combined (in sucrose, starch, cellulose). Starch is the main storage polysaccharide of plants. Sucrose is "
      "non-reducing because the reducing groups of both units form the glycosidic bond, and monosaccharides cannot be "
      "hydrolysed further.",
      ["(a) true", "(b) true", "(c) true", "(d) false: non-reducing", "(e) false: simplest carbohydrates"],
      ncert=f"{NC12}, 'Biomolecules', carbohydrates: classification", seconds=45),
]
