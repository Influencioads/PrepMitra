
# =============================================================== 1. The Living World and Classification (5/7/5)
direct(T_LIV, "Binomial nomenclature", "Basic",
       "The naming system in which every organism is given a name with two components, a generic name and a "
       "specific epithet, was given by:",
       "Carolus Linnaeus",
       ["R.H. Whittaker", "Aristotle", "M.W. Beijerinek"], "B",
       "Origin of binomial nomenclature",
       "Each scientific name has two components, the generic name and the specific epithet. This system of providing "
       "a name with two components is called binomial nomenclature. It was given by Carolus Linnaeus and is practised "
       "by biologists all over the world.",
       ["Two-component naming = binomial nomenclature", "Given by Carolus Linnaeus"],
       why="Whittaker proposed the five kingdom classification; Aristotle made the earliest attempt at a scientific "
           "basis of classification (trees, shrubs, herbs); Beijerinek worked on the tobacco mosaic virus.",
       ncert=ref("LW", "Diversity in the Living World (binomial nomenclature)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Some fungi live as symbionts. The symbiotic association of a fungus with the roots of higher plants is "
       "called:",
       "mycorrhiza",
       ["a lichen", "a root nodule", "a basidiocarp"], "C",
       "Fungi as symbionts",
       "Fungi are heterotrophic. Most are saprophytes and some are parasites. They can also live as symbionts: in "
       "association with algae as lichens, and with the roots of higher plants as mycorrhiza.",
       ["Fungus + alga = lichen", "Fungus + roots of higher plants = mycorrhiza"],
       why="A lichen is a fungus-alga association. Root nodules of legumes contain nitrogen-fixing bacteria. A "
           "basidiocarp is a fruiting body of basidiomycetes, not an association.",
       ncert=ref("BC", "Kingdom Fungi"), secs=20)

match_list(T_LIV, "Lichens, viruses and viroids", "Basic", "disease", "kind of causal agent",
           ["Citrus canker", "Potato spindle tuber disease", "Bovine spongiform encephalopathy (mad cow disease)",
            "Herpes"],
           ["Virus", "Prion", "Bacterium", "Viroid"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "D",
           "Causal agents of diseases",
           "Citrus canker is named by NCERT as a bacterial disease. The viroid discovered by T.O. Diener was found to "
           "be the causal agent of potato spindle tuber disease. Bovine spongiform encephalopathy (mad cow disease) "
           "in cattle is caused by a prion. Herpes, like mumps, small pox and influenza, is caused by a virus.",
           ["Citrus canker → bacterium", "Potato spindle tuber → viroid", "BSE → prion", "Herpes → virus"],
           why="The wrong codes swap the bacterium and the viroid, the prion and the virus, or the viroid and the "
               "prion.",
           ncert=ref("BC", "Kingdom Monera; Viruses, Viroids, Prions and Lichens"), secs=35)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "The genus Panthera (lion, tiger, leopard) and the genus Felis (cats) are placed together in the family:",
       "Felidae",
       ["Canidae", "Hominidae", "Muscidae"], "A",
       "Family as a taxonomic category",
       "A family is a group of related genera with still fewer similarities than genus and species. Among animals, "
       "the genus Panthera (lion, tiger, leopard) and the genus Felis (cats) are put in the family Felidae. The cat "
       "family Felidae is distinguished from the dog family Canidae on the basis of vegetative and reproductive "
       "features.",
       ["Panthera + Felis → family Felidae"],
       why="Canidae is the dog family. Hominidae is the family of man and Muscidae that of the housefly.",
       ncert=ref("LW", "Taxonomic Categories (family)"), secs=20)

statement_pair(T_LIV, "What is living", "Basic",
               "In plants, growth by cell division occurs continuously throughout their life span.",
               "Unicellular organisms also grow by cell division.",
               True, True, "A",
               "Growth by cell division",
               "Increase in mass and increase in number of individuals are twin characteristics of growth. A "
               "multicellular organism grows by cell division. In plants this growth by cell division occurs "
               "continuously throughout their life span; in animals it is seen only up to a certain age. "
               "Unicellular organisms also grow by cell division.",
               ["Statement I: true, plant growth by cell division is lifelong",
                "Statement II: true"],
               ncert=ref("LW", "Diversity in the Living World (characteristics of living organisms)"), secs=30)

direct(T_LIV, "Taxonomy and hierarchy", "Intermediate",
       "In the NCERT table of organisms with their taxonomic categories, which organism is placed in the order "
       "Poales?",
       "Wheat",
       ["Mango", "Housefly", "Man"], "D",
       "Order of organisms in NCERT's table",
       "NCERT's table places wheat (Triticum aestivum) in family Poaceae, order Poales, class Monocotyledonae and "
       "division Angiospermae. Mango is in order Sapindales, the housefly in order Diptera and man in order "
       "Primata.",
       ["Wheat: Poaceae → Poales", "Mango: Sapindales; housefly: Diptera; man: Primata"],
       why="Mango (Sapindales), housefly (Diptera) and man (Primata) are in other orders.",
       ncert=ref("LW", "Taxonomic Categories (Table 1.1)"), secs=25)

match_list(T_LIV, "Taxonomy and hierarchy", "Intermediate", "organism", "class in NCERT's table",
           ["Man", "Housefly", "Mango", "Wheat"],
           ["Insecta", "Monocotyledonae", "Mammalia", "Dicotyledonae"],
           "III I IV II", ["III I II IV", "I III IV II", "IV I III II"], "B",
           "Classes in NCERT's table of taxonomic categories",
           "In the NCERT table, man (Homo sapiens) is in class Mammalia, the housefly (Musca domestica) in class "
           "Insecta, mango (Mangifera indica) in class Dicotyledonae and wheat (Triticum aestivum) in class "
           "Monocotyledonae.",
           ["Man → Mammalia", "Housefly → Insecta", "Mango → Dicotyledonae", "Wheat → Monocotyledonae"],
           why="The wrong codes interchange the two plant classes, or man and the housefly, or a plant and an "
               "animal class.",
           ncert=ref("LW", "Taxonomic Categories (Table 1.1)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "When red dinoflagellates such as Gonyaulax multiply very rapidly, other marine animals such as "
                 "fishes may be killed.",
                 "Toxins are released by the dinoflagellates present in such large numbers.",
                 True, True, True, "A",
                 "Red tides and their effect",
                 "Some dinoflagellates, e.g. Gonyaulax, undergo such rapid multiplication that they make the sea "
                 "appear red (red tides). Toxins released by such large numbers may even kill other marine animals "
                 "such as fishes. So the toxins are the direct cause of the death of fishes.",
                 ["A: true", "R: true, and the toxins are what kill the fishes"],
                 ncert=ref("BC", "Kingdom Protista (Dinoflagellates)"), secs=35)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "A group of fungi grows in soil, on logs and tree stumps, and in living plant bodies as parasites. Asexual "
       "spores are generally not found, but vegetative reproduction by fragmentation is common. Sex organs are "
       "absent, and plasmogamy takes place by fusion of two somatic cells of different strains. Which pair consists "
       "only of fungi of this group?",
       "Ustilago and Puccinia",
       ["Neurospora and Claviceps", "Mucor and Albugo", "Alternaria and Trichoderma"], "C",
       "Identifying basidiomycetes",
       "The features listed are those of basidiomycetes: they grow in soil, on logs and tree stumps and in living "
       "plant bodies as parasites (rusts and smuts); asexual spores are generally not found but fragmentation is "
       "common; sex organs are absent and plasmogamy is by fusion of somatic cells of different strains. Agaricus "
       "(mushroom), Ustilago (smut) and Puccinia (rust fungus) are examples.",
       ["No asexual spores, no sex organs, somatic plasmogamy → basidiomycetes",
        "Examples: Agaricus, Ustilago, Puccinia"],
       why="Neurospora and Claviceps are ascomycetes; Mucor and Albugo are phycomycetes; Alternaria and Trichoderma "
           "are deuteromycetes.",
       ncert=ref("BC", "Kingdom Fungi (Basidiomycetes)"), secs=45)

numerical(T_LIV, "Five kingdom classification", "Intermediate",
          "In Whittaker's table of the characteristics of the five kingdoms, in how many kingdoms is a cell wall "
          "present in at least some members?",
          "4",
          ["3", "5", "2"], "B",
          (sum(1 for k, wall in {"Monera": "present", "Protista": "present in some", "Fungi": "present",
                                  "Plantae": "present", "Animalia": "absent"}.items() if wall != "absent") == 4),
          "Cell wall across the five kingdoms",
          "In Whittaker's table, the cell wall is non-cellulosic (polysaccharide + amino acid) in Monera, present in "
          "some Protista, present without cellulose in Fungi and present (cellulose) in Plantae. Only Animalia has "
          "no cell wall. So 4 kingdoms have a cell wall in at least some members.",
          ["Monera: present", "Protista: present in some", "Fungi: present", "Plantae: present",
           "Animalia: absent → 4"],
          why="3 leaves out Protista, where only some members have a cell wall. 5 forgets that animal cells lack a "
              "cell wall. 2 counts only the kingdoms with a cellulose or chitin wall and drops Monera too.",
          ncert=ref("BC", "Introduction (Table 2.1, characteristics of the five kingdoms)"), secs=40)

statement_pair(T_LIV, "Five kingdom classification", "Intermediate",
               "Aristotle divided animals into two groups: those which had red blood and those that did not.",
               "The two kingdom system of Linnaeus's time distinguished between unicellular and multicellular "
               "organisms.",
               True, False, "C",
               "Early systems of classification",
               "Aristotle classified plants into trees, shrubs and herbs, and divided animals into two groups, those "
               "with red blood and those without. In Linnaeus's time a two kingdom system (Plantae and Animalia) was "
               "developed; it did not distinguish between eukaryotes and prokaryotes, between unicellular and "
               "multicellular organisms, or between photosynthetic and non-photosynthetic organisms.",
               ["Statement I: true", "Statement II: false, the two kingdom system did not make this distinction"],
               ncert=ref("BC", "Introduction"), secs=35)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following organisms are placed in kingdom Protista in Whittaker's five kingdom "
                "classification?",
                [("Gonyaulax", True), ("Plasmodium", True), ("Mycoplasma", False), ("Trypanosoma", True),
                 ("Penicillium", False)],
                ["abc", "bde", "ad"], "C",
                "Members of Protista",
                "Kingdom Protista includes chrysophytes, dinoflagellates (e.g. Gonyaulax), euglenoids, slime moulds "
                "and protozoans; Plasmodium is a sporozoan and Trypanosoma a flagellated protozoan. Mycoplasma is a "
                "wall-less bacterium (Monera), and Penicillium is an ascomycete fungus (Fungi).",
                ["(a), (b), (d): protists", "(c) Mycoplasma → Monera", "(e) Penicillium → Fungi"],
                why="Each wrong combination includes Mycoplasma or Penicillium, or leaves out a protist.",
                ncert=ref("BC", "Kingdom Protista; Kingdom Monera; Kingdom Fungi"), secs=45)

direct(T_LIV, "Monera, Protista and Fungi", "Advanced",
       "An organism is prokaryotic and autotrophic, has a non-cellulosic cell wall, and may be unicellular, colonial "
       "or filamentous; its colonies are surrounded by a gelatinous sheath, some members fix nitrogen in "
       "specialised cells, and it often forms blooms in polluted water bodies. It is:",
       "a cyanobacterium, placed in kingdom Monera",
       ["a dinoflagellate, placed in kingdom Protista", "a green alga, placed in kingdom Plantae",
        "a chrysophyte, placed in kingdom Protista"], "B",
       "Identifying cyanobacteria",
       "Cyanobacteria (blue-green algae) are photosynthetic autotrophs with chlorophyll a. They are unicellular, "
       "colonial or filamentous, freshwater, marine or terrestrial; the colonies are generally surrounded by a "
       "gelatinous sheath; some, like Nostoc and Anabaena, fix atmospheric nitrogen in heterocysts; and they often "
       "form blooms in polluted water bodies. Being prokaryotes, they belong to kingdom Monera.",
       ["Prokaryotic → Monera", "Gelatinous sheath, heterocysts, blooms → cyanobacteria"],
       why="Dinoflagellates, chrysophytes and green algae are eukaryotes; a prokaryotic cell rules all three out.",
       ncert=ref("BC", "Kingdom Monera (Eubacteria)"), secs=45)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Bacteria that live in extreme salty areas belong to the eubacteria.",
                 "Eubacteria are characterised by the presence of a rigid cell wall and, if motile, a flagellum.",
                 False, True, False, "D",
                 "Archaebacteria and eubacteria",
                 "Bacteria of extreme salty areas are halophiles, which are archaebacteria, along with "
                 "thermoacidophiles (hot springs) and methanogens (marshy areas). Their differently structured cell "
                 "wall helps them survive in harsh habitats. So A is false. R is true: the true bacteria or "
                 "eubacteria are characterised by a rigid cell wall and, if motile, a flagellum.",
                 ["A: false, halophiles are archaebacteria", "R: true"],
                 ncert=ref("BC", "Kingdom Monera (Archaebacteria; Eubacteria)"), secs=40)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "Which of the following organisms obtain at least part of their nutrition heterotrophically, as "
                "described in NCERT?",
                [("Euglena kept in the dark", True),
                 ("Cuscuta", True),
                 ("Nostoc", False),
                 ("A slime mould", True),
                 ("Gonyaulax", False)],
                ["abc", "bde", "ade"], "D",
                "Heterotrophy across kingdoms",
                "Euglenoids are photosynthetic in sunlight but, when deprived of sunlight, behave like heterotrophs by "
                "predating on smaller organisms. Kingdom Plantae includes a few partially heterotrophic members, such "
                "as the parasite Cuscuta. Slime moulds are saprophytic protists. Nostoc is a photosynthetic "
                "cyanobacterium, and dinoflagellates such as Gonyaulax are mostly marine and photosynthetic.",
                ["(a) Euglena in dark: heterotroph", "(b) Cuscuta: parasite", "(d) slime mould: saprophyte",
                 "(c), (e): photosynthetic"],
                why="Each wrong combination includes Nostoc or Gonyaulax, which are photosynthetic, or leaves out one "
                    "of the heterotrophs.",
                ncert=ref("BC", "Kingdom Monera; Kingdom Protista; Kingdom Plantae"), secs=60)

statement_pair(T_LIV, "Five kingdom classification", "Advanced",
               "Kingdom Plantae includes algae, bryophytes, pteridophytes, gymnosperms and angiosperms.",
               "Whittaker's five kingdom classification places lichens in kingdom Fungi.",
               True, False, "C",
               "Plantae and the place of lichens",
               "Kingdom Plantae includes all eukaryotic chlorophyll-containing organisms commonly called plants: "
               "algae, bryophytes, pteridophytes, gymnosperms and angiosperms. In Whittaker's five kingdom "
               "classification there is no mention of lichens or of acellular organisms like viruses, viroids and "
               "prions, so lichens are not placed in kingdom Fungi.",
               ["Statement I: true", "Statement II: false, lichens find no mention in the five kingdoms"],
               ncert=ref("BC", "Kingdom Plantae; Viruses, Viroids, Prions and Lichens"), secs=35)

direct(T_LIV, "Lichens, viruses and viroids", "Advanced",
       "Which of the following correctly distinguishes a prion from a viroid?",
       "A prion consists of abnormally folded protein, whereas a viroid is a free RNA that lacks a protein coat",
       ["A prion is a free RNA, whereas a viroid consists of abnormally folded protein",
        "Both consist of a nucleic acid enclosed in a protein capsid",
        "A prion contains DNA in a capsid, whereas a viroid contains RNA of high molecular weight"], "A",
       "Prions and viroids",
       "A viroid, discovered by T.O. Diener in 1971, is a free RNA that lacks the protein coat found in viruses, and "
       "its RNA is of low molecular weight. Prions are infectious agents consisting of abnormally folded protein, "
       "similar in size to viruses; they cause diseases such as bovine spongiform encephalopathy in cattle.",
       ["Viroid: free low molecular weight RNA, no protein coat", "Prion: abnormally folded protein"],
       why="The second option reverses the two. A capsid around nucleic acid describes a virus, not either of these. "
           "Viroid RNA is of low, not high, molecular weight.",
       ncert=ref("BC", "Viruses, Viroids, Prions and Lichens"), secs=40)
