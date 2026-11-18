
# =============================================================== 9. Plant Growth and Development (3/5/3)
_promoters = {"IAA": True, "IBA": True, "GA3": True, "kinetin": True, "zeatin": True, "ABA": False}
numerical(T_PGD, "Plant growth regulators", "Basic",
          "NCERT broadly divides plant growth regulators into growth promoters and growth inhibitors. How many of "
          "the following belong to the growth-promoting group?\n\nindole-3-acetic acid (IAA), indole butyric acid "
          "(IBA), gibberellic acid (GA₃), kinetin, zeatin, abscisic acid (ABA)",
          "5", ["3", "4", "6"], "A",
          sum(_promoters.values()) == 5,
          "Promoters and inhibitors among PGRs",
          "NCERT: one group of PGRs is involved in growth-promoting activities such as cell division, cell "
          "enlargement, pattern formation, tropic growth, flowering, fruiting and seed formation - the auxins, "
          "gibberellins and cytokinins. The other group, which includes abscisic acid, plays an important role in "
          "responses to wounds and stresses and in dormancy and abscission. IAA and IBA are auxins, GA₃ is a "
          "gibberellin, and kinetin and zeatin are cytokinins.",
          ["Auxins: IAA, IBA", "Gibberellin: GA₃", "Cytokinins: kinetin, zeatin", "Inhibitor: ABA",
           "Promoters = 5"],
          why="3 counts only one member of each promoter group. 4 leaves out one of the two cytokinins or one of "
              "the two auxins. 6 wrongly counts ABA, a growth inhibitor.",
          ncert=ref("PGD", "Plant Growth Regulators (characteristics)"), secs=40)

direct(T_PGD, "Plant growth regulators", "Basic",
       "Which of the following is NOT an auxin?",
       "Zeatin",
       ["Indole-3-acetic acid (IAA)", "Indole butyric acid (IBA)", "Naphthalene acetic acid (NAA)"], "D",
       "Identifying auxins",
       "IAA and IBA are natural auxins isolated from plants, and NAA (with 2,4-D) is a synthetic auxin. Zeatin is a "
       "naturally occurring cytokinin isolated from corn kernels and coconut milk.",
       ["Auxins: IAA, IBA (natural), NAA, 2,4-D (synthetic)", "Zeatin: cytokinin"],
       why="IAA, IBA and NAA are all auxins named in NCERT.",
       ncert=ref("PGD", "Plant Growth Regulators (auxins; cytokinins)"), secs=20)

statement_pair(T_PGD, "Plant growth regulators", "Basic",
               "Abscisic acid was discovered for its role in regulating abscission and dormancy.",
               "Ethylene is used to initiate flowering and to synchronise fruit-set in pineapples.",
               True, True, "A",
               "Abscisic acid; ethylene in pineapple",
               "NCERT: abscisic acid was discovered for its role in regulating abscission and dormancy. Ethylene is "
               "used to initiate flowering and to synchronise fruit-set in pineapples, and it also induces flowering "
               "in mango.",
               ["Statement I: true", "Statement II: true"],
               ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=25)

match_list(T_PGD, "Plant growth regulators", "Intermediate", "plant growth regulator",
           "site of production or source described in NCERT",
           ["Auxins (natural)", "Cytokinins (natural)", "Ethylene", "Kinetin"],
           ["Tissues undergoing senescence and ripening fruits, in large amounts",
            "Growing apices of the stems and roots",
            "Autoclaved herring sperm DNA",
            "Regions of rapid cell division, such as root apices, developing shoot buds and young fruits"],
           "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "A",
           "Where PGRs come from",
           "Auxins are generally produced by the growing apices of the stems and roots, from where they migrate to "
           "their regions of action. Natural cytokinins are synthesised in regions where rapid cell division occurs, "
           "such as root apices, developing shoot buds and young fruits. Ethylene is synthesised in large amounts by "
           "tissues undergoing senescence and by ripening fruits. Kinetin was discovered as a modified form of "
           "adenine in autoclaved herring sperm DNA.",
           ["Auxins -> II", "Cytokinins -> IV", "Ethylene -> I", "Kinetin -> III"],
           why="The wrong codes swap auxins with cytokinins, ethylene with kinetin, or cytokinins with ethylene.",
           ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=50)

assertion_reason(T_PGD, "Plant growth regulators", "Intermediate",
                 "Abscisic acid stimulates the closure of stomata.",
                 "Chemically, abscisic acid is a derivative of carotenoids.",
                 True, True, False, "B",
                 "Two separate facts about ABA",
                 "Abscisic acid acts as a general plant growth inhibitor and an inhibitor of plant metabolism; it "
                 "inhibits seed germination, stimulates the closure of stomata and increases tolerance to stresses. "
                 "Separately, NCERT classifies ABA chemically as a derivative of carotenoids. Its chemical origin is "
                 "not given as the reason for its effect on stomata.",
                 ["A: true", "R: true", "The chemical class of ABA does not explain stomatal closure -> R is not "
                  "the explanation"],
                 ncert=ref("PGD", "Plant Growth Regulators (characteristics; abscisic acid)"), secs=35)

multi_statement(T_PGD, "Plant growth regulators", "Intermediate",
                "Which of the following effects are attributed to abscisic acid in NCERT?",
                [("It promotes female flowers in cucumbers.", False),
                 ("It inhibits seed germination.", True),
                 ("It stimulates the closure of stomata.", True),
                 ("It helps to overcome apical dominance.", False),
                 ("It increases the tolerance of plants to various kinds of stresses.", True)],
                [("b", "c"), ("a", "b", "e"), ("c", "d", "e")], "D",
                "Effects of abscisic acid",
                "ABA regulates abscission and dormancy, inhibits seed germination, stimulates the closure of stomata "
                "and increases tolerance to various stresses (hence 'stress hormone'). Promotion of female flowers "
                "in cucumbers is an effect of ethylene, and overcoming apical dominance is an effect of cytokinins.",
                ["(b), (c), (e): ABA", "(a): ethylene", "(d): cytokinins"],
                why="(b) and (c) only leaves out the stress tolerance that gives ABA the name stress hormone. The other "
                    "combinations include an effect of ethylene or of cytokinins.",
                ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (abscisic acid)"), secs=50)

direct(T_PGD, "Plant growth regulators", "Intermediate",
       "Which plant growth regulator BOTH promotes root growth and root hair formation and promotes the senescence "
       "and abscission of plant organs, especially of leaves and flowers?",
       "Ethylene",
       ["Cytokinin", "Gibberellin", "Abscisic acid"], "A",
       "Effects of ethylene",
       "NCERT: ethylene promotes senescence and abscission of plant organs, especially of leaves and flowers. It "
       "also promotes root growth and root hair formation, thus helping plants to increase their absorption "
       "surface.",
       ["Root growth and root hairs: ethylene", "Senescence and abscission of leaves and flowers: ethylene"],
       why="Cytokinins delay leaf senescence. Gibberellins delay senescence and are not linked with root hairs. "
           "ABA regulates abscission and dormancy, but NCERT does not credit it with promoting root hairs.",
       ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (ethylene)"), secs=35)

statement_pair(T_PGD, "Growth rate", "Intermediate",
               "In geometric growth, the initial growth is slow (lag phase), and it increases rapidly thereafter at "
               "an exponential rate (log phase).",
               "In arithmetic growth, a plot of length against time gives a sigmoid curve.",
               True, False, "C",
               "Geometric and arithmetic growth curves",
               "In geometric growth the initial growth is slow (lag phase) and then rises rapidly at an exponential "
               "rate (log or exponential phase); with limited nutrients it slows down to a stationary phase, giving "
               "a sigmoid curve. In arithmetic growth, only one daughter cell continues to divide, and a plot of "
               "length against time gives a linear curve.",
               ["Statement I: true", "Statement II: false; arithmetic growth gives a straight line"],
               ncert=ref("PGD", "Growth (growth rates)"), secs=35)

direct(T_PGD, "Differentiation and redifferentiation", "Advanced",
       "In a woody dicot, a parenchyma cell formed from a meristem matures and loses the ability to divide. Later it "
       "regains that ability and becomes part of the cork cambium, which cuts off cork cells that again lose the "
       "capacity to divide. Which sequence of processes does this show?",
       "Differentiation -> dedifferentiation -> redifferentiation",
       ["Dedifferentiation -> differentiation -> redifferentiation",
        "Differentiation -> redifferentiation -> dedifferentiation",
        "Redifferentiation -> dedifferentiation -> differentiation"], "A",
       "Differentiation, dedifferentiation and redifferentiation",
       "Cells derived from meristems mature to perform specific functions - differentiation. Living differentiated "
       "cells that have lost the capacity to divide can regain it, as when the cork cambium forms from fully "
       "differentiated parenchyma cells - dedifferentiation. The cells produced by such a dedifferentiated "
       "meristem again lose the capacity to divide and mature to perform specific functions - redifferentiation.",
       ["Meristem cell -> parenchyma: differentiation", "Parenchyma -> cork cambium: dedifferentiation",
        "Cork cambium -> cork cells: redifferentiation"],
       why="The other options put the steps in the wrong order: dedifferentiation can only act on a cell that has "
           "already differentiated, and redifferentiation needs a dedifferentiated meristem.",
       ncert=ref("PGD", "Differentiation, Dedifferentiation and Redifferentiation"), secs=50)

assertion_reason(T_PGD, "Plant growth regulators", "Advanced",
                 "Auxins promote the abscission of older, mature leaves and fruits.",
                 "Auxins prevent fruit and leaf drop at all stages of development.",
                 True, False, False, "C",
                 "Dual effect of auxins on abscission",
                 "NCERT: auxins prevent fruit and leaf drop at early stages but promote the abscission of older, "
                 "mature leaves and fruits. The prevention of drop is limited to early stages, so R overstates it.",
                 ["A: true", "R: false - auxins prevent drop only at early stages"],
                 ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators (auxins)"), secs=40)

statement_pair(T_PGD, "Plant growth regulators", "Advanced",
               "Both ethylene and abscisic acid promote seed germination.",
               "Both gibberellins and cytokinins strengthen apical dominance.",
               False, False, "B",
               "Opposing and shared effects of PGRs",
               "Ethylene breaks seed and bud dormancy and initiates germination in peanut seeds, but abscisic acid "
               "inhibits seed germination. Auxins cause apical dominance, while cytokinins help to overcome it; NCERT "
               "does not credit gibberellins with strengthening apical dominance.",
               ["Statement I: false; ABA inhibits seed germination",
                "Statement II: false; cytokinins overcome apical dominance"],
               ncert=ref("PGD", "Physiological Effects of Plant Growth Regulators"), secs=45)
