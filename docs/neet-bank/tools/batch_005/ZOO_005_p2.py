"""Builder for package ZOO_005_p2 of BATCH_005 (Zoology, 121 questions, NEET_ZOO_001130..NEET_ZOO_001250).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_005/ZOO_005_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_005_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_005_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_005_ZOO_p2.json"
FIRST_ID = 1130

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
# HR: one spermatogonium -> 3 mitotic divisions -> 2^3 = 8 cells; each becomes a primary spermatocyte and completes
# spermatogenesis (1 primary spermatocyte -> 2 secondary spermatocytes -> 4 spermatids -> 4 sperms)
prim = 2 ** 3
assert prim == 8 and prim * 4 == 32                            # correct: 32 spermatozoa
assert prim * 2 == 16 and 3 * 4 == 12                          # distractors: stopped at secondary spermatocytes; 3 x 4

# EVO: 400 people = 160 AA, 160 Aa, 80 aa; expected heterozygotes at equilibrium with the same allele frequencies
aa_, ab_, bb_ = 160, 160, 80
n_pop = aa_ + ab_ + bb_
p_A = F(2 * aa_ + ab_, 2 * n_pop)
assert n_pop == 400 and p_A == F(3, 5)
exp_het = 2 * p_A * (1 - p_A) * n_pop
assert exp_het == 192 and exp_het > ab_                        # correct: 192 expected; 160 observed -> deficit
assert p_A * (1 - p_A) * n_pop == 96                            # distractor: forgot the factor 2 in 2pq
assert 2 * F(1, 2) * F(1, 2) * n_pop == 200                     # distractor: assumed p = q = 0.5

# EVO: equilibrium, frequency of AA = 0.49 -> individuals carrying at least one a allele = 1 - p^2
pAA = F(49, 100)
p = F(7, 10)
assert p ** 2 == pAA
q = 1 - p
assert 2 * p * q + q ** 2 == 1 - pAA == F(51, 100)             # correct: 0.51
assert 2 * p * q == F(42, 100) and q ** 2 == F(9, 100) and q == F(3, 10)   # distractors: Aa only, aa only, q

# BPP: 12 kb linear DNA, EcoRI sites at 3 kb and 8 kb -> fragments 3, 5 and 4 kb; the smallest moves farthest
cuts = [0, 3, 8, 12]
frags = [b - a for a, b in zip(cuts, cuts[1:])]
assert frags == [3, 5, 4] and min(frags) == 3 and max(frags) == 5

# BPP: PCR from 5 molecules; minimum cycles to reach at least 1000 molecules
start, target = 5, 1000
n_cyc = next(n for n in range(50) if start * 2 ** n >= target)
assert n_cyc == 8 and start * 2 ** 8 == 1280 and start * 2 ** 7 == 640    # 7 cycles are not enough
assert 2 ** 10 >= target and 2 ** 9 < target                              # distractor: ignored the 5 starting molecules

# BPP: EcoRI cuts between G and A on both strands of GAATTC -> 4-nucleotide single-stranded overhang (AATT)
site = "GAATTC"
assert revcomp(site) == site
top_cut = site.index("A")                       # after G on the upper strand (position 1)
bottom_cut = len(site) - 1                       # same G/A junction on the lower strand, read on the upper strand
overhang = site[top_cut:bottom_cut]
assert overhang == "AATT" and len(overhang) == 4
assert revcomp(overhang) == overhang             # the two sticky ends are complementary to each other

# ================================================================ Chemical Coordination and Integration (5/6/5)
Z(CCI, "Mechanism of hormone action", B, D,
  "Endocrine glands release their secretions (hormones) without the help of any duct. For this reason they are "
  "also called:",
  "Endocrine glands are ductless",
  "NCERT: endocrine glands lack ducts and are hence called ductless glands; their secretions are called hormones.",
  ["Endocrine glands have no ducts", "Hence the name: ductless glands"],
  "Endocrine glands and hormones",
  at="B", correct="Ductless glands",
  wrong=["Exocrine glands", "Holocrine glands", "Accessory glands"],
  why="Exocrine glands pour their secretions through ducts; holocrine and accessory glands are not names NCERT "
      "uses for endocrine glands.", secs=20)

Z(CCI, "Mechanism of hormone action", B, D,
  "According to NCERT, how does the endocrine system of invertebrates compare with that of vertebrates?",
  "Endocrine systems of invertebrates and vertebrates",
  "NCERT: invertebrates possess very simple endocrine systems with few hormones, whereas a large number of "
  "chemicals act as hormones and provide coordination in the vertebrates.",
  ["Invertebrates: very simple endocrine systems, few hormones", "Vertebrates: a large number of hormones"],
  "Endocrine glands and hormones",
  at="C", correct="Invertebrates have very simple endocrine systems with few hormones",
  wrong=["Invertebrates have no hormones; all their coordination is neural",
         "Invertebrates have more hormones than vertebrates",
         "Invertebrates and vertebrates have identical endocrine systems"],
  why="NCERT says invertebrates do have hormones, only few of them, and that vertebrates have a large number of "
      "chemicals acting as hormones; so 'no hormones', 'more hormones' and 'identical systems' are all wrong.",
  secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "The secretion of parathyroid hormone (PTH) is regulated by:",
  "Regulation of PTH secretion",
  "NCERT: the secretion of PTH is regulated by the circulating levels of calcium ions. PTH increases the Ca2+ "
  "level in the blood.",
  ["PTH raises blood Ca2+", "Its secretion is regulated by the circulating Ca2+ level"],
  "The parathyroid gland",
  at="B", correct="The circulating levels of calcium ions",
  wrong=["TSH from the anterior pituitary", "Nerve impulses from the hypothalamus",
         "The circulating level of thyroxine"],
  why="TSH regulates the thyroid, not the parathyroids; NCERT names no hypothalamic nerve control or thyroxine "
      "control for PTH - it names the blood calcium level.", secs=25)

Z(CCI, "Hypothalamus and pituitary", B, D,
  "Hormones originating in the hypothalamic neurons are made available for regulating the pituitary because "
  "they:",
  "How hypothalamic hormones are released",
  "NCERT: the hormones originating in the hypothalamic neurons pass through axons and are released from their "
  "nerve endings. They reach the pituitary through a portal circulatory system.",
  ["Made in the hypothalamic neurons", "Pass through axons, released from nerve endings"],
  "The hypothalamus",
  at="D", correct="Pass through axons and are released from the nerve endings",
  wrong=["Are poured into ducts that open into the pituitary", "Are carried to the pituitary by lymph vessels",
         "Are stored in the pineal gland before release"],
  why="The hypothalamus is part of the endocrine (ductless) system, so no ducts are involved; NCERT mentions axons "
      "and a portal circulatory system, not lymph vessels or the pineal gland.", secs=30)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "Insulin lowers the blood glucose level (hypoglycemia) because it:",
  "Why insulin is hypoglycemic",
  "NCERT: insulin acts mainly on hepatocytes and adipocytes and enhances cellular glucose uptake and utilisation. "
  "As a result there is a rapid movement of glucose from blood to hepatocytes and adipocytes, resulting in "
  "decreased blood glucose levels (hypoglycemia).",
  ["Insulin enhances glucose uptake and utilisation", "Glucose moves from blood into liver and fat cells",
   "Blood glucose falls"],
  "Pancreas",
  at="B", correct="Enhances cellular glucose uptake and utilisation, so glucose moves rapidly from blood into "
                  "hepatocytes and adipocytes",
  wrong=["Stimulates glycogenolysis in the hepatocytes", "Stimulates gluconeogenesis in the liver",
         "Reduces the cellular uptake and utilisation of glucose"],
  why="Glycogenolysis, gluconeogenesis and reduced glucose uptake are the actions of glucagon, which raise blood "
      "glucose (hyperglycemia).", secs=30)

Z(CCI, "Hypothalamus and pituitary", I, ASR,
  AR("If the portal circulatory system between the hypothalamus and the pituitary is blocked, the secretion of TSH "
     "and ACTH is affected.",
     "Hypothalamic hormones that regulate the synthesis and secretion of anterior pituitary hormones reach the "
     "pituitary through this portal circulatory system."),
  "Hypothalamic control of the anterior pituitary",
  "TSH and ACTH are made by the pars distalis (anterior pituitary). Their synthesis and secretion are regulated by "
  "hypothalamic hormones, which reach the pituitary through a portal circulatory system and regulate the functions "
  "of the anterior pituitary. Blocking this route removes the hypothalamic regulation, so A is true and R is the "
  "reason.",
  ["TSH, ACTH: anterior pituitary hormones", "Their regulation needs hypothalamic hormones",
   "These hormones travel by the portal system -> R explains A"],
  "The hypothalamus; The pituitary gland", ans="A",
  why="R is the very route whose blockage causes A, so B is wrong; both statements are true, so C and D are wrong.",
  secs=50)

Z(CCI, "Mechanism of hormone action", I, STP,
  SP("Hormone receptors present inside the target cells are mostly nuclear receptors.",
     "Hormones that interact with membrane-bound receptors mostly regulate gene expression through the interaction "
     "of the hormone-receptor complex with the genome."),
  "Membrane-bound versus intracellular receptors",
  "NCERT: receptors present inside the target cell are called intracellular receptors, mostly nuclear receptors. "
  "Hormones that interact with membrane-bound receptors normally do not enter the target cell; they generate "
  "second messengers that regulate cellular metabolism. It is the hormones with intracellular receptors (steroids, "
  "iodothyronines) that mostly regulate gene expression through the genome.",
  ["Statement I: true", "Statement II: false - that is how intracellular-receptor hormones act"],
  "Mechanism of hormone action", ans="C",
  why="Statement II swaps the two mechanisms, so A and D are wrong; Statement I is an NCERT line, so B is wrong.",
  secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("Glucagon acts mainly on hepatocytes, whereas insulin acts mainly on hepatocytes and adipocytes.",
     "Both glucagon and insulin are peptide hormones."),
  "Targets and nature of the pancreatic hormones",
  "NCERT: glucagon is a peptide hormone that acts mainly on the liver cells (hepatocytes). Insulin is a peptide "
  "hormone that acts mainly on hepatocytes and adipocytes (cells of adipose tissue).",
  ["Statement I: true", "Statement II: true"],
  "Pancreas", ans="A",
  why="Both statements are NCERT lines, so every option calling either of them false is wrong.", secs=40)

Z(CCI, "Adrenal, pancreas and gonads", I, MAT,
  ML(("hormone", "cells or tissue that secrete it"),
     ["Glucagon", "Testosterone", "Progesterone (after ovulation)", "Noradrenaline"],
     ["Adrenal medulla", "Corpus luteum",
      "α-cells of the islets of Langerhans", "Leydig cells in the intertubular spaces of the testis"]),
  "Source cells of hormones",
  "Glucagon is secreted by the α-cells of the islets of Langerhans. Testosterone (an androgen) is produced by the "
  "Leydig (interstitial) cells present in the intertubular spaces of the testis. After ovulation the ruptured "
  "follicle becomes the corpus luteum, which secretes mainly progesterone. Noradrenaline is secreted by the "
  "adrenal medulla.",
  ["A - III", "B - IV", "C - II", "D - I"],
  "Pancreas; Testis; Ovary; The adrenal gland",
  at="D", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="The other codes swap glucagon with testosterone, progesterone with noradrenaline, or testosterone with "
      "progesterone.", secs=50)

Z(CCI, "Mechanism of hormone action", I, MUL,
  MS("Which of the following hormones interact with intracellular receptors and mostly regulate gene expression or "
     "chromosome function?",
     ["Cortisol", "Estradiol", "Thyroxine (an iodothyronine)", "Glucagon", "Insulin"]),
  "Hormones acting through intracellular receptors",
  "NCERT: hormones that interact with intracellular receptors (e.g., steroid hormones, iodothyronines) mostly "
  "regulate gene expression or chromosome function. Cortisol and estradiol are steroids and thyroxine is an "
  "iodothyronine. Glucagon and insulin are peptide hormones that bind membrane-bound receptors and act through "
  "second messengers.",
  ["(a) steroid - yes", "(b) steroid - yes", "(c) iodothyronine - yes", "(d), (e) peptide hormones - no"],
  "Mechanism of hormone action",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(d) and (e) only", "(a), (b), (c) and (e) only", "(a) and (b) only"],
  why="Glucagon and insulin act through membrane-bound receptors, so any option including (d) or (e) is wrong; "
      "leaving out thyroxine ignores the iodothyronines that NCERT names.", secs=50)

Z(CCI, "Hormonal disorders", I, ASR,
  AR("A person with exophthalmic goitre shows loss of body weight.",
     "Exophthalmic goitre is a form of hyperthyroidism in which the basal metabolic rate is increased."),
  "Weight loss in Graves' disease",
  "NCERT: exophthalmic goitre (Graves' disease) is a form of hyperthyroidism characterised by enlargement of the "
  "thyroid, protrusion of the eyeballs, increased basal metabolic rate and weight loss. Thyroid hormones regulate "
  "the BMR; an abnormally raised BMR burns body reserves faster, which causes the weight loss.",
  ["A: true (weight loss is a feature)", "R: true (hyperthyroidism, raised BMR)",
   "Raised BMR is what leads to the weight loss -> R explains A"],
  "The thyroid gland", ans="A",
  why="R gives the cause of the weight loss, so B is wrong; both statements are true, so C and D are wrong.",
  secs=45)

Z(CCI, "Adrenal, pancreas and gonads", A, D,
  "A tumour of the adrenal cortex secretes too much aldosterone. Which of the following changes is expected?",
  "Effects of excess aldosterone",
  "NCERT: aldosterone acts mainly at the renal tubules and stimulates the reabsorption of Na+ and water and the "
  "excretion of K+ and phosphate ions. It thus helps maintain electrolytes, body fluid volume, osmotic pressure and "
  "blood pressure. Too much aldosterone therefore increases Na+ and water retention and K+ loss, which raises the "
  "body fluid volume and tends to raise the blood pressure.",
  ["Aldosterone: Na+ and water reabsorbed, K+ excreted", "Excess -> more Na+/water retained, more K+ lost",
   "More fluid volume -> blood pressure tends to rise"],
  "The adrenal gland",
  at="C", correct="Increased reabsorption of Na+ and water and increased excretion of K+, tending to raise the "
                  "blood pressure",
  wrong=["Decreased reabsorption of Na+, loss of water in urine and a fall in blood pressure",
         "Increased reabsorption of K+ and increased excretion of Na+",
         "A fall in blood glucose due to increased glycogenesis"],
  why="The first option is the effect of too little aldosterone; the second reverses the ions; glycogenesis is an "
      "action of insulin, not of a mineralocorticoid.", secs=60)

Z(CCI, "Thyroid, parathyroid and pineal", A, D,
  "During an operation on the thyroid, all four parathyroid glands of a patient are accidentally removed. What "
  "will happen to the blood calcium level, and why?",
  "Consequence of losing PTH",
  "PTH is the hypercalcemic hormone. It stimulates bone resorption (demineralisation), reabsorption of Ca2+ by the "
  "renal tubules and absorption of Ca2+ from digested food. Without the parathyroids none of these is stimulated, "
  "so the blood Ca2+ level falls.",
  ["Parathyroids make PTH", "PTH raises blood Ca2+ by three routes", "Without PTH, blood Ca2+ falls"],
  "The parathyroid gland",
  at="A", correct="It falls, because bone resorption, renal reabsorption and intestinal absorption of Ca2+ are no "
                  "longer stimulated by PTH",
  wrong=["It rises, because thyrocalcitonin can no longer be secreted by the parathyroids",
         "It remains unchanged, because blood calcium is regulated only by the pineal gland",
         "It rises, because bone demineralisation increases"],
  why="Thyrocalcitonin comes from the thyroid, not the parathyroids; the pineal gland does not regulate blood "
      "calcium; bone demineralisation is stimulated by PTH, so it decreases, not increases, without PTH.", secs=60)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("Which of the following hormones tend to raise the glucose concentration of the blood, by the action stated?",
     ["Glucagon, by stimulating glycogenolysis and gluconeogenesis",
      "Adrenaline and noradrenaline, by stimulating the breakdown of glycogen",
      "Glucocorticoids, by stimulating gluconeogenesis",
      "Insulin, by stimulating glycogenesis in its target cells",
      "Aldosterone, by stimulating the reabsorption of glucose in the renal tubules"]),
  "Hormones that raise blood glucose",
  "NCERT: glucagon stimulates glycogenolysis and gluconeogenesis (hyperglycemia); catecholamines stimulate the "
  "breakdown of glycogen, increasing blood glucose; glucocorticoids stimulate gluconeogenesis. Insulin converts "
  "glucose to glycogen and lowers blood glucose. Aldosterone acts on Na+, K+, phosphate and water, not glucose.",
  ["(a) true", "(b) true", "(c) true", "(d) false - insulin lowers blood glucose",
   "(e) false - aldosterone regulates electrolytes and water"],
  "Pancreas; The adrenal gland",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a) and (d) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"],
  why="Insulin is hypoglycemic, and NCERT gives aldosterone no role in glucose handling, so options including (d) "
      "or (e) are wrong.", secs=60)

Z(CCI, "Hormonal disorders", A, MAT,
  ML(("observation in a patient", "most likely cause"),
     ["High blood glucose for a long time, with glucose and ketone bodies in the urine",
      "Enlarged thyroid in a person whose diet is deficient in iodine",
      "Abnormal growth of the body of a child to a very large size",
      "Raised blood Ca2+ with excessive dissolution (demineralisation) of bone"],
     ["Excess secretion of parathyroid hormone", "Hypothyroidism with goitre",
      "Over-secretion of growth hormone", "Diabetes mellitus"]),
  "Linking observations to hormonal causes",
  "Prolonged hyperglycemia with loss of glucose in urine and formation of ketone bodies is diabetes mellitus. "
  "Iodine deficiency causes hypothyroidism and enlargement of the thyroid (goitre). Over-secretion of growth "
  "hormone causes abnormal growth of the body (gigantism). PTH stimulates bone resorption and raises blood Ca2+, so "
  "excess PTH explains raised calcium with bone demineralisation.",
  ["A - IV", "B - II", "C - III", "D - I"],
  "Pancreas; The thyroid gland; The pituitary gland; The parathyroid gland",
  at="B", match=({"A": "IV", "B": "II", "C": "III", "D": "I"},
                 [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"}]),
  why="The other codes give the diabetic picture to goitre, the bone change to growth hormone, or the thyroid "
      "enlargement to growth hormone.", secs=75)

Z(CCI, "Hypothalamus and pituitary", A, STP,
  SP("GnRH and somatostatin, both hypothalamic hormones, reach the pituitary through a portal circulatory system.",
     "In females, FSH induces the ovulation of the fully mature Graafian follicle."),
  "Hypothalamic hormones and gonadotrophin roles",
  "NCERT: GnRH stimulates and somatostatin inhibits pituitary secretion; hypothalamic hormones reach the pituitary "
  "through a portal circulatory system and regulate the anterior pituitary. In females it is LH that induces "
  "ovulation of fully mature (Graafian) follicles and maintains the corpus luteum; FSH stimulates the growth and "
  "development of the ovarian follicles.",
  ["Statement I: true", "Statement II: false - LH, not FSH, induces ovulation"],
  "The hypothalamus; The pituitary gland", ans="C",
  why="Statement II gives LH's role to FSH, so A and D are wrong; Statement I is true, so B is wrong.", secs=50)

# ================================================================ Human Reproduction (6/8/6)
Z(HR, "Male and female reproductive systems", B, D,
  "Which male accessory duct ascends to the abdomen and loops over the urinary bladder?",
  "Course of the vas deferens",
  "NCERT: the epididymis leads to the vas deferens, which ascends to the abdomen and loops over the urinary "
  "bladder. It receives a duct from the seminal vesicle and opens into the urethra as the ejaculatory duct.",
  ["Epididymis -> vas deferens", "Vas deferens ascends to the abdomen and loops over the bladder"],
  "The male reproductive system",
  at="B", correct="Vas deferens",
  wrong=["Vasa efferentia", "Rete testis", "Urethra"],
  why="The rete testis and vasa efferentia lie in and just outside the testis and lead to the epididymis; the "
      "urethra starts from the urinary bladder and runs through the penis.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "The oviduct has three parts after the funnel-shaped infundibulum. The wider part of the oviduct, which lies "
  "between the infundibulum and the isthmus, is the:",
  "Parts of the oviduct",
  "NCERT: the part of the oviduct closer to the ovary is the funnel-shaped infundibulum. It leads to a wider part "
  "of the oviduct called the ampulla. The last part, the isthmus, has a narrow lumen and joins the uterus.",
  ["Infundibulum -> ampulla (wider part) -> isthmus -> uterus"],
  "The female reproductive system",
  at="C", correct="Ampulla",
  wrong=["Fimbriae", "Cervix", "Endometrium"],
  why="Fimbriae are finger-like projections on the edges of the infundibulum; the cervix and the endometrium are "
      "parts of the uterus, not of the oviduct.", secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "According to NCERT, the male sex accessory ducts (rete testis, vasa efferentia, epididymis and vas deferens) "
  "function to:",
  "Role of the male accessory ducts",
  "NCERT: these ducts store and transport the sperms from the testis to the outside through the urethra.",
  ["Accessory ducts: store and transport sperms", "Route ends at the urethra"],
  "The male reproductive system",
  at="D", correct="Store and transport the sperms from the testis to the outside through the urethra",
  wrong=["Produce the sperms by meiosis", "Synthesise and secrete the androgens",
         "Provide nutrition to the germ cells inside the seminiferous tubules"],
  why="Sperms are produced in the seminiferous tubules, androgens by the Leydig cells, and nutrition to germ cells "
      "is provided by the Sertoli cells.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "According to NCERT, the parts of the female reproductive system, together with a pair of mammary glands, are "
  "integrated structurally and functionally to support:",
  "Integration of the female reproductive system",
  "NCERT: the female reproductive system (ovaries, oviducts, uterus, cervix, vagina and external genitalia) along "
  "with a pair of mammary glands is integrated structurally and functionally to support the processes of "
  "ovulation, fertilisation, pregnancy, birth and child care.",
  ["Female system + mammary glands work together",
   "They support ovulation, fertilisation, pregnancy, birth and child care"],
  "The female reproductive system",
  at="A", correct="Ovulation, fertilisation, pregnancy, birth and child care",
  wrong=["Only the production of ova", "Only the secretion of female sex hormones",
         "Spermatogenesis and insemination"],
  why="NCERT lists the whole range of processes, not only ovum or hormone production; spermatogenesis is a male "
      "process.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "The ovaries are the primary female sex organs. Besides producing the female gamete (ovum), they produce several:",
  "Products of the ovary",
  "NCERT: the ovaries are the primary female sex organs that produce the female gamete (ovum) and several steroid "
  "hormones (ovarian hormones).",
  ["Ovary: ovum + steroid (ovarian) hormones"],
  "The female reproductive system",
  at="B", correct="Steroid hormones (ovarian hormones)",
  wrong=["Gonadotropins such as LH and FSH", "Placental hormones such as hCG and hPL",
         "Releasing hormones such as GnRH"],
  why="LH and FSH come from the anterior pituitary, hCG and hPL from the placenta, and GnRH from the hypothalamus.",
  secs=20)

Z(HR, "Gametogenesis", B, NUM,
  "A spermatogonium divides by mitosis three times in succession. Assume that every cell so formed becomes a "
  "primary spermatocyte and completes spermatogenesis normally. How many spermatozoa are formed in all?",
  "Counting the products of spermatogenesis",
  "Three mitotic divisions give 2 x 2 x 2 = 8 cells, all primary spermatocytes. Each primary spermatocyte completes "
  "the first meiotic division to give two secondary spermatocytes, which undergo the second meiotic division to "
  "give four spermatids; each spermatid becomes one spermatozoon by spermiogenesis.",
  ["Mitosis x 3: 2^3 = 8 primary spermatocytes", "Each gives 4 spermatids -> 4 sperms",
   "8 x 4 = 32 spermatozoa"],
  "Gametogenesis",
  at="D", correct="32", wrong=["8", "16", "12"],
  why="8 counts only the primary spermatocytes; 16 stops at the secondary spermatocytes; 12 multiplies the number "
      "of divisions (3) by 4.", short="Sperms = 2^n x 4 for n mitotic divisions.", secs=45, vb=RECOMPUTED)

Z(HR, "Gametogenesis", I, ASR,
  AR("Spermatids are haploid cells.",
     "Spermatids are transformed into spermatozoa by the process called spermiogenesis."),
  "Ploidy of spermatids versus their fate",
  "Spermatids are haploid because they are formed by the second meiotic division of the haploid secondary "
  "spermatocytes (after the first meiotic division halved the chromosome number). R is a true NCERT statement "
  "about what spermatids later become; it says nothing about how their chromosome number was halved.",
  ["A: true (product of meiosis)", "R: true (spermiogenesis)", "R describes their later change, not why they are "
   "haploid"],
  "Gametogenesis", ans="B",
  why="Spermiogenesis changes the shape of the cell, not its chromosome number, so R cannot explain A (option A "
      "wrong); both statements are true, so C and D are wrong.", secs=45)

Z(HR, "Gametogenesis", I, STP,
  SP("Oogenesis is initiated during the embryonic development stage, whereas spermatogenesis begins at puberty.",
     "In the human female, the primary oocyte completes its first meiotic division before birth."),
  "Timing of gametogenesis",
  "NCERT: oogenesis is initiated during the embryonic development stage when oogonia are formed within each fetal "
  "ovary; spermatogenesis begins at puberty. The primary oocytes enter prophase-I and get temporarily arrested; "
  "the first meiotic division is completed only within the tertiary follicle, long after birth.",
  ["Statement I: true", "Statement II: false - meiosis I is completed in the tertiary follicle"],
  "Gametogenesis", ans="C",
  why="Statement II is false, so A and D are wrong; Statement I is an NCERT line, so B is wrong.", secs=45)

Z(HR, "Fertilisation and implantation", I, STP,
  SP("The second polar body is formed only after a sperm enters the secondary oocyte.",
     "The zygote formed by the fusion of the haploid nuclei of the sperm and the ovum is diploid."),
  "Completion of meiosis and the zygote",
  "NCERT: entry of the sperm induces completion of the meiotic division of the secondary oocyte; this second "
  "meiotic division is unequal and gives a second polar body and a haploid ovum (ootid). The haploid nuclei of the "
  "sperm and the ovum then fuse to form a diploid zygote.",
  ["Statement I: true (sperm entry triggers meiosis II)", "Statement II: true (n + n = 2n)"],
  "Fertilisation and implantation", ans="A",
  why="Both statements are true, so every option calling either of them false is wrong.", secs=40)

Z(HR, "Menstrual cycle", I, MAT,
  ML(("phase or time of the cycle", "hormonal event"),
     ["Follicular phase", "Middle of the cycle (about the 14th day)", "Luteal phase",
      "Menstrual phase of the next cycle (no fertilisation)"],
     ["Rapid secretion of LH (LH surge)", "Large amounts of progesterone secreted by the corpus luteum",
      "Rising secretion of estrogens by the growing follicles",
      "The corpus luteum has degenerated and the endometrium disintegrates"]),
  "Hormones across the menstrual cycle",
  "During the follicular phase the gonadotropins rise gradually and stimulate the growing follicles to secrete "
  "estrogens. LH and FSH peak in the middle of the cycle; the rapid secretion of LH (LH surge) induces ovulation. "
  "In the luteal phase the corpus luteum secretes large amounts of progesterone. Without fertilisation the corpus "
  "luteum degenerates, the endometrium disintegrates and menstruation follows.",
  ["A - III", "B - I", "C - II", "D - IV"],
  "Menstrual cycle",
  at="A", match=({"A": "III", "B": "I", "C": "II", "D": "IV"},
                 [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"}]),
  why="The other codes put the LH surge in the follicular phase, place corpus luteum degeneration in the luteal "
      "phase, or give the corpus luteum's progesterone to the follicular phase.", secs=55)

Z(HR, "Male and female reproductive systems", I, MUL,
  MS("Which of the following statements about the human female reproductive system are correct?",
     ["The ovaries are located one on each side of the lower abdomen.",
      "The oviducts extend from the periphery of each ovary to the uterus.",
      "The uterus is supported by ligaments attached to the pelvic wall.",
      "The cavity of the cervix (cervical canal), along with the vagina, forms the birth canal.",
      "The fimbriae are finger-like projections on the edges of the isthmus."]),
  "Organisation of the female reproductive system",
  "NCERT: ovaries are located one on each side of the lower abdomen; the oviducts extend from the periphery of each "
  "ovary to the uterus; the uterus is supported by ligaments attached to the pelvic wall; the cervical canal with "
  "the vagina forms the birth canal. The fimbriae are on the edges of the infundibulum, the funnel-shaped part "
  "nearest the ovary, not on the isthmus.",
  ["(a), (b), (c), (d): true", "(e) false - fimbriae belong to the infundibulum"],
  "The female reproductive system",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(b), (c), (d) and (e) only", "(a) and (d) only"],
  why="Any option containing (e) is wrong; (a) and (d) only leaves out the true statements (b) and (c).", secs=55)

Z(HR, "Pregnancy, parturition and lactation", I, MUL,
  MS("Which of the following statements about pregnancy are correct?",
     ["After implantation, finger-like projections called chorionic villi appear on the trophoblast.",
      "The placenta facilitates the supply of oxygen and nutrients to the embryo.",
      "hCG, hPL and relaxin are produced in women only during pregnancy.",
      "The placenta is formed entirely by the tissues of the embryo.",
      "The oxytocin that causes the uterine contractions of parturition is secreted by the placenta."]),
  "Placenta and hormones of pregnancy",
  "NCERT: after implantation, chorionic villi appear on the trophoblast; the villi and the uterine tissue become "
  "interdigitated and jointly form the placenta, a structural and functional unit between the embryo and the "
  "mother. The placenta supplies oxygen and nutrients. hCG, hPL and relaxin are produced only during pregnancy. "
  "Oxytocin that acts on the uterine muscle at parturition is released from the maternal pituitary.",
  ["(a) true", "(b) true", "(c) true", "(d) false - placenta is formed jointly with uterine tissue",
   "(e) false - oxytocin comes from the maternal pituitary"],
  "Pregnancy and embryonic development; Parturition and lactation",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="The placenta is formed jointly by the chorionic villi and uterine tissue, and oxytocin is a maternal "
      "pituitary hormone, so options with (d) or (e) are wrong.", secs=55)

Z(HR, "Fertilisation and implantation", I, D,
  "An ovum is released at ovulation, but no sperms reach the ampullary region while the ovum is there. According "
  "to NCERT, which of the following follows?",
  "Consequence of absence of fertilisation",
  "Fertilisation can occur only if the ovum and sperms are transported simultaneously to the ampullary region. If "
  "it does not occur, the corpus luteum degenerates; this causes disintegration of the endometrium, leading to "
  "menstruation and marking a new cycle.",
  ["No sperm at the ampulla -> no fertilisation", "Corpus luteum degenerates", "Endometrium disintegrates -> "
   "menstruation"],
  "Fertilisation and implantation; Menstrual cycle",
  at="D", correct="Fertilisation does not take place; the corpus luteum degenerates and menstruation follows",
  wrong=["The ovum develops into an embryo without fertilisation",
         "The ovum is fertilised later in the uterus during the next cycle",
         "The corpus luteum persists and the woman stops menstruating"],
  why="Human ova do not develop without fertilisation; fertilisation takes place in the ampullary region, not in "
      "the uterus; the corpus luteum is maintained, and menstruation stops, only if pregnancy occurs.", secs=40)

Z(HR, "Male and female reproductive systems", I, ASR,
  AR("The endometrium of the uterus remains unchanged throughout the menstrual cycle.",
     "The endometrium is the inner glandular layer that lines the uterine cavity."),
  "Endometrium and the menstrual cycle",
  "NCERT: the wall of the uterus has three layers; the inner glandular layer, the endometrium, lines the uterine "
  "cavity and undergoes cyclical changes during the menstrual cycle (it regenerates in the follicular phase, is "
  "maintained in the luteal phase and breaks down at menstruation). So A is false and R is true.",
  ["A: false - the endometrium changes cyclically", "R: true"],
  "The female reproductive system", ans="D",
  why="A is false, so options A, B and C (which call A true) are wrong.", secs=35)

Z(HR, "Gametogenesis", A, MUL,
  MS("Which of the following statements comparing spermatogenesis and oogenesis in humans are correct?",
     ["Both processes involve the first and the second meiotic divisions.",
      "A primary spermatocyte gives rise to four spermatozoa, whereas a primary oocyte gives rise to only one large "
      "functional female gamete.",
      "The first meiotic division is equal in spermatogenesis but unequal in oogenesis.",
      "Both spermatogonia and oogonia are haploid cells.",
      "New oogonia continue to be formed in the ovary throughout the reproductive life of a woman."]),
  "Spermatogenesis versus oogenesis",
  "In spermatogenesis a primary spermatocyte completes meiosis I to give two equal haploid secondary spermatocytes, "
  "which give four spermatids and hence four sperms. In oogenesis meiosis I is unequal (large secondary oocyte and "
  "tiny first polar body) and meiosis II is also unequal (ootid and second polar body), so one functional gamete "
  "results. Spermatogonia (46 chromosomes) and oogonia are diploid. No more oogonia are formed or added after "
  "birth.",
  ["(a) true", "(b) true", "(c) true", "(d) false - gonia are diploid", "(e) false - no oogonia after birth"],
  "Gametogenesis",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"],
  why="Gonia are diploid and no oogonia are added after birth, so options with (d) or (e) are wrong.", secs=70)

Z(HR, "Menstrual cycle", A, ASR,
  AR("If the corpus luteum is removed soon after ovulation, the endometrium is likely to break down.",
     "Progesterone secreted by the corpus luteum is essential for the maintenance of the endometrium."),
  "Dependence of the endometrium on the corpus luteum",
  "In the luteal phase the corpus luteum secretes large amounts of progesterone, which is essential for maintaining "
  "the endometrium. NCERT notes that when the corpus luteum degenerates (no fertilisation) the endometrium "
  "disintegrates. Removing it has the same effect, and R gives the reason.",
  ["Corpus luteum -> progesterone", "Progesterone maintains endometrium", "No corpus luteum -> no progesterone -> "
   "endometrium breaks down; R explains A"],
  "Menstrual cycle", ans="A",
  why="R is the direct cause of A, so B is wrong; both statements are true, so C and D are wrong.", secs=50)

Z(HR, "Male and female reproductive systems", A, D,
  "In a man, all the vasa efferentia of each testis are completely blocked, but the seminiferous tubules and all the "
  "accessory glands are normal. Which of the following is expected?",
  "Applying the path of sperms",
  "Sperms formed in the seminiferous tubules pass through the rete testis and vasa efferentia to the epididymis and "
  "vas deferens. A block at the vasa efferentia stops sperms before the epididymis. Seminal plasma, however, comes "
  "from the accessory glands (seminal vesicles, prostate, bulbourethral glands), which are normal, so an ejaculate "
  "is still formed but lacks sperms.",
  ["Path: tubules -> rete testis -> vasa efferentia -> epididymis", "Block -> sperms cannot reach the epididymis",
   "Accessory glands normal -> seminal plasma still formed"],
  "The male reproductive system",
  at="C", correct="Sperms are formed but cannot reach the epididymis, so the ejaculate lacks sperms though seminal "
                  "plasma is still produced",
  wrong=["No sperms are formed at all, because the seminiferous tubules cannot function",
         "Sperms reach the urethra normally through the rete testis",
         "No semen of any kind is ejaculated, because seminal plasma is made in the testis"],
  why="Spermatogenesis in the tubules is unaffected; the rete testis lies before the vasa efferentia, so sperms "
      "cannot bypass the block; seminal plasma comes from the accessory glands, not the testis.", secs=60)

Z(HR, "Fertilisation and implantation", A, MAT,
  ML(("structure in the early embryo", "fate or role"),
     ["Trophoblast", "Inner cell mass", "Ectoderm, mesoderm and endoderm",
      "Chorionic villi interdigitated with uterine tissue"],
     ["Placenta", "Gets attached to the endometrium; chorionic villi later appear on it",
      "Give rise to all tissues (organs) in adults",
      "Differentiates into an outer ectoderm and an inner endoderm soon after implantation"]),
  "Fates of early embryonic structures",
  "The blastomeres of the blastocyst form an outer trophoblast, which attaches to the endometrium and on which "
  "chorionic villi appear, and an inner cell mass. Immediately after implantation the inner cell mass "
  "differentiates into an outer ectoderm and an inner endoderm; a mesoderm soon appears between them. The three "
  "layers give rise to all tissues (organs) in adults. Chorionic villi and uterine tissue become interdigitated "
  "and jointly form the placenta.",
  ["A - II", "B - IV", "C - III", "D - I"],
  "Fertilisation and implantation; Pregnancy and embryonic development",
  at="C", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The other codes swap the trophoblast with the inner cell mass, the inner cell mass with the germ layers, or "
      "the trophoblast with the placenta.", secs=70)

Z(HR, "Gametogenesis", A, STP,
  SP("The oocyte present in a Graafian follicle is a secondary oocyte.",
     "The secondary oocyte completes its second meiotic division before ovulation."),
  "Stage of the female gamete at ovulation",
  "NCERT: the primary oocyte within the tertiary follicle completes the first meiotic division, giving a secondary "
  "oocyte; the tertiary follicle changes into the mature Graafian follicle, in which the secondary oocyte forms a "
  "zona pellucida. The secondary oocyte is released at ovulation, and its meiotic division is completed only "
  "after a sperm enters it.",
  ["Statement I: true", "Statement II: false - meiosis II is completed only after sperm entry"],
  "Gametogenesis; Fertilisation and implantation", ans="C",
  why="Statement II is false, so A and D are wrong; Statement I is true, so B is wrong.", secs=50)

Z(HR, "Menstrual cycle", A, MUL,
  MS("A woman has regular menstrual cycles of 28 days. Which of the following statements are correct for her?",
     ["Ovulation is expected around the 14th day of the cycle.",
      "LH and FSH reach their peak levels around the middle of the cycle.",
      "If the ovum is fertilised and pregnancy follows, menstruation will not occur.",
      "Her menstrual flow is expected to last about 10 to 12 days.",
      "During the follicular phase, estrogens are secreted mainly by the corpus luteum."]),
  "Applying the events of a 28-day cycle",
  "In the middle of the cycle (about the 14th day) LH and FSH reach a peak; the LH surge induces ovulation. During "
  "pregnancy all events of the menstrual cycle stop and there is no menstruation. The menstrual flow lasts for "
  "3-5 days. In the follicular phase estrogens come from the growing follicles; the corpus luteum forms only after "
  "ovulation.",
  ["(a) true", "(b) true", "(c) true", "(d) false - 3 to 5 days", "(e) false - growing follicles secrete estrogens"],
  "Menstrual cycle",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (e) only"],
  why="The flow lasts 3-5 days and the corpus luteum does not exist in the follicular phase, so options with (d) or "
      "(e) are wrong.", secs=60)

# ================================================================ Reproductive Health (4/6/4)
Z(RH, "Contraception", B, D,
  "In tubectomy, a small part of the fallopian tube is removed or tied up through:",
  "Procedure of tubectomy",
  "NCERT: in tubectomy, a small part of the fallopian tube is removed or tied up through a small incision in the "
  "abdomen or through the vagina. (In vasectomy the incision is on the scrotum.)",
  ["Tubectomy: female sterilisation", "Access: small incision in the abdomen, or through the vagina"],
  "Population stabilisation and birth control",
  at="B", correct="A small incision in the abdomen or through the vagina",
  wrong=["A small incision on the scrotum", "A device inserted into the uterus through the vagina",
         "Removal of both ovaries"],
  why="The scrotal incision is for vasectomy; a device placed in the uterus is an IUD; tubectomy does not remove "
      "the ovaries.", secs=25)

Z(RH, "Contraception", B, D,
  "In the 'lactational amenorrhea' method of contraception, the word 'amenorrhea' refers to:",
  "Meaning of lactational amenorrhea",
  "NCERT: lactational amenorrhea means absence of menstruation during the period of intense lactation following "
  "parturition. Since ovulation and therefore the cycle do not occur, the chances of conception are almost nil as "
  "long as the mother breast-feeds the child fully.",
  ["Lactational = during breast-feeding", "Amenorrhea = absence of menstruation"],
  "Population stabilisation and birth control",
  at="C", correct="Absence of menstruation", wrong=["Absence of milk secretion",
                                                    "Failure of the ovum to be fertilised",
                                                    "Painful menstruation"],
  why="Milk is being secreted in this period (that is the point of the method); 'amenorrhea' is about menstruation, "
      "not about fertilisation or pain.", secs=20)

Z(RH, "Infertility and ART", B, D,
  "According to NCERT, which of the following could help in the diagnosis and corrective treatment of some of the "
  "disorders that cause infertility?",
  "Infertility clinics",
  "NCERT: specialised health care units (infertility clinics, etc.) could help in diagnosis and corrective "
  "treatment of some of these disorders and enable couples to have children; where correction is not possible, ART "
  "can help.",
  ["Infertility: physical, congenital, disease, drugs, immunological or psychological causes",
   "Specialised units (infertility clinics) diagnose and correct some"],
  "Infertility",
  at="B", correct="Specialised health care units such as infertility clinics",
  wrong=["Sterilisation procedures such as vasectomy", "Use of intra-uterine devices",
         "Medical termination of pregnancy"],
  why="Vasectomy, IUDs and MTP prevent or end pregnancy; they do not treat infertility.", secs=20)

Z(RH, "MTP and amniocentesis", B, D,
  "Amniocentesis, a foetal sex determination test whose misuse NCERT warns against, is based on the chromosomal "
  "pattern in the:",
  "Sample used in amniocentesis",
  "NCERT describes amniocentesis as a foetal sex determination test based on the chromosomal pattern in the "
  "amniotic fluid surrounding the developing embryo.",
  ["Amniocentesis samples the amniotic fluid", "Chromosomal pattern is examined"],
  "Reproductive health - problems and strategies; Medical termination of pregnancy (MTP)",
  at="D", correct="Amniotic fluid surrounding the developing embryo",
  wrong=["Urine of the mother", "Cervical mucus of the mother", "Milk secreted after parturition"],
  why="None of the maternal fluids listed is the sample; the test uses the amniotic fluid around the embryo.",
  secs=20)

Z(RH, "Contraception", I, ASR,
  AR("Vasectomy prevents the transport of sperms.",
     "In vasectomy, a small part of the fallopian tube is removed or tied up."),
  "Vasectomy versus tubectomy",
  "In vasectomy, a small part of the vas deferens is removed or tied up through a small incision on the scrotum, "
  "which blocks the transport of sperms. Removing or tying the fallopian tube is tubectomy, the female procedure. "
  "A is true and R is false.",
  ["A: true", "R: false - fallopian tube = tubectomy"],
  "Population stabilisation and birth control", ans="C",
  why="R is false, so options A, B and D (which call R true) are wrong.", secs=30)

Z(RH, "Contraception", I, STP,
  SP("Vasectomy and tubectomy both prevent conception by blocking gamete transport.",
     "Lactational amenorrhea and periodic abstinence are both barrier methods of contraception."),
  "Classifying contraceptive methods",
  "NCERT: sterilisation procedures (vasectomy in males, tubectomy in females) block gamete transport and thereby "
  "prevent conception. Periodic abstinence and lactational amenorrhea are natural methods; barrier methods are "
  "condoms, diaphragms, cervical caps and vaults.",
  ["Statement I: true", "Statement II: false - both are natural methods"],
  "Population stabilisation and birth control", ans="C",
  why="Statement II mislabels natural methods as barrier methods, so A and D are wrong; Statement I is true, so B "
      "is wrong.", secs=40)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive method", "part of the reproductive system where it acts"),
     ["Vasectomy", "Tubectomy", "Cervical cap", "Intra-uterine device (IUD)"],
     ["Uterus", "Vas deferens", "Fallopian tube", "Cervix"]),
  "Site of action of contraceptives",
  "In vasectomy a small part of the vas deferens is removed or tied up; in tubectomy a small part of the fallopian "
  "tube is removed or tied up. Diaphragms, cervical caps and vaults are barriers that cover the cervix during "
  "coitus. IUDs are inserted by doctors or expert nurses in the uterus through the vagina.",
  ["A - II", "B - III", "C - IV", "D - I"],
  "Population stabilisation and birth control",
  at="B", match=({"A": "II", "B": "III", "C": "IV", "D": "I"},
                 [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="The other codes swap the two sterilisation sites, place the cap in the uterus and the IUD on the cervix, or "
      "put the cap on the fallopian tube.", secs=45)

Z(RH, "Infertility and ART", I, MUL,
  MS("In which of the following assisted reproductive technologies is the gamete or the early embryo transferred "
     "into the fallopian tube?",
     ["Zygote intra fallopian transfer (ZIFT)", "Gamete intra fallopian transfer (GIFT)",
      "Intra uterine transfer (IUT)", "Intra-uterine insemination (IUI)",
      "Intra cytoplasmic sperm injection (ICSI)"]),
  "Site of transfer in ART",
  "ZIFT: the zygote or early embryo (up to 8 blastomeres) is transferred into the fallopian tube. GIFT: an ovum "
  "collected from a donor is transferred into the fallopian tube of a female who cannot produce one. IUT transfers "
  "embryos with more than 8 blastomeres into the uterus; IUI introduces semen into the uterus; in ICSI a sperm is "
  "injected directly into the ovum in the laboratory.",
  ["(a) fallopian tube", "(b) fallopian tube", "(c), (d) uterus", "(e) ovum in the laboratory"],
  "Infertility",
  at="A", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(c) and (d) only", "(a), (b) and (e) only"],
  why="IUT and IUI use the uterus and ICSI is done on the ovum in the laboratory, so options including (c), (d) or "
      "(e) are wrong.", secs=45)

Z(RH, "STDs and their prevention", I, D,
  "NCERT lists some simple principles for preventing STIs. Which of the following is NOT one of them, and would "
  "not protect against STIs?",
  "Preventing STIs",
  "NCERT's simple principles: avoid sex with unknown partners or multiple partners; always use condoms during "
  "coitus; in case of doubt, go to a qualified doctor for early detection and get complete treatment. Oral pills "
  "act by inhibiting ovulation and implantation and give no barrier against infection.",
  ["Principles: avoid unknown/multiple partners, always use condoms, consult a qualified doctor early",
   "Oral pills prevent conception, not infection"],
  "Sexually transmitted infections (STIs)",
  at="A", correct="Regularly taking oral contraceptive pills",
  wrong=["Avoiding sex with unknown partners or multiple partners", "Always using condoms during coitus",
         "Going to a qualified doctor for early detection and complete treatment in case of doubt"],
  why="The other three are the principles NCERT lists; pills are not among them because they do not block the "
      "transmission of pathogens.", secs=35)

Z(RH, "Infertility and ART", I, STP,
  SP("In vitro fertilisation means fertilisation that takes place inside the female body.",
     "Embryos formed in vitro that have more than 8 blastomeres can be transferred into the uterus (IUT)."),
  "In vitro fertilisation and IUT",
  "NCERT: in vitro fertilisation (IVF) is fertilisation outside the body in almost similar conditions as that in "
  "the body; fertilisation within the female is in vivo. Embryos with more than 8 blastomeres are transferred into "
  "the uterus by IUT.",
  ["Statement I: false - in vitro = outside the body", "Statement II: true"],
  "Infertility", ans="D",
  why="Statement I describes in vivo, not in vitro, fertilisation, so A and C are wrong; Statement II is true, so B "
      "is wrong.", secs=40)

Z(RH, "Infertility and ART", A, D,
  "A woman produces normal ova and has a normal uterus, but both her fallopian tubes are blocked. Which of the "
  "following assisted reproductive techniques is suitable for her, since it does not depend on the fallopian "
  "tubes?",
  "Choosing an ART",
  "With both tubes blocked, gametes or embryos placed in the tube cannot reach the uterus, and sperms placed in the "
  "uterus cannot reach the ovum. The ova can be collected, fertilised in the laboratory (IVF), and the embryo with "
  "more than 8 blastomeres transferred directly into the uterus (IUT).",
  ["GIFT and ZIFT place material into the fallopian tube", "IUI needs sperms to meet the ovum in the tube",
   "IVF + IUT bypasses the tubes"],
  "Infertility",
  at="B", correct="In vitro fertilisation followed by intra uterine transfer (IUT) of the embryo",
  wrong=["Gamete intra fallopian transfer (GIFT)", "Zygote intra fallopian transfer (ZIFT)",
         "Intra-uterine insemination (IUI) with the husband's semen"],
  why="GIFT and ZIFT transfer into the blocked fallopian tube; in IUI the sperms still have to travel up the "
      "blocked tubes to meet the ovum.", secs=60)

Z(RH, "STDs and their prevention", A, ASR,
  AR("Condoms protect the user from STIs, whereas oral contraceptive pills do not.",
     "A condom is a barrier that prevents the ejaculated semen from entering the female reproductive tract, whereas "
     "oral pills act by inhibiting ovulation and implantation."),
  "Why only barrier methods protect against STIs",
  "NCERT: condoms are barriers that prevent the deposition of ejaculated semen into the female reproductive tract, "
  "and they protect the user from STIs and AIDS. Oral pills inhibit ovulation and implantation and alter the "
  "cervical mucus; they set up no physical barrier between partners, so they give no protection against STIs. R "
  "therefore explains A.",
  ["A: true", "R: true", "Barrier vs hormonal mode of action explains the difference"],
  "Population stabilisation and birth control; Sexually transmitted infections (STIs)", ans="A",
  why="R gives the reason for the difference stated in A, so B is wrong; both are true, so C and D are wrong.",
  secs=50)

Z(RH, "Contraception", A, MAT,
  ML(("method", "how it prevents conception"),
     ["Oral pills", "Hormone-releasing IUD", "Periodic abstinence", "Lactational amenorrhea"],
     ["Ovulation does not occur during the period of intense lactation",
      "Coitus is avoided from day 10 to 17 of the cycle, when ovulation could be expected",
      "Make the uterus unsuitable for implantation and the cervix hostile to sperms",
      "Inhibit ovulation and implantation and alter the quality of cervical mucus"]),
  "Modes of action of contraceptives",
  "Oral pills inhibit ovulation and implantation and alter the quality of the cervical mucus. Hormone-releasing "
  "IUDs make the uterus unsuitable for implantation and the cervix hostile to sperms. In periodic abstinence the "
  "couple avoids coitus from day 10 to 17, when ovulation could be expected. In lactational amenorrhea, ovulation "
  "does not occur during intense lactation.",
  ["A - IV", "B - III", "C - II", "D - I"],
  "Population stabilisation and birth control",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The other codes swap pills with hormonal IUDs, the two natural methods with each other, or the hormonal IUD "
      "with periodic abstinence.", secs=60)

Z(RH, "Contraception", A, MUL,
  MS("A couple wants to space their children and may wish to have another child later. Which of the following "
     "methods suit them, being reversible rather than terminal?",
     ["Intra-uterine device (IUD)", "Oral contraceptive pills", "Condoms", "Vasectomy", "Tubectomy"]),
  "Reversible versus terminal methods",
  "NCERT: an ideal contraceptive should be reversible. IUDs (ideal for delaying pregnancy and/or spacing "
  "children), oral pills and condoms are reversible. Surgical methods (vasectomy, tubectomy) are advised as a "
  "terminal method to prevent any more pregnancies, because their reversibility is very poor.",
  ["(a), (b), (c): reversible", "(d), (e): sterilisation, very poor reversibility -> terminal"],
  "Population stabilisation and birth control",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(d) and (e) only", "(a), (b), (c) and (d) only", "(c) and (e) only"],
  why="Vasectomy and tubectomy are terminal methods with very poor reversibility, so options including (d) or (e) "
      "are wrong.", secs=45)

# ================================================================ Evolution (5/7/5)
Z(EVO, "Origin of life", B, D,
  "Oparin and Haldane proposed that the first form of life could have come from pre-existing non-living organic "
  "molecules. According to NCERT, these two scientists were from:",
  "Proponents of chemical evolution",
  "NCERT: Oparin of Russia and Haldane of England proposed that the first form of life could have come from "
  "pre-existing non-living organic molecules (e.g., RNA, protein) and that formation of life was preceded by "
  "chemical evolution.",
  ["Oparin - Russia", "Haldane - England"],
  "Origin of life",
  at="B", correct="Russia and England, respectively", wrong=["England and Russia, respectively",
                                                             "America and England, respectively",
                                                             "Russia and America, respectively"],
  why="The order is Oparin (Russia), Haldane (England); America is associated with S.L. Miller, not with them.",
  secs=20)

Z(EVO, "Origin of life", B, D,
  "According to NCERT, the first non-cellular forms of life, which could have originated about 3 billion years "
  "back, would have been:",
  "First non-cellular forms of life",
  "NCERT: the first non-cellular forms of life could have originated 3 billion years back. They would have been "
  "giant molecules (RNA, protein, polysaccharides, etc.). These capsules reproduced their molecules perhaps. The "
  "first cellular forms did not originate till about 2000 mya.",
  ["Non-cellular forms: giant molecules", "RNA, protein, polysaccharides"],
  "Origin of life",
  at="C", correct="Giant molecules such as RNA, proteins and polysaccharides",
  wrong=["Single cells enclosed by membranes", "Multicellular organisms living on land",
         "Spore-forming fungi that arrived from other planets"],
  why="Cells came later (about 2000 mya); multicellular land forms came much later still; spores from other planets "
      "belong to the panspermia idea, not to the non-cellular forms NCERT describes.", secs=25)

Z(EVO, "Evidences of evolution", B, D,
  "Which evidence of evolution is based on studying the similarities and differences in structure among organisms "
  "of today and those that existed years ago, to infer whether they shared common ancestors?",
  "Comparative anatomy and morphology",
  "NCERT: comparative anatomy and morphology shows similarities and differences among organisms of today and "
  "those that existed years ago. Such similarities can be interpreted to understand whether common ancestors were "
  "shared or not.",
  ["Compares structure (anatomy, morphology)", "Of present and past organisms", "Infers common ancestry"],
  "Evidences for evolution",
  at="B", correct="Comparative anatomy and morphology",
  wrong=["Industrial melanism", "Panspermia", "Spontaneous generation"],
  why="Industrial melanism is evidence for natural selection in action; panspermia and spontaneous generation are "
      "ideas about the origin of life, not evidences from structure.", secs=25)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a. The frequency of the AA "
  "genotype is 0.49. What fraction of the individuals carry at least one copy of allele a?",
  "Genotype frequencies at equilibrium",
  "Individuals with at least one a allele are Aa and aa, i.e., everyone except AA. Since p^2 + 2pq + q^2 = 1, their "
  "frequency is 1 - p^2 = 1 - 0.49 = 0.51. (Check: p = 0.7, q = 0.3; 2pq = 0.42, q^2 = 0.09; 0.42 + 0.09 = 0.51.)",
  ["Carriers of a = Aa + aa = 1 - AA", "1 - 0.49 = 0.51", "Check: 0.42 + 0.09 = 0.51"],
  "Hardy-Weinberg principle",
  at="D", correct="0.51", wrong=["0.42", "0.09", "0.30"],
  why="0.42 counts only heterozygotes; 0.09 counts only aa; 0.30 is the allele frequency q, not a genotype "
      "frequency.", short="Everyone who is not AA carries a: 1 - p^2.", secs=45, vb=RECOMPUTED)

Z(EVO, "Origin of life", B, D,
  "According to NCERT, Louis Pasteur's careful experiments with killed yeast in pre-sterilised flasks demonstrated "
  "that:",
  "Pasteur and the origin of life",
  "NCERT: Louis Pasteur by careful experimentation demonstrated that life comes only from pre-existing life. In "
  "pre-sterilised flasks, life did not come from killed yeast, while in a flask open to air new living organisms "
  "arose. This dismissed spontaneous generation.",
  ["Sterilised flask: no life from killed yeast", "Conclusion: life comes only from pre-existing life"],
  "Origin of life",
  at="C", correct="Life comes only from pre-existing life",
  wrong=["Life arises from decaying and rotting matter like straw and mud",
         "Life came to earth as spores from other planets",
         "Amino acids form when electric discharge is passed through a mixture of gases"],
  why="The first option is spontaneous generation, which Pasteur disproved; the second is panspermia; the last is "
      "Miller's experiment.", secs=25)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, ASR,
  AR("According to the Hardy-Weinberg principle, allele frequencies in a population change in every generation even "
     "when no disturbing factor acts.",
     "Gene migration (gene flow), genetic drift, mutation, genetic recombination and natural selection are factors "
     "that affect Hardy-Weinberg equilibrium."),
  "Hardy-Weinberg principle and its disturbing factors",
  "NCERT: the Hardy-Weinberg principle says that allele frequencies in a population are stable and constant from "
  "generation to generation unless disturbed. Five factors affect this equilibrium: gene migration or gene flow, "
  "genetic drift, mutation, genetic recombination and natural selection. A is false and R is true.",
  ["A: false - frequencies stay constant unless disturbed", "R: true - the five factors"],
  "Hardy-Weinberg principle", ans="D",
  why="A contradicts the principle, so options A, B and C (which call A true) are wrong.", secs=40)

Z(EVO, "Natural selection", I, STP,
  SP("In NCERT's discussion of industrial melanism, no variant is completely wiped out; those that can better adapt "
     "survive and increase in population size.",
     "Homologous structures are the result of convergent evolution."),
  "Natural selection and homology",
  "NCERT (industrial melanism): in a mixed population, those that can better adapt survive and increase in "
  "population size; remember that no variant is completely wiped out. Homologous structures result from divergent "
  "evolution; it is analogous structures that result from convergent evolution.",
  ["Statement I: true", "Statement II: false - homology indicates divergent evolution"],
  "Evidences for evolution", ans="C",
  why="Statement II confuses homology with analogy, so A and D are wrong; Statement I is true, so B is wrong.",
  secs=40)

Z(EVO, "Evidences of evolution", I, MAT,
  ML(("observation", "kind of evidence for evolution"),
     ["Thorn of Bougainvillea and tendril of Cucurbita",
      "Flippers of penguins and of dolphins",
      "Similarities in proteins and genes performing a given function among diverse organisms",
      "Different-aged rock sediments containing different life forms"],
     ["Homologous structures (divergent evolution)", "Analogous structures (convergent evolution)",
      "Biochemical similarity", "Fossils (palaeontological evidence)"]),
  "Classifying evidences of evolution",
  "Thorn of Bougainvillea and tendril of Cucurbita are homologous (divergent evolution). Flippers of penguins and "
  "dolphins are analogous (convergent evolution). Similarities in proteins and genes performing a given function "
  "are biochemical evidence of common ancestry. Rock sediments of different ages containing different life forms "
  "are the basis of fossil evidence.",
  ["A - I", "B - II", "C - III", "D - IV"],
  "Evidences for evolution",
  at="C", match=({"A": "I", "B": "II", "C": "III", "D": "IV"},
                 [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "I", "B": "II", "C": "IV", "D": "III"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="The other codes swap homology with analogy, or biochemical evidence with fossil evidence, or both.", secs=50)

Z(EVO, "Origin of life", I, MUL,
  MS("Which of the following statements about S.L. Miller's experiment and its interpretation are correct?",
     ["He created electric discharge in a closed flask containing CH4, H2, NH3 and water vapour.",
      "He observed the formation of amino acids.",
      "Analysis of meteorite content also revealed similar compounds, indicating that similar processes are "
      "occurring elsewhere in space.",
      "The experiment produced a living cell within the flask.",
      "The flask contained an oxygen-rich atmosphere like that of the present-day earth."]),
  "Miller's experiment",
  "NCERT: S.L. Miller created electric discharge in a closed flask containing CH4, H2, NH3 and water "
  "vapour and observed formation of amino acids. Analysis of meteorite content revealed similar "
  "compounds, indicating similar processes elsewhere in space. The experiment showed chemical evolution of "
  "organic molecules, not the formation of a cell; the gases used were of a reducing (not oxygen-rich) "
  "atmosphere.",
  ["(a) true", "(b) true", "(c) true", "(d) false - only organic molecules formed", "(e) false - no oxygen-rich "
   "atmosphere"],
  "Origin of life",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(b) and (d) only", "(a), (b), (c) and (e) only", "(a), (c) and (d) only"],
  why="No cell was formed and the mixture lacked oxygen, so options including (d) or (e) are wrong.", secs=50)

Z(EVO, "Natural selection", I, D,
  "In a population, over many generations, the mean body size shifts steadily towards larger values because "
  "larger individuals leave more progeny. Which type of natural selection is this?",
  "Recognising directional selection",
  "NCERT: in stabilisation more individuals acquire the mean character value; in directional change more "
  "individuals acquire a value other than the mean character value; in disruption more individuals acquire "
  "peripheral character values at both ends. A steady shift of the mean to one side is directional selection.",
  ["Shift of the mean towards one end", "More individuals acquire a value other than the old mean",
   "-> directional selection"],
  "Evolution by natural selection",
  at="D", correct="Directional selection", wrong=["Stabilising selection", "Disruptive selection",
                                                   "Genetic drift"],
  why="Stabilising selection keeps the mean; disruptive selection favours both ends; genetic drift is a chance "
      "change, whereas here larger individuals leave more progeny (selection).", secs=35)

Z(EVO, "Adaptive radiation", I, STP,
  SP("In Australia, placental mammals also exhibit adaptive radiation, evolving into varieties each of which appears "
     "to be similar to a corresponding marsupial.",
     "When more than one adaptive radiation appears to have occurred in an isolated geographical area, it can be "
     "called convergent evolution."),
  "Adaptive radiation and convergent evolution in Australia",
  "NCERT: placental mammals in Australia also exhibit adaptive radiation in evolving into varieties of placental "
  "mammals, each of which appears to be 'similar' to a corresponding marsupial (e.g., placental wolf and Tasmanian "
  "wolf). When more than one adaptive radiation appears to have occurred in an isolated geographical area "
  "(representing different habitats), one can call this convergent evolution.",
  ["Statement I: true", "Statement II: true"],
  "Adaptive radiation", ans="A",
  why="Both are NCERT statements, so any option calling either of them false is wrong.", secs=45)

Z(EVO, "Darwinism and modern synthesis", I, ASR,
  AR("According to Darwin, heritable variations that enable better survival become more common in a population over "
     "generations.",
     "Individuals with such variations are enabled to reproduce and leave a greater number of progeny."),
  "How natural selection changes a population",
  "NCERT: natural selection is a process in which heritable variations enabling better survival are enabled to "
  "reproduce and leave a greater number of progeny. Because these individuals leave more offspring, which inherit "
  "the variation, the variation becomes more common in later generations. R is the cause of A.",
  ["Better-surviving variants reproduce more", "Offspring inherit the variation",
   "-> variation spreads; R explains A"],
  "Evolution by natural selection", ans="A",
  why="Greater reproduction of the variants is exactly why they increase, so B is wrong; both are true, so C and D "
      "are wrong.", secs=45)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population of 400 individuals, the genotypes for a gene with alleles A and a are 160 AA, 160 Aa and 80 aa. "
  "If this population were in Hardy-Weinberg equilibrium with the same allele frequencies, how many heterozygotes "
  "would be expected, and what does the observed number indicate?",
  "Testing a population against Hardy-Weinberg expectations",
  "Allele A count = 2(160) + 160 = 480 out of 800 alleles, so p = 0.6 and q = 0.4. Expected heterozygotes = "
  "2pq x 400 = 2(0.6)(0.4)(400) = 192. Only 160 are observed. NCERT: when the frequency measured differs from the "
  "expected values, the difference indicates the extent of evolutionary change, so the population is not in "
  "equilibrium.",
  ["p = 480/800 = 0.6, q = 0.4", "Expected Aa = 2pq x N = 0.48 x 400 = 192",
   "Observed 160 < 192 -> not in equilibrium"],
  "Hardy-Weinberg principle",
  at="A", correct="192; the observed 160 is fewer than expected, so the population is not in equilibrium",
  wrong=["160; the population is in equilibrium", "96; the observed 160 is more than expected",
         "200; the observed 160 is fewer than expected"],
  why="160 is just the observed number; 96 forgets the factor 2 in 2pq; 200 wrongly assumes p = q = 0.5.",
  short="Expected Aa = 2pqN; compare with observed.", secs=90, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, D,
  "A few birds from a large mainland population are blown to a distant island and start a new population there. "
  "By chance, the allele frequencies in the island population become very different from those on the mainland, "
  "and the island population may even become a different species. This is best described as:",
  "Recognising the founder effect",
  "NCERT: a change in allele frequency that occurs by chance is genetic drift. Sometimes the change in allele "
  "frequency is so different in the new sample of population that they become a different species. The original "
  "drifted population becomes the founders, and the effect is called the founder effect.",
  ["Small group starts a new population", "Allele frequencies changed by chance -> drift",
   "Founders of a new population -> founder effect"],
  "Hardy-Weinberg principle",
  at="B", correct="Founder effect, a result of genetic drift",
  wrong=["Gene flow, because alleles are added to the mainland population repeatedly",
         "Stabilising selection, because the mean character value is favoured",
         "Industrial melanism, because of pollution on the island"],
  why="Gene flow needs repeated migration between populations; stabilising selection is non-random and keeps the "
      "mean; industrial melanism concerns moth colour and pollution, not chance founding.", secs=50)

Z(EVO, "Darwinism and modern synthesis", A, ASR,
  AR("Darwin's theory proposed that new species arise by single-step large mutations.",
     "The variations that Darwin described are small and directional."),
  "Darwin versus de Vries",
  "NCERT: it was Hugo de Vries who, based on his work on evening primrose, believed that mutation causes evolution "
  "and called single-step large mutation saltation. Darwinian variations are small and directional, and for Darwin "
  "evolution was gradual. So A is false and R is true.",
  ["A: false - saltation is de Vries's idea", "R: true - Darwinian variations are small and directional"],
  "Mechanism of evolution", ans="D",
  why="A attributes de Vries's idea to Darwin, so options A, B and C are wrong.", secs=45)

Z(EVO, "Natural selection", A, MAT,
  ML(("observation", "evolutionary factor or process"),
     ["Individuals move repeatedly between two populations of a species",
      "Allele frequencies of a small population change purely by chance",
      "New, random and directionless variation appears suddenly, as de Vries saw in evening primrose",
      "Over generations, more individuals acquire the mean character value"],
     ["Mutation", "Genetic drift", "Stabilising selection", "Gene flow"]),
  "Identifying evolutionary factors from observations",
  "Repeated migration between populations is gene flow. Chance change in allele frequency is genetic drift. "
  "Random, directionless, sudden variation is mutation (de Vries). More individuals acquiring the mean value is "
  "stabilising selection.",
  ["A - IV", "B - II", "C - I", "D - III"],
  "Hardy-Weinberg principle; Mechanism of evolution",
  at="D", match=({"A": "IV", "B": "II", "C": "I", "D": "III"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"}]),
  why="The other codes swap gene flow with drift, mutation with stabilising selection, or drift with mutation.",
  secs=60)

Z(EVO, "Origin of life", A, STP,
  SP("When the first cellular forms of life originated, all life forms were in the water environment only.",
     "According to NCERT, the first organisms that invaded land were plants."),
  "Water and land in early life",
  "NCERT: the first cellular forms of life were probably single cells, and all life forms were in the water "
  "environment only. Later, the first organisms that invaded land were plants; they were widespread on land when "
  "animals invaded land.",
  ["Statement I: true", "Statement II: true"],
  "Origin of life; A brief account of evolution", ans="A",
  why="Both statements are NCERT lines, so every option calling either of them false is wrong.", secs=45)

# ================================================================ Human Health and Disease (6/8/6)
Z(HHD, "Pathogens and diseases", B, D,
  "Besides typhoid and pneumonia, NCERT names some other bacterial diseases in humans. These are:",
  "Other bacterial diseases",
  "NCERT: dysentery, plague and diphtheria are some of the other bacterial diseases in man.",
  ["Bacterial: typhoid, pneumonia", "Others named: dysentery, plague, diphtheria"],
  "Common diseases in humans",
  at="B", correct="Dysentery, plague and diphtheria",
  wrong=["Malaria, amoebiasis and ascariasis", "Ringworm and filariasis", "Common cold and AIDS"],
  why="Malaria and amoebiasis are protozoan and ascariasis is helminthic; ringworm is fungal and filariasis "
      "helminthic; the common cold and AIDS are viral.", secs=25)

Z(HHD, "Pathogens and diseases", B, D,
  "According to NCERT, health is affected by:",
  "Factors affecting health",
  "NCERT: health is affected by (i) genetic disorders - deficiencies with which a child is born and deficiencies "
  "or defects inherited from parents, (ii) infections and (iii) life style, including the food and water we take, "
  "rest and exercise and the habits we have or lack.",
  ["Genetic disorders", "Infections", "Life style"],
  "Introduction (health)",
  at="B", correct="Genetic disorders, infections and life style",
  wrong=["Infections alone", "Only the balance of the four humors of the body",
         "Only the food we eat"],
  why="NCERT names three factors, not one; the 'good humor' idea was an old belief that was later disproved.",
  secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "Which lymphoid organ is a large bean-shaped organ that acts as a filter of the blood by trapping blood-borne "
  "micro-organisms?",
  "Spleen as a secondary lymphoid organ",
  "NCERT: the spleen is a large bean-shaped organ. It mainly contains lymphocytes and phagocytes. It acts as a "
  "filter of the blood by trapping blood-borne micro-organisms, and it also has a large reservoir of erythrocytes.",
  ["Bean-shaped, large", "Filters blood, traps blood-borne microbes -> spleen"],
  "Lymphoid organs",
  at="C", correct="Spleen", wrong=["Thymus", "Tonsil", "Bone marrow"],
  why="The thymus is a lobed organ near the heart; tonsils lie in the throat and are not described as blood "
      "filters; the bone marrow is where blood cells are produced.", secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "According to NCERT, the main lymphoid organ where all blood cells, including lymphocytes, are produced is the:",
  "Bone marrow",
  "NCERT: the bone marrow is the main lymphoid organ where all blood cells including lymphocytes are produced. "
  "The thymus is a lobed organ located near the heart and beneath the breastbone.",
  ["All blood cells, including lymphocytes, form in the bone marrow"],
  "Lymphoid organs",
  at="D", correct="Bone marrow", wrong=["Spleen", "Lymph node", "Thymus"],
  why="The spleen and lymph nodes are secondary lymphoid organs; the thymus is where lymphocytes mature, not where "
      "all blood cells are produced.", secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "According to NCERT, how is the cause of an allergy in a patient determined?",
  "Finding the allergen",
  "NCERT: to determine the cause of allergy, the patient is exposed to or injected with very small doses of "
  "possible allergens, and the reactions studied.",
  ["Give very small doses of possible allergens", "Observe the reactions"],
  "Allergies",
  at="D", correct="The patient is exposed to or injected with very small doses of possible allergens and the "
                  "reactions are studied",
  wrong=["By the Widal test", "By ELISA for antibodies against HIV", "By a biopsy of the skin for tumour cells"],
  why="The Widal test confirms typhoid, ELISA detects HIV infection, and biopsy is used to detect cancer.",
  secs=25)

Z(HHD, "Cancer", B, D,
  "Malignant tumours are a mass of proliferating cells. NCERT calls these cells:",
  "Neoplastic cells",
  "NCERT: malignant tumours are a mass of proliferating cells called neoplastic or tumour cells. They grow very "
  "rapidly, invading and damaging the surrounding normal tissues.",
  ["Malignant tumour cells = neoplastic or tumour cells"],
  "Cancer",
  at="B", correct="Neoplastic or tumour cells", wrong=["Memory cells", "Mast cells", "Plasma cells of the spleen"],
  why="Memory cells are lymphocytes of the immune response; mast cells release histamine in allergy; none of "
      "these is the name NCERT gives to cancer cells.", secs=20)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("Antigens that get trapped in the lymph nodes cause an immune response.",
     "Antigens trapped in the lymph nodes are responsible for the activation of the lymphocytes present there."),
  "Role of lymph nodes",
  "NCERT: lymph nodes are small solid structures located at different points along the lymphatic system. They "
  "trap the micro-organisms or other antigens that get into the lymph and tissue fluid. Antigens trapped in the "
  "lymph nodes are responsible for the activation of lymphocytes present there and cause the immune response. "
  "Activation of lymphocytes is how the response starts, so R explains A.",
  ["A: true", "R: true", "Activated lymphocytes produce the immune response -> R explains A"],
  "Lymphoid organs", ans="A",
  why="R gives the mechanism of A, so B is wrong; both are true, so C and D are wrong.", secs=40)

Z(HHD, "Pathogens and diseases", I, STP,
  SP("In air-borne diseases such as pneumonia and common cold, close contact with infected persons or their "
     "belongings should be avoided.",
     "The discovery of antibiotics and various other drugs has enabled us to effectively treat infectious "
     "diseases."),
  "Preventing and treating infectious diseases",
  "NCERT: in cases of air-borne diseases such as pneumonia and common cold, in addition to the above measures, "
  "close contact with infected persons or their belongings should be avoided. The discovery of antibiotics and "
  "various other drugs has also enabled us to effectively treat infectious diseases.",
  ["Statement I: true", "Statement II: true"],
  "Prevention and control of diseases", ans="A",
  why="Both statements are NCERT lines, so every option calling either of them false is wrong.", secs=40)

Z(HHD, "Pathogens and diseases", I, MAT,
  ML(("disease", "preventive measure that suits its mode of spread"),
     ["Dengue", "Typhoid", "Pneumonia", "Ringworm"],
     ["Not sharing towels, clothes or combs with infected individuals",
      "Avoiding close contact with infected persons or their belongings",
      "Avoiding stagnation of water and regularly cleaning household coolers",
      "Consuming clean drinking water and food"]),
  "Matching prevention to transmission",
  "Dengue is transmitted by Aedes mosquitoes, so their breeding places (stagnant water, coolers) must be removed. "
  "Typhoid spreads through contaminated food and water. Pneumonia spreads by droplets/aerosols from infected "
  "persons, so close contact with them and their belongings is avoided. Ringworm is acquired from soil or by using "
  "towels, clothes or even the comb of infected individuals.",
  ["A - III", "B - IV", "C - II", "D - I"],
  "Common diseases in humans; Prevention and control of diseases",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
  why="The other codes give the vector measure to typhoid, the towel measure to pneumonia, or the droplet measure "
      "to dengue.", secs=50)

Z(HHD, "Cancer", I, MUL,
  MS("Which of the following are described in NCERT as agents that can cause cancer (carcinogens)?",
     ["Ionising radiations like X-rays and gamma rays", "Non-ionising radiations like UV",
      "Chemical carcinogens present in tobacco smoke", "Cancer-causing (oncogenic) viruses",
      "α-interferon"]),
  "Carcinogens",
  "NCERT: transformation of normal cells into cancerous neoplastic cells may be induced by physical, chemical or "
  "biological agents called carcinogens - ionising radiations (X-rays, gamma rays), non-ionising radiations (UV), "
  "chemical carcinogens in tobacco smoke, and oncogenic viruses. α-interferon is a biological response modifier "
  "used in treatment; it activates the immune system and helps destroy the tumour.",
  ["(a), (b): physical carcinogens", "(c): chemical", "(d): biological", "(e): a treatment, not a carcinogen"],
  "Cancer",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c) and (d) only", "(a), (c), (d) and (e) only"],
  why="α-interferon is used to treat cancer, so options with (e) are wrong; (c) and (d) only leaves out the "
      "radiations.", secs=45)

Z(HHD, "Drug and alcohol abuse", I, D,
  "According to NCERT, dependence on drugs or alcohol leads the patient to:",
  "Consequence of dependence",
  "NCERT: dependence is the tendency of the body to manifest a characteristic and unpleasant withdrawal syndrome "
  "if the regular dose is abruptly discontinued. Dependence leads the patient to ignore all social norms in order "
  "to get sufficient funds to satiate his/her needs.",
  ["Dependence -> withdrawal syndrome on stopping", "Leads to ignoring social norms to get funds"],
  "Drugs and alcohol abuse",
  at="D", correct="Ignore all social norms in order to get sufficient funds to satiate his/her needs",
  wrong=["Lose all desire for the drug within a few days", "Need steadily lower doses to get the same effect",
         "Develop permanent immunity against the drug"],
  why="Dependence increases, not removes, the craving; tolerance means higher (not lower) doses are needed; there "
      "is no immunity against a drug.", secs=30)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Withdrawal symptoms can in some cases be severe and even life threatening, and the person may need medical "
     "supervision.",
     "Cocaine is a depressant that slows down body functions."),
  "Withdrawal and the action of cocaine",
  "NCERT: the withdrawal syndrome is characterised by anxiety, shakiness, nausea and sweating; in some cases "
  "withdrawal symptoms can be severe and even life threatening and the person may need medical supervision. "
  "Cocaine is a potent stimulant of the central nervous system, producing euphoria and increased energy; it is "
  "heroin that is a depressant and slows down body functions.",
  ["Statement I: true", "Statement II: false - cocaine is a stimulant"],
  "Drugs; Adolescence and drug/alcohol abuse", ans="C",
  why="Statement II gives heroin's action to cocaine, so A and D are wrong; Statement I is true, so B is wrong.",
  secs=40)

Z(HHD, "Immunity and vaccines", I, MUL,
  MS("Which of the following statements about vaccination are correct?",
     ["A preparation of antigenic proteins of a pathogen, or of inactivated/weakened pathogens, is introduced into "
      "the body.",
      "The antibodies produced in the body neutralise the pathogenic agents during actual infection.",
      "Vaccines generate memory B and T-cells that recognise the pathogen quickly on subsequent exposure.",
      "Vaccination provides passive immunity.",
      "Vaccines are preferred when a quick immune response is needed, as in tetanus."]),
  "Principle of vaccination",
  "NCERT: in vaccination, a preparation of antigenic proteins of a pathogen or inactivated/weakened pathogen "
  "(vaccine) is introduced; the antibodies produced neutralise the pathogenic agents during actual infection, and "
  "vaccines generate memory B and T-cells. The body makes its own antibodies, so this is active immunity. For a "
  "quick response, as in tetanus, preformed antibodies or antitoxin are injected (passive immunisation).",
  ["(a), (b), (c): true", "(d) false - active immunity", "(e) false - preformed antibodies are used for quick "
   "response"],
  "Vaccination and immunisation",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a) and (e) only"],
  why="Vaccination is active, and the quick response in tetanus needs preformed antibodies, so options with (d) or "
      "(e) are wrong.", secs=50)

Z(HHD, "HIV and AIDS", I, ASR,
  AR("HIV can be transmitted by sharing infected needles, as in intravenous drug abusers.",
     "HIV is a member of the retrovirus group, having an envelope enclosing an RNA genome."),
  "Transmission of HIV versus its structure",
  "Both are NCERT statements. HIV spreads by sharing infected needles because the virus is carried in the infected "
  "blood on the needle. R describes the structure of the virus (retrovirus, RNA genome); this is true of HIV but "
  "it is not why sharing needles transmits it - many viruses with very different genomes are spread the same way.",
  ["A: true", "R: true", "Transmission depends on contact with infected blood, not on having an RNA genome"],
  "AIDS", ans="B",
  why="R gives the structure, not the route, of transmission, so A is wrong; both statements are true, so C and D "
      "are wrong.", secs=45)

Z(HHD, "Immunity and vaccines", A, D,
  "After a deep wound, a child is given an injection of preformed antibodies (antitoxin) against tetanus. Some "
  "weeks later, the same child is given the tetanus vaccine. Which of the following correctly compares the two?",
  "Passive versus active immunisation",
  "Injecting preformed antibodies gives passive immunity: the response is quick, but the child's own lymphocytes "
  "are not stimulated, so no memory is formed. A vaccine gives active immunity: the child produces its own "
  "antibodies, which is slower, and memory B and T-cells are formed for a quick response later.",
  ["Antitoxin -> passive: quick, no memory", "Vaccine -> active: slower, memory cells formed"],
  "Active and passive immunity; Vaccination and immunisation",
  at="C", correct="The antitoxin gives quick passive immunity without memory; the vaccine gives active immunity "
                  "and generates memory B and T-cells",
  wrong=["Both give active immunity with memory cells",
         "The antitoxin gives active immunity; the vaccine gives passive immunity",
         "Both give passive immunity, because both are injected"],
  why="The route (injection) does not decide the type; what matters is whether antibodies are supplied ready-made "
      "(passive) or made by the body (active).", secs=50)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("stage in the life cycle of Plasmodium", "site where it occurs"),
     ["Storage of sporozoites", "First asexual reproduction after entering a human",
      "Development of gametocytes (sexual stages)", "Fertilisation and development of gametes"],
     ["Red blood cells of the human", "Stomach of the female Anopheles mosquito",
      "Salivary glands of the female Anopheles mosquito", "Liver cells of the human"]),
  "Sites in the life cycle of Plasmodium",
  "NCERT: sporozoites are stored in the salivary glands of the mosquito and enter a human through its bite. The "
  "parasites reproduce asexually first in liver cells and then attack the RBCs. Sexual stages (gametocytes) develop "
  "in the RBCs. When a female Anopheles takes up gametocytes with the blood meal, fertilisation and development "
  "take place in the mosquito's stomach.",
  ["A - III", "B - IV", "C - I", "D - II"],
  "Common diseases in humans (malaria)",
  at="D", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
  why="The other codes swap the salivary glands with the stomach, the liver with the RBCs, or the RBCs with the "
      "mosquito's stomach.", secs=60)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("Drugs such as anti-histamines quickly reduce the symptoms of an allergy.",
     "The symptoms of allergic reactions are caused by the release of chemicals like histamine and serotonin from "
     "the mast cells."),
  "Why anti-histamines relieve allergy",
  "NCERT: the allergic reaction is due to the release of chemicals like histamine and serotonin from the mast "
  "cells; the use of drugs like anti-histamine, adrenalin and steroids quickly reduces the symptoms. Because "
  "histamine released by mast cells causes the symptoms, a drug that counters histamine relieves them, so R "
  "explains A.",
  ["Mast cells release histamine -> symptoms", "Anti-histamines counter histamine -> symptoms reduce",
   "R explains A"],
  "Allergies", ans="A",
  why="R gives the cause on which the anti-histamine acts, so B is wrong; both are true, so C and D are wrong.",
  secs=45)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("Which of the following are secondary lymphoid organs?",
     ["Spleen", "Lymph nodes", "Tonsils", "Peyer's patches of the small intestine", "Thymus"]),
  "Primary versus secondary lymphoid organs",
  "NCERT: the primary lymphoid organs are the bone marrow and thymus, where immature lymphocytes differentiate "
  "into antigen-sensitive lymphocytes. After maturation the lymphocytes migrate to secondary lymphoid organs such "
  "as spleen, lymph nodes, tonsils, Peyer's patches of the small intestine and appendix, where they interact with "
  "the antigen and proliferate to become effector cells.",
  ["(a)-(d): secondary", "(e) thymus: primary"],
  "Lymphoid organs",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="The thymus is a primary lymphoid organ, so any option including (e) is wrong.", secs=45)

Z(HHD, "HIV and AIDS", A, D,
  "In an HIV-infected person, the number of helper T-lymphocytes falls progressively. Which immune function is "
  "weakened as a result?",
  "Effect of losing helper T-cells",
  "NCERT: B-lymphocytes produce antibodies; T-cells themselves do not secrete antibodies but help B-cells produce "
  "them, and T-lymphocytes mediate cell-mediated immunity. HIV attacks helper T-lymphocytes (TH) and progressively "
  "decreases their number, so the person becomes immunodeficient: both antibody production (which needs T-cell "
  "help) and cell-mediated responses suffer.",
  ["Helper T-cells help B-cells make antibodies", "T-cells also mediate CMI",
   "Loss of TH cells weakens both -> immunodeficiency"],
  "AIDS; Acquired immunity",
  at="B", correct="Both antibody production by B-cells and cell-mediated immunity, since helper T-cells are needed "
                  "for both",
  wrong=["Only the physical barriers of innate immunity, such as the skin",
         "Only the secretion of acid in the stomach",
         "Neither, because B-cells produce antibodies without any help"],
  why="Skin and stomach acid are innate barriers not dependent on helper T-cells; NCERT states that T-cells help "
      "B-cells produce antibodies, so B-cell function does suffer.", secs=55)

Z(HHD, "Drug and alcohol abuse", A, STP,
  SP("Misuse of anabolic steroids in females can cause abnormal menstrual cycles and excessive hair growth on the "
     "face and body.",
     "In males, misuse of anabolic steroids can cause breast enlargement and has the potential for kidney and liver "
     "dysfunction."),
  "Side-effects of anabolic steroids",
  "NCERT: in females, side-effects of anabolic steroids include masculinisation, increased aggressiveness, mood "
  "swings, depression, abnormal menstrual cycles, excessive hair growth on the face and body, enlargement of the "
  "clitoris and deepening of voice. In males they include acne, aggressiveness, mood swings, depression, reduction "
  "of size of the testicles, decreased sperm production, potential for kidney and liver dysfunction, breast "
  "enlargement, premature baldness and enlargement of the prostate gland.",
  ["Statement I: true", "Statement II: true"],
  "Drugs; Adolescence and drug/alcohol abuse", ans="A",
  why="Both statements are from NCERT's list, so every option calling either of them false is wrong.", secs=45)

# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Bioreactors and downstream processing", B, D,
  "In bioprocess engineering, for producing antibiotics, vaccines and enzymes on a large scale, it is necessary to "
  "maintain:",
  "Sterile conditions in bioprocess engineering",
  "NCERT: bioprocess engineering means maintenance of a sterile (microbial contamination-free) ambience in chemical "
  "engineering processes to enable growth of only the desired microbe/eukaryotic cell in large quantities for the "
  "manufacture of biotechnological products like antibiotics, vaccines and enzymes.",
  ["Large-scale culture of only the desired cells", "Needs a sterile, contamination-free ambience"],
  "Principles of biotechnology",
  at="A", correct="A sterile (microbial contamination-free) ambience, so that only the desired microbe or cell grows",
  wrong=["A mixed culture of many microbes, so that the yield increases",
         "A temperature close to 0 °C throughout the process",
         "Complete absence of oxygen in every bioprocess"],
  why="Contaminating microbes would compete with the desired cells; NCERT does not require near-freezing "
      "temperature or absence of oxygen (stirred-tank bioreactors actually supply oxygen).", secs=25)

Z(BPP, "Restriction enzymes", B, NUM,
  "EcoRI recognises 5'-GAATTC-3' and cuts each strand between the bases G and A. How many unpaired (single-stranded) "
  "nucleotides are present in the overhang of each sticky end so produced?",
  "Sticky ends produced by EcoRI",
  "Upper strand 5'-G|AATTC-3' and lower strand 3'-CTTAA|G-5' are cut between G and A. The single-stranded stretch "
  "left on each end is AATT, i.e., 4 nucleotides. These overhanging stretches are the sticky ends, which form "
  "hydrogen bonds with their complementary cut counterparts.",
  ["Site: GAATTC, palindromic", "Cut after G on both strands", "Overhang = AATT = 4 nucleotides"],
  "Restriction enzymes",
  at="C", correct="4", wrong=["6", "2", "1"],
  why="6 counts the whole recognition site; 2 halves the overhang; 1 counts only the G that stays on one side.",
  short="Overhang length = site length - 2 x (bases before the cut) = 6 - 2 = 4.", secs=45, vb=RECOMPUTED)

Z(BPP, "Restriction enzymes", B, D,
  "In genetic engineering, restriction endonucleases are used to form:",
  "Use of restriction endonucleases",
  "NCERT: restriction endonucleases are used in genetic engineering to form 'recombinant' molecules of DNA, which "
  "are composed of DNA from different genomes.",
  ["Restriction enzymes cut DNA at specific sites", "Fragments from different genomes are joined -> recombinant DNA"],
  "Restriction enzymes",
  at="B", correct="Recombinant molecules of DNA composed of DNA from different genomes",
  wrong=["Proteins from amino acids", "RNA copies of genes for translation", "Primers for PCR"],
  why="Restriction enzymes act on DNA; they do not make proteins or RNA, and primers are chemically synthesised "
      "oligonucleotides.", secs=20)

Z(BPP, "Bioreactors and downstream processing", B, D,
  "According to NCERT, in almost all recombinant technologies the ultimate aim is to:",
  "Aim of recombinant technology",
  "NCERT: in almost all recombinant technologies, the ultimate aim is to produce a desirable protein. A "
  "protein-encoding gene expressed in a heterologous host gives a recombinant protein.",
  ["Ultimate aim: a desirable protein", "Made in a heterologous host -> recombinant protein"],
  "Obtaining the foreign gene product",
  at="D", correct="Produce a desirable protein",
  wrong=["Destroy the host bacterium", "Remove all plasmids from the host cell", "Make the host resistant to all "
                                                                                  "antibiotics"],
  why="The host is used, not destroyed; plasmids are vectors, not something to remove; antibiotic resistance genes "
      "are only selectable markers, not the aim.", secs=20)

Z(BPP, "Restriction enzymes", B, D,
  "Restriction enzymes belong to the class of enzymes called nucleases. Exonucleases, one type of nuclease, remove "
  "nucleotides from:",
  "Exonucleases versus endonucleases",
  "NCERT: nucleases are of two kinds - exonucleases and endonucleases. Exonucleases remove nucleotides from the "
  "ends of the DNA, whereas endonucleases make cuts at specific positions within the DNA.",
  ["Exo- : from the ends", "Endo- : within the DNA, at specific positions"],
  "Restriction enzymes",
  at="D", correct="The ends of the DNA", wrong=["Specific positions within the DNA", "Only RNA molecules",
                                                "The middle of a palindromic sequence only"],
  why="Cutting at specific positions within DNA is what endonucleases do; nucleases named here act on DNA, not "
      "only RNA.", secs=20)

Z(BPP, "PCR and gel electrophoresis", I, NUM,
  "A 12 kb linear DNA molecule has EcoRI sites at 3 kb and at 8 kb from its left end. It is completely digested with "
  "EcoRI and run on an agarose gel. Which fragment moves farthest from the well?",
  "Digestion and size-based separation",
  "Cutting at 3 kb and 8 kb gives fragments of 3 kb (0-3), 5 kb (3-8) and 4 kb (8-12). In agarose gel "
  "electrophoresis DNA fragments separate according to size by the sieving effect of the gel; the smaller the "
  "fragment, the farther it moves. So the 3 kb fragment moves farthest.",
  ["Fragments: 3, 5 and 4 kb", "Smaller fragments move farther", "3 kb moves farthest"],
  "Separation and isolation of DNA fragments (gel electrophoresis)",
  at="D", correct="The 3 kb fragment", wrong=["The 5 kb fragment", "The 4 kb fragment",
                                               "All fragments stay together as one band"],
  why="5 kb is the largest and moves least; 4 kb lies between; fragments of different sizes do separate into "
      "different bands.", secs=60, vb=RECOMPUTED)

Z(BPP, "Competent hosts and transformation", I, ASR,
  AR("Bacterial cells treated with a specific concentration of calcium can take up recombinant DNA.",
     "Divalent cations increase the efficiency with which DNA enters the bacterium through pores in its cell "
     "wall."),
  "Making cells competent",
  "NCERT: since DNA is hydrophilic, it cannot pass through cell membranes. The bacterial cells are made competent "
  "by treating them with a specific concentration of a divalent cation such as calcium, which increases the "
  "efficiency with which DNA enters the bacterium through pores in its cell wall. That increased efficiency is "
  "exactly why calcium-treated cells take up DNA.",
  ["A: true", "R: true", "Calcium (divalent cation) increases DNA entry -> R explains A"],
  "Competent host (for transformation with recombinant DNA)", ans="A",
  why="R is the reason for A, so B is wrong; both statements are true, so C and D are wrong.", secs=40)

Z(BPP, "Cloning vectors", I, STP,
  SP("The presence of more than one recognition site for a restriction enzyme within a vector will generate "
     "several fragments, which will complicate gene cloning.",
     "In selection by insertional inactivation of β-galactosidase, colonies carrying the recombinant DNA give a "
     "blue colour with the chromogenic substrate."),
  "Cloning sites and blue-white selection",
  "NCERT: to link the alien DNA, the vector needs very few, preferably single, recognition sites; more than one "
  "site generates several fragments and complicates cloning. With insertional inactivation of β-galactosidase, "
  "non-recombinant colonies give blue colour, whereas recombinant colonies do not produce any colour.",
  ["Statement I: true", "Statement II: false - recombinant colonies are colourless"],
  "Cloning vectors", ans="C",
  why="Statement II reverses the colours, so A and D are wrong; Statement I is true, so B is wrong.", secs=45)

Z(BPP, "PCR and gel electrophoresis", I, MAT,
  ML(("requirement in an experiment", "technique used"),
     ["Making multiple copies of a gene in vitro", "Separating DNA fragments according to size",
      "Injecting recombinant DNA directly into the nucleus of an animal cell",
      "Bombarding plant cells with DNA-coated gold or tungsten micro-particles"],
     ["Polymerase chain reaction (PCR)", "Biolistics (gene gun)", "Agarose gel electrophoresis",
      "Micro-injection"]),
  "Choosing a technique",
  "PCR synthesises multiple copies of a gene in vitro using primers and DNA polymerase. Agarose gel "
  "electrophoresis separates DNA fragments by size. In micro-injection, recombinant DNA is injected directly into "
  "the nucleus of an animal cell. In biolistics (gene gun), cells are bombarded with high-velocity micro-particles "
  "of gold or tungsten coated with DNA; it is suitable for plants.",
  ["A - I", "B - III", "C - IV", "D - II"],
  "Amplification using PCR; Gel electrophoresis; Competent host",
  at="A", match=({"A": "I", "B": "III", "C": "IV", "D": "II"},
                 [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "I", "B": "III", "C": "II", "D": "IV"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="The other codes swap PCR with electrophoresis, micro-injection with biolistics, or electrophoresis with "
      "micro-injection.", secs=45)

Z(BPP, "Cloning vectors", I, MUL,
  MS("Which of the following features are required in a vector to facilitate cloning?",
     ["An origin of replication (ori)", "A selectable marker", "Cloning sites (recognition sites for restriction "
                                                                "enzymes)",
      "A gene for the Bt toxin", "A large number of recognition sites for the same restriction enzyme"]),
  "Features of a cloning vector",
  "NCERT: the features required to facilitate cloning into a vector are the origin of replication (ori), a "
  "selectable marker and cloning sites (very few, preferably single, recognition sites for the commonly used "
  "restriction enzymes); vectors for plants and animals are also needed for those hosts. A Bt toxin gene is a "
  "gene that may be cloned, not a vector feature, and many sites for one enzyme would cut the vector into "
  "several fragments.",
  ["(a), (b), (c): required", "(d): not a vector feature", "(e): opposite of what is needed"],
  "Cloning vectors",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(b) and (d) only", "(a), (c) and (d) only"],
  why="A vector needs very few recognition sites, not many, and the Bt gene is not a vector feature, so options "
      "with (d) or (e) are wrong.", secs=45)

Z(BPP, "Competent hosts and transformation", I, D,
  "A scientist wants to introduce recombinant DNA into plant cells without using any 'disarmed pathogen' vector. "
  "Which method, described by NCERT as suitable for plants, should be used?",
  "Choosing a DNA-transfer method",
  "NCERT: in biolistics (gene gun), cells are bombarded with high-velocity micro-particles of gold or tungsten "
  "coated with DNA; this method is suitable for plants. Micro-injection injects DNA directly into the nucleus of an "
  "animal cell. Agrobacterium and retroviruses are disarmed pathogen vectors, which the scientist wants to avoid.",
  ["No pathogen vector allowed", "Plant cells", "-> biolistics (gene gun)"],
  "Competent host (for transformation with recombinant DNA)",
  at="B", correct="Biolistics (gene gun)",
  wrong=["Micro-injection into the nucleus of an animal cell", "Ti plasmid of Agrobacterium tumefaciens",
         "Disarmed retrovirus"],
  why="Micro-injection is described for animal cells; Agrobacterium and retroviruses are pathogen-based vectors.",
  secs=35)

Z(BPP, "Bioreactors and downstream processing", I, STP,
  SP("In a continuous culture system, the used medium is drained out from one side while fresh medium is added from "
     "the other.",
     "A continuous culture system maintains the cells in their physiologically most active log/exponential "
     "phase."),
  "Continuous culture",
  "NCERT: in the continuous culture system, the used medium is drained out from one side while fresh medium is "
  "added from the other to maintain the cells in their physiologically most active log/exponential phase. This "
  "produces a larger biomass and higher yields of the desired protein.",
  ["Statement I: true", "Statement II: true"],
  "Obtaining the foreign gene product", ans="A",
  why="Both statements are NCERT lines, so every option calling either of them false is wrong.", secs=40)

Z(BPP, "PCR and gel electrophoresis", A, NUM,
  "A PCR is started with 5 double-stranded molecules of a DNA segment. If every cycle exactly doubles the number of "
  "molecules, what is the minimum number of cycles needed to obtain at least 1000 molecules?",
  "Exponential amplification in PCR",
  "After n cycles the number of molecules is 5 x 2^n. 5 x 2^7 = 640 (less than 1000) and 5 x 2^8 = 1280 (at least "
  "1000). So 8 cycles are the minimum.",
  ["Molecules = 5 x 2^n", "n = 7: 640 < 1000", "n = 8: 1280 >= 1000 -> 8 cycles"],
  "Amplification of gene of interest using PCR",
  at="B", correct="8", wrong=["7", "10", "200"],
  why="7 cycles give only 640; 10 ignores the 5 starting molecules (2^10 = 1024); 200 treats the increase as linear "
      "(1000/5).", short="Find n with 2^n >= 1000/5 = 200, i.e. n = 8.", secs=60, vb=RECOMPUTED)

Z(BPP, "PCR and gel electrophoresis", A, ASR,
  AR("Agarose gel electrophoresis separates DNA fragments according to their size.",
     "Agarose is a natural polymer extracted from sea weeds."),
  "Basis of separation versus source of agarose",
  "NCERT: DNA fragments separate (resolve) according to their size through the sieving effect provided by the "
  "agarose gel. Agarose is a natural polymer extracted from sea weeds. Its source is a true fact but does not "
  "explain size-based separation; the sieving effect does.",
  ["A: true", "R: true", "Separation is due to sieving, not to where agarose comes from"],
  "Separation and isolation of DNA fragments (gel electrophoresis)", ans="B",
  why="R gives the origin of the matrix, not the reason for separation, so A is wrong; both are true, so C and D "
      "are wrong.", secs=45)

Z(BPP, "Restriction enzymes", A, MAT,
  ML(("enzyme", "action in recombinant DNA work"),
     ["Restriction endonuclease", "Ribonuclease", "DNA ligase", "Thermostable DNA polymerase"],
     ["Joins the cut ends of the vector and the foreign DNA",
      "Extends the primers using nucleotides and the template during PCR",
      "Cuts DNA at a specific recognition sequence",
      "Removes RNA from the DNA preparation"]),
  "Enzymes of recombinant DNA technology",
  "Restriction endonucleases cut DNA at specific recognition (palindromic) sequences. Ribonuclease removes RNA "
  "during isolation of DNA. DNA ligase joins the cut vector and the source DNA. A thermostable DNA polymerase "
  "(from Thermus aquaticus) extends the primers in PCR, remaining active at the high temperature used for "
  "denaturation.",
  ["A - III", "B - IV", "C - I", "D - II"],
  "Tools of recombinant DNA technology; Processes of recombinant DNA technology",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The other codes swap the restriction enzyme with ligase, ribonuclease with the polymerase, or the restriction "
      "enzyme with ribonuclease.", secs=55)

Z(BPP, "Restriction enzymes", A, MUL,
  MS("A gene and a plasmid vector are each cut with EcoRI and then mixed with DNA ligase. Which of the following "
     "statements are correct?",
     ["The gene and the vector get the same kind of sticky ends, so they can be joined.",
      "The sticky ends form hydrogen bonds with their complementary cut counterparts, which facilitates the action "
      "of DNA ligase.",
      "The vector should preferably have a single EcoRI site, so that it is not cut into several fragments.",
      "If the gene had been cut with a different restriction enzyme, its ends would always match the EcoRI ends of "
      "the vector.",
      "DNA ligase cuts the DNA at the sequence GAATTC."]),
  "Joining DNA cut by the same enzyme",
  "NCERT: when cut by the same restriction enzyme, the resultant DNA fragments have the same kind of sticky ends, "
  "which can be joined end-to-end using DNA ligases; the sticky ends form hydrogen bonds with their complementary "
  "cut counterparts, which facilitates ligase action. Normally the vector and source DNA must be cut with the same "
  "enzyme; a vector needs very few, preferably single, recognition sites. Ligase joins DNA; it does not cut it.",
  ["(a), (b), (c): true", "(d) false - different enzymes generally give different ends",
   "(e) false - cutting is done by the restriction enzyme"],
  "Restriction enzymes; Cutting of DNA at specific locations",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
  why="Statement (d) ignores the need to use the same enzyme and (e) gives the cutting role to ligase, so options "
      "with (d) or (e) are wrong.", secs=55)

Z(BPP, "Cloning vectors", A, STP,
  SP("Insertional inactivation of β-galactosidase lets recombinants be selected on a single plate, unlike "
     "inactivation of an antibiotic resistance gene, which needs plating on two plates with different "
     "antibiotics.",
     "If many copies of the target DNA are wanted, it should be cloned in a vector whose origin of replication "
     "supports a high copy number."),
  "Practical choices in cloning",
  "NCERT: selection of recombinants by inactivation of an antibiotic resistance gene is cumbersome because it "
  "requires simultaneous plating on two plates having different antibiotics; therefore alternative markers such as "
  "β-galactosidase, which give colour with a chromogenic substrate, have been developed. The ori controls the copy "
  "number of the linked DNA, so a high-copy vector is chosen to get many copies of the target DNA.",
  ["Statement I: true", "Statement II: true"],
  "Cloning vectors", ans="A",
  why="Both statements are true, so every option calling either of them false is wrong.", secs=50)

# ================================================================ Biotechnology and its Applications (5/7/5)
Z(BTA, "Gene therapy", B, D,
  "In gene therapy, a normal gene is delivered into the individual or embryo in order to:",
  "Principle of gene therapy",
  "NCERT: gene therapy involves delivery of a normal gene into the individual or embryo to take over the function "
  "of and compensate for the non-functional gene.",
  ["Normal gene delivered", "It takes over the function of, and compensates for, the faulty gene"],
  "Gene therapy",
  at="A", correct="Take over the function of, and compensate for, the non-functional gene",
  wrong=["Destroy all the cells that carry the defective gene", "Produce antibodies against the defective gene",
         "Convert the person into a transgenic animal model of the disease"],
  why="Gene therapy compensates for the faulty gene; it does not kill cells, raise antibodies, or create disease "
      "models (that is a use of transgenic animals).", secs=25)

Z(BTA, "Human insulin", B, D,
  "Human insulin consists of two short polypeptide chains, chain A and chain B. These chains are linked together "
  "by:",
  "Structure of insulin",
  "NCERT: insulin consists of two short polypeptide chains, chain A and chain B, that are linked together by "
  "disulphide bridges.",
  ["Two chains, A and B", "Joined by disulphide bridges"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="B", correct="Disulphide bridges", wrong=["Phosphodiester bonds", "Glycosidic bonds", "The C peptide"],
  why="Phosphodiester bonds link nucleotides and glycosidic bonds link sugars; the C peptide is the extra stretch "
      "of pro-insulin that is removed during maturation.", secs=20)

Z(BTA, "Bt crops and RNAi", B, D,
  "The Bt toxin used in Bt cotton is produced naturally by Bacillus thuringiensis, which is a:",
  "Source organism of the Bt toxin",
  "NCERT: Bt toxin is produced by a bacterium called Bacillus thuringiensis (Bt for short). The Bt toxin gene has "
  "been cloned from the bacterium and expressed in plants.",
  ["Bacillus thuringiensis = a bacterium"],
  "Biotechnological applications in agriculture",
  at="C", correct="Bacterium", wrong=["Fungus", "Nematode", "Virus with an RNA genome"],
  why="NCERT calls Bacillus thuringiensis a bacterium; the nematode in this chapter is the tobacco parasite "
      "Meloidegyne incognitia.", secs=20)

Z(BTA, "Bt crops and RNAi", B, D,
  "The nematode Meloidegyne incognitia, against which tobacco plants were protected by RNA interference, infects "
  "the:",
  "Site of nematode infection",
  "NCERT: a nematode Meloidegyne incognitia infects the roots of tobacco plants and causes a great reduction in "
  "yield.",
  ["Pest: Meloidegyne incognitia", "Infects tobacco roots, reducing yield"],
  "Biotechnological applications in agriculture",
  at="D", correct="Roots of tobacco plants", wrong=["Leaves of tobacco plants", "Bolls of cotton plants",
                                                   "Grains of rice plants"],
  why="NCERT names the roots of tobacco; cotton bolls are attacked by bollworms, and rice grains are not the site "
      "of this nematode.", secs=20)

Z(BTA, "Bt crops and RNAi", B, STP,
  SP("Bt toxin genes were isolated from Bacillus thuringiensis and incorporated into several crop plants such as "
     "cotton.",
     "The activated Bt toxin kills the insect by dissolving its cuticle (exoskeleton)."),
  "Bt toxin genes and their action",
  "NCERT: Bt toxin genes were isolated from Bacillus thuringiensis and incorporated into several crop plants such "
  "as cotton. The activated toxin binds to the surface of the midgut epithelial cells and creates pores that cause "
  "cell swelling and lysis, eventually causing the death of the insect; it does not dissolve the cuticle.",
  ["Statement I: true", "Statement II: false - it acts on midgut epithelial cells"],
  "Biotechnological applications in agriculture", ans="C",
  why="Statement II misstates the site of action, so A and D are wrong; Statement I is true, so B is wrong.",
  secs=35)

Z(BTA, "Bt crops and RNAi", I, MAT,
  ML(("problem", "biotechnological solution described in NCERT"),
     ["Nematode infection of tobacco roots", "Bollworm damage to cotton",
      "Vitamin A deficiency in a rice-based diet", "Adenosine deaminase (ADA) deficiency in a child"],
     ["Golden rice", "Expression of the genes cryIAc and cryIIAb",
      "RNA interference using nematode-specific genes", "Gene therapy using the patient's lymphocytes"]),
  "Matching problems with solutions",
  "Tobacco was protected from Meloidegyne incognitia by RNAi, using nematode-specific genes introduced with "
  "Agrobacterium vectors. The proteins encoded by cryIAc and cryIIAb control the cotton bollworms. Golden rice is "
  "a GM crop enriched in vitamin A. ADA deficiency was treated by the first clinical gene therapy, in which "
  "lymphocytes from the patient's blood received a functional ADA cDNA.",
  ["A - III", "B - II", "C - I", "D - IV"],
  "Biotechnological applications in agriculture; Gene therapy",
  at="B", match=({"A": "III", "B": "II", "C": "I", "D": "IV"},
                 [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "I", "B": "II", "C": "III", "D": "IV"}]),
  why="The other codes swap RNAi with the cry genes, golden rice with gene therapy, or golden rice with RNAi.",
  secs=45)

Z(BTA, "Bt crops and RNAi", I, ASR,
  AR("Golden rice is a genetically modified crop with enhanced nutritional value.",
     "Golden rice is enriched in vitamin C."),
  "Golden rice",
  "NCERT gives golden rice, i.e., vitamin 'A' enriched rice, as the example of GM crops with enhanced nutritional "
  "value. A is true; R names the wrong vitamin and is false.",
  ["A: true", "R: false - golden rice is enriched in vitamin A"],
  "Biotechnological applications in agriculture", ans="C",
  why="R is false, so options A, B and D (which call R true) are wrong.", secs=30)

Z(BTA, "Human insulin", I, STP,
  SP("In mammals, including humans, insulin is synthesised as a pro-hormone that contains an extra stretch called "
     "the C peptide.",
     "Recombinant therapeutics do not induce unwanted immunological responses, as is common in the case of similar "
     "products isolated from non-human sources."),
  "Pro-insulin and safety of recombinant therapeutics",
  "NCERT: in mammals, including humans, insulin is synthesised as a pro-hormone which contains an extra stretch "
  "called the C peptide; this is removed during maturation. Recombinant DNA technology has enabled mass production "
  "of safe and more effective therapeutic drugs, which do not induce unwanted immunological responses as is common "
  "with similar products isolated from non-human sources.",
  ["Statement I: true", "Statement II: true"],
  "Biotechnological applications in medicine", ans="A",
  why="Both statements are NCERT lines, so every option calling either of them false is wrong.", secs=40)

Z(BTA, "Bt crops and RNAi", I, MUL,
  MS("A farmer grows Bt cotton in place of ordinary cotton. Which of the following are expected, according to "
     "NCERT?",
     ["The crop needs less spraying of insecticides.",
      "The crop is protected against cotton bollworms.",
      "A bollworm larva feeding on the plant ingests an inactive protoxin, which becomes active in its alkaline "
      "gut.",
      "The crop becomes resistant to the nematode Meloidegyne incognitia.",
      "The Bt toxin kills the cotton plant's own cells."]),
  "Consequences of growing Bt cotton",
  "NCERT: the Bt toxin gene expressed in plants provides resistance to insects without the need for insecticides, "
  "in effect a bio-pesticide; the cryIAc and cryIIAb proteins control the cotton bollworms. The toxin exists as an "
  "inactive protoxin; once an insect ingests it, the alkaline pH of the gut solubilises the crystals and activates "
  "it. Nematode resistance in tobacco was produced by RNAi, not Bt genes. The toxin acts on insect midgut cells, "
  "not on the plant.",
  ["(a), (b), (c): true", "(d) false - that was RNAi in tobacco", "(e) false - toxin acts only after activation in "
   "the insect gut"],
  "Biotechnological applications in agriculture",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (e) only"],
  why="Bt toxin is not a defence against nematodes and does not harm the plant, so options with (d) or (e) are "
      "wrong.", secs=55)

Z(BTA, "Biosafety, biopiracy and patents", I, D,
  "A multinational company uses a medicinal plant of a developing country, along with the traditional knowledge "
  "of its people, to make a commercial product, without proper authorisation from the country and people "
  "concerned and without compensatory payment. According to NCERT, this is:",
  "Recognising biopiracy",
  "NCERT: biopiracy is the term used to refer to the use of bio-resources by multinational companies and other "
  "organisations without proper authorisation from the countries and people concerned, without compensatory "
  "payment.",
  ["Bio-resource + traditional knowledge used", "No authorisation, no compensation -> biopiracy"],
  "Ethical issues",
  at="B", correct="Biopiracy",
  wrong=["Gene therapy", "Bioremediation", "Insertional inactivation"],
  why="Gene therapy corrects gene defects; bioremediation uses organisms to clean the environment; insertional "
      "inactivation is a method of selecting recombinants.", secs=30)

Z(BTA, "Bt crops and RNAi", I, STP,
  SP("In the RNAi-based protection of tobacco, the protective molecule produced in the host plant is a "
     "double-stranded RNA, not a toxic protein.",
     "In Bt cotton, the protective molecule is a protein encoded by a gene taken from a bacterium."),
  "RNAi versus Bt: the protective molecule",
  "In the RNAi strategy, nematode-specific DNA produced both sense and anti-sense RNA; being complementary, they "
  "formed dsRNA that silenced a specific mRNA of the nematode. In Bt cotton, the cry genes from Bacillus "
  "thuringiensis encode Bt toxin, an insecticidal protein.",
  ["Statement I: true (dsRNA silences the parasite's mRNA)", "Statement II: true (Bt toxin is a protein)"],
  "Biotechnological applications in agriculture", ans="A",
  why="Both statements are true, so every option calling either of them false is wrong.", secs=40)

Z(BTA, "Human insulin", I, ASR,
  AR("Insulin extracted from the pancreas of slaughtered cattle and pigs caused some patients to develop allergy or "
     "other types of reactions.",
     "Insulin from an animal source is a foreign protein for the human body."),
  "Why animal insulin caused reactions",
  "NCERT: insulin used for diabetes was earlier extracted from the pancreas of slaughtered cattle and pigs. Insulin "
  "from an animal source caused some patients to develop allergy or other types of reactions to the foreign "
  "protein. The reactions occurred because the protein was foreign to the human body, so R explains A.",
  ["A: true", "R: true", "Reactions were 'to the foreign protein' -> R explains A"],
  "Biotechnological applications in medicine (genetically engineered insulin)", ans="A",
  why="R is the stated cause of A, so B is wrong; both are true, so C and D are wrong.", secs=40)

Z(BTA, "Gene therapy", A, MAT,
  ML(("approach to ADA deficiency", "what NCERT says about it"),
     ["Enzyme replacement therapy", "Bone marrow transplantation",
      "Infusion of genetically engineered lymphocytes",
      "Introducing the ADA gene into cells at early embryonic stages"],
     ["Can cure the deficiency in some children",
      "Functional ADA is injected, but the treatment is not completely curative",
      "Could be a permanent cure",
      "Must be repeated periodically because the cells are not immortal"]),
  "Treatments of ADA deficiency",
  "NCERT: ADA deficiency can be cured by bone marrow transplantation in some children; in others it is treated by "
  "enzyme replacement therapy, in which functional ADA is given by injection, but neither approach is completely "
  "curative. Genetically engineered lymphocytes are not immortal, so the patient needs periodic infusions. If the "
  "gene isolated from marrow cells producing ADA is introduced into cells at early embryonic stages, it could be a "
  "permanent cure.",
  ["A - II", "B - I", "C - IV", "D - III"],
  "Gene therapy",
  at="C", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="The other codes swap enzyme replacement with marrow transplantation, the lymphocyte infusions with the "
      "embryonic approach, or marrow transplantation with lymphocyte infusions.", secs=60)

Z(BTA, "Bt crops and RNAi", A, D,
  "Suppose that, in the RNAi strategy against Meloidegyne incognitia, the introduced nematode-specific DNA produced "
  "only sense RNA in the tobacco cells and no anti-sense RNA. What would be the most likely result?",
  "Requirement of dsRNA for RNAi",
  "NCERT: the introduction of DNA produced both sense and anti-sense RNA in the host cells. These two RNAs, being "
  "complementary to each other, formed a double-stranded RNA (dsRNA) that initiated RNAi and silenced the specific "
  "mRNA of the nematode. Without anti-sense RNA, no dsRNA forms, so RNAi is not initiated and the nematode mRNA is "
  "not silenced.",
  ["RNAi needs dsRNA", "dsRNA = sense + complementary anti-sense RNA", "No anti-sense -> no dsRNA -> no silencing"],
  "Biotechnological applications in agriculture",
  at="D", correct="No dsRNA would form, so RNAi would not be initiated and the plant would not be protected",
  wrong=["The sense RNA alone would silence the nematode mRNA even more effectively",
         "The tobacco plant's own mRNA would be silenced instead",
         "The plant would start producing Bt toxin"],
  why="Silencing requires a complementary dsRNA, which needs both strands; nothing in the set-up targets the "
      "plant's own mRNA; Bt toxin genes are not involved in this strategy.", secs=55)

Z(BTA, "Transgenic animals", A, D,
  "Transgenic animals are made in which the formation of insulin-like growth factor is altered, so that its "
  "biological role can be learnt. Among the reasons NCERT gives for producing transgenic animals, this is an "
  "example of:",
  "Classifying a use of transgenic animals",
  "NCERT lists the uses of transgenic animals as normal physiology and development, study of disease, biological "
  "products, vaccine safety and chemical safety testing. Under normal physiology and development, NCERT notes that "
  "transgenic animals can be designed to study how genes are regulated and how they affect normal body functions "
  "and development, e.g., the study of complex factors involved in growth such as insulin-like growth factor: by "
  "introducing genes from other species that alter its formation and studying the effects, its biological role "
  "is learnt.",
  ["Aim: learn the normal biological role of a growth factor", "-> 'normal physiology and development'"],
  "Transgenic animals",
  at="B", correct="Normal physiology and development",
  wrong=["Vaccine safety", "Chemical (toxicity) safety testing", "Biological products"],
  why="Vaccine safety concerns testing vaccines (e.g., polio in mice); chemical safety testing uses animals more "
      "sensitive to toxic substances; biological products are useful human proteins such as α-1-antitrypsin made "
      "by the animal.", secs=40)

Z(BTA, "Gene therapy", A, MUL,
  MS("Which of the following statements about the vectors used in NCERT's examples are correct?",
     ["Nematode-specific genes were introduced into tobacco plants using vectors derived from Agrobacterium.",
      "In the gene therapy for ADA deficiency, a functional ADA cDNA was introduced into the patient's lymphocytes "
      "using a retroviral vector.",
      "Eli Lilly produced the insulin chains using a retroviral vector in human cells.",
      "The ADA cDNA was introduced into lymphocytes using Agrobacterium tumefaciens.",
      "The tobacco RNAi strategy used a retroviral vector."]),
  "Vectors in applied biotechnology",
  "NCERT: for RNAi in tobacco, nematode-specific genes were introduced into the host plant using Agrobacterium "
  "vectors. In gene therapy for ADA deficiency, a functional ADA cDNA was introduced into lymphocytes using a "
  "retroviral vector. Eli Lilly introduced the DNA sequences for chains A and B into plasmids of E. coli.",
  ["(a) true", "(b) true", "(c) false - E. coli plasmids", "(d), (e) false - vectors swapped"],
  "Biotechnological applications in agriculture; Gene therapy",
  at="A", correct="(a) and (b) only",
  wrong=["(b), (c) and (d) only", "(a), (b) and (e) only", "(c), (d) and (e) only"],
  why="Agrobacterium is the plant vector and the retrovirus the animal vector here; insulin chains were made in "
      "E. coli plasmids. Options including (c), (d) or (e) are wrong.", secs=55)

Z(BTA, "Transgenic animals", A, MUL,
  MS("Which of the following are examples NCERT gives under 'biological products' obtained or being sought from "
     "transgenic animals?",
     ["Human protein (α-1-antitrypsin) used to treat emphysema",
      "Human α-lactalbumin in the milk of the transgenic cow Rosie",
      "Attempts towards treatment of phenylketonuria (PKU) and cystic fibrosis",
      "Testing the safety of the polio vaccine in transgenic mice",
      "Animals made more sensitive to toxic substances to test the safety of drugs"]),
  "Biological products from transgenic animals",
  "NCERT (biological products): transgenic animals have been used to produce human protein (α-1-antitrypsin) to "
  "treat emphysema; similar attempts are being made for treatment of PKU and cystic fibrosis; in 1997 the first "
  "transgenic cow, Rosie, produced milk containing human α-lactalbumin. Polio vaccine testing is 'vaccine safety' "
  "and more sensitive animals are 'chemical safety testing'.",
  ["(a), (b), (c): biological products", "(d): vaccine safety", "(e): chemical safety testing"],
  "Transgenic animals",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(d) and (e) only", "(a) and (e) only"],
  why="(d) and (e) belong to other NCERT categories (vaccine safety and chemical safety testing), so options "
      "including them are wrong.", secs=50)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 121
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_005", "created_at": TODAY,
           "notes": "ZOO_005_p2: 121 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers re-derived in tools/batch_005/ZOO_005_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
