
# ================================================================ Biotechnology and its Applications (4/6/4)
Z(BTA, "Bt crops and RNAi", B, D,
  "Although the Green Revolution succeeded in tripling the food supply, NCERT says the increased yields were only "
  "partly due to improved crop varieties. What were they MAINLY due to?",
  "Green Revolution and its limits",
  "NCERT: although the Green Revolution succeeded in tripling the food supply, it was not enough to feed the growing "
  "human population. Increased yields have partly been due to the use of improved crop varieties, but mainly due to "
  "the use of better management practices and use of agrochemicals (fertilisers and pesticides).",
  ["Partly: improved crop varieties", "Mainly: better management practices + agrochemicals"],
  "Biotechnological Applications in Agriculture",
  at="D", correct="Better management practices and the use of agrochemicals (fertilisers and pesticides)",
  wrong=["Genetically modified crops such as Bt cotton", "Organic agriculture alone",
         "RNA interference against crop pests"],
  why="Bt crops and RNAi are genetically engineered approaches that NCERT presents as a further option after the "
      "Green Revolution; organic agriculture is a separate option, not the main reason for those yields.", secs=25)

Z(BTA, "Gene therapy", B, D,
  "Adenosine deaminase (ADA) deficiency was the disorder treated in the first clinical gene therapy. According to "
  "NCERT, what causes this disorder?",
  "Cause of ADA deficiency",
  "NCERT: the first clinical gene therapy was given in 1990 to a 4-year-old girl with adenosine deaminase (ADA) "
  "deficiency. This enzyme is crucial for the immune system to function. The disorder is caused due to the "
  "deletion of the gene for adenosine deaminase.",
  ["ADA crucial for the immune system", "Disorder caused by deletion of the ADA gene"],
  "Gene Therapy",
  at="A", correct="Deletion of the gene for adenosine deaminase",
  wrong=["Infection of lymphocytes by a retrovirus", "Excess production of adenosine deaminase",
         "Insertion of a Bt toxin gene into lymphocytes"],
  why="A retrovirus is the disarmed vector used in the therapy, not the cause; the disorder is a lack, not an "
      "excess, of the enzyme; and Bt toxin genes are used in crops, not linked to ADA deficiency.", secs=20)

Z(BTA, "Bt crops and RNAi", B, STP,
  SP("For farmers in the developing world, agrochemicals are often too expensive.",
     "Further increases in yield with existing varieties are not possible using conventional breeding."),
  "Why genetically engineered crops",
  "NCERT: for farmers in the developing world, agrochemicals are often too expensive, and further increases in "
  "yield with existing varieties are not possible using conventional breeding. NCERT then asks whether any "
  "alternative path exists that genetics could use to increase yields, and turns to genetically modified crops.",
  ["Statement I: true", "Statement II: true"],
  "Biotechnological Applications in Agriculture", ans="A",
  why="Both statements are NCERT's own reasons for looking beyond the Green Revolution, so every option calling "
      "either false is wrong.", secs=25)

Z(BTA, "Transgenic animals", B, ASR,
  AR("Transgenic animals have been used to produce human α-1-antitrypsin, a protein used to treat emphysema.",
     "Over 95 per cent of all existing transgenic animals are mice."),
  "Transgenic animals",
  "NCERT: although transgenic rats, rabbits, pigs, sheep, cows and fish have been produced, over 95 per cent of all "
  "existing transgenic animals are mice. Separately, under biological products, NCERT notes that transgenic "
  "animals have been used to produce human protein (α-1-antitrypsin) used to treat emphysema. Both are true, but "
  "how common transgenic mice are does not explain why transgenic animals can make this protein.",
  ["A: true", "R: true", "R is a count of transgenic species, unrelated to A"],
  "Transgenic Animals", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; the share of mice among "
      "transgenic animals says nothing about producing α-1-antitrypsin, so R is not the explanation.", secs=30)

Z(BTA, "Bt crops and RNAi", I, MAT,
  ML(("way in which genetic modification has been useful", "NCERT detail"),
     ["Tolerance to abiotic stresses", "Pest-resistant crops", "Increased efficiency of mineral usage",
      "Enhanced nutritional value of food"],
     ["Vitamin 'A' enriched rice", "Prevents early exhaustion of the fertility of the soil",
      "Cold, drought, salt and heat", "Reduced reliance on chemical pesticides"]),
  "Uses of genetically modified plants",
  "NCERT: genetic modification has (i) made crops more tolerant to abiotic stresses (cold, drought, salt, heat); "
  "(ii) reduced reliance on chemical pesticides (pest-resistant crops); (iii) helped to reduce post-harvest losses; "
  "(iv) increased efficiency of mineral usage by plants, which prevents early exhaustion of the fertility of the "
  "soil; and (v) enhanced the nutritional value of food, e.g. vitamin 'A' enriched rice.",
  ["A -> III", "B -> IV", "C -> II", "D -> I"],
  "Biotechnological Applications in Agriculture",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "I", "B": "IV", "C": "II", "D": "III"}]),
  why="Cold, drought, salt and heat are abiotic stresses, not pests; soil fertility is linked to mineral usage, "
      "not to pest resistance; and vitamin A rice is an example of better nutrition, not of stress tolerance.",
  secs=45)

Z(BTA, "Biosafety, biopiracy and patents", I, MUL,
  MS("Which of the following statements are correct according to NCERT's discussion of bio-resources and patents?",
     ["Traditional knowledge related to bio-resources can be exploited to develop modern applications.",
      "Attempts have been made to patent uses, products and processes based on Indian traditional herbal "
      "medicines, e.g. turmeric and neem.",
      "Basmati rice is distinct for its unique aroma and flavour.",
      "Industrialised nations are rich in biodiversity and traditional knowledge, but financially poor.",
      "The developing and under-developed world is rich in biodiversity and traditional knowledge related to "
      "bio-resources."]),
  "Bio-resources and patents",
  "NCERT: traditional knowledge related to bio-resources can be exploited to develop modern applications (and can "
  "save time, effort and expenditure during their commercialisation). Basmati rice is distinct for its unique aroma "
  "and flavour. Attempts have been made to patent uses, products and processes based on Indian traditional herbal medicines, e.g. turmeric and neem. The "
  "industrialised nations are rich financially but poor in biodiversity and traditional knowledge, whereas the "
  "developing and under-developed world is rich in biodiversity and traditional knowledge related to "
  "bio-resources.",
  ["(a) true", "(b) true", "(c) true", "(d) false - reversed", "(e) true"],
  "Ethical Issues",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="(d) reverses NCERT's contrast between industrialised and developing nations, so every option with (d) is "
      "wrong; the correct option keeps the other four NCERT statements.", secs=45)

Z(BTA, "Bt crops and RNAi", I, D,
  "According to NCERT, which are the three options that can be thought of for increasing food production?",
  "Options for increasing food production",
  "NCERT: let us take a look at the three options that can be thought of for increasing food production: (i) "
  "agro-chemical based agriculture; (ii) organic agriculture; and (iii) genetically engineered crop-based "
  "agriculture.",
  ["Agro-chemical based agriculture", "Organic agriculture", "Genetically engineered crop-based agriculture"],
  "Biotechnological Applications in Agriculture",
  at="A", correct="Agro-chemical based agriculture, organic agriculture and genetically engineered crop-based "
                  "agriculture",
  wrong=["Agro-chemical based agriculture, shifting cultivation and gene therapy",
         "Organic agriculture, biopiracy and transgenic animals",
         "Genetically engineered crops, MTP and organic agriculture"],
  why="Shifting cultivation is not one of NCERT's three options, gene therapy and MTP are medical procedures, and "
      "biopiracy and transgenic animals are not ways of growing more food.", secs=25)

Z(BTA, "Transgenic animals", I, ASR,
  AR("Rosie produced milk containing human α-lactalbumin, which was nutritionally a more balanced product for "
     "human babies than natural cow milk.",
     "Rosie was the first transgenic sheep, produced in 1997."),
  "Rosie",
  "NCERT: in 1997, the first transgenic COW, Rosie, produced human protein-enriched milk (2.4 grams per litre). The "
  "milk contained the human alpha-lactalbumin and was nutritionally a more balanced product for human babies than "
  "natural cow milk. A is true; R is false because Rosie was a cow.",
  ["A: true", "R: false - Rosie was a cow"],
  "Transgenic Animals", ans="C",
  why="R calls Rosie a sheep, so options treating R as true are wrong; A is NCERT's description of Rosie's milk, so "
      "'A is false' is wrong.", secs=30)

Z(BTA, "Biosafety, biopiracy and patents", I, STP,
  SP("According to NCERT, genetic modification gives fully predictable results, so genetically modified "
     "organisms can be introduced into any ecosystem without regulation.",
     "Biopiracy covers the use of bio-resources not only by multinational companies but also by other "
     "organisations, when it is done without proper authorisation and without compensatory payment."),
  "Regulation of GM organisms and the scope of biopiracy",
  "NCERT: the manipulation of living organisms cannot go on without regulation, and genetic modification of "
  "organisms can have UNPREDICTABLE results when such organisms are introduced into the ecosystem, so Statement I is "
  "false. Biopiracy is the use of bio-resources by multinational companies and other organisations without proper "
  "authorisation from the countries and people concerned and without compensatory payment, so Statement II is true.",
  ["Statement I: false - results can be unpredictable, and regulation is needed",
   "Statement II: true - 'multinational companies and other organisations'"],
  "Ethical Issues", ans="D",
  why="Statement I reverses NCERT's warning about unpredictable results, so options calling it true are wrong; "
      "Statement II is NCERT's definition of biopiracy, so options calling it false are wrong.", secs=30)

Z(BTA, "Biosafety, biopiracy and patents", I, D,
  "According to NCERT, the use of genetically modified organisms for public services (as food and medicine "
  "sources) has also created problems. When did these problems arise?",
  "GM organisms and patents",
  "NCERT: genetic modification of organisms can have unpredictable results when such organisms are introduced into "
  "the ecosystem. Moreover, the use of such organisms for public services (as food and medicine sources) has also "
  "created problems when patents are granted for the same.",
  ["Public-service use of GM organisms", "-> problems when patents are granted for the same"],
  "Ethical Issues",
  at="B", correct="When patents were granted for the same",
  wrong=["When the organisms were grown in bioreactors", "When their genes were amplified by PCR",
         "When their DNA was separated by gel electrophoresis"],
  why="Bioreactors, PCR and gel electrophoresis are laboratory and production tools; NCERT links the problems of "
      "public-service use of GM organisms to the granting of patents.", secs=25)

Z(BTA, "Human insulin", A, MUL,
  MS("Which of the following combinations of the DNA used, the host or recipient, and the purpose are correctly "
     "given, according to NCERT's examples?",
     ["cry genes of Bacillus thuringiensis - cotton plant - protection against bollworms",
      "Nematode-specific genes producing sense and anti-sense RNA - tobacco plant - protection against "
      "Meloidegyne incognitia",
      "Functional ADA cDNA - the patient's lymphocytes - treatment of ADA deficiency",
      "DNA sequences for chains A and B of insulin - plasmids of E. coli - production of human insulin",
      "Genes for human α-lactalbumin - E. coli - production of vitamin A enriched rice"]),
  "Applications compared",
  "NCERT: cry genes from Bacillus thuringiensis expressed in cotton control the cotton bollworms; nematode-specific "
  "genes introduced into tobacco (with Agrobacterium vectors) produce sense and anti-sense RNA that silence a "
  "nematode mRNA; functional ADA cDNA is introduced into the patient's lymphocytes (using a retroviral vector); "
  "and Eli Lilly introduced DNA sequences for chains A and B into plasmids of E. coli to produce insulin chains. "
  "Human α-lactalbumin was in the milk of the transgenic cow Rosie, and vitamin A enriched rice is golden rice.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - mixes Rosie's protein with golden rice"],
  "Biotechnological Applications in Agriculture; Genetically Engineered Insulin; Gene Therapy",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (e) only", "(b), (d) and (e) only"],
  why="(e) joins the human protein of Rosie's milk to E. coli and to golden rice, none of which matches NCERT, so "
      "every option containing (e) is wrong; (a)-(d) are all correct.", secs=60)

Z(BTA, "Gene therapy", A, MAT,
  ML(("approach", "what actually protects the plant or treats the patient"),
     ["Bt cotton", "RNAi-based tobacco resistant to Meloidegyne incognitia",
      "Gene therapy for ADA deficiency using lymphocytes", "Enzyme replacement therapy for ADA deficiency"],
     ["Functional ADA cDNA delivered into lymphocytes by a retroviral vector",
      "A protein toxin, inactive as a protoxin until activated in the insect gut",
      "Functional ADA enzyme given to the patient by injection",
      "dsRNA formed from complementary sense and anti-sense RNA, silencing a specific mRNA of the parasite"]),
  "What each application delivers",
  "NCERT: Bt cotton makes the Bt toxin protein, which exists as an inactive protoxin and becomes active in the "
  "alkaline gut of the insect. In the RNAi tobacco, the introduced DNA produced both sense and anti-sense RNA; these "
  "complementary RNAs formed dsRNA that silenced a specific mRNA of the nematode. In gene therapy for ADA "
  "deficiency, a functional ADA cDNA is introduced into the patient's cultured lymphocytes using a retroviral "
  "vector. In enzyme replacement therapy, functional ADA is given to the patient by injection.",
  ["A -> II", "B -> IV", "C -> I", "D -> III"],
  "Biotechnological Applications in Agriculture; Gene Therapy",
  at="C", match=({"A": "II", "B": "IV", "C": "I", "D": "III"},
                 [{"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="Bt cotton works through a protein and the RNAi tobacco through dsRNA, so swapping them is wrong; gene therapy "
      "delivers the ADA gene (cDNA), whereas enzyme replacement injects the enzyme itself, so swapping C and D is "
      "wrong; lymphocyte gene therapy does not involve dsRNA.", secs=50)

Z(BTA, "Bt crops and RNAi", A, ASR,
  AR("Bacillus thuringiensis is killed by its own Bt toxin when the toxin is present in large amounts in the "
     "bacterium.",
     "In the bacterium, the Bt toxin protein exists as an inactive protoxin."),
  "Why the Bt toxin spares the bacterium",
  "NCERT: the Bt toxin protein exists as an inactive protoxin in the bacterium; once an insect ingests it, it is "
  "converted into an active form of toxin due to the alkaline pH of the gut, which solubilises the crystals. "
  "Because it is inactive in the bacterium, the toxin does not kill Bacillus thuringiensis, so A is false while R "
  "is true.",
  ["A: false - the protoxin is inactive in the bacterium", "R: true"],
  "Biotechnological Applications in Agriculture", ans="D",
  why="A contradicts the very fact stated in R, so options calling A true are wrong; R is NCERT's own statement, so "
      "'A is false but R is true' is the answer.", secs=35)

Z(BTA, "Bt crops and RNAi", A, D,
  "How many of the following crops does NCERT name as plants in which the Bt toxin gene has been expressed to "
  "provide resistance to insects?\n\nCotton, corn, rice, tomato, potato, soyabean, wheat, mustard",
  "Bt crops named in NCERT",
  "NCERT: the Bt toxin gene has been cloned from the bacteria and expressed in plants to provide resistance to "
  "insects without the need for insecticides, in effect creating a bio-pesticide; examples are Bt cotton, Bt corn, "
  "rice, tomato, potato and soyabean. Wheat and mustard are not named.",
  ["Named: cotton, corn, rice, tomato, potato, soyabean = 6", "Not named: wheat, mustard"],
  "Biotechnological Applications in Agriculture",
  at="B", correct="Six",
  wrong=["Five", "Seven", "Eight"],
  why="Five omits one of NCERT's six examples (often soyabean or rice); seven or eight add wheat and/or mustard, "
      "which NCERT does not name.", secs=40)
