

# ================================================================ Chemical Coordination and Integration (B5 I7 A5)
R_CCI = lambda s: ref("Chemical Coordination and Integration", s)

Z(CCI, "Hypothalamus and pituitary", "Basic", "direct",
  "The pituitary gland is located in a bony cavity called the:",
  ["Foramen magnum", "Acetabulum", "Glenoid cavity", "Sella turcica"], "D",
  "Location of the pituitary",
  "NCERT: the pituitary gland is located in a bony cavity called the sella turcica and is attached to the "
  "hypothalamus by a stalk. The foramen magnum is the opening in the skull through which the medulla continues into "
  "the spinal cord; the acetabulum and glenoid cavity are sockets of the girdles.",
  ["Pituitary → sella turcica, attached to the hypothalamus by a stalk"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="A is an opening of the skull; B is a socket of the pelvic girdle and C of the scapula.",
  seconds=20)

Z(CCI, "Adrenal, pancreas and gonads", "Basic", "direct",
  "The corticoids that are involved in regulating the balance of water and electrolytes in our body are called:",
  ["Glucocorticoids", "Mineralocorticoids", "Catecholamines", "Iodothyronines"], "B",
  "Classes of corticoids",
  "NCERT: the adrenal cortex secretes many hormones, commonly called corticoids. Corticoids involved in carbohydrate "
  "metabolism are glucocorticoids (mainly cortisol); those which regulate the balance of water and electrolytes are "
  "mineralocorticoids (mainly aldosterone). Catecholamines come from the adrenal medulla and iodothyronines from the "
  "thyroid.",
  ["Water and electrolyte balance → mineralocorticoids (aldosterone)"],
  R_CCI("human endocrine system – adrenal gland"),
  why_others_wrong="A regulate carbohydrate metabolism; C are adrenal medullary hormones; D are thyroid hormones.",
  seconds=20)

Z(CCI, "Thyroid, parathyroid and pineal", "Basic", "statement_pair",
  sp("Thyroid hormones control the metabolism of carbohydrates, proteins and fats.",
     "Maintenance of water and electrolyte balance is also influenced by thyroid hormones."),
  STATEMENT_PAIR, "A",
  "Actions of thyroid hormones",
  "NCERT: thyroid hormones play an important role in the regulation of the basal metabolic rate, support RBC "
  "formation, control the metabolism of carbohydrates, proteins and fats, and also influence the maintenance of water "
  "and electrolyte balance.",
  ["Statement I → true", "Statement II → true"],
  R_CCI("human endocrine system – thyroid gland"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=25)

Z(CCI, "Thyroid, parathyroid and pineal", "Basic", "assertion_reason",
  ar("The pineal gland secretes the hormone melatonin.",
     "The pineal gland is located on the dorsal side of the forebrain."),
  ASSERTION_REASON, "B",
  "The pineal gland",
  "NCERT: the pineal gland is located on the dorsal side of the forebrain and secretes a hormone called melatonin. "
  "Both statements are true, but the position of a gland does not explain which hormone it secretes; R does not "
  "explain A.",
  ["A → true", "R → true", "Location does not determine the secretion → R does not explain A"],
  R_CCI("human endocrine system – pineal gland"),
  why_others_wrong="A treats the location as the reason for the secretion; C and D reject true statements.",
  seconds=25)

Z(CCI, "Adrenal, pancreas and gonads", "Basic", "match_list",
  ml(("hormone", "description in NCERT"), ["Insulin", "Glucagon", "Parathyroid hormone", "Melatonin"],
     ["Hypercalcemic hormone", "Regulates the 24-hour (diurnal) rhythm of the body",
      "Hyperglycemic hormone", "Moves glucose rapidly from blood into hepatocytes and adipocytes, lowering blood "
      "glucose (hypoglycemia)"]),
  match_options(M("IV", "III", "I", "II"), [M("III", "IV", "I", "II"), M("IV", "III", "II", "I"),
                                            M("IV", "I", "III", "II")], "C"), "C",
  "Hormones and their effects on blood constituents",
  "NCERT: insulin enhances cellular glucose uptake and utilisation, so glucose moves rapidly from blood to hepatocytes "
  "and adipocytes, resulting in decreased blood glucose (hypoglycemia). Glucagon is a hyperglycemic hormone. "
  "Parathyroid hormone increases the Ca²⁺ level in blood and is a hypercalcemic hormone. Melatonin plays an important "
  "role in the regulation of the 24-hour (diurnal) rhythm of our body.",
  ["Insulin → IV", "Glucagon → III", "PTH → I", "Melatonin → II"],
  R_CCI("human endocrine system – pancreas, parathyroid gland and pineal gland"),
  why_others_wrong="A swaps insulin and glucagon; B swaps PTH and melatonin; D swaps glucagon and PTH.",
  seconds=30)

_opts = ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (b) only", "(a), (b) and (c) only"]
Z(CCI, "Adrenal, pancreas and gonads", "Intermediate", "multi_statement",
  ms("Which of the following are secreted by the adrenal cortex, according to NCERT?",
     ["Cortisol", "Aldosterone", "Small amounts of androgenic steroids", "Adrenaline", "Noradrenaline"]),
  _opts, "D",
  "Secretions of the adrenal cortex and medulla",
  "NCERT: the adrenal cortex secretes corticoids – glucocorticoids (mainly cortisol), mineralocorticoids (mainly "
  "aldosterone) – and small amounts of androgenic steroids, which play a role in the growth of axial, pubic and "
  "facial hair during puberty. Adrenaline (epinephrine) and noradrenaline (norepinephrine), the catecholamines, are "
  "secreted by the adrenal medulla.",
  ["(a) cortex", "(b) cortex", "(c) cortex", "(d) medulla", "(e) medulla"],
  R_CCI("human endocrine system – adrenal gland"),
  why_others_wrong="A and B include medullary catecholamines; C leaves out the androgenic steroids.",
  seconds=40)
ms_check("abc", _opts, "D")

Z(CCI, "Adrenal, pancreas and gonads", "Intermediate", "direct",
  "Which hormone does NCERT describe as producing anti-inflammatory reactions and suppressing the immune response?",
  ["Cortisol", "Aldosterone", "Thymosin", "Adrenaline"], "A",
  "Actions of cortisol",
  "NCERT: glucocorticoids, particularly cortisol, produce anti-inflammatory reactions and suppress the immune "
  "response. Aldosterone acts on the renal tubules; thymosins promote immunity (differentiation of T-lymphocytes and "
  "antibody production); adrenaline is an emergency hormone.",
  ["Anti-inflammatory + immunosuppressive → cortisol (a glucocorticoid)"],
  R_CCI("human endocrine system – adrenal gland"),
  why_others_wrong="B regulates water and electrolyte balance; C promotes rather than suppresses immunity; D prepares "
                   "the body for fight or flight.",
  seconds=30)

Z(CCI, "Hormonal disorders", "Intermediate", "assertion_reason",
  ar("A person with pituitary dwarfism shows stunted growth.",
     "Pituitary dwarfism results from low secretion of growth hormone."),
  ASSERTION_REASON, "A",
  "Growth hormone deficiency",
  "NCERT: low secretion of GH results in stunted growth, resulting in pituitary dwarfism. Stunted growth is the direct "
  "consequence of too little growth hormone, so R explains A.",
  ["A → true", "R → true", "Too little GH → stunted growth → R explains A"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="B misses the direct cause; C and D reject statements that NCERT makes.",
  seconds=25)

Z(CCI, "Hypothalamus and pituitary", "Intermediate", "statement_pair",
  sp("In females, LH induces ovulation of fully mature follicles (Graafian follicles) and maintains the corpus "
     "luteum.",
     "In females, FSH stimulates the growth and development of the ovarian follicles."),
  STATEMENT_PAIR, "A",
  "Gonadotrophins in females",
  "NCERT: in females, LH induces ovulation of fully mature follicles (Graafian follicles) and maintains the corpus "
  "luteum formed from the remnants of the Graafian follicles after ovulation. FSH stimulates the growth and "
  "development of the ovarian follicles in females.",
  ["Statement I → true", "Statement II → true"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=30)

Z(CCI, "Adrenal, pancreas and gonads", "Intermediate", "match_list",
  ml(("hormone", "one effect described in NCERT"), ["Catecholamines", "Androgens", "Estrogens", "Cortisol"],
     ["Stimulates RBC production", "High pitch of voice, among the female secondary sex characters",
      "Pupillary dilation and piloerection (raising of hairs)", "Muscular growth and a low pitch of voice"]),
  match_options(M("III", "IV", "II", "I"), [M("IV", "III", "II", "I"), M("III", "IV", "I", "II"),
                                            M("III", "II", "IV", "I")], "B"), "B",
  "Effects of adrenal and gonadal hormones",
  "NCERT: adrenaline and noradrenaline increase alertness, pupillary dilation, piloerection and sweating. Androgens "
  "stimulate muscular growth, growth of facial and axillary hair, aggressiveness and a low pitch of voice. Estrogens "
  "stimulate the appearance of female secondary sex characters, e.g. a high pitch of voice. Cortisol stimulates RBC "
  "production.",
  ["Catecholamines → III", "Androgens → IV", "Estrogens → II", "Cortisol → I"],
  R_CCI("human endocrine system – adrenal gland; testis; ovary"),
  why_others_wrong="A swaps catecholamines and androgens; C swaps estrogens and cortisol; D swaps androgens and "
                   "estrogens.",
  seconds=40)

Z(CCI, "Hormonal disorders", "Intermediate", "direct",
  "According to NCERT, hypothyroidism in adult women may cause:",
  ["Protruding eyeballs", "Vigorous contraction of the uterus", "Excessive pigmentation of the skin",
   "The menstrual cycle to become irregular"], "D",
  "Effect of hypothyroidism in adult women",
  "NCERT: in adult women, hypothyroidism may cause the menstrual cycle to become irregular. Protruding eyeballs are a "
  "feature of exophthalmic goitre, a form of HYPERthyroidism; vigorous uterine contraction at child birth is caused "
  "by oxytocin; pigmentation is regulated by MSH.",
  ["Hypothyroidism in adult women → irregular menstrual cycle"],
  R_CCI("human endocrine system – thyroid gland"),
  why_others_wrong="A belongs to hyperthyroidism; B is an action of oxytocin; C relates to MSH, not the thyroid.",
  seconds=25)

_opts = ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only", "(a), (b) and (c) only"]
Z(CCI, "Thyroid, parathyroid and pineal", "Intermediate", "multi_statement",
  ms("Which of the following statements about the thymus are correct, according to NCERT?",
     ["It is a lobular structure.",
      "It is located between the lungs behind the sternum on the ventral side of the aorta.",
      "Its hormones, thymosins, play a major role in the differentiation of T-lymphocytes, which provide "
      "cell-mediated immunity.",
      "Thymosins also promote the production of antibodies to provide humoral immunity.",
      "The thymus enlarges in old individuals, increasing the production of thymosins."]),
  _opts, "A",
  "The thymus",
  "NCERT: the thymus gland is a lobular structure located between the lungs behind the sternum on the ventral side "
  "of the aorta. It secretes peptide hormones called thymosins, which play a major role in the differentiation of "
  "T-lymphocytes (cell-mediated immunity) and also promote the production of antibodies (humoral immunity). The "
  "thymus is degenerated in old individuals, resulting in decreased production of thymosins, so their immune "
  "responses become weak.",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false – the thymus degenerates with age"],
  R_CCI("human endocrine system – thymus"),
  why_others_wrong="B and C include (e); D leaves out the correct (d).",
  seconds=50)
ms_check("abcd", _opts, "A")

_opts = ["(a), (b) and (e) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"]
Z(CCI, "Mechanism of hormone action", "Advanced", "multi_statement",
  ms("Compare the action of FSH (a pituitary protein hormone) with that of estradiol (a steroid) on their target "
     "cells. Which of the following statements are correct according to NCERT?",
     ["FSH binds to membrane-bound receptors and does not normally enter the target cell.",
      "Binding of FSH generates second messengers such as cyclic AMP, which regulate cellular metabolism.",
      "Estradiol interacts with intracellular receptors.",
      "The estradiol–receptor complex mostly regulates gene expression or chromosome function by interacting with "
      "the genome.",
      "FSH acts mainly by entering the nucleus and binding to the genome."]),
  _opts, "B",
  "Two mechanisms of hormone action",
  "NCERT: hormones which interact with membrane-bound receptors (peptide, polypeptide and protein hormones, such as "
  "the pituitary hormones) normally do not enter the target cell, but generate second messengers (e.g. cyclic AMP, "
  "IP₃, Ca²⁺) which in turn regulate cellular metabolism. Hormones which interact with intracellular receptors (e.g. "
  "steroid hormones such as estradiol, and iodothyronines) mostly regulate gene expression or chromosome function by "
  "the interaction of the hormone–receptor complex with the genome.",
  ["FSH → protein → membrane receptor → second messenger: (a), (b) true", "Estradiol → steroid → intracellular "
   "receptor → genome: (c), (d) true", "(e) false"],
  R_CCI("mechanism of hormone action"),
  why_others_wrong="A, C and D include (e), which gives FSH the mechanism of a steroid hormone.",
  seconds=60)
ms_check("abcd", _opts, "B")

Z(CCI, "Hormonal disorders", "Advanced", "assertion_reason",
  ar("Hypothyroidism during pregnancy can cause stunted growth (cretinism) of the growing baby.",
     "Hypothyroidism increases the basal metabolic rate."),
  ASSERTION_REASON, "C",
  "Hypothyroidism and hyperthyroidism",
  "NCERT: hypothyroidism during pregnancy causes defective development and maturation of the growing baby, leading to "
  "stunted growth (cretinism), mental retardation, low intelligence quotient, abnormal skin, deaf-mutism, etc. – A is "
  "true. An increased basal metabolic rate is NCERT's description of exophthalmic goitre, a form of HYPERthyroidism; "
  "R is false.",
  ["A → true", "Raised BMR → hyperthyroidism (exophthalmic goitre)", "R → false"],
  R_CCI("human endocrine system – thyroid gland"),
  why_others_wrong="A and B accept a raised BMR in hypothyroidism; D rejects the true A.",
  seconds=40)

Z(CCI, "Hypothalamus and pituitary", "Advanced", "statement_pair",
  sp("Both the pars distalis and the pars intermedia are parts of the adenohypophysis.",
     "In humans, the pars intermedia is almost merged with the pars distalis."),
  STATEMENT_PAIR, "A",
  "Parts of the pituitary",
  "NCERT: the pituitary is divided anatomically into an adenohypophysis and a neurohypophysis. The adenohypophysis "
  "consists of two portions, the pars distalis and the pars intermedia. The pars intermedia secretes only one "
  "hormone, MSH; however, in humans, the pars intermedia is almost merged with the pars distalis.",
  ["Statement I → true", "Statement II → true"],
  R_CCI("human endocrine system – the pituitary gland"),
  why_others_wrong="B, C and D reject at least one correct NCERT statement.",
  seconds=35)

Z(CCI, "Hypothalamus and pituitary", "Advanced", "match_list",
  ml(("pair of hormones", "common feature"),
     ["Oxytocin and vasopressin", "LH and FSH", "Adrenaline and noradrenaline", "Estrogen and progesterone"],
     ["Steroid hormones produced by the ovary", "Catecholamines secreted by the adrenal medulla",
      "Gonadotrophins secreted by the pars distalis",
      "Synthesised by the hypothalamus and released from the neurohypophysis"]),
  match_options(M("IV", "III", "II", "I"), [M("III", "IV", "II", "I"), M("IV", "III", "I", "II"),
                                            M("IV", "II", "III", "I")], "D"), "D",
  "Grouping hormones by origin and nature",
  "NCERT: oxytocin and vasopressin are synthesised by the hypothalamus and transported axonally to the "
  "neurohypophysis, which stores and releases them. LH and FSH, secreted by the pars distalis, stimulate gonadal "
  "activity and are called gonadotrophins. Adrenaline and noradrenaline, from the adrenal medulla, are commonly "
  "called catecholamines. The ovary produces two groups of steroid hormones, estrogen and progesterone.",
  ["Oxytocin, vasopressin → IV", "LH, FSH → III", "Adrenaline, noradrenaline → II", "Estrogen, progesterone → I"],
  R_CCI("human endocrine system"),
  why_others_wrong="A swaps the neurohypophysial hormones and the gonadotrophins; B swaps the catecholamines and the "
                   "ovarian steroids; C swaps the gonadotrophins and the catecholamines.",
  seconds=45)

Z(CCI, "Adrenal, pancreas and gonads", "Advanced", "direct",
  "In a man, the Leydig (interstitial) cells of both testes are destroyed, while the seminiferous tubules and the "
  "pituitary remain intact. Based on NCERT's account of androgens, which outcome is expected?",
  ["Androgen secretion falls, and the functions of the male accessory sex organs, the secondary sex characters and "
   "spermatogenesis are affected",
   "Androgen secretion stays normal, but spermatogenesis stops",
   "Androgen secretion falls, but spermatogenesis is not affected because it does not depend on androgens",
   "The pituitary stops secreting LH and FSH"], "A",
  "Role of androgens",
  "NCERT: the Leydig cells in the intertubular spaces produce androgens, mainly testosterone. Androgens regulate the "
  "development, maturation and functions of the male accessory sex organs (epididymis, vas deferens, seminal "
  "vesicles, prostate gland, urethra, etc.), stimulate muscular growth, facial and axillary hair, aggressiveness and "
  "a low pitch of voice, and play a major stimulatory role in spermatogenesis. Destroying the Leydig cells removes "
  "this source of androgens. Nothing in the stem stops the pituitary from secreting gonadotrophins.",
  ["Leydig cells → androgens", "Androgens → accessory organs, secondary sex characters, spermatogenesis",
   "Loss of Leydig cells → all three affected"],
  R_CCI("human endocrine system – testis"),
  why_others_wrong="B keeps androgens normal although their source is lost; C denies NCERT's stimulatory role of "
                   "androgens in spermatogenesis; D blames the pituitary, which is intact.",
  seconds=50)
