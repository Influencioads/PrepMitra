
# =============================================================== 2. Plant Kingdom (5/6/5)
direct(T_PK, "Bryophytes", "Basic",
       "The plant body of the liverwort Marchantia is a thallus that is:",
       "dorsiventral and closely appressed to the substrate",
       ["erect and radially symmetrical", "differentiated into true root, stem and leaves",
        "a creeping, branched, filamentous protonema"], "A",
       "Plant body of a liverwort",
       "The plant body of a liverwort is thalloid, e.g. Marchantia. The thallus is dorsiventral and closely appressed "
       "to the substrate. Liverworts grow in moist, shady habitats such as banks of streams, marshy ground, damp soil "
       "and the bark of trees.",
       ["Liverwort body = thallus", "Marchantia thallus: dorsiventral, closely appressed to the substrate"],
       why="The thallus is not erect or radially symmetrical. Bryophytes lack true roots, stems and leaves. The "
           "protonema is the first stage of the moss gametophyte, not the liverwort thallus.",
       ncert=ref("PK", "Bryophytes (liverworts)"), secs=25)

direct(T_PK, "Pteridophytes", "Basic",
       "Pteridophytes in which all the spores produced are of a similar kind are called:",
       "homosporous",
       ["heterosporous", "isogamous", "oogamous"], "B",
       "Homospory and heterospory",
       "In the majority of pteridophytes all the spores are of similar kinds; such plants are called homosporous. "
       "Genera like Selaginella and Salvinia, which produce two kinds of spores, macro (large) and micro (small) "
       "spores, are known as heterosporous.",
       ["One kind of spore = homosporous", "Two kinds (micro and macro) = heterosporous"],
       why="Heterosporous plants produce two kinds of spores. Isogamous and oogamous describe the kind of gametes that "
           "fuse, not the spores.",
       ncert=ref("PK", "Pteridophytes"), secs=20)

direct(T_PK, "Algae", "Basic",
       "Sexual reproduction in members of Phaeophyceae (brown algae) is:",
       "isogamous, anisogamous or oogamous",
       ["only oogamous", "only isogamous", "absent; they reproduce only by zoospores"], "C",
       "Sexual reproduction in brown algae",
       "In brown algae, asexual reproduction is mostly by biflagellate zoospores. Sexual reproduction may be "
       "isogamous, anisogamous or oogamous. Union of gametes may take place in water or within the oogonium "
       "(oogamous species).",
       ["Brown algae: all three types of sexual reproduction occur"],
       why="Brown algae are not restricted to one type of gamete fusion, and they do reproduce sexually.",
       ncert=ref("PK", "Algae (Phaeophyceae)"), secs=25)

statement_pair(T_PK, "Bryophytes", "Basic",
               "The sex organs of bryophytes are multicellular.",
               "The antheridium of a bryophyte produces a single antherozoid.",
               True, False, "C",
               "Sex organs of bryophytes",
               "The main plant body of a bryophyte is haploid and produces gametes, so it is a gametophyte. The sex "
               "organs in bryophytes are multicellular. The male sex organ, the antheridium, produces biflagellate "
               "antherozoids (many of them). The female sex organ, the archegonium, is flask-shaped and produces a "
               "single egg.",
               ["Statement I: true", "Statement II: false; it is the archegonium that produces a single egg; the "
                "antheridium produces antherozoids"],
               ncert=ref("PK", "Bryophytes"), secs=30)

match_list(T_PK, "Algae", "Basic", "plant", "group",
           ["Ulothrix", "Laminaria", "Gelidium", "Lycopodium"],
           ["Brown alga", "Pteridophyte", "Green alga", "Red alga"],
           "III I IV II", ["I III IV II", "III I II IV", "IV I III II"], "D",
           "Identifying members of the plant kingdom",
           "Ulothrix is a filamentous green alga (Chlorophyceae). Laminaria is a brown alga (Phaeophyceae). Gelidium is "
           "a red alga (Rhodophyceae), one of the sources of agar. Lycopodium is a pteridophyte of the class "
           "Lycopsida.",
           ["Ulothrix → green alga; Laminaria → brown alga", "Gelidium → red alga; Lycopodium → pteridophyte"],
           why="The wrong codes swap the green and brown algae, the red alga and the pteridophyte, or the green and red "
               "algae.",
           ncert=ref("PK", "Algae; Pteridophytes"), secs=30)

assertion_reason(T_PK, "Gymnosperms", "Intermediate",
                 "Gymnosperms are heterosporous.",
                 "The roots of Pinus have a fungal association in the form of mycorrhiza.",
                 True, True, False, "B",
                 "Gymnosperms: spores and roots",
                 "Gymnosperms are heterosporous: they produce haploid microspores and megaspores within sporangia "
                 "borne on sporophylls. Separately, the roots of some genera have a fungal association in the form of "
                 "mycorrhiza (Pinus), while in others (Cycas) coralloid roots are associated with nitrogen-fixing "
                 "cyanobacteria. The root association has nothing to do with the kinds of spores formed.",
                 ["A: true", "R: true", "R is a feature of the roots, unrelated to spore production"],
                 ncert=ref("PK", "Gymnosperms"), secs=35)

assertion_reason(T_PK, "Pteridophytes", "Intermediate",
                 "The prothallus that develops from a spore of a fern is haploid.",
                 "In pteridophytes, the spores are produced by meiosis in spore mother cells within the sporangia.",
                 True, True, True, "A",
                 "Origin of the pteridophyte gametophyte",
                 "The sporophyte bears sporangia, which produce spores by meiosis in spore mother cells. Each spore is "
                 "therefore haploid, and it germinates to give rise to a small, multicellular, free-living, mostly "
                 "photosynthetic thalloid gametophyte called the prothallus. The gametophyte is haploid because the "
                 "spore it grows from was formed by meiosis.",
                 ["Spore mother cell (2n) → meiosis → spores (n)", "Spore (n) → prothallus (n)"],
                 ncert=ref("PK", "Pteridophytes"), secs=40)

statement_pair(T_PK, "Algae", "Intermediate",
               "The red thalli of most red algae are multicellular, and some red algae have a complex body "
               "organisation.",
               "All members of Rhodophyceae live in salt water; none is found in fresh water.",
               True, False, "C",
               "Body and habitat of red algae",
               "NCERT states that the red thalli of most of the red algae are multicellular and some of them have "
               "complex body organisation. The majority of red algae are marine, but NCERT's table gives their habitat "
               "as fresh water (some), brackish water and salt water (most); so some red algae do live in fresh water.",
               ["Statement I: true", "Statement II: false; some red algae are fresh-water forms"],
               ncert=ref("PK", "Algae (Rhodophyceae; Table 3.1)"), secs=35)

direct(T_PK, "Gymnosperms", "Intermediate",
       "Which of the following pairs consists of two plants that are both heterosporous?",
       "Pinus and Salvinia",
       ["Funaria and Cycas", "Marchantia and Salvinia", "Polytrichum and Selaginella"], "D",
       "Heterospory in pteridophytes and gymnosperms",
       "Heterospory (production of two kinds of spores, microspores and megaspores) is found in some pteridophytes, "
       "such as Selaginella and Salvinia, and in all gymnosperms, which produce haploid microspores and megaspores. "
       "Bryophytes such as Funaria, Polytrichum (mosses) and Marchantia (a liverwort) do not produce two kinds of "
       "spores.",
       ["Gymnosperms (Pinus, Cycas): heterosporous", "Selaginella, Salvinia: heterosporous pteridophytes",
        "Mosses and liverworts: not heterosporous"],
       why="Each wrong pair contains a bryophyte (Funaria, Marchantia or Polytrichum), which does not form "
           "microspores and megaspores.",
       ncert=ref("PK", "Pteridophytes; Gymnosperms"), secs=40)

match_list(T_PK, "Algae", "Intermediate", "group", "habitat as given in NCERT",
           ["Chlorophyceae", "Phaeophyceae", "Rhodophyceae", "Bryophytes"],
           ["Fresh water (some), brackish water, salt water (most)", "Moist, shaded areas in the hills",
            "Fresh water, brackish water, salt water", "Fresh water (rare), brackish water, salt water"],
           "III IV I II", ["I IV III II", "III I IV II", "IV III I II"], "A",
           "Habitats of the classes of algae",
           "NCERT's table of the divisions of algae gives the habitat of Chlorophyceae as fresh water, brackish water "
           "and salt water; of Phaeophyceae as fresh water (rare), brackish water and salt water; and of Rhodophyceae "
           "as fresh water (some), brackish water and salt water (most). Bryophytes are found commonly growing in "
           "moist, shaded areas in the hills.",
           ["Green algae: all three waters, no qualifier", "Brown algae: fresh water rare",
            "Red algae: some fresh water, most marine", "Bryophytes: moist shaded hills"],
           why="The wrong codes interchange the 'rare' and 'some' qualifiers of the brown and red algae, or give the "
               "unqualified habitat to brown or red algae.",
           ncert=ref("PK", "Algae (Table 3.1); Bryophytes"), secs=45)

assertion_reason(T_PK, "Algae", "Intermediate",
                 "Sexual reproduction in all algae is oogamous.",
                 "In Spirogyra, fusion takes place between non-flagellated gametes that are similar in size.",
                 False, True, False, "D",
                 "Kinds of sexual reproduction in algae",
                 "Sexual reproduction in algae varies. Fusion of two gametes similar in size is isogamous: the gametes "
                 "may be flagellated (Chlamydomonas) or non-flagellated (Spirogyra). Fusion of two gametes dissimilar "
                 "in size is anisogamous (species of Eudorina). Fusion of a large, non-motile female gamete "
                 "with a smaller, motile male gamete is oogamous (Volvox, Fucus). So not all algae are oogamous; "
                 "Spirogyra itself is an exception.",
                 ["A: false; isogamy and anisogamy also occur", "R: true (isogamy with non-flagellated gametes)"],
                 ncert=ref("PK", "Algae"), secs=40)

multi_statement(T_PK, "Bryophytes", "Advanced",
                "A plant has a free-living, photosynthetic gametophyte that bears antheridia and archegonia. Its "
                "sporophyte remains attached to the gametophyte and is differentiated into a foot, seta and capsule. "
                "Which of the following statements about this plant are correct?",
                [("Its antherozoids are biflagellate.", True),
                 ("It needs water for fertilisation.", True),
                 ("Its spores are formed within the capsule after meiosis.", True),
                 ("Its sporophyte has xylem and phloem.", False),
                 ("Its zygote undergoes meiosis immediately to form spores.", False)],
                [("a", "b", "d"), ("b", "c", "e"), ("a", "c", "d", "e")], "B",
                "Applying the features of bryophytes",
                "A dominant free-living gametophyte bearing antheridia and archegonia, with a dependent sporophyte of "
                "foot, seta and capsule, describes a bryophyte. Its antheridia produce biflagellate antherozoids, which "
                "are released into water and reach the archegonium, so water is needed for fertilisation. The zygote "
                "does not undergo reduction division immediately; it forms a multicellular sporophyte, and spores are "
                "produced within the capsule after meiosis. Bryophytes lack vascular tissue, which first appears in "
                "pteridophytes.",
                ["Identify: bryophyte", "(a), (b), (c) true", "(d) false: no vascular tissue",
                 "(e) false: the zygote forms the sporophyte first"],
                why="Any option containing (d) or (e) includes a false statement; (a), (b) and (c) are all true, so a "
                    "combination missing one of them is incomplete.",
                ncert=ref("PK", "Bryophytes"), secs=60)

multi_statement(T_PK, "Algae", "Advanced",
                "Which of the following features are shared by members of Chlorophyceae and Rhodophyceae, according to "
                "NCERT's table of the divisions of algae?",
                [("Chlorophyll a is present.", True),
                 ("Cellulose is a component of the cell wall.", True),
                 ("Motile cells bear 2–8 equal, apical flagella.", False),
                 ("Food is stored as mannitol.", False),
                 ("Phycoerythrin is the major pigment.", False)],
                [("a", "c"), ("a", "b", "e"), ("b", "d")], "C",
                "Comparing green and red algae",
                "Chlorophyceae: chlorophyll a and b; stored food starch; cell wall cellulose; 2–8 equal, apical flagella. "
                "Rhodophyceae: chlorophyll a and d with phycoerythrin; stored food floridean starch; cell wall of "
                "cellulose, pectin and polysulphate esters; flagella absent. So both have chlorophyll a and cellulose "
                "in the cell wall. Mannitol is stored by brown algae.",
                ["(a) both: true", "(b) both have cellulose in the wall: true",
                 "(c) red algae lack flagella", "(d) mannitol = brown algae", "(e) phycoerythrin only in red algae"],
                why="(c), (e) apply only to one of the two classes and (d) to neither.",
                ncert=ref("PK", "Algae (Table 3.1)"), secs=60)

direct(T_PK, "Pteridophytes", "Advanced",
       "A plant has true roots, stem and leaves with vascular tissue but forms no seeds. Its sporophylls are "
       "compactly arranged in strobili, it produces two kinds of spores, and its female gametophyte is retained on "
       "the parent sporophyte for a variable period. Among the following, the plant is:",
       "Selaginella",
       ["Equisetum", "Pinus", "Dryopteris"], "A",
       "Identifying a heterosporous pteridophyte with strobili",
       "Vascular tissue without seeds indicates a pteridophyte. NCERT names Selaginella and Equisetum as pteridophytes "
       "whose sporophylls form compact strobili, and Selaginella and Salvinia as heterosporous genera whose female "
       "gametophytes are retained on the parent sporophyte. Only Selaginella has all these features.",
       ["Vascular, no seeds → pteridophyte", "Strobili: Selaginella, Equisetum",
        "Heterosporous: Selaginella, Salvinia", "Common to both → Selaginella"],
       why="Equisetum has strobili but is not one of the heterosporous genera named. Pinus is a gymnosperm and forms "
           "seeds. Dryopteris is a fern and is neither named as forming strobili nor as heterosporous.",
       ncert=ref("PK", "Pteridophytes"), secs=60)

statement_pair(T_PK, "Gymnosperms", "Advanced",
               "In gymnosperms, the female gametophyte that bears the archegonia develops from one of the four "
               "megaspores formed by meiosis of the megaspore mother cell.",
               "In gymnosperms, the pollen grains develop within the megasporangia.",
               True, False, "C",
               "Development of gametophytes in gymnosperms",
               "The megaspore mother cell, differentiated from a cell of the nucellus, divides meiotically to form four "
               "megaspores. One of them, enclosed within the megasporangium, develops into a multicellular female "
               "gametophyte that bears two or more archegonia. The microspores develop into the highly reduced male "
               "gametophyte, the pollen grain, and the development of pollen grains takes place within the "
               "microsporangia, not the megasporangia.",
               ["Statement I: true", "Statement II: false; pollen grains develop in microsporangia"],
               ncert=ref("PK", "Gymnosperms"), secs=45)

_BROWN = {"Ectocarpus": True, "Dictyota": True, "Porphyra": False, "Laminaria": True, "Polysiphonia": False,
          "Sargassum": True, "Fucus": True, "Gelidium": False, "Chara": False}
numerical(T_PK, "Algae", "Advanced",
          "How many of the following algae are members of Phaeophyceae?\n"
          "Ectocarpus, Dictyota, Porphyra, Laminaria, Polysiphonia, Sargassum, Fucus, Gelidium, Chara",
          "5", ["4", "6", "3"], "B", sum(_BROWN.values()) == 5,
          "Common members of the classes of algae",
          "NCERT names Ectocarpus, Dictyota, Laminaria, Sargassum and Fucus as common brown algae (Phaeophyceae). "
          "Porphyra, Polysiphonia and Gelidium are red algae (Rhodophyceae), and Chara is a green alga "
          "(Chlorophyceae).",
          ["Brown: Ectocarpus, Dictyota, Laminaria, Sargassum, Fucus = 5",
           "Red: Porphyra, Polysiphonia, Gelidium; green: Chara"],
          why="4 leaves out one brown alga (often Dictyota); 6 counts a red alga such as Porphyra or Gelidium as brown; "
              "3 counts only the kelps and Fucus.",
          ncert=ref("PK", "Algae (Phaeophyceae, Rhodophyceae, Chlorophyceae)"), secs=50)
