
# ================================================================ Sexual Reproduction in Flowering Plants (6 / 9 / 6)
C12_SR = lambda s: ref(12, SRFP, s)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "In the gynoecium of a flower, NCERT describes structures that arise from the placenta and are the "
    "megasporangia. These megasporangia are commonly called:",
    P("Ovules", ["Ovaries", "Embryo sacs", "Locules"], "A"),
    "The ovule is the megasporangium",
    "NCERT: inside the ovary is the ovarian cavity (locule); the placenta is located inside it, and arising from "
    "the placenta are the megasporangia, commonly called ovules. The embryo sac (female gametophyte) lies inside "
    "the nucellus of the ovule, so it is not the sporangium itself.",
    ["Ovary → locule → placenta", "Megasporangia arise from the placenta", "Megasporangia = ovules"],
    C12_SR("pre-fertilisation: the pistil, megasporangium (ovule) and embryo sac"),
    why="The ovary encloses the ovules, the locule is the ovarian cavity, and the embryo sac is the female "
        "gametophyte formed inside the ovule.",
    seconds=20)

add(SRFP, "Microsporogenesis and male gametophyte", "Basic", "direct",
    "In transverse section, a typical angiosperm anther is a four-sided (tetragonal) structure. Where are its "
    "microsporangia located?",
    P("At the four corners, two in each lobe",
      ["All four in the centre, around the connective", "One at each corner of a single lobe, the other lobe being "
       "sterile", "Two at the corners and two along the middle of the anther"], "C"),
    "Arrangement of microsporangia in an anther",
    "NCERT: the anther is a four-sided (tetragonal) structure consisting of four microsporangia located at the "
    "corners, two in each lobe. This fits the bilobed, dithecous anther: each lobe has two theca, and each theca "
    "contains one microsporangium.",
    ["Bilobed, dithecous anther", "Four microsporangia", "At the corners, two in each lobe"],
    C12_SR("pre-fertilisation: stamen, microsporangium and pollen grain"),
    why="NCERT places the microsporangia at the corners, not in the centre, and both lobes are fertile, with two "
        "microsporangia each.",
    seconds=25)

add(SRFP, "Megasporogenesis and embryo sac", "Basic", "direct",
    "The nucleus of the functional megaspore divides mitotically to form two nuclei. According to NCERT, these two "
    "nuclei:",
    P("Move to the opposite poles, forming the 2-nucleate embryo sac",
      ["Fuse with each other to form a diploid nucleus", "Move to the opposite poles, and a cell wall is laid down "
       "between them at once", "Both remain at the micropylar end and directly form the egg apparatus"], "B"),
    "Early development of the embryo sac",
    "NCERT: the nucleus of the functional megaspore divides mitotically to form two nuclei, which move to the "
    "opposite poles, forming the 2-nucleate embryo sac. Two more sequential mitotic nuclear divisions give the "
    "4-nucleate and then the 8-nucleate stages. These divisions are strictly free nuclear: cell walls are laid "
    "down only after the 8-nucleate stage.",
    ["First mitosis → two nuclei", "They move to opposite poles", "2-nucleate embryo sac; walls come only after "
     "the 8-nucleate stage"],
    C12_SR("pre-fertilisation: female gametophyte"),
    why="The nuclei do not fuse; no wall forms at this stage because the divisions are free nuclear; and the egg "
        "apparatus is organised only after the 8-nucleate stage.",
    seconds=25)

add(SRFP, "Pollination", "Basic", "direct",
    "Plants such as Viola, Oxalis and Commelina bear cleistogamous flowers, which do not open at all. How does "
    "pollination take place in these flowers?",
    P("The anthers dehisce in the flower buds, and the pollen grains come in contact with the stigma",
      ["Insects carry pollen to them from the chasmogamous flowers of the same plant",
       "Wind carries pollen from other plants through small openings in the petals",
       "Pollen grains are carried by water to the stigma after the bud is submerged"], "D"),
    "Pollination in cleistogamous flowers",
    "NCERT: in cleistogamous flowers the anthers and stigma lie close to each other. When the anthers dehisce in "
    "the flower buds, the pollen grains come in contact with the stigma to effect pollination. Such flowers are "
    "invariably autogamous, since there is no chance of cross-pollen landing on the stigma.",
    ["Flower never opens", "Anthers and stigma lie close together", "Anthers dehisce inside the bud → autogamy"],
    C12_SR("pollination: kinds of pollination (autogamy)"),
    why="A closed flower cannot receive pollen from insects, wind or water; that is why cleistogamous flowers are "
        "invariably autogamous.",
    seconds=25)

add(SRFP, "Endosperm and embryo", "Basic", "statement_pair",
    sp("As the ovules mature into seeds, the ovary develops into a fruit; the transformation of ovules into seeds "
       "and of the ovary into a fruit proceeds simultaneously.",
       "Most fruits develop only from the ovary and are called true fruits."),
    SP("A"),
    "Seed and fruit formation; true fruits",
    "NCERT: as ovules mature into seeds, the ovary develops into a fruit, i.e. the transformation of ovules into "
    "seeds and ovary into fruit proceeds simultaneously (Statement I true). In a few species such as apple, "
    "strawberry and cashew, the thalamus also contributes to the fruit (false fruits); most fruits, however, develop "
    "only from the ovary and are called true fruits (Statement II true).",
    ["Statement I: true (simultaneous)", "Statement II: true (true fruits from the ovary only)"],
    C12_SR("post-fertilisation: seed and fruit"),
    seconds=30)

add(SRFP, "Pollination", "Basic", "assertion_reason",
    ar("It is believed that the distribution of some bryophytes and pteridophytes is limited.",
       "In these plants, water is needed for the transport of the male gametes and for fertilisation."),
    AR("A"),
    "Water and the male gametes of lower plants",
    "NCERT contrasts the rarity of water pollination in flowering plants with lower plant groups (algae, "
    "bryophytes and pteridophytes), in which water is a regular mode of transport for the male gametes. It states "
    "that, particularly for some bryophytes and pteridophytes, their distribution is believed to be limited because "
    "of the need for water for the transport of male gametes and fertilisation. R is the very reason given for A.",
    ["A: true (NCERT)", "R: true (water carries the male gametes)", "R is the stated cause of A"],
    C12_SR("pollination: agents of pollination (water)"),
    seconds=35)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "direct",
    "NCERT describes two ways in which apomictic seeds may develop. Which of them does it say happens more often?",
    P("Some nucellar cells surrounding the embryo sac start dividing, protrude into the embryo sac and develop into "
      "embryos, as in many Citrus and mango varieties",
      ["A diploid egg cell is formed without reduction division and develops into the embryo without fertilisation",
       "The primary endosperm cell develops into an embryo instead of an endosperm",
       "A synergid is fertilised by the second male gamete and develops into an extra embryo"], "C"),
    "Ways of developing apomictic seeds",
    "NCERT: there are several ways of development of apomictic seeds. In some species, the diploid egg cell is "
    "formed without reduction division and develops into the embryo without fertilisation. More often, as in many "
    "Citrus and mango varieties, some of the nucellar cells surrounding the embryo sac start dividing, protrude into "
    "the embryo sac and develop into embryos; in such species each ovule contains many embryos.",
    ["Way 1 ('in some species'): unreduced diploid egg → embryo", "Way 2 ('more often'): nucellar cells → embryos",
     "Example of way 2: Citrus, mango"],
    C12_SR("apomixis and polyembryony"),
    why="The unreduced-egg route is described for 'some species', not as the commoner route; NCERT gives no "
        "apomixis from the primary endosperm cell or from a fertilised synergid.",
    seconds=35)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "statement_pair",
    sp("Following compatible pollination, the contents of the pollen grain move into the pollen tube, which grows "
       "through the tissues of the stigma and style and reaches the ovary.",
       "The pollen tube can emerge from any point on the pollen grain, because sporopollenin forms a continuous "
       "layer over the whole exine."),
    SP("C"),
    "Germination of the pollen grain on the stigma",
    "NCERT: following compatible pollination, the pollen grain germinates on the stigma to produce a pollen tube "
    "through one of the germ pores; the contents of the pollen grain move into the pollen tube, which grows through "
    "the tissues of the stigma and style and reaches the ovary (Statement I true). The exine has prominent "
    "apertures, the germ pores, where sporopollenin is absent; the tube emerges through one of them, not from any "
    "point (Statement II false).",
    ["Statement I: true", "Germ pores: sporopollenin absent", "Tube emerges through a germ pore → Statement II "
     "false"],
    C12_SR("pollination: pollen-pistil interaction"),
    seconds=35)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "multi_statement",
    ms("Compare microsporogenesis and megasporogenesis in a typical flowering plant. Which of the following "
       "statements are correct?",
       ["In both, a diploid spore mother cell divides by meiosis to give four haploid spores.",
        "All four microspores of a tetrad normally develop into pollen grains, whereas in a majority of flowering "
        "plants only one of the four megaspores is functional.",
        "Both the male and the female gametophyte develop from a haploid spore by mitotic division.",
        "The pollen mother cell is differentiated in the micropylar region of the nucellus.",
        "The four megaspores dissociate from each other as the anther dehydrates."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Spore formation and gametophyte development compared",
    "(a) True: a pollen mother cell gives a microspore tetrad by meiosis, and the megaspore mother cell gives four "
    "megaspores by meiosis. (b) True: as the anthers mature, the microspores dissociate and develop into pollen "
    "grains, while in most flowering plants one megaspore is functional and three degenerate. (c) True: the "
    "microspore nucleus divides mitotically to form the vegetative and generative cells, and the functional "
    "megaspore nucleus divides mitotically to form the embryo sac. (d) False: it is the megaspore mother cell that "
    "is differentiated in the micropylar region of the nucellus. (e) False: it is the microspores that dissociate "
    "as the anther dehydrates.",
    ["Meiosis in both (a)", "4 pollen grains vs 1 functional megaspore (b)", "Gametophytes by mitosis (c)",
     "(d), (e): male and female features swapped"],
    C12_SR("pre-fertilisation: microsporogenesis, megasporogenesis and the female gametophyte"),
    why="Options with (d) or (e) include a male feature given to the female side or the reverse; '(b), (c) and (e)' "
        "also leaves out the true statement (a).",
    seconds=55)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Intermediate", "direct",
    "In an artificial hybridisation experiment with a female parent bearing bisexual flowers, a worker removes the "
    "anthers only after they have dehisced. Why is this a mistake, according to the logic of NCERT's procedure?",
    P("Pollen of the same flower may already have reached the stigma, so some seeds may come from self-pollination "
      "instead of the desired cross",
      ["Anthers that have dehisced can no longer be removed with forceps",
       "Dehisced anthers secrete chemicals that make the stigma permanently non-receptive",
       "Emasculation is never needed in bisexual flowers, so the worker should not have removed the anthers"], "D"),
    "Purpose of emasculation before anther dehiscence",
    "NCERT: in crossing experiments it is important that only the desired pollen grains are used and the stigma is "
    "protected from contamination. If the female parent bears bisexual flowers, the anthers are removed from the "
    "flower bud before the anther dehisces (emasculation), and the flower is then bagged. Once the anthers have "
    "dehisced, the flower's own pollen may already have contaminated the stigma, defeating the purpose.",
    ["Goal: only the desired pollen on the stigma", "Own anthers → self-pollen", "Remove them in the bud, before "
     "dehiscence"],
    C12_SR("pollination: artificial hybridisation"),
    why="The problem is contamination, not difficulty of removal or a chemical effect; and emasculation is exactly "
        "what NCERT requires for bisexual flowers.",
    seconds=40)

add(SRFP, "Pollination", "Intermediate", "assertion_reason",
    ar("Wind-pollinated flowers often have a large, often feathery stigma.",
       "A large, feathery stigma can easily trap air-borne pollen grains."),
    AR("A"),
    "Adaptations of wind-pollinated flowers",
    "NCERT: wind-pollinated flowers often have well-exposed stamens (so that pollen is easily dispersed into wind "
    "currents) and a large, often feathery stigma to easily trap air-borne pollen grains. Since wind carries pollen "
    "at random, a large trapping surface raises the chance that pollen lands on the stigma. R gives the function "
    "for which the feature in A exists.",
    ["A: true", "R: true, the purpose of the feathery stigma", "R explains A"],
    C12_SR("pollination: agents of pollination (wind)"),
    seconds=30)

add(SRFP, "Endosperm and embryo", "Intermediate", "multi_statement",
    ms("Consider where reserve food is found in mature seeds of the plants named in NCERT. Which of the following "
       "statements are correct?",
       ["In a mature pea seed, the endosperm has been consumed, and the food reserves lie in the thick, swollen "
        "cotyledons.",
        "In a mature castor seed, a part of the endosperm persists and is used up during seed germination.",
        "In a mature beet seed, a persistent remnant of the nucellus is present.",
        "In coconut, the endosperm is completely consumed by the embryo before the seed matures.",
        "In groundnut, the endosperm persists in the mature seed."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
    "Persistence of endosperm and perisperm",
    "NCERT: the endosperm may be completely consumed by the developing embryo before seed maturation (pea, "
    "groundnut, beans), or it may persist in the mature seed (castor and coconut) and be used up during seed "
    "germination. In legumes the cotyledons are thick and swollen due to storage of food reserves. In black pepper "
    "and beet, remnants of the nucellus persist as the perisperm. So (a), (b) and (c) are true; (d) and (e) "
    "reverse the cases of coconut and groundnut.",
    ["Pea, groundnut: endosperm consumed; cotyledons store food", "Castor, coconut: endosperm persists",
     "Beet: perisperm"],
    C12_SR("post-fertilisation: endosperm; seed"),
    why="Coconut keeps its endosperm and groundnut does not, so options with (d) or (e) are wrong.",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Intermediate", "statement_pair",
    sp("The megaspore mother cell is differentiated in the micropylar region of the nucellus, and the embryo later "
       "develops at the micropylar end of the embryo sac, where the zygote is situated.",
       "In a mature embryo sac, the three antipodal cells lie at the micropylar end, next to the egg apparatus."),
    SP("C"),
    "Polarity of the ovule and embryo sac",
    "NCERT: ovules generally differentiate a single megaspore mother cell in the micropylar region of the nucellus, "
    "and the embryo develops at the micropylar end of the embryo sac where the zygote is situated (Statement I "
    "true). In the mature embryo sac, three cells are grouped together at the micropylar end (the egg apparatus) "
    "and three cells, the antipodals, are at the chalazal end (Statement II false).",
    ["MMC: micropylar region; embryo: micropylar end → I true", "Antipodals: chalazal end → II false"],
    C12_SR("pre-fertilisation: female gametophyte; post-fertilisation: embryo"),
    seconds=35)

add(SRFP, "Double fertilisation", "Intermediate", "match_list",
    ml(("event", "where it takes place"),
       ["Meiosis of the megaspore mother cell", "Meiosis of the pollen mother cell",
        "Syngamy and triple fusion", "Germination of a compatible pollen grain"],
       ["Stigma", "Embryo sac", "Nucellus of the ovule", "Microsporangium of the anther"]),
    M(mc("III,IV,II,I"), [mc("IV,III,II,I"), mc("III,IV,I,II"), mc("II,IV,III,I")], "D"),
    "Sites of the main reproductive events",
    "The megaspore mother cell lies in the micropylar region of the nucellus and divides there by meiosis (A-III). "
    "Pollen mother cells develop from the sporogenous tissue of the microsporangium and undergo meiosis there "
    "(B-IV). The pollen tube releases "
    "the two male gametes into a synergid of the embryo sac, where one fuses with the egg (syngamy) and the other "
    "with the polar nuclei in the central cell (triple fusion) (C-II). A compatible pollen grain germinates on "
    "the stigma (D-I).",
    ["A → nucellus", "B → microsporangium", "C → embryo sac", "D → stigma"],
    C12_SR("pre-fertilisation events; double fertilisation"),
    why="The other codes swap the two meiotic sites, put fertilisation on the stigma, or put megaspore formation "
        "in the embryo sac, which forms only after meiosis.",
    seconds=40)

add(SRFP, "Apomixis, parthenocarpy and polyembryony", "Intermediate", "multi_statement",
    ms("Which of the following statements about apomixis and polyembryony are correct according to NCERT?",
       ["When seeds of orange are squeezed, many embryos of different sizes and shapes can be seen from each seed.",
        "In species in which nucellar cells develop into embryos, each ovule contains many embryos.",
        "Scientists are working to understand the genetics of apomixis and to transfer apomictic genes into hybrid "
        "varieties.",
        "Polyembryony means the presence of more than one embryo sac in an ovule.",
        "Apomixis is found in all members of Asteraceae and grasses."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "b", "e"], ["c", "d", "e"]], "D"),
    "Polyembryony and the hope of apomictic hybrids",
    "NCERT: in many Citrus and mango varieties, nucellar cells protrude into the embryo sac and develop into "
    "embryos, so each ovule contains many embryos (b); squeezing orange seeds shows many embryos of different sizes "
    "and shapes from each seed (a). Many scientists are working to understand the genetics of apomixis and to "
    "transfer apomictic genes into hybrid varieties (c). Polyembryony is the occurrence of more than one embryo "
    "in a seed, not of extra embryo sacs (d false), and apomixis is seen in some species of Asteraceae and grasses, "
    "not all (e false).",
    ["(a), (b), (c): NCERT statements", "(d): embryos, not embryo sacs", "(e): 'some species', not all"],
    C12_SR("apomixis and polyembryony"),
    why="Any option with (d) or (e) contains a false statement.",
    seconds=45)

_seeds = Counter()
for _f, _m in product("Aa", repeat=2):          # female gametophyte allele, male gamete allele (each 1/2)
    _seeds[("".join(sorted(_f + _m)), "".join(sorted(_f + _f + _m)))] += F(1, 4)
assert _seeds[("Aa", "AAa")] == F(1, 4) and sum(v for (e, _), v in _seeds.items() if e == "Aa") == F(1, 2)

add(SRFP, "Double fertilisation", "Advanced", "numerical",
    "A plant of genotype Aa is self-pollinated. Megasporogenesis is normal and monosporic, and each seed forms by "
    "normal double fertilisation. In what fraction of the seeds will the embryo be Aa and the endosperm AAa?",
    P("1/4", ["1/2", "1/16", "3/4"], "B"),
    "Genotypes of embryo and endosperm in the same seed",
    "All nuclei of an embryo sac come by mitosis from one haploid megaspore, so the egg and both polar nuclei carry "
    "the same allele (A or a, probability 1/2 each). Both male gametes of a pollen grain come from one generative "
    "cell, so they carry the same allele (A or a, 1/2 each). Embryo Aa with endosperm AAa needs a female "
    "gametophyte carrying A (endosperm gets A + A from the polar nuclei) and a pollen grain carrying a: "
    "1/2 × 1/2 = 1/4. (The other Aa embryos, from an a embryo sac and an A pollen grain, have endosperm Aaa.)",
    ["P(embryo sac carries A) = 1/2", "P(pollen carries a) = 1/2", "Embryo Aa and endosperm AAa: 1/2 × 1/2 = 1/4"],
    C12_SR("pre-fertilisation: female gametophyte; double fertilisation"),
    why="1/2 counts every Aa embryo, including those with endosperm Aaa; 1/16 wrongly treats the egg and each polar "
        "nucleus as receiving alleles independently; 3/4 is the fraction of embryos carrying at least one A.",
    seconds=90, verified_by=RECOMPUTED)

add(SRFP, "Endosperm and embryo", "Advanced", "multi_statement",
    ms("In a plant of genotype Aa, seeds are formed after cross-pollination with pollen from a plant of genotype "
       "aa. Which of the following are expected to be genetically identical to the mother plant (Aa) in every "
       "seed or fruit?",
       ["The seed coat", "The perisperm, in a species that has one", "The pericarp",
        "A nucellar embryo, in a species with nucellar polyembryony", "The endosperm"]),
    MS(["a", "b", "c", "d"], [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "C"),
    "Maternal tissues in seeds and fruits",
    "The seed coat develops from the integuments, the perisperm is the persistent nucellus, and the pericarp "
    "develops from the ovary wall: all three are tissues of the mother sporophyte, so they are Aa. A nucellar "
    "embryo arises from a diploid nucellar cell without fertilisation, so it is also Aa. The endosperm develops "
    "from the triple-fused primary endosperm cell: here it is AAa or aaa, never identical to the mother.",
    ["Integuments → seed coat (maternal)", "Nucellus → perisperm (maternal)", "Ovary wall → pericarp (maternal)",
     "Nucellar embryo: maternal; endosperm: AAa or aaa"],
    C12_SR("post-fertilisation: seed and fruit; apomixis and polyembryony"),
    why="'(a), (b) and (c) only' leaves out the nucellar embryo; options with (e) include the triploid endosperm, "
        "which carries the paternal allele.",
    seconds=60)

add(SRFP, "Outbreeding devices and pollen-pistil interaction", "Advanced", "direct",
    "A species with bisexual flowers shows self-incompatibility. A bee carries pollen from one flower to the stigma "
    "of another flower on the same plant. What is the expected outcome?",
    P("The pistil recognises the pollen as 'self' and inhibits pollen germination or pollen tube growth, so the "
      "ovules are not fertilised by it",
      ["Fertilisation occurs, because the pollen came from a different flower and so counts as cross-pollen",
       "The pollen tube grows normally, but the endosperm fails to form",
       "Fertilisation occurs, because self-incompatibility acts only against autogamy within a flower"], "B"),
    "Self-incompatibility blocks geitonogamous pollen too",
    "Transfer of pollen to another flower of the same plant is geitonogamy, which is genetically similar to "
    "autogamy since the pollen comes from the same plant. Self-incompatibility is a genetic mechanism that "
    "prevents self-pollen (from the same flower or other flowers of the same plant) from fertilising the ovules by "
    "inhibiting pollen germination or pollen tube growth in the pistil. The pistil's recognition of the pollen, "
    "followed by acceptance or rejection, is the result of a dialogue between pollen and pistil.",
    ["Same plant → geitonogamy → 'self' pollen", "Self-incompatibility rejects self-pollen", "Germination or tube "
     "growth inhibited → no fertilisation"],
    C12_SR("outbreeding devices; pollen-pistil interaction"),
    why="Geitonogamous pollen is genetically self-pollen, so it is rejected at germination or tube growth; NCERT "
        "does not describe rejection at the endosperm stage.",
    seconds=45)

add(SRFP, "Megasporogenesis and embryo sac", "Advanced", "assertion_reason",
    ar("An ovule generally has a single embryo sac.",
       "Ovules generally differentiate a single megaspore mother cell, and in a majority of flowering plants only "
       "one of the four megaspores it forms is functional and develops into the embryo sac."),
    AR("A"),
    "Why one embryo sac per ovule",
    "NCERT: an ovule generally has a single embryo sac formed from a megaspore. Ovules generally differentiate a "
    "single megaspore mother cell; its meiosis gives four megaspores, and in a majority of flowering plants one is "
    "functional while the other three degenerate. Only the functional megaspore develops into the female "
    "gametophyte. One mother cell × one functional megaspore = one embryo sac, so R explains A.",
    ["One MMC per ovule", "Meiosis → 4 megaspores, 1 functional", "1 functional megaspore → 1 embryo sac"],
    C12_SR("pre-fertilisation: megasporogenesis and the female gametophyte"),
    seconds=40)

_haploid = 24 // 2
assert 3 * _haploid == 36 and 2 * _haploid == 24

add(SRFP, "Microsporogenesis and male gametophyte", "Advanced", "statement_pair",
    "A flowering plant has 2n = 24 and sheds its pollen at the 3-celled stage.\n\n" +
    sp("At the time of shedding, one pollen grain contains 36 chromosomes in all, counting all its nuclei.",
       "Before fertilisation, the central cell of a mature embryo sac of this plant contains 36 chromosomes."),
    SP("C"),
    "Counting chromosomes in gametophytes",
    "n = 12. A pollen grain shed at the 3-celled stage has one vegetative cell and two male gametes, i.e. three "
    "haploid nuclei: 3 × 12 = 36 (Statement I true). The central cell of the embryo sac has two haploid polar "
    "nuclei: 2 × 12 = 24 chromosomes before fertilisation. It becomes triploid (36) only after triple fusion "
    "(Statement II false).",
    ["n = 12", "Pollen: 3 haploid nuclei → 36 (true)", "Central cell: 2 polar nuclei → 24, not 36 (false)"],
    C12_SR("pre-fertilisation: pollen grain and female gametophyte"),
    seconds=60, verified_by=RECOMPUTED)

add(SRFP, "Pollination", "Advanced", "multi_statement",
    ms("A plant species has small flowers that are not colourful and produce no nectar. The pollen grains are light, "
       "non-sticky and produced in very large numbers, the stigma is large and feathery, each ovary has a single "
       "ovule, and many flowers are packed into an inflorescence. Which inferences are reasonable on the basis of "
       "NCERT?",
       ["The species is most probably wind-pollinated.",
        "The pollen grains reaching a given stigma is a chance factor, which is why so much pollen is produced.",
        "The species could well be a grass, in which this mode of pollination is quite common.",
        "Nectar-robbing insects are probably its main pollinators.",
        "Its pollen grains are probably protected from wetting by a mucilaginous covering."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["a", "d", "e"], ["b", "c", "d"]], "D"),
    "Recognising a wind-pollinated flower",
    "All the features listed match NCERT's description of wind-pollinated flowers: light, non-sticky pollen; a "
    "large, often feathery stigma; a single ovule in each ovary and numerous flowers packed into an inflorescence; "
    "flowers not very colourful and without nectar (a). Since contact of pollen with the stigma is a chance factor "
    "in wind pollination, the flowers produce an enormous amount of pollen compared with the number of ovules (b). "
    "NCERT notes that wind pollination is quite common in grasses (c). Pollen and nectar robbers do not pollinate, "
    "and this flower has no nectar (d false); a mucilaginous covering is a feature of water-pollinated pollen (e "
    "false).",
    ["Features → wind pollination (a)", "Chance factor → enormous pollen (b)", "Common in grasses (c)",
     "(d) robbers do not pollinate; (e) water-pollination feature"],
    C12_SR("pollination: agents of pollination"),
    why="Options with (d) or (e) attribute insect or water features to a wind-pollinated flower; '(b), (c) and (d)' "
        "also omits the main inference (a).",
    seconds=60)
