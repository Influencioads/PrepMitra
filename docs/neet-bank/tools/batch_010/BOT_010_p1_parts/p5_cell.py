
# =============================================================== 5. Cell: The Unit of Life (5/6/5)
direct(T_CELL, "Cell envelope and membrane", "Basic",
       "Membrane proteins are classified as integral or peripheral. According to NCERT, this classification is "
       "based on their:",
       "ease of extraction from the membrane",
       ["molecular weight", "content of carbohydrates", "ability to act as enzymes"], "D",
       "Integral and peripheral proteins",
       "NCERT: depending on the ease of extraction, membrane proteins can be classified as integral or peripheral. "
       "Peripheral proteins lie on the surface of the membrane, while integral proteins are partially or totally "
       "buried in it.",
       ["Basis of classification = ease of extraction"],
       why="NCERT does not classify membrane proteins by molecular weight, carbohydrate content or enzyme "
           "activity.",
       ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "According to NCERT, the nucleus as a cell organelle was first described by Robert Brown as early as:",
       "1831",
       ["1838", "1855", "1898"], "B",
       "Discovery of the nucleus",
       "NCERT: the nucleus as a cell organelle was first described by Robert Brown as early as 1831. Later the "
       "material of the nucleus stained by basic dyes was named chromatin by Flemming.",
       ["Robert Brown described the nucleus in 1831"],
       why="1838 is the year of Schleiden's work on plant cells, 1855 that of Virchow's 'Omnis cellula-e cellula', "
           "and 1898 that of Camillo Golgi's observation of the Golgi apparatus.",
       ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In a chloroplast, the membrane of each thylakoid encloses a space called the:",
       "lumen",
       ["stroma", "matrix", "perinuclear space"], "C",
       "Compartments of the chloroplast",
       "The space limited by the inner membrane of the chloroplast is the stroma, in which flattened membranous "
       "sacs, the thylakoids, are present. NCERT: the membrane of the thylakoids encloses a space called a lumen.",
       ["Inside the inner membrane: stroma", "Inside each thylakoid: lumen"],
       why="The stroma surrounds the thylakoids. The matrix is the inner compartment of a mitochondrion, and the "
           "perinuclear space lies between the two membranes of the nuclear envelope.",
       ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=20)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "According to NCERT, the plasma membrane of a prokaryotic cell is:",
       "semi-permeable and structurally similar to that of eukaryotes",
       ["freely permeable and structurally unlike that of eukaryotes",
        "the outermost layer of the cell envelope",
        "absent in Mycoplasma, which lacks a cell wall"], "A",
       "Plasma membrane of prokaryotes",
       "NCERT: in prokaryotes, the plasma membrane is semi-permeable in nature and interacts with the outside world. "
       "This membrane is similar structurally to that of the eukaryotes. The cell envelope consists of the outermost "
       "glycocalyx, then the cell wall and then the plasma membrane.",
       ["Prokaryotic plasma membrane: semi-permeable", "Structure similar to the eukaryotic membrane"],
       why="The membrane is not freely permeable, and it is the innermost, not the outermost, layer of the "
           "envelope. Mycoplasma lacks a cell wall, not a plasma membrane.",
       ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=25)

statement_pair(T_CELL, "Prokaryotic cell", "Basic",
               "Plastids can be seen only with the electron microscope because they are very small.",
               "Motile bacteria show a range in the number and arrangement of their flagella.",
               False, True, "D",
               "Plastids; bacterial flagella",
               "NCERT: plastids are found in all plant cells and in euglenoids; they are easily observed under the "
               "microscope as they are large. Bacterial cells may be motile or non-motile; motile ones have thin "
               "filamentous extensions called flagella, and bacteria show a range in the number and arrangement of "
               "flagella.",
               ["Statement I: false; plastids are large and easily seen under the microscope", "Statement II: true"],
               ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells (plastids)"), secs=30)

match_list(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate", "cell structure",
           "shape or organisation described in NCERT",
           ["Mitochondrion", "Chloroplast", "Golgi apparatus", "Centriole"],
           ["Flat, disc-shaped sacs (cisternae) stacked parallel to each other",
            "Cartwheel-like organisation of nine evenly spaced peripheral fibrils",
            "Sausage-shaped or cylindrical",
            "Lens-shaped, oval, spherical, discoid or even ribbon-like"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D",
           "Shapes of cell organelles",
           "NCERT: mitochondria are sausage-shaped or cylindrical (diameter 0.2-1.0 µm). Chloroplasts may be "
           "lens-shaped, oval, spherical, discoid or even ribbon-like. The Golgi apparatus consists of many flat, "
           "disc-shaped sacs or cisternae stacked parallel to each other. A centriole has an organisation like a "
           "cartwheel, made of nine evenly spaced peripheral fibrils of tubulin.",
           ["Mitochondrion -> III", "Chloroplast -> IV", "Golgi apparatus -> I", "Centriole -> II"],
           why="The wrong codes swap the mitochondrion and the chloroplast, the Golgi apparatus and the centriole, or "
               "the chloroplast and the Golgi apparatus.",
           ncert=ref("CELL", "Eukaryotic Cells"), secs=45)

assertion_reason(T_CELL, "Cell envelope and membrane", "Intermediate",
                 "Peripheral proteins are totally buried in the lipid bilayer of the cell membrane.",
                 "Integral proteins are partially or totally buried in the cell membrane.",
                 False, True, False, "D",
                 "Peripheral and integral proteins",
                 "Peripheral proteins lie on the surface of the membrane, while integral proteins are partially or "
                 "totally buried in the membrane.",
                 ["A: false - peripheral proteins lie on the surface", "R: true"],
                 ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=35)

statement_pair(T_CELL, "Endomembrane system", "Intermediate",
               "Microbodies, membrane-bound minute vesicles containing various enzymes, are present in both plant "
               "and animal cells.",
               "Microbodies are counted by NCERT as part of the endomembrane system.",
               True, False, "C",
               "Microbodies and the endomembrane system",
               "NCERT: many membrane-bound minute vesicles called microbodies, containing various enzymes, are present "
               "in both plant and animal cells. The endomembrane system includes the endoplasmic reticulum, Golgi "
               "complex, lysosomes and vacuoles, whose functions are coordinated; microbodies are not listed in it.",
               ["Statement I: true", "Statement II: false; endomembrane system = ER, Golgi, lysosomes, vacuoles"],
               ncert=ref("CELL", "Eukaryotic Cells (endomembrane system; microbodies)"), secs=35)

multi_statement(T_CELL, "Prokaryotic cell", "Intermediate",
                "Which of the following statements about bacterial flagella are correct?",
                [("A bacterial flagellum is composed of three parts: filament, hook and basal body.", True),
                 ("The filament is the longest portion and extends from the cell surface to the outside.", True),
                 ("Fimbriae form the longest part of the bacterial flagellum.", False),
                 ("Bacterial flagella are structurally identical to eukaryotic flagella.", False),
                 ("Motile bacteria have thin filamentous extensions called flagella.", True)],
                [("a", "b"), ("a", "c", "e"), ("b", "d", "e")], "B",
                "Structure of the bacterial flagellum",
                "Motile bacteria have thin filamentous extensions called flagella. A bacterial flagellum has three "
                "parts - filament, hook and basal body; the filament is the longest portion and extends from the "
                "cell surface to the outside. Fimbriae are separate small bristle-like fibres used for attachment, "
                "and prokaryotic flagella are structurally different from eukaryotic ones.",
                ["(a) true", "(b) true", "(c) false: fimbriae are not part of the flagellum",
                 "(d) false: they are structurally different", "(e) true"],
                why="(a) and (b) only leaves out (e). The other combinations include the false statement (c) or (d).",
                ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=55)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "Which of the following pairs consists of two structures that are NOT bounded by any membrane?",
       "Ribosome and nucleolus",
       ["Lysosome and vacuole", "Ribosome and microbody", "Nucleolus and mitochondrion"], "C",
       "Non-membranous structures of the cell",
       "Ribosomes are composed of RNA and proteins and are not surrounded by any membrane. The nucleolus is not a "
       "membrane-bound structure; its content is continuous with the rest of the nucleoplasm. Lysosomes, vacuoles "
       "and microbodies are membrane-bound, and mitochondria have two membranes.",
       ["Ribosome: no membrane", "Nucleolus: no membrane", "Lysosome, vacuole, microbody, mitochondrion: "
        "membrane-bound"],
       why="Each wrong pair contains at least one membrane-bound structure: lysosome, vacuole (tonoplast), "
           "microbody or mitochondrion (double membrane).",
       ncert=ref("CELL", "Eukaryotic Cells (ribosomes; nucleus)"), secs=35)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
       "Which of the following is found in both plant and animal cells and also contains its own DNA?",
       "Mitochondrion",
       ["Chloroplast", "Centriole", "Lysosome"], "A",
       "Organelles with their own DNA",
       "Mitochondria occur in plant and animal cells, and the mitochondrial matrix possesses a single circular DNA "
       "molecule, a few RNA molecules and 70S ribosomes. Chloroplasts also have DNA but are found in plant cells "
       "(and euglenoids), not in animal cells. Centrioles and lysosomes do not contain DNA.",
       ["Mitochondrion: both cell types + own DNA", "Chloroplast: own DNA but not in animal cells"],
       why="Chloroplasts are absent from animal cells. Centrioles are absent from almost all plant cells and, like "
           "lysosomes, have no DNA.",
       ncert=ref("CELL", "Eukaryotic Cells (mitochondria; plastids)"), secs=30)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "Unless specifically stained, mitochondria are not easily visible under the microscope.",
                 "The number of mitochondria per cell is variable, depending on the physiological activity of the "
                 "cell.",
                 True, True, False, "B",
                 "Two separate features of mitochondria",
                 "NCERT: mitochondria, unless specifically stained, are not easily visible under the microscope. The "
                 "number of mitochondria per cell is variable depending on the physiological activity of the cells. "
                 "How many mitochondria a cell has does not decide whether each one can be seen without staining; "
                 "the two statements describe different properties.",
                 ["A: true", "R: true", "The number per cell has nothing to do with visibility -> R does not "
                  "explain A"],
                 ncert=ref("CELL", "Eukaryotic Cells (mitochondria)"), secs=40)

statement_pair(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
               "In a centriole the peripheral fibrils are doublets of microtubules, whereas in the axoneme of a "
               "cilium the peripheral fibrils are triplets.",
               "The central part of the proximal region of a centriole is called the hub, and it is proteinaceous.",
               False, True, "D",
               "Comparing centrioles and axonemes",
               "The axoneme of a cilium or flagellum has nine pairs of doublets of radially arranged peripheral "
               "microtubules and a pair of centrally located microtubules (9 + 2). A centriole has nine evenly spaced "
               "peripheral fibrils, each a triplet; the central part of its proximal region, the hub, is "
               "proteinaceous and is connected to the peripheral triplets by radial spokes.",
               ["Statement I: false; the doublet and triplet are reversed", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella; centrosome and centrioles)"), secs=45)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "An organism completely lacks a cell wall, is among the smallest living cells known and can survive "
                "without oxygen. Which of the following statements about its cell are correct?",
                [("It is a prokaryotic cell.", True),
                 ("Its ribosomes are associated with the plasma membrane.", True),
                 ("Its genetic material is naked, not enveloped by a nuclear membrane.", True),
                 ("Its cell envelope consists of a glycocalyx, a cell wall and a plasma membrane.", False),
                 ("Its ribosomes are of the 80S type.", False)],
                [("a", "c"), ("a", "b", "d"), ("b", "c", "e")], "A",
                "Applying prokaryotic features to Mycoplasma",
                "The organism described is Mycoplasma, the smallest living cell known (about 0.3 µm), which lacks a "
                "cell wall and can survive without oxygen. NCERT places mycoplasma with bacteria, blue-green algae "
                "and PPLO among prokaryotes. In prokaryotes the genetic material is naked, the ribosomes are 70S "
                "and are associated with the plasma membrane. Lacking a wall, Mycoplasma cannot have the usual "
                "three-layered envelope.",
                ["Organism = Mycoplasma (prokaryote)", "(a), (b), (c): prokaryotic features -> true",
                 "(d) false: it has no cell wall", "(e) false: prokaryotic ribosomes are 70S"],
                why="(a) and (c) only leaves out the true statement (b). The other combinations include (d) or (e).",
                ncert=ref("CELL", "Prokaryotic Cells; Biological Classification (Mycoplasma)"), secs=60)

match_list(T_CELL, "Endomembrane system", "Advanced", "structure", "enzymes or contents described in NCERT",
           ["Lysosome", "Chloroplast stroma", "Mitochondrial membranes", "Microbodies"],
           ["Each of the two membranes has its own specific enzymes associated with the organelle's function",
            "Minute membrane-bound vesicles containing various enzymes, present in both plant and animal cells",
            "Hydrolytic enzymes such as lipases, proteases and carbohydrases, optimally active at acidic pH",
            "Enzymes required for the synthesis of carbohydrates and proteins"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "C",
           "Enzymes of cell compartments",
           "Isolated lysosomal vesicles are very rich in almost all types of hydrolytic enzymes (lipases, proteases, "
           "carbohydrases), optimally active at acidic pH. The chloroplast stroma contains enzymes required for the "
           "synthesis of carbohydrates and proteins. The two mitochondrial membranes have their own specific "
           "enzymes associated with mitochondrial function. Microbodies are membrane-bound minute vesicles that "
           "contain various enzymes and occur in both plant and animal cells.",
           ["Lysosome -> III", "Chloroplast stroma -> IV", "Mitochondrial membranes -> I", "Microbodies -> II"],
           why="The wrong codes swap the lysosome with the stroma, the mitochondrial membranes with microbodies, or "
               "the stroma with the mitochondrial membranes.",
           ncert=ref("CELL", "Eukaryotic Cells"), secs=55)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
       "Which of the following possesses plastids but has no cell wall, according to NCERT?",
       "Euglena",
       ["A mesophyll cell of a leaf", "Nostoc", "Amoeba"], "B",
       "Plastids without a cell wall",
       "NCERT states that plastids are found in all plant cells and in euglenoids. Euglenoids such as Euglena have "
       "no cell wall; instead they have a protein-rich layer called the pellicle. A mesophyll cell has both "
       "plastids and a cell wall. Nostoc, a cyanobacterium, has pigment-containing chromatophores, not plastids, "
       "and Amoeba has neither plastids nor a wall.",
       ["Plastids: plant cells and euglenoids", "Euglenoids: pellicle instead of a cell wall"],
       why="A mesophyll cell has a cell wall. Nostoc is a prokaryote without plastids (it has a cell wall too). "
           "Amoeba has no plastids.",
       ncert=ref("CELL", "Eukaryotic Cells (plastids); Biological Classification (euglenoids)"), secs=45)
