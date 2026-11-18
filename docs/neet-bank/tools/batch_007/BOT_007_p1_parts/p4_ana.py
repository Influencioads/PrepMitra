
# =============================================================== 4. Anatomy of Flowering Plants (4/6/4)
direct(T_ANA, "Plant tissues", "Basic",
       "Growth in plants is largely restricted to specialised regions of active cell division. These regions are "
       "called:",
       "meristems",
       ["permanent tissues", "complex tissues", "stele"], "A",
       "Meristems",
       "Growth in plants is largely restricted to specialised regions of active cell division called meristems "
       "(Gk. meristos: divided). Plants have apical, intercalary and lateral meristems.",
       ["Regions of active cell division → meristems"],
       why="Permanent tissues are cells that have lost the ability to divide. Complex tissues (xylem, phloem) are "
           "made of more than one cell type. The stele is all the tissue inside the endodermis.",
       ncert=ref("ANA", "The Tissues (Meristematic Tissues)"), secs=20)

direct(T_ANA, "Tissue systems", "Basic",
       "On the basis of their structure and location, the tissues of a plant are grouped into three tissue "
       "systems. These are the:",
       "epidermal, ground (fundamental) and vascular (conducting) tissue systems",
       ["meristematic, permanent and secretory tissue systems",
        "simple, complex and secretory tissue systems",
        "apical, intercalary and lateral tissue systems"], "C",
       "The three tissue systems",
       "The structure of tissues varies with their location in the plant body. On this basis there are three "
       "tissue systems: the epidermal tissue system, the ground or fundamental tissue system and the vascular or "
       "conducting tissue system.",
       ["Epidermal + ground + vascular tissue systems"],
       why="Meristematic and permanent, and simple and complex, are kinds of tissues, not tissue systems. Apical, "
           "intercalary and lateral are kinds of meristems.",
       ncert=ref("ANA", "The Tissue System"), secs=20)

direct(T_ANA, "Plant tissues", "Basic",
       "Which of the following pairs consists only of simple permanent tissues?",
       "Collenchyma and sclerenchyma",
       ["Xylem and phloem", "Parenchyma and phloem", "Xylem and sclerenchyma"], "B",
       "Simple and complex tissues",
       "A simple tissue is made of only one type of cell; the simple permanent tissues are parenchyma, collenchyma "
       "and sclerenchyma. Complex tissues are made of more than one type of cell working together as a unit; xylem "
       "and phloem are complex tissues.",
       ["Simple: parenchyma, collenchyma, sclerenchyma", "Complex: xylem, phloem"],
       why="Each wrong pair contains xylem or phloem, which are complex tissues.",
       ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=20)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "The epidermal tissue system forms the outermost covering of the whole plant body.",
               "The vascular system consists of complex tissues, the phloem and the xylem.",
               True, True, "A",
               "Epidermal and vascular tissue systems",
               "The epidermal tissue system forms the outer-most covering of the whole plant body and comprises "
               "epidermal cells, stomata and the epidermal appendages (trichomes and hairs). The vascular system "
               "consists of the complex tissues phloem and xylem, which together form the vascular bundles.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissue System"), secs=25)

numerical(T_ANA, "Plant tissues", "Intermediate",
          "How many of the following are dead at maturity, according to NCERT?\n"
          "Tracheids, vessel members, sclereids, phloem fibres, xylem parenchyma, companion cells, sieve tube "
          "elements, collenchyma cells",
          "4",
          ["5", "3", "6"], "B",
          (sum({"tracheids": 1, "vessel members": 1, "sclereids": 1, "phloem fibres": 1, "xylem parenchyma": 0,
                "companion cells": 0, "sieve tube elements": 0, "collenchyma": 0}.values()) == 4),
          "Living and dead cells of plant tissues",
          "Dead at maturity: tracheids (dead, without protoplasm), vessel members (devoid of protoplasm), sclereids "
          "(highly thickened dead cells) and phloem fibres (lose their protoplasm and become dead at maturity). "
          "Living: xylem parenchyma, companion cells, sieve tube elements (living, with peripheral cytoplasm, though "
          "without a nucleus) and collenchyma. So 4 are dead.",
          ["Dead: tracheids, vessels, sclereids, phloem fibres = 4",
           "Living: xylem parenchyma, companion cells, sieve tube elements, collenchyma"],
          why="5 wrongly counts sieve tube elements as dead because they lack a nucleus. 3 forgets that phloem fibres "
              "die at maturity. 6 counts both sieve tube elements and companion cells as dead.",
          ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=60)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Apical meristems and intercalary meristems are called primary meristems.",
                 "They appear early in the life of a plant and contribute to the formation of the primary plant "
                 "body.",
                 True, True, True, "A",
                 "Primary meristems",
                 "NCERT explains that apical and intercalary meristems are primary meristems because they appear "
                 "early in the life of a plant and contribute to the formation of the primary plant body. Lateral "
                 "meristems, which appear later, are secondary meristems.",
                 ["A: true", "R: true, and it is the reason for the name"],
                 ncert=ref("ANA", "The Tissues (Meristematic Tissues)"), secs=35)

match_list(T_ANA, "Plant tissues", "Intermediate", "cell or tissue", "nature of the cell wall",
           ["Parenchyma", "Collenchyma", "Sclerenchyma", "Endodermis of a dicot root"],
           ["Thin walls made of cellulose",
            "Thickened at the corners by deposition of cellulose, hemicellulose and pectin",
            "Thick and lignified walls with a few or numerous pits",
            "Tangential and radial walls with a deposit of suberin as Casparian strips"],
           "I II III IV", ["II I III IV", "I II IV III", "I III II IV"], "D",
           "Cell walls of plant tissues",
           "Parenchyma cells have thin cell walls made of cellulose. Collenchyma cells are thickened at the corners "
           "due to deposition of cellulose, hemicellulose and pectin. Sclerenchyma has long, narrow cells with thick "
           "and lignified walls with a few or numerous pits. The endodermal cells of the root have a deposition of "
           "water-impermeable, waxy suberin on their tangential and radial walls in the form of Casparian strips.",
           ["Parenchyma → thin cellulose", "Collenchyma → corner thickening", "Sclerenchyma → lignified",
            "Root endodermis → suberin (Casparian strips)"],
           why="The wrong codes swap parenchyma and collenchyma, sclerenchyma and endodermis, or collenchyma and "
               "sclerenchyma.",
           ncert=ref("ANA", "The Tissues; Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=45)

multi_statement(T_ANA, "Plant tissues", "Intermediate",
                "Which of the following statements comparing collenchyma and sclerenchyma are correct?",
                [("Both provide mechanical support.", True),
                 ("Collenchyma cells may contain chloroplasts, in which case they assimilate food.", True),
                 ("Both have lignified cell walls.", False),
                 ("The walls of sclerenchyma cells have a few or numerous pits.", True),
                 ("Collenchyma cells have large intercellular spaces between them.", False)],
                ["abc", "abde", "bd"], "A",
                "Collenchyma and sclerenchyma compared",
                "Collenchyma provides mechanical support to growing parts such as the young stem and petiole; its "
                "cells often contain chloroplasts and then assimilate food; its walls are thickened at the corners "
                "with cellulose, hemicellulose and pectin, and intercellular spaces are absent. Sclerenchyma "
                "provides mechanical support to organs; its cells have thick, lignified walls with a few or "
                "numerous pits.",
                ["(a), (b), (d): true", "(c): false, collenchyma is not lignified",
                 "(e): false, collenchyma has no intercellular spaces"],
                why="Each wrong combination includes (c) or (e), or leaves out a true statement.",
                ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=50)

statement_pair(T_ANA, "Dicot and monocot anatomy", "Intermediate",
               "The hypodermis is sclerenchymatous in a monocot stem but collenchymatous in a dicot stem.",
               "The vascular bundles are conjoint and closed in both dicot and monocot stems.",
               True, False, "C",
               "Dicot and monocot stems compared",
               "In a dicot stem the hypodermis consists of a few layers of collenchymatous cells; the monocot stem "
               "has a sclerenchymatous hypodermis. The vascular bundles of a dicot stem are conjoint and open (with "
               "cambium); those of a monocot stem are conjoint and closed.",
               ["Statement I: true", "Statement II: false, dicot stem bundles are open"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "In the transverse section of a dicot root, which of the following is NOT a part of the stele?",
       "Endodermis",
       ["Pericycle", "Conjunctive tissue", "Pith"], "C",
       "Extent of the stele",
       "All tissues on the inner side of the endodermis, such as the pericycle, vascular bundles and pith, "
       "constitute the stele. In the dicot root this includes the conjunctive tissue (parenchyma between xylem and "
       "phloem). The endodermis is the innermost layer of the cortex and lies outside the stele.",
       ["Stele = everything inside the endodermis", "Endodermis = innermost layer of cortex"],
       why="Pericycle, conjunctive tissue and pith all lie inside the endodermis and so belong to the stele.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Dicotyledonous Root)"), secs=35)

assertion_reason(T_ANA, "Tissue systems", "Advanced",
                 "In grasses, the guard cells of the stomata are dumb-bell shaped.",
                 "In grass leaves, some adaxial epidermal cells along the veins are modified into large, empty, "
                 "colourless bulliform cells.",
                 True, True, False, "B",
                 "Two features of grass leaves",
                 "Both are true features of grass leaves. The dumb-bell shape describes the guard cells that enclose "
                 "the stomatal pore. Bulliform cells are a separate set of epidermal cells along the veins that help "
                 "in rolling the leaf when they lose water. The existence of bulliform cells has nothing to do with "
                 "the shape of the guard cells, so R does not explain A.",
                 ["A: true", "R: true", "R concerns other epidermal cells, not the shape of guard cells"],
                 ncert=ref("ANA", "The Tissue System (Epidermal Tissue System); Monocotyledonous Leaf"), secs=45)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "In the transverse section of a plant organ, the xylem and phloem lie on different radii, the "
                "endodermis has Casparian strips, and the pith is large and well developed. Which of the following "
                "conclusions are correct?",
                [("The section is of a monocot root.", True),
                 ("The protoxylem lies towards the periphery of the organ.", True),
                 ("Cambium is present between the xylem and the phloem, so the bundles are open.", False),
                 ("There are usually more than six xylem bundles.", True),
                 ("The xylem and phloem lie together on the same radius.", False)],
                ["abc", "bde", "ade"], "C",
                "Interpreting a transverse section",
                "Xylem and phloem on different radii means radial vascular bundles, found in roots; a Casparian "
                "endodermis confirms a root. A large, well-developed pith is a feature of the monocot root, which "
                "usually has more than six xylem bundles (polyarch). In roots the primary xylem is exarch, with "
                "protoxylem towards the periphery. Radial bundles have no cambium between xylem and phloem in the "
                "primary structure, and monocot roots do not undergo secondary growth.",
                ["Radial bundles + Casparian strips → root", "Large pith → monocot root (polyarch, exarch)"],
                why="Each wrong combination includes (c) or (e), which contradict the radial arrangement, or leaves "
                    "out a correct conclusion.",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (Monocotyledonous Root)"),
                secs=60)

direct(T_ANA, "Tissue systems", "Advanced",
       "Which of the following pairs consists only of tissues that belong to the ground tissue system of a dicot "
       "stem?",
       "Hypodermis and medullary rays",
       ["Pericycle and protoxylem", "Epidermis and pith", "Companion cells and medullary rays"], "B",
       "Extent of the ground tissue system",
       "All tissues except the epidermis and the vascular bundles constitute the ground tissue. In a dicot stem "
       "this includes the hypodermis, cortical layers, endodermis, pericycle, medullary rays and pith. Protoxylem "
       "and companion cells are parts of the vascular bundles, and the epidermis belongs to the epidermal tissue "
       "system.",
       ["Ground tissue = all except epidermis and vascular bundles",
        "Hypodermis and medullary rays → ground tissue"],
       why="Protoxylem and companion cells belong to the vascular tissue system, and the epidermis to the epidermal "
           "tissue system.",
       ncert=ref("ANA", "The Tissue System (Ground Tissue System); Dicotyledonous Stem"), secs=45)

multi_statement(T_ANA, "Plant tissues", "Advanced",
                "Which of the following plant cells have lignified cell walls?",
                [("Tracheids", True), ("Vessel members", True), ("Sclerenchyma cells", True),
                 ("Collenchyma cells", False), ("Companion cells", False)],
                ["abcd", "bce", "acd"], "D",
                "Lignified walls",
                "Tracheids are elongated, tube-like cells with thick and lignified walls and tapering ends. A vessel "
                "member has lignified walls and a large central cavity. Sclerenchyma consists of long, narrow cells "
                "with thick and lignified cell walls. Collenchyma walls are thickened at the corners with cellulose, "
                "hemicellulose and pectin, not lignin, and companion cells are specialised parenchymatous cells.",
                ["(a), (b), (c): lignified", "(d) collenchyma: cellulose, hemicellulose, pectin",
                 "(e) companion cells: parenchymatous"],
                why="Each wrong combination includes collenchyma or companion cells, or leaves out a lignified "
                    "element.",
                ncert=ref("ANA", "The Tissues (Permanent Tissues)"), secs=50)
