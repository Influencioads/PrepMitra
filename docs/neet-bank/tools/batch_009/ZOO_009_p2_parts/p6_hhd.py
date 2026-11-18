
# ================================================================ Human Health and Disease (6/9/6)
Z(HHD, "Drug and alcohol abuse", B, D,
  "According to NCERT, in which ways is tobacco used by human beings?",
  "Forms of tobacco use",
  "NCERT: tobacco has been used by human beings for more than 400 years. It is smoked, chewed or used as a snuff. "
  "Tobacco contains a large number of chemical substances, including nicotine, an alkaloid.",
  ["Smoked", "Chewed", "Used as a snuff"],
  "Drugs and Alcohol Abuse",
  at="A", correct="It is smoked, chewed or used as a snuff",
  wrong=["It is only smoked; chewing tobacco is not described",
         "It is taken only by intravenous injection",
         "It is used only as an ointment applied to the skin"],
  why="NCERT names chewing (linked to oral cancer) and snuff as well as smoking; injection is described for drugs "
      "like heroin, not tobacco; and NCERT does not mention tobacco ointments.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "In malaria, the chill and high fever recur every three to four days. According to NCERT, this is due to the "
  "release of a toxic substance called:",
  "Cause of malarial fever",
  "NCERT: Plasmodium multiplies within the liver cells and then attacks the red blood cells (RBCs), resulting in "
  "their rupture. The ruptured RBCs release a toxic substance, haemozoin, which is responsible for the chill and "
  "high fever recurring every three to four days.",
  ["Liver cells -> RBCs attacked and ruptured", "Haemozoin released -> chill and high fever every 3-4 days"],
  "Common Diseases in Humans",
  at="C", correct="Haemozoin",
  wrong=["Histamine", "Interferon", "Serotonin"],
  why="Histamine and serotonin are released from mast cells in allergy; interferons are proteins secreted by "
      "virus-infected cells that protect non-infected cells. None is the malarial toxin.", secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "According to NCERT, what has modern-day life style done that results in more and more children in the metro "
  "cities of India suffering from allergies and asthma?",
  "Life style and allergy",
  "NCERT: somehow, modern-day life style has resulted in lowering of immunity and more sensitivity to allergens; "
  "more and more children in metro cities of India suffer from allergies and asthma due to sensitiveness to the "
  "environment.",
  ["Modern life style -> lower immunity + more sensitivity to allergens", "-> allergies and asthma in children"],
  "Immunity (Allergies)",
  at="B", correct="It has lowered immunity and increased sensitivity to allergens",
  wrong=["It has made the thymus larger in children", "It has removed all allergens from the environment",
         "It has stopped the production of IgE antibodies"],
  why="NCERT says the thymus reduces in size with age and does not link it to life style; allergens such as dust "
      "and pollen remain in the environment; and IgE antibodies are what produce allergic reactions, so stopping "
      "them would reduce allergy, not increase it.", secs=25)

Z(HHD, "Immunity and vaccines", B, STP,
  SP("When the body encounters a pathogen for the first time, it produces a primary response of low intensity.",
     "A subsequent encounter with the same pathogen elicits a highly intensified secondary or anamnestic response."),
  "Primary and secondary immune responses",
  "NCERT: our body, when it encounters a pathogen for the first time, produces a response called the primary "
  "response, which is of low intensity. Subsequent encounter with the same pathogen elicits a highly intensified "
  "secondary or anamnestic response. This is ascribed to the fact that our body appears to have memory of the "
  "first encounter.",
  ["Statement I: true - primary response, low intensity", "Statement II: true - secondary (anamnestic), intensified"],
  "Immunity (Acquired Immunity)", ans="A",
  why="Both statements are NCERT's own, so every option calling either false is wrong.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, ASR,
  AR("Cocaine is commonly called coke or crack.",
     "Cocaine interferes with the transport of the neurotransmitter dopamine."),
  "Cocaine",
  "NCERT: coca alkaloid or cocaine is obtained from the coca plant Erythroxylum coca, native to South America. It "
  "interferes with the transport of the neurotransmitter dopamine. Cocaine, commonly called coke or crack, is "
  "usually snorted. Both statements are true, but the drug's street names have nothing to do with its action on "
  "dopamine.",
  ["A: true", "R: true", "R is its mode of action; A is its common name -> unrelated"],
  "Drugs and Alcohol Abuse", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; how cocaine acts on dopamine "
      "transport does not explain what it is commonly called, so R is not the explanation.", secs=25)

Z(HHD, "Pathogens and diseases", B, D,
  "Rhinoviruses cause the common cold, with nasal congestion and discharge, sore throat, hoarseness, cough, "
  "headache and tiredness. According to NCERT, these symptoms usually last for:",
  "Common cold",
  "NCERT: rhinoviruses infect the nose and respiratory passage but not the lungs. The common cold is characterised "
  "by nasal congestion and discharge, sore throat, hoarseness, cough, headache, tiredness, etc., which usually last "
  "for 3–7 days.",
  ["Rhinovirus -> nose and respiratory passage (not lungs)", "Symptoms usually last 3–7 days"],
  "Common Diseases in Humans",
  at="D", correct="3–7 days",
  wrong=["3–5 days", "5–10 years", "12–18 years"],
  why="3–5 days is the duration of menstrual flow; 5–10 years is the usual time-lag between HIV infection and "
      "AIDS symptoms; 12–18 years is NCERT's adolescence period.", secs=20)

Z(HHD, "Pathogens and diseases", I, MAT,
  ML(("disease", "feature in severe or chronic cases, as described in NCERT"),
     ["Typhoid", "Pneumonia", "Ascariasis", "Filariasis"],
     ["Lips and finger nails may turn grey to bluish in colour",
      "Intestinal perforation and death may occur",
      "Gross deformities, with the genital organs also often affected",
      "Blockage of the intestinal passage, with internal bleeding and anaemia"]),
  "Severe features of common diseases",
  "NCERT: in typhoid, intestinal perforation and death may occur in severe cases. In severe cases of pneumonia, "
  "the lips and finger nails may turn grey to bluish in colour. Symptoms of ascariasis include internal bleeding, "
  "muscular pain, fever, anaemia and blockage of the intestinal passage. In filariasis the worms cause chronic "
  "inflammation of the organs in which they live for many years; the genital organs are also often affected, "
  "resulting in gross deformities.",
  ["A typhoid -> II", "B pneumonia -> I", "C ascariasis -> IV", "D filariasis -> III"],
  "Common Diseases in Humans",
  at="D", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"}]),
  why="Bluish lips and nails reflect pneumonia's effect on the lungs, not typhoid; gross deformities belong to "
      "filariasis and intestinal blockage to the roundworm Ascaris; typhoid, not ascariasis, can cause intestinal "
      "perforation.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, MUL,
  MS("Which of the following does NCERT give as causes that motivate youth towards drug and alcohol use?",
     ["Curiosity, need for adventure and excitement, and experimentation",
      "The urge to escape facing problems and failures",
      "Stress from pressure to excel in academics or examinations",
      "The perception that it is 'cool' or progressive to smoke or use drugs or alcohol, promoted by television, "
      "movies, newspapers and the internet",
      "Avoiding undue peer pressure"]),
  "Why adolescents take to drugs",
  "NCERT: curiosity, need for adventure and excitement, and experimentation constitute common causes; children may "
  "also use drugs and alcohol to escape facing problems and failures; stress from pressure to excel in academics "
  "or examinations has played a significant role; the perception that it is 'cool' or progressive, promoted by "
  "television, movies, newspapers and the internet, is another factor; and unstable or unsupportive family "
  "structures and peer pressure also contribute. 'Avoiding undue peer pressure' is a PREVENTION measure.",
  ["(a)-(d): causes", "(e): a prevention measure, not a cause"],
  "Adolescence and Drug/Alcohol Abuse",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (e) only", "(b), (c) and (d) only"],
  why="(e) is listed by NCERT among ways to prevent drug abuse, so every option with (e) is wrong; '(b), (c) and (d) "
      "only' leaves out curiosity and experimentation, which NCERT calls common causes.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, D,
  "According to NCERT, the chronic use of drugs and alcohol damages which of the following?",
  "Long-term effects of alcohol and drugs",
  "NCERT: the chronic use of drugs and alcohol damages the nervous system and the liver (cirrhosis). The use of "
  "drugs and alcohol during pregnancy is also known to adversely affect the foetus.",
  ["Chronic use -> nervous system damage", "-> liver damage (cirrhosis)"],
  "Effects of Drug/Alcohol Abuse",
  at="A", correct="The nervous system and the liver (cirrhosis)",
  wrong=["Only the lymph nodes and the spleen", "Only the skin, as dry scaly lesions",
         "Only the alveoli of the lungs, which fill with fluid"],
  why="Effects on lymphoid organs are not what NCERT describes; dry scaly skin lesions are ringworm; fluid-filled "
      "alveoli are pneumonia. NCERT names the nervous system and the liver.", secs=25)

Z(HHD, "Drug and alcohol abuse", I, ASR,
  AR("Those who take drugs intravenously are much more likely to acquire serious infections like AIDS and hepatitis "
     "B.",
     "The viruses responsible for these diseases are transferred from one person to another by sharing of infected "
     "needles and syringes."),
  "Intravenous drug use and infection",
  "NCERT: those who take drugs intravenously (direct injection into the vein using a needle and syringe) are much "
  "more likely to acquire serious infections like AIDS and hepatitis B. The viruses responsible for these diseases "
  "are transferred from one person to another by sharing of infected needles and syringes. R is the route that "
  "puts intravenous users at higher risk, so it explains A.",
  ["A: true", "R: true", "Shared infected needles carry the viruses -> higher risk"],
  "Effects of Drug/Alcohol Abuse", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT gives needle sharing as "
      "the way the viruses pass between intravenous users, so R explains A.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Hashish, charas and ganja are obtained from the coca plant Erythroxylum coca.",
     "Marijuana, hashish, charas and ganja are known for their effects on the cardiovascular system of the body."),
  "Cannabinoids",
  "NCERT: natural cannabinoids are obtained from the inflorescences of the plant Cannabis sativa. The flower tops, "
  "leaves and resin of the cannabis plant are used in various combinations to produce marijuana, hashish, charas "
  "and ganja; generally taken by inhalation and oral ingestion, these are known for their effects on the "
  "cardiovascular system. Erythroxylum coca is the source of cocaine.",
  ["Statement I: false - from Cannabis sativa", "Statement II: true"],
  "Drugs and Alcohol Abuse", ans="D",
  why="Statement I gives the source of cocaine for the cannabinoids, so options calling it true are wrong; "
      "Statement II is NCERT's description, so options calling it false are wrong.", secs=30)

Z(HHD, "Pathogens and diseases", I, D,
  "Salmonella typhi causes typhoid fever. According to NCERT, how does the pathogen generally enter the body and "
  "reach other organs?",
  "Route of Salmonella typhi",
  "NCERT: Salmonella typhi is a pathogenic bacterium which causes typhoid fever in human beings. These pathogens "
  "generally enter the small intestine through food and water contaminated with them and migrate to other organs "
  "through blood.",
  ["Contaminated food/water -> small intestine", "-> migrate to other organs through blood"],
  "Common Diseases in Humans",
  at="B", correct="It enters the small intestine through contaminated food and water and migrates to other organs "
                  "through blood",
  wrong=["It enters the lungs through droplets and stays confined to the alveoli",
         "It is injected by the bite of a female Anopheles mosquito and multiplies in the liver cells",
         "It enters through the skin from soil and stays in the skin folds"],
  why="Droplets and alveoli describe pneumonia; the mosquito bite and liver multiplication describe Plasmodium; "
      "entry from soil and skin folds describe ringworm fungi.", secs=30)

Z(HHD, "Cancer", I, MAT,
  ML(("term", "meaning, as used in NCERT"),
     ["Contact inhibition", "Metastasis", "Neoplastic cells", "Biological response modifiers"],
     ["Cells sloughed from tumours reach distant sites through blood and start new tumours there",
      "Substances such as α-interferon that activate the immune system to help destroy the tumour",
      "The property by which contact with other cells inhibits uncontrolled growth; lost by cancer cells",
      "The proliferating cells of malignant tumours"]),
  "Cancer terms",
  "NCERT: in normal cells, contact with other cells inhibits their uncontrolled growth, a property called contact "
  "inhibition; cancer cells appear to have lost it. Malignant tumours are a mass of proliferating cells called "
  "neoplastic or tumour cells. Cells sloughed from such tumours reach distant sites through blood and start new "
  "tumours wherever they get lodged; this property is called metastasis. Patients are given substances called "
  "biological response modifiers such as α-interferon, which activate their immune system and help in destroying "
  "the tumour.",
  ["A -> III", "B -> I", "C -> IV", "D -> II"],
  "Cancer",
  at="A", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"}]),
  why="Contact inhibition is a property of normal cells, not the spread of tumour cells; metastasis is the "
      "spreading, not the name of the tumour cells themselves; and neoplastic cells are not immune-activating "
      "substances.", secs=45)

Z(HHD, "Pathogens and diseases", I, MUL,
  MS("Which of the following statements about health are correct, according to NCERT?",
     ["Health is a state of complete physical, mental and social well-being.",
      "Health is affected by genetic disorders, infections and life style.",
      "Balanced diet, personal hygiene and regular exercise are very important to maintain good health.",
      "Proper disposal of wastes, control of vectors and maintenance of hygienic food and water resources are "
      "necessary for achieving good health.",
      "Health simply means the absence of disease or physical fitness."]),
  "Meaning of health",
  "NCERT: health does not simply mean 'absence of disease' or 'physical fitness'; it can be defined as a state of "
  "complete physical, mental and social well-being. Health is affected by genetic disorders, infections and life "
  "style. Balanced diet, personal hygiene and regular exercise are very important to maintain good health, and "
  "awareness about diseases, vaccination, proper disposal of wastes, control of vectors and maintenance of hygienic "
  "food and water resources are necessary for achieving good health.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - NCERT rejects this narrow meaning"],
  "Human Health and Disease (introduction)",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(b), (c) and (e) only", "(a) and (e) only"],
  why="NCERT explicitly says health does not simply mean absence of disease or physical fitness, so every option "
      "containing (e) is wrong; the correct option keeps all four NCERT statements.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, ASR,
  AR("Heroin, commonly called smack, is obtained by the acetylation of morphine.",
     "Morphine is extracted from the inflorescences of the plant Cannabis sativa."),
  "Source of opioids",
  "NCERT: heroin, commonly called smack, is chemically diacetylmorphine, a white, odourless, bitter crystalline "
  "compound obtained by acetylation of morphine, which is extracted from the latex of the poppy plant Papaver "
  "somniferum. Cannabis sativa inflorescences are the source of natural cannabinoids. A is true and R is false.",
  ["A: true", "R: false - morphine comes from the latex of Papaver somniferum"],
  "Drugs and Alcohol Abuse", ans="C",
  why="R names the cannabinoid plant as the source of morphine, so options treating R as true are wrong; A is "
      "NCERT's description of heroin, so 'A is false' is wrong.", secs=30)

Z(HHD, "Drug and alcohol abuse", A, MUL,
  MS("Which of the following statements about addiction and dependence are correct, according to NCERT?",
     ["Addiction is a psychological attachment to certain effects, such as euphoria and a temporary feeling of "
      "well-being, associated with drugs and alcohol.",
      "With repeated use of drugs, the tolerance level of the receptors present in the body increases.",
      "Consequently, the receptors respond only to higher doses of drugs or alcohol, leading to greater intake.",
      "Dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal syndrome if "
      "the regular dose is abruptly discontinued.",
      "Withdrawal symptoms are always mild, so medical supervision is never needed."]),
  "Addiction and dependence",
  "NCERT: addiction is a psychological attachment to certain effects such as euphoria and a temporary feeling of "
  "well-being associated with drugs and alcohol. With repeated use, the tolerance level of the receptors present "
  "in our body increases; consequently the receptors respond only to higher doses, leading to greater intake and "
  "addiction. Dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal "
  "syndrome if the regular dose is abruptly discontinued; in some cases withdrawal symptoms can be severe and even "
  "life threatening, and the person may need medical supervision.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - can be severe, even life threatening"],
  "Addiction and Dependence",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (e) only"],
  why="(e) contradicts NCERT's statement that withdrawal can be severe and even life threatening, so every option "
      "with (e) is wrong; (a)-(d) are all NCERT statements.", secs=55)

Z(HHD, "Drug and alcohol abuse", A, MAT,
  ML(("drug or drug group", "NCERT description"),
     ["Heroin", "Cocaine", "Cannabinoids", "Barbiturates, amphetamines and benzodiazepines"],
     ["Known for their effects on the cardiovascular system",
      "Normally used as medicines to help patients cope with mental illnesses like depression and insomnia, but "
      "often abused",
      "A depressant that slows down body functions",
      "Potent stimulating action on the central nervous system, producing a sense of euphoria and increased energy"]),
  "Commonly abused drugs",
  "NCERT: heroin is a depressant and slows down body functions. Cocaine has a potent stimulating action on the "
  "central nervous system, producing a sense of euphoria and increased energy. Cannabinoids (marijuana, hashish, "
  "charas, ganja) are known for their effects on the cardiovascular system. Drugs like barbiturates, amphetamines "
  "and benzodiazepines are normally used as medicines to help patients cope with mental illnesses like depression "
  "and insomnia, but are often abused.",
  ["A heroin -> III", "B cocaine -> IV", "C cannabinoids -> I", "D barbiturates etc. -> II"],
  "Drugs and Alcohol Abuse",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Heroin is a depressant and cocaine a stimulant, so swapping them is wrong; the cardiovascular effects belong "
      "to cannabinoids, while the medicinal use for depression and insomnia belongs to barbiturates, amphetamines "
      "and benzodiazepines.", secs=50)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Mucosa-associated lymphoid tissue (MALT) constitutes about 50 per cent of the lymphoid tissue in the human "
     "body.",
     "MALT is located only within the lining of the digestive tract."),
  "Mucosa-associated lymphoid tissue",
  "NCERT: there is lymphoid tissue also located within the lining of the major tracts (respiratory, digestive and "
  "urogenital tracts), called mucosa-associated lymphoid tissue (MALT). It constitutes about 50 per cent of the "
  "lymphoid tissue in the human body. R restricts it to the digestive tract, so R is false while A is true.",
  ["A: true - about 50 per cent", "R: false - respiratory, digestive and urogenital tracts"],
  "Immunity (Lymphoid Organs)", ans="C",
  why="R leaves out the respiratory and urogenital tracts, so options treating R as true are wrong; A is NCERT's "
      "figure, so 'A is false' is wrong.", secs=35)

Z(HHD, "Cancer", A, STP,
  SP("Cancer-causing viruses, called oncogenic viruses, have genes called viral oncogenes.",
     "Several chemotherapeutic drugs are used to kill cancerous cells, and some of these are specific for particular "
     "tumours."),
  "Oncogenic viruses and chemotherapy",
  "NCERT: cancer causing viruses called oncogenic viruses have genes called viral oncogenes; several genes called "
  "cellular oncogenes (c-onc) or proto-oncogenes have also been identified in normal cells which, when activated "
  "under certain conditions, could lead to oncogenic transformation. In treatment, several chemotherapeutic drugs "
  "are used to kill cancerous cells; some of these are specific for particular tumours, and the majority have side "
  "effects such as hair loss and anaemia.",
  ["Statement I: true", "Statement II: true"],
  "Cancer", ans="A",
  why="Both statements are NCERT's own; the trap is reading 'some are specific for particular tumours' as false. "
      "Every option calling either statement false is wrong.", secs=35)

Z(HHD, "Pathogens and diseases", A, D,
  "Which one of the following sets of pathogen, disease and mode of transmission is entirely correct according to "
  "NCERT?",
  "Pathogen-disease-transmission",
  "NCERT: Wuchereria (W. bancrofti and W. malayi), the filarial worms, cause filariasis (elephantiasis) and are "
  "transmitted to a healthy person through the bite by the female mosquito vectors. Entamoeba histolytica causes "
  "amoebiasis and spreads through food and water contaminated by faecal matter (houseflies acting as mechanical "
  "carriers). Ringworm fungi (e.g. Trichophyton) are acquired from soil or by using towels, clothes or even the "
  "comb of infected individuals. Streptococcus pneumoniae causes pneumonia, not typhoid.",
  ["Check each part of the set", "Only the Wuchereria set is right in all three parts"],
  "Common Diseases in Humans",
  at="C", correct="Wuchereria – filariasis – bite of female mosquito vectors",
  wrong=["Entamoeba histolytica – amoebiasis – inhaling droplets released by an infected person",
         "Trichophyton – ringworm – bite of the female Anopheles mosquito",
         "Streptococcus pneumoniae – typhoid – contaminated food and water"],
  why="Amoebiasis is not air-borne; ringworm spreads from soil and shared towels, clothes or combs, not by "
      "mosquitoes; and Streptococcus pneumoniae causes pneumonia, while typhoid is caused by Salmonella typhi.",
  secs=45)

Z(HHD, "Pathogens and diseases", A, D,
  "How many of the following human diseases are caused by bacteria, according to NCERT?\n\nTyphoid, pneumonia, "
  "common cold, dysentery, plague, diphtheria, malaria, ringworm, amoebiasis",
  "Bacterial diseases",
  "NCERT: typhoid (Salmonella typhi) and pneumonia (Streptococcus pneumoniae and Haemophilus influenzae) are "
  "bacterial diseases, and 'dysentery, plague, diphtheria, etc., are some of the other bacterial diseases in man'. "
  "The common cold is viral (rhinoviruses), malaria and amoebiasis are protozoan, and ringworm is fungal.",
  ["Bacterial: typhoid, pneumonia, dysentery, plague, diphtheria = 5", "Viral: common cold",
   "Protozoan: malaria, amoebiasis", "Fungal: ringworm"],
  "Common Diseases in Humans",
  at="B", correct="Five",
  wrong=["Four", "Six", "Seven"],
  why="Four usually leaves out dysentery, which NCERT lists among bacterial diseases; six or seven add the common "
      "cold (viral), ringworm (fungal) or a protozoan disease such as amoebiasis.", secs=50)
