
# ================================================================ Biomolecules (Chemistry) (2478-2490)
# 2482: linear double-stranded DNA of 50 base pairs: each strand of 50 nucleotides has 49 phosphodiester links
v_2482 = str(2 * (50 - 1))
assert v_2482 == "98"
# 2487: ds DNA, 1000 nucleotides (500 bp), 22% G -> G = C = 220 -> 220 G-C pairs, 280 A-T pairs
nuc, pg = 1000, F(22, 100)
g = nuc * pg
gc_pairs = g
at_pairs = nuc // 2 - gc_pairs
hb_2487 = 2 * at_pairs + 3 * gc_pairs
assert (g, at_pairs, hb_2487) == (220, 280, 1220)
assert 2 * 220 + 3 * 280 == 1280 and 2 * 390 + 3 * 110 == 1110 and 3 * 500 == 1500
v_2487 = str(hb_2487)

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "According to NCERT, amylose is a long unbranched chain of α-D-(+)-glucose units held together by C1–C4 "
      "glycosidic linkages. The number of glucose units in such a chain is about:",
      ["2 to 10", "20 to 50", "200 to 1000", "50,000 to 100,000"], "C",
      "Structure of amylose",
      "Amylose, the water-soluble component (15–20%) of starch, is a long unbranched chain of 200–1000 "
      "α-D-(+)-glucose units joined by C1–C4 glycosidic linkages.",
      ["Amylose: unbranched, C1–C4, 200–1000 glucose units"],
      why_others_wrong="2 to 10 units defines an oligosaccharide; 20 to 50 and 50,000 to 100,000 are not the "
                       "figures NCERT gives for amylose.",
      ncert=f"{NC12}, 'Biomolecules', polysaccharides: starch", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "match_list",
      *ml("Match the vitamin in List-I with its sources, as given in NCERT, in List-II.",
          ["Vitamin A", "Vitamin B₁ (thiamine)", "Vitamin B₂ (riboflavin)", "Vitamin K"],
          ["Green leafy vegetables", "Milk, egg white, liver, kidney", "Fish liver oil, carrots, butter and milk",
           "Yeast, milk, green vegetables and cereals"],
          "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "D"),
      "Sources of vitamins",
      "NCERT's table of vitamins lists: A — fish liver oil, carrots, butter and milk; B₁ — yeast, milk, green "
      "vegetables and cereals; B₂ — milk, egg white, liver, kidney; K — green leafy vegetables.",
      ["A → III", "B₁ → IV", "B₂ → II", "K → I"],
      why_others_wrong="Codes that swap B₁ and B₂ or A and B₁ mix up two lists that both contain milk; the last code "
                       "gives vitamin K the animal sources of riboflavin.",
      ncert=f"{NC12}, 'Biomolecules', vitamins: sources and deficiency diseases", seconds=40),

    Q(T_BM, "Amino acids and proteins", "Basic", "statement_pair",
      *sp("In the zwitter ionic form, amino acids show amphoteric behaviour, as they react with both acids and "
          "bases.", True,
          "Most naturally occurring α-amino acids have the L-configuration.", True),
      "Properties of amino acids",
      "In water the –COOH group loses a proton and the –NH₂ group gains one, giving a dipolar ion (zwitterion). It "
      "can accept a proton (acting as a base) through –COO⁻ or give one (acting as an acid) through –NH₃⁺. All "
      "naturally occurring α-amino acids except glycine are optically active, and most of them have the "
      "L-configuration.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Biomolecules', amino acids: properties", seconds=30),

    Q(T_BM, "Carbohydrates", "Basic", "assertion_reason",
      *ar("Sucrose reduces Tollens' reagent.", False,
          "On hydrolysis, sucrose gives glucose and fructose.", True),
      "Non-reducing nature of sucrose",
      "In sucrose, C1 of α-D-glucose is joined to C2 of β-D-fructose, so the reducing groups of both units are used "
      "up in the glycosidic bond; sucrose is a non-reducing sugar and does not reduce Tollens' reagent. R is a true "
      "statement about its hydrolysis (to invert sugar). A is false.",
      ["A: false (non-reducing sugar)", "R: true"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides: sucrose", seconds=30),

    N(T_BM, "Nucleic acids", "Intermediate",
      "In a nucleic acid strand, successive nucleotides are joined by phosphodiester linkages between the 5′ and 3′ "
      "carbon atoms of their pentose sugars. How many phosphodiester linkages are present in a linear, "
      "double-stranded DNA segment of 50 base pairs?",
      ["49", v_2482, "50", "100"], "B", v_2482,
      "Phosphodiester linkages in a polynucleotide",
      "A linear strand of n nucleotides has n − 1 linkages between neighbouring nucleotides. A double-stranded "
      "segment of 50 base pairs has two strands of 50 nucleotides each. Base pairing between the strands is by "
      "hydrogen bonds, not phosphodiester linkages.",
      ["One strand: 50 − 1 = 49", "Two strands: 2 × 49 = 98"],
      why_others_wrong="49 counts only one strand; 50 and 100 count one linkage per nucleotide, which would be true "
                       "only for a circular strand.",
      ncert=f"{NC12}, 'Biomolecules', structure of nucleic acids", seconds=45),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "direct",
      "In the dipeptide glycylalanine (Gly–Ala), the carboxyl group of glycine is joined to the amino group of "
      "alanine. By the same convention, in the tripeptide Gly–Ala–Val, the amino acid residue that carries the free "
      "α-amino (–NH₂) group is:",
      ["Glycine", "Alanine", "Valine", "None; all the α-amino groups are used in peptide bonds"], "A",
      "Writing peptides",
      "In Gly–Ala–Val, the –COOH of glycine forms a peptide bond with the –NH₂ of alanine, and the –COOH of alanine "
      "with the –NH₂ of valine. The –NH₂ of glycine remains free, and the –COOH of valine remains free.",
      ["Gly(–NH₂ free)–CO–NH–Ala–CO–NH–Val(–COOH free)"],
      why_others_wrong="Alanine's amino group and valine's amino group are both used in peptide bonds; a linear "
                       "peptide always keeps one free amino group at one end.",
      ncert=f"{NC12}, 'Biomolecules', proteins: peptide bond", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "assertion_reason",
      *ar("A protein loses its biological activity on denaturation.", True,
          "During denaturation, the secondary and tertiary structures of the protein are destroyed, although its "
          "primary structure remains intact.", True, explains=True),
      "Denaturation of proteins",
      "A native protein owes its biological activity to its unique three-dimensional structure. A change in "
      "temperature or pH disturbs the hydrogen bonds; the globules unfold and the helix uncoils, destroying the "
      "secondary and tertiary structures, and the protein loses its biological activity. R explains A.",
      ["Activity depends on the 3-D (2° and 3°) structure", "Denaturation destroys 2° and 3° structure → activity lost"],
      ncert=f"{NC12}, 'Biomolecules', denaturation of proteins", seconds=35),

    Q(T_BM, "Carbohydrates", "Intermediate", "statement_pair",
      *sp("Glycogen is less highly branched than amylopectin.", False,
          "Cellulose is a straight-chain polysaccharide made of α-D-glucose units.", False),
      "Glycogen and cellulose",
      "Glycogen, the animal starch, has a structure similar to amylopectin but is more highly branched. Cellulose "
      "is a straight-chain polysaccharide made only of β-D-glucose units, joined by glycosidic linkages between C1 "
      "of one unit and C4 of the next.",
      ["Statement I: false (glycogen is more branched)", "Statement II: false (β-D-glucose)"],
      ncert=f"{NC12}, 'Biomolecules', polysaccharides: cellulose and glycogen", seconds=35),

    Q(T_BM, "Nucleic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about nucleic acids are correct?",
          [("Nucleic acids are long-chain polymers of nucleotides and are therefore also called polynucleotides.",
            True),
           ("The sugar in DNA is β-D-2-deoxyribose, whereas the sugar in RNA is β-D-ribose.", True),
           ("Cytosine is present in both DNA and RNA.", True),
           ("In a nucleotide, the phosphoric acid is linked to the 1′ position of the pentose sugar.", False),
           ("A nucleoside contains a base, a pentose sugar and a phosphate group.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "D"),
      "Chemical composition of nucleic acids",
      "Nucleic acids are polynucleotides. DNA contains β-D-2-deoxyribose and RNA β-D-ribose; cytosine and the two "
      "purines occur in both, while thymine is only in DNA and uracil only in RNA. The base is attached at C-1′ of "
      "the sugar (nucleoside); the phosphoric acid is esterified at C-5′ (nucleotide).",
      ["(a) true", "(b) true", "(c) true", "(d) false: phosphate at 5′", "(e) false: that is a nucleotide"],
      why_others_wrong="Options with (d) put the phosphate where the base is attached; options with (e) confuse a "
                       "nucleoside with a nucleotide.",
      ncert=f"{NC12}, 'Biomolecules', chemical composition and structure of nucleic acids", seconds=50),

    N(T_BM, "Nucleic acids", "Advanced",
      "A linear double-stranded DNA molecule contains 1000 nucleotides, of which 22% are guanine. An A–T pair is "
      "held by two hydrogen bonds and a G–C pair by three. The total number of hydrogen bonds between the two "
      "strands is:",
      [v_2487, "1110", "1280", "1500"], "A", v_2487,
      "Complementary base pairing",
      "In double-stranded DNA, G pairs with C and A with T, so the number of G–C pairs equals the number of G "
      "nucleotides. 1000 nucleotides make 500 base pairs.",
      ["G = 22% of 1000 = 220 → 220 G–C pairs", "A–T pairs = 500 − 220 = 280",
       "H bonds = 2 × 280 + 3 × 220 = 560 + 660 = 1220"],
      why_others_wrong="1280 swaps the numbers of A–T and G–C pairs; 1110 takes 22% of the 500 pairs as G–C pairs; "
                       "1500 assumes three hydrogen bonds for every pair.",
      ncert=f"{NC12}, 'Biomolecules', structure of DNA", seconds=75),

    Q(T_BM, "Carbohydrates", "Advanced", "match_list",
      *ml("Match the carbohydrate in List-I with the product(s) of its complete hydrolysis in List-II.",
          ["Sucrose", "Lactose", "Cellulose", "Amylose"],
          ["α-D-Glucose only", "D-Glucose and D-galactose", "D-Glucose and D-fructose", "β-D-Glucose only"],
          "III II IV I", ["III II I IV", "II III IV I", "III IV II I"], "C"),
      "Monosaccharide units of di- and polysaccharides",
      "Sucrose is made of α-D-glucose and β-D-fructose; lactose of β-D-galactose and β-D-glucose; cellulose only of "
      "β-D-glucose units; amylose only of α-D-glucose units.",
      ["Sucrose → glucose + fructose", "Lactose → galactose + glucose", "Cellulose → β-D-glucose",
       "Amylose → α-D-glucose"],
      why_others_wrong="Swapping cellulose and amylose confuses the α and β linkages of starch and cellulose; "
                       "swapping sucrose and lactose mixes up fructose and galactose.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides and polysaccharides", seconds=50),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following conclusions about the structure of glucose are correctly drawn from the "
          "observation stated?",
          [("Glucose forms a pentaacetate with acetic anhydride, so it contains five –OH groups.", True),
           ("Prolonged heating with HI gives n-hexane, so the six carbon atoms are linked in a straight chain.",
            True),
           ("Glucose exists in two crystalline forms, α and β, which the open-chain structure cannot explain.", True),
           ("α-D-Glucose and β-D-glucose differ in the configuration at C-5.", False),
           ("Bromine water oxidises glucose to gluconic acid, so glucose contains a ketonic carbonyl group.", False)],
          [["a", "b", "d"], ["c", "d", "e"], ["a", "b", "c", "e"]], "B"),
      "Evidence for the structure of glucose",
      "Acetylation to a pentaacetate shows five –OH groups; reduction to n-hexane shows a straight six-carbon chain; "
      "the α and β forms (anomers) need the cyclic hemiacetal structure. The anomers differ at C-1, the anomeric "
      "carbon. Oxidation by the mild oxidant bromine water to gluconic acid, a six-carbon acid, shows an aldehyde "
      "group.",
      ["(a) true", "(b) true", "(c) true", "(d) false: they differ at C-1", "(e) false: an aldehyde group"],
      why_others_wrong="Options with (d) put the anomeric difference at the ring-closing carbon C-5; options with (e) "
                       "reverse the meaning of the bromine water test.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose", seconds=70),

    Q(T_BM, "Amino acids and proteins", "Advanced", "multi_statement",
      *ms("Which of the following statements about the structure of proteins are correct?",
          [("The primary structure is the sequence of amino acids, and any change in this sequence creates a "
            "different protein.", True),
           ("Quaternary structure is found only in proteins made up of two or more polypeptide chains (subunits).",
            True),
           ("Denaturation of a protein hydrolyses its peptide bonds.", False),
           ("In the α-helix, the –NH group of each amino acid residue is hydrogen bonded to the >C=O of an adjacent "
            "turn of the helix.", True),
           ("Globular proteins such as insulin are usually insoluble in water.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "C"),
      "Levels of protein structure",
      "Primary structure = amino acid sequence; changing it gives a different protein. Quaternary structure is the "
      "spatial arrangement of two or more subunits. In the α-helix, the chain twists into a right-handed screw with "
      "–NH···O=C hydrogen bonds between successive turns. Denaturation destroys 2° and 3° structure but leaves the "
      "peptide bonds (primary structure) intact. Globular proteins are usually water soluble.",
      ["(a) true", "(b) true", "(c) false", "(d) true", "(e) false"],
      why_others_wrong="Options with (c) treat denaturation as hydrolysis; the option with (e) gives globular proteins "
                       "the solubility of fibrous ones.",
      ncert=f"{NC12}, 'Biomolecules', structure of proteins", seconds=60),
]
