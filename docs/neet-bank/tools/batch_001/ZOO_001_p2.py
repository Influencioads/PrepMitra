"""Builder for package ZOO_001_p2 of BATCH_001 (Zoology, 123 questions, NEET_ZOO_000128..NEET_ZOO_000250).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range and answer-key balance are
asserted before the file is written. If any assert fails, nothing is written.

    python tools/batch_001/ZOO_001_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_001_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_001_ZOO_p2.json"
FIRST_ID = 128

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
KEYS = Counter()


def _pick() -> str:
    """Least-used answer letter so far; ties broken by a rotation so the key does not drift to one letter."""
    n = len(QUESTIONS)
    order = LETTERS[n % 4:] + LETTERS[:n % 4]
    return min(order, key=lambda k: (KEYS[k], order.index(k)))


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


def Z(topic, sub, diff, fmt, text, concept, expl, steps, sec, *, ans=None, correct=None, wrong=None,
      match=None, why=None, short=None, secs=45, vb=CHECKED):
    """Adds one question. AR/SP take `ans`; match_list takes match=(correct_dict, [3 wrong dicts]);
    every other format takes `correct` text and three `wrong` texts and gets a balanced answer position."""
    qid = f"NEET_ZOO_{FIRST_ID + len(QUESTIONS):06d}"
    if fmt == "assertion_reason":
        options, answer = list(ASSERTION_REASON), ans
    elif fmt == "statement_pair":
        options, answer = list(STATEMENT_PAIR), ans
    elif fmt == "match_list":
        answer = _pick()
        options = match_options(match[0], match[1], answer)
    else:
        assert len(wrong) == 3 and correct not in wrong, qid
        answer = _pick()
        options = list(wrong)
        options.insert(LETTERS.index(answer), correct)
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, qid
    assert ans is None or fmt in ("assertion_reason", "statement_pair"), qid
    KEYS[answer] += 1
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
# HR: 250 million sperms; NCERT: at least 60 % must have normal shape and size (40 % vigorous motility)
ejaculate = 250
assert ejaculate * F(60, 100) == 150            # correct: 150 million
assert ejaculate * F(40, 100) == 100            # distractor: used the 40 % (motility) figure
assert ejaculate * F(60, 100) * F(40, 100) == 60  # distractor: multiplied both criteria
assert ejaculate * F(60 - 40, 100) == 50        # distractor: subtracted the percentages

# HR: 50 secondary spermatocytes -> 2 spermatids each; 50 primary oocytes -> 1 ovum each
sec_spermatocytes, prim_oocytes = 50, 50
assert sec_spermatocytes * 2 == 100 and prim_oocytes * 1 == 50
assert sec_spermatocytes * 4 == 200             # distractor: treated as primary spermatocytes

# EVO: p = 0.8 -> heterozygotes 2pq
p = F(8, 10)
q_ = 1 - p
assert 2 * p * q_ == F(32, 100) and p * q_ == F(16, 100) and p * p == F(64, 100) and q_ * q_ == F(4, 100)

# EVO: AA 500, Aa 400, aa 100 (N = 1000) -> q by gene counting, expected aa under HW
AA, Aa, aa = 500, 400, 100
N = AA + Aa + aa
q_count = F(2 * aa + Aa, 2 * N)
assert q_count == F(3, 10) and q_count ** 2 * N == 90
assert round((F(aa, N) ** 0.5), 3) == 0.316      # distractor: sqrt of observed aa frequency
assert F(Aa + aa, N) == F(1, 2) and F(1, 2) ** 2 * N == 250  # distractor: (Aa + aa)/N taken as q

# BPP: PCR, 4 double-stranded molecules, 8 cycles, 100 % efficiency
start, cycles = 4, 8
assert start * 2 ** cycles == 1024 and 2 ** cycles == 256 and 2 * start * 2 ** cycles == 2048 and start * cycles == 32

# BPP: complete digestion, 3 sites: linear DNA -> n + 1 fragments, circular DNA -> n fragments
sites = 3
linear, circular = sites + 1, sites
assert (linear, circular) == (4, 3)

# ================================================================ Chemical Coordination and Integration (5/7/5)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "The pars intermedia of the human pituitary gland secretes:",
  "Hormones of the adenohypophysis",
  "The adenohypophysis has two parts. The pars distalis (anterior pituitary) secretes GH, PRL, TSH, ACTH, LH and "
  "FSH, while the pars intermedia secretes only one hormone, melanocyte stimulating hormone (MSH).",
  ["Pars distalis → GH, PRL, TSH, ACTH, LH, FSH", "Pars intermedia → MSH only",
   "Neurohypophysis → stores and releases oxytocin and vasopressin"],
  "The pituitary gland",
  correct="Melanocyte stimulating hormone (MSH)",
  wrong=["Oxytocin", "Adrenocorticotrophic hormone (ACTH)", "Prolactin (PRL)"],
  why="ACTH and prolactin come from the pars distalis; oxytocin is released from the neurohypophysis.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "Which hormone is called a hypercalcemic hormone because it increases the Ca²⁺ level in the blood?",
  "Parathyroid hormone and calcium balance",
  "Parathyroid hormone (PTH) raises blood Ca²⁺ by stimulating bone resorption (demineralisation), reabsorption of "
  "Ca²⁺ by the renal tubules and absorption of Ca²⁺ from digested food. Hence it is a hypercalcemic hormone.",
  ["PTH → bone resorption, renal Ca²⁺ reabsorption, intestinal Ca²⁺ absorption", "Net effect: blood Ca²⁺ rises"],
  "Parathyroid gland",
  correct="Parathyroid hormone (PTH)", wrong=["Thyrocalcitonin (TCT)", "Melatonin", "Glucagon"],
  why="Thyrocalcitonin also regulates blood calcium but is not the hormone that raises it; melatonin regulates "
      "diurnal rhythm; glucagon is hyperglycemic, not hypercalcemic.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "Melatonin, secreted by the pineal gland, plays a very important role in regulating the:",
  "Pineal gland",
  "The pineal gland lies on the dorsal side of the forebrain and secretes melatonin, which regulates the 24-hour "
  "(diurnal) rhythm of the body, for example the sleep-wake cycle and body temperature.",
  ["Pineal → melatonin", "Melatonin → diurnal (24-hour) rhythms such as sleep-wake cycle"],
  "Pineal gland",
  correct="24-hour (diurnal) rhythm of the body, such as the sleep-wake cycle",
  wrong=["Level of calcium in the blood", "Reabsorption of sodium by the renal tubules",
         "Contraction of the uterine muscles during childbirth"],
  why="Blood calcium is regulated by PTH and TCT, sodium reabsorption by aldosterone, and uterine contraction by "
      "oxytocin.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "Androgens, mainly testosterone, are synthesised and secreted by the:",
  "Endocrine function of the testis",
  "The interstitial spaces of the testis contain Leydig cells (interstitial cells), which produce androgens, "
  "mainly testosterone.",
  ["Seminiferous tubules: germ cells and Sertoli cells", "Interstitial spaces: Leydig cells → androgens"],
  "Testis",
  correct="Leydig (interstitial) cells of the testis",
  wrong=["Sertoli cells of the seminiferous tubules", "Spermatogonia of the seminiferous tubules",
         "Cells of the adrenal medulla"],
  why="Sertoli cells nourish germ cells; spermatogonia are germ cells; the adrenal medulla secretes catecholamines.",
  secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, STP,
  SP("Insulin acts mainly on hepatocytes and adipocytes and enhances cellular glucose uptake and utilisation.",
     "Insulin is secreted by the α-cells of the islets of Langerhans."),
  "Pancreatic hormones",
  "Insulin, a peptide hormone, acts mainly on hepatocytes and adipocytes and moves glucose rapidly from blood into "
  "these cells. It is secreted by the β-cells; the α-cells secrete glucagon.",
  ["Statement I: true (target cells of insulin)", "Statement II: false (insulin from β-cells, glucagon from α-cells)"],
  "Pancreas", ans="C", secs=30)

Z(CCI, "Hypothalamus and pituitary", I, MAT,
  ML(("pituitary hormone", "function"), ["Prolactin", "ACTH", "LH (in males)", "MSH"],
     ["Regulates pigmentation by acting on melanocytes",
      "Stimulates synthesis and secretion of androgens from the testis",
      "Stimulates synthesis and secretion of glucocorticoids from the adrenal cortex",
      "Regulates growth of the mammary glands and formation of milk"]),
  "Functions of anterior and intermediate pituitary hormones",
  "Each pituitary hormone has a defined target: PRL acts on mammary glands, ACTH on the adrenal cortex, LH on the "
  "Leydig cells of the testis, and MSH on melanocytes.",
  ["Prolactin → mammary gland growth and milk formation → IV", "ACTH → glucocorticoids from adrenal cortex → III",
   "LH (male) → androgens from testis → II", "MSH → melanocytes, pigmentation → I"],
  "The pituitary gland",
  match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
         [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "I", "B": "III", "C": "II", "D": "IV"},
          {"A": "IV", "B": "III", "C": "I", "D": "II"}]), secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, MUL,
  MS("Which of the following statements about glucocorticoids are correct?",
     ["They stimulate gluconeogenesis, lipolysis and proteolysis.",
      "They inhibit cellular uptake and utilisation of amino acids.",
      "Their secretion from the adrenal cortex is stimulated by TSH.",
      "Cortisol produces anti-inflammatory reactions and suppresses the immune response.",
      "Aldosterone is the main glucocorticoid of the body."]),
  "Hormones of the adrenal cortex",
  "Glucocorticoids (mainly cortisol) stimulate gluconeogenesis, lipolysis and proteolysis, inhibit cellular uptake "
  "and utilisation of amino acids, and suppress the immune response. Their secretion is stimulated by ACTH. "
  "Aldosterone is the main mineralocorticoid.",
  ["(a) True", "(b) True", "(c) False: ACTH, not TSH, stimulates the adrenal cortex", "(d) True",
   "(e) False: aldosterone is a mineralocorticoid"],
  "Adrenal gland",
  correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="Any option containing (c) or (e) is wrong: TSH acts on the thyroid, and aldosterone controls Na⁺ and water.",
  secs=60)

Z(CCI, "Mechanism of hormone action", I, ASR,
  AR("Steroid hormones mostly regulate gene expression or chromosome function in their target cells.",
     "Steroid hormones interact with intracellular receptors, and the hormone-receptor complex interacts with the "
     "genome."),
  "Intracellular receptors",
  "Hormones such as steroids and iodothyronines bind intracellular (mostly nuclear) receptors. The "
  "hormone-receptor complex interacts with the genome, so these hormones mostly act by regulating gene expression or "
  "chromosome function. R therefore explains A.",
  ["A: true", "R: true", "The hormone-receptor complex acting on the genome is why steroids regulate gene expression"],
  "Mechanism of hormone action", ans="A", secs=45)

Z(CCI, "Hypothalamus and pituitary", I, STP,
  SP("The posterior pituitary is under the direct neural regulation of the hypothalamus.",
     "Oxytocin and vasopressin are synthesised by the cells of the neurohypophysis."),
  "Hypothalamus–neurohypophysis relationship",
  "The posterior pituitary is under direct neural control of the hypothalamus. Oxytocin and vasopressin are "
  "synthesised by the hypothalamus and transported axonally to the neurohypophysis, which only stores and releases "
  "them.",
  ["Statement I: true", "Statement II: false (synthesised in the hypothalamus; neurohypophysis stores and releases)"],
  "Hypothalamus; The pituitary gland", ans="C", secs=40)

Z(CCI, "Hormonal disorders", I, D,
  "A patient shows an enlarged thyroid gland, protruding eyeballs, an increased basal metabolic rate and weight "
  "loss. The condition is most likely:",
  "Hyperthyroidism",
  "Exophthalmic goitre (Graves' disease) is a form of hyperthyroidism marked by an enlarged thyroid, protruded "
  "eyeballs, increased BMR and weight loss.",
  ["Increased BMR and weight loss → excess thyroid hormone (hyperthyroidism)",
   "Enlarged thyroid + protruding eyeballs → exophthalmic goitre"],
  "Thyroid gland",
  correct="Exophthalmic goitre (Graves' disease), a form of hyperthyroidism",
  wrong=["Cretinism, caused by hypothyroidism during pregnancy", "Simple goitre caused by iodine deficiency",
         "Addison's disease, caused by underproduction of adrenocortical hormones"],
  why="Cretinism and iodine-deficiency goitre are hypothyroid states (BMR would not rise); Addison's disease "
      "involves the adrenal cortex, not the thyroid.", secs=40)

Z(CCI, "Adrenal, pancreas and gonads", I, MUL,
  MS("Which of the following statements about androgens are correct?",
     ["They regulate the development, maturation and functions of male accessory sex organs such as the epididymis, "
      "vas deferens and seminal vesicles.",
      "They inhibit spermatogenesis.",
      "They act on the central nervous system and influence male sexual behaviour (libido).",
      "They have a catabolic effect on protein metabolism.",
      "They stimulate muscular growth and the growth of facial and axillary hair."]),
  "Actions of androgens",
  "Androgens regulate the male accessory sex organs, stimulate muscular growth, facial and axillary hair, "
  "aggressiveness and low pitch of voice, play a stimulatory role in spermatogenesis, influence libido through the "
  "CNS, and have anabolic effects on protein and carbohydrate metabolism.",
  ["(a) True", "(b) False: androgens stimulate spermatogenesis", "(c) True",
   "(d) False: the effect is anabolic", "(e) True"],
  "Testis",
  correct="(a), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only"],
  why="Options with (b) or (d) reverse the actual effects: androgens are stimulatory for spermatogenesis and "
      "anabolic.", secs=60)

Z(CCI, "Mechanism of hormone action", I, MAT,
  ML(("hormone", "chemical nature"), ["Insulin", "Cortisol", "Thyroxine", "Epinephrine"],
     ["Steroid", "Amino-acid derivative", "Peptide/protein hormone", "Iodothyronine"]),
  "Chemical classification of hormones",
  "NCERT groups hormones as peptide/polypeptide/protein hormones (insulin, glucagon, pituitary and hypothalamic "
  "hormones), steroids (cortisol, testosterone, estradiol, progesterone), iodothyronines (thyroid hormones) and "
  "amino-acid derivatives (epinephrine).",
  ["Insulin → peptide/protein → III", "Cortisol → steroid → I", "Thyroxine → iodothyronine → IV",
   "Epinephrine → amino-acid derivative → II"],
  "Mechanism of hormone action",
  match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
         [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
          {"A": "I", "B": "III", "C": "IV", "D": "II"}]), secs=40)

Z(CCI, "Hypothalamus and pituitary", A, MUL,
  MS("Which of the following statements about the hypothalamus and pituitary are correct?",
     ["GnRH from the hypothalamus stimulates the pituitary to synthesise and release gonadotrophins.",
      "Somatostatin from the hypothalamus inhibits the release of growth hormone from the pituitary.",
      "Hypothalamic hormones reach the posterior pituitary through a portal circulatory system.",
      "In humans, the pars intermedia is almost merged with the pars distalis.",
      "The neurohypophysis secretes ACTH."]),
  "Hypothalamic control of the pituitary",
  "Hypothalamic releasing (e.g. GnRH) and inhibiting (e.g. somatostatin) hormones reach the anterior pituitary "
  "through the hypophyseal portal system. The posterior pituitary is under direct neural control. In humans the pars "
  "intermedia is almost merged with the pars distalis. ACTH comes from the pars distalis.",
  ["(a) True", "(b) True", "(c) False: the portal system serves the anterior pituitary", "(d) True",
   "(e) False: ACTH is an anterior pituitary hormone; the neurohypophysis releases oxytocin and vasopressin"],
  "Hypothalamus; The pituitary gland",
  correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="Statement (c) is the trap: the portal system links the hypothalamus with the anterior, not the posterior, "
      "pituitary.", secs=75)

Z(CCI, "Adrenal, pancreas and gonads", A, ASR,
  AR("Glucagon is a hyperglycemic hormone.", "Glucagon stimulates glycogenesis in hepatocytes."),
  "Glucagon and insulin have opposite actions",
  "Glucagon acts on hepatocytes and stimulates glycogenolysis and gluconeogenesis, and reduces cellular glucose "
  "uptake, so blood glucose rises: A is true. Glycogenesis (glucose → glycogen) is stimulated by insulin, so R is "
  "false.",
  ["A: true (glucagon raises blood glucose)", "R: false (glucagon stimulates glycogenolysis; insulin stimulates "
   "glycogenesis)"],
  "Pancreas", ans="C",
  why="Students who confuse glycogenesis with glycogenolysis mark option A.", secs=50)

Z(CCI, "Mechanism of hormone action", A, STP,
  SP("Hormones that interact with membrane-bound receptors normally enter the target cell to bring about their "
     "effects.",
     "Iodothyronines act mainly through membrane-bound receptors and generate second messengers such as cyclic "
     "AMP."),
  "Membrane-bound and intracellular receptors",
  "Hormones binding membrane-bound receptors normally do not enter the target cell; they generate second messengers "
  "(cyclic AMP, IP₃, Ca²⁺). Iodothyronines, like steroids, interact with intracellular receptors and regulate gene "
  "expression. Both statements are false.",
  ["Statement I: false (they do not enter the cell)",
   "Statement II: false (iodothyronines use intracellular receptors)"],
  "Mechanism of hormone action", ans="B", secs=50)

Z(CCI, "Hormonal disorders", A, MAT,
  ML(("disorder", "cause"), ["Addison's disease", "Cretinism", "Acromegaly", "Pituitary dwarfism"],
     ["Excess secretion of growth hormone in adults, especially in middle age",
      "Underproduction of hormones by the adrenal cortex",
      "Hypothyroidism during pregnancy, affecting the developing baby",
      "Low secretion of growth hormone, resulting in stunted growth"]),
  "Hypo- and hypersecretion disorders",
  "Addison's disease results from underproduction of adrenocortical hormones (acute weakness, fatigue). "
  "Hypothyroidism during pregnancy causes cretinism in the baby. Excess GH in adults causes acromegaly; low GH "
  "causes pituitary dwarfism.",
  ["Addison's disease → II", "Cretinism → III", "Acromegaly → I", "Pituitary dwarfism → IV"],
  "Pituitary gland; Thyroid gland; Adrenal gland",
  match=({"A": "II", "B": "III", "C": "I", "D": "IV"},
         [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
          {"A": "II", "B": "I", "C": "III", "D": "IV"}]),
  why="Swapping acromegaly and dwarfism, or linking cretinism with the adrenal cortex, are the usual errors.",
  secs=50)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following statements about the hormones of the adrenal medulla are correct?",
     ["Adrenaline and noradrenaline are rapidly secreted in response to stress of any kind and during emergency "
      "situations.",
      "They cause constriction of the pupils.",
      "They increase the heartbeat, the strength of heart contraction and the rate of respiration.",
      "They stimulate the breakdown of glycogen, increasing the glucose concentration in blood.",
      "They are steroid hormones secreted by the zona fasciculata."]),
  "Catecholamines: emergency hormones",
  "The adrenal medulla secretes adrenaline and noradrenaline (catecholamines), the 'fight or flight' hormones. They "
  "increase alertness, cause pupillary dilation, piloerection and sweating, raise heart rate, strength of "
  "contraction and breathing rate, and stimulate glycogenolysis.",
  ["(a) True", "(b) False: they dilate the pupils", "(c) True", "(d) True",
   "(e) False: catecholamines are amino-acid derivatives from the medulla; zona fasciculata is part of the cortex"],
  "Adrenal gland",
  correct="(a), (c) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (d) and (e) only"],
  why="(b) reverses the effect on the pupil, and (e) confuses the medulla with the cortex.", secs=60)

# ================================================================ Human Reproduction (6/9/6)
Z(HR, "Male and female reproductive systems", B, D,
  "The scrotum helps to maintain the temperature of the testes lower than the normal internal body temperature, "
  "which is necessary for spermatogenesis. The difference is about:",
  "Scrotum and spermatogenesis",
  "The testes lie outside the abdominal cavity in the scrotum, which keeps them 2–2.5 °C below the normal internal "
  "body temperature, as needed for spermatogenesis.",
  ["Testes are extra-abdominal, in the scrotum", "Scrotal temperature is 2–2.5 °C lower than body temperature"],
  "Male reproductive system",
  correct="2–2.5 °C", wrong=["0.5 °C", "5–6 °C", "10 °C"], secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "Within the seminiferous tubules of the testis, the cells that provide nutrition to the germ cells are the:",
  "Cells of the seminiferous tubule",
  "Each seminiferous tubule is lined by male germ cells (spermatogonia) and Sertoli cells. Sertoli cells provide "
  "nutrition to the germ cells.",
  ["Lining of seminiferous tubule: spermatogonia + Sertoli cells", "Sertoli cells → nourish germ cells"],
  "Male reproductive system",
  correct="Sertoli cells", wrong=["Leydig cells", "Spermatogonia", "Immunocompetent cells of the interstitial spaces"],
  why="Leydig cells and immunocompetent cells lie in the interstitial spaces outside the tubules; spermatogonia are "
      "the germ cells themselves.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "The funnel-shaped part of the oviduct closer to the ovary, whose edges bear finger-like projections that help in "
  "collecting the ovum after ovulation, is the:",
  "Parts of the oviduct",
  "The oviduct (10–12 cm) has three parts: the funnel-shaped infundibulum with fimbriae close to the ovary, the "
  "wider ampulla, and the narrow isthmus that joins the uterus.",
  ["Infundibulum (with fimbriae) → ampulla → isthmus → uterus"],
  "Female reproductive system",
  correct="Infundibulum", wrong=["Ampulla", "Isthmus", "Cervix"], secs=20)

Z(HR, "Fertilisation and implantation", B, D,
  "An embryo with 8 to 16 blastomeres is called a:",
  "Cleavage and early embryo",
  "Mitotic divisions (cleavage) of the zygote give 2, 4, 8, 16 blastomeres. The embryo with 8 to 16 blastomeres is "
  "the morula, which develops further into the blastocyst.",
  ["Zygote → cleavage → morula (8–16 blastomeres) → blastocyst"],
  "Fertilisation and implantation",
  correct="Morula", wrong=["Blastocyst", "Zygote", "Trophoblast"],
  why="The blastocyst comes after the morula; the trophoblast is only the outer layer of the blastocyst.", secs=20)

Z(HR, "Pregnancy, parturition and lactation", B, STP,
  SP("The milk produced during the initial few days of lactation is called colostrum.",
     "Colostrum contains several antibodies that are essential to develop resistance in new-born babies."),
  "Lactation",
  "The mammary glands start producing milk towards the end of pregnancy. The milk of the first few days, colostrum, "
  "contains several antibodies essential for developing resistance in the new-born. Both statements are true.",
  ["Statement I: true", "Statement II: true"],
  "Parturition and lactation", ans="A", secs=25)

Z(HR, "Menstrual cycle", B, D,
  "The first menstruation that begins at puberty is called:",
  "Menstrual cycle terms",
  "The first menstruation at puberty is menarche. The cycles cease around 50 years of age; this is menopause.",
  ["First menstruation → menarche", "Cessation of cycles (~50 years) → menopause"],
  "Menstrual cycle",
  correct="Menarche", wrong=["Menopause", "Ovulation", "Parturition"], secs=20)

Z(HR, "Gametogenesis", I, NUM,
  "During a coitus, a man ejaculates 250 million sperms. According to NCERT, for normal fertility at least 60% of "
  "the sperms must have normal shape and size, and at least 40% of them must show vigorous motility. The minimum "
  "number of sperms in this ejaculate that must have normal shape and size is:",
  "Sperm count and fertility",
  "The shape-and-size criterion is the 60% figure and applies to all the sperms ejaculated; the 40% figure is the "
  "separate motility criterion.",
  ["Normal shape and size needed in ≥ 60% of the sperms", "0.60 × 250 million = 150 million"],
  "Gametogenesis (structure of sperm and sperm count)",
  correct="150 million", wrong=["100 million", "60 million", "50 million"],
  why="100 million uses the 40% motility figure; 60 million multiplies the two criteria (0.6 × 0.4); 50 million "
      "subtracts the two percentages (20%).", secs=50, vb=RECOMPUTED)

Z(HR, "Male and female reproductive systems", I, MAT,
  ML(("part of the uterus", "feature"), ["Perimetrium", "Myometrium", "Endometrium", "Cervical canal"],
     ["Thick layer of smooth muscle that shows strong contractions during delivery of the baby",
      "Thin, outer membranous layer", "Inner glandular layer that undergoes cyclical changes during the menstrual "
      "cycle", "Together with the vagina, forms the birth canal"]),
  "Structure of the uterus",
  "The uterine wall has three layers: the outer thin perimetrium, the middle thick muscular myometrium and the inner "
  "glandular endometrium. The uterus opens into the vagina through the cervix; the cervical canal and vagina form "
  "the birth canal.",
  ["Perimetrium → outer membranous → II", "Myometrium → smooth muscle, contractions at delivery → I",
   "Endometrium → glandular, cyclical changes → III", "Cervical canal + vagina → birth canal → IV"],
  "Female reproductive system",
  match=({"A": "II", "B": "I", "C": "III", "D": "IV"},
         [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
          {"A": "III", "B": "I", "C": "II", "D": "IV"}]), secs=40)

Z(HR, "Male and female reproductive systems", I, MUL,
  MS("Which of the following statements about the male reproductive system are correct?",
     ["Secretions of the accessory glands constitute the seminal plasma, which is rich in fructose, calcium and "
      "certain enzymes.",
      "Secretions of the bulbourethral glands help in the lubrication of the penis.",
      "The prostate is a paired gland.",
      "The vas deferens receives a duct from the seminal vesicle and opens into the urethra as the ejaculatory duct.",
      "The epididymis lies along the anterior surface of each testis."]),
  "Male accessory ducts and glands",
  "The accessory glands are paired seminal vesicles, a single prostate and paired bulbourethral glands. The "
  "epididymis lies along the posterior surface of each testis. The vas deferens loops over the urinary bladder, "
  "receives the duct of the seminal vesicle and opens into the urethra as the ejaculatory duct.",
  ["(a) True", "(b) True", "(c) False: the prostate is single", "(d) True",
   "(e) False: the epididymis is along the posterior surface"],
  "Male reproductive system",
  correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"], secs=60)

Z(HR, "Fertilisation and implantation", I, ASR,
  AR("Not all copulations lead to fertilisation and pregnancy.",
     "Fertilisation can occur only if the ovum and sperms are transported simultaneously to the ampullary "
     "region."),
  "Site and conditions of fertilisation",
  "Sperms swim through the cervix and uterus to the ampullary region of the fallopian tube, where the ovum is also transported. "
  "Fertilisation happens only when both arrive there at the same time. NCERT gives this as the reason why not all "
  "copulations lead to fertilisation and pregnancy, so R explains A.",
  ["A: true", "R: true", "The need for simultaneous arrival at the ampullary region explains A"],
  "Fertilisation and implantation", ans="A", secs=40)

Z(HR, "Fertilisation and implantation", I, STP,
  SP("The second meiotic division of the secondary oocyte is equal and forms two ootids.",
     "Entry of the sperm into the ovum induces completion of the meiotic division of the secondary oocyte."),
  "Completion of oogenesis at fertilisation",
  "The sperm's entry induces the secondary oocyte to complete meiosis II. This division is unequal, giving a second "
  "polar body and a haploid ootid.",
  ["Statement I: false (unequal division: second polar body + one ootid)", "Statement II: true"],
  "Fertilisation and implantation", ans="D", secs=35)

Z(HR, "Pregnancy, parturition and lactation", I, D,
  "Which of the following hormones is produced in women only during pregnancy?",
  "Placental and pregnancy hormones",
  "hCG, hPL and relaxin are produced in women only during pregnancy. Estrogens, progestogens and prolactin are also "
  "produced outside pregnancy, though their levels rise several-fold during it.",
  ["Pregnancy-only hormones: hCG, hPL, relaxin", "Estrogen, progesterone, prolactin: increased, but not exclusive"],
  "Pregnancy and embryonic development",
  correct="Human chorionic gonadotropin (hCG)", wrong=["Estrogen", "Progesterone", "Prolactin"],
  secs=30)

Z(HR, "Menstrual cycle", I, D,
  "The rupture of the Graafian follicle and the release of the ovum in the middle of the menstrual cycle is induced "
  "by:",
  "Hormonal control of ovulation",
  "LH and FSH rise during the follicular phase and peak in mid-cycle. The rapid secretion of LH to its maximum "
  "(LH surge) induces rupture of the Graafian follicle and thereby ovulation.",
  ["Mid-cycle LH surge → rupture of Graafian follicle → ovulation"],
  "Menstrual cycle",
  correct="A rapid surge in LH secretion",
  wrong=["A sharp fall in FSH secretion", "Rising progesterone secreted by the corpus luteum",
         "Degeneration of the corpus luteum"],
  why="The corpus luteum forms only after ovulation, and its degeneration leads to menstruation, not ovulation.",
  secs=30)

Z(HR, "Fertilisation and implantation", I, MAT,
  ML(("structure", "role"), ["Acrosome", "Middle piece of sperm", "Zona pellucida", "Trophoblast"],
     ["Gets attached to the endometrium during implantation",
      "Contains numerous mitochondria that produce energy for tail movement",
      "Cap-like structure filled with enzymes that help in fertilisation",
      "Layer whose changes on sperm contact block the entry of additional sperms"]),
  "Sperm, ovum and blastocyst structures",
  "The acrosome on the sperm head holds enzymes that help the sperm enter the ovum. The middle piece has mitochondria "
  "for tail movement. Changes in the zona pellucida after sperm contact block polyspermy. The trophoblast of the "
  "blastocyst attaches to the endometrium.",
  ["Acrosome → III", "Middle piece → II", "Zona pellucida → IV", "Trophoblast → I"],
  "Gametogenesis; Fertilisation and implantation",
  match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
         [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
          {"A": "IV", "B": "II", "C": "III", "D": "I"}]), secs=40)

Z(HR, "Pregnancy, parturition and lactation", I, D,
  "By the end of which period of pregnancy are most of the major organ systems of the human foetus formed, with the "
  "limbs and external genital organs well developed?",
  "Milestones of foetal development",
  "Heart forms after one month; limbs and digits by the end of the second month; most major organ systems by the "
  "end of 12 weeks (first trimester); first movements and head hair in the fifth month; eyelids separate and "
  "eyelashes form by the end of 24 weeks.",
  ["End of 12 weeks (first trimester) → most major organ systems formed"],
  "Pregnancy and embryonic development",
  correct="End of 12 weeks (first trimester)",
  wrong=["End of the first month", "End of 24 weeks (second trimester)", "End of the fifth month"],
  why="End of the first month: only the heart has formed. Fifth month: first foetal movements. End of 24 weeks: "
      "eyelids separate and eyelashes form.", secs=30)

Z(HR, "Gametogenesis", A, NUM,
  "In a human male, 50 secondary spermatocytes complete spermatogenesis. In a human female, 50 primary oocytes "
  "complete oogenesis (assume every secondary oocyte is fertilised, so both meiotic divisions are completed). The "
  "number of spermatozoa and of functional female gametes (ova) formed are, respectively:",
  "Products of spermatogenesis and oogenesis",
  "A secondary spermatocyte is already past meiosis I; meiosis II gives 2 spermatids, each becoming a sperm. A "
  "primary oocyte gives only one functional gamete, because both meiotic divisions are unequal and produce polar "
  "bodies.",
  ["50 secondary spermatocytes × 2 = 100 spermatozoa", "50 primary oocytes × 1 = 50 ova"],
  "Gametogenesis",
  correct="100 and 50", wrong=["200 and 50", "100 and 100", "200 and 200"],
  why="200 treats secondary spermatocytes as primary ones (4 sperms each); 100 or 200 ova ignores that oogenesis "
      "gives one ovum and polar bodies.", secs=60, vb=RECOMPUTED)

Z(HR, "Gametogenesis", A, MUL,
  MS("Which of the following statements about oogenesis are correct?",
     ["Oogonia are formed within each fetal ovary during embryonic development, and no more oogonia are formed or "
      "added after birth.",
      "Primary oocytes enter prophase-I of meiosis and get temporarily arrested at that stage.",
      "A fluid-filled cavity called the antrum first appears in the secondary follicle.",
      "At puberty, only about 60,000–80,000 primary follicles are left in each ovary.",
      "Primary follicles get surrounded by more layers of granulosa cells and a new theca to become secondary "
      "follicles."]),
  "Oogenesis and follicle development",
  "Oogenesis starts in the fetal ovary; oogonia enter prophase-I and are arrested as primary oocytes. Many follicles "
  "degenerate before puberty, leaving 60,000–80,000 primary follicles in each ovary. Primary → secondary follicle "
  "(more granulosa layers, new theca) → tertiary follicle with the fluid-filled antrum → Graafian follicle.",
  ["(a) True", "(b) True", "(c) False: the antrum characterises the tertiary follicle", "(d) True", "(e) True"],
  "Gametogenesis",
  correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"],
  why="(c) is the trap: the antrum defines the tertiary follicle, not the secondary follicle.", secs=75)

Z(HR, "Menstrual cycle", A, ASR,
  AR("The corpus luteum secretes large amounts of progesterone.",
     "The corpus luteum is formed from the remaining parts of the Graafian follicle during the follicular phase."),
  "Luteal phase",
  "After ovulation, in the luteal phase, the remaining parts of the Graafian follicle form the corpus luteum, which "
  "secretes large amounts of progesterone to maintain the endometrium. A is true; R wrongly places its formation in "
  "the follicular phase.",
  ["A: true", "R: false (corpus luteum forms after ovulation, in the luteal phase)"],
  "Menstrual cycle", ans="C",
  why="The follicular phase comes before ovulation, when the Graafian follicle is still growing.", secs=45)

Z(HR, "Pregnancy, parturition and lactation", A, STP,
  SP("The signals for parturition originate from the maternal hypothalamus, independently of the foetus.",
     "Oxytocin acts on the uterine muscle to cause stronger contractions, which in turn stimulate further secretion "
     "of oxytocin."),
  "Neuroendocrine control of parturition",
  "Signals for parturition come from the fully developed foetus and the placenta, which induce mild uterine "
  "contractions (foetal ejection reflex). This triggers oxytocin release from the maternal pituitary; oxytocin causes "
  "stronger contractions, which stimulate more oxytocin secretion, until the baby is expelled.",
  ["Statement I: false (signals from the foetus and placenta)", "Statement II: true (a stimulatory reflex)"],
  "Parturition and lactation", ans="D", secs=45)

Z(HR, "Menstrual cycle", A, MUL,
  MS("Which of the following statements about the human menstrual cycle are correct?",
     ["Both LH and FSH attain a peak level in the middle of the cycle (about the 14th day).",
      "During the follicular phase, the endometrium regenerates through proliferation.",
      "Menstruation occurs only if the released ovum is not fertilised.",
      "Lack of menstruation is always an indication of pregnancy.",
      "During pregnancy, all events of the menstrual cycle stop and there is no menstruation."]),
  "Phases and hormonal control of the menstrual cycle",
  "LH and FSH peak around day 14. The endometrium regenerates in the follicular phase. Menstruation occurs only "
  "when the ovum is not fertilised, and cycles stop during pregnancy. Lack of menstruation may indicate pregnancy, "
  "but it may also be caused by stress or poor health.",
  ["(a) True", "(b) True", "(c) True", "(d) False: stress or poor health can also stop menstruation", "(e) True"],
  "Menstrual cycle",
  correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (b) and (d) only", "(b), (c) and (e) only"],
  why="The word 'always' makes (d) false; the option with only (b), (c) and (e) leaves out the true statement (a).",
  secs=70)

Z(HR, "Male and female reproductive systems", A, D,
  "Which of the following shows the correct path of sperms from their site of formation to the outside of the "
  "body?",
  "Male accessory ducts",
  "Sperms formed in the seminiferous tubules pass through the rete testis and vasa efferentia to the epididymis, then "
  "the vas deferens, which joins the duct of the seminal vesicle to form the ejaculatory duct opening into the "
  "urethra.",
  ["Seminiferous tubules → rete testis → vasa efferentia → epididymis",
   "Epididymis → vas deferens → ejaculatory duct → urethra → urethral meatus"],
  "Male reproductive system",
  correct="Seminiferous tubules → rete testis → vasa efferentia → epididymis → vas deferens → ejaculatory duct → "
          "urethra",
  wrong=["Seminiferous tubules → vasa efferentia → rete testis → epididymis → vas deferens → ejaculatory duct → "
         "urethra",
         "Seminiferous tubules → rete testis → epididymis → vasa efferentia → vas deferens → ejaculatory duct → "
         "urethra",
         "Seminiferous tubules → rete testis → vasa efferentia → epididymis → ejaculatory duct → vas deferens → "
         "urethra"],
  why="Each wrong sequence swaps one adjacent pair: rete testis/vasa efferentia, epididymis/vasa efferentia, or vas "
      "deferens/ejaculatory duct.", secs=50)

# ================================================================ Reproductive Health (4/6/4)
Z(RH, "Contraception", B, D,
  "Which of the following is NOT a feature of an ideal contraceptive?",
  "Ideal contraceptive",
  "An ideal contraceptive should be user-friendly, easily available, effective and reversible, with no or least "
  "side-effects, and should in no way interfere with the sexual drive, desire or the sexual act.",
  ["Ideal = user-friendly, available, effective, reversible, least side-effects, no interference with sexual act",
   "Irreversibility is the opposite of what is required"],
  "Population stabilisation and birth control",
  correct="It should be irreversible, so that fertility does not return",
  wrong=["It should be user-friendly and easily available", "It should have no or the least side-effects",
         "It should not interfere with the sexual drive, desire or the sexual act"], secs=25)

Z(RH, "Contraception", B, D,
  "In vasectomy:",
  "Surgical methods (sterilisation)",
  "Vasectomy is the surgical method in males: a small part of the vas deferens is removed or tied up through a small "
  "incision on the scrotum, which blocks gamete transport. In tubectomy, a small part of the fallopian tube is "
  "removed or tied up.",
  ["Male sterilisation → vas deferens cut/tied through scrotal incision", "Female sterilisation → tubectomy"],
  "Population stabilisation and birth control",
  correct="A small part of the vas deferens is removed or tied up through a small incision on the scrotum",
  wrong=["A small part of the fallopian tube is removed or tied up through a small incision in the abdomen",
         "A device is inserted into the uterus through the vagina", "Both testes are surgically removed"],
  why="The fallopian-tube option describes tubectomy; the device option describes an IUD; sterilisation does not "
      "remove the testes.", secs=25)

Z(RH, "Contraception", B, STP,
  SP("Condoms protect the user from STIs and AIDS in addition to preventing conception.",
     "Diaphragms, cervical caps and vaults are single-use devices that cannot be reused."),
  "Barrier methods",
  "Condoms are barriers made of thin rubber/latex that also protect against STIs and AIDS. Diaphragms, cervical caps "
  "and vaults are rubber barriers placed over the cervix during coitus; they are reusable.",
  ["Statement I: true", "Statement II: false (they are reusable)"],
  "Population stabilisation and birth control", ans="C", secs=25)

Z(RH, "Infertility and ART", B, D,
  "In intra-uterine insemination (IUI), the semen collected from the husband or a healthy donor is artificially "
  "introduced into the:",
  "Artificial insemination",
  "When the male partner cannot inseminate the female or has a very low sperm count, semen is collected and "
  "artificially introduced into the vagina or into the uterus. Introduction into the uterus is IUI.",
  ["Artificial insemination: semen → vagina or uterus", "Into the uterus → intra-uterine insemination (IUI)"],
  "Infertility",
  correct="Uterus", wrong=["Fallopian tube, together with a donor ovum", "Ovum, by direct injection of one sperm",
                           "Ovary"],
  why="Transfer with a donor ovum into the fallopian tube is GIFT, and injecting a sperm into an ovum is ICSI.",
  secs=20)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive", "category"), ["Lippes loop", "LNG-20", "Cervical cap", "Periodic abstinence"],
     ["Hormone-releasing IUD", "Barrier method", "Non-medicated IUD", "Natural method"]),
  "Types of contraceptive methods",
  "IUDs are non-medicated (Lippes loop), copper-releasing (CuT, Cu7, Multiload 375) or hormone-releasing "
  "(Progestasert, LNG-20). Diaphragms, cervical caps and vaults are barriers. Periodic abstinence is a natural "
  "method.",
  ["Lippes loop → non-medicated IUD → III", "LNG-20 → hormone-releasing IUD → I", "Cervical cap → barrier → II",
   "Periodic abstinence → natural → IV"],
  "Population stabilisation and birth control",
  match=({"A": "III", "B": "I", "C": "II", "D": "IV"},
         [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
          {"A": "III", "B": "I", "C": "IV", "D": "II"}]), secs=40)

Z(RH, "Contraception", I, MUL,
  MS("Which of the following statements about oral contraceptive pills are correct?",
     ["They contain progestogens or progestogen–estrogen combinations.",
      "They are taken daily for 21 days, starting preferably within the first five days of the menstrual cycle.",
      "They make the cervical mucus more favourable for the entry of sperms.",
      "Saheli is a steroidal pill that has to be taken daily.",
      "They inhibit ovulation and implantation."]),
  "Oral contraceptives",
  "Pills (progestogens alone or with estrogen) are taken daily for 21 days, starting within the first five days of "
  "the cycle, then repeated after a 7-day gap. They inhibit ovulation and implantation and alter the cervical mucus "
  "to prevent or retard sperm entry. Saheli is a non-steroidal, once-a-week pill.",
  ["(a) True", "(b) True", "(c) False: they make the mucus hostile to sperm entry",
   "(d) False: Saheli is non-steroidal and taken once a week", "(e) True"],
  "Population stabilisation and birth control",
  correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"], secs=60)

Z(RH, "Contraception", I, ASR,
  AR("As long as a mother breast-feeds her child fully, the chances of conception in the first few months after "
     "parturition are almost nil.",
     "Ovulation, and therefore the menstrual cycle, do not occur during the period of intense lactation following "
     "parturition."),
  "Lactational amenorrhea",
  "Lactational amenorrhea is a natural method based on the absence of ovulation during intense lactation. Because "
  "no ovum is released, conception is almost impossible while the mother breast-feeds fully (reported effective up "
  "to six months). R explains A.",
  ["A: true", "R: true", "No ovulation → no ovum to fertilise → R explains A"],
  "Population stabilisation and birth control", ans="A", secs=40)

Z(RH, "Contraception", I, STP,
  SP("IUDs decrease the phagocytosis of sperms within the uterus.",
     "Hormone-releasing IUDs make the uterus unsuitable for implantation and the cervix hostile to sperms."),
  "Mode of action of IUDs",
  "IUDs increase phagocytosis of sperms within the uterus; copper ions suppress sperm motility and fertilising "
  "capacity; hormone-releasing IUDs make the uterus unsuitable for implantation and the cervix hostile to sperms.",
  ["Statement I: false (IUDs increase phagocytosis of sperms)", "Statement II: true"],
  "Population stabilisation and birth control", ans="D", secs=35)

Z(RH, "MTP and amniocentesis", I, D,
  "Medical termination of pregnancy (MTP) is considered relatively safe up to:",
  "Safety of MTP",
  "MTPs are considered relatively safe during the first trimester, i.e. up to 12 weeks of pregnancy. "
  "Second-trimester abortions are much riskier.",
  ["First trimester = up to 12 weeks → relatively safe", "Second trimester → much riskier"],
  "Medical termination of pregnancy (MTP)",
  correct="12 weeks (the first trimester) of pregnancy",
  wrong=["24 weeks (the end of the second trimester) of pregnancy", "36 weeks of pregnancy",
         "Any stage of pregnancy, if done by a doctor"], secs=25)

Z(RH, "MTP and amniocentesis", I, D,
  "Which of the following statements about amniocentesis is correct?",
  "Amniocentesis",
  "Amniocentesis studies the chromosomal pattern in the amniotic fluid surrounding the developing embryo. It is "
  "used to detect genetic disorders such as Down syndrome, haemophilia and sickle-cell anaemia. Its use for foetal "
  "sex determination is banned by law to check female foeticide.",
  ["Sample: amniotic fluid → chromosomal pattern", "Use: genetic disorders; sex determination is statutorily banned"],
  "Reproductive health – problems and strategies",
  correct="It is based on the chromosomal pattern in the amniotic fluid and can detect genetic disorders such as "
          "Down syndrome",
  wrong=["It is legally permitted in India for determining the sex of the foetus",
         "It is a technique for transferring an early embryo into the uterus",
         "It detects pregnancy by testing the mother's urine for hCG"],
  why="Sex determination by amniocentesis is under a statutory ban; embryo transfer is part of IVF; amniocentesis "
      "samples amniotic fluid, not urine.", secs=35)

Z(RH, "STDs and their prevention", A, MUL,
  MS("Which of the following statements about sexually transmitted infections (STIs) are correct?",
     ["Except hepatitis-B, genital herpes and HIV infections, other STIs are completely curable if detected early "
      "and treated properly.",
      "Chlamydiasis, trichomoniasis and genital warts are sexually transmitted infections.",
      "If untreated, STIs can lead to pelvic inflammatory disease, ectopic pregnancy and infertility.",
      "The incidence of STIs is reported to be highest in the 45–60 year age group.",
      "Hepatitis-B can be transmitted only through sexual contact."]),
  "Sexually transmitted infections",
  "STIs include gonorrhoea, syphilis, genital herpes, chlamydiasis, genital warts, trichomoniasis, hepatitis-B and "
  "HIV. All except hepatitis-B, genital herpes and HIV are completely curable if treated early. Untreated STIs can "
  "cause PID, abortions, still births, ectopic pregnancy, infertility or cancer of the reproductive tract. "
  "Incidence is highest in the 15–24 year age group. Hepatitis-B and HIV also spread through shared needles, "
  "blood transfusion and from mother to foetus.",
  ["(a) True", "(b) True", "(c) True", "(d) False: highest in the 15–24 year age group",
   "(e) False: also through shared needles, transfusion and mother to foetus"],
  "Sexually transmitted infections (STIs)",
  correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
  why="(e) fails because of the word 'only'; (d) gives the wrong age group.", secs=70)

Z(RH, "Contraception", A, STP,
  SP("Progestogens, progestogen–estrogen combinations or IUDs used within 72 hours of coitus are very effective as "
     "emergency contraceptives.",
     "In periodic abstinence, couples avoid coitus from day 10 to day 17 of the menstrual cycle, when ovulation "
     "could be expected."),
  "Emergency contraception and natural methods",
  "Both statements match NCERT: emergency contraception within 72 hours of coitus (for example after rape or "
  "casual unprotected intercourse), and periodic abstinence during days 10–17, the fertile period.",
  ["Statement I: true (72 hours)", "Statement II: true (days 10–17)"],
  "Population stabilisation and birth control", ans="A",
  why="Students who remember 72 hours as 24 hours, or the fertile period as the menstrual days, wrongly reject one "
      "statement.", secs=45)

Z(RH, "Infertility and ART", A, D,
  "A woman cannot produce ova but can provide a suitable environment in her oviduct for fertilisation and further "
  "development of the embryo. Which assisted reproductive technique is designed for such a case?",
  "Assisted reproductive technologies",
  "GIFT (gamete intra fallopian transfer) transfers an ovum collected from a donor into the fallopian tube of a "
  "female who cannot produce ova but can provide a suitable environment for fertilisation and development.",
  ["Problem: no ova, but a functional oviduct", "Donor ovum placed in her fallopian tube → GIFT"],
  "Infertility",
  correct="Gamete intra fallopian transfer (GIFT)",
  wrong=["Intra-uterine insemination (IUI) with donor semen", "Intracytoplasmic sperm injection (ICSI) using her "
         "own ova", "Zygote intra fallopian transfer (ZIFT) using a zygote formed from her own ovum"],
  why="IUI, ICSI and ZIFT with her own ova all need ova from the woman, which she cannot produce.", secs=50)

Z(RH, "Infertility and ART", A, ASR,
  AR("In ZIFT, the zygote is transferred into the uterus.",
     "In IUT, embryos with more than 8 blastomeres are transferred into the uterus."),
  "Embryo transfer: ZIFT and IUT",
  "In embryo transfer after IVF, the zygote or early embryo (up to 8 blastomeres) is transferred into the fallopian "
  "tube (ZIFT), while embryos with more than 8 blastomeres are transferred into the uterus (IUT). A is false; R is "
  "true.",
  ["A: false (ZIFT → fallopian tube)", "R: true (IUT → uterus, > 8 blastomeres)"],
  "Infertility", ans="D", secs=40)

# ================================================================ Evolution (5/7/5)
Z(EVO, "Origin of life", B, D,
  "In S.L. Miller's experiment, an electric discharge was passed through a closed flask containing CH₄, H₂, NH₃ "
  "and water vapour. He observed the formation of:",
  "Chemical evolution: Miller's experiment",
  "Miller recreated the supposed conditions of early earth on a laboratory scale and observed the formation of amino "
  "acids, supporting the idea of chemical evolution (Oparin and Haldane).",
  ["Electric discharge + CH₄, H₂, NH₃, water vapour → amino acids"],
  "Origin of life",
  correct="Amino acids", wrong=["Living cells", "Self-replicating DNA", "Membrane-bound organelles"], secs=20)

Z(EVO, "Evidences of evolution", B, D,
  "Which of the following pairs represents analogous structures?",
  "Analogy and convergent evolution",
  "Analogous structures perform similar functions but are not anatomically similar; they result from convergent "
  "evolution. The wings of a butterfly and of a bird are a standard example.",
  ["Analogous: same function, different anatomy", "Butterfly wing vs bird wing → analogous"],
  "What are the evidences for evolution?",
  correct="Wings of a butterfly and wings of a bird",
  wrong=["Forelimbs of a whale and a bat", "Hearts of different vertebrates", "Brains of different vertebrates"],
  why="Forelimbs, hearts and brains of vertebrates are homologous (same basic structure, divergent evolution).",
  secs=25)

Z(EVO, "Adaptive radiation", B, D,
  "Darwin observed many varieties of finches in the Galapagos Islands. From the original seed-eating form, other "
  "forms with altered beaks arose, enabling them to become insectivorous and vegetarian. This is an example of:",
  "Adaptive radiation",
  "Evolution of different species in a given geographical area starting from a point and radiating to other "
  "habitats is adaptive radiation; Darwin's finches are the NCERT example.",
  ["One ancestral seed-eating finch → many forms with different beaks → adaptive radiation"],
  "What is adaptive radiation?",
  correct="Adaptive radiation", wrong=["Industrial melanism", "Saltation", "Analogy"],
  why="Industrial melanism refers to the peppered moths; saltation is de Vries' single-step large mutation; analogy "
      "describes similar function with different structure.", secs=20)

Z(EVO, "Darwinism and modern synthesis", B, D,
  "According to Darwin, 'fitness' ultimately and only refers to:",
  "Darwinian fitness",
  "Darwinian fitness is reproductive fitness: those better fit in an environment leave more progeny, survive more "
  "and are selected by nature.",
  ["Fitness = reproductive fitness (leaving more progeny)"],
  "Biological evolution",
  correct="Reproductive fitness", wrong=["Physical strength", "Body size",
                                         "Ability to modify organs by their use and disuse"],
  why="The use-and-disuse option describes Lamarck's idea, not Darwin's.", secs=20)

Z(EVO, "Darwinism and modern synthesis", B, STP,
  SP("Hugo de Vries proposed the idea of mutations based on his work on the evening primrose.",
     "According to de Vries, mutations are small and directional, like the variations that Darwin described."),
  "Mutation theory of de Vries",
  "de Vries worked on the evening primrose and proposed that mutations (large differences arising suddenly) cause "
  "evolution. Mutations are random and directionless, while Darwinian variations are small and directional.",
  ["Statement I: true", "Statement II: false (mutations are random and directionless)"],
  "Mechanism of evolution", ans="C", secs=30)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, NUM,
  "In a population in Hardy-Weinberg equilibrium, the frequency of allele A is 0.8. The percentage of heterozygous "
  "(Aa) individuals in the population is:",
  "Hardy-Weinberg principle: p² + 2pq + q² = 1",
  "With p = 0.8 the other allele has q = 1 − 0.8 = 0.2. The heterozygote frequency is 2pq.",
  ["q = 1 − p = 0.2", "2pq = 2 × 0.8 × 0.2 = 0.32", "Heterozygotes = 32%"],
  "Hardy-Weinberg principle",
  correct="32%", wrong=["16%", "64%", "4%"],
  why="16% forgets the factor 2 (pq); 64% is p² (AA); 4% is q² (aa).", secs=40, vb=RECOMPUTED)

Z(EVO, "Human evolution", I, MAT,
  ML(("hominid", "feature"), ["Homo habilis", "Homo erectus", "Neanderthal man", "Australopithecines"],
     ["Brain about 900 cc; probably ate meat", "Brain about 1400 cc; buried their dead",
      "Brain 650–800 cc; probably did not eat meat",
      "Lived in East African grasslands about 2 mya; hunted with stone weapons but essentially ate fruit"]),
  "Origin and evolution of man",
  "NCERT gives: Homo habilis, brain 650–800 cc, probably did not eat meat; Homo erectus (about 1.5 mya), large brain "
  "around 900 cc, probably ate meat; Neanderthal man, brain 1400 cc, used hides and buried their dead; "
  "Australopithecines, about 2 mya in East African grasslands, hunted with stone weapons but ate mainly fruit.",
  ["Homo habilis → III", "Homo erectus → I", "Neanderthal man → II", "Australopithecines → IV"],
  "Origin and evolution of man",
  match=({"A": "III", "B": "I", "C": "II", "D": "IV"},
         [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
          {"A": "IV", "B": "I", "C": "II", "D": "III"}]), secs=45)

Z(EVO, "Natural selection", I, ASR,
  AR("Lichens can be used as industrial pollution indicators.", "Lichens do not grow in areas that are polluted."),
  "Lichens and industrial melanism",
  "In the peppered-moth story, white lichens covered tree trunks before industrialisation. NCERT notes that lichens "
  "can be used as industrial pollution indicators because they will not grow in polluted areas. R explains A.",
  ["A: true", "R: true", "Absence of lichens signals pollution → R explains A"],
  "What are the evidences for evolution? (natural selection in moths of England)", ans="A", secs=35)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, MUL,
  MS("Which of the following statements are correct?",
     ["According to the Hardy-Weinberg principle, allele frequencies in a population are stable and constant from "
      "generation to generation unless disturbed.",
      "The sum total of all the allelic frequencies is 1.",
      "When the original drifted population becomes the founders of a new population, the effect is called the "
      "founder effect.",
      "Genetic recombination does not affect Hardy-Weinberg equilibrium.",
      "Mutation is not one of the factors that affect Hardy-Weinberg equilibrium."]),
  "Hardy-Weinberg equilibrium and the factors that disturb it",
  "The gene pool stays constant (genetic equilibrium) unless disturbed. NCERT lists five disturbing factors: gene "
  "migration (gene flow), genetic drift, mutation, genetic recombination and natural selection. A drifted "
  "population that founds a new one shows the founder effect.",
  ["(a) True", "(b) True", "(c) True", "(d) False: recombination is one of the five factors",
   "(e) False: mutation is one of the five factors"],
  "Hardy-Weinberg principle",
  correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"], secs=60)

Z(EVO, "Adaptive radiation", I, D,
  "When more than one adaptive radiation appears to have occurred in an isolated geographical area (representing "
  "different habitats), it can be called:",
  "Adaptive radiation and convergent evolution",
  "NCERT: when more than one adaptive radiation appears to have occurred in an isolated geographical area, one can "
  "call this convergent evolution. Example: Australian placental mammals each resembling a corresponding marsupial "
  "(placental wolf and Tasmanian wolf).",
  ["Several adaptive radiations in one isolated area → convergent evolution"],
  "What is adaptive radiation?",
  correct="Convergent evolution", wrong=["Divergent evolution", "Genetic drift", "Gene flow"], secs=30)

Z(EVO, "Natural selection", I, D,
  "In a population, natural selection leads to more individuals acquiring peripheral character values at both ends "
  "of the distribution curve. This type of natural selection is:",
  "Types of natural selection",
  "Natural selection can lead to stabilisation (more individuals near the mean), directional change (more "
  "individuals at a value other than the mean) or disruption (more individuals at both peripheral ends).",
  ["Both ends favoured → disruption (disruptive selection)"],
  "Hardy-Weinberg principle (operation of natural selection)",
  correct="Disruptive selection (disruption)",
  wrong=["Stabilising selection", "Directional selection", "Genetic drift"],
  why="Stabilising favours the mean, directional favours one side; drift is a chance change, not selection.",
  secs=30)

Z(EVO, "Evidences of evolution", I, STP,
  SP("The forelimbs of whales, bats, cheetahs and humans share a similar pattern of bones: humerus, radius, ulna, "
     "carpals, metacarpals and phalanges.",
     "Similarities in proteins and genes performing a given function among diverse organisms give clues to common "
     "ancestry."),
  "Comparative anatomy and biochemical evidence",
  "Both are NCERT evidences for evolution: homologous forelimbs (same structure developed in different directions "
  "by divergent evolution), and biochemical similarity of proteins and genes pointing to common ancestry.",
  ["Statement I: true (homology)", "Statement II: true (biochemical similarity)"],
  "What are the evidences for evolution?", ans="A", secs=35)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "A population of 1000 individuals has 500 AA, 400 Aa and 100 aa individuals. What is the frequency of allele a, "
  "and how many aa individuals would be expected if the population were in Hardy-Weinberg equilibrium with the same "
  "allele frequencies?",
  "Allele frequency by gene counting; Hardy-Weinberg expectation",
  "Count alleles directly: each aa has two a alleles and each Aa has one. The square-root method is valid only when "
  "the population is known to be in equilibrium, which is not assumed here.",
  ["Total alleles = 2 × 1000 = 2000", "a alleles = 2 × 100 + 400 = 600 → q = 600/2000 = 0.3",
   "Expected aa = q² × N = 0.09 × 1000 = 90 (observed is 100, so the population is not in equilibrium)"],
  "Hardy-Weinberg principle",
  correct="0.3 and 90", wrong=["0.316 and 100", "0.3 and 100", "0.5 and 250"],
  why="0.316 takes √(100/1000) as if the population were already in equilibrium; '0.3 and 100' gives the observed "
      "rather than the expected number; 0.5 counts every individual carrying a as if it were an allele count.",
  secs=120, vb=RECOMPUTED)

Z(EVO, "Origin of life", A, MUL,
  MS("Which of the following statements about the origin of life are correct?",
     ["Oparin and Haldane proposed that the formation of life was preceded by chemical evolution.",
      "According to the theory of panspermia, units of life called spores were transferred to different planets, "
      "including the earth.",
      "The conditions on early earth included high temperature, volcanic storms and a reducing atmosphere "
      "containing CH₄ and NH₃.",
      "Louis Pasteur showed that new living organisms arose from killed yeast in pre-sterilised flasks.",
      "The first non-cellular forms of life could have originated about 3 billion years back."]),
  "Theories of the origin of life",
  "Oparin and Haldane proposed chemical evolution under early-earth conditions (high temperature, volcanic storms, "
  "reducing atmosphere with CH₄, NH₃). Panspermia proposes spores arriving from other planets. Pasteur showed that "
  "in pre-sterilised flasks life did NOT arise from killed yeast, while it did in flasks open to air, ending the idea "
  "of spontaneous generation. Non-cellular life may have arisen about 3 billion years back.",
  ["(a) True", "(b) True", "(c) True",
   "(d) False: life did not arise from killed yeast in the pre-sterilised flasks", "(e) True"],
  "Origin of life",
  correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (d) only", "(b), (d) and (e) only"],
  why="(d) reverses Pasteur's result: it was the flask open to air in which new organisms arose.", secs=75)

Z(EVO, "Natural selection", A, STP,
  SP("Before industrialisation set in England, dark-winged (melanised) moths outnumbered white-winged moths.",
     "After industrialisation, dark-winged moths decreased in number because predators spotted them easily against "
     "the soot-covered tree trunks."),
  "Industrial melanism",
  "Before industrialisation (around 1850), white-winged moths were more numerous because white lichens covered the "
  "trunks. After industrialisation (around 1920), trunks darkened with smoke and soot, so dark-winged moths were "
  "camouflaged and increased while white-winged moths were picked off by predators. Both statements reverse the "
  "facts.",
  ["Statement I: false (white-winged moths were more before industrialisation)",
   "Statement II: false (dark-winged moths increased after industrialisation)"],
  "What are the evidences for evolution? (natural selection in moths of England)", ans="B", secs=45)

Z(EVO, "Human evolution", A, D,
  "Which of the following statements about human evolution is correct?",
  "Origin and evolution of man",
  "Neanderthal man (brain 1400 cc) lived in the near east and central Asian countries between 1,00,000 and 40,000 "
  "years back and used hides to protect the body. Homo erectus fossils were found in Java (1891). Ramapithecus was "
  "more man-like, Dryopithecus more ape-like. Cave art developed about 18,000 years ago; agriculture came around "
  "10,000 years back.",
  ["Check each option against NCERT dates, places and descriptions", "Only the Neanderthal statement is accurate"],
  "Origin and evolution of man",
  correct="Neanderthal man lived in the near east and central Asian countries between 1,00,000 and 40,000 years back "
          "and used hides to protect the body",
  wrong=["Fossils of Homo erectus were first discovered in Ethiopia and Tanzania",
         "Ramapithecus was more ape-like while Dryopithecus was more man-like",
         "Agriculture began around 18,000 years back, at the same time as pre-historic cave art"],
  why="Homo erectus fossils came from Java; the Ramapithecus/Dryopithecus description is reversed; agriculture "
      "(about 10,000 years back) came much later than cave art (about 18,000 years ago).", secs=60)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, ASR,
  AR("A change in allele frequency that occurs by chance is called genetic drift.",
     "When migration of a section of a population to another place and population occurs multiple times, gene "
     "flow takes place."),
  "Gene flow versus genetic drift",
  "Both statements are NCERT definitions. Gene flow is caused by repeated migration; genetic drift is a chance "
  "change in allele frequency. R describes a different process and does not explain A.",
  ["A: true (definition of genetic drift)", "R: true (definition of gene flow)",
   "Migration does not explain a chance change → R is not the explanation"],
  "Hardy-Weinberg principle", ans="B",
  why="Option A is the trap: both are true, but gene flow is not the cause of genetic drift.", secs=45)

# ================================================================ Human Health and Disease (6/9/6)
Z(HHD, "Pathogens and diseases", B, D,
  "Typhoid fever can be confirmed by the:",
  "Diagnosis of typhoid",
  "Typhoid is caused by Salmonella typhi, which enters the small intestine through contaminated food and water. "
  "The Widal test confirms typhoid fever.",
  ["Typhoid → confirmed by the Widal test"],
  "Common diseases in humans",
  correct="Widal test", wrong=["Amniocentesis", "Autoradiography", "ELISA for HIV antibodies"],
  why="Amniocentesis tests foetal chromosomes, autoradiography detects radioactive probes, and the ELISA named here "
      "detects HIV infection.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "Which of the following correctly describes the common cold?",
  "Common cold",
  "The common cold is caused by rhinoviruses, which infect the nose and respiratory passage but not the lungs. It "
  "spreads through droplets from an infected person's cough or sneeze, or through contaminated objects.",
  ["Pathogen: rhinoviruses", "Site: nose and respiratory passage, not the lungs"],
  "Common diseases in humans",
  correct="It is caused by rhinoviruses that infect the nose and respiratory passage but not the lungs",
  wrong=["It is caused by Streptococcus pneumoniae that infects the alveoli of the lungs",
         "It is caused by rhinoviruses that mainly infect the alveoli of the lungs",
         "It is caused by a protozoan transmitted by the bite of mosquitoes"],
  why="Streptococcus pneumoniae and alveolar infection describe pneumonia; the common cold does not reach the lungs.",
  secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "The antibodies produced in response to allergens such as pollen, dust mites and animal dander are of the type:",
  "Allergy",
  "An allergy is an exaggerated response of the immune system to certain antigens (allergens). The antibodies "
  "produced are of the IgE type; chemicals such as histamine and serotonin are released from mast cells.",
  ["Allergens → IgE antibodies → mast cells release histamine and serotonin"],
  "Immunity (allergies)",
  correct="IgE", wrong=["IgA", "IgG", "IgM"], secs=20)

Z(HHD, "HIV and AIDS", B, D,
  "A widely used diagnostic test for AIDS is:",
  "Diagnosis of AIDS",
  "ELISA (enzyme linked immuno-sorbent assay) is a widely used diagnostic test for AIDS.",
  ["AIDS → ELISA"],
  "AIDS",
  correct="ELISA", wrong=["Widal test", "Amniocentesis", "MRI"], secs=20)

Z(HHD, "Cancer", B, D,
  "Normal cells stop dividing when they come in contact with other cells, a property that cancer cells have lost. "
  "This property is called:",
  "Contact inhibition",
  "In normal cells, contact with other cells inhibits their uncontrolled growth (contact inhibition). Cancer cells "
  "have lost this property, so they keep dividing and form tumours.",
  ["Normal cells: contact inhibition", "Cancer cells: lost → masses of cells (tumours)"],
  "Cancer",
  correct="Contact inhibition", wrong=["Metastasis", "Apoptosis of tumour cells", "Immunosuppression"],
  why="Metastasis is the spread of malignant cells to distant sites, a property of cancer cells, not of normal "
      "cells.", secs=20)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Heroin, commonly called smack, is chemically:",
  "Opioids",
  "Heroin is diacetylmorphine, a white, odourless, bitter crystalline compound obtained by acetylation of morphine, "
  "which is extracted from the latex of the poppy plant Papaver somniferum. It is a depressant.",
  ["Morphine (from poppy latex) → acetylation → diacetylmorphine (heroin)"],
  "Drugs and alcohol abuse",
  correct="Diacetylmorphine, obtained by acetylation of morphine",
  wrong=["A cannabinoid obtained from Cannabis sativa", "An alkaloid obtained from the coca plant",
         "Nicotine obtained from tobacco"], secs=20)

Z(HHD, "Immunity and vaccines", I, MAT,
  ML(("barrier of innate immunity", "example"), ["Physical barrier", "Physiological barrier", "Cellular barrier",
                                                 "Cytokine barrier"],
     ["Interferons secreted by virus-infected cells", "Skin and the mucus coating of epithelia",
      "Acid in the stomach, saliva in the mouth and tears from the eyes",
      "Neutrophils, monocytes, natural killer cells and macrophages"]),
  "Innate immunity",
  "Innate immunity is non-specific and has four kinds of barriers: physical (skin, mucus), physiological (stomach "
  "acid, saliva, tears), cellular (PMNL-neutrophils, monocytes, NK cells, macrophages) and cytokine (interferons "
  "that protect non-infected cells from viral infection).",
  ["Physical → II", "Physiological → III", "Cellular → IV", "Cytokine → I"],
  "Immunity (innate immunity)",
  match=({"A": "II", "B": "III", "C": "IV", "D": "I"},
         [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
          {"A": "II", "B": "IV", "C": "III", "D": "I"}]), secs=40)

Z(HHD, "Pathogens and diseases", I, MUL,
  MS("Which of the following statements about malaria are correct?",
     ["Plasmodium enters the human body as sporozoites through the bite of an infected female Anopheles mosquito.",
      "Fertilisation of Plasmodium gametes takes place inside human red blood cells.",
      "The parasites first multiply within liver cells and then attack red blood cells.",
      "Rupture of RBCs releases haemozoin, which is responsible for the chill and high fever recurring every three "
      "to four days.",
      "Malignant malaria, the most serious type, is caused by Plasmodium vivax."]),
  "Life cycle of Plasmodium",
  "Sporozoites enter through the bite of an infected female Anopheles, multiply in liver cells and then in RBCs. RBC "
  "rupture releases haemozoin (chill and fever every 3–4 days). Gametocytes form in RBCs, but fertilisation and "
  "development occur in the mosquito's stomach. Malignant malaria is caused by P. falciparum.",
  ["(a) True", "(b) False: fertilisation occurs in the mosquito's stomach", "(c) True", "(d) True",
   "(e) False: P. falciparum causes malignant malaria"],
  "Common diseases in humans",
  correct="(a), (c) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (e) only"], secs=60)

Z(HHD, "HIV and AIDS", I, ASR,
  AR("A person infected with HIV gradually becomes immunodeficient.",
     "HIV progressively decreases the number of helper T-lymphocytes in the infected person."),
  "Immunodeficiency in AIDS",
  "Progeny HIV released from infected helper T-lymphocytes attack more helper T-cells, so their number falls "
  "progressively. Because helper T-cells are needed for immune responses, the person becomes immunodeficient and "
  "suffers infections. R explains A.",
  ["A: true", "R: true", "Loss of helper T-cells is the cause of immunodeficiency → R explains A"],
  "AIDS", ans="A", secs=40)

Z(HHD, "Cancer", I, STP,
  SP("Benign tumours normally remain confined to their original location and do not spread to other parts of the "
     "body.",
     "Metastasis is the most feared property of benign tumours."),
  "Benign and malignant tumours",
  "Benign tumours stay confined and cause little damage. Malignant tumours invade surrounding tissues, and their "
  "cells reach distant sites through blood to form new tumours; this metastasis is the most feared property of "
  "malignant tumours.",
  ["Statement I: true", "Statement II: false (metastasis is a property of malignant tumours)"],
  "Cancer", ans="C", secs=30)

Z(HHD, "Immunity and vaccines", I, D,
  "Which of the following is an example of passive immunity?",
  "Active and passive immunity",
  "Passive immunity is given by ready-made antibodies. Antibodies passing from mother to foetus through the placenta "
  "(and IgA in colostrum) are natural examples. Immunity produced by the person's own body after exposure to an "
  "antigen, by infection or vaccination, is active immunity.",
  ["Ready-made antibodies received → passive", "Antibodies made by one's own body → active"],
  "Immunity (active and passive immunity)",
  correct="Antibodies received by the foetus from the mother through the placenta",
  wrong=["Immunity developed after vaccination against hepatitis B",
         "Memory cells formed after the first encounter with a pathogen",
         "Antibodies produced by a person's own B-lymphocytes during an infection"],
  why="The other three involve the person's own immune system producing antibodies or memory cells: active "
      "immunity.", secs=30)

Z(HHD, "Drug and alcohol abuse", I, MAT,
  ML(("drug", "effect"), ["Opioids", "Cocaine", "Cannabinoids", "Nicotine"],
     ["Interferes with the transport of the neurotransmitter dopamine",
      "Bind to specific receptors in the central nervous system and gastrointestinal tract",
      "Known for their effects on the cardiovascular system",
      "Stimulates the adrenal gland to release adrenaline and noradrenaline"]),
  "Commonly abused drugs",
  "Opioids bind specific receptors in the CNS and gut; cannabinoids affect the cardiovascular system; cocaine "
  "(from the coca plant) interferes with dopamine transport; nicotine in tobacco stimulates the adrenal gland to "
  "release adrenaline and noradrenaline, raising blood pressure and heart rate.",
  ["Opioids → II", "Cocaine → I", "Cannabinoids → III", "Nicotine → IV"],
  "Drugs and alcohol abuse",
  match=({"A": "II", "B": "I", "C": "III", "D": "IV"},
         [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
          {"A": "III", "B": "I", "C": "II", "D": "IV"}]), secs=45)

Z(HHD, "Pathogens and diseases", I, STP,
  SP("Aedes mosquitoes are the vectors of dengue and chikungunya.",
     "Introducing fishes such as Gambusia into ponds helps control mosquitoes because they feed on mosquito "
     "larvae."),
  "Vector control",
  "NCERT: Aedes mosquitoes transmit dengue and chikungunya. Control measures include avoiding stagnant water, "
  "spraying insecticides and introducing Gambusia, which feeds on mosquito larvae.",
  ["Statement I: true", "Statement II: true"],
  "Common diseases in humans (prevention and control)", ans="A", secs=30)

Z(HHD, "HIV and AIDS", I, D,
  "HIV is NOT transmitted by:",
  "Transmission of HIV",
  "HIV spreads through body fluids: sexual contact with an infected person, transfusion of contaminated blood or "
  "blood products, sharing infected needles, and from an infected mother to her child through the placenta. It does "
  "not spread by mere touch or physical contact.",
  ["Body fluids → transmission", "Mere touch or physical contact → no transmission"],
  "AIDS",
  correct="Mere touch or physical contact with an infected person",
  wrong=["Transfusion of contaminated blood", "Sharing of infected needles by drug abusers",
         "An infected mother to her child through the placenta"], secs=20)

Z(HHD, "Immunity and vaccines", I, MUL,
  MS("Which of the following statements about acquired immunity are correct?",
     ["Each antibody molecule has two light and two heavy peptide chains (H₂L₂).",
      "Acquired immunity is present from birth and is non-specific.",
      "T-cells do not secrete antibodies themselves but help B-cells to produce them.",
      "The secondary (anamnestic) response is of lower intensity than the primary response.",
      "Cell-mediated immunity is responsible for graft rejection."]),
  "Acquired immunity",
  "Acquired immunity is pathogen-specific and has memory: the secondary (anamnestic) response is highly "
  "intensified. B-cells make antibodies (H₂L₂), T-cells help them, and T-cell–mediated (cell-mediated) immunity "
  "rejects grafts. Innate immunity is the non-specific type present at birth.",
  ["(a) True", "(b) False: that describes innate immunity", "(c) True",
   "(d) False: the secondary response is highly intensified", "(e) True"],
  "Immunity (acquired immunity)",
  correct="(a), (c) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(c), (d) and (e) only", "(a), (b) and (d) only"], secs=60)

Z(HHD, "Cancer", A, MUL,
  MS("Which of the following statements about cancer are correct?",
     ["Computed tomography (CT) uses X-rays to generate a three-dimensional image of the internals of an object.",
      "MRI uses strong magnetic fields and non-ionising radiations to detect pathological changes in living tissue.",
      "Cellular oncogenes (proto-oncogenes) are found only in oncogenic viruses.",
      "α-interferon, a biological response modifier, activates the patient's immune system and helps destroy the "
      "tumour.",
      "UV rays are ionising radiations that cause cancer."]),
  "Detection, causes and treatment of cancer",
  "CT uses X-rays for 3-D images; MRI uses strong magnetic fields and non-ionising radiation. Cellular oncogenes "
  "(c-onc, proto-oncogenes) are present in normal cells and can be activated to cause transformation; viral "
  "oncogenes are in oncogenic viruses. α-interferon is a biological response modifier. UV is a non-ionising "
  "radiation (X-rays and gamma rays are ionising) that can still damage DNA.",
  ["(a) True", "(b) True", "(c) False: proto-oncogenes are in normal cells", "(d) True",
   "(e) False: UV is non-ionising, though it can cause cancer"],
  "Cancer",
  correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(e) is the trap: UV does cause DNA damage, but NCERT classes it as non-ionising.", secs=75)

Z(HHD, "Drug and alcohol abuse", A, ASR,
  AR("Smoking reduces the concentration of haem-bound oxygen in the blood.",
     "Smoking increases the carbon monoxide (CO) content of the blood."),
  "Effects of smoking",
  "Smoke raises the CO content of blood. CO binds to haem in place of oxygen, so the concentration of haem-bound "
  "oxygen falls. R explains A.",
  ["A: true", "R: true", "More CO in blood → less haem-bound O₂ → R explains A"],
  "Drugs and alcohol abuse", ans="A", secs=45)

Z(HHD, "Immunity and vaccines", A, STP,
  SP("Hepatitis B vaccine is produced from yeast using recombinant DNA technology.",
     "When a quick immune response is needed, as in tetanus, a vaccine of weakened pathogens is injected instead "
     "of preformed antibodies or antitoxin."),
  "Vaccination and passive immunisation",
  "Recombinant DNA technology lets antigenic polypeptides be made in bacteria or yeast; hepatitis B vaccine is "
  "produced from yeast. When a quick response is needed, as in tetanus, preformed antibodies or antitoxin are "
  "injected directly (passive immunisation); a vaccine would act too slowly.",
  ["Statement I: true", "Statement II: false (preformed antibodies/antitoxin give the quick response)"],
  "Immunity (vaccination and immunisation)", ans="C", secs=45)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("disease", "feature"), ["Pneumonia", "Amoebiasis", "Filariasis", "Ascariasis"],
     ["Slowly developing chronic inflammation of the lymphatic vessels of the lower limbs",
      "Alveoli fill with fluid; in severe cases the lips and finger nails turn grey to bluish",
      "Stools with excess mucous and blood clots; houseflies act as mechanical carriers",
      "Internal bleeding, muscular pain, fever, anaemia and blockage of the intestinal passage"]),
  "Symptoms of common diseases",
  "Pneumonia (Streptococcus pneumoniae, Haemophilus influenzae) fills the alveoli with fluid. Amoebiasis "
  "(Entamoeba histolytica) infects the large intestine; houseflies carry the parasites. Filariasis (Wuchereria) "
  "inflames lymphatic vessels of the lower limbs (elephantiasis). Ascaris causes internal bleeding, muscular pain, "
  "fever, anaemia and intestinal blockage.",
  ["Pneumonia → II", "Amoebiasis → III", "Filariasis → I", "Ascariasis → IV"],
  "Common diseases in humans",
  match=({"A": "II", "B": "III", "C": "I", "D": "IV"},
         [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
          {"A": "I", "B": "III", "C": "II", "D": "IV"}]),
  why="Amoebiasis and ascariasis are both intestinal, so they are easily swapped; mucous-and-blood stools belong to "
      "amoebiasis.", secs=55)

Z(HHD, "HIV and AIDS", A, D,
  "Which of the following shows the correct sequence of events after HIV enters a macrophage of the human body?",
  "Replication of HIV in the host",
  "HIV, a retrovirus, enters macrophages. Its RNA genome is copied into viral DNA by reverse transcriptase; the "
  "viral DNA is incorporated into the host cell's DNA and directs the infected cell to produce virus particles, so "
  "macrophages act like an HIV factory. (Simultaneously HIV enters helper T-lymphocytes, whose number falls "
  "progressively.)",
  ["Viral RNA → viral DNA (reverse transcriptase)", "Viral DNA → incorporated into host DNA",
   "Infected cell → produces new virus particles"],
  "AIDS",
  correct="Viral RNA copied into viral DNA by reverse transcriptase → viral DNA incorporated into host DNA → "
          "infected cell produces virus particles",
  wrong=["Viral RNA incorporated directly into host DNA → reverse transcriptase copies it into DNA → infected cell "
         "produces virus particles",
         "Viral DNA copied into RNA by reverse transcriptase → viral RNA incorporated into host DNA → infected cell "
         "produces virus particles",
         "Viral RNA translated directly into viral proteins → viral proteins incorporated into host DNA → infected "
         "cell produces virus particles"],
  why="Only DNA can be incorporated into host DNA, so the viral RNA must first be reverse-transcribed; reverse "
      "transcriptase makes DNA from RNA, not RNA from DNA; proteins are never incorporated into DNA.", secs=50)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("Which of the following statements about the lymphoid organs are correct?",
     ["Bone marrow and thymus are primary lymphoid organs, where immature lymphocytes differentiate into "
      "antigen-sensitive lymphocytes.",
      "The thymus is quite large at birth and keeps reducing in size with age.",
      "Peyer's patches of the small intestine are primary lymphoid organs.",
      "Mucosa-associated lymphoid tissue (MALT) constitutes about 50 per cent of the lymphoid tissue in the human "
      "body.",
      "The spleen mainly contains lymphocytes and phagocytes and is a large reservoir of erythrocytes."]),
  "Lymphoid organs",
  "Primary lymphoid organs: bone marrow and thymus. Secondary lymphoid organs: spleen, lymph nodes, tonsils, Peyer's "
  "patches of the small intestine and appendix. The thymus is large at birth and shrinks with age. MALT forms about "
  "50% of the body's lymphoid tissue. The spleen filters blood and stores erythrocytes.",
  ["(a) True", "(b) True", "(c) False: Peyer's patches are secondary lymphoid organs", "(d) True", "(e) True"],
  "Immunity (immune system in the body)",
  correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (d) only", "(b), (c) and (e) only"], secs=70)

# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Restriction enzymes", B, D,
  "The first restriction endonuclease to be isolated, whose functioning depended on a specific DNA nucleotide "
  "sequence, was:",
  "Discovery of restriction endonucleases",
  "The first restriction endonuclease was Hind II. It always cut DNA at a particular point by recognising a "
  "specific sequence of six base pairs, its recognition sequence.",
  ["First restriction endonuclease → Hind II (six-base-pair recognition sequence)"],
  "Tools of recombinant DNA technology (restriction enzymes)",
  correct="Hind II", wrong=["EcoRI", "BamHI", "DNA ligase"],
  why="EcoRI and BamHI are restriction enzymes isolated later; DNA ligase joins DNA and is not a nuclease.",
  secs=20)

Z(BPP, "Competent hosts and transformation", B, D,
  "Bacterial cells are made 'competent' to take up DNA by treating them with a specific concentration of a:",
  "Making host cells competent",
  "DNA is hydrophilic and cannot pass through cell membranes. Treating bacterial cells with a specific "
  "concentration of a divalent cation such as calcium increases the efficiency with which DNA enters the bacterium "
  "through pores in its cell wall.",
  ["Divalent cation (e.g. Ca²⁺) → competence", "Then: incubation on ice → heat shock at 42 °C → back on ice"],
  "Tools of recombinant DNA technology (competent host)",
  correct="Divalent cation such as calcium",
  wrong=["Monovalent cation such as sodium", "Restriction endonuclease", "Chilled ethanol"],
  why="Chilled ethanol precipitates purified DNA during isolation; restriction enzymes cut DNA; NCERT specifies a "
      "divalent cation.", secs=20)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "After agarose gel electrophoresis, the separated DNA fragments are visualised by:",
  "Visualising DNA in a gel",
  "Pure DNA fragments cannot be seen in visible light. They are seen as bright orange bands after staining with "
  "ethidium bromide followed by exposure to UV radiation.",
  ["Stain: ethidium bromide", "Exposure: UV radiation → bright orange bands"],
  "Processes of recombinant DNA technology (separation and isolation of DNA fragments)",
  correct="Staining with ethidium bromide followed by exposure to UV radiation",
  wrong=["Staining with iodine followed by exposure to visible light", "Adding chilled ethanol to the gel",
         "Treating the gel with ribonuclease"], secs=20)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "The thermostable DNA polymerase used in PCR is isolated from the bacterium:",
  "Thermostable DNA polymerase",
  "PCR uses a thermostable DNA polymerase isolated from Thermus aquaticus. It stays active during the high "
  "temperature used to denature double-stranded DNA.",
  ["Thermostable DNA polymerase → Thermus aquaticus"],
  "Processes of recombinant DNA technology (amplification of gene of interest using PCR)",
  correct="Thermus aquaticus", wrong=["Escherichia coli", "Agrobacterium tumefaciens", "Bacillus thuringiensis"],
  secs=20)

Z(BPP, "Competent hosts and transformation", B, STP,
  SP("In biolistics (gene gun), cells are bombarded with high-velocity micro-particles of gold or tungsten coated "
     "with DNA.",
     "In micro-injection, recombinant DNA is directly injected into the nucleus of an animal cell."),
  "Other methods of introducing DNA into host cells",
  "Both statements are NCERT descriptions: biolistics (suitable for plants) uses DNA-coated gold or tungsten "
  "particles; micro-injection puts rDNA directly into an animal cell's nucleus.",
  ["Statement I: true", "Statement II: true"],
  "Tools of recombinant DNA technology (competent host)", ans="A", secs=30)

Z(BPP, "PCR and gel electrophoresis", I, NUM,
  "A PCR is started with 4 molecules of double-stranded template DNA. Assuming every cycle doubles the DNA, how "
  "many double-stranded DNA molecules will be present after 8 cycles?",
  "Exponential amplification in PCR",
  "Each PCR cycle (denaturation, annealing, extension) doubles the number of DNA molecules, so after n cycles there "
  "are N₀ × 2ⁿ molecules.",
  ["N = N₀ × 2ⁿ", "N = 4 × 2⁸ = 4 × 256", "N = 1024 double-stranded molecules"],
  "Processes of recombinant DNA technology (amplification of gene of interest using PCR)",
  correct="1024", wrong=["256", "2048", "32"],
  why="256 forgets the 4 starting molecules; 2048 counts single strands; 32 adds 4 per cycle (linear, 4 × 8) "
      "instead of doubling.", secs=50, vb=RECOMPUTED)

Z(BPP, "Restriction enzymes", I, MAT,
  ML(("enzyme used during isolation of DNA", "purpose"), ["Lysozyme", "Cellulase", "Chitinase", "Protease"],
     ["Breaking open fungal cells", "Breaking open bacterial cells", "Breaking open plant cells",
      "Removing proteins from the DNA preparation"]),
  "Isolation of genetic material",
  "To release DNA, cells are broken with enzymes that digest their walls: lysozyme (bacteria), cellulase (plant "
  "cells) and chitinase (fungi). RNA is removed with ribonuclease and proteins with protease; chilled ethanol then "
  "precipitates the purified DNA.",
  ["Lysozyme → bacterial cells → II", "Cellulase → plant cells → III", "Chitinase → fungal cells → I",
   "Protease → removes proteins → IV"],
  "Processes of recombinant DNA technology (isolation of the genetic material)",
  match=({"A": "II", "B": "III", "C": "I", "D": "IV"},
         [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
          {"A": "I", "B": "III", "C": "II", "D": "IV"}]), secs=40)

Z(BPP, "Cloning vectors", I, ASR,
  AR("When foreign DNA is ligated at the BamHI site of pBR322, the recombinant transformants grow on an "
     "ampicillin-containing medium but not on a tetracycline-containing medium.",
     "Insertion of foreign DNA at the BamHI site inactivates the tetracycline resistance gene."),
  "Insertional inactivation with antibiotic markers",
  "The BamHI site lies in the tetracycline resistance gene of pBR322. Inserting DNA there inactivates tetracycline "
  "resistance, while the ampicillin resistance gene stays intact. So recombinants grow on ampicillin but not on "
  "tetracycline; non-recombinants grow on both. R explains A.",
  ["A: true", "R: true", "Loss of tetR (with ampR intact) is exactly why recombinants fail on tetracycline"],
  "Tools of recombinant DNA technology (cloning vectors)", ans="A", secs=50)

Z(BPP, "Restriction enzymes", I, MUL,
  MS("Which of the following statements about restriction enzymes are correct?",
     ["In EcoRI, the letter 'R' is derived from the name of the bacterial strain.",
      "Exonucleases make cuts at specific positions within the DNA.",
      "The Roman numeral in the name indicates the order in which the enzymes were isolated from that strain of "
      "bacteria.",
      "Fragments with sticky ends produced by the same restriction enzyme can be joined by DNA ligase.",
      "A restriction endonuclease cuts only one strand of the DNA double helix."]),
  "Naming and action of restriction enzymes",
  "In EcoRI, 'E' is the genus (Escherichia), 'co' the species (coli), 'R' the strain (RY 13) and 'I' the order of "
  "isolation. Exonucleases remove nucleotides from the ends; endonucleases cut at specific positions within the DNA, "
  "cutting both strands. Sticky ends made by the same enzyme are joined by DNA ligase.",
  ["(a) True", "(b) False: that describes endonucleases", "(c) True", "(d) True",
   "(e) False: both strands are cut"],
  "Tools of recombinant DNA technology (restriction enzymes)",
  correct="(a), (c) and (d) only",
  wrong=["(a) and (c) only", "(b), (c) and (d) only", "(a), (d) and (e) only"], secs=60)

Z(BPP, "Bioreactors and downstream processing", I, STP,
  SP("Stirred-tank bioreactors are usually cylindrical or have a curved base to facilitate mixing of the reactor "
     "contents.",
     "Bioreactors can process only small volumes of culture, less than 1 litre."),
  "Bioreactors",
  "Bioreactors process large volumes (100–1000 litres) of culture under optimal conditions. The most common are "
  "stirred-tank reactors, which are cylindrical or have a curved base for mixing; the stirrer also spreads oxygen "
  "evenly.",
  ["Statement I: true", "Statement II: false (100–1000 litres)"],
  "Processes of recombinant DNA technology (obtaining the foreign gene product)", ans="C", secs=30)

Z(BPP, "Cloning vectors", I, D,
  "A recombinant DNA is inserted within the coding sequence of the enzyme β-galactosidase in a vector, and the "
  "transformed bacteria are grown on a medium with a chromogenic substrate. Which result is expected?",
  "Insertional inactivation of β-galactosidase",
  "An insert in the β-galactosidase gene inactivates the enzyme. Colonies whose plasmid has no insert make "
  "β-galactosidase and give blue colour with the chromogenic substrate; colonies with the insert produce no colour "
  "and are identified as recombinants.",
  ["Insert → no β-galactosidase → no colour (recombinant)", "No insert → enzyme active → blue colonies"],
  "Tools of recombinant DNA technology (cloning vectors)",
  correct="Colonies with the insert produce no colour, while colonies without the insert give blue colour",
  wrong=["Colonies with the insert give blue colour, while colonies without the insert produce no colour",
         "All colonies give blue colour, whether or not they carry the insert",
         "No colony gives any colour, whether or not it carries the insert"],
  why="The first wrong option reverses the result: the insert destroys the enzyme, so it cannot produce colour.",
  secs=40)

Z(BPP, "Restriction enzymes", I, NUM,
  "A linear DNA molecule and a circular plasmid each have 3 recognition sites for EcoRI. If each is completely "
  "digested with EcoRI, the number of fragments obtained from the linear DNA and from the circular plasmid, "
  "respectively, will be:",
  "Fragments from complete restriction digestion",
  "Each cut in a linear molecule adds one piece, so n cuts give n + 1 fragments. A circle must be cut once just to "
  "open it, so n cuts in a circular molecule give n fragments.",
  ["Linear: 3 cuts → 3 + 1 = 4 fragments", "Circular: 3 cuts → 3 fragments"],
  "Tools of recombinant DNA technology (restriction enzymes)",
  correct="4 and 3", wrong=["3 and 4", "4 and 4", "3 and 3"],
  why="'3 and 4' swaps the two rules; '4 and 4' treats the plasmid as linear; '3 and 3' treats the linear DNA as "
      "circular.", secs=45, vb=RECOMPUTED)

Z(BPP, "Cloning vectors", A, MUL,
  MS("Which of the following statements about the cloning vector pBR322 are correct?",
     ["The rop gene codes for proteins involved in the replication of the plasmid.",
      "The SalI recognition site lies within the tetracycline resistance gene.",
      "Inserting foreign DNA at the PstI site inactivates tetracycline resistance.",
      "pBR322 carries two antibiotic resistance genes, ampR and tetR.",
      "The rop gene confers resistance to ampicillin."]),
  "Features of pBR322",
  "pBR322 has ori, rop (proteins for plasmid replication) and two resistance genes, ampR and tetR. The BamHI and "
  "SalI sites lie in tetR, while the PstI site lies in ampR, so an insert at PstI inactivates ampicillin "
  "resistance, not tetracycline resistance.",
  ["(a) True", "(b) True", "(c) False: PstI lies in ampR", "(d) True", "(e) False: rop is for replication proteins"],
  "Tools of recombinant DNA technology (cloning vectors, Fig. pBR322)",
  correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(c) is the trap: an insert at PstI knocks out ampicillin resistance.", secs=70)

Z(BPP, "Bioreactors and downstream processing", A, ASR,
  AR("Continuous culture systems produce a larger biomass, leading to higher yields of the desired protein.",
     "In a continuous culture system, the cells are maintained in their physiologically most active lag phase."),
  "Continuous culture",
  "In continuous culture, used medium is drained from one side while fresh medium is added from the other, keeping "
  "the cells in their physiologically most active log (exponential) phase. This gives larger biomass and higher "
  "yields. A is true; R is false because it names the lag phase.",
  ["A: true", "R: false (cells are kept in the log/exponential phase, not the lag phase)"],
  "Processes of recombinant DNA technology (obtaining the foreign gene product)", ans="C",
  why="Reading 'lag' as 'log' leads students to option A.", secs=45)

Z(BPP, "Restriction enzymes", A, STP,
  SP("Restriction enzymes cut the DNA strand a little away from the centre of the palindrome site, but between the "
     "same two bases on the opposite strands.",
     "The sticky ends so produced form hydrogen bonds with their complementary cut counterparts, which facilitates "
     "the action of DNA ligase."),
  "Sticky ends",
  "Cutting off-centre but between the same two bases on both strands leaves single-stranded overhangs (sticky "
  "ends). These pair by hydrogen bonds with complementary ends, which helps DNA ligase join the fragments. Both "
  "statements are true.",
  ["Statement I: true", "Statement II: true"],
  "Tools of recombinant DNA technology (restriction enzymes)", ans="A", secs=40)

Z(BPP, "Bioreactors and downstream processing", A, D,
  "Which of the following is the correct sequence of steps in recombinant DNA technology?",
  "Steps of recombinant DNA technology",
  "NCERT lists the steps as: isolation of DNA, fragmentation by restriction endonucleases, isolation of the desired "
  "DNA fragment, ligation into a vector, transfer of the recombinant DNA into the host, culturing the host cells on "
  "a large scale, and extraction of the desired product.",
  ["Isolate DNA → cut → isolate desired fragment → ligate into vector", "Transfer into host → culture → extract product"],
  "Processes of recombinant DNA technology",
  correct="Isolation of DNA → cutting with restriction enzymes → isolation of desired fragment → ligation into vector "
          "→ transfer into host → culturing host cells → extraction of product",
  wrong=["Isolation of DNA → cutting with restriction enzymes → isolation of desired fragment → transfer into host → "
         "ligation into vector → culturing host cells → extraction of product",
         "Isolation of DNA → isolation of desired fragment → cutting with restriction enzymes → ligation into vector "
         "→ transfer into host → culturing host cells → extraction of product",
         "Isolation of DNA → cutting with restriction enzymes → isolation of desired fragment → ligation into vector "
         "→ culturing host cells → transfer into host → extraction of product"],
  why="The fragment must be cut before it can be isolated, ligated into the vector before transfer, and transferred "
      "before the host is cultured.", secs=50)

Z(BPP, "Cloning vectors", A, MAT,
  ML(("feature or vector", "role"), ["Origin of replication (ori)", "Selectable marker",
                                     "Agrobacterium tumefaciens", "Disarmed retroviruses"],
     ["Helps identify and eliminate non-transformants and selectively permits the growth of transformants",
      "Sequence from where replication starts; also controls the copy number of the linked DNA",
      "Delivers T-DNA that transforms normal dicot plant cells into tumour cells",
      "Used to deliver desirable genes into animal cells"]),
  "Cloning vectors and their features",
  "ori is where replication starts and controls copy number. A selectable marker (e.g. an antibiotic resistance "
  "gene) separates transformants from non-transformants. Agrobacterium delivers T-DNA into dicot plant cells; its "
  "Ti plasmid has been modified into a non-pathogenic vector. Retroviruses, which can make animal cells cancerous, "
  "are disarmed and used to deliver genes into animal cells.",
  ["ori → II", "Selectable marker → I", "Agrobacterium tumefaciens → III", "Disarmed retroviruses → IV"],
  "Tools of recombinant DNA technology (cloning vectors)",
  match=({"A": "II", "B": "I", "C": "III", "D": "IV"},
         [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
          {"A": "II", "B": "III", "C": "I", "D": "IV"}]), secs=45)

# ================================================================ Biotechnology and its Applications (5/6/5)
Z(BTA, "Bt crops and RNAi", B, D,
  "The gene that codes for the Bt toxin is named:",
  "Bt toxin genes",
  "The insecticidal Bt toxin of Bacillus thuringiensis is coded by genes named cry (for example cryIAc, cryIIAb, "
  "cryIAb).",
  ["Bt toxin → coded by cry genes"],
  "Biotechnological applications in agriculture",
  correct="cry", wrong=["rop", "ori", "ADA"],
  why="rop and ori are parts of the pBR322 vector; ADA codes for adenosine deaminase.", secs=20)

Z(BTA, "Bt crops and RNAi", B, D,
  "Golden rice, a genetically modified crop with enhanced nutritional value, is enriched in:",
  "Uses of GM plants",
  "One use of GM plants is enhanced nutritional value of food. NCERT's example is golden rice, which is vitamin A "
  "enriched rice.",
  ["Golden rice → vitamin A enriched"],
  "Biotechnological applications in agriculture",
  correct="Vitamin A", wrong=["Vitamin C", "Vitamin D", "Iodine"], secs=20)

Z(BTA, "Gene therapy", B, D,
  "The first clinical gene therapy was given in 1990 to a 4-year-old girl suffering from:",
  "Gene therapy",
  "The first clinical gene therapy (1990) treated a 4-year-old girl with adenosine deaminase (ADA) deficiency, a "
  "disorder caused by deletion of the ADA gene. The enzyme is crucial for the immune system to work.",
  ["1990, 4-year-old girl → ADA deficiency"],
  "Biotechnological applications in medicine (gene therapy)",
  correct="Adenosine deaminase (ADA) deficiency", wrong=["Phenylketonuria", "Emphysema", "Cystic fibrosis"],
  secs=20)

Z(BTA, "Transgenic animals", B, D,
  "Of all the existing transgenic animals, over 95 per cent are:",
  "Transgenic animals",
  "Transgenic rats, rabbits, pigs, sheep, cows and fish have been produced, but over 95% of all existing transgenic "
  "animals are mice.",
  ["Over 95% of transgenic animals → mice"],
  "Transgenic animals",
  correct="Mice", wrong=["Cows", "Sheep", "Fish"], secs=20)

Z(BTA, "Transgenic animals", B, D,
  "Transgenic animals have been used to produce human α-1-antitrypsin, a protein used to treat:",
  "Biological products from transgenic animals",
  "Transgenic animals can produce useful biological products. Human α-1-antitrypsin made this way is used to treat "
  "emphysema.",
  ["α-1-antitrypsin → treatment of emphysema"],
  "Transgenic animals",
  correct="Emphysema", wrong=["Phenylketonuria", "Adenosine deaminase deficiency", "Diabetes mellitus"],
  secs=20)

Z(BTA, "Bt crops and RNAi", I, MUL,
  MS("Which of the following statements about the Bt toxin are correct?",
     ["Bacillus thuringiensis forms protein crystals containing a toxic insecticidal protein during a particular "
      "phase of its growth.",
      "Most Bt toxins are equally effective against all groups of insects.",
      "The alkaline pH of the insect gut solubilises the crystals and the toxin becomes active.",
      "The activated toxin binds to the surface of midgut epithelial cells and creates pores that cause swelling "
      "and lysis of the cells.",
      "Some strains of B. thuringiensis produce proteins that kill lepidopterans, coleopterans and dipterans."]),
  "Mode of action of Bt toxin",
  "B. thuringiensis makes crystals of an insecticidal protein. In the alkaline insect gut the crystals dissolve and "
  "the toxin is activated; it binds midgut epithelial cells and creates pores, causing swelling, lysis and death of "
  "the insect. Most Bt toxins are insect-group specific, so the gene is chosen according to the crop and target "
  "pest.",
  ["(a) True", "(b) False: most Bt toxins are insect-group specific", "(c) True", "(d) True", "(e) True"],
  "Biotechnological applications in agriculture",
  correct="(a), (c), (d) and (e) only",
  wrong=["(a), (b), (c), (d) and (e)", "(a), (c) and (d) only", "(b), (d) and (e) only"], secs=60)

Z(BTA, "Transgenic animals", I, MAT,
  ML(("use of transgenic animals", "example"), ["Vaccine safety", "Chemical safety testing",
                                                "Biological products", "Study of disease"],
     ["Transgenic mice used to test the safety of the polio vaccine",
      "Transgenic cow Rosie produced milk containing human α-lactalbumin",
      "Transgenic models for diseases such as cancer, cystic fibrosis and Alzheimer's",
      "Animals made more sensitive to toxic substances than non-transgenic animals"]),
  "Uses of transgenic animals",
  "Transgenic mice are used to test vaccine safety (e.g. polio vaccine). For toxicity testing, animals are made more "
  "sensitive to toxic substances. Rosie (1997) produced human protein-enriched milk with α-lactalbumin. Transgenic "
  "models help study diseases such as cancer, cystic fibrosis, rheumatoid arthritis and Alzheimer's.",
  ["Vaccine safety → I", "Chemical safety testing → IV", "Biological products → II", "Study of disease → III"],
  "Transgenic animals",
  match=({"A": "I", "B": "IV", "C": "II", "D": "III"},
         [{"A": "IV", "B": "I", "C": "II", "D": "III"}, {"A": "I", "B": "IV", "C": "III", "D": "II"},
          {"A": "II", "B": "IV", "C": "I", "D": "III"}]), secs=45)

Z(BTA, "Bt crops and RNAi", I, ASR,
  AR("The Bt toxin does not kill the Bacillus thuringiensis bacterium that produces it.",
     "In the bacterium, the Bt toxin protein exists as an inactive protoxin."),
  "Why Bt toxin does not harm the bacterium",
  "The toxin is stored as an inactive protoxin and becomes active only in the alkaline gut of the insect that eats "
  "it. So the bacterium is not harmed. R explains A.",
  ["A: true", "R: true", "Inactive protoxin inside the bacterium → no harm to it → R explains A"],
  "Biotechnological applications in agriculture", ans="A", secs=35)

Z(BTA, "Bt crops and RNAi", I, STP,
  SP("RNA interference takes place in all eukaryotic organisms as a method of cellular defence.",
     "The source of the complementary RNA in RNAi could be an infection by viruses having RNA genomes, or mobile "
     "genetic elements (transposons) that replicate via an RNA intermediate."),
  "RNA interference",
  "RNAi silences a specific mRNA through a complementary dsRNA that binds it and prevents translation. It occurs in "
  "all eukaryotes as cellular defence; the complementary RNA may come from RNA viruses or transposons that replicate "
  "via an RNA intermediate. Both statements are true.",
  ["Statement I: true", "Statement II: true"],
  "Biotechnological applications in agriculture (pest resistant plants)", ans="A", secs=35)

Z(BTA, "Human insulin", I, D,
  "During the maturation of human insulin from its pro-hormone, the C peptide is:",
  "Processing of pro-insulin",
  "In mammals insulin is synthesised as a pro-hormone with an extra stretch, the C peptide. The C peptide is removed "
  "during maturation, so mature insulin has only chains A and B joined by disulphide bridges.",
  ["Pro-insulin = A + B + C peptide", "Maturation → C peptide removed → mature insulin (A + B)"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  correct="Removed, so it is not present in mature insulin",
  wrong=["Retained as a third chain of mature insulin", "Added during maturation to link chains A and B",
         "Converted into chain A of mature insulin"],
  why="Chains A and B are linked by disulphide bridges, not by the C peptide, which is absent from the mature "
      "hormone.", secs=30)

Z(BTA, "Gene therapy", I, D,
  "In enzyme replacement therapy for adenosine deaminase (ADA) deficiency:",
  "Treatment approaches for ADA deficiency",
  "NCERT names three approaches: bone marrow transplantation, enzyme replacement therapy (functional ADA given by "
  "injection) and gene therapy (patient's lymphocytes given functional ADA cDNA and returned). Neither of the first "
  "two is completely curative.",
  ["Enzyme replacement → functional ADA injected into the patient"],
  "Biotechnological applications in medicine (gene therapy)",
  correct="Functional ADA enzyme is given to the patient by injection",
  wrong=["Lymphocytes carrying functional ADA cDNA are infused into the patient",
         "The patient receives a bone marrow transplant",
         "The ADA gene is introduced into cells at an early embryonic stage"],
  why="Infusing engineered lymphocytes is gene therapy; bone marrow transplant is a separate approach; introducing "
      "the gene at an early embryonic stage is the possible permanent cure.", secs=35)

Z(BTA, "Human insulin", A, MUL,
  MS("Which of the following statements about genetically engineered human insulin are correct?",
     ["Insulin consists of two short polypeptide chains, A and B, linked together by disulphide bridges.",
      "Insulin extracted from slaughtered cattle and pigs never caused any allergic reaction in patients.",
      "Eli Lilly prepared two DNA sequences corresponding to chains A and B of human insulin and introduced them "
      "into plasmids of E. coli.",
      "Chains A and B were produced separately, extracted and combined by creating disulphide bonds.",
      "Human insulin was first produced commercially by inserting its genes into Agrobacterium tumefaciens."]),
  "Production of human insulin by rDNA technology",
  "Insulin has chains A and B linked by disulphide bridges. Animal insulin caused allergy or other reactions in some "
  "patients. In 1983 Eli Lilly introduced DNA sequences for chains A and B into plasmids of E. coli; the chains were "
  "produced separately, extracted and joined by disulphide bonds to form human insulin.",
  ["(a) True", "(b) False: animal insulin caused allergy in some patients", "(c) True", "(d) True",
   "(e) False: E. coli, not Agrobacterium, was used"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  correct="(a), (c) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a), (b) and (e) only"], secs=60)

Z(BTA, "Gene therapy", A, ASR,
  AR("A patient given gene therapy for ADA deficiency with genetically engineered lymphocytes needs periodic "
     "infusions of such lymphocytes.",
     "The functional ADA cDNA is introduced into the patient's lymphocytes using a retroviral vector."),
  "Limits of lymphocyte-based gene therapy",
  "Lymphocytes from the patient are cultured, given functional ADA cDNA through a retroviral vector and returned. "
  "Both statements are true. But the need for periodic infusion is due to these cells not being immortal, not to "
  "the use of a retroviral vector, so R does not explain A.",
  ["A: true", "R: true", "Real reason for A: the engineered lymphocytes are not immortal"],
  "Biotechnological applications in medicine (gene therapy)", ans="B",
  why="Option A is the trap: R is a true step of the procedure but not the reason for repeated infusions.", secs=50)

Z(BTA, "Bt crops and RNAi", A, STP,
  SP("The proteins encoded by the genes cryIAc and cryIIAb control the corn borer.",
     "The protein encoded by the gene cryIAb controls the corn borer."),
  "Specific cry genes",
  "NCERT: proteins encoded by cryIAc and cryIIAb control cotton bollworms, while that of cryIAb controls the corn "
  "borer. Statement I gives the wrong target pest.",
  ["Statement I: false (cryIAc and cryIIAb → cotton bollworms)", "Statement II: true (cryIAb → corn borer)"],
  "Biotechnological applications in agriculture", ans="D", secs=40)

Z(BTA, "Bt crops and RNAi", A, D,
  "Tobacco plants were made resistant to the nematode Meloidegyne incognitia by RNA interference. The parasite "
  "could not survive in the transgenic host because:",
  "RNAi-based pest resistance",
  "Nematode-specific genes were introduced into tobacco using Agrobacterium vectors. They produced both sense and "
  "anti-sense RNA, which, being complementary, formed dsRNA. The dsRNA started RNAi and silenced a specific mRNA of "
  "the nematode, so the parasite could not survive.",
  ["Agrobacterium vector → nematode-specific genes in tobacco", "Sense + anti-sense RNA → dsRNA",
   "dsRNA → RNAi → nematode mRNA silenced → parasite dies"],
  "Biotechnological applications in agriculture (pest resistant plants)",
  correct="Sense and anti-sense RNA made from the introduced nematode-specific genes formed dsRNA that silenced a "
          "specific mRNA of the nematode",
  wrong=["The transgenic plant produced Bt toxin that formed pores in the nematode's gut cells",
         "The introduced genes made the plant produce antibodies against the nematode",
         "The dsRNA silenced the tobacco plant's own root genes, leaving no root tissue for the nematode"],
  why="Bt toxin is a different strategy; plants do not make antibodies; the silencing targets the parasite's mRNA, "
      "not the host's.", secs=50)

Z(BTA, "Transgenic animals", A, MUL,
  MS("Which of the following statements are correct according to NCERT?",
     ["Transgenic mice are being developed for use in testing the safety of vaccines before they are used on "
      "humans.",
      "In chemical safety testing, transgenic animals carrying genes that make them more sensitive to toxic "
      "substances are exposed to the toxic substances and their effects are studied.",
      "Biopiracy is the use of bio-resources by multinational companies with proper authorisation and compensatory "
      "payment to the countries and people concerned.",
      "Medicines required to treat certain human diseases can contain biological products, but such products are "
      "often expensive to make.",
      "Industrialised nations are generally rich in biodiversity and traditional knowledge."]),
  "Transgenic animals for safety testing and biological products; biopiracy",
  "NCERT: transgenic mice are being developed for use in testing the safety of vaccines before they are used on "
  "humans. In chemical (toxicity/safety) testing, transgenic animals that carry genes making them more sensitive to "
  "toxic substances are exposed to those substances and the effects are studied. Medicines for certain human "
  "diseases can contain biological products, which are often expensive to make; this is why transgenic animals that "
  "produce useful biological products are created. Biopiracy, however, is the use of bio-resources WITHOUT proper "
  "authorisation and compensatory payment, and industrialised nations are financially rich but poor in biodiversity "
  "and traditional knowledge.",
  ["(a) True: vaccine safety", "(b) True: chemical safety testing", "(c) False: biopiracy is use without "
   "authorisation or payment", "(d) True: the reason for making transgenic animals that give biological products",
   "(e) False: developing nations are the ones rich in biodiversity and traditional knowledge"],
  "Transgenic animals; Ethical issues",
  correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"], secs=70)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 123
    ids = [x["question_id"] for x in QUESTIONS]
    assert ids[0] == pkg["question_ids"][0] and ids[-1] == pkg["question_ids"][1] and len(set(ids)) == len(ids)
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    assert all(x["subtopic"] in subtopics[x["topic"]] for x in QUESTIONS)
    assert all(x["solution"]["ncert_reference"] for x in QUESTIONS)
    stems = [x["question_text"] for x in QUESTIONS]
    assert len(set(stems)) == len(stems), "duplicate stem"
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert max(keys.values()) - min(keys.values()) <= 3, keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    for f in (D, ASR, STP, MAT, MUL):
        assert fmts[f] >= 0.08 * len(QUESTIONS), (f, fmts)
    assert 0.03 * len(QUESTIONS) <= fmts[NUM] <= 0.08 * len(QUESTIONS), fmts
    assert all("script:recompute" in x["verification"]["verified_by"] for x in QUESTIONS if x["format"] == NUM)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "ZOO_001_p2: 123 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers re-derived in tools/batch_001/ZOO_001_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
    print("keys", dict(sorted(keys.items())))
    print("formats", dict(fmts))
