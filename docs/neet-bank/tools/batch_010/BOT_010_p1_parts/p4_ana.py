
# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
direct(T_ANA, "Plant tissues", "Basic",
       "According to NCERT, the secondary or lateral meristem occurs in the mature regions of roots and shoots of "
       "many plants, particularly those that:",
       "produce a woody axis",
       ["are grasses regenerating after grazing", "are aquatic and lack vascular tissue",
        "have no apical meristem"], "D",
       "Where lateral meristems occur",
       "NCERT: the meristem that occurs in the mature regions of roots and shoots of many plants, particularly those "
       "that produce a woody axis, and appears later than the primary meristem is called the secondary or lateral "
       "meristem. It is cylindrical; fascicular vascular cambium, interfascicular cambium and cork cambium are "
       "examples.",
       ["Lateral meristem: mature regions of roots and shoots", "Particularly in plants producing a woody axis"],
       why="Regeneration after grazing in grasses is due to intercalary meristems. Flowering plants are not "
           "without vascular tissue, and all have apical meristems at root and shoot tips.",
       ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=20)

numerical(T_ANA, "Plant tissues", "Basic",
          "In angiosperms, how many different kinds of elements make up the xylem and the phloem taken together, as "
          "listed in NCERT?",
          "8", ["4", "6", "7"], "A",
          len(["tracheids", "vessels", "xylem fibres", "xylem parenchyma"]
              + ["sieve tube elements", "companion cells", "phloem parenchyma", "phloem fibres"]) == 8,
          "Elements of xylem and phloem",
          "Xylem is composed of four elements: tracheids, vessels, xylem fibres and xylem parenchyma. Phloem in "
          "angiosperms is composed of sieve tube elements, companion cells, phloem parenchyma and phloem fibres.",
          ["Xylem: 4 elements", "Angiosperm phloem: 4 elements", "Total = 4 + 4 = 8"],
          why="4 counts only one of the two tissues. 6 leaves out the fibres of both tissues. 7 leaves out one "
              "element, such as the phloem fibres.",
          ncert=ref("ANA", "The Tissues (xylem; phloem)"), secs=30)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "The trichomes of the shoot system may be branched or unbranched, and soft or stiff.",
               "The waxy cuticle that covers the epidermis is absent in roots.",
               True, True, "A",
               "Trichomes and cuticle",
               "On the stem, the epidermal hairs are called trichomes. They are usually multicellular, may be branched "
               "or unbranched, soft or stiff, and may even be secretory; they help prevent water loss due to "
               "transpiration. The outside of the epidermis is often covered with a waxy, thick cuticle that "
               "prevents loss of water; the cuticle is absent in roots.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System (epidermal tissue system)"), secs=25)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "Which of the following is found in a monocot stem but NOT in a dicot stem?",
       "Scattered vascular bundles, each surrounded by a sclerenchymatous bundle sheath",
       ["Conjoint vascular bundles", "An epidermis forming the outermost layer",
        "A hypodermis of a few layers of collenchymatous cells"], "B",
       "Monocot stem compared with dicot stem",
       "The monocot stem has a sclerenchymatous hypodermis, a large number of scattered vascular bundles, each "
       "surrounded by a sclerenchymatous bundle sheath, and a large, conspicuous parenchymatous ground tissue. The "
       "dicot stem has a collenchymatous hypodermis and conjoint, open bundles arranged in a ring.",
       ["Monocot stem: scattered bundles with sclerenchymatous sheaths", "Dicot stem: bundles in a ring"],
       why="Conjoint bundles and an epidermis are found in both stems. A collenchymatous hypodermis is a feature "
           "of the dicot stem, not the monocot stem.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (monocot stem)"), secs=30)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Xylem parenchyma is a living component of the xylem.",
                 "All components of the xylem except xylem parenchyma are living cells.",
                 True, False, False, "C",
                 "Living and dead elements of xylem",
                 "Xylem parenchyma cells are living and thin-walled, with cellulose walls, and store starch or fat and "
                 "substances like tannins. The other xylem elements are not living: tracheids are dead and without "
                 "protoplasm, vessel members are devoid of protoplasm, and xylem fibres have highly thickened walls "
                 "with an obliterated lumen.",
                 ["A: true", "R: false - tracheids, vessel members and xylem fibres are not living"],
                 ncert=ref("ANA", "The Tissues (xylem)"), secs=35)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "Which of the following features are common to the vascular bundles of BOTH the dicot stem and the "
                "monocot stem?",
                [("The bundles are conjoint.", True),
                 ("The primary xylem is endarch.", True),
                 ("The bundles are open, with cambium between the xylem and the phloem.", False),
                 ("The bundles are arranged in a ring.", False),
                 ("Water-containing cavities are present within the bundles.", False)],
                [("a", "b", "c"), ("a", "d"), ("b", "e")], "C",
                "Vascular bundles of dicot and monocot stems",
                "In both stems the xylem and phloem lie together on the same radius (conjoint), and, as in all stems, "
                "the protoxylem lies towards the centre and the metaxylem towards the periphery (endarch). The dicot "
                "stem's bundles are open and arranged in a ring; the monocot stem's bundles are closed, scattered, "
                "lack phloem parenchyma and have water-containing cavities.",
                ["(a) both conjoint: true", "(b) both stems endarch: true", "(c) open only in dicot stem: false",
                 "(d) ring only in dicot stem: false", "(e) cavities only in monocot stem: false"],
                why="The other combinations include (c), (d) or (e), each of which belongs to only one of the two "
                    "stems.",
                ncert=ref("ANA", "The Tissues (xylem); Anatomy of Dicotyledonous and Monocotyledonous Plants"),
                secs=60)

direct(T_ANA, "Plant tissues", "Intermediate",
       "Which of the following is true of BOTH sclereids and phloem fibres, but NOT of companion cells?",
       "They are dead at maturity and have thick cell walls.",
       ["They are living at maturity and have a nucleus.",
        "They help in maintaining the pressure gradient in the sieve tubes.",
        "They store resins, latex and mucilage."], "D",
       "Comparing sclerenchymatous cells with companion cells",
       "Sclereids are spherical, oval or cylindrical, highly thickened dead cells with very narrow lumen. Phloem "
       "fibres are sclerenchymatous, with quite thick walls, and lose their protoplasm at maturity to become dead. "
       "Companion cells are specialised, living parenchymatous cells whose nucleus controls the sieve tubes and "
       "which help maintain the pressure gradient in them.",
       ["Sclereids: dead, thick-walled", "Phloem fibres: dead at maturity, thick-walled",
        "Companion cells: living, with nucleus"],
       why="Being living with a nucleus, and maintaining the pressure gradient, describe companion cells only. "
           "Storing resins, latex and mucilage is a function of phloem parenchyma.",
       ncert=ref("ANA", "The Tissues (sclerenchyma; phloem)"), secs=40)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "In a monocot stem, the peripheral vascular bundles are generally smaller than the centrally located "
               "ones.",
               "In a monocot stem, the parenchymatous ground tissue is small and inconspicuous.",
               True, False, "C",
               "Monocot stem",
               "NCERT: the monocot stem has a sclerenchymatous hypodermis, a large number of scattered vascular "
               "bundles, each surrounded by a sclerenchymatous bundle sheath, and a large, conspicuous parenchymatous "
               "ground tissue. Its vascular bundles are conjoint and closed, and the peripheral ones are generally "
               "smaller than the centrally located ones.",
               ["Statement I: true", "Statement II: false; the ground tissue is large and conspicuous"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (monocot stem)"), secs=35)

match_list(T_ANA, "Plant tissues", "Intermediate", "term", "meaning",
           ["Protoxylem", "Metaxylem", "Protophloem", "Metaphloem"],
           ["Later-formed primary phloem with bigger sieve tubes", "First-formed primary xylem elements",
            "First-formed primary phloem with narrow sieve tubes", "Later-formed primary xylem elements"],
           "II IV III I", ["IV II III I", "II IV I III", "III IV II I"], "B",
           "First- and later-formed primary vascular tissues",
           "Primary xylem is of two types: the first-formed elements are protoxylem and the later-formed ones "
           "metaxylem. Likewise, the first-formed primary phloem consists of narrow sieve tubes and is called "
           "protophloem; the later-formed phloem has bigger sieve tubes and is called metaphloem.",
           ["Protoxylem -> II", "Metaxylem -> IV", "Protophloem -> III", "Metaphloem -> I"],
           why="The wrong codes swap the two kinds of xylem, the two kinds of phloem, or protoxylem with protophloem.",
           ncert=ref("ANA", "The Tissues (xylem; phloem)"), secs=35)

numerical(T_ANA, "Dicot and monocot anatomy", "Advanced",
          "In the transverse section of a dicot root, how many of the following lie OUTSIDE the stele?\n\n"
          "epiblema, root hairs, cortex, endodermis, pericycle, conjunctive tissue, xylem, pith",
          "4", ["3", "5", "6"], "B",
          len([p for p, inside in [("epiblema", False), ("root hairs", False), ("cortex", False),
                                   ("endodermis", False), ("pericycle", True), ("conjunctive tissue", True),
                                   ("xylem", True), ("pith", True)] if not inside]) == 4,
          "Extent of the stele in a dicot root",
          "All tissues on the inner side of the endodermis - the pericycle, the vascular bundles (with the "
          "conjunctive tissue between xylem and phloem) and the pith - constitute the stele. The epiblema with its "
          "root hairs, the cortex and the endodermis itself lie outside it.",
          ["Stele = everything inside the endodermis", "Outside: epiblema, root hairs, cortex, endodermis",
           "Count = 4"],
          why="3 wrongly places the endodermis inside the stele. 5 wrongly places the pericycle outside it. 6 also "
              "puts the conjunctive tissue outside, forgetting that it lies between the xylem and phloem.",
          ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicot root)"), secs=60)

assertion_reason(T_ANA, "Dicot and monocot anatomy", "Advanced",
                 "The vascular bundles of a monocot stem do not form secondary xylem and secondary phloem.",
                 "In the vascular bundles of monocots, no cambium is present between the xylem and the phloem.",
                 True, True, True, "A",
                 "Closed vascular bundles",
                 "In dicot stems, cambium between phloem and xylem gives the bundles the ability to form secondary "
                 "xylem and phloem, so they are open. NCERT: in monocotyledons the vascular bundles have no cambium "
                 "in them; hence they do not form secondary tissues and are referred to as closed. The absence of "
                 "cambium is the reason no secondary tissues form.",
                 ["A: true", "R: true", "No cambium -> no secondary xylem or phloem -> R explains A"],
                 ncert=ref("ANA", "The Tissue System (vascular tissue system)"), secs=45)

statement_pair(T_ANA, "Plant tissues", "Advanced",
               "Companion cells and phloem parenchyma cells are both living cells with a nucleus.",
               "Xylem fibres and phloem fibres are both living at maturity.",
               True, False, "C",
               "Living cells of the vascular tissues",
               "Companion cells are specialised parenchymatous cells whose nucleus controls the functions of the "
               "sieve tubes. Phloem parenchyma is made of elongated cells with dense cytoplasm and a nucleus. Xylem "
               "fibres have highly thickened walls and obliterated lumens, and phloem fibres lose their protoplasm "
               "and become dead at maturity.",
               ["Statement I: true", "Statement II: false; both kinds of fibre are dead at maturity"],
               ncert=ref("ANA", "The Tissues (xylem; phloem)"), secs=45)

direct(T_ANA, "Dicot and monocot anatomy", "Advanced",
       "A transverse section of a young plant organ shows a collenchymatous hypodermis, an endodermis whose cells "
       "are rich in starch grains, and semi-lunar patches of sclerenchyma above the phloem. The vascular bundles of "
       "this organ are expected to be:",
       "conjoint, open and endarch, arranged in a ring",
       ["radial, with exarch xylem and two to four xylem patches",
        "conjoint and closed, scattered, each with a sclerenchymatous bundle sheath",
        "conjoint and closed, all of nearly similar size except in the main veins"], "A",
       "Identifying a dicot stem from its section",
       "A collenchymatous hypodermis, a starch sheath (endodermis rich in starch grains) and a pericycle of "
       "semi-lunar sclerenchyma patches above the phloem identify a dicot stem. Its many vascular bundles are "
       "arranged in a ring; each is conjoint, open and has endarch protoxylem.",
       ["Features -> dicot stem", "Dicot stem bundles: conjoint, open, endarch, in a ring"],
       why="Radial bundles with exarch xylem and 2-4 patches describe a dicot root. Scattered, closed bundles with "
           "sclerenchymatous sheaths describe a monocot stem, and bundles of nearly similar size describe an "
           "isobilateral (monocot) leaf.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicot stem)"), secs=50)
