
# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "According to NCERT, the cell cycle is divided into two basic phases. These are:",
       "interphase and M phase",
       ["G1 phase and G2 phase", "karyokinesis and cytokinesis", "S phase and G0 phase"], "B",
       "Two basic phases of the cell cycle",
       "The cell cycle is divided into two basic phases: interphase, the period of preparation for division (G1, S "
       "and G2), and the M phase (mitosis phase), when the actual cell division takes place.",
       ["Basic phases: interphase + M phase", "Interphase = G1 + S + G2"],
       why="G1 and G2 are sub-phases of interphase. Karyokinesis and cytokinesis are the two parts of the M phase. "
           "G0 is a quiescent stage outside the active cycle, and S is a sub-phase of interphase.",
       ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=20)

direct(T_CC, "Mitosis", "Basic",
       "Which of the following is NOT one of the four stages into which karyokinesis of mitosis is divided?",
       "Interkinesis",
       ["Prophase", "Metaphase", "Telophase"], "D",
       "Stages of karyokinesis",
       "Karyokinesis of mitosis is divided into four stages: prophase, metaphase, anaphase and telophase. "
       "Interkinesis is the stage between the two meiotic divisions, not a stage of mitosis.",
       ["Mitotic stages: prophase, metaphase, anaphase, telophase", "Interkinesis: between meiosis I and II"],
       why="Prophase, metaphase and telophase are three of the four stages of karyokinesis.",
       ncert=ref("CC", "M Phase"), secs=20)

statement_pair(T_CC, "Meiosis", "Basic",
               "Meiosis II is initiated immediately after cytokinesis, usually before the chromosomes have fully "
               "elongated.",
               "Prophase II is a much simpler prophase than prophase I.",
               True, True, "A",
               "Start of meiosis II",
               "NCERT: meiosis II is initiated immediately after cytokinesis, usually before the chromosomes have "
               "fully elongated. Interkinesis is followed by prophase II, a much simpler prophase than prophase I.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Meiosis (meiosis II)"), secs=25)

direct(T_CC, "Significance", "Basic",
       "Meiosis ensures that the specific chromosome number of each species is conserved across generations in "
       "sexually reproducing organisms, even though the process itself, paradoxically, results in:",
       "reduction of the chromosome number by half",
       ["doubling of the chromosome number", "no change in the chromosome number of the daughter cells",
        "the formation of diploid gametes"], "D",
       "The paradox of meiosis",
       "NCERT: the conservation of the specific chromosome number of each species across generations is achieved "
       "through meiosis, even though the process, per se, paradoxically, results in reduction of chromosome number "
       "by half. Fertilisation later restores the diploid number.",
       ["Meiosis halves the chromosome number", "Fertilisation restores it -> number conserved across generations"],
       why="Meiosis does not double or keep the chromosome number; it halves it, and the gametes it forms are "
           "haploid, not diploid.",
       ncert=ref("CC", "Significance of Meiosis"), secs=25)

numerical(T_CC, "Cell cycle phases", "Intermediate",
          "How many of the following take place during the M phase of the cell cycle?\n\n(i) Replication of DNA\n"
          "(ii) Duplication of the centriole in an animal cell\n(iii) Condensation of chromosomes\n"
          "(iv) Disintegration of the nuclear envelope\n(v) Cytokinesis\n"
          "(vi) Synthesis of proteins in preparation for mitosis",
          "3", ["2", "4", "5"], "B",
          sum([False, False, True, True, True, False]) == 3,
          "Events of interphase and M phase",
          "DNA replication and centriole duplication take place in the S phase, and proteins are synthesised in "
          "preparation for mitosis in G2 - all parts of interphase. The M phase starts with karyokinesis "
          "(condensation of chromosomes in prophase; complete disintegration of the nuclear envelope marks the start "
          "of metaphase) and usually ends with cytokinesis.",
          ["Interphase: (i), (ii) in S; (vi) in G2", "M phase: (iii), (iv), (v)", "Count = 3"],
          why="2 leaves out cytokinesis, which is part of the M phase. 4 adds G2 protein synthesis or centriole "
              "duplication, and 5 adds both, though they belong to interphase.",
          ncert=ref("CC", "Cell Cycle; M Phase"), secs=50)

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "Mitosis is also called equational division.",
                 "In plant cells, cytokinesis begins with a cell plate that forms in the centre of the cell and "
                 "grows outwards.",
                 True, True, False, "B",
                 "Equational division; cytokinesis in plants",
                 "Mitosis is called equational division because the number of chromosomes in the parent and progeny "
                 "cells is the same. Separately, in plant cells the new wall begins as a cell plate formed in the "
                 "centre and growing outward to meet the lateral walls. The way the cytoplasm is divided in plants "
                 "has nothing to do with why mitosis keeps the chromosome number equal.",
                 ["A: true (same chromosome number in parent and progeny)", "R: true", "R is about cytokinesis in "
                  "plants, not about the chromosome number -> not the explanation"],
                 ncert=ref("CC", "M Phase (cytokinesis)"), secs=35)

multi_statement(T_CC, "Mitosis", "Intermediate",
                "Which of the following take place during telophase of mitosis?",
                [("The centromere of each chromosome splits.", False),
                 ("A nuclear envelope develops around each chromosome cluster at the poles.", True),
                 ("The nucleolus, Golgi complex and ER reform.", True),
                 ("The chromosomes decondense and lose their individuality.", True),
                 ("The chromosomes align on the metaphase plate.", False)],
                [("b", "c"), ("a", "b", "d"), ("c", "d", "e")], "D",
                "Events of telophase",
                "At telophase the chromosomes that have reached their poles decondense and lose their "
                "individuality; the chromatin collects in a mass at each pole. A nuclear envelope develops around "
                "the chromosome clusters at each pole, forming two daughter nuclei, and the nucleolus, Golgi complex "
                "and ER reform. Centromeres split at anaphase, and chromosomes align on the metaphase plate at "
                "metaphase.",
                ["(a) anaphase event: false", "(b) true", "(c) true", "(d) true", "(e) metaphase event: false"],
                why="(b) and (c) only leaves out the decondensation of chromosomes. The other combinations include "
                    "(a) or (e), which belong to anaphase and metaphase.",
                ncert=ref("CC", "M Phase (telophase)"), secs=50)

statement_pair(T_CC, "Meiosis", "Intermediate",
               "Diakinesis is marked by the formation of the synaptonemal complex.",
               "During diakinesis, the chromosomes are fully condensed and the meiotic spindle is assembled to "
               "prepare the homologous chromosomes for separation.",
               False, True, "D",
               "Diakinesis",
               "The synaptonemal complex forms in zygotene and dissolves in diplotene. Diakinesis is marked by "
               "terminalisation of chiasmata; during this phase the chromosomes are fully condensed and the meiotic "
               "spindle is assembled to prepare the homologous chromosomes for separation. By its end the nucleolus "
               "disappears and the nuclear envelope breaks down.",
               ["Statement I: false; synaptonemal complex forms in zygotene", "Statement II: true"],
               ncert=ref("CC", "Meiosis (prophase I)"), secs=35)

direct(T_CC, "Meiosis", "Intermediate",
       "A dividing cell of a diploid organism has n chromosomes, each made of two chromatids. The chromosomes are "
       "becoming compact again, and the nuclear membrane disappears by the end of the stage. The cell is in:",
       "prophase II",
       ["prophase I", "metaphase II", "telophase I"], "B",
       "Recognising prophase II",
       "After meiosis I each cell has n chromosomes, each still with two chromatids. Meiosis II begins immediately; "
       "in prophase II the nuclear membrane disappears by the end of the stage and the chromosomes again become "
       "compact. In metaphase II the chromosomes align at the equator.",
       ["n chromosomes with two chromatids -> after meiosis I", "Chromosomes compacting, nuclear membrane "
        "disappearing -> prophase II"],
       why="A cell in prophase I has 2n chromosomes forming bivalents. In metaphase II the chromosomes are already "
           "aligned at the equator. In telophase I the nuclear membrane and nucleolus reappear rather than "
           "disappear.",
       ncert=ref("CC", "Meiosis (meiosis II)"), secs=40)

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements correctly compare prophase I of meiosis with prophase of "
                "mitosis?",
                [("Prophase I is typically longer and more complex than prophase of mitosis.", True),
                 ("Crossing over between non-sister chromatids occurs in both.", False),
                 ("Synapsis of homologous chromosomes takes place only in prophase I.", True),
                 ("The nuclear envelope remains intact after both of them are over.", False),
                 ("Condensation of the chromosomal material takes place in both.", True)],
                [("a", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Prophase I versus mitotic prophase",
                "NCERT: prophase of the first meiotic division is typically longer and more complex than prophase of "
                "mitosis and is subdivided into leptotene, zygotene, pachytene, diplotene and diakinesis. "
                "Chromosomes condense in both. Synapsis (zygotene) and crossing over between non-sister chromatids "
                "(pachytene) happen only in meiosis I. The nuclear envelope breaks down at the end of mitotic "
                "prophase (its complete disintegration marks the start of metaphase) and by the end of diakinesis.",
                ["(a) true", "(b) false: no crossing over in mitosis", "(c) true",
                 "(d) false: the nuclear envelope breaks down in both", "(e) true"],
                why="(a) and (c) only leaves out the condensation of chromosomes. The other combinations include (b) "
                    "or (d).",
                ncert=ref("CC", "M Phase (prophase); Meiosis (prophase I)"), secs=60)

direct(T_CC, "Meiosis", "Advanced",
       "Which of the following would NOT be seen in a cell at anaphase II of meiosis?",
       "Homologous chromosomes paired as bivalents",
       ["Splitting of the centromere of each chromosome",
        "Sister chromatids moving towards opposite poles",
        "Shortening of the microtubules attached to the kinetochores"], "A",
       "Events of anaphase II",
       "Anaphase II begins with the simultaneous splitting of the centromere of each chromosome, allowing the sister "
       "chromatids to move towards opposite poles by shortening of the microtubules attached to the kinetochores. "
       "The homologous chromosomes had already separated in anaphase I, so no bivalents remain.",
       ["Anaphase II: centromeres split, sister chromatids move apart, microtubules shorten",
        "Homologues separated in anaphase I -> no bivalents"],
       why="Splitting of centromeres, movement of sister chromatids to opposite poles and shortening of "
           "kinetochore microtubules all happen in anaphase II.",
       ncert=ref("CC", "Meiosis (meiosis II)"), secs=40)

assertion_reason(T_CC, "Meiosis", "Advanced",
                 "Interkinesis is followed by a prophase that is more complex than prophase I.",
                 "Interkinesis, the stage between the two meiotic divisions, is generally short-lived.",
                 False, True, False, "D",
                 "Interkinesis and prophase II",
                 "The stage between the two meiotic divisions is called interkinesis and is generally short-lived. "
                 "Interkinesis is followed by prophase II, which NCERT describes as a much simpler prophase than "
                 "prophase I.",
                 ["A: false - prophase II is much simpler than prophase I", "R: true"],
                 ncert=ref("CC", "Meiosis (meiosis I; meiosis II)"), secs=40)

statement_pair(T_CC, "Meiosis", "Advanced",
               "At metaphase I, the chromosomes align on the equatorial plate as single, unpaired chromosomes.",
               "At metaphase of mitosis, both sister chromatids of a chromosome are attached to spindle fibres from "
               "the same pole.",
               False, False, "B",
               "Metaphase of mitosis and metaphase I",
               "At metaphase I, the bivalent chromosomes align on the equatorial plate, and microtubules from the "
               "opposite poles attach to the pair of homologous chromosomes. At metaphase of mitosis, one chromatid "
               "of each chromosome is connected by its kinetochore to spindle fibres from one pole and its sister "
               "chromatid to spindle fibres from the opposite pole.",
               ["Statement I: false; bivalents align at metaphase I",
                "Statement II: false; sister chromatids attach to opposite poles"],
               ncert=ref("CC", "M Phase (metaphase); Meiosis (metaphase I)"), secs=45)
