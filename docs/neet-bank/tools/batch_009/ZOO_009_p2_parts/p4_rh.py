
# ================================================================ Reproductive Health (4/5/4)
Z(RH, "Contraception", B, D,
  "Besides motivating smaller families, NCERT mentions a statutory measure taken to tackle population growth in "
  "India: raising the marriageable age. To what ages was it raised?",
  "Measures for population stabilisation",
  "NCERT: statutory raising of the marriageable age of the female to 18 years and that of the male to 21 years, "
  "and incentives given to couples with small families, are two of the other measures taken to tackle the "
  "problem of population growth.",
  ["Female: 18 years", "Male: 21 years"],
  "Population Stabilisation and Birth Control",
  at="D", correct="18 years for females and 21 years for males",
  wrong=["21 years for females and 18 years for males", "18 years for both females and males",
         "16 years for females and 18 years for males"],
  why="The first option reverses the two ages; NCERT gives different ages for males and females, so 18 for both "
      "is wrong; 16 and 18 are lower than the ages NCERT states.", secs=20)

Z(RH, "STDs and their prevention", B, D,
  "If sexually transmitted infections (STIs) are not detected and treated in time, NCERT says they may lead to "
  "complications later. Which set lists those complications?",
  "Complications of untreated STIs",
  "NCERT: early symptoms of most STIs are minor, and infected females may often be asymptomatic, so infections "
  "may remain undetected or untreated for a long time. This could lead to complications later, which include "
  "pelvic inflammatory diseases (PID), abortions, still births, ectopic pregnancies, infertility or even cancer of "
  "the reproductive tract.",
  ["Untreated STIs -> PID, abortions, still births, ectopic pregnancies, infertility, cancer of the reproductive "
   "tract"],
  "Sexually Transmitted Infections (STIs)",
  at="A", correct="Pelvic inflammatory diseases, abortions, still births, ectopic pregnancies, infertility and even "
                  "cancer of the reproductive tract",
  wrong=["Goitre, cretinism and exophthalmic goitre",
         "Diabetes insipidus, diabetes mellitus and Addison's disease",
         "Colour blindness, haemophilia and sickle-cell anaemia"],
  why="The other sets are hormonal disorders (thyroid, ADH, insulin, adrenal cortex) or inherited genetic "
      "disorders, none of which NCERT links to untreated STIs.", secs=25)

Z(RH, "Contraception", B, STP,
  SP("'Nirodh' is a popular brand of condom for the male.",
     "Unlike diaphragms, cervical caps and vaults, male and female condoms are reusable."),
  "Condoms and other barriers",
  "NCERT: condoms are barriers made of thin rubber/latex sheath; 'Nirodh' is a popular brand of condom for the "
  "male. Both the male and the female condoms are DISPOSABLE, can be self-inserted and thereby give privacy to the "
  "user. It is the diaphragms, cervical caps and vaults (also made of rubber) that are reusable.",
  ["Statement I: true", "Statement II: false - condoms are disposable; diaphragms, caps and vaults are reusable"],
  "Population Stabilisation and Birth Control", ans="C",
  why="Statement II reverses NCERT's contrast between disposable condoms and reusable diaphragms, caps and vaults, "
      "so options calling it true are wrong; Statement I is NCERT's own, so options calling it false are wrong.",
  secs=30)

Z(RH, "Contraception", B, ASR,
  AR("Lactational amenorrhea is a natural method of contraception.",
     "The chances of failure of natural methods of contraception are high."),
  "Natural methods",
  "NCERT: natural methods work on the principle of avoiding chances of the ovum and sperms meeting; periodic "
  "abstinence, withdrawal (coitus interruptus) and lactational amenorrhea are such methods. Since no medicines or "
  "devices are used, side effects are almost nil, but the chances of failure are also high. A method is natural "
  "because it uses no device, medicine or surgery, not because it often fails; so R, though true, does not explain "
  "A.",
  ["A: true", "R: true", "R is a limitation of natural methods, not the reason a method is called natural"],
  "Population Stabilisation and Birth Control", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; a high failure rate is a "
      "drawback of natural methods, not what makes lactational amenorrhea one, so R is not the explanation.",
  secs=35)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive", "type"),
     ["Vaults", "Multiload 375", "Implants under the skin", "Periodic abstinence"],
     ["Natural method", "Barrier method", "Progestogens alone or with estrogen given by the female",
      "Copper-releasing IUD"]),
  "Kinds of contraceptives",
  "NCERT: diaphragms, cervical caps and vaults are barriers made of rubber, inserted into the female tract to cover "
  "the cervix during coitus. Copper-releasing IUDs are CuT, Cu7 and Multiload 375. Progestogens alone or in "
  "combination with estrogen can be used by females as injections or implants under the skin. Periodic abstinence "
  "is a natural method.",
  ["A vaults -> barrier (II)", "B Multiload 375 -> copper IUD (IV)", "C implants -> progestogens (III)",
   "D periodic abstinence -> natural (I)"],
  "Population Stabilisation and Birth Control",
  at="B", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="A vault is a rubber barrier, not an IUD; Multiload 375 releases copper, not hormones, and implants are "
      "hormonal; periodic abstinence uses no barrier at all.", secs=40)

Z(RH, "Infertility and ART", I, MUL,
  MS("A large number of couples all over the world, including India, are infertile. Which of the following does "
     "NCERT list as possible reasons for infertility?",
     ["Physical reasons", "Congenital diseases", "Drugs", "Immunological reasons", "Psychological reasons"]),
  "Causes of infertility",
  "NCERT: infertility is the inability to conceive or produce children even after unprotected sexual "
  "co-habitation. The reasons for this could be many: physical, congenital diseases, drugs, immunological or even "
  "psychological. All five listed causes are therefore in NCERT's list.",
  ["(a)-(e) all appear in NCERT's list: physical, congenital diseases, drugs, immunological, psychological"],
  "Infertility",
  at="D", correct="(a), (b), (c), (d) and (e)",
  wrong=["(a), (b) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only"],
  why="NCERT includes immunological and even psychological reasons alongside physical causes, congenital "
      "diseases and drugs, so every option that leaves out any of them is incomplete.", secs=35)

Z(RH, "Contraception", I, D,
  "Advertisements and posters in India often show a happy couple with two children and the slogan 'Hum Do Hamare "
  "Do' (we two, our two). According to NCERT, what is the purpose of such campaigns?",
  "Motivating small families",
  "NCERT: the most important step to overcome the population explosion is to motivate smaller families by using "
  "various contraceptive methods. Advertisements showing a happy couple with two children and the slogan Hum Do "
  "Hamare Do serve this aim; many couples, mostly the young, urban, working ones, have even adopted a 'one child "
  "norm'.",
  ["Problem: population explosion", "Strategy: motivate smaller families using contraceptive methods"],
  "Population Stabilisation and Birth Control",
  at="C", correct="To motivate smaller families by using contraceptive methods, so as to check population growth",
  wrong=["To encourage medical termination of every third pregnancy",
         "To promote amniocentesis for choosing the sex of the two children",
         "To encourage assisted reproductive technologies for every couple"],
  why="NCERT says MTP is not meant for population control and condemns the misuse of amniocentesis for sex "
      "determination; ART is for infertile couples, not a population measure.", secs=30)

Z(RH, "STDs and their prevention", I, ASR,
  AR("STIs in women may remain undetected or untreated for a long time.",
     "In infected females, STIs are often asymptomatic, and the early symptoms of most STIs are minor."),
  "Late detection of STIs",
  "NCERT: early symptoms of most of these diseases are minor, and these include itching, fluid discharge, slight "
  "pain, swellings, etc., in the genital region. Infected females may often be asymptomatic and hence may remain "
  "undetected for long. Absent or less significant early symptoms (along with social stigma) deter people from "
  "timely detection and treatment. R gives the very reason for A.",
  ["A: true", "R: true", "No or minor symptoms -> infection goes unnoticed -> R explains A"],
  "Sexually Transmitted Infections (STIs)", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; NCERT links the absence of "
      "symptoms directly to infections remaining undetected, so R is the correct explanation.", secs=35)

Z(RH, "Contraception", I, STP,
  SP("The chances of failure of periodic abstinence and coitus interruptus are high.",
     "Tubectomy is the sterilisation method adopted by the male partner."),
  "Natural and surgical methods",
  "NCERT: natural methods such as periodic abstinence and coitus interruptus have almost nil side effects, but "
  "their chances of failure are also high. Sterilisation in the male is called vasectomy (a small part of the vas "
  "deferens is removed or tied up); that in the female is called tubectomy (a small part of the fallopian tube is "
  "removed or tied up).",
  ["Statement I: true", "Statement II: false - tubectomy is for the female; vasectomy for the male"],
  "Population Stabilisation and Birth Control", ans="C",
  why="Statement II confuses tubectomy with vasectomy, so options calling it true are wrong; Statement I is "
      "NCERT's limitation of natural methods, so options calling it false are wrong.", secs=30)

Z(RH, "Contraception", A, MUL,
  MS("Which of the following methods prevent conception WITHOUT the use of any device, medicine or surgery?",
     ["Periodic abstinence", "Coitus interruptus (withdrawal)", "Lactational amenorrhea", "Vasectomy",
      "Diaphragm"]),
  "Natural methods of contraception",
  "NCERT: natural methods work on the principle of avoiding chances of the ovum and sperms meeting; periodic "
  "abstinence, withdrawal (coitus interruptus) and lactational amenorrhea are such methods, and since no medicines "
  "or devices are used in them, side effects are almost nil. Vasectomy is a surgical method (sterilisation), and a "
  "diaphragm is a rubber barrier device.",
  ["(a), (b), (c): natural methods", "(d): surgical", "(e): barrier device"],
  "Population Stabilisation and Birth Control",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(a) and (c) only", "(b), (c) and (d) only"],
  why="A diaphragm is a device and vasectomy is surgery, so options with (d) or (e) are wrong; '(a) and (c) only' "
      "leaves out withdrawal, which NCERT lists as a natural method.", secs=40)

Z(RH, "Infertility and ART", A, D,
  "In how many of the following techniques does fertilisation take place INSIDE the body of the female (in vivo)?"
  "\n\nGIFT, ZIFT, IUT, ICSI, intra-uterine insemination (IUI), artificial insemination with semen introduced into "
  "the vagina",
  "In vivo versus in vitro fertilisation in ART",
  "NCERT: in IVF, ova and sperms are induced to form a zygote under simulated conditions in the laboratory; the "
  "zygote or early embryo (up to 8 blastomeres) is then transferred into the fallopian tube (ZIFT), and embryos "
  "with more than 8 blastomeres into the uterus (IUT). ICSI is a procedure to form an embryo in the laboratory, in "
  "which a sperm is directly injected into the ovum. In GIFT, an ovum collected from a donor is transferred into "
  "the fallopian tube of another female who can provide suitable environment for fertilisation. In artificial "
  "insemination, semen is introduced into the vagina or into the uterus (IUI), so fertilisation follows inside "
  "the female body.",
  ["In vivo: GIFT, IUI, AI into the vagina = 3", "In vitro (laboratory): ZIFT, IUT, ICSI"],
  "Infertility",
  at="B", correct="Three",
  wrong=["Two", "Four", "Five"],
  why="Two forgets that artificial insemination into the vagina, like IUI, leads to fertilisation in the body; four "
      "or five add ZIFT, IUT or ICSI, in which the zygote or embryo is formed in the laboratory.", secs=50)

Z(RH, "Contraception", A, ASR,
  AR("Emergency contraceptives are very effective even when used a week after unprotected coitus.",
     "Administration of progestogens or progestogen–estrogen combinations, or the use of IUDs, can be used as "
     "emergency contraceptives."),
  "Emergency contraception",
  "NCERT: administration of progestogens or progestogen–estrogen combinations, or IUDs, within 72 hours of coitus "
  "have been found to be very effective as emergency contraceptives, as they could be used to avoid possible "
  "pregnancy due to rape or casual unprotected intercourse. A week is well beyond the 72-hour window, so A is "
  "false while R is true.",
  ["A: false - effective within 72 hours", "R: true - pills/progestogens or IUDs"],
  "Population Stabilisation and Birth Control", ans="D",
  why="A ignores NCERT's 72-hour limit, so options calling A true are wrong; R correctly names the emergency "
      "methods, so 'A is false but R is true' is the answer.", secs=35)

Z(RH, "MTP and amniocentesis", A, MUL,
  MS("Which of the following does NCERT mention in its account of reproductive health programmes and their "
     "outcomes in India?",
     ["A statutory ban on amniocentesis for sex determination, to legally check increasing female foeticides",
      "Massive child immunisation",
      "Development of the oral contraceptive 'Saheli' by scientists at CDRI, Lucknow, as an outcome of research "
      "on reproduction-related areas",
      "Increased medically assisted deliveries and better post-natal care, leading to decreased maternal and infant "
      "mortality rates",
      "Compulsory sterilisation of every couple after the birth of two children"]),
  "Reproductive health programmes",
  "NCERT: a statutory ban on amniocentesis for sex determination to legally check increasing female foeticides, "
  "massive child immunisation, etc. are some programmes being undertaken; research on reproduction-related areas "
  "is encouraged, and 'Saheli' was developed by scientists at CDRI, Lucknow. Better awareness, increased "
  "medically assisted deliveries and better post-natal care leading to decreased MMR and IMR indicate improved "
  "reproductive health. NCERT speaks of motivating smaller families and incentives to couples with small "
  "families; it mentions no compulsory sterilisation.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false - not in NCERT; sterilisation is a voluntary terminal "
   "method"],
  "Reproductive Health - Problems and Strategies",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (e) only", "(c), (d) and (e) only"],
  why="(e) is not among NCERT's measures (it speaks of motivation and incentives), so every option containing (e) "
      "is wrong; the remaining four are all NCERT statements.", secs=55)
