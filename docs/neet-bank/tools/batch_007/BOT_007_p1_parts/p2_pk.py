
# =============================================================== 2. Plant Kingdom (5/7/5)
direct(T_PK, "Algae", "Basic",
       "NCERT states that many species of Porphyra, Laminaria and Sargassum are among the marine algae used as food. "
       "How many species of marine algae used as food does NCERT mention?",
       "70",
       ["7", "700", "7000"], "C",
       "Algae as food",
       "Algae are useful to man in a variety of ways. Many species of Porphyra, Laminaria and Sargassum are among "
       "the 70 species of marine algae used as food.",
       ["Marine algae used as food: 70 species (e.g. Porphyra, Laminaria, Sargassum)"],
       why="7, 700 and 7000 are not the figure NCERT gives.",
       ncert=ref("PK", "Algae"), secs=20)

statement_pair(T_PK, "Bryophytes", "Basic",
               "Bryophytes, in general, are of little economic importance.",
               "The plant body of bryophytes is attached to the substratum by true roots.",
               True, False, "C",
               "General features of bryophytes",
               "NCERT states that bryophytes in general are of little economic importance, though some mosses "
               "provide food for animals and Sphagnum provides peat. Their plant body lacks true roots, stem and "
               "leaves; it is attached to the substratum by unicellular or multicellular rhizoids.",
               ["Statement I: true", "Statement II: false, attachment is by rhizoids, not true roots"],
               ncert=ref("PK", "Bryophytes"), secs=30)

direct(T_PK, "Gymnosperms", "Basic",
       "In gymnosperms, the cones bearing microsporophylls with microsporangia are called:",
       "microsporangiate or male strobili",
       ["macrosporangiate or female strobili", "sori", "gemma cups"], "A",
       "Male cones of gymnosperms",
       "Gymnosperms are heterosporous. The microsporophylls bearing microsporangia are arranged spirally along an "
       "axis to form lax or compact cones; the cones bearing microsporophylls are called microsporangiate or male "
       "strobili. Pollen grains develop within the microsporangia.",
       ["Microsporophylls + microsporangia → male (microsporangiate) strobili"],
       why="Macrosporangiate or female strobili bear megasporophylls with ovules. Gemma cups are found on liverwort "
           "thalli. Sori are not the cones of gymnosperms.",
       ncert=ref("PK", "Gymnosperms"), secs=20)

direct(T_PK, "Algae", "Basic",
       "Members of Rhodophyceae (red algae) usually reproduce vegetatively by:",
       "fragmentation",
       ["biflagellate zoospores", "gemmae", "budding in the secondary protonema"], "D",
       "Reproduction in red algae",
       "The red algae usually reproduce vegetatively by fragmentation. They reproduce asexually by non-motile "
       "spores and sexually by non-motile gametes; sexual reproduction is oogamous and followed by complex "
       "post-fertilisation developments.",
       ["Vegetative: fragmentation", "Asexual: non-motile spores", "Sexual: non-motile gametes, oogamous"],
       why="Red algae have no flagellated stages, so no zoospores. Gemmae are formed by liverworts, and budding in "
           "the secondary protonema is seen in mosses.",
       ncert=ref("PK", "Algae (Rhodophyceae)"), secs=25)

match_list(T_PK, "Pteridophytes", "Basic", "plant", "leaves",
           ["Pteris", "Selaginella", "Cycas", "Pinus"],
           ["Needle-like leaves with a thick cuticle and sunken stomata", "Large leaves (macrophylls)",
            "Small leaves (microphylls)", "Pinnate leaves that persist for a few years"],
           "II III IV I", ["III II IV I", "II III I IV", "IV III II I"], "B",
           "Leaves of pteridophytes and gymnosperms",
           "In pteridophytes the leaves may be small (microphylls), as in Selaginella, or large (macrophylls), as in "
           "ferns such as Pteris. In gymnosperms the leaves may be simple or compound; in Cycas the pinnate leaves "
           "persist for a few years, and in conifers such as Pinus the needle-like leaves reduce the surface area, "
           "with a thick cuticle and sunken stomata.",
           ["Pteris → macrophylls", "Selaginella → microphylls", "Cycas → pinnate, persist a few years",
            "Pinus → needles"],
           why="The wrong codes swap the two pteridophyte leaf types, or the two gymnosperms, or a fern with a "
               "gymnosperm.",
           ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=35)

direct(T_PK, "Algae", "Intermediate",
       "Which of the following features is found in members of Chlorophyceae and of Phaeophyceae, but NOT in members "
       "of Rhodophyceae?",
       "Flagellated motile cells",
       ["Chlorophyll d", "Floridean starch as the stored food", "Chlorophyll b"], "A",
       "Comparing the three classes of algae",
       "In NCERT's table, Chlorophyceae have 2–8 equal, apical flagella and Phaeophyceae have 2 unequal, lateral "
       "flagella, whereas flagella are absent in Rhodophyceae. Chlorophyll d and floridean starch occur only in "
       "red algae, and chlorophyll b only in green algae.",
       ["Chlorophyceae: 2–8 equal apical flagella", "Phaeophyceae: 2 unequal lateral flagella",
        "Rhodophyceae: flagella absent"],
       why="Chlorophyll d and floridean starch are found only in Rhodophyceae. Chlorophyll b is found only in "
           "Chlorophyceae, not in brown algae.",
       ncert=ref("PK", "Algae (Table 3.1)"), secs=40)

assertion_reason(T_PK, "Gymnosperms", "Intermediate",
                 "The seeds of gymnosperms are not covered by a fruit.",
                 "In gymnosperms the ovules are not enclosed by any ovary wall and remain exposed, both before and "
                 "after fertilisation.",
                 True, True, True, "A",
                 "Naked seeds",
                 "In gymnosperms (gymnos = naked, sperma = seeds) the ovules are not enclosed by an ovary wall and "
                 "remain exposed before and after fertilisation. After fertilisation the ovules develop into seeds, "
                 "and since there is no ovary to form a fruit, the seeds remain uncovered. R directly explains A.",
                 ["A: true", "R: true, the absence of an ovary is why the seeds are naked"],
                 ncert=ref("PK", "Gymnosperms"), secs=35)

multi_statement(T_PK, "Pteridophytes", "Intermediate",
                "Which of the following plants are pteridophytes?",
                [("Lycopodium", True), ("Salvinia", True), ("Ginkgo", False), ("Psilotum", True),
                 ("Polytrichum", False)],
                ["abc", "bde", "ade"], "B",
                "Identifying pteridophytes",
                "NCERT's examples of pteridophytes include Selaginella, Equisetum, Psilotum, Lycopodium, Salvinia, "
                "Pteris, Dryopteris and Adiantum. Ginkgo is a gymnosperm and Polytrichum a moss.",
                ["(a), (b), (d): pteridophytes", "(c) Ginkgo: gymnosperm", "(e) Polytrichum: moss"],
                why="Each wrong combination includes Ginkgo or Polytrichum, or leaves out a pteridophyte.",
                ncert=ref("PK", "Pteridophytes; Gymnosperms; Bryophytes"), secs=35)

direct(T_PK, "Pteridophytes", "Intermediate",
       "In a fern such as Dryopteris, the antheridia that release antherozoids are borne on:",
       "the prothallus, a small free-living gametophyte",
       ["the sporophylls of the leafy sporophyte", "the strobili of the sporophyte",
        "the capsule of the sporophyte"], "C",
       "Sex organs of pteridophytes",
       "In pteridophytes the main plant body is a sporophyte that bears sporangia on sporophylls. The spores "
       "germinate into small, multicellular, free-living, mostly photosynthetic thalloid gametophytes called "
       "prothallus. The gametophytes bear the male and female sex organs, the antheridia and archegonia, and water "
       "is needed for transfer of antherozoids to the archegonium.",
       ["Sporophyte → sporangia → spores", "Spore → prothallus (gametophyte) → antheridia and archegonia"],
       why="Sporophylls and strobili of the sporophyte bear sporangia, which produce spores, not antherozoids. A "
           "capsule is part of a bryophyte sporophyte.",
       ncert=ref("PK", "Pteridophytes"), secs=35)

statement_pair(T_PK, "Gymnosperms", "Intermediate",
               "The sporophyte is the dominant phase in pteridophytes, whereas the gametophyte is the dominant phase "
               "in gymnosperms.",
               "In both pteridophytes and gymnosperms, the sporangia are borne on sporophylls.",
               False, True, "D",
               "Pteridophytes and gymnosperms compared",
               "In both pteridophytes and gymnosperms the main plant body is the sporophyte. In gymnosperms the male "
               "and female gametophytes have no independent free-living existence; they remain within the "
               "sporangia retained on the sporophyte. In pteridophytes sporangia are borne on leaf-like sporophylls, "
               "and in gymnosperms on microsporophylls and megasporophylls.",
               ["Statement I: false, the sporophyte is dominant in both", "Statement II: true"],
               ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=40)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "In members of Chlorophyceae, the pigments are localised in definite chloroplasts.",
                 "Members of Chlorophyceae lack pyrenoids in their chloroplasts.",
                 True, False, False, "C",
                 "Chloroplasts of green algae",
                 "In green algae the pigments, chiefly chlorophyll a and b, are localised in definite chloroplasts, "
                 "which may be discoid, plate-like, reticulate, cup-shaped, spiral or ribbon-shaped. Most members "
                 "have one or more storage bodies called pyrenoids located in the chloroplasts; pyrenoids contain "
                 "protein besides starch. So R is false.",
                 ["A: true", "R: false, most green algae have pyrenoids in the chloroplasts"],
                 ncert=ref("PK", "Algae (Chlorophyceae)"), secs=35)

direct(T_PK, "Bryophytes", "Intermediate",
       "Which of the following pairs consists of a liverwort and a moss, in that order?",
       "Marchantia and Sphagnum",
       ["Funaria and Marchantia", "Polytrichum and Funaria", "Marchantia and Salvinia"], "D",
       "Liverworts and mosses",
       "Bryophytes include liverworts and mosses. Marchantia is a liverwort. Funaria, Polytrichum and Sphagnum are "
       "mosses. Salvinia is a heterosporous pteridophyte.",
       ["Liverwort: Marchantia", "Mosses: Funaria, Polytrichum, Sphagnum"],
       why="Funaria and Marchantia is the reverse order. Polytrichum and Funaria are both mosses. Salvinia is a "
           "pteridophyte, not a moss.",
       ncert=ref("PK", "Bryophytes"), secs=30)

direct(T_PK, "Bryophytes", "Advanced",
       "A plant has a dominant gametophyte with two stages: a creeping, green, branched, frequently filamentous "
       "stage, and an upright stage of slender axes bearing spirally arranged leaves, attached to the soil by "
       "multicellular, branched rhizoids. Its sporophyte has a foot, seta and capsule. The plant is most likely:",
       "Polytrichum",
       ["Marchantia", "Selaginella", "Spirogyra"], "B",
       "Identifying a moss",
       "In mosses the gametophyte has two stages: the protonema (creeping, green, branched, frequently filamentous) "
       "and the leafy stage, which develops from the secondary protonema and has upright, slender axes with "
       "spirally arranged leaves, attached by multicellular, branched rhizoids. The moss sporophyte is "
       "differentiated into foot, seta and capsule. Funaria, Polytrichum and Sphagnum are mosses.",
       ["Protonema + leafy stage → moss", "Polytrichum is a moss"],
       why="Marchantia is a thalloid liverwort without a protonema stage. Selaginella is a pteridophyte whose "
           "dominant plant body is a sporophyte. Spirogyra is a filamentous green alga.",
       ncert=ref("PK", "Bryophytes (Mosses)"), secs=45)

multi_statement(T_PK, "Gymnosperms", "Advanced",
                "A seed plant bears naked ovules on megasporophylls, and its pollen grains are carried by air "
                "currents to the opening of the ovules. Which of the following statements about this plant are "
                "correct?",
                [("Its seeds are not covered by a fruit.", True),
                 ("It produces haploid microspores and megaspores.", True),
                 ("Its gametophytes have an independent, free-living existence.", False),
                 ("Its main plant body is a sporophyte with true roots, stem and leaves.", True),
                 ("Its ovules are borne on the microsporophylls.", False)],
                ["abc", "ade", "bcd"], "C",
                "Features of gymnosperms",
                "The plant described is a gymnosperm. Gymnosperms are heterosporous (haploid microspores and "
                "megaspores); the main plant body is a sporophyte with roots, stem and leaves; the ovules borne on "
                "megasporophylls are not enclosed by an ovary, so the seeds are naked. The male and female "
                "gametophytes do not have an independent free-living existence, and the microsporophylls bear "
                "microsporangia, not ovules.",
                ["(a), (b), (d): true", "(c): false, gametophytes are retained on the sporophyte",
                 "(e): false, ovules are on megasporophylls"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("PK", "Gymnosperms"), secs=60)

statement_pair(T_PK, "Bryophytes", "Advanced",
               "In Marchantia, the gemma cups are borne on the sporophyte.",
               "In mosses, the spores are formed within the capsule after meiosis.",
               False, True, "D",
               "Gemmae and spore formation in bryophytes",
               "In liverworts such as Marchantia, asexual reproduction is by gemmae, which develop in small "
               "receptacles called gemma cups located on the thalli, i.e. on the gametophyte. The bryophyte "
               "sporophyte (foot, seta, capsule) is attached to the gametophyte; in the capsule, spores are formed "
               "after meiosis.",
               ["Statement I: false, gemma cups are on the gametophyte thallus", "Statement II: true"],
               ncert=ref("PK", "Bryophytes (Liverworts; Mosses)"), secs=40)

multi_statement(T_PK, "Gymnosperms", "Advanced",
                "In which of the following is one generation NOT free-living, but remains attached to or retained "
                "on the other generation?",
                [("The sporophyte of a moss", True),
                 ("The sporophyte of a liverwort", True),
                 ("The prothallus of a fern", False),
                 ("The female gametophyte of a gymnosperm", True),
                 ("The mature sporophyte of a fern", False)],
                ["abc", "bde", "ade"], "A",
                "Dependence between generations",
                "In bryophytes the sporophyte is not free-living but attached to the photosynthetic gametophyte, "
                "from which it derives nourishment. In gymnosperms the gametophytes remain within the sporangia "
                "retained on the sporophyte. In pteridophytes both generations are free-living: the prothallus is a "
                "small free-living gametophyte and the main plant body is an independent sporophyte.",
                ["(a), (b): bryophyte sporophyte attached to gametophyte",
                 "(d): gymnosperm gametophyte retained on sporophyte",
                 "(c), (e): fern generations are both free-living"],
                why="Each wrong combination includes a fern generation, which is free-living, or leaves out one of "
                    "the dependent generations.",
                ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

assertion_reason(T_PK, "Gymnosperms", "Advanced",
                 "In gymnosperms, water is required for the antherozoids to swim to the archegonia.",
                 "In gymnosperms, the pollen tube carrying the male gametes grows towards the archegonia in the "
                 "ovules.",
                 False, True, False, "D",
                 "Fertilisation in gymnosperms",
                 "Gymnosperm pollen grains are carried by air currents to the opening of the ovules. The pollen tube "
                 "carrying the male gametes grows towards the archegonia and discharges the gametes near the mouth "
                 "of the archegonia. So fertilisation does not depend on water for swimming antherozoids, as it "
                 "does in bryophytes and pteridophytes. A is false, R is true.",
                 ["A: false, male gametes reach the archegonia through the pollen tube", "R: true"],
                 ncert=ref("PK", "Gymnosperms"), secs=40)
