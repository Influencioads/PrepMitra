
# =============================================================== 1. The Living World and Classification (5/7/6)
direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "In the NCERT table of some organisms with their taxonomic categories, the housefly (Musca domestica) is "
       "placed in the phylum:",
       "Arthropoda",
       ["Chordata", "Insecta", "Diptera"], "A",
       "Taxonomic categories of the housefly",
       "NCERT's table gives the housefly as: genus Musca, family Muscidae, order Diptera, class Insecta, phylum "
       "Arthropoda, kingdom Animalia.",
       ["Housefly: Musca - Muscidae - Diptera - Insecta - Arthropoda - Animalia", "Phylum = Arthropoda"],
       why="Chordata is the phylum of man in the same table. Insecta is the housefly's class and Diptera its order, "
           "not its phylum.",
       ncert=ref("LW", "Taxonomic categories (table of organisms with their taxonomic categories)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "In fungi, the body consists of long, slender, thread-like structures called hyphae. The network of hyphae is "
       "known as:",
       "mycelium",
       ["conidiophore", "basidiocarp", "ascocarp"], "B",
       "Body of a fungus",
       "With the exception of yeasts, which are unicellular, fungi are filamentous. Their bodies consist of long, "
       "slender, thread-like structures called hyphae, and the network of hyphae is known as mycelium.",
       ["Thread-like unit = hypha", "Network of hyphae = mycelium"],
       why="A conidiophore is the special mycelium on which conidia are produced. Basidiocarps and ascocarps are "
           "fruiting bodies of basidiomycetes and ascomycetes.",
       ncert=ref("BC", "Kingdom Fungi"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "NCERT credits chemosynthetic autotrophic bacteria with playing a great role in:",
       "recycling nutrients such as nitrogen, phosphorus, iron and sulphur",
       ["producing methane (biogas) from the dung of ruminant animals",
        "fixing atmospheric nitrogen in specialised cells called heterocysts",
        "making curd from milk"], "B",
       "Role of chemosynthetic bacteria",
       "Chemosynthetic autotrophic bacteria oxidise various inorganic substances such as nitrates, nitrites and "
       "ammonia and use the released energy for their ATP production. They play a great role in recycling nutrients "
       "like nitrogen, phosphorus, iron and sulphur.",
       ["Chemosynthetic bacteria: energy from oxidising inorganic substances", "Role: recycling of N, P, Fe and S"],
       why="Methane is produced by methanogens (archaebacteria). Heterocysts are found in cyanobacteria such as "
           "Nostoc and Anabaena. Curd is made by heterotrophic bacteria.",
       ncert=ref("BC", "Kingdom Monera (eubacteria)"), secs=25)

statement_pair(T_LIV, "What is living", "Basic",
               "Plants respond to external factors such as light, water, temperature, other organisms and pollutants.",
               "If increase in body mass is taken as the criterion for growth, non-living objects cannot be said to "
               "grow.",
               True, False, "C",
               "Response to stimuli; growth as a criterion",
               "All organisms can sense and respond to environmental cues; plants respond to external factors like "
               "light, water, temperature, other organisms and pollutants. NCERT points out that non-living objects "
               "also grow if increase in body mass is taken as the criterion: mountains, boulders and sand mounds "
               "grow, though by accumulation of material on the surface.",
               ["Statement I: true", "Statement II: false; by the body-mass criterion, non-living objects also grow"],
               ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=30)

direct(T_LIV, "Five kingdom classification", "Basic",
       "According to NCERT, members of kingdom Animalia store their food reserves as:",
       "glycogen or fat",
       ["starch", "cellulose", "chitin"], "D",
       "Food reserves of animals",
       "Members of Animalia are heterotrophic, eukaryotic, multicellular organisms whose cells lack cell walls. They "
       "directly or indirectly depend on plants for food, digest their food in an internal cavity and store food "
       "reserves as glycogen or fat.",
       ["Animalia: holozoic nutrition", "Food reserve: glycogen or fat"],
       why="Starch is the food reserve of plants. Cellulose is a plant cell-wall material and chitin is found in fungal "
           "cell walls; neither is the stored food of animals.",
       ncert=ref("BC", "Kingdom Animalia"), secs=20)

match_list(T_LIV, "Monera, Protista and Fungi", "Intermediate", "fungus", "kind of sexual spore",
           ["Rhizopus", "Claviceps", "Puccinia", "Alternaria"],
           ["Basidiospores", "Sexual stage not known", "Zygospores", "Ascospores"],
           "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A",
           "Classes of fungi and their sexual spores",
           "Rhizopus (the bread mould) is a phycomycete, in which a zygospore is formed by the fusion of two gametes. "
           "Claviceps is an ascomycete; its sexual spores, ascospores, are produced endogenously in asci. Puccinia "
           "(wheat rust) is a basidiomycete, which forms basidiospores on the basidium. Alternaria is a "
           "deuteromycete, a group in which only the asexual or vegetative phases are known.",
           ["Rhizopus: phycomycete -> zygospore", "Claviceps: ascomycete -> ascospores",
            "Puccinia: basidiomycete -> basidiospores", "Alternaria: deuteromycete -> no known sexual stage"],
           why="The wrong codes swap the phycomycete and the ascomycete, the basidiomycete and the deuteromycete, or "
               "the ascomycete and the basidiomycete.",
           ncert=ref("BC", "Kingdom Fungi (Phycomycetes, Ascomycetes, Basidiomycetes, Deuteromycetes)"), secs=45)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "Yeast is a unicellular fungus.",
                 "All members of the class Ascomycetes are unicellular.",
                 True, False, False, "C",
                 "Unicellular and multicellular ascomycetes",
                 "With the exception of yeasts, which are unicellular, fungi are filamentous. The ascomycetes are "
                 "mostly multicellular (e.g. Penicillium) and only rarely unicellular (e.g. yeast, Saccharomyces).",
                 ["A: true", "R: false; ascomycetes are mostly multicellular, rarely unicellular"],
                 ncert=ref("BC", "Kingdom Fungi (Ascomycetes)"), secs=35)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about archaebacteria are correct?",
                [("They differ from other bacteria in having a different cell wall structure.", True),
                 ("Methanogens among them are present in the guts of several ruminant animals such as cows and "
                  "buffaloes.", True),
                 ("The halophiles among them live in hot springs.", False),
                 ("The cyanobacteria (blue-green algae) belong to this group.", False)],
                [("a", "b", "c"), ("b", "d"), ("a", "c", "d")], "B",
                "Archaebacteria",
                "Archaebacteria live in some of the harshest habitats: extreme salty areas (halophiles), hot springs "
                "(thermoacidophiles) and marshy areas (methanogens). They differ from other bacteria in having a "
                "different cell wall structure, which is responsible for their survival in extreme conditions. "
                "Methanogens are present in the guts of several ruminant animals such as cows and buffaloes and are "
                "responsible for the production of methane (biogas) from their dung. Cyanobacteria are described by "
                "NCERT under the eubacteria ('true bacteria').",
                ["(a) true", "(b) true", "(c) false; hot springs = thermoacidophiles; halophiles = salty areas",
                 "(d) false; cyanobacteria are eubacteria"],
                ncert=ref("BC", "Kingdom Monera (archaebacteria, eubacteria)"), secs=50)

statement_pair(T_LIV, "Five kingdom classification", "Intermediate",
               "The cell body of a protist contains a well-defined nucleus and other membrane-bound organelles.",
               "Some protists have flagella or cilia.",
               True, True, "A",
               "Protistan cells",
               "All members of Protista are eukaryotes. The protistan cell body contains a well-defined nucleus and other "
               "membrane-bound organelles, and some have flagella or cilia.",
               ["Statement I: true (protists are eukaryotes)", "Statement II: true"],
               ncert=ref("BC", "Kingdom Protista"), secs=30)

direct(T_LIV, "Lichens, viruses and viroids", "Intermediate",
       "Which of the following is true of both viruses and viroids, but NOT of prions?",
       "They contain nucleic acid as their genetic material.",
       ["They have a protein coat around the nucleic acid.", "They consist of abnormally folded protein.",
        "They contain both DNA and RNA."], "D",
       "Comparing viruses, viroids and prions",
       "Viruses contain genetic material that is either RNA or DNA, within a protein capsid. A viroid is a free RNA "
       "that lacks the protein coat found in viruses. Prions are infectious agents consisting of abnormally folded "
       "protein. So only viruses and viroids carry nucleic acid as genetic material.",
       ["Virus: RNA or DNA + protein coat", "Viroid: free RNA, no protein coat", "Prion: abnormally folded protein"],
       why="Viroids lack the protein coat. Abnormally folded protein describes prions. No virus contains both DNA and "
           "RNA, and a viroid has only RNA.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)

direct(T_LIV, "What is living", "Intermediate",
       "Taking all the properties of life together, NCERT describes living organisms as:",
       "self-replicating, evolving and self-regulating interactive systems capable of responding to external stimuli",
       ["isolated metabolic reactions that can be demonstrated in a test tube",
        "systems that grow only by the accumulation of material on their surface",
        "systems defined by reproduction, so that a non-reproducing organism is non-living"], "D",
       "What is living",
       "NCERT concludes that living organisms are self-replicating, evolving and self-regulating interactive systems "
       "capable of responding to external stimuli. Isolated metabolic reactions in vitro are not living things, "
       "though they are surely living reactions. Growth by accumulation on the surface is how non-living objects "
       "grow. Reproduction is not an all-inclusive defining feature, since many organisms (mules, sterile worker bees, "
       "infertile couples) do not reproduce.",
       ["Living organisms = self-replicating, evolving, self-regulating interactive systems",
        "They respond to external stimuli"],
       why="In vitro reactions are not living things; surface accumulation is non-living growth; reproduction cannot "
           "be an all-inclusive defining characteristic.",
       ncert=ref("LW", "Diversity in the Living World (what is living)"), secs=35)

_mango = ["Mangifera", "Anacardiaceae", "Sapindales", "Dicotyledonae", "Angiospermae"]
numerical(T_LIV, "Taxonomy and hierarchy", "Intermediate",
          "In the NCERT table of organisms with their taxonomic categories, how many taxonomic categories of mango "
          "lie between its genus Mangifera and its division Angiospermae (both excluded)?",
          "3", ["2", "4", "5"], "A",
          len(_mango[1:-1]) == 3,
          "Taxonomic hierarchy of mango",
          "Mango: genus Mangifera, family Anacardiaceae, order Sapindales, class Dicotyledonae, division Angiospermae. "
          "Between the genus and the division (both excluded) lie the family, the order and the class.",
          ["Hierarchy: genus - family - order - class - division", "Between genus and division: family, order, class",
           "Count = 3"],
          why="2 leaves out one category (usually the class); 4 counts the genus or the division as well; 5 counts the "
              "whole list including both ends.",
          ncert=ref("LW", "Taxonomic categories (table of organisms with their taxonomic categories)"), secs=40)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following organisms are eukaryotic and can carry out photosynthesis?",
                [("Chlamydomonas", True), ("Nostoc", False), ("Chlorella", True),
                 ("Euglena (in the presence of sunlight)", True), ("Mucor", False)],
                [("a", "b", "c", "d"), ("b", "c", "d"), ("a", "d", "e")], "C",
                "Eukaryotic photosynthetic organisms",
                "Chlamydomonas and Chlorella are green algae (placed in Protista in the five kingdom system) and are "
                "photosynthetic eukaryotes. Euglena is a protist that is photosynthetic in the presence of sunlight. "
                "Nostoc is a cyanobacterium: photosynthetic but prokaryotic (Monera). Mucor is a fungus: eukaryotic but "
                "heterotrophic.",
                ["(a) eukaryote, photosynthetic", "(b) prokaryote", "(c) eukaryote, photosynthetic",
                 "(d) eukaryote, photosynthetic in sunlight", "(e) heterotrophic fungus"],
                why="Any option with (b) includes a prokaryote; an option with (e) includes a heterotrophic fungus.",
                ncert=ref("BC", "Kingdom Monera; Kingdom Protista; Kingdom Fungi"), secs=60)

assertion_reason(T_LIV, "Five kingdom classification", "Advanced",
                 "Nostoc and Chlamydomonas, though both photosynthetic, are placed in different kingdoms in the five "
                 "kingdom classification.",
                 "Cell structure (prokaryotic or eukaryotic) is one of the main criteria used by Whittaker to "
                 "separate kingdoms.",
                 True, True, True, "A",
                 "Criteria of the five kingdom system",
                 "Whittaker's main criteria were cell structure, body organisation, mode of nutrition, reproduction and "
                 "phylogenetic relationships. Nostoc is prokaryotic and goes to Monera; Chlamydomonas is a eukaryote "
                 "and goes to Protista. The same mode of nutrition does not keep them together because they differ in "
                 "cell structure.",
                 ["A: true (Monera vs Protista)", "R: true", "The prokaryotic/eukaryotic difference is why they are "
                  "separated, so R explains A"],
                 ncert=ref("BC", "Introduction (five kingdom classification); Kingdom Monera; Kingdom Protista"),
                 secs=45)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Advanced",
               "In ascomycetes, both the asexual spores (conidia) and the sexual spores (ascospores) are produced "
               "exogenously.",
               "In deuteromycetes, the mycelium is septate and branched.",
               False, True, "D",
               "Spore formation in ascomycetes; mycelium of deuteromycetes",
               "In ascomycetes the asexual spores, conidia, are produced exogenously on special mycelium called "
               "conidiophores, but the sexual spores, ascospores, are produced endogenously in sac-like asci. "
               "Deuteromycetes reproduce only by asexual spores (conidia), and their mycelium is septate and branched.",
               ["Statement I: false; ascospores are endogenous", "Statement II: true"],
               ncert=ref("BC", "Kingdom Fungi (Ascomycetes, Deuteromycetes)"), secs=40)

direct(T_LIV, "Monera, Protista and Fungi", "Advanced",
       "In some fungi, an intervening dikaryotic stage (n + n) occurs between plasmogamy and karyogamy. In which of the "
       "following pairs can BOTH fungi show this stage?",
       "Claviceps and Agaricus",
       ["Mucor and Albugo", "Alternaria and Trichoderma", "Rhizopus and Puccinia"], "B",
       "Dikaryophase in fungi",
       "The dikaryotic stage occurs in ascomycetes and basidiomycetes. Claviceps is an ascomycete and Agaricus a "
       "basidiomycete, so both can show it. Mucor, Albugo and Rhizopus are phycomycetes; Alternaria and Trichoderma "
       "are deuteromycetes, whose sexual stages are not known.",
       ["Dikaryon: ascomycetes and basidiomycetes", "Claviceps = ascomycete; Agaricus = basidiomycete"],
       why="Mucor and Albugo are both phycomycetes; Alternaria and Trichoderma are deuteromycetes with no known sexual "
           "stage; in the last pair Rhizopus is a phycomycete.",
       ncert=ref("BC", "Kingdom Fungi"), secs=50)

match_list(T_LIV, "Monera, Protista and Fungi", "Advanced", "group", "asexual reproduction as described in NCERT",
           ["Phycomycetes", "Ascomycetes", "Basidiomycetes", "Bacteria"],
           ["Mainly by fission; spores may form under unfavourable conditions",
            "Motile zoospores or non-motile aplanospores formed endogenously in a sporangium",
            "Asexual spores generally not found; fragmentation common",
            "Conidia produced exogenously on conidiophores"],
           "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "D",
           "Asexual reproduction in fungi and bacteria",
           "Phycomycetes reproduce asexually by zoospores (motile) or aplanospores (non-motile), produced endogenously "
           "in a sporangium. Ascomycetes form conidia exogenously on conidiophores. In basidiomycetes asexual spores are "
           "generally not found, but vegetative reproduction by fragmentation is common. Bacteria reproduce mainly by "
           "fission; under unfavourable conditions they may produce spores.",
           ["Phycomycetes -> II", "Ascomycetes -> IV", "Basidiomycetes -> III", "Bacteria -> I"],
           why="The wrong codes exchange the endogenous and exogenous spores of phycomycetes and ascomycetes, give "
               "basidiomycetes the bacterial mode, or give them conidia.",
           ncert=ref("BC", "Kingdom Monera; Kingdom Fungi"), secs=60)

assertion_reason(T_LIV, "Lichens, viruses and viroids", "Advanced",
                 "Viroids are larger than viruses.",
                 "The RNA of a viroid is of low molecular weight.",
                 False, True, False, "D",
                 "Size of viroids",
                 "In 1971, T.O. Diener discovered a new infectious agent that was smaller than viruses and caused "
                 "potato spindle tuber disease. It was a free RNA lacking the protein coat found in viruses, hence the "
                 "name viroid. The RNA of the viroid was of low molecular weight.",
                 ["A: false; viroids are smaller than viruses", "R: true"],
                 ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)
