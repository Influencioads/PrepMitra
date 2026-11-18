
# =============================================================== 5. Cell: The Unit of Life (5/6/5)
direct(T_CELL, "Nucleus", "Basic",
       "In an interphase nucleus, the nucleoprotein fibres form a loose and indistinct network called chromatin. "
       "During the different stages of cell division, cells instead show:",
       "structured chromosomes in place of the nucleus",
       ["a larger number of nucleoli", "a nuclear envelope with more pores", "chromatin fibres fused with the "
        "endoplasmic reticulum"], "C",
       "Chromatin and chromosomes",
       "The interphase nucleus (a nucleus of a cell when it is not dividing) has highly extended and elaborate "
       "nucleoprotein fibres called chromatin, nuclear matrix and one or more spherical nucleoli. During different "
       "stages of cell division, cells show structured chromosomes in place of the nucleus.",
       ["Interphase: chromatin network", "Division: structured chromosomes in place of the nucleus"],
       why="The other options are not what NCERT describes for dividing cells; the nucleus is replaced by condensed, "
           "structured chromosomes.",
       ncert=ref("CELL", "Nucleus"), secs=25)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In chloroplasts, the light energy essential for photosynthesis is trapped by:",
       "chlorophyll and carotenoid pigments",
       ["the 70S ribosomes of the stroma", "the circular DNA of the stroma",
        "the enzymes of the outer membrane"], "D",
       "Pigments of chloroplasts",
       "Chloroplasts contain chlorophyll and carotenoid pigments, which are responsible for trapping light energy "
       "essential for photosynthesis. The stroma contains enzymes for the synthesis of carbohydrates and proteins, "
       "small double-stranded circular DNA and 70S ribosomes; chlorophyll pigments are present in the thylakoids.",
       ["Light trapping = chlorophyll + carotenoids"],
       why="Ribosomes, DNA and membrane enzymes do not absorb light; they serve protein synthesis, heredity and "
           "metabolism.",
       ncert=ref("CELL", "Plastids"), secs=20)

direct(T_CELL, "Cell theory", "Basic",
       "Cells vary greatly in shape; they may be disc-like, polygonal, columnar, cuboid, thread-like or even "
       "irregular. According to NCERT, the shape of a cell may vary with:",
       "the function it performs",
       ["the number of nuclei it contains", "the type of ribosomes it has", "the age of the organism"], "A",
       "Shapes of cells",
       "Cells differ greatly in size, shape and activities. They may be disc-like, polygonal, columnar, cuboid, thread "
       "like, or even irregular, and NCERT notes that the shape of the cell may vary with the function it performs. "
       "For example, nerve cells are branched and long, and red blood cells are round and biconcave.",
       ["Shape varies with function"],
       why="NCERT links cell shape to function, not to the number of nuclei, the ribosome type or the organism's age.",
       ncert=ref("CELL", "An Overview of Cell"), secs=20)

match_list(T_CELL, "Cell theory", "Basic", "scientist", "year of the work as given in NCERT",
           ["Matthias Schleiden", "Theodore Schwann", "Rudolf Virchow", "Singer and Nicolson"],
           ["1855", "1972", "1838", "1839"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B",
           "Dates in the history of the cell",
           "In 1838 Matthias Schleiden, a German botanist, observed that all plants are composed of different kinds of "
           "cells. In 1839 Theodore Schwann, a British zoologist, reported the thin outer layer of animal cells. Rudolf "
           "Virchow (1855) explained that cells divide and new cells are formed from pre-existing cells. Singer and "
           "Nicolson (1972) proposed the fluid mosaic model of the cell membrane.",
           ["Schleiden 1838 → Schwann 1839", "Virchow 1855 → Singer and Nicolson 1972"],
           why="The wrong codes swap Schleiden and Schwann, or Virchow and Singer–Nicolson, or put Virchow first.",
           ncert=ref("CELL", "Cell Theory; Cell Membrane"), secs=35)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Basic",
               "The two centrioles of a centrosome lie perpendicular to each other, and each has an organisation like "
               "a cartwheel.",
               "The centrioles of a centrosome are surrounded by amorphous pericentriolar materials.",
               True, True, "A",
               "Centrosome and centrioles",
               "The centrosome is an organelle usually containing two cylindrical structures called centrioles. They "
               "are surrounded by amorphous pericentriolar materials. Both centrioles in a centrosome lie "
               "perpendicular to each other, and each has an organisation like a cartwheel.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Centrosome and Centrioles"), secs=30)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "Plasmids can confer resistance to antibiotics on some bacteria.",
                 "Pili are elongated tubular structures made of a special protein.",
                 True, True, False, "B",
                 "Plasmids and pili",
                 "Plasmids are small circular DNA outside the genomic DNA; they confer certain unique phenotypic "
                 "characters on bacteria, one of which is resistance to antibiotics. Pili are elongated tubular "
                 "structures made of a special protein, a surface structure of the cell. The composition of pili has "
                 "nothing to do with how plasmids confer antibiotic resistance.",
                 ["A: true", "R: true", "R describes a different structure"],
                 ncert=ref("CELL", "Prokaryotic Cells"), secs=35)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "In a prokaryotic cell, several protein molecules can be made from a single mRNA at the same time.",
                 "Several ribosomes may attach to a single mRNA to form a polysome, and the ribosomes of a polysome "
                 "translate the mRNA into proteins.",
                 True, True, True, "A",
                 "Polysomes",
                 "In prokaryotes, ribosomes are associated with the plasma membrane. Several ribosomes may attach to a "
                 "single mRNA and form a chain called a polyribosome or polysome, and the ribosomes of a polysome "
                 "translate the mRNA into proteins. Because each attached ribosome translates the same mRNA, several "
                 "protein molecules are made from it at once.",
                 ["A: true", "R: true; many ribosomes on one mRNA → many proteins at once"],
                 ncert=ref("CELL", "Prokaryotic Cells (ribosomes and inclusion bodies)"), secs=40)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                "In which of the following does NCERT describe the presence of DNA?",
                [("The matrix of a mitochondrion", True),
                 ("The stroma of a chloroplast", True),
                 ("The Golgi apparatus", False),
                 ("A bacterial plasmid", True),
                 ("A lysosome", False)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "d")], "D",
                "DNA outside the nucleus",
                "The mitochondrial matrix possesses a single circular DNA molecule, a few RNA molecules and 70S "
                "ribosomes. The stroma of the chloroplast contains small, double-stranded circular DNA and 70S "
                "ribosomes. Plasmids are small circular DNA molecules outside the genomic DNA of bacteria. The Golgi "
                "apparatus and lysosomes are parts of the endomembrane system and contain no DNA.",
                ["(a), (b), (d): DNA present", "(c), (e): no DNA"],
                why="(c) and (e) are endomembrane components without DNA; (a) and (d) alone leave out the chloroplast.",
                ncert=ref("CELL", "Mitochondria; Plastids; Prokaryotic Cells"), secs=45)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "A gland cell synthesises and secretes large amounts of protein. Which pair of features would you expect to be "
       "prominent in it?",
       "Abundant rough endoplasmic reticulum and larger, more numerous nucleoli",
       ["Abundant smooth endoplasmic reticulum and few, small nucleoli",
        "Many microbodies and a large central vacuole",
        "Abundant smooth endoplasmic reticulum and many chromoplasts"], "C",
       "Organelles of a protein-secreting cell",
       "The rough ER is frequently observed in cells actively involved in protein synthesis and secretion, because its "
       "ribosomes make the proteins. The nucleolus is the site of active ribosomal RNA synthesis, and larger and more "
       "numerous nucleoli are present in cells actively carrying out protein synthesis.",
       ["Protein synthesis + secretion → RER", "Active protein synthesis → large, numerous nucleoli"],
       why="Smooth ER is the major site of lipid (and, in animals, steroid hormone) synthesis. Microbodies, vacuoles "
           "and chromoplasts are not features of protein-secreting cells.",
       ncert=ref("CELL", "Endomembrane System; Nucleus"), secs=40)

match_list(T_CELL, "Cell envelope and membrane", "Intermediate", "structure", "chemical composition given in NCERT",
           ["Middle lamella", "Cell wall of a higher plant", "Cell wall of an alga", "Peripheral fibrils of a "
            "centriole"],
           ["Cellulose, galactans, mannans and minerals like calcium carbonate", "The protein tubulin",
            "Mainly calcium pectate", "Cellulose, hemicellulose, pectins and proteins"],
           "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "D",
           "Composition of cell structures",
           "The middle lamella, which holds neighbouring cells together, is mainly made of calcium pectate. The cell wall "
           "of algae is made of cellulose, galactans, mannans and minerals like calcium carbonate, while in other plants "
           "it consists of cellulose, hemicellulose, pectins and proteins. The peripheral fibrils of a centriole are made "
           "of the protein tubulin.",
           ["Middle lamella → calcium pectate", "Higher plant wall → cellulose, hemicellulose, pectins, proteins",
            "Algal wall → cellulose, galactans, mannans, CaCO3", "Centriole fibrils → tubulin"],
           why="The wrong codes swap the middle lamella and higher-plant wall, the two kinds of cell wall, or the algal "
               "wall and the centriole.",
           ncert=ref("CELL", "Cell Wall; Centrosome and Centrioles"), secs=40)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "In the membrane of human red blood cells, proteins (about 52 per cent) make up a larger share than "
               "lipids (about 40 per cent).",
               "In the plasma membrane, the lipids are arranged with their hydrophobic tails towards the outer sides "
               "and their polar heads towards the inner part.",
               True, False, "C",
               "Composition and arrangement of the cell membrane",
               "Biochemical investigation showed that the membrane of the human erythrocyte has approximately 52 per "
               "cent protein and 40 per cent lipids. The lipids are arranged within the membrane with the polar head "
               "towards the outer sides and the hydrophobic tails towards the inner part, which protects the non-polar "
               "tails from the aqueous environment.",
               ["Statement I: true (52% protein, 40% lipid)", "Statement II: false; it reverses heads and tails"],
               ncert=ref("CELL", "Cell Membrane"), secs=40)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "Which of the following statements about membrane extensions and infoldings are correct?",
                [("The inner membrane of the mitochondrion forms infoldings called cristae.", True),
                 ("Mesosomes are formed by extensions of the plasma membrane into the cell, in the form of vesicles, "
                  "tubules and lamellae.", True),
                 ("The outer membrane of the mitochondrion forms the cristae.", False),
                 ("The tonoplast folds to form the grana of the vacuole.", False),
                 ("In cyanobacteria, membranous extensions into the cytoplasm called chromatophores contain "
                  "pigments.", True)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "e")], "B",
                "Membrane extensions in cells",
                "The inner mitochondrial membrane forms a number of infoldings called cristae towards the matrix, which "
                "increase the surface area; the outer membrane forms the continuous limiting boundary. In prokaryotes, "
                "mesosomes are extensions of the plasma membrane into the cell as vesicles, tubules and lamellae; they "
                "also increase the surface area of the plasma membrane and its enzymatic content. In some prokaryotes "
                "such as cyanobacteria, other membranous extensions into the cytoplasm, the chromatophores, contain "
                "pigments. Grana are stacks of thylakoids in chloroplasts; the tonoplast is the vacuole membrane.",
                ["(a), (b), (e) true", "(c) false: inner membrane", "(d) false: grana belong to chloroplasts"],
                why="(c) and (d) are false; (a) and (e) alone leave out the mesosomes.",
                ncert=ref("CELL", "Prokaryotic Cells; Mitochondria"), secs=60)

assertion_reason(T_CELL, "Endomembrane system", "Advanced",
                 "Lysosomes are formed by the process of packaging in the Golgi apparatus.",
                 "The Golgi apparatus receives no materials from the endoplasmic reticulum.",
                 True, False, False, "C",
                 "Golgi apparatus and lysosomes",
                 "Lysosomes are membrane-bound vesicular structures formed by the process of packaging in the Golgi "
                 "apparatus. The Golgi apparatus is closely associated with the ER: a number of proteins synthesised by "
                 "ribosomes on the endoplasmic reticulum are modified in the cisternae of the Golgi apparatus before "
                 "they are released from its trans face. So R is false.",
                 ["A: true", "R: false; ER proteins are modified in the Golgi cisternae"],
                 ncert=ref("CELL", "Endomembrane System (Golgi apparatus, lysosomes)"), secs=40)

direct(T_CELL, "Endomembrane system", "Advanced",
       "Which of the following is NOT a function of the Golgi apparatus described in NCERT?",
       "Synthesis of lipid-like steroidal hormones in animal cells",
       ["Packaging materials to be delivered to intracellular targets or secreted outside the cell",
        "Modifying proteins synthesised by ribosomes on the endoplasmic reticulum",
        "Formation of glycoproteins and glycolipids"], "A",
       "Functions of the Golgi apparatus and smooth ER",
       "The Golgi apparatus principally packages materials to be delivered either to intracellular targets or "
       "secreted outside the cell. Proteins synthesised by ribosomes on the ER are modified in its cisternae before "
       "release from the trans face, and it is the important site of formation of glycoproteins and glycolipids. "
       "The smooth ER is the major site of lipid synthesis; in animal cells lipid-like steroidal hormones are "
       "synthesised in the SER.",
       ["Golgi: packaging, modification, glycoproteins and glycolipids", "Steroid hormones: smooth ER"],
       why="The three other options are all Golgi functions listed by NCERT.",
       ncert=ref("CELL", "Endomembrane System"), secs=40)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "Mesosomes help in respiration and secretion processes in a bacterial cell, which has no mitochondria.",
               "The pili of bacteria are made of the protein tubulin, like the microtubules of cilia.",
               True, False, "C",
               "Prokaryotic structures",
               "Prokaryotic cells have no membrane-bound organelles such as mitochondria. Mesosomes, extensions of the "
               "plasma membrane, help in cell wall formation, DNA replication and distribution to daughter cells, and "
               "also in respiration and secretion processes. Pili are elongated tubular structures made of a special "
               "protein; NCERT does not say they are made of tubulin, which forms the microtubules and centriole "
               "fibrils of eukaryotic cells.",
               ["Statement I: true", "Statement II: false; pili are made of a special protein, not tubulin"],
               ncert=ref("CELL", "Prokaryotic Cells; Cilia and Flagella"), secs=45)

direct(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
       "Which pair consists of two structures that are both NOT part of the endomembrane system and that both lack "
       "DNA?",
       "Microbodies and centrioles",
       ["Mitochondria and chloroplasts", "Lysosomes and vacuoles", "Golgi apparatus and endoplasmic reticulum"], "D",
       "Endomembrane system and organelle DNA",
       "The endomembrane system comprises the ER, Golgi complex, lysosomes and vacuoles, whose functions are "
       "coordinated. Mitochondria, chloroplasts and peroxisomes are not part of it, and mitochondria and chloroplasts "
       "contain their own circular DNA. Microbodies (membrane-bound vesicles of enzymes) and centrioles (cylinders of "
       "tubulin fibrils) are outside the endomembrane system and contain no DNA.",
       ["Endomembrane: ER, Golgi, lysosomes, vacuoles", "Mitochondria, chloroplasts: have DNA",
        "Microbodies, centrioles: neither"],
       why="Mitochondria and chloroplasts contain DNA; lysosomes, vacuoles, the Golgi apparatus and the ER are all "
           "part of the endomembrane system.",
       ncert=ref("CELL", "Endomembrane System; Microbodies; Centrosome and Centrioles"), secs=50)
