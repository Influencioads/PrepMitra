
# =============================================================== 4. Anatomy of Flowering Plants (4/5/4)
statement_pair(T_ANA, "Dicot and monocot anatomy", "Basic",
               "In a dorsiventral leaf, the epidermis that covers both the upper (adaxial) and the lower (abaxial) "
               "surface has a conspicuous cuticle.",
               "In a dorsiventral leaf, it is the abaxial epidermis that may even lack stomata.",
               True, False, "C",
               "Epidermis of a dorsiventral leaf",
               "The epidermis covers both the upper surface (adaxial epidermis) and the lower surface (abaxial "
               "epidermis) of a dorsiventral leaf and has a conspicuous cuticle. The abaxial epidermis generally bears "
               "more stomata than the adaxial epidermis; the adaxial (upper) epidermis may even lack stomata.",
               ["Statement I: true", "Statement II: false; the adaxial epidermis may lack stomata"],
               ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dorsiventral leaf)"), secs=35)

direct(T_ANA, "Plant tissues", "Basic",
       "The cells of parenchyma are generally:",
       "isodiametric, with thin walls made of cellulose",
       ["much elongated, with pointed, needle-like apices", "thickened at the corners by cellulose, hemicellulose "
        "and pectin", "dead, with thick and lignified walls"], "D",
       "Parenchyma",
       "Parenchyma forms the major component within organs. Its cells are generally isodiametric; they may be "
       "spherical, oval, round, polygonal or elongated in shape. Their walls are thin and made of cellulose. They may "
       "be closely packed or have small intercellular spaces.",
       ["Parenchyma: isodiametric, thin cellulose walls"],
       why="Needle-like apices describe phloem fibres; corner thickenings describe collenchyma; dead lignified cells "
           "describe sclerenchyma.",
       ncert=ref("ANA", "The Tissues (simple tissues: parenchyma)"), secs=20)

direct(T_ANA, "Dicot and monocot anatomy", "Basic",
       "In a dorsiventral leaf, the vascular bundles of the vascular system can be seen in the:",
       "veins and the midrib",
       ["palisade parenchyma only", "abaxial epidermis", "bulliform cells"], "B",
       "Vascular system of the leaf",
       "A vertical section of a dorsiventral leaf shows three main parts: epidermis, mesophyll and vascular system. "
       "The vascular system includes vascular bundles, which can be seen in the veins and the midrib. The size of the "
       "vascular bundles depends on the size of the veins.",
       ["Leaf: epidermis, mesophyll, vascular system", "Vascular bundles lie in the veins and midrib"],
       why="The palisade parenchyma is part of the mesophyll; the epidermis is the covering layer; bulliform cells are "
           "modified epidermal cells of grass leaves.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (dorsiventral leaf)"), secs=20)

match_list(T_ANA, "Plant tissues", "Basic", "cell", "shape described in NCERT",
           ["Guard cells of a dicot", "Guard cells of a grass", "Sclereids", "Phloem fibres"],
           ["Dumb-bell shaped", "Much elongated and unbranched, with pointed, needle-like apices", "Bean-shaped",
            "Spherical, oval or cylindrical"],
           "III I IV II", ["I III IV II", "III I II IV", "IV I III II"], "A",
           "Shapes of some plant cells",
           "Each stoma has two bean-shaped guard cells; in grasses the guard cells are dumb-bell shaped. Sclereids are "
           "spherical, oval or cylindrical, highly thickened dead cells with very narrow lumen. Phloem fibres are much "
           "elongated, unbranched and have pointed, needle-like apices.",
           ["Dicot guard cell → bean; grass guard cell → dumb-bell", "Sclereid → spherical/oval/cylindrical; "
            "phloem fibre → needle-like"],
           why="The wrong codes interchange the two kinds of guard cells, or the sclereids and fibres.",
           ncert=ref("ANA", "The Tissues; The Tissue System (epidermal tissue system)"), secs=35)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "Collenchyma cells may assimilate food.",
                 "In dicotyledonous plants, collenchyma is found below the epidermis either as a homogeneous layer or "
                 "in patches.",
                 True, True, False, "B",
                 "Collenchyma",
                 "Collenchyma cells often contain chloroplasts, and they assimilate food when they contain chloroplasts. "
                 "Separately, collenchyma occurs in layers below the epidermis in dicotyledonous plants, either as a "
                 "homogeneous layer or in patches. Its position does not explain its ability to assimilate food; the "
                 "chloroplasts do.",
                 ["A: true (when chloroplasts are present)", "R: true, but about position, not the cause of A"],
                 ncert=ref("ANA", "The Tissues (collenchyma)"), secs=40)

assertion_reason(T_ANA, "Plant tissues", "Intermediate",
                 "The functions of a mature sieve tube element are controlled by the nucleus of a companion cell.",
                 "A mature sieve element possesses a peripheral cytoplasm and a large vacuole but lacks a nucleus.",
                 True, True, True, "A",
                 "Sieve tube elements and companion cells",
                 "Sieve tube elements are long tube-like structures associated with companion cells. A mature sieve "
                 "element possesses a peripheral cytoplasm and a large vacuole but lacks a nucleus. Because it has no "
                 "nucleus of its own, its functions are controlled by the nucleus of the companion cell, which is "
                 "connected to it by pit fields in their common longitudinal walls.",
                 ["A: true", "R: true; having no nucleus is why its functions depend on the companion cell"],
                 ncert=ref("ANA", "The Tissues (phloem)"), secs=40)

direct(T_ANA, "Plant tissues", "Intermediate",
       "In flowering plants, tracheids and vessels are the main water-transporting elements. In the xylem of "
       "gymnosperms, water is conducted mainly by:",
       "tracheids, as vessels are absent",
       ["vessels, as tracheids are absent", "xylem fibres", "albuminous cells"], "C",
       "Xylem of gymnosperms",
       "Xylem is composed of tracheids, vessels, xylem fibres and xylem parenchyma. In flowering plants, tracheids and "
       "vessels are the main water-transporting elements. Vessels are a characteristic feature of angiosperms; "
       "gymnosperms lack vessels in their xylem, so the tracheids conduct water.",
       ["Angiosperms: tracheids + vessels", "Gymnosperms: no vessels → tracheids"],
       why="Gymnosperms lack vessels, not tracheids. Xylem fibres are supporting cells. Albuminous cells are found in "
           "the phloem of gymnosperms.",
       ncert=ref("ANA", "The Tissues (xylem)"), secs=35)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Intermediate",
                "Which of the following features are common to the dicot root and the monocot root?",
                [("The vascular bundles are radial.", True),
                 ("A pericycle is present.", True),
                 ("There are usually more than six xylem bundles.", False),
                 ("The pith is large and well developed.", False),
                 ("The primary xylem is exarch.", True)],
                [("a", "b", "c"), ("b", "d", "e"), ("a", "e")], "D",
                "Dicot and monocot roots compared",
                "The anatomy of the monocot root is similar to that of the dicot root in many respects: it has "
                "epidermis, cortex, endodermis, pericycle, vascular bundles and pith. In roots the vascular bundles are "
                "radial and the primary xylem is exarch. They differ in that the monocot root usually has more than six "
                "xylem bundles (polyarch) and a large, well-developed pith, whereas the dicot root has two to four xylem "
                "patches and a small or inconspicuous pith.",
                ["(a), (b), (e): common", "(c), (d): monocot root only"],
                why="(c) and (d) apply only to the monocot root; (a) and (e) alone leave out the pericycle.",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (roots)"), secs=55)

match_list(T_ANA, "Dicot and monocot anatomy", "Intermediate", "feature seen in a section", "organ",
           ["Collenchymatous hypodermis", "Sclerenchymatous hypodermis", "Bulliform cells along the veins",
            "Usually more than six xylem bundles"],
           ["Monocot root", "Dicot stem", "Monocot stem", "Grass leaf"],
           "II III IV I", ["III II IV I", "II III I IV", "IV III II I"], "B",
           "Identifying organs from their anatomy",
           "In the dicot stem, the hypodermis consists of a few layers of collenchymatous cells; the monocot stem has a "
           "sclerenchymatous hypodermis. In grasses, certain adaxial epidermal cells along the veins are modified into "
           "large, empty, colourless bulliform cells. The monocot root usually has more than six xylem bundles "
           "(polyarch).",
           ["Collenchymatous hypodermis → dicot stem", "Sclerenchymatous hypodermis → monocot stem",
            "Bulliform cells → grass leaf", "Polyarch → monocot root"],
           why="The wrong codes swap the two kinds of hypodermis, or the grass leaf and the monocot root.",
           ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants"), secs=40)

_VASC = {"phloem fibres": True, "xylem parenchyma": True, "pericycle": False, "companion cells": True,
         "medullary rays": False, "tracheids": True, "endodermis": False, "bulliform cells": False}
numerical(T_ANA, "Tissue systems", "Advanced",
          "How many of the following belong to the vascular (conducting) tissue system?\n"
          "phloem fibres, xylem parenchyma, pericycle, companion cells, medullary rays, tracheids, endodermis, "
          "bulliform cells",
          "4", ["3", "5", "6"], "A", sum(_VASC.values()) == 4,
          "The three tissue systems",
          "The vascular system consists of the complex tissues xylem (tracheids, vessels, xylem fibres, xylem "
          "parenchyma) and phloem (sieve tube elements, companion cells, phloem parenchyma, phloem fibres). All tissues "
          "except the epidermis and vascular bundles form the ground tissue: cortex, endodermis, pericycle, pith and "
          "medullary rays. Bulliform cells are modified epidermal cells.",
          ["Vascular: phloem fibres, xylem parenchyma, companion cells, tracheids = 4",
           "Ground: pericycle, medullary rays, endodermis", "Epidermal: bulliform cells"],
          why="3 leaves out a parenchyma or fibre component of xylem or phloem; 5 or 6 count the pericycle, medullary "
              "rays or endodermis, which are ground tissue even though they lie close to the vascular bundles.",
          ncert=ref("ANA", "The Tissue System"), secs=50)

multi_statement(T_ANA, "Dicot and monocot anatomy", "Advanced",
                "A leaf section shows stomata on both surfaces, a mesophyll not differentiated into palisade and spongy "
                "parenchyma, vascular bundles of nearly similar size except in the main veins, and large, empty, "
                "colourless cells in the adaxial epidermis along the veins. Which of the following conclusions are "
                "correct?",
                [("The leaf is an isobilateral leaf of a grass.", True),
                 ("When these large epidermal cells lose water and become flaccid, the leaf curls inwards.", True),
                 ("The near-similar size of the vascular bundles reflects the parallel venation of the leaf.", True),
                 ("The guard cells of its stomata are bean-shaped.", False),
                 ("Its palisade parenchyma lies adaxially.", False)],
                [("a", "b", "d"), ("a", "c", "e"), ("b", "c")], "D",
                "Interpreting a section of an isobilateral leaf",
                "Stomata on both surfaces and an undifferentiated mesophyll mark an isobilateral (monocot) leaf. The "
                "large, empty, colourless adaxial cells along the veins are bulliform cells of grasses; when they are "
                "flaccid due to water stress, the leaf curls inwards to minimise water loss. The parallel venation of "
                "monocot leaves is reflected in the near-similar sizes of the vascular bundles (except in the main "
                "veins). In grasses the guard cells are dumb-bell shaped, and an isobilateral leaf has no palisade "
                "layer.",
                ["(a), (b), (c) true", "(d) false: dumb-bell shaped in grasses", "(e) false: mesophyll undifferentiated"],
                why="(d) and (e) are false; (b) and (c) alone leave out (a).",
                ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (isobilateral leaf)"), secs=70)

assertion_reason(T_ANA, "Plant tissues", "Advanced",
                 "Phloem fibres lose their protoplasm and become dead at maturity.",
                 "Phloem fibres are present in the primary phloem but are absent in the secondary phloem.",
                 True, False, False, "C",
                 "Phloem fibres",
                 "Phloem fibres (bast fibres) are made up of sclerenchymatous cells. At maturity these fibres lose their "
                 "protoplasm and become dead. They are generally absent in the primary phloem but are found in the "
                 "secondary phloem, so R states the reverse of the NCERT position.",
                 ["A: true", "R: false; they are absent in primary and present in secondary phloem"],
                 ncert=ref("ANA", "The Tissues (phloem fibres)"), secs=40)

direct(T_ANA, "Dicot and monocot anatomy", "Advanced",
       "A stem section shows conjoint vascular bundles with no cambium between the xylem and the phloem, phloem "
       "parenchyma absent from the bundles, and water-containing cavities within the bundles. The stem is most "
       "likely that of:",
       "a monocotyledon",
       ["a dicotyledon", "a gymnosperm", "a dicotyledon, as the bundles are open"], "B",
       "Identifying a monocot stem",
       "Conjoint bundles without cambium are closed, as in monocot stems and leaves. In the monocot stem, phloem "
       "parenchyma is absent and water-containing cavities are present within the vascular bundles. Dicot stem "
       "bundles are conjoint and open, with cambium between phloem and xylem.",
       ["No cambium → closed bundles", "No phloem parenchyma + water cavities → monocot stem"],
       why="Dicot stems have open bundles with cambium. Bundles without cambium are closed, not open. Gymnosperms are "
           "not described with closed bundles having water-containing cavities.",
       ncert=ref("ANA", "Anatomy of Dicotyledonous and Monocotyledonous Plants (monocot stem)"), secs=45)
