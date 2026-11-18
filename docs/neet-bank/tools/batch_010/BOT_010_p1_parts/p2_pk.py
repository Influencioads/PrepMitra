
# =============================================================== 2. Plant Kingdom (5/6/5)
direct(T_PK, "Gymnosperms", "Basic",
       "In gymnosperms, the pollen tube carrying the male gametes grows towards the archegonia in the ovules. "
       "According to NCERT, it discharges its contents:",
       "near the mouth of the archegonia",
       ["inside the microsporangium", "on the surface of the megasporophyll, outside the ovule",
        "into the soil, where the gametes swim to the ovule"], "B",
       "Fertilisation in gymnosperms",
       "Pollen grains released from the microsporangium are carried by air currents to the opening of the ovules "
       "borne on megasporophylls. The pollen tube carrying the male gametes grows towards the archegonia in the "
       "ovules and discharges its contents near the mouth of the archegonia.",
       ["Pollen reaches the opening of the ovule", "Pollen tube grows to the archegonia",
        "Contents discharged near the mouth of the archegonia"],
       why="The microsporangium is where pollen grains develop, not where they discharge gametes. The tube grows "
           "inside the ovule, not on the megasporophyll surface, and gymnosperm gametes are not released into the "
           "soil.",
       ncert=ref("PK", "Gymnosperms"), secs=25)

direct(T_PK, "Algae", "Basic",
       "NCERT notes that, besides living in water, some algae occur in association with fungi and some with "
       "animals. The association of algae with fungi is seen in:",
       "lichens",
       ["mycorrhiza", "the coralloid roots of Cycas", "the fur of the sloth bear"], "C",
       "Habitats and associations of algae",
       "Algae are largely aquatic, but also occur on moist stones, soils and wood. Some of them also occur in "
       "association with fungi (lichen) and animals (e.g., on sloth bear).",
       ["Algae + fungi -> lichen", "Algae + animal -> e.g., on sloth bear"],
       why="Mycorrhiza is a fungus associated with the roots of higher plants (e.g., Pinus). The coralloid roots of "
           "Cycas are associated with nitrogen-fixing cyanobacteria, and algae on the sloth bear are NCERT's example "
           "of association with an animal.",
       ncert=ref("PK", "Algae"), secs=20)

direct(T_PK, "Gymnosperms", "Basic",
       "Which of the following is NOT a gymnosperm?",
       "Salvinia",
       ["Ginkgo", "Cedrus", "Sequoia"], "D",
       "Identifying gymnosperms",
       "Ginkgo, Cedrus and Sequoia (the giant redwood, one of the tallest tree species) are gymnosperms. Salvinia is "
       "a heterosporous pteridophyte.",
       ["Ginkgo, Cedrus, Sequoia: gymnosperms", "Salvinia: heterosporous pteridophyte"],
       why="Ginkgo and Cedrus are gymnosperm examples in NCERT, and Sequoia is named as a gymnosperm that is one "
           "of the tallest tree species.",
       ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=20)

statement_pair(T_PK, "Pteridophytes", "Basic",
               "Pteridophytes are used for medicinal purposes and as soil-binders, and are frequently grown as "
               "ornamentals.",
               "Although pteridophytes are found in cool, damp, shady places, some may flourish well in sandy-soil "
               "conditions.",
               True, True, "A",
               "Uses and habitat of pteridophytes",
               "NCERT: pteridophytes include horsetails and ferns. They are used for medicinal purposes and as "
               "soil-binders, and are frequently grown as ornamentals. They are found in cool, damp, shady places, "
               "though some may flourish well in sandy-soil conditions.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Pteridophytes"), secs=25)

direct(T_PK, "Algae", "Basic",
       "In members of Chlorophyceae (green algae), the plant body may be:",
       "unicellular, colonial or filamentous",
       ["only unicellular", "always filamentous and attached by rhizoids",
        "always massive, with a holdfast, a stipe and a frond"], "A",
       "Body form of green algae",
       "NCERT: in Chlorophyceae the plant body may be unicellular, colonial or filamentous (e.g., Chlamydomonas, "
       "Volvox, Ulothrix). They are usually grass green because chlorophyll a and b dominate.",
       ["Green algae: unicellular, colonial or filamentous"],
       why="Green algae are not restricted to one body form. Rhizoids attach bryophytes, and a holdfast, stipe and "
           "frond describe the body of brown algae.",
       ncert=ref("PK", "Algae (Chlorophyceae)"), secs=20)

multi_statement(T_PK, "Bryophytes", "Intermediate",
                "Which of the following structures are diploid?",
                [("The seta of a moss", True),
                 ("The megaspore mother cell in the ovule of a gymnosperm", True),
                 ("A leaf of a fern", True),
                 ("The protonema of a moss", False),
                 ("An antherozoid of a fern", False)],
                [("a", "b"), ("b", "c", "e"), ("a", "c", "d")], "B",
                "Haploid and diploid structures in plant groups",
                "In mosses the zygote develops into the sporophyte (foot, seta and capsule), which is diploid; the "
                "spores formed in it by meiosis give the haploid protonema. In gymnosperms the megaspore mother "
                "cell, differentiated from a cell of the nucellus, is diploid and divides meiotically. In ferns the "
                "main plant body, with its leaves, is the diploid sporophyte, while the antherozoids are produced on "
                "the haploid gametophyte.",
                ["(a) seta: part of the sporophyte -> 2n", "(b) megaspore mother cell -> 2n (divides by meiosis)",
                 "(c) fern leaf: sporophyte -> 2n", "(d) protonema: gametophyte -> n",
                 "(e) antherozoid: male gamete -> n"],
                why="(a) and (b) only leaves out the fern leaf. The other combinations include the haploid "
                    "antherozoid or the haploid protonema.",
                ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Members of Phaeophyceae vary in colour from olive green to various shades of brown.",
                 "In members of Phaeophyceae, chlorophyll b is the main pigment.",
                 True, False, False, "C",
                 "Pigments of brown algae",
                 "Brown algae possess chlorophyll a and c, carotenoids and xanthophylls. They vary in colour from "
                 "olive green to various shades of brown depending upon the amount of the xanthophyll pigment "
                 "fucoxanthin. Chlorophyll b is the pigment of green algae (with chlorophyll a); it is not present "
                 "in brown algae.",
                 ["A: true", "R: false - brown algae have chlorophyll a and c; their colour depends on fucoxanthin"],
                 ncert=ref("PK", "Algae (Phaeophyceae)"), secs=35)

statement_pair(T_PK, "Gymnosperms", "Intermediate",
               "In gymnosperms, the ovules are borne on megasporophylls, which may be clustered to form the female "
               "cones.",
               "In gymnosperms, the multicellular female gametophyte bears only a single archegonium.",
               True, False, "C",
               "Ovules and female gametophyte of gymnosperms",
               "NCERT: the ovules are borne on megasporophylls, which may be clustered to form the female cones. The "
               "megaspore mother cell divides meiotically to form four megaspores; one of them develops into a "
               "multicellular female gametophyte that bears two or more archegonia (female sex organs).",
               ["Statement I: true", "Statement II: false; the female gametophyte bears two or more archegonia"],
               ncert=ref("PK", "Gymnosperms"), secs=35)

match_list(T_PK, "Bryophytes", "Intermediate", "structure in bryophytes", "description",
           ["Archegonium", "Antheridium", "Gemma", "Protonema"],
           ["Creeping, green, branched and frequently filamentous stage that develops directly from a spore",
            "Green, multicellular, asexual bud that develops in a small receptacle on the thallus",
            "Flask-shaped sex organ that produces a single egg",
            "Sex organ that produces biflagellate antherozoids"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C",
           "Structures of bryophytes",
           "The archegonium (female sex organ) is flask-shaped and produces a single egg; the antheridium (male sex "
           "organ) produces biflagellate antherozoids. Gemmae are green, multicellular, asexual buds that develop in "
           "small receptacles called gemma cups on liverwort thalli. The protonema is the first stage of the moss "
           "gametophyte: creeping, green, branched and frequently filamentous, developing directly from a spore.",
           ["Archegonium -> III", "Antheridium -> IV", "Gemma -> II", "Protonema -> I"],
           why="The wrong codes swap the two sex organs, the gemma and the protonema, or the antheridium and the "
               "gemma.",
           ncert=ref("PK", "Bryophytes"), secs=45)

multi_statement(T_PK, "Pteridophytes", "Intermediate",
                "Which of the following statements are correct for a fern such as Dryopteris?",
                [("Its main plant body is a sporophyte differentiated into true root, stem and leaves.", True),
                 ("Its leaves are large (macrophylls).", True),
                 ("Its gametophyte needs cool, damp, shady places to grow.", True),
                 ("Its sporophyte remains attached to and nourished by the gametophyte throughout life.", False),
                 ("Its ovules are not enclosed by an ovary wall.", False)],
                [("a", "b", "c", "e"), ("a", "c"), ("b", "c", "d")], "D",
                "Features of ferns",
                "In pteridophytes the main plant body is a sporophyte with true root, stem and leaves; the leaves "
                "are small (microphylls) as in Selaginella or large (macrophylls) as in ferns. The spores give rise "
                "to a small, free-living, mostly photosynthetic gametophyte (prothallus), which needs cool, damp, "
                "shady places to grow. The sporophyte is the dominant, independent phase, and pteridophytes form no "
                "ovules or seeds.",
                ["(a) true", "(b) true: macrophylls as in ferns", "(c) true", "(d) false: that is the bryophyte "
                 "condition", "(e) false: ferns have no ovules"],
                why="The other combinations either add (d) or (e), or leave out the true statement (b).",
                ncert=ref("PK", "Pteridophytes"), secs=55)

direct(T_PK, "Bryophytes", "Intermediate",
       "In which of the following plants is the dominant, independent, photosynthetic phase haploid?",
       "Polytrichum",
       ["Pteris", "Cycas", "Selaginella"], "A",
       "Dominant phase in different plant groups",
       "In bryophytes such as the moss Polytrichum, the main plant body is haploid; it produces gametes and is "
       "called a gametophyte. In pteridophytes (Pteris, Selaginella) and gymnosperms (Cycas), the main plant body "
       "is the diploid sporophyte.",
       ["Moss: dominant phase = gametophyte (n)", "Fern, Selaginella, Cycas: dominant phase = sporophyte (2n)"],
       why="Pteris and Selaginella are pteridophytes and Cycas is a gymnosperm; in all three the dominant, "
           "independent plant is the diploid sporophyte.",
       ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=30)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following are true of members of Chlorophyceae but NOT of members of Phaeophyceae, "
                "according to NCERT's table of the divisions of algae?",
                [("Chlorophyll b is present.", True),
                 ("The stored food is starch.", True),
                 ("The motile cells bear 2-8 equal, apical flagella.", True),
                 ("Cellulose is a component of the cell wall.", False),
                 ("Members occur in brackish water and salt water.", False)],
                [("a", "b"), ("a", "c", "d"), ("b", "c", "e")], "C",
                "Comparing green and brown algae",
                "Chlorophyceae: chlorophyll a and b; stored food starch; cell wall of cellulose; 2-8 equal, apical "
                "flagella; fresh, brackish and salt water. Phaeophyceae: chlorophyll a and c with fucoxanthin; "
                "stored food mannitol and laminarin; cell wall of cellulose and algin; 2 unequal, lateral flagella; "
                "fresh water (rare), brackish and salt water.",
                ["(a), (b), (c) hold only for green algae", "(d) both have cellulose in the wall",
                 "(e) both occur in brackish and salt water"],
                why="(a) and (b) only misses the flagellar difference. The other combinations include (d) or (e), "
                    "which are shared by both classes.",
                ncert=ref("PK", "Algae (table: divisions of algae and their main characteristics)"), secs=70)

numerical(T_PK, "Pteridophytes", "Advanced",
          "How many of the following are formed by meiosis?\n\n(i) Spores in the capsule of a moss\n(ii) The four "
          "megaspores in a gymnosperm ovule\n(iii) Gemmae of Marchantia\n(iv) Microspores of Selaginella\n"
          "(v) Antherozoids of a fern\n(vi) The zygote of a moss",
          "3", ["2", "4", "5"], "C",
          sum([True, True, False, True, False, False]) == 3,
          "Where meiosis occurs in plant groups",
          "Meiosis produces spores: in mosses the spores are formed within the capsule after meiosis; in gymnosperms "
          "the megaspore mother cell divides meiotically to form four megaspores; in pteridophytes, including the "
          "heterosporous Selaginella, the sporangia produce spores by meiosis in spore mother cells. Gemmae are "
          "asexual buds of the haploid thallus, antherozoids are produced in antheridia on the haploid gametophyte, "
          "and a zygote is formed by fusion of gametes - none of these by meiosis.",
          ["By meiosis: (i), (ii), (iv)", "Not by meiosis: (iii) gemmae, (v) antherozoids, (vi) zygote",
           "Count = 3"],
          why="2 leaves out the Selaginella microspores, forgetting that heterosporous spores also arise by meiosis. "
              "4 counts gemmae as meiotic products, and 5 also counts the antherozoids.",
          ncert=ref("PK", "Bryophytes; Pteridophytes; Gymnosperms"), secs=60)

direct(T_PK, "Gymnosperms", "Advanced",
       "Which of the following is true of the female gametophyte of BOTH Selaginella and Pinus?",
       "It is retained on the parent sporophyte: for variable periods in Selaginella, and within the "
       "megasporangium in Pinus.",
       ["It develops from a microspore.", "It is enclosed within an ovary wall.",
        "It is the dominant, long-lived phase of the plant."], "B",
       "Retention of the female gametophyte",
       "In heterosporous pteridophytes such as Selaginella, the female gametophyte is retained on the parent "
       "sporophyte for variable periods, an event regarded as a precursor to the seed habit. In gymnosperms such "
       "as Pinus, the multicellular female gametophyte is retained within the megasporangium on the sporophyte.",
       ["Selaginella: female gametophyte retained on parent sporophyte",
        "Pinus: female gametophyte retained within megasporangium", "Common feature: retention"],
       why="Female gametophytes develop from megaspores, not microspores. Neither plant has an ovary, and in both "
           "the dominant phase is the sporophyte.",
       ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=45)

statement_pair(T_PK, "Pteridophytes", "Advanced",
               "In both Selaginella and Pinus, the sporophylls are arranged to form strobili (cones).",
               "In both Salvinia and Cycas, the ovules develop into naked seeds after fertilisation.",
               True, False, "C",
               "Strobili and seeds compared",
               "In some pteridophytes, such as Selaginella and Equisetum, the sporophylls form compact strobili. In "
               "gymnosperms such as Pinus, sporophylls are arranged spirally along an axis to form lax or compact "
               "strobili or cones. Salvinia, however, is a heterosporous pteridophyte; it forms no ovules or seeds. "
               "Only gymnosperms such as Cycas have naked seeds.",
               ["Statement I: true", "Statement II: false; Salvinia is a pteridophyte and has no seeds"],
               ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=45)

match_list(T_PK, "Gymnosperms", "Advanced", "structure in a gymnosperm", "origin or composition",
           ["Pollen grain", "Ovule", "Female gametophyte", "Seed"],
           ["Develops from one of the four megaspores", "Develops from the ovule after fertilisation",
            "Highly reduced male gametophyte developing from a microspore within the microsporangium",
            "Nucellus together with the envelopes that protect it"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D",
           "Origin of gymnosperm structures",
           "Microspores develop into a highly reduced male gametophyte, the pollen grain, within the microsporangia. "
           "The nucellus, protected by envelopes, forms the ovule. The megaspore mother cell in the nucellus forms "
           "four megaspores by meiosis, and one of them develops into the multicellular female gametophyte. After "
           "fertilisation the zygote forms the embryo and the ovules develop into seeds.",
           ["Pollen grain -> III", "Ovule -> IV", "Female gametophyte -> I", "Seed -> II"],
           why="The wrong codes swap the pollen grain and the ovule, the female gametophyte and the seed, or the ovule "
               "and the female gametophyte.",
           ncert=ref("PK", "Gymnosperms"), secs=55)
