
# =============================================================== 5. Cell: The Unit of Life (5/7/6)
direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "In a chloroplast, the flat membranous tubules that connect the thylakoids of different grana are called:",
       "stroma lamellae",
       ["cristae", "mesosomes", "chromatophores"], "D",
       "Internal membranes of the chloroplast",
       "The space limited by the inner membrane of the chloroplast is the stroma. A number of organised, flattened "
       "membranous sacs, the thylakoids, are present in the stroma and are arranged in stacks like piles of coins "
       "called grana. Flat membranous tubules called stroma lamellae connect the thylakoids of the different grana.",
       ["Thylakoids stack into grana", "Stroma lamellae connect thylakoids of different grana"],
       why="Cristae are infoldings of the inner mitochondrial membrane. Mesosomes and chromatophores are membrane "
           "extensions of prokaryotic cells.",
       ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=20)

direct(T_CELL, "Cell envelope and membrane", "Basic",
       "The quasi-fluid nature of lipid enables lateral movement of proteins within the overall bilayer of the cell "
       "membrane. This ability to move within the membrane is measured as its:",
       "fluidity",
       ["selective permeability", "osmosis", "active transport"], "B",
       "Fluidity of the membrane",
       "In the fluid mosaic model of Singer and Nicolson (1972), the quasi-fluid nature of the lipid enables lateral "
       "movement of proteins within the overall bilayer. This ability to move within the membrane is measured as its "
       "fluidity. The fluid nature is important for functions like cell growth, formation of intercellular junctions, "
       "secretion, endocytosis and cell division.",
       ["Lateral movement within the membrane is measured as fluidity"],
       why="Selective permeability refers to which molecules can cross the membrane. Osmosis is diffusion of water. "
           "Active transport is energy-dependent movement against a concentration gradient.",
       ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=20)

direct(T_CELL, "Nucleus", "Basic",
       "Every chromosome has a primary constriction, the centromere. The disc-shaped structures present on the sides "
       "of the centromere are called:",
       "kinetochores",
       ["satellites", "centrioles", "nucleoli"], "B",
       "Centromere and kinetochores",
       "Every chromosome essentially has a primary constriction, the centromere, on the sides of which disc-shaped "
       "structures called kinetochores are present.",
       ["Primary constriction = centromere", "Disc-shaped structures on its sides = kinetochores"],
       why="A satellite is a small chromosome fragment set off by a non-staining secondary constriction. Centrioles lie "
           "in the centrosome of animal cells, and nucleoli are bodies in the nucleoplasm.",
       ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=20)

statement_pair(T_CELL, "Nucleus", "Basic",
               "Normally there is only one nucleus per cell, although variations in the number of nuclei are also "
               "frequently observed.",
               "The nucleus contains one or more spherical structures called nucleoli in the nucleoplasm.",
               True, True, "A",
               "Number of nuclei and nucleoli",
               "NCERT states that normally there is only one nucleus per cell, though variations in the number of "
               "nuclei are also frequently observed. The nuclear matrix or nucleoplasm contains the nucleolus and "
               "chromatin; the nucleoli are spherical structures present in the nucleoplasm.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=25)

match_list(T_CELL, "Mitochondria, plastids and ribosomes", "Basic", "plastid", "content",
           ["Amyloplasts", "Elaioplasts", "Aleuroplasts", "Chromoplasts"],
           ["Fat-soluble carotenoid pigments", "Proteins", "Starch (carbohydrates)", "Oils and fats"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C",
           "Kinds of plastids",
           "Leucoplasts are colourless plastids of varied shapes and sizes with stored nutrients: amyloplasts store "
           "carbohydrates (starch), elaioplasts store oils and fats, and aleuroplasts store proteins. Chromoplasts "
           "contain fat-soluble carotenoid pigments such as carotene and xanthophylls.",
           ["Amyloplast -> starch", "Elaioplast -> oils and fats", "Aleuroplast -> proteins",
            "Chromoplast -> carotenoids"],
           why="The wrong codes swap amyloplasts and elaioplasts, aleuroplasts and chromoplasts, or elaioplasts and "
               "aleuroplasts.",
           ncert=ref("CELL", "Eukaryotic Cells (plastids)"), secs=30)

assertion_reason(T_CELL, "Endomembrane system", "Intermediate",
                 "In animal cells, lipid-like steroidal hormones are synthesised in the smooth endoplasmic reticulum.",
                 "The smooth endoplasmic reticulum is the major site for the synthesis of lipids.",
                 True, True, True, "A",
                 "Functions of the smooth ER",
                 "The endoplasmic reticulum that does not bear ribosomes appears smooth (SER). The SER is the major site "
                 "for the synthesis of lipid; accordingly, in animal cells, lipid-like steroidal hormones are "
                 "synthesised in the SER.",
                 ["A: true", "R: true", "Steroidal hormones are lipid-like, so they are made where lipids are made"],
                 ncert=ref("CELL", "Eukaryotic Cells (endoplasmic reticulum)"), secs=35)

multi_statement(T_CELL, "Mitochondria, plastids and ribosomes", "Intermediate",
                "In which of the following locations would you expect 70S ribosomes?",
                [("The cytoplasm of a bacterium", True), ("The stroma of a chloroplast", True),
                 ("The matrix of a mitochondrion", True), ("The cytoplasm of an onion root cell", False),
                 ("The rough endoplasmic reticulum of a liver cell", False)],
                [("a", "b"), ("a", "b", "c", "e"), ("b", "c", "d")], "B",
                "70S and 80S ribosomes",
                "Prokaryotic ribosomes are of the 70S type. The chloroplast stroma contains ribosomes smaller (70S) than "
                "the cytoplasmic ones (80S), and the mitochondrial matrix contains 70S ribosomes. The cytoplasm of an "
                "eukaryotic cell, including ribosomes on the RER, has 80S ribosomes.",
                ["(a), (b), (c): 70S", "(d), (e): eukaryotic cytoplasmic ribosomes, 80S"],
                ncert=ref("CELL", "Prokaryotic Cells (ribosomes); Eukaryotic Cells (mitochondria, plastids, ribosomes)"),
                secs=45)

statement_pair(T_CELL, "Cell envelope and membrane", "Intermediate",
               "Transport of a few ions or molecules across the membrane from lower to higher concentration is an "
               "energy-dependent process that uses ATP, as in the Na+/K+ pump.",
               "Neutral solutes move across the membrane by simple diffusion against their concentration gradient.",
               True, False, "C",
               "Passive and active transport",
               "Neutral solutes may move across the membrane by simple diffusion along the concentration gradient, "
               "from higher to lower concentration. A few ions or molecules are transported against their "
               "concentration gradient, from lower to higher concentration; this is an energy-dependent process using "
               "ATP, called active transport, e.g. the Na+/K+ pump.",
               ["Statement I: true (active transport)", "Statement II: false; simple diffusion is along the gradient"],
               ncert=ref("CELL", "Eukaryotic Cells (cell membrane)"), secs=35)

match_list(T_CELL, "Endomembrane system", "Intermediate", "cell activity", "structure chiefly concerned",
           ["A gland cell synthesising and secreting much protein", "Formation of glycoproteins and glycolipids",
            "Osmoregulation and excretion in Amoeba",
            "Accumulating ions in the vacuole above their cytoplasmic concentration"],
           ["Contractile vacuole", "Tonoplast", "Rough endoplasmic reticulum", "Golgi apparatus"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A",
           "Endomembrane components and their roles",
           "The RER is frequently observed in cells actively involved in protein synthesis and secretion. The Golgi "
           "apparatus is the important site of formation of glycoproteins and glycolipids. In Amoeba the contractile "
           "vacuole is important for osmoregulation and excretion. The tonoplast facilitates the transport of a number "
           "of ions and other materials against concentration gradients into the vacuole, so their concentration is "
           "significantly higher in the vacuole than in the cytoplasm.",
           ["Protein secretion -> RER", "Glycoproteins and glycolipids -> Golgi",
            "Amoeba osmoregulation -> contractile vacuole", "Ion accumulation -> tonoplast"],
           why="The wrong codes swap RER and Golgi, the contractile vacuole and tonoplast, or Golgi and the contractile "
               "vacuole.",
           ncert=ref("CELL", "Eukaryotic Cells (endomembrane system)"), secs=45)

_dna_cm = 200 / 46
numerical(T_CELL, "Nucleus", "Intermediate",
          "According to NCERT, a single human cell has an approximately two-metre-long thread of DNA distributed among "
          "its forty-six chromosomes. On average, about how long is the DNA of one chromosome?",
          "About 4.3 cm", ["About 8.7 cm", "About 43 cm", "About 0.43 cm"], "D",
          abs(_dna_cm - 4.35) < 0.01 and abs(200 / 23 - 8.70) < 0.01,
          "Length of DNA in human chromosomes",
          "The DNA of a human cell, about 2 m long, is distributed among 46 chromosomes (23 pairs). The average length "
          "per chromosome is 2 m / 46 = 200 cm / 46, about 4.3 cm.",
          ["2 m = 200 cm", "200 cm / 46 = 4.35 cm, about 4.3 cm"],
          why="8.7 cm divides by the 23 pairs instead of the 46 chromosomes; 43 cm and 0.43 cm are errors of a factor of "
              "10 in converting metres to centimetres.",
          ncert=ref("CELL", "Eukaryotic Cells (nucleus)"), secs=45)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "Mesosomes increase the surface area of the plasma membrane and its enzymatic content.",
                 "Mesosomes are double-membrane-bound organelles, like mitochondria.",
                 True, False, False, "C",
                 "Mesosomes",
                 "Mesosomes are a special membranous structure formed by extensions of the plasma membrane into the cell, "
                 "in the form of vesicles, tubules and lamellae. They help in cell wall formation, DNA replication and "
                 "its distribution to daughter cells, respiration and secretion, and increase the surface area of the "
                 "plasma membrane and its enzymatic content. Prokaryotes have no membrane-bound organelles such as "
                 "mitochondria.",
                 ["A: true", "R: false; mesosomes are extensions of the plasma membrane, not organelles"],
                 ncert=ref("CELL", "Prokaryotic Cells (cell envelope and its modifications)"), secs=35)

match_list(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate", "structure", "organisation",
           ["Axoneme of a cilium", "Centriole", "Bacterial flagellum", "Basal body"],
           ["Filament, hook and basal body", "Centriole-like structure from which a cilium or flagellum emerges",
            "Nine peripheral doublets around a central pair of microtubules",
            "Nine evenly spaced peripheral triplet fibrils of tubulin, like a cartwheel"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B",
           "Microtubular structures",
           "The axoneme of a cilium or flagellum has nine pairs of doublets of radially arranged peripheral microtubules "
           "and a pair of centrally located microtubules (9 + 2). A centriole has an organisation like a cartwheel, made "
           "of nine evenly spaced peripheral fibrils of tubulin, each a triplet. A bacterial flagellum has a filament, a "
           "hook and a basal body. Cilia and flagella emerge from centriole-like structures called basal bodies.",
           ["Axoneme -> 9 + 2 doublets", "Centriole -> 9 triplets", "Bacterial flagellum -> filament, hook, basal body",
            "Basal body -> centriole-like base"],
           why="The wrong codes swap the axoneme and centriole, the bacterial flagellum and basal body, or the axoneme "
               "and bacterial flagellum.",
           ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella; centrosome); Prokaryotic Cells"), secs=45)

multi_statement(T_CELL, "Cell theory", "Advanced",
                "A cell has a nucleus with a nuclear envelope and a centrosome with two centrioles, but no cell wall and "
                "no plastids. Which of the following conclusions about it are correct?",
                [("It is a eukaryotic cell.", True),
                 ("Its outer boundary is the plasma membrane.", True),
                 ("It has a large central vacuole.", False),
                 ("Its centrioles can give rise to the spindle fibres during cell division.", True),
                 ("All its ribosomes are of the 70S type.", False)],
                [("a", "b", "c", "d"), ("a", "d", "e"), ("b", "c", "d")], "C",
                "Recognising an animal cell",
                "A nucleus bounded by a nuclear envelope marks a eukaryotic cell; centrioles with no cell wall or "
                "plastids mark an animal cell. Its delimiting outer structure is the cell membrane. Plant cells, not "
                "animal cells, have a large central vacuole. In animal cells the centrioles give rise to the spindle "
                "fibres of the spindle apparatus. The cytoplasmic ribosomes of eukaryotes are 80S.",
                ["(a), (b), (d) true", "(c) false: large central vacuole is a plant-cell feature",
                 "(e) false: cytoplasmic ribosomes are 80S"],
                ncert=ref("CELL", "Eukaryotic Cells"), secs=60)

assertion_reason(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
                 "The stroma of a chloroplast can carry out protein synthesis.",
                 "The chloroplast stroma contains small, double-stranded circular DNA molecules and ribosomes, along "
                 "with enzymes required for the synthesis of proteins.",
                 True, True, True, "A",
                 "Chloroplast stroma",
                 "The stroma of the chloroplast contains enzymes required for the synthesis of carbohydrates and "
                 "proteins. It also contains small, double-stranded circular DNA molecules and ribosomes (70S). "
                 "Ribosomes are the sites of protein synthesis, so the stroma has the machinery for it.",
                 ["A: true", "R: true", "DNA, ribosomes and enzymes in the stroma explain its protein synthesis"],
                 ncert=ref("CELL", "Eukaryotic Cells (plastids; ribosomes)"), secs=45)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "The chromatophores of cyanobacteria and the thylakoids of chloroplasts both contain pigments.",
               "Chromatophores, like thylakoids, lie inside a double-membrane-bound plastid.",
               True, False, "C",
               "Chromatophores and thylakoids",
               "In some prokaryotes such as cyanobacteria, there are other membranous extensions into the cytoplasm "
               "called chromatophores, which contain pigments. Thylakoids lie in the stroma of the chloroplast, a "
               "double-membrane-bound plastid, and contain the chlorophyll pigments. Prokaryotes have no "
               "membrane-bound organelles, so chromatophores do not lie inside any plastid.",
               ["Statement I: true", "Statement II: false; chromatophores are extensions into the prokaryotic cytoplasm"],
               ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells (plastids)"), secs=45)

match_list(T_CELL, "Endomembrane system", "Advanced", "structure", "origin or nature",
           ["Tonoplast", "Cristae", "Grana", "Nuclear pores"],
           ["Formed by the fusion of the two membranes of the nuclear envelope", "Stacks of thylakoids",
            "Infoldings of the inner mitochondrial membrane", "Single membrane bounding the vacuole"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D",
           "Membranes and membrane-derived structures",
           "The vacuole is bound by a single membrane called the tonoplast. The inner mitochondrial membrane forms a "
           "number of infoldings, the cristae. In the chloroplast stroma, thylakoids are arranged in stacks like piles "
           "of coins called grana. The nuclear envelope is interrupted at places by minute pores formed by the fusion "
           "of its two membranes.",
           ["Tonoplast -> IV", "Cristae -> III", "Grana -> II", "Nuclear pores -> I"],
           why="The wrong codes swap the tonoplast and cristae, the grana and nuclear pores, or the cristae and grana.",
           ncert=ref("CELL", "Eukaryotic Cells (vacuoles, mitochondria, plastids, nucleus)"), secs=50)

direct(T_CELL, "Cell envelope and membrane", "Advanced",
       "Two neighbouring mature plant cells each have a primary and a secondary wall. Which sequence correctly shows "
       "the layers met in going from the plasma membrane of one cell to the plasma membrane of the other?",
       "Secondary wall -> primary wall -> middle lamella -> primary wall -> secondary wall",
       ["Primary wall -> secondary wall -> middle lamella -> secondary wall -> primary wall",
        "Middle lamella -> primary wall -> secondary wall -> primary wall -> middle lamella",
        "Secondary wall -> middle lamella -> primary wall -> middle lamella -> secondary wall"], "D",
       "Layers of the plant cell wall",
       "The cell wall of a young plant cell, the primary wall, is capable of growth. Secondary wall is formed on the "
       "inner (towards the membrane) side of the cell. The middle lamella, mainly calcium pectate, holds or glues "
       "the different neighbouring cells together. So from one plasma membrane outward: secondary wall, primary wall, "
       "then the shared middle lamella, then the other cell's primary and secondary walls.",
       ["Secondary wall lies inside the primary wall", "Middle lamella lies between the walls of neighbouring cells"],
       why="The first wrong sequence puts the secondary wall outside the primary wall. The others put a middle lamella "
           "next to the plasma membrane or between the primary and secondary walls of the same cell.",
       ncert=ref("CELL", "Eukaryotic Cells (cell wall)"), secs=50)

direct(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
       "NCERT describes radial spokes as protein connections in microtubular structures. Radial spokes are found in:",
       "both the axoneme of a cilium and a centriole",
       ["the axoneme of a cilium only", "a centriole only", "the bacterial flagellum only"], "A",
       "Radial spokes in axonemes and centrioles",
       "In the axoneme of cilia and flagella, the central sheath is connected to one of the tubules of each peripheral "
       "doublet by a radial spoke. In a centriole, the central part of the proximal region, the hub, is connected with "
       "the tubules of the peripheral triplets by radial spokes made of protein. So both have radial spokes.",
       ["Axoneme: central sheath -> radial spokes -> peripheral doublets",
        "Centriole: hub -> radial spokes -> peripheral triplets"],
       why="Restricting radial spokes to only one of the two ignores the other description. The bacterial flagellum "
           "has a filament, hook and basal body, not a 9 + 2 or cartwheel structure.",
       ncert=ref("CELL", "Eukaryotic Cells (cilia and flagella; centrosome and centrioles)"), secs=45)
