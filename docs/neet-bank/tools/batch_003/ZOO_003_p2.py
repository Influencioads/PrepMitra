"""Builder for package ZOO_003_p2 of BATCH_003 (Zoology, 122 questions, NEET_ZOO_000629..NEET_ZOO_000750).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_003/ZOO_003_p2.py      (run from docs/neet-bank)
"""

import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
ZOO = "Zoology"
PACKAGE = "ZOO_003_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_003_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_003_ZOO_p2.json"
FIRST_ID = 629

CHECKED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

CCI = "Chemical Coordination and Integration"
HR = "Human Reproduction"
RH = "Reproductive Health"
EVO = "Evolution"
HHD = "Human Health and Disease"
BPP = "Biotechnology: Principles and Processes"
BTA = "Biotechnology and its Applications"

REF = {
    CCI: "Class 11 Biology, Ch 19 'Chemical Coordination and Integration'",
    HR: "Class 12 Biology, Ch 2 'Human Reproduction'",
    RH: "Class 12 Biology, Ch 3 'Reproductive Health'",
    EVO: "Class 12 Biology, Ch 6 'Evolution'",
    HHD: "Class 12 Biology, Ch 7 'Human Health and Disease'",
    BPP: "Class 12 Biology, Ch 9 'Biotechnology: Principles and Processes'",
    BTA: "Class 12 Biology, Ch 10 'Biotechnology and its Applications'",
}

QUESTIONS = []


def match_options(correct: dict, wrong: list, at: str) -> list:
    """Option texts for a match-the-list question with the correct code at position `at` (as in the sample)."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4
    return opts


def AR(a, r):
    return ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {a}\nReason (R): {r}\n\nChoose the correct answer from the options given below:")


def SP(s1, s2):
    return (f"Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")


def ML(intro, list1, list2):
    l1 = "\n".join(f"{k}. {t}" for k, t in zip("ABCD", list1))
    l2 = "\n".join(f"{k}. {t}" for k, t in zip(["I", "II", "III", "IV"], list2))
    return (f"Match List-I ({intro[0]}) with List-II ({intro[1]}).\n\nList-I:\n{l1}\n\nList-II:\n{l2}\n\n"
            "Choose the correct answer from the options given below:")


def MS(intro, stmts):
    body = "\n".join(f"({chr(97 + i)}) {s}" for i, s in enumerate(stmts))
    return f"{intro}\n\n{body}\n\nChoose the correct answer from the options given below:"


def Z(topic, sub, diff, fmt, text, concept, expl, steps, sec, *, at=None, ans=None, correct=None, wrong=None,
      match=None, why=None, short=None, secs=45, vb=CHECKED):
    """Adds one question. AR/SP take `ans` (fixed option set); match_list takes match=(correct_dict, [3 wrong
    dicts]) and `at`; every other format takes `correct`, three `wrong` texts and `at` (the fixed key)."""
    qid = f"NEET_ZOO_{FIRST_ID + len(QUESTIONS):06d}"
    if fmt == "assertion_reason":
        assert at is None, qid
        options, answer = list(ASSERTION_REASON), ans
    elif fmt == "statement_pair":
        assert at is None, qid
        options, answer = list(STATEMENT_PAIR), ans
    elif fmt == "match_list":
        assert ans is None and at in LETTERS, qid
        answer = at
        options = match_options(match[0], match[1], at)
    else:
        assert ans is None and at in LETTERS, qid
        assert len(wrong) == 3 and correct not in wrong, qid
        answer = at
        options = list(wrong)
        options.insert(LETTERS.index(at), correct)
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, qid
    assert why, qid
    QUESTIONS.append({
        "question_id": qid, "exam_mappings": default_mappings(ZOO), "subject": ZOO, "topic": topic,
        "subtopic": sub, "difficulty": diff, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": expl, "steps": steps, "shortcut": short,
                     "why_others_wrong": why, "ncert_reference": f"{REF[topic]}, {sec}",
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": secs,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(vb), "verified_at": TODAY},
    })


B, I, A = "Basic", "Intermediate", "Advanced"
D, NUM, ASR, STP, MAT, MUL = "direct", "numerical", "assertion_reason", "statement_pair", "match_list", "multi_statement"

# ================================================================ verification of computable answers
# EVO: genotype frequencies AA 0.45, Aa 0.30, aa 0.25 -> q = f(aa) + f(Aa)/2
g_AA, g_Aa, g_aa = F(45, 100), F(30, 100), F(25, 100)
assert g_AA + g_Aa + g_aa == 1
assert g_aa + g_Aa / 2 == F(40, 100)                           # correct: q = 0.40
assert g_AA + g_Aa / 2 == F(60, 100)                           # p = 0.60, so p + q = 1
assert g_aa + g_Aa == F(55, 100)                               # distractor: Aa not halved
assert F(1, 2) * F(1, 2) == g_aa                               # distractor 0.50: sqrt of f(aa), assumes equilibrium
assert F(40, 100) ** 2 == F(16, 100) != g_aa                   # so the population is not in equilibrium

# EVO: rare recessive disorder, 1 in 10,000 affected (q^2) -> q = 1/100, p = 99/100, carriers 2pq
q_r = F(1, 100)
assert q_r * q_r == F(1, 10_000)
carriers = 2 * (1 - q_r) * q_r
assert carriers == F(198, 10_000)                              # 0.0198, i.e. about 1 in 50 (2%)
assert abs(1 / carriers - 50) < 1                              # 1/0.0198 = 50.5 -> "about 1 in 50"
assert 1 / q_r == 100 and 1 / (2 * q_r * q_r) == 5_000         # distractors: q alone; 2q^2

# BPP: PCR from 1 double-stranded molecule, 5 cycles, semi-conservative copying
total = 2 ** 5
with_parent = 2                                                # the two original strands end up in two molecules
assert total == 32 and total - with_parent == 30               # correct: 30
assert total - 1 == 31 and total // 2 == 16                    # distractors

# BPP: pBR322 with insert at BamHI (inside tetR); 200 colonies on ampicillin, 150 of them also grow on tetracycline
amp, tet = 200, 150
assert amp - tet == 50                                         # correct: recombinants have lost tetracycline resistance
assert amp + tet == 350                                        # distractor: added the counts

# BPP: insert with EcoRI ends ligated into the single EcoRI site of a circular plasmid
junctions, strands = 2, 2
assert junctions * strands == 4                                # correct: 4 phosphodiester bonds sealed by ligase
assert junctions * 1 == 2 and junctions * strands * 2 == 8     # distractors

# BTA: Rosie's milk, 2.4 g/L human alpha-lactalbumin; 15 L of milk a day for 7 days
conc, litres, days = F(24, 10), 15, 7
assert conc * litres * days == 252                             # correct: 252 g
assert conc * litres == 36                                     # distractor: one day only
assert conc * days == F(168, 10)                               # distractor: forgot the volume

# ================================================================ Chemical Coordination and Integration (5/7/5)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "Anatomically, the pituitary gland is divided into an adenohypophysis and a neurohypophysis. The "
  "adenohypophysis consists of which two portions?",
  "Parts of the pituitary gland",
  "The adenohypophysis consists of two portions, the pars distalis and the pars intermedia. The neurohypophysis is "
  "the pars nervosa (posterior pituitary).",
  ["Adenohypophysis = pars distalis + pars intermedia", "Neurohypophysis = pars nervosa"],
  "The pituitary gland",
  at="B", correct="Pars distalis and pars intermedia",
  wrong=["Pars distalis and pars nervosa", "Pars intermedia and pars nervosa", "Pars nervosa and the hypothalamus"],
  why="The pars nervosa is the neurohypophysis, not a part of the adenohypophysis; the hypothalamus is part of the "
      "brain, not of the pituitary.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "An endocrine gland is composed of follicles and stromal tissues; each follicle consists of follicular cells "
  "enclosing a cavity, and iodine is essential for the normal rate of its hormone synthesis. The gland is the:",
  "Structure of the thyroid gland",
  "The thyroid gland is composed of follicles and stromal tissues. Each thyroid follicle is made of follicular cells "
  "enclosing a cavity; these cells synthesise thyroxine (T4) and triiodothyronine (T3). Iodine is essential for the "
  "normal rate of thyroid hormone synthesis.",
  ["Follicles of follicular cells around a cavity", "Iodine needed for hormone synthesis", "Thyroid gland"],
  "The thyroid gland",
  at="A", correct="Thyroid gland",
  wrong=["Parathyroid gland", "Pineal gland", "Adrenal medulla"],
  why="None of the other glands is built of follicles around a cavity or depends on iodine for its hormones.",
  secs=30)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "The adrenal gland is composed of two types of tissues. Which of the following correctly describes their "
  "arrangement?",
  "Structure of the adrenal gland",
  "The centrally located tissue of the adrenal gland is the adrenal medulla; the adrenal cortex lies outside it.",
  ["Centre: adrenal medulla", "Outside: adrenal cortex"],
  "The adrenal gland",
  at="A", correct="The adrenal medulla is centrally located and the adrenal cortex lies outside it",
  wrong=["The adrenal cortex is centrally located and the adrenal medulla lies outside it",
         "The adrenal medulla and adrenal cortex lie side by side as two lobes joined by an isthmus",
         "The adrenal medulla forms the outermost layer, the zona glomerulosa"],
  why="The cortex surrounds the medulla, not the reverse; an isthmus joins the two lobes of the thyroid; the zona "
      "glomerulosa is the outer layer of the cortex, not the medulla.", secs=25)

Z(CCI, "Mechanism of hormone action", B, D,
  "Hormones produce their effects on target tissues by binding to specific proteins called hormone receptors. "
  "These receptors are located:",
  "Hormone receptors",
  "NCERT states that hormones produce their effects by binding to specific proteins called hormone receptors, which "
  "are located in the target tissues only.",
  ["Receptors are specific proteins", "They are present in the target tissues only"],
  "Mechanism of hormone action",
  at="B", correct="In the target tissues only",
  wrong=["In every cell of the body", "Only in the endocrine gland that secretes the hormone",
         "Only in the blood plasma, which carries the hormone"],
  why="If every cell had the receptor, every cell would be a target; the secreting gland and the blood carry the "
      "hormone but are not where its receptors lie.", secs=25)

Z(CCI, "Hormonal disorders", B, D,
  "Excess secretion of growth hormone in adults, especially in middle age, can result in a condition called "
  "acromegaly. This condition is characterised by:",
  "Acromegaly",
  "Excess secretion of growth hormone in adults, especially in middle age, can result in severe disfigurement "
  "(especially of the face) called acromegaly. It may lead to serious complications and premature death if "
  "unchecked.",
  ["Excess GH in adults (middle age)", "Severe disfigurement, especially of the face = acromegaly"],
  "The pituitary gland",
  at="D", correct="Severe disfigurement, especially of the face",
  wrong=["Stunted growth from childhood (dwarfism)", "Protruding eyeballs and weight loss",
         "Excessive loss of water in urine and dehydration"],
  why="Stunted growth is pituitary dwarfism (low GH); protruding eyeballs and weight loss describe exophthalmic "
      "goitre; excessive water loss describes diabetes insipidus (ADH problem).", secs=30)

Z(CCI, "Hypothalamus and pituitary", I, MAT,
  ML(("hormone", "action"),
     ["Vasopressin", "FSH (in females)", "LH (in females)", "TSH"],
     ["Stimulates growth and development of the ovarian follicles",
      "Stimulates resorption of water and electrolytes by the distal tubules of the kidney",
      "Stimulates synthesis and secretion of thyroid hormones from the thyroid gland",
      "Induces ovulation of fully mature (Graafian) follicles and maintains the corpus luteum"]),
  "Actions of pituitary hormones",
  "Vasopressin acts mainly at the kidney and stimulates resorption of water and electrolytes by the distal tubules "
  "(hence ADH). In females, FSH stimulates growth and development of the ovarian follicles, while LH induces "
  "ovulation of fully mature follicles and maintains the corpus luteum. TSH stimulates the synthesis and secretion "
  "of thyroid hormones.",
  ["A Vasopressin -> II (distal tubules)", "B FSH -> I (follicle growth)", "C LH -> IV (ovulation, corpus luteum)",
   "D TSH -> III (thyroid hormones)"],
  "The pituitary gland",
  at="B", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "IV", "B": "II", "C": "I", "D": "III"}]),
  why="Swapping FSH and LH ignores that FSH grows follicles while LH triggers ovulation; vasopressin acts on the "
      "kidney, not the thyroid, and TSH acts on the thyroid, not the kidney.", secs=50)

Z(CCI, "Thyroid, parathyroid and pineal", I, MUL,
  MS("Which of the following statements about parathyroid hormone (PTH) are correct?",
     ["PTH acts on bones and stimulates bone resorption (dissolution/demineralisation).",
      "PTH stimulates the reabsorption of Ca²⁺ by the renal tubules.",
      "PTH increases the absorption of Ca²⁺ from the digested food.",
      "The secretion of PTH is regulated by the circulating level of TSH.",
      "PTH is a steroid hormone."]),
  "Actions and regulation of PTH",
  "PTH is a peptide hormone that raises blood Ca²⁺: it stimulates bone resorption, reabsorption of Ca²⁺ by the renal "
  "tubules and Ca²⁺ absorption from digested food. Its secretion is regulated by the circulating levels of calcium "
  "ions, not by TSH.",
  ["(a) True", "(b) True", "(c) True", "(d) False: regulated by blood Ca²⁺ level", "(e) False: peptide hormone"],
  "Parathyroid gland",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(a) and (e) only", "(b), (c) and (e) only"],
  why="Any option with (d) or (e) is wrong: PTH secretion follows blood calcium, and PTH is a peptide, not a "
      "steroid.", secs=55)

Z(CCI, "Thyroid, parathyroid and pineal", I, MUL,
  MS("Besides regulating the 24-hour (diurnal) rhythm of the body, melatonin from the pineal gland also influences:",
     ["Metabolism", "Pigmentation", "The menstrual cycle", "Our defence capability",
      "The level of calcium in the blood"]),
  "Functions of melatonin",
  "NCERT: melatonin regulates the diurnal rhythm and also influences metabolism, pigmentation, the menstrual cycle "
  "and our defence capability. Blood calcium is regulated by PTH and thyrocalcitonin, not melatonin.",
  ["(a)-(d) are listed by NCERT", "(e) is the job of PTH and TCT"],
  "Pineal gland",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c) and (d) only", "(a), (b), (c), (d) and (e)"],
  why="Options containing (e) wrongly add calcium regulation; '(c) and (d) only' leaves out metabolism and "
      "pigmentation, which NCERT lists.", secs=45)

Z(CCI, "Hormonal disorders", I, ASR,
  AR("Cancer of the thyroid gland or development of nodules in it may lead to hyperthyroidism, which adversely "
     "affects the body physiology.",
     "Hyperthyroidism is caused by a deficiency of iodine in the diet."),
  "Hyperthyroidism",
  "NCERT: cancer of the thyroid gland or development of thyroid nodules may lead to abnormally high levels of "
  "thyroid hormone synthesis (hyperthyroidism), which adversely affects body physiology. Iodine deficiency instead "
  "causes hypothyroidism and enlargement of the thyroid (goitre).",
  ["A: true (NCERT)", "R: false - iodine deficiency gives hypothyroidism/goitre"],
  "The thyroid gland", ans="C",
  why="R is false, so options A and B are wrong; A is an NCERT statement, so D is wrong.", secs=45)

Z(CCI, "Hormonal disorders", I, D,
  "A pregnant woman suffers from untreated hypothyroidism. Which set of features is the developing baby most likely "
  "to show?",
  "Effect of hypothyroidism during pregnancy",
  "Hypothyroidism during pregnancy causes defective development and maturation of the growing baby, leading to "
  "stunted growth (cretinism), mental retardation, low intelligence quotient, abnormal skin and deaf-mutism.",
  ["Maternal hypothyroidism -> defective development of the baby",
   "Features: stunted growth, mental retardation, low IQ, abnormal skin, deaf-mutism"],
  "The thyroid gland",
  at="B", correct="Stunted growth, mental retardation, low IQ, abnormal skin and deaf-mutism",
  wrong=["Protruding eyeballs, increased basal metabolic rate and weight loss",
         "Abnormal increase in height (gigantism)",
         "Excessive urination and thirst due to impaired ADH release"],
  why="Protruding eyeballs with high BMR is hyperthyroidism (Graves' disease); gigantism comes from excess GH; "
      "excessive urination from ADH deficiency is diabetes insipidus.", secs=40)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("The adrenal cortex secretes many hormones, commonly called corticoids.",
     "The corticoids that are involved in carbohydrate metabolism are called mineralocorticoids."),
  "Classes of corticoids",
  "The adrenal cortex secretes corticoids. Those involved in carbohydrate metabolism are glucocorticoids (e.g. "
  "cortisol); those that regulate the balance of water and electrolytes are mineralocorticoids (e.g. aldosterone).",
  ["Statement I: true", "Statement II: false - carbohydrate metabolism = glucocorticoids"],
  "The adrenal gland", ans="C",
  why="Statement II swaps the two classes of corticoids, so options calling it true are wrong; Statement I is the "
      "NCERT definition, so it is not false.", secs=40)

Z(CCI, "Adrenal, pancreas and gonads", I, ASR,
  AR("Besides producing ova, the ovary also functions as an endocrine gland.",
     "The ovary produces two groups of steroid hormones called estrogen and progesterone."),
  "Endocrine role of the ovary",
  "The ovary is the primary female sex organ that produces one ovum in each menstrual cycle. It is also an endocrine "
  "gland because it produces two groups of steroid hormones, estrogen and progesterone.",
  ["A: true", "R: true", "Secreting hormones is what makes the ovary an endocrine gland, so R explains A"],
  "Gonads", ans="A",
  why="R gives exactly why the ovary counts as an endocrine gland, so B is wrong; both statements are true, so C "
      "and D are wrong.", secs=40)

Z(CCI, "Adrenal, pancreas and gonads", A, MAT,
  ML(("hormone", "action"),
     ["Estrogens", "Glucagon", "Adrenaline and noradrenaline", "Progesterone"],
     ["Supports pregnancy",
      "Increase alertness, pupillary dilation, piloerection (raising of hairs) and sweating",
      "Stimulate the growth and activities of the female secondary sex organs",
      "Acts mainly on hepatocytes and stimulates glycogenolysis, raising the blood sugar"]),
  "Actions of hormones of the adrenal, pancreas and gonads",
  "Estrogens stimulate the growth and activities of female secondary sex organs; glucagon acts mainly on liver "
  "cells and stimulates glycogenolysis, causing hyperglycemia; catecholamines (adrenaline and noradrenaline) "
  "increase alertness, pupillary dilation, piloerection and sweating; progesterone supports pregnancy.",
  ["A Estrogens -> III", "B Glucagon -> IV", "C Catecholamines -> II", "D Progesterone -> I"],
  "The adrenal gland; Pancreas; Testis and ovary",
  at="D", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "I", "B": "IV", "C": "II", "D": "III"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="Swapping estrogens and progesterone confuses the follicle hormone with the pregnancy-supporting hormone; "
      "glucagon acts on hepatocytes, while piloerection and pupillary dilation are emergency effects of "
      "catecholamines.", secs=60)

Z(CCI, "Hypothalamus and pituitary", A, MUL,
  MS("Which of the following statements about the pituitary gland are correct?",
     ["The pars distalis region is commonly called the anterior pituitary.",
      "The neurohypophysis (pars nervosa) is also known as the posterior pituitary.",
      "The pars distalis produces GH, PRL, TSH, ACTH, LH and FSH.",
      "Oxytocin is produced by the pars distalis.",
      "Growth hormone is stored in and released from the neurohypophysis."]),
  "Regions of the pituitary and their hormones",
  "The pars distalis (anterior pituitary) produces GH, prolactin, TSH, ACTH, LH and FSH. The neurohypophysis (pars "
  "nervosa, posterior pituitary) stores and releases oxytocin and vasopressin, which are synthesised by the "
  "hypothalamus. GH is an anterior pituitary hormone.",
  ["(a) True", "(b) True", "(c) True", "(d) False: oxytocin is made by the hypothalamus and released from the "
   "posterior pituitary", "(e) False: the neurohypophysis stores oxytocin and vasopressin, not GH"],
  "The pituitary gland",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(d) puts oxytocin in the wrong lobe and (e) puts GH in the wrong lobe, so every option containing either is "
      "wrong.", secs=65)

Z(CCI, "Hormonal disorders", A, MUL,
  MS("Which of the following statements about hormonal disorders are correct?",
     ["Acromegaly is hard to diagnose in the early stages and often goes undetected for many years, until changes "
      "in external features become noticeable.",
      "In adult women, hypothyroidism may cause the menstrual cycle to become irregular.",
      "Diabetes insipidus results from a deficiency of insulin.",
      "Patients with diabetes mellitus are successfully treated with insulin therapy.",
      "A low level of ADH increases water reabsorption by the kidney, so very little urine is formed."]),
  "Hormonal disorders",
  "Acromegaly is hard to diagnose early and often goes undetected for years. Hypothyroidism in adult women may make "
  "the menstrual cycle irregular. Diabetes insipidus is due to impaired synthesis or release of ADH, which causes "
  "excessive loss of water (diuresis), not water retention. Diabetes mellitus (insulin-related) is successfully "
  "treated with insulin therapy.",
  ["(a) True", "(b) True", "(c) False: ADH, not insulin", "(d) True",
   "(e) False: low ADH reduces water reabsorption and causes diuresis"],
  "The pituitary gland; The thyroid gland; Pancreas",
  at="C", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"],
  why="(c) mixes up diabetes insipidus (ADH) with diabetes mellitus (insulin); (e) reverses the effect of low ADH; "
      "every other option includes one of them.", secs=70)

Z(CCI, "Hypothalamus and pituitary", A, STP,
  SP("In males, LH and androgens regulate spermatogenesis.",
     "Growth hormone is secreted by the pars intermedia of the pituitary."),
  "Gonadotrophins and growth hormone",
  "In males, FSH (not LH) and androgens regulate spermatogenesis; LH stimulates the synthesis and secretion of "
  "androgens. Growth hormone is secreted by the pars distalis; the pars intermedia secretes only MSH.",
  ["Statement I: false - FSH and androgens regulate spermatogenesis", "Statement II: false - GH is from the pars "
   "distalis"],
  "The pituitary gland", ans="B",
  why="Both statements carry a swapped name (LH for FSH, pars intermedia for pars distalis), so any option calling "
      "either true is wrong.", secs=50)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following statements about the gonads are correct?",
     ["The ovary is composed of ovarian follicles and stromal tissues.",
      "Progesterone is the hormone secreted mainly by the growing ovarian follicles before ovulation.",
      "After ovulation, the ruptured follicle is converted into the corpus luteum, which secretes mainly "
      "progesterone.",
      "The testis performs dual functions, as a primary sex organ and as an endocrine gland.",
      "The Leydig cells are located inside the seminiferous tubules."]),
  "Testis and ovary as endocrine glands",
  "The ovary has ovarian follicles and stromal tissues; growing follicles secrete estrogen, and after ovulation the "
  "ruptured follicle becomes the corpus luteum, which secretes mainly progesterone. The testis is both a primary sex "
  "organ and an endocrine gland; it has seminiferous tubules and stromal (interstitial) tissue, and the Leydig cells "
  "lie in the intertubular spaces.",
  ["(a) True", "(b) False: growing follicles secrete estrogen", "(c) True", "(d) True",
   "(e) False: Leydig cells are in the intertubular (interstitial) spaces"],
  "Testis and ovary",
  at="D", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"],
  why="(b) gives the growing follicles the corpus luteum's hormone; (e) puts the Leydig cells inside the tubules; "
      "every other option contains one of them.", secs=65)

# ================================================================ Human Reproduction (6/9/6)
Z(HR, "Male and female reproductive systems", B, D,
  "In human males, the seminal plasma together with the sperms constitutes the:",
  "Composition of semen",
  "The secretions of the male accessory glands form the seminal plasma. The seminal plasma along with the sperms "
  "constitutes the semen.",
  ["Accessory gland secretions = seminal plasma", "Seminal plasma + sperms = semen"],
  "Gametogenesis (spermatogenesis)",
  at="A", correct="Semen", wrong=["Colostrum", "Amniotic fluid", "Antrum fluid"],
  why="Colostrum is the early milk of lactation; amniotic fluid surrounds the foetus; the antrum is the fluid-filled "
      "cavity of the tertiary follicle.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "Each human testis is oval in shape, with a length of about 4 to 5 cm. Its width is about:",
  "Dimensions of the testis",
  "NCERT: each testis is oval in shape, with a length of about 4 to 5 cm and a width of about 2 to 3 cm.",
  ["Length 4-5 cm", "Width 2-3 cm"],
  "The male reproductive system",
  at="A", correct="2 to 3 cm", wrong=["10 to 12 cm", "6 to 8 cm", "0.2 to 0.3 cm"],
  why="10-12 cm is the length of an oviduct; the width cannot exceed the 4-5 cm length; 0.2-0.3 cm is far too "
      "small.", secs=25)

Z(HR, "Gametogenesis", B, D,
  "After spermiogenesis, sperm heads become embedded in the Sertoli cells and are finally released from the "
  "seminiferous tubules. This release is called:",
  "Spermiation",
  "Spermatids are transformed into spermatozoa by spermiogenesis. The sperm heads then become embedded in the "
  "Sertoli cells and are finally released from the seminiferous tubules by the process called spermiation.",
  ["Spermatid -> sperm = spermiogenesis", "Release of sperms from the tubules = spermiation"],
  "Gametogenesis",
  at="D", correct="Spermiation", wrong=["Spermiogenesis", "Insemination", "Ovulation"],
  why="Spermiogenesis is the change of spermatids into sperms, which happens before release; insemination is the "
      "release of semen into the vagina; ovulation is the release of the ovum from the ovary.", secs=25)

Z(HR, "Fertilisation and implantation", B, D,
  "The mitotic divisions (cleavage) of the human zygote as it moves towards the uterus form 2, 4, 8 and 16 "
  "daughter cells. These daughter cells are called:",
  "Cleavage",
  "Cleavage starts as the zygote moves through the isthmus of the oviduct towards the uterus and forms 2, 4, 8, 16 "
  "daughter cells called blastomeres.",
  ["Cleavage = mitotic divisions of the zygote", "Daughter cells = blastomeres"],
  "Fertilisation and implantation",
  at="B", correct="Blastomeres", wrong=["Spermatids", "Polar bodies", "Granulosa cells"],
  why="Spermatids come from meiosis in the testis; polar bodies come from the unequal meiotic divisions of the "
      "oocyte; granulosa cells surround the oocyte in the follicle.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "The shape of the human uterus is like:",
  "Shape of the uterus",
  "The uterus is single and is also called the womb. Its shape is like an inverted pear, and it is supported by "
  "ligaments attached to the pelvic wall.",
  ["Uterus = womb", "Shape: inverted pear"],
  "The female reproductive system",
  at="A", correct="An inverted pear", wrong=["A funnel with fimbriae", "A coiled tube", "A bean with a hilum"],
  why="The funnel with fimbriae is the infundibulum of the oviduct; a coiled tube describes the seminiferous "
      "tubule; the uterus has no bean-like shape.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "According to NCERT, the secretions of which of the following are essential for the maturation and motility of "
  "sperms?",
  "Role of male accessory ducts and glands",
  "Sperms released from the seminiferous tubules are transported by the accessory ducts. The secretions of the "
  "epididymis, vas deferens, seminal vesicle and prostate are essential for the maturation and motility of sperms.",
  ["Epididymis, vas deferens, seminal vesicle and prostate", "Their secretions -> maturation and motility of sperms"],
  "Gametogenesis (spermatogenesis)",
  at="C", correct="Epididymis, vas deferens, seminal vesicle and prostate",
  wrong=["Ovary, oviduct and uterus", "Leydig cells only", "Urinary bladder and ureters"],
  why="Ovary, oviduct and uterus are female organs; Leydig cells secrete androgens into the blood, not secretions "
      "for sperm maturation; the urinary bladder and ureters belong to the excretory system.", secs=30)

Z(HR, "Male and female reproductive systems", I, STP,
  SP("Each ovary is about 2 to 4 cm in length and is connected to the pelvic wall and the uterus by ligaments.",
     "The uterus is single and is also called the womb."),
  "The female reproductive system",
  "NCERT: each ovary is about 2 to 4 cm in length and is connected to the pelvic wall and uterus by ligaments. The "
  "uterus is single and is also called the womb.",
  ["Statement I: true", "Statement II: true"],
  "The female reproductive system", ans="A",
  why="Both statements are NCERT descriptions, so options calling either false are wrong.", secs=35)

Z(HR, "Gametogenesis", I, MUL,
  MS("Which of the following statements about the structure of a human sperm are correct?",
     ["A plasma membrane envelops the whole body of the sperm.",
      "The sperm head contains an elongated haploid nucleus.",
      "The sperm is made up of a head, neck, middle piece and tail.",
      "The tail of the sperm contains numerous mitochondria, which produce energy for its movement.",
      "The acrosome covers the posterior portion of the sperm head."]),
  "Structure of a sperm",
  "A sperm is a microscopic structure made of a head, neck, middle piece and tail; a plasma membrane envelops the "
  "whole body. The head contains an elongated haploid nucleus, the anterior portion of which is covered by a "
  "cap-like acrosome. The middle piece (not the tail) has numerous mitochondria that produce energy for the tail's "
  "movement.",
  ["(a) True", "(b) True", "(c) True", "(d) False: mitochondria are in the middle piece",
   "(e) False: the acrosome covers the anterior portion"],
  "Gametogenesis (spermatogenesis)",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(d) moves the mitochondria to the tail and (e) moves the acrosome to the back of the head, so every option "
      "with either is wrong.", secs=55)

Z(HR, "Menstrual cycle", I, ASR,
  AR("The endometrium of the uterus is maintained during the luteal phase of the menstrual cycle.",
     "The corpus luteum secretes large amounts of progesterone, which is essential for the maintenance of the "
     "endometrium."),
  "Luteal phase",
  "In the luteal phase the remaining parts of the Graafian follicle form the corpus luteum, which secretes large "
  "amounts of progesterone. Progesterone is essential for maintaining the endometrium, which is needed for "
  "implantation of a fertilised ovum.",
  ["A: true", "R: true", "Progesterone from the corpus luteum is the reason the endometrium is maintained"],
  "Menstrual cycle", ans="A",
  why="R gives the cause of A, so B is wrong; both statements are true, so C and D are wrong.", secs=40)

Z(HR, "Menstrual cycle", I, STP,
  SP("Cyclic menstruation is an indicator of the normal reproductive phase and extends between menarche and "
     "menopause.",
     "The secretion of the gonadotropins (LH and FSH) decreases gradually during the follicular phase."),
  "Menstrual cycle",
  "NCERT: cyclic menstruation indicates the normal reproductive phase and extends between menarche and menopause. "
  "During the follicular phase the secretion of gonadotropins increases gradually, stimulating follicular "
  "development and estrogen secretion by the growing follicles.",
  ["Statement I: true", "Statement II: false - gonadotropins increase gradually in the follicular phase"],
  "Menstrual cycle", ans="C",
  why="Statement II reverses the trend of LH and FSH, so options calling it true are wrong; Statement I is an "
      "NCERT line, so options calling it false are wrong.", secs=40)

Z(HR, "Menstrual cycle", I, MAT,
  ML(("phase of the menstrual cycle", "event"),
     ["Menstrual phase", "Follicular phase", "Ovulatory phase", "Luteal phase"],
     ["Remaining parts of the Graafian follicle transform into the corpus luteum",
      "Breakdown of the endometrial lining and its blood vessels when the ovum is not fertilised",
      "Primary follicles grow into a fully mature Graafian follicle",
      "Rupture of the Graafian follicle and release of the ovum"]),
  "Phases of the menstrual cycle",
  "The menstrual phase is the breakdown of the endometrial lining and its blood vessels (when the ovum is not "
  "fertilised). In the follicular phase, primary follicles grow into a fully mature Graafian follicle. In the "
  "ovulatory phase, the Graafian follicle ruptures and releases the ovum. In the luteal phase, the remaining parts "
  "of the Graafian follicle form the corpus luteum.",
  ["A -> II", "B -> III", "C -> IV", "D -> I"],
  "Menstrual cycle",
  at="D", match=({"A": "II", "B": "III", "C": "IV", "D": "I"},
                 [{"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="Follicle growth precedes and ovulation follows it, so swapping B and C is wrong; the corpus luteum forms "
      "after ovulation, not during menstruation.", secs=45)

Z(HR, "Pregnancy, parturition and lactation", I, D,
  "The mammary glands of a female differentiate during pregnancy. They start producing milk:",
  "Lactation",
  "NCERT: the mammary glands of the female undergo differentiation during pregnancy and start producing milk "
  "towards the end of pregnancy by the process called lactation.",
  ["Differentiation: during pregnancy", "Milk production begins: towards the end of pregnancy"],
  "Parturition and lactation",
  at="A", correct="Towards the end of pregnancy",
  wrong=["From the first month of pregnancy", "Only from puberty onwards, in every menstrual cycle",
         "Only several weeks after parturition"],
  why="Milk production does not start early in pregnancy or in non-pregnant cycles; the initial milk (colostrum) "
      "is already available in the first days after birth, so it does not begin weeks later.", secs=30)

Z(HR, "Male and female reproductive systems", I, ASR,
  AR("The functions of the male sex accessory ducts and glands are maintained by the testicular hormones "
     "(androgens).",
     "Androgens are synthesised and secreted by the Sertoli cells of the seminiferous tubules."),
  "Androgens and male accessory organs",
  "NCERT states that the functions of the male sex accessory ducts and glands are maintained by the testicular "
  "hormones (androgens). Androgens are secreted by the Leydig (interstitial) cells in the intertubular spaces; the "
  "Sertoli cells provide nutrition to the germ cells.",
  ["A: true", "R: false - androgens come from the Leydig cells"],
  "Gametogenesis (spermatogenesis); The male reproductive system", ans="C",
  why="R is false, so options A and B are wrong; A is an NCERT statement, so D is wrong.", secs=40)

Z(HR, "Male and female reproductive systems", I, D,
  "Which of the following shows the correct order of the parts of a human oviduct, starting from the end nearer "
  "the ovary?",
  "Parts of the oviduct",
  "Each oviduct extends from the periphery of the ovary to the uterus. The part closer to the ovary is the "
  "funnel-shaped infundibulum; it leads to the wider ampulla; the last part, the isthmus, has a narrow lumen and "
  "joins the uterus.",
  ["Nearest the ovary: infundibulum", "Middle, wider part: ampulla", "Last, narrow part joining the uterus: isthmus"],
  "The female reproductive system",
  at="B", correct="Infundibulum → ampulla → isthmus → uterus",
  wrong=["Isthmus → ampulla → infundibulum → uterus", "Ampulla → infundibulum → isthmus → uterus",
         "Infundibulum → isthmus → ampulla → uterus"],
  why="The isthmus is the last part joining the uterus, not the first; the infundibulum, not the ampulla, is "
      "closest to the ovary; the ampulla lies between the infundibulum and the isthmus.", secs=35)

Z(HR, "Fertilisation and implantation", I, D,
  "During fertilisation in humans, the secretions of the acrosome help the sperm to:",
  "Role of the acrosome in fertilisation",
  "The secretions of the acrosome help the sperm enter into the cytoplasm of the ovum through the zona pellucida "
  "and the plasma membrane. The block to additional sperms comes from changes in the zona pellucida membrane.",
  ["Acrosome = enzyme-filled cap on the sperm head", "Its secretions let the sperm pass the zona pellucida and "
   "plasma membrane into the ovum's cytoplasm"],
  "Fertilisation and implantation",
  at="D", correct="Enter the cytoplasm of the ovum through the zona pellucida and the plasma membrane",
  wrong=["Block the entry of additional sperms into the ovum",
         "Attach the blastocyst to the endometrium",
         "Produce energy for the movement of the tail"],
  why="Blocking extra sperms is done by changes in the zona pellucida; attachment to the endometrium is done by the "
      "trophoblast; energy for the tail comes from mitochondria in the middle piece.", secs=35)

Z(HR, "Menstrual cycle", A, MUL,
  MS("Which of the following statements about the menstrual cycle are correct?",
     ["In the absence of fertilisation, the corpus luteum degenerates, causing disintegration of the endometrium and "
      "marking a new cycle.",
      "The changes in the ovary and the uterus during the cycle are induced by changes in the levels of pituitary "
      "and ovarian hormones.",
      "Progesterone is the main hormone secreted by the growing follicles in the follicular phase.",
      "The reproductive cycle in female primates (monkeys, apes and human beings) is called the menstrual cycle.",
      "Ovulation takes place at the end of the luteal phase."]),
  "Menstrual cycle",
  "If fertilisation does not occur, the corpus luteum degenerates; the endometrium disintegrates, leading to "
  "menstruation and a new cycle. Cyclic changes in the ovary and uterus are induced by pituitary and ovarian "
  "hormones. Growing follicles secrete estrogens; progesterone comes from the corpus luteum after ovulation. The "
  "reproductive cycle of female primates is the menstrual cycle. Ovulation (ovulatory phase) is followed by the "
  "luteal phase, not placed at its end.",
  ["(a) True", "(b) True", "(c) False: growing follicles secrete estrogens", "(d) True",
   "(e) False: the luteal phase comes after ovulation"],
  "Menstrual cycle",
  at="C", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(c) assigns the corpus luteum's hormone to the growing follicles and (e) reverses the order of ovulation and "
      "the luteal phase; every other option includes one of them.", secs=65)

Z(HR, "Gametogenesis", A, ASR,
  AR("The female gamete released from the Graafian follicle at ovulation is a secondary oocyte.",
     "The primary oocyte within the tertiary follicle completes its first meiotic division before ovulation."),
  "Oogenesis and ovulation",
  "The primary oocyte within the tertiary follicle grows and completes its first meiotic division, an unequal "
  "division giving a large haploid secondary oocyte and a tiny first polar body. The Graafian follicle then "
  "ruptures and releases this secondary oocyte (ovum) by ovulation. The second meiotic division is completed only "
  "after a sperm enters.",
  ["A: true", "R: true", "Because meiosis I is completed before ovulation (and meiosis II only after sperm "
   "entry), the released cell is a secondary oocyte: R explains A"],
  "Gametogenesis (oogenesis)", ans="A",
  why="The timing of meiosis I in R is exactly why the released gamete is a secondary oocyte, so B is wrong; both "
      "statements are true, so C and D are wrong.", secs=50)

Z(HR, "Fertilisation and implantation", A, STP,
  SP("The inner cell mass differentiates into the ectoderm and the endoderm before the blastocyst reaches the "
     "uterus.",
     "The placenta facilitates the removal of carbon dioxide and excretory/waste materials produced by the embryo."),
  "Germ layers and the placenta",
  "Immediately after implantation (that is, after the blastocyst has reached and become embedded in the uterus), "
  "the inner cell mass differentiates into an outer ectoderm and an inner endoderm; a mesoderm soon appears between "
  "them. The placenta supplies oxygen and nutrients to the embryo and removes carbon dioxide and excretory/waste "
  "materials produced by it.",
  ["Statement I: false - germ layers form immediately after implantation", "Statement II: true"],
  "Fertilisation and implantation; Pregnancy and embryonic development", ans="D",
  why="Statement I places germ-layer formation before implantation, so options calling it true are wrong; "
      "Statement II is an NCERT function of the placenta, so options calling it false are wrong.", secs=50)

Z(HR, "Gametogenesis", A, MAT,
  ML(("stage of ovarian follicle", "feature"),
     ["Primary follicle", "Secondary follicle", "Tertiary follicle", "Graafian follicle"],
     ["Primary oocyte surrounded by more layers of granulosa cells and a new theca",
      "Mature follicle in which the secondary oocyte forms a new membrane, the zona pellucida",
      "Primary oocyte surrounded by a layer of granulosa cells",
      "Fluid-filled antrum; the theca is organised into an inner theca interna and an outer theca externa"]),
  "Follicle development in oogenesis",
  "A primary oocyte surrounded by a layer of granulosa cells is a primary follicle. With more layers of granulosa "
  "cells and a new theca it becomes a secondary follicle. The tertiary follicle has a fluid-filled antrum and its "
  "theca is organised into theca interna and theca externa. The Graafian (mature) follicle holds the secondary "
  "oocyte, which forms a new membrane, the zona pellucida.",
  ["A -> III", "B -> I", "C -> IV", "D -> II"],
  "Gametogenesis (oogenesis)",
  at="B", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"}]),
  why="A single granulosa layer marks the primary follicle and extra layers the secondary one; the antrum and "
      "split theca mark the tertiary follicle, while the zona pellucida forms around the secondary oocyte in the "
      "Graafian follicle.", secs=60)

Z(HR, "Male and female reproductive systems", A, MUL,
  MS("Which of the following statements about the human male reproductive system are correct?",
     ["The urethra originates from the urinary bladder and extends through the penis to its external opening, the "
      "urethral meatus.",
      "The penis is made up of special tissue that helps in its erection to facilitate insemination.",
      "The testes lie inside the abdominal cavity, whose temperature is suitable for spermatogenesis.",
      "Each seminiferous tubule opens directly into the vas deferens.",
      "The male reproductive system is located in the pelvis region."]),
  "The male reproductive system",
  "The male reproductive system is located in the pelvis region. The urethra arises from the urinary bladder and "
  "runs through the penis to the urethral meatus. The penis has special tissue that helps in erection to facilitate "
  "insemination. The testes lie outside the abdominal cavity in the scrotum, which keeps them cooler than the body "
  "for spermatogenesis. Seminiferous tubules open into the vasa efferentia through the rete testis, then the "
  "epididymis, and only then the vas deferens.",
  ["(a) True", "(b) True", "(c) False: testes are in the scrotum, outside the abdomen",
   "(d) False: the route is rete testis -> vasa efferentia -> epididymis -> vas deferens", "(e) True"],
  "The male reproductive system",
  at="D", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="(c) places the testes in the abdomen and (d) skips the rete testis, vasa efferentia and epididymis; every "
      "other option contains one of them.", secs=65)

Z(HR, "Gametogenesis", A, D,
  "Which of the following lists ONLY haploid cells formed during spermatogenesis in a human male?",
  "Ploidy of cells in spermatogenesis",
  "Spermatogonia (2n = 46) differentiate into primary spermatocytes, which are also diploid. The first meiotic "
  "division gives haploid secondary spermatocytes with 23 chromosomes each; their second meiotic division gives "
  "haploid spermatids, which become haploid spermatozoa.",
  ["Diploid: spermatogonia, primary spermatocytes", "Meiosis I halves the number",
   "Haploid: secondary spermatocytes, spermatids, spermatozoa"],
  "Gametogenesis (spermatogenesis)",
  at="C", correct="Secondary spermatocytes, spermatids and spermatozoa",
  wrong=["Spermatogonia, primary spermatocytes and spermatids",
         "Primary spermatocytes, secondary spermatocytes and spermatozoa",
         "Spermatogonia, secondary spermatocytes and spermatids"],
  why="Each wrong list includes a diploid cell (spermatogonium or primary spermatocyte), which is formed before "
      "the reduction division of meiosis I.", secs=45)

# ================================================================ Reproductive Health (4/6/4)
Z(RH, "STDs and their prevention", B, D,
  "Sexually transmitted infections (STIs) are also called:",
  "Names for STIs",
  "Diseases or infections transmitted through sexual intercourse are collectively called sexually transmitted "
  "infections (STIs), venereal diseases (VD) or reproductive tract infections (RTI).",
  ["STI = VD = RTI"],
  "Sexually transmitted infections (STIs)",
  at="A", correct="Venereal diseases (VD) or reproductive tract infections (RTI)",
  wrong=["Auto-immune diseases", "Congenital disorders", "Deficiency diseases"],
  why="Auto-immune diseases are attacks on self cells; congenital disorders are present from birth; deficiency "
      "diseases come from lack of nutrients; none of these is another name for STIs.", secs=20)

Z(RH, "Contraception", B, D,
  "Which of the following is a hormone-releasing intra-uterine device (IUD)?",
  "Types of IUDs",
  "IUDs are of three kinds: non-medicated (e.g. Lippes loop), copper-releasing (CuT, Cu7, Multiload 375) and "
  "hormone-releasing (Progestasert, LNG-20).",
  ["Non-medicated: Lippes loop", "Copper-releasing: CuT, Cu7, Multiload 375", "Hormone-releasing: Progestasert, "
   "LNG-20"],
  "Birth control (contraceptive methods)",
  at="B", correct="Progestasert", wrong=["CuT", "Cu7", "Lippes loop"],
  why="CuT and Cu7 release copper ions; the Lippes loop is non-medicated.", secs=20)

Z(RH, "Contraception", B, D,
  "Barrier methods of contraception prevent conception by:",
  "Barrier methods",
  "In barrier methods, the ovum and sperms are prevented from physically meeting with the help of barriers such as "
  "condoms, diaphragms, cervical caps and vaults.",
  ["Barrier = physical block", "Ovum and sperm cannot meet"],
  "Birth control (contraceptive methods)",
  at="A", correct="Preventing the ovum and sperms from physically meeting",
  wrong=["Inhibiting ovulation through daily hormone tablets", "Cutting and tying the vas deferens",
         "Releasing copper ions that make the uterus hostile to the embryo"],
  why="Hormone tablets are oral pills; cutting the vas deferens is vasectomy, a surgical method; copper ions are "
      "released by copper IUDs.", secs=25)

Z(RH, "MTP and amniocentesis", B, D,
  "Medical termination of pregnancy (MTP), also called induced abortion, is defined as:",
  "Definition of MTP",
  "Intentional or voluntary termination of pregnancy before full term is called medical termination of pregnancy "
  "(MTP) or induced abortion.",
  ["Intentional or voluntary", "Before full term"],
  "Medical termination of pregnancy (MTP)",
  at="D", correct="Intentional or voluntary termination of pregnancy before full term",
  wrong=["Natural, unplanned loss of a pregnancy after full term",
         "Removal of the fallopian tubes to prevent future pregnancies",
         "Transfer of an embryo into the uterus of another woman"],
  why="MTP is intentional, not natural, and occurs before full term; removing or tying the tubes is tubectomy; "
      "embryo transfer is an assisted reproductive technique.", secs=25)

Z(RH, "Contraception", I, STP,
  SP("Condoms are disposable, can be self-inserted and thereby give privacy to the user.",
     "Condoms for females are used to cover the vagina and cervix just before coitus."),
  "Condoms",
  "Condoms are barriers made of thin rubber/latex sheath used to cover the penis in males or the vagina and cervix "
  "in females, just before coitus, so that the ejaculated semen does not enter the female reproductive tract. They "
  "are disposable, can be self-inserted and thereby give privacy to the user.",
  ["Statement I: true", "Statement II: true"],
  "Birth control (contraceptive methods)", ans="A",
  why="Both statements are NCERT descriptions of condoms, so options calling either false are wrong.", secs=35)

Z(RH, "STDs and their prevention", I, MUL,
  MS("Which of the following statements about the spread and prevention of STIs are correct?",
     ["Hepatitis-B and HIV can be transmitted by sharing injection needles or surgical instruments with infected "
      "persons.",
      "Hepatitis-B and HIV can also be transmitted by transfusion of blood.",
      "Always using condoms during coitus is one of the simple principles for preventing STIs.",
      "In case of doubt, one should go to a qualified doctor for early detection and get complete treatment.",
      "All STIs are transmitted only through sexual contact."]),
  "Transmission and prevention of STIs",
  "Some STIs like hepatitis-B and HIV can also be transmitted by sharing injection needles and surgical instruments "
  "with infected persons, by transfusion of blood, or from an infected mother to the foetus. NCERT's simple "
  "principles for prevention include always using condoms during coitus and consulting a qualified doctor in case "
  "of doubt for early detection and complete treatment.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: some spread by needles, blood or mother to foetus"],
  "Sexually transmitted infections (STIs)",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="(e) is false because hepatitis-B and HIV also spread by non-sexual routes, so options with (e) are wrong.",
  secs=50)

Z(RH, "Contraception", I, ASR,
  AR("Contraceptives are not regular requirements for the maintenance of reproductive health.",
     "Contraceptives are essential for keeping the reproductive organs healthy and must be used throughout the "
     "reproductive life."),
  "Nature of contraceptives",
  "NCERT reminds us that contraceptives are not regular requirements for the maintenance of reproductive health; in "
  "fact, they are practised against a natural reproductive event, i.e. conception/pregnancy. They are used only to "
  "prevent or space pregnancies, not to keep the organs healthy.",
  ["A: true (NCERT)", "R: false - contraceptives are not needed for the health of the organs"],
  "Birth control (contraceptive methods)", ans="C",
  why="R contradicts NCERT, so options A and B are wrong; A is an NCERT statement, so D is wrong.", secs=40)

Z(RH, "Infertility and ART", I, D,
  "According to NCERT, which of the following is, as yet, one of the best methods for couples looking for "
  "parenthood, since our laws permit it?",
  "Adoption",
  "NCERT notes that ART needs very high precision handling and expensive instrumentation, and emotional, religious "
  "and social factors are deterrents. Since the ultimate aim is to have children, it states that our laws permit "
  "legal adoption and that it is, as yet, one of the best methods for couples looking for parenthood.",
  ["Laws permit legal adoption", "NCERT: one of the best methods for couples looking for parenthood"],
  "Infertility",
  at="C", correct="Legal adoption",
  wrong=["Medical termination of pregnancy", "Tubectomy", "Amniocentesis"],
  why="MTP ends a pregnancy; tubectomy is a permanent contraceptive method; amniocentesis is a prenatal test; none "
      "of them gives a couple a child.", secs=25)

Z(RH, "MTP and amniocentesis", I, STP,
  SP("MTPs are used to get rid of unwanted pregnancies due to casual unprotected intercourse, failure of the "
     "contraceptive used during coitus, or rapes.",
     "The MTPs performed in a year all over the world account for about one-half of the total number of conceived "
     "pregnancies in a year."),
  "Uses and extent of MTP",
  "NCERT: MTPs are used to get rid of unwanted pregnancies due to casual unprotected intercourse, contraceptive "
  "failure or rapes. Nearly 45 to 50 million MTPs are performed in a year all over the world, which accounts for "
  "about one-fifth (not one-half) of the total number of conceived pregnancies in a year.",
  ["Statement I: true", "Statement II: false - about 1/5th, not 1/2"],
  "Medical termination of pregnancy (MTP)", ans="C",
  why="Statement II doubles NCERT's figure and more, so options calling it true are wrong; Statement I is an NCERT "
      "line, so options calling it false are wrong.", secs=40)

Z(RH, "Infertility and ART", I, D,
  "A couple is childless because the male partner is unable to inseminate the female and his ejaculates have very "
  "low sperm counts. According to NCERT, the technique that can correct such cases is:",
  "Artificial insemination",
  "Infertility due to the inability of the male partner to inseminate the female, or due to very low sperm counts "
  "in the ejaculates, can be corrected by artificial insemination (AI). The semen from the husband or a healthy "
  "donor is artificially introduced into the vagina or into the uterus (IUI).",
  ["Problem: cannot inseminate / very low sperm count", "NCERT remedy: artificial insemination (AI)"],
  "Infertility",
  at="D", correct="Artificial insemination (AI)",
  wrong=["Gamete intra fallopian transfer (GIFT) of a donor ovum", "Tubectomy",
         "Intra uterine transfer (IUT) of an embryo with more than 8 blastomeres"],
  why="GIFT is meant for a female who cannot produce ova; tubectomy prevents pregnancy; IUT transfers an embryo and "
      "is not the technique NCERT gives for a male who cannot inseminate.", secs=40)

Z(RH, "MTP and amniocentesis", A, MUL,
  MS("According to the MTP (Amendment) Act, 2017, as described in NCERT, which of the following are correct?",
     ["A pregnancy may be terminated on certain considered grounds within the first 12 weeks on the opinion of one "
      "registered medical practitioner.",
      "If the pregnancy has lasted more than 12 weeks but fewer than 24 weeks, two registered medical practitioners "
      "must be of the opinion that termination is justified.",
      "One accepted ground is that continuing the pregnancy would involve a risk to the life of the pregnant woman "
      "or grave injury to her physical or mental health.",
      "Another accepted ground is a substantial risk that the child, if born, would suffer from serious physical or "
      "mental abnormalities.",
      "The Act allows termination at any stage of pregnancy, on request, without any conditions."]),
  "MTP (Amendment) Act, 2017",
  "NCERT: the Government of India enacted the MTP (Amendment) Act, 2017 to reduce illegal abortion and maternal "
  "mortality. A pregnancy may be terminated on considered grounds within the first 12 weeks on the opinion of one "
  "registered medical practitioner; between 12 and 24 weeks the opinion of two registered medical practitioners is "
  "needed. The grounds are a risk to the life or grave injury to the physical or mental health of the pregnant "
  "woman, or a substantial risk of serious physical or mental abnormality in the child. MTP has strict conditions "
  "to avoid misuse, so termination on request at any stage is wrong.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: strict conditions and time limits apply"],
  "Medical termination of pregnancy (MTP)",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (c) and (e) only", "(b), (d) and (e) only", "(a) and (b) only"],
  why="(e) ignores the Act's conditions, so options with (e) are wrong; '(a) and (b) only' leaves out the two "
      "grounds that NCERT lists.", secs=70)

Z(RH, "Contraception", A, ASR,
  AR("Motivating smaller families by using various contraceptive methods is an important step to overcome the "
     "problem of population explosion.",
     "Possible ill-effects of contraceptives include nausea, abdominal pain, breakthrough bleeding, irregular "
     "menstrual bleeding or even breast cancer."),
  "Contraception and population control",
  "NCERT gives motivating smaller families through contraceptive methods as the most important step against "
  "population explosion. Separately, it lists possible ill-effects of contraceptives (nausea, abdominal pain, "
  "breakthrough bleeding, irregular menstrual bleeding or even breast cancer), which, though not very significant, "
  "should not be totally ignored. The ill-effects are a different property of contraceptives and do not explain "
  "why they help control population.",
  ["A: true", "R: true", "R describes side effects; it gives no reason why contraception checks population growth"],
  "Population stabilisation and birth control", ans="B",
  why="R is about side effects, which in no way explain the role of contraception in population control, so A is "
      "wrong; both statements are true, so C and D are wrong.", secs=50)

Z(RH, "Contraception", A, STP,
  SP("Natural methods of contraception work on the principle of avoiding the chances of the ovum and sperms "
     "meeting.",
     "Progestogen injections and implants act in a way quite different from oral pills and have much shorter "
     "effective periods."),
  "Natural methods; injectables and implants",
  "NCERT: natural methods work on the principle of avoiding chances of ovum and sperms meeting. Progestogens alone "
  "or with estrogen can also be used as injections or implants under the skin; their mode of action is similar to "
  "that of pills and their effective periods are much longer.",
  ["Statement I: true", "Statement II: false - similar mode of action, much longer effective periods"],
  "Birth control (contraceptive methods)", ans="C",
  why="Statement II reverses both NCERT points (similar action, longer periods), so options calling it true are "
      "wrong; Statement I is an NCERT line, so options calling it false are wrong.", secs=50)

Z(RH, "Infertility and ART", A, D,
  "In which of the following assisted reproductive techniques does fertilisation take place inside the body of the "
  "female (in vivo)?",
  "Where fertilisation occurs in different ARTs",
  "In GIFT, an ovum collected from a donor is transferred into the fallopian tube of a female who cannot produce "
  "ova but can provide a suitable environment for fertilisation and further development; fertilisation therefore "
  "takes place in her body. In IVF-ET (including ZIFT) and in ICSI, the zygote is formed in the laboratory and only "
  "the zygote or embryo is transferred.",
  ["GIFT transfers a gamete, so fertilisation happens in the fallopian tube", "ZIFT, IVF-ET: zygote formed in vitro",
   "ICSI: sperm injected into the ovum in the laboratory"],
  "Infertility",
  at="D", correct="Gamete intra fallopian transfer (GIFT)",
  wrong=["Zygote intra fallopian transfer (ZIFT)", "Intra cytoplasmic sperm injection (ICSI)",
         "In vitro fertilisation followed by embryo transfer (IVF-ET)"],
  why="ZIFT and IVF-ET transfer a zygote or embryo already formed outside the body, and in ICSI the sperm is "
      "injected into the ovum in the laboratory, so fertilisation is in vitro in all three.", secs=50)

# ================================================================ Evolution (5/7/5)
Z(EVO, "Origin of life", B, D,
  "The theory that explains the origin of the universe as a singular huge explosion, unimaginable in physical "
  "terms, is the:",
  "Origin of the universe",
  "The Big Bang theory attempts to explain the origin of the universe. It talks of a singular huge explosion "
  "unimaginable in physical terms; the universe expanded and the temperature came down.",
  ["Single huge explosion -> Big Bang theory"],
  "Origin of life",
  at="A", correct="Big Bang theory",
  wrong=["Theory of panspermia", "Theory of special creation", "Theory of spontaneous generation"],
  why="Panspermia is about spores of life coming from outer space; special creation says organisms were created as "
      "such; spontaneous generation says life arises from decaying matter. None explains the universe's origin.",
  secs=20)

Z(EVO, "Origin of life", B, D,
  "According to the theory of special creation, the earth is about:",
  "Theory of special creation",
  "The theory of special creation has three connotations: all living organisms were created as such; the diversity "
  "was always the same since creation and will remain so; and the earth is about 4000 years old. Studies in the "
  "nineteenth century challenged these ideas.",
  ["Third connotation of special creation: earth about 4000 years old"],
  "Theory of evolution (special creation)",
  at="B", correct="4000 years old",
  wrong=["4.5 billion years old", "20 billion years old", "65 million years old"],
  why="4.5 billion years is the scientific age of the earth; 20 billion years is not an age NCERT gives for the "
      "earth under any theory; 65 million years ago the dinosaurs disappeared.", secs=25)

Z(EVO, "Darwinism and modern synthesis", B, D,
  "The two key concepts of Darwin's theory of evolution are:",
  "Darwinian theory",
  "NCERT: the two key concepts of the Darwinian theory of evolution are branching descent and natural selection.",
  ["Branching descent", "Natural selection"],
  "Mechanism of evolution / Theory of evolution",
  at="A", correct="Branching descent and natural selection",
  wrong=["Use and disuse of organs, and inheritance of acquired characters",
         "Saltation and mutation pressure",
         "Spontaneous generation and special creation"],
  why="Use and disuse is Lamarck's idea; saltation and single-step mutation are de Vries' ideas; spontaneous "
      "generation and special creation are pre-evolutionary ideas.", secs=25)

Z(EVO, "Human evolution", B, D,
  "Pre-historic cave paintings, made about 18,000 years ago, can be seen at the Bhimbetka rock shelter located in:",
  "Pre-historic cave art in India",
  "NCERT: pre-historic cave art developed about 18,000 years ago. One such set of cave paintings by pre-historic "
  "humans can be seen at the Bhimbetka rock shelter in Raisen district of Madhya Pradesh.",
  ["Cave art about 18,000 years ago", "Bhimbetka rock shelter: Raisen district, Madhya Pradesh"],
  "Origin and evolution of man",
  at="B", correct="Raisen district of Madhya Pradesh",
  wrong=["The Malay Archipelago", "The Galapagos Islands", "Java, where Homo erectus fossils were found"],
  why="The Malay Archipelago is where Wallace worked; the Galapagos are where Darwin saw finches; Java is the site "
      "of the 1891 Homo erectus fossils, not of Bhimbetka.", secs=25)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "In a population, the genotype frequencies for a gene with two alleles, A and a, are AA = 0.45, Aa = 0.30 and "
  "aa = 0.25. What is the frequency of allele a in this population?",
  "Allele frequency from genotype frequencies",
  "Each aa individual carries two copies of allele a and each Aa individual carries one of its two alleles as a, so "
  "the frequency of a is the frequency of aa plus half the frequency of Aa. This counting does not need the "
  "population to be in Hardy-Weinberg equilibrium.",
  ["q = f(aa) + ½ f(Aa)", "q = 0.25 + ½ × 0.30 = 0.25 + 0.15 = 0.40",
   "Check: p = 0.45 + 0.15 = 0.60, and p + q = 1"],
  "Hardy-Weinberg principle",
  at="C", correct="0.40", wrong=["0.25", "0.55", "0.50"],
  why="0.25 counts only the aa individuals and ignores the a alleles in Aa; 0.55 adds the whole Aa frequency "
      "instead of half of it; 0.50 takes the square root of f(aa), which is valid only if the population is in "
      "Hardy-Weinberg equilibrium, and it is not (with p = 0.60 and q = 0.40, equilibrium would give aa = 0.16, not "
      "0.25).",
  secs=40, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", I, STP,
  SP("Karl Ernst von Baer supported Haeckel's proposal by noting that embryos pass through the adult stages of "
     "other animals.",
     "Haeckel's embryological support for evolution was based on functional gill slits that he observed in adult "
     "humans."),
  "Embryological evidence and its rejection",
  "Ernst Haeckel proposed embryological support for evolution: features common to all vertebrate embryos but absent "
  "in adults, e.g. a row of vestigial gill slits behind the head in all vertebrate embryos including humans, which "
  "is functional only in fish. Karl Ernst von Baer disapproved this proposal, noting that embryos never pass "
  "through the adult stages of other animals.",
  ["Statement I: false - von Baer disapproved it; embryos never pass through adult stages of others",
   "Statement II: false - vestigial gill slits are in embryos and absent in adult humans"],
  "Evidences for evolution", ans="B",
  why="Statement I reverses von Baer's finding and Statement II moves the gill slits from embryos to adults, so any "
      "option calling either true is wrong.", secs=45)

Z(EVO, "Adaptive radiation", I, MAT,
  ML(("placental mammal", "Australian marsupial that it resembles"),
     ["Anteater", "Lemur", "Flying squirrel", "Bobcat"],
     ["Flying phalanger", "Tasmanian tiger cat", "Numbat", "Spotted cuscus"]),
  "Convergent evolution of placental mammals and marsupials",
  "Placental mammals in Australia also show adaptive radiation, each variety appearing similar to a corresponding "
  "marsupial. NCERT's figure pairs the anteater with the numbat, the lemur with the spotted cuscus, the flying "
  "squirrel with the flying phalanger and the bobcat with the Tasmanian tiger cat.",
  ["A Anteater -> III Numbat", "B Lemur -> IV Spotted cuscus", "C Flying squirrel -> I Flying phalanger",
   "D Bobcat -> II Tasmanian tiger cat"],
  "Adaptive radiation (Figure: convergent evolution of Australian marsupials and placental mammals)",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The flying squirrel's gliding counterpart is the flying phalanger, the cat-like bobcat matches the Tasmanian "
      "tiger cat, and the ant-eating numbat matches the anteater; the other codes break one of these pairs.",
  secs=45)

Z(EVO, "Natural selection", I, ASR,
  AR("A new variant population can appear in a bacterial colony within days, whereas a comparable change would take "
     "millions of years in fish or fowl.",
     "The rate of appearance of new forms is linked to the life cycle or life span, and microbes that divide fast "
     "can multiply into millions of individuals within hours."),
  "Rate of evolution and life span",
  "NCERT: a bacterial colony has built-in variation; a change in the medium lets only the surviving variant grow, "
  "and it outgrows the others within days. The same would take millions of years in fish or fowl because their life "
  "spans are in years. The rate of appearance of new forms is linked to life cycle or life span.",
  ["A: true", "R: true", "Short life cycle and fast division of microbes is why change appears quickly: R explains A"],
  "Mechanism of evolution", ans="A",
  why="R gives the very reason for A (life span decides the rate), so B is wrong; both are true, so C and D are "
      "wrong.", secs=45)

Z(EVO, "Natural selection", I, D,
  "According to NCERT, evolution is a stochastic process based on:",
  "Nature of evolution",
  "NCERT: evolution is a stochastic process based on chance events in nature and chance mutation in the organisms.",
  ["Stochastic = based on chance", "Chance events in nature + chance mutation in organisms"],
  "Evolution by natural selection (A brief account of evolution)",
  at="B", correct="Chance events in nature and chance mutation in the organisms",
  wrong=["Use and disuse of organs during an individual's lifetime",
         "Changes that organisms make deliberately to meet their needs",
         "A fixed plan in which every species was created as such"],
  why="Use and disuse is Lamarck's explanation; organisms do not change deliberately to meet needs; creation of "
      "species as such is the theory of special creation.", secs=30)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, MUL,
  MS("Which of the following statements about the Hardy-Weinberg principle are correct?",
     ["p² + 2pq + q² = 1 is a binomial expansion of (p + q)².",
      "When allele frequencies are stable, the gene pool (total genes and their alleles in a population) remains a "
      "constant; this is called genetic equilibrium.",
      "When the frequency measured differs from the expected values, the difference (direction) indicates the extent "
      "of evolutionary change.",
      "Natural selection does not change the allele frequencies of a population.",
      "Hardy-Weinberg equilibrium is maintained even when gene migration occurs repeatedly."]),
  "Hardy-Weinberg principle",
  "NCERT: allele frequencies in a population are stable and constant from generation to generation; the gene pool "
  "remains a constant (genetic equilibrium). p² + 2pq + q² = 1 is the binomial expansion of (p + q)². A difference "
  "between measured and expected frequencies indicates the extent of evolutionary change. Gene migration (gene "
  "flow), genetic drift, mutation, recombination and natural selection all disturb the equilibrium.",
  ["(a) True", "(b) True", "(c) True", "(d) False: natural selection changes allele frequencies",
   "(e) False: gene flow disturbs the equilibrium"],
  "Hardy-Weinberg principle",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="Natural selection and gene flow are two of the five factors that disturb Hardy-Weinberg equilibrium, so any "
      "option with (d) or (e) is wrong.", secs=55)

Z(EVO, "Evidences of evolution", I, STP,
  SP("All fossils found in the earth's crust are of organisms that are still living today.",
     "A study of fossils in different sedimentary layers indicates the geological period in which they existed."),
  "Paleontological evidence",
  "Fossils are remains of hard parts of life-forms found in rocks; many represent extinct organisms, e.g. "
  "dinosaurs. A study of fossils in different sedimentary layers indicates the geological period in which they "
  "existed, showing that life-forms varied over time.",
  ["Statement I: false - many fossils are of extinct organisms (e.g. dinosaurs)", "Statement II: true"],
  "Evidences for evolution", ans="D",
  why="Statement I ignores extinct forms such as dinosaurs, so options calling it true are wrong; Statement II is an "
      "NCERT line, so options calling it false are wrong.", secs=35)

Z(EVO, "Human evolution", I, D,
  "Homo erectus, whose fossils were discovered in Java in 1891, existed about:",
  "Homo erectus",
  "NCERT: fossils discovered in Java in 1891 revealed the next stage after Homo habilis, i.e. Homo erectus, about "
  "1.5 mya. Homo erectus had a large brain of around 900 cc and probably ate meat.",
  ["Java fossils (1891) -> Homo erectus", "Time: about 1.5 million years ago"],
  "Origin and evolution of man",
  at="C", correct="1.5 million years ago",
  wrong=["15 million years ago", "18,000 years ago", "10,000 years ago"],
  why="15 mya is the time of Dryopithecus and Ramapithecus; 18,000 years ago is when pre-historic cave art "
      "developed; agriculture came about 10,000 years ago.", secs=30)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "A rare autosomal recessive disorder affects 1 in every 10,000 individuals of a population that is in "
  "Hardy-Weinberg equilibrium. Approximately what proportion of the population are heterozygous carriers?",
  "Carrier frequency of a rare recessive allele",
  "Affected individuals are aa, so q² = 1/10,000 and q = 0.01; p = 0.99. Carriers are heterozygotes, 2pq = 2 × 0.99 "
  "× 0.01 = 0.0198, i.e. about 2%, or about 1 in 50.",
  ["q² = 1/10,000 -> q = 1/100 = 0.01", "p = 1 - q = 0.99", "2pq = 2 × 0.99 × 0.01 = 0.0198 ≈ 1 in 50"],
  "Hardy-Weinberg principle",
  at="B", correct="About 1 in 50 (about 2%)",
  wrong=["About 1 in 100 (1%)", "About 1 in 10,000 (0.01%)", "About 1 in 5,000 (0.02%)"],
  short="For a rare allele p ≈ 1, so carriers ≈ 2q = 2 × 0.01 = 0.02.",
  why="1 in 100 is q, the allele frequency, not the carrier frequency; 1 in 10,000 is q², the affected frequency; "
      "1 in 5,000 is 2q², which wrongly doubles the affected frequency.", secs=75, vb=RECOMPUTED)

Z(EVO, "Origin of life", A, MUL,
  MS("Which of the following statements about the history of life on earth are correct?",
     ["Invertebrates were formed and active before the jawless fish evolved.",
      "Amphibians evolved before the reptiles.",
      "Reptiles evolved before the mammals.",
      "Pouched mammals of Australia survived because of lack of competition from any other mammals.",
      "When South America joined North America, the pouched mammals of South America overrode the North American "
      "fauna."]),
  "A brief account of evolution",
  "NCERT's account runs: invertebrates, then jawless fish, then lobe-finned fish giving rise to amphibians, then "
  "reptiles, and later mammals. Pouched mammals of Australia "
  "survived because of lack of competition from other mammals; when South America joined North America, the "
  "South American pouched mammals were overridden by the North American fauna, not the other way round.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: the pouched mammals were overridden"],
  "A brief account of evolution",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"],
  why="(e) reverses NCERT's account of South American pouched mammals, so options with (e) are wrong.", secs=65)

Z(EVO, "Evidences of evolution", A, ASR,
  AR("The flippers of penguins and of dolphins are analogous structures.",
     "Analogous structures are a result of convergent evolution, in which different structures evolve for the same "
     "function and hence show similarity."),
  "Analogy and convergent evolution",
  "Penguins (birds) and dolphins (mammals) have flippers of different origin that perform the same function "
  "(swimming). NCERT defines analogous structures as a result of convergent evolution, different structures "
  "evolving for the same function and hence having similarity, and names the flippers of penguins and dolphins as "
  "an example.",
  ["A: true (NCERT example)", "R: true (NCERT definition)",
   "The flippers are different structures with the same function, which is exactly what R describes: R explains A"],
  "Evidences for evolution", ans="A",
  why="R states the very reason why the flippers count as analogous, so B is wrong; both statements are true, so C "
      "and D are wrong.", secs=45)

Z(EVO, "Adaptive radiation", A, STP,
  SP("In Australia, adaptive radiation has been observed only among the marsupials.",
     "The similarity between the placental wolf and the Tasmanian wolf (a marsupial) is an example of convergent "
     "evolution."),
  "Adaptive radiation and convergent evolution in Australia",
  "Besides the Australian marsupials, placental mammals in Australia also exhibit adaptive radiation, evolving into "
  "varieties each of which appears similar to a corresponding marsupial (e.g. placental wolf and Tasmanian wolf). "
  "When adaptive radiations in an isolated area lead to such similarities, it is convergent evolution.",
  ["Statement I: false - placental mammals in Australia also show adaptive radiation", "Statement II: true"],
  "Adaptive radiation", ans="D",
  why="The word 'only' makes Statement I false, so options calling it true are wrong; Statement II is NCERT's "
      "example, so options calling it false are wrong.", secs=45)

Z(EVO, "Darwinism and modern synthesis", A, MUL,
  MS("Which of the following statements about Darwin's theory are correct?",
     ["Darwin's conclusions were based on observations made during a sea voyage round the world in the sailing ship "
      "H.M.S. Beagle.",
      "Natural selection is a process in which heritable variations enabling better survival are enabled to "
      "reproduce and leave a greater number of progeny.",
      "Darwin regarded large, single-step mutations as the main cause of evolution.",
      "Darwin concluded that existing living forms share similarities to varying degrees not only among themselves "
      "but also with life forms that existed millions of years ago.",
      "According to Darwin, the fitness of an individual refers to its physical strength."]),
  "Darwin's theory of evolution",
  "Darwin made a sea voyage round the world in H.M.S. Beagle and concluded that existing living forms share "
  "similarities among themselves and with life forms of millions of years ago. Natural selection lets heritable "
  "variations that enable better survival reproduce and leave more progeny. Single-step large mutation (saltation) "
  "was de Vries' idea, and Darwinian fitness refers ultimately only to reproductive fitness.",
  ["(a) True", "(b) True", "(c) False: that is de Vries' saltation", "(d) True",
   "(e) False: fitness means reproductive fitness"],
  "Theory of evolution; Mechanism of evolution",
  at="B", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(c) attributes de Vries' idea to Darwin and (e) misdefines fitness, so every option containing either is "
      "wrong.", secs=65)

# ================================================================ Human Health and Disease (6/8/6)
Z(HHD, "Immunity and vaccines", B, D,
  "The cell-mediated immune response (cell-mediated immunity, CMI) is mediated by:",
  "Types of acquired immune response",
  "Acquired immunity has two types of response. The antibody-mediated (humoral) response is due to antibodies made "
  "by B-lymphocytes; the cell-mediated immune response (CMI) is mediated by T-lymphocytes.",
  ["Antibody-mediated (humoral): B-lymphocytes", "Cell-mediated (CMI): T-lymphocytes"],
  "Immunity (acquired immunity)",
  at="C", correct="T-lymphocytes",
  wrong=["Antibodies dissolved in the plasma", "Mast cells releasing histamine", "Interferons alone"],
  why="Antibodies in the plasma give the humoral response; mast cells and histamine are part of allergic reactions; "
      "interferons are a cytokine barrier of innate immunity.", secs=20)

Z(HHD, "Cancer", B, D,
  "In radiation therapy for cancer:",
  "Treatment of cancer",
  "In radiation therapy, tumour cells are irradiated lethally, taking proper care of the normal tissues surrounding "
  "the tumour mass.",
  ["Radiotherapy: lethal irradiation of tumour cells", "Care is taken to protect surrounding normal tissue"],
  "Cancer (treatment)",
  at="B", correct="Tumour cells are irradiated lethally, taking proper care of the surrounding normal tissues",
  wrong=["Chemicals are injected to kill only the cancerous cells",
         "α-interferon is given to activate the patient's immune system",
         "The tumour is removed surgically along with the surrounding tissue"],
  why="Injected chemicals are chemotherapy; α-interferon is an immunotherapy (biological response modifier); "
      "surgical removal is surgery, not radiation therapy.", secs=25)

Z(HHD, "HIV and AIDS", B, D,
  "In an HIV-infected person, macrophages continue to produce virus particles. Because of this, NCERT says that "
  "macrophages act like a:",
  "Role of macrophages in HIV infection",
  "After HIV enters the body it moves into macrophages, where its RNA is copied into DNA by reverse transcriptase "
  "and incorporated into the host DNA. The infected macrophages continue to produce virus and in this way act like "
  "an HIV factory.",
  ["Macrophages keep producing virus", "So they act like an 'HIV factory'"],
  "AIDS",
  at="A", correct="HIV factory",
  wrong=["Lymphoid organ", "Natural killer cell", "Memory cell"],
  why="Macrophages are not lymphoid organs; natural killer cells and memory cells are other immune cells and are "
      "not what NCERT calls the virus-producing reservoir.", secs=25)

Z(HHD, "Pathogens and diseases", B, D,
  "Health is defined as:",
  "Definition of health",
  "Health does not simply mean absence of disease or physical fitness. It is defined as a state of complete "
  "physical, mental and social well-being.",
  ["Health = complete physical, mental and social well-being"],
  "Human health and disease (introduction)",
  at="A", correct="A state of complete physical, mental and social well-being",
  wrong=["Simply the absence of disease", "Only physical fitness",
         "A balance of four body humors, as Hippocrates proposed"],
  why="NCERT says health is not simply the absence of disease or physical fitness; the 'good humor' hypothesis was "
      "disproved.", secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "B-lymphocytes produce antibodies that are found in the blood. Because of this, the antibody-mediated response "
  "is also called the:",
  "Humoral immune response",
  "B-lymphocytes produce an army of proteins (antibodies) in response to pathogens. Because these antibodies are "
  "found in the blood, the response is also called the humoral immune response.",
  ["Antibodies are in the blood (body fluid)", "Hence: humoral immune response"],
  "Immunity (acquired immunity)",
  at="B", correct="Humoral immune response",
  wrong=["Cell-mediated immune response", "Innate immune response", "Auto-immune response"],
  why="The cell-mediated response is mediated by T-lymphocytes; innate immunity is non-specific and present at "
      "birth; an auto-immune response is an attack on self cells.", secs=20)

Z(HHD, "Drug and alcohol abuse", B, D,
  "The drugs commonly abused, namely opioids, cannabinoids and coca alkaloids, are mostly obtained from:",
  "Sources of commonly abused drugs",
  "NCERT: the drugs commonly abused are opioids, cannabinoids and coca alkaloids. The majority of these are obtained "
  "from flowering plants; some are obtained from fungi.",
  ["Majority: flowering plants", "Some: fungi"],
  "Drugs and alcohol abuse",
  at="D", correct="Flowering plants (some are obtained from fungi)",
  wrong=["Animal tissues", "Bacteria grown in bioreactors", "Marine algae only"],
  why="NCERT names flowering plants and fungi as sources; animal tissues, bacteria and marine algae are not the "
      "sources of these drugs.", secs=20)

Z(HHD, "Pathogens and diseases", I, STP,
  SP("Droplets from the cough or sneezes of a person with the common cold are either inhaled directly or "
     "transmitted through contaminated objects such as pens, books, cups, doorknobs or a computer keyboard.",
     "The filarial worms are transmitted to a healthy person through the bite of female mosquito vectors."),
  "Transmission of common cold and filariasis",
  "NCERT: common cold spreads through droplets inhaled directly or through contaminated objects such as pens, books, "
  "cups, doorknobs, computer keyboard or mouse. Filarial worms (Wuchereria) are transmitted to a healthy person by "
  "the bite of female mosquito vectors.",
  ["Statement I: true", "Statement II: true"],
  "Common diseases in humans", ans="A",
  why="Both statements are NCERT descriptions of transmission, so options calling either false are wrong.",
  secs=40)

Z(HHD, "Pathogens and diseases", I, MUL,
  MS("Which of the following are measures that NCERT recommends for preventing and controlling infectious "
     "diseases?",
     ["Proper disposal of waste and excreta, and periodic cleaning and disinfection of water reservoirs, pools, "
      "cesspools and tanks.",
      "Regular cleaning of household coolers.",
      "Spraying of insecticides in ditches, drainage areas and swamps.",
      "Allowing water to stagnate near houses, since mosquitoes breed only in running water.",
      "Providing doors and windows with wire mesh to prevent the entry of mosquitoes."]),
  "Prevention and control of infectious diseases",
  "Public hygiene includes proper disposal of waste and excreta and periodic cleaning and disinfection of water "
  "reservoirs, pools, cesspools and tanks. Vector-borne diseases are controlled by avoiding stagnation of water "
  "around residential areas, regular cleaning of household coolers, mosquito nets, Gambusia in ponds, spraying "
  "insecticides in ditches, drainage areas and swamps, and wire mesh on doors and windows.",
  ["(a) True", "(b) True", "(c) True", "(d) False: stagnant water must be avoided; mosquitoes breed in it",
   "(e) True"],
  "Common diseases in humans (prevention and control)",
  at="B", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="(d) reverses NCERT's advice to avoid stagnant water, so every option containing it is wrong.", secs=50)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("Even after tissue matching and blood group matching, a patient who receives an organ transplant has to take "
     "immuno-suppressants all his/her life.",
     "Immuno-suppressants strengthen the cell-mediated immune response against the graft."),
  "Graft rejection and immuno-suppressants",
  "Tissue matching and blood group matching are essential before any graft or transplant, and even after this the "
  "patient has to take immuno-suppressants all his/her life. The cell-mediated immune response can reject the graft, "
  "so immuno-suppressants are given to suppress (not strengthen) it.",
  ["A: true (NCERT)", "R: false - immuno-suppressants suppress the immune response"],
  "Immunity (acquired immunity)", ans="C",
  why="R contradicts the purpose of immuno-suppressants, so options A and B are wrong; A is an NCERT line, so D is "
      "wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", I, MAT,
  ML(("drug", "feature"),
     ["Heroin", "Cocaine", "Cannabinoids", "Alcohol (chronic use)"],
     ["Generally taken by inhalation and oral ingestion",
      "Damages the nervous system and the liver (cirrhosis)",
      "White, odourless, bitter crystalline compound taken by snorting and injection",
      "Potent stimulant of the central nervous system producing euphoria and increased energy; excess causes "
      "hallucinations"]),
  "Features of abused drugs",
  "Heroin (diacetylmorphine) is a white, odourless, bitter crystalline compound, generally taken by snorting and "
  "injection. Cocaine has a potent stimulating action on the CNS, producing euphoria and increased energy; excess "
  "causes hallucinations. Cannabinoids are generally taken by inhalation and oral ingestion. Chronic use of drugs "
  "and alcohol damages the nervous system and the liver (cirrhosis).",
  ["A Heroin -> III", "B Cocaine -> IV", "C Cannabinoids -> I", "D Alcohol -> II"],
  "Drugs and alcohol abuse",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Heroin is the crystalline compound taken by snorting and injection, not the stimulant; cocaine is the CNS "
      "stimulant; cannabinoids are inhaled or eaten; any code that swaps these is wrong.", secs=50)

Z(HHD, "Pathogens and diseases", I, MAT,
  ML(("disease", "how infection is acquired"),
     ["Typhoid", "Ascariasis", "Pneumonia", "Ringworm"],
     ["By inhaling droplets/aerosols released by an infected person, or by sharing glasses and utensils with them",
      "From soil, or by using towels, clothes or even the comb of infected individuals",
      "Pathogen enters the small intestine through contaminated food and water and migrates to other organs "
      "through blood",
      "Through water, vegetables or fruits contaminated with eggs passed in the faeces of an infected person"]),
  "Transmission of common diseases",
  "Salmonella typhi enters the small intestine through contaminated food and water and spreads through blood. Eggs "
  "of Ascaris passed with faeces contaminate soil, water and plants; a healthy person is infected through "
  "contaminated water, vegetables and fruits. Pneumonia spreads by inhaling droplets/aerosols or sharing glasses and "
  "utensils. Ringworm is acquired from soil or by using towels, clothes or combs of infected people.",
  ["A Typhoid -> III", "B Ascariasis -> IV", "C Pneumonia -> I", "D Ringworm -> II"],
  "Common diseases in humans",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Typhoid's route is through the small intestine and blood, ascariasis comes from egg-contaminated food, "
      "pneumonia is airborne and ringworm spreads from soil and shared towels or combs; the other codes swap one of "
      "these.", secs=50)

Z(HHD, "Cancer", I, STP,
  SP("Majority of cancers are treated by a combination of surgery, radiotherapy and chemotherapy.",
     "Fewer than ten thousand Indians suffer from cancer."),
  "Cancer in India and its treatment",
  "NCERT: the majority of cancers are treated by a combination of surgery, radiotherapy and chemotherapy. It also "
  "states that more than a million Indians suffer from cancer and a large number of them die from it annually.",
  ["Statement I: true", "Statement II: false - more than a million Indians suffer from cancer"],
  "Cancer", ans="C",
  why="Statement II greatly understates NCERT's figure of more than a million, so options calling it true are "
      "wrong; Statement I is an NCERT line, so options calling it false are wrong.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, MUL,
  MS("Which of the following are listed by NCERT as warning signs of drug and alcohol abuse among youth?",
     ["Drop in academic performance and unexplained absence from school or college",
      "Lack of interest in personal hygiene, withdrawal, isolation and depression",
      "Change in sleeping and eating habits, and fluctuations in weight and appetite",
      "Steadily improving relationships with family and friends",
      "Aggressive and rebellious behaviour"]),
  "Danger signs of drug/alcohol abuse",
  "NCERT lists warning signs: drop in academic performance, unexplained absence from school/college, lack of "
  "interest in personal hygiene, withdrawal, isolation, depression, fatigue, aggressive and rebellious behaviour, "
  "deteriorating (not improving) relationships with family and friends, loss of interest in hobbies, change in "
  "sleeping and eating habits, and fluctuations in weight and appetite.",
  ["(a) True", "(b) True", "(c) True", "(d) False: relationships deteriorate", "(e) True"],
  "Adolescence and drug/alcohol abuse",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="(d) is the opposite of NCERT's 'deteriorating relationships', so every option containing it is wrong.",
  secs=45)

Z(HHD, "Immunity and vaccines", I, D,
  "The principle of immunisation or vaccination is based on which property of the immune system?",
  "Principle of vaccination",
  "NCERT: the principle of immunisation or vaccination is based on the property of 'memory' of the immune system. "
  "A vaccine makes the body produce antibodies and memory B- and T-cells, which recognise the pathogen quickly on "
  "later exposure.",
  ["Vaccination -> primary response + memory B and T cells", "Later exposure -> quick, strong response",
   "Basis: memory of the immune system"],
  "Vaccination and immunisation",
  at="C", correct="Memory",
  wrong=["Inability to distinguish self from non-self", "Non-specific (innate) defence present from birth",
         "Exaggerated response to environmental allergens"],
  why="Failure to tell self from non-self causes auto-immunity; innate defence is non-specific and needs no "
      "vaccine; an exaggerated response to allergens is allergy.", secs=25)

Z(HHD, "HIV and AIDS", A, MUL,
  MS("Which of the following statements about AIDS are correct?",
     ["HIV can be transmitted by sexual contact with an infected person.",
      "HIV can be transmitted by transfusion of contaminated blood and blood products.",
      "HIV can be transmitted by sharing infected needles, as in intravenous drug abusers.",
      "HIV can pass from an infected mother to her child through the placenta.",
      "In AIDS, the immune system attacks the body's own (self) cells, as in auto-immune diseases."]),
  "Transmission of HIV",
  "NCERT: HIV infection is generally transmitted by sexual contact with an infected person, by transfusion of "
  "contaminated blood and blood products, by sharing infected needles (intravenous drug abusers) and from an "
  "infected mother to her child through the placenta. AIDS is an immunodeficiency, in which HIV destroys helper "
  "T-lymphocytes; it is not an auto-immune attack on self cells.",
  ["(a) True", "(b) True", "(c) True", "(d) True", "(e) False: AIDS is immunodeficiency, not auto-immunity"],
  "AIDS",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(a), (c), (d) and (e) only", "(b) and (d) only"],
  why="(e) confuses immunodeficiency with auto-immunity, so options with (e) are wrong; '(b) and (d) only' leaves "
      "out two routes NCERT lists.", secs=55)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Polio, diphtheria, pneumonia and tetanus have been completely eradicated from the world.",
     "The use of vaccines and immunisation programmes has enabled us to completely eradicate a deadly disease like "
     "smallpox."),
  "Achievements of vaccination",
  "NCERT: vaccines and immunisation programmes have enabled us to completely eradicate smallpox. A large number of "
  "other infectious diseases like polio, diphtheria, pneumonia and tetanus have been controlled to a large extent "
  "by vaccines, not completely eradicated.",
  ["A: false - these are controlled to a large extent, not eradicated", "R: true - smallpox was eradicated"],
  "Common diseases in humans (prevention and control)", ans="D",
  why="A overstates 'controlled to a large extent' as 'completely eradicated', so options A, B and C (which call A "
      "true) are wrong.", secs=45)

Z(HHD, "Cancer", A, MAT,
  ML(("agent or technique", "description"),
     ["X-rays and gamma rays", "Tobacco smoke", "Oncogenic viruses", "Radiography"],
     ["Contains chemical carcinogens identified as a major cause of lung cancer",
      "Diagnostic technique that uses X-rays",
      "Ionising radiations that cause DNA damage leading to neoplastic transformation",
      "Carry genes called viral oncogenes"]),
  "Carcinogens and cancer detection",
  "Ionising radiations like X-rays and gamma rays cause DNA damage leading to neoplastic transformation. Chemical "
  "carcinogens in tobacco smoke are a major cause of lung cancer. Cancer-causing (oncogenic) viruses have genes "
  "called viral oncogenes. Radiography, which uses X-rays, is one of the techniques to detect cancers of internal "
  "organs.",
  ["A -> III", "B -> I", "C -> IV", "D -> II"],
  "Cancer (causes and detection)",
  at="B", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "II", "B": "I", "C": "IV", "D": "III"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "I", "B": "III", "C": "IV", "D": "II"}]),
  why="X-rays as such are carcinogenic radiations, while radiography is the diagnostic use of X-rays; swapping these, "
      "or swapping the chemical carcinogen (tobacco) with the biological one (viruses), gives a wrong code.",
  secs=55)

Z(HHD, "HIV and AIDS", A, STP,
  SP("In the term AIDS, 'acquired' indicates that the immune deficiency is acquired during the lifetime of an "
     "individual and is not a congenital disease.",
     "In the term AIDS, 'syndrome' refers to a single specific symptom."),
  "Meaning of the term AIDS",
  "AIDS stands for Acquired Immuno Deficiency Syndrome: a deficiency of the immune system acquired during the "
  "lifetime of an individual, indicating that it is not a congenital disease. 'Syndrome' means a group of symptoms.",
  ["Statement I: true", "Statement II: false - syndrome means a group of symptoms"],
  "AIDS", ans="C",
  why="'Syndrome' is a group of symptoms, so options calling Statement II true are wrong; Statement I is NCERT's "
      "explanation of 'acquired', so options calling it false are wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", A, D,
  "Which of the following is NOT a measure that NCERT suggests for the prevention and control of drug and alcohol "
  "abuse among adolescents?",
  "Prevention and control of drug/alcohol abuse",
  "NCERT's measures: avoid undue peer pressure (a child should not be pushed unduly to perform beyond his/her "
  "threshold limits in studies, sports or other activities); education and counselling to face problems and "
  "stresses; seeking help from parents and peers; looking for danger signs; and seeking professional and medical "
  "help from psychologists, psychiatrists and de-addiction and rehabilitation programmes.",
  ["Avoid undue peer pressure: do NOT push the child beyond threshold limits", "Education and counselling",
   "Help from parents and peers", "Professional and medical help"],
  "Prevention and control (drugs and alcohol abuse)",
  at="C", correct="Pushing the child to perform beyond his/her threshold limits in studies or sports",
  wrong=["Education and counselling to face problems and stresses",
         "Seeking help from parents and peers",
         "Seeking help from psychologists, psychiatrists and de-addiction and rehabilitation programmes"],
  why="The other three are NCERT's own recommended measures; pushing a child beyond his/her limits is exactly what "
      "NCERT says to avoid.", secs=40)

Z(HHD, "Pathogens and diseases", A, STP,
  SP("Entamoeba histolytica, which causes amoebiasis, is a protozoan parasite of the human small intestine.",
     "Heat and moisture help ringworm fungi to grow, which makes them thrive in skin folds such as those in the "
     "groin or between the toes."),
  "Amoebiasis and ringworm",
  "Entamoeba histolytica is a protozoan parasite in the large intestine of humans and causes amoebiasis (amoebic "
  "dysentery). In ringworm, heat and moisture help the fungi grow, so they thrive in skin folds such as in the groin "
  "or between the toes.",
  ["Statement I: false - large intestine, not small intestine", "Statement II: true"],
  "Common diseases in humans", ans="D",
  why="Statement I gives the wrong part of the intestine, so options calling it true are wrong; Statement II is an "
      "NCERT line, so options calling it false are wrong.", secs=45)

# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Bioreactors and downstream processing", B, D,
  "The two core techniques that enabled the birth of modern biotechnology are:",
  "Principles of biotechnology",
  "NCERT: the two core techniques are genetic engineering (altering the chemistry of genetic material to introduce "
  "it into host organisms and change their phenotype) and bioprocess engineering (maintenance of a sterile, "
  "microbial contamination-free ambience to grow only the desired microbe or eukaryotic cell in large quantities).",
  ["Genetic engineering", "Bioprocess engineering"],
  "Principles of biotechnology",
  at="B", correct="Genetic engineering and bioprocess engineering",
  wrong=["Plant breeding and animal husbandry", "Fermentation and pasteurisation",
         "Radiography and computed tomography"],
  why="Breeding and husbandry are traditional improvement methods; fermentation and pasteurisation are older "
      "processes; radiography and CT are diagnostic imaging techniques.", secs=25)

Z(BPP, "Restriction enzymes", B, D,
  "In 1963, two enzymes responsible for restricting the growth of bacteriophage in Escherichia coli were isolated. "
  "One of them added methyl groups to DNA. The other:",
  "Discovery of restriction enzymes",
  "NCERT: in 1963 the two enzymes responsible for restricting bacteriophage growth in E. coli were isolated. One "
  "added methyl groups to DNA, while the other cut DNA; the latter was called restriction endonuclease.",
  ["Enzyme 1: adds methyl groups to DNA", "Enzyme 2: cuts DNA = restriction endonuclease"],
  "Restriction enzymes",
  at="D", correct="Cut DNA and was called a restriction endonuclease",
  wrong=["Joined DNA fragments and was called DNA ligase",
         "Copied RNA into DNA and was called reverse transcriptase",
         "Removed RNA from DNA preparations and was called ribonuclease"],
  why="Ligase joins DNA; reverse transcriptase is the enzyme of retroviruses such as HIV; ribonuclease is used to "
      "remove RNA during DNA isolation. None of them restricts phage growth by cutting DNA.", secs=30)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "In an agarose gel stained with ethidium bromide and exposed to UV light, the separated DNA fragments are seen "
  "as:",
  "Visualising DNA after electrophoresis",
  "DNA fragments can be visualised only after staining with ethidium bromide followed by exposure to UV radiation; "
  "they appear as bright orange coloured bands.",
  ["Stain: ethidium bromide", "Expose to UV", "Bands appear bright orange"],
  "Separation and isolation of DNA fragments",
  at="A", correct="Bright orange coloured bands", wrong=["Blue colonies", "White colonies", "Dark green bands"],
  why="Blue and white colonies describe recombinant selection with a chromogenic substrate, not bands on a gel; "
      "ethidium bromide-stained DNA glows orange, not green.", secs=20)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "In the polymerase chain reaction (PCR), multiple copies of the gene or DNA of interest are synthesised in vitro "
  "using:",
  "Requirements of PCR",
  "In PCR, multiple copies of the gene (or DNA) of interest are synthesised in vitro using two sets of primers "
  "(small chemically synthesised oligonucleotides complementary to regions of the DNA) and the enzyme DNA "
  "polymerase.",
  ["Two sets of primers", "DNA polymerase", "Reaction is in vitro"],
  "Amplification of gene of interest using PCR",
  at="B", correct="Two sets of primers and the enzyme DNA polymerase",
  wrong=["A restriction enzyme and DNA ligase", "Reverse transcriptase and a single primer",
         "Lysozyme and ribonuclease"],
  why="Restriction enzyme and ligase cut and join DNA; reverse transcriptase copies RNA into DNA; lysozyme and "
      "ribonuclease are used during DNA isolation. None amplifies DNA by PCR.", secs=25)

Z(BPP, "Cloning vectors", B, D,
  "Which of the following lists antibiotics whose resistance genes are normally considered useful selectable "
  "markers for E. coli?",
  "Selectable markers",
  "NCERT: genes encoding resistance to antibiotics such as ampicillin, chloramphenicol, tetracycline or kanamycin "
  "are considered useful selectable markers for E. coli.",
  ["Ampicillin", "Chloramphenicol", "Tetracycline", "Kanamycin"],
  "Cloning vectors (selectable marker)",
  at="D", correct="Ampicillin, chloramphenicol, tetracycline and kanamycin",
  wrong=["Lysozyme, cellulase and chitinase", "Ethidium bromide and agarose", "Insulin and interferon"],
  why="Lysozyme, cellulase and chitinase are enzymes for breaking cells; ethidium bromide and agarose are used in "
      "gel electrophoresis; insulin and interferon are recombinant products, not antibiotics.", secs=25)

Z(BPP, "Restriction enzymes", I, STP,
  SP("Each restriction endonuclease functions by 'inspecting' the length of a DNA sequence.",
     "Hind II always cuts DNA molecules at a particular point by recognising a specific sequence of four base "
     "pairs."),
  "How restriction endonucleases act",
  "Each restriction endonuclease inspects the length of a DNA sequence, binds when it finds its recognition "
  "sequence and cuts both strands. Hind II always cuts DNA at a particular point by recognising a specific sequence "
  "of six base pairs, called its recognition sequence.",
  ["Statement I: true", "Statement II: false - six base pairs, not four"],
  "Restriction enzymes", ans="C",
  why="NCERT gives a six-base-pair recognition sequence for Hind II, so options calling Statement II true are wrong; "
      "Statement I is an NCERT line, so options calling it false are wrong.", secs=40)

Z(BPP, "PCR and gel electrophoresis", I, MUL,
  MS("Which of the following statements about the polymerase chain reaction (PCR) are correct?",
     ["By repeating the process, a DNA segment can be amplified approximately a billion times.",
      "The amplified fragment can be used to ligate with a vector for further cloning.",
      "Each cycle consists of denaturation, annealing and extension, in that order.",
      "PCR requires a living host cell to amplify DNA.",
      "In the extension step, DNA polymerase removes the primers from the template."]),
  "Polymerase chain reaction",
  "PCR is carried out in vitro. Each cycle has denaturation of double-stranded DNA, annealing of primers and "
  "extension of the primers by DNA polymerase using the nucleotides and the template. Repeated many times, the "
  "segment is amplified about a billion times, and the amplified fragment can be ligated with a vector for cloning.",
  ["(a) True", "(b) True", "(c) True", "(d) False: PCR is in vitro",
   "(e) False: DNA polymerase extends the primers"],
  "Amplification of gene of interest using PCR",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(d) contradicts the in vitro nature of PCR and (e) reverses what polymerase does to primers; every other "
      "option includes one of them.", secs=50)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("During isolation of DNA, the preparation is treated with a protease.",
     "In the cell, genes are located on long DNA molecules intertwined with proteins such as histones."),
  "Isolation of DNA",
  "To isolate DNA, cells are broken open, releasing DNA with RNA, proteins, polysaccharides and lipids. Because DNA "
  "is intertwined with proteins such as histones, the proteins are removed by treatment with protease (and RNA by "
  "ribonuclease). Purified DNA is then precipitated by chilled ethanol.",
  ["A: true", "R: true", "Proteins bound to DNA must be removed; that is why protease is used: R explains A"],
  "Processes of recombinant DNA technology (isolation of DNA)", ans="A",
  why="R gives the reason protease is needed, so B is wrong; both statements are true, so C and D are wrong.",
  secs=40)

Z(BPP, "Cloning vectors", I, MAT,
  ML(("term", "meaning"),
     ["Plasmid", "Cloning", "Recombinants", "Insertional inactivation"],
     ["Making multiple identical copies of any template DNA",
      "Loss of activity of a gene product, e.g. β-galactosidase, because foreign DNA is inserted within its coding "
      "sequence",
      "Autonomously replicating, circular, extra-chromosomal DNA",
      "Transformed bacterial colonies that carry the vector with the foreign DNA insert"]),
  "Terms in recombinant DNA technology",
  "Plasmids are autonomously replicating circular extra-chromosomal DNA. Cloning means making multiple identical "
  "copies of any template DNA. Recombinants are the transformants (colonies) carrying the insert. Insertional "
  "inactivation is the loss of a gene's activity (such as that of β-galactosidase) when foreign DNA is inserted in "
  "its coding sequence.",
  ["A -> III", "B -> I", "C -> IV", "D -> II"],
  "Tools of recombinant DNA technology; Cloning vectors",
  at="C", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "III", "D": "II"}]),
  why="A plasmid is the circular extra-chromosomal DNA and cloning is the copying of DNA; recombinants are colonies "
      "with the insert, whereas insertional inactivation is the loss of a gene's activity. Other codes swap these.",
  secs=50)

Z(BPP, "Bioreactors and downstream processing", I, D,
  "After separation and purification, a biotechnological product is formulated with suitable preservatives. If the "
  "product is a drug, the formulation must additionally undergo:",
  "Downstream processing",
  "Downstream processing includes separation and purification of the product and its formulation with suitable "
  "preservatives. Such a formulation has to undergo thorough clinical trials in the case of drugs, and strict "
  "quality control testing is required for each product.",
  ["Separation and purification", "Formulation with preservatives", "Drugs: thorough clinical trials"],
  "Downstream processing",
  at="B", correct="Thorough clinical trials",
  wrong=["Insertional inactivation", "Heat shock at 42 °C", "Annealing with primers"],
  why="Insertional inactivation is a way of selecting recombinants; heat shock is used to transform bacteria; "
      "annealing is a step of PCR. None is a step after formulation of a drug.", secs=30)

Z(BPP, "Bioreactors and downstream processing", I, STP,
  SP("Small volume cultures can yield appreciable quantities of products, so bioreactors are not required for "
     "large-scale production.",
     "In a sparged stirred-tank bioreactor, sterile air bubbles are sparged, which greatly increases the area for "
     "oxygen transfer."),
  "Need for bioreactors",
  "NCERT: small volume cultures cannot yield appreciable quantities of products; large-scale production needs "
  "bioreactors in which large volumes (100-1000 litres) are processed. In a sparged stirred-tank bioreactor, sterile "
  "air bubbles are sparged, which increases the surface area for oxygen transfer.",
  ["Statement I: false - small cultures cannot give appreciable yields", "Statement II: true"],
  "Obtaining the foreign gene product (bioreactors)", ans="D",
  why="Statement I contradicts the very reason bioreactors were developed, so options calling it true are wrong; "
      "Statement II is an NCERT line, so options calling it false are wrong.", secs=40)

Z(BPP, "PCR and gel electrophoresis", I, ASR,
  AR("A thermostable DNA polymerase is used in PCR.",
     "The enzyme must remain active during the high temperature used for denaturation of the double-stranded DNA."),
  "Thermostable DNA polymerase in PCR",
  "In each PCR cycle the double-stranded DNA is denatured at high temperature. NCERT states that the thermostable "
  "DNA polymerase (isolated from Thermus aquaticus) is used because it remains active during this high temperature "
  "induced denaturation.",
  ["A: true", "R: true", "Surviving the denaturation temperature is the reason a thermostable enzyme is chosen"],
  "Amplification of gene of interest using PCR", ans="A",
  why="R is the reason for A, so B is wrong; both statements are true, so C and D are wrong.", secs=40)

Z(BPP, "PCR and gel electrophoresis", A, NUM,
  "A PCR is started with a single double-stranded DNA molecule. Each cycle doubles the DNA, and every new molecule "
  "is made of one old and one new strand. After 5 cycles, how many double-stranded molecules contain NO strand of "
  "the original template molecule?",
  "Semi-conservative copying in PCR",
  "After n cycles there are 2^n molecules. The two original strands are never destroyed; each stays paired with a "
  "new strand, so exactly 2 molecules carry an original strand. The rest are made entirely of new strands.",
  ["Total after 5 cycles = 2^5 = 32", "Molecules carrying an original strand = 2", "Fully new molecules = 32 - 2 = 30"],
  "Amplification of gene of interest using PCR",
  at="C", correct="30", wrong=["32", "31", "16"],
  short="Fully new molecules = 2^n - 2.",
  why="32 is the total number of molecules; 31 assumes only one molecule keeps template DNA, but there are two "
      "template strands; 16 is the number after 4 cycles or half of 32.", secs=75, vb=RECOMPUTED)

Z(BPP, "Cloning vectors", A, NUM,
  "Foreign DNA is ligated at the BamHI site of pBR322, which lies within the tetracycline resistance gene, and the "
  "products are used to transform E. coli. On an ampicillin-containing medium, 200 colonies grow. When these 200 "
  "colonies are transferred to a tetracycline-containing medium, 150 of them grow. How many of the 200 colonies are "
  "recombinants?",
  "Selection of recombinants by insertional inactivation",
  "All 200 colonies are transformants (they carry ampR). Insertion at the BamHI site inactivates tetR, so "
  "recombinants grow on ampicillin but not on tetracycline. Non-recombinants grow on both. Recombinants = colonies "
  "that fail on tetracycline.",
  ["Transformants on ampicillin = 200", "Grow on tetracycline too = non-recombinants = 150",
   "Recombinants = 200 - 150 = 50"],
  "Cloning vectors (selectable marker; insertional inactivation)",
  at="A", correct="50", wrong=["150", "200", "350"],
  why="150 are the non-recombinants that kept tetracycline resistance; 200 counts all transformants; 350 adds the "
      "two counts.", secs=70, vb=RECOMPUTED)

Z(BPP, "Restriction enzymes", A, NUM,
  "A circular plasmid with a single EcoRI site is cut with EcoRI, and a foreign DNA fragment with EcoRI sticky ends "
  "at both ends is inserted. How many phosphodiester bonds must DNA ligase form to give a covalently closed circular "
  "recombinant plasmid?",
  "Action of DNA ligase on sticky ends",
  "A restriction enzyme cuts each of the two strands at specific points in the sugar-phosphate backbone. The insert "
  "joins the vector at two junctions, and at each junction both strands have a nick in the backbone that ligase "
  "must seal.",
  ["Junctions between vector and insert = 2", "Nicks per junction = 2 (one in each strand)",
   "Bonds formed by ligase = 2 × 2 = 4"],
  "Tools of recombinant DNA technology (restriction enzymes, ligase)",
  at="D", correct="4", wrong=["2", "1", "8"],
  why="2 counts only the junctions and forgets that both strands are cut; 1 treats the insertion as a single join; "
      "8 double-counts each nick.", secs=75, vb=RECOMPUTED)

Z(BPP, "Competent hosts and transformation", A, STP,
  SP("'Disarmed pathogen' vectors, when allowed to infect the cell, transfer the recombinant DNA into the host.",
     "Biolistics (gene gun) is a method suitable mainly for animal cells."),
  "Methods of introducing recombinant DNA",
  "NCERT lists micro-injection (DNA injected into the nucleus of an animal cell), biolistics or gene gun (suitable "
  "for plants; cells bombarded with gold or tungsten micro-particles coated with DNA) and disarmed pathogen vectors, "
  "which transfer the recombinant DNA into the host when allowed to infect the cell.",
  ["Statement I: true", "Statement II: false - biolistics is the method suitable for plants"],
  "Insertion of recombinant DNA into the host cell/organism", ans="C",
  why="NCERT names biolistics as suitable for plants (micro-injection is the animal-cell method), so options calling "
      "Statement II true are wrong; Statement I is an NCERT line, so options calling it false are wrong.", secs=45)

Z(BPP, "Competent hosts and transformation", A, D,
  "Which of the following is the correct order of steps for isolating pure DNA from a bacterial or plant cell?",
  "Isolation of DNA",
  "The cell is first broken open with enzymes (lysozyme for bacteria, cellulase for plant cells, chitinase for "
  "fungi). RNA is removed with ribonuclease and proteins with protease; other molecules are removed by appropriate "
  "treatments. Finally, chilled ethanol is added and purified DNA precipitates as fine threads.",
  ["1. Break cell walls/membranes with enzymes", "2. Remove RNA (ribonuclease) and proteins (protease)",
   "3. Precipitate DNA with chilled ethanol"],
  "Processes of recombinant DNA technology (isolation of DNA)",
  at="B", correct="Lyse cells with enzymes → treat with ribonuclease and protease → precipitate DNA with chilled "
                  "ethanol",
  wrong=["Precipitate DNA with chilled ethanol → lyse cells with enzymes → treat with ribonuclease and protease",
         "Treat with ribonuclease and protease → precipitate DNA with chilled ethanol → lyse cells with enzymes",
         "Lyse cells with enzymes → precipitate DNA with chilled ethanol → digest the precipitate with DNase"],
  why="DNA cannot be precipitated before the cells are opened; RNA and protein cannot be removed before they are "
      "released; DNase would destroy the DNA being isolated.", secs=40)

# ================================================================ Biotechnology and its Applications (5/6/5)
Z(BTA, "Bt crops and RNAi", B, D,
  "In 'Bt cotton', the abbreviation Bt stands for:",
  "Source of the Bt toxin",
  "Bt toxin is produced by the soil bacterium Bacillus thuringiensis (Bt for short). The gene for the toxin has been "
  "cloned from the bacterium and expressed in plants such as cotton.",
  ["Bt = Bacillus thuringiensis"],
  "Biotechnological applications in agriculture",
  at="A", correct="Bacillus thuringiensis",
  wrong=["Biotechnology transfer", "Bacterial toxin from E. coli", "Biolistic transformation"],
  why="Bt is the name of the bacterium, not a technique; E. coli does not produce the Bt toxin; biolistics is a gene "
      "transfer method.", secs=20)

Z(BTA, "Transgenic animals", B, D,
  "Besides mice, which of the following groups of animals does NCERT list as having been made transgenic?",
  "Transgenic animals produced",
  "NCERT: although transgenic rats, rabbits, pigs, sheep, cows and fish have been produced, over 95 per cent of all "
  "existing transgenic animals are mice.",
  ["Listed: rats, rabbits, pigs, sheep, cows and fish", "Most (over 95%) are mice"],
  "Transgenic animals",
  at="C", correct="Rats, rabbits, pigs, sheep, cows and fish",
  wrong=["Only primates such as monkeys and apes", "Only insects such as fruit flies and mosquitoes",
         "No other animal; only plants besides mice"],
  why="NCERT's list is rats, rabbits, pigs, sheep, cows and fish; it does not limit transgenic animals to primates, "
      "insects or mice.", secs=25)

Z(BTA, "Bt crops and RNAi", B, D,
  "To make tobacco plants resistant to the nematode Meloidegyne incognitia by RNA interference, nematode-specific "
  "genes were introduced into the host plants using vectors derived from:",
  "Vector used in RNAi for nematode resistance",
  "Using Agrobacterium vectors, nematode-specific genes were introduced into the host (tobacco) plants. They "
  "produced both sense and anti-sense RNA in the host cells, forming dsRNA that initiated RNAi.",
  ["Vector: Agrobacterium", "Genes produce sense + anti-sense RNA -> dsRNA -> RNAi"],
  "Pest resistant plants (RNA interference)",
  at="D", correct="Agrobacterium", wrong=["Retroviruses", "Bacteriophage lambda", "HIV"],
  why="Disarmed retroviruses are used to deliver genes into animal cells; NCERT names Agrobacterium for this tobacco "
      "work; HIV is a human pathogen, not a plant vector.", secs=25)

Z(BTA, "Bt crops and RNAi", B, D,
  "Some strains of Bacillus thuringiensis produce proteins that kill lepidopterans. NCERT gives which of the "
  "following as examples of lepidopterans?",
  "Insects killed by Bt toxins",
  "Some strains of Bacillus thuringiensis produce proteins that kill certain insects such as lepidopterans (tobacco "
  "budworm, armyworm), coleopterans (beetles) and dipterans (flies, mosquitoes).",
  ["Lepidopterans: tobacco budworm, armyworm", "Coleopterans: beetles", "Dipterans: flies, mosquitoes"],
  "Biotechnological applications in agriculture (Bt cotton)",
  at="B", correct="Tobacco budworm and armyworm", wrong=["Beetles", "Flies and mosquitoes", "Nematodes"],
  why="Beetles are coleopterans; flies and mosquitoes are dipterans; nematodes are roundworms, not insects.",
  secs=25)

Z(BTA, "Transgenic animals", B, D,
  "NCERT states that transgenic models exist for many human diseases. Which of the following is one of the "
  "diseases it names?",
  "Transgenic models for the study of disease",
  "Transgenic animals are designed to increase our understanding of how genes contribute to the development of "
  "disease. NCERT: transgenic models exist for many human diseases such as cancer, cystic fibrosis, rheumatoid "
  "arthritis and Alzheimer's.",
  ["Diseases named: cancer, cystic fibrosis, rheumatoid arthritis, Alzheimer's"],
  "Transgenic animals (study of disease)",
  at="A", correct="Rheumatoid arthritis", wrong=["Common cold", "Ringworm", "Typhoid"],
  why="Common cold, ringworm and typhoid are infectious diseases caused by pathogens and are not among NCERT's "
      "examples of transgenic disease models.", secs=25)

Z(BTA, "Transgenic animals", I, STP,
  SP("Rosie, the first transgenic cow, was produced in 1997.",
     "The milk produced by Rosie was nutritionally a less balanced product for human babies than natural cow milk."),
  "Transgenic cow Rosie",
  "NCERT: in 1997, the first transgenic cow, Rosie, produced human protein-enriched milk (2.4 grams per litre). The "
  "milk contained human alpha-lactalbumin and was nutritionally a MORE balanced product for human babies than "
  "natural cow milk.",
  ["Statement I: true", "Statement II: false - more balanced, not less"],
  "Transgenic animals (biological products)", ans="C",
  why="Statement II reverses NCERT's comparison, so options calling it true are wrong; Statement I is an NCERT line, "
      "so options calling it false are wrong.", secs=35)

Z(BTA, "Bt crops and RNAi", I, MUL,
  MS("Which of the following statements about Bt toxins and Bt crops are correct?",
     ["Coleopterans killed by some Bt toxins are beetles.",
      "Dipterans killed by some Bt toxins include flies and mosquitoes.",
      "Bt cotton still needs heavy insecticide spraying to control bollworms.",
      "The Bt toxin kills insects by dissolving their exoskeleton.",
      "The Bt toxin is an insecticidal protein."]),
  "Bt toxin",
  "Bacillus thuringiensis forms protein crystals containing a toxic insecticidal protein. Some strains kill "
  "lepidopterans, coleopterans (beetles) and dipterans (flies, mosquitoes). Once activated in the alkaline gut, the "
  "toxin binds the midgut epithelial cells and creates pores, causing swelling and lysis; it does not dissolve the "
  "exoskeleton. Bt cotton gives resistance to insects without the need for insecticides.",
  ["(a) True", "(b) True", "(c) False: no insecticide needed", "(d) False: it acts on midgut epithelial cells",
   "(e) True"],
  "Biotechnological applications in agriculture (Bt cotton)",
  at="D", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="(c) denies the main advantage of Bt cotton and (d) gives the wrong site of action; every other option "
      "contains one of them.", secs=50)

Z(BTA, "Bt crops and RNAi", I, ASR,
  AR("RNA interference (RNAi) involves the silencing of a specific mRNA.",
     "A complementary dsRNA molecule binds to the mRNA and prevents its translation."),
  "Mechanism of RNAi",
  "NCERT: RNAi involves silencing of a specific mRNA due to a complementary dsRNA molecule that binds to and "
  "prevents translation of the mRNA (silencing).",
  ["A: true", "R: true", "Binding of the complementary dsRNA and blocking of translation is how the mRNA is silenced"],
  "Pest resistant plants (RNA interference)", ans="A",
  why="R is the mechanism that produces A, so B is wrong; both are true, so C and D are wrong.", secs=35)

Z(BTA, "Transgenic animals", I, MAT,
  ML(("use of transgenic animals", "NCERT example or advantage"),
     ["Normal physiology and development", "Study of disease", "Chemical safety testing", "Vaccine safety"],
     ["Results are obtained in less time",
      "Mice used to test the polio vaccine could replace the use of monkeys",
      "Altering the formation of insulin-like growth factor to learn its biological role",
      "Increasing our understanding of how genes contribute to the development of disease"]),
  "Uses of transgenic animals",
  "To study normal physiology, genes that alter the formation of insulin-like growth factor are introduced and the "
  "biological effects studied. Disease models increase understanding of how genes contribute to disease. "
  "Toxicity testing with transgenic animals gives results in less time. Transgenic mice used to test the polio "
  "vaccine could, if reliable, replace the use of monkeys.",
  ["A -> III", "B -> IV", "C -> I", "D -> II"],
  "Transgenic animals",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The insulin-like growth factor work studies normal physiology, not disease; faster results belong to "
      "toxicity testing, while replacing monkeys belongs to vaccine safety; the other codes swap these.", secs=50)

Z(BTA, "Biosafety, biopiracy and patents", I, STP,
  SP("NCERT presents the use of genetically modified crops as a possible solution for minimising the use of "
     "fertilisers and chemicals, so that their harmful effects on the environment are reduced.",
     "When transgenic animals are used for chemical safety testing, the procedure is the same as that used for "
     "testing the toxicity of drugs."),
  "Reducing environmental harm and testing chemical safety",
  "NCERT asks whether there is a way to minimise the use of fertilisers and chemicals so that their harmful effects "
  "on the environment are reduced, and answers that the use of genetically modified crops is a possible solution. "
  "Among the uses of transgenic animals, chemical safety testing (toxicity/safety testing) follows the same "
  "procedure as that used for testing the toxicity of drugs.",
  ["Statement I: true (GM crops as a possible solution)", "Statement II: true (same procedure as drug toxicity "
   "testing)"],
  "Applications of biotechnology in agriculture; Transgenic animals", ans="A",
  why="Both are NCERT statements, so options calling either false are wrong.", secs=40)

Z(BTA, "Transgenic animals", I, NUM,
  "According to NCERT, the transgenic cow Rosie produced milk enriched with human alpha-lactalbumin at 2.4 grams "
  "per litre. If such a cow gives 15 litres of milk a day, how much human alpha-lactalbumin would it yield in one "
  "week (7 days)?",
  "Yield from a transgenic animal",
  "Protein per day = concentration × volume; protein per week = daily amount × 7.",
  ["Per day = 2.4 g/L × 15 L = 36 g", "Per week = 36 g × 7 = 252 g"],
  "Transgenic animals (biological products)",
  at="B", correct="252 g", wrong=["36 g", "16.8 g", "43.75 g"],
  why="36 g is the yield of one day only; 16.8 g multiplies the concentration by 7 and forgets the 15 litres; "
      "43.75 g divides the volume by the concentration instead of multiplying.", secs=45, vb=RECOMPUTED)

Z(BTA, "Transgenic animals", A, ASR,
  AR("Medicines containing biological products are always cheap and easy to make, so transgenic animals are not "
     "needed to produce them.",
     "Transgenic animals that produce useful biological products can be created by introducing the portion of DNA "
     "(or genes) which codes for a particular product."),
  "Transgenic animals and biological products",
  "NCERT: medicines required to treat certain human diseases can contain biological products, but such products are "
  "often expensive to make. Transgenic animals that produce useful biological products can be created by "
  "introducing the portion of DNA (or genes) coding for a particular product, e.g. human protein (α-1-antitrypsin) "
  "used to treat emphysema.",
  ["A: false - such products are often expensive to make", "R: true"],
  "Transgenic animals (biological products)", ans="D",
  why="A contradicts NCERT ('often expensive to make'), so options A, B and C, which call A true, are wrong.",
  secs=45)

Z(BTA, "Gene therapy", A, MUL,
  MS("Which of the following statements about gene therapy are correct?",
     ["Gene therapy is a collection of methods that allows correction of a gene defect that has been diagnosed in a "
      "child or embryo.",
      "In gene therapy, genes are inserted into a person's cells and tissues to treat a disease.",
      "Gene therapy can be applied only to adults and never at the embryonic stage.",
      "In the gene therapy for ADA deficiency, the functional ADA cDNA was introduced into lymphocytes using "
      "Agrobacterium tumefaciens as the vector."]),
  "Gene therapy",
  "NCERT: gene therapy is a collection of methods that allows correction of a gene defect diagnosed in a child or "
  "embryo; genes are inserted into a person's cells and tissues to treat a disease. A permanent cure for ADA "
  "deficiency may come from introducing the gene into cells at early embryonic stages. In the ADA gene therapy the "
  "functional cDNA was introduced into the patient's lymphocytes using a retroviral vector, not Agrobacterium.",
  ["(a) True", "(b) True", "(c) False: defects in embryos are also targets", "(d) False: a retroviral vector was "
   "used"],
  "Biotechnological applications in medicine (gene therapy)",
  at="D", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(b) and (d) only", "(a), (c) and (d) only"],
  why="(c) contradicts the definition, which includes embryos, and (d) names a plant vector instead of the "
      "retroviral vector used; every other option contains one of them.", secs=55)

Z(BTA, "Bt crops and RNAi", A, STP,
  SP("Meloidegyne incognitia, against which tobacco was protected by RNAi, is an insect pest.",
     "The transgenic tobacco plant expressing the specific interfering RNA was protected from the parasite, which "
     "could not survive in it."),
  "RNAi against a nematode",
  "Meloidegyne incognitia is a nematode (roundworm) that infects the roots of tobacco plants; it is not an insect. "
  "Nematode-specific genes introduced through Agrobacterium produced sense and anti-sense RNA, forming dsRNA that "
  "silenced a specific mRNA of the nematode, so the parasite could not survive in the transgenic host and the plant "
  "was protected.",
  ["Statement I: false - it is a nematode", "Statement II: true"],
  "Pest resistant plants (RNA interference)", ans="D",
  why="Calling a nematode an insect makes Statement I false, so options calling it true are wrong; Statement II is "
      "NCERT's outcome, so options calling it false are wrong.", secs=45)

Z(BTA, "Human insulin", A, MUL,
  MS("Which of the following statements about recombinant therapeutics and insulin are correct according to NCERT?",
     ["About 30 recombinant therapeutics have been approved for human use the world over.",
      "In India, 12 of these recombinant therapeutics are presently being marketed.",
      "Management of adult-onset diabetes is possible by taking insulin at regular time intervals.",
      "Recombinant human insulin is produced by inserting the insulin genes into the nematode Meloidegyne "
      "incognitia.",
      "Recombinant therapeutics have to be extracted from the pancreas of slaughtered animals."]),
  "Recombinant therapeutics and insulin",
  "NCERT: about 30 recombinant therapeutics have been approved for human use the world over, and in India 12 of "
  "these are presently being marketed. Management of adult-onset diabetes is possible by taking insulin at regular "
  "time intervals. Recombinant insulin was made by introducing DNA sequences for the A and B chains into plasmids of "
  "E. coli; animal pancreas was the older source that recombinant technology replaced.",
  ["(a) True", "(b) True", "(c) True", "(d) False: E. coli plasmids were used",
   "(e) False: recombinant products are made in host cells, not extracted from animal pancreas"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(d) names a nematode as the host and (e) describes the older animal source, so every option containing "
      "either is wrong.", secs=60)

Z(BTA, "Bt crops and RNAi", A, ASR,
  AR("Bt cotton, in effect, acts as a bio-pesticide.",
     "The Bt toxin gene cloned from Bacillus thuringiensis is expressed in the cotton plant and provides resistance "
     "to insects without the need for insecticides."),
  "Bt cotton as a bio-pesticide",
  "NCERT: the Bt toxin gene has been cloned from the bacterium and expressed in plants to provide resistance to "
  "insects without the need for insecticides; in effect this has created a bio-pesticide. The plant itself makes "
  "the insecticidal protein, which is why it works like a pesticide of biological origin.",
  ["A: true", "R: true", "Because the plant makes its own insect-killing protein (R), it acts as a bio-pesticide "
   "(A)"],
  "Biotechnological applications in agriculture (Bt cotton)", ans="A",
  why="NCERT states A as the consequence of R, so B is wrong; both are true, so C and D are wrong.", secs=45)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 122
    ids = [x["question_id"] for x in QUESTIONS]
    assert ids[0] == pkg["question_ids"][0] and ids[-1] == pkg["question_ids"][1] and len(set(ids)) == len(ids)
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    assert all(x["subtopic"] in subtopics[x["topic"]] for x in QUESTIONS)
    assert all(x["solution"]["ncert_reference"] and x["solution"]["why_others_wrong"] for x in QUESTIONS)
    stems = [x["question_text"] for x in QUESTIONS]
    assert len(set(stems)) == len(stems), "duplicate stem"
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert max(keys.values()) - min(keys.values()) <= 3, keys
    for f in (D, ASR, STP, MAT, MUL):
        assert fmts[f] >= 0.08 * len(QUESTIONS), (f, fmts)
    assert 0.03 * len(QUESTIONS) <= fmts[NUM] <= 0.08 * len(QUESTIONS), fmts
    assert all("script:recompute" in x["verification"]["verified_by"] for x in QUESTIONS if x["format"] == NUM)
    assert all("script:recompute" not in x["verification"]["verified_by"] for x in QUESTIONS if x["format"] != NUM)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "ZOO_003_p2: 122 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers re-derived in tools/batch_003/ZOO_003_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
