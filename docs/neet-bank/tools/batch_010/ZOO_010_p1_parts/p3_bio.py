

# ================================================================ Biomolecules (B5 I7 A5)
R_BIO = lambda s: ref("Biomolecules", s)

Z(BIO, "Proteins and amino acids", "Basic", "direct",
  "An amino acid is a substituted methane whose α-carbon carries a hydrogen, an amino group, a carboxyl group and a "
  "variable group R. If R is a methyl (–CH₃) group, the amino acid is:",
  ["Glycine", "Serine", "Alanine", "Lysine"], "C",
  "R groups of amino acids",
  "NCERT: the R group in the proteinaceous amino acids could be a hydrogen (glycine), a methyl group (alanine), a "
  "hydroxy methyl (serine), etc.",
  ["Glycine → H", "Alanine → methyl", "Serine → hydroxy methyl"],
  R_BIO("analysis of chemical composition – amino acids"),
  why_others_wrong="A has hydrogen as its R group and B a hydroxy methyl group; D is a basic amino acid, not one "
                   "with a methyl R group.",
  seconds=20)

Z(BIO, "Proteins and amino acids", "Basic", "statement_pair",
  sp("Trypsin and insulin are both proteins.",
     "Trypsin acts as a hormone, whereas insulin acts as an enzyme."),
  STATEMENT_PAIR, "C",
  "Functions of proteins",
  "NCERT's table of proteins lists trypsin as an enzyme and insulin as a hormone; both are proteins. Statement II "
  "reverses their functions.",
  ["Statement I → true", "Statement II → false: trypsin is the enzyme and insulin the hormone"],
  R_BIO("proteins"),
  why_others_wrong="A and D accept the reversed functions; B rejects the true Statement I.",
  seconds=25)

Z(BIO, "Carbohydrates and lipids", "Basic", "assertion_reason",
  ar("Gingelly oil remains as an oil (liquid) in winter.",
     "Oils have a lower melting point than fats."),
  ASSERTION_REASON, "A",
  "Fats and oils",
  "NCERT: triglycerides are called fats or oils on the basis of melting point. Oils have a lower melting point "
  "(e.g., gingelly oil) and hence remain as oil in winters. The low melting point is exactly why the oil stays liquid "
  "in the cold – R explains A.",
  ["A → true", "R → true", "Low melting point → stays liquid in winter → R explains A"],
  R_BIO("analysis of chemical composition – lipids"),
  why_others_wrong="B misses NCERT's direct 'hence'; C and D reject true statements.",
  seconds=25)

Z(BIO, "Nucleic acids", "Basic", "match_list",
  ml(("compound", "category"), ["Alanine", "Ribose", "Guanine", "Palmitic acid"],
     ["Fatty acid", "Nitrogen base (a substituted purine)", "Amino acid", "Sugar (a pentose)"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "B"), "B",
  "Small organic molecules of the acid-soluble pool",
  "NCERT: alanine is an amino acid; ribose is a sugar (a pentose; glucose is a hexose); guanine, like adenine, is a "
  "substituted purine; palmitic acid is a fatty acid with 16 carbon atoms including the carboxyl carbon.",
  ["Alanine → III", "Ribose → IV", "Guanine → II", "Palmitic acid → I"],
  R_BIO("analysis of chemical composition"),
  why_others_wrong="A swaps the amino acid and the sugar; C swaps the base and the fatty acid; D swaps the sugar and "
                   "the base.",
  seconds=30)

_ratio = 18.5 / 0.03
assert abs(_ratio - 617) < 1
Z(BIO, "Carbohydrates and lipids", "Basic", "numerical",
  "NCERT compares the percentage by weight of elements in the earth's crust and in the human body. Take carbon as "
  "0.03 per cent of the earth's crust and 18.5 per cent of the human body. By about what factor is the relative "
  "abundance of carbon greater in the human body than in the earth's crust?",
  ["About 61.7", "About 6170", "About 1.6 × 10⁻³", "About 617"], "D",
  "Relative abundance of carbon in living matter",
  "NCERT points out that the relative abundance of carbon and hydrogen with respect to other elements is higher in "
  "any living organism than in the earth's crust. Using the given values, the factor is 18.5 / 0.03 ≈ 617.",
  ["Factor = % in body / % in crust", "= 18.5 / 0.03", "≈ 617"],
  R_BIO("analysis of chemical composition – Table: comparison of elements in earth's crust and human body"),
  shortcut="18.5 / 0.03 = 1850 / 3 ≈ 617.",
  why_others_wrong="A and B misplace the decimal point by a factor of 10; C inverts the ratio (crust / body).",
  seconds=40, verified_by=RECOMPUTED)

Z(BIO, "Nucleic acids", "Intermediate", "direct",
  "Which of the following is a nucleoside whose nitrogenous base is a substituted pyrimidine?",
  ["Thymidine", "Adenosine", "Guanosine", "Cytidylic acid"], "A",
  "Nucleosides and nucleotides",
  "NCERT: adenine and guanine are substituted purines; uracil, cytosine and thymine are substituted pyrimidines. A "
  "base attached to a sugar is a nucleoside (adenosine, guanosine, thymidine, uridine, cytidine); if a phosphate is "
  "also esterified to the sugar, it is a nucleotide (adenylic acid, thymidylic acid, guanylic acid, uridylic acid, "
  "cytidylic acid). Thymidine is a nucleoside with the pyrimidine thymine.",
  ["Nucleoside = base + sugar", "Pyrimidine bases → C, T, U", "Thymidine → nucleoside with thymine ✓",
   "Cytidylic acid → pyrimidine, but a nucleotide"],
  R_BIO("analysis of chemical composition – nucleic acids"),
  why_others_wrong="B and C are nucleosides of purines; D has a pyrimidine but carries a phosphate, so it is a "
                   "nucleotide.",
  seconds=35)

_opts = ["(a) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (e) only", "(a), (b) and (c) only"]
Z(BIO, "Enzymes: properties and action", "Intermediate", "multi_statement",
  ms("A human enzyme has an optimum temperature of 37 °C and an optimum pH of 7. Which of the following statements "
     "about it are correct, according to NCERT?",
     ["At 25 °C its activity is lower than at 37 °C.",
      "Kept at 4 °C, it is preserved in a temporarily inactive state.",
      "Heated to 70 °C, it loses its activity because the protein is denatured by heat.",
      "At pH 9 its activity is higher than at pH 7.",
      "Once its maximum velocity (Vmax) is reached, a further rise in substrate concentration raises the velocity "
      "further."]),
  _opts, "D",
  "Temperature, pH and substrate concentration",
  "NCERT: each enzyme shows its highest activity at its optimum temperature and pH, and activity declines both below "
  "and above the optimum. Low temperature preserves the enzyme in a temporarily inactive state, whereas high "
  "temperature destroys enzymatic activity because proteins are denatured by heat. The velocity of the reaction "
  "reaches a maximum (Vmax) that is not exceeded by any further rise in substrate concentration.",
  ["(a) true – below optimum", "(b) true", "(c) true", "(d) false – activity falls above the optimum pH",
   "(e) false – Vmax is not exceeded"],
  R_BIO("enzymes – factors affecting enzyme activity"),
  why_others_wrong="A includes (d); B and C include (e).",
  seconds=50)
ms_check("abc", _opts, "D")

Z(BIO, "Enzymes: properties and action", "Intermediate", "statement_pair",
  sp("Prosthetic groups and co-enzymes are both organic compounds.",
     "Zinc, the co-factor of the proteolytic enzyme carboxypeptidase, is a prosthetic group."),
  STATEMENT_PAIR, "C",
  "Kinds of co-factors",
  "NCERT: co-factors are of three kinds – prosthetic groups (organic compounds tightly bound to the apoenzyme, e.g. "
  "haem in peroxidase and catalase), co-enzymes (organic compounds transiently associated, e.g. NAD, NADP) and metal "
  "ions (e.g. zinc for carboxypeptidase). Zinc is a metal-ion co-factor, not a prosthetic group.",
  ["Statement I → true", "Statement II → false: zinc is a metal ion co-factor"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="A and D call a metal ion a prosthetic group; B rejects the true Statement I.",
  seconds=35)

Z(BIO, "Carbohydrates and lipids", "Intermediate", "assertion_reason",
  ar("Starch gives a blue colour when treated with iodine.",
     "Starch is a store of energy in plant tissues."),
  ASSERTION_REASON, "B",
  "Starch–iodine reaction",
  "NCERT: starch forms helical secondary structures and can hold I₂ molecules in the helical portion; the starch–I₂ "
  "complex is blue. NCERT also states that starch is a store of energy in plant tissues. Being an energy store is a "
  "different property of starch and does not explain the blue colour, which comes from the helices holding iodine.",
  ["A → true (starch–I₂ is blue)", "R → true (energy store in plants)",
   "Colour depends on helices holding I₂, not on storage role → R does not explain A"],
  R_BIO("polysaccharides"),
  why_others_wrong="A gives the wrong reason for the colour; C and D reject true statements.",
  seconds=30)

Z(BIO, "Nucleic acids", "Intermediate", "match_list",
  ml(("term", "description"), ["Homopolymer", "Heteropolymer", "Nucleoside", "Nucleotide"],
     ["Built from only one type of monomer repeated 'n' times, e.g. cellulose",
      "Built from different monomers, e.g. a protein",
      "A nitrogenous base attached to a sugar, e.g. uridine",
      "A phosphate esterified to the sugar of a nucleoside, e.g. guanylic acid"]),
  match_options(M("I", "II", "III", "IV"), [M("II", "I", "III", "IV"), M("I", "II", "IV", "III"),
                                            M("II", "I", "IV", "III")], "A"), "A",
  "Polymers and nucleic-acid building blocks",
  "NCERT: a homopolymer has only one type of monomer repeating 'n' times (cellulose is a homopolymer of glucose), "
  "while proteins are heteropolymers. A nitrogenous base attached to a sugar is a nucleoside (e.g. uridine); if a "
  "phosphate group is also esterified to the sugar, it is a nucleotide (e.g. guanylic acid).",
  ["Homopolymer → I", "Heteropolymer → II", "Nucleoside → III", "Nucleotide → IV"],
  R_BIO("proteins; polysaccharides; nucleic acids"),
  why_others_wrong="B swaps the two kinds of polymer; C swaps nucleoside and nucleotide; D swaps both pairs.",
  seconds=35)

Z(BIO, "Enzyme classification", "Intermediate", "direct",
  "An enzyme links two compounds together by forming a C–S bond between them. In NCERT's classification of enzymes, "
  "it belongs to the class:",
  ["Lyases", "Transferases", "Ligases", "Isomerases"], "C",
  "Ligases",
  "NCERT: ligases catalyse the linking together of two compounds, e.g. enzymes which catalyse the joining of C–O, "
  "C–S, C–N, P–O, etc. bonds. Lyases remove groups leaving double bonds, transferases move a group G (other than "
  "hydrogen) between substrates, and isomerases inter-convert isomers.",
  ["Joining two compounds (C–S bond) → ligase"],
  R_BIO("enzymes – classification and nomenclature"),
  why_others_wrong="A removes groups rather than joining compounds; B transfers a group between two substrates; D "
                   "rearranges a single compound.",
  seconds=30)

_opts = ["(a), (b) and (c) only", "(a), (c) and (d) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"]
Z(BIO, "Proteins and amino acids", "Intermediate", "multi_statement",
  ms("NCERT gives a table of some proteins and their functions. Which of the following protein–function pairs are "
     "correct?",
     ["Collagen – intercellular ground substance", "GLUT-4 – enzyme", "Antibody – fights infectious agents",
      "Receptor – sensory reception (smell, taste, hormone, etc.)", "Trypsin – hormone"]),
  _opts, "B",
  "Functions of some proteins",
  "NCERT's table: collagen – intercellular ground substance; trypsin – enzyme; insulin – hormone; antibody – fights "
  "infectious agents; receptor – sensory reception (smell, taste, hormone, etc.); GLUT-4 – enables glucose transport "
  "into cells.",
  ["(a) correct", "(b) wrong – GLUT-4 enables glucose transport into cells", "(c) correct", "(d) correct",
   "(e) wrong – trypsin is an enzyme"],
  R_BIO("proteins – Table: some proteins and their functions"),
  why_others_wrong="A includes (b); C includes (e); D includes both wrong pairs.",
  seconds=45)
ms_check("acd", _opts, "B")

_items = {"Proteins": True, "Nucleic acids": True, "Polysaccharides": True, "Lipids": False, "Glucose": False,
          "Amino acids": False, "Nucleotides": False}
_opts = ["2", "3", "4", "5"]
Z(BIO, "Carbohydrates and lipids", "Advanced", "direct",
  "A living tissue is ground in trichloroacetic acid and strained. How many of the following would be found in the "
  "acid-insoluble fraction AND have molecular weights in the range of ten thousand daltons and above?\n\n"
  + ", ".join(_items),
  _opts, "B",
  "Acid-soluble and acid-insoluble fractions",
  "NCERT: the acid-insoluble fraction contains proteins, nucleic acids, polysaccharides and lipids. Except lipids, "
  "these have molecular weights of ten thousand daltons and above. Lipids have molecular weights not exceeding about "
  "800 Da; they come into the acid-insoluble fraction only because membranes break into water-insoluble vesicles. "
  "Glucose, amino acids and nucleotides are in the acid-soluble pool (molecular weights about 18 to 800).",
  ["Acid-insoluble → proteins, nucleic acids, polysaccharides, lipids",
   "≥ 10,000 Da → proteins, nucleic acids, polysaccharides (not lipids) = 3"],
  R_BIO("biomacromolecules"),
  why_others_wrong="A drops a macromolecule; C counts the lipids; D also counts a small molecule of the acid-soluble "
                   "pool.",
  seconds=50)
count_check(_items, _opts, "B")

Z(BIO, "Nucleic acids", "Advanced", "statement_pair",
  sp("Removing the phosphate group from adenylic acid leaves adenine.",
     "Thymidine contains a substituted purine."),
  STATEMENT_PAIR, "B",
  "Nucleotide → nucleoside → base",
  "Adenylic acid is a nucleotide (adenine + sugar + phosphate); removing the phosphate leaves the nucleoside "
  "adenosine (adenine + sugar), not the free base adenine. Thymidine is the nucleoside of thymine, which NCERT lists "
  "among the substituted pyrimidines. Both statements are false.",
  ["Statement I → false (gives adenosine)", "Statement II → false (thymine is a pyrimidine)"],
  R_BIO("analysis of chemical composition – nucleic acids"),
  why_others_wrong="A, C and D accept at least one false statement.",
  seconds=40)

Z(BIO, "Carbohydrates and lipids", "Advanced", "match_list",
  ml(("compound", "products of its complete hydrolysis"), ["Lecithin", "A triglyceride", "Cytidylic acid",
                                                           "Cellulose"],
     ["Glucose only", "Cytosine, a pentose sugar and phosphoric acid", "One glycerol and three fatty acids",
      "Glycerol, fatty acids, phosphoric acid and a phosphorylated organic compound"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Building blocks of biomolecules",
  "Lecithin is a phospholipid: besides glycerol and fatty acids it contains phosphorus and a phosphorylated organic "
  "compound. A triglyceride has three fatty acids esterified with one glycerol. Cytidylic acid is a nucleotide – "
  "cytosine, a pentose sugar and phosphate. Cellulose is a homopolymer of glucose.",
  ["Lecithin → IV", "Triglyceride → III", "Cytidylic acid → II", "Cellulose → I"],
  R_BIO("analysis of chemical composition – lipids, nucleotides; polysaccharides"),
  why_others_wrong="A swaps the two lipids; B swaps the nucleotide and cellulose; C swaps the triglyceride and the "
                   "nucleotide.",
  seconds=45)

_opts = ["(a), (b), (c) and (e) only", "(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"]
Z(BIO, "Enzymes: properties and action", "Advanced", "multi_statement",
  ms("Removing a small organic molecule from an enzyme abolishes its activity. NCERT would describe this molecule's "
     "association with the protein as only transient, usually occurring during the course of catalysis. Which of the "
     "following statements are correct?",
     ["The small molecule is a co-enzyme.",
      "It may serve as a co-factor in a number of different enzyme-catalysed reactions.",
      "NAD could be an example of such a molecule.",
      "Haem in peroxidase is another example of this kind of co-factor.",
      "The protein portion left behind is called the apoenzyme."]),
  _opts, "A",
  "Co-enzymes versus prosthetic groups",
  "NCERT: co-enzymes are organic compounds whose association with the apoenzyme is only transient, usually during "
  "catalysis; they serve as co-factors in a number of different enzyme-catalysed reactions; NAD and NADP contain the "
  "vitamin niacin. Prosthetic groups such as haem (in peroxidase and catalase) are tightly bound. The protein portion "
  "of such an enzyme is the apoenzyme, and catalytic activity is lost when the co-factor is removed.",
  ["(a) true", "(b) true", "(c) true", "(d) false – haem is a tightly bound prosthetic group", "(e) true"],
  R_BIO("enzymes – co-factors"),
  why_others_wrong="B and C include (d); D leaves out the correct (b).",
  seconds=55)
ms_check("abce", _opts, "A")

Z(BIO, "Carbohydrates and lipids", "Advanced", "assertion_reason",
  ar("Like cellulose, chitin is a homopolymer of glucose.",
     "Complex polysaccharides, such as chitin of the arthropod exoskeleton, have amino-sugars and chemically modified "
     "sugars as building blocks."),
  ASSERTION_REASON, "D",
  "Chitin compared with cellulose",
  "NCERT: cellulose is a homopolymer of glucose. Complex polysaccharides such as chitin have as building blocks "
  "amino-sugars and chemically modified sugars (e.g. glucosamine, N-acetyl galactosamine). So R is true, while A is "
  "false: chitin is not built of glucose.",
  ["R → true (amino-sugars and modified sugars)", "A → false (chitin's monomer is not glucose)"],
  R_BIO("polysaccharides"),
  why_others_wrong="A and B accept that chitin is made of glucose; C rejects NCERT's statement R.",
  seconds=40)
