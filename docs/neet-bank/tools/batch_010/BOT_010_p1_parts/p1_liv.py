
# =============================================================== 1. The Living World and Classification (5/6/5)
direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "Linnaeus used the term 'Systema' in the title of his publication, from which the word 'systematics' is "
       "derived. The title of that publication, as given in NCERT, is:",
       "Systema Naturae",
       ["Species Plantarum", "Genera Plantarum", "Origin of Species"], "A",
       "Origin of the word systematics",
       "The word systematics is derived from the Latin word 'systema', which means systematic arrangement of "
       "organisms. NCERT notes that Linnaeus used Systema Naturae as the title of his publication.",
       ["Systematics <- Latin 'systema'", "Linnaeus's publication: Systema Naturae"],
       why="NCERT names only Systema Naturae as Linnaeus's publication in this context. Origin of Species is "
           "Darwin's book; the other two titles are not the one NCERT cites.",
       ncert=ref("LW", "Diversity in the Living World (systematics)"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "NCERT states that plant families like Convolvulaceae and Solanaceae are included in one order, mainly on the "
       "basis of floral characters. That order is:",
       "Polymoniales",
       ["Sapindales", "Poales", "Primata"], "C",
       "Order as an assemblage of families",
       "An order is an assemblage of families that exhibit a few similar characters. NCERT's example: plant "
       "families like Convolvulaceae and Solanaceae are included in the order Polymoniales, mainly based on floral "
       "characters.",
       ["Order = assemblage of families with a few similar characters",
        "Convolvulaceae + Solanaceae -> order Polymoniales"],
       why="Sapindales is the order of mango and Poales the order of wheat in NCERT's table. Primata is an animal "
           "order (monkey, gorilla, gibbon).",
       ncert=ref("LW", "Taxonomic categories (order)"), secs=20)

direct(T_LIV, "Taxonomy and hierarchy", "Basic",
       "In taxonomic studies, a group of individual organisms with fundamental similarities, which can be "
       "distinguished from other closely related groups on the basis of distinct morphological differences, is "
       "considered a:",
       "species",
       ["genus", "family", "order"], "B",
       "Species as the basic taxonomic category",
       "NCERT: taxonomic studies consider a group of individual organisms with fundamental similarities as a "
       "species. One should be able to distinguish one species from the other closely related species on the basis "
       "of the distinct morphological differences.",
       ["Group of individuals with fundamental similarities = species",
        "Species are told apart by distinct morphological differences"],
       why="A genus is a group of related species, a family a group of related genera and an order an assemblage "
           "of families; none of these is a group of individuals with fundamental similarities.",
       ncert=ref("LW", "Taxonomic categories (species)"), secs=20)

direct(T_LIV, "Monera, Protista and Fungi", "Basic",
       "Amoeboid protozoans such as Amoeba move and capture their prey by putting out:",
       "pseudopodia (false feet)",
       ["cilia arranged in rows", "two flagella of unequal length", "a protein-rich pellicle"], "D",
       "Locomotion in amoeboid protozoans",
       "Amoeboid protozoans live in fresh water, sea water or moist soil. They move and capture their prey by "
       "putting out pseudopodia (false feet), as in Amoeba.",
       ["Amoeboid protozoans: pseudopodia", "Used both for movement and for capturing prey"],
       why="Rows of cilia are found in ciliated protozoans such as Paramoecium. Two unequal flagella and a "
           "pellicle are features of euglenoids such as Euglena.",
       ncert=ref("BC", "Kingdom Protista (protozoans)"), secs=20)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Basic",
               "Rod-shaped bacteria are called bacilli (singular: bacillus).",
               "Spherical bacteria are called cocci (singular: coccus).",
               True, True, "A",
               "Shapes of bacteria",
               "NCERT groups bacteria into four categories by shape: spherical coccus (pl. cocci), rod-shaped "
               "bacillus (pl. bacilli), comma-shaped vibrium (pl. vibrio) and spiral spirillum (pl. spirilla).",
               ["Statement I: rod-shaped = bacillus, true", "Statement II: spherical = coccus, true"],
               ncert=ref("BC", "Kingdom Monera"), secs=25)

direct(T_LIV, "Five kingdom classification", "Intermediate",
       "In NCERT's table of the characteristics of the five kingdoms, the body organisation described as "
       "'tissue/organ/organ system' belongs to kingdom:",
       "Animalia",
       ["Plantae", "Fungi", "Protista"], "B",
       "Body organisation in the five kingdoms",
       "In Whittaker's table, body organisation is: Monera and Protista - cellular; Fungi - multicellular/loose "
       "tissue; Plantae - tissue/organ; Animalia - tissue/organ/organ system. Only the animal kingdom is credited "
       "with the organ-system level.",
       ["Plantae: tissue/organ", "Animalia: tissue/organ/organ system", "Organ-system level -> Animalia"],
       why="Plantae is given only 'tissue/organ'. Fungi have 'multicellular/loose tissue' and Protista 'cellular' "
           "body organisation.",
       ncert=ref("BC", "Introduction (table: characteristics of the five kingdoms)"), secs=30)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                 "The spores of slime moulds can survive for many years, even under adverse conditions.",
                 "The spores of slime moulds possess true walls and are extremely resistant.",
                 True, True, True, "A",
                 "Survival of slime-mould spores",
                 "Under unfavourable conditions the plasmodium of a slime mould forms fruiting bodies bearing spores "
                 "at their tips. NCERT states that the spores possess true walls; they are extremely resistant and "
                 "survive for many years, even under adverse conditions. The resistant, true-walled spore is what "
                 "lets it survive so long.",
                 ["A: true", "R: true", "True walls make the spores extremely resistant, which is why they survive "
                  "for years -> R explains A"],
                 ncert=ref("BC", "Kingdom Protista (slime moulds)"), secs=40)

statement_pair(T_LIV, "Monera, Protista and Fungi", "Intermediate",
               "In basidiomycetes, the dikaryotic structure formed after plasmogamy ultimately gives rise to the "
               "basidium.",
               "In basidiomycetes, the basidia are arranged in fruiting bodies called ascocarps.",
               True, False, "C",
               "Sexual cycle of basidiomycetes",
               "In basidiomycetes, plasmogamy is by fusion of two somatic cells of different strains. The resulting "
               "structure is dikaryotic, which ultimately gives rise to the basidium. Karyogamy and meiosis take "
               "place in the basidium, producing four basidiospores. The basidia are arranged in fruiting bodies "
               "called basidiocarps; ascocarps are the fruiting bodies of ascomycetes.",
               ["Statement I: dikaryon -> basidium, true", "Statement II: basidia lie in basidiocarps, not "
                "ascocarps; false"],
               ncert=ref("BC", "Kingdom Fungi (Basidiomycetes)"), secs=35)

match_list(T_LIV, "Taxonomy and hierarchy", "Intermediate", "term", "meaning as given in NCERT",
           ["Identification", "Nomenclature", "Classification", "Systematics"],
           ["Grouping into convenient categories based on some easily observable characters",
            "Describing an organism correctly so that we know to what organism a name is attached",
            "A study that takes into account evolutionary relationships between organisms",
            "Naming of an organism according to standardised rules and criteria"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "A",
           "Basic terms of taxonomy",
           "Nomenclature (naming) is possible only when the organism is described correctly and we know to what "
           "organism the name is attached - this is identification. Nomenclature gives scientific names according "
           "to agreed principles and criteria. Classification is the process by which anything is grouped into "
           "convenient categories based on some easily observable characters. Systematics deals with the "
           "classification of organisms and takes into account evolutionary relationships between them.",
           ["Identification -> II", "Nomenclature -> IV", "Classification -> I", "Systematics -> III"],
           why="The wrong codes swap identification with nomenclature, classification with systematics, or "
               "nomenclature with classification.",
           ncert=ref("LW", "Diversity in the Living World"), secs=50)

multi_statement(T_LIV, "Monera, Protista and Fungi", "Intermediate",
                "Which of the following statements about fungi are correct?",
                [("In ascomycetes, conidia on germination produce mycelium.", True),
                 ("Penicillium is a multicellular ascomycete, whereas yeast (Saccharomyces) is a unicellular one.",
                  True),
                 ("In basidiomycetes, vegetative reproduction by fragmentation is common.", True),
                 ("Phycomycetes are found only in aquatic habitats.", False),
                 ("In ascomycetes, the conidiophores bear ascospores.", False)],
                [("a", "b"), ("a", "b", "c", "e"), ("b", "c", "d")], "C",
                "Features of classes of fungi",
                "Ascomycetes are mostly multicellular (Penicillium) or rarely unicellular (yeast, Saccharomyces). "
                "Their asexual spores, conidia, are produced exogenously on conidiophores and on germination "
                "produce mycelium; the sexual spores, ascospores, are produced endogenously in asci. In "
                "basidiomycetes asexual spores are generally not found, but vegetative reproduction by "
                "fragmentation is common. Phycomycetes occur in aquatic habitats, on decaying wood in moist and "
                "damp places, or as obligate parasites on plants.",
                ["(a) true", "(b) true", "(c) true", "(d) false: also on decaying wood and as obligate parasites "
                 "on plants", "(e) false: conidiophores bear conidia; ascospores form in asci"],
                why="(a) and (b) only leaves out the true statement (c). The other combinations include (d) or (e).",
                ncert=ref("BC", "Kingdom Fungi"), secs=60)

direct(T_LIV, "Monera, Protista and Fungi", "Intermediate",
       "In ciliated protozoans such as Paramoecium, the coordinated movement of rows of cilia causes the water laden "
       "with food to be steered into the:",
       "gullet",
       ["contractile vacuole", "pseudopodium", "spore-like infectious stage"], "A",
       "Feeding in ciliated protozoans",
       "Ciliated protozoans are aquatic, actively moving organisms because of the presence of thousands of cilia. "
       "They have a cavity (gullet) that opens to the outside of the cell surface. The coordinated movement of rows "
       "of cilia causes the water laden with food to be steered into the gullet.",
       ["Ciliated protozoans: thousands of cilia and a gullet", "Rows of cilia steer food-laden water into the "
        "gullet"],
       why="Pseudopodia are put out by amoeboid protozoans; an infectious spore-like stage is a feature of "
           "sporozoans. NCERT does not describe the cilia as steering food into a contractile vacuole.",
       ncert=ref("BC", "Kingdom Protista (protozoans)"), secs=30)

numerical(T_LIV, "Monera, Protista and Fungi", "Advanced",
          "NCERT lists the spores by which fungi reproduce. How many of the following are listed as SEXUAL spores "
          "of fungi?\n\nconidia, sporangiospores, zoospores, oospores, ascospores, basidiospores",
          "3", ["2", "4", "6"], "B",
          len([s for s, sexual in [("conidia", False), ("sporangiospores", False), ("zoospores", False),
                                   ("oospores", True), ("ascospores", True), ("basidiospores", True)]
               if sexual]) == 3,
          "Asexual and sexual spores of fungi",
          "NCERT: in fungi, asexual reproduction is by spores called conidia or sporangiospores or zoospores, and "
          "sexual reproduction is by oospores, ascospores and basidiospores.",
          ["Asexual: conidia, sporangiospores, zoospores", "Sexual: oospores, ascospores, basidiospores",
           "Count of sexual spores = 3"],
          why="2 leaves out the oospore, which is often forgotten. 4 wrongly counts zoospores as sexual because they "
              "are motile. 6 counts every spore as sexual.",
          ncert=ref("BC", "Kingdom Fungi"), secs=45)

multi_statement(T_LIV, "Five kingdom classification", "Advanced",
                "According to NCERT's table of the characteristics of the five kingdoms, which of the following are "
                "true of BOTH kingdom Monera and kingdom Fungi?",
                [("A cell wall is present, and it is not made of cellulose.", True),
                 ("A nuclear membrane is present.", False),
                 ("Heterotrophic nutrition (saprophytic or parasitic) is found among their members.", True),
                 ("Body organisation is multicellular/loose tissue.", False),
                 ("The cell type is eukaryotic.", False)],
                [("a", "b", "c"), ("c", "d"), ("a", "c", "e")], "D",
                "Comparing Monera and Fungi",
                "In the table, Monera: prokaryotic, cell wall non-cellulosic (polysaccharide + amino acid), nuclear "
                "membrane absent, cellular body organisation, nutrition autotrophic (chemosynthetic and "
                "photosynthetic) and heterotrophic (saprophytic/parasitic). Fungi: eukaryotic, cell wall present "
                "(without cellulose), nuclear membrane present, multicellular/loose tissue, heterotrophic "
                "(saprophytic/parasitic).",
                ["(a) both have non-cellulosic walls: true", "(b) Monera lack a nuclear membrane: false",
                 "(c) both include saprophytic/parasitic heterotrophs: true",
                 "(d) Monera are cellular: false", "(e) Monera are prokaryotic: false"],
                why="The other combinations include (b), (d) or (e), each of which holds only for Fungi.",
                ncert=ref("BC", "Introduction (table: characteristics of the five kingdoms)"), secs=70)

assertion_reason(T_LIV, "Taxonomy and hierarchy", "Advanced",
                 "The higher the taxonomic category, the greater is the difficulty of determining its relationship "
                 "to other taxa at the same level.",
                 "As we go higher from species to kingdom, the number of common characteristics goes on decreasing.",
                 True, True, True, "A",
                 "Characters shared at different levels of the hierarchy",
                 "NCERT: as we go higher from species to kingdom, the number of common characteristics goes on "
                 "decreasing; the lower the taxon, the more characteristics its members share. Because members of a "
                 "higher category share fewer characters, it becomes harder to determine its relationship to other "
                 "taxa at the same level, and the problem of classification becomes more complex.",
                 ["A: true", "R: true", "Fewer shared characters at higher levels is why relationships are harder "
                  "to judge -> R explains A"],
                 ncert=ref("LW", "Taxonomic categories"), secs=45)

statement_pair(T_LIV, "Binomial nomenclature", "Advanced",
               "In the name Panthera tigris, 'Panthera' is the generic name and 'tigris' is the specific epithet.",
               "Lion (Panthera leo), leopard (P. pardus) and tiger (P. tigris) have different specific epithets and "
               "therefore belong to three different genera.",
               True, False, "C",
               "Genus and specific epithet",
               "In a binomial, the first word is the genus and the second the specific epithet. NCERT notes that "
               "lion (Panthera leo), leopard (P. pardus) and tiger (P. tigris), with several common features, are "
               "all species of the same genus Panthera. A different specific epithet marks a different species, "
               "not a different genus.",
               ["Statement I: true", "Statement II: false; one genus (Panthera), three species"],
               ncert=ref("LW", "Taxonomic categories (genus)"), secs=40)

assertion_reason(T_LIV, "Monera, Protista and Fungi", "Advanced",
                 "Deuteromycetes are placed in a separate class because their mycelium is aseptate and coenocytic.",
                 "When the sexual forms of deuteromycetes are discovered, they are moved to ascomycetes and "
                 "basidiomycetes.",
                 False, True, False, "D",
                 "Why the deuteromycetes form a separate class",
                 "Deuteromycetes (imperfect fungi) are grouped together because only their asexual or vegetative "
                 "phases are known; their mycelium is septate and branched, not aseptate. NCERT adds that when the "
                 "sexual forms of these fungi are discovered, they are moved into the classes they rightly belong "
                 "to, ascomycetes and basidiomycetes.",
                 ["A: false - the mycelium is septate and branched; the grouping rests on the unknown sexual stage",
                  "R: true"],
                 ncert=ref("BC", "Kingdom Fungi (Deuteromycetes)"), secs=40)
