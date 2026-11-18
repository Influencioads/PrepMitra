
# =============================================================== 6. Cell Cycle and Cell Division (5/6/5)
direct(T_CC, "Mitosis", "Basic",
       "Prophase of mitosis is marked by the initiation of condensation of the chromosomal material. The chromosomal "
       "material becomes untangled during the process of:",
       "chromatin condensation",
       ["DNA replication", "synapsis", "crossing over"], "B",
       "Prophase of mitosis",
       "In the S and G2 phases the new DNA molecules are not distinct but intertwined. Prophase is marked by the "
       "initiation of condensation of the chromosomal material, and the chromosomal material becomes untangled during "
       "the process of chromatin condensation.",
       ["S and G2: DNA molecules intertwined", "Prophase: untangled during chromatin condensation"],
       why="DNA replication takes place in the S phase, not prophase. Synapsis and crossing over are events of "
           "prophase I of meiosis.",
       ncert=ref("CC", "M Phase (prophase)"), secs=20)

match_list(T_CC, "Cell cycle phases", "Basic", "item", "value given in NCERT",
           ["Duration of the cell cycle of a typical human cell in culture", "Duration of the M phase of that cell",
            "Duration of the cell cycle of yeast", "Share of interphase in the duration of a cell cycle"],
           ["About 90 minutes", "More than 95 per cent", "About 24 hours", "About an hour"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "D",
           "Timing of the cell cycle",
           "A typical eukaryotic cell, such as a human cell in culture, divides about once every 24 hours. Of this, the "
           "actual division (M phase) lasts only about an hour, and interphase lasts more than 95 per cent of the "
           "cycle. Yeast can progress through the cell cycle in only about 90 minutes.",
           ["Human cell: ~24 h", "M phase: ~1 h", "Yeast: ~90 min", "Interphase: >95 per cent"],
           why="The wrong codes swap the human cycle and the M phase, yeast and interphase, or the human and yeast "
               "cycles.",
           ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=30)

statement_pair(T_CC, "Cell cycle phases", "Basic",
               "All organisms, even the largest, start their life from a single cell.",
               "Like cell growth, DNA synthesis continues throughout the cell cycle.",
               True, False, "C",
               "Cell division and the cell cycle",
               "All organisms, even the largest, start their life from a single cell. Although cell growth (in terms "
               "of cytoplasmic increase) is a continuous process, DNA synthesis occurs only during one specific stage "
               "of the cell cycle, the S phase.",
               ["Statement I: true", "Statement II: false; DNA is synthesised only in the S phase"],
               ncert=ref("CC", "Cell Cycle"), secs=25)

direct(T_CC, "Mitosis", "Basic",
       "Karyokinesis of mitosis is divided into four stages. Which sequence is correct?",
       "Prophase -> metaphase -> anaphase -> telophase",
       ["Prophase -> anaphase -> metaphase -> telophase", "Metaphase -> prophase -> anaphase -> telophase",
        "Prophase -> metaphase -> telophase -> anaphase"], "D",
       "Stages of karyokinesis",
       "Mitosis (karyokinesis) is divided into four stages: prophase, metaphase, anaphase and telophase. Cytokinesis, "
       "the division of the cytoplasm, follows.",
       ["Order: prophase, metaphase, anaphase, telophase"],
       why="Each wrong sequence changes the order of two stages.",
       ncert=ref("CC", "M Phase"), secs=20)

multi_statement(T_CC, "Mitosis", "Basic",
                "Which of the following take place during prophase of mitosis?",
                [("Initiation of condensation of the chromosomal material", True),
                 ("The centrosomes begin to move towards opposite poles of the cell.", True),
                 ("The chromosomes align on the metaphase plate.", False),
                 ("The centromeres split and the chromatids separate.", False),
                 ("Each centrosome radiates out microtubules called asters.", True)],
                [("a", "b", "c"), ("a", "c", "d"), ("b", "d", "e")], "B",
                "Events of prophase",
                "Prophase is marked by the initiation of condensation of the chromosomal material. The centrosome, which "
                "had duplicated during interphase, now begins to move towards opposite poles, and each centrosome "
                "radiates out microtubules called asters. Alignment on the metaphase plate happens in metaphase, and "
                "splitting of centromeres in anaphase.",
                ["(a), (b), (e): prophase", "(c): metaphase", "(d): anaphase"],
                ncert=ref("CC", "M Phase (prophase)"), secs=40)

direct(T_CC, "Mitosis", "Intermediate",
       "In a dividing cell, the nuclear envelope has completely disintegrated, the condensation of chromosomes is "
       "complete, the chromosomes are spread through the cytoplasm, and spindle fibres are attaching to their "
       "kinetochores as they move to the spindle equator. The cell is in:",
       "metaphase of mitosis",
       ["prophase of mitosis", "anaphase of mitosis", "pachytene of meiosis I"], "B",
       "Recognising metaphase",
       "The complete disintegration of the nuclear envelope marks the start of metaphase. By this stage, condensation "
       "of chromosomes is complete and their morphology can be studied. Spindle fibres attach to the kinetochores of "
       "the chromosomes, which are moved to the spindle equator and aligned on the metaphase plate.",
       ["Nuclear envelope fully gone + condensation complete + kinetochore attachment = metaphase"],
       why="In prophase the chromosomes are only beginning to condense and the envelope is still breaking down. In "
           "anaphase the centromeres split and chromatids move apart. Pachytene is a stage of prophase I, before "
           "the nuclear envelope breaks down.",
       ncert=ref("CC", "M Phase (metaphase)"), secs=40)

assertion_reason(T_CC, "Meiosis", "Intermediate",
                 "Pachytene is relatively long-lived compared with leptotene and zygotene.",
                 "Recombination nodules first appear during zygotene.",
                 True, False, False, "C",
                 "Stages of prophase I",
                 "The first two stages of prophase I are relatively short-lived compared with the next stage, pachytene. "
                 "Pachytene is characterised by the appearance of recombination nodules, the sites at which crossing "
                 "over occurs between non-sister chromatids of the homologous chromosomes. Zygotene is the stage of "
                 "synapsis and formation of the synaptonemal complex.",
                 ["A: true", "R: false; recombination nodules appear in pachytene"],
                 ncert=ref("CC", "Meiosis (prophase I)"), secs=35)

match_list(T_CC, "Meiosis", "Intermediate", "event", "stage",
           ["Terminalisation of chiasmata", "Appearance of recombination nodules", "Formation of a dyad of cells",
            "Formation of a tetrad of four haploid cells"],
           ["Telophase II and cytokinesis", "Pachytene", "Telophase I and cytokinesis", "Diakinesis"],
           "IV II III I", ["II IV III I", "IV II I III", "IV III II I"], "A",
           "Events across meiosis",
           "Diakinesis is marked by terminalisation of chiasmata. Pachytene is characterised by the appearance of "
           "recombination nodules. In telophase I the nuclear membrane and nucleolus reappear and cytokinesis follows, "
           "giving a dyad of cells. At the end of meiosis II, cytokinesis follows telophase II, giving a tetrad of four "
           "haploid daughter cells.",
           ["Terminalisation -> diakinesis", "Recombination nodules -> pachytene", "Dyad -> telophase I",
            "Tetrad -> telophase II"],
           why="The wrong codes swap diakinesis and pachytene, the dyad and tetrad, or pachytene and telophase I.",
           ncert=ref("CC", "Meiosis"), secs=40)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Meiosis I is initiated after the parental chromosomes have replicated to produce identical sister "
               "chromatids in the S phase.",
               "In meiosis, recombination takes place between the sister chromatids of the same chromosome.",
               True, False, "C",
               "Key features of meiosis",
               "Meiosis I is initiated after the parental chromosomes have replicated to produce identical sister "
               "chromatids at the S phase. Meiosis involves pairing of homologous chromosomes and recombination "
               "between non-sister chromatids of homologous chromosomes.",
               ["Statement I: true", "Statement II: false; recombination is between non-sister chromatids of "
                "homologues"],
               ncert=ref("CC", "Meiosis"), secs=35)

multi_statement(T_CC, "Significance", "Intermediate",
                "Which of the following are described in NCERT as brought about by mitosis?",
                [("Growth of multicellular organisms", True),
                 ("Restoration of the nucleo-cytoplasmic ratio disturbed by cell growth", True),
                 ("Replacement of cells of the upper layer of the epidermis, the gut lining and blood cells", True),
                 ("Formation of gametes in animals", False),
                 ("Continuous growth of plants through divisions in the apical and lateral cambium", True)],
                [("a", "b", "c", "d"), ("a", "c", "e"), ("b", "c", "d", "e")], "C",
                "Significance of mitosis",
                "Growth of multicellular organisms is due to mitosis. Cell growth disturbs the ratio between the nucleus "
                "and the cytoplasm, so the cell divides to restore the nucleo-cytoplasmic ratio. Mitosis brings about "
                "cell repair: cells of the upper layer of the epidermis, the gut lining and blood cells are constantly "
                "replaced. Mitotic divisions in the apical and lateral cambium give continuous growth of plants "
                "throughout their life. Gametes in animals are formed through meiosis (gametogenesis).",
                ["(a), (b), (c), (e) true", "(d) false; gametogenesis involves meiosis"],
                ncert=ref("CC", "Significance of Mitosis; Meiosis"), secs=50)

direct(T_CC, "Meiosis", "Intermediate",
       "Which of the following is seen at metaphase of mitosis and also at metaphase II of meiosis?",
       "Microtubules from opposite poles attach to the kinetochores of the two sister chromatids of each chromosome.",
       ["Bivalents align on the equatorial plate.",
        "Microtubules from opposite poles attach to the two members of a pair of homologous chromosomes.",
        "Chiasmata hold the homologous chromosomes together."], "D",
       "Metaphase of mitosis compared with metaphase II",
       "At metaphase of mitosis, spindle fibres from one pole attach to the kinetochore of one chromatid and fibres "
       "from the opposite pole to its sister chromatid. At metaphase II the chromosomes align at the equator and "
       "microtubules from opposite poles attach to the kinetochores of sister chromatids. In metaphase I, by contrast, "
       "bivalents align and microtubules from opposite poles attach to the pair of homologous chromosomes.",
       ["Mitosis metaphase and metaphase II: sister chromatids attached to opposite poles"],
       why="Alignment of bivalents and attachment to homologous pairs belong to metaphase I; chiasmata belong to "
           "prophase I and metaphase I, not to mitosis or meiosis II.",
       ncert=ref("CC", "M Phase (metaphase); Meiosis (metaphase I, metaphase II)"), secs=45)

assertion_reason(T_CC, "Significance", "Advanced",
                 "Meiosis is important for the process of evolution.",
                 "Meiosis increases the genetic variability in the population of organisms from one generation to the "
                 "next, and such variations are very important for evolution.",
                 True, True, True, "A",
                 "Significance of meiosis",
                 "Meiosis conserves the specific chromosome number of each species across generations in sexually "
                 "reproducing organisms. It also increases the genetic variability in the population from one "
                 "generation to the next. Variations are very important for the process of evolution; this is why "
                 "meiosis matters for evolution.",
                 ["A: true", "R: true", "Variability produced by meiosis is the reason it matters for evolution"],
                 ncert=ref("CC", "Significance of Meiosis"), secs=40)

direct(T_CC, "Meiosis", "Advanced",
       "Consider these events of meiosis: (i) separation of homologous chromosomes; (ii) terminalisation of chiasmata; "
       "(iii) splitting of the centromeres; (iv) formation of a dyad of cells; (v) alignment of bivalents on the "
       "equatorial plate. Which is the correct order?",
       "(ii) -> (v) -> (i) -> (iv) -> (iii)",
       ["(v) -> (ii) -> (i) -> (iv) -> (iii)", "(ii) -> (v) -> (iii) -> (iv) -> (i)",
        "(ii) -> (i) -> (v) -> (iii) -> (iv)"], "D",
       "Sequence of events in meiosis",
       "Terminalisation of chiasmata marks diakinesis, the end of prophase I. In metaphase I the bivalents align on "
       "the equatorial plate. In anaphase I the homologous chromosomes separate. Telophase I with cytokinesis gives a "
       "dyad of cells. In anaphase II the centromere of each chromosome splits.",
       ["Diakinesis (ii)", "Metaphase I (v)", "Anaphase I (i)", "Telophase I and cytokinesis (iv)", "Anaphase II (iii)"],
       why="The first wrong order puts metaphase I before diakinesis; the second splits centromeres in meiosis I; the "
           "third separates homologues before they align and splits centromeres before the dyad forms.",
       ncert=ref("CC", "Meiosis"), secs=60)

statement_pair(T_CC, "Cell cycle phases", "Advanced",
               "A cell in G2 phase and a cell at metaphase of mitosis of the same diploid plant have the same number of "
               "chromosomes and the same DNA content.",
               "Each nucleus at telophase I and a cell in G1 phase of the same plant have the same DNA content, though "
               "the telophase I nucleus has half as many chromosomes.",
               True, True, "A",
               "DNA content and chromosome number through division",
               "If the G1 cell has 2n chromosomes and 2C DNA, the S phase doubles the DNA to 4C without changing the "
               "chromosome number. So a G2 cell and a mitotic metaphase cell both have 2n chromosomes and 4C DNA. In "
               "meiosis I, homologous chromosomes separate while sister chromatids stay together, so each telophase I "
               "nucleus has n chromosomes of two chromatids each: 2C DNA, the same as a G1 cell.",
               ["G2 = metaphase: 2n, 4C", "Telophase I nucleus: n chromosomes x 2 chromatids = 2C = G1 DNA content"],
               ncert=ref("CC", "Cell Cycle (phases); Meiosis"), secs=60)

match_list(T_CC, "Meiosis", "Advanced", "event in meiosis", "stage in which it occurs",
           ["Nucleolus disappears and nuclear envelope breaks down", "Chiasmata first become visible",
            "Sister chromatids separate", "Homologous chromosomes separate"],
           ["Anaphase I", "Diplotene", "Anaphase II", "Diakinesis"],
           "IV II III I", ["II IV III I", "IV II I III", "IV III II I"], "B",
           "Timing of meiotic events",
           "By the end of diakinesis the nucleolus disappears and the nuclear envelope breaks down. In diplotene the "
           "bivalents tend to separate except at the sites of crossovers; these X-shaped structures are the chiasmata. "
           "In anaphase I homologous chromosomes separate while sister chromatids remain associated at their "
           "centromeres. In anaphase II the centromeres split and sister chromatids separate.",
           ["A -> diakinesis", "B -> diplotene", "C -> anaphase II", "D -> anaphase I"],
           why="The wrong codes swap diakinesis and diplotene, the two anaphases, or diplotene and anaphase II.",
           ncert=ref("CC", "Meiosis"), secs=45)

direct(T_CC, "Meiosis", "Advanced",
       "In a dividing cell of a diploid organism, a group of chromosomes has reached each pole, the nuclear membrane and "
       "nucleolus are reappearing, each group has half the chromosome number of the parent cell, and each chromosome "
       "still consists of two chromatids. The cell is in:",
       "telophase I of meiosis",
       ["telophase of mitosis", "telophase II of meiosis", "anaphase I of meiosis"], "D",
       "Recognising telophase I",
       "In telophase I the nuclear membrane and nucleolus reappear. Because homologous chromosomes separated in "
       "anaphase I while sister chromatids stayed together, each nucleus has half the parental chromosome number, each "
       "chromosome still having two chromatids.",
       ["Half the chromosome number -> meiosis", "Chromosomes still with two chromatids -> after meiosis I, not II",
        "Nuclear membrane reappearing -> telophase"],
       why="Telophase of mitosis keeps the parental (2n) number of single-chromatid chromosomes. In telophase II the "
           "chromosomes have single chromatids. In anaphase I the chromosomes are still moving and no nuclear "
           "membrane is forming.",
       ncert=ref("CC", "Meiosis (telophase I)"), secs=50)
