
# =============================================================== 6. Cell Cycle and Cell Division (4/5/4)
direct(T_CC, "Cell cycle phases", "Basic",
       "Which of the following does NOT take place during interphase?",
       "Condensation of chromatin into compact chromosomes",
       ["Replication of DNA", "Duplication of the centriole in the cytoplasm of an animal cell",
        "Synthesis of proteins in preparation for mitosis"], "B",
       "Events of interphase and M phase",
       "Interphase consists of G1, S and G2. DNA replicates in the S phase, and in animal cells the centriole "
       "duplicates in the cytoplasm during the S phase. In G2, proteins are synthesised in preparation for mitosis "
       "while cell growth continues. Condensation of the chromosomal material into compact mitotic chromosomes marks "
       "prophase, the first stage of the M phase.",
       ["S: DNA replication, centriole duplication", "G2: proteins for mitosis", "Chromosome condensation: prophase"],
       why="DNA replication, centriole duplication and protein synthesis for mitosis all occur in interphase.",
       ncert=ref("CC", "Cell Cycle (phases of cell cycle); M Phase (prophase)"), secs=25)

direct(T_CC, "Significance", "Basic",
       "Which of the following is NOT brought about by mitosis?",
       "Formation of haploid gametes from diploid cells in animals",
       ["Replacement of the cells of the upper layer of the epidermis and the lining of the gut",
        "Continuous growth of plants by the apical and lateral cambium",
        "Increase in the number of cells in a growing multicellular organism"], "D",
       "Significance of mitosis",
       "Mitosis results in diploid daughter cells with identical genetic complement. It brings about the growth of "
       "multicellular organisms, cell repair (cells of the upper layer of the epidermis, the cells of the lining of the "
       "gut and blood cells are constantly replaced) and the continuous growth of plants through divisions in the "
       "apical and lateral cambium. Haploid gametes of animals are formed from diploid cells by meiosis, during "
       "gametogenesis.",
       ["Mitosis: growth, repair, meristem activity", "Gametes from diploid cells in animals: meiosis"],
       why="The other three options are the roles of mitosis listed in NCERT.",
       ncert=ref("CC", "Significance of Mitosis; Meiosis"), secs=25)

statement_pair(T_CC, "Meiosis", "Basic",
               "Electron micrographs of zygotene show that chromosome synapsis is accompanied by the formation of a "
               "complex structure called the synaptonemal complex.",
               "The complex formed by a pair of synapsed homologous chromosomes is called a bivalent.",
               True, True, "A",
               "Zygotene",
               "During zygotene, chromosomes start pairing together; this association is synapsis, and the paired "
               "chromosomes are homologous chromosomes. Electron micrographs of this stage indicate that synapsis is "
               "accompanied by the formation of a complex structure called the synaptonemal complex. The complex formed "
               "by a pair of synapsed homologous chromosomes is called a bivalent or a tetrad.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("CC", "Meiosis I (prophase I: zygotene)"), secs=30)

match_list(T_CC, "Significance", "Basic", "process", "result",
           ["Mitosis in a diploid cell, followed by cytokinesis", "Meiosis I, followed by cytokinesis",
            "Meiosis II, followed by cytokinesis", "Karyokinesis not followed by cytokinesis"],
           ["A tetrad of four haploid cells", "A multinucleate condition (syncytium)",
            "Two cells with the same chromosome number as the parent", "A dyad of cells"],
           "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A",
           "Outcomes of cell division",
           "Mitosis is an equational division: the daughter cells have the same chromosome number as the parent. "
           "Telophase I is followed by cytokinesis, giving a dyad of cells. At the end of meiosis II cytokinesis forms a "
           "tetrad of cells, i.e. four haploid daughter cells. When karyokinesis is not followed by cytokinesis, a "
           "multinucleate condition arises, leading to a syncytium (e.g. the liquid endosperm of coconut).",
           ["Mitosis → 2 cells, same number", "Meiosis I → dyad", "Meiosis II → tetrad",
            "No cytokinesis → syncytium"],
           why="The wrong codes swap the dyad and the tetrad, or the syncytium with a product of meiosis.",
           ncert=ref("CC", "M Phase (cytokinesis); Meiosis I; Meiosis II"), secs=35)

numerical(T_CC, "Meiosis", "Intermediate",
          "A diploid plant cell contains 6 pg of DNA in its G1 phase. It replicates its DNA and then completes "
          "meiosis. How much DNA will be present in each of the four cells formed at the end of meiosis?",
          "3 pg", ["6 pg", "1.5 pg", "12 pg"], "C", Fraction(6 * 2, 4) == 3,
          "DNA content through meiosis",
          "In the S phase the DNA content doubles (6 → 12 pg) while the chromosome number stays the same. Meiosis "
          "involves two sequential cycles of nuclear and cell division but only a single cycle of DNA replication. "
          "Meiosis I halves it to 6 pg per cell, and meiosis II, in which sister chromatids separate, halves it again "
          "to 3 pg per cell.",
          ["G1: 6 pg → after S: 12 pg", "After meiosis I: 6 pg per cell", "After meiosis II: 3 pg per cell"],
          why="6 pg ignores the second division (or the replication); 1.5 pg halves twice without first doubling; "
              "12 pg is the content after the S phase, before any division.",
          ncert=ref("CC", "Cell Cycle (S phase); Meiosis"), secs=60,
          short="Each gamete-like product has half the G1 (2C) content: C = 6/2 = 3 pg.")

assertion_reason(T_CC, "Mitosis", "Intermediate",
                 "In anaphase of mitosis, as the chromatids move towards the poles, the centromere of each chromosome "
                 "leads, with the arms trailing behind.",
                 "The chromatids are moved towards the poles by the lengthening of the microtubules attached to their "
                 "kinetochores.",
                 True, False, False, "C",
                 "Movement of chromosomes in anaphase",
                 "At anaphase, centromeres split and the chromatids separate and move to opposite poles. As each "
                 "chromosome moves away from the equatorial plate, its centromere remains directed towards the pole, "
                 "at the leading edge, with the arms trailing behind. NCERT describes the sister chromatids moving "
                 "towards opposite poles by the shortening, not lengthening, of the microtubules attached to the "
                 "kinetochores.",
                 ["A: true", "R: false; kinetochore microtubules shorten"],
                 ncert=ref("CC", "M Phase (anaphase); Meiosis II (anaphase II)"), secs=40)

direct(T_CC, "Mitosis", "Intermediate",
       "In a dividing cell, the chromosomes have reached the two poles, the nuclear envelope is reassembling around "
       "each group, and a new wall is forming as a cell plate that grows from the centre outwards. This is:",
       "a plant cell at the end of telophase, undergoing cytokinesis",
       ["an animal cell at the end of telophase, undergoing cytokinesis", "a plant cell at anaphase",
        "an animal cell at metaphase"], "B",
       "Telophase and cytokinesis in plant cells",
       "At telophase, chromosomes cluster at opposite spindle poles and the nuclear envelope assembles around each "
       "cluster. In plant cells, enclosed by a relatively inextensible cell wall, cytokinesis takes place by cell wall "
       "formation that starts in the centre of the cell and grows outward to meet the existing lateral walls; it "
       "begins as a simple precursor, the cell plate. Animal cells divide their cytoplasm by a furrow in the plasma "
       "membrane.",
       ["Nuclear envelope reforming → telophase", "Cell plate from the centre → plant cell"],
       why="Animal cells do not form a cell plate; at anaphase and metaphase the nuclear envelope is not being "
           "reassembled.",
       ncert=ref("CC", "M Phase (telophase, cytokinesis)"), secs=40)

multi_statement(T_CC, "Meiosis", "Intermediate",
                "Which of the following take place in meiosis II but NOT in meiosis I?",
                [("Splitting of the centromere of each chromosome", True),
                 ("Separation of sister chromatids towards opposite poles", True),
                 ("Pairing of homologous chromosomes", False),
                 ("Crossing over between non-sister chromatids", False),
                 ("Attachment of microtubules from opposite poles to the kinetochores of sister chromatids", True)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "e")], "D",
                "Meiosis I and meiosis II compared",
                "In metaphase I, microtubules from opposite poles attach to the pair of homologous chromosomes, and in "
                "anaphase I the homologues separate while sister chromatids remain associated at their centromeres. In "
                "metaphase II, microtubules from opposite poles attach to the kinetochores of sister chromatids, and "
                "anaphase II begins with the simultaneous splitting of the centromere of each chromosome, so the sister "
                "chromatids move to opposite poles. Pairing (synapsis) and crossing over occur in prophase I only.",
                ["(a), (b), (e): meiosis II only", "(c), (d): meiosis I only"],
                why="(c) and (d) happen in meiosis I, not meiosis II; (a) and (e) alone leave out (b).",
                ncert=ref("CC", "Meiosis I; Meiosis II"), secs=55)

match_list(T_CC, "Meiosis", "Intermediate", "stage of prophase I", "feature",
           ["Leptotene", "Zygotene", "Pachytene", "Diplotene"],
           ["Can last for months or years in the oocytes of some vertebrates",
            "Compaction of chromosomes continues throughout this stage",
            "Longer-lived than the two stages before it; recombination nodules appear",
            "Chromosomes start pairing together (synapsis)"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "C",
           "Stages of prophase I",
           "In leptotene the chromosomes become gradually visible and their compaction continues throughout the stage. "
           "During zygotene chromosomes start pairing together (synapsis). The first two stages are relatively "
           "short-lived compared with pachytene, in which recombination nodules appear and crossing over occurs. In "
           "the oocytes of some vertebrates, diplotene can last for months or years.",
           ["Leptotene → compaction", "Zygotene → synapsis", "Pachytene → long, recombination nodules",
            "Diplotene → may last months/years"],
           why="The wrong codes swap leptotene and zygotene, pachytene and diplotene, or leptotene and pachytene.",
           ncert=ref("CC", "Meiosis I (prophase I)"), secs=40)

statement_pair(T_CC, "Meiosis", "Advanced",
               "Both mitosis and meiosis are preceded by a phase in which the DNA of the cell replicates.",
               "Sister chromatids separate at anaphase of mitosis and also at anaphase I of meiosis.",
               True, False, "C",
               "DNA replication and chromatid separation",
               "Mitosis follows interphase, in which DNA replicates during the S phase. Meiosis I is initiated after the "
               "parental chromosomes have replicated to produce identical sister chromatids at the S phase; meiosis has "
               "only a single cycle of DNA replication. At anaphase of mitosis the sister chromatids separate, but at "
               "anaphase I the homologous chromosomes separate while the sister chromatids remain associated at their "
               "centromeres; sister chromatids separate only at anaphase II.",
               ["Statement I: true", "Statement II: false; anaphase I separates homologues"],
               ncert=ref("CC", "Cell Cycle; Meiosis I"), secs=45)

numerical(T_CC, "Cell cycle phases", "Advanced",
          "In a culture of human cells, each cell divides about once in 24 hours, and the M phase lasts about 1 hour. "
          "Assume the cells are dividing independently and are spread evenly over all stages of the cycle. In a "
          "sample of 960 cells, about how many would be expected to be in the M phase at any moment?",
          "40", ["24", "920", "96"], "A", 960 * 1 // 24 == 40 and 960 % 24 == 0,
          "Duration of M phase and fraction of dividing cells",
          "A typical human cell in culture divides about once every 24 hours, and the actual cell division (M phase) "
          "lasts only about an hour; interphase takes the rest. If cells are spread evenly over the cycle, the "
          "fraction found in M phase equals the fraction of time spent in it: 1/24. So 960 × 1/24 = 40 cells.",
          ["Fraction of cycle in M = 1/24", "960 × 1/24 = 40"],
          why="24 confuses the number of hours with the number of cells; 920 is the number in interphase; 96 uses 1/10 "
              "instead of 1/24.",
          ncert=ref("CC", "Cell Cycle (phases of cell cycle)"), secs=60,
          short="Cells in M ∝ time in M: 960/24 = 40.")

multi_statement(T_CC, "Meiosis", "Advanced",
                "Which of the following statements comparing telophase of mitosis with telophase I of meiosis are "
                "correct?",
                [("The nuclear membrane and nucleolus reappear in both.", True),
                 ("Each nucleus formed at telophase I has half the chromosome number of the parent meiocyte.", True),
                 ("Each chromosome in a telophase I nucleus still consists of two chromatids.", True),
                 ("At the end of telophase I, the chromosomes always reach the extremely extended state of an "
                  "interphase nucleus.", False),
                 ("Cytokinesis after telophase I produces a tetrad of cells.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c")], "B",
                "Telophase of mitosis and telophase I",
                "At telophase of mitosis the nuclear envelope assembles around each chromosome cluster and the "
                "nucleolus reappears. In telophase I the nuclear membrane and nucleolus reappear and cytokinesis follows, "
                "giving a dyad of cells. Since anaphase I separated homologous chromosomes while sister chromatids "
                "stayed together, each nucleus has half the chromosome number, and each chromosome still has two "
                "chromatids. Although the chromosomes undergo some dispersion, they do not reach the extremely "
                "extended state of the interphase nucleus. A tetrad of cells forms only after meiosis II.",
                ["(a), (b), (c) true", "(d) false: not fully extended", "(e) false: a dyad forms"],
                why="(d) and (e) are false; (a) and (c) alone leave out (b).",
                ncert=ref("CC", "M Phase (telophase); Meiosis I (telophase I)"), secs=60)

assertion_reason(T_CC, "Mitosis", "Advanced",
                 "Each daughter chromosome that moves towards a pole at anaphase of mitosis consists of a single "
                 "chromatid.",
                 "At anaphase, the centromere of each chromosome splits and the two sister chromatids separate and move "
                 "to opposite poles.",
                 True, True, True, "A",
                 "Daughter chromosomes at anaphase",
                 "At metaphase each chromosome is made of two sister chromatids held together by the centromere. At "
                 "anaphase, centromeres split and the chromatids separate; each chromatid, now a daughter chromosome, "
                 "moves to the opposite pole. Because the two chromatids of every chromosome are separated, each moving "
                 "daughter chromosome has only one chromatid.",
                 ["A: true", "R: true; splitting of centromeres and separation of chromatids is why each has one"],
                 ncert=ref("CC", "M Phase (metaphase, anaphase)"), secs=40)
