
# =============================================================== 4. Anatomy of Flowering Plants (5/6/5)
direct(T_ANA, "Plant tissues", "Basic",
       "In the phloem of angiosperms, companion cells are:",
       "specialised parenchymatous cells closely associated with the sieve tube elements",
       ["dead sclerenchymatous cells with very thick, lignified walls",
        "the sieve cells found in the phloem of gymnosperms",
        "thin-walled xylem cells that store tannins"], "B",
       "Companion cells",
       "Companion cells are specialised parenchymatous cells closely associated with the sieve tube elements. The "
       "sieve tube elements and companion cells are connected by pit fields in their common longitudinal walls, and "
       "the nucleus of the companion cell controls the functions of the sieve tube, which lacks a nucleus at "
       "maturity.",
       ["Companion cell = specialised parenchyma cell beside a sieve tube element"],
       why="Dead, thick-walled lignified cells describe sclerenchyma (such as phloem fibres). Gymnosperms have sieve "
           "cells and albuminous cells and lack companion cells. Tannin-storing thin-walled xylem cells are xylem "
           "parenchyma.",
       ncert=ref("ANA", "The Tissues (phloem)"), secs=25)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "In a dorsiventral (dicotyledonous) leaf, the vascular bundles are surrounded by a layer of:",
       "thick-walled bundle sheath cells",
       ["thin-walled bulliform cells", "Casparian strips of suberin", "semi-lunar patches of sclerenchyma"], "D",
       "Vascular bundles of a dorsiventral leaf",
       "The vascular system of a dorsiventral leaf includes the vascular bundles seen in the veins and the midrib. "
       "The vascular bundles are surrounded by a layer of thick-walled bundle sheath cells.",
       ["Dorsiventral leaf: bundles in veins and midrib", "Each surrounded by thick-walled bundle sheath cells"],
       why="Bulliform cells are large epidermal cells of grass leaves. Casparian strips belong to the endodermis of "
           "the root. Semi-lunar sclerenchyma patches are the pericycle of the dicot stem.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dorsiventral leaf)"), secs=25)

statement_pair(T_ANA, "Tissue systems", "Basic",
               "Root hairs and trichomes both belong to the epidermal tissue system.",
               "Root hairs are usually multicellular, whereas the trichomes of the shoot system are unicellular.",
               True, False, "C",
               "Epidermal appendages",
               "The epidermal tissue system is made of epidermal cells, stomata and the epidermal appendages, the "
               "trichomes and hairs. Root hairs are unicellular elongations of the epidermal cells that absorb water "
               "and minerals. The trichomes of the shoot system are usually multicellular; they may be branched or "
               "unbranched, soft or stiff, and even secretory.",
               ["Statement I: true", "Statement II: false; root hairs are unicellular, trichomes usually multicellular"],
               ncert=ref("ANA", "The Tissue System (epidermal tissue system)"), secs=30)

direct(T_ANA, "Plant tissues", "Basic",
       "A simple permanent tissue has oval, spherical or polygonal cells whose walls are thickened at the corners "
       "by deposition of cellulose, hemicellulose and pectin. The cells often contain chloroplasts, and intercellular "
       "spaces are absent. The tissue is:",
       "collenchyma",
       ["parenchyma", "sclerenchyma", "xylem parenchyma"], "A",
       "Identifying collenchyma",
       "Collenchyma cells are thickened at the corners due to a deposition of cellulose, hemicellulose and pectin. "
       "They may be oval, spherical or polygonal, often contain chloroplasts and assimilate food when chloroplasts are "
       "present. Intercellular spaces are absent. Collenchyma gives mechanical support to growing parts such as the "
       "young stem and the petiole.",
       ["Corner thickening of cellulose, hemicellulose, pectin = collenchyma"],
       why="Parenchyma has thin cellulose walls; sclerenchyma has thick lignified walls; xylem parenchyma is a "
           "thin-walled storage tissue of the xylem, a complex tissue.",
       ncert=ref("ANA", "The Tissues (simple tissues: collenchyma)"), secs=25)

match_list(T_ANA, "Plant tissues", "Basic", "meristem or bud", "role described in NCERT",
           ["Apical meristem", "Intercalary meristem", "Lateral meristem", "Axillary bud"],
           ["Can form a branch or a flower", "Produces the secondary tissues",
            "Produces the primary tissues at the tips of roots and shoots",
            "Regenerates parts removed by grazing herbivores in grasses"],
           "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "B",
           "Meristems and their roles",
           "Apical meristems occur at the tips of roots and shoots and produce primary tissues. Intercalary meristems "
           "occur in grasses and regenerate parts removed by grazing herbivores. Lateral meristems, in the mature "
           "regions of roots and shoots, are responsible for producing the secondary tissues. Axillary buds, formed "
           "from cells left behind by the shoot apical meristem, are capable of forming a branch or a flower.",
           ["Apical -> III", "Intercalary -> IV", "Lateral -> II", "Axillary bud -> I"],
           why="The wrong codes swap apical and intercalary, lateral and axillary bud, or intercalary and lateral.",
           ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=35)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Sclereids are commonly found in the seed coats of legumes.",
                 "Sclereids are living cells with thin cellulose walls.",
                 True, False, False, "C",
                 "Sclereids",
                 "Sclereids are spherical, oval or cylindrical, highly thickened dead cells with very narrow cavities "
                 "(lumen). They are commonly found in the fruit walls of nuts, the pulp of fruits like guava, pear and "
                 "sapota, the seed coats of legumes and the leaves of tea.",
                 ["A: true", "R: false; sclereids are dead and highly thickened"],
                 ncert=ref("ANA", "The Tissues (simple tissues: sclerenchyma)"), secs=30)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "The section of a leaf shows a mesophyll differentiated into palisade parenchyma on the adaxial side and "
                "spongy parenchyma below it, with more stomata on the lower epidermis than on the upper. Which of the "
                "following conclusions are correct?",
                [("It is a dorsiventral (dicotyledonous) leaf.", True),
                 ("Its vascular bundles vary in size, depending on the size of the veins.", True),
                 ("Large, empty, colourless bulliform cells are present along its veins in the adaxial epidermis.",
                  False),
                 ("Each stoma is bounded by two bean-shaped guard cells.", True),
                 ("Its spongy parenchyma cells are loosely arranged, with large spaces and air cavities.", True)],
                [("a", "b", "c"), ("a", "c", "d", "e"), ("b", "d", "e")], "A",
                "Interpreting a dorsiventral leaf section",
                "A mesophyll with adaxial palisade and abaxial spongy parenchyma, and more stomata on the abaxial "
                "epidermis, marks a dorsiventral (dicot) leaf. The size of its vascular bundles depends on the size of "
                "the veins, which vary in thickness in the reticulate venation of dicot leaves. Dicot guard cells are "
                "bean-shaped. The spongy parenchyma cells are oval or round, loosely arranged, with large spaces and "
                "air cavities. Bulliform cells are a feature of grass (isobilateral) leaves.",
                ["(a), (b), (d), (e) true", "(c) false; bulliform cells occur in grasses"],
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (leaves); The Tissue System"),
                secs=60)

match_list(T_ANA, "Plant tissues", "Intermediate", "tissue", "function described in NCERT",
           ["Xylem", "Phloem", "Collenchyma", "Sclerenchyma"],
           ["Mechanical support to organs", "Transport of food materials, usually from the leaves to other parts",
            "Mechanical support to growing parts such as the young stem and the petiole",
            "Conduction of water and minerals from the roots to the stem and leaves"],
           "IV II III I", ["II IV III I", "IV II I III", "III II IV I"], "C",
           "Functions of plant tissues",
           "Xylem conducts water and minerals from the roots to the stem and leaves (and gives mechanical strength). "
           "Phloem transports food materials, usually from the leaves to other parts of the plant. Collenchyma gives "
           "mechanical support to the growing parts, such as the young stem and the petiole of a leaf. Sclerenchyma "
           "provides mechanical support to organs.",
           ["Xylem -> IV", "Phloem -> II", "Collenchyma -> III", "Sclerenchyma -> I"],
           why="The wrong codes swap xylem and phloem, collenchyma and sclerenchyma, or xylem and collenchyma.",
           ncert=ref("ANA", "The Tissues"), secs=35)

statement_pair(T_ANA, "Plant tissues", "Intermediate",
               "Both tracheids and vessel members are devoid of protoplasm at maturity.",
               "Xylem fibres have thin walls and a wide central lumen.",
               True, False, "C",
               "Elements of xylem",
               "Tracheids are elongated, tube-like cells with thick, lignified walls and tapering ends; they are dead "
               "and without protoplasm. Vessel members, with lignified walls and a large central cavity, are also "
               "devoid of protoplasm. Xylem fibres have highly thickened walls and obliterated central lumens.",
               ["Statement I: true", "Statement II: false; xylem fibres have very thick walls and obliterated lumens"],
               ncert=ref("ANA", "The Tissues (complex tissues: xylem)"), secs=35)

direct(T_ANA, "Dicot and monocot anatomy", "Intermediate",
       "A transverse section of a young root shows radial vascular bundles with two to four xylem and phloem patches, "
       "a small pith and an endodermis with Casparian strips. In this organ, lateral roots are initiated in the:",
       "pericycle",
       ["endodermis", "epiblema", "conjunctive tissue"], "B",
       "Dicot root: origin of lateral roots",
       "Two to four xylem and phloem patches and a small or inconspicuous pith identify a dicot root. Next to the "
       "endodermis, towards the inside, lie a few layers of thick-walled parenchymatous cells, the pericycle. "
       "Initiation of lateral roots takes place in these cells.",
       ["Features -> dicot root", "Lateral roots arise in the pericycle"],
       why="The endodermis is the innermost cortical layer with Casparian strips; the epiblema is the outermost layer "
           "bearing root hairs; conjunctive tissue is the parenchyma between xylem and phloem.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicotyledonous root)"), secs=40)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Axillary buds are capable of forming a branch or a flower.",
                 "Axillary buds arise from the activity of the lateral meristem.",
                 True, False, False, "C",
                 "Origin of axillary buds",
                 "During the formation of leaves and elongation of the stem, some cells 'left behind' from the shoot "
                 "apical meristem constitute the axillary bud. Such buds are present in the axils of leaves and are "
                 "capable of forming a branch or a flower. The lateral meristem is a cylindrical meristem in the mature "
                 "regions of roots and shoots.",
                 ["A: true", "R: false; axillary buds come from cells left behind by the shoot apical meristem"],
                 ncert=ref("ANA", "The Tissues (meristematic tissues)"), secs=35)

assertion_reason(T_ANA, "Tissue systems", "Advanced",
                 "In a dicot root, the conjunctive tissue is a part of the stele.",
                 "All tissues on the inner side of the endodermis constitute the stele, and the conjunctive tissue "
                 "lies between the xylem and the phloem, inside the endodermis.",
                 True, True, True, "A",
                 "Stele of the dicot root",
                 "In the dicot root, all tissues on the inner side of the endodermis, such as the pericycle, vascular "
                 "bundles and pith, constitute the stele. The conjunctive tissue is the parenchyma lying between the "
                 "xylem and the phloem, which are within the endodermis; so it falls within the stele.",
                 ["A: true", "R: true", "Being inside the endodermis is exactly what makes a tissue part of the stele"],
                 ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicotyledonous root)"),
                 secs=45)

match_list(T_ANA, "Dicot and monocot anatomy", "Advanced", "feature seen in a section", "organ",
           ["Water-containing cavities within the vascular bundles", "Semi-lunar patches of sclerenchyma above the phloem",
            "Large, well-developed pith with usually more than six xylem bundles",
            "Stomata on both surfaces and an undifferentiated mesophyll"],
           ["Isobilateral leaf", "Monocot root", "Dicot stem", "Monocot stem"],
           "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D",
           "Diagnostic features in sections",
           "Water-containing cavities in the bundles are a feature of the monocot stem. Semi-lunar sclerenchyma patches "
           "above the phloem form the pericycle of the dicot stem. A monocot root has a large, well-developed pith and "
           "usually more than six (polyarch) xylem bundles. An isobilateral leaf has stomata on both surfaces and a "
           "mesophyll not differentiated into palisade and spongy parenchyma.",
           ["A -> monocot stem", "B -> dicot stem", "C -> monocot root", "D -> isobilateral leaf"],
           why="The wrong codes swap the two stems, the monocot root and the isobilateral leaf, or the dicot stem and the "
               "monocot root.",
           ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=50)

statement_pair(T_ANA, "Plant tissues", "Advanced",
               "Phloem fibres (bast fibres) are generally absent in the primary phloem but are found in the secondary "
               "phloem.",
               "Phloem fibres are much elongated and unbranched, with pointed, needle-like apices and quite thick "
               "walls.",
               True, True, "A",
               "Phloem fibres",
               "Phloem fibres (bast fibres) are made up of sclerenchymatous cells. They are generally absent in the "
               "primary phloem but are found in the secondary phloem. They are much elongated, unbranched and have "
               "pointed, needle-like apices, and their cell wall is quite thick. At maturity they lose their "
               "protoplasm and become dead.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("ANA", "The Tissues (complex tissues: phloem)"), secs=40)

direct(T_ANA, "Plant tissues", "Advanced",
       "In which of the following pairs do BOTH cells lack a nucleus at maturity?",
       "Tracheid and sieve tube element",
       ["Companion cell and sieve tube element", "Collenchyma cell and tracheid",
        "Xylem parenchyma cell and vessel member"], "A",
       "Cells without a nucleus at maturity",
       "Tracheids are dead and without protoplasm, so they have no nucleus. A mature sieve tube element is living but "
       "possesses only peripheral cytoplasm and a large vacuole and lacks a nucleus; its functions are controlled by "
       "the nucleus of the companion cell. Companion cells, collenchyma cells and xylem parenchyma cells are living "
       "cells with nuclei.",
       ["Tracheid: dead, no protoplasm", "Sieve tube element: living but no nucleus"],
       why="Each wrong pair includes a living, nucleated cell: the companion cell, the collenchyma cell or the xylem "
           "parenchyma cell.",
       ncert=ref("ANA", "The Tissues (xylem and phloem)"), secs=45)

multi_statement(T_ANA, "Tissue systems", "Advanced",
                "Which of the following lie on the inner side of the endodermis in a dicot stem?",
                [("Pericycle", True), ("Medullary rays", True), ("Hypodermis", False), ("Vascular bundles", True),
                 ("Pith", True)],
                [("a", "d", "e"), ("b", "c", "e"), ("a", "b", "c", "d")], "D",
                "Arrangement of tissues in the dicot stem",
                "In the dicot stem, the cortex has three sub-zones: the outer collenchymatous hypodermis, the cortical "
                "layers and the innermost endodermis. Inside the endodermis lie the pericycle (semi-lunar sclerenchyma "
                "patches above the phloem), the ring of vascular bundles, the medullary rays between the bundles and "
                "the central pith.",
                ["Outside the endodermis: epidermis, hypodermis, cortical layers",
                 "Inside: pericycle, vascular bundles, medullary rays, pith"],
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dicotyledonous stem)"),
                secs=50)
