
# ================================================================ Evolution (5/7/5)
_n, _q = 250, F(1, 5)
_A_copies = 2 * _n * (1 - _q)
assert _A_copies == 400
Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "A population of 250 diploid individuals is being studied for a gene with two alleles, A and a. The frequency "
  "of allele a in the gene pool is 0.2. How many copies of allele A are present in the gene pool of this population "
  "for this gene?",
  "Gene pool and allele frequency",
  "NCERT: the gene pool is the total genes and their alleles in a population, and the sum total of all allelic "
  "frequencies is 1. Each diploid individual carries two copies of the gene, so the gene pool holds 2 × 250 = 500 "
  "copies. The frequency of A is 1 - 0.2 = 0.8, so the number of A copies is 0.8 × 500 = 400.",
  ["Copies of the gene = 2 × 250 = 500", "p = 1 - q = 0.8", "A copies = 0.8 × 500 = 400"],
  "Hardy-Weinberg Principle",
  at="A", correct="400",
  wrong=["200", "100", "160"],
  why="200 forgets that each individual carries two copies; 100 is the number of copies of allele a; 160 is the "
      "expected number of AA individuals (0.64 × 250), not of A alleles.",
  short="Copies of an allele = 2N × its frequency.", secs=40, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", B, D,
  "Ernst Haeckel proposed embryological support for evolution based on features common to vertebrate embryos. "
  "Who, according to NCERT, disapproved of this proposal on careful study, noting that embryos never pass through "
  "the adult stages of other animals?",
  "Embryological evidence",
  "NCERT: embryological support for evolution was proposed by Ernst Haeckel based upon the observation of certain "
  "features during the embryonic stage common to all vertebrates that are absent in the adult (e.g. a row of "
  "vestigial gill slits). This proposal was disapproved on careful study performed by Karl Ernst von Baer, who "
  "noted that embryos never pass through the adult stages of other animals.",
  ["Haeckel: proposed embryological support", "von Baer: disapproved it"],
  "What are the Evidences for Evolution?",
  at="B", correct="Karl Ernst von Baer",
  wrong=["Louis Pasteur", "Hugo de Vries", "Alfred Wallace"],
  why="Pasteur disproved spontaneous generation; de Vries proposed mutation from his work on evening primrose; "
      "Wallace reached conclusions similar to Darwin's in the Malay Archipelago. None of them tested Haeckel's "
      "proposal.", secs=25)

Z(EVO, "Evidences of evolution", B, D,
  "Similarities in proteins and genes performing a given function among diverse organisms are used as evidence of "
  "evolution. According to NCERT, what do these similarities indicate?",
  "Biochemical evidence",
  "NCERT: similarities in proteins and genes performing a given function among diverse organisms give clues to "
  "common ancestry. These biochemical similarities point to the same shared ancestry as structural similarities "
  "among diverse organisms.",
  ["Similar proteins and genes for a given function", "-> clues to common (shared) ancestry",
   "Same conclusion as structural (anatomical) similarities"],
  "What are the Evidences for Evolution?",
  at="D", correct="They point to the same shared ancestry as structural similarities among diverse organisms",
  wrong=["They show analogy produced only by convergent evolution",
         "They show that the organisms arose by special creation",
         "They show that the proteins were acquired through use and disuse"],
  why="NCERT treats these biochemical similarities as clues to common ancestry, not as analogy; special creation "
      "and use and disuse (Lamarck) are not what NCERT draws from them.", secs=25)

Z(EVO, "Human evolution", B, STP,
  SP("Fossils of Homo erectus were discovered in Java in 1891.",
     "Neanderthal man used hides to protect the body and buried their dead."),
  "Homo erectus and Neanderthal man",
  "NCERT: fossils discovered in Java in 1891 revealed the next stage, Homo erectus, about 1.5 mya; Homo erectus had "
  "a large brain of around 900 cc and probably ate meat. The Neanderthal man, with a brain size of 1400 cc, lived in "
  "near east and central Asian countries; they used hides to protect their body and buried their dead.",
  ["Statement I: true", "Statement II: true"],
  "Origin and Evolution of Man", ans="A",
  why="Both statements are NCERT's account, so every option calling either of them false is wrong.", secs=25)

Z(EVO, "Origin of life", B, ASR,
  AR("Louis Pasteur's experiments dismissed the theory of spontaneous generation.",
     "Pasteur showed that in pre-sterilised flasks life did not come from killed yeast, while in another flask "
     "open to air new living organisms arose from the 'killed yeast'."),
  "Pasteur and spontaneous generation",
  "NCERT: earlier it was believed that life came out of decaying and rotting matter like straw and mud "
  "(spontaneous generation). Louis Pasteur, by careful experimentation, demonstrated that life comes only from "
  "pre-existing life: in pre-sterilised flasks life did not come from killed yeast, while in another flask open to "
  "air new living organisms arose from killed yeast. Spontaneous generation theory was dismissed once and for all. "
  "The experiment in R is the reason A happened.",
  ["A: true", "R: true", "R is the experimental result that dismissed the theory"],
  "Origin of Life",
  ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R describes the very "
      "experiment that dismissed spontaneous generation, so it explains A.", secs=35)

_cave, _agri = 18000, 10000
assert _cave - _agri == 8000
Z(EVO, "Human evolution", I, NUM,
  "According to NCERT, pre-historic cave art developed about 18,000 years ago, and agriculture came around 10,000 "
  "years back, when human settlements started. About how many years separated the development of cave art from "
  "the coming of agriculture?",
  "Timeline of modern humans",
  "NCERT: pre-historic cave art developed about 18,000 years ago; agriculture came around 10,000 years back and "
  "human settlements started. Both are given as 'years ago', so the gap is 18,000 - 10,000 = 8,000 years, with "
  "cave art coming first.",
  ["Cave art: about 18,000 years ago", "Agriculture: about 10,000 years ago", "Gap = 18,000 - 10,000 = 8,000 years"],
  "Origin and Evolution of Man",
  at="C", correct="About 8,000 years",
  wrong=["About 28,000 years", "About 80,000 years", "About 1,800 years"],
  why="28,000 adds two 'years ago' figures instead of subtracting them; 80,000 and 1,800 slip a factor of ten "
      "(the difference multiplied by ten, and the cave-art date divided by ten).",
  short="For two 'years ago' dates, the gap is the difference.", secs=35, vb=RECOMPUTED)

Z(EVO, "Origin of life", I, MUL,
  MS("Which of the following are connotations of the theory of special creation, as stated in NCERT?",
     ["All living organisms (species or types) that we see today were created as such.",
      "The diversity was always the same since creation and will be the same in future also.",
      "The earth is about 4000 years old.",
      "Present-day species arose by natural selection of heritable variations.",
      "Life came out of decaying and rotting matter like straw and mud."]),
  "Theory of special creation",
  "NCERT: the theory of special creation has three connotations: one, that all living organisms (species or types) "
  "that we see today were created as such; two, that the diversity was always the same since creation and will be "
  "the same in future also; and three, that the earth is about 4000 years old. Natural selection is Darwin's idea, "
  "and life from rotting matter is spontaneous generation.",
  ["(a), (b), (c): the three connotations", "(d): Darwinism", "(e): spontaneous generation"],
  "Evolution of Life Forms - A Theory",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(a) and (d) only", "(b), (c) and (d) only"],
  why="(d) is the opposite of special creation and (e) is the theory of spontaneous generation, so every option "
      "containing either is wrong; all three of (a), (b) and (c) are needed.", secs=40)

Z(EVO, "Natural selection", I, D,
  "NCERT notes that excess use of herbicides and pesticides has resulted only in the selection of resistant "
  "varieties in a much lesser time scale. To which other case does NCERT say this is also true?",
  "Evolution by anthropogenic action",
  "NCERT: excess use of herbicides, pesticides, etc., has only resulted in selection of resistant varieties in a "
  "much lesser time scale. This is also true for microbes against which we employ antibiotics or drugs against "
  "eukaryotic organisms/cells. Hence, resistant organisms/cells are appearing in a time scale of months or years "
  "and not centuries. These are examples of evolution by anthropogenic action.",
  ["Herbicides/pesticides -> resistant varieties quickly",
   "Same for microbes and antibiotics, and drugs against eukaryotic cells", "Time scale: months or years"],
  "Evolution by Natural Selection",
  at="D", correct="Microbes against which we employ antibiotics, and eukaryotic organisms/cells against which we "
                  "use drugs",
  wrong=["Darwin's finches of the Galapagos Islands", "The marsupials of Australia",
         "The forelimbs of whales, bats, cheetahs and humans"],
  why="Darwin's finches and the Australian marsupials are NCERT's examples of adaptive radiation over long periods; "
      "vertebrate forelimbs are homologous organs, an anatomical evidence, not resistance arising from human "
      "action.", secs=30)

Z(EVO, "Origin of life", I, ASR,
  AR("NCERT describes the origin of life as a unique event in the history of the universe.",
     "Life appeared on the earth about one billion years after the earth was formed."),
  "When life appeared",
  "NCERT: the origin of life is considered a unique event in the history of the universe. The earth was formed "
  "about 4.5 billion years back, and life appeared 500 million years after the formation of the earth, i.e. "
  "almost four billion years back. R doubles that interval, so A is true and R is false.",
  ["A: true", "R: false - life appeared about 500 million years after the earth formed"],
  "Origin of Life", ans="C",
  why="R gives one billion years instead of NCERT's 500 million, so options treating R as true are wrong; A is "
      "NCERT's own statement, so 'A is false' is wrong.", secs=35)

Z(EVO, "Origin of life", I, STP,
  SP("The first mammals were large animals, like elephants.",
     "Mammals were viviparous and protected their unborn young inside the mother's body."),
  "Early mammals",
  "NCERT: the first mammals were like shrews; their fossils are small sized. Mammals were viviparous and protected "
  "their unborn young inside the mother's body; they were also more intelligent in sensing and avoiding danger, at "
  "least.",
  ["Statement I: false - the first mammals were like shrews", "Statement II: true"],
  "A Brief Account of Evolution", ans="D",
  why="Statement I is false because NCERT compares the first mammals to shrews, so options calling it true are "
      "wrong; Statement II is NCERT's description, so options calling it false are wrong.", secs=30)

Z(EVO, "Origin of life", I, D,
  "Which sequence of events agrees with NCERT's account of the Big Bang theory of the origin of the universe?",
  "Big Bang and the formation of galaxies",
  "NCERT: the Big Bang theory talks of a singular huge explosion unimaginable in physical terms. The universe "
  "expanded and hence the temperature came down. Hydrogen and helium formed sometime later. The gases condensed "
  "under gravitation and formed the galaxies of the present-day universe. In the solar system of the Milky Way "
  "galaxy, the earth was formed about 4.5 billion years back.",
  ["Explosion -> expansion and cooling", "-> hydrogen and helium formed", "-> gases condensed under gravitation",
   "-> galaxies"],
  "Origin of Life",
  at="B", correct="Huge explosion → expansion and fall in temperature → formation of hydrogen and helium → "
                  "condensation of gases under gravitation to form galaxies",
  wrong=["Formation of galaxies → huge explosion → formation of hydrogen and helium → expansion and fall in "
         "temperature",
         "Huge explosion → condensation of gases under gravitation to form galaxies → expansion and fall in "
         "temperature → formation of hydrogen and helium",
         "Formation of hydrogen and helium → huge explosion → contraction and rise in temperature → formation of "
         "galaxies"],
  why="Galaxies formed last, from gases that condensed after hydrogen and helium had formed, so options placing "
      "galaxies before or at the explosion are wrong; NCERT describes expansion and cooling, not contraction and "
      "heating.", secs=35)

Z(EVO, "Darwinism and modern synthesis", I, MAT,
  ML(("scientist", "what NCERT links with the scientist"),
     ["Charles Darwin", "Hugo de Vries", "Louis Pasteur", "Alfred Wallace"],
     ["Malay Archipelago", "Evening primrose", "Sea voyage round the world in H.M.S. Beagle",
      "Killed yeast in pre-sterilised flasks"]),
  "Scientists in the history of evolutionary thought",
  "NCERT: Darwin's conclusions were based on observations made during a sea voyage in the sailing ship H.M.S. "
  "Beagle round the world. Hugo de Vries, based on his work on evening primrose, brought forth the idea of "
  "mutations. Louis Pasteur showed with killed yeast in pre-sterilised flasks that life comes only from "
  "pre-existing life. Alfred Wallace, a naturalist who worked in the Malay Archipelago, came to similar conclusions "
  "as Darwin around the same time.",
  ["A Darwin -> III", "B de Vries -> II", "C Pasteur -> IV", "D Wallace -> I"],
  "Evolution by Natural Selection; Origin of Life",
  at="D", match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"}]),
  why="Wallace, not Darwin, worked in the Malay Archipelago; de Vries worked on evening primrose and Pasteur on "
      "killed yeast, so swapping them is wrong.", secs=40)

_qq = 1 - F(91, 100)
_q3 = F(3, 10)
assert _q3 * _q3 == _qq
_p3 = 1 - _q3
assert (_p3 * _p3) / (2 * _p3 * _q3) == F(7, 6)
Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population in Hardy-Weinberg equilibrium for a gene with a dominant allele A and a recessive allele a, "
  "91% of the individuals show the dominant phenotype. What is the ratio of homozygous dominant (AA) to "
  "heterozygous (Aa) individuals in this population?",
  "Genotype frequencies from a phenotype frequency",
  "In Hardy-Weinberg equilibrium the genotype frequencies are p², 2pq and q² (p² + 2pq + q² = 1). The recessive "
  "phenotype shows only in aa, so q² = 1 - 0.91 = 0.09 and q = 0.3; p = 1 - 0.3 = 0.7. Then AA = p² = 0.49 and "
  "Aa = 2pq = 2 × 0.7 × 0.3 = 0.42, giving AA : Aa = 0.49 : 0.42 = 7 : 6.",
  ["q² = 1 - 0.91 = 0.09 -> q = 0.3", "p = 0.7", "AA = p² = 0.49; Aa = 2pq = 0.42", "Ratio = 49 : 42 = 7 : 6"],
  "Hardy-Weinberg Principle",
  at="B", correct="7 : 6",
  wrong=["49 : 9", "7 : 3", "1 : 1"],
  why="49 : 9 is AA : aa; 7 : 3 is the ratio of the allele frequencies p : q, not of genotypes; 1 : 1 assumes "
      "the dominant phenotype is split equally between AA and Aa.",
  short="AA : Aa = p² : 2pq = p : 2q = 0.7 : 0.6.", secs=75, vb=RECOMPUTED)

Z(EVO, "Darwinism and modern synthesis", A, MUL,
  MS("Which of the following ideas belong to Darwin's theory of evolution as described in NCERT?",
     ["Any population has built-in variation in characteristics.",
      "Fitness ultimately and only refers to reproductive fitness: those better fit in an environment leave more "
      "progeny than others.",
      "Characters developed by the use of organs during an individual's life are passed on, as in the long neck "
      "of the giraffe.",
      "New species arise by single-step large mutations (saltation).",
      "Existing living forms share similarities, to varying degrees, with life forms that existed millions of "
      "years ago."]),
  "Darwin versus Lamarck and de Vries",
  "NCERT: Darwin concluded that existing living forms share similarities to varying degrees not only among "
  "themselves but also with life forms that existed millions of years ago; that any population has built-in "
  "variation in characteristics; and that fitness ultimately and only refers to reproductive fitness. Evolution "
  "driven by the use and disuse of organs (giraffe's neck) was Lamarck's idea, and single-step large mutation "
  "(saltation) was de Vries's.",
  ["(a) Darwin", "(b) Darwin", "(c) Lamarck", "(d) de Vries", "(e) Darwin"],
  "Evolution by Natural Selection; Mechanism of Evolution",
  at="A", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="(c) is Lamarck's use and disuse and (d) is de Vries's saltation, so every option including either is "
      "wrong; the correct option keeps all three of Darwin's ideas.", secs=50)

Z(EVO, "Darwinism and modern synthesis", A, MAT,
  ML(("term", "meaning, as used in NCERT"),
     ["Saltation", "Fitness (Darwin)", "Genetic equilibrium", "Adaptive radiation"],
     ["Reproductive fitness: those better fit leave more progeny",
      "Allele frequencies stable, so the gene pool remains a constant",
      "Evolution of different species in a given geographical area starting from a point and radiating to other "
      "habitats",
      "Single-step large mutation"]),
  "Evolutionary terms",
  "NCERT: de Vries believed mutation causes evolution, and single-step large mutation is called saltation. "
  "Darwin's fitness ultimately and only refers to reproductive fitness. When allele frequencies are stable, the "
  "gene pool remains a constant; this is called genetic equilibrium. Adaptive radiation is the process of evolution "
  "of different species in a given geographical area starting from a point and literally radiating to other areas "
  "of geography (habitats).",
  ["A saltation -> IV", "B fitness -> I", "C genetic equilibrium -> II", "D adaptive radiation -> III"],
  "Mechanism of Evolution; Hardy-Weinberg Principle; Adaptive Radiation",
  at="C", match=({"A": "IV", "B": "I", "C": "II", "D": "III"},
                 [{"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "I", "B": "IV", "C": "II", "D": "III"}]),
  why="Saltation is a single large mutation, not radiation into habitats; Darwin's fitness concerns leaving more "
      "progeny, while a constant gene pool is genetic equilibrium; and fitness is not a mutation.", secs=50)

Z(EVO, "Evidences of evolution", A, ASR,
  AR("Analogous structures indicate common ancestry of the organisms that have them.",
     "Analogous structures are a result of convergent evolution, in which different structures evolve for the same "
     "function."),
  "Analogy versus homology",
  "NCERT: analogous structures are not anatomically similar though they perform similar functions (e.g. wings of "
  "butterfly and of birds); they are a result of convergent evolution, where different structures evolve for the "
  "same function and hence have similarity. It is homology, a result of divergent evolution, that indicates "
  "common ancestry. So A is false and R is true.",
  ["A: false - homology, not analogy, indicates common ancestry", "R: true - analogy arises by convergent evolution"],
  "What are the Evidences for Evolution?", ans="D",
  why="A gives analogous structures the meaning of homologous ones, so options calling A true are wrong; R is "
      "NCERT's own explanation of analogy, so 'A is false but R is true' is the answer.", secs=40)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "In which of the following situations does the allele frequency of a population change mainly through GENETIC "
  "DRIFT, as NCERT defines it?",
  "Genetic drift as a chance change",
  "NCERT: gene flow is the change in gene frequencies caused by migration of a section of a population to another "
  "place and population. If the same change occurs by chance, it is called genetic drift. Natural selection acts on "
  "heritable variation that enables better survival and reproduction, and mutation produces new variation. A "
  "landslide that kills individuals at random, irrespective of genotype, changes allele frequencies by chance.",
  ["Migration -> gene flow", "Chance -> genetic drift", "Better survival of a variant -> natural selection",
   "New allele -> mutation"],
  "Hardy-Weinberg Principle",
  at="C", correct="A landslide kills half of a small population at random, irrespective of genotype, and the "
                  "allele frequencies of the survivors happen to differ from those before",
  wrong=["Excessive use of a pesticide leaves mostly resistant insects, whose numbers then increase",
         "Individuals of a neighbouring population repeatedly migrate in and interbreed",
         "A new allele appears in a gamete and is passed on to the offspring"],
  why="Pesticide resistance spreading is natural selection; repeated migration with interbreeding is gene flow; a "
      "new allele arising in a gamete is mutation. Only the random deaths change frequencies purely by chance.",
  secs=50)
