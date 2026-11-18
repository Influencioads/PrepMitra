

# ================================================================ Human Health and Disease (7/9/7)
Z(HHD, "Immunity and vaccines", B, D,
  "Which of the following is NOT among the cells that NCERT lists as the cellular barriers of innate immunity?",
  "Cellular barriers of innate immunity",
  "NCERT: certain types of leukocytes of our body like polymorpho-nuclear leukocytes (PMNL - neutrophils), monocytes "
  "and natural killer cells (a type of lymphocyte) in the blood, as well as macrophages in tissues, can phagocytose "
  "and destroy microbes; these are the cellular barriers of innate immunity. B-lymphocytes belong to acquired "
  "immunity: they produce antibodies (humoral immune response).",
  ["Cellular barriers: neutrophils (PMNL), monocytes, NK cells, macrophages",
   "B-lymphocytes: acquired immunity (antibodies)"],
  "Immunity",
  at="A", correct="B-lymphocytes",
  wrong=["Neutrophils (PMNL)", "Natural killer cells", "Macrophages"],
  why="Neutrophils, natural killer cells and macrophages are all named by NCERT as phagocytic cells forming the "
      "cellular barrier of innate immunity.", secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "The thymus is quite large at the time of birth but keeps reducing in size with age. According to NCERT, it "
  "reduces to a very small size by the time:",
  "Thymus and age",
  "NCERT: the thymus is a lobed organ located near the heart and beneath the breastbone. It is quite large at the "
  "time of birth but keeps reducing in size with age, and by the time puberty is attained it reduces to a very "
  "small size.",
  ["Large at birth -> reduces with age -> very small by puberty"],
  "Immunity",
  at="C", correct="Puberty is attained",
  wrong=["The child is one year old", "Old age (about 60 years) is reached", "Menopause sets in"],
  why="NCERT names puberty as the stage by which the thymus becomes very small; the other stages are not given.",
  secs=20)

Z(HHD, "Pathogens and diseases", B, STP,
  SP("Ascaris, the common round worm, is an intestinal parasite that causes ascariasis.",
     "Wuchereria (W. bancrofti and W. malayi), the filarial worms, cause filariasis."),
  "Pathogenic helminths",
  "NCERT: many helminths are pathogenic for man. Ascaris, the common round worm, and Wuchereria, the filarial worm, "
  "are some of them. Ascaris, an intestinal parasite, causes ascariasis. Wuchereria (W. bancrofti and W. malayi), "
  "the filarial worms, cause a slowly developing chronic inflammation of the organs in which they live for many "
  "years, usually the lymphatic vessels of the lower limbs; the disease is called elephantiasis or filariasis.",
  ["Statement I: true", "Statement II: true"],
  "Common Diseases in Humans", ans="A",
  why="Both statements are NCERT's own descriptions, so every option calling one of them false is wrong.", secs=25)

Z(HHD, "Pathogens and diseases", B, ASR,
  AR("Typhoid fever can be confirmed by the Widal test.",
     "Salmonella typhi generally enters the small intestine through contaminated food and water."),
  "Typhoid: diagnosis and entry",
  "NCERT: Salmonella typhi is the pathogenic bacterium that causes typhoid fever in human beings. It generally "
  "enters the small intestine through food and water contaminated with it and migrates to other organs through "
  "blood. Typhoid fever could be confirmed by the Widal test. Both statements are true, but the route by which the "
  "pathogen enters the body does not explain how the disease is confirmed by a test.",
  ["A: true", "R: true", "R is about entry, A is about diagnosis -> not the explanation"],
  "Common Diseases in Humans", ans="B",
  why="R describes how the infection is acquired, which is unrelated to the diagnostic test in A, so 'R is the "
      "correct explanation' is wrong; both are NCERT statements, so the options with a false statement are wrong.",
  secs=30)

Z(HHD, "Pathogens and diseases", B, MAT,
  ML(("disease", "vector, carrier or mode of spread described in NCERT"),
     ["Malaria", "Dengue", "Amoebiasis", "Ringworm"],
     ["Houseflies acting as mechanical carriers", "Using towels, clothes or even the comb of infected individuals",
      "Female Anopheles mosquito", "Aedes mosquitoes"]),
  "How some diseases spread",
  "NCERT: malaria is transmitted by the bite of the infected female Anopheles mosquito; dengue and chikungunya are "
  "vector-borne diseases spread by Aedes mosquitoes; in amoebiasis, houseflies act as mechanical carriers and "
  "transmit the parasite from the faeces of infected persons to food; ringworms are generally acquired from soil or "
  "by using towels, clothes or even the comb of infected individuals.",
  ["A -> III", "B -> IV", "C -> I", "D -> II"],
  "Common Diseases in Humans",
  at="D", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "II", "C": "III", "D": "IV"}]),
  why="Swapping the two mosquitoes confuses the vectors of malaria (Anopheles) and dengue (Aedes); houseflies carry "
      "the amoebiasis parasite, not ringworm; the last code mismatches every disease.", secs=40)

Z(HHD, "Pathogens and diseases", B, D,
  "Which of the following pairs of human diseases are BOTH caused by protozoans?",
  "Protozoan diseases",
  "NCERT: malaria is caused by Plasmodium (P. vivax, P. malariae, P. falciparum), a tiny protozoan; amoebiasis "
  "(amoebic dysentery) is caused by Entamoeba histolytica, a protozoan parasite of the large intestine. Filariasis "
  "and ascariasis are caused by helminths, and typhoid by a bacterium.",
  ["Malaria: Plasmodium (protozoan)", "Amoebiasis: Entamoeba histolytica (protozoan)"],
  "Common Diseases in Humans",
  at="B", correct="Malaria and amoebiasis",
  wrong=["Malaria and filariasis", "Amoebiasis and ascariasis", "Typhoid and amoebiasis"],
  why="Filariasis (Wuchereria) and ascariasis (Ascaris) are helminth diseases, and typhoid is caused by the "
      "bacterium Salmonella typhi, so each other pair contains a non-protozoan disease.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Which of the following sets gives the features of the withdrawal syndrome, as described in NCERT, that appears "
  "when the regular dose of drugs or alcohol is abruptly discontinued?",
  "Withdrawal syndrome",
  "NCERT: dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal syndrome if "
  "the regular dose of drugs/alcohol is abruptly discontinued. This is characterised by anxiety, shakiness, nausea "
  "and sweating, which may be relieved when use is resumed again.",
  ["Withdrawal syndrome: anxiety, shakiness, nausea, sweating"],
  "Drugs and Alcohol Abuse",
  at="C", correct="Anxiety, shakiness, nausea and sweating",
  wrong=["A sense of euphoria, increased energy and hallucinations", "Reckless behaviour, vandalism and violence",
         "Hair loss and anaemia"],
  why="Euphoria, increased energy and (in excess) hallucinations are effects of cocaine; reckless behaviour, "
      "vandalism and violence are the immediate adverse effects of drug abuse; hair loss and anaemia are side effects "
      "of chemotherapeutic drugs.", secs=30)

Z(HHD, "Immunity and vaccines", I, D,
  "According to NCERT, which organ(s) provide the micro-environments for the development and maturation of "
  "T-lymphocytes?",
  "Primary lymphoid organs and T-lymphocytes",
  "NCERT: the bone marrow is the main lymphoid organ where all blood cells including lymphocytes are produced. The "
  "thymus is a lobed organ located near the heart beneath the breastbone. Both bone marrow and thymus provide "
  "micro-environments for the development and maturation of T-lymphocytes.",
  ["NCERT: 'Both bone marrow and thymus provide micro-environments' for T-lymphocyte development and maturation"],
  "Immunity",
  at="D", correct="Both the bone marrow and the thymus",
  wrong=["The thymus only", "The spleen and the lymph nodes", "The bone marrow only"],
  why="NCERT names both primary lymphoid organs, so either one alone is incomplete; the spleen and lymph nodes are "
      "secondary lymphoid organs, to which mature lymphocytes migrate.", secs=30)

Z(HHD, "Pathogens and diseases", I, D,
  "How many of the following diseases are caused by helminths?\n\n"
  "Ascariasis, filariasis, amoebiasis, ringworm, malaria, pneumonia",
  "Helminth diseases",
  "NCERT: Ascaris (common round worm) causes ascariasis and Wuchereria (filarial worm) causes filariasis; both are "
  "helminths. Amoebiasis (Entamoeba histolytica) and malaria (Plasmodium) are protozoan diseases, ringworm is "
  "caused by fungi, and pneumonia by bacteria (Streptococcus pneumoniae, Haemophilus influenzae).",
  ["Helminths: ascariasis, filariasis = 2", "Protozoa: amoebiasis, malaria", "Fungi: ringworm",
   "Bacteria: pneumonia"],
  "Common Diseases in Humans",
  at="A", correct="Two",
  wrong=["One", "Three", "Four"],
  why="One leaves out either ascariasis or filariasis; three or four wrongly add ringworm (a fungal disease) or the "
      "protozoan diseases, amoebiasis and malaria.", secs=35)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("Lymph nodes are secondary lymphoid organs.",
     "In the lymph nodes, immature lymphocytes differentiate into antigen-sensitive lymphocytes."),
  "Primary versus secondary lymphoid organs",
  "NCERT: the primary lymphoid organs are the bone marrow and thymus, where immature lymphocytes differentiate into "
  "antigen-sensitive lymphocytes. After maturation the lymphocytes migrate to secondary lymphoid organs like the "
  "spleen, lymph nodes, tonsils, Peyer's patches of the small intestine and appendix, which provide the sites for "
  "interaction of lymphocytes with the antigen. So A is true, and R describes a primary lymphoid organ, not a lymph "
  "node.",
  ["A: true - lymph nodes are secondary", "R: false - differentiation occurs in bone marrow and thymus"],
  "Immunity", ans="C",
  why="R attributes to lymph nodes the role of the primary lymphoid organs, so options calling R true are wrong; A "
      "is NCERT's own classification, so 'A is false' is wrong.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Cannabinoids are obtained from the inflorescences of the plant Cannabis sativa.",
     "The flower tops, leaves and resin of the cannabis plant are used in various combinations to produce "
     "marijuana, hashish, charas and ganja."),
  "Cannabinoids",
  "NCERT: cannabinoids are a group of chemicals which interact with cannabinoid receptors present principally in the "
  "brain. Natural cannabinoids are obtained from the inflorescences of the plant Cannabis sativa. The flower tops, "
  "leaves and the resin of the cannabis plant are used in various combinations to produce marijuana, hashish, "
  "charas and ganja.",
  ["Statement I: true", "Statement II: true"],
  "Drugs and Alcohol Abuse", ans="A",
  why="Both statements are NCERT's own, so every option calling one of them false is wrong.", secs=30)

Z(HHD, "Cancer", I, MAT,
  ML(("cancer detection or treatment", "NCERT description"),
     ["Detection of leukaemia", "Radiation therapy", "Chemotherapy", "Immunotherapy"],
     ["Biological response modifiers such as alpha-interferon activate the immune system",
      "Most of the drugs have side effects like hair loss and anaemia",
      "Tumour cells are irradiated lethally, taking proper care of the surrounding normal tissues",
      "Blood and bone marrow tests for increased cell counts"]),
  "Detection and treatment of cancer",
  "NCERT: in the case of leukaemia, blood and bone marrow tests for increased cell counts are done. In radiotherapy, "
  "tumour cells are irradiated lethally, taking proper care of the normal tissues surrounding the tumour mass. "
  "Several chemotherapeutic drugs are used to kill cancerous cells, and the majority have side effects like hair "
  "loss and anaemia. Patients are given substances called biological response modifiers such as alpha-interferon, "
  "which activate their immune system and help in destroying the tumour.",
  ["A -> IV", "B -> III", "C -> II", "D -> I"],
  "Cancer",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "I", "B": "II", "C": "IV", "D": "III"}]),
  why="Irradiation is a treatment, not the test for leukaemia, so swapping A and B is wrong; alpha-interferon is the "
      "basis of immunotherapy, while hair loss and anaemia are chemotherapy side effects, so swapping C and D is "
      "wrong; the last code mismatches every row.", secs=45)

Z(HHD, "Immunity and vaccines", I, MUL,
  MS("Which of the following are PHYSIOLOGICAL barriers of innate immunity, according to NCERT?",
     ["Acid in the stomach", "Saliva in the mouth", "Tears from the eyes",
      "Mucus coating of the epithelium lining the respiratory tract",
      "Interferons secreted by virus-infected cells"]),
  "Kinds of innate barriers",
  "NCERT: innate immunity has four types of barriers. Physical barriers: skin, and the mucus coating of the "
  "epithelium lining the respiratory, gastrointestinal and urogenital tracts. Physiological barriers: acid in the "
  "stomach, saliva in the mouth, tears from the eyes - all prevent microbial growth. Cellular barriers: PMNL "
  "(neutrophils), monocytes, natural killer cells and macrophages. Cytokine barriers: interferons secreted by "
  "virus-infected cells, which protect non-infected cells from further viral infection.",
  ["Physiological: (a), (b), (c)", "(d): physical barrier", "(e): cytokine barrier"],
  "Immunity",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(a) and (c) only", "(a), (b), (c) and (e) only"],
  why="The mucus coating of epithelia is a physical barrier and interferons are a cytokine barrier, so options with "
      "(d) or (e) are wrong; '(a) and (c) only' leaves out saliva, which NCERT lists as a physiological barrier.",
  secs=45)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Adolescence is accompanied by several biological and behavioural changes and is a very vulnerable phase of "
     "mental and psychological development of an individual.",
     "According to NCERT, adolescence may be thought of as the period between 18 and 25 years of age."),
  "Adolescence",
  "NCERT: adolescence means both 'a period' and 'a process' during which a child becomes mature in terms of his/her "
  "attitudes and beliefs for effective participation in society. The period between 12-18 years of age may be "
  "thought of as the adolescence period. Adolescence is accompanied by several biological and behavioural changes; "
  "it is thus a very vulnerable phase of mental and psychological development.",
  ["Statement I: true", "Statement II: false - NCERT gives 12-18 years"],
  "Drugs and Alcohol Abuse", ans="C",
  why="Statement II gives the wrong age range (NCERT: 12-18 years), so options calling it true are wrong; Statement I "
      "is NCERT's description, so 'both false' and 'Statement I false' are wrong.", secs=30)

Z(HHD, "Pathogens and diseases", I, ASR,
  AR("Ringworm is generally acquired by inhaling droplets or aerosols released by an infected person.",
     "Ringworm is caused by fungi belonging to the genera Microsporum, Trichophyton and Epidermophyton."),
  "Ringworm: cause and spread",
  "NCERT: many fungi belonging to the genera Microsporum, Trichophyton and Epidermophyton are responsible for "
  "ringworms, one of the most common infectious diseases in man. Ringworms are generally acquired from soil or by "
  "using towels, clothes or even the comb of infected individuals. Inhalation of droplets/aerosols is how pneumonia "
  "spreads. So A is false and R is true.",
  ["A: false - acquired from soil or shared towels, clothes, combs", "R: true"],
  "Common Diseases in Humans", ans="D",
  why="A describes the spread of pneumonia, not ringworm, so all options with A true are wrong; R is NCERT's list of "
      "ringworm fungi, so 'A is false but R is true' is correct.", secs=30)

Z(HHD, "HIV and AIDS", I, ASR,
  AR("Individuals who require repeated blood transfusions are at high risk of getting HIV infection.",
     "HIV can be transmitted by transfusion of contaminated blood and blood products."),
  "High-risk groups for HIV",
  "NCERT: HIV is transmitted generally by sexual contact with an infected person, by transfusion of contaminated "
  "blood and blood products, by sharing infected needles, and from an infected mother to her child through the "
  "placenta. So, people at high risk include individuals who require repeated blood transfusions. Since each "
  "transfusion is a possible route of entry, R directly explains A.",
  ["Route: contaminated blood transfusion (R)", "Repeated transfusions -> repeated exposure -> high risk (A)"],
  "AIDS", ans="A",
  why="R gives the very route that makes repeated transfusion risky, so 'R is not the explanation' is wrong; both "
      "statements are NCERT's own, so the options with a false statement are wrong.", secs=30)

Z(HHD, "Pathogens and diseases", A, D,
  "Which option arranges the following events in the life cycle of Plasmodium in the correct order, according to "
  "NCERT?\n\n(P) The parasites multiply within the liver cells of the human\n(Q) Sporozoites enter the human body "
  "through the bite of an infected female Anopheles mosquito\n(R) The parasites attack the red blood cells, which "
  "rupture and release haemozoin\n(S) A female Anopheles takes up gametocytes with the blood meal, and fertilisation "
  "and development take place in its stomach\n(T) Sporozoites formed in the mosquito are stored in its salivary "
  "glands",
  "Life cycle of Plasmodium",
  "NCERT: Plasmodium enters the human body as sporozoites (infectious form) through the bite of an infected female "
  "Anopheles mosquito (Q). The parasites initially multiply within the liver cells (P) and then attack the red "
  "blood cells, resulting in their rupture and release of haemozoin (R). The sexual stages (gametocytes) develop in "
  "the red blood cells; when a female Anopheles bites an infected person, these enter the mosquito, where "
  "fertilisation and development take place in the stomach (S). The parasites multiply to form sporozoites that are "
  "stored in the salivary glands (T), ready for the next bite.",
  ["Q -> P (liver) -> R (RBCs) -> S (mosquito stomach) -> T (salivary glands)"],
  "Common Diseases in Humans",
  at="D", correct="Q -> P -> R -> S -> T",
  wrong=["Q -> R -> P -> S -> T", "P -> Q -> R -> T -> S", "Q -> P -> R -> T -> S"],
  why="The parasites multiply in the liver before attacking RBCs, so R cannot precede P; sporozoites must enter "
      "before any multiplication in the human, so P cannot come first; sporozoites stored in the salivary glands are "
      "formed only after fertilisation in the mosquito, so T cannot precede S.", secs=60)

Z(HHD, "Drug and alcohol abuse", A, D,
  "Which one of the following sets of drug, source and usual mode of intake is entirely correct according to NCERT?",
  "Drugs: source and mode of intake",
  "NCERT: heroin (smack, diacetylmorphine) is obtained by acetylation of morphine, which is extracted from the latex "
  "of the poppy plant Papaver somniferum; it is generally taken by snorting and injection. Cannabinoids are obtained "
  "from the inflorescences of Cannabis sativa and are generally taken by inhalation and oral ingestion. Cocaine is "
  "obtained from the coca plant Erythroxylum coca, native to South America, and is usually snorted.",
  ["Cocaine: Erythroxylum coca, usually snorted", "Heroin: from morphine (poppy latex), snorting and injection",
   "Cannabinoids: Cannabis sativa inflorescences, inhalation and oral ingestion"],
  "Drugs and Alcohol Abuse",
  at="B", correct="Cocaine - Erythroxylum coca - usually snorted",
  wrong=["Heroin - inflorescences of Cannabis sativa - snorting and injection",
         "Heroin - acetylation of morphine from poppy latex - inhalation and oral ingestion",
         "Cannabinoids - latex of Papaver somniferum - inhalation and oral ingestion"],
  why="Heroin does not come from Cannabis; heroin is taken by snorting and injection, not by inhalation and oral "
      "ingestion; cannabinoids come from Cannabis sativa, not the poppy plant.", secs=50)

Z(HHD, "Pathogens and diseases", A, MUL,
  MS("Which of the following statements are true for BOTH malaria and filariasis, according to NCERT?",
     ["The disease is transmitted through an insect vector (a female mosquito).",
      "The pathogen is a protozoan.",
      "The most important preventive measure is to control or eliminate the vectors and their breeding places.",
      "The pathogen first multiplies within the liver cells of the human.",
      "The pathogen lives for many years in the lymphatic vessels of the lower limbs."]),
  "Malaria and filariasis compared",
  "NCERT: malaria is caused by Plasmodium, a protozoan, transmitted by the female Anopheles mosquito; the parasites "
  "first multiply within liver cells. Filariasis is caused by Wuchereria, a helminth (filarial worm), transmitted by "
  "the bite of female mosquito vectors; the worms live for many years in the lymphatic vessels of the lower limbs. "
  "In case of diseases such as malaria and filariasis that are transmitted through insect vectors, the most "
  "important measure is to control or eliminate the vectors and their breeding places.",
  ["(a), (c): true for both", "(b), (d): only malaria", "(e): only filariasis"],
  "Common Diseases in Humans",
  at="A", correct="(a) and (c) only",
  wrong=["(a), (b) and (c) only", "(a), (c) and (e) only", "(a), (b), (c) and (d) only"],
  why="Wuchereria is a helminth and does not multiply in the liver, so (b) and (d) apply only to malaria; Plasmodium "
      "does not live in lymphatic vessels, so (e) applies only to filariasis.", secs=60)

Z(HHD, "Pathogens and diseases", A, STP,
  SP("Typhoid and amoebiasis are both acquired through contaminated food or water, but it is for amoebiasis that "
     "NCERT names houseflies as mechanical carriers of the pathogen.",
     "Pneumonia and the common cold both infect the alveoli of the lungs."),
  "Comparing modes of infection",
  "NCERT: Salmonella typhi enters the small intestine through food and water contaminated with it. In amoebiasis, "
  "houseflies act as mechanical carriers and serve to transmit the parasite from the faeces of infected persons to "
  "food and food products. Pneumonia-causing bacteria infect the alveoli (air-filled sacs) of the lungs, whereas the "
  "rhinoviruses of the common cold infect the nose and respiratory passage but not the lungs.",
  ["Statement I: true", "Statement II: false - common cold spares the lungs"],
  "Common Diseases in Humans", ans="C",
  why="Statement II is false because the common cold does not infect the lungs, so options calling it true are "
      "wrong; Statement I is consistent with NCERT, so 'both false' and 'Statement I false' are wrong.", secs=50)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Hepatitis B vaccine is produced from yeast using recombinant DNA technology, which allows its large-scale "
     "production.",
     "Hepatitis B can be transmitted by sharing injection needles and syringes with infected persons."),
  "Recombinant hepatitis B vaccine",
  "NCERT: recombinant DNA technology has allowed the production of antigenic polypeptides of pathogens in bacteria "
  "or yeast, so vaccine production on a large scale became possible; for example, hepatitis B vaccine produced from "
  "yeast. Separately, NCERT notes that hepatitis B (like HIV) is transmitted by sharing infected needles and "
  "syringes. Both are true, but the way the disease spreads has nothing to do with how the vaccine is "
  "manufactured.",
  ["A: true", "R: true", "R concerns transmission, A concerns vaccine production -> not the explanation"],
  "Immunity; Drugs and Alcohol Abuse", ans="B",
  why="The route of transmission does not explain the method of vaccine production, so 'R is the correct "
      "explanation' is wrong; both statements are NCERT's, so options with a false statement are wrong.", secs=40)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("Which of the following statements about innate and acquired immunity are correct according to NCERT?",
     ["Innate immunity is a non-specific type of defence that is present at the time of birth.",
      "Acquired immunity is pathogen-specific and is characterised by memory.",
      "Memory-based acquired immunity evolved in higher vertebrates.",
      "Interferons secreted by virus-infected cells are a part of acquired immunity.",
      "The humoral immune response of B-lymphocytes and the cell-mediated immunity of T-lymphocytes are both "
      "responses of acquired immunity."]),
  "Innate and acquired immunity",
  "NCERT: innate immunity is a non-specific type of defence present at the time of birth, accomplished by physical, "
  "physiological, cellular and cytokine barriers (interferons form the cytokine barrier). Acquired immunity is "
  "pathogen-specific and characterised by memory; memory-based acquired immunity evolved in higher vertebrates. "
  "Within acquired immunity, B-lymphocytes give the humoral (antibody-mediated) immune response and T-lymphocytes "
  "mediate cell-mediated immunity.",
  ["(a), (b), (c), (e): true", "(d): false - interferons are a cytokine barrier of innate immunity"],
  "Immunity",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(a), (b), (c) and (d) only", "(b), (c), (d) and (e) only"],
  why="'(a), (b) and (c) only' omits (e), NCERT's two types of acquired immune response; interferons belong to the "
      "innate cytokine barrier, so any option with (d) is wrong.", secs=60)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("item", "time or duration given in NCERT"),
     ["Recurrence of chill and high fever in malaria", "Symptoms of the common cold",
      "Time-lag between HIV infection and appearance of AIDS symptoms", "Use of tobacco by human beings"],
     ["About 3-7 days", "More than 400 years", "Usually 5-10 years", "Every three to four days"]),
  "Time figures in Human Health and Disease",
  "NCERT: in malaria, haemozoin released from ruptured RBCs is responsible for the chill and high fever recurring "
  "every three to four days. The common cold symptoms usually last for 3-7 days. The time-lag between HIV infection "
  "and appearance of AIDS symptoms may vary from a few months to many years (usually 5-10 years). Tobacco has been "
  "used by human beings for more than 400 years.",
  ["A -> IV", "B -> I", "C -> III", "D -> II"],
  "Common Diseases in Humans; AIDS; Drugs and Alcohol Abuse",
  at="D", match=({"A": "IV", "B": "I", "C": "III", "D": "II"},
                 [{"A": "I", "B": "IV", "C": "III", "D": "II"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="Swapping A and B confuses the 3-4 day fever cycle of malaria with the 3-7 day duration of a cold; the HIV "
      "time-lag is years, not centuries; the last code mismatches three of the four rows.", secs=45)
