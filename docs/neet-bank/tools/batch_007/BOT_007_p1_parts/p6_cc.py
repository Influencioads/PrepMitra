
# =============================================================== 6. Cell Cycle and Cell Division (4/6/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "In the cell cycle, the replicated chromosomes (DNA) are distributed to the daughter nuclei by a complex "
       "series of events during cell division. According to NCERT, these events are themselves:",
       "under genetic control",
       ["random and uncontrolled", "controlled only by temperature", "controlled only by light"], "A",
       "Control of the cell cycle",
       "The cell cycle is the sequence of events by which a cell duplicates its genome, synthesises the other "
       "constituents of the cell and eventually divides. The replicated chromosomes are distributed to the "
       "daughter nuclei by a complex series of events, and these events are themselves under genetic control.",
       ["Events of cell division → under genetic control"],
       why="NCERT describes the events as genetically controlled, not random or governed only by an external "
           "factor.",
       ncert=ref("CC", "Cell Cycle"), secs=20)

direct(T_CC, "Meiosis", "Basic",
       "Which division reduces the number of chromosomes to half, so that the two cells formed have half the "
       "chromosome number of the parent cell?",
       "Meiosis I",
       ["Meiosis II", "Mitosis", "Interkinesis"], "D",
       "Reductional division",
       "In anaphase I the homologous chromosomes separate while sister chromatids remain together, so each of the "
       "two cells formed at the end of meiosis I has half the number of chromosomes of the parent meiocyte. "
       "Meiosis II separates sister chromatids and does not change the chromosome number, like mitosis.",
       ["Meiosis I: homologues separate → chromosome number halved"],
       why="Meiosis II and mitosis keep the chromosome number unchanged. Interkinesis is the short stage between the "
           "two meiotic divisions, not a division.",
       ncert=ref("CC", "Meiosis (Meiosis I)"), secs=20)

match_list(T_CC, "Mitosis", "Basic", "term", "meaning",
           ["Karyokinesis", "Cytokinesis", "Interkinesis", "Syncytium"],
           ["Stage between the two meiotic divisions", "Division of the cytoplasm",
            "Multinucleate condition formed when karyokinesis is not followed by cytokinesis",
            "Separation of daughter chromosomes, i.e. nuclear division"],
           "IV II I III", ["II IV I III", "IV II III I", "I II IV III"], "B",
           "Terms used in cell division",
           "The M phase starts with karyokinesis, the nuclear division (separation of daughter chromosomes), and ends "
           "with cytokinesis, the division of the cytoplasm. When karyokinesis is not followed by cytokinesis, a "
           "multinucleate condition arises, leading to a syncytium (e.g. the liquid endosperm of coconut). The stage "
           "between the two meiotic divisions is interkinesis.",
           ["Karyokinesis → nuclear division", "Cytokinesis → cytoplasmic division", "Interkinesis → between meiosis "
            "I and II", "Syncytium → multinucleate"],
           why="The wrong codes swap karyokinesis and cytokinesis, interkinesis and syncytium, or karyokinesis and "
               "interkinesis.",
           ncert=ref("CC", "M Phase; Meiosis"), secs=35)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "Interphase is divided into three further phases: G1, S and G2.",
               "In the S phase, the DNA content doubles from 2C to 4C and the number of chromosomes also doubles.",
               True, False, "C",
               "Sub-phases of interphase and the S phase",
               "Interphase consists of the G1 phase (Gap 1), the S phase (synthesis) and the G2 phase (Gap 2). In the "
               "S phase the amount of DNA per cell doubles (2C → 4C), but there is no increase in the chromosome "
               "number; a cell with 2n chromosomes in G1 still has 2n after the S phase.",
               ["Statement I: true", "Statement II: false, chromosome number does not change in S phase"],
               ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=30)

numerical(T_CC, "Cell cycle phases", "Intermediate",
          "Yeast can progress through the cell cycle in about 90 minutes. Starting from a single yeast cell, and "
          "assuming every cell completes a cycle and divides into two every 90 minutes, how many cells will be "
          "present after 6 hours?",
          "16",
          ["4", "8", "32"], "B",
          (2 ** ((6 * 60) // 90) == 16),
          "Cell number after repeated cycles",
          "6 hours = 360 minutes. Number of cycles = 360 / 90 = 4. Each cycle doubles the number of cells, so the "
          "number of cells = 2⁴ = 16.",
          ["Cycles = 360 / 90 = 4", "Cells = 2⁴ = 16"],
          why="4 is the number of cycles, not cells. 8 counts only three doublings. 32 counts five doublings.",
          ncert=ref("CC", "Cell Cycle"), secs=45)

assertion_reason(T_CC, "Meiosis", "Intermediate",
                 "Meiosis produces four haploid cells from one diploid meiocyte.",
                 "Meiosis involves two sequential cycles of nuclear and cell division but only a single cycle of DNA "
                 "replication.",
                 True, True, True, "A",
                 "Why meiosis gives four haploid cells",
                 "The DNA of the meiocyte replicates once (in the preceding S phase), and the cell then divides twice, "
                 "in meiosis I and meiosis II. Two divisions give four cells, and because there is only one round of "
                 "replication for two divisions, each cell receives half the chromosome number. So R explains A.",
                 ["A: true", "R: true; one replication + two divisions → four haploid cells"],
                 ncert=ref("CC", "Meiosis"), secs=35)

direct(T_CC, "Cell cycle phases", "Intermediate",
       "A cell of a diploid plant has 2n chromosomes and 4C DNA. Its chromosomes have not yet condensed, and its "
       "nuclear envelope and nucleolus are intact. The cell is most likely in the:",
       "G2 phase",
       ["G1 phase", "telophase II", "G0 phase"], "B",
       "Identifying a phase from DNA content",
       "DNA doubles from 2C to 4C in the S phase while the chromosome number stays 2n. A cell with 4C DNA whose "
       "chromosomes are still uncondensed, with an intact nucleus, has completed S but not begun prophase, so it is "
       "in G2, when proteins are synthesised in preparation for mitosis.",
       ["4C + 2n + intact nucleus → after S, before prophase → G2"],
       why="G1 and G0 cells have 2C DNA. A nucleus at telophase II has n chromosomes and 1C DNA.",
       ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=40)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following statements about cytokinesis in a plant cell are correct?",
                [("The new cell wall begins as a simple precursor called the cell plate.", True),
                 ("Wall formation starts in the centre of the cell and grows outward to meet the existing lateral "
                  "walls.", True),
                 ("Cytokinesis takes place by a furrow in the plasma membrane that deepens towards the centre.",
                  False),
                 ("Organelles such as mitochondria and plastids get distributed between the two daughter cells.",
                  True),
                 ("The cell plate later becomes the secondary wall.", False)],
                ["abc", "bde", "ade"], "D",
                "Cytokinesis in plant cells",
                "Plant cells are enclosed by a relatively inextensible cell wall, so cytokinesis is by cell plate "
                "formation, not furrowing. Wall formation starts in the centre and grows outward to meet the lateral "
                "walls. The cell plate represents the middle lamella between the walls of two adjacent cells. At "
                "cytokinesis, organelles like mitochondria and plastids are distributed between the daughter cells.",
                ["(a), (b), (d): true", "(c): false, furrowing is seen in animal cells",
                 "(e): false, the cell plate represents the middle lamella"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("CC", "M Phase (Cytokinesis)"), secs=50)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Interkinesis is generally long-lived, and DNA replicates during it.",
               "Anaphase I separates homologous chromosomes, while anaphase II separates sister chromatids.",
               False, True, "D",
               "Interkinesis and the two anaphases",
               "The stage between the two meiotic divisions, interkinesis, is generally short-lived, and there is no "
               "replication of DNA during it. In anaphase I the homologous chromosomes separate while the sister "
               "chromatids stay associated at their centromeres; in anaphase II the centromere of each chromosome "
               "splits and the sister chromatids move to opposite poles.",
               ["Statement I: false, interkinesis is short and has no DNA replication", "Statement II: true"],
               ncert=ref("CC", "Meiosis (Meiosis I; Meiosis II)"), secs=35)

assertion_reason(T_CC, "Cell cycle phases", "Intermediate",
                 "Cells in the quiescent stage (G0) remain metabolically active.",
                 "Cells in G0 keep proliferating continuously, whatever the requirement of the organism.",
                 True, False, False, "C",
                 "The quiescent stage",
                 "Cells that do not divide further exit G1 and enter G0. Cells in this stage remain metabolically "
                 "active but no longer proliferate unless called on to do so, depending on the requirement of the "
                 "organism. So A is true and R is false.",
                 ["A: true", "R: false, G0 cells do not proliferate unless called on to do so"],
                 ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=35)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements about a cell at metaphase II of meiosis in a diploid (2n) "
                "organism are correct?",
                [("The cell has n chromosomes.", True),
                 ("Each chromosome has two chromatids.", True),
                 ("The homologous chromosomes are paired as bivalents.", False),
                 ("Microtubules from opposite poles attach to the kinetochores of the sister chromatids.", True),
                 ("The cell has 4C DNA.", False)],
                ["abcd", "bde", "ad"], "C",
                "A cell at metaphase II",
                "Meiosis I separates homologous chromosomes, so each cell entering meiosis II has n chromosomes, each "
                "still made of two sister chromatids (2C DNA, half of the 4C of the meiocyte after S phase). At "
                "metaphase II the chromosomes align at the equator and microtubules from opposite poles attach to "
                "the kinetochores of sister chromatids. Bivalents exist only in prophase I and metaphase I.",
                ["n chromosomes × 2 chromatids → 2C DNA", "No bivalents in meiosis II"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("CC", "Meiosis (Meiosis II)"), secs=60)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "In the oocytes of some vertebrates, diplotene can last for months or years.",
                 "Diakinesis is marked by terminalisation of chiasmata.",
                 True, True, False, "B",
                 "Diplotene and diakinesis",
                 "Both statements are true. A concerns the duration of diplotene in vertebrate oocytes. R describes the "
                 "next stage, diakinesis, in which chiasmata terminalise. The terminalisation of chiasmata in a later "
                 "stage does not explain why diplotene is prolonged, so R is not the explanation of A.",
                 ["A: true", "R: true", "R describes a different stage; it does not explain A"],
                 ncert=ref("CC", "Meiosis (Prophase I)"), secs=40)

direct(T_CC, "Meiosis", "Advanced",
       "Which of the following takes place in anaphase I of meiosis, but in neither the anaphase of mitosis nor "
       "anaphase II of meiosis?",
       "Separation of homologous chromosomes, while sister chromatids remain associated at their centromeres",
       ["Splitting of the centromeres", "Movement of chromosomes towards the opposite poles",
        "Shortening of the microtubules attached to the kinetochores"], "A",
       "Anaphases compared",
       "In anaphase I the homologous chromosomes separate, while the sister chromatids remain associated at their "
       "centromeres. In the anaphase of mitosis and in anaphase II the centromeres split and sister chromatids "
       "separate. Movement towards the poles occurs in all three anaphases.",
       ["Anaphase I: homologues separate, centromeres intact",
        "Mitotic anaphase and anaphase II: centromeres split, chromatids separate"],
       why="Splitting of the centromere occurs in mitotic anaphase and anaphase II, not anaphase I. Poleward movement "
           "and the shortening of kinetochore microtubules are not unique to anaphase I.",
       ncert=ref("CC", "M Phase (Anaphase); Meiosis"), secs=45)

statement_pair(T_CC, "Cell cycle phases", "Advanced",
               "Cell growth, in terms of cytoplasmic increase, continues through the cell cycle, but DNA is "
               "synthesised in only one specific stage.",
               "In animal cells, DNA replication begins in the nucleus during the S phase, while the centriole "
               "duplicates in the cytoplasm.",
               True, True, "A",
               "Growth and DNA synthesis in the cell cycle",
               "NCERT states that although cell growth (in terms of cytoplasmic increase) is a continuous process, "
               "DNA synthesis occurs only during one specific stage, the S phase. In animal cells, during the S "
               "phase, DNA replication begins in the nucleus and the centriole duplicates in the cytoplasm.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Cell Cycle (Phases of Cell Cycle)"), secs=35)
