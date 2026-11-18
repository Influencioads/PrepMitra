
# ================================================================ Human Reproduction (6/9/6)
Z(HR, "Gametogenesis", B, D,
  "A couple of million oogonia are formed in each fetal ovary, but a large number of follicles degenerate between "
  "birth and puberty. About how many primary follicles are left in each ovary at puberty?",
  "Follicles left at puberty",
  "NCERT: a large number of the follicles degenerate during the phase from birth to puberty. Therefore, at puberty "
  "only 60,000–80,000 primary follicles are left in each ovary.",
  ["Fetal ovary: a couple of million oogonia", "Birth -> puberty: many follicles degenerate",
   "Puberty: 60,000–80,000 primary follicles per ovary"],
  "Gametogenesis",
  at="C", correct="60,000–80,000",
  wrong=["200–300", "1–2 million", "200–300 million"],
  why="200–300 is near the number of testicular lobules (about 250), not follicles; 1–2 million is the order of "
      "the oogonia formed in fetal life, before degeneration; 200–300 million is the number of sperms in one "
      "ejaculate.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "The urethra of a human male originates from the urinary bladder and extends through the penis. Its external "
  "opening is called the:",
  "Male urethra",
  "NCERT: the urethra originates from the urinary bladder and extends through the penis to its external opening "
  "called the urethral meatus.",
  ["Urinary bladder -> urethra -> through the penis -> urethral meatus"],
  "The Male Reproductive System",
  at="A", correct="Urethral meatus",
  wrong=["Glans penis", "Ejaculatory duct", "Cervical canal"],
  why="The glans penis is the enlarged end of the penis, covered by the foreskin, not an opening; the ejaculatory "
      "duct is formed by the vas deferens and the seminal vesicle duct and opens into the urethra; the cervical "
      "canal is in the female cervix.", secs=20)

Z(HR, "Male and female reproductive systems", B, STP,
  SP("The uterus opens into the vagina through a narrow cervix.",
     "The cavity of the cervix, the cervical canal, forms the birth canal together with the oviduct."),
  "Cervix and birth canal",
  "NCERT: the uterus opens into the vagina through a narrow cervix. The cavity of the cervix is called the "
  "cervical canal, which along with the VAGINA forms the birth canal. The oviduct joins the uterus at the other "
  "end and is not part of the birth canal.",
  ["Statement I: true", "Statement II: false - cervical canal + vagina = birth canal"],
  "The Female Reproductive System", ans="C",
  why="Statement II replaces the vagina with the oviduct, so options calling it true are wrong; Statement I is "
      "NCERT's description, so options calling it false are wrong.", secs=30)

Z(HR, "Male and female reproductive systems", B, ASR,
  AR("Each ovary is covered by a thin epithelium which encloses the ovarian stroma.",
     "The ovaries are located one on each side of the lower abdomen."),
  "Structure and position of the ovary",
  "NCERT: ovaries are the primary female sex organs located one on each side of the lower abdomen. Each ovary is "
  "covered by a thin epithelium which encloses the ovarian stroma, which is divided into a peripheral cortex and "
  "an inner medulla. Both are true, but the ovary's position in the abdomen does not explain its epithelial "
  "covering.",
  ["A: true", "R: true", "R gives position, A gives structure -> no causal link"],
  "The Female Reproductive System", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; where the ovaries lie does "
      "not account for the epithelium around the stroma, so R is not the explanation of A.", secs=30)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "According to NCERT, during which month of human pregnancy are the first movements of the foetus and the "
  "appearance of hair on the head usually observed?",
  "Foetal development timeline",
  "NCERT: after one month of pregnancy, the embryo's heart is formed; by the end of the second month the foetus "
  "develops limbs and digits; by the end of 12 weeks most of the major organ systems are formed; during the fifth "
  "month, the first movements of the foetus and the appearance of hair on the head are usually observed; by the end "
  "of about 24 weeks the body is covered with fine hair, eyelids separate and eyelashes are formed.",
  ["1 month: heart", "2 months: limbs and digits", "12 weeks: major organ systems",
   "5th month: first movements, hair on head", "24 weeks: fine hair, eyelids separate"],
  "Pregnancy and Embryonic Development",
  at="D", correct="The fifth month",
  wrong=["The first month", "The second month", "The ninth month"],
  why="The first month is when the heart forms and the second month when limbs and digits develop; by the end of "
      "the ninth month the foetus is fully developed and ready for delivery, long after the first movements.",
  secs=25)

Z(HR, "Gametogenesis", B, D,
  "In the fetal ovary, the gamete mother cells (oogonia) start division and get temporarily arrested as primary "
  "oocytes. At which stage are they arrested?",
  "Arrest of primary oocytes",
  "NCERT: oogonia start division and enter into prophase-I of the meiotic division and get temporarily arrested "
  "at that stage; they are then called primary oocytes.",
  ["Oogonia -> enter meiosis I", "Arrested in prophase-I -> primary oocytes"],
  "Gametogenesis",
  at="B", correct="Prophase-I of the meiotic division",
  wrong=["Metaphase of mitosis", "Prophase-II of the meiotic division",
         "After completing the second meiotic division"],
  why="The oogonia have entered meiosis, so a mitotic arrest is wrong; prophase-II would require the first "
      "meiotic division to be complete, which happens only within the tertiary follicle; the second meiotic "
      "division is completed only when a sperm enters the secondary oocyte.", secs=25)

Z(HR, "Male and female reproductive systems", I, MAT,
  ML(("part of a human sperm", "feature described in NCERT"),
     ["Head", "Acrosome", "Middle piece", "Tail"],
     ["Its movement facilitates the sperm motility essential for fertilisation",
      "Contains an elongated haploid nucleus",
      "Possesses numerous mitochondria",
      "Cap-like structure filled with enzymes that help fertilisation of the ovum"]),
  "Structure of a sperm",
  "NCERT: the sperm head contains an elongated haploid nucleus, the anterior portion of which is covered by a "
  "cap-like structure, the acrosome, filled with enzymes that help fertilisation of the ovum. The middle piece "
  "possesses numerous mitochondria, which produce energy for the movement of the tail that facilitates sperm "
  "motility essential for fertilisation.",
  ["A head -> II", "B acrosome -> IV", "C middle piece -> III", "D tail -> I"],
  "The Male Reproductive System; Gametogenesis",
  at="D", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="The acrosome caps the head but carries enzymes, while the nucleus lies in the head, so swapping A and B is "
      "wrong; the mitochondria are in the middle piece and supply energy for the tail's movement, so swapping C "
      "and D is wrong; the acrosome holds enzymes, not mitochondria.", secs=40)

Z(HR, "Menstrual cycle", I, MUL,
  MS("Which of the following statements about the human menstrual cycle are correct, according to NCERT?",
     ["The first menstruation, which begins at puberty, is called menarche.",
      "The menstrual flow lasts for about 3–5 days.",
      "The menstrual cycle is repeated at an average interval of about 14 days.",
      "Both LH and FSH attain a peak level in the middle of the cycle (about the 14th day).",
      "Menstrual cycles cease around 50 years of age; this is termed menopause."]),
  "Timings in the menstrual cycle",
  "NCERT: the first menstruation begins at puberty and is called menarche. The cycle is repeated at an average "
  "interval of about 28/29 days. The menstrual flow lasts for 3–5 days. Both LH and FSH attain a peak level in the "
  "middle of the cycle (about the 14th day). In human beings, menstrual cycles cease around 50 years of age, "
  "termed menopause. 14 days is the time to ovulation, not the length of the cycle.",
  ["(a) true", "(b) true", "(c) false - about 28/29 days", "(d) true", "(e) true"],
  "Menstrual Cycle",
  at="C", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (d) only", "(b), (c) and (e) only"],
  why="(c) gives the time to the mid-cycle peak instead of the length of the cycle, so options containing (c) are "
      "wrong; the correct option keeps all the other four NCERT timings.", secs=45)

Z(HR, "Fertilisation and implantation", I, D,
  "In a woman, an ovum is fertilised in the ampullary region and the zygote undergoes cleavage to form a morula, "
  "but the morula fails to transform into a blastocyst. According to NCERT's sequence of events, which of the "
  "following could then NOT take place?",
  "From morula to implantation",
  "NCERT: the morula continues to divide and transforms into a blastocyst as it moves further into the uterus. "
  "The blastomeres in the blastocyst are arranged into an outer trophoblast and an inner cell mass. The "
  "trophoblast layer then gets attached to the endometrium; the uterine cells divide rapidly and cover the "
  "blastocyst, which becomes embedded in the endometrium (implantation). Without a blastocyst there is no "
  "trophoblast to attach, so implantation cannot occur. The other events listed come before the morula stage.",
  ["Fertilisation (done) -> cleavage -> morula (done)", "Morula -> blastocyst (fails)",
   "Trophoblast attaches to endometrium -> implantation (cannot occur)"],
  "Fertilisation and Implantation",
  at="A", correct="Attachment of the trophoblast to the endometrium (implantation)",
  wrong=["Fusion of the haploid nuclei of the sperm and the ovum",
         "Formation of 2, 4 and 8 blastomeres by mitotic division",
         "Completion of the second meiotic division of the secondary oocyte"],
  why="Fusion of the gametes' nuclei and completion of the second meiotic division happen at fertilisation, and "
      "cleavage into 2, 4 and 8 blastomeres produces the morula; all three are already over when the morula "
      "fails to form a blastocyst.", secs=45)

Z(HR, "Gametogenesis", I, ASR,
  AR("Oogonia continue to be formed and added to the ovaries throughout the reproductive life of a woman.",
     "Gamete mother cells (oogonia) are formed within each fetal ovary during embryonic development."),
  "Timing of oogonia formation",
  "NCERT: oogenesis is initiated during the embryonic development stage when a couple of million gamete mother "
  "cells (oogonia) are formed within each fetal ovary; no more oogonia are formed and added after birth. So R is "
  "true and A is false.",
  ["A: false - no oogonia are added after birth", "R: true - formed in the fetal ovary"],
  "Gametogenesis", ans="D",
  why="A contradicts NCERT's statement that no more oogonia are formed and added after birth, so options calling A "
      "true are wrong; R is NCERT's own statement, so 'A is false but R is true' is the answer.", secs=35)

Z(HR, "Male and female reproductive systems", I, STP,
  SP("Each human testis has about 250 compartments called testicular lobules.",
     "Each testicular lobule contains about 10 to 12 highly coiled seminiferous tubules."),
  "Testicular lobules",
  "NCERT: each testis has about 250 compartments called testicular lobules, and each lobule contains one to three "
  "highly coiled seminiferous tubules in which sperms are produced. 10–12 cm is the length of an oviduct, not the "
  "number of tubules.",
  ["Statement I: true", "Statement II: false - one to three tubules per lobule"],
  "The Male Reproductive System", ans="C",
  why="Statement II overstates the number of tubules per lobule, so options calling it true are wrong; Statement "
      "I is NCERT's figure, so options calling it false are wrong.", secs=30)

Z(HR, "Male and female reproductive systems", I, D,
  "Which option gives the three layers of the wall of the human uterus in the correct order from the OUTSIDE to "
  "the INSIDE (towards the uterine cavity)?",
  "Layers of the uterine wall",
  "NCERT: the wall of the uterus has three layers of tissue: the external thin membranous perimetrium, the middle "
  "thick layer of smooth muscle, the myometrium, and the inner glandular layer called the endometrium that lines "
  "the uterine cavity.",
  ["Outer: perimetrium (thin, membranous)", "Middle: myometrium (thick smooth muscle)",
   "Inner: endometrium (glandular, lines the cavity)"],
  "The Female Reproductive System",
  at="B", correct="Perimetrium → myometrium → endometrium",
  wrong=["Endometrium → myometrium → perimetrium", "Myometrium → perimetrium → endometrium",
         "Perimetrium → endometrium → myometrium"],
  why="The first option lists the layers from inside to outside; the myometrium is the middle layer, not the "
      "outermost; and the glandular endometrium lines the cavity, so it cannot lie between the other two.", secs=30)

Z(HR, "Male and female reproductive systems", I, D,
  "According to NCERT, each seminiferous tubule of the human testis is lined on its inside by which two types of "
  "cells?",
  "Lining of the seminiferous tubule",
  "NCERT: each seminiferous tubule is lined on its inside by two types of cells called male germ cells "
  "(spermatogonia) and Sertoli cells. The regions outside the seminiferous tubules, the interstitial spaces, "
  "contain small blood vessels and interstitial cells or Leydig cells; other immunologically competent cells are "
  "also present there.",
  ["Inside the tubule: spermatogonia + Sertoli cells", "Outside (interstitial spaces): Leydig cells, blood vessels"],
  "The Male Reproductive System",
  at="A", correct="Male germ cells (spermatogonia) and Sertoli cells",
  wrong=["Leydig cells and spermatogonia", "Sertoli cells and Leydig cells",
         "Leydig cells and immunologically competent cells"],
  why="Leydig cells and immunologically competent cells lie in the interstitial spaces outside the tubules, so "
      "every option naming Leydig cells is wrong.", secs=25)

# numerical: date of ovulation in a 28-day cycle
import datetime as _dt
_ov = _dt.date(2026, 6, 3) + _dt.timedelta(days=14 - 1)
assert _ov == _dt.date(2026, 6, 16)
Z(HR, "Menstrual cycle", I, NUM,
  "A woman has regular 28-day menstrual cycles. The menstrual flow of one cycle begins on 3 June, which is day 1 of "
  "that cycle. Using NCERT's account that ovulation takes place in the middle of the cycle (about the 14th day), on "
  "about which date is ovulation expected in this cycle?",
  "Locating ovulation in the cycle",
  "NCERT: the menstrual phase starts the cycle, and both LH and FSH peak in the middle of the cycle (about the 14th "
  "day); the LH surge induces rupture of the Graafian follicle and release of the ovum (ovulation). Day 1 is 3 "
  "June, so day 14 is 13 days later: 16 June.",
  ["Day 1 = 3 June", "Day 14 = 3 June + 13 days", "= 16 June"],
  "Menstrual Cycle",
  at="D", correct="16 June",
  wrong=["17 June", "1 July", "10 June"],
  why="17 June adds 14 days to day 1 (that is day 15); 1 July is day 29, the start of the next cycle; 10 June "
      "(day 8) falls in the follicular phase, before the mid-cycle LH surge.",
  short="Day n of the cycle = start date + (n - 1) days.", secs=45, vb=RECOMPUTED)

_chrom = 23 + 23 + 23   # ootid + second polar body + first polar body, all haploid
assert _chrom == 69
Z(HR, "Gametogenesis", I, NUM,
  "A human primary oocyte (46 chromosomes) completes its first meiotic division before ovulation, and the "
  "secondary oocyte completes its second meiotic division when a sperm enters it. Assume the first polar body "
  "does not divide further. What is the total number of chromosomes present in the ootid (ovum), the second polar "
  "body and the first polar body taken together?",
  "Chromosome numbers in oogenesis",
  "NCERT: the first meiotic division of the primary oocyte is unequal and gives a large haploid secondary oocyte "
  "and a tiny first polar body. When a sperm enters, the secondary oocyte completes the second meiotic division, "
  "giving a second polar body and a haploid ovum (ootid). All three cells are haploid, with 23 chromosomes each.",
  ["First polar body: 23", "Second polar body: 23", "Ootid: 23", "Total = 69"],
  "Gametogenesis; Fertilisation and Implantation",
  at="B", correct="69",
  wrong=["46", "92", "23"],
  why="46 forgets the first polar body; 92 treats the ootid as diploid (46) and adds two haploid polar bodies; "
      "23 counts only the ootid.", secs=50, vb=RECOMPUTED)

Z(HR, "Male and female reproductive systems", A, MUL,
  MS("Which of the following statements correctly compare the human testis and ovary?",
     ["Both are primary sex organs that produce gametes as well as hormones.",
      "The testes lie outside the abdominal cavity in the scrotum, whereas the ovaries lie in the lower abdomen.",
      "Both contain highly coiled seminiferous tubules in which the gametes are produced.",
      "Each testis is about 4 to 5 cm long, whereas each ovary is about 2 to 4 cm long.",
      "The ovarian stroma is divided into a peripheral cortex and an inner medulla, whereas each testicular lobule "
      "contains one to three seminiferous tubules."]),
  "Testis and ovary compared",
  "NCERT: the testes are situated outside the abdominal cavity within a pouch called the scrotum; each testis is "
  "oval, about 4 to 5 cm long and 2 to 3 cm wide, with about 250 lobules each containing one to three seminiferous "
  "tubules in which sperms are produced. The ovaries are located one on each side of the lower abdomen; each ovary "
  "is about 2 to 4 cm long, and its stroma is divided into a peripheral cortex and an inner medulla. Both are "
  "primary sex organs that produce gametes and hormones. Seminiferous tubules occur only in the testis; ova "
  "develop in ovarian follicles.",
  ["(a) true", "(b) true", "(c) false - seminiferous tubules only in the testis", "(d) true", "(e) true"],
  "The Male Reproductive System; The Female Reproductive System",
  at="A", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (c) only", "(b), (d) and (e) only"],
  why="(c) is false because ova develop in ovarian follicles, so every option with (c) is wrong; '(b), (d) and (e) "
      "only' leaves out (a), which is true for both gonads.", secs=60)

Z(HR, "Menstrual cycle", A, MAT,
  ML(("event", "hormone mainly responsible, as described in NCERT"),
     ["Rupture of the Graafian follicle and release of the ovum",
      "Maintenance of the endometrium during the luteal phase",
      "Stronger uterine contractions during parturition",
      "Secretion of factors by Sertoli cells that help in spermiogenesis"],
     ["FSH", "Oxytocin", "LH", "Progesterone"]),
  "Hormonal control of reproductive events",
  "NCERT: the rapid secretion of LH (LH surge) in the middle of the cycle induces rupture of the Graafian follicle "
  "and release of the ovum. Progesterone secreted by the corpus luteum is essential for maintenance of the "
  "endometrium. Oxytocin from the maternal pituitary acts on the uterine muscle and causes stronger uterine "
  "contractions at parturition. FSH acts on the Sertoli cells and stimulates secretion of some factors which help "
  "in the process of spermiogenesis (LH acts on the Leydig cells).",
  ["A -> LH (III)", "B -> progesterone (IV)", "C -> oxytocin (II)", "D -> FSH (I)"],
  "Menstrual Cycle; Gametogenesis; Parturition and Lactation",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "I", "B": "IV", "C": "II", "D": "III"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="Swapping LH and FSH puts ovulation under FSH and the Sertoli cells under LH, which acts on the Leydig cells; "
      "progesterone maintains the endometrium and oxytocin causes the contractions, so swapping them is wrong; "
      "FSH does not cause uterine contractions.", secs=55)

Z(HR, "Gametogenesis", A, ASR,
  AR("The secondary oocyte released at ovulation is haploid, although it has not yet completed meiosis.",
     "Before ovulation, the primary oocyte completes its first meiotic division, which results in a large haploid "
     "secondary oocyte and a tiny first polar body."),
  "Ploidy of the ovulated oocyte",
  "NCERT: the primary oocyte within the tertiary follicle grows in size and completes its first meiotic division. "
  "It is an unequal division resulting in the formation of a large haploid secondary oocyte and a tiny first polar "
  "body. The second meiotic division is completed only when a sperm enters. The haploid state of the ovulated cell "
  "is therefore the result of the completed first meiotic division described in R.",
  ["A: true - secondary oocyte is haploid, meiosis II pending", "R: true - meiosis I completed before ovulation",
   "First meiotic division halves the chromosome number -> R explains A"],
  "Gametogenesis", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; the haploid state comes from "
      "the first meiotic division that R describes, so R is the explanation, not an unrelated fact.", secs=45)

Z(HR, "Menstrual cycle", A, STP,
  SP("During pregnancy, all events of the menstrual cycle stop and there is no menstruation.",
     "Menstruation occurs only if the released ovum is not fertilised."),
  "Menstruation and pregnancy",
  "NCERT: menstruation only occurs if the released ovum is not fertilised; lack of menstruation may be indicative "
  "of pregnancy, though it may also be caused by other underlying causes such as stress or poor health. During "
  "pregnancy all events of the menstrual cycle stop and there is no menstruation.",
  ["Statement I: true", "Statement II: true"],
  "Menstrual Cycle", ans="A",
  why="Both statements are NCERT's own, so options calling either false are wrong. (The converse of II, that "
      "every missed period means pregnancy, is NOT claimed: NCERT adds stress and poor health as other causes.)",
  secs=35)

Z(HR, "Pregnancy, parturition and lactation", A, D,
  "How many of the following are produced by the human OVARY (at some stage of the reproductive life of a woman)?"
  "\n\nRelaxin, estrogen, hCG, progesterone, hPL, oxytocin, prolactin, secondary oocyte",
  "Products of the ovary",
  "NCERT: the ovaries produce the female gamete (ovum, released as the secondary oocyte at ovulation) and several "
  "steroid hormones, estrogen and progesterone. In the later phase of pregnancy, relaxin is secreted by the ovary. "
  "hCG and hPL are made by the placenta; oxytocin is released from the maternal pituitary and prolactin from the "
  "anterior pituitary.",
  ["Ovary: secondary oocyte, estrogen, progesterone, relaxin = 4", "Placenta: hCG, hPL",
   "Pituitary: oxytocin (released), prolactin"],
  "The Female Reproductive System; Pregnancy and Embryonic Development",
  at="B", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three usually forgets relaxin, which NCERT says the ovary secretes late in pregnancy; five or six add "
      "placental hormones (hCG, hPL) or pituitary hormones (prolactin, oxytocin).", secs=50)

Z(HR, "Gametogenesis", A, D,
  "Which pair consists of cells that are BOTH haploid and BOTH formed directly by the second meiotic division?",
  "Products of meiosis II",
  "NCERT: secondary spermatocytes undergo the second meiotic division to produce four equal, haploid spermatids. "
  "The secondary oocyte completes the second meiotic division when a sperm enters, forming a second polar body and "
  "a haploid ovum (ootid). Secondary spermatocytes and the first polar body come from the FIRST meiotic division; "
  "spermatozoa come from spermatids by spermiogenesis, which involves no division; and the primary oocyte is "
  "diploid.",
  ["Meiosis I products: secondary spermatocytes, secondary oocyte + first polar body",
   "Meiosis II products: spermatids, ootid + second polar body", "Spermiogenesis: spermatid -> spermatozoon"],
  "Gametogenesis",
  at="C", correct="Spermatid and second polar body",
  wrong=["Secondary spermatocyte and first polar body", "Spermatozoon and ootid", "Primary oocyte and spermatid"],
  why="Secondary spermatocytes and the first polar body are haploid but come from the first meiotic division; a "
      "spermatozoon is formed by spermiogenesis, not by a division; the primary oocyte is diploid.", secs=50)
