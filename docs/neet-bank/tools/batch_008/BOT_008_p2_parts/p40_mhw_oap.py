
# ================================================================ Microbes in Human Welfare (3 / 4 / 3)
C12_MW = lambda s: ref(12, MHW, s)

add(MHW, "Household and industrial products", "Basic", "direct",
    "NCERT points out that microbes are present everywhere. Which of the following places does it name as "
    "habitats where microbes are found?",
    P("Thermal vents (where the temperature may be as high as 100 °C), deep in the soil, under layers of snow and "
      "highly acidic environments",
      ["Only in soil, water and air, never inside the bodies of animals and plants",
       "Only in moderate environments, never above 50 °C or in acidic conditions",
       "Only inside the bodies of animals and plants, never free in nature"], "B"),
    "Microbes are ubiquitous",
    "NCERT: microbes are present everywhere: in soil, water and air, inside our bodies and those of other animals "
    "and plants, and even where no other life form could possibly exist, such as deep inside geysers (thermal "
    "vents) where the temperature may be as high as 100 °C, deep in the soil, under the layers of snow several "
    "metres thick, and in highly acidic environments.",
    ["Everywhere: soil, water, air, inside organisms", "Extreme habitats: thermal vents up to 100 °C, deep soil, "
     "under snow, acidic places"],
    C12_MW("introduction"),
    why="Each wrong option restricts microbes to some habitats, whereas NCERT stresses that they are found "
        "everywhere, including inside bodies and in extreme environments.",
    seconds=25)

add(MHW, "Sewage treatment", "Basic", "direct",
    "In a sewage treatment plant, the secondary treatment, in which the primary effluent is passed into aeration "
    "tanks and microbes consume its organic matter, is also called:",
    P("Biological treatment", ["Physical treatment", "Chemical treatment", "Tertiary treatment"], "D"),
    "Secondary treatment is biological",
    "NCERT: primary treatment involves the physical removal of particles (filtration and sedimentation). Secondary "
    "treatment, or biological treatment, uses the vigorous growth of useful aerobic microbes into flocs in the "
    "aeration tanks; these consume the major part of the organic matter and reduce the BOD of the effluent.",
    ["Primary: physical removal", "Secondary: microbes digest organic matter = biological treatment"],
    C12_MW("microbes in sewage treatment: secondary treatment"),
    why="Physical removal is primary treatment; NCERT does not describe the aeration step as chemical or tertiary "
        "treatment.",
    seconds=20)

add(MHW, "Household and industrial products", "Basic", "statement_pair",
    sp("Microbes such as bacteria and fungi can be grown on nutritive media to form colonies that can be seen with "
       "the naked eye.",
       "Prions, mentioned by NCERT among the diverse microbes, are proteinaceous infectious agents."),
    SP("A"),
    "Diversity and culture of microbes",
    "NCERT: microbes are diverse: protozoa, bacteria, fungi, microscopic plant and animal viruses, viroids and "
    "also prions, which are proteinaceous infectious agents (Statement II true). Microbes like bacteria and many "
    "fungi can be grown on nutritive media to form colonies that can be seen with the naked eye, and such cultures "
    "are useful in studies on micro-organisms (Statement I true).",
    ["Statement I: true", "Statement II: true"],
    C12_MW("introduction"),
    seconds=30)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "assertion_reason",
    ar("Biofertilisers are not yet available commercially in India, so farmers cannot use them in their fields.",
       "Biofertilisers are organisms that enrich the nutrient quality of the soil."),
    AR("D"),
    "Biofertilisers in use",
    "NCERT: biofertilisers are organisms that enrich the nutrient quality of the soil; the main sources are "
    "bacteria, fungi and cyanobacteria (R true). Currently, in our country, a number of biofertilisers are "
    "available commercially in the market, and farmers use these regularly in their fields to replenish soil "
    "nutrients and to reduce dependence on chemical fertilisers. So A is false.",
    ["A: false (commercially available, used regularly)", "R: true (definition)"],
    C12_MW("microbes as biofertilisers"),
    seconds=30)

add(MHW, "Biogas", "Intermediate", "multi_statement",
    ms("Which of the following statements are correct according to NCERT?",
       ["The excreta of cattle, rich in methanogenic bacteria, is used to generate biogas, commonly called gobar "
        "gas.",
        "Rhizobium fixes atmospheric nitrogen in symbiotic association with the root nodules of leguminous plants.",
        "Cyanobacteria are autotrophic microbes widely distributed in aquatic and terrestrial environments.",
        "Methanogens grow aerobically and need constant aeration.",
        "Mycorrhizal fungi such as Glomus fix atmospheric nitrogen for the plant."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "d", "e"], ["a", "c", "d"]], "B"),
    "Microbes in biogas and as biofertilisers",
    "Cattle excreta (gobar), rich in methanogens, is used for biogas, commonly called gobar gas (a). The bacteria "
    "forming nodules on the roots of leguminous plants by symbiotic association are Rhizobium, which fix "
    "atmospheric nitrogen (b). Cyanobacteria are autotrophic microbes widely distributed in aquatic and terrestrial "
    "environments, many of which fix nitrogen (c). Methanogens grow anaerobically (d false). Glomus forms "
    "mycorrhiza and absorbs phosphorus from the soil for the plant; it is not described as fixing nitrogen (e "
    "false).",
    ["(a) gobar gas", "(b) Rhizobium in legume nodules", "(c) cyanobacteria", "(d) anaerobic; (e) phosphorus, not "
     "nitrogen"],
    C12_MW("microbes in production of biogas; microbes as biofertilisers"),
    why="Options with (d) or (e) contain a false statement; '(a), (c) and (d)' also omits (b).",
    seconds=50)

add(MHW, "Sewage treatment", "Intermediate", "statement_pair",
    sp("In primary treatment, all the solids that settle form the primary sludge, and the supernatant forms the "
       "effluent, which is taken for secondary treatment.",
       "Once the BOD has been reduced in the aeration tanks, the effluent is released directly into rivers without "
       "being passed through any settling tank."),
    SP("C"),
    "Sludge and effluent in sewage treatment",
    "NCERT: after filtration and sedimentation in primary treatment, all solids that settle form the primary "
    "sludge, and the supernatant forms the effluent, which goes for secondary treatment (Statement I true). Once "
    "the BOD is reduced significantly, the effluent is passed into a settling tank where the bacterial flocs "
    "sediment as activated sludge; only then is the effluent from secondary treatment released into natural "
    "water bodies (Statement II false).",
    ["Statement I: true", "Settling tank comes before release → Statement II false"],
    C12_MW("microbes in sewage treatment"),
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Intermediate", "match_list",
    ml(("biocontrol agent", "pest or pathogen it controls"),
       ["Ladybird beetle", "Dragonflies", "Bacillus thuringiensis", "Trichoderma"],
       ["Several plant pathogens", "Aphids", "Mosquitoes", "Butterfly caterpillars"]),
    M(mc("II,III,IV,I"), [mc("III,II,IV,I"), mc("II,III,I,IV"), mc("IV,III,II,I")], "D"),
    "Matching biocontrol agents with their targets",
    "NCERT: the ladybird and dragonflies are useful to get rid of aphids and mosquitoes, respectively (A-II, "
    "B-III). Bacillus thuringiensis is used to control butterfly caterpillars (C-IV). Trichoderma species are "
    "free-living fungi that are effective biocontrol agents of several plant pathogens (D-I).",
    ["Ladybird → aphids", "Dragonflies → mosquitoes", "Bt → caterpillars", "Trichoderma → plant pathogens"],
    C12_MW("microbes as biocontrol agents"),
    why="The other codes swap the targets of the ladybird and dragonflies, of Bt and Trichoderma, or of the "
        "ladybird and Bt.",
    seconds=35)

add(MHW, "Biocontrol agents and biofertilisers", "Advanced", "assertion_reason",
    ar("Baculoviruses of the genus Nucleopolyhedrovirus are desirable for biological control in an integrated pest "
       "management programme in which beneficial insects are being conserved.",
       "These viruses are species-specific, narrow-spectrum insecticidal agents with no negative impact on plants, "
       "mammals, birds, fish or even non-target insects."),
    AR("A"),
    "Why baculoviruses suit integrated pest management",
    "NCERT: baculoviruses (mostly genus Nucleopolyhedrovirus) attack insects and other arthropods. They have been "
    "shown to have no negative impacts on plants, mammals, birds, fish or even on non-target insects. This is "
    "especially desirable when beneficial insects are being conserved to aid an overall IPM programme, or when an "
    "ecologically sensitive area is being treated. Their species-specific, narrow-spectrum action is the reason "
    "for A.",
    ["Species-specific, narrow-spectrum", "Spares non-target and beneficial insects", "Hence suitable for IPM"],
    C12_MW("microbes as biocontrol agents"),
    seconds=40)

add(MHW, "Household and industrial products", "Advanced", "multi_statement",
    ms("Which of the following statements about microbes in household and industrial products are correct?",
       ["Both the large holes in Swiss cheese and the puffed-up appearance of dosa and idli dough result from "
        "carbon dioxide produced by microbes.",
        "Whisky is produced by distillation of the fermented broth, whereas wine is produced without distillation.",
        "Lactic acid bacteria convert milk to curd and also increase its vitamin B₁₂ content.",
        "Roquefort cheese is ripened by growing a specific bacterium on it.",
        "Citric acid is produced commercially by the bacterium Acetobacter aceti."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "B"),
    "Microbes in food and industry",
    "Propionibacterium sharmanii produces a large amount of CO₂ that makes the holes in Swiss cheese, and the "
    "dough for dosa and idli puffs up due to CO₂ produced by bacteria (a). Wine and beer are produced without "
    "distillation, whereas whisky, brandy and rum are produced by distillation of the fermented broth (b). LAB "
    "convert milk to curd and improve its nutritional quality by increasing vitamin B₁₂ (c). Roquefort cheese is "
    "ripened by a specific fungus (d false), and citric acid comes from the fungus Aspergillus niger, while "
    "Acetobacter aceti makes acetic acid (e false).",
    ["(a) CO₂ in both", "(b) distilled vs not", "(c) LAB and B₁₂", "(d) fungus; (e) Aspergillus niger"],
    C12_MW("microbes in household products; microbes in industrial products"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (d)' also omits (a).",
    seconds=55)

add(MHW, "Household and industrial products", "Advanced", "direct",
    "Which pair of products are both obtained from bacteria, according to NCERT?",
    P("Streptokinase and butyric acid",
      ["Cyclosporin A and citric acid", "Statins and ethanol", "Penicillin and statins"], "D"),
    "Bacterial, fungal and yeast products",
    "Streptokinase is produced by the bacterium Streptococcus, and butyric acid by the bacterium Clostridium "
    "butylicum. Cyclosporin A comes from the fungus Trichoderma polysporum and citric acid from the fungus "
    "Aspergillus niger; statins come from the yeast Monascus purpureus and ethanol is produced commercially using "
    "the yeast Saccharomyces cerevisiae; penicillin comes from the mould Penicillium notatum.",
    ["Streptokinase: Streptococcus (bacterium)", "Butyric acid: Clostridium butylicum (bacterium)",
     "Others: fungi or yeasts"],
    C12_MW("microbes in industrial products"),
    why="Each of the other pairs contains products of fungi or yeasts only.",
    seconds=40)

# ================================================================ Organisms and Populations (4 / 6 / 4)
C12_OP = lambda s: ref(12, OAP, s)

add(OAP, "Population growth", "Basic", "direct",
    "According to NCERT, populations evolve to maximise their reproductive fitness, also called Darwinian fitness, "
    "in the habitat in which they live. Such fitness is indicated by:",
    P("A high value of r, the intrinsic rate of natural increase",
      ["A high carrying capacity K of the habitat", "A high death rate", "A large body size of the individuals"],
      "B"),
    "Darwinian fitness and r",
    "NCERT (life history variation): populations evolve to maximise their reproductive fitness, also called "
    "Darwinian fitness (high r value), in the habitat in which they live. r is the intrinsic rate of natural "
    "increase, the parameter NCERT also uses to assess the impact of any factor on population growth.",
    ["Reproductive (Darwinian) fitness", "Measured as high r"],
    C12_OP("populations: life history variation"),
    why="K is a property of the habitat, a high death rate lowers r, and NCERT does not equate fitness with body "
        "size.",
    seconds=25)

add(OAP, "Population interactions", "Basic", "assertion_reason",
    ar("In amensalism, both interacting species benefit.",
       "In commensalism, one species benefits and the other is neither harmed nor benefited."),
    AR("D"),
    "Amensalism and commensalism",
    "NCERT: in amensalism one species is harmed whereas the other is unaffected; it is not an interaction in "
    "which both benefit (that is mutualism), so A is false. Commensalism is the interaction in which one species "
    "benefits and the other is neither harmed nor benefited, as with an orchid growing as an epiphyte on a mango "
    "branch (R true).",
    ["Amensalism: (−, 0) → A false", "Commensalism: (+, 0) → R true"],
    C12_OP("populations: population interactions"),
    seconds=25)

add(OAP, "Population attributes", "Basic", "match_list",
    ml(("term", "meaning"),
       ["Carrying capacity (K)", "Intrinsic rate of natural increase (r)", "Age pyramid", "Population density"],
       ["Per capita birth rate minus per capita death rate (b − d)", "Size of a population per unit area, as "
        "numbers, biomass or per cent cover", "Maximum number of individuals that the habitat can support",
        "Plot of the age distribution of a population"]),
    M(mc("III,I,IV,II"), [mc("I,III,IV,II"), mc("III,I,II,IV"), mc("III,IV,I,II")], "C"),
    "Basic terms of population ecology",
    "Carrying capacity K is the limit beyond which no further growth is possible, the maximum the habitat's "
    "resources can support (A-III). In dN/dt = (b − d)N, r = b − d is the intrinsic rate of natural increase "
    "(B-I). Plotting the per cent of individuals in each age group gives the age pyramid (C-IV). Population "
    "density is population size per unit area, measured as numbers, biomass or per cent cover (D-II).",
    ["A → III", "B → I", "C → IV", "D → II"],
    C12_OP("populations: population attributes; population growth"),
    why="The other codes swap K with r, the age pyramid with density, or r with the age pyramid.",
    seconds=30)

add(OAP, "Population growth", "Basic", "statement_pair",
    sp("Some organisms breed only once in their lifetime, such as Pacific salmon fish and bamboo, while others "
       "breed many times during their lifetime, such as most birds and mammals.",
       "Some organisms produce a large number of small-sized offspring, such as oysters and pelagic fishes, while "
       "others produce a small number of large-sized offspring, such as birds and mammals."),
    SP("A"),
    "Life history variation",
    "NCERT: under a particular set of selection pressures, organisms evolve towards the most efficient "
    "reproductive strategy. Some breed only once in their lifetime (Pacific salmon fish, bamboo), while others "
    "breed many times (most birds and mammals) (Statement I true). Some produce a large number of small-sized "
    "offspring (oysters, pelagic fishes), while others produce a small number of large-sized offspring (birds, "
    "mammals) (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_OP("populations: life history variation"),
    seconds=30)

add(OAP, "Population growth", "Intermediate", "assertion_reason",
    ar("A population growing in a habitat with limited resources shows a deceleration phase as its density "
       "approaches the carrying capacity.",
       "In the logistic equation dN/dt = rN[(K − N)/K], the factor (K − N)/K becomes smaller as N increases, "
       "lowering the growth rate per individual."),
    AR("A"),
    "Why logistic growth decelerates",
    "In logistic growth the per capita growth rate is r(K − N)/K. As N rises towards K, (K − N)/K falls towards "
    "zero, so each individual contributes less and less to growth: the curve passes from acceleration into "
    "deceleration and finally reaches an asymptote at K. R is the mathematical reason for A.",
    ["Per capita rate = r(K − N)/K", "Falls as N → K", "Deceleration, then asymptote"],
    C12_OP("populations: population growth (logistic growth)"),
    seconds=40)

_r, _K = F(2, 5), 2000
_rate = lambda n: _r * n * F(_K - n, _K)
assert max(range(0, _K + 1), key=_rate) == 1000 and _rate(1000) == 200

add(OAP, "Population growth", "Intermediate", "numerical",
    "A population grows according to the logistic model, dN/dt = rN[(K − N)/K], with r = 0.4 per year and "
    "K = 2000. At what population size is the growth rate dN/dt the highest, and what is that rate?",
    P("At N = 1000; 200 individuals per year",
      ["At N = 2000; 800 individuals per year", "At N = 1000; 400 individuals per year",
       "At N = 500; 150 individuals per year"], "D"),
    "Maximum growth rate in logistic growth",
    "dN/dt = rN(K − N)/K is a product that is largest when N = K/2 (the middle of the S-shaped curve). Here "
    "N = 2000/2 = 1000, and dN/dt = 0.4 × 1000 × (2000 − 1000)/2000 = 0.4 × 1000 × 0.5 = 200 individuals per "
    "year (the maximum, rK/4).",
    ["Maximum at N = K/2 = 1000", "dN/dt = 0.4 × 1000 × 0.5 = 200"],
    C12_OP("populations: population growth (logistic growth)"),
    why="At N = K growth is zero, not maximum; 400 forgets the (K − N)/K factor; at N = 500 the rate is "
        "0.4 × 500 × 0.75 = 150, which is less than 200.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population growth", "Intermediate", "multi_statement",
    ms("Which of the following statements about life history variation are correct according to NCERT?",
       ["Under a particular set of selection pressures, organisms evolve towards the most efficient reproductive "
        "strategy.",
        "Ecologists suggest that life history traits of organisms have evolved in relation to the constraints "
        "imposed by the abiotic and biotic components of the habitat.",
        "All populations have the same intrinsic rate of natural increase.",
        "The number and size of offspring are the same in all species.",
        "Life history traits do not depend in any way on the habitat."]),
    MS(["a", "b"], [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
    "Evolution of reproductive strategies",
    "NCERT: populations evolve to maximise reproductive fitness in their habitat; under a particular set of "
    "selection pressures, organisms evolve towards the most efficient reproductive strategy (a), and ecologists "
    "suggest that life history traits have evolved in relation to the constraints imposed by the abiotic and "
    "biotic components of the habitat (b). NCERT's r values differ widely (0.12 for the flour beetle, 0.015 for "
    "the Norway rat) (c false); species differ in the number and size of their offspring (d false); and life "
    "history traits are shaped by the habitat (e false).",
    ["(a), (b): NCERT statements", "(c), (d), (e) contradict NCERT"],
    C12_OP("populations: life history variation"),
    why="Every other option includes at least one false statement.",
    seconds=45)

add(OAP, "Population growth", "Intermediate", "direct",
    "For a population growing exponentially (dN/dt = rN) with a constant r, what is the shape of the graph of the "
    "growth rate dN/dt plotted against population size N?",
    P("A straight line through the origin, with slope r",
      ["A horizontal straight line, since dN/dt stays constant", "A bell-shaped curve with its peak at N = K/2",
       "An S-shaped curve that levels off at K"], "C"),
    "Growth rate in exponential growth",
    "In dN/dt = rN, dN/dt is directly proportional to N with constant r, so the graph of dN/dt against N is a "
    "straight line through the origin with slope r: the bigger the population, the faster it grows (this is why "
    "N plotted against time gives a J-shaped curve). A hump-shaped dN/dt with a peak at K/2 belongs to logistic "
    "growth, and the S-shaped curve is N against time in logistic growth.",
    ["dN/dt = rN → proportional to N", "Straight line through origin, slope r", "N vs time → J-shaped"],
    C12_OP("populations: population growth (exponential growth)"),
    why="dN/dt is not constant (it rises with N); the peak at K/2 and the S-shape belong to logistic growth.",
    seconds=45)

add(OAP, "Population interactions", "Intermediate", "statement_pair",
    sp("When certain exotic species are introduced into a geographical area, they may become invasive and spread "
       "fast, because the invaded land does not have their natural predators.",
       "Predators always drive their prey species to extinction."),
    SP("C"),
    "Predators and population regulation",
    "NCERT: one reason why certain exotic species become invasive and spread fast when introduced into a "
    "geographical area is that the invaded land does not have their natural predators, as with the prickly pear "
    "cactus in Australia (Statement I true). Predators in nature are 'prudent': a predator that overexploits its "
    "prey might itself become extinct for lack of food, and predators keep prey populations under control rather "
    "than eliminating them (Statement II false).",
    ["Statement I: true", "Prudent predators; prey kept under control → Statement II false"],
    C12_OP("populations: population interactions (predation)"),
    seconds=35)

add(OAP, "Population interactions", "Intermediate", "multi_statement",
    ms("Which of the following statements about plant defences against herbivores are correct?",
       ["Thorns, as in Acacia and cactus, are the most common morphological means of defence.",
        "Many plants produce and store chemicals that make the herbivore sick when eaten, inhibit feeding or "
        "digestion, disrupt its reproduction or even kill it.",
        "Nicotine, caffeine, quinine, strychnine and opium are produced by plants as defences against grazers and "
        "browsers.",
        "Plants produce these chemicals mainly to attract herbivores.",
        "Calotropis is heavily browsed by cattle and goats."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "A"),
    "Morphological and chemical defences of plants",
    "NCERT: since plants cannot run away, they have evolved morphological and chemical defences. Thorns (Acacia, "
    "cactus) are the most common morphological means of defence (a). Many plants produce and store chemicals that "
    "make the herbivore sick, inhibit feeding or digestion, disrupt reproduction or kill it (b); nicotine, "
    "caffeine, quinine, strychnine and opium are such defences (c). These chemicals deter rather than attract "
    "herbivores (d false), and Calotropis produces highly poisonous cardiac glycosides, so cattle and goats never "
    "browse on it (e false).",
    ["(a) thorns", "(b) defence chemicals", "(c) named chemicals", "(d), (e) false"],
    C12_OP("populations: population interactions (predation)"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (d)' also omits (a).",
    seconds=45)

_rr, _KK = F(1, 5), 1000
_vals = [_rr * 400, _rr * 400 * F(_KK - 400, _KK), _rr * 900 * F(_KK - 900, _KK), _rr * 1000 * 0]
assert _vals == [80, 48, 18, 0]

add(OAP, "Population growth", "Advanced", "match_list",
    "For a population with r = 0.2 per year, compare the exponential model dN/dt = rN with the logistic model "
    "dN/dt = rN[(K − N)/K], taking K = 1000.\n\n" +
    ml(("model and population size", "growth rate (individuals per year)"),
       ["Exponential, N = 400", "Logistic, N = 400", "Logistic, N = 900", "Logistic, N = 1000"],
       ["0", "18", "48", "80"]),
    M(mc("IV,III,II,I"), [mc("III,IV,II,I"), mc("IV,II,III,I"), mc("IV,III,I,II")], "D"),
    "Exponential and logistic growth rates compared",
    "Exponential: 0.2 × 400 = 80 (A-IV). Logistic at 400: 0.2 × 400 × 600/1000 = 48 (B-III). Logistic at 900: "
    "0.2 × 900 × 100/1000 = 18 (C-II). At N = K = 1000: 0.2 × 1000 × 0 = 0; the population has reached its "
    "asymptote (D-I).",
    ["Exponential: rN", "Logistic: rN(K − N)/K", "A-IV, B-III, C-II, D-I"],
    C12_OP("populations: population growth"),
    why="The other codes swap the exponential and logistic values at N = 400, or the logistic values at 900 and "
        "1000.",
    seconds=70, verified_by=RECOMPUTED)

add(OAP, "Population attributes", "Advanced", "multi_statement",
    "The age structure of three populations is: P: pre-reproductive 45 per cent, reproductive 40 per cent, "
    "post-reproductive 15 per cent; Q: 35, 36 and 29 per cent; R: 15, 45 and 40 per cent.\n\n" +
    ms("Which of the following inferences are correct?",
       ["The age pyramid of P has a broad base and indicates an expanding population.",
        "The age pyramid of R is urn-shaped and indicates a declining population.",
        "The age pyramid of Q is bell-shaped and indicates a stable population.",
        "Population P is declining, since its post-reproductive group is the smallest.",
        "Population R has the broadest base of the three pyramids."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
    "Reading age pyramids",
    "The shape of the age pyramid reflects the growth status of a population. P has more pre-reproductive than "
    "reproductive individuals: broad base, expanding (a). R has far fewer pre-reproductive than reproductive "
    "individuals: narrow base, urn-shaped, declining (b). In Q the pre-reproductive and reproductive groups are "
    "nearly equal: bell-shaped, stable (c). A small post-reproductive group does not make P decline (d false), "
    "and R has the narrowest, not the broadest, base (e false).",
    ["P: 45 > 40 → expanding", "Q: 35 ≈ 36 → stable", "R: 15 < 45 → declining"],
    C12_OP("populations: population attributes (age pyramids)"),
    why="(d) judges growth from the post-reproductive group; (e) reverses the base widths.",
    seconds=60)

assert abs(math.log(2) / 0.02 - 34.66) < 0.01

add(OAP, "Population growth", "Advanced", "direct",
    "Two populations of the same species grow exponentially with the same r = 0.02 per year: one starts with 100 "
    "individuals and the other with 10,000. Which statement about the time each takes to double is correct? "
    "(Nₜ = N₀e^(rt); ln 2 = 0.693)",
    P("Both take the same time, about 35 years, because the doubling time depends only on r",
      ["The smaller population doubles 100 times faster", "The larger population doubles 100 times faster",
       "The doubling times cannot be compared without knowing the carrying capacity"], "D"),
    "Doubling time in exponential growth",
    "Doubling means Nₜ = 2N₀: 2N₀ = N₀e^(rt), so e^(rt) = 2 and t = ln 2/r = 0.693/0.02 ≈ 34.7 years. N₀ "
    "cancels: under exponential growth, every population with the same r doubles in the same time, whatever its "
    "starting size, although the larger population adds far more individuals in that time.",
    ["2N₀ = N₀e^(rt) → t = ln 2/r", "N₀ cancels", "t = 0.693/0.02 ≈ 35 years for both"],
    C12_OP("populations: population growth (exponential growth)"),
    why="Starting size does not affect the doubling time in the exponential model, and K does not appear in it.",
    seconds=60, verified_by=RECOMPUTED)

add(OAP, "Population interactions", "Advanced", "multi_statement",
    "Write the effect of an interaction on each partner as + (benefit), − (harm) or 0 (no effect).\n\n" +
    ms("Which of the following pairings are correct?",
       ["Fig and its pollinating wasp: (+, +)",
        "Cattle egret and grazing cattle: (+, 0)",
        "Orchid growing as an epiphyte and the mango branch it grows on: (+, 0)",
        "Cuscuta and the hedge plant on which it grows: (+, 0)",
        "Clown fish and the sea anemone among whose tentacles it lives: (+, +)"]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "A"),
    "Classifying interactions by their effects",
    "Fig and wasp: the wasp pollinates the fig while using its fruit for egg laying and larval food; both "
    "benefit, mutualism (a). Cattle egrets catch insects stirred up by cattle, which are not affected: "
    "commensalism (b). The epiphytic orchid benefits while the mango tree gets no benefit or harm: commensalism "
    "(c). Cuscuta is a parasite deriving nutrition from the host, so the host is harmed: (+, −) (d false). The "
    "clown fish gets protection, and the sea anemone does not appear to derive any benefit: (+, 0), not (+, +) "
    "(e false).",
    ["Mutualism (+, +)", "Commensalism (+, 0)", "Parasitism (+, −)"],
    C12_OP("populations: population interactions"),
    why="Options with (d) or (e) mislabel parasitism or commensalism; '(b), (c) and (d)' also omits (a).",
    seconds=50)
