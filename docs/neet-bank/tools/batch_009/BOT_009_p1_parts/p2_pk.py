
# =============================================================== 2. Plant Kingdom (6/7/6)
direct(T_PK, "Algae", "Basic",
       "The plant body of a brown alga is usually attached to the substratum by a holdfast and has a stalk, the stipe. "
       "Its leaf-like photosynthetic organ is called the:",
       "frond",
       ["thallus", "rhizoid", "sporophyll"], "B",
       "Plant body of brown algae",
       "In Phaeophyceae the plant body is usually attached to the substratum by a holdfast, and has a stalk, the stipe, "
       "and a leaf-like photosynthetic organ, the frond.",
       ["Holdfast = attachment", "Stipe = stalk", "Frond = leaf-like photosynthetic organ"],
       why="Thallus is the general term for an undifferentiated plant body. Rhizoids attach bryophytes, not brown "
           "algae. A sporophyll is a leaf-like appendage bearing sporangia in pteridophytes and gymnosperms.",
       ncert=ref("PK", "Algae (Phaeophyceae)"), secs=20)

direct(T_PK, "Algae", "Basic",
       "NCERT divides algae into three main classes. Which of the following is NOT one of them?",
       "Chrysophyceae",
       ["Chlorophyceae", "Phaeophyceae", "Rhodophyceae"], "B",
       "Classes of algae",
       "Algae are divided into three main classes: Chlorophyceae (green algae), Phaeophyceae (brown algae) and "
       "Rhodophyceae (red algae). Chrysophytes (diatoms and golden algae) are placed by NCERT in kingdom Protista, "
       "not among these classes.",
       ["Three classes: Chlorophyceae, Phaeophyceae, Rhodophyceae"],
       why="The other three options are exactly the three main classes of algae named in NCERT.",
       ncert=ref("PK", "Algae"), secs=20)

direct(T_PK, "Pteridophytes", "Basic",
       "In a pteridophyte, the zygote formed after fusion of the male gamete with the egg in the archegonium develops "
       "into:",
       "a multicellular, well-differentiated sporophyte, which is the dominant phase",
       ["a prothallus, which is the dominant phase", "a protonema, from which leafy shoots arise",
        "a female gametophyte retained within the megasporangium"], "B",
       "Fate of the zygote in pteridophytes",
       "The gametophytes bear antheridia and archegonia. Water carries the antherozoids to the mouth of the "
       "archegonium, and fusion of a male gamete with the egg forms the zygote. The zygote then produces a "
       "multicellular, well-differentiated sporophyte, which is the dominant phase of pteridophytes.",
       ["Male gamete + egg -> zygote", "Zygote -> sporophyte (dominant phase)"],
       why="The prothallus is the gametophyte, formed from a spore and not the dominant phase. The protonema belongs to "
           "mosses. A female gametophyte develops from a megaspore, not from the zygote.",
       ncert=ref("PK", "Pteridophytes"), secs=25)

statement_pair(T_PK, "Gymnosperms", "Basic",
               "The leaves of gymnosperms may be simple or compound.",
               "In gymnosperms, the male and female gametophytes remain within the sporangia retained on the "
               "sporophytes.",
               True, True, "A",
               "Leaves and gametophytes of gymnosperms",
               "In gymnosperms the leaves may be simple or compound; in Cycas the pinnate leaves persist for a few "
               "years. Unlike bryophytes and pteridophytes, the male and female gametophytes of gymnosperms do not "
               "have an independent free-living existence; they remain within the sporangia retained on the "
               "sporophytes.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PK", "Gymnosperms"), secs=30)

match_list(T_PK, "Pteridophytes", "Basic", "term", "meaning in pteridophytes",
           ["Sporophyll", "Strobilus", "Prothallus", "Microphyll"],
           ["Small leaf, as in Selaginella", "Leaf-like appendage that subtends sporangia",
            "Compact structure formed by sporophylls", "Small, free-living, mostly photosynthetic thalloid gametophyte"],
           "II III IV I", ["III II IV I", "II III I IV", "II IV III I"], "B",
           "Terms used for pteridophytes",
           "The pteridophyte sporophyte bears sporangia subtended by leaf-like appendages called sporophylls. In some "
           "(Selaginella, Equisetum) the sporophylls form distinct compact structures called strobili or cones. The "
           "spores germinate into small, multicellular, free-living, mostly photosynthetic thalloid gametophytes "
           "called prothalli. Small leaves, as in Selaginella, are microphylls; large ones, as in ferns, are "
           "macrophylls.",
           ["Sporophyll -> II", "Strobilus -> III", "Prothallus -> IV", "Microphyll -> I"],
           why="The wrong codes exchange sporophyll and strobilus, prothallus and microphyll, or strobilus and "
               "prothallus.",
           ncert=ref("PK", "Pteridophytes"), secs=35)

direct(T_PK, "Algae", "Basic",
       "Which of the following is a green alga (Chlorophyceae)?",
       "Chara",
       ["Dictyota", "Polysiphonia", "Gracilaria"], "D",
       "Examples of green algae",
       "NCERT's examples of Chlorophyceae are Chlamydomonas, Volvox, Ulothrix, Spirogyra and Chara. Dictyota is a brown "
       "alga, while Polysiphonia and Gracilaria are red algae.",
       ["Green algae: Chlamydomonas, Volvox, Ulothrix, Spirogyra, Chara"],
       why="Dictyota belongs to Phaeophyceae; Polysiphonia and Gracilaria belong to Rhodophyceae.",
       ncert=ref("PK", "Algae (Chlorophyceae)"), secs=20)

multi_statement(T_PK, "Algae", "Intermediate",
                "Which of the following statements are true of BOTH brown algae (Phaeophyceae) and red algae "
                "(Rhodophyceae)?",
                [("The majority of members are marine.", True),
                 ("Some members produce hydrocolloids (water-holding substances) that are used commercially.", True),
                 ("Their motile cells bear two unequal, lateral flagella.", False),
                 ("Chlorophyll a is present.", True),
                 ("Food is stored as floridean starch.", False)],
                [("a", "b", "c", "d"), ("b", "d", "e"), ("a", "d")], "A",
                "Comparing brown and red algae",
                "Brown algae are found primarily in marine habitats, and the majority of red algae are marine. Certain "
                "marine brown and red algae produce large amounts of hydrocolloids: algin (brown algae) and carrageen "
                "(red algae), used commercially. Chlorophyll a is present in both. Two unequal lateral flagella occur "
                "only in brown algae; red algae have no flagella. Floridean starch is the food of red algae only; "
                "brown algae store mannitol or laminarin.",
                ["(a) true for both", "(b) true for both (algin; carrageen)", "(c) brown only",
                 "(d) true for both", "(e) red only"],
                ncert=ref("PK", "Algae (Phaeophyceae, Rhodophyceae; table of divisions of algae)"), secs=60)

statement_pair(T_PK, "Algae", "Intermediate",
               "In Chlorophyceae, sexual reproduction may be isogamous, anisogamous or oogamous.",
               "In Rhodophyceae, sexual reproduction may be isogamous, anisogamous or oogamous.",
               True, False, "C",
               "Sexual reproduction in green and red algae",
               "In green algae, sexual reproduction shows considerable variation in the type and formation of sex "
               "cells, and it may be isogamous, anisogamous or oogamous. In red algae, sexual reproduction (by "
               "non-motile gametes) is oogamous and is accompanied by complex post-fertilisation developments.",
               ["Statement I: true", "Statement II: false; red algae are oogamous"],
               ncert=ref("PK", "Algae (Chlorophyceae, Rhodophyceae)"), secs=35)

direct(T_PK, "Bryophytes", "Intermediate",
       "According to NCERT, which of the following is a feature of mosses that is NOT described for liverworts?",
       "A protonema stage of the gametophyte that develops directly from a spore",
       ["Asexual reproduction by gemmae formed in gemma cups", "A sporophyte differentiated into foot, seta and capsule",
        "Multicellular sex organs"], "C",
       "Mosses compared with liverworts",
       "The moss gametophyte has two stages: the protonema, a creeping, green, branched, frequently filamentous stage "
       "that develops directly from a spore, and the leafy stage, which develops from the secondary protonema as a "
       "lateral bud. Liverworts have a thalloid or leafy gametophyte with no protonema stage described. Gemmae in "
       "gemma cups are a liverwort feature; a sporophyte with foot, seta and capsule and multicellular sex organs "
       "are found in both.",
       ["Protonema: mosses", "Gemma cups: liverworts", "Foot-seta-capsule and multicellular sex organs: both"],
       why="Gemmae in gemma cups are described for liverworts. The liverwort sporophyte is also differentiated into "
           "foot, seta and capsule. All bryophytes have multicellular sex organs.",
       ncert=ref("PK", "Bryophytes (liverworts, mosses)"), secs=40)

match_list(T_PK, "Algae", "Intermediate", "plant", "use described in NCERT",
           ["Sphagnum", "Gelidium", "Chlorella", "Porphyra"],
           ["Marine alga used as food", "Source of agar", "Peat, used as fuel",
            "Protein-rich food supplement, used even by space travellers"],
           "III II IV I", ["II III IV I", "III II I IV", "III IV II I"], "D",
           "Economic importance of algae and bryophytes",
           "Species of the moss Sphagnum provide peat, which has long been used as fuel. Agar, used to grow microbes and "
           "in ice-creams and jellies, is obtained from Gelidium and Gracilaria. Chlorella, a unicellular alga rich in "
           "proteins, is used as a food supplement even by space travellers. Porphyra is one of the marine algae "
           "used as food.",
           ["Sphagnum -> peat", "Gelidium -> agar", "Chlorella -> food supplement", "Porphyra -> food"],
           why="The wrong codes swap Sphagnum and Gelidium, Chlorella and Porphyra, or Gelidium and Chlorella.",
           ncert=ref("PK", "Algae; Bryophytes"), secs=40)

assertion_reason(T_PK, "Bryophytes", "Intermediate",
                 "In liverworts, the male and female sex organs are produced either on the same thallus or on "
                 "different thalli.",
                 "The sporophyte of a liverwort is free-living and independent of the gametophyte.",
                 True, False, False, "C",
                 "Sex organs and sporophyte of liverworts",
                 "During sexual reproduction in liverworts, male and female sex organs are produced either on the same "
                 "or on different thalli. The sporophyte, differentiated into foot, seta and capsule, is not "
                 "free-living: in bryophytes it remains attached to the photosynthetic gametophyte and derives "
                 "nourishment from it.",
                 ["A: true", "R: false; the bryophyte sporophyte depends on the gametophyte"],
                 ncert=ref("PK", "Bryophytes (liverworts)"), secs=35)

_mmc = 6
numerical(T_PK, "Gymnosperms", "Intermediate",
          "In a gymnosperm, each ovule has one megaspore mother cell. If the megaspore mother cells of 6 ovules "
          "complete their division, how many megaspores are formed in all, and how many of these develop into female "
          "gametophytes?",
          "24 megaspores; 6 female gametophytes",
          ["24 megaspores; 24 female gametophytes", "12 megaspores; 6 female gametophytes",
           "6 megaspores; 6 female gametophytes"], "A",
          _mmc * 4 == 24 and _mmc * 1 == 6,
          "Megasporogenesis in gymnosperms",
          "The megaspore mother cell is differentiated from one of the cells of the nucellus and divides meiotically to "
          "form four megaspores. One of the megaspores enclosed within the megasporangium develops into a "
          "multicellular female gametophyte bearing two or more archegonia.",
          ["Megaspores = 6 x 4 = 24 (meiosis gives four)", "Female gametophytes = 6 x 1 = 6 (one megaspore each)"],
          why="24 gametophytes assumes every megaspore develops; 12 treats the division as giving two cells; 6 "
              "megaspores ignores that meiosis gives four.",
          ncert=ref("PK", "Gymnosperms"), secs=50)

direct(T_PK, "Pteridophytes", "Intermediate",
       "Which of the following pairs of pteridophytes belong to the same class?",
       "Selaginella and Lycopodium",
       ["Psilotum and Equisetum", "Equisetum and Adiantum", "Selaginella and Dryopteris"], "B",
       "Classes of pteridophytes",
       "NCERT divides pteridophytes into four classes: Psilopsida (Psilotum), Lycopsida (Selaginella, Lycopodium), "
       "Sphenopsida (Equisetum) and Pteropsida (Dryopteris, Pteris, Adiantum). Selaginella and Lycopodium are both "
       "Lycopsida.",
       ["Lycopsida: Selaginella, Lycopodium"],
       why="Psilotum (Psilopsida) and Equisetum (Sphenopsida) differ; Equisetum and Adiantum (Pteropsida) differ; "
           "Selaginella (Lycopsida) and Dryopteris (Pteropsida) differ.",
       ncert=ref("PK", "Pteridophytes"), secs=35)

statement_pair(T_PK, "Algae", "Advanced",
               "Members of both Chlorophyceae and Phaeophyceae have motile cells, but their flagella differ: 2-8, equal "
               "and apical in the former, and 2, unequal and lateral in the latter.",
               "Like the red algae, members of Phaeophyceae store their food as floridean starch.",
               True, False, "C",
               "Flagella and stored food in algae",
               "NCERT's table of the divisions of algae gives Chlorophyceae 2-8 equal, apical flagella and "
               "Phaeophyceae 2 unequal, lateral flagella; Rhodophyceae have none. Stored food is starch in "
               "Chlorophyceae, mannitol or laminarin in Phaeophyceae and floridean starch in Rhodophyceae.",
               ["Statement I: true", "Statement II: false; brown algae store mannitol or laminarin"],
               ncert=ref("PK", "Algae (table of divisions of algae and their main characteristics)"), secs=40)

match_list(T_PK, "Gymnosperms", "Advanced", "feature", "plant group",
           ["Naked seeds", "First terrestrial plants with xylem and phloem",
            "Sporophyte attached to, and nourished by, the gametophyte",
            "Flagellated zoospores as the most common asexual spores"],
           ["Algae", "Bryophytes", "Pteridophytes", "Gymnosperms"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "C",
           "Distinguishing features of plant groups",
           "Gymnosperms have ovules not enclosed by an ovary wall, so the seeds are naked. Pteridophytes are, "
           "evolutionarily, the first terrestrial plants to possess vascular tissues, xylem and phloem. In bryophytes "
           "the sporophyte is not free-living; it is attached to the photosynthetic gametophyte and derives "
           "nourishment from it. In algae the most common asexual spores are the flagellated zoospores.",
           ["Naked seeds -> gymnosperms", "First vascular land plants -> pteridophytes",
            "Dependent sporophyte -> bryophytes", "Zoospores -> algae"],
           why="The wrong codes swap the gymnosperms and pteridophytes, the bryophytes and algae, or the pteridophytes "
               "and bryophytes.",
           ncert=ref("PK", "Algae; Bryophytes; Pteridophytes; Gymnosperms"), secs=50)

assertion_reason(T_PK, "Gymnosperms", "Advanced",
                 "Since gymnosperms are heterosporous, their megaspores are shed and germinate in the soil into "
                 "free-living female gametophytes.",
                 "In gymnosperms, the megaspore mother cell divides meiotically to form four megaspores.",
                 False, True, False, "D",
                 "Female gametophyte of gymnosperms",
                 "Gymnosperms are heterosporous. The megaspore mother cell, differentiated from a nucellus cell, divides "
                 "meiotically to form four megaspores. One megaspore, enclosed within the megasporangium, develops into "
                 "the multicellular female gametophyte, which is retained within the megasporangium; it is not shed "
                 "and is not free-living.",
                 ["A: false; the female gametophyte develops within the megasporangium", "R: true"],
                 ncert=ref("PK", "Gymnosperms"), secs=45)

direct(T_PK, "Bryophytes", "Advanced",
       "Which sequence correctly shows the development of a moss from a spore up to the formation of sex organs?",
       "Spore -> protonema -> lateral bud on the secondary protonema -> leafy stage -> antheridia and archegonia at the "
       "apex of the leafy shoots",
       ["Spore -> leafy stage -> protonema -> antheridia and archegonia on the protonema",
        "Spore -> prothallus -> leafy stage -> antheridia and archegonia on the prothallus",
        "Spore -> protonema -> capsule -> leafy stage -> antheridia and archegonia on the capsule"], "D",
       "Gametophyte of mosses",
       "The protonema develops directly from a spore; it is a creeping, green, branched, frequently filamentous stage. "
       "The leafy stage develops from the secondary protonema as a lateral bud and bears spirally arranged leaves. "
       "The sex organs, antheridia and archegonia, are produced at the apex of the leafy shoots.",
       ["Spore -> protonema", "Secondary protonema -> lateral bud -> leafy stage", "Sex organs at the shoot apex"],
       why="The leafy stage comes after, not before, the protonema. A prothallus is a pteridophyte gametophyte. The "
           "capsule is part of the sporophyte, formed after fertilisation.",
       ncert=ref("PK", "Bryophytes (mosses)"), secs=50)

direct(T_PK, "Algae", "Advanced",
       "Which of the following alga - stored food pairs is INCORRECT?",
       "Fucus - floridean starch",
       ["Porphyra - floridean starch", "Laminaria - mannitol or laminarin", "Chara - starch"], "A",
       "Stored food of the classes of algae",
       "Stored food: Chlorophyceae, starch; Phaeophyceae, mannitol or laminarin; Rhodophyceae, floridean starch. "
       "Porphyra is a red alga, Laminaria and Fucus are brown algae, and Chara is a green alga. Fucus, being brown, "
       "stores mannitol or laminarin, not floridean starch.",
       ["Identify each alga's class", "Apply the class's stored food", "Fucus (brown) - floridean starch is wrong"],
       why="Porphyra (red) does store floridean starch; Laminaria (brown) stores mannitol or laminarin; Chara (green) "
           "stores starch.",
       ncert=ref("PK", "Algae (table of divisions of algae and their main characteristics)"), secs=45)

assertion_reason(T_PK, "Pteridophytes", "Advanced",
                 "In Equisetum, the sporophylls are compactly arranged to form strobili.",
                 "Equisetum belongs to the class Lycopsida.",
                 True, False, False, "C",
                 "Strobili and classes of pteridophytes",
                 "In some pteridophytes the sporophylls form distinct compact structures called strobili or cones, as "
                 "in Selaginella and Equisetum. Equisetum belongs to Sphenopsida; Lycopsida includes Selaginella and "
                 "Lycopodium.",
                 ["A: true", "R: false; Equisetum is in Sphenopsida"],
                 ncert=ref("PK", "Pteridophytes"), secs=35)
