"""Builder for package ZOO_007_p2 of BATCH_007 (Zoology, 125 questions, NEET_ZOO_001626..NEET_ZOO_001750).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_007/ZOO_007_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_007_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_007_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_007_ZOO_p2.json"
FIRST_ID = 1626

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


# ================================================================ Chemical Coordination and Integration (5/6/5)
Z(CCI, "Mechanism of hormone action", B, D,
  "NCERT notes that the classical definition of a hormone (a chemical produced by an endocrine gland, released "
  "into the blood and carried to a distantly located target organ) has only limited current scope. Hormones are "
  "now defined as non-nutrient chemicals which act as intercellular messengers and are produced in trace amounts. "
  "Why is the newer definition preferred?",
  "Definition of hormones",
  "NCERT: the new definition covers a number of new molecules in addition to the hormones secreted by the "
  "organised endocrine glands. The old definition tied a hormone to an organised gland and to transport in the "
  "blood to a distant organ, which leaves out many chemical messengers known today.",
  ["Old definition: organised gland -> blood -> distant target", "New definition: any non-nutrient "
   "intercellular messenger made in trace amounts", "So it also covers new molecules not made by organised glands"],
  "Endocrine Glands and Hormones",
  at="C", correct="It covers a number of new molecules in addition to the hormones secreted by the organised "
                  "endocrine glands",
  wrong=["It restricts the term hormone to the secretions of the organised endocrine glands only",
         "It includes nutrients such as glucose and amino acids that cells need in large amounts",
         "It applies only to invertebrates, which have very simple endocrine systems"],
  why="The newer definition widens, not narrows, the term; it explicitly says non-nutrient and trace amounts, so "
      "nutrients needed in bulk are excluded; and it applies to vertebrates too, which have many hormones.",
  secs=40)

Z(CCI, "Hormonal disorders", B, D,
  "According to NCERT, under-production of hormones by the adrenal cortex causes acute weakness and fatigue, "
  "leading to Addison's disease. This happens because the under-production alters:",
  "Addison's disease",
  "NCERT: underproduction of hormones by the adrenal cortex alters carbohydrate metabolism, causing acute "
  "weakness and fatigue, leading to a disease called Addison's disease. (Glucocorticoids such as cortisol are the "
  "corticoids involved in carbohydrate metabolism.)",
  ["Adrenal cortex hormones (glucocorticoids) regulate carbohydrate metabolism",
   "Too little of them -> carbohydrate metabolism altered -> weakness and fatigue"],
  "Adrenal Gland",
  at="A", correct="Carbohydrate metabolism",
  wrong=["The calcium balance between bones and blood",
         "The 24-hour (diurnal) rhythm of the body",
         "Pigmentation, by acting on the melanocytes"],
  why="Calcium balance is the work of PTH and TCT, the diurnal rhythm is regulated by melatonin of the pineal, and "
      "pigmentation by MSH; none of these is how NCERT explains Addison's disease.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "The follicular cells of the thyroid gland synthesise two hormones. One of them, thyroxine (T₄), is chemically:",
  "Thyroid hormones",
  "NCERT: the follicular cells synthesise two hormones, tetraiodothyronine or thyroxine (T₄) and "
  "triiodothyronine (T₃). The subscript gives the number of iodine atoms, which is why iodine is essential for "
  "their normal rate of synthesis.",
  ["Thyroxine = tetraiodothyronine (T₄)", "The other hormone = triiodothyronine (T₃)"],
  "Thyroid Gland",
  at="D", correct="Tetraiodothyronine",
  wrong=["Triiodothyronine", "Thyrocalcitonin", "Thyroid stimulating hormone"],
  why="Triiodothyronine is T₃, the other follicular hormone; thyrocalcitonin is a protein hormone of the thyroid "
      "that regulates blood calcium; TSH is made by the anterior pituitary, not the thyroid.", secs=20)

Z(CCI, "Mechanism of hormone action", B, D,
  "According to NCERT, what does the formation of a hormone-receptor complex in a target tissue lead to?",
  "Hormone-receptor complex",
  "NCERT: hormone-receptor complex formation leads to certain biochemical changes in the target tissue. Target "
  "tissue metabolism, and hence physiological functions, are regulated by hormones in this way.",
  ["Hormone binds its specific receptor -> hormone-receptor complex", "Complex -> biochemical changes in the "
   "target tissue -> metabolism and functions regulated"],
  "Mechanism of Hormone Action",
  at="B", correct="Certain biochemical changes in the target tissue, through which its metabolism and "
                  "physiological functions are regulated",
  wrong=["Destruction of the target cell, so that the hormone is released back into the blood",
         "Secretion of the same hormone by the target cell, which then acts back on the endocrine gland",
         "Conversion of the hormone into a nutrient that the target cell uses as a source of energy"],
  why="NCERT says nothing of cell destruction or of the target cell secreting the same hormone, and hormones are "
      "defined as non-nutrient chemicals, so they are not used as an energy source.", secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, STP,
  SP("Iodine is essential for the normal rate of hormone synthesis in the thyroid gland.",
     "Parathyroid hormone, along with thyrocalcitonin, plays a significant role in calcium balance in the body."),
  "Thyroid and parathyroid",
  "Statement I is NCERT's own line on iodine and thyroid hormone synthesis. Statement II is also NCERT: PTH is "
  "hypercalcemic and, along with TCT (a protein hormone of the thyroid that regulates blood calcium levels), "
  "plays a significant role in calcium balance.",
  ["Statement I: true (iodine needed for T₄/T₃ synthesis)", "Statement II: true (PTH + TCT -> calcium balance)"],
  "Thyroid Gland; Parathyroid Gland", ans="A",
  why="Both statements are correct NCERT statements, so every option that calls either of them false is wrong.",
  secs=30)

Z(CCI, "Hypothalamus and pituitary", I, D,
  "How many of the following hormones are secreted by the pars distalis of the human pituitary?\n\n"
  "Growth hormone, MSH, prolactin, vasopressin, ACTH, oxytocin, FSH, TSH",
  "Hormones of the pars distalis",
  "NCERT: the pars distalis produces GH, PRL, TSH, ACTH, LH and FSH. The pars intermedia secretes only one "
  "hormone, MSH. Oxytocin and vasopressin are synthesised by the hypothalamus and released from the "
  "neurohypophysis (pars nervosa). From the list, GH, prolactin, ACTH, FSH and TSH are pars distalis hormones.",
  ["Pars distalis: GH, PRL, TSH, ACTH, LH, FSH", "In the list: GH, prolactin, ACTH, FSH, TSH = 5",
   "MSH -> pars intermedia; vasopressin, oxytocin -> released from the neurohypophysis"],
  "The Pituitary Gland",
  at="B", correct="Five", wrong=["Four", "Six", "Eight"],
  why="Six counts MSH (pars intermedia) or one of the neurohypophysis hormones; eight counts every hormone; four "
      "leaves out one of GH, prolactin, ACTH, FSH or TSH.", secs=40)

Z(CCI, "Hormonal disorders", I, MUL,
  MS("Which of the following disorders result from too little of a hormone (hyposecretion or impaired release) "
     "rather than from too much of it?",
     ["Cretinism", "Acromegaly", "Pituitary dwarfism", "Exophthalmic goitre", "Diabetes insipidus"]),
  "Hypo- and hypersecretion disorders",
  "NCERT: cretinism results from hypothyroidism during pregnancy; pituitary dwarfism from low secretion of "
  "growth hormone; diabetes insipidus from impaired synthesis or release of ADH. Acromegaly is due to excess "
  "growth hormone in adults, and exophthalmic goitre is a form of hyperthyroidism.",
  ["(a) hypothyroidism -> too little", "(b) excess GH -> too much", "(c) low GH -> too little",
   "(d) hyperthyroidism -> too much", "(e) impaired ADH release -> too little"],
  "The Pituitary Gland; Thyroid Gland",
  at="D", correct="(a), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(b), (d) and (e) only", "(c), (d) and (e) only"],
  why="Every wrong option includes acromegaly (excess GH) or exophthalmic goitre (excess thyroid hormone), which "
      "are disorders of over-secretion.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, MAT,
  ML(("hormone", "cells or tissue on which NCERT says it mainly acts"),
     ["Glucagon", "Insulin", "Aldosterone", "MSH"],
     ["Melanocytes", "Renal tubules", "Hepatocytes and adipocytes", "Hepatocytes (liver cells)"]),
  "Target cells of hormones",
  "NCERT: glucagon acts mainly on liver cells (hepatocytes); insulin acts mainly on hepatocytes and adipocytes "
  "(cells of adipose tissue); aldosterone acts mainly at the renal tubules; MSH acts on the melanocytes and "
  "regulates pigmentation of the skin.",
  ["Glucagon -> IV", "Insulin -> III", "Aldosterone -> II", "MSH -> I"],
  "The Pituitary Gland; Adrenal Gland; Pancreas",
  at="C", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="The trap is glucagon versus insulin: glucagon acts mainly on hepatocytes alone, insulin on hepatocytes and "
      "adipocytes. The other wrong codes swap aldosterone (kidney) with MSH (melanocytes) or with glucagon.",
  secs=45)

Z(CCI, "Mechanism of hormone action", I, ASR,
  AR("A hormone released into the blood reaches almost all the tissues of the body, yet it acts only on certain "
     "tissues.",
     "Hormones produce their effects by binding to specific hormone receptors, which are located in the target "
     "tissues only."),
  "Specificity of hormone action",
  "NCERT: hormones produce their effects on target tissues by binding to specific proteins called hormone "
  "receptors located in the target tissues only. So although the blood carries a hormone everywhere, only the "
  "tissues that have its receptors respond. R is the reason for A.",
  ["A: true - the blood carries the hormone widely but only target tissues respond",
   "R: true - receptors are present in target tissues only", "No receptor -> no hormone-receptor complex -> no "
   "effect, so R explains A"],
  "Mechanism of Hormone Action", ans="A",
  why="Both statements are true, and the location of receptors only in target tissues is exactly why other "
      "tissues do not respond, so the options saying R is not the explanation, or that either is false, are wrong.",
  secs=40)

Z(CCI, "Adrenal, pancreas and gonads", I, MAT,
  ML(("secretion of the adrenal gland", "action described in NCERT"),
     ["Cortisol", "Aldosterone", "Adrenaline", "Androgenic steroids of the adrenal cortex"],
     ["Growth of axial hair, pubic hair and facial hair during puberty",
      "Increased heartbeat, pupillary dilation and piloerection in an emergency",
      "Reabsorption of Na⁺ and water, and excretion of K⁺ and phosphate ions, by the renal tubules",
      "Anti-inflammatory reactions and suppression of the immune response"]),
  "Hormones of the adrenal cortex and medulla",
  "NCERT: cortisol produces anti-inflammatory reactions and suppresses the immune response; aldosterone acts at "
  "the renal tubules, stimulating reabsorption of Na⁺ and water and excretion of K⁺ and phosphate ions; "
  "adrenaline (a catecholamine of the medulla) increases heartbeat, alertness, pupillary dilation, piloerection "
  "and sweating; small amounts of androgenic steroids from the cortex play a role in the growth of axial, pubic "
  "and facial hair during puberty.",
  ["Cortisol -> IV", "Aldosterone -> III", "Adrenaline -> II", "Adrenal androgens -> I"],
  "Adrenal Gland",
  at="A", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The wrong codes swap the two corticoids (glucocorticoid action versus mineralocorticoid action), give "
      "adrenaline the hair-growth role of the adrenal androgens, or give aldosterone the emergency actions of the "
      "medulla.", secs=50)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("In the human body, androgens are secreted only by the Leydig cells of the testis.",
     "Androgens act on the central neural system and influence male sexual behaviour (libido)."),
  "Sources and actions of androgens",
  "Statement I is false: besides the Leydig cells, NCERT says the adrenal cortex also secretes small amounts of "
  "androgenic steroids, which play a role in the growth of axial, pubic and facial hair during puberty. "
  "Statement II is NCERT's description of androgen action.",
  ["Statement I: false - the adrenal cortex also secretes small amounts of androgenic steroids",
   "Statement II: true"],
  "Adrenal Gland; Testis", ans="D",
  why="Statement I fails because of the word 'only'; Statement II is correct, so 'both true', 'both false' and "
      "'I true, II false' are wrong.", secs=35)

Z(CCI, "Hypothalamus and pituitary", A, D,
  "In a woman with otherwise normal hormone levels, the anterior pituitary fails to produce the rapid mid-cycle "
  "surge of LH, although FSH secretion and the growth of the follicles are normal. Which outcome is expected in "
  "that cycle?",
  "Role of LH in ovulation and the corpus luteum",
  "NCERT: in females, LH induces ovulation of fully mature (Graafian) follicles and maintains the corpus luteum "
  "formed from the remnants of the Graafian follicle after ovulation. The rapid secretion of LH in mid-cycle (LH "
  "surge) induces rupture of the Graafian follicle. Without the surge the follicle does not rupture, so no ovum "
  "is released, no corpus luteum forms, and the progesterone it would secrete is not produced.",
  ["Follicles grow (FSH normal) up to the Graafian stage", "No LH surge -> Graafian follicle does not rupture "
   "-> no ovulation", "No ovulation -> no corpus luteum -> no luteal progesterone"],
  "The Pituitary Gland; also Class 12 Biology, Ch 2 'Human Reproduction', Menstrual Cycle",
  at="B", correct="The Graafian follicle does not rupture, so no ovum is released and no corpus luteum forms to "
                  "secrete progesterone",
  wrong=["Ovulation occurs normally, but the endometrium fails to regenerate during the follicular phase",
         "The corpus luteum forms but secretes mainly estrogen instead of progesterone",
         "Follicles fail to grow beyond the primary stage because estrogen is not secreted"],
  why="Ovulation itself needs the LH surge, so it cannot occur normally; no corpus luteum can form without "
      "ovulation; and the stem says FSH and follicle growth are normal, so follicles do develop and secrete "
      "estrogen.", secs=60)

Z(CCI, "Mechanism of hormone action", A, D,
  "A person's β-cells secrete normal amounts of insulin, but the hepatocytes and adipocytes lack functional "
  "insulin receptors. Which of the following is expected?",
  "Hormones act only through their receptors",
  "NCERT: hormones produce their effects only by binding to specific receptors in the target tissues, and each "
  "receptor is specific to one hormone. Insulin acts mainly on hepatocytes and adipocytes to enhance cellular "
  "glucose uptake and utilisation. If these cells have no working insulin receptors, insulin in the blood cannot "
  "form a hormone-receptor complex, glucose is not moved from the blood into these cells, and blood glucose "
  "stays high even though insulin is present.",
  ["Insulin present in the blood", "No receptor on target cells -> no hormone-receptor complex -> no effect",
   "Glucose uptake by hepatocytes and adipocytes not enhanced -> hyperglycemia persists"],
  "Mechanism of Hormone Action; Pancreas",
  at="D", correct="Blood glucose stays high, because insulin can act on its target cells only after binding to "
                  "its specific receptors",
  wrong=["Blood glucose falls sharply, because unbound insulin acts directly on the genome of the target cells",
         "Blood glucose stays normal, because glucagon receptors take over the action of insulin",
         "Blood glucose stays normal, because insulin enters the cells and acts without any receptor"],
  why="Unbound hormone has no effect; receptors are specific, so glucagon receptors cannot respond to insulin "
      "(and glucagon raises blood sugar anyway); and NCERT says hormones act through receptors, not without them.",
  secs=55)

Z(CCI, "Adrenal, pancreas and gonads", A, MUL,
  MS("A tumour of the adrenal cortex secretes excess cortisol. Based on the actions of glucocorticoids described "
     "in NCERT, which of the following are expected?",
     ["Increased gluconeogenesis, tending to raise the blood glucose level",
      "Suppression of the immune response",
      "Increased cellular uptake and utilisation of amino acids",
      "Increased production of RBCs",
      "Increased secretion of adrenaline by the adrenal cortex"]),
  "Effects of excess glucocorticoid",
  "NCERT: glucocorticoids stimulate gluconeogenesis, lipolysis and proteolysis and inhibit cellular uptake and "
  "utilisation of amino acids; cortisol produces anti-inflammatory reactions and suppresses the immune response; "
  "cortisol stimulates RBC production. Adrenaline is a hormone of the adrenal medulla, not the cortex.",
  ["(a) true - gluconeogenesis stimulated", "(b) true - immune response suppressed",
   "(c) false - amino acid uptake is inhibited", "(d) true - RBC production stimulated",
   "(e) false - adrenaline comes from the medulla"],
  "Adrenal Gland",
  at="A", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only"],
  why="(c) reverses the NCERT action (glucocorticoids inhibit amino-acid uptake and utilisation), and (e) gives "
      "the cortex a medullary hormone, so any option containing them is wrong.", secs=60)

Z(CCI, "Hormonal disorders", A, STP,
  SP("Enlargement of the thyroid gland (goitre) is seen in iodine deficiency, a hypothyroid condition.",
     "Enlargement of the thyroid gland is also seen in exophthalmic goitre, a condition in which the basal "
     "metabolic rate is increased."),
  "Goitre in hypo- and hyperthyroidism",
  "NCERT: deficiency of iodine in the diet results in hypothyroidism and enlargement of the thyroid gland, "
  "commonly called goitre. Exophthalmic goitre is a form of hyperthyroidism characterised by enlargement of the "
  "thyroid gland, protrusion of the eyeballs, increased basal metabolic rate and weight loss. So an enlarged "
  "thyroid by itself does not tell whether thyroid hormone is too little or too much.",
  ["Statement I: true - iodine deficiency -> hypothyroidism + goitre",
   "Statement II: true - exophthalmic goitre (hyperthyroid) also has an enlarged thyroid, with raised BMR"],
  "Thyroid Gland", ans="A",
  why="Students often link an enlarged thyroid only with iodine deficiency and mark Statement II false, but NCERT "
      "describes thyroid enlargement in both conditions.", secs=45)

Z(CCI, "Hypothalamus and pituitary", A, ASR,
  AR("In a man whose pituitary secretes FSH normally but no LH, the secretion of androgens remains normal.",
     "In males, LH acts on the Leydig cells and stimulates the synthesis and secretion of androgens."),
  "LH and androgen secretion",
  "R is NCERT's description of LH action in males. Because LH is the hormone that stimulates the Leydig cells, a "
  "man with no LH would have low androgen secretion even if FSH is normal; FSH (with androgens) regulates "
  "spermatogenesis but does not drive androgen synthesis. So A is false.",
  ["R: true - LH stimulates Leydig cells to make androgens", "No LH -> Leydig cells not stimulated -> "
   "androgens fall", "Normal FSH does not replace LH, so A is false"],
  "The Pituitary Gland; Testis", ans="D",
  why="A is false, so the two 'both true' options and 'A true but R false' are wrong.", secs=45)

# ================================================================ Human Reproduction (6/8/6)
LOBULES, TUBULES_MIN, TUBULES_MAX = 250, 1, 3
assert (LOBULES * TUBULES_MIN, LOBULES * TUBULES_MAX) == (250, 750)
Z(HR, "Male and female reproductive systems", B, NUM,
  "Each human testis has about 250 compartments called testicular lobules, and each lobule contains one to "
  "three highly coiled seminiferous tubules. On this basis, the number of seminiferous tubules in one testis is "
  "expected to lie in the range of about:",
  "Structure of the testis",
  "NCERT: each testis has about 250 testicular lobules, and each lobule contains one to three highly coiled "
  "seminiferous tubules. Minimum = 250 x 1 = 250; maximum = 250 x 3 = 750.",
  ["Minimum: 250 lobules x 1 tubule = 250", "Maximum: 250 lobules x 3 tubules = 750"],
  "The Male Reproductive System",
  at="B", correct="250 to 750", wrong=["83 to 250", "250 to 500", "500 to 1,500"],
  why="83 to 250 divides instead of multiplying; 250 to 500 takes at most two tubules per lobule; 500 to 1,500 "
      "counts both testes, not one.", secs=30, vb=RECOMPUTED)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "According to NCERT, parturition (the delivery of the foetus at the end of pregnancy) is induced by:",
  "Mechanism of parturition",
  "NCERT: parturition is induced by a complex neuroendocrine mechanism. Signals from the fully developed foetus "
  "and the placenta induce mild uterine contractions (foetal ejection reflex), which trigger the release of "
  "oxytocin from the maternal pituitary.",
  ["Parturition = complex neuroendocrine mechanism", "Foetal and placental signals -> foetal ejection reflex "
   "-> oxytocin -> stronger contractions"],
  "Pregnancy and Embryonic Development; Parturition and Lactation",
  at="C", correct="A complex neuroendocrine mechanism",
  wrong=["A purely neural reflex of the mother, without the involvement of any hormone",
         "A sudden fall in hCG secreted by the corpus luteum",
         "Uterine contractions caused by estrogens from the growing ovarian follicles"],
  why="Oxytocin, a hormone, is part of the mechanism, so it is not purely neural; hCG is made by the placenta, "
      "not the corpus luteum; growing follicles and their estrogens are not part of NCERT's account of "
      "parturition.", secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "The seminiferous tubules of the human testis open into the vasa efferentia through the:",
  "Male duct system",
  "NCERT: the seminiferous tubules of the testis open into the vasa efferentia through the rete testis. The vasa "
  "efferentia leave the testis and open into the epididymis.",
  ["Seminiferous tubules -> rete testis -> vasa efferentia -> epididymis"],
  "The Male Reproductive System",
  at="D", correct="Rete testis", wrong=["Epididymis", "Ejaculatory duct", "Urethral meatus"],
  why="The epididymis lies after the vasa efferentia, the ejaculatory duct is formed where the vas deferens "
      "receives the duct of the seminal vesicle, and the urethral meatus is the external opening of the urethra.",
  secs=20)

Z(HR, "Male and female reproductive systems", B, D,
  "Counting each gland separately, how many male accessory glands are present in a human male?",
  "Male accessory glands",
  "NCERT: the male accessory glands include paired seminal vesicles, a prostate and paired bulbourethral glands. "
  "Counting each gland separately: 2 + 1 + 2 = 5.",
  ["Seminal vesicles: 2", "Prostate: 1", "Bulbourethral glands: 2", "Total = 5"],
  "The Male Reproductive System",
  at="C", correct="Five", wrong=["Three", "Four", "Six"],
  why="Three counts only the kinds of gland; four treats one pair as single; six wrongly makes the prostate "
      "paired.", secs=25)

Z(HR, "Male and female reproductive systems", B, ASR,
  AR("The testes of a human male are situated outside the abdominal cavity, within a pouch called the scrotum.",
     "Each testis has about 250 compartments called testicular lobules."),
  "Position and structure of the testis",
  "Both are NCERT facts. A is about where the testes lie (the scrotum keeps them 2-2.5 °C below body "
  "temperature, which is needed for spermatogenesis). R is about the internal structure of the testis. The "
  "number of lobules has nothing to do with the position of the testes, so R does not explain A.",
  ["A: true", "R: true", "R describes internal structure, not the reason for the position -> not the "
   "explanation"],
  "The Male Reproductive System", ans="B",
  why="Both statements are true, so the options calling either false are wrong; the reason for the scrotal "
      "position is temperature, not the number of lobules, so R is not the correct explanation.", secs=30)

Z(HR, "Gametogenesis", B, STP,
  SP("Spermatogonia present on the inside wall of the seminiferous tubules multiply by mitotic division and "
     "increase in number.",
     "Primary spermatocytes contain 23 chromosomes each."),
  "Spermatogenesis",
  "NCERT: spermatogonia, the diploid male germ cells on the inside wall of the seminiferous tubules, multiply by "
  "mitosis. Some of them, called primary spermatocytes, periodically undergo meiosis. A primary spermatocyte has "
  "not yet divided by meiosis, so it is diploid with 46 chromosomes; only after the first meiotic division do "
  "the secondary spermatocytes have 23 chromosomes.",
  ["Statement I: true", "Statement II: false - primary spermatocytes have 46; secondary spermatocytes have 23"],
  "Gametogenesis", ans="C",
  why="Statement II confuses primary with secondary spermatocytes, so the options calling it true are wrong; "
      "Statement I is correct, so 'both false' and 'I false, II true' are wrong.", secs=30)

OOCYTES = 25
POLAR_BODIES = OOCYTES * 1 + OOCYTES * 1   # one first polar body + one second polar body per oocyte
assert POLAR_BODIES == 50
Z(HR, "Gametogenesis", I, NUM,
  "In a human female, 25 primary oocytes complete the first meiotic division. Every secondary oocyte so formed "
  "is then entered by a sperm and completes the second meiotic division. Assuming that the first polar bodies do "
  "not divide further, how many polar bodies are formed in all?",
  "Polar bodies in oogenesis",
  "NCERT: the primary oocyte completes the first meiotic division, an unequal division forming a large haploid "
  "secondary oocyte and a tiny first polar body. When a sperm enters, the secondary oocyte completes the second "
  "meiotic division, again unequal, forming a second polar body and a haploid ovum (ootid). Each primary oocyte "
  "therefore gives 1 ovum and, here, 2 polar bodies: 25 x 2 = 50.",
  ["Per primary oocyte: 1 first polar body + 1 second polar body = 2", "25 x 2 = 50 polar bodies",
   "(and 25 ova)"],
  "Gametogenesis",
  at="B", correct="50", wrong=["25", "75", "100"],
  why="25 counts only one polar body per oocyte; 75 adds the ova to the polar bodies; 100 assumes four products "
      "per oocyte as in spermatogenesis.", secs=40, vb=RECOMPUTED)

Z(HR, "Male and female reproductive systems", I, D,
  "Which of the following shows the correct path of milk in the human mammary gland, from the cells that "
  "secrete it to the duct through which it is sucked out?",
  "Structure of the mammary gland",
  "NCERT: the cells of the alveoli secrete milk, stored in the cavities of the alveoli. The alveoli open into "
  "mammary tubules. The tubules of each lobe join to form a mammary duct. Several mammary ducts join to form a "
  "wider mammary ampulla, which is connected to the lactiferous duct through which milk is sucked out.",
  ["Alveoli -> mammary tubules", "Tubules of a lobe -> mammary duct", "Several ducts -> mammary ampulla",
   "Ampulla -> lactiferous duct"],
  "The Female Reproductive System",
  at="A", correct="Alveoli → mammary tubules → mammary duct → mammary ampulla → lactiferous duct",
  wrong=["Alveoli → mammary duct → mammary tubules → mammary ampulla → lactiferous duct",
         "Alveoli → mammary tubules → mammary ampulla → mammary duct → lactiferous duct",
         "Mammary tubules → alveoli → mammary duct → lactiferous duct → mammary ampulla"],
  why="Each wrong sequence swaps two neighbouring parts: tubules and duct, duct and ampulla, or starts from the "
      "tubules instead of the milk-secreting alveoli.", secs=40)

Z(HR, "Fertilisation and implantation", I, D,
  "The human zygote divides by mitosis (cleavage), forming 2, 4, 8, 16 daughter cells called blastomeres. NCERT "
  "calls an embryo with 8 to 16 blastomeres a morula. Assuming every blastomere divides at each round, after "
  "which numbers of completed rounds of cleavage is the embryo in this range?",
  "Cleavage and the morula",
  "Number of blastomeres after n rounds = 2ⁿ. 2³ = 8 and 2⁴ = 16, so the embryo has 8 to 16 blastomeres after 3 "
  "and after 4 rounds of cleavage. After 2 rounds it has only 4 cells; after 5 rounds it would have 32.",
  ["Cells after n rounds = 2ⁿ", "2³ = 8 and 2⁴ = 16 -> 3 and 4 rounds"],
  "Fertilisation and Implantation",
  at="C", correct="After 3 and after 4 rounds", wrong=["After 2 and after 3 rounds", "After 4 and after 5 rounds",
                                                         "After 8 and after 16 rounds"],
  why="Two rounds give only 4 cells and five rounds give 32; '8 and 16 rounds' confuses the number of cells "
      "with the number of divisions.", secs=35)

Z(HR, "Gametogenesis", I, ASR,
  AR("Each spermatid formed in a human male contains 46 chromosomes.",
     "Spermatids are formed when the secondary spermatocytes undergo the second meiotic division."),
  "Chromosome number in spermatids",
  "R is NCERT's description: the secondary spermatocytes undergo the second meiotic division to produce four "
  "equal, haploid spermatids. The secondary spermatocytes already have only 23 chromosomes after the first "
  "meiotic division, so each spermatid has 23 chromosomes, not 46. A is false.",
  ["Primary spermatocyte (46) -> meiosis I -> secondary spermatocytes (23 each)",
   "Meiosis II -> spermatids (23 each), so A is false", "R: true"],
  "Gametogenesis", ans="D",
  why="A is false because spermatids are haploid, so the options that call A true are wrong.", secs=35)

Z(HR, "Gametogenesis", I, MAT,
  ML(("cell", "where it is found"),
     ["Sertoli cells", "Leydig cells", "Granulosa cells", "Theca"],
     ["In the interstitial spaces outside the seminiferous tubules",
      "Around the oocyte in an ovarian follicle, starting as a single layer in the primary follicle",
      "Inside the seminiferous tubules, where they provide nutrition to the germ cells",
      "Around the secondary follicle, organised into an inner and an outer layer in the tertiary follicle"]),
  "Somatic cells of the testis and of ovarian follicles",
  "NCERT: each seminiferous tubule is lined by spermatogonia and Sertoli cells, which provide nutrition to the "
  "germ cells; the Leydig (interstitial) cells lie in the interstitial spaces outside the tubules. A primary "
  "oocyte surrounded by a layer of granulosa cells is a primary follicle; a secondary follicle has more layers of "
  "granulosa cells and a new theca; in the tertiary follicle the theca is organised into an inner theca interna "
  "and an outer theca externa.",
  ["Sertoli -> III", "Leydig -> I", "Granulosa -> II", "Theca -> IV"],
  "The Male Reproductive System; Gametogenesis",
  at="B", match=({"A": "III", "B": "I", "C": "II", "D": "IV"},
                 [{"A": "I", "B": "III", "C": "II", "D": "IV"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"}]),
  why="Sertoli cells are inside the tubules and Leydig cells outside, so swapping them is wrong; the granulosa "
      "layer is present from the primary follicle, whereas the theca appears only in the secondary follicle.",
  secs=50)

Z(HR, "Gametogenesis", I, MAT,
  ML(("process", "kind of cell division involved"),
     ["Cleavage of the zygote", "Formation of spermatids from secondary spermatocytes", "Spermiogenesis",
      "Formation of the secondary oocyte from the primary oocyte"],
     ["First meiotic division, unequal", "Mitosis", "Second meiotic division",
      "No cell division (transformation of a cell)"]),
  "Divisions in gametogenesis and development",
  "NCERT: cleavage is the mitotic division of the zygote; secondary spermatocytes undergo the second meiotic "
  "division to form spermatids; spermiogenesis transforms spermatids into spermatozoa without any division; the "
  "primary oocyte completes the first meiotic division, an unequal division, forming the secondary oocyte and the "
  "first polar body.",
  ["Cleavage -> II", "Spermatids -> III", "Spermiogenesis -> IV", "Secondary oocyte -> I"],
  "Gametogenesis; Fertilisation and Implantation",
  at="D", match=({"A": "II", "B": "III", "C": "IV", "D": "I"},
                 [{"A": "II", "B": "I", "C": "IV", "D": "III"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "II", "B": "III", "C": "I", "D": "IV"}]),
  why="Spermatids come from the second, not the first, meiotic division; cleavage is a true division (mitosis), "
      "whereas spermiogenesis involves no division; and the primary oocyte must divide (meiosis I) to give the "
      "secondary oocyte.", secs=45)

Z(HR, "Gametogenesis", I, MUL,
  MS("Which of the following events of oogenesis take place in a human female before her birth, that is, "
     "during her fetal life?",
     ["Formation of a couple of million gamete mother cells (oogonia) within each fetal ovary",
      "Entry of these cells into prophase-I of meiosis, where they are temporarily arrested as primary oocytes",
      "Completion of the first meiotic division to form the secondary oocyte",
      "Formation of a fluid-filled cavity called the antrum in the follicle",
      "Completion of the second meiotic division to form the ovum"]),
  "Timing of oogenesis",
  "NCERT: oogenesis is initiated during embryonic development, when a couple of million oogonia are formed "
  "within each fetal ovary; no more are formed after birth. These cells enter prophase-I of meiosis and are "
  "temporarily arrested as primary oocytes. The first meiotic division is completed within the tertiary follicle "
  "(after puberty, as follicles mature); the antrum appears in the tertiary follicle; the second meiotic division "
  "is completed only when a sperm enters the secondary oocyte.",
  ["(a) fetal life - yes", "(b) fetal life - yes", "(c) in the tertiary follicle, after puberty",
   "(d) tertiary follicle, after puberty", "(e) only at fertilisation"],
  "Gametogenesis",
  at="A", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
  why="Meiosis I is completed only in the tertiary follicle, the antrum belongs to the tertiary follicle, and "
      "meiosis II is completed at fertilisation, so (c), (d) and (e) are not fetal events.", secs=55)

Z(HR, "Fertilisation and implantation", I, STP,
  SP("The blastocyst becomes embedded in the endometrium because its trophoblast cells divide rapidly and cover "
     "it.",
     "The inner cell mass of the blastocyst gets differentiated as the embryo."),
  "Implantation",
  "NCERT: the trophoblast layer gets attached to the endometrium and the inner cell mass gets differentiated as "
  "the embryo. After attachment, it is the uterine cells that divide rapidly and cover the blastocyst, so that it "
  "becomes embedded in the endometrium (implantation). Statement I gives the dividing cells wrongly.",
  ["Statement I: false - the uterine cells, not the trophoblast, divide and cover the blastocyst",
   "Statement II: true"],
  "Fertilisation and Implantation", ans="D",
  why="Statement I is false and Statement II true; the other three combinations do not fit.", secs=35)

Z(HR, "Fertilisation and implantation", A, ASR,
  AR("Normally only one sperm fertilises a human ovum.",
     "Contact of a sperm with the zona pellucida layer of the ovum induces changes in the membrane that block "
     "the entry of additional sperms."),
  "Prevention of entry of more than one sperm",
  "NCERT: during fertilisation a sperm comes in contact with the zona pellucida layer of the ovum and induces "
  "changes in the membrane that block the entry of additional sperms. Thus it ensures that only one sperm can "
  "fertilise an ovum. R gives the mechanism of A.",
  ["A: true", "R: true", "The membrane change after the first sperm's contact blocks other sperms -> R explains A"],
  "Fertilisation and Implantation", ans="A",
  why="Both statements are true and NCERT itself links them ('thus it ensures that only one sperm can fertilise "
      "an ovum'), so B, C and D are wrong.", secs=35)

Z(HR, "Menstrual cycle", A, STP,
  SP("If a woman's corpus luteum kept secreting large amounts of progesterone beyond the end of her usual cycle, "
     "her endometrium would be maintained and menstruation would be delayed.",
     "In the absence of fertilisation, the corpus luteum degenerates, and this causes disintegration of the "
     "endometrium."),
  "Corpus luteum, progesterone and menstruation",
  "NCERT: in the luteal phase the corpus luteum secretes large amounts of progesterone, which is essential for "
  "maintenance of the endometrium; in the absence of fertilisation the corpus luteum degenerates, causing "
  "disintegration of the endometrium and leading to menstruation. It follows that continued progesterone "
  "secretion would keep the endometrium and delay menstruation - as indeed happens in pregnancy, when there is "
  "no menstruation.",
  ["Statement II: true (NCERT)", "Statement I: progesterone maintains the endometrium; its fall (corpus luteum "
   "degeneration) causes menstruation -> sustained progesterone delays menstruation -> true"],
  "Menstrual Cycle", ans="A",
  why="Statement I follows directly from the role of progesterone in maintaining the endometrium, and Statement "
      "II is NCERT text, so no option calling either false is correct.", secs=50)

Z(HR, "Male and female reproductive systems", A, MUL,
  MS("In a man, both seminal vesicles and the prostate are absent from birth, but the testes, the duct system "
     "and the bulbourethral glands are normal. Which of the following are expected?",
     ["Sperms are still formed in the seminiferous tubules.",
      "The volume of seminal plasma in his ejaculate is reduced.",
      "The maturation and motility of his sperms may be affected.",
      "Androgen secretion by his Leydig cells stops.",
      "Secretions of the bulbourethral glands are still available for lubrication of the penis."]),
  "Roles of the male accessory glands",
  "NCERT: the secretions of the male accessory glands (seminal vesicles, prostate, bulbourethral glands) "
  "constitute the seminal plasma; the secretions of the epididymis, vas deferens, seminal vesicle and prostate "
  "are essential for maturation and motility of sperms; bulbourethral secretions help in lubrication of the "
  "penis. Sperm formation and androgen secretion take place in the testis, which is normal.",
  ["(a) testis normal -> sperms formed", "(b) two of the three kinds of accessory gland missing -> less seminal "
   "plasma", "(c) seminal vesicle and prostate secretions are essential for maturation and motility",
   "(d) false - Leydig cells are in the normal testis", "(e) bulbourethral glands normal -> lubrication continues"],
  "The Male Reproductive System",
  at="C", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a) and (e) only"],
  why="(d) is wrong because androgens come from the Leydig cells of the testis, which is normal; the options "
      "that leave out (b) or (c) ignore NCERT's role of these glands in seminal plasma and in sperm maturation "
      "and motility.", secs=60)

Z(HR, "Fertilisation and implantation", A, MAT,
  ML(("defect", "most likely consequence"),
     ["The fimbriae of the infundibulum do not function",
      "After the trophoblast attaches, the uterine cells fail to divide",
      "The acrosome of the sperms lacks its enzymes",
      "The lactiferous ducts of a lactating mother are blocked"],
     ["Milk secreted in the alveoli cannot be sucked out",
      "The sperm cannot enter the ovum through the zona pellucida and the plasma membrane",
      "The blastocyst is not covered and embedded, so implantation fails",
      "The ovum released at ovulation is not collected into the oviduct"]),
  "Functions of reproductive structures",
  "NCERT: the fimbriae help in collection of the ovum after ovulation; after the trophoblast attaches, the "
  "uterine cells divide rapidly and cover the blastocyst, embedding it (implantation); secretions of the "
  "acrosome help the sperm enter the cytoplasm of the ovum through the zona pellucida and the plasma membrane; "
  "milk is sucked out through the lactiferous duct.",
  ["Fimbriae -> IV", "Uterine cells -> III", "Acrosome -> II", "Lactiferous duct -> I"],
  "The Female Reproductive System; Fertilisation and Implantation",
  at="A", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="Each wrong code gives one defect the consequence of another: fimbriae act before fertilisation (collecting "
      "the ovum), the uterine cells act at implantation, the acrosome at sperm entry, and the lactiferous duct in "
      "milk removal.", secs=50)

Z(HR, "Pregnancy, parturition and lactation", A, MUL,
  MS("During pregnancy the levels of several hormones rise in the mother's blood. Which of the following are "
     "hormones whose levels increase several-fold during pregnancy but which are ALSO produced in women who are "
     "not pregnant?",
     ["Estrogens", "hCG", "Prolactin", "hPL (human placental lactogen)", "Progestogens"]),
  "Hormones of pregnancy",
  "NCERT: hCG and hPL are produced in women only during pregnancy (by the placenta). In addition, during pregnancy the "
  "levels of other hormones, including estrogens, progestogens and prolactin, are increased several-fold in the "
  "maternal blood; these hormones are also made in women who are not pregnant (estrogens and progesterone by the "
  "ovary, prolactin by the anterior pituitary).",
  ["Only in pregnancy (placental): hCG, hPL -> (b), (d) excluded", "Increased several-fold but made anyway: "
   "estrogens, prolactin, progestogens -> (a), (c), (e)"],
  "Pregnancy and Embryonic Development",
  at="D", correct="(a), (c) and (e) only",
  wrong=["(b) and (d) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"],
  why="hCG and hPL are the trap: they are placental hormones produced in women only during pregnancy, so any option "
      "containing (b) or (d) is wrong; '(b) and (d) only' answers the opposite question.", secs=50)

Z(HR, "Pregnancy, parturition and lactation", A, D,
  "In a human foetus, the heart has formed and its sound can be heard through a stethoscope, but the limbs and "
  "digits have not yet developed. According to the timeline given in NCERT, the pregnancy is most likely:",
  "Timeline of foetal development",
  "NCERT: after one month of pregnancy the embryo's heart is formed, and the first sign of the growing foetus may "
  "be noticed by listening to the heart sound through a stethoscope. By the end of the second month the foetus "
  "develops limbs and digits. So a foetus with a heart but no limbs and digits is between about one and two "
  "months old.",
  ["Heart formed: after one month", "Limbs and digits: by the end of the second month",
   "Heart present, limbs absent -> between one and two months"],
  "Pregnancy and Embryonic Development",
  at="B", correct="Between about one and two months old",
  wrong=["In the fifth month, when the first movements of the foetus are usually observed",
         "At about 24 weeks, at the end of the second trimester",
         "At about 12 weeks, when most of the major organ systems have formed"],
  why="By 12 weeks, the fifth month and 24 weeks the limbs and digits (formed by the end of the second month) "
      "are already present, so none of these fits a foetus without limbs.", secs=45)

# ================================================================ Reproductive Health (4/5/4)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WINDOW_HOURS = 72
assert WINDOW_HOURS % 24 == 0 and DAYS[(DAYS.index("Monday") + WINDOW_HOURS // 24) % 7] == "Thursday"
Z(RH, "Contraception", B, NUM,
  "A woman had unprotected coitus at 9 p.m. on a Monday. According to NCERT, emergency contraceptives "
  "(progestogens or progestogen-estrogen combinations, or IUDs) are very effective if used within 72 hours of "
  "coitus. By what time at the latest should she use one?",
  "Emergency contraception",
  "NCERT: administration of progestogens or progestogen-estrogen combinations or IUDs within 72 hours of coitus "
  "has been found to be very effective as emergency contraceptives. 72 hours = 3 days, and 3 days after 9 p.m. "
  "on Monday is 9 p.m. on Thursday.",
  ["72 h = 72/24 = 3 days", "Monday 9 p.m. + 3 days = Thursday 9 p.m."],
  "Birth Control (Contraceptive Methods)",
  at="B", correct="9 p.m. on Thursday",
  wrong=["9 p.m. on Wednesday", "9 p.m. on Friday", "9 p.m. on the following Monday"],
  why="Wednesday allows only 48 hours, Friday 96 hours and the following Monday a full week; only Thursday is "
      "72 hours later.", secs=25, vb=RECOMPUTED)

Z(RH, "Contraception", B, D,
  "Which of the following pairs consists only of copper-releasing intra-uterine devices (IUDs)?",
  "Types of IUDs",
  "NCERT: IUDs are non-medicated (e.g., Lippes loop), copper-releasing (CuT, Cu7, Multiload 375) or "
  "hormone-releasing (Progestasert, LNG-20).",
  ["Copper-releasing: CuT, Cu7, Multiload 375", "Non-medicated: Lippes loop",
   "Hormone-releasing: Progestasert, LNG-20"],
  "Birth Control (Contraceptive Methods)",
  at="C", correct="CuT and Multiload 375",
  wrong=["Lippes loop and Cu7", "Progestasert and LNG-20", "CuT and Progestasert"],
  why="Lippes loop is non-medicated, and Progestasert and LNG-20 are hormone-releasing IUDs, so each of the "
      "other pairs contains at least one IUD that does not release copper.", secs=25)

Z(RH, "STDs and their prevention", B, D,
  "A young person had unprotected sex with an unknown partner a few weeks ago and has noticed no symptoms so "
  "far. According to NCERT, what is the best course of action?",
  "Early detection of STIs",
  "NCERT: early symptoms of STIs are minor, and infected persons (especially females) may often be "
  "asymptomatic, so infections may remain undetected for long. One of the simple principles for prevention is: "
  "in case of doubt, go to a qualified doctor for early detection and get complete treatment if diagnosed with "
  "an infection. Many STIs are completely curable if detected early and treated properly.",
  ["STIs often show absent or less significant early symptoms", "Doubt -> qualified doctor -> early detection "
   "-> complete treatment"],
  "Sexually Transmitted Infections (STIs)",
  at="A", correct="Go to a qualified doctor for early detection, and get complete treatment if an infection is "
                  "diagnosed",
  wrong=["Wait until symptoms appear, since an STI without symptoms is harmless",
         "Start taking oral contraceptive pills, which also protect against STIs",
         "Avoid going to a doctor, since STIs cannot be detected until AIDS develops"],
  why="Untreated STIs can lead to PID, infertility and other complications even when symptoms are minor; oral "
      "pills give no protection against STIs; and STIs can be detected early, which is why NCERT stresses early "
      "detection.", secs=30)

Z(RH, "Contraception", B, ASR,
  AR("Natural methods of contraception have almost no side effects.",
     "No medicines or devices are used in natural methods of contraception."),
  "Natural methods of contraception",
  "NCERT: natural methods (periodic abstinence, withdrawal, lactational amenorrhea) work on the principle of "
  "avoiding the chances of the ovum and sperms meeting. As no medicines or devices are used in these methods, "
  "side effects are almost nil (though chances of failure are high). R is the stated reason for A.",
  ["A: true", "R: true", "NCERT: 'as no medicines or devices are used ... side effects are almost nil' -> R "
   "explains A"],
  "Birth Control (Contraceptive Methods)", ans="A",
  why="Both statements are true and NCERT gives R as the reason for A, so B, C and D are wrong.", secs=30)

Z(RH, "STDs and their prevention", I, STP,
  SP("A woman who relies only on a hormone-releasing IUD is not protected against STIs from an infected partner.",
     "Because an IUD acts inside the uterus, it also destroys the viruses that cause hepatitis-B and HIV."),
  "Contraceptives and protection from STIs",
  "NCERT: hormone-releasing IUDs make the uterus unsuitable for implantation and the cervix hostile to sperms; "
  "they are not barriers. Of the contraceptives, NCERT credits condoms with protecting the user from STIs and "
  "AIDS, because they prevent contact with semen. So an IUD user is not protected against STIs (Statement I "
  "true), and nothing in NCERT says IUDs destroy viruses (Statement II false).",
  ["Statement I: true - IUDs do not stop the passage of infection during coitus",
   "Statement II: false - IUDs act on sperms and implantation, not on viruses"],
  "Birth Control (Contraceptive Methods); Sexually Transmitted Infections (STIs)", ans="C",
  why="Statement II is false, so 'both true' and 'I false, II true' are wrong; Statement I is true, so 'both "
      "false' is wrong.", secs=40)

Z(RH, "Contraception", I, MUL,
  MS("According to NCERT, which of the following are features of an ideal contraceptive?",
     ["It should be user-friendly and easily available.",
      "It should be effective.",
      "It should be reversible, with no or the least side effects.",
      "It should in no way interfere with the sexual drive, desire and/or the sexual act of the user.",
      "It should permanently stop the formation of gametes."]),
  "Ideal contraceptive",
  "NCERT: an ideal contraceptive should be user-friendly, easily available, effective and reversible with no or "
  "least side-effects; it also should in no way interfere with the sexual drive, desire and/or the sexual act of "
  "the user. A method that permanently stops gamete formation would be irreversible.",
  ["(a), (b), (c), (d): NCERT's list", "(e): irreversible -> not ideal"],
  "Birth Control (Contraceptive Methods)",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(b), (c) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="(e) contradicts reversibility, so any option containing it is wrong.", secs=35)

Z(RH, "Infertility and ART", I, MAT,
  ML(("situation", "assisted reproductive technology that suits it"),
     ["A woman cannot produce ova but can provide a suitable environment for fertilisation in her oviduct",
      "The male partner is unable to inseminate the female, or has very low sperm counts",
      "An embryo with more than 8 blastomeres formed in vitro is to be transferred",
      "A sperm is to be injected directly into the ovum to form an embryo in the laboratory"],
     ["Intra cytoplasmic sperm injection (ICSI)", "Intra uterine transfer (IUT)",
      "Artificial insemination (AI) or intra-uterine insemination (IUI)", "Gamete intra fallopian transfer (GIFT)"]),
  "Choosing an assisted reproductive technology",
  "NCERT: GIFT is the transfer of an ovum collected from a donor into the fallopian tube of a female who cannot "
  "produce one but can provide a suitable environment for fertilisation; AI (into the vagina or, as IUI, into "
  "the uterus) is used where the male cannot inseminate or has very low sperm counts; embryos with more than 8 "
  "blastomeres are transferred into the uterus (IUT); in ICSI a sperm is directly injected into the ovum.",
  ["A -> GIFT (IV)", "B -> AI/IUI (III)", "C -> IUT (II)", "D -> ICSI (I)"],
  "Assisted Reproductive Technologies",
  at="C", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="GIFT and IUT differ in what is transferred and where (an ovum into the oviduct versus an embryo into the "
      "uterus); AI places semen in the female tract, whereas ICSI injects a single sperm into an ovum in the "
      "laboratory.", secs=50)

Z(RH, "Contraception", I, D,
  "A mother is still breast-feeding her baby fully, eight months after parturition, and relies on lactational "
  "amenorrhea as her only method of contraception. According to NCERT, which statement applies to her?",
  "Limits of lactational amenorrhea",
  "NCERT: lactational amenorrhea is based on the fact that ovulation, and therefore the cycle, do not occur "
  "during the period of intense lactation following parturition; it has been reported to be effective only up to "
  "a maximum period of six months following parturition. At eight months she is beyond that period.",
  ["LAM effective up to a maximum of six months after parturition", "8 months > 6 months -> not reliable now"],
  "Birth Control (Contraceptive Methods)",
  at="B", correct="The method is considered effective only up to a maximum of six months after parturition, so "
                  "she should not rely on it alone now",
  wrong=["The method remains effective for as long as she breast-feeds, however long that is",
         "The method is effective only in the first two weeks after parturition",
         "The method works by blocking the fallopian tubes, so its effect is permanent"],
  why="NCERT puts the limit at six months, not 'as long as she breast-feeds' or two weeks; and lactational "
      "amenorrhea acts by the absence of ovulation during intense lactation, not by blocking the tubes.", secs=35)

Z(RH, "Infertility and ART", I, STP,
  SP("In GIFT, fertilisation takes place in the laboratory before the gametes are transferred into the fallopian "
     "tube.",
     "In ZIFT, the zygote or an early embryo with up to 8 blastomeres is transferred into the fallopian tube."),
  "GIFT and ZIFT",
  "NCERT: in GIFT, an ovum collected from a donor is transferred into the fallopian tube of a female who cannot "
  "produce one but can provide a suitable environment for fertilisation; fertilisation therefore takes place "
  "inside her body (in vivo). In ZIFT, the zygote or early embryos (with up to 8 blastomeres), formed in vitro, "
  "are transferred into the fallopian tube.",
  ["Statement I: false - in GIFT a gamete is transferred and fertilisation happens in the oviduct",
   "Statement II: true"],
  "Assisted Reproductive Technologies", ans="D",
  why="Statement I describes ZIFT, not GIFT; Statement II is correct, so only 'I false, II true' fits.", secs=35)

Z(RH, "Contraception", A, ASR,
  AR("Vasectomy stops the production of sperms in the testes.",
     "In vasectomy, a small part of the vas deferens is removed or tied up through a small incision on the "
     "scrotum."),
  "Vasectomy blocks transport, not production",
  "R is NCERT's description of vasectomy. The operation is on the vas deferens, a duct that carries sperms from "
  "the epididymis towards the urethra; it blocks gamete transport and thereby prevents conception. The testes "
  "(seminiferous tubules) are untouched, so sperm production is not stopped. A is false.",
  ["R: true - vas deferens cut or tied", "Surgical methods block gamete transport", "Testes untouched -> sperm "
   "production continues -> A false"],
  "Birth Control (Contraceptive Methods)", ans="D",
  why="A is false, so the two 'both true' options and 'A true but R false' are wrong.", secs=40)

Z(RH, "Infertility and ART", A, MUL,
  MS("A couple wants a child. Both fallopian tubes of the wife are completely blocked, but she produces normal "
     "ova and has a normal uterus. The husband has a very low sperm count. Which of the following techniques "
     "described in NCERT could help them?",
     ["In vitro fertilisation followed by transfer of the embryo into her uterus (IUT)",
      "Intra cytoplasmic sperm injection (ICSI), followed by transfer of the embryo into her uterus",
      "Gamete intra fallopian transfer (GIFT)",
      "Zygote intra fallopian transfer (ZIFT)",
      "Intra-uterine insemination (IUI) alone"]),
  "Choosing ART when the oviducts are blocked",
  "With both oviducts blocked, any technique that places gametes or embryos in the fallopian tube (GIFT, ZIFT) "
  "cannot work, and IUI alone cannot work because the sperms still have to meet the ovum in the oviduct. "
  "Fertilisation must therefore be done in the laboratory and the embryo placed in the uterus: IVF with IUT, or "
  "ICSI (a sperm injected directly into the ovum, useful when sperms are few) with transfer into the uterus.",
  ["Oviducts blocked -> no GIFT, no ZIFT, no IUI", "Uterus normal -> embryo can be placed in the uterus",
   "IVF + IUT and ICSI + transfer into the uterus both bypass the oviduct"],
  "Assisted Reproductive Technologies",
  at="B", correct="(a) and (b) only",
  wrong=["(c) and (d) only", "(a), (b) and (e) only", "(c), (d) and (e) only"],
  why="GIFT and ZIFT need a working fallopian tube, and IUI depends on fertilisation in the oviduct, so options "
      "containing (c), (d) or (e) are wrong.", secs=60)

Z(RH, "Contraception", A, MAT,
  ML(("method", "limitation stated in NCERT"),
     ["Lactational amenorrhea", "Emergency contraceptives", "Surgical methods (sterilisation)",
      "Periodic abstinence and coitus interruptus"],
     ["Chances of failure are high", "Reversibility is very poor",
      "Very effective only if used within 72 hours of coitus",
      "Effective only up to a maximum period of six months following parturition"]),
  "Limitations of contraceptive methods",
  "NCERT: lactational amenorrhea is effective only up to a maximum of six months after parturition; emergency "
  "contraceptives are very effective within 72 hours of coitus; reversibility of sterilisation is very poor; "
  "natural methods such as periodic abstinence and withdrawal have almost no side effects but their chances of "
  "failure are high.",
  ["LAM -> IV", "Emergency contraceptives -> III", "Sterilisation -> II", "Periodic abstinence, withdrawal -> I"],
  "Birth Control (Contraceptive Methods)",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The wrong codes swap the two time limits (six months versus 72 hours) or give sterilisation the high "
      "failure rate of natural methods; sterilisation is very effective but poorly reversible.", secs=45)

Z(RH, "Contraception", A, D,
  "Which of the following pairs of contraceptive methods prevent conception WITHOUT preventing ovulation?",
  "Modes of action of contraceptives",
  "NCERT: condoms are barriers that prevent the meeting of ovum and sperms, and vasectomy blocks sperm "
  "transport; neither affects ovulation. Oral pills and progestogen implants inhibit ovulation and implantation, "
  "and lactational amenorrhea works because ovulation does not occur during intense lactation.",
  ["Condom: barrier", "Vasectomy: blocks transport of sperms", "Pills, implants, LAM: ovulation suppressed"],
  "Birth Control (Contraceptive Methods)",
  at="A", correct="Condoms and vasectomy",
  wrong=["Oral pills and lactational amenorrhea", "Progestogen implants and condoms",
         "Lactational amenorrhea and tubectomy"],
  why="Each wrong pair contains a method that does prevent ovulation: oral pills, implants or lactational "
      "amenorrhea.", secs=40)

# ================================================================ Evolution (5/7/5)
Z(EVO, "Origin of life", B, D,
  "According to NCERT, the early earth had no atmosphere at first. Which gases, released from its molten mass, "
  "then covered its surface?",
  "Conditions on the early earth",
  "NCERT: early earth had no atmosphere. Water vapour, methane, carbon dioxide and ammonia released from the "
  "molten mass covered the surface. (UV rays later broke up water into hydrogen and oxygen; as the earth cooled, "
  "water vapour fell as rain to form the oceans.)",
  ["No atmosphere at first", "Released from the molten mass: water vapour, methane, CO₂, ammonia"],
  "Origin of Life",
  at="C", correct="Water vapour, methane, carbon dioxide and ammonia",
  wrong=["Oxygen, nitrogen and argon", "Oxygen and carbon dioxide only", "Hydrogen sulphide and chlorine only"],
  why="The early earth's gases in NCERT's account were reducing (methane, ammonia) with water vapour and CO₂; "
      "free oxygen was not among the gases released, and H₂S and chlorine are not mentioned.", secs=25)

Z(EVO, "Natural selection", B, D,
  "Before industrialisation set in, white-winged moths survived better than dark-winged moths in the woodlands "
  "of England. According to NCERT, this was because the tree trunks were then covered by:",
  "Industrial melanism",
  "NCERT: before industrialisation set in, a thick growth of almost white-coloured lichen covered the trees, and "
  "in that background the white-winged moth survived while the dark-coloured moths were picked out by "
  "predators. After industrialisation, smoke and soot darkened the trunks and the situation reversed.",
  ["Pre-industrial trunks: almost white lichens", "White moths matched the background -> escaped predators"],
  "Evidence for Evolution",
  at="B", correct="A thick growth of almost white-coloured lichens",
  wrong=["A thick layer of black soot", "Dark green mosses that hid the dark moths",
         "Bare, dark bark with nothing growing on it"],
  why="Soot covered the trunks only after industrialisation; mosses are not part of NCERT's account; and on dark "
      "bark the dark moths, not the white ones, would have survived better.", secs=25)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, MAT,
  ML(("term", "meaning"),
     ["Gene pool", "Genetic drift", "Founder effect", "Gene flow"],
     ["Change in gene frequencies when a section of a population migrates to another place and population",
      "The drifted population becomes the founders of a new population",
      "Total genes and their alleles in a population",
      "Change in allele frequency that occurs by chance"]),
  "Terms of population genetics",
  "NCERT: the total genes and their alleles in a population are its gene pool; if the change in allele frequency "
  "occurs by chance it is called genetic drift; when the original drifted population becomes the founders of a "
  "new population it is called the founder effect; when migration of a section of a population occurs multiple "
  "times, gene flow takes place, changing gene frequencies in both populations.",
  ["Gene pool -> III", "Genetic drift -> IV", "Founder effect -> II", "Gene flow -> I"],
  "Hardy-Weinberg Principle",
  at="B", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="The wrong codes swap gene pool with drift, founder effect with gene flow, or drift with founder effect; "
      "drift is the chance change itself, while the founder effect is what follows when the drifted population "
      "founds a new one.", secs=40)

Z(EVO, "Human evolution", B, D,
  "According to NCERT, after Homo sapiens arose in Africa, it moved across continents and:",
  "Spread of modern humans",
  "NCERT: Homo sapiens arose in Africa and moved across continents and developed into distinct races. During the "
  "ice age between 75,000 and 10,000 years ago, modern Homo sapiens arose.",
  ["Origin: Africa", "Spread: across continents", "Result: distinct races"],
  "Origin and Evolution of Man",
  at="D", correct="Developed into distinct races",
  wrong=["Evolved into Homo erectus in Java", "Gave rise to the Australopithecines of East Africa",
         "Was replaced everywhere by Dryopithecus"],
  why="Homo erectus, the Australopithecines and Dryopithecus are all earlier forms in NCERT's account, so none "
      "of them could arise from, or replace, Homo sapiens.", secs=20)

N_PEOPLE, AA_RECESSIVE = 1000, 90
q = F(3, 10)                     # positive square root of 90/1000, checked on the next line
assert q * q == F(AA_RECESSIVE, N_PEOPLE)
A_COPIES = q * 2 * N_PEOPLE
assert A_COPIES == 600 and q * N_PEOPLE == 300 and 2 * q * (1 - q) * N_PEOPLE == 420
Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "A population of 1,000 people is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a. Ninety "
  "people show the recessive phenotype (aa). How many copies of allele a are present in the whole population?",
  "Counting alleles in a population",
  "q² = 90/1000 = 0.09, so q = 0.3. Each person carries two copies of the gene, so the population carries "
  "2 x 1000 = 2000 copies in all. Copies of a = 0.3 x 2000 = 600.",
  ["q² = 0.09 -> q = 0.3", "Total gene copies = 2N = 2000", "Copies of a = 0.3 x 2000 = 600"],
  "Hardy-Weinberg Principle",
  at="B", correct="600", wrong=["300", "180", "420"],
  short="Copies of a = 2Nq.",
  why="300 forgets that each person has two copies (Nq); 180 counts only the copies in the 90 aa people; 420 is "
      "the number of heterozygous people (2pqN), not of allele copies.", secs=45, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, D,
  "A section of a population of a species migrates to another place and joins another population of the same "
  "species. According to NCERT, what happens to gene frequencies?",
  "Gene migration (gene flow)",
  "NCERT: when migration of a section of a population to another place and population occurs, gene frequencies "
  "change in the original as well as in the new population. New genes/alleles are added to the new population "
  "and these are lost from the old population.",
  ["Migrants carry alleles with them", "Alleles added to the receiving population", "Same alleles lost from the "
   "original population -> both change"],
  "Hardy-Weinberg Principle",
  at="C", correct="Gene frequencies change in the original as well as in the new population: alleles are added "
                  "to the new population and lost from the old one",
  wrong=["Gene frequencies change only in the new population; the original population is unaffected",
         "Gene frequencies stay the same in both, since no new mutation has occurred",
         "The new population at once becomes a different species, by the founder effect"],
  why="NCERT stresses that both populations change; migration changes frequencies without any new mutation; and "
      "the founder effect concerns a drifted population founding a new one, not migrants joining an existing "
      "population.", secs=35)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, STP,
  SP("Sometimes the change in allele frequency is so different in a new sample of a population that it becomes "
     "a different species.",
     "Variation due to recombination during gametogenesis can result in changed frequencies of genes and alleles "
     "in future generations."),
  "Factors that change allele frequency",
  "Both are NCERT statements. Statement I follows NCERT's account of genetic drift (the drifted population may "
  "even become a different species). Statement II: NCERT says that variation due to mutation, recombination "
  "during gametogenesis, gene flow or genetic drift results in changed frequency of genes and alleles in future "
  "generations; genetic recombination is one of the five factors affecting Hardy-Weinberg equilibrium.",
  ["Statement I: true (drift -> may lead to a new species)", "Statement II: true (recombination is a factor)"],
  "Hardy-Weinberg Principle", ans="A",
  why="Recombination is often forgotten as a factor, but NCERT lists it with gene flow, drift, mutation and "
      "natural selection; both statements are true.", secs=35)

Z(EVO, "Natural selection", I, MAT,
  ML(("observation in a bird population", "process"),
     ["Medium-sized birds survive and reproduce best, and more individuals come to have the mean size",
      "Over generations, the mean beak size shifts steadily towards larger values",
      "Birds with very small and with very large beaks both increase, while those with medium beaks decline",
      "In a tiny isolated population, one allele is lost purely by chance"],
     ["Genetic drift", "Disruptive selection", "Directional selection", "Stabilising selection"]),
  "Types of natural selection",
  "NCERT: in stabilisation more individuals acquire the mean character value; in directional change more "
  "individuals acquire a value other than the mean; in disruption more individuals acquire peripheral character "
  "values at both ends of the distribution curve. A change in allele frequency by chance is genetic drift.",
  ["A: mean favoured -> stabilising (IV)", "B: one direction favoured -> directional (III)",
   "C: both extremes favoured -> disruptive (II)", "D: chance -> drift (I)"],
  "Mechanism of Evolution; Hardy-Weinberg Principle",
  at="C", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The wrong codes swap stabilising with directional, directional with disruptive, or disruptive selection "
      "with drift; only D involves pure chance rather than selection.", secs=45)

Z(EVO, "Adaptive radiation", I, MUL,
  MS("Which of the following statements about adaptive radiation are correct according to NCERT?",
     ["It is the evolution of different species in a given geographical area starting from a point and "
      "literally radiating to other areas of geography (habitats).",
      "A number of marsupials, each different from the other, evolved from an ancestral stock within the "
      "Australian island continent.",
      "Placental mammals in Australia also exhibit adaptive radiation.",
      "The resemblance between the placental wolf and the Tasmanian wolf shows that both arose within a single "
      "adaptive radiation from one ancestral stock.",
      "Adaptive radiation requires the inheritance of characters acquired through the use and disuse of organs."]),
  "Adaptive radiation and convergence",
  "NCERT defines adaptive radiation as in (a), gives the Australian marsupials (b) and says placental mammals in "
  "Australia also exhibit adaptive radiation (c). The placental wolf and the Tasmanian wolf (a marsupial) belong "
  "to two different radiations; their similarity is given as convergent evolution, so (d) is false. Use and "
  "disuse is Lamarck's idea, not part of adaptive radiation (e).",
  ["(a) true - definition", "(b) true - marsupials", "(c) true - placentals", "(d) false - convergent evolution "
   "between two radiations", "(e) false - Lamarckian idea"],
  "What is Adaptive Radiation?",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (e) only"],
  why="(d) misreads convergent evolution as a single radiation, and (e) brings in Lamarck, so any option with "
      "them is wrong.", secs=50)

Z(EVO, "Natural selection", I, ASR,
  AR("Excessive use of herbicides and pesticides has resulted in the selection of resistant varieties in a much "
     "shorter time than the usual pace of evolution.",
     "Resistant variants present in the population survive the chemical and leave more progeny, so they increase "
     "in number."),
  "Evolution by anthropogenic action",
  "NCERT: excess use of herbicides and pesticides has resulted only in the selection of resistant varieties in a "
  "much lesser time scale; this is evolution by anthropogenic action. The mechanism is natural selection: "
  "variants that can survive the chemical reproduce and leave a greater number of progeny, so their frequency "
  "rises. R explains how A happens.",
  ["A: true (NCERT)", "R: natural selection of resistant variants", "Survivors leave more progeny -> resistant "
   "variety spreads -> R explains A"],
  "Evidence for Evolution; Biological Evolution", ans="A",
  why="Both statements are true and R is the selection mechanism behind A, so B, C and D are wrong.", secs=40)

Z(EVO, "Human evolution", I, STP,
  SP("Homo habilis, with a brain capacity of about 1400 cc, probably ate meat.",
     "Neanderthal man lived in the East African grasslands about 2 million years ago."),
  "Features of hominids",
  "NCERT: Homo habilis had brain capacities between 650 and 800 cc and probably did not eat meat. Neanderthal man, "
  "with a brain size of 1400 cc, lived in the near east and central Asian countries between 1,00,000 and 40,000 "
  "years back. The Australopithecines probably lived in East African grasslands about 2 mya. Both statements mix "
  "up the features of different hominids.",
  ["Statement I: false - 1400 cc is Neanderthal; H. habilis 650-800 cc and probably did not eat meat",
   "Statement II: false - that habitat and time belong to the Australopithecines"],
  "Origin and Evolution of Man", ans="B",
  why="Each statement transfers features from another hominid, so both are false and every option calling either "
      "true is wrong.", secs=40)

P25 = F(3, 4)
assert (P25, P25 ** 2, 2 * P25 * (1 - P25), (1 - P25) ** 2) == (F(3, 4), F(9, 16), F(3, 8), F(1, 16))
assert [float(x) for x in (P25, P25 ** 2, 2 * P25 * (1 - P25), (1 - P25) ** 2)] == [0.75, 0.5625, 0.375, 0.0625]
Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, MAT,
  ML(("quantity, for a population in Hardy-Weinberg equilibrium in which the frequency of allele a (q) is 0.25",
      "value"),
     ["Frequency of allele A (p)", "Frequency of genotype AA (p²)", "Frequency of genotype Aa (2pq)",
      "Frequency of genotype aa (q²)"],
     ["0.0625", "0.375", "0.5625", "0.75"]),
  "Hardy-Weinberg frequencies",
  "p = 1 - q = 0.75. p² = 0.5625, 2pq = 2 x 0.75 x 0.25 = 0.375, q² = 0.0625. Check: 0.5625 + 0.375 + 0.0625 = 1.",
  ["p = 1 - 0.25 = 0.75 (IV)", "p² = 0.5625 (III)", "2pq = 0.375 (II)", "q² = 0.0625 (I)"],
  "Hardy-Weinberg Principle",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  short="The three genotype frequencies must add up to 1.",
  why="The wrong codes swap p with p², p² with 2pq, or 2pq with q²; the check p² + 2pq + q² = 1 rules them out.",
  secs=50, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, ASR,
  AR("An allele that is common in a large mainland population may be completely absent from a new island "
     "population started by a few founders from the mainland.",
     "The founders are a small sample whose allele frequencies can differ, purely by chance, from those of the "
     "original population."),
  "Founder effect",
  "NCERT: a change in allele frequency that occurs by chance is genetic drift; when the drifted population "
  "becomes the founder of a new population it is called the founder effect, and the change can be so large that "
  "the new population becomes a different species. A few founders are a small chance sample, so an allele common "
  "on the mainland may simply not be carried by any of them. R explains A.",
  ["A: true - possible", "R: true - small founding sample, chance differences", "Chance sampling -> allele "
   "missing -> R explains A"],
  "Hardy-Weinberg Principle", ans="A",
  why="Both are true and the chance sampling of a small founding group is the cause of A, so B, C and D are "
      "wrong.", secs=40)

pq = F(1, 3)                     # p^2 = 4 q^2 -> p = 2q -> q = 1/3
p2 = 1 - pq
assert p2 ** 2 == 4 * pq ** 2 and 2 * p2 * pq == F(4, 9)
assert p2 * pq == F(2, 9) and 2 * F(4, 5) * F(1, 5) == F(8, 25)
Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population in Hardy-Weinberg equilibrium for a gene with alleles A and a, homozygous dominant individuals "
  "(AA) are four times as frequent as homozygous recessive individuals (aa). What is the frequency of "
  "heterozygous individuals (Aa)?",
  "Hardy-Weinberg from a ratio of homozygotes",
  "p² = 4q², so p = 2q (frequencies are positive). With p + q = 1: 3q = 1, q = 1/3 and p = 2/3. Frequency of "
  "Aa = 2pq = 2 x 2/3 x 1/3 = 4/9.",
  ["p²/q² = 4 -> p/q = 2", "p + q = 1 -> q = 1/3, p = 2/3", "2pq = 4/9"],
  "Hardy-Weinberg Principle",
  at="B", correct="4/9", wrong=["2/9", "8/25", "1/3"],
  short="Take the square root of the genotype ratio to get the allele ratio.",
  why="2/9 is pq without the factor 2; 8/25 comes from taking p = 4q (forgetting the square root); 1/3 is the "
      "frequency of allele a, not of heterozygotes.", secs=60, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, MUL,
  MS("A biologist follows a gene with two alleles in a population over several generations. Which of the "
     "following observations would indicate that the population is NOT in Hardy-Weinberg equilibrium?",
     ["The observed genotype frequencies differ from the values expected from p², 2pq and q².",
      "The allele frequencies change from one generation to the next.",
      "The sum of the frequencies of the two alleles is 1.",
      "The observed frequency of heterozygotes equals 2pq in every generation.",
      "A new allele of the gene appears by mutation and spreads in the population."]),
  "Recognising disturbance of Hardy-Weinberg equilibrium",
  "NCERT: allele frequencies in a population are stable and constant from generation to generation unless "
  "disturbed (genetic equilibrium); when the measured frequency differs from the expected values, the difference "
  "indicates the extent of evolutionary change; mutation is one of the factors that disturb the equilibrium. "
  "p + q = 1 holds in any population, so it says nothing about equilibrium, and heterozygotes matching 2pq is "
  "what equilibrium predicts.",
  ["(a) yes - departure from expected values", "(b) yes - allele frequencies should stay constant",
   "(c) no - always true", "(d) no - consistent with equilibrium", "(e) yes - mutation disturbs equilibrium"],
  "Hardy-Weinberg Principle",
  at="C", correct="(a), (b) and (e) only",
  wrong=["(a), (c) and (d) only", "(c) and (d) only", "(b), (c) and (e) only"],
  why="(c) is true of every population and (d) is the expectation under equilibrium, so options containing them "
      "describe no departure from equilibrium.", secs=55)

Z(EVO, "Natural selection", A, D,
  "NCERT explains industrial melanism in England through predation: moths that did not match the colour of the "
  "tree trunks were picked out by predators. Suppose that in an industrial area there were no predators of "
  "these moths at all. What would this explanation predict about the proportions of dark-winged and white-winged "
  "moths after industrialisation?",
  "Selection needs a selecting agent",
  "In NCERT's account, the dark moths increased after industrialisation because the white moths stood out on the "
  "soot-darkened trunks and were picked out by predators. Natural selection here acts through predation. If "
  "there were no predators, matching or not matching the trunk colour would not affect survival, so the "
  "explanation predicts no shift in the proportions because of trunk colour.",
  ["Selection agent = predators", "No predators -> colour does not affect survival or progeny",
   "-> no shift in proportions due to trunk colour"],
  "Evidence for Evolution",
  at="A", correct="They would not shift because of trunk colour, since without predators the moths that do not "
                  "match the background are not selected against",
  wrong=["Dark-winged moths would still increase, because soot settling on white moths turns them dark",
         "White-winged moths would disappear completely, because lichens cannot grow in polluted areas",
         "Both kinds would become extinct, because natural selection always eliminates variants"],
  why="Soot does not change the moths' inherited colour; the absence of lichens matters only through predators; "
      "and NCERT notes that in natural selection no variant is completely wiped out.", secs=55)

Z(EVO, "Evidences of evolution", A, MUL,
  MS("Which of the following pairs are homologous structures, indicating common ancestry?",
     ["The forelimbs of a cheetah and of a whale",
      "The thorn of Bougainvillea and the tendril of Cucurbita",
      "The wings of a butterfly and of a bird",
      "The brains of different vertebrates",
      "Sweet potato and potato"]),
  "Homology versus analogy",
  "NCERT: the forelimbs of whales, bats, cheetah and human share the same pattern of bones (homology, divergent "
  "evolution); vertebrate hearts and brains are also homologous; the thorn of Bougainvillea and the tendril of "
  "Cucurbita are homologous in plants. Wings of butterfly and of birds, and sweet potato (root modification) and "
  "potato (stem modification), are analogous: different structures performing the same function.",
  ["(a) homologous", "(b) homologous", "(c) analogous", "(d) homologous", "(e) analogous"],
  "Evidence for Evolution",
  at="D", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"],
  why="Sweet potato and potato look alike as storage organs but one is a root and the other a stem, and butterfly "
      "and bird wings have different structure; both are analogous, so options containing (c) or (e) are wrong.",
  secs=50)

# ================================================================ Human Health and Disease (7/9/7)
Z(HHD, "Pathogens and diseases", B, D,
  "The 'good humor' hypothesis of health was disproved partly by William Harvey's discovery of blood circulation. "
  "According to NCERT, it was also disproved by the demonstration, using a thermometer, that persons with "
  "'black bile' had:",
  "Disproving the 'good humor' hypothesis",
  "NCERT: the discovery of blood circulation by William Harvey using the experimental method, and the "
  "demonstration of normal body temperature in persons with 'black bile' using a thermometer, disproved the "
  "'good humor' hypothesis of health.",
  ["Old belief: black bile -> hot personality, fevers", "Thermometer showed normal body temperature -> "
   "hypothesis disproved"],
  "Introduction (health and the 'good humor' hypothesis)",
  at="A", correct="Normal body temperature",
  wrong=["A permanently high fever", "A body temperature lower than that of all other persons",
         "Black-coloured blood"],
  why="The old belief linked black bile with fevers; measurement showed a normal temperature, which is what "
      "disproved it. The other options are not in NCERT's account.", secs=25)

Z(HHD, "Immunity and vaccines", B, D,
  "According to NCERT, the mind and mental state can affect our health because the mind influences our immune "
  "system through the:",
  "Mind, health and immunity",
  "NCERT: in later years, biology stated that the mind influences, through the neural system and endocrine "
  "system, our immune system, and that our immune system maintains our health. Hence the mind and mental state "
  "can affect our health.",
  ["Mind -> neural system and endocrine system -> immune system -> health"],
  "Introduction (health and the 'good humor' hypothesis)",
  at="C", correct="Neural system and endocrine system",
  wrong=["Digestive system and excretory system", "Skeletal system alone",
         "Lymph nodes alone, without any neural or hormonal link"],
  why="NCERT names only the neural and endocrine systems as the link between the mind and the immune system.",
  secs=20)

Z(HHD, "Drug and alcohol abuse", B, D,
  "According to NCERT, the term 'adolescence' means:",
  "Adolescence",
  "NCERT: adolescence means both 'a period' and 'a process' during which a child becomes mature in terms of "
  "his/her attitudes and beliefs for effective participation in society. The period between 12 and 18 years of "
  "age may be thought of as the adolescence period, a very vulnerable phase of mental and psychological "
  "development.",
  ["Both a period and a process", "Child becomes mature in attitudes and beliefs for effective participation in "
   "society"],
  "Adolescence and Drug/Alcohol Abuse",
  at="D", correct="Both 'a period' and 'a process' during which a child becomes mature in attitudes and beliefs "
                  "for effective participation in society",
  wrong=["Only the age span of 12 to 18 years, with no reference to maturation",
         "The period after which a person can no longer become addicted to drugs",
         "The stage of life in which a person is least vulnerable to drug abuse"],
  why="NCERT stresses that adolescence is a process as well as a period; it calls adolescence a very vulnerable "
      "phase, and drug dependence can develop at any age.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Tobacco contains a large number of chemical substances. According to NCERT, nicotine, one of these, is:",
  "Nicotine",
  "NCERT: tobacco contains a large number of chemical substances including nicotine, an alkaloid. Nicotine "
  "stimulates the adrenal gland to release adrenaline and nor-adrenaline.",
  ["Nicotine = an alkaloid present in tobacco"],
  "Drugs and Alcohol Abuse",
  at="B", correct="An alkaloid", wrong=["A steroid", "A peptide hormone", "An opioid obtained from the poppy plant"],
  why="Nicotine is neither a steroid nor a hormone; opioids such as morphine and heroin come from the poppy, not "
      "from tobacco.", secs=20)

Z(HHD, "Pathogens and diseases", B, MUL,
  MS("NCERT divides the hygiene measures for preventing infectious diseases into personal hygiene and public "
     "hygiene. Which of the following are measures of PUBLIC hygiene?",
     ["Proper disposal of waste and excreta",
      "Periodic cleaning and disinfection of water reservoirs, pools, cesspools and tanks",
      "Observing standard practices of hygiene in public catering",
      "Keeping the body clean",
      "Consumption of clean drinking water, food, vegetables and fruits"]),
  "Personal and public hygiene",
  "NCERT: personal hygiene includes keeping the body clean and consumption of clean drinking water, food, "
  "vegetables, fruits, etc. Public hygiene includes proper disposal of waste and excreta, periodic cleaning and "
  "disinfection of water reservoirs, pools, cesspools and tanks, and observance of standard practices of hygiene "
  "in public catering.",
  ["(a), (b), (c): public hygiene", "(d), (e): personal hygiene"],
  "Common Diseases in Humans",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(c), (d) and (e) only", "(a), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="Keeping the body clean and consuming clean water and food are what an individual does, so NCERT classes "
      "them as personal hygiene; any option with (d) or (e) is wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", B, STP,
  SP("These days cannabinoids are also being abused by some sportspersons.",
     "Cannabinoids are generally taken by snorting and injection."),
  "Cannabinoids",
  "NCERT: cannabinoids are generally taken by inhalation and oral ingestion and are known for their effects on "
  "the cardiovascular system; these days they are also being abused by some sportspersons. Snorting and "
  "injection is how NCERT says heroin is generally taken.",
  ["Statement I: true", "Statement II: false - inhalation and oral ingestion (snorting and injection = heroin)"],
  "Drugs and Alcohol Abuse", ans="C",
  why="Statement II gives the route of heroin, so it is false; Statement I is NCERT's line, so only 'I true, II "
      "false' fits.", secs=30)

Z(HHD, "Pathogens and diseases", B, MAT,
  ML(("pathogen", "part of the body where it lives or multiplies"),
     ["Rhinoviruses", "Entamoeba histolytica", "Wuchereria", "Plasmodium (first, after entering the body)"],
     ["Liver cells, after which it attacks the red blood cells", "Lymphatic vessels of the lower limbs",
      "Large intestine", "Nose and respiratory passage, but not the lungs"]),
  "Sites of infection",
  "NCERT: rhinoviruses infect the nose and respiratory passage but not the lungs; Entamoeba histolytica is a "
  "protozoan parasite in the large intestine of humans; Wuchereria worms live for many years in the lymphatic "
  "vessels of the lower limbs; Plasmodium multiplies first within the liver cells and then attacks the red blood "
  "cells.",
  ["Rhinoviruses -> IV", "Entamoeba -> III", "Wuchereria -> II", "Plasmodium -> I"],
  "Common Diseases in Humans",
  at="A", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="Each wrong code moves one parasite to another's site; Entamoeba lives in the large intestine, and "
      "Wuchereria in lymphatic vessels, not blood cells.", secs=40)

Z(HHD, "Drug and alcohol abuse", I, ASR,
  AR("Use of tobacco tends to raise the blood pressure and increase the heart rate.",
     "Nicotine stimulates the adrenal gland to release adrenaline and nor-adrenaline into the blood circulation."),
  "Nicotine and the adrenal medulla",
  "NCERT: nicotine stimulates the adrenal gland to release adrenaline and nor-adrenaline into blood circulation, "
  "both of which raise blood pressure and increase heart rate. (In Class 11, catecholamines are described as "
  "increasing the heartbeat and the strength of heart contraction.) R is the cause of A.",
  ["Nicotine -> adrenal gland -> adrenaline, nor-adrenaline", "These hormones -> raised BP and heart rate",
   "So R explains A"],
  "Drugs and Alcohol Abuse", ans="A",
  why="Both are NCERT statements and NCERT links them directly, so B, C and D are wrong.", secs=35)

Z(HHD, "Cancer", I, ASR,
  AR("Cancer patients are given substances called biological response modifiers, such as α-interferon.",
     "Tumour cells have been shown to avoid detection and destruction by the immune system."),
  "Immunotherapy for cancer",
  "NCERT: tumour cells have been shown to avoid detection and destruction by the immune system; therefore the "
  "patients are given substances called biological response modifiers such as α-interferon, which activate "
  "their immune system and help in destroying the tumour. R is NCERT's stated reason for A.",
  ["A: true", "R: true", "NCERT joins them with 'therefore' -> R explains A"],
  "Cancer", ans="A",
  why="Both statements are true and R is the reason NCERT gives, so the other options are wrong.", secs=35)

Z(HHD, "Cancer", I, MUL,
  MS("Which of the following techniques used in detecting cancer make use of X-rays?",
     ["Radiography", "Computed tomography (CT)", "Magnetic resonance imaging (MRI)",
      "Biopsy and histopathological study of the tissue", "Blood and bone marrow tests for increased cell counts"]),
  "Imaging techniques for cancer detection",
  "NCERT: radiography is the use of X-rays; CT uses X-rays to generate a three-dimensional image of the "
  "internals of an object; MRI uses strong magnetic fields and non-ionising radiations. Biopsy with "
  "histopathology, and blood and bone marrow tests (as in leukaemia), are laboratory tests on tissue or blood.",
  ["(a) X-rays", "(b) X-rays", "(c) magnetic fields and non-ionising radiation", "(d), (e) laboratory tests"],
  "Cancer",
  at="B", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(b) and (c) only", "(c), (d) and (e) only"],
  why="MRI is the usual trap: it uses magnetic fields and non-ionising radiation, not X-rays, so options with "
      "(c) are wrong; (d) and (e) involve no radiation at all.", secs=35)

Z(HHD, "Immunity and vaccines", I, D,
  "A child is given the hepatitis B vaccine produced from yeast. According to NCERT, what does such a vaccine "
  "contain, and why could it be made on a large scale?",
  "Recombinant vaccines",
  "NCERT: recombinant DNA technology has allowed the production of antigenic polypeptides of a pathogen in "
  "bacteria or yeast; vaccines produced using this approach allow large-scale production and hence greater "
  "availability for immunisation, e.g., the hepatitis B vaccine produced from yeast. The child's own immune "
  "system then makes antibodies and memory cells (active immunity).",
  ["Gene for an antigenic polypeptide put into yeast", "Yeast makes the polypeptide in bulk", "Vaccine = "
   "antigenic polypeptide -> active immunity"],
  "Immunity (Vaccination and immunisation)",
  at="D", correct="Antigenic polypeptides of the pathogen, made in yeast by recombinant DNA technology, which "
                  "allows large-scale production",
  wrong=["Preformed antibodies against the virus, collected from the blood of recovered patients",
         "Whole live hepatitis B viruses grown in large numbers inside yeast cells",
         "Interferons secreted by yeast cells infected with the virus"],
  why="Preformed antibodies would give passive immunity and are not made in yeast; the yeast makes only a "
      "polypeptide of the pathogen, not whole viruses; and interferons are made by virus-infected animal cells.",
  secs=40)

Z(HHD, "Pathogens and diseases", I, STP,
  SP("Since Salmonella typhi enters the body through contaminated food and water, a cook who carries the "
     "pathogen can spread typhoid to many people through the food he or she prepares.",
     "Typhoid usually spreads through droplets released when an infected person coughs or sneezes."),
  "Spread of typhoid",
  "NCERT: Salmonella typhi generally enters the small intestine through food and water contaminated with it and "
  "migrates to other organs through blood. Mary Mallon, a cook, was a typhoid carrier who continued to spread "
  "typhoid for several years through the food she prepared. Droplet spread is how NCERT describes the common "
  "cold and pneumonia, not typhoid.",
  ["Statement I: true - food-borne spread, as in the 'Typhoid Mary' case",
   "Statement II: false - droplets spread the common cold and pneumonia"],
  "Common Diseases in Humans", ans="C",
  why="Statement II gives typhoid the mode of spread of air-borne diseases, so it is false, while Statement I is "
      "true.", secs=35)

Z(HHD, "Immunity and vaccines", I, MAT,
  ML(("situation", "kind of immune phenomenon"),
     ["A new-born baby receives IgA antibodies through colostrum",
      "A person who recovered from an infection resists the same pathogen later",
      "The body attacks its own joint tissues, as in rheumatoid arthritis",
      "Sneezing, watery eyes and a running nose follow exposure to pollen"],
     ["Allergy", "Auto-immunity", "Active immunity", "Passive immunity"]),
  "Kinds of immune responses",
  "NCERT: when ready-made antibodies are given (e.g., IgA in colostrum, antibodies across the placenta) the "
  "immunity is passive; when the host meets an antigen and produces its own antibodies (natural infection or "
  "vaccination) it is active; when the body attacks self-cells it is an auto-immune disease, such as rheumatoid "
  "arthritis; the exaggerated response to environmental antigens such as pollen is allergy.",
  ["Colostrum IgA -> IV", "Recovery and later resistance -> III", "Rheumatoid arthritis -> II",
   "Pollen reaction -> I"],
  "Immunity",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The wrong codes swap active and passive immunity (who makes the antibodies), or allergy and auto-immunity "
      "(environmental antigen versus self-cells).", secs=45)

Z(HHD, "Immunity and vaccines", I, D,
  "According to NCERT, the secondary lymphoid organs, such as the spleen, lymph nodes and tonsils, provide the "
  "sites for:",
  "Secondary lymphoid organs",
  "NCERT: the primary lymphoid organs are the bone marrow and thymus, where immature lymphocytes differentiate "
  "into antigen-sensitive lymphocytes. After maturation the lymphocytes migrate to secondary lymphoid organs "
  "(spleen, lymph nodes, tonsils, Peyer's patches, appendix), which provide the sites for interaction of "
  "lymphocytes with the antigen; the lymphocytes then proliferate to become effector cells.",
  ["Primary organs: production and maturation of lymphocytes", "Secondary organs: lymphocyte-antigen "
   "interaction -> proliferation into effector cells"],
  "Immunity (Lymphoid organs)",
  at="D", correct="Interaction of lymphocytes with the antigen, after which the lymphocytes proliferate to become "
                  "effector cells",
  wrong=["Production of all blood cells, including lymphocytes",
         "Differentiation of immature lymphocytes into antigen-sensitive lymphocytes",
         "Secretion of interferons by virus-infected cells"],
  why="Production of all blood cells happens in the bone marrow, and maturation into antigen-sensitive "
      "lymphocytes in the primary lymphoid organs; interferons come from any virus-infected cell.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, MUL,
  MS("Which of the following are measures that NCERT suggests for the prevention and control of drug and "
     "alcohol abuse among adolescents?",
     ["Avoiding undue peer pressure",
      "Education and counselling, to help them face problems and stresses and accept disappointments and "
      "failures as part of life",
      "Seeking help from parents and peers",
      "Looking for danger signs, and seeking professional and medical help when needed",
      "Allowing adolescents to experiment with drugs once, so that they lose their curiosity"]),
  "Prevention of drug and alcohol abuse",
  "NCERT lists: avoid undue peer pressure; education and counselling; seeking help from parents and peers; "
  "looking for danger signs; seeking professional and medical help. Curiosity and the need for experimentation "
  "are among the CAUSES that NCERT says motivate youth towards drugs, so allowing experimentation is not a "
  "preventive measure.",
  ["(a)-(d): NCERT's measures", "(e): curiosity and experimentation are causes, not cures"],
  "Prevention and Control",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="(e) would encourage exactly the curiosity and experimentation that NCERT names as reasons for starting "
      "drugs, so every option containing (e) is wrong.", secs=40)

Z(HHD, "Drug and alcohol abuse", I, D,
  "According to NCERT, which of the following are the IMMEDIATE adverse effects of drug and alcohol abuse?",
  "Effects of drug and alcohol abuse",
  "NCERT: the immediate adverse effects of drugs and alcohol abuse are manifested in the form of reckless "
  "behaviour, vandalism and violence. Damage to the nervous system and liver cirrhosis follow chronic use, and "
  "the effects of anabolic steroids appear with their misuse over time.",
  ["Immediate: reckless behaviour, vandalism, violence", "Chronic: nervous system damage, cirrhosis"],
  "Effects of Drug/Alcohol Abuse",
  at="A", correct="Reckless behaviour, vandalism and violence",
  wrong=["Cirrhosis of the liver", "Damage to the nervous system", "Reduction in the size of the testicles"],
  why="Cirrhosis and nervous-system damage result from chronic use of drugs and alcohol, and reduced testicle "
      "size is a side-effect of misuse of anabolic steroids, not an immediate effect.", secs=30)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("A child is born without functional B-lymphocytes, but his T-lymphocytes are normal. Which of the following "
     "are expected?",
     ["Vaccination with weakened pathogens will produce high levels of antibodies.",
      "The humoral immune response fails, since antibodies are not produced.",
      "Cell-mediated immunity, such as rejection of a mismatched graft, can still occur.",
      "Passive immunity can still be provided by injecting preformed antibodies.",
      "Innate barriers such as the skin, stomach acid and phagocytes are also absent."]),
  "B-cells, T-cells and kinds of immunity",
  "NCERT: B-lymphocytes produce antibodies (humoral immune response); T-lymphocytes mediate cell-mediated "
  "immunity (CMI), which is responsible for graft rejection, and T-cells do not secrete antibodies. Passive "
  "immunity uses ready-made antibodies given from outside. Innate immunity (physical, physiological, cellular "
  "and cytokine barriers) is non-specific and does not depend on B-cells.",
  ["(a) false - no B-cells, so no antibodies even after vaccination", "(b) true", "(c) true - CMI is by "
   "T-cells", "(d) true - antibodies supplied from outside", "(e) false - innate barriers are separate"],
  "Immunity",
  at="A", correct="(b), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(a), (d) and (e) only", "(b), (c), (d) and (e) only"],
  why="(a) needs B-cells to make antibodies, and (e) wrongly ties innate barriers to B-cells; options containing "
      "either are wrong.", secs=60)

Z(HHD, "Immunity and vaccines", A, D,
  "In a patient the bone marrow stops functioning, but the thymus is normal. Based on NCERT's account of the "
  "lymphoid organs, what is expected?",
  "Bone marrow and thymus",
  "NCERT: the bone marrow is the main lymphoid organ where all blood cells, including lymphocytes, are produced. "
  "The thymus provides the micro-environment for the development and maturation of T-lymphocytes but does not "
  "produce lymphocytes from nothing. If the marrow fails, the supply of both B- and T-lymphocytes falls.",
  ["All blood cells, including lymphocytes, come from the bone marrow", "Thymus only matures T-cells that come "
   "to it", "Marrow failure -> both B- and T-lymphocytes fall"],
  "Immunity (Lymphoid organs)",
  at="C", correct="The supply of both B- and T-lymphocytes falls, because all blood cells, including lymphocytes, "
                  "are produced in the bone marrow",
  wrong=["Only B-lymphocytes fall; T-lymphocytes continue to be produced by the thymus itself",
         "Lymphocytes are unaffected, since they are produced in the lymph nodes",
         "Only red blood cells fall, since lymphocytes are not blood cells"],
  why="The thymus matures, but does not produce, lymphocytes; lymph nodes are secondary lymphoid organs where "
      "lymphocytes meet antigens; and lymphocytes are blood cells made in the marrow.", secs=50)

Z(HHD, "Drug and alcohol abuse", A, ASR,
  AR("Heroin is a depressant and slows down body functions.",
     "Heroin is obtained by the methylation of morphine."),
  "Heroin",
  "NCERT: heroin, commonly called smack, is chemically diacetylmorphine, a white, odourless, bitter crystalline "
  "compound obtained by ACETYLATION of morphine, which is extracted from the latex of the poppy plant. Heroin is "
  "a depressant and slows down body functions. A is true; R names the wrong reaction.",
  ["A: true", "R: false - acetylation (diacetylmorphine), not methylation"],
  "Drugs and Alcohol Abuse", ans="C",
  why="R is false, so the two 'both true' options are wrong; A is true, so 'A false but R true' is wrong.",
  secs=35)

Z(HHD, "Pathogens and diseases", A, MAT,
  ML(("pathogen", "how it reaches a healthy person"),
     ["Ascaris", "Entamoeba histolytica", "Streptococcus pneumoniae", "Plasmodium"],
     ["By inhaling droplets or aerosols released by an infected person, or by sharing glasses and utensils",
      "As eggs taken in with water, vegetables or fruits contaminated by the faeces of an infected person",
      "Through drinking water and food contaminated by faecal matter, with houseflies carrying the parasite to "
      "the food",
      "As sporozoites injected by the bite of an infected female Anopheles mosquito"]),
  "Modes of transmission",
  "NCERT: eggs of Ascaris are excreted with the faeces of infected persons and contaminate soil, water and "
  "plants; a healthy person acquires the infection through contaminated water, vegetables, fruits, etc. For "
  "amoebiasis, houseflies act as mechanical carriers that transmit the parasite from faeces to food, and drinking "
  "water and food contaminated by faecal matter are the main source of infection. Pneumonia is acquired by "
  "inhaling droplets/aerosols released by an infected person or by sharing glasses and utensils. Plasmodium "
  "enters as sporozoites through the bite of an infected female Anopheles mosquito.",
  ["Ascaris -> II (eggs)", "Entamoeba -> III (houseflies as carriers)", "S. pneumoniae -> I (droplets)",
   "Plasmodium -> IV (sporozoites)"],
  "Common Diseases in Humans",
  at="D", match=({"A": "II", "B": "III", "C": "I", "D": "IV"},
                 [{"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "I", "B": "III", "C": "II", "D": "IV"}]),
  why="Ascaris and Entamoeba both spread by faecal contamination, but only Ascaris is described as taken in as "
      "eggs and only amoebiasis with houseflies as carriers; pneumonia is air-borne and malaria vector-borne.",
  secs=55)

Z(HHD, "HIV and AIDS", A, MAT,
  ML(("component of HIV infection", "description in NCERT"),
     ["Macrophages", "Helper T-lymphocytes", "Reverse transcriptase", "ELISA"],
     ["A widely used diagnostic test for AIDS",
      "Enzyme with whose help the viral RNA genome is replicated to form viral DNA",
      "Their number decreases progressively in the infected person",
      "Continue to produce virus particles and act like an HIV factory"]),
  "Events in HIV infection",
  "NCERT: after entering the body, HIV enters macrophages, where its RNA genome is replicated to form viral DNA "
  "with the help of reverse transcriptase; the viral DNA is incorporated into the host DNA and the infected cells "
  "produce virus particles, so macrophages act like an HIV factory. HIV also enters helper T-lymphocytes, whose "
  "number decreases progressively. A widely used diagnostic test for AIDS is ELISA.",
  ["Macrophages -> IV", "Helper T-cells -> III", "Reverse transcriptase -> II", "ELISA -> I"],
  "AIDS",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The commonest trap swaps macrophages and helper T-cells: macrophages keep producing virus, while it is "
      "the helper T-cell count that falls. The other codes confuse the enzyme with the test.", secs=45)

Z(HHD, "Pathogens and diseases", A, STP,
  SP("Avoiding stagnation of water around houses and regularly cleaning household coolers helps to control both "
     "dengue and chikungunya.",
     "Introducing fishes like Gambusia into ponds can also help control filariasis, since the fishes feed on "
     "mosquito larvae."),
  "Vector control",
  "NCERT: the vectors of dengue and chikungunya are Aedes mosquitoes; measures such as avoiding stagnation of "
  "water near residential areas and regular cleaning of household coolers control mosquito breeding. Gambusia "
  "feeds on mosquito larvae, and filarial worms are transmitted through the bite of female mosquito vectors, so "
  "reducing mosquitoes also helps control filariasis.",
  ["Statement I: true - both diseases spread by Aedes; breeding sites removed",
   "Statement II: true - filariasis is mosquito-borne; Gambusia eats mosquito larvae"],
  "Common Diseases in Humans", ans="A",
  why="Both measures reduce mosquito vectors, and NCERT names mosquitoes as the vectors of dengue, chikungunya "
      "and filariasis, so neither statement is false.", secs=45)

Z(HHD, "Drug and alcohol abuse", A, MUL,
  MS("A man has smoked and chewed tobacco for many years. According to NCERT, he is at increased risk of which "
     "of the following?",
     ["Cancer of the lung", "Cancer of the oral cavity", "Bronchitis and emphysema", "Coronary heart disease",
      "An increase in the concentration of haem-bound oxygen in his blood"]),
  "Effects of tobacco",
  "NCERT: smoking is associated with increased incidence of cancers of the lung, urinary bladder and throat, "
  "bronchitis, emphysema, coronary heart disease, gastric ulcer, etc.; tobacco chewing is associated with "
  "increased risk of cancer of the oral cavity. Smoking increases the carbon monoxide content of blood and "
  "REDUCES the concentration of haem-bound oxygen, causing oxygen deficiency in the body.",
  ["(a), (c), (d): smoking", "(b): chewing", "(e) false - haem-bound oxygen is reduced by CO"],
  "Drugs and Alcohol Abuse",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="Smoking raises carbon monoxide and lowers haem-bound oxygen, so (e) is the reverse of NCERT; every option "
      "with (e) is wrong.", secs=45)

# ================================================================ Biotechnology: Principles and Processes (6/7/6)
Z(BPP, "Bioreactors and downstream processing", B, D,
  "Small-volume cultures cannot yield appreciable quantities of products. According to NCERT, bioreactors are "
  "used for large-scale production because in them large volumes of culture can be processed, of about:",
  "Scale of bioreactors",
  "NCERT: to produce in large quantities, bioreactors are developed where large volumes (100-1000 litres) of "
  "culture can be processed. Bioreactors can be thought of as vessels in which raw materials are biologically "
  "converted into specific products.",
  ["Small cultures -> small yields", "Bioreactors -> 100-1000 litres of culture"],
  "Processes of Recombinant DNA Technology (Obtaining the foreign gene product)",
  at="B", correct="100 to 1000 litres",
  wrong=["1 to 10 millilitres", "Less than 1 litre", "1 to 10 million litres"],
  why="Millilitre and sub-litre volumes are small laboratory cultures, which NCERT says cannot give appreciable "
      "yields; millions of litres is far beyond NCERT's figure.", secs=20)

Z(BPP, "Restriction enzymes", B, D,
  "The discovery of which enzymes, often called 'molecular scissors', made it possible to cut DNA at specific "
  "locations and thus to construct the first recombinant DNA?",
  "Molecular scissors",
  "NCERT: the cutting of DNA at specific locations became possible with the discovery of the so-called "
  "'molecular scissors' - restriction enzymes. The cut piece of DNA was then linked with the plasmid DNA by the "
  "enzyme DNA ligase.",
  ["Cutting at specific sites -> restriction enzymes (molecular scissors)", "Joining -> DNA ligase"],
  "Principles of Biotechnology",
  at="D", correct="Restriction enzymes",
  wrong=["DNA ligases", "DNA polymerases", "Ribonucleases"],
  why="DNA ligase joins DNA fragments rather than cutting them; DNA polymerase synthesises DNA; ribonuclease "
      "removes RNA during DNA isolation.", secs=20)

Z(BPP, "Restriction enzymes", B, D,
  "According to NCERT, more than 900 restriction enzymes are known today, each recognising a different "
  "recognition sequence. These enzymes have been isolated from:",
  "Sources of restriction enzymes",
  "NCERT: today we know more than 900 restriction enzymes that have been isolated from over 230 strains of "
  "bacteria, each of which recognises different recognition sequences.",
  ["More than 900 restriction enzymes", "Isolated from over 230 bacterial strains"],
  "Tools of Recombinant DNA Technology (Restriction enzymes)",
  at="B", correct="Over 230 strains of bacteria",
  wrong=["A single strain of Escherichia coli", "Over 230 species of fungi",
         "Bacteriophages that infect Escherichia coli"],
  why="Restriction enzymes are bacterial enzymes that restrict phage growth; they come from many bacterial "
      "strains, not one strain of E. coli, and not from fungi or from the phages themselves.", secs=20)

Z(BPP, "Bioreactors and downstream processing", B, MAT,
  ML(("part of a stirred-tank bioreactor", "function"),
     ["Stirrer (agitator)", "Sparger", "Sampling ports", "Foam control system"],
     ["Controls the foam formed in the culture",
      "Allows small volumes of the culture to be withdrawn periodically",
      "Bubbles sterile air through the culture, greatly increasing the area for oxygen transfer",
      "Facilitates even mixing and oxygen availability throughout the bioreactor"]),
  "Stirred-tank bioreactor",
  "NCERT: the stirrer facilitates even mixing and oxygen availability throughout the bioreactor; in sparged "
  "stirred-tank bioreactors sterile air bubbles are sparged, which greatly increases the area for oxygen "
  "transfer; a bioreactor has an agitator system, an oxygen delivery system, a foam control system, a "
  "temperature control system, a pH control system and sampling ports so that small volumes of the culture can "
  "be withdrawn periodically.",
  ["Stirrer -> IV", "Sparger -> III", "Sampling ports -> II", "Foam control -> I"],
  "Processes of Recombinant DNA Technology (Obtaining the foreign gene product)",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="Both the stirrer and the sparger help oxygen supply, but only the sparger bubbles air; sampling ports "
      "remove small samples and do not add medium.", secs=40)

Z(BPP, "PCR and gel electrophoresis", B, ASR,
  AR("DNA fragments separated by agarose gel electrophoresis are seen as bright orange-coloured bands after "
     "staining with ethidium bromide and exposure to UV radiation.",
     "Ethidium bromide cuts DNA into smaller fragments of different sizes."),
  "Visualising DNA after electrophoresis",
  "NCERT: the separated DNA fragments can be visualised only after staining the DNA with a compound known as "
  "ethidium bromide followed by exposure to UV radiation; the DNA fragments are seen as bright orange coloured "
  "bands. Ethidium bromide is a stain; DNA is cut by restriction enzymes before electrophoresis. A is true, R "
  "false.",
  ["A: true", "R: false - restriction enzymes cut DNA; ethidium bromide only stains it"],
  "Processes of Recombinant DNA Technology (Separation and isolation of DNA fragments)", ans="C",
  why="R is false, so both 'both true' options are wrong; A is true, so 'A false but R true' is wrong.", secs=30)

Z(BPP, "Cloning vectors", B, STP,
  SP("Plasmid DNA acts as a vector to transfer the piece of DNA attached to it into the host.",
     "Plasmids are linear DNA molecules that replicate only along with the bacterial chromosome."),
  "Plasmids as vectors",
  "NCERT: plasmid DNA acts as a vector to transfer the piece of DNA attached to it. Plasmids are autonomously "
  "replicating, circular, extra-chromosomal DNA; plasmids and bacteriophages can replicate within bacterial "
  "cells independent of the control of chromosomal DNA.",
  ["Statement I: true", "Statement II: false - plasmids are circular and replicate independently of the "
   "chromosome"],
  "Principles of Biotechnology; Tools of Recombinant DNA Technology (Cloning vectors)", ans="C",
  why="Statement II contradicts both features that make plasmids useful vectors (circular, autonomous "
      "replication), while Statement I is NCERT's line.", secs=30)

VECTOR_KB, INSERT_KB = F(44, 10), F(16, 10)
RECOMB_KB = VECTOR_KB + INSERT_KB
SITES = 2                      # the original site is now present at both junctions
assert RECOMB_KB == 6 and SITES == 2   # a circle with 2 sites gives 2 fragments: 4.4 kb and 1.6 kb
Z(BPP, "Cloning vectors", I, NUM,
  "A circular vector of 4.4 kb has a single BamHI site. A 1.6 kb DNA fragment with BamHI sticky ends at both "
  "ends is ligated into this site. The recombinant plasmid is then completely digested with BamHI. What is the "
  "size of the recombinant plasmid, and what does the digestion give?",
  "Recombinant plasmid and restriction digestion",
  "Size = 4.4 + 1.6 = 6.0 kb. Inserting a fragment with BamHI ends into the BamHI site recreates a BamHI site at "
  "each junction, so the recombinant has two BamHI sites. Cutting a circular DNA at 2 sites gives 2 fragments: "
  "the 4.4 kb vector and the 1.6 kb insert.",
  ["Recombinant size = 4.4 + 1.6 = 6.0 kb", "BamHI sites in the recombinant = 2 (one at each junction)",
   "Circular DNA with n sites -> n fragments -> 4.4 kb and 1.6 kb"],
  "Tools of Recombinant DNA Technology (Restriction enzymes; Cloning vectors)",
  at="B", correct="6.0 kb; two fragments, of 4.4 kb and 1.6 kb",
  wrong=["6.0 kb; three fragments", "4.4 kb; a single fragment of 4.4 kb", "6.0 kb; a single linear fragment of "
                                                                          "6.0 kb"],
  why="Three fragments would need three sites (or a linear molecule with two); 4.4 kb ignores the insert; a "
      "single 6.0 kb fragment counts only one site in the recombinant.", secs=60, vb=RECOMPUTED)

SEQS = ["GTTAAC", "CTGCAG", "GATATC", "AGCTAG", "GAACTC"]
assert sum(s == revcomp(s) for s in SEQS) == 3
Z(BPP, "Restriction enzymes", I, D,
  "A palindrome in DNA reads the same on the two strands when the orientation of reading is kept the same "
  "(5' → 3'). How many of the following double-stranded sequences, each given as its upper (5' → 3') strand, "
  "are palindromes?\n\n5'-GTTAAC-3', 5'-CTGCAG-3', 5'-GATATC-3', 5'-AGCTAG-3', 5'-GAACTC-3'",
  "Palindromic recognition sequences",
  "Write the complementary strand and read it 5' → 3' (that is, take the reverse complement). GTTAAC -> GTTAAC, "
  "CTGCAG -> CTGCAG and GATATC -> GATATC are palindromes. AGCTAG -> CTAGCT and GAACTC -> GAGTTC are not.",
  ["GTTAAC: reverse complement GTTAAC - palindrome", "CTGCAG: CTGCAG - palindrome",
   "GATATC: GATATC - palindrome", "AGCTAG: CTAGCT - not", "GAACTC: GAGTTC - not", "Total = 3"],
  "Tools of Recombinant DNA Technology (Restriction enzymes)",
  at="B", correct="Three", wrong=["Two", "Four", "Five"],
  short="A DNA palindrome equals its own reverse complement.",
  why="Reading the second strand in the same direction is the test; counting AGCTAG or GAACTC uses the plain "
      "complement or a simple reversal instead of the reverse complement.", secs=60)

ECO = "GAATTC"
CUT = 1                                     # EcoRI cuts between G and A
top_overhang = ECO[CUT:len(ECO) - CUT]
assert top_overhang == "AATT" and revcomp(top_overhang) == "AATT"
Z(BPP, "Restriction enzymes", I, D,
  "EcoRI recognises 5'-GAATTC-3' (complementary strand 3'-CTTAAG-5') and cuts each strand between the bases G "
  "and A. What is the single-stranded overhang on each sticky end produced?",
  "Sticky ends of EcoRI",
  "Cutting the upper strand G^AATTC and the lower strand (read 5' → 3', also G^AATTC) leaves each fragment with a "
  "single-stranded stretch of 5'-AATT-3'. Because the site is palindromic, both sticky ends carry the same "
  "overhang, which is why they can pair with each other by hydrogen bonds.",
  ["Upper strand: G | AATTC", "Lower strand, read 5' → 3': G | AATTC", "Each end keeps an unpaired 5'-AATT-3'"],
  "Tools of Recombinant DNA Technology (Restriction enzymes)",
  at="A", correct="5'-AATT-3' on each end", wrong=["5'-GAAT-3' on each end", "5'-TC-3' on each end",
                                                  "No overhang, since EcoRI gives blunt ends"],
  why="GAAT would need a cut between T and C; a two-base overhang would need a cut in the middle of the other "
      "strand; and NCERT shows EcoRI producing sticky, not blunt, ends.", secs=50)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("During the isolation of DNA, the preparation is treated with ribonuclease.",
     "When the cell is broken open, RNA is released along with DNA, and DNA must be free from other "
     "macromolecules before it can be cut with restriction enzymes."),
  "Purifying DNA before restriction digestion",
  "NCERT: to cut DNA with restriction enzymes it needs to be in pure form, free from other macromolecules. When "
  "the cell is broken open, DNA is released along with other macromolecules such as RNA, proteins, "
  "polysaccharides and lipids. RNA is removed by treatment with ribonuclease, proteins with protease. R is the "
  "reason for A.",
  ["A: true", "R: true", "RNA present + DNA must be pure -> RNA removed by ribonuclease -> R explains A"],
  "Processes of Recombinant DNA Technology (Isolation of the genetic material)", ans="A",
  why="Both statements are true and the need to remove RNA is exactly why ribonuclease is used, so B, C and D are "
      "wrong.", secs=35)

Z(BPP, "Restriction enzymes", I, STP,
  SP("Exonucleases make cuts at specific positions within the DNA, whereas endonucleases remove nucleotides from "
     "the ends of the DNA.",
     "Restriction enzymes belong to a larger class of enzymes called nucleases."),
  "Exonucleases and endonucleases",
  "NCERT: restriction enzymes belong to a larger class of enzymes called nucleases, of two kinds: exonucleases "
  "remove nucleotides from the ends of the DNA, whereas endonucleases make cuts at specific positions within the "
  "DNA. Statement I swaps the two.",
  ["Statement I: false - the roles are swapped", "Statement II: true"],
  "Tools of Recombinant DNA Technology (Restriction enzymes)", ans="D",
  why="Statement I is false and Statement II true; the prefix 'endo-' (within) is the clue that endonucleases cut "
      "inside the molecule.", secs=30)

Z(BPP, "PCR and gel electrophoresis", I, MAT,
  ML(("step or component of PCR", "what happens or why it is used"),
     ["Denaturation", "Annealing", "Extension", "Thermostable DNA polymerase (from Thermus aquaticus)"],
     ["Remains active during the high temperature used to separate the DNA strands",
      "DNA polymerase extends the primers using the nucleotides provided and the template DNA",
      "Primers bind to complementary regions of the single-stranded template DNA",
      "Double-stranded DNA is separated into single strands by high temperature"]),
  "Steps of the polymerase chain reaction",
  "NCERT: each PCR cycle has three steps: denaturation (high temperature separates the strands), annealing (the "
  "two sets of primers bind to complementary regions) and extension (DNA polymerase extends the primers using "
  "the nucleotides provided and the genomic DNA as template). A thermostable DNA polymerase, isolated from "
  "Thermus aquaticus, is used because it remains active during the high-temperature denaturation.",
  ["Denaturation -> IV", "Annealing -> III", "Extension -> II", "Thermostable polymerase -> I"],
  "Processes of Recombinant DNA Technology (Amplification of gene of interest using PCR)",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The wrong codes swap denaturation with annealing, annealing with extension, or extension with the reason "
      "for using a thermostable enzyme.", secs=40)

Z(BPP, "PCR and gel electrophoresis", I, MUL,
  MS("A restriction digest gives three DNA fragments of 0.5 kb, 2 kb and 5 kb, which are separated by agarose gel "
     "electrophoresis. Which of the following are correct?",
     ["The 0.5 kb fragment moves farthest from the well.",
      "The 5 kb fragment stays closest to the well.",
      "After staining with ethidium bromide and exposure to UV radiation, three bright orange bands are seen.",
      "The fragments move towards the cathode (negative electrode).",
      "The 2 kb band can be cut out of the gel and the DNA extracted (eluted) for use in constructing "
      "recombinant DNA."]),
  "Reading an agarose gel",
  "NCERT: DNA fragments are negatively charged and move towards the anode under an electric field; they "
  "separate according to size through the sieving effect of the agarose gel, so the smaller the fragment the "
  "farther it moves. Bands are seen after ethidium bromide staining and UV exposure as bright orange bands; the "
  "separated bands are cut out and extracted (elution), and the purified fragments are used in constructing "
  "recombinant DNA.",
  ["(a) true - smallest moves farthest", "(b) true - largest moves least", "(c) true - three sizes, three bands",
   "(d) false - towards the anode", "(e) true - elution"],
  "Processes of Recombinant DNA Technology (Separation and isolation of DNA fragments)",
  at="B", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (d) only", "(c), (d) and (e) only", "(b), (c), (d) and (e) only"],
  why="DNA is negatively charged and moves to the anode, so (d) is false and every option containing it is "
      "wrong.", secs=45)

SITE_LEN, DNA_BP = 6, 409_600
assert DNA_BP // 4 ** SITE_LEN == 100 and DNA_BP // 4 ** 4 == 1600 and DNA_BP // 4 ** 7 == 25
Z(BPP, "Restriction enzymes", A, NUM,
  "Assume a DNA molecule whose sequence is random, with A, T, G and C equally frequent. On average, how many "
  "recognition sites of a restriction enzyme that recognises one specific 6-bp palindromic sequence (such as "
  "EcoRI's 5'-GAATTC-3') are expected in 409,600 bp of this DNA? (Count along one strand; because the site is "
  "palindromic, the other strand gives the same sites.)",
  "Frequency of a recognition sequence",
  "The chance that any given 6 consecutive bases match one specific sequence is (1/4)⁶ = 1/4096. So a 6-bp site "
  "is expected about once every 4096 bp. Expected sites = 409,600 / 4096 = 100.",
  ["P(one specific base) = 1/4", "P(specific 6-bp sequence) = (1/4)⁶ = 1/4096",
   "409,600 / 4096 = 100 sites"],
  "Tools of Recombinant DNA Technology (Restriction enzymes)",
  at="A", correct="100", wrong=["1,600", "25", "68,267"],
  short="A specific n-bp site occurs about once every 4ⁿ bp.",
  why="1,600 uses a 4-bp site (4⁴ = 256); 25 uses 4⁷; 68,267 divides by 6 instead of by 4⁶.", secs=70,
  vb=RECOMPUTED)

Z(BPP, "Competent hosts and transformation", A, MUL,
  MS("Which of the following methods introduce recombinant DNA into host cells WITHOUT using a 'disarmed "
     "pathogen' that infects the cell?",
     ["Micro-injection of recombinant DNA into the nucleus of an animal cell",
      "Biolistics (gene gun) with DNA-coated gold or tungsten micro-particles",
      "Treatment of bacterial cells with calcium ions followed by a heat shock",
      "Use of the Ti plasmid of Agrobacterium tumefaciens",
      "Use of disarmed retroviruses"]),
  "Methods of introducing DNA into hosts",
  "NCERT: in micro-injection recombinant DNA is directly injected into the nucleus of an animal cell; in "
  "biolistics, cells are bombarded with high-velocity micro-particles of gold or tungsten coated with DNA "
  "(suitable for plants); bacteria are made competent with a divalent cation such as calcium and given a heat "
  "shock. The Ti plasmid of Agrobacterium and disarmed retroviruses are 'disarmed pathogen' vectors which, when "
  "allowed to infect the cell, transfer the recombinant DNA into the host.",
  ["(a), (b), (c): physical or chemical methods", "(d), (e): disarmed pathogen vectors"],
  "Processes of Recombinant DNA Technology (Insertion of recombinant DNA into the host cell/organism)",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(d) and (e) only", "(a), (d) and (e) only", "(b), (c) and (d) only"],
  why="Agrobacterium (Ti plasmid) and retroviruses are pathogens modified to be harmless, so they are exactly the "
      "'disarmed pathogen' vectors excluded by the question.", secs=45)

Z(BPP, "PCR and gel electrophoresis", A, ASR,
  AR("In PCR, the DNA polymerase does not have to be added afresh after each denaturation step.",
     "The thermostable DNA polymerase isolated from Thermus aquaticus remains active during the high temperature "
     "used for denaturation of double-stranded DNA."),
  "Why a thermostable polymerase is used",
  "NCERT: the PCR enzyme is a thermostable DNA polymerase (isolated from the bacterium Thermus aquaticus), which "
  "remains active during the high temperature induced denaturation of double-stranded DNA. Because the enzyme is "
  "not destroyed when the reaction is heated to separate the strands, the same enzyme works through repeated "
  "cycles. R explains A.",
  ["Denaturation needs high temperature", "Thermostable enzyme survives it", "So it need not be replaced each "
   "cycle -> R explains A"],
  "Processes of Recombinant DNA Technology (Amplification of gene of interest using PCR)", ans="A",
  why="An ordinary polymerase would be inactivated at the denaturation temperature; the thermostability stated "
      "in R is exactly why A holds, so B, C and D are wrong.", secs=40)

Z(BPP, "PCR and gel electrophoresis", A, STP,
  SP("In PCR, the part of the template that gets amplified is decided by the primers, because the DNA polymerase "
     "extends the primers bound to complementary regions of the template.",
     "PCR can amplify a gene only after the gene has been cloned in a plasmid and introduced into a living host "
     "cell."),
  "What PCR needs",
  "NCERT: in PCR, multiple copies of the gene (or DNA) of interest are synthesised in vitro using two sets of "
  "primers (small chemically synthesised oligonucleotides complementary to regions of DNA) and the enzyme DNA "
  "polymerase, which extends the primers. The primers therefore mark the ends of the amplified region. PCR is "
  "done in vitro; its product can later be ligated with a vector for cloning, but no host cell is needed for the "
  "amplification.",
  ["Statement I: true - amplification runs between the primer-binding regions",
   "Statement II: false - PCR is an in vitro method"],
  "Processes of Recombinant DNA Technology (Amplification of gene of interest using PCR)", ans="C",
  why="Statement II reverses the order of events: PCR products may be cloned afterwards, but PCR itself needs no "
      "living cell.", secs=40)

Z(BPP, "Cloning vectors", A, MAT,
  ML(("observation after transformation", "interpretation"),
     ["With a vector carrying ampR and tetR, the insert placed in tetR: a colony grows on ampicillin but not on "
      "tetracycline",
      "With the same vector: a colony grows on both ampicillin and tetracycline",
      "A bacterium spread on an ampicillin plate does not grow at all",
      "With a vector whose insert site lies in the β-galactosidase gene: a colony gives no colour with the "
      "chromogenic substrate"],
     ["Insertional inactivation of the β-galactosidase gene by the insert",
      "The cell did not take up the vector",
      "Transformant carrying the vector without an insert",
      "Insertional inactivation of the tetracycline resistance gene by the insert"]),
  "Selection of recombinants",
  "NCERT: normal E. coli cells do not carry resistance against these antibiotics, so a cell that does not grow "
  "on ampicillin has not taken up the vector. If foreign DNA is inserted within the tetracycline resistance gene, "
  "recombinants lose tetracycline resistance but still grow on ampicillin; non-recombinant transformants grow on "
  "both. With β-galactosidase as marker, colonies whose plasmid has an insert give no colour, while those "
  "without an insert give blue colonies.",
  ["Grows on amp, not tet -> IV", "Grows on both -> III", "No growth on amp -> II", "No colour -> I"],
  "Tools of Recombinant DNA Technology (Cloning vectors)",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="Growth on both antibiotics means both genes are intact (no insert), while loss of tetracycline resistance "
      "marks the recombinant; a colourless colony marks an insert in the β-galactosidase gene, not a cell "
      "without the vector.", secs=60)

Z(BPP, "Competent hosts and transformation", A, D,
  "A researcher uses a vector whose only selectable marker is the ampicillin resistance gene, but by mistake the "
  "E. coli strain used as the host is already resistant to ampicillin. What problem will arise when the treated "
  "cells are plated on an ampicillin-containing medium?",
  "Why the host must lack the marker",
  "NCERT: selectable markers help in identifying and eliminating non-transformants; antibiotic resistance genes "
  "are useful markers for E. coli because normal E. coli cells do not carry resistance against these "
  "antibiotics. Only the transformants then grow on the antibiotic. If the host is already resistant, every cell "
  "grows, so transformants cannot be told apart from non-transformants.",
  ["Selection works only if non-transformants are killed by the antibiotic", "Host already resistant -> all "
   "cells grow -> no selection"],
  "Tools of Recombinant DNA Technology (Cloning vectors)",
  at="C", correct="Non-transformants will also grow, so transformants cannot be distinguished from them",
  wrong=["No cells will grow, because the two resistance genes cancel each other",
         "Only the recombinants will grow, because the insert inactivates the host's resistance gene",
         "The vector will not replicate, because the host already has an origin of replication"],
  why="Resistance genes do not cancel; the insert sits in the vector, not in the host chromosome; and the "
      "vector's ori works independently of the host's own replication.", secs=50)

# ================================================================ Biotechnology and its Applications (5/7/5)
Z(BTA, "Bt crops and RNAi", B, D,
  "NCERT lists several ways in which genetic modification has been useful in crop plants. Which of the following "
  "is NOT one of them?",
  "Uses of genetically modified plants",
  "NCERT: genetic modification has (i) made crops more tolerant to abiotic stresses (cold, drought, salt, heat), "
  "(ii) reduced reliance on chemical pesticides (pest-resistant crops), (iii) helped to reduce post-harvest "
  "losses, (iv) increased efficiency of mineral usage by plants, and (v) enhanced nutritional value of food, e.g. "
  "golden rice.",
  ["Listed: stress tolerance, reduced reliance on pesticides, fewer post-harvest losses, better mineral use, "
   "better nutrition", "Increased reliance on pesticides is the opposite of (ii)"],
  "Biotechnological Applications in Agriculture",
  at="B", correct="Increased reliance on chemical pesticides",
  wrong=["Crops more tolerant to abiotic stresses such as cold, drought, salt and heat",
         "Reduced post-harvest losses",
         "Increased efficiency of mineral usage by plants"],
  why="The other three are NCERT's own examples of the benefits of GM plants; pest-resistant GM crops reduce, "
      "not increase, the use of chemical pesticides.", secs=25)

Z(BTA, "Biosafety, biopiracy and patents", B, D,
  "A company wants to introduce a new genetically modified crop for cultivation in India. According to NCERT, "
  "which organisation set up by the Indian Government makes decisions regarding the validity of GM research and "
  "the safety of introducing GM organisms for public services?",
  "Regulation of GM organisms in India",
  "NCERT: the Indian Government has set up organisations such as GEAC, which will make decisions regarding the "
  "validity of GM research and the safety of introducing GM-organisms for public services. (NCERT expands GEAC "
  "as the Genetic Engineering Approval Committee; the committee is now officially called the Genetic Engineering "
  "Appraisal Committee, which is why the option gives only the abbreviation.)",
  ["GM organism for public use -> safety and validity decided by GEAC"],
  "Ethical Issues",
  at="C", correct="GEAC",
  wrong=["NACO", "CDRI, Lucknow", "The US Patent and Trademark Office"],
  why="NACO works on AIDS awareness, CDRI developed the pill Saheli, and the US Patent and Trademark Office "
      "granted the Basmati patent; none decides on GM organisms in India.", secs=25)

Z(BTA, "Bt crops and RNAi", B, MAT,
  ML(("gene or DNA introduced", "condition it was used to control"),
     ["cryIAc and cryIIAb", "cryIAb", "Nematode-specific genes producing sense and anti-sense RNA",
      "Functional ADA cDNA"],
     ["An immune disorder in a child, treated by gene therapy", "Infection of tobacco roots by Meloidegyne "
      "incognitia", "Damage by the corn borer", "Damage to cotton by bollworms"]),
  "Genes used in applied biotechnology",
  "NCERT: the proteins encoded by cryIAc and cryIIAb control the cotton bollworms, and that of cryIAb controls "
  "the corn borer. Nematode-specific genes introduced into tobacco produced sense and anti-sense RNA, which "
  "protected the roots from Meloidegyne incognitia by RNAi. A functional ADA cDNA was introduced into the "
  "lymphocytes of a child with ADA deficiency (ADA is crucial for the immune system to function).",
  ["cryIAc, cryIIAb -> IV", "cryIAb -> III", "Nematode genes -> II", "ADA cDNA -> I"],
  "Biotechnological Applications in Agriculture; Gene Therapy",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The commonest slip swaps the cotton genes (cryIAc, cryIIAb) with the corn gene (cryIAb); the nematode "
      "genes act through RNAi, not as cry toxins.", secs=40)

Z(BTA, "Bt crops and RNAi", B, MUL,
  MS("Which of the following statements about RNA interference (RNAi) are correct according to NCERT?",
     ["RNAi takes place in all eukaryotic organisms as a method of cellular defence.",
      "The source of the complementary RNA could be an infection by viruses having RNA genomes.",
      "The source of the complementary RNA could also be mobile genetic elements (transposons) that replicate "
      "via an RNA intermediate.",
      "RNAi is a method of cellular defence found only in prokaryotes.",
      "RNAi works only when the Bt toxin protein is also present in the cell."]),
  "RNA interference",
  "NCERT: RNAi takes place in all eukaryotic organisms as a method of cellular defence. It involves silencing of a "
  "specific mRNA due to a complementary dsRNA molecule. The source of this complementary RNA could be from an "
  "infection by viruses having RNA genomes or mobile genetic elements (transposons) that replicate via an RNA "
  "intermediate. RNAi has nothing to do with the Bt toxin.",
  ["(a), (b), (c): NCERT", "(d) false - eukaryotes", "(e) false - RNAi and Bt toxin are separate strategies"],
  "Biotechnological Applications in Agriculture",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
  why="(d) contradicts (a), since NCERT says RNAi occurs in all eukaryotes; (e) mixes up two unrelated "
      "pest-resistance methods.", secs=35)

Z(BTA, "Human insulin", B, STP,
  SP("Insulin used for diabetes was earlier extracted from the pancreas of slaughtered cattle and pigs.",
     "About 30 recombinant therapeutics have been approved for human use the world over."),
  "Insulin and recombinant therapeutics",
  "Both are NCERT statements. Insulin was earlier extracted from the pancreas of slaughtered cattle and pigs "
  "(which caused allergy or other reactions in some patients). NCERT also says that at present about 30 "
  "recombinant therapeutics have been approved for human use the world over.",
  ["Statement I: true", "Statement II: true"],
  "Biotechnological Applications in Medicine", ans="A",
  why="Both statements are true, so any option that calls either of them false is wrong.", secs=25)

Z(BTA, "Transgenic animals", I, MAT,
  ML(("use of transgenic animals", "reason, as classified in NCERT"),
     ["Transgenic sheep give milk containing a human protein needed to treat a disease",
      "Transgenic mice are used, in place of monkeys, to check a new batch of vaccine",
      "Transgenic mice made more sensitive to a toxic substance give the results of a drug's toxicity testing in "
      "less time",
      "Transgenic mice carrying a gene for a human disease are used to try out new treatments"],
     ["Study of disease", "Chemical safety testing", "Vaccine safety", "Biological products"]),
  "Why transgenic animals are produced",
  "NCERT gives these reasons: biological products (e.g., human α-1-antitrypsin, human α-lactalbumin in milk); "
  "vaccine safety (transgenic mice being developed to test the safety of the polio vaccine, which could replace "
  "monkeys); chemical safety testing (animals made more sensitive to toxic substances give results in less time); "
  "study of disease (transgenic models to investigate new treatments for human diseases).",
  ["Human protein in milk -> IV", "Vaccine testing -> III", "Toxicity testing -> II", "Disease models -> I"],
  "Transgenic Animals",
  at="C", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="Each wrong code places a situation under a neighbouring reason; the purpose of the experiment (a product, "
      "vaccine checking, toxicity testing or a disease model) decides the category.", secs=45)

Z(BTA, "Human insulin", I, MAT,
  ML(("figure in NCERT", "what it refers to"),
     ["1983", "1990", "27", "2.4 grams per litre"],
     ["Amount of human protein in the milk of the transgenic cow Rosie",
      "Number of documented varieties of Basmati grown in India",
      "Year of the first clinical gene therapy, given for ADA deficiency",
      "Year in which Eli Lilly prepared DNA sequences for chains A and B of human insulin and introduced them "
      "into plasmids of E. coli"]),
  "Landmarks in applied biotechnology",
  "NCERT: in 1983 Eli Lilly prepared two DNA sequences corresponding to chains A and B of human insulin and "
  "introduced them into plasmids of E. coli; the first clinical gene therapy was given in 1990 to a 4-year-old "
  "girl with ADA deficiency; there are 27 documented varieties of Basmati grown in India; Rosie, the first "
  "transgenic cow (1997), produced human protein-enriched milk (2.4 grams per litre) containing human "
  "α-lactalbumin.",
  ["1983 -> IV (insulin)", "1990 -> III (gene therapy)", "27 -> II (Basmati)", "2.4 g/L -> I (Rosie)"],
  "Biotechnological Applications in Medicine; Transgenic Animals; Ethical Issues",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The two years are the usual mix-up: insulin chains in E. coli came first (1983), gene therapy later "
      "(1990); 27 is a count of varieties and 2.4 a concentration, so they cannot be exchanged.", secs=45)

Z(BTA, "Bt crops and RNAi", I, D,
  "In the RNAi strategy against Meloidegyne incognitia, suppose that by mistake a gene essential to the tobacco "
  "plant itself, rather than a nematode-specific gene, is introduced so that it produces both sense and anti-sense "
  "RNA in the plant cells. What is the most likely result?",
  "Specificity of RNA interference",
  "NCERT: RNAi involves silencing of a specific mRNA due to a complementary dsRNA molecule that binds to and "
  "prevents translation of the mRNA. In the tobacco example the dsRNA was made from nematode genes, so it "
  "silenced a specific mRNA of the nematode. RNAi occurs in all eukaryotes, so a dsRNA made from the plant's own "
  "gene would silence the matching mRNA of the plant itself.",
  ["Sense + anti-sense RNA -> dsRNA", "dsRNA silences the mRNA complementary to it", "Plant gene used -> plant "
   "mRNA silenced -> plant harmed, nematode not targeted"],
  "Biotechnological Applications in Agriculture",
  at="C", correct="The dsRNA formed would silence the matching mRNA of the tobacco plant, harming the plant "
                  "rather than the nematode",
  wrong=["The nematode would still be killed, because any dsRNA is toxic to nematodes",
         "Nothing would happen, because RNA interference does not occur in plants",
         "The plant would become resistant to bollworms, because the dsRNA acts like the Bt toxin"],
  why="RNAi silences only the mRNA complementary to the dsRNA, so it is not a general nematode poison; RNAi "
      "occurs in all eukaryotes, plants included; and dsRNA does not act like the Bt toxin protein.", secs=50)

Z(BTA, "Bt crops and RNAi", I, ASR,
  AR("Bt toxin genes are expressed in crop plants to make them resistant to insect pests.",
     "After being activated by the alkaline pH of the insect gut, the Bt toxin binds to the midgut epithelial "
     "cells and creates pores that cause swelling and lysis of the cells, eventually killing the insect."),
  "How Bt crops resist insects",
  "NCERT: Bt toxin genes isolated from Bacillus thuringiensis are incorporated into crop plants such as cotton, "
  "providing resistance to insects without the need for insecticides. The toxin kills the insect that eats the "
  "plant: the inactive protoxin is solubilised and activated by the alkaline gut pH, binds to the midgut "
  "epithelial cells and creates pores, causing swelling and lysis and eventually death. R explains why the "
  "expressing crop is resistant.",
  ["A: true", "R: true - the mode of action of Bt toxin", "Insect eating the crop is killed -> crop protected -> "
   "R explains A"],
  "Biotechnological Applications in Agriculture", ans="A",
  why="Both are NCERT statements, and the killing of feeding insects described in R is what gives the crop its "
      "resistance, so B, C and D are wrong.", secs=40)

Z(BTA, "Biosafety, biopiracy and patents", I, MUL,
  MS("A foreign company uses neem, an Indian traditional herbal medicine, together with the traditional "
     "knowledge of the people, to make a commercial product and patents it, without authorisation from India or "
     "the people concerned and without any compensatory payment. Which of the following are correct according "
     "to NCERT?",
     ["NCERT mentions neem among the Indian traditional herbal medicines on which attempts have been made to "
      "patent uses, products and processes.",
      "Use of bio-resources in this way, without proper authorisation and compensatory payment, is called "
      "biopiracy.",
      "The developing and the under-developed world is rich in biodiversity and traditional knowledge related to "
      "bio-resources.",
      "Industrialised nations are rich in biodiversity and traditional knowledge, so they rarely need bio-resources "
      "from other countries.",
      "Biopiracy means using bio-resources only after paying full compensation to the countries concerned."]),
  "Biopiracy",
  "NCERT: there have been attempts to patent uses, products and processes based on Indian traditional herbal "
  "medicines, e.g., turmeric and neem. Biopiracy is the term used to refer to the use of bio-resources by "
  "multinational companies and other organisations without proper authorisation from the countries and people "
  "concerned and without compensatory payment. Industrialised nations are rich financially but poor in "
  "biodiversity and traditional knowledge, whereas the developing and under-developed world is rich in them.",
  ["(a) true - turmeric and neem", "(b) true - definition of biopiracy", "(c) true",
   "(d) false - industrialised nations are poor in biodiversity", "(e) false - biopiracy is WITHOUT payment"],
  "Ethical Issues",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (d) and (e) only", "(b) and (e) only", "(a), (b), (c) and (d) only"],
  why="(d) reverses which nations are rich in biodiversity, and (e) reverses the definition of biopiracy, so any "
      "option containing them is wrong.", secs=50)

Z(BTA, "Transgenic animals", I, ASR,
  AR("Transgenic mice are being developed for use in testing the safety of the polio vaccine.",
     "Over 95 per cent of all existing transgenic animals are mice."),
  "Transgenic mice",
  "Both are NCERT statements. The reason given for A is vaccine safety: if successful, transgenic mice could "
  "replace monkeys for testing the safety of batches of the polio vaccine. R is a separate fact about how common "
  "transgenic mice are; it does not explain why they are used to test the polio vaccine.",
  ["A: true (vaccine safety)", "R: true (statistic)", "R does not give the reason for A"],
  "Transgenic Animals", ans="B",
  why="Both are true, so C and D are wrong; the share of mice among transgenic animals is a different fact and "
      "not the reason for using them in vaccine testing, so A is also wrong.", secs=35)

Z(BTA, "Gene therapy", I, STP,
  SP("In the gene therapy given for ADA deficiency, lymphocytes from the patient's blood were grown in a culture "
     "outside the body.",
     "The functional ADA cDNA was introduced into these lymphocytes by biolistics (gene gun)."),
  "Steps of ADA gene therapy",
  "NCERT: in gene therapy for ADA deficiency, lymphocytes from the blood of the patient are grown in a culture "
  "outside the body; a functional ADA cDNA is then introduced into these lymphocytes using a retroviral vector, "
  "and the cells are returned to the patient.",
  ["Statement I: true", "Statement II: false - a retroviral vector was used, not biolistics"],
  "Gene Therapy", ans="C",
  why="Biolistics is described in NCERT as a method suited to plant cells; the ADA cDNA was delivered by a "
      "retroviral vector, so Statement II is false and Statement I true.", secs=30)

Z(BTA, "Bt crops and RNAi", A, D,
  "A tomato crop is badly damaged by beetles (coleopterans). Following NCERT's account of Bt crops, which "
  "transgenic approach would be most suitable?",
  "Choosing Bt toxin genes for a target pest",
  "NCERT: some strains of Bacillus thuringiensis produce proteins that kill certain insects such as lepidopterans, "
  "coleopterans (beetles) and dipterans; most Bt toxins are insect-group specific, and the choice of genes "
  "depends upon the crop and the targeted pest. Bt toxin genes have been expressed in tomato among other crops. "
  "So the tomato should be given toxin genes from a strain whose protein kills coleopterans.",
  ["Pest = coleopteran", "Bt toxins are insect-group specific", "Choose genes from a strain toxic to "
   "coleopterans and express them in tomato"],
  "Biotechnological Applications in Agriculture",
  at="C", correct="Express in tomato the toxin gene from a strain of Bacillus thuringiensis whose protein kills "
                  "coleopterans",
  wrong=["Express cryIAc and cryIIAb, since these genes control every kind of insect",
         "Introduce nematode-specific genes so that RNAi silences the beetles' mRNA",
         "Introduce the genes used in golden rice, since vitamin A protects plants from beetles"],
  why="cryIAc and cryIIAb are named for cotton bollworms, and Bt toxins are not effective against every insect; "
      "RNAi with nematode genes would target a nematode, not beetles; golden rice genes improve nutrition, not "
      "pest resistance.", secs=55)

Z(BTA, "Human insulin", A, D,
  "Suppose that, instead of following Eli Lilly's approach, a company expressed in E. coli a single gene for "
  "human pro-insulin. Based on NCERT, what additional step would be needed to obtain functional insulin?",
  "Pro-insulin and mature insulin",
  "NCERT: in mammals, including humans, insulin is synthesised as a pro-hormone which contains an extra stretch "
  "called the C peptide; this C peptide is not present in mature insulin and is removed during maturation into "
  "insulin. The main challenge was getting insulin assembled into a mature form, which Eli Lilly avoided by "
  "making chains A and B separately and joining them by disulphide bonds. A pro-insulin product would still "
  "need its C peptide removed.",
  ["Pro-insulin = A + B + C peptide", "Mature insulin lacks the C peptide", "So the C peptide must be removed"],
  "Biotechnological Applications in Medicine (Genetically Engineered Insulin)",
  at="D", correct="Removal of the C peptide, to convert the pro-hormone into mature insulin",
  wrong=["Addition of a C peptide, which mature insulin requires",
         "Separation of chains A and B so that they are never joined",
         "Conversion of the protein into DNA before injection"],
  why="The C peptide is absent from mature insulin, so it must be removed, not added; chains A and B must be "
      "linked (by disulphide bridges) in functional insulin; and a protein is not converted into DNA.", secs=45)

Z(BTA, "Gene therapy", A, MAT,
  ML(("problem", "solution described in NCERT"),
     ["Some patients developed allergy to insulin from slaughtered cattle and pigs",
      "Genetically engineered lymphocytes are not immortal, so infusions must be repeated",
      "Emphysema patients need human α-1-antitrypsin",
      "People eating mainly rice may lack vitamin A"],
     ["Golden rice", "Transgenic animals producing the human protein",
      "Introducing the ADA gene into cells at early embryonic stages", "Human insulin produced by recombinant DNA "
      "technology"]),
  "Problems and biotechnological solutions",
  "NCERT: animal insulin caused allergy or other reactions in some patients, a problem avoided by recombinant "
  "human insulin; lymphocyte-based ADA therapy needs periodic infusion because the cells are not immortal, while "
  "introducing the gene from ADA-producing marrow cells into cells at early embryonic stages could be a permanent "
  "cure; transgenic animals have been used to make human α-1-antitrypsin used to treat emphysema; golden rice is "
  "a GM crop enriched in vitamin A.",
  ["Allergy -> IV", "Short-lived lymphocytes -> III", "Emphysema -> II", "Vitamin A -> I"],
  "Biotechnological Applications in Medicine; Gene Therapy; Transgenic Animals",
  at="B", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The wrong codes give the insulin problem the transgenic-animal solution, give the lymphocyte problem a "
      "protein product instead of early embryonic gene introduction, or exchange golden rice with α-1-antitrypsin.",
  secs=50)

Z(BTA, "Biosafety, biopiracy and patents", A, STP,
  SP("A patent is the right granted by a government to an inventor to prevent others from commercial use of his "
     "invention.",
     "There is a growing realisation of the injustice, inadequate compensation and benefit sharing between "
     "developed and developing countries."),
  "Patents and benefit sharing",
  "Both are NCERT statements. A patent is a right granted by a government to an inventor to prevent others from "
  "commercial use of the invention. In its discussion of biopiracy, NCERT also notes a growing realisation of the "
  "injustice, inadequate compensation and benefit sharing between developed and developing countries.",
  ["Statement I: true - definition of a patent", "Statement II: true - injustice and inadequate benefit sharing"],
  "Ethical Issues", ans="A",
  why="Both statements are NCERT's own lines, so no option calling either false is correct.", secs=30)

Z(BTA, "Bt crops and RNAi", A, MUL,
  MS("Which of the following statements correctly compare Bt cotton with the RNAi-based tobacco that resists "
     "Meloidegyne incognitia?",
     ["In Bt cotton the protective molecule is a protein, whereas in the RNAi tobacco it is a double-stranded RNA.",
      "The genes used in Bt cotton come from a bacterium, whereas those used in the RNAi tobacco come from the "
      "pest (the nematode) itself.",
      "Vectors derived from Agrobacterium were used to introduce the nematode-specific genes into tobacco.",
      "Both strategies work by silencing a specific mRNA of the pest.",
      "Both strategies kill the pest by creating pores in the cells of its midgut."]),
  "Two strategies for pest resistance",
  "NCERT: Bt cotton expresses cry genes isolated from the bacterium Bacillus thuringiensis; the toxin protein "
  "kills insects by binding to midgut epithelial cells and making pores. In the tobacco example, "
  "nematode-specific genes were introduced into the host plant using Agrobacterium vectors; they produced sense "
  "and anti-sense RNA, which formed dsRNA that silenced a specific mRNA of the nematode (RNAi).",
  ["(a) true - protein vs dsRNA", "(b) true - bacterial genes vs nematode genes", "(c) true - Agrobacterium "
   "vectors", "(d) false - only RNAi silences mRNA", "(e) false - only the Bt toxin forms pores"],
  "Biotechnological Applications in Agriculture",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
  why="(d) applies only to RNAi and (e) only to the Bt toxin; each wrongly extends one mechanism to both crops.",
  secs=60)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 125
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
    assert all(x["suggested_time_seconds"] <= 180 for x in QUESTIONS)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_007", "created_at": TODAY,
           "notes": "ZOO_007_p2: 125 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers and computed match/count keys re-derived in tools/batch_007/ZOO_007_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
