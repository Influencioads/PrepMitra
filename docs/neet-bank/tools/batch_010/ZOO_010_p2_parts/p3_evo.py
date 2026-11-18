

# ================================================================ Evolution (6/8/6)
# recomputed keys: homozygotes = heterozygotes; p^2 - q^2 = 0.20; maximum of 2pq; HR meiotic divisions
_q = F(1, 2)
assert (1 - _q) ** 2 + _q ** 2 == 2 * (1 - _q) * _q and _q == F(1, 2)
assert all(((1 - F(k, 100)) ** 2 + F(k, 100) ** 2 == 2 * (1 - F(k, 100)) * F(k, 100)) == (k == 50) for k in range(101))
_p = (1 + F(1, 5)) / 2
assert _p == F(3, 5) and _p ** 2 - (1 - _p) ** 2 == F(1, 5) and 2 * _p * (1 - _p) == F(12, 25)
assert max(2 * F(k, 1000) * (1 - F(k, 1000)) for k in range(1001)) == F(1, 2)
assert (100 // 4) * (1 + 2) == 75 and 100 * (1 + 1) == 200
Z(EVO, "Evidences of evolution", B, D,
  "Fossils found in different-aged rock sediments are used as evidence for evolution. Which method does NCERT "
  "refer to for calculating the ages of fossils?",
  "Dating of fossils",
  "NCERT: fossils are remains of hard parts of life-forms found in rocks, and different-aged rock sediments contain "
  "fossils of different life-forms. While discussing palaeontological evidence, NCERT asks the reader to recall how "
  "the ages of fossils are calculated, i.e. the method of radioactive dating and the principles behind it.",
  ["Age of fossils -> radioactive dating"],
  "What are the Evidences for Evolution?",
  at="C", correct="Radioactive dating",
  wrong=["Comparing the similarities in proteins and genes", "Counting the number of sediment layers above them",
         "Measuring the size of the fossil"],
  why="Protein and gene similarities are biochemical evidence of common ancestry, not a way to date fossils; NCERT "
      "does not describe counting layers or measuring size as methods for calculating the age of fossils.", secs=25)

Z(EVO, "Origin of life", B, D,
  "S.L. Miller, an American scientist, created conditions similar to those of the early earth on a laboratory scale "
  "and observed the formation of amino acids. According to NCERT, he did this experiment in:",
  "Miller's experiment",
  "NCERT: in 1953, S.L. Miller, an American scientist, created electric discharge in a closed flask containing CH4, "
  "H2, NH3 and water vapour and observed the formation of amino acids.",
  ["Miller's experiment: 1953"],
  "Origin of Life",
  at="A", correct="1953",
  wrong=["1938", "1891", "1920"],
  why="1938 is the year a coelacanth was caught in South Africa; 1891 is when Homo erectus fossils were found in "
      "Java; 1920 is the year of the post-industrial moth collection in England.", secs=20)

Z(EVO, "Evidences of evolution", B, D,
  "NCERT notes that man's intensive breeding programmes have created breeds that differ from other breeds but still "
  "are of the same group. Which animal does NCERT give as the example?",
  "Artificial selection by man",
  "NCERT: man has bred selected plants and animals for agriculture, horticulture, sport and security, and has "
  "domesticated many wild animals and crops. This intensive breeding programme has created breeds that differ from "
  "other breeds (e.g., dogs) but still are of the same group.",
  ["Example given: breeds of dogs"],
  "What are the Evidences for Evolution?",
  at="D", correct="Dogs",
  wrong=["Moths", "Finches", "Marsupials"],
  why="Moths are NCERT's example of industrial melanism, finches of adaptive radiation in the Galapagos, and "
      "marsupials of adaptive radiation in Australia; none of these is an example of breeds made by man.", secs=20)

Z(EVO, "Natural selection", B, D,
  "According to NCERT, evolution by natural selection, in a true sense, would have started when:",
  "Beginning of evolution by natural selection",
  "NCERT (Biological Evolution): evolution by natural selection, in a true sense, would have started when cellular "
  "forms of life with differences in metabolic capability originated on earth. Selection needs differences among "
  "individuals that affect survival and reproduction.",
  ["Natural selection needs variation", "Start: cellular forms of life with differences in metabolic capability"],
  "Biological Evolution",
  at="B", correct="Cellular forms of life with differences in metabolic capability originated on earth",
  wrong=["The first giant molecules such as RNA and proteins formed in the oceans",
         "The first mammals appeared on land",
         "Human beings began agriculture and settlements"],
  why="NCERT links true natural selection to cellular life with metabolic differences, not to the earlier "
      "non-cellular giant molecules; mammals and agriculture came far later in the history of life.", secs=30)

Z(EVO, "Origin of life", B, D,
  "Early Greek thinkers thought that units of life called spores were transferred to different planets, including "
  "the earth. According to NCERT, this idea of 'panspermia' is still a favourite idea for:",
  "Panspermia",
  "NCERT: some scientists believe that life came from outer space. Early Greek thinkers thought units of life called "
  "spores were transferred to different planets including earth. 'Panspermia' is still a favourite idea for some "
  "astronomers.",
  ["Panspermia: spores transferred between planets", "Still favoured by some astronomers"],
  "Origin of Life",
  at="B", correct="Some astronomers",
  wrong=["Oparin and Haldane", "Louis Pasteur", "Most biologists"],
  why="Oparin and Haldane proposed chemical evolution from non-living organic molecules; Pasteur showed that life "
      "comes only from pre-existing life; NCERT says the majority accept that life arose through evolutionary forces "
      "from non-living molecules.", secs=25)

Z(EVO, "Natural selection", B, ASR,
  AR("In England, the collection of moths made in the 1850s had more dark-winged (melanised) moths than "
     "white-winged moths.",
     "The 1850s collection of moths was made before industrialisation set in."),
  "Industrial melanism: the 1850s collection",
  "NCERT: in a collection of moths made in the 1850s, i.e. before industrialisation set in, there were more "
  "white-winged moths on trees than dark-winged or melanised moths; in the collection from the same area after "
  "industrialisation (1920), there were more dark-winged moths. So A is false and R is true.",
  ["A: false - the 1850s collection had more white-winged moths", "R: true - it was pre-industrial"],
  "What are the Evidences for Evolution?", ans="D",
  why="A reverses NCERT's observation for the 1850s, so all options calling A true are wrong; R is correct, so "
      "'A is false but R is true' is the answer.", secs=30)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a. The combined frequency of the "
  "two homozygous genotypes (AA + aa) is exactly equal to the frequency of the heterozygous genotype (Aa). What is "
  "the frequency of allele a?",
  "Hardy-Weinberg: equating homozygotes and heterozygotes",
  "Under Hardy-Weinberg equilibrium the genotype frequencies are p² (AA), 2pq (Aa) and q² (aa), with p + q = 1 and "
  "p² + 2pq + q² = 1. If p² + q² = 2pq, then p² - 2pq + q² = 0, i.e. (p - q)² = 0, so p = q = 0.5.",
  ["p² + q² = 2pq", "(p - q)² = 0 -> p = q", "p + q = 1 -> q = 0.5"],
  "Hardy-Weinberg Principle",
  at="B", correct="0.5",
  wrong=["0.25", "0.71", "0.33"],
  why="0.25 is q² at p = q, not q; 0.71 comes from wrongly setting q² = 0.5; 0.33 comes from treating the three "
      "genotypes as equally frequent.", short="Homozygotes = heterozygotes = 0.5 each, which happens only when p = q.",
  secs=60, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", I, D,
  "The flippers of penguins (birds) and of dolphins (mammals) look alike and perform the same function. According to "
  "NCERT, which of the following best explains such similarity?",
  "Analogy and similar habitat",
  "NCERT: analogous structures are a result of convergent evolution - different structures evolving for the same "
  "function and hence having similarity; the flippers of penguins and dolphins are an example. One can say that it "
  "is the similar habitat that has resulted in selection of similar adaptive features in different groups of "
  "organisms, but towards the same function.",
  ["Flippers: analogous (convergent evolution)", "Cause: similar habitat selects similar adaptive features"],
  "What are the Evidences for Evolution?",
  at="A",
  correct="A similar habitat has resulted in the selection of similar adaptive features in different groups of "
          "organisms, towards the same function",
  wrong=["The same structure developed along different directions due to adaptations to different needs",
         "Penguins and dolphins arose from one ancestral stock within a single adaptive radiation",
         "The flippers were developed by use during the lives of the animals and passed on to the offspring"],
  why="Development of one structure in different directions describes homology (divergent evolution); penguins and "
      "dolphins belong to different groups and are not one adaptive radiation; inheritance of characters acquired by "
      "use is Lamarck's idea, not NCERT's explanation.", secs=40)

Z(EVO, "Evidences of evolution", I, ASR,
  AR("NCERT argues that nature could have created new types of organisms over millions of years.",
     "Within hundreds of years, man has been able to create new breeds of animals and plants by intensive breeding "
     "programmes."),
  "Argument from artificial selection",
  "NCERT: man has bred selected plants and animals and, by intensive breeding programmes, created breeds that differ "
  "from other breeds but still are of the same group. It is argued that if within hundreds of years man could create "
  "new breeds, could not nature have done the same over millions of years? The argument in A rests directly on the "
  "fact in R.",
  ["R: man-made breeds within hundreds of years", "A: inference - nature could do the same over millions of years",
   "R is the basis of A -> R explains A"],
  "What are the Evidences for Evolution?", ans="A",
  why="A is drawn by NCERT from R itself, so 'R is not the explanation' is wrong; both statements are NCERT's own, so "
      "the options calling either false are wrong.", secs=40)

Z(EVO, "Darwinism and modern synthesis", I, STP,
  SP("Although Mendel had talked of inheritable 'factors' influencing the phenotype, Darwin either ignored or kept "
     "silence on these aspects.",
     "Hugo de Vries believed that the minor heritable variations described by Darwin, rather than mutations, cause "
     "evolution."),
  "Source of variation: Darwin and de Vries",
  "NCERT (Mechanism of Evolution): even though Mendel had talked of inheritable 'factors' influencing phenotype, "
  "Darwin either ignored or kept silence on these aspects. The work of Hugo de Vries on evening primrose brought "
  "forth the idea of mutations; he believed that it is mutation which causes evolution and not the minor "
  "(heritable) variations that Darwin talked about.",
  ["Statement I: true", "Statement II: false - de Vries held the reverse"],
  "Mechanism of Evolution", ans="C",
  why="Statement II reverses de Vries' view, so options calling it true are wrong; Statement I is NCERT's own line, "
      "so 'both false' and 'Statement I false' are wrong.", secs=35)

Z(EVO, "Darwinism and modern synthesis", I, MAT,
  ML(("term", "description given in NCERT"),
     ["Darwinian variations", "Mutations (as proposed by de Vries)", "Evolution, as Darwin saw it",
      "Saltation"],
     ["Single-step large mutation", "Gradual", "Random and directionless", "Small and directional"]),
  "Darwin's and de Vries' views compared",
  "NCERT: mutations are random and directionless while Darwinian variations are small and directional. Evolution "
  "for Darwin was gradual, while de Vries believed mutation caused speciation and hence called it saltation "
  "(single-step large mutation).",
  ["A -> IV", "B -> III", "C -> II", "D -> I"],
  "Mechanism of Evolution",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="Swapping A and B gives Darwin's variations the features of mutations; swapping C and D makes Darwin's "
      "evolution saltatory; the last code mismatches every term.", secs=45)

Z(EVO, "Evidences of evolution", I, STP,
  SP("The study of fossils shows that every form of life has existed throughout the whole history of the earth.",
     "The study of fossils shows that certain life forms are restricted to certain geological time-spans, so new "
     "forms of life have arisen at different times in the history of the earth."),
  "What fossils show",
  "NCERT: the study of fossils in different sedimentary layers indicates the geological period in which they "
  "existed. The study showed that life-forms varied over time and certain life forms are restricted to certain "
  "geological time-spans. Hence new forms of life have arisen at different times in the history of the earth. This "
  "is palaeontological evidence.",
  ["Statement I: false - life forms varied over time", "Statement II: true"],
  "What are the Evidences for Evolution?", ans="D",
  why="Statement I contradicts the fossil record described by NCERT, so options calling it true are wrong; Statement "
      "II is NCERT's conclusion, so 'both false' is wrong.", secs=35)

Z(EVO, "Human evolution", I, D,
  "NCERT compares the skulls of an adult modern human being, a baby chimpanzee and an adult chimpanzee. What does "
  "this comparison show?",
  "Comparison of skulls",
  "NCERT (Origin and Evolution of Man) gives a comparison of the skulls of an adult modern human being, a baby "
  "chimpanzee and an adult chimpanzee, and notes that the skull of the baby chimpanzee is more like the adult human "
  "skull than the adult chimpanzee skull.",
  ["Baby chimpanzee skull resembles the adult human skull more than the adult chimpanzee skull"],
  "Origin and Evolution of Man",
  at="C",
  correct="The skull of the baby chimpanzee is more like the adult human skull than the adult chimpanzee skull",
  wrong=["The skull of the adult chimpanzee is more like the adult human skull than the baby chimpanzee skull",
         "The skulls of the baby and the adult chimpanzee are identical, and both differ from the human skull",
         "The skull of the baby chimpanzee resembles neither the adult chimpanzee skull nor the adult human skull"],
  why="NCERT's point is the reverse of the first option; baby and adult chimpanzee skulls are not identical; and the "
      "baby chimpanzee skull does resemble the adult human skull.", secs=30)

Z(EVO, "Natural selection", I, STP,
  SP("In rural areas of England where industrialisation had not occurred, the count of melanic (dark-winged) moths "
     "was low.",
     "According to NCERT, this observation supports the belief that, in a given background, moths that did not "
     "match the background were picked out by predators."),
  "Industrial melanism: evidence from rural areas",
  "NCERT: before industrialisation, thick growth of almost white-coloured lichen covered the trees and the "
  "white-winged moths survived while dark moths were picked out by predators; after industrialisation, the trunks "
  "became dark with smoke and the reverse happened. NCERT adds that this belief is supported by the fact that in "
  "rural areas where industrialisation had not occurred, the count of melanic moths was low.",
  ["Statement I: true (NCERT)", "Statement II: true - NCERT uses it as support for the predation explanation"],
  "What are the Evidences for Evolution?", ans="A",
  why="Both statements are NCERT's own, so each option with a false statement is wrong.", secs=35)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a, and allele A is the more "
  "common one. The frequency of the AA genotype exceeds that of the aa genotype by exactly 0.20. What is the "
  "frequency of heterozygotes (Aa)?",
  "Hardy-Weinberg: difference of homozygote frequencies",
  "p² - q² = (p + q)(p - q). Since p + q = 1, p² - q² = p - q. So p - q = 0.20 and p + q = 1, giving p = 0.6 and "
  "q = 0.4. The heterozygote frequency is 2pq = 2 x 0.6 x 0.4 = 0.48. Check: p² = 0.36, q² = 0.16, difference "
  "0.20.",
  ["p² - q² = (p + q)(p - q) = p - q = 0.20", "p = 0.6, q = 0.4", "2pq = 0.48"],
  "Hardy-Weinberg Principle",
  at="C", correct="0.48",
  wrong=["0.42", "0.32", "0.50"],
  why="0.42 uses p = 0.7 (taking the difference of allele frequencies as 0.4); 0.32 uses p = 0.8 (treating 0.2 as "
      "q); 0.50 assumes p = q, which would make the homozygote frequencies equal.",
  short="For two alleles, p² - q² always equals p - q.", secs=90, vb=RECOMPUTED)

Z(EVO, "Natural selection", A, MUL,
  MS("Which of the following statements about fitness are correct according to NCERT?",
     ["The so-called fitness is based on characteristics which are inherited.",
      "Adaptive ability is inherited; it has a genetic basis.",
      "Fitness is the end result of the ability to adapt and get selected by nature.",
      "According to Darwin, the fitness of an individual refers to its physical strength.",
      "Characters developed by the use of organs during an individual's life form the basis of fitness."]),
  "Fitness and its genetic basis",
  "NCERT: nature selects for fitness; the so-called fitness is based on characteristics which are inherited, so "
  "there must be a genetic basis for getting selected and to evolve. Some organisms are better adapted to survive "
  "in an otherwise hostile environment; adaptive ability is inherited and has a genetic basis. Fitness is the end "
  "result of the ability to adapt and get selected by nature. For Darwin, fitness ultimately and only refers to "
  "reproductive fitness. Use and disuse of organs is Lamarck's idea.",
  ["(a), (b), (c): NCERT's statements", "(d): false - reproductive fitness",
   "(e): false - acquired characters (Lamarck), not inherited ones"],
  "Biological Evolution; Evolution of Life Forms - A Theory",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only"],
  why="'(a) and (b) only' leaves out NCERT's description of fitness as the end result of adaptation and selection; "
      "fitness in Darwin's sense is reproductive, not physical strength, and fitness rests on inherited, not acquired, "
      "characters, so options with (d) or (e) are wrong.", secs=60)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "In a very large population with no migration, no new mutations and random mating, individuals of genotype aa "
  "consistently leave fewer surviving offspring than AA and Aa individuals in every generation, and the frequency of "
  "allele a falls steadily. Which of the factors that NCERT lists as affecting Hardy-Weinberg equilibrium is acting "
  "here?",
  "Identifying the factor disturbing Hardy-Weinberg equilibrium",
  "NCERT lists five factors that affect Hardy-Weinberg equilibrium: gene migration (gene flow), genetic drift, "
  "mutation, genetic recombination and natural selection. Natural selection is a process in which heritable "
  "variations enabling better survival are enabled to reproduce and leave a greater number of progeny. Here a "
  "genotype consistently leaves fewer offspring - a systematic, not chance, effect - in a very large population with "
  "no migration or mutation.",
  ["No migration -> not gene flow", "Very large population, consistent effect -> not chance (drift)",
   "Differential reproduction by genotype -> natural selection"],
  "Hardy-Weinberg Principle",
  at="B", correct="Natural selection",
  wrong=["Genetic drift", "Gene flow", "Founder effect"],
  why="Genetic drift and the founder effect are chance changes, typically in small samples, not a steady, "
      "genotype-linked difference in reproduction in a very large population; gene flow needs migration, which the "
      "stem excludes.", secs=50)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, STP,
  SP("If the allele frequencies of a population remain stable and constant from generation to generation, the "
     "population is undergoing evolution.",
     "A change in the frequency of alleles in a population, i.e. a disturbance of Hardy-Weinberg equilibrium, is "
     "interpreted as resulting in evolution."),
  "Genetic equilibrium and evolution",
  "NCERT: the Hardy-Weinberg principle says that allele frequencies in a population are stable and constant from "
  "generation to generation; the gene pool remains a constant (genetic equilibrium). Disturbance in genetic "
  "equilibrium, or Hardy-Weinberg equilibrium, i.e. a change of frequency of alleles in a population, is then "
  "interpreted as resulting in evolution. Stable allele frequencies therefore mean no evolution at that gene.",
  ["Statement I: false - stable frequencies = genetic equilibrium", "Statement II: true"],
  "Hardy-Weinberg Principle", ans="D",
  why="Statement I describes equilibrium as evolution, the opposite of NCERT, so options calling it true are wrong; "
      "Statement II is NCERT's interpretation, so 'both false' is wrong.", secs=45)

Z(EVO, "Human evolution", A, ASR,
  AR("Of the two early primates Dryopithecus and Ramapithecus, Ramapithecus was more man-like while "
     "Dryopithecus was more ape-like.",
     "Both Dryopithecus and Ramapithecus were hairy and walked like gorillas and chimpanzees."),
  "Dryopithecus and Ramapithecus",
  "NCERT describes the early primates Dryopithecus and Ramapithecus: they were hairy and walked like "
  "gorillas and chimpanzees. Ramapithecus was more man-like while Dryopithecus was more ape-like. R describes "
  "features the two shared, so it cannot explain how they differed.",
  ["A: true", "R: true", "R gives shared features; A is a difference -> R is not the explanation"],
  "Origin and Evolution of Man", ans="B",
  why="A shared feature cannot explain a difference between the two primates, so 'R is the correct explanation' is "
      "wrong; both statements are NCERT's, so the options calling either false are wrong.", secs=40)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "For a gene with two alleles, A (frequency p) and a (frequency q), in a population in Hardy-Weinberg equilibrium, "
  "which of the following is ALWAYS true, whatever the value of p?",
  "Limits of Hardy-Weinberg genotype frequencies",
  "Genotype frequencies are p², 2pq and q² with p + q = 1. The heterozygote frequency 2pq = 2p(1 - p) is largest when "
  "p = 0.5, where it equals 0.5; for any other p it is smaller. So 2pq can never exceed 0.5. The other statements "
  "fail for some value of p: for p = 0.5, AA (0.25) is less than Aa (0.5); for p = 0.9, 2pq = 0.18 is less than "
  "p² + q² = 0.82; q² equals q only when q is 0 or 1.",
  ["2pq = 2p(1 - p), maximum at p = 0.5", "Maximum value = 2 x 0.5 x 0.5 = 0.5",
   "Counter-examples rule out the other options"],
  "Hardy-Weinberg Principle",
  at="C", correct="The frequency of heterozygotes (2pq) can never exceed 0.5",
  wrong=["The frequency of genotype AA is always greater than that of genotype Aa",
         "The frequency of heterozygotes is always greater than the combined frequency of the two homozygotes",
         "The frequency of genotype aa is always equal to the frequency of allele a"],
  why="At p = 0.5, AA (0.25) is less than Aa (0.5); at p = 0.9, heterozygotes (0.18) are fewer than homozygotes "
      "(0.82); q² equals q only when q is 0 or 1.", secs=75, vb=RECOMPUTED)
