
# =============================================================== 5. Cell: The Unit of Life (5/7/5)
direct(T_CELL, "Prokaryotic cell", "Basic",
       "The 70S ribosome of a prokaryotic cell is made of two subunits. These are:",
       "50S and 30S",
       ["60S and 40S", "40S and 30S", "60S and 10S"], "D",
       "Subunits of the prokaryotic ribosome",
       "In prokaryotes, ribosomes are about 15 nm by 20 nm in size and are made of two subunits, 50S and 30S, which "
       "together form the 70S prokaryotic ribosome. The eukaryotic 80S ribosome has 60S and 40S subunits.",
       ["70S = 50S + 30S (prokaryotes)", "80S = 60S + 40S (eukaryotes)"],
       why="60S and 40S are the subunits of the eukaryotic 80S ribosome. S values are sedimentation coefficients and "
           "are not simply added, so pairs chosen to add up to 70 are wrong.",
       ncert=ref("CELL", "Prokaryotic Cells (Ribosomes and Inclusion Bodies)"), secs=20)

match_list(T_CELL, "Cell theory", "Basic", "cell", "NCERT's description",
           ["Egg of an ostrich", "Nerve cell", "Human red blood cell", "White blood cell"],
           ["Amoeboid", "The largest isolated single cell", "Round and biconcave", "Some of the longest cells"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "Cells differ in size and shape",
           "Cells differ greatly in size, shape and activities. The largest isolated single cell is the egg of an "
           "ostrich. Nerve cells are some of the longest cells. Red blood cells are round and biconcave, while white "
           "blood cells are amoeboid.",
           ["Ostrich egg → largest isolated cell", "Nerve cell → among the longest", "RBC → round, biconcave",
            "WBC → amoeboid"],
           why="The wrong codes swap the ostrich egg and the nerve cell, the two blood cells, or the ostrich egg and "
               "the red blood cell.",
           ncert=ref("CELL", "An Overview of Cell"), secs=30)

direct(T_CELL, "Prokaryotic cell", "Basic",
       "In prokaryotic cells, the ribosomes are associated with the:",
       "plasma membrane",
       ["endoplasmic reticulum", "nuclear envelope", "Golgi apparatus"], "A",
       "Location of ribosomes in prokaryotes",
       "No organelles like those of eukaryotes are found in prokaryotic cells, except ribosomes. NCERT states that "
       "in prokaryotes the ribosomes are associated with the plasma membrane of the cell.",
       ["Prokaryotes have no ER, nuclear envelope or Golgi", "Ribosomes → associated with plasma membrane"],
       why="The endoplasmic reticulum, nuclear envelope and Golgi apparatus are all absent in prokaryotic cells.",
       ncert=ref("CELL", "Prokaryotic Cells (Ribosomes and Inclusion Bodies)"), secs=20)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
       "Which cell organelle is described by NCERT as a double membrane-bound structure that is sausage-shaped or "
       "cylindrical, with a diameter of 0.2–1.0 µm?",
       "Mitochondrion",
       ["Lysosome", "Golgi apparatus", "Ribosome"], "C",
       "Shape of mitochondria",
       "Mitochondria are sausage-shaped or cylindrical, with a diameter of 0.2–1.0 µm (average 0.5 µm) and a "
       "length of 1.0–4.1 µm. Each is a double membrane-bound structure, with the inner membrane forming cristae.",
       ["Sausage-shaped or cylindrical, double membrane → mitochondrion"],
       why="Lysosomes are single membrane-bound vesicles. The Golgi apparatus is made of flat, disc-shaped "
           "cisternae. Ribosomes have no membrane at all.",
       ncert=ref("CELL", "Mitochondria"), secs=20)

statement_pair(T_CELL, "Mitochondria, plastids and ribosomes", "Basic",
               "Chloroplasts may be lens-shaped, oval, spherical, discoid or even ribbon-like organelles.",
               "The space limited by the inner membrane of the chloroplast is called the stroma.",
               True, True, "A",
               "Chloroplast shape and stroma",
               "The chloroplasts in green plants are lens-shaped, oval, spherical, discoid or even ribbon-like, with "
               "a length of 5–10 µm and a width of 2–4 µm. They are double membrane-bound, and the space limited by "
               "the inner membrane is called the stroma, in which the thylakoids lie.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CELL", "Plastids"), secs=25)

numerical(T_CELL, "Cytoskeleton, cilia and centrioles", "Intermediate",
          "How many individual microtubules are present in the 9 + 2 axoneme of a cilium, and in the nine "
          "peripheral fibrils of a centriole, respectively?",
          "20 and 27",
          ["11 and 9", "20 and 18", "18 and 27"], "C",
          (9 * 2 + 2 == 20 and 9 * 3 == 27),
          "Counting microtubules",
          "The axoneme has nine doublets of radially arranged peripheral microtubules and a pair of centrally "
          "located microtubules: 9 × 2 + 2 = 20. A centriole has nine evenly spaced peripheral fibrils of tubulin, "
          "each of which is a triplet: 9 × 3 = 27.",
          ["Axoneme: 9 doublets + 2 central = 18 + 2 = 20", "Centriole: 9 triplets = 27"],
          why="11 and 9 count fibrils, not individual microtubules. 20 and 18 treats the centriole fibrils as "
              "doublets. 18 and 27 forgets the central pair of the axoneme.",
          ncert=ref("CELL", "Cilia and Flagella; Centrosome and Centrioles"), secs=50)

direct(T_CELL, "Endomembrane system", "Intermediate",
       "A protein synthesised by ribosomes on the endoplasmic reticulum is to be secreted from the cell. Which route "
       "does it most likely follow?",
       "Rough ER → cis face of the Golgi apparatus → trans face of the Golgi apparatus → outside the cell",
       ["Trans face of the Golgi apparatus → cis face → rough ER → outside the cell",
        "Smooth ER → lysosome → nucleus → outside the cell",
        "Rough ER → trans face of the Golgi apparatus → cis face → outside the cell"], "B",
       "Route of secretory proteins",
       "The Golgi cisternae have a convex cis (forming) face and a concave trans (maturing) face. Materials to be "
       "packaged come from the ER, fuse with the cis face and move towards the trans face. Many proteins "
       "synthesised by ribosomes on the ER are modified in the Golgi cisternae before they are released from its "
       "trans face; the Golgi apparatus packages materials to be secreted outside the cell.",
       ["RER ribosomes make the protein", "Enters Golgi at cis face", "Leaves from trans face for secretion"],
       why="The cis face receives and the trans face releases, so routes that go trans → cis are reversed. Lysosomes "
           "and the nucleus are not on the secretory route.",
       ncert=ref("CELL", "Endomembrane System (Golgi Apparatus)"), secs=40)

assertion_reason(T_CELL, "Prokaryotic cell", "Intermediate",
                 "The genomic DNA of a prokaryotic cell is described as 'naked'.",
                 "In prokaryotes, the genetic material is not enveloped by a nuclear membrane.",
                 True, True, True, "A",
                 "Naked genetic material of prokaryotes",
                 "Prokaryotes have no well-defined nucleus. Their genetic material is basically naked, i.e. not "
                 "enveloped by a nuclear membrane; the genomic DNA is a single chromosome or circular DNA lying in "
                 "the cytoplasm. The absence of the envelope is exactly what 'naked' means, so R explains A.",
                 ["A: true", "R: true and explains A"],
                 ncert=ref("CELL", "Prokaryotic Cells"), secs=30)

multi_statement(T_CELL, "Nucleus", "Intermediate",
                "In which of the following does NCERT describe RNA as a component?",
                [("Ribosomes", True), ("Chromatin", True), ("The mitochondrial matrix", True),
                 ("The middle lamella", False), ("The cell wall of a higher plant", False)],
                ["abcd", "bce", "ac"], "D",
                "Where RNA is found",
                "Ribosomes are composed of ribonucleic acid and proteins. Chromatin contains DNA, histones, some "
                "non-histone proteins and also RNA. The mitochondrial matrix has a single circular DNA molecule, a "
                "few RNA molecules and ribosomes. The middle lamella is mainly calcium pectate, and the cell wall of "
                "higher plants consists of cellulose, hemicellulose, pectins and proteins.",
                ["(a), (b), (c): contain RNA", "(d), (e): no RNA"],
                why="Each wrong combination includes the middle lamella or the cell wall, or leaves out one of the "
                    "RNA-containing structures.",
                ncert=ref("CELL", "Ribosomes; Mitochondria; Nucleus; Cell Wall"), secs=50)

match_list(T_CELL, "Endomembrane system", "Intermediate", "scientist", "contribution",
           ["George Palade", "Camillo Golgi", "Flemming", "Singer and Nicolson"],
           ["Proposed the fluid mosaic model of the cell membrane (1972)",
            "First observed ribosomes under the electron microscope as dense particles (1953)",
            "Named the material of the nucleus stained by basic dyes 'chromatin'",
            "First observed densely stained reticular structures near the nucleus (1898)"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "D",
           "Discoverers of cell components",
           "Ribosomes were first observed by George Palade (1953). Camillo Golgi (1898) first observed densely "
           "stained reticular structures near the nucleus, later named the Golgi bodies. Flemming named the material "
           "of the nucleus stained by basic dyes chromatin. Singer and Nicolson (1972) proposed the fluid mosaic "
           "model.",
           ["Palade → ribosomes", "Golgi → Golgi bodies", "Flemming → chromatin", "Singer-Nicolson → fluid mosaic"],
           why="The wrong codes swap Palade and Golgi, Flemming and Singer-Nicolson, or Palade and Flemming.",
           ncert=ref("CELL", "Cell Membrane; Golgi Apparatus; Ribosomes; Nucleus"), secs=45)

statement_pair(T_CELL, "Prokaryotic cell", "Intermediate",
               "All prokaryotes have a cell wall surrounding the cell membrane, except Mycoplasma.",
               "In motile bacteria, the thin filamentous extensions that bring about movement are called pili.",
               True, False, "C",
               "Cell wall and motility structures of prokaryotes",
               "NCERT states that all prokaryotes have a cell wall surrounding the cell membrane, except in "
               "mycoplasma. Motile bacteria have thin filamentous extensions from their cell wall called flagella. "
               "Pili and fimbriae are surface structures that do not play a role in motility.",
               ["Statement I: true", "Statement II: false, movement is by flagella; pili do not help in motility"],
               ncert=ref("CELL", "Prokaryotic Cells (Cell Envelope and its Modifications)"), secs=35)

assertion_reason(T_CELL, "Endomembrane system", "Intermediate",
                 "The endoplasmic reticulum divides the intracellular space into two distinct compartments, the "
                 "luminal (inside ER) and the extra-luminal (cytoplasm) compartments.",
                 "The smooth endoplasmic reticulum is the major site for the synthesis of lipids.",
                 True, True, False, "B",
                 "Structure and function of the ER",
                 "Both statements are true. A describes how the network of the ER divides the space inside the cell. "
                 "R describes a function of the smooth ER (lipid synthesis, and steroidal hormones in animal cells). "
                 "Lipid synthesis has nothing to do with how the ER compartmentalises the cell, so R does not explain "
                 "A.",
                 ["A: true", "R: true", "R is a function, unrelated to compartmentalisation"],
                 ncert=ref("CELL", "Endomembrane System (The Endoplasmic Reticulum)"), secs=40)

multi_statement(T_CELL, "Prokaryotic cell", "Advanced",
                "Which of the following statements comparing prokaryotic and eukaryotic cells are correct?",
                [("Both have a plasma membrane and ribosomes.", True),
                 ("Mesosomes, formed by extensions of the plasma membrane into the cell, are characteristic of "
                  "prokaryotes.", True),
                 ("The inclusion bodies of prokaryotes are not bounded by any membrane system.", True),
                 ("Prokaryotic cells have membrane-bound organelles such as mitochondria.", False),
                 ("The genomic DNA of both is enclosed in a nuclear envelope.", False)],
                ["abcd", "bce", "ace"], "A",
                "Prokaryotic and eukaryotic cells compared",
                "Plasma membrane and ribosomes are common to all cells. Mesosomes, a specialised differentiated "
                "form of the cell membrane, are characteristic of prokaryotes. Reserve material in prokaryotes is "
                "stored as inclusion bodies, not bounded by any membrane. Prokaryotes lack membrane-bound organelles "
                "and a nuclear envelope; these are features of eukaryotic cells.",
                ["(a), (b), (c): true", "(d), (e): false"],
                why="Each wrong combination includes (d) or (e), or leaves out a true statement.",
                ncert=ref("CELL", "Prokaryotic Cells; Eukaryotic Cells"), secs=55)

direct(T_CELL, "Mitochondria, plastids and ribosomes", "Advanced",
       "An organelle is bounded by two membranes, of which the inner one is relatively less permeable. Inside it "
       "are flattened membranous sacs stacked like piles of coins, and its matrix contains small double-stranded "
       "circular DNA and 70S ribosomes. The organelle is the:",
       "chloroplast",
       ["mitochondrion", "Golgi apparatus", "nucleus"], "C",
       "Identifying the chloroplast",
       "The chloroplast is double membrane-bound, and its inner membrane is relatively less permeable. The "
       "thylakoids are arranged in stacks like piles of coins called grana. The stroma contains small, "
       "double-stranded circular DNA molecules and 70S ribosomes, and enzymes for synthesis of carbohydrates and "
       "proteins.",
       ["Double membrane + DNA + 70S ribosomes → mitochondrion or chloroplast",
        "Stacks of sacs like piles of coins (grana) → chloroplast"],
       why="A mitochondrion also has two membranes, DNA and 70S ribosomes, but its inner membrane forms cristae, not "
           "stacked sacs. The Golgi apparatus has single-membrane cisternae and no DNA. The nucleus has a double "
           "envelope with pores, but no grana-like stacks and no 70S ribosomes.",
       ncert=ref("CELL", "Plastids; Mitochondria"), secs=45)

assertion_reason(T_CELL, "Cytoskeleton, cilia and centrioles", "Advanced",
                 "Centrioles are present in almost all plant cells.",
                 "Centrioles form the basal bodies of cilia or flagella, and in animal cells they give rise to the "
                 "spindle fibres of the spindle apparatus during cell division.",
                 False, True, False, "D",
                 "Centrioles",
                 "Animal cells have centrioles, which are absent in almost all plant cells, so A is false. R is "
                 "true: centrioles form the basal body of cilia or flagella, and spindle fibres that give rise to the "
                 "spindle apparatus during cell division in animal cells.",
                 ["A: false, centrioles are absent in almost all plant cells", "R: true"],
                 ncert=ref("CELL", "Centrosome and Centrioles; Eukaryotic Cells"), secs=40)

statement_pair(T_CELL, "Prokaryotic cell", "Advanced",
               "Both the bacterial flagellum and the eukaryotic flagellum have a 9 + 2 axoneme.",
               "Fimbriae help some bacteria attach to rocks in streams and also to the host tissues.",
               False, True, "D",
               "Surface structures of bacteria",
               "The bacterial flagellum is composed of three parts, the filament, hook and basal body; NCERT notes that "
               "prokaryotic bacteria have flagella that are structurally different from those of eukaryotes, which "
               "have a 9 + 2 axoneme. Fimbriae are small bristle-like fibres; in some bacteria they help attach the "
               "cell to rocks in streams and to host tissues.",
               ["Statement I: false, bacterial flagellum = filament, hook, basal body", "Statement II: true"],
               ncert=ref("CELL", "Prokaryotic Cells; Cilia and Flagella"), secs=40)

direct(T_CELL, "Prokaryotic cell", "Advanced",
       "A prokaryotic 70S ribosome is about 15 nm by 20 nm. Which of the following arranges these in increasing "
       "order of size?",
       "Prokaryotic 70S ribosome < Mycoplasma < typical bacterium < human red blood cell",
       ["Mycoplasma < prokaryotic 70S ribosome < typical bacterium < human red blood cell",
        "Prokaryotic 70S ribosome < Mycoplasma < human red blood cell < typical bacterium",
        "Typical bacterium < Mycoplasma < prokaryotic 70S ribosome < human red blood cell"], "B",
       "Comparing sizes",
       "The stem gives the ribosome as about 15 nm by 20 nm (0.015–0.02 µm). NCERT gives Mycoplasma as about 0.3 µm, "
       "a typical bacterium as 3–5 µm and a human red blood cell as about 7.0 µm in diameter. So the order is ribosome < "
       "Mycoplasma < bacterium < red blood cell.",
       ["Ribosome ≈ 0.02 µm", "Mycoplasma 0.3 µm", "Bacterium 3–5 µm", "RBC ≈ 7 µm"],
       why="Mycoplasma (0.3 µm) is larger than a ribosome (20 nm). A typical bacterium (3–5 µm) is smaller than a "
           "red blood cell (7 µm). The last option reverses the first three.",
       ncert=ref("CELL", "An Overview of Cell; Prokaryotic Cells"), secs=50)
