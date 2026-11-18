
# ================================================================ Ecosystem (4 / 5 / 4)
C12_EC = lambda s: ref(12, ECO, s)

add(ECO, "Structure and components", "Basic", "multi_statement",
    ms("NCERT lists the important components of the functional aspects of an ecosystem, with a pond as its "
       "example. Which of the following are among them?",
       ["Productivity", "Decomposition", "Energy flow", "Stratification", "Species composition"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["c", "d", "e"], ["a", "d", "e"]], "B"),
    "Structural and functional aspects of an ecosystem",
    "NCERT: the important components of an ecosystem's function are (i) productivity, (ii) decomposition, "
    "(iii) energy flow and (iv) nutrient cycling. Species composition (identification and enumeration of species) "
    "and stratification (vertical distribution of species at different levels) are features of an ecosystem's "
    "structure.",
    ["Functions: productivity, decomposition, energy flow, nutrient cycling", "Structure: species composition, "
     "stratification"],
    C12_EC("ecosystem: structure and function"),
    why="Stratification and species composition describe structure, not function, so options with (d) or (e) are "
        "wrong.",
    seconds=30)

add(ECO, "Structure and components", "Basic", "direct",
    "According to NCERT, the autotrophic components of a pond ecosystem include:",
    P("Phytoplankton, some algae, and the floating, submerged and marginal plants found at the edges",
      ["Zooplankton and the free-swimming and bottom-dwelling animals", "Fungi, bacteria and flagellates at the "
       "bottom of the pond", "Only the rooted plants at the edges; phytoplankton are consumers"], "B"),
    "Producers of a pond",
    "NCERT describes the pond: the abiotic component is the water with dissolved inorganic and organic substances "
    "and the rich soil deposit at the bottom; the autotrophic components include the phytoplankton, some algae and "
    "the floating, submerged and marginal plants found at the edges; the consumers are zooplankton and the "
    "free-swimming and bottom-dwelling forms; and the decomposers are fungi, bacteria and flagellates, especially "
    "abundant at the bottom.",
    ["Autotrophs: phytoplankton, algae, floating, submerged and marginal plants", "Consumers: zooplankton and "
     "animals", "Decomposers: fungi, bacteria, flagellates"],
    C12_EC("ecosystem: structure and function (pond)"),
    why="Zooplankton and animals are consumers; fungi, bacteria and flagellates are decomposers; phytoplankton "
        "are producers.",
    seconds=25)

add(ECO, "Ecological pyramids", "Basic", "statement_pair",
    sp("NCERT's ideal pyramid of energy shows that primary producers convert only about 1 per cent of the energy "
       "in the sunlight available to them into net primary productivity.",
       "In an energy pyramid, the energy at a lower trophic level is always more than at a higher level."),
    SP("A"),
    "The ideal pyramid of energy",
    "NCERT's figure of an ideal pyramid of energy notes that primary producers convert only 1 per cent of the "
    "energy in the sunlight available to them into NPP (Statement I true). The pyramid of energy is always "
    "upright: energy at a lower trophic level is always more than at a higher level, because some energy is lost "
    "as heat at each step (Statement II true).",
    ["Statement I: true (1 per cent into NPP)", "Statement II: true (always upright)"],
    C12_EC("ecological pyramids"),
    seconds=30)

add(ECO, "Productivity and decomposition", "Basic", "assertion_reason",
    ar("Decomposers are heterotrophic organisms.",
       "Decomposers make their own food by photosynthesis."),
    AR("C"),
    "Decomposers are heterotrophs",
    "NCERT: decomposers are heterotrophic organisms, mainly fungi and bacteria, which meet their energy and "
    "nutrient requirements by degrading dead organic matter (detritus); they are also called saprotrophs. A is "
    "true. They do not photosynthesise, so R is false.",
    ["A: true", "Energy from dead organic matter, not photosynthesis → R false"],
    C12_EC("energy flow: detritus food chain"),
    seconds=25)

_npp_year = (4 - 4 * F(25, 100)) * 365
assert _npp_year == 1095

add(ECO, "Productivity and decomposition", "Intermediate", "numerical",
    "The gross primary productivity of a grassland averages 4 g m⁻² day⁻¹ (dry weight), and the plants use 25 per "
    "cent of it in respiration. Taking a year as 365 days, what is the net primary productivity of the grassland in "
    "g m⁻² yr⁻¹?",
    P("1,095", ["1,460", "365", "3"], "B"),
    "Net primary productivity and its units",
    "NPP = GPP − R = 4 − (0.25 × 4) = 3 g m⁻² day⁻¹. NCERT expresses productivity per unit area per year, so "
    "3 × 365 = 1,095 g m⁻² yr⁻¹.",
    ["R = 25% of 4 = 1 g m⁻² day⁻¹", "NPP = 3 g m⁻² day⁻¹", "× 365 = 1,095 g m⁻² yr⁻¹"],
    C12_EC("productivity"),
    why="1,460 is the annual GPP (respiration not subtracted); 365 is the annual respiration loss; 3 is the daily "
        "NPP, not the yearly value.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Intermediate", "direct",
    "In cold, waterlogged bogs, partly decomposed plant remains accumulate over many years. Which explanation "
    "fits NCERT's account of decomposition?",
    P("Low temperature and anaerobiosis inhibit decomposition, resulting in a build-up of organic materials",
      ["Water-soluble nutrients are leached away, so decomposers have nothing to act on",
       "Cold, wet conditions speed up humification and mineralisation",
       "Detritivores multiply rapidly in waterlogged soil and convert all detritus into humus at once"], "D"),
    "Climatic control of decomposition",
    "NCERT: decomposition is largely an oxygen-requiring process, and its rate is controlled by the chemical "
    "composition of the detritus and by climatic factors. Warm and moist environments favour decomposition, "
    "whereas low temperature and anaerobiosis inhibit it, resulting in the build-up of organic materials. A cold, "
    "waterlogged bog combines both inhibiting conditions.",
    ["Decomposition needs oxygen and warmth", "Bog: cold + anaerobic", "Decomposition inhibited → organic matter "
     "builds up"],
    C12_EC("decomposition"),
    why="Leaching removes only soluble nutrients, not the detritus; cold, wet, anoxic conditions slow, not speed, "
        "decomposition; and detritivores do not thrive under anaerobiosis.",
    seconds=40)

add(ECO, "Energy flow", "Intermediate", "multi_statement",
    "In a lake, phytoplankton are eaten by zooplankton and by molluscs; small fish eat zooplankton; large fish eat "
    "small fish and molluscs; and kingfishers eat small fish and large fish. Take producers as the first trophic "
    "level.\n\n" +
    ms("Which of the following statements are correct?",
       ["The molluscs are herbivores (primary consumers).",
        "The large fish occupies the third and the fourth trophic levels.",
        "The kingfisher occupies the fourth and the fifth trophic levels.",
        "The small fish is a primary consumer.",
        "The zooplankton are producers."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Trophic levels in a food web",
    "Phytoplankton (1) → molluscs and zooplankton (2): both are primary consumers; NCERT names molluscs as the "
    "common herbivores of aquatic ecosystems (a). Small fish eat zooplankton: level 3, a secondary consumer (d "
    "false). Large fish eat molluscs (level 3) and small fish (level 4) (b). Kingfishers eat small fish (level 4) "
    "and large fish (levels 4 and 5) (c). Zooplankton are consumers (e false).",
    ["Molluscs, zooplankton: level 2", "Small fish: level 3", "Large fish: 3 and 4", "Kingfisher: 4 and 5"],
    C12_EC("energy flow: food chains and food web"),
    why="Options with (d) or (e) contain a false statement; '(b), (c) and (e)' also omits (a).",
    seconds=70)

add(ECO, "Productivity and decomposition", "Intermediate", "statement_pair",
    sp("Identical leaf litter can decompose at different rates in two regions, because decomposition is controlled "
       "by climatic factors such as temperature and soil moisture.",
       "Humus is decomposed rapidly by microbes, so it cannot serve as a reservoir of nutrients."),
    SP("C"),
    "Rate of decomposition and humus",
    "NCERT: the rate of decomposition is controlled by the chemical composition of the detritus and by climatic "
    "factors; temperature and soil moisture are the most important climatic factors (Statement I true). Humus is "
    "highly resistant to microbial action and undergoes decomposition at an extremely slow rate; being colloidal, "
    "it serves as a reservoir of nutrients (Statement II false).",
    ["Statement I: true", "Humus: extremely slow decomposition, nutrient reservoir → Statement II false"],
    C12_EC("decomposition"),
    seconds=35)

_pc, _tc = 708_000, 3
assert round(_pc / _tc) == 236_000

add(ECO, "Ecological pyramids", "Intermediate", "direct",
    "In a grassland, the counts per unit area are: primary producers 58,42,000; primary consumers 7,08,000; "
    "secondary consumers 3,54,000; tertiary consumers 3. About how many primary consumers are there for each "
    "tertiary consumer, and what is the shape of this pyramid of numbers?",
    P("About 2.4 lakh; upright", ["About 2; upright", "About 2.4 lakh; inverted", "About 19 lakh; inverted"], "B"),
    "Reading a pyramid of numbers",
    "Primary consumers per tertiary consumer = 7,08,000/3 = 2,36,000 ≈ 2.4 lakh. The numbers fall at each higher "
    "trophic level (58,42,000 > 7,08,000 > 3,54,000 > 3), with producers forming the broad base and top "
    "carnivores the apex, so the pyramid is upright.",
    ["7,08,000 ÷ 3 ≈ 2,36,000", "Numbers decrease upward → upright"],
    C12_EC("ecological pyramids"),
    why="2 is the ratio of primary to secondary consumers; the pyramid is not inverted, since every level has fewer "
        "individuals than the one below; 19 lakh divides the producers by 3.",
    seconds=45, verified_by=RECOMPUTED)

_e = [50_000]
for _eff in (F(10, 100), F(15, 100), F(20, 100)):
    _e.append(_e[-1] * _eff)
assert _e == [50_000, 5_000, 750, 150] and _e[0] - _e[1] == 45_000

add(ECO, "Energy flow", "Advanced", "match_list",
    "In a grazing food chain, the producers fix 50,000 kJ. The herbivores obtain 10 per cent of the producers' "
    "energy, the primary carnivores 15 per cent of the herbivores' energy, and the secondary carnivores 20 per "
    "cent of the primary carnivores' energy.\n\n" +
    ml(("quantity", "energy (kJ)"),
       ["Energy obtained by the herbivores", "Energy obtained by the primary carnivores",
        "Energy obtained by the secondary carnivores", "Energy of the producers not passed on to the herbivores"],
       ["150", "750", "5,000", "45,000"]),
    M(mc("III,II,I,IV"), [mc("III,I,II,IV"), mc("IV,II,I,III"), mc("III,II,IV,I")], "B"),
    "Energy transfer with different efficiencies",
    "Herbivores: 10% of 50,000 = 5,000 kJ (A-III). Primary carnivores: 15% of 5,000 = 750 kJ (B-II). Secondary "
    "carnivores: 20% of 750 = 150 kJ (C-I). Energy not passed to herbivores: 50,000 − 5,000 = 45,000 kJ, lost in "
    "respiration as heat or passed to the detritus food chain (D-IV).",
    ["5,000", "750", "150", "45,000"],
    C12_EC("energy flow"),
    why="The other codes swap the carnivore values, or the herbivore energy with the energy not passed on.",
    seconds=70, verified_by=RECOMPUTED)

add(ECO, "Productivity and decomposition", "Advanced", "multi_statement",
    ms("Which of the following predictions about decomposition are correct according to NCERT?",
       ["Identical nitrogen-rich litter decomposes faster in a warm, moist plot than in a cold plot.",
        "In waterlogged soil with anaerobic conditions, organic matter tends to build up.",
        "Leaching can carry water-soluble inorganic nutrients down into the soil horizon, where they precipitate "
        "as unavailable salts.",
        "Earthworms carry out the catabolism of detritus by secreting enzymes that convert it into simple inorganic "
        "substances.",
        "Detritus rich in lignin decomposes faster than detritus rich in water-soluble sugars."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
    "Applying the controls of decomposition",
    "Warm, moist conditions favour decomposition (a); low temperature and anaerobiosis inhibit it, so organic "
    "matter builds up (b). In leaching, water-soluble inorganic nutrients go down into the soil horizon and get "
    "precipitated as unavailable salts (c). Earthworms are detritivores that fragment detritus; catabolism is the "
    "enzymatic degradation by bacteria and fungi (d false). Lignin- and chitin-rich detritus decomposes slowly, "
    "while nitrogen- and sugar-rich detritus decomposes quickly (e false).",
    ["(a), (b) climate", "(c) leaching", "(d) fragmentation, not catabolism", "(e) lignin is slow"],
    C12_EC("decomposition"),
    why="Options with (d) or (e) contain a false statement.",
    seconds=50)

_e2 = 10**6 * F(1, 100) * F(1, 10) * F(1, 10)
assert _e2 == 100

add(ECO, "Energy flow", "Advanced", "direct",
    "The sunlight available to the producers of an ecosystem is 10⁶ J. Assume that the producers convert 1 per "
    "cent of it into net primary productivity and that 10 per cent of the energy passes from each trophic level to "
    "the next. How much energy reaches the primary carnivores?",
    P("100 J", ["1,000 J", "10,000 J", "10 J"], "C"),
    "From sunlight to carnivores",
    "NPP = 1% of 10⁶ J = 10⁴ J. Herbivores (second trophic level) get 10% of this = 10³ J. Primary carnivores "
    "(third trophic level) get 10% of that = 100 J.",
    ["NPP = 10⁶ × 0.01 = 10,000 J", "Herbivores = 1,000 J", "Primary carnivores = 100 J"],
    C12_EC("energy flow; ecological pyramids"),
    why="10,000 J is the NPP, 1,000 J reaches the herbivores, and 10 J would be the secondary carnivores' share.",
    seconds=50, verified_by=RECOMPUTED)

add(ECO, "Ecological pyramids", "Advanced", "statement_pair",
    sp("In a sea, the pyramid of biomass is generally inverted, while the pyramid of energy is upright.",
       "This shows that the 10 per cent law of energy transfer does not apply in the sea."),
    SP("C"),
    "Inverted biomass but upright energy",
    "NCERT: the pyramid of biomass in a sea is generally inverted because the biomass of fishes far exceeds that "
    "of phytoplankton, but the pyramid of energy is always upright, because some energy is always lost as heat at "
    "each step (Statement I true). The upright energy pyramid of the sea shows that energy still decreases at each "
    "trophic level; the inverted biomass pyramid concerns standing crop at one time, not energy flow, so it gives "
    "no reason to reject the 10 per cent law (Statement II false).",
    ["Statement I: true", "Energy still decreases upward → Statement II false"],
    C12_EC("ecological pyramids"),
    seconds=45)

# ================================================================ Biodiversity and Conservation (4 / 5 / 4)
C12_BD = lambda s: ref(12, BDC, s)

add(BDC, "Hotspots and Red Data Book", "Basic", "direct",
    "India's regions of exceptionally high biodiversity are covered by three of the world's biodiversity hotspots. "
    "Which option names them?",
    P("Western Ghats and Sri Lanka, Indo-Burma, and Himalaya",
      ["Western Ghats and Sri Lanka, Eastern Ghats, and Himalaya", "Indo-Burma, Thar Desert, and Sundarbans",
       "Himalaya, Eastern Ghats, and Andaman Islands"], "A"),
    "Hotspots covering India",
    "NCERT: three hotspots, Western Ghats and Sri Lanka, Indo-Burma and Himalaya, cover our country's "
    "exceptionally high biodiversity regions. Hotspots are regions with very high levels of species richness and "
    "a high degree of endemism.",
    ["Western Ghats and Sri Lanka", "Indo-Burma", "Himalaya"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity (hotspots)"),
    why="The Eastern Ghats, Thar Desert, Sundarbans and Andaman Islands are not among the three hotspots NCERT "
        "lists for India.",
    seconds=25)

add(BDC, "Patterns of biodiversity", "Basic", "statement_pair",
    sp("For many taxonomic groups, species inventories are more complete in temperate than in tropical countries.",
       "An overwhelmingly large proportion of the species waiting to be discovered are in the tropics."),
    SP("A"),
    "Where species remain to be discovered",
    "NCERT: there are two kinds of estimates of species numbers: those already described and an estimate of the "
    "total. For many taxonomic groups, species inventories are more complete in temperate than in tropical "
    "countries (Statement I true), and an overwhelmingly large proportion of the species waiting to be discovered "
    "are in the tropics (Statement II true).",
    ["Statement I: true", "Statement II: true"],
    C12_BD("biodiversity: how many species are there on earth"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Basic", "direct",
    "According to NCERT, some extreme estimates of the total number of species on earth range from:",
    P("20 to 50 million", ["2 to 5 million", "1.5 to 2 million", "200 to 500 million"], "D"),
    "Estimates of global species diversity",
    "NCERT: some extreme estimates range from 20 to 50 million, but a more conservative and scientifically sound "
    "estimate made by Robert May places global species diversity at about 7 million. The number of species "
    "already described is slightly more than 1.5 million (IUCN, 2004).",
    ["Extreme estimates: 20–50 million", "May's estimate: about 7 million", "Described: about 1.5 million"],
    C12_BD("biodiversity: how many species are there on earth"),
    why="1.5–2 million is near the number already described; 2–5 million is below May's estimate; 200–500 million "
        "is a factor-of-ten slip.",
    seconds=25)

add(BDC, "Importance and loss", "Basic", "assertion_reason",
    ar("Nations endowed with rich biodiversity can expect to reap enormous benefits.",
       "With increasing resources put into bioprospecting, the molecular, genetic and species-level diversity is "
       "being explored for products of economic importance."),
    AR("A"),
    "Bioprospecting and the narrowly utilitarian argument",
    "NCERT (narrowly utilitarian argument): bioprospecting is exploring molecular, genetic and species-level "
    "diversity for products of economic importance. With increasing resources put into bioprospecting, nations "
    "endowed with rich biodiversity can expect to reap enormous benefits. The benefits arise because the diversity "
    "is being explored for valuable products, so R explains A.",
    ["Bioprospecting explores diversity for products", "More diversity → more potential products", "R explains "
     "A"],
    C12_BD("biodiversity conservation: why should we conserve biodiversity"),
    seconds=30)

add(BDC, "Patterns of biodiversity", "Intermediate", "direct",
    "Robert May's estimate of global species diversity rests on a method described in NCERT. Biologists:",
    P("Make a statistical comparison of the temperate–tropical species richness of an exhaustively studied group "
      "of insects and extrapolate this ratio to other groups of animals and plants",
      ["Count every species in a sample plot of tropical forest and multiply by the area of the earth",
       "Use the slope Z of the species–area relationship for whole continents",
       "Add up the species listed in the IUCN Red List"], "D"),
    "How the total number of species is estimated",
    "NCERT: since an overwhelmingly large proportion of undiscovered species are in the tropics, biologists make a "
    "statistical comparison of the temperate–tropical species richness of an exhaustively studied group of "
    "insects and extrapolate this ratio to other groups of animals and plants to come up with a gross estimate of "
    "the total number of species on earth. May's conservative estimate is about 7 million.",
    ["Well-studied insect group", "Temperate : tropical richness ratio", "Extrapolated to other groups → ~7 "
     "million"],
    C12_BD("biodiversity: how many species are there on earth"),
    why="NCERT describes extrapolation of a temperate–tropical ratio, not plot counts scaled to the earth, the "
        "species–area slope or Red List totals.",
    seconds=40)

add(BDC, "Importance and loss", "Intermediate", "multi_statement",
    ms("A large forest is broken up by roads and farms into small, isolated fragments. According to NCERT, which "
       "of the following consequences are expected?",
       ["Mammals and birds requiring large territories are badly affected.",
        "Certain animals with migratory habits are badly affected.",
        "Populations of such animals decline.",
        "All species benefit, because the forest edges increase.",
        "Only plant species are affected; animals simply move elsewhere."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
    "Effects of habitat fragmentation",
    "NCERT: when large habitats are broken up into small fragments due to various human activities, mammals and "
    "birds requiring large territories and certain animals with migratory habits are badly affected, leading to "
    "population declines. Habitat loss and fragmentation is the most important cause driving animals and plants to "
    "extinction, so (d) and (e) are false.",
    ["Large-territory mammals and birds (a)", "Migratory animals (b)", "Population declines (c)"],
    C12_BD("loss of biodiversity: causes (habitat loss and fragmentation)"),
    why="Options with (d) or (e) contradict NCERT; '(a), (c) and (e)' also omits migratory animals.",
    seconds=40)

add(BDC, "In situ and ex situ conservation", "Intermediate", "assertion_reason",
    ar("Ex situ conservation is the approach that protects the whole ecosystem in which a threatened species "
       "lives.",
       "When we conserve and protect the whole ecosystem, its biodiversity at all levels is protected; for "
       "example, we save the entire forest to save the tiger."),
    AR("D"),
    "In situ protects the whole ecosystem",
    "NCERT: when we conserve and protect the whole ecosystem, its biodiversity at all levels is protected, as in "
    "saving the entire forest to save the tiger: this is in situ (on site) conservation (R true). Ex situ (off "
    "site) conservation takes threatened animals and plants out of their natural habitat and places them in "
    "special settings such as zoological parks, botanical gardens and seed banks, so A is false.",
    ["Whole ecosystem protected → in situ", "Ex situ: outside the natural habitat → A false", "R: true"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity"),
    seconds=35)

_ratio = 8.1 / 2.4
assert 3.3 < _ratio < 3.5

add(BDC, "Patterns of biodiversity", "Intermediate", "direct",
    "India has only 2.4 per cent of the world's land area but 8.1 per cent of the global species diversity. Relative "
    "to the world average, about how many times as many species per unit land area does this imply for India?",
    P("About 3.4 times", ["About 5.7 times", "About 0.3 times", "About 19 times"], "B"),
    "India's share of global species diversity",
    "Species per unit area relative to the world average = (share of species)/(share of land) = 8.1/2.4 ≈ 3.4. "
    "NCERT uses these figures to show that India, one of the 12 megadiversity countries, is far richer in species "
    "than its land area alone would suggest.",
    ["Ratio = 8.1 ÷ 2.4", "≈ 3.4 times"],
    C12_BD("biodiversity: how many species are there on earth and how many in India"),
    why="5.7 is the difference of the percentages, not a ratio; 0.3 inverts the ratio; 19 multiplies the two "
        "percentages.",
    seconds=35, verified_by=RECOMPUTED)

add(BDC, "Patterns of biodiversity", "Intermediate", "multi_statement",
    ms("Which of the following are examples of genetic diversity given in NCERT?",
       ["Variation in the potency and concentration of the active chemical reserpine in Rauwolfia vomitoria growing "
        "in different Himalayan ranges",
        "India has more than 50,000 genetically different strains of rice.",
        "India has 1,000 varieties of mango.",
        "The Western Ghats have a greater amphibian species diversity than the Eastern Ghats.",
        "India has a greater ecosystem diversity than a Scandinavian country like Norway."]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "A"),
    "Levels of biodiversity",
    "NCERT's examples of genetic diversity within a species: Rauwolfia vomitoria from different Himalayan ranges, "
    "differing in the potency and concentration of reserpine (a); more than 50,000 genetically different strains "
    "of rice (b) and 1,000 varieties of mango (c) in India. The Western Ghats' amphibian richness is NCERT's "
    "example of species diversity (d), and India versus Norway illustrates ecological diversity (e).",
    ["Genetic: (a), (b), (c)", "Species: (d)", "Ecological: (e)"],
    C12_BD("biodiversity: levels of biodiversity"),
    why="Options with (d) or (e) mix in NCERT's examples of species and ecological diversity.",
    seconds=40)

add(BDC, "Importance and loss", "Advanced", "multi_statement",
    ms("Community P has many more species than an otherwise similar community Q. On the basis of NCERT's account "
       "of biodiversity and ecosystem stability, which predictions are reasonable?",
       ["P will show less year-to-year variation in total biomass than Q.",
        "P will tend to have higher productivity than Q.",
        "P will be more resistant to invasions by alien species than Q.",
        "P will be more susceptible to environmental perturbations such as drought than Q.",
        "Loss of a few species from P can never affect any of its ecosystem processes."]),
    MS(["a", "b", "c"], [["a", "b", "c", "e"], ["b", "c", "d"], ["a", "d", "e"]], "D"),
    "Species richness and stability",
    "NCERT: ecologists believe communities with more species tend to be more stable. A stable community should "
    "not show too much variation in productivity from year to year, should be resistant or resilient to "
    "occasional disturbance, and should be resistant to invasions by alien species. Tilman found that plots with "
    "more species showed less year-to-year variation in total biomass and that increased diversity contributed to "
    "higher productivity (a, b, c). Loss of biodiversity lowers resistance to perturbations such as drought (d "
    "false) and may increase variability in ecosystem processes; losing a key species can be serious (e false).",
    ["Tilman: less variation, higher productivity", "Stable: resistant to aliens", "(d), (e) contradict NCERT"],
    C12_BD("patterns of biodiversity: importance of species diversity to the ecosystem"),
    why="Options with (d) or (e) contain a false prediction; '(b), (c) and (d)' also omits (a).",
    seconds=55)

_C, _Z, _A = 10, F(1, 5), 10**5
assert 10 ** (math.log10(_C) + float(_Z) * math.log10(_A)) == 100

add(BDC, "Patterns of biodiversity", "Advanced", "direct",
    "For islands within a region, the species–area relationship is log S = log C + Z log A, with C = 10 and Z = 0.2 "
    "(area in km²). How many species are expected on an island of 1,00,000 km²?",
    P("100", ["20,000", "50", "1,000"], "C"),
    "Using the species–area equation",
    "log A = log 10⁵ = 5. log S = log 10 + 0.2 × 5 = 1 + 1 = 2, so S = 10² = 100 species. Equivalently, "
    "S = C·A^Z = 10 × (10⁵)^0.2 = 10 × 10 = 100.",
    ["log A = 5", "log S = 1 + 0.2 × 5 = 2", "S = 100"],
    C12_BD("patterns of biodiversity: species–area relationships"),
    why="20,000 multiplies Z by A instead of using logarithms; 50 halves the answer; 1,000 comes from slips such as "
        "taking Z = 0.4 (log S = 1 + 2 = 3).",
    seconds=60, verified_by=RECOMPUTED)

add(BDC, "Importance and loss", "Advanced", "assertion_reason",
    ar("When alien species are introduced unintentionally or deliberately, some of them turn invasive and cause "
       "the decline or extinction of indigenous species.",
       "Parthenium, Lantana and water hyacinth are indigenous Indian species that have been threatened by "
       "over-exploitation."),
    AR("C"),
    "Alien species invasions",
    "NCERT: when alien species are introduced, some of them turn invasive and cause decline or extinction of "
    "indigenous species (A true), as with the Nile perch in Lake Victoria. NCERT cites carrot grass (Parthenium), "
    "Lantana and water hyacinth (Eichhornia) as invasive weed species that have posed a threat to our native "
    "species; they are aliens, not threatened indigenous species, so R is false.",
    ["A: true", "Parthenium, Lantana, Eichhornia: invasive aliens → R false"],
    C12_BD("loss of biodiversity: causes (alien species invasions)"),
    seconds=40)

add(BDC, "In situ and ex situ conservation", "Advanced", "multi_statement",
    ms("Which of the following measures are correctly classified?",
       ["Propagating a rare orchid by tissue culture: ex situ conservation",
        "Declaring the forest habitat of an endangered deer a biosphere reserve: in situ conservation",
        "Storing the sperm of a threatened mammal by cryopreservation: ex situ conservation",
        "Keeping animals in a wildlife safari park: in situ conservation",
        "Protecting a sacred grove: ex situ conservation"]),
    MS(["a", "b", "c"], [["a", "b", "c", "d"], ["b", "c", "e"], ["a", "d", "e"]], "B"),
    "Classifying conservation measures",
    "NCERT: in situ conservation protects species in their natural habitat, e.g. biosphere reserves, national "
    "parks, wildlife sanctuaries and sacred groves. Ex situ conservation protects them outside their natural "
    "habitat: zoological parks, botanical gardens, wildlife safari parks, cryopreservation of gametes, in vitro "
    "fertilisation, tissue culture propagation and seed banks. So (a), (b) and (c) are correctly classified, while "
    "safari parks are ex situ (d false) and sacred groves are in situ (e false).",
    ["In situ: biosphere reserve, sacred grove", "Ex situ: tissue culture, cryopreservation, safari park"],
    C12_BD("biodiversity conservation: how do we conserve biodiversity"),
    why="Options with (d) or (e) reverse the class of safari parks or sacred groves.",
    seconds=45)
