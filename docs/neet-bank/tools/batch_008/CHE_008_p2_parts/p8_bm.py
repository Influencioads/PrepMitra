
# ================================================================ Biomolecules (1978-1990)
# 1979: glucose + HI (prolonged heating) -> n-hexane C6H14 ; 18 g glucose
v_1979 = g(F(18) / mm(C=6, H=12, O=6) * mm(C=6, H=14))
assert v_1979 == "8.6 g"
# 1982: reducing sugars among five
reducing = {"glucose": True, "fructose": True, "sucrose": False, "maltose": True, "lactose": True}
v_1982 = str(sum(reducing.values()))
assert v_1982 == "4"
# 1987: glucose + 5 (CH3CO)2O -> pentaacetate + 5 CH3COOH ; 9.0 g glucose
n_1987 = F(9) / mm(C=6, H=12, O=6)
v_1987 = g(n_1987 * 5 * mm(C=4, H=6, O=3), 2)
assert v_1987 == "25.50 g" and g(n_1987 * mm(C=4, H=6, O=3), 2) == "5.10 g"

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "Which of the following gives only D-glucose on complete hydrolysis?",
      ["Sucrose", "Maltose", "Lactose", "Fructose"], "B",
      "Composition of disaccharides",
      "Maltose is made of two α-D-glucose units, so its hydrolysis gives only glucose. Sucrose gives glucose and "
      "fructose; lactose gives galactose and glucose; fructose is a monosaccharide and is not hydrolysed.",
      ["Maltose → 2 glucose", "Sucrose → glucose + fructose", "Lactose → galactose + glucose"],
      why_others_wrong="Sucrose and lactose each give a second sugar; fructose cannot be hydrolysed.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides", seconds=20),

    N(T_BM, "Carbohydrates", "Basic",
      "On prolonged heating with HI, glucose is converted into n-hexane. The mass of n-hexane obtained from 18 g of "
      "glucose, assuming complete conversion, is (C = 12, H = 1, O = 16):",
      ["18.0 g", "4.3 g", "17.2 g", "8.6 g"], "D", v_1979,
      "Evidence for the straight chain of glucose",
      "One molecule of glucose (six carbons in a straight chain) gives one molecule of n-hexane, C₆H₁₄.",
      ["n(glucose) = 18/180 = 0.10 mol", "n(C₆H₁₄) = 0.10 mol; M = 86", "Mass = 8.6 g"],
      why_others_wrong="18.0 g repeats the mass of glucose; 4.3 g and 17.2 g halve or double the 1 : 1 ratio.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose", seconds=35),

    Q(T_BM, "Carbohydrates", "Basic", "statement_pair",
      *sp("Carbohydrates are classified as monosaccharides, oligosaccharides and polysaccharides according to their "
          "behaviour on hydrolysis.", True,
          "A monosaccharide that contains an aldehyde group is called an aldose.", True),
      "Classification of carbohydrates",
      "Monosaccharides cannot be hydrolysed further, oligosaccharides give two to ten monosaccharide units and "
      "polysaccharides give a large number. A monosaccharide with –CHO is an aldose; one with a keto group is a "
      "ketose. Both statements are true.",
      ["Classification by hydrolysis → true", "Aldehyde group → aldose → true"],
      ncert=f"{NC12}, 'Biomolecules', classification of carbohydrates", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "match_list",
      *ml("Match the vitamin in List-I with its chemical name in List-II.",
          ["Vitamin B₁", "Vitamin B₂", "Vitamin B₆", "Vitamin C"],
          ["Ascorbic acid", "Pyridoxine", "Thiamine", "Riboflavin"],
          "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "D"),
      "Names of vitamins",
      "Vitamin B₁ is thiamine, B₂ riboflavin, B₆ pyridoxine and C ascorbic acid.",
      ["B₁ → thiamine (III)", "B₂ → riboflavin (IV)", "B₆ → pyridoxine (II)", "C → ascorbic acid (I)"],
      why_others_wrong="The other codes swap thiamine and riboflavin, or riboflavin and pyridoxine, or pyridoxine and "
                       "ascorbic acid.",
      ncert=f"{NC12}, 'Biomolecules', vitamins (table of vitamins and their sources)", seconds=30),

    N(T_BM, "Carbohydrates", "Intermediate",
      "How many of the following are reducing sugars?\nGlucose, fructose, sucrose, maltose, lactose",
      ["3", "4", "5", "2"], "B", v_1982,
      "Reducing and non-reducing sugars",
      "A sugar is reducing if it has (or can open to give) a free aldehydic or ketonic group. All monosaccharides are "
      "reducing. In maltose and lactose one unit keeps a free anomeric carbon. In sucrose the reducing groups of both "
      "glucose (C1) and fructose (C2) are used in the glycosidic bond.",
      ["Glucose, fructose: reducing", "Maltose, lactose: reducing", "Sucrose: non-reducing", "Total = 4"],
      why_others_wrong="3 usually leaves out fructose, a ketose that is still a reducing sugar; 5 counts sucrose; 2 "
                       "counts only the monosaccharides.",
      ncert=f"{NC12}, 'Biomolecules', reducing and non-reducing sugars", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "assertion_reason",
      *ar("Glycine is optically inactive.", True,
          "Glycine is a basic amino acid.", False),
      "Structure of glycine",
      "Glycine, H₂N–CH₂–COOH, has R = H, so its α-carbon carries two hydrogen atoms and is not chiral: glycine is "
      "optically inactive (A true). With one amino and one carboxyl group it is a neutral amino acid, not a basic one "
      "(R false).",
      ["α-C of glycine: H, H, NH₂, COOH → not chiral", "One –NH₂ and one –COOH → neutral amino acid"],
      ncert=f"{NC12}, 'Biomolecules', amino acids", seconds=30),

    Q(T_BM, "Nucleic acids", "Intermediate", "match_list",
      *ml("Match the description in List-I with the component of nucleic acids in List-II.",
          ["Purine bases present in both DNA and RNA", "Pyrimidine base present in DNA but not in RNA",
           "Pyrimidine base present in RNA but not in DNA", "Sugar present in DNA"],
          ["Adenine and guanine", "Uracil", "2-Deoxy-D-ribose", "Thymine"],
          "I IV II III", ["I II IV III", "IV I II III", "I IV III II"], "A"),
      "Chemical composition of nucleic acids",
      "DNA contains adenine, guanine, cytosine and thymine with 2-deoxy-D-ribose; RNA contains adenine, guanine, "
      "cytosine and uracil with D-ribose. Adenine and guanine are purines; cytosine, thymine and uracil are "
      "pyrimidines.",
      ["Purines: A, G (I)", "DNA-only pyrimidine: thymine (IV)", "RNA-only pyrimidine: uracil (II)",
       "DNA sugar: 2-deoxy-D-ribose (III)"],
      why_others_wrong="The other codes swap thymine and uracil, or put a base in place of the sugar.",
      ncert=f"{NC12}, 'Biomolecules', nucleic acids: chemical composition", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "multi_statement",
      *ms("Which of the following statements about proteins are correct?",
          [("In fibrous proteins the polypeptide chains run parallel and are held together by hydrogen and "
            "disulphide bonds.", True),
           ("Denaturation of a protein destroys its primary structure.", False),
           ("Keratin is a globular protein.", False),
           ("The spatial arrangement of two or more polypeptide subunits with respect to each other is the "
            "quaternary structure.", True),
           ("A peptide bond is formed between the –COOH group of one amino acid and the –NH₂ group of another, "
            "with the loss of a water molecule.", True)],
          [["a", "b", "d"], ["d", "e"], ["a", "c", "e"]], "D"),
      "Structure of proteins",
      "Fibrous proteins have parallel chains linked by hydrogen and disulphide bonds (keratin, myosin). Denaturation "
      "disturbs the secondary and tertiary structures but leaves the primary structure (sequence) intact. A peptide "
      "bond, –CO–NH–, forms by a condensation that releases water.",
      ["(a) true", "(b) false: primary structure intact", "(c) false: keratin is fibrous", "(d) true", "(e) true"],
      ncert=f"{NC12}, 'Biomolecules', structure of proteins", seconds=50),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "direct",
      "The side chain R of an α-amino acid, H₂N–CH(R)–COOH, is –CH₂–C₆H₄–OH, with the –OH group at the para position "
      "of the benzene ring. The amino acid is:",
      ["Phenylalanine", "Tyrosine", "Tryptophan", "Serine"], "B",
      "Side chains of α-amino acids",
      "Tyrosine has a p-hydroxybenzyl side chain. Phenylalanine has a benzyl side chain without –OH; serine has "
      "–CH₂OH; tryptophan has an indole-containing side chain.",
      ["–CH₂–C₆H₄–OH (p) → tyrosine"],
      why_others_wrong="Phenylalanine lacks the –OH; serine has no ring; tryptophan's ring contains nitrogen (indole).",
      ncert=f"{NC12}, 'Biomolecules', amino acids (table of natural amino acids)", seconds=30),

    N(T_BM, "Carbohydrates", "Advanced",
      "Glucose reacts with acetic anhydride to form glucose pentaacetate, every –OH group being acetylated. The "
      "minimum mass of acetic anhydride, (CH₃CO)₂O, needed to convert 9.0 g of glucose completely into its "
      "pentaacetate is (C = 12, H = 1, O = 16):",
      ["25.50 g", "5.10 g", "15.00 g", "12.75 g"], "A", v_1987,
      "Five –OH groups in glucose",
      "Each –OH group is acetylated by one molecule of acetic anhydride, which also gives one molecule of ethanoic "
      "acid. Glucose has five –OH groups.",
      ["n(glucose) = 9.0/180 = 0.05 mol", "n(anhydride) = 5 × 0.05 = 0.25 mol", "M[(CH₃CO)₂O] = 102 g mol⁻¹",
       "Mass = 0.25 × 102 = 25.50 g"],
      why_others_wrong="5.10 g assumes one anhydride per glucose; 15.00 g is the mass of ethanoic acid formed "
                       "(0.25 × 60); 12.75 g counts one anhydride per two –OH groups.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose (acetylation)", seconds=60),

    Q(T_BM, "Carbohydrates", "Advanced", "assertion_reason",
      *ar("Lactose is a reducing sugar.", True,
          "Lactose is found in milk.", True, explains=False),
      "Reducing nature of lactose",
      "In lactose, C1 of β-D-galactose is linked to C4 of β-D-glucose, so the glucose unit keeps a free anomeric "
      "carbon (C1) that can open to an aldehyde: lactose is reducing. Its occurrence in milk is true, but it says "
      "nothing about its reducing property.",
      ["Galactose C1 → glucose C4: glucose C1 free → reducing (A true)", "Milk sugar (R true)", "R does not explain A"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides: lactose", seconds=30),

    Q(T_BM, "Hormones", "Advanced", "statement_pair",
      *sp("Hormones are molecules that act as intercellular messengers; they are produced by endocrine glands and "
          "carried by the blood to their target sites.", True,
          "All hormones are steroids.", False),
      "General introduction to hormones",
      "Hormones are chemical messengers released by endocrine glands into the blood. Chemically they are of different "
      "kinds: steroids (e.g. oestrogens, androgens), polypeptides (e.g. insulin) and amino acid derivatives (e.g. "
      "epinephrine, thyroxine). So Statement II is false.",
      ["Statement I: definition → true", "Insulin is a polypeptide, thyroxine an amino acid derivative → II false"],
      ncert=f"{NC12}, 'Biomolecules', hormones (general introduction)", seconds=30),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about glucose and its cyclic (hemiacetal) structure are correct?",
          [("Glucose does not give the 2,4-DNP test, although it contains an aldehyde group in its open-chain form.",
            True),
           ("Glucose does not form a hydrogensulphite addition product with NaHSO₃.", True),
           ("In the six-membered ring of glucose, the ring is closed by the –OH group at C-5 adding to the –CHO "
            "group.", True),
           ("Oxidation of glucose by bromine water gives saccharic acid.", False),
           ("The α and β forms of glucose differ in the configuration at C-1, which becomes a new chiral centre on "
            "ring formation.", True)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "d", "e"]], "D"),
      "Cyclic structure of glucose",
      "The open-chain formula could not explain why glucose does not give the 2,4-DNP test or Schiff's test and does "
      "not form a NaHSO₃ adduct. The C-5 –OH adds to the –CHO group to give a six-membered (pyranose) ring, and C-1 "
      "becomes chiral, giving the α and β anomers. Bromine water oxidises glucose to gluconic acid, not saccharic "
      "acid, and this is a property of the aldehyde group, not evidence for the ring.",
      ["(a) true", "(b) true", "(c) true", "(d) false: gluconic acid", "(e) true"],
      ncert=f"{NC12}, 'Biomolecules', cyclic structure of glucose", seconds=60),
]
