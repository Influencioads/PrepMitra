
# ================================================================ Chemical Coordination and Integration (4/6/4)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "Which one of the following hormones is NOT secreted by the adenohypophysis (pars distalis and pars "
  "intermedia)?",
  "Adenohypophysis versus neurohypophysis",
  "NCERT: the pars distalis produces GH, PRL, TSH, ACTH, LH and FSH, and the pars intermedia secretes only one "
  "hormone, MSH. The pars nervosa (neurohypophysis) stores and releases oxytocin and vasopressin, which are "
  "actually synthesised by the hypothalamus.",
  ["Pars distalis: GH, PRL, TSH, ACTH, LH, FSH", "Pars intermedia: MSH",
   "Neurohypophysis: releases oxytocin and vasopressin (made in hypothalamus)"],
  "Pituitary Gland",
  at="D", correct="Oxytocin",
  wrong=["Melanocyte stimulating hormone", "Prolactin", "Adrenocorticotrophic hormone"],
  why="MSH comes from the pars intermedia, and prolactin and ACTH from the pars distalis, so all three are "
      "adenohypophysis hormones; oxytocin is released from the neurohypophysis.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "The glucocorticoids of the adrenal cortex take part in carbohydrate metabolism. Which hormone does NCERT "
  "name as the main glucocorticoid in our body?",
  "Glucocorticoids and mineralocorticoids",
  "NCERT: corticoids involved in carbohydrate metabolism are called glucocorticoids; in our body, cortisol is the "
  "main glucocorticoid. Corticoids which regulate the balance of water and electrolytes are called "
  "mineralocorticoids, and aldosterone is the main mineralocorticoid.",
  ["Glucocorticoids: carbohydrate metabolism -> main one cortisol",
   "Mineralocorticoids: water and electrolyte balance -> main one aldosterone"],
  "Adrenal Gland",
  at="B", correct="Cortisol",
  wrong=["Aldosterone", "Adrenaline", "Testosterone"],
  why="Aldosterone is the main mineralocorticoid; adrenaline is a catecholamine of the adrenal medulla; "
      "testosterone is the main androgen of the Leydig cells of the testis.", secs=20)

Z(CCI, "Adrenal, pancreas and gonads", B, STP,
  SP("A pair of testes is present in the scrotal sac, outside the abdomen, of male individuals.",
     "A pair of ovaries, the primary female sex organs, is located in the abdomen."),
  "Location of the gonads",
  "NCERT: a pair of testis is present in the scrotal sac (outside abdomen) of male individuals; the testis "
  "performs dual functions as a primary sex organ as well as an endocrine gland. Females have a pair of ovaries "
  "located in the abdomen; the ovary is the primary female sex organ.",
  ["Statement I: true", "Statement II: true"],
  "Testis; Ovary", ans="A",
  why="Both statements are NCERT descriptions, so every option calling either of them false is wrong.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, ASR,
  AR("Deficiency of iodine in the diet results in hypothyroidism and enlargement of the thyroid gland, commonly "
     "called goitre.",
     "Iodine is essential for the normal rate of hormone synthesis in the thyroid gland."),
  "Iodine and the thyroid",
  "NCERT: iodine is essential for the normal rate of hormone synthesis in the thyroid. Deficiency of iodine in our "
  "diet results in hypothyroidism and enlargement of the thyroid gland, commonly called goitre. Without enough "
  "iodine the gland cannot make its hormones at the normal rate, which is why iodine deficiency causes "
  "hypothyroidism; R explains A.",
  ["A: true", "R: true", "Too little iodine -> too little hormone synthesis -> hypothyroidism"],
  "Thyroid Gland", ans="A",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R gives the reason iodine "
      "deficiency lowers thyroid hormone output, so it is not an unrelated statement.", secs=30)

Z(CCI, "Thyroid, parathyroid and pineal", I, MAT,
  ML(("hormone", "one of its actions described in NCERT"),
     ["Melatonin", "Cortisol", "Thyroid hormones", "Androgens"],
     ["Anabolic (synthetic) effects on protein and carbohydrate metabolism",
      "Influences the menstrual cycle",
      "Maintenance of water and electrolyte balance",
      "Produces anti-inflammatory reactions and suppresses the immune response"]),
  "Less familiar hormone actions",
  "NCERT: melatonin also influences metabolism, pigmentation, the menstrual cycle and our defence capability. "
  "Glucocorticoids, particularly cortisol, produce anti-inflammatory reactions and suppress the immune response. "
  "Maintenance of water and electrolyte balance is also influenced by thyroid hormones. Androgens produce "
  "anabolic (synthetic) effects on protein and carbohydrate metabolism.",
  ["A -> II", "B -> IV", "C -> III", "D -> I"],
  "Pineal Gland; Thyroid Gland; Adrenal Gland; Testis",
  at="D", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Anti-inflammatory and immunosuppressive action belongs to cortisol, not to thyroid hormones or melatonin; "
      "the anabolic effect is an androgen action, not a melatonin action.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, MUL,
  MS("Which of the following hormones are produced by cells of the gonads (testis or ovary)?",
     ["Testosterone", "Estrogen", "Progesterone", "Follicle stimulating hormone", "Gonadotrophin releasing hormone"]),
  "Hormones of the gonads",
  "NCERT: Leydig cells in the intertubular spaces of the testis produce androgens, mainly testosterone. In the "
  "ovary, estrogen is synthesised and secreted mainly by the growing ovarian follicles, and the corpus luteum "
  "(formed from the ruptured follicle after ovulation) secretes mainly progesterone. FSH is a pars distalis "
  "hormone that acts on the gonads, and GnRH is a hypothalamic hormone acting on the pituitary.",
  ["(a) Leydig cells", "(b) growing follicles", "(c) corpus luteum", "(d) pituitary - acts ON gonads",
   "(e) hypothalamus"],
  "Testis; Ovary",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="FSH and GnRH regulate the gonads but are made in the pituitary and the hypothalamus respectively, so every "
      "option containing (d) or (e) is wrong.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", I, D,
  "Which of the following actions does NCERT ascribe to BOTH the glucocorticoids (such as cortisol) and the "
  "catecholamines (adrenaline and noradrenaline)?",
  "Comparing adrenal cortex and adrenal medulla hormones",
  "NCERT: glucocorticoids stimulate gluconeogenesis, lipolysis and proteolysis; cortisol also produces "
  "anti-inflammatory reactions, suppresses the immune response and stimulates RBC production. Catecholamines "
  "increase alertness, pupillary dilation, piloerection and sweating, increase heart beat and rate of respiration, "
  "stimulate glycogen breakdown, and also stimulate the breakdown of lipids and proteins. Breakdown of lipids and "
  "proteins is the action common to both.",
  ["Glucocorticoids: lipolysis + proteolysis (+ gluconeogenesis)",
   "Catecholamines: breakdown of lipids and proteins (+ glycogen breakdown)", "Common: lipids and proteins broken down"],
  "Adrenal Gland",
  at="A", correct="Stimulating the breakdown of lipids and proteins",
  wrong=["Causing pupillary dilation and piloerection", "Suppressing the immune response",
         "Stimulating RBC production"],
  why="Pupillary dilation and piloerection are catecholamine effects only; suppression of the immune response and "
      "stimulation of RBC production are given for cortisol only.", secs=40)

Z(CCI, "Thyroid, parathyroid and pineal", I, ASR,
  AR("Thyroid hormones support the process of red blood cell formation.",
     "The thyroid gland is composed of follicles and stromal tissues."),
  "Thyroid structure and functions",
  "NCERT: the thyroid gland is composed of follicles and stromal tissues, each follicle being composed of "
  "follicular cells enclosing a cavity. Separately, NCERT lists among the actions of thyroid hormones that they "
  "support the process of red blood cell formation. Both are true, but the histology of the gland does not "
  "explain why its hormones support RBC formation.",
  ["A: true", "R: true", "R is structure of the gland, A is an action of its hormones -> unrelated"],
  "Thyroid Gland", ans="B",
  why="Both statements are NCERT facts, so options with a false statement are wrong; R describes the gland's "
      "tissue make-up, which says nothing about the hormones' effect on RBC formation, so it is not the "
      "explanation.", secs=35)

Z(CCI, "Thyroid, parathyroid and pineal", I, STP,
  SP("Thyroxine (tetraiodothyronine) and triiodothyronine, the hormones of the thyroid follicular cells, are "
     "iodothyronines.",
     "Thyrocalcitonin (TCT), which is also secreted by the thyroid gland, is an iodothyronine as well."),
  "Chemical nature of thyroid secretions",
  "NCERT: the follicular cells synthesise two hormones, tetraiodothyronine or thyroxine (T4) and "
  "triiodothyronine (T3); in the classification of hormones by chemical nature, iodothyronines are the thyroid "
  "hormones. The thyroid gland also secretes a PROTEIN hormone called thyrocalcitonin (TCT), which regulates the "
  "blood calcium level.",
  ["Statement I: true (T4 and T3 are iodothyronines)", "Statement II: false - TCT is a protein hormone"],
  "Thyroid Gland; Mechanism of Hormone Action", ans="C",
  why="Statement II is false because NCERT calls TCT a protein hormone, so options calling it true are wrong; "
      "Statement I is true, so options calling it false are wrong.", secs=35)

Z(CCI, "Hypothalamus and pituitary", I, D,
  "A hormone has these three features: it is synthesised by hypothalamic neurons; it is stored in and released "
  "from the neurohypophysis; and it acts mainly at the kidney, reducing the loss of water through urine. The "
  "hormone is:",
  "Identifying a hormone from its features",
  "NCERT: the pars nervosa stores and releases oxytocin and vasopressin, which are synthesised by the "
  "hypothalamus and transported axonally to the neurohypophysis. Vasopressin acts mainly at the kidney and "
  "stimulates resorption of water and electrolytes by the distal tubules, thereby reducing loss of water through "
  "urine (diuresis); hence it is also called the anti-diuretic hormone (ADH).",
  ["Hypothalamic synthesis + neurohypophysis release -> oxytocin or vasopressin",
   "Acts on kidney, reduces water loss -> vasopressin (ADH)"],
  "Hypothalamus; Pituitary Gland",
  at="D", correct="Vasopressin",
  wrong=["Oxytocin", "Aldosterone", "Parathyroid hormone"],
  why="Oxytocin shares the origin and release route but acts on smooth muscles (uterus, mammary glands), not the "
      "kidney; aldosterone and PTH act on renal tubules but come from the adrenal cortex and the parathyroid "
      "glands, not from hypothalamic neurons.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following actions does NCERT attribute to ESTROGENS?",
     ["Stimulation of growth and activities of the female secondary sex organs",
      "Development of the growing ovarian follicles",
      "Stimulation of the formation of alveoli in the mammary glands and of milk secretion",
      "Regulation of female sexual behaviour",
      "Induction of ovulation of the fully mature Graafian follicle"]),
  "Actions of estrogens",
  "NCERT: estrogen performs a wide range of actions such as stimulation of growth and activities of female "
  "secondary sex organs, development of growing ovarian follicles, appearance of female secondary sex characters "
  "and mammary gland development; estrogens also regulate female sexual behaviour. The formation of alveoli (sac-"
  "like structures which store milk) and milk secretion is stimulated by PROGESTERONE, and ovulation of the "
  "Graafian follicle is induced by LH.",
  ["(a) true", "(b) true", "(c) false - progesterone", "(d) true", "(e) false - LH"],
  "Ovary; Pituitary Gland",
  at="C", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(c) is a progesterone action and (e) is an LH action, so every option containing either is wrong; (a), "
      "(b) and (d) are the estrogen actions listed by NCERT.", secs=50)

Z(CCI, "Mechanism of hormone action", A, MAT,
  ML(("hormone", "chemical nature"),
     ["Thyrocalcitonin", "Triiodothyronine", "Progesterone", "Epinephrine"],
     ["Steroid", "Protein hormone", "Amino-acid derivative", "Iodothyronine"]),
  "Chemical classes of hormones",
  "NCERT groups hormones into peptide, polypeptide and protein hormones; steroids (e.g. cortisol, testosterone, "
  "estradiol and progesterone); iodothyronines (thyroid hormones); and amino-acid derivatives (e.g. epinephrine). "
  "The trap is thyrocalcitonin: although it comes from the thyroid gland, NCERT calls it a protein hormone, while "
  "triiodothyronine is an iodothyronine.",
  ["A thyrocalcitonin -> protein (II)", "B triiodothyronine -> iodothyronine (IV)", "C progesterone -> steroid (I)",
   "D epinephrine -> amino-acid derivative (III)"],
  "Mechanism of Hormone Action; Thyroid Gland",
  at="B", match=({"A": "II", "B": "IV", "C": "I", "D": "III"},
                 [{"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="Calling TCT an iodothyronine (and T3 a protein) confuses the two thyroid secretions; epinephrine is an "
      "amino-acid derivative, not a protein; and progesterone is a steroid, not an amino-acid derivative.",
  secs=50)

Z(CCI, "Hormonal disorders", A, ASR,
  AR("Both cretinism and exophthalmic goitre are disorders involving the thyroid gland.",
     "Both cretinism and exophthalmic goitre are forms of hyperthyroidism."),
  "Hypo- and hyperthyroid disorders",
  "NCERT: hypothyroidism during pregnancy causes defective development and maturation of the growing baby, "
  "leading to stunted growth (cretinism), mental retardation and other defects. Exophthalmic goitre (Graves' "
  "disease) is a form of hyperthyroidism, characterised by enlargement of the thyroid, protruding eyeballs, "
  "increased BMR and weight loss. So both involve the thyroid (A true), but cretinism results from "
  "HYPOthyroidism (R false).",
  ["A: true - both are thyroid disorders", "R: false - cretinism is due to hypothyroidism"],
  "Thyroid Gland", ans="C",
  why="R is false because cretinism is a hypothyroid condition, so options treating R as true are wrong; A is true, "
      "so 'A is false but R is true' is wrong.", secs=40)

Z(CCI, "Mechanism of hormone action", A, D,
  "How many of the following hormones are steroids, according to NCERT's classification of hormones by chemical "
  "nature?\n\nCortisol, thyroxine, testosterone, insulin, estradiol, epinephrine, progesterone, glucagon",
  "Steroid hormones",
  "NCERT: steroids include cortisol, testosterone, estradiol and progesterone. Thyroxine is an iodothyronine, "
  "insulin and glucagon are peptide (protein) hormones, and epinephrine is an amino-acid derivative.",
  ["Steroids: cortisol, testosterone, estradiol, progesterone = 4",
   "Not steroids: thyroxine (iodothyronine), insulin and glucagon (peptide), epinephrine (amino-acid derivative)"],
  "Mechanism of Hormone Action",
  at="D", correct="Four",
  wrong=["Three", "Five", "Six"],
  why="Three leaves out one of NCERT's four steroid examples; five adds thyroxine, which also acts through "
      "intracellular receptors but is an iodothyronine, not a steroid; six adds insulin and glucagon or "
      "epinephrine.", secs=45)
