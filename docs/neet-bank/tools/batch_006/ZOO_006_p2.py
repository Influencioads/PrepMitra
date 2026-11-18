"""Builder for package ZOO_006_p2 of BATCH_006 (Zoology, 128 questions, NEET_ZOO_001373..NEET_ZOO_001500).

Topics: Chemical Coordination and Integration, Human Reproduction, Reproductive Health, Evolution,
Human Health and Disease, Biotechnology: Principles and Processes, Biotechnology and its Applications.

Every numerical answer is re-derived below with an assert; the plan quota, ID range, format mix and answer-key
balance are asserted before the file is written. If any assert fails, nothing is written. Each question's
correct position is fixed by hand (argument `at`), so editing one question never moves the options of another.

    python tools/batch_006/ZOO_006_p2.py      (run from docs/neet-bank)
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
PACKAGE = "ZOO_006_p2"
PLAN = ROOT / "batches" / "plans" / "BATCH_006_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_006_ZOO_p2.json"
FIRST_ID = 1373

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




# ================================================================ Chemical Coordination and Integration (5/7/5)
Z(CCI, "Hypothalamus and pituitary", B, D,
  "Most hormones of the pars distalis act on another endocrine gland. Which of the following pars distalis "
  "hormones acts instead on a gland that is NOT an endocrine gland?",
  "Targets of the anterior pituitary hormones",
  "NCERT: TSH stimulates the thyroid, ACTH stimulates the adrenal cortex and LH stimulates the gonads (androgen "
  "secretion from the testis; ovulation and corpus luteum in the ovary) - all endocrine tissues. Prolactin "
  "regulates the growth of the mammary glands and formation of milk; the mammary gland is not an endocrine gland.",
  ["TSH -> thyroid (endocrine)", "ACTH -> adrenal cortex (endocrine)", "LH -> gonads (endocrine)",
   "Prolactin -> mammary glands (not endocrine)"],
  "The pituitary gland",
  at="C", correct="Prolactin",
  wrong=["TSH", "ACTH", "LH"],
  why="TSH, ACTH and LH all stimulate hormone secretion by another endocrine gland (thyroid, adrenal cortex, "
      "gonads), so they do not fit the description.", secs=30)

Z(CCI, "Adrenal, pancreas and gonads", B, D,
  "Both ovaries of a woman are removed surgically. The blood levels of which pair of hormones will fall as a "
  "direct result?",
  "The ovary as an endocrine gland",
  "NCERT: the ovary produces two groups of steroid hormones, estrogen and progesterone. Estrogen is synthesised "
  "mainly by the growing ovarian follicles and progesterone by the corpus luteum. Removing the ovaries removes "
  "both sources.",
  ["Ovary secretes estrogen (follicles) and progesterone (corpus luteum)", "No ovaries -> both fall"],
  "Testis and ovary",
  at="D", correct="Estrogen and progesterone",
  wrong=["FSH and LH", "Oxytocin and prolactin", "Insulin and glucagon"],
  why="FSH, LH and prolactin come from the anterior pituitary, oxytocin from the hypothalamus via the posterior "
      "pituitary, and insulin and glucagon from the pancreatic islets; none of these is made in the ovary.",
  secs=25)

Z(CCI, "Hypothalamus and pituitary", B, D,
  "A drug blocks the release of gonadotrophin releasing hormone (GnRH) from the hypothalamus. The secretion of "
  "which pituitary hormones will fall as a direct result?",
  "Hypothalamic control of the gonadotrophins",
  "NCERT: GnRH from the hypothalamus stimulates the pituitary to synthesise and release gonadotrophins. LH and FSH "
  "are the gonadotrophins because they stimulate gonadal activity. Blocking GnRH lowers LH and FSH.",
  ["GnRH stimulates gonadotrophin release", "Gonadotrophins = LH and FSH"],
  "The hypothalamus; The pituitary gland",
  at="D", correct="LH and FSH",
  wrong=["TSH and ACTH", "Oxytocin and vasopressin", "Growth hormone and prolactin"],
  why="TSH, ACTH, GH and prolactin are not gonadotrophins and are not controlled by GnRH; oxytocin and vasopressin "
      "are hypothalamic hormones released from the neurohypophysis, not hormones whose release GnRH stimulates.",
  secs=25)

Z(CCI, "Thyroid, parathyroid and pineal", B, D,
  "The anterior pituitary of a person secretes too little TSH. Which of the following is the expected direct "
  "consequence?",
  "TSH and the thyroid",
  "NCERT: TSH stimulates the synthesis and secretion of thyroid hormones from the thyroid gland. Low TSH therefore "
  "lowers the secretion of thyroxine (T4) and triiodothyronine (T3).",
  ["TSH -> thyroid", "Low TSH -> less T4 and T3"],
  "The pituitary gland; The thyroid gland",
  at="B", correct="Decreased secretion of thyroxine and triiodothyronine by the thyroid",
  wrong=["Decreased secretion of parathyroid hormone", "Decreased secretion of glucocorticoids by the adrenal "
         "cortex", "Decreased secretion of melatonin by the pineal gland"],
  why="PTH secretion is regulated by blood Ca2+, glucocorticoid secretion by ACTH, and melatonin is a pineal "
      "hormone; none of these depends on TSH.", secs=25)

Z(CCI, "Hormonal disorders", B, D,
  "Which of the following disorders results from UNDER-secretion (hyposecretion) of a hormone rather than from "
  "its over-secretion?",
  "Hypo- and hyperactivity of endocrine glands",
  "NCERT: Addison's disease is caused by underproduction of hormones by the adrenal cortex. Exophthalmic goitre is "
  "a form of hyperthyroidism, and acromegaly and gigantism result from excess growth hormone.",
  ["Addison's disease: underproduction by adrenal cortex", "Others: excess hormone"],
  "The adrenal gland; The thyroid gland; The pituitary gland",
  at="D", correct="Addison's disease",
  wrong=["Exophthalmic goitre", "Acromegaly", "Gigantism"],
  why="Exophthalmic goitre (Graves' disease) is hyperthyroidism; acromegaly (adults) and gigantism (children) "
      "result from excess growth hormone.", secs=25)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("In a person whose β-cells of the islets of Langerhans have been destroyed, glucose moves from the blood "
     "into hepatocytes and adipocytes much more slowly than normal.",
     "In such a person, the conversion of glucose to glycogen (glycogenesis) in the target cells is stimulated "
     "more than normal."),
  "Actions of insulin",
  "NCERT: insulin, secreted by the β-cells, acts mainly on hepatocytes and adipocytes, enhances cellular glucose "
  "uptake and utilisation (rapid movement of glucose from blood into these cells) and stimulates glycogenesis. "
  "Without β-cells there is no insulin, so glucose uptake is slow (Statement I true) and glycogenesis is not "
  "stimulated (Statement II false).",
  ["β-cells -> insulin", "No insulin -> slow glucose uptake: I true",
   "Glycogenesis is an insulin action, so it is not stimulated: II false"],
  "Pancreas", ans="C",
  why="Statement II attributes an insulin action to a person who lacks insulin, so options calling it true are "
      "wrong; Statement I correctly follows from the loss of insulin.", secs=45)

Z(CCI, "Hypothalamus and pituitary", I, MAT,
  ML(("hormone", "endocrine tissue whose secretion it directly stimulates"),
     ["GnRH", "TSH", "ACTH", "LH (in males)"],
     ["Leydig cells of the testis", "Thyroid gland", "Adrenal cortex", "Pars distalis of the pituitary"]),
  "Chain of control from the hypothalamus",
  "NCERT: GnRH from the hypothalamus stimulates the pituitary (pars distalis) to release gonadotrophins; TSH "
  "stimulates the thyroid; ACTH stimulates the adrenal cortex to secrete glucocorticoids; LH in males stimulates "
  "the synthesis and secretion of androgens from the testis (Leydig cells).",
  ["GnRH -> IV", "TSH -> II", "ACTH -> III", "LH -> I"],
  "The hypothalamus; The pituitary gland; Testis and ovary",
  at="B", match=({"A": "IV", "B": "II", "C": "III", "D": "I"},
                 [{"A": "I", "B": "II", "C": "III", "D": "IV"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="GnRH acts on the pituitary itself, not on the testis; TSH and ACTH must not be swapped (thyroid vs adrenal "
      "cortex); the other codes break one of these links.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, ASR,
  AR("The pancreas is a composite gland that acts as both an exocrine and an endocrine gland.",
     "Glucagon secreted by the pancreas is a peptide hormone."),
  "Pancreas: composite gland; chemical nature of glucagon",
  "Both statements are true (NCERT). A is true because the pancreas has exocrine tissue (digestive secretion) and "
  "endocrine islets of Langerhans. R describes the chemical nature of one islet hormone; the peptide nature of "
  "glucagon has nothing to do with the pancreas having both exocrine and endocrine parts.",
  ["A true: exocrine part + islets", "R true: glucagon is a peptide hormone",
   "R is about chemical class, not the dual nature -> not the explanation"],
  "Pancreas; Mechanism of hormone action", ans="B",
  why="R is true, so 'R is false' options are wrong; A is true; R does not explain why the pancreas is composite.",
  secs=40)

Z(CCI, "Hypothalamus and pituitary", I, ASR,
  AR("Oxytocin released at the time of child birth causes a vigorous contraction of the uterus.",
     "Oxytocin acts on the smooth muscles of our body and stimulates their contraction."),
  "Action of oxytocin",
  "NCERT: oxytocin acts on the smooth muscles of our body and stimulates their contraction; in females it "
  "stimulates a vigorous contraction of the uterus at the time of child birth. The uterine wall (myometrium) is "
  "smooth muscle, so R directly explains A.",
  ["R: oxytocin contracts smooth muscle", "Uterine myometrium is smooth muscle", "So R explains A"],
  "The pituitary gland", ans="A",
  why="Both statements are true and the uterine contraction is a direct instance of oxytocin's action on smooth "
      "muscle, so B, C and D are wrong.", secs=35)

Z(CCI, "Adrenal, pancreas and gonads", I, D,
  "If the adrenal cortex of a person secretes too little aldosterone, which of the following changes is expected?",
  "Actions of aldosterone",
  "NCERT: aldosterone acts mainly at the renal tubules and stimulates the reabsorption of Na+ and water and the "
  "excretion of K+ and phosphate ions; it helps maintain electrolytes, body fluid volume, osmotic pressure and "
  "blood pressure. Too little aldosterone means less Na+ and water are reabsorbed (more lost in urine), K+ is "
  "retained, and blood pressure tends to fall.",
  ["Aldosterone: Na+ and water reabsorption, K+ excretion", "Deficiency reverses these",
   "Less body fluid volume -> blood pressure tends to fall"],
  "The adrenal gland",
  at="D", correct="More Na+ and water are lost in the urine, K+ is retained, and blood pressure tends to fall",
  wrong=["More Na+ and water are reabsorbed, K+ is lost, and blood pressure tends to rise",
         "Blood glucose rises sharply because gluconeogenesis is stimulated",
         "Blood Ca2+ falls because bone resorption stops"],
  why="The second option describes aldosterone excess; gluconeogenesis is a glucocorticoid/glucagon action and "
      "bone resorption is a PTH action, not aldosterone effects.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", I, STP,
  SP("The testis and the ovary are primary sex organs that also function as endocrine glands.",
     "Progesterone, secreted mainly by the corpus luteum, acts on the mammary glands and stimulates the formation "
     "of alveoli and milk secretion."),
  "Gonads as endocrine glands",
  "NCERT: the testis performs dual functions - as a primary sex organ and as an endocrine gland; the ovary is the "
  "primary female sex organ and produces estrogen and progesterone. Progesterone, secreted mainly by the corpus "
  "luteum, supports pregnancy and also acts on the mammary glands, stimulating the formation of alveoli "
  "(sac-like structures that store milk) and milk secretion. Both statements are true.",
  ["Gonads: gametes + hormones -> I true", "Progesterone (corpus luteum) -> mammary alveoli, milk secretion -> II "
   "true"],
  "Testis and ovary", ans="A",
  why="Both statements match NCERT, so any option calling either of them false is wrong.", secs=40)

Z(CCI, "Hypothalamus and pituitary", I, MUL,
  MS("Which of the following hormones are secreted by glands outside the pituitary but are directly stimulated by "
     "a hormone of the pars distalis?",
     ["Thyroxine", "Glucocorticoids such as cortisol", "Testosterone", "Adrenaline", "Parathyroid hormone"]),
  "Pituitary hormones that control other glands",
  "NCERT: TSH stimulates the secretion of thyroid hormones; ACTH stimulates the secretion of glucocorticoids from "
  "the adrenal cortex; LH stimulates the synthesis and secretion of androgens (mainly testosterone) from the "
  "testis. Adrenaline is secreted by the adrenal medulla in response to stress or emergency, and PTH secretion is "
  "regulated by the circulating Ca2+ level - neither is stimulated by a pituitary hormone.",
  ["(a) TSH -> thyroxine", "(b) ACTH -> glucocorticoids", "(c) LH -> testosterone",
   "(d) adrenaline: stress/emergency", "(e) PTH: blood Ca2+"],
  "The pituitary gland",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="Options containing (d) or (e) are wrong: adrenaline release is a stress response of the adrenal medulla and "
      "PTH is controlled by blood calcium, not by a pituitary hormone.", secs=50)

Z(CCI, "Hypothalamus and pituitary", A, MUL,
  MS("In a person, the hypothalamic axons that run to the neurohypophysis are damaged, but the portal circulatory "
     "system between the hypothalamus and the anterior pituitary is intact. Which of the following are expected?",
     ["Release of vasopressin from the posterior pituitary decreases.",
      "The person may lose large amounts of water in the urine and become dehydrated.",
      "Secretion of TSH and ACTH continues.",
      "Oxytocin continues to be released normally from the posterior pituitary.",
      "The pars distalis stops secreting growth hormone."]),
  "Neural and portal links between hypothalamus and pituitary",
  "NCERT: the posterior pituitary is under the direct neural regulation of the hypothalamus; oxytocin and "
  "vasopressin are synthesised by the hypothalamus and transported axonally to the neurohypophysis for storage "
  "and release. The anterior pituitary is regulated by hypothalamic hormones reaching it through a portal "
  "circulatory system. Damaged axons -> less vasopressin (ADH) and oxytocin released; low ADH -> excessive loss "
  "of water and dehydration (diabetes insipidus). With the portal system intact, TSH, ACTH and GH continue.",
  ["(a) axons carry vasopressin -> true", "(b) low ADH -> water loss -> true", "(c) portal route intact -> true",
   "(d) oxytocin uses the same axons -> false", "(e) GH needs the portal route, which is intact -> false"],
  "The hypothalamus; The pituitary gland; Disorders",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (c) and (e) only"],
  why="(d) is false because oxytocin travels along the same damaged axons; (e) is false because GH secretion "
      "depends on the intact portal route. Options including either are wrong.", secs=75)

Z(CCI, "Mechanism of hormone action", A, D,
  "Which of the following shows the correct sequence of events when a steroid hormone acts on its target cell?",
  "Mechanism of action of steroid hormones",
  "NCERT: hormones such as steroid hormones interact with intracellular (mostly nuclear) receptors; the "
  "hormone-receptor complex interacts with the genome and regulates gene expression, leading to new mRNA and "
  "proteins and finally the physiological response. They do not need a second messenger.",
  ["Hormone enters the cell", "Binds intracellular receptor -> complex", "Complex acts on genome -> gene "
   "expression (mRNA, protein)", "Physiological response"],
  "Mechanism of hormone action",
  at="B", correct="Hormone enters the cell -> binds an intracellular receptor -> hormone-receptor complex "
                  "interacts with the genome -> mRNA and new proteins -> physiological response",
  wrong=["Hormone binds a membrane receptor -> cyclic AMP is generated -> hormone enters the nucleus -> "
         "physiological response",
         "Hormone enters the cell -> generates IP3 and Ca2+ -> hormone-receptor complex forms on the cell membrane "
         "-> response",
         "Hormone-receptor complex interacts with the genome -> hormone enters the cell -> binds a membrane "
         "receptor -> response"],
  why="Second messengers (cAMP, IP3, Ca2+) belong to hormones acting through membrane-bound receptors; the last "
      "option puts the events in an impossible order (the complex cannot act on the genome before the hormone "
      "enters).", secs=50)

Z(CCI, "Hypothalamus and pituitary", A, ASR,
  AR("Destruction of the pars distalis of the pituitary would reduce the secretion of glucocorticoids and of "
     "thyroid hormones.",
     "The pars distalis secretes ACTH and TSH, which stimulate the adrenal cortex and the thyroid gland "
     "respectively."),
  "Tropic hormones of the pars distalis",
  "NCERT: the pars distalis produces GH, PRL, TSH, ACTH, LH and FSH. ACTH stimulates the synthesis and secretion "
  "of glucocorticoids from the adrenal cortex; TSH stimulates the synthesis and secretion of thyroid hormones. "
  "Without the pars distalis there is no ACTH or TSH, so these secretions fall: R directly explains A.",
  ["Pars distalis -> ACTH, TSH", "ACTH -> glucocorticoids; TSH -> thyroid hormones",
   "Loss of pars distalis -> both fall: R explains A"],
  "The pituitary gland", ans="A",
  why="Both statements are true and the fall in glucocorticoids and thyroid hormones follows directly from the "
      "loss of ACTH and TSH, so B, C and D are wrong.", secs=50)

Z(CCI, "Hormonal disorders", A, STP,
  SP("Diabetes insipidus is characterised by prolonged hyperglycemia, with glucose appearing in the urine.",
     "In diabetes mellitus, prolonged hyperglycemia leads to loss of glucose through urine and to the formation "
     "of harmful compounds called ketone bodies."),
  "Diabetes insipidus versus diabetes mellitus",
  "NCERT: impaired ADH synthesis or release results in diminished ability of the kidney to conserve water, "
  "leading to water loss and dehydration - diabetes insipidus; blood glucose is not the problem. Prolonged "
  "hyperglycemia leads to diabetes mellitus, associated with loss of glucose through urine and formation of "
  "ketone bodies. Statement I is false and Statement II is true.",
  ["DI: ADH deficiency -> water loss, not hyperglycemia -> I false", "DM: hyperglycemia, glycosuria, ketone "
   "bodies -> II true"],
  "The pituitary gland; Pancreas", ans="D",
  why="Statement I borrows the features of diabetes mellitus for diabetes insipidus, so options calling it true "
      "are wrong; Statement II is NCERT's description.", secs=45)

Z(CCI, "Adrenal, pancreas and gonads", A, MAT,
  ML(("hormone", "action on metabolism described in NCERT"),
     ["Insulin", "Glucagon", "Glucocorticoids", "Catecholamines"],
     ["Stimulate gluconeogenesis, lipolysis and proteolysis, and inhibit cellular uptake and utilisation of amino "
      "acids",
      "Stimulates the conversion of glucose to glycogen in its target cells",
      "Stimulate the breakdown of glycogen, and also the breakdown of lipids and proteins",
      "Acts mainly on hepatocytes, stimulating glycogenolysis and gluconeogenesis"]),
  "Hormones in carbohydrate, lipid and protein metabolism",
  "NCERT: insulin stimulates glycogenesis in target cells; glucagon acts mainly on hepatocytes and stimulates "
  "glycogenolysis and gluconeogenesis; glucocorticoids stimulate gluconeogenesis, lipolysis and proteolysis and "
  "inhibit cellular uptake and utilisation of amino acids; catecholamines stimulate the breakdown of glycogen "
  "and also of lipids and proteins.",
  ["Insulin -> II", "Glucagon -> IV", "Glucocorticoids -> I", "Catecholamines -> III"],
  "Pancreas; The adrenal gland",
  at="A", match=({"A": "II", "B": "IV", "C": "I", "D": "III"},
                 [{"A": "IV", "B": "II", "C": "I", "D": "III"},
                  {"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="Insulin is the only hormone here that builds glycogen; the glucocorticoid row is the one that mentions "
      "amino-acid uptake, and the catecholamine row adds glycogen breakdown to lipid and protein breakdown - each "
      "wrong code swaps one of these pairs.", secs=60)


# ================================================================ Human Reproduction (7/9/7)
# HR numerical: a primary oocyte (46 chromosomes) completes meiosis I -> secondary oocyte + first polar body, both
# haploid (23 chromosomes each)
prim_oocyte = 46
assert prim_oocyte // 2 == 23                                  # correct: 23 and 23
assert (prim_oocyte, prim_oocyte // 2) == (46, 23)             # distractor: polar body thought to be diploid

Z(HR, "Male and female reproductive systems", B, D,
  "In the human female, which of the following together constitute the female accessory ducts?",
  "Parts of the female reproductive system",
  "NCERT: the oviducts (fallopian tubes), uterus and vagina constitute the female accessory ducts. The ovaries "
  "are the primary female sex organs, and the mons pubis, labia and clitoris are external genitalia.",
  ["Primary sex organs: ovaries", "Accessory ducts: oviducts, uterus, vagina"],
  "The female reproductive system",
  at="D", correct="Oviducts, uterus and vagina",
  wrong=["Ovaries, oviducts and uterus", "Rete testis, vasa efferentia and epididymis",
         "Labia majora, labia minora and clitoris"],
  why="The ovaries are primary sex organs, not ducts; rete testis, vasa efferentia and epididymis are male "
      "accessory ducts; the labia and clitoris are external genitalia.", secs=25)

Z(HR, "Gametogenesis", B, D,
  "When a sperm enters the secondary oocyte, the oocyte completes its second meiotic division. Besides the second "
  "polar body, this division produces:",
  "Completion of oogenesis",
  "NCERT: the entry of the sperm into the ovum induces the completion of the meiotic division of the secondary "
  "oocyte. This results in the formation of a second polar body and a haploid ovum (ootid).",
  ["Sperm entry -> meiosis II completed", "Products: second polar body + haploid ovum (ootid)"],
  "Gametogenesis; Fertilisation and implantation",
  at="B", correct="A haploid ovum (ootid)",
  wrong=["A diploid primary oocyte", "A first polar body", "A Graafian follicle"],
  why="The primary oocyte and the first polar body belong to the first meiotic division, which is completed "
      "before ovulation; the Graafian follicle is an ovarian follicle, not a product of the oocyte's division.",
  secs=25)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "At the end of pregnancy, signals originating from the fully developed foetus and the placenta induce mild "
  "uterine contractions. These mild contractions are called the:",
  "Initiation of parturition",
  "NCERT: parturition is induced by a complex neuroendocrine mechanism. The signals originate from the fully "
  "developed foetus and the placenta and induce mild uterine contractions called the foetal ejection reflex, "
  "which triggers the release of oxytocin from the maternal pituitary.",
  ["Signals from foetus + placenta", "Mild contractions = foetal ejection reflex"],
  "Parturition and lactation",
  at="B", correct="Foetal ejection reflex",
  wrong=["Milk ejection reflex", "Implantation reflex", "Luteal surge"],
  why="Milk ejection concerns the mammary glands after birth; 'implantation reflex' and 'luteal surge' are not "
      "NCERT terms for the onset of parturition.", secs=25)

Z(HR, "Pregnancy, parturition and lactation", B, D,
  "In a pregnant woman, the umbilical cord:",
  "Placenta and umbilical cord",
  "NCERT: the placenta is connected to the embryo through an umbilical cord, which helps in the transport of "
  "substances to and from the embryo.",
  ["Placenta <-> embryo link = umbilical cord", "Function: transport of substances to and from the embryo"],
  "Pregnancy and embryonic development",
  at="B", correct="Connects the placenta to the embryo and helps in the transport of substances to and from the "
                  "embryo",
  wrong=["Connects the ovary to the uterus and carries the ovum", "Secretes hCG, hPL and relaxin",
         "Attaches the blastocyst to the endometrium during implantation"],
  why="The oviduct, not the umbilical cord, links ovary and uterus; hCG and hPL come from the placenta and relaxin "
      "from the ovary; implantation is the attachment of the trophoblast to the endometrium.", secs=25)

Z(HR, "Gametogenesis", B, NUM,
  "A human primary oocyte has 46 chromosomes. It completes its first meiotic division to form a secondary oocyte "
  "and the first polar body. The number of chromosomes in the first polar body and in the secondary oocyte, "
  "respectively, is:",
  "Reduction division in oogenesis",
  "The first meiotic division is the reduction division: each product receives one chromosome of every "
  "homologous pair. NCERT calls both the secondary oocyte and the first polar body haploid, so each has "
  "46/2 = 23 chromosomes; the division is unequal only in the amount of cytoplasm.",
  ["Meiosis I halves the chromosome number: 46 -> 23", "Both products are haploid", "First polar body: 23; "
   "secondary oocyte: 23"],
  "Gametogenesis",
  at="C", correct="23 and 23",
  wrong=["46 and 23", "23 and 46", "46 and 46"],
  why="'46 and 23' treats the tiny polar body as if it kept the diploid set; '23 and 46' and '46 and 46' confuse "
      "the unequal sharing of cytoplasm with the sharing of chromosomes.", secs=35, vb=RECOMPUTED)

Z(HR, "Male and female reproductive systems", B, STP,
  SP("Humans are sexually reproducing and viviparous.",
     "In humans, fertilisation takes place outside the body of the female."),
  "Mode of reproduction in humans",
  "NCERT: humans are sexually reproducing and viviparous. Semen is released into the vagina (insemination) and "
  "fertilisation takes place in the ampullary region of the oviduct, i.e. inside the female body (internal "
  "fertilisation). Statement I is true; Statement II is false.",
  ["Viviparous, sexual: I true", "Fertilisation in the ampulla of the oviduct: internal -> II false"],
  "Human Reproduction (introduction); Fertilisation and implantation", ans="C",
  why="Fertilisation is internal, in the oviduct, so Statement II is false and options calling it true are wrong.",
  secs=25)

Z(HR, "Male and female reproductive systems", B, D,
  "Which of the following is NOT a male accessory gland?",
  "Male accessory ducts versus accessory glands",
  "NCERT: the male accessory glands include paired seminal vesicles, a prostate and paired bulbourethral glands. "
  "The epididymis is one of the male sex accessory ducts (rete testis, vasa efferentia, epididymis, vas "
  "deferens).",
  ["Glands: seminal vesicles, prostate, bulbourethral", "Epididymis: an accessory duct"],
  "The male reproductive system",
  at="D", correct="Epididymis",
  wrong=["Seminal vesicle", "Prostate", "Bulbourethral gland"],
  why="Seminal vesicles, prostate and bulbourethral glands are the three accessory glands named by NCERT, so they "
      "do not answer a 'NOT' question.", secs=20)

Z(HR, "Male and female reproductive systems", I, D,
  "Both fallopian tubes of a woman are completely blocked, but her ovaries, pituitary and uterus are normal. "
  "Which of the following is expected?",
  "Role of the oviduct",
  "NCERT: the oviduct collects the ovum (infundibulum, fimbriae) and is the site of fertilisation (ampullary "
  "region); sperms reach the ampulla by swimming through the cervix, uterus and isthmus. Blocked tubes stop the "
  "gametes from meeting, but ovulation and the menstrual cycle depend on pituitary and ovarian hormones, which are "
  "normal.",
  ["Cycle controlled by pituitary + ovarian hormones -> continues", "Ovum and sperm cannot meet in the ampulla -> "
   "no fertilisation"],
  "The female reproductive system; Menstrual cycle; Fertilisation and implantation",
  at="D", correct="Ovulation and menstrual cycles continue, but sperms and ovum cannot meet, so fertilisation "
                  "does not occur",
  wrong=["Ovulation stops, so menstruation also stops",
         "Fertilisation occurs normally in the uterus instead of the oviduct",
         "The corpus luteum persists, so menstruation stops"],
  why="Blocking the tubes does not change the hormones that drive ovulation and menstruation; NCERT places "
      "fertilisation in the ampulla, not the uterus; nothing keeps the corpus luteum alive without pregnancy.",
  secs=45)

Z(HR, "Fertilisation and implantation", I, MUL,
  MS("Which of the following events normally take place in the human oviduct (fallopian tube)?",
     ["Fusion of the sperm with the ovum (fertilisation)",
      "Completion of the second meiotic division of the secondary oocyte",
      "The first mitotic divisions (cleavage) of the zygote",
      "Implantation of the blastocyst",
      "Transformation of the remaining parts of the Graafian follicle into the corpus luteum"]),
  "Sites of events from fertilisation to implantation",
  "NCERT: fertilisation takes place in the ampullary region; sperm entry induces completion of meiosis II there; "
  "cleavage starts as the zygote moves through the isthmus towards the uterus. The blastocyst is implanted in the "
  "endometrium of the uterus. The corpus luteum is formed in the ovary from the remaining parts of the Graafian "
  "follicle after ovulation.",
  ["(a) ampulla", "(b) on sperm entry, ampulla", "(c) isthmus", "(d) uterus - not oviduct",
   "(e) ovary - not oviduct"],
  "Fertilisation and implantation",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (e) only", "(c), (d) and (e) only", "(a) and (d) only"],
  why="Implantation (d) is in the uterine endometrium and the corpus luteum (e) forms in the ovary, so options "
      "containing them are wrong.", secs=50)

Z(HR, "Gametogenesis", I, ASR,
  AR("If the Sertoli cells of a man fail to respond to FSH, the formation of mature spermatozoa will be impaired.",
     "FSH acts on the Sertoli cells and stimulates the secretion of some factors which help in the process of "
     "spermiogenesis."),
  "Hormonal control of spermatogenesis",
  "NCERT: at puberty GnRH raises LH and FSH; LH acts on the Leydig cells (androgens), while FSH acts on the "
  "Sertoli cells and stimulates the secretion of factors that help in spermiogenesis (transformation of "
  "spermatids into spermatozoa). If Sertoli cells cannot respond, these factors are not secreted and "
  "spermiogenesis suffers - R directly explains A.",
  ["FSH -> Sertoli cells -> factors for spermiogenesis", "No response -> spermatids not transformed properly",
   "R explains A"],
  "Gametogenesis", ans="A",
  why="Both statements are true and R gives exactly the step that fails, so B, C and D are wrong.", secs=40)

Z(HR, "Gametogenesis", I, STP,
  SP("The oocyte released from the Graafian follicle at ovulation has completed its first meiotic division but "
     "not its second.",
     "The first polar body is formed at the time of fertilisation, when the sperm enters the oocyte."),
  "Timing of the meiotic divisions in oogenesis",
  "NCERT: the primary oocyte within the tertiary follicle completes its first meiotic division, forming a large "
  "haploid secondary oocyte and a tiny first polar body; the secondary oocyte is released at ovulation. Meiosis II "
  "is completed only when the sperm enters, forming the second polar body and the ootid. So Statement I is true "
  "and Statement II is false (that is the second polar body).",
  ["Meiosis I in tertiary follicle -> secondary oocyte + first polar body", "Ovulation releases secondary oocyte "
   "-> I true", "Sperm entry -> second polar body -> II false"],
  "Gametogenesis", ans="C",
  why="Statement II confuses the first polar body with the second, so it is false; Statement I is NCERT's "
      "description, so options calling it false are wrong.", secs=45)

Z(HR, "Male and female reproductive systems", I, MAT,
  ML(("part of the female reproductive tract", "feature"),
     ["Infundibulum", "Ampulla", "Isthmus", "Cervical canal"],
     ["Narrow lumen; joins the uterus", "Forms the birth canal together with the vagina",
      "Funnel-shaped part with fimbriae that help collect the ovum", "Wider part where fertilisation takes place"]),
  "Regions of the oviduct and cervix",
  "NCERT: the infundibulum is funnel-shaped with finger-like fimbriae that help collect the ovum; the ampulla is "
  "the wider part of the oviduct where fertilisation occurs (ampullary region); the isthmus has a narrow lumen and "
  "joins the uterus; the cavity of the cervix (cervical canal) along with the vagina forms the birth canal.",
  ["Infundibulum -> III", "Ampulla -> IV", "Isthmus -> I", "Cervical canal -> II"],
  "The female reproductive system; Fertilisation and implantation",
  at="C", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
  why="The fimbriae belong to the infundibulum and fertilisation to the ampulla; the narrow isthmus joins the "
      "uterus, while only the cervical canal forms part of the birth canal. Each wrong code swaps one pair.",
  secs=45)

Z(HR, "Gametogenesis", I, STP,
  SP("Spermatids are formed when the secondary spermatocytes undergo the second meiotic division.",
     "Spermiogenesis, the transformation of spermatids into spermatozoa, does not involve any further cell "
     "division."),
  "Spermatids and spermiogenesis",
  "NCERT: the secondary spermatocytes undergo the second meiotic division to produce four equal haploid "
  "spermatids; the spermatids are then transformed into spermatozoa by spermiogenesis. Spermiogenesis is a "
  "change of form (head, middle piece, tail develop); the number of cells does not change - 4 spermatids give 4 "
  "sperms. Both statements are true.",
  ["Secondary spermatocyte --meiosis II--> spermatids: I true", "Spermatid -> spermatozoon, one to one: II true"],
  "Gametogenesis", ans="A",
  why="Both statements agree with NCERT (four spermatids become four sperms), so options calling either false "
      "are wrong.", secs=40)

Z(HR, "Male and female reproductive systems", I, ASR,
  AR("The glandular tissue of each human breast contains clusters of cells called alveoli.",
     "The milk secreted by the alveolar cells is stored in the cavities of the lactiferous duct, and not in the "
     "alveoli."),
  "Structure of the mammary gland",
  "NCERT: the glandular tissue of each breast is divided into 15-20 mammary lobes containing clusters of cells "
  "called alveoli. The cells of the alveoli secrete milk, which is stored in the cavities (lumens) of the alveoli. "
  "The alveoli open into mammary tubules, ducts, ampulla and finally the lactiferous duct, through which milk is "
  "sucked out. A is true; R is false.",
  ["A: lobes contain alveoli -> true", "Milk is stored in the alveolar lumens -> R false"],
  "The female reproductive system (mammary glands)", ans="C",
  why="R misplaces the storage of milk (NCERT: lumens of the alveoli), so options treating R as true are wrong; A "
      "is true.", secs=40)

Z(HR, "Pregnancy, parturition and lactation", I, MAT,
  ML(("hormone in a pregnant woman", "source"),
     ["hCG", "Relaxin (later phase of pregnancy)", "Oxytocin (at parturition)", "Prolactin"],
     ["Ovary", "Anterior pituitary", "Placenta", "Maternal pituitary, released in response to the foetal "
      "ejection reflex"]),
  "Hormones of pregnancy and their sources",
  "NCERT: the placenta acts as an endocrine tissue and produces hCG, hPL, estrogens and progestogens. In the "
  "later phase of pregnancy, relaxin is secreted by the ovary. The foetal ejection reflex triggers release of "
  "oxytocin from the maternal pituitary. Prolactin is an anterior pituitary (pars distalis) hormone.",
  ["hCG -> III", "Relaxin -> I", "Oxytocin -> IV", "Prolactin -> II"],
  "Pregnancy and embryonic development; Parturition and lactation",
  at="D", match=({"A": "III", "B": "I", "C": "IV", "D": "II"},
                 [{"A": "I", "B": "III", "C": "IV", "D": "II"},
                  {"A": "III", "B": "I", "C": "II", "D": "IV"},
                  {"A": "II", "B": "I", "C": "IV", "D": "III"}]),
  why="Relaxin is ovarian, not placental, so codes that swap hCG and relaxin are wrong; oxytocin is released from "
      "the maternal pituitary on the foetal ejection reflex, while prolactin is the anterior pituitary hormone.",
  secs=45)

Z(HR, "Menstrual cycle", I, D,
  "A woman has a regular 28-day menstrual cycle. In which part of the cycle does the corpus luteum form?",
  "Ovulation and formation of the corpus luteum",
  "NCERT: ovulation occurs in the middle of the cycle (about the 14th day). After ovulation, in the luteal phase, "
  "the remaining parts of the Graafian follicle transform into the corpus luteum, which secretes large amounts of "
  "progesterone. So it forms just after day 14.",
  ["Ovulation ~ day 14", "Luteal phase follows", "Remaining Graafian follicle -> corpus luteum"],
  "Menstrual cycle",
  at="B", correct="Just after ovulation, at the start of the luteal phase (soon after about day 14)",
  wrong=["During the menstrual phase (days 1-5)", "During the follicular phase, before ovulation",
         "At the very end of the cycle (about day 28)"],
  why="The corpus luteum is formed from the follicle that has already released the ovum, so it cannot appear "
      "before ovulation; by day 28 (no fertilisation) it is degenerating, not forming.", secs=35)

Z(HR, "Menstrual cycle", A, MUL,
  MS("In the ovarian and uterine events of a normal menstrual cycle without fertilisation, which of the following "
     "pairs occur at the same time?",
     ["Growth of primary follicles into a Graafian follicle - regeneration of the endometrium through "
      "proliferation",
      "Peak (surge) of LH - breakdown of the endometrial lining and its blood vessels",
      "Secretion of large amounts of progesterone by the corpus luteum - maintenance of the endometrium",
      "Degeneration of the corpus luteum - disintegration of the endometrium",
      "Rupture of the Graafian follicle - menstrual flow"]),
  "Coordination of ovarian and uterine events",
  "NCERT: in the follicular phase, primary follicles grow into a Graafian follicle and simultaneously the "
  "endometrium regenerates through proliferation (a true). LH and FSH peak in the middle of the cycle and induce "
  "ovulation (rupture of the Graafian follicle) - not menstruation (b, e false). In the luteal phase the corpus "
  "luteum secretes progesterone, essential for maintaining the endometrium (c true). Without fertilisation, the "
  "corpus luteum degenerates, causing disintegration of the endometrium and menstruation (d true).",
  ["(a) follicular phase -> true", "(b) LH surge is mid-cycle, menstruation at start -> false",
   "(c) luteal phase -> true", "(d) end of cycle -> true", "(e) ovulation is mid-cycle -> false"],
  "Menstrual cycle",
  at="C", correct="(a), (c) and (d) only",
  wrong=["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"],
  why="Both (b) and (e) pair a mid-cycle ovarian event (LH surge, ovulation) with menstruation, which occurs at "
      "the start of the cycle, so any option containing them is wrong.", secs=70)

Z(HR, "Menstrual cycle", A, D,
  "In a woman, the pituitary secretes very little FSH throughout the cycle, while other hormones are initially "
  "normal. Which of the following is the most likely result?",
  "Role of FSH in the ovarian cycle",
  "NCERT (Ch 19 and Ch 2): in females FSH stimulates the growth and development of the ovarian follicles, and the "
  "gonadotropins stimulate follicular development and the secretion of estrogens by the growing follicles. "
  "Without enough FSH the follicles do not mature into a Graafian follicle, estrogen from growing follicles stays "
  "low, and there is no mature follicle for the LH surge to rupture - so ovulation fails.",
  ["FSH -> growth of follicles", "Growing follicles -> estrogens", "No Graafian follicle -> no ovulation"],
  "Menstrual cycle; Gametogenesis",
  at="D", correct="Ovarian follicles fail to develop properly, so estrogen secretion stays low and ovulation does "
                  "not occur",
  wrong=["Follicles develop normally, but the corpus luteum fails to secrete progesterone",
         "Ovulation occurs earlier than normal because LH acts alone",
         "Menstruation stops because the endometrium is maintained by excess progesterone"],
  why="The corpus luteum forms only after ovulation, which needs a developed follicle; LH cannot rupture a "
      "follicle that never matured; there is no source of excess progesterone without a corpus luteum.", secs=60)

Z(HR, "Gametogenesis", A, MUL,
  MS("Which of the following cells formed during human gametogenesis are haploid?",
     ["Primary oocyte", "First polar body", "Secondary spermatocyte", "Spermatogonium", "Ootid (ovum)"]),
  "Ploidy of cells in spermatogenesis and oogenesis",
  "NCERT: spermatogonia (46 chromosomes) and primary spermatocytes are diploid; the first meiotic division gives "
  "haploid secondary spermatocytes (23). Primary oocytes are formed from oogonia and are diploid (they are only "
  "arrested in prophase-I); the first meiotic division gives a haploid secondary oocyte and a haploid first polar "
  "body; meiosis II gives the second polar body and the haploid ovum (ootid).",
  ["(a) primary oocyte: diploid", "(b) first polar body: haploid", "(c) secondary spermatocyte: haploid",
   "(d) spermatogonium: diploid", "(e) ootid: haploid"],
  "Gametogenesis",
  at="A", correct="(b), (c) and (e) only",
  wrong=["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"],
  why="Primary oocytes (a) and spermatogonia (d) have not yet undergone meiosis I, so they are diploid; options "
      "containing them are wrong.", secs=50)

Z(HR, "Male and female reproductive systems", A, MUL,
  MS("In a man, the Leydig cells are destroyed, but the pituitary and the Sertoli cells are normal. Which of the "
     "following are expected?",
     ["Secretion of androgens falls.",
      "The functions of the male sex accessory ducts and glands are impaired.",
      "Spermatogenesis is adversely affected.",
      "The Sertoli cells stop responding to FSH.",
      "The pituitary stops secreting FSH."]),
  "Leydig cells and androgens",
  "NCERT: the Leydig (interstitial) cells synthesise and secrete testicular hormones called androgens. The "
  "functions of the male sex accessory ducts and glands are maintained by androgens, and LH acting on the Leydig "
  "cells stimulates the androgens that in turn stimulate spermatogenesis. Losing Leydig cells therefore lowers "
  "androgens (a), impairs accessory organs (b) and spermatogenesis (c). FSH acts on the Sertoli cells, which are "
  "normal, and the pituitary is normal, so (d) and (e) are false.",
  ["(a) Leydig cells = androgen source -> true", "(b) accessory organs need androgens -> true",
   "(c) androgens stimulate spermatogenesis -> true", "(d), (e) Sertoli cells and pituitary are unaffected"],
  "The male reproductive system; Gametogenesis",
  at="B", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(a) and (e) only", "(b), (d) and (e) only"],
  why="Statements (d) and (e) blame cells the stem says are normal; options containing either are wrong.",
  secs=60)

Z(HR, "Gametogenesis", A, D,
  "Which of the following shows the correct sequence of events in human oogenesis and follicle development?",
  "Sequence of oogenesis",
  "NCERT: oogonia formed in the fetal ovary enter meiosis as primary oocytes and are arrested in prophase-I; each "
  "primary oocyte with a layer of granulosa cells is a primary follicle; more granulosa layers and a new theca "
  "form the secondary follicle; a fluid-filled antrum marks the tertiary follicle, within which the primary oocyte "
  "completes meiosis I (secondary oocyte + first polar body); the tertiary follicle matures into the Graafian "
  "follicle, which ruptures to release the secondary oocyte (ovulation).",
  ["Oogonium -> primary oocyte (arrested, prophase-I)", "Primary -> secondary -> tertiary follicle",
   "Meiosis I completed in tertiary follicle", "Graafian follicle -> ovulation of secondary oocyte"],
  "Gametogenesis",
  at="C", correct="Oogonium -> primary oocyte arrested in prophase-I -> primary follicle -> secondary follicle -> "
                  "tertiary follicle (meiosis I completed) -> Graafian follicle -> ovulation of the secondary "
                  "oocyte",
  wrong=["Oogonium -> primary follicle -> secondary oocyte -> tertiary follicle -> primary oocyte -> Graafian "
         "follicle -> ovulation",
         "Oogonium -> primary oocyte -> meiosis II completed in the Graafian follicle -> ovulation of the ootid",
         "Primary oocyte -> oogonium -> tertiary follicle -> secondary follicle -> primary follicle -> ovulation"],
  why="The secondary oocyte cannot precede the primary oocyte; meiosis II is completed only on sperm entry, so the "
      "ootid is never ovulated; the last option reverses the follicle stages.", secs=55)

Z(HR, "Fertilisation and implantation", A, D,
  "Which of the following events in early human development occurs LAST?",
  "Order of events after fertilisation",
  "NCERT: cleavage gives the morula (8-16 blastomeres); the morula transforms into a blastocyst as it moves into "
  "the uterus; the blastocyst is implanted in the endometrium; after implantation the inner cell mass "
  "differentiates into an outer ectoderm and an inner endoderm, and a mesoderm soon appears between them.",
  ["Morula", "-> blastocyst", "-> implantation", "-> ectoderm and endoderm", "-> mesoderm appears (last)"],
  "Fertilisation and implantation; Pregnancy and embryonic development",
  at="B", correct="Appearance of the mesoderm between the ectoderm and the endoderm",
  wrong=["Formation of the morula", "Transformation of the morula into a blastocyst",
         "Implantation of the blastocyst in the endometrium"],
  why="Morula, blastocyst and implantation all come before the inner cell mass forms germ layers, so none of "
      "them is the last event.", secs=45)

Z(HR, "Fertilisation and implantation", A, STP,
  SP("A human sperm and a human ovum each carry 22 autosomes and one sex chromosome.",
     "The sex of the baby is decided at the time of implantation, depending on where the blastocyst attaches."),
  "Chromosomes of gametes and sex determination",
  "Gametes are haploid (23 chromosomes = 22 autosomes + 1 sex chromosome): the ovum always carries X and a sperm "
  "carries X or Y. NCERT: the sex of the baby is decided at fertilisation - a sperm carrying X gives XX (female), "
  "a sperm carrying Y gives XY (male). Implantation site has no role. Statement I is true; Statement II is false.",
  ["Gametes: 22 + 1 = 23 -> I true", "Sex fixed at fertilisation by the sperm's X or Y -> II false"],
  "Fertilisation and implantation", ans="C",
  why="Statement II replaces fertilisation by implantation as the moment of sex determination, so it is false; "
      "Statement I is true, so options calling it false are wrong.", secs=40)


# ================================================================ Reproductive Health (5/6/5)
# RH numerical: periodic abstinence from day 10 to day 17 of the cycle, both days included
abst = list(range(10, 17 + 1))
assert len(abst) == 8                                          # correct: 8 days
assert 17 - 10 == 7 and 28 - 17 == 11                          # distractors: forgot to count both ends; days after

Z(RH, "Contraception", B, D,
  "According to the World Health Organisation, as quoted in NCERT, reproductive health means:",
  "Meaning of reproductive health",
  "NCERT: according to the WHO, reproductive health means a total well-being in all aspects of reproduction, i.e. "
  "physical, emotional, behavioural and social. A society with people having physically and functionally normal "
  "reproductive organs and normal emotional and behavioural interactions in all sex-related aspects is "
  "reproductively healthy.",
  ["WHO: total well-being in all aspects of reproduction", "Physical, emotional, behavioural and social"],
  "Reproductive health - problems and strategies",
  at="B", correct="Total well-being in all aspects of reproduction: physical, emotional, behavioural and social",
  wrong=["Only the absence of sexually transmitted infections",
         "Only the ability to produce a large number of children",
         "Only physically normal reproductive organs, without regard to behaviour"],
  why="NCERT's (WHO) meaning covers physical, emotional, behavioural and social well-being; each other option "
      "narrows it to a single aspect, or to large families, which is not part of the definition.", secs=25)

Z(RH, "STDs and their prevention", B, D,
  "According to NCERT, the incidence of sexually transmitted infections (STIs) is reported to be very high among "
  "persons in the age group of:",
  "Who is most affected by STIs",
  "NCERT: the incidence of STIs is reported to be very high among persons in the age group of 15-24 years - the "
  "age group to which students belong - which is why awareness and early treatment are stressed.",
  ["NCERT figure: 15-24 years"],
  "Sexually transmitted infections (STIs)",
  at="D", correct="15-24 years",
  wrong=["5-12 years", "35-45 years", "Above 60 years"],
  why="NCERT names 15-24 years; the other age groups are not the ones it identifies as having very high incidence.",
  secs=20)

Z(RH, "Contraception", B, NUM,
  "A couple practising periodic abstinence avoids coitus from day 10 to day 17 of the menstrual cycle (both days "
  "included), the period when ovulation could be expected. For how many days of each cycle do they abstain?",
  "Periodic abstinence",
  "NCERT: in periodic abstinence the couple avoids coitus from day 10 to 17 of the menstrual cycle, when "
  "ovulation could be expected; chances of fertilisation are very high in this period. Counting both end days: "
  "17 - 10 + 1 = 8 days.",
  ["Days 10, 11, ..., 17", "Number = 17 - 10 + 1 = 8"],
  "Birth control (natural methods)",
  at="B", correct="8 days",
  wrong=["7 days", "10 days", "17 days"],
  why="7 forgets to count one of the end days (17 - 10); 10 and 17 confuse the first or last day of the period "
      "with its length.", secs=25, vb=RECOMPUTED)

Z(RH, "STDs and their prevention", B, D,
  "Which of the following is NOT a sexually transmitted infection?",
  "Examples of STIs",
  "NCERT lists gonorrhoea, syphilis, genital herpes, chlamydiasis, genital warts, trichomoniasis, hepatitis-B and "
  "HIV as common STIs. Typhoid is a bacterial disease spread through contaminated food and water (Ch 7).",
  ["NCERT STI list includes gonorrhoea, syphilis, chlamydiasis", "Typhoid: food- and water-borne"],
  "Sexually transmitted infections (STIs)",
  at="D", correct="Typhoid",
  wrong=["Gonorrhoea", "Syphilis", "Chlamydiasis"],
  why="Gonorrhoea, syphilis and chlamydiasis all appear in NCERT's list of STIs.", secs=20)

Z(RH, "STDs and their prevention", B, D,
  "According to NCERT, which of the following indicates improved reproductive health of a society?",
  "Indicators of improved reproductive health",
  "NCERT: better awareness about sex-related matters, increased number of medically assisted deliveries and "
  "better post-natal care leading to decreased maternal and infant mortality rates, an increased number of "
  "couples with small families, better detection and cure of STDs and overall increased medical facilities for "
  "all sex-related problems indicate improved reproductive health.",
  ["Indicators: lower MMR and IMR, small families, better STD detection and cure"],
  "Reproductive health - problems and strategies",
  at="C", correct="Decreased maternal and infant mortality rates because of medically assisted deliveries and "
                  "better post-natal care",
  wrong=["An increase in the number of couples with large families",
         "A rise in the incidence of STIs among young people",
         "Fewer medically assisted deliveries"],
  why="NCERT counts small families, better STD control and more medically assisted deliveries as signs of "
      "improvement; the other options describe the opposite trends.", secs=30)

Z(RH, "Contraception", I, D,
  "A man has undergone vasectomy. His seminal vesicles, prostate and bulbourethral glands are normal. Which of the "
  "following is expected?",
  "How vasectomy prevents conception",
  "NCERT: in vasectomy a small part of the vas deferens is removed or tied up through a small incision on the "
  "scrotum, blocking gamete transport. Sperms from the testis can no longer pass through the vas deferens, but the "
  "accessory glands still secrete the seminal plasma, so an ejaculate is still formed - without sperms.",
  ["Vas deferens cut/tied -> sperms cannot pass", "Accessory glands normal -> seminal plasma still formed",
   "Ejaculate lacks sperms"],
  "Birth control (surgical methods); Ch 2 'The male reproductive system'",
  at="A", correct="Seminal plasma is still ejaculated, but it lacks sperms",
  wrong=["No semen of any kind is ejaculated", "Sperm formation in the testes stops completely",
         "Sperms are ejaculated, but they cannot swim"],
  why="The accessory glands still produce seminal plasma, so some ejaculate is formed; vasectomy blocks transport, "
      "not sperm formation; it does not affect sperm motility - the sperms simply do not reach the ejaculate.",
  secs=40)

Z(RH, "Contraception", I, MUL,
  MS("Which of the following contraceptive methods act, at least in part, by preventing ovulation, according to "
     "NCERT?",
     ["Oral pills containing progestogens or progestogen-estrogen combinations",
      "Progestogen or progestogen-estrogen injections or implants under the skin",
      "Lactational amenorrhea",
      "Condoms",
      "Vasectomy"]),
  "Contraceptives that act on ovulation",
  "NCERT: oral pills inhibit ovulation and implantation and alter cervical mucus; injections and implants act in "
  "a way similar to pills (with much longer effective periods); in lactational amenorrhea, ovulation and therefore "
  "the cycle do not occur during intense lactation. Condoms are barriers, and vasectomy blocks sperm transport in "
  "the male.",
  ["(a) pills inhibit ovulation", "(b) same mode of action as pills", "(c) no ovulation during intense "
   "lactation", "(d) barrier", "(e) blocks sperm transport"],
  "Birth control",
  at="D", correct="(a), (b) and (c) only",
  wrong=["(a) and (b) only", "(a), (b), (c) and (d) only", "(c), (d) and (e) only"],
  why="'(a) and (b) only' misses lactational amenorrhea, which works because ovulation does not occur; options "
      "with (d) or (e) wrongly include methods that block the gametes, not ovulation.", secs=50)

Z(RH, "Contraception", I, ASR,
  AR("A copper-releasing IUD such as CuT can prevent conception even though it does not physically cover the "
     "cervix.",
     "The copper ions released suppress sperm motility and the fertilising capacity of sperms."),
  "Mode of action of copper-releasing IUDs",
  "NCERT: IUDs increase phagocytosis of sperms within the uterus, and the Cu ions released suppress sperm motility "
  "and the fertilising capacity of sperms. So CuT works on the sperms themselves rather than as a cervical "
  "barrier - R explains A.",
  ["CuT sits in the uterus, not over the cervix", "Cu ions: less motile, less fertile sperms", "R explains A"],
  "Birth control (IUDs)", ans="A",
  why="Both statements are true and the action of copper ions on sperms is precisely how CuT prevents conception "
      "without a barrier, so B, C and D are wrong.", secs=40)

Z(RH, "Infertility and ART", I, STP,
  SP("In artificial insemination, semen collected from the husband or a healthy donor may be introduced into the "
     "vagina or into the uterus.",
     "In in vitro fertilisation (IVF), the ovum and sperm fuse inside the fallopian tube of the woman."),
  "Artificial insemination and IVF",
  "NCERT: in artificial insemination (AI), the semen collected from the husband or a healthy donor is "
  "artificially introduced either into the vagina or into the uterus (IUI - intra-uterine insemination). IVF is "
  "fertilisation outside the body in almost similar conditions as in the body, followed by embryo transfer. "
  "Statement I is true; Statement II is false.",
  ["AI: vagina or uterus (IUI) -> I true", "IVF: fertilisation outside the body -> II false"],
  "Infertility", ans="C",
  why="'In vitro' means outside the body, so Statement II is false; Statement I is NCERT's description of AI.",
  secs=40)

Z(RH, "Contraception", I, MAT,
  ML(("contraceptive method", "NCERT description"),
     ["Diaphragms, cervical caps and vaults", "Progestogen implants", "Emergency contraception",
      "Saheli"],
     ["A 'once a week' pill containing a non-steroidal preparation", "Pills, IUDs or progestogens used within 72 "
      "hours of coitus", "Reusable rubber barriers that cover the cervix during coitus",
      "Placed under the skin; act like pills but with a much longer effective period"]),
  "Features of contraceptive methods",
  "NCERT: diaphragms, cervical caps and vaults are made of rubber, inserted to cover the cervix, and are reusable. "
  "Progestogens alone or with estrogen can be used as injections or implants under the skin; their mode of action "
  "is similar to pills and their effective periods are much longer. Progestogens, progestogen-estrogen "
  "combinations or IUDs within 72 hours of coitus are effective emergency contraceptives. Saheli is a once-a-week "
  "pill with a non-steroidal preparation.",
  ["Barriers -> III", "Implants -> IV", "Emergency -> II", "Saheli -> I"],
  "Birth control",
  at="A", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
  why="Implants, not cervical barriers, sit under the skin; emergency contraception is defined by the 72-hour "
      "window, not by long effect; Saheli is the weekly non-steroidal pill. Each wrong code swaps one pair.",
  secs=45)

Z(RH, "STDs and their prevention", I, D,
  "Which of the following sexually transmitted infections is completely curable if detected early and treated "
  "properly, according to NCERT?",
  "Curability of STIs",
  "NCERT: except for hepatitis-B, genital herpes and HIV infections, other STIs are completely curable if "
  "detected early and treated properly. Gonorrhoea is not in the list of exceptions.",
  ["Not completely curable: hepatitis-B, genital herpes, HIV", "Gonorrhoea: curable if treated early"],
  "Sexually transmitted infections (STIs)",
  at="C", correct="Gonorrhoea",
  wrong=["Hepatitis-B", "Genital herpes", "HIV infection"],
  why="Hepatitis-B, genital herpes and HIV are the three exceptions NCERT names as not completely curable.",
  secs=30)

Z(RH, "STDs and their prevention", A, MUL,
  MS("Which of the following statements about reproductive health in India are correct according to NCERT?",
     ["India was amongst the first countries in the world to initiate action plans and programmes at a national "
      "level to attain total reproductive health as a social goal.",
      "Improved programmes covering wider reproduction-related areas are currently in operation under the name "
      "'Reproductive and Child Health Care (RCH) programmes'.",
      "Amniocentesis is legally permitted in India for finding out the sex of the foetus.",
      "Governmental and non-governmental agencies use audio-visual and print media to create awareness about "
      "reproduction-related aspects.",
      "Research in reproduction-related areas is encouraged; the oral contraceptive Saheli was developed by "
      "scientists at CDRI, Lucknow."]),
  "Reproductive health programmes in India",
  "NCERT: India was amongst the first countries to initiate national action plans for total reproductive health "
  "(family planning); improved programmes now run as RCH programmes; creating awareness with the help of "
  "audio-visual and print media is a key strategy; research is encouraged and Saheli was developed at CDRI, "
  "Lucknow. NCERT states there is a statutory ban on amniocentesis for sex determination.",
  ["(a), (b), (d), (e) true", "(c) false: statutory ban on amniocentesis for sex determination"],
  "Reproductive health - problems and strategies",
  at="B", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
  why="(c) is false because amniocentesis for sex determination is banned, so options with (c) are wrong; '(a), "
      "(d) and (e) only' leaves out the true statement (b) about RCH programmes.", secs=60)

Z(RH, "Contraception", A, D,
  "A woman had unprotected coitus five days ago and now wants to avoid a possible pregnancy. According to NCERT, "
  "which of the following is correct?",
  "Time limit of emergency contraception",
  "NCERT: administration of progestogens or progestogen-estrogen combinations, or IUDs, within 72 hours of "
  "coitus is very effective as an emergency contraceptive, since these could be used to avoid possible pregnancy "
  "due to rape or casual unprotected intercourse. Five days = 120 hours, which is beyond the 72-hour window.",
  ["Emergency contraception window: 72 hours", "5 days = 120 hours > 72 hours",
   "So NCERT's emergency methods no longer fit this case"],
  "Birth control (emergency contraceptives)",
  at="D", correct="The NCERT emergency methods (pills or IUD) are effective only within 72 hours of coitus, so "
                  "this time window has already passed",
  wrong=["Emergency pills are effective up to 10 days after coitus",
         "A condom used now will prevent the pregnancy",
         "Periodic abstinence from now on will prevent the pregnancy"],
  why="NCERT gives a 72-hour window, not 10 days; condoms and periodic abstinence only work at the time of coitus "
      "and cannot act on an insemination that has already happened.", secs=45)

Z(RH, "STDs and their prevention", A, ASR,
  AR("Hepatitis-B can spread from one person to another even without any sexual contact.",
     "Hepatitis-B can also be transmitted by sharing injection needles or surgical instruments with infected "
     "persons, by transfusion of blood, or from an infected mother to the foetus."),
  "Non-sexual routes of STIs",
  "NCERT: some STIs, like hepatitis-B and HIV, can also be transmitted by sharing injection needles, surgical "
  "instruments, etc., with infected persons, by transfusion of blood, or from an infected mother to the foetus. "
  "These non-sexual routes are exactly why hepatitis-B can spread without sexual contact - R explains A.",
  ["Non-sexual routes listed in R", "These routes allow spread without sexual contact", "R explains A"],
  "Sexually transmitted infections (STIs)", ans="A",
  why="Both statements are true and R lists the very routes that make A true, so B, C and D are wrong.", secs=40)

Z(RH, "Infertility and ART", A, D,
  "A woman cannot produce ova and both her fallopian tubes are blocked, but her uterus is normal. Which of the "
  "following approaches, built from the techniques NCERT describes, can help her bear a child?",
  "Choosing an assisted reproductive technology",
  "NCERT: in IVF, ova from the wife or a donor and sperms from the husband or a donor are induced to form a "
  "zygote in the laboratory; embryos with more than 8 blastomeres are transferred into the uterus (IUT). GIFT and "
  "ZIFT need a functional fallopian tube, which she lacks. So a donor ovum fertilised in vitro, followed by "
  "transfer of the embryo into her uterus, fits her case.",
  ["No ova -> donor ovum", "Blocked tubes -> avoid GIFT/ZIFT (tube transfers)",
   "Normal uterus -> IVF + intra-uterine transfer"],
  "Infertility",
  at="B", correct="IVF using a donor ovum, followed by transfer of the embryo into her uterus (IUT)",
  wrong=["Gamete intra fallopian transfer (GIFT) of a donor ovum",
         "Zygote intra fallopian transfer (ZIFT) of her own zygote",
         "Intra-uterine insemination (IUI) with her husband's semen"],
  why="GIFT and ZIFT place gametes or the zygote into the fallopian tube, which is blocked; ZIFT and IUI also "
      "need her own ova, which she cannot produce.", secs=55)

Z(RH, "Infertility and ART", A, STP,
  SP("In IVF-ET, embryos with more than 8 blastomeres are transferred into the fallopian tube.",
     "Intra cytoplasmic sperm injection (ICSI) is a procedure to form an embryo in the laboratory, in which a "
     "sperm is directly injected into the ovum."),
  "Embryo transfer and ICSI",
  "NCERT: the zygote or early embryo (with up to 8 blastomeres) is transferred into the fallopian tube (ZIFT), "
  "and embryos with more than 8 blastomeres into the uterus (IUT). ICSI is another specialised procedure to form "
  "an embryo in the laboratory in which a sperm is directly injected into the ovum. Statement I is false; "
  "Statement II is true.",
  ["Up to 8 blastomeres -> fallopian tube (ZIFT)", "More than 8 -> uterus (IUT): I false", "ICSI description: "
   "II true"],
  "Infertility", ans="D",
  why="Statement I swaps the destinations of ZIFT and IUT, so it is false; Statement II is NCERT's own "
      "description of ICSI.", secs=40)


# ================================================================ Evolution (6/7/6)
# EVO basic: q = 0.1 -> p = 0.9 -> AA = p^2 = 0.81 (81%)
q1 = F(1, 10)
p1 = 1 - q1
assert p1 ** 2 == F(81, 100)                                   # correct: 81%
assert 2 * p1 * q1 == F(18, 100) and p1 == F(9, 10) and q1 ** 2 == F(1, 100)   # distractors: 18%, 90%, 1%

# EVO advanced: q = 0.2 -> Aa : aa = 2pq : q^2 = 0.32 : 0.04 = 8 : 1
q2 = F(1, 5)
p2 = 1 - q2
ratio = (2 * p2 * q2) / (q2 ** 2)
assert 2 * p2 * q2 == F(32, 100) and q2 ** 2 == F(4, 100) and ratio == 8      # correct: 8
assert (p2 * q2) / (q2 ** 2) == 4 and (2 * p2 * q2) / (p2 ** 2) == F(1, 2)    # distractors: no factor 2; vs AA
assert p2 / q2 == 4 and (p2 ** 2) / (q2 ** 2) == 16 and 1 / ratio == F(1, 8)

# EVO advanced: q = 0.1; share of all 'a' alleles that sit in heterozygotes
q3 = F(1, 10)
p3 = 1 - q3
a_in_het = 2 * p3 * q3 * 1          # each Aa individual carries one a allele
a_in_hom = q3 ** 2 * 2              # each aa individual carries two
share = a_in_het / (a_in_het + a_in_hom)
assert a_in_het == F(18, 100) and a_in_hom == F(2, 100) and share == F(9, 10)  # correct: 90%
assert (2 * p3 * q3) / (2 * p3 * q3 + q3 ** 2) == F(18, 19)                   # distractor: counted aa once (~95%)
assert q3 ** 2 / (2 * p3 * q3 + q3 ** 2) == F(1, 19)

Z(EVO, "Origin of life", B, D,
  "As the early earth cooled, the water vapour in its atmosphere fell as rain. According to NCERT, what did this "
  "rain water form?",
  "Early earth",
  "NCERT: as the earth cooled, the water vapour fell as rain, to fill the depressions and form oceans. Life later "
  "appeared in this water, about 500 million years after the formation of the earth.",
  ["Earth cools -> water vapour condenses as rain", "Rain fills the depressions -> oceans"],
  "Origin of life",
  at="A", correct="Oceans, by filling the depressions on the earth's surface",
  wrong=["Glaciers on the mountain tops", "Underground coal deposits", "The first land plants"],
  why="Glaciers, coal (from giant ferns) and land plants are unrelated to this early stage; the rain filled the "
      "depressions to form oceans.", secs=25)

Z(EVO, "Human evolution", B, D,
  "Among the fossils of about 2 million years ago, some bones differed from those of the Australopithecines. "
  "NCERT calls this creature the first human-like being, the hominid. It was named:",
  "First human-like being",
  "NCERT: some of the bones discovered (about 2 mya) were different; this creature was called the first "
  "human-like being, the hominid, and was named Homo habilis. Its brain capacity was 650-800 cc and it probably "
  "did not eat meat.",
  ["About 2 mya", "First human-like being (hominid) = Homo habilis"],
  "Origin and evolution of man",
  at="C", correct="Homo habilis",
  wrong=["Dryopithecus", "Homo erectus", "Neanderthal man"],
  why="Dryopithecus (about 15 mya) was ape-like; Homo erectus (about 1.5 mya) and Neanderthal man came later and "
      "are not described as the first human-like being.", secs=25)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, D,
  "NCERT lists five factors that affect Hardy-Weinberg equilibrium. Which of the following is NOT one of them?",
  "Factors affecting Hardy-Weinberg equilibrium",
  "NCERT: five factors are known to affect Hardy-Weinberg equilibrium: gene migration or gene flow, genetic "
  "drift, mutation, genetic recombination and natural selection. The use and disuse of organs is Lamarck's idea, "
  "not one of these factors.",
  ["Five factors: gene flow, drift, mutation, recombination, natural selection", "Use and disuse: Lamarck"],
  "Hardy-Weinberg principle",
  at="D", correct="Use and disuse of organs",
  wrong=["Gene migration (gene flow)", "Genetic drift", "Genetic recombination"],
  why="Gene flow, genetic drift and genetic recombination are all in NCERT's list of five factors.", secs=25)

Z(EVO, "Darwinism and modern synthesis", B, ASR,
  AR("Lamarck proposed natural selection as the mechanism of evolution.",
     "According to Lamarck, the evolution of life forms had occurred, driven by the use and disuse of organs."),
  "Lamarck's idea",
  "NCERT: Lamarck said that evolution of life forms had occurred but was driven by the use and disuse of organs "
  "(the giraffe's long neck is his example). Natural selection was proposed by Darwin (and Wallace). So A is false "
  "and R is true.",
  ["R: Lamarck - use and disuse -> true", "Natural selection: Darwin -> A false"],
  "Biological evolution", ans="D",
  why="A wrongly credits Lamarck with natural selection, so options calling A true are wrong; R is NCERT's own "
      "description of Lamarck's view.", secs=30)

Z(EVO, "Origin of life", B, D,
  "According to NCERT, the universe is made up of huge clusters of:",
  "Composition of the universe",
  "NCERT: the universe is vast and very old. Huge clusters of galaxies comprise the universe; galaxies contain "
  "stars and clouds of gas and dust.",
  ["Universe -> clusters of galaxies", "Galaxies -> stars, clouds of gas and dust"],
  "Origin of life",
  at="B", correct="Galaxies",
  wrong=["Planets only", "Meteorites", "Solar systems without stars"],
  why="NCERT says the universe comprises clusters of galaxies (with stars, gas and dust); planets and meteorites "
      "are much smaller bodies, and a solar system has a star at its centre.", secs=20)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", B, NUM,
  "A population is in Hardy-Weinberg equilibrium for a gene with alleles A and a. The frequency of allele a is "
  "0.1. What percentage of the individuals are homozygous dominant (AA)?",
  "Hardy-Weinberg genotype frequencies",
  "Allele frequencies add up to 1, so p = 1 - 0.1 = 0.9. The frequency of AA is p² = 0.9 × 0.9 = 0.81, i.e. 81% "
  "of the population.",
  ["p + q = 1 -> p = 0.9", "AA = p² = 0.81", "= 81%"],
  "Hardy-Weinberg principle",
  at="A", correct="81%",
  wrong=["90%", "18%", "1%"],
  why="90% is the allele frequency p, not a genotype frequency; 18% is 2pq (heterozygotes); 1% is q² (aa).",
  secs=30, vb=RECOMPUTED)

Z(EVO, "Origin of life", I, MAT,
  ML(("scientist", "contribution described in NCERT"),
     ["Louis Pasteur", "Oparin and Haldane", "S.L. Miller", "Karl Ernst von Baer"],
     ["Observed the formation of amino acids from CH4, H2, NH3 and water vapour with an electric discharge",
      "Noted that embryos never pass through the adult stages of other animals",
      "Showed that life comes only from pre-existing life",
      "Proposed that the formation of life was preceded by chemical evolution"]),
  "Scientists in the study of origin of life and evolution",
  "NCERT: Pasteur showed by careful experiments that life comes only from pre-existing life; Oparin (Russia) and "
  "Haldane (England) proposed that life came from pre-existing non-living organic molecules and that its "
  "formation was preceded by chemical evolution; Miller observed amino acids in his closed-flask experiment; "
  "Karl Ernst von Baer disapproved Haeckel's proposal, noting that embryos never pass through the adult stages "
  "of other animals.",
  ["Pasteur -> III", "Oparin and Haldane -> IV", "Miller -> I", "von Baer -> II"],
  "Origin of life; Evidence for evolution",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="Chemical evolution was Oparin and Haldane's proposal, not Pasteur's; Miller did the experiment that "
      "tested it; von Baer's observation concerns embryos. Each wrong code swaps one of these pairs.", secs=45)

Z(EVO, "Natural selection", I, ASR,
  AR("Industrial melanism in moths of England is an example of evolution by natural selection.",
     "In industrial areas, white-winged moths turned dark because soot settled on their wings."),
  "Industrial melanism",
  "NCERT: after industrialisation, tree trunks became dark due to industrial smoke and soot, and lichens did not "
  "grow. White-winged moths did not survive because predators spotted them against the dark background, while "
  "dark-winged (melanised) moths survived and increased. Selection acted on existing variants - so A is true. "
  "Moths did not become dark by soot settling on them, so R is false.",
  ["Existing variation: white and dark moths", "Dark trunks -> predators pick white moths -> dark moths increase",
   "A true; soot did not darken the moths -> R false"],
  "Evidence for evolution (industrial melanism)", ans="C",
  why="R describes a non-heritable change produced directly by the environment, which is not what NCERT says; "
      "options treating R as true are wrong, and A is true.", secs=40)

Z(EVO, "Darwinism and modern synthesis", I, MUL,
  MS("According to NCERT, which of the following describe the mutations that Hugo de Vries proposed as the cause "
     "of evolution?",
     ["They are random.", "They are directionless.", "They are small and directional, like Darwinian variations.",
      "They are single-step large changes (saltation).", "They cause speciation."]),
  "De Vries' mutation theory",
  "NCERT: based on his work on the evening primrose, Hugo de Vries brought forth the idea of mutations - large "
  "differences arising suddenly in a population. He believed that it is mutation which causes evolution, not the "
  "minor variations (heritable) that Darwin talked about. Mutations are random and directionless, while Darwinian "
  "variations are small and directional. Single-step large mutation is saltation, which he believed caused "
  "speciation.",
  ["(a), (b): random, directionless", "(c): describes Darwinian variations -> false", "(d) saltation",
   "(e) speciation by saltation"],
  "Mechanism of evolution",
  at="A", correct="(a), (b), (d) and (e) only",
  wrong=["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c) and (d) only"],
  why="Statement (c) describes Darwin's variations, which NCERT contrasts with mutations; any option including "
      "(c) is wrong.", secs=45)

Z(EVO, "Natural selection", I, D,
  "A bacterial colony grows on a medium. When the composition of the medium is changed, most cells die, but a few "
  "cells that can survive the new conditions multiply and, within days, form a population different from the "
  "original. According to NCERT's reasoning, this is best explained as:",
  "Natural selection of pre-existing variants in microbes",
  "NCERT: a change in medium composition brings out only that part of the bacterial population that can survive "
  "under the new conditions; this variant population outgrows the others and appears as a new species within "
  "days. Variation already present is selected by the changed environment - natural selection; microbes show it "
  "quickly because they divide fast.",
  ["Variants already present", "Changed medium favours some of them", "They outgrow the rest -> selection"],
  "Biological evolution",
  at="D", correct="Natural selection of variants already present, which then outgrow the others",
  wrong=["Inheritance of characters acquired by the use and disuse of organs",
         "Special creation of a new kind of bacterium by the new medium",
         "Gene flow from another bacterial population"],
  why="Use and disuse is Lamarck's idea; special creation is not a scientific explanation; the stem describes no "
      "migration of cells from another population, so gene flow does not apply.", secs=45)

Z(EVO, "Human evolution", I, STP,
  SP("Homo erectus had a larger brain than Homo habilis.",
     "The brain size of Neanderthal man was about 900 cc."),
  "Brain capacity in human evolution",
  "NCERT: Homo habilis had a brain capacity of 650-800 cc; Homo erectus had a large brain of around 900 cc; "
  "Neanderthal man had a brain size of 1400 cc. So Statement I is true and Statement II is false (900 cc is the "
  "Homo erectus value).",
  ["habilis 650-800 cc < erectus ~900 cc -> I true", "Neanderthal 1400 cc -> II false"],
  "Origin and evolution of man", ans="C",
  why="Statement II gives the Homo erectus value to Neanderthal man, so it is false; Statement I is true, so "
      "options calling it false are wrong.", secs=35)

Z(EVO, "Evidences of evolution", I, MUL,
  MS("Which of the following are examples of convergent evolution?",
     ["The eye of the octopus and the eye of mammals",
      "The Tasmanian wolf (a marsupial) and the placental wolf",
      "The forelimbs of whales and bats",
      "The flippers of penguins and of dolphins",
      "The thorn of Bougainvillea and the tendril of Cucurbita"]),
  "Convergent versus divergent evolution",
  "NCERT: analogous structures - different structures evolving for the same function - result from convergent "
  "evolution, e.g. the eyes of octopus and mammals and the flippers of penguins and dolphins. When placental "
  "mammals in Australia resemble corresponding marsupials (placental wolf and Tasmanian wolf), this is also "
  "convergent evolution. Forelimbs of whales and bats, and thorn/tendril, are homologous - divergent evolution.",
  ["(a), (d): analogous -> convergent", "(b): Australian example of convergence",
   "(c), (e): homologous -> divergent"],
  "Evidence for evolution; What is adaptive radiation?",
  at="C", correct="(a), (b) and (d) only",
  wrong=["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"],
  why="(c) and (e) are NCERT's examples of homology (divergent evolution), so options including them are wrong.",
  secs=50)

Z(EVO, "Human evolution", I, MAT,
  ML(("form in human evolution", "approximate time (NCERT)"),
     ["Dryopithecus and Ramapithecus", "Australopithecines", "Homo erectus", "Neanderthal man"],
     ["About 1.5 million years ago", "Between 1,00,000 and 40,000 years back", "About 15 million years ago",
      "About 2 million years ago"]),
  "Time-line of human evolution",
  "NCERT: about 15 mya, Dryopithecus and Ramapithecus existed; about 2 mya, Australopithecines probably lived in "
  "East African grasslands; Homo erectus existed about 1.5 mya; Neanderthal man lived in near east and central "
  "Asian countries between 1,00,000 and 40,000 years back.",
  ["Dryopithecus, Ramapithecus -> III", "Australopithecines -> IV", "Homo erectus -> I", "Neanderthal -> II"],
  "Origin and evolution of man",
  at="A", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
  why="The order of appearance (15 mya -> 2 mya -> 1.5 mya -> 1,00,000-40,000 years) fixes the code; each wrong "
      "code swaps two neighbouring forms.", secs=45)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "In a population in Hardy-Weinberg equilibrium, the frequency of the recessive allele a is 0.2. How many times "
  "more numerous are the heterozygous carriers (Aa) than the homozygous recessive individuals (aa)?",
  "Carriers versus affected individuals",
  "q = 0.2, so p = 0.8. Aa = 2pq = 2 × 0.8 × 0.2 = 0.32; aa = q² = 0.04. Ratio = 0.32/0.04 = 8. (In general "
  "2pq/q² = 2p/q.)",
  ["p = 1 - 0.2 = 0.8", "Aa = 2pq = 0.32", "aa = q² = 0.04", "0.32/0.04 = 8"],
  "Hardy-Weinberg principle",
  at="B", correct="8 times",
  wrong=["4 times", "One-eighth as many (0.125 times)", "16 times"],
  short="2pq/q² = 2p/q = 2 × 0.8/0.2 = 8.",
  why="4 comes from forgetting the factor 2 in 2pq (pq/q² = p/q); one-eighth inverts the ratio (aa/Aa); 16 is "
      "p²/q², the ratio of AA to aa, not of Aa to aa.", secs=60, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, NUM,
  "A population is in Hardy-Weinberg equilibrium and the frequency of the recessive allele a is 0.1. Of all the "
  "copies of allele a present in the population, what percentage are carried by heterozygous (Aa) individuals?",
  "Where recessive alleles are hidden",
  "q = 0.1, p = 0.9. Per individual: Aa individuals (frequency 2pq = 0.18) carry one a each -> 0.18 copies; aa "
  "individuals (q² = 0.01) carry two each -> 0.02 copies. Share in heterozygotes = 0.18/(0.18 + 0.02) = 0.9 = "
  "90%.",
  ["Aa = 2pq = 0.18 -> 0.18 a copies", "aa = q² = 0.01 -> 0.02 a copies", "0.18/0.20 = 90%"],
  "Hardy-Weinberg principle",
  at="D", correct="90%",
  wrong=["95%", "18%", "10%"],
  short="Share of a alleles in heterozygotes = 2pq/(2pq + 2q²) = p = 0.9.",
  why="95% (18/19) counts each aa individual as carrying only one a allele; 18% is just the heterozygote "
      "frequency; 10% is the allele frequency q.", secs=75, vb=RECOMPUTED)

Z(EVO, "Gene flow, drift and Hardy-Weinberg", A, MUL,
  MS("A few birds from a mainland population reach a distant island and found a new population, with no further "
     "contact with the mainland. Which of the following can make the island population diverge from the mainland "
     "population?",
     ["Genetic drift, i.e. changes in allele frequency by chance",
      "The founder effect, since the founders may carry allele frequencies different from the mainland",
      "Natural selection under the different conditions of the island",
      "Continuous gene flow between the island and the mainland",
      "Inheritance of characters acquired by use and disuse of organs"]),
  "Drift, founder effect and selection in isolated populations",
  "NCERT: change in allele frequency by chance is genetic drift; sometimes the change is so different that the "
  "drifted founders form a different population (founder effect). Natural selection also changes allele "
  "frequencies. Gene flow is ruled out by the stem and, if it occurred often, would keep the populations alike; "
  "use and disuse is Lamarck's discarded idea, not one of NCERT's factors.",
  ["(a), (b) drift and founder effect -> true", "(c) selection -> true",
   "(d) excluded by the stem -> false", "(e) not an NCERT factor -> false"],
  "Hardy-Weinberg principle",
  at="A", correct="(a), (b) and (c) only",
  wrong=["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(c) and (e) only"],
  why="The stem rules out further contact, so (d) cannot act, and (e) is not an accepted evolutionary factor; "
      "options containing either are wrong.", secs=55)

Z(EVO, "Evidences of evolution", A, ASR,
  AR("The thorn of Bougainvillea and the tendril of Cucurbita are homologous structures.",
     "Sweet potato (a root modification) and potato (a stem modification) are analogous structures."),
  "Homology and analogy in plants",
  "NCERT gives both as examples: thorn of Bougainvillea and tendril of Cucurbita represent homology (same origin, "
  "different functions - divergent evolution); sweet potato and potato are analogous (different origin, same "
  "function - convergent evolution). Both statements are true, but R is a separate example of analogy and says "
  "nothing about why the thorn and tendril are homologous.",
  ["A true: homology", "R true: analogy", "R does not explain A"],
  "Evidence for evolution", ans="B",
  why="Both statements are correct, so C and D are wrong; R concerns a different pair of organs and a different "
      "concept, so it cannot be the explanation of A (option A).", secs=40)

Z(EVO, "Natural selection", A, D,
  "Suppose that, in an industrial area of England, pollution is controlled, lichens grow again and the tree trunks "
  "become light-coloured once more. Using NCERT's explanation of industrial melanism, what would be expected in the "
  "moth population over many generations?",
  "Reversal of industrial melanism",
  "NCERT: the moths that are better camouflaged against the background are not picked out by predators and "
  "survive; in unpolluted areas with lichen-covered trunks, white-winged moths survive better, while dark moths "
  "are spotted easily. If the trunks become light again, selection favours white-winged moths, so their "
  "proportion rises again (no variant is completely wiped out).",
  ["Light trunks -> white moths camouflaged", "Dark moths easily seen by predators", "White-winged moths increase"],
  "Evidence for evolution (industrial melanism)",
  at="C", correct="White-winged moths would again increase in proportion, because dark moths would be spotted "
                  "more easily by predators",
  wrong=["Dark-winged moths would continue to increase, because dark colour once acquired cannot be lost",
         "All moths would become white within one generation because of the clean air",
         "Both types would stay in exactly the same proportion, because predators do not hunt by sight"],
  why="Selection depends on the current background, so the dark advantage disappears; change happens over "
      "generations, not instantly; NCERT's explanation rests precisely on predators spotting moths.", secs=55)

Z(EVO, "Adaptive radiation", A, MAT,
  ML(("observation", "evolutionary concept it illustrates"),
     ["Weeds become resistant after excessive use of herbicides, within a short time",
      "A placental wolf resembles the Tasmanian wolf (a marsupial)",
      "Finches with altered beaks arose from an original seed-eating form in the Galapagos",
      "Large, sudden variations appear in evening primrose"],
     ["Adaptive radiation", "Mutation (saltation)", "Evolution by anthropogenic action",
      "Convergent evolution"]),
  "Recognising evolutionary processes",
  "NCERT: excessive use of herbicides and pesticides has selected resistant varieties in a much lesser time scale "
  "- evolution by anthropogenic action; placental mammals resembling corresponding marsupials is convergent "
  "evolution; Darwin's finches radiating from a seed-eating ancestor are adaptive radiation; de Vries' evening "
  "primrose work led to the idea of mutation (single-step large mutation = saltation).",
  ["Herbicide resistance -> III", "Placental vs marsupial wolf -> IV", "Finches -> I", "Evening primrose -> II"],
  "Evidence for evolution; What is adaptive radiation?; Mechanism of evolution",
  at="D", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="Resemblance between unrelated placental and marsupial forms is convergence, while radiation from one "
      "ancestor (finches) is adaptive radiation; herbicide resistance is NCERT's anthropogenic example and the "
      "evening primrose is de Vries' mutation example. Each wrong code swaps one pair.", secs=50)


# ================================================================ Human Health and Disease (6/8/6)
# HHD numerical: each antibody molecule = 2 light + 2 heavy chains (H2L2) -> 5 molecules
n_ab = 5
assert n_ab * (2 + 2) == 20                                    # correct: 20 chains
assert n_ab * 2 == 10 and n_ab * 1 == 5 and n_ab * 8 == 40       # distractors: heavy only; one per molecule; double

Z(HHD, "Pathogens and diseases", B, D,
  "According to NCERT, which practice has been followed since time immemorial to achieve physical and mental "
  "health?",
  "Maintaining good health",
  "NCERT: balanced diet, personal hygiene and regular exercise are very important for maintaining good health. "
  "Yoga has been practised since time immemorial to achieve physical and mental health. Education and awareness "
  "about diseases also help.",
  ["Balanced diet, hygiene, exercise", "Yoga - since time immemorial - physical and mental health"],
  "Human Health and Disease (introduction)",
  at="A", correct="Yoga",
  wrong=["Self-medication with antibiotics", "Use of anabolic steroids", "Smoking in moderation"],
  why="NCERT warns against drug misuse, anabolic steroids and smoking; none of them is described as a practice "
      "for physical and mental health.", secs=20)

Z(HHD, "Pathogens and diseases", B, D,
  "Which of the following diseases is NOT caused by a bacterium?",
  "Bacterial and viral diseases",
  "NCERT: typhoid (Salmonella typhi), pneumonia (Streptococcus pneumoniae, Haemophilus influenzae), dysentery, "
  "plague and diphtheria are bacterial diseases. The common cold is caused by rhinoviruses, a group of viruses.",
  ["Bacterial: typhoid, pneumonia, dysentery, plague, diphtheria", "Common cold: rhinoviruses"],
  "Common diseases in humans",
  at="D", correct="Common cold",
  wrong=["Plague", "Diphtheria", "Dysentery"],
  why="Plague, diphtheria and dysentery are listed by NCERT among bacterial diseases.", secs=20)

Z(HHD, "Immunity and vaccines", B, D,
  "Virus-infected cells secrete proteins called interferons. According to NCERT, these proteins:",
  "Cytokine barriers of innate immunity",
  "NCERT: virus-infected cells secrete proteins called interferons, which protect non-infected cells from further "
  "viral infection. This is the cytokine barrier of innate immunity.",
  ["Interferons from virus-infected cells", "Protect non-infected cells from further viral infection"],
  "Immunity (innate immunity)",
  at="B", correct="Protect non-infected cells from further viral infection",
  wrong=["Destroy all bacteria in the blood", "Act as antibodies of the IgE type",
         "Cause the release of histamine from mast cells"],
  why="Interferons are non-specific cytokines aimed at viral spread; they are not antibodies, they do not kill all "
      "bacteria, and histamine release from mast cells is part of allergy.", secs=25)

Z(HHD, "Drug and alcohol abuse", B, D,
  "Cannabinoids are a group of chemicals that interact with cannabinoid receptors. According to NCERT, these "
  "receptors are present principally in the:",
  "Site of action of cannabinoids",
  "NCERT: cannabinoids are a group of chemicals which interact with cannabinoid receptors present principally in "
  "the brain. Natural cannabinoids are obtained from the inflorescences of Cannabis sativa.",
  ["Cannabinoids -> cannabinoid receptors", "Present principally in the brain"],
  "Drugs and alcohol abuse",
  at="D", correct="Brain",
  wrong=["Liver", "Kidneys", "Skin"],
  why="NCERT names the brain as the principal location of cannabinoid receptors; liver, kidney and skin are not "
      "mentioned.", secs=20)

Z(HHD, "Immunity and vaccines", B, NUM,
  "Each antibody molecule has the structure H2L2. How many polypeptide chains in all are present in 5 antibody "
  "molecules?",
  "Structure of an antibody molecule",
  "NCERT: each antibody molecule has four peptide chains - two small chains called light chains and two longer "
  "chains called heavy chains (H2L2). 5 molecules × 4 chains = 20 chains.",
  ["One antibody = 2 H + 2 L = 4 chains", "5 × 4 = 20"],
  "Immunity (acquired immunity)",
  at="C", correct="20",
  wrong=["10", "5", "40"],
  why="10 counts only the heavy (or only the light) chains; 5 counts one chain per molecule; 40 doubles the "
      "count, as if each molecule had eight chains.", secs=25, vb=RECOMPUTED)

Z(HHD, "Cancer", B, D,
  "Chemotherapeutic drugs are used to kill cancerous cells. According to NCERT, the majority of these drugs have "
  "side effects such as:",
  "Side effects of chemotherapy",
  "NCERT: several chemotherapeutic drugs are used to kill cancerous cells; some are specific for particular "
  "tumours. Majority of drugs have side effects like hair loss, anaemia, etc.",
  ["Chemotherapy kills cancer cells", "Side effects: hair loss, anaemia"],
  "Cancer (treatment)",
  at="A", correct="Hair loss and anaemia",
  wrong=["Increased height and muscle growth", "Improved immunity and resistance to all infections",
         "Formation of new teeth"],
  why="NCERT names hair loss and anaemia; the other options are not side effects of anti-cancer drugs.",
  secs=20)

Z(HHD, "Immunity and vaccines", I, ASR,
  AR("A child whose thymus fails to develop would have a very weak cell-mediated immune response.",
     "The thymus provides the micro-environment for the development and maturation of T-lymphocytes, which "
     "mediate cell-mediated immunity."),
  "Primary lymphoid organs and CMI",
  "NCERT: the thymus is a primary lymphoid organ that provides the micro-environment for the development and "
  "maturation of T-lymphocytes; the cell-mediated immune response (CMI) is mediated by T-lymphocytes. Without the "
  "thymus, mature T-cells are lacking, so CMI is weak - R explains A.",
  ["Thymus -> T-lymphocyte maturation", "T-lymphocytes -> CMI", "No thymus -> weak CMI"],
  "Immunity (lymphoid organs)", ans="A",
  why="Both statements are true and the role of the thymus in T-cell maturation is the direct cause of the weak "
      "CMI, so B, C and D are wrong.", secs=40)

Z(HHD, "Immunity and vaccines", I, STP,
  SP("Lymphocytes, like all other blood cells, are produced in the bone marrow.",
     "Lymph nodes are primary lymphoid organs, where immature lymphocytes differentiate into antigen-sensitive "
     "lymphocytes."),
  "Primary and secondary lymphoid organs",
  "NCERT: the bone marrow is the main lymphoid organ where all blood cells including lymphocytes are produced. "
  "The primary lymphoid organs are the bone marrow and thymus, where immature lymphocytes differentiate into "
  "antigen-sensitive lymphocytes; lymph nodes are secondary lymphoid organs that trap antigens. Statement I is "
  "true; Statement II is false.",
  ["Bone marrow produces all blood cells -> I true", "Lymph nodes = secondary lymphoid organs -> II false"],
  "Immunity (lymphoid organs)", ans="C",
  why="Statement II gives lymph nodes the role of primary lymphoid organs (bone marrow and thymus), so it is "
      "false; Statement I is true.", secs=40)

Z(HHD, "Immunity and vaccines", I, MAT,
  ML(("cell", "role in body defence"),
     ["Helper T-lymphocytes", "Mast cells", "Natural killer cells", "Memory B- and T-cells"],
     ["Part of the cellular barrier of innate immunity", "Recognise the same pathogen quickly on a later "
      "exposure", "Help B-cells to produce antibodies", "Release histamine and serotonin in allergic reactions"]),
  "Cells of the immune system",
  "NCERT: T-cells do not secrete antibodies but help B-cells produce them (helper T-cells); in allergy, chemicals "
  "like histamine and serotonin are released from mast cells; neutrophils, monocytes, natural killer cells and "
  "macrophages form the cellular barrier of innate immunity; vaccination generates memory B and T-cells that "
  "recognise the pathogen quickly on subsequent exposure.",
  ["Helper T -> III", "Mast cells -> IV", "NK cells -> I", "Memory cells -> II"],
  "Immunity; Allergies; Vaccination and immunisation",
  at="D", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
  why="Histamine release belongs to mast cells, not helper T-cells; NK cells are part of innate (non-specific) "
      "defence and have no memory; memory cells, not helper cells, give the quick later response.", secs=45)

Z(HHD, "Pathogens and diseases", I, STP,
  SP("Different species of Plasmodium, such as P. vivax, P. malariae and P. falciparum, are responsible for "
     "different types of malaria.",
     "The female Anopheles mosquito is the vector (transmitting agent) of malaria."),
  "Malaria: pathogen and vector",
  "NCERT: Plasmodium, a tiny protozoan, causes malaria; different species (P. vivax, P. malariae and P. "
  "falciparum) are responsible for different types of malaria, the malignant one being caused by P. falciparum. "
  "The female Anopheles mosquito is the vector. Both statements are true.",
  ["Three species, different malarias -> I true", "Female Anopheles = vector -> II true"],
  "Common diseases in humans (malaria)", ans="A",
  why="Both statements agree with NCERT, so options calling either of them false are wrong.", secs=35)

Z(HHD, "Pathogens and diseases", I, ASR,
  AR("Ringworm is caused by bacteria of the genus Trichophyton.",
     "Ringworms are generally acquired from soil or by using towels, clothes or even the comb of infected "
     "individuals."),
  "Ringworm",
  "NCERT: many fungi belonging to the genera Microsporum, Trichophyton and Epidermophyton are responsible for "
  "ringworms; Trichophyton is a fungus, not a bacterium, so A is false. Ringworms are generally acquired from soil "
  "or by using towels, clothes or even the comb of infected individuals, so R is true.",
  ["Trichophyton = fungus -> A false", "Mode of spread in R -> true"],
  "Common diseases in humans (ringworm)", ans="D",
  why="Since A is false, options A, B and C (which all call A true) are wrong.", secs=35)

Z(HHD, "Drug and alcohol abuse", I, STP,
  SP("Heroin is a depressant and slows down body functions.",
     "Morphine, from which heroin is obtained by acetylation, is extracted from the latex of the poppy plant "
     "Papaver somniferum."),
  "Opioids",
  "NCERT: heroin (smack), chemically diacetylmorphine, is obtained by acetylation of morphine, which is extracted "
  "from the latex of the poppy plant Papaver somniferum. Generally taken by snorting and injection, heroin is a "
  "depressant and slows down body functions. Both statements are true.",
  ["Heroin: depressant -> I true", "Morphine from poppy latex; heroin = acetylated morphine -> II true"],
  "Drugs and alcohol abuse", ans="A",
  why="Both statements are NCERT facts; calling heroin a stimulant or naming another plant would be wrong, so "
      "options declaring either statement false are wrong.", secs=35)

Z(HHD, "HIV and AIDS", I, MUL,
  MS("Which of the following statements about HIV infection are correct?",
     ["After entering a macrophage, the viral RNA genome is replicated to form viral DNA with the help of reverse "
      "transcriptase.",
      "The viral DNA gets incorporated into the host cell's DNA.",
      "HIV also enters helper T-lymphocytes, where it replicates and produces progeny viruses.",
      "HIV infection leads to a progressive increase in the number of helper T-lymphocytes.",
      "As the infection progresses, the person becomes unable to fight even infections that could otherwise "
      "have been overcome."]),
  "Course of HIV infection",
  "NCERT: after entering the body, HIV enters macrophages, where its RNA genome is replicated to form viral DNA by "
  "reverse transcriptase; the viral DNA gets incorporated into the host DNA and directs the infected cells to "
  "produce virus particles. HIV enters helper T-lymphocytes (TH), replicates and produces progeny viruses, which "
  "attack other helper T-cells; the number of helper T-cells decreases progressively, and the person becomes "
  "immunodeficient and unable to protect against infections (e.g. Mycobacterium, Toxoplasma).",
  ["(a), (b) true: reverse transcription, integration", "(c) true: helper T-cells infected",
   "(d) false: helper T-cells decrease", "(e) true: immunodeficiency"],
  "AIDS",
  at="B", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"],
  why="Statement (d) reverses NCERT - helper T-lymphocytes fall progressively - so options containing (d) are "
      "wrong.", secs=55)

Z(HHD, "Pathogens and diseases", I, MAT,
  ML(("disease", "type of pathogen"),
     ["Common cold", "Pneumonia", "Malaria", "Filariasis"],
     ["Protozoan", "Helminth (worm)", "Virus", "Bacterium"]),
  "Pathogen groups",
  "NCERT: common cold - rhinoviruses (virus); pneumonia - Streptococcus pneumoniae and Haemophilus influenzae "
  "(bacteria); malaria - Plasmodium, a tiny protozoan; filariasis - Wuchereria (W. bancrofti and W. malayi), "
  "filarial worms (helminths).",
  ["Common cold -> III", "Pneumonia -> IV", "Malaria -> I", "Filariasis -> II"],
  "Common diseases in humans",
  at="A", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "III", "B": "I", "C": "IV", "D": "II"}]),
  why="Rhinoviruses are viruses and pneumonia is bacterial; Plasmodium is a protozoan while Wuchereria is a worm. "
      "Each wrong code swaps one of these pairs.", secs=40)

Z(HHD, "Immunity and vaccines", A, MUL,
  MS("In which of the following situations does the person develop ACTIVE immunity?",
     ["A child is given a vaccine containing inactivated or weakened pathogens.",
      "A person recovers from a natural infection by a pathogen.",
      "A new-born baby receives IgA antibodies through colostrum.",
      "A person bitten by a snake receives an injection of preformed antibodies against the venom.",
      "A person is vaccinated with hepatitis B vaccine produced from yeast."]),
  "Active versus passive immunity",
  "NCERT: when a host is exposed to antigens, which may be living or dead microbes or other proteins, antibodies "
  "are produced in the host body - active immunity; it can be induced naturally during infection or deliberately "
  "by immunisation (any vaccine, including the recombinant hepatitis B vaccine from yeast, which supplies "
  "antigenic proteins). When ready-made antibodies are given (colostrum IgA, antivenom), it is passive immunity.",
  ["(a), (e): vaccine antigens -> own antibodies -> active", "(b): natural infection -> active",
   "(c), (d): ready-made antibodies -> passive"],
  "Immunity (active and passive immunity)",
  at="C", correct="(a), (b) and (e) only",
  wrong=["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"],
  why="(c) and (d) supply preformed antibodies, which is passive immunity, so options containing them are wrong; "
      "the recombinant hepatitis B vaccine still provides antigens, so it gives active immunity.", secs=55)

Z(HHD, "Immunity and vaccines", A, ASR,
  AR("When a person meets the same pathogen a second time, the antibody response is much quicker and more "
     "intense than on the first encounter.",
     "The first encounter with the pathogen leaves memory B- and T-cells that recognise it quickly on subsequent "
     "exposure."),
  "Primary and secondary (anamnestic) response",
  "NCERT: our body, on first encounter with a pathogen, produces a primary response of low intensity; a "
  "subsequent encounter with the same pathogen elicits a highly intensified secondary or anamnestic response, "
  "because our body appears to have memory of the first encounter (memory B and T-cells). R directly explains A.",
  ["Primary response: low intensity", "Memory B and T-cells formed", "Second encounter: highly intensified -> "
   "R explains A"],
  "Immunity (acquired immunity); Vaccination and immunisation", ans="A",
  why="Both statements are true and the memory cells are the reason for the stronger secondary response, so "
      "B, C and D are wrong.", secs=40)

Z(HHD, "Pathogens and diseases", A, D,
  "A female Anopheles mosquito bites a person in whom Plasmodium is still multiplying only within the liver cells "
  "and has not yet attacked the red blood cells. Why is the mosquito unlikely to pick up an infection that can "
  "later be passed on?",
  "Where Plasmodium gametocytes develop",
  "NCERT: sporozoites enter the human, multiply in liver cells and then attack red blood cells; the sexual stages "
  "(gametocytes) develop in the red blood cells. When a female Anopheles bites an infected person, these "
  "gametocytes enter the mosquito, where fertilisation and development take place. If the parasites are still "
  "only in the liver, there are no gametocytes in the blood to be picked up.",
  ["Liver: asexual multiplication", "Gametocytes develop only in RBCs", "No RBC stage -> nothing for the "
   "mosquito to take up"],
  "Common diseases in humans (malaria)",
  at="B", correct="Gametocytes, the stages that infect the mosquito, develop only in red blood cells",
  wrong=["Sporozoites are found only in the human blood at this stage",
         "Fertilisation of Plasmodium gametes takes place in the human liver",
         "Only male mosquitoes can pick up Plasmodium from humans"],
  why="Sporozoites are the stage injected by the mosquito, not taken up by it; fertilisation happens in the "
      "mosquito, not the human liver; NCERT names the female Anopheles as the vector.", secs=55)

Z(HHD, "Immunity and vaccines", A, D,
  "Which of the following shows the correct sequence of events in an allergic reaction to pollen?",
  "Mechanism of allergy",
  "NCERT: allergy is the exaggerated response of the immune system to certain antigens (allergens) in the "
  "environment, such as pollen; the antibodies produced are of the IgE type; allergic reactions are due to the "
  "release of chemicals like histamine and serotonin from the mast cells, causing symptoms such as sneezing, "
  "watery eyes, running nose and difficulty in breathing.",
  ["Pollen (allergen) enters", "IgE antibodies produced", "Mast cells release histamine and serotonin",
   "Symptoms"],
  "Allergies",
  at="D", correct="Exposure to pollen -> production of IgE antibodies -> release of histamine and serotonin "
                  "from mast cells -> sneezing, watery eyes and running nose",
  wrong=["Exposure to pollen -> release of interferons by infected cells -> production of IgA -> sneezing",
         "Exposure to pollen -> attack on self-cells by the immune system -> release of histamine -> joint pain",
         "Release of histamine from mast cells -> exposure to pollen -> production of IgG -> sneezing"],
  why="Interferons come from virus-infected cells and allergy involves IgE, not IgA or IgG; attack on self-cells "
      "is auto-immunity; histamine release cannot come before exposure to the allergen.", secs=50)

Z(HHD, "Drug and alcohol abuse", A, STP,
  SP("Misuse of anabolic steroids by females can cause enlargement of the clitoris and deepening of the voice.",
     "Misuse of anabolic steroids by males increases sperm production and the size of the testicles."),
  "Side effects of anabolic steroids",
  "NCERT: in females, side effects of anabolic steroids include masculinisation (features like males), increased "
  "aggressiveness, mood swings, depression, abnormal menstrual cycles, excessive hair growth on face and body, "
  "enlargement of clitoris and deepening of voice. In males, they include acne, increased aggressiveness, mood "
  "swings, depression, reduction of size of the testicles, decreased sperm production, potential for kidney and "
  "liver dysfunction, breast enlargement and premature baldness. Statement I is true; Statement II is false.",
  ["Females: enlargement of clitoris, deepening of voice -> I true",
   "Males: smaller testicles, decreased sperm production -> II false"],
  "Drugs and alcohol abuse", ans="C",
  why="Statement II reverses NCERT's effects in males (testicles shrink and sperm production falls), so it is "
      "false; Statement I is true.", secs=45)

Z(HHD, "Immunity and vaccines", A, MAT,
  ML(("immune phenomenon", "best description"),
     ["Graft rejection", "Antibodies present in the blood", "Allergy", "Rheumatoid arthritis"],
     ["Exaggerated response to environmental antigens, with IgE antibodies", "Body attacks self-cells "
      "(auto-immune disease)", "Cell-mediated immunity by T-lymphocytes", "Humoral immune response by "
      "B-lymphocytes"]),
  "Kinds of immune responses",
  "NCERT: cell-mediated immunity (T-lymphocytes) is responsible for graft rejection; antibodies produced by "
  "B-lymphocytes are found in the blood, so this is the humoral immune response; allergy is the exaggerated "
  "response to certain environmental antigens, with IgE antibodies; rheumatoid arthritis is an auto-immune "
  "disease in which the body attacks self-cells.",
  ["Graft rejection -> III", "Blood antibodies -> IV", "Allergy -> I", "Rheumatoid arthritis -> II"],
  "Immunity; Allergies; Auto immunity",
  at="B", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "IV", "B": "III", "C": "I", "D": "II"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"},
                  {"A": "I", "B": "IV", "C": "III", "D": "II"}]),
  why="Graft rejection is cell-mediated, not humoral; allergy (environmental antigens) must not be confused with "
      "auto-immunity (self-cells). Each wrong code swaps one of these pairs.", secs=45)


# ================================================================ Biotechnology: Principles and Processes (5/7/5)
Z(BPP, "Bioreactors and downstream processing", B, D,
  "The European Federation of Biotechnology (EFB) has given a definition of biotechnology that encompasses both "
  "traditional views and modern molecular biotechnology. According to it, biotechnology is:",
  "Definition of biotechnology",
  "NCERT: the EFB defines biotechnology as 'the integration of natural science and organisms, cells, parts "
  "thereof, and molecular analogues for products and services'.",
  ["EFB: integration of natural science and organisms, cells, parts thereof, molecular analogues",
   "For products and services"],
  "Principles of biotechnology",
  at="B", correct="The integration of natural science and organisms, cells, parts thereof, and molecular analogues "
                  "for products and services",
  wrong=["Only the use of chemical fertilisers and pesticides in agriculture",
         "Only the making of curd, bread and wine by traditional methods",
         "The study of fossils to trace the history of life"],
  why="The EFB definition is broad, covering both traditional and modern molecular biotechnology; fertiliser use, "
      "traditional fermentation alone and fossil study are not the definition.", secs=25)

Z(BPP, "PCR and gel electrophoresis", B, D,
  "During the isolation of DNA, purified DNA precipitates on adding chilled ethanol and can be seen as a "
  "collection of fine threads in the suspension. These threads can be removed by:",
  "Isolating DNA",
  "NCERT: purified DNA ultimately precipitates out after the addition of chilled ethanol; this can be seen as a "
  "collection of fine threads in the suspension, and the DNA that separates out can be removed by spooling.",
  ["Chilled ethanol -> DNA precipitates as fine threads", "Removed by spooling"],
  "Processes of recombinant DNA technology (isolation of DNA)",
  at="A", correct="Spooling",
  wrong=["Elution", "Ligation", "Annealing"],
  why="Elution extracts DNA from a gel piece after electrophoresis; ligation joins DNA fragments; annealing is the "
      "binding of primers in PCR.", secs=20)

Z(BPP, "Bioreactors and downstream processing", B, D,
  "According to NCERT, the most commonly used bioreactors are of the:",
  "Types of bioreactors",
  "NCERT: the most commonly used bioreactors are of the stirring type. A stirred-tank reactor is usually "
  "cylindrical or has a curved base to facilitate mixing; the stirrer facilitates even mixing and oxygen "
  "availability.",
  ["Most common: stirring type", "Stirred-tank: cylindrical or curved base"],
  "Processes of recombinant DNA technology (bioreactors)",
  at="D", correct="Stirring type",
  wrong=["Rectangular flat-bottomed type without any mixing", "Open pond type",
         "Type that works only at volumes below 1 litre"],
  why="NCERT stresses mixing, and bioreactors process large volumes (100-1000 litres), so unmixed, open-pond or "
      "sub-litre vessels are not the commonly used kind.", secs=20)

Z(BPP, "Bioreactors and downstream processing", B, D,
  "Making curd, bread or wine are microbe-mediated processes that could be thought of as a form of biotechnology. "
  "According to NCERT, in the restricted sense in which the term is used today, biotechnology refers to processes "
  "that:",
  "Traditional versus modern biotechnology",
  "NCERT: biotechnology deals with techniques of using live organisms or enzymes from organisms to produce "
  "products and processes useful to humans; curd, bread and wine making could be thought of as biotechnology. "
  "However, it is used in a restricted sense today, to refer to such processes which use genetically modified "
  "organisms to achieve the same on a larger scale.",
  ["Broad sense: live organisms/enzymes for useful products", "Restricted sense today: GMOs on a larger scale"],
  "Biotechnology: Principles and Processes (introduction)",
  at="B", correct="Use genetically modified organisms to achieve such products on a larger scale",
  wrong=["Use only chemical catalysts and no living cells", "Are carried out only in households",
         "Use only wild-type microbes without any genetic change"],
  why="The restricted modern meaning is defined by the use of genetically modified organisms at a larger scale; "
      "the other options exclude living or modified organisms, or limit the scale.", secs=30)

Z(BPP, "Cloning vectors", B, D,
  "Agrobacterium tumefaciens, a pathogen of several dicot plants, delivers a piece of DNA (T-DNA) that transforms "
  "normal plant cells into tumour cells. According to NCERT, the T-DNA also directs these tumour cells to:",
  "Natural genetic engineering by Agrobacterium",
  "NCERT: Agrobacterium tumefaciens is able to deliver a piece of DNA known as T-DNA to transform normal plant "
  "cells into a tumour and direct these tumour cells to produce the chemicals required by the pathogen. Its Ti "
  "plasmid has now been modified into a non-pathogenic cloning vector.",
  ["T-DNA -> tumour", "Tumour cells make chemicals required by the pathogen"],
  "Cloning vectors",
  at="C", correct="Produce the chemicals required by the pathogen",
  wrong=["Produce antibodies against the bacterium", "Undergo meiosis to form gametes",
         "Secrete restriction enzymes that destroy the bacterium"],
  why="Plants do not make antibodies; T-DNA does not cause meiosis; NCERT says the tumour cells serve the "
      "pathogen, not destroy it.", secs=25)

Z(BPP, "Cloning vectors", I, ASR,
  AR("Genetic engineering can introduce a desirable gene into a target organism without also introducing "
     "undesirable genes.",
     "In genetic engineering, the desired gene is first isolated (cut out with a restriction enzyme), linked to a "
     "vector and then transferred, so only that piece of DNA is introduced into the host."),
  "Why genetic engineering?",
  "NCERT: traditional hybridisation very often leads to inclusion and multiplication of undesirable genes along "
  "with the desired genes, whereas the techniques of genetic engineering (creation of recombinant DNA, gene "
  "cloning and gene transfer) allow us to isolate and introduce only one or a set of desirable genes without "
  "introducing undesirable genes. Because the gene is isolated and carried alone by a vector, nothing else enters "
  "the host - R is the direct cause of A.",
  ["Gene isolated with restriction enzyme", "Linked to vector and transferred alone",
   "Only the desired DNA enters -> R explains A"],
  "Principles of biotechnology", ans="A",
  why="Both statements are true and the isolation and vector-borne transfer of the single gene in R is exactly "
      "why no undesirable genes enter (A), so B, C and D are wrong.", secs=40)

Z(BPP, "Cloning vectors", I, D,
  "A gene of interest is joined to a DNA fragment that has no origin of replication (ori) and is introduced into "
  "E. coli. It does not integrate into the host chromosome. What is the most likely result?",
  "Role of the origin of replication",
  "NCERT: ori is the sequence from where replication starts, and any piece of DNA linked to it can be made to "
  "replicate within the host cells. A piece of alien DNA without it usually cannot multiply in the progeny cells "
  "(unless it integrates into the genome). So the gene is not copied and is diluted out as the bacteria divide.",
  ["ori = start of replication", "No ori, no integration -> no replication", "Gene lost as cells divide"],
  "Cloning vectors; Tools of recombinant DNA technology",
  at="B", correct="The gene is not replicated, so it is not passed on to the progeny cells as they divide",
  wrong=["The gene is replicated to a very high copy number",
         "The gene is cut out by DNA ligase",
         "The bacteria become resistant to all antibiotics"],
  why="High copy number needs an ori that supports it; ligase joins, not cuts, DNA; nothing in the stem supplies "
      "antibiotic resistance genes.", secs=45)

Z(BPP, "PCR and gel electrophoresis", I, MUL,
  MS("A researcher wants to isolate pure DNA from a fungus. Which of the following should be used in the "
     "procedure?",
     ["Chitinase, to break open the cells", "Ribonuclease, to remove RNA", "Protease, to remove proteins",
      "Cellulase, as the essential enzyme to break the fungal cell wall", "Chilled ethanol, to precipitate the DNA"]),
  "Isolation of DNA from different cells",
  "NCERT: DNA is released by treating the cells with lysozyme (bacteria), cellulase (plant cells) or chitinase "
  "(fungus). RNA is removed by ribonuclease and proteins by protease; purified DNA precipitates on adding chilled "
  "ethanol. For a fungus, chitinase - not cellulase - is the enzyme NCERT names.",
  ["(a) chitinase: fungus", "(b) RNase, (c) protease", "(d) cellulase is for plant cells -> not",
   "(e) chilled ethanol"],
  "Processes of recombinant DNA technology (isolation of DNA)",
  at="D", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a) and (e) only"],
  why="Cellulase (d) is NCERT's enzyme for plant cells, so options with (d) are wrong; '(a) and (e) only' leaves "
      "out the removal of RNA and proteins.", secs=50)

Z(BPP, "Competent hosts and transformation", I, MAT,
  ML(("vector", "feature or use"),
     ["Plasmid pBR322", "Ti plasmid of Agrobacterium tumefaciens", "Retrovirus", "Bacteriophage"],
     ["Disarmed and used to deliver desirable genes into animal cells",
      "Has a very high number of copies of its genome within bacterial cells",
      "E. coli cloning vector carrying ampicillin and tetracycline resistance genes",
      "Modified into a non-pathogenic vector for transferring genes into dicot plant cells"]),
  "Vectors and their uses",
  "NCERT: pBR322 is an E. coli cloning vector; the Ti plasmid of Agrobacterium has been modified into a "
  "non-pathogenic vector for plants; retroviruses have been disarmed and are used to deliver desirable genes into "
  "animal cells; bacteriophages, viruses of bacteria, have very high copy numbers in bacterial cells.",
  ["pBR322 -> III", "Ti plasmid -> IV", "Retrovirus -> I", "Bacteriophage -> II"],
  "Cloning vectors",
  at="A", match=({"A": "III", "B": "IV", "C": "I", "D": "II"},
                 [{"A": "III", "B": "I", "C": "IV", "D": "II"},
                  {"A": "II", "B": "IV", "C": "I", "D": "III"},
                  {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
  why="Agrobacterium is the plant vector and retroviruses the animal vector, so these must not be swapped; the "
      "very high copy number is NCERT's point about bacteriophages, while ampR and tetR identify pBR322.", secs=40)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("In order to cut DNA with restriction enzymes, the DNA needs to be in a pure form, free from other "
     "macromolecules.",
     "Restriction enzymes digest proteins and RNA as readily as they digest DNA."),
  "Purity of DNA before restriction digestion",
  "NCERT: in order to cut the DNA with restriction enzymes, it needs to be in pure form, free from other "
  "macromolecules; hence RNA and proteins are removed by ribonuclease and protease. Restriction enzymes are "
  "nucleases that recognise specific DNA sequences; they do not digest proteins. A is true; R is false.",
  ["A: NCERT statement -> true", "Restriction enzymes = DNA-cutting nucleases -> R false"],
  "Processes of recombinant DNA technology", ans="C",
  why="R misdescribes restriction enzymes, so options calling R true are wrong; A is NCERT's statement.",
  secs=35)

Z(BPP, "PCR and gel electrophoresis", I, D,
  "A student runs a restriction digest on an agarose gel but does not stain it with ethidium bromide. When the gel "
  "is looked at in ordinary light, no DNA bands are seen. The most likely reason is that:",
  "Visualising DNA after electrophoresis",
  "NCERT: the separated DNA fragments can be visualised only after staining the DNA with a compound known as "
  "ethidium bromide followed by exposure to UV radiation; pure DNA fragments cannot be seen in visible light "
  "without staining. They then appear as bright orange coloured bands.",
  ["DNA bands invisible in plain light", "Need ethidium bromide + UV", "Then: bright orange bands"],
  "Processes of recombinant DNA technology (separation and isolation of DNA fragments)",
  at="C", correct="DNA fragments can be seen only after staining with ethidium bromide and exposure to UV light",
  wrong=["DNA fragments always run off the gel towards the cathode", "Restriction enzymes destroy all DNA",
         "Agarose dissolves DNA completely"],
  why="DNA is negatively charged and moves towards the anode, not off towards the cathode; restriction enzymes cut "
      "DNA into fragments rather than destroying it; agarose only acts as a sieve.", secs=40)

Z(BPP, "Restriction enzymes", I, ASR,
  AR("EcoRI produces DNA fragments with sticky ends.",
     "EcoRI was isolated from Escherichia coli strain RY 13."),
  "Sticky ends and naming of restriction enzymes",
  "NCERT: restriction enzymes such as EcoRI cut the DNA a little away from the centre of the palindrome site, "
  "but between the same two bases on the opposite strands, leaving single-stranded portions (sticky ends). In "
  "EcoRI, E comes from Escherichia, co from coli and R from strain RY 13. Both are true, but the source strain "
  "has nothing to do with the way the enzyme cuts.",
  ["A true: staggered cut -> sticky ends", "R true: naming convention", "Source strain does not explain sticky "
   "ends"],
  "Tools of recombinant DNA technology (restriction enzymes)", ans="B",
  why="Both statements are true, so C and D are wrong; the reason for sticky ends is the staggered cut, not the "
      "bacterial strain, so A is wrong.", secs=35)

Z(BPP, "Cloning vectors", A, MUL,
  MS("Foreign DNA is inserted into the coding sequence of β-galactosidase in a vector that also carries an "
     "ampicillin resistance gene. E. coli is transformed and plated on a medium containing ampicillin and a "
     "chromogenic substrate. Which of the following are correct?",
     ["Bacteria that did not take up any vector do not grow.",
      "Transformants carrying the vector without the insert give blue coloured colonies.",
      "Colonies carrying the recombinant DNA do not produce any colour.",
      "Colonies carrying the recombinant DNA give a blue colour.",
      "Both recombinant and non-recombinant transformants can grow on this medium."]),
  "Combining an antibiotic marker with insertional inactivation",
  "NCERT: normal E. coli cells do not carry resistance against ampicillin, so only transformants grow on "
  "ampicillin (a true, e true - the ampicillin gene is intact in both). Recombinant DNA inserted within the "
  "β-galactosidase coding sequence inactivates the enzyme (insertional inactivation); with a chromogenic "
  "substrate, colonies without the insert give blue colour (b true) and those with the insert do not produce "
  "any colour (c true, d false).",
  ["(a) no ampR -> no growth", "(b) intact β-gal -> blue", "(c) inactivated β-gal -> no colour",
   "(d) false", "(e) ampR intact in both kinds of transformant"],
  "Cloning vectors (selectable marker, insertional inactivation)",
  at="B", correct="(a), (b), (c) and (e) only",
  wrong=["(a), (b) and (d) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
  why="Recombinants are the colourless colonies, so any option containing (d) is wrong.", secs=60)

Z(BPP, "Cloning vectors", A, MUL,
  MS("Which of the following features would make a plasmid a POOR cloning vector?",
     ["Many recognition sites for the restriction enzyme that is to be used",
      "No selectable marker",
      "No origin of replication",
      "A single recognition site for the restriction enzyme, located within a selectable marker gene",
      "An origin of replication that supports a high copy number"]),
  "Features required in a cloning vector",
  "NCERT: a vector needs an ori (to replicate; it also controls copy number - high copy numbers are useful when "
  "many copies are needed), a selectable marker (to distinguish transformants), and very few, preferably single, "
  "recognition sites for the commonly used restriction enzymes - more than one site generates several fragments "
  "and complicates cloning. A single site within a marker gene even allows insertional inactivation.",
  ["(a) many sites -> fragments -> poor", "(b) no marker -> cannot select -> poor",
   "(c) no ori -> no replication -> poor", "(d), (e) desirable features"],
  "Cloning vectors",
  at="C", correct="(a), (b) and (c) only",
  wrong=["(a), (d) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
  why="(d) and (e) are features NCERT recommends, so options listing them as making a poor vector are wrong.",
  secs=50)

Z(BPP, "Restriction enzymes", A, STP,
  SP("Once a restriction endonuclease finds its specific recognition sequence, it binds to the DNA and cuts each "
     "of the two strands of the double helix at specific points in their sugar-phosphate backbones.",
     "A restriction endonuclease separates the two strands of DNA only by breaking the hydrogen bonds between the "
     "complementary bases."),
  "How restriction endonucleases cut DNA",
  "NCERT: each restriction endonuclease functions by 'inspecting' the length of a DNA sequence; once it finds its "
  "specific recognition sequence, it binds to the DNA and cuts each of the two strands of the double helix at "
  "specific points in their sugar-phosphate backbones. It cuts the backbone (phosphodiester linkages); merely "
  "breaking hydrogen bonds would only separate strands, as in denaturation. Statement I is true; II is false.",
  ["Cut is in the sugar-phosphate backbone -> I true", "Not merely hydrogen bonds -> II false"],
  "Tools of recombinant DNA technology (restriction enzymes)", ans="C",
  why="Statement II describes strand separation (like heat denaturation in PCR), not cutting, so it is false; "
      "Statement I is NCERT's description.", secs=45)

Z(BPP, "Cloning vectors", A, MAT,
  ML(("feature of pBR322", "description"),
     ["ori", "rop", "BamHI site", "PstI site"],
     ["Lies within the ampicillin resistance gene", "Codes for proteins involved in the replication of the "
      "plasmid", "Sequence from where replication starts; also controls the copy number of linked DNA",
      "Lies within the tetracycline resistance gene"]),
  "Map of pBR322",
  "NCERT (Fig. of pBR322 and text): ori is the sequence where replication starts and it controls the copy number; "
  "rop codes for the proteins involved in the replication of the plasmid; the BamHI site lies in the tetracycline "
  "resistance gene (insertion there inactivates tetR); the PstI (and PvuI) site lies in the ampicillin resistance "
  "gene.",
  ["ori -> III", "rop -> II", "BamHI -> IV", "PstI -> I"],
  "Cloning vectors",
  at="D", match=({"A": "III", "B": "II", "C": "IV", "D": "I"},
                 [{"A": "II", "B": "III", "C": "IV", "D": "I"},
                  {"A": "III", "B": "II", "C": "I", "D": "IV"},
                  {"A": "I", "B": "II", "C": "IV", "D": "III"}]),
  why="ori and rop both relate to replication but ori is the start site while rop codes proteins; BamHI is in "
      "tetR and PstI in ampR, so swapping them is wrong.", secs=45)

Z(BPP, "Competent hosts and transformation", A, D,
  "Bacterial cells are treated with calcium ions and incubated with recombinant DNA on ice, but the brief "
  "transfer to 42 °C is skipped and the cells are kept on ice throughout. What is the most likely effect?",
  "Heat shock in transformation",
  "NCERT: since DNA is hydrophilic, it cannot pass through cell membranes; cells are made competent with divalent "
  "cations such as calcium. The rDNA is then forced into the cells by incubating them with rDNA on ice, followed "
  "by placing them briefly at 42 °C (heat shock), and then back on ice - this enables the bacteria to take up "
  "the rDNA. Skipping the heat shock means far fewer cells take up the rDNA.",
  ["Ca2+ makes cells competent", "Heat shock at 42 °C forces rDNA in", "No heat shock -> poor uptake"],
  "Processes of recombinant DNA technology (insertion of rDNA into host)",
  at="A", correct="Far fewer bacteria take up the recombinant DNA, so very few transformants are obtained",
  wrong=["The DNA is cut into fragments by the calcium ions",
         "All bacteria take up the DNA even better, because cold increases pore size",
         "The recombinant DNA becomes double the size by ligation"],
  why="Calcium ions make cells competent, they do not cut DNA; NCERT says the heat shock is what enables uptake; "
      "no ligation occurs in this step.", secs=45)


# ================================================================ Biotechnology and its Applications (5/6/5)
Z(BTA, "Bt crops and RNAi", B, D,
  "NCERT lists the main areas in which biotechnology has been applied. Which of the following is NOT one of them?",
  "Areas of application of biotechnology",
  "NCERT: biotechnology has a wide range of applications - therapeutics, diagnostics, genetically modified crops "
  "for agriculture, processed food, bioremediation, waste treatment and energy production. Weather forecasting "
  "is not a biotechnological application.",
  ["NCERT list: therapeutics, diagnostics, GM crops, processed food, bioremediation, waste treatment, energy "
   "production"],
  "Biotechnology and its Applications (introduction)",
  at="D", correct="Weather forecasting",
  wrong=["Bioremediation", "Waste treatment", "Energy production"],
  why="Bioremediation, waste treatment and energy production are all in NCERT's list of applications.", secs=20)

Z(BTA, "Bt crops and RNAi", B, D,
  "According to NCERT, tailor-made genetically modified plants can be used to supply alternative resources to "
  "industries in the form of:",
  "Uses of GM plants",
  "NCERT: genetic modification has been used to create tailor-made plants to supply alternative resources to "
  "industries, in the form of starches, fuels and pharmaceuticals.",
  ["Tailor-made plants -> starches, fuels, pharmaceuticals"],
  "Biotechnological applications in agriculture",
  at="B", correct="Starches, fuels and pharmaceuticals",
  wrong=["Fertilisers, pesticides and herbicides", "Metals, plastics and glass", "Antibodies, vaccines and blood"],
  why="NCERT names starches, fuels and pharmaceuticals; GM plants are meant to reduce reliance on pesticides, and "
      "metals, glass, antibodies and blood are not plant products named here.", secs=20)

Z(BTA, "Human insulin", B, D,
  "A diabetic patient using insulin extracted from the pancreas of slaughtered pigs develops an allergic "
  "reaction. Which kind of insulin is the better option for this patient, according to NCERT?",
  "Advantage of recombinant human insulin",
  "NCERT: insulin from slaughtered cattle and pigs caused some patients to develop allergy or other reactions to "
  "the foreign protein. It is now possible to produce human insulin using bacteria (rDNA technology); recombinant "
  "therapeutics do not induce unwanted immunological responses, as is common with products from non-human "
  "sources.",
  ["Animal insulin = foreign protein -> allergy", "Human insulin made by rDNA in bacteria -> no unwanted immune "
   "response"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="A", correct="Human insulin produced by recombinant DNA technology",
  wrong=["Insulin extracted from the pancreas of slaughtered cattle", "Insulin containing the C peptide",
         "Glucagon from the α-cells of the islets"],
  why="Cattle insulin is also a foreign protein; mature functional insulin lacks the C peptide; glucagon raises "
      "blood glucose and cannot replace insulin.", secs=30)

Z(BTA, "Bt crops and RNAi", B, D,
  "In producing Bt cotton, which organism supplied the toxin genes and which organism expresses them?",
  "Source and host in Bt cotton",
  "NCERT: Bt toxin is produced by the bacterium Bacillus thuringiensis (Bt). The Bt toxin gene has been cloned "
  "from the bacteria and expressed in plants to provide resistance to insects - in Bt cotton, the cotton plant "
  "expresses it.",
  ["Source: Bacillus thuringiensis", "Expressed in: cotton plant"],
  "Biotechnological applications in agriculture",
  at="C", correct="Genes from the bacterium Bacillus thuringiensis are expressed in the cotton plant",
  wrong=["Genes from the cotton plant are expressed in Bacillus thuringiensis",
         "Genes from the nematode Meloidegyne incognitia are expressed in the cotton plant",
         "Genes from Agrobacterium tumefaciens are expressed in the cotton bollworm"],
  why="The first option reverses source and host; nematode-specific genes were used for RNAi in tobacco; "
      "Agrobacterium is a vector for plants, and the bollworm is the pest, not the host of the toxin genes.",
  secs=25)

Z(BTA, "Bt crops and RNAi", B, ASR,
  AR("Bt cotton plants are protected against cotton bollworms.",
     "Bt cotton expresses the Bt toxin genes cryIAc and cryIIAb, whose proteins control the cotton bollworms."),
  "Bt cotton and cry genes",
  "NCERT: the Bt toxin is coded by genes named cry; the proteins encoded by the genes cryIAc and cryIIAb control "
  "the cotton bollworms. Expressing these genes in cotton gives Bt cotton, which resists bollworms - R explains A.",
  ["cryIAc, cryIIAb proteins control bollworms", "Expressed in cotton -> protection", "R explains A"],
  "Biotechnological applications in agriculture", ans="A",
  why="Both statements are true and R names the very genes that give the protection, so B, C and D are wrong.",
  secs=30)

Z(BTA, "Gene therapy", I, D,
  "Which of the following shows the correct sequence in the gene therapy given for adenosine deaminase (ADA) "
  "deficiency, as described in NCERT?",
  "Steps in ADA gene therapy",
  "NCERT: lymphocytes from the blood of the patient are grown in a culture outside the body; a functional ADA "
  "cDNA is then introduced into these lymphocytes using a retroviral vector; the lymphocytes are subsequently "
  "returned to the patient. As these cells are not immortal, the patient requires periodic infusion of such "
  "genetically engineered lymphocytes.",
  ["Take lymphocytes, culture outside body", "Insert functional ADA cDNA by retroviral vector",
   "Return lymphocytes to patient", "Repeat periodically"],
  "Biotechnological applications in medicine (gene therapy)",
  at="B", correct="Lymphocytes cultured outside the body -> functional ADA cDNA introduced with a retroviral "
                  "vector -> lymphocytes returned to the patient -> infusions repeated periodically",
  wrong=["Functional ADA enzyme injected -> lymphocytes become immortal -> single treatment cures the patient",
         "Lymphocytes cultured outside the body -> ADA cDNA introduced with Agrobacterium -> lymphocytes returned "
         "-> permanent cure",
         "Bone marrow cells removed -> cry gene introduced -> cells returned -> periodic infusions"],
  why="Enzyme injection is enzyme replacement therapy, not gene therapy, and lymphocytes are not immortal; "
      "Agrobacterium is a plant vector; cry genes code Bt toxins, not ADA.", secs=45)

Z(BTA, "Bt crops and RNAi", I, MAT,
  ML(("Bt toxin target", "example given in NCERT"),
     ["Lepidopterans", "Coleopterans", "Dipterans", "Protein encoded by cryIAb"],
     ["Corn borer", "Beetles", "Flies and mosquitoes", "Tobacco budworm and armyworm"]),
  "Insects controlled by Bt toxins",
  "NCERT: there are strains of Bacillus thuringiensis producing proteins that kill insects such as lepidopterans "
  "(tobacco budworm, armyworm), coleopterans (beetles) and dipterans (flies, mosquitoes). The protein encoded by "
  "cryIAb controls corn borer.",
  ["Lepidopterans -> IV", "Coleopterans -> II", "Dipterans -> III", "cryIAb -> I"],
  "Biotechnological applications in agriculture",
  at="C", match=({"A": "IV", "B": "II", "C": "III", "D": "I"},
                 [{"A": "II", "B": "IV", "C": "III", "D": "I"},
                  {"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "I", "B": "II", "C": "III", "D": "IV"}]),
  why="Budworms and armyworms are caterpillars (lepidopterans), beetles are coleopterans and flies and mosquitoes "
      "are dipterans; cryIAb is NCERT's corn borer gene. Each wrong code swaps one of these pairs.", secs=40)

Z(BTA, "Human insulin", I, STP,
  SP("Eli Lilly produced pro-insulin containing the C peptide in E. coli and then processed it into mature insulin.",
     "In Eli Lilly's method, chains A and B were produced separately, extracted and combined by creating "
     "disulphide bonds to form human insulin."),
  "How recombinant human insulin was made",
  "NCERT: in 1983, Eli Lilly prepared two DNA sequences corresponding to the A and B chains of human insulin and "
  "introduced them into plasmids of E. coli to produce insulin chains. Chains A and B were produced separately, "
  "extracted and combined by creating disulphide bonds to form human insulin. No pro-insulin with a C peptide was "
  "made. Statement I is false; Statement II is true.",
  ["Two separate DNA sequences for A and B chains", "No pro-insulin route -> I false", "Separate chains + "
   "disulphide bonds -> II true"],
  "Biotechnological applications in medicine (genetically engineered insulin)", ans="D",
  why="Statement I describes the pro-hormone route of the body, not Eli Lilly's method, so it is false; Statement "
      "II is NCERT's description.", secs=40)

Z(BTA, "Gene therapy", I, ASR,
  AR("Gene therapy for ADA deficiency using the patient's genetically engineered lymphocytes is not a "
     "permanent cure.",
     "Lymphocytes cannot be grown in a culture outside the body."),
  "Limitation of lymphocyte gene therapy",
  "NCERT: in this gene therapy, lymphocytes from the patient's blood are grown in a culture outside the body, "
  "given a functional ADA cDNA and returned; as these cells are not immortal, the patient requires periodic "
  "infusion of such lymphocytes. So A is true. R is false, because NCERT describes exactly such culturing.",
  ["Cells not immortal -> periodic infusion -> not permanent: A true", "Lymphocytes are cultured outside the body "
   "-> R false"],
  "Biotechnological applications in medicine (gene therapy)", ans="C",
  why="R contradicts NCERT's procedure, so options calling R true are wrong; A is true.", secs=35)

Z(BTA, "Bt crops and RNAi", I, D,
  "Suppose an insect with an acidic (not alkaline) gut feeds on a Bt crop. Using NCERT's account of how Bt toxin "
  "works, which outcome is most likely?",
  "Activation of Bt protoxin",
  "NCERT: the Bt toxin protein exists as an inactive protoxin; once an insect ingests it, it is converted into an "
  "active form of toxin due to the alkaline pH of the gut, which solubilises the crystals. The activated toxin "
  "binds to the surface of midgut epithelial cells and creates pores, causing swelling, lysis and death. Without "
  "alkaline pH, the protoxin would not be solubilised and activated, so the insect would likely survive.",
  ["Protoxin is inactive", "Alkaline gut pH solubilises and activates it", "No activation -> no pores -> insect "
   "survives"],
  "Biotechnological applications in agriculture",
  at="A", correct="The protoxin is not solubilised and activated, so the insect is unlikely to be killed",
  wrong=["The toxin is activated even faster and kills the insect sooner",
         "The toxin now kills the crop plant instead of the insect",
         "The toxin dissolves the insect's exoskeleton from outside"],
  why="NCERT ties activation specifically to alkaline pH, so faster activation in acid is not supported; the "
      "plant is never the target; Bt toxin acts on midgut cells, not the exoskeleton.", secs=45)

Z(BTA, "Transgenic animals", I, STP,
  SP("Many transgenic animals are specially made to serve as models for human diseases, so that investigation of "
     "new treatments for those diseases becomes possible.",
     "Transgenic animals made more sensitive to toxic substances than non-transgenic animals give results of "
     "toxicity testing in less time."),
  "Uses of transgenic animals",
  "NCERT: study of disease - many transgenic animals are specially made to serve as models for human diseases so "
  "that investigation of new treatments is made possible (transgenic models exist for cancer, cystic fibrosis, "
  "rheumatoid arthritis and Alzheimer's). Chemical safety testing - transgenic animals carrying genes that make "
  "them more sensitive to toxic substances are exposed to them and their effects studied, which allows results "
  "in less time. Both statements are true.",
  ["Disease models -> I true", "More sensitive animals -> quicker toxicity results -> II true"],
  "Transgenic animals", ans="A",
  why="Both statements restate NCERT's reasons for producing transgenic animals, so options calling either false "
      "are wrong.", secs=40)

Z(BTA, "Bt crops and RNAi", A, ASR,
  AR("A crop made transgenic with only the cryIAb gene can be expected to resist the corn borer, but not "
     "necessarily the cotton bollworm.",
     "Most Bt toxins are insect-group specific, so the choice of Bt toxin genes depends upon the crop and the "
     "targeted pest."),
  "Specificity of Bt toxins",
  "NCERT: the proteins encoded by cryIAc and cryIIAb control cotton bollworms, while that of cryIAb controls corn "
  "borer; specific Bt toxin genes are chosen according to the crop and the targeted pest, since most Bt toxins "
  "are insect-group specific. Because toxins are specific, a cryIAb-only crop targets the corn borer and cannot "
  "be assumed to control bollworms - R explains A.",
  ["cryIAb -> corn borer", "cryIAc, cryIIAb -> bollworms", "Toxins are pest-specific -> R explains A"],
  "Biotechnological applications in agriculture", ans="A",
  why="Both statements are true and the specificity of Bt toxins in R is exactly why A holds, so B, C and D are "
      "wrong.", secs=45)

Z(BTA, "Human insulin", A, D,
  "According to NCERT, what was the main challenge in producing human insulin by recombinant DNA techniques?",
  "Problem of assembling mature insulin",
  "NCERT: in mammals, including humans, insulin is synthesised as a pro-hormone with an extra C peptide that is "
  "removed during maturation. The main challenge for production of insulin using rDNA techniques was getting "
  "insulin assembled into a mature form. Eli Lilly overcame this by making chains A and B separately and joining "
  "them by disulphide bonds.",
  ["Body makes pro-insulin and processes it", "Challenge: assembling mature insulin",
   "Solution: separate A and B chains joined by disulphide bonds"],
  "Biotechnological applications in medicine (genetically engineered insulin)",
  at="C", correct="Getting insulin assembled into a mature form",
  wrong=["Finding any bacterium that could take up plasmids", "Synthesising the amino acids needed for the chains",
         "Preventing insulin from being digested by E. coli ribonuclease"],
  why="Transforming E. coli with plasmids was routine; making the polypeptide chains was not described as the "
      "difficulty; a ribonuclease digests RNA, not proteins such as insulin.", secs=40)

Z(BTA, "Bt crops and RNAi", A, D,
  "A plant breeder wants a single transgenic tobacco line that resists both a root-infecting nematode and "
  "lepidopteran caterpillars. Based on the NCERT examples, which combination of strategies is suitable?",
  "Combining RNAi and Bt approaches",
  "NCERT: tobacco was made resistant to the nematode Meloidegyne incognitia by RNAi - nematode-specific genes "
  "introduced with Agrobacterium vectors produce sense and anti-sense RNA, forming dsRNA that silences a specific "
  "nematode mRNA. Insect resistance comes from Bt toxin genes (cry genes) of Bacillus thuringiensis, some of "
  "whose proteins kill lepidopterans such as the tobacco budworm.",
  ["Nematode: RNAi with nematode-specific genes (Agrobacterium vector)", "Caterpillars: suitable cry genes from "
   "B. thuringiensis"],
  "Biotechnological applications in agriculture",
  at="D", correct="RNAi using nematode-specific genes, plus cry genes from Bacillus thuringiensis that act on "
                  "lepidopterans",
  wrong=["cry genes alone, since all Bt toxins kill nematodes too",
         "RNAi alone, using sense RNA of the caterpillar's genes without any anti-sense RNA",
         "Introducing the ADA gene with a retroviral vector"],
  why="NCERT's nematode protection used RNAi, not Bt toxins; RNAi needs both sense and anti-sense RNA to form "
      "dsRNA; the ADA gene and retroviral vector belong to human gene therapy.", secs=55)

Z(BTA, "Bt crops and RNAi", A, ASR,
  AR("Golden rice is a genetically modified crop enriched in vitamin A.",
     "Bt toxin genes have been expressed in plants such as cotton, corn, rice, tomato, potato and soyabean."),
  "Golden rice and Bt crops",
  "Both statements are NCERT facts: golden rice is a GM crop with enhanced nutritional value (vitamin A "
  "enriched), and Bt toxin genes have been expressed in several crops including rice. But insect resistance "
  "from Bt genes has nothing to do with the vitamin A content of golden rice, so R does not explain A.",
  ["A true: vitamin A-enriched rice", "R true: Bt genes in several crops", "Pest resistance does not explain "
   "vitamin A enrichment"],
  "Biotechnological applications in agriculture", ans="B",
  why="Both statements are true, so C and D are wrong; R is about insect resistance, a different trait, so it is "
      "not the explanation of A.", secs=40)

Z(BTA, "Bt crops and RNAi", A, MAT,
  ML(("organism", "role in the NCERT examples of applied biotechnology"),
     ["Bacillus thuringiensis", "Agrobacterium", "Meloidegyne incognitia", "Escherichia coli"],
     ["Host whose plasmids carried DNA sequences for the A and B chains of human insulin",
      "Parasite of tobacco roots, controlled by RNA interference",
      "Source of the cry genes that make crops insect-resistant",
      "Source of vectors used to introduce nematode-specific genes into tobacco"]),
  "Organisms in biotechnological applications",
  "NCERT: Bt toxin genes (cry) come from Bacillus thuringiensis; nematode-specific genes were introduced into "
  "tobacco using Agrobacterium vectors; Meloidegyne incognitia infects tobacco roots and was controlled by RNAi; "
  "Eli Lilly introduced DNA for insulin chains A and B into plasmids of E. coli.",
  ["B. thuringiensis -> III", "Agrobacterium -> IV", "Meloidegyne -> II", "E. coli -> I"],
  "Biotechnological applications in agriculture; Biotechnological applications in medicine",
  at="B", match=({"A": "III", "B": "IV", "C": "II", "D": "I"},
                 [{"A": "IV", "B": "III", "C": "II", "D": "I"},
                  {"A": "III", "B": "IV", "C": "I", "D": "II"},
                  {"A": "III", "B": "II", "C": "IV", "D": "I"}]),
  why="B. thuringiensis supplies genes while Agrobacterium supplies vectors; Meloidegyne is the pest and E. coli "
      "the insulin host. Each wrong code swaps one of these pairs.", secs=45)

# ================================================================ checks and output
if __name__ == "__main__":
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, sorted((set(have.items()) ^ set(planned.items())))
    assert len(QUESTIONS) == pkg["count"] == 128
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_006", "created_at": TODAY,
           "notes": "ZOO_006_p2: 128 original Zoology questions (Chemical Coordination and Integration, Human "
                    "Reproduction, Reproductive Health, Evolution, Human Health and Disease, Biotechnology: "
                    "Principles and Processes, Biotechnology and its Applications). Facts from rationalised NCERT; "
                    "numerical answers re-derived in tools/batch_006/ZOO_006_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QUESTIONS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QUESTIONS)))
