"""Builder for package ZOO_008_p2 of BATCH_008 (Zoology, 133 questions, NEET_ZOO_001868..NEET_ZOO_002000).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_008/ZOO_008_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_008_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_008_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_008_ZOO_p2.json"
FIRST_ID = 1868

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


# ================================================================ Chemical Coordination and Integration (5/7/5)
Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "NCERT divides the adrenal cortex into three layers. Which layer lies outermost, just below the capsule of the "
  "gland?",
  "Layers of the adrenal cortex",
  "NCERT: the adrenal cortex can be divided into three layers, called zona reticularis (inner layer), zona "
  "fasciculata (middle layer) and zona glomerulosa (outer layer). The adrenal medulla is the centrally located "
  "tissue, not a layer of the cortex.",
  ["Inner layer: zona reticularis", "Middle layer: zona fasciculata", "Outer layer: zona glomerulosa"],
  "Adrenal Gland",
  at="D", correct="Zona glomerulosa",
  wrong=["Zona fasciculata", "Zona reticularis", "Adrenal medulla"],
  why="Zona fasciculata is the middle layer and zona reticularis the inner layer of the cortex; the adrenal medulla "
      "is the central tissue of the gland and lies inside the cortex, not outside it.", secs=20)

Z(CCI, "Hypothalamus and pituitary", B, D,
  "Oxytocin and vasopressin are released into the blood from the posterior pituitary (neurohypophysis). According "
  "to NCERT, what is the role of the neurohypophysis with respect to these two hormones?",
  "Neurohypophysis stores and releases hypothalamic hormones",
  "NCERT: the neurohypophysis (pars nervosa), also known as the posterior pituitary, stores and releases two "
  "hormones called oxytocin and vasopressin, which are actually synthesised by the hypothalamus and are "
  "transported axonally to the neurohypophysis.",
  ["Synthesis: hypothalamic neurosecretory cells", "Transport: along axons to the pars nervosa",
   "Neurohypophysis: storage and release into the blood"],
  "The Pituitary Gland",
  at="B", correct="It stores and releases them, though they are synthesised by the hypothalamus and reach it "
                  "through axons",
  wrong=["It synthesises them from precursors supplied by the pars distalis",
         "It receives them from the hypothalamus through the hypophyseal portal blood vessels and modifies them",
         "It converts them from inactive to active forms that are then sent to the pars intermedia"],
  why="The neurohypophysis does not synthesise these hormones; the portal circulation links the hypothalamus with "
      "the anterior pituitary, whereas the posterior pituitary receives its hormones axonally; and nothing is sent "
      "on to the pars intermedia.", secs=30)

Z(CCI, "Mechanism of hormone action", B, D,
  "FSH is a protein hormone. Based on NCERT's account of hormone action, how does FSH bring about its effect on "
  "its target cells?",
  "Action of protein hormones",
  "NCERT: hormones which interact with membrane-bound receptors normally do not enter the target cell, but generate "
  "second messengers (e.g., cyclic AMP, IP₃, Ca²⁺) which in turn regulate cellular metabolism. NCERT's diagram uses "
  "FSH as the example of a protein hormone acting in this way, while steroid hormones enter the cell and act "
  "through intracellular receptors.",
  ["FSH = protein hormone -> membrane-bound receptor", "Hormone-receptor complex -> second messenger (cAMP)",
   "Second messenger -> biochemical and physiological responses"],
  "Mechanism of Hormone Action",
  at="D", correct="It binds to a membrane-bound receptor and, without entering the cell, generates a second "
                  "messenger such as cyclic AMP",
  wrong=["It enters the nucleus and binds directly to DNA to start transcription",
         "It diffuses through the plasma membrane and binds to an intracellular receptor in the nucleus",
         "It is converted into a steroid inside the cell, which then acts on the genome"],
  why="Entering the cell and acting through intracellular (nuclear) receptors on the genome is the route of steroid "
      "hormones and iodothyronines, not of protein hormones; and protein hormones are not converted into steroids.",
  secs=30)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "Which of the following is described in NCERT both as an endocrine gland (secreting a hormone) and as a primary "
  "lymphoid organ?",
  "Thymus: endocrine gland and lymphoid organ",
  "In the chapter on chemical coordination, the thymus is an endocrine gland that secretes thymosins, which play a "
  "major role in the differentiation of T-lymphocytes. In the chapter on human health and disease, the bone marrow "
  "and the thymus are the primary lymphoid organs, where immature lymphocytes differentiate into "
  "antigen-sensitive lymphocytes.",
  ["Thymus secretes thymosins (endocrine role)", "Thymus is a primary lymphoid organ where T-lymphocytes mature",
   "Thyroid, pineal and adrenal are endocrine glands only"],
  "Thymus; Class 12 Biology, Ch 7 'Human Health and Disease', Lymphoid Organs",
  at="B", correct="Thymus",
  wrong=["Thyroid gland", "Pineal gland", "Adrenal gland"],
  why="The thyroid, pineal and adrenal glands are endocrine glands, but none of them is a lymphoid organ; the "
      "primary lymphoid organs are the bone marrow and the thymus.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", B, STP,
  SP("The testis is composed of seminiferous tubules and stromal or interstitial tissue.",
     "The Leydig cells, present in the intertubular spaces of the testis, produce a group of hormones called "
     "androgens, mainly testosterone."),
  "Endocrine role of the testis",
  "Both are NCERT lines. The testis performs dual functions, as a primary sex organ and as an endocrine gland; it is "
  "composed of seminiferous tubules and stromal or interstitial tissue, and the Leydig (interstitial) cells in the "
  "intertubular spaces produce androgens, mainly testosterone.",
  ["Statement I: true - seminiferous tubules + interstitial tissue", "Statement II: true - Leydig cells -> "
   "androgens (testosterone)"],
  "Testis", ans="A",
  why="Both statements are correct, so every option that calls either of them false is wrong.", secs=30)

Z(CCI, "Thyroid, parathyroid and pineal", I, ASR,
  AR("The immune responses of old persons become weak.",
     "The thymus degenerates in old individuals, resulting in a decreased production of thymosins."),
  "Thymus and ageing",
  "NCERT: thymosins play a major role in the differentiation of T-lymphocytes, which provide cell-mediated immunity, "
  "and also promote the production of antibodies to provide humoral immunity. The thymus is degenerated in old "
  "individuals, resulting in a decreased production of thymosins; as a result, the immune responses of old persons "
  "become weak. So R is the reason NCERT gives for A.",
  ["A: true (NCERT)", "R: true - thymus degenerates, less thymosin", "Less thymosin -> weaker cell-mediated and "
   "humoral immunity -> R explains A"],
  "Thymus", ans="A",
  why="R is the cause NCERT states for A, so 'R is not the correct explanation' is wrong, and neither statement is "
      "false.", secs=35)

Z(CCI, "Hypothalamus and pituitary", I, D,
  "A tumour of the pars distalis secretes much more TSH than normal, while the thyroid gland itself is normal. "
  "Which of the following is expected?",
  "Excess TSH and the thyroid",
  "NCERT: TSH stimulates the synthesis and secretion of thyroid hormones from the thyroid gland, and thyroid "
  "hormones play an important role in the regulation of the basal metabolic rate. Excess TSH therefore drives the "
  "normal thyroid to secrete more thyroid hormones, raising the BMR (as in hyperthyroid states, where weight loss "
  "is seen).",
  ["Excess TSH -> thyroid stimulated", "More T₄ and T₃ secreted", "Thyroid hormones regulate BMR -> BMR rises"],
  "The Pituitary Gland; Thyroid Gland",
  at="B", correct="Increased secretion of thyroid hormones, raising the basal metabolic rate",
  wrong=["Decreased secretion of thyroid hormones, lowering the basal metabolic rate",
         "Increased secretion of parathyroid hormone, raising the blood calcium level",
         "Increased secretion of glucocorticoids by the adrenal cortex"],
  why="TSH stimulates, not inhibits, the thyroid; the parathyroid is regulated by blood calcium, not by TSH; and "
      "glucocorticoid secretion is stimulated by ACTH, not by TSH.", secs=40)

Z(CCI, "Hormonal disorders", I, MUL,
  MS("According to NCERT, which of the following hormones act on the kidney (renal tubules) as one of their "
     "actions?",
     ["Vasopressin (ADH)", "Aldosterone", "Parathyroid hormone", "Glucagon", "Melanocyte stimulating hormone"]),
  "Hormones acting on the kidney",
  "NCERT: vasopressin acts mainly at the kidney and stimulates resorption of water and electrolytes by the distal "
  "tubules; aldosterone acts mainly at the renal tubules and stimulates reabsorption of Na⁺ and water and "
  "excretion of K⁺ and phosphate ions; PTH stimulates reabsorption of Ca²⁺ by the renal tubules. Glucagon acts "
  "mainly on hepatocytes and MSH on melanocytes.",
  ["(a) ADH -> distal tubules: yes", "(b) aldosterone -> renal tubules: yes", "(c) PTH -> Ca²⁺ reabsorption by "
   "renal tubules: yes", "(d) glucagon -> hepatocytes: no", "(e) MSH -> melanocytes: no"],
  "The Pituitary Gland; Parathyroid Gland; Adrenal Gland",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (e) only"],
  why="'(a) and (b) only' misses PTH, which also acts on the renal tubules; the other two include glucagon "
      "(liver cells) or MSH (melanocytes), neither of which NCERT describes as acting on the kidney.", secs=45)

Z(CCI, "Hypothalamus and pituitary", I, MAT,
  ML(("hormone", "what regulates or triggers its secretion, as described in NCERT"),
     ["Parathyroid hormone", "Adrenaline and noradrenaline", "Thyroid hormones", "Oxytocin at child birth"],
     ["Stress of any kind and emergency situations", "TSH from the pars distalis",
      "Foetal ejection reflex (mild uterine contractions)", "Circulating level of calcium ions"]),
  "Regulation of hormone secretion",
  "NCERT: the secretion of PTH is regulated by the circulating levels of calcium ions; adrenaline and noradrenaline "
  "are rapidly secreted in response to stress of any kind and during emergency situations; TSH stimulates the "
  "synthesis and secretion of thyroid hormones; at the end of pregnancy, the foetal ejection reflex triggers the "
  "release of oxytocin from the maternal pituitary.",
  ["PTH -> IV", "Catecholamines -> I", "Thyroid hormones -> II", "Oxytocin at parturition -> III"],
  "Parathyroid Gland; Adrenal Gland; The Pituitary Gland; Class 12 Ch 2, Parturition and Lactation",
  at="A", match=({"A": "IV", "B": "I", "C": "II", "D": "III"},
                 [{"A": "II", "B": "I", "C": "IV", "D": "III"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "II", "D": "III"}]),
  why="PTH is regulated by blood calcium, not by TSH; oxytocin release at birth is triggered by the foetal "
      "ejection reflex, while catecholamines respond to stress; and the thyroid is stimulated by TSH, not by "
      "calcium.", secs=50)

Z(CCI, "Hormonal disorders", I, STP,
  SP("Both cretinism and pituitary dwarfism are characterised by stunted growth.",
     "Acromegaly results from low secretion of growth hormone in adults, especially in middle age."),
  "Growth disorders",
  "NCERT: hypothyroidism during pregnancy causes defective development of the growing baby, leading to stunted "
  "growth (cretinism), mental retardation, low IQ, abnormal skin and deaf-mutism; low secretion of growth hormone "
  "results in stunted growth, resulting in pituitary dwarfism. Acromegaly results from EXCESS secretion of growth "
  "hormone in adults, especially in middle age.",
  ["Statement I: true - stunted growth is part of both", "Statement II: false - acromegaly = excess GH in "
   "adults"],
  "The Pituitary Gland; Thyroid Gland", ans="C",
  why="Statement II reverses the cause of acromegaly, so options calling it true are wrong; Statement I is a "
      "correct combination of two NCERT descriptions.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", I, D,
  "A drug blocks the receptors for glucagon on hepatocytes, while insulin acts normally. Based on NCERT, which "
  "change is expected in the liver and the blood?",
  "Glucagon action on the liver",
  "NCERT: glucagon acts mainly on the liver cells (hepatocytes) and stimulates glycogenolysis, resulting in an "
  "increased blood sugar; it also stimulates gluconeogenesis, which contributes to hyperglycemia. A hormone acts "
  "only after binding its specific receptor, so with the receptors blocked, glycogenolysis and gluconeogenesis "
  "driven by glucagon fall, and the blood glucose tends to fall.",
  ["Glucagon must bind its receptor on hepatocytes", "Blocked -> less glycogenolysis and gluconeogenesis",
   "Less glucose released into blood -> blood glucose tends to fall"],
  "Pancreas; Mechanism of Hormone Action",
  at="C", correct="Glycogenolysis and gluconeogenesis in the liver decrease, so the blood glucose level tends to "
                  "fall",
  wrong=["Glycogenolysis in the liver increases, so the blood glucose level rises",
         "The liver stops responding to insulin as well, so glycogenesis stops completely",
         "The β-cells stop secreting insulin, so the blood glucose level rises"],
  why="Blocking glucagon removes its hyperglycemic action, so blood glucose cannot rise for this reason; each "
      "receptor is specific to one hormone, so insulin's action is not blocked; and nothing in the case affects "
      "the β-cells.", secs=45)

Z(CCI, "Mechanism of hormone action", I, ASR,
  AR("Estradiol produces its effects mainly by generating second messengers such as cyclic AMP at the surface of "
     "its target cells.",
     "Estradiol is a steroid hormone."),
  "Steroid hormones act through intracellular receptors",
  "NCERT classifies estradiol with cortisol, testosterone and progesterone as steroids. Hormones which interact "
  "with intracellular receptors (e.g., steroid hormones, iodothyronines) mostly regulate gene expression or "
  "chromosome function by the interaction of the hormone-receptor complex with the genome. Generating second "
  "messengers at the membrane is the route of hormones acting through membrane-bound receptors. So A is false and "
  "R is true.",
  ["R: estradiol is a steroid - true", "Steroids -> intracellular receptors -> gene expression",
   "So A (second messengers at the cell surface) is false"],
  "Mechanism of Hormone Action", ans="D",
  why="A describes the action of protein hormones, not of a steroid like estradiol, so any option calling A true "
      "is wrong; R is a correct NCERT classification.", secs=40)

Z(CCI, "Hypothalamus and pituitary", A, D,
  "In a person, a small lesion destroys only the pars intermedia of the pituitary, while the pars distalis, the pars "
  "nervosa and the hypothalamus remain intact. Based on NCERT's account of the human pituitary, the secretion of "
  "which hormone, and hence which function, would be directly affected?",
  "Pars intermedia and MSH",
  "NCERT: the pituitary is divided anatomically into an adenohypophysis (pars distalis and pars intermedia) and a "
  "neurohypophysis (pars nervosa). The pars intermedia secretes only one hormone, melanocyte stimulating hormone "
  "(MSH), and in humans it is almost merged with the pars distalis. MSH acts on the melanocytes (pigment-containing "
  "cells) and regulates pigmentation of the skin. GH and prolactin come from the pars distalis; oxytocin and "
  "vasopressin are released from the pars nervosa; melatonin is a pineal hormone.",
  ["Pars intermedia -> only MSH", "MSH -> melanocytes -> skin pigmentation", "Pars distalis (GH, PRL) and pars "
   "nervosa (oxytocin, vasopressin) intact"],
  "The Pituitary Gland",
  at="B", correct="MSH, which acts on the melanocytes and regulates pigmentation of the skin",
  wrong=["Oxytocin and vasopressin, since the pars intermedia is a part of the neurohypophysis",
         "Growth hormone and prolactin, since in humans these are made by the pars intermedia",
         "Melatonin, which regulates the 24-hour (diurnal) rhythm of the body"],
  why="The pars intermedia belongs to the adenohypophysis, not the neurohypophysis; GH and prolactin are pars "
      "distalis hormones, which is intact; and melatonin is secreted by the pineal gland, not the pituitary.",
  secs=50)

Z(CCI, "Hypothalamus and pituitary", A, MUL,
  MS("In a patient, the pars distalis of the pituitary is destroyed, but the hypothalamus, the neurohypophysis and "
     "all other endocrine glands are intact. Which of the following are expected?",
     ["Secretion of thyroid hormones falls, lowering the basal metabolic rate.",
      "Vasopressin continues to be released from the posterior pituitary.",
      "Secretion of glucocorticoids by the adrenal cortex falls.",
      "Secretion of parathyroid hormone stops, since PTH secretion depends on the pituitary.",
      "Secretion of insulin by the β-cells stops, since the islets are controlled by ACTH."]),
  "Consequences of losing the anterior pituitary",
  "The pars distalis produces GH, PRL, TSH, ACTH, LH and FSH. Losing TSH lowers thyroid hormone secretion (and so "
  "BMR); losing ACTH lowers glucocorticoid secretion. Vasopressin is synthesised by the hypothalamus and released "
  "from the neurohypophysis, which is intact. PTH secretion is regulated by the circulating level of calcium ions, "
  "and NCERT does not describe insulin secretion as controlled by any pituitary hormone.",
  ["(a) TSH lost -> thyroid hormones fall: yes", "(b) neurohypophysis intact -> vasopressin released: yes",
   "(c) ACTH lost -> glucocorticoids fall: yes", "(d) PTH depends on blood Ca²⁺: no", "(e) insulin not under "
   "ACTH: no"],
  "The Pituitary Gland; Parathyroid Gland; Pancreas",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only"],
  why="'(a) and (c) only' wrongly drops vasopressin, whose release does not involve the pars distalis; (d) and (e) "
      "are false because PTH is regulated by blood calcium and insulin is not under ACTH.", secs=60)

Z(CCI, "Hormonal disorders", A, MAT,
  ML(("finding in a patient", "endocrine tissue most likely at fault"),
     ["Prolonged hyperglycemia, with glucose and ketone bodies in the urine",
      "Excessive loss of water in dilute urine, with dehydration, though blood glucose is normal",
      "Acute weakness and fatigue due to altered carbohydrate metabolism",
      "In an adult woman, irregular menstrual cycles together with a low basal metabolic rate"],
     ["Thyroid gland (hypothyroidism)", "Adrenal cortex (under-production)",
      "β-cells of the islets of Langerhans (insulin)", "Hypothalamus and neurohypophysis (ADH)"]),
  "Locating an endocrine defect",
  "NCERT: prolonged hyperglycemia with loss of glucose and formation of ketone bodies is diabetes mellitus, treated "
  "with insulin (β-cells). Impaired synthesis or release of ADH causes diabetes insipidus, with excessive loss of "
  "water and dehydration; ADH is made by the hypothalamus and released from the neurohypophysis. Under-production "
  "of adrenal cortex hormones alters carbohydrate metabolism, causing acute weakness and fatigue (Addison's "
  "disease). Hypothyroidism in adult women may make the menstrual cycle irregular, and thyroid hormones regulate "
  "the BMR.",
  ["A -> III (insulin)", "B -> IV (ADH)", "C -> II (adrenal cortex)", "D -> I (thyroid)"],
  "The Pituitary Gland; Thyroid Gland; Adrenal Gland; Pancreas",
  at="C", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="The wrong codes exchange the two kinds of 'diabetes' (insulin vs ADH), exchange Addison's disease with "
      "hypothyroidism, or give ADH's water loss to the adrenal cortex.", secs=60)

Z(CCI, "Hypothalamus and pituitary", A, ASR,
  AR("If the hypothalamus of a man stops secreting GnRH, both the secretion of androgens and spermatogenesis "
     "decline.",
     "GnRH stimulates the pituitary to release gonadotrophins; LH stimulates the Leydig cells to secrete "
     "androgens, and FSH and androgens regulate spermatogenesis."),
  "Hypothalamus-pituitary-testis chain",
  "NCERT: GnRH from the hypothalamus stimulates the pituitary synthesis and release of gonadotrophins (LH and FSH). "
  "In males, LH acts on the Leydig cells and stimulates the synthesis and secretion of androgens, and FSH and "
  "androgens regulate spermatogenesis. Without GnRH, LH and FSH fall, so androgen secretion and spermatogenesis "
  "both decline. R gives exactly this chain, so it explains A.",
  ["No GnRH -> LH and FSH fall", "Less LH -> less androgen from Leydig cells", "Less FSH and androgen -> "
   "spermatogenesis declines -> R explains A"],
  "Hypothalamus; The Pituitary Gland; Testis", ans="A",
  why="R is the complete causal chain for A, so 'R is not the correct explanation' is wrong, and both statements "
      "are true.", secs=50)

Z(CCI, "Hormonal disorders", A, D,
  "Two patients both pass unusually large volumes of urine. In patient P the blood glucose stays high and the "
  "urine contains glucose and ketone bodies. In patient Q the blood glucose is normal, the urine has no glucose and "
  "the patient becomes dehydrated. Based on NCERT, which hormonal defects are most likely?",
  "Diabetes mellitus vs diabetes insipidus",
  "NCERT: prolonged hyperglycemia leads to diabetes mellitus, associated with loss of glucose through urine and "
  "formation of harmful compounds called ketone bodies; it is treated with insulin. Impaired synthesis or release "
  "of ADH results in a diminished ability of the kidney to conserve water, leading to water loss and dehydration "
  "(diabetes insipidus). P fits insulin deficiency, Q fits ADH deficiency.",
  ["P: hyperglycemia + glucose + ketone bodies -> diabetes mellitus (insulin)", "Q: water loss, no glucose -> "
   "diabetes insipidus (ADH)"],
  "The Pituitary Gland; Pancreas",
  at="D", correct="P lacks insulin action (diabetes mellitus); Q has impaired synthesis or release of ADH "
                  "(diabetes insipidus)",
  wrong=["P has impaired release of ADH; Q lacks insulin action",
         "Both P and Q lack insulin action, Q being only a milder case",
         "P has excess glucagon from the adrenal medulla; Q has excess aldosterone"],
  why="The first option swaps the two disorders; Q has no hyperglycemia, so it is not a case of insulin "
      "deficiency; glucagon comes from the α-cells of the pancreas, not the adrenal medulla, and excess "
      "aldosterone increases Na⁺ and water reabsorption rather than causing water loss.", secs=55)


# ================================================================ Human Reproduction (7/8/7)
Z(HR, "Gametogenesis", B, D,
  "According to NCERT, spermatogenesis in a human male starts at the age of puberty because of:",
  "Onset of spermatogenesis",
  "NCERT: spermatogenesis starts at the age of puberty due to a significant increase in the secretion of "
  "gonadotropin releasing hormone (GnRH), a hypothalamic hormone. The increased GnRH acts on the anterior "
  "pituitary and stimulates the secretion of the gonadotropins LH and FSH.",
  ["Puberty -> GnRH secretion rises significantly", "GnRH -> anterior pituitary -> LH and FSH",
   "LH and FSH -> testis -> spermatogenesis begins"],
  "Gametogenesis",
  at="D", correct="A significant increase in the secretion of GnRH by the hypothalamus",
  wrong=["A sharp fall in the secretion of GnRH by the hypothalamus",
         "The first appearance of Sertoli cells in the seminiferous tubules at puberty",
         "The secretion of hCG by the testes at puberty"],
  why="NCERT links puberty to a rise, not a fall, in GnRH; Sertoli cells line the tubules already and are not "
      "described as appearing only at puberty; and hCG is a placental hormone of pregnancy, not a testicular "
      "hormone.", secs=25)

Z(HR, "Menstrual cycle", B, D,
  "In the menstrual phase, the breakdown of the endometrial lining of the uterus and its blood vessels forms a "
  "liquid that comes out through the vagina. According to NCERT, the menstrual flow lasts for about:",
  "Duration of menstrual flow",
  "NCERT: the cycle starts with the menstrual phase, when menstrual flow occurs, and it lasts for 3-5 days. The "
  "whole cycle is repeated at an average interval of about 28/29 days.",
  ["Menstrual phase = first phase of the cycle", "Menstrual flow lasts 3-5 days"],
  "Menstrual Cycle",
  at="C", correct="3-5 days",
  wrong=["One day only", "10-12 days", "28/29 days"],
  why="Ten to twelve days is far longer than NCERT's figure, one day is too short, and 28/29 days is the length of "
      "the whole menstrual cycle, not of the flow.", secs=20)

Z(HR, "Pregnancy, parturition and lactation", B, STP,
  SP("Breast-feeding during the initial period of infant growth is recommended by doctors for bringing up a "
     "healthy baby.",
     "Colostrum is the milk produced during the last few days of lactation, just before the baby is weaned."),
  "Lactation and colostrum",
  "NCERT: the milk produced during the initial few days of lactation is called colostrum, which contains several "
  "antibodies absolutely essential to develop resistance for the new-born babies. Breast-feeding during the "
  "initial period of infant growth is recommended by doctors for bringing up a healthy baby. Statement II wrongly "
  "places colostrum at the end of lactation.",
  ["Statement I: true (NCERT)", "Statement II: false - colostrum is the milk of the initial few days"],
  "Parturition and Lactation", ans="C",
  why="Colostrum belongs to the initial few days of lactation, so any option calling Statement II true is wrong; "
      "Statement I is NCERT's own line.", secs=30)

Z(HR, "Fertilisation and implantation", B, NUM,
  "A couple already has two daughters and is expecting a third child. Using NCERT's account of how the sex of the "
  "baby is decided at fertilisation (all ova carry X; 50 per cent of sperms carry X and 50 per cent carry Y), what "
  "is the probability that the third child will be a son?",
  "Sex of the child in each pregnancy",
  "Each ovum carries an X chromosome; half of the sperms carry X and half carry Y, and whichever sperm fertilises "
  "the ovum decides the sex (XX female, XY male). Each pregnancy is an independent event, so in every pregnancy "
  "the probability of a male child is always 50 per cent, whatever the sexes of the earlier children.",
  ["Probability that the fertilising sperm carries Y = 1/2", "Earlier births do not change this",
   "P(son) = 1/2 = 50 per cent"],
  "Fertilisation and Implantation; Class 12 Ch 4 'Principles of Inheritance and Variation', Sex Determination",
  at="B", correct="1/2 (50 per cent)", wrong=["1/8", "1/4", "3/4"],
  why="1/8 is the chance of three daughters in a row, not of the next child's sex; 1/4 squares the 1/2; 3/4 "
      "wrongly assumes that two daughters make a son more likely. Each pregnancy is independent.",
  secs=30, vb=RECOMPUTED)

Z(HR, "Gametogenesis", B, ASR,
  AR("Spermatogonia present on the inside wall of the seminiferous tubules are diploid cells.",
     "Spermatogonia increase in number by meiotic divisions."),
  "Spermatogonia",
  "NCERT: the spermatogonia present on the inside wall of the seminiferous tubules multiply by mitotic division and "
  "increase in number. Each spermatogonium is diploid and contains 46 chromosomes. Meiosis begins only when some "
  "spermatogonia become primary spermatocytes. So A is true and R is false.",
  ["A: true - spermatogonia are diploid (46 chromosomes)", "R: false - they multiply by mitosis, not meiosis"],
  "Gametogenesis", ans="C",
  why="R is false (spermatogonia divide mitotically), so options calling R true are wrong; A is a correct NCERT "
      "statement.", secs=30)

Z(HR, "Gametogenesis", B, D,
  "According to NCERT, about how many sperms does a human male ejaculate during a coitus?",
  "Sperm number in an ejaculate",
  "NCERT: the human male ejaculates about 200 to 300 million sperms during a coitus, of which, for normal "
  "fertility, at least 60 per cent must have normal shape and size and at least 40 per cent must show vigorous "
  "motility.",
  ["NCERT figure: 200 to 300 million sperms per ejaculate"],
  "Gametogenesis",
  at="D", correct="200 to 300 million",
  wrong=["2 to 3 million", "20 to 30 thousand", "60,000 to 80,000"],
  why="The other figures are far too small; 60,000 to 80,000 is NCERT's figure for the primary follicles left in "
      "each ovary at puberty, not for sperms.", secs=20)

Z(HR, "Gametogenesis", B, MAT,
  ML(("term", "meaning"),
     ["Spermiogenesis", "Spermiation", "Insemination", "Ovulation"],
     ["Release of semen by the penis into the vagina during copulation",
      "Release of sperms from the seminiferous tubules after their heads were embedded in the Sertoli cells",
      "Release of the ovum (secondary oocyte) from the ovary by rupture of the Graafian follicle",
      "Transformation of spermatids into spermatozoa"]),
  "Terms of gametogenesis and transfer",
  "NCERT: spermatids are transformed into spermatozoa by spermiogenesis; after spermiogenesis, sperm heads become "
  "embedded in the Sertoli cells and are finally released from the seminiferous tubules by spermiation; during "
  "copulation semen is released by the penis into the vagina (insemination); the Graafian follicle ruptures to "
  "release the secondary oocyte by ovulation.",
  ["Spermiogenesis -> IV", "Spermiation -> II", "Insemination -> I", "Ovulation -> III"],
  "Gametogenesis; Fertilisation and Implantation",
  at="B", match=({"A": "IV", "B": "II", "C": "I", "D": "III"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "IV", "B": "I", "C": "II", "D": "III"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
  why="The commonest slip is to exchange spermiogenesis (a transformation) with spermiation (a release); the other "
      "codes mix up the release of semen into the vagina with the release of sperms or of the ovum.", secs=35)

Z(HR, "Fertilisation and implantation", I, NUM,
  "A couple plans to have three children. Using NCERT's statement that in each pregnancy the chance of a male or "
  "a female child is 50 per cent, what is the probability that all three children will be daughters?",
  "Independent pregnancies",
  "In each pregnancy P(daughter) = 1/2, and the pregnancies are independent, so the probability that all three "
  "are daughters is 1/2 × 1/2 × 1/2 = 1/8.",
  ["P(daughter) in one pregnancy = 1/2", "Three independent pregnancies: (1/2)³", "= 1/8"],
  "Fertilisation and Implantation; Class 12 Ch 4 'Principles of Inheritance and Variation', Sex Determination",
  at="A", correct="1/8", wrong=["1/2", "3/8", "1/6"],
  why="1/2 is the chance for a single pregnancy; 3/8 is the chance of exactly one (or exactly two) daughters; 1/6 "
      "comes from dividing by 2 × 3 instead of multiplying the three probabilities.",
  secs=40, vb=RECOMPUTED)

Z(HR, "Male and female reproductive systems", I, D,
  "In a man, both testes fail to descend into the scrotum and remain inside the abdominal cavity, although the "
  "pituitary and the testicular tissue are otherwise normal. Based on NCERT, what is the most likely consequence?",
  "Scrotum and testicular temperature",
  "NCERT: the testes are situated outside the abdominal cavity within a pouch called the scrotum, which helps in "
  "maintaining the low temperature of the testes (2-2.5 °C lower than the normal internal body temperature) "
  "necessary for spermatogenesis. Testes kept at the internal body temperature cannot have this lower "
  "temperature, so spermatogenesis is impaired.",
  ["Spermatogenesis needs a temperature 2-2.5 °C below internal body temperature", "Scrotum provides it; the "
   "abdominal cavity does not", "-> spermatogenesis impaired"],
  "Male Reproductive System",
  at="B", correct="Spermatogenesis is impaired, because the testes are not kept at the lower temperature needed "
                  "for it",
  wrong=["Spermatogenesis increases, because the higher temperature speeds up cell division",
         "Androgen secretion stops completely, because Leydig cells can work only inside the scrotum",
         "Ejaculation becomes impossible, because the vas deferens can open only from the scrotum"],
  why="NCERT says the lower temperature is necessary for spermatogenesis, so a higher temperature does not "
      "improve it; NCERT says nothing about Leydig cells needing the scrotum or about the vas deferens opening "
      "from it.", secs=40)

Z(HR, "Fertilisation and implantation", I, D,
  "The sperms of a man have normal heads and acrosomes, but the mitochondria of their middle pieces are "
  "non-functional. Based on NCERT, why would such sperms be unlikely to fertilise an ovum?",
  "Middle piece and sperm motility",
  "NCERT: the middle piece of the sperm possesses numerous mitochondria, which produce energy for the movement of "
  "the tail that facilitates sperm motility, essential for fertilisation. Without energy from these mitochondria "
  "the tail cannot move the sperm, so it is unlikely to reach the ovum in the ampullary region.",
  ["Middle piece mitochondria -> energy for tail movement", "No energy -> poor motility",
   "Motility is essential for reaching and fertilising the ovum"],
  "Gametogenesis (structure of sperm); Fertilisation and Implantation",
  at="D", correct="The tail would lack energy for movement, so the sperms would have poor motility",
  wrong=["The acrosome would be unable to release its enzymes",
         "The haploid nucleus would become diploid",
         "The sperms would be unable to bind the zona pellucida because the plasma membrane is lost"],
  why="The acrosome is normal in this case and its enzymes are not made by middle-piece mitochondria; nothing "
      "here changes the ploidy of the nucleus; and NCERT links the mitochondria to tail movement, not to the "
      "plasma membrane.", secs=40)

Z(HR, "Fertilisation and implantation", I, D,
  "After insemination, which of the following gives the correct route taken by motile sperms to reach the place "
  "where they meet the ovum?",
  "Route of sperms in the female tract",
  "NCERT: the motile sperms swim rapidly, pass through the cervix, enter into the uterus and finally reach the "
  "junction of the isthmus and ampulla (ampullary-isthmic junction) of the fallopian tube. From the uterus the "
  "first part of the oviduct reached is the isthmus, which joins the uterus.",
  ["Vagina (insemination)", "Cervical canal -> uterus", "Isthmus of the oviduct -> ampullary-isthmic junction"],
  "Fertilisation and Implantation",
  at="C", correct="Vagina → cervical canal → uterus → isthmus → ampullary-isthmic junction of the oviduct",
  wrong=["Vagina → cervical canal → uterus → infundibulum → ampulla of the oviduct",
         "Vagina → uterus → cervical canal → ampulla → isthmus of the oviduct",
         "Vagina → cervical canal → isthmus → uterus → ampullary-isthmic junction of the oviduct"],
  why="The infundibulum is the ovarian end of the oviduct, so sperms reach the ampulla from the isthmus side; the "
      "cervix lies between the vagina and the uterus; and the isthmus is entered only after the uterus.",
  secs=40)

Z(HR, "Pregnancy, parturition and lactation", I, STP,
  SP("By the end of nine months of pregnancy, the foetus is fully developed and is ready for delivery.",
     "Soon after the infant is delivered, the placenta is also expelled out of the uterus."),
  "End of pregnancy",
  "Both are NCERT lines: the foetus is fully developed and ready for delivery by the end of nine months, and soon "
  "after the infant is delivered, the placenta is also expelled out of the uterus.",
  ["Statement I: true", "Statement II: true"],
  "Pregnancy and Embryonic Development; Parturition and Lactation", ans="A",
  why="Both statements are correct NCERT lines, so every option calling either of them false is wrong.", secs=30)

Z(HR, "Pregnancy, parturition and lactation", I, ASR,
  AR("hCG is normally present in the blood of a non-pregnant woman during the luteal phase of her menstrual "
     "cycle.",
     "During pregnancy, the placenta acts as an endocrine tissue and produces several hormones such as hCG, hPL, "
     "estrogens and progestogens."),
  "hCG is a hormone of pregnancy",
  "NCERT: the placenta acts as an endocrine tissue and produces hCG, hPL, estrogens and progestogens, and hCG is "
  "produced in women only during pregnancy. In the luteal phase of a non-pregnant woman, the hormone secreted in "
  "large amounts is progesterone from the corpus luteum, not hCG. So A is false and R is true.",
  ["A: false - hCG is made only during pregnancy", "R: true - placental hormones"],
  "Pregnancy and Embryonic Development", ans="D",
  why="A is false, so the options calling A true are wrong; R is a correct NCERT statement.", secs=35)

Z(HR, "Male and female reproductive systems", I, MUL,
  MS("Which of the following structures of the human male reproductive system are paired?",
     ["Seminal vesicles", "Prostate", "Bulbourethral glands", "Testes", "Urethra"]),
  "Paired and unpaired male organs",
  "NCERT: a pair of testes is present in the scrotum; the male accessory glands include paired seminal vesicles, a "
  "prostate and paired bulbourethral glands. The urethra is a single tube that originates from the urinary bladder "
  "and extends through the penis to the urethral meatus.",
  ["(a) paired seminal vesicles: yes", "(b) a (single) prostate: no", "(c) paired bulbourethral glands: yes",
   "(d) a pair of testes: yes", "(e) single urethra: no"],
  "Male Reproductive System",
  at="C", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"],
  why="NCERT describes 'a prostate', a single gland, and the urethra is single, so any option containing (b) or "
      "(e) is wrong.", secs=40)

Z(HR, "Male and female reproductive systems", I, MAT,
  ML(("cell or gland", "product or role described in NCERT"),
     ["Sertoli cells", "Leydig cells", "Bulbourethral glands", "Cells of the mammary alveoli"],
     ["Secretions that help in the lubrication of the penis", "Milk, which is stored in the cavities of the "
      "alveoli", "Nutrition to the germ cells", "Androgens"]),
  "Secretory cells of the reproductive system",
  "NCERT: Sertoli cells provide nutrition to the germ cells; Leydig (interstitial) cells synthesise and secrete "
  "testicular hormones called androgens; the secretions of the bulbourethral glands help in the lubrication of the "
  "penis; the cells of the mammary alveoli secrete milk, which is stored in the cavities (lumens) of the alveoli.",
  ["Sertoli -> III", "Leydig -> IV", "Bulbourethral -> I", "Alveolar cells -> II"],
  "Male Reproductive System; Female Reproductive System (mammary glands)",
  at="D", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
  why="The wrong codes exchange the two testicular cell types (nutrition vs androgens), give androgen secretion to "
      "the bulbourethral glands, or give lubrication to the mammary alveoli.", secs=40)

MENARCHE, MENOPAUSE, CYCLES_PER_YEAR, PAUSED_YEARS = 13, 50, 13, 2
OVA = (MENOPAUSE - MENARCHE - PAUSED_YEARS) * CYCLES_PER_YEAR
assert OVA == 455
Z(HR, "Menstrual cycle", A, NUM,
  "A woman has her menarche at 13 years and her menopause at 50 years. Assume 13 menstrual cycles in a year and, "
  "following NCERT, that one ovum is released during each menstrual cycle. She has two pregnancies, and for each "
  "pregnancy together with the period of intense lactation after it, assume that no cycles occur for exactly one "
  "year. About how many ova does she release in her lifetime?",
  "Ova released in a lifetime",
  "NCERT: one ovum is released (ovulation) during the middle of each menstrual cycle; cycles run from menarche to "
  "menopause; during pregnancy all events of the menstrual cycle stop, and ovulation does not occur during intense "
  "lactation. Reproductive span = 50 - 13 = 37 years; minus 2 years without cycles = 35 years; 35 × 13 = 455 ova.",
  ["Span: 50 - 13 = 37 years", "Years without cycles: 2 -> 35 years with cycles", "Ova: 35 × 13 = 455"],
  "Menstrual Cycle; Class 12 Ch 3 'Reproductive Health' (lactational amenorrhea)",
  at="A", correct="455", wrong=["481", "910", "507"],
  why="481 ignores the two years without cycles (37 × 13); 910 counts two ova per cycle; 507 adds the two paused years "
      "instead of subtracting them (39 × 13).",
  secs=60, vb=RECOMPUTED)

Z(HR, "Gametogenesis", A, MUL,
  MS("Which of the following statements correctly compare a secondary spermatocyte with a secondary oocyte?",
     ["Both are haploid cells.",
      "Both are formed by the first meiotic division.",
      "Both complete the second meiotic division by dividing into two cells of equal size.",
      "The secondary oocyte is much larger, as it retains the bulk of the nutrient-rich cytoplasm of the primary "
      "oocyte.",
      "Both are formed only before birth, during fetal life."]),
  "Secondary spermatocyte vs secondary oocyte",
  "NCERT: a primary spermatocyte completes the first meiotic division (reduction division) to form two equal, "
  "haploid secondary spermatocytes, which undergo the second meiotic division to produce four equal haploid "
  "spermatids. The primary oocyte within the tertiary follicle completes the first meiotic division, an unequal "
  "division forming a large haploid secondary oocyte (retaining the bulk of the cytoplasm) and a tiny first polar "
  "body. The second meiotic division of the secondary oocyte, induced by sperm entry, gives a large ovum and a tiny "
  "second polar body, so it is also unequal. Both cells form after puberty, not in fetal life.",
  ["(a) true - both haploid", "(b) true - both products of meiosis I", "(c) false - oocyte division unequal",
   "(d) true - secondary oocyte keeps the cytoplasm", "(e) false - formed from puberty onwards"],
  "Gametogenesis; Fertilisation and Implantation",
  at="B", correct="(a), (b) and (d) only",
  wrong=["(a), (b) and (c) only", "(a), (b), (c) and (d) only", "(b), (d) and (e) only"],
  why="(c) is false because the second meiotic division of the secondary oocyte is unequal, and (e) is false "
      "because secondary oocytes form within tertiary follicles and secondary spermatocytes form after puberty.",
  secs=60)

Z(HR, "Menstrual cycle", A, D,
  "A woman has regular 28-day menstrual cycles. A test on one day of her cycle shows a high level of progesterone, "
  "LH and FSH below their peak levels, and a corpus luteum present in one ovary; she is not pregnant. On which day "
  "of her cycle was the test most likely done?",
  "Reading the phase of the cycle",
  "NCERT: in a 28-day cycle, LH and FSH peak in the middle of the cycle (about the 14th day) and induce ovulation. "
  "In the luteal phase that follows, the remaining parts of the Graafian follicle form the corpus luteum, which "
  "secretes large amounts of progesterone. Without fertilisation the corpus luteum degenerates and menstruation "
  "begins a new cycle. A corpus luteum with high progesterone and no LH/FSH peak points to the luteal phase, e.g. "
  "about day 21.",
  ["Corpus luteum + high progesterone -> luteal phase", "LH/FSH not at peak -> not day 14",
   "Luteal phase of a 28-day cycle -> between day 15 and day 28 -> about day 21"],
  "Menstrual Cycle",
  at="B", correct="About day 21",
  wrong=["About day 3", "About day 9", "About day 14"],
  why="Day 3 is the menstrual phase and day 9 the follicular phase, when there is no corpus luteum; day 14 is "
      "the time of the LH and FSH peak and ovulation, before the corpus luteum forms.", secs=50)

Z(HR, "Pregnancy, parturition and lactation", A, D,
  "Suppose that at the end of a pregnancy, the fully developed foetus and the placenta fail to send the signals "
  "that induce mild uterine contractions. Following NCERT's account of parturition, what would be the most likely "
  "result?",
  "Foetal ejection reflex and oxytocin",
  "NCERT: the signals for parturition originate from the fully developed foetus and the placenta, which induce "
  "mild uterine contractions called the foetal ejection reflex. This triggers the release of oxytocin from the "
  "maternal pituitary; oxytocin acts on the uterine muscle and causes stronger contractions, which in turn "
  "stimulate further secretion of oxytocin. Without the reflex, this sequence would not start, so labour would "
  "not be induced normally.",
  ["No foetal/placental signal -> no foetal ejection reflex", "No reflex -> oxytocin release not triggered",
   "No oxytocin -> no stronger contractions -> parturition not induced"],
  "Parturition and Lactation",
  at="A", correct="Oxytocin release from the maternal pituitary would not be triggered, so strong uterine "
                  "contractions and delivery would not be induced normally",
  wrong=["Oxytocin would be released in larger amounts, causing a very rapid delivery",
         "The placenta would release oxytocin directly, so delivery would be unaffected",
         "Milk ejection would start in place of uterine contractions, and delivery would still occur on time"],
  why="NCERT's chain needs the reflex to trigger oxytocin release, so oxytocin would not rise; oxytocin comes from "
      "the maternal pituitary, not the placenta; and nothing in NCERT replaces the uterine contractions with milk "
      "ejection.", secs=50)

Z(HR, "Menstrual cycle", A, ASR,
  AR("There is no menstruation during pregnancy.",
     "The placenta is connected to the embryo through an umbilical cord."),
  "Pregnancy and the menstrual cycle",
  "NCERT: during pregnancy all events of the menstrual cycle stop and there is no menstruation. Separately, NCERT "
  "states that the placenta is connected to the embryo through an umbilical cord, which helps in the transport of "
  "substances to and from the embryo. Both statements are true, but the umbilical cord connection has nothing to "
  "do with why the menstrual cycle stops.",
  ["A: true (NCERT)", "R: true (NCERT)", "R describes the umbilical cord, not the stopping of the cycle -> not "
   "the explanation"],
  "Menstrual Cycle; Pregnancy and Embryonic Development", ans="B",
  why="Both statements are true, so the options with a false statement are wrong; R is a structural fact about the "
      "placenta and does not explain the absence of menstruation.", secs=35)

Z(HR, "Fertilisation and implantation", A, MUL,
  MS("Which of the following take place BEFORE the implantation of the human embryo?",
     ["Mitotic division (cleavage) of the zygote",
      "Transformation of the morula into a blastocyst",
      "Appearance of chorionic villi on the trophoblast",
      "Differentiation of the inner cell mass into an outer ectoderm and an inner endoderm",
      "Formation of an embryo with 8 to 16 blastomeres (morula)"]),
  "Events before implantation",
  "NCERT: cleavage starts as the zygote moves through the isthmus of the oviduct; the embryo with 8 to 16 "
  "blastomeres is the morula, which continues to divide and transforms into the blastocyst as it moves further "
  "into the uterus; the blastocyst then becomes embedded in the endometrium (implantation). After implantation, "
  "finger-like chorionic villi appear on the trophoblast, and immediately after implantation the inner cell mass "
  "differentiates into ectoderm and endoderm.",
  ["(a) cleavage: before", "(b) morula -> blastocyst: before", "(c) chorionic villi: after",
   "(d) ectoderm and endoderm: immediately after", "(e) morula: before"],
  "Fertilisation and Implantation; Pregnancy and Embryonic Development",
  at="D", correct="(a), (b) and (e) only",
  wrong=["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
  why="Chorionic villi (c) and the differentiation of the inner cell mass into ectoderm and endoderm (d) both come "
      "after implantation, so every option containing either is wrong.", secs=55)

Z(HR, "Fertilisation and implantation", A, ASR,
  AR("A blastocyst that fails to become embedded in the endometrium cannot establish a pregnancy.",
     "Implantation normally takes place in the ampullary region of the fallopian tube."),
  "Site of implantation",
  "NCERT: the blastocyst becomes embedded in the endometrium of the uterus; this is called implantation, and it "
  "leads to pregnancy. So A is true. The ampullary region of the fallopian tube is the site of fertilisation, not "
  "of implantation, so R is false.",
  ["A: true - implantation in the endometrium leads to pregnancy", "R: false - ampulla = site of fertilisation; "
   "implantation is in the uterus"],
  "Fertilisation and Implantation", ans="C",
  why="R confuses the site of fertilisation with that of implantation, so it is false; options calling R true are "
      "wrong, and A is correct by NCERT.", secs=40)


# ================================================================ Reproductive Health (5/6/5)
Z(RH, "Contraception", B, D,
  "NCERT notes that India was amongst the first countries in the world to initiate action plans and programmes at "
  "a national level to attain total reproductive health as a social goal. These programmes, called 'family "
  "planning', were initiated in:",
  "Family planning programmes in India",
  "NCERT: the programmes called 'family planning' were initiated in 1951 and were periodically assessed over the "
  "past decades. Improved programmes covering wider reproduction-related areas are currently in operation under "
  "the name 'Reproductive and Child Health Care (RCH) programmes'.",
  ["Family planning programmes: initiated in 1951", "Later broadened into the RCH programmes"],
  "Reproductive Health - Problems and Strategies",
  at="B", correct="1951", wrong=["1971", "1981", "2017"],
  why="1971 is the year of the original MTP Act, 1981 the year AIDS was first reported, and 2017 the year of the "
      "MTP amendment; none is the start of the family planning programmes.", secs=20)

Z(RH, "Contraception", B, STP,
  SP("IUDs increase the phagocytosis of sperms within the uterus.",
     "Lippes loop is a hormone-releasing intra-uterine device."),
  "Intra-uterine devices",
  "NCERT: IUDs increase phagocytosis of sperms within the uterus, and the Cu ions released suppress sperm motility "
  "and the fertilising capacity of sperms. NCERT classifies IUDs as non-medicated IUDs (e.g., Lippes loop), "
  "copper-releasing IUDs (CuT, Cu7, Multiload 375) and hormone-releasing IUDs (Progestasert, LNG-20). So Lippes "
  "loop is non-medicated.",
  ["Statement I: true", "Statement II: false - Lippes loop is a non-medicated IUD"],
  "Birth Control", ans="C",
  why="Statement II misclassifies Lippes loop (non-medicated, not hormone-releasing), so options calling it true "
      "are wrong; Statement I is NCERT's own line.", secs=30)

Z(RH, "Infertility and ART", B, D,
  "Besides the need for extremely high precision handling by specialised professionals and expensive "
  "instrumentation, NCERT says the adoption of assisted reproductive technologies is also deterred by:",
  "Limits on the use of ART",
  "NCERT: ART techniques require extremely high precision handling by specialised professionals and expensive "
  "instrumentation, so they are presently available only in very few centres in the country and are affordable "
  "to only a limited number of people. Emotional, religious and social factors are also deterrents in the "
  "adoption of these methods.",
  ["Cost and expertise limit availability", "Emotional, religious and social factors also deter adoption"],
  "Infertility",
  at="D", correct="Emotional, religious and social factors",
  wrong=["The complete failure of all ART techniques to produce a pregnancy",
         "A legal ban on all ART procedures in India",
         "The fact that ART can be used only for male infertility"],
  why="NCERT presents ART as techniques that do help infertile couples, does not describe them as banned, and "
      "describes ART for female as well as male problems (e.g., GIFT for a woman who cannot produce ova).",
  secs=25)

Z(RH, "Infertility and ART", B, D,
  "Which of the following is NOT one of the assisted reproductive technologies (ART) described in NCERT?",
  "Identifying ART procedures",
  "NCERT's ART include IVF followed by embryo transfer (ZIFT or IUT), GIFT, ICSI, and artificial insemination "
  "(including IUI). Medical termination of pregnancy is the intentional termination of a pregnancy before full "
  "term; it ends a pregnancy rather than helping a couple to have one.",
  ["GIFT, ZIFT, ICSI, AI/IUI: ART", "MTP: termination of pregnancy, not ART"],
  "Infertility; Medical Termination of Pregnancy",
  at="C", correct="Medical termination of pregnancy (MTP)",
  wrong=["Gamete intra fallopian transfer (GIFT)", "Intra cytoplasmic sperm injection (ICSI)",
         "Zygote intra fallopian transfer (ZIFT)"],
  why="GIFT, ICSI and ZIFT are all ART procedures listed in NCERT for infertile couples; only MTP is not an ART.",
  secs=20)

ROUNDS = 4
CELLS = 2 ** ROUNDS
assert CELLS == 16 and CELLS > 8
Z(RH, "Infertility and ART", B, NUM,
  "In an IVF programme, a zygote formed in the laboratory undergoes 4 rounds of cleavage, every blastomere dividing "
  "in each round. According to NCERT's rule for embryo transfer (embryos with up to 8 blastomeres into the "
  "fallopian tube, those with more than 8 blastomeres into the uterus), how many blastomeres does the embryo have "
  "and where should it be transferred?",
  "ZIFT vs IUT by blastomere number",
  "Each round doubles the number of cells: 2⁴ = 16 blastomeres. NCERT: the zygote or early embryos (with up to 8 "
  "blastomeres) are transferred into the fallopian tube (ZIFT), and embryos with more than 8 blastomeres into the "
  "uterus (IUT). 16 is more than 8, so the embryo goes into the uterus by IUT.",
  ["Blastomeres = 2⁴ = 16", "16 > 8", "-> intra uterine transfer (IUT)"],
  "Infertility",
  at="D", correct="16 blastomeres; into the uterus (IUT)",
  wrong=["8 blastomeres; into the fallopian tube (ZIFT)", "16 blastomeres; into the fallopian tube (ZIFT)",
         "4 blastomeres; into the fallopian tube (ZIFT)"],
  why="8 counts only three rounds and 4 counts two rounds (or multiplies 4 rounds by 1); 16 blastomeres is more than "
      "8, so ZIFT is not the right transfer for it.", secs=35, vb=RECOMPUTED)

Z(RH, "Contraception", I, MUL,
  MS("Which of the following contraceptive methods are adopted by the male partner?",
     ["Condoms such as 'Nirodh'", "Vasectomy", "Coitus interruptus (withdrawal)", "Saheli", "Tubectomy"]),
  "Male contraceptive methods",
  "NCERT: condoms (e.g., the popular brand 'Nirodh' for males) cover the penis; in vasectomy a small part of the vas "
  "deferens is removed or tied up through a small incision on the scrotum; in coitus interruptus the male partner "
  "withdraws his penis from the vagina just before ejaculation. Saheli is an oral pill for females, and tubectomy "
  "is the sterilisation procedure for females (fallopian tube).",
  ["(a) male condom: yes", "(b) vasectomy (vas deferens): yes", "(c) withdrawal by the male: yes",
   "(d) Saheli: female pill", "(e) tubectomy: female sterilisation"],
  "Birth Control",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(b), (c) and (e) only", "(a), (b) and (d) only"],
  why="'(a) and (b) only' leaves out coitus interruptus, in which the male partner withdraws; Saheli (d) and "
      "tubectomy (e) are methods for females.", secs=40)

Z(RH, "Contraception", I, ASR,
  AR("Tubectomy prevents conception.",
     "Saheli, a once-a-week pill, contains a non-steroidal preparation."),
  "Two unrelated facts on contraception",
  "NCERT: in tubectomy a small part of the fallopian tube is removed or tied up through a small incision in the "
  "abdomen or through the vagina, which blocks gamete transport and prevents conception. NCERT also describes "
  "Saheli as a 'once a week' pill containing a non-steroidal preparation. Both are true, but the composition of an "
  "oral pill has nothing to do with how tubectomy works.",
  ["A: true - tubectomy blocks gamete transport", "R: true - Saheli is non-steroidal", "R is about a different "
   "method -> not the explanation"],
  "Birth Control", ans="B",
  why="Both statements are true, so options with a false statement are wrong; R concerns a pill, so it cannot "
      "explain how a surgical method prevents conception.", secs=30)

Z(RH, "Infertility and ART", I, STP,
  SP("In both ZIFT and IUT, fertilisation takes place outside the body of the woman.",
     "In GIFT, an ovum is transferred into the fallopian tube, so that fertilisation can take place within the "
     "female body."),
  "Where fertilisation occurs in ART",
  "NCERT: in IVF, ova and sperms are induced to form a zygote under simulated conditions in the laboratory; the "
  "zygote or early embryo is then transferred into the fallopian tube (ZIFT) or the embryo into the uterus (IUT), "
  "so fertilisation in both is in vitro. In GIFT, an ovum collected from a donor is transferred into the fallopian "
  "tube of a female who cannot produce one but can provide suitable conditions for fertilisation and further "
  "development, so fertilisation occurs in vivo.",
  ["Statement I: true - ZIFT and IUT follow IVF", "Statement II: true - GIFT gives in vivo fertilisation"],
  "Infertility", ans="A",
  why="Both statements are correct, so every option calling either of them false is wrong.", secs=35)

Z(RH, "MTP and amniocentesis", I, MAT,
  ML(("term", "NCERT description"),
     ["Infertility", "Medical termination of pregnancy", "Amniocentesis", "Emergency contraception"],
     ["Intentional or voluntary termination of pregnancy before full term",
      "Use of pills, IUDs or progestogens within 72 hours of coitus",
      "Inability to produce children in spite of unprotected sexual co-habitation",
      "Foetal sex determination test based on the chromosomal pattern in the amniotic fluid"]),
  "Terms of reproductive health",
  "NCERT: couples unable to produce children in spite of unprotected sexual co-habitation are infertile; MTP or "
  "induced abortion is the intentional or voluntary termination of pregnancy before full term; amniocentesis is a "
  "foetal sex determination test based on the chromosomal pattern in the amniotic fluid surrounding the "
  "developing embryo; progestogens, progestogen-estrogen combinations or IUDs used within 72 hours of coitus are "
  "effective emergency contraceptives.",
  ["Infertility -> III", "MTP -> I", "Amniocentesis -> IV", "Emergency contraception -> II"],
  "Medical Termination of Pregnancy; Infertility; Amniocentesis; Birth Control",
  at="B", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"}]),
  why="The wrong codes exchange infertility with MTP, exchange MTP with emergency contraception (which acts within "
      "72 hours of coitus, before any pregnancy is established), or exchange amniocentesis with emergency "
      "contraception.", secs=40)

Z(RH, "STDs and their prevention", I, D,
  "How many of the following sexually transmitted infections does NCERT describe as completely curable if detected "
  "early and treated properly?\n\nGonorrhoea, genital herpes, syphilis, hepatitis-B, chlamydiasis, HIV infection, "
  "trichomoniasis",
  "Curable and non-curable STIs",
  "NCERT: except for hepatitis-B, genital herpes and HIV infections, other diseases (STIs) are completely curable if "
  "detected early and treated properly. In the list, gonorrhoea, syphilis, chlamydiasis and trichomoniasis are "
  "curable: four.",
  ["Not completely curable: genital herpes, hepatitis-B, HIV", "Curable: gonorrhoea, syphilis, chlamydiasis, "
   "trichomoniasis", "Count = 4"],
  "Sexually Transmitted Infections (STIs)",
  at="D", correct="Four", wrong=["Three", "Five", "Seven"],
  why="Three leaves out one curable STI; five counts one of hepatitis-B, genital herpes or HIV as curable; seven "
      "treats all STIs as curable, ignoring NCERT's three exceptions.", secs=40)

Z(RH, "Contraception", I, ASR,
  AR("Condoms, diaphragms, cervical caps and vaults can prevent conception.",
     "These barrier methods prevent the ovum and sperms from physically meeting."),
  "How barrier methods work",
  "NCERT: in barrier methods, the ovum and sperms are prevented from physically meeting with the help of barriers; "
  "condoms prevent the ejaculated semen from entering the female reproductive tract, and diaphragms, cervical caps "
  "and vaults cover the cervix during coitus and block the entry of sperms through the cervix. Preventing the "
  "gametes from meeting is exactly why conception is prevented, so R explains A.",
  ["A: true", "R: true - barrier stops gametes from meeting", "No meeting -> no fertilisation -> R explains A"],
  "Birth Control", ans="A",
  why="R is the mechanism by which barrier methods prevent conception, so 'R is not the correct explanation' is "
      "wrong, and neither statement is false.", secs=30)

Z(RH, "Contraception", A, MUL,
  MS("In which of the following methods can conception be prevented even though ovulation occurs and semen is "
     "deposited in the vagina?",
     ["Copper-releasing IUD", "Tubectomy", "Hormone-releasing IUD", "Oral contraceptive pills", "Condom"]),
  "Where each method acts",
  "NCERT: copper-releasing IUDs increase phagocytosis of sperms in the uterus and Cu ions suppress sperm motility "
  "and fertilising capacity; tubectomy blocks gamete transport in the fallopian tube; hormone-releasing IUDs make "
  "the uterus unsuitable for implantation and the cervix hostile to sperms. All three act after insemination and "
  "without stopping ovulation. Oral pills act by inhibiting ovulation (and implantation), so ovulation would not "
  "occur, and a condom prevents the ejaculated semen from entering the female reproductive tract.",
  ["(a) acts on sperms in the uterus: yes", "(b) blocks the fallopian tube: yes", "(c) uterus unsuitable, cervix "
   "hostile: yes", "(d) pills inhibit ovulation: no", "(e) condom stops semen entering: no"],
  "Birth Control",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a) and (c) only", "(a), (c) and (d) only", "(b), (d) and (e) only"],
  why="'(a) and (c) only' misses tubectomy, which works with normal ovulation and insemination; pills (d) inhibit "
      "ovulation and condoms (e) stop semen reaching the vagina, so they break the stem's conditions.", secs=55)

Z(RH, "Infertility and ART", A, D,
  "A woman cannot produce ova, but her fallopian tubes and uterus are normal. Her husband has a very low sperm "
  "count, though some of his sperms are normal. Which of the following combinations of NCERT techniques could help "
  "this couple have a child who is the husband's biological offspring?",
  "Combining ART procedures",
  "The woman needs a donor ovum. Since the husband's sperm count is very low, fertilisation is best done in the "
  "laboratory by injecting one of his sperms directly into the ovum (ICSI). The early embryo (up to 8 blastomeres) "
  "can then be transferred into her normal fallopian tube (ZIFT). IUI alone cannot work without an ovum, and GIFT "
  "would still depend on natural insemination with the very low sperm count.",
  ["No ova -> donor ovum needed", "Very low sperm count -> ICSI in the laboratory", "Early embryo -> her fallopian "
   "tube (ZIFT)"],
  "Infertility",
  at="A", correct="ICSI using a donor ovum and the husband's sperm, followed by transfer of the early embryo into "
                  "her fallopian tube (ZIFT)",
  wrong=["Intra-uterine insemination (IUI) with the husband's semen alone",
         "IVF using her own ova, followed by intra uterine transfer (IUT)",
         "GIFT of a donor ovum, relying on natural insemination by the husband"],
  why="IUI alone supplies no ovum; she cannot produce ova, so her own ova cannot be used; GIFT here would depend on "
      "natural insemination, which NCERT's AI/ICSI exist to overcome when sperm counts are very low.", secs=60)

Z(RH, "Contraception", A, MAT,
  ML(("couple's situation", "method best suited, following NCERT"),
     ["They have completed their family and want no more pregnancies",
      "The woman wants to delay her next pregnancy and space her children",
      "Unprotected coitus took place the previous night",
      "They also want protection from STIs and AIDS"],
     ["Condoms", "Sterilisation (vasectomy or tubectomy)", "Emergency contraception (within 72 hours)",
      "Intra-uterine device"]),
  "Choosing a contraceptive",
  "NCERT: surgical methods (sterilisation) are generally advised to the male/female partner as a terminal method to "
  "prevent any more pregnancies; IUDs are ideal contraceptives for females who want to delay pregnancy and/or space "
  "children; pills, IUDs or progestogens used within 72 hours of coitus are effective emergency contraceptives; "
  "condoms also protect the user from STIs and AIDS.",
  ["No more children -> II", "Spacing -> IV", "Coitus last night -> III", "STI protection -> I"],
  "Birth Control",
  at="D", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="Sterilisation is terminal and so does not suit spacing; condoms, not emergency methods, give STI protection; "
      "and an IUD is the NCERT choice for spacing, while emergency contraception suits coitus already over.",
  secs=50)

Z(RH, "MTP and amniocentesis", A, ASR,
  AR("Amniocentesis is legally permitted in India for finding out the sex of a foetus.",
     "Amniocentesis is based on the chromosomal pattern in the amniotic fluid surrounding the developing embryo."),
  "Amniocentesis and its misuse",
  "NCERT: amniocentesis is a foetal sex determination test based on the chromosomal pattern in the amniotic fluid "
  "surrounding the developing embryo, so R is true. NCERT also states that there is a statutory ban on "
  "amniocentesis for sex determination, to legally check increasing female foeticide, so A is false.",
  ["A: false - statutory ban on its use for sex determination", "R: true - basis of the test"],
  "Reproductive Health - Problems and Strategies; Amniocentesis", ans="D",
  why="A contradicts NCERT's statement on the statutory ban, so options calling A true are wrong; R is NCERT's "
      "description of the test.", secs=35)

Z(RH, "MTP and amniocentesis", A, STP,
  SP("MTPs are much safer in the second trimester than in the first trimester.",
     "A majority of the MTPs are performed illegally by unqualified quacks, which are not only unsafe but could "
     "be fatal too."),
  "Safety of MTP",
  "NCERT: MTPs are considered relatively safe during the first trimester (up to 12 weeks); second-trimester "
  "abortions are much more risky. NCERT also points out a dangerous trend: a majority of MTPs are performed "
  "illegally by unqualified quacks, which are not only unsafe but could be fatal too.",
  ["Statement I: false - the first trimester is the safer period", "Statement II: true (NCERT)"],
  "Medical Termination of Pregnancy", ans="D",
  why="Statement I reverses NCERT's comparison of the two trimesters, so options calling it true are wrong; "
      "Statement II is NCERT's own warning.", secs=35)


# ================================================================ Evolution (6/8/6)
Z(EVO, "Origin of life", B, D,
  "How does NCERT describe the origin of life in relation to the history of the universe?",
  "Origin of life",
  "NCERT opens its account of the origin of life by stating that the origin of life is considered a unique event in "
  "the history of the universe.",
  ["NCERT: origin of life = a unique event in the history of the universe"],
  "Origin of Life",
  at="B", correct="As a unique event in the history of the universe",
  wrong=["As an event that is repeated every few million years on earth",
         "As an event that took place only about 4000 years ago",
         "As an event that happened before the formation of galaxies"],
  why="NCERT does not describe life as arising repeatedly; 4000 years is the age of the earth according to the "
      "theory of special creation, which NCERT does not accept; and life appeared on earth long after galaxies "
      "existed.", secs=20)

Z(EVO, "Evidences of evolution", B, D,
  "Ernst Haeckel based his embryological support for evolution on certain features common to the embryos of all "
  "vertebrates, including humans. Which observation did he use?",
  "Embryological evidence (Haeckel)",
  "NCERT: embryological support for evolution was proposed by Ernst Haeckel based upon the observation of certain "
  "features during the embryonic stage common to all vertebrates that are absent in the adult. For example, the "
  "embryos of all vertebrates including humans develop a row of vestigial gill slits just behind the head, but it "
  "is a functional organ only in fish and not in any other adult vertebrates. (Karl Ernst von Baer later "
  "disapproved the proposal.)",
  ["Feature: row of vestigial gill slits behind the head in all vertebrate embryos", "Functional only in adult "
   "fish", "Absent as functional organs in other adult vertebrates"],
  "Evidences for Evolution",
  at="D", correct="A row of vestigial gill slits just behind the head, functional only in fish among adult "
                  "vertebrates",
  wrong=["Functional gill slits present in adult humans",
         "Identical forelimb bones in whales, bats, cheetahs and humans",
         "Similar proteins and genes performing a given function in diverse organisms"],
  why="The gill slits are not functional in adult humans; forelimb bones are comparative-anatomy evidence and "
      "similar proteins and genes are biochemical evidence, not Haeckel's embryological evidence.", secs=30)

Z(EVO, "Natural selection", B, D,
  "In England, collections of moths from the same area were compared before and after industrialisation. In the "
  "collection that showed more dark-winged (melanised) moths than white-winged moths, NCERT gives the year of "
  "collection as:",
  "Industrial melanism: the two collections",
  "NCERT: in collections of moths made in the 1850s, before industrialisation set in, there were more white-winged "
  "moths on trees than dark-winged or melanised moths. In the collection carried out from the same area after "
  "industrialisation, in 1920, there were more dark-winged moths.",
  ["1850s collection: more white-winged moths", "1920 collection (after industrialisation): more dark-winged "
   "moths"],
  "Evolution by Natural Selection (industrial melanism)",
  at="D", correct="1920", wrong=["The 1850s", "1859", "1938"],
  why="The 1850s collection, before industrialisation, had more white-winged moths; 1859 is not NCERT's date for "
      "either collection; 1938 is the year NCERT gives for the coelacanth caught in South Africa.", secs=25)

Z(EVO, "Evidences of evolution", B, STP,
  SP("Fossils are remains of hard parts of life-forms found in rocks.",
     "A cross-section of the earth's crust indicates the arrangement of sediments one over the other during the "
     "long history of the earth."),
  "Fossils and sedimentary layers",
  "Both are NCERT lines from the palaeontological evidence. Rocks form sediments, and a cross-section of the "
  "earth's crust indicates the arrangement of sediments one over the other during the long history of the earth; "
  "different-aged rock sediments contain different life-forms.",
  ["Statement I: true", "Statement II: true"],
  "Evidences for Evolution", ans="A",
  why="Both statements are correct NCERT lines, so every option calling either of them false is wrong.", secs=30)

P_, Q_ = F(45, 100), F(35, 100)
R_ = 1 - P_ - Q_
assert R_ == F(1, 5)
Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "A gene has three alleles, A, a¹ and a², in a population. The frequency of A is 0.45 and that of a¹ is 0.35. "
  "Using the Hardy-Weinberg principle that the sum total of all the allelic frequencies is 1, what is the "
  "frequency of a²?",
  "Sum of allele frequencies",
  "NCERT: the sum total of all the allelic frequencies is 1. So f(a²) = 1 - (0.45 + 0.35) = 1 - 0.80 = 0.20.",
  ["Sum of all allele frequencies = 1", "f(a²) = 1 - 0.45 - 0.35", "= 0.20"],
  "Hardy-Weinberg Principle",
  at="B", correct="0.20", wrong=["0.80", "0.10", "0.04"],
  why="0.80 is the sum of the two given frequencies, not the remainder; 0.10 is the difference between them; 0.04 "
      "squares the answer as if it were a genotype frequency.", secs=25, vb=RECOMPUTED)

Z(EVO, "Evidences of evolution", B, ASR,
  AR("The wings of a butterfly and the wings of a bird are analogous structures.",
     "The wings of a butterfly and of a bird have the same anatomical structure."),
  "Analogous structures",
  "NCERT: analogous structures are not anatomically similar structures, though they perform similar functions; "
  "the wings of butterfly and of birds are its example, the result of convergent evolution. So A is true and R, "
  "which claims the same anatomy, is false.",
  ["A: true - NCERT's example of analogy", "R: false - analogous structures are not anatomically similar"],
  "Evidences for Evolution", ans="C",
  why="R contradicts the definition of analogous structures, so options calling R true are wrong; A is NCERT's own "
      "example.", secs=30)

N1, P1, N2, P2 = 900, F(6, 10), 100, F(2, 10)
P_MIX = (N1 * P1 + N2 * P2) / (N1 + N2)
assert P_MIX == F(56, 100)
Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, NUM,
  "A population of 900 individuals has a frequency of allele A of 0.6. A group of 100 individuals of the same "
  "species, in which the frequency of A is 0.2, migrates into it and the two groups interbreed freely. Assuming "
  "each individual carries two copies of the gene, what is the frequency of A in the combined population?",
  "Gene flow changes allele frequencies",
  "NCERT: when a section of a population migrates to another place and population, gene frequencies change in the "
  "original as well as in the new population (gene flow). Copies of A: 900 × 2 × 0.6 = 1080 and 100 × 2 × 0.2 = 40, "
  "total 1120 out of 2000 copies, so p = 1120/2000 = 0.56.",
  ["Copies of A: 1800 × 0.6 = 1080; 200 × 0.2 = 40", "Total copies = 2000", "p = 1120/2000 = 0.56"],
  "Hardy-Weinberg Principle",
  at="C", correct="0.56", wrong=["0.40", "0.60", "0.80"],
  why="0.40 is the simple average of 0.6 and 0.2, ignoring the sizes of the groups; 0.60 ignores the migrants; 0.80 "
      "adds the two frequencies.", secs=60, vb=RECOMPUTED)

Z(EVO, "Natural selection", I, ASR,
  AR("After industrialisation, dark-winged moths came to outnumber white-winged moths in the industrial areas of "
     "England.",
     "Industrial smoke and soot darkened the tree trunks, so white-winged moths resting on them were picked out by "
     "predators, while dark-winged moths escaped."),
  "Industrial melanism",
  "NCERT: during post-industrialisation the tree trunks became dark due to industrial smoke and soots; under this "
  "condition the white-winged moths did not survive due to predators, while dark-winged or melanised moths "
  "survived. Before industrialisation, white lichens on the trunks gave white moths the advantage. Selective "
  "predation against moths that do not match the background is the cause of the change in proportions, so R "
  "explains A.",
  ["A: true (1920 collection)", "R: true - dark trunks, white moths conspicuous to predators",
   "Differential survival -> more dark moths -> R explains A"],
  "Evolution by Natural Selection (industrial melanism)", ans="A",
  why="R gives the selective cause NCERT states for A, so 'R is not the correct explanation' is wrong; neither "
      "statement is false.", secs=40)

Z(EVO, "Human evolution", I, STP,
  SP("Homo habilis, with a brain capacity of 650-800 cc, probably did not eat meat.",
     "Homo erectus, with a large brain of around 900 cc, probably ate meat."),
  "Brain size and diet of early Homo",
  "NCERT: the brain capacities of Homo habilis were between 650-800 cc and they probably did not eat meat. Fossils "
  "discovered in Java in 1891 revealed the next stage, Homo erectus, about 1.5 mya; Homo erectus had a large brain "
  "around 900 cc and probably ate meat.",
  ["Statement I: true (NCERT)", "Statement II: true (NCERT)"],
  "Origin and Evolution of Man", ans="A",
  why="Both statements are NCERT's own descriptions, so every option calling either false is wrong.", secs=30)

Z(EVO, "Origin of life", I, MAT,
  ML(("idea about the origin of life", "its main claim, as described in NCERT"),
     ["Theory of special creation", "Panspermia", "Spontaneous generation", "Chemical evolution (Oparin and "
      "Haldane)"],
     ["Life came out of decaying and rotting matter like straw and mud",
      "The first form of life could have come from pre-existing non-living organic molecules (e.g., RNA, protein)",
      "Units of life called spores were transferred to different planets including the earth",
      "All living organisms that we see today were created as such, and the earth is about 4000 years old"]),
  "Theories of the origin of life",
  "NCERT: the theory of special creation holds that all species were created as such, that diversity was always the "
  "same, and that the earth is about 4000 years old; according to panspermia, units of life called spores were "
  "transferred to different planets including the earth; spontaneous generation held that life came out of "
  "decaying and rotting matter; Oparin and Haldane proposed that the first form of life could have come from "
  "pre-existing non-living organic molecules, i.e., that life was preceded by chemical evolution.",
  ["Special creation -> IV", "Panspermia -> III", "Spontaneous generation -> I", "Chemical evolution -> II"],
  "Origin of Life; Evolution of Life Forms - A Theory",
  at="C", match=({"A": "IV", "B": "III", "C": "I", "D": "II"},
                 [{"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "IV", "B": "I", "C": "III", "D": "II"}]),
  why="The wrong codes exchange special creation with panspermia, exchange spontaneous generation (decaying matter) "
      "with chemical evolution (organic molecules), or give 'spores from other planets' to spontaneous generation.",
  secs=45)

Z(EVO, "Natural selection", I, MUL,
  MS("Which of the following does NCERT give as examples of evolution by anthropogenic action, i.e. changes brought "
     "about by human activity that took place in a much shorter time scale than usual?",
     ["Selection of herbicide-resistant varieties after excess use of herbicides",
      "Selection of pesticide-resistant varieties after excess use of pesticides",
      "Microbes becoming resistant to the antibiotics or drugs used against them",
      "Darwin's finches with altered beaks arising from a seed-eating form",
      "Radiation of a number of different marsupials in Australia"]),
  "Evolution by anthropogenic action",
  "NCERT: excess use of herbicides, pesticides, etc., has only resulted in selection of resistant varieties in a "
  "much lesser time scale; this is also true for microbes against which we employ antibiotics or drugs against "
  "eukaryotic organisms/cell, and resistant organisms/cells appear in a time scale of months or years and not "
  "centuries. These are examples of evolution by anthropogenic action. Darwin's finches and Australian "
  "marsupials are examples of adaptive radiation, not of human-caused change.",
  ["(a), (b), (c): human use of chemicals selects resistant forms", "(d), (e): natural adaptive radiation"],
  "Evolution by Natural Selection",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"],
  why="'(a) and (b) only' leaves out antibiotic resistance, which NCERT names explicitly; Darwin's finches (d) and "
      "the marsupials (e) are cases of adaptive radiation, not anthropogenic action.", secs=45)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", I, D,
  "Two neighbouring populations of the same species start exchanging individuals frequently, and the migrants "
  "interbreed in their new population. According to NCERT, which statement about this is correct?",
  "Gene flow",
  "NCERT: when a section of a population migrates to another place and population, gene frequencies change in the "
  "original as well as in the new population: new genes/alleles are added to the new population and these are "
  "lost from the old population. If this gene migration happens multiple times, there is gene flow, one of the "
  "factors that affect Hardy-Weinberg equilibrium.",
  ["Migration adds alleles to one population and removes them from the other", "Repeated migration = gene flow",
   "Gene flow disturbs Hardy-Weinberg equilibrium"],
  "Hardy-Weinberg Principle",
  at="B", correct="Gene flow occurs, changing the allele frequencies of both populations, so Hardy-Weinberg "
                  "equilibrium is disturbed",
  wrong=["The allele frequencies stay constant, because no new alleles are formed by mutation",
         "Only the population receiving migrants changes; the population losing them keeps its allele frequencies",
         "This is the founder effect, since the migrants found a new species"],
  why="Gene flow changes allele frequencies without any mutation; NCERT says frequencies change in both the "
      "original and the new population; and the founder effect concerns a drifted population founding a new "
      "population, not repeated exchange between existing ones.", secs=40)

Z(EVO, "Darwinism and modern synthesis", I, D,
  "Giraffes have long necks. Which of the following explanations is in line with Darwin's theory of natural "
  "selection rather than with Lamarck's idea?",
  "Darwin vs Lamarck",
  "Lamarck said evolution of life forms was driven by the use and disuse of organs, e.g., giraffes elongating their "
  "necks by stretching to forage leaves and passing on this acquired character. Darwin's natural selection works "
  "on heritable variation already present: individuals with variations that make them better fit leave more "
  "progeny, so those variations become more common over generations.",
  ["Lamarck: acquired by use, then inherited", "Darwin: pre-existing heritable variation + differential "
   "reproduction", "Longer-necked variants leave more progeny -> long necks become common"],
  "Evolution by Natural Selection; Mechanism of Evolution",
  at="B", correct="Giraffes varied in neck length; those with heritably longer necks survived and left more "
                  "progeny, so long necks became common over generations",
  wrong=["Giraffes stretched their necks to reach leaves, and the stretched necks were passed on to the offspring",
         "The long neck arose suddenly in a single step in one generation and was not affected by selection",
         "Short-necked giraffes deliberately chose to grow longer necks to compete for food"],
  why="Stretching and passing on the result is Lamarck's use-and-disuse idea; a single large step without "
      "selection resembles saltation, not Darwin's gradual natural selection; and organisms do not choose their "
      "variations.", secs=40)

Z(EVO, "Human evolution", I, MUL,
  MS("Which of the following features does NCERT describe for Neanderthal man?",
     ["Brain size of about 1400 cc", "Lived in near east and central Asian countries between 1,00,000-40,000 years "
      "back", "Used hides to protect their body", "Buried their dead", "Fossils discovered in Java in 1891"]),
  "Neanderthal man",
  "NCERT: Neanderthal man, with a brain size of 1400 cc, lived in near east and central Asian countries between "
  "1,00,000-40,000 years back. They used hides to protect their body and buried their dead. The fossils "
  "discovered in Java in 1891 were of Homo erectus.",
  ["(a) 1400 cc: yes", "(b) near east and central Asia: yes", "(c) hides: yes", "(d) burial: yes",
   "(e) Java 1891: Homo erectus"],
  "Origin and Evolution of Man",
  at="D", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"],
  why="(e) belongs to Homo erectus, so options with (e) are wrong, and '(b), (c) and (d) only' leaves out the "
      "1400 cc brain, which NCERT gives for Neanderthal man.", secs=45)

N_POP, N_AA = 2500, 400
Q_HW = F(2, 5)
assert Q_HW ** 2 == F(N_AA, N_POP)
HET = 2 * (1 - Q_HW) * Q_HW * N_POP
assert HET == 1200 and (1 - Q_HW) ** 2 * N_POP == 900
Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "A population of 2,500 individuals is in Hardy-Weinberg equilibrium for a gene with two alleles, A (dominant) and "
  "a (recessive). 400 individuals show the recessive phenotype (aa). How many individuals are expected to be "
  "heterozygous (Aa)?",
  "Heterozygote number from the recessive phenotype",
  "q² = 400/2500 = 0.16, so q = 0.4 and p = 1 - 0.4 = 0.6. The frequency of heterozygotes is 2pq = 2 × 0.6 × 0.4 = "
  "0.48, so the expected number is 0.48 × 2500 = 1200. (Check: AA = 0.36 × 2500 = 900; 900 + 1200 + 400 = 2500.)",
  ["q² = 400/2500 = 0.16 -> q = 0.4", "p = 0.6", "2pq = 0.48 -> 0.48 × 2500 = 1200"],
  "Hardy-Weinberg Principle",
  at="D", correct="1200", wrong=["900", "1500", "672"],
  why="900 is the expected number of AA individuals (p² × 2500); 1500 is p × 2500, an allele frequency used as if it "
      "were a genotype frequency; 672 uses q² = 0.16 as if it were q (2 × 0.84 × 0.16 × 2500).",
  secs=75, vb=RECOMPUTED)

P_7 = F(55, 100)
Q_3 = 1 - P_7
assert Q_3 == F(45, 100) and P_7 ** 2 == F(3025, 10000) and 2 * P_7 * Q_3 == F(495, 1000) and Q_3 ** 2 == F(2025, 10000)
assert P_7 ** 2 + Q_3 ** 2 != 1
Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, MUL,
  MS("A population is in Hardy-Weinberg equilibrium for a gene with two alleles, A and a, and the frequency of "
     "allele A (p) is 0.55. Which of the following statements are correct?",
     ["The frequency of allele a (q) is 0.45.",
      "The frequency of the AA genotype is 0.3025.",
      "The frequency of the Aa genotype is 0.495.",
      "The frequency of the aa genotype is 0.2025.",
      "The frequencies of the two homozygous genotypes add up to 1."]),
  "Applying p² + 2pq + q² = 1",
  "The sum total of the allele frequencies is 1, so q = 1 - 0.55 = 0.45. From the binomial expansion p² + 2pq + q² = "
  "1: AA = p² = 0.3025, Aa = 2pq = 2 × 0.55 × 0.45 = 0.495, aa = q² = 0.2025. The two homozygotes together are 0.3025 + "
  "0.2025 = 0.505, not 1, because the heterozygotes (0.495) make up the rest.",
  ["(a) q = 0.45: true", "(b) p² = 0.3025: true", "(c) 2pq = 0.495: true", "(d) q² = 0.2025: true",
   "(e) p² + q² = 0.505: false"],
  "Hardy-Weinberg Principle",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (b), (c), (d) and (e)"],
  why="(e) is false because p² + q² = 0.505; it is p² + 2pq + q² that equals 1. '(b), (c) and (d) only' leaves out "
      "the correct value of q.", secs=60, vb=RECOMPUTED)

Z(EVO, "Origin of life", A, D,
  "Louis Pasteur showed, with killed yeast, that life comes only from pre-existing life. Which result of his "
  "experiment would instead have SUPPORTED the theory of spontaneous generation?",
  "Logic of Pasteur's experiment",
  "NCERT: Pasteur demonstrated that in pre-sterilised flasks, life did not come from killed yeast, while in another "
  "flask open to air, new living organisms arose from killed yeast. If living organisms had appeared even in the "
  "pre-sterilised (closed) flasks, where no living things could enter from outside, life would have arisen from "
  "non-living matter, which is what spontaneous generation claims.",
  ["Spontaneous generation: life from non-living matter", "Test: a flask that no living thing can enter",
   "Life appearing there would have supported it"],
  "Origin of Life",
  at="B", correct="New living organisms appearing from killed yeast in the pre-sterilised flasks",
  wrong=["New living organisms appearing from killed yeast in the flask open to air",
         "No living organisms appearing in either flask",
         "No living organisms appearing in the pre-sterilised flasks"],
  why="Organisms in the open flask can come from the air, so they show nothing about spontaneous generation; no "
      "life in the sterilised flasks is exactly what Pasteur found, which disproved the theory; and no life in "
      "either flask also gives no evidence for it.", secs=60)

Z(EVO, "Adaptive radiation", A, ASR,
  AR("Darwin's finches of the Galapagos Islands are an example of adaptive radiation.",
     "Hugo de Vries proposed the idea of mutations based on his work on the evening primrose."),
  "Two independent facts",
  "NCERT: from the original seed-eating finches, many other forms with altered beaks arose, enabling them to become "
  "insectivorous and vegetarian finches; this process of evolution of different species in a geographical area "
  "starting from a point is adaptive radiation. Separately, de Vries proposed mutations based on work on evening "
  "primrose. Both are true, but de Vries's work does not explain the finches' radiation.",
  ["A: true", "R: true", "R concerns a different scientist and organism -> not the explanation"],
  "Adaptive Radiation; Mechanism of Evolution", ans="B",
  why="Both statements are true, so options with a false statement are wrong; R says nothing about the finches, "
      "so it does not explain A.", secs=35)

QA, QB = F(1, 2), F(1, 10)
assert 2 * (1 - QA) * QA == F(1, 2) > QA ** 2 and 2 * (1 - QA) * QA > (1 - QA) ** 2
assert 2 * (1 - QB) * QB == F(18, 100)
Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, STP,
  SP("In a population in Hardy-Weinberg equilibrium in which the two alleles of a gene are equally frequent (p = q "
     "= 0.5), heterozygotes are the most common genotype.",
     "In a population in Hardy-Weinberg equilibrium in which the frequency of the recessive allele is 0.1, about "
     "18 per cent of the individuals are heterozygous carriers."),
  "Using p² + 2pq + q² = 1",
  "Statement I: with p = q = 0.5, AA = 0.25, Aa = 2 × 0.5 × 0.5 = 0.5, aa = 0.25, so heterozygotes (50 per cent) "
  "are the most common. Statement II: with q = 0.1 and p = 0.9, 2pq = 2 × 0.9 × 0.1 = 0.18, i.e. 18 per cent.",
  ["I: p² = 0.25, 2pq = 0.50, q² = 0.25 -> true", "II: 2pq = 2(0.9)(0.1) = 0.18 -> true"],
  "Hardy-Weinberg Principle", ans="A",
  why="Both computations come out as stated, so every option calling either statement false is wrong.",
  secs=60, vb=RECOMPUTED)

Z(EVO, "Adaptive radiation", A, D,
  "A single ancestral species of lizard colonises a group of isolated islands. Over a long time, many species arise "
  "from it, each adapted to a different habitat and food on the islands. Following NCERT, this pattern is best "
  "described as:",
  "Recognising adaptive radiation",
  "NCERT: the process of evolution of different species in a given geographical area starting from a point and "
  "literally radiating to other areas of geography (habitats) is called adaptive radiation (e.g., Darwin's "
  "finches, Australian marsupials). Here many species arise from one ancestral stock and spread into different "
  "habitats, which is adaptive radiation.",
  ["One ancestral stock", "Many species, each in a different habitat", "-> adaptive radiation"],
  "Adaptive Radiation",
  at="C", correct="Adaptive radiation",
  wrong=["Convergent evolution between unrelated lineages",
         "Industrial melanism",
         "Saltation by a single large mutation"],
  why="Convergent evolution concerns different lineages coming to resemble each other, whereas here all species "
      "come from one ancestor; industrial melanism is a change in moth colour proportions; and saltation is de "
      "Vries's single-step change, not radiation into many habitats.", secs=45)


# ================================================================ Human Health and Disease (7/8/7)
Z(HHD, "Drug and alcohol abuse", B, D,
  "According to NCERT, tobacco has been used by human beings for more than:",
  "History of tobacco use",
  "NCERT: tobacco has been used by human beings for more than 400 years. It is smoked, chewed or used as a snuff.",
  ["NCERT figure: more than 400 years"],
  "Drugs and Alcohol Abuse",
  at="B", correct="400 years", wrong=["40 years", "4000 years", "40,000 years"],
  why="The other figures are not NCERT's; 4000 years is the age of the earth claimed by the theory of special "
      "creation, and 40 years is far too short.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "The 'good humor' hypothesis of health, according to which health was a state of body and mind where there was a "
  "balance of certain 'humors', was held by:",
  "Early ideas about health",
  "NCERT: the 'good humor' hypothesis of health was held by early Greeks like Hippocrates as well as by the Indian "
  "Ayurveda system of medicine. It was disproved by William Harvey's discovery of blood circulation and by the "
  "demonstration of normal body temperature in persons with 'black bile' using a thermometer.",
  ["Held by: early Greeks such as Hippocrates", "Also: the Indian Ayurveda system of medicine",
   "Disproved partly by William Harvey"],
  "Common Diseases in Humans (introduction)",
  at="D", correct="Early Greeks like Hippocrates, as well as the Indian Ayurveda system of medicine",
  wrong=["William Harvey, who discovered blood circulation",
         "Louis Pasteur, who showed that life comes from pre-existing life",
         "Mary Mallon, the typhoid carrier"],
  why="William Harvey's discovery helped to disprove the hypothesis; Pasteur's work concerned spontaneous "
      "generation; and Mary Mallon was a typhoid carrier, not a proponent of any theory of health.", secs=25)

Z(HHD, "Pathogens and diseases", B, MAT,
  ML(("pathogen", "kind of organism"),
     ["Haemophilus influenzae", "Microsporum", "Wuchereria malayi", "Rhinovirus"],
     ["Helminth", "Virus", "Bacterium", "Fungus"]),
  "Kinds of pathogens",
  "NCERT: Haemophilus influenzae, along with Streptococcus pneumoniae, is a bacterium responsible for pneumonia; "
  "Microsporum (with Trichophyton and Epidermophyton) is a fungus causing ringworm; Wuchereria (W. bancrofti and "
  "W. malayi) is a filarial worm (helminth) causing filariasis; rhinoviruses are viruses causing the common cold.",
  ["H. influenzae -> III (bacterium)", "Microsporum -> IV (fungus)", "W. malayi -> I (helminth)",
   "Rhinovirus -> II (virus)"],
  "Common Diseases in Humans",
  at="A", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="Haemophilus 'influenzae' is a bacterium, not a virus, despite its name; Microsporum is a fungus and "
      "Wuchereria a worm, not the other way round; and the last code exchanges the bacterium with the fungus.",
  secs=35)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Cocaine, obtained from the coca plant Erythroxylum coca, is commonly called coke or crack. According to NCERT, it "
  "is usually:",
  "Mode of intake of cocaine",
  "NCERT: cocaine, commonly called coke or crack, is usually snorted. It has a potent stimulating action on the "
  "central nervous system, producing a sense of euphoria and increased energy.",
  ["Cocaine = coke or crack", "Usual mode of intake: snorting"],
  "Drugs and Alcohol Abuse",
  at="C", correct="Snorted", wrong=["Chewed as leaves", "Applied on the skin", "Taken only as a tablet"],
  why="NCERT names snorting as the usual mode for cocaine; chewing is mentioned for tobacco, and NCERT does not "
      "describe cocaine as applied on the skin or taken only as tablets.", secs=20)

Z(HHD, "HIV and AIDS", B, STP,
  SP("Anti-retroviral drugs are only partially effective in AIDS: they can prolong the life of the patient but "
     "cannot prevent death.",
     "Since there is no cure for AIDS, prevention is the best option."),
  "Treatment and prevention of AIDS",
  "Both are NCERT statements. Treatment of AIDS with anti-retroviral drugs is only partially effective; the drugs "
  "can only prolong the life of the patient but cannot prevent death. Since there is no cure for AIDS, prevention "
  "is the best option.",
  ["Statement I: true", "Statement II: true"],
  "AIDS", ans="A",
  why="Both statements are NCERT's own lines, so every option calling either of them false is wrong.", secs=30)

Z(HHD, "Cancer", B, D,
  "In the detection of cancer by biopsy, a piece of the suspected tissue is cut into thin sections, stained and "
  "examined under a microscope. According to NCERT, this examination (histopathological study) is done by a:",
  "Biopsy",
  "NCERT: in biopsy, a piece of the suspected tissue cut into thin sections is stained and examined under a "
  "microscope (histopathological studies) by a pathologist.",
  ["Thin stained sections of suspected tissue", "Examined under a microscope by a pathologist"],
  "Cancer (detection and diagnosis)",
  at="B", correct="Pathologist",
  wrong=["Radiologist, using X-rays", "Surgeon, without a microscope", "Pharmacist"],
  why="X-ray based methods (radiography, CT) are separate imaging techniques; NCERT says the sections are examined "
      "under a microscope by a pathologist, not by a surgeon or pharmacist.", secs=20)

Z(HHD, "Immunity and vaccines", B, ASR,
  AR("Innate immunity is a specific type of defence that develops only after exposure to a particular pathogen.",
     "Innate immunity is present at the time of birth."),
  "Innate immunity",
  "NCERT: innate immunity is a non-specific type of defence that is present at the time of birth; it is "
  "accomplished by providing different types of barriers to the entry of foreign agents. Acquired immunity, "
  "by contrast, is pathogen-specific and develops after exposure. So A is false and R is true.",
  ["A: false - innate immunity is non-specific and present from birth", "R: true"],
  "Immunity", ans="D",
  why="A describes acquired, not innate, immunity, so options calling A true are wrong; R is NCERT's own line.",
  secs=30)

Z(HHD, "Pathogens and diseases", I, ASR,
  AR("Houseflies can help to spread amoebiasis.",
     "Houseflies act as mechanical carriers and transmit the parasite from the faeces of an infected person to food "
     "and food products, thereby contaminating them."),
  "Spread of amoebiasis",
  "NCERT: Entamoeba histolytica causes amoebic dysentery (amoebiasis); houseflies act as mechanical carriers and "
  "serve to transmit the parasite from the faeces of infected persons to food and food products, thereby "
  "contaminating them; drinking water and food contaminated by faecal matter are the main source of infection. R "
  "is the way houseflies spread the disease, so it explains A.",
  ["A: true", "R: true - mechanical carriers from faeces to food", "Contaminated food -> infection -> R explains "
   "A"],
  "Common Diseases in Humans", ans="A",
  why="R states the exact route by which houseflies spread amoebiasis, so 'R is not the correct explanation' is "
      "wrong; both statements are true.", secs=35)

Z(HHD, "HIV and AIDS", I, STP,
  SP("After HIV enters a macrophage, its RNA genome is replicated to form viral DNA with the help of the enzyme "
     "reverse transcriptase.",
     "Once HIV starts infecting helper T-lymphocytes, the infected macrophages stop producing virus particles."),
  "Role of macrophages in HIV infection",
  "NCERT: after getting into the body, the virus enters macrophages, where its RNA genome is replicated to form viral "
  "DNA with the help of reverse transcriptase; the viral DNA gets incorporated into the host cell's DNA and directs "
  "the infected cells to produce virus particles. The macrophages continue to produce virus and in this way act "
  "like an HIV factory. Simultaneously, HIV enters helper T-lymphocytes.",
  ["Statement I: true", "Statement II: false - macrophages continue producing virus (HIV factory)"],
  "AIDS", ans="C",
  why="NCERT says macrophages continue to produce the virus, so Statement II is false and options calling it true "
      "are wrong; Statement I is correct.", secs=35)

Z(HHD, "Cancer", I, MAT,
  ML(("technique used for cancer detection", "its basis, as described in NCERT"),
     ["Radiography", "Computed tomography (CT)", "Magnetic resonance imaging (MRI)", "Biopsy"],
     ["Strong magnetic fields and non-ionising radiations detect pathological and physiological changes in "
      "living tissue",
      "Thin stained sections of the suspected tissue are examined under a microscope",
      "Use of X-rays",
      "X-rays are used to generate a three-dimensional image of the internals of an object"]),
  "Techniques for detecting cancer",
  "NCERT: techniques like radiography (use of X-rays), CT (computed tomography) and MRI (magnetic resonance imaging) "
  "are very useful to detect cancers of the internal organs. CT uses X-rays to generate a three-dimensional image of "
  "the internals of an object; MRI uses strong magnetic fields and non-ionising radiations to accurately detect "
  "pathological and physiological changes in living tissue. Biopsy involves stained thin sections of tissue "
  "examined under a microscope.",
  ["Radiography -> III", "CT -> IV", "MRI -> I", "Biopsy -> II"],
  "Cancer (detection and diagnosis)",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="Radiography uses X-rays but CT is the one that builds a three-dimensional image; MRI does not use X-rays; "
      "and microscopy of stained sections is biopsy, not radiography.", secs=45)

Z(HHD, "Cancer", I, D,
  "A biopsy shows that a tumour's cells are invading and damaging the surrounding normal tissue, and secondary "
  "tumours of the same cells are found in a distant organ. Based on NCERT, which description fits this tumour?",
  "Benign vs malignant tumours",
  "NCERT: benign tumours normally remain confined to their original location and do not spread to other parts of the "
  "body. Malignant tumours are a mass of proliferating cells (neoplastic or tumour cells) that grow very rapidly, "
  "invade and damage the surrounding normal tissues; cells sloughed from such tumours reach distant sites through "
  "blood and start new tumours there. This property, metastasis, is the most feared property of malignant "
  "tumours.",
  ["Invasion of nearby tissue -> malignant", "Secondary tumours at a distant site -> metastasis",
   "Benign tumours stay confined"],
  "Cancer",
  at="A", correct="A malignant tumour showing metastasis",
  wrong=["A benign tumour, since it is confined to its original location",
         "A benign tumour showing metastasis",
         "A collection of normal cells showing contact inhibition"],
  why="Benign tumours stay confined and do not spread, so neither benign option fits; cells that continue to "
      "divide and invade have lost, not kept, contact inhibition.", secs=40)

Z(HHD, "Pathogens and diseases", I, MUL,
  MS("Which of the following human diseases are transmitted through the bite of mosquitoes, according to NCERT?",
     ["Malaria", "Filariasis", "Dengue", "Chikungunya", "Typhoid"]),
  "Mosquito-borne diseases",
  "NCERT: malaria (Plasmodium) is transmitted by the bite of an infected female Anopheles mosquito; filarial worms "
  "are transmitted to a healthy person through the bite of female mosquito vectors; the Aedes mosquitoes are the "
  "vectors of dengue and chikungunya. Typhoid spreads through food and water contaminated with Salmonella typhi.",
  ["(a) malaria: Anopheles", "(b) filariasis: female mosquito vectors", "(c), (d) dengue, chikungunya: Aedes",
   "(e) typhoid: contaminated food and water"],
  "Common Diseases in Humans",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a) and (b) only", "(a), (c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="'(a) and (b) only' leaves out dengue and chikungunya, spread by Aedes; any option with typhoid is wrong, "
      "since typhoid spreads through contaminated food and water.", secs=40)

Z(HHD, "Drug and alcohol abuse", I, ASR,
  AR("Cocaine has a potent stimulating action on the central nervous system, producing a sense of euphoria and "
     "increased energy.",
     "Cocaine is obtained from the coca plant Erythroxylum coca, native to South America."),
  "Cocaine: action vs source",
  "Both are NCERT statements. Cocaine interferes with the transport of the neurotransmitter dopamine and has a "
  "potent stimulating action on the CNS. That it comes from a South American plant is a fact about its source; it "
  "does not explain why it stimulates the nervous system.",
  ["A: true", "R: true", "R gives the plant source, not the mechanism -> not the explanation"],
  "Drugs and Alcohol Abuse", ans="B",
  why="Both statements are true, so options with a false statement are wrong; R is about where cocaine comes from, "
      "not about how it acts.", secs=30)

Z(HHD, "Cancer", I, D,
  "According to NCERT, which of the following can cause DNA damage leading to neoplastic transformation even though "
  "it is a NON-ionising radiation?",
  "Physical carcinogens",
  "NCERT: ionising radiations like X-rays and gamma rays and non-ionising radiations like UV cause DNA damage leading "
  "to neoplastic transformation. Of these, UV is the non-ionising one.",
  ["Ionising carcinogens: X-rays, gamma rays", "Non-ionising carcinogen named by NCERT: UV"],
  "Cancer (causes of cancer)",
  at="C", correct="UV radiation", wrong=["X-rays", "Gamma rays", "Tobacco smoke"],
  why="X-rays and gamma rays are carcinogens but are ionising radiations; tobacco smoke is a chemical carcinogen, "
      "not a radiation.", secs=25)

Z(HHD, "Immunity and vaccines", I, MAT,
  ML(("lymphoid organ", "NCERT description"),
     ["Bone marrow", "Thymus", "Spleen", "Lymph nodes"],
     ["Lobular organ near the heart, beneath the breastbone; quite large at birth and reduces in size with age",
      "Small solid structures located at different points along the lymphatic system that trap antigens in lymph "
      "and tissue fluid",
      "Main lymphoid organ, where all blood cells including lymphocytes are produced",
      "Large bean-shaped organ that filters the blood and is a large reservoir of erythrocytes"]),
  "Lymphoid organs",
  "NCERT: the bone marrow is the main lymphoid organ where all blood cells including lymphocytes are produced; the "
  "thymus is a lobular organ located near the heart and beneath the breastbone, quite large at birth but reducing "
  "in size with age; the spleen is a large bean-shaped organ that acts as a filter of the blood and has a large "
  "reservoir of erythrocytes; lymph nodes are small solid structures located at different points along the "
  "lymphatic system that trap micro-organisms or other antigens in the lymph and tissue fluid.",
  ["Bone marrow -> III", "Thymus -> I", "Spleen -> IV", "Lymph nodes -> II"],
  "Immunity (lymphoid organs)",
  at="D", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="The wrong codes exchange the bone marrow with the thymus, the spleen (filters blood) with the lymph nodes "
      "(trap antigens in lymph), or the thymus with the spleen.", secs=45)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("A woman who has been vaccinated against tetanus gives birth. Her baby receives antibodies against the "
     "tetanus toxin through the placenta. Which of the following statements are correct?",
     ["At birth, the baby has passive immunity against tetanus.",
      "The baby's own memory B and T-cells against tetanus have been generated by these antibodies.",
      "The antibodies were produced by the mother's immune system, not by the baby's.",
      "Vaccinating the baby later will give it active immunity against tetanus.",
      "The protection the baby has at birth is a form of innate immunity."]),
  "Passive and active immunity",
  "NCERT: when ready-made antibodies are directly given, it is called passive immunity; the foetus receives some "
  "antibodies from the mother through the placenta during pregnancy, an example of passive immunity. Preformed "
  "antibodies do not make the receiver produce its own antibodies or memory cells. Active immunity results when the "
  "host is exposed to antigens (as in vaccination) and produces its own antibodies, generating memory B and "
  "T-cells. Innate immunity is non-specific; antibodies against one toxin are part of acquired immunity.",
  ["(a) true - ready-made antibodies", "(b) false - no memory cells from passive transfer", "(c) true",
   "(d) true - vaccination = active immunity", "(e) false - antibodies are acquired, specific defence"],
  "Immunity (active and passive immunity; vaccination)",
  at="A", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"],
  why="(b) is false because only exposure to antigens, not receiving antibodies, generates memory cells; (e) is "
      "false because specific antibodies belong to acquired immunity, not to innate, non-specific defence.",
  secs=55)

Z(HHD, "Pathogens and diseases", A, D,
  "A town faces outbreaks of malaria, dengue and typhoid. Which single measure from NCERT's list would help to "
  "control malaria and dengue but would NOT, by itself, prevent typhoid?",
  "Matching control measures to modes of spread",
  "Malaria and dengue are spread by mosquitoes (Anopheles and Aedes), so NCERT's vector-control measures - avoiding "
  "stagnation of water in and around homes, regular cleaning of household coolers, use of mosquito nets, "
  "introducing fishes like Gambusia that feed on mosquito larvae, spraying of insecticides - help against both. "
  "Typhoid spreads through food and water contaminated with Salmonella typhi, so controlling mosquitoes does not "
  "prevent it; clean drinking water and food do.",
  ["Malaria, dengue: mosquito vectors", "Typhoid: contaminated food and water", "Mosquito control -> first two "
   "only"],
  "Common Diseases in Humans; Prevention and Control of Diseases",
  at="D", correct="Avoiding stagnation of water around homes and regularly cleaning household coolers",
  wrong=["Consuming only clean drinking water and food",
         "Proper disposal of human excreta",
         "Observing standard practices of hygiene in public catering"],
  why="Clean water and food, disposal of excreta and hygiene in catering are measures against diseases spread "
      "through contaminated food and water such as typhoid, and they do little against mosquito breeding.",
  secs=50)

Z(HHD, "HIV and AIDS", A, ASR,
  AR("In an AIDS patient, the production of antibodies against new infections becomes weak.",
     "HIV progressively increases the number of helper T-lymphocytes in the infected person."),
  "Helper T-cells, antibodies and HIV",
  "NCERT: T-cells themselves do not secrete antibodies but help B-cells produce them. In HIV infection the number "
  "of helper T-lymphocytes progressively DECREASES, and the person becomes unable to produce a proper immune "
  "response, including antibody production. So A is true, but R reverses the change in helper T-cells and is false.",
  ["A: true - fewer helper T-cells -> less help to B-cells", "R: false - helper T-cell number decreases"],
  "AIDS; Immunity", ans="C",
  why="R states an increase where NCERT describes a progressive decrease, so options calling R true are wrong; A is "
      "true.", secs=40)

Z(HHD, "Immunity and vaccines", A, MAT,
  ML(("defect in a person", "defence that is most directly impaired"),
     ["No functional B-lymphocytes", "No functional T-lymphocytes", "No mast cells",
      "Virus-infected cells cannot secrete interferons"],
     ["Protection of non-infected cells from further viral infection",
      "Release of histamine and serotonin in allergic reactions",
      "Humoral immune response (antibodies in the blood)",
      "Cell-mediated immunity, such as graft rejection"]),
  "Matching defects to defence components",
  "NCERT: B-lymphocytes produce the antibodies of the humoral immune response; T-lymphocytes mediate cell-mediated "
  "immunity, which is responsible for graft rejection; allergic symptoms are due to chemicals like histamine and "
  "serotonin released from mast cells; virus-infected cells secrete interferons, which protect non-infected cells "
  "from further viral infection.",
  ["No B-cells -> III", "No T-cells -> IV", "No mast cells -> II", "No interferons -> I"],
  "Immunity",
  at="B", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="The wrong codes exchange the humoral (B-cell) and cell-mediated (T-cell) responses, exchange mast cells with "
      "interferons, or give the allergic reaction to T-cells.", secs=50)

Z(HHD, "Immunity and vaccines", A, D,
  "How many of the following are SECONDARY lymphoid organs, according to NCERT?\n\nSpleen, thymus, tonsils, bone "
  "marrow, Peyer's patches of the small intestine, appendix, lymph nodes",
  "Primary and secondary lymphoid organs",
  "NCERT: the primary lymphoid organs are the bone marrow and the thymus, where immature lymphocytes differentiate "
  "into antigen-sensitive lymphocytes. The secondary lymphoid organs are the spleen, lymph nodes, tonsils, Peyer's "
  "patches of the small intestine and the appendix. From the list: spleen, tonsils, Peyer's patches, appendix and "
  "lymph nodes = 5.",
  ["Primary: thymus, bone marrow (2)", "Secondary: spleen, tonsils, Peyer's patches, appendix, lymph nodes",
   "Count = 5"],
  "Immunity (lymphoid organs)",
  at="C", correct="Five", wrong=["Four", "Six", "Seven"],
  why="Four leaves out the appendix (or another secondary organ); six counts the thymus or bone marrow as "
      "secondary; seven counts every organ, ignoring that the thymus and bone marrow are primary.", secs=40)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("A person who has been vaccinated against a pathogen usually does not suffer from the disease on later "
     "exposure to that pathogen.",
     "Vaccination generates memory B and T-cells that recognise the pathogen quickly on subsequent exposure and "
     "overwhelm the invaders with a massive production of antibodies."),
  "Principle of vaccination",
  "NCERT: the principle of immunisation or vaccination is based on the property of memory of the immune system. "
  "Vaccines generate memory B and T-cells that recognise the pathogen quickly on subsequent exposure and overwhelm "
  "the invaders with a massive production of antibodies. That is exactly why the vaccinated person is protected, "
  "so R explains A.",
  ["A: true", "R: true - memory cells, quick and massive response", "Quick response neutralises the pathogen -> R "
   "explains A"],
  "Vaccination and Immunisation", ans="A",
  why="R is the mechanism of protection by vaccines, so 'R is not the correct explanation' is wrong; neither "
      "statement is false.", secs=35)

Z(HHD, "Pathogens and diseases", A, MUL,
  MS("Which of the following diseases are acquired mainly by taking in food or water contaminated with the "
     "pathogen or its eggs?",
     ["Typhoid", "Amoebiasis", "Ascariasis", "Pneumonia", "Ringworm"]),
  "Diseases spread through contaminated food and water",
  "NCERT: Salmonella typhi generally enters the small intestine through food and water contaminated with it; "
  "drinking water and food contaminated by faecal matter are the main source of Entamoeba infection (amoebiasis); "
  "a healthy person acquires Ascaris infection through water, vegetables, fruits, etc., contaminated with its "
  "eggs. Pneumonia spreads by inhaling droplets/aerosols released by an infected person, and ringworms are "
  "acquired from soil or by using towels, clothes or combs of infected individuals.",
  ["(a) typhoid: food and water", "(b) amoebiasis: food and water contaminated by faeces", "(c) ascariasis: eggs "
   "in water, vegetables, fruits", "(d) pneumonia: droplets", "(e) ringworm: soil, towels, combs"],
  "Common Diseases in Humans",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (c) and (d) only", "(b), (c) and (e) only"],
  why="'(a) and (b) only' leaves out ascariasis, whose eggs are taken in with contaminated food and water; "
      "pneumonia (droplets) and ringworm (soil, towels, combs) are acquired in other ways.", secs=45)


# ================================================================ Biotechnology: Principles and Processes (6/7/6)
Z(BPP, "Restriction enzymes", B, D,
  "Hind II, the first restriction endonuclease whose functioning depended on a specific DNA nucleotide sequence, "
  "always cuts DNA molecules at a particular point by recognising a specific sequence of:",
  "Recognition sequence of Hind II",
  "NCERT: the first restriction endonuclease, Hind II, was found to always cut DNA molecules at a particular point "
  "by recognising a specific sequence of six base pairs. This specific base sequence is known as the recognition "
  "sequence for Hind II.",
  ["Hind II: recognition sequence of six base pairs", "Cuts at a particular point within that sequence"],
  "Restriction Enzymes",
  at="D", correct="Six base pairs", wrong=["Four base pairs", "Two base pairs", "Twelve base pairs"],
  why="NCERT gives six base pairs for Hind II; the other numbers are not NCERT's figure for this enzyme.",
  secs=20)

Z(BPP, "Cloning vectors", B, D,
  "In the E. coli cloning vector pBR322 shown in NCERT, the recognition sites for PstI and PvuI lie within which "
  "gene?",
  "Restriction sites in pBR322",
  "NCERT's map of pBR322 shows the antibiotic resistance genes ampR and tetR, the ori and the rop gene, with "
  "restriction sites for Hind III, EcoRI, BamHI, SalI, PvuII, PstI, PvuI and ClaI. BamHI and SalI lie within the "
  "tetracycline resistance gene, while PstI and PvuI lie within the ampicillin resistance gene.",
  ["BamHI, SalI -> tetR", "PstI, PvuI -> ampR"],
  "Cloning Vectors",
  at="C", correct="The ampicillin resistance gene (ampR)",
  wrong=["The tetracycline resistance gene (tetR)", "The rop gene", "The origin of replication (ori)"],
  why="tetR carries the BamHI and SalI sites; rop codes for proteins involved in replication and ori is where "
      "replication starts; neither holds the PstI and PvuI sites in NCERT's map.", secs=25)

Z(BPP, "PCR and gel electrophoresis", B, ASR,
  AR("The progression of a restriction enzyme digestion can be checked by agarose gel electrophoresis.",
     "In agarose gel electrophoresis, smaller DNA fragments move more slowly than larger ones."),
  "Gel electrophoresis",
  "NCERT: you can check the progression of a restriction enzyme digestion by agarose gel electrophoresis. The DNA "
  "fragments separate according to their size through the sieving effect provided by the agarose gel; hence, the "
  "smaller the fragment size, the farther it moves. So A is true and R, which reverses this, is false.",
  ["A: true (NCERT)", "R: false - smaller fragments move farther (faster)"],
  "Processes of Recombinant DNA Technology (Cutting of DNA; separation of DNA fragments)", ans="C",
  why="R reverses the relation between fragment size and distance moved, so options calling R true are wrong; A is "
      "NCERT's own line.", secs=30)

Z(BPP, "Competent hosts and transformation", B, D,
  "Which of the following is NOT a method for introducing recombinant DNA into host cells?",
  "Methods of introducing DNA",
  "NCERT: recombinant DNA can be introduced into host cells by making bacteria competent (calcium treatment and heat "
  "shock), by micro-injection into the nucleus of an animal cell, by biolistics (gene gun) for plants, and by "
  "'disarmed pathogen' vectors. Elution is the extraction of separated DNA bands cut out from an agarose gel.",
  ["Micro-injection, biolistics, disarmed pathogens, competence: DNA transfer methods",
   "Elution: recovering DNA from a gel piece"],
  "Competent Host (for transformation with recombinant DNA)",
  at="D", correct="Elution",
  wrong=["Micro-injection", "Biolistics (gene gun)", "Use of a 'disarmed pathogen' vector"],
  why="Micro-injection, biolistics and disarmed pathogen vectors are all NCERT's methods of introducing alien DNA "
      "into host cells; elution only recovers DNA from a gel.", secs=20)

Z(BPP, "Bioreactors and downstream processing", B, D,
  "A bioreactor provides the optimal conditions for achieving the desired product. Which of the following is NOT "
  "among the conditions NCERT lists?",
  "Optimal conditions in a bioreactor",
  "NCERT: a bioreactor provides the optimal conditions for achieving the desired product by providing optimum "
  "growth conditions - temperature, pH, substrate, salts, vitamins and oxygen. Light intensity is not in this list.",
  ["NCERT list: temperature, pH, substrate, salts, vitamins, oxygen", "Light intensity: not listed"],
  "Processes of Recombinant DNA Technology (Obtaining the foreign gene product)",
  at="B", correct="Light intensity", wrong=["pH", "Oxygen", "Vitamins"],
  why="pH, oxygen and vitamins are all among NCERT's optimum growth conditions provided in a bioreactor.", secs=20)

TOTAL, BLUE = 300, 240
WHITE = TOTAL - BLUE
assert WHITE == 60 and F(WHITE, TOTAL) == F(1, 5)
Z(BPP, "Cloning vectors", B, NUM,
  "Foreign DNA is inserted within the coding sequence of β-galactosidase in a vector that also carries an "
  "ampicillin resistance gene, and E. coli is transformed. On a plate containing ampicillin and a chromogenic "
  "substrate, 300 colonies grow, of which 240 are blue. How many of the colonies carry recombinant DNA?",
  "Counting recombinants by colour",
  "Only transformants grow on ampicillin. NCERT: the presence of a chromogenic substrate gives blue coloured "
  "colonies if the plasmid in the bacteria does not have an insert; in the presence of an insert, the "
  "β-galactosidase gene is inactivated (insertional inactivation) and the colonies do not produce any colour. So "
  "recombinants = 300 - 240 = 60.",
  ["All 300 colonies are transformants", "Blue = no insert (240)", "Colourless = recombinants: 300 - 240 = 60"],
  "Cloning Vectors (insertional inactivation)",
  at="A", correct="60", wrong=["240", "300", "180"],
  why="240 counts the blue colonies, which carry the vector without the insert; 300 counts every transformant; "
      "180 subtracts the recombinants twice (240 - 60).", secs=35, vb=RECOMPUTED)

Z(BPP, "Restriction enzymes", I, D,
  "A plasmid vector is cut with EcoRI and a gene of interest is cut out with BamHI. Following NCERT, what is the "
  "problem in joining them with DNA ligase?",
  "Same enzyme, same sticky ends",
  "NCERT: when cut by the same restriction enzyme, the resultant DNA fragments have the same kind of 'sticky ends', "
  "and these can be joined together (end-to-end) using DNA ligases. Normally, the vector and the source DNA are "
  "therefore cut with the same restriction enzyme. Ends made by two different enzymes such as EcoRI and BamHI are "
  "not the same kind of sticky ends.",
  ["Joining needs complementary sticky ends", "Same enzyme -> same kind of sticky ends", "EcoRI ends and BamHI "
   "ends differ -> cannot be joined directly"],
  "Processes of Recombinant DNA Technology (Insertion of the gene into a vector)",
  at="A", correct="The two DNAs do not have the same kind of sticky ends, so they cannot pair and be joined as "
                  "they are",
  wrong=["DNA ligase can join only DNA fragments that have no sticky ends",
         "BamHI produces fragments that cannot be separated on an agarose gel",
         "EcoRI destroys the origin of replication of every vector it cuts"],
  why="NCERT describes ligase joining fragments with matching sticky ends; BamHI fragments separate on gels like "
      "any others; and EcoRI does not destroy the ori of every vector (vectors are chosen with single, suitable "
      "sites).", secs=40)

Z(BPP, "Competent hosts and transformation", I, MUL,
  MS("Which of the following steps does NCERT describe for making E. coli cells take up a recombinant plasmid?",
     ["Treating the cells with a specific concentration of a divalent cation such as calcium",
      "Incubating the cells with the recombinant DNA on ice",
      "Placing them briefly at 42 °C (heat shock)",
      "Putting them back on ice",
      "Treating them with lysozyme first to break open the cells"]),
  "Making bacteria competent",
  "NCERT: since DNA is hydrophilic, bacterial cells are made 'competent' by treating them with a specific "
  "concentration of a divalent cation such as calcium, which increases the efficiency with which DNA enters the "
  "bacterium through pores in its cell wall. The cells are incubated with recombinant DNA on ice, then placed "
  "briefly at 42 °C (heat shock), and then put back on ice. Lysozyme is used to break open bacterial cells when "
  "DNA is to be isolated, which would kill the host.",
  ["(a), (b), (c), (d): the competence and heat-shock procedure", "(e) lysozyme lyses cells - used for DNA "
   "isolation"],
  "Competent Host (for transformation with recombinant DNA)",
  at="B", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (c) and (e) only", "(a), (b), (c), (d) and (e)", "(b), (c) and (d) only"],
  why="Lysozyme breaks open bacterial cells during DNA isolation and has no place in transformation, so options "
      "with (e) are wrong; '(b), (c) and (d) only' leaves out the calcium treatment that makes the cells "
      "competent.", secs=45)

Z(BPP, "PCR and gel electrophoresis", I, MUL,
  MS("Which of the following must be added to the reaction for amplifying a gene by PCR, as described in NCERT?",
     ["The DNA (template) containing the gene", "Two sets of primers", "A thermostable DNA polymerase",
      "Nucleotides (deoxynucleotides)", "A restriction enzyme and DNA ligase"]),
  "Ingredients of a PCR",
  "NCERT: in PCR, multiple copies of the gene (or DNA) of interest are synthesised in vitro using two sets of "
  "primers and the enzyme DNA polymerase. The enzyme extends the primers using the nucleotides provided in the "
  "reaction and the genomic DNA as template. A thermostable DNA polymerase (from Thermus aquaticus) is used. "
  "Restriction enzymes and ligase are not part of the amplification itself.",
  ["(a) template: yes", "(b) two sets of primers: yes", "(c) thermostable polymerase: yes",
   "(d) nucleotides: yes", "(e) restriction enzyme and ligase: no"],
  "Processes of Recombinant DNA Technology (Amplification of gene of interest using PCR)",
  at="C", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (b), (c), (d) and (e)"],
  why="'(a), (b) and (c) only' forgets the nucleotides from which the new strands are built; PCR amplification "
      "does not use a restriction enzyme or DNA ligase, so options with (e) are wrong.", secs=40)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("Chitinase is used to break open plant cells during the isolation of DNA.",
     "Cellulase is used to break open plant cells during the isolation of DNA."),
  "Enzymes for isolating DNA",
  "NCERT: in order to release DNA along with other macromolecules, the cell is broken open by treating it with "
  "enzymes such as lysozyme (bacteria), cellulase (plant cells) and chitinase (fungus). So A is false and R is "
  "true.",
  ["Lysozyme -> bacteria", "Cellulase -> plant cells (R true)", "Chitinase -> fungi (A false)"],
  "Processes of Recombinant DNA Technology (Isolation of the genetic material)", ans="D",
  why="Chitinase is NCERT's enzyme for fungal cells, so A is false and options calling it true are wrong; R is "
      "correct.", secs=30)

Z(BPP, "Cloning vectors", I, MAT,
  ML(("feature of a plasmid used as a cloning vector", "consequence"),
     ["It lacks an origin of replication",
      "It lacks a selectable marker",
      "It has several recognition sites for the restriction enzyme to be used",
      "The foreign DNA is inserted within its β-galactosidase gene"],
     ["Colonies carrying the recombinant DNA give no colour with a chromogenic substrate",
      "The plasmid is cut into several fragments, which complicates gene cloning",
      "Transformants cannot be identified and separated from non-transformants",
      "The plasmid, with any linked DNA, is not replicated in the host"]),
  "Features of cloning vectors",
  "NCERT: ori is the sequence from where replication starts, and any piece of DNA linked to it can replicate within "
  "the host cells; a selectable marker helps in identifying and eliminating non-transformants; the presence of more "
  "than one recognition site within the vector will generate several fragments, which will complicate gene "
  "cloning; insertion of foreign DNA within the β-galactosidase gene inactivates it, so recombinant colonies do "
  "not produce colour with a chromogenic substrate.",
  ["No ori -> IV", "No marker -> III", "Several sites -> II", "Insert in β-gal -> I"],
  "Cloning Vectors",
  at="D", match=({"A": "IV", "B": "III", "C": "II", "D": "I"},
                 [{"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
  why="The wrong codes exchange the roles of ori (replication) and the marker (selection), confuse the marker with "
      "the restriction sites, or give the colour result to multiple sites.", secs=45)

Z(BPP, "PCR and gel electrophoresis", I, STP,
  SP("In agarose gel electrophoresis, DNA fragments separate according to their size through the sieving effect "
     "provided by the agarose gel.",
     "The separated DNA bands are cut out from the gel, and the DNA extracted from them is used in constructing "
     "recombinant DNA by joining it with cloning vectors."),
  "Gel electrophoresis and elution",
  "Both are NCERT statements. Fragments separate by size through the sieving effect of the agarose gel; the "
  "separated bands are cut out and extracted from the gel piece (elution), and the purified DNA fragments are used "
  "in constructing recombinant DNA by joining them with cloning vectors.",
  ["Statement I: true", "Statement II: true"],
  "Processes of Recombinant DNA Technology (separation and isolation of DNA fragments)", ans="A",
  why="Both statements are NCERT's own, so every option calling either of them false is wrong.", secs=30)

Z(BPP, "Bioreactors and downstream processing", I, D,
  "A recombinant protein to be used as a drug has been produced in a bioreactor. Which of the following gives the "
  "correct order of the steps that follow, as described in NCERT?",
  "Downstream processing",
  "NCERT: after completion of the biosynthetic stage, the product has to be subjected through a series of "
  "processes before it is ready for marketing as a finished product. The processes include separation and "
  "purification, collectively referred to as downstream processing. The product has to be formulated with "
  "suitable preservatives, and such formulation has to undergo thorough clinical trials, as in the case of drugs.",
  ["Separation and purification (downstream processing)", "Formulation with suitable preservatives",
   "Thorough clinical trials (for drugs)"],
  "Processes of Recombinant DNA Technology (Downstream processing)",
  at="C", correct="Separation and purification → formulation with suitable preservatives → clinical trials",
  wrong=["Clinical trials → separation and purification → formulation with suitable preservatives",
         "Formulation with suitable preservatives → separation and purification → clinical trials",
         "Separation and purification → clinical trials → isolation of the gene of interest"],
  why="A product must be separated and purified before it can be formulated, and it is the formulation that "
      "undergoes clinical trials; isolating the gene is an early step of recombinant DNA work, not one after "
      "production.", secs=40)

HB_AT = 2
OVERHANG = "AATT"
assert sum(HB_AT for b in OVERHANG if b in "AT") == 8
Z(BPP, "Restriction enzymes", A, NUM,
  "EcoRI cuts 5'-GAATTC-3' between G and A on each strand, leaving a single-stranded overhang 5'-AATT-3' on each "
  "cut end. When two such ends meet, the overhangs pair with each other. Using the base-pairing rule that A pairs "
  "with T through two hydrogen bonds (and G with C through three), how many hydrogen bonds hold the two paired "
  "overhangs together at one such joint, before DNA ligase acts?",
  "Hydrogen bonding of sticky ends",
  "The 5'-AATT-3' overhang of one end pairs, antiparallel, with the 5'-AATT-3' overhang of the other end, forming "
  "four base pairs, all A-T. Each A-T pair has two hydrogen bonds, so 4 × 2 = 8 hydrogen bonds. NCERT: these "
  "hydrogen bonds between sticky ends facilitate the action of DNA ligase.",
  ["Overhang length = 4 nucleotides -> 4 base pairs", "All are A-T pairs", "4 × 2 = 8 hydrogen bonds"],
  "Restriction Enzymes; Class 12 Ch 5 'Molecular Basis of Inheritance', Structure of polynucleotide chain",
  at="B", correct="8", wrong=["12", "4", "6"],
  why="12 uses three hydrogen bonds per pair (the G-C value); 4 counts one bond per pair; 6 counts only three "
      "base pairs.", secs=60, vb=RECOMPUTED)

Z(BPP, "PCR and gel electrophoresis", A, D,
  "A circular plasmid is digested and run on an agarose gel. With EcoRI alone, one band of 5 kb is seen. With BamHI "
  "alone, one band of 5 kb is seen. With EcoRI and BamHI together, two bands of 2 kb and 3 kb are seen. What can be "
  "concluded?",
  "Interpreting a double digest",
  "A circular DNA cut at n sites gives n fragments. One 5 kb band with each enzyme alone means each enzyme cuts the "
  "5 kb circle once (opening it into a 5 kb linear molecule). Cutting with both gives two fragments, 2 kb and 3 kb, "
  "so the EcoRI and BamHI sites are 2 kb apart on one side of the circle and 3 kb apart on the other. Smaller "
  "fragments move farther in the gel, so the 2 kb band lies farther from the well.",
  ["Single digests: one site each, plasmid = 5 kb", "Double digest: 2 kb + 3 kb = 5 kb",
   "Sites are 2 kb apart one way round and 3 kb the other"],
  "Processes of Recombinant DNA Technology (Cutting of DNA; separation of DNA fragments)",
  at="D", correct="The plasmid is 5 kb, with one EcoRI site and one BamHI site that are 2 kb apart one way round "
                  "the circle and 3 kb apart the other",
  wrong=["The plasmid is 10 kb, with two EcoRI sites and two BamHI sites",
         "Neither enzyme cuts the plasmid, since one band is seen with each",
         "The plasmid is 5 kb with two EcoRI sites, 2 kb apart, and no BamHI site"],
  why="Two sites per enzyme in a circle would give two fragments with each enzyme alone; an uncut plasmid would "
      "not give a linear 5 kb band whose double digest splits into 2 + 3 kb; and if BamHI had no site, the double "
      "digest would match the EcoRI digest.", secs=75)

Z(BPP, "Competent hosts and transformation", A, MUL,
  MS("A scientist wants to introduce a recombinant gene into PLANT cells. Which of the following methods described "
     "in NCERT are suitable?",
     ["Biolistics (gene gun), using gold or tungsten micro-particles coated with DNA",
      "A 'disarmed' Ti plasmid of Agrobacterium tumefaciens",
      "Micro-injection, which NCERT describes for injecting DNA into the nucleus of an animal cell",
      "A disarmed retrovirus",
      "Calcium treatment followed by heat shock, as used for bacteria"]),
  "Choosing a gene-transfer method for plants",
  "NCERT: biolistics or gene gun is suitable for plants; the Ti plasmid of Agrobacterium tumefaciens has been "
  "modified into a cloning vector that is no longer pathogenic to plants but delivers genes of interest into a "
  "variety of plants. Micro-injection is described for animal cells, retroviruses have been disarmed to deliver "
  "genes into animal cells, and calcium treatment with heat shock is the method for making bacteria competent.",
  ["(a) biolistics: plants", "(b) disarmed Ti plasmid: plants", "(c) micro-injection: animal cells",
   "(d) retrovirus: animal cells", "(e) Ca²⁺ + heat shock: bacteria"],
  "Competent Host (for transformation with recombinant DNA); Cloning Vectors (vectors for cloning genes in plants "
  "and animals)",
  at="A", correct="(a) and (b) only",
  wrong=["(a), (b) and (c) only", "(b) and (d) only", "(a), (d) and (e) only"],
  why="NCERT describes micro-injection and disarmed retroviruses for animal cells and calcium plus heat shock for "
      "bacteria, so options containing (c), (d) or (e) are wrong.", secs=50)

Z(BPP, "Restriction enzymes", A, MAT,
  ML(("DNA digested completely with one restriction enzyme", "number of fragments obtained"),
     ["A linear DNA with one recognition site", "A circular plasmid with one recognition site",
      "A linear DNA with three recognition sites", "A circular plasmid with three recognition sites"],
     ["One", "Two", "Three", "Four"]),
  "Counting fragments from linear and circular DNA",
  "Cutting a linear molecule at n sites gives n + 1 fragments; cutting a circle at n sites gives n fragments. So: "
  "linear, 1 site -> 2; circular, 1 site -> 1 (the circle is only opened); linear, 3 sites -> 4; circular, 3 sites "
  "-> 3.",
  ["Linear: n + 1", "Circular: n", "A -> II, B -> I, C -> IV, D -> III"],
  "Restriction Enzymes",
  at="B", match=({"A": "II", "B": "I", "C": "IV", "D": "III"},
                 [{"A": "I", "B": "II", "C": "III", "D": "IV"},
                  {"A": "II", "B": "I", "C": "III", "D": "IV"},
                  {"A": "I", "B": "II", "C": "IV", "D": "III"}]),
  why="The wrong codes use the circular rule (n) for linear DNA, the linear rule (n + 1) for circular DNA, or both "
      "mistakes together.", secs=45)

Z(BPP, "PCR and gel electrophoresis", A, ASR,
  AR("If the denaturation step of a PCR cycle is omitted, the primers cannot anneal to the template DNA.",
     "In PCR, the double-stranded DNA is separated into single strands at high temperature (denaturation), and "
     "the primers then bind to complementary regions of the single-stranded template."),
  "Order of PCR steps",
  "NCERT: each PCR cycle has three steps: denaturation, annealing and extension. Denaturation separates the "
  "double-stranded DNA; the primers (small chemically synthesised oligonucleotides complementary to regions of "
  "the template) then anneal to the single-stranded DNA. Without denaturation the template remains double-stranded "
  "and the primers cannot bind, so R explains A.",
  ["Annealing needs single-stranded template", "Single strands come from denaturation", "No denaturation -> no "
   "annealing -> R explains A"],
  "Processes of Recombinant DNA Technology (Amplification of gene of interest using PCR)", ans="A",
  why="R states why primers need the denaturation step, so 'R is not the correct explanation' is wrong; neither "
      "statement is false.", secs=40)

assert 2 ** 10 == 1024
Z(BPP, "PCR and gel electrophoresis", A, STP,
  SP("Starting from a single double-stranded DNA molecule, 10 PCR cycles in which the DNA doubles every cycle give "
     "1024 molecules.",
     "On an agarose gel, a 0.5 kb DNA fragment moves a shorter distance from the well than a 5 kb fragment."),
  "PCR numbers and gel mobility",
  "Statement I: 1 × 2¹⁰ = 1024 molecules, so it is true. Statement II: NCERT - the smaller the fragment size, the "
  "farther it moves; the 0.5 kb fragment moves farther than the 5 kb fragment, so Statement II is false.",
  ["I: 2¹⁰ = 1024 -> true", "II: smaller fragments move farther -> false"],
  "Processes of Recombinant DNA Technology (PCR; separation of DNA fragments)", ans="C",
  why="Statement II reverses the size-mobility relation, so options calling it true are wrong; the arithmetic in "
      "Statement I is correct.", secs=45, vb=RECOMPUTED)


# ================================================================ Biotechnology and its Applications (5/7/5)
Z(BTA, "Transgenic animals", B, D,
  "Which of the following is NOT one of the reasons NCERT gives for producing transgenic animals?",
  "Why transgenic animals are made",
  "NCERT lists the common reasons for producing transgenic animals as: normal physiology and development, study of "
  "disease, biological products, vaccine safety, and chemical safety testing. Making animals run faster is not "
  "among them.",
  ["NCERT reasons: physiology and development; disease; biological products; vaccine safety; chemical safety",
   "Locomotion speed: not a listed reason"],
  "Transgenic Animals",
  at="D", correct="To increase the speed of locomotion of farm animals",
  wrong=["Study of normal physiology and development", "Vaccine safety testing", "Chemical (toxicity) safety "
         "testing"],
  why="Normal physiology and development, vaccine safety and chemical safety testing are all reasons NCERT lists "
      "for producing transgenic animals.", secs=20)

Z(BTA, "Bt crops and RNAi", B, D,
  "NCERT names some crop plants in which Bt toxin genes have been expressed to provide resistance to insects. Which "
  "of the following crops is NOT among those named?",
  "Crops expressing Bt toxin genes",
  "NCERT: the Bt toxin gene has been cloned from the bacteria and expressed in plants to provide resistance to "
  "insects without the need for insecticides; examples named are Bt cotton, Bt corn, rice, tomato, potato and "
  "soyabean. Wheat is not among the crops NCERT names.",
  ["Named: cotton, corn, rice, tomato, potato, soyabean", "Wheat: not named"],
  "Biotechnological Applications in Agriculture",
  at="C", correct="Wheat", wrong=["Corn", "Tomato", "Soyabean"],
  why="Corn, tomato and soyabean all appear in NCERT's list of crops in which Bt toxin genes have been expressed.",
  secs=20)

Z(BTA, "Bt crops and RNAi", B, MAT,
  ML(("term", "meaning"),
     ["Bt", "cry", "RNA interference (RNAi)", "Genetically modified organism (GMO)"],
     ["Plants, bacteria, fungi or animals whose genes have been altered by manipulation",
      "Bacillus thuringiensis, the bacterium that produces the toxin",
      "Silencing of a specific mRNA by a complementary dsRNA molecule that binds to it and prevents its translation",
      "Name of the genes that code for the Bt toxin protein"]),
  "Terms of agricultural biotechnology",
  "NCERT: Bt stands for Bacillus thuringiensis; the Bt toxin is coded by a gene cry, and there are a number of them "
  "(e.g., cryIAc, cryIIAb, cryIAb); RNAi involves silencing of a specific mRNA due to a complementary dsRNA molecule "
  "that binds to and prevents translation of the mRNA; plants, bacteria, fungi and animals whose genes have been "
  "altered by manipulation are called genetically modified organisms (GMO).",
  ["Bt -> II", "cry -> IV", "RNAi -> III", "GMO -> I"],
  "Biotechnological Applications in Agriculture",
  at="C", match=({"A": "II", "B": "IV", "C": "III", "D": "I"},
                 [{"A": "IV", "B": "II", "C": "III", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "II", "B": "III", "C": "IV", "D": "I"}]),
  why="The wrong codes exchange the bacterium with its toxin genes, exchange RNAi with the definition of a GMO, or "
      "give mRNA silencing to the cry genes.", secs=35)

Z(BTA, "Human insulin", B, ASR,
  AR("Insulin consists of two short polypeptide chains, chain A and chain B, that are linked together by disulphide "
     "bridges.",
     "In Eli Lilly's method, a single gene for pro-insulin was expressed in E. coli and the C peptide was then "
     "removed."),
  "Structure and production of human insulin",
  "NCERT: insulin consists of two short polypeptide chains, chain A and chain B, linked together by disulphide "
  "bridges, so A is true. In 1983, Eli Lilly prepared two DNA sequences corresponding to the A and B chains, "
  "introduced them into plasmids of E. coli to produce the chains separately, and combined the extracted chains by "
  "creating disulphide bonds. R, which describes a single pro-insulin gene, is false.",
  ["A: true", "R: false - separate DNA sequences for chains A and B"],
  "Biotechnological Applications in Medicine (Genetically Engineered Insulin)", ans="C",
  why="R misdescribes Eli Lilly's method, so options calling R true are wrong; A is NCERT's description of insulin.",
  secs=35)

Z(BTA, "Transgenic animals", B, STP,
  SP("Transgenic animals that produce useful biological products can be created by introducing the portion of DNA "
     "(or genes) which codes for a particular product.",
     "Human protein (α-1-antitrypsin) produced using transgenic animals is used to treat emphysema."),
  "Transgenic animals and biological products",
  "Both are NCERT statements under 'biological products': such animals are made by introducing the portion of DNA "
  "coding for a particular product, e.g., human protein (α-1-antitrypsin) used to treat emphysema; similar "
  "attempts are being made for the treatment of phenylketonuria and cystic fibrosis.",
  ["Statement I: true", "Statement II: true"],
  "Transgenic Animals", ans="A",
  why="Both statements are correct NCERT lines, so every option calling either of them false is wrong.", secs=30)

Z(BTA, "Human insulin", I, D,
  "A company uses E. coli to produce only chain A of human insulin and markets it as insulin. Based on NCERT, why "
  "would this product not be functional insulin?",
  "Both chains are needed",
  "NCERT: insulin consists of two short polypeptide chains, chain A and chain B, linked together by disulphide "
  "bridges. In Eli Lilly's method, chains A and B were produced separately, extracted and combined by creating "
  "disulphide bonds to form human insulin. Chain A alone lacks chain B and the disulphide links, so it is not "
  "insulin.",
  ["Functional insulin = chain A + chain B", "Linked by disulphide bridges", "Chain A alone -> not insulin"],
  "Biotechnological Applications in Medicine (Genetically Engineered Insulin)",
  at="B", correct="Functional insulin needs both chain A and chain B, joined by disulphide bridges",
  wrong=["Chain A must first be converted into DNA inside the patient",
         "Insulin made in bacteria is always pig insulin, which causes allergy",
         "Chain A is the C peptide, which is removed from mature insulin"],
  why="Proteins are not converted into DNA; recombinant human insulin is human, not pig, insulin; and the C peptide "
      "is a separate stretch of the pro-hormone, not chain A.", secs=40)

Z(BTA, "Human insulin", I, MUL,
  MS("According to NCERT, which of the following are advantages of therapeutic drugs produced by recombinant DNA "
     "technology?",
     ["They can be mass-produced.",
      "They are safe and more effective.",
      "They do not induce the unwanted immunological responses that are common with similar products isolated "
      "from non-human sources.",
      "They have to be extracted from the pancreas of slaughtered animals.",
      "Recombinant insulin is cattle insulin made in bacteria."]),
  "Recombinant therapeutics",
  "NCERT: recombinant DNA technological processes have made immense impact in healthcare by enabling mass "
  "production of safe and more effective therapeutic drugs; further, recombinant therapeutics do not induce "
  "unwanted immunological responses, as is common in the case of similar products isolated from non-human sources. "
  "Extraction from slaughtered animals is the older method, and recombinant insulin is human insulin.",
  ["(a), (b), (c): NCERT's advantages", "(d) old method", "(e) false - human insulin"],
  "Biotechnological Applications in Medicine",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (e) only"],
  why="'(a) and (b) only' leaves out the absence of unwanted immune responses; extraction from animal pancreas (d) "
      "is what recombinant production replaced, and the insulin made is human insulin, not cattle insulin (e).",
  secs=40)

Z(BTA, "Gene therapy", I, MUL,
  MS("A child with adenosine deaminase (ADA) deficiency is given gene therapy using his own lymphocytes. Which of "
     "the following statements are correct?",
     ["The enzyme ADA is crucial for the immune system to function.",
      "Lymphocytes from the patient's blood are grown in a culture outside the body.",
      "A functional ADA cDNA is introduced into these lymphocytes using a retroviral vector.",
      "Retroviruses used as vectors for animal cells are disarmed before use.",
      "Once infused, the engineered lymphocytes are immortal, so a single infusion cures the child."]),
  "ADA gene therapy across chapters",
  "NCERT (Ch 10): ADA is crucial for the immune system to function; in gene therapy, lymphocytes from the blood of "
  "the patient are grown in a culture outside the body, a functional ADA cDNA is introduced into them using a "
  "retroviral vector, and the cells are returned to the patient; as these cells are not immortal, the patient "
  "requires periodic infusion. NCERT (Ch 9): retroviruses, which can transform normal cells into cancerous cells, "
  "have been disarmed and are now used to deliver desirable genes into animal cells.",
  ["(a) true", "(b) true", "(c) true", "(d) true (Ch 9, vectors for animal cells)", "(e) false - cells are not "
   "immortal; periodic infusion needed"],
  "Gene Therapy; Class 12 Ch 9, Cloning Vectors",
  at="A", correct="(a), (b), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (c), (d) and (e) only"],
  why="(e) is false because NCERT says the engineered lymphocytes are not immortal; '(a), (b) and (c) only' leaves "
      "out (d), which is NCERT's statement that retroviral vectors are disarmed.", secs=55)

Z(BTA, "Human insulin", I, ASR,
  AR("A diabetic patient who is allergic to insulin extracted from the pancreas of pigs can usually be treated with "
     "human insulin produced by recombinant DNA technology.",
     "Recombinant therapeutics do not induce the unwanted immunological responses that are common with similar "
     "products isolated from non-human sources."),
  "Why recombinant human insulin avoids allergy",
  "NCERT: insulin from slaughtered cattle and pigs caused some patients to develop allergy or other types of "
  "reactions to the foreign protein. Recombinant therapeutics do not induce unwanted immunological responses, as "
  "is common with products from non-human sources. That is why recombinant human insulin suits such a patient, so "
  "R explains A.",
  ["Pig insulin = foreign protein -> allergy in some patients", "Recombinant human insulin: no unwanted immune "
   "response", "-> R explains A"],
  "Biotechnological Applications in Medicine (Genetically Engineered Insulin)", ans="A",
  why="R is the reason the switch to recombinant insulin helps, so 'R is not the correct explanation' is wrong; "
      "neither statement is false.", secs=35)

Z(BTA, "Bt crops and RNAi", I, STP,
  SP("Most Bt toxins are insect-group specific, so the choice of the toxin genes depends upon the crop and the "
     "targeted pest.",
     "Bt toxin genes have so far been expressed only in cotton."),
  "Specificity and spread of Bt crops",
  "NCERT: the toxin is coded by a gene cry, and the choice of genes depends upon the crop and the targeted pest, as "
  "most Bt toxins are insect-group specific. NCERT also names several crops besides cotton in which Bt toxin genes "
  "have been expressed: corn, rice, tomato, potato and soyabean.",
  ["Statement I: true", "Statement II: false - also corn, rice, tomato, potato, soyabean"],
  "Biotechnological Applications in Agriculture", ans="C",
  why="Statement II ignores the other crops NCERT names, so options calling it true are wrong; Statement I is "
      "NCERT's own reasoning.", secs=30)

Z(BTA, "Biosafety, biopiracy and patents", I, MAT,
  ML(("item", "what NCERT says about it"),
     ["Some ethical standards", "Gene therapy", "Turmeric and neem", "Biotechnology"],
     ["Indian traditional herbal medicines on which attempts were made to patent uses, products and processes",
      "Deals essentially with industrial-scale production of biopharmaceuticals and biologicals using genetically "
      "modified microbes, fungi, plants and animals",
      "Required to evaluate the morality of all human activities that might help or harm living organisms",
      "An attempt to provide a corrective therapy for a hereditary disease with which a person is born"]),
  "Ethics, bio-resources and the scope of biotechnology",
  "NCERT: some ethical standards are required to evaluate the morality of all human activities that might help or harm living organisms; there have "
  "been attempts to patent uses, products and processes based on Indian traditional herbal medicines, e.g., "
  "turmeric and neem; biotechnology essentially deals with industrial-scale production of biopharmaceuticals and "
  "biologicals using genetically modified microbes, fungi, plants and animals; and if a person is born with a "
  "hereditary disease, gene therapy is an attempt to take a corrective therapy for such a disease.",
  ["Ethical standards -> III", "Gene therapy -> IV", "Turmeric and neem -> I", "Biotechnology -> II"],
  "Ethical Issues; chapter introduction; Gene therapy",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
  why="The wrong codes exchange the role of ethical standards with the scope of biotechnology, exchange gene therapy "
      "with the herbal medicines, or exchange the herbal medicines with the scope of biotechnology.", secs=50)

Z(BTA, "Bt crops and RNAi", I, ASR,
  AR("Golden rice protects itself from insect pests by producing the Bt toxin.",
     "Golden rice is a genetically modified crop enriched in vitamin A."),
  "Golden rice",
  "NCERT gives golden rice, i.e., vitamin A enriched rice, as an example of a GM crop with enhanced nutritional "
  "value. It is not described as a Bt (insect-resistant) crop; insect resistance comes from cry genes of Bacillus "
  "thuringiensis. So A is false and R is true.",
  ["A: false - golden rice is about nutrition, not Bt toxin", "R: true - enriched in vitamin A"],
  "Biotechnological Applications in Agriculture", ans="D",
  why="A wrongly attributes Bt-based insect resistance to golden rice, so options calling A true are wrong; R is "
      "NCERT's description.", secs=30)

Z(BTA, "Bt crops and RNAi", A, D,
  "A virus with an RNA genome infects a eukaryotic cell. According to NCERT's account of RNA interference as a "
  "method of cellular defence, how could the cell limit the virus?",
  "RNAi as a natural defence",
  "NCERT: RNAi takes place in all eukaryotic organisms as a method of cellular defence. This method involves "
  "silencing of a specific mRNA due to a complementary dsRNA molecule that binds to and prevents translation of the "
  "mRNA (silencing). The source of this complementary RNA could be an infection by viruses having RNA genomes, or "
  "mobile genetic elements (transposons) that replicate via an RNA intermediate.",
  ["Viral RNA infection can provide the complementary RNA", "dsRNA binds the specific mRNA", "Translation of "
   "that mRNA is prevented -> silencing"],
  "Biotechnological Applications in Agriculture (RNA interference)",
  at="D", correct="A complementary dsRNA molecule could bind to the specific viral mRNA and prevent its translation "
                  "(silencing)",
  wrong=["The cell could produce Bt toxin, which creates pores in the virus",
         "The cell could cut the viral RNA with EcoRI at GAATTC sites",
         "The cell could produce interferons that make the infected cell immortal"],
  why="Bt toxin acts on insect midgut cells, not on viruses; EcoRI is a bacterial enzyme that cuts DNA, not a "
      "eukaryotic defence acting on RNA; and interferons protect non-infected cells, they do not make cells "
      "immortal.", secs=50)

Z(BTA, "Human insulin", A, MUL,
  MS("Which of the following statements correctly compare insulin made in the human body with the human insulin "
     "produced by Eli Lilly?",
     ["In the body, insulin is synthesised as a pro-hormone containing an extra stretch called the C peptide.",
      "Eli Lilly produced chains A and B separately in E. coli.",
      "In both cases, the functional hormone has chains A and B linked by disulphide bonds.",
      "Eli Lilly had to remove the C peptide from the chains made in E. coli.",
      "Eli Lilly introduced DNA sequences corresponding to the A and B chains into plasmids of E. coli."]),
  "Natural vs recombinant insulin",
  "NCERT: in mammals, including humans, insulin is synthesised as a pro-hormone that contains an extra stretch "
  "called the C peptide, which is removed during maturation. Eli Lilly prepared two DNA sequences corresponding to "
  "the A and B chains, introduced them into plasmids of E. coli to produce the chains separately, and combined the "
  "extracted chains by creating disulphide bonds. Since no pro-hormone was made, there was no C peptide to remove.",
  ["(a) true", "(b) true", "(c) true - A and B linked by disulphide bonds", "(d) false - no pro-insulin made, no C "
   "peptide", "(e) true"],
  "Biotechnological Applications in Medicine (Genetically Engineered Insulin)",
  at="B", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (d) only", "(a), (b), (c), (d) and (e)", "(b), (c) and (e) only"],
  why="(d) is false because Eli Lilly's chains were made separately, not as pro-insulin, so options with (d) are "
      "wrong; '(b), (c) and (e) only' leaves out the natural pro-hormone with its C peptide.", secs=60)

Z(BTA, "Gene therapy", A, ASR,
  AR("Adenosine deaminase (ADA) deficiency affects the functioning of the immune system.",
     "The first clinical gene therapy was given in 1990 to a 4-year-old girl with ADA deficiency."),
  "ADA deficiency",
  "NCERT: the enzyme ADA is crucial for the immune system to function, so its deficiency affects immunity; "
  "separately, the first clinical gene therapy was given in 1990 to a 4-year-old girl with ADA deficiency. Both "
  "statements are true, but the date of the first gene therapy says nothing about why ADA deficiency affects the "
  "immune system.",
  ["A: true", "R: true", "R is a historical fact, not the cause of A"],
  "Gene Therapy", ans="B",
  why="Both statements are true, so options with a false statement are wrong; R records when the first therapy "
      "was given and does not explain A.", secs=35)

Z(BTA, "Transgenic animals", A, STP,
  SP("Transgenic mice are being developed for use in testing the safety of the polio vaccine; if successful, they "
     "could replace the use of monkeys for testing the safety of batches of the vaccine.",
     "Transgenic animals made more sensitive to toxic substances than non-transgenic animals take longer to give "
     "the results of toxicity testing."),
  "Safety testing with transgenic animals",
  "NCERT: transgenic mice are being developed for use in testing the safety of vaccines; if successful and found "
  "reliable, they could replace the use of monkeys to test the safety of batches of the vaccine (polio). For "
  "chemical (toxicity) safety testing, transgenic animals carrying genes that make them more sensitive to toxic "
  "substances are exposed to the substances, and the effects studied allow results to be obtained in LESS time.",
  ["Statement I: true", "Statement II: false - results in less time"],
  "Transgenic Animals", ans="C",
  why="Statement II reverses NCERT's point that sensitive transgenic animals give results in less time, so options "
      "calling it true are wrong; Statement I is NCERT's account.", secs=40)

Z(BTA, "Biosafety, biopiracy and patents", A, D,
  "A company develops a commercial product from a medicinal plant of a developing country and the traditional "
  "knowledge of its people. It does so with proper authorisation from the country and the people concerned and "
  "makes the agreed compensatory payment to them. According to NCERT's definition, is this biopiracy?",
  "Definition of biopiracy",
  "NCERT: biopiracy is the term used to refer to the use of bio-resources by multinational companies and other "
  "organisations without proper authorisation from the countries and people concerned, without compensatory "
  "payment. Here both authorisation and compensation are present, so by NCERT's definition it is not biopiracy.",
  ["Biopiracy = use without authorisation AND without compensatory payment", "Here: authorised and compensated",
   "-> not biopiracy"],
  "Ethical Issues",
  at="A", correct="No, because biopiracy refers to use without proper authorisation and without compensatory "
                  "payment",
  wrong=["Yes, because any commercial use of bio-resources of another country is biopiracy",
         "Yes, because only industrialised nations may use bio-resources",
         "No, because medicinal plants are not bio-resources"],
  why="NCERT's definition depends on the absence of authorisation and compensation, not on commercial use as such; "
      "nothing in NCERT restricts the use of bio-resources to industrialised nations; and medicinal plants are "
      "bio-resources, which is why turmeric and neem appear in NCERT's discussion.", secs=45)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 133
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_008", "created_at": TODAY,
           "notes": "ZOO_008_p2: 133 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers and computed match/count keys re-derived in tools/batch_008/ZOO_008_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
