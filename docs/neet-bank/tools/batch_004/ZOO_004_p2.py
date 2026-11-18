"""Builder for package ZOO_004_p2 of BATCH_004 (Zoology, 129 questions, NEET_ZOO_000872..NEET_ZOO_001000).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_004/ZOO_004_p2.py      (run from docs/neet-bank)
"""

import json
import math
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
PACKAGE = "ZOO_004_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_004_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_004_ZOO_p2.json"
FIRST_ID = 872

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
    for m in [correct, *wrong]:
        assert sorted(m.values()) == ["I", "II", "III", "IV"], m
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


def revcomp(s):
    return s[::-1].translate(str.maketrans("ATGC", "TACG"))


# ================================================================ verification of computable answers
# HR: one primary spermatocyte (44 autosomes + XY) -> 4 sperms; half carry Y, each has 22 autosomes
sperms = 4
assert sperms // 2 == 2 and 44 // 2 == 22                      # correct: 2 Y-bearing sperms, 22 autosomes each
assert 44 != 22 and 46 // 2 == 23                              # distractors: 44 (forgot halving), 23 (counted X/Y)

# RH: oral pills - 21 days of pills, then a 7-day gap, then the next course starts
assert 21 + 7 == 28                                            # correct: next course starts 28 days after the first pill
assert 21 + 7 + 7 == 35                                        # distractor: counted the gap twice

# EVO: homozygotes (p^2 + q^2) = 0.58 -> 2pq = 0.42 -> pq = 0.21 -> p, q = 0.7, 0.3
hom = F(58, 100)
het = 1 - hom
assert het == F(42, 100) and het / 2 == F(21, 100)
roots = sorted([F(3, 10), F(7, 10)])
assert all(x * (1 - x) == F(21, 100) for x in roots)
assert roots[1] ** 2 + roots[0] ** 2 == hom                    # check: 0.49 + 0.09 = 0.58
assert max(roots) == F(7, 10)                                  # correct: 0.7

# EVO: codominant alleles M, N; 500 people = 180 MM, 240 MN, 80 NN
mm, mn, nn = 180, 240, 80
n = mm + mn + nn
p_m = F(2 * mm + mn, 2 * n)
assert n == 500 and p_m == F(6, 10)
assert (p_m ** 2 * n, 2 * p_m * (1 - p_m) * n, (1 - p_m) ** 2 * n) == (mm, mn, nn)   # observed = expected -> equilibrium
assert F(mm, n) == F(36, 100)                                  # distractor: MM genotype frequency, not allele frequency

# BPP: plasmid copy number 20 per cell, 5 x 10^5 cells -> 1 x 10^7 copies of the cloned gene
assert 20 * 5 * 10 ** 5 == 10 ** 7
assert 5 * 10 ** 5 == 500_000 and 20 + 5 * 10 ** 5 != 10 ** 7  # distractors: one copy per cell; added

# BPP: PCR from one double-stranded molecule, 3 cycles: strands = 2^(n+1); only the 2 template strands lack a primer
cycles = 3
strands = 2 ** (cycles + 1)
assert strands == 16 and strands - 2 == 14                     # correct: 14 primers built into new strands
assert 2 ** cycles == 8 and 2 * cycles == 6                    # distractors: counted molecules; 2 per cycle

# BPP: palindrome check for the direct question
assert revcomp("GGATCC") == "GGATCC"
for s in ("GATCTC", "AAGCTA", "GGAACC"):
    assert revcomp(s) != s

# ================================================================ Chemical Coordination and Integration (5/6/5)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "The hypothalamus, which contains groups of neurosecretory cells that regulate the pituitary, is the basal part "
  "of the:",
  "Location of the hypothalamus",
  "NCERT describes the hypothalamus as the basal part of the diencephalon of the forebrain. It regulates a wide "
  "spectrum of body functions.",
  ["Hypothalamus = basal part of diencephalon", "Diencephalon is a part of the forebrain"],
  "The hypothalamus",
  at="A", correct="Diencephalon of the forebrain",
  wrong=["Midbrain", "Cerebellum of the hindbrain", "Medulla oblongata"],
  why="The midbrain, cerebellum and medulla are other parts of the brain; none of them contains the hypothalamus.",
  secs=25)

Z(CCI, "Hypothalamus and pituitary", B, D,
  "In females, besides causing a vigorous contraction of the uterus at the time of child birth, oxytocin "
  "stimulates:",
  "Actions of oxytocin",
  "Oxytocin acts on the smooth muscles of the body. In females it stimulates a vigorous contraction of the uterus "
  "at child birth and milk ejection from the mammary glands.",
  ["Oxytocin acts on smooth muscle", "Second action in females: milk ejection"],
  "The pituitary gland",
  at="B", correct="Milk ejection from the mammary glands",
  wrong=["Growth of the mammary glands and formation of milk", "Formation of alveoli in the mammary glands",
         "Resorption of water by the distal tubules of the kidney"],
  why="Growth of the mammary glands and milk formation is the action of prolactin; formation of alveoli is "
      "stimulated by progesterone; water resorption by the distal tubules is the action of vasopressin.", secs=30)

Z(CCI, "Hypothalamus and pituitary", B, D,
  "The hormones produced by the hypothalamus that regulate the pituitary are of two types. These are:",
  "Types of hypothalamic hormones",
  "NCERT: the hypothalamic hormones are of two types - releasing hormones, which stimulate the secretion of "
  "pituitary hormones, and inhibiting hormones, which inhibit it. GnRH is a releasing hormone; somatostatin is an "
  "inhibiting hormone.",
  ["Releasing hormones stimulate pituitary secretion", "Inhibiting hormones inhibit pituitary secretion"],
  "The hypothalamus",
  at="C", correct="Releasing hormones and inhibiting hormones",
  wrong=["Glucocorticoids and mineralocorticoids", "Estrogens and progestogens", "Iodothyronines and catecholamines"],
  why="Glucocorticoids and mineralocorticoids come from the adrenal cortex, estrogens and progestogens from the "
      "ovary or placenta, and iodothyronines and catecholamines from the thyroid and adrenal medulla.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "Adrenaline and noradrenaline are rapidly secreted in response to stress of any kind and during emergency "
  "situations. They are therefore called:",
  "Catecholamines as emergency hormones",
  "NCERT calls adrenaline and noradrenaline emergency hormones or hormones of Fight or Flight, because they are "
  "rapidly secreted from the adrenal medulla in response to stress and emergencies.",
  ["Released quickly in stress or emergency", "Name: emergency hormones / hormones of Fight or Flight"],
  "The adrenal gland",
  at="D", correct="Emergency hormones or hormones of Fight or Flight",
  wrong=["Anti-diuretic hormones", "Hypercalcemic hormones", "Gonadotrophins"],
  why="Anti-diuretic hormone is vasopressin, the hypercalcemic hormone is PTH, and gonadotrophins are LH and FSH.",
  secs=25)

Z(CCI, "Mechanism of hormone action", B, D,
  "On the basis of their chemical nature, insulin, glucagon, the pituitary hormones and the hypothalamic hormones "
  "are all grouped as:",
  "Chemical classes of hormones",
  "NCERT groups hormones as (i) peptide, polypeptide and protein hormones (e.g., insulin, glucagon, pituitary "
  "hormones, hypothalamic hormones), (ii) steroids, (iii) iodothyronines and (iv) amino-acid derivatives.",
  ["Insulin, glucagon, pituitary and hypothalamic hormones", "All are peptide/polypeptide/protein hormones"],
  "Mechanism of hormone action",
  at="A", correct="Peptide, polypeptide or protein hormones",
  wrong=["Steroid hormones", "Iodothyronines", "Amino-acid derivatives"],
  why="Steroids are hormones such as cortisol and testosterone; iodothyronines are thyroid hormones; epinephrine "
      "is NCERT's example of an amino-acid derivative.", secs=30)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("Aldosterone stimulates the excretion of K+ and phosphate ions by the renal tubules.",
     "The zona fasciculata forms the middle layer of the adrenal cortex."),
  "Aldosterone and adrenal cortex layers",
  "Aldosterone acts mainly at the renal tubules, stimulating the reabsorption of Na+ and water and the excretion of "
  "K+ and phosphate ions. The adrenal cortex has three layers: zona reticularis (inner), zona fasciculata (middle) "
  "and zona glomerulosa (outer).",
  ["Statement I: true (excretion of K+ and phosphate)", "Statement II: true (fasciculata is the middle layer)"],
  "The adrenal gland", ans="A",
  why="Both statements are NCERT lines, so any option calling either of them false is wrong.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, ASR,
  AR("Androgens produce anabolic (synthetic) effects on protein and carbohydrate metabolism.",
     "Androgens are synthesised and secreted by the Leydig (interstitial) cells of the testis."),
  "Androgens: source versus action",
  "Both are NCERT statements. R tells us where androgens are made; it says nothing about why they have an anabolic "
  "effect on metabolism. Knowing the source of a hormone does not explain its effect on target tissues, so R is "
  "true but not the explanation of A.",
  ["A: true", "R: true", "R gives the site of synthesis, which does not explain the metabolic effect"],
  "Testis", ans="B",
  why="A is wrong because R does not explain A; C and D are wrong because both statements are true.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, MAT,
  ML(("hormone", "action described in NCERT"),
     ["Estrogens", "Androgens", "Catecholamines", "Thymosins"],
     ["Stimulate the breakdown of lipids and proteins",
      "Promote the production of antibodies to provide humoral immunity",
      "Stimulate the development of growing ovarian follicles",
      "Stimulate aggressiveness and a low pitch of voice"]),
  "Lesser-known actions of hormones",
  "Estrogens stimulate the development of growing ovarian follicles. Androgens stimulate muscular growth, facial "
  "and axillary hair, aggressiveness and a low pitch of voice. Catecholamines, besides glycogen breakdown, also "
  "stimulate the breakdown of lipids and proteins. Thymosins, besides differentiating T-lymphocytes, promote the "
  "production of antibodies to provide humoral immunity.",
  ["A (estrogens) - III", "B (androgens) - IV", "C (catecholamines) - I", "D (thymosins) - II"],
  "The adrenal gland; The thymus; Testis; Ovary",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The other codes swap estrogens with androgens, catecholamines with thymosins, or give the catecholamine "
      "action to estrogens.", secs=60)

Z(CCI, "Mechanism of hormone action", I, STP,
  SP("Neural coordination is slow but long-lasting.",
     "Nerve fibres innervate every cell of the body, so hormones are not needed for the continuous regulation of "
     "cellular functions."),
  "Why chemical coordination is needed",
  "NCERT: the neural system provides point-to-point rapid coordination, which is fast but short-lived. As the nerve "
  "fibres do not innervate all cells of the body and cellular functions need continuous regulation, a special kind "
  "of coordination is provided by hormones.",
  ["Statement I: false - neural coordination is fast but short-lived", "Statement II: false - nerve fibres do not "
   "innervate all cells"],
  "Introduction (need for chemical coordination)", ans="B",
  why="Statement I reverses NCERT's 'fast but short-lived' and Statement II contradicts the reason given for "
      "hormones, so every option calling either true is wrong.", secs=40)

Z(CCI, "Hormonal disorders", I, ASR,
  AR("Addison's disease is characterised by acute weakness and fatigue.",
     "Addison's disease is caused by over-production of hormones by the adrenal cortex."),
  "Addison's disease",
  "NCERT: underproduction of hormones by the adrenal cortex alters carbohydrate metabolism, causing acute weakness "
  "and fatigue; this is Addison's disease. So A is true, but R wrongly says over-production.",
  ["A: true (acute weakness and fatigue)", "R: false - it is underproduction, not over-production"],
  "The adrenal gland", ans="C",
  why="R is false, so options A and B (both true) are wrong; A is an NCERT statement, so D is wrong.", secs=40)

Z(CCI, "Thyroid, parathyroid and pineal", I, STP,
  SP("Melatonin helps in maintaining the normal rhythm of body temperature.",
     "The pineal gland is located on the ventral side of the hindbrain."),
  "Melatonin and the pineal gland",
  "Melatonin regulates the 24-hour (diurnal) rhythm of the body; for example, it helps maintain the normal rhythms "
  "of the sleep-wake cycle and body temperature. The pineal gland is located on the dorsal side of the forebrain, "
  "not the ventral side of the hindbrain.",
  ["Statement I: true", "Statement II: false - dorsal side of the forebrain"],
  "The pineal gland", ans="C",
  why="Statement II misplaces the pineal gland, so options A and D are wrong; Statement I is NCERT, so B is wrong.",
  secs=40)

Z(CCI, "Hypothalamus and pituitary", A, MUL,
  MS("Which of the following statements about the pituitary gland are correct?",
     ["LH and FSH are called gonadotrophins because they stimulate gonadal activity.",
      "The pars intermedia secretes only one hormone.",
      "If unchecked, acromegaly may lead to serious complications and premature death.",
      "ACTH stimulates the synthesis and secretion of mineralocorticoids from the adrenal cortex.",
      "In females, FSH maintains the corpus luteum."]),
  "Pituitary hormones and their actions",
  "LH and FSH stimulate gonadal activity and are therefore called gonadotrophins. The pars intermedia secretes only "
  "one hormone, MSH. Acromegaly, if unchecked, may lead to serious complications and premature death. ACTH "
  "stimulates the secretion of glucocorticoids (not mineralocorticoids), and it is LH (not FSH) that maintains the "
  "corpus luteum.",
  ["(a) True", "(b) True: only MSH", "(c) True", "(d) False: ACTH -> glucocorticoids",
   "(e) False: LH maintains the corpus luteum"],
  "The pituitary gland",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"],
  why="Every other option includes (d) or (e), which swap glucocorticoids with mineralocorticoids and LH with FSH.",
  secs=70)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following statements about the pancreas and blood glucose are correct?",
     ["The pancreas acts as both an exocrine and an endocrine gland.",
      "Glucagon reduces the cellular glucose uptake and utilisation.",
      "Glucagon stimulates gluconeogenesis, which also contributes to hyperglycemia.",
      "Insulin and glucagon are steroid hormones.",
      "Glucose homeostasis in blood is maintained by insulin alone."]),
  "Pancreatic hormones and glucose homeostasis",
  "The pancreas is a composite gland, acting as both an exocrine and an endocrine gland. Glucagon reduces cellular "
  "glucose uptake and utilisation, stimulates glycogenolysis and gluconeogenesis, and is hyperglycemic. Insulin and "
  "glucagon are peptide hormones, and glucose homeostasis is maintained jointly by the two.",
  ["(a) True: composite gland", "(b) True", "(c) True", "(d) False: both are peptide hormones",
   "(e) False: maintained jointly by insulin and glucagon"],
  "Pancreas",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
  why="(d) and (e) are false, and every other option contains at least one of them.", secs=70)

Z(CCI, "Mechanism of hormone action", A, D,
  "A drug blocks the generation of second messengers (such as cyclic AMP, IP3 and Ca2+) in target cells, but does "
  "not affect intracellular receptors. The action of which of the following hormones is most likely to be blocked?",
  "Membrane-bound versus intracellular receptors",
  "Hormones that bind membrane-bound receptors do not enter the cell; they generate second messengers. Hormones "
  "that bind intracellular receptors (steroids, iodothyronines) regulate gene expression directly. Glucagon is a "
  "peptide hormone, so it acts through membrane receptors and second messengers; cortisol and testosterone "
  "(steroids) and thyroxine (an iodothyronine) act through intracellular receptors.",
  ["Blocking second messengers affects membrane-receptor hormones", "Steroids and iodothyronines use intracellular "
   "receptors", "Glucagon (peptide) is the only membrane-receptor hormone listed"],
  "Mechanism of hormone action",
  at="B", correct="Glucagon",
  wrong=["Cortisol", "Thyroxine", "Testosterone"],
  why="Cortisol and testosterone are steroids and thyroxine is an iodothyronine; NCERT says these interact with "
      "intracellular receptors, which the drug does not affect.", secs=60)

Z(CCI, "Adrenal, pancreas and gonads", A, D,
  "In a patient, the adrenal cortex has stopped secreting its hormones but the adrenal medulla works normally. "
  "Which of the following would still be secreted normally by the adrenal gland?",
  "Products of the adrenal cortex and medulla",
  "The adrenal medulla secretes adrenaline and noradrenaline (catecholamines). The adrenal cortex secretes the "
  "corticoids - glucocorticoids such as cortisol, mineralocorticoids such as aldosterone - and small amounts of "
  "androgenic steroids. With the cortex failing, only the medullary hormones remain normal.",
  ["Cortex: cortisol, aldosterone, adrenal androgens", "Medulla: adrenaline and noradrenaline",
   "Only medulla is normal -> catecholamines"],
  "The adrenal gland",
  at="C", correct="Adrenaline and noradrenaline",
  wrong=["Cortisol", "Aldosterone", "Small amounts of androgenic steroids that support pubic and axial hair growth"],
  why="Cortisol, aldosterone and the adrenal androgenic steroids are all products of the adrenal cortex, which has "
      "failed in this patient.", secs=50)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following statements about the gonads and their hormones are correct?",
     ["The ovary produces one ovum during each menstrual cycle.",
      "Androgens regulate the development, maturation and functions of the prostate gland and urethra.",
      "Estrogens are secreted mainly by the corpus luteum.",
      "Estrogens stimulate mammary gland development.",
      "Progesterone is a peptide hormone."]),
  "Hormones of the testis and ovary",
  "The ovary produces one ovum during each menstrual cycle. Androgens regulate the male accessory sex organs, "
  "including the prostate gland and urethra. Estrogens are secreted mainly by the growing ovarian follicles and "
  "stimulate mammary gland development; the corpus luteum secretes mainly progesterone. Progesterone, like estrogen, "
  "is a steroid hormone.",
  ["(a) True", "(b) True", "(c) False: growing follicles secrete estrogens", "(d) True",
   "(e) False: progesterone is a steroid"],
  "Testis; Ovary",
  at="D", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"],
  why="(c) gives estrogen the corpus luteum as its main source and (e) calls progesterone a peptide; every other "
      "option includes one of them.", secs=70)

# ================================================================ Human Reproduction (7/9/7)
Z(HR, "Male and female reproductive systems", B, D,
  "In the female external genitalia, the clitoris is a tiny finger-like structure that lies:",
  "Female external genitalia",
  "NCERT: the clitoris is a tiny finger-like structure which lies at the upper junction of the two labia minora, "
  "above the urethral opening.",
  ["Clitoris: tiny finger-like structure", "Position: upper junction of the labia minora, above the urethral opening"],
  "The female reproductive system",
  at="D", correct="At the upper junction of the two labia minora, above the urethral opening",
  wrong=["Below the vaginal opening, between the labia majora", "Inside the cervical canal",
         "On the mons pubis, below the urethral opening"],
  why="NCERT places the clitoris above the urethral opening at the upper junction of the labia minora; the other "
      "positions are invented.", secs=25)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "The average duration of human pregnancy, about 9 months, is called the:",
  "Gestation period",
  "NCERT: the average duration of human pregnancy is about 9 months, which is called the gestation period.",
  ["Duration of pregnancy = gestation period", "About 9 months in humans"],
  "Parturition and lactation",
  at="A", correct="Gestation period",
  wrong=["Lactation period", "Luteal phase", "Ovulatory phase"],
  why="Lactation is milk production after birth; the luteal and ovulatory phases are parts of the menstrual cycle.",
  secs=20)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "The process of delivery of the foetus (child birth) at the end of pregnancy is called:",
  "Parturition",
  "Vigorous contraction of the uterus at the end of pregnancy causes expulsion of the foetus. NCERT calls this "
  "process of delivery of the foetus parturition.",
  ["Delivery of the foetus = parturition"],
  "Parturition and lactation",
  at="B", correct="Parturition",
  wrong=["Implantation", "Insemination", "Ovulation"],
  why="Implantation is the embedding of the blastocyst, insemination is the release of semen into the vagina, and "
      "ovulation is the release of the ovum from the ovary.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "In the human mammary gland, the alveoli open into the:",
  "Duct system of the mammary gland",
  "NCERT: the cells of the alveoli secrete milk, which is stored in their cavities. The alveoli open into mammary "
  "tubules; the tubules of each lobe join to form a mammary duct.",
  ["Alveoli -> mammary tubules", "Tubules of each lobe -> mammary duct"],
  "The female reproductive system",
  at="C", correct="Mammary tubules",
  wrong=["Lactiferous duct directly", "Mammary ampulla directly", "Fallopian tubes"],
  why="The ampulla and lactiferous duct come later in the path (mammary ducts -> ampulla -> lactiferous duct); "
      "fallopian tubes belong to the reproductive tract, not the breast.", secs=30)

Z(HR, "Male and female reproductive systems", B, D,
  "Each human ovary is covered by a thin epithelium which encloses the:",
  "Structure of the ovary",
  "NCERT: each ovary is covered by a thin epithelium which encloses the ovarian stroma. The stroma is divided into a "
  "peripheral cortex and an inner medulla.",
  ["Thin epithelium covers the ovary", "It encloses the ovarian stroma"],
  "The female reproductive system",
  at="D", correct="Ovarian stroma",
  wrong=["Endometrium", "Myometrium", "Seminiferous tubules"],
  why="The endometrium and myometrium are layers of the uterus; seminiferous tubules are found in the testis.",
  secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "Which of the following are the male accessory ducts?",
  "Male accessory ducts",
  "NCERT: the male sex accessory ducts include the rete testis, vasa efferentia, epididymis and vas deferens. The "
  "seminal vesicles, prostate and bulbourethral glands are the male accessory glands.",
  ["Ducts: rete testis, vasa efferentia, epididymis, vas deferens", "Glands: seminal vesicles, prostate, "
   "bulbourethral glands"],
  "The male reproductive system",
  at="A", correct="Rete testis, vasa efferentia, epididymis and vas deferens",
  wrong=["Seminal vesicles, prostate and bulbourethral glands", "Seminiferous tubules, Leydig cells and Sertoli "
         "cells", "Ureter, urinary bladder and urethra only"],
  why="The second option lists accessory glands, the third lists parts and cells of the testis, and the fourth "
      "lists urinary passages.", secs=30)

Z(HR, "Gametogenesis", B, D,
  "The Graafian follicle ruptures to release the secondary oocyte (ovum) from the ovary. This process is called:",
  "Ovulation",
  "NCERT: the Graafian follicle ruptures to release the secondary oocyte (ovum) from the ovary by the process called "
  "ovulation.",
  ["Rupture of Graafian follicle + release of ovum = ovulation"],
  "Gametogenesis",
  at="B", correct="Ovulation",
  wrong=["Spermiation", "Menarche", "Cleavage"],
  why="Spermiation is the release of sperms from the seminiferous tubules, menarche is the first menstruation, and "
      "cleavage is the mitotic division of the zygote.", secs=20)

Z(HR, "Menstrual cycle", I, STP,
  SP("The cycle of events starting from one menstruation till the next one is called the menstrual cycle.",
     "During the follicular phase, the gonadotropins stimulate the secretion of estrogens by the growing follicles."),
  "Menstrual cycle and follicular phase",
  "NCERT defines the menstrual cycle as the cycle of events from one menstruation till the next. The secretion of "
  "gonadotropins (LH and FSH) increases gradually during the follicular phase and stimulates follicular development "
  "as well as the secretion of estrogens by the growing follicles.",
  ["Statement I: true (definition)", "Statement II: true"],
  "Menstrual cycle", ans="A",
  why="Both statements are NCERT lines, so options calling either of them false are wrong.", secs=40)

Z(HR, "Gametogenesis", I, ASR,
  AR("Formation of sperms continues even in old men.",
     "Formation of ova ceases in women around the age of fifty years."),
  "Gametogenesis in old age",
  "NCERT notes that sperm formation continues even in old men, but formation of ova ceases in women around fifty "
  "years. Both are true, but R is a fact about women and cannot explain why men continue to form sperms.",
  ["A: true", "R: true", "R describes women, so it does not explain A"],
  "Introduction (reproductive events in humans)", ans="B",
  why="R cannot explain a fact about men, so A is wrong; both statements are true, so C and D are wrong.", secs=40)

Z(HR, "Gametogenesis", I, NUM,
  "In a human male, a primary spermatocyte has 46 chromosomes (44 autosomes + X + Y). It completes meiosis "
  "normally and the four spermatids become sperms. How many of these sperms carry a Y chromosome, and how many "
  "autosomes does each sperm contain?",
  "Meiosis and sex chromosomes in sperms",
  "Meiosis halves the chromosome number: each sperm gets 22 autosomes plus one sex chromosome. The X and Y separate "
  "in meiosis, so of the four sperms formed from one primary spermatocyte, two carry X and two carry Y. This is why "
  "about 50 per cent of sperms carry X and 50 per cent carry Y.",
  ["Autosomes per sperm = 44 / 2 = 22", "Sex chromosomes: X and Y separate; 4 sperms -> 2 X + 2 Y",
   "Answer: 2 Y-bearing sperms, 22 autosomes each"],
  "Gametogenesis; Fertilisation and implantation",
  at="C", correct="2 sperms carry Y; each sperm has 22 autosomes",
  wrong=["1 sperm carries Y; each sperm has 22 autosomes", "2 sperms carry Y; each sperm has 44 autosomes",
         "4 sperms carry Y; each sperm has 23 autosomes"],
  why="'1 sperm' ignores that the two secondary spermatocytes each divide again; 44 autosomes forgets the halving "
      "in meiosis; 23 counts the sex chromosome as an autosome and '4 Y' ignores X-Y segregation.",
  secs=60, vb=RECOMPUTED)

Z(HR, "Pregnancy, parturition and lactation", I, MAT,
  ML(("hormone", "source"),
     ["Human placental lactogen (hPL)", "Prolactin", "Progesterone during the luteal phase",
      "Gonadotropin releasing hormone (GnRH)"],
     ["Hypothalamus", "Anterior pituitary", "Corpus luteum", "Placenta"]),
  "Sources of reproductive hormones",
  "The placenta acts as an endocrine tissue and produces hCG, hPL, estrogens and progestogens. Prolactin is an "
  "anterior pituitary hormone whose level rises in pregnancy. In the luteal phase, the corpus luteum secretes large "
  "amounts of progesterone. GnRH comes from the hypothalamus and its significant increase at puberty starts "
  "spermatogenesis.",
  ["A (hPL) - IV placenta", "B (prolactin) - II anterior pituitary", "C (progesterone, luteal) - III corpus luteum",
   "D (GnRH) - I hypothalamus"],
  "Pregnancy and embryonic development; Menstrual cycle; Gametogenesis",
  at="D", match=({"A": "IV", "B": "II", "C": "III", "D": "I"},
                 [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "I", "C": "III", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="The other codes give hPL to the pituitary, prolactin to the hypothalamus, or swap the placenta with the "
      "corpus luteum.", secs=50)

Z(HR, "Menstrual cycle", I, D,
  "During the luteal phase, the endometrium is maintained by progesterone from the corpus luteum. According to "
  "NCERT, such an endometrium is necessary for:",
  "Role of the endometrium",
  "Progesterone from the corpus luteum maintains the endometrium. NCERT: such an endometrium is necessary for "
  "implantation of the fertilised ovum and other events of pregnancy.",
  ["Corpus luteum -> progesterone -> endometrium maintained", "Needed for implantation and pregnancy"],
  "Menstrual cycle",
  at="A", correct="Implantation of the fertilised ovum and other events of pregnancy",
  wrong=["Rupture of the Graafian follicle", "Transport of sperms to the ampulla", "Formation of the zona pellucida"],
  why="Follicle rupture is induced by the LH surge, sperm transport happens in the oviduct, and the zona pellucida "
      "is formed by the secondary oocyte; none depends on the maintained endometrium.", secs=35)

Z(HR, "Male and female reproductive systems", I, STP,
  SP("The vasa efferentia open directly into the vas deferens.",
     "The female reproductive system is located in the pelvic region."),
  "Male duct path and female system location",
  "The seminiferous tubules open into the vasa efferentia through the rete testis; the vasa efferentia leave the "
  "testis and open into the epididymis, which leads to the vas deferens. The female reproductive system (ovaries, "
  "oviducts, uterus, cervix, vagina and external genitalia) is located in the pelvic region.",
  ["Statement I: false - vasa efferentia open into the epididymis", "Statement II: true"],
  "The male reproductive system; The female reproductive system", ans="D",
  why="The epididymis lies between the vasa efferentia and the vas deferens, so Statement I is false (A and C "
      "wrong); Statement II is NCERT, so B is wrong.", secs=40)

Z(HR, "Pregnancy, parturition and lactation", I, ASR,
  AR("During parturition, the uterine contractions become stronger and stronger.",
     "Mild uterine contractions (the foetal ejection reflex) trigger the release of oxytocin, which causes stronger "
     "contractions that in turn stimulate further secretion of oxytocin."),
  "Neuroendocrine control of parturition",
  "Signals from the fully developed foetus and placenta induce mild uterine contractions called the foetal ejection "
  "reflex, which triggers oxytocin release from the maternal pituitary. Oxytocin causes stronger contractions, which "
  "stimulate more oxytocin. This stimulatory reflex continues, giving stronger and stronger contractions.",
  ["A: true", "R: true", "The oxytocin-contraction reflex in R is why contractions keep strengthening (A)"],
  "Parturition and lactation", ans="A",
  why="R is the very mechanism NCERT gives for A, so B is wrong; both are true, so C and D are wrong.", secs=45)

Z(HR, "Fertilisation and implantation", I, STP,
  SP("After insemination, the motile sperms pass directly from the vagina into the oviduct without entering the "
     "uterus.",
     "Cleavage of the zygote begins only after it reaches the uterus."),
  "Path of sperms and site of cleavage",
  "NCERT: the motile sperms swim rapidly, pass through the cervix, enter the uterus and finally reach the junction "
  "of the isthmus and ampulla of the oviduct. Cleavage (mitotic division) starts as the zygote moves through the "
  "isthmus of the oviduct towards the uterus.",
  ["Statement I: false - sperms pass through the cervix and uterus", "Statement II: false - cleavage starts in the "
   "oviduct (isthmus)"],
  "Fertilisation and implantation", ans="B",
  why="Both statements contradict NCERT, so every option calling either of them true is wrong.", secs=40)

Z(HR, "Pregnancy, parturition and lactation", I, D,
  "During pregnancy, the levels of estrogens, progestogens, cortisol, prolactin and thyroxine increase several-fold "
  "in the maternal blood. According to NCERT, this increased production is essential for:",
  "Hormones of pregnancy",
  "NCERT: increased production of these hormones is essential for supporting the foetal growth, metabolic changes "
  "in the mother and maintenance of pregnancy.",
  ["Several hormones rise in pregnancy", "Purpose: foetal growth, maternal metabolic changes, maintaining pregnancy"],
  "Pregnancy and embryonic development",
  at="B", correct="Supporting foetal growth, metabolic changes in the mother and maintenance of pregnancy",
  wrong=["Starting a new menstrual cycle during pregnancy", "Causing ovulation every 28 days during pregnancy",
         "Triggering the degeneration of the placenta"],
  why="During pregnancy all events of the menstrual cycle, including ovulation, stop; the hormones support the "
      "pregnancy and do not destroy the placenta.", secs=35)

Z(HR, "Pregnancy, parturition and lactation", A, MUL,
  MS("Which of the following statements about pregnancy and embryonic development are correct?",
     ["Chorionic villi are surrounded by the uterine tissue and maternal blood.",
      "A mesoderm soon appears between the ectoderm and the endoderm of the embryo.",
      "The three germ layers give rise to all tissues (organs) in adults.",
      "Relaxin is secreted by the placenta.",
      "Human pregnancy lasts about 6 months."]),
  "Placenta and germ layers",
  "After implantation, chorionic villi appear on the trophoblast and are surrounded by uterine tissue and maternal "
  "blood. Immediately after implantation, the inner cell mass differentiates into ectoderm and endoderm; a mesoderm "
  "soon appears between them, and these three layers give rise to all tissues (organs) in adults. Relaxin is "
  "secreted by the ovary in the later phase of pregnancy, and human pregnancy lasts about 9 months.",
  ["(a) True", "(b) True", "(c) True", "(d) False: relaxin comes from the ovary", "(e) False: about 9 months"],
  "Pregnancy and embryonic development",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (d) only"],
  why="(d) wrongly names the placenta as the source of relaxin and (e) gives the wrong duration; each other option "
      "contains one of them.", secs=65)

Z(HR, "Gametogenesis", A, MUL,
  MS("Which of the following statements about spermatogenesis are correct?",
     ["Each spermatogonium is diploid and contains 46 chromosomes.",
      "FSH acts on the Leydig cells and stimulates the secretion of androgens.",
      "LH acts at the Leydig cells and stimulates the synthesis and secretion of androgens.",
      "Each secondary spermatocyte has only 23 chromosomes.",
      "Spermatids are transformed into spermatozoa by spermiation."]),
  "Spermatogenesis and its hormonal control",
  "Spermatogonia are diploid (46 chromosomes). The first meiotic division gives two haploid secondary spermatocytes "
  "with 23 chromosomes each. LH acts at the Leydig cells to stimulate androgen secretion, while FSH acts on the "
  "Sertoli cells. Spermatids become spermatozoa by spermiogenesis; spermiation is the release of sperms from the "
  "seminiferous tubules.",
  ["(a) True", "(b) False: FSH acts on Sertoli cells", "(c) True", "(d) True",
   "(e) False: that is spermiogenesis"],
  "Gametogenesis",
  at="D", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only"],
  why="(b) gives FSH the action of LH and (e) confuses spermiation with spermiogenesis; each other option contains "
      "one of them.", secs=65)

Z(HR, "Fertilisation and implantation", A, D,
  "Which of the following shows the correct sequence of reproductive events in humans?",
  "Sequence of reproductive events",
  "NCERT lists the events as: formation of gametes (gametogenesis), transfer of sperms into the female genital "
  "tract (insemination), fusion of gametes (fertilisation), formation and attachment of the blastocyst to the "
  "uterine wall (implantation), embryonic development (gestation) and delivery of the baby (parturition).",
  ["Gametes are made first, then transferred (insemination)", "Fertilisation precedes implantation",
   "Gestation precedes parturition"],
  "Introduction (reproductive events in humans)",
  at="A", correct="Gametogenesis -> insemination -> fertilisation -> implantation -> gestation -> parturition",
  wrong=["Insemination -> gametogenesis -> fertilisation -> gestation -> implantation -> parturition",
         "Gametogenesis -> fertilisation -> insemination -> implantation -> gestation -> parturition",
         "Gametogenesis -> insemination -> implantation -> fertilisation -> gestation -> parturition"],
  why="Gametes must exist before insemination, insemination must come before fertilisation, and only a "
      "fertilised embryo (blastocyst) can implant before gestation; each wrong option breaks one of these.", secs=50)

Z(HR, "Gametogenesis", A, ASR,
  AR("At puberty, each ovary has far fewer primary follicles than the number of oogonia formed in it during fetal "
     "life.",
     "No more oogonia are formed after birth, and a large number of follicles degenerate during the phase from birth "
     "to puberty."),
  "Loss of follicles before puberty",
  "A couple of million oogonia are formed in each fetal ovary and none are added after birth. A large number of "
  "follicles degenerate between birth and puberty, so only 60,000-80,000 primary follicles remain in each ovary at "
  "puberty. R explains A.",
  ["A: true", "R: true", "No new oogonia + degeneration of follicles -> fewer follicles at puberty"],
  "Gametogenesis", ans="A",
  why="R is exactly why the number falls, so B is wrong; both are NCERT statements, so C and D are wrong.", secs=50)

Z(HR, "Male and female reproductive systems", A, STP,
  SP("A functional mammary gland is characteristic of all mammals, both male and female.",
     "The mammary glands are paired structures that contain glandular tissue and a variable amount of fat."),
  "The mammary glands",
  "NCERT: a functional mammary gland is characteristic of all female mammals - not of males. The mammary glands are "
  "paired structures (breasts) that contain glandular tissue and a variable amount of fat.",
  ["Statement I: false - only female mammals", "Statement II: true"],
  "The female reproductive system", ans="D",
  why="Statement I adds males, so options A and C are wrong; Statement II is NCERT, so B is wrong.", secs=45)

Z(HR, "Menstrual cycle", A, MUL,
  MS("Which of the following statements about the human menstrual cycle are correct?",
     ["One ovum is released during the middle of each menstrual cycle.",
      "The secretion of LH and FSH increases gradually during the follicular phase.",
      "The corpus luteum secretes large amounts of estrogen, which maintains the endometrium.",
      "Lack of menstruation may be caused by stress or poor health, and not only by pregnancy.",
      "The menstrual phase is followed directly by the luteal phase."]),
  "Events of the menstrual cycle",
  "One ovum is released in the middle of each cycle. LH and FSH rise gradually in the follicular phase and peak at "
  "mid-cycle. The corpus luteum secretes large amounts of progesterone (not estrogen) to maintain the endometrium. "
  "Lack of menstruation may indicate pregnancy, but may also be due to stress, poor health, etc. The menstrual phase "
  "is followed by the follicular phase.",
  ["(a) True", "(b) True", "(c) False: progesterone", "(d) True", "(e) False: follicular phase follows"],
  "Menstrual cycle",
  at="B", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(c) names the wrong hormone and (e) the wrong phase order; every other option includes one of them.",
  secs=65)

Z(HR, "Fertilisation and implantation", A, MAT,
  ML(("process", "site"),
     ["Fertilisation", "Implantation", "Spermiogenesis",
      "Completion of the first meiotic division of the primary oocyte"],
     ["Tertiary follicle in the ovary", "Seminiferous tubules of the testis", "Endometrium of the uterus",
      "Ampullary region of the oviduct"]),
  "Where reproductive events occur",
  "Fertilisation occurs in the ampullary region of the fallopian tube. The blastocyst implants in the endometrium. "
  "Spermiogenesis (spermatids -> sperms) is part of spermatogenesis in the seminiferous tubules. The primary oocyte "
  "completes its first meiotic division within the tertiary follicle of the ovary.",
  ["A (fertilisation) - IV", "B (implantation) - III", "C (spermiogenesis) - II", "D (meiosis I of oocyte) - I"],
  "Gametogenesis; Fertilisation and implantation",
  at="C", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "I", "B": "III", "C": "II", "D": "IV"}]),
  why="The other codes put fertilisation in the uterus, spermiogenesis in the ovary, or the first meiotic division "
      "in the oviduct.", secs=55)

# ================================================================ Reproductive Health (4/6/4)
Z(RH, "Infertility and ART", B, D,
  "According to NCERT, a couple is described as infertile when:",
  "Meaning of infertility",
  "NCERT: a large number of couples all over the world, including India, are infertile, i.e., they are unable to "
  "produce children in spite of unprotected sexual co-habitation.",
  ["Infertile = unable to produce children", "Condition: in spite of unprotected sexual co-habitation"],
  "Infertility",
  at="A", correct="They are unable to produce children in spite of unprotected sexual co-habitation",
  wrong=["They use contraceptives regularly and so do not have children",
         "One partner has undergone vasectomy or tubectomy by choice",
         "They have decided to adopt a child instead of having their own"],
  why="Using contraceptives or sterilisation is a deliberate choice to prevent conception, and adoption is an "
      "option for parenthood; none of these defines infertility.", secs=25)

Z(RH, "MTP and amniocentesis", B, D,
  "Compared with MTPs done during the first trimester, abortions in the second trimester are, according to NCERT:",
  "Safety of MTP and timing",
  "NCERT: MTPs are considered relatively safe during the first trimester, i.e., up to 12 weeks of pregnancy. "
  "Second trimester abortions are much more risky.",
  ["First trimester: relatively safe", "Second trimester: much more risky"],
  "Medical termination of pregnancy (MTP)",
  at="C", correct="Much more risky",
  wrong=["Equally safe", "Safer, because the foetus is larger", "Completely free of risk if done in a hospital"],
  why="NCERT says the reverse of 'equally safe' or 'safer'; no MTP is described as completely free of risk.",
  secs=20)

Z(RH, "STDs and their prevention", B, D,
  "According to NCERT, what deters persons infected with STIs from going for timely detection and proper "
  "treatment?",
  "Why STIs go untreated",
  "NCERT: absence or less significant symptoms at the early stages of infection and the social stigma attached to "
  "STIs deter infected persons from going for timely detection and proper treatment.",
  ["Early symptoms absent or mild", "Social stigma attached to STIs"],
  "Sexually transmitted infections (STIs)",
  at="B", correct="Absent or less significant early symptoms and the social stigma attached to STIs",
  wrong=["Severe pain from the very first day of infection", "The fact that all STIs are incurable",
         "Lack of any difference between STIs and other diseases"],
  why="Early symptoms are usually mild, not severe; most STIs are curable if detected early; the other option is "
      "not a reason given by NCERT.", secs=30)

Z(RH, "Contraception", B, D,
  "Saheli, an oral contraceptive for females, was developed by scientists at the:",
  "Development of Saheli",
  "NCERT: scientists at the Central Drug Research Institute (CDRI) in Lucknow, India, came out with Saheli, a new "
  "oral contraceptive for females.",
  ["Saheli: new oral contraceptive pill for females", "Developed at CDRI, Lucknow"],
  "Population stabilisation and birth control",
  at="D", correct="Central Drug Research Institute (CDRI), Lucknow",
  wrong=["National AIDS Control Organisation (NACO)", "Indian Agricultural Research Institute (IARI), New Delhi",
         "US Patent and Trademark Office"],
  why="NACO works on AIDS awareness, IARI is an agricultural research institute, and a patent office grants "
      "patents; none developed Saheli.", secs=25)

Z(RH, "Contraception", I, STP,
  SP("Oral contraceptive pills are very effective, have lesser side effects and are well accepted by females.",
     "CuT and Cu7 are copper-releasing intra-uterine devices."),
  "Oral pills and copper IUDs",
  "NCERT: pills are very effective with lesser side effects and are well accepted by the females. Copper-releasing "
  "IUDs include CuT, Cu7 and Multiload 375; Lippes loop is non-medicated and Progestasert and LNG-20 are "
  "hormone-releasing.",
  ["Statement I: true", "Statement II: true"],
  "Population stabilisation and birth control", ans="A",
  why="Both are NCERT statements, so any option calling either false is wrong.", secs=40)

Z(RH, "MTP and amniocentesis", I, ASR,
  AR("MTP has a significant role in decreasing the population.",
     "MTP is meant mainly as a method of population control."),
  "MTP and population",
  "NCERT: MTP has a significant role in decreasing the population, though it is not meant for that purpose. It is "
  "used to get rid of unwanted pregnancies and when continuing the pregnancy could harm the mother or foetus.",
  ["A: true", "R: false - NCERT says MTP is not meant for that purpose"],
  "Medical termination of pregnancy (MTP)", ans="C",
  why="R contradicts NCERT, so A and B are wrong; A itself is an NCERT line, so D is wrong.", secs=40)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive method", "category"),
     ["Coitus interruptus (withdrawal)", "Vaults", "Progestasert", "Vasectomy"],
     ["Surgical method (sterilisation)", "Hormone-releasing IUD", "Barrier method", "Natural method"]),
  "Categories of contraceptives",
  "Coitus interruptus is a natural method. Vaults (like diaphragms and cervical caps) are barriers. Progestasert is a "
  "hormone-releasing IUD. Vasectomy is a surgical (sterilisation) method in the male.",
  ["A - IV natural", "B - III barrier", "C - II hormone-releasing IUD", "D - I surgical"],
  "Population stabilisation and birth control",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "I", "B": "III", "C": "II", "D": "IV"}]),
  why="The other codes call withdrawal a barrier, vaults an IUD, or vasectomy a natural method.", secs=45)

Z(RH, "STDs and their prevention", I, STP,
  SP("Prevention or early detection and cure of STIs are given prime consideration under the reproductive "
     "health-care programmes.",
     "Genital herpes is completely curable if detected early and treated properly."),
  "STIs: priority and curability",
  "NCERT: prevention or early detection and cure of these diseases are given prime consideration under "
  "reproductive health-care programmes. Except hepatitis-B, genital herpes and HIV infections, other STIs are "
  "completely curable if detected early and treated properly.",
  ["Statement I: true", "Statement II: false - genital herpes is one of the exceptions"],
  "Sexually transmitted infections (STIs)", ans="C",
  why="Genital herpes is named among the STIs that are not completely curable, so A and D are wrong; Statement I is "
      "NCERT, so B is wrong.", secs=40)

Z(RH, "STDs and their prevention", I, ASR,
  AR("Introduction of sex education in schools should be encouraged.",
     "It provides the right information to the young, so as to discourage them from believing in myths and having "
     "misconceptions about sex-related aspects."),
  "Sex education and reproductive health",
  "NCERT: introduction of sex education in schools should be encouraged to provide the right information to the "
  "young so as to discourage children from believing in myths and having misconceptions about sex-related aspects. "
  "Proper information about reproductive organs, adolescence, safe and hygienic sexual practices and STIs helps "
  "people lead a reproductively healthy life.",
  ["A: true", "R: true", "R is NCERT's stated purpose for A"],
  "Reproductive health - problems and strategies", ans="A",
  why="R is the reason NCERT gives for encouraging sex education, so B is wrong; both are true, so C and D are "
      "wrong.", secs=40)

Z(RH, "Contraception", I, NUM,
  "A woman uses oral contraceptive pills exactly as NCERT describes: one pill daily for 21 days, starting within "
  "the first five days of the menstrual cycle, followed by a gap of 7 days (during which menstruation occurs) before "
  "the same pattern is repeated. How many days after taking her first pill will she take the first pill of the "
  "next course?",
  "Schedule of oral pills",
  "The pills are taken for 21 days, then there is a 7-day gap; the next course starts after the gap. So the next "
  "course begins 21 + 7 = 28 days after the first pill.",
  ["Pill days = 21", "Gap = 7 days", "Next course starts 21 + 7 = 28 days after the first pill"],
  "Population stabilisation and birth control",
  at="B", correct="28 days",
  wrong=["21 days", "35 days", "14 days"],
  why="21 ignores the 7-day gap, 35 counts the gap twice, and 14 confuses the schedule with the day of ovulation.",
  secs=40, vb=RECOMPUTED)

Z(RH, "Contraception", A, MUL,
  MS("Which of the following statements about contraceptive methods are correct?",
     ["Natural methods have almost no side effects, but their chances of failure are high.",
      "Oral pills inhibit ovulation and implantation and alter the quality of cervical mucus to prevent or retard "
      "the entry of sperms.",
      "Saheli is a 'once a week' pill with very few side effects and high contraceptive value.",
      "Surgical methods (sterilisation) are highly reversible.",
      "IUDs are usually inserted by the woman herself."]),
  "Features of contraceptive methods",
  "As no medicines or devices are used in natural methods, side effects are almost nil, but the chances of failure "
  "are high. Pills inhibit ovulation and implantation and alter cervical mucus. Saheli is a once-a-week, "
  "non-steroidal pill with very few side effects and high contraceptive value. Sterilisation has very poor "
  "reversibility, and IUDs are inserted by doctors or expert nurses.",
  ["(a) True", "(b) True", "(c) True", "(d) False: reversibility is very poor", "(e) False: doctors or expert nurses"],
  "Population stabilisation and birth control",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(d) and (e) are false; every other option includes at least one of them.", secs=65)

Z(RH, "Contraception", A, MUL,
  MS("According to NCERT, which of the following are probable reasons for the rapid increase in human population "
     "that makes birth control necessary?",
     ["A rapid decline in the death rate",
      "A decline in the maternal mortality rate (MMR)",
      "A decline in the infant mortality rate (IMR)",
      "An increase in the number of people in the reproducible age",
      "A rapid rise in the infant mortality rate"]),
  "Causes of population growth",
  "NCERT: a rapid decline in death rate, maternal mortality rate (MMR) and infant mortality rate (IMR), as well as an "
  "increase in the number of people in reproducible age, are probable reasons for the population increase. A rise in "
  "infant mortality would reduce, not increase, the population.",
  ["(a), (b), (c): falling death rates -> more survivors", "(d): more people of reproducible age",
   "(e): opposite of (c) - false"],
  "Population stabilisation and birth control",
  at="A", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(b), (c) and (e) only", "(a) and (d) only"],
  why="(e) is the reverse of NCERT's reason, and '(a) and (d) only' leaves out the falling MMR and IMR, which NCERT "
      "also names.", secs=55)

Z(RH, "Infertility and ART", A, MAT,
  ML(("assisted reproductive technology", "description"),
     ["ZIFT", "IUT", "GIFT", "ICSI"],
     ["Embryos with more than 8 blastomeres are transferred into the uterus",
      "A sperm is directly injected into the ovum to form an embryo in the laboratory",
      "A zygote or early embryo (up to 8 blastomeres) is transferred into the fallopian tube",
      "An ovum collected from a donor is transferred into the fallopian tube of a female who cannot produce one"]),
  "Comparing ART procedures",
  "ZIFT transfers the zygote or early embryo (up to 8 blastomeres) into the fallopian tube; IUT transfers embryos "
  "with more than 8 blastomeres into the uterus; in GIFT, an ovum from a donor is transferred into the fallopian "
  "tube of a female who cannot produce ova but can support fertilisation; in ICSI, a sperm is injected directly "
  "into the ovum in the laboratory.",
  ["A (ZIFT) - III", "B (IUT) - I", "C (GIFT) - IV", "D (ICSI) - II"],
  "Infertility",
  at="B", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "III", "D": "II"}]),
  why="The other codes swap ZIFT with IUT (fallopian tube versus uterus), GIFT with ICSI, or ZIFT with GIFT "
      "(zygote versus donor ovum).", secs=55)

Z(RH, "MTP and amniocentesis", A, D,
  "NCERT lists situations in which MTPs are used or considered essential. Which of the following is NOT one of "
  "them?",
  "Legitimate uses of MTP versus its misuse",
  "MTPs are used to get rid of unwanted pregnancies due to casual unprotected intercourse, failure of the "
  "contraceptive used during coitus or rapes, and are essential when continuing the pregnancy could be harmful or "
  "fatal to the mother or foetus. Terminating a normal pregnancy because amniocentesis showed a female foetus is "
  "the misuse NCERT calls dangerous and against the law.",
  ["Listed: unprotected intercourse, contraceptive failure, rape, danger to mother/foetus",
   "Sex-selective termination after amniocentesis is a misuse, not a listed use"],
  "Medical termination of pregnancy (MTP)",
  at="D", correct="Termination of a normal pregnancy because amniocentesis showed the foetus to be female",
  wrong=["Pregnancy resulting from the failure of the contraceptive used during coitus",
         "Pregnancy resulting from rape",
         "Pregnancy whose continuation could be harmful or even fatal to the mother or the foetus"],
  why="The three wrong options are exactly the situations NCERT lists for MTP.", secs=50)

# ================================================================ Evolution (6/7/5)
Z(EVO, "Origin of life", B, D,
  "Analysis of the contents of meteorites revealed compounds similar to those formed in Miller-type experiments. "
  "According to NCERT, this indicates that:",
  "Meteorite evidence and chemical evolution",
  "NCERT: analysis of meteorite content also revealed similar compounds, indicating that similar processes are "
  "occurring elsewhere in space.",
  ["Meteorites contain compounds like those of Miller's experiment", "Conclusion: similar processes occur elsewhere "
   "in space"],
  "Origin of life",
  at="C", correct="Similar processes are occurring elsewhere in space",
  wrong=["Life on earth was created as such and never changed", "Meteorites brought fully formed cells to the earth",
         "Organic compounds can never form without living organisms"],
  why="The first option is special creation, the second goes beyond what the compounds show, and the fourth is "
      "contradicted by Miller's experiment itself.", secs=30)

Z(EVO, "Origin of life", B, D,
  "Which of the following is NOT one of the connotations of the theory of special creation?",
  "Theory of special creation",
  "Special creation has three connotations: all living organisms (species or types) that we see today were created "
  "as such; the diversity was always the same since creation and will be the same in future; and the earth is about "
  "4000 years old. Gradual origin of species from common ancestors is the idea of evolution, which challenges it.",
  ["Three connotations: created as such; diversity unchanging; earth about 4000 years old",
   "Gradual descent from common ancestors is evolution, not special creation"],
  "Evolution of life forms - a theory",
  at="D", correct="Present-day species arose gradually from common ancestors over millions of years",
  wrong=["All living organisms that we see today were created as such",
         "The diversity of life was always the same since creation and will be the same in future",
         "The earth is about 4000 years old"],
  why="The three wrong options are exactly the three connotations NCERT lists for special creation.", secs=30)

Z(EVO, "Evidences of evolution", B, D,
  "Besides the forelimbs of vertebrates, NCERT gives vertebrate hearts and brains as examples of:",
  "Homologous organs",
  "Under comparative anatomy, NCERT says that besides the forelimbs of whales, bats, cheetahs and humans, other "
  "examples of homology are vertebrate hearts or brains. Homology indicates common ancestry.",
  ["Same basic structure from a common ancestor = homology", "Vertebrate hearts and brains are homologous"],
  "What are the evidences for evolution?",
  at="A", correct="Homologous organs",
  wrong=["Analogous organs", "Convergent evolution", "Vestigial organs"],
  why="Analogous organs and convergent evolution describe different structures performing the same function, which "
      "is not the case for vertebrate hearts; vestigial organs are not the example NCERT uses here.", secs=25)

Z(EVO, "Adaptive radiation", B, D,
  "The process of evolution of different species in a given geographical area, starting from a point and literally "
  "radiating to other areas of geography (habitats), is called:",
  "Definition of adaptive radiation",
  "NCERT defines adaptive radiation as the process of evolution of different species in a given geographical area "
  "starting from a point and literally radiating to other areas of geography (habitats). Darwin's finches and "
  "Australian marsupials are examples.",
  ["Many species from one starting point in an area", "They spread into different habitats = adaptive radiation"],
  "What is adaptive radiation?",
  at="B", correct="Adaptive radiation",
  wrong=["Genetic drift", "Founder effect", "Industrial melanism"],
  why="Genetic drift is a chance change in allele frequency, the founder effect is drift in a new founder "
      "population, and industrial melanism is a change in moth colour after industrialisation.", secs=25)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, D,
  "In the Hardy-Weinberg equation p² + 2pq + q² = 1, for a gene with alleles A (frequency p) and a (frequency q), "
  "the term 2pq represents the frequency of:",
  "Terms of the Hardy-Weinberg equation",
  "In p² + 2pq + q² = 1, p² is the frequency of AA, q² the frequency of aa, and 2pq the frequency of the "
  "heterozygotes (Aa).",
  ["p² = AA", "q² = aa", "2pq = Aa (heterozygotes)"],
  "Hardy-Weinberg principle",
  at="C", correct="Heterozygous individuals (Aa)",
  wrong=["Homozygous dominant individuals (AA)", "Homozygous recessive individuals (aa)", "Allele a alone"],
  why="AA is p² and aa is q²; the frequency of allele a is q, not 2pq.", secs=25)

Z(EVO, "Origin of life", B, D,
  "According to NCERT, which version of the origin of life is accepted by the majority?",
  "Accepted view of the origin of life",
  "NCERT: the version of abiogenesis in which the first form of life arose slowly through evolutionary forces from "
  "non-living molecules is accepted by the majority.",
  ["Abiogenesis: life from non-living molecules", "Arose slowly through evolutionary forces"],
  "Origin of life",
  at="D", correct="The first form of life arose slowly through evolutionary forces from non-living molecules",
  wrong=["All life forms were created as such and have not changed since",
         "Living organisms arise even today from decaying and rotting matter like straw and mud",
         "Life began only when fully formed cells arrived from other planets"],
  why="The first option is special creation, the second is spontaneous generation (disproved by Pasteur), and the "
      "fourth is not the view NCERT says the majority accepts.", secs=30)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a. The combined frequency of the "
  "two homozygous genotypes (AA + aa) is 0.58. What is the frequency of the more common allele?",
  "Working back from genotype frequencies to allele frequencies",
  "p² + 2pq + q² = 1, so 2pq = 1 - 0.58 = 0.42 and pq = 0.21. With p + q = 1, p and q are the roots of "
  "x(1 - x) = 0.21, i.e., 0.7 and 0.3. Check: 0.7² + 0.3² = 0.49 + 0.09 = 0.58. The more common allele has "
  "frequency 0.7.",
  ["2pq = 1 - 0.58 = 0.42", "pq = 0.21 and p + q = 1 -> p = 0.7, q = 0.3", "Check: 0.49 + 0.09 = 0.58"],
  "Hardy-Weinberg principle",
  at="A", correct="0.7",
  wrong=["0.42", "0.21", "0.58"],
  why="0.42 is the heterozygote frequency (2pq), 0.21 is pq, and 0.58 is the given homozygote total; none is an "
      "allele frequency.", short="Try p = 0.7: 0.49 + 0.09 = 0.58 matches at once.", secs=75, vb=RECOMPUTED)

Z(EVO, "Origin of life", I, STP,
  SP("The first non-cellular forms of life would have been single cells enclosed by membranes.",
     "The first cellular forms of life were probably multicellular organisms that lived on land."),
  "First forms of life",
  "NCERT: the first non-cellular forms of life could have originated about 3 billion years back and would have been "
  "giant molecules (RNA, protein, polysaccharides, etc.). The first cellular forms of life were probably single "
  "cells, and all life forms were in a water environment only.",
  ["Statement I: false - giant molecules, not cells", "Statement II: false - single cells, in water"],
  "Origin of life", ans="B",
  why="Both statements contradict NCERT, so every option calling either of them true is wrong.", secs=40)

Z(EVO, "Evidences of evolution", I, ASR,
  AR("Fossils found in rocks are remains of only the soft parts of organisms.",
     "Different-aged rock sediments contain different life forms, which probably died during the formation of the "
     "particular sediment."),
  "Fossils as evidence",
  "NCERT: fossils are remains of hard parts of life forms found in rocks. Rocks form sediments, and different-aged "
  "rock sediments contain different life forms who probably died during the formation of that sediment. So A is "
  "false and R is true.",
  ["A: false - fossils are remains of hard parts", "R: true (NCERT)"],
  "What are the evidences for evolution?", ans="D",
  why="A is false, so options A, B and C (which treat A as true) are wrong.", secs=40)

Z(EVO, "Darwinism and modern synthesis", I, MAT,
  ML(("scientist", "idea or contribution"),
     ["Hugo de Vries", "Lamarck", "Charles Darwin", "Alfred Wallace"],
     ["Worked in the Malay Archipelago and reached conclusions similar to Darwin's",
      "Evolution of life forms driven by the use and disuse of organs",
      "Single-step large mutations (saltation) cause speciation",
      "Branching descent and natural selection, based on observations during the voyage of H.M.S. Beagle"]),
  "Contributors to evolutionary theory",
  "Hugo de Vries, working on evening primrose, proposed that mutations cause speciation and called it saltation. "
  "Lamarck said evolution was driven by use and disuse of organs. Darwin's key concepts, drawn from the voyage of "
  "H.M.S. Beagle, were branching descent and natural selection. Wallace, working in the Malay Archipelago, came to "
  "similar conclusions.",
  ["A (de Vries) - III", "B (Lamarck) - II", "C (Darwin) - IV", "D (Wallace) - I"],
  "Evolution of life forms - a theory; Mechanism of evolution",
  at="B", match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The other codes give saltation to Lamarck, the Malay Archipelago to Darwin, or saltation to Darwin.",
  secs=50)

Z(EVO, "Evidences of evolution", I, MUL,
  MS("Which of the following statements about fossils as evidence for evolution are correct?",
     ["A cross-section of the earth's crust shows sediments arranged one over the other.",
      "Some fossils appear similar to modern organisms.",
      "Dinosaurs are an example of extinct organisms represented by fossils.",
      "Fossils are found only in igneous rocks formed from molten lava.",
      "Fossils are found only in the uppermost (youngest) sediment layer."]),
  "Palaeontological evidence",
  "NCERT: rocks form sediments, and a cross-section of the earth's crust indicates the arrangement of sediments one "
  "over the other. Different-aged sediments contain different life forms; some appear similar to modern organisms, "
  "and others represent extinct organisms such as dinosaurs. Fossils occur in sediments of different ages, not only "
  "in the youngest layer.",
  ["(a) True", "(b) True", "(c) True", "(d) False: fossils are in sedimentary layers",
   "(e) False: sediments of different ages contain fossils"],
  "What are the evidences for evolution?",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"],
  why="(d) and (e) are false; every other option contains at least one of them.", secs=55)

Z(EVO, "Evidences of evolution", I, STP,
  SP("NCERT states that the true reason for the sudden disappearance of the dinosaurs from the earth is not known.",
     "According to NCERT, some say that most of the dinosaurs evolved into birds."),
  "Disappearance of dinosaurs",
  "NCERT: about 65 million years ago the dinosaurs suddenly disappeared from the earth. We do not know the true "
  "reason. Some say climatic changes killed them; some say most of them evolved into birds. The truth may live in "
  "between.",
  ["Statement I: true", "Statement II: true"],
  "A brief account of evolution", ans="A",
  why="Both statements are taken from NCERT's account, so options calling either false are wrong.", secs=35)

Z(EVO, "Natural selection", I, ASR,
  AR("Over a few generations, the selection of pre-existing advantageous mutations can result in speciation.",
     "Pre-existing advantageous mutations, when selected, result in the observation of new phenotypes."),
  "Selection of mutations and speciation",
  "NCERT: the pre-existing advantageous mutations when selected will result in the observation of new phenotypes. "
  "Over a few generations, this would result in speciation. The appearance of new selected phenotypes (R) is what "
  "accumulates into speciation (A).",
  ["A: true", "R: true", "Selected mutations -> new phenotypes -> over generations, new species"],
  "Mechanism of evolution", ans="A",
  why="R is the step NCERT says leads to A, so B is wrong; both are true, so C and D are wrong.", secs=45)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population of 500 people, the alleles M and N of a gene are codominant. The population has 180 MM, 240 MN "
  "and 80 NN individuals. What is the frequency of allele M, and is the population in Hardy-Weinberg equilibrium?",
  "Allele frequency and equilibrium test",
  "With codominance every genotype can be counted. Allele M = (2 x 180 + 240) / (2 x 500) = 600 / 1000 = 0.6, so "
  "N = 0.4. Expected numbers at equilibrium: MM = 0.36 x 500 = 180, MN = 2 x 0.6 x 0.4 x 500 = 240, "
  "NN = 0.16 x 500 = 80. Observed equals expected, so the population is in Hardy-Weinberg equilibrium.",
  ["M alleles = 2(180) + 240 = 600 of 1000 -> p = 0.6", "Expected: MM 180, MN 240, NN 80",
   "Observed = expected -> equilibrium"],
  "Hardy-Weinberg principle",
  at="D", correct="0.6; yes, it is in Hardy-Weinberg equilibrium",
  wrong=["0.6; no, there is an excess of heterozygotes", "0.36; yes, it is in Hardy-Weinberg equilibrium",
         "0.48; no, there is a deficit of heterozygotes"],
  why="0.36 is the MM genotype frequency and 0.48 the MN frequency, not the allele frequency; the observed MN count "
      "(240) equals the expected count, so there is neither an excess nor a deficit of heterozygotes.",
  secs=100, vb=RECOMPUTED)

Z(EVO, "Human evolution", A, D,
  "Which of the following arranges the forms in human evolution in the order in which NCERT describes them, from "
  "the earliest to the latest?",
  "Sequence of human evolution",
  "NCERT: Dryopithecus and Ramapithecus existed about 15 mya; Australopithecines lived about 2 mya; the first "
  "human-like being was Homo habilis; Homo erectus (about 1.5 mya) was the next stage; Neanderthal man lived between "
  "1,00,000 and 40,000 years back; modern Homo sapiens arose during the ice age, between 75,000 and 10,000 years ago.",
  ["Dryopithecus (15 mya) -> Australopithecines (2 mya)", "Homo habilis -> Homo erectus (1.5 mya)",
   "Neanderthal -> modern Homo sapiens"],
  "Origin and evolution of man",
  at="B", correct="Dryopithecus -> Australopithecines -> Homo habilis -> Homo erectus -> Neanderthal man -> "
                  "modern Homo sapiens",
  wrong=["Australopithecines -> Dryopithecus -> Homo habilis -> Homo erectus -> Neanderthal man -> modern Homo "
         "sapiens",
         "Dryopithecus -> Australopithecines -> Homo erectus -> Homo habilis -> Neanderthal man -> modern Homo "
         "sapiens",
         "Dryopithecus -> Australopithecines -> Homo habilis -> Neanderthal man -> Homo erectus -> modern Homo "
         "sapiens"],
  why="Each wrong option swaps one adjacent pair: Dryopithecus is older than the Australopithecines, Homo habilis "
      "came before Homo erectus, and Homo erectus came long before Neanderthal man.", secs=60)

Z(EVO, "Origin of life", A, MUL,
  MS("Which of the following statements about ideas on the origin of life are correct?",
     ["Earlier, it was believed that life came out of decaying and rotting matter like straw and mud (spontaneous "
      "generation).",
      "Louis Pasteur's careful experiments dismissed the theory of spontaneous generation once and for all.",
      "Oparin and Haldane proposed that the first form of life could have come from pre-existing non-living organic "
      "molecules such as RNA and protein.",
      "The early earth had an atmosphere from the very beginning of its formation.",
      "Pasteur showed that new organisms arose from killed yeast in pre-sterilised flasks."]),
  "Spontaneous generation, Pasteur and chemical evolution",
  "Spontaneous generation held that life came from decaying and rotting matter. Pasteur showed that in "
  "pre-sterilised flasks life did not come from killed yeast, while in a flask open to air new organisms arose; "
  "this dismissed spontaneous generation once and for all. Oparin and Haldane proposed that life came from "
  "pre-existing non-living organic molecules, preceded by chemical evolution. NCERT says there was no atmosphere on "
  "the early earth.",
  ["(a) True", "(b) True", "(c) True", "(d) False: no atmosphere on early earth",
   "(e) False: life did not arise in the pre-sterilised flask"],
  "Origin of life",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
  why="(d) contradicts NCERT's 'no atmosphere' and (e) reverses Pasteur's result; every other option contains one "
      "of them.", secs=65)

Z(EVO, "Evidences of evolution", A, MAT,
  ML(("group", "NCERT description"),
     ["First mammals", "First amphibians (from lobefins)", "Tyrannosaurus rex",
      "South American mammals resembling horse, hippopotamus, bear and rabbit"],
     ["Overridden by North American fauna when South America joined North America",
      "Ancestors of modern-day frogs and salamanders",
      "Viviparous; protected their unborn young inside the mother's body",
      "About 20 feet in height, with huge, fearsome, dagger-like teeth"]),
  "Episodes in the history of life",
  "The first mammals were shrew-like, viviparous, and protected the unborn young inside the mother's body. Lobefins "
  "evolved into the first amphibians, ancestors of modern frogs and salamanders. The biggest dinosaur, Tyrannosaurus "
  "rex, was about 20 feet tall with dagger-like teeth. Due to continental drift, when South America joined North "
  "America, its mammals were overridden by North American fauna.",
  ["A (mammals) - III", "B (amphibians) - II", "C (T. rex) - IV", "D (South American mammals) - I"],
  "A brief account of evolution",
  at="D", match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The other codes give viviparity to amphibians, the North American takeover to T. rex, or the dagger-like "
      "teeth to mammals.", secs=55)

Z(EVO, "Origin of life", A, STP,
  SP("As the early earth cooled, water vapour fell as rain to fill the depressions and form oceans.",
     "On the early earth, UV rays from the sun combined hydrogen and oxygen to form water."),
  "Conditions on the early earth",
  "NCERT: UV rays from the sun broke up water into hydrogen and oxygen, and the lighter hydrogen escaped. Oxygen "
  "combined with ammonia and methane to form water, CO2 and others. As the earth cooled, water vapour fell as rain "
  "to fill the depressions and form oceans. Statement II reverses the role of UV rays.",
  ["Statement I: true", "Statement II: false - UV rays broke water up, they did not form it"],
  "Origin of life", ans="C",
  why="Statement II reverses NCERT, so options A and D are wrong; Statement I is NCERT, so B is wrong.", secs=45)

# ================================================================ Human Health and Disease (7/9/7)
Z(HHD, "Cancer", B, D,
  "According to NCERT, among the non-infectious diseases, the major cause of death is:",
  "Infectious and non-infectious diseases",
  "Diseases are broadly grouped into infectious and non-infectious. NCERT: among non-infectious diseases, cancer is "
  "the major cause of death.",
  ["Typhoid, pneumonia and AIDS are infectious", "Major non-infectious killer = cancer"],
  "Introduction; Cancer",
  at="A", correct="Cancer",
  wrong=["AIDS", "Typhoid", "Pneumonia"],
  why="AIDS, typhoid and pneumonia are infectious diseases, so none of them can answer a question about "
      "non-infectious diseases.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "In a chronic infection, the worms live for many years in the lymphatic vessels of the lower limbs, and the "
  "genital organs are also often affected, resulting in gross deformities. The disease and its pathogen are:",
  "Filariasis",
  "NCERT: Wuchereria (W. bancrofti and W. malayi), the filarial worms, cause a slowly developing chronic inflammation "
  "of the organs in which they live for many years, usually the lymphatic vessels of the lower limbs; the disease is "
  "called elephantiasis or filariasis. The genital organs are also often affected, resulting in gross deformities.",
  ["Lymphatic vessels of lower limbs + genital deformities", "Filariasis (elephantiasis), Wuchereria"],
  "Common diseases in humans",
  at="B", correct="Filariasis (elephantiasis), caused by Wuchereria",
  wrong=["Ascariasis, caused by Ascaris", "Amoebiasis, caused by Entamoeba histolytica",
         "Ringworm, caused by Microsporum"],
  why="Ascaris is an intestinal worm, Entamoeba lives in the large intestine, and ringworm fungi infect skin, nails "
      "and scalp; none lives in lymphatic vessels.", secs=30)

Z(HHD, "HIV and AIDS", B, D,
  "In India, the organisation that, along with non-governmental organisations (NGOs), is doing a lot to educate "
  "people about AIDS is the:",
  "AIDS awareness in India",
  "NCERT: in our country the National AIDS Control Organisation (NACO) and other non-governmental organisations "
  "(NGOs) are doing a lot to educate people about AIDS.",
  ["Prevention of AIDS relies on education", "In India: NACO and NGOs"],
  "AIDS",
  at="C", correct="National AIDS Control Organisation (NACO)",
  wrong=["Indian Agricultural Research Institute (IARI)", "Central Drug Research Institute (CDRI)",
         "Indian Patent Office"],
  why="IARI is an agricultural research institute, CDRI developed the pill Saheli, and the patent office grants patents; none "
      "is NCERT's AIDS-education body.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, D,
  "According to NCERT, the period between 12 and 18 years of age may be thought of as the:",
  "Adolescence",
  "NCERT: adolescence means both 'a period' and 'a process' during which a child becomes mature in terms of "
  "attitudes and beliefs for effective participation in society. The period between 12-18 years of age may be "
  "thought of as the adolescence period.",
  ["12-18 years = adolescence period"],
  "Adolescence - drug and alcohol abuse",
  at="D", correct="Adolescence period",
  wrong=["Infancy", "Gestation period", "Old age"],
  why="Infancy is the earliest stage after birth, gestation is the period of pregnancy and old age comes much "
      "later.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "According to the old 'good humor' belief described in NCERT, persons with 'black bile' belonged to a 'hot "
  "personality' and would have:",
  "Early ideas about health",
  "Hippocrates and the Indian Ayurveda system held that health was a balance of certain 'humors'. NCERT: it was "
  "thought that persons with 'black bile' belonged to a 'hot personality' and would have fevers. Such ideas were "
  "later disproved by experiment.",
  ["Health = balance of humors (old belief)", "Black bile -> hot personality -> fevers"],
  "Introduction (health)",
  at="A", correct="Fevers",
  wrong=["Allergies", "Ringworm", "Cancer"],
  why="NCERT links black bile only with a hot personality and fevers; the other conditions are unrelated to the "
      "humor belief.", secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "NCERT states that different types of antibodies are produced in our body. Which of the following lists these "
  "types?",
  "Types of antibodies",
  "NCERT: different types of antibodies are produced in our body; IgA, IgM, IgE, IgG are some of them. Interferons "
  "are proteins of the cytokine barrier, histamine and serotonin are chemicals released from mast cells, and "
  "thymosins are thymus hormones.",
  ["Antibodies: IgA, IgM, IgE, IgG", "Not antibodies: interferons, histamine, serotonin, thymosins"],
  "Immunity",
  at="B", correct="IgA, IgM, IgE and IgG",
  wrong=["Interferons, histamine, serotonin and IgE", "Thymosins, IgA, IgM and IgG",
         "Histamine, IgM, IgE and interferons"],
  why="Each wrong option includes non-antibody substances: interferons, histamine, serotonin or thymosins.",
  secs=25)

Z(HHD, "Pathogens and diseases", B, D,
  "To multiply in a host, a pathogen has to adapt to life within the host's environment. According to NCERT, "
  "pathogens that enter the gut must know a way of:",
  "Adaptation of pathogens",
  "NCERT: a pathogen has to adapt to life within the environment of the host. For example, pathogens that enter the "
  "gut must know a way of surviving in the stomach at low pH and resisting the various digestive enzymes.",
  ["Gut is hostile: low pH in stomach, digestive enzymes", "Pathogen must survive both"],
  "Common diseases in humans",
  at="C", correct="Surviving in the stomach at low pH and resisting the various digestive enzymes",
  wrong=["Surviving only at high temperatures above 100 °C", "Making the stomach contents strongly alkaline",
         "Avoiding the blood completely"],
  why="None of the wrong options is the adaptation NCERT describes; the stomach is acidic, which the pathogen must "
      "withstand rather than reverse.", secs=30)

Z(HHD, "HIV and AIDS", I, STP,
  SP("During the period in which the number of helper T-lymphocytes falls progressively, an HIV-infected person "
     "suffers from bouts of fever, diarrhoea and weight loss.",
     "The time-lag between HIV infection and the appearance of AIDS symptoms may vary from a few months to many "
     "years (usually 5-10 years)."),
  "Course of HIV infection",
  "NCERT: progeny viruses attack other helper T-lymphocytes, leading to a progressive decrease in their number; "
  "during this period the person suffers from bouts of fever, diarrhoea and weight loss. There is always a time-lag "
  "between infection and the appearance of AIDS symptoms, which may vary from a few months to many years (usually "
  "5-10 years).",
  ["Statement I: true", "Statement II: true"],
  "AIDS", ans="A",
  why="Both statements are NCERT lines, so options calling either false are wrong.", secs=40)

Z(HHD, "Pathogens and diseases", I, ASR,
  AR("For diseases like malaria and filariasis, vaccination is the most important preventive measure.",
     "Malaria and filariasis are transmitted through insect vectors."),
  "Prevention of vector-borne diseases",
  "NCERT: in diseases like malaria and filariasis that are transmitted through insect vectors, the most important "
  "measure is to control or eliminate the vectors and their breeding places. So A is false and R is true.",
  ["A: false - vector control is the most important measure", "R: true"],
  "Common diseases in humans", ans="D",
  why="A is false, so options A, B and C (which treat A as true) are wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", I, MAT,
  ML(("term", "meaning or note in NCERT"),
     ["Addiction", "Dependence", "Drug abuse", "Cocaine"],
     ["Obtained from the coca plant, native to South America",
      "Taking drugs for a purpose other than medical use, or in amounts or frequency that impair physical, "
      "physiological or psychological functioning",
      "Tendency of the body to show a characteristic, unpleasant withdrawal syndrome if the regular dose is "
      "abruptly discontinued",
      "A psychological attachment to certain effects, such as euphoria and a temporary feeling of well-being"]),
  "Addiction, dependence and abuse",
  "NCERT: addiction is a psychological attachment to certain effects (euphoria, temporary well-being). Dependence is "
  "the tendency of the body to manifest a characteristic, unpleasant withdrawal syndrome if the regular dose is "
  "abruptly discontinued. Taking drugs for a non-medical purpose, or in amounts or frequency that impair "
  "functioning, constitutes drug abuse. Cocaine is obtained from the coca plant Erythroxylum coca, native to South "
  "America.",
  ["A (addiction) - IV", "B (dependence) - III", "C (drug abuse) - II", "D (cocaine) - I"],
  "Drugs and alcohol abuse; Addiction and dependence",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="The other codes swap addiction with dependence (psychological attachment versus withdrawal syndrome), or "
      "confuse drug abuse with dependence or addiction.", secs=55)

Z(HHD, "Immunity and vaccines", I, MUL,
  MS("Which of the following statements about immunity and auto-immunity are correct?",
     ["Memory-based acquired immunity evolved in higher vertebrates.",
      "Acquired immunity is based on the ability to differentiate foreign organisms (e.g., pathogens) from self-cells.",
      "Due to genetic and other unknown reasons, the body sometimes attacks self-cells, resulting in auto-immune "
      "disease.",
      "Rheumatoid arthritis is an example of an allergy.",
      "Innate immunity is pathogen-specific and is characterised by memory."]),
  "Self versus non-self",
  "NCERT: memory-based acquired immunity evolved in higher vertebrates based on the ability to differentiate foreign "
  "organisms from self-cells. Sometimes, due to genetic and other unknown reasons, the body attacks self-cells, "
  "causing auto-immune disease; rheumatoid arthritis is an example of auto-immune disease, not an allergy. Innate "
  "immunity is non-specific; acquired immunity is pathogen-specific and characterised by memory.",
  ["(a) True", "(b) True", "(c) True", "(d) False: it is auto-immune", "(e) False: describes acquired immunity"],
  "Immunity",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(d) misclassifies rheumatoid arthritis and (e) gives innate immunity the features of acquired immunity; "
      "every other option includes one of them.", secs=55)

Z(HHD, "Cancer", I, STP,
  SP("In cancer cells, the mechanisms that regulate cell growth and differentiation become stronger.",
     "Non-ionising radiations like UV cannot damage DNA."),
  "Cancer cells and carcinogens",
  "NCERT: in our body, cell growth and differentiation is highly controlled and regulated; in cancer cells there is "
  "a breakdown of these regulatory mechanisms. Ionising radiations like X-rays and gamma rays and non-ionising "
  "radiations like UV cause DNA damage leading to neoplastic transformation.",
  ["Statement I: false - regulation breaks down", "Statement II: false - UV also damages DNA"],
  "Cancer", ans="B",
  why="Both statements contradict NCERT, so every option calling either of them true is wrong.", secs=40)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("Recombinant DNA vaccines are produced by growing large quantities of the whole pathogen.",
     "Recombinant DNA technology allows antigenic polypeptides of a pathogen to be produced in bacteria or yeast, "
     "which makes large-scale production possible."),
  "Recombinant vaccines",
  "NCERT: recombinant DNA technology has allowed the production of antigenic polypeptides of the pathogen in "
  "bacteria or yeast; vaccines produced this way allow large-scale production and hence greater availability for "
  "immunisation (e.g., hepatitis B vaccine from yeast). The whole pathogen is not grown, so A is false.",
  ["A: false - only antigenic polypeptides are made, in bacteria or yeast", "R: true"],
  "Immunity (vaccination and immunisation)", ans="D",
  why="A is false, so options A, B and C (which treat A as true) are wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", I, D,
  "Besides cancers of the lung, urinary bladder and throat, NCERT associates smoking with an increased incidence of:",
  "Effects of smoking",
  "NCERT: smoking is associated with increased incidence of cancers of the lung, urinary bladder and throat, "
  "bronchitis, emphysema, coronary heart disease, gastric ulcer, etc.",
  ["Smoking: cancers + bronchitis, emphysema, coronary heart disease, gastric ulcer"],
  "Drugs and alcohol abuse",
  at="D", correct="Bronchitis, emphysema, coronary heart disease and gastric ulcer",
  wrong=["Typhoid, amoebiasis, ascariasis and ringworm", "Goitre, cretinism, acromegaly and diabetes insipidus",
         "Malaria, filariasis, dengue and chikungunya"],
  why="The wrong options list infectious diseases or hormonal disorders, which NCERT does not attribute to smoking.",
  secs=30)

Z(HHD, "HIV and AIDS", I, D,
  "According to NCERT, which of the following groups of people is at high risk of getting HIV infection?",
  "High-risk groups for HIV",
  "NCERT: people at high risk include individuals who have multiple sexual partners, drug addicts who take drugs "
  "intravenously, individuals who require repeated blood transfusions and children born to an HIV-infected mother. "
  "HIV does not spread by mere touch or by mosquitoes like malaria.",
  ["High risk: multiple partners, IV drug users, repeated transfusions, children of infected mothers"],
  "AIDS",
  at="A", correct="Individuals who require repeated blood transfusions",
  wrong=["People living in areas with many Anopheles mosquitoes", "People who received the recombinant hepatitis B "
         "vaccine", "Health workers who only shake hands with patients"],
  why="HIV is not spread by mosquitoes, by vaccines or by touching; only repeated transfusion is one of NCERT's "
      "high-risk groups.", secs=30)

Z(HHD, "Pathogens and diseases", I, D,
  "According to NCERT, when people are healthy:",
  "Importance of health",
  "NCERT: when people are healthy, they are more efficient at work. This increases productivity and brings economic "
  "prosperity. Health also increases the longevity of people and reduces infant and maternal mortality.",
  ["Healthy people work more efficiently", "Productivity, prosperity and longevity rise; infant and maternal "
   "mortality fall"],
  "Introduction (health)",
  at="C", correct="Productivity and economic prosperity increase, longevity increases, and infant and maternal "
                  "mortality fall",
  wrong=["Productivity rises but longevity falls", "Infant and maternal mortality rise because of larger families",
         "Work efficiency falls although immunity rises"],
  why="Each wrong option reverses at least one of NCERT's stated benefits of health.", secs=30)

Z(HHD, "HIV and AIDS", A, MUL,
  MS("Which of the following are among the steps NCERT lists for preventing the spread of HIV?",
     ["Making blood from blood banks safe from HIV",
      "Ensuring the use of only disposable needles and syringes in public and private hospitals and clinics",
      "Free distribution of condoms",
      "Promoting regular check-ups for HIV in susceptible populations",
      "Avoiding all physical contact, including touch, with HIV-infected persons"]),
  "Prevention of AIDS",
  "NCERT lists: making blood (from blood banks) safe from HIV, ensuring use of only disposable needles and syringes, "
  "free distribution of condoms, controlling drug abuse, advocating safe sex and promoting regular check-ups for HIV "
  "in susceptible populations. HIV is not spread by mere touch, so avoiding all contact is neither listed nor "
  "needed; infected persons should not be isolated from family and society.",
  ["(a)-(d) are NCERT measures", "(e) is false: HIV does not spread by touch"],
  "AIDS",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="(e) is based on a myth; every wrong option includes it.", secs=55)

Z(HHD, "HIV and AIDS", A, ASR,
  AR("An AIDS patient may suffer from infections, such as those caused by Mycobacterium or the parasite Toxoplasma, "
     "that could otherwise have been overcome.",
     "In AIDS, the number of helper T-lymphocytes decreases progressively, making the person immunodeficient."),
  "Opportunistic infections in AIDS",
  "NCERT: due to the decrease in helper T-lymphocytes, the person starts suffering from infections that could have "
  "been otherwise overcome, such as those due to bacteria (especially Mycobacterium), viruses, fungi and even "
  "parasites like Toxoplasma. The patient becomes so immunodeficient that he or she cannot fight these infections.",
  ["A: true", "R: true", "Loss of helper T cells (R) -> immunodeficiency -> infections (A)"],
  "AIDS", ans="A",
  why="R is the cause NCERT gives for A, so B is wrong; both are true, so C and D are wrong.", secs=45)

Z(HHD, "Drug and alcohol abuse", A, MUL,
  MS("Which of the following statements about the effects of drug and alcohol abuse are correct?",
     ["Excessive doses of drugs may lead to coma and death due to respiratory failure, heart failure or cerebral "
      "haemorrhage.",
      "Smoking paves the way to hard drugs.",
      "A combination of drugs, or their intake along with alcohol, generally results in overdosing and even deaths.",
      "Heroin is obtained from the inflorescences of Cannabis sativa.",
      "The effects of drug abuse are limited to the abuser and do not reach the family or society."]),
  "Consequences of drug and alcohol abuse",
  "NCERT: excessive doses may lead to coma and death due to respiratory failure, heart failure or cerebral "
  "haemorrhage; a combination of drugs or their intake with alcohol generally results in overdosing and even deaths; "
  "smoking paves the way to hard drugs. Heroin is made from morphine of the poppy plant, and drug abuse has "
  "far-reaching effects on the family and even society.",
  ["(a) True", "(b) True", "(c) True", "(d) False: heroin comes from morphine (poppy)",
   "(e) False: family and society are affected"],
  "Effects of drug/alcohol abuse",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(d) gives heroin the wrong source and (e) denies the social effects; every other option includes one of "
      "them.", secs=60)

Z(HHD, "Cancer", A, STP,
  SP("Cells sloughed from tumours reach distant sites through blood, and wherever they get lodged in the body they "
     "start a new tumour.",
     "Proto-oncogenes (cellular oncogenes) are present only in cancer cells and never in normal cells."),
  "Metastasis and proto-oncogenes",
  "NCERT: cells sloughed from malignant tumours reach distant sites through blood, and wherever they get lodged they "
  "start a new tumour (metastasis). Genes called cellular oncogenes (c-onc) or proto-oncogenes have been identified "
  "in normal cells; when activated under certain conditions, they could lead to oncogenic transformation of the "
  "cells.",
  ["Statement I: true (metastasis)", "Statement II: false - proto-oncogenes are identified in normal cells"],
  "Cancer", ans="C",
  why="Statement II contradicts NCERT's 'identified in normal cells', so options A and D are wrong; Statement I is "
      "NCERT, so B is wrong.", secs=45)

Z(HHD, "Drug and alcohol abuse", A, D,
  "According to NCERT, which of the following is NOT among the causes that motivate youth towards drug and alcohol "
  "use?",
  "Why adolescents start using drugs",
  "NCERT: curiosity, need for adventure and excitement, and experimentation are common causes; the child may later "
  "use drugs to escape facing problems; peer pressure and unstable or unsupportive family structures also "
  "contribute. A stable, supportive family is protective, not a cause.",
  ["Causes: curiosity, adventure, experimentation, escaping problems, peer pressure", "Unstable families "
   "contribute; a stable, supportive family does not"],
  "Adolescence - drug and alcohol abuse",
  at="C", correct="A stable and supportive family structure",
  wrong=["Curiosity, need for adventure and excitement, and experimentation", "Pressure from peers",
         "Using drugs to escape facing problems"],
  why="The three wrong options are causes NCERT names; only the stable, supportive family is the opposite of a "
      "cause.", secs=40)

Z(HHD, "Cancer", A, ASR,
  AR("Cancerous cells give rise to masses of cells called tumours.",
     "Cancerous cells have lost the property of contact inhibition and just continue to divide."),
  "Contact inhibition and tumour formation",
  "Normal cells stop dividing on contact with other cells (contact inhibition). NCERT: cancerous cells appear to "
  "have lost this property; as a result they just continue to divide, giving rise to masses of cells called "
  "tumours. R explains A.",
  ["A: true", "R: true", "Loss of contact inhibition -> continued division -> tumour"],
  "Cancer", ans="A",
  why="R is the cause of A in NCERT's account, so B is wrong; both are true, so C and D are wrong.", secs=40)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("disease", "type of pathogen"),
     ["Typhoid", "Amoebiasis", "Ascariasis", "Ringworm"],
     ["Protozoan", "Fungi", "Bacterium", "Helminth"]),
  "Pathogen groups",
  "Typhoid is caused by the bacterium Salmonella typhi; amoebiasis by the protozoan Entamoeba histolytica; "
  "ascariasis by the helminth (roundworm) Ascaris; ringworm by fungi such as Microsporum, Trichophyton and "
  "Epidermophyton.",
  ["A (typhoid) - III bacterium", "B (amoebiasis) - I protozoan", "C (ascariasis) - IV helminth",
   "D (ringworm) - II fungi"],
  "Common diseases in humans",
  at="A", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="The other codes call typhoid protozoan, ringworm a worm, or amoebiasis a helminth disease.", secs=45)

# ================================================================ Biotechnology: Principles and Processes (6/7/6)
Z(BPP, "Restriction enzymes", B, D,
  "Restriction endonucleases recognise palindromic sequences, which read the same on the two strands of DNA when "
  "the orientation of reading is kept the same (5' to 3'). Which of the following double-stranded sequences, given "
  "as its upper (5' to 3') strand, is a palindrome?",
  "Palindromic recognition sequences",
  "A sequence is palindromic if its complementary strand, read 5' to 3', is the same. For 5'-GGATCC-3' the "
  "complementary strand is 3'-CCTAGG-5', which read 5' to 3' is GGATCC - identical. The other sequences give "
  "different sequences when the complementary strand is read 5' to 3'.",
  ["Write the complementary strand", "Read it 5' to 3' (right to left)", "GGATCC -> GGATCC: palindrome"],
  "Tools of recombinant DNA technology (restriction enzymes)",
  at="A", correct="5'-GGATCC-3'",
  wrong=["5'-GATCTC-3'", "5'-AAGCTA-3'", "5'-GGAACC-3'"],
  why="GATCTC reads GAGATC on the other strand, AAGCTA reads TAGCTT and GGAACC reads GGTTCC; none is the same on "
      "both strands.", short="The second half must be the complement of the first half read backwards: GGA|TCC.",
  secs=50)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "In the polymerase chain reaction (PCR), the DNA polymerase extends the primers using:",
  "Extension step of PCR",
  "NCERT: in PCR, the enzyme extends the primers using the nucleotides provided in the reaction and the genomic DNA "
  "as template. A thermostable polymerase is used so that it survives the high-temperature denaturation.",
  ["Primers bind the template", "Polymerase adds nucleotides supplied in the reaction, copying the genomic DNA "
   "template"],
  "Amplification of gene of interest using PCR",
  at="B", correct="The nucleotides provided in the reaction and the genomic DNA as template",
  wrong=["Amino acids provided in the reaction and mRNA as template", "Restriction enzymes and DNA ligase",
         "Ribosomes of the host cell and tRNA"],
  why="Amino acids, ribosomes and tRNA are used in protein synthesis, not DNA synthesis; restriction enzymes and "
      "ligase cut and join DNA but do not copy it.", secs=30)

Z(BPP, "Bioreactors and downstream processing", B, D,
  "According to NCERT, bioreactors can be thought of as vessels in which:",
  "What a bioreactor is",
  "NCERT: bioreactors can be thought of as vessels in which raw materials are biologically converted into specific "
  "products, individual enzymes, etc., using microbial, plant, animal or human cells.",
  ["Raw materials -> products by biological conversion", "Uses microbial, plant, animal or human cells"],
  "Obtaining the foreign gene product",
  at="C", correct="Raw materials are biologically converted into specific products using microbial, plant, animal "
                  "or human cells",
  wrong=["DNA is cut into fragments and separated by size", "DNA is amplified in vitro by repeated cycles of "
         "heating and cooling", "Bacterial cells are made competent with calcium ions"],
  why="Cutting and separating DNA describes restriction digestion and gel electrophoresis, amplification is PCR, "
      "and making cells competent is a transformation step.", secs=30)

Z(BPP, "Cloning vectors", B, D,
  "Retroviruses are used to develop vectors for animal cells because, in animals, retroviruses have the ability "
  "to:",
  "Retroviruses as vectors",
  "NCERT: retroviruses in animals have the ability to transform normal cells into cancerous cells. Disarmed "
  "retroviruses are now used to deliver desirable genes into animal cells.",
  ["Natural ability: transform normal cells into cancerous cells", "Disarmed forms deliver useful genes"],
  "Cloning vectors",
  at="D", correct="Transform normal cells into cancerous cells",
  wrong=["Deliver T-DNA into dicot plant cells", "Cut DNA at specific palindromic sites",
         "Remain active at the high temperatures used in PCR"],
  why="Delivering T-DNA is the property of Agrobacterium tumefaciens, cutting at palindromes is done by restriction "
      "enzymes, and heat stability belongs to Taq polymerase.", secs=30)

Z(BPP, "Cloning vectors", B, D,
  "A piece of alien DNA moved into an organism usually cannot multiply in the progeny cells. When it becomes "
  "integrated into the genome of the recipient, it may multiply and be inherited along with the host DNA because:",
  "Why alien DNA must join a replicon",
  "NCERT: when the alien piece of DNA becomes part of a chromosome, which has the ability to replicate, it is "
  "replicated and inherited along with the host DNA. A chromosome carries an origin of replication, responsible for "
  "initiating replication.",
  ["Free alien DNA cannot replicate on its own", "Once part of a chromosome (with ori) it replicates with it"],
  "Principles of biotechnology",
  at="B", correct="It has become part of a chromosome, which has the ability to replicate",
  wrong=["It has been cut into sticky ends by a restriction enzyme", "It has been stained with ethidium bromide",
         "It has been converted into protein by the host cell"],
  why="Sticky ends allow joining, staining allows viewing, and translation makes protein; none of these lets the "
      "DNA replicate.", secs=35)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "After agarose gel electrophoresis, the separated DNA bands are cut out and the DNA is extracted (elution). "
  "According to NCERT, the purified DNA fragments are then used in:",
  "Use of eluted DNA fragments",
  "NCERT: the separated bands of DNA are cut out from the agarose gel and extracted from the gel piece (elution). "
  "The DNA fragments purified in this way are used in constructing recombinant DNA by joining them with cloning "
  "vectors.",
  ["Separate -> cut out band -> elute", "Purified fragment joined with a cloning vector -> recombinant DNA"],
  "Separation and isolation of DNA fragments",
  at="B", correct="Constructing recombinant DNA by joining them with cloning vectors",
  wrong=["Making bacterial cells competent", "Measuring the copy number of a plasmid",
         "Producing ethidium bromide for staining"],
  why="Competence is induced with divalent cations, copy number is a property of the vector, and ethidium bromide "
      "is a stain added from outside; none is what eluted DNA is used for.", secs=30)

Z(BPP, "Cloning vectors", I, NUM,
  "A gene is cloned into a plasmid whose copy number is 20 per cell. A culture contains 5 × 10^5 transformed "
  "bacterial cells, each carrying the recombinant plasmid at this copy number. How many copies of the cloned gene "
  "are present in the culture?",
  "Copy number and amplification of cloned DNA",
  "NCERT: if an alien piece of DNA is linked with plasmid DNA, its number can be multiplied to the copy number of "
  "the plasmid. With 20 plasmids per cell and 5 × 10^5 cells: 20 × 5 × 10^5 = 1 × 10^7 copies.",
  ["Copies per cell = copy number = 20", "Total = 20 × 5 × 10^5", "= 1 × 10^7"],
  "Cloning vectors",
  at="C", correct="1 × 10^7",
  wrong=["5 × 10^5", "2.5 × 10^4", "1 × 10^6"],
  why="5 × 10^5 assumes one copy per cell, 2.5 × 10^4 divides by the copy number instead of multiplying, and "
      "1 × 10^6 slips a power of ten.", secs=45, vb=RECOMPUTED)

Z(BPP, "Restriction enzymes", I, STP,
  SP("Restriction enzyme digestions are performed by incubating purified DNA molecules with the restriction enzyme "
     "under the optimal conditions for that specific enzyme.",
     "Sticky ends are so named because they form covalent bonds with their complementary cut counterparts."),
  "Restriction digestion and sticky ends",
  "NCERT: restriction enzyme digestions are performed by incubating purified DNA with the enzyme at the optimal "
  "conditions for that specific enzyme. Sticky ends are named so because they form hydrogen bonds (not covalent "
  "bonds) with their complementary cut counterparts; DNA ligase then seals the backbone.",
  ["Statement I: true", "Statement II: false - hydrogen bonds"],
  "Processes of recombinant DNA technology; Restriction enzymes", ans="C",
  why="Statement II replaces hydrogen bonds with covalent bonds, so options A and D are wrong; Statement I is "
      "NCERT, so B is wrong.", secs=40)

Z(BPP, "Cloning vectors", I, ASR,
  AR("Plasmids and bacteriophages are used as cloning vectors.",
     "Plasmids and bacteriophages have the ability to replicate within bacterial cells independent of the control "
     "of chromosomal DNA."),
  "Why plasmids and phages are vectors",
  "NCERT: plasmids and bacteriophages have the ability to replicate within bacterial cells independent of the "
  "control of chromosomal DNA. So a foreign DNA linked to them is replicated too, which is why they are used as "
  "cloning vectors.",
  ["A: true", "R: true", "Independent replication carries the linked foreign DNA along -> vector"],
  "Cloning vectors", ans="A",
  why="R is the property that makes them vectors, so B is wrong; both are true, so C and D are wrong.", secs=40)

Z(BPP, "Restriction enzymes", I, MAT,
  ML(("part of the name 'EcoRI'", "what it indicates"),
     ["E", "co", "R", "I"],
     ["Order in which the enzyme was isolated from that strain", "Strain RY 13", "Species coli",
      "Genus Escherichia"]),
  "Naming of restriction enzymes",
  "NCERT: the first letter of the name comes from the genus and the second two letters from the species of the "
  "prokaryotic cell; EcoRI comes from Escherichia coli RY 13, the letter 'R' coming from the strain. The Roman "
  "numeral indicates the order in which the enzymes were isolated from that strain.",
  ["E - Escherichia (genus)", "co - coli (species)", "R - strain RY 13", "I - first enzyme isolated from the strain"],
  "Tools of recombinant DNA technology (restriction enzymes)",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The other codes swap genus with species, strain with the Roman numeral, or species with strain.", secs=40)

Z(BPP, "Cloning vectors", I, MUL,
  MS("Which of the following statements about the principles of biotechnology are correct?",
     ["Traditional hybridisation often leads to the inclusion and multiplication of undesirable genes along with "
      "the desired genes.",
      "Genetic engineering allows us to isolate and introduce only one or a set of desirable genes into the target "
      "organism.",
      "The techniques of genetic engineering include creation of recombinant DNA, use of gene cloning and gene "
      "transfer.",
      "Traditional hybridisation transfers only the desired gene into the progeny."]),
  "Genetic engineering versus hybridisation",
  "NCERT: traditional hybridisation procedures very often lead to inclusion and multiplication of undesirable genes "
  "along with the desired genes. The techniques of genetic engineering, which include creation of recombinant DNA, "
  "use of gene cloning and gene transfer, overcome this limitation and allow us to isolate and introduce only one "
  "or a set of desirable genes.",
  ["(a) True", "(b) True", "(c) True", "(d) False: contradicts (a)"],
  "Principles of biotechnology",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a) and (d) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)"],
  why="(d) is the very limitation of hybridisation that genetic engineering overcomes; every other option includes "
      "it.", secs=45)

Z(BPP, "Bioreactors and downstream processing", I, ASR,
  AR("A stirred-tank bioreactor has sampling ports.",
     "Through the sampling ports, fresh medium is continuously added to keep the cells in the lag phase."),
  "Sampling ports of a bioreactor",
  "NCERT: a bioreactor has an agitator system, an oxygen delivery system, a foam control system, a temperature "
  "control system, a pH control system and sampling ports so that small volumes of the culture can be withdrawn "
  "periodically. Sampling ports are for withdrawing culture, and continuous culture keeps cells in the log "
  "(exponential) phase, not the lag phase.",
  ["A: true", "R: false - sampling ports withdraw small volumes; continuous culture targets the log phase"],
  "Obtaining the foreign gene product", ans="C",
  why="R is false, so options A and B are wrong; A is NCERT, so D is wrong.", secs=45)

Z(BPP, "Competent hosts and transformation", I, D,
  "Which of the following gives, in the correct order, the three basic steps in genetically modifying an organism?",
  "Basic steps of genetic modification",
  "NCERT: there are three basic steps in genetically modifying an organism - (i) identification of DNA with "
  "desirable genes; (ii) introduction of the identified DNA into the host; (iii) maintenance of the introduced DNA "
  "in the host and transfer of the DNA to its progeny.",
  ["1: identify the desirable DNA", "2: introduce it into the host", "3: maintain it and pass it to progeny"],
  "Principles of biotechnology",
  at="C", correct="Identification of DNA with desirable genes -> introduction of the identified DNA into the host -> "
                  "maintenance of the introduced DNA in the host and its transfer to the progeny",
  wrong=["Introduction of DNA into the host -> identification of DNA with desirable genes -> maintenance in the "
         "host", "Maintenance of DNA in the host -> identification of DNA with desirable genes -> introduction into "
         "the host", "Identification of DNA with desirable genes -> maintenance in the host -> introduction into the "
         "host"],
  why="A gene must be identified before it can be introduced, and it can be maintained in the host only after it "
      "has been introduced; each wrong option breaks this order.", secs=40)

Z(BPP, "PCR and gel electrophoresis", A, NUM,
  "A PCR starts with a single double-stranded DNA molecule. Every new DNA strand is synthesised by extension of one "
  "primer, and each cycle copies every strand present. After 3 cycles, how many primer molecules have been "
  "incorporated into DNA?",
  "Counting primers in PCR",
  "After n cycles there are 2^n double-stranded molecules, i.e., 2^(n+1) strands. Only the 2 original template "
  "strands were not made by extending a primer; every other strand begins with one primer. For n = 3: 2^4 = 16 "
  "strands, so 16 - 2 = 14 primers are incorporated.",
  ["Molecules after 3 cycles = 2^3 = 8", "Strands = 16", "Strands without a primer = 2 original", "Primers = 16 - 2 = 14"],
  "Amplification of gene of interest using PCR",
  at="D", correct="14",
  wrong=["8", "16", "6"],
  why="8 counts double-stranded molecules, 16 counts all strands including the two original template strands, and "
      "6 assumes only two primers per cycle.", short="Primers used = (2 × number of molecules) - 2.",
  secs=90, vb=RECOMPUTED)

Z(BPP, "Cloning vectors", A, D,
  "Foreign DNA is ligated at the PstI site of pBR322, which lies within the ampicillin resistance gene, and E. coli "
  "is transformed. Which of the following correctly describes the growth of transformants?",
  "Insertional inactivation of the ampicillin resistance gene",
  "Inserting foreign DNA within a gene inactivates it (insertional inactivation). Recombinant plasmids lose "
  "ampicillin resistance but keep the intact tetracycline resistance gene. Non-recombinant plasmids keep both "
  "genes. Untransformed cells have neither resistance.",
  ["Insert in ampR -> ampR inactivated in recombinants", "Recombinants: grow on tetracycline only",
   "Non-recombinant transformants: grow on both"],
  "Cloning vectors",
  at="A", correct="Recombinants grow on tetracycline but not on ampicillin; non-recombinant transformants grow on both",
  wrong=["Recombinants grow on ampicillin but not on tetracycline; non-recombinant transformants grow on neither",
         "Recombinants and non-recombinant transformants both grow on ampicillin and tetracycline",
         "Recombinants grow on neither antibiotic, because the plasmid is destroyed by the insert"],
  why="The first wrong option is the BamHI (tetR) situation reversed; the second ignores insertional inactivation; "
      "the third forgets that the tetracycline resistance gene remains intact.", secs=60)

Z(BPP, "Cloning vectors", A, MAT,
  ML(("problem in recombinant DNA work", "solution described in NCERT"),
     ["Many copies of the target DNA are needed",
      "Bacterial cells cannot take up hydrophilic DNA",
      "Selection by inactivation of an antibiotic resistance gene needs two plates and is cumbersome",
      "Genes have to be delivered into plant cells without causing disease"],
     ["Use the Ti plasmid of Agrobacterium modified into a non-pathogenic cloning vector",
      "Use a marker such as β-galactosidase that gives colour with a chromogenic substrate",
      "Clone it in a vector whose origin of replication supports a high copy number",
      "Treat the cells with a divalent cation such as calcium and give a heat shock"]),
  "Solving practical problems in cloning",
  "If many copies of a target DNA are needed, it should be cloned in a vector whose ori supports a high copy number. "
  "Cells are made competent with divalent cations (Ca2+) and a heat shock. Because antibiotic-gene inactivation "
  "needs replica plating, alternative markers such as β-galactosidase with a chromogenic substrate were developed. "
  "The Ti plasmid of Agrobacterium tumefaciens has been modified into a cloning vector that is no longer pathogenic "
  "to plants.",
  ["A - III (high copy ori)", "B - IV (Ca2+ + heat shock)", "C - II (chromogenic substrate)",
   "D - I (disarmed Ti plasmid)"],
  "Cloning vectors; Competent host (for transformation with recombinant DNA)",
  at="B", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="The other codes give the copy-number problem the calcium treatment, the plant problem the colour marker, or "
      "the selection problem the high-copy vector.", secs=60)

Z(BPP, "Bioreactors and downstream processing", A, STP,
  SP("Downstream processing and quality control testing are the same for every biotechnological product.",
     "A bioreactor has an agitator system, an oxygen delivery system, a foam control system, a temperature control "
     "system and a pH control system."),
  "Downstream processing and bioreactor design",
  "NCERT: strict quality control testing is required for each product, and the downstream processing and quality "
  "control testing vary from product to product. A bioreactor has an agitator system, an oxygen delivery system, a "
  "foam control system, a temperature control system, a pH control system and sampling ports.",
  ["Statement I: false - they vary from product to product", "Statement II: true"],
  "Downstream processing; Obtaining the foreign gene product", ans="D",
  why="Statement I contradicts NCERT, so options A and C are wrong; Statement II is NCERT, so B is wrong.",
  secs=45)

Z(BPP, "Restriction enzymes", A, ASR,
  AR("Normally, the vector and the source DNA must be cut with the same restriction enzyme to create a recombinant "
     "DNA molecule.",
     "DNA fragments cut by the same restriction enzyme have the same kind of sticky ends, which can be joined "
     "end-to-end by DNA ligase."),
  "Why the same enzyme is used",
  "NCERT: when cut by the same restriction enzyme, the resultant DNA fragments have the same kind of sticky ends, "
  "and these can be joined together (end-to-end) using DNA ligase. Normally, unless one cuts the vector and the "
  "source DNA with the same restriction enzyme, the recombinant vector molecule cannot be created.",
  ["A: true", "R: true", "Matching sticky ends (R) are why the same enzyme is needed (A)"],
  "Processes of recombinant DNA technology", ans="A",
  why="R gives the reason for A, so B is wrong; both are NCERT statements, so C and D are wrong.", secs=45)

Z(BPP, "Restriction enzymes", A, MUL,
  MS("Which of the following statements about isolating and joining DNA are correct?",
     ["DNA is enclosed within membranes, so the cell has to be broken open to release it.",
      "When the cell is broken open, DNA is released along with RNA, proteins, polysaccharides and lipids.",
      "Ribonuclease is used to remove the proteins from the DNA preparation.",
      "The cut 'gene of interest' and the cut vector are mixed and DNA ligase is added to prepare recombinant DNA.",
      "DNA ligase cuts DNA at specific recognition sequences."]),
  "Isolation of DNA and ligation",
  "NCERT: since DNA is enclosed within membranes, the cell has to be broken open, releasing DNA along with RNA, "
  "proteins, polysaccharides and lipids. RNA is removed by ribonuclease and proteins by protease. After cutting, the "
  "gene of interest and the cut vector are mixed and ligase is added to give recombinant DNA. Cutting at "
  "recognition sequences is done by restriction enzymes, not ligase.",
  ["(a) True", "(b) True", "(c) False: ribonuclease removes RNA", "(d) True", "(e) False: ligase joins, it does "
   "not cut"],
  "Isolation of the genetic material (DNA); Processes of recombinant DNA technology",
  at="C", correct="(a), (b) and (d) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
  why="(c) gives ribonuclease the job of protease and (e) gives ligase the job of a restriction enzyme; every other "
      "option includes one of them.", secs=60)

# ================================================================ Biotechnology and its Applications (5/6/5)
Z(BTA, "Gene therapy", B, D,
  "According to NCERT, besides enzyme replacement therapy, adenosine deaminase (ADA) deficiency can be cured in "
  "some children by:",
  "Treatments for ADA deficiency",
  "NCERT: in some children ADA deficiency can be cured by bone marrow transplantation; in others it can be treated "
  "by enzyme replacement therapy, in which functional ADA is given by injection. Neither approach is completely "
  "curative.",
  ["Option 1: bone marrow transplantation", "Option 2: enzyme replacement therapy (injection of ADA)"],
  "Gene therapy",
  at="C", correct="Bone marrow transplantation",
  wrong=["Taking insulin at regular intervals", "Spraying Bt toxin", "Removal of the thymus gland"],
  why="Insulin manages diabetes, Bt toxin is an insecticidal protein, and removing the thymus would weaken the "
      "immune system further; none treats ADA deficiency.", secs=25)

Z(BTA, "Human insulin", B, D,
  "In mammals, including humans, insulin is synthesised as a pro-hormone that needs to be processed before it "
  "becomes fully mature and functional. NCERT compares this pro-hormone to a:",
  "Pro-hormone of insulin",
  "NCERT: in mammals, including humans, insulin is synthesised as a pro-hormone (like a pro-enzyme) which needs to "
  "be processed before it becomes a fully mature and functional hormone. The pro-hormone contains an extra stretch "
  "called the C peptide.",
  ["Insulin is first made as a pro-hormone", "Comparison: like a pro-enzyme (inactive precursor)"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="D", correct="Pro-enzyme",
  wrong=["Coenzyme", "Restriction enzyme", "Cofactor"],
  why="A coenzyme and a cofactor are non-protein helpers of enzymes and a restriction enzyme cuts DNA; only a "
      "pro-enzyme is an inactive precursor that must be processed, like pro-insulin.", secs=25)

Z(BTA, "Biosafety, biopiracy and patents", B, D,
  "In the Basmati patent case, the 'new' variety was obtained by crossing Indian Basmati with semi-dwarf varieties. "
  "According to NCERT, this variety was then claimed as:",
  "The Basmati patent",
  "NCERT: the 'new' variety of Basmati had actually been derived from Indian farmers' varieties. Indian Basmati was "
  "crossed with semi-dwarf varieties and claimed as an invention or a novelty.",
  ["Derived from Indian farmers' varieties", "Crossed with semi-dwarf varieties", "Claimed as an invention or "
   "novelty"],
  "Ethical issues",
  at="A", correct="An invention or a novelty",
  wrong=["A traditional Indian farmers' variety", "A transgenic Bt crop", "A variety protected by GEAC"],
  why="The company claimed novelty, not that it was a traditional variety; the variety came from crossing, not "
      "from inserting Bt genes; GEAC is an Indian committee unrelated to the US patent.", secs=30)

Z(BTA, "Bt crops and RNAi", B, D,
  "According to NCERT, several nematodes parasitise a wide variety of:",
  "Nematodes as parasites",
  "NCERT: several nematodes parasitise a wide variety of plants and animals including human beings. Meloidegyne "
  "incognitia infects the roots of tobacco plants and causes a great reduction in yield.",
  ["Nematodes parasitise plants and animals", "Including human beings"],
  "Biotechnological applications in agriculture",
  at="B", correct="Plants and animals, including human beings",
  wrong=["Plants only, never animals", "Bacteria only", "Fungi only"],
  why="NCERT explicitly includes animals and humans among the hosts of nematodes; bacteria and fungi are not "
      "mentioned as hosts.", secs=20)

Z(BTA, "Transgenic animals", B, D,
  "Among the reasons for producing transgenic animals, NCERT says that 'chemical safety testing' is also known as:",
  "Chemical safety testing",
  "NCERT: chemical safety testing is known as toxicity/safety testing. Transgenic animals are made that carry genes "
  "which make them more sensitive to toxic substances than non-transgenic animals.",
  ["Chemical safety testing = toxicity/safety testing"],
  "Transgenic animals",
  at="D", correct="Toxicity/safety testing",
  wrong=["Gene therapy", "Enzyme replacement therapy", "Insertional inactivation"],
  why="Gene therapy and enzyme replacement therapy are treatments of patients, and insertional inactivation is a "
      "method of selecting recombinants.", secs=20)

Z(BTA, "Gene therapy", I, ASR,
  AR("A patient given lymphocyte-based gene therapy for ADA deficiency requires periodic infusions of genetically "
     "engineered lymphocytes.",
     "The genetically engineered lymphocytes are immortal and keep dividing in the patient indefinitely."),
  "Limitation of lymphocyte gene therapy",
  "NCERT: lymphocytes from the patient's blood are grown in culture, a functional ADA cDNA is introduced using a "
  "retroviral vector, and the cells are returned to the patient. As these cells are not immortal, the patient "
  "requires periodic infusion of such genetically engineered lymphocytes. So A is true and R is false.",
  ["A: true", "R: false - the cells are not immortal (that is why infusions are repeated)"],
  "Gene therapy", ans="C",
  why="R is false, so options A and B are wrong; A is NCERT, so D is wrong.", secs=40)

Z(BTA, "Transgenic animals", I, MAT,
  ML(("application", "organism, vector or source used"),
     ["Protecting tobacco against Meloidegyne incognitia", "Gene therapy for ADA deficiency",
      "Insect resistance in cotton", "Production of human α-1-antitrypsin"],
     ["Retroviral vector", "Transgenic animals", "Agrobacterium vectors", "Genes from Bacillus thuringiensis"]),
  "Tools behind biotechnology applications",
  "Nematode-specific genes were introduced into tobacco using Agrobacterium vectors (RNAi). In ADA gene therapy, a "
  "functional ADA cDNA is introduced into lymphocytes using a retroviral vector. Bt cotton carries cry genes from "
  "Bacillus thuringiensis. Transgenic animals have been used to produce human α-1-antitrypsin for emphysema.",
  ["A - III (Agrobacterium)", "B - I (retroviral vector)", "C - IV (B. thuringiensis genes)",
   "D - II (transgenic animals)"],
  "Biotechnological applications in agriculture; Gene therapy; Transgenic animals",
  at="C", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "IV", "B": "I", "C": "III", "D": "II"}]),
  why="The other codes swap the Agrobacterium and retroviral vectors, give antitrypsin production to Bt genes, or "
      "use Bt genes against the nematode.", secs=50)

Z(BTA, "Bt crops and RNAi", I, D,
  "Which of the following shows the correct sequence of events by which the Bt toxin kills an insect?",
  "Mode of action of Bt toxin",
  "The Bt toxin exists as an inactive protoxin. Once the insect ingests it, the alkaline pH of the gut solubilises "
  "the crystals and the toxin becomes active. The activated toxin binds to the surface of midgut epithelial cells "
  "and creates pores, causing swelling and lysis of the cells and eventually the death of the insect.",
  ["Ingestion of protoxin", "Alkaline gut pH solubilises crystals -> active toxin", "Binding to midgut cells -> "
   "pores", "Swelling, lysis -> death"],
  "Biotechnological applications in agriculture",
  at="D", correct="Ingestion of inactive protoxin -> solubilisation by alkaline gut pH and activation -> binding to "
                  "midgut epithelial cells and pore formation -> swelling and lysis of cells -> death of the insect",
  wrong=["Activation in the bacterium -> ingestion by the insect -> pore formation in the exoskeleton -> death",
         "Ingestion of inactive protoxin -> activation by acidic gut pH -> binding to salivary gland cells -> death",
         "Ingestion of inactive protoxin -> binding to midgut cells -> solubilisation by alkaline pH -> activation -> "
         "death"],
  why="The toxin is inactive in the bacterium, it is activated by alkaline (not acidic) pH, and it must be activated "
      "before it binds the midgut cells; each wrong option breaks one of these.", secs=50)

Z(BTA, "Biosafety, biopiracy and patents", I, ASR,
  AR("Going beyond the morality of manipulating living organisms, the biological significance of such "
     "manipulation is also important.",
     "Genetic modification of organisms can have unpredictable results when such organisms are introduced into the "
     "ecosystem."),
  "Biological significance of genetic modification",
  "NCERT: going beyond the morality of such issues, the biological significance of such things is also important. "
  "It explains this at once: genetic modification of organisms can have unpredictable results when such organisms "
  "are introduced into the ecosystem. The possible effect on the ecosystem is exactly the biological significance "
  "that has to be weighed, so R explains A.",
  ["A: true", "R: true", "R names the biological consequence (unpredictable results in the ecosystem) that makes "
   "the biological significance important, so R explains A"],
  "Ethical issues", ans="A",
  why="R is the reason NCERT gives for looking beyond morality to biological significance, so B is wrong; both "
      "statements are NCERT lines, so C and D are wrong.",
  secs=40)

Z(BTA, "Gene therapy", I, STP,
  SP("Both bone marrow transplantation and enzyme replacement therapy are completely curative for ADA deficiency.",
     "In enzyme replacement therapy, functional ADA is given to the patient by injection."),
  "Limits of present treatments for ADA deficiency",
  "NCERT: ADA deficiency can be cured in some children by bone marrow transplantation and treated in others by "
  "enzyme replacement therapy, in which functional ADA is given by injection. But the problem with both these "
  "approaches is that they are not completely curative.",
  ["Statement I: false - neither is completely curative", "Statement II: true"],
  "Gene therapy", ans="D",
  why="Statement I contradicts NCERT, so options A and C are wrong; Statement II is NCERT, so B is wrong.", secs=40)

Z(BTA, "Biosafety, biopiracy and patents", I, MUL,
  MS("Which of the following statements are correct according to NCERT?",
     ["Industrialised (developed) nations are financially rich but poor in biodiversity and traditional knowledge.",
      "The developing and the under-developed world is rich in biodiversity and traditional knowledge related to "
      "bio-resources.",
      "India has very few varieties of rice.",
      "Patents are never granted for products or technologies that use biological resources."]),
  "Biodiversity, traditional knowledge and patents",
  "NCERT: industrialised nations are rich financially but poor in biodiversity and traditional knowledge, whereas "
  "the developing and under-developed world is rich in biodiversity and traditional knowledge. India has about "
  "200,000 varieties of rice. Certain companies have been granted patents for products and technologies that make "
  "use of the genetic materials, plants and other biological resources used by farmers and indigenous people.",
  ["(a) True", "(b) True", "(c) False: India has a very large number of rice varieties",
   "(d) False: such patents have been granted"],
  "Ethical issues",
  at="B", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(c) and (d) only", "(b) and (d) only"],
  why="(c) and (d) contradict NCERT; every other option includes at least one of them.", secs=45)

Z(BTA, "Bt crops and RNAi", A, MUL,
  MS("Which of the following statements about applications of biotechnology are correct?",
     ["In Bt cotton, the proteins encoded by the genes cryIAc and cryIIAb control the cotton bollworms.",
      "Golden rice is enriched in vitamin A.",
      "The transgenic cow Rosie produced milk containing human α-1-antitrypsin.",
      "Transgenic tobacco was protected against Meloidegyne incognitia by the Bt toxin.",
      "Transgenic mice are being developed for use in testing the safety of the polio vaccine."]),
  "Linking products with their details",
  "cryIAc and cryIIAb proteins control cotton bollworms; golden rice is vitamin A-enriched; Rosie's milk contained "
  "human alpha-lactalbumin (α-1-antitrypsin is a different transgenic-animal product, used for emphysema); tobacco "
  "was protected against the nematode by RNA interference, not by Bt toxin; transgenic mice are being developed to "
  "test the safety of the polio vaccine.",
  ["(a) True", "(b) True", "(c) False: alpha-lactalbumin", "(d) False: RNAi", "(e) True"],
  "Biotechnological applications in agriculture; Transgenic animals",
  at="A", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="(c) swaps two transgenic-animal products and (d) swaps RNAi with Bt toxin; every other option includes one "
      "of them.", secs=65)

Z(BTA, "Bt crops and RNAi", A, ASR,
  AR("The choice of Bt toxin genes introduced into a crop depends upon the crop and the targeted pest.",
     "In the bacterium Bacillus thuringiensis, the Bt toxin protein exists as an inactive protoxin."),
  "Choice of cry genes versus protoxin",
  "NCERT: the choice of genes depends upon the crop and the targeted pest, as most Bt toxins are insect-group "
  "specific. Separately, the toxin exists as an inactive protoxin in the bacterium, which is why the bacterium is "
  "not harmed. The protoxin form explains the bacterium's safety, not the choice of genes for a crop.",
  ["A: true (insect-group specificity)", "R: true", "R explains why the bacterium is not killed, not why genes are "
   "chosen per pest"],
  "Biotechnological applications in agriculture", ans="B",
  why="R concerns a different property (the inactive form inside the bacterium), so A is wrong; both are true, so "
      "C and D are wrong.", secs=45)

Z(BTA, "Bt crops and RNAi", A, STP,
  SP("In the RNAi-based protection of tobacco, the introduced DNA produced both sense and anti-sense RNA in the host "
     "cells.",
     "The dsRNA so formed silenced a specific mRNA of the tobacco plant itself."),
  "Target of RNAi in transgenic tobacco",
  "NCERT: nematode-specific genes were introduced into tobacco using Agrobacterium vectors in such a way that both "
  "sense and anti-sense RNA were produced in the host cells. Being complementary, they formed dsRNA that initiated "
  "RNAi and silenced the specific mRNA of the nematode - not of the tobacco plant. The parasite could not survive.",
  ["Statement I: true", "Statement II: false - the nematode's mRNA was silenced"],
  "Biotechnological applications in agriculture", ans="C",
  why="Statement II names the wrong target, so options A and D are wrong; Statement I is NCERT, so B is wrong.",
  secs=45)

Z(BTA, "Biosafety, biopiracy and patents", A, MAT,
  ML(("term", "meaning"),
     ["Genetically modified organisms (GMO)", "Transgenic animals", "Biopiracy", "Patent"],
     ["Right granted by a government to an inventor to prevent others from commercial use of his invention",
      "Use of bio-resources by multinational companies and other organisations without proper authorisation from "
      "the countries and people concerned, and without compensatory payment",
      "Animals whose DNA has been manipulated to possess and express an extra (foreign) gene",
      "Plants, bacteria, fungi and animals whose genes have been altered by manipulation"]),
  "Key terms in biotechnology and its regulation",
  "NCERT: plants, bacteria, fungi and animals whose genes have been altered by manipulation are called GMOs. "
  "Transgenic animals are animals whose DNA has been manipulated to possess and express an extra (foreign) gene. "
  "Biopiracy is the use of bio-resources by multinational companies and other organisations without proper "
  "authorisation and compensatory payment. A patent is the right granted by a government to an inventor to prevent "
  "others from commercial use of his invention.",
  ["A - IV", "B - III", "C - II", "D - I"],
  "Biotechnological applications in agriculture; Transgenic animals; Ethical issues",
  at="C", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The other codes swap GMO with transgenic animals, biopiracy with patent, or transgenic animals with "
      "biopiracy.", secs=50)

Z(BTA, "Human insulin", A, D,
  "Which of the following correctly describes how the American company Eli Lilly produced human insulin by "
  "recombinant DNA technology?",
  "Production of recombinant human insulin",
  "Insulin has two chains, A and B, joined by disulphide bridges, and is made in the body as a pro-hormone with a C "
  "peptide that is removed. Eli Lilly prepared two DNA sequences corresponding to chains A and B and introduced them "
  "into plasmids of E. coli to produce the chains separately; the chains were extracted and combined by creating "
  "disulphide bonds to form human insulin.",
  ["Two DNA sequences: chain A and chain B", "Introduced into E. coli plasmids; chains made separately",
   "Chains combined by disulphide bonds"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="B", correct="DNA sequences for chains A and B were introduced into plasmids of E. coli; the chains were made "
                  "separately, extracted and combined by creating disulphide bonds",
  wrong=["The pro-insulin gene was inserted into Agrobacterium, and the C peptide was retained in the final hormone",
         "Insulin was extracted from the pancreas of slaughtered cattle and pigs and then chemically modified",
         "A single chain was produced in yeast and folded into two chains without any disulphide bonds"],
  why="Mature insulin lacks the C peptide and was made in E. coli, not Agrobacterium; animal pancreas was the older "
      "source that recombinant insulin replaced; the chains are joined by disulphide bonds.", secs=50)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 129
    ids = [x["question_id"] for x in QUESTIONS]
    assert ids[0] == pkg["question_ids"][0] and ids[-1] == pkg["question_ids"][1] and len(set(ids)) == len(ids)
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    assert all(x["subtopic"] in subtopics[x["topic"]] for x in QUESTIONS), \
        [(x["question_id"], x["subtopic"]) for x in QUESTIONS if x["subtopic"] not in subtopics[x["topic"]]]
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_004", "created_at": TODAY,
           "notes": "ZOO_004_p2: 129 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers re-derived in tools/batch_004/ZOO_004_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
